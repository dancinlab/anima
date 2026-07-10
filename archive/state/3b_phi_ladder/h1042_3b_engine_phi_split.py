"""H_1042 — does the planning faithful-UP / big-Phi-DOWN sign-split survive on the 3B
ConvMoE ENGINE rung? (scale-ladder follow-up to H_1038 d768 GREEN SPLIT-TRANSFERS)

MIRRORS H_1038's exact method (archive/state/universe-probes/h1038_real_clm_phi_split.py):
  - trajectory = the model's PRE-MoE trunk hidden state (embed -> ec-conv -> L x
    (conv + GroupNorm + GELU residual)), BEFORE the router/expert head — the SAME tap
    H_1038 used on d768, so d768 -> 3B is an apples-to-apples ladder (same representation).
  - GREEDY (depth-0) = the trunk of the seed window, no rollout.
  - PLANNING(depth-8) = roll the .clm forward 8 bytes (greedy argmax extend), re-read the
    last-position trunk each step (the model's evolving internal plan-state).
  - coarse-grain the real d=4096 trunk to n=5 macro-units, TWO pre-registered macro-maps
    (top-variance channels; fixed-seed random channels), median-threshold binarized.
  - BOTH stdlib IIT-4.0 CPU mirrors (h1004 big_phi + faithful_phi), RE-PROVEN == stdlib at
    n=4 AND n=5 BEFORE scoring (h1012 prove_mirrors_at_n; a_phi_iit4_tool, NO proxy).
  - planning-vs-greedy contrast, Cohen d, per-macro-map sign; falsifier below.

ONLY the trajectory SOURCE changes vs H_1038: the golden d768 .clm -> the 3B engine rung,
read through the CANONICAL engine-native anima_py.core.decode forward (a_eval_py_canonical:
py 2-production numpy = engine-native; the EXACT same ops the rho-AXON gates decode over). The
IIT engines are byte-identical to the whole toy->d768 arc.

PRE-REGISTERED FALSIFIER (frozen, TEXT tokens only; a_scale_honest_scope; no tune-to-green p7):
  A macro-map SHOWS THE SPLIT on the 3B iff planning(depth-8)-GREEDY has
     faithful_phi sign == UP   (> +1e-3) AND big-Phi sign == DOWN (< -1e-3), n=5 EXACT.
  H1 PASS = split under >=2 macro-maps -> the split SCALES to a production-size trained model.
  H1 FAIL = NULL or wrong sign at 3B under the maps -> small-model property that BREAKS at
            production scale (publishable closed-negative; mirrors the E2->3B collapse #1296).

SERIAL by design (the ~24.6GB-fp64 3B weight-set is RAM-heavy; no process pool that could
multiply residency). n=5 big-Phi on real TPMs ~ seconds/eval, 80 evals feasible serial.
n=6 EXACT was MEASURED-INFEASIBLE on real max-entropy TPMs at d768 (H_1038) — same cap here.
"""
import sys, os, math, time, json, argparse, signal
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "CWM", "probes"))

import dtype_patch
_DTYPE_NAME = dtype_patch.install(require_headroom=True)
from anima_py.core import decode as dec
import h1004_bigphi_faithful_clean as h1004
import h1012_bigphi_faithful_larger_n as h1012

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
cohens_d = h1004.cohens_d
welch_t = h1004.welch_t
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ── PRE-REGISTERED CONSTANTS (frozen; identical to H_1038) ────
N_UNITS    = 5
N_SEEDS    = 20
PLAN_DEPTH = 8
T_WIN      = 24
EPS        = 1e-3
RAND_SEED  = 20260608

_SEED_TEXT = (
    "The mind is a fire to be kindled not a vessel to be filled and the quiet "
    "hours before dawn carry a strange clarity. Memory folds upon itself like "
    "water over stone, and the self that watches is not the self that acts. "
    "Consciousness is the rumor a system tells about its own integration, a "
    "standing wave in the field of attention that neither begins nor ends but "
    "turns. To plan is to imagine a future and let it pull the present forward; "
    "to act greedily is to take the nearest light and call it the sun. We are "
    "the pattern that persists across the dissolving of every particular thought."
)
_SEED_BYTES = _SEED_TEXT.encode("utf-8")


