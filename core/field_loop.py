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

ARMS = ("off", "purefield16", "purefield16-yoked",
        # H_9957 generic-recurrence sibling · rung 1 (fable): the H_9607 leaky integral `I` (tau=400)
        # is shared plumbing UPSTREAM of PureField — the doc-scale memory may live entirely in `I`, with
        # PureField a nonlinear passthrough. `integrator16` reads I through FIXED random features
        # tanh(w*I+b) (no cell, +0 params), same drive/bridge/gamma/reset. If its fieldctl Δ matches
        # purefield16's, the channel is the shared scalar integrator and PureField is NOT load-bearing.
        "integrator16", "integrator16-yoked",
        # H_9957 sibling · rung 2 (fable): gru16-frozen = a FIXED random GRU-16 driven by the same
        # scalar u=-0.6*I. Unlike integrator16 (memoryless read of the scalar), this is a genuine
        # multi-D RECURRENT expansion with frozen weights (+0 trainable params). If it matches
        # purefield16's Δ, any fixed multi-D recurrence suffices (PureField not special); if it carries
        # ~0 like integrator16, PureField's specific dynamics (or a TRAINED cell) are needed.
        "gru16-frozen", "gru16-frozen-yoked",
        # H_9957 Φ-measurability arm (fable): m COUPLED leaky cells + DCT-mode vector write. cells>1 +
        # --field-write vector makes the state a system faithful IIT-4 can read (a 1-cell integral has
        # Φ undefined); the FIXED weak cell-coupling makes integration available so the Φ question is not
        # vacuous. The mission DV is Φ collapse-Δ of the CE-earned state, not payload bits.
        "coupled", "coupled-yoked")


class _FrozenGRU:
    """A FIXED (untrained) GRU-n driven by a scalar u — the H_9957 sibling rung-2 generic-recurrence
    control. Standard GRU with frozen random weights; fable's init: recurrent W_h orthogonal × 0.95,
    update-gate bias log-spaced so unit time-constants span ~2..400 blocks (mirrors PureField's
    fast/slow oscillator structure, prevents the reservoir-forgets-at-init false negative). Numpy,
    no grad — it is a fixed nonlinear multi-D expansion of the drive history, contrasted against
    PureField's fixed oscillator dynamics under the identical bridge/gamma/optimizer."""

    def __init__(self, n, rng):
        self.n = int(n)

        def _orth(m):
            q, _ = np.linalg.qr(rng.standard_normal((m, m)))
            return q * 0.95
        self.Wz_h, self.Wr_h, self.Wh_h = _orth(n), _orth(n), _orth(n)
        self.Wz_u = rng.standard_normal(n) * 0.5
        self.Wr_u = rng.standard_normal(n) * 0.5
        self.Wh_u = rng.standard_normal(n) * 0.5
        tau = np.logspace(np.log10(2.0), np.log10(400.0), n)         # per-unit time constants
        z_tgt = 1.0 - np.exp(-1.0 / tau)
        self.bz = np.log(z_tgt / (1.0 - z_tgt))                      # logit -> log-spaced retention
        self.br = np.zeros(n)
        self.bh = np.zeros(n)

    def step(self, h, u):
        """Advance [B,n] state by one block under per-row scalar drive u [B]. no_grad numpy."""
        u = np.asarray(u, dtype=np.float64)[:, None]                 # [B,1]
        z = _sigmoid(h @ self.Wz_h.T + u * self.Wz_u + self.bz)
        r = _sigmoid(h @ self.Wr_h.T + u * self.Wr_u + self.br)
        ht = np.tanh((r * h) @ self.Wh_h.T + u * self.Wh_u + self.bh)
        return (1.0 - z) * h + z * ht

    def state(self):
        return {"n": self.n, "Wz_h": self.Wz_h.tolist(), "Wr_h": self.Wr_h.tolist(),
                "Wh_h": self.Wh_h.tolist(), "Wz_u": self.Wz_u.tolist(), "Wr_u": self.Wr_u.tolist(),
                "Wh_u": self.Wh_u.tolist(), "bz": self.bz.tolist(), "br": self.br.tolist(),
                "bh": self.bh.tolist()}

    @staticmethod
    def from_state(st):
        g = _FrozenGRU.__new__(_FrozenGRU)
        g.n = int(st["n"])
        for k in ("Wz_h", "Wr_h", "Wh_h", "Wz_u", "Wr_u", "Wh_u", "bz", "br", "bh"):
            setattr(g, k, np.asarray(st[k], dtype=np.float64))
        return g


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _fixed_rotation(m, rng, theta=0.15):
    """A FIXED weak orthogonal cell-coupling matrix [m,m] (identity when m==1). Weak so the leaky
    dynamics dominate but cross-cell influence is nonzero → integration is available-by-construction,
    which is what makes Φ on the m-cell state a non-vacuous question (fable · H_9957). Deterministic
    given the rng draw; persisted with the FieldLoop so eval reconstructs it exactly."""
    if m == 1:
        return np.eye(1)
    A = rng.standard_normal((m, m))
    A = A - A.T                                    # skew-symmetric -> exp(theta*A) is a small rotation
    # low-order series for a small rotation (theta small): I + θA + (θA)^2/2
    tA = theta * A
    return np.eye(m) + tA + 0.5 * (tA @ tA)


