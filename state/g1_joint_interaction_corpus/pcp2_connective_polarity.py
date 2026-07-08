"""PC-P2 connective-polarity probe (Fable PC-P redesign, 1순위) — model-free, $0.

Tests whether the pipeline detects a GENUINE non-additive (XOR-type) interaction
that lives in real byte text:
  A = polarity of the clause BEFORE a connective (pos / neg)
  B = connective type (contrast 지만/하지만/... vs conjunction 그리고/또한/...)
  y = polarity of the clause AFTER the connective (pos / neg)
Textbook XOR crossover: (pos,conj)->pos · (pos,contrast)->neg · (neg,conj)->neg ·
(neg,contrast)->POS. An additive main-effect logit can only shift y by a per-B
constant; it CANNOT flip the sign of A's effect => it mispredicts the (neg,contrast)
cell. That sign-flip is the real non-additive signal 조사 lacked.

Canonical additive baseline = main-effect multinomial logit fit by IPF (matches the
{AB},{AY},{BY} 2-way margins, 3-way λ_ABY≡0) — 1:1 equivalent to the trunk-CE floor
the dead levers hit (logits = W·[f(A)+g(B)] + b). Interaction signal I3 = conditional
deviance G²/2N = nats a bind must earn. Null = parametric bootstrap from the fitted
additive model (a shuffle cannot isolate λ_ABY). Decision = R0 ∧ R1 ∧ R2 + PC-N.
"""
import sys, json, math
from collections import Counter

KO_GENERAL = ("/Users/mini/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-general/"
              "snapshots/9f03495689d52fb50b5b7d8d673d77e38266afcc/anima-corpus-ko-general.txt")

# --- pre-registered lexicons (FROZEN before scan; do not widen to fill cells) ---
POS = ["좋", "기쁘", "행복", "훌륭", "멋지", "예쁘", "아름답", "즐겁", "사랑", "맛있"]
NEG = ["나쁘", "싫", "슬프", "힘들", "아프", "무섭", "화나", "끔찍", "어렵", "지겹"]
CONTRAST = ["지만", "하지만", "그러나", "그런데"]
CONJ = ["그리고", "또한", "게다가"]
W_PRE = 80
W_POST = 80
NMIN = 200          # min count per cell (G gate)
SEED = 7
BOOT = 1000


def polarity_last(seg):
    """last polarity word in seg -> 0(pos)/1(neg)/None, by byte position of match."""
    bp = bn = -1
    for w in POS:
        i = seg.rfind(w)
        if i > bp:
            bp = i
    for w in NEG:
        i = seg.rfind(w)
        if i > bn:
            bn = i
    if bp < 0 and bn < 0:
        return None
    return 0 if bp > bn else 1


def polarity_first(seg):
    """first polarity word in seg -> 0(pos)/1(neg)/None."""
    bp = bn = 10 ** 9
    for w in POS:
        i = seg.find(w)
        if i >= 0:
            bp = min(bp, i)
    for w in NEG:
        i = seg.find(w)
        if i >= 0:
            bn = min(bn, i)
    if bp == bn == 10 ** 9:
        return None
    return 0 if bp < bn else 1


def build_cube(text):
    """count[a][b][y] over connective hits. b: 0=contrast 1=conj."""
    cube = [[[0, 0] for _ in range(2)] for _ in range(2)]
    n = len(text)
    conns = [(w, 0) for w in CONTRAST] + [(w, 1) for w in CONJ]
    # scan by scanning for each connective occurrence
    for w, b in conns:
        start = 0
        while True:
            i = text.find(w, start)
            if i < 0:
                break
            start = i + 1
            pre = text[max(0, i - W_PRE):i]
            post = text[i + len(w):i + len(w) + W_POST]
            a = polarity_last(pre)
            y = polarity_first(post)
            if a is None or y is None:
                continue
            cube[a][b][y] += 1
    return cube


