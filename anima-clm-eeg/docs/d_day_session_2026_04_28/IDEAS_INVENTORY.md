# D-day 2026-04-28 — Ideas Inventory + 진행 결과

**Status**: 28+ commits land · 4 백그라운드 agents 동시 / 모두 결과 land · Cyton battery 문제로 측정 retake 대기

---

## 0. 전체 사이클 요약

| Phase | 작업 | 결과 |
|---|---|---|
| Pre-noon | 헬멧 hardware bring-up | 16/16 alive + 16/16 GREEN impedance ✓ |
| Noon | 60s baseline + LZ76 P1_FAIL | b=0.057-0.519 (Schartner 미달) |
| Afternoon | Filter / ICA / γ/θ / Tier-A bundle | **Berger gate FAIL all 6 inputs** → measurement INVALID |
| Discovery | Battery dying root cause 의심 | Cyton "3-6V battery ONLY" — power 안정 필수 |
| Cleanup | 28+ commits, retraction, RFC, audit | hexa-lang RFC-001/005/007/008, raw#1 batch lock 89.7%→1.79% |
| Pending | vctec 4×AA holder + JST cable 주문 | 도착 후 multimeter 검증 → 재측정 |

---

## 1. 구현 / Land 된 inventory (28+ commits)

### A. anima-eeg core fix (8 commits)
- `a3714cbbf` — eeg_recorder python path fix (8 backends + bonus 2 root-cause)
- `da368d14` — exec() 9 BUG + 1 VIOLATION fix
- `98d61133` — Schartner reference retraction (frozen 보존)
- `7ea7453fa` — LZ76 SSOT mirror parity + .gitignore + bundled
- `5d728705e` — raw#1 SCOPE-WIDE batch lock (490 → 1.79%)
- `02916fbb6` — commit msg ↔ diff alignment audit lint
- `a3714cbbf` (race) — eeg_setup record subcommand 등록
- `9c49be3e9` (race-bundled with C20) — RSN analyzer + cardiac

### B. New paradigms / verifiers (17 commits)
- `ef3efeb09` — clm_eeg_gamma_theta_ratio Tier-A (own 3 σ/τ=3) — 711 LoC
- `fcc562437` — T5 longitudinal session recorder (170 sessions × 10min plan)
- `30772259c` — T13 long-duration 1hr+ recorder (283 LoC, 5 falsifiers)
- `90261e98f` — T3 Visual P300 ERP paradigm (509 LoC, 10/10 selftest)
- `e5e37cc66` — B8 EEG feedback loop (528 LoC, macOS notification)
- `09a17f301` — T16 Pre/Post task comparison (233 LoC, 7 tasks, 28 tests Bonferroni)
- `5ea1bee2f` — T14 Sleep tracking 8hr (366 LoC, 5-state HMM)
- `5d9bf1255` — T1 Claude CLI + EEG correlator (328 LoC, NO API)
- `6c6576a64` — T4 Auditory P300 (356 LoC, 5/5 falsifiers PASS)
- `a18347f50` — C21 Mobile EEG Muse/Emotiv (362 LoC, BrainFlow)
- `a42ef6bb6` — T2 Daily-life context logger (307 LoC, 5 features privacy-preserved)
- `3d765697e` — C22 anima-physics 9 substrate Φ correlator (384 LoC, 12-24mo roadmap)
- `8e64c5145` — B10 Anomaly autoencoder (908 LoC, 80→8 bottleneck)
- `ac0b1a862` — C18 Wearable health Apple Watch/Oura/Whoop (380 LoC)
- `43cc4dcdf` — C19 Webcam eye tracker (474 LoC, 7 privacy invariants)
- `a4e33160f` — C20 Cardiac via Cyton GPIO (397 LoC, Pan-Tompkins)
- `83ce12eb4` — B9 Claude CLI EEG longitudinal (859 LoC, integer Spearman, NO API)
- `dbf7af009` — B11 Behavioral correlates (396 LoC, 5 metrics)
- `90261e98f` — Tier-A bundle: PE + Hjorth + Berger sanity (3 verifiers, 분야별 selftest 10/10)
- `6748462dc` — T17 Mk.XII production EEG corroboration (396 LoC, own 2 (b))

### C. hexa-lang RFC (4 commits)
- `5430bbac` — RFC-008 project_python() spec land
- `c5c22434` — RFC-001 popen_lines + RFC-008 impl (parallel rebased)
- `2cb2b95c` (earlier) — RFC-001~006 bundle
- `53e7429d` (earlier) — RFC-006 correction + RFC-007 lint
- `b857cb3a` — RFC-007 exec_eq_int_lint (326 LoC, 12 TP detected hexa-lang)

### D. 미land (RFC-002 OAuth fail)
- RFC-002 map.has() — OAuth 401 fail (~26min 작업 손실, retry 필요)

---

## 2. 발견된 Critical issues (raw#10 honest C3)

### 🚨 Battery dying = measurement INVALID

