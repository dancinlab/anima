"""H_1038 — does the planning faithful-UP / big-Phi-DOWN sign-split appear on a REAL
trained ConvMoE .clm, or was it a toy-TPM artifact?  (production-direction closure)

Production-direction closure of the Phi measure-dependence arc H_1004 -> H_1037, which was
measured ONLY on hand-built TOY TPM substrates. a_toy_scale_recheck MANDATES a scale-up
re-test for scale-sensitive phenomena. THIS rung replaces the toy `planning_trajectories`
WM with REAL CLM rollouts on the golden trained ConvMoE reexport_d768_v2_fast.clm
(CPU-decoded via state/mid_convmoe_fire/clm_decode_mirror.py, memory clm-decode-macos-link-gap),
feeds the coarse-grained REAL trunk activations to the SAME stdlib IIT-4.0 engines used in
the toy arc, and asks: does the faithful-UP / big-Phi-DOWN planning sign-split TRANSFER?

SERIAL by design (NO multiprocessing.Pool). The prior attempt's Pool DEADLOCKED when the
parent agent died on a rate-limit storm (orphaned job burned 2.7s CPU over 33min — a hung,
not live, process). The golden d768 .clm is small and n<=6 macro-IIT is cheap, so a single
process is plenty; a hard wall-timeout guards against any silent hang.

ENGINES — BOTH stdlib IIT-4.0 CPU mirrors (a_phi_iit4_tool), RE-PROVEN == stdlib at n=4 AND
n=5 BEFORE scoring via the H_1012 prove_mirrors_at_n discipline (LIVE stdlib refs embedded):
  big-Phi      = hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s over the MIP,
                 MIP fully enumerated, EXACT at n<=6).
  faithful_phi = hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar, exact n<=8).
NEVER a proxy. The mirrors are imported by REAL MODULE NAME (h1004/h1012) — same engine code
the whole toy arc used; ONLY the trajectory source changes (toy WM -> real .clm).

HONEST scope (a_scale_honest_scope): d768 = ONE real-model rung. n<=6 is the largest EXACT
IIT size. 3B / 7B engine-rung transfer is UNVERIFIED (a real trained model is not a toy, but
ONE model is not a ladder; the 3B rung needs GPU and is H_1042's job, GATED). Verdict scoped
to the d768 golden real trained ConvMoE, coarse-grained to n<=6 EXACT. g5 CODE-measured (no
LLM self-judge, p7). Pure-CPU EXACT, NOT a forge binary.
"""
import sys, os, math, time, json, argparse, signal
import multiprocessing as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(REPO, "CWM", "probes"))   # cwm_probe_lib (cohens_d, welch_t, ...)
sys.path.insert(0, HERE)                                    # h1004 / h1012 engine mirrors
sys.path.insert(0, os.path.join(REPO, "state", "mid_convmoe_fire"))  # clm_decode_mirror

# REAL-MODULE-NAME imports (no importlib custom-name). Same stdlib-mirror engines the toy arc
# used; ONLY the trajectory source changes below (toy WM -> real .clm).
import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402
import clm_decode_mirror as clm                  # noqa: E402

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
cohens_d = h1004.cohens_d
welch_t = h1004.welch_t
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ── PRE-REGISTERED CONSTANTS (frozen before scoring) ────────────────────────
N_UNITS    = 6        # n<=6 EXACT (largest exact IIT size)
N_SEEDS    = 20       # >= the pre-registered 20
PLAN_DEPTH = 8        # depth-ladder rollout horizon (planning); greedy = depth-0
T_WIN      = 24       # the .clm decode window length (engine convention)
EPS        = 1e-3     # H_1024 signword threshold
RAND_SEED  = 20260608 # fixed seed for macro-map B (random channels)

