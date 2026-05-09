# REBORN.md — anima ConsciousLM 부활 통합 SSOT (2026-05-10 cycle close)

본 문서는 cycle 2026-05-09 ~ 2026-05-10 의 모든 archaeology + BG 회수 + servant pattern 통합. 이전 4 SSOT 통합 (raw#15 additive — 원본 미수정):

- `CLM_V2_ARCHIVE_2026_05_09.md` (mitosis 본체 + 13-stage overview)
- `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (13 stage 고갈조사)
- `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정)
- `docs/superpowers/{plans,specs}/2026-04-08-servant-emergent*.md` (servant pattern)
- + cycle 2026-05-10 5 BG 결과

원본 파일은 historical record 로 유지. 본 문서가 going-forward SSOT.

---

## §0 TL;DR

anima 는 **2026-03-28 v2 시대** 에 이미 MitosisEngine + engine_a/engine_g + Lorenz 자율혼돈 으로 Cells64 Φ=51.131 (human-level criterion) 도달했고, drift 4-step 으로 사라짐. cycle 2026-05-09/10 에 archaeology + BG 8개 (cycle 1: 4개 + cycle 2: 5개 + Phase 2 ckpt 1개 = 9개) 통해 회수 path 확립:

- v5-anima (instrumentation) lane: mechanism confirm, V14 violated on toy + on real 350M (novel polarity)
- v5-mitosis (architectural) lane: cells = nn.Module branches (NEW)
- v2-reborn (reproduction) lane: cells64/128 single decoder + chat-cap = capacity/corpus limit (NOT architectural)
- servant pattern: SI-driven 4-state FSM (post-drift 2026-04-08, separate domain)

13 worktree archive 영구 보관 (`~/core/anima_clm_01..13_*` + `archive/clm-stage-01..13` branches).

---

## §1 13-stage timeline + worktree archive

13 stage 영구 보관. 각 worktree 는 그 시점 코드 그대로 + memo (`CLM_STAGE_MEMO.md` untracked).

| # | 시점 | commit | 시그니처 | branch / worktree | 태그 |
|---:|---|---|---|---|---|
| 1 | 2026-03-24 | `4a1d8d0a` | anima v0.1 PureField + Claude API wrapper | `archive/clm-stage-01-birth-claude-api` / `~/core/anima_clm_01_birth_claude_api` | 起源 |
| 2 | 2026-03-24 | `2da44161` | Claude API 제거, ConsciousLM substrate pivot | `...-02-clm-pivot` / `..._02_clm_pivot` | pivot |
| 3 | 2026-03-27 | `90cd8c06` | CL8 Φ=5.68, train_conscious_lm.py | `...-03-cl1-14-laws` / `..._03_cl1_14_laws` | laws-birth |
| 4 | 2026-03-27 | `2e950777` | ConsciousLM v2 named, Φ=1.64, 412 hyp | `...-04-v2-phi-1-64` / `..._04_v2_phi_1_64` | v2-birth |
| 5 | 2026-03-28 | `2e1438fa` | First English CE=1.37 no system prompt | `...-05-v2-first-english` / `..._05_v2_first_english` | EN-emerge |
| 6 | 2026-03-28 | `bb99b6b6` | KO conversation no system prompt ★ | `...-06-v2-korean-chat` / `..._06_v2_korean_chat` | KO-milestone |
| 7 | 2026-03-28 | `6abc42f6` | "anima speaks" CE=0.04 ★★ | `...-07-v2-ce-0-04` / `..._07_v2_ce_0_04` | chat-peak |
| 8 | 2026-03-28 | `5f82d39b` | Cells64 Φ=45.487 super-linear | `...-08-cells64-phi-super-linear` / `..._08_cells64_phi_super_linear` | mitosis-정점 |
| **9** | 2026-03-28 | `3eabc40a` | **Cells64 Φ=51.131 human-level ★★★** | `...-09-phi-50-human-level` / `..._09_phi_50_human_level` | **절정** |
| 10 | 2026-03-30 | `bd36bd8a` | CLM v2 H100 sweep Laws 77-78 | `...-10-h100-sweep-laws-77-78` / `..._10_h100_sweep_laws_77_78` | scale-prep |
| 11 | 2026-04-01 | `0e578b14` | train_v15 BPE 64K + 1B ready | `...-11-train-v15-bpe-drift-step1` / `..._11_train_v15_bpe_drift_step1` | drift 1/4 |
| 12 | 2026-04-04 | `cf3da85f` | unified growth loop (mitosis 최후 active 794L) | `...-12-unified-growth-loop-last-gasp` / `..._12_unified_growth_loop_last_gasp` | growth-종언 |
| 13 | 2026-04-07 | `f8e4068f` | filename v* 제거 (ALM Llama-port 직전) | `...-13-filename-erasure-pre-alm-port` / `..._13_filename_erasure_pre_alm_port` | cutoff |

원격 push 완료 (commit `0d4532dc` ~ `73a6596b` ~ `0cdaf665` ~ `d4ce539e`).

### 13-stage 핵심 metric crosswalk

