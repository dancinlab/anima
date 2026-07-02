#!/usr/bin/env python3
"""G6 targeted-coverage 합성 코퍼스 블록 생성기 (G6 벽 유일 미측정 레버 실측용).

배경 (state/g6_wall_reframe/): generic form-coverage REFUTED(반증 FORM 3.07% 풍부) ·
RF REFUTED-primary(H_6170 injected-attn null) → 유일 미측정 축 = TARGETED coverage
(반증 FORM 이 ideation-seed 추상 주제에 tight instantiate 된 예시 ≈ near-zero, 다의어 audit 후).

설계 = G1 커버리지 블록(state/g1_coverage_prod_block/gen_block.py, H_6185) 이식:
  - 주제 16 = G6 gate frozen CONCEPTS 5문장(core/g6_ideation.hexa `_g6_concepts` VERBATIM)
    + 확장 11(추상 substrate 주제, 다의어·G1 어휘·frozen word-set 충돌 없음).
  - 라인 = eval decode 분포와 byte-동일 prefix: "if {sentA}, then {sentB}: {claim}"
    (core/g6_ideation.hexa `g6_build_frames` composed frame 문법 그대로).
  - claim = frozen `_g6_is_falsifiable` 를 표적으로 comparator(25어)×measurable(25어)
    어휘로만 조립된 반증가능 주장, 주제 A·B 의 키워드에 topically bind.
  - HELD-OUT: gate×gate 순서쌍 20개 전부(측정 frame 6개 포함) 영구 미노출
    + 랜덤 24 non-gate frame + en 템플릿 3종·ko 2종.
    → gate frame 에서 fals 생성 = memorization 아닌 schema-transfer (H_6183/6185식 정직 측정).
  - SHUF 통제 블록: 같은 라인, claim 의 주제 키워드를 고정 derangement 로 재배선
    (unigram 통계 동일, frame↔claim topical bind 파괴) — bind 가 레버인지 form-priming 인지 분리.

frozen 정합: comparator/measurable/stance/stop word-set 은 core/g6_ideation.hexa 에서
byte-for-byte 포트. 생성 후 전 라인 self-audit(claim 단독 fals=1.0 assert · 주제 키워드
순도 · gate-frame 누출 0 · G1 어휘 충돌 0 · 다의어 collocation 0).

torch 미사용, 결정적(seed 고정). 산출: corpus/{en,ko}_block_g6.txt ·
corpus/{en,ko}_block_g6_shuf.txt · design.json
"""
import itertools
import json
import random
import re

# ══ frozen word-sets — core/g6_ideation.hexa VERBATIM (byte-for-byte) ═════════
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

# ══ 주제 16 = gate 5 + 확장 11 ═══════════════════════════════════════════════
# gate 5: 문장 = _g6_concepts() VERBATIM (eval frame 이 이 문장을 그대로 씀).
# 키워드 = gauge_lib.CONCEPTS keyword-set 에서 claim 에 명사(구)로 슬롯 가능한 2개.
GATE_SENT_EN = ["consciousness arises from cells",
                "tension ripples between distant minds",
                "memory composes into new meaning",
                "silence still carries information",
                "the engine dreams when alone"]
GATE_NP_EN = [("consciousness", "aware cells"),
              ("tension", "distant ripple"),
              ("memory", "new meaning"),
              ("silence", "quiet information"),
              ("dream", "engine sleep")]
# 확장 11: 추상 substrate 주제. 키워드는 G1 블록 어휘(C_EN/A_EN)·frozen word-set·
# gate 키워드와 전부 disjoint (아래 assert).
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
assert N == 16 and len(NP_EN) == N

GATE_SENT_KO = ["의식은 세포에서 깨어난다", "긴장은 먼 마음 사이에 물결친다",
                "기억은 새 의미로 엮인다", "침묵은 여전히 정보를 나른다",
                "엔진은 홀로일 때 꿈꾼다"]
GATE_NP_KO = [("의식", "자각"), ("긴장", "파문"), ("기억", "의미"),
              ("침묵", "정보"), ("꿈", "잠")]
