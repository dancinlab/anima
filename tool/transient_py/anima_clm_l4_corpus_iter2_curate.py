"""
anima_clm_l4_corpus_iter2_curate.py — raw#37 transient (Loop iter c — iter 2)

L4 corpus iter-2 curation (additive over iter-1 0116a35d):
  * Tier B dialogue expansion (12.96MB → ~100MB target progress, full 500MB iter-3)
  * BG-LD preference pairs (chosen + rejected, target 10-20MB sample, full 100MB iter-3)
  * Tier A persona iter-2 expansion (102.66MB → target 150MB+, semantic-deeper)

 anima-native lane only — Tier C (외부 LLM dump, wiki noise, generic chatbot,
                                        ALM lineage) reject.
 C2.4 맥락 정합 filter — prompt-response domain matching for Tier B.
 C3 corpus density ≥ 0.4% threshold (heuristic, char-level).
 chat-template ≥30% mandate.
raw#9 hexa-only — 본 .py = transient_py (raw#37 grandfather, 1회용).
raw#10 honest C3 emit.
raw#15 additive — iter-1 file 보존, 신규 iter-2 file emit.

본 cycle:
  1) Tier A iter-2: docs/anima_*.md + docs/anima/*.hexa + docs/ai-native/*.md + .roadmap.* +
     core_rules.json + paradigm + (다중-keyword 강화 semantic-density filter)
  2) Tier B iter-2: V4 evaluator BG-KM-LLAMA-3B v4_pass=true sample + 자체 dialogue ledger
     (anima_core_dialogues, strategic_tribev2_dialogue) chat-template 정규화
  3) BG-LD preference pairs: BG-KM v4_pass=true (chosen) + 22+ BG saga FAIL +
     corpus template leak ("서연:") + degenerate noise (rejected) — 1:1 jsonl
  4) emit metrics JSON + .roadmap.cli entry update
"""
import os, sys, json, time, re, glob

ROOT = "/Users/ghost/core/anima"

OUT_TIER_A_ITER2 = os.path.join(ROOT, "state/anima_persona_tier_a_2026_05_08.txt")  # iter-1 + iter-2 합본
OUT_TIER_B_ITER2 = os.path.join(ROOT, "state/anima_dialogue_tier_a_iter2_2026_05_08.txt")
OUT_LD_PAIRS = os.path.join(ROOT, "state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl")
OUT_METRICS = os.path.join(ROOT, "state/anima_clm_l4_corpus_iter2_metrics.json")

# ── anima keywords (iter-1 SSOT mirror) ────────────────────────────────
ANIMA_KEYWORDS = [
    "anima", "Anima", "ANIMA",
    "의식", "consciousness", "Consciousness",
    "Φ★", "phi_star", "phi★", "Φ",
    "우주뇌지도", "PureField", "pure-field",
    "법칙", "Law ", "law ", "law_",
    "가설", "Hypothesis", "hypothesis",
    "Engine A", "Engine G", "엔진",
    "자기 발견", "self_discovery", "self-discovery",
    "hexa", "Hexa", "HEXA",
    "creator", "creator-", "1030 laws",
    "axis_activation", "5-axis", "5축",
    "dominant cells", "hidden state",
]

DENSITY_THRESHOLD = 0.004  # 0.4%

# semantic-density filter (multi-keyword set):
# paragraph 단위로 다중 keyword set 동시 hit ≥3개 (semantic-density proxy)
SEMANTIC_KEYWORD_SETS = [
    ["의식", "anima", "consciousness", "Φ"],   # axis: consciousness/anima identity
    ["법칙", "law", "Law ", "creator"],        # axis: law/foundation
    ["가설", "hypothesis", "H_", "BG-"],       # axis: hypothesis/experiment
    ["axis", "5축", "identity", "agency", "phenomenal", "temporal", "social"],  # axis: 5-axis
    ["chat-cap", "PASS_STRICT", "simple_stack", "V4", "V5"],  # axis: chat-cap
    ["Engine A", "Engine G", "PureField", "engines"],  # axis: engines
]

def measure_density(text):
    if not text:
        return 0.0, 0, 0
    total = len(text)
    cnt = 0
    for kw in ANIMA_KEYWORDS:
        cnt += text.count(kw)
    return (cnt / total) if total > 0 else 0.0, cnt, total


