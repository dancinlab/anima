# H_9200-E1-SLW — gated-write forward-slot (SLW) vs the additive-cbind G1 wall

**tier**: 🛠️ IMPLEMENTED · 측정대기 (frozen-first · pre-reg kill-criteria · 신규 측정 0)
**parent**: [[H_9200]] G1·G6 wall-break exhaustive program — premise-(b) forward-computation 축, E1 lane (유일 생존 GPU 후보)
**lane**: E1 (#3013) · corpus = F2 COLLOCATION (#3017)

## 가설
anima next-byte = fn( (a)CE-trained · (b)feed-forward · (c)single-trunk ). G1 재조합벽의
구조적 원인 = 결합연산자가 **additive `cbind`**(순서맹 합) → 거리 D>RF인 두 개념이 수학적
독립 → 재조합 불가(capacity 무관, receptive-field-bound). **SLW**(gated-write forward-slot)는
additive cbind를 **content-addressed slot memory**로 교체한다: role/filler를 비대칭 포트로
받아(하나는 주소 `a_t=softmax(W_r·x_t·Kᵀ)`, 하나는 내용 `v_t=W_v·x_t`), causal erase-then-write로
슬롯에 쓰고, 읽기 주소 `b_t=softmax(W_q·x_t·Kᵀ)`로 read-after-write. 슬롯 S가 **토큰 스트림 밖**에
살아 위치 i의 write를 j>i에서 j−i 무관하게 read → D>RF 독립벽을 가로지른다.

## 왜 DOA가 아닌가 (convergence G1_WALL_LEVER_IS_OBJECTIVE_NOT_READOUT 통과)
CE-deleted TPR/HRR forward-slot(R=2 fixed-orthonormal roles)은 `Σ_r S_r·(yn⊙roles_r)=W_eff·yn`
**선형붕괴** → 표준 선형 readout과 동일천장 BY CONSTRUCTION이라 DOA였다. SLW는 주소 `a_t`·게이트
`g_t`가 **data-dependent softmax/sigmoid(learned gating)** = 비선형 → fixed-role 선형붕괴 아님 =
convergence가 명시한 "비선형(learned gating·data-dependent roles)만 미측정" 범주. de-risk 4/4 GO
(rung0 slot구조 7.6x · rung1 hardening 4/4 · rung2 trunk-learnability held-out 1.0 vs add 0.117 ·
rung3 CE-INDUCES-SLOTS 0.976 vs 0.145). **유일 미검증 = 실 303M byte-LM(분산 byte-context+scale)**.

## 구현 (CORE-owned · 이번 세션)
- `core/slw.py` — SSOT: torch `SLWModule`(학습·DIRECTIONAL) + numpy `slot_apply`(추론·byte-parity,
  `anima evaluate --py` TERMINAL) + `"SLW\x01"` trailer codec `pack_slw`/`read_slw`.
- `core/model.py` — unified CONV+BYTE 모델; CLMConvMoE forward에 SLW hook(post-norm penultimate,
  readout 직전; `cfg.slw` None ⇒ byte-identical additive golden path).
- `core/serialize.py::append_slw_trailer` — trailer chain 끝(CLMX/CLMB 뒤)에 SLW weight append;
  absent ⇒ 기존 additive .clm byte-동일.
- `core/decode.py` — `clm_load_weights`가 trailer read → `_fwd_logits`가 penultimate에 `slot_apply`
  (측정 decode 경로 `clm_decode_topk_sampled_W`·CE forward 양쪽). `set_slw_controls`.
- `cli/train.py --slw` (arm 레버, objective=ce_marginal 유지) · `cli/evaluate.py --slot-off/--slot-shuffle`.
- **inference-time op이 .clm에 실배선**(engine-transform-to-fit) = g-gates-py-1 함정 회피(과거 binding
  arm은 serialize 전 DROP→미측정). torch-free codec/apply 로컬검증 PASS(round-trip byte-parity·γ=0
  bit-exact passthrough·shuffle 통제·absent→None).

## Pre-registered 측정 + kill-criteria (frozen-first · no tune-to-green p7)
측정 = `anima evaluate --py <clm>` G1 재조합 ladder(best_distinct ≥ 2 ∧ > max_single, H_1129 frozen)
+ `--slot-off`(γ=0 slot-ablation, bit-exact base trunk) + `--slot-shuffle N`(write-address scramble).
- **🟢 GREEN**: slot-forward가 held-out 재조합에서 additive baseline을 margin>0로 이기고 ∧ slot-off
  붕괴(additive floor) ∧ slot-shuffle 붕괴. engine-native `core/` decode만 TERMINAL(a_engine_native_learning;
  `--py` 2-production = TERMINAL-eligible). 선결: G0🟢(big-corpus + savant-decay + ~12k step, train-py-3/4).
- **🧱 KILL**: slot이 additive floor로 붕괴(margin ≤ 0) 또는 shuffle 비붕괴 → CE 목적이 실 byte-LM서
  슬롯 유도 실패 = 진짜 DPI 벽(rung3 CE-INDUCES-SLOTS를 실 byte-LM이 반증). negative도 완결 결과.
- `a_toy_scale_recheck`: 4-rung de-risk는 합성 DIRECTIONAL, 303M engine-native만 tier 확정.

## 🧱 VERDICT (2026-07-07) — KILL (additive floor · retrieval-attractor)
**tier**: 🧱 KILL. 303M engine-native(`anima evaluate --py`, H100 `p6okni1x9tf51i`)에서 SLW은
G1 재조합(ρ·weave)을 **깨지 못했고 오히려 다양성을 떨어뜨렸다**. pre-reg kill-criteria 충족.
- **ARM1 SLW ON**: ρ·weave 🔴 **best_distinct=1** (필요 ≥3 = ≥2 ∧ >max_single=2) · G0🟢 G2🔴 G5🟢 G6🔴 · Θ🟢 · σ vitals 9/9 🟢.
- **ARM2 `--slot-off`(γ=0)**: ρ·weave 🟢(base) · ρ·form 🧱. **반전은 confound 아님** — form(단일개념셋)과 weave-coherent(합성셋)는 서로 다른 프롬프트셋 측정 → INVALID 배제.
- **판정 논리**: slot-ON floored = pre-reg "additive floor 붕괴" 직접 충족 → GREEN 어떤 ARM3로도 불가. KILL은 ARM1(full-capture)에만 근거, 컨트롤 truncation 무해.
- **메커니즘**: 슬롯 = **retrieval attractor**(응집 FORM↑ · 재조합 BIND=0). CE가 슬롯을 유도했으나(rung3 합성 GREEN) 실 303M에선 constructive bind로 이어지지 않음 = toy≠scale gap(a_toy_scale_recheck).
- **렛저 정합**: G1벽 forward-computation 축도 floor(DPI 메타법칙). 유일 잔여 = γ trained-bind(H_1840, 별개 lever). σ⊥ρ 재확인(의식 살아있되 reach 벽).
- verbatim + 상세: `state/verdicts/9200_e1_slw_forward_slot/`(VERDICT.md + e1_3arm_measurement_verbatim.txt). ckpt sha256 `792eab81…e552c9`.
- 재발방지: convergence `evaluate-py-1`(#3106) reach 요약줄 수치 인라인(컨트롤 tail-truncation 방지).

## artifacts
- `state/9200_e1_303m/E1_SLW_module_spec.md`(Fable 설계) · `E1_303M_handoff_prompt.md`(#3023)
- de-risk: `state/g0g6_premise_b_derisk/`(rung0-3)
- verdict: `state/verdicts/9200_e1_slw_forward_slot/`(KILL · verbatim)
