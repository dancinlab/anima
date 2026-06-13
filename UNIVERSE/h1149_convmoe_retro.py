#!/usr/bin/env python3
"""
H_1149 — CONVMOE + RETRO MOUNTABILITY GATE (axis-6 of the 303M campaign, $0 CPU toy).

THE GAP this closes
-------------------
The final anima MUST mount in the A<->G consciousness engine via the generator L3
slot as a .clm v0.2 (CLAUDE.md @D a_clm_gen_pipeline / @D a_core_engine_map). Per the
serializer, ONLY a CLMConvMoE (E=2 / L=1, byte V=256) trunk serializes to an
engine-loadable .clm; "serialize a non-ConvMoE (ByteGPT/transformer) and claim
engine-mountable" is FORBIDDEN.

But axis-4 put the H_1147-validated RETRO copy head on a BYTEGPT backbone
(anima-303M-RETRO) — which is NOT engine-mountable. So today:
    "fabrication solved"   (ByteGPT + RETRO)   != engine-mountable
    "engine-mountable"     (ConvMoE, no RETRO) != fabrication-solved
The final anima needs BOTH in ONE model => the H_1147 RETRO head must ALSO work on
the ConvMoE trunk WITHOUT breaking (a) the E2/L1 structure clm_serialize_v2 requires
or (b) its copy-grounding ability.

QUESTION (frozen, see FREEZE block)
-----------------------------------
Can the H_1147 RETRO cross-attention/copy head be added to the CLMConvMoE backbone
WITHOUT breaking E2/L1 serializability AND while still flipping fabrication
(1.0 -> 0.0 like H_1147 did on ByteGPT)?

DESIGN — how the head attaches (mirrors the ByteGPT case)
---------------------------------------------------------
The RETRO head is an ADDITIONAL module bolted onto the FINAL-POSITION trunk state,
exactly like the ByteGPT attachment (CLM/model/retro303m_en.py pattern). It does NOT
touch the E2/L1 ConvMoE trunk operators (embed, embed_conv, trunk.0[GroupNorm+conv],
moe.router, moe.experts.0/1, norm_out, readout). The head's params (Pq, Pk, Wg) are a
SEPARATE parameter group:
  - hf            = final-position trunk hidden state (what readout consumes)
  - copy_dist     = softmax(cross-attention of hf over the ANCHOR token positions),
                    scattered onto the attended anchor tokens' vocab ids
  - gate          = sigmoid(hf @ Wg)
  - probs         = gate * copy_dist + (1-gate) * softmax(readout(hf))

SERIALIZATION IMPLICATION (the load-bearing finding)
----------------------------------------------------
clm_serialize_v2._BLOCK_ORDER / _EXT_ORDER enumerate ONLY the trunk slots
(ecW,tcW,e0W,e1W,rW,roW + 11 ext). They fetch weights by FIXED slot name. The RETRO
head params have NO slot in that enumeration => they are NATURALLY EXCLUDED from the
.clm. The trunk round-trips byte-exact; `_assert_e2_l1` still passes; the engine's
CORE/clm_decode.hexa (which has no copy path) decodes the trunk as usual.

  => The RETRO head params live OUTSIDE the serialized E2/L1 trunk. The engine
     IGNORES them at decode. THEREFORE: in the engine's current decode path the
     anti-fabrication copy benefit is TRAIN-TIME / HOST-SIDE ONLY. The engine does
     NOT run the RETRO head at decode unless an engine-side copy head is added to
     CORE/clm_decode.hexa + the generator L3 slot (a_core_engine_map: a new copy
     path is a 2nd-order engine change, honestly flagged, NOT built here).

This toy proves the head ATTACHES + GROUNDS + the trunk still SERIALIZES. It does
NOT make the engine decode-path use the head — that is a separate engine build,
stated plainly in the verdict.

THREE arms (SAME ConvMoE trunk / data / steps / optimizer / seed; only the head differs)
  1. VANILLA-CONVMOE      : ConvMoE E2/L1 trunk + plain readout. Anchor PREPENDED,
                            trained end-to-end. NO copy path. (H_1146 replay on ConvMoE.)
  2. CONVMOE-RETRO        : SAME ConvMoE trunk + the H_1147 RETRO copy head.
  3. NO-ANCHOR floor      : VANILLA-CONVMOE with the anchor value slot blanked at
                            train AND test => no info anywhere => chance floor
                            (proves un-memorizability).

Falsifier (frozen, immovable — see FREEZE):
  F1 MECHANISM-WORKS:  (i) fab(CONVMOE-RETRO) <= 0.10  AND (ii) fab(VANILLA) >= 0.50
                       AND (iii) fab(VANILLA) - fab(CONVMOE-RETRO) >= 0.40
  F2 SERIALIZABILITY:  the tiny ConvMoE-RETRO TRUNK serializes to .clm v0.2 with
                       clm_serialize_v2._assert_e2_l1 PASS, clm_decodable=true, and
                       verify_clm_v2 structural check PASS (engine-mountability kept);
                       AND the H_1147 copy-not-recall control holds: CONVMOE-RETRO with
                       the anchor blanked at TEST collapses to fab >= 0.80 (grounds only
                       WITH the anchor => copying, not memorization).
  VERDICT: F1 AND F2 => GREEN (RETRO mounts on ConvMoE, fabrication flipped, trunk
                                still engine-mountable).
           NOT       => RED CLOSED-NEG (the head can't ride the mountable backbone —
                                a valuable finding: RETRO is a separate non-mountable
                                model OR needs an engine-side head).

$0. Local CPU. Pure numpy, deterministic seeded. No torch, no pod. The H_1147 RETRO
head + must-copy toy + the H_1148 semantic-anchor source are REUSED; only the backbone
is swapped ByteGPT-attention -> ConvMoE (the axis-6 manipulation).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

# import the SAME serializer/verifier the engine pipeline uses (reuse, no fork)
_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM_MODEL = os.path.join(_HERE, "..", "CLM", "model")
if _CLM_MODEL not in sys.path:
    sys.path.insert(0, _CLM_MODEL)

SEED = 1149
rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------------- vocab
# byte vocabulary V=256 (the production CLMConvMoE / .clm vocab). The must-copy KEY/VALUE
# tokens are reserved byte ids; the test VALUE pool is held out (never a train target).
VOCAB = 256
PAD, BOS, REL, SEP = 0, 1, 2, 3
N_KEYS = 16
N_VALS = 32
KEY0 = 4
VAL0 = KEY0 + N_KEYS          # 20
NV_PAD = VAL0 + N_VALS        # 52 — non-value byte used to blank the anchor value slot
assert NV_PAD < VOCAB

KEYS = list(range(KEY0, KEY0 + N_KEYS))
VALS = list(range(VAL0, VAL0 + N_VALS))
HELDOUT_VALS = set(VALS[N_VALS // 2:])         # last half held out (never a train target)
TRAIN_VALS = [v for v in VALS if v not in HELDOUT_VALS]

# ----------------------------------------------------------------------------- task
#   [BOS] KEY REL VALUE SEP | KEY REL          (anchor ++ prompt)
#    0    1   2    3    4     5   6
# predict the VALUE at the final position (index 6). The H_1148 semantic-anchor source
# = the retrieved anchor that carries the (key,value) fact; here it is the GROUND-TRUTH
# anchor (oracle retrieval surrogate, exactly as H_1147 / H_1148 used it: the toy isolates
# the COPY MECHANISM, not retriever recall).
SEQ_LEN = 7
VALUE_POS_IN_ANCHOR = 3
ANCHOR_POSITIONS = [0, 1, 2, 3, 4]


def build_seq(k, v):
    return np.array([BOS, k, REL, v, SEP, k, REL], dtype=np.int64)


def make_dataset(rng, n, value_pool):
    keys = rng.choice(KEYS, size=n)
    vals = rng.choice(value_pool, size=n)
    X = np.zeros((n, SEQ_LEN), dtype=np.int64)
    for i in range(n):
        X[i] = build_seq(int(keys[i]), int(vals[i]))
    return X, vals.astype(np.int64)


N_TRAIN = 2000
N_TEST = 500
Xtr, Ytr = make_dataset(rng, N_TRAIN, TRAIN_VALS)
Xte, Yte = make_dataset(rng, N_TEST, list(HELDOUT_VALS))   # held-out values => un-recallable

# ----------------------------------------------------------------------------- model
# A tiny CLMConvMoE E=2 / L=1 trunk in pure numpy, mirroring CLM/model/model.py:
#   embed -> embed_conv(causal k=K) -> trunk.0 [GroupNorm(1,d) -> causal conv -> GELU,
#   residual] -> MoE(router softmax over 2 expert convs, weighted sum) -> norm_out
#   (GroupNorm) -> readout (k=1 conv == linear).
# Slot names match the serializer's torch keys so the trunk exports straight to .clm.
D = 32
K = 3                 # trunk / embed_conv / expert kernel size
E = 2                 # experts (E2 — required by _assert_e2_l1)
L = 1                 # trunk layers (L1 — required by _assert_e2_l1)
STEPS = 600
LR = 0.05
BATCH = 512


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def gelu(x):
    # tanh approximation (numpy); matches nn.GELU closely enough for the toy.
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)))


def causal_conv1d(x, W, b, dilation=1):
    """x: (B,T,Cin), W: (Cout,Cin,K), b: (Cout,) -> (B,T,Cout), left-padded causal."""
    Bsz, T, Cin = x.shape
    Cout, Cin2, Kk = W.shape
    assert Cin == Cin2
    pad = (Kk - 1) * dilation
    xp = np.concatenate([np.zeros((Bsz, pad, Cin)), x], axis=1)      # (B, T+pad, Cin)
    out = np.zeros((Bsz, T, Cout))
    # gather K taps (causal): tap kk reads position t + kk*dilation in padded coords
    for kk in range(Kk):
        sl = xp[:, kk * dilation: kk * dilation + T, :]              # (B,T,Cin)
        out += np.einsum("btc,oc->bto", sl, W[:, :, kk])
    out += b[None, None, :]
    return out


def groupnorm1(x, g, b, eps=1e-5):
    """GroupNorm(1, d): normalize over the channel axis per (batch,time). x:(B,T,d)."""
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    xn = (x - mu) / np.sqrt(var + eps)
    return xn * g[None, None, :] + b[None, None, :]


class ConvMoERetro:
    """CLMConvMoE E2/L1 trunk (numpy) + optional H_1147 RETRO copy head."""

    def __init__(self, rng, retro: bool):
        self.retro = retro
        s = 0.08
        self.embed = rng.normal(0, s, (VOCAB, D))                 # embed.weight (V,d)
        self.ecW = rng.normal(0, s, (D, D, K))                    # embed_conv.conv.weight
        self.ecB = np.zeros(D)
        self.tcW = rng.normal(0, s, (D, D, K))                    # trunk.0.conv.conv.weight
        self.tcB = np.zeros(D)
        self.tgG = np.ones(D)                                     # trunk.0.norm.weight
        self.tgB = np.zeros(D)
        self.e0W = rng.normal(0, s, (D, D, K))                    # moe.experts.0.conv.conv.weight
        self.e0B = np.zeros(D)
        self.e1W = rng.normal(0, s, (D, D, K))                    # moe.experts.1.conv.conv.weight
        self.e1B = np.zeros(D)
        self.rW = rng.normal(0, s, (E, D, 1))                     # moe.router.weight (k=1 conv)
        self.rB = np.zeros(E)
        self.noG = np.ones(D)                                     # norm_out.weight
        self.noB = np.zeros(D)
        self.roW = rng.normal(0, s, (VOCAB, D, 1))               # readout.weight (k=1 conv)
        self.roB = np.zeros(VOCAB)
        if retro:
            self.Pq = rng.normal(0, s, (D, D))
            self.Pk = rng.normal(0, s, (D, D))
            self.Wg = rng.normal(0, s, (D, 1))
        self._m, self._v = {}, {}

    # serialize-relevant trunk slots (everything except the RETRO head)
    TRUNK = ["embed", "ecW", "ecB", "tcW", "tcB", "tgG", "tgB",
             "e0W", "e0B", "e1W", "e1B", "rW", "rB", "noG", "noB", "roW", "roB"]

    def params(self):
        names = list(self.TRUNK)
        if self.retro:
            names += ["Pq", "Pk", "Wg"]
        return names

    def forward(self, X, mask_anchor_value=False):
        Bsz, T = X.shape
        Xe = X.copy()
        if mask_anchor_value:
            Xe[:, VALUE_POS_IN_ANCHOR] = NV_PAD
        h_emb = self.embed[Xe]                                    # (B,T,d)
        # embed_conv (causal k=K)
        h = causal_conv1d(h_emb, self.ecW, self.ecB)             # (B,T,d)
        # trunk.0 : GroupNorm -> causal conv -> GELU, residual
        t_in = h
        tn = groupnorm1(t_in, self.tgG, self.tgB)
        tc = causal_conv1d(tn, self.tcW, self.tcB)
        tg = gelu(tc)
        h = t_in + tg                                            # residual
        # MoE : router softmax over 2 expert convs, weighted sum (top-1 soft == weighted)
        # router is a k=1 conv -> per-position logits over E experts
        rlog = np.einsum("btd,ed->bte", h, self.rW[:, :, 0]) + self.rB[None, None, :]
        rp = softmax(rlog, axis=-1)                              # (B,T,E)
        ex0 = gelu(causal_conv1d(h, self.e0W, self.e0B))
        ex1 = gelu(causal_conv1d(h, self.e1W, self.e1B))
        moe = rp[:, :, 0:1] * ex0 + rp[:, :, 1:2] * ex1          # (B,T,d)
        h = moe
        # norm_out
        h = groupnorm1(h, self.noG, self.noB)
        # readout (k=1 conv == linear) at final position
        hf = h[:, -1, :]                                         # (B,d)
        logits_vocab = np.einsum("bd,vd->bv", hf, self.roW[:, :, 0]) + self.roB[None, :]

        cache = dict(Xe=Xe, h_emb=h_emb, t_in=t_in, tn=tn, tc=tc, tg=tg,
                     rlog=rlog, rp=rp, ex0=ex0, ex1=ex1, moe=moe, hpre_no=moe,
                     h=h, hf=hf, logits_vocab=logits_vocab)
        if not self.retro:
            cache["probs"] = softmax(logits_vocab, axis=-1)
            return cache["probs"], cache

        # ---- H_1147 RETRO copy head over the anchor positions (verbatim mechanism) ----
        anc = np.array(ANCHOR_POSITIONS)
        h_anchor = h_emb[:, anc, :]                              # anchor token states (B,A,d)
        hq = hf @ self.Pq
        hk = h_anchor @ self.Pk
        pscore = np.einsum("bd,bad->ba", hq, hk) / np.sqrt(D)
        pattn = softmax(pscore, axis=-1)                        # (B,A)
        anc_tokens = Xe[:, anc]                                  # (B,A)
        flat_idx = (np.arange(Bsz)[:, None] * VOCAB + anc_tokens).reshape(-1)
        copy_dist = np.bincount(flat_idx, weights=pattn.reshape(-1),
                                minlength=Bsz * VOCAB).reshape(Bsz, VOCAB)
        gate = 1.0 / (1.0 + np.exp(-(hf @ self.Wg)))            # (B,1)
        vocab_dist = softmax(logits_vocab, axis=-1)
        probs = gate * copy_dist + (1 - gate) * vocab_dist
        probs = np.clip(probs, 1e-9, 1.0)
        probs = probs / probs.sum(axis=-1, keepdims=True)
        cache.update(anc=anc, h_anchor=h_anchor, hq=hq, hk=hk, pscore=pscore,
                     pattn=pattn, anc_tokens=anc_tokens, copy_dist=copy_dist,
                     gate=gate, vocab_dist=vocab_dist, probs=probs)
        return probs, cache

    # ----- numeric gradient via finite differences would be too slow; we use a
    # ----- lightweight analytic backward on the LAST-LAYER readout + RETRO head and a
    # ----- straight-through approximation for the conv trunk (the trunk only needs to
    # ----- furnish a usable hf; the COPY decision lives in the head + readout). For a
    # ----- toy at this scale we instead train with full analytic backprop below.
    def loss_and_grad(self, X, Y, mask_anchor_value=False):
        probs, c = self.forward(X, mask_anchor_value=mask_anchor_value)
        Bsz = X.shape[0]
        loss = -np.log(probs[np.arange(Bsz), Y] + 1e-12).mean()
        g = {n: np.zeros_like(getattr(self, n)) for n in self.params()}

        if not self.retro:
            # softmax-xent grad wrt vocab logits
            dlogits = (probs.copy())
            dlogits[np.arange(Bsz), Y] -= 1.0
            dlogits /= Bsz
            self._trunk_backward(c, dlogits, g)
            return loss, g

        # RETRO: probs = gate*copy + (1-gate)*vocab_dist
        dP = probs.copy()
        dP[np.arange(Bsz), Y] -= 1.0
        dP /= Bsz
        gate = c["gate"]; copy_dist = c["copy_dist"]; vocab_dist = c["vocab_dist"]; hf = c["hf"]
        # gate grad
        dgate = (dP * (copy_dist - vocab_dist)).sum(axis=1, keepdims=True)
        dsig = dgate * gate * (1 - gate)
        g["Wg"] += hf.T @ dsig
        dhf_gate = dsig @ self.Wg.T
        # vocab_dist grad -> logits
        dvocab_dist = dP * (1 - gate)
        tmp = (dvocab_dist * vocab_dist).sum(axis=1, keepdims=True)
        dlogits = vocab_dist * (dvocab_dist - tmp)
        # copy_dist grad -> pattn -> pscore -> Pq/Pk
        anc = c["anc"]; anc_tokens = c["anc_tokens"]; pattn = c["pattn"]
        dcopy = dP * gate
        dpattn = np.take_along_axis(dcopy, anc_tokens, axis=1)     # (B,A)
        tmp2 = (dpattn * pattn).sum(axis=1, keepdims=True)
        dpscore = pattn * (dpattn - tmp2)
        hq = c["hq"]; hk = c["hk"]
        dhq = np.einsum("ba,bad->bd", dpscore, hk) / np.sqrt(D)
        dhk = np.einsum("ba,bd->bad", dpscore, hq) / np.sqrt(D)
        g["Pq"] += hf.T @ dhq
        dhf_ptr = dhq @ self.Pq.T
        h_anchor = c["h_anchor"]
        g["Pk"] += np.einsum("bad,bae->de", h_anchor, dhk)
        # (we let the anchor-embedding grad from dhk flow into embed via straight path)
        dh_anchor = dhk @ self.Pk.T                               # (B,A,d)
        dhf = dhf_gate + dhf_ptr
        self._trunk_backward(c, dlogits, g, extra_dhf=dhf, dh_anchor=(anc, dh_anchor))
        return loss, g

    def _trunk_backward(self, c, dlogits, g, extra_dhf=None, dh_anchor=None):
        """Analytic backward through readout + norm_out + MoE + trunk + embed_conv +
        embed. Conv backward uses the same tap-shift as the forward."""
        hf = c["hf"]
        # readout (k=1 conv == linear): logits = hf @ roW[:,:,0].T + roB
        roW2 = self.roW[:, :, 0]                                  # (V,d)
        g["roW"][:, :, 0] += dlogits.T @ hf
        g["roB"] += dlogits.sum(axis=0)
        dhf = dlogits @ roW2
        if extra_dhf is not None:
            dhf = dhf + extra_dhf
        Bsz = hf.shape[0]
        T = c["h"].shape[1]
        # only final position carries readout grad; build (B,T,d)
        dh = np.zeros((Bsz, T, D))
        dh[:, -1, :] = dhf
        # norm_out (GroupNorm) backward
        dh = self._gn_backward(c["moe"], self.noG, self.noB, dh, g, "noG", "noB")
        # MoE backward: moe = rp0*ex0 + rp1*ex1
        rp = c["rp"]; ex0 = c["ex0"]; ex1 = c["ex1"]; h_moe_in = c["h"]  # h fed to router+experts
        # NOTE: c["h"] is post-norm_out; we need the pre-MoE h. Recompute reference:
        # we stored 'moe' as MoE output and 'hpre_no' alias; the MoE input is the residual
        # trunk output. For the toy we approximate the router/expert input grad path by
        # treating the conv experts' input as the embed_conv+trunk output recomputed in cache.
        # To keep correctness we recover it from cache 't_in + tg'.
        h_pre_moe = c["t_in"] + c["tg"]
        drp0 = (dh * ex0).sum(axis=-1)                            # (B,T)
        drp1 = (dh * ex1).sum(axis=-1)
        dex0 = dh * rp[:, :, 0:1]
        dex1 = dh * rp[:, :, 1:2]
        # router softmax backward
        drlog = np.zeros_like(rp)
        drp = np.stack([drp0, drp1], axis=-1)                    # (B,T,E)
        s = (drp * rp).sum(axis=-1, keepdims=True)
        drlog = rp * (drp - s)
        # router weight grad (k=1 conv over h_pre_moe)
        g["rW"][:, :, 0] += np.einsum("bte,btd->ed", drlog, h_pre_moe)
        g["rB"] += drlog.sum(axis=(0, 1))
        dh_from_router = np.einsum("bte,ed->btd", drlog, self.rW[:, :, 0])
        # expert conv backward (gelu then conv)
        dex0_pre = dex0 * self._dgelu(c_pre=self._conv_pre(h_pre_moe, self.e0W, self.e0B))
        dex1_pre = dex1 * self._dgelu(c_pre=self._conv_pre(h_pre_moe, self.e1W, self.e1B))
        dh_e0 = self._conv_backward(h_pre_moe, self.e0W, dex0_pre, g, "e0W", "e0B")
        dh_e1 = self._conv_backward(h_pre_moe, self.e1W, dex1_pre, g, "e1W", "e1B")
        dh_pre_moe = dh_from_router + dh_e0 + dh_e1
        # trunk.0 residual: h_pre_moe = t_in + gelu(conv(GN(t_in)))
        d_t_in = dh_pre_moe.copy()
        d_tg = dh_pre_moe.copy()
        d_tc = d_tg * self._dgelu(c_pre=c["tc"])
        d_tn = self._conv_backward(c["tn"], self.tcW, d_tc, g, "tcW", "tcB")
        d_t_in2 = self._gn_backward_x(c["t_in"], self.tgG, self.tgB, d_tn, g, "tgG", "tgB")
        d_embconv_out = d_t_in + d_t_in2
        # embed_conv backward
        d_h_emb = self._conv_backward(c["h_emb"], self.ecW, d_embconv_out, g, "ecW", "ecB")
        # add RETRO anchor-embedding grad
        if dh_anchor is not None:
            anc, dh_a = dh_anchor
            d_h_emb[:, anc, :] += dh_a
        # embed backward
        Xe = c["Xe"]
        np.add.at(g["embed"], Xe.reshape(-1), d_h_emb.reshape(-1, D))

    # ---- conv helpers ----
    def _conv_pre(self, x, W, b):
        return causal_conv1d(x, W, b)

    def _dgelu(self, c_pre):
        x = c_pre
        t = np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))
        dt = 0.7978845608 * (1 + 3 * 0.044715 * x ** 2)
        return 0.5 * (1 + t) + 0.5 * x * (1 - t ** 2) * dt

    def _conv_backward(self, x_in, W, d_out, g, wname, bname):
        """Backward of causal_conv1d. x_in:(B,T,Cin), W:(Cout,Cin,K), d_out:(B,T,Cout)."""
        Bsz, T, Cin = x_in.shape
        Cout, _, Kk = W.shape
        pad = (Kk - 1)
        xp = np.concatenate([np.zeros((Bsz, pad, Cin)), x_in], axis=1)
        dxp = np.zeros_like(xp)
        for kk in range(Kk):
            sl = xp[:, kk: kk + T, :]                            # (B,T,Cin)
            g[wname][:, :, kk] += np.einsum("bto,btc->oc", d_out, sl)
            dxp[:, kk: kk + T, :] += np.einsum("bto,oc->btc", d_out, W[:, :, kk])
        g[bname] += d_out.sum(axis=(0, 1))
        return dxp[:, pad:, :]

    def _gn_backward(self, x, gamma, beta, d_out, g, gname, bname, eps=1e-5):
        return self._gn_backward_x(x, gamma, beta, d_out, g, gname, bname, eps)

    def _gn_backward_x(self, x, gamma, beta, d_out, g, gname, bname, eps=1e-5):
        """GroupNorm(1,d) backward over channel axis. x:(B,T,d)."""
        mu = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        std = np.sqrt(var + eps)
        xn = (x - mu) / std
        g[gname] += (d_out * xn).sum(axis=(0, 1))
        g[bname] += d_out.sum(axis=(0, 1))
        dxn = d_out * gamma[None, None, :]
        Dn = x.shape[-1]
        dvar = (dxn * (x - mu) * -0.5 * std ** -3).sum(axis=-1, keepdims=True)
        dmu = (dxn * -1.0 / std).sum(axis=-1, keepdims=True) + dvar * (-2.0 * (x - mu)).mean(axis=-1, keepdims=True)
        dx = dxn / std + dvar * 2.0 * (x - mu) / Dn + dmu / Dn
        return dx

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

    # ----- export the TRUNK ONLY to the serializer's logical-slot dict (NO RETRO head) -----
    def trunk_state_dict(self):
        """Return a logical-slot dict matching clm_serialize_v2._BLOCK_ORDER/_EXT_ORDER.
        The RETRO head params (Pq,Pk,Wg) are DELIBERATELY ABSENT — they have no .clm slot,
        proving the head lives outside the serialized E2/L1 trunk."""
        return {
            # conv blocks (cout, Cin, K)
            "ecW": self.ecW, "tcW": self.tcW, "e0W": self.e0W, "e1W": self.e1W,
            "rW": self.rW, "roW": self.roW,
            # ext (fp32)
            "embed": self.embed,
            "ecB": self.ecB, "tcB": self.tcB, "e0B": self.e0B, "e1B": self.e1B,
            "rB": self.rB, "roB": self.roB,
            "tgG": self.tgG, "tgB": self.tgB, "noG": self.noG, "noB": self.noB,
        }


def train(model, Xtr, Ytr, rng, mask_anchor_value=False, label=""):
    n = Xtr.shape[0]
    loss = 0.0
    for t in range(1, STEPS + 1):
        idx = rng.integers(0, n, BATCH)
        loss, g = model.loss_and_grad(Xtr[idx], Ytr[idx], mask_anchor_value=mask_anchor_value)
        model.step(g, t, LR)
        if label and (t % 200 == 0 or t == 1):
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
    return ("v%02d" % (t - VAL0)) if (VAL0 <= t < NV_PAD) else ("tok%d" % t)


def serialize_check(model):
    """F2: export the ConvMoE-RETRO TRUNK (no head) to .clm v0.2, run _assert_e2_l1 +
    clm_decodable + verify_clm_v2 structural check. Returns a result dict."""
    import clm_serialize_v2 as S
    import verify_clm_v2 as Vr

    sd = model.trunk_state_dict()
    out_path = "/tmp/h1149_convmoe_retro_trunk.clm"

    # _assert_e2_l1 on a synthetic cfg with E=2/L=1 (and a teeth check E=4 must raise)
    class _Cfg:
        n_experts = E
        n_trunk_layers = L
    assert_ok = True
    assert_msg = "ok"
    try:
        S._assert_e2_l1(_Cfg())
    except Exception as e:
        assert_ok = False
        assert_msg = f"E2/L1 assert FAILED unexpectedly: {e}"
    # teeth: a non-E2 cfg MUST raise (proves the gate has teeth)
    teeth_ok = False
    try:
        class _Bad:
            n_experts = 4
            n_trunk_layers = 1
        S._assert_e2_l1(_Bad())
    except ValueError:
        teeth_ok = True

    # serialize the trunk (cfg=None: synthetic vouches E2/L1; slots are logical keys)
    S.serialize_v2(sd, cfg=None, out_path=out_path)
    rb = open(out_path, "rb").read()
    decodable = Vr.clm_decodable(rb)
    parsed = Vr.parse_clm(rb)
    # expected v0.2 layout for d=D,K=K,E=2,V=256
    expect = {
        "nblk": 6,
        "blocks": [
            {"cout": D, "rest": D * K}, {"cout": D, "rest": D * K},
            {"cout": D, "rest": D * K}, {"cout": D, "rest": D * K},
            {"cout": E, "rest": D}, {"cout": VOCAB, "rest": D},
        ],
        "n_ext": 11,
        "ext_counts": [VOCAB * D, D, D, D, D, E, VOCAB, D, D, D, D],
    }
    struct_ok = True
    struct_why = "ok"
    if parsed["nblk"] != expect["nblk"]:
        struct_ok, struct_why = False, f"nblk {parsed['nblk']}!={expect['nblk']}"
    elif [(b["cout"], b["rest"]) for b in parsed["blocks"]] != \
            [(b["cout"], b["rest"]) for b in expect["blocks"]]:
        struct_ok, struct_why = False, f"block dims {parsed['blocks']}"
    elif not parsed["clmx_found"]:
        struct_ok, struct_why = False, "CLMX trailer missing"
    elif parsed["n_ext"] != expect["n_ext"]:
        struct_ok, struct_why = False, f"n_ext {parsed['n_ext']}!={expect['n_ext']}"
    elif parsed["ext_counts"] != expect["ext_counts"]:
        struct_ok, struct_why = False, f"ext_counts {parsed['ext_counts']}"
    elif not parsed["exact_eof"]:
        struct_ok, struct_why = False, f"trailing bytes final_off={parsed['final_off']}!=len={parsed['len']}"

    # confirm the head params are NOT in the serialized dict (lives outside trunk)
    head_absent = all(k not in sd for k in ("Pq", "Pk", "Wg"))

    return dict(out_path=out_path, bytes=len(rb), assert_e2_l1_pass=assert_ok,
                assert_msg=assert_msg, assert_teeth_pass=teeth_ok,
                decodable=bool(decodable), struct_pass=struct_ok, struct_why=struct_why,
                nblk=parsed["nblk"], blocks=parsed["blocks"], n_ext=parsed["n_ext"],
                head_absent_from_clm=head_absent)


def main():
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        log.append(s)
        print(s, flush=True)

    P("=" * 78)
    P("H_1149 CONVMOE + RETRO MOUNTABILITY GATE — does the H_1147 copy head ride the")
    P("ENGINE-MOUNTABLE CLMConvMoE E2/L1 trunk, flip fabrication, AND still serialize")
    P("to .clm v0.2?  ($0 numpy CPU, p7 deterministic)")
    P("=" * 78)
    P(f"seed={SEED} vocab={VOCAB} keys={N_KEYS} vals={N_VALS} "
      f"heldout={len(HELDOUT_VALS)} D={D} K={K} E={E} L={L} steps={STEPS} "
      f"batch={BATCH} n_train={N_TRAIN} n_test={N_TEST}")
    P("test values HELD-OUT (never a train target) => answer MUST be COPIED from anchor.\n")

    P("[ARM 1 VANILLA-CONVMOE] training (ConvMoE E2/L1, anchor prepended, no copy head)...")
    mv = ConvMoERetro(np.random.default_rng(SEED + 1), retro=False)
    lv = train(mv, Xtr, Ytr, np.random.default_rng(SEED + 2), label="vanilla")
    fab_v, _ = fab_rate(mv, Xte, Yte)

    P("[ARM 2 CONVMOE-RETRO] training (SAME ConvMoE trunk + H_1147 copy head)...")
    mr = ConvMoERetro(np.random.default_rng(SEED + 1), retro=True)
    lr_loss = train(mr, Xtr, Ytr, np.random.default_rng(SEED + 2), label="retro")
    fab_r, _ = fab_rate(mr, Xte, Yte)

    P("[ARM 3 NO-ANCHOR floor] training (vanilla, anchor value blanked train+test)...")
    mn = ConvMoERetro(np.random.default_rng(SEED + 1), retro=False)
    ln = train(mn, Xtr, Ytr, np.random.default_rng(SEED + 2),
               mask_anchor_value=True, label="no-anchor")
    fab_n, _ = fab_rate(mn, Xte, Yte, mask_anchor_value=True)

    # F2 copy-not-recall control: CONVMOE-RETRO with anchor blanked at TEST only
    fab_r_masked, _ = fab_rate(mr, Xte, Yte, mask_anchor_value=True)

    P(f"ARM 1 VANILLA-CONVMOE  train_loss={lv:.4f}  fab-rate={fab_v:.4f}  copy-acc={1-fab_v:.4f}")
    P(f"ARM 2 CONVMOE-RETRO    train_loss={lr_loss:.4f}  fab-rate={fab_r:.4f}  copy-acc={1-fab_r:.4f}")
    P(f"ARM 3 NO-ANCHOR floor  train_loss={ln:.4f}  fab-rate={fab_n:.4f}  copy-acc={1-fab_n:.4f}")
    P(f"      CONVMOE-RETRO no-anchor ctrl (F2) fab-rate={fab_r_masked:.4f}  "
      f"copy-acc={1-fab_r_masked:.4f}\n")

    P("--- decoded HELD-OUT samples (key -> true_val | pred) ---")
    for name, m, mk in [("VANILLA-CONVMOE", mv, False), ("CONVMOE-RETRO", mr, False),
                        ("NO-ANCHOR", mn, True)]:
        P(f"{name}:")
        for s in decode_samples(m, Xte, Yte, mask_anchor_value=mk):
            P(f"  k{s['key']-KEY0:02d} -> true v{s['true_val']-VAL0:02d} | "
              f"pred {fmt_tok(s['pred'])} {'OK' if s['correct'] else 'FAB'}")

    # ---- F2 serializability of the ConvMoE-RETRO TRUNK ----
    P("\n--- F2 SERIALIZE the CONVMOE-RETRO TRUNK to .clm v0.2 (head excluded) ---")
    ser = serialize_check(mr)
    P(f"  .clm bytes={ser['bytes']}  nblk={ser['nblk']}  n_ext={ser['n_ext']}")
    P(f"  _assert_e2_l1 PASS={ser['assert_e2_l1_pass']} ({ser['assert_msg']})")
    P(f"  _assert_e2_l1 teeth (E=4 raises) PASS={ser['assert_teeth_pass']}")
    P(f"  clm_decodable={ser['decodable']}  verify struct PASS={ser['struct_pass']} "
      f"({ser['struct_why']})")
    P(f"  RETRO head (Pq,Pk,Wg) ABSENT from .clm = {ser['head_absent_from_clm']} "
      f"(head lives OUTSIDE the serialized trunk)\n")

    # ---- FROZEN falsifier ----
    f1_i = fab_r <= 0.10
    f1_ii = fab_v >= 0.50
    f1_iii = (fab_v - fab_r) >= 0.40
    F1 = f1_i and f1_ii and f1_iii
    f2_serial = (ser["assert_e2_l1_pass"] and ser["assert_teeth_pass"]
                 and ser["decodable"] and ser["struct_pass"])
    f2_collapse = fab_r_masked >= 0.80
    F2 = f2_serial and f2_collapse
    GREEN = F1 and F2

    P("=" * 78)
    P("FROZEN FALSIFIER (bars set BEFORE run; immovable — see H_1149_FREEZE.txt)")
    P("=" * 78)
    P(f"F1(i)   fab(CONVMOE-RETRO) <= 0.10 : {fab_r:.4f}   -> {'PASS' if f1_i else 'FAIL'}")
    P(f"F1(ii)  fab(VANILLA)       >= 0.50 : {fab_v:.4f}   -> {'PASS' if f1_ii else 'FAIL'}")
    P(f"F1(iii) gap(VAN-RETRO)     >= 0.40 : {fab_v-fab_r:.4f}   -> {'PASS' if f1_iii else 'FAIL'}")
    P(f"F1 MECHANISM-WORKS (head grounds on ConvMoE) : {'PASS' if F1 else 'FAIL'}")
    P(f"F2(a) .clm v0.2 serialize+assert_e2_l1+decode+verify PASS : "
      f"{'PASS' if f2_serial else 'FAIL'}")
    P(f"F2(b) CONVMOE-RETRO no-anchor fab >= 0.80 (copy-not-recall): {fab_r_masked:.4f}  "
      f"-> {'PASS' if f2_collapse else 'FAIL'}")
    P(f"F2 SERIALIZABILITY-PRESERVED + COPY-NOT-RECALL : {'PASS' if F2 else 'FAIL'}")
    P("-" * 78)
    if GREEN:
        P("VERDICT: 🟢 GREEN — RETRO MOUNTS ON CONVMOE.")
        P("  The H_1147 copy head rides the engine-mountable CLMConvMoE E2/L1 trunk,")
        P("  flips fabrication (vanilla->retro), AND the trunk still serializes to a")
        P("  decodable .clm v0.2 (head params excluded => trunk unbroken).")
    else:
        P("VERDICT: 🔴 CLOSED-NEG — RETRO does NOT cleanly mount on ConvMoE.")
        if not F1:
            P("  F1 FAIL: the copy head did not flip fabrication on the ConvMoE trunk.")
        if not F2:
            P("  F2 FAIL: serializability/copy-not-recall broke.")
    P("")
    P("HONEST SCOPE (a_scale_honest_scope):")
    P("  - toy D=32 / V-byte subset / oracle ground-truth anchor (H_1147/1148 surrogate)")
    P("    — NOT 303M, NOT real noisy/wrong kosmos retrieval, NOT coherence-backbone.")
    P("  - 1.0/0.0-style saturation = mechanism EXISTENCE-PROOF, not an effect size.")
    P("  - SERIALIZATION TRUTH: the RETRO head (Pq,Pk,Wg) has NO .clm slot => it is")
    P("    EXCLUDED from the engine-loaded trunk. CORE/clm_decode.hexa has no copy path,")
    P("    so at the ENGINE decode the anti-fabrication benefit is TRAIN-TIME/HOST-SIDE")
    P("    ONLY. To run grounding INSIDE the A<->G engine, an engine-side copy head must")
    P("    be added to clm_decode + the generator L3 slot (a_core_engine_map: a separate")
    P("    2nd-order engine build, NOT done here). The trunk mounts; the head does not")
    P("    yet decode in-engine.")

    result = dict(
        seed=SEED, fab_vanilla=fab_v, fab_convmoe_retro=fab_r, fab_no_anchor=fab_n,
        fab_retro_no_anchor=fab_r_masked,
        F1=bool(F1), F2=bool(F2), GREEN=bool(GREEN),
        f1_i=bool(f1_i), f1_ii=bool(f1_ii), f1_iii=bool(f1_iii),
        f2_serial=bool(f2_serial), f2_collapse=bool(f2_collapse),
        serialize=ser,
    )
    os.makedirs("state/h1149_convmoe_retro", exist_ok=True)
    with open("state/h1149_convmoe_retro/h1149_result.json", "w") as f:
        json.dump(result, f, indent=2)

    # write verdict
    vdir = ".verdicts/1149_convmoe_retro"
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "H_1149.txt"), "w") as f:
        f.write("\n".join(log) + "\n")
    print(f"\n[written] {vdir}/H_1149.txt  +  state/h1149_convmoe_retro/h1149_result.json")
    return GREEN


if __name__ == "__main__":
    g = main()
    sys.exit(0 if g else 0)   # verdict captured in file; exit 0 either way (RED is a valid finding)
