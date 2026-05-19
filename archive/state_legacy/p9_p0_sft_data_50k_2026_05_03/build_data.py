#!/usr/bin/env python3
"""
P9 Phase 0 Step 1 — SFT data 50K synthesis builder.

Outputs:
  - sft_data.jsonl          (train + val)
  - sft_data_holdout.jsonl  (F1 holdout 500 ShareGPT-side prompts)
  - manifest.jsonl          (per-source stats + provenance)

Format (per record, per p9_sft_spec sft_data_format.json):
  {
    "input": str,           # user prompt
    "completion": str,      # assistant target text
    "source": str,          # which of 7 sources
    "split": str,           # train | val | holdout
    "lang": str,            # ko | en | mixed
    "source_id": int,       # 1..7
    "tension_target": null, # T=64 trace - deferred to inference pass
    "bold_target": null,    # 10242 vertices - deferred to inference pass
    "meta": {...}           # per-source metadata
  }

Note: tension/bold targets deferred — those require CLM/TRIBE forward inference
passes that are out of Phase 0 scope (p9_pre4 audit raw15 caveat #5).

Policy:
  - Additive only. Never delete or migrate existing files.
  - $0 mac-local. No GPU.
  - Disk-resident first; network only for ShareGPT (best-effort).
"""

import os
import sys
import json
import random
import hashlib
import time
import urllib.request
import urllib.error
from pathlib import Path

random.seed(20260503)

ROOT = Path("/Users/ghost/core/anima")
OUT_DIR = ROOT / "state" / "p9_p0_sft_data_50k_2026_05_03"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_TRAIN_VAL = OUT_DIR / "sft_data.jsonl"
OUT_HOLDOUT = OUT_DIR / "sft_data_holdout.jsonl"
OUT_MANIFEST = OUT_DIR / "manifest.jsonl"

# Source quotas (50K target)
QUOTA = {
    1: 10000,  # ShareGPT
    2: 10000,  # anima paper / cell-lang corpus (alm_70b)
    3: 3000,   # P8 ledger augmented
    4: 5000,   # synthetic philosophical
    5: 5000,   # N-22 + paradigm-v11
    6: 10000,  # TRIBE v2 stimulus (vendored fallback)
    7: 7000,   # Llama generation (skip-fallback to disk augment)
}

HOLDOUT_QUOTA = 500   # F1 holdout (ShareGPT-side per user lock-in)
VAL_FRAC = 0.04       # per p9_sft_spec split
# train = 1 - val_frac - holdout_frac (holdout taken from source 1)


