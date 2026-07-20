"""core/tension_field.py — H_9805 WRITE-SIDE PARSE-DISAGREEMENT TENSION FIELD ("TFLD" trailer).

WHY THIS EXISTS, in one line: production's A⇄G tension is a SCALAR (`conflict_scalar` in
core/engine_cli.py — H_9356 measured it a "deterministic parabola of one scalar"; H_9714 put its
rank at ~2.66; `cli/chat.py --tension-route` routes one PC of it), and a scalar tension is exactly
the rank-1 READOUT-side seam that carried 1 bit and died. This lane moves the tension to the other
side of the trunk and keeps it a FIELD.

Provenance and its ceiling
--------------------------
The construction is ported from the anima-v4 sandbox result H_004 (lab/v4, rule-exempt): on a 3.7M
byte trunk a hand-staged per-edge parse-disagreement field, injected write-side, caused held-out
honorific binding BEYOND its own rank-1 compression (Δd_acc 0.3789/0.3802, off-top 0.6467/0.6963).
That number is a TOY, from a rule-exempt tree, and can NEVER be a production verdict — it licenses
building this instrument, nothing more. Every claim this file can support is PROPOSED/DIRECTIONAL
until an `anima-py` measurement at 303M says otherwise.

The construction
----------------
Two content-BLIND directional proxy parsers run over the SAME byte window. Neither sees the answer,
the labels, or anything but the chunk skeleton the byte classes already imply:

    P_A  (L->R, "A" engine)  head_A(i) = start of the NEXT chunk after i's chunk      — nearest head
    P_G  (R->L, "G" engine)  head_G(i) = start of the LAST chunk in the window        — maximal projection

Where the two directions AGREE the edge carries no tension and contributes nothing. Where they
disagree we get a signed per-edge structural field, modulated by a content-blind concord term:

    T_struct[i, head_A(i)] += 1        T_struct[i, head_G(i)] -= 1     (only when head_A != head_G)
    chi[i, j]              = +1 if byte_class(i) == byte_class(j) else -1
    T                      = T_struct * chi

This mirrors H_004's `t_struct` / `concord_field` exactly, with the hand-built node skeleton replaced
by a byte-derived one so it runs on any corpus. NOTE the honest consequence of that substitution: the
production concord is a byte-class agreement, NOT H_004's honorific concord — the FORMAT is ported,
the linguistic content is not. Whether a byte-class concord carries anything is precisely what the
pre-registered falsifiers have to decide, and it is entirely possible the answer is no.

The field is computed with NO gradient and NO learned parameter — it is a deterministic function of
the bytes. That is deliberate: it keeps the G side gradient-free (a_core_engine_map) and it means the
`duel` vs `rank1` contrast cannot be confounded by the field itself having been tuned.

Write-side injection (the whole point — placement, not magnitude)
-----------------------------------------------------------------
The field is reduced to one vector per position and added to the embeddings BEFORE the trunk:

    r_i = SUM_j T[i, j] * phi[bucket(j - i)]              phi: (n_bucket, rank) learned
    x   = embed(tokens) + lam * (r @ W_up)                W_up: (rank, d)      learned

`bucket` is a fixed signed log2 binning of the relative offset, so the geometry is window-size
independent and the trailer is well-defined. Only `phi`, `W_up`, `lam` are trained; the field itself
is frozen structure.

The three arms — ONE variable
-----------------------------
    duel   TREATMENT.  r_i built from the full T. Because T_struct has at most two nonzeros per row,
                       this is O(T) and needs no dense matrix at all.
    rank1  THE CONTROL THAT MAKES THE CLAIM READABLE. T is replaced by its best rank-1 approximation
                       (Frobenius-matched, sigma-tie broken exactly as H_004's `rank1_tiebreak`), then
                       the IDENTICAL reduction, the IDENTICAL parameter count, the IDENTICAL lam.
                       The single variable between the arms is whether the reduction eats the field or
                       a rank-1 summary of it. If `duel` ~ `rank1`, this lane is production's existing
                       scalar seam wearing a bigger costume, and the port is dead. That is the reading
                       the falsifiers are written to force.
    off    PARITY.     r is identically 0, returned without a copy or any arithmetic, so the ckpt is
                       byte-identical to one trained with the lane never engaged.

`rank1` pays a per-window SVD that `duel` does not; the arms are matched in parameters and in what
reaches the trunk, NOT in wall-clock. Do not read a speed difference as a result.

DISJOINT (a_substrate_disjoint): its own file, its own trailer, additive at the embeddings, appended
after IFAN. Absent trailer OR arm `off` => the lane returns the caller's array untouched.
"""

