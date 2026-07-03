# H_9121 — G1 objective-floor escape 사전등록 (CE-replace × TPR-invariant)

> **tier:** 🧱 **FALSIFIED-CEILING** (escape 공간 DRY · **terminal by construction**) — escape 전 칸(A11 TPR/HRR bind + contrastive-replace · coverage-density · **CE-deleted TPR-forward-slot**) engine-native mouth-gen 전수 floor (pod43727405 + pod43736708, 상세 [[H_9120]]) · **wired:** N/A (배선 안 함 — FALSIFIED escape는 production 미배선, `a_verified_must_wire`)
>
> **최종 (마지막 칸 닫힘 · WIRE_SPEC v0.3 BUILT+MEASURED, pod43736708):** 이전까지 유일 미측정이던 **CE-deleted TPR-forward-slot**(WIRE_SPEC 5단계: CE-DELETED InfoNCE + `out[t]=Σ_r S_r·(yn[t]⊙roles[r])` R=2 fixed-orthonormal roles + CLMT v0.3 serializer + `core/decode.py` bind_type=3)이 **빌드+학습+engine-native `--py` 채점**됨 → **CLM 0/5 ∧ ByteGPT(G0🟢 h1129c) 0/5 = FALSIFIED-CEILING, terminal_flip=FALSE**. TPR readout numpy↔torch byte-exact parity **0.0e+00**. **★ terminal by construction(신규):** R=2 fixed-orthonormal-role TPR은 `Σ_r S_r·(yn⊙roles_r)=(Σ_r S_r·diag(roles_r))·yn=W_eff·yn`로 **증명 가능하게 선형** → 표준 선형 byte readout(=H_9120 floor)과 **동일 천장 by construction**. engine-native 0/5가 증명 확증. 자유변수(InfoNCE=H_1602 floored·factored-init bias)도 미상승 → objective-floor CONFIRMED-TERMINAL, **마지막 escape cell 닫힘**.
>
> **직전 최종:** A11 signature-decode 5/5 REACHABLE(torch)가 실 303M byte mouth `anima evaluate --py` 채점서 **전수 floor**(cbind 0/1·cnce 1/1·cov 1/1, 전부 G0🟢) = **synthetic REACHABLE이 autoregressive mouth-generation으로 transfer 안 됨**(a_toy_scale_recheck 실증). ckpt `~/anima-weights/g1_escape/{cbind_en,cnce_en,cov_en}.bin` + `~/anima-weights/g1_a11tpr/{a11_tpr.clm,a11_tpr_bg.bin}`. 상세 = `state/g1_objfloor_escape/A11_engine_native/RESULT_tpr_wire.md`.
>
> **A11 실행 결과 (a2eebb91 · $0 aiden RTX5070):** ledger-FRESH(H_1441/1464 G6-noslot·H_1813 TPR-under-CE·H_9120 additive와 distinct). real deep conv byte trunk(production CLMConvMoE E2/L1 d768 7.3M, contrastive-replace end-to-end no-CE, held-out 20% novel-pair) 5 seed: **TPR HIT 5/5** margins +99~108·reach_novel 1.0·scramble≤0.02·InfoNCE→0 vs **ADD HIT 0/5**(all neg). → **floor=ARCHITECTURAL 확증**(ADD floors same objective)·**CE-basin=trap**(E2 TPR-under-CE floored). **CE 제거 + TPR slot 동시 = held-out recombination 도달** = toy가 free-lookup artifact 아님(real trunk survive). 정직(a_toy_scale_recheck·a_engine_native_learning): torch=DIRECTIONAL(H_9120 objective-floor terminal NOT flipped)·synthetic corpus(roles orthonormal→per-slot readout by-construction=escape 가설 자체)·natural-corpus production G1 미주장. **terminal follow-on = engine-native**: TPR forward-slot을 `core/clm_decode.hexa`+serializer 배선→real corpus contrastive-replace 학습→`anima evaluate --py` 채점. artifacts `state/g1_objfloor_escape/A11_TPR_contrastive/`.
>
> **결과 (workflow wee6usdpr · $0 cost-gate 유지):**
> - **Escape-1 (CE-replace 단독)** = **TOY-AT-FLOOR-SKIP** (numpy N=24 D=96 held-out split, 5/5 seed): ADD arch(no-slot) margin=−0.47·reach=0 AT-FLOOR vs **TPR arch(slot) 동일 objective margin=+3.30·reach=1.0 REACHABLE** → **floor는 objective 아니라 ARCHITECTURAL 확증** (contrastive 단독은 슬롯 없으면 INERT). H_9120 additive-FALSIFIED + [[H_1816]] 정합. 303M 학습 스킵(cost-gate).
> - **Escape-2 (TPR 단독, CE)** = **FALSIFIED**: TOY REACHABLE(unbind 1.0 vs additive 0.242, ablation causal)이나 = CE-basin toy-overstate regime(`a_toy_scale_recheck`, H_6112 numpy 0→1.0 vs real 0→0.022). **engine-native 303M ledger가 이미 FALSIFIED**: [[H_1813]](TPR expert-weight reparam, CE, --py) NOT-SUPPORTED at-floor best_distinct max1<2 · H_1623 frozen clm303 mult-bind FAIL 0/3 → <4/5. CE가 TPR slot을 compositional하게 안 씀(INERT-under-CE). 이 escape = H_6123 DUP-WALLED. G1 천장 HARDENED.
> - **∴ 결정 압축**: E1이 floor=architectural 확증, E2가 TPR-under-CE 기각 → **남은 유일 칸 = A11(TPR slot × contrastive-replace _동시_)**. E1 side-probe가 A11=TOY REACHABLE(margin+3.30) 실증했으나 303M 미측정(toy-overstate 위험). H_9120 directional-terminal 유지(A11 미측정이라 confident 아님).
> **slug:** `g1_objfloor_escape` · **date:** 2026-07-04

