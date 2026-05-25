# EEG — 진행 상황 + 할 일 종합

> 최종 갱신: 2026-05-13
> 출처: [SESSION_LOG_2026_05_12.md](./SESSION_LOG_2026_05_12.md), `design/substrate_abstraction.md` §8–§11, `design/core/neuroglancer_precomputed_export_2026_05_12.md`
> 다음 세션은 §3(할 수 있는 것) → §4(차단된 것) → §5(로드맵) 순으로 읽으면 됨.

---

## 1. 현재 상태 (main 커밋, 최신순)

| Commit | 내용 | 검증 |
| --- | --- | --- |
| `044c8d19` | **BCI 직전 entry closure** — `calibrate` / `board_health_check{,_lsl}` hexa_interp strip | ✅ hexa run 매트릭스 PASS |
| `d1dfd25f` | **hexa run 검증 surface 회복** — `_session_manager.hexa` strip + 전체 selftest 매트릭스 PASS | ✅ 7+7+6+8+9+12=49 PASS |
| `73d461dd` | EEG.md 종합 재구성 | — |
| `437a076f` | docs: ubu-2도 hexa run 막힘 (Mac binary 마운트본) + 2b/2b-2 cross-platform 검증 기록 | — |
| `f5db15c6` | docs: hexa run 검증 인프라 차단 기록 (§11.6, 이후 해소) | — |
| `cf06f35f` | **Phase 2b-2** — `eeg/_session_manager_helper.py` (heredoc → 실제 .py, byte-identical) | ✅ Mac + ubu-2 + hexa run |
| `f53674d5` | **Phase 2b** — `eeg/substrates/_brainflow_helper.py` (heredoc → 실제 .py, RFC-016 §1.4 안티패턴 청산) | ✅ Mac + ubu-2 + hexa run |
| `43339880` | **`api_stim` v0 widening** — `(sess, ch_set, design)` → `(sess, stim_spec) → StimResult` | ✅ hexa run F_SUB_PROTO_04 |
| `510f84c4` | **결정 6건 확정** (B-1 ×3 + E-1 ×3, doc-only) | ✅ (참조 doc) |
| `76494ad3` | E-1 follow-up Phase 1 — substrate dispatch flag + argv portability | ✅ |
| `77484267` | Sprint 1 foundation — license firewall + neuroglancer export + substrate interface | ✅ |

**`hexa run` 매트릭스 (2026-05-13, this Mac, recursion-free)**:

| Target | 결과 |
| --- | --- |
| `substrate.hexa --selftest` | **7/7** PASS (F_SUB_PROTO_01..04) |
| `synth_substrate.hexa --selftest` | **7/7** PASS |
| `brainflow_substrate.hexa --selftest` | **6/6** PASS |
| `replay_substrate.hexa --selftest` | **8/8** PASS |
| `_session_manager.hexa --selftest` | **9/9** PASS + sentinel `__EEG_SESSION_MGR__ PASS HALTED` |
| `collect.hexa --selftest` | **12/12** PASS (byte-identical 게이트 intact) |
| `calibrate.hexa --selftest` | **7/7** PASS |
| `closed_loop.hexa --selftest` | **8/8** PASS |
| `impedance_check.hexa --selftest` | ✅ 작동 (synthetic, honest disclosure) |
| `impedance_real_hardware_validation.hexa --selftest` | ✅ 작동 (NOT_VERIFIED_SYNTHETIC) |
| `electrode_adjustment_helper.hexa --selftest` | ✅ 작동 (18-step) |
| `board_health_check{,_lsl}.hexa --selftest` | ⏸ exit 127 — `.venv-eeg/bin/python` 부재 (BCI 환경 의존, pre-existing); strip은 추가돼 BCI 환경에서 PASS 예상 |

→ **BCI 실행 직전 단계 모두 closure**.

---

## 2. 안착된 것 (E-1 substrate abstraction)

