"""core/ifan.py — H_9803 BRANCH-LATENT ideation-fan lane ("IFAN" trailer), CORE-owned SSOT.

WHY THIS EXISTS, in one line: every previous attempt at ρ·fan (G6) diversity put a knob on ONE
next-byte distribution (temperature / top-k / an entropy bonus / a cosine-repulsion penalty), and
each of those is a SAMPLING TRICK — it widens the same distribution instead of representing several
different futures. This lane refuses that class BY CONSTRUCTION.

The construction
----------------
From a PRESERVED early tap (trunk layer L, default 3 — the H_9720 tap-DEPTH result: the early layer
still carries content that the penultimate has already collapsed) we build K proposal latents

    z_k = tanh( tap[fork] @ W_in[k] )            k = 0..K-1   ★ W_in[k] are DISJOINT blocks

All K read the SAME fork-point tap, so every branch gets IDENTICAL topic grounding. Nothing here
pushes them apart. What differentiates them is entirely the training signal (below).

Each branch then perturbs the mouth multiplicatively, at every continuation position t:

    g_k(t) = tanh( h_t @ W_h ) ⊙ z_k            ★ Hadamard — the branch latent GATES the running state
    s_k(t) = g_k(t) @ W_out
    logits_k(t) = logits(t) + λ · s_k(t)

`h_t` is the ordinary pre-readout penultimate, so the branch never sees anything the trunk did not
see, and the branch identity `z_k` is computed from the CONTEXT ONLY (position `fork`). That is
load-bearing: if `z_k` were recomputed from positions inside the continuation, a branch could read
off WHICH continuation it is being scored against, and the set-CE below would be solvable by
target-identification rather than by mode-commitment.

Where the diversity comes from (the whole hypothesis)
----------------------------------------------------
The training target is not one continuation but a SET of M real continuations observed after the
same context/topic in the corpus. Per document we build the cost matrix

    C[k][m] = mean CE of the m-th OBSERVED continuation under branch k's logits

and solve a min-cost (Hungarian) assignment σ, then minimise  (1/K) Σ_k C[k][σ(k)].

Because the assignment is a MATCHING, two branches cannot both claim the same observed future — but
crucially the pressure that separates them is "explain a DIFFERENT REAL continuation", never a
push-apart term. There is no repulsion, no entropy bonus, no diversity regulariser anywhere in this
file; grep it. If the K branches collapse onto one mode the set-CE goes UP because the unclaimed
observed futures are still in the sum. Diversity is therefore GROUNDED in observed future modes: it
is a consequence of the corpus containing several real continuations, not of an ungrounded prior.

The negative control that makes the claim readable
--------------------------------------------------
`assign="shuffle"` (train) / `--fan-branch assignment-shuffle` (eval) keeps EVERYTHING — same K, same
targets, same parameter count, same total CE mass — and only destroys the branch↔target
correspondence (train: reshuffle σ every batch; eval: read branch k's latent through branch π(k)'s
output block). If the lane were a sampling trick, K arbitrary directions are exchangeable and the
shuffle costs nothing. Only a lane whose branch identity actually carries a specific future mode
collapses under it. That control is the reason the mechanism is falsifiable at all.

DISJOINT (a_substrate_disjoint): its own file, its own trailer, additive at the logits, appended
after MBND. Absent trailer OR lane switch off ⇒ ifan_apply returns the caller's array unchanged ⇒
byte-identical to the base decode (the `--fan-branch off` parity arm asserts exactly this).
"""

from __future__ import annotations

import struct
import numpy as np

IFAN_MAGIC = bytes([73, 70, 65, 78])   # "IFAN" — chain CLMB→SLW→CLML→CLMS→MBND→IFAN


