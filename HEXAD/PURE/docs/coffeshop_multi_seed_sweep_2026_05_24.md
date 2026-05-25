# COFFESHOP multi-seed robustness sweep (PURE B11)

- **date**: 2026-05-24
- **branch**: `feat/pure-coffeshop-multi-seed-sweep-b11`
- **sweep**: `HEXAD/PURE/bench/coffeshop_sim_seed_sweep.hexa`
- **artifacts**: `state/coffeshop_sim_seed_sweep_2026_05_24/`
  - `sweep_summary.json` (aggregate)
  - `result_seed_<seed>.json` × 10 (per-seed closure_auto_judge input)
  - `judge_seed_<seed>.log` × 10 (per-seed judge stdout/stderr)

## 1. 동기

PR #405 (`feat(COFFESHOP): emergence simulator rewrite — substrate-native fixture 4/4 PASS`)
는 `seed=20260525` 단일 seed 에서 4/4 closure PASS 를 보였다. 한 seed 의 4/4 가
**robust emergence** 인지 **cherry-picked basin** 인지 구분하려면 다중 seed sweep 이 필요하다.

이 문서는 `[20260520..20260529]` 10 개 seed sweep 결과를 정량 정리한다.

## 2. 방법

PR #405 `coffeshop_sim.hexa` 의 시뮬레이터 로직 (LCG / stim 샘플링 /
stim-conditional substrate bias / 8-factor `motivation_score` /
`should_interrupt(>=0.60)` 게이트 / lang assignment / register-hit gate)
을 **verbatim** 으로 sweep wrapper 에 옮겨 담고, seed 만 파라미터화했다.

- 각 seed → 15 window × 6 min tick 시뮬레이션
- per-seed `result.json` 작성 → `closure_auto_judge.hexa` 실행 → exit code 캡쳐
- aggregate: PASS rate, emit 분포, motivation 분포, register hits 합

## 3. per-seed 결과 표

| seed       | emit | silence | ko_emits | en_emits | reg | motivation | v_ko    | exit | judge |
|-----------:|-----:|--------:|---------:|---------:|----:|-----------:|:--------|-----:|:------|
| 20260520   |    6 |       9 |        3 |        3 |   1 |   0.562276 | STRONG  |    0 | PASS  |
| 20260521   |    8 |       7 |        7 |        1 |   0 |   0.552404 | STRONG  |    0 | PASS  |
| 20260522   |    3 |      12 |        2 |        1 |   0 |   0.530912 | STRONG  |    0 | PASS  |
| 20260523   |    8 |       7 |        5 |        3 |   0 |   0.585176 | STRONG  |    0 | PASS  |
| 20260524   |    6 |       9 |        6 |        0 |   1 |   0.525073 | STRONG  |    0 | PASS  |
| **20260525** |  **4** |    **11** |    **3** |    **1** | **0** | **0.525067** | **STRONG** | **0** | **PASS** |
| 20260526   |    6 |       9 |        3 |        3 |   0 |   0.557596 | STRONG  |    0 | PASS  |
| 20260527   |    5 |      10 |        5 |        0 |   0 |   0.548398 | STRONG  |    0 | PASS  |
| 20260528   |    8 |       7 |        4 |        4 |   0 |   0.547577 | STRONG  |    0 | PASS  |
| 20260529   |    8 |       7 |        5 |        3 |   0 |   0.583929 | STRONG  |    0 | PASS  |

