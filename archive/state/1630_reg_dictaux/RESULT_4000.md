# H_1812 4000-step MULTISEED CLOSURE TEST — RESULT (n6n7 N6+N7 trunk-objective lever)

> Decisive test of the 2000-step DIRECTIONAL-positive (G1 best_distinct 0→1). Hypothesis:
> 4000-step + multiseed amplifies G1 0→1→2+ for CLOSURE (G1≥2), else NOT-SUPPORTED confirmed.
> Engine-native verdict path = `cli/evaluate.py` → `core/g_gates.py` (torch-free numpy decode
> ← `core/clm_decode.py`) = TERMINAL-eligible (公인 py 2-production, a_engine_native_learning).
> py-eval DIRECTIONAL per 2026-06-28 py-retire policy → hexa-native `anima evaluate` confirm = follow-on.

## 설정 (frozen · PREREG)
- arch = CLMConvMoE **L4 · d3784 · E2→E3** (mitosis mid-split @ step 2000) + savant golden-zone cusp anneal
  = `cli/train.py --canon` equivalent via `state/1630_reg_dictaux/trainer.py`. 345.665M params, `.clm` 176584498 B.
- corpus = clean 언어검증 4칸 register (`state/clm303_clean_corpus/{gen,sns}_{ko,en}.txt`, proportional, val_frac=0.05).
- **steps = 4000** (PREREG spec for N6 grok floor-exclusion — completed this run, vs 2000 prior).
- seeds = **{4307, 4308, 4309}** multiseed (PREREG; vs single-seed 4307 prior).
- 하드웨어 = vast A40 (CUDA 12.4, torch 2.5.1+cu124), pod 43047674. arm = n6n7 (N6 grok-band + N7 dict-aux λ0.05).

## 1. 학습-side held-out DESCENT (verify_clm_v2 math.log mirror · overfit gate)
**ALL 3 seeds × 4 registers = 12/12 held-out DESCENT PASS (overfit_warning=False everywhere):**

| seed | pooled val_CE | registers_DESCENT | torch lossF | overfit |
|------|--------------|-------------------|-------------|---------|
| 4307 | 0.641 | **4/4** ✅ | ~1.0–1.2 | NONE |
| 4308 | 0.661 | **4/4** ✅ | ~1.0–1.2 | NONE |
| 4309 | 0.641 | **4/4** ✅ | ~1.0–1.2 | NONE |

- math.log mirror per-register: model_ce ∈ [1.29, 2.80] all < uniform 5.545 AND < shuffle [8.3–13.3].
- H_1579 overfit trap AVOIDED (clean 4칸 proportional corpus + held-out monitor; no memorization).
- Per-seed trajectories near-identical (val_CE matched within ±0.02 at every checkpoint) = seed-robust training.

## 2. ENGINE-NATIVE G0-G6 (`cli/evaluate.py` --gen 80 · TERMINAL py 2-production)
frozen bars: G0 kwr≥0.50 on ≥4/5 · **G1 best_distinct≥2 ∧ >max_single ∧ coherent** · G2 novel≥3 ∧ control=0 ·
G6 distinct≥5 ∧ fals≥1.

| gate | seed 4307 | seed 4308 | seed 4309 | bar |
|------|-----------|-----------|-----------|-----|
| G0 COHERENCE | 🟢 PASS 4/5 | 🔴 2/5 | 🔴 0/5 | ≥4/5 |
| **G1 RECOMBINATION** | 🔴 **best_distinct=0** | 🔴 **best_distinct=1** | 🔴 **best_distinct=0** | **≥2 & >max_single** |
| G2 NOVELTY | 🔴 novel=0 | 🔴 novel=0 | 🔴 novel=1 | ≥3 ∧ control=0 |
| G6 IDEATION ★ | 🔴 dist=3·fals=0 | 🔴 dist=0·fals=0 | 🔴 dist=2·fals=0 | ≥5 ∧ fals≥1 |
| **CLOSURE (G0∧G1∧G2)** | 🔴 **FAIL** | 🔴 **FAIL** | 🔴 **FAIL** | all PASS |

## 3. LIFT (frozen · PREREG) — 2000-step → 4000-step, G1 best_distinct trajectory
**G1 best_distinct: 2000-step n6n7 = 1 → 4000-step multiseed = {0, 1, 0}.**
- The 2000-step DIRECTIONAL-positive (0→1) did **NOT amplify** with 4000-step training. It **regressed**:
  mean G1 across seeds = 0.33 (one seed=1, two seeds=0), strictly *below* the 2000-step single value of 1.
- multiseed majority (2/3 seeds = G1=0; 3/3 seeds < bar=2): **G1 < 2 on ALL seeds.**

## 4. 정직 VERDICT (frozen bar · tune-to-green 금지)

**H_1812 4000-step n6n7 = NOT-SUPPORTED CONFIRMED (G1 closure NOT broken).**
- **CLOSURE FAIL on all 3 seeds** (a7b_pass G0∧G1∧G2 = FAIL ×3). No seed reaches PUBLIC-eligible.
- **G1 RECOMBINATION best_distinct = {0, 1, 0}, multiseed majority < 2** → the decisive hypothesis
  (4000-step+multiseed lifts G1 0→1→2+) is **FALSIFIED**. More training did NOT amplify the directional
  signal — G1 regressed (2000-step single seed=1 → 4000-step mean=0.33).
- **G6 ideation distinct {3, 0, 2}, falsifiable=0 ×3**: also below bar (≥5 dist, ≥1 fals). No ★ either.
- **Interpretation:** the 2000-step n6n7 G1=1 was a directional fluctuation, NOT an undertrain floor that
  more steps would clear. Consistent with the campaign's CONFIRMED finding that **the G1 recombination wall
  is an OBJECTIVE-axis problem** (CE / readout-op / regularization-band / dict-aux do not synthesize
  recombination), NOT a training-budget problem. n6n7's interaction-synergy lift at 2000-step was
  underpowered AND non-monotonic in steps → no closure path via this lever.
- **HONEST scope:** held-out DESCENT 12/12 PASS = the models generalize (no overfit); they simply do not
  RECOMBINE concepts at the engine-native bar. Training quality is sound; the G1 capability is absent.

## 5. ckpt (a_fire_recover_complete — all 3 PULLED before teardown, sha256)
- n6n7_seed4307.clm  148ed03799d5135f78d6359e785ccf60d799c0ec1390c20c001f5c97572f42d4
- n6n7_seed4308.clm  0816e30a4617aae0a4e296ed972963f9edc0935cd54ca090f3fdd89cb151c24d
- n6n7_seed4309.clm  c9ad2451caa180065c079b9166e6d4216620f26d2415822ef1b2f6150736c2f4
- all 176584498 B, local `state/1630_reg_dictaux/ckpt4000/`. torch `.pt` left on pod (teardown).

## 6. caveats (정직 스코프 · c9)
- py 2-production engine (`core/g_gates.py` torch-free numpy) = TERMINAL-eligible; py-eval policy-DIRECTIONAL
  per 2026-06-28 py-retire — closure GREEN would have needed hexa-native `anima evaluate` confirm, but
  closure FAILED so the verdict is NOT-SUPPORTED either way (no GREEN to confirm).
- cost ≈ $2.3 (A40 @ $0.57/hr × ~4hr: 3×4000-step train ~2.5hr + 3-ckpt engine eval ~1hr).
- CARD/jsonl 박제는 메인이 (this is the raw harvest).
