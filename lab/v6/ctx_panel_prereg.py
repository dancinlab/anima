"""V6_20 -- derive and FREEZE this panel's bar BEFORE the first run.

V6_19 established the panel runs on the existing --weave-panel flag and showed the frozen
0.30/0.15 bar is not readable for it: that bar was calibrated for the 12-item recombination
battery, and reading V6_18's forced-choice numbers against it compares two different readouts.
Deciding the bar after seeing a run is tune-to-green, so it gets decided here.

The bar is NOT an absolute rate. measurement-metalaw: FORM is tunable, BIND is earned -- the
signal is the collapse-delta over controls, never a raw value (p7). So what has to be frozen
is: which contrast, what minimum effect, at what power, and every cell of the judgment table
including the below-chance ones (prereg-table-must-cover-below-chance).

Everything here is arithmetic on n and the design. No model is touched, nothing is fired.
"""
import math

N_ITEMS = 4385      # V6_19 emitted panel
N_DOCS  = 3083      # independent documents the items came from
ALPHA   = 0.01      # two-sided
POWER   = 0.90

z_a = 2.5758        # z_{1-alpha/2}, alpha=.01
z_b = 1.2816        # z_{power},     power=.90

m    = N_ITEMS / N_DOCS                       # mean items per document
RHO  = 0.20                                   # assumed intra-document correlation (stated, not measured)
DEFF = 1 + (m - 1) * RHO                      # design effect from clustering
N_EFF = N_ITEMS / DEFF

print("=" * 78)
print("PRE-REGISTRATION — frozen before the first run  (V6_20)")
print("=" * 78)
print(f"  panel items ............ {N_ITEMS:,}")
print(f"  independent documents .. {N_DOCS:,}   ({m:.2f} items/doc)")
print(f"  design effect .......... {DEFF:.3f}   (rho={RHO} assumed, NOT measured -- see honesty note)")
print(f"  effective n ............ {N_EFF:,.0f}")
print(f"  alpha {ALPHA} two-sided · power {POWER}")
print()

# ---- the contrast: paired binary, same items under intact vs each control -> McNemar ----
print("=" * 78)
print("THE CONTRAST — paired, McNemar (same items, two arms)")
print("=" * 78)
print("  primary   Delta_FORM = rate(intact) - rate(swap_cue)    transport, not echo")
print("  primary   Delta_BIND = rate(intact) - rate(bind_cue)    transport, not local window")
print("  floor     rate(null)                                    unprompted base rate")
print("  PASS requires BOTH deltas positive and significant, AND the floor below both controls.")
print("  A single significant delta is NOT a pass -- either control alone has a trivial explanation.")
print()

# McNemar MDE: with discordant-pair proportion p_d, detectable delta ~ (z_a+z_b)*sqrt(p_d/n)
print("%-28s %12s %12s" % ("discordant pairs p_d", "MDE (delta)", "as % points"))
print("-" * 78)
for p_d in (0.05, 0.10, 0.20, 0.30, 0.50):
    mde = (z_a + z_b) * math.sqrt(p_d / N_EFF)
    print("%-28s %12.4f %11.2f%%" % (f"{p_d:.2f}", mde, 100 * mde))
print("-" * 78)
mde20 = (z_a + z_b) * math.sqrt(0.20 / N_EFF)
print(f"  At a plausible p_d=0.20 the panel detects {100*mde20:.2f} percentage points.")
print(f"  Sol's reference: 212 IID items are powered only for ~13 points. This is ~{13/(100*mde20):.0f}x finer.")
print()

# ---- the frozen minimum interesting effect --------------------------------------------
MIE = 0.05
print("=" * 78)
print("FROZEN: minimum interesting effect")
print("=" * 78)
print(f"  MIE = {MIE:.2f} on BOTH deltas.")
print(f"  Chosen ABOVE the {100*mde20:.2f}-point resolution so the panel is not merely reporting")
print("  its own precision, and set now so it cannot be moved after a run.")
print()

# ---- the full judgment table, below-chance cells included ------------------------------
print("=" * 78)
print("JUDGMENT TABLE — every cell, including below-chance")
print("=" * 78)
rows = [
 ("both deltas >= MIE, both significant, floor lowest",
  "TRANSPORT PRESENT", "highly informative -- see the asymmetry below"),
 ("both deltas >= MIE but floor >= a control",
  "INVALID", "the floor is not a floor; instrument fault, not a result"),
 ("exactly one delta >= MIE",
  "UNDECIDABLE", "one control alone always has a trivial reading"),
 ("both deltas in (0, MIE)",
  "BOUNDED-NULL", "report the TOST interval, never 'no effect'"),
 ("both deltas ~ 0 (TOST equivalent)",
  "ABSENT-AT-THIS-CORPUS", "NOT a faculty verdict -- V6_16 predicts it"),
 ("either delta significantly NEGATIVE",
  "INSTRUMENT-DEAD", "a control beating the intact arm means the arms are mislabelled or leaked"),
 ("intact rate at or below the null floor",
  "INSTRUMENT-DEAD", "the panel is not measuring the cue at all"),
]
print("%-52s %-24s" % ("outcome", "verdict"))
print("-" * 78)
for cond, verdict, note in rows:
    print("%-52s %-24s" % (cond, verdict))
    print("%-52s   %s" % ("", note))
print()

print("=" * 78)
print("THE ASYMMETRY, restated so it cannot be forgotten at read time")
print("=" * 78)
print("  measurable sites 4,385   vs   training-pressure events 24 (V6_16)")
print("  A POSITIVE is strong: the lane learned transport on ~24 pressure events.")
print("  A NEGATIVE is nearly empty: the supply measurement already predicts it, so")
print("  ABSENT-AT-THIS-CORPUS may NEVER be written up as a faculty wall.")
print()
print("=" * 78)
print("HONESTY NOTES")
print("=" * 78)
print("  1. rho=0.20 is ASSUMED, not measured. It only scales the MDE; measure the realized")
print("     intra-document correlation on the first run and report the MDE with the realized rho.")
print("  2. Seeds: minimum 2, majority read, oracle-valid runs only")
print("     (single-retrain-outlier-faked-a-refutation). Seed replication is not item power.")
print("  3. Whole-corpus held-out CE must stay inside a frozen non-inferiority band (Sol), or a")
print("     'pass' could be a lane that bought transport by damaging the trunk.")
print("  4. This table is frozen as of this commit. Re-anchoring after a run is tune-to-green")
print("     (burned-gate-no-refreeze-sequential-gating).")
