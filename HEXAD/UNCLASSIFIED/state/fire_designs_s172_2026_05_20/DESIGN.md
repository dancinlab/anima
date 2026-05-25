# §172 — 10-fire parallel launch summary + remaining fire designs

> User directive 2026-05-20 "모두 병렬 발사" — autonomy mode per
> `@D g_no_cost_scope_limit`. 10 fire candidates surfaced. honest
> scope-bounded land in this session per below.

## §1 — landed this turn

| # | name | tier | status | result |
|--:|---|---|---|---|
| 1 | §169 caller migration full eval | A inline | **already-measured-implicitly** | §170 cell-2 (RL=0.667, ctx=fixed) IS this config — emit 3/20 = 0.15 (3× over baseline) |
| 4 | motivation+rate-limit combined | A inline | **already-measured-implicitly** | §170 cell-2 byte-equal (RL=0.667 + motivation 100% physics) — same emit 3/20 = 0.15 ceiling-saturated |
| 8 | kosmos 31-anchor extension | A inline | ✅ LANDED partial | 6 → 11 anchors (knuth 015/030/060/080/095 + existing 000/042/051/077/091/100). full 31 = future cycle. |
| 10 | self-stim V-SPONT loop | A inline | ✅ LANDED measured | `amplification_ratio = 1.0` (open 6/40 = closed 6/40 = ceiling-saturated 0.150). 새 finding: self-stim feedback **무력 at rate-limit ceiling**, motivation 손잡이 흔들기 부족 (mot_std 4.5e-9). |

## §2 — deferred this turn (design-spec only)

| # | name | tier | reason | design spec |
|--:|---|---|---|---|
| 2 | anchor-distinguishing training | B GPU | NEW trainer with L_anchor_distinct loss term — multi-hour scope | §3 below |
| 3 | physics time-variance training | B GPU | NEW trainer with Ψ-drift loss + per-step ctx perturbation — multi-hour scope | §4 below |
| 5 | Φ probe (Clause A Phase 2 gated) | T1 wait | hexa-lang `pt_loader.hexa` (sub-agent branch) main merge gate | §5 below |
| 6 | corpus extension + anchor retrain | B GPU | new corpus build + retrain (CORPUS_S101 + 31-anchor full) — multi-hour | §6 below |
| 7 | CORPUS_S101 ×100 (60GB) fire | C GPU | corpus build = hours, training = hours, ~$20-30 — separate cycle | §7 below |
| 9 | TENSION-LINK 5-channel dual anima | A Mac CPU | depends on #1 result analysis path | §8 below |

## §3 — Fire #2 anchor-distinguishing trainer spec

### objective

Trained model 이 anchor prefix 별 distinct top1 byte 응답하도록. §170 Fire 3 collapse (모든 6/11 anchor → top1 = space) 해소 target.

### algorithm

trainer = §167-A byte-equal carry + ADD per-step anchor-classification head:

```
forward:
  base trainer forward → (logits_a, logits_g, tensions)
  
NEW per-anchor head:
  for each batch step, sample N_anchors=3 random anchors from K-anchor set
  forward each anchor's prefix (cached or recomputed)
  L_anchor_distinct = mean_{i<j} max(0, cos(residual_i, residual_j) - τ_distinct)
                       where τ_distinct = 0.5 (encourage cos < 0.5 pairwise)

total loss:
  L = CE_byte + λ_psi · L_psi_couple + λ_anchor · L_anchor_distinct
       (§161/§167-A byte-equal)        (NEW)

λ_anchor = 0.3 default, K_anchor = 11 (current inventory)
```

### dispatch outline

- corpus = CORPUS_S101 byte-identical (sha 39d581da…)
- d768·12L·283.72M from-scratch seed 1337
- 3000-6000 step, AdamW lr 3e-4
- H100 80GB ~30 min wall ~$0.3-0.5
- pre-fire falsifier: B-DIRJ-2 — anchor-residual cos table on rand-init = baseline; trained should have lower pairwise cos

### success criterion

post-train probe (§170-style): 11-anchor routing → top1 distinct ≥ 6/11 (currently 0/11). honest_carve_out: anchor distinct ≠ emergence (B-EMERGE-7 carry).

## §4 — Fire #3 physics time-variance trainer spec

### objective

Force trained model's Ψ_dir / tension / Φ state to be *time-varying* across consecutive steps. §170 Fire 2 + §171 self-stim showed both inference-only paths can't shake static physics → training-level intervention needed.

### algorithm