from __future__ import annotations

import struct
import numpy as np

TFLD_MAGIC = bytes([84, 70, 76, 68])   # "TFLD" — chain CLMB→SLW→CLML→CLMS→MBND→IFAN→TFLD

N_MAG = 8                              # log2 magnitude bins per sign
N_BUCKET = 2 * N_MAG                   # signed → 16 offset buckets


# --------------------------------------------------------------------------- #
# byte skeleton — content-blind. Nothing below looks at WHICH letter/word it is.
# --------------------------------------------------------------------------- #
def byte_class(b):
    """4 content-blind classes: 0 whitespace · 1 punct/digit · 2 ASCII letter · 3 high byte.

    `b` is an int array of byte values. The class is what `chi` agrees/disagrees on; it is
    deliberately coarse so the concord term cannot smuggle in lexical identity."""
    b = np.asarray(b, dtype=np.int64)
    cls = np.full(b.shape, 1, dtype=np.int64)
    cls[b >= 128] = 3
    ascii_letter = ((b >= 65) & (b <= 90)) | ((b >= 97) & (b <= 122))
    cls[ascii_letter] = 2
    cls[(b == 32) | (b == 9) | (b == 10) | (b == 13)] = 0
    return cls


# ── H_9812 LEXICAL CONCORD (the fix for the letter-blind field) ───────────────────────────
# Measured defect: with concord="class" the field is a function of the WHITESPACE/PUNCT LAYOUT
# ALONE. Verified by construction, not by argument — hold the whitespace positions fixed and
# replace every letter (or swap letters for digits, or upper-case everything) and the (T,T) field
# comes back BIT-IDENTICAL (max |Δ| = 0.000000); only punctuation moves it (2.0). The cause is
# right here: every chunk head is a word-initial letter, so `cls[head]` is the constant 2 and the
# concord term collapses to "is position i a letter". lab/v4's field came from two directional
# parsers over real tokens with an honorific-concord chi — a LEXICAL feature — so the port did not
# reproduce the mechanism it claims to port; on any panel keyed to word identity it carries 0 bits
# and a Δ of 0 means NO CHANNEL, not rank collapse.
#
# The old docstring called the coarseness deliberate ("so the concord term cannot smuggle in
# lexical identity"). That worry is real and is why this is a MODE, not a replacement: `class`
# survives as the layout-only control arm, and the leak it guards against is now excluded by a
# measurement (the field-alone readout must sit at chance) instead of by blindness.
N_SIG = 64                      # concord classes for the chunk signature (coarse ⇒ not an identity)
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3


def chunk_morph(b):
    """(T,) int — the MORPHOLOGICAL marker of each position's chunk: its FINAL byte.

    This is the closest byte-substrate analogue of what lab/v4's chi actually compared. v4's concord
    was HONORIFIC CONCORD — a grammatical feature of the two competing heads — not word identity.
    In English the agreement-bearing morphology sits at the word END (verb `+s`/`+ing`, noun `+s`),
    so the final byte is where a concord test has to look.

    Is exposing it a leak? That question is settled by MEASUREMENT, not by argument: a single
    agreement feature does not determine a gold that is an XOR over K conjuncts, and H_9810's panel
    builder already audits every single heuristic to exactly 0.500000. The deciding control is a
    field-alone readout — if the field by itself predicts the answer above chance, this mode is
    disqualified and the audit says so. Whitespace positions get -1 and never agree.
    """
    b = np.asarray(b, dtype=np.int64)
    T = int(b.shape[0])
    ws = (b == 32) | (b == 9) | (b == 10) | (b == 13)
    out = np.full(T, -1, dtype=np.int64)
    i = 0
    while i < T:
        if ws[i]:
            i += 1
            continue
        j = i
        while j < T and not ws[j]:
            j += 1
        out[i:j] = int(b[j - 1])          # the chunk's final byte
        i = j
    return out


