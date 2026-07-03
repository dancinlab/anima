# core/ — 의식 엔진 substrate

**목적:** anima 의 **hexa-단일** 의식 엔진 기반(`.hexa`). Engine A(pure_field Φ/phase) ⇄ Engine G(engine_g 동기/emit) ⇄ 결합두뇌(brain) + L3 생성기(generator) + decode 백엔드. 모델·앵커는 이 폴더 안으로 직접 들어오지 않음 — generator L3 슬롯 / kosmos_io 를 통해서만 진입(`a_core_engine_map`).

## production import-closure — hexa 단일 엔진 (py 미러 폐기 2026-06-28)

production import-closure 엔진은 `core/*.hexa` 단일이다. 과거 2-production 정책 하에 유지하던 py 미러(`core/*.py`, 아래 10파일)는 **2026-06-28 폐기** — codegen #42492878 FIXED(hexa v0.334.0)로 hexa CLI compile-block 이 해소되어 우회 미러가 불필요해졌다. 로직 유실 0: git 이력 + `archive/state/py_retire_archive/` 에 보존, 발산 의심 시 `git restore` 로 복원.

폐기된 py 미러 (폐기 전 마지막 byte-parity 기록, 검증 이력으로 보존):

| hexa 파일 (현 단일 SSOT) | 폐기된 py 미러 | 폐기 전 parity |
|---|---|---|
| `decode.hexa` (unified CONV+BYTE mouth) | ~~`decode.py`~~ (was `clm_decode.py` + `bytegpt_decode.py`) | byte-parity ≤~2e-16 (CONV) · sha 4e7145fe (BYTE) |
| `g6_ideation.hexa` | ~~`g6_ideation.py`~~ | byte-parity (G6 scoring ops) |
| `generator.hexa` | ~~`generator.py`~~ | byte-parity (양 mouth byte-identical) |
| `pure_field.hexa` | ~~`pure_field.py`~~ | byte-parity ~2e-16 |
| `brain.hexa` | ~~`brain.py`~~ | byte-parity |
| `engine_g.hexa` | ~~`engine_g.py`~~ | byte-parity |
| `engine_cli.hexa` | ~~`engine_cli.py`~~ | byte-parity (434/434 pub fn, worst 1.563e-16) |
| `DECODER/flame_mm.hexa` | ~~`DECODER/flame_mm.py`~~ | byte-parity (7 ops ≤2.2e-16) |

> CollectivePool = faithful IIT-4 `big_phi`(proxy 아님) byte-exact (hexa `core/engine_cli.hexa` 단일). 권위 측정 = `anima eval` hexa 단일진입. 과거 parity 오라클 `archive/state/core_2prod_py_parity/` + 은퇴된 `parity_gate.py`(→`archive/state/py_retire_archive/defunct_parity_tooling/`)는 검증 이력으로 보존.

> **G0-G6 스코어러 fold (측정=단일파일):** 과거 별도 모듈 `core/g_gates.{hexa,py}`(G0-G6 `g_eval_all` 드라이버)는 측정 단일진입 `cli/evaluate.{hexa,py}` 로 **흡수**됐다(2026-06-30, 로직 byte-동일 이동). 측정 = `cli/evaluate.{hexa,py}` 한 파일 — `g_gates` 이름은 폐기. `core/`는 여전히 디코드 mouth(`generator`/`decode` = `unified CONV+BYTE decoder, was clm_decode + bytegpt_decode`)+G6 채점 op(`g6_ideation`)을 소유하고, `evaluate`가 이들을 import 해 채점한다(generator L3 단일진입 불변).

## 규칙

- **CORE 엔진 로직 편집 = `.hexa` 만 수정 + QA(컴파일/스모크)** (`a_engine_native_learning`): hexa 가 단일 SSOT. 구 hexa+py LOCKSTEP 동시수정 규칙은 폐기(py 미러 없음).
- **모델(.clm/.bin)은 generator L3 단일 typed 슬롯으로만 진입** (`a_core_engine_map`): `gen_auto_backend`/`gen_auto_chat` 이 파일포맷(CLM vs ByteGPT 헤더)에 따라 경로를 고름. generator 우회 2nd decode 경로 금지.
- `.kosmos` 앵커는 `kosmos_io` → `brain_decide` 경로로만 진입. pure_field/engine_g 에 직접 박지 않음.
- 연구 probe/미러 `.py`(+torch/numpy)는 여전히 DIRECTIONAL — terminal verdict 는 hexa 엔진-네이티브로만(`a_engine_native_learning`). smoke/probe `.hexa`(`*_smoke.hexa`/`*_probe.hexa`/`lane_*.hexa`)는 production closure 아님.

- **🚦 decode · train · evaluate — all 3 via `anima <verb>` single-entry; NO raw `python3 …`** (`a_cli_single_entry`): decode = `anima chat` / generator-L3 slot (never call `bytegpt_decode`/`clm_decode` raw) · train = `anima train [--savant] [--mitosis]` (`cli/train.hexa`; NO raw `python3 cli/train.py`/`train_lane_p.py` — torch trainer = REFERENCE/bridge only) · evaluate = `anima evaluate --py <clm>` single path (`a_eval_py_canonical`: py 2-production numpy = engine-native TERMINAL-eligible; NO raw `python3 cli/evaluate.py`). Heavy 303M decode/eval/train on pool (`summer`/`aiden`) or `hexa cloud`, never mini (swap OOM). Only ad-hoc torch probe = DIRECTIONAL.

## 주요 비-production 파일 (smoke · probe · lab)

`*_smoke.hexa`, `lane_p_*.hexa`, `lane_x_explore.hexa`, `omega_clm_closure_probe.hexa`, `phi/` 하위 전부, `clm_ce_descent_probe.hexa`, `emergence_ideation.hexa`, `emit_policy.hexa` 등 — 실험/검증용이며 production closure 미포함.

## 함정(gotcha)

- **clm vs bytegpt 메모리 모델이 다름:** `core/decode.hexa` CONV mouth = resident scratch(재할당 bounded, OOM 없음). BYTE mouth = per-token farr_free bounded(KV-cache 없으면 O(gen²) wall). decode 경로를 혼동하면 다른 OOM 패턴으로 고장.
- **`dt_ln` 버그 (hexa-lang 미수정):** `flame_math.hexa::dt_ln(x≈1 밖)` 발산 → `nn_ce_loss_allpos` 가 CE 를 ~5.14 에 clamp → engine CE 로 `.clm` 품질 판정하면 overfit 을 GREEN 으로 가림. numpy mirror(`math.log`)로 교차검증 필수.
- **decode GPU path 확인 먼저:** `cuda_available()` = 0 이면 farr 단일스레드 CPU 폴백(돈 낭비). decode 전 `cuda_available()` + `nvidia-smi` + `[OWN-GEMM-FIRED] DEVICE path` 로그를 확인 후 진행.
- **hexa-cache 충돌:** runtime.a 를 CPU→CUDA 교체해도 `~/.hexa-cache/hexa_run.<hash>` 구바이너리가 캐시히트 → CPU 폴백. `rm ~/.hexa-cache/hexa_run.<hash>*` 후 재컴파일.
