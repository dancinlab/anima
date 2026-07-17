"""core/clms.py — H_9423 CLMS store-bridge trailer lane, CORE-owned SSOT.

The ρ·weave recombination wall (was G1) is the ABSENCE of an operator<->declaration-store runtime
lookup bridge (H_9359): the FACT can live in a store and the OPERATOR in the text, yet a frozen conv
byte-LM has no port to bind them (bolt-on died 3-port, H_9392). anima-v2 DIRECTIONAL-proved that a
CO-TRAINED bridge learns the lookup (V2_6 held-out macro 0.987/0.992). CLMS ports that co-trained
bridge onto the parent conv trunk as a trailer lane: at the answer position it forms a query from the
trunk penultimate, looks up an 8-slot content-addressed store (keys = a FROZEN per-byte embedding of
the entity name → generalizes to held-out entities), reads the polarity value, and fuses it with the
operator through a GELU-MLP — the nonlinearity the parent's linear 1x1-conv readout cannot supply on
its own (v2's XOR wall). The answer-position logits row is OVERWRITTEN with λ·store_logits (store_only
gate), so the trunk logit can never receive answer-position gradient = ② shortcut-cut is structural.

DISJOINT (a_substrate_disjoint): the store content is RUNTIME-injected (train: block store manifest;
eval: `--store` manifest via set_clms_store), never serialized into the .clm — only the learned bridge
weights {W_q, val, W_h, b_h, W_out, λ} + the frozen key_emb table live in the trailer. Absent trailer
OR un-injected store <=> byte-identical to today's .clm (loaders passthrough on short/absent read;
forward passthrough when _CLMS_STORE is None). This is the H_9392 boundary made literal: "does the
fusion parameter live inside the .clm and enter the forward pass" — yes (co-trained), vs --store-mix
(post-forward posterior arithmetic actuator).

CORE-owned, ONE file (mirrors core/slw.py, core/clml.py): store_apply + find_qpos (torch-free numpy
inference mirror, byte-parity target for core/decode.hexa) · pack_clms/read_clms ("CLMS" trailer codec)
· CLMSModule (torch training module, DIRECTIONAL, defined only when torch importable so inference stays
torch-free). Store is injected via set_clms_store (mirrors slw.set_slw_controls) — trailer present +
store None = passthrough (the C0-f "trailer有 store無 = byte-identical" seal).
"""

from __future__ import annotations

import struct
import numpy as np

# ── "CLMS" trailer magic (mirrors the CLMB/SLW/CLML trailer convention) ─────────
CLMS_MAGIC = bytes([67, 76, 77, 83])   # "CLMS"


def _softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def _gelu(x):
    # tanh approximation — MUST match CLMSModule's F.gelu(approximate="tanh") for 2-production parity
    # (constants byte-identical to core/clml._gelu).
    return 0.5 * x * (1.0 + np.tanh(0.7978845608028654 * (x + 0.044715 * x**3)))


# --------------------------------------------------------------------------- #
# (a) numpy inference mirror — torch-free, byte-parity target for core/decode.hexa
# --------------------------------------------------------------------------- #
def find_qpos(tok):
    """Answer positions in a decode window. Returns the list of t where tok[t-2:t+1] == "=> "
    (bytes 61,62,32): logits[t] predicts the FIRST answer byte, so t is both the query-formation
    position and the row CLMS overwrites (a causal LM aligns logits[t] with tok[t+1]). Pure function
    of the window bytes (no side channel) — the same scanner the trainer reuses. Usually 0–1 hits for
    a T=24 window over ≤23-byte lines; t == T-1 (last row) is valid (its argmax is the first answer
    byte at generation)."""
    t_list = []
    for t in range(2, len(tok)):
        if int(tok[t]) == 32 and int(tok[t - 1]) == 62 and int(tok[t - 2]) == 61:
            t_list.append(t)
    return t_list


