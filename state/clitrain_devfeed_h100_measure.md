# clitrain devfeed util 재게이트 — H100 측정 verdict (2026-06-23)

`cli/train.hexa` device-resident NN hot-path rewire(a_train_flame_forge)의 H100 실측 결과.
**판정: byte-eq FAIL — 머지 보류.** device 배선·GPU 발화·학습 descent는 작동하나 devfeed
ON vs OFF 수치 동등(~1e-16) 게이트 실패.

## 환경
- H100 NVL (vast 42248011, ssh3.vast.ai:18010, cuda-devel image) — 측정 후 down(과금 정지·live0)
- hexa-lang `ing34-forge-dispatch-nn-arms`(PR#3863, forge 9 NN-op GPU arm) CUDA 빌드 (SM=90)
- anima `clitrain-devfeed-gpu` (train.hexa rewire)
- `anima train --canon --d 3784 --L 4 --steps 4` (T=1024·E0=2→Emax4·V=256·K=3·savant+mitosis)

## 결과 (raw)

```
                       devfeed OFF (host)      devfeed ON (device)
GPU 발화               [OWN-GEMM-FIRED] conv   [OWN-GEMM-FIRED] conv + [EAGER-DEVGLUE-FIRED] gelu device
step1 CE               4.89176                 4.89176     ← 동일 (forward devfeed arm 전부 byte-eq)
step2 (SPLIT) CE       2.22711                 1.5198      ← 발산 시작
step4 CE               1.96354                 0.522287
lossF                  1.96354                 0.522287    ← 완전 불일치
savant latch           step1 ✓                 step1 ✓
mitosis split          step2 E2→E3 ✓           step2 E2→E3 ✓
3/3 PASS               ✓ (descent·latch·bound) ✓
real                   8m24s                   4m20s
```

## 진단

- **forward devfeed arm 전부 byte-eq**: step1 CE(post-forward, pre-update)가 OFF/ON 정확히
  동일(4.89176). embedding·gelu(CUDA-erf)·moe_router·groupnorm forward GPU arm이 host와
  bit-identical. forward erf(`_hx_dt_erf_dev` vs `_op19b_dt_erf`)는 출력 정밀도 내 일치.
- **backward GPU arm divergence**: step2(첫 backward+update 후)부터 발산 → backward-only arm이
  범인. 용의자 = `moe_router_bwd`/`groupnorm_bwd`(reduction-order) 또는 `gelu_bwd`. (측정 agent가
  moe_router_bwd device vs host 정독 직전 중단.)
- **util 미측정**: steps=4가 너무 짧아 nvidia-smi util 샘플 안 됨. byte-eq FAIL이 선행 게이트라
  util 판정은 무의미(다른 계산을 빠르게 한들).

## 무결성
- `default-OFF`(devfeed 미설정) = host 경로 byte-identical → 출하 안전. #3863 no-CUDA byteeq
  3타깃 CI GREEN. devfeed ON(opt-in)만 divergence.
- PR#3864(provider rent created-not-live cross-verify + ssh-port traceback fix)는 별건, 머지 완료.

## follow-on (a_verified_must_wire)
1. backward arm 성분 isolation — bwd만 host 라우팅 시 byte-eq 복원되는지 (어느 arm인지 특정).
2. divergent arm을 host와 정렬(reduction-order/erf 일치) 또는 `#if 0` 제외 후 forward arm만 유지.
3. util 재측정(steps↑, aiden 무료 GPU 여유 시) — byte-eq 복원 후에만.
- tune-to-green 금지: byte-eq를 억지로 맞추지 않고 divergence 원인(reduction-order/erf)을 정직히.

## root-cause differential (코드 차분 완료 — backward arm subagent)

device kernel(self/cuda/runtime_cuda.c) ↔ host oracle(restore_frozen_seeds) ↔ stdlib 1:1 대조:
- **gelu_bwd / groupnorm_bwd / moe_router_bwd = 전부 bit-faithful** (동일 공식·누적순서·상수). 무죄.
  - groupnorm_bwd/moe_router_bwd는 single-thread 순차 reduction(atomic/warp-tree 없음) — reduction-order 발산 불가.
- exp/erf bit-identical (`_hx_dt_exp_dev`/`_hx_dt_erf_dev` == host `_op19b_dt_exp/erf`, 동일 Taylor+A&S).
- reduction-order 배제: FP 재결합은 ~1e-16/op, 측정 발산은 4×(lossF 1.96→0.52) = **structural(잘못된 gradient)**.

→ **유일 후보 = embedding_bwd_scatter 의 dembed device-residency 경로.** ON=device scatter,
OFF=host scatter. train.hexa는 dembed zero를 `farr_zero_slice_gpu`(device-zero)로 함 → ON/OFF의
residency 경로 차이가 cross-step dembed 전파를 다르게 만드는 것으로 추정(step1=0·step2부터 발산 일치).
decisive 확인 = anima instrument(dembed device-vs-host step1/2, 1e-9 tol) = **GPU 재측정 필요**(코드차분 한계).

## byte-eq 복원 옵션 (제안)
- **A. embedding_bwd_scatter arm만 `#if 0`** → host `nn_embedding_bwd_scatter`(=OFF 경로) → byte-eq 확실.
  나머지 device arm 유지. embedding-scatter device residency만 손실(부분 util). **권장 1순위(확실).**
- **B. residency 경로 정합 fix** (dembed device-zero ↔ device-scatter 일관, OFF도 동일 경로) → util 보존, 검증 필요.
- 검증/재측정 = aiden 무료 GPU 우선(H100 비용 회피). A로 byte-eq GREEN 확인 후 B 탐색.