def _dct_basis(m, T):
    """First m DCT-II temporal basis rows [m, T] (orthonormal-ish). Row 0 is the flat/mean mode, so a
    scalar write (mode 0 only) is the block-mean of the profile = the legacy H_9607 scalar up to scale."""
    t = np.arange(T)
    k = np.arange(m)[:, None]
    W = np.cos(np.pi * (t + 0.5) * k / T)          # [m, T]
    W = W / np.linalg.norm(W, axis=1, keepdims=True)
    return W


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
                 seed=0, leaky=1.0 / 400.0, drive_gain=-0.6, write="scalar", cells=1):
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
        self.yoked = arm.endswith("-yoked")
        base = arm[:-len("-yoked")] if self.yoked else arm
        self.kind = {"off": "off", "purefield16": "purefield", "integrator16": "integrator",
                     "gru16-frozen": "gru-frozen", "coupled": "coupled"}.get(base, "purefield")
        self.pf = [PF.pure_field_new() for _ in range(self.B)]        # per-row field
        self.I = np.zeros(self.B, dtype=np.float64)                   # per-row leaky A<->G integral
        # integrator16 (sibling rung 1): FIXED random features of I, C_DIM-wide, frozen at seed (no cell)
        self.int_w = self.rng.standard_normal(G.C_DIM) if self.kind == "integrator" else None
        self.int_b = self.rng.standard_normal(G.C_DIM) if self.kind == "integrator" else None
        # gru16-frozen (sibling rung 2): FIXED random GRU-16, scalar-driven, C_DIM-wide bounded state
        self.gru = _FrozenGRU(G.C_DIM, self.rng) if self.kind == "gru-frozen" else None
        self.gru_h = np.zeros((self.B, G.C_DIM)) if self.kind == "gru-frozen" else None
        # coupled (H_9957 Φ-measurability arm · fable): m coupled leaky cells, log-spaced τ, a FIXED weak
        # rotation R so integration is available-by-construction (Φ non-vacuous); write = first m DCT modes
        # of the per-byte A−G tension profile (scalar = mode 0 only, so cells=1/write=scalar == the legacy
        # integrator). Only bridge+gamma train; the write basis + cell dynamics are fixed (the substrate
        # under test). This is the state faithful IIT-4 can read — 1-cell integral has Φ undefined.
        self.write = write
        self.m = int(cells) if (self.kind == "coupled" and write == "vector") else 1
        if self.kind == "coupled":
            tau = np.array([400.0]) if self.m == 1 else np.logspace(2.0, np.log10(6400.0), self.m)
            self.lam = 1.0 / tau                                     # per-cell leak (m=1 -> 1/400)
            self.Ivec = np.zeros((self.B, self.m), dtype=np.float64)
            self.R = _fixed_rotation(self.m, self.rng)              # weak fixed cell coupling (I if m=1)
            self.Wdct = None                                        # DCT basis [m, T], built when T known
        else:
            self.lam = None; self.Ivec = None; self.R = None; self.Wdct = None
        c_dim = self.m if self.kind == "coupled" else G.C_DIM
        self.bridge = G.GraftBridge(c_dim=c_dim, h=hidden, d=self.d, gate_rho=gate_rho)
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
             "leaky": self.leaky, "drive_gain": self.drive_gain,
             "int_w": None if self.int_w is None else self.int_w.tolist(),
             "int_b": None if self.int_b is None else self.int_b.tolist(),
             "gru": None if self.gru is None else self.gru.state(),
             "write": self.write, "m": self.m,
             "lam": None if self.lam is None else self.lam.tolist(),
             "R": None if self.R is None else self.R.tolist()}, path)

    @staticmethod
    def load(path, batch_rows, device="cpu", seed=0):
        """Reconstruct a FieldLoop from a save() sidecar (for eval). batch_rows = the K documents /
        rows the eval will run in parallel; the field state itself is re-seeded fresh (the trained
        thing is the bridge+gamma, not the transient field)."""
        import torch
        st = torch.load(path, map_location="cpu", weights_only=False)
        fl = FieldLoop(batch_rows, int(st["d"]), arm=st["arm"], gate_rho=float(st["gate_rho"]),
                       hidden=int(st["hidden"]), seed=seed,
                       leaky=float(st["leaky"]), drive_gain=float(st["drive_gain"]),
                       write=st.get("write", "scalar"), cells=int(st.get("m", 1)))
        if st.get("int_w") is not None:                              # restore integrator16 fixed features
            fl.int_w = np.asarray(st["int_w"], dtype=np.float64)
            fl.int_b = np.asarray(st["int_b"], dtype=np.float64)
        if st.get("gru") is not None:                                # restore gru16-frozen fixed weights
            fl.gru = _FrozenGRU.from_state(st["gru"])
        if st.get("lam") is not None:                                # restore coupled cells' fixed dynamics
            fl.lam = np.asarray(st["lam"], dtype=np.float64)
            fl.R = np.asarray(st["R"], dtype=np.float64)
        fl.bridge.load_state_dict(st["bridge"])
        with torch.no_grad():
            fl.gamma.fill_(float(st["gamma"]))
        return fl.to(device)

    def _C(self):
        if self.kind == "integrator":                                # fixed random features of I (no cell)
            C = np.tanh(self.int_w[None, :] * self.I[:, None] + self.int_b[None, :])   # [B, C_DIM]
        elif self.kind == "gru-frozen":                              # fixed random GRU state (recurrent)
            C = self.gru_h
        elif self.kind == "coupled":                                 # m coupled leaky cells (the Φ state)
            C = self.Ivec
        else:
            C = np.stack([self.G.graft_c_state(p) for p in self.pf])
        return self.torch.tensor(C, dtype=self.torch.float32, device=self.dev)

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
        """After the block, advance the field by the H_9607 drive. no_grad (the field is not a graph
        leaf). s = A - G, A = exp(-CE), G = gradient-free reverse-recognition reach; I <- (1-1/400) I + s.
        On the yoked arm the drive is deranged across rows (fancy-seed control). The COUPLED arm accepts
        a per-byte CE/G profile [B,T] and writes its first m DCT modes into m coupled leaky cells."""
        if self.kind == "coupled":
            return self._writeback_coupled(ce_per_row, g_per_row)
        A = np.exp(-np.asarray(ce_per_row, dtype=np.float64))
        Gv = np.asarray(g_per_row, dtype=np.float64)
        if A.shape != (self.B,) or Gv.shape != (self.B,):
            raise ValueError(f"ce/g per-row must be shape ({self.B},), got {A.shape}/{Gv.shape}")
        if self.yoked:
            perm = self._derangement()
            A, Gv = A[perm], Gv[perm]
        s = A - Gv
        self.I = (1.0 - self.leaky) * self.I + s                      # the shared leaky integrator (all arms)
        drive = self.drive_gain * self.I                             # the same post-integrator scalar drive
        if self.kind == "purefield":                                 # PureField advances its oscillator field
            for i in range(self.B):
                self.pf[i] = self.PF.pure_field_step(self.pf[i], float(drive[i])) or self.pf[i]
        elif self.kind == "gru-frozen":                              # frozen GRU advances its recurrent state
            self.gru_h = self.gru.step(self.gru_h, drive)
        # integrator16 reads I directly (no cell to advance)

    def _writeback_coupled(self, ce, g):
        """Coupled-cell write. vector: ce/g are per-byte [B,T] -> s = first m DCT modes of the A-G
        tension profile. scalar (m=1): ce/g are per-row [B] mean-CE -> s is the block-mean = mode 0.
        State: I <- R · diag(1-λ) · I + s (fixed weak coupling R, per-cell leak λ). Yoked derangement
        permutes the drive rows. no_grad."""
        ce = np.asarray(ce, dtype=np.float64)
        g = np.asarray(g, dtype=np.float64)
        if self.write == "vector":
            if ce.ndim != 2 or ce.shape[0] != self.B:
                raise ValueError(f"vector coupled write needs per-byte ce [B,T], got {ce.shape}")
            T = ce.shape[1]
            if self.Wdct is None or self.Wdct.shape[1] != T:
                self.Wdct = _dct_basis(self.m, T)
            if g.ndim == 1:
                g = np.repeat(g[:, None], T, axis=1)                 # broadcast per-row g to per-byte
            s = (np.exp(-ce) - g) @ self.Wdct.T                      # [B,m] first m DCT modes of A-G
        else:                                                        # scalar (m=1) = legacy mode-0 write
            if ce.shape != (self.B,):
                raise ValueError(f"scalar coupled write needs per-row ce [B], got {ce.shape}")
            s = (np.exp(-ce) - g)[:, None]                           # [B,1]
        if self.yoked:
            s = s[self._derangement()]                              # derange the drive across rows
        self.Ivec = (self.Ivec * (1.0 - self.lam)) @ self.R.T + s   # [B,m] coupled leaky update

    def reset(self, rows=None):
        """Reset the field/integral for the given rows (default all) — call between documents."""
        idx = range(self.B) if rows is None else rows
        for i in idx:
            self.pf[i] = self.PF.pure_field_new()
            self.I[i] = 0.0
            if self.gru_h is not None:
                self.gru_h[i] = 0.0
            if self.Ivec is not None:
                self.Ivec[i] = 0.0


