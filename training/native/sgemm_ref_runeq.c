/*
 * sgemm_ref_runeq.c — C RUNEQ baseline driver for C-PORT milestone-3.
 *
 * Exercises the PORTABLE scalar GEMM reference that the tier-C smoke
 * harnesses (hxblas_cuda_smoke.c / hxblas_cuda_smoke_large.c) carry: the
 * deterministic input pattern + the C_ref triple-loop matmul (honouring
 * transA/transB) + an fp32 summary (sum + max abs). NO vendor-ABI call:
 * hxblas_sgemm (the cuBLAS / Accelerate-cblas half of the smoke) is NOT
 * invoked here — only the reference side, which is the hexa-portable
 * surface ported in sgemm_ref_native.hexa.
 *
 * The reference loop is copied VERBATIM from hxblas_cuda_smoke_large.c's
 * run_case (the non-vendor half), so this driver computes bit-identically
 * to that harness. `float s` keeps fp32 accumulation; the summary sum is
 * likewise fp32 (float) so it rounds exactly like the hexa round_f32 path.
 *
 * Build:  cc -O2 -o sgemm_ref_runeq sgemm_ref_runeq.c -lm
 * Output format MUST match sgemm_ref_native.hexa main() line-for-line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* Format a float the way hexa's str(Float) does: read the f32 back as
 * double and print with shortest-%g (matches deref_f32 -> hexa_float). */
static char* fmtf(float v) {
    static char b[64];
    snprintf(b, sizeof(b), "%g", (double)v);
    return b;
}

static void run_case(int M, int N, int K, int transA, int transB) {
    int rowsA = transA ? K : M; int colsA = transA ? M : K;
    int rowsB = transB ? N : K; int colsB = transB ? K : N;
    float *A    = (float*)calloc(rowsA*colsA, sizeof(float));
    float *B    = (float*)calloc(rowsB*colsB, sizeof(float));
    float *Cref = (float*)calloc(M*N, sizeof(float));

    /* deterministic pattern — VERBATIM from hxblas_cuda_smoke_large.c */
    for (int i = 0; i < rowsA*colsA; i++) A[i] = 0.02f * (float)((i*37)%131 - 65);
    for (int i = 0; i < rowsB*colsB; i++) B[i] = 0.02f * (float)((i*53)%127 - 63);

    /* scalar reference honouring transpose — VERBATIM from run_case */
    for (int i = 0; i < M; i++) for (int j = 0; j < N; j++) {
        float s = 0.0f;
        for (int k = 0; k < K; k++) {
            float a = transA ? A[k*M+i] : A[i*K+k];
            float b = transB ? B[j*K+k] : B[k*N+j];
            s += a*b;
        }
        Cref[i*N+j] = s;
    }

    /* fp32 summary: sum (fp32-accumulated) + max abs element. */
    float sum = 0.0f, maxabs = 0.0f;
    for (int idx = 0; idx < M*N; idx++) {
        float v = Cref[idx];
        sum += v;
        float av = fabsf(v);
        if (av > maxabs) maxabs = av;
    }

    printf("[%dx%dx%d tA=%d tB=%d] sum=%s ", M, N, K, transA, transB, fmtf(sum));
    printf("maxabs=%s\n", fmtf(maxabs));

    free(A); free(B); free(Cref);
}

int main(void) {
    run_case(16, 16, 16, 0, 0);
    run_case(16, 16, 16, 1, 0);
    run_case(16, 16, 16, 0, 1);
    run_case(16, 16, 16, 1, 1);
    run_case(128, 128, 128, 0, 0);
    run_case(128, 128, 128, 1, 0);
    run_case(128, 128, 128, 0, 1);
    run_case(64, 32, 128, 0, 0);
    printf("[sgemm_ref] DONE\n");
    return 0;
}
