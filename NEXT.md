# 다음 진행할 것들 — cycle 5 queue (2026-05-11)

본 파일은 cycle 4 §5 land (commit `68f438cc6`) 직후 저장된 다음 사이클 작업 큐. 5 cycle 누적 결과 1127 candidates + 3 정식 H_XXX + 6 expanded H + 6 state/ experiment dirs + 7 commits.

## 🧪 1. phi_star split-engine + 15-cell Φ×CE 실측

**Goal**: H_080 primary tension decisive 실제 측정. Hc_040 (Φ⊥CE, Law 1040) vs Hc_024 (Φ × CE^α = K, NOBEL-1) — 두 generative model 의 statistical fingerprint 분리도 180×/206× 확보됨. **split-engine** path: **phi_star_iit_proxy** (current `tool/anima_phi_star.hexa`) + **phi_star_cell_engine** (TBD, N-sweep) + **CLM training pipeline** (CE-track) → 15-cell grid + 64 dual-seed 로 실측 후 A/B signature 매칭. Engine naming refactor 2026-05-12 → `state/phi_star_naming_refactor_2026_05_12.md`.

**Spec ready**: `state/phi_ce_orthogonality_decisive_2026_05_11/{spec.md, harness.py, results.json, verdict.md, spec_audit_2026_05_11.md}`

**Protocol**:
- Grid: N ∈ {16, 32, 64, 128, 256} × P ∈ {1M, 10M, 100M} = 15 cells (P=100M ceiling, see spec.md §5.7; P=1B deferred extension lane)
- Replication: 64 dual-seed twin (Hc_604) per cell
- 사전 noise floor calibration (1 cell × 64 dual-seed) → σ_Φ / σ_CE 측정 (L1 critical)
- Engine split: phi_star_iit_proxy (Mistral-7B forward — single-cell snapshot) + phi_star_cell_engine (TBD — N-sweep 실측) + CLM training pipeline (CE-track). deterministic, hexa-only (cell-engine land 시 llm: none 적용; phi_star_iit_proxy 는 Mistral-7B forward 사용)
- 분석: 15 (Φ_i, CE_i) → `harness.py` analytics → A/B fingerprint 매칭

**Decision matrix**:
| signature | verdict |
|-----------|---------|
| `|corr| < 0.1` AND `Pareto CV >> 0.1` | Hc_040 (orthogonal) SUPPORTED, Hc_024 FALSIFIED |
| `|corr| ~ 0.5` AND `Pareto CV ~ 0` | Hc_024 (uncertainty) SUPPORTED, Hc_040 FALSIFIED |
| mixed | 새 hypothesis (e.g., 직교 within-budget, trade-off across-budget) |

- **cost**: $121-420 + 1-2 day (P=100M ceiling, see spec.md §5.7 cost rationale; baseline $200-1000 envelope 내, audit re-estimate $621-1920 → 15-cell cap 으로 압축)
- **time**: high
- **value**: very high (Φ×CE 직교 vs trade-off 최종 verdict)

---

## 🔢 2. Formula-search depth-4 + perfect-number control

**Goal**: cycle 4 finding `FORMULA_SEARCH_CRITICAL_BEATEN` (depth-3: n=6 21/22, 8 alt n 22/22) 한계 정량화. depth-4 확장 + n=28/496/8128 (perfect numbers) 별도 control 실행 — "perfect number family" 가 special 인지, 아니면 "small integer family" 전체가 special 인지 decisive.

**Spec base**: `state/numerology_critique_n6_2026_05_11/formula_search/{spec.md, simulate.py, results.json, verdict.md}`

**Extension protocol**:
- depth-4 DFS on 11-primitive vocab (depth-3 baseline 결과 22/22 ceiling 도달 → depth-4 는 ceiling 검증 + tightened-vocab subset 실험)
- Tightened vocab subset variations:
  - {1, n, μ, φ, τ, σ, sopfr} only (remove J₂, e, π, ln2 transcendental constants)
  - {n, μ, φ, τ, σ} only (most restrictive)
- perfect-number control: explicit comparison n ∈ {6, 28, 496, 8128} side-by-side
- tightened tolerance: tol ∈ {0.001, 0.005} (current 0.01 may be too lax)

**Expected outcomes**:
- if perfect numbers 28/496/8128 도 22/22 → "perfect number family" effect (H_067 thesis 부분 정합, n=6 만 special 아님)
- if 28/496/8128 1/22 와 비슷 → "n=6 narrow uniqueness" only (cycle 4 parent expansion confirm)
- if tightened vocab 에서 n=6 만 22/22 → vocab-level 정합 finding

