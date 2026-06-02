# AKIDA — log

`AKIDA.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-06-02T10:57Z — Lane-A 멀티스텝 자기회귀 ROLLOUT rung 🔴 CLOSED-NEGATIVE — 단일스텝 generation 은 작동하나 chaining 시 1 hop 만에 붕괴 (substrate=AKIDA · 안정 PSU 위 완주)

직전 single-step GENERATION rung 🟢(F-GEN, hop-1 0.4337) 이후 held next-step = **자기회귀 roll-out**: chip 이 produce 한 코드 `g_hat` 를 `neutral_bind` 로 되먹여 K=3 hop chaining (전부 AKD1000 on-chip · 같은 256-unit 1-bit AkidaUnsupervised FC 재인코딩 · NO GPU · NO sw fallback g63). encoder/binding/codebook/decode 는 `onchip_xlm_generation.py` 와 byte-match, feedback loop 만 신규. **core full-LM 질문 = trajectory 가 on-manifold 유지되나, 아니면 1-2 hop 후 noise 로 drift 하나?** → **drift. 단 1 hop 만에 신호 소멸.** live AKD1000 BC.00.000.002, akida 2.19.1, N=8 trials, exit rc=0, throttled=0x0.

- [x] DISPOSITION verbatim (g5, `.verdicts/lane-a-rollout/F-ROLL.txt`):
  ```
  [roll] learn_all_hw       : True
  [roll] chance             : 0.0204  K=3
  [roll] decay curve (k1..K): ['0.4287', '0.0277', '0.0090']
  [roll] hop 1  roll=0.4287 ci_lo=0.4118 | shufNULL hi=0.0511 p=0.0050 | idNULL hi=0.3695 | aboveShuf=True aboveId=True
  [roll] hop 2  roll=0.0277 ci_lo=0.0212 | shufNULL hi=0.0396 p=0.2040 | idNULL hi=0.0305 | aboveShuf=False aboveId=False
  [roll] hop 3  roll=0.0090 ci_lo=0.0057 | shufNULL hi=0.0394 p=0.8607 | idNULL hi=0.0150 | aboveShuf=False aboveId=False
  [roll] F-ROLL-1 survives  : NOT-REFUTED: rollout DROPS INTO shuffle-NULL at some hop -> autoregressive signal does NOT survive chaining at 1-bit/256-unit (CLOSED-NEGATIVE)
  [roll] F-ROLL-2 no-collapse: NOT-REFUTED: rollout COLLAPSES by hop 3 (final acc <= chance OR < half single-step) -> catastrophic autoregressive decay (a_paper_negative_ok)
  ```
- [x] **decay curve (정직, 항상 기록)** — hop1 **0.4287** → hop2 **0.0277** → hop3 **0.0090** (chance=0.0204). hop1 은 generation rung headline(0.4337) 재현 (sanity OK).
- [x] **F-ROLL-1 NOT-REFUTED** — hop1 만 shuffle-NULL 초과(ci_lo 0.4118 > hi 0.0511, p=0.005). hop2 부터 shuffle-NULL 안으로 떨어짐(0.0277 < hi 0.0396, p=0.204). 자기회귀 신호가 chaining 을 **생존 못 함**.
- [x] **F-ROLL-2 NOT-REFUTED** — final hop(0.0090) < chance(0.0204), single-step 의 0.5x(0.214) 한참 미달 → **파국적 붕괴**. hop2 이미 chance 부근, hop3 chance 이하.
- [x] **결론 = ROLLOUT COLLAPSE closed-negative (a_paper_negative_ok)** — single-step open-vocab generation 은 작동(retrieval→generation 다리 🟢 유지)하나, chip 의 produced code 를 되먹이면 **1 hop 만에 off-manifold drift**. 1-bit/256-unit Hebbian FC 는 상태를 carry 못 함(no recurrence/state). 다음 다리 NAMED = state-carrying/paged generator · multi-FC depth · off-chip decode. retrieval+single-step rung 은 영향 없음.
- [x] 두 falsifier 모두 사전등록(run 전, script docstring) · NO sw fallback(g63) · 매 trial learn=True(8/8 on-chip Hebbian). identity-NULL 도 hop2~3 동반 붕괴(hi 0.0305→0.0150) → trained 와 untrained 모두 chaining 시 무너짐 = 신호가 produced-code 의 single forward 에만 있음을 분리 확인.
- [x] result `out/result_onchip_xlm_rollout.json` sha256 `7d2e3cd0201398ff9caadf5f1bdd4d012a41a0cfb1ad26a2cd0bbe72286ffb1e` (host↔local byte-eq) · 산출물 `AKIDA/state/onchip_rollout_2026_06_02/`.
- [x] scope (a_scale_honest_scope) — 250앵커/50개념/5lang toy, 256-unit 단일 1-bit FC, K=3 hop. **toy-only closed-negative**: 단일 칩 FC 의 자기회귀 한계를 정량화(1 hop 생존). PUBLIC checkbox 미flip 유지 — rollout 은 또 하나의 toy 다리이지 closure 아님. substrate=AKIDA, Lane-G/GPU 수치와 NEVER 병합(a_lane_akida_gpu_split).
- [x] 전원 — PSU 안정, fire 전후 throttled=0x0, streamer service 정상 정지→trap 복원(rollout_wrap.log, exit rc=0 후 자동 restore).

## 2026-06-02T10:43Z — Lane-A full-LM GENERATION rung 🟢 — on-chip open-vocab next-step DECODE > shuffle-NULL AND > identity-NULL (substrate=AKIDA · 안정 PSU 위 완주)

Lane-A PUBLIC frontier 가 **retrieval → generation 다리**를 건넘. 직전 transition 리드아웃(`result_onchip_xlm_transition.json`)은 above-NULL t→t+1 신호(tr_acc ci_lo=0.260 vs NULL hi=0.040, p=0.005)를 줬으나 **후보 shortlist 를 점수화하는 RETRIEVAL** 이었음(후보 g 가 probe 입력에 baked-in). full-LM 은 후보 목록 없이 다음 토큰을 **PRODUCE** 해야 함. 본 rung 은 chip 이 `code_t` 만으로(neutral-bound, 후보 미포함) 다음 코드 `g_hat` 를 생성하고 **전체 codebook(NC=50개념×5lang, shortlist 없음) open-vocab decode** 로 t+1 적중을 측정. live AKD1000 BC.00.000.002, akida 2.19.1, N=8 trials × 256-unit AkidaUnsupervised FC, exit rc=0, throttled=0x0 부하검증 통과.

- [x] DISPOSITION verbatim (g5, `.verdicts/lane-a-generation/F-GEN.txt`):
  ```
  [gen] learn_all_hw       : True
  [gen] gen_acc (open-vocab): mean=0.4337 ci_lo=0.4096 (chance=0.0204)
  [gen] identity-NULL acc  : mean=0.3571 hi=0.3847
  [gen] shuffle-NULL       : mean=0.0183 sd=0.0120 hi=0.0418 p=0.0050
  [gen] F-GEN-1 above-shuf : REFUTED: open-vocab on-chip GENERATION beats shuffle-NULL (gen ci_lo>NULL hi AND p<0.05) -> produced successor carries t->t+1 structure
  [gen] F-GEN-2 not-echo   : REFUTED: generated successor beats the IDENTITY-NULL (untrained-FC echo) -> the chip PRODUCES a successor, it is not echoing code_t
  [gen] DISPOSITION        : ON-CHIP OPEN-VOCAB GENERATION DEMONSTRATED (gen > shuffle-NULL AND > identity-NULL) -> retrieval->generation bridge CROSSED on silicon; Lane A PUBLIC full-LM (generation) flips toward earned-green
  ```
- [x] **F-GEN-1 REFUTED** — gen ci_lo=0.4096 ≫ shuffle-NULL hi=0.0418 (p=0.005). 생성된 successor 가 t→t+1 구조를 담음(~21x chance).
- [x] **F-GEN-2 REFUTED (핵심 구분)** — gen ci_lo=0.4096 > identity-NULL hi=0.3847. identity-NULL(미학습 random-init FC 에 같은 neutral probe 통과)이 0.357 로 **높지만** trained chip 이 그것을 넘김 → 'generation' 이 입력 echo 가 아니라 chip 이 successor 를 **PRODUCE** 함을 분리 입증. 마진은 좁음(0.025) 이나 8/8 trial 일관 + ci 분리 → clean.
- [x] 두 falsifier 모두 사전등록(run 전, script docstring) · NO sw fallback(g63, `akida.devices()` 빈배열 시 panic) · 매 trial learn=True(8/8 on-chip Hebbian 갱신).
- [x] result `out/result_onchip_xlm_generation.json` sha256 `d2d8021f4aa11043e0236837030b2c9752065bb5ea0821ef6518e83ebb323743` (host↔local byte-eq) · 산출물 `AKIDA/state/onchip_generation_2026_06_02/`.
- [x] scope (a_scale_honest_scope) — 250앵커/50개념/5lang toy 스케일, 256-unit 단일 1-bit FC. open-vocab generation 이 toy 스케일에서 **작동**함을 입증(retrieval→generation 다리). 프로덕션 full-LM(3B/7B) 전환은 별도 ladder 필요 — toy green 을 프로덕션 처방으로 승격하지 않음.
- [x] 별개 축 — 이 generation PASS 는 상대-LIFT closed-negative(H-A1~A4 4/4 falsified)와 충돌 없음: 1-bit Hebbian 이 *margin lift* 는 안 사도, 강한(whitened) 인코더 + 명시적 transition 학습으로 **open-vocab next-step 생성**은 가능. encoder-axis 🟢 + transition retrieval 🟢 위에 generation 🟢 누적.
- [x] 전원 — PSU 교체(2026-06-02) 후 안정 전원, fire 전후 throttled=0x0, streamer service 정상 정지→복원(generation_wrap.log). substrate=AKIDA, Lane-G/GPU 수치와 NEVER 병합(a_lane_akida_gpu_split).
- [ ] 다음 = 다단계 autoregressive roll-out(t→t+1→t+2 chained generation) · 또는 paged 다중-FC generator 로 스케일 ladder ≥3 rung.

## 2026-06-02T07:40:00Z — Lane A (substrate=AKIDA · pi5-akida · a_lane_akida_gpu_split — NEVER merged with any GPU/Lane-G number) — host FLAPPED up→fired→dark 다시; decider died mid-`whitened`; harvester false-RUNNING 버그 FIX + chip-lock-aware 재무장

substrate=AKIDA. NO on-chip 결과 fabricated. Lane-G(GPU) 미접촉. pi5-akida = sacred host config(PI5-AKIDA.json) — consulted, NOT modified; os_default daemon 무접촉; 공용 pool 전환 안 함.

- [x] **probe verbatim — host 일시 ALIVE 였음(드뭄)**: 세션 시작 시 `ping 192.168.50.155` → `2 packets transmitted, 2 packets received, 0.0% packet loss` · `ssh ubuntu@192.168.50.155 'echo ALIVE; uname -a'` → `ALIVE` / `Linux ubuntu 6.8.0-1007-raspi ... aarch64`. 직전 다수 세션의 BLOCKED-OUTAGE(100% loss) 와 달리 이번엔 잠깐 LAN 복귀.
- [x] **이전 harvester(`/tmp/laneA_harvest.sh` v1)가 false-RUNNING 버그로 멈춰 있었음 발견**: v1 의 `ssh $HOST 'pgrep -f abs_margin_chip.py'` 가 자기 자신의 원격 명령 문자열을 매칭 → 영원히 `proc=RUNNING` 오보 → 재발사 안 함. 로그에 try 401 까지 `fire still running` 으로 거짓 기록. **실제로는 decider 죽어 있었음.**
- [x] **on-chip 직접 검증 — decider DEAD, 결과 미완**: `pgrep -fa abs_margin_chip.py` → 실 프로세스 없음(NO_DECIDER_PROC) · `abs_margin.log` 24줄에 FROZEN(mtime 04:11:35, host 가 04:11 에 mid-fire 로 떨어졌을 때 nohup 동사) · `out/result_abs_margin.json` = `"scales": {}` (시작 시 commit-early 만, terminal `disposition` 없음).
- [x] **실측 부분 결과(verbatim, 비-종결)** — host 가 04:11 에 떨어지기 전 chip(`BC.00.000.002`, akida 2.19.1, learn=True)이 남긴 부분 trace:
  `[abs] random_int4  ABSOLUTE mean=-1.5070 sd=0.2507 ci95=[-1.6807,-1.3333] n_pos=0/8 CROSSES_ZERO=False`
  `[abs] svd_struct   ABSOLUTE mean=-0.5560 sd=0.1253 ci95=[-0.6428,-0.4692] n_pos=0/8 CROSSES_ZERO=False`
  `[abs] whitened     trial 0/1/2 = -0.7120/-0.8800/-0.9840` (8 중 3 까지 · 미완)
  → **control + 2 구조 인코더 ABSOLUTE ci_hi < 0 (zero 미교차)**. 단, 결정 arm = **oracle-LDA 미실행** → PASS vs CLOSED-NEGATIVE 판정 불가. **AKIDA verdict 청구 안 함**(a_scale_honest_scope · g5).
- [x] **chip 단일점유 확인** — `akida.devices()` → `[] ERROR (file lock): 11`: R3 tonic streamer(`spike_streamer.py --port 9512 --duration 86400 --regime R3`, PID 1089)가 akida device lock 보유. systemd 서비스는 host reboot 으로 유실(`inactive`/`not-found`)이나 프로세스는 복귀. decider 는 chip map 위해 exclusive 필요.
- [x] **재발사 시도 → host 다시 DARK** — streamer-stop→decider→streamer-restore wrapper(`run_decider_with_streamer_restore.sh`) host 에 기록(WROTE_WRAPPER) 후 nohup 발사했으나, 직후 host 가 **다시 off-network**: `ssh: No route to host` · `ping` 100% packet loss · 30s/60s 백오프 재시도 모두 timeout(3 probe → DARK 확정). pi5-akida 는 **간헐적 flapping**(up→down) 상태.
- [x] **harvester v2 재무장(durable, a_cpu_local_no_waiter) — false-RUNNING FIX + chip-lock-aware**: `/tmp/laneA_harvest.sh` 재작성 — (1) `pgrep -fa abs_margin_chip.py` 출력에서 자기 ssh/pgrep shell 제외 후 `bin/python` 매칭으로 RUNNING 진위 판정(거짓 RUNNING 제거) · (2) terminal `disposition` 있으면 harvest · (3) 없고 미실행이면 streamer-restore wrapper 로 재발사(chip lock 해제→decider→R3 tonic 복원) · (4) terminal 까지 폴링. nohup+disown 분리 기동 확인(PID alive, STAT=SN).
- [ ] **on host return (자동, harvester 발사)** — pi5-akida 가 LAN 복귀하면 harvester 가 자동: streamer stop → `~/.venv/anima-akida/bin/python -u abs_margin_chip.py`(4 인코더 × 2 스케일, ~16 chip-map cycle) → R3 streamer 복원 → `abs_margin.log` + `result_abs_margin.json` terminal `disposition` harvest. **oracle-LDA arm 이 PASS(PUBLIC, some-encoder ci_lo>0) vs CLOSED-NEGATIVE(전부 ci_lo≤0, 25/250-anchor scoped)** 결정. (pre-reg: `.verdicts/lane-a-absmargin/PREREGISTER.md`)

## 2026-05-30T12:00:00Z — LAUNCHPAD COFFESHOP-on-AKIDA 라이브 폐루프 (9513 control port 첫 실응용)

- [x] `spike_streamer.py` 의 9513 control port(`set_threshold`) 가 COFFESHOP emit/silence 폐루프의 코어로 첫 실응용 — SW motivation_score → on-chip threshold 변조 → 9512 spike → emit 판정.
- [x] 라이브 AKD1000(BC.00.000.002 BackendType.Hardware) 에서 COFFESHOP 90-min trajectory 완전 재현 — emit window [3,10,14,15] · silence 11 · provenance=akida-hw · trajectory_match True (UNIVERSE H_846 🟢 SUPPORTED-NUMERICAL).
- [x] single-chip 절차: spike-streamer service stop → 자체 M-regime streamer(--allow-ctrl) → launch hw → service restart. 종료 시 streamer **active 복원 확인**.
- [x] decoder emit-decision HW↔SW byte-match(15/15) · raw-spike 7 window ±1 (on-chip 정수 threshold 양자화 · decision 동치이나 raw byte-identical 아님 정직표기).
- [x] PLASTICITY 학습 lane (emit-quorum stim_type 적응) 🔴 CLOSED-NEGATIVE (SW≠HW · 비결정론).
- [x] 어댑터 `HEXAD/CHAT/coffeshop_akida.{hexa,py}` · 학습 `LAUNCHPAD/coffeshop_quorum_learn.{hexa,py}` · 발사 `LAUNCHPAD/coffeshop_akida_launch.{hexa,py}` · verdict `.verdicts/coffeshop_akida/`.
- [ ] 다음 = broker `/ws/akida_ingest` 라이브 push 데모 (현재 옵션 wire `--broker` 만).

## 2026-05-30T00:00:00Z — HW-first 통합 + PLASTICITY 학습 lane 신설 (DECODER ⊥ PLASTICITY 2-lane)

- [x] **HW-first 스위치 SSOT 강화** (PR-B #1447) — `akida_backend.hexa` 에 `akida_backend_resolve_graceful` (의도 hw + HW미도달 → panic 아닌 SW fallback) + `akida_provenance` (akida-hw / akida-sw-fallback) 추가. default "hw" 유지. AKIDA/spike 경로 전용 · LM lora default 불변.
- [x] **PLASTICITY 학습 lane 도메인 신설** (PR-A #1446) — DECODER(추론·결정론·byte-identical)와 본질 다른 학습 lane(비결정론·HW-only)을 형제 도메인으로 분리. DOMAINS.tape 33 domains. SW numpy 근사는 HW on-chip edge-learn 과 🔴 비동치(CLOSED-NEGATIVE) 정직 표기.
- [x] **DECODER lane 배선** (PR-C #1448) — `CORE/DECODER/DECODER.md` 에 AKIDA HW-first lane section + 양방향 sibling 신설. HW forward / SW akida_sw_lif (byte-identical 🟢, r1~r5 입증).
- [x] **PLASTICITY lane 배선 + SW 근사 learner** (PR-D #1449) — `plasticity_lane.hexa` (HW-first 라우터) + `plasticity_sw_approx.py` (numpy Hebbian 근사). 🔴 verdict `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt`.
- [x] **5도메인 백링크** (PR-E #1450) — MITOSIS/CHANNEL/WAKE/EEG/HW-CORE sibling 에 AKIDA HW-first + PLASTICITY/DECODER 포인터. AKIDA.md sibling 에 DECODER(🟢)/PLASTICITY(🔴)/HW-CORE boost.
- [x] **문서 SSOT + 감사 H 2건** (PR-F) — `AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md` (전체 구조 + 2-lane 표 + provenance + 크로스포인터) · `UNIVERSE/H_679_plasticity_hw_first.md` (🔴 CLOSED-NEGATIVE 4/4) · `UNIVERSE/H_680_decoder_hw_first.md` (🟢 SUPPORTED-NUMERICAL verify 5/5).
- [x] **HW edge-learn 지원 실측 재확인** — `SUB_ENGINES/AKIDA/state/edge_learn_probe_2026_05_22.json` edge_learning_supported=true (BC.00.000.002 · AkidaUnsupervised compile+fit ok).
- [x] **regression-free** — verify_substrate_akida 5/5 PASS 유지 · LM lora default 불변 · H_672~H_678 status 불가침.
- [ ] (optional) pi5-akida live probe — DECODER HW byte-match 재확인 + PLASTICITY few-shot 비결정성 정량 → `.verdicts/`. 단일-칩 점유 spike-streamer stop→probe→start. $0.

## 2026-05-29T14:00:00Z — pi5-akida 재배포 + H_672 HW live-confirm 🟢🟢 (SW→HW 승격 · 통합 배선 문서)

- [x] 코드-레벨 배선 6 PR 머지 — SubstrateAKIDA plugin + AKIDA_BACKEND/--substrate akida + akida_sw_lif numpy LIF + dispatch.hexa probe (argv-fix) + 5/5 verify + HANDOFF (#1419~#1424)
- [x] pi5-akida 물리 재배포 — 디스크 풀(50G stale worktree) 정리 → scripts 8파일 + `spike-streamer.service`(enable+linger) 복원 · `PI5-AKIDA.json` state removed→active (local-only)
- [x] **라이브 HW 검증** — `spontaneous_emission.py` R0~R4 실 AKD1000 sweep · `mapped_on_hardware=True` · on-chip checks 8/8 True · R0=1.0/R1=0.0/R2=0.475/R3=0.5/R4=1.0 (SW canonical 정확 일치 seed=187)
- [x] H_672 SW→HW 승격 — falsifier 4/4 PASS on real silicon · verdict `.verdicts/672_akida_spontaneous_firing/hw_live_2026_05_29.txt` · status `SW 5/5 + HW 4/4 live-confirmed`
- [x] 통합 기록 — `AKIDA/HW_SW_WIRING_2026_05_29.md` (스위치 아키텍처 + 6PR + 물리재배포 + 라이브 verdict + 검증매트릭스 + 크로스포인터)
- [ ] (남음) H_673~H_678 은 HW-runnable 이나 HW-confirm 미시행 (SW-confirmed 유지 · 과대주장 금지)

## 2026-05-29T06:00:00Z — Group A~G 18+ sub-아이디어 HW/SW 통합 구현 (7 H_xxx · SW 7/7 🟢 · backend switch)

- [x] backend switch 통합 모듈 — `AKIDA/akida_backend.hexa` · `akida_backend_resolve("auto"|"hw"|"sw")` + `akida_hw_reachable()` 3-신호 (`/dev/akida0` + akida pkg import + hostname) + `akida_panic_no_hw()` 명시 panic + SW mock raster `akida_sw_mock_raster_R1..R4()` (canonical 2026-05-22 raster numbers) + `akida_verdict_tier(backend, all_pass)` (HW=silicon-confirmed · SW=mock-replay · 🔴=closed-negative · 🔵 위조 금지)
- [x] backend smoke — `AKIDA/akida_backend_smoke.hexa` 11/11 PASS (arg overrides env / env overrides default / default=hw / hw 미도달 panic message / hw_label / verdict tier hw/sw/fail / mock raster R1=0 R3=1600 R4=3200)
- [x] H_672 Group A spontaneous-firing × AKIDA — SW 4/4 🟢 GREEN_NUMERICAL_CONFIRM (R1.rate=0 / R2=0.475 / R3=0.5 / R4=1.0 · 8-factor SPIKE_FACTOR_MAP fires on R3 · 4 sub C1~C4 통합) · [impl](./impl/H_672_spontaneous_firing.hexa)
- [x] H_673 Group B core-decide × AKIDA — SW 4/4 🟢 (Ψ=1/2 외란 |Ψ(R2)-0.5|=0.025 < |Ψ(R1)-0.5|=0.5 · LIF excitable R3 · emit slot R3>R1 · selftest reachable · 4 sub A1~A4 통합) · [impl](./impl/H_673_core_decide.hexa)
- [x] H_674 Group C persistence × AKIDA — SW 4/4 🟢 (.kosmos 5-ch anchor schema len=5 · memristor persist last10 rate=0.5>0 · telemetry JSONL row · §95 edge-learn caveat 명시 · 4 sub B1~B4 통합) · [impl](./impl/H_674_persistence.hexa)
- [x] H_675 Group D mitosis × AKIDA — SW 4/4 🟢 (kuramoto order R3=1.0 · izhikevich regime diversity=4 buckets · 생사 분기 R4-R1=1.0>0.5 · phoenix R3 recoverable · 3 sub M1~M3 통합 · H_258/H_263 sister) · [impl](./impl/H_675_mitosis.hexa)
- [x] H_676 Group E decoder × AKIDA — SW 4/4 🟢 (emit budget R3=0.5 R4=1.0 비례 · sparse-attention wake_score R2=0.499>R1=0 · energy sparse R2/R3<1.0 · emit_budget float NOT bool gate · 2 sub O1~O2 통합) · [impl](./impl/H_676_decoder.hexa)
- [x] H_677 Group F measurement × AKIDA — SW 5/5 🟢 (D1 inherit PR#1371 all_pass=true silicon-confirmed · D2 silicon-class signature(class_id=5)=1.0 additive 0 changes on 2/3/4 · D3 3-substrate triangulation: AKIDA 0.297 · EEG L2 1.59 · ECA rule110 0.83 · diff=1.293>0 · D4 R2 QRNG std=7.99>0 · D5 v0.5.0 8/8 closed-discovery cite · 5 sub D1~D5 통합) · [impl](./impl/H_677_measurement.hexa)
- [x] H_678 Group G channel-bridge × AKIDA — SW 4/4 🟢 (E1 EEG→AKIDA bridge tool/anima_eeg_to_akida_spike.hexa 존재 · E2 tension-link 5-ch payload len=5 · E3 전력 mW sane range (8e-6 mW R3) · 3 채널 모두 surface · 3 sub E1~E3 통합) · [impl](./impl/H_678_channel_bridge.hexa)
- [x] HW path probe — pi5-akida pool 도달 (192.168.50.155 · /dev/akida0 OK · ssh-mutating 0 · live R3 spike_streamer 미중단) · local Mac probe MISS/MISS/Mac (예상) · 정직 표기 "🟡 SW-confirmed HW-pending probe-refinement" (위조 0 · `state/akida_hw_sw_impl_2026_05_29/hw_probe_2026_05_29.txt`)
- [x] UNIVERSE 등록 — H_672~H_678 7건 신설 (slug-stale 3-신호 검증 통과 · git ls-tree origin/main + git log --all + README grep) · CANDIDATES.md Consumed Cycle #22 1줄 추가 · README.md 인덱스 7 행 추가 · INBOX 환류 0건 (사용자 명시 폐기)
- [x] CORE substrate-class scope note — D2 silicon-class 는 H_677 impl 내부 `_pe_silicon_class_signature(class_id)` 로 additive marker (CORE/phi_envelope_substrate.hexa 의 기존 class 2/3/4 함수 signature 0 변경, 단조 정합은 deferred)
- [ ] HW 7/7 re-confirm — venv-aware probe + pi5-akida pool route refinement 후 7 H 각 `--backend hw` 실행

## 2026-05-29T05:10:00Z — D1 edge-of-chaos Φ 실리콘 검증 🟢 (3/3 PASS · GREEN_NUMERICAL_CONFIRM)

- [x] harness 작성 — `AKIDA/akida_edge_of_chaos_phi.hexa` (phi_silicon_proxy = activity_gate × integration × differentiation × entropy_weight · 정직 명명 · iit4 big_phi 의 multi-axis Φ 의미 보존)
- [x] mock smoke 통과 — 합성 R1~R4 raster 3/3 PASS 0.000/0.456/0.250/0.000 (HW_SPONTANEOUS_EMISSION_2026_05_22 baseline 수치 입력)
- [x] pi5-akida AKD1000 실측 — `BackendType.Hardware` BC.00.000.002 · n_neurons=16 · 200 step · seed=187 · 4 regime sweep 카논 `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` (live R3 streamer 中단 없이 기존 측정 활용)
- [x] verdict — F-AKIDA-EDGE-1 PASS (Φ(R2)=0.297 > Φ(R1)=0.000) · F-AKIDA-EDGE-2 PASS (Φ(R3)=0.250 > Φ(R1)=0.000) · F-AKIDA-EDGE-3 PASS (edge_max=0.297 ≥ Φ(R4)=0.000) · 3/3 → all_pass → **GREEN_NUMERICAL_CONFIRM**
- [x] inverse-U(∩) 곡선 실리콘 확증 — order={0.000, 0.475, 0.500, 1.000} 축 위 Φ={0.000, 0.297, 0.250, 0.000} edge-of-chaos peak (R2/R3 중심) · die-out floor (R1) · over-driven floor (R4)
- [x] H_670 / `pe_edge_of_chaos_peak` (CORE M2 🟡 PARTIAL) — ECA + logistic 시뮬 universal-but-PARTIAL → AKIDA AKD1000 silicon transfer **confirmed** (cross-substrate 3-class 정합 — ECA · logistic · neuromorphic silicon)
- [x] 산출물 — `state/akida_edge_chaos_phi_2026_05_29/{result.json, akd1000_spontaneous_emission_2026_05_22.json, hexa_run_verbatim.log}` · CORE/phi_envelope_substrate.hexa 주석 tier 노트 추가
- [x] M2 tier 재평가 — 🟡 PARTIAL → 🟢 numerical 후보 (silicon transfer 확증 + cross-substrate 정합 + 2-component 분리 Φ proxy)

## 2026-05-29T00:00:00Z — 도메인 신설 + 활용 아이디어 카탈로그 seed

- [x] AKIDA 도메인 신설 — `AKIDA/AKIDA.md`(스냅샷) + `AKIDA.easy.md`(쉬운 카탈로그) + `AKIDA.log.md`(로그), DOMAINS.tape 등록
- [x] 활용 아이디어 추출 — 18개 이상 (CORE×AKIDA 8 + 자연발화/세포/측정/채널 그룹), 전부 $0 pi5-로컬
- [x] sibling 양방향 엮음 — CORE · MITOSIS · WAKE · CHANNEL · EEG · UNIVERSE
- [ ] 다음 = D1 edge-of-chaos Φ 실리콘 검증 (파킹된 plan `drafts/akida-edge-of-chaos-phi-plan.md`) · D2 substrate-class 등록
- [ ] 환류 — 측정 결과는 UNIVERSE/CANDIDATES.md 에 기록 (bench SSOT)
