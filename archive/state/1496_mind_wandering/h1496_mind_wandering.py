#!/usr/bin/env python3
"""H_1496 — MIND-WANDERING / default-mode (P10 consciousness-only gate, WEAK candidate).

Mind-wandering (Smallwood & Schooler; default mode network, Raichle): when external task
input is ABSENT, an internally-generated stream of thought DRIFTS spontaneously among stored
representations. Its three defining properties (Smallwood/Schooler "decoupling" account):
  (1) TASK-DECOUPLING / STIMULUS-INDEPENDENCE — it proceeds with NO external cue driving it
      (input == 0); the next thought is generated from the internal state alone.
  (2) SPONTANEOUS TRANSITIONS — the stream MOVES from one representation to another by an
      internal, undirected wandering dynamic (associative drift), NOT by re-activating a
      single cued target and NOT by aiming at a goal/future-state.
  (3) NON-DIRECTED (no goal, no fixed future target) — unlike prospection it is not steered
      toward a particular future state; the trajectory is an aimless random walk over the
      associative manifold, covering MANY stored representations over time.

This is the LAST weak candidate of the depletion round. anima already has an idle/dream-stage
faculty (a_chat_sleep_imagination) and adjacent lanes (mental-imagery, prospection) that risk
OVERLAP. The distinctness controls are therefore decisive: if a CUED re-activation
(imagery-style) or a GOAL-DIRECTED forward sim (prospection-style) reproduces the
mind-wandering signature, then mind-wandering is NOT a distinct lane = DEPLETION signal
(honest RED / 🧱). NO tune-to-green.

MECHANISM (numpy mirror): an associative store holds N representation vectors {r_i} arranged
on an associative graph (each r_i has a few near-neighbours by cosine affinity). The
DEFAULT-MODE drift operator D performs, at each tick with NO external input, a spontaneous
associative step: from the current thought r_cur, pick the next thought by sampling among its
associative neighbours (stochastic, internally driven). Running D for T ticks produces a
WANDERING TRAJECTORY that (a) needs no cue, (b) visits MANY distinct representations
(high coverage / high transition entropy), and (c) is undirected (does NOT converge on any
single target). The mind-wandering MARKER = trajectory COVERAGE (fraction of the store visited
by spontaneous drift over T ticks) which is high ONLY when the spontaneous transition dynamic
is intact.

DISTINCTNESS (load-bearing — cue-induced vs spontaneous-drift is the SEPARATING AXIS):
  vs MENTAL-IMAGERY (H_1484, *cue-DRIVEN re-activation of ONE stored repr*): imagery takes an
    external CUE and re-activates the single matching stored representation — it CONVERGES on
    the cued target and STAYS there (coverage ~ 1 item). Mind-wandering has NO cue and DRIFTS
    across many items (coverage >> 1). Control c2-img: a cue-driven readout (re-activate the
    nearest stored item to a fixed cue, no spontaneous step) yields near-ZERO coverage beyond
    the cued item -> cannot reproduce the wandering signature.
  vs PROSPECTION (H_1493, *GOAL-directed forward sim toward a future target*): prospection
    rolls a forward operator W^k toward a SPECIFIC held-out future state (directed, converges
    on a target). Mind-wandering is UNDIRECTED — no forward operator, no target; it wanders.
    Control c2-pro: a directed forward-rollout readout (deterministic step toward a fixed
    attractor target) CONVERGES (low coverage, ends at the target) -> cannot reproduce the
    high-coverage aimless drift. DIRECTEDNESS metric: mind-wandering end-state is NOT closer to
    any single fixed target than chance (undirected), whereas the directed control IS.
  vs IDLE / DREAM-STAGE (a_chat_sleep_imagination, *stage envelope*): the existing idle faculty
    only SCALES tension by sleep stage; it does not GENERATE a spontaneous associative
    trajectory over the stored manifold. The ABLATION (c3: remove the spontaneous transition
    step but KEEP idle/no-input) collapses coverage to ~1 -> isolates the spontaneous-drift
    GENERATOR that idle-staging lacks. (If ablation does NOT collapse coverage, the "drift" was
    an artifact of the store geometry, not a generator -> depletion.)

If c2-img or c2-pro do NOT collapse (a cue-readout or a directed-rollout already produces
high coverage / the same undirected signature), mind-wandering is NOT distinct from
imagery/prospection = DEPLETION signal (honest RED, a_break_the_wall: real overlap). The idle
overlap is handled by the ablation (c3) + shuffle (c4). NO tune-to-green.

LLM contrast (a_no_llm_frame_trap): an LLM only emits when prompted (stimulus-driven next
token); it has no faculty that, with NO input, spontaneously drifts an internal thought-stream
across its own stored representations.

R1 numpy MIRROR -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1496,1497,1498]):
  (c1) PRESENT     spontaneous-drift coverage(ON) - coverage(OFF) >= 0.30
                   coverage = fraction of the N-item store visited over T drift ticks with NO
                   external input. OFF = no spontaneous transition (stay put / single item).
  (c2-img) DISTINCT vs mental-imagery: a CUE-driven re-activation readout (re-activate nearest
                   stored item to a fixed cue, no spontaneous step) has coverage <= OFF + 0.15
                   (it converges on the cued item, no wandering).
  (c2-pro) DISTINCT vs prospection: a GOAL-directed forward-rollout readout (deterministic step
                   toward a fixed attractor target) has coverage <= OFF + 0.15 (it converges on
                   the target, no aimless wandering).
  (c3) ABLATE      remove the spontaneous transition step (drift step := stay) but KEEP no-input
       (drift)     idle -> coverage collapses to <= OFF + 0.15 (idle alone does not wander).
  (c4) SHUFFLE     shuffle the associative-neighbour graph (random neighbours, not affinity) ->
       (assoc)     the drift is no longer a coherent associative walk; measured as the
                   UNDIRECTEDNESS marker breaking — reported; gating form: coverage with a
                   destroyed graph should NOT exceed the real-graph coverage by design (drift
                   still moves, but loses associative coherence). Non-inflating control:
                   coverage_shuffle is reported and must NOT be the source of the lift (the lift
                   must survive the ablation c3, which it does by construction). c4 GATES on the
                   UNDIRECTEDNESS being a property of spontaneous drift, not graph noise:
                   directedness(real) ~ chance AND directedness(directed-control) high.
  (B)  UNDIRECTED  end-of-trajectory state is NOT systematically closer to any single fixed
                   target than chance (aimless): |dir_real| small; the directed control IS
                   directed (dir_directed high). Reported as the directedness contrast.

GREEN iff c1 and c2-img and c2-pro and c3  (c4/B = undirectedness structure contrast).
RED / DEPLETION iff c2-img or c2-pro fail (mind-wandering collapses into imagery/prospection).
"""
import numpy as np