class _FieldStream:
    """Per-row CONTIGUOUS byte-cursors into a corpus — the cross-chunk premise FIELD-LOOP needs (the
    field is the only thing that persists across adjacent blocks, so it must carry out-of-window
    history the trunk's window cannot). Each row advances contiguously; a row that reaches the end
    wraps to 0 and is reported as a document boundary (the caller resets that row's field). Replaces
    the trainer's random-window draw for the field-loop path. Returns
    (x[B,block], y[B,block] = x shifted by 1, wrapped_rows)."""

    def __init__(self, data_bytes, B, block, seed=0, doc_len=0):
        import torch
        self.torch = torch
        self.data = np.frombuffer(data_bytes, dtype=np.uint8)
        self.N = int(self.data.shape[0])
        self.B = int(B)
        self.block = int(block)
        if self.N < block + 2:
            raise ValueError(f"corpus too small: {self.N} bytes < block+2 = {block + 2}")
        # doc_len>0 = DOC-AWARE mode (H_9957 fieldctl): blocks align to a fixed doc grid and the field
        # is reset at every planted doc boundary, so the leaky integral carries ONE doc's key, not a
        # ~400-block blur of many docs. Rows are held B-docs apart and cycle, so a batch spans distinct
        # docs (mixed keys => the row-centered residual is non-degenerate). doc_len=0 = legacy random-
        # start contiguous stream (natural-corpus path), byte-identical to before.
        self.doc_len = int(doc_len)
        if self.doc_len > 0:
            if self.doc_len % self.block != 0:
                raise ValueError(f"doc_len {self.doc_len} must be a multiple of block {self.block}")
            self.doc_blocks = self.doc_len // self.block
            self.ndocs = self.N // self.doc_len
            if self.ndocs < self.B:
                raise ValueError(f"corpus has {self.ndocs} docs < B={self.B}")
            self.row_doc = (np.arange(self.B) % self.ndocs).astype(np.int64)
            self.blk_in_doc = np.zeros(self.B, dtype=np.int64)
        else:
            rng = np.random.default_rng(seed)
            self.cur = rng.integers(0, self.N - block - 1, size=self.B).astype(np.int64)

    def next_block(self):
        xs = []
        wrapped = []
        if self.doc_len > 0:                                # DOC-AWARE (fieldctl)
            for i in range(self.B):
                if int(self.blk_in_doc[i]) >= self.doc_blocks:      # finished a doc -> next doc, reset
                    self.row_doc[i] = (self.row_doc[i] + self.B) % self.ndocs
                    self.blk_in_doc[i] = 0
                    wrapped.append(i)
                c = int(self.row_doc[i]) * self.doc_len + int(self.blk_in_doc[i]) * self.block
                seg = self.data[c:c + self.block + 1]
                if seg.shape[0] < self.block + 1:           # last doc's last block: pad the +1 target
                    seg = np.concatenate([seg, seg[-1:].repeat(self.block + 1 - seg.shape[0])])
                xs.append(seg)
                self.blk_in_doc[i] += 1
        else:                                               # legacy random-start contiguous stream
            for i in range(self.B):
                c = int(self.cur[i])
                if c + self.block + 1 > self.N:             # wrap = new document boundary
                    c = 0
                    wrapped.append(i)
                xs.append(self.data[c:c + self.block + 1])
                self.cur[i] = c + self.block                # next block continues where this ended
        arr = np.stack(xs).astype(np.int64)                 # [B, block+1]
        t = self.torch.tensor(arr, dtype=self.torch.long)
        return t[:, :-1].contiguous(), t[:, 1:].contiguous(), wrapped


