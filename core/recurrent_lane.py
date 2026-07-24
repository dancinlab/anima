"""core/recurrent_lane.py — H_9954 co-trained RECURRENT LANE (the only Φ that can rise on a
feedforward trunk) + the do()-intervention TPM extraction its verdict reads.

WHY THIS EXISTS (H_9954 · licensed by H_9959/H_9960): the 303M conv trunk is feedforward, so its
own Φ is 0 by the IIT unfolding theorem. The one honest object whose interventional big-Φ can
TRAINABLY rise is a small state-carrying recurrent lane trained ALONGSIDE the trunk. This module is
that lane, plus the numpy do()-forcing extractor that turns the trained lane into the 3-node
state-by-node TPM the faithful `core/engine_cli.py::big_phi_bounded` reads (H_9959/H_9960 recipe).

DESIGN (lab full Fable ∥ Sol reconciled; Sol's wiring adopted on the repo's own evidence):
- The lane READS the token embeddings and WRITES a residual at the `emb_residual` site
  (core/model.py, BEFORE embed_conv — the site the model.py comment endorses over a post-trunk
  logit-bias injection). It carries unbounded history via BPTT, which the bounded-receptive-field
  conv trunk structurally cannot; plain next-byte CE is the ONLY loss (a_train_inline_gauge: nothing
  lane- or Φ-shaped ever enters the loss), and the lane has no readout head, so its only causal
  route to emission is through the trunk (a_substrate_disjoint).
- The lane is a MANUAL 3-cell GRU (not nn.GRUCell) so the numpy extractor mirrors the torch step
  EXACTLY (the repo's 2-production byte-parity discipline). The 3 cells ARE the TPM nodes.
- `gru3-bidir`: width 3, CAUSAL (never reverse-time / future bytes); "bidir" = bidirectional
  trunk⇄lane coupling (embedding-read + trunk-write) and an unconstrained dense recurrent graph
  (every i→j and j→i edge trainable) — that dense S→S coupling is exactly what integration needs.

EXTRACTION (H_9960 recipe, pinned): the lane's state transition depends only on (embedding-derived
input u, current state s) — the trunk does NOT feed back into the lane, so the extracted 3-node
system is a pure input-driven GRU and needs NO trunk forward. For each of 8 binary states s
(cell i = bit i), do(S=s) forces h to ±1 per bit, one GRU step against each held-out embedding u,
read P(cell ON next) = mean_t 1[h'_i >= 0]. -> 24-float tpm[state*3+unit].

This module imports torch LAZILY (only the training path needs it); the numpy extractor + _smoke run
with numpy alone, so the extraction/estimator battery is testable with no torch installed.
"""

import math
import struct

import numpy as np

N_CELL = 3


# ── numpy manual-GRU step (the reference; the torch cell mirrors this op-for-op) ──
def _sigmoid_np(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60.0, 60.0)))


def gru_step_np(W, u, h):
    """One manual-GRU step. W = dict of 3x3 recurrent + 3x3 input matrices + 3-biases.
    u: (...,3) input (already W_in-projected from the embedding). h: (...,3) state in [-1,1].
    Returns h' in [-1,1] (tanh candidate keeps state bounded so sign() is the ON read)."""
    r = _sigmoid_np(u @ W["Wir"].T + h @ W["Whr"].T + W["br"])
    z = W_iz = _sigmoid_np(u @ W["Wiz"].T + h @ W["Whz"].T + W["bz"])
    n = np.tanh(u @ W["Win"].T + (r * (h @ W["Whn"].T)) + W["bn"])
    return (1.0 - z) * n + z * h


def extract_tpm_np(W, u_pool):
    """do()-intervention state-by-node TPM (H_9960 recipe). W: GRU weight dict. u_pool: (M,3)
    W_in-projected held-out embeddings. Returns 24-float tpm[state*3+unit] = P(cell ON next)."""
    u_pool = np.asarray(u_pool, dtype=np.float64)
    tpm = []
    for state in range(1 << N_CELL):
        h_forced = np.array([1.0 if (state >> i) & 1 else -1.0 for i in range(N_CELL)])
        h_forced = np.broadcast_to(h_forced, u_pool.shape)          # (M,3)
        h_next = gru_step_np(W, u_pool, h_forced)                    # (M,3)
        on = (h_next >= 0.0).astype(np.float64).mean(axis=0)        # (3,)
        for i in range(N_CELL):
            tpm.append(float(on[i]))
    return tpm


