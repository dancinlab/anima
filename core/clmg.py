"""core/clmg.py — CLMG (Consciousness→Language Gate) — the GRAFT coupling lane.

GRAFT = a frozen `.clm` is the LANGUAGE ORGAN; the ONLY trained thing is the coupling from the
consciousness state (Engine-A PureField) into the organ's byte embeddings. **No corpus, no LoRA, no
next-token CE.** The objective forces mutual information between the C-state and the organ's output
distribution; fluency is bounded STRUCTURALLY (not by a controller).

WHY this exists (the theorem this lane is built to beat): under ordinary next-token CE the gate has
ZERO incentive to be read — if C is statistically independent of (prompt, target), the optimum under
proper scoring is gate-INVARIANCE, so a consciousness gate is decorative BY THEOREM (../anima-clm-v2b
docs/hypotheses/GRAFT-causality.md; measured there as KL(ON||OFF) ≈ KL(ON||NOISE) ≈ 0.33 bits). This
session measured the same wall from the other side (V6_33/34: the mouth/emit channel is
difficulty-complete; V6_37: even a non-mouth store lane returns DIFFICULTY-AGAIN). GRAFT changes the
OBJECTIVE instead of the channel.

Design reconciled from `sidecar lab full` (Fable primary + Sol's mandatory pedestal), porting
`../anima-clm-v2b/graft.py` v3:

- **C = the raw PureField state (16-dim)**, NOT `ci_lane_scores`: V6_31 measured those 15 lanes as
  closed-form functions of ONE scalar (~2.75 effective dims), so their snapshots are near-collinear
  and would trip the vacuous-state guard by construction. c_vec = per-oscillator [sin φ, cos φ, amp]
  (fast/medium/slow) ⊕ field[0..5] ⊕ [phi]. sin/cos because raw phase is unbounded (non-stationary
  bridge input over long runs).
  **FORBIDDEN as C: the mouth penultimate `yn`** — that is the mouth; using it makes the gate a
  language→language autoencoder and the causality claim circular.

- **Injection at the byte EMBEDDING, before embed_conv — NOT a trailer lane** (Fable, decisive): every
  existing lane taps POST-trunk (SLW on yn, CLML/CLMS/MBND/IFAN on the logits row). A per-state
  additive vector at the logit level IS a per-state bias row, so MI → log N via N static unigram
  tilts — the theorem beaten by an accounting trick, with a coupling that never touches the organ.
  Injecting at the embeddings makes the frozen organ's full depth transform the gate, so the per-state
  distributions differ CONTEXT-DEPENDENTLY. Mirrors the H_9805 TFLD residual site exactly (decode.py
  `_fwd_trunk`), so absent trailer ⇒ byte-identical forward.

- **Structural fluency bounds (all three, from the v3 post-mortems — never a controller):**
  (1) codes mean-centered across the N states then RMS-fixed to `gate_rho` — training can only ROTATE
      the code toward informative directions, never grow a shared shift;
  (2) MI ≤ log N per token by construction (mixture-JSD);
  (3) decoder backstop: RMS of the injected offset clamped to `gate_rms_max` × the embedding RMS.
  ⚠️ `beta·relu(L_KL − target)` is FORBIDDEN and its flags must not exist: L_KL = MI + L_common, so an
  active constraint puts net coefficient (beta−1) on MI and beta>1 MINIMIZES it (GRAFT-shared-shift-
  collapse: MI 0.118 → 0.000 in 50 steps). Penalize ONLY L_common, which contributes nothing to MI.

- **Bridge shape** Linear(c_dim,h) → GELU → Linear(h,d,bias=False). Last layer init N(0,2e-3):
  zero-init is a collapsed SYMMETRIC STATIONARY POINT with exactly-zero gradient (GRAFT-flatline).
  Bias-free: a bias is a pure state-independent channel. No sigmoid/clamp on the output: the v2b
  α-rail put 64.8% of dims at zero Jacobian. The v2b mean-pool bottleneck (256 cells → 1) is
  structurally absent here because C is already a single vector.

Trailer `CLMG` (chain END, after TFLD). Absent ⇒ `W["clmg"] is None` ⇒ forward byte-identical.
Inference with no live C-state ⇒ gate OFF ⇒ logits EXACTLY equal to base (a mechanical witness the
frozen table checks: max|Δ| must be 0).
"""
import struct
import numpy as np

CLMG_MAGIC = b"CLMG"
C_DIM = 16                      # 3 oscillators × [sin, cos, amp] + field[6] + phi