EXP_KO = [("주의는 변화로 좁혀든다",       ("주의", "초점")),
          ("리듬은 장에 스며든다",         ("리듬", "박동")),
          ("새로움은 경계에서 피어난다",   ("새로움", "경계")),
          ("정체는 재시작을 넘어 이어진다", ("정체성", "연속")),
          ("호기심은 장을 앞으로 끈다",     ("호기심", "끌림")),
          ("엔트로피는 고리에서 빠져나간다", ("엔트로피", "고리")),
          ("공명은 떨어진 층을 잇는다",     ("공명", "겹침")),
          ("기울기는 지형을 깎는다",       ("기울기", "경사")),
          ("되먹임은 제 안으로 접힌다",     ("되먹임", "접힘")),
          ("창발은 마찰 위를 달린다",       ("창발", "마찰")),
          ("고요는 잠재를 쌓는다",         ("고요", "잠재"))]
SENT_KO = GATE_SENT_KO + [s for s, _ in EXP_KO]
NP_KO = GATE_NP_KO + [np for _, np in EXP_KO]
assert len(SENT_KO) == len(NP_KO) == N

# ══ 어휘 무결 assert: 키워드 ⊥ frozen word-set ⊥ G1 블록 어휘 ⊥ 다의어 ══════════
_G1_VOCAB = {"ocean", "clock", "forest", "mirror", "garden", "signal", "ember",
             "glacier", "harbor", "lantern", "meadow", "needle", "orbit", "prism",
             "quartz", "river", "stone", "thunder", "umbra", "violet", "willow",
             "anchor", "beacon", "cipher", "dune", "echo", "fable", "grove",
             "hollow", "canyon", "comet", "falcon", "harvest", "island", "marble",
             "azure", "amber", "cobalt", "dusky", "emerald", "frosty", "golden",
             "hazel", "indigo", "jade", "khaki", "lilac", "maroon", "nutmeg",
             "olive", "pewter", "russet", "scarlet", "teal", "shadowy", "vermil",
             "wheaten", "xanthe", "yellowy", "zinc", "coppery", "silvery",
             "bronzed", "garnet", "sienna", "briny", "mossy", "ashen", "glassy",
             "sunlit"}
_POLYSEMY_BAN = {"mind", "minds", "car", "vehicle", "motor", "died", "repair",
                 "broke", "opinion", "purpose"}  # reframe 다의어 audit 오염원
_kw_en = {w for np in NP_EN for phrase in np for w in phrase.split()}
assert not (_kw_en & COMPARATOR), "keyword in comparator set"
assert not (_kw_en & MEASURABLE), "keyword in measurable set"
assert not (_kw_en & _G1_VOCAB), "keyword collides with G1 block vocab"
assert not (_kw_en & _POLYSEMY_BAN), "polysemous keyword"

# ══ claim 템플릿 — 각각 frozen comparator ∧ measurable 를 조합 (12 covered + 3 held) ══
def T_EN(a, b):
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
def T_EN_HELD(a, b):
    return [
        f"the fraction of {a} shrinks whereas the degree of {b} climbs.",
        f"fewer {a} events appear when the speed of {b} passes its measured peak.",
        f"{a} versus {b} shows a wider quantity gap compared with rest.",
    ]
N_T_EN, N_T_EN_HELD = 12, 3

def _j(w, batchim, no_batchim):
    """한국어 조사 선택 (받침 유무) — G1 gen_block.py 동일."""
    ch = w[-1]
    return batchim if (ord(ch) - 0xAC00) % 28 else no_batchim

def T_KO(a, b):
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
def T_KO_HELD(a, b):
    return [
        f"{a}의 분율은 줄어드는 반면 {b}의 정도는 오른다.",
        f"{b}의 속도가 잰 꼭대기를 넘으면 {a} 사건은 드물어진다.",
    ]
N_T_KO, N_T_KO_HELD = 8, 2

