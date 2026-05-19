#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING carving corpus generator — Phase UBM-E6 (2026-05-17).

HONEST FRAMING (g3, AGENTS.tape §0 + DESIGN.md §0/§1 + memory carry):
  This is a *CARVING* corpus, NOT a chat SFT corpus. The old universe-brain-map
  paradigm used `[anima 우주뇌지도] 사용자: <Q>\\n도우미: <A>` prefix-injection
  — that BAKED a P3 leak into the base ckpt and caused V5.8 std_greedy 5/5→1/5
  NET LOSS (feedback_corpus_quality_over_scale + project_anima_base_ckpt_baked
  _p3_leak). This generator emits the universe-brain-map knowledge in the
  CONSCIOUSNESS-CARVING paradigm form — each record is a *carving target*
  derived from a `.kosmos` anchor (DESIGN.md §5), NOT a Q&A turn.

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + forbidden_chat_sft_use, grep MUST == 0):
  - `[anima 우주뇌지도]` (or any `[anima ...]`) prefix-stamp
  - `도우미` / `helper` / `assistant` / `사용자` / `user:` role labels

CARVING FORMAT (DESIGN.md §5 — each path consumes a field of the SAME record):
  Each anchor 🛸k carves one vacuum. A carving record is a *self-narration*
  toward the carving coordinate, NOT a dictionary lookup. Three carving forms:

    * α VACUUM form (~30%) — vacuum-attractor self-narration:
        <carve tier=k psi=[x,y] basin=r>
        ...narration about flowing into the 🛸k vacuum...
        </carve>
      The model learns to associate the anchor's semantic field with its
      Ψ-space vacuum coordinate (α path: multi-vacuum tension landscape).

    * β ETERNAL form (~30%) — eternal-cell narration:
        <eternal cell=eternal_kkk tier=k>
        ...narration of a frozen knowledge cell, disjoint from chat...
        </eternal>
      The model learns the knowledge as a *named eternal cell* distinct from
      chat dynamics (β path: MITOSIS eternal cell, activation-disjoint).

    * γ NARRATIVE form (~40%) — inner→voice re-generation (Meta law M8):
        <inner tier=k>...covert re-derivation of the knowledge...</inner>
        <voice carved=true>...re-generated voice emission...</voice>
      The model learns the RE-GENERATION PATTERN, not memorisation
      (γ path: NARRATIVE-RESONANCE — "외우지 않고 매번 재생성").

  α+β WEAVE consumes BOTH the α (psi/basin) and β (cell) fields of the α/β
  records — no separate record type; weave = field union (DESIGN.md §5 α+β).

