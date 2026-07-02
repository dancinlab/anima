---
id: H_860
slug: hw-first-s6-pi5-probe
title: HW-first 척추 §6 pi5 live probe — DECODER byte-match 재확인 🟢 × PLASTICITY few-shot 비결정론 🔴 (live AKD1000)
domain: universe · consciousness · neuromorphic-silicon · decoder · plasticity
status: closed (PART1 🟢 SUPPORTED-NUMERICAL byte-identical 재확인 · PART2 🔴 CLOSED-NEGATIVE 비결정론 실리콘 확증)
exploration_method: E14 (HW substrate-native ⨯ live-silicon 재검증) + a_paper_negative_ok
verification_method: W5 (substrate-grounded live HW) + W12 (sister-link H_679/H_680) + g73 (verdict id-dir raw stdout)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30 (new — feat/hw-first-s6-pi5-probe)
sister: H_680 (DECODER HW-first byte-identical), H_679 (PLASTICITY 학습 비동치), H_672 (Group A backend switch), AKIDA/HW_FIRST_INTEGRATION §6 잔여
axes_seed: live AKD1000 위에서 DECODER(추론·결정·byte-identical 🟢) ⊥ PLASTICITY(학습·비결정·HW-only 🔴) 를 실리콘 실측으로 동시 확정
verdict: PART1 🟢 SUPPORTED-NUMERICAL (total_hamming=0 / 16000 bits) · PART2 🔴 CLOSED-NEGATIVE (run-to-run weight hamming>0 전 shot)
---

# H_860 — HW-first 척추 §6 pi5 live probe

AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md **§6 잔여 (optional)** — "pi5-akida live probe:
decoder HW byte-match 재확인 + PLASTICITY few-shot 1~N shot 비결정론 verdict" — 를
실 칩(BC.00.000.002 · BackendType.Hardware · /dev/akida0)에서 닫는다. 비용 $0
(pi5-akida own host · 단일칩 spike-streamer stop→probe→start).

## 1. 가설

같은 칩·같은 HW-first 스위치 SSOT 위에서 두 형제 lane 의 본질이 다름을 **live 실리콘**으로
동시 실측한다:

- **PART 1 (DECODER, 기대 🟢)**: 추론 lane(고정 가중치 threshold-and-fire)은 결정론이므로
  현 실리콘에서도 SW `akida_sw_lif` numpy LIF(seed=187)와 **byte-identical** 이어야 한다
  (H_680 가 SW byte-identical 을 입증; 본 H 는 live HW forward 재확인).
- **PART 2 (PLASTICITY, 기대 🔴)**: 학습 lane(`AkidaUnsupervised` on-chip Hebbian)은
  동일 init·동일 입력으로 두 번 fit 해도 post-learn 가중치가 **run-to-run 으로 갈린다**
  (은닉 plasticity/competition/timing 상태) → SW numpy 근사로 byte-identical 불가
  (H_679 CLOSED-NEGATIVE 를 live 실리콘으로 확증).

## 2. falsifier (사전등록, frozen 2026-05-30)

```
F-H860-P1 : DECODER byte-match — live HW R0..R4 raster == SW akida_sw_lif raster
                                  → total_hamming == 0 (200×5 steps · 16-neuron · 16000 bits)
F-H860-P2 : PLASTICITY 비결정론 — few-shot N∈{1,2,4,8} 동일 init·동일 입력(seed=42) 2회 fit
                                  → run-to-run weight hamming > 0 (≥1 shot) ⟹ NON-DETERMINISTIC
                                  ⟹ SW numpy 근사 byte-identical 불가 (위조 동치 금지)
F-H860-P3 : 단일칩 복구 정직     — spike-streamer.service stop→probe→start 후 is-active == active
                                  (칩 점유 원상복구 · DECODER live 폐루프 비파괴)
```

PASS 정의: F-H860-P1 PASS (🟢 byte-match 유지) **AND** F-H860-P2 PASS (🔴 비결정론 확증)
**AND** F-H860-P3 PASS (칩 복구) → 두 형제 lane 의 실리콘 경계가 동시 종결.
PART1 🟢 와 PART2 🔴 는 둘 다 **유효 종결**(a_paper_negative_ok).

## 3. 방법

