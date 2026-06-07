"""H_1033 — which TASK-STRUCTURAL property predicts the big-Phi-DOWN (split-enabling) half?

RESIDUAL OF H_1023
------------------
H_1023 (🔴 SPLIT-TASK-LOCAL) found the redundancy-driven faithful-UP / big-Phi-DOWN split is
NOT substrate-general: on a generic coupled-copy TPM substrate big-Phi went UP under the
redundancy intervention (RAISES, +4.42), not DOWN. The WB redundancy-margin stayed general,
but the SIGN of big-Phi did not flip the way it does on the planning-control task. So the
split is a joint property of (the two Phi measures) x (the TASK structure). OPEN: WHICH task
structural property makes the big-Phi-DOWN half appear?

THE H_1033 PRE-REGISTERED TEST (frozen 2026-06-08 in H_1033_split_task_property.md)
----------------------------------------------------------------------------------
FROZEN FAMILY of 5 n=4 task substrates, each an explicit frozen intervention vs the SAME
H_1023 independent-noisy-bits baseline (run_base):
  1. modular-planning : 2 independent coupled sub-modules {0,1},{2,3} (factorizes -> expect bigΦ DOWN)
  2. coupled-chain    : directed ring 0->1->2->3->0 (integrated, no single driver)
  3. random-TPM       : frozen random dense stochastic channel (generic, no clean factor)
  4. xor-parity       : each unit = XOR of the other three (H_1023 synergy control; non-decomposable)
  5. copy-channel     : H_1023 coupled-copy (one shared driver floods all -> made bigΦ go UP)

FROZEN structural predictor Δ_DEC (decomposability) — from the mirror-built MI matrix, the
best-balanced-bipartition normalized cut: over the 3 balanced 2|2 bipartitions, cross = sum of
cross-partition MI, within = sum of within-partition MI; cross_min = cheapest cut; DEC =
(within - cross_min)/(within + cross_min + eps). Δ_DEC = DEC(intervention) - DEC(baseline).
POSITIVE Δ_DEC = intervention made the system MORE decomposable. NOT a Phi proxy (Phi from the
stdlib engine mirrors only, a_phi_iit4_tool). PID red/syn totals recorded as secondary cross-check.

FROZEN separation rule: label a task bigΦ-DOWN iff its big-Phi contrast < -eps (eps=1e-3).
PASS = TASK-PROPERTY-PREDICTS-SPLIT : Δ_DEC PERFECTLY rank-separates bigΦ-DOWN from bigΦ-NOT-DOWN
  (min Δ_DEC over DOWN > max Δ_DEC over NOT-DOWN), direction matching the hypothesis (DOWN = the
  more-decomposable, higher-Δ_DEC tasks). Requires >=1 task in each class else INCONCLUSIVE.
FAIL = NO-TASK-PREDICTOR : the two classes interleave in Δ_DEC (closed-negative, a_paper_negative_ok).

REUSE: the two stdlib IIT-4.0 engine CPU mirrors + matched discretization reads + H_1012
prove_mirrors_at_n proof + WB I_min PID + run_base — ALL imported VERBATIM via the H_1023 module.
This file adds ONLY the 4 extra frozen task channels + the frozen Δ_DEC predictor + the test.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT; big-Phi
super-exponential so n=4 is the rung for the full family x 30 seeds. Δ_DEC exact + deterministic.
Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU. g5 CODE-measured (no LLM
self-judge, p7), a_phi_iit4_tool (REAL stdlib engines, no proxy).
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Import the H_1023 module VERBATIM: it re-exports (via its H_1017->H_1014->H_1004 chain)
#    both engine mirrors, the matched discretization reads, the H_1012 equivalence proof, the
#    WB I_min PID, AND the frozen run_base / run_redundancy / run_synergy channels + N_* knobs. ──
import importlib.util as _ilu
_h1023_path = os.path.join(HERE, "h1023_phi_split_substrate_generality.py")
_spec = _ilu.spec_from_file_location("h1023", _h1023_path)
_h1023 = _ilu.module_from_spec(_spec)
_src = open(_h1023_path).read().replace('if __name__ == "__main__":\n    main()', "")
# REPAIR (read-only to shared tree): the committed h1017 module re-exports faithful_phi_from_mi
# but NOT a top-level `faithful_phi`, so h1023 line `faithful_phi = _h1017.faithful_phi` raises
# AttributeError on import today. faithful_phi lives one hop deeper (h1017 holds _h1014, which
# re-exports faithful_phi from h1004). Rewrite ONLY that one reference in the in-memory source
# string (we do not edit the shared file) so the verbatim engine import chain loads.
_src = _src.replace("faithful_phi = _h1017.faithful_phi",
                    "faithful_phi = _h1017._h1014.faithful_phi")
exec(compile(_src, _h1023_path, "exec"), _h1023.__dict__)

prove_mirrors_at_n = _h1023.prove_mirrors_at_n
big_phi = _h1023.big_phi
faithful_phi = _h1023.faithful_phi
build_mi_matrix = _h1023.build_mi_matrix
faithful_phi_from_mi = _h1023.faithful_phi_from_mi
binary_seq_to_tpm = _h1023.binary_seq_to_tpm
modal_state = _h1023.modal_state
binary_seq_to_faithful_state = _h1023.binary_seq_to_faithful_state
pid_system = _h1023.pid_system
_pid_two_source = _h1023._pid_two_source
cohens_d = _h1023.cohens_d
welch_t = _h1023.welch_t
run_base = _h1023.run_base
run_redundancy = _h1023.run_redundancy   # == copy-channel
run_synergy = _h1023.run_synergy         # == xor-parity
_noise_flip = _h1023._noise_flip

N_UNITS = _h1023.N_UNITS                  # 4
N_STEPS = _h1023.N_STEPS                  # 200
N_SEEDS = _h1023.N_SEEDS                  # 30
NOISE = _h1023.NOISE                      # 0.10
assert N_UNITS == 4, "frozen n=4 family"

# ═══════════════════════════════════════════════════════════════════════════
# FROZEN ADDITIONAL TASK CHANNELS (3 new; copy-channel + xor-parity reused from H_1023).
# Each shares the SAME seed base (50_000 + seed) as run_base -> matched-baseline contrast.
# ═══════════════════════════════════════════════════════════════════════════
def run_modular(seed, n_steps=N_STEPS):
    """modular-planning intervention: 2 independent coupled sub-modules {0,1} and {2,3}, the two
    modules causally DECOUPLED. Within each module the two units relax toward a SHARED module coin
    (so the module is internally coupled / a unit), but the modules are independent of each other.
    Factorizes cleanly into 2 parts -> expected MORE decomposable -> big-Phi DOWN."""
    rng = np.random.default_rng(50_000 + seed)
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        coin_a = int(rng.random() > 0.5)   # shared driver for module {0,1}
        coin_b = int(rng.random() > 0.5)   # independent shared driver for module {2,3}
        bits[t, 0] = _noise_flip(rng, coin_a)
        bits[t, 1] = _noise_flip(rng, coin_a)
        bits[t, 2] = _noise_flip(rng, coin_b)
        bits[t, 3] = _noise_flip(rng, coin_b)
    return bits

def run_chain(seed, n_steps=N_STEPS):
    """coupled-chain intervention: directed ring 0->1->2->3->0; each unit is a noisy copy of its
    predecessor's PREVIOUS bit. Integrated around a cycle, NO single shared driver -> intermediate
    integration (no clean 2|2 factorization)."""
    rng = np.random.default_rng(50_000 + seed)
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        prev = bits[t - 1]
        for u in range(N_UNITS):
            src = prev[(u - 1) % N_UNITS]   # predecessor in the ring
            bits[t, u] = _noise_flip(rng, int(src))
    return bits

# A FROZEN random dense channel structure (drawn ONCE here, not per-seed) so the substrate is
# fixed across seeds; only the base-noise / seed schedule varies. Frozen RNG seed = 99_991.
_RTPM_RNG = np.random.default_rng(99_991)
# each next-bit u is a noisy majority-vote over a frozen random non-empty subset of current bits.
_RTPM_SUBSETS = []
for _u in range(N_UNITS):
    while True:
        mask = (_RTPM_RNG.random(N_UNITS) > 0.5).astype(int)
        if mask.sum() >= 1:
            break
    _RTPM_SUBSETS.append(np.flatnonzero(mask))

def run_random_tpm(seed, n_steps=N_STEPS):
    """random-TPM intervention: each next-bit = noisy majority of a FROZEN random subset of current
    bits (subsets drawn once, seed 99_991). Generic dense channel, no clean factorization."""
    rng = np.random.default_rng(50_000 + seed)
    bits = np.zeros((n_steps, N_UNITS), dtype=int)
    bits[0] = (rng.random(N_UNITS) > 0.5).astype(int)
    for t in range(1, n_steps):
        prev = bits[t - 1]
        for u in range(N_UNITS):
            sub = _RTPM_SUBSETS[u]
            vote = int(prev[sub].sum() * 2 >= len(sub))   # majority (ties -> 1)
            bits[t, u] = _noise_flip(rng, vote)
    return bits

# ═══════════════════════════════════════════════════════════════════════════
# FROZEN structural predictor Δ_DEC (decomposability) — from the mirror-built MI matrix.
# ═══════════════════════════════════════════════════════════════════════════
_BAL_BIPARTS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]  # all 3 balanced 2|2 cuts

def _decomposability(mi):
    """DEC = (within - cross_min)/(within + cross_min + eps) over the BEST (cheapest-cut) balanced
    2|2 bipartition of the 4 units. HIGH = factors cleanly (cheap cut). mi = symmetric MI matrix."""
    eps = 1e-12
    best = None  # (cross_weight, within_weight) for the cheapest cut
    for A, B in _BAL_BIPARTS:
        cross = mi[A[0], B[0]] + mi[A[0], B[1]] + mi[A[1], B[0]] + mi[A[1], B[1]]
        within = mi[A[0], A[1]] + mi[B[0], B[1]]
        if best is None or cross < best[0]:
            best = (cross, within)
    cross_min, within = best
    return (within - cross_min) / (within + cross_min + eps)

def reads_from_bits(bits):
    """big-Phi + faithful_phi (stdlib mirrors) + Δ_DEC structural predictor + PID cross-check, all
    on the SAME bits + SAME mirror-built MI matrix used by faithful_phi."""
    n = N_UNITS
    tpm, sc = binary_seq_to_tpm(bits, n)
    s = modal_state(sc)
    bphi = big_phi(tpm, n, s)[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    mi = build_mi_matrix(fstate, fn, fdim, 2)
    fphi = faithful_phi_from_mi(mi, fn)
    dec = _decomposability(mi)
    p = pid_system(bits)
    return dict(big=bphi, faith=fphi, dec=dec,
                red_total=p["red_total"], syn_total=p["syn_total"])

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(I, B, k):
    c = I[k].mean() - B[k].mean()
    try:
        d = cohens_d(I[k], B[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(I[k], B[k])
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p, base=B[k].mean(), intv=I[k].mean())

def score(name, gen, t0):
    """gen(seed) -> bits (intervention arm). Baseline = run_base(seed). Matched contrast over seeds."""
    base_rows, intv_rows = [], []
    for s in range(N_SEEDS):
        base_rows.append(reads_from_bits(run_base(s)))
        intv_rows.append(reads_from_bits(gen(s)))
        print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(intv_rows)
    return {k: _contrast(I, B, k) for k in ("big", "faith", "dec", "red_total", "syn_total")}

def sgn(x, eps=1e-3):
    return +1 if x > eps else (-1 if x < -eps else 0)

def signword(x, eps=1e-3):
    return "RAISES" if x > eps else ("LOWERS" if x < -eps else "NULL")

def main():
    print("=" * 84)
    print("H_1033 — which TASK-STRUCTURAL property predicts the big-Phi-DOWN (split-enabling) half?")
    print("RESIDUAL of H_1023 (🔴 SPLIT-TASK-LOCAL: big-Phi went UP not DOWN on a generic TPM).")
    print("FROZEN family of 5 n=4 task substrates, each vs the SAME H_1023 independent-bits baseline.")
    print("FROZEN structural predictor Δ_DEC = decomposability(intervention) − decomposability(base),")
    print("  from the best balanced 2|2 cut of the mirror-built MI matrix (NOT a Phi proxy).")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("engine reads=CPU mirror (numpy), H_1004 engines RE-PROVEN == stdlib at n=4 AND n=5 (H_1012)")
    print("  BEFORE scoring. PID = Williams-Beer (2010) I_min, imported VERBATIM (secondary cross-check).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("PASS = TASK-PROPERTY-PREDICTS-SPLIT: Δ_DEC PERFECTLY rank-separates bigΦ-DOWN from bigΦ-NOT-DOWN")
    print("  (min Δ_DEC over DOWN > max over NOT-DOWN), DOWN = the more-decomposable tasks.")
    print("FAIL = NO-TASK-PREDICTOR: the two classes interleave in Δ_DEC (closed-negative).")
    print("=" * 84)
    print()

    # ── STEP 0 — equivalence proof BEFORE scoring (H_1012), n=4 + n=5. ──
    print("EQUIVALENCE PROOF (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    ok = ok and ok5

    # predictor determinism + engine determinism on a fixed sample of THIS family's bits.
    b_fixed = run_modular(0)
    r1 = reads_from_bits(b_fixed); r2 = reads_from_bits(b_fixed)
    dec_det = abs(r1["dec"] - r2["dec"]) < 1e-12
    eng_det = (abs(r1["big"] - r2["big"]) < 1e-12 and abs(r1["faith"] - r2["faith"]) < 1e-12)
    print(f"  predictor/engine deterministic re-run: dec={dec_det} engine={eng_det}  "
          f"dec={r1['dec']:.6f} big={r1['big']:.4f} faith={r1['faith']:.6f}")

    # Δ_DEC sanity: on a perfectly modular substrate DEC should be high; on XOR/parity low.
    mi_mod = build_mi_matrix(*binary_seq_to_faithful_state(run_modular(0), N_UNITS)[0:3] + (2,)) \
        if False else None  # (explicit per-arm computed below to avoid arg confusion)
    # compute DEC for canonical structures directly through reads_from_bits:
    dec_mod = reads_from_bits(run_modular(0))["dec"]
    dec_xor = reads_from_bits(run_synergy(0))["dec"]
    dec_base = reads_from_bits(run_base(0))["dec"]
    dec_sane = (dec_mod > dec_xor)  # modular factorizes more cleanly than pure-XOR synergy
    print(f"  Δ_DEC sanity: DEC(modular)={dec_mod:.4f} > DEC(xor)={dec_xor:.4f} : {dec_sane} "
          f"| DEC(base)={dec_base:.4f}")

    # WB sanity (canonical COPY=redundancy / XOR=synergy) — re-validated this run.
    Tc = np.array([0,1,0,1,1,0,1,0]); rc, _, _, sc_ = _pid_two_source(Tc, Tc, Tc)
    Xa = np.array([0,0,1,1,0,0,1,1]); Xb = np.array([0,1,0,1,0,1,0,1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    copy_ok = (rc > 0.5 and abs(sc_) < 1e-6)
    xor_ok = (rx < 1e-6 and sx > 0.5)
    print(f"  WB sanity: COPY red={rc:.4f} syn={sc_:.4f} | XOR red={rx:.4f} syn={sx:.4f} "
          f"-> COPY={copy_ok} XOR={xor_ok}")
    ok = ok and dec_det and eng_det and dec_sane and copy_ok and xor_ok
    print(f"  EQUIVALENCE + PREDICTOR-VALIDITY PROOF: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/predictor proof failed — aborting")
    print()

    # FROZEN family (modular, chain, random-TPM, xor-parity, copy-channel)
    SET = [
        ("modular-planning", run_modular,    "2 indep coupled sub-modules {0,1},{2,3} (factorizes)"),
        ("coupled-chain",    run_chain,      "directed ring 0->1->2->3->0 (integrated, no driver)"),
        ("random-TPM",       run_random_tpm, "frozen random dense majority channel (generic)"),
        ("xor-parity",       run_synergy,    "each unit = XOR of other three (pure synergy, H_1023)"),
        ("copy-channel",     run_redundancy, "units 1,2,3 noisy copies of shared driver (H_1023)"),
    ]
    t0 = time.time()
    results = {}
    for name, gen, note in SET:
        print(f"################ SCORE task = {name}  [{note}] ################")
        r = score(name, gen, t0)
        results[name] = r
        bs = signword(r["big"]["contrast"]); fs = signword(r["faith"]["contrast"])
        split = sgn(r["faith"]["contrast"]) != sgn(r["big"]["contrast"])
        print(f"  --- {name}: intervention vs independent-bits baseline (matched n=4) ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {bs}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {fs}")
        print(f"     SPLIT label (sign(faith)!=sign(big)): {split}")
        print(f"     Δ_DEC (decomposability) contrast={r['dec']['contrast']:+.4f} d={r['dec']['d']:+.3f} "
              f"[base={r['dec']['base']:.4f} intv={r['dec']['intv']:.4f}]")
        print(f"     (cross-check) Δredund={r['red_total']['contrast']:+.4f} Δsynergy={r['syn_total']['contrast']:+.4f}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER TEST — does Δ_DEC perfectly rank-separate bigΦ-DOWN from bigΦ-NOT-DOWN?
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 84)
    print("SPLIT-PREDICTOR MATRIX — per task: big-Phi sign x Δ_DEC predictor")
    print("=" * 84)
    print(f"  {'task':18s} | {'big sign':>9s} | {'bigΦ-DOWN?':>10s} | {'Δ_DEC':>9s} | {'faith sign':>10s}")
    rows = {}
    for name, gen, note in SET:
        r = results[name]
        down = r["big"]["contrast"] < -1e-3
        ddec = r["dec"]["contrast"]
        rows[name] = dict(down=down, ddec=ddec, big_c=r["big"]["contrast"], faith_c=r["faith"]["contrast"])
        print(f"  {name:18s} | {signword(r['big']['contrast']):>9s} | {str(down):>10s} | "
              f"{ddec:+9.4f} | {signword(r['faith']['contrast']):>10s}")
    print()

    down_tasks = [n for n in rows if rows[n]["down"]]
    notdown_tasks = [n for n in rows if not rows[n]["down"]]
    print(f"  bigΦ-DOWN tasks ({len(down_tasks)}): {down_tasks}")
    print(f"  bigΦ-NOT-DOWN tasks ({len(notdown_tasks)}): {notdown_tasks}")
    print()

    if not down_tasks or not notdown_tasks:
        # degenerate family — frozen rule says INCONCLUSIVE, not PASS.
        print("=" * 84)
        print("OVERALL: ⚪ INCONCLUSIVE — the frozen family is degenerate (a class is empty); the")
        print("  separation test requires >=1 task in EACH class. No predictor claim made.")
        print(f"  (bigΦ-DOWN count={len(down_tasks)}, bigΦ-NOT-DOWN count={len(notdown_tasks)})")
        print("  VERDICT-TOKEN: INCONCLUSIVE-DEGENERATE-FAMILY")
        print("=" * 84)
        _scope()
        return

    min_down = min(rows[n]["ddec"] for n in down_tasks)
    max_notdown = max(rows[n]["ddec"] for n in notdown_tasks)
    # PASS: perfect rank-separation AND direction matches hypothesis (DOWN = more decomposable, higher Δ_DEC).
    separates = min_down > max_notdown
    tau = (min_down + max_notdown) / 2.0
    print(f"  min Δ_DEC over bigΦ-DOWN     = {min_down:+.4f}")
    print(f"  max Δ_DEC over bigΦ-NOT-DOWN = {max_notdown:+.4f}")
    print(f"  perfect rank-separation (min_DOWN > max_NOTDOWN): {separates}  (threshold τ≈{tau:+.4f})")
    print(f"  direction matches hypothesis (bigΦ-DOWN = higher-Δ_DEC = more decomposable): {separates}")
    print()

    print("=" * 84)
    if separates:
        print("OVERALL: 🟢 TASK-PROPERTY-PREDICTS-SPLIT — the frozen structural predictor Δ_DEC")
        print("  (decomposability of the cause-effect MI geometry) PERFECTLY rank-separates the")
        print("  bigΦ-DOWN (split-enabling) tasks from the bigΦ-NOT-DOWN tasks across the frozen")
        print("  family, in the hypothesized direction: big-Phi goes DOWN exactly when the")
        print("  intervention makes the system MORE decomposable (the MIP cut gets cheaper). The")
        print("  H_1023 residual is resolved — the split-enabling half is PREDICTABLE from a task's")
        print("  effect on decomposability, not unpredictable.")
        print("  VERDICT-TOKEN: TASK-PROPERTY-PREDICTS-SPLIT")
    else:
        print("OVERALL: 🔴 NO-TASK-PREDICTOR (CLOSED-NEGATIVE) — the frozen structural predictor")
        print("  Δ_DEC does NOT cleanly separate the bigΦ-DOWN tasks from the bigΦ-NOT-DOWN tasks;")
        print("  the two classes interleave in decomposability. The split-enabling big-Phi-DOWN")
        print("  half is NOT predicted by this pre-registered structural measure (a_paper_negative_ok)")
        print("  — it stays unpredictable by decomposability across this task family.")
        print("  VERDICT-TOKEN: NO-TASK-PREDICTOR")
    print("=" * 84)
    _scope()

def _scope():
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for the full family x 30 seeds. Both CPU")
    print("mirrors RE-PROVEN == stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring;")
    print("Δ_DEC is exact + deterministic on the mirror-built MI matrix; the PID is validated on")
    print("canonical COPY/XOR. The predictor is NOT a proxy for Phi (Phi from stdlib mirrors only).")
    print("Scale-transfer UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool.")
    print("NOT a forge binary; $0 CPU-local, no GPU.")

if __name__ == "__main__":
    main()