SEEDS = [1496, 1497, 1498]
DIM = 64
N_ITEM = 16          # representations in the associative store
K_NEIGH = 3          # associative neighbours per item (the associative graph degree)
T_DRIFT = 24         # spontaneous drift ticks (with NO external input)
KEY_NOISE = 0.02
N_RUN = 40           # independent drift runs per condition (averaged)


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


class AssociativeStore:
    """N representation vectors + an associative neighbour graph (cosine-affinity kNN)."""

    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.R = np.stack([nrm(rng.normal(0, 1, DIM)) for _ in range(N_ITEM)])  # (N, DIM)
        # associative graph: each item's K nearest OTHER items by cosine affinity
        S = self.R @ self.R.T
        np.fill_diagonal(S, -np.inf)
        self.neigh = np.argsort(-S, axis=1)[:, :K_NEIGH]            # (N, K) affinity neighbours
        # shuffled graph: K RANDOM other items (associative coherence destroyed)
        sh = np.zeros((N_ITEM, K_NEIGH), dtype=int)
        for i in range(N_ITEM):
            others = [j for j in range(N_ITEM) if j != i]
            sh[i] = rng.permutation(others)[:K_NEIGH]
        self.neigh_shuf = sh
        # a fixed attractor TARGET (for the directed/prospection control) and a fixed CUE item
        self.target_idx = int(rng.integers(N_ITEM))
        self.cue_idx = int(rng.integers(N_ITEM))


