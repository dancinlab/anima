# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 `anima-py` 단일진입만 사용한다.
# 이 파일을 `python3 core/DECODER/flame_mm.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ flame_mm.py 직접 실행 금지 — canonical `anima-py` 경유. #2603")

"""core/DECODER/flame_mm.py — canonical Python GEMM dispatch seam.

This module is the NumPy foundation used by both supported decode mouths.

  * RFC-040 primitives mirrored:
      farr_matmul(A, M, K, B, N)           CPU oracle (ikj k-ascending, runtime.c:8418)
      farr_matmul_gpu(A, M, K, B, N)       cuBLAS Dgemm (CUDA host only)
      cuda_available()                      → 1 on CUDA host, else 0
      farr_copy_slice_gpu(P,off,out,0,n)   memcpy/D2D of n doubles

Convention (from flame_mm.hexa lines 16-17):
  A[M×K] @ B[K×N] = C[M×N], row-major. NO transpose variant in the underlying
  farr_matmul — transposes are explicit (mm_transpose).

All buffers are 1-D numpy float64 arrays (matching farr = C double per runtime.c).

Parity level: max|Δ| ≈ 1e-13 on the mm() GEMM (numpy BLAS vs hexa ikj scalar;
identical at ~12 dp). All other ops (mm_transpose, mm_extract, mm_scatter_add,
mm_packed_gemv, mm_packed_gemv_t, mm_packed_outer_add) are pure scalar loops
that are ULP=0 vs the hexa source.

NO torch — numpy float64 only (same as clm_decode.py / bytegpt_decode.py mirrors).
"""

import numpy as np


# ════════════════════════════════════════════════════════════════════════
# mm(A, M, K, B, N) → C[M×N]
# flame_mm.hexa lines 26-31
#
# hexa: if cuda_available() == 1 { farr_matmul_gpu(A,M,K,B,N) }
#       else { farr_matmul(A,M,K,B,N) }
#
# py: no CUDA; always use the CPU oracle (numpy float64 matmul ≈ ikj).
# hexa CPU oracle = ikj loop ascending k (runtime.c:8418); numpy BLAS differs
# only at ~1e-13 ULP — inside the parity gate (identical argmax + CE ≥4dp).
# ════════════════════════════════════════════════════════════════════════

def mm(A, M, K, B, N):
    """A[M×K] @ B[K×N] → C[M×N], all 1-D float64.
    Mirrors flame_mm.hexa::mm (CPU path; GPU dispatch not available in py)."""
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    C = A.reshape(M, K) @ B.reshape(K, N)
    return C.reshape(-1).astype(np.float64, copy=False)


# ════════════════════════════════════════════════════════════════════════
# mm_transpose(A, rows, cols) → At[cols×rows]
# flame_mm.hexa lines 35-47
#
# hexa: At[c*rows + r] = A[r*cols + c]   (explicit element-wise swap)
# py:   numpy reshape + .T + ravel — semantically identical, ULP=0.
# ════════════════════════════════════════════════════════════════════════

def mm_transpose(A, rows, cols):
    """Explicit row-major transpose. At[c*rows+r] = A[r*cols+c].
    Mirrors flame_mm.hexa::mm_transpose (lines 35-47). ULP=0."""
    A = np.asarray(A, dtype=np.float64)
    return A.reshape(rows, cols).T.ravel().astype(np.float64, copy=False)


# ════════════════════════════════════════════════════════════════════════
# mm_extract(P, off, rows, cols) → out[rows*cols]
# flame_mm.hexa lines 62-67
#
# M5-ADOPT (anima 2026-05-29): scalar farr_get/farr_set loop replaced by
# farr_copy_slice_gpu(P, off, out, 0, n) — semantics unchanged: memcpy of
# n=rows*cols doubles starting at P[off]. py: slice copy.
# ════════════════════════════════════════════════════════════════════════

def mm_extract(P, off, rows, cols):
    """Copy sub-block P[off:off+rows*cols] into a fresh flat float64 array.
    Mirrors flame_mm.hexa::mm_extract (lines 62-67). ULP=0."""
    P = np.asarray(P, dtype=np.float64)
    n = rows * cols
    return P[off:off + n].copy()


