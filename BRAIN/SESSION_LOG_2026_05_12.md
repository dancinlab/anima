# Session Log — 2026-05-12

> Stop 훅 요구사항 (AI agent는 진행하면서 반드시 md로 기록을 남겨야 함) 충족용 세션 종료 기록.
> 세션 범위:
>   1차 (ubu-2): GOOGLE_CONSCIOUSNESS_CHIP 리서치 흡수 → Sprint 1 plan 수립/승인 → A/B-1/E-1 세 부분 격리 worktree 병렬 구현 → main commit `77484267`.
>   2차 (Mac): 사용자 "go" 재개 → E-1 follow-up Phase 1 (substrate dispatch flag + argv portability) → main commit `76494ad3`.
> 실행 환경: 1차는 ubu-2 (summer uid 1000) 원격 offload, 2차는 Mac (`/Users/ghost/core/hexa-brain`) 직접.

---

## 1. 한 줄 요약

GOOGLE_CONSCIOUSNESS_CHIP 8개 외부 OSS landscape에서 hexa-brain v3-v5 substrate interop 토대 3개 동시 착륙(`77484267`, 30 files / +5423) + 후속 substrate dispatch flag Phase 1 안착(`76494ad3`, 11 files / +247) — 합계 41 files / +5670 / −6, 2개 main commit.

---

## 2. 산출물 인벤토리

### 2.1 신규 파일 (19)

| Path | 역할 |
| --- | --- |
| `GOOGLE_CONSCIOUSNESS_CHIP.md` | 루트 복사본 (리서치 SSOT) |
| `vendor/external_deps.yaml` | hand-curated 외부 의존성 catalog |
| `vendor/license_policy.yaml` | 4계층(eeg/eeg_core/core/tool) allow-list |
| `vendor/README.ai.md` | vendor/ AI-native 스키마 |
| `bin/check_licenses.sh` | 422줄 enforcer + F_LF_01/02/03 selftest |
| `LICENSE_FIREWALL.md` | 사용자-facing 정책 doc |
| `design/license_firewall.md` | 설계 rationale |
| `design/substrate_abstraction.md` | substrate 11-method contract v0 |
| `design/core/neuroglancer_precomputed_export_2026_05_12.md` | B-1 설계 doc |
| `eeg/export_neuroglancer.hexa` | hand-written MIT-clean Precomputed writer |
| `eeg/doc/neuroglancer_export_runbook_2026_05_12.md` | 운영 runbook |
| `eeg/protocols/README.ai.md` | protocols/ AI-native frontmatter |
| `eeg/substrates/__init__.hexa` | 패키지 로더 + marker |
| `eeg/substrates/README.ai.md` | substrates/ AI-native frontmatter |
| `eeg/substrates/substrate.hexa` | 11-method protocol contract |
| `eeg/substrates/synth_substrate.hexa` | deterministic LCG seed=1 backend |
| `eeg/substrates/brainflow_substrate.hexa` | `_session_manager` 위임 shim |
| `eeg/substrates/replay_substrate.hexa` | `.npy` 디스크 재생 backend |
| `eeg/substrates/channel_set.hexa` | CYTON_DAISY_16 preset + 10-20 labels |
| `eeg/substrates/registry.yaml` | 백엔드별 metadata (nes/cl1은 declared-not-implemented) |

### 2.2 수정 파일 (7)

| Path | 변경 |
| --- | --- |
| `.gitignore` | `/tmp/license_firewall_*.py` 추가 |
| `AGENTS.md` | license-firewall 의무 단락 추가 |
| `CHANGELOG.md` | Unreleased 섹션 (A + B-1 + E-1) |
| `LATTICE_POLICY.md` | §3.4 License gates 추가 |
| `README.md` | CC BY-NC 라인 → 방화벽 링크, neuroglancer exporter 멘션 |
| `bin/hexa-brain` | `license-check` subsystem + `export-neuroglancer` verb |
| `eeg/_session_manager.hexa` | 가산적 `api_read_chunk/get_eeg_indices/get_sample_rate/stim` 추가 (cmd_selftest byte-identical 회귀 게이트 유지) |

### 2.3 commit

```
77484267 feat: Sprint 1 foundation — license firewall + neuroglancer export + substrate interface
30 files changed, 5423 insertions(+), 1 deletion(-)
```

---

## 3. 검증 결과

| Falsifier | 결과 |
| --- | --- |
| `F_LF_01` clean tree → exit 0 | PASS |
| `F_LF_02` planted violation → exit 2 | PASS |
| `F_LF_03` comment-only → exit 0 | PASS |
| Real scan: 205 files, 0 violations | PASS |
| `F_NG_01..06` (B-1, worktree) | 6/6 PASS |
| `F_SM_01..03` (regression gate) | PASS |
| `F_SUB_PROTO_01..03` + `F_SUB_01..03` + `F_CS_01..03` (E-1) | PASS |