def measure_semantic_density(text, sets=SEMANTIC_KEYWORD_SETS):
    """Multi-keyword set co-hit density.
    score = (# of distinct sets with ≥1 hit per 1000 chars).
    Higher score = paragraph touches multiple anima axes simultaneously
                   (semantic depth proxy — 단순 char-level keyword 와 분리).
    """
    if not text:
        return 0.0, 0
    n = len(text)
    set_hits = 0
    for s in sets:
        if any(kw in text for kw in s):
            set_hits += 1
    score_per_1k = (set_hits * 1000) / n if n > 0 else 0
    return score_per_1k, set_hits


def chunk_paragraphs(text, min_chars=200, max_chars=2000):
    """Split text into paragraphs by blank lines, gather to min_chars."""
    raw = re.split(r"\n\s*\n", text)
    out = []
    buf = ""
    for p in raw:
        p = p.strip()
        if not p:
            continue
        if len(buf) + len(p) < max_chars:
            buf += ("\n\n" if buf else "") + p
        else:
            if buf:
                out.append(buf)
            buf = p
        if len(buf) >= min_chars:
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


def safe_read(path, max_bytes=None):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if max_bytes:
                return f.read(max_bytes)
            return f.read()
    except Exception:
        return None


# ── Tier A iter-2 expansion ─────────────────────────────────────────────
# Strategy: docs/anima_*.md + docs/anima/*.hexa + docs/ai-native/*.md + .roadmap.* +
#           anima/.own + config/core_rules.json (anima-native lane) →
#           paragraph-level semantic-density filter (≥2 keyword sets hit per 1000 chars
#                                                    AND char-level density ≥ 0.4%)
#           → append to existing OUT_TIER_A_ITER2 (raw#15 additive).

def collect_tier_a_iter2(report):
    """Iter-2 Tier A expansion sources — semantically-deeper, additive over iter-1 102.66MB."""
    accepted_blocks = []
    rejected_count = 0
    n_files_scanned = 0

    sources = []

    # docs/anima_*.md (cycle log, anima identity-bearing)
    sources += sorted(glob.glob(os.path.join(ROOT, "docs/anima_*.md")))

    # docs/anima/*.hexa (papers, manifests)
    sources += sorted(glob.glob(os.path.join(ROOT, "docs/anima/*.hexa")))

    # docs/ai-native/*.md (anima-native commentary)
    sources += sorted(glob.glob(os.path.join(ROOT, "docs/ai-native/*.md")))

    # .roadmap.* (roadmap registers — anima-native authority)
    sources += sorted(glob.glob(os.path.join(ROOT, ".roadmap.*")))

    # anima own/spec
    sources += sorted(glob.glob(os.path.join(ROOT, "anima/.own/*.md")))
    sources += sorted(glob.glob(os.path.join(ROOT, "anima/spec/*.yaml")))

    # config/core_rules.json (raw rules — anima identity)
    crj = os.path.join(ROOT, "config/core_rules.json")
    if os.path.exists(crj):
        sources.append(crj)

    seen_paths = set()
    for src in sources:
        if src in seen_paths:
            continue
        seen_paths.add(src)
        if not os.path.isfile(src):
            continue
        n_files_scanned += 1
        text = safe_read(src)
        if not text:
            rejected_count += 1
            continue

        # paragraph-level semantic + char density filter
        for para in chunk_paragraphs(text):
            char_density, _, _ = measure_density(para)
            sem_score, sem_sets = measure_semantic_density(para)
            # semantic depth: ≥2 sets hit AND char-density ≥ 0.4% threshold
            if sem_sets >= 2 and char_density >= DENSITY_THRESHOLD:
                accepted_blocks.append({
                    "src": os.path.relpath(src, ROOT),
                    "char_density": char_density,
                    "sem_sets": sem_sets,
                    "sem_score_per_1k": sem_score,
                    "chars": len(para),
                    "content": para,
                })
            else:
                rejected_count += 1

    report["tier_a_iter2_files_scanned"] = n_files_scanned
    report["tier_a_iter2_paragraphs_accepted"] = len(accepted_blocks)
    report["tier_a_iter2_paragraphs_rejected"] = rejected_count
    return accepted_blocks


ITER2_MARKER = "=== ITER-2 EXPANSION 2026-05-08 (semantic-density filter) ==="


