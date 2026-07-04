#!/usr/bin/env python3
"""
H_9129 STEP-0 (mini numpy, DIRECTIONAL — NOT 303M engine-native, a_engine_native_learning).

L5 hippocampal associative-store lane: novel-combine placed in a SEPARATE lane
(pattern-separated storage + CA3-attractor pattern-completion), NOT in the mouth
(byte-LM readout / Broca). The lane only STORES relations and COMPLETES patterns;
there is no generative mouth. Read-out = relatedness via multi-step chained completion.

Uncheatable BIND test = Dusek-Eichenbaum transitive-inference paradigm:
  held-out NOVEL pairs split into
    (a) reachable  : same-chain non-adjacent (A-B, B-C stored  =>  A-C completable)
    (b) unreachable: cross-chain (no stored relation path connects them)
  BOTH are held-out (never directly stored) and share the SAME surface form
  (item codes drawn iid from one distribution => raw-form similarity matched).

fooled_by_form == True  iff  reachable ~= unreachable  (lane is also just FORM).
verdict:
  BIND  if reachable >> unreachable  (relation-chaining, not form)
  form  if reachable ~= unreachable
  floor if both ~0 (lane retrieves nothing)

Controls:
  - FORM baseline: raw code cosine (no relations)  -> should give reachable ~= unreachable
                   (proves the two pair-classes are form-matched / test is fair)
  - SHUFFLE ablation: destroy stored chain structure (permute the successor map)
                   -> reachable must collapse to unreachable (proves lift = RELATION, not form)
"""
import numpy as np

SEED = 20260705
rng = np.random.default_rng(SEED)

# ---- substrate params ----
N_CHAINS   = 8
CHAIN_LEN  = 6          # items per chain
DIM        = 2048       # sparse high-dim code (pattern separation)
ACTIVE     = 40         # active bits per item code (sparse)
STEPS      = 6          # CA3 completion iterations (chain depth reachable)
KWTA       = 40         # k-winners-take-all per completion step (attractor cleanup)

N_ITEMS = N_CHAINS * CHAIN_LEN

def make_codes():
    """Pattern separation: each item = random sparse binary {0,1} code, near-orthogonal."""
    C = np.zeros((N_ITEMS, DIM), dtype=np.float32)
    for i in range(N_ITEMS):
        idx = rng.choice(DIM, size=ACTIVE, replace=False)
        C[i, idx] = 1.0
    return C

def chain_of(item):   # which chain an item index belongs to
    return item // CHAIN_LEN
def pos_in_chain(item):
    return item % CHAIN_LEN

def build_store(codes, successor):
    """
    Heteroassociative CA3 store: W maps a cue toward its stored successor.
    W = sum_k outer(code[next_k], code[cur_k]).  Only ADJACENT (premise) pairs stored.
    """
    W = np.zeros((DIM, DIM), dtype=np.float32)
    for cur, nxt in successor.items():
        W += np.outer(codes[nxt], codes[cur])
    return W

def kwta_vec(v, k):
    """k-winners-take-all cleanup -> sparse binary attractor state."""
    if k >= v.size:
        return (v > 0).astype(np.float32)
    thr_idx = np.argpartition(v, -k)[-k:]
    out = np.zeros_like(v)
    pos = thr_idx[v[thr_idx] > 0]      # only positive drive
    out[pos] = 1.0
    return out

def relatedness(W, codes, i, j):
    """
    Read-out (NO mouth): seed lane with code[i], run CA3 completion STEPS times,
    return the max overlap between any visited attractor state and code[j].
    Multi-step => transitive chaining i -> i+1 -> ... reaches j if a relation path exists.
    Overlap = normalized dot (cosine on binary sparse vectors).
    """
    x = codes[i].copy()
    cj = codes[j]
    cj_norm = np.linalg.norm(cj) + 1e-9
    best = 0.0
    for _ in range(STEPS):
        drive = W @ x
        x = kwta_vec(drive, KWTA)
        ov = float(x @ cj) / ((np.linalg.norm(x) + 1e-9) * cj_norm)
        if ov > best:
            best = ov
    return best

def form_cos(codes, i, j):
    a, b = codes[i], codes[j]
    return float(a @ b) / ((np.linalg.norm(a) + 1e-9) * (np.linalg.norm(b) + 1e-9))

def make_pairs():
    """held-out (non-adjacent, never directly stored) pairs, form-matched."""
    reachable, unreachable = [], []
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for a in range(CHAIN_LEN):
            for b in range(a + 2, CHAIN_LEN):        # gap>=2 => non-adjacent, forward reachable
                reachable.append((base + a, base + b))
    # unreachable: cross-chain pairs, matched count, random item codes (same distribution)
    n_needed = len(reachable)
    seen = set()
    while len(unreachable) < n_needed:
        i = int(rng.integers(N_ITEMS)); j = int(rng.integers(N_ITEMS))
        if chain_of(i) == chain_of(j):
            continue
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        unreachable.append((i, j))
    return reachable, unreachable