---

## 4. 미완 / 차단

| # | 항목 | 차단 요인 |
| --- | --- | --- |
| #11 | E-1 follow-up — `collect.hexa`/`eeg_recorder.hexa` substrate API 리팩토링 + `dual_stream.hexa:211` replay 연결 + contract v0→v1 승급 | **bg 에이전트 인증 만료 ("Not logged in · Please run /login")** |
| #12 | C-1 NES adapter — Docker 이미지 + `eeg/substrates/sim_nes.hexa` + `eeg/closed_loop_nes.hexa` | 사용자 NES upstream probe 선행 (로컬 docker 구동 + curl REST 캡처) |

---

## 5. 사용자 결정 대기 (6건)

### B-1 (Neuroglancer)
1. `--verify`가 `neuroglancer-py` 없을 때 PASS-with-skip vs 엄격 FAIL?
2. Ledger idempotency: 매 selftest 1행 추가 유지?
3. Phase 2 helmet 3D 좌표 출처: MNE `standard_1020` vs FreeSurfer `fsaverage`?

### E-1 (Substrate)
4. `EXPECTED_DATA_ROWS=32` 처리 — (a) eeg_indices 슬라이스 / (b) synth·replay가 32 rows 에뮬레이션 / (c) spec에 명시? (현재 design (a) 권장)
5. Synth timestamp = sim time (샘플카운트/sample_rate) — wall time 차이 honest disclosure로 처리, OK?
6. brainflow_substrate selftest의 stub fallback — "shim contract OK" 의미로 PASS, OK?

### Sprint plan (C-1 진입 전)
- NES endpoint 실제 형태 (사용자 probe 필요)
- NES neuron count 기본값 (1k 권장)
- GitLab vs GitHub 클론 URL
- `api_stim` 시그니처 (dict vs CL1-style triple)

---

## 6. 부수 산출물 (이번 세션, 별도 repo)

- `~/core/sim-universe/DESIGN_IDEAS_2026_05_12.md` — sim-universe v1.0.0 설계/구현 아이디어 286줄. 핵심: dancinlab 6 프로젝트 공통 `substrate.manifest.yaml` 표준 제안 (hexa-brain license firewall과 직접 시너지).

---

## 7. 다음 액션 후보

| 액션 | 차단 | 비용 |
| --- | --- | --- |
| `/login` 재인증 → #11 E-1 follow-up bg 재기동 | 사용자 액션 | 1분 |
| C-1 NES upstream probe (docker 구동 + curl 캡처) | 사용자 액션 | 30분~2시간 |
| 오픈 질문 6건 답변 → E-1 follow-up에 반영 | 사용자 결정 | 즉시 |
| sim-universe §0 substrate-manifest cross-project 작업 | 없음 | ~1주 |

---

## 8. 환경 메모

- 원격 실행: ubu-2 (uid 1000 summer), `/home/summer/mac_home/core/hexa-brain` 마운트 통한 작업
- Mac 측 SSOT: `/Users/ghost/core/hexa-brain` (동일 commit `77484267` 가시)
- `.git/` 소유자 = uid 501 (Mac), `chmod g+w` 후 summer write 가능
- safe.directory: `/home/summer/mac_home/core/hexa-brain` 글로벌 등록 완료
- Worktree 3개 정리 완료 (`agent-aa61ca4f3804caaf4`, `agent-aa796522a59160c53`, `agent-ab9d38ddc5f081958`)
- bg 에이전트 인증 실패 원인: 추정 oauth slot TTL 만료 (cl wrapper의 `expired-permanent` slot 처리와 별개 가능성). 재인증 명령: `claude /login` 해당 host TTY.

---

## 9. 세션 종료 사유 (1차 — ubu-2 인증 만료)

Stop 훅에 의해 .md 기록 후 종료 지시. bg 에이전트는 인증 만료로 #11 미진행 → 재인증 + 재기동은 사용자 권한 작업.

---

## 10. 후속 진행 (Mac 측, 2026-05-12 추가 작업)

사용자 "go" 한 마디로 #11 (E-1 follow-up) 재개. Mac 측에서 직접 작업.

### 10.1 commit `76494ad3`

`feat(eeg): E-1 follow-up Phase 1 — substrate dispatch flag + argv portability` (11 files, +247 / −5).

### 10.2 산출물