def ipf_additive(cube, iters=200):
    """Fit no-3-way log-linear (main-effect logit) by IPF on 2x2x2 counts.
    Preserves {a,b},{a,y},{b,y} margins; 3-way interaction removed."""
    mu = [[[1.0, 1.0] for _ in range(2)] for _ in range(2)]
    N = sum(cube[a][b][y] for a in range(2) for b in range(2) for y in range(2))

    def marg_ab(t): return [[sum(t[a][b]) for b in range(2)] for a in range(2)]
    def marg_ay(t): return [[sum(t[a][b][y] for b in range(2)) for y in range(2)] for a in range(2)]
    def marg_by(t): return [[sum(t[a][b][y] for a in range(2)) for y in range(2)] for b in range(2)]

    C_ab, C_ay, C_by = marg_ab(cube), marg_ay(cube), marg_by(cube)
    eps = 1e-9
    for _ in range(iters):
        M = marg_ab(mu)
        for a in range(2):
            for b in range(2):
                s = C_ab[a][b] / (M[a][b] + eps)
                for y in range(2):
                    mu[a][b][y] *= s
        M = marg_ay(mu)
        for a in range(2):
            for y in range(2):
                s = C_ay[a][y] / (M[a][y] + eps)
                for b in range(2):
                    mu[a][b][y] *= s
        M = marg_by(mu)
        for b in range(2):
            for y in range(2):
                s = C_by[b][y] / (M[b][y] + eps)
                for a in range(2):
                    mu[a][b][y] *= s
    return mu, N


def cond(t, a, b):
    s = t[a][b][0] + t[a][b][1]
    if s <= 0:
        return [0.5, 0.5]
    return [t[a][b][0] / s, t[a][b][1] / s]


def i3_deviance(cube, mu):
    """conditional deviance / N = per-token nats the additive model misses."""
    N = sum(cube[a][b][y] for a in range(2) for b in range(2) for y in range(2))
    tot = 0.0
    for a in range(2):
        for b in range(2):
            pe = cond(cube, a, b)
            pa = cond(mu, a, b)
            for y in range(2):
                if cube[a][b][y] > 0:
                    tot += cube[a][b][y] * math.log((pe[y] + 1e-12) / (pa[y] + 1e-12))
    return tot / N if N else 0.0


def double_diff(cube):
    """interaction log-odds double difference Δ² (sign = crossover direction)."""
    def lo(a, b):
        p = cond(cube, a, b)
        return math.log((p[0] + 1e-9) / (p[1] + 1e-9))
    return (lo(0, 0) - lo(0, 1)) - (lo(1, 0) - lo(1, 1))


class RNG:
    """tiny deterministic LCG (Math.random-free environment safety)."""
    def __init__(self, s): self.s = s & 0xFFFFFFFF
    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


def bootstrap_null(mu, N, rng, reps=BOOT):
    """parametric bootstrap: sample N tokens from the additive-fitted dist, recompute I3."""
    flat = []
    tot = 0.0
    for a in range(2):
        for b in range(2):
            for y in range(2):
                tot += mu[a][b][y]
    cum = []
    acc = 0.0
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
        mu2, _ = ipf_additive(c, iters=60)
        out.append(i3_deviance(c, mu2))
    out.sort()
    return out[int(0.95 * len(out))]


def loco_r2(cube):
    """leave-one-cell-out: fit additive on 3 (a,b) cells, predict the 4th.
    R2 cell passes if additive's held-out argmax SIGN is wrong (not just less
    confident) vs the empirical joint."""
    results = []
    for ha in range(2):
        for hb in range(2):
            # fit main-effect logit on the other 3 cells: logit(y=neg|a,b)=θ+αa+βb
            # closed form on 3 cells (binary y). Use log-odds additive decomposition.
            def lo(a, b):
                p = cond(cube, a, b)
                return math.log((p[1] + 1e-9) / (p[0] + 1e-9))  # log-odds of NEG
            # additive predicts lo(ha,hb) = lo(ha, other_b) + lo(other_a, hb) - lo(other_a, other_b)
            oa, ob = 1 - ha, 1 - hb
            pred_lo = lo(ha, ob) + lo(oa, hb) - lo(oa, ob)
            emp_lo = lo(ha, hb)
            sign_wrong = (pred_lo > 0) != (emp_lo > 0) and abs(emp_lo) > 0.2
            results.append(dict(cell=(ha, hb), pred_lo=round(pred_lo, 3),
                                emp_lo=round(emp_lo, 3), sign_wrong=sign_wrong))
    n_wrong = sum(r["sign_wrong"] for r in results)
    return results, n_wrong


