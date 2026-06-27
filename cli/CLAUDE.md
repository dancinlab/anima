# cli/ — anima CLI 진입점

**목적:** anima 의 **hexa-단일** 진입점 모음. 추론/평가 진입(`anima.hexa`, evaluate·serialize·train 은 서브커맨드) + production 트레이너(`train.hexa`). py 진입점(`anima.py`·`train.py`)은 2026-06-28 폐기. 루트 `CLAUDE.md` 의 scoped 보강 — 충돌 시 루트 우선.

## 핵심파일

| 파일 | 역할 | verdict 자격 |
|---|---|---|
| `anima.hexa` | **단일 추론/평가 진입점** — `anima chat` · `anima eval <ckpt>` (L236→`anima_eval_mode`→`g_eval_all`) | 엔진-네이티브 terminal |
| `anima_chat_cli.hexa` | 대화형 채팅 REPL helper | 엔진-네이티브 |
| `eval_pod.sh` | GPU pod 원격 측정 발사·회수 one-liner (`cli/eval_pod.sh <pod_id>`) | — |
| `train.hexa` | **production canonical 트레이너 (단일)** — SAVANT/MITOSIS/4셀/held-out val/descent 통합 (`a_train_flame_forge`) | 엔진-네이티브 |

> `train.py`(torch Lane-P REFERENCE+bridge)는 2026-06-28 폐기 — core 미러라 `git rm`(`cli/train.hexa` 가 task#10 full-parity 로 모든 레버 보유). 과거 torch Lane-P GPU 트레이너는 `state/py_retire_archive/train_torch_lane_p/`.

## 규칙

- **`anima eval <ckpt>` = canonical G0-G6 단일진입 (`a_engine_native_learning`)** — generator L3 mouth(`gen_auto_ideate`) → G0-G6 엔진-네이티브 채점. per-gate 파이썬 하네스·ad-hoc decode 우회 금지.
- ckpt verdict 는 `.clm` → `anima eval` 엔진-네이티브 재측정으로만 성립 — torch-side probe 채점 단독 verdict 금지(연구 미러 = DIRECTIONAL).
- `train.hexa` 의 수치 커널(forward/CE/decode-logits)은 numpy `math.log` + torch fp32 golden reference 와 성분별 byte-match 로 검증(CI fixture). `dt_ln` 발산·own-GEMM TF32 decode 발산을 잡는 장치(reference-match, py 엔진 미러 아님).
- post-serialize HELD-OUT DESCENT 게이트 필수(`verify_clm_v2.py descent <clm> <heldout>`) — `a_clm_gen_pipeline`. `verify_clm_v2.py`(torch-free numpy mirror)는 폐기 아님 = train.hexa 가 런타임 shell-out 하는 canonical descent 도구.

## 함정(gotcha)

- **`--gen 0` 은 "제한 없음"이 아님 (g_gates.hexa L494):** `g_eval_all` 안에서 `if gen > 0 { gen } else { _g_default_gen() }` → 0 이면 40 으로 collapse. G1 budgets(single=80, composed=120)도 `gen<=0` 이면 ref 값 그대로 사용. 의도가 "넓게"면 `--gen 80` 이상을 명시.
- **엔진 CE(`clm_forward_ce`) 는 `dt_ln` 버그로 overfit 을 GREEN 으로 가림** → `.clm` 품질은 numpy mirror(`verify_clm_v2.py`, `math.log`)로 교차검증. `dt_ln` 수정 전까지 engine CE 단독 verdict 는 DIRECTIONAL.
- **train-loss/lossF≈0 = 암기, 능력 아님** — held-out CE 가 없으면 clm303 처럼 4MB 1칸 120× 반복 암기를 '학습 성공'으로 오판 가능.
- `eval_pod.sh` 는 hexa ≥ v0.311.0 필수(이전 버전 = farr 누수로 85GB OOM).
