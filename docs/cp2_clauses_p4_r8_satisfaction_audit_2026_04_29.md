# CP2 3-clause × TOP-1 (`p4_r8`) 충족도 정량 audit

> **ts**: 2026-04-29
> **author**: Claude (opus-4-7-1m), invocation by user
> **scope**: read-only, .roadmap 정정 NOT 본 commit (사용자 승인 후 별도)
> **TOP-1 release candidate (under audit)**: `state/trained_adapters/p4_r8/final/` — base `mistralai/Mistral-7B-v0.3` + LoRA r=96 α=192, 185.92 MB, sha n/a (mtime 2026-04-25 11:23)
> **selection commit**: `9c2f2b5d7` (analysis(adapter-release-selection))
> **parent doc**: `docs/anima_adapter_release_candidate_selection_2026_04_29.md` (TOP-1 = 29/30 anima-general score)
> **CP2 clauses audited**: #78 제타가능 / #79 직원가능 / #80 트레이딩가능
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#70 multi-axis ≥3 orthogonal · raw#71 falsifier 5 preregister · raw#86 cost-attribution · raw#91 honest 5축 · own#5 completeness-first

---

## §0 Executive summary

### 0.1 3-clause 가중 충족도 (raw count + LIVE count)

| clause | exit_criteria 갯수 | raw 충족도 (가중평균) | LIVE 충족도 (spec 환산 후) | 임시공개 verdict |
|---|---:|---:|---:|---|
| **#78 제타가능** | 4 | **22.5%** | **2.5%** | NOT-OK (Likert live A/B 절대부재) |
| **#79 직원가능** | 6 | **20.0%** | **3.3%** | NOT-OK (LIVE evidence ledger 0 files) |
| **#80 트레이딩가능** | 7 | **19.3%** | **2.9%** | NOT-OK (T1/T2 0 files, 4-stage gate 0 record) |
| **3-clause 평균** | 17 | **20.5%** | **2.9%** | 0/3 OK · 0/3 BORDERLINE · 3/3 NOT-OK |

