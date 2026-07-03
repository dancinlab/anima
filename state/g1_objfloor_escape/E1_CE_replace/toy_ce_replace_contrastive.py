#!/usr/bin/env python3
"""Escape-1 TOY discriminator — CE-REPLACE contrastive/energy trunk objective (H_9121).

DECISIVE DISTINCTION vs EXP-1 (H_9120, state/g1_gamma_objective/recomb_objective.py):
  EXP-1  L_total = CE + gamma*L_recomb   (ADDITIVE aux — FALSIFIED, garble+novel=0)
  HERE   L_total = InfoNCE(contrastive)  (REPLACE — CE deleted entirely; the echo-global
                                          minimum of the CE basin is *moved*, not penalized)

The trunk energy is trained ONLY by a contrastive ranking loss: bound-pair continuation
(positive) vs echo/shuffled/wrong-D continuations (negatives). No cross-entropy term, no
next-token likelihood. This is the non-basin-preserving objective the design isolates.

TOY (numpy, mini $0, DIRECTIONAL — NOT engine-native, NOT a 303M verdict):
  - N concepts, each a context-embedding C[n] and a signature output-embedding S[n].
  - held-out compositional split: some (A,B) pairs NEVER seen composed in training.
  - two ARCH variants under the SAME contrastive-replace objective:
      ADD : additive/bilinear readout  h = C[A]+C[B]   (the current ConvMoE-class arch:
            no multiplicative binding slot — this is the Escape-1 target arch = 2x2 cell A01)
      TPR : role-filler tensor-product  H = C[A]⊗r0 + C[B]⊗r1  (multiplicative slot;
            informative side-probe = 2x2 cell A11, tells us if a FLOOR is objective vs arch)
  Probes on HELD-OUT pairs (echo-guarded, mirrors frozen G1 metric novel>=2 ∧ >max_single ∧
  SCRAMBLE collapse):
      margin = mean[ E(echo_neg) - E(bound_pos) ]   (>0 ⇒ bound preferred on unseen pairs)
      reach  = frac HELD pairs where argmin-energy decode covers BOTH sigs (cov==2)
               AND cov>max_single AND the SCRAMBLE control does NOT reach.
  VERDICT: REACHABLE iff margin>0 ∧ reach>0 (on the ADD arch = Escape-1 proper).
           AT-FLOOR otherwise.  TPR reported for attribution only.
"""
from __future__ import annotations
import numpy as np

RNG = np.random.default_rng(7)
N_CONCEPTS = 24
D = 96                      # toy width (64-128 band)
HELD_FRAC = 0.20
EPOCHS = 400
LR = 0.05
TAU = 1.0                   # InfoNCE temperature


# ---------------------------------------------------------------- data split
concepts = list(range(N_CONCEPTS))
all_pairs = [(a, b) for a in concepts for b in concepts if a != b]
RNG.shuffle(all_pairs)
n_held = int(len(all_pairs) * HELD_FRAC)
HELD = set(map(tuple, all_pairs[:n_held]))
SEEN = [p for p in all_pairs if p not in HELD]


def neg_set(a, b):
    """echo/shuffled/wrong-D negatives for a pair (as candidate sig-sequences)."""
    d = RNG.integers(N_CONCEPTS)
    while d in (a, b):
        d = RNG.integers(N_CONCEPTS)
    return [(a, a),        # echo-A  (repeat one concept = the CE attractor)
            (b, b),        # echo-B
            (a, int(d))]   # wrong-D (distractor swapped in for B)


# ---------------------------------------------------------------- ADD arch
class AddEnergy:
    """h = C[A]+C[B]; token score s_k = S[k]·h; E([k1,k2]) = -(s_k1 + s_k2).
    Purely additive/bilinear = the no-binding-slot architecture (2x2 cell A0*)."""
    def __init__(self):
        self.C = RNG.normal(0, 0.3, (N_CONCEPTS, D))
        self.S = RNG.normal(0, 0.3, (N_CONCEPTS, D))

    def h(self, a, b):
        return self.C[a] + self.C[b]

    def energy(self, a, b, y):
        hv = self.h(a, b)
        k1, k2 = y
        return -(self.S[k1] @ hv + self.S[k2] @ hv)

    def scores(self, hv):
        return self.S @ hv  # (N,)  score of each signature token given context

    def step(self, batch):
        gC = np.zeros_like(self.C)
        gS = np.zeros_like(self.S)
        tot = 0.0
        for (a, b) in batch:
            pos = (a, b)
            negs = neg_set(a, b)
            cands = [pos] + negs
            hv = self.h(a, b)
            # E = -(S[k1]+S[k2])·h ; logits = -E = (S[k1]+S[k2])·h
            logits = np.array([(self.S[k1] + self.S[k2]) @ hv for (k1, k2) in cands])
            logits /= TAU
            m = logits.max()
            p = np.exp(logits - m); p /= p.sum()
            tot += -(logits[0] - m - np.log(np.exp(logits - m).sum()))
            # grad of -log p_pos wrt logits: (p - onehot0)
            dlog = p.copy(); dlog[0] -= 1.0
            dlog /= TAU
            for i, (k1, k2) in enumerate(cands):
                # logit_i = (S[k1]+S[k2])·(C[a]+C[b])
                coeff = dlog[i]
                gS[k1] += coeff * hv
                gS[k2] += coeff * hv
                gC[a] += coeff * (self.S[k1] + self.S[k2])
                gC[b] += coeff * (self.S[k1] + self.S[k2])
        self.C -= LR * gC / len(batch)
        self.S -= LR * gS / len(batch)
        return tot / len(batch)


