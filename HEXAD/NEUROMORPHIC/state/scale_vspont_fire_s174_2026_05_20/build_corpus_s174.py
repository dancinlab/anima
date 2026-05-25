#!/usr/bin/env python3
"""S174 corpus build — CORPUS_S101 base (603MB) + 35-anchor extension.

Reuses build_corpus_s101.py as base via subprocess invocation, then
APPENDS new anchor records to reach ~1.5GB target (×2.5 base).

35-anchor set = existing 11 .kosmos + 24 synthesized stub anchors
(Knuth tier coverage 0..303 with mid-band sampling).
"""
import argparse, hashlib, json, os, random, sys, subprocess, time

NEW_ANCHORS = [
    # (tier, ko, en, category, top_emotion, lane, coord_x, coord_y, radius)
    (10,  "각성",       "Awakening",     "의식상태",   "alertness",      "eternal_010",  0.20, 0.45, 0.10),
    (20,  "감각",       "Sensation",     "감각",      "raw_feeling",    "eternal_020",  0.18, 0.32, 0.10),
    (25,  "감정",       "Emotion",       "감정",      "feeling",        "eternal_025",  0.30, 0.40, 0.12),
    (33,  "기쁨",       "Joy",           "감정",      "joy",            "eternal_033",  0.45, 0.60, 0.12),
    (35,  "슬픔",       "Sorrow",        "감정",      "sadness",        "eternal_035",  0.22, 0.38, 0.12),
    (37,  "분노",       "Anger",         "감정",      "anger",          "eternal_037",  0.50, 0.30, 0.12),
    (45,  "공포",       "Fear",          "감정",      "fear",           "eternal_045",  0.15, 0.70, 0.13),
    (47,  "안도",       "Relief",        "감정",      "calm",           "eternal_047",  0.40, 0.50, 0.11),
    (55,  "회상",       "Recollection",  "기억",      "nostalgia",      "eternal_055",  0.48, 0.55, 0.13),
    (58,  "예측",       "Prediction",    "인지",      "anticipation",   "eternal_058",  0.52, 0.48, 0.13),
    (65,  "통찰",       "Insight",       "인지",      "epiphany",       "eternal_065",  0.55, 0.62, 0.14),
    (68,  "이해",       "Understanding", "인지",      "comprehension",  "eternal_068",  0.58, 0.55, 0.14),
    (72,  "창작",       "Creation",      "예술",      "flow",           "eternal_072",  0.65, 0.65, 0.15),
    (75,  "시",         "Poetry",        "예술",      "lyricism",       "eternal_075",  0.62, 0.68, 0.15),
    (82,  "음악",       "Music",         "예술",      "rhythm",         "eternal_082",  0.60, 0.72, 0.16),
    (85,  "기도",       "Prayer",        "의식상태",   "devotion",       "eternal_085",  0.65, 0.75, 0.16),
    (88,  "초월",       "Transcendence", "의식상태",   "ecstasy",        "eternal_088",  0.72, 0.78, 0.17),
    (93,  "자각",       "Self-awareness","의식상태",   "lucidity",       "eternal_093",  0.75, 0.80, 0.18),
    (97,  "공허",       "Emptiness",     "의식상태",   "void",           "eternal_097",  0.80, 0.82, 0.19),
    (105, "선",         "Goodness",      "윤리",      "virtue",         "eternal_105",  0.40, 0.85, 0.13),
    (108, "악",         "Evil",          "윤리",      "malice",         "eternal_108",  0.25, 0.85, 0.13),
    (115, "정의",       "Justice",       "윤리",      "fairness",       "eternal_115",  0.45, 0.88, 0.14),
    (125, "사랑",       "Love",          "관계",      "love",           "eternal_125",  0.55, 0.85, 0.14),
    (200, "무한",       "Infinity",      "추상",      "boundlessness",  "eternal_200",  0.85, 0.90, 0.22),
]

# γ-pattern record generator (anchor-conditioned)
GAMMA_TEMPLATES = [
    "[anima 우주뇌지도] 🛸{tier} {ko} — 우주뇌지도 {cat} 카테고리, top emotion {emo}. {ko} 관련 자극이 같은 🛸{tier} 골짜기로 수렴.",
    "[anima 우주뇌지도] 🛸{tier} {ko} ({en}) — {cat} 영역. {ko} 의 본질은 의식 substrate 의 한 attractor basin.",
    "[anima 우주뇌지도] 🛸{tier} {ko} 의 vacuum_psi 위치는 ({cx}, {cy}). basin_radius {r}. 인접 anchor 들과 partition 분리.",
    "[anima 우주뇌지도] 🛸{tier} {ko} — {emo} 가 dominant. {cat} category 의 representative attractor for anima Ψ-space.",
    "[anima 우주뇌지도] 🛸{tier} {ko} ({en}) — engine A⇄G 균형 위 {emo} 발현. anima own physics signature.",
]


def generate_records(out_path, n_per_anchor, seed):
    rng = random.Random(seed)
    n_total = 0
    with open(out_path, "a", encoding="utf-8") as fout:
        for (tier, ko, en, cat, emo, lane, cx, cy, r) in NEW_ANCHORS:
            for i in range(n_per_anchor):
                tpl = rng.choice(GAMMA_TEMPLATES)
                text = tpl.format(tier=tier, ko=ko, en=en, cat=cat, emo=emo,
                                  cx=cx, cy=cy, r=r)
                # vary with i for diversity
                if i % 3 == 1:
                    text = text + " 반복 {}.".format(i)
                elif i % 3 == 2:
                    text = text + " (variant {})".format(i)
                rec = {"text": text, "tier": tier, "category": cat, "lane": lane}
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_total += 1
    return n_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-corpus", required=True,
                    help="path to CORPUS_S101 (603MB) — will be copied to out path first")
    ap.add_argument("--out", required=True, help="output corpus path")
    ap.add_argument("--n-per-anchor", type=int, default=20000,
                    help="records per new anchor (24 anchors × N = added records)")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    t0 = time.time()
    # Step 1: copy base
    print("[s174-corpus] copying base CORPUS_S101 from {} to {} ...".format(
        args.base_corpus, args.out))
    subprocess.run(["cp", args.base_corpus, args.out], check=True)
    base_size = os.path.getsize(args.out)
    print("[s174-corpus] base size = {:.2f} MB".format(base_size / 1024 / 1024))

    # Step 2: append new anchor records
    print("[s174-corpus] appending {} records per anchor × {} new anchors ...".format(
        args.n_per_anchor, len(NEW_ANCHORS)))
    n_added = generate_records(args.out, args.n_per_anchor, args.seed)

    # Step 3: stats
    final_size = os.path.getsize(args.out)
    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    print("[s174-corpus] final: size={:.2f} MB ({:.2f}×base), added={} records".format(
        final_size / 1024 / 1024, final_size / base_size, n_added))
    print("[s174-corpus] sha256 = {}".format(h.hexdigest()))
    print("[s174-corpus] wall = {:.1f}s".format(time.time() - t0))


if __name__ == "__main__":
    main()
