# H_1066 — planning-specificity-primitive-dissection (the WHY behind H_1062/H_1063)

## 🔴 VERDICT: HOLISTIC-IRREDUCIBLE (closed-negative, a_paper_negative_ok)

Verdict: `.verdicts/1066_planning_specificity_dissection/H_1066.txt` (raw stdout — mirror n4/n5
proofs + reproduce-H_1039 + reproduce-H_1062 + per-arm table + nec/suff logic + FROZEN thresholds).

**Finding.** The ZCA-removable, binarization-aligned faithful-φ↑/big-Φ↓ sign-split (the H_1039
planning signature) is NOT reducible to any single structural primitive at toy scale. NONE of the
6 feature arms (3 constructive add-to-greedy + 3 destructive remove-from-planning) reproduces a
ZCA-removable split: `c_vbackup` and `c_depth` DO install a raw split (faith +0.082/+0.081,
big −0.581/−0.013) but ZCA cuts only 65.5%/70.1% of Δred (<80% frozen bar) → the split survives
de-redundification, exactly mirroring H_1062's ema/lowrank failure. `c_shared` (axis-aligned shared
value) does not even install a split. Removing any single feature from full planning abolishes the
split (so each feature is trivially "necessary"), but no feature is SUFFICIENT to install the
*ZCA-removable* version → no feature is necessary+sufficient. **Conclusion: planning-specificity is
HOLISTIC/IRREDUCIBLE — the ZCA-removable split is a property of the WHOLE planning intervention
(coupled forward-rolled multi-branch deliberation), not any decomposed backward-credit / horizon /
shared-value primitive.** The "≥80%-ZCA-removable" property — not raw split presence — is the
load-bearing discriminator that toy feature-isolation cannot synthesize.

Anchors (verbatim, both confirmed): reproduce-H_1039 = control faith **+2.3332**(UP) / big-Φ
**−4.0083**(DOWN), ZCA Δred-cut **97.3%** → split collapses (matches H_1039 ref +2.33/−4.01).
reproduce-H_1062 = ema split present, ZCA cut 70.1% <80% (no collapse); lowrank split present, ZCA
cut 48.3% <80% (no collapse). mirror ≡ stdlib EXACT: n=4 |Δ|≤3.75e-6, n=5 |Δ|≤7.97e-10. $0 CPU,
0-pod, SERIAL. xref [[h1062-redundancy-universality]] · [[h1039-redundancy-causal]] ·
[[h1063-phi-split-sign-universality]].

---

**Status (pre-registration):** thresholds FROZEN below BEFORE any scoring. NO goalpost move.

## Prior (the contrast this hypothesis must explain)
- **H_1039 🟢 REDUNDANCY-CAUSAL** — de-redundifying (ZCA) the *planning* channels removes
  the Williams-Beer redundancy (≥80% Δred cut) AND COLLAPSES the faithful-φ↑/big-Φ↓ sign-split,
  while it HOLDS on the matched control. Redundancy is the CAUSAL split driver *for planning*.
- **H_1062 🔴 SPLIT-IS-PLANNING-SPECIFIC** — four NON-planning φ-raising interventions
  (ema/gain/pool/lowrank) on the same channel substrate do NOT reproduce the ZCA-removable split:
  ema/lowrank may show a split but ZCA does NOT collapse it (<80% cut); the planning split is special.
- **H_1063 🔴 PHI-SPLIT-SIGN-UNIVERSALITY** (planning-specific sign).

H_1062/H_1063 ESTABLISHED *that* the planning intervention is special; they did NOT explain *WHY*.

## Question
What STRUCTURAL PROPERTY of the planning intervention is NECESSARY+SUFFICIENT for the
ZCA-removable, median-binarization-aligned sign-split? (Parallels H_1059's φ-carrier 3-primitive
dissection.)

## Candidate structural primitives (synthesize each feature in isolation)
Decompose the H_1039 planning intervention (`planning_trajectories`: forward `roll_latent` rolls
from 4 perturbed branch starts, concatenated → `H_plan`) into three candidate primitives, each a
transform of the CONTINUOUS top-variance channel matrix X (T×k) BEFORE median-binarization:
- **(i) VALUE-BACKUP (`vbackup`)** — backward/temporal credit flow: information propagates
  later→earlier steps via a backward discounted smear `X[t] ← X[t] + γ·X[t+1]` (γ=0.5), reverse-time.