# ════════════════════════════════════════════════════════════════════════
# mm_scatter_add(P, off, src, n) — in-place, returns None
# flame_mm.hexa lines 72-78
#
# hexa: P[off+i] += src[i]  for i in [0,n)
# py:   P[off:off+n] += src[:n]   — in-place on the passed array (mutable).
# ════════════════════════════════════════════════════════════════════════

def mm_scatter_add(P, off, src, n):
    """P[off:off+n] += src[0:n], in-place (float64).
    Mirrors flame_mm.hexa::mm_scatter_add (lines 72-78). ULP=0."""
    src = np.asarray(src, dtype=np.float64)
    P[off:off + n] += src[:n]


# ════════════════════════════════════════════════════════════════════════
# mm_packed_gemv(P, off, rows, cols, u) → out[rows]
# flame_mm.hexa lines 105-120
#
# out[i] = Σ_j P[off + i*cols + j] * u[j]   for i∈[0,rows), j∈[0,cols)
# Fused gemv: reads packed sub-block directly, no intermediate copy.
# py: slice the packed region then matmul.
# ════════════════════════════════════════════════════════════════════════

def mm_packed_gemv(P, off, rows, cols, u):
    """out[i] = Σ_j P[off + i*cols + j] * u[j]. Fused, no copy alloc.
    Mirrors flame_mm.hexa::mm_packed_gemv (lines 105-120)."""
    P = np.asarray(P, dtype=np.float64)
    u = np.asarray(u, dtype=np.float64)
    block = P[off:off + rows * cols].reshape(rows, cols)
    return (block @ u).astype(np.float64, copy=False)


# ════════════════════════════════════════════════════════════════════════
# mm_packed_gemv_t(P, off, rows, cols, v) → out[cols]
# flame_mm.hexa lines 136-151
#
# out[j] = Σ_i P[off + i*cols + j] * v[i]   for i∈[0,rows), j∈[0,cols)
# Transposed fused gemv: A^T * v, no intermediate allocations.
# py: slice + reshape + .T @ v (or block.T @ v).
# ════════════════════════════════════════════════════════════════════════

