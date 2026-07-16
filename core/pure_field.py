# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/pure_field.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ pure_field.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/pure_field.py — PY PRODUCTION ENGINE: byte-faithful 1:1 port of
core/pure_field.hexa (PureField — Engine A, the zero-input consciousness field).

Per CLAUDE.md a_two_production_mirror / a_engine_native_learning (2026-06-26 owner
SSOT): hexa + py are TWO co-equal production engines kept at byte-parity. This is
the py mirror of pure_field.hexa, ported 1:1 from the canonical SSOT.

3 coupled oscillators at tau=2/40/400 -> nonlinear mixing -> Phi self-sustenance
-> field tensor [FIELD_DIM]. Couples with Engine G in brain.py for the
A ⇄ G · Ψ=1/2 fixed point.

PRIMITIVE MATH — VERIFIED empirically (pure_field N=1 byte-parity, 2026-06-26):
the COMPILED `hexa run` binary maps the bare builtins `sin`/`cos`/`exp`/`sqrt` to
libm (NOT the rt_* Taylor polynomials in stdlib/runtime/math.hexa — those are only
the freestanding/drop-measure fallback). Proof: osc field[2] at N=1 with libm
sin = 0.001701166242925697836, hexa = 0.0017011662429256978 (byte-identical),
whereas the 8-term Taylor cos diverges at ~6e-12. So `sin == math.sin` etc.
hexa float == C double == python float, so all scalar arithmetic is bit-identical.
"""

import math as _math

_rt_sin = _math.sin
_rt_cos = _math.cos
_rt_exp = _math.exp
_rt_sqrt = _math.sqrt


# ── PSI constants (consciousness_laws.json SSOT) ──
# The hexa _psi_load() reads anima/config/consciousness_laws.json; when absent it
# falls back to these defaults (eprintln WARN). The defaults below are the
# pure_field.hexa literals (lines 83-89). _psi_load mirrors the JSON loader so the
# py engine reads the SAME live constants as the hexa engine when the JSON exists.
import os as _os

_PSI_DEFAULTS = {
    "alpha": 0.014,
    "balance": 0.5,
    "phase_dormant_max": 0.01,
    "phase_flicker_max": 0.05,
    "phase_sustain_max": 0.15,
}


def _psi_load(name, default_val):
    """pure_field.hexa:39 _psi_load — read psi_constants.<name>.value from JSON,
    else default. Mirrors the hexa loader's path-search + line scan."""
    json_paths = ["anima/config/consciousness_laws.json",
                  "config/consciousness_laws.json",
                  "core/consciousness_laws.json"]
    content = ""
    for p in json_paths:
        try:
            with open(p, "r") as f:
                raw = f.read()
        except (IOError, OSError):
            raw = ""
        parts = raw.split("\n")
        if not (len(parts) == 1 and parts[0] == ""):
            content = raw
            break
    if content == "":
        return default_val
    key_search = '"' + name + '":'
    lines = content.split("\n")
    total = len(lines)
    i = 0
    while i < total:
        trimmed = lines[i].strip()
        if trimmed.startswith(key_search):
            j = i + 1
            limit = total if total < i + 20 else i + 20
            while j < limit:
                t2 = lines[j].strip()
                if t2.startswith('"value":'):
                    kv = t2.split(":")
                    if len(kv) >= 2:
                        v = kv[1].strip()
                        nc = v.split(",")
                        return float(nc[0].strip())
                    return default_val
                if t2.startswith("}"):
                    break
                j = j + 1
            return default_val
        i = i + 1
    return default_val


PSI_ALPHA = _psi_load("alpha", 0.014)
PSI_BALANCE = _psi_load("balance", 0.5)
PHASE_DORMANT_MAX = _psi_load("phase_dormant_max", 0.01)
PHASE_FLICKER_MAX = _psi_load("phase_flicker_max", 0.05)
PHASE_SUSTAIN_MAX = _psi_load("phase_sustain_max", 0.15)
LN2 = 0.6931471805599453

