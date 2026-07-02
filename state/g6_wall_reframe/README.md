# G6 벽 fresh-lens 재분석 — coverage-density + RF (G1 이식)

**날짜:** 2026-07-03 · **수행:** fable (자율, `--write`; 분석+측정+state 착지만, bookkeeping 은 로컬 에이전트)
**표기:** **DIRECTIONAL** (torch-free 코퍼스 통계; engine-native decode 아님) · frozen G6 detector 불변 · tune-to-green 없음

---

## 질문

G1 재조합 벽이 이번 세션에 "trunk-objective TERMINAL" 에서 **데이터-커버리지-밀도 + 수용영역(RF) 이중 bound** 로 재프레임됐다(H_6182~6185). 같은 fresh-lens 를 **G6 반증가능성 벽**(comparator×measurable 를 한 발화에 bind)에 적용 — G6 도 미탐 데이터-측 레버가 있나, 아니면 진짜 attention-capacity 천장인가?

## 방법 (G1 reference-match)

- **검출기 = frozen.** `core/g6_ideation.hexa` 의 `_g6_is_falsifiable` 를 VERBATIM 포트: (a) comparator 25어 (if/than/more/greater/faster/…) ∧ (b) measurable 25어 (rate/level/number/threshold/…) ∧ (c) ≥2 content words, not '?', not pure-stance. 어휘셋 byte-for-byte.
- **코퍼스 = exact HF 4칸** `dancinlab/anima-corpus-{ko,en}-{general,sns}` 127.6MB — G1 prod density(`state/g1_prod_corpus_density`)와 **동일 코퍼스**. `/tmp/hf_exact_corpus` 캐시 사용(무-다운로드).
- **3 렌즈 측정:**
  1. `measure_g6_coverage.py` — generic comparator×measurable 공동출현 밀도 (반증 FORM 이 코퍼스에 얼마나 있나) + comp↔meas **byte-거리 분포**(RF 렌즈).
  2. `measure_g6_targeted.py` — **진짜 G1-analog**: 반증 FORM ∩ ideation-seed 주제어(consciousness·mind·substrate·memory…, `gauge_lib.IDEATION_SEEDS+CONCEPTS` VERBATIM). G1 은 generic 이 아니라 gate 의 TARGET 개념쌍을 쟀으므로.
- ko 칸은 English word-set 이라 ~0 (honest-null); 유효 측정은 en-general(60MB)+en-sns(1.3MB).

## (a) 벽 재분류 (break-walls TAXONOMY)

| 렌즈 | 판정 | 근거 |
|---|---|---|
| **coverage-density (generic form)** | **REFUTED as wall** | 반증 FORM = en 8,794라인 = 3.07% 라인 = **143/MB**. G1 target-pair 밀도 0.118/MB 의 **~1,214배**. G6 는 form-coverage 굶주림 아님. |
| **RF (수용영역)** | **REFUTED as primary** | comp↔meas byte-거리 median 65·mean 114; fals 라인 **2/3 가 clm303 conv RF(~31B) 초과**(within-31B 0.329). 그러나 1/3(~2,900 en라인)은 within-RF = 학습가능 tight 예시 풍부. 게다가 **H_6170 injected full-attention**(RF/capacity 제한 제거)도 depth·register 둘 다 null → RF 는 primary 아님, 기껏 secondary. |
| **targeted-coverage (form ON seed topics)** | **SPARSE like G1, 그러나 UNTESTED engine-native → INCONCLUSIVE** | 반증 FORM ∩ seed-topic = en 1,695라인(fals 의 19%). **그러나 전수 샘플 audit: 다의어 충돌 지배**(engine=차량 "your engine just died"·mind=견해·between=수치범위 "between 170 and 300 g"·meaning=목적). consciousness/substrate 의미의 반증주장은 사실상 **near-zero** — G1 target 희박성과 동형. 이 축만 G6 engine-native 미발사. |

**NET:** **attention-capacity / trunk-objective 천장 SUPPORTED (overturned 아님).** fresh-lens 는 두 저가 축(generic-coverage·RF)을 **벽 아님으로 falsify** 했고, G1 을 구한 유일 축(targeted-coverage)은 G6 에서 sparse 하나 **engine-native 미검** = INCONCLUSIVE residual lever.

