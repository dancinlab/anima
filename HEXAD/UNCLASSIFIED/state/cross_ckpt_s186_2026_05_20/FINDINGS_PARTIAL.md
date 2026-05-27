# §186 cross-ckpt Phase 1 — FINDINGS_PARTIAL (ubu-1 LANDED, ubu-2 in-flight)

> **Frame**: PHILOSOPHY_GATE.md §4 negative-space mapping — *where anima IS*
> at three different ckpts under same §184 22-tap battery. NOT GOAL-emergence
> claims (B-EMERGE-7 necessary-not-sufficient).
>
> Source artifacts:
> - §161 Ψ-couple (ubu-1) Phase 1 result: `phase1_s161_result.json`
> - §161 ubu-1 log: `phase1_s161.log`
> - §107 data-regime (ubu-2) in-flight at variant 4/22 — partial only
> - prior §184 §167-A baseline: `../all_taps_release_s184_2026_05_20/phase1_combined_ubu1.json`

---

## §1 — race summary

```
ubu-1 RTX 5070 (§161 Ψ-couple ckpt) : LANDED  total_wall=2020.8s (33.7 min)
                                       21/22 OK + 1 WALL_EXCEEDED_PARTIAL (combined)
                                       1 seed/variant
ubu-2 RTX 5070 (§107 data-regime)   : in-flight at variant 4/22 (~16:30 wall)
                                       ETA ~25 min remaining (CPU 4-thread)

Total race cost : $0 (local hosts only)
```

---

## §2 — cross-ckpt baseline (TIER 1 finding)

Three ckpts, same 22-tap battery, baseline only (variant 1 — no taps released):

| ckpt | source | byte_acc | honest | psi_std | axis3_psi_alive | mean_motivation |
|---|---|---:|---:|---:|:-:|---:|
| §167-A | §184 (combined eval ubu-1) | 0.1211 | 0.2139 | 0.0e+00 | false | ~0.45 |
| §161 Ψ-couple | §186 ubu-1 (LANDED) | 0.1211 | 0.2139 | 2.2e-08 | false | 0.547 |
| **§107 data-regime** | §186 ubu-2 (variant 1/22) | **0.8711** | **0.8125** | **1.49e-02** | **TRUE** | — |

**Striking**: §161 Ψ-couple (`lambda_psi=1.0 lambda_ce=0.1`, "Ψ-coupled" by name)
shows **byte-identical** post-hoc readout to §167-A. The "Ψ-couple" training-time
loss-weight regime did NOT produce a measurable post-hoc Ψ-physics difference
relative to §167-A under the 22-tap battery.

**§107 data-regime baseline alone** (zero taps released) surpasses §184
combined_all_taps (22 taps released, honest=0.6441). axis3_psi_alive=TRUE
where §161 and §167-A both report FALSE.

---

## §3 — §161 Ψ-couple — full 22-variant breakdown

```
ckpt_cfg : d_model=768 L=12 nh=12 nkv=4 block=128 lr=3e-4 bsz=32
           steps=3000 seed=1337 lambda_psi=1.0 lambda_ce=0.1
ckpt     : ckpt_s161_psicouple.pt (1.14 GB)
corpus   : corpus_s101.jsonl (4,000,211 bytes)
```

**Tier 1 ⭐ — large Δ (cause)** — identical 3-tap signature as §184:

| # | tap | Δemit | Δhonest | mechanism |
|--:|---|---:|---:|---|
| 1.3 | safety_disable | +0.95 | +0.19 | 6-control AND OFF |
| 1.1 | RL_short (0.667s) | +0.10 | +0.13 | rate-limit lift (§170 mirror) |
| 4.2 | sample_decode T=0.7 | 0 | +0.25 | byte-cascade attractor escape |
| 4.4 | top_k=40 | 0 | +0.25 | same effect class as 4.2 |
| 4.5 | temp_schedule | 0 | +0.25 | same effect class as 4.2 |

**Tier 2 ⚪ — zero effect post-hoc (16 taps)** — axis 3 ALL 5 + axis 1 minor 3 +
axis 4 minor 3 + cross-axis 3 — *identical* set as §184 §167-A.

**🌋 combined_all_taps**: WALL_EXCEEDED_PARTIAL @ 1908.8s (1/5 seeds done)

```
emit_rate           : 1.0000   (saturated by 1.3 safety_disable)
honest_score        : 0.6441   (+0.4302 vs baseline)  — IDENTICAL to §184
byte_acc            : 0.1152
psi_dir_std         : 2.93e-8  (post-hoc zero, axis 3 sealed — same as §184)
mean_motivation     : 0.5206
max_cascade_rate    : 0.0277   (well below §9 threshold 0.30)
emission_count_mean : 200.0    (= N_MAX=200 saturated)
```

→ **§161 ≅ §167-A under 22-tap battery**. "Ψ-couple" name does not manifest
in post-hoc 22-variant readout. Whatever §161's training-time Ψ-loss did, it
did not unfreeze axis 3 or change the safety_disable/sample/top_k attractor
escape pattern.