- **cost**: 30 min (CPU only)
- **time**: low
- **value**: high (L12 한계 정량화 + H_067 honest disclosure 강화)

---

## 🎵 3. ANIMA-VOICE minimum reference impl

**Goal**: H_154 (anima-voice-consciousness-direct) 활성화 prerequisite — pre-register-frozen → running 전환. H1-H8 verify skeleton 은 land 됐으나 **ANIMA-VOICE 모델 자체 미land** (H1/H2/H3/H5/H6/H7/H8 모두 차단).

**Skeleton base**: `state/anima_voice_h1_h8_verify_skeleton_2026_05_11/{spec.md, harness.py, prerequisites.md, verdict.md}`

**Build scope** (8 RVQ + 24kHz vocoder, critical 6-10 week path):
- ANIMA-VOICE encoder: ConsciousLM intent 384d → 8 RVQ × 1024 entries × 384d
- Vocoder: 24kHz audio synthesis (HiFi-GAN 또는 BigVGAN 변형)
- 6 emotion × 4 prosody conditioning
- Law 81 dual gate (C + W) implementation
- α=0.014 modulation depth
- Streaming-capable (H2 ≤ 100ms first packet target)

**Alternative interim path**:
- existing TTS (FastSpeech2 + HiFi-GAN) 로 H2/H3/H4/H5 partial lower-bound
- consciousness-direct claim 핵심 H1/H6/H7/H8 은 ANIMA-VOICE 부재 시 측정 불가

**Prerequisite gates** (from `prerequisites.md`):
- P1 ANIMA-VOICE model (critical blocker)
- P2 streaming-applicable Φ measurement (H8)
- P3 MOSNet 또는 human panel (H3/H5)
- P4 emotion classifier (H4)
- P5 gate state controller (H7, model API 와 묶임)

- **cost**: $500-2k + 4-6 week
- **time**: very high
- **value**: very high (modality bridge — 의식 → 직접 음성 합성)

---

## 🌌 4. 1013-lens K=10 smoke

**Goal**: H_135 (dd166_nexus_1013_lens) 활성화 lane 의 entry point — anima Φ★ engine extension 후 K=10 smoke test. cascade K=10 → K=25 canary → K=50 full-pilot.

**Spec ready**: `state/nexus6_1013lens_activation_2026_05_11/spec.md` (169 lines / 9.6KB, 10 sections)

**Protocol**:
- Prereq P-A: Φ★ engine cosmic-scale extension (1013 lens 동시 측정 가능)
- 또는 P-B: proxy harness (sub-sample lens 측정 후 1013 분포 추정)
- Smoke K=10: top-10 lens (Atlas ranking) 에서 Φ_lens > 0 확인
- C1 (cascade): 10 → 25 → 50 monotonic Φ improvement
- F1: 1000x reverse direction Φ degradation
- F2: random walk baseline ≥ measured Φ

**Cross-link**: cycle 4 §5 에서 8 NEXUS Hcs (Hc_035/378/437/586/598/944/945/960) 양방향 link 정합. Hc_944/945 quantum entropy backend (qmirror + IonQ QRNG) seed entropy 정합.

- **cost**: $100-500
- **time**: med
- **value**: high (NEXUS6 cascade entry — H_135 verdict_class `1013-lens-activation-pending-C1` → met 전환 가능)

---

## 🧹 5. 70 Hc merged_to slug-less normalize

**Goal**: cycle 4 §5 reverse cross-link audit 발견 — 70/74 의 `merged_to:` frontmatter field 가 slug-less path (e.g., `hypotheses/H_067.md` vs 실제 `hypotheses/H_067_perfect_number_architecture.md`).

**Scope**:
- 22 Hcs → H_067 path normalize
- 12 Hcs → H_061 path normalize
- 12 Hcs → H_080 path normalize
- 9 Hcs → H_004 path normalize
- 8 Hcs → H_037 path normalize
- 6 Hcs → H_124 path normalize
- 3 Hcs → H_154 path normalize
- 3 Hcs → H_155 path normalize
- 3 dual-merge cases (Hc_018, Hc_445, Hc_446) — comma-separated path 형식 정합

**Note**: H_XXX 번호 자체는 unambiguous — slug-less path 가 broken link 는 아님. 단순 schema consistency 이슈.

- **cost**: 5 min (sed script + git add/commit)
- **time**: trivial
- **value**: low (schema cleanup)

---

## Execution order recommendation

