# EEG Arrival + D-day Post — anima-clm-eeg landing (2026-05-01)

> **created**: 2026-05-01 (post-helmet-session, post-first-empiricals, pre-multi-cohort)
> **canonical hardware doc**: `anima-eeg/docs/d_day_helmet_session_results_2026_04_28.md` (this is the cross-link layer)
> **canonical session inventory**: `anima-clm-eeg/docs/d_day_session_2026_04_28/INDEX.md`

---

## §1. Why this doc exists

Before 2026-04-28 the `anima-clm-eeg/README.md` 의 status 는 `Path A (Q1 prep, EEG D-1 lever-ready). Hardware not required for pre-register.` 로 표기되어 있었다. 그러나 다음 사실들이 발생:

- **2026-04-28**: EEG hardware (OpenBCI Cyton + Daisy + Ultracortex Mark IV 16ch) 도착 + helmet bring-up 완료 + impedance 16/16 GREEN
- **2026-04-28**: 60s baseline_resting / post_battery / daily_life recordings 수집, ICA 후 ~50 µV rms (정상 EEG range)
- **2026-04-28**: P1 LZ76 prior canonical Mac runs P1_FAIL, 이후 batch dispatch BLOCKED (Mac OOM + Hetzner 124 GB OOM)
- **2026-04-28**: MNE PSD ↔ anima Berger cross-validation AGREE
- **2026-04-29**: `electrode_adjustment_helper.hexa` 16ch concurrent touch detection upgrade landed (1310→1542 LoC, selftest dual-spike PASS)
- **2026-04-28~29**: anima-eeg/ 측 hardware tool 대량 landed (impedance_check, board_health_check, headplot_helper, full_helmet_health_view 등)
- **2026-04-28**: Mk.XII production deploy + EEG corroboration pilot N=1 honest fail (commit `6748462dc`)

이 문서는 anima-clm-eeg/ (R&D / falsifier / pre-register track) 관점에서 위 사실들을 cross-link 하고, pre-register criteria (P1/P2/P3) 에 어떤 영향이 있는지 정리한다. 거짓 PASS 주장 X — FALSIFIED 는 FALSIFIED 그대로, PENDING 은 PENDING 그대로.

---

## §2. 사실 timeline (commit-anchored)

```
2026-04-26  anima-clm-eeg/ 폴더 생성, pre-register v1 frozen
2026-04-27  pre-register v1.1 (operational tolerances) + Path A integrity verify
2026-04-28  ┌─ 09:?? Cyton+Daisy+Mark IV 도착, BOARD_NOT_READY_ERROR:7 → power cycle 복구
            ├─ 10:?? Cyton 4/8 ↔ 0/8 ↔ 7/8 변동, 7 wires 진단 → user full re-wiring → 16/16 alive
            ├─ 11:15 helmet 위치 + saline 적용 → impedance 16/16 GREEN (5-23 kΩ)
            │   evidence: state/impedance_real_hardware_audit/2026-04-28_20260428T111506Z.jsonl
            ├─ 12:01 daily_life ICA recording → LZ76 b=286‰ P1_FAIL (Mac canonical)
            ├─ 13:35 post_battery ICA recording → LZ76 b=350‰ P1_FAIL (Mac canonical)
            ├─ 21:21 commit 6748462dc — Mk.XII production deploy + EEG corroboration N=1 pilot
            │   verdict: CORROBORATION_FAIL by design (C1=1<5, C4=999, C5=0 — 3 deferred long-term gates)
            ├─ 22:59 commit f27d6363f — clm-eeg-p3 own 3 σ/τ=3 첫 D-day empirical
            │   real verdict: FALSIFIED_P3 (post_battery_ica grand=0.240, aiclean grand=0.009; target 3.0)
            └─ 23:59 D-day Tier-A #5 commit 2e69d896a — MNE PSD ↔ anima Berger AGREE
2026-04-29  ┌─ 00:?? commit 9a80237ae — eeg-core-phase6 _integrations/ 7 modules
            │   (clm_eeg_p1, clm_eeg_p3, berger, artifact_pipeline, rsn, cyborg_token, multi_subject)
            ├─ commit 98f438b5e — electrode_adjustment 16ch concurrent touch detection
            ├─ commit f73670a4a — electrode adjustment 16ch upgrade rationale + selftest evidence
            ├─ commit b1187d875 — eeg-core-phase6-gap _integrations/clm_eeg_p2.hexa (TLR Kuramoto)
            ├─ commit e0bbbfea7 — integration clm-eeg-p2 route Phase 6 gap LANDED
            └─ commit 5d7988201 — anima-clm-eeg-writers schema_version emit (5 ledgers)
2026-04-30  (production track migration continues via eeg-core dispatcher)
2026-05-01  this landing doc (cross-link layer for anima-clm-eeg/ R&D track)
```