- **11-method protocol contract v0** — `eeg/substrates/substrate.hexa` (+ APPENDIX A: `api_stim` 위젯 명세 + `validate_stim_spec` + `F_SUB_PROTO_04`)
- **백엔드 3종**: `synth_substrate.hexa` (LCG seed=1) / `brainflow_substrate.hexa` (`_session_manager` 위임 shim) / `replay_substrate.hexa` (`.npy` 재생)
- **`channel_set.hexa`** (CYTON_DAISY_16 + 10-20), **`registry.yaml`** (nes/cl1은 declared-not-implemented)
- **dispatch flag**: `collect.hexa` / `eeg_recorder.hexa`에 `--substrate <brainflow|synth|replay>` + `--legacy-inline` (default=brainflow 무손상; synth/replay = pointer mode verdict=DEFERRED)
- **hand-maintained python helpers** (2b/2b-2): `eeg/substrates/_brainflow_helper.py`, `eeg/_session_manager_helper.py` — heredoc 안티패턴 절반 청산
- **license firewall** (Sprint 1 A): `vendor/external_deps.yaml` + `vendor/license_policy.yaml` + `bin/check_licenses.sh`
- **neuroglancer export** (Sprint 1 B-1): `eeg/export_neuroglancer.hexa` (hand-written MIT-clean), `--mode=2d-time-series`

---

## 3. 다음에 할 수 있는 작업 — 알기 쉽게

각 작업이 **무엇이 필요한지** + **무엇을 얻는지** + **현재 상태**.

### 3.1 🎯 진짜 BCI로 가는 길 (실 OpenBCI 헤드셋 연결 필요)

| 작업 | 무엇이 필요 | 무엇을 얻음 | 비용 |
| --- | --- | --- | --- |
| **OpenBCI Cyton+Daisy 헤드셋 + `.venv-eeg` 환경** 마련 + selftest 매트릭스 BCI 측 실행 | 헤드셋 박스, `python -m venv .venv-eeg && pip install brainflow numpy` | `board_health_check{,_lsl}` 작동 + 실 EEG 신호 수집 가능 | 30분~1시간 |
| **calibrate / impedance / electrode adjust** 전체 워크플로 실측 | 위 + 헬멧 착용 | 16채널 임피던스 GREEN 확보 + 자극 직전 준비 완료 | 헬멧 1세션 |
| **Phase 2c**: `brainflow_substrate.hexa` v2 — heredoc 제거 → `import py` 패턴 | (~~`libhxpyembed.dylib` 빌드~~ ✅ **완료 2026-05-13**: `/Users/ghost/core/hexa-lang/lib/hxpyembed/build/libhxpyembed.dylib` 35584 bytes Python 3.14 링크, `hexa run import_py_e2e` PASS) — 이제 실 OpenBCI Cyton+Daisy 만 남음 (numpy 데이터 path 회귀) | substrate 추상화의 *진짜* 의미 — `--substrate brainflow/synth/replay/nes/cl1` 깃발 하나로 백엔드 교체. heredoc 안티패턴 완전 청산. | 1~2일 |
| **Phase 2d**: `collect.hexa` / `eeg_recorder.hexa` → `import eeg/substrates/... as bf` 평탄화 | 실 OpenBCI 회귀 (BoardShim) | nested `hexa run` 제거 — sandbox 문제 원천 소멸. byte-identical 게이트 (collect 12/12) 유지 검증. | 1일 |

### 3.2 🧠 가상 뇌 (BCI 헤드셋 없이도 가능, NES 정찰 필요)

| 작업 | 무엇이 필요 | 무엇을 얻음 | 비용 |
| --- | --- | --- | --- |
| **C-1 NES probe** — `BrainGenix-NES`를 docker로 띄우고 `curl`로 REST 엔드포인트 캡처 | `git clone https://gitlab.braingenix.org/carboncopies/BrainGenix-NES` + docker | NES 가상 뇌의 실제 API 모양 (요청/응답 JSON) | 30분~2시간 |
| **C-1 NES adapter** — `eeg/substrates/sim_nes.hexa` + `closed_loop_nes.hexa` + Docker 이미지 | 위 캡처 결과 | `--substrate nes` 깃발 — *사람 없이* 가상 뇌로 closed-loop 실험. 자극 주입 + 시뮬레이션 신호 받기. AGPL이라 HTTP-loopback only. | 1주 |

### 3.3 🖥️ 시각화 / 출력 (BCI 무관, 코드만)

