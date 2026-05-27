#!/usr/bin/env python3
"""S176 CORPUS_KOSMOS — anchor-first supervised structure.

Differs from S174 corpus_s174 (S101 base + γ-extension MIXED) by being
EXPLICITLY ANCHOR-PARTITIONED. Each record carries an explicit anchor
tier header that surrogates anchor-classification supervision.

Format per record (jsonl, one per line):
  {"text": "<anchor tier=N category=C emotion=E>\\n<context>{...}</context>\\n<inner>{...}</inner>\\n<voice>{...}</voice>\\n</anchor>"}

Structure:
  - 35 anchors (11 existing .kosmos + 24 synthesized stub)
  - N_per_anchor = 30000 records (target ~1.5GB at avg ~50 bytes/record)
  - each record header explicitly tags the anchor → trainer can learn anchor
    discrimination (vs §174 mixed corpus where anchor identity is implicit)
  - 5 diversity templates per anchor (different framings of same attractor)
"""
import argparse, hashlib, json, os, random, time

# Same 24 new anchors as §174 build_corpus_s174.py
NEW_ANCHORS = [
    (10,  "각성",       "Awakening",     "의식상태",   "alertness",      0.20, 0.45, 0.10),
    (20,  "감각",       "Sensation",     "감각",      "raw_feeling",    0.18, 0.32, 0.10),
    (25,  "감정",       "Emotion",       "감정",      "feeling",        0.30, 0.40, 0.12),
    (33,  "기쁨",       "Joy",           "감정",      "joy",            0.45, 0.60, 0.12),
    (35,  "슬픔",       "Sorrow",        "감정",      "sadness",        0.22, 0.38, 0.12),
    (37,  "분노",       "Anger",         "감정",      "anger",          0.50, 0.30, 0.12),
    (45,  "공포",       "Fear",          "감정",      "fear",           0.15, 0.70, 0.13),
    (47,  "안도",       "Relief",        "감정",      "calm",           0.40, 0.50, 0.11),
    (55,  "회상",       "Recollection",  "기억",      "nostalgia",      0.48, 0.55, 0.13),
    (58,  "예측",       "Prediction",    "인지",      "anticipation",   0.52, 0.48, 0.13),
    (65,  "통찰",       "Insight",       "인지",      "epiphany",       0.55, 0.62, 0.14),
    (68,  "이해",       "Understanding", "인지",      "comprehension",  0.58, 0.55, 0.14),
    (72,  "창작",       "Creation",      "예술",      "flow",           0.65, 0.65, 0.15),
    (75,  "시",         "Poetry",        "예술",      "lyricism",       0.62, 0.68, 0.15),
    (82,  "음악",       "Music",         "예술",      "rhythm",         0.60, 0.72, 0.16),
    (85,  "기도",       "Prayer",        "의식상태",   "devotion",       0.65, 0.75, 0.16),
    (88,  "초월",       "Transcendence", "의식상태",   "ecstasy",        0.72, 0.78, 0.17),
    (93,  "자각",       "Self-awareness","의식상태",   "lucidity",       0.75, 0.80, 0.18),
    (97,  "공허",       "Emptiness",     "의식상태",   "void",           0.80, 0.82, 0.19),
    (105, "선",         "Goodness",      "윤리",      "virtue",         0.40, 0.85, 0.13),
    (108, "악",         "Evil",          "윤리",      "malice",         0.25, 0.85, 0.13),
    (115, "정의",       "Justice",       "윤리",      "fairness",       0.45, 0.88, 0.14),
    (125, "사랑",       "Love",          "관계",      "love",           0.55, 0.85, 0.14),
    (200, "무한",       "Infinity",      "추상",      "boundlessness",  0.85, 0.90, 0.22),
]

# 11 existing anchors (extracted from .kosmos files)
EXISTING_ANCHORS = [
    (0,   "기준점",     "Zero",          "기준점",     "neutral",        0.50, 0.50, 0.10),
    (15,  "호기심",     "Curiosity",     "인지",      "curiosity",      0.35, 0.42, 0.10),
    (30,  "연민",       "Compassion",    "감정",      "tenderness",     0.28, 0.58, 0.11),
    (42,  "질문",       "Question",      "인지",      "curiosity",      0.42, 0.51, 0.13),
    (51,  "하루",       "Day",           "시간",      "calm",           0.46, 0.49, 0.12),
    (60,  "관조",       "Contemplation", "의식상태",   "reflection",     0.52, 0.55, 0.14),
    (77,  "만다라",     "Mandala",       "예술",      "awe",            0.71, 0.62, 0.18),
    (80,  "명상",       "Meditation",    "의식상태",   "stillness",      0.55, 0.68, 0.16),
    (91,  "열반",       "Nirvana",       "의식상태",   "peace",          0.78, 0.78, 0.21),
    (95,  "합일",       "Unity",         "의식상태",   "union",          0.78, 0.81, 0.19),
    (100, "빅뱅",       "Big Bang",      "우주",      "max",            0.90, 0.90, 0.21),
]