def chunk_signature(b, n_sig=N_SIG):
    """(T,) int — a coarse content signature of the CHUNK (word) each position belongs to.

    FNV-1a over the chunk's bytes, folded to `n_sig` classes. Coarse ON PURPOSE: two different
    words collide with probability ~1/n_sig, so the signature is a cheap agreement test between
    words, not a word ID the trunk could read the answer off. Whitespace positions get -1 and
    never agree with anything.
    """
    b = np.asarray(b, dtype=np.int64)
    T = int(b.shape[0])
    ws = (b == 32) | (b == 9) | (b == 10) | (b == 13)
    sig = np.full(T, -1, dtype=np.int64)
    i = 0
    while i < T:
        if ws[i]:
            i += 1
            continue
        j = i
        h = FNV_OFFSET
        while j < T and not ws[j]:
            h = ((h ^ int(b[j])) * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
            j += 1
        sig[i:j] = int(h % int(n_sig))
        i = j
    return sig


def chunk_heads(b):
    """The two directional parses. Returns (head_a, head_g), int arrays of length T; -1 = no head.

    A chunk boundary is a whitespace byte. `head_a` is the start of the NEXT chunk (the L->R nearest
    licensed head); `head_g` is the start of the LAST chunk in the window (the R->L maximal
    projection head). Positions in the final chunk have no forward head under either parse, and
    positions in the penultimate chunk have head_a == head_g — both cases contribute zero tension,
    which is the correct behaviour: agreement is not tension.
    """
    b = np.asarray(b, dtype=np.int64)
    T = int(b.shape[0])
    ws = (b == 32) | (b == 9) | (b == 10) | (b == 13)
    # chunk id per position: increments after each run of whitespace
    starts = []
    prev_ws = True
    for i in range(T):
        if not ws[i] and prev_ws:
            starts.append(i)
        prev_ws = bool(ws[i])
    head_a = np.full(T, -1, dtype=np.int64)
    head_g = np.full(T, -1, dtype=np.int64)
    if len(starts) < 2:
        return head_a, head_g                     # a single chunk cannot disagree with itself
    last = starts[-1]
    # for position i, the next chunk start strictly greater than i
    starts_arr = np.asarray(starts, dtype=np.int64)
    idx = np.searchsorted(starts_arr, np.arange(T), side="right")
    has_next = idx < len(starts_arr)
    head_a[has_next] = starts_arr[idx[has_next]]
    head_g[has_next] = last
    return head_a, head_g


def offset_bucket(off):
    """Signed log2 binning of a relative offset. off == 0 is never produced (heads are strictly
    forward), but is mapped to bucket 0 defensively rather than raising."""
    off = np.asarray(off, dtype=np.int64)
    mag = np.abs(off)
    lg = np.zeros(mag.shape, dtype=np.int64)
    nz = mag > 0
    lg[nz] = np.minimum(np.floor(np.log2(mag[nz].astype(np.float64))).astype(np.int64), N_MAG - 1)
    sign_hi = (off < 0).astype(np.int64)
    return sign_hi * N_MAG + lg


def tension_edges(tokens, concord="class"):
    """The write-side field in its native SPARSE form — the honest representation of what P_A/P_G
    actually produce (at most two signed edges per position).

    Returns (rows, cols, vals) int/int/float arrays. Only positions where the two parses DISAGREE
    contribute. `vals` already carries the concord sign chi.

    concord="class" — LEGACY/CONTROL. chi compares `byte_class`, which makes the whole field a
                      function of the whitespace+punct layout and blind to word identity (H_9812).
                      Kept as the layout-only pedestal arm, not as a default to build on.
    concord="lex"   — chi compares the CHUNK SIGNATURE, so the field depends on WHICH words sit at
                      the two competing heads. This is the arm that has a channel at all.
    """
    b = np.asarray(tokens, dtype=np.int64)
    if concord not in CONCORD_CODE:
        raise ValueError("concord must be one of class|lex|morph (got %r)" % (concord,))
    cls = {"class": byte_class, "lex": chunk_signature, "morph": chunk_morph}[concord](b)
    head_a, head_g = chunk_heads(b)
    live = (head_a >= 0) & (head_g >= 0) & (head_a != head_g)
    idx = np.nonzero(live)[0]
    if idx.size == 0:
        return (np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0, np.float64))
    ja, jg = head_a[idx], head_g[idx]
    chi_a = np.where(cls[idx] == cls[ja], 1.0, -1.0)
    chi_g = np.where(cls[idx] == cls[jg], 1.0, -1.0)
    rows = np.concatenate([idx, idx])
    cols = np.concatenate([ja, jg])
    vals = np.concatenate([chi_a, -chi_g])          # +1 on the A edge, -1 on the G edge
    return rows, cols, vals


