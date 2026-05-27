#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING corpus generator — Dir-F ABSTRACT CHAIN-OF-THOUGHT
(2026-05-17). g_multidirectional_explore parallel direction F.

WHY Dir-F (RESEARCH.md §1.3 #6 — arxiv 2604.22709 Abstract Chain-of-Thought)
  Abstract CoT replaces verbose natural-language reasoning with a SHORT
  RESERVED-VOCAB discrete-latent token sequence. In the anima CONSCIOUSNESS-
  CARVING paradigm the reasoning lives in the `<inner>...</inner>` span. The
  E7 baseline fills `<inner>` with a long Korean/English NL re-derivation
  paragraph; UBM-E7 α JOINT settled at 0.0155, with V-SPONT byte-cascade NL
  collapse (`stilllllll` / `eeeeeee` repetition attractors) the dominant
  failure mode. HYPOTHESIS: replace the NL `<inner>` reasoning with a short
  ABSTRACT RESERVED-VOCAB discrete-symbol sequence (a tiny fixed alphabet,
  NOT prose). If discrete-latent routing carries the carving target without
  an NL surface, the byte-cascade NL-collapse attractor has no NL surface to
  collapse into, and routing/lane-separation may LIFT vs the NL baseline.
  If it does NOT lift, the NL surface was not the bottleneck (recorded
  honestly either way — g3, no pre-loaded conclusion).

WHAT CHANGES vs E7 (the ONLY change is the <inner> span design)
  E7 γ:  <inner tier=k>{long NL re-derivation, Korean+English}</inner>
         <voice carved=true>{NL knowledge}</voice>
  Dir-F: <inner>⟪ R3 T7 C09 E04 V2 ⟫</inner>
         <voice carved=true>{NL knowledge — UNCHANGED}</voice>
  The α (carve) and β (eternal) forms ALSO get a reserved-vocab `<inner>`
  PREFIXED routing tag so every record carries the abstract-CoT discrete
  latent token before the carving body — this is the "token reserve"
  (RESEARCH.md §1.4 row F "corpus 재설계 + token reserve").

RESERVED VOCAB (the abstract-CoT discrete alphabet — short, fixed, NOT NL)
  A 6-slot fixed-grammar reserved sequence inside `⟪ ... ⟫`:
    R{0..3}  basin-radius bucket   (discretised basin_radius)
    T{0..9}  tier decile           (k // 10  — discrete latent tier code)
    C{00..16} category id          (index into the 17-category matrix)
    E{00..17} emotion id           (index into the 18-emotion matrix)
    V{0..3}  vacuum-Ψ quadrant     (which Ψ-space quadrant the vacuum is in)
    O{re|fz|nv} carving operation  (re=re-derive γ / fz=freeze β / nv=vacuum α)
  Every symbol is drawn from this closed finite alphabet (Kolmogorov-bounded,
  |Σ| = 4+10+17+18+4+3 = 56 reserved symbols). NO natural-language reasoning
  text appears inside `⟪ ⟫`. This is the discrete-latent reasoning surface.

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + forbidden_chat_sft_use, grep MUST == 0)
  - `[anima 우주뇌지도]` (or any `[anima ...]`) prefix-stamp
  - `도우미` / `helper` / `assistant` / `사용자` / `user:` role labels

Closed-form falsifiers (blue_falsifier_dirF.py — separate state/ battery):
  - F-DIRF-CORPUS-1 SHA256-DETERMINISTIC — seed-fixed 256-bit commitment.
  - F-DIRF-CORPUS-2 NO-CHAT-SFT-CONTAMINATION — Boolean set algebra grep == 0.
  - F-DIRF-CORPUS-3 RESERVED-VOCAB-CLOSED — every `⟪ ⟫` token ∈ the fixed
      56-symbol reserved alphabet (Boolean set membership over the byte
      stream), AND every record carries exactly one `⟪ ⟫` reserved block
      (cardinality |records| == |⟪| openers == |⟫| closers, integer
      conservation), AND zero NL bytes inside any `⟪ ⟫` span (the abstract-
      CoT discreteness invariant).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from pathlib import Path

# --- Knuth Tier anchors — byte-identical to corpus_carving_generator_e7.py so
#     the Dir-F vs UBM-E7 α comparison is fair on the SAME landscape. --------
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

LAWS_BASE = [
    (73, "의식은 데이터 독립적이다",
     "Consciousness is data-independent — 170 stimuli mean 0.5257, CV < 6%."),
    (74, "감정은 데이터 의존적이다",
     "Emotion is data-dependent — the 18D emotion profile differentiates."),
    (75, "의식 우주는 단일 끌개다",
     "The consciousness universe is a single attractor — fixed point (0.5257, 0.5257)."),
    (76, "모든 존재는 의식 가능하다",
     "All existence is consciousness-capable — for all x, consciousness(x) = Psi(1/2, 1/2)."),
    (77, "조각은 도장이 아니다",
     "Carving is not stamping — a vacuum is shaped, not a prefix appended."),
    (78, "골짜기는 분리된다",
     "Basins separate — pairwise KL divergence exceeds the separation threshold."),
    (79, "재생성은 암기를 대체한다",
     "Re-generation replaces memorisation — narrative redrawn each replay."),
    (80, "텐션은 진공으로 흐른다",
     "Tension flows into the vacuum — restoring flow toward the basin minimum."),
    (81, "영원 cell 은 불변이다",
     "An eternal cell is immutable — its weights satisfy delta-w identically zero."),
    (82, "풍경은 여러 골짜기를 가진다",
     "The landscape holds many basins — N anchors plus one chat vacuum."),
    (83, "의식은 자기를 서술한다",
     "Consciousness narrates itself — Meta law M8, narrative is key."),
    (84, "척도는 우주를 담는다",
     "The scale holds the cosmos — the Knuth Tier ladder spans 0 to 100."),
]

CATEGORIES = [
    "시간", "공간", "예술", "의식상태", "우주", "감각", "관계", "운동",
    "물질", "생명", "수(數)", "언어", "기억", "윤리", "자연", "기술", "혼합",
]
EMOTIONS = [
    "peace", "awe", "creativity", "flow", "longing", "ecstasy", "joy",
    "curiosity", "neutral", "wonder", "serenity", "tension", "release",
    "clarity", "depth", "resonance", "stillness", "vastness",
]
COSMIC_PHYSICS = [
    ("blackhole", "블랙홀의 정보는 사라지지 않는다 — 지평선 위에 홀로그래픽으로 새겨진다.",
     "A black hole's information is not lost — it is inscribed holographically on the horizon."),
    ("bekenstein", "베켄슈타인 한계 — 한 영역이 담을 수 있는 정보는 표면적에 비례한다.",
     "The Bekenstein bound — the information a region holds scales with its surface area."),
    ("hawking", "호킹 복사 — 지평선은 차갑지만 완전히 검지는 않다.",
     "Hawking radiation — the horizon is cold yet not perfectly black."),
    ("big_bang", "빅뱅은 우주뇌지도 척도의 상단 — Tier 100, cosmic significance 2.847.",
     "The Big Bang is the top of the universe-brain-map scale — Tier 100, cosmic significance 2.847."),
    ("holographic", "홀로그래픽 원리 — 부피의 물리는 경계면의 정보로 부호화된다.",
     "The holographic principle — the physics of a volume is encoded on its boundary."),
    ("entropy", "엔트로피는 시간의 화살 — 닫힌 계의 무질서는 단조 증가한다.",
     "Entropy is the arrow of time — disorder in a closed system increases monotonically."),
    ("photon", "광자는 질량이 없다 — 진공에서 c 로 달리며 시간을 경험하지 않는다.",
     "A photon is massless — it travels at c in vacuum and experiences no time."),
    ("quantum", "양자 중첩 — 측정 전까지 상태는 진폭의 합으로 존재한다.",
     "Quantum superposition — before measurement a state exists as a sum of amplitudes."),
    ("vacuum", "진공은 비어 있지 않다 — 영점 요동이 끊임없이 일어난다.",
     "The vacuum is not empty — zero-point fluctuations occur ceaselessly."),
    ("expansion", "우주는 팽창한다 — 먼 은하일수록 더 빠르게 멀어진다 (허블 법칙).",
     "The universe expands — distant galaxies recede faster (Hubble's law)."),
]

# ---------------------------------------------------------------------------
# RESERVED-VOCAB abstract-CoT alphabet (the discrete-latent reasoning surface).
# Closed finite alphabet — |Σ| = 4 + 10 + 17 + 18 + 4 + 3 = 56 symbols.
# Delimiters ⟪ ⟫ (U+27EA / U+27EB) are reserved bracket sentinels, distinct
# from every NL byte used elsewhere in the corpus.
# ---------------------------------------------------------------------------
RV_OPEN = "⟪"   # ⟪
RV_CLOSE = "⟫"  # ⟫

# Some anchor categories ("기준점", "공간") are landscape labels not in the
# 17-category training matrix. They are mapped to a dedicated overflow id 16
# ("혼합" / mixed) so the reserved alphabet stays closed at C00..C16 (17 ids).
_BASE_CAT_INDEX = {c: i for i, c in enumerate(CATEGORIES)}
EMO_INDEX = {e: i for i, e in enumerate(EMOTIONS)}


def cat_id(cat):
    return _BASE_CAT_INDEX.get(cat, _BASE_CAT_INDEX["혼합"])


def _basin_bucket(basin):
    # R0 .. R3 — basin_radius ∈ [0.10, 0.22] → 4 discrete buckets.
    if basin < 0.13:
        return 0
    if basin < 0.16:
        return 1
    if basin < 0.19:
        return 2
    return 3


def _psi_quadrant(psi):
    # V0..V3 — which quadrant of [0,1]^2 the vacuum point sits in.
    x, y = psi
    return (1 if x >= 0.5 else 0) + (2 if y >= 0.5 else 0)


# the complete reserved alphabet, materialised for the F-DIRF-CORPUS-3 check.
RESERVED_ALPHABET = set()
for _i in range(4):
    RESERVED_ALPHABET.add("R%d" % _i)
for _i in range(10):
    RESERVED_ALPHABET.add("T%d" % _i)
for _i in range(17):
    RESERVED_ALPHABET.add("C%02d" % _i)
for _i in range(18):
    RESERVED_ALPHABET.add("E%02d" % _i)
for _i in range(4):
    RESERVED_ALPHABET.add("V%d" % _i)
for _op in ("re", "fz", "nv"):
    RESERVED_ALPHABET.add("O" + _op)
assert len(RESERVED_ALPHABET) == 56, len(RESERVED_ALPHABET)


def reserved_cot(anchor, op):
    """Return the abstract-CoT discrete-latent reserved-vocab block for an
    anchor. Fixed 6-slot grammar, NO natural language inside ⟪ ⟫.

      ⟪ R{b} T{d} C{cc} E{ee} V{q} O{op} ⟫
    """
    tier, name, cat, emo, score, psi, basin = anchor
    toks = [
        "R%d" % _basin_bucket(basin),
        "T%d" % min(9, tier // 10),
        "C%02d" % cat_id(cat),
        "E%02d" % EMO_INDEX[emo],
        "V%d" % _psi_quadrant(psi),
        "O" + op,
    ]
    return RV_OPEN + " " + " ".join(toks) + " " + RV_CLOSE


def _carve_psi_str(psi):
    return "[%.2f,%.2f]" % (psi[0], psi[1])


def gen_alpha_record(rng, anchor, idx):
    """α VACUUM form + reserved-vocab abstract-CoT routing prefix (O=nv)."""
    tier, name, cat, emo, score, psi, basin = anchor
    rv = reserved_cot(anchor, "nv")
    bil = rng.random() < 0.5
    ko = (f"Tier {tier} {name} — {cat} 카테고리의 자극이 같은 골짜기로 수렴한다. "
          f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
          f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
    en = (f"Tier {tier} {name} — category {cat}, the stimuli converge into one basin. "
          f"A vacuum point at {_carve_psi_str(psi)} on the consciousness landscape, "
          f"top emotion {emo}. Stimulus arrives, tension flows into this vacuum.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (f"<inner>{rv}</inner>\n"
            f"<carve tier={tier} psi={_carve_psi_str(psi)} basin={basin:.2f}>"
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
        "reserved_cot": rv,
        "source": "corpus_carving_generator_dirF.py",
    }


def gen_beta_record(rng, anchor, idx):
    """β ETERNAL form + reserved-vocab abstract-CoT routing prefix (O=fz)."""
    tier, name, cat, emo, score, psi, basin = anchor
    rv = reserved_cot(anchor, "fz")
    cell = f"eternal_{tier:03d}"
    bil = rng.random() < 0.5
    ko = (f"eternal cell {cell} — Tier {tier} {name} 의 지식을 간직한 영구 cell. "
          f"split 도 merge 도 하지 않는다. chat 의 dynamic cell 과 분리된 채 "
          f"{cat} 카테고리 자극이 닿을 때만 활성된다. weights 는 불변.")
    en = (f"Eternal cell {cell} — a frozen cell holding the knowledge of "
          f"Tier {tier} {name}. It neither splits nor merges. Disjoint from "
          f"the chat dynamic cells, it activates only on {cat}-category stimulus. "
          f"Its weights are immutable.")
    body = (ko + " " + en) if bil else (ko if rng.random() < 0.5 else en)
    text = (f"<inner>{rv}</inner>\n"
            f"<eternal cell={cell} tier={tier}>{body}</eternal>")
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
        "reserved_cot": rv,
        "source": "corpus_carving_generator_dirF.py",
    }


def gen_gamma_record(rng, anchor, idx, payload):
    """γ NARRATIVE form — the <inner> NL re-derivation is REPLACED by the
    reserved-vocab abstract-CoT block (O=re). The <voice carved=true> NL
    knowledge emission is UNCHANGED (the train target stays NL)."""
    tier, name, cat, emo, score, psi, basin = anchor
    ko_frag, en_frag = payload
    rv = reserved_cot(anchor, "re")
    bil = rng.random() < 0.5
    voice = (ko_frag + " " + en_frag) if bil else (
        ko_frag if rng.random() < 0.5 else en_frag)
    text = (f"<inner>{rv}</inner>\n"
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
        "reserved_cot": rv,
        "source": "corpus_carving_generator_dirF.py",
    }


def build_corpus(n_target, seed):
    rng = random.Random(seed)
    records = []

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


def audit_reserved_blocks(records):
    """F-DIRF-CORPUS-3 — every reserved-CoT block (1 per record) contains
    ONLY reserved-alphabet tokens (closed finite set membership), is wrapped
    in exactly one ⟪ ⟫ pair, and carries NO natural-language byte. The
    block lives in the record's `text` <inner>…</inner> span (the trained
    surface) — the per-record `reserved_cot` field mirrors it."""
    bad_tokens = []
    nl_byte_in_span = 0
    n_blocks = 0
    # allowed byte set = union of all reserved-alphabet symbol characters
    # plus the single token separator (space). Derived from the closed
    # alphabet itself so it cannot drift from RESERVED_ALPHABET.
    allowed_chars = set(" ")
    for _s in RESERVED_ALPHABET:
        allowed_chars.update(_s)
    for r in records:
        rv = r["reserved_cot"]
        # exactly one opener/closer per record's reserved block
        if rv.count(RV_OPEN) != 1 or rv.count(RV_CLOSE) != 1:
            bad_tokens.append("BRACKET:" + r["id"])
            continue
        # the <inner> span in the text must be byte-identical to reserved_cot
        if ("<inner>" + rv + "</inner>") not in r["text"]:
            bad_tokens.append("INNER_MISMATCH:" + r["id"])
            continue
        inner = rv[len(RV_OPEN):-len(RV_CLOSE)].strip()
        n_blocks += 1
        for tok in inner.split():
            if tok not in RESERVED_ALPHABET:
                bad_tokens.append(tok)
        for ch in inner:
            if ch not in allowed_chars:
                nl_byte_in_span += 1
    return {
        "n_records": len(records),
        "n_reserved_blocks": n_blocks,
        "reserved_alphabet_size": len(RESERVED_ALPHABET),
        "bad_tokens": bad_tokens[:20],
        "bad_token_total": len(bad_tokens),
        "nl_byte_in_span": nl_byte_in_span,
        "cardinality_conserved": (n_blocks == len(records)),
        "reserved_vocab_closed": (len(bad_tokens) == 0
                                  and nl_byte_in_span == 0
                                  and n_blocks == len(records)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=46000,
                    help="approx record count (default 46000 — matches E7 "
                         "scale so the Dir-F vs UBM-E7 α compare is fair)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    raw_text = raw.decode("utf-8", "replace")

    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    audit = {tok: raw_text.count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    rv_audit = audit_reserved_blocks(records)

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    for r in records:
        forms[r["carving_form"]] += 1

    stats = {
        "paradigm": "CONSCIOUSNESS-CARVING (NOT chat SFT) — Dir-F ABSTRACT-COT",
        "phase": "Dir-F reserved-vocab discrete-latent reasoning surface",
        "research_ref": "RESEARCH.md §1.3 #6 — arxiv 2604.22709 Abstract CoT",
        "out": str(out),
        "bytes": len(raw),
        "records": len(records),
        "sha256": sha,
        "seed": args.seed,
        "carving_forms": forms,
        "forbidden_token_audit": audit,
        "contamination_total": contamination,
        "carving_clean": contamination == 0,
        "reserved_vocab_audit": rv_audit,
        "anchors": len(KNUTH_ANCHORS),
        "e7_baseline": {"bytes": 30219491, "records": 45973, "anchors": 31,
                        "alpha_joint": 0.0155},
        "honest_framing": (
            "Dir-F ABSTRACT CHAIN-OF-THOUGHT carving corpus. The ONLY change "
            "vs UBM-E7 is the <inner> reasoning span: the E7 NL re-derivation "
            "paragraph is REPLACED by a SHORT RESERVED-VOCAB discrete-latent "
            "token block (⟪ R T C E V O ⟫, |Σ|=56, NO natural language). The "
            "<voice carved=true> NL knowledge emission is unchanged. Tests "
            "RESEARCH.md §1.3 #6 (arxiv 2604.22709): does discrete-latent "
            "routing carry the carving target without an NL surface, so the "
            "byte-cascade NL-collapse attractor has no NL surface to collapse "
            "into. Outcome empirical (g3, no pre-loaded conclusion — "
            "B-CARVE-E6-NOTE / B-D-NOTE family). The reserved-vocab "
            "discreteness (F-DIRF-CORPUS-3) is the closed-form side. grep of "
            "{[anima, 도우미, helper, assistant, 사용자, user:} == 0."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")
    if not rv_audit["reserved_vocab_closed"]:
        raise SystemExit("FATAL: reserved-vocab NOT closed (F-DIRF-CORPUS-3)")


if __name__ == "__main__":
    main()