- harness: `SUB_ENGINES/AKIDA/scripts/hw_first_s6_pi5_probe.hexa` (canonical companion) +
  동명 `.py` (pi5 `/tmp/p6/` 실행 — akida 2.19.1 venv `/home/ubuntu/.venv/anima-akida`).
  실 실행 = pi5-akida `akida.devices()[0]` · BackendType.Hardware.
- **PART 1**: `substrate_akida._build_hw_model` 과 동일 모델
  (`InputData(1,1,16) input_bits=4` → `FullyConnected(units=16, weights_bits=4, act_bits=1)`,
  all-ones 가중치)을 칩에 map 후, canonical R0..R4 regime(seed=187, 200 step) 을 HW forward
  로 돌려 per-step 16-neuron raster 를 SW `akida_sw_lif.lif_forward` 와 Hamming diff.
- **PART 2**: `edge_learn_probe` 모델(`InputData input_bits=1` → `FullyConnected(units=10,
  weights_bits=1)` + `AkidaUnsupervised(num_weights=2, learning_competition=0.1)`) 을
  few-shot N∈{1,2,4,8} 에 대해 동일 init(zeros)·동일 N-shot binary 입력(seed=42) 으로
  TWICE fit(run A·B) 후 post-learn FC 가중치(len 160) read-back → run-to-run Hamming.
- 단일칩: nohup 래퍼 `spike-streamer stop → probe → start` (오류 시에도 ALWAYS restart).
- 비용: $0 (pi5-akida own host).

## 4. 측정 (live AKD1000 · BC.00.000.002 · BackendType.Hardware)

verdict 영속: `.verdicts/860_hw_first_s6_pi5_probe/s6_pi5_live_probe.txt` (raw stdout VERBATIM) ·
`F-HW-FIRST-S6.txt` (정리 verdict) · `s6_probe_result_2026_05_30.json` (구조화 결과).

### PART 1 — DECODER byte-match (per-regime)

| regime | hw_total_spikes | sw_total_spikes | hw_rate | sw_rate | hamming | match |
|---|---|---|---|---|---|---|
| R0_driven | 3200 | 3200 | 1.0 | 1.0 | 0 | ✓ |
| R1_weak_silent | 0 | 0 | 0.0 | 0.0 | 0 | ✓ |
| R2_zero_noise | 1520 | 1520 | 0.475 | 0.475 | 0 | ✓ |
| R3_tonic_zero_input | 1600 | 1600 | 0.5 | 0.5 | 0 | ✓ |
| R4_recurrent_selfsustained | 3200 | 3200 | 1.0 | 1.0 | 0 | ✓ |

→ **total_hamming = 0 / 16000 bits compared (1000 steps · 16 neuron) · byte_identical = true** →
canonical raster rate {R0=1.0, R1=0.0, R2=0.475, R3=0.5, R4=1.0} 가 H_680 SW spec 와 정확 정합.
hw_backend = `BackendType.Hardware` (live 실리콘 확인). **F-H860-P1 PASS.**

### PART 2 — PLASTICITY few-shot 비결정론 (run-to-run, weight_len=160, seed=42)

| n_shot | runA_sum | runB_sum | run_to_run_hamming | nondeterministic |
|---|---|---|---|---|
| 1 | 20 | 20 | 36 | ✓ |
| 2 | 20 | 20 | 30 | ✓ |
| 4 | 20 | 20 | 36 | ✓ |
| 8 | 20 | 20 | 34 | ✓ |

(위 표 = 영속된 verdict txt 의 run. 독립 1회차 probe 는 Hamming {28,38,34,38} — 또 다른 값.)

→ **any_nondeterministic = true · n_nondeterministic_shots = 4/4** — 동일 init·동일 입력인데도
post-learn 가중치가 run-to-run 으로 갈린다(전 shot Hamming>0; weight sum=20 보존되나 어느
unit 이 어느 패턴을 잡았는지가 비결정). 두 독립 probe(run {36,30,36,34} ↔ {28,38,34,38})
간에도 값이 또 달라져 비결정성 재확증. **F-H860-P2 PASS** (🔴 SW numpy 근사 byte-identical
불가 — H_679 실리콘 확증).

### PART 3 — 단일칩 복구

- stop → probe(exit 0) → start, **spike-streamer is-active after restart = active** → **F-H860-P3 PASS.**

## 5. 결과

