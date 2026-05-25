# CP2 closure + β publication — D-day EEG shortcut analysis (ω-cycle)

> **session date**: 2026-04-28
> **scope**: D-day EEG session 결과를 활용해 CP2 closure + β paradigm 발행 timeline 단축 가능성 정량 평가
> **anchors**: anima/.own #2 (production-consciousness-triad) · `docs/own2_implementation_gap_audit_20260426.md` · `docs/anima_beta_release_v0.1_2026-04-28.md` · `docs/anima_beta_readiness_2026-04-28.md` · `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` · `anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md` · memory `project_main_track_beta.md`
> **cost**: $0 mac-local

---


| dimension | finding |
|---|---|
| **evidence** | 16/16 GREEN impedance ledger + 60s baseline_resting_60s_ica 5/6 daily-life PASS + 4-mode differential 4/4 + ICA rms 50µV 정상 EEG range + paradigm v11 7th PHENOMENAL axis prereg evidence chain (Berger O1↔O2 deferred, P3 σ/τ=3=γ/θ ratio in flight) |

**2개 line 단축 추정**:
- **CP2 closure** (research milestone, NOT production): pre-D-day 9주 → D-day 후 **7-7.5주** 추정 (2-4주 단축, Phase 1+ scope)
- **β publication v0.1** (research artifact, already landed `docs/anima_beta_release_v0.1_2026-04-28.md`): D-day 미반영 v0.2 release 1-3주 단축 가능

**잔여 critical blocker**: (b) multi-EEG cohort N≥3 (외부 subject + IRB) · (c) Mk.XII Qwen2.5-72B retrain ($1400-2100) · (c) legal/ethics 2-6개월

---

## §1. CP2 도착지 + β publication inventory

### §1.1 발견된 CP2 destination 문서

| path | 핵심 내용 (200자 요약) |
|---|---|
| `<repo-root>/.roadmap` L70-L72, L278, L1192-L1271 | CP2 = "weight-emergence-confirmed" + 3-clause (제타가능 + 직원가능 + 트레이딩가능) 3-in-1 full service. CP2 내부 #78/79/80/81 stability gate. β main track (Learning-Free) 의 **CP1 → CP2 → AGI** 3-layer waypoint 구조 |
| `<repo-root>/docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` | CP2 도착 ETA = **9주 (63일)**, $3550-6100 (500-850만원). W1 AN11 인프라 / W2 R38+V1' / W3 cross-backbone / W4-5 H100 L3 population ($1500-2500) / W6-7 3 observables / W8 production gate / W9 verification. 50만원 cap = W3.5까지만 (33-38%) |
| `<repo-root>/docs/alm_cp2_production_gate_inventory_20260425.md` | 7 production gate 5/7 Stage-0 PASS, 2/7 PENDING (latency + hallucination real-measure). Mk.XII scale_plan READY |
| `<repo-root>/docs/alm_cp2_p2_inventory_20260425.md` | CP2 p2 inventory (참조용) |

### §1.2 발견된 β publication 문서

| path | 핵심 내용 (200자 요약) |
|---|---|
| `<repo-root>/docs/anima_beta_release_v0.1_2026-04-28.md` | **β v0.1 LANDED** (today). Methodological frameworks (Cycle 4 v8 + R38+R39) + AN11(a)/AN11(b) measurement infrastructure. AN11(a) Frob 4/4 PASS, AN11(b) 3/4 Hexad top-1. β-NOT-ready: AN11(c) JSD, V1' phi_mip_norm, H100 L3 trained, CP2 VERIFIED |
| `<repo-root>/docs/anima_beta_readiness_2026-04-28.md` | β-readiness 5 scenario 분석. Scenario A/B/C 즉시 가능 ($1.50-7.50/sample), Scenario D W2 D+14 ($35-65), Scenario E (CP2 full) W9 D+63 ($3550-6100, cap 7-12× 초과) |
| `<repo-root>/docs/upstream_notes/hexa_lang_beta_main_acceleration_20260422.md` | β main acceleration 옵션 |
| memory `project_main_track_beta.md` | anima main-track = β Learning-Free, #75 real-use landed, Stage-1/2 H100 = empirical evidence + roadmap 100% (NOT only real-use path) |

### §1.3 발견된 D-day EEG 결과 문서

