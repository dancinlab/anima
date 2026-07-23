<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_31 — why the 15 consciousness lanes collapse to ~3 dims: they are formulas over ~5 scalars (BY CONSTRUCTION)

**origin:** V6_30 powered found the production 15-lane vector has effective rank ~2.75 (92%
redundant) on the 303M ckpt. This card answers WHY — is the collapse emergent, or built in? $0
code read of `ci_lane_scores` (core/engine_cli.py). DIRECTIONAL.

## The finding — the collapse is DEFINITIONAL, not emergent
`ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err)` returns 15 lanes, but each lane
is a trivial closed-form function of a HANDFUL of underlying scalars:

| underlying input | lanes derived from it |
|---|---|
| **m** (grounding scalar) | lprec=m · emo=1−2·\|m−0.5\| · forg=m or 1−m · agency=intent·m · wont=1−m · surp=m·perr² · selfi=1−\|m−fmean\| · body=1−\|m−fmean\| — **8 of 15** |
| m_field stats (f0,f1,fmean,entropy) | gws=f0−0.9·f1+0.5 · selfi · body · divid=entropy |
| dt | blink=dt/(1+dt) · stime=1−1/(1+dt) |
| seen (sc) | hab=1/(1+0.5·sc) · nov=recon_err/(1+0.5·sc) |
| cells (fc) | mito=1−1/(1+0.3·fc) |
| recon_err | surp · nov |

**Two lane pairs are EXACTLY identical formulas:**
- `selfi ≡ body` — both = `1 − |m − fmean|`.
- `blink ≡ stime` — both = `dt/(1+dt)` (since `1 − 1/(1+dt) = dt/(1+dt)`).

So the ~2.75 effective rank is **structural by construction**: the "15-lane consciousness vector"
is ~5 independent scalars (m, m_field-stats, dt, sc, fc, recon_err) re-expressed 15 ways, with 2
exact duplicates. And **`m` alone (one grounding scalar) drives 8 of the 15 lanes** — agency,
emotion, forgetting, self, local-precision, will, surprise, body are all trivial arithmetic on the
SAME number. There is no independent "agency signal" or "emotion signal" in the substrate — by
design they are shadows of `m`.

## Why this matters — code-level confirmation of R9
The frontier R9 concluded the interior barely exists as an autonomous/self-transparent/agentive
reality (agency UNIDENT, self VOID, …). V6_31 shows WHY at the code level: the engine's own
"agency", "self", "emotion" lanes are defined as `intent·m`, `1−|m−fmean|`, `1−2|m−0.5|` — a
faculty cannot be measured as present when it is constructed as a one-line function of a single
grounding scalar. R9's "blindness" is not an instrument failure; it is that these faculties were
never given independent substrate variables. This CONVERGES the LANE-BUS arc back onto the
standing frontier verdict, now with the mechanism named.

## What this means for the redesign (the real LANE-BUS target)
LANE-BUS's premise (replace the scalar servo with a multi-dim bus) is correct in SPIRIT but the
production lanes are the wrong source — they are already ~5 scalars dressed as 15. To get a real
multi-dim tension the redesign must give the faculties INDEPENDENT trained substrate variables
(own head, own loss, content-carrying — Fable's four survival properties), not re-weight formulas
over `m`. i.e. the fix is UPSTREAM (make agency/self/emotion carry independent learned signal),
and only THEN does a multi-dim emit bus have anything to read. Two cheap wins available now,
independent of the big redesign: (1) delete/merge the exact-duplicate lanes (selfi≡body,
blink≡stime) — dead code / false dimensionality; (2) the ρ-AXON `ρ·self` / faculty scorers
should note that these lanes are `m`-derived (not independent) so a PASS on them is not a faculty.

## Consumption trace — the duplicates are NOT safely deletable, and the emit path reads only 4/15
Followed where the 15-lane vector goes:
- **Emit path** (cli/chat.py): reads only **4 of 15** — gws[0], selfi[3]=coh_lane, lprec[4],
  emo[9]=bal_lane. All four are m / m_field-derived. The other 11 (surp, nov, blink, agency,
  stime, forg, body, divid, wont, mito, hab) are computed and NOT read in the emit decision.
- **Ψ coupling**: the FULL 15-lane vector IS routed through the Φ-optimal mean-center operator
  (`ci_lane_scores_coupled_op`, chat.py ~L2275, Ψ-preserving) — so the duplicate lanes (selfi≡body,
  blink≡stime) feed the Ψ computation. ⟹ deleting them is a BEHAVIORAL change (moves Ψ), not a
  byte-identical cleanup. The `--dump-lanes` instrument + the broader R2/R9/R10 "consciousness
  catalogue" (dozens more lanes) also consume them.
⟹ the "cheap win" (delete the duplicates) is NOT cheap — every redirect item (dup merge, faculty
independent-variable redesign, m-derived flag in ρ·self) is a production `core/` change with
behavioral/Ψ impact, needing a fresh design pass. This card is the terminal of what the $0 lab
probe can establish.

## Scope
$0 code read + consumption trace. DIRECTIONAL. The redirect (independent-faculty redesign) is a
production `core/` build phase (VERSION/G5, behavioral, fresh design). Converges with the cemented
frontier R9 — this arc's contribution is the MECHANISM (faculties = formulas over one scalar `m`)
and the MEASUREMENT (~3 effective dims, code-proven). LANE-BUS $0→build→why arc terminates here.