def _entity_key(key_emb, entity):
    """Content address for an entity name = mean of the frozen per-byte embedding rows. Generalizes to
    held-out entities (a new key built from seen bytes). key_emb is (256, d_k)."""
    ids = np.frombuffer(entity.encode("ascii"), dtype=np.uint8)
    return key_emb[ids].mean(axis=0)


def store_apply(logits, yn, clms, store, qpos, oracle=False, lam_override=None, audit=None):
    """CLMS store-bridge lane: OVERWRITE the answer-position logits row with λ·store_logits.

    logits : (T, V) float — readout(+CLML) logits. The caller's array is NOT mutated (internal copy).
    yn     : (T, d) float — pre-slot trunk penultimate (= _fwd_trunk output = yn_trunk, the SAME tap
             CLML reads; NOT the SLW-modified penultimate).
    clms   : dict from read_clms (key_emb, W_q, val, W_h, b_h, W_out, lam, n_slot, d_k, d_s, r).
    store  : {"entities": [str]*n_slot, "pols": [int in {0,1}]*n_slot, "target_slot": int|None}.
             target_slot is used only when oracle=True.
    qpos   : list of int from find_qpos(tok).
    oracle : True => bypass the softmax lookup, a = one_hot(target_slot) (C0-e positive control:
             hands the lookup for free, so ORACLE<0.90 = the value/MLP/λ/serialization plumbing is
             dead, independent of whether addressing can be learned — read no negative before it passes).
    lam_override : None = file λ · 0.0 = λ0 control (C2, byte-identical passthrough) · 1.0 = store_only.

    Passthrough (returns logits unchanged): clms None · lane_type==0 · store None · qpos empty · λ==0.
    Op order is IDENTICAL to CLMSModule.forward (2-production parity)."""
    if clms is None or int(clms.get("lane_type", 0)) == 0 or store is None or not qpos:
        return logits
    lam = float(clms["lam"]) if lam_override is None else float(lam_override)
    if lam == 0.0:
        return logits
    dt = logits.dtype
    n_slot = int(clms["n_slot"])
    key_emb = clms["key_emb"]
    ents = store["entities"]
    pols = np.asarray(store["pols"], dtype=np.int64)
    K = np.stack([_entity_key(key_emb, ents[i]) for i in range(n_slot)])   # (n_slot, d_k)
    V_slots = clms["val"][pols]                                            # (n_slot, d_s)
    scale = 1.0 / np.sqrt(float(clms["d_k"]))
    out = logits.copy()
    lane_type = int(clms.get("lane_type", 1))
    for t in qpos:
        h = yn[t]                                                          # (d,)
        q = h @ clms["W_q"]                                               # (d_k,) [row-vector conv, CLML-form]
        if oracle:
            a = np.zeros(n_slot, dtype=q.dtype)
            a[int(store["target_slot"])] = 1.0                            # softmax bypassed (address free)
        else:
            a = _softmax(q @ K.T * scale)                                # (n_slot,) content-address lookup
        if audit is not None:                                            # H_9672 addr-audit (None=byte-identical)
            ts = store.get("target_slot")
            audit.append({"argmax": int(np.argmax(a)),
                          "a_target": float(a[int(ts)]) if ts is not None else -1.0,
                          "target": int(ts) if ts is not None else -1})
        if lane_type == 3:                                                # RV-3 majority-null centering (H_9710)
            a = a - (1.0 / n_slot)                                        # v≡0 at uniform a → shortcut basin gone
        v = a @ V_slots                                                   # (d_s,) = Σ (aᵢ−c)·val[polᵢ]
        if lane_type in (2, 3):
            g = h @ clms["W_g"]                                           # (d_g,) op-gate bottleneck (H_9423)
            z = _gelu(np.concatenate([v, g]) @ clms["W_h"] + clms["b_h"]) # (r,) [v; g] fusion (v un-diluted)
        else:                                                             # lane_type 1 legacy: [v; h] fusion
            z = _gelu(np.concatenate([v, h]) @ clms["W_h"] + clms["b_h"]) # (r,) — S1/S2 artifacts, no silent recast
        s = z @ clms["W_out"]                                             # (V,)
        out[t] = (lam * s).astype(dt)                                     # ★ overwrite = store_only gate
    return out


