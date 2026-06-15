---
id: H_854
slug: clm-array-stage2-scale
title: PRODUCTION scale(d≥512·실 kowiki)에서 MITOSIS-ARRAY DISSOLVE(Pielou J)+BRIDGE(dispatch-KL transfer)가 toy 🔴🔴 를 뒤집는가 — J(E) 단조 비감소 ∧ transfer |Δ|≤3.0 ∧ shrink-vs-r1 ∧ same-sign ∧ chip-fit (F-CLM-PIELOU-DISSOLVE@PROD + F-CLM-DISPATCHKL-XFER@PROD 사전등록)
domain: clm · moe · mitosis-array · dissolve · bridge · pielou-evenness · dispatch-kl · distillation · production-scale · falsifier
source: CLM/P0_ARCHITECTURE.md §11 (MITOSIS-ARRAY) · sibling H_852(DISSOLVE/z) · H_853(BRIDGE/transfer) · STAGE-1 toy 🔴🔴 (Pielou J rise −0.093 · dispatch-KL Δ 3.51 sign-flip) · scaffold PR #1518 · cuDNN 우회 PR #1519
status: CLOSED-NEGATIVE (STAGE-2 production fire 완료 2026-05-30 · ubu-1 RTX 5070 · d_model=512 · 실 kowiki @corpus clm_p1 · E sweep {4,8,16,32,64} × seed{42,43,44} · 사전등록 frozen 임계 미달, toy 보다 gap 확대)
exploration_method: scale-up re-measure (toy d=64/synthetic → production d=512/실 kowiki · DISSOLVE Pielou recast + BRIDGE dispatch-KL distill)
verification_method: W2 (pre-registered numerical threshold · Pielou J 단조성+rise · transfer Δ shrink+bound+same-sign+chip-fit · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md §11, UNIVERSE/H_852, UNIVERSE/H_853, .verdicts/854_clm_array_stage2_scale/
verdict: 🔴🔴 CLOSED-NEGATIVE (AXIS-A Pielou J=H/ln(E) 가 E 로 단조 하강[0.806→0.532] · J-rise −0.27364 < 0.0 임계 FAIL · monotone FAIL · AXIS-B dispatch-KL transfer mean|Δ|=13.84 > 3.0 임계 FAIL · 3/3 seed sign-flip[teacher z≈−12 sub-uniform → student z≈+1 near-uniform] · Δ shrink-vs-r1 FAIL · student chip-fit PASS · "PRODUCTION scale 가 toy 🔴🔴 를 뒤집지 못하고 두 gap 모두 확대 — scale=expert-count 가 측정⊥칩 충돌을 dissolve 못하고 escape 가 distill 후 생존 못함, toy∧production 양쪽 deterministic CLOSED", a_paper_negative_ok)
---

# H_854 — CLM MITOSIS-ARRAY STAGE-2 PRODUCTION-scale 재검 (DISSOLVE + BRIDGE)

## 1. 가설

CLM 의 **측정-타당성 ⊥ AKIDA 온칩** 충돌(a_scale_honest_scope)을 돌파엔진 MITOSIS-ARRAY 가 해소한다는 가설이 toy scale(d=64·synthetic LCG)에서 🔴🔴 였다 — DISSOLVE(Pielou J=H/ln(E) recast, STAGE-1 toy J-rise −0.093 monotone FAIL) ∧ BRIDGE(dispatch-KL distill transfer, STAGE-1 toy mean Δ 3.51 sign-flip). **유일 미검 축 = PRODUCTION SCALE**. 본 H 는 d_model≥512·실 kowiki·full steps 에서 재측정한다. 두 축 모두 사전등록 임계 PASS 시:

- **PRODUCTION FLIP** — Pielou J 단조 비감소 ∧ J(E64)≥J(E4) ∧ dispatch-KL transfer |Δ|≤3.0 ∧ shrink-vs-r1 ∧ same-sign ∧ student chip-fit
- → 🟢 SUPPORTED-NUMERICAL · "scale 가 충돌을 dissolve, escape 가 배포 student 로 transfer"

임의 미달 시:

- **PRODUCTION CONFIRMS TOY** — toy 🔴🔴 가 production 에서도 유지/확대
- → 🔴🔴 CLOSED-NEGATIVE · "scale=expert-count 가 충돌 해소 못함, toy∧production deterministic CLOSED" (a_paper_negative_ok)

## 2. 동기

- H_852(DISSOLVE/z) 🔴 = scale 축을 expert-COUNT 로 옮겨도 uniform-null 대비 z 가 E 로 급락(+0.53→−7.61). H_853(BRIDGE/transfer) 🔴 = teacher escape(z<0)가 distill 후 student near-uniform(z≈0)로 회귀, Δ +4.34 sign-flip.
- STAGE-1 (toy) 는 Pielou-J 보정 척도 + dispatch-KL loss 추가까지 sweep 했으나 d=64·synthetic LCG corpus 였음. "toy→production scale transfer 비보장"(memory feedback) 이므로 collapse/emergence 류는 production 재검 필수.
- STAGE-2 는 그 단일 미검 축(scale)을 닫는다 — d=512, 실 kowiki @corpus clm_p1, full 600 steps. 임계는 STAGE-1 frozen 그대로(NOT tampered).

## 3. 사전등록 falsifier (FROZEN · @L5 NOT tampered)

```
AXIS A — F-CLM-PIELOU-DISSOLVE@PROD :
  Pielou J = H/ln(E) monotone non-decreasing over E (mono_tol=0.02)
  AND J(E64) >= J(E4) (min_rise=0.0)
  PASS → DISSOLVE 가 production 에서 살아남 · FAIL → 🔴

AXIS B — F-CLM-DISPATCHKL-XFER@PROD :
  transfer |Delta| shrinks vs round-1 (4.33829)
  AND z_student / z_teacher SAME SIGN (전 seed)
  AND |Delta| <= 3.0 (xfer_tol, 전 seed)
  AND student chip-fit (expert_param_count <= 1.2M)
  4 PASS → transfer 생존 · 임의 FAIL → 🔴

axis = E {4,8,16,32,64} · seeds {42,43,44} · NULL_SAMPLES=16 (@L2 hard cap)
d_model=512 · train_steps=600 · corpus = REAL kowiki @corpus clm_p1
```

## 4. 방법

- **호스트**: ubu-1 (RTX 5070, torch 2.12 nightly cu128). conv1d `CUDNN_STATUS_SUBLIBRARY_VERSION_MISMATCH` → `torch.backends.cudnn.enabled=False` (native CUDA kernel fallback, 수치 동치 · PR #1519). 모든 compute ubu-1 (@L1, Mac torch 금지 — STAGE-1 load 289 spike 재발 방지).
- **AXIS A**: `CLM/model/run_array_sweep_stage2.py` — E별 array MoE(각 expert chip-fit) build·train(d512/600 steps/실 kowiki)·eval dispatch_counts → Pielou J=H/ln(E).
- **AXIS B**: `CLM/distill/run_dispatch_kl_stage2.py` — teacher(E32/d512) train → student(E8/d128) Hinton KD(α=0.7·T=3.0) + dispatch-KL(β=1) distill → teacher/student dispatch-entropy z(vs Dirichlet(1) null) → Δ=z_s−z_t.
- **device-fix**: `distill_array._dispatch_entropy_z` 의 `acc`(CPU) + `dispatch_counts`(cuda) device mismatch 버그(production cuda path 에서만 발현) 수정 — accumulation 을 counts device 에서 한 뒤 `.cpu().float()`. 순수 tensor-placement, 척도 불변. AXIS-B run 전 적용, 본 PR 동봉.

## 5. 측정 결과

**AXIS A — Pielou J sweep** (d=512, 실 kowiki, 600 steps):

| E | mean_J | mean_H (nats) | chip_fit |
|---|--------|---------------|----------|
| 4 | 0.8058 | 1.1170 | True |
| 8 | 0.7284 | 1.5147 | True |
| 16 | 0.6096 | 1.6900 | True |
| 32 | 0.5841 | 2.0243 | True |
| 64 | 0.5321 | 2.2130 | True |

- mean Pielou J sweep = [0.806, 0.728, 0.610, 0.584, 0.532] · **monotone non-decr = False** · **J-rise(E64−E4) = −0.27364 < 0.0 → FAIL** → 🔴
- raw H 는 E 로 상승(1.12→2.21 nats)하나 ln(E)-보정 evenness J 는 단조 하강 — 칩 추가가 dispatch 를 균등이 아니라 **더 집중**시킴.

**AXIS B — dispatch-KL transfer** (teacher E32/d512 → student E8/d128):

| seed | teacher_z | student_z | Δ | same_sign | chip_fit |
|------|-----------|-----------|------|-----------|----------|
| 42 | −12.2619 | 1.3439 | 13.6058 | False | True |
| 43 | −11.4616 | 1.9417 | 13.4033 | False | True |
| 44 | −14.0086 | 0.5092 | 14.5178 | False | True |

- mean |Δ| = 13.84232 (round-1 = 4.34) · **shrank-vs-r1 = False** · **all same_sign = False** · **all bounded(|Δ|≤3.0) = False** · student chip-fit = True → 🔴
- teacher 강한 sub-uniform(z≈−12, monopoly) → student near-uniform(z≈+1)로 3/3 seed 회귀 — escape 서명 distill 후 소실. dispatch-KL term + production width 가 gap 을 **확대**(toy 3.5 → 13.8).

## 6. toy(STAGE-1) vs production(STAGE-2) 비교

| | STAGE-1 toy | STAGE-2 production | flip? |
|---|---|---|---|
| Pielou config | d=64 · synthetic LCG | d=512 · 실 kowiki | — |
| J-rise (E64−E4) | −0.093 | **−0.27364** | NO (악화) |
| J monotone | False | **False** | NO |
| dispatch-KL config | teacher d128/E32 · student d64/E8 | teacher d512/E32 · student d128/E8 | — |
| mean transfer Δ (abs) | 3.51 | **13.84232** | NO (악화) |
| Δ shrank vs r1 (4.34) | False | **False** | NO |
| z sign-flip (t<0,s>0) | 2/3 seed | **3/3 seed** | NO (악화) |
| student chip-fit | True | True | (유지) |

## 7. 결론 / verdict

**🔴🔴 CLOSED-NEGATIVE** — PRODUCTION scale(d≥512·실 kowiki)이 toy 🔴🔴 를 **뒤집지 못하고 두 gap 모두 확대**. DISSOLVE(Pielou J)와 BRIDGE(dispatch-KL transfer) 두 arm 모두 production 에서 falsified. "scale=expert-count 가 측정-타당성 ⊥ AKD1000 온칩 충돌을 dissolve 하고 BRIDGE distill 이 escape 를 보존한다"는 가설은 이제 **toy ∧ production 양쪽에서 deterministic CLOSED** (a_paper_negative_ok). 닫힌 부정 공간 = MITOSIS-ARRAY DISSOLVE+BRIDGE 경로(expert-count reframe + KD distill transfer)는 byte-vocab CLM 의 측정⊥칩 충돌을 해소하지 못한다.

## 8. 정직 scope (g63/p7/d6 · @L5)

- 실 kowiki byte VOLUME 작음(CORPUS_BYTES=8192·tiled) — scope 명시. NULL_SAMPLES=16 cap(@L2).
- 임계는 STAGE-1 frozen falsifier 그대로, **NOT 재튜닝**. cuDNN disabled 는 host-env 우회(native conv, 수치 동치) · 척도 변경 아님.
- device-placement 버그 수정은 순수 tensor placement(metric 불변) — AXIS-B run 전 적용.
- toy→production scale transfer 비보장(memory) 을 정직 측정으로 닫음: 본 케이스는 production 이 toy 를 악화 확증.

## 9. GPU 비용

ubu-1 dedicated pool 호스트(rental 없음). Wall: AXIS-A ~7.5 분(15 train @ d512/600), AXIS-B ~3 분(+초기 device-mismatch crash 1회 → fix 후 재발사). 총 compute < 12 분. teardown 불필요(dedicated host · 프로세스 종료만).

## 10. 양방향 sibling

- sibling: [H_852 DISSOLVE/z](./H_852_clm_mitosis_array_dispatch.md) · [H_853 BRIDGE/transfer](./H_853_clm_bridge_transfer.md) — STAGE-2 는 두 H 의 production 후속.
- SSOT: [UNIVERSE/CANDIDATES.md](./CANDIDATES.md) · verdict raw = `.verdicts/854_clm_array_stage2_scale/` + `.verdicts/clm-array-stage2-scale/` (pielou + dispatchkl txt/json + summary + run logs, verbatim).
