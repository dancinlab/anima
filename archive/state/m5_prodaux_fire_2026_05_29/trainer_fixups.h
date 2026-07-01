/* trainer_fixups.h — surgical externs + shims for prodaux trainer
 *
 * The hexa-lang codegen for train_v3_moe_prodaux.hexa (PR #1397 trainer)
 * emits calls to several bare-name primitives that:
 *   (a) ARE defined in user-module .hexa code but were NOT extern'd at
 *       the top of trainer.c (codegen2 cross-module extern emission gap)
 *   (b) ARE NOT defined anywhere in the runtime under their bare names —
 *       only _gpu suffixed variants exist (M2/M4 #1318 wiring gap)
 *
 * (a) v3_moe_fwd                — defined in CORE/DECODER/v3_moe_arch.hexa
 * (b) farr_softmax_rows         — only _gpu (3-arg, returns new id) exists
 * (b) farr_ce_seed              — only _gpu (5-arg) exists
 * (b) farr_adamw_step_inplace   — only adamw_step (10-arg) exists
 *
 * For (a) we add forward decls. For (b) we add CPU shims that match the
 * .hexa source's signature.
 */
#ifndef PRODAUX_TRAINER_FIXUPS_H
#define PRODAUX_TRAINER_FIXUPS_H

#include "runtime.h"
#include <math.h>
#include <stdint.h>

/* (a) v3_moe_fwd — defined in trainer.c via the v3_moe_arch transpilation.
 * We just need a forward decl since it appears here as a bare call. */
extern HexaVal v3_moe_fwd(HexaVal, HexaVal, HexaVal, HexaVal, HexaVal,
                          HexaVal, HexaVal, HexaVal, HexaVal);

/* (b) farr_softmax_rows(x_id, out_id, R, C) — in-place row-softmax. */
static HexaVal farr_softmax_rows(HexaVal x_v, HexaVal out_v,
                                  HexaVal r_v, HexaVal c_v) {
    int64_t R = HX_INT(r_v);
    int64_t C = HX_INT(c_v);
    for (int64_t r = 0; r < R; r++) {
        double m = -1e308;
        for (int64_t c = 0; c < C; c++) {
            double xv = HX_FLOAT(hexa_farr_get(x_v, hexa_int(r * C + c)));
            if (xv > m) m = xv;
        }
        double s = 0.0;
        for (int64_t c = 0; c < C; c++) {
            double xv = HX_FLOAT(hexa_farr_get(x_v, hexa_int(r * C + c))) - m;
            s += exp(xv);
        }
        double inv = (s > 0.0) ? (1.0 / s) : 0.0;
        for (int64_t c = 0; c < C; c++) {
            double xv = HX_FLOAT(hexa_farr_get(x_v, hexa_int(r * C + c))) - m;
            (void)hexa_farr_set(out_v, hexa_int(r * C + c),
                                 hexa_float(exp(xv) * inv));
        }
    }
    return hexa_int(0);
}

/* (b) farr_ce_seed(sm_id, tgt_id, dlog_id, R, V) — dlog = sm - onehot(tgt). */
static HexaVal farr_ce_seed(HexaVal sm_v, HexaVal tgt_v, HexaVal dlog_v,
                             HexaVal r_v, HexaVal c_v) {
    int64_t R = HX_INT(r_v);
    int64_t C = HX_INT(c_v);
    for (int64_t r = 0; r < R; r++) {
        int64_t tgt = (int64_t)HX_FLOAT(hexa_farr_get(tgt_v, hexa_int(r)));
        for (int64_t c = 0; c < C; c++) {
            double sm = HX_FLOAT(hexa_farr_get(sm_v, hexa_int(r * C + c)));
            double dv = sm - ((c == tgt) ? 1.0 : 0.0);
            (void)hexa_farr_set(dlog_v, hexa_int(r * C + c), hexa_float(dv));
        }
    }
    return hexa_int(0);
}

/* (b) farr_adamw_step_inplace(W, m, v, g, n, lr, b1, b2, eps, wd, t)
 *     11-arg in-place AdamW. Math: same as runtime's adamw_step which
 *     was an array-id-returning variant. We do in-place writes to W.
 */
static HexaVal farr_adamw_step_inplace(HexaVal W_v, HexaVal m_v, HexaVal v_v,
                                        HexaVal g_v, HexaVal n_v,
                                        HexaVal lr_v, HexaVal b1_v, HexaVal b2_v,
                                        HexaVal eps_v, HexaVal wd_v,
                                        HexaVal t_v) {
    int64_t n = HX_INT(n_v);
    double lr = HX_FLOAT(lr_v);
    double b1 = HX_FLOAT(b1_v);
    double b2 = HX_FLOAT(b2_v);
    double eps = HX_FLOAT(eps_v);
    double wd = HX_FLOAT(wd_v);
    double t = HX_FLOAT(t_v);
    double bc1 = 1.0 - pow(b1, t);
    double bc2 = 1.0 - pow(b2, t);
    for (int64_t i = 0; i < n; i++) {
        double g = HX_FLOAT(hexa_farr_get(g_v, hexa_int(i)));
        double mm = HX_FLOAT(hexa_farr_get(m_v, hexa_int(i)));
        double vv = HX_FLOAT(hexa_farr_get(v_v, hexa_int(i)));
        double w = HX_FLOAT(hexa_farr_get(W_v, hexa_int(i)));
        mm = b1 * mm + (1.0 - b1) * g;
        vv = b2 * vv + (1.0 - b2) * g * g;
        double mhat = mm / bc1;
        double vhat = vv / bc2;
        w = w - lr * (mhat / (sqrt(vhat) + eps) + wd * w);
        (void)hexa_farr_set(m_v, hexa_int(i), hexa_float(mm));
        (void)hexa_farr_set(v_v, hexa_int(i), hexa_float(vv));
        (void)hexa_farr_set(W_v, hexa_int(i), hexa_float(w));
    }
    return hexa_int(0); /* Returns int 0; trainer.c handles HX_IS_STR/cmp_ge */
}

#endif /* PRODAUX_TRAINER_FIXUPS_H */
