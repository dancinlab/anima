/* runtime_cuda.c — anima RFC 040 Phase A real-cuBLAS impl.
 *
 * Provides the `_hx_cuda_*` TU forward-decl'd by hexa-lang self/runtime.c
 * under `#ifdef HEXA_CUDA`. When the host has a CUDA toolkit, this TU
 * compiles + links with `-lcudart -lcublas`, giving farr_matmul_gpu a
 * real cuBLAS Dgemm body. On a no-CUDA host this file is simply not
 * compiled (the no-CUDA build is byte-identical to today).
 *
 * Math contract — same as RFC 032 farr_matmul:
 *   A row-major M×K, B row-major K×N, C row-major M×N.
 *   Reproducible bit-identity is NOT claimed (cuBLAS reduces in a
 *   different order than the CPU ikj scalar loop, fp non-associativity).
 *   Tolerance: |Δ| < ~1e-9 for Dgemm — matches RFC 040 §"Honest caveats"
 *   TOL_MATMUL guess; this fire measures and reports the actual max |Δ|.
 *
 * cuBLAS is column-major. Our farr is row-major. We map row-major
 * C = A·B to cuBLAS column-major by computing:
 *   C^T_col = B^T_col · A^T_col
 * which in cuBLAS column-major terms (treating row-major A as col-major
 * A^T) is: `cublasDgemm(handle, N, N, N=cols_out, M=rows_out, K, alpha,
 * B_dev, ldb=N, A_dev, lda=K, beta, C_dev, ldc=N)`.
 *
 * Device-farr coordination: we own a tiny device-side mirror table keyed
 * by farr_id. Operands are uploaded H2D on demand (when not already
 * resident) and outputs allocated device-side. The runtime.c side keeps
 * `dirty_host=1` / `loc=FARR_DEVICE` to track residence; this TU does
 * the actual cudaMalloc / cudaMemcpy calls.
 *
 * Honest reporting: every error path returns -1 + a one-line stderr
 * message naming the failure. No silent fallbacks; no fake CUDA results.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include <cuda_runtime.h>
#include <cublas_v2.h>

/* Tiny device-side mirror table. Keyed by farr_id (same int handle the
 * runtime.c HexaFarrEntry table uses). Sparse: grows on demand. */
typedef struct {
    double*  d_buf;       /* cudaMalloc'd device pointer, or NULL */
    int64_t  len;         /* element count (must match host len when valid) */
} _CudaFarrSlot;

static _CudaFarrSlot* g_slots     = NULL;
static int64_t        g_slot_cap  = 0;

static int _ensure_slot_cap(int64_t id) {
    if (id < 0) return -1;
    if (id < g_slot_cap) return 0;
    int64_t new_cap = g_slot_cap < 16 ? 16 : g_slot_cap;
    while (new_cap <= id) new_cap *= 2;
    _CudaFarrSlot* ns = (_CudaFarrSlot*)realloc(g_slots,
                            (size_t)new_cap * sizeof(_CudaFarrSlot));
    if (!ns) { fprintf(stderr, "[cuda] OOM slot table\n"); return -1; }
    /* zero-init the new tail. */
    for (int64_t i = g_slot_cap; i < new_cap; i++) {
        ns[i].d_buf = NULL;
        ns[i].len   = 0;
    }
    g_slots = ns;
    g_slot_cap = new_cap;
    return 0;
}

/* Forward decls — these live in self/runtime.c. We access the host
 * HexaFarrEntry table to read host buf + len for H2D + D2H. */
typedef struct {
    double*  buf;
    int64_t  len;
    void*    d_buf;       /* runtime.c side device-ptr slot (we mirror) */
    int      loc;
    int      pinned;
    int      dirty_host;
    int      dirty_dev;
} HexaFarrEntry;
extern HexaFarrEntry* _hx_farr_table;
extern int64_t        _hx_farr_count;

enum { FARR_HOST = 0, FARR_DEVICE = 1, FARR_MIRRORED = 2 };

/* cuBLAS handle — lazy init. */
static cublasHandle_t g_cublas = NULL;

static int _ensure_cublas(void) {
    if (g_cublas) return 0;
    cublasStatus_t st = cublasCreate(&g_cublas);
    if (st != CUBLAS_STATUS_SUCCESS) {
        fprintf(stderr, "[cuda] cublasCreate failed: %d\n", (int)st);
        g_cublas = NULL;
        return -1;
    }
    /* Default math mode is fp64-strict for Dgemm; do NOT set
     * CUBLAS_TENSOR_OP_MATH (we want bit-reproducible Dgemm). */
    return 0;
}

