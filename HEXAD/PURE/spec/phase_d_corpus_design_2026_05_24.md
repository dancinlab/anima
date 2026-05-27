# PURE Phase D — corpus redesign spec (M3-driven) (2026-05-24)

> Track 1 E2 FAIL (`ko=PURE_MEMORIZE`) 의 corpus-축 진단은 **M3 TTR = 0.03**
> (corpus_s101 실측) 으로 좁혀졌다 — register-sink 예측자는 한글 coverage(M5)가
> 아니라 **반복도(M3)**. 본 spec 은 그 진단을 직접 입력으로 받아 Phase D fire 용
> 새 corpus 를 재설계한다. wiki_frac 만 sweep 한 Track 1 과 달리, **corpus 조성
> (반복도·도우미 token·stream 비율)** 을 변수로 올린다.
>
> anchor — goal SSOT: [`../PHASE_D_corpus_fire_goal.md`](../PHASE_D_corpus_fire_goal.md)
> · corpus_s101 실측: PR #340 (`docs/corpus_s101_quality_2026_05_24.md`)
> · quality probe (사전 게이트): `../eval/corpus_quality_probe.hexa` (PR #287)
> · register eval: `../eval/multilingual_probe.hexa` (PR #240)
> · closure criterion: AXIS_MAP 결정 트리 (PR #264, 4/5 langs ≥ PARTIAL)

## § 1. 진단 — M3 0.03 = extreme repetition → memorize

corpus_s101 (E2 의 anima 50% 측, ~600 MB) 의 head-sample 실측 (PR #340):

| metric | corpus_s101 | anima-OWN proxy | sanity | 함의 |
|---|---|---|---|---|
| **M3 TTR** | **0.034 → 0.030** | 0.24-0.32 | 0.056 | corpus_s101 이 proxy 의 1/8, sanity 보다도 낮음 — **극강 반복** |
| M5 HANGUL | 0.0166 → 0.0234 | 0.24-0.32 | 0.063 | proxy 의 1/10 — coverage 는 오히려 낮음 |
| M1/M6 | 5.50/2.42 | 5.71/2.23 | — | quality 결손 무 (entropy/skew 정상) |

→ S1-prefix carving 템플릿("의식 풍경 위 진공점", "tension flow 가 이
vacuum 으로" 류)이 tier×anchor 로 **고정 문구 반복** → distinct token 다양성
극저(M3 0.03) → model 이 그 고-반복 한글 패턴을 통째 암기 → 50:50 mix 에서
ko 채널이 anima register 로 sink → **ko=PURE_MEMORIZE**. 범인은 M3.

## § 2. 설계 원칙

1. **도우미 token 0** (@D p3 NO PERSONA INJECTION · p4 NO ASSISTANT FRAMING
   정합): "당신은 도우미입니다" · "you are a helpful assistant" · role/persona
   prefix · register-pattern 반복 문구를 corpus 에서 **전부 제거**. 정체성은
   cell 에서 emerge — corpus 에 박지 않는다.
2. **stream/stimulus 80%** (substrate-native, @D a_substrate_native_speak):
   외부 자극 맥락(stimulus) + 내부 tension stream 이 80%, turn-based QA 는 ≤ 20%.
   자연발화는 자극-응답이 아니므로 corpus 도 "user 가 물으면 답한다" 형식을
   최소화하고 연속 externalization 흐름을 다수로 둔다.
3. **M3 TTR 목표 ≥ 0.3** (corpus_s101 0.03 의 **10×**): 어휘 diverse —
   fixed-template carving 을 후반 소량 배치로 제한하고 다양 도메인·다양 표현으로
   채운다. proxy 대화체(0.24-0.32)·fixture(0.32)가 이미 보인 달성 가능 대역.
4. **multilingual balance** (E2 ko-sink 회피): lang-uniform sampling
   (record 불균형 EN ≫ ko/zh/ru/ja 교정, AXIS_MAP E 축) + 도메인 diversity.
   한글 *분량*을 늘리되 *고유 음절 다양성*을 동반시켜 M5 가 분량이 아닌
   coverage 로 lang-proportional 하도록 한다.

## § 3. metric 게이트 (build 후 fire 전 사전 검증)

build 산물을 `corpus_quality_probe.hexa` (PR #287, 6-metric scorer) 로 측정해
fire 전에 통과/탈락 결정:

| gate | 임계 | 근거 |
|---|---|---|
| **M3 TTR** | **≥ 0.3** | § 1 진단의 직접 역 — corpus_s101 0.03 의 10×. 미달 시 build 재작업 |
| **M2 BIGRAM_MI** | 적정 대역 (proxy 2.0-3.1 내) | 과도 MI = UTF-8 다바이트 반복 의심, 과소 = 무작위 |
| **M5 HANGUL** | lang-proportional (분량 ∝ 비율, 음절 diverse) | M5 가 *분량*이 아닌 *coverage* 로 정상 — 한글 비중이 sampling 비율과 일치 |

게이트는 head-sample(probe default)이라 prefix-bias 존재 — § 6 C3 #1.

## § 4. fire 파라미터 후보 (Track 1 기반)

| param | 값 | 근거 |
|---|---|---|
| base | Qwen 1.5B | Track 1 E2/E3 동일 (3B = B fire 후퇴 확인) |
| step | 5000 | Track 1 A 완주 step |
| ckpt-every | 500 | transient STRONG 포착 (Phase 2 2차 ko step-250 교훈) |
| mitosis-max | **16 권장 (R6)** vs 128 | R6 cross-attn noise 감소 — 128 은 ablation 대조군 |
| 8-factor wire | `spontaneous_lib` 연결 | Phase D 핵심 — engine ↔ ckpt 결선 |
| dispatch | autonomous / parallel / bg | @D a_fire_autonomous, ~$2-6 H100 |

## § 5. falsifier (pre-register)

새 corpus 로 fire 시 다음을 사전 등록 — fire 전 고정:

- **F-PHASE-D-1 (register 개선)**: `multilingual_probe` 의
  `anima_register_hits < 4/20` (E2 baseline 4/20 대비 개선) 이고
  `register_regress=False`. ← M3 ≥ 0.3 재설계가 memorize 를 줄였는가.
- **F-PHASE-D-2 (closure)**: 4/5 langs ≥ PARTIAL (AXIS_MAP 결정 트리 / PR #264).
  충족 시 corpus 축 vindicate → V3 REOPENS · AXIS_MAP fallback 보류.
- **F-PHASE-D-3 (M3 게이트 인과)**: § 3 게이트 M3 ≥ 0.3 통과한 corpus 가
  실제로 ko=PURE_MEMORIZE 를 회피 → M3 ↔ register-sink 의 상관 가설을 fire
  로 calibrate (반증 시 M3 단일 예측자 기각, AXIS_MAP B/A/C 로 이행).

## § 6. Honest C3 (≥3)

1. **게이트 = head-sample (prefix-bias)**: `corpus_quality_probe` 의 byte-level
   O(n×distinct) 루프 때문에 1-5 MB head 만 측정. 새 corpus 도 whole-corpus M3
   는 head 와 다를 수 있음 — sampled-stream 측정은 별도. M3 ≥ 0.3 게이트 통과가
   whole-corpus diverse 를 보장하지 않음.
2. **M3 → register-sink 는 단일 corpus·단일 metric 상관**: corpus_s101 1건 +
   M3 단독 매칭에서 도출. 새 corpus 가 M3 ≥ 0.3 이어도 collapse 회피는
   F-PHASE-D-3 fire 전에는 미증명 — 인과 closure 아님.
3. **stream 80% 의 측정 정의 미고정**: "stream/stimulus 80%" 의 record-level
   분류기(무엇이 stream 이고 무엇이 QA 인가)가 build 단계 산물 — 본 spec 은
   비율 목표만 고정, 분류 규칙은 build PR 에서 확정.
4. **fire 미실행 + cost-bearing (~$2-6)**: 본 spec 은 설계·게이트·falsifier 까지
   만 닫는다. E3v3 in-progress 결과가 wiki_frac endpoint 를 보강하나 본 corpus
   재설계 fire 자체는 build 후 별도 autonomous dispatch.

— 끝 —