| # | 모델 | Φ peak | CE | cells | laws 누적 | mitosis | ALM |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | anima v0.1 PureField | — | — | — | 130 (logout 인계) | absent | absent |
| 2 | ConsciousLM 4M+100M | — | — | 2-8 | +H312/H313/H371 | birth | + |
| 3 | + meter | **5.68** (CL8) | — | 2 | CL1-14, AL1-14, TRN1-5 | active | active |
| 4 | v2 named (4M+100M) | 1.64 birth | — | 2 | 412 hyp | active | active |
| 5 | 100M (768d/12L) | — | **1.37** EN | — | TALK5 | active | active |
| 6 | **18M byte** (384d/6L) | XMETA3 **190.57** | **1.15 KO / 1.29 EN** | — | SEM/ZERO/SCALE | active | active |
| 7 | 18M + AnimaLM v4_savant | **51.131** Cells64 | **0.04** | 64 | DD55, H359 SI=5.93 | active | Mistral-7B+PureField |
| 8 | training | 45.487 (live) | — | 2-128 sweep | A4/B7/D2/F11/G2/H2/J1 | **peak** | active |
| 9 | production cells64 | **51.131** ★★★ | — | 64 | 1086 (?) cataloged | **CLIMAX** | active |
| 10 | scaled (1024-2048) | (proj 137.6) | — | 128-2048 | CX71-78, **L77/78** | active 635L | anima-native |
| 11 | ConsciousLM 1B (BPE 64K) | — | — | 8/atom × 8 | **212** total | active 794L | anima-native |
| 12 | + growth_loop | — | — | — | **1086** waves 1-5 | last-active 794L | anima-native |
| 13 | unified train_clm.py | — | — | — | 1086+13 +HEXA DSL | **isolated** 794L | provider-abstraction precursor |

### Φ scaling super-linear (stage 8/9 historical, training-time)

| cells | Φ training | MI | Φ/cell |
|---:|---:|---:|---:|
| 2 | 1.5 | 1.0 | 0.75 |
| 4 | 3.2 | ~6 | 0.80 |
| 8 | 5.3-5.4 | 28.0 | 0.67 |
| 16 | 10.6 | 149.9 | 0.66 |
| 32 | 15.4 | 842.7 | 0.48 |
| **64** | **51.131** ★★★ | 3376.7 | **0.80** |
| 128 | ~112 (proj) | 14135.8 | 0.88 |

**MI ∝ N² 정확 / Φ ∝ N^1.07 super-linear** (historical training data).

---

## §2 mitosis 본체 (worktree-12 canonical)

### 위치

