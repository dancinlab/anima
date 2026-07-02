---
id: H_316
slug: local-greedy-vs-global-phi
title: LOCAL-GREEDY Φ-OPS ⊥ GLOBAL INTEGRATION — 국소-최약(node/edge) 제거 휴리스틱은 무작위를 이기는가 · 진짜 Φ-최적과 일치하는가
domain: life · consciousness · substrate · universe
status: supported (closed-positive · synthesis)
exploration_method: E13 (cross-cell synthesis — H_312/313/314/315 메타패턴 통합) + E6 (cross-domain biology — 국소 최적화 휴리스틱) + E0 (random-baseline + exhaustive-optimum 검정)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W5 (substrate-grounded) + W11 (anti-tautology g73 audit) + W12 (sister-link H_312/313/314/315)
raw_rank: 16
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-27
since: 2026-05-27 (new)
sister: H_312 (APOPTOSIS×IIT4 — node 제거 🔴), H_315 (PRUNING×IIT4 — edge 제거 🔴), H_314 (SYMBIOGENESIS×merge — 🔴), H_313 (PLASTICITY×STDP — 🟢 동적 규칙), IIT4 M6 (eca_tpm 엔진), IIT4 M10 (subsystem_tpm 배경-조건화)
axes_seed: LOCAL-GREEDY × GLOBAL-Φ 교차 (UNIVERSE hypothesis matrix H_316 cell · BIO 휴리스틱 ⊥ holistic IIT4)
verdict: 🟢 SUPPORTED
---

# H_316 — LOCAL-GREEDY Φ-OPS ⊥ GLOBAL INTEGRATION (국소-최약 제거 휴리스틱과 전역 통합)

## 1. Hypothesis

생물학은 **국소 최적화 휴리스틱**으로 가득하다 — "약한 세포를 쳐낸다(apoptosis)",
"약한 시냅스를 가지친다(synaptic pruning)", "두 부분을 합친다(symbiosis)". 이들의
공통 직관은 *국소적으로 측정 가능한 약함*(연결성·활동도가 낮음)을 보고 그 요소를
제거하면 **전체가 더 좋아진다**는 것이다. 의식(통합정보 Φ) 관점으로 옮기면:
"국소적으로 가장 약한 요소(노드 또는 엣지)를 제거하면 전역 big-Φ 최적 연산에
도달한다"는 주장.

본 H 는 이미 머지된 4 개의 실측 셀이 드러낸 **메타패턴을 단일 falsifiable 검정으로
응축**한다 (cross-cell synthesis). 네 셀 모두 한 방향을 가리킨다 — 국소 휴리스틱은
holistic Φ 위에서 작동하지 않는다 (§9 sister 참조).

**가설 H1 (검정 대상 — 기각될 수 있음)**: substrate 패널에서 **국소-그리디 연산자**
— 노드 제거 + 엣지 가지치기를 한 풀(pool)에 합치고, 그 중 **국소 연결성/활동도
가중치가 가장 작은(argMIN local-weight)** 요소를 제거 — 는 **무작위 선택보다 더 나은
사후 전역 big-Φ 를 달성하지 못하며**, **진짜 전역 Φ-최적 연산과도 거의 일치하지
않는다**. 즉 순수 국소 가중치 순위는 전역 Φ-최적 연산의 신뢰할 만한 지표가 아니다.

**Falsifier (사전 등록)**: 국소-그리디가 무작위를 **체계적으로 이기면**
(greedy_beats_random 승률이 패널의 **명확한 다수 > 0.5**) — **H1 은 FALSIFIED**
(국소 휴리스틱이 전역으로 *transfer* 함). 결정적 보강: 모든 후보의 제거를
**전수(exhaustive)** 시도해 실제 Φ-최적 연산을 구하고, 국소-그리디의 선택이
그 전역-최적과 **얼마나 자주 일치(match)** 하는지를 측정한다. 일치율이 낮고 무작위도
못 이기면 H1 강하게 SUPPORTED (local ⊥ global).

