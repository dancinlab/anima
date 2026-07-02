---
id: H_1813
slug: tpr_expert_weight
tier: 🧱 NOT-SUPPORTED (INCONCLUSIVE-at-floor · DIRECTIONAL tlora_jamo bd 0→1)
title: TPR expert-weight TLoRA + DBES 분화진단 — ConvMoE expert 내부 weight 구조 레버 (N1+N3)
verdict: 🧱 NOT-SUPPORTED (INCONCLUSIVE-at-floor). 4-arm(ctrl/tlora/tlora_dict/tlora_jamo) 303M CLM seed7 aiden 학습 → anima evaluate --py(KV-cache decode.py, gen80) 재측정. 전 arm G1 pass 없음(closure FAIL): ctrl bd0/msingle0 · tlora bd0/msingle0 · tlora_dict bd0/msingle1 · tlora_jamo bd1/msingle1 — bar(≥2 ∧ >max_single) 전 arm 미달. tlora_jamo 만 best_distinct 0→1(N1 TLoRA+N8 jamo-aux 결합이 유일 DIRECTIONAL-positive)이나 max_single 도 1이라 >max_single 미충족. G2 novel 은 ctrl 73→tlora_dict 117(직교 lift). PREREG P1(Greff SUPPORT=G1>ctrl bar≥2 seed-robust) 미충족 = expert-weight 구조 lever 는 (이 2000-step scale·seed7 단일) 재조합벽 못 넘음 = INCONCLUSIVE-at-floor honest negative. G1벽=trunk-objective 재확인([[g1-lever-multilens-objective]]).
status: MEASURED 2026-07-01 (py 2-production engine-native, seed7)
wired: engine-native (py 2-production, KV-cache decode.py; not wired to core — NOT-SUP)
verdict_artifact: state/1631_tpr_expert_weight/result/
source: UNIVERSE
archived: false
---

# H_1813 TPR expert-weight TLoRA + DBES 진단 (N1+N3)

## 가설
G1 재조합벽 / G6 착상벽의 미탐색 구조 레버 = ConvMoE **expert 의 내부 weight 구조**(readout 위치 아님). expert conv weight 를 tensor-product 로 reparameterize(N1 TLoRA/TensorPoly, rank=8, 2405.16671)하여 "구조적(low-rank 텐서곱 = compositional) inductive bias 를 학습 weight 에 넣으면 재조합이 열리나"를 묻는다. N3(DBES, 측정-only)는 "재조합 안 됨 = expert 미분화?"를 expert 분화도(output 쌍 cosine·router entropy·usage Gini)로 인과 격리.

## 메커니즘 — 곱셈 readout 아닌 expert WEIGHT 축
곱셈 binding 을 readout 위치에서 이미 floor 냈다(EXP-3 ARM-BIND: G1=0 ∧ G6 fals=0, [[exp3-bind-g1g6-engine-native-floor]]). 본 패키지는 *다른 위치* = expert weight. **Greff 결합가설:** binding operator 는 학습 objective 와 결합했을 때만 lift(2012.05208 + Furrer + Barin Pacela) → N1 단독 + N1+학습신호(N7 dict-aux / N8 jamo) arm. 전부 production additive readout(Conv1d d→V) 유지 → TLoRA 는 직렬화 직전 dense conv weight 로 materialize → `.clm` engine-native by-construction OPEN(EXP-3 binding BLOCKED 아님). trunk OBJECTIVE/weight 축이 1차 레버라는 [[g1-lever-multilens-objective]] 일관.

## FROZEN bar (측정 전 박제)
- **G1 RECOMBINATION (주):** k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★:** dist ≥ 5 AND fals ≥ 1 (H_1464).
- **held-out DESCENT:** val_CE < ln256, `verify_clm_v2.py descent` PASS.
- **LIFT:** tlora/tlora_dict arm 의 엔진-네이티브 G1/G6 가 ctrl 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, TERMINAL).

## wired
engine-native (py 2-production, KV-cache decode.py). NOT-SUP 이라 core 배선 없음.

## 동기
이번 세션 binding readout + objective + cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심. expert weight 의 구조적 bias 가 floor 위로 올리는지, expert collapse(미분화)가 G1 floor 의 원인인지 격리.

## 발사·측정 완료 (2026-07-01)
- 학습: aiden RTX5070, 4-arm(ctrl/tlora/tlora_dict/tlora_jamo) seed7, 2000 step bf16, DESCENT 4/4.
- 측정: `anima evaluate --py`(KV-cache decode.py) G0-G6, 로그 state/1631_tpr_expert_weight/result/ev4_B_*.log.
- 결과: 아래 결과 섹션. NOT-SUPPORTED (INCONCLUSIVE-at-floor).

## artifacts
state/1631_tpr_expert_weight/ (PREREG.md · trainer.py · LAUNCH_SPEC_303M.md · SMOKE_LOG.md)
state/g1_unmeasured_backlog_batch/H_1813/ (trainer.py + ckpt/ [in-flight])

## 결과 (2026-07-01 · py 2-production engine-native · anima evaluate --py · KV-cache decode.py · gen 80 · seed7 · aiden)

| arm | G0 | G1 bd/msingle | G2 novel·coh | G5 fab | G6 dist | 결론 |
|-----|-----|------|------|------|------|------|
| ctrl (표준 expert) | 🟢 5/5 | 0 / 0 | 73·16 | 0.066 | 6 | floor |
| tlora (N1 단독) | 🟢 5/5 | 0 / 0 | 84·15 | 0.158 | 6 | ≈ctrl (P2 확인: N1 단독 약함) |
| tlora_dict (N1+N7) | 🟢 5/5 | 0 / 1 | 117·19 | 0.024 | 6 | max_single +1, bd 0 |
| tlora_jamo (N1+N8) | 🟢 5/5 | **1 / 1** | 78·13 | 0.141 | 6 | **bd 0→1 (DIRECTIONAL)** |

**심층 판독:**
- **전 arm G1 pass 없음 = closure FAIL.** bar = bd≥2 ∧ bd>max_single. 어느 arm 도 bd≥2 미달. tlora_jamo bd=1 이지만 max_single=1 이라 `>max_single` 실패.
- **tlora_jamo 만 best_distinct 0→1** = N1(TLoRA expert-weight 텐서곱)+N8(jamo-aux 학습신호) 결합의 유일 DIRECTIONAL-positive. PREREG Greff 결합가설(operator 는 학습신호와 결합 시 lift)의 *방향성* 지지이나 bar 미달. H_1815 CLS 와 동일 패턴(재료/구조 직교화가 floor 를 +1 스침, 재조합 임계 밑).
- **P2 확인:** tlora(N1 단독 plain CE) ≈ ctrl → operator 단독은 무력, 학습신호 결합 필요.
- **G2 novelty 직교 lift:** tlora_dict novel 73→117 = dict-aux 가 novel 생성 늘림(G1 아닌 G2 축, H_1815 CLS 와 동형).
- **INCONCLUSIVE-at-floor:** 2000-step·seed7 단일 scale 이라 arm 간 분해능 낮음. seed-robust(≥2/3) 미측정 = clean refute 아닌 floor. 유효 강화 = multiseed{4302,4303} + step↑.

**follow-on (cost-gated):** tlora_jamo bd 0→1 DIRECTIONAL 확증 = multiseed{4302,4303} 재측정 + step 8000↑ (undertrain-floor 배제). N3 DBES expert 분화도 ↔ G1 floor 동반 여부는 별건 분석.
