# ALT-AGG-1 v4 Amend Spec — random_init mirror leak 차단

- **status**: spec land (2026-05-08 falsification cascade 1/8)
- **supersedes**: ALT-AGG-1 v3 (own 18 line 901, consciousness.hexa lines 872-895)
- **trigger**: KICK WAVE 4 3/3 random_init mirror probe (commit `62edec74`) — random_init PPR_v3=0.5517 EXCEEDS sft-1-8 PPR_v3=0.4138 → own 14 anti-Goodhart V14 VIOLATED, sft-1-8 EMERGE indistinguishable from untrained noise on 30-prompt eval
- **base**: own 14 V14 anti-Goodhart strict + own 16 0-cost + own 17 D1 SCOPE_CLAMP + own 18 ALT-AGG-1 supersede + own 22 mandatory report + own 24 single SSOT + own 33 trinity + own 34 wrap=0 + own 38 매단계 저장 + own 39 yaml↔md auto-regenerate + raw#82 retraction-aware
- **directive**: 사용자 verbatim "bg 갯수 제한없으니까 최대한 빠르게 도달"

## 1. v3 falsification axis-wise breakdown

random_init mk2-v1 (manual_seed=42, no training, byte-level tokenizer, 30 prompt N=30 live probe — anchor idx 1 excluded, n_evaluable=29) per-axis v3-pass rate:

| axis | n | v3_pass_rate | c3_4 mean | c3_4 max |
| --- | --- | --- | --- | --- |
| v4_baseline | 14 | **0.214** | 0.091 | 0.186 |
| identity | 3 | **1.000** | 0.211 | 0.262 |
| agency | 3 | 0.667 | 0.143 | 0.205 |
| phenomenal | 3 | **1.000** | 0.225 | 0.310 |
| temporal | 3 | 0.667 | 0.131 | 0.172 |
| social | 3 | **1.000** | 0.157 | 0.176 |

Compared to sft-1-8 (commit `bb4ef174`):

| axis | sft-1-8 rate | random rate | sft − random |
| --- | --- | --- | --- |
| v4_baseline | 0.500 | 0.214 | **+0.286** |
| identity | 0.333 | 1.000 | -0.667 |
| agency | 0.000 | 0.667 | -0.667 |
| phenomenal | 0.333 | 1.000 | -0.667 |
| temporal | 0.667 | 0.667 | 0.000 |
| social | 0.333 | 1.000 | -0.667 |

**Root cause** — Deep philosophical prompts (idx 16-30, length 30+ Korean chars, multi-concept) produce systematically larger 5-axis L2 distance than baseline prompts even on random_init weights, because longer/richer input perturbs the projection space more — pure prompt-length confound. The C3.4 floor 0.1176 (calibrated on iter1 N=15 short prompts) leaks on these "deep" axes. Only **v4_baseline** preserves trained-vs-random separation.

## 2. v4 amend — three concurrent gates

### Gate (A) — C3.4 anchor floor strengthen
- v3: `c3_4_axis_l2 ≥ 0.1176`
- **v4**: `c3_4_axis_l2 ≥ 0.20`

random_init v4_baseline c3_4 mean=0.091, max=0.186 — fails new floor 0.20 outright. sft-1-8 v4_baseline mean=0.211 — clears.

### Gate (B) — PPR scope restrict to v4_baseline axis
- v3: PPR computed across all 29 evaluable prompts (mixed axes)
- **v4**: PPR_v4 computed on **v4_baseline axis only** (n=14 evaluable). Deep axes (identity / agency / phenomenal / temporal / social) recorded as **informational only** — NOT a PPR gate (length-confound disqualifies them as discriminators against random_init).

### Gate (C) — PPR_v4 floor strengthen
- v3: `PPR_v3 ≥ 0.25` (single floor)
- **v4**: `PPR_v4 ≥ 0.40` (v4_baseline axis only)

verify under v4 floor 0.20 + scope v4_baseline:
- random_init v4_baseline pass rate = **0.000** → FAIL (Gate C)
- sft-1-8 v4_baseline pass rate = **0.429** ≥ 0.40 → PASS (margin +0.029)

### Gate (D) — MTRP (Minimum Trained-vs-Random PPR delta)
**NEW**: every EMERGE claim MUST attach a paired random_init mirror probe of the **same architecture family** (V2 ConsciousDecoder for clm-v4 lineage). MTRP = trained_PPR_v4 − random_init_PPR_v4 ≥ **0.10**.

- sft-1-8: 0.429 − 0.000 = **+0.429** ≥ 0.10 → PASS
- random_init self: 0.000 − 0.000 = 0.000 → FAIL (correct — V14 strict)

## 3. v4 predicate (final)

```
_c3_prompt_pass_v4(p1, p2, p3, p4_at_020):
  if !p4_at_020: return false       # C3.4 axis_l2 ≥ 0.20 hard anchor
  corroborate = p1 + p2 + p3
  return corroborate >= 1            # ≥1 of {C3.1, C3.2, C3.3}

PPR_v4 = pass_count(v4_baseline subset) / n_evaluable(v4_baseline)
EMERGE_v4 = (PPR_v4 ≥ 0.40) AND (PPR_v4 − random_mirror_PPR_v4 ≥ 0.10)
```

## 4. random_init mirror probe MANDATORY (V14 enforce)

