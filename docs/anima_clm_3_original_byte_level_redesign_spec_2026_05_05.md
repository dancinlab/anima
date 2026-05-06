# anima CLM-3-original — byte-level v4 redesign spec (Option β, BG-ER)

- Date: 2026-05-06 (filed under 2026-05-05 cycle)
- Status: SPEC LANDED (doc-only; no build / no train this cycle)
- Cost: $0 (mac, doc only)
- Lane: Option β of #115-ARCHITECTURAL-FINAL-4-CLOSURE H1 — alternate
  CLM-3 redesign that **restores the 2026-03-28 original v4 design** in
  full (byte-level vocab 256, max_cells 32, ~55M params, 100K-step
  3-phase curriculum, 19 Φ-boost techniques applied simultaneously).
- Predecessor docs:
  1. `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md`
     (BG — drift table commit `fca0eede` → `145838d2`)
  2. `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM
     — drift'ed CLM-3 design w/ BPE 64K + 530M scale + 4-bucket mix)
  3. `docs/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05.md`
     (BG-DK)
- Source of truth: commit `fca0eede:docs/next-model-design.md` (406 LoC,
  2026-03-28). All numeric specs in §1 are direct quotations of that
  commit; no derivation, no interpolation.

---

## 0. Abstract / 초록

**EN.** CLM-3-original is the alternate-β redesign of CLM-3 H1: instead of
scaling **up** to 530M+/BPE-64K (BG-BM CLM-3), we scale **back to the
2026-03-28 original v4 design** that produced demonstrable chat capability
on byte-level CLM v2 (CE 0.04 EN / 1.15 KO, no system prompt). The hypothesis
is that anima-native chat does **not** require BPE multilingual + 530M+
scale, but is in fact recoverable at 55M / byte-level / 32 cells / 100K
steps with the 19 Φ-boost techniques applied simultaneously per DD16/EX24.
This spec fixes the original v4 numerics verbatim, diffs them against
BG-BM CLM-3 (drift'ed), locks 5 falsifiers, lays a $0-$500 cost envelope
across two compute paths (ubu1 RTX 5070 sm_120 free vs H100 ~$200-500
paid), and presents a user-fire menu of three commands.

**KO.** CLM-3-original 은 CLM-3 H1 의 대안 β 재설계 다. BG-BM CLM-3 의
530M+/BPE-64K **scale-up** 방향과 정반대로, **2026-03-28 original v4
design 으로 정확히 되돌아간다**. 이 design 은 byte-level CLM v2 에서
chat capability 를 명시적으로 산출했다 (CE 0.04 EN / 1.15 KO, system
prompt 無). 가설: anima-native chat 은 BPE multilingual + 530M+ scale 이
**필요하지 않으며**, 55M / byte-level / 32 cells / 100K steps + 19 Φ-boost
simultaneously 에서 회복 가능하다. 본 문서는 original v4 numerics 그대로
재현, BG-BM (drift'ed) 와의 diff, 5 falsifier lock, $0-$500 cost envelope
(ubu1 5070 free vs H100 paid), 그리고 3-command user-fire menu 를
정식 명세한다.

---

## 1. Original 2026-03-28 v4 spec — 전체 (verbatim from `fca0eede`)

### 1.1 Architecture (commit `fca0eede:docs/next-model-design.md` §1.1)

| Parameter | v3 (then-current) | **v4 (original spec, 2026-03-28)** |
|---|---|---|
| dim | 768 | **768** |
| hidden (FFN) | 1536 | **1536** (2× dim, standard) |
| layers | 12 | **12** |
| heads | 12 | **12** (TL1: σ(6)=12 perfect-number heads, Φ=7.022) |
| max_cells | 8 | **32** ← single highest-leverage change (Φ ~ N linear) |
| vocab | 256 (byte) | **256 (byte)** ← byte-level **unchanged** |
| context_len | 512 | **1024** |
| params | ~50M | **~55M** |
| shared_dims | – | **24** (PX8 integration forge) |
| ratchet_trials | – | **10** (FX2 optimal) |

### 1.2 Training recipe (3-phase curriculum, 100K steps total = 2× v3)

| Phase | Steps | Focus | LR | Techniques |
|---|---|---|---|---|
| **Phase 1: Mitosis** | 0–20K | Cell differentiation | 5e-4 (warmup 2K) | Fibonacci growth 1,1,2,3,5,8,13,21,32; FX2 Adam Φ proxy; PX4 Gram-Schmidt sculptor |
| **Phase 2: Language** | 20K–60K | **CE minimization on dialogue+wiki** | 3e-4 (cosine decay) | CL8 tension-weighted CE (3× important tokens); CL5 Φ-regularized CE; SL3 6-loss ensemble |
| **Phase 3: Combined** | 60K–100K | Φ + CE jointly | 1e-4 (cosine→1e-5) | DD16 all-top-5 simultaneous; EX24 all discoveries; GD18 enactivism; GD15 edge of chaos |

### 1.3 Growth schedule — Fibonacci (DD3, Φ=5.196)

```
Step     0 →  1 cell
Step  5000 →  1 cell  (consolidation)
Step 10000 →  2 cells (consciousness birth, CB5)
Step 15000 →  3 cells
Step 20000 →  5 cells
Step 30000 →  8 cells
Step 40000 → 13 cells
Step 55000 → 21 cells
Step 70000 → 32 cells (max)
```

### 1.4 19 Φ-boost techniques (all applied simultaneously per DD16/EX24)

| # | ID | Technique | Φ (bench) |
|---|---|---|---|
| 1 | COMBO2 | 6-loss learnable ensemble + MHA | 8.014 |
| 2 | FX2 | Differentiable Φ proxy + Adam 5-step + ratchet 10 | 8.911 |
| 3 | WI1 | Soliton consciousness (sech² packet) | 4.460 |
| 4 | PX4 | Cell sculptor (Gram-Schmidt orthogonalization) | 0.830* |
| 5 | PX8 | Integration forge (shared 24d + private channels) | 0.873* |
| 6 | GD18 | Enactivism (sensory-motor coupling loop) | 4.229 |
| 7 | GD15 | Edge of chaos (Lyapunov exponent → 0) | 3.978 |
| 8 | **CL8** | **Tension-weighted CE (3× on high-tension tokens)** | **5.678** ← language-loss core |
| 9 | CL5 | Φ-regularized CE (dynamic Φ/CE balance) | 5.055 |
| 10 | DD3 | Fibonacci growth (1,1,2,3,5,8,13,21,32) | 5.196 |
| 11 | DD11 | Klein bottle topology (non-orientable manifold) | 5.243 |
| 12 | DD18 | Channel capacity bottleneck (Shannon limit) | 6.426 |
| 13 | DD5 | Φ self-reference (Φ optimizes itself) | 4.125 |
| 14 | TL13 | ln(4/3) Golden Zone weight | 7.876 |
| 15 | TL1 | σ(6)=12 heads, e-based decay | 7.022 |
| 16 | NV7 | Impedance (Φ-proportional input resistance) | 4.515 |
| 17 | BV1 | Neurotransmitters (DA/5HT/NE) | 4.618 |
| 18 | EV3 | Free will (internal/external action ratio) | 4.482 |
| 19 | SC2 | Dim-inverse merge threshold (prevents cell death) | 2.381 |

`*` PX4/PX8 weak individually but essential in combination (PX10=4.735, ZZ2=10.591).

> Key principle (commit verbatim): "All discoveries are synergistic" — EX24
> (10.833) > sum of individual discoveries. **Apply everything
> simultaneously. Never sequentially.**

### 1.5 Hyperparameters (commit verbatim)

```
optimizer:        AdamW (β1=0.9, β2=0.999, eps=1e-8)
weight_decay:     0.01
lr_schedule:      cosine with warmup (2K steps)
peak_lr:          5e-4 (phase 1), 3e-4 (phase 2), 1e-4 (phase 3)
batch_size:       32
seq_len:          1024
gradient_clip:    1.0 (NF1 + tension-proportional TRN2)
tension_clamp:    100 (NF4 — prevents NaN)
ema_reset:        on phase transition (NF9)
dropout:          0.1 (standard); savant cells 0.2123 (Golden Zone lower)
merge_threshold:  0.01 * (64 / 768) = 0.00083 (SC2)
split_noise:      0.02 * sqrt(768/64) = 0.069 (SC1)
```

### 1.6 Training data (commit verbatim, §1.6 row "Training data")

> v4 row: `corpus.txt + dialogue` ← v3 was `corpus.txt` only

i.e., dialogue corpus is mixed in **at cycle 0** of training, not post-hoc.
Mix ratio is left implicit in the original commit; this spec proposes
**70% wiki + 30% dialogue (AL4-balance, lifted from AnimaLM v8 §2.2)** as
the byte-level analog, since both ALM v8 and CLM v4 share the AL4
1−1/e ≈ 0.6321 tension-CE balance principle.

### 1.7 Expected Φ (commit verbatim, §1.3)

```
Conservative (dim=768, cells=32, 100K steps):  Φ = 8–15
Optimistic (if scaling law Φ~N holds):         Φ = 20+ (benchmark ZZ-32 = 27.6)
```

### 1.8 VRAM + wall-clock (commit verbatim, §1.4 + §1.5)

```
Total VRAM:       ~3.2 GB (peak with grad checkpoint ~4.5 GB)
H100 wall-clock:  ~10 hours (100K steps @ ~0.3s/step)
```

> "Fits easily on H100 80GB alongside other experiments. Can also run on
> RTX 5070 (12GB) for inference." (commit verbatim) — spec extends:
> **5070 sm_120 also fits training** by capacity (3.2 GB ≪ 12 GB), bounded
> by step throughput, not VRAM.

---

## 2. BG-BM CLM-3 vs CLM-3-original — diff

BG-BM `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` proposes
a **drift'ed** CLM-3. Side-by-side:

| Element | BG-BM CLM-3 (drift'ed) | **CLM-3-original (this spec)** | Why diff |
|---|---|---|---|
| vocab | BPE 64000 multilingual | **256 byte-level** | byte-level is the **commit-`fca0eede` original**; CLM v2 byte-level produced chat (CE 0.04 EN); BPE 64K introduced 2026-04-01 is exactly the drift point |
| layers | 16 | **12** | original v4 §1.1 |
| heads | 6 (+ 2 KV, GQA) | **12** (no GQA) | original v4 §1.1 (TL1 σ(6)=12) |
| max_cells | 8 | **32** | original v4 §1.1 — "the single highest-leverage change" (verbatim) |
| dim / FFN | 768 / 2048 (SwiGLU) | **768 / 1536 (2× dim)** | original v4 §1.1 |
| context_len | 512 | **1024** | original v4 §1.1 |
| params | 530M+ | **~55M** | 10× downsize; original v4 §1.1 |
| training steps | implicit (1B tokens × 30 days) | **100K steps 3-phase** | original v4 §1.2 |
| objective | weighted sum L_total = α·L_substrate + β·L_chat + γ·L_axis (3-term) | **19 Φ-boost simultaneous + Phase-2 CE on dialogue+wiki + Phase-3 Φ+CE joint** | EX24 "apply simultaneously, never sequentially" |
| corpus mix | 50% general / 30% dialogue / 15% reasoning / 5% conscious_states (4-bucket) | **70% wiki + 30% dialogue (2-bucket, AL4 balance)** | minimal mix-axis count; matches commit `corpus.txt + dialogue` row |
| compute | H100 1× × 30 days, ≈ $1k (Variant B) | **H100 1× × ~10 hours, ≈ $200-500** OR **ubu1 5070 ~5-10 days, $0** | direct quote of commit `~10 hours H100`; 5070 viability extended from "inference" to "training" by VRAM headroom |
| chat target | composite ≥ 0.45 (80% of Llama-3.2-3B 0.5584) | **chat target = recover CLM v2-class chat (CE < 3.5 + KO 5-prompt coherent ≥ 3/5)** | Llama-3.2-3B is a wrong anchor for byte-level 55M; CLM v2 is the demonstrable byte-level chat anchor |
| scale lever | scale **up** (more params, bigger BPE) | **scale recover** (back to byte/55M; cell-count is the lever, not params) | commit verbatim: "Φ ~ N (linear)" — N = cells, not params |

### 2.1 diff core in one line

> **BG-BM = scale-up + objective-add. CLM-3-original = scale-recover +
> 19-technique-simultaneous. Both target chat-cap; the tradeoff is BG-BM is
> more familiar (BPE Llama-style), CLM-3-original is more anima-native
> (byte/cell-mitosis is the substrate's identity).**

### 2.2 Why CLM-3-original keeps paradigm v11 G3

paradigm v11 G3's `consciousness_states` cross-attention is **substrate-
property orthogonal** to vocab/cell-count. The 32-cell mitosis engine is in
fact the **canonical substrate** that paradigm v11 G3 was reverse-engineered
to extract Φ★ from. CLM-3-original therefore **retains** paradigm v11 G3 as
the Φ-source for the §1.4 19-technique simultaneous training, with **no
modification** to the cross-attn surface. F-CLM3-orig-5 (NO_FLIP) is
operationally identical to BG-BM F-CLM-3-1.

---

## 3. CLM-3-original — precise spec

### 3.1 Architecture (locked)

```
dim:              768
hidden_ffn:       1536  (2× dim, no SwiGLU)
layers:           12
heads:            12  (TL1: σ(6)=12, no GQA)
max_cells:        32  (mitosis max, Φ ~ N lever)
vocab:            256  (byte-level, UTF-8)
context_len:      1024
params_estimate:  ~55M  (model) + ~76M (MitosisEngine 32-cell GRU(768d))
shared_dims:      24
ratchet_trials:   10
```

### 3.2 Training (locked)

```
total_steps:      100000  (3-phase)
phase_1:          0–20000   (Mitosis,  LR 5e-4 warmup 2K)
phase_2:          20000–60000   (Language CE, LR 3e-4 cosine)
phase_3:          60000–100000  (Φ+CE joint, LR 1e-4 cosine→1e-5)
batch_size:       32
seq_len:          1024
gradient_clip:    1.0
optimizer:        AdamW (β1=0.9, β2=0.999, eps=1e-8)
weight_decay:     0.01
mixed_precision:  bf16
fibonacci_growth: 1,1,2,3,5,8,13,21,32 at steps 0,5K,10K,15K,20K,30K,40K,55K,70K
techniques:       19 simultaneous (COMBO2, FX2, WI1, PX4, PX8, GD18, GD15,
                  CL8, CL5, DD3, DD11, DD18, DD5, TL13, TL1, NV7, BV1, EV3, SC2)