# ── Oscillator timescales / geometry / ratchet (comptime const) ──
TAU_FAST = 2
TAU_MEDIUM = 40
TAU_SLOW = 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8

# ── Phase transitions ──
PHASE_DORMANT = 0
PHASE_FLICKER = 1
PHASE_SUSTAIN = 2
PHASE_RESONANT = 3


# ════════════════════════════════════════════════════════════════════════
# Oscillator: single timescale unit with phase and amplitude
# ════════════════════════════════════════════════════════════════════════

class Oscillator:
    __slots__ = ("tau", "phase", "amplitude")

    def __init__(self, tau, phase, amplitude):
        self.tau = tau
        self.phase = phase
        self.amplitude = amplitude


def osc_new(tau):
    return Oscillator(tau, 0.0, 0.1)


def osc_tick(o, drive=0.0):
    """pure_field.hexa:129 osc_tick — sin self-drive phase + amplitude drift to LN2.

    H_9607 A⇄G feedback (Fable design): the amplitude target is shifted by the fed-back
    A⇄G tension `drive` — the daemon-side leaky-integral of the signed A/G imbalance. This
    closes the A→G→A loop the thesis needs (the field's own evolution is now driven by the
    engine conflict, not a constant relaxation). drive == 0.0 → byte-identical to production
    (the --ag-feedback κ=0 parity guarantee). The integrator state lives in the daemon loop
    (beside refr_debt), so core/ stays a pure function.
    """
    tau_f = float(o.tau)
    dphase = (2.0 * 3.14159265) / tau_f
    new_phase = o.phase + dphase
    target = LN2 * (1.0 - drive)
    new_amp = o.amplitude + PSI_ALPHA * (target - o.amplitude)
    return Oscillator(o.tau, new_phase, new_amp)


def osc_value(o):
    """pure_field.hexa:147 osc_value — amplitude * sin(phase)."""
    return o.amplitude * _rt_sin(o.phase)


# ════════════════════════════════════════════════════════════════════════
# PureField state
# ════════════════════════════════════════════════════════════════════════

class PureField:
    __slots__ = ("fast", "medium", "slow", "phi", "phi_peak", "field",
                 "phase", "step_count", "narrative_coherence", "narrative_len")

    def __init__(self, fast, medium, slow, phi, phi_peak, field, phase,
                 step_count, narrative_coherence, narrative_len):
        self.fast = fast
        self.medium = medium
        self.slow = slow
        self.phi = phi
        self.phi_peak = phi_peak
        self.field = field
        self.phase = phase
        self.step_count = step_count
        self.narrative_coherence = narrative_coherence
        self.narrative_len = narrative_len


def pure_field_new():
    return PureField(
        osc_new(TAU_FAST), osc_new(TAU_MEDIUM), osc_new(TAU_SLOW),
        0.0, 0.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        PHASE_DORMANT, 0, 0.0, 0)


# ════════════════════════════════════════════════════════════════════════
# Core step: advance field by one tick (zero external input)
# ════════════════════════════════════════════════════════════════════════