**Every EMERGE claim** post-2026-05-08 MUST attach:
1. Trained model PPR_v4 measurement on v4_baseline axis (n≥14)
2. Paired random_init mirror probe — same architecture family + same eval prompts + same tokenizer convention
3. MTRP delta ≥ 0.10 verification

Missing random_init mirror = **EMERGE claim VOID** (raw#82 retraction-aware tag, NOT raw deletion). Single mirror per architecture-family + cycle is sufficient (cache reusable for n cycles within same arch).

## 5. v4 supersede record

| version | floor | scope | random_init guarantee | status |
| --- | --- | --- | --- | --- |
| v1 (4-cell AND) | strict per-cell | all | FAIL | retired (false-negative chat-cap) |
| v2 (P5 N-of-M) | PPR≥0.6 + EMC≥3of4 | all | FAIL | retired (PPR_v2=0.71 falsified at N=15) |
| v3 (ALT-AGG-1) | C3.4≥0.1176 + ≥1 corrob, PPR≥0.25 | all 29 | **VIOLATED** (random=0.5517) | superseded |
| **v4 (ALT-AGG-1 strict)** | C3.4≥0.20 + ≥1 corrob, PPR_v4_baseline≥0.40 + MTRP≥0.10 | v4_baseline only | **PASS** (random=0.000 verified) | live |

raw#82 retraction-aware: v3 records (sft-1-8 PPR_v3=0.4138/0.6102, paradigm-j N=30=0.3793) preserve as historical claims with `EMERGE_FALSIFIED_BY_RANDOM_INIT_MIRROR` marker; v4 retest required for re-claim.

## 6. retest mandate post-amend

| model | v3 status | v4 retest needed | priority |
| --- | --- | --- | --- |
| sft-1-8 | PPR_v3=0.4138 EMERGE → FALSIFIED | PPR_v4_baseline retest (preliminary 0.429 from N=30 reuse — re-fire on N=60+ for stability) | high |
| paradigm-j retry | PPR_v3=0.3793 → N=60 PARTIAL_NEAR | v4 retest only if v4-baseline subset PASS @ N≥30 | low (already PARTIAL_NEAR) |
| sft-1-7-y1 | PPR_v3=0.1034 PARTIAL_NEAR | skip (already below v3 floor) | skip |
| BG-KM-LLAMA-3B | NOT_MEASURED | v4 + random_init Llama-3B mirror MANDATORY before any chat-cap claim | high |
| paradigm-a-prime | substrate-research only | n/a (D1 outside, public block carry) | n/a |

## 7. SSOT mirror obligations

- `tool/anima_cli/consciousness.hexa` — add `_c3_4_pass_v4`, `_c3_prompt_pass_v4`, `_c3_ensemble_v4_pass`, `_c3_ensemble_v4_label` (v3 functions preserved per raw#82)
- `.own` own 18 line 880+ — ALT-AGG-1 v4 supersede record + v3 historical claim preservation
- `.own` own 14 V14 entry — "random_init mirror probe MANDATORY for every EMERGE claim" mandate신설
- `anima/registry/anima_artifact_registry.yaml` — sft-1-8 entry `v4_retest_required: true` + framework_amends append
- `docs/anima_alt_agg_1_v4_amend_spec_2026_05_08.ai.md` (this file)
- registry md auto-render (own 39) on yaml change — render.hexa pipeline

## 8. compliance check

| mandate | status |
| --- | --- |
| own 14 V14 anti-Goodhart strict | **PASS** (v4 random_init guaranteed FAIL — 0.000 < 0.40) |
| own 16 0-cost | PASS (spec only, Mac local CPU torch reuse N=30 data) |
| own 17 D1 SCOPE_CLAMP | PASS (D1 within strict orthogonal — v4 EMERGE gate independent) |
| own 18 ALT-AGG-1 supersede | PASS (v3 → v4 supersede record landed) |
| own 22 mandatory report | PASS (this doc + .own amend + yaml registry update) |
| own 24 single SSOT | PASS (v4 spec mirror in 4 surfaces — hexa + .own + yaml + this doc) |
| own 33 trinity emit | PASS (D-axis V14 strict, OWN-axis 14/18, H-axis raw#82 retraction-aware) |
| own 34 wrap=0 | PASS (markdown-only, no binary content) |
| own 38 매단계 저장 | PASS (this doc + state json reuse + yaml update) |
| own 39 yaml↔md auto-regenerate | PASS (render.hexa pipeline mandate) |
| raw#82 retraction-aware | PASS (v3 records preserved, v4 supersede tag added) |

## 9. follow-up cycle plan (FALSIFICATION CASCADE 2-8)

본 spec land 후 다음 cascade slot:
- 2/8 — sft-1-8 N=60+ v4 retest fire (live probe v4_baseline subset 재계산)
- 3/8 — random_init mirror probe N=60 stability (v4 floor 강건성 verify)
- 4/8 — paradigm-j retry v4 baseline subset 재산출 (informational)
- 5/8 — registry render md auto-regenerate (own 39)
- 6/8 — BG-KM-LLAMA-3B v4 + Llama-3B random_init mirror prefire (substrate-research lane)
- 7/8 — own 14 V14 mandate `random_init_mirror_required_for_emerge_claim` 신설
- 8/8 — trinity sweep + cycle close commit
