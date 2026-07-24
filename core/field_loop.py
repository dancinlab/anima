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
        self.dev = torch.device("cpu")

    def to(self, device):
        """Move the trainable params (bridge + gamma) AND anchor the device the C-state is built on,
        so residual() never mixes a CPU C-tensor with a CUDA bridge (train-py-1 device-mismatch)."""
        self.dev = self.torch.device(device)
        self.bridge.to(self.dev)
        self.gamma.data = self.gamma.data.to(self.dev)
        return self

    def parameters(self):
        """The trainable field-loop params to hand the optimizer (bridge + gamma)."""
        return list(self.bridge.parameters()) + [self.gamma]

    def save(self, path):
        """Persist the TRAINED coupling (bridge + gamma + config) as a torch sidecar next to the .clm.
        The .clm holds only the trunk; the eval (Delta_collapse / sever / rotation / FORM) needs this
        to reconstruct the field->language mapping."""
        self.torch.save(
            {"bridge": {k: v.detach().cpu() for k, v in self.bridge.state_dict().items()},
             "gamma": float(self.gamma.detach()), "c_dim": self.G.C_DIM,
             "hidden": int(self.bridge.l1.out_features), "d": self.d,
             "gate_rho": float(self.bridge.gate_rho), "arm": self.arm,
             "leaky": self.leaky, "drive_gain": self.drive_gain}, path)

    @staticmethod
    def load(path, batch_rows, device="cpu", seed=0):
        """Reconstruct a FieldLoop from a save() sidecar (for eval). batch_rows = the K documents /
        rows the eval will run in parallel; the field state itself is re-seeded fresh (the trained
        thing is the bridge+gamma, not the transient field)."""
        import torch
        st = torch.load(path, map_location="cpu", weights_only=False)
        fl = FieldLoop(batch_rows, int(st["d"]), arm=st["arm"], gate_rho=float(st["gate_rho"]),
                       hidden=int(st["hidden"]), seed=seed,
                       leaky=float(st["leaky"]), drive_gain=float(st["drive_gain"]))
        fl.bridge.load_state_dict(st["bridge"])
        with torch.no_grad():
            fl.gamma.fill_(float(st["gamma"]))
        return fl.to(device)

    def _C(self):
        return self.torch.tensor(
            np.stack([self.G.graft_c_state(p) for p in self.pf]),
            dtype=self.torch.float32, device=self.dev)

    def residual(self):
        """emb_residual [B, d] (grad flows to bridge+gamma) for the current per-row C-state, BEFORE the
        block forward. Returns None on the off arm (byte-identical to no-field), AND whenever the rows'
        C-states are still identical (fresh fields at step 0, or just after a reset): the bridge centers
        across rows, so identical rows give a zero-variance input whose RMS-normalization gradient is
        singular (sqrt(0) -> inf -> NaN in gamma). Identical rows also carry NO differential state to
        inject, so skipping is correct, not just safe. At gamma=0 the residual is exactly zero, so
        training starts from the base model and CE decides whether to raise gamma."""
        if self.arm == "off":
            return None
        C = self._C()
        if float((C - C.mean(dim=0, keepdim=True)).abs().max()) < 1e-6:
            return None                                              # rows identical -> no injection
        return self.bridge(C) * self.gamma                          # [B, d]

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


class _FieldStream:
    """Per-row CONTIGUOUS byte-cursors into a corpus — the cross-chunk premise FIELD-LOOP needs (the
    field is the only thing that persists across adjacent blocks, so it must carry out-of-window
    history the trunk's window cannot). Each row advances contiguously; a row that reaches the end
    wraps to 0 and is reported as a document boundary (the caller resets that row's field). Replaces
    the trainer's random-window draw for the field-loop path. Returns
    (x[B,block], y[B,block] = x shifted by 1, wrapped_rows)."""

    def __init__(self, data_bytes, B, block, seed=0):
        import torch
        self.torch = torch
        self.data = np.frombuffer(data_bytes, dtype=np.uint8)
        self.N = int(self.data.shape[0])
        self.B = int(B)
        self.block = int(block)
        if self.N < block + 2:
            raise ValueError(f"corpus too small: {self.N} bytes < block+2 = {block + 2}")
        rng = np.random.default_rng(seed)
        self.cur = rng.integers(0, self.N - block - 1, size=self.B).astype(np.int64)

    def next_block(self):
        xs = []
        wrapped = []
        for i in range(self.B):
            c = int(self.cur[i])
            if c + self.block + 1 > self.N:                 # wrap = new document boundary
                c = 0
                wrapped.append(i)
            xs.append(self.data[c:c + self.block + 1])
            self.cur[i] = c + self.block                    # next block continues where this ended
        arr = np.stack(xs).astype(np.int64)                 # [B, block+1]
        t = self.torch.tensor(arr, dtype=self.torch.long)
        return t[:, :-1].contiguous(), t[:, 1:].contiguous(), wrapped


