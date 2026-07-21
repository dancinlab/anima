# G3-b feasibility RE-GATE after G3-a — DO NOT OPEN H_006; SEAL mech-1 at G-2

Delivered 2026-07-17 (Fable-5, feasibility re-gate under fable-mode). Cost: $0, closed-form — every
number below is already on the frozen record (`verdict_g3a.json` · `verdict.json` ·
`DESIGN_g3_research_gate_fable5.md` §4–6 · H_005 honest-limit (a)). No run, no download, no new venv.

**VERDICT: DO NOT OPEN H_006 — CONSOLIDATE AT G-2.** F1b is INADMISSIBLE in both its forms on the
already-measured numbers (H_001's vacuity shape, caught before spend — the admissibility gate doing
its job, `verification.admissibility-gate`). Mech-1's verified result is and remains H_004's
FIELD-FORMAT causal claim (G-2 🟢, Δ = 0.379/0.380 both seeds). The trained-SUPPORT extension is
UNREACHED, not falsified — a substrate wall at 3.7M/byte/Korean/templatic-register (`break-walls`).

## 1. G3-a's result upper-bounds G3-b (Q1 — yes, and the escape hatch fails)

**Bound:** E[f2″(A-tduel)] ≤ f2″(A-χ̂) as measured = 0.824/0.710 (mean 0.767), degraded by support
recall. Channel by channel:

