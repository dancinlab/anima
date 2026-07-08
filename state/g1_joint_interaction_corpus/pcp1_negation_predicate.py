"""PC-P1 negation × predicate-polarity → emotion-marker probe (Fable PC-P redesign).

A second, denser-data XOR positive control (complements PC-P2 which was power-
limited on formal ko). Lives in ko-sns where emotion markers are abundant:
  A = negation present before the predicate (안/못)  ∈ {no, yes}
  B = predicate polarity (positive stem 좋/맛있/... vs negative 나쁘/싫/...)
  y = following emotion marker: laugh(ㅋ/ㅎ run) vs sad(ㅠ/ㅜ run) within W_POST
Effective sentiment = B XOR A: 좋(pos)+없음 -> laugh; 안 좋(pos+neg) -> sad;
나쁘(neg)+없음 -> sad; 안 나쁘(neg+neg) -> laugh. Pure XOR: an additive main-effect
logit can only add a per-B constant and CANNOT flip A's effect -> mispredicts the
(neg-stem, negated) cell. Same frozen IPF/I3/LOCO/bootstrap machinery as PC-P2.

model-free, $0. Single pre-registered run (NOT axis-hunting): reports whatever it
finds, with the 조사 PC-N specificity control obligation noted separately.
"""
import sys, json, math

KO_SNS = ("/Users/mini/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-sns/"
          "snapshots/410b0b7bcfb15c78ebd609f3af6cef40aa5a7442/anima-corpus-ko-sns.txt")

# frozen lexicons (pre-registered; do not widen to fill cells)
POS = ["좋", "기쁘", "행복", "예쁘", "귀엽", "재밌", "즐겁", "사랑", "맛있", "멋지"]
NEG = ["나쁘", "싫", "짜증", "힘들", "슬프", "아프", "무섭", "화나", "끔찍", "지겹"]
NEGATORS = ["안", "못"]           # 술어 직전 부정소
LAUGH = ["ㅋ", "ㅎ"]              # y=0
SAD = ["ㅠ", "ㅜ"]               # y=1
W_NEG = 3      # bytes(chars) before predicate to look for a negator
W_POST = 40    # chars after predicate to look for an emotion marker
NMIN = 200
SEED = 7


def has_negator(pre3):
    """negator immediately before predicate (안/못 within last W_NEG chars, token-ish)."""
    for ng in NEGATORS:
        j = pre3.rfind(ng)
        if j < 0:
            continue
        # require the negator be near the end (adjacent to predicate) and not mid-word:
        # char before negator is space/start/punct
        if j >= len(pre3) - W_NEG:
            before = pre3[j - 1] if j > 0 else " "
            if not ('가' <= before <= '힣'):   # not preceded by another hangul syllable
                return True
    return False


def first_marker(seg):
    """first emotion marker run in seg -> 0(laugh)/1(sad)/None."""
    bl = bs = 10 ** 9
    for w in LAUGH:
        i = seg.find(w)
        if i >= 0:
            bl = min(bl, i)
    for w in SAD:
        i = seg.find(w)
        if i >= 0:
            bs = min(bs, i)
    if bl == bs == 10 ** 9:
        return None
    return 0 if bl < bs else 1


def build_cube(text):
    """count[a=negation][b=predPolarity][y=marker]. a:0=none 1=negated · b:0=pos 1=neg."""
    cube = [[[0, 0] for _ in range(2)] for _ in range(2)]
    stems = [(w, 0) for w in POS] + [(w, 1) for w in NEG]
    for stem, b in stems:
        start = 0
        while True:
            i = text.find(stem, start)
            if i < 0:
                break
            start = i + 1
            pre = text[max(0, i - W_NEG - 1):i]
            a = 1 if has_negator(pre) else 0
            post = text[i + len(stem):i + len(stem) + W_POST]
            y = first_marker(post)
            if y is None:
                continue
            cube[a][b][y] += 1
    return cube


# --- shared stat machinery (same as pcp2, proven) ---
def ipf_additive(cube, iters=200):
    mu = [[[1.0, 1.0] for _ in range(2)] for _ in range(2)]
    def m_ab(t): return [[sum(t[a][b]) for b in range(2)] for a in range(2)]
    def m_ay(t): return [[sum(t[a][b][y] for b in range(2)) for y in range(2)] for a in range(2)]
    def m_by(t): return [[sum(t[a][b][y] for a in range(2)) for y in range(2)] for b in range(2)]
    C_ab, C_ay, C_by = m_ab(cube), m_ay(cube), m_by(cube)
    eps = 1e-9
    for _ in range(iters):
        M = m_ab(mu)
        for a in range(2):
            for b in range(2):
                s = C_ab[a][b] / (M[a][b] + eps)
                for y in range(2):
                    mu[a][b][y] *= s
        M = m_ay(mu)
        for a in range(2):
            for y in range(2):
                s = C_ay[a][y] / (M[a][y] + eps)
                for b in range(2):
                    mu[a][b][y] *= s
        M = m_by(mu)
        for b in range(2):
            for y in range(2):
                s = C_by[b][y] / (M[b][y] + eps)
                for a in range(2):
                    mu[a][b][y] *= s
    return mu