def run_axis(name, cube):
    N = sum(cube[a][b][y] for a in range(2) for b in range(2) for y in range(2))
    min_cell = min(cube[a][b][0] + cube[a][b][1] for a in range(2) for b in range(2))
    mu, _ = ipf_additive(cube)
    I3 = i3_deviance(cube, mu)
    dd = double_diff(cube)
    rng = RNG(SEED)
    null95 = bootstrap_null(mu, N, rng, reps=200)  # 200 for speed; 1000 in full
    loco, n_wrong = loco_r2(cube)
    # R0: any cell argmax mismatch + |dd| >= 0.5 + sign reversal both directions
    argmax_mismatch = any(
        (cond(cube, a, b)[0] > cond(cube, a, b)[1]) != (cond(mu, a, b)[0] > cond(mu, a, b)[1])
        for a in range(2) for b in range(2))
    R0 = argmax_mismatch and abs(dd) >= 0.5
    R1 = I3 > null95
    R2 = n_wrong >= 2   # majority of 4 cells
    return dict(name=name, N=N, min_cell=min_cell, gate_ok=min_cell >= NMIN,
                I3=round(I3, 5), null95=round(null95, 5), dd=round(dd, 4),
                R0=R0, R1=R1, R2=R2, n_wrong=n_wrong, loco=loco,
                PASS=(min_cell >= NMIN and R0 and R1 and R2))


KO_SNS = ("/Users/mini/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-sns/"
          "snapshots/410b0b7bcfb15c78ebd609f3af6cef40aa5a7442/anima-corpus-ko-sns.txt")


def pool_cubes(*cubes):
    out = [[[0, 0] for _ in range(2)] for _ in range(2)]
    for c in cubes:
        for a in range(2):
            for b in range(2):
                for y in range(2):
                    out[a][b][y] += c[a][b][y]
    return out


if __name__ == "__main__":
    corpora = sys.argv[1:] if len(sys.argv) > 1 else [KO_GENERAL, KO_SNS]
    print(f"# PC-P2 connective-polarity probe · POOLED {[c.split('/')[-1] for c in corpora]}")
    cubes = []
    for corpus in corpora:
        with open(corpus, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        print(f"# {corpus.split('/')[-1]}: {len(text):,} chars")
        cubes.append(build_cube(text))
    cube = pool_cubes(*cubes)
    print("# cube count[a=prePolarity][b=conn][y=postPolarity]  (a/y: 0=pos 1=neg · b: 0=contrast 1=conj)")
    for a in range(2):
        for b in range(2):
            print(f"  a={'pos' if a==0 else 'neg'} b={'contrast' if b==0 else 'conj'} "
                  f"-> pos={cube[a][b][0]:6d} neg={cube[a][b][1]:6d}")
    res = run_axis("PC-P2_connective_polarity", cube)
    print()
    for k in ("N", "min_cell", "gate_ok", "I3", "null95", "dd", "R0", "R1", "R2", "n_wrong", "PASS"):
        print(f"  {k:>10}: {res[k]}")
    print("  LOCO (held-out cell sign check):")
    for r in res["loco"]:
        print(f"    cell(a={r['cell'][0]},b={r['cell'][1]}) pred_lo={r['pred_lo']:+.3f} "
              f"emp_lo={r['emp_lo']:+.3f} sign_wrong={r['sign_wrong']}")
    print()
    verdict = "PASS — pipeline detects genuine XOR interaction" if res["PASS"] \
        else "not-yet (see R0/R1/R2)"
    print(f"# PC-P2 verdict: {verdict}")
    json.dump(res, open("state/g1_joint_interaction_corpus/pcp2_result.json", "w"),
              ensure_ascii=False, indent=1, default=str)
