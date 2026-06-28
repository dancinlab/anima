# cli/ — anima CLI 진입점

**목적:** anima 의 두-언어(hexa · py) 단일진입점 모음. canonical 진입(`anima.hexa` · py twin `anima.py`)이 **3 설치형 verb** `train` · `serialize` · `evaluate` 를 대칭 파일로 디스패치 — 측정(`evaluate.{hexa,py}`) ⊥ 직렬화(`serialize.{hexa,py}`) ⊥ 학습(`train.{hexa,py}`). `hx install anima` → `bin/anima` shim 으로 **`anima` PATH 명령**화(= `hexa run cli/anima.hexa --` 노출 0). 루트 `CLAUDE.md` 의 scoped 보강 — 충돌 시 루트 우선.

## 설치형 CLI (사용자 타이핑 = `anima <verb>`, `hexa run` 아님)

```
anima train <args> [--py]      학습 → .pt + 자동 .clm v0.3 (+ held-out DESCENT 게이트)
anima serialize <pt> <clm> [--py]  독립 재직렬화 (.pt → .clm v0.3 + DESCENT) — 복구/재export
anima evaluate <model.clm> [--py]  G0-G6 측정 (.clm 전용; .pt 주면 친절에러→serialize 안내)
anima chat <ckpt.clm> [--byte] consciousness/byte chat — 명시 verb (= bare `anima <ckpt.clm>`)
anima <ckpt.clm> [--byte]      chat 단축형 (bare-ckpt)
anima help | -h | --help       usage
```

**2-production 엔진 선택 (`--py`):** 기본은 hexa twin(`cli/{train,serialize,evaluate}.hexa`), `--py` 면 py twin(`cli/{train,serialize,evaluate}.py`, CO-EQUAL byte-parity production). anima.hexa dispatch가 플래그 소비 후 `python3 cli/{x}.py` 로 라우팅 — 무거운 303M `evaluate` 시 hexa-farr decode 누수 우회 가능. `chat`/no-args/`help`/`-h`/`--help` 전부 usage.

## 핵심파일

| 파일 | 역할 | verdict 자격 |
|---|---|---|
| `anima.hexa` | **canonical 단일진입점** — verb 라우터: `train`/`serialize`/`evaluate` 를 cli/{train,serialize,evaluate}.hexa 로 sub-process 디스패치 + `chat`(default consciousness / `--byte`) | 엔진-네이티브 terminal |
| `anima.py` | **canonical py 진입점** (anima.hexa twin) — `evaluate`→cli/evaluate.py · `serialize`→cli/serialize.py · `train`→cli/train.py 디스패치 + `chat` stub. torch-free(디스패처). | — (디스패처) |
| `evaluate.hexa` | **측정 단일진입** — `g_eval_all`(generator L3 `gen_auto_ideate`) G0-G6 엔진-네이티브 채점 | 엔진-네이티브 terminal |
| `evaluate.py` | evaluate.hexa twin — `core/g_gates.py::g_eval_all` import(byte-parity py 엔진, torch-free) | 엔진-네이티브 terminal (byte-parity py 엔진) |
| `serialize.hexa` | **독립 재직렬화** — `.pt`→`.clm` v0.3 (cli/serialize.py 로 디스패치; .pt 로딩 py-native) | reference-match bridge |
| `serialize.py` | serialize backend — `clm_serialize_v2.serialize_v3` + `verify_clm_v2 descent`(torch 허용=학습계열) | reference-match bridge |
| `bin/anima` | 설치형 `anima` PATH shim — `cd <pkg> && hexa run cli/anima.hexa -- "$@"` (forge/drive shim 선례) | — |
| `anima_chat_cli.hexa` | 대화형 채팅 REPL helper | 엔진-네이티브 |
| `eval_pod.sh` | GPU pod 원격 측정 발사·회수 one-liner (`cli/eval_pod.sh <pod_id>`) | — |
| `train.hexa` | **production canonical 트레이너** — SAVANT/MITOSIS/4셀 통합 + 학습후 자동 .clm 직렬화 + held-out DESCENT (`a_train_flame_forge`·`a_clm_gen_pipeline`) | 엔진-네이티브 |
| `train.py` | REFERENCE + BRIDGE (torch Lane-P, `a_clm_gen_pipeline`) — 학습후 자동 serialize_v3 + DESCENT | DIRECTIONAL only |