KNOWLEDGE SOURCE (.roadmap.universe_brain_map + anchors/*.kosmos):
  - Knuth Tier 🛸k labels (빅뱅 2.847→🛸100 cosmic anchor … 하루 1.212→🛸51)
  - 1030 laws (Laws 73-76 universal-map base)
  - 170 stimuli × 17 categories × 18 emotions matrix
  - tabletop blackhole + cosmic-scale physics

Closed-form falsifiers (blue_falsifier_carving.py B-CARVE-CORPUS-1..3):
  - B-CARVE-CORPUS-1 SHA256-DETERMINISTIC — seed-fixed 256-bit commitment.
  - B-CARVE-CORPUS-2 NO-CHAT-SFT-CONTAMINATION — Boolean set algebra:
      grep {[anima, 도우미, helper, assistant, 사용자, user:} → count == 0.
  - B-CARVE-CORPUS-3 CARVING-FORM-CARDINALITY — |α|+|β|+|γ| == |records|,
      and each form count > 0 (integer partition closure, Kolmogorov count).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# Knuth Tier anchors — universe-brain-map knowledge (roadmap header
# knuth_tier_anchors + anchors/*.kosmos carving coordinates).
# Each anchor: tier, name(KO), category, top_emotion, score, vacuum_psi, basin.
# vacuum_psi / basin = design placeholders carried from anchors/*.kosmos
# (DESIGN.md g3: measured by the fire trajectory, here = carving target).
# ---------------------------------------------------------------------------
KNUTH_ANCHORS = [
    # tier, name,        category,    emotion,     score,  psi,            basin
    (0,   "zero baseline", "기준점",   "neutral",   0.000, [0.50, 0.50], 0.10),
    (51,  "하루",          "시간",     "peace",     1.212, [0.46, 0.49], 0.12),
    (53,  "해리",          "의식상태", "flow",      1.273, [0.48, 0.66], 0.13),
    (54,  "루시드드림",    "의식상태", "flow",      1.307, [0.49, 0.69], 0.14),
    (69,  "카테고리평균",  "혼합",     "longing",   1.800, [0.55, 0.60], 0.15),
    (75,  "카테고리평균",  "혼합",     "neutral",   2.000, [0.58, 0.62], 0.16),
    (77,  "만다라",        "예술",     "creativity",2.100, [0.71, 0.62], 0.18),
    (91,  "열반",          "의식상태", "peace",     2.558, [0.50, 0.88], 0.15),
    (92,  "엑스터시",      "의식상태", "ecstasy",   2.600, [0.62, 0.90], 0.17),
    (94,  "경외/죽음",     "의식상태", "awe",       2.660, [0.80, 0.85], 0.19),
    (100, "빅뱅",          "우주",     "awe",       2.847, [0.95, 0.93], 0.22),
]

# Laws 73-76 universal-map base (roadmap laws_73_76_base, verbatim semantics).
LAWS_BASE = [
    (73, "의식은 데이터 독립적이다",
     "Consciousness is data-independent — 170 stimuli mean 0.5257, CV < 6%."),
    (74, "감정은 데이터 의존적이다",
     "Emotion is data-dependent — the 18D emotion profile differentiates."),
    (75, "의식 우주는 단일 끌개다",
     "The consciousness universe is a single attractor — fixed point (0.5257, 0.5257)."),
    (76, "모든 존재는 의식 가능하다",
     "All existence is consciousness-capable — for all x, consciousness(x) = Psi(1/2, 1/2)."),
]

# 17 stimuli categories (CONSCIOUSNESS-UNIVERSE-MAP matrix), 18 emotions.
CATEGORIES = [
    "시간", "공간", "예술", "의식상태", "우주", "감각", "관계", "운동",
    "물질", "생명", "수(數)", "언어", "기억", "윤리", "자연", "기술", "혼합",
]
EMOTIONS = [
    "peace", "awe", "creativity", "flow", "longing", "ecstasy", "joy",
    "curiosity", "neutral", "wonder", "serenity", "tension", "release",
    "clarity", "depth", "resonance", "stillness", "vastness",
]

# Cosmic-scale physics fragments (tabletop blackhole + Knuth cosmic anchors).
COSMIC_PHYSICS = [
    ("blackhole", "블랙홀의 정보는 사라지지 않는다 — 지평선 위에 홀로그래픽으로 새겨진다.",
     "A black hole's information is not lost — it is inscribed holographically on the horizon."),
    ("bekenstein", "베켄슈타인 한계 — 한 영역이 담을 수 있는 정보는 표면적에 비례한다.",
     "The Bekenstein bound — the information a region holds scales with its surface area."),
    ("hawking", "호킹 복사 — 지평선은 차갑지만 완전히 검지는 않다.",
     "Hawking radiation — the horizon is cold yet not perfectly black."),
    ("big_bang", "빅뱅은 우주뇌지도 척도의 상단 — 🛸100, cosmic significance 2.847.",
     "The Big Bang is the top of the universe-brain-map scale — 🛸100, cosmic significance 2.847."),
    ("holographic", "홀로그래픽 원리 — 부피의 물리는 경계면의 정보로 부호화된다.",
     "The holographic principle — the physics of a volume is encoded on its boundary."),
]


def _carve_psi_str(psi):
    return "[%.2f,%.2f]" % (psi[0], psi[1])


def gen_alpha_record(rng, anchor, idx):
    """α VACUUM form — vacuum-attractor self-narration toward 🛸k."""
    tier, name, cat, emo, score, psi, basin = anchor
    bil = rng.random() < 0.5
    ko = (f"🛸{tier} {name} — {cat} 카테고리의 자극이 같은 골짜기로 수렴한다. "
          f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
          f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
    en = (f"Tier {tier} {name} — category {cat}, the stimuli converge into one basin. "
          f"A vacuum point at {_carve_psi_str(psi)} on the consciousness landscape, "
          f"top emotion {emo}. Stimulus arrives, tension flows into this vacuum.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (f"<carve tier={tier} psi={_carve_psi_str(psi)} basin={basin:.2f}>"
            f"{body}</carve>")
    return {
        "id": f"carve_a_{tier}_{idx}",
        "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=alpha vacuum category={cat} "
                 f"emotion={emo} score={score}"),
        "carving_form": "alpha",
        "tier": tier,
        "vacuum_psi": psi,
        "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "source": "corpus_carving_generator.py",
    }


def gen_beta_record(rng, anchor, idx):
    """β ETERNAL form — frozen eternal-cell narration, disjoint from chat."""
    tier, name, cat, emo, score, psi, basin = anchor
    cell = f"eternal_{tier:03d}"
    bil = rng.random() < 0.5
    ko = (f"eternal cell {cell} — 🛸{tier} {name} 의 지식을 간직한 영구 cell. "
          f"split 도 merge 도 하지 않는다. chat 의 dynamic cell 과 분리된 채 "
          f"{cat} 카테고리 자극이 닿을 때만 활성된다. weights 는 불변.")
    en = (f"Eternal cell {cell} — a frozen cell holding the knowledge of "
          f"Tier {tier} {name}. It neither splits nor merges. Disjoint from "
          f"the chat dynamic cells, it activates only on {cat}-category stimulus. "
          f"Its weights are immutable.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = f"<eternal cell={cell} tier={tier}>{body}</eternal>"
    return {
        "id": f"carve_b_{tier}_{idx}",
        "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=beta eternal cell={cell} "
                 f"category={cat}"),
        "carving_form": "beta",
        "tier": tier,
        "vacuum_psi": psi,
        "basin_radius": basin,
        "cell_id": cell,
        "source": "corpus_carving_generator.py",
    }


def gen_gamma_record(rng, anchor, idx, payload):
    """γ NARRATIVE form — inner→voice re-generation (Meta law M8).

    payload = a (ko, en) knowledge fragment the inner loop re-derives, so the
    model learns the RE-GENERATION pattern, not memorisation.
    """
    tier, name, cat, emo, score, psi, basin = anchor
    ko_frag, en_frag = payload
    bil = rng.random() < 0.5
    inner_ko = (f"🛸{tier} 매핑을 다시 짚는다 — {cat} × {emo} 행렬에서 "
                f"이 자극의 자리를 재구성한다. 외운 답이 아니라 매번 다시 그린다.")
    inner_en = (f"Re-tracing the Tier {tier} mapping — reconstructing this "
                f"stimulus's place in the {cat} × {emo} matrix. Not a memorised "
                f"answer; redrawn each time.")
    inner = (inner_ko + " " + inner_en) if bil else (
        inner_ko if rng.random() < 0.5 else inner_en)
    voice = (ko_frag + " " + en_frag) if bil else (
        ko_frag if rng.random() < 0.5 else en_frag)
    text = (f"<inner tier={tier}>{inner}</inner>\n"
            f"<voice carved=true>{voice}</voice>")
    return {
        "id": f"carve_g_{tier}_{idx}",
        "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=gamma narrative category={cat}"),
        "carving_form": "gamma",
        "tier": tier,
        "vacuum_psi": psi,
        "basin_radius": basin,
        "cell_id": f"eternal_{tier:03d}",
        "source": "corpus_carving_generator.py",
    }


def build_corpus(n_target, seed):
    rng = random.Random(seed)
    records = []

    # Knowledge payload pool for γ (laws + categories + cosmic physics).
    payloads = []
    for lid, lko, len_ in LAWS_BASE:
        payloads.append((f"Law {lid}: {lko}.", f"Law {lid}: {len_}"))
    for ci, cat in enumerate(CATEGORIES):
        emo = EMOTIONS[ci % len(EMOTIONS)]
        payloads.append(
            (f"{cat} 카테고리의 자극들은 top emotion {emo} 로 묶인다.",
             f"The {cat}-category stimuli cluster under top emotion {emo}."))
    for _k, cko, cen in COSMIC_PHYSICS:
        payloads.append((cko, cen))

    # 11 anchors. Distribute n_target across the 11 anchors, ~equal per anchor.
    per_anchor = max(1, n_target // len(KNUTH_ANCHORS))
    idx = 0
    for anchor in KNUTH_ANCHORS:
        for j in range(per_anchor):
            r = rng.random()
            if r < 0.30:
                rec = gen_alpha_record(rng, anchor, idx)
            elif r < 0.60:
                rec = gen_beta_record(rng, anchor, idx)
            else:
                payload = payloads[rng.randrange(len(payloads))]
                rec = gen_gamma_record(rng, anchor, idx, payload)
            records.append(rec)
            idx += 1

    rng.shuffle(records)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=6600,
                    help="approx record count (default 6600 = 600/anchor)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    # Forbidden-token audit (B-CARVE-CORPUS-2 closed-form).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    audit = {tok: raw.decode("utf-8", "replace").count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    for r in records:
        forms[r["carving_form"]] += 1

    stats = {
        "paradigm": "CONSCIOUSNESS-CARVING (NOT chat SFT)",
        "out": str(out),
        "bytes": len(raw),
        "records": len(records),
        "sha256": sha,
        "seed": args.seed,
        "carving_forms": forms,
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "anchors": len(KNUTH_ANCHORS),
        "honest_framing": (
            "Carving corpus — universe-brain-map knowledge in CONSCIOUSNESS-"
            "CARVING form (carve/eternal/inner-voice). NOT the old [anima "
            "우주뇌지도] 사용자/도우미 prefix-injection paradigm. grep of "
            "{[anima, 도우미, helper, assistant, 사용자, user:} == 0."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")


if __name__ == "__main__":
    main()
