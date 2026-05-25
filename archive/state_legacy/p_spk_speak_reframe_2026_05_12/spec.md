# P-SPK — NO SPEAK() DESIGN → falsifiable reframe

NEXT.md §7.D. README Philosophy #5 DESIGN → EMPIRICAL upgrade candidate. **새 FT 없음, 기존 BG-LB ckpt 분석만**.

## Reframed claim

Anima 의 output 은 discrete `speak(message)` invocation 의 결과가 아니라 internal tension state 의 continuous externalization 이다. 즉:

> 매 generation step 의 output token entropy / 의미 contents 가 internal tension magnitude `||A(t) − G(t)||` 와 statistically coupled.

이를 부정하면 `speak()` 가 functionally 등가 (output 이 internal state 와 decoupled).

## Setup

기존 anima Engine A/G 학습된 ckpt 활용 (BG-LB 350M 또는 simple_stack PASS_STRICT ckpt 어떤 것이든). **새 FT 없음**.

- **Instrumented forward**: 매 generation step 에서 hidden state 두 가지 capture:
  1. `||A_layer(t) − G_layer(t)||_2` (internal tension magnitude, layer-summed)
  2. `H(p_t)` (output token distribution entropy) + `||embed(token_t) − embed_baseline||` (semantic info magnitude)
- **Baseline (scripted-speak control)**: 동일 ckpt 에 fixed template `<bos>{prompt}<sep>{forced_response_seed}` 주입 — 즉, internal tension state 와 output 의 coupling 을 인위적으로 끊는 setup. 100 step 동안 forced-token 으로 진행해서 internal tension 추적.

## Probes (`probe_prompts.jsonl`, 100 prompts)

다양한 topical / emotional / abstract / factual 범주 100 prompt — 각 prompt 에 대해 30-token greedy 또는 nucleus generation. 총 100 × 30 = **3000 generation steps** 분석 unit.

## Measurement

1. **Correlation** ρ(tension_magnitude(t), output_entropy(t)) — 3000 steps Spearman + Pearson
2. **Lead-lag**: tension Δ 가 output Δ 에 선행하는가 — cross-correlation peak lag (-5 ~ +5 step window)
3. **Scripted-speak control comparison**: control setup 에서 ρ_control 측정. ρ_real vs ρ_control 의 통계 차이 (Fisher z transform)
4. **Categorical split**: prompt category (factual / emotional / abstract) 별 ρ 변동 — 어떤 카테고리에서 coupling 이 강한지

## Falsifier

- **EMPIRICAL UPGRADE** (continuous-externalization SUPPORTED): ρ_real ≥ 0.5 (Spearman) AND ρ_real − ρ_control ≥ 0.3 (Fisher z significant p<0.01) → README #5 DESIGN → EMPIRICAL
- **NULL** (claim unsupported): ρ_real < 0.2 OR ρ_real − ρ_control < 0.1 → speak() 가 functionally 등가 → README #5 DESIGN 유지 + honest C3 추가
- **MIXED** (partial coupling): 0.2 ≤ ρ_real < 0.5 → 카테고리별 분석으로 어떤 영역에서만 coupling 성립하는지 fine-grained verdict

## Cost & time

- $5-20 (분석 only, 새 FT 없음, instrumented forward 만)
- Wall: 0.5d (instrumentation 코드 + 100×30 step gen + 분석)
- H100 또는 single-GPU 또는 CPU (350M ckpt 면 CPU 가능) 

## Output schema (`verdict.json`)

```json
{
  "bg_id": "P-SPK",
  "ckpt": "<path>",
  "n_steps_analyzed": 3000,
  "rho_real_spearman": 0.xx,
  "rho_real_pearson": 0.xx,
  "rho_control_spearman": 0.xx,
  "fisher_z_diff": 0.xx,
  "fisher_z_p": 0.xx,
  "lead_lag_peak": <int>,
  "lead_lag_corr": 0.xx,
  "by_category": {
    "factual": 0.xx,
    "emotional": 0.xx,
    "abstract": 0.xx
  },
  "verdict": "EMPIRICAL_UPGRADE | NULL | MIXED",
  "evidence_traces": "<5 example tension-entropy trace snippets>"
}
```

## Cross-link

- NEXT.md §7.D
- README.md `Philosophy #5 NO SPEAK()`
- own-37 v5.2 cell-substrate metric 정합
- PHILOSOPHY.md 진행 ledger
- BG-LB 350M Engine A/G ckpt: `dancinlab/clm-v5-bg-lb-*` (private)