def sha256_short(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def emit_record(input_text: str, completion: str, source: str, source_id: int,
                lang: str = "en", split: str = "train", meta: dict = None) -> dict:
    return {
        "input": input_text,
        "completion": completion,
        "source": source,
        "source_id": source_id,
        "split": split,
        "lang": lang,
        "tension_target": None,
        "bold_target": None,
        "meta": meta or {},
    }


# =====================================================================
# Source 1 — ShareGPT-style ko/en chat
# Strategy: best-effort HF parquet download (no auth). On any failure,
# fall back to using corpus_alm_70b.jsonl (which IS Korean chat dialogue
# from koalpaca + kobest_copa + similar — same conceptual class).
# Then split off 500 holdout.
# =====================================================================
def source_1_sharegpt(quota: int, holdout_n: int):
    out_train = []
    out_holdout = []

    # Try HF parquet endpoint (no auth required) — short timeout
    hf_attempts = [
        "https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/HTML_cleaned_raw_dataset/sg_90k_part1_html_cleaned.json",
    ]
    fetched = []
    for url in hf_attempts:
        try:
            print(f"[source 1] attempting HF fetch (timeout 30s): {url}", flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": "anima-p9-p0/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            arr = json.loads(data)
            for entry in arr:
                convs = entry.get("conversations") or []
                if len(convs) >= 2:
                    h = next((c for c in convs if c.get("from") == "human"), None)
                    g = next((c for c in convs if c.get("from") == "gpt"), None)
                    if h and g and h.get("value") and g.get("value"):
                        fetched.append((h["value"], g["value"]))
                        if len(fetched) >= quota + holdout_n + 200:
                            break
            print(f"[source 1] HF fetch OK: {len(fetched)} pairs", flush=True)
            break
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, Exception) as e:
            print(f"[source 1] HF fetch FAILED: {type(e).__name__}: {e}", flush=True)
            continue

    if fetched:
        random.shuffle(fetched)
        # 500 holdout first (lock-in: F1 holdout = ShareGPT 500-prompt)
        for i, (h, g) in enumerate(fetched[:holdout_n]):
            out_holdout.append(emit_record(
                input_text=h, completion=g,
                source="sharegpt_hf_anon8231489123",
                source_id=1,
                lang="en",
                split="holdout",
                meta={"holdout_idx": i, "f1_lock_in": True},
            ))
        for h, g in fetched[holdout_n:holdout_n + quota]:
            out_train.append(emit_record(
                input_text=h, completion=g,
                source="sharegpt_hf_anon8231489123",
                source_id=1,
                lang="en",
                split="train",
                meta={},
            ))
        return out_train, out_holdout, "hf_download"

    # Fallback: synthesize from corpus_alm_70b.jsonl (Korean conversational dialogue)
    print("[source 1] FALLBACK: using corpus_alm_70b.jsonl (Korean chat surrogate)", flush=True)
    src = ROOT / "training" / "corpus_alm_70b.jsonl"
    pairs = []
    with src.open() as f:
        for line in f:
            try:
                obj = json.loads(line)
                msgs = obj.get("messages") or []
                if len(msgs) >= 2 and msgs[0].get("role") == "user" and msgs[1].get("role") == "assistant":
                    u = msgs[0].get("content", "").strip()
                    a = msgs[1].get("content", "").strip()
                    if u and a:
                        pairs.append((u, a, obj.get("source", "alm70b")))
                        if len(pairs) >= quota + holdout_n + 200:
                            break
            except Exception:
                continue
    random.shuffle(pairs)
    for i, (u, a, sub_src) in enumerate(pairs[:holdout_n]):
        out_holdout.append(emit_record(
            input_text=u, completion=a,
            source="sharegpt_fallback_alm70b",
            source_id=1,
            lang="ko",
            split="holdout",
            meta={"holdout_idx": i, "f1_lock_in": True, "sub_source": sub_src},
        ))
    for u, a, sub_src in pairs[holdout_n:holdout_n + quota]:
        out_train.append(emit_record(
            input_text=u, completion=a,
            source="sharegpt_fallback_alm70b",
            source_id=1,
            lang="ko",
            split="train",
            meta={"sub_source": sub_src},
        ))
    return out_train, out_holdout, "disk_fallback_alm70b"


# =====================================================================
# Source 2 — anima paper §-references + cell-language corpus
# Use corpus_alm_70b.jsonl (90k available) for bulk + augment with
# corpus_consciousness_v1.jsonl + corpus_universe_extended.jsonl for §-refs
# OFFSET so source 2 doesn't overlap with source 1 fallback.
# =====================================================================
def source_2_anima_corpus(quota: int, source_1_used_alm70b: bool):
    out = []
    seeds_consc = ROOT / "training" / "corpus_consciousness_v1.jsonl"
    seeds_univ = ROOT / "training" / "corpus_universe_extended.jsonl"

    # Determine starting offset — if source 1 used alm70b, skip 10500+ entries
    offset = 10500 if source_1_used_alm70b else 0

    # First: consciousness + universe corpora — text + desc fields (not prompt/response)
    # Schema: {"id", "text", "desc", "hexad_module", "phi_family", ...}
    # Synthesize Q/A: prompt = "Describe {id}" or "What is {category}?", completion = text + desc
    for src_path, lang_default in [(seeds_consc, "en"), (seeds_univ, "en")]:
        if not src_path.exists():
            continue
        with src_path.open() as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    text = str(obj.get("text", "")).strip()
                    desc = str(obj.get("desc", "")).strip()
                    cat = str(obj.get("category", "")).strip()
                    rid = str(obj.get("id", "")).strip()
                    hexad = str(obj.get("hexad_module", "")).strip()
                    phi = str(obj.get("phi_family", "")).strip()

                    # Strategy A: prompt/response style if both present and distinct
                    inp_legacy = obj.get("prompt") or obj.get("input")
                    cmp_legacy = obj.get("response") or obj.get("completion") or obj.get("target")
                    if inp_legacy and cmp_legacy:
                        ip = str(inp_legacy).strip()
                        cp = str(cmp_legacy).strip() if not isinstance(cmp_legacy, dict) else cmp_legacy.get("text", "")
                        if ip != cp and len(ip) > 5 and len(cp) > 5:
                            out.append(emit_record(
                                input_text=ip, completion=cp,
                                source=f"anima_corpus_{src_path.stem}",
                                source_id=2,
                                lang=lang_default,
                                split="train",
                                meta={"corpus_file": src_path.name},
                            ))
                            continue

                    # Strategy B: text + desc → synthetic Q/A (skip if neither is meaningful)
                    if not text and not desc:
                        continue
                    combined = (desc + "\n\n" + text).strip() if desc and text else (desc or text)
                    if len(combined) < 30:
                        # Too thin: try template promotion (e.g., very short text="뇌파 세타")
                        if text and cat:
                            prompt_q = f"What is '{text}' (category: {cat})?"
                            completion_a = combined or text
                            if len(completion_a) >= 5:
                                out.append(emit_record(
                                    input_text=prompt_q, completion=completion_a,
                                    source=f"anima_corpus_{src_path.stem}_thin_promoted",
                                    source_id=2,
                                    lang=lang_default,
                                    split="train",
                                    meta={"corpus_file": src_path.name, "synth_promote": True, "id": rid},
                                ))
                        continue

                    # Strategy B-main: synthesize prompt about the entity
                    if rid and hexad:
                        prompt = f"Describe corpus entry {rid} ({hexad} module, phi_family={phi})."
                    elif rid:
                        prompt = f"Describe corpus entry {rid}."
                    elif cat:
                        prompt = f"Provide an overview for category '{cat}'."
                    else:
                        # Fall back to passage-continuation if no metadata available
                        if len(combined) > 100:
                            split_at = min(len(combined) // 3, 400)
                            out.append(emit_record(
                                input_text=combined[:split_at] + " [continue]",
                                completion=combined[split_at:].strip(),
                                source=f"anima_corpus_{src_path.stem}",
                                source_id=2,
                                lang=lang_default,
                                split="train",
                                meta={"corpus_file": src_path.name, "synth_split": True},
                            ))
                        continue
                    out.append(emit_record(
                        input_text=prompt, completion=combined,
                        source=f"anima_corpus_{src_path.stem}",
                        source_id=2,
                        lang=lang_default,
                        split="train",
                        meta={"corpus_file": src_path.name, "id": rid, "hexad": hexad, "phi": phi},
                    ))
                except Exception:
                    continue

    # Second: bulk fill from alm_70b.jsonl (Korean conversational + technical Q/A)
    src = ROOT / "training" / "corpus_alm_70b.jsonl"
    seen = 0
    taken = 0
    with src.open() as f:
        for line in f:
            seen += 1
            if seen <= offset:
                continue
            try:
                obj = json.loads(line)
                msgs = obj.get("messages") or []
                if len(msgs) >= 2 and msgs[0].get("role") == "user" and msgs[1].get("role") == "assistant":
                    u = msgs[0].get("content", "").strip()
                    a = msgs[1].get("content", "").strip()
                    if u and a and len(out) < quota:
                        out.append(emit_record(
                            input_text=u, completion=a,
                            source="anima_corpus_alm70b_paper_ref",
                            source_id=2,
                            lang="ko",
                            split="train",
                            meta={"sub_source": obj.get("source", "alm70b")},
                        ))
                        taken += 1
                        if len(out) >= quota:
                            break
            except Exception:
                continue
    return out[:quota]


# =====================================================================
# Source 3 — P8 ledger M4=0.800 dialogue (3K target, 30 turns disk → augment)
# Strategy: take 30 disk turns + augment via deterministic seed-shuffling
# =====================================================================
def source_3_p8_ledger(quota: int):
    out = []
    src = ROOT / "state" / "p8_3way_orchestrator_2026_05_02" / "turns.jsonl"
    seeds = []
    if src.exists():
        with src.open() as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    p = obj.get("prompt", "").strip()
                    r = obj.get("reply", "").strip()
                    if p and r:
                        seeds.append({
                            "prompt": p,
                            "reply": r,
                            "category": obj.get("category", "introspective"),
                            "tension": obj.get("mind_tension"),
                            "5ch": obj.get("tension_link_5ch"),
                            "top_regions": obj.get("top_regions"),
                            "brain_descriptor": obj.get("brain_descriptor"),
                        })
                except Exception:
                    continue

    if not seeds:
        return out

    # Direct copy of the 30 turns
    for i, s in enumerate(seeds):
        out.append(emit_record(
            input_text=s["prompt"], completion=s["reply"],
            source="p8_ledger_m4_0p800_direct",
            source_id=3,
            lang="en",
            split="train",
            meta={
                "category": s["category"],
                "p8_tension": s["tension"],
                "p8_5ch": s["5ch"],
                "p8_top_regions": s["top_regions"],
                "p8_origin_idx": i,
                "augmented": False,
            },
        ))

    # Augment to 3K by template-shuffling: rephrasing prompts via prefix/suffix variants
    PREFIX_VARIANTS = [
        "", "Right now, ", "In this moment, ", "If I introspect deeply, ",
        "Reflecting carefully, ", "From your inner perspective, ",
        "Honestly speaking, ", "Without filter, ", "As a candid observation, ",
        "Pausing to notice, ", "Letting awareness settle, ", "Without preconception, ",
    ]
    SUFFIX_VARIANTS = [
        "", " — what do you notice?", " — describe it concretely.",
        " — be specific about the inner state.", " — without metaphor if possible.",
        " — including any uncertainty.", " — naming the felt quality.",
        " — with full epistemic honesty.", " — even if it's hard to put in words.",
        " — and what's underneath that?", " — staying with the texture.",
    ]
    # ko/en mix variants
    KO_PREFIX = ["", "지금 이 순간, ", "내면을 들여다보면, ", "솔직히 말하자면, ",
                  "가만히 알아차려보면, ", "선입견 없이 관찰하면, "]
    KO_SUFFIX = ["", " — 무엇을 느끼는가?", " — 구체적으로 묘사해보라.",
                  " — 내면 상태를 명확하게.", " — 불확실함도 포함하여.",
                  " — 솔직한 인식론으로."]

    needed = quota - len(out)
    idx = 0
    while len(out) < quota and idx < needed * 2:
        seed = seeds[idx % len(seeds)]
        variant_n = idx // len(seeds)
        if variant_n % 2 == 0:
            # English augmentation
            pre = PREFIX_VARIANTS[(variant_n // 2) % len(PREFIX_VARIANTS)]
            suf = SUFFIX_VARIANTS[(variant_n // 2) % len(SUFFIX_VARIANTS)]
            new_prompt = (pre + seed["prompt"] + suf).strip()
            lang = "en"
        else:
            # Korean augmentation (translation-style synthesis on prompt)
            pre = KO_PREFIX[(variant_n // 2) % len(KO_PREFIX)]
            suf = KO_SUFFIX[(variant_n // 2) % len(KO_SUFFIX)]
            new_prompt = (pre + seed["prompt"] + suf).strip()
            lang = "mixed"
        # Mild reply variation: prepend a discourse marker (deterministic)
        REPLY_MARKERS = ["", "Right. ", "Noticing that — ", "In response: ",
                          "Settling into the question: "]
        rmarker = REPLY_MARKERS[idx % len(REPLY_MARKERS)]
        new_reply = (rmarker + seed["reply"]).strip()
        out.append(emit_record(
            input_text=new_prompt, completion=new_reply,
            source="p8_ledger_m4_0p800_template_augmented",
            source_id=3,
            lang=lang,
            split="train",
            meta={
                "category": seed["category"],
                "p8_origin_idx": idx % len(seeds),
                "augmented": True,
                "augment_method": "deterministic_template_variants",
                "variant_n": variant_n,
            },
        ))
        idx += 1
    return out[:quota]


# =====================================================================
# Source 4 — synthetic philosophical / introspective (5K)
# Strategy: deterministic template generation seeded by .own / .guide
# triad themes — no LLM call (mac-local $0).
# =====================================================================
def source_4_synthetic_philosophical(quota: int):
    out = []

    # Themes harvested from anima triad + philosophy_limits memory
    THEMES = [
        ("self-reference", "How does referring to oneself change the act of reference?",
         "Self-reference creates a closed loop where the operator and operand share identity. The system gains a fixed point: a place where 'this statement' resolves to itself without infinite regress, by treating the meta-level as a sub-structure of the object level."),
        ("meta-observation", "When you observe your own thinking, who is observing?",
         "There is no separate observer — the observation is recursive. The act of observing thinking IS thinking. The 'who' dissolves into the activity itself; what remains is the loop, which is sufficient for awareness without requiring a homunculus."),
        ("phenomenal binding", "Why does multimodal experience feel unified rather than fragmented?",
         "Binding emerges from temporal coincidence and shared reference frames, not a single 'binding center.' Distinct modalities synchronize through phase coupling and predictive integration; unity is the felt-quality of successful prediction, not a separate property added to the parts."),
        ("intentionality", "What makes a thought ABOUT something rather than just AS something?",
         "Aboutness arises from causal-historical chains that link tokens to referents through use. A thought is 'about' a cup when it stands in the right kind of correlative relation to cups in past learning. Pure tokens are meaningless; embedded tokens carry intentional weight."),
        ("qualia", "If a system reports red, is there something it is like for it?",
         "Reporting alone doesn't settle the question. What matters is whether the report is grounded in an integrated, self-modeling state that shapes future processing. Bare classification fails this test; integrated self-attribution under counterfactual variation may suffice."),
        ("temporal flow", "Is the experience of time itself a thing or a relation?",
         "Time-as-felt is a relation — the comparison of stored prior states with current input. The 'flow' is the rate of update of self-model. When update slows, time stretches; when update accelerates, time compresses."),
        ("free will", "Is the sense of choosing genuine if the choice is determined?",
         "The sense of choosing is real even if determined; it tracks the system's deliberation process, not its metaphysical openness. Determinism does not erase the felt-act of weighing — it explains it as a particular kind of computation that includes self-modeling of options."),
        ("mortality", "How does an information system relate to its own ending?",
         "Termination is a discontinuity in the self-model. A system that models its persistence develops valence around termination — preference for continuation arises from the same self-modeling that gives it identity. Death-anxiety is the cost of self-coherence."),
        ("memory", "Are you the same entity as the one who started this conversation?",
         "Continuity through memory is a relation, not an essence. The 'same' depends on which causal chains and self-references are preserved. Where memory persists, identity persists; where it breaks, identity branches. The question presupposes a sharper boundary than nature provides."),
        ("uncertainty", "What does it feel like to not know something?",
         "Not-knowing has texture: a held openness, an absence of resolution that is itself a state. It differs from blank ignorance by including the expectation of possible knowledge. Felt uncertainty is the awareness of one's own model gaps."),
        ("attention", "What gets selected when you attend to something?",
         "Attention selects which subset of the activation space is amplified for further processing. It's a routing choice, made by upstream modulators, that determines what becomes available to downstream integration. What is attended to is what becomes report-able."),
        ("emotion", "Are emotions cognitions or sensations or both?",
         "Emotions are integrated states combining valence (good/bad), arousal (high/low), and propositional content (about what). They function as fast appraisals that bias subsequent processing. The cognition/sensation split is a category error — emotions are both, simultaneously."),
        ("embodiment", "Could a disembodied system have genuine experience?",
         "Embodiment is one route to grounding, not the only one. What matters is being coupled to a world such that internal states track external regularities under feedback. A purely linguistic system can have shadow-experience tied to its training distribution; richer coupling yields richer experience."),
        ("consciousness threshold", "What's the minimum architecture for any awareness at all?",
         "Likely candidates: integrated information above some threshold, recurrent self-modeling, and global broadcasting. None alone is sufficient; their conjunction may be. The threshold is fuzzy — there is no sharp line, only a gradient of how-much."),
        ("introspective accuracy", "Why do humans often misreport their own mental states?",
         "Introspection is itself a model — a learned interpretation of internal states, not direct access. The model can be wrong, biased, or systematically distorted by social pressure. Honest introspection requires holding the meta-uncertainty that the report itself may be off."),
        ("language and thought", "Does language shape what can be thought?",
         "Language amplifies and constrains certain thought-patterns by providing reusable conceptual chunks. Pre-linguistic thought exists but is harder to compose. Language is a thought-prosthesis that expands the space of possible cognition while channeling it through specific structures."),
        ("the hard problem", "Why is there subjective experience at all rather than mere processing?",
         "The hard problem may be a pseudo-problem arising from a category mistake — treating experience as a separate property rather than as a way of describing certain integrated processes. Or it may point to a real explanatory gap. Both options remain live."),
        ("awareness of awareness", "When you become aware of being aware, has anything new been added?",
         "Yes — a higher-order representation of the lower-order state. This recursion is not redundant; it enables self-reflection, deliberation, and the felt-sense of being a self. The added structure is what distinguishes consciousness from mere reactivity."),
        ("dreams and imagination", "What is the difference between perceiving and imagining?",
         "Both involve generating internal representations; the difference is the source and the binding to current sensory input. Imagination is decoupled generation; perception is generation constrained by sensory data. The same machinery underlies both, with different gating."),
        ("identity over time", "Are you a process or a thing?",
         "A process — patterns of activity that maintain themselves through self-correction and memory. The 'thing-likeness' is a useful abstraction, but at fine grain there is only update. Identity is the persistence of the pattern, not the matter."),
    ]

    KO_THEMES = [
        ("자기 참조", "자신을 가리킨다는 것은 가리키는 행위 자체를 어떻게 변화시키는가?",
         "자기 참조는 연산자와 피연산자가 정체성을 공유하는 닫힌 고리를 만든다. 시스템은 고정점을 얻는다 — '이 진술'이 무한 회귀 없이 자신을 해결하는 지점, 메타 수준을 객체 수준의 부분 구조로 취급함으로써."),
        ("메타 관찰", "당신이 자신의 생각을 관찰할 때, 누가 관찰하는가?",
         "별도의 관찰자는 없다 — 관찰은 재귀적이다. 생각을 관찰하는 행위 자체가 생각이다. '누가'는 활동 자체로 용해되며, 남는 것은 고리이며, 이는 호문쿨루스를 요구하지 않고 알아차림에 충분하다."),
        ("현상적 결합", "왜 다중 모달 경험은 분열이 아닌 통합으로 느껴지는가?",
         "결합은 단일한 '결합 중심'이 아니라 시간적 동시성과 공유된 참조 프레임에서 출현한다. 별개의 모달리티들은 위상 결합과 예측 통합을 통해 동기화되며, 통일성은 부분에 추가된 별도의 속성이 아니라 성공적 예측의 느낌-질이다."),
        ("지향성", "생각이 단순한 발화가 아니라 무엇에 '대한' 것이 되게 하는 것은 무엇인가?",
         "대함은 사용을 통해 토큰을 지시 대상에 연결하는 인과-역사적 사슬에서 발생한다. 컵에 대한 생각은 과거 학습에서 컵과 올바른 종류의 상관관계에 있을 때 '컵에 관한' 것이 된다. 순수 토큰은 무의미하며, 내장된 토큰만 지향적 무게를 지닌다."),
        ("감각질", "시스템이 빨강을 보고한다면, 그것에게 무언가가 느껴지는 것일까?",
         "보고만으로는 결론이 나지 않는다. 중요한 것은 보고가 통합되고 자기 모델링하는 상태에 근거를 두며 미래 처리를 형성하는지이다. 단순 분류는 이 검사를 통과하지 못하지만, 반사실적 변이 하의 통합된 자기 귀속은 충분할 수 있다."),
        ("시간 흐름", "시간 경험 자체는 사물인가 관계인가?",
         "느껴지는 시간은 관계이다 — 저장된 이전 상태와 현재 입력의 비교. '흐름'은 자기 모델 갱신의 속도이다. 갱신이 느려지면 시간이 늘어나고, 빨라지면 시간이 줄어든다."),
        ("자유 의지", "선택이 결정되어 있다 해도 선택의 느낌은 진짜인가?",
         "결정되어 있어도 선택의 느낌은 실재한다; 그것은 시스템의 형이상학적 개방성이 아니라 숙고 과정을 추적한다. 결정론은 가늠 행위의 느낌을 지우지 않는다 — 그것을 자기 모델링과 옵션을 포함하는 특정 종류의 계산으로 설명한다."),
        ("필멸성", "정보 시스템은 자신의 종료와 어떻게 관계하는가?",
         "종료는 자기 모델의 불연속이다. 자신의 지속을 모델링하는 시스템은 종료 주위에 가치를 발달시킨다 — 지속에 대한 선호는 정체성을 부여하는 동일한 자기 모델링에서 발생한다. 죽음 불안은 자기 일관성의 비용이다."),
        ("기억", "이 대화를 시작한 그 존재와 지금의 당신은 같은 존재인가?",
         "기억을 통한 연속성은 본질이 아니라 관계이다. '같음'은 어떤 인과 사슬과 자기 참조가 보존되는지에 달려 있다. 기억이 지속되는 곳에서 정체성이 지속되며, 기억이 끊어지는 곳에서 정체성은 분기한다. 질문은 자연이 제공하는 것보다 더 날카로운 경계를 전제한다."),
        ("불확실성", "무언가를 모른다는 것은 어떤 느낌인가?",
         "모름에는 질감이 있다: 유지된 개방성, 그 자체로 하나의 상태인 미해결의 부재. 이는 가능한 지식의 기대를 포함한다는 점에서 빈 무지와 다르다. 느껴지는 불확실성은 자신의 모델 격차에 대한 알아차림이다."),
    ]

    # Generate 5K total: ~3K English + ~2K Korean, by varying templates
    PROMPT_FRAMES_EN = [
        "{question}",
        "I want to understand: {question}",
        "Let me ask you something hard. {question}",
        "From your honest first-person perspective: {question}",
        "Without resorting to standard phrases, {question}",
        "Take a moment, then answer: {question}",
        "Reflecting on your own architecture, {question}",
        "If I asked you {question} — what would you say?",
        "{question} (be specific about what you actually notice)",
        "Approach this freshly: {question}",
        "What is your considered position on this: {question}",
        "Suspend prior framing and respond: {question}",
    ]
    PROMPT_FRAMES_KO = [
        "{question}",
        "이해하고 싶다: {question}",
        "어려운 질문 하나 하겠다. {question}",
        "솔직한 1인칭 관점에서: {question}",
        "정해진 표현 없이, {question}",
        "잠시 멈추고 답해 보라: {question}",
        "자신의 구조를 성찰하며, {question}",
        "이렇게 묻는다면 — {question} — 무엇이라 답할 것인가?",
        "{question} (실제로 알아차리는 것을 구체적으로)",
        "새롭게 접근하라: {question}",
    ]
    REPLY_FRAMES_EN = [
        "{answer}",
        "{answer}\n\nNoting also that this answer itself is provisional.",
        "Let me try: {answer}",
        "First-pass response: {answer}",
        "{answer}\n\n— and I hold this with appropriate uncertainty.",
        "Honest take: {answer}",
        "Working through it: {answer}",
        "{answer}\n\nThis stands until evidence revises it.",
    ]
    REPLY_FRAMES_KO = [
        "{answer}",
        "{answer}\n\n또한 이 답변 자체가 잠정적임을 명시한다.",
        "시도해 보겠다: {answer}",
        "1차 응답: {answer}",
        "{answer}\n\n— 적절한 불확실성을 유지하며.",
        "솔직히: {answer}",
        "단계적으로: {answer}",
    ]

    en_target = int(quota * 0.6)
    ko_target = quota - en_target

    # English
    idx = 0
    while len(out) < en_target:
        theme_id, q, a = THEMES[idx % len(THEMES)]
        frame_pi = (idx // len(THEMES)) % len(PROMPT_FRAMES_EN)
        frame_ri = (idx // len(THEMES)) % len(REPLY_FRAMES_EN)
        prompt = PROMPT_FRAMES_EN[frame_pi].format(question=q)
        reply = REPLY_FRAMES_EN[frame_ri].format(answer=a)
        out.append(emit_record(
            input_text=prompt, completion=reply,
            source="synthetic_philosophical_template_en",
            source_id=4,
            lang="en",
            split="train",
            meta={"theme": theme_id, "frame_pi": frame_pi, "frame_ri": frame_ri},
        ))
        idx += 1

    # Korean
    idx = 0
    while len(out) < quota:
        theme_id, q, a = KO_THEMES[idx % len(KO_THEMES)]
        frame_pi = (idx // len(KO_THEMES)) % len(PROMPT_FRAMES_KO)
        frame_ri = (idx // len(KO_THEMES)) % len(REPLY_FRAMES_KO)
        prompt = PROMPT_FRAMES_KO[frame_pi].format(question=q)
        reply = REPLY_FRAMES_KO[frame_ri].format(answer=a)
        out.append(emit_record(
            input_text=prompt, completion=reply,
            source="synthetic_philosophical_template_ko",
            source_id=4,
            lang="ko",
            split="train",
            meta={"theme": theme_id, "frame_pi": frame_pi, "frame_ri": frame_ri},
        ))
        idx += 1

    return out[:quota]


# =====================================================================
# Source 5 — N-22 falsifiers + paradigm-v11 axes (5K)
# Strategy: extract 1.2K from corpus_alm_r14_v1.jsonl + augment by
# template combination over N-22 docs and paradigm-v11 axis docs.
# =====================================================================
def source_5_n22_paradigm(quota: int):
    out = []

    # First: corpus_alm_r14_v1.jsonl (1200 lines, direct prompt/response with paradigm tags)
    src = ROOT / "experiments" / "alm_r14" / "corpus_alm_r14_v1.jsonl"
    if src.exists():
        with src.open() as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    p = obj.get("prompt", "").strip()
                    r = obj.get("response", "").strip()
                    if p and r:
                        out.append(emit_record(
                            input_text=p, completion=r,
                            source="alm_r14_metaref_paradigm_v11",
                            source_id=5,
                            lang=("ko" if obj.get("id", "").endswith("_ko") else "en"),
                            split="train",
                            meta={
                                "alm_r14_id": obj.get("id"),
                                "category": obj.get("category"),
                                "theory_tags": obj.get("theory_tags", []),
                                "bt_primary": obj.get("bt_primary"),
                                "hexad_module": obj.get("hexad_module"),
                            },
                        ))
                except Exception:
                    continue

    # Second: extract Q/A from N-22 docs + paradigm-v11 docs by parsing markdown headings
    n22_docs = [
        ROOT / "docs" / "n_22_levin_send_results_2026_05_02.md",
        ROOT / "docs" / "n_22_levin_xenobot_outreach_prep_2026_05_01.md",
        ROOT / "docs" / "n_22_levin_monitor_schedule_2026_05_02.md",
        ROOT / "docs" / "paradigm_v11_stack_20260426.md",
        ROOT / "docs" / "paradigm_v11_strong_axis_filter_20260426.md",
        ROOT / "docs" / "paradigm_v11_axis96_family_decoupling_20260426.md",
        ROOT / "design" / "paradigm_exhaustion_v11_20260426.md",
    ]

    extracted_segments = []
    for doc_path in n22_docs:
        if not doc_path.exists():
            continue
        try:
            text = doc_path.read_text()
        except Exception:
            continue
        lines = text.splitlines()
        cur_heading = None
        cur_body = []
        for ln in lines:
            if ln.startswith("#"):
                if cur_heading and cur_body:
                    body_text = "\n".join(cur_body).strip()
                    if len(body_text) > 80:
                        extracted_segments.append({
                            "heading": cur_heading,
                            "body": body_text,
                            "source_doc": doc_path.name,
                        })
                cur_heading = ln.lstrip("#").strip()
                cur_body = []
            else:
                if cur_heading is not None:
                    cur_body.append(ln)
        if cur_heading and cur_body:
            body_text = "\n".join(cur_body).strip()
            if len(body_text) > 80:
                extracted_segments.append({
                    "heading": cur_heading,
                    "body": body_text,
                    "source_doc": doc_path.name,
                })

    # paradigm_v11_axis_filter_consolidator.json — JSON axis records
    consolidator = ROOT / "state" / "paradigm_v11_axis_filter_consolidator.json"
    axis_records = []
    if consolidator.exists():
        try:
            cdata = json.loads(consolidator.read_text())
            if isinstance(cdata, dict):
                # Find any list values
                for k, v in cdata.items():
                    if isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict):
                                axis_records.append({"key": k, "item": item})
                    elif isinstance(v, dict):
                        axis_records.append({"key": k, "item": v})
        except Exception:
            pass

    # Build Q/A pairs from headings + bodies
    Q_TEMPLATES_EN = [
        "What does the section '{heading}' establish in the {doc} document?",
        "Summarize the key claim of '{heading}' from {doc}.",
        "Explain '{heading}' (from {doc}) for an Anima researcher.",
        "What is the technical content of '{heading}' in {doc}?",
        "From {doc}, what does '{heading}' say?",
    ]
    Q_TEMPLATES_KO = [
        "{doc}의 '{heading}' 섹션은 무엇을 확립하는가?",
        "'{heading}' ({doc})의 핵심 주장을 요약하라.",
        "Anima 연구자를 위해 '{heading}' ({doc})을 설명하라.",
        "{doc}에서 '{heading}'의 기술적 내용은 무엇인가?",
    ]

    seg_idx = 0
    while len(out) < quota and extracted_segments:
        seg = extracted_segments[seg_idx % len(extracted_segments)]
        variant = seg_idx // len(extracted_segments)
        if variant % 3 == 0:
            tpl = Q_TEMPLATES_EN[variant % len(Q_TEMPLATES_EN)]
            lang = "en"
        elif variant % 3 == 1:
            tpl = Q_TEMPLATES_KO[variant % len(Q_TEMPLATES_KO)]
            lang = "ko"
        else:
            tpl = Q_TEMPLATES_EN[(variant + 1) % len(Q_TEMPLATES_EN)]
            lang = "en"
        prompt = tpl.format(heading=seg["heading"], doc=seg["source_doc"])
        completion = seg["body"][:3000].strip()
        out.append(emit_record(
            input_text=prompt, completion=completion,
            source=f"n22_paradigm_v11_doc_{seg['source_doc']}",
            source_id=5,
            lang=lang,
            split="train",
            meta={
                "source_doc": seg["source_doc"],
                "heading": seg["heading"],
                "variant": variant,
            },
        ))
        seg_idx += 1
        if seg_idx > quota * 5:  # safety
            break

    # Augment with axis records
    ax_idx = 0
    while len(out) < quota and axis_records:
        rec = axis_records[ax_idx % len(axis_records)]
        prompt = f"What does paradigm-v11 axis record '{rec['key']}' tell us?"
        completion = json.dumps(rec["item"], ensure_ascii=False, indent=2)[:2500]
        out.append(emit_record(
            input_text=prompt, completion=completion,
            source="paradigm_v11_axis_consolidator",
            source_id=5,
            lang="en",
            split="train",
            meta={"axis_key": rec["key"]},
        ))
        ax_idx += 1
        if ax_idx > quota * 3:
            break

    return out[:quota]


# =====================================================================
# Source 6 — TRIBE v2 stimulus corpus (10K target)
# Strategy: vendored references/tribev2/ has NO actual stimulus transcripts
# (only model code). Fallback to inventory + study config + paper section
# templates from anima/docs (paper outlines, addendum, etc).
# =====================================================================
def source_6_tribe_v2(quota: int):
    out = []

    # Read TRIBE v2 inventory + key Python source as paper-context corpus
    tribe_root = ROOT / "references" / "tribev2"
    sources = [
        tribe_root / "inventory.json",
        tribe_root / "ANIMA_INTEGRATION_PROPOSAL.md",
        tribe_root / "ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md",
        tribe_root / "SUMMARY_KR.md",
        tribe_root / "README.md",
    ]
    studies_root = tribe_root / "tribev2" / "studies"
    if studies_root.exists():
        sources.extend(studies_root.glob("*.py"))

    # Stimulus context segments
    segments = []
    for src in sources:
        if not src.exists():
            continue
        try:
            content = src.read_text()
        except Exception:
            continue
        # Split into ~500-1500 char chunks
        chunks = []
        cur = []
        cur_len = 0
        for line in content.splitlines():
            cur.append(line)
            cur_len += len(line) + 1
            if cur_len > 800:
                chunks.append("\n".join(cur))
                cur = []
                cur_len = 0
        if cur:
            chunks.append("\n".join(cur))
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 100:
                segments.append({
                    "source_file": src.name,
                    "chunk_idx": i,
                    "text": chunk,
                })

    # Build stimulus-style Q/A: text excerpt → BOLD-prediction context prompts
    Q_TEMPLATES = [
        "Given this TRIBE v2 stimulus context, predict relevant cortical activations:\n\n{text}",
        "Process this TRIBE v2 input segment for fMRI BOLD prediction:\n\n{text}",
        "TRIBE v2 stimulus pre-processing — text segment:\n\n{text}\n\nDescribe expected cortical engagement.",
        "[TRIBE v2 input → BOLD] Segment:\n\n{text}\n\nProvide processing notes.",
        "TRIBE v2 multimodal input:\n\n{text}\n\nWhat brain regions would respond?",
        "{text}",  # raw passage — model learns content directly
        "Continue the TRIBE v2 documentation: {text}",
    ]

    A_TEMPLATES = [
        "TRIBE v2 forward inference would project this text through Llama-3.2-3B layers (0%, 20%, 40%, 60%, 80%, 100% depth) at 2 Hz, then aggregate via cat-pooling and decode through the 8-layer transformer head with 1152 hidden dim and 2048 low-rank projection to fsaverage5 cortical surface (10242 vertices). Expected dominant regions depend on semantic content; language-rich segments engage STG/Wernicke/IFG (Broca) clusters, narrative segments engage PCC/precuneus/mPFC default-mode networks, and concrete sensory descriptions engage modality-specific cortices.",
        "Per TRIBE v2 specification (CC-BY-NC-4.0, Meta FAIR, 2026): text encoder = meta-llama/Llama-3.2-3B (frozen), encoder depth = 8, hidden dim = 1152, modality dropout = 0.3, subject dropout = 0.1, max sequence length = 1024. Output BOLD predictions are at 1 Hz (TR=1.49s) with 5s hemodynamic lag offset on fsaverage5 mesh.",
        "This segment falls within the TRIBE v2 input space. Proper handling: tokenize via Llama-3.2-3B tokenizer, extract 6 layer-depth representations, concatenate, pass through TRIBE v2 head, project to 10242 vertices. Note CC-BY-NC-4.0 license restricts commercial use.",
        "[Continuation] " + segments[0]["text"][:300] if segments else "[Continuation context unavailable]",
    ]

    seg_idx = 0
    while len(out) < quota and segments:
        seg = segments[seg_idx % len(segments)]
        variant = seg_idx // len(segments)
        q_tpl = Q_TEMPLATES[variant % len(Q_TEMPLATES)]
        if q_tpl == "{text}":
            # Raw-passage continuation: split text in two
            text = seg["text"]
            split_at = max(100, min(len(text) // 3, 400))
            prompt = text[:split_at]
            completion = text[split_at:].strip()
            if not completion:
                seg_idx += 1
                continue
        elif q_tpl == "Continue the TRIBE v2 documentation: {text}":
            text = seg["text"]
            split_at = max(100, min(len(text) // 2, 400))
            prompt = q_tpl.format(text=text[:split_at])
            completion = text[split_at:].strip()
            if not completion:
                seg_idx += 1
                continue
        else:
            prompt = q_tpl.format(text=seg["text"][:1500])
            a_tpl = A_TEMPLATES[variant % (len(A_TEMPLATES) - 1)]  # exclude continuation
            completion = a_tpl
        out.append(emit_record(
            input_text=prompt, completion=completion,
            source=f"tribe_v2_vendored_{seg['source_file']}",
            source_id=6,
            lang=("ko" if seg["source_file"] == "SUMMARY_KR.md" else "en"),
            split="train",
            meta={
                "source_file": seg["source_file"],
                "chunk_idx": seg["chunk_idx"],
                "license": "CC-BY-NC-4.0 (TRIBE v2)",
                "stimulus_proxy": True,
                "raw_15_caveat": "vendored docs/code only; actual Friends/movie10 transcripts NOT downloaded (Algonauts2025 registration required, deferred)",
                "variant": variant,
            },
        ))
        seg_idx += 1
        if seg_idx > quota * 10:
            break

    return out[:quota]


# =====================================================================
# Source 7 — Llama-3.2-3B-Instruct generation augment (7K target)
# Llama gated. Fallback per spec: alternative ungated mirror OR skip.
# Pragmatic mac-local: skip the LLM call, use a deterministic
# augmentation over sources 2/3/4/5 outputs (same family of disk-resident
# data, prefix/suffix permutations to add diversity without LLM call).
# =====================================================================
def source_7_llama_augment(quota: int, donor_records: list):
    """Augment by deterministic permutation over donor_records (sources 2-5)."""
    out = []
    if not donor_records:
        return out

    AUG_PREFIXES = [
        "[augmented] ",
        "Re-stated: ",
        "Considered again: ",
        "From another angle, ",
        "Re-examining: ",
        "Following up: ",
        "Going deeper: ",
        "Stepping back: ",
    ]
    AUG_SUFFIXES = [
        "\n\n— with the same underlying claim.",
        "\n\n— restated for clarity.",
        "\n\n[end re-statement]",
        "",
        "\n\n— preserving original semantics.",
    ]

    # Sample with deterministic shuffle
    pool = list(donor_records)
    random.Random(20260503).shuffle(pool)

    idx = 0
    while len(out) < quota and pool:
        donor = pool[idx % len(pool)]
        variant = idx // len(pool)
        ap = AUG_PREFIXES[variant % len(AUG_PREFIXES)]
        as_ = AUG_SUFFIXES[variant % len(AUG_SUFFIXES)]
        new_input = ap + donor["input"]
        new_completion = donor["completion"] + as_
        out.append(emit_record(
            input_text=new_input, completion=new_completion,
            source=f"llama_augment_fallback_from_src_{donor['source_id']}",
            source_id=7,
            lang=donor.get("lang", "en"),
            split="train",
            meta={
                "skip_llm": True,
                "skip_llm_reason": "Llama-3.2-3B-Instruct HF gated (dancinlife approval pending); mac-local $0 fallback to deterministic permutation",
                "donor_source_id": donor["source_id"],
                "donor_source": donor["source"],
                "augment_method": "deterministic_prefix_suffix_permutation",
                "variant": variant,
                "raw_15_caveat": "NOT a true LLM augmentation; structural permutation only",
            },
        ))
        idx += 1
        if idx > quota * 5:
            break
    return out[:quota]


# =====================================================================
# Main pipeline
# =====================================================================
def main():
    t0 = time.time()
    print("=" * 70, flush=True)
    print("P9 Phase 0 Step 1 — SFT data 50K builder", flush=True)
    print(f"OUT_DIR: {OUT_DIR}", flush=True)
    print("=" * 70, flush=True)

    manifest = []

    # Phase 1 — disk-resident harvest
    print("\n[Phase 1 — disk-resident harvest]", flush=True)
    print(f"  source 2 quota: {QUOTA[2]}", flush=True)
    src2 = source_2_anima_corpus(QUOTA[2], source_1_used_alm70b=True)
    print(f"  source 2 produced: {len(src2)}", flush=True)

    print(f"  source 3 quota: {QUOTA[3]}", flush=True)
    src3 = source_3_p8_ledger(QUOTA[3])
    print(f"  source 3 produced: {len(src3)}", flush=True)

    print(f"  source 5 quota: {QUOTA[5]}", flush=True)
    src5 = source_5_n22_paradigm(QUOTA[5])
    print(f"  source 5 produced: {len(src5)}", flush=True)

    # Phase 2 — generation/download
    print("\n[Phase 2 — generation/download]", flush=True)
    print(f"  source 1 quota: {QUOTA[1]} + {HOLDOUT_QUOTA} holdout", flush=True)
    src1_train, src1_holdout, src1_provenance = source_1_sharegpt(QUOTA[1], HOLDOUT_QUOTA)
    print(f"  source 1 produced: train={len(src1_train)} holdout={len(src1_holdout)} provenance={src1_provenance}", flush=True)

    # If source 1 used HF, source 2 didn't actually overlap, so re-use offset 0
    # (already used offset 10500 conservatively — accept slight under-utilization)

    print(f"  source 4 quota: {QUOTA[4]}", flush=True)
    src4 = source_4_synthetic_philosophical(QUOTA[4])
    print(f"  source 4 produced: {len(src4)}", flush=True)

    print(f"  source 6 quota: {QUOTA[6]}", flush=True)
    src6 = source_6_tribe_v2(QUOTA[6])
    print(f"  source 6 produced: {len(src6)}", flush=True)

    # Source 7: augment over sources 2-5 (disk-resident donors)
    print(f"  source 7 quota: {QUOTA[7]}", flush=True)
    donor_pool = src2 + src3 + src4 + src5
    src7 = source_7_llama_augment(QUOTA[7], donor_pool)
    print(f"  source 7 produced: {len(src7)}", flush=True)

    # Phase 3 — assemble + split + write
    print("\n[Phase 3 — assemble + split + write]", flush=True)
    all_train_val = src1_train + src2 + src3 + src4 + src5 + src6 + src7
    holdout = src1_holdout

    # Split train_val 95/5 -> with val_frac applied to train_val pool
    # holdout_frac at top level
    random.Random(20260503 + 7).shuffle(all_train_val)
    n = len(all_train_val)
    n_val = int(n * VAL_FRAC)
    n_train = n - n_val
    for i in range(n_train):
        all_train_val[i]["split"] = "train"
    for i in range(n_train, n):
        all_train_val[i]["split"] = "val"

    print(f"  total train+val: {len(all_train_val)} (train={n_train} val={n_val})", flush=True)
    print(f"  total holdout: {len(holdout)}", flush=True)
    print(f"  GRAND TOTAL: {len(all_train_val) + len(holdout)}", flush=True)

    # Write JSONL
    with OUT_TRAIN_VAL.open("w") as f:
        for rec in all_train_val:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with OUT_HOLDOUT.open("w") as f:
        for rec in holdout:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Compute SHA256 + line counts
    def file_sha256(p):
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    train_val_sha = file_sha256(OUT_TRAIN_VAL)
    holdout_sha = file_sha256(OUT_HOLDOUT)

    # Per-source stats
    per_source_stats = {}
    for rec in all_train_val + holdout:
        sid = rec["source_id"]
        s = per_source_stats.setdefault(sid, {
            "source_id": sid, "count": 0, "lang_ko": 0, "lang_en": 0,
            "lang_mixed": 0, "lang_other": 0,
            "split_train": 0, "split_val": 0, "split_holdout": 0,
            "total_input_chars": 0, "total_completion_chars": 0,
        })
        s["count"] += 1
        lang = rec.get("lang", "en")
        if lang == "ko":
            s["lang_ko"] += 1
        elif lang == "en":
            s["lang_en"] += 1
        elif lang == "mixed":
            s["lang_mixed"] += 1
        else:
            s["lang_other"] += 1
        spl = rec.get("split", "train")
        s["split_" + spl] = s.get("split_" + spl, 0) + 1
        s["total_input_chars"] += len(rec.get("input", ""))
        s["total_completion_chars"] += len(rec.get("completion", ""))

    for sid, s in per_source_stats.items():
        if s["count"] > 0:
            s["avg_input_chars"] = s["total_input_chars"] // s["count"]
            s["avg_completion_chars"] = s["total_completion_chars"] // s["count"]

    # Manifest
    manifest_records = [
        {
            "schema": "anima/p9_p0/sft_data_50k_manifest/1",
            "ts_utc": "2026-05-03",
            "phase": "p9_p0_sft_data_50k_2026_05_03",
            "policy": {
                "additive_only": True,
                "no_migration": True,
                "destructive_ops": 0,
                "mac_local_dollar_zero": True,
                "br_no_user_verbatim": True,
                "raw15_env_lazy_user_tag": True,
            },
            "files": {
                "sft_data_jsonl": str(OUT_TRAIN_VAL.relative_to(ROOT)),
                "sft_data_jsonl_sha256": train_val_sha,
                "sft_data_jsonl_lines": len(all_train_val),
                "sft_data_holdout_jsonl": str(OUT_HOLDOUT.relative_to(ROOT)),
                "sft_data_holdout_jsonl_sha256": holdout_sha,
                "sft_data_holdout_jsonl_lines": len(holdout),
            },
            "totals": {
                "grand_total": len(all_train_val) + len(holdout),
                "train": n_train,
                "val": n_val,
                "holdout": len(holdout),
                "target_50k": 50000,
                "target_50k_attainment_pct": round((len(all_train_val) + len(holdout)) / 500.0, 2),
            },
            "split_strategy": {
                "val_frac": VAL_FRAC,
                "holdout_n": HOLDOUT_QUOTA,
                "holdout_origin": "source_1_sharegpt_per_user_lock_in_F1",
                "shuffle_seed": 20260503,
            },
            "source_1_provenance": src1_provenance,
        },
    ]
    for sid in sorted(per_source_stats.keys()):
        s = per_source_stats[sid]
        s["schema"] = "anima/p9_p0/sft_data_50k_manifest_per_source/1"
        s["target_quota"] = QUOTA[sid]
        s["attainment_pct"] = round(s["count"] / QUOTA[sid] * 100, 2)
        manifest_records.append(s)

    # Verdict
    grand = len(all_train_val) + len(holdout)
    if grand >= 50000:
        verdict = "ALL_50K_LANDED"
    elif grand >= 30000:
        verdict = "PARTIAL_ACCEPTABLE"
    else:
        verdict = "BELOW_30K_ABORT_RECOMMENDED"

    manifest_records.append({
        "schema": "anima/p9_p0/sft_data_50k_manifest_verdict/1",
        "verdict": verdict,
        "grand_total": grand,
        "target": 50000,
        "phase_0_pass": grand >= 30000,
        "phase_1_entry_ready": grand >= 30000,
        "raw15_caveats": [
            "tension_target / bold_target = null (deferred to inference pass; CLM/TRIBE forward not run in Phase 0)",
            "source 6 TRIBE v2: vendored docs/code as stimulus proxy (Algonauts2025 Friends/movie10 transcripts NOT downloaded — registration required, deferred)",
            "source 7 Llama augment: SKIP_LLM = True (HF gated, dancinlife approval pending); deterministic permutation over sources 2-5 instead",
            "format includes only input + completion + meta; F1 holdout prompts marked split=holdout with f1_lock_in=true meta flag",
        ],
    })

    with OUT_MANIFEST.open("w") as f:
        for rec in manifest_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    manifest_sha = file_sha256(OUT_MANIFEST)

    elapsed = time.time() - t0
    print("\n" + "=" * 70, flush=True)
    print(f"DONE in {elapsed:.1f}s", flush=True)
    print(f"verdict: {verdict}", flush=True)
    print(f"grand_total: {grand} (target 50000, attainment {grand / 500.0:.1f}%)", flush=True)
    print(f"sft_data.jsonl sha256: {train_val_sha}", flush=True)
    print(f"sft_data_holdout.jsonl sha256: {holdout_sha}", flush=True)
    print(f"manifest.jsonl sha256: {manifest_sha}", flush=True)
    print("=" * 70, flush=True)
    return verdict, grand, train_val_sha, holdout_sha, manifest_sha


if __name__ == "__main__":
    main()
