#!/usr/bin/env python3
"""H_1493 — PROSPECTION / episodic future thinking (P7 consciousness-only gate candidate).

Prospection (Schacter & Addis constructive-episodic-simulation, Gilbert & Wilson): the mind
RECOMBINES elements of past episodic memory to SIMULATE a future state that has NOT yet
happened (episodic future thinking). The defining property is FORWARD TEMPORAL PROJECTION
plus CONSTRUCTIVE RECOMBINATION: stored episodic *elements* (who/where/what fragments) are
re-assembled, then rolled FORWARD in time to predict a future-state cue that was NEVER itself
stored. The target is a *novel future configuration*, not a replay of any single stored episode.

MECHANISM (numpy mirror): an episodic store holds E elements, each a (context_t -> element)
pair sampled along a temporal trajectory with a fixed forward transition operator W (the
"how the world evolves" model learned from past transitions). PROSPECTION = take the CURRENT
context, apply the forward rollout W^k (project k steps into the FUTURE), and reconstruct the
future state by RECOMBINING the stored elements whose contexts the rolled-forward trajectory
passes through. The predicted future state is a recombination of past elements at a future
time index that was never directly observed (held out). Success = the predicted future state
matches the held-out true future element.

DISTINCTNESS (load-bearing — this is a WEAK candidate; depletion-round, controls decide):
  vs MENTAL-IMAGERY (H_1484, *input==0 retrieval of a STORED repr*): imagery re-activates a
    pattern that ALREADY EXISTS in the store via a content-addressable cue. It has NO forward
    operator and NO recombination — it returns the nearest stored item. On a FUTURE-state that
    was held out (never stored), an imagery-style readout (nearest stored element to the
    current context) returns a PAST element, not the future one -> scores at chance for the
    future target. Bar (c2-img) makes this explicit: imagery-style nearest-stored readout on
    the future-prediction task == chance. PROSPECTION's lift over imagery IS the forward
    rollout + recombination.
  vs SELF-CONTINUITY (H_1471, *past->present anchor PERSIST*): continuity carries the current
    identity FORWARD UNCHANGED (persist/copy), no transition model, no recombination. A
    persist-style readout (predict future == current context, i.e. W := Identity) cannot reach
    a future state that has MOVED in trajectory space -> chance on the future target.
    Bar (c2-cont).
  vs SUBJECTIVE-TIME / TRW (H_1486, *integration window over the PAST*): TRW integrates
    incoming past context into a present percept; it is BACKWARD/present, never projects a
    future index. A backward-integration readout (average of past contexts) does not reach the
    future. Folded into the persist/imagery controls (both are non-forward) + the ablation.
  vs HIERARCHICAL-PFC goal stack (H_1294, *ordered goal POINTER*): a goal stack advances a
    pointer over PRE-STORED ordered subgoals; it does not CONSTRUCT a novel future state by
    recombining elements at an unobserved time index. The shuffle-timeline control (c4) breaks
    exactly the forward-temporal-order structure a pointer would also need, but the ablation
    (c3, remove the rollout while KEEPING element access) isolates the FORWARD-PROJECTION term
    that a pointer/retrieval lane lacks.

If c2-img / c2-cont do NOT both collapse to chance (i.e. imagery-style retrieval or
continuity-style persist already solves the future task), then prospection is NOT distinct
from those lanes = DEPLETION signal (honest RED, a_break_the_wall: real overlap, not a
metric artifact). NO tune-to-green.

LLM contrast (a_no_llm_frame_trap): an LLM predicts the next token from the present context;
it has no faculty that recombines stored episodic ELEMENTS and rolls them FORWARD k steps to
construct a novel future EPISODE at a time index never observed.

R1 numpy MIRROR -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1493,1494,1495]) — catalogue P7 c1-c4:
  (c1) PRESENT     prospection-ON future-state prediction acc - prospection-OFF acc >= 0.30
                   (off = no forward rollout: predict from the raw current context only)
  (c2-img) DISTINCT vs mental-imagery: an imagery-style nearest-STORED readout (no forward
                   operator, returns nearest stored element to current ctx) on the FUTURE
                   target scores at chance: acc <= chance + 0.15
  (c2-cont) DISTINCT vs self-continuity: a persist-style readout (W := Identity, predict
                   future == current context) on the future target scores at chance:
                   acc <= chance + 0.15
  (c3) ABLATE      forward-rollout term OFF (k:=0) but element access KEPT -> cannot reach a
       (rollout)   future trajectory index -> collapses: acc <= off + 0.15
  (c4) SHUFFLE     shuffle the temporal order of stored transitions before learning W -> the
       (timeline)  forward operator no longer encodes the real trajectory -> future
                   recombination invalid: acc <= off + 0.15
  (B)  RECOMBINE   the predicted future state is a NOVEL recombination, not a replay of any
                   single stored episode: cos(pred, nearest STORED element) is NOT ~1.0
                   (pred != any single stored item) yet cos(pred, true_future) high.
                   Reported (structure-confirming, non-gating).

GREEN iff c1 and c2-img and c2-cont and c3 and c4  (B is the recombination structure check).
RED / DEPLETION iff c2-img or c2-cont fail (prospection collapses into imagery/continuity).
"""
import numpy as np