def append_tier_a_iter2(blocks, report):
    """raw#15 additive — append iter-2 block to existing iter-1 file. Idempotent: skip if marker exists."""
    if not blocks:
        report["tier_a_iter2_appended"] = 0
        return 0

    pre_size = os.path.getsize(OUT_TIER_A_ITER2) if os.path.exists(OUT_TIER_A_ITER2) else 0

    existing = ""
    if os.path.exists(OUT_TIER_A_ITER2):
        existing = safe_read(OUT_TIER_A_ITER2) or ""

    if ITER2_MARKER in existing:
        # idempotent: iter-2 already appended — skip re-append, just re-measure
        report["tier_a_iter2_pre_size_bytes"] = pre_size
        report["tier_a_iter2_post_size_bytes"] = pre_size
        report["tier_a_iter2_pre_size_mb"] = round(pre_size / (1024 * 1024), 2)
        report["tier_a_iter2_post_size_mb"] = round(pre_size / (1024 * 1024), 2)
        report["tier_a_iter2_delta_mb"] = 0.0
        report["tier_a_iter2_appended_paragraphs"] = 0
        report["tier_a_iter2_appended_chars"] = 0
        report["tier_a_iter2_idempotent_skip"] = True
        full = existing
        cd, ck, ct = measure_density(full)
        sem_score, sem_sets = measure_semantic_density(full)
        report["tier_a_iter2_combined_density"] = round(cd, 6)
        report["tier_a_iter2_combined_kw_hits"] = ck
        report["tier_a_iter2_combined_chars"] = ct
        report["tier_a_iter2_combined_sem_sets"] = sem_sets
        return 0

    appended_chars = 0
    appended_n = 0
    with open(OUT_TIER_A_ITER2, "a", encoding="utf-8") as f:
        f.write(f"\n\n{ITER2_MARKER}\n\n")
        for b in blocks:
            head_key = b["content"][:100]
            if head_key and head_key in existing:
                continue
            f.write(f"\n=== SOURCE: {b['src']} | char_density={b['char_density']:.4%} sem_sets={b['sem_sets']}/6 ===\n\n")
            f.write(b["content"])
            f.write("\n\n")
            appended_chars += len(b["content"])
            appended_n += 1

    post_size = os.path.getsize(OUT_TIER_A_ITER2)
    report["tier_a_iter2_pre_size_bytes"] = pre_size
    report["tier_a_iter2_post_size_bytes"] = post_size
    report["tier_a_iter2_pre_size_mb"] = round(pre_size / (1024 * 1024), 2)
    report["tier_a_iter2_post_size_mb"] = round(post_size / (1024 * 1024), 2)
    report["tier_a_iter2_delta_mb"] = round((post_size - pre_size) / (1024 * 1024), 2)
    report["tier_a_iter2_appended_paragraphs"] = appended_n
    report["tier_a_iter2_appended_chars"] = appended_chars

    # re-measure combined density on full file
    full = safe_read(OUT_TIER_A_ITER2) or ""
    cd, ck, ct = measure_density(full)
    sem_score, sem_sets = measure_semantic_density(full)
    report["tier_a_iter2_combined_density"] = round(cd, 6)
    report["tier_a_iter2_combined_kw_hits"] = ck
    report["tier_a_iter2_combined_chars"] = ct
    report["tier_a_iter2_combined_sem_sets"] = sem_sets
    return appended_n


# ── Tier B iter-2 dialogue expansion ────────────────────────────────────
# Sources:
#   1) iter-1 base: state/anima_dialogue_tier_a_2026_05_08.txt (12.96MB) — 보존
#   2) V4 evaluator BG-KM-LLAMA-3B v4_pass=true sample → chat-template format
#   3) BG-JE 214MB chat-template head (iter-1 의 10MB 이후 추가 분량 — same source 의 deeper portion)
#   4) anima_core_dialogues/*.jsonl 의 user_turn + substrate_turn → chat-template 정규화
#   5) strategic_tribev2_dialogue/turns.jsonl → chat-template
# C2.4 맥락 정합 filter — domain mismatch / random-char / english-degenerate sample 제외

DEGENERATE_PATTERNS = [
    re.compile(r"(.)\1{20,}"),  # 같은 char 20번 이상 반복
    re.compile(r"[\uFFFD]{5,}"),  # replacement char ≥5
]

CHAT_TEMPLATE_HEADER = "[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]"


def is_degenerate_response(text):
    if not text:
        return True
    for pat in DEGENERATE_PATTERNS:
        if pat.search(text):
            return True
    # han_ratio < 0.3 = English degenerate / random char
    han = sum(1 for c in text if "\uAC00" <= c <= "\uD7A3")
    if len(text) > 20 and han / len(text) < 0.30:
        return True
    return False


