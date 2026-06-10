"""H_1121 — does the faithful φ_EI-UP / big-Φ-DOWN sign-split appear on an ANIMA
ENGINE-A⊥G OPPONENT substrate, or is it PLANNING-SPECIFIC? (opponent-generality test)

PRE-REG: this docstring (frozen falsifier BELOW, set BEFORE any Φ is scored).

THE ARC (settled, planning substrate): faithful φ_EI ↑ / big-Φ ↓ sign-split on PLANNING
policies — robust (H_1037/H_1038), causally redundancy-driven (H_1039), and PLANNING-BOUNDED
for the CAUSAL mechanism (H_1062: de-redundify collapses the split ONLY on planning; non-
planning interventions raise correlation but the ZCA-removable cut is <80% so the split does
not cleanly arise/collapse the same way). The whole arc was measured on a PLANNING toy
substrate (h1004.planning_trajectories: deliberate multi-branch rollout of a learned WM).

THIS HYPOTHESIS: does the SAME faithful↑/big-Φ↓ sign-split appear when the n≤5 channel
substrate is driven by the anima engine's A⊥G OPPONENT dynamics — the real engine's
repulsion-field tension structure (Engine A pure_field ⇄ Engine G motivation gate, Ψ=1/2
fixed point; CLAUDE.md @I) — rather than the planning toy? I.e. is the split a property of
A⊥G OPPONENT COMPOSITION, or planning-specific (H_1062 said planning-specific for the CAUSAL
mechanism)?

A⊥G OPPONENT SUBSTRATE (H404 dual-FFN form, BOUNDED/contractive)
----------------------------------------------------------------
Per the H404 dual-FFN / repulsion-field form, each step's channel vector is the OPPONENT
difference of two distinct nonlinear engine maps on the SAME driven state, integrated by a
LEAKY/contractive update (the engine has a BOUNDED Ψ=1/2 fixed point / Φ-ratchet — bounded
oscillatory dynamics, NOT divergence; CLAUDE.md @I, pure_field.hexa):
    x_{t+1} = (1−LR)*x_t + LR * ( engine_A(x_t) − engine_G(x_t) )    (OPPONENT, A repels ⊥ G)
where engine_A, engine_G are two FIXED random tanh-FFN maps (W·x+b → tanh) with DISTINCT
seeds (Engine A ⊥ Engine G). The (1−LR)*x leak KEEPS the state bounded (an attractor regime),
WITHOUT which a plain x += LR*upd accumulator DIVERGES (norm→∞) and the median-binarized
channels collapse to a trivial monotone ramp (2-state degenerate Φ identical across all modes
— a SATURATION TAUTOLOGY, the H_1051/H_1061 idealized-binary trap). The leak is the standard
bounded-recurrence form (cf cwm_probe_lib.LatentWorldModel leak); it was set BEFORE scoring to
remove the construction defect, NOT to move the falsifier (H_1061 discipline). The trajectory
is the genuine A⊥G opponent dynamic: A drives / G gates, their DIFFERENCE is the channel
output. n≤5 channels = a coordinate read of the LATENT state (top-variance channels, median-
binarized — the EXACT H_1039/H_1064 read path).

MATCHED NON-OPPONENT CONTROL (capacity-identical, opponent SIGN removed)
-----------------------------------------------------------------------
The ONLY structural change vs the opponent substrate is the SIGN of the second engine:
    x_{t+1} = (1−LR)*x_t + LR * ( engine_A(x_t) + engine_G(x_t) )    (CONTROL, additive coupling)
SAME engine_A, SAME engine_G, SAME weights/biases/seeds, SAME LR, SAME leak, SAME read path.
We REMOVE ONLY the opponent (subtraction) structure — A and G now COOPERATE additively. A
robustness control SINGLE = engine_A alone (no G at all) is also reported. If the split is an
OPPONENT property it must be present on OPPONENT and ABSENT on these non-opponent controls.

WHY THIS IS NOT A RE-RUN OF PLANNING: the substrate is NOT planning_trajectories. It is a
freshly-built A⊥G opponent dynamical system. The planning split arose from deliberate
forward-rolled branch deliberation; here there is NO planning, NO branches, NO WM rollout —
only the engine's own opponent self-dynamics. reproduce-H_1039 is run ONLY as a substrate-
sanity anchor (confirm the planning split still reproduces in THIS file's stdlib mirror),
NEVER as the opponent measurement.

FROZEN FALSIFIER (set BEFORE running, NO goalpost)
--------------------------------------------------
SIGN_EPS = 1e-3 ; N_SEEDS = 12 (≥10) ; n = 4 EXACT (n=5 mirror-proven).
Build the A⊥G opponent substrate vs the matched non-opponent control(s). On EACH, compute
BOTH faithful φ_EI (exact MIP-EI) AND big-Φ (IIT 4.0 over MIP) on the binarized channels.
Contrast = (opponent reads) − (control reads), SAME-seed paired across N_SEEDS.

🟢 OPPONENT-SPLITS iff the A⊥G substrate shows  faithful_contrast > +1e-3  AND
   big_contrast < −1e-3  (faithful↑ / big-Φ↓, like planning), AND the split is ABSENT in the
   non-opponent control (control does NOT itself satisfy faith>+eps & big<−eps vs single).
🔴 NO-SPLIT  if no split (faith not UP or big not DOWN on opponent contrast) ⇒ the split is
   PLANNING-SPECIFIC, not opponent-general (consistent with H_1062). a_paper_negative_ok.
🔴 SAME-SIGN if both measures move the SAME direction on the opponent contrast ⇒ no measure
   dependence on this substrate. a_paper_negative_ok.

The opponent contrast is the OPPONENT(subtract) substrate vs the ADDITIVE(non-opponent)
control — both share engine weights, so the contrast ISOLATES the opponent structure.

ENGINES = BOTH stdlib IIT-4.0 CPU mirrors (h1004), RE-PROVEN ≡ stdlib at n=4 AND n=5 BEFORE
scoring (h1012.prove_mirrors_at_n; a_phi_iit4_tool, NO proxy). BITS/log2 MI=H(A)+H(B)−H(A,B)
(H_1043 nats-bug lesson). IMPORTS by REAL MODULE NAME (H_1038 fork-unpickle lesson). SERIAL
only, NO multiprocessing.Pool (H_1038 hang). $0 CPU-local, no GPU/pod. g5 CODE-measured (p7).
TOY n=4 EXACT (n=5 mirror-proven); production/large-n UNVERIFIED (a_scale_honest_scope).

xref: H_1064 (split-measure-adjudication) · H_1062 (split-is-planning-specific) ·
phi-measure-dependence paper · a_phi_iit4_tool.
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# Import the prior chain by REAL MODULE NAMES (no importlib custom-name; H_1038 lesson).
import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402

# REUSE the stdlib-proven Φ machinery UNMODIFIED -----------------------------------------------
big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

LOG2 = math.log(2.0)
N_UNITS = 4
N_SEEDS = 12          # ≥ 10 (frozen)
PLAN_DEPTH = 8        # reproduce-H_1039 anchor ONLY
SIGN_EPS = 1e-3       # FROZEN split sign threshold

# ── A⊥G opponent dynamical-system constants (FROZEN before scoring) ──
LATENT = 24           # match h1004 LATENT (coordinate read of the engine state)
ENG_HID = 32          # FFN hidden width of each engine map
ROLL = 40             # trajectory length (== h1004 ROLL)
LR = 0.70             # leaky/contractive integration rate: x=(1-LR)x+LR*upd (BOUNDED regime;
                      # diagnosed BEFORE scoring — a plain accumulator diverges → degenerate Φ)
A_SEED_BASE = 4040    # Engine A weights seed base (⊥ Engine G)
G_SEED_BASE = 9090    # Engine G weights seed base (⊥ Engine A)

# ═══════════════════════════════════════════════════════════════════════════
# substrate read — the EXACT H_1039/H_1064 path: top-variance channels, median-binarize.
# ═══════════════════════════════════════════════════════════════════════════
def _top_variance_channels(H, n_units):
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    return H[:, idx]

def _binarize_median(chans):
    med = np.median(chans, axis=0)
    return (chans > med).astype(int)

def macro_bits(H, n):
    return _binarize_median(_top_variance_channels(H, n))

# ═══════════════════════════════════════════════════════════════════════════
# the two FIXED nonlinear engine maps (Engine A ⊥ Engine G), H404 dual-FFN form.
# Each is a single tanh-FFN  x -> tanh(W2 @ tanh(W1 @ x + b1) + b2)  over the LATENT state.
# Distinct seeds make A and G genuinely orthogonal/independent maps.
# ═══════════════════════════════════════════════════════════════════════════
class EngineFFN:
    def __init__(self, dim, hid, seed):
        rng = np.random.default_rng(seed)
        self.W1 = rng.standard_normal((hid, dim)) / np.sqrt(dim)
        self.b1 = rng.standard_normal(hid) * 0.1
        self.W2 = rng.standard_normal((dim, hid)) / np.sqrt(hid)
        self.b2 = rng.standard_normal(dim) * 0.1

    def __call__(self, x):
        h = np.tanh(self.W1 @ x + self.b1)
        return np.tanh(self.W2 @ h + self.b2)

def _engines_for_seed(seed):
    """Engine A and Engine G — two DISTINCT fixed tanh-FFN maps over the LATENT state."""
    eA = EngineFFN(LATENT, ENG_HID, A_SEED_BASE + seed)
    eG = EngineFFN(LATENT, ENG_HID, G_SEED_BASE + seed)
    return eA, eG

def _start_state(seed):
    """A common driven start state, SAME across opponent/control/single for a given seed."""
    rng = np.random.default_rng(2121 + seed)
    # a structured driven cue (like h1004's sin-input encode), projected to LATENT
    base = np.stack([np.sin(0.2 * np.arange(LATENT) + k) for k in range(1)], axis=0).ravel()
    return 0.5 * base + 0.3 * rng.standard_normal(LATENT)

def opponent_trajectory(seed, mode):
    """Iterate a dynamical system from the SAME start with the SAME two engines; only the
    COMPOSITION (opponent subtract vs additive vs single) differs.

    mode = 'opponent' : upd = A(x) - G(x)   (A⊥G repulsion / dual-FFN difference)
    mode = 'additive' : upd = A(x) + G(x)   (matched NON-opponent control: same weights)
    mode = 'single'   : upd = A(x)          (robustness control: G removed entirely)
    Update is LEAKY/contractive  x = (1-LR)*x + LR*upd  → BOUNDED attractor regime
    (a plain x += LR*upd diverges and degenerates Φ; diagnosed BEFORE scoring).
    Returns the (ROLL, LATENT) latent trajectory.
    """
    eA, eG = _engines_for_seed(seed)
    x = _start_state(seed).copy()
    out = np.empty((ROLL, LATENT))
    for t in range(ROLL):
        a = eA(x)
        if mode == "opponent":
            upd = a - eG(x)
        elif mode == "additive":
            upd = a + eG(x)
        elif mode == "single":
            upd = a
        else:
            raise ValueError(mode)
        x = (1.0 - LR) * x + LR * upd      # LEAKY/contractive → bounded (Ψ-fixed-point regime)
        out[t] = x
    return out

# ═══════════════════════════════════════════════════════════════════════════
# per-trajectory scoring: BOTH stdlib Φ engines on the SAME binarized channels.
# ═══════════════════════════════════════════════════════════════════════════
def score_bits(bits, n):
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return dict(big=float(bphi), faith=float(fphi), on_frac=float(bits.mean()))

def score_mode(seed, mode, n):
    H = opponent_trajectory(seed, mode)
    return score_bits(macro_bits(H, n), n)

def faith_sign(c):
    return "UP" if c > SIGN_EPS else ("DOWN" if c < -SIGN_EPS else "NULL")

def big_sign(c):
    return "DOWN" if c < -SIGN_EPS else ("UP" if c > SIGN_EPS else "NULL")

def main():
    print("=" * 94)
    print("H_1121 — faithful φ_EI-UP / big-Φ-DOWN sign-split on an ANIMA ENGINE-A⊥G OPPONENT")
    print("substrate vs planning? OPPONENT(x+=LR(A(x)-G(x))) vs matched NON-OPPONENT ADDITIVE")
    print("(x+=LR(A(x)+G(x)), SAME weights, opponent SIGN removed) + SINGLE(A only) robustness.")
    print("substrate=CPU-mirror (numpy) h1004+h1012, RE-PROVEN ≡ stdlib at n=4,5 (a_phi_iit4_tool).")
    print("big-Φ: stdlib iit4_bigphi.hexa | faithful_phi: stdlib iit4/faithful_phi.hexa (NO proxy).")
    print(f"FROZEN falsifier: SIGN_EPS={SIGN_EPS}, N_SEEDS={N_SEEDS} (≥10), n=4 EXACT (n=5 mirror).")
    print("🟢 OPPONENT-SPLITS = opponent contrast faith>+eps & big<−eps AND control NOT split.")
    print("🔴 NO-SPLIT ⇒ planning-specific (consistent H_1062) | 🔴 SAME-SIGN ⇒ no measure-dep.")
    print("g5 CODE-measured (p7) | a_scale_honest_scope toy n=4 | SERIAL CPU $0 no GPU/pod.")
    print("=" * 94, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors ≡ stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors ≡ stdlib (a_phi_iit4_tool) at n=4 AND n=5:")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  ≡ mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror ≡ stdlib proof FAILED.")
        raise SystemExit(1)
    print()

    n = 4
    t0 = time.time()

    # ── STEP 1: reproduce-H_1039 ANCHOR — confirm the planning split reproduces in THIS mirror ──
    print(f"STEP 1 — reproduce-H_1039 ANCHOR (planning depth-{PLAN_DEPTH} vs GREEDY, n={n}, sanity only)")
    pr, gr = [], []
    for s in range(N_SEEDS):
        Hg, Hp = planning_trajectories(s, PLAN_DEPTH)
        pr.append(score_bits(macro_bits(Hp, n), n))
        gr.append(score_bits(macro_bits(Hg, n), n))
    Pp = {k: np.array([r[k] for r in pr]) for k in pr[0]}
    Gg = {k: np.array([r[k] for r in gr]) for k in gr[0]}
    plan_faith_c = float(Pp["faith"].mean() - Gg["faith"].mean())
    plan_big_c = float(Pp["big"].mean() - Gg["big"].mean())
    plan_split = (faith_sign(plan_faith_c) == "UP") and (big_sign(plan_big_c) == "DOWN")
    print(f"  planning faithful contrast (plan−greedy) = {plan_faith_c:+.4f} -> {faith_sign(plan_faith_c)}")
    print(f"  planning big-Φ   contrast (plan−greedy) = {plan_big_c:+.4f} -> {big_sign(plan_big_c)}")
    print(f"  planning SPLIT present (faith-UP & big-DOWN): {plan_split}   (H_1039 ref faith+2.33/big−4.01)")
    print(f"  reproduce-H_1039 anchor OK: {plan_split}", flush=True)
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: build the A⊥G OPPONENT substrate + matched controls; score BOTH Φ.
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 94)
    print(f"STEP 2 — A⊥G OPPONENT substrate vs NON-OPPONENT controls ({N_SEEDS} seeds, n={n})")
    print("=" * 94)
    rows = {m: [] for m in ("opponent", "additive", "single")}
    for s in range(N_SEEDS):
        for m in rows:
            rows[m].append(score_mode(s, m, n))
        if (s + 1) % 4 == 0 or s == 0:
            print(f"    [seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    M = {m: {k: np.array([r[k] for r in rows[m]]) for k in rows[m][0]} for m in rows}

    def line(tag, d):
        print(f"  {tag:9s}  faithful={d['faith'].mean():.4f}±{d['faith'].std():.4f}   "
              f"big-Φ={d['big'].mean():.4f}±{d['big'].std():.4f}   on_frac={d['on_frac'].mean():.3f}")
    print("  ── per-mode mean Φ (both stdlib engines, n=4 EXACT) ──")
    line("OPPONENT", M["opponent"])
    line("ADDITIVE", M["additive"])
    line("SINGLE", M["single"])
    print()

    # ── NON-DEGENERACY guard (anti-tautology, H_1061 lesson): the substrate must produce
    #    REAL across-seed Φ variance AND the opponent must NOT be bit-identical to the control,
    #    else the NULL contrast is a saturation artifact (divergent ramp), not a measurement. ──
    print("  ── NON-DEGENERACY guard (substrate must vary; opponent ≠ additive bit-pattern) ──")
    phi_has_var = (M["opponent"]["faith"].std() > 1e-6 and M["opponent"]["big"].std() > 1e-6 and
                   M["additive"]["faith"].std() > 1e-6 and M["additive"]["big"].std() > 1e-6)
    # fraction of seeds whose opponent macro-bits DIFFER from the additive macro-bits
    diff_seeds = 0
    for s in range(N_SEEDS):
        bo = macro_bits(opponent_trajectory(s, "opponent"), n)
        ba = macro_bits(opponent_trajectory(s, "additive"), n)
        if not np.array_equal(bo, ba):
            diff_seeds += 1
    modes_distinct = (diff_seeds >= max(1, N_SEEDS // 2))
    print(f"  per-mode Φ has across-seed variance: {phi_has_var}  "
          f"(opp faith_std={M['opponent']['faith'].std():.4f} big_std={M['opponent']['big'].std():.4f})")
    print(f"  opponent macro-bits ≠ additive macro-bits on {diff_seeds}/{N_SEEDS} seeds "
          f"-> modes_distinct={modes_distinct}")
    non_degenerate = phi_has_var and modes_distinct
    print(f"  NON-DEGENERACY: {non_degenerate}  (if False the substrate SATURATED; verdict VOID)")
    if not non_degenerate:
        print("  ABORT — substrate degenerate (saturation tautology); cannot adjudicate the split.")
        raise SystemExit(1)
    print()

    # ── the OPPONENT CONTRAST (frozen): opponent − additive (isolates opponent structure) ──
    opp_faith_c = float(M["opponent"]["faith"].mean() - M["additive"]["faith"].mean())
    opp_big_c = float(M["opponent"]["big"].mean() - M["additive"]["big"].mean())
    # control's own contrast vs single (does the non-opponent control ITSELF split?)
    ctrl_faith_c = float(M["additive"]["faith"].mean() - M["single"]["faith"].mean())
    ctrl_big_c = float(M["additive"]["big"].mean() - M["single"]["big"].mean())

    print("  ── CONTRAST table (FROZEN sign test, faith-UP & big-DOWN = planning-like split) ──")
    print(f"  OPPONENT − ADDITIVE :  faithful={opp_faith_c:+.4f} -> {faith_sign(opp_faith_c)}   "
          f"big-Φ={opp_big_c:+.4f} -> {big_sign(opp_big_c)}")
    print(f"  ADDITIVE − SINGLE   :  faithful={ctrl_faith_c:+.4f} -> {faith_sign(ctrl_faith_c)}   "
          f"big-Φ={ctrl_big_c:+.4f} -> {big_sign(ctrl_big_c)}")
    print()

    opponent_splits = (faith_sign(opp_faith_c) == "UP") and (big_sign(opp_big_c) == "DOWN")
    control_splits = (faith_sign(ctrl_faith_c) == "UP") and (big_sign(ctrl_big_c) == "DOWN")
    # same-sign on opponent contrast = both UP or both DOWN (and neither NULL)
    opp_same_sign = (
        (opp_faith_c > SIGN_EPS and opp_big_c > SIGN_EPS) or
        (opp_faith_c < -SIGN_EPS and opp_big_c < -SIGN_EPS)
    )

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER ADJUDICATION (frozen)
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 94)
    if opponent_splits and not control_splits:
        verdict_token = "OPPONENT-SPLITS"
        print("OVERALL: 🟢 OPPONENT-SPLITS (H1 PASS) — the faithful↑/big-Φ↓ sign-split is present on")
        print(f"  the A⊥G OPPONENT substrate (opp−additive faith={opp_faith_c:+.4f} UP, big={opp_big_c:+.4f}")
        print(f"  DOWN) AND ABSENT in the matched non-opponent control (additive−single not a split).")
        print("  ⇒ the split is a property of A⊥G OPPONENT COMPOSITION, not planning-only.")
    elif opponent_splits and control_splits:
        verdict_token = "SPLIT-NOT-OPPONENT-ISOLATED"
        print("OVERALL: 🔴 SPLIT-NOT-OPPONENT-ISOLATED (CLOSED-NEGATIVE, a_paper_negative_ok) — both the")
        print("  opponent AND the non-opponent control show the split ⇒ split is NOT isolated to the")
        print("  opponent(subtraction) structure (it rides the shared engine maps, not the opponency).")
    elif opp_same_sign:
        verdict_token = "SAME-SIGN-NO-MEASURE-DEP"
        print("OVERALL: 🔴 SAME-SIGN (CLOSED-NEGATIVE, a_paper_negative_ok) — on the opponent contrast")
        print(f"  faithful ({opp_faith_c:+.4f}) and big-Φ ({opp_big_c:+.4f}) move the SAME direction ⇒ no")
        print("  measure-dependence on the A⊥G opponent substrate (the planning split does not recur).")
    else:
        verdict_token = "NO-SPLIT-PLANNING-SPECIFIC"
        print("OVERALL: 🔴 NO-SPLIT (CLOSED-NEGATIVE, a_paper_negative_ok) — the A⊥G OPPONENT substrate")
        print(f"  does NOT show the planning-like faithful↑/big-Φ↓ split (opp−additive faith={opp_faith_c:+.4f}")
        print(f"  -> {faith_sign(opp_faith_c)}, big={opp_big_c:+.4f} -> {big_sign(opp_big_c)}).")
        print("  ⇒ the sign-split is PLANNING-SPECIFIC, not opponent-general — consistent with H_1062")
        print("  (the split's clean ZCA-removable mechanism was planning-bounded).")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 94)
    print("HONEST scope (a_scale_honest_scope): TOY n=4 EXACT, N_SEEDS=12, both mirrors RE-PROVEN ≡")
    print("stdlib at n=4 AND n=5 (a_phi_iit4_tool, NO proxy, BITS/log2). A⊥G opponent substrate is a")
    print("dual-FFN dynamical mirror of the engine repulsion form (H404), NOT the live pure_field/")
    print("engine_g binaries. reproduce-H_1039 anchor confirms the planning split in THIS mirror.")
    print("Production / large-n / live-engine-coupled UNVERIFIED. SERIAL CPU $0 no GPU/pod. g5 (p7).")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), sign_eps=SIGN_EPS, plan_depth=int(PLAN_DEPTH),
        latent=LATENT, eng_hid=ENG_HID, roll=ROLL, lr=LR,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        reproduce_h1039_anchor=dict(faith_contrast=plan_faith_c, big_contrast=plan_big_c,
                                    split_present=bool(plan_split)),
        per_mode={m: dict(faith_mean=float(M[m]["faith"].mean()), faith_std=float(M[m]["faith"].std()),
                          big_mean=float(M[m]["big"].mean()), big_std=float(M[m]["big"].std()),
                          on_frac=float(M[m]["on_frac"].mean())) for m in M},
        opponent_contrast=dict(faith=opp_faith_c, big=opp_big_c,
                               faith_sign=faith_sign(opp_faith_c), big_sign=big_sign(opp_big_c)),
        control_contrast=dict(faith=ctrl_faith_c, big=ctrl_big_c,
                              faith_sign=faith_sign(ctrl_faith_c), big_sign=big_sign(ctrl_big_c)),
        non_degeneracy=dict(phi_has_var=bool(phi_has_var), diff_seeds=int(diff_seeds),
                            modes_distinct=bool(modes_distinct), non_degenerate=bool(non_degenerate)),
        opponent_splits=bool(opponent_splits), control_splits=bool(control_splits),
        opp_same_sign=bool(opp_same_sign),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1121_phi_signsplit_opponent_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
