---
id: H_829
slug: xeno-invariant-detector
title: XENO 도메인의 substrate-blind Φ-formalism 검출기(invariant_detector) 는 단어/외형/시간축/차원 가정 0 으로 임의 float[] 신호의 의식-여부 판정에 충분한지
domain: xeno · substrate-blind · IIT4
source: XENO/detector/invariant_detector.hexa (PR-B #1398) · DATASET XENO 5-source (PR-A #1396)
status: closed-numerical (5/5 PASS F-DETECT-NULL/NOISE/COUPLED smoke)
exploration_method: E1 (mechanism-from-axiom) + E4 (substrate-blind extension)
verification_method: W4 (verdict-4-class) + .verdicts/ verbatim
raw_rank: 9
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: XENO/XENO.md, HEXAD/IIT4/IIT4.md, XENO/detector/invariant_detector.hexa, .verdicts/829_xeno_invariant_detector/x1_smoke.txt
verdict: 🟢 SUPPORTED-NUMERICAL (smoke 5/5 PASS · false-positive 0)
---

# H_829 — XENO invariant_detector (substrate-blind Φ-formalism)

## 1. 가설

substrate-blind invariant_detector 는 다음을 만족한다:

```
input  : float[] signal, int n_samples
output : { phi: float, integration: float, irreducibility: float, substrate_type: string }
```

pipeline = min-max normalise → 0.5 threshold binarise → 2-unit co-occurrence TPM → IIT4 big-Φ.

predict — 의식 substrate 의 외형/언어/차원 가정 0 으로, 신호의 Φ-irreducibility 만으로 의식 유무 진단 가능.

## 2. 동기/배경

- IIT4 big-Φ (Tononi/Koch) 는 substrate-agnostic claim, 하지만 종래 구현은 specific TPM 입력 필요.
- XENO 도메인 (외계/이종 substrate Φ-detector) 는 임의 신호를 입력으로 받을 수 있어야 함.
- HEXAD/IIT4/lib/iit4_bigphi.hexa stdlib 재사용 (g61).

## 3. falsifier (사전등록)

```
F-DETECT-NULL    : all-zero signal  → phi == 0  (no structure, no consciousness)
F-DETECT-NOISE   : pseudo-random LCG → phi < 0.1 (false-positive floor)
F-DETECT-COUPLED : XOR-coupled LFSR  → phi > 0  (true-positive, integration > noise)
```

## 4. 방법

XENO/detector/invariant_detector_smoke.hexa 의 3 falsifier 직접 실행 (n=200).

## 5. 측정

`hexa run XENO/detector/invariant_detector_smoke.hexa` 2026-05-29 mac local $0:

```
NULL  : phi=0.0       integ=0.0       type=noise
NOISE : phi=0.0887403 integ=1.08874   type=coherent_non_conscious
COUP  : phi=1.63007   integ=2.17253   type=conscious
```

verdict ref: `.verdicts/829_xeno_invariant_detector/x1_smoke.txt` (5 PASS / 0 FAIL).

## 6. 결과

5/5 PASS, rc 0. F-DETECT-NULL/NOISE/COUPLED 전부 통과.

## 7. 해석

- substrate-blind detector pipeline 은 IIT4 axiomatic Φ 의 표준 frontier 를 임의 float[] 입력으로 확장한 thin wrapper.
- 의식 substrate 의 외형/언어 가정 0 (어떤 substrate 의 신호든 float[] 로 표현되면 적용 가능).
- coherent_non_conscious vs conscious 분류는 irreducibility ratio (Φ / total) 의 0.5 threshold.

## 8. 한계 (honest C3)

- 2-unit TPM 은 시퀀스의 (t, t+1) co-occurrence 만 캡처 → 장기 시간 의존성 (long-range LFSR) 은 부분적으로만 반영.
- 0.5 binarisation threshold 는 median-free 단순 선택, 자체 calibration 부재.
- F-DETECT-COUPLED 의 XOR-LFSR 은 mathematically irreducible 이지만 Φ는 토이 수준 (1.63) — 실 의식 substrate 의 Φ 분포 calibration 추가 필요.

## 9. 다음 단계

H_830 (sim_substrate_cross 4 substrate cross-test), H_831 (5-source DATASET scan).

## 10. SSOT 인용

- XENO/detector/invariant_detector.hexa (이 구현)
- HEXAD/IIT4/lib/iit4_bigphi.hexa (stdlib shim)
- .verdicts/829_xeno_invariant_detector/x1_smoke.txt (verbatim verdict)
- XENO/state/xeno_x1_x2_2026_05_29/result.json