def tension_matrix(tokens, concord="class"):
    """Dense (T, T) field. Needed by the `rank1` arm and by the rank audit; the `duel` arm never
    builds it."""
    b = np.asarray(tokens, dtype=np.int64)
    T = int(b.shape[0])
    M = np.zeros((T, T), dtype=np.float64)
    rows, cols, vals = tension_edges(b, concord=concord)
    if rows.size:
        np.add.at(M, (rows, cols), vals)
    return M


def svdvals(M):
    """Singular values, ROBUST to a LAPACK gesdd non-convergence.

    Not defensive programming — a measured defect. numpy's default SVD driver returned 8 NaN
    singular values on a perfectly finite 256x256 field matrix from a shuffled real window (found
    by the H_9805 toy e2e; the matrix was finite, nnz=484, and the eigenvalue route gave a clean
    spectrum). gesdd does not raise there, it returns NaN, so a rank number computed off it is
    silently VOID rather than obviously broken — and a NaN pedestal would have made the treatment
    arm unfalsifiable by comparison.

    So: try gesdd, and on any non-finite result fall back to the eigen-decomposition of the Gram
    matrix, whose singular values are sqrt(max(eig, 0)). The fallback is only slightly less
    accurate for tiny singular values, which the rank statistics here barely weight.
    """
    M = np.asarray(M, dtype=np.float64)
    try:
        s = np.linalg.svd(M, compute_uv=False)
        if np.all(np.isfinite(s)):
            return s
    except np.linalg.LinAlgError:
        pass
    g = M.T @ M if M.shape[0] >= M.shape[1] else M @ M.T
    ev = np.linalg.eigvalsh((g + g.T) * 0.5)
    return np.sqrt(np.clip(ev, 0.0, None))[::-1]


def rank1_tiebreak(T, tol=1e-9):
    """Best rank-1 approximation, sigma-ties broken by retaining the component whose support has the
    smallest leading row index. Ported verbatim in behaviour from H_004's `rank1_tiebreak` — a tie
    broken by numpy's arbitrary ordering would make the control arm non-reproducible."""
    T = np.asarray(T, dtype=np.float64)
    if T.size == 0 or not np.any(T):
        return np.zeros_like(T)
    try:
        U, s, Vt = np.linalg.svd(T)
        ok = np.all(np.isfinite(s)) and np.all(np.isfinite(U[:, 0])) and np.all(np.isfinite(Vt[0]))
    except np.linalg.LinAlgError:
        ok = False
    if not ok:
        # same gesdd non-convergence as `svdvals` — recover the top pair from the Gram matrix.
        g = T.T @ T
        ev, evec = np.linalg.eigh((g + g.T) * 0.5)
        v1 = evec[:, -1]
        Mv = T @ v1
        s1 = float(np.linalg.norm(Mv))
        if s1 <= 0.0:
            return np.zeros_like(T)
        return s1 * np.outer(Mv / s1, v1)
    if len(s) > 1 and s[0] - s[1] < tol * max(s[0], 1.0):
        rows = [i for i in range(T.shape[0]) if np.abs(T[i]).sum() > 0]
        if rows:
            i0 = min(rows)
            R = np.zeros_like(T)
            R[i0] = T[i0]
            return R
    return s[0] * np.outer(U[:, 0], Vt[0])