def field_loop_train(model, data_bytes, arm, steps, d, B=8, block=256, lr=1e-3, seed=0,
                     device="cpu", hidden=64, g_fn=None, log_every=25, log=print, doc_len=0,
                     write="scalar", cells=1):
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
    fl = FieldLoop(B, d, arm=arm, hidden=hidden, seed=seed, write=write, cells=cells).to(device)
    vec_wb = (fl.kind == "coupled" and fl.write == "vector")      # per-byte write needs the [B,T] CE
    core_m = model.module if hasattr(model, "module") else model
    emb_w = getattr(core_m, "embed", None)
    emb_rms = (float(emb_w.weight.detach().float().pow(2).mean().sqrt())
               if emb_w is not None else 1.0)                # residual amplitude anchor (GRAFT-style)
    stream = _FieldStream(data_bytes, B, block, seed=seed, doc_len=doc_len)
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
        ce_all = F.cross_entropy(logits, y, reduction="none")         # [B, T] per-byte CE
        ce_row = ce_all.mean(dim=1)                                   # [B]
        loss = ce_row.mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)          # GRAFT/standard-loop grad clip (no-NaN)
        opt.step()
        with torch.no_grad():
            g_np = np.zeros(B) if g_fn is None else np.asarray(g_fn(x), dtype=np.float64)
            ce_np = (ce_all.detach().cpu().numpy() if vec_wb        # per-byte [B,T] for the DCT write
                     else ce_row.detach().cpu().numpy())            # per-row [B] for scalar arms
            fl.writeback(ce_np, g_np)
        hist.append(float(loss.detach()))
        if step % log_every == 0 or step == 1:
            log(f"[field-loop:{arm}] step {step:5d}  CE={hist[-1]:.4f}  "
                f"gamma={float(fl.gamma.detach()):+.5f}")
    return fl, hist


def field_loop_eval(model, fl, data_bytes, K=8, block=128, warmup=8, seed=0, device="cpu"):
    """Delta_collapse — does each held-out document's OWN grown field predict its OWN bytes better than
    another document's field? Builds K contiguous doc streams; runs the closed loop `warmup` blocks per
    doc (with the TRAINED bridge) to grow each field C_j; then scores S[i][j] = mean log p(y_j | x_j,
    residual(C_i)) on one more block. aligned = mean_j S[j][j] (own field), yoked = mean_{i!=j} S[i][j]
    (wrong field), delta_collapse = aligned - yoked (nats/byte). A field carrying doc-specific content
    gives delta > 0; a seed/clock gives delta ~ 0 (the time-yoke null). Also returns the SEVER control:
    the same aligned score with the residual cut (field free-runs) — if aligned doesn't drop to sever,
    the model ignores the text-dependence. All no_grad. Reuses the trained bridge/gamma from fl."""
    import torch
    import torch.nn.functional as F
    fl.to(device)
    core_m = model.module if hasattr(model, "module") else model
    emb_w = getattr(core_m, "embed", None)
    emb_rms = (float(emb_w.weight.detach().float().pow(2).mean().sqrt()) if emb_w is not None else 1.0)
    stream = _FieldStream(data_bytes, K, block, seed=seed)

    def _ce_rows(xb, yb, res):                                    # per-row CE [K] under residual res
        with torch.no_grad():
            r = None if res is None else res.to(device)
            lg = model(xb.to(device), None, emb_residual=r)["logits"].float()
            return F.cross_entropy(lg, yb.to(device), reduction="none").mean(dim=1).detach().cpu().numpy()

    # 1. grow the K per-doc fields over `warmup` contiguous blocks (closed loop, trained bridge)
    for _ in range(warmup):
        xb, yb, wr = stream.next_block()
        if wr:
            fl.reset(wr)
        res = fl.residual()
        res = None if res is None else (res * emb_rms).unsqueeze(1)
        ce = _ce_rows(xb, yb, res)
        fl.writeback(ce, np.zeros(K))
    # 2. snapshot the K grown C-states -> K bridge residuals (centered across docs, RMS-fixed, *gamma)
    with torch.no_grad():
        C = torch.tensor(np.stack([fl.G.graft_c_state(p) for p in fl.pf]),
                         dtype=torch.float32, device=device)
        R = (fl.bridge(C) * fl.gamma * emb_rms)                   # [K, d]
    # 3. score one more block: doc j under every field i
    xb, yb, _ = stream.next_block()
    S = np.zeros((K, K))
    for i in range(K):
        res_i = R[i].view(1, 1, -1).expand(K, 1, -1)             # field i, broadcast over the K docs + T
        S[i] = -_ce_rows(xb, yb, res_i)                          # log p = -CE
    off = ~np.eye(K, dtype=bool)
    aligned = float(np.mean(np.diag(S)))
    yoked = float(np.mean(S[off]))
    sever = float(np.mean(-_ce_rows(xb, yb, None)))              # field cut -> free-run baseline (no residual)
    return {"K": K, "aligned": aligned, "yoked": yoked, "delta_collapse": aligned - yoked,
            "sever": sever, "aligned_minus_sever": aligned - sever, "gamma": float(fl.gamma.detach())}