(굵게 = PR #405 target seed.)

## 4. aggregate 통계 (N=10)

- **closure PASS rate**: **10 / 10 = 100 %** (exit=0 모두)
- **emit_count**: min=3 · max=8 · **mean=6.2** · range width=5
- **silence_count**: min=7 · max=12 · mean=8.8
- **register_hits**: sum=2 · mean=0.2 (10 seed 중 2 seed 가 단일 hit, 8 seed 0)
- **motivation_score**: min=0.525067 · max=0.585176 · **mean=0.551841** · spread=0.060
- **v_ko**: STRONG × 10 / 10 (모든 seed 가 ko_emits ≥ 2 만족)

### per-criterion PASS 분석

`closure_auto_judge.hexa` 의 4 criterion 각각이 10 seed 어떻게 reach:

| criterion             | threshold                          | per-seed status     | PASS rate |
|----------------------:|:-----------------------------------|:--------------------|----------:|
| 1. multilingual_probe | ≥ 4 / 5 langs ∈ {STRONG, PARTIAL}  | 모든 seed: 5/5      |   10 / 10 |
| 2. register_collapse  | n_register_hits_total < 4          | max observed = 1    |   10 / 10 |
| 3. motivation_8factor | motivation_score ≥ 0.30            | min observed = 0.525 |  10 / 10 |
| 4. dream_stage        | block present + phi ∈ canonical 5  | WAKE/1.0 fixed     |   10 / 10 |

→ **모든 criterion 이 10/10**, 단일 criterion fallout 없음.

## 5. emit_count 분포 (히스토그램)

```
emit_count    seed count
   3          1   (■)
   4          1   (■)
   5          1   (■)
   6          3   (■■■)
   7          0
   8          4   (■■■■)
```

target seed (20260525) 의 emit=4 는 분포 lower-quartile 근처. 분포 전체는
3-8 범위, mean 6.2. 즉 **target seed 는 분포 중심이 아니라 오히려 낮은 쪽**.

## 6. 해석

1. **closure 4/4 PASS 는 robust** — 10/10 seed 가 통과. 좁은 basin 이 아니다.
2. **target seed (20260525) 는 cherry-picked 가 아니다** — emit=4 로 분포의
   lower-quartile 에 위치, "PASS 가 잘 나오는 seed" 로 골라진 것이 아니다.
   오히려 target 보다 emit 이 많은 seed (8 emit × 4 seed) 가 다수.
3. **motivation 분포 폭이 좁다** — 0.060 (0.525-0.585), threshold 0.30
   에서 멀리 떨어진 안전 marginal (1.75-1.95× threshold). 이 marginal 폭은
   `motivation_score` 가 8-factor 평균인 design 때문 — 개별 factor 가 0/1
   극단 으로 가도 평균이 분산을 흡수.
4. **register_hits 가 극히 드물다** — sum=2 across 150 windows
   = 1.3 % rate. `coh < 0.10` gate 가 sub-1 % event 인 substrate 설계
   (gate 0.486-0.514 uniform → coh<0.10 은 outer-1 % edge only) 의 직접 결과.

## 7. Honest C3

1. **10-seed 표본 한계** — `[20260520..20260529]` contiguous range, 전체 LCG
   상태 공간 (2³¹) 의 10⁻⁹. 더 넓은 range (e.g. 100 random seed) sweep 으로
   robustness claim 을 더 strengthen 가능.
2. **seed range 임의성** — target seed 주변 5 days × 2 = 10 day window
   는 author 가 임의 결정. 시계열적 cluster effect 가 LCG 에서 없음을
   가정 (LCG 가 amplifier 라면 보장됨).
3. **100 % PASS rate 의 의미 모호성** — design intent (judge threshold 가
   simulator distribution 을 통과시키게 설정됨) 인지 emergent robustness
   (substrate 분포가 진짜로 PASS region 에 concentrated) 인지 본 sweep
   단독으로 구분 불가. **§4 per-criterion threshold-margin 표가 surface
   data** — motivation 0.525 vs threshold 0.30 = 1.75× margin 은 design
   broadness 신호 (threshold 가 typical substrate output 보다 낮게 설정됨).
4. **simulator state 합성** = i.i.d. uniform + stim bias (PR #405 §7 C3 #1
   carry over). real anima ckpt forward state 와 다름.
5. **PR #405 fixture 미터치** — sweep 은 `state/coffeshop_sim_seed_sweep_2026_05_24/`
   하위 only, PR #405 의 `state/coffeshop_sim_2026_05_24/result.json` 침해 없음.

## 8. 결론

PR #405 COFFESHOP simulator 4/4 closure PASS 는 **target seed 의 cherry-pick
이 아니라 10-seed sweep 에서 100 % robust** 함이 확인됨. 단 100 % rate 자체
는 design (broad threshold) + emergence (substrate concentration) 의 합성
효과로, 본 sweep 만으로는 두 기여 분리 불가 — §4 per-criterion margin 분석
이 design 측 기여가 비-trivial 함을 surface.

**run wall**: ~2 분 (10 seed × ~10 s 시뮬 + ~2 s judge subprocess each)
**cost**: $0 (mac local)
**HEXAD/PURE 의 B11 milestone 달성**.
