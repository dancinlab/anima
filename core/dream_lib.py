"""core/dream_lib.py — DREAM 5-stage schedule + Process-S sleep-pressure homeostat.

py 2-production twin of core/dream_lib.hexa — byte-exact mirror (owner directive 2026-07-09
"py 자체구현 · 언어간 상호의존 0"). 90-tick session (WAKE/N1/N2/N3/REM), stage tables, and the
two-process homeostat (Process-S adenosine build/clear via exp, Process-C circadian). Pure
scalar math (exp via libm → python math.exp at machine epsilon); no numpy, no FFI. Returns
numbers only — bool 게이트 0 (p5 · a_autonomy).
"""

from math import exp


def dr_n_ticks():   return 90
def dr_n_stages():  return 5


def dr_stage_at(tick):
    if tick < 60: return 0    # WAKE [0..59]
    if tick < 70: return 1    # N1   [60..69]
    if tick < 80: return 2    # N2   [70..79]
    if tick < 87: return 3    # N3   [80..86]
    return 4                  # REM  [87..89]


def dr_stage_name(stage):
    if stage == 0: return "WAKE"
    if stage == 1: return "N1"
    if stage == 2: return "N2"
    if stage == 3: return "N3"
    if stage == 4: return "REM"
    return "UNKNOWN"


def dr_stage_size(stage):
    if stage == 0: return 60
    if stage == 1: return 10
    if stage == 2: return 10
    if stage == 3: return 7
    if stage == 4: return 3
    return 0


def dr_mitosis_prior(stage):
    if stage == 3: return 0.80
    if stage == 4: return 0.80
    return 0.10


def dr_imagination_active(stage):
    if stage == 3: return 1
    if stage == 4: return 1
    return 0


def dr_emit_envelope(stage):
    if stage == 3: return 0
    if stage == 4: return 0
    return 1


def dr_density(count, size):
    if size <= 0: return 0.0
    return float(count) / float(size)


def dr_ratio_sleep_wake(sleep_density, wake_density):
    if wake_density <= 0.0: return 0.0
    return sleep_density / wake_density


def dr_mitosis_density_ratio(sleep_count, sleep_size, wake_count, wake_size):
    sd = dr_density(sleep_count, sleep_size)
    wd = dr_density(wake_count, wake_size)
    return dr_ratio_sleep_wake(sd, wd)


# ── Process-S (sleep pressure) + Process-C (circadian) homeostat ──
def sp_tau_wake():    return 30.0   # adenosine build-up time constant (ticks)
def sp_tau_sleep():   return 12.0   # clearance time constant (ticks)
def sp_upper():       return 1.0    # saturating asymptote (max pressure)
def sp_lower():       return 0.0    # discharge asymptote (rested)
def sp_w_pressure():  return 0.6    # homeostatic weight in the gate-bias
def sp_w_circadian(): return 0.4    # rhythm (Process-C) weight in the gate-bias


def _sp_clamp01(x):
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def sp_pressure_wake(wake_ticks, s0):
    u = sp_upper()
    decay = exp(-float(wake_ticks) / sp_tau_wake())
    return u - (u - s0) * decay


def sp_pressure_sleep(sleep_ticks, s0):
    l = sp_lower()
    decay = exp(-float(sleep_ticks) / sp_tau_sleep())
    return l + (s0 - l) * decay


def sp_pressure_at(tick, s0):
    if tick < 60:
        return sp_pressure_wake(tick, s0)          # WAKE — accumulate
    peak = sp_pressure_wake(60, s0)                # pressure at sleep onset (tick 60)
    return sp_pressure_sleep(tick - 60, peak)      # sleep — discharge from peak


def sp_circadian_bias(tick):
    n = dr_n_ticks()
    ph = tick % n
    if ph < 0: return 0.0
    return float(ph) / float(n)


def sp_sleep_propensity(pressure, circadian):
    return _sp_clamp01(sp_w_pressure() * pressure + sp_w_circadian() * circadian)


def sp_sleep_propensity_ablated(circadian):
    return _sp_clamp01(sp_w_circadian() * circadian)
