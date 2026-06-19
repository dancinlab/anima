# M4b 장기학습 결정 발사 — dec_undertrain 프로덕션 검증 (2026-05-28)

## 가설 (dec_undertrain 결정적 테스트)

MoE 디코더 mode-collapse(`decode=[1,1,...,1]`, distinct_experts=1, 2/5 FAIL) saga에서
네 가지 레버가 모두 탈출에 실패했다 — corpus-diversity(#1296) · routing/aux(#1315 A≈B) ·
head-capacity(#1315 d 64→256 무변화). $0 capacity-cliff micro-exp(PR #1314,
`.discoveries/decoder_collapse_undertrain.tape`)가 collapse를 **토큰-제시 예산(step/data
budget)**으로 재귀인했다: head-rank V*(d)는 기하급수적으로 자라 d=64는 V=151643에 충분한
rank를 가지나, 모든 기존 발사는 ≤200 token-step(V=151643의 1패스에도 한참 못 미침)을 썼다.
토이(V=64) 예측: **presentations ≫ V (~50 epoch)이면 탈출**.

본 발사는 이 예측의 프로덕션 결정 테스트였다 — d=64 고정, 전체 corpus, **epoch 예산만** 변화
(LO=1 · MID=12 · HI=60)시켜 탈출 임계 epoch을 핀하는 3-pod 병렬 sweep.

## 방법 (epoch-budget sweep, 3× H100 80GB SECURE 병렬)

- 고정: d=64, V=151643(실제 Qwen2.5-1.5B BPE · 151387 merges), E=2, h=256, n_layer=1,
  T=4, HARD top-1 routing. 단일 변수 = 토큰-제시 예산(M4B_EPOCHS).
- 사전등록 탈출 게이트(pod별): TTR≥0.30 ∧ LZ_norm≥0.50 ∧ distinct_experts≥2.
- 트레이너 `CORE/DECODER/train_v3_moe_longtrain.hexa`(857줄, mm-leak 수정 = per-step 버퍼
  hoist · epoch-driven n_steps · M4B_EPOCHS 권위화). cuBLAS = glue.c strong override
  (`hexa_cuda_available`→`_hx_cuda_runtime_available`, `-lcuda`).

## 측정 (verdict matrix)

**결과: 프로덕션 V=151643에서 sweep을 실행 불가 — 세 가지 hexa-lang 툴체인 블로커가
MID/HI(≫V-presentation pod)를 intractable로 만듦. 깨끗한 verdict matrix 미생산.**

H100 80GB SECURE pod에서 실측한 사실 (`state/m4b_longtrain_2026_05_28/BLOCKER_FINDINGS.md`):

| 블로커 | 측정 증거 |
|--------|-----------|
| **① BPE encode O(bytes×n_merges)** | merge-table LOAD은 O(1)(358ms · #1869 확인). 그러나 `self/ml/tokenizer_bpe.hexa get_merge_rank`는 151387 merge에 대한 **선형 스캔** → encode가 ~O(text_bytes × n_merges). 전체 2000줄 corpus(1.27MB)는 15.5분 @ 100% CPU에도 encode 미완료 · 100줄/63KB는 180s 미완료 · **24줄/6.6KB trim corpus만 tractable**(n_toks=6034). |
| **② cuBLAS gemv 깨짐** | `cuda_available()==1`(glue 정상 작동) 이나 expert gemv `[V=151643 × d=64] @ [d×1]`에서 `_hx_cuda_farr_matmul_gpu` → `cudaMemcpy C D2H failed: an illegal memory access` → handle -1 반환. GPU util/mem가 학습 중에도 0 유지. cuBLAS가 작동했어도 가속하는 것은 gemv 한 개뿐. |
| **③ O(V) per-step CPU 비용** | CPU step rate ≈ **0.26s/step**(1 epoch=1507 step이 401s에 미완료). step당 `mm_extract`가 [V×d]=9.7M 원소 expert weight를 토큰마다 fresh 버퍼로 복사 + V=151643 위 O(V) softmax/argmax/loss 루프가 지배. |

**Wall-time 귀결**(V=151643, 24줄 corpus, 1507 step/epoch, ~0.26s/step):

| pod | epoch | step | ~wall @0.26s/step | 실행가능? |
|-----|-------|------|-------------------|-----------|
| LO  | 1     | 1,507 | ~7분  | 가능 |
| MID | ~1500 (40×V pres) | ~2.3M | ~7일  | 불가 |
| HI  | ~7500 (200×V pres)| ~11M  | ~33일 | 불가 |

3-pod는 cuBLAS 미작동(GPU 0%)으로 idle-watchdog에 의해 외부 종료됨 — 깨끗한 결과 미수확
(LO조차 connection-drop으로 verdict 직전 SIGHUP). 모든 pod teardown 확인, 잔여 과금 0.

## 발견 (closed — 프로덕션-scale BLOCKED, 근본원인 핀)

토이(V=64)는 ~50 epoch 탈출을 예측했다. 이를 **프로덕션 V=151643에서 검증하는 것은
anima 트레이너가 아니라 hexa-lang 툴체인 한계로 차단됨** — BPE encode 복잡도 + 깨진 cuBLAS
gemv + O(V) per-step CPU 비용. 이는 cross-cutting 원칙(toy→production transfer 비보장)의
강한 사례다: 여기서 transfer는 **현 툴체인으로 검증 불가능**하다.

discovery tape의 모호한 "blocked-untested"를 **세 개의 구체적·근본원인-핀된·실측 증거를 가진
툴체인 블로커**로 격상시킨 것이 본 발사의 finding이다. dec_undertrain은 프로덕션에서
CONFIRMED도 REFUTED도 아니며 — **UNVERIFIABLE-AT-SCALE (toolchain-blocked)**로 닫힌다.

## a_runpod_inbox 후속 (hexa-lang 패치 대상)

1. `self/ml/tokenizer_bpe.hexa get_merge_rank` 선형 스캔 → hashmap(O(1) rank lookup),
   corpus encode를 O(text)로.
2. `self/cuda/runtime_cuda.c _hx_cuda_farr_matmul_gpu` [M=151643, N=1] tall-gemv shape의
   illegal D2H — out-buffer/grid 사이징 버그.
3. (선택) `v3_moe_arch` per-step `mm_extract` V×d 복사 제거 — 오프셋-aware gemv로 직접 참조.

## 산출물
- `CORE/DECODER/train_v3_moe_longtrain.hexa` — 트레이너(epoch-driven · mm-leak fix).
- `CORE/DECODER/state/m4b_longtrain_2026_05_28/{BLOCKER_FINDINGS.md, DISPATCH.md,
  pod_build_fire.sh, glue.c, podssh.sh, RUNNING_PODS.md}` — 발사 recipe + 블로커 실측.
- HF 업로드 없음 (모델 artifact 미생산 · negative/blocked = a_hf_autonomous 비대상).

provenance: github.com/dancinlab/anima · 본 결과는 #1296 + #1314 + #1315 saga의 프로덕션-
scale 후속이며, dec_undertrain 레버의 검증을 막는 툴체인 ceiling을 결정적으로 핀한다.