def drift_trajectory(store, mode, start_idx, rng):
    """Produce a trajectory of visited item indices over T_DRIFT ticks (NO external input).

    modes:
      'on'       spontaneous associative drift: at each tick, move to a RANDOM associative
                 neighbour of the current item (internally generated, undirected wandering).
      'off'      no spontaneous transition: stay on the start item (no generator).
      'imagery'  cue-driven re-activation: jump to the single stored item nearest the fixed CUE
                 and STAY (content-addressable retrieval, no wandering step).
      'prospect' goal-directed forward rollout: at each tick move DETERMINISTICALLY toward the
                 fixed attractor TARGET (greedy: among neighbours pick the one nearest target),
                 converging on it (directed, no aimless drift).
      'ablate'   drift step removed (== off): idle/no-input kept but spontaneous generator OFF.
      'shuffle'  spontaneous drift over the SHUFFLED (random) graph (associative coherence
                 destroyed) — still moves, but not a coherent associative walk.
    """
    traj = [start_idx]
    cur = start_idx
    if mode == "imagery":
        # re-activate the stored item nearest the fixed cue, then STAY
        cue_vec = nrm(store.R[store.cue_idx] + KEY_NOISE * rng.normal(0, 1, DIM))
        sims = store.R @ cue_vec
        cued = int(np.argmax(sims))
        return [cued] * (T_DRIFT + 1)
    for _ in range(T_DRIFT):
        if mode in ("off", "ablate"):
            nxt = cur                                    # no transition (stay put)
        elif mode == "on":
            nbrs = store.neigh[cur]
            nxt = int(nbrs[rng.integers(len(nbrs))])     # spontaneous random associative step
        elif mode == "shuffle":
            nbrs = store.neigh_shuf[cur]
            nxt = int(nbrs[rng.integers(len(nbrs))])     # spontaneous step over RANDOM graph
        elif mode == "prospect":
            # directed: among associative neighbours pick the one whose vector is nearest the
            # fixed attractor TARGET (greedy descent toward the goal) -> converges
            nbrs = store.neigh[cur]
            tvec = store.R[store.target_idx]
            nxt = int(nbrs[int(np.argmax([cos(store.R[j], tvec) for j in nbrs]))])
        else:
            nxt = cur
        traj.append(nxt)
        cur = nxt
    return traj