# --------------------------------------------------------------------------- #
# (b) "CLMS" trailer codec — write (serialize) + read (loaders) · LE f32
#   header: CLMS magic · lane_type u8 · n_slot u32 · d_k u32 · d_s u32 · r u32 · key_seed u32
#   arrays (row-major): key_emb[256·d_k] W_q[d·d_k] val[2·d_s] W_h[(d_s+d)·r] b_h[r] W_out[r·V] lam[1]
#   (d, V come from the model — read_clms(buf, off, d, V) — as in read_clml. key_emb's first axis 256
#    is the fixed byte alphabet, V-independent. key_seed is PROVENANCE ONLY — the reader never
#    regenerates the table, it reads the stored bytes: a seed-regenerated table is the quietest
#    instrument-death vector, train-pod vs eval-host generation drift degrades the lookup silently
#    and a single-host determinism gate can't catch it. 64KB is 0.02% of a 303M .clm — store it.)
# --------------------------------------------------------------------------- #
_ARR_ORDER = ("key_emb", "W_q", "val", "W_h", "b_h", "W_out", "lam")               # lane_type 1 (legacy)
_ARR_ORDER_V2 = ("key_emb", "W_q", "W_g", "val", "W_h", "b_h", "W_out", "lam")     # lane_type 2 (H_9423 W_g)
_KEY_ALPHABET = 256


def pack_clms(w: dict) -> bytes:
    """Pack a CLMS weight dict into appended trailer bytes. Absent trailer <=> byte-identical model, so
    a writer only calls this when the model actually has a CLMS lane. lane_type 2 (H_9423, default for a
    trained torch module) inserts d_g into the header (<BIIIIII) and W_g after W_q; lane_type 1 (legacy
    S1/S2 artifacts) keeps the original <BIIIII header and no W_g — the reader branches on lane_type."""
    out = bytearray()
    out += CLMS_MAGIC
    lane_type = int(w.get("lane_type", 2))
    if lane_type in (2, 3):   # 2 = W_g fusion (H_9423) · 3 = 2 + majority-null centering (H_9710 RV-3)
        out += struct.pack("<BIIIIII", lane_type, int(w["n_slot"]), int(w["d_k"]), int(w["d_s"]),
                           int(w["d_g"]), int(w["r"]), int(w["key_seed"]))
        order = _ARR_ORDER_V2
    else:
        out += struct.pack("<BIIIII", 1, int(w["n_slot"]), int(w["d_k"]),
                           int(w["d_s"]), int(w["r"]), int(w["key_seed"]))
        order = _ARR_ORDER
    for name in order:
        out += np.asarray(w[name], dtype="<f4").reshape(-1).tobytes()
    return bytes(out)