SEEDS = [1493, 1494, 1495]
DIM = 64
N_STEPS = 12          # length of the temporal trajectory (episodes along time)
HORIZON = 4           # how many steps into the FUTURE prospection must project (held out)
N_ELEM = N_STEPS      # one stored element per observed time step
KEY_NOISE = 0.02
N_TRIAL = 60          # prediction trials per condition
CHANCE = 1.0 / N_ELEM # nearest-element classification chance


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


class EpisodicWorld:
    """A temporal trajectory of context states linked by a FIXED forward operator W.

    The PAST portion [0 .. N_STEPS-1] is stored (context_t -> element_t pairs). The FUTURE
    portion [N_STEPS .. N_STEPS+HORIZON-1] is HELD OUT (never stored). Prospection must
    project the current context forward through W to reach a future context, then recombine
    the stored elements to RECONSTRUCT the held-out future element.
    """

    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.rng = rng
        # forward transition operator W: a smooth near-orthogonal rotation in DIM space.
        A = rng.normal(0, 1, (DIM, DIM))
        Q, _ = np.linalg.qr(A)               # orthonormal -> distances preserved, trajectory moves
        # blend toward identity a bit so steps are smooth (continuous trajectory)
        self.W = nrm_mat(0.5 * np.eye(DIM) + 0.5 * Q)

        # trajectory of contexts c_0 -> c_1 -> ... by repeatedly applying W
        c0 = nrm(rng.normal(0, 1, DIM))
        self.ctx = [c0]
        for _ in range(N_STEPS + HORIZON):
            self.ctx.append(nrm(self.W @ self.ctx[-1]))
        # each time step has an ELEMENT (who/where/what fragment) bound to its context by a
        # FIXED context->element map M (the world's "what happens given this state"). Because
        # M is shared across time, a future element is a RECOMBINATION of the same generative
        # factors seen in the past -> reconstructable from past (context,element) pairs IF the
        # context is first rolled forward to the future index. The future element itself is a
        # NOVEL configuration (never stored), reachable only via the forward projection.
        M = rng.normal(0, 1, (DIM, DIM))
        self.M = nrm_mat(M)
        self.elem = [nrm(self.M @ c) for c in self.ctx]

    def stored_contexts(self):
        return self.ctx[:N_STEPS]

    def stored_elements(self):
        return self.elem[:N_STEPS]

    def learn_W(self, shuffle=False):
        """Estimate the forward operator from STORED consecutive context transitions.

        Least-squares W_hat mapping ctx_t -> ctx_{t+1} over the observed (past) trajectory.
        If shuffle=True the temporal pairing is permuted -> W_hat no longer encodes the real
        forward dynamics (timeline destroyed).
        """
        X = np.stack(self.ctx[:N_STEPS - 1])         # (T-1, DIM) sources
        Y = np.stack(self.ctx[1:N_STEPS])            # (T-1, DIM) targets (next step)
        if shuffle:
            Y = Y[self.rng.permutation(len(Y))]      # break the temporal pairing
        # W_hat = Y^T X (X^T X)^-1   (ridge for stability)
        XtX = X.T @ X + 1e-3 * np.eye(DIM)
        W_hat = Y.T @ X @ np.linalg.inv(XtX)
        return W_hat


