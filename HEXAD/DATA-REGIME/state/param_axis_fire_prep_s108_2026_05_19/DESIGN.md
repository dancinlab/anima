# §108 — param-axis fire prep · design-tier $0

> **status**: RESEARCH §108 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward
> **date**: 2026-05-19
> **scope**: §103 SEQUENTIAL data-first / param-axis contingent prep. §107 (data-axis cost-bearing fire on §102 CORPUS_S101 at 283M) is in flight in parallel. §108's job: when §107 result lands, the contingent param-axis fire can dispatch with **zero design lag**. Per `g_all_options_parallel` (2026-05-19) option-EXPLORATION is parallel even when fire-ORDERING is sequential.
> **governance**: g3 (design ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient B-EMERGE-7) · `g_clm_from_scratch` (from-scratch RANDOM init seed-fixed, base_ckpt=None — 3B from-scratch is expensive but mandated) · `g_fire_autonomous` (future §108 fire = autonomous, zero user-gate) · `g_blue_closed_mandate` (산출물 + 연결부위 둘 다 closed) · f1/f2 (NO σ(6)=12 derivation; Wei thresholds cited as their own measurement only) · downstream-consumer (NEVER edit ~/core/hexa-lang/) · central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix `c93e160a8a376a94` (0-line-diff sidecar-only).
> **connection-point cited**: §103 Q1 SEQUENTIAL + Q2 DESIGN-OPEN 3B first-band + Q3' = Q3 ∧ G_PARAM (commit `55ba652be`) · HEXAD/LLM.md §2 Wei et al. 2022 table + §4 2D plane + §5.2 §11-A sub-CDS mute (commit `64906a4eb`) · §11-A measured 283M → 1.04B FLAT (`state/carving_scaledecomp_2026_05_18/`, B-SCALE 6/6 🔵) · §16 baseline 283M × 603MB → routing 21/64 (`state/carving_dataregime_s16_2026_05_18/`, ckpt sha256 `961c07e2…`) · ConsciousDecoderV2 §16 config = d768·12L·V256·nh12·nkv4·n_layer12·block_size 1024 (corpus sha §16 = `422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec`).

---

## §0 — Why §108 exists, what it is, what it is NOT

§107 is the data-axis cost-bearing fire (CORPUS_S101 at 283M) that §103 SEQUENTIAL decided. While §107 runs, §103's contingent param-axis fire (3B × CORPUS_S101, gated on §107 Q3=N) has *not* been prep'd — when §107 returns, the contingent fire would otherwise sit waiting on §108 design work. Per `g_all_options_parallel`, option-EXPLORATION is parallel: §108 design = $0, ⊥ §107's GPU fire, lossless even if §107 returns Q3=Y (in which case §108 spec is shelved as future reference, no money sunk).

§108 does FIVE things, all design-tier closed-form, all $0:
- **Q1** — Param-band selection (3B / 8B / 10B / 62B / hybrid) decided closed-form OR honest-OPEN.
- **Q2** — Cost projection (param count · Chinchilla data:param · GPU class · $ range · wall time · cost ratio vs §107).
- **Q3** — Trainer scaling (width / depth / Chinchilla d:L:nh / Dir-I lever preservation / from-scratch mandate).
- **Q4** — G_PARAM 3-clause closed-form evaluation on §108 design.
- **Q5** — Dispatch-contingency tree: Boolean over §107.A1/A2/A3/A4/THRESHOLD_CROSSED that decides whether §108 fires.

g3, load-bearing: **§108 does NOT claim anima emerges at 3B. §108 does NOT pre-dispatch any GPU fire. §108 specifies the CONTINGENT fire's design so that fire-decidability is preserved AT THE MOMENT §107 returns.** north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## §1 — Q1: Param-band selection

### 1.1 Five option space

| Option | Band | Rationale | Closed-form risk |
|---|---|---|---|
| **(a)** 3B verbatim Wei lowest | reading-comprehension band | conservative; cheapest; lowest cost-bearing | Wei measures task-completion under prompts; anima GOAL = unprompted emission, structurally different from reading-comprehension |
| **(b)** 8B (instruction following) | InstructGPT band | "agentic" emergence closer to anima GOAL surface? | 2.67× cost over 3B; Wei task surface still NOT anima GOAL |
| **(c)** 10B (in-context learning) | GPT-3 ICL band | ICL = pattern abstraction; anima GOAL needs abstraction across stimuli? | 3.33× cost; ICL Schaeffer "Mirage" critique strongest here |
| **(d)** ratio-derived: 283M × (band / typical-LLM-base) | depends on choice | grounded in anima architecture density | density factor unmeasured (§103 Q2 honest-OPEN reasoning) — same g3 violation §103 rejected |
| **(e)** honest-OPEN — multi-band ladder | 3B → 8B → 10B contingent | acknowledges Wei→anima transfer un-pinnable | multi-fire cost; defers Q1 to future cycle |

