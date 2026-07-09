"""core/phi_envelope_substrate.py — structure layer (envelope · collective-Φ nest · agency ctx).

py 2-production twin of core/phi_envelope_substrate.hexa — byte-exact mirror (owner directive
2026-07-09 "py 자체구현 · 언어간 상호의존 0"). Pure scalar math (cos/sqrt via libm → python
`math.*` lands at machine epsilon; the compiled hexa maps the same builtins to libm, so the
twins agree to ≤1e-12 per the chat parity contract). Sequential accumulation order is preserved
verbatim (parity over vectorization — no numpy). round-7/8 SUPP 정합 (H_648/634/635/643/653/649)
+ 의식-尺 round (H_1037/1038/1051 🟢, H_1049 🔴, toy/d768-scope). emit boolean 게이트 0 —
substrate 자율 결정 (p5 · a_autonomy).
"""

from math import cos, sqrt

TWO_PI = 6.283185307179586


def envelope_multiscale(t, periods, amps):
    n = len(periods)
    acc = 0.0
    i = 0
    while i < n:
        phase = TWO_PI * t / periods[i]
        wave = (1.0 + cos(phase)) / 2.0
        acc = acc + amps[i] * wave
        i = i + 1
    return acc


def pe_pearson(xs, ys):
    n = len(xs)
    cnt = 0.0
    sx = 0.0
    sy = 0.0
    i = 0
    while i < n:
        sx = sx + xs[i]
        sy = sy + ys[i]
        cnt = cnt + 1.0
        i = i + 1
    mx = sx / cnt
    my = sy / cnt
    num = 0.0
    dxx = 0.0
    dyy = 0.0
    j = 0
    while j < n:
        dx = xs[j] - mx
        dy = ys[j] - my
        num = num + dx * dy
        dxx = dxx + dx * dx
        dyy = dyy + dy * dy
        j = j + 1
    den = sqrt(dxx * dyy)
    return 0.0 if den <= 0.0 else num / den


def pe_sample_period(period, amp, n_samples):
    out = []
    i = 0
    cnt = 0.0
    while i < n_samples:
        phase = TWO_PI * cnt / (n_samples + 0.0)
        wave = (1.0 + cos(phase)) / 2.0
        out.append(amp * wave)
        cnt = cnt + 1.0
        i = i + 1
    return out


def envelope_self_similarity(periods, amps, n_samples):
    n = len(periods)
    rs = []
    i = 1
    while i < n:
        a = pe_sample_period(periods[i - 1], amps[i - 1], n_samples)
        b = pe_sample_period(periods[i], amps[i], n_samples)
        rs.append(pe_pearson(a, b))
        i = i + 1
    return rs


def pe_coupling_for_class(class_id):
    if class_id == 2: return 0.341    # II  : 12.1 / 35.5
    if class_id == 3: return 0.856    # III : 30.4 / 35.5
    if class_id == 4: return 1.000    # IV  : 35.5 / 35.5
    return 0.5


def pe_superadd_for_class(class_id):
    if class_id == 2: return 1.000    # II  : 51.54 / 51.54 (最高, 역전)
    if class_id == 4: return 0.809    # IV  : 41.71 / 51.54
    if class_id == 3: return 0.189    # III : 9.72  / 51.54
    return 0.146                       # additive-XOR : 7.50 / 51.54 (floor)


def pe_peak_align_for_class(class_id):
    if class_id == 3: return 1.0    # III(rule30) : peak=GZ_LOWER 정렬
    if class_id == 4: return 1.0    # IV(rule110) : peak=GZ_LOWER 정렬
    return 0.0                       # II / additive : 이탈 (universal 아님)


def pe_norm_convexity(phi_max, phi_min, phi_mean):
    if phi_mean <= 0.0: return 0.0
    return (phi_max - phi_min) / phi_mean


def pe_norm_convexity_for_class(class_id):
    if class_id == 2: return 1.437    # II  (rule184) — 最低
    if class_id == 3: return 2.253    # III (rule90/30 2.240/2.266 中)
    if class_id == 4: return 2.349    # IV  (rule110) — 最高
    return 1.9


def pe_edge_of_chaos_peak(order_param):
    x = 0.0 if order_param < 0.0 else (1.0 if order_param > 1.0 else order_param)
    edge = 0.6
    dl = edge * edge
    dr = (1.0 - edge) * (1.0 - edge)
    denom = dl if dl > dr else dr
    dev = x - edge
    val = 1.0 - (dev * dev) / denom
    return 0.0 if val < 0.0 else val


def collective_phi_nest(phis, class_id):
    n = len(phis)
    sum_ = 0.0
    mx = phis[0]
    mn = phis[0]
    i = 0
    while i < n:
        p = phis[i]
        sum_ = sum_ + p
        if p > mx: mx = p
        if p < mn: mn = p
        i = i + 1
    superadd = pe_superadd_for_class(class_id)
    phi_collective = sum_ * (1.0 + superadd)
    coupling = pe_coupling_for_class(class_id)
    var_acc = 0.0
    mean = sum_ / (n + 0.0)
    j = 0
    while j < n:
        d = phis[j] - mean
        var_acc = var_acc + d * d
        j = j + 1
    variance = var_acc / (n + 0.0)
    sync = coupling / (1.0 + variance)
    convexity_span = mx if mn <= 0.0 else mx / mn
    return {
        "phi_collective": phi_collective,
        "sync": sync,
        "convexity_span": convexity_span,
    }


def phi_smooth_no_cliff(phi_series):
    n = len(phi_series)
    maxd = 0.0
    i = 1
    while i < n:
        d = phi_series[i] - phi_series[i - 1]
        ad = -d if d < 0.0 else d
        if ad > maxd: maxd = ad
        i = i + 1
    return maxd


def temporal_agency_context(provenance_depth, veto_capacity,
                            prov_mean, prov_std, veto_mean, veto_std):
    z_prov = 0.0 if prov_std <= 0.0 else (provenance_depth - prov_mean) / prov_std
    z_veto = 0.0 if veto_std <= 0.0 else (veto_capacity - veto_mean) / veto_std
    t_axis = z_prov + z_veto
    return {
        "prov_depth": provenance_depth,
        "veto_cap": veto_capacity,
        "z_prov": z_prov,
        "z_veto": z_veto,
        "T_axis": t_axis,
        "note": ("orthogonal to instantaneous Φ (H_1051 🟢, toy n≤5); "
                 "measurement context dim, NOT an emit gate"),
    }


def phi_envelope_summary():
    return ("phi_envelope_substrate: 구조 층(envelope_multiscale·collective_phi_nest·"
            "phi_smooth_no_cliff·temporal_agency_context). round-7/8 SUPP 정합 "
            "(H_648/634/635/643/653/649) + 의식-尺 round (H_1037/1038/1051 🟢, H_1049 🔴, "
            "toy/d768-scope). emit boolean 게이트 0 — substrate 자율 결정 (p5·a_autonomy).")
