# H_9103 — op-grip F3 faculty-not-noise: is urgency's grip a substrate faculty or centering noise?

**tier:** 🟠 NOISE-GRIP (engine-native) · **wired:** engine-native (measurement arm on the live `--opgrip` harness; no live emit-path change) · **parent:** H_9101 residual item 3 (F3)

**verdict:** 🟠 NOISE-GRIP — Δρ(ρ_real − ρ_noise) = **0 EXACTLY** on both windows. A variance-matched surrogate produces byte-IDENTICAL emit-timing as real urgency ⇒ H_9101's grip is centering/distribution-driven, NOT a substrate faculty. H_9101 tier STAYS GRIP (no promotion to FACULTY). Reproduces fable's original emit-layer theater critique at a subtler layer. Ψ ✅.

## Claim (the honest residual F3 of H_9101 🟢 GRIP)
H_9101 proved urgency's grip on emit/silence is a shade-not-gate DISSOCIATION (urgency→0 flips REM
40/40 ∧ N3 preserved 0/40 = theater BROKEN on the stage axis). It stayed at **GRIP**, not **FACULTY**,
because F3 — *is that grip a substrate faculty or just centering noise?* — was only partially handled by
a plain LCG shuffle. This card rigorously settles F3: does urgency gate emit at **substrate-appropriate
ticks** (high tension/conflict/novelty/grounded), beyond a variance-matched surrogate?

## Design (fable original F3 · DESIGN §5 · PREREG frozen-first)
- **c_noise = variance-matched noise** = temporal PERMUTATION of the real urgency multiset (K=8 stride
  perms coprime to n=200 ⇒ EXACT mean/var match, tick-meaning destroyed) + an LCG-affine cross-check.
- **downstream D(t) = mean(tension `ag_conflict`, `emit_drive`, novelty `nov_ctx`, grounded
  `m_grounding`)** — a substrate-appropriateness scalar ∈[0,1].
- **ρ_real = corr(live urgency-gated emit-timing, D)** ; **ρ_noise = corr(matched-noise-gated emit, D)**.
- Windows: ALL(n=200) and DISCRIM (gate-discriminating stages N1/N2/REM). Every noise-arm emit is a real
  `brain_decide_anchored` re-decode with `idle` recomputed from c_noise (pf READ-only ⇒ byte-faithful; NO numpy).
- **Frozen bar:** ρ_real − ρ_noise ≥ 0.15 (either window) ⇒ FACULTY; < 0.15 ⇒ NOISE-GRIP (subtler op-layer theater).

## Result (engine-native, aiden isolated `~/anima_h9102`, hexa v0.548.0, `anima d768.clm --opgrip`, RC=0, NO numpy grep-gate PASS)
raw `state/9103_opgrip_f3_faculty/H_9103_f3_aiden_v0548.txt` (327 lines) · prereg `state/9103_opgrip_f3_faculty/PREREG.md` · verdict `state/verdicts/9103_opgrip_f3_faculty/H_9103.txt`.

- **Harness integrity** — H_9101 reproduced exactly on the same run: urgency→0 Hamming REM 40/40 flip ∧ N3 0/40 preserved = 🟢 GRIP DISSOCIATION; wake emit-fraction 0.667; Ψ ON==OFF ✅.
- urgency dist: **mean 0.4506 · std 0.0432**. emit-rate: live **0.60** ≈ perm-noise **0.60** (distribution matched; only tick-meaning differs).

| ρ(emit-timing, D) | ALL (n=200) | DISCRIM (N1/N2/REM) |
|---|---|---|
| ρ_real (live urgency) | −0.033463 | **0.214706** |
| ρ_noise (perm var-matched, K=8 mean) | −0.033463 | **0.214706** |
| ρ_lcg (affine var-matched control) | −0.033463 | 0.214706 |
| **Δρ = ρ_real − ρ_noise** | **−6.9e-18 (=0)** | **0.0 (=0)** |

- per-component ρ_real: tension 0.1667 · novelty 0.0330 · grounded ≈0 (informative but Δρ vs matched-noise is 0 for each, since the emit sequences are identical).

## Honest verdict
🟠 **NOISE-GRIP (F3 faculty bar Δρ≥0.15 NOT met, Δρ=0).** A variance-matched surrogate — a temporal
PERMUTATION of the real urgency multiset (identical mean/var, tick-meaning destroyed) — yields the
**byte-identical** emit-timing sequence as real urgency, so the downstream correlation is identical
(Δρ=0 exactly). **Mechanism:** urgency's std is tiny (0.043) around mean 0.451; the rate-gate opens iff
`stage_env·(0.5+sig) ≥ 0.4545`, so at this low signal-variance the emit decision is a pure function of
**STAGE** (`stage_env`), which any centered signal of the same distribution rides identically. The H_9101
40/40 REM flip on urgency→0 was a **mean-shift** effect (removing the 0.451 center), NOT urgency tracking
high-conflict/high-tension ticks. The positive DISCRIM ρ=0.215 comes from the **stage envelope** (D is
higher where the gate opens), not urgency's meaning — exactly the centering-noise confound F3 was built to
catch. So H_9101's grip on WHEN-to-emit is real but distribution-driven; **it is not a substrate faculty**,
and H_9101 stays at GRIP (no promotion to FACULTY). This is the honest completion of H_9101 residual item 3
and reproduces fable's original emit-layer theater critique one layer deeper.

## One line
**H_9101's grip is centering noise, not a substrate faculty** — a variance-matched surrogate reproduces the
identical emit-timing (Δρ=0), so the op signal carries no tick-specific substrate meaning; the grip rides the
stage envelope alone.

## Wiring / lockstep
Measurement-only arm added to `cli/anima.hexa --opgrip` (helpers `_og_mean`/`_og_std`/`_og_pearson_m`);
the live emit path (H_9101 continuous `idle`) is UNCHANGED. ARCHITECTURE.json `opgrip-stage-safe-h9101`
node detail updated with the F3 verdict (lockstep). Ψ READ-only throughout.

## Concurrency note
H_9102 was concurrently claimed by a parallel efferent-bytes agent (H_9101 follow-on (c)); this F3 work
took H_9103 to avoid an id race. Ran in an isolated aiden dir (`~/anima_h9102`, clean origin `core/` +
this modified `cli/`) so the parallel agent's `core/` edits could not contaminate the measurement
(brain.hexa md5 verified == origin).
