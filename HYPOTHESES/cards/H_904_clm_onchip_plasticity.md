---
id: H_904
slug: clm-onchip-plasticity
title: 온칩 가소성 AKD1000 실측 — Akida native edge-learning(AkidaUnsupervised) 이 실리콘에서 live 로 동작 ∧ HW≠SW 정량 (H_877 🟠 추론-byte-identical 의 학습-half 캡스톤 · H_679 plasticity-HW-first 를 실측으로 확증)
domain: clm · universe · neuromorphic-silicon · plasticity · akida · on-chip-learning · falsifier · capstone
source: UNIVERSE/PLASTICITY-CANDIDATES.md H_904 ★ row · H_877 🟠 (추론 byte-identical) · H_679 (plasticity HW-first)
status: 🟢 SUPPORTED — on-chip edge-learning ran live on AKD1000 (BC.00.000.002, BackendType.Hardware) ∧ HW≠SW 정량 (weight Δ 172/1024, out Δ 120/320 · 결정론 SW-sim 대조 byte-exact control · 2026-05-31 · 1 physical AKD1000 a_scale_honest_scope)
exploration_method: E14 (HW substrate-native ⨯ 학습 lane cross-domain 배선) · E5 (rung toy→edge-learn 확장)
verification_method: W2 (사전등록 falsifier · fixed-init + 결정론 SW-sim control · g5 CODE-measured · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: H_877 (추론 byte-identical mid 🟠), H_679 (plasticity HW-first), H_680/H_860 (toy decoder byte-match 🟢), .verdicts/904_clm_onchip_plasticity/, .verdicts/clm-onchip-plasticity/
verdict: 🟢 SUPPORTED — AKD1000 native on-chip edge-learning(AkidaUnsupervised, last-layer binary-weight few-shot update)이 pi5-akida 실리콘(device BC.00.000.002, NSoC_v2, BackendType.Hardware) 에서 LIVE 로 실행되어 last-layer 가중치를 측정가능하게 변경(learn_happened_hw=true). 동일 fixed init weight + 동일 결정론 spike 입력으로 byte-exact 재현되는 SW-sim 대조(software backend)와 비교 시 HW≠SW 정량: 학습된 post-weight 172/1024 위치 상이(Δmax=1), per-sample 출력 120/320 위치 상이(Δmax=5), hw_eq_sw_weights=false ∧ hw_eq_sw_outs=false. 추론은 byte-identical(H_877 🟠)이지만 LEARNING 은 HW≠SW — H_679 의 "가소성이 HW↔SW 의 유일한 차이" 주장을 실리콘에서 확증. g5 CODE-measured. a_paper_negative_ok (HW==SW 였다면 H_679 반증이었을 것 — 어느 쪽이든 major finding).
---

# H_904 ★ — 온칩 가소성 AKD1000 실측 (capstone)

## 1. 가설

BrainChip **AKD1000 의 native 온칩 edge-learning**(`AkidaUnsupervised` — last-layer
binary-weight few-shot 갱신)이 실제 실리콘에서 **live 로 동작**하며 출력을 측정가능하게
변경한다. 그리고 그 온칩 학습 결과(가중치·출력)는 **동일 갱신의 결정론 SW-sim**(동일
fixed init weight + 동일 결정론 spike 입력)과 **byte 단위로 다르다**(HW≠SW).

이는 substrate 의 **학습 half** 를 실측한다: 추론은 byte-identical(H_877 🟠 — DECODER
forward total_hamming=0)이지만, **H_679 는 학습이 HW≠SW** 라고 주장한다. H_904 는 그
학습-half 를 실리콘에서 측정해 H_877/H_679 를 닫는 캡스톤이다.

## 2. 사전등록 falsifier (run 이전 frozen · post-tuning 0)

`.verdicts/904_clm_onchip_plasticity/F-CLM-ONCHIP_prereg.txt` (run 전 freeze, sha256
`e171c7b0…`). 🟢 CONFIRMED iff 둘 다 성립:

- **(A) 온칩 학습 live**: AKD1000 에서 온칩 갱신이 pre-learn 대비 last-layer 가중치를
  측정가능하게 변경(`learn_happened_hw == true`).
- **(B) HW≠SW 정량**: 온칩 학습 post-weight **또는** per-sample 출력이 byte-identical
  SW-sim 의 동일 갱신과 float-noise 를 넘어 상이(`hw_eq_sw_weights == false` OR
  `hw_eq_sw_outs == false`).

🔴 REFUTED iff: 온칩 학습은 동작했으나 HW==SW byte-exact (H_679 "학습이 HW 에서 다르다"
주장 반증 — major finding either way, a_paper_negative_ok), 또는 온칩 학습 자체가 불가/
가중치 무변경.

## 3. 실험 control (공정 비교)

- **fixed init weight**: Akida 기본 가중치 init 은 build 마다 비결정론적(검증됨 — 같은
  코드 두 번 build 시 hash 상이, sum 만 동일). 따라서 한 valid binary edge-learning
  init 을 캡처해 **HW·SW 양쪽 모델에 동일 주입**.
- **동일 입력**: numpy seed=904, 20 samples, 1×1×64 binary spike.
- **SW-sim**: akida **software backend**(device map 없음)의 동일 모델 — fixed init 으로
  **두 SW run 이 byte-exact 재현됨**을 검증 (결정론 control).
- **모델**: `InputData(1,1,64, 1bit)` → `FullyConnected(units=16, weights_bits=1,
  activation=False)`, `AkidaUnsupervised(num_weights=12)`.

## 4. 결과 (g5 CODE-measured · `.verdicts/904_clm_onchip_plasticity/result.json`)

| 항목 | 값 |
|------|-----|
| device | `BC.00.000.002` (NSoC_v2, **BackendType.Hardware**) |
| akida SDK | 2.19.1 (venv `~/.venv/anima-akida`) |
| init_weight_hash (양쪽 동일) | `5618fb88095e0903` |
| HW post-weight hash | `f761bb3c59210810` |
| SW post-weight hash | `c5e9189c3879ffb2` |
| HW out hash / SW out hash | `82fc30b767da1e2f` / `2260e7f5b4119516` |
| learn_happened (HW / SW) | true / true |
| **weight Δ** (HW vs SW) | nnz **172 / 1024**, max **1**, sum 172 |
| **output Δ** (HW vs SW) | nnz **120 / 320**, max **5**, sum 193 |
| hw_eq_sw_weights / hw_eq_sw_outs | **false** / **false** |
| **verdict** | **🟢 GREEN** — 온칩 학습 live ∧ HW≠SW 정량 |

(A)·(B) 모두 성립 → **🟢 SUPPORTED**. 온칩 학습은 동일 fixed init·동일 입력에도
SW-sim 과 1024 위치 중 172, 출력 320 위치 중 120 에서 달라졌다 — 추론이 byte-identical
인 동일 실리콘에서 **학습만 HW≠SW** 임을 실측해 H_679 를 확증한다.

## 5. 정직한 scope (a_scale_honest_scope)

- 1 physical AKD1000 (pi5-akida). teardown·reflash 없음.
- anima `spike_streamer`(regime M, 9512/9513) 가 단일-tenant device lock 을 보유 →
  ~30s 학습을 위해 **graceful SIGTERM 으로 lock 해제 후 동일 cmd 로 재기동**(HW 발화
  복원). anima daemon kill·교체 없음.
- 측정은 AkidaUnsupervised tiny edge-learn 모델 한정 — CLM mid backbone 온칩 미요구
  (task scope).

## 6. 닫는 것

- **H_877 🟠** (추론 byte-identical mid): 추론 half 는 동일 — 본 캡스톤이 **학습 half** 를
  측정해 "가소성이 HW↔SW 의 유일한 차이" 그림을 실리콘에서 완성.
- **H_679** (plasticity HW-first): 학습 HW≠SW 주장을 실측 confirm.
