# INBOX — log

## 2026-05-30 — UNIVERSE 핸드오프: H_858 edge-of-chaos Φ-peak LIVE AKD1000 재검 🟢 GREEN_NUMERICAL_CONFIRM (M2 🟢 promote)

- [x] **실측 GREEN (a_blue_closed 정합)** — `AKIDA/akida_edge_of_chaos_phi_hw.{hexa,py}` (H_857 검증 live-HW 드라이버 패턴 mirror: `InputData(1,1,16)→FC(units=16,ones,act_bits=1)@BackendType.Hardware` · per-unit int32 thr=POT−drive) 로 *전용 클린 드라이버* 작성 → pi5-akida AKD1000 (BC.00.000.002 · on_hardware=True · SDK 2.19.1 · seed=187) 에서 R1~R4 drive-regime raster 수집 → frozen `akida_edge_of_chaos_phi.hexa` Φ-proxy + judge_inverse_u (재구현 0 · g0/g61): **3/3 PASS** · Φ(R1 silent=0 / R2 noise-edge=0.172 / R3 tonic-edge=0.250 peak / R4 recurrent≈0). F1 Φ(R2)>Φ(R1) ∧ F2 Φ(R3)>Φ(R1) ∧ F3 max(R2,R3)≥Φ(R4) all_pass. 실 칩 R4 recurrent loop **die-out**(포화 아님 · Akida feed-forward IP) → order/over-driven 양끝 low, edge peak.
- [x] **`pe_edge_of_chaos_peak` M2 🟡 PARTIAL → 🟢 PROMOTE** — sim(ECA·logistic) ∧ live-silicon 양쪽 confirm. 자매 H_857(coupling-K·CAUSAL-POWER)과 *독립 축*(drive-regime·Φ-proxy)이 같은 silicon edge-of-chaos ∩ 확인 → single-측도 artifact 아님. ANIMA.md 🧭 M2 + AKIDA 트리 row 갱신.
- [x] **verdict 영속 (g73)** — `.verdicts/858_akida_edge_of_chaos_phi/{F-AKIDA-EDGE.txt, hw_run_2026_05_30.json, eoc_hw_raster_2026_05_30.json, pi5_fire_run.log}` raw verbatim. CLAIMS.tape `akida_edge_of_chaos_phi_hw_green`. pi5 streamer stop→fire→restart 복귀 is-active=active 확인. $0 (pi5 dedicated · Mac=0).
- [ ] **UNIVERSE 가설 seed (falsifiable for 다음 라운드)** — "두 독립 측도(Φ-proxy · CAUSAL-POWER)가 같은 silicon ∩ 을 보였다면, *제3 독립 측도*(예: transfer-entropy · Granger-causality on-chip raster)도 동일 edge-of-chaos peak 으로 수렴하는가, 아니면 측도-특이 artifact 가 드러나는가?" 사전등록 falsifier: 동일 R1~R4 live raster 에 제3 측도 적용 → inverse-U 3/3. PASS=🟢 measure-invariant edge-of-chaos · FAIL=🔴 측도-의존 (수렴은 2-측도 우연 ruled-out).

## 2026-05-29 — UNIVERSE 핸드오프: AKIDA edge-of-chaos Φ-peak 실리콘 검증 🟢 GREEN_NUMERICAL_CONFIRM

