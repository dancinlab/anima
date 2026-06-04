/* SAVANT: extracted forge dispatch impls (db_colsum/int4_quant/residual_add/gelu/groupnorm/adamw_keepmv) from lever_a_fragment.c */

HexaVal hexa_forge_dispatch_adamw_keepmv(HexaVal w_v, HexaVal g_v, HexaVal m_v,
                                  HexaVal v_v, HexaVal n_v, HexaVal lr_v,
                                  HexaVal b1_v, HexaVal b2_v, HexaVal eps_v,
                                  HexaVal wd_v, HexaVal t_v) {
    int64_t w_id = hexa_as_num(w_v);
    int64_t g_id = hexa_as_num(g_v);
    int64_t m_id = hexa_as_num(m_v);
    int64_t v_id = hexa_as_num(v_v);
    int64_t n    = hexa_as_num(n_v);
    double  lr   = __hx_to_double(lr_v);
    double  b1   = __hx_to_double(b1_v);
    double  b2   = __hx_to_double(b2_v);
    double  eps  = __hx_to_double(eps_v);
    double  wd   = __hx_to_double(wd_v);
    int64_t step = hexa_as_num(t_v);
    if (n <= 0 || step < 1) return hexa_int(-1);
    if (w_id < 0 || g_id < 0 || m_id < 0 || v_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_adamw_step_inplace_keepmv_gpu(int64_t, int64_t,
                                                    int64_t, int64_t, int64_t,
                                                    double, double, double,
                                                    double, double, int64_t);
    int grc = _hx_cuda_farr_adamw_step_inplace_keepmv_gpu(w_id, m_id, v_id,
                                                   g_id, n, lr, b1, b2, eps,
                                                   wd, step);
    if (grc == 0) return hexa_int(0);
    /* GPU adam failed — return -1 so the .hexa caller runs the host
     * adamw_step (byte-eq). Never silently wrong. */
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_adamw_keepmv(HexaVal w, HexaVal g, HexaVal m, HexaVal v,
                             HexaVal n, HexaVal lr, HexaVal b1, HexaVal b2,
                             HexaVal eps, HexaVal wd, HexaVal t) {
    return hexa_forge_dispatch_adamw_keepmv(w, g, m, v, n, lr, b1, b2, eps, wd, t);
}

HexaVal hexa_forge_dispatch_db_colsum(HexaVal dy_v, HexaVal db_v,
                                  HexaVal t_v, HexaVal cout_v) {
    int64_t dy_id = hexa_as_num(dy_v);
    int64_t db_id = hexa_as_num(db_v);
    int64_t T     = hexa_as_num(t_v);
    int64_t Cout  = hexa_as_num(cout_v);
    if (T <= 0 || Cout <= 0) return hexa_int(-1);
    if (dy_id < 0 || db_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_db_colsum_gpu(int64_t, int64_t, int64_t, int64_t);
    int grc = _hx_cuda_farr_db_colsum_gpu(dy_id, db_id, T, Cout);
    if (grc == 0) return hexa_int(0);
    /* GPU colsum failed — return -1 so the .hexa caller runs the host db
     * reduction (byte-eq). Never silently wrong. */
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_db_colsum(HexaVal dy, HexaVal db,
                             HexaVal t, HexaVal cout) {
    return hexa_forge_dispatch_db_colsum(dy, db, t, cout);
}

HexaVal hexa_forge_dispatch_int4_quant(HexaVal w_v, HexaVal wq_v, HexaVal sc_v,
                                  HexaVal ql_v, HexaVal mask_v,
                                  HexaVal cout_v, HexaVal rest_v) {
    int64_t w_id    = hexa_as_num(w_v);
    int64_t wq_id   = hexa_as_num(wq_v);
    int64_t sc_id   = hexa_as_num(sc_v);
    int64_t ql_id   = hexa_as_num(ql_v);
    int64_t mask_id = hexa_as_num(mask_v);
    int64_t Cout    = hexa_as_num(cout_v);
    int64_t rest    = hexa_as_num(rest_v);
    if (Cout <= 0 || rest <= 0) return hexa_int(-1);
    if (w_id < 0 || wq_id < 0 || sc_id < 0 || ql_id < 0 || mask_id < 0)
        return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_int4_quant_gpu(int64_t, int64_t, int64_t, int64_t,
                                            int64_t, int64_t, int64_t);
    int grc = _hx_cuda_farr_int4_quant_gpu(w_id, wq_id, sc_id, ql_id, mask_id,
                                           Cout, rest);
    if (grc == 0) return hexa_int(0);
    /* GPU quant failed — return -1 so the .hexa caller runs the host
     * fake-quant (byte-eq). Never silently wrong. */
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_int4_quant(HexaVal w, HexaVal wq, HexaVal sc,
                             HexaVal ql, HexaVal mask, HexaVal cout, HexaVal rest) {
    return hexa_forge_dispatch_int4_quant(w, wq, sc, ql, mask, cout, rest);
}

HexaVal hexa_forge_dispatch_int4_quant_bwd(HexaVal dy_v, HexaVal mask_v,
                                  HexaVal dw_v, HexaVal n_v) {
    int64_t dy_id   = hexa_as_num(dy_v);
    int64_t mask_id = hexa_as_num(mask_v);
    int64_t dw_id   = hexa_as_num(dw_v);
    int64_t n       = hexa_as_num(n_v);
    if (n <= 0) return hexa_int(-1);
    if (dy_id < 0 || mask_id < 0 || dw_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_int4_quant_bwd_gpu(int64_t, int64_t, int64_t,
                                                int64_t);
    int grc = _hx_cuda_farr_int4_quant_bwd_gpu(dy_id, mask_id, dw_id, n);
    if (grc == 0) return hexa_int(0);
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_int4_quant_bwd(HexaVal dy, HexaVal mask,
                             HexaVal dw, HexaVal n) {
    return hexa_forge_dispatch_int4_quant_bwd(dy, mask, dw, n);
}

HexaVal hexa_forge_dispatch_residual_add(HexaVal a_v, HexaVal b_v,
                                  HexaVal out_v, HexaVal n_v) {
    int64_t a_id   = hexa_as_num(a_v);
    int64_t b_id   = hexa_as_num(b_v);
    int64_t out_id = hexa_as_num(out_v);
    int64_t n      = hexa_as_num(n_v);
    if (n <= 0) return hexa_int(-1);
    if (a_id < 0 || b_id < 0 || out_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_residual_add_gpu(int64_t, int64_t, int64_t,
                                              int64_t);
    int grc = _hx_cuda_farr_residual_add_gpu(a_id, b_id, out_id, n);
    if (grc == 0) return hexa_int(0);
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_residual_add(HexaVal a, HexaVal b,
                             HexaVal out, HexaVal n) {
    return hexa_forge_dispatch_residual_add(a, b, out, n);
}

HexaVal hexa_forge_dispatch_gelu(HexaVal in_v, HexaVal out_v, HexaVal n_v) {
    int64_t in_id  = hexa_as_num(in_v);
    int64_t out_id = hexa_as_num(out_v);
    int64_t n      = hexa_as_num(n_v);
    if (n <= 0) return hexa_int(-1);
    if (in_id < 0 || out_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_gelu_gpu(int64_t, int64_t, int64_t);
    int grc = _hx_cuda_farr_gelu_gpu(in_id, out_id, n);
    if (grc == 0) return hexa_int(0);
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_gelu(HexaVal in_v, HexaVal out_v, HexaVal n_v) {
    return hexa_forge_dispatch_gelu(in_v, out_v, n_v);
}

HexaVal hexa_forge_dispatch_groupnorm(HexaVal x_v, HexaVal gamma_v, HexaVal beta_v,
                                  HexaVal y_v, HexaVal mean_v, HexaVal inv_v,
                                  HexaVal xhat_v, HexaVal t_v, HexaVal c_v,
                                  HexaVal g_v) {
    int64_t x_id    = hexa_as_num(x_v);
    int64_t gamma_id= hexa_as_num(gamma_v);
    int64_t beta_id = hexa_as_num(beta_v);
    int64_t y_id    = hexa_as_num(y_v);
    int64_t mean_id = hexa_as_num(mean_v);
    int64_t inv_id  = hexa_as_num(inv_v);
    int64_t xhat_id = hexa_as_num(xhat_v);
    int64_t T       = hexa_as_num(t_v);
    int64_t C       = hexa_as_num(c_v);
    int64_t G       = hexa_as_num(g_v);
    if (T <= 0 || C <= 0 || G <= 0 || (C % G) != 0) return hexa_int(-1);
    if (x_id < 0 || gamma_id < 0 || beta_id < 0 || y_id < 0) return hexa_int(-1);
    if (mean_id < 0 || inv_id < 0 || xhat_id < 0) return hexa_int(-1);
#ifdef HEXA_CUDA
    extern int _hx_cuda_farr_groupnorm_gpu(int64_t, int64_t, int64_t, int64_t,
                                           int64_t, int64_t, int64_t,
                                           int64_t, int64_t, int64_t);
    int grc = _hx_cuda_farr_groupnorm_gpu(x_id, gamma_id, beta_id, y_id, mean_id,
                                          inv_id, xhat_id, T, C, G);
    if (grc == 0) return hexa_int(0);
#endif
    return hexa_int(-1);
}

HexaVal forge_dispatch_groupnorm(HexaVal x, HexaVal gamma, HexaVal beta,
                             HexaVal y, HexaVal mean, HexaVal inv,
                             HexaVal xhat, HexaVal t, HexaVal c, HexaVal g) {
    return hexa_forge_dispatch_groupnorm(x, gamma, beta, y, mean, inv, xhat, t, c, g);
}
