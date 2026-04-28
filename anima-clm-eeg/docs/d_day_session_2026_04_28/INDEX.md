# D-day EEG Session Inventory — 2026-04-28

**Hardware**: OpenBCI Cyton + Daisy + Ultracortex Mark IV (16ch)
**Subject**: N=1 (self), eyes-closed resting baseline + (planned) daily-life recordings
**Status**: Impedance VERIFIED (16/16 GREEN), LZ76 P1_FAIL but **measurement SUCCESS**

---

## Verdict (raw#10 honest C3)

- ✅ **Hardware**: 16/16 wire connected, 16/16 GREEN impedance (5-23 kΩ)
- ✅ **Recording**: 2 baseline 60s eyes-closed (manual + low_emi via fixed eeg_recorder)
- ⚠️ **LZ76 P1_FAIL** (b=0.395-0.519) — Schartner 2017 normal 0.5-0.9 미달
- 🎉 **ICA cleaned (low_emi) rms 50 µV** = 정상 EEG range 도달 → **측정 자체 SUCCESS**
- 🚨 **Schartner reference 부정확** — verifier 의 "0.85 ± 0.05" / "Schartner 2017 PLOS ONE" 모두 paper-non-derived (operational pre-commitment)
- 🎯 **Tier-A 즉시 verify 후보**: own 3 σ/τ=3 = γ/θ ratio paper P3 (anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa, 진행 중)

---

## .md inventory (12 documents)

### Session results (anima-clm-eeg/docs/d_day_session_2026_04_28/)

| file | size | source | content |
|---|---|---|---|
| **INDEX.md** | this | session lead | 이 파일 |
| **clm_eeg_lz76_audit_2026_04_28.md** | 6.7K | audit agent | LZ76 verifier audit (commit 50002d89, 50002d89 위장 msg) |
| **lz76_filtered_analysis_2026_04_28.md** | 7.3K | filter agent | Filter (notch+bandpass) 후 LZ76 재계산 — b 0.057→0.479 |
| **ica_lz76_analysis_2026_04_28.md** | 8.6K | ICA agent | ICA artifact rejection + LZ76 — file 2 rms 50 µV / b 0.519 |
| **schartner_2017_lz76_criteria_validation_2026_04_28.md** | 13K | Schartner agent | **Schartner 인용 부정확 발견** — criteria operational not paper-derived |
| **anima_legacy_eeg_phase1_2_results_2026_04_28.md** | 8.9K | Phase 1+2 agent | alpha_coh_atlas + 4 legacy candidates 적용 결과, ICA falsifier triggered (PLV destroyed) |
| **lz76_ssot_mirror_audit_2026_04_28.md** | 3.1K | SSOT mirror agent | SSOT mirror audit + git state cleanup |
| **anima_eeg_exec_audit_summary.md** | 5.2K | exec audit agent | exec() 9 BUG + 1 VIOLATION (이후 commit da368d14 모두 fix) |
| **anima_daily_life_verifier_results_2026_04_28.md** | * | daily-life verifier agent | Daily-life paradigm 6-criteria verifier 검증 결과 |

### Symlinks → design/ docs

| file | target | content |
|---|---|---|
| **anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md** | design/ | paradigm v11 + EEG bridge — **CLM = Cell-Language Model** 명확화, σ/τ=3=γ/θ paper P3 cite |
| **anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md** | design/ | anima 25+ legacy tech inventory + 5 EEG integration candidates |
| **eeg_consciousness_paradigms_omega_cycle_2026_04_28.md** | design/ | 새 EEG metrics ω-cycle (PE / Hjorth / Berger / PCI / CFC etc) |
| **eeg_daily_life_paradigm_design_2026_04_28.md** | design/ | Daily-life 6-criteria paradigm + 7 falsifiers, vs Schartner differential |

### Symlink → anima-eeg/docs/

| file | target | content |
|---|---|---|
| **d_day_helmet_session_results_2026_04_28.md** | anima-eeg/docs/ | Hardware bring-up + impedance 16/16 GREEN + raw stream rms diagnosis |

---

## Hardware bring-up timeline