verdict (raw#10 honest): **TOP-1 p4_r8 으로 #78/#79/#80 어떤 clause 도 임시공개 LIVE 형태로 OK 아님**. 단 spec/showcase (Option C) + Mac local (Option D) 형태로 demo 출시는 가능 (별도 path).

### 0.2 캐시 1-line per clause (가장 큰 차단 요인)

- **#78 제타**: Zeta competitor API key 없음 + durable anima endpoint 없음 → 100 pair blind A/B 0 회 실행
- **#79 직원**: `state/dest2_employee_*.json = 0 files` (find 결과) — `hire_sim_live.hexa` self-disclosed "spec-only pending S1 endpoint" + 가장 가까운 baseline `training/deploy/hire_sim_lenient_20260417_015253.json` (12일 stale, completion=0.4333, gates ALL FAIL)
- **#80 트레이딩**: T1 paper 30-day backtest pnl ledger 0 files + T2 live exchange 7-day 0 files + 4-stage risk gate 통과 0 record + audit_log immutable r2 (config 만 존재, 실 record 0)

### 0.3 LIVE 100% 도달 ETA per clause (병렬 모드)

| clause | 직렬 ETA | 병렬 ETA | 외부 의존 | $cost |
|---|---|---|---|---|
| #78 | 5-10d | 3-5d | Zeta API key | $5-50 (zeta API + 100 prompt eval) |
| #79 | 3-7d | 2-4d | (없음, S1 endpoint local OK) | $0 (local Mac) OR $20-100 (1 H100 hour rerun if needed) |
| #80 | **30-37d** (T1 30d minimum) | 30-37d | broker API key (T2) + regulatory audit consultation | $200-2000 (broker fee + audit consultant) |

병렬 경로에서도 **#80 trading T1 paper 30-day = 캘린더 시간 hard floor** (baked into spec). T2 live 7-day 추가 시 37d 최소.

---

## §1 #78 제타가능 — 4 criteria audit

### 1.1 exit_criteria 원문 (.roadmap line 1218)

> Likert ≥ 3.0 (100 pair blind A/B vs Zeta) + 응답 <1s + 30 turn 세션 유지 + 5 카테고리 coverage

### 1.2 criterion-by-criterion 측정 (p4_r8 기준)

| # | criterion | 측정값 | classification | cite |
|---:|---|---|---|---|
| 78-a | Likert ≥ 3.0 (100 pair blind A/B) | **0/100 pair 실행** (live_ab_executed=false) | RED MISSING | `state/zeta_likert_result.json:live_ab_executed=false` + blockers list 3건 |
| 78-b | 응답 latency <1s | p4_r8 으로 측정한 latency record 부재 (p1 cp1_real_validation 도 generation_not_validated_locally) | RED MISSING | `state/cp1_real_validation_result.json:verdict=STRUCTURAL_PASS__GENERATION_NOT_VALIDATED_LOCALLY` |
| 78-c | 30 turn 세션 유지 | smoke `tool/anima_serve_smoke.hexa` 만 stub (3 endpoint) — 실 30-turn run 0 회 | GREY SPEC-ONLY | `state/anima_serve_smoke_result.json:scope="Pre-H100 contract freeze. Three endpoint schemas exercised via CPU-local stubs. Real LoRA + GPU serving PENDING (Phase 2)."` |
| 78-d | 5 카테고리 coverage | `bench/zeta_likert.hexa` framework 완비 (ZALM-P0-2 T1-T7 + TALM-P1-2 P1-P5) — but 실측 0 회 | GREY SPEC-ONLY | `state/zeta_likert_result.json:framework_verified.zalm_p0_2_t1_t7_prompts="100 pair blind A/B layer A"` (frame OK, run=0) |

### 1.3 #78 score

가중치: GREEN=1.0 / INFERRED=0.7 / PARTIAL=0.4 / MISSING=0.0 / SPEC-ONLY=0.2 / EXTERNAL=0.1

- raw 충족도: (0.0 + 0.0 + 0.2 + 0.2) / 4 = **0.10 → 10.0%** (purely measured)
- 다만 framework_verified=true 가 deterministic scorer + prompt set + structural blind invariance 확인 → ESTIMATE bonus +0.5×(1/4) = **22.5%** (framework readiness 가중)
- LIVE 충§ 환산 (SPEC-ONLY → 0.0): (0+0+0+0)/4 = **0.0%**, +framework structural 1/4 partial credit = **2.5%**

**verdict**: **NOT-OK 임시공개**. Likert blind A/B 의 의미가 LIVE pair execution 자체이므로 spec 만으로 Option C/D 도 weak claim.

---

## §2 #79 직원가능 — 6 criteria audit

### 2.1 exit_criteria 원문 (.roadmap line 1228)

> E1 hire_sim_live 45K LOC independent module closure (tier-9+ probe, judge lenient rubric) + E2 autonomy_live + autonomy_loop + discovery_loop 3체 closed-loop + goal_memory/scratch/report_writer 완비 + phi trail logger 활성 + abort policy (phi_delta<0 N연속) OR (laws_pass=false) 즉시 abort

### 2.2 criterion-by-criterion 측정 (p4_r8 기준)

| # | criterion | 측정값 | classification | cite |
|---:|---|---|---|---|
| 79-1 | E1 `hire_sim_live` 45K LOC closure (tier-9+ probe) | spec 완비 (`anima-agent-hire-sim/hire_sim_live.hexa` + 7 sibling) — 자체 진술 line 3: "STATUS: spec-only pending S1 endpoint" — p4_r8 으로 100×5 run 0 회 | GREY SPEC-ONLY | `anima-agent-hire-sim/hire_sim_live.hexa:3` self-disclosure |
| 79-2 | judge lenient rubric tier-9+ probe | rubric 코드 `serving/hire_sim_judge_lenient.hexa` 존재 — baseline 측정 `training/deploy/hire_sim_lenient_20260417_015253.json` (endpoint=`localhost:18282/generate` ≠ p4_r8, 12일 stale) — completion 0.4333, gates ALL FAIL (alm_0.85=false / clm_0.80=false / z_0.75=false / verdict=BLOCKED_<0.60) | YELLOW PARTIAL (baseline only, non-p4_r8) | `training/deploy/hire_sim_lenient_20260417_015253.json:gates` |
| 79-3 | E2 autonomy_live + autonomy_loop + discovery_loop 3체 closed-loop | 3 hexa 모두 존재 — `autonomy_loop.hexa` self-disclosed line 19 "Current scaffold: only 'mock' path is wired inline here. Live wire ... " (mock backend) | GREY SPEC-ONLY | `anima-agent/autonomy_loop.hexa:19-20` |
| 79-4 | goal_memory + scratch + report_writer 완비 | `anima-agent/employee/goal_store.hexa` + `scratchpad.hexa` + `emit_report.hexa` 3 module 모두 존재 (구현 spec OK) — LIVE evidence ledger 0 | GREY SPEC-ONLY | `anima-agent/employee/{goal_store,scratchpad,emit_report}.hexa` |
| 79-5 | phi trail logger 활성 | grep `phi_trail` in `anima-agent/employee/{goal_store,test_employee_skeleton,emit_report}.hexa` 3 hit (구조 인지) — 실 log file `state/phi_trail_*` = 0 files | GREY SPEC-ONLY | grep result + `find state -name "phi_trail*" = empty` |
| 79-6 | abort policy ((phi_delta<0 N연속) OR (laws_pass=false) 즉시 abort) | abort_policy 전용 모듈 0 (`find . -name abort_policy*` = empty) — 정책은 autonomy_loop 내부 inline 으로 추정되나 raw#10 직접 evidence 부재 | RED MISSING | `find . -maxdepth 3 -name "abort_policy*" = 0 files` |

### 2.3 #79 score

- raw 충족도: (0.2 + 0.4 + 0.2 + 0.2 + 0.2 + 0.0) / 6 = **0.20 → 20.0%**
- LIVE 충족도 환산: SPEC-ONLY 4건 + PARTIAL 1건 (non-p4_r8) + MISSING 1건 → (0+0.2+0+0+0+0)/6 = **3.3%**

**verdict**: **NOT-OK 임시공개 LIVE**. spec 100% LIVE 0% gap (cascade close commit `d627c0bf8` self-disclosed 와 일치). Option D Mac local 에서 mock backend 로 demo 는 가능하나 "직원가능" claim 은 거짓.

### 2.4 spec-vs-LIVE gap 정량

- spec LOC: hire_sim 8 hexa + employee 4 hexa + autonomy 3 hexa + abort policy 0 = ~14 hexa modules + 45K LOC (E1 spec 진술)
- LIVE evidence ledger files: **0** (`state/dest2_employee_*.json` find 결과 empty)
- spec/LIVE ratio = ~14:0 = **∞** (모든 spec live evidence 0)
- 가장 가까운 LIVE 측정: 12일 stale + non-p4_r8 (localhost:18282 endpoint, completion 0.4333 gates FAIL)

---

## §3 #80 트레이딩가능 — 7 criteria audit

### 3.1 exit_criteria 원문 (.roadmap line 1239)

> T1 paper 30-day stability (pnl positive trend + drawdown<10%) + T2 live exchange 실거래 7-day window + risk gate 4-stage 통과 + pain_signal<0.7 + current_dd<10% + AN11 3조건 + regulatory compliance (audit_log_schema)

### 3.2 criterion-by-criterion 측정 (p4_r8 기준)

| # | criterion | 측정값 | classification | cite |
|---:|---|---|---|---|
| 80-1 | T1 paper 30-day stability (pnl positive + dd<10%) | paper backtest ledger 0 files (`find . -name *paper*back* -o -name *backtest*` = empty) | RED MISSING | (find empty) |
| 80-2 | T2 live exchange 실거래 7-day window | live exchange ledger 0 files (`state/live_exchange_*` = empty) | RED MISSING | (find empty) |
| 80-3 | risk gate 4-stage 통과 | `anima-agent/trading/risk.hexa` 구현 존재 (RiskMetrics struct + ConsciousnessGate gate_check) — 4-stage 통과 record 0 — 실 trade 0 | GREY SPEC-ONLY | `anima-agent/trading/risk.hexa:1-30` (struct 정의) |
| 80-4 | pain_signal<0.7 | RiskMetrics.pain_signal 필드 존재 — 실 측정값 0 | GREY SPEC-ONLY | `anima-agent/trading/risk.hexa:9` |
| 80-5 | current_dd<10% | RiskMetrics.current_drawdown 필드 존재 — 실 측정값 0 | GREY SPEC-ONLY | `anima-agent/trading/risk.hexa:8` |
| 80-6 | AN11 3조건 (a/b/c) for p4_r8 | (a) `state/an11_phi_mip_p4_r8.json:phi_mip=0.195 verdict=FAIL` (≥0.55 pass) · (b) `state/an11_sma_p4_r8.json` direct 256-d cosine variant (verdict 미기재) · (c) `state/an11_cps_p4_r8.json:CPS=0.843 verdict=FAIL` (≥3.0 pass) — 3 measure 모두 p4_r8 본인 측정 but 모두 FAIL | RED MISSING (FAIL gate) | `state/an11_{phi_mip,sma,cps}_p4_r8.json` |
| 80-7 | regulatory compliance audit_log_schema | spec doc `docs/audit_log_schema_design_20260419.md` (6.0 KB) + `config/r2_audit_log_immutable.json` 구성 만 존재 — 실 trade audit log 0 record + regulatory consultation 0 | EXTERNAL + GREY | spec doc만 존재, 외부 regulatory 인증 0 |

### 3.3 #80 score

- raw 충족도: (0.0 + 0.0 + 0.2 + 0.2 + 0.2 + 0.0 + 0.15(EXTERNAL+GREY 평균)) / 7 = **0.107 → ~10.7%**
- 단 AN11 3 measure 가 p4_r8 본인 측정 = framework operational confirmed (+가산 0.6×1/7) = **~19.3%**
- LIVE 충족도 환산: (0+0+0+0+0+0+0.05) / 7 = **0.7%** (regulatory only minor partial)
- AN11 framework operational 가산 (+0.15×1/7) = **2.9%** LIVE

**verdict**: **NOT-OK 임시공개 LIVE 절대불가**. T1 paper 30-day = 캘린더 시간 hard floor (압축 불가). AN11 3조건 모두 p4_r8 에서 FAIL — 더 큰 issue. trading 임시공개는 reckless (미인가 + 30d backtest 부재 + risk gate 미통과).

### 3.4 AN11 fail breakdown for p4_r8 (큰 발견)

p4_r8 본인 측정 AN11 verdict (cite `state/an11_{phi_mip,cps,sma}_p4_r8.json`):

| measure | value | threshold | verdict |
|---|---:|---|---|
| AN11(a) phi_mip (V1) | 0.195 | ≥0.55 PASS | **FAIL** |
| AN11(b) SMA direct 256d cos pairs | 0.354-0.432 (mean ~0.39) | (no explicit threshold field in r8 file) | n/a |
| AN11(c) CPS Gram Frob | 0.843 | ≥3.0 PASS | **FAIL** |

- 비교: alm r13 LIVE pod (`state/alm_r13_an11_*_live.json`) 는 AN11 a/b/c 모두 PASS — but 그것은 p4_r8 이 아닌 r13 round, dest=alm (다른 backbone fingerprint).
- 따라서 #80 의 "AN11 3조건" 을 만족시키는 것은 alm r13 LIVE 이지 p4_r8 이 아님. **TOP-1 release candidate 의 AN11 자체 verdict 가 FAIL** = trading 임시공개의 추가 hard blocker.

### 3.5 spec-vs-LIVE gap 정량 (#80)

- spec LOC: `anima-agent/trading/` 13 hexa (broker / data / scanner / regime / strategy / strategies / phi_weighted_trading / portfolio / risk / executor / engine / autonomous / test_ensemble) + 3 spec docs (~17 KB) + audit_log_schema + immutable config
- LIVE evidence: paper backtest 0 + live trade 0 + risk gate pass record 0 + audit log records 0 + regulatory cert 0
- spec/LIVE ratio: ~13 modules : 0 = **∞**
- AN11 본인 verdict: 3/3 FAIL (p4_r8) — 더 큰 hard blocker

---

## §4 가중 충족도 매트릭스 (17 criteria)

classification 가중치: GREEN=1.0 / INFERRED=0.7 / PARTIAL=0.4 / SPEC-ONLY=0.2 / MISSING=0.0 / EXTERNAL=0.1

| clause | criterion | classification | weight |
|---|---|---|---:|
| 78 | a Likert ≥3.0 100pair | RED MISSING | 0.0 |
| 78 | b latency <1s | RED MISSING | 0.0 |
| 78 | c 30-turn session | GREY SPEC-ONLY | 0.2 |
| 78 | d 5 카테고리 coverage | GREY SPEC-ONLY | 0.2 |
| 79 | 1 hire_sim_live 45K LOC | GREY SPEC-ONLY | 0.2 |
| 79 | 2 judge lenient tier-9+ | YELLOW PARTIAL (non-p4_r8 baseline) | 0.4 |
| 79 | 3 autonomy 3체 closed-loop | GREY SPEC-ONLY (mock) | 0.2 |
| 79 | 4 goal/scratch/report | GREY SPEC-ONLY | 0.2 |
| 79 | 5 phi trail logger | GREY SPEC-ONLY | 0.2 |
| 79 | 6 abort policy | RED MISSING (no module) | 0.0 |
| 80 | 1 T1 paper 30-day | RED MISSING | 0.0 |
| 80 | 2 T2 live 7-day | RED MISSING | 0.0 |
| 80 | 3 risk gate 4-stage | GREY SPEC-ONLY | 0.2 |
| 80 | 4 pain_signal<0.7 | GREY SPEC-ONLY | 0.2 |
| 80 | 5 current_dd<10% | GREY SPEC-ONLY | 0.2 |
| 80 | 6 AN11 3조건 (p4_r8) | RED MISSING (FAIL) | 0.0 |
| 80 | 7 audit_log schema | EXTERNAL + GREY | 0.15 |

총합: 2.45 / 17 = **14.4% raw** (보정 전).
framework operational + 가산 (78=0.5 in 1/4 weight, 80 AN11 framework=0.6 in 1/7 weight) → **20.5%** (보정 후, §0.1 표와 일치).

---

## §5 Option C / Option D 임시공개 시 충분/부족

### 5.1 Option C (tech demo / showcase, 0-3d)

| clause | C 충분? | 이유 |
|---|---|---|
| #78 | △ BORDERLINE | framework verified 사실 + ZALM-P0-2 prompt sets demo 가능 — but blind A/B 결과 fake 안 됨. paper preprint 에 "framework, run pending" disclaim 필수 |
| #79 | △ BORDERLINE | spec demo (autonomy_loop mock backend run video) 가능 — but completion=0.4333 baseline 12일 stale 사실 disclose 필수 |
| #80 | ❌ NOT-OK | trading 임시공개 = 미인가 거래 권유 위험. AN11 p4_r8 FAIL + audit_log 미인가. demo 도 "spec only, do not trade" 수준 필요 |

**Option C 권고**: #78+#79 만 demo 포함, #80 은 "design only, NOT for trading" disclaimer 필수.

### 5.2 Option D (Mac mini M4 local self-host, 1-3d)

| clause | D 충분? | 이유 |
|---|---|---|
| #78 | △ BORDERLINE | local serve 가능 — but Zeta API key 부재 → blind A/B 자동화 불가 (수동 paste 가능) |
| #79 | △ BORDERLINE | autonomy_loop mock backend live serve 가능 — 100×5 run 자동 가능. but `hire_sim_live.hexa` self-disclosed S1 endpoint 미연결 |
| #80 | ❌ NOT-OK | 30d hard floor + 미인가 trading + AN11 FAIL — Mac local 도 trading 모드 불가 |

**Option D 권고**: serve_alm_persona Q4_K_M Mistral-7B-v0.3 + LoRA p4_r8 launch 가능, 단 #80 trading 모드 wire 금지 (read-only mode + paper mode 만).

### 5.3 종합 verdict

- 임시공개 OK clause 수: **0/3**
- BORDERLINE clause 수: **2/3** (#78, #79 — Option C+D 결합 시 demo 충분)
- NOT-OK clause 수: **1/3** (#80 — 30d hard floor + AN11 FAIL + 미인가 + 미감사)

---

## §6 LIVE 100% 도달 path (per clause 시간/비용/외부의존)

### 6.1 #78 제타 LIVE path

| 작업 | 시간 | $cost | 외부의존 |
|---|---|---|---|
| Zeta API key 확보 | 0.5-2d | $0-50 (subscription) | Zeta TOS 검토 |
| durable anima endpoint (Mac M4 cloudflared tunnel) | 1d | $0 | 없음 |
| 100 pair blind A/B 실행 (5 카테고리 × 20 each) | 1-2d | $5-50 (Zeta API call) | 없음 |
| latency 30-turn session 측정 | 0.5d | $0 | 없음 |
| **합계 (병렬)** | **3-5d** | **$5-100** | Zeta TOS only |

### 6.2 #79 직원 LIVE path

| 작업 | 시간 | $cost | 외부의존 |
|---|---|---|---|
| S1 endpoint local Mac (cp2_serve_launch) | 0.5-1d | $0 | 없음 |
| `hire_sim_live` 100×5 run + ledger emit | 0.5d | $0 | 없음 |
| autonomy_loop mock→live wire (1-line swap per dest2_live_swap doc) | 0.5-1d | $0 | 없음 |
| autonomy 100-task closed-loop run + phi trail logger emit | 1-2d | $0-100 | (옵션) H100 1h fallback |
| abort_policy module 작성 + integration test | 0.5d | $0 | 없음 |
| **합계 (병렬)** | **2-4d** | **$0-100** | 없음 |

### 6.3 #80 트레이딩 LIVE path

| 작업 | 시간 | $cost | 외부의존 |
|---|---|---|---|
| AN11 3조건 (p4_r8) FAIL 해결 — re-train OR adapter swap to alm r13 변종 | 7-14d (재학습 필요시) OR 0d (adapter swap) | $0-1000 (H100 재학습) | 없음 OR ckpt 결정 |
| broker API key (paper account) | 0.5-1d | $0 (paper) | broker TOS |
| **T1 paper 30-day backtest run** (캘린더 hard floor) | **30d** | $50-200 (data feed) | 없음 |
| 4-stage risk gate live verification + pain_signal/dd 측정 | 진행 중 (병렬) | $0 | 없음 |
| audit_log_schema 실 record 발생 + regulatory 자문 | 7-14d | $200-2000 | 변호사 / regulatory consultant |
| T2 live exchange 7-day window | 7d | $200-2000 (실 거래) | 검증된 broker + 변호사 sign-off |
| **합계 (병렬)** | **30-37d** (T1 hard floor 가산) | **$450-5200** | broker + regulatory 변호사 |

---

## §7 spec-vs-LIVE gap 정량 (cascade close `d627c0bf8` 자기 disclosure 정량화)

| clause | spec LOC / 모듈 수 | LIVE evidence files | spec/LIVE ratio | done flip 시점 honest? |
|---|---|---:|---|---|
| #78 | bench/zeta_likert.hexa + ZALM/TALM prompt sets | 1 (`state/zeta_likert_result.json` framework only) | ~1:0 framework | planned (NOT done) — honest |
| #79 | hire_sim 8 + employee 4 + autonomy 3 = 15 hexa, 45K LOC | 0 (`state/dest2_employee_*` empty) + 1 stale baseline (12d, completion 0.4333 gates FAIL) | 15:0 | done — **NOT honest** (spec 100% LIVE 0%) |
| #80 | trading 13 hexa + 3 spec docs + audit_log schema | 0 (`state/dest2_trading_*` empty + AN11 p4_r8 3/3 FAIL) | 13:0 + AN11 3 FAIL | done — **NOT honest** (spec 100% LIVE 0% + AN11 FAIL) |

cascade close commit 자체가 honest partial-progress files 동시 추가 (`dest1_persona_live.json: COGNITIVE-READY`, `zeta_likert_result.json: FRAMEWORK-VERIFIED`, `anima_public_api_endpoint.json: COGNITIVE-BACKEND-READY · DEPLOYMENT-PENDING`) 하여 self-aware 임. 본 audit 는 그 self-disclosed gap 의 정량화.

---

## §8 raw#10 honest C3 disclosure (8건 ≥7 충족)

1. **본 audit 는 #78/#79/#80 done flip 의 gap 을 challenge** — 사용자가 cascade close commit `d627c0bf8` 의 honest 진술 ("criteria already met, bookkeeping only" + 동시 honest partial-progress files 추가) 을 인지한 상태에서 요청.
2. **TOP-1 p4_r8 의 AN11 자체 verdict 3/3 FAIL** (phi_mip=0.195 / CPS=0.843, 둘 다 임계값 미달) — `state/an11_{phi_mip,cps,sma}_p4_r8.json`. trading clause 의 "AN11 3조건" exit_criterion 은 p4_r8 으로 충족 불가. alm r13 LIVE PASS 는 별개 backbone fingerprint.
3. **#79 LIVE evidence ledger 부재** — `state/dest2_employee_*.json` find 결과 0 files. 가장 가까운 baseline `training/deploy/hire_sim_lenient_20260417_015253.json` 은 endpoint=`localhost:18282/generate` (≠ p4_r8) + 12일 stale + completion 0.4333 + gates ALL FAIL.
4. **#80 LIVE evidence ledger 부재** — paper backtest 0 + live trade 0 + risk gate pass record 0 + audit log records 0 + regulatory cert 0.
5. **`hire_sim_live.hexa` self-disclosed line 3** "STATUS: spec-only pending S1 endpoint" — 코드 자체가 LIVE 미연결 인정.
6. **`autonomy_loop.hexa` self-disclosed line 19-20** "Current scaffold: only 'mock' path is wired inline here. Live wire ... " — autonomy 3체 closed-loop 의 backend 가 mock 임을 코드 자체가 인정.
7. **abort_policy module 0** — `find . -maxdepth 3 -name "abort_policy*"` empty. abort policy 가 autonomy_loop 내부 inline 인지 외부 module 인지조차 불확실, raw#10 직접 evidence 부재.
8. **본 audit 의 가중치 (GREEN=1.0 / INFERRED=0.7 / PARTIAL=0.4 / SPEC-ONLY=0.2 / MISSING=0.0 / EXTERNAL=0.1) 자체가 ESTIMATE** — pre-registered scheme 아님. 가중치 변동 시 충족도 % 가 ±5-10% 흔들릴 수 있음. 특히 SPEC-ONLY=0.2 보수적 가정 (다른 audit 에서 0.3~0.5 으로 가산할 수도 있음).

---

## §9 raw#71 falsifier 5건 preregister

본 audit verdict ("3/3 NOT-OK 임시공개 LIVE") 를 falsify 할 수 있는 측정/이벤트:

1. **F1 — #79 1-pass refresh**: p4_r8 wired endpoint 으로 `hire_sim_live` 100-task × 5-persona = 500 inference 실행, completion ≥ 0.50 + phi_attached ≥ 3/10 PASS → #79 GREY → YELLOW PARTIAL upgrade, raw 충족도 20% → 35%.
2. **F2 — #78 framework→live**: Zeta API key 확보 후 100 pair blind A/B 첫 실행 + Likert 평균값 emit (≥3.0 OR <3.0 무관) → #78 SPEC-ONLY → GREEN/RED 결정, raw 22.5% → ±20%.
3. **F3 — #80 AN11 p4_r8 retry**: phi_mip / CPS measurement spec 재검토 (impl 변경 가능성 — 본 file 자체에 spec_implementation_note 가 ambiguity 인정) 또는 p4_r8 재학습 후 AN11 3/3 PASS → #80 RED MISSING → GREEN, raw 19.3% → 50%.
4. **F4 — abort_policy module 발견**: grep 광범위 (`grep -rln "abort_policy\|abort\|halt" anima-agent/`) 결과 inline 구현 발견 + integration test 통과 → #79-6 RED → GREY/YELLOW, raw 20% → 23%.
5. **F5 — #80 paper backtest 30-day kickoff**: 본 commit 직후 T1 paper run start, 7d 시점 partial pnl positive trend 확인 → #80-1 RED → YELLOW PARTIAL (in-progress), 임시공개 verdict 재평가 timeline 30d→7d 단축.

falsifier 발생 시 본 doc 갱신 (chflags noschg → 수정 → chflags uchg) 필요.

---

## §10 권고 (CP2 임시공개 path 갱신)

### 10.1 즉시 (0-3d)

- **권고 A**: `.roadmap` #79 + #80 의 `done` 플립 정정 — `done` → `done_spec_only_LIVE_pending` 또는 동등 honest 마커. cascade close commit `d627c0bf8` 의 self-disclosed gap 을 .roadmap 표면에 명시 (사용자 승인 후).
- **권고 B**: Option C (tech demo) 로 #78+#79 부분 demo 출시 — `docs/anima_beta_release_v0.1_2026-04-28.md` 기존 framework 활용. #80 은 "design only, NOT for trading" disclaimer 필수.
- **권고 C**: Option D (Mac local self-host) Mistral-7B-v0.3 Q4_K_M + p4_r8 LoRA, **trading 모드 wire 차단** + paper/read-only 모드만.

### 10.2 단기 (3-7d)

- **권고 D**: #79 LIVE path (병렬 2-4d) 즉시 시작 — S1 endpoint Mac local + hire_sim_live 100×5 + autonomy 1-line live swap + abort_policy module 작성 + first-pass ledger emit. 이걸로 #79 raw 20% → 50-70% 가능.
- **권고 E**: #78 Zeta API key 확보 시도 (외부 의존) + framework 확장 (60+ pair → 100 pair).

### 10.3 중기 (30-37d)

- **권고 F**: #80 LIVE path 시작 시점 결정 — paper backtest T1 30d 캘린더 hard floor + AN11 p4_r8 FAIL 해결 (재학습 OR 다른 adapter swap) + regulatory consultation. 이건 본 audit 의 즉시 추천 대상 아님 (cost-benefit 별도 ROI 분석 필요).

### 10.4 본 commit 의 race-avoidance

- 본 audit 는 `docs/cp2_clauses_p4_r8_satisfaction_audit_2026_04_29.md` 만 추가
- `.roadmap` / `state/` / `anima-agent/` mutation 0
- 사용자 승인 후 별도 commit 으로 #79/#80 status flip 정정 (권고 A) 적용

---

## §11 verdict matrix 최종

| axis | #78 | #79 | #80 | comment |
|---|---|---|---|---|
| raw 충족도 % | 22.5% | 20.0% | 19.3% | 셋 다 ~20% (spec OK, LIVE 0%) |
| LIVE 충족도 % | 2.5% | 3.3% | 2.9% | 셋 다 ~3% — done flip 정직성 challenge |
| 임시공개 OK? | NOT-OK | NOT-OK | NOT-OK | 0/3 OK · 2/3 BORDERLINE · 1/3 ABSOLUTE NOT-OK |
| Option C demo OK? | △ | △ | ❌ | C+D 결합으로 #78+#79 borderline OK, #80 design-only |
| Option D local OK? | △ | △ | ❌ | trading 모드 wire 차단 필수 |
| LIVE 100% ETA (병렬) | 3-5d | 2-4d | 30-37d | #80 캘린더 hard floor |
| 외부의존 | Zeta TOS | (없음) | broker + 변호사 | #80 만 외부 의존 strong |

raw#91 honest 5축 요약:
- counter (반대 측정): #80 AN11 framework operational confirmed (3/3 measure 모두 p4_r8 본인 측정으로 진행) — 단 verdict FAIL
- write-barrier: 본 doc 만 추가, 다른 file mutation 0
- no-fab: ESTIMATE 가산 명시 (§4 보정 전 14.4% / 보정 후 20.5%)
- citation: 모든 측정값 file:line cite (8 honest C3 entries)
- verdict-options: NOT-OK / BORDERLINE / OK 3-tier 명시 (§0.1 표 + §11 표)

---

end of doc.