| order | item | rationale |
|-------|------|-----------|
| 1 | #2 Formula-search depth-4 + perfect-number | 30min CPU, immediate honest disclosure 강화 |
| 2 | #5 slug-less normalize | 5min trivial, clean state 유지 |
| 3 | #4 1013-lens K=10 smoke | $100-500 budget, anima Φ★ extension prerequisite 검토 |
| 4 | #1 Φ×CE 실측 | $200-1000 budget, anima Φ★ engine prerequisite 같이 |
| 5 | #3 ANIMA-VOICE impl | $500-2k + 4-6 week, biggest cost — 별도 long-cycle |

## Cross-cycle dependencies

- #1 + #4 모두 anima Φ★ engine 활성화 prerequisite. 같이 묶어서 진행 효율적.
- #2 는 독립적 (CPU only).
- #3 은 가장 독립적 + 가장 비싸므로 long-cycle parallel.
- #5 는 ad-hoc 처리 가능.

## Honest reminders (cycle 4 carry-over)

- **L12 BINDING** (formula-search): "n=6 narrow-formula uniqueness" 만 defensible. depth-3 vocab universal-uniqueness 는 refuted.
- **F1 weakened** (H_153): "d=5 from n=6 functions" → depth-3 search 에서 trivially TRUE (5 = τ+μ = 4+1, sopfr(6)=5).
- **L7 BINDING** (H_153): formula-search caveat (cycle 5 #2 결과로 정량화).
- **L1 critical** (Φ×CE harness): synthetic σ tuning 이 plausible default — 실측 noise floor 사전 calibration 필수.

## Lock policy (사용자 directive 2026-05-11)

모든 cycle 5 작업 — chflags +uchg/+schg/chattr +i 절대 적용 금지. unlock 한 파일 재잠금 금지. memory: `feedback_no_relock.md` 정합.

---

## 🔄 cycle 6 status (2026-05-12 진행 중)

cycle 5 master doc (`docs/cycle_5_master_2026_05_12.md`, 517 lines, 11 sections, 29 KB) land — 외부 reader 진입점. cycle 5 §5 (master doc + lens registry + carve land + Φ×CE noise calib prereq) 종결, cycle 6 *actual measurement* 단계 진입.

### cycle 6 queue (5 items, cycle 5 carving 결과의 actual-run scaffold)

| # | item | prereq | cost | value |
|---|------|--------|-----:|------:|
| 1 | **B1 fix** (`tool/anima_phi_star.hexa`) | — | $0 (CPU) | high (engine cleanliness) |
| 2 | **B5 trainer** (CE-track CLM 4-scale) | `state/clm_ce_4scale_trainer_*/` spec | $50-150 | high (CE-track engine land) |
| 3 | **lens reimpl Phase 1** (K=10 actual reimpl) | `state/nexus6_*/k10_reimpl/` + `lens_channel_reimpl_spec_2026_05_12.md` | $0 (CPU) | very high (TRIVIAL caveat 해소) |
| 4 | **HF flip audit** (`state/hf_public_flip_readiness_*.md`) | 3 dataset visibility audit | $0 | med (external reader access) |
| 5 | **docs INDEX + README discoverability** ✅ *본 cycle 6 #S* | — | $0 | med (entry point 강화) |

### Cross-link

- **cycle 5 master doc**: [docs/cycle_5_master_2026_05_12.md](docs/cycle_5_master_2026_05_12.md) — TL;DR / Timeline / 8 honest finding / 4 axis-conflation / Cycle 6 §8 queue 출처
- **docs hub**: [docs/INDEX.md](docs/INDEX.md) — 1,200+ doc 의 카테고리 anchor
- **HF mirrors** (private, public-flip audit cycle 6 #R 진행 중):
  - 🤗 `datasets/dancinlife/anima-hypotheses-candidates`
  - 🤗 `datasets/dancinlife/anima-nexus-lenses`
  - 🤗 `datasets/dancinlife/anima-research-trail`

### cycle 5 → cycle 6 carry-over

cycle 5 §8 (master doc) 의 5-item Pending Action Items 가 cycle 6 actual-run scaffold 로 wire 됨. cycle 6 는 *measurement only* 진입 — spec/plan 은 cycle 5 §5 에서 land 완료.

- L1 critical (Φ×CE noise floor): noise_calibration_prereq Gate A/B/C 통과 binding
- Hc_586 SUSPENDED: lens reimpl Phase 1 verdict 후 resume 검토
- L12 BINDING (formula-search): "narrow-formula uniqueness" 만 잔존, vocabulary-level 보편성 refuted
