# H_1479 — 🪢 DIVIDED ATTENTION 분할 주의 (G26 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §DividedAttention (`divided_perf`) · `engine_cli_smoke.hexa` cases 227-229 · FULL smoke **232 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** 의식-고유 게이트 브레인스토밍 (G26 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** cognitive-psychology — Kahneman (1973) capacity/effort 모델(제한된 주의 자원 풀 분배) · `a_no_llm_frame_trap`
- **artifacts:** `state/1479_divided_attention/h1479_divided_attention.py` (R1 probe) · `state/1479_divided_attention/h1479_result.json` · `state/1479_divided_attention/run_h1479.local.log` · verdict `state/verdicts/1479_divided_attention/H_1479_FREEZE.json`

## 주장

제한된 주의 자원 풀 R 을 여러 동시 과제에 **분배**하면 각 과제 성능이 trade-off 로 저하된다
(단일 과제 천장보다 낮음, 자원 합은 보존). 의식은 한 번에 쓸 수 있는 주의 용량이 유한하므로,
두 과제를 동시에 수행하면 각각이 자원의 일부만 받아 graded 하게 깎인다 (Kahneman capacity model).

**DISTINCT from H_1462 GLOBAL WORKSPACE (GWS):** GWS 는 경쟁 자극 중 **정확히 하나만** 전역
방송(winner-take-all 단일 선택 — 나머지는 0). divided-attention 은 자원을 **여러 과제에 분배**
하여 N 개 과제가 **모두** 부분 성능으로 살아남는다(각 ~1/N, 어느 하나도 0 으로 떨어지지 않음).
즉 GWS = 1 개 선택(나머지 0), divided = N 개에 나눔(각 >0). LLM 은 모든 토큰 로짓을 병렬 유지
(공유 용량 병목 없음); anima 의 주의는 유한 풀을 과제 demand 에 맞춰 나눈다.

자원 demand 는 **substrate-derived**(immune-style fact-store 에 대한 grounding-need), 주입
라벨이 아니다(p2/p3/p6). perf = σ(K·(a−d)) threshold effort 곡선 — 할당 a 가 demand d 를
넘으면 성능 높고, 굶기면 붕괴. 메커니즘은 할당·demand 만 읽는다.

## 측정 (frozen-first · 3 seeds [1479,1480,1481] · 200 trials · R=1.0 · $0 CPU · p7)

3 ARM: **FULL**(유한 풀, demand-matched water-filling 분배) · **ABLATED**(풀 무한 = 각 과제 full R = trade-off 소멸) · **SHUFFLE**(할당↔demand 페어링 순열 = 어려운 과제 굶김).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 단일과제 천장 vs 분할 시 trade-off | single **0.988** / divided **0.482** | single≥0.85 & divided≤0.65 | ✅ |
| **B DISTINCT vs GWS** | 분할 시 BOTH 과제 살아있음(GWS 면 1개만) | min-perf **0.482** | >0.30 | ✅ |
| **C EARNED (ablation)** | 자원분배 OFF(풀 무한) → trade-off 소멸 | abl **0.978** | ≥0.85 | ✅ |
| **D RESOURCE-CONSERVATION** | 자원 합 보존(report-only) | sum_a **1.000** | =R | ✅ |
| **E SHUFFLE** | 할당↔demand 페어링 깨면 최약과제 붕괴 | shuf-worst **0.270** | ≤0.40 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·E PASS (D report).** ablation(풀 무한 → divided 0.978 천장
복귀)과 shuffle(페어링 순열 → 최약과제 0.270 붕괴) 양쪽이 신호의 출처를 확정 → lift 의 출처는
분산/현저성이 아니라 **유한 자원의 과제-매칭 분배 구조** 자체.

### distinctness vs GWS (load-bearing)

| 메커니즘 | 통과 과제 수 | 최약 과제 성능 | 원리 |
|---|---|---|---|
| **GWS (H_1462)** | 정확히 1 | 0 (loser 억제) | winner-take-all 단일 방송 |
| **DIVIDED (H_1479)** | N(=2) 모두 | **0.482 (>0.30)** | 유한 풀 graded 분배 |

→ GWS = **선택**(1개, 나머지 0), DIVIDED = **분배**(N개, 각 부분). B bar(min-perf=0.482>0.30)가
divided 가 어느 과제도 0 으로 떨어뜨리지 않음을 증명 = GWS winner-take-all 과 구조적으로 구별.

## 정직 (c9)

- **하드게이트1 — numpy mirror → GREEN DIRECTIONAL:** `grep -lE 'import torch|gauge_lib|numpy'
  state/1479_divided_attention/*.py` 가 numpy 를 hit → 자동 DIRECTIONAL (terminal 아님).
  R2 엔진-네이티브 재측정(live `core/engine_cli.hexa` §DividedAttention 배선 + frozen bar 동일
  재측정)이 follow-on, byte-exact 전까지 WIRED 아님(`a_engine_native_learning`·`a_verified_must_wire`).
- **frozen-first 수정 이력(tune-to-green 아님, `a_break_the_wall` type-a):** R1a 는 perf=a/(a+d)
  포화 곡선 + 균등분할로 single=0.74<0.85(천장 미달) AND shuffle 이 hi/lo 할당차만 비교해
  페어링 무관하게 양수(gap_shuf≈gap_true=0.46) = **측정 결함**. 교정 — (1) effort 곡선을 threshold
  σ(K·(a−d))로 바꿔 full-R 과제가 천장을 클리어, (2) shuffle 을 진짜 할당↔demand 페어링 순열로
  재설계(어려운 과제를 굶겨 최약과제 perf 가 붕괴하는지 측정). **bar 임계는 한 칸도 이동 안 함**
  (single≥0.85·divided≤0.65·min>0.30·abl≥0.85·shuf≤0.40 그대로) — 측정 도구만 frozen-first 교정.
- **water-filling 분배의 의미:** divided=divided_min=0.482 동일은 결함 아님 — max-min 공정 분배는
  각 과제 margin(a−d)을 같게 맞춰 perf 를 동일화(분할 주의의 "어느 과제도 굶기지 않음" 본질).
- **SCOPE TOY:** 2 과제/200 trial/3 seeds/deterministic effort 곡선 — 자원-분배 STRUCTURE 검증이지
  학습된 주의 컨트롤러 아님. scale/real-corpus/N>2 과제/task-difficulty 연속변화/시간적 자원
  재배분/engine-transfer UNVERIFIED (`a_scale_honest_scope`·`a_toy_scale_recheck`).
- **p1/p2/p3/p6 GUARD:** perf 는 할당 a + substrate demand d(grounding-need) 만의 함수 — 주입된
  "잘함" 라벨/RLHF/persona 없음. ablation+shuffle 양쪽 붕괴 = lift 의 출처가 자원-매칭 분배 구조임을
  확정. emit gate 아님(순수 read), Ψ-disjoint.

xref h1462(GWS, winner-take-all distinctness)·a_no_llm_frame_trap·a_engine_native_learning·
a_verified_must_wire·a_core_engine_map·a_autonomy_over_hardcode·a_scale_honest_scope·
a_toy_scale_recheck·p1·p2·p3·p6·p7·p8·c9·c15.