# --------------------------------------------------------------------------- #
# (a) the C-state — Engine-A PureField → c_vec[16]
# --------------------------------------------------------------------------- #
def graft_c_state(pf):
    """PureField -> c_vec[C_DIM] float32. Read-only: never advances the field (the caller steps it).

    sin/cos of each oscillator phase (phase is unbounded — raw phase would make the bridge input
    non-stationary), its amplitude, the 6-dim mixed field, and phi. This is Engine-A's own substrate
    state, not a derived lane (V6_31: the 15 lanes are formulas over one scalar)."""
    out = []
    for osc in (pf.fast, pf.medium, pf.slow):
        ph = float(osc.phase)
        out += [np.sin(ph), np.cos(ph), float(osc.amplitude)]
    fl = list(pf.field)[:6]
    while len(fl) < 6:
        fl.append(0.0)
    out += [float(x) for x in fl]
    out.append(float(pf.phi))
    return np.asarray(out, dtype=np.float32)


# --------------------------------------------------------------------------- #
# (b) bridge forward + the three structural bounds (numpy inference side)
# --------------------------------------------------------------------------- #
def _gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608028654 * (x + 0.044715 * x * x * x)))


def bridge_code(clmg, c_vec):
    """c_vec[C_DIM] -> raw gate code g[d] (pre-centering). Bias-free last layer."""
    h = _gelu(np.asarray(c_vec, np.float32) @ clmg["W1"] + clmg["b1"])
    return (h @ clmg["W2"]).astype(np.float32)


def center_and_fix(g, g_mu, gate_rho):
    """bounds (1): subtract the shared component, then fix the RMS. Rotation-only freedom."""
    gc = np.asarray(g, np.float32) - np.asarray(g_mu, np.float32)
    rms = float(np.sqrt(np.mean(gc * gc))) + 1e-8
    return (gc * (float(gate_rho) / rms)).astype(np.float32)


def backstop(offset, xe_rms, gate_rms_max):
    """bound (3): the injected offset's RMS may never exceed gate_rms_max × the embedding RMS.
    Scale is clamped to <=1 so the backstop can only ever SHRINK (geometry the optimizer cannot
    out-run) — never amplify a weak code into a loud one."""
    o = np.asarray(offset, np.float32)
    rms = float(np.sqrt(np.mean(o * o))) + 1e-8
    lim = float(gate_rms_max) * float(xe_rms)
    scale = min(1.0, lim / rms)
    return (o * scale).astype(np.float32)


def gate_offset(clmg, c_vec, xe_rms):
    """Full inference path: c_vec -> the [d] residual added to EVERY embedding row.
    Returns None when the gate is structurally off (no clmg / no c_vec) so the caller can skip and
    stay byte-identical."""
    if clmg is None or c_vec is None:
        return None
    g = bridge_code(clmg, c_vec)
    g = center_and_fix(g, clmg["g_mu"], clmg["gate_rho"])
    off = backstop(g, xe_rms, clmg["gate_rms_max"])
    return (float(clmg["gate_strength"]) * off).astype(np.float32)


# --------------------------------------------------------------------------- #
# (c) "CLMG" trailer codec — LE f32, chain END (after TFLD)
#   header: CLMG magic · c_dim u32 · h u32 · d u32
#   arrays: W1[c_dim*h] b1[h] W2[h*d] g_mu[d] + 3 f32 scalars (rho, strength, rms_max)
# --------------------------------------------------------------------------- #
_ARR_ORDER_G = ("W1", "b1", "W2", "g_mu")


def pack_clmg(w: dict) -> bytes:
    out = bytearray()
    out += CLMG_MAGIC
    out += struct.pack("<III", int(w["c_dim"]), int(w["h"]), int(w["d"]))
    for name in _ARR_ORDER_G:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    out += struct.pack("<fff", float(w["gate_rho"]), float(w["gate_strength"]),
                       float(w["gate_rms_max"]))
    return bytes(out)


