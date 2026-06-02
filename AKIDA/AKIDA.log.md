# AKIDA — log

`AKIDA.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-06-02T09:40Z — FULL-LM TRANSFER 탐침 🟡 CAPACITY-GAP CHARACTERIZED (substrate=AKIDA · live AKD1000 · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU)

검증된 primitive(whitened 비지도 인코더 + 1-bit Hebbian abs-margin readout)를 실제 on-chip 교차언어 **시퀀스/next-token** 작업으로 가교 — corpus_big 50 concept 은 연속 FLORES 문장(시간축 t)이라는 사실을 이용. live AKD1000(BC.00.000.002, akida 2.19.1, N=8, throttled=0x0 부하검증 완주, R3 streamer stop→run→복원 pid 9686).

- [x] **사전등록 falsifier 2건 (실행 前 선언, g63 — HW only, SW fallback 라벨 금지)**:
  - F-LM-1 (headline): "whitened+1-bit Hebbian 은 NULL 위 on-chip 교차언어 NEXT-SENTENCE 예측을 못 낸다" (next ci_lo>shuffle-NULL hi AND p<0.05 시 REFUTED)
  - F-LM-2 (margin→retrieval bridge): "margin readout 이 same-concept 교차언어 retrieval 도 못 산다"
- [x] **DISPOSITION verbatim (g5, `xlm.log`)**:
  ```
  [xlm] same_acc          : mean=0.1300 ci_lo=0.1195 (chance=0.0200, above=True)
  [xlm] next_acc          : mean=0.0306 ci_lo=0.0234
  [xlm] shuffle-NULL next : mean=0.0207 sd=0.0093 hi=0.0389 p_next=0.1542
  [xlm] F-LM-1 next       : NOT-REFUTED: next-sentence acc within shuffle-NULL -> primitive does NOT transfer to a sequence LM at this 1-bit/32-unit capacity (CLOSED on LM axis at this scale)
  [xlm] F-LM-2 same-bridge: REFUTED: margin readout DOES buy above-chance same-concept cross-lingual retrieval
  [xlm] DISPOSITION       : CAPACITY-GAP CHARACTERIZED: primitive binds cross-lingual CONCEPTS (same-concept>chance) but has NO learned TIME/sequence model (next-sentence at NULL) -> Lane A PUBLIC stays open; named next-step = a sequence/recurrent readout beyond the 1-bit static margin (paged/temporal layer)
  ```
- [x] **F-LM-2 REFUTED (bridge HOLDS)** — same-concept 교차언어 leave-one-lang-out top-1 retrieval mean=0.1300 ci_lo=0.1195 vs chance 1/50=0.0200 → **6.5x chance**, 8/8 trial learn-on-chip live. 검증된 abs-margin readout 이 실제 사용 가능한 교차언어 concept retrieval 로 전이됨.
- [x] **F-LM-1 NOT-REFUTED (시퀀스/시간 모델 부재)** — next-sentence(t→t+1) mean=0.0306 ci_lo=0.0234; shuffle-NULL(B=200, concept→time label permute) mean=0.0207 hi=0.0389 p=0.1542 → next-acc 가 NULL 밴드 내. 1-bit/32-unit 정적 Hebbian readout 은 시간/시퀀스 구조를 학습하지 못함.
- [x] **scale-ladder addendum 25/125/250 (a_scale_honest_scope ≥3 rung, 실 FLORES 부분집합 — 위조 corpus 0)** verbatim (`xlm_scale.log`):
  ```
  [scale] c25   SAME mean=0.2200 ci_lo=0.1808 chance=0.2000 above=False | NEXT mean=0.2750 null=0.2445 p=0.3483 above=False
  [scale] c125  SAME mean=0.1470 ci_lo=0.1338 chance=0.0400 above=True | NEXT mean=0.0458 null=0.0402 p=0.4030 above=False
  [scale] c250  SAME mean=0.1410 ci_lo=0.1297 chance=0.0200 above=True | NEXT mean=0.0265 null=0.0206 p=0.2388 above=False
  [scale] same-lift curve 25/125/250: [0.020, 0.107, 0.121]
  [scale] F-SCALE-1: PARTIAL: bridge above chance at some but not all rungs
  [scale] F-SCALE-2: NULL HOLDS at every rung -> capacity gap (no time model) is scale-robust
  ```
  - same-concept bridge lift-over-chance 가 scale 로 **성장** (+0.020→+0.107→+0.121; 25앵커 5-concept 는 small-n 으로 chance 동률, 125·250 은 결정적 above) — 검증된 margin 곡선과 일치.
  - next-sentence NULL 이 **전 3 rung 에서 유지** → 시간 모델 부재는 scale-robust (250-only artifact 아님).
- [x] **CAPACITY-GAP 특성화 (PUBLIC-grade on-chip CLM 이 필요로 하는 것 — closed written result, a_paper_negative_ok)**: AKD1000 의 1-bit 마지막-FC Hebbian primitive 는 (1) 교차언어 CONCEPT 결속을 학습(margin·6.5x-chance retrieval, scale-survives)하나 (2) **학습된 TIME/sequence transition 모델이 없음**. PUBLIC-grade on-chip CLM 으로 가는 named next-step = 정적 1-bit margin readout 너머의 **시퀀스/recurrent readout** — (a) 시간축을 입력에 인코딩(t·t+1 페어를 명시 입력하는 transition probe) (b) paged/멀티-FC 레이어로 transition matrix 를 on-chip 보유 (c) on-chip(개념결속) ⊥ off-chip(시퀀스 디코드) 분할. 현 단일 AKD1000 1-bit last-FC 용량으로는 정적 readout 까지가 한계.
- [x] **전원 proof** — throttled=0x0 두 fire(WRAP start/fire/exit 전 구간) 부하검증 통과 · pwr.log EXT5V≈5.01–5.05V 64–67°C(brownout 0) · spike-streamer R3 복원(pid 9686, 86400s tonic). 두 fire 직렬 단일-칩 점유, R3 stop→run→restore 패턴.
- [x] **artifact** — `SUB_ENGINES/AKIDA/state/fulllm_transfer_2026_06_02/`: result_onchip_xlm_seq.json sha256 `74b8ba10b61672a2510fc640d509a2275ff8acdb4bb594ccd7be8b778270c227` · result_onchip_xlm_scale.json sha256 `4a3e2623164757712f2844cb7f77b8cb84add83bdd1c126f0a1590f8adc56a9a` · 탐침 2건 + log/wrap 미러. probe = `SUB_ENGINES/AKIDA/onchip_xlm_seq{,_scale}.py` (repo SSOT) ↔ `~/clm_kosmos_akida/` (host).
- [x] **별개 축 (a_lane_akida_gpu_split)** — Lane A 전용 결과 · Lane G(GPU CE-descent)와 절대 병합 안 함.
- [ ] **다음 = transition-probe** — t·t+1 페어를 명시 입력하는 on-chip 교차언어 transition retrieval (시간축 인코딩 후 NULL 교차 시 Lane A PUBLIC 후보) · paged 멀티-FC readout 용량 탐침.

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