def cond(t, a, b):
    s = t[a][b][0] + t[a][b][1]
    return [0.5, 0.5] if s <= 0 else [t[a][b][0] / s, t[a][b][1] / s]


def i3_deviance(cube, mu):
    N = sum(cube[a][b][y] for a in range(2) for b in range(2) for y in range(2))
    tot = 0.0
    for a in range(2):
        for b in range(2):
            pe, pa = cond(cube, a, b), cond(mu, a, b)
            for y in range(2):
                if cube[a][b][y] > 0:
                    tot += cube[a][b][y] * math.log((pe[y] + 1e-12) / (pa[y] + 1e-12))
    return tot / N if N else 0.0


def double_diff(cube):
    def lo(a, b):
        p = cond(cube, a, b)
        return math.log((p[0] + 1e-9) / (p[1] + 1e-9))
    return (lo(0, 0) - lo(0, 1)) - (lo(1, 0) - lo(1, 1))


class RNG:
    def __init__(self, s): self.s = s & 0xFFFFFFFF
    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


def bootstrap_null(mu, N, rng, reps=200):
    tot = sum(mu[a][b][y] for a in range(2) for b in range(2) for y in range(2))
    cum, acc = [], 0.0
    for a in range(2):
        for b in range(2):
            for y in range(2):
                acc += mu[a][b][y] / tot
                cum.append((acc, a, b, y))
    out = []
    for _ in range(reps):
        c = [[[0, 0] for _ in range(2)] for _ in range(2)]
        for _ in range(N):
            r = rng.next()
            for acc, a, b, y in cum:
                if r <= acc:
                    c[a][b][y] += 1
                    break
        out.append(i3_deviance(c, ipf_additive(c, iters=60)))
    out.sort()
    return out[int(0.95 * len(out))]


def loco_r2(cube):
    res = []
    def lo(a, b):
        p = cond(cube, a, b)
        return math.log((p[1] + 1e-9) / (p[0] + 1e-9))   # log-odds of SAD
    for ha in range(2):
        for hb in range(2):
            oa, ob = 1 - ha, 1 - hb
            pred = lo(ha, ob) + lo(oa, hb) - lo(oa, ob)
            emp = lo(ha, hb)
            res.append(dict(cell=(ha, hb), pred_lo=round(pred, 3), emp_lo=round(emp, 3),
                            sign_wrong=(pred > 0) != (emp > 0) and abs(emp) > 0.2))
    return res, sum(r["sign_wrong"] for r in res)


def analyze(name, cube):
    N = sum(cube[a][b][y] for a in range(2) for b in range(2) for y in range(2))
    min_cell = min(cube[a][b][0] + cube[a][b][1] for a in range(2) for b in range(2))
    mu = ipf_additive(cube)
    I3 = i3_deviance(cube, mu)
    dd = double_diff(cube)
    null95 = bootstrap_null(mu, N, RNG(SEED), reps=200)
    loco, n_wrong = loco_r2(cube)
    argmax_mm = any((cond(cube, a, b)[0] > cond(cube, a, b)[1]) != (cond(mu, a, b)[0] > cond(mu, a, b)[1])
                    for a in range(2) for b in range(2))
    R0 = argmax_mm and abs(dd) >= 0.5
    R1 = I3 > null95
    R2 = n_wrong >= 2
    return dict(name=name, N=N, min_cell=min_cell, gate_ok=min_cell >= NMIN,
                I3=round(I3, 5), null95=round(null95, 5), dd=round(dd, 4),
                R0=R0, R1=R1, R2=R2, n_wrong=n_wrong, loco=loco,
                PASS=(min_cell >= NMIN and R0 and R1 and R2))


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else KO_SNS
    print(f"# PC-P1 negation×predicate→emotion-marker · {corpus.split('/')[-1]}")
    with open(corpus, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    print(f"# chars: {len(text):,}")
    cube = build_cube(text)
    print("# cube count[a=negation][b=predPolarity][y=marker]  (a:0=none 1=negated · b:0=pos 1=neg · y:0=laugh 1=sad)")
    for a in range(2):
        for b in range(2):
            print(f"  neg={'yes' if a else 'no ':3} pred={'pos' if b==0 else 'neg'} "
                  f"-> laugh={cube[a][b][0]:6d} sad={cube[a][b][1]:6d}")
    r = analyze("PC-P1_negation_predicate", cube)
    print()
    for k in ("N", "min_cell", "gate_ok", "I3", "null95", "dd", "R0", "R1", "R2", "n_wrong", "PASS"):
        print(f"  {k:>10}: {r[k]}")
    print("  LOCO:")
    for x in r["loco"]:
        print(f"    cell(a={x['cell'][0]},b={x['cell'][1]}) pred_lo={x['pred_lo']:+.3f} "
              f"emp_lo={x['emp_lo']:+.3f} sign_wrong={x['sign_wrong']}")
    print(f"\n# PC-P1 verdict: {'PASS' if r['PASS'] else 'not-yet (see gate/R0/R1/R2)'}")
    json.dump(r, open("state/g1_joint_interaction_corpus/pcp1_result.json", "w"),
              ensure_ascii=False, indent=1, default=str)
