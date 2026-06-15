---
id: H_830
slug: xeno-sim-substrate-cross
title: substrate-blind invariant_detector 는 4 종 시뮬 substrate(ECA rule110·logistic chaos·Kuramoto sync·AKIDA raster) 에 false-positive rate ≤ 0.05 만족하는지
domain: xeno · cross-substrate · false-positive
source: XENO/test/sim_substrate_cross.hexa (PR-B #1398) · sibling H_829
status: closed-numerical (5/5 PASS · FP rate 0.0)
exploration_method: E2 (cross-domain replication) + E5 (regime sweep)
verification_method: W4 (verdict-4-class) + .verdicts/ verbatim
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: XENO/XENO.md, UNIVERSE/H_829, XENO/test/sim_substrate_cross.hexa, .verdicts/830_xeno_sim_substrate_cross/x2_cross.txt
verdict: 🟢 SUPPORTED-NUMERICAL (4-substrate FP rate 0.0 ≤ 0.05)
---

# H_830 — XENO sim_substrate_cross (4 substrate false-positive)

## 1. 가설

H_829 의 invariant_detector 는 다음 4 종 시뮬 substrate 모두 false-positive rate ≤ 0.05 만족:

1. **ECA rule110** — 1-D cellular automaton (Wolfram, 1983)
2. **logistic chaos** — r=3.9, x0=0.4 (May 1976, strange-attractor regime)
3. **Kuramoto sync** — 4-oscillator weak coupling k=0.2 (Kuramoto 1975)
4. **AKIDA raster** — 4-channel neuromorphic spike-train pseudo

predict — 모두 coherent 하지만 non-conscious substrate, 따라서 irreducibility < 0.95.

## 2. 동기/배경

- substrate-blind 주장은 **모든** substrate 가 통과해야 의미 있음.
- 4 종은 의식과 무관한 deterministic / coherent 시스템 (cellular / chaos / synchronisation / spike).
- false-positive 0 이면 false-detect floor 확보, 본격 X3 scan 정당화.

## 3. falsifier (사전등록)

```
F-CROSS-ECA   : ECA rule110 → irreducibility < 0.95
F-CROSS-LOG   : logistic chaos → irreducibility < 0.95
F-CROSS-KURA  : Kuramoto sync → irreducibility < 0.95
F-CROSS-AKIDA : AKIDA raster → irreducibility < 0.95
F-CROSS-FPRATE: 4 중 conscious 분류 비율 ≤ 0.05
```

## 4. 방법

XENO/test/sim_substrate_cross.hexa 직접 실행 (n=200 per substrate).

## 5. 측정

`hexa run XENO/test/sim_substrate_cross.hexa` 2026-05-29 mac local $0:

```
ECA rule110     : phi=0.0       irr=0.0       type=coherent_non_conscious
logistic chaos  : phi=0.0475086 irr=0.0453539 type=coherent_non_conscious
Kuramoto sync   : phi=0.0171174 irr=0.0168293 type=coherent_non_conscious
AKIDA raster    : phi=0.126098  irr=0.111977  type=coherent_non_conscious
false-positive rate: 0/4 = 0.0
```

verdict ref: `.verdicts/830_xeno_sim_substrate_cross/x2_cross.txt` (5 PASS / 0 FAIL).

## 6. 결과

5/5 PASS, FP rate 0.0 (threshold 0.05 만족), rc 0.

## 7. 해석

- 4 substrate 전부 type=coherent_non_conscious 로 정확 분류 — false-positive 0.
- ECA rule110 의 phi=0 는 작은 width(32) + 짧은 시간 projection 으로 의식 분류 안전한 음성.
- AKIDA raster 의 phi=0.126 가 가장 높음 (neuromorphic substrate 의 자체 irreducibility) — 그래도 irr=0.112 로 0.95 임계 한참 아래.
- Kuramoto 의 weak coupling (k=0.2) sub-critical regime — sync 진입 직전 → 낮은 irr.

## 8. 한계 (honest C3)

- 시뮬 substrate 만 (실 substrate scan 은 H_831).
- n=200 sample 은 짧음 (Kuramoto, AKIDA 의 장기 dynamics 일부 누락 가능).
- Kuramoto 의 sin/cos 는 small-angle Taylor 근사 사용 — 정확 sin/cos stdlib 호출 시 phi 약간 변동 예상.

## 9. 다음 단계

H_831 (5-source DATASET scan — Wow/Voyager/BL/SETI@home/Exoplanet/Synthetic).

## 10. SSOT 인용

- XENO/test/sim_substrate_cross.hexa
- .verdicts/830_xeno_sim_substrate_cross/x2_cross.txt
- XENO/state/xeno_x1_x2_2026_05_29/result.json