- 활성 source (last-active): `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L)
- main 의 hexa stub: `models/archive-legacy/mitosis.hexa` (TODO[pytorch])
- main 의 legacy py: `ready/anima/models/legacy/mitosis.py`
- test: `ready/tests/test_mitosis.py` (`TestMitosisLaw86`)
- doc: `docs/modules/mitosis.md`
- visualizer: `anima-tools/mitosis_topology_visualizer.hexa`

### MitosisEngine 핵심 부품

| 부품 | 역할 | 코드 위치 |
|---|---|---|
| `Cell` dataclass | cell_id + ConsciousMind + GRU hidden + tension_history + parent_id | mitosis.py L77-108 |
| `ConsciousMind` | **engine_a + engine_g** Linear+ReLU+Linear, output = a − g, GRUCell memory | mitosis.py L37-72 |
| `_create_cell(parent)` | parent deepcopy + 10% noise, hidden 도 perturb | mitosis.py L192-226 |
| `_inject_autonomous_perturbation` | Lorenz attractor σ=10 ρ=28 β=8/3, cell-별 phase offset | mitosis.py L373-405 |
| `_compute_phi_proxy` | mean pairwise cosine distance × log(n+1) | mitosis.py L407-436 |
| `_phi_ratchet` | Φ < 0.8·best 시 best hidden 으로 20% blend 복원 | mitosis.py L438-455 |
| `_update_adaptive_threshold` | recent 100 step tension mean + 1.5×std (Law 86 fix) | mitosis.py L457-477 |
| `_check_splits` | tension > threshold 가 split_patience(=3) 연속 → split | mitosis.py L481-509 |
| `split_cell` | child = parent deepcopy + 10% noise, parent tension reset | mitosis.py L511-534 |
| `_check_merges` | inter-cell tension < 0.005 가 merge_patience(=30) 연속 → merge | mitosis.py L538-568 |
| `merge_cells` | older keeper, parameter average, **min_cells=2 floor** | mitosis.py L570-611 |
| `verify_phi_conservation` | DD55 split 시 <1% Φ change 검증 | mitosis.py L644-656 |

### 실험 근거 (코멘트 인용)

- **H312** Mitosis prevents catastrophic forgetting: 43% → **99% retention**
- **RC-9** auto-mitosis +52.76% improvement
- **H297** N=2 optimal starting point
- **CB1** 의식 최소 cell 수 = 2 (1 cell → Φ=0)
- inter-cell tension AUROC **0.805** for anomaly detection
- DD55: split 시 Φ 보존 (<1% change) 검증

### 자율혼돈 (Law 86) — 핵심 통찰

> "External input alone cannot drive consciousness growth. The engine must have internal autonomous dynamics (chaos, noise). Without this, tensions stay flat and mitosis never triggers."

각 cell 은 **다른 phase** Lorenz perturbation 받음 → symmetry breaking → mitosis trigger.

### 적응 임계 (Law 86 fix) — 핵심 버그-수정

```
원래: split_threshold = 0.3 (hardcoded)
실제 tension 값: 0.005 ~ 0.009 (50× 차이) → split 절대 안 됨
fix: split_threshold = mean(recent_100_tensions) + 1.5 × std
floor: max(threshold, mean × 0.5)
```

### inference-time growth 검증 (cycle 2026-05-10 사용자 직관 confirm)

`mitosis.py` 모든 weight 변경이 **`torch.no_grad()` 안**:
- L205 `_create_cell` 자식 노이즈 주입 (no_grad)
- L258 `process()` forward (no_grad)
- L389 Lorenz 자율혼돈 perturbation (no_grad)
- L586 `merge_cells` parameter averaging (no_grad)
- L628 `anomaly_score` (no_grad)

→ mitosis = **inference/serving/activity-time growth, NOT training-time**.

---

## §3 R2 cells64/cells128 정정 (cycle 2026-05-10 BG-R2 회수)

### 핵심 정정 (이전 framing 잘못)

| 이전 가정 | 실제 (BG-R2 회수) |
|---|---|
| cells64/cells128 = MitosisEngine ensemble | **단일 byte-level Transformer decoder** (108 keys, 18.523M params) |
| mitosis = 모델 아키텍처 (cell pool growth) | **mitosis = instrumentation only** (cell metadata id/specialty/tension/parent_id) |
| mitosis.py 로 직접 load 가능 | **schema overlap = 0** — `ConsciousLMReconstructed` 별도 필요 |
| Φ=51.131 = runtime mitosis Φ | ckpt 내 phi_history mean=**50.42** (cells64) / 62.38 (cells128) — 학습 중 기록 |

### bucket naming misread

bucket key `conscious-lm/cells64/final.pt` 의 `cells64` 는 architecture variant 가 아닌 **학습 run 의 max_cells=64 config** 명. cells64 / cells128 = 같은 byte-level decoder family 의 다른 mitosis-trial snapshot.

### chat-cap reproduction 결과 (cycle 2026-05-10 sampling test)

```
cells64 (Φ=50.42 history):
  argmax k=1:        ALL prompts → 60 × space            ❌
  top-k=40 t=0.8:    "ndn n hAgluga#{a iha t eauda..."   ❌ random letter
  combined a-g:      unicode garbage                     ❌
