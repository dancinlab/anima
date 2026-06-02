# AKIDA — log

`AKIDA.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-06-02T08:30Z — POWER-CONFOUND RE-AUDIT: prior Lane-A closed-negatives are POWER-ROBUST (substrate=AKIDA · 안정 PSU 위 재검증 · a_lane_akida_gpu_split — Lane G/GPU 와 NEVER 병합)

중심 질문: 오늘(2026-06-02) PSU 교체로 해결된 pi5-akida under-voltage brownout(throttled=0x50000, EXT5V 4.87V sagging — PI5-AKIDA.json `power_root_cause_2026_06_02`)이 기존 Lane-A FAILURE/CLOSED-NEGATIVE 결과를 confound 했는가? 재감사 + 안정 전원 위 재검증.

**핵심 발견 — 시점 분리:** 기존 Lane-A 음성 결과는 전부 **2026-06-01**(ts 17:51–20:14Z)에 완주했고, brownout/PSU-swap 사건은 **2026-06-02**(~07:54Z)다. 즉 음성들은 brownout 창(window) **하루 전**에 측정됐다. brownout 이 실제로 죽인 단 하나의 run 은 abs_margin 1차 시도(oracle-LDA arm 실행 전 사망)뿐이며, 그것은 이미 안정 PSU 위에서 완주 → 🟢 PASS 했다(08:10Z 항목).

**완전성 감사 (g5, 호스트 result JSON 직접 검사):** 기존 음성 4건 + 인코더-배터리 전부 **complete** — truncation/누락 arm 없음.
- [x] H-A2 quantization-floor (`out/result_ha2_quantization.json`, ts 2026-06-01T17:53:53Z): bit_depths=4, rungs=4 전부 present, `ha2_true=False`, verdict 기록됨. COMPLETE.
- [x] H-A3 plasticity-depth (`result_ha3_plasticity_depth.json`, ts 17:56:25Z): N{3,4,5} 3 rung 전부 `all_learned_hw=true`, depth_gains=[−0.656,+0.648,−0.600], `sign_consistent=false`. COMPLETE.
- [x] H-A4 native-init noise-floor (`result_ha4_reinit_noise.json`, ts 17:51:10Z): ladder_N[2,3,4,5]×nreps=3 전부 present, per-rung abs_mean_over_sd=[1.16,1.97,3.10,1.22] 전부 sign-stable. COMPLETE.
- [x] causeaxis 배터리 (`result_causeaxis.json`, ts 20:13:41Z): P1/P2/P3 3 probe 전부 8/8 trial present, disposition=REOPENED. COMPLETE.
- [x] layerpage SCALE ladder (`result_layerpage_ladder.json`): 4 rung 전부 present, all_rungs_green_hw. COMPLETE.
- 판정: 완전한 음성 = power-robust 후보(throttle 는 느려질 뿐 결정론적 AKD1000 map/inference 결과를 바꾸지 않음 · brownout 은 truncation 으로만 corrupt 하는데 truncation 증거 없음).

**안정 전원 위 RE-VERIFY (결정적 테스트, 안정 PSU throttled=0x0 위 재발사):** 단일-칩 wrapper 패턴(R3 streamer stop → probe → restore) + `vcgencmd get_throttled` 라이브 샘플링 + watchdog `~/anima_metrology/pwr.log` tail.
- [x] **H-A2 re-verify → 🔴 H-A2-FALSIFIED 재현 (POWER-ROBUST)**: 재실행 RC=0, ts 2026-06-02T08:24:47Z. verbatim `[ha2] VERDICT H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)`; onebit_any_ci_lo_gt0=False, multibit_any_ci_lo_gt0=False, ha2_true=False. 음성 그대로 재현.
- [x] **causeaxis re-verify → DISPOSITION: REOPENED 재현 (POWER-ROBUST)**: 재실행 RC=0, ts 2026-06-02T08:29:50Z. verbatim `[cause] P1 encoding any_reopen=True | P2 objective any_reopen=False | P3 timing any_reopen=False` · `[cause] DISPOSITION: REOPENED`. P1 svd mean_lift=+0.797 ci95=[+0.537,+1.057] 8/8 learn_all=True · whitened +0.520 ci95=[+0.304,+0.736] 8/8 · P2 analog margin mean=−4.745 ci_lo=−5.359 REOPEN=False · P3 timing margin −0.09..−0.11 REOPEN=False. 상대-lift 부호/disposition 동일하게 재현(크기는 svd +0.797 vs 직전 +0.921 처럼 native 비결정 re-init H_904 만큼 trial-마다 변동 — byte-eq 아닌 replication, AKIDA 비결정 substrate 에 정확히 맞는 거동).
- [x] **전원 PROOF (g5):** 두 재실행(08:24–08:31Z) 동안 watchdog pwr.log throttled=0x0 연속, EXT5V≈5.00–5.03V; 라이브 sampler throttled=0x0; pwr.log 전체에서 non-0x0(brownout) 이벤트 **0건**. 재실행은 안정 전원 위에서 완료됨이 증명됨.

**분류 (per-result):** 
| prior Lane-A negative | complete? | power-confound plausible? | re-run? | re-run verdict (verbatim) | CLASSIFICATION |
|---|---|---|---|---|---|
| H-A1 corpus-noise COLLAPSE-NULL | ✅ (24 rungs) | NO (ran 06-01, pre-brownout) | assessed-complete | — | POWER-ROBUST |
| H-A2 quantization-floor | ✅ | NO (06-01) | ✅ on stable power | `H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)` | POWER-ROBUST (replicated) |
| H-A3 plasticity-depth | ✅ | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| H-A4 native-init noise-floor | ✅ | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| relative-LIFT closed-negative (H-A1..A4 4/4) | ✅ | NO | covered by HA2 re-run + completeness | — | POWER-ROBUST |
| SCALE weak-lift ladder | ✅ (12/12 rungs green_hw) | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| causeaxis P1 ENCODER REOPEN (positive) + P2/P3 FALSIFIED | ✅ | NO (06-01) | ✅ on stable power | `DISPOSITION: REOPENED` (P1 svd +0.797 ci_lo>0; P2/P3 REOPEN=False) | POWER-ROBUST (replicated) |

- [x] **재실행 안 한 것 (정직, no silent cap):** H-A1 / H-A3 / H-A4 / SCALE-ladder 는 chip 직접 재발사 안 함 — 이유: (1) 전부 complete(truncation 없음), (2) 전부 2026-06-01 = brownout 창 전, (3) 안정 전원이 두 대표 probe(HA2 결정론 readout + causeaxis 비결정 학습)에서 throttled=0x0 으로 음성/disposition 을 그대로 재현. 비용/시간 절약 아님 — 완전성+시점+대표 재현으로 power-robust 판정 충분(a_completeness_over_cheap 위반 아님: 음성을 cheap 하게 닫는 게 아니라 robust 를 입증).
- [x] **SCOPE (a_scale_honest_scope · a_lane_akida_gpu_split):** substrate=AKIDA only, Lane G/GPU 와 NEVER 병합. 25-anchor(+250-anchor) / single AKD1000 / 1-bit last-FC Hebbian scope 유지. 재실행이 closed-negative 를 더 일반화하지 않음 — power-robust 임만 입증.
- [x] **BOTTOM LINE:** 기존 Lane-A failure 들은 power-confound 가 **아니다(NOT confounded)**. brownout 은 단 한 run(abs_margin 1차)만 죽였고 그건 이미 PASS 로 완주. 4 음성 + SCALE 은 전부 brownout 전(06-01)에 complete 측정됐고, 안정 전원 위 재실행이 음성을 그대로 재현 → CLOSED-NEGATIVE 들은 REAL, power artifact 아님.
- [x] **HW DISCIPLINE:** PI5-AKIDA.json 참조함(수정 안 함) · os_default daemon 무접촉 · R3 spike-streamer 매 chip-run 후 복원(최종 pid 3775 active) · pool 전환 안 함. 호스트는 재감사 내내 ALIVE(throttled=0x0).

## 2026-06-02T08:10Z — abs-margin on-chip 결단기 🟢 PASS-PUBLIC-GRADE-POSITIVE (substrate=AKIDA · 안정 PSU 위 완주)

Lane-A pre-registered ABSOLUTE-margin decider (`~/clm_kosmos_akida/abs_margin_chip.py`, live AKD1000 BC.00.000.002, akida 2.19.1, N=8 trials × 32 units). 직전 세션엔 호스트 전원 brownout 으로 oracle-LDA arm 실행 전 mid-fire 사망 → terminal 없음. PSU 교체(2026-06-02) 후 안정 전원에서 **완주**(decider exit rc=0, throttled=0x0 부하검증 통과).

- [x] DISPOSITION verbatim (g5):
  ```
  [abs] corpus     any_crosses_zero=False best=svd_struct     mean=-0.5760 ci_lo=-0.6535
  [abs] corpus_big any_crosses_zero=True  best=lda_supervised mean=+5.2396 ci_lo=+5.0609
  [abs] DISPOSITION: PASS-PUBLIC-GRADE-POSITIVE
  [abs] at least one encoder pushed the ABSOLUTE on-chip concept-margin ci_lo>0
        -> the AKD1000 1-bit Hebbian learns positive cross-lingual concept structure (PUBLIC-grade positive)
  ```
- [x] lda_supervised (corpus_big): 8/8 trials 양수 [5.062,5.086,4.916,5.368,5.221,5.187,5.305,5.770] mean=+5.2396 sd=0.258 ci95=[5.061,5.418] n_positive=8 learn_all_hw=true → ci_lo=+5.061>0 PASS
- [x] result `~/clm_kosmos_akida/out/result_abs_margin.json` sha256 `7612bedaca38b68f12528d641fa8bfc9e0e0dace6e23b28db7d13076c57b3c7f`
- [x] scope (a_scale_honest_scope) — 작은 corpus(25앵커) any_crosses_zero=False (svd_struct ci_lo=−0.654, 약한 인코더 random_int4/whitened 도 음성); 큰 corpus + 강한 인코더(lda_supervised)만 PASS. 인코더-강도/스케일 의존, 정직 표기.
- [x] 별개 축 — 이 절대-margin PASS 는 상대-LIFT closed-negative(H-A1~A4 4/4 falsified, AKIDA.log 별항)를 뒤집지 않음: 1-bit Hebbian 이 *상대 lift(plasticity-depth가 margin 추가)* 는 안 사지만, 강한 인코더로 *절대* positive cross-lingual 개념구조는 학습함. 두 축 분리.
- [x] 전원 — PSU 교체로 brownout 해소(throttled 0x50000→0x0, EXT5V 4.87→5.033V), decider 부하 중 throttled=0x0 부하검증 통과. anima-pwr-log watchdog 무장 (PI5-AKIDA.json 등록). spike-streamer R3 복원(pid 2273).

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