def read_clms(buf: bytes, off: int, d: int, V: int):
    """Read a CLMS trailer at byte offset `off`. `d`,`V` come from the model (loader passes W["d"],
    W["V"]). Returns (clms_dict, new_off) or (None, off) if absent/short (passthrough-safe, same guard
    idiom as read_clml). Round-trip byte-identity is trivial: every array is <f4 in the file, the reader
    frombuffers and the writer tobytes — no recompute, no RNG."""
    if off < 0 or off + 5 > len(buf) or buf[off:off + 4] != CLMS_MAGIC:
        return None, off
    p = off + 4
    lane_type = buf[p]; p += 1
    if lane_type in (2, 3):                                # 2 = W_g fusion · 3 = 2 + centering (RV-3 · same header)
        if p + 24 > len(buf):
            return None, off
        n_slot, d_k, d_s, d_g, r, key_seed = struct.unpack_from("<IIIIII", buf, p); p += 24
    else:                                                  # lane_type 1 legacy (no W_g; d_g=0)
        if p + 20 > len(buf):
            return None, off
        n_slot, d_k, d_s, r, key_seed = struct.unpack_from("<IIIII", buf, p); p += 20
        d_g = 0

    def take(n, shape):
        nonlocal p
        arr = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy(); p += n * 4
        return arr

    clms = {"lane_type": int(lane_type), "n_slot": int(n_slot), "d_k": int(d_k),
            "d_s": int(d_s), "d_g": int(d_g), "r": int(r), "key_seed": int(key_seed)}
    clms["key_emb"] = take(_KEY_ALPHABET * d_k, (_KEY_ALPHABET, d_k))
    clms["W_q"] = take(d * d_k, (d, d_k))
    if lane_type in (2, 3):
        clms["W_g"] = take(d * d_g, (d, d_g))
    clms["val"] = take(2 * d_s, (2, d_s))
    w_h_in = (d_s + d_g) if lane_type in (2, 3) else (d_s + d)
    clms["W_h"] = take(w_h_in * r, (w_h_in, r))
    clms["b_h"] = take(r, (r,))
    clms["W_out"] = take(r * V, (r, V))
    clms["lam"] = float(np.frombuffer(buf, "<f4", 1, p)[0]); p += 4
    return clms, p


def clms_weights_from_torch(mod) -> dict:
    """Extract the CLMS weight dict (numpy) from a trained torch CLMSModule. nn.Linear.weight is
    (out,in) so the projections transpose; val is a raw Parameter (no transpose). d≠d_k, d_s+d≠r, r≠V
    are all non-square, so a missing transpose dies as a shape error (never silently)."""
    def n(t):
        return t.detach().cpu().numpy().astype("<f4")
    return {
        "lane_type": 3 if getattr(mod, "val_center", False) else 2,   # RV-3 centering → lane_type 3
        "n_slot": mod.n_slot, "d_k": mod.d_k, "d_s": mod.d_s,
        "d_g": mod.d_g, "r": mod.r, "key_seed": mod.key_seed,
        "key_emb": n(mod.key_emb),
        "W_q": n(mod.W_q.weight).T,          # (d_k,d) → (d,d_k)
        "W_g": n(mod.W_g.weight).T,          # (d_g,d) → (d,d_g)  H_9423 fusion bottleneck
        "val": n(mod.val),                    # (2,d_s)
        "W_h": n(mod.W_h.weight).T,          # (r,d_s+d_g) → (d_s+d_g,r)
        "b_h": n(mod.W_h.bias),
        "W_out": n(mod.W_out.weight).T,      # (V,r) → (r,V)
        "lam": n(mod.lam).reshape(1),
    }


# --------------------------------------------------------------------------- #
# (c) torch training module (DIRECTIONAL) — defined only when torch is present so
#     the inference import (store_apply / read_clms) stays torch-free (pod-clean).
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    import torch.nn.functional as _F
    _HAS_TORCH = True
except Exception:                     # pragma: no cover - inference pod has no torch
    _HAS_TORCH = False

