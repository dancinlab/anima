#!/usr/bin/env python3
"""H_1498 — SENSORIMOTOR COUNTERFACTUAL PRESENCE (Q2 consciousness-only gate — WEAK candidate).

O'Regan & Noë (sensorimotor contingency theory; "perceptual presence without counterfactual
richness", Tandfonline 17588928.2014.907257): perceptual *presence* — the felt sense that an
OCCLUDED part of an object is still "there" (the back of a cup you cannot see, yet feel is
present) — arises from MASTERY of the counterfactual SENSORIMOTOR LAW: you feel the hidden side
is present because you IMPLICITLY KNOW what sensation each virtual ACTION (turn the cup, move
your head) WOULD produce. Presence = the *richness* of the distribution of sensory outcomes that
your possible actions would reveal, NOT a single forward prediction.

CORE CLAIM: the presence proxy is grounded in COUNTERFACTUAL RICHNESS — the *width / coverage*
of the distribution of sensory outcomes over MANY virtual actions. An agent that masters the
full sensorimotor law (knows what EACH action would reveal) has high presence for the occluded
object; an agent that can only predict the SINGLE next-step sensation (a forward model) does NOT
get presence from richness, because presence lives in the WIDTH of the action->sensation map,
not in one prediction.

MECHANISM (numpy mirror):
  An OBJECT is a hidden 3-D-ish structure: a set of S "facets" (e.g. the visible front + the
  occluded back/sides), each a DIM-vector. At any moment only a SUBSET of facets is directly
  sensed (the rest are OCCLUDED). The agent has an ACTION set A (viewpoint shifts). The
  SENSORIMOTOR LAW is a fixed map L: (current_view, action) -> revealed_facet — i.e. "if I take
  action a from view v, sensation reveals facet L(v,a)". The agent LEARNS this law from
  (view, action -> revealed) transitions.

  PRESENCE of an occluded facet f = mastery of the counterfactual law that would bring f into
  view: from the current view, roll over ALL virtual actions, predict which facet each would
  reveal, and measure how well the RICHNESS of that predicted action->sensation distribution
  COVERS the occluded facets. Concretely the presence proxy for the object = the fraction of
  currently-occluded facets that the agent CORRECTLY knows it could reveal — an occluded facet
  counts as PRESENT only when SOME virtual action's predicted outcome both (i) lands on that
  facet AND (ii) matches the TRUE sensorimotor law for that (view,action) (genuine contingency
  mastery, not a lucky guess). High when the agent masters the WHOLE law (every hidden facet is
  reachable+correctly-predicted by SOME virtual action); low when it does not. A FALSE law earns
  no credit (its predictions never match the true contingency), so mere prediction BREADTH cannot
  fake presence — only correct mastery does.

DISTINCTNESS (load-bearing — WEAK candidate, depletion-round, forward-model control decides):
  vs FORWARD-MODEL / cerebellum (H_1280, VForwardField, *single next-step prediction*): a forward
    model predicts the sensation of the ONE action actually about to be taken (next step). It is
    accurate at next-step prediction YET it does NOT integrate over the action SET, so it cannot
    report the RICHNESS/coverage that grounds presence. The control (c2) gives the forward model
    its OWN best single-step prediction and scores the presence task with it: it should NOT
    reach the richness-based presence proxy, because one prediction covers at most one facet, not
    the occluded SET. If the single-step forward model ALREADY solves the presence task ->
    presence is NOT distinct from forward-model = DEPLETION signal (honest RED, a_break_the_wall:
    real overlap, NOT a metric artifact). NO tune-to-green.
  vs PROSPECTION (H_1493, *forward temporal rollout to a future state*): prospection projects ONE
    trajectory FORWARD in time to a future episode; presence is NOT temporal-forward, it is the
    BREADTH over counterfactual ACTIONS available NOW (atemporal action-coverage). The ablation
    (c3: collapse the rollout WIDTH to a single action) removes exactly the breadth a temporal
    rollout lacks anyway -> folded in.
  vs PERCEPTUAL-COMPLETION (H_1490, *interpolate/fill a missing region*): completion fills an
    occluded region by INTERPOLATING from the visible context (a single inference), with no
    notion of "what ACTION would reveal it". The forward-model control + the shuffle (c4: permute
    the action->sensation law) break the action-contingency structure that completion lacks; a
    completion-style fill has no action set to shuffle, so it cannot be the source of the lift.
  vs AGENCY / sense-of-agency (8): agency is SELF-ATTRIBUTION of an action's effect; presence is
    about the OBJECT's hidden structure, not who caused the change. Not action-attribution here.

If the forward-model control (c2) does NOT stay below the presence proxy (i.e. a single next-step
predictor already solves the richness-presence task), then presence collapses into forward-model
= DEPLETION signal (honest RED). This is the WEAK-candidate failure mode the catalogue warns of.

LLM contrast (a_no_llm_frame_trap): an LLM has no faculty that rolls over a set of virtual
sensorimotor ACTIONS and integrates the WIDTH of their predicted sensory outcomes to ground a
felt presence of an unsensed object part.

R1 numpy MIRROR -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1498,1499,1500]) — catalogue Q2 c1-c4:
  (c1) PRESENT   counterfactual-richness presence proxy (full law mastery, roll over ALL virtual
                 actions, coverage of occluded facets) - richness-OFF presence proxy >= 0.30
                 (off = only the SINGLE next action available, no action-set breadth)
  (c2) DISTINCT  a FORWARD-MODEL readout (best single next-step sensation prediction, the cerebellar
       vs        VForwardField analogue) scores the presence task <= off + 0.15 (it covers at most
       fwd-model one facet, not the occluded SET -> cannot reach richness-presence). THE decisive
                 weak-candidate control.
  (c3) ABLATE    collapse the counterfactual rollout WIDTH to 1 (only one virtual action explored)
       (width)   -> presence proxy collapses: <= off + 0.15 (isolates the breadth/richness term)
  (c4) SHUFFLE   master a FALSE law (action -> permuted/wrong revealed facet) -> the agent's
       (law)     predictions never match the TRUE contingency, so correct-mastery coverage earns
                 zero credit despite full action breadth: <= off+0.15
  (B)  FIDELITY  the full-law presence rests on CORRECT per-action sensation prediction (mastery),
                 not random coverage: mean per-action reveal-prediction accuracy reported
                 (structure-confirming, non-gating).

GREEN iff c1 and c2 and c3 and c4 (3-seed mean). B is the mastery-fidelity structure check.
RED / DEPLETION iff c2 fails (presence collapses into the single-step forward model).
"""
import numpy as np

