#!/usr/bin/env python3
# ==========================================================================
# core/wm_bind_lane.py — L1 PFC WORKING-MEMORY VARIABLE-BINDING lane (numpy 2-prod).
#
# H_9129 integrated rung-3 (PFC × basal-ganglia × hippocampus).  A DISJOINT
# role⊛filler binding lane over anima representations. Holographic Reduced
# Representation (Plate, HRR): circular-convolution binds a role vector with a
# filler vector into a DIM-preserving trace; superposition folds many bindings
# into ONE activation vector M; correlation (involution) unbinds a noisy filler
# that a codebook cleanup denoises to the nearest known filler cell.
#
# a_substrate_disjoint: this is a READ-ONLY workspace lane. It owns ONLY its own
# WMBind state — it NEVER writes the emit-drive lane (Ψ / motivation / recall_thr
# / generator / brain / lanes[0]/[4]). It is a NEW file imported by NO emit
# consumer, so adding/consulting it cannot change generation bytes (separation =
# preservation). Byte-parity hexa twin = core/kosmos_io.hexa (wmbind_cconv /
# wmbind_cinv / wmbind_superpose / wmbind_unbind / wmbind_cleanup_idx).
#
# The lane objective is unbind-reconstruction fidelity — a pure algebraic
# self-supervised signal DISJOINT from the mouth CE (no shared gradient tape),
# so the H_1816 form-priming collapse is structurally impossible here.
#
# Role/filler/item vectors are the REAL ByteGPT-303M reps supplied by the
# py-canonical path (core/decode.py == anima evaluate --py ops). The binding
# ALGEBRA is fixed HRR (untrained) — honest scope: this is an explicit
# variable-binding FACULTY over trunk reps, NOT a proof the trunk composes.
# ==========================================================================
import numpy as np


def unit(v):
    v = np.asarray(v, dtype=np.float64)
    return v / (np.linalg.norm(v) + 1e-9)


# ── HRR primitives (circular convolution / correlation) ─────────────────────
def hrr_bind(r, f):
    """Circular convolution c = r ⊛ f ; c[i] = Σ_j r[j]·f[(i-j) mod D].
    Direct O(D^2) form (matches the hexa twin exactly, no FFT rounding drift)."""
    r = np.asarray(r, dtype=np.float64)
    f = np.asarray(f, dtype=np.float64)
    D = r.shape[0]
    out = np.zeros(D)
    for i in range(D):
        s = 0.0
        for j in range(D):
            s += r[j] * f[(i - j) % D]
        out[i] = s
    return out


def hrr_unbind(r, m):
    """Circular correlation with the involution r*[i]=r[(-i) mod D]:
    f_hat[i] = Σ_j r[j]·m[(i+j) mod D]. Recovers a noisy filler from M."""
    r = np.asarray(r, dtype=np.float64)
    m = np.asarray(m, dtype=np.float64)
    D = r.shape[0]
    out = np.zeros(D)
    for i in range(D):
        s = 0.0
        for j in range(D):
            s += r[j] * m[(i + j) % D]
        out[i] = s
    return out


def hrr_superpose(roles, fillers, strengths=None):
    """WM activation M = Σ_k a_k · (unit(role_k) ⊛ unit(filler_k)). One volatile
    DIM vector holding many role↔filler bindings — the PFC superposition buffer.
    Crosstalk grows with the number superposed ⇒ genuine WM capacity limit."""
    roles = np.asarray(roles, dtype=np.float64)
    fillers = np.asarray(fillers, dtype=np.float64)
    n, D = roles.shape
    if strengths is None:
        strengths = np.ones(n)
    M = np.zeros(D)
    for k in range(n):
        M += strengths[k] * hrr_bind(unit(roles[k]), unit(fillers[k]))
    return M


def cleanup_idx(fhat, codebook):
    """Denoise a noisy unbound filler to the nearest codebook cell (cosine).
    Returns (winning index, cosine) — the cleanup memory / attractor."""
    fhat = unit(fhat)
    C = np.asarray(codebook, dtype=np.float64)
    Cn = C / (np.linalg.norm(C, axis=1, keepdims=True) + 1e-9)
    sims = Cn @ fhat
    return int(np.argmax(sims)), float(np.max(sims))


def recon_fidelity(roles, fillers, codebook, gold_idx):
    """★ DISJOINT lane objective: bind all (role_k,filler_k) into ONE M, then per
    role unbind+cleanup — fraction landing on the gold filler cell. Pure algebra,
    no mouth CE. Shuffling roles must collapse it (binding-is-causal ablation)."""
    M = hrr_superpose(roles, fillers)
    hit = 0
    for k in range(roles.shape[0]):
        fhat = hrr_unbind(unit(roles[k]), M)
        idx, _ = cleanup_idx(fhat, codebook)
        if idx == gold_idx[k]:
            hit += 1
    return hit / max(1, roles.shape[0])


# ── deterministic integer fixture (byte-parity oracle for the hexa twin) ────
def fixture_vecs(n, dim, seed):
    """Deterministic dense pseudo-random vectors WITHOUT float RNG divergence:
    v[i,b] = ((lcg stream) mod 2001 - 1000)/1000 — pure integer construction so
    hexa and py agree byte-for-byte over the whole bind/unbind/cleanup pipeline."""
    V = np.zeros((n, dim), dtype=np.float64)
    for i in range(n):
        h = (i * 2654435761 + seed) & 0xFFFFFFFF
        for b in range(dim):
            h = (h * 1664525 + 1013904223) & 0xFFFFFFFF
            V[i, b] = ((h % 2001) - 1000) / 1000.0
    return V


def _fixture_report():
    """Deterministic small HRR bind/unbind/cleanup report for hexa byte-parity.
    4 roles ⊛ 4 fillers superposed into one M; each role must unbind→cleanup to
    its own filler (recon), and a shuffled-role read must degrade."""
    N, DIM, SEED = 4, 64, 20260705
    roles = fixture_vecs(N, DIM, SEED)
    fillers = fixture_vecs(N, DIM, SEED + 777)
    gold = list(range(N))
    fid = recon_fidelity(roles, fillers, fillers, gold)
    print("py recon_fidelity=%.6f" % fid)
    M = hrr_superpose(roles, fillers)
    fhat0 = hrr_unbind(unit(roles[0]), M)
    idx0, sim0 = cleanup_idx(fhat0, fillers)
    print("py unbind0_idx=%d" % idx0)
    print("py unbind0_sim=%.6f" % sim0)
    fhat_sh = hrr_unbind(unit(roles[1]), M)
    idx_sh, _ = cleanup_idx(fhat_sh, fillers)
    print("py shuffle0_idx=%d" % idx_sh)


if __name__ == "__main__":
    _fixture_report()