---

## §3. Pre-register criteria 영향 (frozen v1 / v1.1 SHA-256 lock)


| pilot | gate | frozen threshold | 2026-05-01 status |
|---|---|---|---|
| **P1 V_phen_EEG-LZ × CLM-LZ** | LZ76(EEG) ≥ 0.65 AND \|Δ\|/human ≤ 20% | b≥650, Δ≤200‰, baseline 850‰ | PARTIAL — selftest VERIFIED, real .npy P1_FAIL on 2 ICA files (b=286‰, b=350‰); batch BLOCKED |
| **P2 TLR Tension-Link Resonance** | EEG α-band coherence ≥ 0.45 AND CLM V_sync r ≥ 0.38 | unchanged | PENDING — selftest only; real-data run not yet executed |
| **P3 GCG Granger Causality Gate** | EEG P3b → CLM layer 25-30 GC F-stat ≥ 4.0 AND unidirectional | unchanged | PENDING — separate from γ/θ proxy P3 below |
| **P3-proxy γ/θ paper σ/τ=3** | γ(30-50Hz)/θ(4-8Hz) PSD ratio target 3.0 | not in v1 frozen, paper-anchored | **REAL FALSIFIED_P3** (Apr 28, N=1 60s post-battery, both ICA + aiclean fall in F1 γ-absent regime) |

- Berger eyes-open daily_life 0/4 PASS → eyes-open false-positive 0 → falsifier 정상 작동
- pre-register criteria 자체는 손대지 않았으므로 silent-edit 위반 X

- N=1 single-subject single-day
- 60s short window per recording
- eyes-closed only (eyes-open daily-life 일부 진행)
- Cyton anti-alias filter 가 30-50Hz γ band attenuation 가능성
- 50Hz mains roll-off / amplifier scale issue 의심
- aiclean pipeline 이 γ band 를 ICA 대비 ~10x 더 suppress 함 (γ-absent regime 의 인공 강화 가능)

---

## §4. P1 (LZ76) status detail

**code path**: `tool/clm_eeg_lz76_real.hexa` (986 LoC, post-`50002d89` 568-line upgrade), `tool/clm_eeg_p1_lz_pre_register.hexa` (16497 bytes, 2026-04-29)

**selftest evidence (read-only audit)**:
- random mode: c(n)=39, b(n)_x1000=1218, ordering b(rand) > b(struct) HOLDS
- structured mode: c(n)=8, b(n)_x1000=250
- frozen criteria 650/200/850 byte-identical pre/post-50002d89 — silent-edit 없음

- `post_battery_ica` sha=a90b46fd…, b=350‰, **P1_FAIL**, 2026-04-28T13:35:17Z
- `daily_life_ica`   sha=3a636347…, b=286‰, **P1_FAIL**, 2026-04-28T12:01:51Z

**batch dispatch BLOCKED (commit `5693e8611`)**:
- Mac local: OOM/jetsam at n=119840 binarized stream
- Hetzner linux interp: OOM kill at anon-rss 129 GB / total-vm 230 GB
- AOT path: hexa_v2_linux transpile OK but gcc compile fail (hexa_str_trim implicit-decl, toolchain bug, out of scope)
- ubu1: no anima workspace

