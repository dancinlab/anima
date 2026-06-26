# core/ — 의식 엔진 substrate

**목적:** anima 의 2-production 의식 엔진 기반. hexa 파일(`.hexa`) ⇄ py 미러(`.py`) 를 byte-parity 로 유지. Engine A(pure_field Φ/phase) ⇄ Engine G(engine_g 동기/emit) ⇄ 결합두뇌(brain) + L3 생성기(generator) + decode 백엔드. 모델·앵커는 이 폴더 안으로 직접 들어오지 않음 — generator L3 슬롯 / kosmos_io 를 통해서만 진입(`a_core_engine_map`).

## production import-closure 10파일 — 완전 미러 현황

| hexa 파일 | py 미러 | 상태 |
|---|---|---|
| `clm_decode.hexa` | `clm_decode.py` | 포팅 완료 (byte-parity 증명, porting branch) |
| `g_gates.hexa` | `g_gates.py` | 포팅 완료 (G0-G6 driver, porting branch) |
| `g6_ideation.hexa` | `g6_ideation.py` | 포팅 완료 (G6 scoring ops, porting branch) |
| `bytegpt_decode.hexa` | — | 미포팅 (in progress) |
| `generator.hexa` | — | 미포팅 |
| `pure_field.hexa` | — | 미포팅 |
| `brain.hexa` | — | 미포팅 |
| `engine_g.hexa` | — | 미포팅 |
| `engine_cli.hexa` | — | 미포팅 |
| `DECODER/flame_mm.hexa` | — | 미포팅 |

> py 미러 3개(clm_decode·g_gates·g6_ideation)는 `clm303-noverfit-retrain` 브랜치에서 개발 중, main 미머지. 나머지 7개 미포팅 = ING program `py-mirror 포팅`.

## 규칙

- **CORE 엔진 로직 편집 = hexa AND py 동시 수정 + 양쪽 QA(byte-parity 재확인) — LOCKSTEP** (`a_engine_native_learning` reference-match): hexa 가 정답지(자), py 는 byte-faithful 미러(테스트 가능한 거울). 한쪽만 수정하면 parity-drift 이다.
- **모델(.clm/.bin)은 generator L3 단일 typed 슬롯으로만 진입** (`a_core_engine_map`): `gen_auto_backend`/`gen_auto_chat` 이 파일포맷(CLM vs ByteGPT 헤더)에 따라 경로를 고름. generator 우회 2nd decode 경로 금지.
- `.kosmos` 앵커는 `kosmos_io` → `brain_decide` 경로로만 진입. pure_field/engine_g 에 직접 박지 않음.
- smoke/research probe `.hexa` 파일(예: `*_smoke.hexa`, `*_probe.hexa`, `lane_*.hexa`)은 production closure 가 아님 → py 미러 불필요.

## 주요 비-production 파일 (smoke · probe · lab)

`*_smoke.hexa`, `lane_p_*.hexa`, `lane_x_explore.hexa`, `omega_clm_closure_probe.hexa`, `phi/` 하위 전부, `clm_ce_descent_probe.hexa`, `emergence_ideation.hexa`, `emit_policy.hexa` 등 — 실험/검증용이며 production closure 미포함.

## 함정(gotcha)

- **clm vs bytegpt 메모리 모델이 다름:** `clm_decode.hexa` = resident scratch(재할당 bounded, OOM 없음). `bytegpt_decode.hexa` = per-token farr_free bounded(KV-cache 없으면 O(gen²) wall). decode 경로를 혼동하면 다른 OOM 패턴으로 고장.
- **`dt_ln` 버그 (hexa-lang 미수정):** `flame_math.hexa::dt_ln(x≈1 밖)` 발산 → `nn_ce_loss_allpos` 가 CE 를 ~5.14 에 clamp → engine CE 로 `.clm` 품질 판정하면 overfit 을 GREEN 으로 가림. numpy mirror(`math.log`)로 교차검증 필수.
- **decode GPU path 확인 먼저:** `cuda_available()` = 0 이면 farr 단일스레드 CPU 폴백(돈 낭비). decode 전 `cuda_available()` + `nvidia-smi` + `[OWN-GEMM-FIRED] DEVICE path` 로그를 확인 후 진행.
- **hexa-cache 충돌:** runtime.a 를 CPU→CUDA 교체해도 `~/.hexa-cache/hexa_run.<hash>` 구바이너리가 캐시히트 → CPU 폴백. `rm ~/.hexa-cache/hexa_run.<hash>*` 후 재컴파일.