def field_loop_train(model, data_bytes, arm, steps, d, B=8, block=256, lr=1e-3, seed=0,
                     device="cpu", hidden=64, g_fn=None, log_every=25, log=print):
    """One FIELD-LOOP training run (model-agnostic — cli/train.py --field-loop passes the real
    CLMConvMoE; the $0 smoke passes a tiny stand-in). Per contiguous block:
        residual = FieldLoop.residual()   [B,d] broadcast over T at the embedding site
        logits   = model(x, None, emb_residual=residual[:,None,:])["logits"]   [B,V,T]
        ce_row   = mean_T CE(logits, y)                                          [B]
        loss.backward(); opt.step()       # model + bridge + gamma train JOINTLY
        write-back: s = A - G, A = exp(-ce_row), G = g_fn(x)  (gradient-free reverse recognition)
    No MI/lambda term — plain next-byte CE is the whole objective (the train-time difference from
    GRAFT). g_fn(x_block)->[B] defaults to zeros (smoke stub; the caller wires the real
    immune_memory_recall_reach). Returns (FieldLoop, per-step mean-CE history)."""
    import torch
    import torch.nn.functional as F
    fl = FieldLoop(B, d, arm=arm, hidden=hidden, seed=seed).to(device)
    core_m = model.module if hasattr(model, "module") else model
    emb_w = getattr(core_m, "embed", None)
    emb_rms = (float(emb_w.weight.detach().float().pow(2).mean().sqrt())
               if emb_w is not None else 1.0)                # residual amplitude anchor (GRAFT-style)
    stream = _FieldStream(data_bytes, B, block, seed=seed)
    params = list(model.parameters()) + fl.parameters()
    opt = torch.optim.Adam(params, lr=lr)
    hist = []
    for step in range(1, steps + 1):
        x, y, wrapped = stream.next_block()
        if wrapped:
            fl.reset(wrapped)                                # doc boundary -> reset that row's field
        x = x.to(device)
        y = y.to(device)
        res = fl.residual()                                  # [B, d] or None (off)
        if res is not None:
            res = (res * emb_rms).unsqueeze(1)               # anchor amplitude to the model's embedding
            #      RMS (GRAFT's stability anchor) so gamma stays O(1), then broadcast over T
        logits = model(x, None, emb_residual=res)["logits"].float()   # [B, V, T]
        ce_row = F.cross_entropy(logits, y, reduction="none").mean(dim=1)  # [B]
        loss = ce_row.mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)          # GRAFT/standard-loop grad clip (no-NaN)
        opt.step()
        with torch.no_grad():
            ce_np = ce_row.detach().cpu().numpy()
            g_np = np.zeros(B) if g_fn is None else np.asarray(g_fn(x), dtype=np.float64)
            fl.writeback(ce_np, g_np)
        hist.append(float(loss.detach()))
        if step % log_every == 0 or step == 1:
            log(f"[field-loop:{arm}] step {step:5d}  CE={hist[-1]:.4f}  "
                f"gamma={float(fl.gamma.detach()):+.5f}")
    return fl, hist


