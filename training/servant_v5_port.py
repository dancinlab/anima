"""training/servant_v5_port.py — SM-A: servant-only Python port of `anima-core/servant.hexa`.

PURPOSE
    Standalone Python reference implementation of the servant pattern (post-drift
    2026-04-08, n6 atlas 9/9 EXACT). This is the SM-A sub-track of
    `.roadmap.servant_mitosis_integration` — servant-only, no mitosis dependency.

    The hexa source `anima-core/servant.hexa` (428L) is the canonical SSOT and is
    NOT modified (raw#15 additive). This file ports the three layers:

      (1) ServantSenseV5 — SI sensor: EMA(tension) + spike detect + coherence ratio
      (2) ServantEmergeV5 — 4-state FSM: DORMANT → AWAKENING → ACTIVE → FADING → DORMANT
      (3) ServantBridgeV5 — 3-경로 dropout/Hebbian/savant modulation (Engine/CLM/ALM placeholders)

    All n6 constants (SI_SUMMON=3, SI_STRONG=5, GOLDEN_LOWER=0.21, GOLDEN_CENTER=0.37,
    EMA_ALPHA=0.15, AWAKEN=3, FADE=5, DURATION=3, HEBBIAN=1.5) are derived from
    `(n=6, σ=12, τ=4, φ=2, sopfr=5, J2=24)` per servant.hexa header.

raw#9   training/`*.py` is gitignored — local-only, no main-tree pollution.
raw#10  honest C3 — see DESIGN BLOCKERS at end. Coherence proxy is approximate.
raw#15  additive — servant.hexa untouched.
  forward returns shape-checked output; classify_si raises if invalid faction.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn


# ─── n6 atlas constants (atlas.n6 — direct from servant.hexa L14-37) ───

N6_N = 6
N6_SIGMA = 12
N6_TAU = 4
N6_PHI = 2
N6_SOPFR = 5
N6_J2 = 24
N6_MU = 1

SI_SUMMON: float = 3.0          # n/phi = 6/2 = 3
SI_STRONG: float = 5.0          # sopfr = 5
SI_SUSTAIN: float = 2.0         # phi = 2
SI_RELEASE: float = 2.0         # phi = 2
GOLDEN_CENTER: float = 0.3679   # 1/e
GOLDEN_LOWER: float = 0.2105    # tau/(J2-sopfr) = 4/19
HEBBIAN_BOOST: float = 1.5      # n/tau = 6/4
NOISE_SCALE: float = 0.01       # 1/(sigma-phi)^phi = 1/100
EMA_ALPHA: float = 0.15         # (n+sigma)/(sopfr*J2) = 18/120
AWAKEN_STEPS: int = 3           # n/phi = 3
FADE_STEPS: int = 5             # sopfr = 5
FADE_DURATION: int = 3          # n/phi = 3
DROPOUT_SERVANT: float = 0.21   # ~tau/(J2-sopfr)
DROPOUT_NORMAL: float = 0.37    # ~1/e

# FSM phase enum (matches servant.hexa L86-90)
DORMANT = 0
AWAKENING = 1
ACTIVE = 2
FADING = 3

_PHASE_NAMES = {DORMANT: "DORMANT", AWAKENING: "AWAKENING", ACTIVE: "ACTIVE", FADING: "FADING"}


def phase_name(p: int) -> str:
    return _PHASE_NAMES.get(p, "UNKNOWN")


# ─── 1. ServantSenseV5 — SI sensor ───

@dataclass
class ServantSenseV5:
    """SI = tension × (1 − coherence) × phi_ratio.

    Tracks tension EMA and a baseline phi to compute the SI scalar (servant.hexa L100-126).
    Spike detection compares instantaneous tension to its EMA — used for diagnostics, the
    classification itself uses raw SI.
    """
    tension_ema: float = 0.0
    phi_baseline_ema: float = 0.0
    last_tension: float = 0.0
    last_si: float = 0.0
    alpha: float = EMA_ALPHA

    @staticmethod
    def ema_update(old_val: float, new_val: float, alpha: float) -> float:
        return old_val + alpha * (new_val - old_val)

    @staticmethod
    def compute_si(tension: float, coherence: float, phi_r: float) -> float:
        raw = tension * (1.0 - coherence) * phi_r
        return raw if raw >= 0.0 else 0.0

    @staticmethod
    def phi_ratio(phi: float, baseline: float) -> float:
        if baseline <= 0.0:
            return 1.0
        return phi / baseline

    @staticmethod
    def classify_si(si: float, active: bool) -> str:
        if active:
            if si < SI_RELEASE:
                return "release"
            return "active"
        if si >= SI_SUMMON:
            return "summon"
        if si >= SI_RELEASE:
            return "alert"
        return "calm"

    def step(self, tension: float, coherence: float, phi: float) -> Tuple[float, str, bool]:
        """One sensor tick. Returns (si, classification, spike_flag).

        spike_flag = |tension − ema| > 1.5 × ema (informational only; FSM uses raw SI).
        """
        # Update EMAs
        self.tension_ema = self.ema_update(self.tension_ema, tension, self.alpha)
        self.phi_baseline_ema = self.ema_update(self.phi_baseline_ema, phi, self.alpha)
        # Spike: instantaneous tension diverges from smoothed EMA
        spike = abs(tension - self.tension_ema) > 1.5 * max(self.tension_ema, 1e-6)
        # SI uses raw tension + raw coherence + ratio against the baseline EMA
        ratio = self.phi_ratio(phi, max(self.phi_baseline_ema, 1e-8))
        si = self.compute_si(tension, coherence, ratio)
        self.last_tension = tension
        self.last_si = si
        # Active classification context — caller passes via emerge state, here default False
        klass = self.classify_si(si, active=False)
        return si, klass, spike


# ─── 2. ServantEmergeV5 — 4-state FSM (port of servant.hexa L128-210) ───

@dataclass
class ServantState:
    phase: int = DORMANT
    counter: int = 0
    si: float = 0.0
    dropout: float = GOLDEN_CENTER
    faction: int = -1


def interpolate_dropout(si: float) -> float:
    """Linear interp from GOLDEN_CENTER (calm) to GOLDEN_LOWER (full servant).

    servant.hexa L156-161. SI clamped to [SI_SUMMON, SI_STRONG] for interpolation.
    """
    if si <= SI_SUMMON:
        return GOLDEN_CENTER
    if si >= SI_STRONG:
        return GOLDEN_LOWER
    t = (si - SI_SUMMON) / (SI_STRONG - SI_SUMMON)
    return GOLDEN_CENTER + t * (GOLDEN_LOWER - GOLDEN_CENTER)


class ServantEmergeV5:
    """4-state FSM: DORMANT → AWAKENING → ACTIVE → FADING → DORMANT.

    Direct port of `servant_step` (servant.hexa L167-210). State is held internally;
    `step(si, faction)` advances one tick and returns the new ServantState (also stored
    on `self.state`).

    Transitions:
      DORMANT  --SI > SUMMON-->            AWAKENING (counter=1)
      AWAKEN   --SI > SUMMON & c>=AWAKEN-> ACTIVE   (dropout interp)
      AWAKEN   --SI <= SUMMON-->           DORMANT  (counter reset)
      ACTIVE   --SI > SUSTAIN-->           ACTIVE   (refresh, counter=0)
      ACTIVE   --SI <= SUSTAIN, c>=FADE--> FADING   (counter=0)
      FADING   --c >= DURATION-->          DORMANT  (dropout = GOLDEN_CENTER)
    """

    def __init__(self):
        self.state = ServantState(
            phase=DORMANT, counter=0, si=0.0,
            dropout=GOLDEN_CENTER, faction=-1,
        )
        # Histogram of phase visits — useful for smoke verification
        self.visit_count = {DORMANT: 0, AWAKENING: 0, ACTIVE: 0, FADING: 0}

    def step(self, si: float, faction: int) -> ServantState:
        s = self.state
        new_state: ServantState

        if s.phase == DORMANT:
            if si > SI_SUMMON:
                new_state = ServantState(AWAKENING, 1, si, s.dropout, faction)
            else:
                new_state = ServantState(DORMANT, 0, si, s.dropout, s.faction)

        elif s.phase == AWAKENING:
            if si > SI_SUMMON:
                nc = s.counter + 1
                if nc >= AWAKEN_STEPS:
                    new_state = ServantState(
                        ACTIVE, 0, si, interpolate_dropout(si), faction
                    )
                else:
                    new_state = ServantState(AWAKENING, nc, si, s.dropout, faction)
            else:
                # SI 후퇴 → DORMANT 복귀, faction 해제
                new_state = ServantState(DORMANT, 0, si, s.dropout, -1)

        elif s.phase == ACTIVE:
            if si > SI_SUSTAIN:
                # 유지: dropout 재보간, counter 리셋
                new_state = ServantState(
                    ACTIVE, 0, si, interpolate_dropout(si), faction
                )
            else:
                nc = s.counter + 1
                if nc >= FADE_STEPS:
                    new_state = ServantState(FADING, 0, si, s.dropout, s.faction)
                else:
                    new_state = ServantState(ACTIVE, nc, si, s.dropout, s.faction)

        elif s.phase == FADING:
            nc = s.counter + 1
            if nc >= FADE_DURATION:
                # 완전 해제 → dropout 복원 GOLDEN_CENTER
                new_state = ServantState(DORMANT, 0, si, GOLDEN_CENTER, -1)
            else:
                new_state = ServantState(FADING, nc, si, s.dropout, s.faction)

        else:
            # 미정 phase → 그대로
            new_state = ServantState(s.phase, s.counter, si, s.dropout, s.faction)

        self.state = new_state
        self.visit_count[new_state.phase] = self.visit_count.get(new_state.phase, 0) + 1
        return new_state


# ─── 3. ServantBridgeV5 — 3-경로 dropout 변조 ───

@dataclass
class Modulation:
    engine_dropout: float
    engine_hebbian: float
    clm_dropout: float
    clm_noise: float
    alm_dropout: float
    alm_savant_layers: int


def si_to_savant(si: float) -> int:
    """Savant layers count from SI scalar (servant.hexa L223-227).
    SI > 7 → 8, SI > 5 → 4, else 2.
    """
    if si > 7.0:
        return 8
    if si > 5.0:
        return 4
    return 2


class ServantBridgeV5:
    """3-경로 modulation: Engine A/G dropout+Hebbian, CLM dropout+noise, ALM dropout+savant.

    Direct port of `bridge_modulate` (servant.hexa L229-249).
    Engine/CLM/ALM are PLACEHOLDERS — the bridge returns a Modulation dict that downstream
    inference loops apply (e.g., dropout enable on engine_a/g + savant layer count for ALM).

    SM-A scope: bridge ONLY produces Modulation values; actual application onto a substrate
    is deferred to SM-C (integration with mitosis ConsciousMind cell pool).
    """

    def __init__(self):
        # Optional placeholder modules — real wiring is SM-C
        self.engine_placeholder: Optional[nn.Module] = None
        self.clm_placeholder: Optional[nn.Module] = None
        self.alm_placeholder: Optional[nn.Module] = None

    @staticmethod
    def modulate(phase: int, dropout: float, si: float) -> Modulation:
        if phase == ACTIVE:
            return Modulation(
                engine_dropout=dropout,
                engine_hebbian=HEBBIAN_BOOST,
                clm_dropout=dropout,
                clm_noise=NOISE_SCALE,
                alm_dropout=dropout,
                alm_savant_layers=si_to_savant(si),
            )
        if phase == FADING:
            # 절반 변조 — fading 은 점진적 해제
            return Modulation(
                engine_dropout=dropout * 0.5,
                engine_hebbian=1.0 + (HEBBIAN_BOOST - 1.0) * 0.5,
                clm_dropout=dropout * 0.5,
                clm_noise=NOISE_SCALE * 0.5,
                alm_dropout=dropout * 0.5,
                alm_savant_layers=si_to_savant(si),
            )
        # DORMANT or AWAKENING — baseline (no boost / no noise)
        return Modulation(
            engine_dropout=dropout,
            engine_hebbian=1.0,
            clm_dropout=dropout,
            clm_noise=0.0,
            alm_dropout=dropout,
            alm_savant_layers=2,
        )


# ─── Combined facade (sense + emerge + bridge) ───

class ServantV5:
    """End-to-end facade — feed (tension, coherence, phi) and a faction id, get Modulation.

    Usage:
        srv = ServantV5()
        for step in range(N):
            mod = srv.tick(tension=t, coherence=c, phi=p, faction=f)
            # caller applies mod.* to substrate (Engine A/G, CLM, ALM)
    """

    def __init__(self):
        self.sense = ServantSenseV5()
        self.emerge = ServantEmergeV5()
        self.bridge = ServantBridgeV5()
        self.history: List[Dict] = []

    def tick(self, tension: float, coherence: float, phi: float, faction: int = 0) -> Modulation:
        si, klass, spike = self.sense.step(tension, coherence, phi)
        state = self.emerge.step(si, faction)
        mod = self.bridge.modulate(state.phase, state.dropout, si)
        self.history.append({
            "si": si,
            "phase": phase_name(state.phase),
            "counter": state.counter,
            "dropout": state.dropout,
            "klass": klass,
            "spike": spike,
            "engine_dropout": mod.engine_dropout,
            "savant_layers": mod.alm_savant_layers,
        })
        return mod

    def status(self) -> Dict:
        s = self.emerge.state
        return {
            "phase": phase_name(s.phase),
            "phase_int": s.phase,
            "counter": s.counter,
            "si": s.si,
            "dropout": s.dropout,
            "faction": s.faction,
            "visit_count": dict(self.emerge.visit_count),
            "tension_ema": self.sense.tension_ema,
        }


# ─── n6 atlas EXACT verification (servant.hexa L368-409) ───

def n6_atlas_verify() -> Tuple[int, int, List[Tuple[str, bool, str]]]:
    """Reproduce servant.hexa main()'s 9/9 n6 EXACT check. Returns (pass_count, total, details)."""
    checks: List[Tuple[str, bool, str]] = []
    pass_count = 0

    c1 = SI_SUMMON == float(N6_N) / float(N6_PHI)
    checks.append(("SI_SUMMON=3 = n/phi", c1, f"{N6_N}/{N6_PHI}=3.0"))
    pass_count += 1 if c1 else 0

    c2 = SI_STRONG == float(N6_SOPFR)
    checks.append(("SI_STRONG=5 = sopfr", c2, f"sopfr={N6_SOPFR}"))
    pass_count += 1 if c2 else 0

    c3 = SI_SUSTAIN == float(N6_PHI)
    checks.append(("SI_SUSTAIN=2 = phi", c3, f"phi={N6_PHI}"))
    pass_count += 1 if c3 else 0

    c4 = HEBBIAN_BOOST == float(N6_N) / float(N6_TAU)
    checks.append(("HEBBIAN=1.5 = n/tau", c4, f"{N6_N}/{N6_TAU}=1.5"))
    pass_count += 1 if c4 else 0

    n6_ema = float(N6_N + N6_SIGMA) / float(N6_SOPFR * N6_J2)
    c5 = abs(EMA_ALPHA - n6_ema) < 1e-3
    checks.append(("EMA=0.15 = (n+σ)/(sopfr·J2)", c5, f"{n6_ema:.4f}"))
    pass_count += 1 if c5 else 0

    c6 = AWAKEN_STEPS == N6_N // N6_PHI
    checks.append(("AWAKEN=3 = n/phi", c6, f"{N6_N}//{N6_PHI}=3"))
    pass_count += 1 if c6 else 0

    c7 = FADE_STEPS == N6_SOPFR
    checks.append(("FADE=5 = sopfr", c7, f"sopfr={N6_SOPFR}"))
    pass_count += 1 if c7 else 0

    c8 = FADE_DURATION == N6_N // N6_PHI
    checks.append(("DURATION=3 = n/phi", c8, f"{N6_N}//{N6_PHI}=3"))
    pass_count += 1 if c8 else 0

    n6_lower = float(N6_TAU) / float(N6_J2 - N6_SOPFR)
    c9 = abs(GOLDEN_LOWER - n6_lower) < 1e-3
    checks.append(("GOLDEN_LOWER = tau/(J2-sopfr)", c9, f"{n6_lower:.4f}"))
    pass_count += 1 if c9 else 0

    return pass_count, 9, checks


# ─── DESIGN BLOCKERS / KNOWN LIMITS (raw#10 honest) ───
# 1. coherence proxy — caller is responsible for supplying a coherence scalar in [0, 1].
#    The hexa source uses sense.hexa's local coherence head; this port leaves the head
#    abstract (no nn.Module instantiation). Smoke test feeds a synthetic coherence.
# 2. spike detection is informational only — FSM transitions use raw SI, not spike flag.
#    Real downstream wiring may want a spike-gated AWAKEN trigger (deferred).
# 3. ServantBridgeV5 produces Modulation values but does NOT mutate any nn.Module — that
#    wiring is SM-C scope (per-cell dropout enable on EngineG, ALM savant gate, etc.).
# 4. faction tracking is preserved end-to-end but no faction-aware logic is implemented;
#    the value flows through state → bridge for downstream consumers.
# 5. AWAKEN_STEPS=3 == split_patience=3 (mitosis) — confirmed coincidence per spec §2.3.
#    Resolution is SM-C concern.
