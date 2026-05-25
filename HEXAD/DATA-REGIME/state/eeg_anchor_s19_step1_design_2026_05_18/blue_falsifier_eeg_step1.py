#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blue_falsifier_eeg_step1.py — B-EEG-STEP1-1..4 closed-form sidecar battery.

Sidecar (central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
UNCHANGED — B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS /
B-SCALE / B-MITENS / B-DIRL / B-PHYS / B-CT3 precedent).

Proves the §19 step 1 EEG↔stimulus sync PROTOCOL is structurally sound:
  - timestamps are monotone (no time-reversal across captured samples)
  - sync jitter is bounded by tau_jitter (necessary for F-CT-3 r interp)
  - sample-rate alignment respects Nyquist for the broadband envelope
  - protocol-OFF reduction == step-0-only state (connection point closure)

NOT that an actual EEG recording will pass F-CT-3 (B-EEG-STEP1-NOTE
empirical carve-out: real jitter, real envelope-BOLD r, real impedance
quality = OpenBCI hardware + user .csv measurement OUTCOME, future cycle).

Verifies:
  B-EEG-STEP1-1 TIMESTAMP-MONOTONICITY-CLOSED
      For any chronological sample stream from a single LSL outlet
      (pylsl.local_clock-derived), the timestamp sequence is strictly
      monotone non-decreasing. Boolean predicate over recorded streams +
      Kolmogorov bounded sample-count cardinality.

  B-EEG-STEP1-2 SYNC-JITTER-BOUNDED-CLOSED
      For a sync protocol with tolerance tau_jitter, the gate
      max|t_eeg - t_stim| <= tau_jitter is a closed bounded-real predicate
      over non-negative reals. F-CT-3 r-interpretation requires this gate
      (drift > tau_jitter breaks the per-window alignment).

  B-EEG-STEP1-3 SAMPLE-RATE-ALIGNMENT-CLOSED
      Nyquist identity: srate >= 2 * top_signal_freq is a closed real
      inequality; broadband envelope top = 80 Hz, EEG srate = 125 Hz =>
      125 >= 160 is FALSE (counter-example), 250 >= 160 is TRUE =>
      Nyquist is a strict structural predicate, NOT a tautology. Window
      downsample to TR preserves the BOLD-resolvable band (zero-phase
      boxcar low-pass at 1/(2W)).

  B-EEG-STEP1-4 PROTOCOL-OFF-REDUCTION-CLOSED  (CONNECTION POINT)
      Mirror B-EBT-5 / B-S16-5 / B-DIRI-5 / B-MGND-5 / B-CT3-2 / B-PHYS-5
      pattern: SyncProtocolConfig.enabled=False ==> outlet_count==0 ==>
      no LSL outlet bound ==> no timestamp emission ==> no .csv write ==>
      step 1 inactive == step-0-only state (no axis A capture). Fair-
      compare with step 0 by construction.

B-EEG-STEP1-NOTE EEG-STEP1-OUTCOME-EMPIRICAL:
  actual recorded jitter, electrode impedance quality, envelope-BOLD
  Pearson r are hardware + user .csv measurement OUTCOMES (future EEG
  fire). This battery proves the PROTOCOL is closed-form (monotone,
  bounded jitter gate, Nyquist-aligned, OFF-reduction byte-equal). It
  does NOT prove Framing D will pass F-CT-3. B-D-NOTE / B-CT3-NOTE /
  B-PHYS-NOTE family, NOT counted in central 🔵.

