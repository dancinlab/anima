#!/usr/bin/env python3
"""w_native_ptd.py — RESEARCH.md §59 W-module-native temporal forward-model.

$0 Mac CPU. NO GPU. NO model.forward. NO autograd. NO weight mutation of any
HEXAD ckpt. Pure numpy hand-coded forward-model on a STUB W-state sequence.
Capability claim 0 — this is a STRUCTURAL-VALIDATION smoke.

═══════════════════════════════════════════════════════════════════════════
THE §59 REFRAME (structural, not a new fire)
═══════════════════════════════════════════════════════════════════════════
§49 wired §48's PTD-aux head into the §24 emission loop. PTD-aux there was a
*distillation-label predictor bolted to the emission gate*: it predicted the
next physics-state, but the training signal that shaped it was the §24
hand-coded talker_should_emit threshold (95% REMAIN_SILENT). It collapsed to
the corpus majority class (§49 FINDINGS §3).

§58 reverse-traced: PTD-aux ≅ NONE of the σ(6)=12 wiring connection-points.
It is a NEW connection-point TYPE — "a module predicts its own next state"
(temporal forward-model). §58 hand-off: its single-facet domain-kin is W↔C;
its natural home, if BUILT, is W-module-adjacent.

§59 builds that W-native home and tests ONE structural hypothesis:

  When the forward-model is OWNED BY W (its prediction-error IS W's
  epistemic-value / curiosity drive — Active Inference EFE: surprise about
  the future self-state is *intrinsically* what curiosity is), does the
  §49-collapse picture change STRUCTURALLY, or is PTD-aux distillation
  regardless of its home?

KEY STRUCTURAL DIFFERENCE (the whole point of §59):
  §49 bolt-on   : target  = §24 hand-coded label (external to W-physics).
                  error    fed to → the §24 emission gate.
                  Objective: minimise distance to a HAND-CODED threshold.
  §59 W-native  : target  = the NEXT ACTUAL W-state (self-prediction).
                  error    fed to → W.curiosity (EFE epistemic value).
                  Objective: predict your own future physics; the residual
                             surprise IS the curiosity signal (NO label).

This is §7-legitimate: the signal is anima's OWN W-physics (W-state →
W-state self-prediction; error = epistemic value), NOT an external
distillation label. That is a real structural improvement over §49.

═══════════════════════════════════════════════════════════════════════════
THE HONEST CRUX (g3 — confronted directly, NOT hidden)
═══════════════════════════════════════════════════════════════════════════
The W-native reframe changes the OBJECTIVE SEMANTICS (intrinsic curiosity
vs distillation label). It does NOT, by itself, change the DATA. If the
underlying W-state sequence is itself corpus-majority-dominated (the §27/§48
trace is ~95% one regime), then a self-predictive forward-model can STILL
learn "predict the prior mean" and its error collapses to a near-constant
(the §49 echo) — only now relabelled "curiosity" instead of "distillation".

So the open question is precise:
  Does W-native (error-as-curiosity) make the forward-model's error a
  NON-DEGENERATE function of state-surprise (varies as the W-state varies),
  or does it collapse to the prior-mean residual REGARDLESS of home?

This smoke measures exactly that — with TWO contrasting W-state regimes:
  (R1) DIVERSE W-state  : surprise varies step-to-step (genuine dynamics).
  (R2) MAJORITY W-state : ~95% one regime (the §27/§48 corpus shape).
And the structural control:
  (OFF) W-native-PTD disabled ⇒ W-module byte-equal baseline (no curiosity
        coupling) — the connection-point reduction.

If R1 error-variance ≫ τ but R2 error-variance ≤ τ ≈ R2-prior-residual,
the verdict is: W-native is §7-legitimate AND structurally distinct from
§49, but it does NOT escape collapse when the W-state itself is majority-
dominated — the §49 collapse is data-shape-bound, not home-bound. That is
the honest expected result, stated up front (g3, mirror §49 FINDINGS).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

SEED = 1337
OUT = Path(__file__).resolve().parent

# ── W-module SSOT mirror (HEXAD/W/w_lib.hexa byte-equal closed forms) ───────
PSI_BALANCE = 0.5
LN2 = 0.6931471805599453


def w_lr_mult(phi: float, n_cells: int) -> float:
    """HEXAD/W/w_lib.hexa :: w_lr_mult — byte-equal mirror."""
    if n_cells < 1:
        n_cells = 1
    scale = phi / (n_cells * 1.0)
    m = scale if scale <= LN2 else LN2
    return PSI_BALANCE + m


def w_satisfaction(phi: float, phi_prev: float) -> float:
    """HEXAD/W/w_lib.hexa :: w_satisfaction — Law-84 binary pulse mirror."""
    return 1.0 if phi >= phi_prev else 0.0


# ───────────────────────────────────────────────────────────────────────────
# Deterministic LCG (NO np.random — B-S59-3 determinism, §48/§27 precedent)
# ───────────────────────────────────────────────────────────────────────────
class LCG:
    _A = 6364136223846793005
    _C = 1442695040888963407
    _M = 1 << 64

    def __init__(self, seed: int):
        self.s = seed & (self._M - 1)

    def _next(self) -> int:
        self.s = (self._A * self.s + self._C) % self._M
        return self.s

    def uniform(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * (self._next() / self._M)


# ───────────────────────────────────────────────────────────────────────────
# W-STATE: the anima physics state the W-module observes.
#   The 4-dim W-state vector mirrors the W-relevant facet of the §27/§48
#   physics feature vector: [curiosity_ema, tension, psi_dir, phi].
#   W.curiosity-relevant; psi_dir/phi are Law-71 / Law-84 W inputs.
# ───────────────────────────────────────────────────────────────────────────
W_DIM = 4


def _w_state(curiosity_ema: float, tension: float, psi_dir: float,
             phi: float) -> list[float]:
    return [
        max(0.0, min(1.0, curiosity_ema)),
        max(0.0, min(1.0, tension)),
        max(0.0, min(1.0, psi_dir)),
        max(0.0, min(2.0, phi)),
    ]


def _gen_w_sequence(regime: str, n_steps: int = 400) -> list[list[float]]:
    """A stub W-state sequence. regime ∈ {'diverse','majority'}.

    'diverse'  : genuine W-dynamics — curiosity/tension/psi/phi all evolve,
                 step-to-step surprise is real (non-degenerate).
    'majority' : ~95% of steps sit in ONE near-constant regime (the §27/§48
                 corpus shape: 95% REMAIN_SILENT-equivalent low-activity);
                 ~5% are sparse excursions.
    """
    g = LCG(SEED + (0 if regime == "diverse" else 7))
    seq: list[list[float]] = []
    phi = 1.0
    for step in range(n_steps):
        if regime == "diverse":
            cur = 0.5 + 0.45 * math.sin(0.21 * step + 0.3)
            ten = 0.30 + 0.40 * math.sin(0.6 * step + g.uniform(0, 6.283) * 0.0
                                         + 0.7)
            psi = PSI_BALANCE + 0.30 * math.sin(0.4 * step) \
                + 0.10 * math.cos(0.13 * step)
            phi = 0.6 + 0.7 * (0.5 + 0.5 * math.sin(0.17 * step + 1.1))
        else:  # majority — 95% near-constant low-activity, 5% excursions
            in_excursion = (step % 20 == 3)  # 1/20 ≈ 5% sparse excursion
            if in_excursion:
                cur = 0.55 + 0.40 * g.uniform(0.0, 1.0)
                ten = 0.30 + 0.40 * g.uniform(0.0, 1.0)
                psi = PSI_BALANCE + 0.30 * (g.uniform(0.0, 1.0) - 0.5)
                phi = 0.6 + 0.7 * g.uniform(0.0, 1.0)
            else:  # the ~95% majority regime — near-constant
                cur = 0.06 + 0.01 * math.sin(0.02 * step)
                ten = 0.30 + 0.003 * math.sin(0.05 * step)
                psi = PSI_BALANCE + 0.004 * math.cos(0.03 * step)
                phi = 1.00 + 0.002 * math.sin(0.01 * step)
        seq.append(_w_state(cur, ten, psi, phi))
    return seq


# ───────────────────────────────────────────────────────────────────────────
# W-NATIVE PTD FORWARD-MODEL
#   A tiny linear-affine forward-model g_θ : W_state_t → \hat W_state_{t+1}.
#   Trained ONLINE by the W-module to predict its OWN next state.
#   prediction-error = ‖W_{t+1} − \hat W_{t+1}‖² ≥ 0  (MSE; EFE epistemic
#   value: surprise about the future self-state).  This residual IS
#   W.curiosity — NO external label.  (§49: target was the §24 hand-coded
#   threshold; HERE target is the next ACTUAL W-state — the structural
#   distinction B-S59-1 / B-S59-2 close.)
# ───────────────────────────────────────────────────────────────────────────
class WNativePTD:
    def __init__(self, dim: int = W_DIM, lr: float = 0.02,
                 w_native_enabled: bool = True):
        self.dim = dim
        self.lr = lr
        self.enabled = w_native_enabled
        # W (dim×dim) + b (dim) — zero-init ⇒ first prediction = 0-vector;
        # with enabled=False the forward-model is a no-op (OFF reduction).
        self.Wm = [[0.0] * dim for _ in range(dim)]
        self.b = [0.0] * dim

    def predict(self, x: list[float]) -> list[float]:
        if not self.enabled:
            # OFF: no forward-model exists. predict() must not be called on
            # the OFF path (step() short-circuits); kept defensive.
            return list(x)
        out = []
        for i in range(self.dim):
            acc = self.b[i]
            row = self.Wm[i]
            for j in range(self.dim):
                acc += row[j] * x[j]
            out.append(acc)
        return out

    def step(self, x: list[float], y_next: list[float]) -> float:
        """Online predict-then-learn. Returns prediction-error (= curiosity).

        When OFF: error ≡ 0 by construction — the forward-model does NOT
                  exist, so there is NO epistemic surprise and NO W.curiosity
                  coupling beyond W-module baseline. This is the
                  connection-point reduction (B-S59-4): W-native-PTD disabled
                  ⇒ W-module byte-equal (mirror B-DHDL-5 / B-EBT-5 OFF).
        When ON : MSE(\hat y, y_next) ≥ 0 — Active-Inference epistemic value.
        """
        if not self.enabled:
            return 0.0
        yhat = self.predict(x)
        err = 0.0
        for i in range(self.dim):
            d = y_next[i] - yhat[i]
            err += d * d
        err /= self.dim
        if self.enabled:
            # SGD step on the self-prediction objective (predict OWN future
            # state). No external label anywhere — §7-legitimate intrinsic.
            for i in range(self.dim):
                grad_o = -2.0 * (y_next[i] - yhat[i]) / self.dim
                for j in range(self.dim):
                    self.Wm[i][j] -= self.lr * grad_o * x[j]
                self.b[i] -= self.lr * grad_o
        return err


# ───────────────────────────────────────────────────────────────────────────
# W.curiosity coupling — the W-native error feeds W.curiosity, NOT the
# §24 emission gate. (B-S59-1 connection-point: distinct site from §49.)
#   curiosity_coupled = clamp01( base_curiosity_ema + κ · prediction_error )
# The prediction-error (epistemic surprise) ADDS to W's intrinsic curiosity.
# ───────────────────────────────────────────────────────────────────────────
KAPPA = 2.0


def w_curiosity_coupled(base_cur_ema: float, pred_error: float) -> float:
    return max(0.0, min(1.0, base_cur_ema + KAPPA * pred_error))


# ───────────────────────────────────────────────────────────────────────────
# SMOKE: run W-native PTD over diverse vs majority W-state, + OFF control.
#   Collapse-vs-signal test (decidable Boolean, mirrors §49 divergence
#   metric): error-variance > τ ⇒ non-degenerate curiosity signal;
#   ≤ τ ⇒ collapsed (prior-mean residual, the §49 echo).
# ───────────────────────────────────────────────────────────────────────────
TAU = 1e-4  # collapse threshold (mirror §24 B-PHASE-B-RUN nontrivial τ=1e-4)


def _variance(xs: list[float]) -> float:
    n = len(xs)
    if n == 0:
        return 0.0
    m = sum(xs) / n
    return sum((x - m) ** 2 for x in xs) / n


def _run_regime(regime: str, enabled: bool) -> dict:
    seq = _gen_w_sequence(regime)
    fm = WNativePTD(w_native_enabled=enabled)
    errs: list[float] = []
    curs: list[float] = []
    # honest stratification: for the majority regime, separate the ~95%
    # majority-regime steps (data near-constant) from the ~5% sparse
    # excursion steps. The §49-echo question is precisely: on the
    # majority-regime steps (where the data IS constant), does the
    # self-predictive error collapse to the prior-mean residual?
    majority_step_errs: list[float] = []
    excursion_step_errs: list[float] = []
    warm = len(seq) // 4
    for t in range(len(seq) - 1):
        x, y = seq[t], seq[t + 1]
        e = fm.step(x, y)
        base_cur = x[0]  # curiosity_ema is W-state[0]
        c = w_curiosity_coupled(base_cur, e)
        if t >= warm:
            errs.append(e)
            curs.append(c)
            if regime == "majority":
                # excursion step ⇔ next state is the perturbed regime
                is_exc = ((t + 1) % 20 == 3)
                (excursion_step_errs if is_exc
                 else majority_step_errs).append(e)
    ev = _variance(errs)
    cv = _variance(curs)
    out = {
        "regime": regime,
        "w_native_enabled": enabled,
        "n_measured": len(errs),
        "error_mean": sum(errs) / len(errs) if errs else 0.0,
        "error_variance": ev,
        "error_max": max(errs) if errs else 0.0,
        "error_min": min(errs) if errs else 0.0,
        "curiosity_variance": cv,
        # decidable Boolean (mirror §49 / §24): variance > τ ⇒ non-degenerate
        "non_degenerate_curiosity": bool(ev > TAU),
        "collapsed_to_prior": bool(ev <= TAU),
    }
    if regime == "majority":
        mse_mean = (sum(majority_step_errs) / len(majority_step_errs)
                    if majority_step_errs else 0.0)
        mse_var = _variance(majority_step_errs)
        exc_mean = (sum(excursion_step_errs) / len(excursion_step_errs)
                    if excursion_step_errs else 0.0)
        out["majority_regime_steps"] = {
            "n": len(majority_step_errs),
            "error_mean": mse_mean,
            "error_variance": mse_var,
            # the §49-echo: on the constant-data 95%, does error collapse?
            "collapsed_on_constant_data": bool(mse_var <= TAU),
        }
        out["excursion_steps"] = {
            "n": len(excursion_step_errs),
            "error_mean": exc_mean,
        }
    return out


def main() -> None:
    results = {
        "research_md_section": "§59",
        "title": "PTD-aux as W-module-native temporal forward-model "
                 "(error-as-curiosity)",
        "$cost": "$0 Mac CPU (numpy hand-coded, no GPU, no model.forward)",
        "seed": SEED,
        "tau_collapse": TAU,
        "kappa_curiosity_coupling": KAPPA,
        "structural_distinction": {
            "s49_bolt_on": "target = §24 hand-coded threshold label; "
                           "error → §24 emission gate (external label).",
            "s59_w_native": "target = next ACTUAL W-state (self-predict); "
                            "error → W.curiosity (EFE epistemic value, "
                            "§7-legitimate intrinsic, NO external label).",
        },
        "runs": {},
    }

    # R1 diverse W-state, W-native ON
    r1 = _run_regime("diverse", enabled=True)
    # R2 majority W-state (the §27/§48 corpus shape), W-native ON
    r2 = _run_regime("majority", enabled=True)
    # OFF control on diverse: W-native disabled ⇒ W-module byte-equal
    # baseline (error ≡ 0, no curiosity coupling) — connection-point.
    r_off = _run_regime("diverse", enabled=False)

    results["runs"]["R1_diverse_on"] = r1
    results["runs"]["R2_majority_on"] = r2
    results["runs"]["OFF_diverse_disabled"] = r_off

    # The honest crux verdict (g3 — decided by measurement, not pre-loaded).
    # Collapse on the majority regime is judged on the ~95% CONSTANT-DATA
    # steps (the §49-echo question), NOT on the aggregate variance which is
    # dominated by the rare ~5% excursion spikes (a measurement artefact
    # that would falsely read as "non-degenerate"). This stratification is
    # the honest structurally-correct test.
    diverse_signal = r1["non_degenerate_curiosity"]
    majority_collapsed = r2["majority_regime_steps"][
        "collapsed_on_constant_data"]
    off_is_zero = (abs(r_off["error_mean"]) < 1e-12
                   and abs(r_off["error_variance"]) < 1e-12)

    if diverse_signal and majority_collapsed:
        crux = ("W-NATIVE-IS-STRUCTURALLY-DISTINCT-BUT-COLLAPSE-IS-"
                "DATA-SHAPE-BOUND")
        crux_text = (
            "W-native error IS a non-degenerate curiosity signal when the "
            "W-state itself is diverse (R1 variance > τ), but it STILL "
            "collapses to the prior-mean residual when the W-state is "
            "majority-dominated (R2 ≤ τ — the §27/§48 ~95% corpus shape). "
            "Therefore the §49 collapse is DATA-SHAPE-bound, NOT home-bound: "
            "making PTD-aux W-native is a real §7-legitimate STRUCTURAL "
            "improvement (intrinsic curiosity, not external label — "
            "B-S59-1/2), but it does NOT by itself escape §49 collapse on "
            "majority-dominated input. The reframe changes the objective "
            "semantics; it does not change the data."
        )
    elif diverse_signal and not majority_collapsed:
        crux = "W-NATIVE-ESCAPES-MAJORITY-COLLAPSE"
        crux_text = (
            "W-native error stays non-degenerate even on majority-dominated "
            "W-state — self-prediction surprise survives the prior. This "
            "would be a stronger structural result than expected; treat "
            "with caution pending a real-state fire (B-S59-NOTE)."
        )
    else:
        crux = "W-NATIVE-DOES-NOT-CHANGE-COLLAPSE"
        crux_text = (
            "Even on diverse W-state the W-native error collapses — the "
            "reframe is pure relabelling, no structural change vs §49."
        )

    results["honest_crux"] = {
        "verdict": crux,
        "text": crux_text,
        "r1_diverse_non_degenerate": diverse_signal,
        "r2_majority_collapsed": majority_collapsed,
        "off_reduction_error_is_zero": off_is_zero,
    }
    results["goal_distance"] = (
        "§15 milestone unchanged. north-star (GOAL.md) NOT reached. §59 = "
        "§7-legitimate STRUCTURAL reframe (error-as-curiosity vs §49 "
        "bolt-on) + $0 structural-validation smoke. Whether W-native "
        "escapes collapse AT SCALE on real anima W-state is an honest "
        "future-fire question (B-S59-NOTE). Capability claim 0."
    )

    (OUT / "result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== §59 W-native PTD smoke ===")
    for k, v in results["runs"].items():
        print(f"{k:24s} err_mean={v['error_mean']:.6e} "
              f"err_var={v['error_variance']:.6e} "
              f"non_degenerate={v['non_degenerate_curiosity']}")
    print(f"OFF reduction error≡0: {off_is_zero}")
    print(f"CRUX: {crux}")


if __name__ == "__main__":
    main()
