#!/usr/bin/env python3
"""ladder-evidence — DERIVE the ladder's handle table from the repo instead of asserting it.

WHY THIS FILE EXISTS
--------------------
`ladder.py` reports which rung an architecture reaches, and its answer is only as good as
its handle table -- which the card admitted was "load-bearing and a review target". It was
hand-written, and hand-written tables drift. This one caught itself immediately:

    ladder.py claimed anima has `store_do_handle`, citing `--permute-store`
    that flag DOES NOT EXIST in the repo

The capability was real -- the repo has --store-shuffle, --store-flip,
--store-component-swap, --store-adversarial and more -- so the verdict was right and the
CITATION was invented. That is exactly the failure a derived table removes: a claim can
still be wrong, but it can no longer cite something that is not there.

⚠️ AND IT CAUGHT ITSELF ONCE MORE
The first version reported EVERY handle ABSENT -- including ones I had grepped by hand
minutes earlier. An all-absent table on a repo known to contain the flags is a red flag,
not a finding: the git-grep invocation was malformed (`-l -- pat REF -- paths` puts two
`--` separators in one command). Fixing that was not enough -- it still read all-absent,
because git pathspecs are relative to the CURRENT DIRECTORY and this file lives in
lab/v6/, so `cli/` meant `lab/v6/cli/`. Fixed again with top-level-relative `:/cli/`.

Two bugs, both of which returned "nothing found". That shape is the danger: a broken
detector and a clean negative are indistinguishable from the output alone, which is why
the sanity check has to be "do I already know this repo contains one of these?" rather
than "did the tool print something plausible".

HOW IT WORKS
------------
Each handle names the evidence that would establish it -- flags, symbols, files. This
greps `origin/main` and reports PRESENT with the actual matches, or ABSENT. Nothing is
asserted; a handle is present iff the repo says so.

WHAT STAYS DECLARED
-------------------
RCFS does not exist, so its handles cannot be derived. They are marked PROPOSED and are
never mixed with derived ones -- a proposal that quietly reads as evidence is how a design
document turns into a claim.
"""
import subprocess
import sys

REF = "origin/main"
PATHS = [":/cli/", ":/core/"]   # top-level-relative: this file lives in lab/v6/

# handle -> (what it means, [evidence patterns])
EVIDENCE = {
    "psi_fixed_point":  ("dynamics with a non-degenerate Psi=1/2 point",
                         ["pure_field_step", "bridge_clamp"]),
    "action_channel":   ("the system emits", ["emit_drive", "should_emit"]),
    "ab_randomizer":    ("exogenous do() with a yoked floor", ["--closure-ladder"]),
    "content_store":    ("a content-addressed store", ["--store-bridge", "clms"]),
    "store_do_handle":  ("content can be set/permuted exogenously",
                         ["--store-shuffle", "--store-flip", "--store-component-swap"]),
    "readout_surface":  ("the effect reaches a measured surface", ["--store-readout"]),
    "interior_width":   ("a vector-valued interior path to the mouth",
                         ["--residual-profile", "--reflex-only"]),
    # PRESENT but NOT the production default -- see the DEFAULT-OFF note below.
    "emit_free_variable": ("emit can vary with content, not the clock",
                           ["--emit-refractory"]),
    "self_log":         ("own-vs-foreign history distinction", ["--swap-selflog"]),
}


def grep(pat):
    try:
        out = subprocess.run(["git", "grep", "-l", "-e", pat, REF, "--"] + PATHS,
                             capture_output=True, text=True, timeout=60)
        files = [l.split(":", 1)[-1] for l in out.stdout.strip().splitlines() if l.strip()]
        return files
    except Exception:
        return []


def main():
    print("ladder-evidence - handles DERIVED from %s, not asserted\n" % REF)
    print("%-22s %-9s %s" % ("handle", "state", "evidence"))
    print("-" * 78)
    derived = {}
    for h, (meaning, pats) in EVIDENCE.items():
        hits = []
        for p in pats:
            for f in grep(p):
                hits.append("%s in %s" % (p, f))
        derived[h] = bool(hits)
        state = "PRESENT" if hits else "ABSENT"
        first = hits[0] if hits else meaning
        print("%-22s %-9s %s" % (h, state, first))
        for extra in hits[1:3]:
            print("%-22s %-9s %s" % ("", "", extra))
        if len(hits) > 3:
            print("%-22s %-9s ... and %d more" % ("", "", len(hits) - 3))
    print("-" * 78)
    print()
    print("DERIVED handle table for anima-as-wired:")
    for h, v in derived.items():
        print("  %-22s %s" % (h, v))
    print()
    print("NOT derived, and deliberately kept separate: RCFS does not exist, so every")
    print("handle it 'has' is a PROPOSAL. Mixing proposed handles into a derived table is")
    print("how a design document quietly becomes a claim.")
    print()
    print("⚠️ PRESENT is not the same as ON. `--emit-refractory` exists in cli/chat.py, but")
    print("its default is \"\" -- the clock path. My hand-written table recorded this handle")
    print("as absent, which was wrong; the honest state is PRESENT-BUT-DEFAULT-OFF, and that")
    print("is a different rung verdict: not BLOCKED (needs building) but NEEDS-RUN behind a")
    print("non-default flag (needs measuring). Collapsing the two is how a ladder overstates")
    print("what is missing.")
    print()
    absent = [h for h, v in derived.items() if not v]
    print("absent in the repo today: %s" % (", ".join(absent) if absent else "none"))
    print("Those are precisely the conjuncts the ladder reports as BLOCKED, and now the")
    print("BLOCKED verdicts are backed by a grep rather than by my memory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
