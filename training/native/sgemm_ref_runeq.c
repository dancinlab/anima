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
 * The reference loop mirrors hxblas_cuda_smoke_large.c's run_case (the
 * non-vendor half), but for a value-EXACT RUNEQ against the hexa port it must
 * model fp32 the SAME WAY the port does, not the way a naive `float`-typed C
 * loop does. See the FP-CONTRACT note below.
 *
 * ── FP-CONTRACT (RUNEQ-CRITICAL — why this is NOT a plain `float` loop) ──────
 * The hexa port (sgemm_ref_native.hexa) has no native f32 type: hexa Float is
 * f64. It models fp32 by storing into a 4-byte slot and reading it back
 * (write_f32 / deref_f32 = an explicit round-to-binary32 at each materialise),
 * with all ARITHMETIC done in f64 between those rounds. Concretely the port:
 *   (a) fills inputs as r32( 0.02 * (double)int )   — the 0.02 is an f64
 *       constant, NOT the f32 literal 0.02f (0.02f != (double)0.02);
 *   (b) forms each product in f64 then rounds: r32( (double)a * (double)b );
 *   (c) accumulates in f64 then rounds after EVERY add: s = r32( s + prod );
 *       i.e. NO fused multiply-add (the product is rounded to f32 BEFORE the
 *       add) and NO f32-native multiply.
 * A naive C ref (`0.02f`, `float a*b`, `s += a*b`) diverges from the port in
 * THREE independent ways: the f32 vs f64 input constant, the f32-native vs
 * f64-then-round product, and -O2's fused `s += a*b` (single-rounded FMA).
 * These are fp-SEMANTICS mismatches, NOT a port bug and NOT a compiler bug —
 * a faithful RUNEQ must pin an IDENTICAL fp model on both sides. This driver
 * therefore reproduces the port's model EXACTLY via the r32() helper, and the
 * build pins -ffp-contract=off so the C compiler cannot re-fuse the explicitly
 * rounded add back into an FMA. Verified: with this model the C ref is
 * element-BIT-exact to the port across all 8 cases (0/16384 + 0/256 mismatches)
 * — see .verdicts/c-port/sgemm-ref-runeq.txt.
 *
 * Build:  cc -O2 -ffp-contract=off -o sgemm_ref_runeq sgemm_ref_runeq.c -lm
 *         (the -ffp-contract=off is REQUIRED for the value-exact RUNEQ.)
 * Output format MUST match sgemm_ref_native.hexa main() line-for-line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* round-to-binary32 — models the port's write_f32/deref_f32 slot round-trip
 * (an explicit IEEE-754 round-to-nearest f32 of an f64 value). Every port
 * arithmetic step that materialises a Float into a 4-byte slot is one r32(). */
static float r32(double v) { return (float)v; }

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

    /* deterministic pattern — port's model: f64 0.02 * (double)int, round f32.
     * (NOT the f32 literal 0.02f — that diverges 1 ULP on ~26% of elements.) */
    for (int i = 0; i < rowsA*colsA; i++) A[i] = r32(0.02 * (double)((i*37)%131 - 65));
    for (int i = 0; i < rowsB*colsB; i++) B[i] = r32(0.02 * (double)((i*53)%127 - 63));

    /* scalar reference honouring transpose — port's model: product formed in
     * f64 then rounded to f32 (r32), accumulated in f64 then rounded after
     * EVERY add. No FMA: the product is rounded BEFORE the add. */
    for (int i = 0; i < M; i++) for (int j = 0; j < N; j++) {
        float s = r32(0.0);
        for (int k = 0; k < K; k++) {
            float a = transA ? A[k*M+i] : A[i*K+k];
            float b = transB ? B[j*K+k] : B[k*N+j];
            s = r32((double)s + r32((double)a * (double)b));
        }
        Cref[i*N+j] = s;
    }

    /* fp32 summary: sum (round after every add, mirroring the port) + max abs. */
    float sum = r32(0.0), maxabs = 0.0f;
    for (int idx = 0; idx < M*N; idx++) {
        float v = Cref[idx];
        sum = r32((double)sum + (double)v);
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
