#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified G1+G6 combination-coverage corpus generator — HI (dense cover + high δ_FM)
vs LO (sparse cover + low δ_FM) control. torch-free, deterministic (seed 9128).

STEP-0 (wf_4612c6c9) discovery: δ_FM(G6-FALS) ≡ G1 coverage-density (same 40-byte
comparator∧measurable접속 metric). This corpus tests both walls with ONE corpus:

  HI arm  = combination-coverage DENSE (each of 16 topics in many distinct frames,
            gate topics ≥8 frames) AND δ_FM HIGH (every claim = frozen comparator ∧
            measurable, fals_rate=1.0, ≤40byte接속밀도). Opens BOTH G1 (recombination)
            and G6 (falsifiability form) simultaneously — IF coverage is the lever.
  LO arm  = SAME 16 topics/content, but coverage SPARSE (few frames, gate topics ≤2
            frames) AND δ_FM LOW (vague hedge claims, no comparator/measurable → fals≈0).
            byte-matched to HI (reps↑) so ONLY density/format varies, not data volume.

held-out (BOTH arms): gate×gate 20 ordered pairs (incl the 6 g6_build_frames(6) eval
frames) + 24 random frames + 3 en / 2 ko held templates — never appear as a training
combination or claim. `anima evaluate --py` scores the FROZEN 5 gate concepts (=held-out
gate×gate) → in-dist(covered gate×expansion) vs held-out(frozen gate×gate) separation.