**Schartner reference 부정확 (commit `98d61133`)**:
- "0.85 ± 0.05 awake mean" — 어느 paper 에도 없음 (operational pre-commitment)
- C1 b≥0.65 임계 — paper-derived 아님 (operational tolerance)
- Kaspar-Schuster 1987 만 정확
- 추후: criteria 자체 의심 + Schartner 2017 niw022 또는 2015 PLOS ONE e0133532 SSOT 재확인 필요

---

## §5. P2 (TLR Kuramoto) status detail

**code path**: `tool/clm_eeg_p2_tlr_pre_register.hexa` (17620 bytes, 2026-04-29)

**status**: **PENDING REAL-DATA**
- selftest level 만 통과
- production track 측 `_integrations/clm_eeg_p2.hexa` (commit `b1187d875`) Phase 6 gap LANDED — TLR Kuramoto integration route 가능
- 실제 dual-stream (EEG α-PLV + CLM V_sync r) 동시 측정 미시행 — CLM substrate (`edu/cell/lagrangian/l_ix_integrator.hexa`) timing alignment 미확립

**diagnostic note**: Phase-1+2 5 candidates run (alpha_coh_atlas + 4 legacy) 결과 `anima_legacy_eeg_phase1_2_results_2026_04_28.md` 에서 ICA falsifier triggered (PLV destroyed) — α-PLV 자체가 ICA 후 attenuated. P2 real verify 전에 ICA pipeline 의 PLV-preserving 변형 필요 가능성.

---

## §6. P3 (GCG vs γ/θ proxy) status detail

**중요 구분**:
- pre-register **P3 GCG** (Granger Causality Gate, EEG P3b → CLM layer 25-30): 별도 test, **PENDING**
- paper P3 **γ/θ proxy** (own 3 σ/τ=3 = 12/4 = 3 phase acceleration scalar): commit `f27d6363f` 에서 first D-day empirical 시행됨


```
post_battery_eeg16_ica.npy      grand=0.240, occ=0.328, fro=0.211 → FALSIFIED_P3 (F1 γ-absent)
post_battery_eeg16_aiclean.npy  grand=0.009                       → FALSIFIED_P3 (F1 γ-absent)
target: 3.0 (ratio 3:1, σ/τ=3 paper anchor)
```

- synthetic_3      → grand=2.973  → VERIFIED_P3 (PASS path 살아있음)
- synthetic_5      → grand=4.954  → FALSIFIED_P3 (γ-inflated)
- synthetic_1      → grand=0.992  → FALSIFIED_P3 (F1 γ-absent)
- synthetic_random → grand=5.138  → FALSIFIED_P3 (white noise)

honest interpretation: paper P3 (own 3 σ/τ=3 = γ/θ band ratio) 가 이 subject/session 에서 NOT corroborated. PASS path 자체는 synthetic_3 으로 살아있으므로 falsifier 자체가 trivial reject 는 아님. 단 N=1 60s post-battery 로 단정 X — multi-cohort + amplifier filter audit 필요.

**P3 GCG**: 현재 selftest 만 통과 (`tool/clm_eeg_p3_gcg_pre_register.hexa` 19787 bytes, 2026-04-29). Granger F-stat ≥ 4.0 unidirectional EEG→CLM 측정 미시행.

---

## §7. Hardware-side cross-links (anima-eeg/ 측)

이 폴더는 hardware 를 직접 다루지 않지만 다음 cross-link 가 있다 (read-only consumption):

| concern | anima-eeg/ artifact | anima-clm-eeg/ usage |
|---|---|---|
| impedance ledger | `state/impedance_real_hardware_audit/2026-04-28_20260428T111506Z.jsonl` | data quality gate (16/16 GREEN required for downstream verify) |
| recording artifacts | `state/eeg_recordings/<ts>_*.npy` | P1/P2/P3 verifier input |
| board health | `anima-eeg/board_health_check.hexa` 결과 (verdict heuristic 미세조정 후보) | recording trust gate |
| electrode adjustment | `anima-eeg/electrode_adjustment_helper.hexa` (16ch concurrent, 1542 LoC) | pre-recording placement validation |
| headplot ascii | `anima-eeg/headplot_helper.hexa` | live electrode contact visualization |
| full helmet health | `anima-eeg/full_helmet_health_view.hexa` | aggregate hardware status panel |