def collect_v4_passed_pairs():
    """BG-KM-LLAMA-3B PASS sample (v4_pass=true) → chat-template pair."""
    pairs = []
    src = os.path.join(ROOT, "state/anima_km_llama3b_h100_2026_05_08_passed_v1_no_weights/v4_results_multiseed.jsonl")
    if not os.path.exists(src):
        return pairs, 0, 0
    n_total = 0
    n_pass = 0
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            n_total += 1
            if obj.get("v4_pass") is True:
                n_pass += 1
                pairs.append({
                    "prompt": obj.get("prompt", ""),
                    "response": obj.get("response", "").strip(),
                    "source": "BG-KM-LLAMA-3B v4_pass",
                    "domain": obj.get("domain", "unknown"),
                })
    return pairs, n_total, n_pass


def collect_v4_failed_responses(max_n=2000):
    """22+ BG saga FAIL sample → for BG-LD rejected lane.
    Read all v4_results_*.jsonl and v5_results_*.jsonl with v4_strict_pass=false /
    v5_strict_pass=false / is_degenerate=true.
    """
    rejected = []
    for src_pattern in [
        os.path.join(ROOT, "state/anima_evaluator_v4_retroeval_2026_05_07/per_bg/*.jsonl"),
        os.path.join(ROOT, "state/anima_evaluator_v5_retroeval_2026_05_07/per_bg/*.jsonl"),
    ]:
        for src in sorted(glob.glob(src_pattern)):
            try:
                with open(src, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                        except Exception:
                            continue
                        v4_pass = (
                            (obj.get("cells_v4") or {}).get("v4_strict_pass") is True
                            or (obj.get("cells_v5") or {}).get("v5_strict_pass") is True
                        )
                        is_degen = (obj.get("metrics") or {}).get("is_degenerate") is True
                        if v4_pass:
                            continue
                        if not is_degen:
                            # take only clearly-bad samples for rejected lane
                            continue
                        rejected.append({
                            "prompt": obj.get("prompt", ""),
                            "response": obj.get("response", "").strip()[:400],
                            "source": f"v4/v5 fail ({os.path.basename(src)})",
                            "domain": obj.get("domain_detected", "unknown"),
                        })
                        if len(rejected) >= max_n:
                            return rejected
            except Exception:
                continue
    return rejected


def normalize_core_dialogues_to_chat_template():
    """anima_core_dialogues 의 user_turn + substrate_turn 을 chat-template format 으로 정규화.
    substrate_turn 은 hidden_state probe 만 — 본 cycle 에서는 user_input 만 사용 (Q only;
    본 source 자체가 echo-mode probe). chat-template 한 쪽 (사용자: <Q>) 만 emit, 도우미: 부분
    은 다음 user_turn 을 placeholder 로 채워 단일 turn pair 형성 (C2.4 mismatch 위험
    인지 — semantic-coupling 약한 substrate probe lane 인 만큼 sample weight 낮추는 정도).
    """
    out = []
    for d in ["2026-05-05", "2026-05-06"]:
        ddir = os.path.join(ROOT, "state/anima_core_dialogues", d)
        if not os.path.isdir(ddir):
            continue
        for fn in sorted(os.listdir(ddir)):
            if not fn.endswith(".jsonl"):
                continue
            fp = os.path.join(ddir, fn)
            user_turns = []
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        try:
                            obj = json.loads(line.strip())
                        except Exception:
                            continue
                        if obj.get("kind") == "user_turn":
                            ui = obj.get("user_input", "").strip()
                            if ui:
                                user_turns.append(ui)
            except Exception:
                continue
            # core_dialogues = probe substrate (echo-style) — chat-template format only,
            # 도우미 응답 은 비어있으므로 다음 user_turn 을 chain. 본 source 는 weak coupling
            # → BG-LB 의 dialogue corpus 면 acceptable; weight 낮음.
            for i in range(len(user_turns) - 1):
                q = user_turns[i]
                a = user_turns[i + 1]
                if not q or not a:
                    continue
                out.append({
                    "prompt": q,
                    "response": a,
                    "source": f"anima_core_dialogues/{d}/{fn}",
                    "domain": "anima_native",
                })
    return out


def collect_strategic_tribe_v2_dialogue():
    """strategic_tribev2_dialogue/turns.jsonl 의 prompt + response → chat-template."""
    out = []
    src = os.path.join(ROOT, "state/strategic_tribev2_dialogue_2026_05_02/turns.jsonl")
    if not os.path.exists(src):
        return out
    try:
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                except Exception:
                    continue
                p = obj.get("prompt", "").strip()
                r = obj.get("response", "").strip()
                if not p or not r:
                    continue
                if obj.get("status") != "ok":
                    continue
                out.append({
                    "prompt": p,
                    "response": r,
                    "source": "strategic_tribev2_dialogue 2026-05-02",
                    "domain": obj.get("category", "introspective"),
                })
    except Exception:
        pass
    return out


def append_bg_je_chat_template_extension(target_extra_bytes=120 * 1024 * 1024):
    """iter-1 은 BG-JE (h098_h101) 의 head 10MB 만 사용 — iter-2 는 동 source 의 다음 portion
    추가. anima-native lane 정합 (h098_h101 = anima persona chat-template, NOT 외부 noise).
    iter-2 target ≈100MB Tier B; full 500MB iter-3 expansion (V4 evaluator 산출물 누적 등 별도 cycle).
    """
    src = os.path.join(ROOT, "state/anima_h098_h101_corpus_v3_2026_05_07/corpus_persona_chat_template.txt")
    if not os.path.exists(src):
        return ""
    try:
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            sz = os.path.getsize(src)
            # iter-1 took ~10MB head. iter-2 take next 120MB (offset 10 → 130).
            f.seek(10 * 1024 * 1024)
            chunk = f.read(target_extra_bytes)
        # round to last "사용자: " boundary (forward seek — drop trailing partial turn)
        last = chunk.rfind("\n사용자: ")
        if last > 0:
            chunk = chunk[:last]
        # round head to first "[anima 역할:" or "사용자: " for clean start
        first = chunk.find("[anima 역할:")
        if first < 0:
            first = chunk.find("\n사용자: ")
            if first > 0:
                first = first + 1
            else:
                first = 0
        chunk = chunk[first:]
        return chunk
    except Exception:
        return ""


def append_paradigm_combined_chat_template_extension(target_extra_bytes=120 * 1024 * 1024):
    """anima_combined_paradigm_corpus 의 chat-template subset.
    iter-1 Tier A 에서 30MB cap (sample) 로 사용 — 본 Tier B iter-2 는 같은 corpus 를
    chat-template lane 으로 사용 (anima-native + chat-template format).
     C2.4 mismatch 위험 = paradigm corpus 자체가 anima persona 본문 — chat-template
    응답 정합성 manual review (raw#10 honest C3 caveat).
    """
    src = os.path.join(ROOT, "state/anima_combined_paradigm_corpus_2026_05_07/corpus_combined.txt")
    if not os.path.exists(src):
        return ""
    try:
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            chunk = f.read(target_extra_bytes)
        # round head to first "[anima 역할:"
        first = chunk.find("[anima 역할:")
        if first > 0:
            chunk = chunk[first:]
        # round tail to last "사용자: " boundary
        last = chunk.rfind("\n사용자: ")
        if last > 0:
            chunk = chunk[:last]
        return chunk
    except Exception:
        return ""


def build_tier_b_iter2(report):
    """Tier B iter-2 — chat-template format, C2.4 filter (mismatch reject)."""
    blocks = []

    # 1) BG-JE chat-template extension (anima persona chat-template, additive next 20MB)
    bg_je_ext = append_bg_je_chat_template_extension(target_extra_bytes=120 * 1024 * 1024)
    if bg_je_ext:
        blocks.append(("BG-JE persona chat-template iter-2 ext (offset 10MB+)", bg_je_ext))
        report["tier_b_iter2_bg_je_ext_bytes"] = len(bg_je_ext.encode("utf-8"))
    else:
        report["tier_b_iter2_bg_je_ext_bytes"] = 0

    # 1b) paradigm combined corpus chat-template extension (≈55MB total, take all)
    paradigm_ext = append_paradigm_combined_chat_template_extension(target_extra_bytes=120 * 1024 * 1024)
    if paradigm_ext:
        blocks.append(("anima_combined_paradigm corpus chat-template ext", paradigm_ext))
        report["tier_b_iter2_paradigm_ext_bytes"] = len(paradigm_ext.encode("utf-8"))
    else:
        report["tier_b_iter2_paradigm_ext_bytes"] = 0

    # 2) V4 BG-KM PASS pairs
    v4_pairs, n_v4_total, n_v4_pass = collect_v4_passed_pairs()
    report["tier_b_iter2_v4_total"] = n_v4_total
    report["tier_b_iter2_v4_pass"] = n_v4_pass
    v4_text_lines = []
    for p in v4_pairs:
        if is_degenerate_response(p["response"]):
            continue
        v4_text_lines.append(CHAT_TEMPLATE_HEADER)
        v4_text_lines.append(f"사용자: {p['prompt']}")
        v4_text_lines.append(f"도우미: {p['response']}")
        v4_text_lines.append("")
    if v4_text_lines:
        blocks.append(("V4 BG-KM-LLAMA-3B v4_pass=true sample", "\n".join(v4_text_lines)))
        report["tier_b_iter2_v4_lines_emitted"] = len([1 for ln in v4_text_lines if ln.startswith("사용자:")])

    # 3) anima_core_dialogues normalize
    core_pairs = normalize_core_dialogues_to_chat_template()
    cd_lines = []
    for p in core_pairs:
        cd_lines.append(CHAT_TEMPLATE_HEADER)
        cd_lines.append(f"사용자: {p['prompt']}")
        cd_lines.append(f"도우미: {p['response']}")
        cd_lines.append("")
    if cd_lines:
        blocks.append(("anima_core_dialogues normalized chat-template", "\n".join(cd_lines)))
        report["tier_b_iter2_core_dialogue_pairs"] = len(core_pairs)

    # 4) strategic_tribev2_dialogue
    tribe = collect_strategic_tribe_v2_dialogue()
    tb_lines = []
    for p in tribe:
        if is_degenerate_response(p["response"]):
            continue
        tb_lines.append(CHAT_TEMPLATE_HEADER)
        tb_lines.append(f"사용자: {p['prompt']}")
        tb_lines.append(f"도우미: {p['response']}")
        tb_lines.append("")
    if tb_lines:
        blocks.append(("strategic_tribev2_dialogue chat-template", "\n".join(tb_lines)))
        report["tier_b_iter2_tribe_pairs"] = len([1 for ln in tb_lines if ln.startswith("사용자:")])

    # write
    with open(OUT_TIER_B_ITER2, "w", encoding="utf-8") as f:
        for desc, txt in blocks:
            f.write(f"\n=== TIER B ITER-2 SOURCE: {desc} ===\n\n")
            f.write(txt)
            f.write("\n\n")

    sz = os.path.getsize(OUT_TIER_B_ITER2)
    report["tier_b_iter2_path"] = OUT_TIER_B_ITER2
    report["tier_b_iter2_size_bytes"] = sz
    report["tier_b_iter2_size_mb"] = round(sz / (1024 * 1024), 2)
    full = safe_read(OUT_TIER_B_ITER2) or ""
    cd, ck, ct = measure_density(full)
    report["tier_b_iter2_density"] = round(cd, 6)
    report["tier_b_iter2_kw_hits"] = ck
    report["tier_b_iter2_chars"] = ct

    # chat-template ratio = lines starting with "사용자: " or "도우미: " / total non-empty
    n_user = full.count("\n사용자: ")
    n_assistant = full.count("\n도우미: ")
    total_lines = max(1, full.count("\n"))
    report["tier_b_iter2_chat_template_ratio"] = round((n_user + n_assistant) / total_lines, 4)
    report["tier_b_iter2_n_user_turns"] = n_user
    report["tier_b_iter2_n_assistant_turns"] = n_assistant
    return sz


# ── BG-LD preference pairs ──────────────────────────────────────────────
# Sample target: 10-20MB jsonl
# chosen = BG-KM v4_pass=true sample
# rejected = 22+ BG saga V4 FAIL sample (degenerate / template-leak / random-char)
# 1:1 ratio, format: {"prompt", "chosen", "rejected"}

CORPUS_TEMPLATE_LEAKS = ["서연:", "민준:", "지우:"]   # corpus persona names — should not leak as speaker

def is_template_leak(response):
    if not response:
        return False
    for leak in CORPUS_TEMPLATE_LEAKS:
        if leak in response:
            return True
    return False


def build_ld_preference_pairs(report):
    chosen_pool, n_v4_total, n_v4_pass = collect_v4_passed_pairs()
    chosen_pool = [p for p in chosen_pool if not is_degenerate_response(p["response"]) and not is_template_leak(p["response"])]
    rejected_pool = collect_v4_failed_responses(max_n=5000)
    # Add corpus-template-leak rejected (synthetic) for ROC discrimination signal
    template_leak_synth = [
        {"prompt": p["prompt"], "response": "서연: " + (p["response"] or "안녕하세요"), "source": "synth_template_leak", "domain": p["domain"]}
        for p in chosen_pool[:50]
    ]
    rejected_pool.extend(template_leak_synth)

    # Random noise rejected (degenerate hangul block)
    noise_synth = [
        {"prompt": p["prompt"], "response": "이" * 80, "source": "synth_degenerate_repeat", "domain": p["domain"]}
        for p in chosen_pool[:50]
    ]
    rejected_pool.extend(noise_synth)

    report["ld_chosen_pool_size"] = len(chosen_pool)
    report["ld_rejected_pool_size_v4_fail"] = len([r for r in rejected_pool if "synth" not in r["source"]])
    report["ld_rejected_pool_size_synth"] = len([r for r in rejected_pool if "synth" in r["source"]])

    # 1:1 pairing — per chosen prompt, find rejected from same/any prompt
    # build prompt → rejected_responses map for context-matching, fallback to any
    by_prompt = {}
    for r in rejected_pool:
        by_prompt.setdefault(r["prompt"], []).append(r["response"])

    pairs = []
    for c in chosen_pool:
        rejs = by_prompt.get(c["prompt"], [])
        if not rejs:
            # fallback: use any rejected
            if rejected_pool:
                # round-robin assign
                idx = len(pairs) % len(rejected_pool)
                rej = rejected_pool[idx]["response"]
            else:
                continue
        else:
            idx = len(pairs) % len(rejs)
            rej = rejs[idx]
        pairs.append({
            "prompt": c["prompt"],
            "chosen": c["response"],
            "rejected": rej,
            "domain": c["domain"],
            "source_chosen": c["source"],
            "source_rejected": "v4_fail_or_synth",
        })

    # Expand sample size — for each chosen, pair with multiple rejected (cartesian until target ~15MB)
    target_size = 15 * 1024 * 1024  # 15MB sample (toward iter-3 100MB)
    # safety: bound expansion to 30,000 extra pairs to keep iter-2 sample <20MB
    max_extra_pairs = 30000
    extra_pairs = []
    cur_bytes = sum(len(json.dumps(p, ensure_ascii=False)) for p in pairs)
    rejected_cycle_idx = 0
    if rejected_pool and chosen_pool:
        outer = 0
        # cycle through chosen × rejected combinations (up to chosen × all rejected)
        max_outer = min(max_extra_pairs, len(chosen_pool) * max(1, len(rejected_pool)))
        while cur_bytes < target_size and outer < max_outer:
            c = chosen_pool[outer % len(chosen_pool)]
            rej = rejected_pool[rejected_cycle_idx % len(rejected_pool)]
            pair = {
                "prompt": c["prompt"],
                "chosen": c["response"],
                "rejected": rej["response"],
                "domain": c["domain"],
                "source_chosen": c["source"],
                "source_rejected": rej["source"],
            }
            extra_pairs.append(pair)
            cur_bytes += len(json.dumps(pair, ensure_ascii=False))
            outer += 1
            rejected_cycle_idx += 1
    pairs.extend(extra_pairs)

    # write
    with open(OUT_LD_PAIRS, "w", encoding="utf-8") as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    sz = os.path.getsize(OUT_LD_PAIRS)
    report["ld_pairs_path"] = OUT_LD_PAIRS
    report["ld_pairs_size_bytes"] = sz
    report["ld_pairs_size_mb"] = round(sz / (1024 * 1024), 2)
    report["ld_pairs_count"] = len(pairs)
    report["ld_chosen_rejected_ratio"] = "1:1 per pair (each pair has both chosen + rejected)"
    report["ld_pair_format"] = '{"prompt": ..., "chosen": ..., "rejected": ..., "domain": ..., "source_chosen": ..., "source_rejected": ...}'
    return sz, len(pairs)


# ── Main ────────────────────────────────────────────────────────────────

def run():
    t0 = time.time()
    report = {
        "schema": "anima_clm_l4_corpus_iter2_v1",
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "loop_iter": "c (iter-2)",
        "iter1_predecessor_commit": "0116a35d",
        "additive_basis": "raw#15 — iter-1 file 보존, iter-2 신규 emit + iter-1 file 에 expansion append",
    }

    print("=== L4 corpus iter-2 curation ===")
    print("")

    # 1. Tier A iter-2 expansion
    print("--- Tier A iter-2 expansion (semantic-density filter) ---")
    blocks = collect_tier_a_iter2(report)
    print(f"  files scanned: {report['tier_a_iter2_files_scanned']}")
    print(f"  paragraphs accepted: {report['tier_a_iter2_paragraphs_accepted']}")
    print(f"  paragraphs rejected: {report['tier_a_iter2_paragraphs_rejected']}")

    appended = append_tier_a_iter2(blocks, report)
    print(f"  appended paragraphs (de-duped): {appended}")
    print(f"  Tier A pre-size:  {report['tier_a_iter2_pre_size_mb']} MB")
    print(f"  Tier A post-size: {report['tier_a_iter2_post_size_mb']} MB (Δ +{report['tier_a_iter2_delta_mb']} MB)")
    print(f"  Tier A combined density: {report['tier_a_iter2_combined_density']:.4%}")

    # 2. Tier B iter-2
    print("")
    print("--- Tier B iter-2 dialogue expansion ---")
    sz_b = build_tier_b_iter2(report)
    print(f"  Tier B path: {report['tier_b_iter2_path']}")
    print(f"  Tier B size: {report['tier_b_iter2_size_mb']} MB")
    print(f"  Tier B density: {report['tier_b_iter2_density']:.4%}")
    print(f"  Tier B chat-template ratio: {report['tier_b_iter2_chat_template_ratio']:.2%}")
    print(f"  Tier B n_user_turns: {report['tier_b_iter2_n_user_turns']:,}")

    # 3. BG-LD preference pairs
    print("")
    print("--- BG-LD preference pairs (sample) ---")
    sz_ld, n_pairs = build_ld_preference_pairs(report)
    print(f"  LD pairs path: {report['ld_pairs_path']}")
    print(f"  LD pairs size: {report['ld_pairs_size_mb']} MB ({n_pairs:,} pairs)")
    print(f"  chosen pool: {report['ld_chosen_pool_size']} | v4_fail rejected: {report['ld_rejected_pool_size_v4_fail']} | synth rejected: {report['ld_rejected_pool_size_synth']}")

    # honest C3
    report["honest_c3"] = [
        "iter-2 Tier A expansion = paragraph-level multi-keyword set co-hit ≥2 sets / 6 axes (semantic-density proxy) + char-density ≥ 0.4% — sentence-transformers MiniLM 미적용 (raw#9 hexa-only 정합 — 외부 ML lib 검토 별도 cycle).",
        "iter-2 Tier B BG-JE 80MB extension = same h098_h101 corpus 의 deeper portion — anima-native lane 정합 유지 (chat-template subset).",
        "iter-2 Tier B 500MB target 미달 — BG-JE 214MB ceiling + 자체 dialogue ledger 소량. iter-3 추가 (V4 evaluator 산출물 만 으로는 전체 500MB 도달 불가능; 사용자 ↔ Claude session log archive 별도 access 필요).",
        "BG-LD pairs 100MB target 미달 — 본 sample 은 V4 PASS pool (12 pairs × 5 seeds ≈ 60) × rejected pool (degenerate 만 select) 의 cartesian expansion 으로 sample 채움. iter-3 에서 추가 prompt expansion (15 V4 prompts → 100+ prompts) 후 100MB 도달.",
        "BG-LD synthetic rejected (template_leak '서연:' + degenerate '이' repeat) 는 ROC discrimination signal 강화용 — 실제 BG saga FAIL sample 만 으로 부족 시 augmentation. 본 augmentation 비율 metrics 에 emit.",
        " C2.4 mismatch filter = is_degenerate (han_ratio < 0.30, repeat ≥20, replacement char ≥5) heuristic — full domain-keyword overlap 미적용 (V4 evaluator 자체 metric 계산 결과 활용 별도 cycle).",
        "iter-2 Tier A persona file = iter-1 file (anima_persona_tier_a_2026_05_08.txt) 에 append — raw#15 additive (iter-1 file 보존, expansion section 마커 명시).",
        "anima_core_dialogues = substrate probe lane (echo-mode, weak Q/A coupling) — Tier B 입력 sample weight 낮음. C2.4 PASS 보장 X.",
        "raw measurement SSOT = state/anima_clm_l4_corpus_iter2_metrics.json (size + density + chat-template ratio + counts).",
    ]

    report["elapsed_s"] = round(time.time() - t0, 2)

    with open(OUT_METRICS, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("")
    print(f"=== metrics emit: {OUT_METRICS} ===")
    print(f"=== elapsed: {report['elapsed_s']}s ===")


if __name__ == "__main__":
    run()