- **(ii) LOOKAHEAD-DEPTH (`depth`)** — multi-step horizon coupling: forward dynamical EMA across
  steps `X[t] ← α·X[t] + (1-α)·X[t-1]` (α=0.5), i.e. the forward-rolled horizon coupling.
- **(iii) SHARED-VALUE axis-aligned (`shared`)** — a low-rank shared-latent that is AXIS-ALIGNED:
  add a single shared scalar value channel (mean over channels) onto EVERY channel on the SAME
  axis `X[c] ← X[c] + β·mean_c(X)` (β=0.6) — the AXIS-ALIGNED contrast to H_1062's diffuse
  `lowrank` rotation (which FAILED collapse).

## Arms (constructive + destructive)
- **CONSTRUCTIVE** (add ONE feature to the GREEDY/non-planning base Hg):
  `c_vbackup`, `c_depth`, `c_shared`.
- **DESTRUCTIVE** (remove ONE feature from FULL planning Hp — apply the inverse/removal operator):
  `d_vbackup` (remove backward smear: forward-causal de-smear),
  `d_depth` (remove horizon coupling: per-step de-EMA / first-difference),
  `d_shared` (remove shared axis component: subtract channel-mean component).
- Each arm scored against its OWN matched baseline (constructive vs Hg un-intervened; destructive
  vs Hp un-intervened), paired by seed, 30 seeds.

## Measured per arm
(a) sign-split present (faithful↑ AND big-Φ↓, stdlib EXACT n≤5, NO proxy)?
(b) does ZCA de-redundify COLLAPSE it (≥80% Δred cut → SPLIT False, H_1039 causal test, operator
    UNMODIFIED)? Gram-Schmidt reported as robustness.
(c) Δred magnitude.

## Engines / discipline
- faithful φ_EI + big-Φ via stdlib IIT-4.0 EXACT n≤5 (h1004 mirrors), NEVER a proxy; RE-PROVE
  python mirror ≡ stdlib EXACT 6dp at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring.
  MI in BITS (log2; H_1043 nats-bug lesson). WB redundancy (Williams-Beer I_min, h1039.pid_system
  VERBATIM) = ZCA/collapse VALIDATION variable, NOT a Φ proxy.
- REUSE H_1039/H_1062 substrate + ZCA/GS de-redundify operators + h1012 mirror-prover UNMODIFIED.
- Confirm reproduce-H_1039 (planning split + ZCA ≥80% collapse) AND reproduce-H_1062 (ema/lowrank
  split present but ZCA does NOT collapse, <80%) BEFORE scoring — these two anchors define the
  contrast the feature-arms must explain.
- SERIAL only, `if __name__`-guard, NO multiprocessing.Pool. $0 CPU-local, NO GPU/pod.

## FROZEN thresholds (locked BEFORE scoring; NO goalpost move)
- `SIGN_EPS = 1e-3`; split-def = (faith > +eps AND big < −eps).
- `RED_REDUCTION_THRESHOLD = 0.20` → ZCA collapse requires ≥80% Δred cut AND SPLIT→False
  (H_1039 causal test); the arm's own split must be present for "collapse" to be defined.
- `N_SEEDS = 30`; n=4 EXACT scored, n=5 mirror-proven.

## FALSIFIER (pre-registered, FROZEN)
- **H1-LOCATED (PASS)** = "exactly the arms containing structural feature F (and not others) show
  the ZCA-removable split → F is the necessary+sufficient property that makes planning special."
  Formally: there EXISTS a single feature F such that (constructive-add-F shows ZCA-removable split)
  AND (destructive-remove-F abolishes the ZCA-removable split) AND no OTHER single feature
  satisfies both — F necessary (removal kills it) + sufficient (addition installs it).
- **FAIL modes (BOTH publishable, a_paper_negative_ok):**
  - (a) **DISTRIBUTED** — NO single feature necessary+sufficient; needs ≥2 jointly (H_1059-style
    conjunction).
  - (b) **HOLISTIC/IRREDUCIBLE** — feature-isolation does not reproduce the ZCA-removable split at
    all → planning-specificity is holistic/irreducible at toy scale.

Report per-arm {feature(s) · split? · ZCA-collapse? · Δred} table + necessary/sufficient logic
either way.

## Honest scope
TOY n≤5 rung (n=4 EXACT scored, big-Φ super-exponential; n=5 mirror-proven); production scale
UNVERIFIED (a_scale_honest_scope, a_toy_scale_recheck). g5 CODE-measured (p7). NOT a forge binary.