def project_embeddings_np(W_in, ln_g, ln_b, embs):
    """u = W_in( LayerNorm(e) ). Non-affine LN then a learned 3xd projection. embs: (M,d)."""
    embs = np.asarray(embs, dtype=np.float64)
    mu = embs.mean(axis=1, keepdims=True)
    var = embs.var(axis=1, keepdims=True)
    xn = (embs - mu) / np.sqrt(var + 1e-5)
    if ln_g is not None:
        xn = xn * ln_g + ln_b
    return xn @ np.asarray(W_in, dtype=np.float64).T                 # (M,3)


# ── torch lane (training) — mirrors gru_step_np op-for-op ──
def build_torch_lane(d, seed):
    """Return a RecurrentLane3 nn.Module. Imported lazily so numpy-only hosts can use the extractor."""
    import torch
    import torch.nn as nn

    class RecurrentLane3(nn.Module):
        """3-cell manual GRU. Reads embeddings (B,T,d) -> residual (B,T,d) at the emb_residual site.
        gamma init small so plain CE decides whether to open the channel; W_out no bias (not a pure
        bias channel). Trunk stays parallel: the lane scan is 3-dim ops in a T-loop."""

        def __init__(self, d_model):
            super().__init__()
            g = torch.Generator().manual_seed(seed)
            self.d = int(d_model)
            self.ln = nn.LayerNorm(d_model, elementwise_affine=True)
            self.W_in = nn.Parameter(torch.randn(N_CELL, d_model, generator=g) / math.sqrt(d_model))
            # input-side (u->gate) and recurrent (h->gate) 3x3 matrices + biases
            def m33():
                return nn.Parameter(torch.randn(N_CELL, N_CELL, generator=g) * 0.5)
            self.Wir, self.Whr = m33(), m33()
            self.Wiz, self.Whz = m33(), m33()
            self.Win, self.Whn = m33(), m33()
            self.br = nn.Parameter(torch.zeros(N_CELL))
            self.bz = nn.Parameter(torch.zeros(N_CELL))
            self.bn = nn.Parameter(torch.zeros(N_CELL))
            self.W_out = nn.Parameter(torch.zeros(d_model, N_CELL))   # init 0 -> silent at step 0
            self.gamma = nn.Parameter(torch.tensor(0.01))

        def _step(self, u, h):
            r = torch.sigmoid(u @ self.Wir.T + h @ self.Whr.T + self.br)
            z = torch.sigmoid(u @ self.Wiz.T + h @ self.Whz.T + self.bz)
            n = torch.tanh(u @ self.Win.T + (r * (h @ self.Whn.T)) + self.bn)
            return (1.0 - z) * n + z * h

        def forward(self, e):
            # e: (B,T,d). Causal scan, h0=0 per window (windows are unrelated random slices).
            B, T, d = e.shape
            un = self.ln(e)                                   # (B,T,d)
            u_seq = un @ self.W_in.T                           # (B,T,3)
            h = e.new_zeros(B, N_CELL)
            outs = []
            for t in range(T):
                h = self._step(u_seq[:, t, :], h)             # (B,3)
                outs.append(h)
            H = torch.stack(outs, dim=1)                       # (B,T,3)
            r = self.gamma * (H @ self.W_out.T)                # (B,T,d)
            return r, H

        def weights_np(self):
            def a(p):
                return p.detach().cpu().double().numpy()
            return {
                "W_in": a(self.W_in), "ln_g": a(self.ln.weight), "ln_b": a(self.ln.bias),
                "Wir": a(self.Wir), "Whr": a(self.Whr), "Wiz": a(self.Wiz), "Whz": a(self.Whz),
                "Win": a(self.Win), "Whn": a(self.Whn),
                "br": a(self.br), "bz": a(self.bz), "bn": a(self.bn),
                "W_out": a(self.W_out), "gamma": float(self.gamma.detach()),
            }

    return RecurrentLane3(d)


def gru_dict_from_np(w):
    """Slice a weights_np() dict down to the GRU-step subset extract_tpm_np needs."""
    return {k: w[k] for k in ("Wir", "Whr", "Wiz", "Whz", "Win", "Whn", "br", "bz", "bn")}