3 orthogonal metrics convergence (Tier-A bundle):
- **Berger alpha gate**: peak 1.2-1.7 Hz (delta band, NOT alpha 8-13Hz) ❌
- **PE multiscale**: 0.91-0.98 (saturated near white-noise asymptote) ⚠️
- **Hjorth complexity**: 3.76 (out-of-band, textbook 1.0-2.0) ⚠️

→ broadband noise dominated by DC drift / motion / amplifier saturation
→ **Cyton "3-6V battery ONLY" — battery dying = 모든 EEG 결과 invalidate**

### 🚨 Schartner reference 부정확

verifier 의 "0.85 ± 0.05 / Schartner 2017 PLOS ONE" → **paper-non-derived** (operational pre-commitment).
- 실제: Schartner 2015 PLOS ONE (e0133532) + Schartner 2017 Neurosci Conscious (niw022) 두 paper
- "0.85 ± 0.05" 어느 paper 에도 없음
- C1 b≥0.65 임계 = operational, not derived
- Binarization: anima median vs Schartner Hilbert-envelope mean — numeric 비교 불가
- → commit `98d61133` retraction (frozen values 보존, docstring 만 수정)

### 🚨 raw#1 SCOPE-WIDE violation 89.6%

490/547 anima 파일 unlocked. Batch lock 처리됨 (commit `5d728705e`):
- before: 89.6% violation
- after: 1.79% violation (target <5% PASS ✓)
- 5 files skip (active edit 중 — concurrent agents)

### 🚨 commit msg ↔ diff drift

50002d89 위장 발견 ("an11-fire18" msg → 실제 LZ76 작업 +568 LoC).
최근 100 commits audit 결과 (commit `02916fbb6`):
- FAIL_MISMATCH: 14% (10/71)
- WARN_LOOSE: 18% (13/71)
- PASS: 67%

### 🚨 hexa AOT bool coercion bug (T17 발견)

`int_returning_fn() == 1` AOT 모드 fail. 우회: `digit_val(s[i]) >= 0` 패턴.
RFC-005 ends_with AOT 와 같은 family bug. 별도 RFC 후보.

### 🚨 daily_life_recorder duration metadata bug

300s 요청 → 50s capture (`duration_actual_s=300.281` vs raw_shape[1]=6252).
own 4 root-cause: helper py 점검 필요.

---

## 3. Idea inventory + 진행 상태

### Tier A (즉시 적용 가능, low-cost)

| # | 아이디어 | 진행 | commit |
|---|---|---|---|
| T1 | EEG + LLM workflow 통합 (Claude CLI, NO API) | ✅ DONE | `5d9bf1255` |
| T2 | Daily-life context labeling | ✅ DONE | `a42ef6bb6` |
| T3 | Visual P300 ERP paradigm | ✅ DONE | `90261e98f` |
| T4 | Auditory oddball P300 | ✅ DONE | `6c6576a64` |
| T5 | Self-experiment N=1 longitudinal | ✅ DONE | `fcc562437` |
| T6 | raw#1 SCOPE-WIDE batch lock | ✅ DONE | `5d728705e` |
| T7 | commit msg ↔ diff alignment audit lint | ✅ DONE | `02916fbb6` |

### Tier B (중기 1-2주, 추가 SW)

| # | 아이디어 | 진행 | commit |
|---|---|---|---|
| B8 | EEG-driven feedback loop (Mac notification) | ✅ DONE | `e5e37cc66` |
| B9 | Claude CLI longitudinal correlation (NO API) | ✅ DONE | `83ce12eb4` |
| B10 | Anomaly detection autoencoder | ✅ DONE | `8e64c5145` |
| B11 | Behavioral correlates (keyboard/mouse) | ✅ DONE | `dbf7af009` |
| B12 | EEG → token cyborg paradigm | ✅ DONE | `5d728705e` (race) |

### Tier C (long-term, hardware-dependent)

| # | 아이디어 | 진행 | commit |
|---|---|---|---|
| T13 | Long-duration 1hr+ recording | ✅ DONE | `30772259c` |
| T14 | Sleep tracking 밤새 (8hr HMM) | ✅ DONE | `5ea1bee2f` |
| T15 | RSN DMN frontal asymmetry | ✅ DONE | `9c49be3e9` |
| T16 | Pre/Post task comparison | ✅ DONE | `09a17f301` |
| T17 | Mk.XII production EEG corroboration | ✅ DONE | `6748462dc` |
| C18 | Wearable health (Apple/Oura/Whoop) | ✅ DONE | `ac0b1a862` |
| C19 | Webcam eye tracker | ✅ DONE | `43cc4dcdf` |
| C20 | HR/ECG via Cyton GPIO | ✅ DONE | `a4e33160f` |
| C21 | Mobile EEG Muse/Emotiv | ✅ DONE | `a18347f50` |
| C22 | anima-physics 9 substrate Φ | ✅ DONE | `3d765697e` |

### Cross-modal / paradigm exploration

