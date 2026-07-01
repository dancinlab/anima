# cli/ — anima CLI 진입점

**목적:** anima 의 진입점 모음. 추론/평가 진입(`anima.hexa`, evaluate·serialize·train 은 서브커맨드) + production 트레이너(`train.hexa`). py 진입점 중 `anima.py` 는 2026-06-28 폐기; **`train.py`·`evaluate.py` 는 canonical py 학습/측정 진입점**(`anima train --py`·`anima evaluate --py`)으로 유지 — hexa 트레이너가 GPU-util fix 중이라 py 가 현재 작동 학습 경로. 루트 `CLAUDE.md` 의 scoped 보강 — 충돌 시 루트 우선.

## 핵심파일

| 파일 | 역할 | verdict 자격 |
|---|---|---|
| `anima.hexa` | **단일 추론/평가 진입점** — `anima chat` · `anima evaluate <ckpt> [--py]` (L230 `argv[0]=="evaluate"`→`anima_evaluate_mode`→ `--py`?`cli/evaluate.py`(py 2-prod numpy):`cli/evaluate.hexa`→`g_eval_all`) | 엔진-네이티브 terminal |
| `anima_chat_cli.hexa` | 대화형 채팅 REPL helper | 엔진-네이티브 |
| `eval_pod.sh` | GPU pod 원격 측정 발사·회수 one-liner (`cli/eval_pod.sh <pod_id>`) | — |
| `train.hexa` | **production canonical 트레이너 (hexa-native)** — SAVANT/MITOSIS/4셀/held-out val/descent 통합 (`a_train_flame_forge`); 현재 GPU-util fix 중(#2598/#2600 CPU-scalar-bound) | 엔진-네이티브 |
| `train.py` | **canonical python 학습 진입점** (`anima train --py`) — torch Lane-P CLMConvMoE + SAVANT/MITOSIS 레시피 + H_1640 `--arm {ctrl,tlora,tlora_dict,tlora_jamo}`×`--objective {ce_marginal,infonce,contrastive_equilibrium,predictive_info,constructive_bind,composed_nce}` compositional 레버 매트릭스; `evaluate.py`(canonical py eval)와 대칭 | DIRECTIONAL(torch-side) → `anima evaluate --py` 로 `.clm` engine-native terminal |

> **`cli/train.py` = canonical python 학습 진입점**(`anima train --py` → 이 파일), `cli/evaluate.py`(canonical py eval)와 대칭. torch Lane-P CLMConvMoE 를 GPU-bound 로 학습(SAVANT+MITOSIS 레시피 + H_1640 arm×objective compositional 레버, 마지막 3개 objective=predictive_info·constructive_bind·composed_nce = 새 G1 trunk-objective 레버) → `.clm` v0.3 직렬화. hexa 트레이너 `cli/train.hexa` 가 GPU-util fix 중(single-thread CPU-scalar-bound)이라 py 가 현재 작동 학습 경로(`a_clm_gen_pipeline`: "Lane-P torch = REFERENCE + bridge, forge is the PUBLIC production trainer"). torch-side CE/gauges = **DIRECTIONAL only**; TERMINAL verdict = 직렬화 `.clm` 을 `anima evaluate --py <clm>` 로 engine-native 재측정(`a_engine_native_learning`). 실사용은 `--py` 경유(`--py` 없는 `anima train` 은 여전히 `cli/train.hexa` 로 디스패치).

## 규칙

- **`anima evaluate <ckpt>` = canonical G0-G6 단일진입 (`a_engine_native_learning`)** — generator L3 mouth(`gen_auto_ideate`) → G0-G6 엔진-네이티브 채점. 서브커맨드는 `evaluate`(코드 `argv[0]=="evaluate"`), `eval` 아님. per-gate 파이썬 하네스·ad-hoc decode 우회 금지.
- **`anima evaluate --py <ckpt>` = py 2-production 측정 경로 (`a_engine_native_learning` 2-production)** — `--py` 플래그면 launcher 가 hexa det-eval(`cli/evaluate.hexa`, OWN-GEMM fp64) 대신 **`cli/evaluate.py`**(torch-free numpy `g_eval_all`)로 G0-G6 채점한다. 동일 frozen bars·byte-parity 라 **terminal 자격 동일**(2nd-class 미러 아님). 용도 = 큰 ckpt(303M+)가 hexa bump-allocator fp64 det-eval 에서 OOM 죽을 때 (numpy 는 decode 당 메모리 free → 측정-무거운 풀 eval 에 강함). `--py` 는 launcher 가 consume(strip)해 `evaluate.py` 엔 `<ckpt> [--corpus …] [--gen N]` 만 전달. anima.hexa/anima.py 양 launcher lockstep.
- **`anima train --py` = canonical py 학습 경로 (`a_clm_gen_pipeline` Lane-P bridge)** — `--py` 플래그면 launcher(`anima_train_mode`)가 hexa `cli/train.hexa` 대신 **`cli/train.py`**(torch Lane-P CLMConvMoE + SAVANT/MITOSIS + `--arm`×`--objective` compositional 레버)로 GPU-bound 학습 후 `.clm` 직렬화. `anima evaluate --py` 와 대칭 구현(`--py` consume·`cd $ANIMA_SRC`·result-file 후 second-exec cat; train 은 stdout stream 이라 shell `> rf 2>&1` 리다이렉트로 long-run pipe-close 회피). torch-side 는 **DIRECTIONAL** — verdict 는 직렬화 `.clm` 을 `anima evaluate --py` engine-native 재측정으로만 성립(`a_engine_native_learning`). ckpt 는 teardown 전 PULL(`a_fire_recover_complete`). `--py` 없는 `anima train` 은 `cli/train.hexa` 로 디스패치.
- **진입은 설치된 canonical `anima` PATH 명령만 (`hx install anima`)** — `hexa run cli/anima.hexa` 직접실행·`python cli/*.py`·engine-internal scorer 직접실행은 `.harness/enforcement.json` H-ANIMA-SINGLE-ENTRY pre_bash 가 차단(#2603). 단 hexa canonical 경로가 내부 subprocess 로 부르는 `verify_clm_v2.py descent`·`serialize_standalone.py` 는 정상(pre_bash 는 agent top-level 만 후킹, 내부 shell-out 미차단).
- ckpt verdict 는 `.clm` → `anima evaluate` 엔진-네이티브 재측정으로만 성립 — torch-side probe 채점 단독 verdict 금지(연구 미러 = DIRECTIONAL).
- `train.hexa` 의 수치 커널(forward/CE/decode-logits)은 numpy `math.log` + torch fp32 golden reference 와 성분별 byte-match 로 검증(CI fixture). `dt_ln` 발산·own-GEMM TF32 decode 발산을 잡는 장치(reference-match, py 엔진 미러 아님).
- post-serialize HELD-OUT DESCENT 게이트 필수(`verify_clm_v2.py descent <clm> <heldout>`) — `a_clm_gen_pipeline`. `verify_clm_v2.py`(torch-free numpy mirror)는 폐기 아님 = train.hexa 가 런타임 shell-out 하는 canonical descent 도구.

## 함정(gotcha)

- **`--gen 0` 은 "제한 없음"이 아님 (evaluate.hexa `g_eval_all`):** `g_eval_all` 안에서 `if gen > 0 { gen } else { _g_default_gen() }` → 0 이면 40 으로 collapse. G1 budgets(single=80, composed=120)도 `gen<=0` 이면 ref 값 그대로 사용. 의도가 "넓게"면 `--gen 80` 이상을 명시.
- **엔진 CE(`clm_forward_ce`) 는 `dt_ln` 버그로 overfit 을 GREEN 으로 가림** → `.clm` 품질은 numpy mirror(`verify_clm_v2.py`, `math.log`)로 교차검증. `dt_ln` 수정 전까지 engine CE 단독 verdict 는 DIRECTIONAL.
- **train-loss/lossF≈0 = 암기, 능력 아님** — held-out CE 가 없으면 clm303 처럼 4MB 1칸 120× 반복 암기를 '학습 성공'으로 오판 가능.
- `eval_pod.sh` 는 hexa ≥ v0.311.0 필수(이전 버전 = farr 누수로 85GB OOM).