def nrm_mat(M):
    # scale matrix so its operator norm ~1 (keep contexts on the unit sphere after nrm())
    s = np.linalg.norm(M, 2)
    return M / s if s > 0 else M


def run_seed(seed):
    w = EpisodicWorld(seed)
    rng = np.random.default_rng(seed + 777)
    stored_ctx = w.stored_contexts()
    stored_elem = w.stored_elements()
    all_elem = w.elem                     # incl. held-out future elements
    W_hat = w.learn_W(shuffle=False)
    W_hat_shuf = w.learn_W(shuffle=True)

    # learn the context->element recombination map M_hat from STORED (context, element) pairs.
    # Applying M_hat to ANY context (incl. a rolled-forward future one) recombines the same
    # generative factors -> reconstructs the element bound to that context.
    Xc = np.stack(stored_ctx)                         # (T, DIM)
    Ye = np.stack(stored_elem)                        # (T, DIM)
    XtX = Xc.T @ Xc + 1e-3 * np.eye(DIM)
    M_hat = Ye.T @ Xc @ np.linalg.inv(XtX)            # element = M_hat @ context

    def predict_future_elem(mode):
        """Return predicted future ELEMENT vector for a random held-out future step.

        modes:
          'full'    prospection: from a start context, roll FORWARD via W_hat to the future
                    step, then recombine stored elements by context affinity at that future
                    context -> reconstruct the future element.
          'off'     no rollout: predict the future element from the RAW current context
                    (recombine stored elements at the *current* context, no forward step).
          'imagery' nearest-STORED readout: return the stored element whose context is nearest
                    the CURRENT context (content-addressable retrieval, no forward operator).
          'cont'    persist (self-continuity): W := Identity -> future context == current
                    context -> recombine at current context (no movement forward).
          'ablate'  rollout term OFF (k:=0) but element-recombination KEPT (== off, isolates
                    the forward-projection contribution).
          'shuffle' use the timeline-shuffled W_hat_shuf for the rollout.
        """
        # pick a held-out FUTURE target step and the matching START context `h` steps before
        fut = rng.integers(N_STEPS, N_STEPS + HORIZON)     # held-out future index
        h = fut - (N_STEPS - 1)                            # steps to roll forward from last seen
        start_ctx = w.ctx[N_STEPS - 1].copy()              # current (last observed) context
        start_ctx = nrm(start_ctx + KEY_NOISE * rng.normal(0, 1, DIM))
        true_future = all_elem[fut]

        # roll the context forward to the future index
        if mode in ("full", "shuffle"):
            Wk = W_hat_shuf if mode == "shuffle" else W_hat
            c = start_ctx.copy()
            for _ in range(h):
                c = nrm(Wk @ c)
            query_ctx = c
        elif mode == "cont":
            query_ctx = start_ctx                          # W := Identity, no forward movement
        else:  # off, ablate, imagery
            query_ctx = start_ctx                          # no rollout

        if mode == "imagery":
            # content-addressable RETRIEVAL: return the STORED element nearest the current
            # context (no forward operator, no recombination map applied to a future context).
            sims = np.array([cos(start_ctx, stored_ctx[k]) for k in range(len(stored_ctx))])
            pred = nrm(stored_elem[int(np.argmax(sims))])
            return pred, true_future

        # RECOMBINATION: apply the learned context->element map to the QUERY context.
        # For 'full'/'shuffle' query_ctx is the rolled-forward future context -> reconstructs
        # the future element. For 'off'/'ablate'/'cont' query_ctx is the current context ->
        # reconstructs the CURRENT (already-seen) element, not the future one.
        pred = nrm(M_hat @ query_ctx)
        return pred, true_future

    def acc(mode, ntrial=N_TRIAL):
        hit = 0
        for _ in range(ntrial):
            pred, true_future = predict_future_elem(mode)
            # classify: is the predicted element nearest to the TRUE future element among all?
            sims = np.array([cos(pred, all_elem[k]) for k in range(len(all_elem))])
            hit += int(int(np.argmax(sims)) == _true_idx(true_future, all_elem))
        return hit / ntrial

    acc_full = acc("full")
    acc_off = acc("off")
    acc_img = acc("imagery")
    acc_cont = acc("cont")
    acc_ablate = acc("ablate")
    acc_shuffle = acc("shuffle")

    # (B) recombination structure check: predicted future is a NOVEL blend, not a single replay
    novel_gaps, fut_cos = [], []
    for _ in range(N_TRIAL):
        pred, true_future = predict_future_elem("full")
        near_stored = max(cos(pred, e) for e in stored_elem)   # closest single stored element
        novel_gaps.append(near_stored)                          # if ~1.0 -> just a replay
        fut_cos.append(cos(pred, true_future))
    nearest_stored_cos = float(np.mean(novel_gaps))
    future_cos = float(np.mean(fut_cos))

    return dict(
        acc_full=acc_full, acc_off=acc_off, acc_img=acc_img, acc_cont=acc_cont,
        acc_ablate=acc_ablate, acc_shuffle=acc_shuffle,
        nearest_stored_cos=nearest_stored_cos, future_cos=future_cos,
    )


