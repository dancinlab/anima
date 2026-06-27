# H_1640 CLS-SEP-COMPLETE (303M) — frozen pre-registration

> 생물 렌즈 #1 (PRIMARY) — 해마 보완학습계(CLS)의 **pattern separation(직교화) + pattern
> completion(부분→전체 복원)** 을 G1 재조합 레버로. arxiv **2507.11393**(CLS sep/completion NN,
> 2025) + Marr-Albus(expand+sparsen+decorrelate, biorxiv 108431). a_no_llm_frame_trap 정합:
> 모든 anima 돌파는 생물 렌즈에서 — 해마 계보(H_1227 immune-memory · H_1288 eviction)의
> **미탐색 축 = 저장이 아니라 *재조합 재료의 직교화***.

**가설:** anima 의 G1 재조합벽은 트렁크가 **합칠 개념들의 표현을 분리(직교화)하지 못해서** 생긴다.
A 와 B 가 penultimate 표현에서 엉켜 있으면(entangled) 모델은 둘을 *구별되는 재료*로 잡고 합성할
수 없다. 해마 DG 의 **pattern separation(직교화·sparsen)** 으로 재료를 분리하고, CA3 의
**pattern completion(부분 cue→전체 복원)** 으로 합성을 가능케 하면 G1 재조합이 floor 위로 올라온다.

**핵심 질문:** CLS separation(±completion) 보조 objective 가 `ce_marginal`(표준 CE baseline)
대비 held-out 재조합(G1)을 *올리나*?

## 구현 축 — OBJECTIVE/표현, **곱셈 readout 아님** (직전 세션 확정 교훈)

직전 세션 확정: 곱셈 **binding operator 를 readout 에 끼우면 floor**(exp3 bind NOT-SUPPORTED,
[[exp3-bind-g1g6-engine-native-floor]]) AND non-additive readout 은 `.clm` 직렬화 BLOCKED.
→ CLS 는 **trunk penultimate(post `norm_out`, pre `readout`)** 에 거는 **2 보조 손실**로 구현하고
**production additive readout(`Conv1d d→V`)은 세 arm 전부 동일**하게 유지한다:

- **`L_sep`** (분리) = penultimate 코드의 채널 간 **off-diagonal correlation energy → 0**(직교화)
  + 약한 L1 sparsity(Marr-Albus sparsen). DG separation 압력을 재조합에 들어가는 *그 표현*에.
- **`L_complete`** (완성) = penultimate 채널의 일부를 마스킹(부분 cue)한 뒤 작은 linear head 가
  **전체 코드를 복원(MSE)**. CA3 autoassociative reinstate. head 는 **학습 전용**(직렬화 전 폐기)
  → `.clm` 은 production additive 모델과 아키텍처-동일.

readout 이 additive 이므로 **세 arm 전부 `.clm`-직렬화 가능 → engine-native G1 by-construction
열림**(exp3 binding 과 달리 BLOCKED 아님). torch-side metric = DIRECTIONAL monitor 보조
(a_engine_native_learning); `.clm` export → `anima eval`/`clm_decode.py` G1 이 terminal.

## 3 arm — trunk·데이터·step·seed·readout 동일, **CLS objective 만 다름**

세 arm 은 **동일 trunk init seed · 동일 데이터 stream · 동일 step · 동일 production additive
readout**. 단일변수 = CLS 보조 objective.

- **`ce_marginal`** (baseline / discriminating control): 표준 CE next-byte 만. CE 는 separation/
  completion 을 보상 안 함 = **대조군 내장**(가설의 null).
- **`cls_sep`**: CE + λ_sep·`L_sep`. separation 단독.
- **`cls_full`**: CE + λ_sep·`L_sep` + λ_comp·`L_complete`. separation + completion.

## Arch — 현 production 303M CLMConvMoE (clm303_clean / H_1602 동형)
trunk = `CLMConvMoE` (byte V=256, **L=4 · d=3784 · E0=2→Emax=3 mid-split**, K=3,
dilation=min(2^l,512)), savant(golden-zone inhibition cusp anneal) + mitosis(E2→E3) ON =
`cli/train.py --canon` 동형. 4-cell register corpus(`a_chat_registers`, ko/en × 일반/SNS)
proportional 샘플, val_frac=0.05. trunk init·mitosis·savant·corpus stream·step 전부 arm 간 동일.

## FROZEN 하이퍼 (실행 전 사전등록 · tune-to-green 금지 · p7/c9)
- `LAMBDA_SEP = 0.1` · `LAMBDA_COMP = 0.1` · `SEP_SPARSITY = 0.01`(L_sep 내부 L1 sub-weight)
- `COMPLETE_MASK = 0.5`(완성 cue 마스킹 채널 비율) · `COMPLETE_HID = 256`(완성 head 폭, 학습전용)

## FROZEN bars (사전등록 · tune-to-green 금지 · p7/c9)

**주 측정 = G1 재조합 (a7b_pass / H_1129 def VERBATIM):**
어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2` **AND** `> max_single` **AND** coherent(kwr≥0.50).
seed-robust {7, 4302, 4303} majority ≥ 2/3 (`g_eval_g1_multiseed`).
- **engine-native (terminal)** = `.clm` export → `anima eval`(또는 `clm_decode.py` 2-production)
  의 G1 measure. 세 arm 전부 additive → engine-native by-construction 열림.
- torch-probe gauge(`gauge_lib`) = DIRECTIONAL monitor only (a_engine_native_learning), 보조.

**보조 측정 (공정·dt_ln-immune):** 4-cell held-out val CE(`F.cross_entropy`, dt_ln 무관) —
DESCENT(val_CE < ln256=5.545) 무결성 + arm 간 일반화 대조. ce_marginal 도 4/4 DESCENT 기대(무결성
가드 — overfit 이면 전 arm 무효, a_clm_gen_pipeline held-out 게이트).

## 반증조건 (FALSIFY)
- **cls_sep / cls_full 의 engine-native G1 ≤ ce_marginal G1** (seed-majority) → CLS separation/
  completion 은 G1 레버 아님 = **NOT-SUPPORTED**(objective-lever census 에 추가, a_break_the_wall
  class-d 후보). H_1602 objrun 결과와 합쳐 "어떤 objective 도 G1 안 엶"이면 더 강한 천장 증거.
- **어느 arm 이든 held-out 4/4 DESCENT 실패** → 무결성 FAIL(overfit/굶주림), G1 verdict 무효 →
  코퍼스/step 재점검 먼저(천장 아님, class-(a)/(e)).
- **CLS arm 이 G1 올리되 held-out CE 가 ce_marginal 보다 *나빠짐*** → separation 이 일반화를
  희생(trade-off) → 정직히 보고(은폐 금지 c9), G1 lift 의 scope 를 명시.

## 측정 절차 (engine-native terminal)
1. 각 arm `.clm` export (additive, by-construction decodable) — 직렬화 직후 `clm_decodable` 확인.
2. held-out DESCENT 게이트: `verify_clm_v2.py descent <clm> <heldout> [train]` 4-cell 4/4 (math.log mirror).
3. `anima eval <clm> --corpus <4cell> --gen 80` → G0-G6 engine-native(`g_eval_g1_multiseed`).
4. arm 간 G1 대조(cls_sep/cls_full vs ce_marginal). seed {7,4302,4303}.

## ckpt 회수 (a_fire_recover_complete)
torch `.pt` + `.clm` + summary.json + 로그 전부 teardown 전 pull. `.clm` 없으면 engine-check 영구 불가.