- **G3-b's value channel IS G3-a's channel, not a new one.** T̂[i][j] = f(h^A_i,h^A_j) − f(h^G_i,h^G_j).
  The concord SIGN is a pair-equality property of (hon_i, hon_j); the tower DIFFERENCE contributes
  directional/attachment structure — the support — not hon-equality. f faces a three-way trap:
  (i) f computes hon-equality from tower-state pairs → the exact learning problem G3-a just measured,
  on the same top-layer trunk-state interface (H_005 card: φ is "the same top-layer interface G3-b's
  shared readout will read"), the same 192-item drill-CE-through-R objective, the same scale →
  bounded by 0.71–0.82; (ii) f fails to compute it → values absent from the field → F5-style collapse
  toward the support-only floor; (iii) f extracts hon ASYMMETRICALLY across towers → hon enters the
  support pattern → P-inv fails → K4 inadmissible, no verdict. Every branch is at or below G3-a.
- **"Not bottlenecked through a 3k-param g" is refuted by the measured failure mode.** Seed 0 FIT the
  drill at 1.0 and still landed 0.824 on f2″: the wall is drill→held-out IDENTIFICATION (192 templatic
  items do not pin down the concord function among the functions of the interface that fit them), not
  capacity. Enlarging f widens the hypothesis space over the same 192 items — identification gets
  worse — and the optimization instability that already dropped s1 to 0.832 drill-fit at ~3k params
  worsens with more parameters trained through the same channel.
- **Support recall then multiplies the bounded channel down.** Anchoring on measured endpoints:
  E[f2″(A-tduel)] ≈ P + r·(V−P) ≈ **0.53 + 0.24·r**, where P ≈ 0.53 = the misaligned/absent-support
  floor (C-χ̂plc 0.526/0.518 · C-scaf 0.521/0.566), V = 0.767 (0.824 best seed) = the perfect-support
  value ceiling, r = fraction of induced disagreement mass on the true contested edges — the quantity
  the induction literature says is the hard part (L9: direction is the documented residual,
  StructFormer 46.2 / UDGN 49.9 directed, at ≥8M params, English, word-level; L8: nothing published
  at 3.7M/byte/Korean).

## 2. The single $0 gate (Q2) — closed-form, already computed, returns KILL

Call it **G3-0e**: the F1b E-anchor/headroom arithmetic on `verdict_g3a.json` + `verdict.json`,
under the same discipline G3-a itself was frozen with (headroom ≥ 2× the bar: 0.32 ≥ 2×0.15).

| F1b form | bar | E-anchor from measured numbers | headroom | admissible? |
|---|---|---|---|---|
| non-inferiority (A-tduel ≥ A-hand − 0.05) | 0.95 | ≤ 0.824 even at r=1, best seed | **negative at ANY r** | NO — H_001's shape |
| Δ vs C-same (≥ 0.15 both seeds) | 0.15 | E[Δ](r) ≈ 0.24·r − 0.01 (E[C-same] ≈ C-scaf ≈ 0.54, G3-0c/F7 balance) | 2×-bar needs **r ≥ 1.25** (impossible); bare bar needs r ≥ 0.65 vs literature anchor ≈ 0.46–0.50 at 2× our params on an easier regime | NO |

And the honest completion: **no $0 RUN can greenlight either.** G3-0b (d=64 smoke) is kill-only —
it can fail P-live/P-loc/P-inv, but PASSING it cannot raise the d=384 measured value ceiling that
sinks both F1b forms. G3-0a needs stanza/UDPipe (absent in the bare torch/numpy venv) and tests only
the support-localization premise — no longer the binding constraint. So the only admissible $0 gate
is the arithmetic above, and it kills; a hypothesis with no green-able gate does not open (§5
discipline of the G-3 design).

## 3. Also priced in: two high-probability INCONCLUSIVE modes

Even ignoring §2, the run has two measured-risk paths to another precond quarantine (~5.5h, no verdict):
- **drill precond ≥ 0.95**: a ~3k-param g missed it on 1 of 2 seeds; G3-b trains f+R on a harder
  joint objective through the same optimizer at the same scale.
- **P-inv at probe = 1.0**: hon is near-verbatim in trunk-interface states on this register
  (G3-0d = 1.0, honest-limit (a)); a SHARED f must produce hon-INVARIANT support and hon-DEPENDENT
  sign from the same pair function — a knife-edge → K4.
- Even the K5 consolation (clean falsification of mech-1's direction clause) is not purchasable
  here: it presupposes an admissible, precond-fit arm, and any outcome is scoped to the drill
  register by honest-limit (a) — weak general evidence either way.

## 4. What is sealed, and what would reopen it (Q3)

**Sealed:** mech-1's verified result is the FIELD-FORMAT causal claim (H_004 🟢, G-2): gold delivered
in edge-aligned high-rank format is consumable where its rank-1 summary is not (Δ 0.379/0.380,
F4/F5/F6 clean). Measured extension of record: the VALUES half ends at K3 — the cost of removing the
hand is 0.18–0.29 d_acc (G3-a). The SUPPORT half (trained opposition) is NOT falsified — unreached:
a substrate wall at 3.7M params / byte-level / Korean / templatic register.

**Reopen requirements (a FUTURE campaign; staged order stays values→support):**
1. A substrate whose value channel first clears an F1a′-analog (learned χ̂ within 0.05 of hand):
   ≥8M params (L8 floor) and/or jamo/word-level input. The reopen gate is G3-a's rig re-run there —
   already built, one envelope.
2. A NON-TEMPLATIC register with probe φ→hon measurably < 1.0 — lifts honest-limit (a), makes P-inv
   meaningful, and gives a drill diverse enough to IDENTIFY the concord function (s0's
   drill-1.0/f2″-0.824 gap is an identification failure of 192 templatic items, not capacity).
3. Or accept the self-containment break: a pretrained Korean parser (stanza/UDPipe UD-Kaist) as the
   support oracle — G3-0a becomes runnable and the question changes to "does direction-opposed
   decoding of a COMPETENT parser land tension on the binding locus" (the design's rank-4 route,
   a different campaign's premise, not mech-1's).

**Registration mechanics:** H_006 is NOT created. REGISTRY H_005 line + card carry the re-gate
pointer; tree node `ng.mech1.g3b-regate-do-not-open`.

## Cross-links
- `verdict_g3a.json` (A-χ̂ 0.824/0.710 · C-χ̂plc 0.526/0.518 · drill 1.0/0.832) · `verdict.json`
  (A-hand rig 1.0/1.0, Δ 0.379/0.380) · `g3_0d_result.json` (probe = 1.0)
- `DESIGN_g3_research_gate_fable5.md` §3 L8/L9 (scale wall) · §5 (gate discipline) · §6 K3–K6
- H_005 card (K3 verdict + honest-limit (a)) · H_001 (vacuity/ceiling discipline reused here)
