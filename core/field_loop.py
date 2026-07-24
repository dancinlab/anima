"""FIELD-LOOP (H_9957) — the closed text<->PureField re-entry mechanism, the train-time replacement
for GRAFT. This module is the mechanism ONLY (per-row PureField state + a trainable bridge that emits
an embedding residual + the H_9607 A<->G write-back + the off/yoked control arms). Wiring it into the
303M train loop (contiguous document streams + per-step carry + post-block write-back) is the next
increment; this module + its $0 smoke is landed first so the mechanism is correct before any pool GPU.

Why a closed loop at all (H_9957, fable+sol reconciled): a FREE-RUNNING field at train time is
information-theoretically a seed — C _|_ (Y,X) => the CE-optimal predictor of text given a
text-independent input is the marginal, so plain cross-entropy provably IGNORES it. GRAFT needed a
`(logN - MI)` term precisely because the state was useless for prediction, and that term is what
manufactured the lambda fluency trade-off; at train time such an in-loss gauge is illegal
(`a_train_inline_gauge`). The only lawful path: the state must carry PREDICTIVE information the trunk
cannot get otherwise, which requires (1) text writing back into the field and (2) the field being the
sole carrier (bottleneck) of some out-of-window natural-text history. Then plain next-byte CE turns
the channel on iff it lowers CE, and if it is worthless the optimizer drives gamma -> 0 (a clean
measured negative). The incentive sign flips vs GRAFT: MI is earned BY CE, not bought against a frozen
organ. PureField physics is FIXED (the substrate's own dynamics are the inductive bias under test);
only `bridge` + `gamma` train.

arms:
  off               — residual forced to None/zero (the 'model ignored the field' + fluency baseline).
  purefield16       — the live closed loop.
  purefield16-yoked — the train-time fancy-seed control: derange the (A,G) write-back pairs across
                      batch rows so the field's drive multiset/physics/autocorrelation are identical
                      but the text<->state correspondence is destroyed.
"""
import numpy as np

ARMS = ("off", "purefield16", "purefield16-yoked")


class FieldLoop:
    """Per-batch-row PureField + H_9607 leaky A<->G integrator + a trainable GraftBridge/gamma that
    injects the C-state as an embedding residual. PureField physics fixed; only bridge+gamma train.

    Usage inside a contiguous-stream train step (next increment):
        fl = FieldLoop(B, d, arm=..., seed=...)
        ...
        res = fl.residual()                 # [B, d] torch (grad to bridge/gamma) or None (off)
        out = model(x, y, emb_residual=res) # residual broadcast over T at the embedding site
        loss = out['loss']; loss.backward(); opt.step()   # bridge+gamma+model train jointly
        fl.writeback(ce_per_row, g_per_row) # no_grad: s=A-G, A=exp(-CE), leaky-integrate -> drive
    Between documents call fl.reset(rows). Requires B>=2 (the bridge centers across rows, so only
    per-row STATE differences survive — that is the point; single-stream B=1 must instead subtract the
    running g_mu, a follow-on)."""

    def __init__(self, batch_rows, d, arm="purefield16", gate_rho=1.0, hidden=64,
                 seed=0, leaky=1.0 / 400.0, drive_gain=-0.6):
        import pure_field as PF
        import clmg as G
        import torch
        if arm not in ARMS:
            raise ValueError(f"arm must be one of {ARMS}, got {arm!r}")
        self.PF, self.G, self.torch = PF, G, torch
        self.arm = arm
        self.d = int(d)
        self.B = int(batch_rows)
        self.leaky = float(leaky)
        self.drive_gain = float(drive_gain)
        self.rng = np.random.default_rng(seed)
        self.pf = [PF.pure_field_new() for _ in range(self.B)]        # per-row field
        self.I = np.zeros(self.B, dtype=np.float64)                   # per-row leaky A<->G integral
        self.bridge = G.GraftBridge(c_dim=G.C_DIM, h=hidden, d=self.d, gate_rho=gate_rho)
        # gamma trainable, init 0 -> CE may turn the channel on or leave it off (no fixed injection)
        self.gamma = torch.nn.Parameter(torch.zeros(()))

    def parameters(self):
        """The trainable field-loop params to hand the optimizer (bridge + gamma)."""
        return list(self.bridge.parameters()) + [self.gamma]

    def _C(self):
        return self.torch.tensor(
            np.stack([self.G.graft_c_state(p) for p in self.pf]), dtype=self.torch.float32)

    def residual(self):
        """emb_residual [B, d] (grad flows to bridge+gamma) for the current per-row C-state, BEFORE the
        block forward. Returns None on the off arm (byte-identical to no-field). At gamma=0 the residual
        is exactly zero, so training starts from the base model and CE decides whether to raise gamma."""
        if self.arm == "off":
            return None
        return self.bridge(self._C()) * self.gamma                   # [B, d]

    def _derangement(self):
        """A random derangement of range(B) (no row keeps its own index) — the yoked control."""
        if self.B < 2:
            return np.arange(self.B)
        while True:
            p = self.rng.permutation(self.B)
            if not np.any(p == np.arange(self.B)):
                return p

    def writeback(self, ce_per_row, g_per_row):
        """After the block, advance each row's field by the H_9607 drive. no_grad (the field is not a
        graph leaf). s = A - G, A = exp(-CE) (the forward CE-trained engine's support for the observed
        bytes), G = the gradient-free reverse-recognition reach; I <- (1-1/400) I + s; drive = -0.6 I.
        On the yoked arm the (A,G) pairs are deranged across rows first (fancy-seed control)."""
        A = np.exp(-np.asarray(ce_per_row, dtype=np.float64))
        Gv = np.asarray(g_per_row, dtype=np.float64)
        if A.shape != (self.B,) or Gv.shape != (self.B,):
            raise ValueError(f"ce/g per-row must be shape ({self.B},), got {A.shape}/{Gv.shape}")
        if self.arm == "purefield16-yoked":
            perm = self._derangement()
            A, Gv = A[perm], Gv[perm]
        s = A - Gv
        self.I = (1.0 - self.leaky) * self.I + s
        drive = self.drive_gain * self.I
        for i in range(self.B):
            self.pf[i] = self.PF.pure_field_step(self.pf[i], float(drive[i])) or self.pf[i]

    def reset(self, rows=None):
        """Reset the field/integral for the given rows (default all) — call between documents."""
        idx = range(self.B) if rows is None else rows
        for i in idx:
            self.pf[i] = self.PF.pure_field_new()
            self.I[i] = 0.0


