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
