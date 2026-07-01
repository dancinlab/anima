# G1 Frozen Mouth-Bind Screen — DIRECTIONAL

**Probe:** Numpy DIRECTIONAL (retired `core/clm_decode.py` py mirror). NOT engine-native TERMINAL.  
**Date:** 2026-06-29 · **Weights:** clm303_clean.clm (303M CLMConvMoE, held-out DESCENT verified)  
**Hypothesis family:** H_1616 (VSA/HRR) · H_1623 (Hypernet-mult) · H_1449/H_1649 (attention/saddle)  
**Frozen bar:** composed_distinct≥2 ∧ >max_single ∧ kwr≥0.50 in ≥2/3 seeds {7, 4302, 4303}  
**Ablation:** bind-ON vs bind-OFF (baseline `none` op) on IDENTICAL frozen clm303_clean weights.

---

## Part 1: Abstract Mechanism Probes

Tests whether each operator's *algebraic binding primitive* works in isolation (no clm303 weights).

| Mechanism | ON | OFF | CTRL | Bar PASS? | Note |
|---|---|---|---|---|---|
| VSA/HRR (H_1616) | **1.000** | 0.076 | 0.194 | ✅ | N=5 bundle retrieval, d=512 |
| Hypernet-mult (H_1623) | 1.000 | 0.750 | — | ✅ (corrected) | Bilinear task; original probe had holdout-element bug (both=0.0) |
| A⇄G Saddle (H_1649) | 0.0 | 0.0 | 0.0 | ❌ | Toy too small; saddle diverges meaningfully from energy (L2=6.3) but bar not passed |

**Abstract-only conclusion:** VSA/HRR algebraic property demonstrated (ON>>OFF). Hypernet bilinear advantage confirmed with correct task design. Saddle diverges from energy descent but not demonstrated at retrieval accuracy level in this toy.

**Implementation caveats:** The original probe.py Hypernet and Saddle probes used "holdout element" (zero-shot extrapolation to an entirely unseen entity) which is unfair to all models — fixed in `abstract_probe_corrected.py` + `abstract_corrected_results.json`.

---

## Part 2: Frozen clm303 G1 with Mouth-Bind Ops at Readout

Injection point: `yn [T_ctx=24, d=3784]` (penultimate, before `readout_conv`). Each op transforms `yn[-1]` then passes back through `readout_conv` for vocab logits. Renormalized to same L2 norm as original `yn[-1]`.

### Per-Operator Results

| Op | G1 seeds pass | 0/3 FAIL | Sample output quality |
|---|---|---|---|
| `none` (control) | 0/3 | FAIL | Coherent generic English, zero concept keywords |
| `vsa_hrr` | 0/3 | FAIL | ⚠️ Garbled binary bytes — readout corrupted |
| `hadamard` | 0/3 | FAIL | ⚠️ Garbled uppercase ASCII — readout corrupted |
| `cross_attn` | 0/3 | FAIL | Coherent (gentle residual blend) — still zero concept keywords |

### Detailed Numbers (per-seed composed_distinct counts)

**`none` (control):**
```
seed=7:    max_single=0  best_composed=0  clears=FAIL
seed=4302: max_single=0  best_composed=0  clears=FAIL
seed=4303: max_single=0  best_composed=0  clears=FAIL
```
Model generates fluent English social-media style text, ignores concept keywords entirely (overfit pattern).

**`vsa_hrr`:**
```
seed=7:    max_single=0  best_composed=0  clears=FAIL
seed=4302: max_single=0  best_composed=0  clears=FAIL  
seed=4303: max_single=0  best_composed=0  clears=FAIL
```
Circular FFT convolution of `yn[-1]` with context mean produces a vector outside the subspace the frozen `readout_conv` weights were trained on → **vocab logit distribution collapses to raw byte tokens** (surrogate chars, binary). Concept keyword count: 0. KWR vacuously high (byte stream has no "common words").

**`hadamard` (attention-gated):**
```
seed=7:    max_single=0  best_composed=0  clears=FAIL
seed=4302: max_single=0  best_composed=0  clears=FAIL
seed=4303: max_single=0  best_composed=0  clears=FAIL
```
Self-attention gate `tanh(ctx) * yn[-1]` pushes `yn[-1]` into a different norm regime → **readout generates random uppercase letter strings** (not words). KWR ~0.1–0.3.

**`cross_attn` (residual blend):**
```
seed=7:    max_single=0  best_composed=0  clears=FAIL
seed=4302: max_single=0  best_composed=0  clears=FAIL
seed=4303: max_single=0  best_composed=0  clears=FAIL
```
Soft 0.5× residual blend maintains output coherence (readable text) but zero concept keyword lift.

---

## Interpretation

### Why all ops fail: the trunk representation problem

