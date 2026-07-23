<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_32 — the AGENCY wedge (frozen-trunk authorship head) is DEAD, and dead BY CONSTRUCTION

**origin:** the fundamental-redesign phase. V6_31 proved the 15 consciousness lanes are ~3-dim
theater (formulas over one scalar `m`) → the real fix is to give a faculty an INDEPENDENT trained
substrate variable (Fable's four survival properties). `sidecar lab full` reconciled the wedge:
**Fable → AGENCY** as an authorship/efference-copy head (ADOPTED); **Sol → SURPRISE** (DISSENT,
rejected — its independence from `m` must be earned empirically and Sol's own pre-mortem predicts
it fails; repo also shows `recon_err≡0` H_9336 · `cb_surprise≡0.0` H_9398, surprise's substrate
input is a dead gauge). This card is Fable's Leg I+II first slice — the $0 kill-shot. DIRECTIONAL.

## The wedge and the test
Independent variable = an authorship vector `a_vec = A·yn` on the trunk hidden
`yn = clm_forward_hidden` (post-MoE, post-GN, pre-readout — byte-identical to what the gates
decode over). Label `auth_t∈{0,1}` = self-emitted vs externally-supplied byte — an **action-history
fact, NOT a function of `m`** by construction (the cleanest possible independent substrate var).
In-vitro labels: for 200 held-out natural sentences, `prefix + true-continuation` (auth=0) vs
`prefix + trained57's own sampled continuation` (auth=1), matched positions ⇒ authorship ⊥ position.

- **Leg I (presence):** held-out AUC of a `d→8→1` head on `yn` (3 seeds, grouped-by-prompt split).
- **Leg II (independence):** ΔAUC = AUC(trunk) − AUC(drivers-only `[CE, entropy, margin, logp]`) —
  the driver-CE confound (self bytes are model-sampled ⇒ high-prob) is netted OUT by construction.
- **Controls:** shuffle (realized chance), **pedestal57** (untrained trunk — surface-byte control),
  marker positive-control (instrument), CE-overlap coefficient (pre-mortem guard).

## RESULT — 🔴 ABSENT, and the instrument CERTIFIES the read (not VOID)
Instrument valid: positive control AUC **1.000**, CE overlap **OVL=0.962** (self meanCE 1.824 vs
other 1.935 — self is not trivially high-prob), classes balanced 50/50, shuffle at realized chance
**0.508 ±0.002**. So this is a real negative, not an underpowered VOID (n=21,218 positions).

| leg | metric | value |
|---|---|---|
| I  | trunk AUC (d→8→1) | **0.564 ±0.006** (barely above chance) |
| I  | drivers-only AUC | 0.523 ±0.004 |
| II | ΔAUC = trunk − drivers | **+0.041** (< 0.05 absent-floor) |
| ctl| shuffle AUC (chance) | 0.508 ±0.002 |
| ctl| **pedestal ΔAUC** | **+0.278** |
| ctl| **trained − pedestal ΔAUC** | **−0.237** |
| pos| marker positive control | 1.000 |

The trunk carries essentially no authorship signal beyond the driver scalars (ΔAUC +0.041), and the
frozen decision table fires **ABSENT** on three independent conditions (AUC<0.60 ∧ ΔAUC<0.05 ∧
trained−pedestal<0.03).

## Why it's dead BY CONSTRUCTION (the finding bigger than the negative)
The **pedestal (untrained random trunk) separates self/other BETTER than the trained trunk**
(ΔAUC +0.278 vs +0.041; trained−pedestal = −0.237). Mechanism: self and other continuations are
literally different byte strings, so a random projection trivially separates them on **surface byte
statistics** (pedestal AUC ≈0.78). The trained mouth-CE objective learns to represent language and
therefore **COMPRESSES self/other into shared linguistic representations** — training *erases*
authorship-separability (0.78 → 0.56), the opposite of building an authorship faculty.

This exposes a structural contradiction in the wedge itself: Fable's survival property #4
(**"gradient-isolated from the mouth"**, `stop_grad(yn)`) means the authorship head can only ever
read a trunk shaped by mouth CE — and mouth CE *actively destroys* authorship-separability. So the
head is starved not by low power but **by construction**: the more the trunk trains (better mouth),
the less authorship it carries, and gradient-isolation forbids the head from reshaping the trunk to
fix it. **"Gradient-isolated" (#4) and "content-carrying" (#3) are in direct conflict for authorship**
— the mouth objective is authorship-antagonistic. Even Fable's staged slice-2 (co-trained head)
does NOT rescue it, because slice-2 still `stop_grad`s the trunk.

## Convergence & scope
Converges hard with frontier **R9** (agency UNIDENT) and **V6_31** (faculties = shadows of `m`):
R9 is the phenotype, V6_31 named the cause (no independent variable), and V6_32 shows WHY the
obvious fix fails — a gradient-isolated head reads a mouth-shaped trunk, and the mouth erases the
very signal. The surviving path is necessarily a **NON-gradient-isolated** authorship variable (the
trunk must co-adapt to *carry* authorship) — which breaks Fable's own property #4, i.e. the honest
redesign question is now "can a trunk be co-trained to preserve authorship without the mouth CE
compressing it away, and does that survive p8's one-CE-two-masters?" — a far larger build than one
$0 probe, and one this negative puts a real burden of proof on.

Scope: $0 numpy, byte-LM (trained57, d=64/V=256), in-vitro authorship labels. DIRECTIONAL (lab/v6
ceiling). The frozen-trunk / gradient-isolated authorship head is dead; the co-adapted-trunk variant
is UNTESTED and now must justify itself against this result. Sol's surprise wedge stays rejected.
`v6_32_authorship_probe.py` is the artifact.