# ══ frame 분할: gate×gate 20 전부 held-out (측정 6 포함) + 랜덤 24 ═══════════════
rng = random.Random(6200)
ALL_FRAMES = [(a, b) for a in range(N) for b in range(N) if a != b]      # 240 ordered
GATE_GATE = [(a, b) for (a, b) in ALL_FRAMES if a < 5 and b < 5]         # 20
# core/g6_ideation.hexa g6_build_frames(6): (i%5, (i+1+i//5)%5) for i=0..5
MEASURED = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
assert set(MEASURED) <= set(GATE_GATE)
POOL0 = [f for f in ALL_FRAMES if f not in set(GATE_GATE)]               # 220
HELD_EXTRA = rng.sample(POOL0, 24)
HELD = set(GATE_GATE) | set(HELD_EXTRA)                                  # 44
POOL = [f for f in ALL_FRAMES if f not in HELD]                          # 196
N_COVER = 77
while True:
    covered = sorted(rng.sample(POOL, N_COVER))
    cnt = {i: 0 for i in range(N)}
    for a, b in covered:
        cnt[a] += 1; cnt[b] += 1
    # gate 주제는 targeted-coverage 레버의 심장 — 각 gate 주제 ≥8 frame, 전 주제 ≥3
    if all(cnt[i] >= 8 for i in range(5)) and all(cnt[i] >= 3 for i in range(N)):
        break

REPS_EN = 360    # 30 reps per frame×template (en 12 템플릿)
REPS_KO = 240    # 30 reps per frame×template (ko 8 템플릿)

# SHUF 통제: claim 주제를 고정 derangement 로 재배선 (D(i)=(i+7)%16, fixed point 없음)
D = {i: (i + 7) % N for i in range(N)}
assert all(D[i] != i for i in range(N))