## 배경 — [[H_9120]] directional-terminal에서 압축된 escape 공간
G1 objective-floor = **directional-terminal**([[H_9120]], numpy A.novel=0이나 no-slot 아키텍처 위 objective만 측정). Fable 2발산(b9l75vja2 벽돌파 + bmcmti1pb fleet-full)이 escape 공간을 **정확히 2칸**으로 압축 — basin-preserving 4렌즈(readout·objective-additive·retrieval·coverage)는 각각 DPI-INERT / EXP-1 🧱 / [[H_9118]] 🧱 / [[H_6190]] ECHO-ONLY로 engine-native 원리 기각.

**objective-basin 메타법칙 (DPI의 learning-축 특수화):** CE는 echo(최단경로)를 basin 전역최소로 보상 → novel 결합은 saddle 너머. additive/readout/retrieval은 전부 **basin-preserving**이라 최소를 못 옮긴다. 외부 수렴(arxiv 30편): objective+정규화 > binding-operator > scale, neurosymbolic만 DPI를 구조적으로 깸(비-cheap).

## escape 후보 2 (non-basin-preserving · census 자가검증 통과 · cost-gated)
- **Escape-1 (CE-replace)**: CE를 *replace*하는 contrastive/energy trunk objective(echo=명시 negative, non-basin-preserving). EXP-1([[H_9120]])이 닫은 건 *additive* aux; **replace는 미측정** — 결정 구분(재포장 아님).
- **Escape-2 (TPR-invariant)**: TPR(Smolensky tensor-product)/binding-slot을 mouth forward **아키텍처 invariant**로 hard-wire(objective 아님 = [[H_1816]] additive 붕괴 우회, DPI 우회 유일 비-cheap 경로). objective 형태면 H_1816로 기각, **순수 forward hard-wire만** escape.
- (기각: Escape-3 tension-loop = H_1834/1837 재포장 → 자가검증 기각)

## frozen 예측 (측정 전 사전등록 · bar 고정 · tune-to-green 금지)
- **PRED-E1**: contrastive/energy *replace* objective + held-out 조합 split(SCAN/COGS) 재학습 `.clm` → engine-native G1 `A.novel≥2 ∧ >max_single ∧ SCRAMBLE≤1`이 **≥4/5 seed HIT** → Escape-1 PREDICTIVE. 미만 → objective-floor가 replace에도 성립=천장 강화.
- **PRED-E2**: TPR forward-invariant hard-wire `.clm`(CE 불변) → 동 bar **≥4/5 HIT** → Escape-2 PREDICTIVE. 미만 → architecture도 CE-basin에 삼켜짐=천장 강화.
- **NULL**: 둘 다 MISS → objective-floor는 (additive+replace+architecture) 전 학습축 성립 = **진짜 confident 천장**, 남은 건 non-learning 경로(외부 consequence loop = G1 재조합축 밖).