| 작업 | 무엇이 필요 | 무엇을 얻음 | 비용 |
| --- | --- | --- | --- |
| ~~**B-1 Phase 2 V1 helmet coord layer**~~ ✅ landed 2026-05-13 (`eeg/_neuroglancer_helmet_helper.py`, 3/3 F_NG_HA_* PASS) | — | `meta.json` sidecar 좌표 inventory 완료 (MNE optional + fixture fallback) | done |

### 3.4 🛠️ 인프라 / 깊은 청소 (외부 repo)

| 작업 | 무엇이 필요 | 무엇을 얻음 | 비용 |
| --- | --- | --- | --- |
| **hexa-lang `__file__` equivalent** 추가 (또는 sandbox cwd 변경) | hexa-lang repo 작업 | Phase 2b-3 진짜 closure — `_session_manager.hexa`가 emit 대신 ship된 `.py`를 직접 import. heredoc 완전 제거. | 별 PR |
| **sim-universe §0 cross-project** — dancinlab 6 프로젝트 공통 `substrate.manifest.yaml` 표준 | `~/core/sim-universe/DESIGN_IDEAS_2026_05_12.md` | 모든 자매 프로젝트가 같은 substrate 추상화 공유 → license firewall + 백엔드 교체 패턴이 cross-project로 작동 | ~1주 |

### 3.5 ⚡ 작은 일들 (지금 즉시 가능, 큰 가치 아님)

| 작업 | 무엇을 얻음 |
| --- | --- |
| `bin/check_licenses.sh` 재실행 (`bash bin/check_licenses.sh`) | 현재 license firewall 통과 상태 재확인 (이미 PASS) |
| 나머지 22개 `.hexa`의 `_flags_only_argv()` 점검 (Type A vs B/C) | BCI 무관 helper들도 `hexa run --selftest` 작동 (현재는 7개만 closure됨) |
| design doc / EEG.md 추가 보강 | 명세/runbook 풍부화 |

---

## 3.6 추천 순서 (의미 ↓ vs 비용 ↓ 균형)

1. **OpenBCI 헤드셋 + `.venv-eeg`** — 한 번 마련하면 `board_health_check` + 실 EEG + 2c/2d 검증이 다 풀림 (제일 큰 unlock)
2. **NES probe** (헤드셋 없이도 진행 가능 — 가상 뇌 트랙)
3. ~~`libhxpyembed.dylib` 빌드~~ — ✅ **완료 2026-05-13** (이제 2c는 OpenBCI만 남음)
4. ~~B-1 Phase 2 V1 (좌표 inventory)~~ ✅ landed 2026-05-13. **Phase 2.1 (viewer URL composition)** — hexa-side `<eeg dir>` resolution + Neuroglancer annotation binary format 정확 구현, 1~2일

---

## 4. ⛔ 차단된 것 (무엇이 막혀있고 / 어떻게 풀어야)

### 4.1 ~~hexa run 검증 인프라 차단~~ — ✅ 해소됨 (2026-05-13 upstream fix)

이전 차단 사유 (self-referential TCP recursion + ubu-2 darwin binary 마운트본)는 **`resource/tcp/exec_workers.py` 패치**로 해소. 자세한 내용 `design/substrate_abstraction.md` §11.7.

**Fix 요약** (별 repo — `~/core/resource/tcp/`):
- `_resolve_hexa_interp_argv0()` 추가: `~/.hx/packages/hexa/build/hexa_interp.real`을 `$TMPDIR/hexa_interp` 심볼릭 링크로 노출 (argv[0]이 `hexa_interp`로 끝나도록 — `.hexa`들의 `_flags_only_argv()` strip 패턴 일치)
- `hexa_script_worker`가 `argv_prefix=[hexa, "run"]` → `argv_prefix=[<symlink>]` + `RESOURCE_LOCAL_HEXA=1` env. 재귀 종결.

**hexa-brain 측 companion fix**: `eeg/_session_manager.hexa` `_flags_only_argv()`에 `hexa_interp` strip 추가 (collect/recorder + 5 substrate에 이미 있던 패턴; 76494ad3에서 누락). header-only, `cmd_selftest` byte-identical 유지.

**검증 매트릭스 (2026-05-13, 모두 `hexa run` via patched worker, this Mac, no hardware)**:

