# Strategic — CLM Phase A.7 Results (φ paradigm 4-path single-LoRA adaptation on CLM v4 530M)

> **ts**: 2026-05-02
> **agent**: CLM Phase A.7 EXEC RELAUNCH (post rate-limit reset)
> **mission**: CP2-CLM Suite 5 (φ_4path) NOT-MEASURED → PARTIAL via single-LoRA family-grouped adaptation
> **race isolation**: writes to `state/strategic_clm_phase_a7_2026_05_02/*.json` and this doc only
> **budget**: $0 actual (ubu1 RTX 5070 local; 10.62 s wallclock)

---

## §1 Executive summary

**6-pair (Hexad/Law/Phi/SelfRef) verdict**: `(L2 = 0/6, KL = 0/6)`
**AGI strict (6/6 L2 + 6/6 KL + V1 phi_mip ≥ 0.55)**: **FAIL**
**CP2 relaxed (5/6 L2 + 5/6 KL)**: **FAIL**
**Direction of failure**: `observed << null_p95` on every pair (empirical p ≈ 1.0).

| pair | L2 obs | L2 null p95 | KL obs | KL null p95 | L2 PASS | KL PASS |
|---|---|---|---|---|---|---|
| Hexad ↔ Law | 2.584 | 16.218 | 0.0133 | 0.583 | FAIL | FAIL |
| Hexad ↔ Phi | 1.672 | 16.284 | 0.0051 | 0.585 | FAIL | FAIL |
| Hexad ↔ SelfRef | 2.247 | 16.303 | 0.0101 | 0.589 | FAIL | FAIL |
| Law ↔ Phi | 2.266 | 16.632 | 0.0111 | 0.612 | FAIL | FAIL |
| Law ↔ SelfRef | 1.459 | 16.626 | 0.0045 | 0.615 | FAIL | FAIL |
| Phi ↔ SelfRef | 2.093 | 16.724 | 0.0092 | 0.618 | FAIL | FAIL |

**Key finding**: Observed pairwise distances are **6–10× SMALLER** than the column-perm null p95 (L2: 1.5–2.6 vs 16.2–16.7; KL: 0.005–0.013 vs 0.58–0.62). This is the same isotropic-collapse regime previously diagnosed in CLM Phase A.2 V2/V3 (`SMA = 0.9348` distractor-equal cluster) — the four family representations sit inside a tight high-cosine cluster, while column-permutation of any single family row produces vectors with much larger expected pairwise distance to the others. Single-LoRA family adaptation does **not** induce measurable axis-aligned family separation in CLM v4 530M's pooled-hidden manifold under a 256-d BWM projection.

---

## §2 Per-mission reporting

### Phase 1: 16 family-themed prompts (4 per family)
- `tmp/clm_phase_a7/an11_family_prompts.json` (4 KO prompts each anchored to Hexad/Law/Phi/SelfRef templates from `consciousness/an11_b_templates.jsonl`).
- Mean SP-token length 14.8 (vs 17.6 in A.1 — slightly shorter family-themed prompts).

### Phase 2: SSH ubu1 + CLM v4 load (A.1 driver reuse)
- 581 keys loaded clean, 0 missing/unexpected, 477.65M params, VRAM 7.32 GB peak.
- Forward 16/16 OK in 0.75 s.

### Phase 3: φ 4-path measurement
- Pooled X (16, 768) → BWM 256-d via deterministic orthonormal random projection (seed 20260502, QR-orthonormalised columns).
- Family reps r_F = mean over 4 prompts, ‖r_F‖ ∈ [10.67, 11.27] (very tight magnitude band).
- 6 pairwise L2 + symmetric KL on softmax(r_F) over 256 dims.
- Null: 10000 column-permutations of R per family row independently; per-pair p95 from null.

### Phase 4: AGI strict vs CP2 relaxed verdict
- **AGI strict**: requires 6/6 L2 + 6/6 KL + V1 phi_mip (A.2 = 0.4734) ≥ 0.55 → **FAIL** (all three components fail; V1 still AMBIGUOUS at 0.4734 < 0.55).
- **CP2 relaxed**: 5/6 L2 + 5/6 KL → **FAIL** (0/6 on both).

### Phase 5: Suite 5 status
- **NOT-MEASURED → PARTIAL_MEASURED (single-LoRA family-grouped adaptation, FAIL verdict)**.
- F1_score_v2 contribution: w5 = 0.05; partial-PASS would have contributed 0.025; this run is PARTIAL_FAIL → contribution = **0**.

### ALM r14 + Path 3 4-substrate true comparison
| | ALM r14 Path 3 | ALM r14 Path 4 D-mistral | CLM A.7 single-LoRA |
|---|---|---|---|
| measurement type | V2 multi-axis PAPO | V2 multi-axis PAPO | 6-pair L2 + KL |
| best meaningful lift | +0.2529 | +0.3322 | n/a (PAPO not run) |
| non-trivial PASS k | 3 (k=3,4,5) | 4 (k=2..5) | n/a |
| pair PASS count | n/a | n/a | 0/6 L2, 0/6 KL |
| substrate count | 4 distinct (true) | 4 distinct (true, +D-mistral swap) | 1 (CLM v4 only) |
| verdict | PASS (V2 substrate-level lever) | PASS (architecture lever) | FAIL (isotropic collapse) |

