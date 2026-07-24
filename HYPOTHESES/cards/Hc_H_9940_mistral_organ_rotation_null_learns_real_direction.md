# H_9940 · Mistral organ rotation-null: 결합은 **실재하는 방향**을 학습한다 — gate-off은 λ-경제학이지 organ 무능이 아니다

**한 줄:** H_9939 가 `rotation_null:0` 로 남긴 **결정적 통제**를 새로 배선한 `graft check --hf-model`
(#4527 HF 분기 + #4528~4530 device/dtype fix 3종)로 실행하니, 4bit Mistral-7B 의 학습된 codes 가
displacement-exact rotation-null 을 **z=+18.59 로 압도(PASS>q99, n=64)**. 즉 near-floor fit MI
(+0.0048 nats)는 organ 이 상태를 못 실어서가 아니라, **λ=1 목적함수가 그 실재하는 정렬 방향을 gate-off
밑으로 벌점**한 것이다. toy `trained57`(H_9937 z=+28~38)과 **같은 시그니처가 d=4096 7B 에서도** 난다.

- 계기: `anima-py graft check /home/summer/graft_mistral_s1.pt --hf-model
  mistralai/Mistral-7B-Instruct-v0.2 --rotation-null 64 --k 8 --state-gap 13 --p1-steps 2000
  --cont-len 32 --seed 1 --probes 2` (summer RTX 5070 · 4bit · seed 1). regime `no-corpus` · DIRECTIONAL.
- 신설 계기 = 이 카드가 배선한 것: `_check_hf_setup`(HFOrgan+GraftBridge 재적재 → codes 를 `_fit_hf`
  와 동일 재구성) · probes 는 subword 라 `organ.encode` · rotation-null 은 d=4096 용 thin-SVD
  `rotation_null_offsets`(D-exact O(d·r)). H_9939 가 이 통제를 못 돌린 이유(`_check` 에 HF 분기 부재)를
  #4527 이 해소, #4528~4530 이 never-run-on-HF 의 `.cpu()`·`.float()`(bf16)·`device=lp.device` 3종
  버그를 fix(`instrument-never-run-hides-multiple-bugs`).

## 결과 — 학습본이 displacement-exact null 을 압도 (rc=0)
| arm | 값 |
|---|---|
| **ROTATION-NULL** | **MI_trained=0.0104 bits · null(n=64) mean 0.0021 sd 0.0004 q95 0.0029 q99 0.0031 · z=+18.59 · PASS(>q99)** |
| SWAP | MI_swap=1.144 bits (ceiling log2 K=3.0) · acc 0.375 (chance 0.125) · perm_p=0.0010 |
| ABLATION | KL(ON‖OFF)=0.0487 bits vs KL(NOISE) q95=0.0131 · ratio=3.72× (gate is distinguishable from noise) |

rotation-null 은 노름·Gram·평균·실현변위 D 를 모두 보존하고 방향만 파괴하는 통제다 — 그걸 학습본이
z=+18.59 로 넘는다는 것은 학습이 codes 를 **기관의 민감한 방향에 정렬**시켰다는 뜻이지, 진폭/변위
artifact 가 아니다(H_9936/H_9935 가 걸러낸 그 병 아님).

## 판정 — 🟢 DIRECTIONAL: 결합은 실재하는 방향정렬을 학습한다 (4bit Mistral · null 압도)
- **H_9939 와 AGREES + EXTENDS, 모순 아님**: H_9939 의 arithmetic(step-50 loss 2.1450 > gate-off
  2.0794 ⟹ λ=1 에서 gate-off 최적)은 **목적함수**에 대한 판정이고, 이 rotation-null 은 **결합 품질**에
  대한 판정이다. 둘은 상보 — 결합은 정렬을 배웠으나(z=+18.59), 그 정렬이 λ=1 에서 켜는 값이 못 된다.
- **fable Q1(c) / sol two-sided outcome #1 확증**: near-floor 는 (b) organ 무능도 (a) 방향 부재도
  아니라 (c) 고칠 수 있는 목적함수 세(λ·L_common 세). MI/L_common 교환비가 toy 2.9 → 7B 0.68 로
  1.0 을 가로지른 것(H_9939)과 정합.
- **sol 의 kill 조건 미충족**: "정렬이 부재하면 frozen-LLM GRAFT 폐기" — 정렬은 실재한다(PASS>q99).

## 정직 경계 (no tune-to-green · a_toy_scale_recheck)
1. **DIRECTIONAL**: 4bit · 1 seed · `cont-len 32`(fit 의 64 아님) · Mistral ≠ 303M(terminal 은 거기서만).
2. MI_trained 절대값은 param 의존(같은 계기 tiny run k=4 서 0.0321, 여기 k=8 서 0.0104) — **신호는
   matched null 대비 z 이지 raw MI 아님**(`a_bound_the_measurement_exceeds_is_not_a_bound` 의 쌍대).
3. z=+18.59 < toy +28~38 — 7B 서 다소 낮으나 같은 PASS>q99 방향(스케일에 따라 채널이 얇아짐과 정합).
4. 이건 **결합이 방향을 배웠다는 통제**이지 "gate 를 켜면 이득"이 아니다 — **λ<0.68 이득영역의 존재는
   미측정**(H_9939 next-①). 이득영역 없이 정렬만 실재하면 "얇지만 실재하는, 목적함수가 안 쓰는 채널".

## 다음
① **λ<0.68 refit + rotation-null + fluency-price**(fable primary): 이득영역 존재 판정. DV = rotation-null
   지배 + fluency price ≤ 잡음, **MI↑ 단독 금지**(λ 가 MI 를 기계적으로 산다 · tune-to-green 방벽).
② **bf16 재측정**(양자화 경계 — H_9939 가 flag, 병렬세션이 fit 진행중이었음): rotation-null 을 bf16
   bridge 에도.
③ **303M `.clm` engine-native graft**(terminal 지점 · exchange-rate 곡선 toy 2.9 / 303M ? / 7B 0.68 의
   빠진 중간점 · 포팅 불필요, `anima-py graft fit/check` 존재).