/* Upload host buf → device. Allocate if needed. Returns 0 ok / -1 err. */
static int _h2d(int64_t id) {
    if (id < 0 || id >= _hx_farr_count) {
        fprintf(stderr, "[cuda] h2d: bad id %lld\n", (long long)id);
        return -1;
    }
    if (_ensure_slot_cap(id) != 0) return -1;
    HexaFarrEntry* e = &_hx_farr_table[id];
    _CudaFarrSlot* s = &g_slots[id];
    if (!e->buf || e->len <= 0) {
        fprintf(stderr, "[cuda] h2d: empty host farr id=%lld\n", (long long)id);
        return -1;
    }
    if (!s->d_buf || s->len != e->len) {
        if (s->d_buf) cudaFree(s->d_buf);
        cudaError_t er = cudaMalloc((void**)&s->d_buf,
                                    (size_t)e->len * sizeof(double));
        if (er != cudaSuccess) {
            fprintf(stderr, "[cuda] cudaMalloc(%lld doubles) failed: %s\n",
                    (long long)e->len, cudaGetErrorString(er));
            s->d_buf = NULL; s->len = 0;
            return -1;
        }
        s->len = e->len;
    }
    cudaError_t er = cudaMemcpy(s->d_buf, e->buf,
                                (size_t)e->len * sizeof(double),
                                cudaMemcpyHostToDevice);
    if (er != cudaSuccess) {
        fprintf(stderr, "[cuda] cudaMemcpy H2D failed: %s\n",
                cudaGetErrorString(er));
        return -1;
    }
    /* Mirror device pointer back to runtime.c entry for visibility. */
    e->d_buf = (void*)s->d_buf;
    if (e->loc == FARR_HOST) e->loc = FARR_MIRRORED;
    e->dirty_dev = 0;
    return 0;
}

/* Copy device → host. Returns 0 ok / -1 err. */
static int _d2h(int64_t id) {
    if (id < 0 || id >= _hx_farr_count) return -1;
    if (id >= g_slot_cap)               return -1;
    HexaFarrEntry* e = &_hx_farr_table[id];
    _CudaFarrSlot* s = &g_slots[id];
    if (!e->buf || !s->d_buf || s->len != e->len) {
        fprintf(stderr, "[cuda] d2h: state mismatch id=%lld\n", (long long)id);
        return -1;
    }
    cudaError_t er = cudaMemcpy(e->buf, s->d_buf,
                                (size_t)e->len * sizeof(double),
                                cudaMemcpyDeviceToHost);
    if (er != cudaSuccess) {
        fprintf(stderr, "[cuda] cudaMemcpy D2H failed: %s\n",
                cudaGetErrorString(er));
        return -1;
    }
    e->dirty_host = 0;
    if (e->loc == FARR_DEVICE) e->loc = FARR_MIRRORED;
    return 0;
}

/* ── Public surface (forward-decl'd in self/runtime.c HEXA_CUDA block) ── */

int _hx_cuda_runtime_available(void) {
    int n = 0;
    cudaError_t er = cudaGetDeviceCount(&n);
    if (er != cudaSuccess) return 0;
    return (n > 0) ? 1 : 0;
}

int _hx_cuda_device_count_impl(void) {
    int n = 0;
    cudaError_t er = cudaGetDeviceCount(&n);
    if (er != cudaSuccess) return 0;
    return (n > 0) ? n : 0;
}

int _hx_cuda_farr_to_device(int64_t farr_id) {
    if (_h2d(farr_id) != 0) return -1;
    return 1;
}

int _hx_cuda_farr_to_host(int64_t farr_id) {
    if (_d2h(farr_id) != 0) return -1;
    return 1;
}

int _hx_cuda_farr_device_free(int64_t farr_id) {
    if (farr_id < 0 || farr_id >= g_slot_cap) return 1; /* nothing to free */
    _CudaFarrSlot* s = &g_slots[farr_id];
    if (s->d_buf) {
        cudaFree(s->d_buf);
        s->d_buf = NULL;
        s->len = 0;
    }
    if (farr_id < _hx_farr_count) {
        HexaFarrEntry* e = &_hx_farr_table[farr_id];
        e->d_buf = NULL;
        e->loc = FARR_HOST;
        e->dirty_host = 0;
        e->dirty_dev = 0;
    }
    return 1;
}