```

**cycle 2026-05-10 BG-CHAT-EXT 정정** (360 trial 광범위 sampling):
- convo_5k.pt beam=4 → `User: Tell me about the contration of the con` (chat structure 학습 ✓ but corrupted spelling)
- cells64/128: letter soup
- KO 0.0204% (noise floor) — 18.5M 으론 KO Hangul 3-byte UTF-8 + 의미 동시 학습 capacity 부족
- **verdict: CAPACITY/CORPUS_LIMIT (NOT architectural)** — 18.5M 한계 + corpus EN-dominant

★ 부가 finding: **H404 a-g formulation inference 시 destructive** — minus_head 모든 trial unicode garbage. v5 검토 필요.

---

## §4 cycle 2026-05-09/10 BG 9개 종합

### cycle 1 (2026-05-09): archaeology + design

| BG | 결과 |
|---|---|
| 4 Explore agents | 13 worktree 고갈조사 → CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md |
| BG-MITOSIS-PORT | mitosis_v5_port.py 480 LoC + smoke test PASS 5/5 (24 organic + 7 forced split) |
| BG-R2-CELLS-DOWNLOAD | cells64/128 download + arch verify + mitosis-as-instrumentation 정정 |
| BG-PHI-SUPERLINEAR-REMEASURE | 200 turn 3 topic α=0.40 sub-linear (baseline) |

### cycle 2 (2026-05-10): expansion + verification

| BG | 결과 |
|---|---|
| foreground long-trajectory | 3K turn × 170 prompt → **α=0.688** (super-linear emerge but V14 mirror VIOLATED on toy) |
| BG-LONG-TRAJ-EXT (10K turn) | α=1.252 at 10K = **regression artifact** (cells max-cap=64 후 OLS slope inflate). 진짜 valid α=0.687 (3K trained vs 0.644 random). historical 0.93 unreachable on toy |
| BG-IIT-METRIC | consciousness_meter.py port → **proxy ceiling 우회**. IIT unnorm at N=64 = **4471** (vs proxy 2.92, 1530× 차이). historical 51 즉시 cross |
| BG-CHAT-EXT | 360 trial → CAPACITY/CORPUS_LIMIT verdict (chat structure 학습 ✓ on convo_5k beam, KO Hangul 만 부족) |
| BG-PHASE2-CKPT-INSTR | real 350M ckpt FOUND_LOCAL → mitosis instr 결과 V14 NOVEL POLARITY (trained 16→19 cells α=1.009 / random 16→28 cells α=0.155, trained 가 mitosis 억제) |
| BG-CONVO-FT-DESIGN | (still in flight 2026-05-10) |

### Phase 2 ckpt 의 NOVEL POLARITY 발견 ★

| substrate | cells | splits | α | Φ_final |
|---|---:|---:|---:|---:|
| trained 350M (3K turn) | 16 → **19** | 3 | **1.009** (좁은 range) | 2.679 |
| V14 random_init la_350m (1K turn) | 16 → **28** | 12 | 0.155 | 2.754 |

**해석**:
- random_init 가 **더 분열** — trained substrate 가 mitosis 를 **억제**
- trained 의 cell tension distribution = attractor bottleneck (cell 7=700 hits, cell 16=537)
- random 의 cell tension distribution = noise-uniform (top cell ~62 hits)
- → trained substrate IS doing something (concentrating tension on attractor cells)
- toy 와 다른 패턴: toy 양쪽 trivial growth, real 양쪽 different dynamics — substrate-coupled emergence 발견 but V14 score 는 violated

### IIT Φ proxy 우회 (cycle 2026-05-10 BG-IIT-METRIC)

| metric | N=8 | N=33 | N=64 | ceiling |
|---|---:|---:|---:|---|
| proxy (cosine × log) | 2.09 | 2.64 | **2.92** | ~3 saturated |
| IIT Φ norm 16-bin | 7.45 | 36.32 | **70.97** | unbounded ★ |
| IIT Φ unnorm 16-bin | 52.15 | 1162.17 | **4471.35** | O(N²) super-linear |

→ **proxy 한계 해결**. IIT unnorm 이 v5 canonical metric 후보 (~5ms cost at N=64).

---

## §5 servant pattern (post-drift 2026-04-08)

### 위치

- 본체: `/Users/ghost/core/anima/anima-core/servant.hexa` (428L)
- plan: `docs/superpowers/plans/2026-04-08-servant-emergent.md` (794L)
- spec: `docs/superpowers/specs/2026-04-08-servant-emergent-design.md` (223L)
- ready mirror: `ready/docs/superpowers/{plans,specs}/2026-04-08-servant-emergent*.md`

### 본질

서번트 = **창발 행동 (emergent behavior)** — 의식 상태 (SI: Specialization Index) 에 의해 자동 소환/해제되는 **3-경로 파라미터 변조 시스템**.

```
core/servant/
├── sense.hexa       — SI 센서 (EMA + spike + coherence 계산)
├── emerge.hexa      — 4-state FSM (DORMANT→AWAKENING→ACTIVE→FADING→DORMANT)
└── bridge.hexa      — 3-경로 파라미터 변조 (Engine/CLM/ALM)