## 규칙

- **`anima evaluate <model.clm>` = canonical G0-G6 단일진입 (`a_engine_native_learning`)** — generator L3 mouth(`gen_auto_ideate`) → G0-G6 엔진-네이티브 채점. **`.clm` 전용**(엔진은 .clm 만 디코드; .pt 주면 `anima serialize` 안내 친절에러). per-gate 파이썬 하네스·ad-hoc decode 우회 금지. verb 는 **`evaluate`**(구 `eval` rename 2026-06-28).
- **`anima evaluate` py = cli/evaluate.py (anima.hexa evaluate 의 py 등가물)** — `core/g_gates.py::g_eval_all` 을 **import 해서 호출**(byte-parity py 엔진, torch-free). `core/g_gates.py` 직접호출 = side-harness 우회 → 이 단일진입으로 수렴. 수치 동치: `cli/evaluate.py` ⇔ `core/g_gates.py` 동일 ckpt/gen 에서 G0-G6 byte-identical. `anima.py`/`evaluate.py`/`serialize.py`(디스패처+측정면)는 torch-free 유지 = 트레이너 dep 비-링크; `serialize.py`는 torch 허용(학습계열, .pt 로딩).
- **`anima train` 1회 = .pt + 자동 .clm + DESCENT** — train.{hexa,py}가 학습 종료 시 `serialize_v3`(.clm v0.3) + `verify_clm_v2 descent`(held-out mirror, math.log)까지 자동(재구현 아님 reference-match). `anima serialize`는 **이미 학습된 .pt** 독립 재export(복구). 둘 다 백엔드 = `train/clm/model/{clm_serialize_v2,verify_clm_v2}.py` 단일 SSOT.
- **무거운 decode 는 pool/summer (mac swap 🔴 OOM)** — 303M 급 eval 은 `cli/eval_pod.sh` 또는 pool 호스트. mac 은 small-ckpt(d768 4.4MB 류) parity smoke 만.
- `train.py` 는 production 아님 — ckpt verdict 는 `.clm` → `anima eval` 재측정으로만 성립. torch-side probe 채점 단독 verdict 금지.
- `train.hexa` ↔ `train.py` 수치 커널 **byte-parity(Tier-1 BLOCKING):** forward/CE/decode-logits 는 numpy `math.log` + torch fp32 golden 과 성분별 byte-match 필수(CI fixture). 이 tier 가 `dt_ln` 발산·own-GEMM TF32 decode 발산 등을 잡는 단 하나의 장치.
- Tier-2 레버(SAVANT 골든존·MITOSIS split·4셀 register·fail-loud 가드·held-out val)는 양쪽 lockstep 권장; drift 시 `parity-drift: <레버>` 명시(비blocking).
- post-serialize HELD-OUT DESCENT 게이트 필수(`verify_clm_v2.py descent <clm> <heldout>`) — `a_clm_gen_pipeline`.

## 함정(gotcha)

- **`--gen 0` 은 "제한 없음"이 아님 (g_gates.hexa L494):** `g_eval_all` 안에서 `if gen > 0 { gen } else { _g_default_gen() }` → 0 이면 40 으로 collapse. G1 budgets(single=80, composed=120)도 `gen<=0` 이면 ref 값 그대로 사용. 의도가 "넓게"면 `--gen 80` 이상을 명시.
- **엔진 CE(`clm_forward_ce`) 는 `dt_ln` 버그로 overfit 을 GREEN 으로 가림** → `.clm` 품질은 numpy mirror(`verify_clm_v2.py`, `math.log`)로 교차검증. `dt_ln` 수정 전까지 engine CE 단독 verdict 는 DIRECTIONAL.
- **train-loss/lossF≈0 = 암기, 능력 아님** — held-out CE 가 없으면 clm303 처럼 4MB 1칸 120× 반복 암기를 '학습 성공'으로 오판 가능.
- `eval_pod.sh` 는 hexa ≥ v0.311.0 필수(이전 버전 = farr 누수로 85GB OOM).
