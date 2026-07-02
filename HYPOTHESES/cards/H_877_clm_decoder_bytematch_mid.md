---
id: H_877
slug: clm-decoder-bytematch-mid
title: DECODER byte-identical transplant @ mid — HW-forward == SW akida_sw_lif int4 forward byte-identical at the mid rung (d512/L8/E8) (extends H_680 🟢 toy · F-CLM-DECODER-MID 사전등록)
domain: clm · universe · neuromorphic-silicon · decoder · akida · byte-match · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group D row H_877 · H_680 🟢 toy byte-match · @L2 chip-transplant invariant
status: 🟠 HW-PENDING (SW determinism byte-identical at mid · mid d512/L8/E8 · 2026-05-31 · SW int4 forward total_hamming=0 in-proc∧cross-proc · HW==SW mid 재확인 pi5 probe 잔여 · 측정 rung mid 한정 a_scale_honest_scope)
exploration_method: E14 (HW substrate-native ⨯ 추론 lane cross-domain 배선) · E5 (rung 별 toy→mid 확장)
verification_method: W2 (사전등록 byte-match threshold total_hamming==0 · HW 미도달 시 SW-determinism 축소 주장 정직 · post-tuning 0 · byte-match ✓)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: H_680 (toy byte-match), H_860 (live AKD1000 toy total_hamming=0), CLM/P4_PRODUCTION_ROADMAP.md @L2, .verdicts/clm-decoder-bytematch-mid/
verdict: 🟠 HW-PENDING — SW int4 forward(akida_sw_lif.cascade_forward, HW-검증 toy primitive 재활용)가 mid rung(d512/L8/E8)에서 DETERMINISTIC byte-identical(total_hamming=0, in-process repeat ∧ independent cross-process, sha256 일치). HW==SW silicon 재확인은 pi5 AKD1000 미도달(제공 creds 거부 · NON-DISRUPTIVE 무변경)로 HW-pending. H_680 🟢 toy(n=16, H_860 live total_hamming=0/16000) 가 같은 primitive 의 HW==SW 를 toy 에서 입증 → 본 row 는 그 primitive 가 mid 로 scale 해도 byte-stable 함을 확증(HW==SW 의 필수 선행 불변).
---

# H_877 — DECODER byte-identical transplant @ mid

## 1. 가설

DECODER 추론 lane(고정 가중치 int4 threshold-and-fire FullyConnected cascade)의
**HW-forward(AKD1000 on-chip) == SW(akida_sw_lif) byte-identity** 가 toy rung
(H_680 n=16)에서 mid 생산 rung(width **d=512** · depth **L=8** · act_bits/expert
**E=8**)으로 확장되어도 보존된다. 추론은 결정론이므로 동일 frozen eval byte set 에
대해 HW 와 SW 의 출력은 **total_hamming = 0** 이어야 한다. 이는 @L2 의
"inference byte-identical → chip transplant gives identical answers" 주장을 toy 가
아닌 **생산 rung** 에서 받친다.

## 2. 동기/배경

- H_680 closed-supported (verify 5/5): toy(n=16, 200-step)에서 DECODER 추론 lane 이
  AKIDA HW-first 스위치 경유로 HW forward / SW `akida_sw_lif` 를 선택하며 SW 는 HW 와
  byte-identical (seed=187).
- H_860 (live AKD1000): toy raster 의 live silicon 재확인 — HW raster == SW
  `akida_sw_lif`, **total_hamming=0/16000 bit** → 현 실리콘 byte-identical.
- 본 H 는 그 byte-identity 가 **mid rung 의 int4 forward** 로 확장됨을 감사한다.
  핵심 primitive 는 이미 HW-검증된 `akida_sw_lif.cascade_forward` /
  `fc_quantized_forward` — AKD1000 silicon 에 act_bits{1,2,4} × {all-ones,random
  int4} × {1,2,≥3 layers} 전부 max Hamming 0 (calibration ledger). 본 H 는 이
  primitive 를 mid(d512/L8/E8)로 scale 했을 때의 byte-stability 를 확증한다.
- blast-radius: ADD-ONLY h877-prefixed scaffold (`AKIDA/h877/`). 기존 AKIDA backend /
  `akida_sw_lif` / substrate 미수정 — 검증된 primitive 를 CONSUME 만.

