# H_9118 — G1 해마 hetero-associative retrieve-into-context lane

> **tier:** 🧱 MOUTHFLOOR (engine-native own-GEMM 303M) · **wired:** engine-native (🧱 = wire 불필요, GREEN 아님)
> **slug:** `g1_hippocampus_lane` · **date:** 2026-07-03

## 가설
G1 재조합 벽이 정보 *접근* 문제라면, 해마 hetero-associative retrieve로 두 개념쌍의 off-cue 파트너 D를 context에 주입하면 mouth가 composed novel-only를 max_single 위로 올릴 것이다(retrieval-augmentation이 재조합 벽을 연다).

## 방법 (engine-native)
- **live op**: `core/hippo_retrieve.hexa`(conjunction-key hetero recall, kosmos cosine) → `hippo_retrieve_texts`로 seed 개념쌍 key → `.kosmos` anchor의 off-cue D 회수 → context 주입 → **frozen 303M mouth `gen_auto_ideate_W`(own-GEMM)** decode → echo-guard novel-only 채점.
- **배선 표면**: `hippo_g1_eval.hexa` (live core decode `.hexa`, grep-clean: torch/numpy/gauge_lib 0). readout/trunk 미터치.
- **own-GEMM 실측**: `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path` + `[EAGER-DEVGLUE-FIRED]` CUDA GELU, cuda_available()=1, GPU util 83%, NVIDIA L40S.
- **ckpt**: g1_realign.clm sha256 `7222554f25d5baccd3ffed56f6345642bed6269efa87c392283630c99de209a3`, gen=40 FROZEN, bar≥2.

## 결과 (verbatim, `state/g1_hippocampus_lane/engine_native/hippo_verdict_ownGEMM.log`)
```
회수(hippo_retrieve): 4/4 정확 —
  ocean+engine→harvest · forest+music→voyage · ocean+music→furnace · forest+engine→archive
  composed(BIND) novel-only = 0/4
  max_single(ECHO)          = 0/4   (baseline)
  SCRAMBLE novel-only       = 0/4
  single-parent leak        = 0
  gate: composed>max_single (false) AND BIND>=2 (false) AND scramble-collapse (false) AND leak=0 (true)
  VERDICT: 🧱 MOUTHFLOOR — hippo retrieve does NOT lift novel-only above baseline
```
BIND arm 예시: `novel(harvest)=0 cont: "The last weeks have been called."` (주입된 harvest 무시, seed echo/drop).

## verdict
🧱 **MOUTHFLOOR (engine-native)** — 해마 retrieve가 off-cue D를 **4/4 정확히 회수**해 context에 주입해도, frozen 303M mouth가 injected D를 **BIND 안 하고 seed를 echo/drop** → composed novel-only=0/4 = max_single=0/4. **retrieval-augmentation은 G1 재조합 벽을 못 연다.**

## 함의 (재분류)
G1 벽을 *retrieval/coverage/data 문제 → in-context 결합-생성 operator 문제*로 **재분류**하는 결정적 증거 — access(4/4)와 binding(0/4)을 분리해 retrieval-augmentation이 **틀린 처방**임을 증명. `state/g1_growwindow_remeasure`(window 열어도 echo)와 합쳐 (c)decode-window·(a)access축을 동시 소거 → 남은 원인 = **(b) objective floor**(CE-echo가 novel-composition 학습 안 함). 진단+레버 사전등록 = `state/g1_mouthbind_lever_analysis/PREREG.md`.

## 선행/관련
- H_1459 retrieval_bind (🧱 torch DIRECTIONAL) → 본 H가 engine-native own-GEMM으로 확정 승격.
- 남은 미측정 레버 = trunk recomb-objective(H_1602/1840, 진행 중) + trained bind-lane(H_1282). readout-bind(H_1812/1816)는 전수 🧱.

## artifacts
`state/g1_hippocampus_lane/` (DESIGN.md · SMOKE_RESULT.md · engine_native/hippo_g1_eval.hexa · engine_native/hippo_verdict_ownGEMM.log)