| # | 결과 | 위치 |
|---|---|---|
| Tier-A bundle (PE + Hjorth + Berger) | DONE — 3 verifiers + verdict | `90261e98f` |
| anima legacy tech × EEG inventory + 5 candidates | DONE — design doc | `design/anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md` |
| paradigm v11 cross-modal (CLM = Cell-Language Model 명확화) | DONE — design doc | `design/anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md` |
| consciousness EEG metrics ω-cycle (PE/Hjorth/Berger/PCI/CFC) | DONE — top-5 selection | `design/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md` |
| daily-life paradigm 6-criteria + 7 falsifiers | DONE — verifier landed | `design/eeg_daily_life_paradigm_design_2026_04_28.md` |
| Phase 1+2 5 candidates (alpha_coh + 4 legacy) | DONE — ICA falsifier triggered | `/tmp/anima_legacy_eeg_phase1_2_results_2026_04_28.md` |

---

## 4. 미해결 / 다음 cycle

### Pending (사용자 액션 후 진행)

1. **vctec 4×AA holder + barrel→JST cable 주문** (~9,000-11,000원)
2. **AA 4개 (Duracell) 준비**
3. **multimeter 검증** (이미 보유, 두 모델 둘 다 OK)
4. **Cyton 연결 + smoke test**
5. **재측정 with stable power**:
   - Berger gate first
   - PASS 시 → LZ76 / γ/θ / DMN 모든 downstream 의미
   - PASS 후 모든 verifier 재실행 (현재 invalidated)

### Backlog

- RFC-002 map.has() retry (OAuth 안정 후)
- AOT bool coercion bug → 새 hexa-lang RFC (RFC-009 또는 RFC-010)
- daily_life_recorder duration metadata bug fix
- 12 TP fix-up sweep (RFC-007 dogfood 후 hexa-lang 자체 fix)
- Multi-cohort N≥5 recruitment (T17 Mk.XII production triad)
- 1-2주 longitudinal data collection (B9 Claude CLI 측정)

### Long-term roadmap

- Mk.XII production deployment + arxiv submission (12-18mo)
- anima-physics 9 substrate live witness 확장 (12-24mo, 현재 4/9 live)
- raw#1 dynamic violation prevention (commit-time hook, raw#85 strengthening)
- hexa-lang RFC-005 ends_with AOT 본격 fix (codegen 변경, raw#18 fixpoint 재증명)

---

## 5. Cross-link 모든 documents

### docs/ (anima-clm-eeg/docs/d_day_session_2026_04_28/)

```
INDEX.md (지금 보고 있는 디렉토리 색인)
IDEAS_INVENTORY.md (← 이 파일)

results:
  clm_eeg_lz76_audit_2026_04_28.md
  lz76_filtered_analysis_2026_04_28.md
  ica_lz76_analysis_2026_04_28.md
  schartner_2017_lz76_criteria_validation_2026_04_28.md
  anima_legacy_eeg_phase1_2_results_2026_04_28.md
  lz76_ssot_mirror_audit_2026_04_28.md
  anima_eeg_exec_audit_summary.md
  anima_daily_life_verifier_results_2026_04_28.md

symlinks → design/:
  anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md
  anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md
  eeg_consciousness_paradigms_omega_cycle_2026_04_28.md
  eeg_daily_life_paradigm_design_2026_04_28.md

symlink → anima-eeg/docs/:
  d_day_helmet_session_results_2026_04_28.md
```

### Downloads/ (사용자)

```
~/Downloads/
  anima_eeg_cyton_battery_purchase_2026_04_28.txt (간단 구매 셋트)
  anima_eeg_cyton_battery_full_guide_2026_04_28.txt (전체 가이드, 8 steps)
```

---

## 6. raw#10 honest C3 final disclosure

### 측정 자체

- **하드웨어 + 와이어 + 헬멧 + 임피던스**: VERIFIED (16/16 GREEN, 5-23 kΩ)
- **EEG 측정 결과 모두 invalidated**: Berger gate FAIL all inputs (battery dying)
- **재측정 필수**: vctec 셋트 도착 + multimeter polarity 검증 후
- **Berger gate first**: alpha 8-13 Hz peak 검증 통과 시에만 모든 downstream 의미

### 코드 자체

- **24+ verifier / paradigm / lint / logger 모두 selftest PASS + chflags uchg**
- 사용자 hardware 회복 시 즉시 활용 가능
- raw#1 governance hardening (89.6% → 1.79%)
- hexa-lang 4 RFC land + 1 lint impl (12 TP detected)
- Schartner reference 부정확 발견 + retraction
- commit msg drift detection lint (14% FAIL_MISMATCH discovered)

### 발견된 새 bugs

- daily_life_recorder duration metadata mismatch (300s → 50s)
- hexa AOT bool coercion (`fn() == 1` → 항상 false)
- Cyton USB 전원 미지원 (battery only) — measurement 불가능 시간 큰 문제

---

raw#91 honest triad: **claim** = 28+ commits land + 24+ verifier 모두 selftest PASS, 헬멧 hardware VERIFIED; **evidence** = git log + chflags uchg + commit shas + ledger files; **limit** = battery dying 문제로 모든 실측 EEG 결과 invalidated, vctec 셋트 도착 + multimeter 검증 후 Berger gate-gated 재측정 mandatory.