def eval_set(W, codes, pairs):
    return np.array([relatedness(W, codes, i, j) for i, j in pairs], dtype=np.float64)

def form_set(codes, pairs):
    return np.array([form_cos(codes, i, j) for i, j in pairs], dtype=np.float64)

def summarize(name, arr):
    return f"{name}: mean={arr.mean():.4f} std={arr.std():.4f} med={np.median(arr):.4f} n={len(arr)}"

def main():
    codes = make_codes()

    # true successor map (adjacent within chain)
    successor = {}
    for c in range(N_CHAINS):
        base = c * CHAIN_LEN
        for p in range(CHAIN_LEN - 1):
            successor[base + p] = base + p + 1

    reachable, unreachable = make_pairs()

    # --- FORM baseline (control: proves pair-classes are surface-form matched) ---
    fr = form_set(codes, reachable)
    fu = form_set(codes, unreachable)

    # --- STORE (real lane) ---
    W = build_store(codes, successor)
    sr = eval_set(W, codes, reachable)
    su = eval_set(W, codes, unreachable)

    # --- SHUFFLE ablation (destroy relation structure, keep same #associations) ---
    keys = list(successor.keys())
    vals = list(successor.values())
    perm = rng.permutation(len(vals))
    successor_sh = {keys[k]: vals[perm[k]] for k in range(len(keys))}
    Wsh = build_store(codes, successor_sh)
    shr = eval_set(Wsh, codes, reachable)
    shu = eval_set(Wsh, codes, unreachable)

    # per-gap breakdown for reachable (transitive distance)
    gaps = {}
    for (i, j), v in zip(reachable, sr):
        g = pos_in_chain(j) - pos_in_chain(i)
        gaps.setdefault(g, []).append(v)

    lines = []
    lines.append("# H_9129 L5 hippocampal associative-store transitive-inference (numpy DIRECTIONAL)")
    lines.append(f"seed={SEED} N_CHAINS={N_CHAINS} CHAIN_LEN={CHAIN_LEN} DIM={DIM} ACTIVE={ACTIVE} STEPS={STEPS} KWTA={KWTA}")
    lines.append("")
    lines.append("## FORM baseline (raw code cosine, no relations) -- must be reachable ~= unreachable")
    lines.append("  " + summarize("form_reachable  ", fr))
    lines.append("  " + summarize("form_unreachable", fu))
    lines.append(f"  form_gap (reach-unreach) = {fr.mean()-fu.mean():+.4f}")
    lines.append("")
    lines.append("## STORE lane (CA3 completion relatedness)")
    lines.append("  " + summarize("store_reachable  ", sr))
    lines.append("  " + summarize("store_unreachable", su))
    lines.append(f"  store_gap (reach-unreach) = {sr.mean()-su.mean():+.4f}")
    ratio = sr.mean() / (su.mean() + 1e-9)
    lines.append(f"  store_ratio reach/unreach = {ratio:.2f}x")
    lines.append("")
    lines.append("## per-gap reachable (transitive distance vs relatedness)")
    for g in sorted(gaps):
        a = np.array(gaps[g])
        lines.append(f"  gap={g}: mean={a.mean():.4f} n={len(a)}")
    lines.append("")
    lines.append("## SHUFFLE ablation (relation structure destroyed) -- reachable must collapse")
    lines.append("  " + summarize("shuf_reachable  ", shr))
    lines.append("  " + summarize("shuf_unreachable", shu))
    lines.append(f"  shuf_gap (reach-unreach) = {shr.mean()-shu.mean():+.4f}")
    lines.append("")

    # verdict logic
    floor_thr = 0.02
    form_tol  = 0.02      # |gap| below this => classes indistinguishable (form)
    store_gap = sr.mean() - su.mean()
    max_signal = max(sr.mean(), su.mean())
    if max_signal < floor_thr:
        verdict = "floor"
        fooled = None
    elif abs(store_gap) < form_tol or ratio < 1.5:
        verdict = "form-priming"
        fooled = True
    else:
        verdict = "BIND"
        fooled = False
    # form-matched sanity: FORM baseline gap should be ~0
    form_matched = abs(fr.mean() - fu.mean()) < form_tol
    # ablation collapse check: shuffle should remove the reachable lift
    shuf_collapsed = (shr.mean() - shu.mean()) < 0.5 * store_gap if store_gap > 0 else True

    lines.append("## VERDICT")
    lines.append(f"  verdict = {verdict}")
    lines.append(f"  fooled_by_form = {fooled}")
    lines.append(f"  form_matched (FORM baseline reach~=unreach) = {form_matched}")
    lines.append(f"  shuffle_collapsed (ablation removes lift) = {shuf_collapsed}")

    out = "\n".join(lines)
    print(out)
    with open(__file__.rsplit("/", 1)[0] + "/result.txt", "w") as f:
        f.write(out + "\n")

if __name__ == "__main__":
    main()
