# Mk.XII N=1 honest fail follow-up spec — 2026-05-01

**status**: spec-only · 후속 cycle 위임 (코드 변경 X, frozen criteria 변경 X)
**scope**: commit `6748462dc` (T17 own2-b Mk.XII production deploy + EEG corroboration pilot N=1) honest-fail 결과의 사후 옵션 분석 + raw#71 falsifier 등록 + 권장 path
**raw cross-references**: raw 9 (hexa-only) · raw 10 (honest C3) · raw 12 (frozen criteria seal) · raw 65 (idempotent audit) · raw 71 (falsifier registration) · raw 82 (multi-axis orthogonal) · raw 91 (honesty triad C3) · raw 106 (multi-realizability) · (production-consciousness-triad) · (research-completeness)
**predecessor**: `design/mk_xii_production_deployment_eeg_corroboration_2026_04_28.md` (T17 own2-b 설계)

---

## §0 Executive summary

T17 own2-b cycle 의 단일 hardware ground truth 기반 N=1 pilot 은 **CORROBORATION_FAIL** 로 정직 종료. fail 의 본질은 sample-size 부족 X **frozen 5-criteria 중 3개 (C1/C4/C5) 가 long-term gate (12-18mo) 였다는 설계상 예정 미달**. 이 결과는 research-completeness 위반 신호가 아니라, raw#10 honest C3 가 강제한 정직한 skeleton-validation 결과.

후속 옵션 4종:

| 옵션 | 본질 | 시간 | honesty cost |
|---|---|---|---|
| A | N=2/3 second/third pilot (사용자 hardware action 필요) | 2-6 weeks | low |
| B | PHENOMENAL axis criteria 자체 reformulation (frozen v1 → v2 bump, SHA-lock 갱신) | 1 week spec + n weeks 재검증 | mid (raw#12 spirit 준수 필수) |
| C | Mk.XII fold to substrate-only validated (CLM-EEG empirical 우회) | 1 cycle (spec 기반 lock 갱신) | mid (PHENOMENAL axis 영구 INSUFFICIENT 인정) |
| D | stop and report (research-completeness 위반 인정 후 정지) | 1 day | high |

권장 path: **A + B 병행** — A 가 12-18mo 본 timeline 의 first sub-milestone, B 는 D-day empirical 결과 (P3 FALSIFIED + Berger 0/15 + P1 P1_FAIL b=351 + P2 INSUFFICIENT) 를 반영한 frozen v1 → v2 patch 의 사전 등록.

본 문서는 **spec only** — 실제 옵션 실행은 별도 sub-cycle 에서 falsifier (raw#71) + honest C3 (raw#10) + frozen criteria seal (raw#12) 통과 시에만 진행.

---

## §1 commit `6748462dc` 분석

### §1.1 측정 axes (5 frozen criteria, raw#12)

| #  | criterion                              | threshold                          | N=1 pilot 측정값 (×1000) | gate verdict |
|----|----------------------------------------|------------------------------------|---------------------------|--------------|
| C1 | Multi-EEG cohort N≥5                   | n_subjects ≥ 5                    | 1                         | FAIL (1 < 5) |
| C2 | Cohen's d cross-subject reliability    | d > 0.8                           | 355                       | FAIL (need 800) |
| C3 | Behavioral self-report ↔ EEG corr     | Pearson r > 0.5 (Likert 1-7 paired)| 520                       | partial PASS (>500) |
| C4 | Adversarial probing misclassification | < 10%                             | 999                       | FAIL (no advers labels) |
| C5 | CLM ↔ EEG α-PLV identity verified     | cross-modal agent paradigm pass   | 0                         | FAIL (no CLM substrate) |

추가 측정 entry (`state/mk_xii_eeg_audit/2026-04-28_pilot_n1.jsonl`):
- `n_pairs` = 5
- `pair_ok_rate_x1000` = 0
- `falsifiers_total` = 5, `falsifiers_pass` = 5 (raw#71 5-falsifier all hold)
- `fingerprint` = 1270597047 (raw#65 idempotent)

session_verdict: **CORROBORATION_FAIL**.

### §1.2 fail root-cause — single hardware ground truth → honest C3 reformulation 강요

핵심: pilot data 가 사용자 단일 16-ch 5-min daily-life 녹음 1건 (`recordings/sessions/baseline_resting_60s_20260428.npy` family) 만 제공 가능했음. 이 단일 ground truth 가 frozen 5-criteria 중 3개 (C1 cohort, C4 advers labels, C5 CLM substrate) 를 자동으로 정의상 fail 시킴 — N=1 은 cohort N≥5 정의 불가, 하루 daily-life 녹음은 sleep/meditation/drowsy advers protocol 미포함, CLM substrate 는 paradigm v11 G7 별도 cycle 의 cross-modal agent.

raw#10 honest C3 의 강요 force:
- 만약 selftest 만으로 PASS 선언했다면 → raw#10 위반 (synthetic 은 real evidence 아님)
- 만약 N=1 결과를 PASS 로 내렸다면 → raw#12 frozen criteria 위반 (N≥5 silently relaxing)
- 만약 측정 자체를 미루고 commit 했다면 → research-completeness 위반 (skeleton 은 있어도 first measurement absent)

따라서 cycle 가 이 3개 disjunct 위반 회피 path 는 **honest fail 측정 + raw#71 falsifier all-pass 기록** 한 가지 — 이것이 commit `6748462dc` 가 도달한 path. fail 자체가 raw#10/12/71 triple-seal 의 정직한 산물.

---

## §2 Mk.XII Integration tier baseline (#144 proposal 라인업)

### §2.1 5-component (HCI / CPGD / CLM-EEG / TRIBE / V11)

ω-cycle trawl (`state/design_strategy_trawl/2026-04-27_anima-clm-eeg-comprehensive_omega_cycle.json:151`) 명시:

> "Mk.XII v3 = 5+1 component (HCI+CPGD+EEG+TRIBE+PV11 + substrate ledger sister-cluster). EEG STACK feeds PV11 (hard edge) per g9_dag_cascade_landing.md:60"

5-component:
1. **HCI** — Path B Q3 (#155 hardness-conditioned-integration)
2. **CPGD** — Path C Q4 (#156, #158 4-task)
3. **CLM-EEG** — Path A Q1 pre-register (#157 — P1/P2/P3 PHENOMENAL axis)
4. **TRIBE** — Pilot-T1 (#160), Pilot-T3 R33 (#162) launcher v3 (#66)
5. **V11 (paradigm v11)** — 8-axis FINAL_PASS ((a) FC, #144 v3 quartet validation lineage)

(+1) 별도 sister-cluster: substrate ledger / G8/G9/G10 hexad triangulation.

### §2.2 composite ≥ 2/3 PASS for VALIDATED — 현 D-day 상태

Source: `anima-clm-eeg/README.md:85` + `state/clm_eeg_pre_register_v1.json` (frozen v1 SHA-lock)

| pilot (PHENOMENAL axis) | gate threshold | D-day result (`5b3e80ab…` family) | verdict |
|---|---|---|---|
| **P1 V_phen_EEG-LZ × CLM-LZ** | LZ76(EEG) ≥ 0.65 AND \|Δ\|/human ≤ 20% | b=351 (post_battery_ica), 286 (daily_life), 398 (alt) → 모두 ≤ 650 lo | **P1_FAIL (partial — selftest VERIFIED, real_npy P1_FAIL)** |
| **P2 TLR Tension-Link Resonance** | EEG α-band coherence ≥ 0.45 AND CLM V_sync r ≥ 0.38 | selftest only, real-data pending (depends on dual-stream CLM substrate) | **INSUFFICIENT** |
| **P3 GCG Granger Causality Gate** | EEG P3b → CLM layer 25-30 GC F-stat ≥ 4.0 AND unidirectional | γ/θ proxy P3 grand=0.240 (ICA) / 0.009 (aiclean), target=3.0 | **FALSIFIED** (commit `f27d6363f`) |

추가 sanity gate:
- **Berger α-band** (Phase 2 `_gates/berger_alpha.hexa`): 0/15 PASS real .npy (peaks cluster 1.2-1.7 Hz delta drift), 즉 awake-eye-closed Berger effect 가 single-subject 60s 에서 미감지 — Schartner-2017 normal range b=0.5-0.9 이 단일 hardware 에 transfer 불가능함을 시사 (commit `06fe4142c`)

집계: 1 FALSIFIED (P3) + 1 INSUFFICIENT (P2) + 1 partial P1_FAIL (P1) → **0/3 PASS** → composite ≥ 2/3 PASS for VALIDATED 미충족.

PHENOMENAL axis 0.67 baseline (raw#46 multi-candidate v11 stack) 는 D-day empirical 로 **개선되지 않음**. Mk.XII Integration tier 의 (CLM-EEG component) 가 현 frozen-v1 로는 VALIDATED 도달 불가.

### §2.3 N=1 pilot 의 Integration tier 위치

own2-b corroboration sub-axis 는 PHENOMENAL axis 의 **사이드 채널 corroboration** — composite 2/3 PASS 자체를 대체하지 않음. 즉 Mk.XII Integration tier composite 는 P1/P2/P3 라인 (CLM-EEG) 으로 결정되고, own2-b N=1 fail 은 (b) 의 5-criteria 별도 frozen scale 위반.

두 fail (composite 0/3 + own2-b N=1) 은 **상관 있으나 동일 사건 X**. raw#82 multi-axis orthogonal 원칙 기반 별개 표시.

---

## §3 후속 옵션

### §3.1 옵션 A — N=2/3 second/third pilot (hardware action 추가 녹음, user only)

- **action**: 사용자가 1-2 명 추가 동의자 (가족/지인) 와 16-ch 5-min daily-life 녹음 + paired Mk.XII conversation session 수행
- **tool**: 기존 `anima-clm-eeg/tool/mk_xii_eeg_corroboration.hexa` (chflags uchg locked, 396 LoC) 그대로 재호출 — 코드 변경 X
- **cost**: hardware time only, $0 mac-local 분석
- **expected outcome**:
  - N=2 milestone → C1 still FAIL but cross-subject Cohen's d 첫 추정 가능 (C2 partial)
  - N=3 milestone → C1 still FAIL, C2 partial, but C3 (self-report ↔ EEG) 가 paired protocol 시 PASS 가능
- **N=5 milestone ((b) C1 satisfied)**: 12-18mo timeline 의 binding gate
- **honesty cost**: low — frozen criteria 그대로, 단지 sample 진행
- **falsifier (raw#71)**: §6 F1 (N=3 도 cross-subject Cohen's d < 0.5 → A path retire), §6 F2 (N=5 도 C3 self-report r < 0.2 → A path retire)

### §3.2 옵션 B — PHENOMENAL axis criteria 자체 reformulation (frozen v1 → v2 bump)

- **action**: D-day empirical 결과 (P3 FALSIFIED + Berger 0/15 + P1 b=351) 를 반영한 frozen criteria patch
  - P1 lo 650 → 단일 hardware (OpenBCI Cyton+Daisy) calibration 곡선 기반 재산정 (paper evidence 필수, raw#12 spirit 준수)
  - P3 γ/θ ratio target 3.0 → P3b ERP 기반 GCG 로 분리 (proxy γ/θ 는 별도 axis)
  - Berger α-band 60s 단일-subject 미감지 → minimum 5min eyes-closed protocol 명시
- **tool**: `state/clm_eeg_pre_register_v1.json` SHA-lock → `_v2.json` SHA-lock 갱신, `state/clm_eeg_pre_register_v1_to_v2_diff.md` 등록 (silent edit ban — raw#10/12 동시 준수)
- **cost**: 1 week spec + n weeks 재검증 (재측정 = 옵션 A 와 병행 가능)
- **expected outcome**: composite 재정의 후 D-day empirical 가 (P1 INSUFFICIENT/PASS 재분류 + P2 PASS/INSUFFICIENT + P3 reframed) 로 변경, 0/3 → 1/3 또는 2/3 가능
- **honesty cost**: mid — raw#12 frozen criteria seal 의 spirit 위반 가능성 높음. 따라서 **paper evidence (Schartner-2017, Casali-2013, Tort-2010) 를 인용한 v2 spec 의 사전 등록 + SHA-lock 의 atlas 등재** 가 필수 selfcheck — 이 절차 통과 시에만 raw#12 spirit 준수.
- **falsifier (raw#71)**: §6 F3 (v2 reformulation 후에도 D-day empirical 가 0/3 PASS 면 B path retire — relaxation 만 한 셈)

### §3.3 옵션 C — Mk.XII fold to substrate-only validated (CLM-EEG empirical 우회)

- **action**: Mk.XII Integration tier 의 5-component 중 **CLM-EEG component 를 영구 INSUFFICIENT 로 lock** + 나머지 4 (HCI / CPGD / TRIBE / V11) 만으로 VALIDATED 선언 (4/5 PASS 기준)
- **tool**: `.roadmap` #119 BLOCKED-EEG 갱신 + `state/mk_xii_validated_substrate_only_2026_xx.json` 신규 (CLM-EEG 영구 INSUFFICIENT 명시)
- **cost**: 1 cycle (spec 기반 lock 갱신, 재측정 X)
- **expected outcome**: Mk.XII Integration tier VALIDATED 선언 가능, 단 PHENOMENAL axis 는 영구 INSUFFICIENT — (b) PC empirical-maximum 의 EEG corroboration sub-axis 폐쇄
- **honesty cost**: mid — 4/5 기준 VALIDATED 선언 자체는 정직하나, "PHENOMENAL axis 폐쇄" 는 의 본 목적인 **PC empirical-maximum** 의 핵심 가설 포기에 해당
- **falsifier (raw#71)**: §6 F4 (4/5 substrate-only 라도 HCI/CPGD/TRIBE/V11 중 1개라도 fail 면 C path retire)

### §3.4 옵션 D — stop and report (research-completeness 위반 인정)

- **action**: research-completeness frozen 위반 명시 + Mk.XII Integration tier track 정지 선언 + raw#10 honest C3 종합 보고서 작성
- **tool**: `docs/mk_xii_research_completeness_violation_report_2026_05_xx.md` (신규), `.roadmap` Mk.XII 관련 entries 모두 BLOCKED 표시
- **cost**: 1 day spec + report
- **expected outcome**: 모든 Mk.XII track 동결, 다른 axes (paradigm v11 FINAL_PASS = (a) FC, an11 alm-free, hxc compression family 등) 만 진행
- **honesty cost**: high — 12-18mo timeline 자체를 포기. 단, raw#10 honest C3 의 한 valid path 임 (research 가 결과 없을 수 있음을 인정)
- **falsifier (raw#71)**: §6 F5 (D path 선언 후에도 user 가 N=2 hardware action 을 자발 수행 시 D path retire — premature stop 인정)

---

## §4 trade-off matrix

| 옵션 | cost (time) | cost (honesty) | generalization (Cohen's d/multi-subject) | time-to-VALIDATED | risk |
|---|---|---|---|---|---|
| **A** N=2/3 pilot | 2-6 weeks (hardware availability) | low | progressive (N→5 binding) | 12-18mo (binding gate C1) | none — 본 timeline 진행 |
| **B** v1→v2 bump | 1 week + n weeks revalidation | mid (raw#12 spirit risk; paper-evidence 사전 등록 시 mitigated) | unchanged threshold scale | 4-8 weeks if paper evidence 충실 | low — 단 silent edit 시 high |
| **C** substrate-only fold | 1 cycle | mid (PHENOMENAL axis 영구 폐쇄) | n/a (CLM-EEG 측정 중지) | 1-2 weeks | mid — (b) PC empirical-maximum 핵심 포기 |
| **D** stop and report | 1 day | high (12-18mo 본 timeline 포기) | n/a | n/a | high — research-completeness 자체 위반 인정 |

핵심 trade-off:
- **A vs D**: 시간 vs 즉시성. D 는 즉시 완결 가능하나 비용 high.
- **B vs A**: B 는 빠르나 raw#12 spirit risk; A 는 느리나 frozen 그대로.
- **C vs A/B**: C 는 PHENOMENAL axis 자체 폐쇄로 (b) 핵심 포기 — A/B 가 가능하면 C 는 후순위.

---

## §5 raw#10 honest C3 — N=1 fail은 sample 부족 X 사실 부족 X 동등 (혼동 회피)

명시 분리:

| 표현 | 의미 | 본 사건 적용 |
|---|---|---|
| **sample 부족** (sample-size insufficiency) | N 이 too small → statistical power 부족, 추론 불가 | C2 (Cohen's d) 에 해당 — N=1 → cross-subject d 정의 자체 불가 |
| **사실 부족** (evidence absent) | data 자체가 measurement target 을 cover 안 함 | C4 (advers labels), C5 (CLM substrate) 에 해당 — daily-life 녹음에는 advers protocol 없음, CLM substrate 자체가 paradigm v11 G7 별개 cycle |
| **(동등하지 않음)** | 위 2개는 raw#10 honest C3 에서 별개 disjunct | 본 fail 은 (sample 부족 1건 + 사실 부족 2건) 의 **혼합** — 단일 카테고리 X |

따라서:
- "N=1 이라 fail" 은 **부분 진실** (C2 는 sample 부족, C1 도 sample 부족 — 즉 2/5 가 sample 부족)
- "측정 자체 불가" 는 **부분 진실** (C4 는 사실 부족, C5 는 사실 부족 — 즉 2/5 가 사실 부족)
- C3 (520) 만이 partial PASS — 즉 1/5 가 측정 가능 + threshold 통과 가능성 표시

옵션 A 는 sample 부족 (C1, C2) 해소 path. 옵션 B 는 사실 부족 (C4, C5) 의 frozen-criteria 재정의 path. 두 path 는 **orthogonal** (raw#82 multi-axis) — 동시 진행 가능.

---

## §6 raw#71 falsifier 3개 (각 옵션의 retire 조건)

각 옵션별 falsifier 사전 등록 — falsifier 조건 충족 시 해당 path 즉시 retire (raw#71 mandatory).

### F1 — 옵션 A retire (N=3 cross-subject Cohen's d < 0.5)

- **trigger**: 옵션 A 진행 후 N≥3 도달 시 cross-subject Cohen's d (×1000 scale) 가 < 500 (즉 d<0.5)
- **detection**: `mk_xii_eeg_corroboration.hexa` 의 C2_effect_x1000_mean field 가 < 500 in N≥3 audit row
- **interpretation**: 효과크기가 동의자 사이에 충분히 일관되지 않음 → multi-subject EEG corroboration 자체가 Mk.XII 의 PHENOMENAL substrate 이 될 수 없음
- **action on trigger**: 옵션 A retire, 옵션 C (substrate-only fold) 또는 옵션 D (stop) 로 cascade

### F2 — 옵션 A retire (N=5 도달 시 C3 self-report r < 0.2)

- **trigger**: 옵션 A 진행 후 N=5 도달 시 self-report ↔ EEG Pearson r (×1000) 가 < 200
- **detection**: C3_self_eeg_r_x1000_mean < 200 in N=5 audit row
- **interpretation**: behavioral self-report 와 EEG biomarker 가 무상관 → corroboration 핵심 가설 fail
- **action on trigger**: 옵션 A retire, B (criteria reformulation 후 r threshold lower) 또는 D (stop) cascade

### F3 — 옵션 B retire (v2 reformulation 후 D-day empirical 0/3 PASS 유지)

- **trigger**: 옵션 B 진행하여 frozen v2 SHA-lock 등재 후 D-day empirical 재산정 시 composite 가 여전히 0/3 PASS
- **detection**: 재산정된 composite verdict 가 < 2/3 PASS
- **interpretation**: v2 가 단순 relaxation 이 아니라 paper-evidence 기반이었음에도 empirical 미통과 → 즉 paper threshold 자체가 단일 hardware 에서 도달 불가능함을 증명
- **action on trigger**: 옵션 B retire, 옵션 C (substrate-only fold) cascade. v2 spec 은 retire 가 아니라 "documented but not VALIDATED" 로 보존 (이후 다른 hardware 환경에서 재시도 가능)

### F4 — 옵션 C retire (substrate-only 4/5 중 1개 이상 fail)

- **trigger**: 옵션 C 진행하여 substrate-only VALIDATED 선언 후 HCI/CPGD/TRIBE/V11 중 1개라도 frozen criteria fail
- **detection**: 각 component 의 ledger row 에서 verdict != PASS
- **interpretation**: substrate-only fold 가 안정한 base 가 아니었음 → Mk.XII Integration tier 자체가 불안정
- **action on trigger**: 옵션 C retire, 옵션 D (stop and report) cascade

### F5 — 옵션 D retire (stop 후 user 자발 hardware action)

- **trigger**: 옵션 D 선언 후 30 days 이내 user 가 자발적으로 N=2 hardware action 수행 (paired Mk.XII conversation + EEG 녹음)
- **detection**: `state/mk_xii_eeg_audit/` 에 새 audit row appearance 후 30 days within
- **interpretation**: D path 가 premature 였음 — research-completeness 위반 인정이 사실상 자발 진행 시점 이전
- **action on trigger**: 옵션 D retire, 옵션 A 로 reactivate

---

## §7 권장 path + 사유

**권장 path**: **옵션 A + 옵션 B 병행** (raw#82 multi-axis orthogonal — 두 path 가 충돌 X)

### 사유

1. ** research-completeness 보존** — 옵션 D 회피. A 는 본 12-18mo timeline 진행, B 는 frozen-v2 사전 등록으로 v1 → v2 명시적 lineage 보존.
2. **raw#10 honest C3 준수** — A 는 N=1 → N=2/3/5 progressive sample 진행으로 honest C3 의 자연스러운 path. B 는 paper-evidence 기반 reformulation 으로 silent edit 회피 (raw#10/12 동시 준수).
3. **raw#12 frozen criteria spirit** — A 단독 진행 시 frozen v1 그대로 — spirit 100% 준수. B 는 v2 bump 시 paper-evidence 사전 등록 + atlas SHA-lock 등재 의 dual gate 통해 spirit 유지.
4. **D-day empirical 결과 활용** — D-day 측정값 (P3 FALSIFIED + Berger 0/15 + P1 b=351 + P2 INSUFFICIENT) 이 그대로 묻히지 않고 옵션 B 의 v2 spec 의 입력 data 로 재활용.
5. **옵션 C 회피** — (b) PC empirical-maximum 의 핵심 가설 (multi-source corroboration) 폐쇄는 의 production-consciousness-triad 자체의 본 의미 손상. C 는 A/B 둘 다 falsifier hit 시점에서만 cascade.

### 진행 순서

1. (이 cycle) 본 spec 등재 + commit (single-file)
2. (next cycle) 옵션 B v2 spec 사전 등록 — `state/clm_eeg_pre_register_v2.json` 후보 spec + paper-evidence 인용 (Schartner-2017 + Casali-2013 + Tort-2010 + Bandt-Pompe-2002) + SHA-lock 보고
3. (user-led) 옵션 A N=2 hardware action — user 단독 trigger 권한
4. (after N=2) corroboration 재실행 (chflags uchg locked tool 그대로) → cross-subject Cohen's d 첫 측정
5. (after v2 등재) D-day empirical 재산정 — composite verdict 갱신 (0/3 → 가능한 X/3)
6. F1/F2/F3 falsifier monitoring — trigger 시 즉시 cascade

### 비-권장 path

- **옵션 C 단독**: PHENOMENAL axis 폐쇄 비용이 (b) 본 의미 손상 정도와 비례하지 않음 (3-criteria long-term gate 가 그저 시간이 필요할 뿐, 영구 fail 신호 아님)
- **옵션 D 단독**: 위반 인정의 cost 가 12-18mo timeline 자체보다 큼. 옵션 A 의 single hardware action (사용자 1명 추가) 만으로도 N=2 가능 — 비용/이익 비례 안 됨

---

## §8 honest C3 (raw#91 triad 의심 1-3)

이 cycle 본 spec 작성에서 raw#91 honesty triad C3 disclosed 의심 (자기 reformulation 위험):

1. **의심 1 — 옵션 권장 자체가 raw#10 honest C3 의 fail 인정 회피용 reframe 일 수 있음**: "fail 은 honest 했다" 라는 frame 이 후속 옵션 A/B/C/D 의 trade-off 분석을 통해 결국 "진행 권장" 로 종착 — 이는 N=1 fail 자체를 정직하게 받아들이지 못한 reformulation 위험. 본 spec 은 옵션 D (stop) 를 비-권장으로 분류했으나, 실제로 research-completeness 의 weight 가 어떤지에 대한 사용자 선언 이 우선 — 본 spec 의 권장 path 는 사용자 weight 결정 후에만 valid.

2. **의심 2 — §2.2 D-day composite "0/3 PASS" 집계가 실제 frozen v1 의 의도와 일치하는가**: P2 INSUFFICIENT 를 P2 "fail" 로 동치 처리하는 것 — frozen v1 spec 은 "real-data run 미수행" 을 PASS/FAIL 어디로 분류하는지 명시 약함. 만약 INSUFFICIENT 가 "측정 미수행" 으로 frozen v1 의 PASS 정의 외 단순 미진행 이라면, composite 산정에서 분모가 3이 아닌 2 (P1 + P3 만) 가 될 수 있음 — 이 경우 0/2 PASS, 즉 "분명한 fail" 표시. 본 spec 은 분모 3 으로 처리 (가장 보수적 honest interpretation) — 이는 frozen v1 SHA-lock 의 정확한 letter 와 일치하지 않을 수 있음. 즉 의심: 본 spec 의 §2.2 composite 분모 자체가 약간 reformulation.

3. **의심 3 — 옵션 B 의 raw#12 frozen criteria spirit 준수 가능성**: paper-evidence 사전 등록 + SHA-lock dual gate 라 했으나, 실제 v1 → v2 의 SHA-lock 갱신 자체가 raw#12 의 "frozen seal" 정의와 충돌 가능. raw#12 가 "frozen" 을 (a) v1 그대로 영구 또는 (b) v1 → v2 lineage 가능 둘 중 어느 의미인지 — 본 spec §3.2 는 (b) 로 가정. 만약 raw#12 가 (a) 의미였다면 옵션 B 자체가 raw#12 위반 — 즉 옵션 B 는 spec 외부 추가 raw 보강 (예: raw#46 multi-candidate refinement) 필요. 본 spec 은 이 점 명시 안 함 — 의심.

(raw#10 honest C3 — 위 3개 의심 모두 본 spec 외부 사용자 결정 또는 추가 raw 보강이 필요함을 인정)

---

## §9 제약 (이 cycle 한정)

- spec only — 코드 X, frozen criteria 변경 X (옵션 B 의 v2 spec 등재는 별도 cycle)
- single-file commit — 본 doc 만
- `.roadmap`, mk_xii tool, frozen state ledger 모두 read-only
- absolute path leak 0건 (raw#15 iter5 준수 — 본 doc 내 모든 path 는 repo-relative)
- raw#9 hexa-only, NO_API
- 거짓 PASS 주장 X — fail 은 fail