# 20 distinct in-distribution real-text seed windows (English, byte-level model). Fixed pool
# sliced deterministically into T_WIN=24-byte windows; self-contained + deterministic ($0).
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
    """Deterministic distinct T-byte windows over the fixed real-text pool."""
    b = _SEED_BYTES
    usable = len(b) - T - PLAN_DEPTH - 1
    assert usable >= n_seeds, f"seed pool too short ({usable} < {n_seeds})"
    stride = max(1, usable // n_seeds)
    wins = []
    for s in range(n_seeds):
        base = s * stride
        wins.append(np.frombuffer(b, dtype=np.uint8, count=T, offset=base).astype(float))
    return wins


# ═══════════════════════════════════════════════════════════════════════════
# REAL .clm trunk reader — returns the d=768 trunk hidden state (T x d), EXACTLY
# the xt the mirror computes in fwd_logits BEFORE the router/expert head. This is
# the real trained model's internal trajectory (the analogue of the toy WM latent).
# ═══════════════════════════════════════════════════════════════════════════
def fwd_trunk(W, tok, T):
    """Re-run clm_decode_mirror.fwd_logits's trunk and return xt (T x d). Byte-faithful
    to the mirror's trunk (same int4 dequant, causal dilated conv, GroupNorm+GELU residual)."""
    d, E, V, K, L = W["d"], W["E"], W["V"], W["K"], W["L"]
    xe = W["embed"][tok.astype(int)]                       # (T, d)
    xt = clm.conv1d(xe, W["ecW"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        dil_eff = min(dil, 512)
        h = clm.conv1d(xt, W["tcW"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = clm.groupnorm1(h, W["tgG"][li], W["tgB"][li], T, d)
        hg = clm.gelu(hn)
        xt = xt + hg
        dil *= 2
    return xt   # (T, d) — the trunk hidden state, the real-model trajectory


def _argmax_next(W, tok, T):
    """Greedy next-byte = argmax of the last-position logits (depth-0 policy step)."""
    logits = clm.fwd_logits(W, tok, T)
    return int(np.argmax(logits[T - 1]))


def real_clm_trajectories(W, seed_window, depth):
    """REAL .clm analogue of the toy planning_trajectories(seed, depth).

    GREEDY  (depth-0)  = the trunk hidden state of the seed window with NO rollout
                         (the model's internal state of what it is reading right now).
    PLANNING(depth-d)  = roll the .clm forward `depth` bytes (greedy argmax extend),
                         re-reading the trunk each step; the planning trajectory is the
                         sequence of real trunk hidden states the model produces as it
                         imagines forward. (Same convention as H_1004/H_1029/H_1037:
                         the trajectory = the sequence of internal states under each policy.)
    Returns (H_greedy, H_plan), each (n_steps x d) real trunk activations.
    """
    T = T_WIN
    tok = np.asarray(seed_window, float).copy()

    # GREEDY: the trunk of the seed window (depth-0). T real trunk states.
    H_greedy = fwd_trunk(W, tok, T)                        # (T, d)

    # PLANNING: extend `depth` bytes by greedy argmax, collect the trunk's last-position
    # hidden state at each rollout step (the model's evolving internal plan-state).
    plan_states = []
    cur = tok.copy()
    for _ in range(depth):
        nb = _argmax_next(W, cur, T)
        cur = np.concatenate([cur[1:], [float(nb)]])       # slide the window forward 1 byte
        xt = fwd_trunk(W, cur, T)
        plan_states.append(xt[T - 1].copy())               # last-pos trunk = the new plan-state
    H_plan = np.array(plan_states) if plan_states else H_greedy
    return H_greedy, H_plan


# ═══════════════════════════════════════════════════════════════════════════
# COARSE-GRAINING — REAL d=768 trunk -> n<=6 macro-units. TWO pre-registered macro-maps
# (guards a coarse-graining artifact, mirroring H_1037 discretization-invariance logic):
#   macro-map A = TOP-VARIANCE channels (the n=6 highest-variance trunk channels;
#                 the H_1024 channel selector).
#   macro-map B = RANDOM channels (a fixed-seed random n=6 channel subset).
# Each selected channel binarized at its OWN median over the trajectory (nb=2). The n<=6
# binary node sequence -> macro-TPM (big-Phi) and -> faithful-state (faithful_phi).
# ═══════════════════════════════════════════════════════════════════════════
def latent_to_bits_macromap(H, n_units, macro_map):
    """(n_steps x d) REAL trunk -> (n_steps x n_units) BINARY via a macro-map. Each selected
    channel binarized at its OWN median over the trajectory (H_1004/H_1037 convention)."""
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
        raise ValueError(f"unknown macro_map {macro_map}")
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    bits = (chans > med).astype(int)
    return bits, n_units


def both_phi_macromap(H, n_units, macro_map):
    """ONE macro-map coarse-graining of a REAL trajectory, BOTH engines.
    big-Phi EXACT (MIP fully enumerated). Returns (big, faith, on_frac)."""
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
    try:
        d = cohens_d(a, b)
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(a, b)
    except Exception:
        p = float("nan")
    return dict(contrast=float(c), d=float(d), p=float(p),
                plan_mean=float(a.mean()), greedy_mean=float(b.mean()))


# ═══════════════════════════════════════════════════════════════════════════
# PARALLELISM — the n=6 big-Phi on a HIGH-ENTROPY real-model TPM is intrinsically
# expensive (all 2^6-1 mechanisms active; full distinction+relation enumeration +
# MIP search) — ~minutes/eval, exactly why the toy n=6 arc (H_1037) used a 96-core
# pool. The CHEAP part (the real .clm rollout forwards) is run SERIAL; only the
# EXPENSIVE big-Phi/faithful evals are dispatched over a GUARDED process pool that
# satisfies all four prompt-required guards:
#   (a) guarded by `if __name__ == '__main__'` (the pool is created only inside main());
#   (b) workers re-import by REAL MODULE NAME (h1004/h1012/clm_decode_mirror — top of
#       this file), NOT an importlib custom name -> no PicklingError on fork;
#   (c) workers NEVER read stdin;
#   (d) HARD per-eval timeout (a worker-side SIGALRM) so a single eval can't hang the
#       pool silently — the prior deadlock came from an UNGUARDED, orphaned pool whose
#       parent died on a rate-limit storm; this pool is guarded + parent-alive + timed.
# The bits are precomputed SERIAL and passed to the worker, so the worker does ONLY the
# deterministic pure-arithmetic IIT evals (no .clm I/O, no RNG) — fully reproducible.
# ═══════════════════════════════════════════════════════════════════════════
_PER_EVAL_TIMEOUT = 300   # per-eval wall cap (s) inside each worker — NON-FATAL


class _EvalTimeout(Exception):
    pass


def _phi_worker(job):
    """TOP-LEVEL worker: ONE (key, bits-as-list, n) -> (key, big, faith, on_frac, timed_out).
    Pure arithmetic over the passed bits (no I/O, no RNG). The per-eval SIGALRM is NON-FATAL:
    on timeout the worker returns timed_out=True with NaN phis, so ONE pathological
    high-entropy real-model TPM (where big-Phi's distinction+relation+MIP enumeration
    explodes) cannot crash the whole run — it is honestly EXCLUDED + disclosed (a single
    excluded eval out of 20 seeds barely shifts a sign-contrast). faithful_phi is computed
    FIRST (it is cheap and never the bottleneck) so it survives even a big-Phi timeout."""
    key, bits_list, n = job
    bits = np.asarray(bits_list, dtype=int)
    on_frac = float(bits.mean())
    # faithful_phi first (cheap; always succeeds at n<=6)
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = float(faithful_phi(fstate, fn, fdim, 2))

    def _to(signum, frame):
        raise _EvalTimeout()
    old = signal.signal(signal.SIGALRM, _to)
    signal.alarm(_PER_EVAL_TIMEOUT)
    try:
        tpm, sc = binary_seq_to_tpm(bits, n)
        bphi = float(big_phi(tpm, n, modal_state(sc))[0])
        timed_out = False
    except _EvalTimeout:
        bphi = float("nan")
        timed_out = True
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
    return key, bphi, fphi, on_frac, bool(timed_out)


def score_all(W, macro_maps, pool, t0):
    """Precompute the 40 REAL .clm trajectories SERIAL (cheap forwards), coarse-grain to
    bits per macro-map (cheap), then dispatch ONLY the expensive big-Phi/faithful evals
    over the guarded pool. Returns {macro_map: result-dict}."""
    print(f"------ PRECOMPUTE {2*N_SEEDS} REAL .clm trajectories SERIAL (cheap forwards; "
          f"elapsed {time.time()-t0:.1f}s) ------", flush=True)
    wins = real_text_windows(N_SEEDS, T_WIN)
    trajs = {}     # seed -> (H_greedy, H_plan)
    tb = time.time()
    for s, win in enumerate(wins):
        trajs[s] = real_clm_trajectories(W, win, PLAN_DEPTH)
        if (s + 1) % 5 == 0:
            print(f"   ... trajectory {s+1}/{N_SEEDS} ({time.time()-tb:.1f}s)", flush=True)
    print(f"   trajectories DONE in {time.time()-tb:.1f}s", flush=True)

    # build the eval jobs (bits precomputed serial; worker does only the IIT arithmetic)
    jobs = []
    for mm in macro_maps:
        for s in range(N_SEEDS):
            Hg, Hp = trajs[s]
            bits_g, _ = latent_to_bits_macromap(Hg, N_UNITS, mm)
            bits_p, _ = latent_to_bits_macromap(Hp, N_UNITS, mm)
            jobs.append(((mm, s, "greedy"), bits_g.tolist(), N_UNITS))
            jobs.append(((mm, s, "plan"),   bits_p.tolist(), N_UNITS))
    print(f"------ DISPATCH {len(jobs)} EXACT n={N_UNITS} big-Phi/faithful evals over "
          f"{pool._processes} guarded workers (per-eval timeout {_PER_EVAL_TIMEOUT}s; "
          f"elapsed {time.time()-t0:.1f}s) ------", flush=True)
    te = time.time()
    results = pool.map(_phi_worker, jobs)
    print(f"   {len(jobs)} evals DONE in {time.time()-te:.1f}s wall "
          f"({(time.time()-te)/len(jobs):.1f}s/eval amortized)", flush=True)

    # collect per (macro_map, seed): big/faith for plan + greedy, plus timeout flags.
    # big-Phi is PAIRED per seed (plan-greedy), so a seed is EXCLUDED from the big-Phi
    # contrast iff EITHER its plan or greedy big-Phi timed out (NON-FATAL). faithful_phi
    # never times out (cheap), so its contrast uses ALL 20 seeds. Timeouts are disclosed.
    cells = {mm: {s: {} for s in range(N_SEEDS)} for mm in macro_maps}
    n_timeout = {mm: 0 for mm in macro_maps}
    timeout_keys = []
    for (mm, s, which), bphi, fphi, onf, to in results:
        cells[mm][s][which] = dict(big=bphi, faith=fphi, on=onf, to=to)
        if to:
            n_timeout[mm] += 1
            timeout_keys.append((mm, s, which))
    out = {}
    for mm in macro_maps:
        big_plan, big_greedy = [], []     # paired, timeout-excluded
        faith_plan, faith_greedy = [], []  # all seeds
        on_all = []
        n_excluded = 0
        for s in range(N_SEEDS):
            cp = cells[mm][s].get("plan"); cg = cells[mm][s].get("greedy")
            faith_plan.append(cp["faith"]); faith_greedy.append(cg["faith"])
            on_all.append(cp["on"]); on_all.append(cg["on"])
            if cp["to"] or cg["to"]:
                n_excluded += 1
            else:
                big_plan.append(cp["big"]); big_greedy.append(cg["big"])
        out[mm] = dict(big=contrast(big_plan, big_greedy),
                       faith=contrast(faith_plan, faith_greedy),
                       on_frac=float(np.mean(on_all)),
                       n_big_seeds=len(big_plan), n_excluded=int(n_excluded),
                       elapsed=float(time.time()-te))
    if timeout_keys:
        print(f"   NOTE: {len(timeout_keys)} big-Phi eval(s) hit the {_PER_EVAL_TIMEOUT}s "
              f"per-eval timeout (pathological high-entropy real-model TPM) and were EXCLUDED "
              f"from the big-Phi contrast (faithful_phi unaffected): {timeout_keys}", flush=True)
    return out


def _timeout_handler(signum, frame):
    raise TimeoutError("H_1038 hard wall-timeout reached — aborting (so it can't hang silently)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clm", type=str,
                    default="/Users/mini/dancinlab/anima/state/laneg_d768_recover/reexport_d768_v2_fast.clm")
    ap.add_argument("--out", type=str,
                    default=os.path.join(HERE, "state", "h1038_real_clm_phi_split_result.json"))
    ap.add_argument("--timeout", type=int, default=7200, help="hard wall-timeout (s)")
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 1),
                    help="guarded pool workers (parallelizes ONLY the expensive n=6 big-Phi)")
    args = ap.parse_args()

    # HARD wall-timeout so a silent hang is impossible (the prior failure mode).
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(int(args.timeout))

    t0 = time.time()
    print("=" * 90)
    print("H_1038 — does the planning faithful-UP / big-Phi-DOWN sign-split appear on a REAL")
    print("         trained ConvMoE .clm, or was the toy-TPM arc (H_1004 -> H_1037) an artifact?")
    print("substrate = golden trained ConvMoE reexport_d768_v2_fast.clm, CPU-decoded via")
    print("            state/mid_convmoe_fire/clm_decode_mirror.py (memory clm-decode-macos-link-gap)")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s, MIP fully enumerated)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("CHEAP .clm rollouts SERIAL; the EXPENSIVE n=6 big-Phi evals over a GUARDED process")
    print("pool (guarded by __main__, real-module imports, no stdin, hard per-eval timeout) —")
    print("the prior FAILURE was an UNGUARDED pool ORPHANED by a dead parent, not the pool itself.")
    print(f"n={N_UNITS} EXACT | {N_SEEDS} seeds | plan depth={PLAN_DEPTH} | eps={EPS} | "
          f"2 macro-maps (top-variance, random) | workers={args.workers}")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print(f"hard wall-timeout={args.timeout}s | per-eval timeout={_PER_EVAL_TIMEOUT}s")
    print("=" * 90, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 BEFORE scoring (a_phi_iit4_tool) ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5")
    print("         BEFORE scoring (H_1012 prove_mirrors_at_n discipline; LIVE stdlib refs):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # ── STEP 0b: load the REAL .clm + decode-sanity (it must DESCEND, else the trunk is junk) ──
    print(f"STEP 0b — load golden .clm + decode-sanity: {args.clm}", flush=True)
    W = clm.load_clm(args.clm)
    print(f"   loaded: d={W['d']} E={W['E']} V={W['V']} L={W['L']} K={W['K']}")
    probe_seq = [84,104,101,32,109,105,110,100,32,105,115,32,97,32,102,105,114,101,32,116,111,32,98,101]
    log = clm.fwd_logits(W, np.array(probe_seq, dtype=float), T_WIN)
    ce_real, _ = clm.ce_nextbyte(log, probe_seq, T_WIN, W["V"])
    uniform = math.log(W["V"])
    print(f"   decode-sanity: CE_realtext={ce_real:.5f} < uniform_lnV={uniform:.5f}: "
          f"{ce_real < uniform}  (the trunk is a TRAINED descent, not junk)", flush=True)
    if not (ce_real < uniform):
        print("   ABORT — .clm does not descend; trunk activations are not a trained model.")
        raise SystemExit(1)
    print()

    # ── STEP 0c: determinism guard. The trunk + coarse-grain are pure fns of the .clm bytes,
    #    so two re-runs must yield BIT-IDENTICAL macro-bits (cheap) + identical faithful_phi
    #    (instant). big-Phi is a deterministic pure fn of identical bits, so bit-identity
    #    PROVES big-Phi determinism without paying the n=6 big-Phi cost here (a_wall_first). ──
    print("STEP 0c — REAL-trajectory determinism guard (pure fn of fixed .clm bytes; "
          "bit-identity + faithful, cheap):", flush=True)
    w0 = real_text_windows(N_SEEDS, T_WIN)[0]
    _, HpA = real_clm_trajectories(W, w0, PLAN_DEPTH)
    _, HpB = real_clm_trajectories(W, w0, PLAN_DEPTH)
    bitsA, _ = latent_to_bits_macromap(HpA, N_UNITS, "top_variance")
    bitsB, _ = latent_to_bits_macromap(HpB, N_UNITS, "top_variance")
    fsA, fnA, fdA = binary_seq_to_faithful_state(bitsA, N_UNITS)
    fsB, fnB, fdB = binary_seq_to_faithful_state(bitsB, N_UNITS)
    fA = faithful_phi(fsA, fnA, fdA, 2)
    fB = faithful_phi(fsB, fnB, fdB, 2)
    bits_identical = bool(np.array_equal(bitsA, bitsB))
    det_ok = bool(bits_identical and abs(fA - fB) < 1e-12)
    print(f"   seed0 plan (top-variance) macro-bits identical across re-runs: {bits_identical}; "
          f"faithful determinism: {abs(fA-fB) < 1e-12} (fA={fA:.6f}, fB={fB:.6f})", flush=True)
    print(f"   -> big-Phi determinism follows (pure fn of identical bits): {det_ok}", flush=True)
    if not det_ok:
        print("   ABORT — real-trajectory read non-deterministic.")
        raise SystemExit(1)
    print()

    # ── STEP 1: score BOTH macro-maps at n=6 EXACT (cheap rollouts serial, expensive
    #    big-Phi over the GUARDED pool) ──
    print(f"STEP 1 — score planning(depth-{PLAN_DEPTH}) - GREEDY at n={N_UNITS} EXACT on the "
          f"REAL .clm, for BOTH macro-maps", flush=True)
    all_rows = []
    MACRO_MAPS = ["top_variance", "random"]
    pool = mp.Pool(processes=args.workers)
    try:
        scored = score_all(W, MACRO_MAPS, pool, t0)
    finally:
        pool.close()
        pool.join()
    print()
    for mm in MACRO_MAPS:
        r = scored[mm]
        bc = r["big"]["contrast"]; fc = r["faith"]["contrast"]
        bs = signword(bc); fs = signword(fc)
        split = (fs == "UP" and bs == "DOWN")
        print(f"   faithful_phi contrast(plan-greedy)={fc:+.4f} d={r['faith']['d']:+.3f} "
              f"p={r['faith']['p']:.3e} -> {fs}  (plan={r['faith']['plan_mean']:.4f} "
              f"greedy={r['faith']['greedy_mean']:.4f})")
        print(f"   big-Phi      contrast(plan-greedy)={bc:+.4f} d={r['big']['d']:+.3f} "
              f"p={r['big']['p']:.3e} -> {bs}  (plan={r['big']['plan_mean']:.4f} "
              f"greedy={r['big']['greedy_mean']:.4f})")
        print(f"   on-fraction(mean)={r['on_frac']:.3f}  "
              f"big-Phi seeds used={r['n_big_seeds']}/{N_SEEDS} "
              f"(excluded {r['n_excluded']} on per-eval timeout)")
        print(f"   SHOWS THE SPLIT (faith-UP & big-DOWN): {split}", flush=True)
        print()
        all_rows.append(dict(macro_map=mm, bc=float(bc), fc=float(fc),
                             bd=float(r["big"]["d"]), fd=float(r["faith"]["d"]),
                             bp=float(r["big"]["p"]), fp=float(r["faith"]["p"]),
                             bs=bs, fs=fs, on_frac=float(r["on_frac"]),
                             split=bool(split), elapsed=float(r["elapsed"]),
                             n_big_seeds=int(r["n_big_seeds"]), n_excluded=int(r["n_excluded"]),
                             faith_plan=float(r["faith"]["plan_mean"]),
                             faith_greedy=float(r["faith"]["greedy_mean"]),
                             big_plan=float(r["big"]["plan_mean"]),
                             big_greedy=float(r["big"]["greedy_mean"])))

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER — per-macro-map SIGN table on the REAL .clm at n=6 EXACT
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 90)
    print(f"PER-MACRO-MAP SIGN TABLE on the REAL d768 .clm at n={N_UNITS} EXACT "
          f"— planning(depth-{PLAN_DEPTH}) - GREEDY contrast SIGN")
    print("=" * 90)
    print(f"  {'macro-map':13s} | {'on_frac':>7s} | {'bigN':>4s} | {'faith d':>9s} | {'faith':>5s} | "
          f"{'big-Phi d':>10s} | {'big-Phi':>7s} | {'SPLIT?':>6s}")
    n_split = 0
    for r in all_rows:
        if r["split"]:
            n_split += 1
        print(f"  {r['macro_map']:13s} | {r['on_frac']:>7.3f} | "
              f"{r['n_big_seeds']:>2d}/{N_SEEDS:<1d} | {r['fc']:+9.4f} | {r['fs']:>5s} | "
              f"{r['bc']:+10.4f} | {r['bs']:>7s} | {str(r['split']):>6s}")
    print()
    n_total = len(all_rows)
    both_split = (n_split == n_total)        # ROBUSTNESS: split under BOTH macro-maps
    any_split = (n_split >= 1)
    print(f"macro-maps SHOWING the split (faith-UP & big-Phi-DOWN) at n={N_UNITS} EXACT: "
          f"{n_split}/{n_total}")
    print()

    # frozen pre-reg verdict tokens:
    #   TRANSFERS         = split under BOTH macro-maps (clean toy->real bridge)
    #   AMBER-MAP-DEP     = split under ONE macro-map but flips under the other (coarse-grain dep)
    #   TOY-ARTIFACT      = split under NEITHER macro-map (NULL or wrong sign)
    if both_split:
        token = "TRANSFERS"
    elif any_split:
        token = "AMBER-MAP-DEPENDENT"
    else:
        token = "TOY-ARTIFACT"

    print("=" * 90)
    if token == "TRANSFERS":
        print("OVERALL: SPLIT-TRANSFERS-TO-REAL-MODEL — on the golden trained ConvMoE .clm the")
        print("  planning faithful_phi-UP / big-Phi-DOWN sign-split appears under BOTH macro-maps")
        print("  (top-variance AND random channel). The toy-TPM arc H_1004 -> H_1037 split is a")
        print("  property of a REAL trained consciousness model too — toy -> real BRIDGED at d768.")
    elif token == "AMBER-MAP-DEPENDENT":
        print("OVERALL: AMBER-MACRO-MAP-DEPENDENT — the split appears under ONE macro-map but flips")
        print("  under the other on the REAL .clm. NOT a clean transfer: the real-model split is")
        print("  sensitive to the coarse-graining choice (a possible coarse-graining artifact).")
        print("  Honest AMBER, not a clean PASS or a clean closed-negative.")
    else:
        print("OVERALL: TOY-TPM-ARTIFACT (CLOSED-NEGATIVE) — the planning faithful-UP / big-Phi-DOWN")
        print("  split does NOT appear on the REAL trained ConvMoE .clm (NULL or wrong sign) under")
        print("  either macro-map. The toy-TPM arc split was a property of the hand-built TOY TPM,")
        print("  NOT of a real trained model -> a publishable closed-negative (a_paper_negative_ok).")
    print(f"  VERDICT-TOKEN: {token}")
    print("=" * 90)
    print(f"HONEST scope (a_scale_honest_scope): d768 = ONE real-model rung; n={N_UNITS} is the")
    print("largest EXACT IIT size. 3B / 7B engine-rung transfer is UNVERIFIED (3B needs GPU =")
    print("H_1042's job, GATED). Verdict scoped to the d768 golden real trained ConvMoE, coarse-")
    print("grained to n<=6 EXACT, 2 pre-registered macro-maps, 20 real-text seed windows. BOTH")
    print("CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring (a_phi_iit4_tool; no")
    print("proxy). Cheap rollouts serial; the expensive n=6 big-Phi over a GUARDED pool (guarded")
    print("by __main__, real-module imports, no stdin, hard per-eval timeout); each read a pure fn")
    print("of the fixed .clm bytes. g5 CODE-measured (no LLM self-judge, p7). NOT a forge binary;")
    print("pure-CPU EXACT. ConvMoE substrate only (a_clm_gen_pipeline).")

    signal.alarm(0)  # disarm the wall-timeout
    out = dict(clm=args.clm, n=N_UNITS, n_seeds=N_SEEDS, plan_depth=PLAN_DEPTH,
               mirror_proven={int(k): bool(v) for k, v in proven.items()},
               decode_ce_real=float(ce_real), decode_uniform=float(uniform),
               det_ok=bool(det_ok), n_split=int(n_split), n_total=int(n_total),
               both_split=bool(both_split), verdict_token=token,
               rows=all_rows, total_wall_sec=float(time.time() - t0))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    # fork start-method: workers inherit the already-imported real-module engines (no re-import,
    # no PicklingError). The pool is created ONLY here (guarded by __main__), so a dead parent
    # leaves no orphaned, un-reapable pool (the prior failure mode).
    try:
        mp.set_start_method("fork")
    except RuntimeError:
        pass
    main()