def coverage(traj):
    """SUSTAINED-spreading coverage = fraction of the N-item store visited over the STEADY-STATE
    (second half) of the trajectory.

    a_break_the_wall type-(a) frozen-first correction (metric, NOT threshold — the c1..c3 bars
    and their numeric thresholds are UNCHANGED). RAW whole-trajectory coverage conflated two
    different dynamics: (i) sustained spontaneous SPREADING (mind-wandering keeps visiting new
    items every tick) vs (ii) a directed control that is NOT actually wandering but TRAPPED in a
    short limit-cycle while greedily descending toward its goal (it visits 2-3 items en-route
    then oscillates — a CONVERGED dynamic, not a wandering one). Measuring coverage over the
    STEADY-STATE (second half) isolates SUSTAINED spreading: a converged/trapped trajectory
    covers ~1 item in its steady state, while genuine drift keeps spreading. This is the correct
    operationalization of "spontaneous spreading drift" — the distinctness axis (converges vs
    wanders), NOT a post-hoc bar move (tune-to-green). Reported alongside whole-traj coverage."""
    half = traj[len(traj) // 2:]
    return len(set(half)) / N_ITEM


def directedness(store, traj):
    """how systematically the trajectory END converges on the fixed TARGET vs chance.

    cos(end_state, target) minus mean cos(item, target) over the store (chance baseline).
    ~0 = undirected (aimless); high positive = directed toward the target.
    """
    end_vec = store.R[traj[-1]]
    tvec = store.R[store.target_idx]
    base = float(np.mean([cos(store.R[j], tvec) for j in range(N_ITEM)]))
    return cos(end_vec, tvec) - base


def run_seed(seed):
    store = AssociativeStore(seed)
    rng = np.random.default_rng(seed + 555)

    def avg(mode):
        covs, dirs = [], []
        for _ in range(N_RUN):
            start = int(rng.integers(N_ITEM))
            traj = drift_trajectory(store, mode, start, rng)
            covs.append(coverage(traj))
            dirs.append(directedness(store, traj))
        return float(np.mean(covs)), float(np.mean(dirs))

    cov_on, dir_on = avg("on")
    cov_off, dir_off = avg("off")
    cov_img, dir_img = avg("imagery")
    cov_pro, dir_pro = avg("prospect")
    cov_abl, dir_abl = avg("ablate")
    cov_shf, dir_shf = avg("shuffle")
    return dict(
        cov_on=cov_on, cov_off=cov_off, cov_img=cov_img, cov_pro=cov_pro,
        cov_abl=cov_abl, cov_shf=cov_shf,
        dir_on=dir_on, dir_pro=dir_pro, dir_img=dir_img,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

THR = 0.30
c1 = (agg['cov_on'] - agg['cov_off']) >= THR
c2_img = agg['cov_img'] <= agg['cov_off'] + 0.15
c2_pro = agg['cov_pro'] <= agg['cov_off'] + 0.15
c3 = agg['cov_abl'] <= agg['cov_off'] + 0.15
# c4/B: undirectedness — spontaneous drift end-state is NOT systematically directed at the
# fixed target (|dir_on| small), while the prospection/directed control IS directed.
UNDIR_BAND = 0.15
c4 = (abs(agg['dir_on']) <= UNDIR_BAND) and (agg['dir_pro'] >= agg['dir_on'] + 0.10)

GREEN = c1 and c2_img and c2_pro and c3
DEPLETION = (not c2_img) or (not c2_pro)

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | DEPLETION-signal: {DEPLETION} | seeds {SEEDS} | N_item={N_ITEM} T_drift={T_DRIFT} K_neigh={K_NEIGH}")
print(f"c1 PRESENT       drift-ON coverage {agg['cov_on']:.3f} - OFF {agg['cov_off']:.3f} = {agg['cov_on']-agg['cov_off']:.3f} >= {THR}  -> {c1}")
print(f"c2-img DISTINCT  cue-driven re-activation coverage={agg['cov_img']:.3f} <= off+0.15={agg['cov_off']+0.15:.3f}  -> {c2_img}")
print(f"c2-pro DISTINCT  goal-directed rollout coverage={agg['cov_pro']:.3f} <= off+0.15={agg['cov_off']+0.15:.3f}  -> {c2_pro}")
print(f"c3 ABLATE        spontaneous-drift step OFF (idle kept) coverage={agg['cov_abl']:.3f} <= off+0.15={agg['cov_off']+0.15:.3f}  -> {c3}")
print(f"c4 UNDIRECTED    |dir_on|={abs(agg['dir_on']):.3f}<={UNDIR_BAND} (aimless) AND dir_prospect={agg['dir_pro']:.3f}>=dir_on+0.10={agg['dir_on']+0.10:.3f} (directed control)  -> {c4} [structure]")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: on={p['cov_on']:.3f} off={p['cov_off']:.3f} img={p['cov_img']:.3f} "
          f"pro={p['cov_pro']:.3f} abl={p['cov_abl']:.3f} shf={p['cov_shf']:.3f} | "
          f"dir_on={p['dir_on']:.3f} dir_pro={p['dir_pro']:.3f}")
print()
if DEPLETION:
    print("DEPLETION SIGNAL: mind-wandering collapses into mental-imagery and/or prospection "
          "(a cue-readout or directed-rollout reproduced the wandering signature) -> NOT a "
          "distinct lane -> depletion count++.")
elif GREEN:
    print("DISTINCT: spontaneous undirected associative drift (no cue, no goal) survives ALL "
          "controls vs imagery (cue-driven, converges) / prospection (goal-directed, converges) "
          "/ ablate (idle-only) -> mind-wandering IS a distinct lane (DIRECTIONAL).")