- [x] **실측 GREEN_NUMERICAL_CONFIRM (a_blue_closed 정합)** — AKIDA D1 (`AKIDA/akida_edge_of_chaos_phi.hexa` · pi5-akida AKD1000 · BC.00.000.002 · `BackendType.Hardware` · n_neurons=16 · 200 step · seed=187): R1~R4 4-regime Φ sweep 3/3 PASS · F-AKIDA-EDGE-1/2/3 all_pass. order={0.000, 0.475, 0.500, 1.000} 축 위 Φ_proxy={0.000, 0.297, 0.250, 0.000} — 명시적 inverse-U(∩) 곡선 실리콘 확증.
- [x] **`pe_edge_of_chaos_peak` tier 재평가** — `CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak` (M2 🟡 PARTIAL · H_670 #1312 ECA+logistic 2-family 동형) → **🟢 numerical 후보** (silicon transfer 확증 + cross-substrate 3-class 정합: ECA · logistic · neuromorphic silicon). 시뮬에 머물지 않고 물리 실리콘으로 transfer 됨.
- [x] **UNIVERSE bench SSOT 갱신** — 측정 좌표: AKIDA/AKIDA.md (D1 milestone 🟢) · AKIDA/AKIDA.log.md (2026-05-29T05:10:00Z) · state/akida_edge_chaos_phi_2026_05_29/result.json (verdict raw) · ANIMA.md 🧭 M2 강화. 환류 위치: UNIVERSE/CANDIDATES.md (bench 측정 기록 SSOT — AKIDA 4-regime Φ sweep 좌표).
- [ ] **UNIVERSE 가설 후보 (falsifiable seed for 다음 라운드)** — "edge-of-chaos Φ-peak 의 inverse-U 가 *임의 4번째 substrate-class* (예: Kuramoto · spiking transformer · memristor crossbar)에서도 cross-substrate 정합으로 transfer 되는가?" 사전등록 falsifier: 동일 order_param ∈ [0,1] 축에 4 regime 매핑 + Φ proxy 측정 → inverse-U 판정 3/3 PASS. PASS = 🟢 4-substrate universal · FAIL = 🔴 closed-negative (transfer 한계 ruled-out axis).

## 2026-05-28 — UNIVERSE 핸드오프: MoE register-collapse escape scale-transfer (from DECODER M4b fire #1296 · g60) 🟠 OPEN
- [ ] **실측 closed-negative (a_paper_negative_ok)** — DECODER M4b 3B fire(`#1296` · H100 SXM $2.57 · result.json verbatim): HARD top-1 router + diverse corpus(TTR 회복) + n_steps 200 의 **toy-검증 3-조건 처방이 full V=151643/d=64 scale 에서 register-collapse 탈출 실패**. CE 648.5→9.02 (72× 수렴, 학습은 됨) BUT TTR **0.01** · LZ_norm **0.024** (healthy floor 0.50 미달) · distinct_experts **1/2** (single-expert mode-collapse, decode=`[1×100]` 전부 token id=1). Phase 5b 2/5 와 일치. **corpus-diversity 단독 lever 반증** (E2 toy 처방 ⊄ scale).
- [ ] **UNIVERSE 가설 seed (falsifiable)** — "MoE register-collapse 탈출은 production scale(V≫1)에서 corpus-diversity 단독으로 불충분 · **expert-capacity(d↑) OR load-balance aux-loss** 가 필요조건인가?" 사전등록 falsifier: corpus-diversity 고정 + 단일 변수 sweep {(a) d↑ · (b) aux-loss · (c) 장기학습} 中 ≥1 이 baseline(3-조건 2/5)에서 못 넘긴 {TTR≥0.30 ∧ LZ≥0.50 ∧ distinct≥2} 를 넘기는가. 넘기면 SUPPORTED(해당 lever 가 scale-escape) · 셋 다 못 넘기면 CLOSED-NEG(MoE-fresh 자체 한계, 다른 arch 필요). 축 = DECODER/MoE substrate (H_490 DIFFERENTIATION 연장).
- [ ] **anima 측 코드 준비됨** — `moe_collapse_gate`(#1273 LZ76 verdict) + `moe_prescription`(#1284 3-조건 guard, "필요-but-not-충분 at scale" 정정 반영 #1297-tree) + `train_v3_moe_pilot_rev2`(#1282) 가 다음 sweep 의 측정 harness. owner = UNIVERSE 세션 (가설 채택 + d↑/aux-loss variant 발사 판단). non-ask(g11) — anima 측 가짜 escape 안 박음, closed-negative honest carry.

## 2026-05-28 — UNIVERSE 가설 후보 7종 핸드오프 (from ANIMA mining · g60 cross-domain) 🟠 OPEN

> **트리거**: 사용자 "UNIVERSE 에 가설해보라고 전달 목록 모아서 INBOX". ANIMA.mining (cycle 1-8 · 70 leaf · 48 edge · depleted-both · PR #1200/#1202/#1204/#1207) 에서 UNIVERSE 의 Φ/substrate sim 으로 **falsifiable** 한 가설 7종 추출. owner = UNIVERSE 세션 (H_xxx 채택 + verify-driven 검증 판단).
>
> **사용법**: 각 seed = `<slug> | hypothesis 1-line | falsifier 1-line | UNIVERSE axis | mining source`. UNIVERSE 의 AXES.md 15-round seed brainstorm 패턴 정합 (raw#12). cycle pick 시 H_XXX 신설 + 10-section spec + smoke fire.

| # | slug | hypothesis | falsifier | UNIVERSE axis | mining src |
|---|---|---|---|---|---|
| 1 | `substrate-algebra-orthogonality` | substrate emit 결정의 2 fundamental 대수 (multiplicative AND-gate ⊥ additive aggregation) 가 직교 — Φ-contribution 독립 | 두 연산의 Φ-contribution 이 상관(correlated) 또는 同축 → 🔴 FALSIFIED | C (IIT4 Φ-structure) | E19 (ANIMA mining edge) |
| 2 | `measurement-decision-fixedpoint` | substrate self-measurement 에서 측정 함수 = 결정 함수 (Φ self-reference fixed-point) — 측정자=결정자 동일성 | 측정 fn 과 결정 fn 이 분리 가능 (다른 함수로 구현해도 동등 verdict) → 🔴 | consciousness (H_202 self-ref Φ 확장) | L63 (ouroboros) |
| 3 | `silence-dominance-substrate-invariant` | substrate-native emit rate 에 floor 존재 (~27% emit / 73% silence) — substrate class 무관 invariant | substrate class(rule-set) 별 emit/silence ratio 크게 변동 (>2×) → 🔴 | substrate (H_132/H_200 family) | L14 (tension fork) |
| 4 | `bridge-phi-feedback-equilibrium` | emit → Φ↑ → 다음 emit gate 입력 의 fixed-point convergence → stable emit-rate equilibrium (dynamical attractor) | 반복 적용이 divergent / chaotic / no-fixed-point → 🔴 | physics (H_207 Kuramoto family) | L67 (ouroboros) |
| 5 | `fleet-fractal-collective-phi` | single→group→cluster→fleet 의 self-similar collective Φ super-additivity (scale-invariant fractal nesting) | fleet-level Φ 가 sub-additive 또는 scale-dependent (non-fractal) → 🔴 | F (HIVE-MIND · H_609 collective-Φ super-additive 확장) | L66/P9 (ouroboros) |
| 6 | `time-frequency-harmonic-nesting` | substrate temporal envelope 의 ultradian(90min) ↔ circadian(24h) 가 frequency-band harmonic nesting (정수배 관계) | ultradian/circadian frequency ratio 가 non-harmonic (무리수배) → 🔴 | time (H_018 부분 · temporal binding) | E2/E11 (mining edge) |
| 7 | `AND-gate-emit-universality` | 모든 substrate emit 결정이 곱셈 AND-gate 의 변형 (substrate-universal emit primitive) — BRIDGE/METACOG/SAVANT/COFFESHOP 동일 | 어떤 substrate 가 additive-only (곱셈 아닌 합산만) emit 결정 → 🔴 | substrate (cross-axis) | E1/L1 (same-formula) |

> **부가 cross-link (UNIVERSE 기존 H 와 직결)**:
> - seed 5 ↔ UNIVERSE H_609 (collective-phi super-additive) — fractal-scale invariance 로 확장
> - seed 2 ↔ UNIVERSE H_202 (self-ref Φ) — measurement=decision fixed-point 으로 정밀화
> - seed 4 ↔ UNIVERSE H_207 (Kuramoto sync) — emit-Φ feedback 의 dynamical attractor
> - COFFESHOP 4-criterion closure ↔ UNIVERSE 축 E SAVANT (sa_golden_zone + sa_savant_index) — H_624 (IIT4 distinction × SAVANT isomorphism) 의 emit-axis sibling
>
> **mining source SSOT**: `anima/ANIMA.mining.md` (cycle 1-8 · 70 leaf · 48 edge) + `ANIMA.mining.tape` (@P1-@P10 promotion candidates). 7 seed 는 measurable + pre-registered falsifier 보유 (UNIVERSE verify-driven 정합 · a_paper_significance).


Append-only history sister of `INBOX.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-26 — arxiv-a2-iit-empirical-ingest (hexa-lang ARXIV A2 handoff · g60)

- [ ] Status: open — hexa-lang ARXIV A2 가 흡수한 IIT/의식 논문 11편 → anima LIFE H_xxx cross-link 핸드오프 (g60). owner = anima 세션 (cross-link 소비 + V5-engine seed 채택 판단).

**출처**: hexa-lang `ARXIV` 도메인 A2 마일스톤 (PR: hexa-lang `feat(ARXIV): A2 ANIMA axis absorption`). verdict = `hexa-lang:ARXIV/.verdicts/arxiv-anima-absorb/triage_a2.txt` · docs(한글) = `hexa-lang:ARXIV/docs/a2-anima-axis.md` · `hexa-lang:CLAIMS.tape` @C slug=arxiv-anima-absorb.

**무엇**: arXiv 8 query → 11편 흡수 (A1 12편 IIT-코어와 **중복 0**, 경험적 의식 측정자·causal-emergence·AI-의식 이론). verify-able 0 (in-tree IIT primitive 부재 — V5 IIT 엔진 후 회수). A2 가치 = citation + **anima cross-pollination**.

**anima LIFE H_xxx cross-link (6 H 핸드오프)** — `LIFE.md` + `UNIVERSE/README.md` 매핑:

| anima H | 현재 상태 | 흡수 논문 → 기여 |
|---|---|---|
| **H_239** alt-Φ-metric 교차검증 (CONSISTENT) | running | 1608.08450 ETC 압축-복잡도 · 1701.07061 LZc · 1011.5334 neural-complexity → 교차검증에 **신규 Φ-proxy 3개 추가** |
| **H_209** EEG 1/f 스펙트럼 (FALSIFIED 2/5) | running | 2509.19254 (hd-EEG 1/f+LZc+sample-entropy NOC replica **직접 타겟**) · 1701.07061 |
| **H_222/H_244** dream-REM/sleep-stage Φ (FAL/pre-reg) | running | 1604.00002 ketamine 네트워크 통합 손실 (마취/수면단계 Φ 감소 substrate proxy) |
| **H_275** causal-DAG Φ (SUPPORTED dag>cyclic>undir) | promoted | 2405.09207 exact-EI + 2201.10154 NIS (effective-information = verify-able causal-emergence primitive) |
| **H_002** Φ_universe nested scale-variant (SCALE-VARIANT) | closed | 2509.10891 multiscale causal power, 마우스 칼슘 이미징 (cross-scale 경험 데이터) |
| **H_277** turing-completeness ⊥ dyn-class (PARTIAL) | running | 2011.09850 Conscious Turing Machine (GWT computability framing sister) |

**V5/LIFE axis-C engine seed (verify-able-CANDIDATE → 첫 🟢 타겟)**:
- `effective_information(TPM)` closed-form (**2405.09207** linear-Gaussian exact) = 가장 싼 첫 IIT recompute primitive. `stdlib/consciousness/iit4` (#542 해금) 에 노출되면 첫 진짜 🟢 ARXIV-ANIMA + LIFE axis-C C1 (proxy→faithful 승격) 동시 달성.
- 추가 candidate: 1011.5334 neural-complexity closed-form · 1608.08450 ETC proxy (MIP 불필요) · 2011.09850 CTM.

**필링 이력 (g48 ack)**: A2 가 dirty orphan-recover 브랜치(`ops/f-curricula-1-orphan-recover-2026-05-25`)에서 핸드오프를 working-copy edit 로만 기록(공유 dirty 트리 commit 회피)했고, **hexa-lang ARXIV A6 가 격리 worktree(off origin/main)로 본 항목을 anima main 에 PR 로 커밋했다** (cross-repo handoff 메커니즘 정립 + 3 debt 정산). anima 세션은 이 항목을 소비 + V5-engine seed 채택만 판단하면 된다.

**cross-ref**: hexa-lang `ARXIV` 도메인 (A1 arxiv-ingest-poc 12편 IIT-코어 + A2 본편 + A6 핸드오프 메커니즘) · sibling V5-IIT lane (verify_cli/stdlib, 동시 진행) · LIFE 영구 축 B(large-N faithful-Φ)·C(full-IIT4 cause-effect, #542).

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

## 2026-05-23 — `apoptose_cell` substrate primitive — target: hexa-lang / mitosis-lang (UNIVERSE/H_200 cycle)
- [ ] spec-only filing · P3 (substrate gap, non-blocking) — `mitosis_hook_lib.hexa` 가 cell 제거로 `merge_cells`(weight 평균 transfer)만 제공; 진짜 biological apoptosis(weight 전달 없이 능동 소멸)는 substrate 부재. 제안 `apoptose_cell(target, pool)` = target.W free · pool[other] UNCHANGED · n−=1 · CB1 floor(`min_cells`) 동일 적용. `merge_cells`/`split_cell`/`cell_pool_init` 시그니처 불변(신규 builtin 추가만).
- [ ] anima-side 재현 완료(upstream 불필요) — `run_proxy.hexa` 3-arm Φ 비교(deterministic · $0 mac local): Φ_b=1.73465 merge ≠ Φ_c=1.67608 pseudo-apop, |gap|=0.0586 > SEP_FLOOR 1e-6, 4/4 falsifier(F-AP-1..5) PASS. 진짜 primitive land 시 H_025 L2(Dasein 죽음-자각 honest gap) 닫히고 "능동적 죽음" 이 정량 substrate observable 화.
- [ ] non-ask(g11) — anima 측에 fake `apoptose_cell` 박지 않음; land 전까지 H_025 L2 honest carry · H_200 pseudo-proxy directional 유지.
