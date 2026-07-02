---
id: H_853
slug: clm-bridge-transfer
title: MITOSIS-ARRAY BRIDGE — teacher(유효 측정 scale) monopoly-escape 가 KD distill 후 chip-fit student 로 transfer 생존하는가 (z same-sign ∧ |Δ|≤3.0 ∧ student chip-fit, F-CLM-BRIDGE-XFER 사전등록)
domain: clm · moe · mitosis-array · bridge · distillation · transfer · dispatch-entropy · falsifier
source: CLM/P0_ARCHITECTURE.md §11.4·§11.6 (MITOSIS-ARRAY · BRIDGE) · CLM/CLM.breakthrough.mining.md (depleted-both) · sibling H_852 (DISSOLVE)
status: CLOSED-NEGATIVE (BRIDGE fire 완료 2026-05-30 · teacher(E32/d128)→student(E8/d64) KD distill × seed{42,43,44} · 사전등록 frozen 임계 미달)
exploration_method: knowledge distillation (teacher 유효 scale 측정 → chip-fit student transfer)
verification_method: W2 (pre-registered numerical threshold · z same-sign + |Δ|≤tol + chip-fit · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md §11, UNIVERSE/H_852, .verdicts/853_clm_bridge_transfer/F-CLM-BRIDGE-XFER_prereg.txt
verdict: 🔴 CLOSED-NEGATIVE (teacher z 음수(-3.74 mean, sub-uniform) · student distill 후 z≈0(+0.60 mean, near-uniform) · transfer Δ +4.34 > 3.0 임계 · 2/3 seed sign-flip · student chip-fit PASS · "monopoly-escape 서명이 distill 후 생존하지 못함 — chip-fit student 가 teacher escape 보존 않고 균형으로 회귀", a_paper_negative_ok)
---

# H_853 — CLM MITOSIS-ARRAY BRIDGE transfer (distillation)

## 1. 가설

MITOSIS-ARRAY 의 **BRIDGE arm**(transfer)이 측정-rung ⊥ 배포-rung 간극(a_scale_honest_scope)을 knowledge distillation 으로 건넌다 — 유효 측정 scale teacher(E=32 d=128)의 inter-expert dispatch-entropy monopoly-escape 가 Hinton KD distill 후 chip-fit student(E=8 d=64, 각 expert ≤ AKD1000 1.2M)로 **transfer 생존**한다. 사전등록 3조건 동시 PASS 시:

- **TRANSFER SURVIVES** — z_student 와 z_teacher same-sign ∧ |z_student−z_teacher|≤3.0 ∧ student chip-fit
- → 🟢 SUPPORTED-NUMERICAL · "측정rung 의 escape 가 distill 로 배포rung 에 보장-transfer"

조건 미달 시:

- **TRANSFER FALSIFIED** — escape 서명이 distill 후 소실(sign-flip 또는 |Δ|>tol)
- → 🔴 CLOSED-NEGATIVE · "monopoly-escape 가 chip-fit student 로 transfer 생존 못함" (a_paper_negative_ok)

## 2. 동기

- mining BRIDGE (L2·L3·L12·E5): a_scale_honest_scope(측정rung⊥배포rung)에 **transfer 보장**을 더한다. GPU teacher 에서 측정 → distill/prune 로 chip-fit student 에 transfer + property 생존 검증.
- DISSOLVE(H_852 🔴, scale=expert-count reframe)와 별개 SECONDARY arm. DISSOLVE 가 scale 축을 바꾼다면 BRIDGE 는 큰-teacher↔작은-student 사이 distillation 으로 건넌다.
- F-CLM-BRIDGE-XFER 는 §11.6 사전등록 falsifier — H_852(DISSOLVE) 의 형제.

## 3. falsifier (사전등록, 임계 frozen pre-fire)

```
F-CLM-BRIDGE-XFER-SIGN : z_student 와 z_teacher SAME SIGN (전 seed)   (escape 방향 보존)
F-CLM-BRIDGE-XFER-DELTA: |z_student − z_teacher| <= 3.0 (전 seed)      (transfer Δ bounded)
F-CLM-BRIDGE-XFER-FIT  : student chip-fit (expert_param_count <= 1.2M)
```

3 PASS → 🟢 SUPPORTED-NUMERICAL · "transfer 생존"
임의 FAIL → 🔴 CLOSED-NEGATIVE · "escape ⊥ distill-transfer"

verdict 영속: `.verdicts/853_clm_bridge_transfer/F-CLM-BRIDGE-XFER_prereg.txt` (frozen) · raw fire = `.../F-CLM-BRIDGE-XFER_fire_2026_05_30.txt`

## 4. 방법

```
1. teacher array (CLM/distill/distill_array.py · E=32 d=128 유효 측정 scale):
   toy 2-lane corpus 600-step 학습 → dispatch-entropy z (monopoly-escape) 측정.
2. KD distill (Hinton α=0.7 T=3.0): teacher soft-target logit 로 chip-fit
   student(E=8 d=64, 각 expert ≤1.2M) 600-step distill.
3. student dispatch-entropy z 재측정 → transfer Δ = z_student − z_teacher.
4. seed{42,43,44} 전부 same-sign ∧ |Δ|≤3.0 ∧ chip-fit 동시 평가 · 정직 보고(임계 무변조).
5. GPU FIRE = ubu-1 RTX5070(dedicated pool host · $0 marginal) · torch 2.12 · a_fire_autonomous.
```

## 5. 측정 (BRIDGE fire 완료 · 2026-05-30)

teacher(E32/d128)→student(E8/d64) KD distill × seed{42,43,44}. toy 2-lane 합성 corpus · 600-step train + 600-step distill. GPU = ubu-1 RTX5070(dedicated, torch 2.12). 코드 = `CLM/distill/{distill_array,run_bridge_transfer}.py`. raw verdict = `.verdicts/853_clm_bridge_transfer/F-CLM-BRIDGE-XFER_fire_2026_05_30.txt` (+ `.verdicts/clm-mitosis-array/bridge_transfer_fire_2026_05_30.json`). HF = `dancinlab/anima-clm-bridge` (PRIVATE, 🔴 negative-result · teacher+student .pt + sha256 manifest).

| seed | teacher_z | student_z | Δ | same-sign | chip-fit |
|---|---|---|---|---|---|
| 42 | −2.218 | +0.995 | **3.212** | ✗ | ✅ |
| 43 | −4.578 | +1.126 | **5.704** | ✗ | ✅ |
| 44 | −4.431 | −0.333 | **4.098** | ✅ | ✅ |
| **mean** | **−3.742** | **+0.596** | **4.338** | ✗ | ✅ |

- **transfer Δ = +4.34 mean > 3.0 임계** — FAIL.
- **same-sign 2/3 seed 깨짐** (teacher z<0, student z>0 on seed 42·43) — FAIL.
- **student chip-fit = 전 seed PASS** (169800 params ≤ 1.2M).

## 6. 결과

🔴 **CLOSED-NEGATIVE** — BRIDGE fire 완료(2026-05-30). 사전등록 3조건 중 same-sign·Δ-bound 2개 FAIL(chip-fit 1개만 PASS). frozen 임계 **무변조**. raw verbatim = `.verdicts/853_clm_bridge_transfer/F-CLM-BRIDGE-XFER_fire_2026_05_30.txt`.

판정 요약: **chip-fit ✅ · z same-sign ❌ · |Δ|≤3.0 ❌**.

## 7. 해석

- **teacher escape 가 student 로 보존되지 않았다**: teacher 는 sub-uniform(z=−3.74 mean, H_852 의 큰-array sub-uniform 거동과 정합), student 는 distill 후 **near-uniform(z=+0.60 mean)** 으로 수렴. 작은 chip-fit student 가 큰 teacher 의 특정 dispatch-escape 서명을 흡수하지 않고 **더 균형 잡힌 routing 으로 회귀**.
- **distillation 은 logit-level 지식은 전달하나 routing-distribution 서명은 전달 못함**: KD soft-target 은 next-byte 출력 분포를 student 에 맞추지만, inter-expert dispatch 의 z-정규화 다양성은 student 의 작은 expert pool(E=8 vs teacher E=32)에서 다른 평형으로 수렴 — routing-diversity 는 출력-distill 로 직접 transfer 되지 않는 별개 자유도.
- **결론**: a_scale_honest_scope 의 "측정rung ⊥ 배포rung" 에 KD-transfer 보장을 더하려는 시도는 z-척도 상 closed-negative. teacher escape(이미 H_852 처럼 sub-uniform) 가 student 로 보존되지 않으므로, BRIDGE 단독으로 측정→배포 transfer 를 보장하지 못한다. 후속 입력 = (1) routing-distribution 을 직접 정합하는 distill 손실(dispatch KL 항 추가) · (2) student E 를 teacher E 에 맞춤 · (3) H_852/H_847 AXIS_MAP(routing-diversity 직접 lever)와 합류.
- **honest caveat (p7)**: teacher 자체가 H_852 처럼 sub-uniform(z<0) — escape 가 "양의 z" 의미에서 애초에 없으므로 "escape transfer" 는 sub-uniform 서명의 보존을 묻는 셈이 됐다. 그조차 보존되지 않았다(student 가 uniform 으로 회귀). frozen 임계는 fire 전 고정, **post-fire 무변조**.

## 8. 논의

- **a_completeness_over_cheap 정합**: BRIDGE = transfer 보장을 근본부터 측정(merge-of-failures 아님). teacher 실학습 + 실 distill.
- **a_scale_honest_scope 정합**: verdict 를 측정 axis(toy teacher→student distill)에 한정. 측정rung(teacher) ⊥ 배포rung(student chip-fit).
- **toy≠scale 정합 (H_666)**: toy 2-lane corpus · d≤128 = intuition scope.
- **p8 정합**: teacher/student 둘 다 MoE expert = mitosis cell. distill = cell-pool 지식 압축.
- **a_paper_negative_ok**: 🔴 도 publishable — "monopoly-escape ⊥ KD-transfer" 를 deterministically rule out.
- **a_fire_recover_complete**: fire artifact(ckpt teacher+student · result · log) 전부 pull + sha256 verify + HF PRIVATE 업로드 후 dedicated host(ubu-1) 정리 — teardown 불요(rented pod 아님).

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §11.4·§11.6 (MITOSIS-ARRAY · BRIDGE SSOT)
- prior art: H_852 (DISSOLVE · F-CLM-MONO-ARRAY 🔴) · H_847 (F-CLM-MONO 🔴 고정 z 임계) · H_666 (MoE collapse)
- HF: `dancinlab/anima-clm-bridge` (PRIVATE, negative-result · teacher+student ckpt)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