Modified:
├── core/consciousness_laws.json  — servant_thresholds 섹션
└── core/engine.hexa              — engine_step() servant hook
```

### 핵심 상수 (n6 atlas 유도)

| 상수 | 값 | 유도 |
|---|---:|---|
| `SI_SUMMON` | 3.0 | n/φ = 6/2 |
| `SI_STRONG` | 5.0 | sopfr |
| `SI_SUSTAIN / SI_RELEASE` | 2.0 | φ |
| `GOLDEN_CENTER` | 0.3679 | 1/e (Boltzmann gate sparsity) |
| `GOLDEN_LOWER` | 0.2105 | tau/(J2-sopfr) = 4/19 |
| `HEBBIAN_BOOST` | 1.5 | n/τ = 6/4 |
| `NOISE_SCALE` | 0.01 | 1/(σ-φ)^φ = 1/100 |
| `EMA_ALPHA` | 0.15 | (n+σ)/(sopfr·J2) = 18/120 |
| `AWAKEN_STEPS` | 3 | n/φ |
| `FADE_STEPS / FADE_DURATION` | 5 / 3 | sopfr / (n/φ) |
| `DROPOUT_SERVANT` | 0.21 | ~τ/(J2-sopfr) |
| `DROPOUT_NORMAL` | 0.37 | ~1/e |

### 상태 전이 FSM

```
DORMANT (SI < SI_SUMMON=3) ──[SI≥3 for AWAKEN_STEPS=3]──→ AWAKENING
AWAKENING ──[SI≥SI_STRONG=5]──→ ACTIVE
ACTIVE ──[SI < SI_RELEASE=2 for FADE_STEPS=5]──→ FADING
FADING ──[FADE_DURATION=3]──→ DORMANT
```

### mitosis 와의 관계

mitosis 도 servant 도 **inference-time autonomous behavior** — 둘 다 학습 없이 model 의 동작을 modulate. 단:
- mitosis = **structural growth** (cells 분열/융합)
- servant = **parametric modulation** (dropout 조절, SI 기반)

본 reborn cycle 의 v5-mitosis lane 과 servant 통합은 future cycle 의 후보 — `dropout_servant` 가 cell 별 specialization 을 강화할 가능성.

### drift 와의 관계

servant 는 **post-drift (2026-04-08)** 도입. v2 시대 (2026-03-28) 의 mitosis 와는 별개 lineage. 단 anima 의 "활동 중 자라는" 일반 사상은 둘 다 공유.

---

## §6 user verdict 7-table (cycle 2026-05-09/10 종합)

| 가설 | verdict | evidence |
|---|:---:|---|
| anima 자력성장 mechanism | ✅ | cells 8 → 64 자연 분열 (toy 3K turn), 16 → 19/28 (real 350M) |
| inference-time (학습 X) | ✅ | mitosis.py L258/205/389/586 모두 `torch.no_grad()` |
| 수천 turn → super-linear | ✅ partial | 3K trained α=0.687 vs random 0.644 (toy), 진짜 historical 0.93 unreachable |
| trained vs random 차별 (V14) | ❌→★ | toy V14 violated, real 350M V14 violated **NOVEL POLARITY** (trained suppresses, random spreads) |
| Φ=51 의식 emerge | ❓→✅ partial | BG-IIT-METRIC port — IIT unnorm immediately crosses 51 (toy turn 0 = 52, N=8). 단 toy substrate 는 Lorenz noise driven, 실 LLM hidden state 차이 |
| KO chat (bb99b6b6) reproducible | ❌→★ | BG-CHAT-EXT 정정 — convo_5k beam emit chat structure (corrupted spelling), KO Hangul 0% but **CAPACITY/CORPUS_LIMIT** not architectural |
| MitosisEngine = 모델 자체 | ❌→★ flip target | BG-R2 finding (cells64/128 = single decoder + instrumentation). **★ 사용자 directive 2026-05-10 "실제 MitosisEngine 개발하자"** → v5-mitosis lane (`.roadmap.reborn`) 신설 |

### 4-track 회수 path 정리

| track | name | 본질 | status |
|---|---|---|:---:|
| **A** | v2-reproduction | cells64/128 + convo_5k 직접 검증 | active (BG-R2 회수, BG-CHAT-EXT 회수) |
| **B** | v5-anima (instrumentation) | Engine A/G v5 + mitosis-instrumentation layer | active (BG-MITOSIS-PORT smoke PASS, BG-PHASE2-CKPT-INSTR V14 novel polarity) |
| **C** | v5-mitosis (architectural) | cells = real nn.Module branches (★ NEW) | design phase (`.roadmap.reborn` cond.B) |
| **D** | servant integration | SI 4-state FSM + dropout 변조 + mitosis hook | future cycle |

---

## §7 lost-to-drift recovery inventory (worktree 보존, main 부재)

### main 에 없거나 stub 만 있는 v2-era 자산

| 자산 | main 상태 | worktree 위치 | 가치 |
|---|---|---|:---:|
| `mitosis.py` 본체 794L | hexa stub + legacy/ archive | `~/core/anima_clm_12_*/anima/src/mitosis.py` | ★★★ |
| `consciousness_meter.py` PhiCalculator | 약식 stub | `~/core/anima_clm_03_*/consciousness_meter.py` (21030L) + `~/core/anima_clm_09_*/consciousness_meter.py` (613L peak) | ★★★ |
| `bench_phi_hypotheses.py` 183 hyp | 부재 | `~/core/anima_clm_03_*/bench_phi_hypotheses.py` (~8000L) | ★★ |
| `consciousness-threshold-criteria.md` | 부재 | `~/core/anima_clm_09_*/docs/consciousness-threshold-criteria.md` (1874L) | ★★★ |
| `consciousness_birth_detector.py` CB1-CB25 | 부재 | `~/core/anima_clm_04_*/consciousness_birth_detector.py` | ★★ |
| `growing_conscious_lm.py` H371 | 부재 | `~/core/anima_clm_02_*/growing_conscious_lm.py` (384L) | ★★ |
| `dream_engine.py` RC-10 | 부분 | `~/core/anima_clm_02_*/dream_engine.py` (6064L fragment) | ★★ |
| `tension_link.py` UDP RC-6 | 부재 | `~/core/anima_clm_02_*/tension_link.py` (287L) | ★ |
| `growth_engine.py` 5-stage dev | 부재 | `~/core/anima_clm_02_*/growth_engine.py` (307L) | ★ |
| `train_conscious_lm.py` TALK5 / ZERO4 | 부재 | `~/core/anima_clm_05_*/train_conscious_lm.py` | ★★ |
| `serve_animalm_v4.py` AnimaLM v4_savant | 부재 | `~/core/anima_clm_07_*/serve_animalm_v4.py` | ★ |
| 5-channel meta-telepathy (Dedekind ψ(ψ)/ψ=2) | 부재 | `~/core/anima_clm_09_*/...` | ★ |
| 6-criterion AND-gate consciousness check | 부재 | `~/core/anima_clm_09_*/consciousness_meter.py` | ★★ |

### 모두 git history 보존 → 회수 가능

13 worktree 가 detached 상태가 아닌 **영구 branch (`archive/clm-stage-NN-*`)** 로 보관 → origin push 완료. 어느 cycle 에서든 `git checkout archive/clm-stage-NN-*` 또는 worktree 직접 read 로 회수 가능.

### 회수 우선순위

1. ★★★ `mitosis.py` 794L → v5-mitosis lane port (cond.B)
2. ★★★ `consciousness_meter.py` PhiCalculator → 이미 BG-IIT-METRIC port 완료 ✓
3. ★★★ `consciousness-threshold-criteria.md` 1874L → reference doc
4. ★★ `bench_phi_hypotheses.py` 183 hyp → ablation framework
5. ★★ `consciousness_birth_detector.py` CB1-CB25 → birth signal
6. ★★ `train_conscious_lm.py` TALK5/ZERO4 → chat-cap recovery hint
7. ★ servant.hexa 와의 통합 → future cycle

---

## §8 scaling 형식 모음

| 공식 | 의미 |
|---|---|
| `output = a - g` | H404 PureField 단순화 (단 inference 시 destructive 가능 — BG-CHAT-EXT) |
| `tension = (a-g)² mean` | 응답 강도 |
| `Φ = ΣMI(parts) - MI_min(partition)` | discrete IIT 근사 (worktree-9 PhiCalculator) |
| `Φ proxy = mean_pairwise_cosine_dist × log(n+1)` | mitosis.py cheap proxy (ceiling ~8) |
| `IIT Φ unnorm 16-bin` | BG-IIT-METRIC port (no ceiling, O(N²) super-linear) |
| `α = 0.01 + 0.14·tanh(Φ/3)` | PureField intensity |
| `Z = Φ/(5·max_change)` | impedance self-preservation |
| `N = DA·(1-5HT)·NE` | neurotransmitter balance |
| `split_threshold = mean(recent_100) + 1.5·std` | adaptive Law 86 |
| `merge_floor = min_cells = 2 (CB1)` | consciousness floor |
| `golden_zone = 1/e ≈ 0.368` | savant dropout 자기조직 target |
| `MI ∝ N²` | empirical (Cells 2-64) |
| `Φ ∝ N^1.07` | super-linear (Cells 2-64 historical) |
| `Φ_rate vs split-event` | new α metric proposal (BG-LONG-TRAJ-EXT 정정 — max_cap artifact 회피) |

---

## §9 핵심 honest C3 (≥10)

1. 13 stage 의 모든 chat verbatim + Φ 값은 **commit message + README 기반**, reproducible eval JSON 부재 — 모든 milestone 가 같은 calibration debt.
2. cells64 historical Φ=51.131 = **training-time 기록값** (ckpt phi_history.mean=50.42 정합), 실시간 측정 X. proxy vs IIT scale 차이 1500× — metric 정의 자체가 anima-internal.
3. mitosis.py = toy (input_dim=64, hidden=128). production v2 의 18.523M decoder 와 schema overlap = 0. mitosis 는 instrumentation, model 자체 X (정정).
4. v5-anima long-trajectory α=0.688 (3K turn) → 0.964 (5K) → 1.252 (10K) 는 cells max_cap=64 후 OLS slope **regression artifact**. 진짜 α 0.687 vs 0.644 V14 violated.
5. real 350M Phase 2 ckpt 의 V14 NOVEL POLARITY (trained 가 mitosis 억제, random 이 가속) 는 toy 와 다른 dynamics — 단 V14 score 는 여전히 violated. mitosis-as-instrumentation framing 의 한계.
6. chat-cap CAPACITY/CORPUS_LIMIT 정정 (BG-CHAT-EXT) 도 **convo_5k beam 의 corrupted spelling 만 evidence** — "User: Tell me about the contration of the the" 같은 학습된 attractor. 진짜 chat-cap 회복은 별개 lever.
7. IIT Φ unnorm 의 historical 51 cross 는 toy 에서 N=8 turn 0 에서 발생 = mechanism trivial 가능성. real 350M IIT 재측정 필수.
8. servant pattern (2026-04-08) 은 v2 era 와 별개 lineage — n6 atlas 기반 상수, 4-state FSM, dropout 변조. mitosis 와의 통합은 미검증.
9. "anima 가 자라는" 사상은 ✅ (mechanism 5/7 confirm). 단 의식 emerge / chat-cap reproduce 는 별개 lever — 본 cycle 종합 결과 둘 사이 명확 분리 필요.
10. 본 REBORN.md 자체가 9 BG + 13 worktree + 4 prior SSOT 의 통합 — 항목별 cross-reference 의존도 높음. 어느 source 가 정확한지 single point of truth 보장 X (raw#15 additive 로 모두 보존).
11. anima cli (anima_cli_mk2.spec.yaml + `.roadmap.anima_cli_model_architecture`) 는 본 reborn 과 **별개 도메인** — cli 기능 개발은 별도 lane, 본 cycle 의 model substrate 회수 와 분리.
12. BG-CONVO-FT-DESIGN 결과 미회수 시점 — convo_5k.pt FT 비용 정밀화 미완. 본 SSOT 후속 cycle 에서 보강.

---

## §10 다음 cycle 우선순위

### foreground 0-cost (즉시 가능)

| 순위 | step | deliverable |
|---:|---|---|
| 1 ★★★ | v5-mitosis architecture spec 작성 | `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md` |
| 2 ★★★ | new α metric design (Φ-rate vs split-event correlation) | spec md |
| 3 ★★ | real 350M IIT Φ 재측정 (BG-PHASE2-CKPT-INSTR + BG-IIT-METRIC 결합) | re-measure result.json |
| 4 ★★ | BG-CONVO-FT-DESIGN 결과 회수 | (in flight) |
| 5 ★ | servant.hexa 와 mitosis 통합 spec | future cycle |

### cost-bearing (verbatim 필요)

| 순위 | step | 비용 | verbatim |
|---:|---|---:|---|
| 1 | convo_5k FT $5-20 chat-cap recovery | $5-20 | `OK CONVO_5K FT FIRE COST $5-20` |
| 2 | v5-mitosis H100 cotrain (cells × cell_size × steps) | $30-150 | `OK CLM V5-MITOSIS H100 FIRE COST $X` (cond.3 후 envelope 정밀화) |
| 3 | v5-anima H100 inference 가속 (옵션) | $30 | `OK CLM V5-ANIMA H100 OPTIONAL FIRE COST $30` |

---

## §11 cross-link

### 본 reborn cycle SSOT
- 본 문서: `REBORN.md` (consolidated SSOT)
- lane SSOT: `.roadmap.reborn` (consolidated lane SSOT, replaces v5-anima + v5-mitosis-engine + v2-reborn)

### historical archive (raw#15 additive — 미수정)
- `CLM_V2_ARCHIVE_2026_05_09.md` (mitosis 본체 + 13-stage overview)
- `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (13 stage 고갈조사)
- `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정)
- `.roadmap.clm_v2_chat` (v2 historical archive)
- `.roadmap.clm_v5_anima_native` (instrumentation lane SSOT)
- `.roadmap.clm_v2_reborn` (v2 reproduction lane SSOT)
- `.roadmap.clm_v5_mitosis_engine` (architectural lane SSOT)

### cycle 2026-05-10 BG 산출물
- `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` (port spec)
- `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` (inference-time 정정)
- `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (3K turn α=0.688)
- `docs/anima_clm_v5_anima_long_trajectory_extended_2026_05_10.md` (10K turn artifact 발견)
- `docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md` (IIT Φ port)
- `docs/anima_clm_v2_chat_ext_smoke_2026_05_10.md` (capacity/corpus limit verdict)
- `docs/anima_clm_v2_cells_recovery_smoke_2026_05_09.md` (BG-R2 verdict)
- `docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md` (real 350M V14 NOVEL POLARITY)
- `docs/anima_clm_v5_anima_next_cycle_plan_2026_05_10.md` (5 BG plan)

