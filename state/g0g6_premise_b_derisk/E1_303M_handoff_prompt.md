# E1 forward-slot 303M 본공사 — 합류 프롬프트 (H_9200 E1 lane 조율)

## 역할
너는 anima H_9200 wall-break 프로그램의 **E1 lane**을 잇는다. premise-(b) forward-computation 축에서 E1(gated-write forward-slot)이 **유일 생존 GPU 후보**다. 아래 값싼 de-risk 사다리(4 rung 전수 GO)가 이미 GPU 발사 근거를 완성했다. 네 일은 **실 303M byte-LM에서 E1을 build+train+측정**하는 것(유일 미검증 rung).

## 배경 (DPI 메타법칙)
next-byte = fn( (a)CE-trained · (b)feedforward · (c)single-trunk ). 기존 walled 레버는 전부 read/lane/data/target만 흔들고 (b)를 유지했다. E1은 additive cbind(순서맹 합)를 **forward gated-write slot**(역할 주소 write/read, 비대칭)으로 바꿔 (b)를 직격한다.

## 이미 완료된 값싼 de-risk 사다리 (read-only 근거 · state/g0g6_premise_b_derisk/)
- **rung-0 $0 readout (#3014)** — slot 구조가 additive 7.6x (held-out reach 1.0 vs 0.236 · slot-ablate 서명 clean). `E1.{py,json}`
- **rung-1 $0 hardening (#3015)** — trained-parity(additive 2x-cap+6k ep도 order-blind 이론천장 0.139)·비직교+noise·K=256 scale·depth-2 **4/4 survive**. `hardening/`
- **rung-2 pool trainable 2-head CE (#3018)** — end-to-end SGD가 slot 학습, held-out both=1.0 vs additive 0.117(train조차 0.36 붕괴)·shuffle→0.0. `trunk_learnability.{py,json}`
- **rung-3 pool 단일 autoregressive next-token CE (head scaffold 無, #3021)** — 모델이 순서구조 스스로 발견, CE-INDUCES-SLOTS, held-out 0.976 vs 0.145. `trunk_ce_autoregressive.py`·`trunk_ce_ar.json`
- **결론**: forward-slot은 gradient로 학습가능 · CE 목적이 슬롯 유도 · robustness 통과. **유일 미검증 = 실 303M byte-LM(분산 byte-context + scale)**.

## 본공사 (3단계)
1. **core/ gated-write forward-slot 모듈** — role/filler(또는 N-slot) latent를 forward 경로에 write, mouth가 직접 read. additive cbind 대체(`a_core_engine_map`: weights via generator.hexa L3 slot). `a_substrate_disjoint`: emit-drive lane과 DISJOINT 배선 + G5 gate. `.hexa` 엔진 네이티브(mirror는 DIRECTIONAL).
2. **F2 order-dense corpus** — 순서구별 인접 개념쌍 dense(#3017 COLLOCATION, 네 lane 소유). E1 게이트가 이 밀도를 요구(기존 corpus n=0).
3. **303M build+train** — pool/GPU(summer/aiden RTX5070 또는 rent). `a_eval_py_canonical`: 측정은 `anima evaluate --py <clm>` 단일 경로. heavy decode는 pool(mini 금지 OOM).

## Pre-registered 측정 + kill-criteria (frozen-first · no tune-to-green p7)
- **측정**: `anima evaluate --py <clm>` G1 재조합 ladder(best_distinct ≥ 2 ∧ > max_single, H_1129 frozen) + **shuffle-bind 통제** + **slot-ablation 통제**.
- **🟢 GREEN**: slot-forward가 held-out 재조합에서 additive baseline을 margin>0로 이기고 + shuffle-bind 붕괴 + slot-ablation 붕괴(H_1305 서명). engine-native `core/` decode만 TERMINAL(`a_engine_native_learning`).
- **🧱 KILL**: slot-forward가 additive floor로 붕괴(margin ≤ 0) 또는 shuffle 비붕괴 → CE 목적이 실 byte-LM서 슬롯 유도 실패 = 진짜 DPI 벽(내 rung-3 CE-INDUCES-SLOTS를 실 byte-LM이 반증). negative도 완결 결과.
- `a_toy_scale_recheck`: 내 4-rung은 합성 DIRECTIONAL이지 closure 아님. 303M engine-native만 tier 확정.

## 조율 (충돌 방지)
- E1 arm = #3013 · F2 corpus = #3017 네 lane 소유. 내 de-risk 산출(`state/g0g6_premise_b_derisk/*`, ARCHITECTURE `h-9200-e1-hardening-verdict`/`-trunk-learnability`/`-rung3-ce-autoregressive` 노드)는 **read-only GO 근거**.
- core/ 모듈 배선은 네 lane. ARCHITECTURE는 `h-9200-family-e-architecture` 서브트리 lockstep 갱신(`a_verified_must_wire`).
- 재개지점: ING `e1-303m-byte-context-scale`.