방향성: `anima-clm-eeg/` → consumes → `anima-eeg/` → consumes → hardware. anima-eeg/ 가 anima-clm-eeg/ 를 import 하지 않음 (one-way; this folder 삭제해도 production untouched).

---

## §8. Production track (eeg-core dispatcher) migration cross-link

별도 background subagent track 으로 `anima-clm-eeg/tool/*.hexa` 의 일부가 `eeg-core/_integrations/*.hexa` 로 absorb-port 되는 중:

- `_integrations/clm_eeg_p1.hexa` (commit `9a80237ae`)
- `_integrations/clm_eeg_p2.hexa` (commit `b1187d875` + dispatch `e0bbbfea7`)
- `_integrations/clm_eeg_p3.hexa` (commit `9a80237ae`)
- `_integrations/synthetic_fixture.hexa` (commit `e35ac8579` + dispatch `908831cb3`)
- `_integrations/berger.hexa` / `artifact_pipeline.hexa` / `rsn.hexa` / `cyborg_token.hexa` / `multi_subject.hexa`
- writers schema_version emit: `clm-eeg-legacy.v1` (commit `5d7988201`)


상세 migration plan: `docs/anima-clm-eeg-migration` (commit `fb5b423c2`) 참조 — inventory + categorize + roadmap proposal.

---


본 landing 에서 명시적으로 제한해야 할 사실들:

1. **N=1 subject** — multi-cohort 부재. 본인 1명 × 1일.
2. **60s recording window** — 짧음. state transition 충분히 covered X.
3. **eyes-closed dominant** — eyes-open daily_life 일부만 있음. paradigm balance X.
4. **Cyton anti-alias filter γ attenuation 의심** — γ-absent regime 이 amplifier artifact 일 가능성.
5. **aiclean γ suppression 10x more than ICA** — pipeline-induced FALSIFIED 가능성.
6. **Schartner reference operational not paper-derived** — C1 b≥0.65 임계 자체 재확인 필요.
7. **Mac OOM + Hetzner OOM** — batch sweep impossible 현재 환경. AOT toolchain bug 의존.
8. **CLM substrate timing alignment 미확립** — P2 dual-stream verify 전 prerequisite.
9. **5-second smoke recording 만 있고 protocol-grade 본 녹음 미실시 case 다수** — 본 doc 에 listed 된 60s는 baseline_resting + post_battery + daily_life 한정. 그 외 paradigm (visual-P300, auditory-oddball, sleep-staging, longitudinal) 미시행.
10. **production deploy "EEG corroboration" 은 N=1 honest fail** (Mk.XII commit `6748462dc`) — 거짓 success 주장 금지.

이 limit register 는 거짓 PASS 차단 + 다음 사이클에서 어떤 변수를 close 해야 하는지 명시.

---

## §10. 다음 단계 (priority-ordered candidate)


### 즉시 (D+2~D+7)
- **Schartner reference 재anchoring** — paper-derived criteria 로 P1 v2 bump 검토 (`docs/clm_eeg_pre_register_v1_to_v1_1_changelog.md` 후속)
- **AOT toolchain bug fix** (hexa_str_trim implicit-decl) → batch LZ76 unblock
- **amplifier filter audit** — Cyton Daisy 30-50 Hz attenuation 측정 (sine sweep injection)
- **ICA pipeline PLV-preserving 변형** → P2 real verify enable

### 단기 (D+7~D+30)
- **multi-cohort N≥3 within-subject longitudinal** — 카페인/시간대/식사/운동
- **visual-P300 + auditory-oddball paradigm** — standard ERP cross-validation
- **CLM substrate timing emit** — `edu/cell/lagrangian/l_ix_integrator.hexa` 의 V_sync r 실시간 dump

### 장기 (D+30~D+180, sleep-tracking 포함)
- **Mk.XII multi-cohort N≥5** (commit `6748462dc` deferred long-term gates: C1 N≥5, C4 advers labels, C5 CLM substrate)
- **arxiv submission** — paradigm v11 7th PHENOMENAL axis registration prerequisite
- **closed-loop neurofeedback** — engagement/drowsiness signature