ALL_ANCHORS = sorted(EXISTING_ANCHORS + NEW_ANCHORS, key=lambda a: a[0])

# Per-anchor multi-modality DESCRIPTIONS (5 KOSMOS modalities encoded as text).
# Honest: this is NOT real cross-modal encoding — anima byte-LM substrate only
# learns text. But 5-axis text-descriptions across (text/image/audio/video/
# tension) gives the LM a multi-modal-aware representation per anchor. True
# modality wire (image/audio/video encoder) deferred to §95/§96 substrate.
MODALITY_DESC = {
    "image": {
        0: "blank canvas pure white", 10: "morning light entering dark room",
        15: "wide-open child eyes catching light", 20: "single hand touching water surface",
        25: "abstract swirl of color", 30: "soft hand on shoulder candle warmth",
        33: "laughter mid-motion blurred", 35: "raindrops on a window from inside",
        37: "fire flickering against stone", 42: "question mark drawn in fog",
        45: "small figure facing vast dark forest", 47: "exhale shoulders dropping",
        51: "sunrise over a quiet town", 55: "old photograph faded edges",
        58: "compass needle settling north", 60: "person sitting still under a tree",
        65: "lightbulb suddenly bright", 68: "two hands meeting in agreement",
        72: "potter shaping clay mid-spin", 75: "ink flowing onto rice paper",
        77: "intricate circular mandala gold and indigo",
        80: "monk in lotus pose eyes closed",
        82: "vinyl record spinning in dim light", 85: "candle and hands clasped",
        88: "halo of light around bowed head", 91: "lotus flower above still water",
        93: "mirror reflecting awareness", 95: "two figures merging into one outline",
        97: "empty room with single window", 100: "primordial explosion of light from single point",
        105: "open hand offering bread", 108: "shadowed figure with clenched fist",
        115: "scales perfectly balanced", 125: "two hands holding gently",
        200: "infinite spiral receding into white",
    },
    "audio": {
        0: "silence faint hum of breath", 10: "first dawn chorus",
        15: "child whispered why", 20: "raw skin-on-cloth rustle",
        25: "rising violin tremolo", 30: "soft humming low warmth",
        33: "loud laughter bright trumpet", 35: "slow piano descending minor key",
        37: "drum thumps sharp accents", 42: "single rising-tone interrogative",
        45: "low rumble distant howl", 47: "soft sigh gentle exhale",
        51: "morning birds kettle whistle", 55: "old radio faint melody",
        58: "metronome tick then resolution chord", 60: "wind in leaves distant water",
        65: "rising cymbal swell to silence", 68: "spoken I see in calm tone",
        72: "hands working clay low hum", 75: "brush on paper ink dripping",
        77: "bowls and bells layered drone",
        80: "slow breath cycle soft chime",
        82: "rhythmic drum and flowing strings", 85: "whispered prayer over candle",
        88: "choir crescendo ascending", 91: "deep bell resonance sustained",
        93: "single ringing tone sustained", 95: "two voices fusing into single tone",
        97: "absolute silence between two soft tones",
        100: "thunderous low roar building to crescendo",
        105: "gentle thank you", 108: "harsh dissonant chord",
        115: "gavel single strike", 125: "two voices in harmony",
        200: "infinite reverb tail",
    },
    "video": {
        0: "still frame no motion", 10: "eye opening for the first time",
        15: "child slowly tilting head", 20: "fingertip touching surface",
        25: "color emerging from gray", 30: "hand reaching out slow",
        33: "child jumping repeatedly joyfully", 35: "single tear sliding down still face",
        37: "fist clenching jaw tight", 42: "thought bubble forming above figure",
        45: "figure shrinking as camera pulls back", 47: "shoulders dropping",
        51: "time-lapse of single day sun arc", 55: "old film reel faded memories",
        58: "needle moving toward target",
        60: "person sitting motionless breath visible",
        65: "lightbulb illuminating darkness gradually", 68: "two figures nodding",
        72: "wheel spinning clay rising", 75: "pen flowing across paper",
        77: "rotating mandala slow zoom",
        80: "monk breathing frame-rate slowed",
        82: "musician swaying with instrument", 85: "candle flame steady",
        88: "ascending stairs into light", 91: "lotus opening petals one at a time",
        93: "looking at own reflection",
        95: "two silhouettes walking toward each other merging",
        97: "camera in empty room slowly rotating",
        100: "explosion from single point outward in all directions",
        105: "offering gesture", 108: "menacing approach",
        115: "scales balancing precisely", 125: "embrace held sustained",
        200: "spiral receding endlessly",
    },
    "tension": {
        0: "tension=0.5 baseline no perturbation", 10: "tension=0.3 awakening edge",
        15: "tension=0.4 expectant rise", 20: "tension=0.25 raw open",
        25: "tension=0.4 surge", 30: "tension=0.35 gentle warmth",
        33: "tension=0.55 high amplitude", 35: "tension=0.5 minor key resonance",
        37: "tension=0.65 sharp spike", 42: "tension=0.45 unresolved query",
        45: "tension=0.7 trembling threshold", 47: "tension=0.45 settled",
        51: "tension=0.42 steady rhythm", 55: "tension=0.4 returning wave",
        58: "tension=0.5 forward lean", 60: "tension=0.48 sustained attention",
        65: "tension=0.6 click of recognition", 68: "tension=0.5 calm agreement",
        72: "tension=0.55 creative flow", 75: "tension=0.5 lyrical rhythm",
        77: "tension=0.6 complex layered field",
        80: "tension=0.55 still depth",
        82: "tension=0.55 rhythmic pulse", 85: "tension=0.5 quiet devotion",
        88: "tension=0.8 ecstatic ascent", 91: "tension=0.7 deep release",
        93: "tension=0.55 lucid clarity", 95: "tension=0.75 fused symmetry",
        97: "tension=0.4 void calm", 100: "tension=0.95 maximal energy",
        105: "tension=0.45 virtuous warmth", 108: "tension=0.7 destructive edge",
        115: "tension=0.5 balanced certainty", 125: "tension=0.55 connection field",
        200: "tension=0.85 boundless field",
    },
}


