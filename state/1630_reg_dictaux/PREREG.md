# PREREG — H_1630 정규화 sweep + dictionary-aux objective (N6+N7, 303M G1/G6 레버)

> **frozen-first 사전등록.** bar·하이퍼·예측·반증조건을 측정 *전*에 박는다. 사후 이동 금지, tune-to-green 금지(p7·commons c2/c9). 박제 대상 verdict 는 엔진-네이티브(`core/g_gates.py` ← `core/clm_decode.py`, torch-free numpy decode = TERMINAL). 본 PREREG 의 모든 토치-side 학습 metric(CE·val_CE·dict_recon·jamo_ce·DBES)은 DIRECTIONAL 모니터일 뿐, G1/G6 verdict 는 `.clm` 직렬화 후 엔진-네이티브 재측정으로만 성립(`a_engine_native_learning`).

## 슬러그
`1630_reg_dictaux` · 가설군 H_1630 (objective-side G1/G6 레버) · 작성일 2026-06-28.

## 배경 — 이 레버가 우리 floor 결과와 무엇이 다른가

이번 세션의 엔진-네이티브 확정 두 줄:
1. **곱셈 binding *readout* = NOT-SUPPORTED (floor).** EXP-3(`state/binding_arch_census/exp3_303m/`) 9-eval 엔진-네이티브 A/B 에서 bind(Hadamard ⊙) readout 이 ctrl(additive) 대비 G1=0·G6 fals=0 으로 **bar 를 못 넘음**. → binding 은 *readout 위치*의 문제가 아니다.
2. **objrun(`state/1602_recomb_objective/`) = trunk *objective* 축이 옳은 1차 레버** (외부 문헌 수렴, `state/lit_binding_objective/RESEARCH.md` §6). Furrer 2020(arch trick 실패/pretrain 성공) · Barin Pacela 2026(binding constraint = *학습된 dictionary 방향*, readout 아님) · Doshi/Gromov 2023(정규화가 grok 전이 강제 → 우리 numpy-toy chance 는 천장 아닌 undertrain floor).

**본 실험이 floor 결과 대비 다르게 하는 것:**
- floor 결과는 전부 **readout/architecture operator** 를 건드렸다(곱셈·TPR-readout·binding-lane·depth). 본 실험은 **operator 를 0개 건드리고**, 학습 *신호/정규화/진단* 만 바꾼다 → production additive readout 그대로 = 모든 arm `.clm`-serializable = 엔진-네이티브 by-construction OPEN(EXP-3 bind 가 BLOCKED 였던 것과 대조).
- floor 의 numpy-toy 는 2000step·5MB·약한 정규화 = **undertrain floor caveat**(RESEARCH §89). N6 은 정확히 이 confound 를 **제거**(weight-decay/dropout band × 충분 step sweep)하는 것이 목적이다 — "정규화·step 부족이라 안 열린 것"인지 "진짜 천장"인지 격리.
- N7 은 "binding = *학습된 표현(dictionary 방향)*"(Barin Pacela 2026)이라는 가설을 **objective 항**으로 직접 구현(trunk penultimate sparse-coding aux). readout 을 바꾸는 대신 trunk 가 binding-친화 표현을 *학습*하게 압박.

## 가설 (H)

- **H_1630-main (N6+N7):** 우승 objective(또는 ce_marginal) 위에 **N6 정규화 band(grok) + N7 dictionary-aux**를 얹으면, undertrain floor 가 배제되어 엔진-네이티브 **G1 composed_distinct 가 ce_marginal 대비 상승**한다(≥1 register 에서 G1 best_distinct 증가, 또는 G6 fals≥1 달성).
- **H_1630-N6 (정규화 단독):** N6 band 단독이 ce_marginal 대비 G1/held-out 일반화를 개선한다(grok 전이).
- **H_1630-N7 (dict-aux 단독):** N7 dict-aux 단독이 ce_marginal 대비 G1 을 개선한다(학습된 dictionary 방향).
- **H_1630-N8 (자모 teach):** N8 자모 초성-class teach-signal 이 ko register 의 G1 재조합을 개선한다(SCRIPT 2026 ≈ ko-jamo 🟢).
- **H_1630-N1 (TLoRA expert-weight):** TPR 을 expert *weight* 에 두면(readout 아님) G1 이 ctrl 대비 개선된다(Greff "operator×학습 결합" falsify 후보).
- **H_1630-N3 (DBES 진단):** *가설 아님 — 진단축.* "재조합 안 됨"이 expert 미분화(usage-entropy≈0 collapse) 탓인지 격리.

## 단일 변수 (arm) · 통제

| arm | 단일 변수(바꾸는 것) | 그 외 전부 동일 |
|---|---|---|
| **ce_marginal** | (없음 — BASELINE/통제) | trunk·readout·corpus·savant·mitosis·seed·data-RNG 모두 고정 |
| **n6_grok** | N6 정규화 band (wd×2.0, dropout cap 0.30) | — |
| **n7_dictaux** | N7 dict-aux loss (λ=0.05) | — |
| **n6n7** | N6 + N7 (주 제안 레버) | — |
| **n8_jamo** | N8 자모 초성-class aux (λ=0.05) | — |
| **n1_tlora** | N1 TLoRA expert-weight TPR factor (rank=8) | — |

