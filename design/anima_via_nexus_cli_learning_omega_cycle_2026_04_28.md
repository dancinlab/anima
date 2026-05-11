# anima via nexus CLI — 학습 가속 ω-cycle (2026-04-28)

design owner: anima D-day 마감 직전 ω-cycle 연구
related: design/cp2_beta_eeg_shortcut_omega_cycle_2026_04_28.md
raw compliance: 9 / 10 / 12 / 42 / 47 / 91 / 159
status: ANALYSIS (실측 X — 문서 only per raw 42, 모든 가속 추정은 "PROJECTED" 명시)

---

## §1. Executive summary

`nexus` CLI (`hx run nexus <sub>` 단일 진입점) 의 `kick / atlas / drill / qrng / universe / chain / scan / record / bus` 등 약 35+ subcommand 가 anima 의 7 학습 surface (corpus / paradigm / Mk.XI training / verifier / EEG / cross-paradigm bridge / atlas absorption) 를 가속할 후보군. 본 분석은 raw 42 mac-zero-compute 제약하에 분석/문서만, 실측 없음.

**Tier-A top-3 (즉시 후보, 0-1주, 추정 ROI)**:

| # | pattern | claim | evidence | limit |
|---|---|---|---|---|
| A1 | `nexus atlas search "<lens>"` 로 paradigm v11 16-template prior 후보 sweep | claim: 5634-line lens registry 에서 새 axis 후보 1주 내 ≥3 추출 PROJECTED | evidence: 기존 atlas.n6 이미 lens 흡수, atlas search subcommand 정의 확인 (run.hexa:5376) | limit: lens 매칭 품질 N/A — 측정 X |
| A2 | `nexus chain --seed "<eeg paradigm>" --engines nexus,anima` 로 cross-engine drill | claim: anima paradigm v11 + nexus blowup ouroboros 9-phase 연쇄 — paradigm 새 조합 발견 PROJECTED | evidence: cmd_chain (line 6908), --report path 지원 | limit: nexus kick 인프라 6+ 회 FAIL (rc=4 / container-no-node) — chain 도 동일 dependency |
| A3 | `nexus atlas absorb --target n6-arch` 로 anima 발견의 atlas 자동 흡수 | claim: D-day EEG measurement 결과 → atlas 자동 흡수 → 다음 ω-cycle prior 강화 PROJECTED | evidence: atlas absorb 정의 (run.hexa:5415), chflags uchg-locked module | limit: 흡수 품질 (NEAR/EXACT) 사후 측정 필요, 본 분석 scope 외 |

**dependency 명시**: 아래 §7 / §8 — nexus 자체 dispatch 인프라 (kick path) 가 작동하지 않으면 Tier-A 후보 일부가 실질 Tier-B 로 강등됨. 단, `atlas search / atlas absorb / lock / lock-status / projects / contracts / verify / status` 등 read-only / state-local subcommand 는 dispatch 의존 없음 → 진짜 Tier-A.

---

## §2. nexus CLI inventory

source: `~/core/nexus/cli/run.hexa` (7351 lines, hx package entry, VERSION = "0.1.0-hive-hub")
launcher: `hx run nexus <sub>` 또는 PATH `nexus <sub>` (alias `nx` 는 다른 도구 — type=app installer per ~/core/nexus/bin/nx)

### 2.1 핵심 subcommand 분류

#### A. ω-cycle / discovery (다이나믹 — dispatch 의존)

