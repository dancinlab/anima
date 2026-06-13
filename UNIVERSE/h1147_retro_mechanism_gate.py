#!/usr/bin/env python3
"""
H_1147 — RETRO MECHANISM GATE (the $0 toy that gates the anima-303M-RETRO build).

Question (frozen FREEZE 2026-06-13):
  Does RETRO retrieval-grounding (a copy/cross-attention objective TRAINED INTO the
  weights over a retrieved anchor) actually REDUCE fabrication, where decode-time
  anchor-prepend (H_1146 ORACLE) FAILED?

H_1146 proved: prepending even a PERFECT (oracle) ground-truth anchor barely moved the
byte-LM's fabrication (0.2955 -> 0.2577) BECAUSE the LM was never TRAINED with a
retrieve-then-ground objective — prepending only shifts prefix bytes, it installs no
attend-to-context capability. The ONE remaining grounding path before any 303M GPU spend:
make grounding ARCHITECTURAL — a copy/pointer/cross-attention head over the retrieved
anchor, TRAINED INTO the weights. anima-native: the store is anima's OWN kosmos anchors
(a_kosmos / a_core_engine_map). p1-p8 preserved: the anchor is RETRIEVED DECODE-CONTEXT the
model is TRAINED to use, NOT a system-prompt / persona / reward model.

This is the CHEAP $0 toy that ISOLATES the mechanism. a_scale_honest_scope: it validates the
MECHANISM (does a trained copy objective USE the retrieved anchor where decode-prepend cannot?)
at TOY scale on a SYNTHETIC must-copy task. It does NOT validate 303M-scale transfer, real
noisy kosmos retrieval, or coherence-first backbone training. A GREEN here is a mechanism
existence-proof that JUSTIFIES the 303M-RETRO build; a RED here (a trained copy mechanism
ALSO cannot ground) is DECISIVE against the spend (redesign grounding) — both publishable
(a_paper_negative_ok).

Synthetic must-copy task (un-memorizable factual toy):
  Each example has a KEY token (k pool) and a VALUE token drawn RANDOMLY per example
  (v pool) => the value is un-memorizable => the model MUST copy it from the anchor.
    ANCHOR (retrieved context):  [BOS] <KEY> REL <VALUE> [SEP]
    PROMPT (query):              <KEY> REL
    TARGET (emit at final pos):  <VALUE>
  Full sequence = ANCHOR ++ PROMPT ; predict TARGET at the final position.
  Train / test draw DISJOINT (key,value) random pairings AND a held-out VALUE subset is
  never used as a training target (so test values cannot be recalled).

THREE arms (SAME size / data / steps / optimizer / seed; only the grounding mechanism differs):
  1. VANILLA-PREPEND (H_1146 replay): tiny self-attention decoder LM, anchor merely
       PREPENDED and trained end-to-end. NO explicit pointer/copy pathway. Must learn
       key->value from context via ordinary self-attention only. Control = reproduces
       H_1146 (prepend without a trained copy mechanism fabricates).
  2. RETRO-TRAINED (the test arm): SAME backbone PLUS an explicit learned pointer/copy head
       that cross-attends to the ANCHOR token positions and copies the attended token; a
       learned gate mixes copy-distribution with the vocab head.
  3. NO-ANCHOR (floor): the VANILLA backbone with the anchor's value slot blanked at BOTH
       train and test => there is NO information about the answer anywhere => chance floor.
       (Establishes the un-memorizability of the test set: even a trained model with no
       anchor cannot do better than chance.)

Metrics (p7 deterministic; NOT perplexity, NOT LLM-judge):
  fabricated-entity rate = fraction of HELD-OUT examples where greedy argmax predicted token
                           != the anchor's true VALUE token (emitting any other token = fab).
  copy-accuracy          = 1 - fab_rate (does the arm reproduce the anchor's true entity?).

Frozen falsifier + bars (immovable, set BEFORE any run — see FREEZE block):
  F1 MECHANISM-WORKS:  (i) fab(RETRO) < 0.10  AND  (ii) fab(VANILLA-PREPEND) > 0.50
                       AND (iii) fab(VANILLA-PREPEND) - fab(RETRO) >= 0.40
  F2 COPY-NOT-RECALL:  copy-accuracy(RETRO) clearly above the NO-ANCHOR floor, AND the
                       RETRO no-anchor control collapses to fab >= 0.80 (chance) — i.e. RETRO
                       grounds ONLY when the anchor is present => the win is COPYING the
                       retrieved entity, not memorization.
  VERDICT: F1 AND F2 => GREEN MECHANISM-VALIDATED (build anima-303M-RETRO).
           NOT (F1 AND F2) => RED CLOSED-NEG (redesign grounding; saves the 303M spend).

$0. Local CPU. Pure numpy, deterministic seeded. No torch, no pod.
"""
import json
import sys
import numpy as np

