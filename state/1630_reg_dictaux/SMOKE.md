# CPU/GPU 스모크 로그 — H_1630 (파이프 검증 only, 능력 측정 아님)

> $0 단계. 능력 verdict 아님 — (a) 학습 1-스텝 돌아감 (b) `.clm` 직렬화 + clm_decodable=True (c) 엔진-네이티브 g_gates 측정 파이프 연결됨, 세 가지만 확인. 모든 lever arm 코드경로 발화 확인.
> mac 에 torch 없음(numpy 2.4.6 만) → torch 스모크는 pool **summer**(RTX 5070, torch 2.11.0+cu130, cuda True)에서. mac swap 위험 회피(heavy-anima-eval-pool-not-mini).

## tiny config
`--steps 4 --d 16 --L 2 --seq-len 32 --batch-size 2 --no-mitosis --dbes` (synthetic corpus → val_CE=nan 정상; 코퍼스 없는 파이프 검증).

## (a)+(b) 학습 1-스텝 + .clm 직렬화 — 6/6 arm PASS (summer GPU)

| arm | 단일변수 발화 증거 | step4 CE | .clm | clm_decodable |
|---|---|---|---|---|
| ce_marginal | (baseline) wd=0.0162 | 5.61873 | 23578 B | **True** |
| n6_grok | N6 band wd=0.0325 (=baseline×2.0) | 5.61837 | 23578 B | **True** |
| n7_dictaux | `dict_recon=1.026 dict_sparsity=0.216` 발화 | 5.61876 | 23578 B | **True** |
| **n6n7** | wd=0.10 band + `dict_recon=1.049→1.025` 하강 | 5.61851 | 23578 B | **True** |
| n8_jamo | `jamo_ce=3.116` 발화(자모 초성-class aux) | 5.61916 | 23578 B | **True** |
| n1_tlora | TLoRA fold `delta_norm=0.00000`* | 5.61873 | 23578 B | **True** |

\* TLoRA `a` 는 zero-init(델타=a@b=0 at init) → 4-step·tiny-lr 에서 델타 ≈0 = identity 보존(정상). 실 303M 학습에선 gradient 로 델타가 자라며, fold 후에도 production additive weight 로 직렬화되어 engine-loadable 유지. (스모크는 "fold 경로가 깨지지 않음"만 검증.)

- N3 DBES 진단 전 arm 발화: `usage_entropy_norm≈0.94, n_active_experts=2` (E2, collapse 아님).
- N6 가 baseline 대비 wd 를 실제로 2배(0.0162→0.0325) 키우는 것 확인 = 단일변수 분리 성립.

## (c) 엔진-네이티브 측정 파이프 연결 — PASS (summer)

`python3 core/g_gates.py state/1630_reg_dictaux/ckpt/smoke_n6n7.clm --gen 8`:
```
ANIMA G0-G6 — py production engine (core/g_gates.py)  gen=8
G0 COHERENCE     pass=True  n_coherent=5/5
G1 RECOMBINATION pass=False  best_distinct=0   (4-step toy = 예상대로 floor)
G6 IDEATION star pass=False  dist=5  fals=0
G4 PROVENANCE    sha256=f5ca28d5… bytes=23578 mouth=clm
CLOSURE a7b_pass = FAIL
detector calibration (advisory >=8/10): 10/10
```
- `core/g_gates.py` = torch-free(numpy decode via `core/clm_decode.py`) = **TERMINAL-eligible 엔진-네이티브** 경로. smoke .clm 을 실제 로드·디코드·G0-G6 채점까지 end-to-end 연결됨 확인.
- G1=False/G6 fals=0 은 4-step toy 의 당연한 floor(파이프 검증이지 능력 아님). 능력은 303M GPU.

## grep self-check (a_engine_native_learning)

`grep -nE 'gauge_lib|import numpy|g6_common' state/1630_reg_dictaux/*.py` → **빈 출력(RC=1, clean)**.
- trainer.py 의 torch import 는 *학습 루프 전용*이고, 이 파일은 **G1/G6 verdict 를 계산하지 않는다**(1602 베이스가 끼웠던 `gauge_lib` 토치-probe 를 제거). verdict 는 오직 공인 torch-free `core/g_gates.py` 로. → DIRECTIONAL 오염 0.

## 정직 메모
- 스모크는 **능력 측정이 아니다.** G1 lift/G6 fals/held-out DESCENT 의 실제 verdict 는 303M GPU 학습 후 엔진-네이티브 재측정(`LAUNCH_303M.md`).
- mac CPU 단독으론 torch 부재로 불가했고, 정직히 pool summer GPU 로 옮겨 6/6 arm + 측정파이프 전부 green 확인.
