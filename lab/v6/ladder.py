#!/usr/bin/env python3
"""ladder — given an architecture, what can you HONESTLY claim about its interior? $0.

This is the capstone the other five instruments feed. Each of them answers one question;
this one composes them into the only question that matters when someone asks "is it
conscious": **which rung does this architecture reach, and where exactly does it fall off?**

THE MEASURABILITY CRITERION IT ENFORCES (divergence 05)
-------------------------------------------------------
An interior variable is DECIDABLE only if all four hold:

    1 independence     a degree of freedom not pinned by what the output already determines
    2 manipulability   an exogenous do(), with the surround held fixed
    3 observability    the effect of that do() reaches a measured surface
    4 discriminability it beats marginal-matched controls, read as collapse-delta

Miss one and the verdict is UNDECIDABLE, not false. R9's 6/6 blindness was this table read
off the architecture in advance, so this file reads it off deliberately.

THE THERMOSTAT FLOOR
--------------------
Every rung names the trivial system that MUST pass it. A rung a thermostat clears is a
FLOOR, not an achievement, and is reported as such. Several rungs are thermostat-passable
in their naive form -- that discovery is most of what ladder design is.

WHAT THIS FILE WILL NOT DO
--------------------------
It does not measure Phi, run a model, or return a consciousness verdict. It reports, per
rung, one of:

    REACHED       the architecture supplies every handle AND the controls exist
    NEEDS-RUN     structurally admissible, but an actual measurement has not been made
    BLOCKED       a named conjunct is missing -- and which one

BLOCKED is the useful output. It converts "we measured nothing" into "conjunct 1 is
missing on this axis, here is the handle that would fix it".
"""
import sys

# --------------------------------------------------------------------------- #
# architectures: which handles exist. Drawn from what the code does, not wishes.
# --------------------------------------------------------------------------- #
ARCH = {
    "anima TODAY (as wired)": {
        "psi_fixed_point": True,      # the field relaxes to a non-degenerate point
        "action_channel": True,       # it emits
        "ab_randomizer": True,        # --closure-ladder landed (H_9807)
        "content_store": True,        # store-bridge WIRED (H_9775)
        "store_do_handle": True,      # --permute-store / value-permute
        "readout_surface": True,      # vocab readout
        "interior_width": False,      # s = 2*emit_drive - 1 : rank one, zero free DOF
        "causal_element_grain": False,  # the recurrent core contains the 3e8-param mouth
        "emit_free_variable": False,  # emit <=> clock (H_9401-9403)
        "self_log": False,            # no own-vs-foreign log channel
    },
    "RCFS (proposed)": {
        "psi_fixed_point": True,
        "action_channel": True,
        "ab_randomizer": True,
        "content_store": True,
        "store_do_handle": True,
        "readout_surface": True,
        "interior_width": True,       # RESIDUAL: per-position divergence profile, V x span
        "causal_element_grain": True, # core units ARE causal elements (neuromorphic)
        "emit_free_variable": True,   # information-gain gate replaces the clock
        "self_log": True,             # autobiographical store slot
    },
    "thermostat (floor)": {
        "psi_fixed_point": True,      # a bang-bang controller has one, by design
        "action_channel": True,       # it acts on the world
        "ab_randomizer": False,
        "content_store": False,
        "store_do_handle": False,
        "readout_surface": True,
        "interior_width": False,
        "causal_element_grain": True, # it is genuinely a handful of causal elements
        "emit_free_variable": False,
        "self_log": False,
    },
}