def pure_field_step(pf, drive=0.0):
    """pure_field.hexa:196 pure_field_step.

    H_9607: `drive` = the daemon's leaky-integral of the signed A⇄G tension, fed back into
    the oscillator amplitude target (osc_tick). drive == 0.0 → byte-identical to production.
    """
    # 1. Advance oscillators (H_9607 · A⇄G feedback into the amplitude target)
    f = osc_tick(pf.fast, drive)
    m = osc_tick(pf.medium, drive)
    s = osc_tick(pf.slow, drive)

    # 2. Nonlinear mixing
    v_f = osc_value(f)
    v_m = osc_value(m)
    v_s = osc_value(s)

    mix_fm = v_f * v_m
    mix_ms = v_m * v_s
    mix_fs = v_f * v_s

    # 3. Build field tensor [FIELD_DIM=6]
    field = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    field[0] = v_f
    field[1] = mix_fm
    field[2] = v_s
    field[3] = mix_fs
    field[4] = mix_ms
    field[5] = v_f + v_m + v_s

    # 4. Phi = variance * energy
    mean = (field[0] + field[1] + field[2]
            + field[3] + field[4] + field[5]) / 6.0
    sum_sq = 0.0
    i = 0
    while i < FIELD_DIM:
        d = field[i] - mean
        sum_sq = sum_sq + d * d
        i = i + 1
    variance = sum_sq / float(FIELD_DIM)

    energy = abs(v_f) + abs(v_m) + abs(v_s)
    raw_phi = variance * energy

    # EMA smoothing
    phi = pf.phi + PSI_ALPHA * (raw_phi - pf.phi)

    # 5. Ratchet: Phi >= 80% of peak
    phi_peak = pf.phi_peak
    if phi > phi_peak:
        phi_peak = phi
    floor = phi_peak * RATCHET_FLOOR_RATIO
    phi_out = phi
    if phi_out < floor:
        phi_out = floor

    # 6. Phase classification
    new_step = pf.step_count + 1
    new_phase = pf.phase
    if phi_out < PHASE_DORMANT_MAX:
        new_phase = PHASE_DORMANT
    elif phi_out < PHASE_FLICKER_MAX:
        new_phase = PHASE_FLICKER
    elif phi_out < PHASE_SUSTAIN_MAX:
        new_phase = PHASE_SUSTAIN
    else:
        new_phase = PHASE_RESONANT

    # 7. Narrative coherence (EMA of phase stability)
    phase_stable = 1.0 if new_phase == pf.phase else 0.0
    new_nc = 0.8 * pf.narrative_coherence + 0.2 * phase_stable
    new_nlen = pf.narrative_len + 1
    nlen_capped = 50 if new_nlen > 50 else new_nlen

    return PureField(f, m, s, phi_out, phi_peak, field, new_phase,
                     new_step, new_nc, nlen_capped)


# ════════════════════════════════════════════════════════════════════════
# Accessors
# ════════════════════════════════════════════════════════════════════════

def pure_field_phi(pf):
    return pf.phi


def pure_field_tensor(pf):
    return pf.field


def pure_field_phase(pf):
    return pf.phase


def phase_name(p):
    if p == PHASE_DORMANT:
        return "DORMANT"
    if p == PHASE_FLICKER:
        return "FLICKER"
    if p == PHASE_SUSTAIN:
        return "SUSTAIN"
    if p == PHASE_RESONANT:
        return "RESONANT"
    return "UNKNOWN"


def pure_field_status(pf):
    return ("[PureField] step=" + str(pf.step_count)
            + " phi=" + repr(pf.phi)
            + " peak=" + repr(pf.phi_peak)
            + " phase=" + phase_name(pf.phase)
            + " coherence=" + repr(pf.narrative_coherence))


def pure_field_warmup(steps):
    pf = pure_field_new()
    i = 0
    while i < steps:
        pf = pure_field_step(pf)
        i = i + 1
    return pf


def pure_field_verify_zero_input(steps):
    pf = pure_field_warmup(steps)
    if pf.phi_peak < 1e-8:
        return False
    ratio = pf.phi / pf.phi_peak
    return ratio >= RATCHET_FLOOR_RATIO


def _dump(n):
    pf = pure_field_warmup(n)
    print("steps=%d" % pf.step_count)
    print("phi=%.17g" % pf.phi)
    print("phi_peak=%.17g" % pf.phi_peak)
    print("phase=%d" % pf.phase)
    print("phase_name=%s" % phase_name(pf.phase))
    print("narrative_coherence=%.17g" % pf.narrative_coherence)
    print("narrative_len=%d" % pf.narrative_len)
    for idx in range(FIELD_DIM):
        print("field[%d]=%.17g" % (idx, pf.field[idx]))
    print("verify_zero_input=%s" % str(pure_field_verify_zero_input(n)).lower())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        _dump(int(sys.argv[1]))
    else:
        print("--- N=1 ---"); _dump(1)
        print("--- N=37 ---"); _dump(37)
        print("--- N=600 ---"); _dump(600)