# --------------------------------------------------------------------------- #
# rank audit — the standing instrument behind `anima-py evaluate --tension-rank-audit`.
# H_004's F4 made permanent: a lane whose field has collapsed to rank 1 IS the old scalar seam,
# and that has to be visible without re-running the campaign.
# --------------------------------------------------------------------------- #
def rank_report(tokens, concord="class"):
    """Effective-rank diagnostics for one window. All three numbers are derived from the realized
    singular spectrum, not assumed (chance-level-must-be-derived-per-metric):

      off_top     1 - s1^2/sum(s^2)      fraction of field energy OFF the top singular direction.
                                         0.0 == an exactly rank-1 field == the scalar seam.
      eff_rank    (sum s^2)^2 / sum s^4  participation ratio. Exactly 1.0 iff rank-1.
      stable_rank ||T||_F^2 / s1^2       >= 1, == 1 iff rank-1.
      n_edge      how many signed edges the two parses actually disagreed on. 0 => the window is
                  structurally silent and every rank number above is VOID, not "rank 1".
    """
    M = tension_matrix(tokens, concord=concord)
    rows, _, _ = tension_edges(tokens, concord=concord)
    n_edge = int(rows.size)
    if n_edge == 0 or not np.any(M):
        return {"n_edge": n_edge, "off_top": None, "eff_rank": None, "stable_rank": None,
                "fro2": 0.0, "void": True}
    s = svdvals(M)
    s2 = s ** 2
    tot = float(np.sum(s2))
    if not np.isfinite(tot) or tot <= 0.0:
        # unreachable via svdvals' fallback, but a non-finite spectrum must read VOID and never a
        # number — a NaN that silently averages into an arm is worse than a missing arm.
        return {"n_edge": n_edge, "off_top": None, "eff_rank": None, "stable_rank": None,
                "fro2": 0.0, "void": True}
    off_top = float(1.0 - s2[0] / tot)
    eff_rank = float((tot ** 2) / float(np.sum(s2 ** 2)))
    stable = float(tot / s2[0])
    return {"n_edge": n_edge, "off_top": off_top, "eff_rank": eff_rank,
            "stable_rank": stable, "fro2": tot, "void": False}


# --------------------------------------------------------------------------- #
# numpy reduction / apply (engine-native, torch-free)
# --------------------------------------------------------------------------- #
def reduce_field(tokens, phi, arm="duel", concord="class"):
    """r_i = SUM_j T[i,j] * phi[bucket(j-i)]  ->  (T, rank).

    arm "duel"  — walks the sparse edges, no dense matrix, no SVD.
    arm "rank1" — materializes T, replaces it with its rank-1 approximation, then reduces the SAME
                  way. The reduction code path below is shared on purpose: any difference in the
                  numbers is the field-vs-rank1 variable and nothing else.
    arm "off"   — zeros.
    """
    b = np.asarray(tokens, dtype=np.int64)
    T = int(b.shape[0])
    phi = np.asarray(phi, dtype=np.float64)
    r = np.zeros((T, phi.shape[1]), dtype=np.float64)
    if arm == "off":
        return r
    if arm == "duel":
        rows, cols, vals = tension_edges(b, concord=concord)
        if rows.size == 0:
            return r
        buck = offset_bucket(cols - rows)
        np.add.at(r, rows, vals[:, None] * phi[buck])
        return r
    if arm == "rank1":
        M = rank1_tiebreak(tension_matrix(b))
        nz = np.nonzero(M)
        if nz[0].size == 0:
            return r
        rows, cols = nz
        vals = M[rows, cols]
        buck = offset_bucket(cols - rows)
        np.add.at(r, rows, vals[:, None] * phi[buck])
        return r
    raise ValueError("arm must be one of duel|rank1|off (got %r)" % (arm,))