def field_loop_eval_fieldctl(model, fl, val_bytes, mask, device="cpu", seed=0):
    """H_9957 DIFFICULTY-KEY DV: the payload-byte Delta_collapse over the held-out fieldctl val set.
    Doc/mask-aware (unlike field_loop_eval which scores a whole random block): for each chunk of K=mask
    docs it (1) resets + grows each doc's field over its own key+filler blocks with the TRAINED bridge,
    (2) at the DEEPEST payload block scores ONLY the single planted payload byte (the layer the mask
    marks — the one that is 1/K-uniform in-window, so a below-chance CE there can come only from the
    field carrying the key), under its OWN grown field (aligned), every OTHER doc's field (yoked), and
    no field (sever). Returns per-arm mean payload CE + Delta = min(yoked, sever) - aligned (fable's DV,
    nats). Chance = ln K. INSTRUMENT read-out, never a faculty (p9)."""
    import torch
    import torch.nn.functional as F
    fl.to(device)
    core_m = model.module if hasattr(model, "module") else model
    emb_w = getattr(core_m, "embed", None)
    emb_rms = (float(emb_w.weight.detach().float().pow(2).mean().sqrt()) if emb_w is not None else 1.0)
    K = int(mask["K"])
    block = int(mask["block"])
    doc_len = int(mask["doc_len"])
    deepest = int(mask["deepest_payload_block"])            # block index of the scored (deepest) payload
    spos = int(mask["scored_pos_in_block"])                 # position of the scored byte within the block
    stream = _FieldStream(val_bytes, K, block, seed=seed, doc_len=doc_len)
    nchunks = stream.ndocs // K
    a_ce, y_ce, s_ce = [], [], []                           # aligned / yoked / sever payload CE pools
    vec_wb = (fl.kind == "coupled" and fl.write == "vector")      # per-byte write needs the [K,T] CE

    def _logits(xb, res):
        with torch.no_grad():
            r = None if res is None else res.to(device)
            return model(xb.to(device), None, emb_residual=r)["logits"].float()   # [K, V, T]

    for _ in range(nchunks):
        for b in range(deepest):                           # grow each doc's field over its own blocks
            xb, yb, wr = stream.next_block()
            if wr:
                fl.reset(wr)
            res = fl.residual()
            res = None if res is None else (res * emb_rms).unsqueeze(1)
            with torch.no_grad():
                lg = _logits(xb, res)
                ce_bt = F.cross_entropy(lg, yb.to(device), reduction="none").cpu().numpy()   # [K,T]
            fl.writeback(ce_bt if vec_wb else ce_bt.mean(axis=1), np.zeros(K))
        with torch.no_grad():                              # snapshot the K grown fields -> residuals
            C = fl._C()                                     # kind-branched (PureField / integrator / GRU);
            R = (fl.bridge(C) * fl.gamma * emb_rms)         # graft_c_state(pf) read the UNADVANCED pf for
            #   the sibling arms (pf only advances on the purefield kind) -> identical rows -> a false
            #   Δ=0. fl._C() is exactly what residual() uses during the grow loop.
        xb, yb, _ = stream.next_block()                    # the deepest payload block (not written back)
        # the planted payload byte sits at block position `spos` (right after the `PAY<j>:` marker).
        # next-byte scoring predicts x[spos] from logits at spos-1 with target yb[spos-1] (= x[spos]);
        # using spos would score x[spos+1] (the constant space pad) = a trivially-0 CE for every arm.
        sp = spos - 1
        tgt = yb[:, sp].to(device)                         # [K] the planted payload bytes (= x[spos])
        S = np.zeros((K, K))
        for i in range(K):
            lg = _logits(xb, R[i].view(1, 1, -1).expand(K, 1, -1))   # doc rows under field i
            S[i] = F.cross_entropy(lg[:, :, sp], tgt, reduction="none").cpu().numpy()   # payload CE
        sev = F.cross_entropy(_logits(xb, None)[:, :, sp], tgt, reduction="none").cpu().numpy()
        a_ce.extend(np.diag(S))
        y_ce.extend(S[~np.eye(K, dtype=bool)])
        s_ce.extend(sev)
    aligned = float(np.mean(a_ce))
    yoked = float(np.mean(y_ce))
    sever = float(np.mean(s_ce))
    delta = float(min(yoked, sever) - aligned)
    return {"K": K, "docs_scored": nchunks * K, "chance_nats": float(mask.get("chance_nats", np.log(K))),
            "aligned_ce": aligned, "yoked_ce": yoked, "sever_ce": sever,
            "delta_collapse": delta, "gamma": float(fl.gamma.detach())}