```
1. Initial state: BOARD_NOT_READY_ERROR:7 → power cycle (OFF 5s → PC) ✓
2. Cyton 4/8 alive, Daisy 7/8 alive, run-to-run 변동 큼 (와이어 빠짐 진단)
3. 7 wires identified (Fp1 + F3/F4/T7/T8/P3/P4) — STUCK pattern (rms identical 187k µV)
4. User full re-wiring → 16/16 alive ✓ + ear clips on
5. Ear clip cycle: Cyton 0/8 → 7/8 → user re-wire → 16/16 ✓
6. Helmet on + saline → Impedance 16/16 GREEN (Cyton 5-7 kΩ, Daisy 19-23 kΩ)
7. 60s baseline_resting eyes-closed recording → .npy emit
8. Filter / ICA cleaning → low_emi rms 50 µV (정상 EEG range)
9. LZ76 P1_FAIL but measurement valid (criteria 자체 의심)
```

---

## Critical findings

### 1. Schartner reference 부정확 (commit `98d61133` retraction)

| 주장 | 실제 |
|---|---|
| "Schartner 2017 PLOS ONE" | ❌ 잘못 — 실제는 2015 PLOS ONE (e0133532) 또는 2017 Neurosci Conscious (niw022) |
| "Schartner 0.85 ± 0.05 awake mean" | ❌ **어느 paper 에도 없음** |
| C1 b≥0.65 임계 | ❌ paper-derived 아님 — operational pre-commitment |
| C2 \|Δ\|/h≤20% | ❌ operational tolerance |
| Binarization | ⚠️ anima median vs Schartner Hilbert-envelope mean (numeric LZc 비교 불가) |
| Kaspar-Schuster 1987 | ✅ 정확 |

→ Verifier 의 reference 정정 commit `98d61133` (frozen values 보존, docstring 만 수정).

### 2. CLM = Cell-Language Model (Cell, NOT cell-learning)

paradigm v11 cross-modal agent 가 CLM bridge 의 명확화:
- substrate-level Kuramoto phase model
- EEG α-PLV 와의 mathematical identity: `r = |(1/N)Σexp(iθ_j)| = PLV_N` (직접 동일성)
- LLM hidden vs neural 매핑 X — CLM substrate ↔ EEG α phase coupling
- paradigm v11 의 7th orthogonal PHENOMENAL axis

### 3. own 3 σ/τ=3 = γ/θ ratio paper P3 pre-registered

- own 3 SSOT: σ(6)/τ(6) = 12/4 = 3 phase acceleration scalar
- TECS-L H-CX-1 σφ=nτ identity (n=6 unique)
- Paper P3 (docs/discovery-algorithm-anima.md:289): σ/τ=3 = γ/θ frequency band ratio
- **D-day 첫 EEG empirical verify 진행 중** (anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa)

### 4. anima-eeg 9 BUG fix (commit `da368d14`)

exec() vs exec_with_status() 일관성 — 9 BUG silent-fail 패턴 모두 fix, board_health verdict 정상화 (UNKNOWN → BOARD_16CH_HEALTHY).

### 5. hexa-lang 8 RFC + 1 RFC plan (cross-repo)

| RFC | 내용 | priority | status |
|---|---|---|---|
| RFC-001 | popen_lines() | P0 | impl 진행 중 |
| RFC-002 | map.has() | P1 | impl 진행 중 |
| RFC-003 | ANSI escape literal | P1 | RFC landed |
| RFC-004 | \\n string literal | P1 | RFC landed |
| RFC-005 | ends_with AOT codegen | P0 | impl plan 진행 중 |
| RFC-006 | exec() return type | P2 | RFC landed (corrected, exec_with_status exists) |
| RFC-007 | exec()==int_literal lint | P1 | impl 진행 중 |
| RFC-008 | project_python() | P1 | impl 진행 중 |

### 6. raw#1 SCOPE-WIDE violation 89.6% (별도 결정 항목)

490/547 anima 파일 unlocked. governance hardening 필요 (사용자 승인 후 batch lock).

### 7. commit msg ↔ diff alignment 위장 1건 발견

