"""
H_1232 — RESEARCH-AXIS-LEVEL COMBINATION CLIMB (real axes B·E·F·G on one substrate)
Round-1/2 climbed TOY measurement-signals. This climbs the ACTUAL UNIVERSE research
axes on a SHARED substrate (ECA panel) — the literal "축끼리 매트릭스". Find the FINAL
COMBINATION of research axes that determines substrate COMPLEXITY (Wolfram class III/IV
= the consciousness-relevant edge-of-chaos / integration regime). Framework MATRIX.md §0.
$0 LOCAL numpy (n small, no corpus/GPU). a_phi_iit4_tool: variance-partition Φ-proxy is
a PRE-SCREEN proxy (not a terminal Φ verdict) — flagged honestly.

SHARED SUBSTRATE: elementary cellular automata (ECA), width W, T steps, drop transient.
Each (rule, density, seed) run → per-run REAL axis measures:
  B-PHI   = variance-partition integration  (global_var − mean bipartition part_var)  [axis B/D]
  E-SI    = Savant Index = max/mean region-activity (savant_lib formula)              [axis E]
  F-SYNC  = synchrony order param = mean pairwise cell-timeseries correlation         [axis F]
  G-LZ    = normalized LZ76 complexity of spacetime                                   [axis G]
  density, col-entropy  = controls
TARGET = Wolfram class ∈ {III, IV} (complex) vs {I, II} (trivial) — external labels.

METHOD: greedy forward climb by held-out logistic-probe AUROC over the axes.
FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 FIXED-POINT — climb saturates at k* < N (next axis gain < EPS) → a FINAL research-
                   axis COMBINATION determines complexity.
  F2 NON-TRIVIAL — k* >= 2 AND saturation AUROC >= 0.70.
  H_1232 SUPPORTED iff F1 AND F2 (a real multi-axis combination determines complexity).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff no saturation (irreducible — every axis adds)
  OR k*=1 (one axis dominates, complexity is single-axis).

scope: small ECA, proxy-Φ pre-screen (a_scale_honest_scope · a_phi_iit4_tool). seed-fixed.
"""
import os, math, json, random
import numpy as np

SEED = 7
random.seed(SEED); np.random.seed(SEED)
W = 24; T = 80; TRANSIENT = 20; DENS = [0.2, 0.5, 0.8]; SEEDS = list(range(6)); EPS = 0.01
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1232_research_axis_climb")

# Wolfram classes (canonical): I uniform, II periodic, III chaotic, IV complex
CLASS = {
    0:"I", 8:"I", 32:"I", 128:"I", 160:"I", 250:"I",
    1:"II", 2:"II", 4:"II", 12:"II", 36:"II", 108:"II", 184:"II", 232:"II",
    18:"III", 22:"III", 30:"III", 45:"III", 60:"III", 90:"III", 105:"III", 126:"III", 150:"III",
    54:"IV", 110:"IV", 124:"IV", 137:"IV", 193:"IV",
}
COMPLEX = {"III", "IV"}


def eca_run(rule, width, steps, dens, seed):
    rng = np.random.RandomState(seed*1000 + rule)
    row = (rng.random(width) < dens).astype(np.int8)
    table = [(rule >> i) & 1 for i in range(8)]
    space = np.zeros((steps, width), dtype=np.int8)
    for t in range(steps):
        space[t] = row
        l = np.roll(row, 1); r = np.roll(row, -1)
        idx = (l << 2) | (row << 1) | r
        row = np.array([table[i] for i in idx], dtype=np.int8)
    return space[TRANSIENT:]  # drop transient


def phi_proxy(space):
    # variance-partition integration: total col-var minus mean of two-half part vars
    x = space.astype(float)
    gv = x.var(axis=0).sum()
    h = x.shape[1] // 2
    pv = x[:, :h].var(axis=0).sum() + x[:, h:].var(axis=0).sum()
    return float(gv - pv)


def savant_index(space):
    # region activity: split into 4 regions, activity = mean firing; SI = max/mean
    w = space.shape[1]; q = w // 4
    acts = [space[:, i*q:(i+1)*q].mean() for i in range(4)]
    acts = np.array(acts); m = acts.mean()
    return float(acts.max()/m) if m > 1e-9 else 0.0


def sync_param(space):
    # mean pairwise correlation between cell time-series (synchrony)
    x = space.astype(float)
    sd = x.std(axis=0)
    live = sd > 1e-9
    if live.sum() < 2: return 0.0
    c = np.corrcoef(x[:, live].T)
    n = c.shape[0]
    iu = np.triu_indices(n, 1)
    return float(np.abs(c[iu]).mean())


def lz76(seq):
    # normalized Lempel-Ziv 76 complexity of a binary string
    s = ''.join(str(int(b)) for b in seq)
    i, c, l = 0, 1, 1; n = len(s)
    k, kmax = 1, 1
    while True:
        if i + k > n - 1:
            c += 1; break
        if s[i:i+k] in s[l-1+0 : l-1+k] if False else (s[i:i+k] in "".join([s[a] for a in range(l-1, l-1+k)]) if l-1+k<=n else False):
            pass
        # robust substring search
        if s[i:i+k] in s[l-1:l-1+kmax] if False else False:
            pass
        sub = s[l-1:l-1+k]
        if s[i:i+k] == sub:
            k += 1
            if l + k > n: c += 1; break
        else:
            if k > kmax: kmax = k
            i += 1
            if i == l:
                c += 1; l += kmax; i = 0; kmax = 1; k = 1
                if l + 1 > n: break
            else:
                k = 1
    # normalize
    return c * math.log(max(n,2), 2) / max(n, 1)