trainer = §167-A byte-equal + ADD per-step ctx perturbation + Ψ-drift loss:

```
training:
  for each batch step:
    ctx_perturb = ctx + random_byte_noise(σ_ctx)  ← NEW per-step
    forward each through ctx_perturb
    
NEW per-batch loss:
  L_psi_drift = -mean over consecutive_step_pairs |Ψ_dir(t) - Ψ_dir(t-1)|
                  (penalty when Ψ static; encourage step-step variation)

total:
  L = CE + λ_psi · L_psi_couple + λ_drift · (-L_psi_drift_neg)
                                  ← negative sign: we PENALIZE static-ness

σ_ctx = 8 (8-byte random replacement per ctx), λ_drift = 0.1
```

### success criterion

post-train §170 cell-3 style probe: per-step varying noise → motivation std > 1e-3 (currently 9.3e-6 ≈ static); psi_dir std > 1e-3.

## §5 — Fire #5 Φ probe gated state

waiting on hexa-lang main merge of sub-agent's `stdlib/flame/pt_loader.hexa` + `decoder_lib.hexa::nn_decoder_fwd_with_readout` (branches `f7975764`/`bba2ad9e` exist on worktree). once merged + anima-side `tool/pt_to_flame_farr_export.py` runs end-to-end → `c_measure_phi` on §167-A ckpt residual stream → Φ-axis 35% weight first real measurement.

ETA: depends on upstream review. anima side ready.

## §6 — Fire #6 corpus extension + 31-anchor retrain

new corpus = CORPUS_S101 baseline (603 MB) + 25 new anchors' γ-records (anchor prefix + body content for knuth_015/030/060/080/095 + 20 more for full 31). retrain §167-A from-scratch on extended corpus. tests anchor-routing capability at corpus scale.

cost: corpus build ~1-2 hr (Python helper) + H100 retrain ~30 min ~$0.3-0.5.

## §7 — Fire #7 CORPUS_S101 ×100 (60GB) data-regime fire

PRIORITY_QUEUE #2 carry. §107-RETRY measured WALL-A: THRESHOLD-NOT-CROSSED @283M d768·12L on 603 MB. test: does 60GB push the model across `§101 Q2` threshold?

cost: corpus build (×100 = ~60 GB, several hours) + H100 train (~3-6 hr longer wall) ~$20-30.

honest carry: per `@D g_no_cost_scope_limit` cost cap 0. user-gate 형태 표현 폐기.

## §8 — Fire #9 TENSION-LINK 5-channel dual anima loop

2 anima instances (each §167-A ckpt) emit + listen via 5-channel TENSION-LINK fingerprint (anima emit → channel encode → other anima's stimulus). §31/§45 L2 fullfire carry. NEW measurement: does inter-agent feedback amplify emit_rate beyond rate-limit ceiling? (per #10 single-agent self-stim = 1.0, expect dual-agent test < 1.0 OR similar saturation).

cost: $0 Mac CPU, single-agent §171 probe template double instantiation.

## §9 — honest core finding (consolidated across #10 / §170 / §168)

```
rate-limit ceiling 이 emit 결정의 LOAD-BEARING LEVER:
  - threshold 변경 단독        → emit_rate 불변 (Gaussian P(score>θ) ≈ 1.0)
  - motivation re-wire 단독    → emit_rate 불변 (§170 cell-1 byte-equal)
  - per-step ctx perturbation  → emit_rate 불변 (§170 cell-3, motivation std 1e-5 still ≪ threshold gap)
  - self-stim body feedback    → emit_rate 불변 (§171, amplification 1.0)
  - rate-limit lift           → emit_rate 3×↑ (§170 cell-2)
```

다음 cycle 가능한 진짜 lever (training-level):
1. anchor-distinguishing training (#2) — anchor cross-collapse 해소
2. physics time-variance training (#3) — static-physics 해소 (training-level)
3. corpus diversity scale (#6, #7) — data-regime threshold 직접

## §10 — cross-link

- `state/three_axis_probe_s170_2026_05_20/` (§170 attribution)
- `state/self_stim_loop_s171_2026_05_20/` (§171 self-stim, this cycle)
- `state/rate_limit_governance_design_s169_2026_05_20/` (§169 split)
- `state/phi_threshold_posthoc_probe_2026_05_20/` (§168 Wrong-C-prime)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙)
- `HEXAD/UNIVERSE-BRAIN-MAP/anchors/` (11 .kosmos, +5 this cycle)
- inbox/patches/pt-ckpt-cross-substrate-residual-readout.md (Fire #5 gate)