## (b) 수치

**G6-coverage (generic 반증 FORM):**
- en-general: 8,693 fals / 279,429 라인 = **3.11%**, 144.76/MB
- en-sns: 101 fals / 6,862 라인 = **1.47%**, 76.16/MB
- ko-general 6 · ko-sns 0 (honest-null, English word-sets)
- **en 합계 8,794 fals · 143.3/MB — G1 pair-density(0.118/MB) 대비 ~1,214×**

**RF: comp↔meas 최근접 byte-거리 (en-general fals 라인, n=8,693):**
- median 65 · mean 114.4 · p90 275 · p99 715 · max 2,129
- within-RF 누적: 9B **0.164** · 31B **0.329** · 61B **0.485** · 128B 0.701 · 256B 0.882 · 511B 0.974
- → clm303 L=4 conv RF(~31B)면 fals 의 67% unlearnable, 하지만 33%(~2,900)는 within-RF. dilated L=8(RF≈511B)면 97% 포섭.

**G6 TARGETED coverage (form ON seed topics, en):**
- fals ∩ topic = 1,695라인(fals 의 19.3%, 27.6/MB) — 그러나 다의어 audit 후 genuine ≈ near-zero.

## (c) verdict

**attention-capacity 천장 SUPPORTED (CONFIRMED-terminal 아님, DIRECTIONAL).**
데이터-레버 발견 = **부분적/negative**: generic form-coverage 와 RF 는 벽 아님으로 falsify(G1 처방이 G6 엔 이미 만족되거나 무관). G1 을 구한 targeted-coverage 축만 sparse 하나 engine-native 미검 → 그 한 축은 **INCONCLUSIVE**, 나머지는 천장 지지.

## (d) 처방 · G1 vs G6 원리적 차이

**왜 데이터-레버가 G1 은 열고 G6 은 (아마) 못 여나:**
- **G1** = 프롬프트에 **CO-PRESENT 한 2개념의 retrieval-composition** ("the ocean and the clock yield ___"). 구제된 이유 = target pair binds 가 (a)코퍼스 부재 ∧ (b)RF 초과 둘 다 → pair 를 within-RF 로 in-corpus 넣으면 작동.
- **G6** = **추상 seed 에 조건부인 3항 GENERATIVE bind**(comparator+measurable+coherent, "a new idea about consciousness: …"). 반증 SCHEMA 는 코퍼스에 풍부(form-half 는 갭 아님) — 빠진 건 그 schema 를 **추상 seed 주제로 instantiate** 한 것 = **cross-domain schema-transfer**, G1 의 in-prompt pair 합성보다 엄격히 어려움. **H_6170 이 RF/capacity 제한을 제거(injected full-attention)했는데도 null** = 병목은 데이터/RF 가 아니라 **transfer** 임을 시사 → 천장 쪽 무게.

**만약 residual lever 를 추적한다면(cost-gated GPU, engine-native):**
G1 의 `L8(RF≈511B)+조합-커버리지 블록` 레시피를 G6 로 이식 — ideation-seed 주제어 × comparator × measurable 를 한 발화 tight(within-RF)로 합성한 코퍼스 블록을 ~20% 임계 밀도 주입 → h1129 warm-FT → engine-native G6 재측정. **pre-register(frozen):** fals ≥ majority on seeds {7,4302,4303}. **사전 예측:** H_6170 injected-attn null 감안, 천장이면 NULL 유지 / 레버면 fals>0. 이 발사 전엔 G6 = 천장 SUPPORTED 유지.

## (e) 산출물

- `measure_g6_coverage.py` · `results.json` — generic 밀도 + RF 거리 분포 (4칸)
- `measure_g6_targeted.py` · `results_targeted.json` — targeted(form ∩ seed-topic) + 다의어 샘플
- `verdict.json` — 구조화 verdict
- 코퍼스는 착지 안 함(`hf download dancinlab/anima-corpus-{ko,en}-{general,sns} --repo-type dataset` 재현)

> ⚠️ bookkeeping(HYPOTHESES/jsonl/카드/CHANGELOG/ARCHITECTURE/commit/PR)은 **미터치** — 로컬 에이전트 소관. 이 폴더는 분석+측정 증거만.
