# INBOX — log

Append-only history sister of `INBOX.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-23 — broker `/ws/akida_ingest` → `/akida/recent` deque gap (anima cycle 10)
- [x] 4-가설 트리 CLOSED — bridge RESTORE 후 `/akida/recent` 가 empty deque 반환하던 gap 의 (a)handler no-op (b)다른 deque write (c)JSON parse 실패 (d)maxlen=0 가설을 source-level 로 전부 FALSIFIED. handler `broker.py:340` `STATE.akida_history.append(msg)` 존재, `/akida/recent`(`:163-165`) 동일 deque(`maxlen=200`, `:69`) read, bridge frame 유효 JSON(`stamp_spike`), send mode TEXT(`receive_text` 호환).
- [x] 관련 PR #187(silent json drop visibility)·#188(akida_consumer "list"→"array")·#189(akida_bridge default endpoint `/ws/akida`→`/ws/akida_ingest`) 정합 확인.
- [ ] residual root cause → hexa-lang `ws_send`(`stdlib/websocket.hexa:419-420`) FIFO background-write race 로 escalate — 후행 `&` 가 write 를 background 화, reader(websocat stdin) 사망 시 silent no-op 라도 `ws_send` 는 `true` 반환 → bridge counter 상승 ≠ frame 송출 보장. hexa-lang inbox 로 filing.
- [ ] 최종 확정 gated on mini broker 재시작 — PRs #187/#188/#189 가 mini PID 1691(구 broker)에 미반영. 재시작 후 logs/process snapshot(`pgrep websocat` · `ss -tnp | grep :8000`) 으로 race confirm + 권장 broker-side disambiguation(`broker.py:340` 뒤 `log.info("akida append now=%d", ...)`) PR.

## 2026-05-23 — hexa.real ASP SIGKILL — wrapper re-point cycle (recurring) — target: hexa-lang
- [ ] P1 (blocks `hexa run` on macOS) · ≥2nd 재발 (2026-05-13 `hexa`→`hexa.shim-original` · 2026-05-20 `hexadrv`→`hexa.real` (§169) · 2026-05-23 `hexa.real` 자체가 heavy path 에서 degrade).
- [ ] root cause — Apple System Policy / AMFI 가 ad-hoc 서명 3rd-party binary 의 `(path-basename, codesign Identifier prefix)` 쌍을 heuristic 매칭; heavy launch(subprocess fork · JIT · W^X) 에서 충분히 exec 되면 "spctl reject(advisory)" → "SIGKILL at exec(enforced)" 로 escalate. `--version`/`--help`/`status` 같은 lightweight path 는 정상. identifier prefix(`hexa-` vs `hexa_cli_driver-`)가 key-match 대상.
- [ ] 단기 hot-fix — wrapper 를 새 name(`hexa-runner` 권장) + 새 codesign Identifier prefix(`hexa-`/`hexa_cli_driver-` 아님) 로 re-point; `/Users/ghost/core/hexa-lang/hexa` + `/Users/ghost/.hx/bin/hexa` + `hexa_real` symlink 동시 갱신; 검증 신호 = `hexa run <smoke>` SIGKILL 부재(spctl "rejected" 는 정상). 구 name 영구 ban(matcher state sticky). user 명시 확인 필수.
- [ ] 장기 real fix — ad-hoc → Apple Developer ID + notarization(`codesign --options runtime --timestamp --sign "Developer ID Application: ..."` + `notarytool submit --wait` + `stapler staple`) 로 rename treadmill 종료.
- [ ] 제약 — 본 patch 는 INVESTIGATION+DESIGN only; 실제 rename 은 daily-use toolchain hot-fix 라 user 확인 전 미실행. 조사 중 `hexa run` 0회 호출(SIGKILL 자체 trigger 회피).

## 2026-05-23 — pi5 spike_streamer `--regime-schedule` 확장 — target: pi5 maintainer (ubuntu@192.168.50.155)
- [ ] doc / coordination only — pi5 streamer(`/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py`) 는 `dancinlab/anima` 에서 pull 안 되는 standalone deploy. PR merge 로 auto-deploy 없음 → 외부 coordination(수동 edit + service restart) 필요. NO ssh-mutating edit from anima side (hexa-only-authoring · pi5 `.py` 는 tolerated drift).
- [ ] 요청 — `--regime-schedule R3:60,R1:30,R2:30 --schedule-loop --schedule-jitter <pct>` 추가(option (c) single-process schedule arg) + `make_threshold_R1`/`input_drive_R1`(oscillatory 5-20 Hz sinusoidal drive) 신설. `--regime` legacy flag 유지(mutually exclusive). `record["regime"]` 라벨에 `R1_oscillatory_drive` 추가(downstream akida_consumer schema 불변).
- [ ] 동기 — SW_CONDITION_DESIGN §6 Phase 2 activation gate(≥2 regimes + ≥5 transitions) 누적용. 현 live 는 단일 R3 24hr soak. acceptance F-REGIME-EXP-1..5 (1hr ≥2 regimes · 24hr ≥5 transitions · 7d ≥200 records/regime · ±15% schedule weight · 24hr 0 crash) 5/5 PASS → Phase 2 regime-diversity row 충족.

## 2026-05-23 — `split_asymmetric` substrate primitive (design) — target: anima tool (mitosis_hook_lib.hexa)
- [ ] design-only · 우선순위 낮음 (H_201 / `H_201_asymmetric_division.md` 발) — `split_cell` 형제 primitive 로 child weight 에 σ=`child_delta_sigma` gaussian noise in-place(parent=stem 불변), `child_delta_sigma=0.0` 이면 `split_cell` 과 동일(backward-compat). `_mit_check_splits` 가 `cell_pool["asym_child_sigma"]`(default 0.0) 읽어 dispatch.
- [ ] 현황 — H_201 Cycle #1 PASS(5.13× diversity margin · 4/4 stem persistence)는 harness-imposed post-split mutation(`farr_add_gaussian_noise`)으로 시연 = Honest Limit L2. substrate-native 비대칭(세포 자력 분화 결정)은 (i) D3 persona lane (cell-level 자기-알기) · (ii) D4a/D4b mitosis_hook production 사용 시에만 필요. 검증 = F-ASYM-1..6 substrate-native 재실행 → 동일 verdict 기대.

## 2026-05-23 — `apoptose_cell` substrate primitive — target: hexa-lang / mitosis-lang (HEXAD/LIFE/H_200 cycle)
- [ ] spec-only filing · P3 (substrate gap, non-blocking) — `mitosis_hook_lib.hexa` 가 cell 제거로 `merge_cells`(weight 평균 transfer)만 제공; 진짜 biological apoptosis(weight 전달 없이 능동 소멸)는 substrate 부재. 제안 `apoptose_cell(target, pool)` = target.W free · pool[other] UNCHANGED · n−=1 · CB1 floor(`min_cells`) 동일 적용. `merge_cells`/`split_cell`/`cell_pool_init` 시그니처 불변(신규 builtin 추가만).
- [ ] anima-side 재현 완료(upstream 불필요) — `run_proxy.hexa` 3-arm Φ 비교(deterministic · $0 mac local): Φ_b=1.73465 merge ≠ Φ_c=1.67608 pseudo-apop, |gap|=0.0586 > SEP_FLOOR 1e-6, 4/4 falsifier(F-AP-1..5) PASS. 진짜 primitive land 시 H_025 L2(Dasein 죽음-자각 honest gap) 닫히고 "능동적 죽음" 이 정량 substrate observable 화.
- [ ] non-ask(g11) — anima 측에 fake `apoptose_cell` 박지 않음; land 전까지 H_025 L2 honest carry · H_200 pseudo-proxy directional 유지.