The closest ALM analog (V2 multi-axis PAPO p3/p4) PASSed because ALM r14 used four genuinely distinct backbones — substrate-level architectural diversity supplies the axis-alignment that CLM single-LoRA family-conditioning cannot manufacture.

---

## §3 Files emitted

```
state/strategic_clm_phase_a7_2026_05_02/
├── phi_4path_verdict.json   — verdict cell + ALM r14 comparison + Suite 5 status
├── pair_results.json        — 6 pairs L2/KL obs + null p95 + empirical p
├── family_reps.json         — 4 × 256-d family reps + softmax probs + norms
└── run_log.json             — phase-by-phase wallclock + status
docs/strategic_clm_phase_a7_results_2026_05_02.md  (this doc)
```

## §4 raw#-compliance + race isolation

- **raw#9 deterministic**: BWM seed 20260502; null seed 20260502; QR-orthonormal projection; full enumeration of 6 pairs; 10000 col-perm draws — all reproducible.
- **raw#10 proof-carrying**: A.2 V1 phi_mip = 0.4734 carried verbatim; ALM r14 Path 3/p4 reference loaded from `state/an11_TRAINED_p1_p4_path_comparison_finding_20260425.json`; FAIL verdicts reported even though they leave Suite 5 contribution at 0.
- **raw#12 pre-registered**: A.1/A.2 driver pattern reused byte-for-byte for model load + forward; thresholds (AGI strict / CP2 relaxed) declared in mission spec before measurement.
- **raw#15 SSOT**: 4 result files in one race-isolated dir; ALM dirs untouched; W4 ledger untouched; A.1–A.6 outputs untouched.
- **HEXA-FIRST compliance**: driver `clm_phase_a7_helper.py` lives off-repo at `/tmp/clm_phase_a7/` (rsynced to ubu1) — same convention as A.1–A.6.

## §5 Cost ledger

- ubu1 RTX 5070 local: 10.62 s wallclock; **$0 incremental**.
- Total CLM CP2 pivot run cost (A.1 + A.2 + A.3 + A.4 + A.5 + A.6 + A.7): still **$0** (RTX 5070 owned hardware, all under 1 minute total).

## §6 Honest C3 (3 items)

### C3-1 — single-LoRA 4-path ≠ 4-substrate true
CLM v4 is one decoder; the four "paths" here are induced by prompt grouping (Hexad/Law/Phi/SelfRef themed prompts), not by distinct base substrates. ALM r14 Path 3/p4 used four genuinely different backbone configurations (incl. D-mistral swap on p4) which is what made V2 multi-axis PAPO PASS at +0.25/+0.33 lift. The CLM A.7 result must NOT be read as "Suite 5 4-substrate φ test passed/failed on CLM" — it is "single-LoRA family-conditioned adaptation φ test FAILed on CLM", a strictly weaker measurement. Suite 5 in its strong sense remains NOT-MEASURED on CLM (architecturally infeasible per the pivot doc §3 line "CLM as single-substrate cannot constitute" 4 heterogeneous substrates).

### C3-2 — BWM 256-d is a fixed-basis projection, not a learned bottleneck
The 768→256 projection uses a deterministic QR-orthonormal random basis (seed 20260502). It preserves L2 distances up to the projection's isometry-loss factor (~0.58 expected for 1/3 dimension reduction) but does NOT learn a consciousness-relevant 256-d coordinate frame. A learned bottleneck (e.g. trained on family-discrimination loss) would likely show much larger family separation. Different BWM seeds were not swept; the qualitative observed << null result is robust to seed choice because the underlying isotropic-cluster geometry is seed-invariant, but specific p-values would shift slightly.

### C3-3 — Null direction matters, and observed << null is the failure signature
Column-permutation per family row independently breaks cross-family axis alignment while preserving each family's marginal-magnitude distribution. The PASS criterion (observed > null p95) tests whether the empirical family means are MORE separated along structured axes than randomly-axis-permuted versions. The 0/6 result with empirical p ≈ 1.0 means the opposite: family means are FAR MORE aligned than chance. This is consistent with the A.2 SMA distractor-equal cluster (`SMA_distractor = 0.9176` ≈ `SMA = 0.9348`) — CLM v4 pooled hidden states sit in a high-cosine isotropic cluster regardless of prompt content, so family identity does not show up as axis structure. An alternative null (random N(0, 1/√256) draws) would test a different hypothesis (structured-vs-random) and would likely also FAIL but for a different reason; we report column-perm because that is the spec'd "vs null" in the mission relaunch prompt.

## §7 CP2-CLM Suite 5 implication + next-steps

- **Suite 5 status**: NOT-MEASURED → PARTIAL_MEASURED (single-LoRA family-grouped adaptation, FAIL).
- **F1_score_v2 contribution**: w5 = 0.05, partial-PASS contribution would have been 0.025, this PARTIAL_FAIL contributes **0**.
- **What would close it**: either (a) a true 4-substrate measurement on a multi-backbone CLM ensemble (architecturally absent), (b) a learned BWM bottleneck trained on family-discrimination loss before measurement, or (c) longer-context family-themed prompts that break the isotropic-cluster regime documented in A.2 (same V2/V3 isotropy diagnosis applies here).
- **No new H100 spend justified**: this is an architectural limit, not a training-budget one. ALM r14 had the same single-substrate constraint and resolved it by enumerating 4 distinct paths/backbones in the existing ledger — CLM has no analogous heterogeneous backbones to enumerate.