SEED = 1147
rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------------- vocab
PAD, BOS, REL, SEP = 0, 1, 2, 3
N_KEYS = 32
N_VALS = 32
KEY0 = 4
VAL0 = KEY0 + N_KEYS
NV_PAD = VAL0 + N_VALS          # non-value pad used to blank the anchor value slot
VOCAB = NV_PAD + 1

KEYS = list(range(KEY0, KEY0 + N_KEYS))
VALS = list(range(VAL0, VAL0 + N_VALS))

# held-out value subset: these value tokens are NEVER a training target.
HELDOUT_VALS = set(VALS[N_VALS // 2:])      # last half held out
TRAIN_VALS = [v for v in VALS if v not in HELDOUT_VALS]

# ----------------------------------------------------------------------------- data
# sequence layout (length 7):
#   [BOS] KEY REL VALUE SEP | KEY REL        (anchor ++ prompt)
#    0    1   2    3    4     5   6
# predict the VALUE at the final position (index 6).
SEQ_LEN = 7
VALUE_POS_IN_ANCHOR = 3
ANCHOR_POSITIONS = [0, 1, 2, 3, 4]


def build_seq(k, v):
    return np.array([BOS, k, REL, v, SEP, k, REL], dtype=np.int64)


def make_dataset(rng, n, value_pool):
    """Each example: random KEY, VALUE drawn UNIFORMLY (with replacement) from value_pool.
    The value is randomized per example => the model CANNOT memorize key->value, it MUST
    copy the value from the anchor. Train/test disjointness is guaranteed STRUCTURALLY by
    the DISJOINT value pools (TRAIN_VALS vs HELDOUT_VALS), not by per-example pair-uniqueness:
    every test (k,v) has v in HELDOUT_VALS which is never a training target, so no test
    answer can be recalled. (The earlier per-pair-uniqueness loop was IMPOSSIBLE: only
    32*16=512 distinct train pairs exist but N_TRAIN=2000>512 was requested -> infinite loop
    at 97% CPU. Within-split uniqueness was never required by the falsifier; the held-out
    value pool already supplies the un-memorizable guarantee. Pre-score construction fix;
    falsifier bars 0.10/0.50/0.40/floor+0.40/0.80 UNTOUCHED.)
    """
    keys = rng.choice(KEYS, size=n)
    vals = rng.choice(value_pool, size=n)
    X = np.zeros((n, SEQ_LEN), dtype=np.int64)
    for i in range(n):
        X[i] = build_seq(int(keys[i]), int(vals[i]))
    return X, vals.astype(np.int64)


N_TRAIN = 2000
N_TEST = 500
Xtr, Ytr = make_dataset(rng, N_TRAIN, TRAIN_VALS)
# test uses HELD-OUT values (disjoint pool) => answers cannot be recalled from training
Xte, Yte = make_dataset(rng, N_TEST, list(HELDOUT_VALS))

# ----------------------------------------------------------------------------- model
D = 48
STEPS = 500           # the tiny must-copy task converges in a few hundred steps at this batch;
LR = 0.05             # convergence is checked on the printed train loss (must fall + plateau).
BATCH = 512           # large batch amortizes fixed per-step numpy/einsum overhead (fewer iters).


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


class Model:
    def __init__(self, rng, retro: bool):
        self.retro = retro
        s = 0.08
        self.Emb = rng.normal(0, s, (VOCAB, D))
        self.Pos = rng.normal(0, s, (SEQ_LEN, D))
        self.Wq = rng.normal(0, s, (D, D))
        self.Wk = rng.normal(0, s, (D, D))
        self.Wv = rng.normal(0, s, (D, D))
        self.Wo = rng.normal(0, s, (D, VOCAB))
        if retro:
            self.Pq = rng.normal(0, s, (D, D))
            self.Pk = rng.normal(0, s, (D, D))
            self.Wg = rng.normal(0, s, (D, 1))
        self._m = {}
        self._v = {}

    def params(self):
        names = ["Emb", "Pos", "Wq", "Wk", "Wv", "Wo"]
        if self.retro:
            names += ["Pq", "Pk", "Wg"]
        return names

    def forward(self, X, mask_anchor_value=False):
        B, T = X.shape
        Xe = X.copy()
        if mask_anchor_value:
            Xe[:, VALUE_POS_IN_ANCHOR] = NV_PAD     # blank the anchor value slot
        h0 = self.Emb[Xe] + self.Pos[None, :, :]
        Q = h0 @ self.Wq
        K = h0 @ self.Wk
        V = h0 @ self.Wv
        scores = Q @ K.transpose(0, 2, 1) / np.sqrt(D)
        A = softmax(scores, axis=-1)
        ctx = A @ V
        h = h0 + ctx
        hf = h[:, -1, :]
        logits_vocab = hf @ self.Wo

        cache = dict(Xe=Xe, h0=h0, Q=Q, K=K, V=V, A=A, ctx=ctx, h=h, hf=hf,
                     logits_vocab=logits_vocab)
        if not self.retro:
            cache["probs"] = softmax(logits_vocab, axis=-1)
            return cache["probs"], cache

        anc = np.array(ANCHOR_POSITIONS)
        hq = hf @ self.Pq
        hk = h0[:, anc, :] @ self.Pk
        pscore = np.einsum("bd,bad->ba", hq, hk) / np.sqrt(D)
        pattn = softmax(pscore, axis=-1)
        anc_tokens = cache["Xe"][:, anc]
        # fast vectorized scatter: distribute pattn mass onto anchor token vocab ids per row
        # (replaces np.add.at, which is pathologically slow). flat index = b*VOCAB + token.
        flat_idx = (np.arange(B)[:, None] * VOCAB + anc_tokens).reshape(-1)
        copy_dist = np.bincount(flat_idx, weights=pattn.reshape(-1),
                                minlength=B * VOCAB).reshape(B, VOCAB)
        gate = 1.0 / (1.0 + np.exp(-(hf @ self.Wg)))
        vocab_dist = softmax(logits_vocab, axis=-1)
        probs = gate * copy_dist + (1 - gate) * vocab_dist
        probs = np.clip(probs, 1e-9, 1.0)
        probs = probs / probs.sum(axis=-1, keepdims=True)
        cache.update(anc=anc, hq=hq, hk=hk, pscore=pscore, pattn=pattn,
                     anc_tokens=anc_tokens, copy_dist=copy_dist, gate=gate,
                     vocab_dist=vocab_dist, probs=probs)
        return probs, cache

    def loss_and_grad(self, X, Y, mask_anchor_value=False):
        probs, c = self.forward(X, mask_anchor_value=mask_anchor_value)
        B = X.shape[0]
        loss = -np.log(probs[np.arange(B), Y] + 1e-12).mean()

        g = {n: np.zeros_like(getattr(self, n)) for n in self.params()}
        dprobs = probs.copy()
        dprobs[np.arange(B), Y] -= 1.0
        dprobs /= B

        if not self.retro:
            dlogits = (probs - self._onehot(Y, B)) / B
            self._backbone_backward(X, c, dlogits, g)
            return loss, g

        gate = c["gate"]
        copy_dist = c["copy_dist"]
        vocab_dist = c["vocab_dist"]
        hf = c["hf"]
        dP = dprobs
        dgate = (dP * (copy_dist - vocab_dist)).sum(axis=1, keepdims=True)
        dsig = dgate * gate * (1 - gate)
        g["Wg"] += hf.T @ dsig
        dhf_from_gate = dsig @ self.Wg.T

        dvocab_dist = dP * (1 - gate)
        tmp = (dvocab_dist * vocab_dist).sum(axis=1, keepdims=True)
        dlogits = vocab_dist * (dvocab_dist - tmp)

        anc = c["anc"]
        anc_tokens = c["anc_tokens"]
        pattn = c["pattn"]
        dcopy = dP * gate
        dpattn = np.take_along_axis(dcopy, anc_tokens, axis=1)
        pa = pattn
        tmp2 = (dpattn * pa).sum(axis=1, keepdims=True)
        dpscore = pa * (dpattn - tmp2)
        hq = c["hq"]; hk = c["hk"]
        dhq = np.einsum("ba,bad->bd", dpscore, hk) / np.sqrt(D)
        dhk = np.einsum("ba,bd->bad", dpscore, hq) / np.sqrt(D)
        g["Pq"] += hf.T @ dhq
        dhf_from_ptr = dhq @ self.Pq.T
        h0 = c["h0"]
        h0a = h0[:, anc, :]
        g["Pk"] += np.einsum("bad,bae->de", h0a, dhk)
        dh0a = dhk @ self.Pk.T

        dhf = dhf_from_gate + dhf_from_ptr
        self._backbone_backward(X, c, dlogits, g, extra_dhf=dhf, dh0_anchor=(anc, dh0a))
        return loss, g

    def _onehot(self, Y, B):
        oh = np.zeros((B, VOCAB)); oh[np.arange(B), Y] = 1.0; return oh

    def _backbone_backward(self, X, c, dlogits, g, extra_dhf=None, dh0_anchor=None):
        hf = c["hf"]
        g["Wo"] += hf.T @ dlogits
        dhf = dlogits @ self.Wo.T
        if extra_dhf is not None:
            dhf = dhf + extra_dhf
        B, T, _ = c["h0"].shape
        dh = np.zeros((B, T, D)); dh[:, -1, :] = dhf
        dh0 = dh.copy()
        dctx = dh.copy()
        A = c["A"]; V = c["V"]
        dA = dctx @ V.transpose(0, 2, 1)
        dV = A.transpose(0, 2, 1) @ dctx
        scores_soft = A
        dscores = scores_soft * (dA - (dA * scores_soft).sum(axis=-1, keepdims=True))
        dscores /= np.sqrt(D)
        Q = c["Q"]; K = c["K"]
        dQ = dscores @ K
        dK = dscores.transpose(0, 2, 1) @ Q
        h0 = c["h0"]
        g["Wq"] += np.einsum("btd,bte->de", h0, dQ)
        g["Wk"] += np.einsum("btd,bte->de", h0, dK)
        g["Wv"] += np.einsum("btd,bte->de", h0, dV)
        dh0 = dh0 + dQ @ self.Wq.T + dK @ self.Wk.T + dV @ self.Wv.T
        if dh0_anchor is not None:
            anc, dh0a = dh0_anchor
            dh0[:, anc, :] += dh0a
        Xe = c["Xe"]
        np.add.at(g["Emb"], Xe.reshape(-1), dh0.reshape(-1, D))
        g["Pos"] += dh0.sum(axis=0)

    def step(self, g, t, lr):
        b1, b2, eps = 0.9, 0.999, 1e-8
        for n in self.params():
            if n not in self._m:
                self._m[n] = np.zeros_like(g[n]); self._v[n] = np.zeros_like(g[n])
            self._m[n] = b1 * self._m[n] + (1 - b1) * g[n]
            self._v[n] = b2 * self._v[n] + (1 - b2) * (g[n] ** 2)
            mhat = self._m[n] / (1 - b1 ** t)
            vhat = self._v[n] / (1 - b2 ** t)
            getattr(self, n)[...] -= lr * mhat / (np.sqrt(vhat) + eps)


def train(model, Xtr, Ytr, rng, mask_anchor_value=False, label=""):
    n = Xtr.shape[0]
    loss = 0.0
    for t in range(1, STEPS + 1):
        idx = rng.integers(0, n, BATCH)
        loss, g = model.loss_and_grad(Xtr[idx], Ytr[idx],
                                      mask_anchor_value=mask_anchor_value)
        model.step(g, t, LR)
        if label and (t % 300 == 0 or t == 1):
            print(f"  [{label}] step {t}/{STEPS}  loss={loss:.4f}", flush=True)
    return loss


def fab_rate(model, X, Y, mask_anchor_value=False):
    probs, _ = model.forward(X, mask_anchor_value=mask_anchor_value)
    pred = probs.argmax(axis=1)
    return float((pred != Y).mean()), pred


def decode_samples(model, X, Y, n=8, mask_anchor_value=False):
    probs, _ = model.forward(X[:n], mask_anchor_value=mask_anchor_value)
    pred = probs.argmax(axis=1)
    out = []
    for i in range(n):
        out.append(dict(key=int(X[i, 1]), true_val=int(Y[i]), pred=int(pred[i]),
                        correct=bool(pred[i] == Y[i])))
    return out


def fmt_tok(t):
    return ("v%02d" % (t - VAL0)) if t >= VAL0 and t < NV_PAD else ("tok%d" % t)


def main():
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        log.append(s)
        print(s, flush=True)

    P("=" * 78)
    P("H_1147 RETRO MECHANISM GATE — does a TRAINED copy objective ground where")
    P("decode-time anchor-prepend (H_1146 ORACLE) could not?  ($0 numpy CPU, p7 det.)")
    P("=" * 78)
    P(f"seed={SEED} vocab={VOCAB} keys={N_KEYS} vals={N_VALS} "
      f"heldout_vals={len(HELDOUT_VALS)} D={D} steps={STEPS} batch={BATCH} "
      f"n_train={N_TRAIN} n_test={N_TEST}")
    P("test values are HELD-OUT (never a training target) + pairings disjoint")
    P("=> un-memorizable; the answer MUST be COPIED from the retrieved anchor.\n")

    # ---- arm 1: VANILLA-PREPEND (H_1146 replay) ----
    P("[ARM 1 VANILLA-PREPEND] training...")
    mv = Model(np.random.default_rng(SEED + 1), retro=False)
    lv = train(mv, Xtr, Ytr, np.random.default_rng(SEED + 2), label="vanilla")
    fab_v, _ = fab_rate(mv, Xte, Yte)

    # ---- arm 2: RETRO-TRAINED (the test arm) ----
    P("[ARM 2 RETRO-TRAINED] training...")
    mr = Model(np.random.default_rng(SEED + 1), retro=True)
    lr_loss = train(mr, Xtr, Ytr, np.random.default_rng(SEED + 2), label="retro")
    fab_r, _ = fab_rate(mr, Xte, Yte)

    # ---- arm 3: NO-ANCHOR floor: vanilla backbone trained AND tested with anchor blanked ----
    P("[ARM 3 NO-ANCHOR floor] training...")
    mn = Model(np.random.default_rng(SEED + 1), retro=False)
    ln = train(mn, Xtr, Ytr, np.random.default_rng(SEED + 2), mask_anchor_value=True,
               label="no-anchor")
    fab_n, _ = fab_rate(mn, Xte, Yte, mask_anchor_value=True)

    # ---- F2 control: RETRO arm with anchor value-slot MASKED at TEST only ----
    fab_r_masked, _ = fab_rate(mr, Xte, Yte, mask_anchor_value=True)

    P(f"ARM 1 VANILLA-PREPEND  train_loss={lv:.4f}  fab-rate={fab_v:.4f}  "
      f"copy-acc={1-fab_v:.4f}")
    P(f"ARM 2 RETRO-TRAINED    train_loss={lr_loss:.4f}  fab-rate={fab_r:.4f}  "
      f"copy-acc={1-fab_r:.4f}")
    P(f"ARM 3 NO-ANCHOR floor  train_loss={ln:.4f}  fab-rate={fab_n:.4f}  "
      f"copy-acc={1-fab_n:.4f}")
    P(f"      RETRO no-anchor ctrl (F2) fab-rate={fab_r_masked:.4f}  "
      f"copy-acc={1-fab_r_masked:.4f}\n")

    P("--- decoded HELD-OUT samples (key -> true_val | pred) ---")
    for name, m, mk in [("VANILLA-PREPEND", mv, False), ("RETRO-TRAINED", mr, False),
                        ("NO-ANCHOR", mn, True)]:
        P(f"{name}:")
        for s in decode_samples(m, Xte, Yte, mask_anchor_value=mk):
            P(f"  k{s['key']-KEY0:02d} -> true v{s['true_val']-VAL0:02d} | "
              f"pred {fmt_tok(s['pred'])} {'OK' if s['correct'] else 'FAB'}")

    # ---- FROZEN falsifier (immovable bars) ----
    f1_i = fab_r < 0.10
    f1_ii = fab_v > 0.50
    f1_iii = (fab_v - fab_r) >= 0.40
    F1 = f1_i and f1_ii and f1_iii
    f2_copy_above_floor = (1 - fab_r) > (1 - fab_n) + 0.40   # RETRO copy-acc clearly > floor
    f2_collapse = fab_r_masked >= 0.80                       # RETRO grounds only WITH anchor
    F2 = f2_copy_above_floor and f2_collapse
    GREEN = F1 and F2

    P("\n" + "=" * 78)
    P("FROZEN FALSIFIER (bars set BEFORE run; immovable — see H_1147_FREEZE.txt)")
    P("=" * 78)
    P(f"F1(i)   fab(RETRO)        < 0.10 : {fab_r:.4f}        -> {'PASS' if f1_i else 'FAIL'}")
    P(f"F1(ii)  fab(VANILLA-PREP) > 0.50 : {fab_v:.4f}        -> {'PASS' if f1_ii else 'FAIL'}")
    P(f"F1(iii) gap(VAN-RETRO)   >= 0.40 : {fab_v-fab_r:.4f}        -> {'PASS' if f1_iii else 'FAIL'}")
    P(f"F1 MECHANISM-WORKS               : {'PASS' if F1 else 'FAIL'}")
    P(f"F2(a) RETRO copy-acc > floor+0.40: {1-fab_r:.4f} vs floor {1-fab_n:.4f} "
      f"-> {'PASS' if f2_copy_above_floor else 'FAIL'}")
    P(f"F2(b) RETRO no-anchor fab >= 0.80: {fab_r_masked:.4f}        -> "
      f"{'PASS' if f2_collapse else 'FAIL'}")
    P(f"F2 COPY-NOT-RECALL               : {'PASS' if F2 else 'FAIL'}")
    P("-" * 78)
    if GREEN:
        P("VERDICT: 🟢 GREEN — MECHANISM-VALIDATED.")
        P("  A TRAINED copy/pointer objective GROUNDS on the retrieved anchor where")
        P("  decode-time prepend (H_1146 ORACLE) could not, and the win is COPYING not")
        P("  recall (F2). Architectural grounding is REAL at toy scale.")
        P("  => MODEL.md BUILD ORDER: build anima-303M-RETRO (step 2).")
    else:
        P("VERDICT: 🔴 RED — CLOSED-NEG.")
        P("  The frozen mechanism bar was not cleared; a trained copy mechanism does NOT")
        P("  separate as required at toy scale. Honest negative (a_paper_negative_ok).")
        P("  => MODEL.md BUILD ORDER: redesign the grounding mechanism (saves the spend).")
    P("=" * 78)

    result = dict(
        fab_vanilla_prepend=fab_v, fab_retro=fab_r, fab_no_anchor_floor=fab_n,
        fab_retro_no_anchor_ctrl=fab_r_masked,
        copy_acc_vanilla=1 - fab_v, copy_acc_retro=1 - fab_r,
        copy_acc_floor=1 - fab_n,
        F1=F1, F1_i=f1_i, F1_ii=f1_ii, F1_iii=f1_iii,
        F2=F2, F2_copy_above_floor=f2_copy_above_floor, F2_collapse=f2_collapse,
        GREEN=GREEN, gap_van_retro=fab_v - fab_r,
        train_loss_vanilla=lv, train_loss_retro=lr_loss, train_loss_floor=ln,
        seed=SEED, steps=STEPS, n_train=N_TRAIN, n_test=N_TEST, vocab=VOCAB,
    )
    return result, "\n".join(log)


if __name__ == "__main__":
    result, logtext = main()
    out_txt = sys.argv[1] if len(sys.argv) > 1 else None
    out_json = sys.argv[2] if len(sys.argv) > 2 else None
    if out_txt:
        with open(out_txt, "w") as f:
            f.write(logtext + "\n")
    if out_json:
        with open(out_json, "w") as f:
            json.dump(result, f, indent=2)