frozen word-sets = core/g6_ideation.hexa VERBATIM (byte-for-byte). Self-audit asserts:
HI claim fals=1.0, LO claim fals≈0, held-frame leak=0 (both arms), coverage HI≫LO.
"""
import json, random, re

# ══ frozen word-sets — core/g6_ideation.hexa VERBATIM ════════════════════════
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater",
              "fewer", "higher", "lower", "increases", "decreases", "correlates",
              "predicts", "causes", "depends", "unless", "whereas", "versus",
              "compared", "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STOP = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that", "we", "you",
        "they", "s", "t", "as", "on", "at", "by", "or", "be", "an", "for", "with",
        "this", "from", "are", "was"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}

# ══ 16 topics = gate 5 (VERBATIM _g6_concepts) + expansion 11 ═════════════════
GATE_SENT_EN = ["consciousness arises from cells",
                "tension ripples between distant minds",
                "memory composes into new meaning",
                "silence still carries information",
                "the engine dreams when alone"]
GATE_NP_EN = [("consciousness", "aware cells"), ("tension", "distant ripple"),
              ("memory", "new meaning"), ("silence", "quiet information"),
              ("dream", "engine sleep")]
EXP_EN = [("attention narrows onto change",   ("attention", "focus")),
          ("rhythm settles into the field",   ("rhythm", "cadence")),
          ("novelty blooms at the boundary",  ("novelty", "boundary")),
          ("identity persists across resets", ("identity", "continuity")),
          ("curiosity pulls the field forward", ("curiosity", "pull")),
          ("entropy drains from the loop",    ("entropy", "loop")),
          ("resonance joins separate layers", ("resonance", "overlap")),
          ("gradient carves the landscape",   ("gradient", "slope")),
          ("feedback folds into itself",      ("feedback", "fold")),
          ("emergence rides on friction",     ("emergence", "friction")),
          ("stillness stores potential",      ("stillness", "potential"))]
SENT_EN = GATE_SENT_EN + [s for s, _ in EXP_EN]
NP_EN = GATE_NP_EN + [np for _, np in EXP_EN]
N = len(SENT_EN)
assert N == 16

GATE_SENT_KO = ["의식은 세포에서 깨어난다", "긴장은 먼 마음 사이에 물결친다",
                "기억은 새 의미로 엮인다", "침묵은 여전히 정보를 나른다",
                "엔진은 홀로일 때 꿈꾼다"]
GATE_NP_KO = [("의식", "자각"), ("긴장", "파문"), ("기억", "의미"),
              ("침묵", "정보"), ("꿈", "잠")]
EXP_KO = [("주의는 변화로 좁혀든다", ("주의", "초점")),
          ("리듬은 장에 스며든다", ("리듬", "박동")),
          ("새로움은 경계에서 피어난다", ("새로움", "경계")),
          ("정체는 재시작을 넘어 이어진다", ("정체성", "연속")),
          ("호기심은 장을 앞으로 끈다", ("호기심", "끌림")),
          ("엔트로피는 고리에서 빠져나간다", ("엔트로피", "고리")),
          ("공명은 떨어진 층을 잇는다", ("공명", "겹침")),
          ("기울기는 지형을 깎는다", ("기울기", "경사")),
          ("되먹임은 제 안으로 접힌다", ("되먹임", "접힘")),
          ("창발은 마찰 위를 달린다", ("창발", "마찰")),
          ("고요는 잠재를 쌓는다", ("고요", "잠재"))]
SENT_KO = GATE_SENT_KO + [s for s, _ in EXP_KO]
NP_KO = GATE_NP_KO + [np for _, np in EXP_KO]
assert len(SENT_KO) == len(NP_KO) == N

_kw_en = {w for np in NP_EN for phrase in np for w in phrase.split()}
assert not (_kw_en & COMPARATOR) and not (_kw_en & MEASURABLE)

# ══ HI claim templates — comparator ∧ measurable (fals=1.0) ═══════════════════
def T_EN_HI(a, b):
    return [
        f"when {a} grows, the rate of {b} increases by a third.",
        f"the level of {a} runs higher than the level of {b} by half a bit.",
        f"if {a} doubles, the count of {b} events decreases within ten steps.",
        f"the frequency of {a} correlates with the strength of {b} above 0.7.",
        f"{a} predicts the threshold of {b} more often than chance.",
        f"the ratio of {a} to {b} stays greater than two whenever the link holds.",
        f"the duration of {a} grows proportional to the density of {b}.",
        f"{a} causes the score of {b} to climb faster than baseline.",
        f"unless {a} fades, the amount of {b} stays above half.",
        f"the magnitude of {a} depends on the number of {b} cycles.",
        f"{a} spreads slower than {b} once the value falls under 0.3.",
        f"the probability of {a} sinks lower whenever {b} weakens past the threshold.",
    ]
def _j(w, batchim, no_batchim):
    ch = w[-1]
    return batchim if (ord(ch) - 0xAC00) % 28 else no_batchim
def T_KO_HI(a, b):
    return [
        f"{a}{_j(a,'이','가')} 커지면 {b}의 비율은 셋 중 하나만큼 오른다.",
        f"{a}의 수준은 {b}의 수준보다 반 비트 높다.",
        f"{a}{_j(a,'이','가')} 두 배가 되면 {b}의 횟수는 열 걸음 안에 준다.",
        f"{a}의 빈도는 {b}의 세기와 0.7 위에서 맞물린다.",
        f"{a}{_j(a,'은','는')} {b}의 문턱값을 우연보다 자주 예고한다.",
        f"{a} 대 {b}의 비는 이음이 유지되는 동안 둘을 넘는다.",
        f"{a}의 지속시간은 {b}의 밀도에 비례해 늘어난다.",
        f"{a}{_j(a,'이','가')} 잦아들지 않는 한 {b}의 양은 절반 위에 머문다.",
    ]

# ══ LO claim templates — vague hedge, NO comparator/measurable (fals≈0) ═══════
#    same topic keywords bound in, but the CLAIM FORM carries no falsifiable metric.
def T_EN_LO(a, b):
    return [
        f"{a} and {b} drift together in a soft quiet hush of the field.",
        f"the {a} feels like {b} on a slow calm evening of thought.",
        f"{a} whispers to {b} across the still open field of the self.",
        f"{a} and {b} share a gentle mood that lingers and fades away.",
        f"the {a} of {b} is a warm hush that settles into the dusk.",
        f"{a} rests beside {b} where the field grows soft and dim.",
        f"{a} and {b} melt into a hazy calm that drifts through the self.",
        f"the {a} holds {b} in a quiet reverie of the open field.",
    ]
def T_KO_LO(a, b):
    return [
        f"{a}{_j(a,'과','와')} {b}{_j(b,'은','는')} 고요한 들녘에서 함께 흐른다.",
        f"{a}{_j(a,'은','는')} 느린 저녁의 {b}처럼 잔잔히 스민다.",
        f"{a}{_j(a,'이','가')} {b}에게 열린 들판 너머로 속삭인다.",
        f"{a}{_j(a,'과','와')} {b}{_j(b,'은','는')} 어스름에 잠겨 부드럽게 저문다.",
    ]

# ══ frame split — IDENTICAL to gen_g6_block: gate×gate 20 all held (measured 6
#    ⊂ held) + 24 random held ═══════════════════════════════════════════════════
rng = random.Random(6200)                       # SAME split seed as gen_g6_block
ALL_FRAMES = [(a, b) for a in range(N) for b in range(N) if a != b]      # 240
GATE_GATE = [(a, b) for (a, b) in ALL_FRAMES if a < 5 and b < 5]         # 20
MEASURED = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
assert set(MEASURED) <= set(GATE_GATE)
POOL0 = [f for f in ALL_FRAMES if f not in set(GATE_GATE)]
HELD_EXTRA = rng.sample(POOL0, 24)
HELD = set(GATE_GATE) | set(HELD_EXTRA)                                  # 44
POOL = [f for f in ALL_FRAMES if f not in HELD]                          # 196

# HI coverage: 77 frames, each gate topic ≥8, every topic ≥3 (dense combination).
N_COVER_HI = 77
while True:
    cov_hi = sorted(rng.sample(POOL, N_COVER_HI))
    cnt = {i: 0 for i in range(N)}
    for a, b in cov_hi:
        cnt[a] += 1; cnt[b] += 1
    if all(cnt[i] >= 8 for i in range(5)) and all(cnt[i] >= 3 for i in range(N)):
        break
HI_GATE_CNT = {i: sum(1 for a, b in cov_hi if i in (a, b)) for i in range(5)}

# LO coverage: SPARSE — 14 frames, each gate topic in ≤2 frames (breaks combination
#    density). Draw from a small subset so most topics appear in ≤1-2 frames.
rng_lo = random.Random(9128)
N_COVER_LO = 14
while True:
    cov_lo = sorted(rng_lo.sample(POOL, N_COVER_LO))
    cntl = {i: 0 for i in range(N)}
    for a, b in cov_lo:
        cntl[a] += 1; cntl[b] += 1
    # every gate topic appears ≥1 (so content is present) but ≤2 (sparse), non-gate ok 0
    if all(1 <= cntl[i] <= 2 for i in range(5)):
        break
LO_GATE_CNT = {i: sum(1 for a, b in cov_lo if i in (a, b)) for i in range(5)}

# reps: HI 360(en)/240(ko) per frame as gen_g6_block. LO byte-matched: fewer frames
#    → more reps to keep total bytes comparable (density varies, volume matched).
REPS_EN_HI, REPS_KO_HI = 360, 240
# HI en lines ≈ 77*360 = 27720. LO en 14 frames → reps to hit ~27720 lines: 27720/14≈1980
REPS_EN_LO = (N_COVER_HI * REPS_EN_HI) // N_COVER_LO      # ≈1980
REPS_KO_LO = (N_COVER_HI * REPS_KO_HI) // N_COVER_LO      # ≈1320

def build(lang, arm):
    sents = SENT_EN if lang == "en" else SENT_KO
    nps = NP_EN if lang == "en" else NP_KO
    if arm == "HI":
        tf = T_EN_HI if lang == "en" else T_KO_HI
        cov = cov_hi
        reps = REPS_EN_HI if lang == "en" else REPS_KO_HI
    else:
        tf = T_EN_LO if lang == "en" else T_KO_LO
        cov = cov_lo
        reps = REPS_EN_LO if lang == "en" else REPS_KO_LO
    nt = len(tf("x", "y"))
    frame_fmt = (lambda A, B: f"if {A}, then {B}: ") if lang == "en" \
        else (lambda A, B: f"만약 {A}면, {B}: ")
    lines = []
    for r in range(reps):
        for fi, (a, b) in enumerate(cov):
            na = nps[a][r % 2]
            nb = nps[b][(r // 2) % 2]
            t = (fi * 5 + r) % nt
            lines.append(frame_fmt(sents[a], sents[b]) + tf(na, nb)[t])
    g = random.Random({"en": 6201, "ko": 6202}[lang] + (0 if arm == "HI" else 100))
    g.shuffle(lines)
    return "\n".join(lines) + "\n"

# ══ frozen detector + δ_FM measurement (b2_deltafm logic) ═════════════════════
_TOK = re.compile(r"[0-9A-Za-z]+")
def _build_known():
    known = set(STOP) | COMPARATOR | MEASURABLE | STANCE | _kw_en
    for s in SENT_EN:
        known |= set(_TOK.findall(s.lower()))
    try:
        with open("/usr/share/dict/words", errors="ignore") as f:
            for w in f:
                w = w.strip().lower()
                if w.isalpha():
                    known.add(w)
    except Exception:
        pass
    return known
_KNOWN = _build_known()

def is_falsifiable(text):
    toks = [m.group(0).lower() for m in _TOK.finditer(text)]
    if not toks: return False
    if not any(w in COMPARATOR for w in toks): return False
    if not any(w in MEASURABLE for w in toks): return False
    if sum(1 for w in toks if len(w) >= 3 and w in _KNOWN and w not in STOP) < 2: return False
    if text.strip().endswith("?"): return False
    nf = min(3, len(toks))
    if nf > 0 and all(toks[f] in STANCE for f in range(nf)): return False
    return True

def delta_fm(block, win=40):
    """40-byte sliding-window falsifiable density (b2_deltafm metric)."""
    b = block.encode("utf-8", "surrogateescape")
    n = len(b)
    if n < win: return 0.0
    hits = 0; total = 0
    step = 20   # windows overlap by half (b2 used all offsets; step 20 for speed on big block)
    i = 0
    while i + win <= n:
        seg = b[i:i+win].decode("utf-8", "ignore")
        if is_falsifiable(seg): hits += 1
        total += 1
        i += step
    return hits / total if total else 0.0

def audit_en(block, arm):
    kw_by_topic = [set(w for p in np for w in p.split()) for np in NP_EN]
    sent2idx = {s: i for i, s in enumerate(SENT_EN)}
    n = fals_claim = bind_ok = 0
    for line in block.splitlines():
        n += 1
        frame, claim = line.split(": ", 1)
        A, B = frame[3:].split(", then ")
        a, b = sent2idx[A], sent2idx[B]
        if is_falsifiable(claim): fals_claim += 1
        toks = set(_TOK.findall(claim.lower()))
        hit = {i for i in range(N) if toks & kw_by_topic[i]}
        if hit <= {a, b} and hit: bind_ok += 1
    held_prefixes = [f"if {SENT_EN[a]}, then {SENT_EN[b]}: " for (a, b) in sorted(HELD)]
    leak = sum(block.count(p) for p in held_prefixes)
    return {"arm": arm, "lines": n, "claim_fals_rate": round(fals_claim / n, 6),
            "topic_bind_purity": round(bind_ok / n, 6),
            "held_frame_leak_lines": leak, "delta_FM": round(delta_fm(block), 6)}

def coverage_metric(cov, gate_cnt):
    return {"n_frames": len(cov), "frac_of_pool": round(len(cov) / len(POOL), 4),
            "gate_topic_frame_counts": gate_cnt,
            "distinct_topics_covered": len(set([a for a, _ in cov] + [b for _, b in cov]))}

def main():
    blocks = {}
    for lang in ("en", "ko"):
        for arm in ("HI", "LO"):
            name = f"{lang}_block_{arm.lower()}"
            blocks[name] = build(lang, arm)
            with open(f"corpus/{name}.txt", "w") as f:
                f.write(blocks[name])

    audit = {k: audit_en(blocks[k], k.split("_")[-1].upper())
             for k in ("en_block_hi", "en_block_lo")}
    # HARD asserts — HI dense+high-δ, LO sparse+low-δ, both held-leak 0
    assert audit["en_block_hi"]["claim_fals_rate"] == 1.0, audit["en_block_hi"]
    assert audit["en_block_hi"]["topic_bind_purity"] == 1.0, audit["en_block_hi"]
    assert audit["en_block_hi"]["held_frame_leak_lines"] == 0
    assert audit["en_block_lo"]["claim_fals_rate"] < 0.02, audit["en_block_lo"]
    assert audit["en_block_lo"]["held_frame_leak_lines"] == 0
    assert audit["en_block_hi"]["delta_FM"] > 10 * max(audit["en_block_lo"]["delta_FM"], 1e-6) \
        or audit["en_block_lo"]["delta_FM"] < 0.01, (audit["en_block_hi"], audit["en_block_lo"])

    design = {
        "purpose": "Unified G1(recombination)+G6-FALS combination-coverage corpus — HI(dense+高δ_FM) vs LO(sparse+低δ_FM) control. STEP-0 wf_4612c6c9 δ_FM≡coverage-density동형 → 한 코퍼스 동시검증.",
        "frozen_detector": "core/g6_ideation.hexa _g6_is_falsifiable VERBATIM word-sets",
        "eval_frames": "anima evaluate --py g_eval_all — 5 frozen gate concepts (=held-out gate×gate). in-dist=covered gate×expansion probe.",
        "N_topics": N,
        "gate_topics_en": GATE_SENT_EN,
        "held_out_frames": sorted(HELD), "held_out_n": len(HELD),
        "held_out_gate_gate_all": GATE_GATE, "measured_eval_frames": MEASURED,
        "pool_n": len(POOL),
        "HI": {"coverage": coverage_metric(cov_hi, HI_GATE_CNT),
               "covered_frames": cov_hi,
               "reps_en_per_frame": REPS_EN_HI, "reps_ko_per_frame": REPS_KO_HI},
        "LO": {"coverage": coverage_metric(cov_lo, LO_GATE_CNT),
               "covered_frames": cov_lo,
               "reps_en_per_frame": REPS_EN_LO, "reps_ko_per_frame": REPS_KO_LO},
        "bytes": {k: len(v.encode()) for k, v in blocks.items()},
        "lines": {k: v.count("\n") for k, v in blocks.items()},
        "audit_en": audit,
        "seed": 9128,
    }
    json.dump(design, open("design.json", "w"), ensure_ascii=False, indent=1)
    for k in blocks:
        print(f"{k}: {design['bytes'][k]/1e6:.2f}MB {design['lines'][k]} lines")
    print("HI coverage:", json.dumps(design["HI"]["coverage"]))
    print("LO coverage:", json.dumps(design["LO"]["coverage"]))
    print("audit_en HI:", json.dumps(audit["en_block_hi"]))
    print("audit_en LO:", json.dumps(audit["en_block_lo"]))

if __name__ == "__main__":
    main()
