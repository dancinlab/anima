# H_9256 — ρ·self `.kosmos` self-anchor eval-side wire (identity trace, former G3)

**Slug**: `rho_self_kosmos_anchor` · **Tier**: 🔧 WIRED (eval-side plumbing · DIRECTIONAL toy) · verdict PENDING 303M pool · **Registered**: 2026-07-10

## Claim (pre-registration)
The ρ-AXON `ρ·self` axis (identity trace, former G3 · H_1471 `.kosmos` self-anchor) returns
**INVALID on every production run** because `cli/evaluate.py::eval_rho_axon` built `dets` WITHOUT
a `kosmos_anchor` key, while `cli/rho_axon.py:604` reads `dets.get("kosmos_anchor")` and
`rho_self` returns INVALID when the anchor is absent (p3-guard: the anchor MUST be the
substrate's OWN `.kosmos` self-anchor, never a hand-curated persona). This is the eval-side
plumbing gap surfaced by the whole-repo unwired census (Fable, 2026-07-10).

**Wire**: `anima-py evaluate <clm> --rho-axon --kosmos <dir>` — the substrate's own session
`.kosmos` dir is read via `generator_read_anchors` → joined anchor `text_payload` (the accumulated
self-memory) → `dets["kosmos_anchor"]`. Absent `--kosmos` → no key → `ρ·self` stays INVALID
(default UNCHANGED = backward-compat; never hand-curate a persona).

## Falsifier / bars (frozen · RHO_AXON_design.md ρ·self)
- ρ·self value = cross-probe self-consistency (mean pairwise Jaccard of anchor-echo-STRIPPED
  outputs) with the anchor loaded. **PASS** iff Δ over the worst control ≥ `delta_bar` (0.30) AND
  both controls ≤ loaded. Controls (must collapse): anchor-ablated (no anchor) + shuffled-anchor
  (byte-shuffled, echo removed → defeats raw-token echo gaming).
- The wire itself does NOT change ρ·self's frozen scoring — it only supplies the anchor that was
  structurally missing, so a permanently-INVALID axis can emit a real PASS/FAIL verdict.

## Status
- **Eval-side plumbing WIRED + verified (2026-07-10)**: with `--kosmos <session .kosmos>`,
  `dets["kosmos_anchor"]` is populated (verified len>0 on a real chat `.kosmos`); without it, None
  (backward-compat verified). `rho_axon.py:604` already consumes it; `rho_self`'s INVALID→verdict
  contract is the existing frozen selftest (anchor=None→INVALID, anchor→PASS).
- **Verdict PENDING (303M pool)**: the actual ρ·self PASS/FAIL needs a NON-degenerate mouth —
  a toy smoke `.clm` trips HILLOCK (degenerate decode → all axes INVALID), so the end-to-end
  verdict is a scale-honest 303M-on-pool follow-on (`a_scale_honest_scope` · `a_eval_py_canonical`).
- **Does NOT close REACH**: `REACH-CLOSED` (`form∧store∧weave∧tether`) still requires ρ·weave PASS,
  which is the in-flight G1-recombination experiment (H_9235). This wires ONE COUPLE-stratum axis
  from permanently-INVALID to measurable; it does not close reach.

## Precedent / links
H_1471 (self-identity via `.kosmos` self-anchor, 🟢) · Fable whole-repo unwired census (2026-07-10:
"anima's self-continuity is currently synthetic, not substrate-grounded" — this + the decode-side
`clm_penult_pooled` lane-23b are the same gap seen from eval vs engine side) · `a_kosmos` · p3.