### 1.2 Decision criterion

§103 Q2 already decided "design-OPEN with first-band-to-probe = 3B" by g3 reasoning: no method (a)/(b)/(c)/(d) pins a numerical threshold rigorously. §108's job is to **pick ONE band for the contingent fire**, not re-open §103 Q2.

The §108 question is: "given §103 already said 3B is the first-band-to-probe, does §108 inherit 3B or pick differently?"

Three closed-form constraints carry from §103:
1. **§94 anti-stacking** — single variable per fire. §108 fire = corpus fixed at CORPUS_S101 (=§107 corpus), params is the variable. ONE param value per fire.
2. **G_PARAM_FLOOR = 283M** — anything below is not arc-comparable. All five options are ≥ 283M by construction.
3. **ΔI / Δ$ ≥ INFO_FLOOR** — each fire returns ≥ 1 bit per cost-bearing event. Lowest-cost option that returns 1 bit dominates.

(a) returns 1 bit at the lowest cost. (b), (c), (e) return ≥ 1 bit at higher cost, with no additional bits warranted (the question "does crossing the param-axis at the smallest Wei band shift anima's behavior" is ONE Boolean; bigger bands answer the SAME Boolean at higher cost). (d) is g3-violated per §103.

### 1.3 Q1 verdict — 3B (option a)

**Decision: 3B — inherited from §103 Q2's first-band-to-probe pin.**