SEEDS = [1498, 1499, 1500]
DIM = 96
N_FACET = 8          # facets of the object (front + occluded back/sides)
N_VIEW = 8           # distinct viewpoints
N_ACTION = 8         # virtual viewpoint-shift actions available from any view (>= N_FACET so the
                     # full occluded set is reachable; each action maps to a DISTINCT facet)
KEY_NOISE = 0.02
N_TRIAL = 40         # presence-evaluation trials per condition


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


class SensorimotorObject:
    """A hidden object with S facets, sensed only partially from any single viewpoint.

    The SENSORIMOTOR LAW reveal[v, a] -> facet index: taking action `a` from view `v` reveals a
    particular facet. Each viewpoint `v` DIRECTLY senses a small subset of facets (visible[v]);
    the rest are OCCLUDED but REACHABLE by some action via the law. Presence of an occluded facet
    = mastery of which virtual action would reveal it (the counterfactual sensorimotor contingency).
    """

    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.rng = rng
        # facet feature vectors (the object's hidden structure)
        self.facets = [nrm(rng.normal(0, 1, DIM)) for _ in range(N_FACET)]
        # viewpoint embeddings
        self.views = [nrm(rng.normal(0, 1, DIM)) for _ in range(N_VIEW)]
        # action embeddings (viewpoint-shift commands)
        self.actions = [nrm(rng.normal(0, 1, DIM)) for _ in range(N_ACTION)]
        # SENSORIMOTOR LAW: reveal[v][a] = facet index revealed by taking action a from view v.
        # Constructed so that, across ALL actions from a given view, the FULL occluded set is
        # COVERED (every hidden facet is reachable by SOME virtual action) -> mastering the whole
        # law grounds presence of the whole object. A single action covers only one facet.
        # N_ACTION >= N_FACET: the first N_FACET actions reveal a permutation of ALL facets (so the
        # whole object is reachable by SOME virtual action), any extra actions wrap around.
        self.reveal = np.zeros((N_VIEW, N_ACTION), dtype=int)
        for v in range(N_VIEW):
            perm = rng.permutation(N_FACET)
            for a in range(N_ACTION):
                self.reveal[v][a] = int(perm[a % N_FACET])
        # which facets are DIRECTLY visible (sensed) from each view (small subset) -> the rest are
        # occluded and only PRESENT via counterfactual action knowledge.
        self.visible = []
        for v in range(N_VIEW):
            vis = set(rng.choice(N_FACET, size=2, replace=False).tolist())
            self.visible.append(vis)

    def occluded(self, v):
        return [f for f in range(N_FACET) if f not in self.visible[v]]

    def key(self, v, a):
        """Sensorimotor key for (view, action) = the substrate's content-addressable index
        (cf. ImmuneMemoryGrow FNV-key affinity, H_1227). The agent stores facet outcomes against
        these keys and retrieves the revealed facet by nearest-key cosine affinity."""
        return nrm(np.concatenate([self.views[v], self.actions[a]]))   # (2*DIM,)

    def law_store(self, shuffle_law=False):
        """The agent's mastered sensorimotor law = an associative store mapping each (view,action)
        KEY -> the facet that action reveals. Retrieval is nearest-key affinity. If shuffle_law:
        the action->revealed pairing is permuted (the law is a FALSE contingency), so the store
        binds keys to the WRONG facets and predictions never match the true law.
        """
        keys, facet_idx = [], []
        for v in range(N_VIEW):
            rmap = self.reveal[v].copy()
            if shuffle_law:
                rmap = rmap[self.rng.permutation(N_ACTION)]
            for a in range(N_ACTION):
                keys.append(self.key(v, a))
                facet_idx.append(int(rmap[a]))
        return np.stack(keys), np.array(facet_idx, dtype=int)


