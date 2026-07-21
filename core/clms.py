"""core/clms.py — H_9423 CLMS store-bridge trailer lane, CORE-owned SSOT.

The ρ·weave recombination wall (was G1) is the ABSENCE of an operator<->declaration-store runtime
lookup bridge (H_9359): the FACT can live in a store and the OPERATOR in the text, yet a frozen conv
byte-LM has no port to bind them (bolt-on died 3-port, H_9392). v2 DIRECTIONAL-proved that a
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


def _sigmoid(x):
    """Overflow-safe logistic (H_9696 gate). The naive 1/(1+exp(-x)) warns and loses the branch for
    |x|>~700; a saturated gate is a LEGITIMATE state here (gate→0 is how the lane stays silent where
    it has nothing to say), so it must saturate cleanly rather than RuntimeWarning."""
    if x >= 0.0:
        return 1.0 / (1.0 + np.exp(-x))
    e = np.exp(x)
    return e / (1.0 + e)


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


def _entity_key(key_emb, entity, key_fn="mean"):
    """Content address for an entity name, built from the frozen per-byte embedding rows so it
    generalizes to held-out entities (a new key from seen bytes). key_emb is (256, d_k).

    key_fn="mean" (lane_type 1-5, the shipped address) is a plain row mean, which carries NO order
    term — entities sharing a normalised byte histogram get one key exactly, and equal keys give
    equal attention mass for every query, so training cannot separate them (H_9850).

    key_fn="roll" (lane_type 6) rotates each row by its byte POSITION before averaging, so order
    enters the address. Parameter-free — same frozen table, nothing new to learn — and it dominated
    every candidate on collisions, crowding and the exact-W ceiling in the H_9852 screen. Rotation
    wraps at d_k, so positions p and p+d_k rotate alike; entity names are far shorter than d_k."""
    ids = np.frombuffer(entity.encode("ascii"), dtype=np.uint8)
    if key_fn == "mean":
        return key_emb[ids].mean(axis=0)
    if key_fn == "roll":
        return np.mean([np.roll(key_emb[b], i) for i, b in enumerate(ids)], axis=0)
    raise ValueError("_entity_key: unknown key_fn %r (known: mean, roll)" % (key_fn,))


def _key_fn_of(lane_type):
    """lane_type -> address function. 6 = lane_type 3 semantics (W_g fusion + majority-null
    centering) with the order-aware key; every other lane keeps the shipped mean, so existing
    checkpoints are byte-identical."""
    return "roll" if int(lane_type) == 6 else "mean"


def store_apply(logits, yn, clms, store, qpos, oracle=False, lam_override=None, audit=None,
                query="qpos", fuse="overwrite", fresh_yn=None):
    """CLMS store-bridge lane: OVERWRITE the answer-position logits row with λ·store_logits.

    query/fuse (H_9695 R3 · the read→mouth wiring the G6 angles need · defaults reproduce the
    H_9423 lane byte-for-byte):
      query="qpos"        — fire only where find_qpos hits the literal "=> " trigram (H_9423).
      query="every-token" — fire at EVERY row. The literal trigram cannot exist in free ideation,
                            so a G6-facing lane must be able to query without a marker. Note the
                            marker is not merely absent in free generation: teaching the mouth to
                            emit "=> " itself would be kill #1's scaffold moved inside the mouth,
                            which is why the legal form is a learned gate (H_9696), not a literal.
      fuse="overwrite"    — out[t] = λ·s (H_9423 store_only gate: the structural shortcut-cut that
                            makes the storebind readout attributable to the lane alone).
      fuse="gated-add"    — out[t] = logits[t] + λ·s. Overwriting EVERY row would delete the trunk
                            and destroy fluency (dist<5 kills the ρ·fan panel before bind can be
                            read); additive keeps the lane a perturbation whose CONTENT-dependence
                            is what the scramble controls test.

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

    Passthrough (returns logits unchanged): clms None · lane_type==0 · store None · λ==0 · and
    (query="qpos" only) qpos empty. query="every-token" does NOT require qpos — free ideation
    contains no "=> " by construction, so gating the marker-free lane on the marker would silence
    it exactly where it is meant to fire (H_9695).
    Op order is IDENTICAL to CLMSModule.forward (2-production parity)."""
    if clms is None or int(clms.get("lane_type", 0)) == 0 or store is None:
        return logits
    if query == "qpos" and not qpos:
        return logits
    # numpy 2 refuses float() on a size-1 array, and clms_weights_from_torch emits lam with
    # shape (1,) while read_clms yields a scalar — accept both (H_9853, caught on a pool host
    # whose numpy is newer than the dev machine's).
    lam = (float(np.asarray(clms["lam"]).reshape(-1)[0]) if lam_override is None
           else float(lam_override))
    if lam == 0.0:
        return logits
    dt = logits.dtype
    n_slot = int(clms["n_slot"])
    key_emb = clms["key_emb"]
    ents = store["entities"]
    pols = np.asarray(store["pols"], dtype=np.int64)
    lane_type = int(clms.get("lane_type", 1))
    _kf = _key_fn_of(lane_type)                                            # 6 = order-aware (H_9852)
    K = np.stack([_entity_key(key_emb, ents[i], _kf) for i in range(n_slot)])   # (n_slot, d_k)
    if lane_type == 4:
        # H_9696 CLMS-FAN: free ideation carries no polarity, so the value cannot be val[pols]. The
        # slot's value is projected out of the slot's OWN key — the lane retrieves "which word I am
        # holding is relevant here" and re-injects its identity = the mouth-internal binding operator
        # H_1603 names as the shared missing part of both walls.
        V_slots = K @ clms["W_v"]                                          # (n_slot, d_s)
    else:
        V_slots = clms["val"][pols]                                        # (n_slot, d_s)
    scale = 1.0 / np.sqrt(float(clms["d_k"]))
    out = logits.copy()
    if query == "every-token":
        rows = range(len(yn))          # H_9695: marker-free — the lane queries at every position
    elif query == "qpos":
        rows = qpos
    else:
        raise ValueError("store_apply: query must be 'qpos' or 'every-token' (got %r)" % query)
    if fuse not in ("overwrite", "gated-add", "odd", "pairodd"):
        raise ValueError("store_apply: fuse must be 'overwrite', 'gated-add', 'odd' or 'pairodd' (got %r)" % fuse)
    for t in rows:
        h = yn[t]                                                          # (d,)
        if lane_type == 5:                                                 # H_9720-ⓐ fresh query lane
            hf = (fresh_yn[t] if fresh_yn is not None else h)              # early-layer tap (decode supplies it)
            q = _gelu(hf @ clms["W_fresh"]) @ clms["W_q_fresh"]           # (d_k,) disjoint address query
        else:
            q = h @ clms["W_q"]                                           # (d_k,) [row-vector conv, CLML-form]
        if oracle == "pair":
            # H_9875 PAIR-ORACLE — the 2-conjunct analogue of the C0-e oracle. Hands the address
            # for BOTH named slots (a = 1/2 onehot(A) + 1/2 onehot(B)) so v is exactly the mixture
            # the lane would form if its softmax had found both. It splits the only two live
            # accounts of the composed failure: the fusion MLP CAN separate the mixture (v sits at
            # the midpoint for xor=1 and at an endpoint for xor=0), so a PASS here says addressing
            # / credit assignment is the wall, and a FAIL says the answer never became a function
            # of v at all. Requires target_slot_b (compose panels carry it).
            a = np.zeros(n_slot, dtype=q.dtype)
            tb = store.get("target_slot_b")
            if tb is None:
                raise ValueError("store_apply: oracle='pair' needs target_slot_b — the panel is not "
                                 "a compose-2 panel (build it with `corpus storebind --compose 2`)")
            a[int(store["target_slot"])] += 0.5
            a[int(tb)] += 0.5
        elif oracle:
            a = np.zeros(n_slot, dtype=q.dtype)
            a[int(store["target_slot"])] = 1.0                            # softmax bypassed (address free)
        else:
            a = _softmax(q @ K.T * scale)                                # (n_slot,) content-address lookup
        if audit is not None:                                            # H_9672 addr-audit (None=byte-identical)
            ts = store.get("target_slot")
            # H_9802 store-telemetry: `a_max`/`a_ent` are TARGET-FREE, so they stay meaningful on
            # natural text where no target_slot exists (a_target degenerates to -1 there). They
            # split the two failure modes the H_9802 pre-check must tell apart BEFORE any training
            # spend: a_max ≈ 1/n_slot (uniform) ⟹ natural text never ADDRESSES the store
            # (recruitment problem); a_max ≫ 1/n_slot with wrong values ⟹ it addresses but the
            # values are garbage (alignment problem). a_ent is the entropy of the address
            # distribution normalised by log(n_slot), so 1.0 = uniform and 0.0 = a hard one-slot
            # hit — both read against the DERIVED uniform baseline, never an assumed chance.
            # MONITOR-ONLY (a_train_inline_gauge): never enters any loss or any frozen bar.
            _p = a / (a.sum() + 1e-12)
            _ent = float(-(_p * np.log(_p + 1e-12)).sum() / (np.log(n_slot) + 1e-12))
            audit.append({"argmax": int(np.argmax(a)),
                          "a_target": float(a[int(ts)]) if ts is not None else -1.0,
                          "target": int(ts) if ts is not None else -1,
                          "a_max": float(np.max(a)),
                          "a_ent": _ent})
        if lane_type in (3, 6):                                           # RV-3 majority-null centering (H_9710)
            a = a - (1.0 / n_slot)                                        # v≡0 at uniform a → shortcut basin gone
        v = a @ V_slots                                                   # (d_s,) = Σ (aᵢ−c)·val[polᵢ]
        if lane_type in (2, 3, 4, 5, 6):
            g = h @ clms["W_g"]                                           # (d_g,) op-gate bottleneck (H_9423)
            z = _gelu(np.concatenate([v, g]) @ clms["W_h"] + clms["b_h"]) # (r,) [v; g] fusion (v un-diluted)
        else:                                                             # lane_type 1 legacy: [v; h] fusion
            z = _gelu(np.concatenate([v, h]) @ clms["W_h"] + clms["b_h"]) # (r,) — S1/S2 artifacts, no silent recast
        s = z @ clms["W_out"]                                             # (V,)
        if fuse == "odd":                                                 # H_9760 odd-symmetrized fusion:
            v_neg = -v                                                    #   s_odd = ½(s(v,g) − s(−v,g)) cancels the
            if lane_type in (2, 3, 4, 5, 6):                                 #   even (op-gate g-path) prior that emits a
                z_neg = _gelu(np.concatenate([v_neg, g]) @ clms["W_h"] + clms["b_h"])  # polarity-invariant constant on
            else:                                                         #   op=0 (H_9744 flip-coh gap). For lane_type 3
                z_neg = _gelu(np.concatenate([v_neg, h]) @ clms["W_h"] + clms["b_h"])  # (Σ(aᵢ−1/n)=0 ⟹ v_flip≡−v) this
            s = 0.5 * (s - z_neg @ clms["W_out"])                         #   makes fixed-address flip-coherence = 1.
        elif fuse == "pairodd":                                           # H_9775 Π-equivariant pair-odd: full-row odd
            v_neg = -v                                                    #   (H_9760) killed the g/b argmax because it
            if lane_type in (2, 3, 4, 5, 6):                                 #   subtracted the even level that made g/b the
                z_neg = _gelu(np.concatenate([v_neg, g]) @ clms["W_h"] + clms["b_h"])  # top logits. Here out[c∉{g,b}]=
            else:                                                         #   ½(s⁺+s⁻) PRESERVES that even level (argmax
                z_neg = _gelu(np.concatenate([v_neg, h]) @ clms["W_h"] + clms["b_h"])  # stays g/b = readable) while
            s_neg = z_neg @ clms["W_out"]                                 #   swapping ONLY the answer pair makes the g/b
            G_BYTE, B_BYTE = 103, 98                                      #   margin exactly odd in store polarity (Π =
            sp_g, sp_b = float(s[G_BYTE]), float(s[B_BYTE])              #   103↔98 = the task's answer alphabet, not
            sn_g, sn_b = float(s_neg[G_BYTE]), float(s_neg[B_BYTE])      #   per-query gold). readability = measured DV.
            s = 0.5 * (s + s_neg)                                         #   out[c] = ½(s⁺[c]+s⁻[c]) for c∉{g,b}
            s[G_BYTE] = 0.5 * (sp_g + sn_b)                               #   out[g] = ½(s⁺[g]+s⁻[b])
            s[B_BYTE] = 0.5 * (sp_b + sn_g)                               #   out[b] = ½(s⁺[b]+s⁻[g])  ⟹ margin odd
        if lane_type == 4:
            # H_9696 learned query gate — the legal replacement for the "=> " literal. A literal
            # taught to the mouth is kill #1's scaffold relocated; a data-dependent nonlinear gate is
            # precisely the class kill #7 left unmeasured. gate→0 lets the lane stay silent where it
            # has nothing to say, which is what keeps free-gen fluency (dist>=5) alive.
            s = _sigmoid(float(h @ clms["W_gate"])) * s
        if fuse in ("overwrite", "odd", "pairodd"):                       # odd/pairodd use overwrite semantics (H_9760/H_9775)
            out[t] = (lam * s).astype(dt)                                 # ★ store_only gate (H_9423)
        else:                                                             # gated-add (H_9695/H_9696)
            out[t] = (logits[t] + lam * s).astype(dt)                     # lane = perturbation, trunk kept
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
# lane_type 3 = 2 + RV-3 majority-null centering (H_9710) — SAME arrays/header as V2, no new tensors.
# lane_type 4 (H_9696 CLMS-FAN): W_v projects the VALUE out of the slot's own key (free ideation has
# no polarity, so val[pols] has nothing to index) and W_gate is the learned query gate that replaces
# the "=> " literal. NOTE the number: lane_type 3 was taken by H_9710 (merged first) — same ID-race
# class as hypotheses-jsonl-3, one axis over. Pre-emptor keeps the number; this lane yields to 4.
_ARR_ORDER_V4 = ("key_emb", "W_q", "W_g", "W_v", "W_gate", "W_h", "b_h", "W_out", "lam")
# lane_type 5 (H_9720-ⓐ EN-disjoint fresh query lane): the address query is read from an early-layer
# tap through W_fresh→W_q_fresh (store-CE co-adapts an entity basis off the EN-occupied penultimate);
# W_q stays packed (unused for addressing, kept for diagnostics). Header adds fresh_k·fresh_L.
_ARR_ORDER_V5 = ("key_emb", "W_q", "W_fresh", "W_q_fresh", "W_g", "val", "W_h", "b_h", "W_out", "lam")


# ── H_9696 (R4) perceptual charging — what the store holds during free ideation ──────────
# The storebind lane got its store from a runtime manifest. Free ideation has no manifest, and both
# lab-full models named the same missing part: something must WRITE the store from what the mouth is
# actually reading. The one p5-clean answer is perception — the decode window's own content words
# become the keys (holding what you read in WM is a perception route, never the emit gate). p8-clean
# REQUIRES train and eval to charge through THIS SAME function: a manifest at train and a window at
# eval is literally a train/infer split.

def charge_store(tok, known, n_slot=8, min_len=3):
    """Build a store from the decode window's own bytes (perceptual charging · H_9696).

    tok   : the window's byte list (the SAME bytes the trunk sees — no side channel).
    known : the frozen dictionary the ρ·fan detector already uses. A nonce CANNOT be a G6 store entry
            because the detector's content-word gate requires `w in known` (rho_fan.py:364), so a
            store of CVCVC nonces is invisible to the very gate G6 scores — this is exactly where
            H_9672's synthetic-nonce lane and a G6-facing lane part ways.
    Returns {"entities": [w]*n_slot, "pols": [0]*n_slot, "target_slot": None}; pols is a structural
    placeholder (lane_type 4 derives its value from the key via W_v, never from pols). Fewer than
    n_slot distinct words ⇒ the tail repeats the last (a short window must not change the slot count,
    or the softmax denominator would move with window length). No content word ⇒ None = the lane
    stays passthrough (honest silence beats a fabricated store)."""
    s = "".join(chr(b) for b in tok if 0 <= b < 128)
    words = []
    seen = set()
    for w in _tokenize_ascii(s):
        if len(w) >= min_len and w in known and w not in seen:
            seen.add(w)
            words.append(w)
    if not words:
        return None
    while len(words) < n_slot:
        words.append(words[-1])
    return {"entities": words[:n_slot], "pols": [0] * n_slot, "target_slot": None}


def _tokenize_ascii(s):
    """Lowercased alnum runs — the shape rho_fan._rho_fan_words uses, kept local so core/clms does not
    import the scorer (the lane must not depend on the gate that judges it)."""
    out = []
    cur = []
    for ch in s:
        if ch.isalnum():
            cur.append(ch.lower())
        else:
            if cur:
                out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out
_KEY_ALPHABET = 256


def pack_clms(w: dict) -> bytes:
    """Pack a CLMS weight dict into appended trailer bytes. Absent trailer <=> byte-identical model, so
    a writer only calls this when the model actually has a CLMS lane. lane_type 2 (H_9423, default for a
    trained torch module) inserts d_g into the header (<BIIIIII) and W_g after W_q; lane_type 1 (legacy
    S1/S2 artifacts) keeps the original <BIIIII header and no W_g — the reader branches on lane_type."""
    out = bytearray()
    out += CLMS_MAGIC
    lane_type = int(w.get("lane_type", 2))
    if lane_type == 5:        # H_9720-ⓐ fresh query lane — V2 header + fresh_k/fresh_L, W_fresh/W_q_fresh
        out += struct.pack("<BIIIIIIII", 5, int(w["n_slot"]), int(w["d_k"]), int(w["d_s"]),
                           int(w["d_g"]), int(w["r"]), int(w["key_seed"]),
                           int(w["fresh_k"]), int(w["fresh_L"]))
        order = _ARR_ORDER_V5
    elif lane_type == 4:      # H_9696 CLMS-FAN — same header as V2/V3, extra W_v/W_gate arrays
        out += struct.pack("<BIIIIII", 4, int(w["n_slot"]), int(w["d_k"]), int(w["d_s"]),
                           int(w["d_g"]), int(w["r"]), int(w["key_seed"]))
        order = _ARR_ORDER_V4
    elif lane_type in (2, 3, 6):  # 2 = W_g fusion (H_9423) · 3 = 2 + majority-null centering (H_9710 RV-3) · 6 = 3 + order-aware key (H_9852)
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
    fresh_k = fresh_L = 0
    if lane_type == 5:                                     # H_9720-ⓐ fresh query lane (+fresh_k/fresh_L)
        if p + 32 > len(buf):
            return None, off
        n_slot, d_k, d_s, d_g, r, key_seed, fresh_k, fresh_L = struct.unpack_from("<IIIIIIII", buf, p); p += 32
    elif lane_type in (2, 3, 4, 6):                        # 2 = W_g · 3 = +centering (RV-3) · 4 = CLMS-FAN · 6 = 3 + order-aware key
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
            "d_s": int(d_s), "d_g": int(d_g), "r": int(r), "key_seed": int(key_seed),
            "fresh_k": int(fresh_k), "fresh_L": int(fresh_L)}
    clms["key_emb"] = take(_KEY_ALPHABET * d_k, (_KEY_ALPHABET, d_k))
    clms["W_q"] = take(d * d_k, (d, d_k))
    if lane_type == 5:                                    # H_9720-ⓐ fresh lane: W_fresh · W_q_fresh (pack order)
        clms["W_fresh"] = take(d * fresh_k, (d, fresh_k))
        clms["W_q_fresh"] = take(fresh_k * d_k, (fresh_k, d_k))
    if lane_type in (2, 3, 4, 5, 6):
        clms["W_g"] = take(d * d_g, (d, d_g))
    if lane_type == 4:                                     # H_9696: value-from-key + learned gate
        clms["W_v"] = take(d_k * d_s, (d_k, d_s))
        clms["W_gate"] = take(d, (d,))
    if lane_type != 4:                                     # lane 4 has no polarity table (W_v replaces it)
        clms["val"] = take(2 * d_s, (2, d_s))
    w_h_in = (d_s + d_g) if lane_type in (2, 3, 4, 5, 6) else (d_s + d)
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
    out = {
        "lane_type": (6 if getattr(mod, "key_fn", "mean") == "roll" else  # 6=H_9852 order-aware key (3+roll)
                      (5 if int(getattr(mod, "fresh_k", 0)) > 0 else       # 5=H_9720-ⓐ fresh query lane
                      (4 if getattr(mod, "fangate", False) else
                       (3 if getattr(mod, "val_center", False) else 2)))),  # 4=CLMS-FAN · 3=RV-3 · 2=W_g
        "n_slot": mod.n_slot, "d_k": mod.d_k, "d_s": mod.d_s,
        "d_g": mod.d_g, "r": mod.r, "key_seed": mod.key_seed,
        "fresh_k": int(getattr(mod, "fresh_k", 0)), "fresh_L": int(getattr(mod, "fresh_L", 3)),
        "key_emb": n(mod.key_emb),
        "W_q": n(mod.W_q.weight).T,          # (d_k,d) → (d,d_k)
        "W_g": n(mod.W_g.weight).T,          # (d_g,d) → (d,d_g)  H_9423 fusion bottleneck
        "val": n(mod.val),                    # (2,d_s)
        "W_h": n(mod.W_h.weight).T,          # (r,d_s+d_g) → (d_s+d_g,r)
        "b_h": n(mod.W_h.bias),
        "W_out": n(mod.W_out.weight).T,      # (V,r) → (r,V)
        "lam": n(mod.lam).reshape(1),
    }
    if out["lane_type"] == 5:                 # H_9720-ⓐ — fresh query lane projections
        out["W_fresh"] = n(mod.W_fresh.weight).T      # (fresh_k,d) → (d,fresh_k)
        out["W_q_fresh"] = n(mod.W_q_fresh.weight).T  # (d_k,fresh_k) → (fresh_k,d_k)
    if out["lane_type"] == 4:                 # H_9696 — value-from-key + learned gate; val not packed
        out["W_v"] = n(mod.W_v.weight).T      # (d_s,d_k) → (d_k,d_s)
        out["W_gate"] = n(mod.W_gate.weight).reshape(-1)   # (1,d) → (d,)
        out.pop("val", None)
    return out


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
                     key_seed=9423, key_emb=None, lam0=1.0, d_g=64, val_center=False, fangate=False,
                     fresh_k=0, fresh_L=3, key_fn="mean"):
            super().__init__()
            self.key_fn = key_fn          # H_9852 address function (mean | roll)
            self.d, self.V, self.n_slot = d, V, n_slot
            self.d_k, self.d_s, self.r, self.key_seed = d_k, d_s, r, key_seed
            self.d_g = d_g                                          # H_9423 fusion-bottleneck (lane_type 2)
            self.val_center = bool(val_center)                     # RV-3 majority-null centering (lane_type 3)
            self.fangate = bool(fangate)                           # H_9696 CLMS-FAN (lane_type 4)
            # H_9720-ⓐ EN-disjoint fresh query lane (lane_type 5): the ADDRESS query is read from an
            # early-layer tap (detached from the trunk in the trainer) through W_fresh·W_q_fresh — store-CE
            # co-adapts an entity basis that does NOT compete with EN-CE for the penultimate. fresh_k=0 =
            # off = every existing lane byte-identical (nothing packed, forward unchanged).
            self.fresh_k, self.fresh_L = int(fresh_k), int(fresh_L)
            self.scale = 1.0 / (d_k ** 0.5)
            if key_emb is None:
                ke = (np.random.RandomState(key_seed).standard_normal((256, d_k))
                      * (1.0 / np.sqrt(d_k))).astype("<f4")
            else:
                ke = np.asarray(key_emb, dtype="<f4")
            self.register_buffer("key_emb", _torch.from_numpy(ke.copy()), persistent=True)
            self.W_q = _nn.Linear(d, d_k, bias=False)
            if self.fresh_k > 0:                                   # H_9720-ⓐ fresh query lane params
                self.W_fresh = _nn.Linear(d, self.fresh_k, bias=False)      # tap(d) → fresh_k
                self.W_q_fresh = _nn.Linear(self.fresh_k, d_k, bias=False)  # fresh_k → d_k address
            # H_9423 value-read fix: yn_q enters the fusion MLP through a learned bottleneck W_g:d→d_g
            # (op is ~1 bit; d_g=64 suffices) so the store value v (d_s) is not diluted 59× against the
            # raw d=3784 penultimate. Restores the toy [v64;g64] fusion geometry d_model-invariantly —
            # the S2 both-arm ORACLE-death (0.47/0.49) was v drowned in [v; yn_q] at d=3784.
            self.W_g = _nn.Linear(d, d_g, bias=False)
            self.val = _nn.Parameter(_torch.randn(2, d_s) * 0.02)
            if self.fangate:
                # H_9696: free ideation has no polarity — the value is projected from the slot's OWN
                # key (W_v), and a learned data-dependent gate (W_gate) replaces the "=> " literal.
                # `val` stays allocated but is UNUSED on this lane (and is not packed).
                self.W_v = _nn.Linear(d_k, d_s, bias=False)
                self.W_gate = _nn.Linear(d, 1, bias=False)
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

        def forward(self, yn_q, K, pols, oracle_slot=None, need_att=False, yn_fresh=None):
            # yn_q:(B,d) query-position penultimate · K:(B,n_slot,d_k) · pols:(B,n_slot) in {0,1}
            # yn_fresh:(B,d) H_9720-ⓐ early-layer tap (trainer detaches it); when present + fresh_k>0 the
            # ADDRESS query comes from the disjoint fresh lane, but yn_q STILL drives the W_g op-gate below.
            if self.fresh_k > 0 and yn_fresh is not None:
                q = self.W_q_fresh(_F.gelu(self.W_fresh(yn_fresh), approximate="tanh"))  # (B,d_k)
            else:
                q = self.W_q(yn_q)                                        # (B,d_k)
            att = _torch.bmm(K, q.unsqueeze(-1)).squeeze(-1) * self.scale  # (B,n_slot) address logits
            if oracle_slot is not None:
                a = _F.one_hot(oracle_slot, self.n_slot).to(q.dtype)      # (B,n_slot) softmax bypassed
            else:
                a = _torch.softmax(att, dim=-1)
            V_slots = self.W_v(K) if self.fangate else self.val[pols]     # (B,n_slot,d_s)
            if self.val_center:                                           # RV-3 majority-null centering (H_9710)
                a = a - (1.0 / self.n_slot)                               # v≡0 at uniform a → shortcut basin gone
            v = _torch.bmm(a.unsqueeze(1), V_slots).squeeze(1)           # (B,d_s)
            g = self.W_g(yn_q)                                            # (B,d_g) op-gate bottleneck
            z = _F.gelu(self.W_h(_torch.cat([v, g], dim=-1)), approximate="tanh")   # (B,r) [v; g] fusion
            s = self.W_out(z)                                             # (B,V)
            if self.fangate:
                s = _torch.sigmoid(self.W_gate(yn_q)) * s                 # (B,1)*(B,V) learned gate
            out = self.lam * s
            # H_9672 addr-loss: expose the pre-softmax address logits so the trainer can supervise them
            # (L_addr = CE(att, target_slot)). att is computed regardless of oracle_slot, so oracle-train
            # + addr-loss compose. need_att=False → byte-identical to the prior single-return signature.
            return (out, att) if need_att else out

    def codec_roundtrip_selftest(key_fn="mean", verbose=True):
        """pack_clms -> read_clms must return EVERY array at its original shape, not just the same
        lane_type (H_9853).

        A lane_type left out of read_clms's HEADER branch silently falls through to the legacy
        header, which has no d_g field: d_g reads 0, W_g comes back (d, 0), W_h/b_h/W_out come back
        at the wrong width, and the lane is dead at inference while training reported perfect
        accuracy. That is exactly how lane 6 shipped broken — the roundtrip was checked for
        lane_type only, so the shapes were never compared. Comparing lane_type alone is not a
        roundtrip check."""
        import numpy as np
        d, V, n_slot, d_k, d_s, r = 32, 48, 8, 16, 16, 24
        _torch.manual_seed(9853)
        mod = CLMSModule(d, V, n_slot=n_slot, d_k=d_k, d_s=d_s, r=r, lam0=0.7,
                         val_center=(key_fn == "roll"), key_fn=key_fn).double()
        w = clms_weights_from_torch(mod)
        got = read_clms(pack_clms(w), 0, d, V)
        if isinstance(got, tuple):
            got = got[0]
        rows, ok = [], True
        if int(got.get("lane_type", -1)) != int(w["lane_type"]):
            rows.append(("lane_type", w["lane_type"], got.get("lane_type"), False)); ok = False
        for k in ("d_g", "d_k", "d_s", "r", "n_slot"):
            same = int(got.get(k, -1)) == int(w[k])
            ok = ok and same
            rows.append((k, int(w[k]), int(got.get(k, -1)), same))
        for k in ("key_emb", "W_q", "W_g", "val", "W_h", "b_h", "W_out"):
            a = np.asarray(w[k]).shape
            b = np.asarray(got[k]).shape if k in got else None
            same = (a == b)
            ok = ok and same
            rows.append((k, a, b, same))
        if verbose:
            print("  codec roundtrip · key_fn=%s (lane_type %d)" % (key_fn, w["lane_type"]))
            for nm, a, b, same in rows:
                print("    %-9s packed=%-14s read=%-14s %s"
                      % (nm, a, b, "ok" if same else "MISMATCH <-- lane dropped to a wrong header"))
            print("  ROUNDTRIP %s" % ("PASS" if ok else "FAIL"))
        return ok, rows


    def parity_selftest(tol=2e-5, seed=9826, q_scale=8.0, key_fn="mean", verbose=True):
        """H_9826 — does the numpy inference mirror still equal the torch trainer?

        The lane is written TWICE: CLMSModule.forward trains it, store_apply serves it. Until now
        the two were held in step by a COMMENT ("Op order MIRRORS core/clms.store_apply 6–14"), so a
        silent op-order divergence would move a verdict in either direction with nothing to catch it.

        Builds one random CLMSModule, converts it with clms_weights_from_torch, runs BOTH paths on
        the same input, and compares. Then, one tensor at a time, RESAMPLES that tensor at its own
        scale — the shape a real "the two implementations disagree here" drift takes — and asserts
        every such divergence is caught. A guard is trustworthy only once it has been shown it can
        fail (lab/v2 gradcheck --selftest discipline).

        OPERATING POINT (why q_scale exists, measured not assumed): at raw random init the address
        softmax is near-uniform (a_max 0.1281 vs uniform 0.1250), so v = a·V_slots barely moves when
        the address changes and a W_q divergence is INVISIBLE (delta 1.3e-05 < tol) — the check would
        report a clean bill while blind to one tensor. Influence rises monotonically with the query
        scale (a_max 0.1376 / 0.1512 / 0.1808 at scale 4 / 8 / 16; W_q delta 5.1e-05 / 1.0e-04 /
        2.1e-04), while parity itself stays exact (~1e-17) at every scale. So the module is placed at
        a well-scaled point and the address influence is then ASSERTED as a precondition — reading
        the corruption arms at a dead-flat point is what makes a guard fake.

        arm64 numpy raises spurious divide-by-zero/overflow RuntimeWarnings inside matmul here while
        every value stays finite (a known false alarm in this repo); finiteness is asserted instead.

        Returns (ok, rows) with rows = [(name, max_abs_delta, caught_or_None)]; row 0 is the
        uncorrupted parity arm, row 1 the address-influence precondition."""
        import numpy as np
        d, V, n_slot, d_k, d_s, r = 32, 48, 8, 16, 16, 24
        _torch.manual_seed(seed)
        rng = np.random.default_rng(seed)
        mod = CLMSModule(d, V, n_slot=n_slot, d_k=d_k, d_s=d_s, r=r, lam0=0.7,
                         val_center=(key_fn == "roll"), key_fn=key_fn).double()
        mod.eval()
        with _torch.no_grad():
            mod.W_q.weight.mul_(q_scale)          # well-scaled point: the address path must matter
        w = clms_weights_from_torch(mod)
        for k in ("key_emb", "W_q", "W_g", "val", "W_h", "b_h", "W_out", "lam"):
            w[k] = np.asarray(w[k], dtype=np.float64)

        ents = ["slot%d" % i for i in range(n_slot)]
        pols = [int(rng.integers(0, 2)) for _ in range(n_slot)]
        store = {"entities": ents, "pols": pols, "target_slot": 3}
        yn = rng.standard_normal((5, d))
        logits = rng.standard_normal((5, V))
        qpos = [2]

        _kf = _key_fn_of(w["lane_type"])          # the guard must use the lane's OWN address fn
        K = np.stack([_entity_key(w["key_emb"], e, _kf) for e in ents])     # (n_slot, d_k)
        with _torch.no_grad():
            ref = mod(_torch.from_numpy(yn[qpos]),                          # (1,d)
                      _torch.from_numpy(K)[None, :, :],                     # (1,n_slot,d_k)
                      _torch.tensor([pols], dtype=_torch.long)).numpy()[0]  # (V,)

        def _delta(wd):
            got = store_apply(logits, yn, wd, store, qpos, fuse="overwrite")[qpos[0]]
            if not (np.all(np.isfinite(got)) and np.all(np.isfinite(ref))):
                return float("nan")
            return float(np.max(np.abs(got - ref)))

        a_unif = 1.0 / n_slot
        a_max = float(np.max(_softmax((yn[qpos[0]] @ w["W_q"]) @ K.T / np.sqrt(float(d_k)))))
        par = _delta(w)
        rows = [("parity (uncorrupted)", par, None),
                ("address influence a_max", a_max, None)]
        for name in ("W_q", "W_g", "val", "W_h", "b_h", "W_out", "lam"):
            bad = dict(w)
            t = np.asarray(w[name], dtype=np.float64)
            bad[name] = rng.standard_normal(t.shape) * (float(t.std()) + 1e-12)
            rows.append((("drift " + name), _delta(bad), None))

        ok_par = (par == par) and par <= tol            # NaN-safe
        ok_point = a_max > a_unif * 1.10                # the address must actually influence output
        out_rows = [rows[0], rows[1]]
        ok_catch = True
        for nm, dv, _ in rows[2:]:
            caught = (dv == dv) and dv > tol
            ok_catch = ok_catch and caught
            out_rows.append((nm, dv, caught))
        ok = ok_par and ok_point and ok_catch
        if verbose:
            print("  tolerance = %.1e   (torch fp64 vs numpy fp64) · q_scale = %.1f · key_fn = %s "
                  "(lane_type %d)" % (tol, q_scale, _kf, w["lane_type"]))
            print("    %-24s max|delta| = %.3e   %s" %
                  ("parity (uncorrupted)", par, "PASS" if ok_par else "FAIL <-- mirror diverged"))
            print("    %-24s a_max = %.4f (uniform %.4f)   %s" %
                  ("address influence", a_max, a_unif,
                   "PASS" if ok_point else "FAIL <-- dead-flat point, corruption arms unreadable"))
            for nm, dv, caught in out_rows[2:]:
                print("    %-24s max|delta| = %.3e   %s" %
                      (nm, dv, "CAUGHT" if caught else "MISSED <-- guard blind to this tensor"))
        return ok, out_rows