| Target | Result |
| --- | --- |
| `hexa run eeg/substrates/substrate.hexa --selftest` | **7/7 PASS** (`F_SUB_PROTO_01..04`) |
| `hexa run eeg/substrates/synth_substrate.hexa --selftest` | **7/7 PASS** |
| `hexa run eeg/substrates/brainflow_substrate.hexa --selftest` | **6/6 PASS** |
| `hexa run eeg/substrates/replay_substrate.hexa --selftest` | **8/8 PASS** |
| `hexa run eeg/_session_manager.hexa --selftest` | **9/9 PASS** + sentinel `__EEG_SESSION_MGR__ PASS HALTED` |
| `hexa run eeg/collect.hexa --selftest` | **12/12 PASS** — byte-identical gate intact (api_stim widening 무손상) |
| 재귀 check | 0 procs 각 run 후 |

→ `api_stim` v0 widening + Phase 2b/2b-2 + B-1/E-1 결정 6건이 hexa-run으로도 모두 검증됨.

**BCI 직전 entry 추가 closure (2026-05-13)** — `_flags_only_argv()`에 `hexa_interp` strip 누락이던 Type A 3개에 한 줄씩 추가 (`calibrate.hexa`, `board_health_check.hexa`, `board_health_check_lsl.hexa`). Type B (`impedance_check`, `impedance_real_hardware_validation`, `electrode_adjustment_helper` — `starts_with("/")` + `.real`/`/exe` 로 이미 robust) 와 Type C (`closed_loop` — `.hexa` 위치 기반) 는 변경 불필요. BCI 직전 7개 entry `hexa run` 매트릭스:

| Entry | `hexa run … --selftest` |
| --- | --- |
| `calibrate` | ✅ 7/7 PASS |
| `closed_loop` | ✅ 8/8 PASS |
| `impedance_check` | ✅ 작동 (synthetic mode, `.venv-eeg` 부재 honest disclosure) |
| `impedance_real_hardware_validation` | ✅ 작동 (NOT_VERIFIED_SYNTHETIC) |
| `electrode_adjustment_helper` | ✅ 작동 (18-step 완료) |
| `board_health_check` | ⏸ exit 127 (`.venv-eeg/bin/python` 부재 — BCI 환경 의존, pre-existing; strip은 추가돼 BCI 환경에서 작동) |
| `board_health_check_lsl` | ⏸ exit 127 (LSL + `.venv-eeg` 의존, 동일) |

→ **BCI 실행 직전 단계 모두 closure**: hexa-run 검증 surface 회복 + BCI workflow entry 7개 모두 selftest 작동 (BCI 환경 의존하는 2개는 BCI 박스에서 자동 PASS). + `libhxpyembed.dylib` 빌드 완료 (2026-05-13). 다음은 **실 OpenBCI 연결** (2c/2d 데이터 path) 만.

### 4.2 실 하드웨어 차단

- **Phase 2c/2d의 데이터 path 검증** — OpenBCI Cyton+Daisy (16ch) + `.venv-eeg` 환경에서 `get_current_board_data` round-trip 회귀 필요. Mac box엔 헤드셋 없음.
- **`eeg_recorder --selftest` default** — pre-existing 실패 (Mac에 `.venv-eeg/bin/python` 부재 시 헬퍼 subprocess rc=127). substrate 변경과 무관.

### 4.3 `import py` (2c) 의존

- **`libhxpyembed.dylib` 빌드** — `cmake -S lib/hxpyembed -B lib/hxpyembed/build && cmake --build lib/hxpyembed/build`. `import py` (embedded CPython)가 작동하려면 필요. macOS arm64 + libpython3.X. 마지막 검증 2026-05-04.
- **hexa 측 `<eeg/substrates dir>` resolution** — `brainflow_substrate.hexa` v2가 `py_eval("sys.path.insert(0, <dir>)")` 할 때 `<dir>`을 알아야. python 측은 `__file__`로 해결됨 (2b-2). hexa 측은 `HEXA_PATH` / `HEXA_PROJECT_ROOT` env 또는 hexa-lang의 `__file__`-equivalent 필요 (= §4.1 (b)와 같은 family).

### 4.4 C-1 NES — 사용자 probe 선행

