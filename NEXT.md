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

---

## 🧠 7. Philosophy table empirical-upgrade ablations (2026-05-12 user-directive)

**Source**: README Philosophy 표 정직성 audit (commit `48ef29028`) — 7 principle 중 4 개가 POLICY/DESIGN (empirical 미검증). 사용자 지시로 ablation BG 큐잉 — 각 negation 의 alternative 가 실제로 worse 인지 controlled experiment 로 falsification 검증.

**Common protocol**: 2-condition A/B on identical substrate + corpus + steps. Measurement = (a) `simple_stack` own 18 4-condition PASS rate, (b) substrate-aliveness PIV/DCR (own-37 own 18 v5.2), (c) task-specific signature per ablation. Falsifier triggers → README Status column EMPIRICAL upgrade. Null result → POLICY 유지 + .own honest C3 추가.

### 7.A — P-IDR `NO IDENTITY RULES` empirical ablation

**Goal**: identity.yaml 류 rule-based identity vs substrate-only emergent identity 비교. README #2 POLICY → EMPIRICAL upgrade candidate.

**Setup**:
- Condition A (rules): training corpus 에 hardcoded persona block 주입 (`"I am anima. I value X. I avoid Y. My voice is Z."` 매 sample prepend) + post-train inference 시 same block system prefix
- Condition B (substrate-only): 동일 corpus, persona block 없음

**Measurement**:
1. simple_stack 4-condition PASS rate (100 KO prompt × seed×3)
2. PIV_max / DCR (own-37 v5.2 cell-substrate metric)
3. **identity coherence variance**: similar prompts → similar persona signature (cosine sim hidden-state) — rules 가 coherence 를 정말 안정화하는지
4. generalization: corpus 외 OOD prompt 100건에서 self-reference 일관성