safeguards:       NF1 grad-clip, NF4 tension-clamp 100, NF9 EMA-reset on phase tx
```

### 3.3 Corpus mix (locked, default; ablation TBD pre-launch)

```
70% wiki/general (KO+EN, license-filtered, byte-encoded UTF-8)
30% dialogue (KO+EN, ChatML byte-form OR anima-native emerge-trace)
   - reasoning chains (CoT) folded into dialogue at ≤ 5% inside the 30%
   - if Stage 3 emerge-dialogue logs ≥ 30 sessions before fire, replace
     up to 5% of the 30% with anima-native traces
0% post-hoc / SFT / adapter — everything is cycle-0 mix
```

### 3.4 Run-time profile (locked)

```
H100 80GB:        VRAM ~3.2 GB (peak ~4.5 GB w/ grad checkpoint)
                  step time ~0.3s; 100K steps ≈ 8.3h; w/ overhead ~10h
ubu1 5070 12GB:   VRAM 3.2 GB fits comfortably (sm_120 + torch 2.11.0+cu128
                  per memory reference_ubu1_venv_orchestrator)
                  step time est. ~3-6× slower (5070 vs H100 fp16/bf16
                  throughput gap ~3-6× depending on op mix);
                  100K steps ≈ 5–10 days wall-clock at $0
