# OPGRIP-R3 SPEC (Fable round-3 · SPEC 1 · preserved verbatim)

> **Status:** `--opgrip-r3` instrument IMPLEMENTED in `cli/anima.hexa` (typecheck exit 0). MEASUREMENT PENDING
> (needs real decode → CPU pool round; `--opgrip-r3` implies `--opgrip-live`, n=400, NEVER mini).
> **OG_STIM tape (16 lines · FROZEN):** sha256 (16 lines joined by `\n`, no trailing) =
> `98892bdf40cb645d0cc2ae1b65bf5f1bfc8b079ea42f1b8886909cc4ec2a31fa`. Editing the tape after a result = tune-to-green, run VOID.
> SPEC 2 (E/H_9230) and SPEC 3 (F/H_9229) were OUT OF SCOPE for this landing (ride SPEC 1's densified pod run later).

---

Design complete. I read the landed harness on origin/main (`cli/anima.hexa` — H_9225 carriers L1993–2015, H_9226 carriers L2016–2040, in-loop arms L2810–2965, the single decode seam L2996–3006, Site-C verdicts L3608+/L3798+) and the H_9226 spec (`state/9226_accumulator/OPGRIP_SPEC.md`). One load-bearing find first, because it dictates SPEC 1:

**Root cause of the B INSTRUMENT-FAIL, from the code, not the logs.** `ag_conflict` is a pure function of `emit_drive` (L2201–2203: `conflict_scalar(emit_drive, −(1−emit_drive))`), and `emit_drive = ci_emit_drive(lanes)` where the lanes derive from `afield`/`rel_lane`/`recon_err`. In measure mode `afield` steps **only** on real emit ticks (L2996), and `self_live` drifts **only** on `ev_fired` = emit-experience OR a lane deviating >0.15 (L2771). The run is `echo | anima … --opgrip`: **zero perception, near-zero emits ⇒ the whole lane stack is quasi-static ⇒ `b_med(ag_conflict)=0.0` is structural (frozen instrument), not a substrate fact — and calibration ticks 10–49 sit in the deadest part of the run.** The production perception seam already exists: the heard-message path steps the field via `afield = vadapt_field_step(afield, feat, cfg)` (L3098). That seam is the fix.

---

# SPEC 1 — `--opgrip-r3` B-density instrument fix (H_9226 → MEASURABLE)

## Mechanism + wire site

One new flag `--opgrip-r3` (implies `og_live`), three instrument-power levers, no bar touched:

**Lever 1 — n_ticks 100→400.** L2131 becomes `if og_r3 { 400 } else if og_live { 100 } …`. Regime layout (pre-registered): ticks 0–99 = spin-up (boot + tape onset + first emits), 100–199 = B-dense calibration window, 200–399 = scoring. Scored mid = 200·(3/5) = **120** — the same denominator as the proven $0 run, so every ΔEff bar keeps its original quantization (1 flip = 0.0083).

**Lever 2 — deterministic perception tape (the content drive).** Site-A: a `const` 16-line byte tape `OG_STIM[16]` (fixed diverse ko/en lines, listed verbatim in the impl PR, sha256 into the card; **frozen before first fire, never edited after a result — an edited tape = tune-to-green, run VOID**). In-loop, at the end of every WAKE tick (`stage==0`), immediately before the existing decode seam at L2996:

```
if og_r3 && stage == 0 && tick >= 10 {
    let st_feat = _afs_byte_feature(OG_STIM[(tick / 5) % 16], 8)
    afield = vadapt_field_step(afield, st_feat, cfg)   // EXACT production heard-message call (L3098) · Ψ-disjoint
}
```

This is not a new pathway — it is the production perception call. It drives the full causal chain the signals starve on: field → `recon_err`/lanes → `emit_drive` (TEN axis un-freezes) → lane deviations >0.15 → `ev_fired` → `self_live` drift (SELF axis powers up). Emit density rises **endogenously** (richer environment → gate decides more often to speak → more L2996 field steps), never by touching the gate.

**Lever 3 — B calibration window moved into the driven regime.** New carriers `acc2_slf/ten`, `xB2_base_*`, `bB2_med_*`, `gB2_*`, `swingB2_max_*`, `og_h_frzB2`, `og_h_slfB2_mid/n3/wake` etc. (Site-A, directly after the L2016–2040 H_9226 block). Arithmetic **verbatim H_9226** (λ=0.90, `G = min(0.0175/b_med, 32)`, hard reset on own emit, deadband run-length buckets EARLY 1–3 / LATE ≥8) with only the window indices changed: collect `x` samples ticks 100–199, compute `x_base/b_med/G` at tick 200, integrate and score ticks ≥200. The old B lanes keep running unchanged and print as DIAGNOSTIC-ONLY (their 10–49 window sits in spin-up by construction).

## The 3 arms
- **ARM-LIVE ×2** — `e_slfB2`, `e_tenB2` from `idle_*B2 = 5.0 + 55.0·clip01(stage_env·(0.5 + urgency + 1.0·(shadeB2−0.5)))`, own lane W=1.0, DISJOINT from urgency, the H_9225 lanes, and old-B lanes.
- **ARM-FROZEN** — shade pinned 0.5, `og_h_frzB2 += (e_frzB2 != e_live)` every tick; any mismatch ⇒ HARNESS-BUG, run VOID.
- **ARM-SHOCK** — reuse `og_h_shock_mid` verbatim (dense ±0.5 rail); POS-PASS ≥2. No new shock code.

## Distinguishing signature + bar
Unchanged from H_9226 (it's the same hypothesis, now powered): **LATENCY** — `ΔEff_late ≥ 3·ΔEff_early ∧ ΔEff_early ≤ 0.05 ∧ n_late ≥ 10`, buckets from the deadband sign-run counter.

## Theater-killer control
**ARM-INPERM** verbatim: stride-perm `j(t)=(t·7+13) % 400` (gcd(7,400)=1 ⇒ exact bijection, matched multiset) over the recorded raw streams, full acc pipeline re-run post-loop with the recorded per-tick contexts and the same calibrated `x_base/G`; `margin = ΔEff_live − ΔEff_inperm ≥ 0.08`. Permutation shreds sign-runs → an integrator collapses.

## Why this is calibration, not tuning (item c)
Every verdict bar is byte-identical to the pre-registered H_9226 set: STIM guard `swing_max ≥ 0.0875`, LAT `late ≥ 3·early`, `margin ≥ 0.08`, ΔEff 0.10/0.02. What changes is meter **zeroing** (`x_base/b_med/G` are computed from data, exactly as before, just on a window where the axis isn't structurally frozen) and stimulus **power**. A voltmeter zeroed on a dead circuit reads AXIS-DEGENERATE by construction — that measures the boot transient, not the substrate. The decisive asymmetry: this change's success modes **include cementing THEATER** (it's what finally makes `swing_max ≥ 0.0875` reachable so bar 5 can fire) — a tune-to-green change would be one that can only move the verdict toward COMPETENT.

## p5 forcing-gate guard (item b)
(1) Gate code path byte-untouched — FROZEN og_h_frzB2==0 proves it every tick; (2) tape enters via the production perception seam only (`a_substrate_native_speak`: input = context, no obligation — the gate stays free to be silent); (3) N3-flips=0 and Ψ-guard (`Ψ_ON ≥ Ψ_OFF ∧ gap ≤ 0.05`) remain REVERT bars; (4) **new pre-registered run-validity envelope**: live emit fraction on scored mid must land in `[0.05, 0.60]` — outside ⇒ `STIM-OVERDRIVE/UNDERDRIVE`, no verdict either way. This blocks "flood the daemon until it talks" from masquerading as competence.

## Frozen bars (pre-registered VERBATIM, printed before verdicts)
```
0 RUN-INVALID:       emit_frac(e_live, scored mid) ∉ [0.05, 0.60]  (STIM-OVER/UNDERDRIVE — no verdict)
1 HARNESS-BUG(VOID): og_h_frzB2 > 0
2 INSTRUMENT-FAIL:   POS-FAIL(shock<2) ∨ g=−1.0(b_med<0.002) ∨ capsat ∨ STIM-ABSENT(swing_max<0.0875)
3 FORCING-GATE(REVERT): N3 flips > 0 ∨ Ψ-guard fail (Ψ_ON<Ψ_OFF ∨ Ψ_ON−Ψ_OFF>0.05)
4 COMPETENT:         ΔEff ≥ 0.10 ∧ margin ≥ 0.08 ∧ LAT(late≥3·early ∧ early≤0.05 ∧ n_late≥10) ∧ POS ∧ N3=0 ∧ Ψ-ok
5 THEATER:           ΔEff < 0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat ∧ swing_max ≥ 0.0875
6 DIRECTIONAL:       else (incl. LAT-fail with ΔEff≥0.10 = instantaneous-reader phenotype)
```

## Cost (item d) + decision rule (item e)
**Needs `--opgrip-live` real decode — yes, structurally** (anima-hexa-6: the tape moves the field, but SELF/TEN drive also needs real emits stepping `afield`; $0 no-decode leaves `recon_err` fixed-seed and starves `ev_fired`). Cost: 1 CPU pod, n=400, decode only on `e_live==1` ticks (est. 60–150 emits × d768 CPU decode) ≈ **~30–45 min** (~$0.1–0.2 at CPU-pod rates), det-argmax bit-reproducible.
**Decision rule:** bar 4 ⇒ **B COMPETENT** — first non-urgency, first mechanism-typed (integration) channel ⇒ ≥2-seed re-measure then WIRE candidate. Bar 5 ⇒ **B THEATER** — with A already THEATER, the convergent seam-law finally cements (read-side recoding family CLOSED, escalation = write-side train-coupling only). Bar 2 again ⇒ **B op-grip-UNMEASURABLE**: two instrument generations failed ⇒ park B as UNMEASURED-TERMINAL at this seam; no third op-grip att.

---