/* _hx_cuda_farr_matmul_gpu(A, M, K, B, N, C) — Dgemm row-major C = A · B.
 *   A is M×K, B is K×N, C is M×N.
 *   - Caller (runtime.c) has already allocated C farr_id with len = M·N
 *     via hexa_farr_zeros.
 *   - We upload A,B to device (idempotent — skips if already resident),
 *     compute Dgemm on device, copy result back to host C buf,
 *     mark C dirty_host=0 (host current), loc=MIRRORED.
 *   - Returns 0 ok / -1 err.
 *
 *   Row-major → column-major mapping:
 *     C_row[M,N] = A_row[M,K] · B_row[K,N]
 *   View row-major A as column-major A^T (K×M); same for B,C. Then
 *     C^T_col[N,M] = B^T_col[N,K] · A^T_col[K,M]
 *   cuBLAS Dgemm with (op=N, op=N, m=N, n=M, k=K, A=B_dev, lda=N,
 *                      B=A_dev, ldb=K, C=C_dev, ldc=N).
 */
int _hx_cuda_farr_matmul_gpu(int64_t a_id, int64_t M, int64_t K,
                             int64_t b_id, int64_t N,
                             int64_t c_id) {
    if (_ensure_cublas() != 0) return -1;
    if (a_id < 0 || b_id < 0 || c_id < 0) {
        fprintf(stderr, "[cuda] matmul: bad ids %lld %lld %lld\n",
                (long long)a_id, (long long)b_id, (long long)c_id);
        return -1;
    }
    if (M <= 0 || K <= 0 || N <= 0) {
        fprintf(stderr, "[cuda] matmul: bad shape M=%lld K=%lld N=%lld\n",
                (long long)M, (long long)K, (long long)N);
        return -1;
    }
    /* Upload A,B (H2D). */
    if (_h2d(a_id) != 0) return -1;
    if (_h2d(b_id) != 0) return -1;
    /* Ensure C device buffer exists with size M·N. We re-use _ensure_slot_cap
     * + a fresh cudaMalloc to make a clean device-resident output. */
    if (_ensure_slot_cap(c_id) != 0) return -1;
    HexaFarrEntry* ce = &_hx_farr_table[c_id];
    _CudaFarrSlot*  cs = &g_slots[c_id];
    if (!ce->buf || ce->len < M * N) {
        fprintf(stderr, "[cuda] matmul: C host len %lld < M*N %lld\n",
                (long long)ce->len, (long long)(M*N));
        return -1;
    }
    if (!cs->d_buf || cs->len != ce->len) {
        if (cs->d_buf) cudaFree(cs->d_buf);
        cudaError_t er = cudaMalloc((void**)&cs->d_buf,
                                    (size_t)ce->len * sizeof(double));
        if (er != cudaSuccess) {
            fprintf(stderr, "[cuda] cudaMalloc C(%lld) failed: %s\n",
                    (long long)ce->len, cudaGetErrorString(er));
            cs->d_buf = NULL; cs->len = 0;
            return -1;
        }
        cs->len = ce->len;
    }
    double* A_dev = g_slots[a_id].d_buf;
    double* B_dev = g_slots[b_id].d_buf;
    double* C_dev = cs->d_buf;
    const double alpha = 1.0;
    const double beta  = 0.0;
    /* Row-major C = A · B → column-major C^T = B^T · A^T trick:
     *   cuBLAS sees B's row-major buffer as column-major (N×K)
     *   cuBLAS sees A's row-major buffer as column-major (K×M)
     * Dgemm(N,N, m=N, n=M, k=K, alpha, B_dev, ldb=N, A_dev, lda=K,
     *       beta, C_dev, ldc=N) — produces column-major (N×M), which
     * IS the row-major C (M×N). */
    cublasStatus_t st = cublasDgemm(g_cublas,
                                    CUBLAS_OP_N, CUBLAS_OP_N,
                                    (int)N, (int)M, (int)K,
                                    &alpha,
                                    B_dev, (int)N,
                                    A_dev, (int)K,
                                    &beta,
                                    C_dev, (int)N);
    if (st != CUBLAS_STATUS_SUCCESS) {
        fprintf(stderr, "[cuda] cublasDgemm failed: %d\n", (int)st);
        return -1;
    }
    /* Copy C device → host so the host-side caller sees the result. */
    cudaError_t er = cudaMemcpy(ce->buf, C_dev,
                                (size_t)(M * N) * sizeof(double),
                                cudaMemcpyDeviceToHost);
    if (er != cudaSuccess) {
        fprintf(stderr, "[cuda] cudaMemcpy C D2H failed: %s\n",
                cudaGetErrorString(er));
        return -1;
    }
    ce->d_buf      = (void*)C_dev;
    ce->loc        = FARR_MIRRORED;
    ce->dirty_host = 0;
    ce->dirty_dev  = 0;
    return 0;
}