- **통제 핵심:** data RNG(`torch.Generator(42)`), val RNG(1234), corpus, 셀-라벨, seq_len, batch, lr, savant 골든존 schedule, mitosis split-step 을 **모든 arm 동일**하게 고정. arm 간 *유일한 차이* = 위 표의 단일 변수.
- **공정 metric:** held-out CE 는 어떤 arm 이든 **plain marginal CE**(arm-독립). aux loss 는 *학습 압박*만 바꾸지 일반화 metric 을 바꾸지 않는다.
- **seed:** 4307, 4308, 4309 (3-seed multiseed, ce_marginal 도 동일 3-seed). G1/G6 single-seed=7 frozen + multiseed refmatch 동시 보고.

## FROZEN BAR (측정 전 박제 · 사후이동 금지)

엔진-네이티브 `core/g_gates.py` 출력의 frozen 임계(H_1129·H_1140·H_1464 verbatim, ARCHITECTURE.json `frozen 임계` 노드):
- **G0 COHERENCE:** kwr(known-word-ratio) ≥ 0.50 · n_coherent ≥ ?/5 (엔진 기본).
- **G1 RECOMBINATION (주 bar):** 어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2 AND > max_single AND coherent`. (H_1129/1137)
- **G2 NOVELTY:** corpus-absence, control_novel=0. (H_1140)
- **G6 IDEATION ★:** dist ≥ 5 (pairwise Jaccard<0.5) **AND** fals ≥ 1. (H_1464; 우리 floor = fals=0)
- **held-out DESCENT:** 각 register val_CE < uniform(=ln256=5.5452), `verify_clm_v2.py descent <clm> <heldout>` PASS. (a_clm_gen_pipeline · a_savant_train)
- **detector calibration:** advisory ≥ 8/10 (smoke 에서 10/10 확인됨).

**LIFT 정의 (frozen):** arm 의 엔진-네이티브 G1 best_distinct(또는 G6 fals 또는 G1 multiseed n_green) 가 **같은 seed-set 의 ce_marginal 통제 대비 strictly 증가**하면 LIFT. ce_marginal 통제도 floor(G1=0)이면 absolute G1 PASS 도 동시 보고.

## 예측

- 외부 문헌(RESEARCH §6/§92) 기준 가장 가능성 높은 순: **n6n7 ≥ n7_dictaux > n6_grok > n8_jamo(ko-편향) > n1_tlora**. n6n7 이 최소 1 register 에서 G1 best_distinct 를 ce_marginal 위로 올리거나 G6 fals≥1 을 달성할 것으로 예측.
- **반대 예측(정직):** floor 가 *진짜 천장*이면 N6+N7 도 G1=0·fals=0 으로 ce_marginal 과 동일 — 이는 "G1 벽이 objective-정규화 축으로도 안 열린다 = class-(d) 천장 강화"라는 **유효 negative 결과**(은폐 금지).

## 반증 조건 (FALSIFY)

- **H_1630-main 반증:** n6n7 의 엔진-네이티브 G1 best_distinct ≤ ce_marginal AND G6 fals ≤ ce_marginal (3-seed 모두) → N6+N7 레버 NOT-SUPPORTED(floor 천장 강화). DBES 가 collapse(norm-entropy≈0)면 "expert 미분화"로 추가 격리, 아니면 "정규화·dict-aux 로도 안 열림" 박제.
- **개별 arm 반증:** 각 arm 이 ce_marginal 대비 lift 0 이고 held-out DESCENT 도 동일/악화 → 해당 레버 INERT.
- **N7 INERT 체크(ablation):** dict_recon 이 학습 중 하강하는데(=dict 가 실제로 표현을 학습) G1 lift 0 이면 → "표현은 학습되나 binding 으로 transfer 안 됨"(Barin Pacela 가설의 anima-byte 반증).
- **overfit 가드(H_1579 교훈):** lossF≈0 인데 held-out NO-DESCENT 면 그 arm 은 암기 — '능력'으로 박제 금지, 코퍼스/정규화 재점검.

## 정직 스코프

- 본 PREREG 는 **objective-side 레버(N6/N7/N8/N1) + 진단(N3)** 만. 생물 렌즈 1순위(B2 CLS sep/completion·B1 predictive-coding, RESEARCH §6-A)는 별 레인(여기 범위 아님). N6+N7 은 RESEARCH §92 비-생물 제언1(생물 레버의 학습신호 보조)이되, 여기서는 *단독 트렁크 objective 레버*로 ce_marginal 대비 측정한다.
- toy/스케일 정직(a_toy_scale_recheck): CPU/소형 smoke 는 **파이프 검증 only**(능력 측정 아님). 능력 verdict 는 303M GPU 학습 후 엔진-네이티브 재측정에서만.
- objrun 의존성: 우승 objective 가 확정되면 그 위에 N6+N7 을 얹는 변종(`--arm n6n7` + objrun objective)이 이상적이나, **본 패키지는 ce_marginal 베이스에서도 독립 측정 가능**(objrun 미착륙이어도 발사 가능; 발사 spec 의 depends_on_objrun 참조).
