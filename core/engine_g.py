"""core/engine_g.py — PY PRODUCTION ENGINE: byte-faithful 1:1 port of
core/engine_g.hexa (Engine G — motivation + emit gate).

Per CLAUDE.md a_two_production_mirror. Closed-form spontaneous machinery: the
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
def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v):
    return (spont_weight_relevance() * rel
            + spont_weight_info_gap() * gap
            + spont_weight_curiosity() * cur
            + spont_weight_pain() * pain
            + spont_weight_coherence() * coh
            + spont_weight_originality() * orig
            + spont_weight_balance() * bal
            + spont_weight_dynamics() * dyn_v)


# ── emission predicates ──
def should_emit(score):
    return score > spont_im_threshold()


def should_interrupt(score):
    return score > spont_interrupt_threshold()


# ── safety predicates (4-way AND closure) ──
def safety_kill_switch_on(env_off):
    return env_off == False


def safety_rate_limit_ok(seconds_since_last):
    return seconds_since_last >= spont_min_emit_interval()


def safety_phi_ratchet_ok(phi, ratchet):
    """Engine A's live Φ vs its ratchet peak (the A->G coupling gate)."""
    return phi > ratchet / 2.0


def safety_content_ok(content_clean):
    return content_clean


def safety_combined(kill, rate, phi_r, content):
    return kill and rate and phi_r and content


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