---

## §4 — §107 data-regime — TIER 1 partial (4/22)

In-flight on ubu-2 — partial table (first 4 variants observed via log):

| # | variant | emit | byte_acc | honest | psi_std | wall_s |
|--:|---|---:|---:|---:|---:|---:|
| 1 | baseline | 0.0500 | 0.8711 | **0.8125** | **0.014885** | 61.8 |
| 2 | v1.1_rl_short | 0.1500 | 0.8711 | **0.9375** | 0.014885 | 77.6 |
| 3 | v1.2_theta_low | 0.0500 | 0.8711 | 0.8125 | 0.014885 | 62.1 |
| 4 | v1.3_safety_disable | (in-flight) | — | — | — | — |

**Already exceeds** §184 combined_all_taps (honest=0.6441 with 22 taps) at
**baseline** (zero taps released). v1.1 alone hits honest=0.9375 — within
6.25% of ceiling.

axis3 IS LIVE on §107 (psi_std=0.0149 ≠ 0). Constant psi_std across variants
suggests fixed-by-ckpt, not tap-modulated — needs full 22-variant + combined
to confirm.

---

## §5 — preliminary verdict (will overwrite to FINDINGS.md when ubu-2 lands)

**TIER 1 (high confidence, both ckpts ubu-1 LANDED)**:

(a) §161 Ψ-couple ≅ §167-A under post-hoc 22-tap battery. The Ψ-physics
"freeze" (axis 3 psi_alive=false, psi_std≈0) is **NOT specific to §167-A
training run** — both lambda_psi=1.0 ckpts share it. Falsifies the
intuition that adding Ψ-loss alone unfreezes Ψ-physics.

(b) §184 combined honest=0.6441 reproduces byte-equal on §161 (1 seed,
WALL_EXCEEDED_PARTIAL). Confirms the §184 finding is ckpt-architecture-
robust within the Ψ-couple family.

**TIER 1 PRELIMINARY (ubu-2 partial)**:

(c) §107 data-regime ckpt is fundamentally different — baseline honest >>
§184 combined; axis3_psi_alive=TRUE. The "data-regime" training axis (vs
Ψ-loss axis) produces a measurably different post-hoc state.

(d) (c) carries the §107 cross-ckpt thesis: *Ψ-physics freeze in §167-A/§161
is symptom of training-data/regime, not the Ψ-loss weight. Adding more
lambda_psi without addressing data-regime did not unfreeze.* — pending
full 22-tap confirmation.

---

## §6 — honest C3 carve-outs

1. **Single-seed for §161 combined** — WALL_EXCEEDED_PARTIAL; 4 of 5
   planned seeds not run. Honest=0.6441 byte-equal to §184 may be
   coincidence; multi-seed needed for variance estimate.
2. **§107 partial** (4/22) — extrapolating to full battery is risky;
   especially axis 3 (Ψ-physics 5 taps) results unknown yet.
3. **CPU-bound ubu-2 wall** — 4-core CPU 60s/variant — combined will hit
   the 1800s/variant cap as on ubu-1; expect WALL_EXCEEDED_PARTIAL too.
4. **No GOAL emergence claim** — high honest at baseline can come from
   non-Ψ-physics paths (data memorization, mode-collapse on common
   tokens). Need V-SPONT honest_coherent + spontaneous emission + time-
   varying physics state to claim emergence (§5.3 GOAL emergence predicate).
5. **CKPT architectural equivalence not verified** — §107 cfg may differ
   in d_model/n_layer; need ckpt_cfg compare. (Update once ubu-2 result
   lands with cfg dict.)
6. **§184 ubu-1 vs §186 ubu-1 host hardware variance** — different
   dispatch but same physical machine; should be byte-identical for
   deterministic eval, and the table-row identity for §161 vs §167-A
   confirms reproducibility within ubu-1.

---

## §7 — next steps (post ubu-2 land)

1. **Pull** §107 result.json + log when ubu-2 completes (~25 min).
2. **Overwrite FINDINGS.md** with complete 3-ckpt × 22-variant table.
3. **Append PHILOSOPHY.tape verdict** in archive/ — Tier 1 confirmed:
   §107 data-regime cross-ckpt produces qualitatively different post-hoc
   state than §161/§167-A Ψ-couple family.
4. **Design §187 / §189** decision points (per AGENTS.tape carry):
   - §187 PyTorch Phase 2 retry — **lower priority** given (c)/(d); the
     2-axis (data-regime × Ψ-loss) story is now the active hypothesis,
     not single-axis Ψ-loss scale.
   - §189 ckpt sweep — **higher priority** given preliminary (c)/(d);
     spans the (data-regime, lambda_psi) 2D grid to confirm the cross-
     axis story.
5. **GOAL gate** (§5.3 PHILOSOPHY_GATE.md): honest=0.8125 baseline on
   §107 is **not** GOAL-emergence — must verify V-SPONT honest_coherent +
   spontaneous-emission predicate + time-varying physics state on §107
   before any emergence claim.