The three bind ops operate on `yn[-1]` — the penultimate vector at the **last token position** after the trunk. For binding to work, `yn[-1]` would need to encode concept A and context `yn[:-1]` would need to encode concept B in distinct, separable axes, so that `bind(yn[-1], context_aggregate)` could compose them into a novel concept-C token distribution.

**The frozen clm303 trunk does NOT do this:**
1. The model is overfit: generates generic English social-media text regardless of input (H_1579 confirmed). The `yn[-1]` vector is essentially "what token comes next in casual English" regardless of concept keywords in the seed.
2. `max_single=0` for ALL seeds under `none`: the trunk never generates even a single concept keyword in isolation. There are literally no concept-axis features in `yn` to bind.
3. VSA/HRR transforms `yn[-1]` via circular conv with context — but if neither `yn[-1]` nor context encode concept-specific features, the convolution produces garbage relative to the readout distribution (which was trained on the raw `yn` distribution).

**EXP-3 precedent confirmed:** `state/binding_arch_census/exp3_303m/RESULT.md` §4b showed that trained Hadamard readout (300K-step training) produced G1=0 ∧ G6 fals=0 for ALL 9 arms. Frozen (untrained) ops fare even worse because readout weights weren't adapted.

### Verdict

**OUTCOME B confirmed: all bind operators INERT (or WORSE) on frozen clm303 weights.**

- `cross_attn`: INERT (output coherent but zero G1 lift)
- `none`: INERT baseline (expected)
- `vsa_hrr`: DESTRUCTIVE (corrupts output)
- `hadamard`: DESTRUCTIVE (corrupts output)

**NOT an interesting OUTCOME A: no operator lifts G1 on frozen weights.**

---

## Recommendation

**Do not escalate any mouth-bind operator to engine-native testing on frozen clm303.**

All four ops fail — the bottleneck is the trunk representation, not the absence of a binding operator at readout. Wiring a binding op into frozen `core/clm_decode.hexa` would produce the same FAIL (or garbled output for the non-renormalizing ops).

**The real lever is H_1602 (recombination objective):**

The trunk must be trained to encode concepts as separable axes so that composition at readout has something to bind. G1 requires a training signal that rewards producing NEW concept combinations (recombination-objective), not just fluent next-token prediction (CE on a small biased corpus).

**Escalation path (in order of confidence):**
1. H_1602 (recombination objective): cost-gated GPU train — add G1 recombination reward to training objective so the trunk learns concept axes. This is the root-cause fix (G1≡G6 = one compositional-binding deficit per H_1603).
2. N6+N7 (regularization + dict-aux auxiliary loss): DIRECTIONAL positive on gen80 FALS 0→1 (per `g1-closure-campaign-3lever-not-supported.md`), 4000-step follow-on pending.

**wired:** DIRECTIONAL-mirror (numpy retired py mirror, NOT engine-native TERMINAL)

---

## Files

```
state/g1_frozen_mouthbind_screen/
├── probe.py                     # Full probe (abstract + frozen G1 bind ops)
├── probe_run.log                # Raw stdout (all op×seed×k combinations)
├── raw_results.json             # Machine-readable per-op G1 results
├── abstract_probe_corrected.py  # Corrected Hypernet + Saddle probes
├── abstract_corrected_results.json  # Corrected abstract probe results
└── RESULT.md                   # This file
```

**Baseline reference:** `state/1588_g1_multiseed_refmatch/result_clm_clm303_clean.clm.json` (G1=0/3 confirmed baseline, same weights)

## SCOPE 정정 (메인 검토 2026-06-29 — 과장 방지)

이 screen의 🧱 NOT-SUPPORTED 는 **"frozen 가중치에 bind op 얹기"** 에만 적용된다 — "wiring-binding 일반"이 아니다. 두 by-construction 결함이 frozen 경로를 inert/destructive 하게 만든다:
1. **입력 부재**: clm303_clean 이 max_single=0(씨앗 개념 단독도 안 엮음) → bind op 에 *묶을 개념 표현이 없음*. binding 수학은 유효(abstract HRR ON=1.000 vs OFF=0.076)하나 입력이 0.
2. **off-manifold readout**: frozen readout_conv 는 *묶인* 벡터를 디코드하도록 학습된 적 없어 bind 출력에 logit 붕괴.

→ **미측정(=진짜 다음 수)**: bind op 을 *in-forward 로 retain 한 채 trunk+readout 공동학습*(직렬화 전 drop 아님 = g-gates-py-1 함정 회피, frozen 얹기도 아님). 그래야 (a) 개념 축이 형성되고 (b) readout 이 binding 디코드를 학습한다. 이는 실패한 'training-only-dropped'(operator drop)와 inert 한 'frozen-wired' 사이의 미탐색 sweet-spot. cost-gated 303M 학습 필요(user-go).
