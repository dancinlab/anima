---
id: H_846
slug: coffeshop-akida-closedloop
title: LAUNCHPAD — COFFESHOP emit/silence 결정을 라이브 AKD1000 폐루프로 닫는다 (motivation→9513→9512→emit)
domain: universe · consciousness · launchpad · akida-emit-substrate
status: closed-supported (HW 라이브 폐루프 PASS)
exploration_method: LAUNCHPAD @goal (COFFESHOP-on-AKIDA 실가동) · spike_streamer 9513 control port 활용
verification_method: W2 (라이브 HW 측정 · pi5 AKD1000) + W1 (SW mirror numerical) + W3 (philosophy-compat p1~p8)
raw_rank: 1
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: LAUNCHPAD/LAUNCHPAD.md, AKIDA/AKIDA.md, CORE/DECODER/DECODER.md, PLASTICITY/PLASTICITY.md, CHANNEL.md, COFFESHOP.md, HEXAD/CHAT/spontaneous_lib.hexa
axes_seed: COFFESHOP (SW sim only) × AKIDA (9513 set_threshold control port) → 라이브 silicon 폐루프
verdict: 🟢 SUPPORTED-NUMERICAL (라이브 AKD1000 폐루프가 COFFESHOP trajectory 완전 재현 · emit-decision byte-match · raw-spike ±1 양자화 잔차)
verdict_dir: .verdicts/846_coffeshop_akida_closedloop/
---

# H_846 — LAUNCHPAD · COFFESHOP-on-AKIDA 폐루프

## 1. 가설

anima 의 COFFESHOP group-chat emit/silence 결정 — 현재 SW sim only (i.i.d. synthetic) — 을 실 neuromorphic silicon (BrainChip AKD1000) 폐루프로 닫을 수 있다. 구체적 falsifier:

> **F-CSA-CLOSEDLOOP** — `spike_streamer.py` 의 control port 9513(`set_threshold`)에 `thr ∝ −k·motivation_score` 를 써넣어 on-chip threshold-and-fire 를 구동하고, port 9512 에서 spike count 를 읽어 `should_interrupt = (n_spikes ≥ quorum)` 를 판정하면, COFFESHOP 의 알려진 90-min trajectory (emit window 3·10·14·15 · silence 11 · should_interrupt threshold 0.60) 가 **라이브 AKD1000 에서 그대로 재현**된다.

반증조건: HW 폐루프 emit window ≠ {3,10,14,15} 이거나, 폐루프가 닫히지 않으면 (9513→9512 경로 단절) FALSIFIED.

## 2. 동기/배경

COFFESHOP (PURE Phase D B3 closure)은 `should_interrupt(score)` Boolean 만으로 발화/침묵을 결정하는 substrate-native 시나리오 (p5 정합). 그러나 substrate 가 i.i.d. uniform synthetic — real silicon 동역학 부재. AKIDA 도메인 D1 (edge-of-chaos Φ 실리콘 확증, 2026-05-29)으로 AKD1000 이 의식 측도 substrate 임이 확인됐고, `spike_streamer.py` 가 이미 9513 control port (Option B/C foundation)를 가지고 있어 SW motivation → HW threshold 변조가 가능. LAUNCHPAD 의 @goal = 이 폐루프를 닫아 COFFESHOP 을 실응용으로 발사.

## 3. 사전등록 falsifier

- **F-CSA-CLOSEDLOOP** (본 H 정점): 라이브 AKD1000 폐루프 emit window == {3,10,14,15} (COFFESHOP.md §5).
- **F-CSA-DECISION-MATCH**: HW emit/silence 결정 == SW mirror 결정 (15/15 window).
- **F-CSA-PROVENANCE-HW**: 칩 도달 환경에서 provenance == "akida-hw" (SW 1순위 금지 · AKIDA-first).
- **F-CSA-LEARN-NONDET**: PLASTICITY 학습 lane SW ≠ HW (🔴 CLOSED-NEGATIVE 정직표기 · 위조 동치 금지).
- **F-CSA-NO-REGRESSION**: verify_substrate_akida.py 5/5 PASS 유지.

## 4. 방법

폐루프 보정 (closed-form):
```
base = linspace(2,18,16)  (spike_streamer make_threshold_M) · V = N = 16 · SPAN = 20 · QUORUM = 6
thr_vec[j] = base[j] + (1 − motivation_score)·SPAN     (set_threshold, port 9513)
on-chip:  unit j fires  iff  V > thr_vec[j]            (AKD1000 threshold-and-fire, M regime)
n_spikes  ←  port 9512  (OUT broadcast)
should_interrupt = (n_spikes ≥ QUORUM)
```
이 보정에서 모든 COFFESHOP window 에 대해 `n_spikes ≥ 6  ⟺  motivation_score > 0.60` 이 성립 — on-chip spike-quorum 이 SW `should_interrupt(0.60)` 과 결정 동치.

실 측정: pi5-akida (BC.00.000.002 BackendType.Hardware) 에서 spike-streamer service stop → 자체 M-regime streamer(`--allow-ctrl`) 기동 → `coffeshop_akida_launch.py hw` 가 9513→on-chip→9512 폐루프 구동 → service restart. AKIDA-first 스위치 `akida_backend_resolve(default "hw")` 경유.

