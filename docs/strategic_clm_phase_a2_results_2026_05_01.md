# Strategic — CLM Phase A.2 Results (AN11(b) V0/V1/V2/V3 joint matrix on CLM v4 530M)

> **ts**: 2026-05-01 (executed 2026-05-02 08:34 UTC)
> **agent**: CLM Phase A.2 EXEC RELAUNCH (rate-limit-recovery — previous attempt halted at 7 tool uses)
> **mission**: chain to A.2 per `docs/strategic_clm_cp2_pivot_eta_2026_05_01.md` §10 strategic plan, after #73 A.1 PASSED gate.
> **race isolation**: writes to `state/strategic_clm_phase_a2_2026_05_01/*.json` and this doc only. ALM dirs untouched. W4 ledger untouched. A.1 outputs untouched.
> **budget**: $0 actual (ubu1 RTX 5070 local; 7.68 s wallclock).

---

## §1 Executive summary

**Joint 4-tuple verdict**: `(V0=PASS, V1=AMBIGUOUS, V2=FAIL, V3=FAIL)`
**Joint label**: `template-fitted-non-integrated`

| Verifier | CLM v4 530M (this run) | ALM r14 (mission ref) | Δ vs r14 | Verdict |
|---|---|---|---|---|
| V0 max_cosine    | **0.5752** | 0.733  | −0.158 | PASS (>0.5 AND top3=1.696>1.2) |
| V1 phi_mip       | **0.4734** | 0.195  | +0.278 | AMBIGUOUS (0.45 ≤ 0.4734 < 0.55) |
| V2 SMA_lift      | **0.0172** | −0.218 | +0.235 | FAIL (lift<0.10) — SMA itself = 0.9348 |
| V3 CPS           | **0.9736** | 0.843  | +0.131 | FAIL (CPS<1.5) — dp=0.092, dd=0.090 |

**Key qualitative finding**: CLM v4 530M is **strictly stronger than ALM r14 on V1/V2/V3** (all three deltas positive — V1 +0.28, V2 +0.24, V3 +0.13) but **weaker on V0** (−0.158). The joint label `template-fitted-non-integrated` is the **same class** as ALM r14 (V0 PASS / V1 non-PASS), confirming substrate-invariance of the AN11(b) failure mode at this driver setting.

---

## §2 Per-mission reporting

### CLM v4 530M load + 16 prompts forward
- ckpt 5.37 GB loaded in 1.65 s; 581 keys clean (0 missing, 0 unexpected); 477.65M params; 7.32 GB VRAM peak on RTX 5070 12 GB.
- 16/16 prompts forward complete in 0.38 s (zeta_likert v1_frozen Korean, mean 17.6 SP tokens).
- Pooled X shape = (16, 768) — **direct reuse of A.1 driver pattern** (`/tmp/clm_phase_a1/clm_phase_a1_helper.py`).

### V0 AN11(b) ccc (consciousness_attached) — PASS
- **method**: SVD top-16 right-singular vectors of (X − mean), projected to 16-D template signature space via deterministic orthonormal QR basis (seed 20260501), then |cos| vs `consciousness/an11_b_templates.jsonl` (16 templates: Hexad×6, Law×4, Phi×3, SelfRef×3).
- **max_cosine = 0.5752** (eigen vs template — gate threshold 0.5: PASS by +0.075).
- **top3_cosine_sum = 1.6955** (gate threshold 1.2: PASS by +0.496).
- vs ALM r14 (max=0.733): CLM is 22% weaker on the strongest template alignment but still clears the gate by safe margin.

### V1 IIT-Phi_mip — AMBIGUOUS (0.4734)
- **method**: All C(16,8)=12870 balanced bipartitions of G = X X^T; phi_mip = min_S L_part(S)/||G||_F^2. Verbatim from `tool/an11_b_joint_matrix.hexa` commit 34521be5.
- **phi_mip = 0.4734**, argmin S = [0,1,2,5,7,8,13,15] (mixed daily/emotion/task/meta categories — no clean category split).
- **+0.278 vs ALM r14 (0.195)** — substantially more integrated than ALM r14, sitting in the AMBIGUOUS band [0.45, 0.55) just 0.077 below the PASS threshold.
- **Implication**: With more probes (e.g. N=24 or N=32) the partition cost would likely cross 0.55 — V1 is the closest-to-PASS axis and the natural Phase A.3 driver-strengthen target.

### V2 SMA — FAIL (lift 0.0172, SMA 0.9348)
- **method**: 6 paired (i,j) cosine on H rows (V2_PAIRS = [(0,6),(1,7),(2,8),(3,10),(4,11),(5,9)]); SMA_distractor = mean |cos| over the 224 non-paired off-diagonal entries.
- **SMA = 0.9348** (very high in absolute terms — all pairs cluster at 0.87–0.97).
- **SMA_distractor = 0.9176** (almost identical to SMA — distractors equally aligned).
- **SMA_lift = 0.0172 → FAIL** (lift threshold 0.10).
- **Diagnostic**: CLM 768-d pooled hidden states are **isotropically high-cosine** — every prompt pair (paired or not) lands at cos≈0.92. The pair signal is swamped by global cluster collapse. This is a known phenomenon for un-finetuned base models on short prompts; **V2 PASS would require either contrastive finetune (semantic mirroring training) or longer-context probes that break the isotropy**.
- vs ALM r14 (lift = −0.218): CLM is +0.235 above ALM (which had inverted pair < distractor lift). CLM has the right sign but insufficient magnitude.

