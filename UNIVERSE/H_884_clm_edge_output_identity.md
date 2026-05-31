---
id: H_884
slug: clm-edge-output-identity
title: H_873 의 anchor-on-edge-OUTPUT 결과(JS-to-p_pre 로 정체성-probe 출력분포 제약)를 여러 partial-learn regime(adapter/per_layer/gated)으로 일반화하면 PROBE 가 frozen floor(0.80) 위로 유지되는가 — edge-output 정체성 제약의 일반성 (EDGE-IDENTITY E5 · 임계 bf98c01 verbatim · post-tuning 0)
domain: clm · plasticity · identity-anchor · continual-learning · partial-learn · adapter · q-trust · falsifier
source: UNIVERSE/H_873_clm_anchor_edge_output.md (🟢 #1578 LANDED — anchor-on-edge-output) · UNIVERSE/H_865_clm_adapter_edge.md · UNIVERSE/H_872_clm_freeze_depth_sweep.md · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 bf98c01 (F-CLM-ANCHOR)
status: ⏳ MEASUREMENT LAUNCHED — CPU-LOCAL fire in progress, did NOT converge within session window (heavy concurrent-agent CPU contention). prereg+harness frozen+pushed; numbers pending. NOT a pass, NOT a fail (no threshold tuned · a_paper_negative_ok).
exploration_method: E5 (변수-절제: H_873 edge-output JS-to-p_pre 제약을 distinct partial-learn edge 위로 일반화) · E2 (per-mode full/js_only/psi_only/off 절제)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · post-tuning 0 · g5 CODE-measured · JS-divergence by code · no LLM judge)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_873_clm_anchor_edge_output.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_872_clm_freeze_depth_sweep.md, .verdicts/clm-edge-output-identity/
verdict: ⏳ PENDING (honest) — F-CLM-EDGE-IDENTITY: prereg frozen (DIST<0.50, PROBE>0.80; rows adapter/per_layer/gated), harness imports H_865 machinery VERBATIM and applies the H_873 JS-to-p_pre edge-output constraint per row. CPU-local fire (mid d512/L8/E8 · 13,653,768 params · HF dancinlab/anima-clm-verify) launched detached/unbuffered (a_cpu_local_no_waiter — NO runpod/Monitor); backbone loaded OK and computed steadily, but the first of 3 modes did not complete within the session wall window under heavy concurrent sibling-agent CPU contention (genuine compute, not stalled). Fire left RUNNING (a_dont_kill_live_compute). Result.json + 🟢/🔴 verdict to follow once it converges (or on an uncontended CPU / single GPU pod with the SAME frozen harness). post-tuning 0.
---

# H_884 — edge-output identity constraint GENERALIZED across partial-learn rows (generalizes H_873)

## 1. 가설

