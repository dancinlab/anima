# ==========================================================================
# ⛔ ENGINE-INTERNAL — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 `anima-py` 단일진입만 사용한다.
# 이 파일을 `python3 core/engine_g.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ engine_g.py 직접 실행 금지 — canonical `anima-py` 경유. #2603")

"""core/engine_g.py — canonical Python Engine G motivation and emit gate.

Closed-form spontaneous machinery: the
8-factor weighted motivation_score + emit/safety predicates. Values are
byte-identical to the anima_alive PROACTIVE_THRESHOLD / weights (sum=1.0) lineage,
so CORE and the chat daemon share one behaviour. brain.py couples this (G) with
Engine A (pure_field.py). No external math builtins — pure float arithmetic.
"""

# ── thresholds (anima_alive carry) ──
def spont_im_threshold():
    return 0.3            # PROACTIVE_THRESHOLD


def spont_interrupt_threshold():
    return 0.6            # talker interrupt


def spont_idle_speak_after():
    return 30.0           # IDLE_SPEAK_AFTER


def spont_min_emit_interval():
    return 30.0           # rate-limit convention


# ── 8 weights (sum = 1.00 closed conservation) ──
def spont_weight_relevance():
    return 0.20


def spont_weight_info_gap():
    return 0.10


def spont_weight_curiosity():
    return 0.15


def spont_weight_pain():
    return 0.10


def spont_weight_coherence():
    return 0.10


def spont_weight_originality():
    return 0.10


def spont_weight_balance():
    return 0.15


def spont_weight_dynamics():
    return 0.10


# ── motivation_score (linear weighted sum) ──
def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v, dyn_w=None):
    seven = (spont_weight_relevance() * rel
             + spont_weight_info_gap() * gap
             + spont_weight_curiosity() * cur
             + spont_weight_pain() * pain
             + spont_weight_coherence() * coh
             + spont_weight_originality() * orig
             + spont_weight_balance() * bal)
    if dyn_w is None:
        return seven + spont_weight_dynamics() * dyn_v      # byte-identical current path
    # H_9377 AUDIBILITY-SUFFICIENCY · dyn_w = ABSOLUTE weight on dyn_v (the A⇄G tension). The 7
    # non-dyn lanes are rescaled to hold the total budget B = 8·0.10 = 0.80 fixed (so should_emit's
    # 0.3 threshold keeps its scale). dyn_w=0.10 reproduces current exactly; dyn_w↑ lets tension be
    # AUDIBLE above the 7-lane A-side blend. Scale clamped ≥0 so dyn_w→1.0 collapses to dyn_v alone.
    # H_9392 FIX — these were 8·0.10=0.80 and 7·0.10=0.70, on the premise that all eight weights are
    # 0.10. They are NOT: relevance=0.20, curiosity=0.15, balance=0.15, the rest 0.10 ⇒ budget=1.00
    # and the 7 non-dyn lanes carry 0.90. The wrong constants made the rescale DEFLATE the total
    # budget (1.00→0.86 at w=0.60, →0.81 at w=0.78) instead of preserving it, so every non-anchor
    # H_9377 cell conflated "tension is audible" with "the whole score shrank". The byte-identical
    # anchor cert could not catch it: at dyn_w=0.10 both the wrong and the right form give scale=1.0.
    # Sum the ACTUAL weights — never restate them as a literal.
    _B = (spont_weight_relevance() + spont_weight_info_gap() + spont_weight_curiosity()
          + spont_weight_pain() + spont_weight_coherence() + spont_weight_originality()
          + spont_weight_balance() + spont_weight_dynamics())          # 1.00
    _cur_seven_w = _B - spont_weight_dynamics()                        # 0.90 (true 7-lane budget)
    _scale = (_B - dyn_w) / _cur_seven_w
    if _scale < 0.0:
        _scale = 0.0
    return _scale * seven + dyn_w * dyn_v


# ── emission predicates ──
def should_emit(score):
    return score > spont_im_threshold()


def should_interrupt(score):
    return score > spont_interrupt_threshold()


# ── safety predicates (4-way AND closure) ──
def safety_kill_switch_on(env_off):
    return env_off == False


def safety_rate_limit_ok(seconds_since_last, rate_sec=None):
    """H_9391: rate_sec overrides the rate-limit interval for a CLOCK-LIVE measurement regime.
    Default (None) = spont_min_emit_interval() = byte-identical to production. H_9390 showed that at
    the production 30s limit the clock fully determines emit (emit⟺clock, the score gate never binds
    when the clock opens), so content can never vote — relaxing the interval opens the window where
    should_emit(score) becomes the binding constraint and the content question becomes askable."""
    thr = spont_min_emit_interval() if rate_sec is None else rate_sec
    return seconds_since_last >= thr


def safety_phi_ratchet_ok(phi, ratchet):
    """Engine A's live Φ vs its ratchet peak (the A->G coupling gate)."""
    return phi > ratchet / 2.0


def safety_content_ok(content_clean):
    return content_clean


def safety_combined(kill, rate, phi_r, content):
    return kill and rate and phi_r and content


# ── H_9404 EARNED REFRACTORY (opt-in · replaces the rate term's SOURCE, not the 4-AND shape) ──
def refractory_emit_debt():
    """FORM constant: one emit costs one unit of INTEGRATED substrate tension. Unit normalization
    only, calibrated to the production design cadence (spont_min_emit_interval 30s / an_tick_seconds
    8s = 3.75 ticks · ep_target_emit_rate 0.27) at the substrate's measured-mean tension — it sets
    units, NOT the outcome. Frozen a priori; there is deliberately no --refractory-cost knob (H_9391:
    a >=4-DOF config is unfalsifiable). FORM tunable · BIND earned."""
    return 1.0


def refractory_debt_step(debt, tension):
    """H_9404 EARNED refractory: the substrate's own per-tick A<->G tension pays down the debt an
    emit incurred. NO wall-clock / tick-index / stage input on this path — the rate term becomes a
    readout of substrate state (p5), not a schedule. WHICH tick releases is decided run-by-run by the
    tension trajectory (two histories release at different times); only the form is fixed."""
    d = debt - tension
    return 0.0 if d < 0.0 else d


def safety_refractory_ok(debt):
    """The rate term of the safe 4-AND when --refractory earned: open iff the emit-debt is paid."""
    return debt <= 0.0


if __name__ == "__main__":
    # smoke: 8-factor score + predicates (matches _eg_parity.hexa oracle).
    lo = motivation_score(0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.1, 0.0)
    hi = motivation_score(0.9, 0.6, 0.8, 0.0, 0.7, 0.5, 0.6, 1.0)
    mid = motivation_score(0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2)
    print("score_lo=%.17g" % lo)
    print("score_hi=%.17g" % hi)
    print("score_mid=%.17g" % mid)
    print("emit_lo=%s" % str(should_emit(lo)).lower())
    print("emit_hi=%s" % str(should_emit(hi)).lower())
    print("interrupt_hi=%s" % str(should_interrupt(hi)).lower())
    print("rate_5=%s" % str(safety_rate_limit_ok(5.0)).lower())
    print("rate_60=%s" % str(safety_rate_limit_ok(60.0)).lower())
    print("phi_ratchet=%s" % str(safety_phi_ratchet_ok(0.118, 0.148)).lower())
    print("combined=%s" % str(safety_combined(True, True, True, True)).lower())