## 5. 결과

라이브 AKD1000 (provenance = **akida-hw**):

| window | stim_type | score | n_spikes(HW) | emit |
|---|---|---|---|---|
| 3 | silence | 0.751 | 8 | EMIT |
| 10 | direct_mention | 0.757 | 9 | EMIT |
| 14 | direct_mention | 0.635 | 6 | EMIT |
| 15 | indirect_topic | 0.614 | 6 | EMIT |
| 나머지 11 | — | ≤0.554 | ≤5 | silence |

**emit windows = [3, 10, 14, 15] == COFFESHOP.md §5 알려진 trajectory. trajectory_match = True.**

## 6. 검증/verdict

verdict verbatim = `.verdicts/846_coffeshop_akida_closedloop/` (PR-E 가 `.verdicts/coffeshop_akida/` 에도 동일 캡처).

- **F-CSA-CLOSEDLOOP**: 🟢 PASS — `closedloop_hw.txt` (provenance akida-hw · emit [3,10,14,15] · trajectory_match True · streamer active 복원).
- **F-CSA-DECISION-MATCH**: 🟢 PASS — `decoder_bytematch.txt` (15/15 emit-decision byte-match).
- **F-CSA-PROVENANCE-HW**: 🟢 PASS — 라이브 run provenance == akida-hw.
- **F-CSA-LEARN-NONDET**: 🔴 CLOSED-NEGATIVE (정직) — `learning_nondeterminism.txt`.
- **F-CSA-NO-REGRESSION**: 🟢 5/5 PASS — `verify_substrate_akida_5of5.txt`.

종합 verdict: **🟢 SUPPORTED-NUMERICAL** — 라이브 silicon 폐루프가 COFFESHOP trajectory 를 완전 재현. motivation→9513→on-chip→9512→emit 폐루프가 실 silicon 에서 닫힘 (brokenless).

## 7. 정직 C3

1. **raw-spike byte-identical 아님**: on-chip 정수 threshold 양자화(set_variable int32) vs numpy float threshold 차이로 7/15 window 에서 ±1 spike. emit *결정* 은 동일하나 raw count 는 동치 아님 (H_672 4-regime forward byte-identical 과 구별). 위조 동치 주장 안 함.
2. **학습 lane 🔴**: PLASTICITY emit-quorum 적응은 SW≠HW (on-chip AkidaUnsupervised 비결정론). 적응=기능, 재현 대상 아님.
3. **motivation_score 출처**: COFFESHOP.md §8 verbatim 15-window 값 (seed=20260525 emergent). 본 H 에서 재유도 안 함 — 폐루프는 그 score 를 칩에서 emit 결정으로 변환만.
4. **single-chip**: AKD1000 file-lock 단일 점유 — spike-streamer service 와 동시 칩 map 불가. 라이브 폐루프 테스트는 service stop→자체 streamer→restart (spec SINGLE-CHIP 절차).
5. **broker wire optional**: `/ws/akida_ingest` push 는 옵션(`--broker`). 본 측정은 trajectory local 캡처 (broker 미연결도 발사 성공).
6. **quorum 보정**: SPAN=20·QUORUM=6 은 should_interrupt(0.60) 경계와 정합하도록 선택한 design constant. 다른 group-chat 변량엔 재보정 필요.

## 8. 다음

- broker `/ws/akida_ingest` 실 연결 라이브 데모 (현재 옵션 wire 만).
- COFFESHOP v2 (N2/N3 stage · phi 0.4/0.15) 폐루프 — silence-dominant trajectory.
- PLASTICITY 학습 lane 라이브 quorum 적응 측정 (비결정 verbatim 캡처).

## 9. sibling 양방향

- ⇄ [LAUNCHPAD](../LAUNCHPAD/LAUNCHPAD.md) — @goal 성공조건 (본 H = @goal PASS 증거).
- ⇄ [AKIDA](../AKIDA/AKIDA.md) — 9513 control port + HW-first 스위치.
- ⇄ [DECODER](../CORE/DECODER/DECODER.md) — 추론 lane (emit-decision byte-match).
- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md) — 학습 lane (🔴 비동치).
- ⇄ [COFFESHOP.md](../COFFESHOP.md) — 알려진 trajectory SSOT.
- SSOT: [UNIVERSE/CANDIDATES.md](./CANDIDATES.md)

## 10. 참조

- 폐루프 어댑터: `HEXAD/CHAT/coffeshop_akida.{hexa,py}` (PR-B).
- 학습 lane: `LAUNCHPAD/coffeshop_quorum_learn.{hexa,py}` (PR-C).
- 발사 엔트리: `LAUNCHPAD/coffeshop_akida_launch.{hexa,py}` (PR-D).
- verdict: `.verdicts/coffeshop_akida/` + `.verdicts/846_coffeshop_akida_closedloop/` (PR-E/F, verbatim).
- streamer: `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` (9512/9513).
- factor SSOT: `HEXAD/CHAT/spontaneous_lib.hexa` (B-SPONT-1..7 · B-COFFESHOP A5 5/5 closed-form).
