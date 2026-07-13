# H_9290 NAT-ATOM — VERDICT: 🧱 NO-RESCUE (DATA-🧱)

**2026-07-13 · pod 44684279 (vast ssh3, RTX 4090) · anima-py 303M CLMConvMoE · engine-native**

## 결론
codec 형태소 원자성은 **자연-분포 held-out 술어 극성 접지를 rescue하지 못한다**.

| 지표 | codec_Mnat | raw-byte 기준(N2 #3372) | bar |
|---|---|---|---|
| held-out probe-acc | **0.3448** | 0.5517 | ≥0.65 |
| train_fit | 1.0 (프로브 유효) | — | — |
| shuffle floor | 0.4948 | 0.5138 | — |
| Δ vs shuffle | **−0.150** | +0.038 | ≥0.08 |
| **RESCUE** | **false** | — | — |

codec이 raw보다 **낮다**. train_fit=1.0 ∧ shuffle≈0.5 ⟹ 프로브 유효·held-out 전이만 실패(INFO-ABSENT).

## 방법 (reference-match)
- base 303M → reinit-embed → **CPT 16k on 자연 codec 코퍼스**(MORPH-2B로 인코딩한 NSMC 120k lines · **drill 無**).
- H_9289 `gt_step0_gprobe.py` 프로토콜 **verbatim**: frozen dump-hidden(d3784 penultimate) → 원자 mean-pool →
  L2-logreg(train P_grid 20 → test held-out P_nat 29). frozen 자산(gt_atoms·gt_prompts 1176 문맥) 그대로.
- **유일 차이 = tokenization**(raw vs codec). 그 외 동일 ⟹ 원자성의 인과 기여만 격리.

## 2×2 완성
| | 합성(drill) | 자연 분포 |
|---|---|---|
| raw utf-8 | XBIND 🟢 (H_9267) | NAT-CRACK 반증 🧱 (H_9286) · INFO-ABSENT (H_9289) |
| codec 원자성 | MORPH-ATOM 🟢 (H_9288 · 0.908≫0.617) | **NO-RESCUE 🧱 (이 verdict)** |

## 해석
- **원자성은 신호를 만들지 못한다.** 자연 부정 신호는 이미 얇음(`a0neg` d_nat=42.3/MB · NOT POWERED).
  tokenization은 데이터에 없는 접지를 창발시키지 못함. N2+G-PROBE+본 verdict 3중 정합.
- **H_9288과 모순 아님**: 원자성은 drill이 flip을 가르칠 때 held-out 재조합을 *가능하게* 한다(증폭기).
  가르치지 않으면 자연 분포만으로 접지가 설치되지 않는다(원천 아님).
- ⟹ **G1 자연 자발창발의 병목 = DATA**(신호 밀도·접지 채널), substrate/tokenization 아님.

## scope · cement 조건
1 seed(4302) · CPT 16k · custom harness · held-out 술어 극성 단일 construct. 음성 주장이므로 terminal cement엔
사전등록 TOST(Δ_eq·N_REQ 사전고정)가 필요(negative-claims-need-tost). 현 tier = 🧱 DIRECTIONAL-NEGATIVE.

## 인프라 (infra-wall-noneval · 측정과 분리)
2건의 pod 장애 후 clean 측정: (1) pod 44680852 = 1.5GB base.pt 업로드가 sshd wedge → 파괴·재렌트.
(2) `install_ma.sh`가 `/workspace/ma` 하드코딩 → `/workspace/na`서 조용히 실패(convergence `install-ma-sh-1`,
디렉토리-relative로 근본수정). 두 장애 모두 **과학 결과와 무관**; 본 verdict는 clean 완주 run에서만 나옴.

## 산출
gprobe=`~/anima-weights/morphatom/gprobe_codec_result.json` · 도구=scratchpad `gen_codec_natural.py`·
`morphatom_dumphidden.py`·`morphatom_gprobe_run.py`·`fire_natatom.sh` (+ `state/nbindg_grounding/gt_*`).