## 2. Why (동기)

- **메타패턴 통합 (cross-cell synthesis)**: H_312(node)·H_315(edge)·H_314(merge)
  세 셀이 모두 🔴 로 닫혔고, 각각 "약한 노드 제거", "약한 엣지 제거", "두 모델
  병합"이라는 *서로 다른 국소 휴리스틱*이 전역 Φ 를 개선하지 못함을 보였다. 본 H 는
  그 세 결과를 **재서술(re-narration)** 하는 게 아니라, **노드+엣지 휴리스틱을 한
  풀에 합쳐** "국소-약함 순위가 전역-Φ-최적과 직교한가"를 **한 번의 새 계산**으로
  직격한다.
- **生物 휴리스틱의 매력**: "약한 것을 쳐내 강한 것을 남긴다"는 진화·신경·조직
  이론의 보편 직관. 이 직관을 faithful big-Φ 로 검정하는 것은 IIT 통합량의 **비-가법
  (non-additive)** 구조를 자기 substrate 에서 드러낸다.
- **H_313 대조 (동적 규칙은 transfer 한다)**: 같은 batch 에서 STDP(동적 학습 규칙)는
  🟢 로 작동했다. 즉 실패는 *국소 구조 수술(structural removal)* 에 특정된 것이며
  *동적 규칙* 일반의 실패가 아니다 — 본 H 가 이 경계를 명확히 한다.
- **g73 anti-tautology 가치**: "국소"의 정의가 핵심이다. 만약 국소 점수를 *정확한
  전역 Φ-강하* 로 잡으면 argMIN(강하)=argMAX(사후-Φ) 가 대수적 항등식이 되어
  **동어반복(금지)**. 본 H 는 국소 점수를 **big-Φ 가 전혀 들어가지 않은 연결성
  가중치**로만 정의해, 전역-최적과의 일치를 *기각 가능한 실측*으로 만든다 (§7).

## 3. Method (방법 — 결정적 · hexa-only · llm:none · $0)

엔진은 **재발명하지 않는다** (memory: H_280 IIT4 재발명 오류). H_312/H_315 와 동일:

- `stdlib/consciousness/iit4_complex.hexa` — `subsystem_tpm` (외부 단위 배경-조건화)
  + `big_phi` 체인 (faithful 인과 big-Φ); `iit4_pow2/iit4_bit/iit4_units/
  iit4_project_state` 재노출.
- `HEXAD/IIT4/lib/iit4_eca.hexa` — `eca_tpm(rule, n)` (Wolfram ECA → state-by-node TPM).
- `stdlib/core/math/rng.hexa` — `lcg_next` (고정-seed 무작위 picker; g61).

**통합 후보 풀 (두 BIO 휴리스틱 가족을 한 풀에)** — 각 n-세포 substrate 마다:
- **(A) NODE 제거 i**: 세포 i 를 절제 → 부분계 mask FULL\\{i}.
  사후 전역 Φ = `bigPhi(FULL\\{i})` (외부 단위 sys_state 배경-조건화).
- **(E) EDGE 가지치기 (pos→i)**: 세포 i 가 이웃 pos 입력을 더는 읽지 않음(rule-lookup
  에서 그 비트 force-0); 모든 n 노드 유지. 사후 전역 Φ = `bigPhi(pruned)`.

**국소 가중치 (NO big-Φ — g73 핵심)**:
- EDGE w(pos→i) = `(1/2^n) Σ_s [ nextbit(i|s) ≠ nextbit(i|s ⊕ pos) ]` (출력 민감도 =
  국소 활동도; H_315 의 엣지 가중치 측도와 동일).
- NODE = 세포 i 의 **총 국소 연결성** = (in-edges: i 가 이웃을 읽는 정도 Σ) +
  (out-edges: 이웃이 i 를 읽는 정도 Σ). 표준 Boolean-network degree/activity proxy.