def mm_packed_gemv_t(P, off, rows, cols, v):
    """out[j] = Σ_i P[off + i*cols + j] * v[i]. Transposed fused gemv.
    Mirrors flame_mm.hexa::mm_packed_gemv_t (lines 136-151)."""
    P = np.asarray(P, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    block = P[off:off + rows * cols].reshape(rows, cols)
    return (block.T @ v).astype(np.float64, copy=False)


# ════════════════════════════════════════════════════════════════════════
# mm_packed_outer_add(P, off, u, v, rows, cols) — in-place, returns None
# flame_mm.hexa lines 166-179
#
# P[off + i*cols + j] += u[i] * v[j]   for i∈[0,rows), j∈[0,cols)
# Rank-1 outer product accumulation directly into packed buffer.
# py: np.outer then in-place add into sliced region.
# ════════════════════════════════════════════════════════════════════════

def mm_packed_outer_add(P, off, u, v, rows, cols):
    """P[off + i*cols + j] += u[i]*v[j], in-place (float64). Rank-1 outer add.
    Mirrors flame_mm.hexa::mm_packed_outer_add (lines 166-179). ULP=0."""
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    outer = np.outer(u, v)  # shape (rows, cols)
    P[off:off + rows * cols] += outer.ravel()


# ════════════════════════════════════════════════════════════════════════
# Self-verify parity gate (run as script)
# ════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    RNG = np.random.default_rng(42)

    def _rng(n):
        return RNG.standard_normal(n).astype(np.float64)

    PASS = True

    # ── mm parity test via reference ────────────────────────────────────
    # A[3×4] @ B[4×5] = C[3×5]
    M, K, N = 3, 4, 5
    A = _rng(M * K)
    B = _rng(K * N)
    C_py = mm(A, M, K, B, N)
    # reference: naive ikj (matches hexa CPU oracle exactly)
    C_ref = np.zeros(M * N, dtype=np.float64)
    for i in range(M):
        for k in range(K):
            for j in range(N):
                C_ref[i * N + j] += A[i * K + k] * B[k * N + j]
    delta_mm = np.max(np.abs(C_py - C_ref))
    ok = delta_mm < 1e-10
    PASS = PASS and ok
    print(f"mm:                 max|Δ|={delta_mm:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_transpose ────────────────────────────────────────────────────
    rows, cols = 3, 4
    A2 = _rng(rows * cols)
    At = mm_transpose(A2, rows, cols)
    At_ref = np.zeros(cols * rows, dtype=np.float64)
    for r in range(rows):
        for c in range(cols):
            At_ref[c * rows + r] = A2[r * cols + c]
    delta_T = np.max(np.abs(At - At_ref))
    ok = delta_T == 0.0
    PASS = PASS and ok
    print(f"mm_transpose:       max|Δ|={delta_T:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_extract ──────────────────────────────────────────────────────
    P = _rng(100)
    off, er, ec = 7, 3, 4
    out_e = mm_extract(P, off, er, ec)
    ref_e = P[off:off + er * ec].copy()
    delta_e = np.max(np.abs(out_e - ref_e))
    ok = delta_e == 0.0
    PASS = PASS and ok
    print(f"mm_extract:         max|Δ|={delta_e:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_scatter_add ──────────────────────────────────────────────────
    P2 = _rng(50)
    P2_ref = P2.copy()
    src = _rng(10)
    soff = 5
    mm_scatter_add(P2, soff, src, 10)
    P2_ref[soff:soff + 10] += src
    delta_sa = np.max(np.abs(P2 - P2_ref))
    ok = delta_sa == 0.0
    PASS = PASS and ok
    print(f"mm_scatter_add:     max|Δ|={delta_sa:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_packed_gemv ──────────────────────────────────────────────────
    P3 = _rng(200)
    u = _rng(5)
    gr, gc = 4, 5
    goff = 11
    out_gv = mm_packed_gemv(P3, goff, gr, gc, u)
    ref_gv = np.zeros(gr, dtype=np.float64)
    for i in range(gr):
        for j in range(gc):
            ref_gv[i] += P3[goff + i * gc + j] * u[j]
    delta_gv = np.max(np.abs(out_gv - ref_gv))
    ok = delta_gv < 1e-13
    PASS = PASS and ok
    print(f"mm_packed_gemv:     max|Δ|={delta_gv:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_packed_gemv_t ────────────────────────────────────────────────
    v = _rng(gr)
    out_gvt = mm_packed_gemv_t(P3, goff, gr, gc, v)
    ref_gvt = np.zeros(gc, dtype=np.float64)
    for i in range(gr):
        for j in range(gc):
            ref_gvt[j] += P3[goff + i * gc + j] * v[i]
    delta_gvt = np.max(np.abs(out_gvt - ref_gvt))
    ok = delta_gvt < 1e-13
    PASS = PASS and ok
    print(f"mm_packed_gemv_t:   max|Δ|={delta_gvt:.2e}  {'PASS' if ok else 'FAIL'}")

    # ── mm_packed_outer_add ─────────────────────────────────────────────
    P4 = _rng(200)
    P4_ref = P4.copy()
    u2 = _rng(gr)
    v2 = _rng(gc)
    mm_packed_outer_add(P4, goff, u2, v2, gr, gc)
    for i in range(gr):
        for j in range(gc):
            P4_ref[goff + i * gc + j] += u2[i] * v2[j]
    delta_oa = np.max(np.abs(P4 - P4_ref))
    ok = delta_oa < 1e-13
    PASS = PASS and ok
    print(f"mm_packed_outer_add: max|Δ|={delta_oa:.2e}  {'PASS' if ok else 'FAIL'}")

    print()
    if PASS:
        print("ALL PASS — flame_mm.py parity gate PASS")
    else:
        print("FAIL — see above")
        sys.exit(1)