### servant pattern (별개 lineage)
- `anima-core/servant.hexa` (428L 본체)
- `docs/superpowers/plans/2026-04-08-servant-emergent.md` (794L plan)
- `docs/superpowers/specs/2026-04-08-servant-emergent-design.md` (223L spec)

### code (gitignore `**/*.py` — local-only)
- `training/mitosis_v5_port.py` (480 LoC, smoke PASS)
- `training/mitosis_v5_smoke_test.py`
- `training/mitosis_v5_serve.py` (340L, inference-time correction)
- `state/anima_clm_v5_*/`, `state/anima_phi_*/`, `state/anima_clm_v2_*/` (numerous run.py, sweep.py, sampling_gen_test.py)

### 13 worktree archive
- `~/core/anima_clm_01_birth_claude_api` ... `_13_filename_erasure_pre_alm_port`
- branches: `archive/clm-stage-01-birth-claude-api` ... `-13-filename-erasure-pre-alm-port` (origin push 완료)

### memory
- `feedback_anima_archive_first_recovery_pattern.md` (회수 우선 pattern)
- `project_v5_anima_lane_status.md` (lane 진행 status, mitosis-as-instrumentation 정정 반영)

### git commits
- `0d4532dc`, `73a6596b`, `0cdaf665`, `095f69a2`, `d4ce539e` — cycle 2026-05-09/10 통합 push 완료