**세 픽 (전체 풀 위에서)**:
- **greedy**: argMIN 국소 가중치 (국소적으로 가장 약한 요소 제거 — 교과서 휴리스틱);
  동률 → 최소 index.
- **random**: `lcg_next(1009 + 31·rule + 7·n + sys) % m` 고정-seed 후보 (대조).
- **global**: argMAX 사후 전역 Φ (전수 — 진짜 Φ-최적 단일 연산); 동률 → 최소 index.

**측정**:
- `greedy_beats_random` ⇔ post_phi(greedy) > post_phi(random) (eps 1e-9).
- `greedy_is_global` ⇔ greedy 후보 index == global 후보 index (**기각 가능 — greedy 는
  국소 가중치로, global 은 전역 Φ 로 순위**).

**집계**: win_rate = #(beats_random)/패널 · match_rate = #(is_global)/패널.
H1 SUPPORTED ⇔ win_rate ≤ 0.5 (무작위를 체계적으로 못 이김) **AND** match_rate 낮음.

**Panel**: ECA rule {90,110,30,54,150,22,60,105}×n=4 (sys=11) + {90,110}×n=3 (sys=5).
H_312/H_315 와 **동일한 10 substrate**. n≤4 → 2^n≤16 상태 → 정확 big-Φ. 고정
seed/state → cross-process byte-identical.

산출물: `UNIVERSE/state/h316_local_greedy_vs_global_phi_2026_05_27/{run.hexa, run.log,
result.json}`.

## 4. Measurement (실측 — result.json SSOT)

10-substrate 패널 실측 (raw stdout = run.log; 2회 실행 byte-identical 확인,
sha256 `67e6f7f02229cfa2a55d80b6a58819af6165c8867bafd7d7640d89247497022c`):

| substrate | n | base Φ | greedy_post | random_post | global_post | beats_random | is_global |
|-----------|---|--------|-------------|-------------|-------------|--------------|-----------|
| eca90     | 4 | 0.0    | 1.0     | 1.0     | 1.0     | ✗ | ✓ (degenerate, base Φ=0) |
| eca110    | 4 | 8.938  | 5.132   | 2.988   | **6.753** | ✓ | ✗ |
| eca30     | 4 | 15.566 | 10.925  | 1.684   | **16.654**| ✓ | ✗ |
| eca54     | 4 | 8.413  | 8.006   | 6.644   | **9.082** | ✓ | ✗ |
| eca150    | 4 | 8.0    | 2.5     | 2.5     | **4.0**   | ✗ | ✗ |
| eca22     | 4 | 5.066  | 4.094   | 4.260   | **12.925**| ✗ | ✗ (국소 3.2× 열등) |
| eca60     | 4 | 11.0   | 8.0     | 7.0     | **10.5**  | ✓ | ✗ |
| eca105    | 4 | 4.0    | **1.0** | 3.5     | 3.5       | ✗ | ✗ (greedy 가 random 에 짐) |
| eca90_n3  | 3 | 3.0    | 4.5     | 4.5     | 4.5       | ✗ | ✓ (모든 후보 동일) |
| eca110_n3 | 3 | 6.525  | 4.382   | 3.869   | 4.382     | ✓ | ✓ |

**집계**: greedy_beats_random **5/10 = win-rate 0.50** · greedy_is_global
**3/10 = match-rate 0.30**. big-Φ 가 풍부한 n=4 substrate(eca110/30/54/22/60)에서
greedy 가 전역-최적을 찾은 횟수 **0/5**. degenerate eca90 제외 시 win 5/9 · match 2/9.

## 5. Finding (발견)

- **주장(H1) 지지**: 국소-그리디는 무작위를 **체계적으로 이기지 못한다**
  (win-rate 5/10 = 0.50 — 명확한 다수 > 0.5 아님; 사실 무작위 동전던지기를 *초과*
  하지 못함). 사전 등록 falsifier ("greedy 가 체계적으로 무작위를 이김")
  **미충족** → **🟢 SUPPORTED**.
