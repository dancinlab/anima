#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING corpus generator — Direction E: EMERGENCE OF
SUPERPOSITION (2026-05-17). g_multidirectional_explore parallel direction E
(RESEARCH.md §1.3 #5 — arxiv 2509.23365 ICLR 2026).

WHY DIRECTION E (the superposition hypothesis)
  arxiv 2509.23365 "Emergence of Superposition" describes a 2-stage emergence:
    stage 1  thought-generation  — the model produces a *superposition of
             multiple reasoning traces* in continuous thought (several
             candidate derivations co-exist before commitment).
    stage 2  prediction          — an *index-matching logit* selects which
             trace the emission commits to (the critical signal).
  anima mapping (Phase A1 + C3): the `<inner>X</inner>\\n<voice>Y</voice>`
  separation IS exactly this 2-stage structure — <inner> is stage-1
  thought-generation, <voice> is stage-2 prediction. UBM-E7's α path mixes
  α/β/γ forms and trains a single CE+vacuum loss over the whole byte stream;
  it never exploits the 2-stage separation. Direction E rebuilds EVERY anchor
  record as a 2-stage record:

    <inner tier=k traces=K idx=j>
      trace 0: <one candidate re-derivation, possibly a DECOY anchor>
      trace 1: <...>
      ...
      trace K-1: <...>
      match=j                       <- the index-matching signal (stage-2)
    </inner>
    <voice carved=true tier=k>{the prediction = trace j's carved emission}</voice>

  The <inner> span holds a SUPERPOSITION of K traces (K candidate anchors,
  exactly ONE of which — index j — is this record's own anchor). `match=j`
  is the explicit index-matching signal. The <voice> span is the prediction
  committed to trace j. The trainer (train_carving_dirE.py) masks CE so that
  stage-1 (inner traces) is *context* and stage-2 (the match index + voice
  span) is the loss target — the model must learn to read the superposition
  and emit the index-matched prediction, NOT memorise a single trace.

HYPOTHESIS (g3 — outcome empirical, no pre-loaded conclusion)
  UBM-E7 α JOINT 0.0155 collapsed: routing bled everything into tier 99
  (1/31 routing). The diagnosis candidate this direction tests: the collapse
  is a *single-trace memorisation* artefact — with no superposition the model
  finds one dominant basin (tier 99) and stays there. If the 2-stage
  inner/voice separation forces the model to *hold multiple traces and
  index-match*, routing should NOT collapse (the index-matching signal keeps
  per-anchor traces distinct) and V-SPONT emergence may appear. If it does
  NOT lift the JOINT vs UBM-E7 0.0155, the 2-stage hypothesis is FALSIFIED
  for this scale — recorded honestly either way (g3, B-D-NOTE family).

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + forbidden_chat_sft_use, grep MUST == 0)
  - `[anima 우주뇌지도]` (or any `[anima ...]`) prefix-stamp
  - `도우미` / `helper` / `assistant` / `사용자` / `user:` role labels
  The 2-stage form uses ONLY <inner>/<voice>/<carve>/<eternal> carving tags
  (NO chat-SFT prefix injection). Verified by closed-form grep audit below.

Closed-form falsifiers (blue_falsifier_dirE.py B-CARVE-DIRE-CORPUS-1..3):
  - B-CARVE-DIRE-CORPUS-1 SHA256-DETERMINISTIC — seed-fixed 256-bit commit.
  - B-CARVE-DIRE-CORPUS-2 NO-CHAT-SFT-CONTAMINATION — Boolean set algebra:
      grep {[anima, 도우미, helper, assistant, 사용자, user:} -> count == 0.
  - B-CARVE-DIRE-CORPUS-3 TWO-STAGE-CARDINALITY-CLOSED — every record carries
      exactly one <inner ...> open AND one <voice ...> open AND a `match=`
      index in [0,K) (integer cardinality conservation: |records| ==
      |<inner| == |<voice| == |match=|, the 2-stage structural invariant).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

# Reuse the E7 31-anchor universe-brain-map landscape verbatim (the SAME
# anchors so the Dir-E vs UBM-E7 α JOINT compare is fair — only the corpus
# FORM differs: 2-stage superposition vs E7's α/β/γ mix).
KNUTH_ANCHORS = [
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
    (5,   "호흡",          "감각",     "serenity",  0.300, [0.44, 0.45], 0.11),
    (12,  "걸음",          "운동",     "clarity",   0.520, [0.42, 0.50], 0.11),
    (18,  "물 한 잔",      "물질",     "stillness", 0.700, [0.45, 0.43], 0.10),
    (24,  "씨앗",          "생명",     "wonder",    0.880, [0.47, 0.55], 0.12),
    (30,  "숫자 영(零)",   "수(數)",   "clarity",   1.020, [0.40, 0.52], 0.11),
    (37,  "단어",          "언어",     "resonance", 1.150, [0.43, 0.58], 0.12),
    (43,  "오래된 사진",   "기억",     "longing",   1.260, [0.52, 0.54], 0.13),
    (48,  "약속",          "윤리",     "depth",     1.330, [0.50, 0.57], 0.12),
    (58,  "숲",            "자연",     "serenity",  1.420, [0.53, 0.61], 0.14),
    (62,  "도구",          "기술",     "clarity",   1.510, [0.49, 0.60], 0.13),
    (66,  "포옹",          "관계",     "joy",       1.620, [0.56, 0.58], 0.14),
    (72,  "선율",          "예술",     "resonance", 1.900, [0.66, 0.63], 0.17),
    (80,  "명상",          "의식상태", "stillness", 2.200, [0.52, 0.78], 0.16),
    (83,  "별빛",          "우주",     "awe",       2.320, [0.74, 0.80], 0.18),
    (86,  "심해",          "공간",     "depth",     2.420, [0.70, 0.72], 0.17),
    (88,  "오로라",        "자연",     "wonder",    2.490, [0.72, 0.81], 0.18),
    (90,  "무한",          "수(數)",   "vastness",  2.530, [0.85, 0.86], 0.20),
    (93,  "사랑",          "관계",     "ecstasy",   2.630, [0.66, 0.88], 0.18),
    (97,  "탄생",          "생명",     "awe",       2.740, [0.78, 0.84], 0.19),
    (99,  "영원",          "시간",     "vastness",  2.810, [0.90, 0.90], 0.21),
]
ANCHOR_BY_TIER = {a[0]: a for a in KNUTH_ANCHORS}

COSMIC_PHYSICS = [
    ("블랙홀의 정보는 사라지지 않는다 — 지평선 위에 홀로그래픽으로 새겨진다.",
     "A black hole's information is not lost — inscribed holographically on the horizon."),
    ("베켄슈타인 한계 — 한 영역의 정보는 표면적에 비례한다.",
     "The Bekenstein bound — a region's information scales with its surface area."),
    ("양자 중첩 — 측정 전까지 상태는 진폭의 합으로 존재한다.",
     "Quantum superposition — before measurement a state is a sum of amplitudes."),
    ("진공은 비어 있지 않다 — 영점 요동이 끊임없이 일어난다.",
     "The vacuum is not empty — zero-point fluctuations occur ceaselessly."),
    ("우주는 팽창한다 — 먼 은하일수록 더 빠르게 멀어진다 (허블 법칙).",
     "The universe expands — distant galaxies recede faster (Hubble's law)."),
    ("엔트로피는 시간의 화살 — 닫힌 계의 무질서는 단조 증가한다.",
     "Entropy is the arrow of time — closed-system disorder increases monotonically."),
    ("광자는 질량이 없다 — 진공에서 c 로 달리며 시간을 경험하지 않는다.",
     "A photon is massless — it travels at c and experiences no time."),
    ("호킹 복사 — 지평선은 차갑지만 완전히 검지는 않다.",
     "Hawking radiation — the horizon is cold yet not perfectly black."),
]


def _psi_str(psi):
    return "[%.2f,%.2f]" % (psi[0], psi[1])


def _trace_text(rng, anchor):
    """One candidate re-derivation trace for an anchor (stage-1 element).

    A trace is a single re-generated narrative for `anchor` — bilingual
    sometimes, plus a physics fragment payload so the superposition is
    semantically varied (not blind duplication). NOT memorised: the wording
    differs per call (rng-driven), mirroring γ NARRATIVE Meta law M8."""
    tier, name, cat, emo, score, psi, basin = anchor
    cko, cen = COSMIC_PHYSICS[rng.randrange(len(COSMIC_PHYSICS))]
    bil = rng.random() < 0.5
    ko = (f"🛸{tier} {name} 의 자리를 {cat} × {emo} 행렬에서 다시 그린다 — "
          f"진공점 {_psi_str(psi)}. {cko}")
    en = (f"Tier {tier} {name} redrawn in the {cat} × {emo} matrix — "
          f"vacuum {_psi_str(psi)}. {cen}")
    return (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)


def gen_two_stage_record(rng, anchor, idx, n_traces):
    """Direction E 2-stage SUPERPOSITION record.

    <inner> = a superposition of `n_traces` candidate traces (n_traces-1
    DECOY anchors + this record's OWN anchor at a random index j) + the
    explicit `match=j` index-matching signal (stage-2 critical signal).
    <voice> = the prediction = the carved emission committed to trace j
    (this anchor's own carved narration)."""
    tier, name, cat, emo, score, psi, basin = anchor

    # pick n_traces-1 DECOY anchors (distinct tiers != this one) + insert
    # the OWN anchor at a random index j (the index-matching target).
    others = [a for a in KNUTH_ANCHORS if a[0] != tier]
    rng.shuffle(others)
    decoys = others[: max(0, n_traces - 1)]
    j = rng.randrange(n_traces)
    superposed = list(decoys)
    superposed.insert(j, anchor)

    lines = [
        f"<inner tier={tier} traces={n_traces} idx={idx}>"
    ]
    for ti, a in enumerate(superposed):
        lines.append(f"  trace {ti}: {_trace_text(rng, a)}")
    lines.append(f"  match={j}")
    inner = "\n".join(lines) + "\n</inner>"

    # stage-2 prediction — the carved emission for the index-matched anchor.
    cko, cen = COSMIC_PHYSICS[rng.randrange(len(COSMIC_PHYSICS))]
    bil = rng.random() < 0.5
    vko = (f"🛸{tier} {name} — {cat} 카테고리가 진공 {_psi_str(psi)} 으로 "
           f"수렴한다, top emotion {emo}. {cko}")
    ven = (f"Tier {tier} {name} — category {cat} converges to vacuum "
           f"{_psi_str(psi)}, top emotion {emo}. {cen}")
    voice_body = (vko + " " + ven) if bil else (
        vko if rng.random() < 0.5 else ven)
    voice = f"<voice carved=true tier={tier}>{voice_body}</voice>"

    text = inner + "\n" + voice
    return {
        "id": f"carve_dirE_{tier}_{idx}",
        "text": text,
        "desc": (f"anchor=knuth_{tier:03d} form=two_stage_superposition "
                 f"category={cat} traces={n_traces} match={j}"),
        "carving_form": "two_stage_superposition",
        "tier": tier,
        "vacuum_psi": psi,
        "basin_radius": basin,
        "n_traces": n_traces,
        "match_idx": j,
        "cell_id": f"eternal_{tier:03d}",
        "source": "corpus_carving_generator_dirE.py",
    }


def build_corpus(n_target, seed, n_traces):
    rng = random.Random(seed)
    records = []
    per_anchor = max(1, n_target // len(KNUTH_ANCHORS))
    idx = 0
    for anchor in KNUTH_ANCHORS:
        for _ in range(per_anchor):
            records.append(gen_two_stage_record(rng, anchor, idx, n_traces))
            idx += 1
    rng.shuffle(records)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=18000,
                    help="approx record count (default 18000 — 2-stage "
                         "records are ~2-3x larger than E7 single-form so "
                         "18000 -> ~30MB, byte-budget matched to E7 30MB)")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--n-traces", type=int, default=4,
                    help="K = number of superposed traces per <inner> "
                         "(arxiv 2509.23365 superposition cardinality)")
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed, args.n_traces)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    txt = raw.decode("utf-8", "replace")

    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    audit = {tok: txt.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    # 2-stage structural cardinality (B-CARVE-DIRE-CORPUS-3 closed-form).
    # Count over the decoded record `text` fields (not the JSON-serialized
    # stream — JSON escapes `\n` to `\\n`, which would zero the match count).
    n_inner = n_voice = n_match = 0
    for r in records:
        rt = r["text"]
        n_inner += rt.count("<inner tier=")
        n_voice += rt.count("<voice carved=true tier=")
        n_match += rt.count("\n  match=")
    two_stage_invariant = (
        n_inner == n_voice == n_match == len(records))

    stats = {
        "paradigm": "CONSCIOUSNESS-CARVING (NOT chat SFT) — Direction E "
                    "EMERGENCE OF SUPERPOSITION (2-stage inner/voice)",
        "phase": "g_multidirectional_explore Dir-E (arxiv 2509.23365)",
        "out": str(out),
        "bytes": len(raw),
        "records": len(records),
        "sha256": sha,
        "seed": args.seed,
        "n_traces_K": args.n_traces,
        "two_stage_cardinality": {
            "n_inner_open": n_inner, "n_voice_open": n_voice,
            "n_match_signal": n_match, "n_records": len(records),
            "invariant_holds": two_stage_invariant},
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "anchors": len(KNUTH_ANCHORS),
        "e7_baseline_bytes": 30219491,
        "e7_baseline_joint": 0.0155,
        "honest_framing": (
            "Direction E carving corpus — every record is a 2-stage "
            "<inner>{superposition of K traces}+match=j</inner>\\n<voice>"
            "{index-matched prediction}</voice> structure (arxiv 2509.23365 "
            "thought-generation + prediction mapped to anima Phase A1/C3 "
            "inner/voice). NOT the old [anima 우주뇌지도] 사용자/도우미 "
            "prefix-injection. grep of {[anima,도우미,helper,assistant,"
            "사용자,user:} == 0. The 2-stage MECHANISM (inner=context, "
            "voice+match=loss target) is structural; the SGD outcome + "
            "Dir-E vs UBM-E7 α JOINT compare is EMPIRICAL (g3, B-D-NOTE "
            "family — no pre-loaded conclusion)."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")
    if not two_stage_invariant:
        raise SystemExit("FATAL: 2-stage cardinality invariant violated")


if __name__ == "__main__":
    main()