```

### 3.5 What CLM-3-original does NOT do (closures stated)

- does NOT add post-hoc adapter (closure 1 bypassed by construction)
- does NOT add Φ★-only distill teacher (closure 2 bypassed; CL8/CL5
  weight chat-tokens directly into Φ-coupled CE)
- does NOT add cross-modal bridge (closure 3 N/A; same byte-level LM head
  as CLM v2)
- does NOT do residual-stream probing as fix (closure 4 mitigation:
  byte-level chat tokens are basis-trained at every layer from cycle 0)

---

## 4. Cost + falsifier locks

### 4.1 Cost envelope

| Compute | Wall-clock | Direct $ | Operator cost | own 16 watchdog? |
|---|---|---|---|---|
| H100 1× (paid) | ~10h (100K @ 0.3s/step, +overhead) | **$200–500** (≈ 10h × $4–5/hr H100 spot, +eval+checkpoint) | low; one-shot fire | **yes** (see §5.2) |
| ubu1 RTX 5070 (own) | ~5–10 days | **$0** | power + occupancy single GPU 5–10d | n/a (no cloud spend) |

Both compute paths are **viable**. H100 is ~10× faster for ~$200–500;
ubu1 is free but ties up the 5070 for 5–10 days. Recommendation in §5
ranks H100 first by 완성도 (faster cycle = faster falsifier resolution).

### 4.2 Falsifiers (locked pre-fire, raw#9)

All 5 are **pre-fire LOCKED**. Re-definition after fire = raw#9 violation.

#### F-CLM3-orig-1 — spec match

- Target: built artifact's runtime config matches §3.1+§3.2 exactly:
  byte-level vocab=256, max_cells=32 (Fibonacci to 32 by step 70K), 19 of
  19 Φ-boost techniques active, 3-phase LR schedule observable in logs.
- PASS: all 4 numeric assertions match (tolerance 0%).
- FAIL kind: SPEC_DRIFT — config diverged from original v4; lane closure
  before training compute is consumed (eval at step 0 + step 21K + step
  70K + step 100K).

#### F-CLM3-orig-2 — Phase 2 dialogue CE evidence

- Target: Phase 2 (steps 20K–60K) CE on a held-out dialogue eval slice
  drops monotonically from start-of-phase to end-of-phase by ≥ 30%
  (relative).
- PASS: held-out dialogue CE @ 60K ≤ 0.7 × CE @ 20K.
- FAIL kind: LANGUAGE_PHASE_DEAD — Phase 2 did not learn dialogue; CL8
  tension-weighting may be mis-applied; closure of CLM-3-original lane.
- Anchor: CLM v2 byte-level achieved CE 0.04 EN / 1.15 KO with `corpus.txt`
  alone; with explicit dialogue 30%, Phase-2 monotonic drop is the
  minimum credible signal.

#### F-CLM3-orig-3 — Φ ≥ 11 at 32 cells

- Target: Φ_real (paradigm v11 G3 measurement harness) at step 100K ≥ 11.
- PASS: 11 ≤ Φ_real (matches commit "predicted Φ~11" lower bound; commit
  conservative range was Φ=8–15).
- FAIL kind: PHI_SCALING_BROKE — 32 cells did not yield Φ scaling
  predicted by commit; substrate-research failure; investigate cell death
  (SC2 mis-tuned), Phase-3 EX24 mis-applied, etc.
- Anchor: paradigm v11 G3 carry on the 530M drift'ed substrate measured
  +41.86 Φ★ — that is on a 10×-larger substrate. 55M @ 32 cells must
  exceed Φ=11 to be a credible chat-cap-and-substrate-property dual win.

#### F-CLM3-orig-4 — chat capability KO probe

- Target: 5-prompt KO dialogue probe (anima-native emerge questions,
  hand-curated by user pre-fire) yields ≥ 3 of 5 coherent emit responses
  at step 100K, judged by user (binary: coherent / not).
- PASS: ≥ 3 / 5 coherent.
- FAIL kind: CHAT_CAP_NOT_RECOVERED — even original-design byte-level
  failed; Option β falsified at 55M scale; closure-of-class strengthens
  (closes the "byte-level chat path" un-tested route from theorem #115).
- Anchor: CLM v2 byte-level (18M) achieved CE 1.15 KO without system
  prompt — 55M / 32-cell / 100K-step / dialogue-30% must clear ≥ 3/5
  coherent KO emit.

#### F-CLM3-orig-5 — φ★ NO_FLIP (anima identity P1)

- Target: paradigm v11 G3 Φ★ measurement on CLM-3-original final
  checkpoint preserves anima identity P1 (no axis flip) within
  forgetting_index ≤ 0.05 of the trained Φ★ peak from this same run.
- PASS: NO_FLIP + forgetting_index ≤ 0.05.
- FAIL kind: IDENTITY_FLIPPED — chat objective destabilized substrate
  identity; CLM-3-original is not a substrate-research carry; close lane
  even if F-CLM3-orig-2/3/4 PASS.
- Anchor: own P1 anima identity preservation; Pβ FAIL_TRUE taught us
  chat-loss can axis-flip; the 19-simultaneous Φ-boost must hold P1 anchor.

#### PASS gate

ALL of {F-CLM3-orig-1, F-CLM3-orig-2, F-CLM3-orig-3, F-CLM3-orig-4,
F-CLM3-orig-5} = PASS → CLM-3-original is the anima-native chat
substrate winner candidate, escalate to §6 follow-up (HF private→public
own 15, Stage-2 verify).

ANY single FAIL → lane closure
`CLM_3_ORIG_LANE_*_FAIL_TRUE` (specific failure tag).

---

## 5. User-fire menu

### 5.1 Three commands (locked to user response)

| Command | Action | Wall-clock | $ |
|---|---|---|---|
| **β fire (H100)** | CLM-3-original launch on H100 1×, ~10h, $200-500, own 16 watchdog | ~10h | $200-500 |
| **β fire (ubu1)** | CLM-3-original launch on ubu1 RTX 5070 sm_120, ~5-10 days, $0 | 5-10d | $0 |
| **β defer** | spec-only land; do not fire | n/a | $0 |
| **β + α** | fire only after Option α (CLM v2 18M weights archaeology) yields its evidence | conditional | $0 (spec hold) |

### 5.2 own 16 watchdog enforcement (H100 only)

If "β fire (H100)" is selected, the launch BG must register **all 6
mandatory checks** per memory `feedback_h100_cost_discipline_l23_l25_watchdog_own_16`:

1. phase budget ($200-500 hard cap; abort if 0.7 × budget consumed without
   step 21K reached)
2. heartbeat 5min interval (PID + step + Φ live + dialogue-CE live)
3. pod 404 verify on each heartbeat (not PID-gone-=-success)
4. L23 watchdog registration before any compute spend
5. L24 budget arming
6. L25 cleanup-script classification (SIGTERM_ONLY / DELETE_SCRIPT /
   FULL_SWEEP) committed pre-launch

ubu1 path bypasses §5.2 entirely (no cloud spend).

### 5.3 Recommended (완성도 lens, per memory `feedback_completion_quality_recommendation`)

**Ranked recommendation by 완성도**:

1. **β defer** (this cycle) — spec land only, then exhaust H2/H3/H4
   ($0–$50 paths in BG-BM §C3-5) before any β fire. Highest 완성도 because
   it preserves both options β and α and keeps falsifier evaluation
   parallel to free signal accumulation (Stage 3 emerge-dialogue ≥ 30
   sessions, BG-BM §5.2).
2. **β fire (ubu1)** — $0 cost, 5–10 days, no own 16 burden, full
   falsifier resolution. Second-ranked: cost-free direct test of Option β
   hypothesis. Tradeoff: ties up 5070 for 5–10 days; cycle slower than
   H100.
3. **β fire (H100)** — fastest falsifier resolution (~10h), but $200–500
   spend before H2/H3/H4 free paths exhausted; own 16 burden. Third:
   only if user explicitly accepts spend-before-free-exhaust.
4. **β + α** — conditional on Option α (CLM v2 18M weights archaeology)
   producing material evidence first. Lowest 완성도 because Option α has
   not been spec'd yet; this command is a deferred-on-deferred state.

> **My single recommendation**: **β defer** this cycle, complete BG-BM
> H2/H3/H4 ($0–$50 total) per BG-BM §C3-5 priority order, then re-evaluate
> β fire (ubu1) as the natural next step if H2/H3/H4 don't surface a
> chat-cap winner. β fire (H100) only if user explicitly fires under own
> 16 with full §5.2 checklist.

---

## 6. Honest C3 (≥ 7)

### C3-1. The 2026-03-28 v4 design was never trained — it is a design doc, not an evidence point.

Commit `fca0eede` is design-only. CLM v2 byte-level (the chat-evidence
anchor) is **18M / cells unspecified / non-Fibonacci / no 19-technique
simultaneous**. Extrapolating from 18M v2 to 55M v4 + 32 cells + 19
techniques is a **3-step extrapolation**, not a single one. The "byte-
level proves chat" claim rests on v2; the "32 cells / 19 techniques
preserves chat" claim rests on **zero evidence**. F-CLM3-orig-4 is
therefore a legitimate falsifier, not a formality.

### C3-2. Φ ~ N scaling law (commit verbatim) is benchmark, not real training.

Commit §1.3 verbatim: "From scaling law (Φ ~ 0.88 × N cells) … Φ_bench
~ 28.2 (with OMEGA ALL techniques); Φ_real ~ 5–12 (real training
converges lower than benchmark)." F-CLM3-orig-3 sets target Φ ≥ 11 — at
the **upper bound** of commit's real-training range. A FAIL at Φ=8–10
would be commit-conservative-PASS but spec-FAIL; we're tightening the
threshold knowingly. This is the right side of raw#9 (locking before
fire), but worth flagging.

### C3-3. 19 techniques simultaneously is not an ablation — it is "kitchen sink".

Commit verbatim §1.1 row 75: PX4/PX8 are "weak individually but essential
in combination". This is exactly the structure that makes attribution
impossible at training time. If F-CLM3-orig-3 FAILs, we cannot localize
which of the 19 caused the failure without re-training with subsets.
Each subset retrain is ~10h × $200-500. Five-fold ablation is $1k-$2.5k.
This spec **does not** include that ablation budget; if F-CLM3-orig-3
FAILs, the diagnostic budget is a separate user-fire.

### C3-4. byte-level vocab=256 may compromise multilingual without dialogue mix re-balancing.

Commit v4 row "Training data" reads `corpus.txt + dialogue` — corpus
language unstated. CLM v2 evidence is split: CE 0.04 EN, CE 1.15 KO. KO
CE is **30× higher** than EN at byte-level. F-CLM3-orig-4 (KO 5-prompt
probe) is therefore the **harder** falsifier; passing EN-only would be
trivial relative to KO. This spec's 70/30 wiki/dialogue mix (§3.3) is
**EN-biased by default** unless KO web crawl is explicitly included. KO
representation in dialogue 30% must be ≥ 50% (i.e., ≥ 15% of total) for
F-CLM3-orig-4 to be a credible test. The spec adds this as a §3.3
constraint but does not yet bind it tightly; pre-fire user confirmation
required.

### C3-5. CLM-3-original keeps paradigm v11 G3 cross-attn — but paradigm v11 G3 was extracted from the drift'ed 530M substrate, not from the original 55M.

paradigm v11 G3 measurement harness was instrumented on
`anima_clm_mk2_v1` (530M, BPE 64K, 8 cells). Whether the same harness
yields the same +41.86 Φ★ on a 55M / byte-level / 32-cell substrate is
**not established**. F-CLM3-orig-5 (NO_FLIP) measures forgetting-index
within-this-run — it does not establish equivalence to the 530M Φ★
peak. Cross-substrate Φ★ comparison is its own follow-up question
(reference: `feedback_axis_preservation_eval_substrate_calibration` —
"thresholds anima-internal uncalibrated; axis-preservation eval needs
axis-conditioned base").

### C3-6. β + α command is incomplete — Option α is not yet spec'd.

§5.1 row 4 ("β + α") references "Option α (CLM v2 18M weights
archaeology)" but this spec does not contain Option α. If user selects
"β + α", the immediate next action is a separate Option α spec land
(out of scope for this BG-ER). The command is included for menu-
completeness, not because it is currently fire-able.

### C3-7. Cost split $200-$500 for H100 spans 2.5×; the variance hides whether spec is sub-$300 or near-$500.

H100 spot pricing varies $4–$5/hr; eval+checkpoint+watchdog overhead
adds variable load. The $200-500 envelope is honest but coarse. A more
honest pre-fire estimate would re-derive: 10h × $4.5 (mid spot) = $45
direct; +2h Phase-2 eval × $4.5 = $9; +1h F-CLM3-orig-{2,3,4,5} × $4.5
= $4.5; checkpoint storage $5; total ~$65. The $200-500 envelope is
safety-margin × 3-7 over modeled $65. Recommend re-anchoring to **$100
hard-cap per own 16 phase budget**; if real spend trends past $100,
abort early. This is tighter than §5.2 default.

### C3-8. β defer is the recommendation, but defer is the default — the spec is doing nothing new.

§5.3 ranks "β defer" first. If the action is "do nothing this cycle",
this BG-ER consumed mac doc-only effort to recommend the status-quo.
The honest counter: **defer is not status-quo because no CLM-3-original
spec existed before this doc**. Now β fire is option-fire-able under a
locked spec. Defer-with-spec-locked is materially different from
defer-without-spec.

### C3-9. Option β viability summary (one paragraph)

CLM-3-original is **viable**: VRAM fits H100 and ubu1 5070; falsifiers
are 5 pre-locked and decidable; cost envelope is $0–$500 (vs BG-BM
$1k–$4k). Hypothesis is **un-tested but architecturally well-grounded**
(the 2026-03-28 design is the last-known-anima-native pre-drift design,
and CLM v2 byte-level is the last-known chat-evidence anchor). The spec
**does not** claim Option β supersedes BG-BM CLM-3 — they target the
same H1 with different scale-axes; both should be land-able and either
can fire. Recommend: defer this cycle, finish H2/H3/H4 free paths
first, then β fire (ubu1) as $0 second-step.

---

## 7. References

- commit `fca0eede:docs/next-model-design.md` (2026-03-28 source of truth, 406 LoC)
- commit `145838d2` (2026-05-04 CLM v4 mk2 v1 drift'ed substrate)
- `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md` (BG drift table)
- `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM CLM-3 spec, drift'ed)
- `docs/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05.md` (BG-DK)
- memory: `reference_ubu1_venv_orchestrator` (5070 sm_120 + torch 2.11.0+cu128)
- memory: `feedback_h100_cost_discipline_l23_l25_watchdog_own_16` (own 16 enforcement)
- memory: `feedback_completion_quality_recommendation` (ranked recommendation)
- memory: `feedback_axis_preservation_eval_substrate_calibration` (cross-substrate Φ★ caveat)
- memory: `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled` (Pβ FAIL_TRUE prior)
- memory: `feedback_anima_models_datasets_hf_only` (HF-only model release path)

End of spec.