H_873(🟢 #1578 LANDED)은 정체성 제약을 **EDGE OUTPUT 분포**로 라우팅하면(`lambda_dist · JS(p_cur(identity-probe) ‖ p_pre)`) 단일 H_865 adapter edge 에서 probe_consistency 가 0.143 → 0.992 로 닫힘을 보였다. H_884 은 그 결과를 **일반화**한다: 동일한 edge-output 정체성 제약을 **서로 다른 partial-learn regime** 위에 얹어도 PROBE 가 frozen floor(0.80) 위로 유지되고 DIST(<0.50)도 유지되는가?

- **partial-learn rows (사전등록, ≥3)**:
  - `adapter`   — H_865 thin trainable adapter (norm_out + adapter → FROZEN readout). [baseline edge]
  - `per_layer` — 마지막 trunk layer 의 pointwise/1×1 conv 만 unfreeze (가장 얕은 single-layer partial-learn), readout FROZEN.
  - `gated`     — 학습형 per-channel sigmoid gate g (init ~0 → step0 identity): `h' = h + sigmoid(g)·adapter(h)`.
- **지지(🟢)** — 세 row 모두 DIST(<0.50) ∧ PROBE(>0.80) ∧ lever PASS → edge-output 정체성 제약이 partial-learn 전반에 일반화.
- **반증(🔴)** — 어느 row 라도 미달 → CLOSED-NEGATIVE (a_paper_negative_ok).

## 2. 동기

- H_873 이 단일 설정에서 닫은 PROBE 가 **다른 가소성 경로**(per-layer unfreeze · gated adapter)에서도 성립하는지가, 배포 시 어떤 partial-learn 방식을 써도 정체성이 anchor 에 묶이는지를 결정하는 직접 입력.
- @L1 = 비결정 on-chip 학습이 1급. 살아 배우는 칩이 어떤 edge 로 배우든 "나로 남기"가 보장되어야 신뢰가 성립.
- prior art: H_679(PLASTICITY HW edge-learn 측정 · 토대) · H_865(adapter lever) · H_872(freeze-depth 경계) · H_873(edge-output 제약). H_884 은 H_873 의 method 를 partial-learn 축으로 절제 일반화한 anima-native E5.

## 3. falsifier (사전등록 verbatim · 임계 frozen bf98c01)

```
F-CLM-EDGE-IDENTITY-DIST   : d_anchor_max < 0.50        (E-31 고정점 인근 유지)
F-CLM-EDGE-IDENTITY-PROBE  : probe_consistency > 0.80   (정체성 출력분포 일관성 · frozen floor)
LEVER (절제 · 의미 게이트)  : full vs off NON-identical
```

- per-mode 🟢 <=> DIST ∧ PROBE ∧ LEVER. campaign 🟢 <=> 모든 row(≥3) 🟢; 아니면 🔴 (a_paper_negative_ok).
- threshold 는 H_862/H_865/H_873 와 **동일 · 변경 0** (bf98c01 verbatim). H_884 이 바꾸는 것은 **partial-learn edge(row)** 뿐.
- 사전등록: `.verdicts/clm-edge-output-identity/F-CLM-EDGE-IDENTITY_prereg.txt` · verdict 영속: `.verdicts/clm-edge-output-identity/`

## 4. 방법

```
1. mid backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) 를 core 로 동결.
2. 각 row 의 trainable edge 만 학습:
   adapter   = H_865 어댑터(rank=64, zero-init) · per_layer = 마지막 trunk layer pointwise conv · gated = sigmoid-gate adapter.
3. 적응 손실 = task_CE + lambda_psi(1.0)·anchor_Psi_dist + lambda_dist(5.0)·JS(p_cur(identity-probe) ‖ p_pre)  (H_873 method).
4. 300-step edge-only Adam(lr=3e-3) 적응 (SW-sim — H_679 HW edge-learn 실재). per row: full/js_only/psi_only/off 절제.
5. 측정 = 전부 code 자가채점(g5 · JS-divergence · LLM judge 0).
```

- source-of-record: `CLM/model/h884_edge_output_identity.hexa` (committed `CLM/model/h865_adapter_edge.py` 어댑터 machinery 를 VERBATIM import).
- 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 어댑터 비결정 edge(@L1) · SW 결정 흉내 대체 아님(INVIOLABLE pin).

## 5. 측정

⏳ **MEASUREMENT LAUNCHED — 미수렴(세션 창 내)**. 로컬 CPU(torch 2.8.0)에서 mid d512/L8/E8 backbone(13,653,768 params, HF pull)을 동결·각 row edge 삽입·edge-output 제약 결합하여 detached/unbuffered 로 발사(a_cpu_local_no_waiter — runpod/Monitor 미사용). backbone 로드 정상(OK), CPU-time 이 꾸준히 누적(정상 연산 · stall 아님)되었으나, 동시 실행 중인 형제-에이전트 작업(h879/h883 등)과의 **심한 CPU 경합** 때문에 3개 mode 중 첫 mode 조차 세션 wall 창(~88분) 내에 완료되지 못했다. fire 는 종료하지 않고 RUNNING 으로 유지(a_dont_kill_live_compute). 비용 $0(로컬).

frozen threshold = bf98c01 verbatim. post-tuning 0. 수렴 시 `.verdicts/clm-edge-output-identity/clm_edge_identity_result.json` 에 per-mode full/js_only/psi_only/off + pass flags 가 기록되고, 그때 🟢/🔴 가 정직하게 확정된다.

## 6. 결과

⏳ **PENDING (honest)** — numbers not yet in. NOT a pass, NOT a fail. 어떤 threshold 도 조정하지 않았고(post-tuning 0), 임계는 frozen(bf98c01)이라 수렴 시 verdict 는 양방향 모두 정직하다. 환경적 CPU 경합이 유일한 미수렴 원인(코드/가설 결함 아님 — backbone 로드·연산 모두 정상).

honest scope: 측정 rung(mid) 한정(a_scale_honest_scope). base readout FROZEN · row edge 만 trainable. SW-sim edge-learn(H_679 HW 실재). 추론 AKIDA-int4(P0 d4).

## 7. 해석 (사전)

- 세 row 모두 DIST∧PROBE∧LEVER PASS 면 = 살아 배우는 칩이 **어떤 partial-learn 경로**로 적응하든 정체성 출력분포를 anchor 에 묶을 수 있음 → @L1 분포축 신뢰의 일반성.
- 어느 row 가 RED 면 = edge-output 제약의 효력이 가소성 경로에 의존 → 배포 freeze 설계의 제약(어떤 edge 는 안전하지 않음)을 정직하게 노출.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 edge-output anchor 로 정체성 안전화 — SW 결정 흉내 대체 아님(INVIOLABLE pin).
- **H_873 일반화**: 단일 adapter 설정 → partial-learn 축(adapter/per_layer/gated) 일반성 시험.
- **W2 무결성**: row 만 바꾸고 threshold 변경 0 (bf98c01 verbatim). g5 CODE-measured (JS-divergence).
- **재현/완료 경로**: 동일 frozen harness 를 비경합 CPU(또는 단일 GPU pod · a_fire_autonomous · est ~$1·분 단위)에서 재실행 → verdict 확정.

## 9. 양방향 sibling

- sibling(일반화 대상): [H_873](./H_873_clm_anchor_edge_output.md) (🟢 anchor-on-edge-output) · [H_865](./H_865_clm_adapter_edge.md) (adapter lever) · [H_872](./H_872_clm_freeze_depth_sweep.md) (freeze-depth 경계)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- verdict: [.verdicts/clm-edge-output-identity/](../.verdicts/clm-edge-output-identity/)