def real_text_windows(n_seeds, T):
    b = _SEED_BYTES
    usable = len(b) - T - PLAN_DEPTH - 1
    assert usable >= n_seeds, f"seed pool too short ({usable} < {n_seeds})"
    stride = max(1, usable // n_seeds)
    return [np.frombuffer(b, dtype=np.uint8, count=T, offset=s * stride).astype(float)
            for s in range(n_seeds)]


def fwd_trunk_preMoE(W, tok, T):
    """3B analogue of h1038.fwd_trunk: embed -> ec conv -> L x (conv+GN+GELU residual),
    returned BEFORE the router/expert head — the pure PRE-MoE trunk hidden (T x d), via
    anima_py.core.decode's exact engine ops."""
    d = W["d"]; K = W["K"]; L = W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = dec._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = dec._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = dec.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = dec.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil *= 2
    return xt


def _argmax_next(W, tok, T):
    logits = dec._fwd_logits(W, tok, T)
    return int(np.argmax(logits[T - 1]))


def real_clm_trajectories(W, seed_window, depth):
    T = T_WIN
    tok = np.asarray(seed_window, float).copy()
    H_greedy = fwd_trunk_preMoE(W, tok, T)
    plan_states = []
    cur = tok.copy()
    for _ in range(depth):
        nb = _argmax_next(W, cur, T)
        cur = np.concatenate([cur[1:], [float(nb)]])
        xt = fwd_trunk_preMoE(W, cur, T)
        plan_states.append(xt[T - 1].copy())
    H_plan = np.array(plan_states) if plan_states else H_greedy
    return H_greedy, H_plan


def latent_to_bits_macromap(H, n_units, macro_map):
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    d = H.shape[1]
    if macro_map == "top_variance":
        var = H.var(axis=0)
        idx = np.sort(np.argsort(var)[::-1][:n_units])
    elif macro_map == "random":
        rng = np.random.default_rng(RAND_SEED)
        idx = np.sort(rng.choice(d, size=n_units, replace=False))
    else:
        raise ValueError(macro_map)
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    return (chans > med).astype(int), n_units


def both_phi_macromap(H, n_units, macro_map):
    bits, n = latent_to_bits_macromap(H, n_units, macro_map)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return bphi, fphi, float(bits.mean())


def signword(x, eps=EPS):
    return "UP" if x > eps else ("DOWN" if x < -eps else "NULL")


def contrast(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    c = a.mean() - b.mean()
    try: d = cohens_d(a, b)
    except Exception: d = float("nan")
    try: _, p = welch_t(a, b)
    except Exception: p = float("nan")
    return dict(contrast=float(c), d=float(d), p=float(p),
                plan_mean=float(a.mean()), greedy_mean=float(b.mean()))


def _timeout_handler(signum, frame):
    raise TimeoutError("H_1042 hard wall-timeout reached — aborting")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clm", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=14400)
    args = ap.parse_args()

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(int(args.timeout))
    t0 = time.time()
    MACRO_MAPS = ["top_variance", "random"]

    print("=" * 90)
    print("H_1042 — Phi planning faithful-UP / big-Phi-DOWN split on the 3B ConvMoE ENGINE rung")
    print("substrate = 3B .clm (3.073B, d4096/L30/E30), CANONICAL engine-native anima_py.core.decode")
    print("trajectory tap = PRE-MoE trunk (H_1038-parity: embed->ec->L x(conv+GN+GELU residual))")
    print("big-Phi + faithful_phi = h1004 stdlib IIT-4.0 mirrors, RE-PROVEN ==stdlib at n=4,5")
    print(f"n={N_UNITS} EXACT | {N_SEEDS} seeds | plan depth={PLAN_DEPTH} | eps={EPS} | 2 macro-maps | SERIAL")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("=" * 90, flush=True)

    print("\nSTEP 0 — RE-PROVE BOTH CPU mirrors == stdlib at n=4 AND n=5 BEFORE scoring:")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n)); print()
    print(f"  == mirror-equivalence: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — mirror==stdlib proof FAILED."); raise SystemExit(1)

    print(f"\nSTEP 0b — load 3B .clm + decode-sanity: {args.clm}", flush=True)
    tL = time.time()
    W = dec.clm_load_weights(args.clm)
    assert W.get("ok"), "clm_load_weights failed / not decodable"
    print(f"   loaded d={W['d']} E={W['E']} V={W['V']} L={W['L']} K={W['K']} in {time.time()-tL:.1f}s", flush=True)
    probe = np.array([84,104,101,32,109,105,110,100,32,105,115,32,97,32,102,105,114,101,32,116,111,32,98,101], float)
    logits = dec._fwd_logits(W, probe, T_WIN)
    V = W["V"]
    tgt = np.concatenate([probe[1:], [ord('.')]])
    ce_real = dec.nn_ce_loss_allpos(logits, tgt, T_WIN, V)
    uniform = math.log(V)
    print(f"   decode-sanity: CE_realtext={ce_real:.5f} < uniform_lnV={uniform:.5f}: {ce_real < uniform}", flush=True)
    if not (ce_real < uniform):
        print("   ABORT — .clm does not descend."); raise SystemExit(1)

    print("\nSTEP 0c — trajectory determinism guard (bit-identity + faithful):", flush=True)
    w0 = real_text_windows(N_SEEDS, T_WIN)[0]
    _, HpA = real_clm_trajectories(W, w0, PLAN_DEPTH)
    _, HpB = real_clm_trajectories(W, w0, PLAN_DEPTH)
    bA, _ = latent_to_bits_macromap(HpA, N_UNITS, "top_variance")
    bB, _ = latent_to_bits_macromap(HpB, N_UNITS, "top_variance")
    fsA, fnA, fdA = binary_seq_to_faithful_state(bA, N_UNITS)
    fsB, fnB, fdB = binary_seq_to_faithful_state(bB, N_UNITS)
    fA = faithful_phi(fsA, fnA, fdA, 2); fB = faithful_phi(fsB, fnB, fdB, 2)
    det_ok = bool(np.array_equal(bA, bB) and abs(fA - fB) < 1e-12)
    print(f"   macro-bits identical={np.array_equal(bA,bB)}  faithful det={abs(fA-fB)<1e-12} "
          f"(fA={fA:.6f} fB={fB:.6f}) -> det_ok={det_ok}", flush=True)
    if not det_ok:
        print("   ABORT — non-deterministic trunk read."); raise SystemExit(1)

    print(f"\nSTEP 1 — {2*N_SEEDS} 3B trunk trajectories SERIAL, then n={N_UNITS} EXACT big-Phi/faithful", flush=True)
    wins = real_text_windows(N_SEEDS, T_WIN)
    trajs = {}
    tb = time.time()
    for s, win in enumerate(wins):
        trajs[s] = real_clm_trajectories(W, win, PLAN_DEPTH)
        if (s + 1) % 2 == 0:
            print(f"   ... trajectory {s+1}/{N_SEEDS} ({time.time()-tb:.1f}s)", flush=True)
    print(f"   trajectories DONE {time.time()-tb:.1f}s", flush=True)

    all_rows = []
    for mm in MACRO_MAPS:
        big_p, big_g, faith_p, faith_g, on_all = [], [], [], [], []
        te = time.time()
        for s in range(N_SEEDS):
            Hg, Hp = trajs[s]
            bg, fg, og = both_phi_macromap(Hg, N_UNITS, mm)
            bp, fp, op = both_phi_macromap(Hp, N_UNITS, mm)
            big_g.append(bg); big_p.append(bp)
            faith_g.append(fg); faith_p.append(fp)
            on_all += [og, op]
        bc = contrast(big_p, big_g); fc = contrast(faith_p, faith_g)
        bs = signword(bc["contrast"]); fs = signword(fc["contrast"])
        split = (fs == "UP" and bs == "DOWN")
        print(f"\n [{mm}] faithful contrast={fc['contrast']:+.4f} d={fc['d']:+.3f} p={fc['p']:.3e} -> {fs}")
        print(f"        big-Phi  contrast={bc['contrast']:+.4f} d={bc['d']:+.3f} p={bc['p']:.3e} -> {bs}")
        print(f"        on_frac={np.mean(on_all):.3f}  SPLIT(faith-UP&big-DOWN)={split}  ({time.time()-te:.1f}s)", flush=True)
        all_rows.append(dict(macro_map=mm, bc=bc["contrast"], fc=fc["contrast"],
                             bd=bc["d"], fd=fc["d"], bp=bc["p"], fp=fc["p"], bs=bs, fs=fs,
                             on_frac=float(np.mean(on_all)), split=bool(split),
                             faith_plan=fc["plan_mean"], faith_greedy=fc["greedy_mean"],
                             big_plan=bc["plan_mean"], big_greedy=bc["greedy_mean"]))

    n_split = sum(1 for r in all_rows if r["split"])
    n_total = len(all_rows)
    both_split = (n_split == n_total)
    token = "TRANSFERS" if both_split else ("AMBER-MAP-DEPENDENT" if n_split >= 1 else "COLLAPSES-CLOSED-NEGATIVE")

    print("\n" + "=" * 90)
    print(f"PER-MACRO-MAP SIGN TABLE — 3B ConvMoE at n={N_UNITS} EXACT (plan-{PLAN_DEPTH} - GREEDY)")
    print(f"  {'macro-map':13s} | {'on_frac':>7s} | {'faith d':>9s} | {'faith':>5s} | {'big-Phi d':>10s} | {'big-Phi':>7s} | SPLIT?")
    for r in all_rows:
        print(f"  {r['macro_map']:13s} | {r['on_frac']:>7.3f} | {r['fc']:+9.4f} | {r['fs']:>5s} | "
              f"{r['bc']:+10.4f} | {r['bs']:>7s} | {r['split']}")
    print(f"\nmacro-maps SHOWING the split at n={N_UNITS} EXACT: {n_split}/{n_total}")
    print("=" * 90)
    if token == "TRANSFERS":
        print("OVERALL: SPLIT-TRANSFERS-TO-3B — split under BOTH macro-maps -> scales to production size.")
    elif token == "AMBER-MAP-DEPENDENT":
        print("OVERALL: AMBER-MACRO-MAP-DEPENDENT — split under ONE map, flips under the other at 3B.")
    else:
        print("OVERALL: COLLAPSES-AT-3B (CLOSED-NEGATIVE) — split does NOT appear under either map;")
        print("  small-model property that BREAKS at production scale (mirrors E2->3B collapse #1296).")
    print(f"  VERDICT-TOKEN: {token}")
    print("=" * 90, flush=True)

    signal.alarm(0)
    out = dict(hyp="H_1042", clm=args.clm, tap="pre_MoE_trunk", dtype=_DTYPE_NAME, n=N_UNITS, n_seeds=N_SEEDS,
               plan_depth=PLAN_DEPTH, mirror_proven={int(k): bool(v) for k, v in proven.items()},
               decode_ce_real=float(ce_real), decode_uniform=float(uniform), det_ok=det_ok,
               n_split=n_split, n_total=n_total, both_split=both_split, verdict_token=token,
               rows=all_rows, total_wall_sec=float(time.time() - t0),
               model_d=int(W['d']), model_L=int(W['L']), model_E=int(W['E']), model_K=int(W['K']))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