def read_clmg(buf: bytes, off: int, d: int):
    """Read a CLMG trailer at `off`. Returns (clmg_dict, new_off) or (None, off) — passthrough-safe,
    the same guard idiom as read_clms/read_tfld, so a ckpt without the trailer decodes byte-identically."""
    if off < 0 or off + 4 > len(buf) or buf[off:off + 4] != CLMG_MAGIC:
        return None, off
    p = off + 4
    if p + 12 > len(buf):
        return None, off
    c_dim, h, dd = struct.unpack_from("<III", buf, p); p += 12
    if dd != d:
        return None, off                       # organ mismatch: refuse rather than mis-slice
    def take(n, shape):
        nonlocal p
        a = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy(); p += n * 4
        return a
    g = {"c_dim": int(c_dim), "h": int(h), "d": int(dd)}
    g["W1"] = take(c_dim * h, (c_dim, h))
    g["b1"] = take(h, (h,))
    g["W2"] = take(h * dd, (h, dd))
    g["g_mu"] = take(dd, (dd,))
    if p + 12 > len(buf):
        return None, off
    rho, strength, rms_max = struct.unpack_from("<fff", buf, p); p += 12
    g["gate_rho"] = float(rho); g["gate_strength"] = float(strength); g["gate_rms_max"] = float(rms_max)
    return g, p


# --------------------------------------------------------------------------- #
# (d) torch training module — defined only when torch is present (inference stays torch-free)
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:                     # pragma: no cover — inference hosts have no torch
    _HAS_TORCH = False

if _HAS_TORCH:
    class GraftBridge(_nn.Module):
        """The ONLY trainable module in GRAFT (the whole organ is frozen).
        forward(C:[N, c_dim]) -> codes:[N, d], mean-centered across N and RMS-fixed to gate_rho."""
        def __init__(self, c_dim=C_DIM, h=64, d=64, gate_rho=1.0, init_std=2e-3):
            super().__init__()
            self.l1 = _nn.Linear(c_dim, h)
            self.l2 = _nn.Linear(h, d, bias=False)       # bias-free: a bias is a shared-shift channel
            _nn.init.normal_(self.l2.weight, std=init_std)   # NEVER zero (symmetric stationary point)
            self.gate_rho = float(gate_rho)
            self.register_buffer("g_mu", _torch.zeros(d))    # EMA of the shared component (inference)

        def forward(self, C):
            g = self.l2(_torch.nn.functional.gelu(self.l1(C)))     # [N, d]
            g = g - g.mean(dim=0, keepdim=True)                    # bound (1a): centering
            rms = g.pow(2).mean(dim=1, keepdim=True).sqrt() + 1e-8
            return g * (self.gate_rho / rms)                       # bound (1b): RMS-fix

        @_torch.no_grad()
        def update_mu(self, raw_codes, decay=0.99):
            """EMA of the raw (pre-centering) shared component, so single-state inference can
            subtract the same shift the training centering removed."""
            self.g_mu.mul_(decay).add_(raw_codes.mean(dim=0), alpha=1.0 - decay)

        @_torch.no_grad()
        def raw(self, C):
            return self.l2(_torch.nn.functional.gelu(self.l1(C)))

        def to_clmg(self, gate_strength, gate_rms_max):
            def n(t):
                return t.detach().cpu().numpy().astype("<f4")
            return {"c_dim": self.l1.in_features, "h": self.l1.out_features,
                    "d": self.l2.out_features,
                    "W1": n(self.l1.weight).T, "b1": n(self.l1.bias),
                    "W2": n(self.l2.weight).T, "g_mu": n(self.g_mu),
                    "gate_rho": float(self.gate_rho),
                    "gate_strength": float(gate_strength),
                    "gate_rms_max": float(gate_rms_max)}