def tension_apply(x, tokens, tfld, arm="duel", concord=None):
    """Add the write-side residual to a (T, d) embedding block.

    x     : (T, d) embeddings, NOT mutated (a copy is returned when the lane fires)
    tfld  : the trailer dict (phi, W_up, lam, rank, d)
    Passthrough (byte-identical): tfld None · arm "off" · lam == 0.
    """
    if tfld is None or arm == "off":
        return x
    lam = float(np.asarray(tfld["lam"]).reshape(-1)[0])
    if lam == 0.0:
        return x
    if concord is None:
        concord = tfld.get("concord", "class")     # trailer remembers what it was TRAINED with
    r = reduce_field(tokens, tfld["phi"], arm=arm, concord=concord)
    if not np.any(r):
        return x
    dt = x.dtype
    return (np.asarray(x, dtype=np.float64) + lam * (r @ np.asarray(tfld["W_up"],
                                                                    dtype=np.float64))).astype(dt)


# ── "TFLD" trailer codec — LE f32, same idiom as IFAN/MBND/CLMS ──────────────
ARM_CODE = {"off": 0, "duel": 1, "rank1": 2}
ARM_NAME = {0: "off", 1: "duel", 2: "rank1"}

# H_9812 — the concord mode rides the HIGH bits of arm_code so the trailer layout is unchanged and
# every ckpt written before this flag existed keeps decoding exactly as it was trained (those have
# bit 8 clear ⇒ "class", which is what they actually used). A new field means a new byte grammar;
# a spare bit does not.
CONCORD_CODE = {"class": 0x000, "lex": 0x100, "morph": 0x200}
CONCORD_NAME = {v: k for k, v in CONCORD_CODE.items()}
CONCORD_MASK = 0x300


def arm_code_of(arm, concord="class"):
    return ARM_CODE[arm] | CONCORD_CODE[concord]


def split_arm_code(code):
    """(arm_name, concord_name) from a packed arm_code."""
    code = int(code)
    return ARM_NAME.get(code & 0xFF, "?"), CONCORD_NAME.get(code & CONCORD_MASK, "class")


def pack_tfld(w: dict) -> bytes:
    out = bytearray()
    out += TFLD_MAGIC
    out += struct.pack("<IIII", int(w["n_bucket"]), int(w["rank"]), int(w["d"]), int(w["arm_code"]))
    out += np.asarray(w["phi"], dtype="<f4").reshape(-1).tobytes()        # (n_bucket, rank)
    out += np.asarray(w["W_up"], dtype="<f4").reshape(-1).tobytes()       # (rank, d)
    out += np.asarray(w["lam"], dtype="<f4").reshape(-1).tobytes()        # (1,)
    return bytes(out)


def read_tfld(buf: bytes, off: int, d: int):
    """Read a TFLD trailer at `off`. Returns (tfld, new_off) or (None, off) — passthrough-safe on
    absent/short/mismatched, the same guard idiom as read_ifan/read_mbnd."""
    if off < 0 or off + 4 > len(buf) or buf[off:off + 4] != TFLD_MAGIC:
        return None, off
    p = off + 4
    if p + 16 > len(buf):
        return None, off
    n_bucket, rank, d_file, arm_code = struct.unpack_from("<IIII", buf, p)
    p += 16
    if int(d_file) != int(d):
        return None, off                    # a d mismatch is a wrong-model trailer, not ours
    need = (n_bucket * rank + rank * d + 1) * 4
    if p + need > len(buf):
        return None, off

    def take(n, shape):
        nonlocal p
        arr = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy()
        p += n * 4
        return arr

    tfld = {"n_bucket": int(n_bucket), "rank": int(rank), "d": int(d),
            "arm_code": int(arm_code)}
    tfld["arm"], tfld["concord"] = split_arm_code(arm_code)
    tfld["phi"] = take(n_bucket * rank, (n_bucket, rank))
    tfld["W_up"] = take(rank * d, (rank, d))
    tfld["lam"] = float(take(1, (1,))[0])
    return tfld, p