### 폐기 / 보류
- **P3 GCG real-data verify** — γ/θ proxy 가 FALSIFIED 인 상태에서 GCG 까지 가기 전 raw signal-quality 확립 우선
- **composite ≥2/3 PASS verdict** — 현재 1/3 PARTIAL + 1 FALSIFIED + 1 PENDING; 작위적 시도 X

---

## §11. Cross-reference index

### anima-clm-eeg/ 내부
- `README.md` — folder SSOT (이 landing doc 으로 status 갱신됨)
- `state/clm_eeg_pre_register_v1.json` / `v1_1.json` — frozen criteria
- `tool/clm_eeg_lz76_real.hexa` — P1 verifier (986 LoC)
- `tool/clm_eeg_gamma_theta_ratio.hexa` — γ/θ paper P3 verifier
- `tool/clm_eeg_p{1,2,3}_*_pre_register.hexa` — pre-register variant
- `tool/clm_eeg_synthetic_fixture.hexa` — dry-run 16ch synthesizer
- `docs/d_day_session_2026_04_28/INDEX.md` — 12-doc session inventory
- `docs/clm_eeg_d_day_chain_review_20260427_landing.md` — pre-arrival D-1 chain review
- `docs/eeg_d_day_user_setup_record_20260428_landing.md` — D-day user setup
- `docs/clm_eeg_pre_register_v1_to_v1_1_changelog.md` — operational tolerance changelog
- `docs/anima_eeg_anima_clm_eeg_cross_link_audit.md` — folder boundary policy

### anima-eeg/ (hardware track)
- `docs/d_day_helmet_session_results_2026_04_28.md` — impedance 16/16 GREEN
- `docs/electrode_adjustment_16ch_concurrent_2026_04_29.md` — 16ch concurrent upgrade
- `docs/full_helmet_health_view_design_2026_04_28.md` — aggregate panel design
- `docs/headplot_ascii_design_2026_04_28.md` — live ASCII headplot
- `docs/impedance_z_command_implementation_plan_2026_04_28.md` — z-command spec

### design/ (paradigm v11)
- `docs/paradigm_v11_stack_20260426.md` — 7th axis target
- `docs/omega_cycle_alm_free_paradigms_20260426.md` §4 PHENOMENAL axis
- `design/anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md` — CLM = Cell-Language Model 명확화
- `design/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md` — 새 EEG metrics

### CLM substrate (`edu/cell/`)
- (P2 real verify prerequisite — timing emit 필요)

### Mk.XII production (own 2 (b))
- commit `6748462dc` — N=1 honest fail pilot
- `design/mk_xii_production_deployment_eeg_corroboration_2026_04_28.md`
- `anima-clm-eeg/tool/mk_xii_eeg_corroboration.hexa` (~396 LoC)

### Memory pointers
- `~/.claude/projects/-Users-ghost-core-anima/memory/project_clm_eeg_pre_register.md`
- `~/.claude/projects/-Users-ghost-core-anima/memory/feedback_korean_response.md` (한글 응답 mandate)

---

## §12. raw 의무 + 본 landing 의 honesty triad

### raw 의무 적용

### 본 landing 의 honesty triad
- **claim**: EEG hardware ARRIVED + impedance VERIFIED + first D-day empiricals 시행됨, 그러나 P3 γ/θ proxy FALSIFIED + P1 batch BLOCKED + P2/P3 GCG PENDING; composite ≥2/3 PASS verdict 미달.
- **evidence**: commit hashes (`f27d6363f`, `06fe4142c`, `5693e8611`, `2e69d896a`, `6748462dc`, `98f438b5e`, `f73670a4a`, `9a80237ae`, `b1187d875`) + 직접 인용 가능한 ledger paths + selftest matrix (4-cell P3, 2-mode LZ76, 15-file Berger).
- **limit**: §9 의 10항목 — N=1, 60s, eyes-closed-dominant, amplifier filter 의심, aiclean γ-suppression artifact 가능, Schartner operational, OOM blocker, CLM timing 미확립, paradigm-coverage 부족, Mk.XII production deploy honest fail.

---