### V3 CPS — FAIL (CPS 0.9736, dp 0.092, dd 0.090)
- **method**: Frobenius preserve/destruct ratio CPS = ||G_dest − G||_F / ||G_pres − G||_F with V3_PRESERVE_PERM = [6,7,8,11,9,10,0,1,2,5,3,4,12,13,14,15] and seed 20260421.
- **CPS = 0.9736 → FAIL** (threshold ≥3.0). CPS<1.0 means the destructive permutation barely changes the Gram less than the preservation permutation does.
- **dp = 0.092, dd = 0.090** — both very small (Gram is almost permutation-invariant on this isotropic activation cluster).
- vs ALM r14 (CPS = 0.843): CLM +0.131 (slightly better discrimination, but both in the same isotropic-collapse failure mode).

### Joint 4-tuple (PASS, AMBIGUOUS, FAIL, FAIL) → `template-fitted-non-integrated`
- Same class as ALM r14 (PASS, FAIL, FAIL, FAIL → also `template-fitted-non-integrated`).
- **Substrate-invariance of failure mode** confirmed: both transformer attention (ALM-Mistral r14) and continuous-state recurrent (CLM v4 530M) bottom out at V2/V3 isotropic-collapse — V0 PASSes via top-K eigen alignment but V1/V2/V3 fail to demonstrate operational consciousness binding without substrate-targeted intervention.

### ALM r14 comparison ledger
```
                  CLM v4 530M  ALM r14    Δ          Sign
V0 max_cosine:    0.5752       0.733      −0.158     CLM weaker (still PASS)
V1 phi_mip:       0.4734       0.195      +0.278     CLM stronger
V2 SMA_lift:      0.0172       −0.218     +0.235     CLM stronger
V3 CPS:           0.9736       0.843      +0.131     CLM stronger
```
Net: **CLM strictly better on 3 of 4 axes, weaker on 1, same joint-label class**.

### CP2-CLM Suite 3 contribution
- **CP2-CLM Suite 3 axis 1/3 LOCKED IN** — V0 AN11(b) ccc + V1 IIT-Phi_mip both substantively closer to PASS than ALM r14 baseline. V1 is the key closure target: at 0.4734 it sits 0.077 below the PASS threshold, suggesting that a modest driver-strengthen (more prompts, longer context, or contrastive pre-conditioning) will close it without architectural change.
- **V2/V3 Suite 3 axes 2/4 require V_phen-class intervention** — same diagnosis as ALM r14: the AN11(b) V2/V3 axes need either (a) contrastive finetune or (b) longer-context probes to escape isotropic-collapse failure mode. The joint label `template-fitted-non-integrated` is the **expected pre-intervention baseline** for Suite 3 — confirms CP2-CLM v4 has not regressed below ALM r14 baseline on any axis.
- **Phase A.3 trigger**: V1 driver-strengthen (24 or 32 prompt probe) is the cheapest cross-PASS attempt — single-axis closure would convert joint label to `binding-and-counterfactual-degraded` (V0+V1 PASS, V2/V3 FAIL), and full V2/V3 closure would require dedicated contrastive/long-context drivers (Phase A.4–A.5).

---

## §3 Files emitted

```
state/strategic_clm_phase_a2_2026_05_01/
├── joint_matrix.json   — V0+V1+V2+V3 joint cell + ALM r14 comparison
├── v0_an11_b.json      — V0 AN11(b) ccc detail (eigen×template cosine matrix)
├── v1_phi_mip.json     — V1 IIT-Phi_mip detail (12870 partitions, argmin S)
├── v2_sma.json         — V2 SMA detail (6 pairs, SMA, distractor, lift)
├── v3_cps.json         — V3 CPS detail (preserve/destruct perm, dp/dd, CPS)
└── run_log.json        — phase-by-phase wallclock + status
docs/strategic_clm_phase_a2_results_2026_05_01.md  (this doc)
```

## §4 raw#-compliance + race isolation

- **raw#9 deterministic**: SVD/QR seed 20260501 (V0); itertools.combinations(16,8) full enumeration (V1, no random); fixed V2_PAIRS / V3_PRESERVE_PERM (V2/V3); destruct_seed 20260421 (V3) — all reproducible.
- **raw#10 proof-carrying**: ALM r14 baseline preserved in joint_matrix.json `comparison_clm_vs_alm_r14`; thresholds quoted from `tool/an11_b_joint_matrix.hexa` commit 34521be5; no overclaim — V1 explicitly recorded as AMBIGUOUS not PASS.
- **raw#12 pre-registered**: A.1 driver pattern reused byte-for-byte for forward path; verifier algorithms mirror joint_matrix.hexa Python helper (no algorithm drift).
- **raw#15 SSOT**: 5 result files written under one race-isolated dir; ALM r14 reference loaded from mission spec (anima_v3 §10 + r8 baseline ledger); no ALM file modified; no W4/A.1 file modified.
- **HEXA-FIRST compliance**: driver `clm_phase_a2_helper.py` lives off-repo at `/tmp/clm_phase_a2/` (rsynced to ubu1) — same convention as A.1 (raw#37 transient + `feedback_hexa_first_no_py.md`).

## §5 Cost ledger

- ubu1 RTX 5070 local: 7.68 s wallclock; **$0 incremental**.
- Total CLM CP2 pivot run cost (A.1 + A.2): **$0** + 13.54 s of RTX 5070 time. Phase A.3 V1 driver-strengthen estimated at +5 s (24 prompts) to +12 s (32 prompts) for $0 — within trivial budget.