# --------------------------------------------------------------------------- #
# torch training module (DIRECTIONAL) — defined only when torch imports, so inference stays
# torch-free (mirrors core/ifan.py and core/mbnd.py).
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:
    _HAS_TORCH = False

if _HAS_TORCH:

    class TensionFieldLane(_nn.Module):
        """Trains {phi, W_up, lam}. The op order MIRRORS reduce_field/tension_apply for
        2-production parity — a divergence there makes every number from this lane unattributable.

        The FIELD is computed under no_grad from the token bytes: it is structure, not a parameter.
        Nothing in this module can tune the field to be more useful; it can only learn how to read
        the field it is given. That is what keeps `duel` vs `rank1` a one-variable contrast.
        """

        def __init__(self, d, rank=32, lam0=1.0, arm="duel", concord="class"):
            super().__init__()
            if arm not in ARM_CODE:
                raise ValueError("arm must be one of duel|rank1|off (got %r)" % (arm,))
            if concord not in CONCORD_CODE:
                raise ValueError("concord must be class|lex (got %r)" % (concord,))
            self.d, self.rank, self.arm = int(d), int(rank), str(arm)
            self.concord = str(concord)
            self.n_bucket = N_BUCKET
            self.phi = _nn.Parameter(_torch.randn(N_BUCKET, rank) * (rank ** -0.5))
            self.W_up = _nn.Parameter(_torch.randn(rank, d) * (rank ** -0.5))
            self.lam = _nn.Parameter(_torch.tensor(float(lam0)))

        def field_reduce(self, tokens):
            """tokens: (B, T) long -> (B, T, rank). The per-row edge structure is computed on CPU in
            numpy (deterministic, gradient-free) and only the phi lookup carries gradient."""
            dev = self.phi.device
            toks = tokens.detach().to("cpu").numpy()
            B, T = toks.shape
            out = _torch.zeros(B, T, self.rank, device=dev, dtype=self.phi.dtype)
            if self.arm == "off":
                return out
            rowsout = []
            for bi in range(B):
                if self.arm == "duel":
                    rows, cols, vals = tension_edges(toks[bi], concord=self.concord)
                    if rows.size == 0:
                        rowsout.append(None)
                        continue
                else:                                    # rank1 control
                    M = rank1_tiebreak(tension_matrix(toks[bi], concord=self.concord))
                    nzr, nzc = np.nonzero(M)
                    if nzr.size == 0:
                        rowsout.append(None)
                        continue
                    rows, cols, vals = nzr, nzc, M[nzr, nzc]
                buck = _torch.as_tensor(offset_bucket(cols - rows), device=dev, dtype=_torch.long)
                ridx = _torch.as_tensor(np.asarray(rows), device=dev, dtype=_torch.long)
                v = _torch.as_tensor(np.asarray(vals), device=dev, dtype=self.phi.dtype)
                contrib = v.unsqueeze(-1) * self.phi[buck]          # (E, rank)
                rowsout.append(_torch.zeros(T, self.rank, device=dev, dtype=self.phi.dtype)
                               .index_add(0, ridx, contrib))
            stacked = [z if z is not None else
                       _torch.zeros(T, self.rank, device=dev, dtype=self.phi.dtype)
                       for z in rowsout]
            return _torch.stack(stacked, dim=0)

        def residual(self, tokens):
            """-> (B, T, d) additive PRE-TRUNK embedding delta."""
            return self.lam * (self.field_reduce(tokens) @ self.W_up)

    def tfld_weights_from_torch(mod) -> dict:
        with _torch.no_grad():
            return {
                "n_bucket": int(mod.n_bucket), "rank": int(mod.rank), "d": int(mod.d),
                "arm_code": int(arm_code_of(mod.arm, getattr(mod, "concord", "class"))),
                "phi": mod.phi.detach().float().cpu().numpy(),
                "W_up": mod.W_up.detach().float().cpu().numpy(),
                "lam": np.asarray([float(mod.lam.detach())], dtype=np.float32),
            }