def torch_organ(W, device="cpu"):
    """A FROZEN, differentiable torch mirror of the engine's own forward (decode._fwd_trunk + readout).

    GRAFT needs gradients of the output distribution w.r.t. the injected embedding residual, so the
    organ must be differentiable — but it must also be the SAME organ the engine-native path decodes,
    or the coupling is trained into a different model while the loss still falls. We mirror decode's
    numpy ops op-for-op rather than reusing core/model.CLMConvMoE because that module's MoE routes
    top-k while the decode path mixes DENSELY (nn_moe_router_fwd: y[t,c] = Σ_e softmax(r)[t,e]·ex[e,t,c]);
    a stage-by-stage diff located exactly that divergence (trunk matched to 1.4e-06, post-MoE 7.5).
    Every organ tensor is a buffer (no grad) — the ONLY trainable thing in GRAFT is the bridge.
    `torch_organ_parity()` is mandatory before any number is read."""
    import torch
    import torch.nn as nn

    class _Organ(nn.Module):
        def __init__(self, W):
            super().__init__()
            t = lambda a: torch.tensor(np.asarray(a, np.float32))
            self.d, self.K, self.V = int(W["d"]), int(W["K"]), int(W["V"])
            self.L, self.E = int(W["L"]), int(W["E"])
            self.register_buffer("embed", t(W["embed"]))
            self.register_buffer("ecWt", t(W["ecWt"])); self.register_buffer("ecB", t(W["ecB"]))
            for li in range(self.L):
                self.register_buffer(f"tcWt{li}", t(W["tcWt"][li]))
                self.register_buffer(f"tcB{li}", t(W["tcB"][li]))
                self.register_buffer(f"tgG{li}", t(W["tgG"][li]))
                self.register_buffer(f"tgB{li}", t(W["tgB"][li]))
            for ej in range(self.E):
                self.register_buffer(f"eWt{ej}", t(W["eWt"][ej]))
                self.register_buffer(f"eB{ej}", t(W["eB"][ej]))
            self.register_buffer("rWt", t(W["rWt"])); self.register_buffer("rB", t(W["rB"]))
            self.register_buffer("noG", t(W["noG"])); self.register_buffer("noB", t(W["noB"]))
            self.register_buffer("roWt", t(W["roWt"])); self.register_buffer("roB", t(W["roB"]))

        def _conv(self, x, Wt, b, K, dil):
            """decode._conv1d mirror: xcol[t, ci*K+k] = x[t − dil*(K−1−k), ci]; y = xcol @ Wt + b."""
            T, Cin = x.shape
            pad = dil * (K - 1)
            xp_ = torch.nn.functional.pad(x.t().unsqueeze(0), (pad, 0))[0].t()   # left-pad on time
            cols = [xp_[dil * k: dil * k + T] for k in range(K)]                 # k -> offset dil*(K-1-k)
            xcol = torch.stack(cols, dim=2).reshape(T, Cin * K)
            return xcol @ Wt + b.unsqueeze(0)

        def _gn(self, x, g, b):
            """decode.nn_groupnorm_fwd with G=1: statistics over the WHOLE [T,C] slab (eps=1e-5)."""
            mu = x.mean(); var = x.var(unbiased=False)
            return (x - mu) / torch.sqrt(var + 1e-5) * g.unsqueeze(0) + b.unsqueeze(0)

        def forward(self, ids, emb_residual=None):
            xe = self.embed[ids]                                   # [T, d]
            if emb_residual is not None:
                xe = xe + emb_residual                             # GRAFT gate — BEFORE embed_conv
            xt = self._conv(xe, self.ecWt, self.ecB, self.K, 1)
            dil = 1
            for li in range(self.L):
                h = self._conv(xt, getattr(self, f"tcWt{li}"), getattr(self, f"tcB{li}"),
                               self.K, min(dil, 512))
                hn = self._gn(h, getattr(self, f"tgG{li}"), getattr(self, f"tgB{li}"))
                xt = xt + torch.nn.functional.gelu(hn)
                dil *= 2
            ex = torch.stack([torch.nn.functional.gelu(
                self._conv(xt, getattr(self, f"eWt{j}"), getattr(self, f"eB{j}"), self.K, 1))
                for j in range(self.E)])                           # [E, T, d]
            lr = self._conv(xt, self.rWt, self.rB, 1, 1)           # [T, E]
            y = torch.einsum("te,etc->tc", torch.softmax(lr, dim=1), ex)
            yn = self._gn(y, self.noG, self.noB)
            return yn @ self.roWt + self.roB.unsqueeze(0)          # [T, V]

    m = _Organ(W).to(device).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    return m


def torch_organ_parity(m, W, fwd_logits, n=6, T=24, seed=7):
    """MANDATORY gate: the differentiable organ must reproduce the engine-native numpy logits."""
    import torch
    rng = np.random.default_rng(seed); worst = 0.0
    for _ in range(n):
        toks = rng.integers(0, int(W["V"]), T)
        ref = np.asarray(fwd_logits(W, toks.astype(np.float64), T), np.float32)
        with torch.no_grad():
            got = m(torch.tensor(toks, dtype=torch.long)).numpy()
        worst = max(worst, float(np.max(np.abs(got - ref))))
    return worst