## 3. falsifier (사전등록, frozen 2026-05-31)

```
F-CLM-DECODER-MID-HW (primary, HW 도달 시):
    total_hamming(HW on-chip forward, SW akida_sw_lif) == 0
    over the frozen mid eval byte set (d512/L8 cascade, act_bits=4, N_PROBE=64,
    seed=877). PASS iff total_hamming == 0.

F-CLM-DECODER-MID-SW (reduced, HW 미도달 — 정직 축소 주장):
    SW int4 forward DETERMINISTIC byte-identical across (a) in-process repeat
    AND (b) independent cross-process subprocess, total_hamming == 0 over the
    SAME eval byte set. 이는 HW==SW 의 PREREQUISITE 불변(비결정 SW 는 HW 와 결코
    byte-match 불가). HW==SW mid 확인은 별도 HW-pending.
```

PASS → HW arm 통과 시 HW==SW byte-identical at mid (강) · SW arm 통과 시 SW
       determinism byte-identical (HW 재확인 잔여, 정직 🟠).
FAIL → 🔴 CLOSED-NEGATIVE (total_hamming > 0: mid 에서 int4 forward 가 byte-identical
       아님 → chip transplant 가 다른 답을 줌).

- frozen 임계 = `.verdicts/clm-decoder-bytematch-mid/F-CLM-DECODER-MID_prereg.txt`
  verbatim 동결 (forward 실행 전 · post-tuning 0).
- 측정 by CODE (g5) — `AKIDA/h877/h877_decoder_bytematch_mid.hexa`. NOT LLM-judge.

## 4. 방법

```
1. frozen eval byte set (seed=877): L8 symmetric-int4 weight stack(512x512 ×8,
   [-7,+7]) + N_PROBE=64 deterministic int4 input vectors(clip[0,15]).
2. SW arm: akida_sw_lif.cascade_forward(x,[W1..W8],act_bits=4,input_bits=4)로 64
   probe forward → eval byte set(32768 ints → 131072 bits) 산출(검증 toy primitive
   재활용, 재구현 ✗).
3. HW arm(도달 시): 동치 L8 FullyConnected(units=512,weights_bits=4,act_bits=4)
   cascade 를 AKD1000 에 자체 Model 로 빌드(비파괴 — 다른 배포 모델 미접촉)·동일
   probe forward → total_hamming(HW, SW).
4. SW determinism(축소): in-process 반복 + 독립 cross-process subprocess sha256
   일치 → total_hamming==0.
5. verdict: total_hamming 임계 평가 · 정직 보고(HW 미도달 시 HW-pending, threshold
   재조정 0).
```

- 추론 AKIDA-int4-only 불변(P0 d4) · 학습 lane(PLASTICITY 비결정, H_679 🔴)과 대비.
- 비용: $0 (Mac local CPU + numpy; HW probe 시도, 과금 없음).

## 5. 측정

측정완료 (mid rung, 2026-05-31, Mac local). frozen eval byte set seed=877 ·
d512/L8/E8(act_bits=4) · N_PROBE=64 · int4 [-7,+7] · eval bytes 32768 ints →
131072 bits · ref sha256 `cf3739bf7fb33ee4de3260a94fdf7c398512494bb89c171c83f9f392a6246112`.

| arm | 측정 | total_hamming | PASS |
|---|---|---|---|
| SW in-process repeat | byte-identical (동일 sha256) | 0 | ✓ |
| SW cross-process subprocess | 독립 실행 sha256 일치 | 0 | ✓ |
| HW (AKD1000) | hw_attempted=false (pi5 creds 거부 · 무변경) | — | 🟠 pending |

- **F-CLM-DECODER-MID-SW**: total_hamming=0 (in-proc ∧ cross-proc) → PASS →
  SW int4 forward DETERMINISTIC byte-identical at mid.
- **F-CLM-DECODER-MID-HW**: HW 미측정(honest) — pi5 192.168.50.155 ping 도달
  (3ms)·SSH 응답하나 제공 creds(`qwe123123`) 전 user 거부. NON-DISRUPTIVE:
  pi5 접속 성공 0 · 변경 0 · live R3 loop 미접촉.