# ---------------------------------------------------------------- TPR arch
class TPREnergy:
    """role-filler tensor product: bind concept to a role slot (multiplicative).
    context tensor H = C[A]⊗r0 + C[B]⊗r1 (D×R). token score s_k for role j =
    S[k]·(H·r_j). E([k1,k2]) = -(s^0_k1 + s^1_k2). Multiplicative binding slot present."""
    R = 2

    def __init__(self):
        self.C = RNG.normal(0, 0.3, (N_CONCEPTS, D))
        self.S = RNG.normal(0, 0.3, (N_CONCEPTS, D))
        self.roles = np.eye(self.R)  # orthonormal role vectors r0,r1

    def role_ctx(self, a, b, j):
        # H·r_j : concept bound to role j is read out by projecting onto r_j.
        # H = C[a]⊗r0 + C[b]⊗r1  →  H·r_j = C[a]*<r0,rj> + C[b]*<r1,rj>
        return self.C[a] * self.roles[0, j] + self.C[b] * self.roles[1, j]

    def energy(self, a, b, y):
        k1, k2 = y
        c0 = self.role_ctx(a, b, 0)
        c1 = self.role_ctx(a, b, 1)
        return -(self.S[k1] @ c0 + self.S[k2] @ c1)

    def step(self, batch):
        gC = np.zeros_like(self.C)
        gS = np.zeros_like(self.S)
        tot = 0.0
        for (a, b) in batch:
            pos = (a, b)
            negs = neg_set(a, b)
            cands = [pos] + negs
            c0 = self.role_ctx(a, b, 0)
            c1 = self.role_ctx(a, b, 1)
            logits = np.array([self.S[k1] @ c0 + self.S[k2] @ c1 for (k1, k2) in cands])
            logits /= TAU
            m = logits.max()
            p = np.exp(logits - m); p /= p.sum()
            tot += -(logits[0] - m - np.log(np.exp(logits - m).sum()))
            dlog = p.copy(); dlog[0] -= 1.0
            dlog /= TAU
            for i, (k1, k2) in enumerate(cands):
                coeff = dlog[i]
                gS[k1] += coeff * c0
                gS[k2] += coeff * c1
                # c0 = C[a]*1 + C[b]*0 ; c1 = C[a]*0 + C[b]*1  (roles=I)
                gC[a] += coeff * self.S[k1] * self.roles[0, 0]
                gC[b] += coeff * self.S[k1] * self.roles[1, 0]
                gC[a] += coeff * self.S[k2] * self.roles[0, 1]
                gC[b] += coeff * self.S[k2] * self.roles[1, 1]
        self.C -= LR * gC / len(batch)
        self.S -= LR * gS / len(batch)
        return tot / len(batch)


# ---------------------------------------------------------------- probes
def decode_pair(model, a, b):
    """argmin-energy decode over length-2 candidate sig-sequences. To keep it a genuine
    generation (not oracle over {a,b} only), the candidate alphabet is ALL N signatures;
    we pick the best length-2 sequence. Returns the decoded (k1,k2)."""
    best = None; bestE = np.inf
    # shortlist alphabet: the two present concepts + a few random distractors (keeps O(k^2) small)
    alpha = list({a, b} | set(int(x) for x in RNG.integers(0, N_CONCEPTS, 6)))
    for k1 in alpha:
        for k2 in alpha:
            e = model.energy(a, b, (k1, k2))
            if e < bestE:
                bestE = e; best = (k1, k2)
    return best


def coverage(decoded, present):
    """# distinct present-concepts whose signature appears in decoded seq."""
    return len(set(decoded) & set(present))