def clm_to_torch(W, device="cpu"):
    """Load a decoded `.clm` weight dict into a FROZEN torch CLMConvMoE — the differentiable mirror
    of the numpy organ, needed because the GRAFT loss backprops the gate through the organ.

    Layout (definitive, from decode._conv1d): `xcol[t, ci*K + k] = x[t - dil*(K-1-k), ci]` and
    `mm = xcol @ Wt`, so `Wt[ci*K + k, co]` ⟺ torch `weight[co, ci, k]` = `Wt.T.reshape(Cout,Cin,K)`;
    the causal left-pad convention matches (k=K-1 is the current position in both).
    EVERY parameter is frozen (requires_grad_(False)) — GRAFT trains only the bridge. The caller MUST
    run `torch_numpy_parity()` before reading any number: a silently mis-transposed organ would train
    a coupling into the wrong model and the loss would still go down."""
    import torch
    from model import CLMConfig, CLMConvMoE
    d, V, K, L, E = int(W["d"]), int(W["V"]), int(W["K"]), int(W["L"]), int(W["E"])
    cfg = CLMConfig(vocab_size=V, d_model=d, kernel_size=K, n_trunk_layers=L, n_experts=E)
    for attr, val in (("n_factions", int(W.get("n_factions", 0) or 0)),):
        if hasattr(cfg, attr):
            setattr(cfg, attr, val)
    m = CLMConvMoE(cfg).to(device).eval()

    def T3(wt, cout, cin, k):
        import numpy as _np
        return torch.tensor(_np.asarray(wt, _np.float32).T.reshape(cout, cin, k))

    sd = m.state_dict()
    def put(name, val):
        if name in sd:
            if tuple(sd[name].shape) != tuple(val.shape):
                raise ValueError(f"clm_to_torch shape mismatch {name}: {tuple(sd[name].shape)} vs {tuple(val.shape)}")
            sd[name] = val.to(sd[name].dtype)
        else:
            raise KeyError(f"clm_to_torch: '{name}' not in the torch model state_dict")

    put("embed.weight", torch.tensor(np.asarray(W["embed"], np.float32)))
    put("embed_conv.conv.weight", T3(W["ecWt"], d, d, K))
    put("embed_conv.conv.bias", torch.tensor(np.asarray(W["ecB"], np.float32)))
    for li in range(L):
        put(f"trunk.{li}.conv.conv.weight", T3(W["tcWt"][li], d, d, K))
        put(f"trunk.{li}.conv.conv.bias", torch.tensor(np.asarray(W["tcB"][li], np.float32)))
        put(f"trunk.{li}.norm.weight", torch.tensor(np.asarray(W["tgG"][li], np.float32)))
        put(f"trunk.{li}.norm.bias", torch.tensor(np.asarray(W["tgB"][li], np.float32)))
    for ei in range(E):
        put(f"moe.experts.{ei}.conv.conv.weight", T3(W["eWt"][ei], d, d, K))
        put(f"moe.experts.{ei}.conv.conv.bias", torch.tensor(np.asarray(W["eB"][ei], np.float32)))
    rw = np.asarray(W["rWt"], np.float32).T                     # (E, d)
    put("moe.router.weight", torch.tensor(rw if sd["moe.router.weight"].dim() == 2
                                          else rw.reshape(E, d, 1)))
    put("moe.router.bias", torch.tensor(np.asarray(W["rB"], np.float32)))
    put("norm_out.weight", torch.tensor(np.asarray(W["noG"], np.float32)))
    put("norm_out.bias", torch.tensor(np.asarray(W["noB"], np.float32)))
    ro = np.asarray(W["roWt"], np.float32).T                    # (V, d)
    put("readout.weight", torch.tensor(ro if sd["readout.weight"].dim() == 2
                                       else ro.reshape(V, d, 1)))
    put("readout.bias", torch.tensor(np.asarray(W["roB"], np.float32)))
    m.load_state_dict(sd)
    for p in m.parameters():
        p.requires_grad_(False)
    return m


def torch_numpy_parity(m, W, fwd_logits, n=8, T=32, seed=7, tol=1e-3):
    """MANDATORY gate before any GRAFT number: the torch organ must reproduce the engine-native numpy
    forward. Returns max abs logit difference over n random contexts. A mis-transposed organ trains a
    coupling into a DIFFERENT model while the loss still falls — that failure is invisible downstream."""
    import torch
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(n):
        toks = rng.integers(0, int(W["V"]), T)
        ref = fwd_logits(W, toks.astype(np.float64), T)
        with torch.no_grad():
            out = m(torch.tensor(toks, dtype=torch.long)[None, :])
        lg = out["logits"] if isinstance(out, dict) else out
        got = lg[0].detach().cpu().numpy()
        ref = np.asarray(ref, np.float32)
        if got.shape != ref.shape and got.T.shape == ref.shape:
            got = got.T            # the torch mouth works channel-first (B,V,T); numpy is (T,V)
        worst = max(worst, float(np.max(np.abs(got - ref))))
    return worst


