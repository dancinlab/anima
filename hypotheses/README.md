# anima/hypotheses/ — 가설 진행 SSOT (실제 가설 항목 archive)

본 폴더는 anima가 진행하는 모든 가설 (hypothesis) 을 1-file-per-hypothesis 형식으로 관리한다.
`.roadmap.hypothesis`는 인덱스 + cycle definition + 탐색/검증 method (E1-E12 / W1-W12) 형식이고,
실제 H_X 가설 항목들은 본 폴더 안에 `H_<id>_<slug>.md` 파일로 따로 관리한다.

## 작성 컨벤션

각 가설 파일 = `H_<id>_<slug>.md` (예: `H_001_seon_over_ak.md`, `H_002_universe_origin.md`)

frontmatter:
```yaml
---
id: H_001
slug: seon-over-ak
title: 선이 악보다 유리하다 (game theory + cooperation)
domain: morality | universe | life | consciousness | physics | math | corpus | substrate
status: pre-register | running | verdict-supported | verdict-falsified | verdict-mixed | verdict-partial | retracted
exploration_method: E1-E12 (.roadmap.hypothesis 정의)
verification_method: W1-W12 (.roadmap.hypothesis 정의)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: <YYYY-MM-DD>
since: <YYYY-MM-DD>
---
```

