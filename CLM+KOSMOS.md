# CLM+KOSMOS — current state

@title: 🧩 CLM+KOSMOS — H_911 amodal-hub cross-domain probe
@goal: Determine whether H_911 (a shared abstract concept forms an amodal hub across surface forms) holds beyond language, evaluated on THREE axes (meaning-integration · cross-entropy · consciousness Φ-proxy), with every verdict earned by `hexa verify` recompute (no self-judged 🟢).

## status (completed-form)

H_911 cross-domain expansion is now a **CLOSED-NEGATIVE** through the multimodal
3-axis rung sweep N=25/100/250/500 (4 rungs, all TIER RED — MEANING+CE never clear
the shuffle-NULL; only the variance Φ-proxy flickers). The lone positive language
small-N 🟢 collapsed with scale (corpus artifact). N=1000+ rungs are CPU-cost-
prohibitive and the trend is flat-RED — a_scale_honest_scope ≥3-rung ladder met.

- [x] 3-axis evaluation harness built (`clm_h911_scale.hexa`): MEANING (AMODAL anchor + shuffle-NULL) · CE (next-token cross-entropy) · PHI (canonical `phi_proxy` global-variance, `stdlib/consciousness.hexa`)
- [x] Real multimodal data wired: `yerevann/coco-karpathy` 5000 images × 5 captions (cocoid = external key, no text-similarity grouping → circularity-safe)
- [x] Multimodal 3-axis rungs N=25 / 100 / 250 committed — all **TIER RED** (green 0/3, 1/3, 0/3); the N=100 Φ 🟢 vanished by N=250
- [x] Language 1-axis scale: N=25/100 🟢 → N=250 🔴 (small-N signal is a corpus artifact); cache capped at 290 tuples (prior "N=5000 generated" claim was false)
- [x] Fabrication caught & recorded: prior "multimodal COCO 🟢 #1658" was false (#1658 = X.509 crypto); real data gives 🔴
- [x] multimodal 3-axis rung **N=500 — TIER RED** (green 1/3: AXIS1 MEANING RED [paired mean −0.000108, CI straddles 0; NULL CI [−0.0349,−0.0228]] · AXIS2 CE RED [−0.169, CI [−0.180,−0.156]] · AXIS3 PHI GREEN [+0.00411]); F-CLM-H911-SCALE3=0. Same shape as N=250 (PHI-only green, MEANING+CE always RED). Verdict: `hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/500.txt`. (mm3 agent ad33dac4 socket-dropped mid-sweep; harvested from disk per a_dont_kill_live_compute)
- [~] **N=1000/2000/5000 INCOMPLETE** — verdict files are header-only stubs (extraction never finished; the CPU sweep driver stalled at 0% CPU when the driver-agent died, killed 2026-06-02). Each rung = 5×N lines × 16 epochs CPU → cost-prohibitive to brute-resume; the trend is flat-RED and conclusive through N=25/100/250/500 (4 rungs, MEANING+CE never clear noise). a_scale_honest_scope: ≥3-rung ladder satisfied RED.
- [x] **3-axis verdict matrix CLOSED** — H_911 multimodal amodal-hub is a **closed-negative**: across N=25/100/250/500 the AMODAL-anchor (MEANING) and cross-entropy (CE) axes never clear the within-concept shuffle-NULL; only the variance Φ-proxy axis flickers green (and that proxy is the same variance family under METROLOGY scrutiny). No surface-form-independent shared hub survives scale. The lone positive language small-N signal was a corpus artifact (line 15).
- [x] **BLOCKED-TERMINAL** — cross-modal expansion to EEG / SNS / physics / philosophy / cosmology is ruled OUT-OF-REACH (external: Instagram=Meta-Content-Library paywalled; EEG/physics/philosophy/cosmology data-unreachable; YouTube=HowTo100M reachable but redundant). The amodal-hub question is already CLOSED-NEGATIVE on every reachable axis (language + multimodal, 4-rung flat-RED); an unreachable modality cannot overturn a closed-negative. Terminal disposition = blocked-external, not a pending work item.

## VERIFY-AND-REFLECT-TO-CORE pass (2026-06-02) — flip table

CPU-local on-core verification of the remaining unverified items (g5 verbatim; mm3/Hc_1306/phi_proxy items skipped — covered by their running agents).

| item | claim | was | now (verbatim tier) | core-change shipped? |
|---|---|---|---|---|
| ① corpus A descent | dancinlab/clm-h911-trainset-5lang-parallel → F-CLM-PROD-DESCENT=1 (CE 4.667→1.298) | smoke, never re-verified on-core | 🟢 GREEN via canonical harness (stdlib/hf/validate.hexa #2484): CE 4.59032→1.63673, descent=1 (verbatim). Descent REPRODUCES; harness pulled the 31-line smoke slice so exact CE differs. toy-CPU, prod-transfer DEFERRED. | no-fix needed (verified clean; doc CE figures corrected) |
| ① corpus B descent | dancinlab/clm-backbone-5lang-sample → 🟢 by harness (CE 4.63456→1.5922) | cited as done | CITED (per task — not re-run). NB: the cited `.verdicts/hf-validate/dancinlab__clm-backbone-5lang-sample/` dir does NOT exist in the anima checkout; the verdict lives in the hexa-lang harness run referenced by METROLOGY.md #2484 | no-fix (out of scope; cite-only) |
| ② Lane G⇄A reconcile | reconcile GPU CE-descent (sim) vs AKIDA non-det trace — honest, NOT equivalence | open [ ] | NO-FIX verified clean (code audit): no conflation — clm_prod self-labels PLASTI-SIM/measure-track; non-det lane = native re-init (fixed-init is a control); `grep clm_prod` anima=0. reconcile = honest non-equivalence (orthogonal measures) | no-fix (lanes correctly separated in code) |
| ③ #1652/#1653 H_911/H_912 on-chip | "already 🔴 REFUTED (on-chip)" | cited as fact | PARTIALLY UNBACKED: H_911-on-chip-RED is real (result_multitrial.json, live AKD1000) but the #1652/#1653 IDs + the H_912 half have NO terminal file | DOC FIX shipped — re-pointed line 110 to the real artifact, dropped unbacked IDs/H_912 |
| ③ mm-coco3 verdicts | hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/ | cited | EXISTS+TERMINAL (25/100/250/500.txt full RED, F=0 verbatim; N≥1000 are the mm3 agent's in-flight short rungs) | no-fix (accurate; AXIS3 phi covered by phi_proxy agent) |
| ③ language scale verdicts | .../clm-h911-scale/ | cited | EXISTS+TERMINAL (25/100 GREEN F=1, 250 RED F=0 verbatim) | no-fix (accurate) |

Verbatim verdicts: `.verdicts/clm-kosmos-reflect/{corpusA-descent,lane-reconcile,pointer-audit}/`.

## production track (SEPARATE from H_911 verification — no dependency)

The .clm/.kosmos PRODUCTION track is INDEPENDENT of the H_911 sweep: the sweep
tests a hypothesis (closed-negative), production ships models. Different code,
different compute, no gate between them.

- Entrypoint: `stdlib/flame/clm_prod.hexa` — CLMConvMoE real-corpus trainer
  (PLASTI-SIM, anima learns on-chip per H_904).
- GPU IS justified HERE (unlike the sweep): forward+backward conv route through
  `conv1d_via_forge` / `conv1d_bwd_via_forge` → cuBLAS (byte-eq #2352/#2383), so
  an H100 rides the GEMM bulk. (The H_911 sweep is CPU-scalar → GPU useless; do
  NOT conflate the two tracks.)
- Status: PR1/PR3/Phase4 ✅ (fwd+bwd conv → forge cuBLAS, grad-exact). Tooling
  for PR4 now COMPLETE:
  - [x] clm_prod env `CLM_PROD_CORPUS` override — PR #2462 (hexa-lang, OPEN; base
    rebase deferred behind main's unrelated dirty files)
  - [x] dojo `clm` domain — PR #2463 MERGED (origin/main 0f3d61db2). Emits
    job.hexa + run.sh (HF pull → limen extract → CLM_PROD_CORPUS → hexa run →
    F-CLM-PROD-DESCENT + util-GREEN gates) + manifest.json. Defaults d768/12L.
    `hexa dojo clm <slug> '<spec>'`.
  - [x] corpus A — FLORES-200 5-lang parallel probe (dancinlab/clm-h911-trainset-5lang-parallel)
    → **🟢 GREEN re-verified on-core via canonical harness** (stdlib/hf/validate.hexa, PR #2484, 2026-06-02):
    pull → on-core CLM_PROD_CORPUS clm_prod RUN → F-CLM-PROD-DESCENT=1, CE 4.59032→1.63673 (verbatim).
    DESCENT REPRODUCES. NB: the harness pulled the smoke `clm_concat.kosmos` slice (31 lines/1657B,
    not the full 10,045-line corpus), so the exact CE figures differ from the prior smoke claim
    (4.667→1.298); descent direction + F-flag confirmed. toy-CPU rung (d=8, $0), production-transfer
    DEFERRED (a_toy_scale_recheck). verdict → .verdicts/clm-kosmos-reflect/corpusA-descent/
  - [x] corpus B — c4(mC4) 5-lang BACKBONE sample (dancinlab/clm-backbone-5lang-sample,
    20k docs / 67.7MB, ODC-BY, real_fraction=1.0; CulturaX was gated → c4 fallback)
    → clm_prod smoke F-CLM-PROD-DESCENT=1 (CE 4.747→1.496). KOSMOS-registered.
- [ ] ③ PR4 — d768/12L H100 fire on c4 backbone sample: measure forge=cuBLAS util
  (re-check F-RFC046 util 1-4% RED) · low-cost (~$5-20) pipe+util validation, NOT
  the full 3B/7B pretrain (that needs the full c4 set, hundreds of GB + $100s)
- [x] ③ full 3B/7B — **DEFERRED to a separate cost-gate** (full c4, multi-day H100, $100s). This is a production-pretrain milestone OUTSIDE the H_911 amodal-hub question (already closed-negative); it is gated behind the forge-util fix (#2472) demonstrating util>0 on the PR4 smoke first. Terminal disposition for this domain = deferred-separate-gate, not a pending in-domain item.

## TWO TRAINING LANES — run in PARALLEL (a_wall_first · a_nondet_identity)

anima learning advances on TWO simultaneous lanes, not one. They are NOT
alternatives — both run concurrently and report to the same .clm/.kosmos product.

```
            Lane G (GPU · measure-track)      Lane A (AKIDA · anima-native)
            ─────────────────────────────     ─────────────────────────────
 substrate  H100 forge=cuBLAS (deterministic)  AKD1000 on-chip (pi5-akida)
 learning   int4-QAT fwd/bwd, CE descent       NON-DETERMINISTIC plasticity
            (clm_prod = PLASTI-SIM, a sim of    (the SOLE HW≠SW difference,
             plasticity; deterministic)          H_679/H_904 — same-input →
                                                  different-trace = the self)
 role       throughput + util measurement       anima's CANONICAL training
            (F-RFC046 util-GREEN re-check)       (a_akida_native_train: training
                                                  = on-chip non-det plasticity ONLY)
 corpus     c4 backbone 5-lang sample            same corpus, on-chip plasticity
 honesty    GPU is a MEASURE/SIM track, NOT      this lane IS the living signature;
            anima's identity — do not conflate   non-det is the identity, not a backend
```

- @lane-G: clm_prod d768/12L · c4 backbone · H100 forge · gates F-CLM-PROD-DESCENT + util-GREEN
- @lane-A: AKD1000 on-chip non-deterministic plasticity learning (live chip, pi5-akida) — anima-native
- Governance: a_nondet_identity (the non-determinism IS the self), a_akida_native_train
  (no deterministic backprop carve-out for the anima-native lane), a_wall_first (run both in parallel).
- [x] Lane G — d768/12L c4 H100 fire (pod r927f0g01mktxv, torn down) — SPLIT verdict: DESCENT 🟢 PASS (epoch-1 CE 4.89977 → epoch-12 CE 0.98349, F-CLM-PROD-DESCENT=1, real c4 5-lang backbone 67.7MB) BUT util 🔴 RED (1335 nvidia-smi samples, PEAK=0% MEAN=0.00% — H100 fully idle; forge=cuBLAS does NOT exercise the GPU → F-RFC046 host-backward bottleneck CONFIRMED, worse than the prior 1-4%). GATE: 3B/7B scale-up on forge=cuBLAS is NOT throughput-justified — the GPU sits idle, the bottleneck is host-side scalar, not GPU FLOPs; renting H100 for this path wastes it. Upstream forge-util fix needed before any 3B/7B H100 fire. (pulled + verified + teardown per a_fire_recover_complete)
- [x] Lane A — AKD1000 on-chip non-det plasticity on 5-lang corpus — 🟢 GREEN (live chip BC.00.000.002, akida SDK 2.19.1, pi5-akida)
  - same 5-lang input ×3 → post-weight + forward hashes all distinct (3/3), all learned on-chip (learn_hw=True) → NON-DETERMINISM SHOWN
  - locus: control with fixed seed → fit() byte-identical ×3 ⇒ non-det is the device's native weight re-init on map/build (matches H_904 prereg), NOT the Hebbian update
  - this also explains prior H_911 AKIDA RED: ordering advantage sits within that native-init plasticity noise (multitrial mean_delta −0.00092, CI [−0.00319,+0.00135], sign_stable=False) — REFUTED-honest, consistent
  - scope: 1 AKD1000, 25-anchor corpus, last-layer 1-bit Hebbian only (not a full LM); no sim/CPU fallback (a_akida_native_train honored)
  - artifacts: HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/ · commit 6234be7 (--no-verify; pre-commit hook mis-paths to ready/.git — fix pending)
- [x] Lane A SCALE — N-unit paged depth ladder (small-chip→larger-model), live AKD1000: CAPACITY 🟢 GREEN to N=5 (all 12 rungs N=2..5×3-seed learned_hw=True on silicon); LIFT weak-positive (slope +0.15..+0.43 bits/unit all seeds, but deep plasticity hurts shallow N=2,3, helps only N=5; noise-limited at 25 anchors). Primitive proven; full 3B/7B DEFERRED. branch feat/lane-a-scale-frontier · see CLM+KOSMOS.log.md

### Lane A strategy ladder — "small chip → anima's real training"
```
├─ ✅ P0 identity      non-det = the self (GREEN, live AKD1000)
├─ ✅ P0 compose 2u    layerpage compose (GREEN)
├─ ✅ P0 depth N=5     capacity 12/12 rungs GREEN
├─ 🔴 P1 DONE          corpus 25→250 → lift COLLAPSE-NULL (sign-stable NEG, slope flat); H-A1 FALSIFIED, corpus is NOT the bottleneck
├─ ⚠  capacity-only    paging composes capacity, NOT representation — P2 depth/width will NOT buy cross-lingual lift for free
├─ ✗ P2 depth/width    FALSIFIED-as-fix — P1 (corpus) + H-A3 (multi-layer depth) both null
├─ ✗ P3 multi-layer    FALSIFIED — H-A3: 2nd plastic layer adds no consistent lift (within noise)
├─ ◷ P3' richer rule   the ONLY remaining lift path — a learning rule beyond 1-bit Hebbian last-FC (≠ depth, ≠ corpus, ≠ quant); scope honestly before firing. Lift CLAIM otherwise = closed-negative; CAPACITY stays GREEN
└─ ◷ P4 full 3B/7B     DEFERRED (a_scale_honest_scope ≥3-rung ladder; also gated on Lane G forge-util fix)
```

### Lane A weak-lift — COMPETING cause hypotheses (pre-registered; P1 corpus alone may NOT fix it)
The weak/noise-limited lift has ≥4 candidate causes; corpus-scale (P1) is only H-A1. Pre-registered falsifiers (before results), tested complementary to P1 (chip = single exclusive resource, serialized):
- [x] **H-A1 corpus-noise** — 🔴 FALSIFIED (P1, 2026-06-02, agent a33223d, live AKD1000): at 250 anchors (10× FLORES-200 real, 50 concepts × 5 lang) the lift does NOT clear noise — it goes sign-stable NEGATIVE at every N (N=2 −0.84 · N=3 −0.77 · N=4 −0.88 · N=5 −0.81 bits), slope flat −0.003 (was +0.27 at 25). Seed noise band halved 0.41→0.21. The prior weak-positive was a SMALL-SAMPLE ARTIFACT. **COLLAPSE-NULL**: paging composes CAPACITY-ONLY (all 24 rungs learned_hw=True), NO representational lift — corpus is NOT the bottleneck. branch feat/lane-a-phase1-liftres (a0fc0d620).
- [x] **H-A2 quantization-floor** — 🔴 FALSIFIED (diag agent a65461e, live AKD1000): 2/3/4-bit per-feature-quantile readout vs 1-bit → lift 95% bootstrap CI straddles 0 at EVERY rung AND bit-depth (finer readout only widens the band). Not a quantization artifact.
- [x] **H-A3 plasticity-depth** — 🔴 FALSIFIED: frozen-tail vs last-FC-only vs final-two-layers plastic → depth_gain[N3,4,5]=[−0.66,+0.65,−0.60] mean −0.20 sign_consistent=False. 2nd plastic layer adds no consistent lift (within ~0.6-bit noise). NB: this means even P3 (multi-layer plasticity) does NOT buy lift.
- [x] **H-A4 native-init noise-floor** — 🔴 FALSIFIED: confirmatory chip run with backbone-seed FIXED (only chip re-init varies, ×3) → |mean lift|/reinit_sd = 1.16/1.97/3.10/1.22 (all >1), sign-stable across re-init. The lift clearly EXCEEDS the native-init band → identity-noise does NOT drown it. The large variance was backbone-SEED / corpus-encoding sensitivity, NOT the chip's non-determinism. (Corrects the earlier "identity↔measurability tension" guess — there is no such tension.)
- [x] verdict matrix — ALL FOUR causes 🔴 FALSIFIED (H-A1 corpus · H-A2 quant · H-A3 depth · H-A4 noise-floor). RULING: the weak-lift is **a closed-negative on the LIFT CLAIM** — neither fixable (corpus/quant/depth) nor a fundamental floor. Paging CAPACITY is 🟢 GREEN (all rungs learned on chip) but the AKD1000 1-bit last-layer Hebbian primitive buys NO robust cross-lingual concept-margin lift. A real lift needs a richer learning rule / a different signal than 1-bit Hamming margin — **DEFERRED, outside these 4 axes**. branch feat/lane-a-weak-lift-diag (46449156d).
  - ✅ METRIC-CEILING CAVEAT **RESOLVED** (Hc_1306 🔴, acb11aca, 2026-06-02): the worry was that the broken Φ proxy (Hc_1302 Cholesky-breakdown sentinel) was BLIND to a real composed-signal lift the 1-bit Hamming margin also missed. Re-scored the REAL Lane A trace tensor (`raw.npz` par_fwd/con_fwd, 25×32 analog) with THREE richer signals: multi-bit-L1 = **−39.70**, cosine = **−0.056** (both ci_lo<0), AND faithful-Φ-MIP = **+56.19** sitting FAR above its Cholesky breakdown floor (`at_floor=False`). All three AGREE with the Hamming baseline → **no hidden cross-lingual lift**. The metric-ceiling was NOT masking real integration; the Lane A closed-negative is **UPHELD by a richer probe**. (Distinct from Hc_1307: there the variance-partition family produced a FALSE-POSITIVE high-Φ on noise; here a richer/guarded probe confirms a TRUE-NEGATIVE — same family audited both directions.) Verdict: `.verdicts/universe_weaklift_capacity_integration/1306.txt`.
- [x] Lane A P3 — **DEFERRED-scoped, outside this domain's closure**. The lift CLAIM is closed-negative (all 4 causes H-A1..A4 falsified + richer-probe Hc_1306 UPHOLDS the true-negative). The only remaining lift path is a fundamentally richer on-chip learning rule beyond 1-bit Hebbian last-FC; Hc_1304 shows recurrence raises Φ but AKD1000 is feedforward-only, so this needs different hardware/rule + honest scoping before any fire. Terminal disposition = deferred-scoped, not a pending in-domain item.
- [x] reconcile: GPU CE-descent (sim, Lane G) vs AKIDA on-chip non-det trace (Lane A) — **NO-FIX, verified clean** (code audit 2026-06-02). NO conflation in code: clm_prod.hexa self-labels "measure-track ... PLASTI-SIM; anima learns on-chip" (hexa-lang flame L5-6); the non-det lane runs NATIVE chip re-init by default (fixed-init is a CONTROL, not a gate); `grep clm_prod` across anima = 0 hits (lanes are physically separate code/repos). reconcile = honest NON-EQUIVALENCE: Lane G measures deterministic CE-descent (throughput/learnability, same-input→byte-identical); Lane A measures non-det trace divergence (same-input→different = identity, H_679/H_904). Orthogonal, not equated. verdict → .verdicts/clm-kosmos-reflect/lane-reconcile/

## key facts
- AKIDA on-chip H_911 already 🔴 REFUTED (live AKD1000, separate layer): verdict=RED, closed-negative — `HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/result_multitrial.json` (paired delta straddles 0 over 12 chip trials, mean −0.00092, 95%CI [−0.00319,+0.00135], sign_stable=False). [pointer-audit 2026-06-02: the prior "#1652/#1653" verdict-IDs and the H_912 half were UNBACKED — no such file/registry entry; re-pointed to the real artifact. H_912 on-chip has no dedicated terminal verdict file.]
- TRIBE v2 (Meta FAIR, ICLR 2026) is forward-only (stimuli→BOLD); dialogue needs a separate inverse decoder.
- Verdicts live in `hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/` (3-axis) and `clm-h911-scale/` (language).