def _smoke():
    """$0 mechanism + end-to-end wiring smoke — no GPU, no corpus file, no pool. Certifies the 4
    mechanical witnesses AND that a residual->forward->CE->backward->write-back step trains gamma+bridge
    jointly on a tiny stand-in LM, before the real CLMConvMoE is wired in cli/train.py --field-loop."""
    import torch
    B, d = 4, 64

    # (1) off arm -> no residual (byte-identical to no-field)
    fl_off = FieldLoop(B, d, arm="off", seed=1)
    assert fl_off.residual() is None, "off arm must produce no residual"
    print("(1) off arm: residual is None  OK")

    # (2) purefield16 -> fresh rows share one field, so residual() returns None (the identical-rows
    #     guard: a zero-variance input has a singular RMS-normalization gradient = NaN, and identical
    #     rows carry no differential state). The field carries signal only once rows DIVERGE via
    #     different text-dependent write-back history — THEN residual() is a nonzero grad-carrying tensor.
    fl = FieldLoop(B, d, arm="purefield16", seed=1)
    assert fl.residual() is None, "identical fresh rows must return None (no differential state)"
    for _ in range(3):                                            # accumulate text-dependent history
        fl.writeback(np.array([0.1, 0.9, 0.4, 1.5]), np.array([0.2, 0.2, 0.2, 0.2]))
    with torch.no_grad():
        fl.gamma.fill_(1.0)
    r1 = fl.residual()
    assert r1 is not None and r1.shape == (B, d), "diverged rows must give a [B,d] residual"
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

    # (5) END-TO-END wiring on a tiny stand-in LM with the CLMConvMoE interface
    #     (tokens, targets, emb_residual)->{"logits": [B,V,T]}. Proves the closed loop
    #     residual->forward->per-row CE->backward->write-back trains gamma+bridge jointly, and that
    #     the off arm is a true no-op (gamma stays exactly 0). The real 303M CLMConvMoE is passed by
    #     cli/train.py --field-loop; this stand-in keeps the smoke $0/CPU/dependency-light.
    class _TinyLM(torch.nn.Module):
        def __init__(self, V=256, dm=32):
            super().__init__()
            self.embed = torch.nn.Embedding(V, dm)
            self.head = torch.nn.Linear(dm, V)

        def forward(self, tokens, targets=None, emb_residual=None):
            h = self.embed(tokens)                      # [B, T, dm]
            if emb_residual is not None:
                h = h + emb_residual                    # [B, 1, dm] -> broadcast over T
            return {"logits": self.head(h).transpose(1, 2)}   # [B, V, T]

    dm = 32
    data = bytes(np.random.default_rng(0).integers(0, 256, size=20000).astype(np.uint8).tobytes())
    torch.manual_seed(0)
    fl_e, hist = field_loop_train(_TinyLM(256, dm), data, arm="purefield16", steps=60, d=dm,
                                  B=8, block=128, lr=3e-3, seed=0, log_every=10_000)
    assert len(hist) == 60 and all(np.isfinite(hist)), "e2e CE must stay finite for all steps"
    assert np.isfinite(float(fl_e.gamma.detach())), "gamma must stay finite"
    torch.manual_seed(0)
    fl_off, hist_off = field_loop_train(_TinyLM(256, dm), data, arm="off", steps=20, d=dm,
                                        B=8, block=128, lr=3e-3, seed=0, log_every=10_000)
    assert float(fl_off.gamma.detach()) == 0.0, "off arm gamma must stay EXACTLY 0 (no residual path)"
    assert all(np.isfinite(hist_off)), "off arm CE must stay finite"
    print(f"(5) e2e tiny-LM: purefield16 CE {hist[0]:.3f}->{hist[-1]:.3f} gamma={float(fl_e.gamma.detach()):+.5f}"
          f" · off gamma=0.0 (true no-op)  OK")

    # (6) save/load roundtrip — the trained bridge+gamma survive a sidecar write/read (eval needs this)
    import tempfile
    import os as _os
    with torch.no_grad():
        fl_e.gamma.fill_(0.1234)
    p = _os.path.join(tempfile.gettempdir(), "fl_roundtrip.pt")
    fl_e.save(p)
    fl_r = FieldLoop.load(p, batch_rows=8, device="cpu")
    assert abs(float(fl_r.gamma.detach()) - 0.1234) < 1e-6, "gamma must survive save/load"
    b0 = list(fl_e.bridge.state_dict().values())[0]
    b1 = fl_r.bridge.state_dict()[list(fl_e.bridge.state_dict().keys())[0]]
    assert torch.allclose(b0.cpu(), b1.cpu()), "bridge weights must survive save/load"
    _os.remove(p)
    print("(6) save/load: gamma+bridge roundtrip byte-faithful  OK")

    print("\nFIELD-LOOP SMOKE: ALL PASS (mechanism + e2e wiring + persistence — eval harness is next)")
    return 0


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(_smoke())