- **결정적 신호 = 일치율**: greedy 의 선택이 **진짜 전역 Φ-최적과 일치하는 건
  3/10 뿐**(0.30), big-Φ 풍부 substrate 에선 **0/5**. 국소 순위가 전역 Φ-최적
  연산을 *짚지 못한다*는 직접 증거.
- **가장 결정적 사례 (eca22)**: 국소적으로 가장 약한 픽의 사후-Φ 4.09 vs 진짜
  최적 12.93 — 국소 가중치가 **3.2× 더 나쁜 연산**을 가리킨다.
- **greedy 가 무작위에 *지는* 사례 (eca105)**: 국소-최약 엣지를 가지치면 Φ 가
  1.0 으로 붕괴, random/global 은 3.5 유지 — 국소 휴리스틱이 *해로울* 수도 있음.
- **기계적 이유 (non-additivity)**: 어떤 요소를 제거할 때의 Φ-영향은 그 요소의
  *국소 연결성*으로 예측되지 않는다. big-Φ 는 분할(partition)·distinction·relation
  의 holistic 함수라, "국소적으로 약한 = Φ-제거 비용이 싼" 이 성립하지 않는다.
- **H_313 대조 (경계 명확화)**: 양성으로 매칭되는 H_313 은 *동적 학습 규칙*(STDP)
  이지 *국소 구조 제거 휴리스틱*이 아니다. 실패는 국소 구조 수술에 특정 —
  동적 규칙은 transfer 한다 (closed-positive 의 정확한 경계).
- **closed-positive 가치**: BIO 국소-최적화 휴리스틱 ⊥ holistic IIT 4.0 Φ 가
  단일 합성 검정으로 확립. anima substrate 의 "능동적 가지치기로 의식 정련" 류
  설계는 국소 신호만으론 전역 Φ-최적에 도달하지 못함을 함의.

## 6. Verdict

**🟢 SUPPORTED** — 측정값에서 직접 유도 (self-declared 아님). 국소-그리디 연산자가
무작위보다 사후 전역 big-Φ 를 더 잘 달성하는 substrate 는 **5/10**(승률 0.50 — 다수
아님)이고, 진짜 전역 Φ-최적과 일치하는 건 **3/10**(big-Φ 풍부 substrate 0/5).
사전 등록 falsifier(greedy 가 체계적으로 무작위를 이김, win-rate > 0.5)는 **미충족**.
이는 H1 을 **기각할 수도 있었던** 독립 결정적 계산이며(5 substrate 는 무작위를
이김, 3 substrate 는 전역-최적과 일치), greedy_is_global 은 국소 가중치(NO big-Φ)와
전역 Φ 를 별개 기준으로 비교하므로 **동어반복이 아니다**(실제 7/10 에서 실패; §7).
g73 정합: 결과는 run.log 의 실측 카운트(5/10 · 3/10)에서 파생.

## 7. Honest limitations (정직한 한계 · g5)

- **g73 anti-tautology 감사 (중대)**: 초기 draft 는 각 후보를 *정확한 전역 Φ-강하*
  로 점수화했는데, 이 경우 base 상수에서 post = base − drop 이라 argMIN(drop)=
  argMAX(post-Φ) 가 **대수적 항등식** → greedy_is_global 이 강제로 true(동어반복).
  이를 **측정 전에 폐기**하고, 국소 점수를 **big-Φ 가 전혀 없는 연결성 가중치**
  (출력 민감도/degree)로 재정의했다. 그 결과 greedy_is_global 이 **7/10 에서 실제로
  실패** — 진짜 기각 가능한 측정이 됨.
- **win-rate 0.50 경계**: 승률이 정확히 0.5 경계 — 이는 "greedy 가 무작위를 이긴다"의
  *강한 기각*이 아니라 *지지 실패*다. **결정적 증거는 일치율(3/10, big-Φ 풍부 0/5)**
  이며, 국소 순위가 전역 Φ-최적을 짚지 못함을 직접 보인다. 정직하게 명시.