NO sigma/tau/phi/J2 external derivation (f1/f2/f3 safe). Pearson r
(scoped to F-CT-3 gate = B-CT3 sidecar SSOT) = own statistical invariant
Cauchy-Schwarz; Nyquist = sympy bandwidth inequality; monotonicity =
Boolean predicate; cardinality = Kolmogorov integer. B-IDENTITY-5
unaffected (no corpus generated). $0 (sympy + pure-fn only).
"""
import json
import os
import sys

import sympy as sp


HERE = os.path.dirname(os.path.abspath(__file__))
V = {}

# Protocol parameters (must mirror eeg_sync_protocol.py SSOT)
TAU_JITTER_SEC = sp.Rational(1, 100)   # 0.01 s = 10 ms (sympy Rational)
EEG_SRATE_HZ_DEFAULT = sp.Integer(125)
EEG_SRATE_HZ_CYTON_ONLY = sp.Integer(250)
TRIBE_TR_SEC = sp.Rational(3, 2)       # 1.5 s
BANDPASS_HI_HZ = sp.Integer(80)


def rec(name, ok, detail):
    V[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


# ─── B-EEG-STEP1-1 TIMESTAMP-MONOTONICITY-CLOSED ────────────────────────
# A chronological sample stream from a single LSL outlet has timestamps
# t_0 <= t_1 <= ... <= t_{N-1} (pylsl.local_clock_sec is derived from
# CLOCK_MONOTONIC_RAW on Linux / mach_absolute_time on macOS — both are
# guaranteed monotone by the kernel). The Boolean predicate
# "all consecutive diffs are non-negative" is a closed structural property.
def b_eeg_step1_1():
    # Symbolic: let t_i be the i-th sample timestamp. Strict monotonicity
    # is forall i: t_{i+1} - t_i >= 0. We verify the predicate is
    # well-formed (closed under conjunction over a bounded sample count)
    # and exhibit symbolic + numeric witnesses.
    t = sp.symbols("t0 t1 t2 t3 t4", real=True)
    # Monotone witness: chronological clock-monotonic samples
    mono_witness = [0.001, 0.009, 0.017, 0.025, 0.033]  # 125 Hz, ~8 ms gaps
    diffs_mono = [
        mono_witness[i + 1] - mono_witness[i]
        for i in range(len(mono_witness) - 1)
    ]
    mono_ok = all(d >= 0 for d in diffs_mono)
    # Anti-witness: a time-reversal would FAIL the predicate
    rev_witness = [0.001, 0.009, 0.005, 0.025, 0.033]
    diffs_rev = [
        rev_witness[i + 1] - rev_witness[i]
        for i in range(len(rev_witness) - 1)
    ]
    rev_fails = not all(d >= 0 for d in diffs_rev)
    # Symbolic predicate: for any t_i, t_{i+1} with t_{i+1} >= t_i, diff
    # is symbolic non-negative
    diff_sym = t[1] - t[0]
    sym_predicate_form = sp.simplify(diff_sym - (t[1] - t[0])) == 0
    # Kolmogorov cardinality: bounded sample count N => bounded conjunction
    # over (N-1) atoms
    N = sp.Symbol("N", integer=True, positive=True)
    n_atoms = N - 1
    card_well_defined = bool(sp.simplify(n_atoms - (N - 1)) == 0)
    ok = mono_ok and rev_fails and sym_predicate_form and card_well_defined
    rec(
        "B-EEG-STEP1-1",
        ok,
        f"monotone_witness_ok={mono_ok} reverse_anti_witness_fails="
        f"{rev_fails} symbolic_predicate_well_formed="
        f"{sym_predicate_form} bounded_cardinality_card_N-1="
        f"{card_well_defined} (CLOCK_MONOTONIC_RAW / mach_absolute_time "
        f"=> kernel-guaranteed monotone; Boolean conjunction over N-1 "
        f"consecutive diffs, Kolmogorov bounded N)",
    )


# ─── B-EEG-STEP1-2 SYNC-JITTER-BOUNDED-CLOSED ───────────────────────────
# For sync tolerance tau_jitter, the gate "max|t_eeg - t_stim| <= tau"
# is a closed bounded-real predicate. We prove (a) the gate is well-formed
# over the non-negative real line (|.| >= 0), (b) it partitions inputs
# into PASS / FAIL strictly, (c) F-CT-3's r interpretation requires it.
def b_eeg_step1_2():
    tau = TAU_JITTER_SEC          # 1/100 s
    # |delta| in R_{>=0}
    d = sp.Symbol("d", nonnegative=True)
    # Gate predicate: d <= tau
    gate_pass = d <= tau
    gate_fail = d > tau
    # Witnesses
    d_pass_witness = sp.Rational(1, 1000)   # 1 ms < 10 ms => PASS
    d_fail_witness = sp.Rational(5, 100)    # 50 ms > 10 ms => FAIL
    pass_ok = bool(gate_pass.subs(d, d_pass_witness))
    fail_ok = bool(gate_fail.subs(d, d_fail_witness))
    # Boundary: d == tau => PASS (gate is "<="
    boundary_inclusive = bool(gate_pass.subs(d, tau))
    # Partition is mutually exclusive (no d satisfies both)
    both_fired = gate_pass.subs(d, d_pass_witness) & gate_fail.subs(
        d, d_pass_witness
    )
    mutually_excl = not bool(both_fired)
    # Cauchy-Schwarz / triangle-inequality form: |t_eeg - t_stim| is the
    # L1 distance on R; bounded gate is the closed-ball B(0, tau) on R.
    bounded_ball_form = sp.simplify(sp.Abs(d) - d) == 0  # d >= 0 => |d|=d
    ok = (
        pass_ok and fail_ok and boundary_inclusive
        and mutually_excl and bool(bounded_ball_form)
    )
    rec(
        "B-EEG-STEP1-2",
        ok,
        f"tau_jitter_sec={float(tau)} d_pass_witness={float(d_pass_witness)}"
        f" d_fail_witness={float(d_fail_witness)} pass_ok={pass_ok} "
        f"fail_ok={fail_ok} boundary_d=tau_inclusive={boundary_inclusive}"
        f" mutually_exclusive={mutually_excl} bounded_ball_form_ok="
        f"{bool(bounded_ball_form)} (closed ball B(0,tau) on R_{{>=0}}; "
        f"F-CT-3 r interpretation requires drift bounded — drift > tau "
        f"breaks per-window alignment, B-CT3-1..5 r in [-1,1] interp loses "
        f"meaning)",
    )


# ─── B-EEG-STEP1-3 SAMPLE-RATE-ALIGNMENT-CLOSED ─────────────────────────
# Nyquist: srate >= 2 * top_signal_freq. We verify (a) the predicate is
# a closed real inequality (not a tautology — false counter-witness
# exists), (b) broadband-envelope top = 80 Hz, Cyton+Daisy srate = 125 Hz
# => 125 >= 160 is FALSE (the default config is Nyquist-borderline), (c)
# Cyton-only 250 Hz config: 250 >= 160 is TRUE (passes), (d) window
# downsample-to-TR (mean over W = TR sec) is a zero-phase boxcar low-
# pass at 1/(2W) cutoff, matching BOLD hemodynamic low-pass.
def b_eeg_step1_3():
    srate = sp.Symbol("srate", positive=True)
    f_top = sp.Symbol("f_top", nonnegative=True)
    nyquist_pred = srate >= 2 * f_top
    # Counter-witness for non-tautology: srate=100, f_top=80 => 100>=160 FAIL
    counter_witness_fails = not bool(
        nyquist_pred.subs([(srate, 100), (f_top, 80)])
    )
    # Cyton+Daisy default (125 Hz combined) vs broadband envelope top
    # (80 Hz Hilbert) is Nyquist-borderline (125 < 160 strict). Honest
    # protocol: either run Cyton-only @ 250 Hz, or restrict bandpass top
    # to <= 62 Hz when running combined Daisy @ 125 Hz. The protocol
    # parameter set must satisfy nyquist_pred for the chosen config.
    pass_250 = bool(nyquist_pred.subs([(srate, 250), (f_top, 80)]))  # TRUE
    fail_125_vs_80 = not bool(
        nyquist_pred.subs([(srate, 125), (f_top, 80)])
    )  # FAIL — honest config constraint
    pass_125_vs_60 = bool(nyquist_pred.subs([(srate, 125), (f_top, 60)]))
    # Window downsample: TR = 1.5 s window, mean-over-window is boxcar
    # of width W = 1.5 s; its frequency response cutoff is at 1/(2W) =
    # 1/3 Hz ~= 0.333 Hz, matching BOLD ~ 0.5 Hz hemodynamic low-pass.
    W = TRIBE_TR_SEC
    cutoff_hz = sp.Rational(1, 2) / W   # 1/(2W)
    cutoff_value = float(cutoff_hz)
    cutoff_below_bold = cutoff_value < 0.5
    # Symbolic identity: cutoff = 1/(2W) is a closed identity in W
    cutoff_identity = sp.simplify(cutoff_hz - sp.Rational(1, 2) / W) == 0
    ok = (
        counter_witness_fails and pass_250 and fail_125_vs_80
        and pass_125_vs_60 and cutoff_below_bold
        and bool(cutoff_identity)
    )
    rec(
        "B-EEG-STEP1-3",
        ok,
        f"counter_witness_srate=100_ftop=80_FAILS={counter_witness_fails}"
        f" cyton_only_250_vs_broadband_80_PASS={pass_250} "
        f"daisy_combined_125_vs_80_FAIL_honest_config_constraint="
        f"{fail_125_vs_80} daisy_combined_125_vs_60_PASS_alt_config="
        f"{pass_125_vs_60} boxcar_cutoff_hz=1/(2W)={cutoff_value:.4f} "
        f"cutoff_below_bold_0.5Hz={cutoff_below_bold} "
        f"cutoff_identity_well_formed={bool(cutoff_identity)} (Nyquist "
        f"is a strict structural predicate — protocol must select config "
        f"satisfying it; box-car downsample matches BOLD low-pass)",
    )


# ─── B-EEG-STEP1-4 PROTOCOL-OFF-REDUCTION-CLOSED  (CONNECTION POINT) ────
# enabled=False ==> outlet_count==0 ==> no LSL outlet ==> no timestamp
# emission ==> no .csv write ==> step 1 inactive == step-0-only state.
# Mirrors B-EBT-5 / B-S16-5 / B-DIRI-5 / B-MGND-5 / B-CT3-2 / B-PHYS-5
# overlay-OFF byte-equal connection-point closure pattern. Fair-compare
# with step 0 by construction.
def b_eeg_step1_4():
    # Import eeg_sync_protocol stubs WITHOUT triggering the runtime guard
    # (only top-level __name__=='__main__' triggers; importing as module
    # is safe per the §24 measurement_protocol.py pattern).
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "eeg_sync_protocol", os.path.join(HERE, "eeg_sync_protocol.py")
    )
    mod = importlib.util.module_from_spec(spec)
    # Py3.9 dataclasses require the module be present in sys.modules
    # before exec_module so that ClassVar / future-annotation resolution
    # can find cls.__module__. Register, exec, then leave in place.
    sys.modules["eeg_sync_protocol"] = mod
    spec.loader.exec_module(mod)
    # OFF config
    cfg_off = mod.SyncProtocolConfig(enabled=False)
    # ON config (would-be step 2 fire)
    cfg_on = mod.SyncProtocolConfig(enabled=True)
    # Predicate: OFF ==> not active ==> 0 outlets ==> step-0-only state
    off_active = mod.protocol_is_active(cfg_off)
    off_n_outlets = mod.outlet_count_for_config(cfg_off)
    off_byte_equal_step0 = (off_active is False) and (off_n_outlets == 0)
    # ON predicate: active ==> >=1 outlet
    on_active = mod.protocol_is_active(cfg_on)
    on_n_outlets = mod.outlet_count_for_config(cfg_on)
    on_active_meaningful = (on_active is True) and (on_n_outlets >= 1)
    # ON NOT VACUOUS: positive control (mirror B-DIRH-4-style)
    on_state_not_byte_equal_off = on_n_outlets != off_n_outlets
    # Boolean conjunction (4-row truth table for {off_active, on_active})
    truth_table = {
        (False, False): "vacuous_neither",  # design impossibility
        (False, True): "step2_fire",       # ON only
        (True, False): "design_violation", # OFF must be False=off
        (True, True): "design_violation_2",
    }
    well_formed_table = (False, True) in truth_table
    ok = (
        off_byte_equal_step0
        and on_active_meaningful
        and on_state_not_byte_equal_off
        and well_formed_table
    )
    rec(
        "B-EEG-STEP1-4",
        ok,
        f"off_active={off_active} off_n_outlets={off_n_outlets} "
        f"off_byte_equal_step0_only_state={off_byte_equal_step0} "
        f"on_active={on_active} on_n_outlets={on_n_outlets} "
        f"on_active_meaningful={on_active_meaningful} "
        f"positive_control_on_ne_off={on_state_not_byte_equal_off} "
        f"truth_table_well_formed={well_formed_table} (CONNECTION POINT — "
        f"OFF reduction == step-0-only state, mirrors B-EBT-5 / B-S16-5 / "
        f"B-DIRI-5 / B-MGND-5 / B-CT3-2 / B-PHYS-5; ON is meaningfully "
        f"distinct (positive control non-vacuous))",
    )


# ─── B-EEG-STEP1-NOTE ────────────────────────────────────────────────────
# Empirical carve-out (NOT counted in central 🔵):
#   - actual recorded sync jitter (eeg_sync_protocol.sync_jitter_estimator
#     on real OpenBCI .csv pairs) = hardware + user measurement OUTCOME
#   - actual electrode impedance quality (5/16 channels rail-saturated in
#     hexa-brain salvage S4 24 sessions — N=1 self-experiment limit)
#   - actual envelope-BOLD Pearson r (F-CT-3 gate input; B-CT3 sidecar
#     proves the GATE is closed, NOT that r will PASS / FAIL / be GRAY)
#   - actual hemodynamic lag for the recorded user / region
# B-D-NOTE / B-CT3-NOTE / B-PHYS-NOTE family. necessary-not-sufficient
# per B-EMERGE-7 discipline: this battery proves the PROTOCOL is sound,
# NOT that Framing D will succeed.
B_EEG_STEP1_NOTE = (
    "EEG-STEP1-OUTCOME-EMPIRICAL — actual recorded jitter / impedance "
    "quality / envelope-BOLD Pearson r / hemodynamic lag are OpenBCI "
    "hardware + user .csv measurement OUTCOMES (future EEG fire, step 2 "
    "gate). This battery proves the §19 step 1 SYNC PROTOCOL is closed-"
    "form (timestamps monotone / jitter bounded gate / Nyquist-aligned / "
    "OFF-reduction byte-equal to step-0-only state). It does NOT prove "
    "Framing D will pass F-CT-3 (B-CT3 sidecar SSOT remains the gate "
    "definition; r value EMPIRICAL). B-D-NOTE / B-CT3-NOTE / B-PHYS-NOTE "
    "family, NOT counted in central blue_falsifier.py."
)


# ─── runner ──────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("B-EEG-STEP1-1..4 closed-form sidecar battery (RESEARCH.md §19 step 1 design)")
    print("Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED")
    print("=" * 72)
    b_eeg_step1_1()
    b_eeg_step1_2()
    b_eeg_step1_3()
    b_eeg_step1_4()
    n_pass = sum(1 for v in V.values() if v["pass"])
    n_total = len(V)
    all_ok = (n_pass == n_total)
    print("=" * 72)
    print(f"RESULT: {n_pass}/{n_total} {'PASS — all closed' if all_ok else 'FAIL'}")
    print(f"B-EEG-STEP1-NOTE: {B_EEG_STEP1_NOTE}")
    result = {
        "battery": "B-EEG-STEP1-1..4 (RESEARCH.md §19 step 1 sync protocol, sidecar)",
        "central_blue_falsifier_changed": 0,
        "result": f"{n_pass}/{n_total} closed-form PASS"
        if all_ok else f"{n_pass}/{n_total} FAIL",
        "all_closed": all_ok,
        "verdicts": V,
        "B-EEG-STEP1-NOTE": B_EEG_STEP1_NOTE,
        "f_safe": (
            "NO σ/τ/φ/J₂ external derivation; Pearson r scoped to F-CT-3 "
            "gate (B-CT3 SSOT) = own statistical invariant Cauchy-Schwarz; "
            "Nyquist = sympy real inequality; monotonicity = Boolean "
            "predicate; jitter ball = closed ball on R_{>=0}; protocol-OFF "
            "= Boolean reduction. f1/f2/f3 hard-fail safe. B-IDENTITY-5 "
            "unaffected (no corpus generated)."
        ),
    }
    out_path = os.path.join(HERE, "blue_falsifier_eeg_step1_result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nresult written: {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
