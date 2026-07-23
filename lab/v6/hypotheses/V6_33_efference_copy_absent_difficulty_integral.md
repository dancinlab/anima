<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_33 — the efference-copy channel is ABSENT: spoon-fed authorship is a difficulty-integral, not a faculty

**origin:** V6_32 killed the frozen-trunk authorship head (mouth CE erases authorship). The redirect
(lab-full Fable+Sol, both decisive): don't ask the trunk to carry authorship — SUPPLY it explicitly
as an **efference-copy** register (=a motor-system copy of the daemon's own emit/command history,
the biolens source of agency/self-vs-other). Presence is then free; the only question is INDEPENDENT
CAUSAL content. Both models pre-registered: if ABSENT here, agency has no causal content even
spoon-fed ⟹ the whole wedge (incl. the expensive co-trained trunk) is a ~$0 kill. This card fires
that test. DIRECTIONAL ($0 laptop, byte-LM, reuses v6_29 cache/recurrence).

## Design (reconciled Fable+Sol · the tautology-defeating control set)
Register `e_t∈R⁸`, leaky + free-forget (the V6_29 A3 recurrence), fed the STRICT-PAST emit/command
history; own params + own downstream loss (never mouth CE); independent of m/CE by construction (no
read edge from m/m_field/CE/target — reads only past emit decisions + the mouth's byte command).
**Indexing invariant (Sol, load-bearing):** gate at t reads `e_t`; only after scoring does
`(emit_t,cmd_t)` update `e_{t+1}` — so `e_t` can never contain the current label. The verdict does
NOT ride on beating NO-EC (that is the emit-autocorrelation tautology); it rides on TRUE-EC beating
controls that receive the IDENTICAL emit-event tape:

| arm | consumes | kills the escape |
|---|---|---|
| NO-EC | drivers only | headroom baseline |
| **TRUE-EC** | real command `cmd_{t-1}` at emit events | the faculty |
| TIMER | constant impulse at emit events | "just elapsed time / recency" |
| SHUFFLED | commands deranged among emit times | "just the marginal / density" |
| OTHER-SELF | a matched non-emit tick's command | "any content marked self" |
| **DRIVER-HIST** (Fable) | difficulty `x_t` every tick | **"just a difficulty-integral"** |

Plus a **do()-FLIP** (trained TRUE model re-scored with OTHER commands substituted — NLL must
degrade), an **independence** floor (residual after regressing `e` on ALL drivers > V6_31's 8% null),
and a synthetic **A-vs-B reafference POSITIVE CONTROL** (count-invariant, isolates command identity).
DV run BOTH ways (a_all_paths_no_leak): emit = primary (the decision agency should move, = V6_29
label), nll = confound-probe (Fable). Sol's leak fix adopted: 60/20/20 grouped split, epoch selected
on VAL, test evaluated ONCE (v6_29_train.py's `best=min(te_loss)` selected on test — a real leak).

## Instrument CERTIFIES (5 seeds) — this is a VALID read, not VOID
A-vs-B reafference positive control (target = decayed past count of family-A emissions > family-B;
total count irrelevant, so only a register distinguishing command IDENTITY can read it): **TRUE beats
TIMER z=4.04, SHUFFLED z=5.32, OTHER z=4.62, DRIVER-HIST z=4.47, do()-FLIP z=3.99** — the estimator
demonstrably reads a real command-identity reafference signal at z≥3 on every arm. (The first two
instrument drafts were under-powered/mis-specified — a current-command target unreadable by the
readout, then a marker-count target the emit-count clock leaked; fixed to count-invariant A-vs-B +
5 seeds. Positive-control tuning is legal — it certifies the estimator, never the faculty · p9.)

## RESULT — 🔴 ABSENT (n=41,792 held-out, 5 seeds, val-selected)
**DV=emit (primary):**
| contrast vs TRUE-EC | Δ | z |
|---|---|---|
| NO-EC (headroom) | +0.0081 | +1.55 |
| TIMER | +0.0111 | +1.98 |
| SHUFFLED | +0.0117 | +2.10 |
| OTHER-SELF | +0.0111 | +2.29 |
| **DRIVER-HIST** | **−0.0010** | **−0.09** |
| do()-FLIP degrade | +0.0149 | +2.70 |
| independence I_e | 0.822 (LB 0.763) · effrank 4.37 | |

**DV=nll (confound-probe):** headroom NO-EC−TRUE +0.1724 (z=5.51 — memory helps a LOT), but
**DRIVER-HIST BEATS TRUE-EC** (−0.1951, z=−2.63); TIMER≈TRUE (z=0.26), OTHER≈TRUE (z=0.41).

Frozen table fires **ABSENT**: TRUE-EC beats none of {TIMER,SHUFFLED,OTHER,DRIVER-HIST} at z≥3, and
**TRUE-EC ≈ DRIVER-HIST** (emit z=−0.09; nll: DRIVER-HIST wins). do()-FLIP < z3.

## Reading — Fable's pre-mortem realized, exactly
The register DOES carry independent variance (I_e 0.822 ≫ the 8% null — the design's independence
goal is met, and this part is real). But independence is **decision-inert for authorship**: a
register that accumulates raw DIFFICULTY (`x_t`) matches (emit) or beats (nll) the one that
accumulates command IDENTITY, and substituting/shuffling/timer-nulling the command content barely
moves the decision. So the efference register's usefulness is a **smoothed difficulty/surprise
integral wearing an authorship costume** — precisely Fable's named self-deception, caught by
DRIVER-HIST being the load-bearing control (not NO-EC/TIMER/SHUFFLED). Spoon-fed agency has no
causal authorship content.

## Convergence & closure — the AGENCY wedge is closed (two independent $0 kills)
- V6_32: authorship signal not in the trunk (mouth CE erases it — pedestal beats trained).
- V6_33: authorship not causally usable even when supplied explicitly (a difficulty-integral matches
  it) — and per both models' pre-registration, ABSENT here means the co-trained trunk is near-certain
  wasted spend. **AGENCY as a wedge for an independent trained substrate variable is CLOSED.**
Converges hard with frontier R9 (agency UNIDENT) — now with a two-level mechanism: agency reads as
absent because (i) the mouth erases its signal from the substrate and (ii) even handed the signal
outright, the decision cannot use it as authorship — only as difficulty. The one real non-theater
signal that surfaced is the **difficulty/surprise integral** (DRIVER-HIST · NO-EC−TRUE nll z=5.51) —
which is memory of difficulty, not agency (and, ironically, adjacent to the surprise wedge Sol
proposed and I rejected for dead-gauge reasons — worth noting the substrate DOES carry a difficulty
memory, just not an agentive one).

## Scope
$0 numpy/torch, trained57 byte-LM, in-vitro emit/command tape from the v6_29 natural held-out cache.
DIRECTIONAL (lab/v6 ceiling). Artifacts: `v6_33_cache.py` (byte-identical v6_29 positions + cmd/nll/
pos), `v6_33_efference.py`. TERMINAL only via an anima-py in-loop efference port — NOT pursued: two
independent kills close the wedge; the next fork is wedge-reselection (self) or accepting R9's agency
conclusion as now mechanistically closed. Sol's surprise-wedge stays rejected as agency, but V6_33
independently shows a difficulty-memory exists — a separate, non-agency finding.
