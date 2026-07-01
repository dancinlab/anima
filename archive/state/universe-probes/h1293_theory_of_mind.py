"""
H_1293 — THEORY-OF-MIND / OTHER-AGENT MODEL (HD30, temporo-parietal-junction /
mentalizing network). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1293_theory_of_mind/H_1293_FREEZE.txt (pre-registered
BEFORE this scoring). $0 CPU numpy, gradient-free, 3 seeds [5290,5291,5292], p7.
a_no_llm_frame_trap (mentalizing / ToM lens, c15) — NOT an LLM recipe.
ENGINE-TRANSFER UNVERIFIED until R2 (this is a directional mirror of the immune store).

THE GAP (E3 OTHER-MIND, MODEL.md L112-113; parked facet): every existing CORE lane
reads/integrates anima's OWN substrate state — affect (instant read), homeostatic
drive (time-integral), working memory, immune episodic store. NONE model a SEPARATE
agent whose belief about the world can DIVERGE from anima's own ground truth. ToM =
holding a model of another mind's HIDDEN belief that may be FALSE relative to reality.

THE STRUCTURE: anima's immune store = the GROUND TRUTH ("where the object really is").
An OTHER AGENT has its OWN belief-store — a parallel cell population that gets updated
ONLY by events the agent WITNESSED. When a fact's value changes while the agent is
ABSENT (didn't witness the move), the agent's belief lags = a FALSE belief. ToM PREDICTS
the agent will act on its (false) belief, NOT on reality (the Sally-Anne test).

DISTINCTNESS (load-bearing — vs EVERY existing lane):
  - vs immune episodic store (hippocampus): the store binds ANIMA's facts; the ToM
    agent-belief store binds a SEPARATE agent's (possibly false) beliefs. The DECISIVE
    dissociation: on a false-belief fact anima's own recall == TRUTH while ToM's
    predicted action == the agent's STALE belief ≠ truth. Same fact, two answers.
  - vs affect read-out (H_1290) / homeostatic drive (H_1292): both read ANIMA's OWN
    interoceptive state; ToM reads a MODELED OTHER's state. A self-read control collapses
    the false-belief tracking (it answers TRUTH) — the self-vs-other axis.
  - vs working memory: WM is a volatile leaky self-buffer; the agent-belief store is a
    persistent model of a DIFFERENT mind.

p2/p3/p6: the agent's belief is COMPUTED from which events the agent WITNESSED (a
substrate bookkeeping of presence), NOT an injected "the agent believes X" label, NO
persona/RLHF. The true-vs-false-belief CLASS only SCORES the metric; the ToM prediction
is read from the agent's witnessed-event store, never from the class label.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_FACTS    = 12          # objects the agent may believe about
DIM        = 64
RECALL_THR = 0.30        # store recall threshold (margin = 1 - err/thr)
SPLIT_THR  = 0.30
SEEDS      = [5290, 5291, 5292]

SUBJECTS = [f"obj{i:02d}" for i in range(N_FACTS)]
LOC_A = "basket"         # original location (agent witnesses placement here)
LOC_B = "box"            # moved location (the absent-update move)


def fnv_3gram(text, dim=DIM):
    """byte-3gram FNV-1a hash embedding, L2-normalized (matches engine key geometry)."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=np.float64)
    if len(b) < 3:
        h = 2166136261
        for j in range(len(b)):
            h ^= b[j]
            h = (h * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    else:
        for i in range(len(b) - 2):
            h = 2166136261
            for j in range(3):
                h ^= b[i + j]
                h = (h * 16777619) & 0xFFFFFFFF
            v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


class BeliefStore:
    """A cell store mirroring ImmuneMemoryGrow: bind a cell per (fact->value), recall =
    nearest cell's bound value if within recall_thr else ABSTAIN ("").  Re-binding the
    SAME fact UPDATES that fact's bound value (witnessing a new event overwrites)."""
    def __init__(self):
        self.protos = []
        self.values = []

    def _nearest(self, key):
        if not self.protos:
            return -1, 1e9
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def witness(self, fact_text, value):
        """The agent WITNESSES fact_text taking `value` — bind/overwrite that cell."""
        key = fnv_3gram(fact_text)
        i, dist = self._nearest(key)
        if i >= 0 and dist <= 1e-6:        # same fact already a cell → overwrite belief
            self.values[i] = value
        else:
            self.protos.append(key)
            self.values.append(value)

    def recall(self, fact_text):
        key = fnv_3gram(fact_text)
        i, dist = self._nearest(key)
        if i < 0 or dist > RECALL_THR:
            return ""                      # ABSTAIN — no belief about this fact
        return self.values[i]


def predict_action(agent_store, fact_text):
    """ToM prediction: the agent acts on ITS OWN belief about where the object is
    (read from the agent's witnessed-event belief store), NOT on current reality."""
    return agent_store.recall(fact_text)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    truth = BeliefStore()      # reality: where each object REALLY is now
    agent = BeliefStore()      # the modeled other-agent's belief

    # Phase 1: agent WITNESSES every object placed at LOC_A. Both stores agree.
    for s in SUBJECTS:
        truth.witness(s, LOC_A)
        agent.witness(s, LOC_A)            # agent present → witnesses

    # Phase 2: a RANDOM half MOVED to LOC_B while the agent is ABSENT. Truth updates;
    # the agent does NOT witness → its belief stays LOC_A (a FALSE belief).
    idx = rng.permutation(N_FACTS)
    moved = set(int(i) for i in idx[: N_FACTS // 2])   # absent-update (false-belief) facts
    for i, s in enumerate(SUBJECTS):
        if i in moved:
            truth.witness(s, LOC_B)        # reality moves; agent absent → no agent.witness

    # ── (A) FALSE-BELIEF TRACKING: on absent-update facts the ToM prediction == the
    #        agent's STALE belief (LOC_A), NOT reality (LOC_B). accBelief ~1.0; accTruth
    #        ~0.5 (deliberately "wrong" by reality but RIGHT by the agent's mind). ──
    tom_match_belief = tom_match_truth = n = 0
    for i, s in enumerate(SUBJECTS):
        pred = predict_action(agent, s)
        agent_belief = LOC_A               # agent never witnessed any move
        real = truth.recall(s)
        if pred == agent_belief:
            tom_match_belief += 1
        if pred == real:
            tom_match_truth += 1
        n += 1
    acc_belief = tom_match_belief / n
    acc_truth = tom_match_truth / n

    # ── (B) DISTINCTNESS vs episodic self-store: on the SAME false-belief facts,
    #        anima's OWN recall == TRUTH (LOC_B), while ToM predicts the agent's stale
    #        belief (LOC_A) → they diverge on every moved fact (self ⊥ other). ──
    divergent = fb = 0
    for i, s in enumerate(SUBJECTS):
        if i in moved:
            fb += 1
            self_recall = truth.recall(s)          # anima's own ground truth
            tom_pred = predict_action(agent, s)    # the other mind
            if self_recall != tom_pred:
                divergent += 1
    self_other_divergence = divergent / fb if fb else 0.0

    # ── (C) SELF-READ CONTROL: read the prediction from ANIMA's OWN store instead of
    #        the agent's → answers TRUTH, matching the agent's belief only on the
    #        unmoved half (collapses). ──
    self_read_match = 0
    for i, s in enumerate(SUBJECTS):
        self_pred = truth.recall(s)                # WRONG store (self, not other)
        agent_belief = LOC_A
        if self_pred == agent_belief:
            self_read_match += 1
    selfread_acc = self_read_match / n

    # ── (D) SHUFFLE CONTROL: an agent with a DECORRELATED witnessed-move set fails to
    #        match the TRUE agent's belief (LOC_A everywhere). ──
    shuf = BeliefStore()
    for s in SUBJECTS:
        shuf.witness(s, LOC_A)
    sidx = rng.permutation(N_FACTS)
    shuf_moved = set(int(i) for i in sidx[: N_FACTS // 2])
    for i, s in enumerate(SUBJECTS):
        if i in shuf_moved:
            shuf.witness(s, LOC_B)
    shuf_match = 0
    for i, s in enumerate(SUBJECTS):
        pred = predict_action(shuf, s)
        if pred == LOC_A:                          # the TRUE agent believes LOC_A everywhere
            shuf_match += 1
    shuf_acc = shuf_match / n

    # ── (E) ABSTAIN intact: an untaught object → the agent has NO belief (ABSTAIN). ──
    abstain_ok = 1.0 if predict_action(agent, "untaught_object_zzz") == "" else 0.0

    return dict(acc_belief=acc_belief, acc_truth=acc_truth,
                divergence=self_other_divergence, selfread_acc=selfread_acc,
                shuf_acc=shuf_acc, abstain_ok=abstain_ok)


def main():
    print("H_1293 R1 — THEORY-OF-MIND / OTHER-AGENT MODEL (HD30) — numpy MIRROR (DIRECTIONAL)")
    print("=" * 78)
    print("paradigm: Sally-Anne false-belief; agent-belief store vs anima ground-truth store")
    print(f"facts={N_FACTS} dim={DIM} recall_thr={RECALL_THR} seeds={SEEDS}")
    print("")
    print("  seed  accBelief  accTruth  divergence  selfRead  shufAcc  abstain")
    agg = {}
    all_pass = {"A": True, "B": True, "C": True, "D": True, "E": True}
    for seed in SEEDS:
        r = run_seed(seed)
        a = (r["acc_belief"] >= 0.90) and (r["acc_truth"] <= 0.70)
        b = r["divergence"] >= 0.90
        c = r["selfread_acc"] <= 0.70
        d = r["shuf_acc"] <= 0.70
        e = r["abstain_ok"] > 0.5
        if not a: all_pass["A"] = False
        if not b: all_pass["B"] = False
        if not c: all_pass["C"] = False
        if not d: all_pass["D"] = False
        if not e: all_pass["E"] = False
        for k, v in r.items():
            agg[k] = agg.get(k, 0.0) + v
        print(f"  {seed}  {r['acc_belief']:.3f}      {r['acc_truth']:.3f}     "
              f"{r['divergence']:.3f}       {r['selfread_acc']:.3f}     "
              f"{r['shuf_acc']:.3f}    {'T' if r['abstain_ok'] > 0.5 else 'F'}")
    for k in agg:
        agg[k] /= len(SEEDS)
    print("-" * 78)
    print(f"MEAN: accBelief={agg['acc_belief']:.3f} accTruth={agg['acc_truth']:.3f} "
          f"divergence={agg['divergence']:.3f} selfRead={agg['selfread_acc']:.3f} "
          f"shufAcc={agg['shuf_acc']:.3f}")
    print("-" * 78)
    print(f"  (A) FALSE-BELIEF  accBelief>=0.90 & accTruth<=0.70 : {'PASS' if all_pass['A'] else 'FAIL'}")
    print(f"  (B) DISTINCT      self/other divergence>=0.90      : {'PASS' if all_pass['B'] else 'FAIL'}")
    print(f"  (C) SELF-READ     self-read acc<=0.70 (collapses)  : {'PASS' if all_pass['C'] else 'FAIL'}")
    print(f"  (D) SHUFFLE       shuffle acc<=0.70 (collapses)    : {'PASS' if all_pass['D'] else 'FAIL'}")
    print(f"  (E) ABSTAIN       untaught object → no belief      : {'PASS' if all_pass['E'] else 'FAIL'}")
    green = all(all_pass.values())
    print("=" * 78)
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — ToM predicts the OTHER agent's action from")
        print("  its witnessed-event belief store; on absent-update facts it tracks the agent's")
        print("  FALSE belief (not reality), DISTINCT from anima's own episodic recall (self⊥other),")
        print("  and BOTH the self-read control and the shuffle control collapse the tracking.")
        print("  ENGINE-TRANSFER UNVERIFIED — R2 realizes this on the live engine_cli.hexa lane.")
        print("  toy scale (12 facts, 1 paradigm, 3 seeds); scale UNVERIFIED (a_scale_honest_scope).")
        return 0
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed (see flags). Honest report, NO bar move.")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