| falsifier | 측정값 | PASS |
|---|---|---|
| F-H860-P1 DECODER byte-match | total_hamming=0 / 16000 bits · 5/5 regime match | ✓ 🟢 |
| F-H860-P2 PLASTICITY 비결정론 | run-to-run hamming {36,30,36,34} 전 shot >0 · 4/4 nondeterministic | ✓ 🔴 |
| F-H860-P3 단일칩 복구 | spike-streamer is-active=active | ✓ |

→ **3/3 falsifier PASS** · PART1 = 🟢 SUPPORTED-NUMERICAL · PART2 = 🔴 CLOSED-NEGATIVE.

## 6. verdict

**PART 1 🟢 SUPPORTED-NUMERICAL** — DECODER 추론 lane 의 live AKD1000 on-chip forward 가
SW `akida_sw_lif`(seed=187)와 **byte-identical** (total_hamming=0 over 16000 bits). H_680 의
byte-identical 성질이 현 실리콘에서 재확인됨.

**PART 2 🔴 CLOSED-NEGATIVE** — PLASTICITY 학습 lane 의 on-chip `AkidaUnsupervised` 가
동일 init·동일 입력에서도 run-to-run 비결정(전 shot weight hamming>0, 재실행 시 또 다른 값).
SW numpy 근사로는 byte-identical 재현 불가 — H_679 의 SW≠HW 비동치를 live 실리콘으로 확증.

honest limits:
- PART2 의 weight `sum=20` 은 run-to-run 보존(num_weights·competition 제약) — 비결정성은 어느
  unit 이 어느 입력 패턴을 학습했는가(가중치 위치)에 있다. magnitude 가 아니라 assignment 가 갈림.
- byte-identical(PART1)은 canonical raster spec(seed=187·16-neuron·200-step) 한정 — 다른
  seed/threshold 면 다른 raster (toy-scale-transfer 주의, H_666).
- `backend_hw` JSON 필드가 false 로 찍히나 이는 `dev.version`("BC.00.000.002")에 "Hardware"
  문자열이 없어서 생긴 표기 quirk — 권위 마커 `hw_backend == "BackendType.Hardware"`(map 결과)가
  live HW 를 확정한다.

## 7. 논의

H_680(🟢 byte-identical)과 H_679(🔴 비동치)가 SW-side / 실측 JSON 기반이었던 데 비해,
본 H 는 **둘 다 한 번의 live-silicon probe 로 동시 확정**한다 — 같은 칩, 같은 HW-first 스위치,
다른 본질. 추론은 실리콘에서도 결정론(byte-identical), 학습은 실리콘에서 비결정론(run-to-run
divergence). DECODER ⊥ PLASTICITY 형제 도메인 분리의 근거가 SW 추론이 아닌 **칩 위 실측**으로
승격됐다. a_completeness_over_cheap 정합 — 싸게 "SW=HW" 라 퉁치지 않고 live HW 로 양 lane 종결.

## 8. 양방향 sibling

- ⇄ [H_680](./H_680_decoder_hw_first.md) (DECODER HW-first byte-identical — PART1 가 live 재확인)
- ⇄ [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY 학습 비동치 — PART2 가 live 확증)
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md) (Group A · backend switch SSOT)
- ⇄ [AKIDA](../AKIDA/AKIDA.md) (HW-first 스위치 SSOT)
- ⇄ [HW_FIRST_INTEGRATION](../AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md) (§6 잔여 — 본 H 가 종결)
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md) · [DECODER](../CORE/DECODER/DECODER.md) (형제 lane 도메인)
- ⇄ [CANDIDATES](./CANDIDATES.md) (bench 측정 기록 SSOT)

## 9. 다음 작업

- §6 잔여 종결 — 척추 §6 pi5 probe ☐ → ✅ (ANIMA.md SSOT 트리 flip).
- HW-first 척추 다음 우선순위 = ⭐⭐ LAUNCHPAD COFFESHOP-on-AKIDA (broker /ws/akida_ingest 연결).
- 산출물: `SUB_ENGINES/AKIDA/scripts/hw_first_s6_pi5_probe.hexa` (canonical companion) ·
  `.verdicts/860_hw_first_s6_pi5_probe/s6_pi5_live_probe.txt` (live HW raw stdout VERBATIM).