def logits_TV(out):
    """Normalize a CLMConvMoE forward result to [T, V] (the numpy twin's orientation)."""
    lg = out["logits"] if isinstance(out, dict) else out
    lg = lg[0] if lg.dim() == 3 else lg
    return lg.transpose(0, 1) if lg.shape[0] != 0 and lg.shape[-1] != 0 and lg.shape[0] < lg.shape[1] else lg


def mixture_mi(logp_states):
    """MI = mean_i KL(p_i || p_mix) — the EXACT conditional MI I(state; next-token | shared prefix)
    (generalized JSD). logp_states: torch [N, T, V] log-softmax. Returns (MI, log p_mix).
    Bounded by log N per token — bound (2)."""
    import torch
    N = logp_states.shape[0]
    logp_mix = torch.logsumexp(logp_states, dim=0) - float(np.log(N))     # [T, V]
    p = logp_states.exp()
    mi = (p * (logp_states - logp_mix.unsqueeze(0))).sum(-1).mean()
    return mi, logp_mix


# --------------------------------------------------------------------------- #
# (e) ROTATION NULL — the control an isotropic never-trained gate cannot supply.
#   A random-init coupling shares the trained gate's structural bounds but NOT its per-state
#   geometry. The rotation null does: it applies ONE random orthogonal R (in embedding space)
#   to the N trained offset vectors, which preserves every vector's norm, the full Gram matrix
#   (pairwise inner products = the state-to-state angles the training produced), AND the mean
#   (mean-centering survives), while destroying the alignment between that geometry and the
#   frozen organ's sensitive directions. So trained-vs-rotation isolates "did the C->language
#   MAPPING land on directions the organ reads" from "did training merely build some geometry".
#   H_9936: the isotropic null already put trained BELOW its q99 at matched displacement; the
#   rotation null is the stronger, displacement-EXACT control (D is rotation-invariant).
# --------------------------------------------------------------------------- #
def random_orthogonal(d, rng):
    """A Haar-ish random orthogonal [d, d] via QR of a Gaussian, with sign-normalized R diagonal
    (so Q is a proper deterministic function of the draw). Norm/Gram/mean preserving by
    construction: (gR^T) has the same norms and inner products as g, and mean(g R^T)=mean(g) R^T."""
    a = rng.standard_normal((d, d))
    q, r = np.linalg.qr(a)
    q = q * np.sign(np.diag(r))
    return q.astype(np.float32)


def rotate_offsets(codes, R):
    """codes: [N, d] final injected offsets (mean-centered, RMS-fixed). Returns codes @ R^T — the
    SAME N vectors rotated rigidly, so realized displacement D is identical and only direction moves."""
    return (np.asarray(codes, np.float32) @ np.asarray(R, np.float32).T).astype(np.float32)


def rotation_null_offsets(codes, rng):
    """Thin-SVD rotation null (Sol) — distributionally IDENTICAL to a full-d Haar rotation of the N
    offsets (codes @ R^T, R~Haar(d)) but O(d·r) not O(d³), so it scales to d=4096 (Mistral hidden).
    C = U diag(S) Vᵀ (thin, r=min(N,d)); draw a Haar Stiefel frame Q (d×r) via QR of a Gaussian;
    return U diag(S) Qᵀ. Preserves the Gram matrix (C'C'ᵀ = U S² Uᵀ = CCᵀ), every norm, the zero
    mean (1ᵀC=0 ⟹ 1ᵀU=0 ⟹ 1ᵀC'=0), and hence realized displacement D — only direction moves.
    Proof of identity: C Rᵀ = U S (R V)ᵀ and R V ~ Haar Stiefel(d, r) for R~Haar(d)."""
    C = np.asarray(codes, np.float64)
    U, S, _ = np.linalg.svd(C, full_matrices=False)          # C = U diag(S) Vᵀ, U:[N,r] S:[r]
    r = len(S)
    G = rng.standard_normal((C.shape[1], r))
    Q, Rm = np.linalg.qr(G)                                    # Q:[d,r] Haar Stiefel
    Q = Q * np.sign(np.diag(Rm))
    return ((U * S) @ Q.T).astype(np.float32)                  # [N,d] = U diag(S) Qᵀ