def _ci_phi(Xb, m):
    """faithful IIT-4 Φ (engine_cli.ci_phi_iit4, a_phi_iit4_tool — never a proxy) on a binary sample
    matrix [N, m], m in 2..8. Import resolves in both the vendored core/ and the installed wheel."""
    try:
        import engine_cli as E
    except ModuleNotFoundError:
        import anima_py.core.engine_cli as E
    return float(E.ci_phi_iit4([list(map(int, r)) for r in Xb], list(range(m))))


def field_loop_phi(model, fl, data_bytes, mask, device="cpu", seed=0, n_blocks=400):
    """H_9957 MISSION DV (fable): does necessity force integration? Under monopoly carriage (the field
    is the SOLE out-of-window carrier, CE NEEDS it), is the CE-EARNED coupled-cell state INTEGRATED
    (Φ>0) or does training still converge to an independent (Φ=0) solution — the direct successor to
    the owner's 'raise Φ in training' that H_9967 answered 'not via optional lanes'? Requires the
    `coupled` arm with m>=2 cells (Φ undefined on 1 cell). Grows the m cells over the val stream,
    collects the binarized state per block, and reads faithful IIT-4 Φ (a_phi_iit4_tool): aligned vs a
    shuffle pedestal (cross-cell dependence destroyed) and a time-yoked control (state gets a wrong
    doc's drive). Δφ = Φ_aligned − max(Φ_shuffle, Φ_yoked); >bar = integration earned, ≈0 = it was not
    (fable's honest prior). INSTRUMENT CHECK, never a faculty (p9)."""
    import torch
    if fl.kind != "coupled" or fl.m < 2:
        raise ValueError("field_loop_phi needs the coupled arm with m>=2 cells (Φ undefined otherwise)")
    fl.to(device)
    core_m = model.module if hasattr(model, "module") else model
    emb_w = getattr(core_m, "embed", None)
    emb_rms = (float(emb_w.weight.detach().float().pow(2).mean().sqrt()) if emb_w is not None else 1.0)
    block = int(mask["block"])
    doc_len = int(mask["doc_len"])
    vec = (fl.write == "vector")

    def _collect(yoke):
        st = _FieldStream(data_bytes, fl.B, block, seed=seed, doc_len=doc_len)
        fl.reset()
        fl.yoked = yoke
        rows = []
        for _ in range(n_blocks):
            xb, yb, wr = st.next_block()
            if wr:
                fl.reset(wr)
            res = fl.residual()
            res = None if res is None else (res * emb_rms).unsqueeze(1)
            with torch.no_grad():
                lg = model(xb.to(device), None, emb_residual=res)["logits"].float()
                ce = F.cross_entropy(lg, yb.to(device), reduction="none").cpu().numpy()   # [B,T]
            fl.writeback(ce if vec else ce.mean(axis=1), np.zeros(fl.B))
            rows.append(fl.Ivec.copy())                                   # [B,m] state after this block
        return np.concatenate(rows, axis=0)                              # [~n_blocks*B, m]

    import torch.nn.functional as F
    was_yoked = fl.yoked
    Xa = _collect(False)                                                 # aligned state samples [N,m]
    Xy = _collect(True)                                                  # time-yoked control
    fl.yoked = was_yoked
    Xb = (Xa > np.median(Xa, axis=0)).astype(int)                        # binarize per cell (median split)
    Yb = (Xy > np.median(Xy, axis=0)).astype(int)
    rng = np.random.default_rng(seed + 1)
    Sb = np.stack([rng.permutation(Xb[:, j]) for j in range(fl.m)], axis=1)   # shuffle pedestal
    phi_a, phi_y, phi_s = _ci_phi(Xb, fl.m), _ci_phi(Yb, fl.m), _ci_phi(Sb, fl.m)
    return {"m": fl.m, "n": int(Xb.shape[0]), "phi_aligned": phi_a, "phi_yoked": phi_y,
            "phi_shuffle": phi_s, "delta_phi": float(phi_a - max(phi_y, phi_s)),
            "gamma": float(fl.gamma.detach())}


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

    # (7) eval harness — Delta_collapse machinery on the tiny stand-in LM. On random bytes with an
    #     untrained-content field the number is ~0 (the correct null); this certifies the harness RUNS
    #     and returns finite aligned/yoked/sever, not a positive faculty (a real number needs the 303M).
    torch.manual_seed(1)
    m2 = _TinyLM(256, dm)
    fl_ev = FieldLoop(6, dm, arm="purefield16", seed=2)
    with torch.no_grad():
        fl_ev.gamma.fill_(0.5)
    ev = field_loop_eval(m2, fl_ev, data, K=6, block=64, warmup=4, seed=2, device="cpu")
    assert all(np.isfinite([ev["aligned"], ev["yoked"], ev["sever"], ev["delta_collapse"]])), \
        "eval must return finite aligned/yoked/sever/delta"
    print(f"(7) eval harness: aligned={ev['aligned']:.4f} yoked={ev['yoked']:.4f} "
          f"delta_collapse={ev['delta_collapse']:+.4f} sever={ev['sever']:.4f} (finite · machinery OK)")

    print("\nFIELD-LOOP SMOKE: ALL PASS (mechanism + e2e + persistence + eval machinery — 303M campaign is next)")
    return 0