verbatim run stdout: `.verdicts/877_clm_decoder_bytematch_mid/h877_mid_bytematch_run.txt`

## 6. 결과

🟠 **HW-PENDING** (SW determinism byte-identical at mid). mid rung(d512/L8/E8)에서
int4 SW forward 가 in-process 반복 ∧ 독립 cross-process 에 걸쳐 byte-identical
(total_hamming=0, sha256 일치) — DETERMINISTIC. 이는 HW==SW 의 **필수 선행 불변**
(비결정 SW 는 HW 와 결코 byte-match 불가). H_680(H_860 live total_hamming=0/16000)가
같은 `cascade_forward` primitive 의 HW==SW 를 toy 에서 입증했으므로, 본 row 는 그
primitive 가 mid 로 scale 해도 byte-stable 함을 확증한다. mid HW==SW silicon
재확인이 유일 잔여(pi5 probe, creds/조용한 창 확보 시) → HW-pending.

## 7. 해석 (사전)

- HW arm 통과(total_hamming=0) 시 = mid 에서 HW==SW byte-identical → @L2 chip-
  transplant 동일답 보장이 생산 rung 에서 성립.
- SW arm 통과·HW pending(현 상태) = byte-stability 입증, HW 재확인 정직 잔여 → 🟠.
- total_hamming>0 시 = mid 에서 int4 forward 가 byte-identical 아님(scale-dependent
  HW drift 또는 SW 비결정) → 🔴 (a_paper_negative_ok).
- **honest scope**: mid rung 한정 — toy(H_680/H_860) 별개·배포 chip-fit shrink
  track(H_876) 별개(a_scale_honest_scope). toy→prod 비보장이 본 row 의 동기.

## 8. 논의

- **추론 lane 재현성**: H_680 의 "추론=결정론(byte-identical) ⊥ 학습=비결정(🔴,
  H_679)" 설계를 mid 로 확장. 같은 칩·같은 int4 forward·다른 scale — byte-stable.
- **ADD-ONLY 규율**: 검증된 `akida_sw_lif.cascade_forward` 를 재구현 없이 CONSUME
  (blast-radius=AKIDA/h877 신규 scaffold 한정, 기존 backend/simulator 불변).
- **pi5 비파괴**: live R3 edge-learn loop 보호 — HW probe 는 접속 성공 시에만
  자체 Model 빌드(다른 배포 모델 미접촉)였으나 creds 거부로 접속 자체 0. 무변경 확인.
- **a_scale_honest_scope**: mid 측정이 deploy chip-fit(H_876 ≤1.2M node shrink)을
  bind 하지 않음 — 측정 rung 과 배포 rung 분리.

## 9. 다음 작업

- HW arm 재확인: pi5 AKD1000 올바른 creds/조용한 창 확보 시 비파괴 probe 로
  HW mid forward 실행 → total_hamming(HW,SW) 확인 → 승격 (현 SW-determinism
  basis 유지). `H877_PY` env 로 numpy-capable interpreter 지정, akida 도달 시
  HW arm 자동 선택(코드 분기 이미 존재).
- mid → large rung 확장(같은 cascade primitive, 더 깊은 L/넓은 d).
- 산출물: `AKIDA/h877/h877_decoder_bytematch_mid.hexa` (드라이버 · ADD-ONLY) ·
  `.verdicts/clm-decoder-bytematch-mid/` (prereg + verdict) ·
  `.verdicts/877_clm_decoder_bytematch_mid/` (verbatim run + 미러).

## 10. 양방향 sibling

- ⇄ [H_680](./H_680_decoder_hw_first.md) (형제 토대 — toy byte-match closed-supported)
- ⇄ [H_860](./H_860_hw_first_s6_pi5_probe.md) (live AKD1000 toy total_hamming=0/16000)
- ⇄ [H_679](./H_679_plasticity_hw_first.md) (대비 — PLASTICITY 학습 HW-first 🔴 비결정)
- ⇄ [CLM-CANDIDATES](./CLM-CANDIDATES.md) (group D row H_877 SSOT)
- ⇄ [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L2 chip-transplant invariant