def lz76_simple(seq):
    # clean LZ76: count distinct phrases (production complexity), normalized
    s = ''.join(str(int(b)) for b in seq); n = len(s)
    phrases = set(); i = 0; cur = ""
    count = 0
    seen = set()
    while i < n:
        cur += s[i]; i += 1
        if cur not in seen:
            seen.add(cur); count += 1; cur = ""
    if cur: count += 1
    norm = count / (n / math.log2(n)) if n > 4 else count
    return float(norm)


def col_entropy(space):
    p = space.mean()
    if p <= 0 or p >= 1: return 0.0
    return float(-(p*math.log2(p) + (1-p)*math.log2(1-p)))


def auroc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty(len(s), float); ranks[order] = np.arange(1, len(s)+1)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); avg = rsum/cnt; ranks = avg[inv]
    n1 = int(y.sum()); n0 = len(y)-n1
    if n1 == 0 or n0 == 0: return float("nan")
    return (ranks[y==1].sum() - n1*(n1+1)/2)/(n1*n0)


def logreg_auroc(Xtr, ytr, Xte, yte, iters=600, lr=0.3, l2=1e-3):
    if Xtr.ndim == 1: Xtr = Xtr[:,None]; Xte = Xte[:,None]
    mu = Xtr.mean(0); sd = Xtr.std(0)+1e-6; Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    n,d = Xtr.shape; w=np.zeros(d); b=0.0
    for _ in range(iters):
        p=1/(1+np.exp(-(Xtr@w+b))); w-=lr*(Xtr.T@(p-ytr)/n+l2*w); b-=lr*float((p-ytr).mean())
    return float(auroc(1/(1+np.exp(-(Xte@w+b))), yte))


AXES = ["B-PHI","E-SI","F-SYNC","G-LZ","density","col-ent"]

def main():
    print("=== H_1232 research-axis combination climb (ECA shared substrate) ===", flush=True)
    rows = []
    for rule in CLASS:
        for d in DENS:
            for sd in SEEDS:
                sp = eca_run(rule, W, T, d, sd)
                feats = {
                    "B-PHI": phi_proxy(sp),
                    "E-SI": savant_index(sp),
                    "F-SYNC": sync_param(sp),
                    "G-LZ": lz76_simple(sp.flatten()),
                    "density": float(sp.mean()),
                    "col-ent": col_entropy(sp),
                }
                rows.append((rule, 1 if CLASS[rule] in COMPLEX else 0, feats))
    rng = np.random.RandomState(SEED); order = rng.permutation(len(rows))
    rows = [rows[i] for i in order]
    y = np.array([r[1] for r in rows])
    feats = {a: np.array([r[2][a] for r in rows]) for a in AXES}
    half = len(y)//2; ytr, yte = y[:half].astype(float), y[half:].astype(float)
    print(f"[data] {len(rows)} ECA runs · complex(III/IV)={int(y.sum())} trivial(I/II)={len(y)-int(y.sum())}", flush=True)
    def Xof(sel, sl): return np.stack([feats[a][sl] for a in sel], axis=1)

    chosen, ladder, rem, prev = [], [], list(AXES), 0.5
    while rem:
        ba, bau = None, -1
        for a in rem:
            au = logreg_auroc(Xof(chosen+[a], slice(0,half)), ytr, Xof(chosen+[a], slice(half,None)), yte)
            if au > bau: bau, ba = au, a
        ladder.append({"k":len(chosen)+1,"added":ba,"auroc":bau,"gain":bau-prev})
        print(f"  k={len(chosen)+1} +{ba:9s} AUROC={bau:.4f} gain={bau-prev:+.4f}", flush=True)
        chosen.append(ba); rem.remove(ba); prev = bau
    kstar = len(AXES); final = list(chosen); sat = ladder[-1]["auroc"]
    for i in range(1, len(ladder)):
        if ladder[i]["gain"] < EPS: kstar=i; final=[ladder[j]["added"] for j in range(i)]; sat=ladder[i-1]["auroc"]; break

    f1 = kstar < len(AXES)
    f2 = (kstar >= 2) and (sat >= 0.70)
    supported = bool(f1 and f2)
    if supported:
        ruling = f"SUPPORTED: a FINAL research-axis COMBINATION determines substrate complexity — k*={kstar} {final} (AUROC {sat:.3f}); the axes combine to a fixed point"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: no saturation — every research axis keeps adding (irreducible whole, echoes axis-D)"
    else:
        ruling = f"CLOSED-NEGATIVE: trivial — k*={kstar} (single-axis dominance or sat<0.70, AUROC {sat:.3f})"

    verdict = {
        "H":"H_1232","title":"research-axis combination climb (ECA shared substrate)","axes":AXES,
        "n_runs":len(rows),"n_complex":int(y.sum()),"ladder":ladder,"k_star":kstar,
        "final_combination":final,"saturation_auroc":sat,
        "F1_fixed_point":{"k_star":kstar,"N":len(AXES),"pass":bool(f1)},
        "F2_non_trivial":{"k_star":kstar,"sat":sat,"pass":bool(f2)},
        "supported":supported,"ruling":ruling,
        "framework":"MATRIX.md §0 — research-axis-level climb (B·E·F·G real axes)",
        "caveat":"variance-partition Φ-proxy = pre-screen (a_phi_iit4_tool: NOT a terminal faithful-Φ verdict); small ECA (a_scale_honest_scope)",
        "seed":SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