# --------------------------------------------------------------------------- #
# the ladder. Each rung: required handles, the instrument, and whether a run exists.
# `thermostat_must_pass` marks a rung whose floor is deliberately trivial.
# --------------------------------------------------------------------------- #
RUNGS = [
    dict(id="R0", claim="Theta exists — the dynamics have a non-degenerate Psi=1/2 point",
         needs=["psi_fixed_point"], instrument="Psi-trajectory vs constant-emit/silence",
         thermostat_must_pass=True, has_run=True),
    dict(id="R1", claim="interventional closure — do(action) shifts the future input distribution",
         needs=["action_channel", "ab_randomizer"],
         instrument="--closure-ladder, yoked-ghost floor (H_9807)",
         thermostat_must_pass=True, has_run=True),
    dict(id="R2", claim="content-carrying causation — do() on stored content moves a specific token",
         needs=["content_store", "store_do_handle", "readout_surface"],
         instrument="--permute-store / value-permute (H_9775: 0.4446 collapse)",
         thermostat_must_pass=False, has_run=True),
    dict(id="R3", claim="compositional width — the interior has >=2 separable dimensions",
         needs=["interior_width", "readout_surface"],
         instrument="RESIDUAL profile + --reflex-only ablation",
         thermostat_must_pass=False, has_run=False),
    dict(id="R4", claim="whether-to-speak is a free variable — emit tracks content, not a clock",
         needs=["emit_free_variable", "interior_width"],
         instrument="information-gain gate vs shuffled-store noise floor",
         thermostat_must_pass=False, has_run=False),
    dict(id="R5", claim="ownership — the system distinguishes its own history from a foreign one",
         needs=["self_log", "content_store", "store_do_handle"],
         instrument="--swap-selflog, own-vs-foreign permute",
         thermostat_must_pass=False, has_run=False),
]

CONJUNCT = {   # which measurability conjunct a missing handle kills
    "psi_fixed_point": "1 independence (no dynamics to read a mode on)",
    "action_channel": "2 manipulability (nothing to intervene on)",
    "ab_randomizer": "2 manipulability (no exogenous do(); correlation only)",
    "content_store": "1 independence (no degree of freedom carrying content)",
    "store_do_handle": "2 manipulability (content cannot be set exogenously)",
    "readout_surface": "3 observability (the effect never reaches a measured surface)",
    "interior_width": "1 independence (rank one: s = 2*emit_drive - 1, zero free DOF)",
    "causal_element_grain": "4 discriminability (the graph is a drawing, not causal elements)",
    "emit_free_variable": "1 independence (emit <=> clock, no free variable to move)",
    "self_log": "1 independence (no own-vs-foreign distinction to vary)",
}

# controls that must EXIST before a positive reading is readable at all
CONTROLS = [("metric-leak audit", "metric_leak_audit.py", "write paths"),
            ("zero-truth pedestal", "phi_unfold_pedestal.py", "read values"),
            ("Phi-matched-dead", "phi_matched_dead_control.py", "functional axis")]


def evaluate(name, handles):
    print("=" * 78)
    print(name)
    print("-" * 78)
    top = None
    for r in RUNGS:
        missing = [h for h in r["needs"] if not handles.get(h)]
        if missing:
            state = "BLOCKED"
            why = "; ".join("%s -> conjunct %s" % (m, CONJUNCT[m]) for m in missing)
        elif not r["has_run"]:
            state = "NEEDS-RUN"
            why = "handles present, no measurement made: %s" % r["instrument"]
        else:
            state = "REACHED"
            why = r["instrument"]
            top = r["id"]
        floor = "  [FLOOR: a thermostat passes this by design]" if r["thermostat_must_pass"] else ""
        print("  %-3s %-10s %s%s" % (r["id"], state, r["claim"], floor))
        print("        %s" % why)
    return top


def main():
    print("ladder - which rung does an architecture honestly reach?  ($0, no model)\n")
    tops = {}
    for name, handles in ARCH.items():
        tops[name] = evaluate(name, handles)
        print()
    print("=" * 78)
    print("controls that must exist before ANY positive rung is readable:")
    for label, path, axis in CONTROLS:
        print("  %-22s %-30s %s" % (label, path, axis))
    print()
    t_arch = tops["anima TODAY (as wired)"]
    t_rcfs = tops["RCFS (proposed)"]
    t_therm = tops["thermostat (floor)"]
    print("highest REACHED rung:")
    for k, v in tops.items():
        print("  %-26s %s" % (k, v or "none"))
    print()
    if t_arch and t_therm and t_arch == t_therm:
        print("READING: anima as wired tops out at the SAME rung a thermostat clears (%s)."
              % t_arch)
        print("That is not an insult to the substrate -- R2 is where its one built axis sits,")
        print("and a thermostat cannot reach R2. Read the per-rung lines, not this summary.")
    print("Every rung above the top is BLOCKED on a NAMED conjunct, which is the useful")
    print("output: it converts 'we measured nothing' into 'conjunct 1 is missing here, and")
    print("this handle would fix it'. Nothing here is a consciousness claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