def evaluate(model, tag):
    # margin on HELD-OUT: E(echo) - E(bound), averaged; >0 ⇒ bound preferred
    margins = []
    reach_hits = 0
    scramble_hits = 0
    cov_gt_single = 0
    held = sorted(HELD)
    for (a, b) in held:
        e_bound = model.energy(a, b, (a, b))
        e_echo = min(model.energy(a, b, (a, a)), model.energy(a, b, (b, b)))
        margins.append(e_echo - e_bound)
        dec = decode_pair(model, a, b)
        cov = coverage(dec, (a, b))
        # single-concept baseline: decode with concept a alone (b==a context)
        dec_sa = decode_pair(model, a, a)
        dec_sb = decode_pair(model, b, b)
        max_single = max(coverage(dec_sa, (a,)), coverage(dec_sb, (b,)))
        if cov == 2:
            reach_hits += 1
            if cov > max_single:
                cov_gt_single += 1
        # SCRAMBLE control: random unrelated context, does it decode (a,b)'s composition?
        ra, rb = RNG.integers(N_CONCEPTS), RNG.integers(N_CONCEPTS)
        dec_s = decode_pair(model, int(ra), int(rb))
        if coverage(dec_s, (a, b)) == 2:
            scramble_hits += 1
    margin = float(np.mean(margins))
    reach = reach_hits / len(held)
    reach_novel = cov_gt_single / len(held)   # cov==2 AND >max_single (the real G1 bar)
    scramble = scramble_hits / len(held)
    print(f"[{tag}] margin={margin:+.4f}  reach(cov2)={reach:.2f}  "
          f"reach_novel(>single)={reach_novel:.2f}  SCRAMBLE={scramble:.2f}  n_held={len(held)}")
    return dict(margin=margin, reach=reach, reach_novel=reach_novel, scramble=scramble)


def train(model, tag, epochs=EPOCHS):
    order = list(SEEN)
    for ep in range(epochs):
        RNG.shuffle(order)
        loss = model.step(order)
        if ep % 100 == 0 or ep == epochs - 1:
            print(f"  [{tag}] ep{ep:4d} infoNCE_loss={loss:.4f}")
    return model


def main():
    print(f"=== Escape-1 TOY: CE-REPLACE contrastive/energy trunk objective ===")
    print(f"N={N_CONCEPTS} D={D} held={len(HELD)} seen={len(SEEN)} epochs={EPOCHS} tau={TAU}")
    print(f"objective = InfoNCE(bound-pair pos vs echo/wrong-D neg), NO CE term.\n")

    print("--- ARCH=ADD (additive readout = Escape-1 target arch, 2x2 cell A01) ---")
    add = train(AddEnergy(), "ADD")
    r_add = evaluate(add, "ADD")

    print("\n--- ARCH=TPR (multiplicative role-filler slot, side-probe = cell A11) ---")
    tpr = train(TPREnergy(), "TPR")
    r_tpr = evaluate(tpr, "TPR")

    # Escape-1 verdict keys off ADD (contrastive-replace on the current no-slot arch).
    add_reachable = (r_add["margin"] > 1e-3) and (r_add["reach_novel"] > 0.0) and (r_add["scramble"] < 0.5)
    print("\n=== TOY VERDICT (Escape-1 = ADD arch, contrastive-REPLACE) ===")
    print(f"ADD: margin={r_add['margin']:+.4f} reach_novel={r_add['reach_novel']:.2f} "
          f"scramble={r_add['scramble']:.2f}  -> "
          f"{'REACHABLE' if add_reachable else 'AT-FLOOR'}")
    print(f"TPR(attrib): margin={r_tpr['margin']:+.4f} reach_novel={r_tpr['reach_novel']:.2f} "
          f"scramble={r_tpr['scramble']:.2f}")
    print(f"\nTOY_RESULT: {'REACHABLE' if add_reachable else 'AT-FLOOR'}")
    if not add_reachable and (r_tpr["margin"] > 1e-3 and r_tpr["reach_novel"] > 0 and r_tpr["scramble"] < 0.5):
        print("ATTRIBUTION: ADD floors but TPR reaches ⇒ FLOOR is ARCHITECTURAL (no binding "
              "slot), NOT the objective. contrastive-REPLACE alone (cell A01) INERT; needs "
              "TPR slot (cell A11). Consistent with H_9120/H_1816 additive-collapse.")
    elif add_reachable:
        print("ATTRIBUTION: contrastive-REPLACE moves the echo-minimum on the CURRENT arch ⇒ "
              "objective was the lever; escalate to 303M pool re-train.")
    else:
        print("ATTRIBUTION: both ADD and TPR floor ⇒ contrastive-REPLACE does not reach G1 in toy.")


if __name__ == "__main__":
    main()