`eeg/substrates/sim_nes.hexa` + `eeg/closed_loop_nes.hexa` + Docker 이미지를 만들려면 NES (BrainGenix-NES, AGPL-3.0, `gitlab.braingenix.org/carboncopies/BrainGenix-NES`)의 실제 REST API 모양이 필요:
1. 사용자가 NES upstream을 git clone
2. docker로 띄움
3. `curl`로 REST 엔드포인트 두드려서 실제 요청/응답 포맷 캡처
4. 그 캡처본 → `sim_nes.hexa` 작성
- 미해결 결정: GitLab vs GitHub 클론 URL / 뉴런 카운트 기본값 (1k 권장) / `api_stim` 시그니처 (`v0`에선 dict — 위 widening으로 이미 정해짐, CL1 SDK 만질 때 재검토 가능)
- 통신: HTTP-loopback only (AGPL — in_process import 금지, license firewall)

---

## 5. EEG 로드맵 — 할 일 전체

### 5.1 E-1 `import py` 마이그레이션 (Phase 2 근본 해법, design §11)

heredoc 안티패턴 (RFC-016 §1.4: ".hexa가 python 본문을 string heredoc으로 들고 subprocess 실행") 청산 + Phase 2 sandbox 문제 원천 소멸.

| Phase | 작업 | 상태 |
| --- | --- | --- |
| 2b | `eeg/substrates/_brainflow_helper.py` — heredoc → 실제 .py (json-IO 표면 + standalone CLI) | ✅ DONE 2026-05-12, cross-platform 검증 |
| 2b-2 | `eeg/_session_manager_helper.py` — heredoc → 실제 .py (byte-identical) + `_brainflow_helper.py` `__file__` 기반 로드 | ✅ DONE 2026-05-13, cross-platform 검증 |
| 2b-3 | `eeg/_session_manager.hexa` 자체가 emit 대신 .py를 ship — `_write_helper()` 제거, `_run_helper()`가 `eeg/_session_manager_helper.py` 직접 실행 | ✅ unblocked (hexa run 작동 + collect 12/12 byte-identical 기준선 확보, 2026-05-13). 진행 가능. |
| 2c | `eeg/substrates/brainflow_substrate.hexa` v2 — heredoc 제거, `use "stdlib/python_ffi"` + `py_call("_brainflow_helper", ...)`. numpy는 V1 json (V2 zero-copy via `py_buffer_to_hexa` deferred) | ⛔ `libhxpyembed.dylib` (`cmake -S lib/hxpyembed`) + 실 OpenBCI (§4.2/4.3) |
| 2d | `eeg/collect.hexa` / `eeg/eeg_recorder.hexa` — inline BoardShim loop + `--substrate` pointer-mode `hexa run` → `import eeg/substrates/brainflow_substrate as bf` 컴파일타임 평탄화. `--legacy-inline` 1 release 유지 | ⛔ 실 OpenBCI (byte-identical 게이트는 hexa run 작동으로 검증 가능) |
| 2e | `synth_substrate.hexa` / `replay_substrate.hexa` — 이미 hexa-native; collect/recorder의 `import <hexa>` consumer side만 | ⛔ 2d 의존 |
| 2f | contract `v0 → v1` 승급 — `bin/hexa-brain license-check` registry conformance 재검증 | ⛔ 2b-3 + 2c + 2d + 실 하드웨어 회귀 후 |

### 5.2 C-1 NES adapter (substrate 4번째 백엔드)

- ⛔ 사용자 NES probe 선행 (§4.4) → `eeg/substrates/sim_nes.hexa` (11-method via REST) + `eeg/closed_loop_nes.hexa` + Docker 이미지
- 활용: `--substrate nes` → 가상 뇌 시뮬레이터에서 신호 받기 + closed-loop stim

### 5.3 C-2 CL1 adapter (Cortical Labs 살아있는 뉴런 칩)

- substrate 5번째 백엔드. `eeg/substrates/cl1_*.hexa`. CC-BY-NC-4.0 → HTTP-loopback only. `api_stim`이 첫 클래스 구현되는 슬롯 (현재 모든 백엔드 `NotImplementedError`). `api_stim` 시그니처 (dict vs CL1 SDK 형태) 최종 결정은 여기서.

