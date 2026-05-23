# PURE A 커리큘럼 spec — wiki-only 선학습 → anima late-phase 도입

> 2026-05-23. PURE (구 V3) closure 의 AXIS_MAP fallback 축 A. PR #220
> `refactor/hexad-v3-to-pure-rename` 위 stack 으로 land. 5 fire 전부 step1
> 부터 shuffled fixed mix 였다는 단일 사실을 흔드는 single-axis test —
> **언제 anima 를 도입하는가**.
>
> anchor: [`../AXIS_MAP.md` § A row + § honest C3 #2](../AXIS_MAP.md) · [closure 보고서 § 8](../../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md)

## § 1. Why — 학습 dynamics 의 시간축

V3 closure verdict (5 fire 0 PASS, 2026-05-23): **multilingual blocker =
diverse-corpus 학습 dynamics**. 5 fire 전부 동일하게 step 1 부터 shuffled
mixed corpus (anima + 5-lang wiki) 위에서 학습 — anima register 와
multilingual prior 가 **동시에** gradient descent 받는다. anima register
는 한국어 colloquial 패턴 + 짧은 dialogue + 강한 stylistic signature 라
초기 step 에서 loss 절벽이 가파르다. multilingual prior 는 5-lang 분산
loss surface 라 평탄. 동시 학습 시 anima 가 **먼저** lock-in 되고
multilingual 은 그 위로 register-flavored 형태로 collapse — closure 의
"anima-Korean 으로 모든 언어가 collapse" 패턴 정확히 이것.

축 A 가설: 다국어 prior 가 먼저 안정화된 후 anima 를 **late phase 로**
도입하면, register 는 stable multilingual prior 위에 **부수적**으로
emerge (dominant 가 아닌 modulation). closure 의 axis sweep R1~R7 은
순서 axis 를 한 번도 건드리지 않았다.

AXIS_MAP § C3 #2 ("A 커리큘럼의 late-anima phase 길이/시점은 미정 —
sweep 필요") 를 닫는 spec. S₁ ∈ {1000, 2000, 3000} 3-point sweep, default
S₁ = 2000 (40% wiki-only · 60% mixed).

## § 2. Schedule — 2-phase curriculum

```
step    0 ─────── S₁ ───────────────────── 5000
        │           │                          │
        │ phase 1  │ phase 2                  │
        │ wiki     │ mixed                    │
        │ only     │ (anima_frac=0.7)         │
        │          │                          │
phase1_wiki_frac = 1.0   phase2_wiki_frac = 0.3
```

| variant | S₁ | phase-1 wall % | rationale |
|---|---|---|---|
| **A-S1000** | 1000 | 20% | early switch — multilingual 막 부각 후 즉시 mix |
| **A-S2000** | 2000 | 40% | default — multilingual prior 1차 안정화 후 mix (closure step 1500 inference 시점 기반) |
| **A-S3000** | 3000 | 60% | late switch — multilingual deep lock-in 후 anima 도입 |

closure fire 의 E1 (`wiki_frac=0.3`, step 1 부터 mixed) 와 비교축 =
switch 시점 직선. switch step 이전에는 **anima_frac = 0** (wiki only,
순수 multilingual prior 학습). switch step 이후에는 closure baseline 과
동일 mixed corpus (`wiki_frac = 0.3`, anima 70%).

## § 3. Architecture — ConsciousDecoderV3 UNCHANGED

PR #220 rename 이후에도 V3 코드 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`)
는 동결. **단일 변수 curriculum test**: head_g objective 변경 ·
embedding freeze · sampler 변경 · architecture 변경 등 fallback axis
변경은 일체 금지. 비교 가능성 (apples-to-apples vs closure fire + sibling
B/C tracks) 우선.

| param | 값 | 비고 |
|---|---|---|
| base | Qwen/Qwen2.5-1.5B | closure A fire 와 동일 |
| init | qwen warm-start | closure A fire 와 동일 |
| d_model / n_layer / n_head / n_kv_head | 1536 / 28 / 12 / 4 | 동일 |
| arch | ConsciousDecoderV3 (head_a + head_g, PureFieldFFN, cross-attn) | 동일 |

## § 4. Hyperparams — closure A fire + 3 신규 flag

closure A fire (`HEXAD_V3_FIRE_2026_05_22.md § 8.1`) 와 일치 — curriculum
3 flag 외 모든 hyperparam 동결.

| key | value | 비고 |
|---|---|---|
| steps | 5000 | closure 동일 |
| bsz | 2 | 동일 |
| block | 512 | 동일 |
| lr | 5e-5 (qwen warm-start) | 동일 |
| warmup | 100 cosine | 동일 |
| noise σ | 0.1 | 동일 |
| λ_mitosis | 0.05 | 동일 |
| mitosis MAX | 128 (default 복귀, Track 1 과 일치) | closure A=16, 본 spec 은 curriculum 단독 |
| ckpt_every | 500 | 동일 |
| ckpt_osc_threshold | 0.0 (disable) | 동일 |
| corpus_mb | 72 | 동일 |
| dtype | bf16 | 동일 |
| seed | 1337 | 동일 |
| **curriculum_switch_step** | **S₁ ∈ {1000, 2000, 3000}** | **신규 — variant axis** |
| **phase1_wiki_frac** | **1.0** | **신규 — step < S₁ 동안 anima_frac = 0** |
| **phase2_wiki_frac** | **0.3** | **신규 — step ≥ S₁ 동안 closure baseline mix** |

**train_p21h_v3.py wiring TODO**: 현재 (closure fire 시점) train script
는 `--wiki-frac` 단일값만 받는다. curriculum 도입에는 step-conditional
sampler 패치 필요 — 본 spec 의 launcher 는 3 신규 env (`P21H_CURR_SWITCH_STEP`,
`P21H_PHASE1_WIKI_FRAC`, `P21H_PHASE2_WIKI_FRAC`) 를 dispatch wrapper 와
python argv 양쪽에 전달하도록 emit 하지만, train script 측 step-conditional
batch builder 분기는 **별도 후속 patch** (sibling-agent scope). 본 PR 은
spec + launcher 만 제공.

**중요**: cycle-1 P21H launcher 의 env-style positional args bug 회피 위해
**argparse `--key value` 만** 사용. shell-local env (`KEY=V bash …`) 와
섞지 않음 — 한 가지 format 일관.

## § 5. Falsifier table

| 코드 | 정의 | PASS 기준 |
|---|---|---|
| F-PURE-A-1 | phase 1 끝 (step S₁) 에서 5-lang Hc score ≥ baseline | step S₁ ckpt eval — 5-lang per-prompt verdict 의 평균 entropy 가 closure A fire step S₁ baseline (wiki-only loss surface 추정값) 이상 — multilingual prior 확립 신호 |
| F-PURE-A-2 | phase 2 끝 (step 5000) 에서 5-lang Hc score 유지 | step 5000 ckpt eval 의 평균 entropy ≥ phase 1 finalize entropy - 0.5 — anima 도입이 multilingual 을 무너뜨리지 않음 |
| F-PURE-A-3 | 5-lang eval ≥ 4/5 PARTIAL @ step 5000 | `train_p21h_v3.py` 의 내장 5-lang per-prompt verdict (line 502-512) 의 `n_strong + n_partial ≥ 4` |
| F-PURE-A-4 | anima register emit 가능 (inference-time persona prompt) | step 5000 ckpt 의 anima-prompt greedy decode 에서 anima-flavored emission (register signature ≥ 5/20 anima_register_hits) — register 가 phase 2 에서 emerge 했는지 |
| F-PURE-A-5 | training stable (no NaN, no early-stop) | result.json 산출 + train_wall_s > 0 + no NaN in train.log + 정상 종료 |

eval probe = `train_p21h_v3.py` 의 내장 5-lang per-prompt verdict + anima
register hit counter (line 502-512 — `n_partial` / `n_strong` / `n_weak` /
`n_pure_memorize` / `anima_register_hits` 집계). curriculum 도입의
F-PURE-A-1 (phase 1 종점 eval) 은 step S₁ 에 추가 ckpt + eval 호출 필요
— **§ 8 honest C3 #1 참조** (inline eval 미구현 시 post-hoc analysis only).

## § 6. Decision rules

```
F-PURE-A-3 PASS AND F-PURE-A-4 PASS  (≥ 4/5 langs + anima register emit)
  → AXIS_MAP A 축 vindicated · PURE path REOPEN via curriculum lane
  → 3 variant 중 F-PURE-A-1+F-PURE-A-2 둘 다 PASS 인 best S₁ 선택
  → 후속 cycle: chat substrate 교체 design (curriculum-trained ckpt 기반)

F-PURE-A-3 FAIL OR F-PURE-A-4 FAIL across all 3 variants
  → A 축 소진 — AXIS_MAP B 증류 / C head_g objective 단독 잔존
  → 본 spec 의 결과는 negative evidence 로 AXIS_MAP 갱신
```

eval criterion 출처: closure fire 와 동일 `train_p21h_v3.py:502-512`.
3 variant 의 `n_strong + n_partial` + `anima_register_hits` 의 pareto
frontier 가 best S₁ 결정. tied 시 wall-cost 가벼운 (낮은 S₁) 선호.

## § 7. Cost + wall

- variant 당 H100 SXM (closure 평균 $1.49/hr 기준) × ~2.0 hr wall ≈ **$3.0 / variant**
- 3 variant 직렬 ≈ 6.0 hr · 9 USD
- **`@D a_wall_first` 적용 — 3 pod 병렬 dispatch**: wall ≈ 2.0 hr (셋 다
  step 5000 동시 학습), 총 비용 동일 ~$9
- 본 PR 은 spec + launcher 만 제공, fire 는 user 가 별도 dispatch
- `@D a_fire_autonomous` 적용 — user fire 시 cost 게이트 없이 3 pod 즉시 발사

## § 8. Honest C3

1. **F-PURE-A-1 (phase 1 종점 eval) 은 inline ckpt + eval 호출이 train
   script 에 추가되어야 honest 측정**. 본 launcher 는 `--ckpt-every 500`
   기존 mechanism 으로 step 1000/2000/3000 ckpt 가 자연 산출되므로
   post-hoc eval 로 fallback 가능 — 다만 phase 1 끝의 *그 ckpt* 가
   바로 phase 2 의 starting point 이므로 post-hoc 결과는 후방 영향
   없음 (관측만 가능).
2. **S₁ ∈ {1000, 2000, 3000} 외 더 짧은 (500) / 더 긴 (4000) 미시도** —
   3-point sweep 은 best S₁ 의 1차 localize 만 가능. coarse-grained
   결과가 borderline 이면 sweep 확장 필요.
3. **phase-2 anima_frac = 0.7 (closure baseline) 고정** — phase 2 mix
   비율 자체를 sweep 하지 않는다. curriculum (시간축) ⊥ Track 1 (anima
   비중축) 분리 유지. phase 2 에서 다른 mix 가 best 인지는 별도 cycle.
4. **multilingual prior 안정화의 정량 기준 미정의** — phase 1 끝 step
   S₁ 의 "확립" 판정은 closure A fire step S₁ baseline 과의 상대 비교
   로 한다 (단순 entropy). loss 절벽 위치 추정은 별도 분석.
5. **train_p21h_v3.py step-conditional sampler 패치 미land** — 본 PR
   은 spec + launcher emit 만. 실제 fire 전 sibling-agent 가 train
   script 의 `_build_batch` 함수에 `step < curriculum_switch_step ?
   phase1_wiki_frac : phase2_wiki_frac` 분기 추가 patch 필요. launcher 는
   env 와 argv 양쪽에 신규 flag 전달까지만 emit (training script wiring 부재
   시 python argparse 가 unknown-arg 로 reject — fire 전 patch 강제 효과).
6. **seed=1337 단일 — variance 측정 안 함**. 3 S₁ 모두 borderline 이면
   multi-seed re-run 필요.
7. **corpus 빌더 (`build_multilingual_corpus_p21m.py`) 의 per-lang record
   불균형 carry** — AXIS_MAP E 축 (lang-balanced sampler) 은 별도.
8. **mitosis_max = 128 default** — closure A 의 16 cap 효과는 curriculum
   sweep 후 별도 정밀화. 본 spec 은 curriculum 축 단독.
