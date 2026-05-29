/* shims.h — local 4/5-arg in-place farr_softmax_rows / farr_ce_seed
 *
 * The .hexa source calls bare-name `farr_softmax_rows(x, out, R, C)` and
 * `farr_ce_seed(sm, tgt, dlogits, R, V)` which were never wired in the
 * runtime's bare-name dispatch (only `_gpu` variants exist as registered
 * HexaVal fn handles, with different signatures: 3-arg returning a NEW id).
 *
 * We expose CPU shims that match the .hexa source's 4-/5-arg in-place
 * semantics. trainer.c is patched (sed) to call these directly instead of
 * the failing hexa_call4/hexa_call5(<undefined>) dispatch.
 *
 * Math contract:
 *   farr_softmax_rows_shim(x_id, out_id, R, V):
 *     out[r, c] = exp(x[r,c] - max_r) / sum_c exp(x[r,c] - max_r)
 *   farr_ce_seed_shim(sm_id, tgt_id, dlog_id, R, V):
 *     dlog[r, c] = sm[r, c] - onehot(c == int64(tgt[r]))
 *
 * Forward to existing static internals in runtime.c:
 *   _hx_farr_softmax_rows_cpu (returns NEW id; we copy into out)
 *   _hx_farr_ce_seed_cpu      (writes into provided dlog_id directly)
 */
#ifndef PRODAUX_SHIMS_H
#define PRODAUX_SHIMS_H
#include "runtime.h"
#include <string.h>
#include <math.h>
#include <stdint.h>

/* Both float arrays in this trainer are F64 (RFC 032 farr type). We work
 * directly via farr_get/farr_set HexaVal API to stay layout-agnostic.
 */

static HexaVal farr_softmax_rows_shim(HexaVal x_v, HexaVal out_v,
                                       HexaVal r_v, HexaVal c_v) {
    int64_t R = HX_INT(r_v);
    int64_t C = HX_INT(c_v);
    for (int64_t r = 0; r < R; r++) {
        /* pass 1: max */
        double m = -1e308;
        for (int64_t c = 0; c < C; c++) {
            HexaVal v = hexa_farr_get(x_v, hexa_int(r * C + c));
            double xv = HX_FLOAT(v);
            if (xv > m) m = xv;
        }
        /* pass 2: sum exp */
        double s = 0.0;
        for (int64_t c = 0; c < C; c++) {
            HexaVal v = hexa_farr_get(x_v, hexa_int(r * C + c));
            double xv = HX_FLOAT(v) - m;
            s += exp(xv);
        }
        /* pass 3: normalize */
        double inv = (s > 0.0) ? (1.0 / s) : 0.0;
        for (int64_t c = 0; c < C; c++) {
            HexaVal v = hexa_farr_get(x_v, hexa_int(r * C + c));
            double xv = HX_FLOAT(v) - m;
            (void)hexa_farr_set(out_v, hexa_int(r * C + c),
                                 hexa_float(exp(xv) * inv));
        }
    }
    return hexa_int(0);
}

static HexaVal farr_ce_seed_shim(HexaVal sm_v, HexaVal tgt_v, HexaVal dlog_v,
                                  HexaVal r_v, HexaVal c_v) {
    int64_t R = HX_INT(r_v);
    int64_t C = HX_INT(c_v);
    for (int64_t r = 0; r < R; r++) {
        HexaVal tv = hexa_farr_get(tgt_v, hexa_int(r));
        int64_t tgt = (int64_t)HX_FLOAT(tv);
        for (int64_t c = 0; c < C; c++) {
            HexaVal smv = hexa_farr_get(sm_v, hexa_int(r * C + c));
            double dv = HX_FLOAT(smv) - ((c == tgt) ? 1.0 : 0.0);
            (void)hexa_farr_set(dlog_v, hexa_int(r * C + c), hexa_float(dv));
        }
    }
    return hexa_int(0);
}

#endif /* PRODAUX_SHIMS_H */