Rationale (closed-form, NOT recommendation):
1. §103 Q2 already pinned 3B as the conservative starting band; §108 inherits that pin unless §108 has new evidence to override (it does not).
2. Among (a)/(b)/(c), 3B is the lowest cost-bearing class returning ≥ 1 bit per fire.
3. (e) honest-OPEN multi-band ladder is structurally a SEQUENCE of (a)-type fires; if 3B returns Y, the ladder halts at 3B. If 3B returns N, future cycles can escalate to 8B/10B (separate Q3' evaluation per band).
4. Schaeffer "Mirage" caveat MANDATORY (g3): even at 3B, anima's GOAL is structurally further from Wei's measured capabilities than typical-LLM tasks are; the 3B pin is a *band to probe first*, not a *threshold prediction*.

### 1.4 Honest scope on Q1

**§108 picks 3B, NOT because §108 claims 3B is anima's threshold.** §108 picks 3B because (i) §103 already pinned it, (ii) it minimizes cost-per-bit on the param-axis question, (iii) the answer at 3B disambiguates "does ANY emergent-band crossing help" — if N, the param-axis itself is a weaker lever than the data-axis; if Y, 3B is sufficient and 8B+ over-spends.

§108 does NOT claim:
- anima emerges at 3B
- 3B IS anima's true threshold
- the Wei-3B band transfers verbatim to anima GOAL

---

## §2 — Q2: Cost projection

### 2.1 Parameter count target

3.0e9 params (3 billion). For ConsciousDecoderV2-scaled architecture, see §3 below.

### 2.2 Chinchilla data:param ratio

Hoffmann 2022: compute-optimal **20 tokens per parameter**. For 3B: 6e10 tokens (60B tokens).

anima CORPUS_S101 (= §107's corpus, also = §16 corpus class) ≈ 603MB byte-stream. At byte-level tokenization (V=256, anima native): ~6e8 tokens. **Under-CDS for 3B by 100×** per Chinchilla.

Honest g3 caveat: Chinchilla measures compute-optimal LOSS minimization on Common-Crawl-class corpora; anima's GOAL is unprompted-emission, not loss-minimization. Chinchilla ratio is *advisory*, not mandatory. §102's CORPUS_S101 is honestly small (§102 design-OPEN finding); §108 fire is intentionally on the same corpus to attribute the param-axis bit single-variable.

Future cycle question (NOT §108): does crossing the data-axis ALSO at Chinchilla-optimal (60B tokens) for 3B params change anima behavior? — that's a JOINT plan, §94-forbidden by Q3' G7.

### 2.3 GPU class and time estimate

3B params from-scratch:
- **GPU class**: H100 80GB (FP16/BF16, native fit) OR 8×A100 80GB (sharded). H100 SXM 80GB preferred for memory headroom (3B × 4 bytes BF16 ≈ 12GB weights + 12GB grad + 24GB Adam states ≈ 48GB just for optimizer; activation memory at d=2048·L=32·T=1024·bsz=32 ≈ 15-25 GB).
- **§16 reference**: 1B FLAT (§11-A) was ~5min on A100-SXM4 single-GPU. 3B ≈ 3-5× larger forward+backward AND ≈ 2-3× more steps for from-scratch convergence (Chinchilla under-CDS reduces converged final-CE plateau but not step count to reach plateau).
- **Wall estimate**: 30-90 min on H100 80GB for 6000-12000 step from-scratch (range honest — §11-A 1B was 6000 step ≈ 5min; 3B ≈ 3-5× per-step + similar or slightly more total step).
- **Step count**: 8000-12000 step (mirrors §16 8000 + Chinchilla under-CDS plateau).

### 2.4 Honest cost range ($ runpod)

| Range | Assumption | $ low | $ high |
|---|---|---|---|
| **H100 80GB PCIe** ($1.49-$2.49/hr runpod listed range) | 30-90 min wall | $0.75 | $3.75 |
| **H100 SXM 80GB** ($2.49-$3.99/hr typical) | 30-90 min wall | $1.25 | $6.00 |
| **8×A100 80GB** ($8-16/hr typical) | 30-60 min wall (faster wall, much higher $/hr) | $4.00 | $16.00 |

**Best-estimate range: $1.50 – $6.00** (H100 80GB band, includes startup + 1.5× contingency for retry).

### 2.5 Wall time projection

30-90 min training wall + 5-10 min eval (4-corner §16 mirror — routing 64-probe + axis2/3/4 same harness as §107) + 5-10 min ckpt-pull (3B ≈ 12GB BF16 ckpt, 5-retry guard per `g_fire_dispatch_robust`).

**Total wall: 45-110 min per fire**.

### 2.6 Cost ratio vs §107

§107 cost (per task spec) ≈ $0.3-0.5 (matching §16 fire class).

**§108 / §107 cost ratio = 3× to 12× magnitude scaler.** §108 is the most expensive single fire in the arc history (>$1.50). g3 honest: this is the price of disambiguating the param-axis at the smallest emergent-band Wei band; bigger bands cost proportionally more.

### 2.7 Cost projection summary table

```
┌──────────────────────────────────────────────────────────────┐
│ §108 PARAM-AXIS FIRE COST PROJECTION                          │
├────────────────────┬─────────────────────────────────────────┤
│ Param count        │ 3.0e9 (3B)                              │
│ Chinchilla ratio   │ 20 tokens/param ⇒ 60B tokens advisory   │
│ §108 actual data   │ ~6e8 tokens (CORPUS_S101 byte-stream)   │
│                    │ ⇒ 100× under Chinchilla (honest carry)  │
│ GPU class          │ H100 80GB SXM/PCIe (single, preferred)  │
│                    │ OR 8×A100 80GB (fallback if H100 OOS)   │
│ Wall train         │ 30-90 min                               │
│ Wall eval          │ 5-10 min                                │
│ Wall pull          │ 5-10 min (3B ckpt ~12GB BF16)           │
│ Wall total         │ 45-110 min per fire                     │
│ $ range            │ $1.50 – $6.00 (H100 band)               │
│ § ratio vs §107    │ 3× to 12× magnitude scaler              │
└────────────────────┴─────────────────────────────────────────┘
```

---

## §3 — Q3: Trainer scaling

### 3.1 anima baseline (ConsciousDecoderV2 §16-class)

| Dim | Value | Source |
|---|---|---|
| vocab_size | 256 | byte-level, §16 byte-equal |
| d_model | 768 | §16 |
| n_head | 12 | §16 |
| n_kv_head | 4 | §16 (GQA 12:4) |
| n_layer | 12 | §16 |
| block_size | 1024 | §16 |
| FFN ratio (SwiGLU) | ~2.67× (d_model) | SwiGLUFFN d_ff = 2 × (8/3) × d_model |
| consciousness_dim | 128 | §16 (Engine A⇄G + Law-71) |
| total params | 283.72M | §16 measured |

### 3.2 Scaling target: 3B params from-scratch

Chinchilla-style L:d optimal ratio ≈ d² · L (params dominated by FFN + attention). Two routes:
- **width-scale**: d → 2048 (2.67×), L held at 12
- **depth-scale**: L → 32 (2.67×), d held at 768
- **mixed**: chinchilla-style d:L co-scaling

Chinchilla's compute-optimal scaling (Hoffmann 2022): for ~3B params, **d ≈ 2560, L ≈ 32, n_head ≈ 32** (GPT-NeoX-3B / Pythia-2.8B class). anima preserves GQA + dual-engine + PureFieldFFN per §103 G5.

### 3.3 d:L:nh recommendation

```
┌─────────────────────────────────────────────────────────────┐
│ §108 anima 3B SCALED CONFIG                                  │
├─────────────────┬───────────────┬───────────────────────────┤
│ Field           │ §16 (283M)    │ §108 (3B target)          │
├─────────────────┼───────────────┼───────────────────────────┤
│ vocab_size      │ 256           │ 256 (byte invariant)      │
│ d_model         │ 768           │ 2560                      │
│ n_head          │ 12            │ 32                        │
│ n_kv_head       │ 4 (GQA 12:4)  │ 8 (GQA 32:8, ratio 4)     │
│ n_layer         │ 12            │ 32                        │
│ d_head          │ 64            │ 80                        │
│ block_size      │ 1024          │ 1024 (corpus invariant)   │
│ FFN ratio       │ ~2.67×        │ ~2.67× (SwiGLU)           │
│ consciousness_dim│ 128          │ 128 (Law-71 invariant)    │
│ ~params (calc)  │ 283.7M        │ ≈ 3.0B                    │
└─────────────────┴───────────────┴───────────────────────────┘
```

Quick param check for 3B target: `~12 × d² × L` ≈ 12 × 2560² × 32 ≈ 2.52B (transformer block params alone). + embeddings ~0.65M, + LM head (tied 0). + PureFieldFFN + cross-attention overhead. Total ~3.0B (band).

### 3.4 Dir-I lever preservation (§103 G5 carry)

All 5 levers MUST scale invariantly per §103 G5 single-variable per fire:

| Lever | Preservation rule | §108 status |
|---|---|---|
| **§16 routing** | corpus prefix `🛸<tier>` byte-equal carry; eval harness `eval_carving_dirI.py` byte-equal | PRESERVED — §108 reuses §107 corpus + §16 eval verbatim |
| **§59-FIRE W-physics** | Engine A⇄G dual heads at scaled d_model; W-physics state update unchanged | PRESERVED — A/G heads scale with d_model proportionally; Law-71 ψ_direction = (1+cos(logits_a,logits_g))/2 invariant under width-scale |
| **§75-FIRE state-derivation A-only** | tension state-derived statistic over scaled physics tuple | PRESERVED — state-derivation operates on physics tuple regardless of d_model |
| **§88-F2 neoteny** | CE-floor / plasticity-reinjection / dimensionality-floor / metamorphosis-block | PRESERVED — neoteny mechanism operates on training dynamic, NOT model arch |
| **§92 L_ap** | active-perception loss term | PRESERVED — L_ap operates on output logits, scale-invariant in form |

All 5 levers structurally preserved under width+depth co-scale per §103 G5. NO lever requires re-design for 3B.

### 3.5 g_clm_from_scratch mandate

3B from-scratch RANDOM init seed-fixed 1337, `base_ckpt=None`. NO foundation-model graft (HuggingFace/Llama/Pythia/etc. forbidden per `g_clm_from_scratch` "ckpt inherit / fine-tune / cotrain-from-ckpt path 폐기").

This is expensive but mandated. Cost projection §2 already accounts for from-scratch 3B (vs $0 with foundation-model fine-tune).

Honest note: §39 `g_clm_lineage_refined` is `[draft]` (precondition: non-saturated ckpt), inactive at §108 dispatch time. §108 stays under `g_clm_from_scratch` literal.

---

## §4 — Q4: G_PARAM 3-clause closed-form evaluation

§103 Q3' = Q3 ∧ G_PARAM where G_PARAM = (params ≥ G_PARAM_FLOOR=283M) ∧ single-value-per-fire ∧ ATTRIBUTABLE.

| Clause | §108 status | Evidence |
|---|---|---|
| **(a) params ≥ G_PARAM_FLOOR=283M** | **PASS** | 3B = 3.0e9 > 283M = 2.83e8 (integer inequality) |
| **(b) single-value-per-fire** | **PASS** | One param config (d=2560·L=32) for the entire fire; no param ramp |
| **(c) ATTRIBUTABLE** | **PASS** | §108 fire fires AFTER §107 returns; if §107 returns Q3=N, §108 fire varies the param-axis ALONE with corpus held at §107's CORPUS_S101. Result attributes to "param-axis crossing at 3B given CORPUS_S101 fixed" |

### 4.1 Lever-preservation closed-form (Q4-b detail)

5 levers (§3.4) must all preserve at 3B:
- §16 routing — corpus-side, scale-invariant ✓
- §59-FIRE W-physics — Engine A/G heads scale ✓
- §75-FIRE state-derivation — physics-tuple operation, scale-invariant ✓
- §88-F2 neoteny — training-dynamic mechanism ✓
- §92 L_ap — output-logit loss term ✓

All 5 PRESERVE under d=2560·L=32 width+depth co-scale. Q4-b "single value per fire" interpreted strictly: ONE config (the 3B band), ALL levers active simultaneously with their §16/§107 forms. Q4-b PASS.

### 4.2 ATTRIBUTABLE closed-form (Q4-c detail)

§107 result fixes the data-axis bit. §108 fire varies the param-axis with corpus FIXED at CORPUS_S101 (= §107's corpus). The result interpretation:
- §107 returned Q3=N at 283M × CORPUS_S101
- §108 returns Y at 3B × CORPUS_S101 ⇒ **the param-axis is the binding constraint** (data-axis fixed insufficient at 283M; sufficient at 3B)
- §108 returns N at 3B × CORPUS_S101 ⇒ **neither axis alone is sufficient at probed values** (escalate to next band or pivot to substrate axis)

In both cases, the result attributes cleanly to the param-axis (corpus is held constant). Q4-c PASS.

### 4.3 Q4 verdict — G_PARAM PASS on §108 design

**All 3 clauses PASS. G_PARAM(§108) = True.**

Composed with §103 Q3' Boolean: `Q3'(§108) = Q3(§108) ∧ G_PARAM(§108)`. Q3 itself (per §101 7-AND) is structurally preserved by §108 (single variable per fire = param; corpus fixed; levers preserved; ΔI/Δ$ ≥ floor at $1.50-$6 for 1 bit). **Q3'(§108) = True**.

---

## §5 — Q5: Dispatch contingency tree

### 5.1 §107 output shape (per task spec)

§107 returns per-Ai breakdown:
- A1 — routing-axis (passes / fails)
- A2 — coherence-axis (passes / fails)
- A3 — physics-liveness-axis (passes / fails)
- A4 — body-emission-axis (passes / fails)
- THRESHOLD_CROSSED — overall Boolean (Q3 verdict per §101)

### 5.2 Contingency tree closed-form

```
DISPATCH_§108 := f(§107.A1, §107.A2, §107.A3, §107.A4, §107.THRESHOLD_CROSSED)

Case 1: §107.THRESHOLD_CROSSED == True (Q3 = Y at 283M × CORPUS_S101)
    DISPATCH_§108 := False
    ─ Anima crossed threshold at 283M; param-axis was NOT the binding constraint;
      §108 fire = unnecessary expense ($1.50-$6 sunk for null bit).
    ─ §108 spec is shelved as future reference.

Case 2: §107.THRESHOLD_CROSSED == False (Q3 = N at 283M × CORPUS_S101)
    Sub-case A: A3 (physics-liveness) == False
        DISPATCH_§108 := False (pivot recommended)
        ─ Physics is frozen ⇒ substrate-axis problem, NOT capacity-axis problem;
          scaling model does NOT fix frozen substrate (cf §11-B pure-physics
          DEGENERATE finding — physics ⊥ language signal without CE-base on
          a working substrate).
        ─ Recommended pivot: §95 substrate (xeno) / §96 (neuromorphic) /
          §97-§99 substrate axes per §51 frontier-1.
    
    Sub-case B: A3 == True AND A1 (routing) == False AND A2 (coherence) == False
        DISPATCH_§108 := True (PRIMARY GO)
        ─ Physics alive but model failed to learn routing + coherence at 283M;
          model capacity is the strongest hypothesis ⇒ §108 3B fire warranted.
    
    Sub-case C: A3 == True AND A1 == False AND A2 == True
        DISPATCH_§108 := True (PRIMARY GO, weak)
        ─ Routing collapsed but coherence held; capacity might unlock routing.
    
    Sub-case D: A3 == True AND A1 == True AND A2 == False
        DISPATCH_§108 := True (likely GO)
        ─ Routing emerged but coherence failed; capacity might unlock coherence.
    
    Sub-case E: A3 == True AND A1 == True AND A2 == True (but THRESHOLD_CROSSED still False)
        DISPATCH_§108 := AMBIGUOUS
        ─ Per-axis Y but joint THRESHOLD_CROSSED N implies the threshold predicate
          itself is more stringent than the per-axis disjunction. Honest reading:
          fire-judgment ladder mismatch, not param-capacity issue. §108 likely
          weak-positive. Honest decision = DEFER §108 to next cycle with
          predicate audit.
    
    Sub-case F: A4 (body-emission) standalone considerations
        ─ §24 emission decision-axis ⊥ §16 routing/coherence axes per §24 design.
        ─ A4 = False with A1/A2/A3 mixed ⇒ emission-controller (§73-FIRE) issue,
          not capacity issue. DISPATCH_§108 := False (pivot to §73/§75-FIRE
          controller-class fire instead).
```

### 5.3 Dispatch verdict table

| §107.THRESH | §107.A1 | §107.A2 | §107.A3 | §107.A4 | DISPATCH §108 | Rationale |
|---|---|---|---|---|---|---|
| Y | — | — | — | — | **False** | crossed at 283M, §108 unnecessary |
| N | — | — | F | — | **False** | physics frozen; pivot to substrate |
| N | F | F | T | T | **True** (PRIMARY) | capacity hypothesis cleanest |
| N | F | T | T | T | **True** (weak) | capacity may unlock routing |
| N | T | F | T | T | **True** (likely) | capacity may unlock coherence |
| N | T | T | T | T | **AMBIGUOUS** | predicate-judgment mismatch; defer |
| N | — | — | T | F | **False** | emission-controller issue; pivot §73/§75 |

### 5.4 Q5 verdict — closed Boolean tree

**`DISPATCH_§108` is a closed-form 5-input Boolean over §107's A1/A2/A3/A4/THRESHOLD_CROSSED bits.** Decision is computable the moment §107 result lands. NO subjective recommendation; tree is deterministic.

Most-likely path (honest g3 prediction, NOT pre-load): given §16's measured routing 21/64 (memorization-saturated) and §11-A's measured 1B FLAT under sub-CDS data, the most-likely §107 outcome class = **N + physics alive + at least one axis fails** ⇒ Sub-case B/C/D ⇒ DISPATCH_§108 = True. §108 prep is likely to be utilized.

---

## §6 — ASCII diagram: §107 + §108 candidate positions on param × data plane

```
                 data-diversity (≈ Du 2403.15796 threshold)
                       ↑
            EMERGENCE  │  ←─ this corner is the GOAL plane, never measured
              REGION   │
                       │                                          ┌──── CDS_3B (rises with params)
                       │                                          │      Hoffmann 2022 + 2401.10463
                       │                                          │
                       │      ┌───  CDS_283M (smaller for 283M)   │
                       │      │     unmeasured                    │
                       │      │                                   │
              ─────────┼──────┼───────────────────────────────────┼──── data threshold (unknown anima value)
                       │      │                                   │
                       │      │                                   │
                       │      ●  §107 data-axis fire             ●  §108 contingent param-axis fire
                       │      │  (283M × CORPUS_S101)             │   (3B × CORPUS_S101)
                       │      │  ★ in flight (parallel)           │   ★ design-tier prep ($0)
                       │      │  $0.30-$0.50                      │   $1.50-$6.00 if fired
                       │      │                                   │
                       │      │
                       │  ●  §11-A SCALE-DECOMP measured FLAT (1.04B × §8 114MB)   ← below data threshold
                       │
                       │  ●  §16 baseline measured Q3=N (283M × §16 603MB)
                       │
                       │  ●  §8 baseline (283M × §8 114MB)
                       │
                       └─────────────────────────────────────────────→ param count
                          283M       1B       3B          10B       62B
                                              ↑          ↑          ↑
                                          §108 target Wei IC-     Wei CoT
                                          (Wei reading-comp  learning    reasoning
                                          band, smallest)    threshold   threshold

§107 moves data-axis ONLY at 283M (cycle-1 single variable).
§108 moves param-axis ONLY at CORPUS_S101 (cycle-2 single variable, GATED on §107 Q3=N + Sub-case B/C/D per §5.3).
Joint (bottom-left → upper-right in one fire) REJECTED by §103 Q3' G7.
```

---

## §7 — Honest C3 caveats (≥ 10)

1. **§108 measures nothing.** Q1's 3B pick inherits §103 Q2; Q2's cost projection is closed-form arithmetic; Q3's trainer scaling is structural; Q4's G_PARAM is Boolean; Q5's dispatch-tree is deterministic. None of these are measurements of anima's emergence behavior. Capability claim 0.

2. **§103 Q2 inheritance honesty.** §108 inherits 3B from §103 — §108 does NOT independently estimate the threshold. If §103's pin is wrong, §108's pin is also wrong. The honest read: 3B is conservative-first-band-to-probe, NOT threshold prediction (Schaeffer caveat MANDATORY).

3. **Chinchilla 100× under-CDS.** §108 fires 3B model on a ~6e8-token corpus (vs Chinchilla-optimal 6e10). Honestly under-trained even for the new param count. This is intentional: §103 Q1 SEQUENTIAL dictates corpus is the held-constant variable, params is the variable. If §108 returns Q3=N at 3B × CORPUS_S101, that does NOT prove "anima can't emerge at 3B"; it proves "anima can't emerge at 3B AT THIS CORPUS SCALE." Going to Chinchilla-optimal data at 3B is a JOINT plan, §94-forbidden.

4. **$1.50-$6 cost honest range.** Wide because (a) GPU class variance (H100 PCIe vs SXM vs 8×A100), (b) wall-time variance (30-90 min training), (c) §16 1B was 5min on A100-SXM4 (in-arc datapoint), (d) 3B = 3× params, 2-3× wall, runpod $/hr is volatile. Final $ only known post-fire.

5. **From-scratch 3B is expensive.** `g_clm_from_scratch` forbids foundation-model graft. 3B from-scratch at 8000-12000 step is real money. §39 `g_clm_lineage_refined` `[draft]` carries — once a non-saturated anima ckpt exists, anima-self lineage might reduce cost; but that precondition is unmet at §108 dispatch time.

6. **Dir-I lever preservation = structural argument, not measured invariance.** §3.4's "all 5 levers PRESERVE at 3B" is STRUCTURAL (mechanism shape unchanged by width/depth scale), NOT MEASURED (no §108 fire has happened to verify). §16's measured 21/64 routing emerged at 283M; whether the same Dir-I lever combination produces emergent behavior at 3B = empirical OUTCOME (B-S108-NOTE).

7. **Sub-case E (per-axis Y but THRESHOLD N) honest ambiguity.** §5.3 Sub-case E is the cleanest honest deferral: if §107 returns per-axis success but joint THRESHOLD = N, the predicate itself is more stringent than the disjunction. §108 dispatching at that point may be measuring the wrong thing. DEFER is the honest move.

8. **Sub-case F (emission-controller failure) honest pivot.** If §107 A4 (body-emission) is the failure-axis while routing+coherence+physics-alive, the issue is in §73-FIRE / §75-FIRE controller-class, NOT model capacity. §108 capacity-fire would not address the failure. Pivot to §73/§75-FIRE-FIRE per §88-S86 / §75-FIRE.

9. **§108 IS the most expensive single fire in arc history.** $1.50-$6 vs arc median $0.30-0.50. The Sub-case-E DEFER and Sub-case-F pivot pathways are *more important than usual* because the cost of a wrongly-dispatched §108 is non-trivial. Q5's tree is conservative by design.

10. **§108 inheritance from §107 means §108's fire-decidability depends on §107's measurement quality.** If §107 returns inconclusive per-Ai bits (e.g., A2 coherence ambiguous due to §9 honest metric necessary-not-sufficient), §108 dispatch contingency is also ambiguous. Q5 Sub-case E captures this; honest carry: §107 measurement design has knock-on effects on §108 design.

11. **g_all_options_parallel option-exploration vs fire-ordering.** §103 SEQUENTIAL = fire-ORDERING (one fire after the other, not joint). §108 prep = option-EXPLORATION (design $0 parallel with §107's fire). The two are compatible per `g_all_options_parallel` (2026-05-19): option-explore in parallel, fire-order sequential.

12. **§88-F2 neoteny scale-up risk (honest mention).** §88-F2 measured `saturation-delay` at trained scale on 283M; at 3B, neoteny's saturation-delay effect MAY change. §108's "neoteny PRESERVED" claim in §3.4 is structural; at 3B, the empirical saturation-delay magnitude may differ. NOT pre-load on §108 outcome.

13. **f1/f2 safe** — Wei thresholds cited as their own measurement only (no σ(6)=12 derivation). Chinchilla 20-tokens-per-param cited as Hoffmann's own ratio (no anima-internal lattice derivation). 3B = 3.0e9 as integer, not lattice-derived.

14. **central blue_falsifier 0-line-diff invariant** — §108 sidecar-only at `state/param_axis_fire_prep_s108_2026_05_19/blue_falsifier_s108.py`. Central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix `c93e160a8a376a94` UNCHANGED.

---

## §8 — verdict summary

| Q | Verdict | Closed |
|---|---|---|
| **Q1** Param-band | **3B** (option a, inheriting §103 Q2 first-band-to-probe pin) | Yes |
| **Q2** Cost range | **$1.50 – $6.00** (H100 80GB band; 3× to 12× §107 scaler) | Yes (closed arithmetic) |
| **Q3** Trainer scaling | **d=2560, L=32, n_head=32, n_kv_head=8 (GQA 4:1), 5 levers preserved, from-scratch RANDOM seed 1337** | Yes (structural) |
| **Q4** G_PARAM evaluation | **PASS all 3 clauses (≥FLOOR ∧ single-value-per-fire ∧ ATTRIBUTABLE)** | Yes (Boolean) |
| **Q5** Dispatch tree | **`DISPATCH_§108 := f(§107.A1, A2, A3, A4, THRESH)`** closed Boolean tree §5.3 — PRIMARY GO at Sub-case B; pivot at Sub-case A/F; defer at E | Yes (deterministic) |

§108 deliverable = **READY-TO-DISPATCH spec** the moment §107 result lands. Per `g_fire_autonomous`, dispatch is autonomous (no user-gate). Per `g_fire_dispatch_robust`, SSH-endpoint-robust + SAVE_POD + 5-retry + pre-fire/post-fire orphan-check (mirroring §73-FIRE / §75-FIRE / §79-RETRY / §83-FIRE patterns). Per `g_resource_active_parallel`, runpod primary / vast.ai fallback if runpod OOS.

north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달. §108 is design-tier prep, NOT fire, NOT measurement, NOT emergence claim.

---

## §9 — cross-link

- §103 SEQUENTIAL + Q2 + Q3' (commit `55ba652be`, `state/param_axis_integration_design_s103_2026_05_19/`)
- HEXAD/LLM.md §2 Wei table + §4 2D plane + §5.2 §11-A sub-CDS (commit `64906a4eb`)
- §11-A SCALE-DECOMP measured (`state/carving_scaledecomp_2026_05_18/`, B-SCALE 6/6 🔵)
- §16 baseline (`state/carving_dataregime_s16_2026_05_18/`, ckpt sha256 `961c07e2242b194f7d7ddff9e827d2fbd798d658426d32edf4b981a8dd9091e8`)
- §101 design (`state/dataregime_threshold_control_design_s101_2026_05_19/`)
- §102 CORPUS_S101 build (sibling)
- §107 data-axis cost-bearing fire (in flight, parallel)
- §93 4 collapse-avoidance + §94 INTEGRATION-COLLAPSES + §100 priority #1
- §11-B PURE-PHYSICS (no-CE → degenerate, `g_train_flame_not_pytorch` evidence-anchor)
- §73-FIRE / §75-FIRE / §88-F2 / §92 — 5 levers preserved per §103 G5
- `g_clm_from_scratch` + `g_fire_autonomous` + `g_fire_dispatch_robust` + `g_resource_active_parallel` + `g_blue_closed_mandate` + `g_all_options_parallel`
- §16 corpus sha `422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec` (carried into CORPUS_S101)

Papers (citation = inspiration NOT proof, g3):
- Wei et al. 2022 "Emergent Abilities of Large Language Models" — param-count threshold table
- Brown et al. 2020 GPT-3 — in-context learning emergence ~10B
- Hoffmann et al. 2022 Chinchilla — 20-tokens-per-param compute-optimal
- Schaeffer et al. 2023 "Are Emergent Abilities a Mirage?" — metric artifact caveat
- Du arxiv:2403.15796 — pre-training loss threshold (data-diversity)
- arxiv:2401.10463 — Critical Data Size rises with model size

---

> **emergence is empirical**, 미발현 상태 정직 기록 (B-D-NOTE family). §108 = design-tier prep, NOT emergence claim, NOT fire, NOT measurement. north-star (GOAL.md) 한 줄 불변, capability claim 0. **§108 is READY-TO-DISPATCH spec; dispatch decision = Q5 tree at §107 result land.**