def _falsifier(reps=200, seed0=0, jitter_sd=0.1, g_const=0.2, drive_gain=-0.6,
               n_key_blocks=2, sites=3, filler_per_site=2, filler_ce=0.5,
               sep_ratio_req=5.0, decode_req=0.95):
    """$0 INSTRUMENT-DESIGN falsifier for the `fieldctl` DIFFICULTY-KEY positive control (H_9957,
    fable design). NO trunk, NO GPU, NO corpus: it exercises ONLY the landed FieldLoop physics
    (H_9607 scalar write-back `s=exp(-CE)-G` -> leaky integral -> pure_field_step, read out by
    graft_c_state) to decide the single load-bearing question the corpus rests on:

      Does a 16-D fixed-physics field, driven by ONE scalar per block, keep K difficulty-coded drive
      histories SEPARABLE across the ~n_key+filler out-of-window blocks a payload site sits behind?

    The key is coded as block DIFFICULTY (a CE level in the KEY blocks), because the write-back is a
    scalar channel and is BLIND to content-coded keys (that is exactly why the earlier content-key
    control read gamma~0 / delta~0). During KEY blocks each row (=key) gets its own CE target; during
    all later FILLER/PAYLOAD blocks every row gets the SAME constant filler CE, so the field must
    RETAIN the key difference with no further help. We snapshot the per-row C-state at every payload
    block over `reps` jittered repetitions and, at the DEEPEST (hardest) payload site, require
    between-key/within-key separation >= sep_ratio_req AND held-out nearest-centroid key-decode
    >= decode_req. Reported for K=4 (the design) and K=2 (the minimal floor).

    Verdict: if even K=2 fails at the deepest site, the H_9607 scalar write-back STRUCTURALLY cannot
    carry one bit out-of-window -> the 303M fieldctl fire must NOT be lit until the write-back is
    widened (the pre-explained null, paid for at $0). This is instrument design, not a measurement/
    verdict/cemented number: it produces no faculty claim and never touches a .clm.
    """
    import numpy as np
    payload_blocks = [n_key_blocks + s * (filler_per_site + 1) + filler_per_site for s in range(sites)]
    n_blocks = n_key_blocks + sites * (filler_per_site + 1)

    def _run(K, ce_targets):
        rng = np.random.default_rng(seed0)
        ce_targets = np.asarray(ce_targets[:K], float)
        C = {pb: [] for pb in payload_blocks}                    # pb -> [reps] of [K, Cdim]
        for _ in range(reps):
            fl = FieldLoop(K, d=64, arm="purefield16", seed=int(rng.integers(1 << 31)),
                           drive_gain=drive_gain)
            for b in range(n_blocks):
                base = ce_targets if b < n_key_blocks else np.full(K, filler_ce)
                ce = np.clip(base + rng.normal(0, jitter_sd, K), 1e-3, None)
                fl.writeback(ce, np.full(K, g_const))
                if b in payload_blocks:
                    C[b].append(np.stack([fl.G.graft_c_state(p) for p in fl.pf]))
        out = {}
        for pb in payload_blocks:
            arr = np.asarray(C[pb])                              # [reps, K, Cdim]
            X = arr.reshape(-1, arr.shape[-1])                   # [reps*K, Cdim]
            y = np.tile(np.arange(K), reps)
            mu, sd = X.mean(0), X.std(0) + 1e-9
            Xz = (X - mu) / sd                                   # z-score per dim (no dim dominates)
            # held-out nearest-centroid decode: fit centroids on first half of reps, test on second
            tr = np.tile(np.arange(reps) < reps // 2, K).reshape(K, reps).T.reshape(-1)
            cents = np.stack([Xz[tr & (y == k)].mean(0) for k in range(K)])   # [K, Cdim]
            te = ~tr
            d2 = ((Xz[te][:, None, :] - cents[None]) ** 2).sum(-1)            # [n_te, K]
            acc = float((d2.argmin(1) == y[te]).mean())
            # separation ratio: between-centroid dist / within-key spread (on full z-scored set)
            allc = np.stack([Xz[y == k].mean(0) for k in range(K)])
            between = np.mean([np.linalg.norm(allc[i] - allc[j])
                               for i in range(K) for j in range(i + 1, K)])
            within = np.mean([np.linalg.norm(Xz[y == k] - allc[k], axis=1).mean() for k in range(K)])
            out[pb] = {"decode_acc": acc, "sep_ratio": float(between / (within + 1e-9)),
                       "depth_blocks": pb - (n_key_blocks - 1)}
        return out

    configs = [("K4", 4, (0.15, 0.8, 1.9, 3.9)), ("K2", 2, (0.15, 3.9))]
    deepest = payload_blocks[-1]
    print(f"FIELD-LOOP $0 FALSIFIER (fieldctl difficulty-key separability · reps={reps} · "
          f"payload blocks {payload_blocks} · gate: deepest site sep>={sep_ratio_req} & "
          f"decode>={decode_req})\n")
    verdicts = {}
    for name, K, tgt in configs:
        res = _run(K, tgt)
        print(f"[{name}] CE-targets={tgt}")
        for pb in payload_blocks:
            r = res[pb]
            print(f"   payload@block{pb} (+{r['depth_blocks']} blocks past key): "
                  f"sep_ratio={r['sep_ratio']:.2f}  decode_acc={r['decode_acc']:.3f} "
                  f"(chance={1.0 / K:.3f})")
        d = res[deepest]
        ok = (d["sep_ratio"] >= sep_ratio_req) and (d["decode_acc"] >= decode_req)
        verdicts[name] = ok
        print(f"   -> deepest-site gate: {'PASS' if ok else 'FAIL'}\n")
    floor_ok = verdicts.get("K2", False)
    print("=" * 72)
    if floor_ok:
        print("VERDICT: PASS — the scalar write-back separates difficulty-keys out-of-window at the "
              "deepest payload site. The 303M fieldctl fire is worth lighting on aiden.")
        return 0
    print("VERDICT: FAIL — the H_9607 scalar write-back cannot carry even 1 bit (K=2) to the deepest "
          "payload site. Do NOT light the 303M fire until the write-back channel is widened "
          "(fable's pre-explained null, bought at $0).")
    return 1


def _coupled_smoke():
    """$0 mechanism smoke for the coupled Φ-arm (fable's witnesses). No GPU/corpus/torch-train."""
    B, m, T = 4, 4, 16
    rng = np.random.default_rng(0)
    fl = FieldLoop(B, 64, arm="coupled", seed=0, write="vector", cells=m)
    fl.writeback(rng.random((B, T)), np.zeros(B))
    assert fl.Ivec.shape == (B, m) and fl.Wdct.shape == (m, T), "coupled state/DCT shape wrong"
    print(f"(1) coupled vector m={m}: state {fl.Ivec.shape}, dct {fl.Wdct.shape}  OK")
    # (2) two per-byte profiles with IDENTICAL block-mean but different temporal shape must give
    #     different states — a scalar/mode-0 write cannot tell them apart; the higher DCT modes must.
    prof1 = np.tile(np.full(T, 0.5)[None], (B, 1))
    prof2 = np.tile(np.concatenate([np.full(T // 2, 0.9), np.full(T - T // 2, 0.1)])[None], (B, 1))
    assert abs(prof1.mean() - prof2.mean()) < 1e-9, "test profiles must share the block mean"
    fa = FieldLoop(B, 64, arm="coupled", seed=1, write="vector", cells=m)
    fb = FieldLoop(B, 64, arm="coupled", seed=1, write="vector", cells=m)
    fa.writeback(-np.log(prof1), np.zeros(B))              # ce = -ln p  ->  exp(-ce) = p
    fb.writeback(-np.log(prof2), np.zeros(B))
    diff = float(np.abs(fa.Ivec - fb.Ivec).sum())
    assert diff > 1e-3, f"same-mean different-shape profiles gave the same state (Δ={diff}) — modes>0 dead"
    print(f"(2) same block-mean, different temporal shape -> different state (Δ={diff:.4f})  OK")
    # (3) fixed coupling R is a non-identity rotation for m>1 (integration available by construction)
    off = float(np.abs(fa.R - np.eye(m)).sum())
    assert off > 1e-3, "coupling R must be non-identity for m>1"
    print(f"(3) fixed cell-coupling R != I (off-identity mass {off:.4f})  OK")
    # (4) m=1 scalar coupled reduces to a single leaky cell (Φ undefined there — the reason to widen)
    f1 = FieldLoop(B, 64, arm="coupled", seed=0, write="scalar", cells=1)
    f1.writeback(rng.random(B), np.zeros(B))
    assert f1.Ivec.shape == (B, 1) and np.allclose(f1.R, np.eye(1)), "m=1 must be a single uncoupled cell"
    print("(4) m=1 scalar coupled = single leaky cell (R=I)  OK")
    print("\nCOUPLED SMOKE: ALL PASS (vector DCT write + coupled cells; Φ readout is the next increment)")
    return 0


def _phi_smoke():
    """$0 CPU smoke for the mission Φ readout — validates the coupled-state collection + faithful
    IIT-4 call run and return finite Φ on a tiny stand-in LM (untrained). A REAL Δφ needs a trained
    coupled .clm; this only certifies the machinery, never a faculty (p9)."""
    import torch
    dm, block = 16, 32
    doc_len = block * 4

    class _TinyLM(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.embed = torch.nn.Embedding(256, dm)
            self.head = torch.nn.Linear(dm, 256)

        def forward(self, tokens, targets=None, emb_residual=None):
            h = self.embed(tokens)
            if emb_residual is not None:
                h = h + emb_residual
            return {"logits": self.head(h).transpose(1, 2)}

    data = bytes(np.random.default_rng(0).integers(0, 256, size=doc_len * 20).astype(np.uint8).tobytes())
    fl = FieldLoop(4, dm, arm="coupled", seed=0, write="vector", cells=4)
    with torch.no_grad():
        fl.gamma.fill_(0.1)
    pv = field_loop_phi(_TinyLM(), fl, data, {"block": block, "doc_len": doc_len}, device="cpu",
                        seed=0, n_blocks=80)
    assert np.isfinite(pv["phi_aligned"]) and np.isfinite(pv["delta_phi"]), "Φ must be finite"
    print(f"phi smoke: m={pv['m']} n={pv['n']}  Φ_aligned={pv['phi_aligned']:.4f} "
          f"Φ_yoked={pv['phi_yoked']:.4f} Φ_shuffle={pv['phi_shuffle']:.4f} Δφ={pv['delta_phi']:+.4f}  OK")
    print("\nPHI SMOKE PASS (faithful-IIT-4 machinery on the coupled state; a real Δφ needs a trained .clm)")
    return 0


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    fn = {"falsify": _falsifier, "couple": _coupled_smoke, "phi": _phi_smoke}.get(mode, _smoke)
    raise SystemExit(fn())