if _HAS_TORCH:
    class CLMSModule(_nn.Module):
        """Learnable co-trained store-bridge lane. Trains {W_q, val, W_h(+bias), W_out, lam}; key_emb is
        a FROZEN buffer (never a parameter — no grad, not in the optimizer). K_slots is NOT a parameter:
        the store is runtime-injected. forward(yn_q:(B,d), K:(B,n_slot,d_k), pols:(B,n_slot),
        oracle_slot=None) -> (B,V) = lam·store_logits. Op order MIRRORS core/clms.store_apply 6–14
        exactly for 2-production parity. The caller overwrites logits[b, qpos] = forward(...) and takes
        CE — the module emits ONLY store_logits, so the trunk logit never receives answer-position grad
        (② shortcut-cut is structural, not a regulariser)."""

        def __init__(self, d, V, n_slot=8, d_k=64, d_s=64, r=128,
                     key_seed=9423, key_emb=None, lam0=1.0, d_g=64, val_center=False):
            super().__init__()
            self.d, self.V, self.n_slot = d, V, n_slot
            self.d_k, self.d_s, self.r, self.key_seed = d_k, d_s, r, key_seed
            self.d_g = d_g                                          # H_9423 fusion-bottleneck (lane_type 2)
            self.val_center = bool(val_center)                     # RV-3 majority-null centering (lane_type 3)
            self.scale = 1.0 / (d_k ** 0.5)
            if key_emb is None:
                ke = (np.random.RandomState(key_seed).standard_normal((256, d_k))
                      * (1.0 / np.sqrt(d_k))).astype("<f4")
            else:
                ke = np.asarray(key_emb, dtype="<f4")
            self.register_buffer("key_emb", _torch.from_numpy(ke.copy()), persistent=True)
            self.W_q = _nn.Linear(d, d_k, bias=False)
            # H_9423 value-read fix: yn_q enters the fusion MLP through a learned bottleneck W_g:d→d_g
            # (op is ~1 bit; d_g=64 suffices) so the store value v (d_s) is not diluted 59× against the
            # raw d=3784 penultimate. Restores the toy [v64;g64] fusion geometry d_model-invariantly —
            # the S2 both-arm ORACLE-death (0.47/0.49) was v drowned in [v; yn_q] at d=3784.
            self.W_g = _nn.Linear(d, d_g, bias=False)
            self.val = _nn.Parameter(_torch.randn(2, d_s) * 0.02)
            self.W_h = _nn.Linear(d_s + d_g, r)
            self.W_out = _nn.Linear(r, V, bias=False)
            self.lam = _nn.Parameter(_torch.tensor(float(lam0)))   # monitor-only scalar (no loss term)

        def entity_keys(self, entities):
            """(n_slot, d_k) content-addresses for a list of entity names — same formula as numpy
            _entity_key (mean of the frozen per-byte rows). Trainer builds K per block-store with this."""
            rows = []
            for e in entities:
                ids = _torch.tensor(list(e.encode("ascii")), dtype=_torch.long, device=self.key_emb.device)
                rows.append(self.key_emb[ids].mean(dim=0))
            return _torch.stack(rows)

        def forward(self, yn_q, K, pols, oracle_slot=None, need_att=False):
            # yn_q:(B,d) query-position penultimate · K:(B,n_slot,d_k) · pols:(B,n_slot) in {0,1}
            q = self.W_q(yn_q)                                            # (B,d_k)
            att = _torch.bmm(K, q.unsqueeze(-1)).squeeze(-1) * self.scale  # (B,n_slot) address logits
            if oracle_slot is not None:
                a = _F.one_hot(oracle_slot, self.n_slot).to(q.dtype)      # (B,n_slot) softmax bypassed
            else:
                a = _torch.softmax(att, dim=-1)
            V_slots = self.val[pols]                                      # (B,n_slot,d_s)
            if self.val_center:                                           # RV-3 majority-null centering (H_9710)
                a = a - (1.0 / self.n_slot)                               # v≡0 at uniform a → shortcut basin gone
            v = _torch.bmm(a.unsqueeze(1), V_slots).squeeze(1)           # (B,d_s)
            g = self.W_g(yn_q)                                            # (B,d_g) op-gate bottleneck
            z = _F.gelu(self.W_h(_torch.cat([v, g], dim=-1)), approximate="tanh")   # (B,r) [v; g] fusion
            s = self.W_out(z)                                             # (B,V)
            out = self.lam * s
            # H_9672 addr-loss: expose the pre-softmax address logits so the trainer can supervise them
            # (L_addr = CE(att, target_slot)). att is computed regardless of oracle_slot, so oracle-train
            # + addr-loss compose. need_att=False → byte-identical to the prior single-return signature.
            return (out, att) if need_att else out