# --------------------------------------------------------------------------- #
# min-cost assignment (Hungarian / Jonker-Volgenant, O(n^3)) — pure python, no scipy.
# Deterministic (no RNG, no tie-break by hash) so a set-CE number is reproducible.
# --------------------------------------------------------------------------- #
def min_cost_assignment(cost) -> list:
    """cost: (n, m) array-like with n <= m. Returns ass[i] = the column matched to row i.

    Pure O(n^2 m) JV shortest-augmenting-path. n,m are the branch/target counts (single digits
    in every planned arm), so the python loop is not on any hot path."""
    C = np.asarray(cost, dtype=np.float64)
    n, m = C.shape
    if n > m:
        raise ValueError("min_cost_assignment needs n <= m (branches <= targets); pad first")
    INF = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (m + 1)
    p = [0] * (m + 1)          # p[j] = row matched to column j (0 = free)
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = -1
            for j in range(1, m + 1):
                if used[j]:
                    continue
                cur = C[i0 - 1, j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0
                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j
            for j in range(0, m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    ass = [-1] * n
    for j in range(1, m + 1):
        if p[j] != 0:
            ass[p[j] - 1] = j - 1
    return ass


# --------------------------------------------------------------------------- #
# numpy decode-side apply (engine-native, torch-free)
# --------------------------------------------------------------------------- #
def ifan_apply(logits, yn, tap, ifan, branch=0, mode="live", perm_seed=9803, last_only=False,
               fork=None):
    """Apply the branch-latent ideation fan.

    logits : (T, V) base logits (NOT mutated — a copy is returned when the lane fires)
    yn     : (T, d) pre-readout trunk penultimate (the SAME tap CLML/CLMS/MBND read)
    tap    : (T, d) preserved EARLY (layer-L) trunk tap; None ⇒ fall back to `yn` (the
             `penult` route = the H_9720-C1-style tap-DEPTH control, NOT the l3 route)
    branch : which of the K proposal latents drives this decode
    mode   : "live"                — branch k reads its own W_in[k] / W_out[k]        (treatment)
             "assignment-shuffle"  — branch k's latent is read out through branch π(k)'s
                                     output block; K, params and λ are untouched      (control)
             "off"                 — return `logits` UNCHANGED, no copy, no arithmetic (parity arm)
    fork   : index of the fork point (last CONTEXT position). None ⇒ T-1. The branch latent is
             computed ONLY from tap[fork] so it stays context-grounded; a sliding decode window
             clamps it to 0 once the seed has scrolled out.

    Passthrough (byte-identical): ifan None · mode "off" · λ==0 · T<1.
    """
    if ifan is None or mode == "off":
        return logits
    lam = float(np.asarray(ifan["lam"]).reshape(-1)[0])
    if lam == 0.0:
        return logits
    T = int(len(yn))
    if T < 1:
        return logits
    K = int(ifan["K"])
    k = int(branch) % K
    src = tap if tap is not None else yn
    f = (T - 1) if fork is None else int(fork)
    if f < 0:
        f = 0
    if f > T - 1:
        f = T - 1
    # branch identity: the proposal latent, read from the CONTEXT fork point only.
    z = np.tanh(np.asarray(src[f], dtype=np.float64) @ ifan["W_in"][k])          # (r,)
    # the readout block. "live" = k's own; "assignment-shuffle" = a derangement-style fixed
    # permutation of the OUTPUT blocks, so branch identity is re-paired while nothing else moves.
    k_out = k
    if mode == "assignment-shuffle":
        perm = np.random.default_rng(int(perm_seed)).permutation(K)
        k_out = int(perm[k])
    W_out = ifan["W_out"][k_out]                                                 # (r, V)
    dt = logits.dtype
    out = logits.copy()
    rows = (T - 1,) if last_only else range(T)
    for t in rows:
        g = np.tanh(np.asarray(yn[t], dtype=np.float64) @ ifan["W_h"]) * z       # (r,) Hadamard
        out[t] = (logits[t] + lam * (g @ W_out)).astype(dt)
    return out


# ── "IFAN" trailer codec — LE f32, same idiom as MBND/CLMS ───────────────────
def pack_ifan(w: dict) -> bytes:
    out = bytearray()
    out += IFAN_MAGIC
    out += struct.pack("<IIIII", int(w["K"]), int(w["rank"]), int(w["d"]), int(w["V"]),
                       int(w.get("route_L", 3)))
    out += np.asarray(w["W_in"], dtype="<f4").reshape(-1).tobytes()       # (K, d, r)
    out += np.asarray(w["W_h"], dtype="<f4").reshape(-1).tobytes()        # (d, r)
    out += np.asarray(w["W_out"], dtype="<f4").reshape(-1).tobytes()      # (K, r, V)
    out += np.asarray(w["lam"], dtype="<f4").reshape(-1).tobytes()        # (1,)
    return bytes(out)


def read_ifan(buf: bytes, off: int, d: int, V: int):
    """Read an IFAN trailer at `off`. Returns (ifan, new_off) or (None, off) — passthrough-safe
    on absent/short/mismatched, the same guard idiom as read_mbnd/read_clms."""
    if off < 0 or off + 4 > len(buf) or buf[off:off + 4] != IFAN_MAGIC:
        return None, off
    p = off + 4
    if p + 20 > len(buf):
        return None, off
    K, rank, d_file, V_file, route_L = struct.unpack_from("<IIIII", buf, p)
    p += 20
    if int(d_file) != int(d) or int(V_file) != int(V):
        return None, off                    # a d/V mismatch is a wrong-model trailer, not ours
    need = (K * d * rank + d * rank + K * rank * V + 1) * 4
    if p + need > len(buf):
        return None, off

    def take(n, shape):
        nonlocal p
        arr = np.frombuffer(buf, "<f4", n, p).reshape(shape).copy()
        p += n * 4
        return arr

    ifan = {"K": int(K), "rank": int(rank), "d": int(d), "V": int(V), "route_L": int(route_L)}
    ifan["W_in"] = take(K * d * rank, (K, d, rank))
    ifan["W_h"] = take(d * rank, (d, rank))
    ifan["W_out"] = take(K * rank * V, (K, rank, V))
    ifan["lam"] = float(take(1, (1,))[0])
    return ifan, p


# --------------------------------------------------------------------------- #
# torch training module (DIRECTIONAL) — defined only when torch imports, so inference stays
# torch-free (mirrors core/mbnd.py's guard).
# --------------------------------------------------------------------------- #
try:
    import torch as _torch
    import torch.nn as _nn
    _HAS_TORCH = True
except Exception:
    _HAS_TORCH = False

if _HAS_TORCH:

    class BranchLatentFan(_nn.Module):
        """Trains {W_in[K], W_h, W_out[K], λ}. The op order MIRRORS ifan_apply for 2-production
        parity — a divergence there makes every number from this lane unattributable.

        NOTE what is NOT in this module: no repulsion term, no entropy bonus, no diversity
        regulariser, no temperature. The ONLY thing that separates the branches is the set-level
        assignment in `set_ce_loss`, which is grounded in several REAL observed continuations.
        """

        def __init__(self, d, V, K=4, rank=64, lam0=1.0, route_L=3):
            super().__init__()
            self.d, self.V, self.K, self.rank, self.route_L = d, V, int(K), int(rank), int(route_L)
            self.W_in = _nn.Parameter(_torch.randn(self.K, d, rank) * (d ** -0.5))
            self.W_h = _nn.Parameter(_torch.randn(d, rank) * (d ** -0.5))
            self.W_out = _nn.Parameter(_torch.randn(self.K, rank, V) * (rank ** -0.5))
            self.lam = _nn.Parameter(_torch.tensor(float(lam0)))

        def branch_latents(self, tap_fork):
            """tap_fork: (B, d) the EARLY-tap row at the fork point (context-only, already
            detached by the caller on the l3-disjoint route). -> (B, K, r)."""
            return _torch.tanh(_torch.einsum("bd,kdr->bkr", tap_fork, self.W_in))

        def residual(self, yn, z):
            """yn: (B, T, d) running penultimate · z: (B, K, r) -> (B, K, T, V) logit delta."""
            gh = _torch.tanh(yn @ self.W_h)                       # (B, T, r)
            g = gh.unsqueeze(1) * z.unsqueeze(2)                  # (B, K, T, r) Hadamard gate
            return self.lam * _torch.einsum("bktr,krv->bktv", g, self.W_out)

    def ifan_weights_from_torch(mod) -> dict:
        with _torch.no_grad():
            return {
                "K": int(mod.K), "rank": int(mod.rank), "d": int(mod.d), "V": int(mod.V),
                "route_L": int(mod.route_L),
                "W_in": mod.W_in.detach().float().cpu().numpy(),
                "W_h": mod.W_h.detach().float().cpu().numpy(),
                "W_out": mod.W_out.detach().float().cpu().numpy(),
                "lam": np.asarray([float(mod.lam.detach())], dtype=np.float32),
            }

    def set_ce_loss(base_logits, ifan_mod, tap_fork, yn, targets, mask, assign="hungarian",
                    shuffle_gen=None):
        """The H_9803 SET-level CE with min-cost branch↔target assignment.

        base_logits : (M, T, V)  base mouth logits for the M observed continuations
        tap_fork    : (M, d)     early-tap fork row — IDENTICAL topic grounding for every branch
                                 (the caller passes the CONTEXT row, broadcast over M)
        yn          : (M, T, d)  running penultimate for each observed continuation
        targets     : (M, T)     the M REAL observed continuations (next-byte ids)
        mask        : (M, T)     1 on continuation positions, 0 on context/pad
        assign      : "hungarian" = min-cost matching (treatment)
                      "shuffle"   = a random permutation redrawn EVERY call (the negative control:
                                    same K, same targets, same CE mass — only the correspondence
                                    is destroyed)

        Returns (loss, aux) where aux is MONITOR-ONLY (a_train_inline_gauge — nothing in aux is
        ever added back into the loss).
        """
        M, T, V = base_logits.shape
        K = ifan_mod.K
        z = ifan_mod.branch_latents(tap_fork)                     # (M, K, r)
        # every branch reads the SAME fork grounding, so collapse the M axis to branch 0's row set:
        # residual for branch k evaluated against target m needs yn of sequence m -> keep (M,K,T,V).
        delta = ifan_mod.residual(yn, z)                          # (M, K, T, V)
        logits_kb = base_logits.unsqueeze(1) + delta              # (M, K, T, V)
        lsm = _torch.log_softmax(logits_kb.float(), dim=-1)
        tgt = targets.unsqueeze(1).expand(M, K, T).unsqueeze(-1)  # (M,K,T,1)
        nll = -lsm.gather(-1, tgt).squeeze(-1)                    # (M, K, T)
        w = mask.unsqueeze(1).float()                             # (M, 1, T)
        denom = w.sum(dim=-1).clamp_min(1.0)                      # (M, 1)
        ce_km = (nll * w).sum(dim=-1) / denom                     # (M, K) = CE of target m under k
        cost = ce_km.transpose(0, 1)                              # (K, M)
        n = min(K, M)
        with _torch.no_grad():
            Cn = cost[:n, :].detach().float().cpu().numpy()
            if assign == "shuffle":
                # NEGATIVE CONTROL — the correspondence is randomised anew every batch. Note it is a
                # PERMUTATION, not random independent picks: the multiset of (branch, target) pairs
                # and hence the CE mass class is preserved; only WHICH branch owns WHICH observed
                # future is destroyed.
                g = shuffle_gen if shuffle_gen is not None else _torch.Generator()
                sel = _torch.randperm(M, generator=g)[:n].tolist()
            else:
                sel = min_cost_assignment(Cn)
        idx = _torch.tensor(sel, dtype=_torch.long, device=cost.device)
        picked = cost[_torch.arange(n, device=cost.device), idx]  # (n,)
        loss = picked.mean()
        aux = {
            "ifan_set_ce": float(loss.detach()),
            "ifan_mean_ce": float(cost.mean().detach()),          # monitor: unassigned average
            "ifan_worst_ce": float(cost.max().detach()),
            "ifan_n_distinct_tgt": float(len(set(sel))),          # monitor: assignment spread
            "ifan_lam": float(ifan_mod.lam.detach()),
        }
        return loss, aux
