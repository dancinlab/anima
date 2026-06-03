/*
 * train_ffi_runeq.c — C RUNEQ baseline driver for C-PORT milestone-2.
 *
 * Exercises the PURE / PORTABLE functions of train_ffi.c byte-for-byte:
 *   - train_ffi_set_hp   (scalar -> struct marshaling)
 *   - train_ffi_get_step / get_grad_norm / get_elapsed_us  (getters)
 *
 * It #includes train_ffi.c (non-CUDA host branch) so it links against
 * the REAL functions + the REAL static FfiState G — no re-implementation.
 * The 3 train_step_* externs (the CUDA bridge) are stubbed: the RUNEQ
 * deliberately does NOT invoke the GPU hot path, only the portable glue.
 *
 * Build:  cc -O2 -o train_ffi_runeq train_ffi_runeq.c
 * Output format MUST match train_ffi_native.hexa main() line-for-line.
 */
#include <stdio.h>

/* Format a float the way hexa's str(Float) does: read the f32 back as
 * double (matches deref_f32 -> hexa_float((double)f)) and print with the
 * same shortest-%g style hexa uses. Static buffer, single-call per line. */
static char* fmtf(float v) {
    static char b[64];
    snprintf(b, sizeof(b), "%g", (double)v);
    return b;
}

/* Header declares the 3 CUDA-bridge entry points; include it first so the
 * stub definitions below match its exact prototypes. */
#include "train_step.h"

/* Stub the CUDA-bridge externs train_ffi.c references (host, non-CUDA).
 * The RUNEQ never calls these — only the portable glue is exercised. */
void* train_step_init(const ModelConfig* cfg) { (void)cfg; return (void*)0; }
void  train_step_cleanup(void* scratch)       { (void)scratch; }
int   train_step(const ModelConfig* cfg, ModelWeights* w, AdamState* a,
                 const TrainHParams* hp, const Batch* b, StepResult* r) {
    (void)cfg;(void)w;(void)a;(void)hp;(void)b;(void)r; return 0;
}

/* Pull in the REAL portable code + the static global FfiState G. */
#include "train_ffi.c"

int main(void) {
    /* Mark initialized so the getters read live struct fields (the
     * portable bookkeeping init_state that train_ffi_init would set;
     * we set ONLY the non-CUDA scalar fields it owns). */
    G.initialized = 1;

    /* PORT-EQ target #1: train_ffi_set_hp (struct marshaling). */
    train_ffi_set_hp(5.0e-4f, 0.85f, 0.98f, 1.0e-9f, 0.02f, 0.5f);

    /* PORT-EQ target #2: the step bump train_ffi_step owns (portable
     * pre-CUDA bookkeeping: G.hp.step++). Replay 3 times. */
    G.hp.step = 0;
    G.hp.step++;
    G.hp.step++;
    G.hp.step++;

    /* PORT-EQ target #3: StepResult fields the getters read back. */
    G.result.grad_norm = 1.2345f;
    G.result.elapsed_us = 987654;

    printf("set_hp.lr=%s\n",          fmtf(G.hp.lr));
    printf("set_hp.beta1=%s\n",       fmtf(G.hp.beta1));
    printf("set_hp.beta2=%s\n",       fmtf(G.hp.beta2));
    printf("set_hp.eps=%s\n",         fmtf(G.hp.eps));
    printf("set_hp.weight_decay=%s\n",fmtf(G.hp.weight_decay));
    printf("set_hp.grad_clip=%s\n",   fmtf(G.hp.grad_clip));
    printf("get_step=%d\n",           train_ffi_get_step());
    printf("get_grad_norm=%s\n",      fmtf(train_ffi_get_grad_norm()));
    printf("get_elapsed_us=%ld\n",    train_ffi_get_elapsed_us());
    return 0;
}