def _smoke():
    """$0 numpy self-test: a hand-set dense-recurrent GRU reads Φ>0; a decoupled one reads ~0.
    Certifies the extractor wiring independent of torch (mirrors H_9960's running-net cert)."""
    import importlib
    import os
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    E = importlib.import_module("engine_cli")

    def phi(tpm):
        return sum(E.big_phi_bounded(tpm, 3, s, 3)[0] for s in range(8)) / 8.0

    # a pool of "inputs" that push the gates; here u=0 so the step is pure recurrence h'->f(h)
    u_pool = np.zeros((1, 3))

    # DENSE ROTATION-like recurrent coupling: strong off-diagonal Whn/Whz driving a cycle.
    G = 8.0
    dense = {k: np.zeros((3, 3)) for k in ("Wir", "Whr", "Wiz", "Whz", "Win", "Whn")}
    dense["Whn"] = np.array([[0, 0, G], [G, 0, 0], [0, G, 0]], float)  # n_i <- h_{i-1} (3-cycle)
    dense["Whz"] = np.full((3, 3), -G)                                  # z->0 so h'=n (use candidate)
    for b in ("br", "bz", "bn"):
        dense[b] = np.zeros(3)
    dense["bz"] = np.full(3, -G)                                        # force z~0
    phi_dense = phi(extract_tpm_np(dense, u_pool))

    # DECOUPLED: each cell copies itself, no cross edge -> free cut -> Phi 0
    dec = {k: np.zeros((3, 3)) for k in ("Wir", "Whr", "Wiz", "Whz", "Win", "Whn")}
    dec["Whn"] = np.eye(3) * G
    dec["Whz"] = np.full((3, 3), 0.0)
    for b in ("br", "bz", "bn"):
        dec[b] = np.zeros(3)
    dec["bz"] = np.full(3, -G)
    phi_dec = phi(extract_tpm_np(dec, u_pool))

    print("recurrent_lane _smoke: phi(dense-cycle)=%.4f  phi(decoupled)=%.4f" % (phi_dense, phi_dec))
    ok = phi_dense >= 2.0 and phi_dec <= 1e-6
    print("  extractor sane:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _smoke() else 1)


# ── RCRL .clm trailer (serialize/evaluate) — the lane weights the engine-native readout reads ──
RCRL_MAGIC = bytes([82, 67, 82, 76])   # "RCRL" — chain end after TFLD


def pack_rcrl(w):
    """Pack a weights_np() dict into an RCRL trailer. Layout: MAGIC + <II d n_cell> + tensors f4
    (W_in[3,d] ln_g[d] ln_b[d] Wir/Whr/Wiz/Whz/Win/Whn[3,3] br/bz/bn[3] W_out[d,3] gamma[1])."""
    d = int(np.asarray(w["W_in"]).shape[1])
    out = bytearray()
    out += RCRL_MAGIC
    out += struct.pack("<II", d, N_CELL)
    order = ["W_in", "ln_g", "ln_b", "Wir", "Whr", "Wiz", "Whz", "Win", "Whn",
             "br", "bz", "bn", "W_out"]
    for k in order:
        out += np.asarray(w[k], dtype="<f4").reshape(-1).tobytes()
    out += np.asarray([float(w["gamma"])], dtype="<f4").tobytes()
    return bytes(out)


def read_rcrl(buf, off, d):
    """Read an RCRL trailer at `off`. Returns (weights_dict, new_off) or (None, off) — passthrough-
    safe on absent/short/d-mismatch (same guard idiom as read_tfld)."""
    if off < 0 or off + 4 > len(buf) or buf[off:off + 4] != RCRL_MAGIC:
        return None, off
    p = off + 4
    if p + 8 > len(buf):
        return None, off
    d_file, n_cell = struct.unpack_from("<II", buf, p)
    p += 8
    if int(d_file) != int(d) or int(n_cell) != N_CELL:
        return None, off
    shapes = [("W_in", (N_CELL, d)), ("ln_g", (d,)), ("ln_b", (d,)),
              ("Wir", (N_CELL, N_CELL)), ("Whr", (N_CELL, N_CELL)), ("Wiz", (N_CELL, N_CELL)),
              ("Whz", (N_CELL, N_CELL)), ("Win", (N_CELL, N_CELL)), ("Whn", (N_CELL, N_CELL)),
              ("br", (N_CELL,)), ("bz", (N_CELL,)), ("bn", (N_CELL,)), ("W_out", (d, N_CELL))]
    need = sum(int(np.prod(sh)) for _, sh in shapes) + 1
    if p + need * 4 > len(buf):
        return None, off
    w = {}
    for k, sh in shapes:
        n = int(np.prod(sh))
        w[k] = np.frombuffer(buf, "<f4", n, p).reshape(sh).astype(np.float64).copy()
        p += n * 4
    w["gamma"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    return w, p