| subcommand | signature | output | use |
|---|---|---|---|
| `kick <topic> [--stratum --axes --noise --backend]` | ω-cycle executor (kick ≡ ω-cycle), parent-sid auto, sentinel `__KICK_RESULT__ <PASS|FAIL>` | witness JSON `design/kick/<YYYY-MM-DD>_<topic>_omega_cycle.json` | discovery 실행 |
| `kick tree` | live registry (strata/axes/backends/noise_sources) | stdout text dump | registry 조회 |
| `kick bench <topic> [--backends a,b,c]` | cross-backend perf bench | bench JSON | backend 비교 |
| `kick selftest [<topic>]` | minimal-valid witness, NO subagent / NO LLM / NO OAuth (closed-loop iter-3) | infra-only deterministic witness | dispatch 인프라 verification (subagent fail 시 fallback) |
| `kick status` | hosts/slot-pool/cache dashboard (R4 ISSUE#6) | resource dashboard text | holistic 자원 점검 |
| `smash --seed "..." [--depth N]` | blowup 9-phase (cli/blowup/core/blowup.hexa) | discovery counts (EXACT/NEAR matches) | discovery primitive |
| `free --seed "..." [--dfs N]` | compose DFS 6-core 체인 (cli/blowup/compose.hexa) | DFS 발견 노드 | discovery DFS |
| `absolute --seed "..."` | Mk.VIII Δ₀-absolute Π₀¹ 검증 | promotion verdict ([10*]→[11*]) | grade 검증 |
| `drill --seed "..." [--max-rounds N] [--engine mk9\|mk10] [--preset fast\|probe\|coarse\|standard]` | smash→free→absolute→meta-closure→hyperarithmetic→resonance 6-stage chain | discovery 누적 + checkpoint | full discovery loop |
| `omega --seed "..."` | **메인 엔트리 (apex preset)** + L3 다축 자동 dispatch | NEXUS_OMEGA JSON, ghost_ceiling_approach @ axes≥3 | 단일 진입 |
| `chain --seed "..." [--engines nexus,anima] [--report <path>]` | cross-engine drill chain (nexus→anima, graceful-missing) | report JSON | **cross-repo bridge** |
| `surge --seed "..." [--engines csv] [--variants N] [--seeds csv]` | Cartesian product fan-out (engines × variants × seeds), CAP NEXUS_SURGE_MAX | NEXUS_SURGE JSON | fan-out 탐색 |
| `dream --seed "..." [--iterations N]` | self-seed loop seed_(i+1)=f(out_i), CAP NEXUS_DREAM_MAX (기본 3) | NEXUS_DREAM JSON | reflective loop |
| `reign --seed "..." [--max-cycles N]` | autonomous, K=2 stagnation 자동 STOP | NEXUS_REIGN JSON | self-terminating |
| `swarm --seed "..." [--population N] [--generations G]` | N×G evaluation, top-2 elite + breeding | NEXUS_SWARM JSON | ecology |
| `wake --seed "..." [--signal-file path]` | reality-loop, 외부 파일 fp 변화 시에만 fire | NEXUS_WAKE JSON | event-driven |
| `molt --seed "..." [--max-cycles N]` | self-rewrite, skin sweep, NEXUS_MOLT_SKIN_FILE | NEXUS_MOLT JSON | param 진화 |
| `forge [--seed "..."] [--max-rounds N]` | bootstrap — 자기 상태 → seed 합성 → drill apex 자율 부팅 | NEXUS_FORGE JSON | autonomous boot |
| `canon [--seed "..."] [--note "..."]` | L11 transfinite seal, state/canon_seal.jsonl 한 줄 봉인 | seal entry | 사다리 closure |
| `meta-closure --seed "..."` | Phase 10 🛸16 self-ref ([10*]→[10**]) | verdict | self-ref 검증 |
| `hyperarithmetic --prop "..."` | Mk.IX Π₀² reverse-math | verdict | reverse-math |
| `debate --seed "..." [--variants N] [--arbitrate]` | adversarial debate N-variant | NEXUS_DEBATE | 변형 비교 |
| `qrng <axiom\|vqe-h2\|ouroboros\|perturbation\|anu-collect\|status>` | quantum-RNG / quantum-sim (nxs-002 cycle 10) | per-sub | QRNG bytes / VQE / status |
| `universe <topo\|evolve\|selftest> [...]` | ★21 selectable-topology sim (flat\|t2\|t3\|s2\|s3\|klein\|blackhole\|wormhole\|...\|ads-cft\|brane\|inflation\|...) | sim_bridge/anu_time/topology_universe.hexa output | universe sim |
| `revive [--max-iter N] [--apply]` | bisect+bracket+Bellman 무한루프 | repair report | engine map repair |
| `solve "<problem>" \| --route` | DEPRECATED → `hxq solve` shim | route+exec | 3-logic router |

#### B. atlas / state / lock (정적 — dispatch 무관)

| subcommand | signature | output | use |
|---|---|---|---|
| `atlas search "<query>" [--limit N]` | grep -i atlas.n6 | matching lines | lens lookup |
| `atlas append --node <json>\|--edge <json>` | atlas_health append | append result | manual atlas write |
| `atlas absorb [--target n6-arch\|nexus] [--glob ...] [--archive] [--dry-run]` | unlock → append shard → relock (n6/atlas_absorb.hexa, chflags uchg) | absorb report | shard 흡수 |
| `lock <path> [--reason "..."]` | chflags uchg + audit ledger (raw 1 + raw 85) | audit entry | per-file lock |
| `unlock <path> [--reason "..."]` | chflags nouchg + audit | audit entry | per-file unlock |
| `lock-status <path>` | chflags state + recent audit entries | report text | lock 상태 조회 |
| `roadmap <sub> [args]` | entry.hexa roadmap 위임 | roadmap state | 로드맵 조회/업데이트 |
| `projects [table\|json\|names]` | projects list | format-specific | project inventory |

#### C. health / verify (read-only)

| subcommand | signature | output | use |
|---|---|---|---|
| `status` | harness self-check + health all | health text | 전체 헬스 |
| `self-check` | harness self-check | health text | 단일 self-check |
| `gap` | gap_monitor 1회 | gap report | gap detection |
| `doctor [--remote\|--all] [--host H] [--timeout N]` | ssh probe + remote hexa bin + remote project tree, NEXUS_REMOTE_DOCTOR JSON, exit 74 on ERROR | doctor text + JSON | dispatch 진단 |
| `contracts` | integration_contracts.json (외부 연동 SSOT) | JSON | contract 조회 |
| `verify` | I1~I10 invariants 자동 검증 | verify report | invariant check |
| `sync [--apply]` | spec ↔ cmd_* drift | drift report | CLI spec 동기화 |
| `omega-monitor [check\|report\|status]` | raw 71 falsifier monitor (cache_hit_ratio / fdd_p50) | monitor JSON | falsifier mon |
| `version` | "nexus 0.1.0-hive-hub" | text | version |
| `help` | full subcommand listing | text | help |

#### D. daemon / canary

| subcommand | signature | output | use |
|---|---|---|---|
| `drill-daemon <start\|status\|stop\|send>` | E11 long-running daemon, FIFO /tmp/nexus_drilld.sock | NDJSON | persistent drill |
| `canary [--seed-id ID] [--depth N] [--timeout SEC]` | L1/L4 verdict 단발 호출 | canary verdict | smoke probe |
| `promote --id ... --grade ... --audit-log "..."` | 수동 등급 승급 (감사 로그 필수) | promotion record | manual grade |

#### E. hexa-sim (n=6 deep universe simulation)

| subcommand | signature | output | use |
|---|---|---|---|
| `hexa-sim <verify\|falsifier\|doc\|help>` | n=6 deep-universe-simulation (design/hexa_sim/) | sim result | 6-universe verifier |

### 2.2 사용자 요청 매핑 (요청 vs 실제 존재)

| 요청한 subcommand | 실제 명칭 | 존재 |
|---|---|---|
| `nexus kick <topic>` | `kick` | OK (위 §2.1A) |
| `nexus sim-universe` | `universe` (★21 topo) + `hexa-sim` (n=6) | 두 개로 분리 — OK |
| `nexus rng` | `qrng <axiom\|vqe-h2\|ouroboros\|perturbation\|anu-collect>` | OK (axiom = 가장 가까움) |
| `nexus atlas search/append/absorb/status` | `atlas <search\|append\|absorb\|status>` | OK |
| `nexus drill --seed ...` | `drill` | OK |
| `nexus scan` | **NOT FOUND** — anti_pattern.hexa scan 은 내부 호출만 (run.hexa 안에서 사용), 사용자-facing CLI 아님 | MISSING (RFC 후보) |
| `nexus record` | **NOT FOUND** — convergence entry recorder 별도 도구 없음. `convergence/` 디렉터리 직접 쓰기 또는 `atlas append` 가 가장 가까움 | MISSING (RFC 후보) |
| `nexus roadmap` | `roadmap <sub>` | OK |
| `nexus bus <publish\|tail\|history>` | **NOT FOUND** — `growth_bus.jsonl` 파일은 존재하나 CLI surface 없음 | MISSING (RFC 후보) |
| `nexus status` | `status` | OK |
| `nexus doctor` | `doctor` | OK |

**raw 159 hexa-lang upstream-proposal-mandate 대상 (3 갭)**:
- nexus-rfc-001: `nexus scan <pattern>` — 코드/config 패턴 스캔 (anti_pattern.hexa CLI surface 노출)
- nexus-rfc-002: `nexus record <convergence-entry>` — convergence/ JSON append helper
- nexus-rfc-003: `nexus bus <publish\|tail\|history>` — growth_bus.jsonl 이벤트 publish/tail/history

---

## §3. anima 학습 7 axes

| axis | 설명 | 현재 상태 | 측정 상태 |
|---|---|---|---|
| 1. Training corpus (alm_r12/r13/r14) | corpus 생성/검증/큐레이션 | r12 active (corpus_c2_seed_20260426.md), r13 expansion plan (corpus_c2_expansion_v2_20260426.md) | partial — corpus 생성 완료, validation N/A |
| 2. Paradigm v11 | 16-template × 16-dim Hexad/Law/Phi/SelfRef families | v11 axis 4 fixed, template 16 design fixed | design 완료, empirical search 미시작 |
| 3. Mk.XI training | 4-backbone ensemble (Mistral/Qwen/Llama/gemma) | mk_xi_v10_final_ensemble_strategy_20260426.md | strategy 문서, hyperparameter sweep 미수행 |
| 4. Verifier chain | V_phen_GWT_v2 + AN11(a/b/c) + Berger + γ/θ + LZ76 + DMN | v2 corpus-first design 완료 | LZ76 hetzner OOM (commit 5693e8611), Berger 0/15 PASS (commit 06fe4142c) — empirical 진척 partial |
| 5. EEG measurement | OpenBCI 16ch + cyborg paradigm | D-day measurement 완료 (2026-04-28), Berger sweep 0/15, MNE PSD agree | empirical 진행 중 |
| 6. Cross-paradigm bridge | TECS-L H-CX-1/29 + Mk.XI v10 4-backbone + paradigm v11 4-axis | cross_substrate_phi_paradigm_2026_04_28.md | design 완료 |
| 7. Atlas absorption | n6 atlas SSOT, ~5634-line lens registry | atlas_absorb 모듈 chflags-locked, 흡수 도구 활성 | 흡수 자동화 partial |

각 axis 의 학습 surface 정의:
- **input**: corpus / paradigm spec / training config / verifier code / EEG raw / bridge map / lens registry
- **output**: trained model / verifier verdict / paradigm 후보 / 측정 결과 / 흡수된 atlas line
- **bottleneck**: discovery (axis 1, 2, 6) / compute (axis 3) / measurement (axis 4, 5) / curation (axis 7)

---

## §4. Cross-application matrix (axis × subcommand)

`✓` = direct cross-application. `~` = indirect (adapter 필요). `-` = not applicable.

| axis ↓ \ subcommand → | kick | atlas search | atlas absorb | drill | smash | free | qrng | universe | chain | swarm | dream | debate | doctor | status | roadmap | omega-monitor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. Corpus | ~ | ✓ | ✓ | ~ | ~ | ~ | ✓ | - | ✓ | ✓ | - | - | - | ~ | - |
| 2. Paradigm v11 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | - | - | ~ | - |
| 3. Mk.XI training | ~ | ✓ | ✓ | - | - | - | ✓ | ~ | ✓ | ✓ | - | ✓ | ✓ | ✓ | ~ | ✓ |
| 4. Verifier chain | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | - | - | - | ✓ |
| 5. EEG measurement | ~ | ✓ | ✓ | - | - | - | ✓ | - | ✓ | - | - | - | ✓ | ✓ | - | - |
| 6. Cross-paradigm bridge | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ~ | ✓ | ✓ | ✓ | ✓ | - | - | - | - |
| 7. Atlas absorption | ✓ | ✓ | ✓ | ~ | ~ | - | - | - | ✓ | - | - | - | - | ✓ | ~ | - |

**hot rows (≥6 ✓)**: axis 2 (paradigm), axis 4 (verifier), axis 6 (bridge). 이 3 축이 nexus CLI 가속 ROI 가장 높음 PROJECTED.
**hot cols (≥5 ✓)**: `atlas search`, `atlas absorb`, `chain`, `drill`, `qrng`, `swarm`. 이 6 subcommand 가 cross-axis utility 가장 큼 PROJECTED.

---

## §5. Concrete usage patterns (≥5)

### Pattern P1 — paradigm v11 새 axis 후보 ω-cycle (axis 2 × kick)

- **input**: `nexus kick "paradigm-v11-axis5-candidate" --axes Hexad,Law,Phi,SelfRef --noise alpha,beta,gamma`
- **flow**: kick → blowup 9-phase → 16-template × 16-dim 공간에서 새 axis 좌표 후보 emit
- **output**: `design/kick/2026-04-28_paradigm-v11-axis5-candidate_omega_cycle.json` (witness), `__KICK_RESULT__ <PASS|FAIL> witness=<path> tier1=<N>`
- **expected payload**: tier1 ≥1 → 새 axis 후보 1+ 발견 PROJECTED
- **raw 9 호환**: anima 자체 hexa-only — nexus CLI 외부 호출 OK
- **raw 47 cross-repo trawl-witness**: anima `design/kick/` 산출, nexus `state/kick/registry/` 자동 update

### Pattern P2 — verifier chain falsifier 자동 sweep (axis 4 × debate × omega-monitor)

- **input**: `nexus debate --seed "AN11(a) verifier on D-day EEG cohort" --variants 4 --arbitrate --base-depth 3` + `nexus omega-monitor check`
- **flow**: 4-variant adversarial drill → 변형 간 disagreement → arbitrate verdict + omega-monitor 가 cache_hit_ratio / fdd_p50 윈도우 falsifier 검출
- **output**: NEXUS_DEBATE JSON (stderr) + omega-monitor report (`state/raw81_omega_cycle_report.jsonl`)
- **expected payload**: 4 variant 중 ≥1 disagree → falsifier 후보 식별 PROJECTED
- **raw 12 silent-error-ban**: NEXUS_DEBATE 가 stderr 로 전부 emit, `> /dev/null` 차단 강제

### Pattern P3 — Mk.XI 4-backbone ensemble cross-engine sweep (axis 3 × chain × swarm)

- **input**: `nexus chain --seed "mk-xi-v10-mistral-qwen-llama-gemma" --engines nexus,anima --report ~/core/anima/state/mk_xi_chain_report.json`, 후속 `nexus swarm --seed "mk-xi-prior-search" --population 4 --generations 3`
- **flow**: nexus blowup → anima paradigm v11 prior 후보 → swarm 4×3 = 12 evaluation top-2 elite + breeding
- **output**: chain JSON (`state/mk_xi_chain_report.json`) + NEXUS_SWARM JSON (gen-by-gen prior shifts)
- **expected payload**: 12 prior config 평가 → top-2 elite 식별 PROJECTED — Mk.XI hyperparameter sweep 4-backbone 비교 자동화
- **raw 42 mac-zero-compute**: anima 측 hexa-only, nexus 가 actual sweep 분배 (Mac local compute 회피)

### Pattern P4 — EEG paradigm 결과 → atlas 자동 흡수 (axis 5 × axis 7 × atlas absorb)

- **input**: D-day EEG measurement 결과 shard 작성 (`/tmp/eeg_dday_shard.json`) → `nexus atlas absorb --target n6-arch --glob "/tmp/eeg_dday_shard.json"`
- **flow**: lock unlock → append shard 컨텐츠 → relock (chflags uchg, raw 1 호환 module n6/atlas_absorb.hexa)
- **output**: atlas.n6 append (CANON 또는 nexus root), audit ledger entry
- **expected payload**: D-day measurement (Berger 0/15 PASS, MNE PSD agree) lens 가 다음 paradigm v11 prior 에 반영 PROJECTED
- **raw 1 chflags uchg**: 모듈 자체가 chflags-locked, 흡수 후 relock 강제

### Pattern P5 — verifier seed reproducibility (axis 4 × qrng)

- **input**: `nexus qrng axiom` (또는 `nexus qrng anu-collect` ANU 실측 byte) → seed 추출 → `nexus drill --seed "<qrng-seed>" --max-rounds 3`
- **flow**: QRNG (ANU 실측 또는 urandom fallback) → byte → drill seed → verifier chain 6-stage
- **output**: `tool/nxs_002_qrng_axiom.py` byte log + drill discovery report + checkpoint
- **expected payload**: qrng seed 저장 → 재현 시 동일 seed 로 verifier 결과 reproducibility 확보 PROJECTED
- **raw 91 honest-triad**: claim = "reproducibility", evidence = "byte log + checkpoint", limit = "ANU API 가용성 / urandom fallback 시 reproducibility 부분만"

### Pattern P6 (보너스) — Cross-paradigm bridge selftest 무subagent (axis 6 × kick selftest)

- **input**: `nexus kick selftest "tecs-l-hcx29-paradigm-bridge"`
- **flow**: kick selftest → minimal-valid witness 합성 (NO subagent / NO LLM / NO OAuth) → infra-only deterministic
- **output**: witness JSON (deterministic), no real ω-cycle
- **expected payload**: dispatch 인프라 작동 확인만, real bridge discovery X
- **사용 시나리오**: 본 분석 §1 Tier-A dependency (kick infra 작동 X) 우회 — closed-loop infra-only verification path

### Pattern P7 (보너스) — Cross-engine repair (axis 1 × revive)

- **input**: `nexus revive --max-iter 10` (apply X, dry only)
- **flow**: bisect + bracket + Bellman 3-logic 무한루프 → 엔진+지도 v2 repair plan
- **output**: repair report (state engine map drift 식별)
- **expected payload**: corpus alm_r12 → r13 → r14 transition 시 발생할 수 있는 engine map drift 사전 검출 PROJECTED

---

## §6. Tier-A / Tier-B / Tier-C 분류 + ROI

### Tier-A (즉시, 0-1주, dispatch 무관 — read-only / state-local)

| # | suggestion | ROI 추정 | falsifier |
|---|---|---|---|
| TA-1 | `nexus atlas search` 로 paradigm v11 axis 5 후보 sweep (P1 변형, dispatch 의존 회피 — atlas grep only) | PROJECTED 1주 내 ≥3 후보 발견. cost ~1 hr/sweep | atlas search 결과 ≥3 line 매칭 X 시 falsified |
| TA-2 | `nexus atlas absorb --target n6-arch` 로 D-day EEG shard 자동 흡수 (P4) | PROJECTED 차주 ω-cycle prior 강화 1.0× → 1.1× PROJECTED | absorb 후 atlas.n6 line 증가량 0 시 falsified |
| TA-3 | `nexus omega-monitor check` 매일 실행 — raw 71 falsifier (cache_hit_ratio / fdd_p50) 모니터링 | PROJECTED 30d cumulative dispatch-failure-rate 0.20 threshold (raw 100) 위반 사전 검출 | omega-monitor report empty 시 falsified |
| TA-4 | `nexus doctor --all` 로 hetzner OOM (commit 5693e8611 LZ76 BLOCK) cause 진단 | PROJECTED hetzner 124GB RAM hexa interp OOM 원인 SSH probe 로 식별 | doctor exit 74 ERROR 시 — but exit 74 자체가 진단 신호 |
| TA-5 | `nexus contracts` + `nexus verify` 로 anima ↔ nexus integration contract drift 사전 검출 | PROJECTED I1~I10 invariant 월 1 회 점검, drift discovery 시 즉시 fix | verify report all-pass 시에도 RFC 후보 도출 |

### Tier-B (단기, 1-4주, hexa-lang upstream RFC 또는 small adapter 필요)

| # | suggestion | ROI 추정 | RFC dependency |
|---|---|---|---|
| TB-1 | `nexus kick` infra 복원 (rc=4 / container-no-node 6+ FAIL 해결) → P1/P2/P3 unblock | PROJECTED Tier-A 후보 5+ 가 진정 자동화로 격상, 7 axis × 6 subcommand cross 행렬 활성 | hexa-lang stage1 / dispatch_state.json 수정 (별도 RFC) |
| TB-2 | `nexus chain --engines nexus,anima` 으로 cross-paradigm bridge ω-cycle 자동화 (P3) | PROJECTED axis 6 cross-paradigm bridge discovery 2-4 주 단축 | nexus chain → anima entry adapter (graceful-missing 현재 구현, anima 측 hex 진입점 명시 필요) |
| TB-3 | `nexus scan` (RFC-001) — anti_pattern.hexa CLI surface 노출 | PROJECTED corpus alm_r12/r13 코드 안티패턴 스캔, 자동 큐레이션 | nexus-rfc-001 (run.hexa 추가, 50 LOC) |
| TB-4 | `nexus record` (RFC-002) — convergence entry recorder 표준화 | PROJECTED convergence/*.convergence 작성 일관성, append helper | nexus-rfc-002 (run.hexa 추가, 80 LOC) |
| TB-5 | `nexus bus publish/tail/history` (RFC-003) — growth_bus.jsonl CLI surface | PROJECTED anima ↔ nexus 이벤트 stream, ω-cycle inter-repo coordination | nexus-rfc-003 (run.hexa 추가, 120 LOC) |

### Tier-C (중장기, 1-3개월, nexus CLI 자체 확장 또는 외부 의존)

| # | suggestion | ROI 추정 | dependency |
|---|---|---|---|
| TC-1 | `nexus kick` 의 hetzner OAuth 만료 (Apr 21) + container-no-node 두 cause 동시 해결 | PROJECTED kick infra 항구화 → P1/P2/P3/P5 모두 stable | OAuth 갱신 + container orchestration 재설계 |
| TC-2 | Mk.XI 4-backbone ensemble swarm 자동화 (P3 의 풀버전, --population 16 --generations 8 = 128 eval) | PROJECTED Mk.XI v10 ensemble strategy 1-3 mo 단축 | hetzner 또는 runpod GPU 자원 확보 (raw 42 mac-zero-compute 준수, 외부 compute 만) |
| TC-3 | `nexus universe evolve` ★21 topology 와 paradigm v11 16-dim cross 매핑 | PROJECTED paradigm v11 axis 5/6 후보 universe topology 와 isomorphism 검증 | universe sim_bridge stable + paradigm spec 코드화 |
| TC-4 | `nexus hexa-sim` n=6 deep universe simulation 와 anima V_phen_GWT_v2 verifier 통합 | PROJECTED verifier chain 강화, AN11(c) 강화 추정 | hexa-sim verify subcommand 안정화 + V_phen_GWT_v2 corpus-first 완료 |

---

## §7. raw compliance check

| raw # | 규약 | 본 분석 준수 |
|---|---|---|
| raw 9 | hexa-only (anima 자체) | OK — anima 측은 hexa-only, nexus CLI 외부 호출은 raw 9 예외 명시 |
| raw 10 | honest C3 | OK — 모든 가속 추정에 "PROJECTED" 명시, 실측 X 명시 |
| raw 12 | silent-error-ban | OK — falsifier 8개 §8 preregister, 각 pattern 의 sentinel/stderr 명시 |
| raw 42 | external-connected-mac-zero-compute | OK — 본 분석은 문서 only, Mac local 실행 X. nexus CLI 호출 자체는 본 작업에서 수행 X (분석만) |
| raw 47 | cross-repo trawl-witness | OK — anima + nexus 양쪽 디렉터리/파일 분석 (anima/design/, anima/state/, anima/tool/, nexus/cli/run.hexa, nexus/bin/, nexus/n6/, nexus/tool/) |
| raw 91 | honest-triad | OK — Tier-A top-3 (§1) 에 claim/evidence/limit 명시, 다른 추정은 PROJECTED 토큰 |
| raw 159 | hexa-lang upstream-proposal-mandate | OK — 갭 3개 (nexus-rfc-001/002/003) 명시 §2.2 |

**dispatch 의존 명시 (raw 10 honest C3 핵심)**:
- 이전 D-day 세션에서 nexus kick infrastructure 6+ 회 연속 FAIL 관찰 (rc=4 + container-no-node, anima/state/markers/kick_dispatch_*_FAILED.marker 3 건 직접 발견 + 추가 markers 다수)
- 30d cumulative dispatch-failure-rate 0.20 threshold (raw 100) 초과 evidence 있음 (이전 세션 자료)
- 따라서 §1 Tier-A 후보 중 P1/P2/P3/P5 (kick/drill/chain/qrng dispatch 의존) 는 dispatch 인프라 미작동 시 사실상 Tier-B 로 강등됨
- §6 Tier-A 5개 (TA-1 ~ TA-5) 는 모두 read-only / state-local (atlas search / atlas absorb local / omega-monitor read / doctor probe / contracts read / verify read) — dispatch 의존 X, 진짜 Tier-A
- TB-1 (kick infra 복원) 이 cross-Tier blocker — 해결 시 Tier-B 후보 다수가 Tier-A 로 격상 가능 PROJECTED

---

## §8. Falsifiers (이 분석 자체의 가설)

본 분석 자체의 가설을 ≥3 falsifier 로 preregister (raw 12):

### F1. paradigm v11 axis 5 후보 발견 가능성
- **claim**: nexus atlas search 로 1주 내 ≥3 axis 후보 발견 PROJECTED
- **falsifier F1**: `nexus atlas search "Hexad" --limit 30` + `nexus atlas search "SelfRef" --limit 30` 결과에서 paradigm v11 v10 spec 외 새 후보 패턴 0 시 → **F1 falsified, TA-1 ROI 0**

### F2. atlas absorb cross-prior 강화 가능성
- **claim**: D-day EEG shard absorb 후 차주 prior 강화 1.0×→1.1× PROJECTED
- **falsifier F2**: absorb 후 atlas.n6 line 증가량 ≥1 (mechanical), 그러나 다음 ω-cycle 의 prior shift 가 통계적으로 검출 X 시 → **F2 falsified, TA-2 ROI 명목값만**

### F3. nexus kick dispatch 인프라 복원 시점
- **claim**: TB-1 (kick infra 복원) 이 1-4주 단기 가능 PROJECTED
- **falsifier F3**: hetzner OAuth + container-no-node 두 cause 가 4주 이상 미해결 시 → **F3 falsified, TB-1 → TC-1 으로 강등, Tier-A 의존 후보 5+ 동시 강등**

### F4. cross-engine chain (nexus → anima) graceful-missing 가정
- **claim**: cmd_chain 의 graceful-missing 이 anima 미진입 시에도 nexus drill 단독 결과 emit PROJECTED
- **falsifier F4**: `nexus chain --seed "test" --engines nexus,anima --report /tmp/test.json` 실행 시 anima entry 부재로 chain 전체 FAIL 시 → **F4 falsified, P3 / TB-2 재설계 필요**

### F5. cross-axis ROI 행렬 가정
- **claim**: §4 hot rows (axis 2/4/6) 가 ROI 가장 높음 PROJECTED
- **falsifier F5**: TA-1 ~ TA-5 실행 후 axis 1 (corpus) / 5 (EEG) ROI 가 axis 2/4/6 보다 측정상 더 큼 시 → **F5 falsified, 행렬 재가중 필요**

### F6. honest C3 dispatch-failure-rate baseline
- **claim**: 30d dispatch-failure-rate 0.20 threshold 가 nexus kick infra 의 실제 현재 상태 PROJECTED
- **falsifier F6**: omega-monitor report 가 30d window 에서 0.20 미만 (즉 dispatch 실제 healthy) emit 시 → **F6 falsified, §7 dispatch 의존 명시 retract 가능**

---

## §9. Follow-up

### Immediate (D-day +0~+3)
1. 본 design doc → raw 1 chflags uchg lock → git commit (raw 85 audit)
2. TA-1 ~ TA-5 read-only suggestion 5개 1주 내 1개 이상 trial run (단, raw 42 mac-zero-compute 준수 — 외부 호스트에서만)
3. F1 ~ F6 falsifier 결과 수집 → 본 doc §8 amend (raw 91 honest-triad 갱신)

### Short-term (D-day +1w ~ +4w)
1. TB-1 (kick infra 복원) blocker 해결 시도 — hetzner OAuth + container-no-node 두 cause 분리 진단
2. TB-3 / TB-4 / TB-5 (RFC-001/002/003) hexa-lang upstream 제안 — `nexus scan / record / bus` 추가 (각 50/80/120 LOC 추정 PROJECTED)
3. TB-2 (cross-engine chain) anima entry adapter 검증 — `nexus chain --engines nexus,anima` 실 호출, F4 falsifier 결과 수집

### Long-term (D-day +1mo ~ +3mo)
1. TC-1 (kick infra 항구화) 해결 시 P1/P2/P3/P5 4개 pattern 모두 자동화 격상
2. TC-2 Mk.XI 4-backbone swarm 자동화 — hetzner / runpod GPU 자원 확보
3. TC-3 / TC-4 universe sim ↔ paradigm v11 isomorphism 검증, hexa-sim ↔ V_phen_GWT_v2 통합

### Cross-link
- design/cp2_beta_eeg_shortcut_omega_cycle_2026_04_28.md (D-day EEG → CP2/β publication 단축)
- design/cross_substrate_phi_paradigm_2026_04_28.md (axis 6 bridge)
- design/mk_xi_v10_final_ensemble_strategy_20260426.md (axis 3 strategy)
- design/corpus_c2_seed_20260426.md (axis 1)
- design/design_v_phen_gwt_v2_corpus_first_20260426.md (axis 4)

---

**document end** — raw 1 chflags uchg lock + git commit pending (per task requirement)