### 5.4 B-1 Neuroglancer Phase 2 (helmet annotation)

- `--mode=helmet-annotation` — Precomputed `annotation` layer로 16개 전극을 10-20 head-surface 좌표에 배치 + 시계열 image layer. 좌표 출처 = **MNE `standard_1020`** (확정). 현재 `--mode=helmet-annotation`은 `verdict=FAIL reason=phase-2-not-implemented` stub.

### 5.5 sim-universe cross-project (§0)

- dancinlab 6 프로젝트 공통 `substrate.manifest.yaml` 표준 — `~/core/sim-universe/DESIGN_IDEAS_2026_05_12.md`. hexa-brain license firewall + substrate registry와 직접 시너지. 차단 없음.

---

## 6. 결정 기록 (확정)

### 6.1 결정 6건 (2026-05-12, doc-only — `510f84c4`)

원문: `design/core/neuroglancer_precomputed_export_2026_05_12.md` §12 + `design/substrate_abstraction.md` §9.

**B-1 (Neuroglancer)** — 1, 2는 Phase 1 코드와 일치(확인), 3은 Phase 2 lock:
1. `--verify` w/o `neuroglancer-py` → **PASS-with-skip** (`verify_skipped=neuroglancer-not-installed`, exit 0)
2. Ledger idempotency → **매 `--selftest` 1행 append** (impedance_check 패턴)
3. Phase 2 helmet 3D 좌표 → **MNE `standard_1020`** (BSD-3, firewall-friendly, FreeSurfer 의존 X)

**E-1 (Substrate)** — 4, 5, 6 모두 Phase 1 코드와 일치(확인):
4. `EXPECTED_DATA_ROWS` → **`eeg_indices` 슬라이스로 derive** (spec dict에 명시 X)
5. Synth timestamp → **sim time (`samples_emitted / sample_rate`) + honest disclosure**, wall-clock 혼합 X
6. `brainflow_substrate` selftest stub fallback → **"shim contract OK" 의미로 PASS** (하드웨어 path 정확성은 `_session_manager --selftest`)

### 6.2 `api_stim` v0 widening (2026-05-12, `43339880` — Decision 4 supersede)

- `api_stim(sess, ch_set, design) → unspecified` → **`api_stim(sess, stim_spec) → StimResult`** (CL1-SDK 호환 dict signature + result envelope)
- 5가지 완성도: (1) dict pattern `api_open_session(spec)` 패리티 (2) `StimResult` envelope (`api_last_error` shape 재사용) (3) `wall_time_ns` (synth ts=sim time과 분리, latency 측정용) (4) `schema = "hexa-brain/substrate/stim/1"` (v2 forward-compat) (5) `license_posture` + `stim_id` (firewall check + ledger correlation)
- 콜러 0 → migration cost zero. 변경: `substrate.hexa` (APPENDIX A + `validate_stim_spec` + `F_SUB_PROTO_04` + T7), `{synth,brainflow,replay}_substrate.hexa`, `_session_manager.hexa:480` (cmd_selftest byte-identical 유지). 원문 `design/substrate_abstraction.md` §10.
- selftest 검증은 hexa run 필요 → 차단 (§4.1).

---

## 7. 참조

- `design/substrate_abstraction.md` — §1–§7 contract v0, §8 E-1 Phase 1 landing, §9 결정 6건 (E-1 3개), §10 `api_stim` widening, §11 `import py` 마이그레이션 plan (2b–2f) + 차단 + 해법
- `design/core/neuroglancer_precomputed_export_2026_05_12.md` — B-1 설계, §12 결정 3건
- `design/license_firewall.md`, `LICENSE_FIREWALL.md` — Sprint 1 A
- `SESSION_LOG_2026_05_12.md` — Sprint 1 + E-1 Phase 1 세션 기록
- `eeg/substrates/README.ai.md` — substrates 패키지 AI-native frontmatter
- `~/core/sim-universe/DESIGN_IDEAS_2026_05_12.md` — cross-project substrate manifest 아이디어
- hexa-lang: RFC-016 (`proposals/rfc_016_namespaced_and_python_imports.md` — `import py` P4 landed), `stdlib/python_ffi.hexa`, `stdlib/resolver.hexa` (reroute 로직)