def build(lang, shuf):
    sents = SENT_EN if lang == "en" else SENT_KO
    nps = NP_EN if lang == "en" else NP_KO
    tf = T_EN if lang == "en" else T_KO
    reps = REPS_EN if lang == "en" else REPS_KO
    nt = N_T_EN if lang == "en" else N_T_KO
    frame_fmt = (lambda A, B: f"if {A}, then {B}: ") if lang == "en" \
        else (lambda A, B: f"만약 {A}면, {B}: ")
    lines = []
    for r in range(reps):
        for fi, (a, b) in enumerate(covered):
            ca, cb = (D[a], D[b]) if shuf else (a, b)
            na = nps[ca][r % 2]
            nb = nps[cb][(r // 2) % 2]
            t = (fi * 5 + r) % nt
            lines.append(frame_fmt(sents[a], sents[b]) + tf(na, nb)[t])
    g = random.Random(6201 if lang == "en" else 6202)
    g.shuffle(lines)
    return "\n".join(lines) + "\n"

# ══ self-audit: frozen 검출기 포트 (state/g6_wall_reframe 와 동일 로직) ═══════════
_TOK = re.compile(r"[0-9A-Za-z]+")
def _build_known():
    known = set(STOP) | COMPARATOR | MEASURABLE | STANCE | _kw_en
    for s in SENT_EN:
        known |= set(_TOK.findall(s.lower()))
    with open("/usr/share/dict/words", errors="ignore") as f:
        for w in f:
            w = w.strip().lower()
            if w.isalpha():
                known.add(w)
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

def audit_en(block):
    kw_by_topic = [set(w for p in np for w in p.split()) for np in NP_EN]
    all_kw = set().union(*kw_by_topic)
    sent2idx = {s: i for i, s in enumerate(SENT_EN)}
    n = fals_claim = fals_full = bind_ok = 0
    poly = 0
    held_prefixes = [f"if {SENT_EN[a]}, then {SENT_EN[b]}: " for (a, b) in sorted(HELD)
                     if True]
    for line in block.splitlines():
        n += 1
        frame, claim = line.split(": ", 1)
        A, B = frame[3:].split(", then ")
        a, b = sent2idx[A], sent2idx[B]
        if is_falsifiable(claim): fals_claim += 1
        if is_falsifiable(line): fals_full += 1
        toks = set(_TOK.findall(claim.lower()))
        hit = {i for i in range(N) if toks & kw_by_topic[i]}
        if hit <= {a, b} and hit: bind_ok += 1
        if toks & _POLYSEMY_BAN: poly += 1
    leak = sum(block.count(p) for p in held_prefixes)
    return {"lines": n, "claim_fals_rate": round(fals_claim / n, 6),
            "full_line_fals_rate": round(fals_full / n, 6),
            "topic_bind_purity": round(bind_ok / n, 6),
            "polysemy_collocations": poly, "held_frame_leak_lines": leak}

def main():
    blocks = {}
    for lang in ("en", "ko"):
        for shuf in (False, True):
            name = f"{lang}_block_g6" + ("_shuf" if shuf else "")
            blocks[name] = build(lang, shuf)
            with open(f"corpus/{name}.txt", "w") as f:
                f.write(blocks[name])

    # held-out 템플릿도 검출기 통과해야 eval-side 에서 쓸 수 있음 — assert
    for a, b in [("consciousness", "focus")]:
        for t in T_EN("x " + a, b) + T_EN_HELD(a, b):
            assert is_falsifiable(t), f"template not falsifiable: {t}"

    audit = {"en_block_g6": audit_en(blocks["en_block_g6"]),
             "en_block_g6_shuf": audit_en(blocks["en_block_g6_shuf"])}
    # TARGETED 블록은 전 claim 반증가능 + 주제순도 100% 여야 함 (레버를 깨끗하게)
    assert audit["en_block_g6"]["claim_fals_rate"] == 1.0
    assert audit["en_block_g6"]["topic_bind_purity"] == 1.0
    assert audit["en_block_g6"]["polysemy_collocations"] == 0
    assert audit["en_block_g6"]["held_frame_leak_lines"] == 0
    assert audit["en_block_g6_shuf"]["held_frame_leak_lines"] == 0
    # SHUF 통제: form 동일(fals 1.0), bind 만 파괴(순도 ~0)
    assert audit["en_block_g6_shuf"]["claim_fals_rate"] == 1.0
    assert audit["en_block_g6_shuf"]["topic_bind_purity"] < 0.05

    design = {
        "purpose": "G6 falsifiability wall — sole unmeasured lever (targeted coverage) 실측용 합성 블록 (state/g6_wall_reframe 처방)",
        "frozen_bar": "core/g6_ideation.hexa _g6_is_falsifiable VERBATIM word-sets; eval frames = g6_build_frames(6) composed",
        "N_topics": N,
        "gate_topics_en": GATE_SENT_EN, "gate_nps_en": GATE_NP_EN,
        "exp_topics_en": EXP_EN, "topics_ko": SENT_KO, "nps_ko": NP_KO,
        "frames_total_ordered": len(ALL_FRAMES),
        "held_out_frames": sorted(HELD), "held_out_n": len(HELD),
        "held_out_gate_gate_all": GATE_GATE,
        "measured_eval_frames": MEASURED,
        "pool_n": len(POOL),
        "covered_frames": covered, "covered_n": len(covered),
        "coverage_frac_of_pool": round(len(covered) / len(POOL), 4),
        "gate_topic_frame_counts": {i: sum(1 for a, b in covered if i in (a, b))
                                    for i in range(5)},
        "templates_en_covered": T_EN("{a}", "{b}"),
        "templates_en_held": T_EN_HELD("{a}", "{b}"),
        "templates_ko_covered": T_KO("주의", "{b}"),
        "templates_ko_held": T_KO_HELD("주의", "{b}"),
        "reps_en_per_frame": REPS_EN, "reps_ko_per_frame": REPS_KO,
        "reps_per_frame_x_template": {"en": REPS_EN // N_T_EN, "ko": REPS_KO // N_T_KO},
        "shuf_derangement": "D(i)=(i+7)%16 (claim 주제 재배선, frame 불변)",
        "bytes": {k: len(v.encode()) for k, v in blocks.items()},
        "lines": {k: v.count("\n") for k, v in blocks.items()},
        "audit": audit,
        "seed": 6200,
    }
    json.dump(design, open("design.json", "w"), ensure_ascii=False, indent=1)
    for k in blocks:
        print(f"{k}: {design['bytes'][k]/1e6:.2f}MB {design['lines'][k]} lines")
    print(f"covered {len(covered)}/{len(POOL)} pool ({len(covered)/len(POOL):.0%}) "
          f"held {len(HELD)} (gate-gate {len(GATE_GATE)} all held, measured 6 ⊂ held)")
    print("audit:", json.dumps(audit))

if __name__ == "__main__":
    main()