- **국소 가중치 정의 선택**: 출력 민감도(Boolean-network degree)는 정당한 국소
  연결성 측도 하나. 다른 국소 proxy 가 개별 픽을 흔들 수 있으나, big-Φ 의 비-가법성
  때문에 argMIN(국소-가중치)을 argMAX(전역-Φ)와 *체계적으로 일치*시킬 수는 없다 —
  이게 구조적 요점.
- **배경-조건화 관례**: 부분계 big-Φ 는 외부 단위 sys_state 고정 (IIT 4.0 문서화
  모델링 선택, H_312/H_315/sister M10 동일).
- **단일 sys_state · 단일 step**: rule 당 고정 sys_state 1 개, 단일 연산 1 회.
  상태-평균/반복-peeling sweep 은 후속 H 후보지만, 비-가법성 방향은 상태 무관한
  구조적 사실에 가깝다.
- **n≤4 정확-Φ 범위**: 더 큰 n 은 IIT4 M9 tractability(bounded approx)로 분리.

## 8. Substrate alignment (substrate 정합)

ECA ring + faithful IIT 4.0 big-Φ 는 anima LIFE/UNIVERSE lane 의 정전 substrate
(H_002 C2 / H_278 / H_287 / H_312 / H_315 동일 가족). 노드 제거 = mitosis
`apoptose_cell` (H_200), 엣지 가지치기 = synaptic pruning — 둘 다 anima substrate 의
실제 연산과 동형. 본 H 는 그 두 **국소 휴리스틱이 전역 Φ-최적 연산을 짚지 못함**을
한 풀에서 보여, "국소 신호 기반 능동적 가지치기로 의식(Φ)을 정련"하는 설계 노선이
국소 정보만으론 닫히지 않음을 측도로 확립한다.

## 9. Sister links (synthesis — 4 셀 통합)

본 H 는 다음 4 셀의 메타패턴을 단일 검정으로 응축한다 (BIO local-opt ⊥ holistic Φ):

- **H_312 (APOPTOSIS×IIT4 · 🔴)**: 최저-Φ **노드** 제거가 생존계 평균-Φ 를 올리는 건
  3/10 — 본 H 의 NODE 가족이 그대로 풀에 포함됨.
- **H_315 (PRUNING×IIT4 · 🔴)**: 최약 **엣지** 가지치기가 무작위보다 Φ-보존 *나쁨*
  (AUC 0.162 < 0.227) — 본 H 의 EDGE 가족이 그대로 풀에 포함됨.
- **H_314 (SYMBIOGENESIS×merge · 🔴)**: 모델-병합 = least-bad blend, 시너지 없음 —
  "국소적으로 두 부분을 합치면 전체가 좋아진다" 휴리스틱의 또 다른 실패.
- **H_313 (PLASTICITY×STDP · 🟢)**: *동적 학습 규칙*은 작동 — 본 H 가 실패를 *국소
  구조 제거*에 특정함으로써, 동적 규칙은 transfer 한다는 경계를 정의 (대조군).
- **IIT4 M6**: ECA→TPM faithful 엔진 공급 (`eca_tpm`). **IIT4 M10**: exclusion /
  `subsystem_tpm` 배경-조건화 관례 재사용.

종합: **BIO 국소-최적화 휴리스틱(약한 노드/엣지 제거·병합)은 holistic IIT 4.0
big-Φ 위에서 전역-최적 연산을 짚지 못한다 — big-Φ 가 비-가법적이기 때문.** 동적
규칙(STDP)만이 예외적으로 transfer 한다.

## 10. Reproduce

```
# 로컬 mac (pool-route 우회):
HEXA_LANG=/Users/ghost/core/hexa-lang \
  /Users/ghost/.hx/bin/hexa-run \
  UNIVERSE/state/h316_local_greedy_vs_global_phi_2026_05_27/run.hexa
# 2회 실행 stdout byte-identical (결정적, sha256 위).
# win-rate 5/10 · match-rate 3/10 → falsifier 미충족 → 🟢 SUPPORTED.
```