def _smoke():
    """$0 mechanism smoke — no GPU, no training, no corpus. Certifies the 4 mechanical witnesses the
    design rests on before any pool spend."""
    import torch
    B, d = 4, 64

    # (1) off arm -> no residual (byte-identical to no-field)
    fl_off = FieldLoop(B, d, arm="off", seed=1)
    assert fl_off.residual() is None, "off arm must produce no residual"
    print("(1) off arm: residual is None  OK")

    # (2) purefield16 -> gamma=0 gives EXACTLY zero residual. Raising gamma is not enough on its own:
    #     freshly-initialized rows share one field, and the bridge centers ACROSS rows, so an identical
    #     field zeros the residual by construction. That is the design working — the field carries
    #     signal only once rows DIVERGE via different text-dependent write-back history. So we diverge
    #     the rows first (distinct per-row drive), THEN the residual is nonzero and grad-carrying.
    fl = FieldLoop(B, d, arm="purefield16", seed=1)
    r0 = fl.residual()
    assert r0.shape == (B, d), f"residual shape {tuple(r0.shape)} != {(B, d)}"
    assert float(r0.detach().abs().max()) == 0.0, "gamma init 0 must give exactly-zero residual"
    for _ in range(3):                                            # accumulate text-dependent history
        fl.writeback(np.array([0.1, 0.9, 0.4, 1.5]), np.array([0.2, 0.2, 0.2, 0.2]))
    with torch.no_grad():
        fl.gamma.fill_(1.0)
    r1 = fl.residual()
    assert float(r1.detach().abs().max()) > 0.0, "diverged rows at gamma=1 must give a nonzero residual"
    assert r1.requires_grad, "residual must carry grad to bridge+gamma"
    print(f"(2) purefield16: gamma0 zero; after divergence gamma1 |max|={float(r1.detach().abs().max()):.4f}, "
          f"grad OK  OK")

    # (3) write-back with DISTINCT per-row CE advances each row's field DIFFERENTLY (text-dependence)
    c0 = np.stack([fl.G.graft_c_state(p) for p in fl.pf])
    ce = np.array([0.1, 0.9, 0.3, 1.7]); g = np.array([0.2, 0.2, 0.2, 0.2])
    fl.writeback(ce, g)
    c1 = np.stack([fl.G.graft_c_state(p) for p in fl.pf])
    dpr = np.abs(c1 - c0).sum(axis=1)
    assert np.all(dpr > 0), "write-back must move every row's field"
    assert dpr.std() > 0, "distinct per-row CE must move rows by DIFFERENT amounts (text-dependence)"
    print(f"(3) write-back: per-row field deltas {np.round(dpr, 3)} (differ) OK")

    # (4) yoked arm deranges (A,G) across rows -> the SAME (ce,g) advances the field differently than
    #     the aligned arm, because each row gets another row's drive
    fla = FieldLoop(B, d, arm="purefield16", seed=7)
    fly = FieldLoop(B, d, arm="purefield16-yoked", seed=7)
    ce2 = np.array([0.05, 1.2, 0.4, 0.8]); g2 = np.array([0.1, 0.5, 0.2, 0.3])
    fla.writeback(ce2, g2); fly.writeback(ce2, g2)
    ca = np.stack([fla.G.graft_c_state(p) for p in fla.pf])
    cy = np.stack([fly.G.graft_c_state(p) for p in fly.pf])
    assert np.abs(ca - cy).sum() > 0, "yoked arm must advance the field differently than aligned"
    print("(4) yoked arm: derangement changes the trajectory vs aligned  OK")

    print("\nFIELD-LOOP MECHANISM SMOKE: ALL PASS (mechanism only — train-loop wiring is the next increment)")
    return 0


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(_smoke())
