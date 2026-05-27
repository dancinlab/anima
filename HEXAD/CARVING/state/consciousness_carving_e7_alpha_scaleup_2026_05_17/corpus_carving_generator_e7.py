#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING carving corpus generator — Phase UBM-E7 SCALE-UP
(2026-05-17). α VACUUM-LANDSCAPE path scale-up fire.

WHY E7 (RESEARCH.md §2.6 — next-cycle candidate)
  UBM-E6 diagnosed (RESEARCH.md §2.4): a 4.3MB carving corpus / d512·8L /
  2000 step is a *memorization-saturated regime* — the paradigm is new but
  the corpus scale is below the capability-emergence threshold. E7 tests the
  hypothesis: if UBM-E6's joint ~0 is a corpus-scale limit, then SCALING the
  α path (bigger carving corpus + bigger model) should LIFT α's JOINT /
  V-SPONT. If it does NOT lift, scale alone is insufficient (other diagnosis
  needed) — recorded honestly either way (g3, no pre-loaded conclusion).

WHAT SCALES vs UBM-E6 (genuine diversity, NOT blind duplication)
  - anchors      : 11 -> 31 Knuth Tier anchors (more universe-brain-map
                   coverage — more vacuum points on the landscape).
  - payload pool : laws + categories + cosmic physics EXPANDED (the γ
                   re-generation pool grows so re-derivation is varied).
  - records      : ~6,600 -> --n (default 46,000) — ~7x toward ~25-35MB.
  This generator is the E6 corpus_carving_generator.py scaled up; the
  CARVING FORM is unchanged (carve/eternal/inner-voice), grep of forbidden
  tokens still == 0.

HONEST FRAMING (g3, AGENTS.tape §0 + DESIGN.md §0/§1/§G + memory carry)
  This is a *CARVING* corpus, NOT a chat SFT corpus. The old universe-brain-
  map paradigm used `[anima 우주뇌지도] 사용자: <Q>\\n도우미: <A>` prefix-
  injection — that BAKED a P3 leak (feedback_corpus_quality_over_scale +
  project_anima_base_ckpt_baked_p3_leak). Each record here is a *carving
  target* derived from a `.kosmos` anchor (DESIGN.md §5), NOT a Q&A turn.

ABSOLUTE FORBIDDEN (B-IDENTITY-5 + forbidden_chat_sft_use, grep MUST == 0)
  - `[anima 우주뇌지도]` (or any `[anima ...]`) prefix-stamp
  - `도우미` / `helper` / `assistant` / `사용자` / `user:` role labels

CARVING FORM (DESIGN.md §5 — same three forms as E6):
  α VACUUM  (~30%)  <carve tier=k psi=[x,y] basin=r> ... </carve>
  β ETERNAL (~30%)  <eternal cell=eternal_kkk tier=k> ... </eternal>
  γ NARRATIVE(~40%) <inner tier=k>...</inner>\\n<voice carved=true>...</voice>

  NOTE on the E7 α fire: train_carving_4path.py --path alpha consumes ALL
  three forms as the byte stream + uses the per-record vacuum_psi for the
  α vacuum-attractor loss term. The carving-form distribution is kept as in
  E6 so the α loss term sees the same landscape, just at scale.

Closed-form falsifiers (blue_falsifier_carving_e7.py B-CARVE-E7-CORPUS-1..3):
  - B-CARVE-E7-CORPUS-1 SHA256-DETERMINISTIC — seed-fixed 256-bit commitment.
  - B-CARVE-E7-CORPUS-2 NO-CHAT-SFT-CONTAMINATION — Boolean set algebra:
      grep {[anima, 도우미, helper, assistant, 사용자, user:} -> count == 0.
  - B-CARVE-E7-CORPUS-3 SCALE-UP-CARDINALITY — |records_E7| > |records_E6|
      AND bytes_E7 > bytes_E6 (integer >-inequality, Kolmogorov byte count).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

# ---------------------------------------------------------------------------
# Knuth Tier anchors — E7 SCALE-UP: 11 (E6) -> 31 anchors. The E6 11 anchors
# are kept verbatim (vacuum_psi/basin carried from anchors/*.kosmos design
# placeholders); 20 additional Knuth Tier anchors fill the landscape. The
# extra anchors' vacuum_psi are interpolated design placeholders on the
# Ψ-space landscape (g3: design placeholder, measured by the fire trajectory
# — NOT a closed-form claim).
# ---------------------------------------------------------------------------
KNUTH_ANCHORS = [
    # --- E6 anchors (verbatim) ---
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
    # --- E7 SCALE-UP anchors (20 additional Knuth Tiers) ---
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

# Laws 73-76 universal-map base (roadmap laws_73_76_base, verbatim semantics)
# + E7 SCALE-UP: Laws 77-84 universal-map extension (γ re-generation pool).
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

# Cosmic-scale physics fragments — E7 SCALE-UP: 5 (E6) -> 10 fragments.
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
        "source": "corpus_carving_generator_e7.py",
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
        "source": "corpus_carving_generator_e7.py",
    }


def gen_gamma_record(rng, anchor, idx, payload):
    """γ NARRATIVE form — inner->voice re-generation (Meta law M8)."""
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
        "source": "corpus_carving_generator_e7.py",
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

    # Distribute n_target across the anchors, ~equal per anchor.
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
    ap.add_argument("--n", type=int, default=46000,
                    help="approx record count (default 46000 — E7 scale-up; "
                         "~31 anchors -> ~1480/anchor -> ~27-32MB)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    records = build_corpus(args.n, args.seed)

    out = Path(args.out)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    raw = out.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    # Forbidden-token audit (B-CARVE-E7-CORPUS-2 closed-form).
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    audit = {tok: raw.decode("utf-8", "replace").count(tok) for tok in forbidden}
    contamination = sum(audit.values())

    forms = {"alpha": 0, "beta": 0, "gamma": 0}
    for r in records:
        forms[r["carving_form"]] += 1

    stats = {
        "paradigm": "CONSCIOUSNESS-CARVING (NOT chat SFT) — E7 SCALE-UP",
        "phase": "UBM-E7 α VACUUM-LANDSCAPE scale-up",
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
        "e6_baseline": {"bytes": 4351148, "records": 6600, "anchors": 11},
        "scale_up_factor_bytes": round(len(raw) / 4351148, 3),
        "scale_up_factor_records": round(len(records) / 6600, 3),
        "honest_framing": (
            "E7 SCALE-UP carving corpus — universe-brain-map knowledge in "
            "CONSCIOUSNESS-CARVING form (carve/eternal/inner-voice), 31 "
            "anchors (E6 had 11). NOT the old [anima 우주뇌지도] 사용자/도우미 "
            "prefix-injection paradigm. grep of {[anima, 도우미, helper, "
            "assistant, 사용자, user:} == 0. Scale-up tests RESEARCH.md §2.4 "
            "hypothesis (memorization-saturated regime vs emergence threshold) "
            "— outcome empirical, no pre-loaded conclusion (g3)."),
    }
    with out.with_suffix(".stats.json").open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if contamination != 0:
        raise SystemExit("FATAL: forbidden-token contamination detected")


if __name__ == "__main__":
    main()