## 실행 (cost-gated · explicit-go 대기)
303M pool 학습(summer/aiden or 렌트 GPU, explicit-go). TOY 판별기(mini $0) 선행 → CRUX A00–A11 2×2(slot × signal). 채점 = `a_eval_py_canonical`(--py) or engine-native. L3 하네스 `hippo_g1_eval.hexa` 재사용. garble은 G0🟢-gate로 폐기(L4 혼재 방지).

## 정직 수렴 (c9)
**(i)-우세 with (ii)-잔존**: basin-preserving 4렌즈 전수 engine-native 기각 + 메타법칙이 전부 삼킴 = **매우 강한 천장**. 단 non-basin-preserving escape 2개가 census 자가검증 통과·미측정·cost-gated로 정직하게 열림. **L3 MOUTHFLOOR + L4 FALSIFY가 escape 공간을 이 둘로 압축한 결정 증거.**

## engine-native 판별 시도 (wrno7ys0s · $0 · 둘 다 INFRA-BLOCKED but A11 강화)
**A11 natural-transfer 확증 (DIRECTIONAL, terminal NEITHER flip NOR cement):**
- real deep conv byte trunk(d768 7.3M)을 **natural corpus**(overlapping ko/en words, synthetic orthonormal 아님)로 contrastive-replace 학습, 5 seed: **TPR HIT 5/5** margin +34.2/+32.6/+35.7/+28.6/+36.0·reach_novel 1.0·scramble≤0.02 vs **ADD 0/5**. margin이 synthetic +99 → natural +28~36으로 떨어지나 **강하게 positive 유지 = NATURAL-TRANSFER-SURVIVES**.
- 함의: `a_toy_scale_recheck`의 "synthetic clean-corpus artifact" 우려를 **kill**(natural transfer 실패 안 함) → FALSIFIED-CEILING 미획득. 단 torch·signature-decode readout(roles orthonormal by-construction)이라 engine-native 아님 → PREDICTIVE-ESCAPED도 미획득. **terminal decider = 실 .clm(TPR forward-slot)+contrastive-replace 학습→`anima evaluate --py` mouth-generation G1 = INFRA-BLOCKED**(aiden reboot·summer no-torch·303M pod babysit 불가). WIRE_SPEC.md(미적용 배선 spec — 학습 ckpt 없이 배선=dead code, `a_verified_must_wire`).

**coverage-density (H_6185 recipe) = INFRA-BLOCKED (별개 lever, un-refuted):**
- corpus 합성 완료(combination-coverage: N=40 concepts·25% coverage·600 reps/pair·en 3.0MB+ko 2.5MB·held-out 엄격 0). RF L4→8 config 배선(cli/train.hexa L_canon 8). `fire_l8_canon.sh` fire-ready(warm-FT h1129c + --py --L8 + --py G1 judge).
- 2 infra wall: (1)303M heavy-GPU no-host(summer high-load·aiden reboot·24GB+ pod=explicit-go) (2)$0 L8 engine-native smoke가 anima full-stack build wall(cli/anima.hexa forward_model codegen 버그=전체 --py 깨뜨림 → 서브 수정했으나 arm64 linker `_main` undefined=stale hexat toolchain). **infra-wall-noneval**: 미측정=verdict 아님, coverage-density는 DISTINCT un-refuted lever(staged·fire-ready). 24GB+ free host에서 fire_l8_canon.sh 발사 시 결정.

## artifacts
- `state/g1_objfloor_breakwall/BREAKWALL.md` (b9l75vja2 벽돌파), `FLEETFULL.md` (bmcmti1pb research→implement→abstract→falsify)
- 상위 verdict: [[H_9120]] (L4 recomb-objective FALSIFY → directional-terminal)