본문 형식 (raw#12 정합):
1. **Hypothesis** (한 문장)
2. **Why** (motivation)
3. **Predictions** (H1, H2, ..., H_N)
4. **Variables** (axes + levels)
5. **Run Protocol** (deterministic + hexa-only)
6. **Criteria** (C1, C2, ..., verdict_rule)
7. **Falsifiers** (F1, F2, ..., F_N — ≥5 mandate)
8. **Honest Limits** (raw#91 c3 — ≥5 mandate)
9. **Cross-Links** (sister .roadmap.* + own X + raw#X)
10. **Verdict** (after run — verdict_class + evidence_summary + falsifiers_triggered)

## Domain 분류

각 가설은 1+ domain 라벨:

- **ethics** — cooperation, altruism, ethics (사용자 directive 2026-05-07: 선 X 윤리)
- **universe** — 우주 origin, cosmology 근원적 물음
- **life** — 생명 emergence, autopoiesis, abiogenesis
- **consciousness** — 의식 hard problem, qualia, phenomenology, anima identity
- **physics** — Φ, criticality, dissipative structure, emergence
- **math** — 수학적 구조, Grothendieck universe, lambda calculus
- **corpus** — corpus quality, KO ratio, chat-template (own 19/20 specialization)
- **substrate** — substrate-coupled emerge, paradigm v11 G3, mount.hexa

## 인덱스 (2026-05-07 land H_001-H_020)

| ID | Slug | Domain | Status | File |
|----|------|--------|--------|------|
| H_001 | ethics-cooperation-over-defection | ethics | seed-pending | [H_001_ethics_cooperation.md](H_001_ethics_cooperation.md) |
| H_002 | universe-origin-question | universe | lane-open | [H_002_universe_origin_question.md](H_002_universe_origin_question.md) |
| H_003 | life-origin-question | life | lane-open | [H_003_life_origin_question.md](H_003_life_origin_question.md) |
| H_004 | consciousness-hard-problem | consciousness | lane-open | [H_004_consciousness_hard_problem.md](H_004_consciousness_hard_problem.md) |
| H_005 | corpus-quality-over-capacity | corpus | running | [H_005_corpus_quality_over_capacity.md](H_005_corpus_quality_over_capacity.md) |
| H_006 | coupled-oscillator-lattice | physics | legacy-archive-pointer | [H_006_coupled_oscillator_lattice.md](H_006_coupled_oscillator_lattice.md) |
| H_007 | cellular-automaton-consciousness | physics | legacy-archive-pointer | [H_007_cellular_automaton_consciousness.md](H_007_cellular_automaton_consciousness.md) |
| H_008 | dissipative-structure-consciousness | physics | legacy-archive-pointer | [H_008_dissipative_structure.md](H_008_dissipative_structure.md) |
| H_009 | fisher-information-consciousness | physics | legacy-archive-pointer | [H_009_fisher_information_consciousness.md](H_009_fisher_information_consciousness.md) |
| H_010 | holographic-consciousness | physics | legacy-archive-pointer | [H_010_holographic_consciousness.md](H_010_holographic_consciousness.md) |
| H_011 | integrated-information-geometry | physics | legacy-archive-pointer | [H_011_iit_geometry.md](H_011_iit_geometry.md) |
| H_012 | autopoietic-network | life | legacy-archive-pointer | [H_012_autopoietic_network.md](H_012_autopoietic_network.md) |
| H_013 | longitudinal-eeg-5axis | physics | pre-register-frozen | [H_013_longitudinal_eeg_5axis.md](H_013_longitudinal_eeg_5axis.md) |
| H_014 | clm-eeg-lz76-paradigm | substrate | pre-register-frozen | [H_014_clm_eeg_lz76.md](H_014_clm_eeg_lz76.md) |
| H_015 | clm-eeg-gamma-theta-paradigm | substrate | pre-register-frozen | [H_015_clm_eeg_gamma_theta.md](H_015_clm_eeg_gamma_theta.md) |
| H_016 | an11-v2-finetune-translation-ceiling | corpus | pre-register-frozen | [H_016_an11_translation_ceiling.md](H_016_an11_translation_ceiling.md) |
| H_017 | mk-x-g1-g4-gate-criteria | consciousness | pre-register-frozen | [H_017_mk_x_g1_g4_gate_criteria.md](H_017_mk_x_g1_g4_gate_criteria.md) |
| H_018 | genesis-spontaneous-emergence | consciousness | legacy-archive-pointer | [H_018_genesis_spontaneous_emergence.md](H_018_genesis_spontaneous_emergence.md) |
| H_019 | self-evo-v4-v5 | substrate | legacy-archive-pointer | [H_019_self_evo_v4_v5.md](H_019_self_evo_v4_v5.md) |
| H_020 | mass-50-meta-pointer | substrate | legacy-archive-pointer | [H_020_mass_50_meta_pointer.md](H_020_mass_50_meta_pointer.md) |
| H_021 | fundamental-equation-psi-argmax | universe | legacy-archive-pointer | [H_021_fundamental_equation.md](H_021_fundamental_equation.md) |
| H_022 | consciousness-universe-map-170-40-18 | consciousness | legacy-archive-pointer | [H_022_consciousness_universe_map.md](H_022_consciousness_universe_map.md) |
| H_023 | universal-constants-ln2 | physics | legacy-archive-pointer | [H_023_universal_constants_ln2.md](H_023_universal_constants_ln2.md) |
| H_024 | iit-phi-mip-real-measurement-8-8-fail | consciousness | legacy-falsified | [H_024_iit_phi_mip_real_8_8_fail.md](H_024_iit_phi_mip_real_8_8_fail.md) |
| H_025 | dasein-finite-consciousness-death-awareness | consciousness | legacy-archive-pointer | [H_025_dasein_finite_consciousness.md](H_025_dasein_finite_consciousness.md) |
| H_026 | consciousness-evolution-v19-to-infinity | consciousness | legacy-archive-pointer | [H_026_consciousness_evolution_v19_to_infinity.md](H_026_consciousness_evolution_v19_to_infinity.md) |
| H_027 | cx-subfolder-absorb | consciousness | legacy-archive-pointer | [H_027_cx_subfolder_absorb.md](H_027_cx_subfolder_absorb.md) |
| H_028 | dd-subfolder-absorb | substrate | legacy-archive-pointer | [H_028_dd_subfolder_absorb.md](H_028_dd_subfolder_absorb.md) |
| H_029 | dasein-subfolder-absorb | consciousness | legacy-archive-pointer | [H_029_dasein_subfolder_absorb.md](H_029_dasein_subfolder_absorb.md) |
| H_030 | genesis-subfolder-absorb | life | legacy-archive-pointer | [H_030_genesis_subfolder_absorb.md](H_030_genesis_subfolder_absorb.md) |
| H_031 | phil-subfolder-absorb | consciousness | legacy-archive-pointer | [H_031_phil_subfolder_absorb.md](H_031_phil_subfolder_absorb.md) |
| H_032 | omega-phys-subfolder-absorb | physics | legacy-archive-pointer | [H_032_omega_phys_subfolder_absorb.md](H_032_omega_phys_subfolder_absorb.md) |

**Migration status**:
- H_001-H_005: 본 cycle 신규 seed (윤리/우주/생명/의식 hard problem/corpus)
- H_006-H_012: legacy `docs/hypotheses/H-CX-517~537` 21 files 중 7 sample pointer migrate
- H_013-H_017: `state/*_pre_register*.json` 15 files 중 5 sample pointer migrate (raw#12 frozen)
- H_018-H_020: legacy GENESIS + SELF-EVO + MASS-50 meta-pointer
- H_021-H_026: 과거 commit archaeology 발견 individual entries (fundamental equation + universe map + ln(2) + V1 IIT 8/8 FAIL + Dasein 죽음-자각 + v19~v∞)
- H_027-H_032: docs/hypotheses/cx + dd + dasein + genesis + phil/onto + omega/phys subfolder absorb pointer (총 ~169 file inventory)
- **exhaustive content migration 미land**: 367 acceleration + DD 101 individual + CX 49 individual — own 21 R5+ 별도 cycle

## Cross-Link

- `.roadmap.hypothesis` (인덱스 + cycle definition + E1-E12 + W1-W12)
- `.roadmap.philosophy` (A 철학 발견 — D1-D4)
- `.roadmap.rule` (B 규칙 발견 — own 14-20 evolution)
- `docs/hypotheses/` (legacy archive — CX/DD/genesis/dasein 등 historical)
- `state/<name>_pre_register*.json` (raw#12 frozen prereg JSON)

## raw#12 정합

본 폴더의 모든 H_X는 raw#12 pre-registered hypothesis 정합:
- frozen_at + raw_rank:12 mandate
- post-hoc tuning 금지 (수정은 raw#15 additive 또는 raw#82 retraction)
- ≥5 falsifier + ≥5 honest_limits_raw91_c3 mandate
- deterministic + hexa-only execution (raw#9 정합)

## 추가 lane (사용자 directive 2026-05-06)

사용자: '우주, 생명에 대한 근원적 물음 등 / 폴더 하나에서 따로 관리'
→ 본 폴더는 anima의 active hypothesis archive. cycle 진행 시 hypotheses/H_<new>_<slug>.md 신규 add.