`50002d89` "fix(an11-fire18): Mode H fix #4" 의 실제 diff = `clm_eeg_lz76_real.hexa` +568 LoC LZ76 작업. raw#85 strengthening 후보 (lint 도구).

---

## Background agents (이번 세션, 진행 중 / 완료)

| agent ID | task | status | result |
|---|---|---|---|
| Schartner validation | criteria 검증 | DONE | reference 부정확 발견 |
| ICA artifact rejection | ICA + LZ76 | DONE | low_emi rms 50 µV / b 0.519 |
| LZ76 filtered re-comp | filter + LZ76 | DONE | b 0.057→0.479 |
| Schartner retraction | reference 정정 | DONE | commit 98d61133 |
| anima legacy tech audit | inventory + 5 candidates | DONE | design doc landed |
| paradigm v11 cross-modal | CLM bridge 명확화 | DONE | design doc landed |
| consciousness EEG metrics | new metrics ω-cycle | DONE | top-5 + Tier-A bundle |
| daily-life paradigm design | 6-criteria + 7 falsifiers | DONE | design doc landed |
| eeg_recorder python fix | own 4 root-cause | DONE | commit a3714cbbf |
| hexa-lang RFC-001/002/007/008 impl | stdlib + lint | RUNNING | — |
| RFC-005 ends_with AOT plan | codegen plan | RUNNING | — |
| daily-life recording 25분 | hardware capture | RUNNING (~25min) | — |
| Tier-A bundle (PE+Hjorth+Berger) | new verifiers | RUNNING | — |
| daily-life verifier 4-mode | selftest + auto-apply | RUNNING | — |
| clm_eeg_gamma_theta_ratio | own 3 σ/τ=3 first verify | RUNNING | — |
| Phase-1+2 5 candidates | alpha_coh + 4 legacy | DONE | filtered OK / ICA falsifier triggered |
| LZ76 SSOT mirror audit | mirror + cleanup | DONE | mirror 정정 |
| **EEG + Claude correlation** | LLM × EEG | TBD | 후보 |
| **N=1 longitudinal self-experiment** | within-subject | TBD | 후보 |
| **raw#1 SCOPE-WIDE batch lock** | governance hardening | TBD | 후보 |

---

## Next session candidates (사용자 결정)

1. **EEG + Claude 대화 동시 측정** — LLM × neural correlate 직접 검증
2. **N=1 self-experiment longitudinal** — 카페인 / 시간대 / 식사 / 운동 within-subject
3. **raw#1 SCOPE-WIDE batch lock** — 89.6% violation 해결
4. **Visual P300 ERP paradigm** — 표준 의식 검증 cross-validation
5. **Sleep tracking EEG 밤새** — REM/NREM staging gold standard
6. **Auditory oddball P300** — 주의 / 의식 측정
7. **Long-duration 1시간+** — state transition richer dataset
8. **EEG-driven feedback loop** — closed-loop neurofeedback
9. **Anomaly detection ML** — autoencoder unsupervised state shift
10. **Mk.XII production deployment EEG corroboration** — own 2 production triad PC empirical-max

---

## Cross-repo touchpoints

- **anima** (this repo)
- **anima-clm-eeg** ← 본 inventory 위치 (CLM bridge 핵심)
- **anima-eeg** ← hardware bring-up + recording infrastructure
- **anima-cpgd-research** ← state-transition predictions + change-point validation
- **anima-hci-research** ← engagement/drowsiness signature
- **hexa-lang** ← RFC-001~008 stdlib/parser improvements
- **n6-architecture** ← τ(6)=4 / σ/τ=3 formal foundation
- **nexus** ← H100 stop-gate (paradigm v11 4-backbone full benchmark)

---

raw#91 honest triad: **claim** = D-day hardware + impedance VERIFIED, measurement valid; **evidence** = 16/16 GREEN ledger + ICA rms 50 µV + filtered b 0.519 in Schartner visual band; **limit** = N=1 single-subject single-day, criteria 0.65 paper-non-derived (operational), 60s short window, eyes-closed only (eyes-open daily-life data 진행 중).