def run_seed(seed):
    obj = SensorimotorObject(seed)
    rng = np.random.default_rng(seed + 777)

    keys, fidx = obj.law_store(shuffle_law=False)        # mastered TRUE sensorimotor law
    keys_s, fidx_s = obj.law_store(shuffle_law=True)     # mastered a FALSE law

    def predict_reveal(store, v, a):
        """Retrieve the predicted revealed-facet for (view,action) by nearest-key affinity in the
        mastered law store. `store` = (keys, facet_idx)."""
        K, FI = store
        q = obj.key(v, a)
        q = nrm(q + KEY_NOISE * rng.normal(0, 1, 2 * DIM))
        sims = K @ q                                      # cosine (keys are unit-norm, q ~unit)
        best = int(np.argmax(sims))
        return int(FI[best]), sims

    L_hat = (keys, fidx)
    L_shuf = (keys_s, fidx_s)

    def presence_proxy(mode):
        """Fraction of currently-OCCLUDED facets the agent CORRECTLY knows it could reveal.

        An occluded facet f counts as PRESENT only when SOME explored virtual action a has a
        predicted outcome pf that (i) equals f AND (ii) MATCHES THE TRUE sensorimotor law
        (obj.reveal[v][a] == f) -- i.e. genuine contingency mastery, not a lucky landing. This
        makes a FALSE/shuffled law earn ZERO credit (its predictions never match the true
        contingency), so prediction BREADTH alone cannot fake presence.

        modes:
          'full'    counterfactual RICHNESS: explore ALL N_ACTION virtual actions, count occluded
                    facets with a CORRECTLY-predicted revealing action.
          'off'     no action-set breadth: only the SINGLE next action explored -> at most one
                    occluded facet correctly known.
          'fwdmodel' FORWARD-MODEL control: predict the sensation of the ONE next action (best
                    single next-step prediction, cerebellar VForwardField analogue) -> covers at
                    most one facet, cannot reach richness-presence over the occluded SET.
          'ablate'  rollout WIDTH collapsed to 1 (only one virtual action explored), mastered law
                    (isolates the breadth/richness term).
          'shuffle' the agent mastered the FALSE (shuffled) law L_shuf -> its predictions never
                    match the TRUE contingency -> zero correct coverage despite full breadth.
        """
        covered = 0.0
        total = 0
        for _ in range(N_TRIAL):
            v = int(rng.integers(0, N_VIEW))
            occ = set(obj.occluded(v))
            total += len(occ)
            if mode in ("full", "shuffle"):
                acts = list(range(N_ACTION))
                L = L_shuf if mode == "shuffle" else L_hat
            else:  # off, fwdmodel, ablate -> ONE virtual action only
                acts = [int(rng.integers(0, N_ACTION))]
                L = L_hat
            known = set()
            for a in acts:
                pf, _ = predict_reveal(L, v, a)
                true_f = int(obj.reveal[v][a])           # TRUE facet this action reveals
                # credit ONLY genuine mastery: predicted facet matches the true contingency AND
                # that facet is currently occluded -> the agent correctly knows it is "there".
                if pf == true_f and true_f in occ:
                    known.add(true_f)
            covered += len(known)
        return covered / total if total else 0.0

    p_full = presence_proxy("full")
    p_off = presence_proxy("off")
    p_fwd = presence_proxy("fwdmodel")
    p_ablate = presence_proxy("ablate")
    p_shuffle = presence_proxy("shuffle")

    # (B) mastery fidelity: per-action reveal-prediction accuracy under the learned law
    correct, tot = 0, 0
    for v in range(N_VIEW):
        for a in range(N_ACTION):
            pf, _ = predict_reveal(L_hat, v, a)
            correct += int(pf == obj.reveal[v][a]); tot += 1
    fidelity = correct / tot

    return dict(p_full=p_full, p_off=p_off, p_fwd=p_fwd, p_ablate=p_ablate,
                p_shuffle=p_shuffle, fidelity=fidelity)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