| Path | 변경 |
| --- | --- |
| `eeg/collect.hexa` | `--substrate <brainflow\|synth\|replay>` + `--legacy-inline` 가산. Default brainflow 무손상. synth/replay = pointer mode (verdict=DEFERRED). `_flags_only_argv` host-portability 패치. |
| `eeg/eeg_recorder.hexa` | 동일 surgery. |
| `eeg/dual_stream.hexa:211` | Phase-5 forward-look 코멘트를 `replay_substrate` 가리키도록 갱신. 동작 무손상. |
| `eeg/substrates/{substrate,synth,brainflow,replay,channel_set}_substrate.hexa` | `_flags_only_argv`에 `hexa_interp` strip 추가. |
| `design/substrate_abstraction.md` | §8 landing record + Phase 1/2 분리 + 검증 매트릭스. |
| `CHANGELOG.md` | Unreleased에 E-1 follow-up Phase 1 + dual_stream + design doc 항목 추가. |
| `state/license_firewall_checks.jsonl` | 3개 ledger row (이번 세션 license-check 실행). |

### 10.3 검증 (Mac 측, 직접 실행)

| Case | 결과 |
| --- | --- |
| `license-check --selftest` | 3/3 PASS |
| `collect --selftest` (default) | 12/12 PASS — byte-identical 회귀 |
| `collect --selftest --legacy-inline` | 12/12 PASS |
| `collect --selftest --substrate {synth,replay}` | exit 0, verdict=DEFERRED |
| `collect --selftest --substrate bogus` | exit 2, reason=substrate-invalid |
| `collect --collect --substrate synth ...` | exit 2, Phase-2 reject |
| `eeg_recorder --selftest --substrate synth` | exit 0, verdict=DEFERRED |
| `substrate.hexa --selftest` | 6/6 PASS |
| `synth_substrate.hexa --selftest` | 7/7 PASS |
| `replay_substrate.hexa --selftest` | 8/8 PASS |
| `bin/check_licenses.sh` (real scan) | 205 files, 0 violations |

총 48/48 in-test assertion PASS + 5 honest-deferral case (의도된 verdict=DEFERRED / exit 2).

### 10.4 환경 정직 disclosure

1. **hexa 런타임 sandboxing**: `hexa run`이 job.hexa를 `/tmp/resource-tcp-XXXXX`로 복사 후 isolated cwd로 실행. `pwd` 안에서 본 cwd가 `/tmp`라 nested `hexa run eeg/substrates/<X>.hexa`가 relative path를 못 찾음 → 빈 stdout. 이게 Phase 2 deferral 사유. 해결책: (a) shim에서 `HEXA_PROJECT_ROOT` env export, (b) shim의 path-translation table 활용, (c) nested run 대신 python3 직접 호출.
2. **eeg_recorder default `--selftest` 실패 (pre-existing)**: 이 Mac box에 `.venv-eeg/bin/python` 부재 → 헬퍼 subprocess `rc=127`. ubu-2 (Sprint 1 commit `77484267` 검증 호스트)는 .venv-eeg 있어서 PASS였음. 본 PR과 무관 — 가산 변경만 했음.
3. **argv[0] portability**: hexa-real interp가 darwin에서 `/home/aiden/.hx/bin/build/hexa_interp` 형태 argv[0] 방출 (Linux 빌드 디렉토리 경로가 그대로 노출됨 — 빌드자=aiden, 실행자=ghost. cross-platform shim 추정). 기존 `_flags_only_argv`는 `.hexa`/`/exe` 두 패턴만 strip. `hexa_interp` strip 추가가 본 PR에 포함됨 (collect/recorder + 5 substrate 모두).

### 10.5 미완 (사용자/Phase 2 결정 대기)

| 항목 | 차단 요인 |
| --- | --- |
| #11 Phase 2 — collect/recorder의 BoardShim 라인을 `brainflow_substrate.api_open_session`로 완전 위임 | 실 하드웨어 (OpenBCI Cyton+Daisy + .venv-eeg) regression 필요. 본 세션 환경엔 불가. |
| Nested `hexa run` 서브프로세스 작동 | hexa 런타임 shim에 `HEXA_PROJECT_ROOT` 또는 path-translation 노출 필요. |
| Contract `v0 → v1` 승급 | 위 둘 다 closure 필요. |
| #12 C-1 NES adapter | 사용자 NES upstream probe (변동 없음). |
| `dual_stream.hexa`의 real `compare_streams_from_files(anima_npy, eeg_npy)` | nested run 작동 후. |

---

## 11. 세션 종료 사유 (2차 — Phase 2 차단)

Phase 1 dispatch 안착 완료. Phase 2 (full BoardShim 위임 + nested-run shim fix)는 환경/하드웨어 차단. 정직한 DEFERRED 마커 + design doc §8 + CHANGELOG 모두 본 commit `76494ad3`에 반영.