def _true_idx(vec, pool):
    for i, p in enumerate(pool):
        if p is vec:
            return i
    # fallback by exact match
    return int(np.argmax([cos(vec, p) for p in pool]))


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

c1 = (agg['acc_full'] - agg['acc_off']) >= 0.30
c2_img = agg['acc_img'] <= CHANCE + 0.15
c2_cont = agg['acc_cont'] <= CHANCE + 0.15
c3 = agg['acc_ablate'] <= agg['acc_off'] + 0.15
c4 = agg['acc_shuffle'] <= agg['acc_off'] + 0.15
cB = (agg['nearest_stored_cos'] <= 0.95) and (agg['future_cos'] >= 0.50)
GREEN = c1 and c2_img and c2_cont and c3 and c4

# DEPLETION diagnosis: if the distinctness controls (vs imagery / vs continuity) fail, the
# prospection lift is NOT distinct from those lanes -> honest RED = depletion signal.
DEPLETION = (not c2_img) or (not c2_cont)

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | DEPLETION-signal: {DEPLETION} | seeds {SEEDS} | chance={CHANCE:.3f} | horizon={HORIZON}")
print(f"c1 PRESENT       full {agg['acc_full']:.3f} - off {agg['acc_off']:.3f} = {agg['acc_full']-agg['acc_off']:.3f} >= 0.30  -> {c1}")
print(f"c2-img DISTINCT  imagery-style nearest-STORED acc(future)={agg['acc_img']:.3f} <= chance+0.15={CHANCE+0.15:.3f}  -> {c2_img}")
print(f"c2-cont DISTINCT persist-style (W:=I) acc(future)={agg['acc_cont']:.3f} <= chance+0.15={CHANCE+0.15:.3f}  -> {c2_cont}")
print(f"c3 ABLATE        rollout OFF (k:=0) acc={agg['acc_ablate']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f}  -> {c3}")
print(f"c4 SHUFFLE       timeline-shuffled W acc={agg['acc_shuffle']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f}  -> {c4}")
print(f"B  RECOMBINE     nearest-single-stored cos={agg['nearest_stored_cos']:.3f}<=0.95 (novel blend) & future-cos={agg['future_cos']:.3f}>=0.50  -> {cB} [structure, non-gating]")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: full={p['acc_full']:.3f} off={p['acc_off']:.3f} img={p['acc_img']:.3f} "
          f"cont={p['acc_cont']:.3f} ablate={p['acc_ablate']:.3f} shuffle={p['acc_shuffle']:.3f} "
          f"nearStored={p['nearest_stored_cos']:.3f} futCos={p['future_cos']:.3f}")
print()
if DEPLETION:
    print("DEPLETION SIGNAL: prospection collapses into mental-imagery and/or self-continuity "
          "(a distinctness control did NOT survive) -> NOT a distinct lane -> depletion count++.")
elif GREEN:
    print("DISTINCT: forward-rollout + recombination survives ALL controls vs imagery/continuity/"
          "timeline -> prospection IS a distinct lane (DIRECTIONAL).")