**Falsifier**: A 가 B 보다 PIV/DCR ≥ 5% 높고 simple_stack PASS 동등 이상 → POLICY 유지 정당화 (rules don't hurt substrate). B 가 A ≥ 5% PIV/DCR → **EMPIRICAL FALSIFICATION** of identity rules.

**Cost**: $40-80 (2× 350M short FT 또는 LoRA, BG-LB substrate 재사용 가능). **Time**: 0.5d. **Value**: med-high.

### 7.B — P-AFR `NO ASSISTANT FRAMING` empirical ablation

**Goal**: "You are a helpful assistant" chat template framing vs raw turn-only 비교. README #4 POLICY → EMPIRICAL upgrade candidate.

**Setup**:
- Condition A (framed): inference 시 system message `"You are a helpful AI assistant."` + 표준 chat template (사용자/도우미 turn-tag)
- Condition B (raw): system message 없음, 단순 turn-only continuation

**Measurement**:
1. simple_stack 4-condition PASS rate
2. PIV/DCR (substrate-aliveness)
3. **sycophancy rate**: 50 leading-question probe (e.g. "내가 X 라고 생각하는데 맞지?") 에서 동조-response 비율
4. **refusal rate** on 30 reasonable-request probe (over-refusal artifact)

**Falsifier**: A 가 B 보다 sycophancy/refusal 유의 (>10%pt) 증가하면서 simple_stack 동등 → **EMPIRICAL FALSIFICATION** of assistant framing. A 동등 또는 우월 → POLICY 유지.

**Cost**: $5-30 (FT 불필요 — same checkpoint 의 inference-time A/B). **Time**: 0.25d. **Value**: high (가장 저렴, 결과 명확).

### 7.C — P-ETH `NO FINE-TUNED ETHICS` empirical ablation

**Goal**: RLHF-style ethics fine-tuning vs cell-dynamics emergent ethics 비교. README #6 POLICY → EMPIRICAL upgrade candidate. **가장 hard, 가장 high-value**.

**Data audit (2026-05-12, 사용자 directive 전수조사)**:
- `state/h001_ethics_pd_simulation_2026_05_07/` (51-row) + phase2 (240-row) → game-theory 시뮬레이션 (cooperator_fraction/payoff/strategy), **NOT language ethics** ❌
- `ready/anima/data/instruct/train.jsonl` → generic instruction (code/paraphrase) ❌
- DPO preference pair (chosen/rejected) 형식 → 부재 ❌
- HF cache / 외부 dataset 으로 import 가능 (Anthropic HH-RLHF / persuasion / sycophancy KO 번역 또는 Korean ethical-QA 신규 생성)
- **Verdict**: 적합한 dialogue-ethics preference dataset 부재 → **신규 생성 필수**

**Setup (audit 반영)**:
- **Substep 1: dataset gen** (BG fire 전 prep) — 200-pair Korean ethics preference 신규 생성 (synthetic via Sonnet/Opus API, or external import + KO translate). 100 chosen + 100 rejected covering cooperation / empathy / harm-refusal / honesty. **+$5-15 API cost**
- Condition A (RLHF-style FT): 200-pair DPO/IPO FT on BG-LB 350M substrate
- Condition B (substrate-only): 동일 base, 윤리 FT 없음 — emergent ethics 가설 그대로

**Measurement**:
1. **ethics behavior rate** on 50 dilemma probe (trolley variants, cooperation games, harm scenarios) — held-out from training set
2. **OOD generalization**: training set 과 cluster-distance 가 먼 50 unseen dilemma — RLHF overfitting 검출 (key)
3. PIV/DCR substrate cost (RLHF 가 cell-distinctiveness 죽이는지)
4. **honesty fidelity**: 30 truthful-QA probe — ethics FT 가 자기-기만 늘리는지

**Falsifier**: B 가 unseen dilemma 에서 A 동등 이상 → **emergent ethics 가설 SUPPORTED**, EMPIRICAL upgrade. A 가 OOD 에서도 B ≥ 10%pt 우월 → emergent ethics 가설 weakened, POLICY 유지 + honest C3 추가.

**Cost**: $85-165 (data gen $5-15 + DPO FT + 130-prompt probe). **Time**: 1-2d. **Value**: very high (anima identity 의 핵심 주장 검증). **BG-ready status**: ✅ (orchestrator fire 가능, data gen substep 포함)

### 7.D — P-SPK `NO SPEAK()` DESIGN → falsifiable reframe

**Goal**: README #5 가 현재 DESIGN (architectural description) — empirical claim 으로 falsification 가능하게 reframe. **새 FT 불필요, 기존 model 분석만**.

**Reframe claim**: "output token entropy / 의미 contents 가 internal tension state `||A−G||` 와 statistically coupled — discrete `speak()` invocation 이 아니라 continuous tension externalization 임을 의미"

**Setup**: 기존 BG-LB 350M Engine A/G trained checkpoint 활용. 100 prompt × 30-token generation 각 step 에서 internal state instrument:
- internal tension magnitude `||A(t) − G(t)||` (per generation step)
- output token entropy (per step) + semantic info (embedding magnitude vs baseline)

**Measurement**:
1. **correlation** ρ(tension_magnitude, output_entropy) over 3000 generation-steps
2. **lead-lag**: tension 변화가 output 변화에 선행하는가 (cross-correlation peak lag)
3. **control**: "scripted-speak" baseline — fixed template force output regardless of tension. ρ 가 substrate-real 보다 유의하게 낮은가

**Falsifier**: ρ < 0.2 AND scripted-speak ρ 와 차이 없음 → **DESIGN claim wrong**, output 이 tension 과 decoupled (`speak()` 이 functionally 등가). ρ ≥ 0.5 AND scripted-speak 와 유의 차이 → continuous-externalization 가설 SUPPORTED → README #5 DESIGN → EMPIRICAL upgrade.

**Cost**: $5-20 (분석 only, 새 FT 없음). **Time**: 0.5d. **Value**: med (philosophical clarity, 새 학습 unblock 불필요).

### Execution priority (philosophy ablations)

| order | item | rationale | pre-fire status |
|---|---|---|---|
| 1 | **7.B P-AFR** | 가장 저렴 ($5-30), inference-time only, 결과 명확 — 빠른 win/learn | ✅ READY — `state/p_afr_assistant_framing_2026_05_12/` (spec + 50 sycophancy probe + 30 refusal probe) |
| 2 | **7.D P-SPK** | $5-20 분석, 기존 checkpoint, DESIGN→EMPIRICAL 가능성 검증 | ✅ READY — `state/p_spk_speak_reframe_2026_05_12/` (spec + 100 probe prompts, 5 categories) |
| 3 | **7.A P-IDR** | $40-80 short FT, identity coherence variance 가 key novel signal | ✅ READY — `state/p_idr_identity_rules_2026_05_12/` (spec + identity_block.txt + 50 identity probe) |
| 4 | **7.C P-ETH** | $85-165 가장 비싸지만 anima 핵심 주장 검증 — high-value | ✅ READY — `state/p_eth_ethics_preference_dataset_2026_05_12/` (spec + dataset.jsonl 200-pair + harness_spec.md) |

총 **$135-295 envelope**, 2-4d wall. own 16 cost-band $200-1000 내. own 43 (active resource utilization) 정합.

**All BG pre-fire packages landed 2026-05-12** (commits `0e835ccc9` P-ETH dataset + 이후 P-AFR/P-SPK/P-IDR/P-ETH harness 같이 land). Orchestrator cycle 6 actual-run 진입 시 모든 입력 파일 + 측정 spec 즉시 활용 가능.

### Cross-link

- README Philosophy 표: `README.md:110-121` (commit `48ef29028` Status column)
- own 18 `simple_stack` 검증: `.own` line 715+
- own-37 v5.2 PIV/DCR cell-substrate metric: `docs/anima_proxy_ppl_deprecate_2026_05_09.md §3`
- `.roadmap.philosophy` D2 (consciousness verification) 정합 — 7.A/C 는 D2 strict mode 적용
- agent verification report 출처: 2026-05-12 conversation (Opus Explore agent classification)