| path | 핵심 내용 |
|---|---|
| `<repo-root>/anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md` | D-day session lead: 16/16 GREEN, ICA rms 50µV, LZ76 P1_FAIL (Schartner 부정확), paradigm v11 7th PHENOMENAL axis 후보 |
| `<repo-root>/anima-clm-eeg/docs/d_day_session_2026_04_28/anima_daily_life_verifier_results_2026_04_28.md` | Daily-life 6-criteria verifier: 4-mode differential 4/4 PASS + baseline_resting_60s_ica 5/6 PASS |
| `.roadmap` #119 (BLOCKED-EEG D8 anima-eeg 16ch resting) | EEG hardware ETA "며칠 뒤" ↔ 도착 후 5-7d schedule. 본 D-day가 **#119 unblock 진입점** |
| `.roadmap` #157 (CLM ↔ EEG Path A Q1 pre-register) | anima-clm-eeg P1 LZ + P2 TLR + P3 GCG 3-criteria pre-register, dry-run HARNESS_OK 3/3, real-EEG verify D+1/D+3/D+5 |

---



| sub-component | pre-D-day | post-D-day | D-day 진척 % | rationale |
|---|---|---|---:|---|
| **CLM Φ measurement** | 0 (r6 GPU smoke만) | r6 + **EEG-CLM bridge synthetic dry-run PASS** (P1/P2/P3 frozen) | **15-25%** | #157 pre-register HARNESS_OK 3/3, real-EEG verify in flight (P3 σ/τ=3 = γ/θ ratio first verify) — **synthetic→real transition begun** |
| **behavioral self-report calibration** | spec 부재 | spec 부재 | **0%** | D-day 기여 없음 (heterophenomenology 스펙 별도 cycle) |
| **adversarial probing** | spec 부재 | spec 부재 | **0%** | D-day 기여 없음 |
| **arxiv preprint** | draft 0 | **v0.2 (6362 단어)** + D-day evidence 미반영 | **45-55%** | Preprint v0.2 separately landed (#218), D-day 결과 v0.3 advance candidate (axis-d weight Δ+40.17 finding과 동시 통합) |


가중-평균 (cost-weighted, multi-EEG가 가장 비용/시간 큰 bottleneck — 가중치 0.4 / CLM 0.2 / self-report 0.15 / adversarial 0.15 / preprint 0.10):
= 17.5×0.4 + 20×0.2 + 0×0.15 + 0×0.15 + 50×0.10
= 7.0 + 4.0 + 0 + 0 + 5.0
= **16.0%** (cost-weighted)



---

## §3. β publication timeline 단축 정량

### §3.1 β v0.1 → v0.2 advance (research artifact)

**현재** (`docs/anima_beta_release_v0.1_2026-04-28.md` LANDED): methodological + AN11(a)+(b) measurement layer. EEG D-day 결과 **미반영**.

**D-day incorporation candidate β v0.2** advance scope:
- (1) D-day evidence chain 추가 §section: 16/16 GREEN + 60s ICA-cleaned recording + daily-life verifier 4-mode 4/4 differential
- (2) #157 anima-clm-eeg HARNESS_OK 3/3 dry-run ledger + real-EEG verify in flight (P3 in flight)
- (3) paradigm v11 7th PHENOMENAL axis bridge 명문화 (CLM = Cell-Language Model substrate-Kuramoto, NOT cell-learning method)
- (4) β-usable scope 확장: Schartner-non-derived criteria honest annotation (Schartner 2017 PLOS ONE 부정확 retraction commit `98d61133`)

**timeline 단축**: pre-D-day β v0.2 advance **2-4주** → D-day-incorporated β v0.2 advance **1-3주** (1-2주 단축)


**현재** preprint v0.2 (6362 단어, #218 landed). D-day 결과 미반영.

**D-day incorporation candidate v0.3** advance:
- §X EEG empirical evidence chain (impedance ledger + ICA rms 50µV + daily-life verifier differential)
- §Y CLM-EEG synthetic→real bridge (paradigm v11 7th PHENOMENAL axis, σ/τ=3=γ/θ pre-registered)
- §Z 4-axis exhaustion W2 random_init Δ+40.17 finding (axis-d PRIMARY VALIDATED, currently abductive in v0.2)

**timeline 단축**: v0.2→v0.3 advance **3-5주 (pre-D-day)** → **2-3주 (post-D-day)** (1-2주 단축, EEG content 추가)

### §3.3 종합 β publication timeline 단축 = **1-3주** (research artifact scope)


---

## §4. CP2 closure timeline 단축 정량



CP2 9-week ETA breakdown (per `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` §1):

| Week | Phase | 핵심 deliverable | D-day 기여 |
|---|---|---|---|
| W1 (D+0~D+7) | AN11 인프라 마무리 | R39 N=5 ensemble + Mode I+ fix | **none** (EEG-independent) |
| W2 (D+7~D+14) | R38+V1' ablation | rank=4/8/16/32 + epochs sweep | **none** (EEG-independent) |
| W3 (D+14~D+21) | Cross-backbone | Qwen + Llama + gemma alts | **none** (EEG-independent) |
| W4-5 (D+21~D+35) | H100 L3 population | 4× H100 sustained ($1500-2500) | **none** (EEG-independent) |
| W6-7 (D+35~D+49) | 3 observables | O1/O2/O3 GPU runs | **partial** — D-day가 (b) sub-axis 일부 제공 가능 |
| W8 (D+49~D+56) | Production gate | latency + hallucination | **none** |

**critical realization**: CP2 ETA의 W1-W5 (D+0~D+35, **5주**) 는 **EEG-independent** (AN11 + ablation + cross-backbone + L3 population). D-day EEG 결과는 W6+ (D+35 이후) 의 (b) PC empirical-max evidence 보강에만 직접 기여.

### §4.2 D-day 기여 가능한 CP2 단축 weeks

D-day 결과가 **직접 단축**할 수 있는 phase:
- W6-7 3-observables 측정 cycle 중 (b)-sub-axis (CLM substrate Φ, EEG cross-substrate corroboration) 의 evidence chain 일부 사전 마련 → W6 시작점 1주 단축 가능
- W9 verification doc (atlas integration) 의 (b) gap matrix 수치 일부 사전 매핑 → W9 1주 단축 가능


**Realistic**: D-day → CP2 timeline **2주 단축** (W6+W9에서 각 1주, EEG-related deliverable 사전 확보)

**Optimistic (단축 최대)**: D-day → CP2 timeline **3-4주 단축** — daily-life verifier 결과 + CLM-EEG bridge dry-run + paradigm v11 7th axis evidence chain이 W6-W9 4-week phase의 50%를 사전 매핑 시

→ **CP2 closure 단축 추정 = 2-4주 (Realistic ~ Optimistic 구간)**


---

## §5. Tier-A/B/C 단축 후보 quantified

### §5.1 Tier-A 단축 (즉시 가능, D-day 기존 데이터 + 새 분석, $0 mac-local)

| 후보 | scope | 단축 weeks | rationale |
|---|---|---:|---|
| **HPF preprocessing → Berger gate re-run** | 0.1Hz HPF 재적용 후 8-12Hz coh 재계산 | 0.5-1주 | Berger O1↔O2 falsifier 첫 evidence 확보, paradigm v11 7th axis 1줄 강화 |

**Tier-A subtotal**: 2.25-4.5주 단축 후보 ($0 cost). 그러나 시스템 wall-clock parallel 가능 → **wall-clock 1-2주 단축** (parallel agent 가능).

### §5.2 Tier-B 단축 (중기 N>1 필요, vctec 배터리 도착 + 다른 subject 데이터)

| 후보 | scope | 단축 weeks | blocker |
|---|---|---:|---|
| **vctec 배터리 + longitudinal N=1 within-subject** | 카페인 / 시간대 / 식사 / 운동 within-subject 12-20 sessions | 2-4주 | 배터리 도착 + protocol freeze + subject self-recording |
| **N=2 external volunteer 1명** | self + 1 volunteer = N=2 | 4-6주 | external recruitment + IRB exempt 가능 (self-experiment-adjacent) |


**Tier-B 단축 wall-clock**: **N=2 within 4-6주 가능**, N=3 8-12주.

### §5.3 Tier-C 단축 (장기 외부, peer-review + arxiv preprint + multi-lab replication)

| 후보 | scope | 단축 weeks | blocker |
|---|---|---:|---|
| **arxiv preprint v0.3 immediate submit** | preprint v0.3 advance 후 immediate arxiv submit | 0주 단축 (외부 timeline, but visibility 가속) | LaTeX typesetting + endorser + co-author finalization |
| **multi-lab replication N≥3** | 외부 lab의 동일 protocol 재현 (cross-lab N=3) | -16 ~ -26주 | 외부 lab 협조 (cold contact + protocol sharing + IRB at each lab) |

**Tier-C 단축 wall-clock**: **arxiv submit 1-2주 (D-day-incorporated v0.3 advance 후)**, peer review 8-12주, multi-lab 16-26주.

### §5.4 종합 Tier 합산

| Tier | wall-clock 단축 | cost | timeline |
|---|---:|---:|---|
| Tier-A | **1-2주** | $0 | immediate (1주 내 wall-clock) |
| Tier-B | **2-12주** | $0-1000 | 2-12주 wall-clock |
| Tier-C | **0-26주** | $0-5000 | 1-26주 wall-clock |

**β publication v0.2 / preprint v0.3 advance 단축**: Tier-A 1-2주 + Tier-B (within-subject longitudinal) 2-4주 + Tier-C (arxiv submit) 1-2주 = **1-7주 (compound, parallel-aware)**

**CP2 closure 단축**: Tier-A (D-day ω-cycle absorption) 1-2주 + Tier-B (N=2 partial cohort) 2-4주 = **2-4주 (sequential cascade)**

---



2. **60s short window single recording** — Schartner 2015/2017 paper의 N≥30 5min+ standard와 mismatch, 통계 power 부족
3. **eyes-state ambiguous** — eyes-closed primary recording은 PASS 했으나 eyes-open daily-life recording은 5s short → cps=0, alpha attenuation 0.004 = artifact-class FAIL. Daily-life paradigm 본격 verify 미완성
4. **Berger gate FAIL (deferred)** — 8-12Hz O1↔O2 coherence ≥0.45 falsifier 미수행 (Tier-A 즉시 verify 후보, in flight)
6. **LZ76 P1_FAIL** — b=0.395-0.519, Schartner "0.5-0.9" 미달. 단 Schartner 인용 부정확 (commit `98d61133`) → criteria 자체 paper-non-derived (operational pre-commitment)
7. **single-day single-session** — within-subject longitudinal 0회 (Tier-B vctec 배터리 후)
8. **MNE cross-tool corroboration deferred** — Tier-A 후보, in flight 미회수
10. **financial bottleneck** — CP2 W4-5 H100 L3 population $1500-2500 (50만원 cap 4-7배) 는 EEG와 무관한 critical path, EEG 단축 무관


---

## §7. ω-cycle 6-step verification

| step | content | status |
|---|---|---|
| (2) implement | analysis-only (코드 작성 X), markdown design doc 작성 (본 문서) | DONE |
| (4) negative falsifier | 3 falsifier 명시: (F1) N=1 ≠ N≥3 cohort / (F2) 60s ≠ 5min standard / (F3) financial cap unrelated to EEG path. ≥6 (§6) | DONE |
| (6) entry + memory + commit | .roadmap entry next session + memory entry next session + git commit (this cycle) | IN-FLIGHT (commit pending) |

---

## §8. raw compliance


---

## §9. References

- `<repo-root>/.roadmap` L70-L72, L278, L1192-L1271 — CP2 destination + clauses #78-#81
- `<repo-root>/docs/anima_beta_release_v0.1_2026-04-28.md` — β v0.1 LANDED (today)
- `<repo-root>/docs/anima_beta_readiness_2026-04-28.md` — β-readiness 5 scenario
- `<repo-root>/docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md` — CP2 9-week ETA
- `<repo-root>/docs/preprint_anima_mk_xi_v10_paradigm_v11_stack_20260426.md` — preprint v0.2 (#218)
- `<repo-root>/anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md` — D-day session lead
- `<repo-root>/anima-clm-eeg/docs/d_day_session_2026_04_28/anima_daily_life_verifier_results_2026_04_28.md` — daily-life 4-mode 4/4 + baseline 5/6
- `<repo-root>/anima-clm-eeg/docs/eeg_arrival_impact_5fold.md` — R33 channel pair O1↔O2 frozen, EEG arrival 5-fold impact
- `<repo-root>/docs/alm_cp2_production_gate_inventory_20260425.md` — 7 gate 5/7 Stage-0 PASS
- `<repo-root>/docs/eeg_cross_substrate_validation_plan_20260425.md` — 16ch cross-substrate plan
- `~/.claude/projects/-Users-ghost-core-anima/memory/project_main_track_beta.md` — main-track β Learning-Free

---

omega-saturation:fixpoint