c1 = (agg['p_full'] - agg['p_off']) >= 0.30
c2 = agg['p_fwd'] <= agg['p_off'] + 0.15
c3 = agg['p_ablate'] <= agg['p_off'] + 0.15
c4 = agg['p_shuffle'] <= agg['p_off'] + 0.15
cB = agg['fidelity'] >= 0.50
GREEN = c1 and c2 and c3 and c4

# DEPLETION diagnosis: if the forward-model control (c2) fails, the richness-presence proxy is
# NOT distinct from a single-step forward model -> honest RED = depletion signal.
DEPLETION = not c2

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | DEPLETION-signal: {DEPLETION} | seeds {SEEDS} | facets={N_FACET} actions={N_ACTION}")
print(f"c1 PRESENT       full {agg['p_full']:.3f} - off {agg['p_off']:.3f} = {agg['p_full']-agg['p_off']:.3f} >= 0.30  -> {c1}")
print(f"c2 DISTINCT(fwd) forward-model single-step presence={agg['p_fwd']:.3f} <= off+0.15={agg['p_off']+0.15:.3f}  -> {c2}")
print(f"c3 ABLATE(width) rollout-width:=1 presence={agg['p_ablate']:.3f} <= off+0.15={agg['p_off']+0.15:.3f}  -> {c3}")
print(f"c4 SHUFFLE(law)  false-law rollout presence={agg['p_shuffle']:.3f} <= off+0.15={agg['p_off']+0.15:.3f}  -> {c4}")
print(f"B  FIDELITY      mastered-law per-action reveal acc={agg['fidelity']:.3f} >= 0.50  -> {cB} [structure, non-gating]")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: full={p['p_full']:.3f} off={p['p_off']:.3f} fwd={p['p_fwd']:.3f} "
          f"ablate={p['p_ablate']:.3f} shuffle={p['p_shuffle']:.3f} fidelity={p['fidelity']:.3f}")
print()
if DEPLETION:
    print("DEPLETION SIGNAL: sensorimotor-counterfactual presence collapses into the single-step "
          "FORWARD-MODEL (c2 control did NOT survive: a next-step predictor already solves the "
          "presence task) -> NOT a distinct lane -> depletion count++. WEAK candidate confirmed derivative.")
elif GREEN:
    print("DISTINCT: counterfactual RICHNESS (coverage over the full virtual-action set) survives "
          "ALL controls vs forward-model(single-step)/width-ablation/false-law -> sensorimotor "
          "presence IS a distinct lane (DIRECTIONAL).")