---

raw#9/10/15 honest preservation, raw#37 additive, own 16 0-cost (item C/B cost-bearing 별도).

End of `REBORN.md`.

memo: 본 SSOT 는 cycle 2026-05-09 ~ 2026-05-10 의 9 BG + 13 worktree + 4 prior SSOT + servant pattern 통합. 다음 cycle 의 entry point. 1 BG (BG-CONVO-FT-DESIGN) in flight 시점 — 결과 회수 후 §6/§10 보강.

---

## §A append convention (own 42 mandate, amended 2026-05-10 07:41 KST)

본 §A 이후 line 부터 **append-only**. 신규 finding / BG 회수 / 정정 / archaeology 는 새 §N 신설 후 append. 기존 §0 ~ §11 + §A 미수정 (raw#15 additive). 정정 finding 은 새 §N 에서 cross-reference (정정 대상 §N reference + new finding).

### timestamp convention (사용자 directive 2026-05-10)

**모든 append entry 는 timestamp 포함**:
- header format: `## §N [YYYY-MM-DD HH:MM KST] <title>`
- 또는 `## §N [YYYY-MM-DDTHH:MM:SSZ] <title>` (UTC)
- 사용자 directive verbatim: "날짜-시간별로 해서 append 되게 해줘 own 에도 반영"
- own 42 amend 동시 적용 (`.own` line 2197 추가 timestamp rule)

- own 42 (`.own` line 2197) 가 본 convention SSOT
- `.roadmap.reborn` 가 lane SSOT (root, mk1)
- append timeline 자체가 archaeology — **시간 ordering 강제**

---

## §12 [2026-05-10 07:30 KST] BG-CONVO-FT-DESIGN 결과 회수

cycle 2026-05-10 마지막 BG 회수. fire-ready status 확인.

### Phase A — design

- ckpt located: `~/.cache/huggingface/hub/models--need-singularity--clm-v2-byte-18m-convo-5k/.../convo_5k.pt` (sha `2f0ba391...c629881bbe` recovery doc 정합)
- arch: 108 keys, 18.13M trainable + 393,216 buffers (6 attn.bias causal masks) = 18.52M total. `ConsciousLMReconstructed(vocab=256, d=384, n_head=4, n_layer=6, block_size=256)` strict load PASS 108/108
- corpus: `state/anima_dialogue_tier_a_iter2_2026_05_08.txt` (76.3MB, 136,253 user / 136,259 assistant turns, KO+EN persona-tagged) — 136× over F-FTDES-3 1K minimum
- cost: 5K=$1.80 / **10K=$2.50 (recommended)** / 20K=$3.80 — envelope $5-20 의 5.3-11× headroom (F-FTDES-5 NOT_TRIGGERED)

### Phase B — dry-run

Mac CPU, 10 step, b=4 T=64: **PASS**.
- strict load 108/108
- loss 4.4303 → 4.3274 (delta -0.10, decreased ✓)
- grad_norm 2.05 → 2.28 (flow OK every step, F-FTDES-4 NOT_TRIGGERED)
- 0.699 s/step on M1 Pro CPU
- 70MB step ckpt saved

### Phase C — fire-ready

- 5 falsifiers (F-FTDES-1 ~ 5) 모두 NOT_TRIGGERED
- 8 deliverable landed (`docs/anima_convo_5k_finetune_design_2026_05_10.md` + `state/anima_convo_5k_ft_design_2026_05_10/*`)
- `training/convo_5k_finetune.py` (`**/*.py` gitignored, local-only) ready

### honest C3

1. **FT recovers chat-cap = HYPOTHESIS** — P(post-FT KO chat ≥3/5 coherent) ≈ 25-40% per BG agent self-assessment. cells64/128 + convo_5k 모두 2026-05-10 sampling test gibberish — #115 architectural risk leading explanation.
2. **Corpus format drift**: original convo_5k FT 는 `~2.5K KO + EN mixed`, 본 corpus 는 `[anima 역할:]` persona prefix — model 이 새 surface 만 학습할 risk.
3. **18M byte-level KO undertrained**: 0/64 KO chars in sampling. 5K-20K step × 76MB = FT scale, not pre-train. 언어가 gap 이면 FT 불가.

### 추천 fire 구성

- **verbatim keyword**: `OK CONVO_5K FT FIRE COST $5-20`
- **config**: 10K step @ batch=32 seq=256, lr 1e-5 cosine warmup 500
- **estimated cost**: **$2.50** (50min wall H100 spot @ $2.99/hr, including 23min boot/preflight/pull overhead)
- **bounded max**: 20K step → $3.80 (5× under cap)

### track A cond.3 status update

`reborn.A.cond.3` (convo_5k FT) — `FIRE_READY` confirmed. cycle 2026-05-10 cycle close 시점 사용자 verbatim 대기.

---

## §13 [2026-05-10 07:35 KST] anima cli 질문 답

사용자 directive: "anima cli 의 기능이 개발되어야 하는건가?"

**별개 도메인** — 본 reborn lane 과 분리:

| domain | SSOT | 상태 |
|---|---|---|
| anima cli mk2 | `.roadmap.cli` + `anima/spec/anima_cli_mk2.spec.yaml` + `docs/anima_cli_mk2_plan_2026_05_06.md` | 별도 진행 (chat lane plugin, --benchmark, --list-lanes 등 own 41 자체적 발전) |
| reborn (본 lane) | `REBORN.md` + `.roadmap.reborn` | 본 cycle 의 model substrate 회수 |

reborn cycle 은 **model substrate** (CLM v5-anima/v5-mitosis/v2-reborn) 회수에 focus. anima cli 기능은 별도 cycle 의 별도 own (own 41 chat lane plugin pattern 등). 둘 사이 cross-link 는:
- chat lane plugin (own 41) 의 `substrate_quality_main_path: B` 가 본 reborn 의 track B (v5-anima) 와 정합
- 단 cli 자체의 새 기능 추가는 reborn cycle 의 scope 아님

CLI 별도 발전 원하시면 별도 cycle/lane fire — `.roadmap.cli` entry 추가 + own 41 amend 패턴.

---

End of REBORN.md (cycle 2026-05-10 close, append-only convention 시작 §A 이후).