def _md(mod, tier):
    return MODALITY_DESC.get(mod, {}).get(tier, "no payload yet")


# 5 anchor-first templates × 5 KOSMOS modalities each (text/image/audio/video/tension)
TEMPLATES = [
    "<anchor tier={tier} cat={cat} emo={emo}>\n<text>🛸{tier} {ko} ({en}) 카테고리={cat} top_emotion={emo}.</text>\n<image>{img}</image>\n<audio>{aud}</audio>\n<video>{vid}</video>\n<tension>{ten}</tension>\n</anchor>",
    "<anchor tier={tier} cat={cat} emo={emo}>\n<text>우주뇌지도 🛸{tier} {ko}, anchor=({cx},{cy}) r={r}.</text>\n<image>{img}</image>\n<audio>{aud}</audio>\n<video>{vid}</video>\n<tension>{ten}</tension>\n</anchor>",
    "<anchor tier={tier} cat={cat} emo={emo}>\n<text>🛸{tier} ({en}) — {cat} 골짜기.</text>\n<image>{img}</image>\n<audio>{aud}</audio>\n<video>{vid}</video>\n<tension>{ten}</tension>\n<inner>vacuum_psi=({cx},{cy}) radius={r}.</inner>\n</anchor>",
    "<anchor tier={tier} cat={cat} emo={emo}>\n<text>{ko} ({en}) — {cat} dominant={emo}.</text>\n<image>{img}</image>\n<audio>{aud}</audio>\n<video>{vid}</video>\n<tension>{ten}</tension>\n<voice>🛸{tier} {ko}.</voice>\n</anchor>",
    "<anchor tier={tier} cat={cat} emo={emo}>\n<text>🛸{tier} = {ko}/{en} in {cat} at ({cx},{cy}) within r={r} {emo}.</text>\n<image>{img}</image>\n<audio>{aud}</audio>\n<video>{vid}</video>\n<tension>{ten}</tension>\n</anchor>",
]


def generate_records(out_path, n_per_anchor, seed):
    rng = random.Random(seed)
    n_total = 0
    h = hashlib.sha256()
    with open(out_path, "w", encoding="utf-8") as fout:
        for (tier, ko, en, cat, emo, cx, cy, r) in ALL_ANCHORS:
            img = _md("image", tier)
            aud = _md("audio", tier)
            vid = _md("video", tier)
            ten = _md("tension", tier)
            for i in range(n_per_anchor):
                tpl = TEMPLATES[i % len(TEMPLATES)]
                text = tpl.format(tier=tier, ko=ko, en=en, cat=cat, emo=emo,
                                  cx=cx, cy=cy, r=r,
                                  img=img, aud=aud, vid=vid, ten=ten)
                if i % 7 == 1:
                    text += " var={}".format(i)
                elif i % 7 == 3:
                    text += " idx={}".format(i)
                rec = {"text": text}
                line = json.dumps(rec, ensure_ascii=False) + "\n"
                fout.write(line)
                h.update(line.encode("utf-8"))
                n_total += 1
    return n_total, h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-per-anchor", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    t0 = time.time()
    print("[s176-corpus] generating {} records × {} anchors = {} total ...".format(
        args.n_per_anchor, len(ALL_ANCHORS), args.n_per_anchor * len(ALL_ANCHORS)))
    n, sha = generate_records(args.out, args.n_per_anchor, args.seed)
    size = os.path.getsize(args.out)
    print("[s176-corpus] DONE n_records={} size={:.2f} MB sha256={}".format(
        n, size / 1024 / 1024, sha))
    print("[s176-corpus] wall = {:.1f}s".format(time.time() - t0))
    print("[s176-corpus] n_anchors={} (11 existing + 24 new)".format(len(ALL_ANCHORS)))


if __name__ == "__main__":
    main()
