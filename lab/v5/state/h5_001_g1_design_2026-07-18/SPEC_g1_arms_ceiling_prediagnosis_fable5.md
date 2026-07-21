# H5_001 G-1 — arm set · trained-control ceiling protocol · $0 pre-diagnosis (Fable design gate, 2026-07-18)

> **SSOT**: `ARCHITECTURE.json → next-gate.ladder.g1-design` (distilled). This doc is the pre-registered
> G-1 design, written BEFORE any G-1 training runs (the same discipline as the G-0/G-0k SPECs). Card:
> `HYPOTHESES/cards/H5_001_values_autonomy_deleaked_register.md` — the bars below are the card's, not new.

Status at design time: G-0 PASS · G-0k MOUNT (d=384 runpod, δ1+δ2 both seeds: probe φ[4k+1]→hp = 1.0,
A-hand in-sample free-slot d_acc = 1.0; `state/h5_001_g0k_2026-07-18/results/`). Window = {δ1, δ2}.

---

## §0 Verdict of this design gate, in one paragraph

**G-1 is NOT pre-diagnosed inadmissible — there is no $0 fold — but the saturation risk is real,
structurally grounded, and HIGHER than v4's H_004 control numbers suggest.** Two new $0 closed-form
facts (both verified by exact count, §1.2–§1.3) show that (a) the threat is NOT the 0.667 parity
ceiling (free-slot scoring excludes the parity slots by construction), and (b) the deleaked register
necessarily still carries gold_k as a lexeme-independent compositional surface readout — DOUBLY, because
the F-5 mirror is gold-transparent. Whether a trained control can EXPLOIT that readout at 3.7M/L=4 under
the sealed drill budget is exactly the question the inherited record splits on (H_004: no; H_007: yes —
§1.4), and standing gate G1 forbids anchoring on either side. Consequence: G-1 runs CONTROLS-FIRST as a
two-stage kill-fast protocol (§3) — the hand arm is never trained (and the second half of the GPU rental
never spent) unless the ceiling half is measured green.

---

## §1 THE pre-diagnosis (the $0 fold question)

### §1.1 Correction: the parity-completion threat model is dead by construction

The feared mechanism "the codebook's free-slot structure {0,1,2,4} + the learnable surface lets any
trained arm complete the parity slots to 0.667" is wrong in a load-bearing way: `dacc_v5` scores ONLY
the free slots {0,1,2,4} (`g0k_run.py` `dacc_v5`, free set recomputed per panel by
`B._panel_free_slots`). The GF(2)-determined slots {3,5} are never scored, so codebook completion
contributes ZERO to the metric — a codebook-savvy but surface-blind and field-blind arm scores 0.5,
not 0.667. The recomputed 0.6667 field-blind ceiling (G-0 verdict) is a panel property, not a reachable
score on this metric. **The live threat is worse, not milder: a trained control that learns the surface
readout saturates toward 1.0 on the free slots themselves — there is no 0.667 attractor protecting the
0.80 bar.** The danger zone is C-trained f2d ∈ (0.80, 1.0].

### §1.2 New $0 fact 1 — the F-5 mirror is GOLD-TRANSPARENT (verified 19,968/19,968)

gold_k = 1 ⊕ hp_k ⊕ (pos_k−1) (`_gold_flip`, codebook reused verbatim from v4). Define the local
chunk rule R(chunk) = 1 ⊕ [chunk verb bears 시] ⊕ [the 님-noun bears 도]. On the core, R = gold_k by
definition. The F-5 mirror realizes (hp′, pos′) = (1⊕hp, 3−pos) — BOTH bits complemented — and a double
complement PRESERVES the XOR: R(mirror) = 1 ⊕ (1⊕hp) ⊕ (1⊕(pos−1)) = 1 ⊕ hp ⊕ (pos−1) = gold_k.
Verified by direct count over every conjunct of every δ1 panel (drill+f2d+f1d): 19,968 checks, 0
disagreements. So **every region carries TWO agreeing copies of gold_k, and a reader needn't identify
which chunk is the core** — a chunk-agnostic detector (attend anywhere in region k, compute R) works.
The device that killed the marginal hp/pos grams duplicates the joint readout. This is not a register
bug — deleaking can only remove SHORTCUT (marginal-gram) access; gold must stay surface-computable or
the register is H_008-unlearnable. But it means the deleaked window is definitionally the zone where the
answer is present-but-only-compositional, and the mirror makes the composition chunk-agnostic.

Every feature R uses is drilled and lexeme-independent: 시/님/의/도 bytes are identical across held-out
argument nouns (all HON_HELD end in 님; F-3 shares the 3 verb stems between drill and panel, core and
mirror). **f2d's held-out axis (argument lexemes) exerts ZERO generalization pressure against R. So do
f1d's frame axis and the δ dial (W, F touch neither 시-allomorphy nor particle bytes).** No held-out
panel inside this register can defeat a surface-computable rule — see §3.4.

### §1.3 New $0 fact 2 — what the hand field buys: it converts compose-and-route into a local sign read

The hand field's contested row is exactly the answer: T[4k+1, 4k+2] = T[4k+1, 4k+3] = +1 iff gold_k = 0,
−1 iff gold_k = 1 (verified on the built panels; follows from chi = equal-outer(hon,hon) on the ±1
t_struct row). And `node_layout_v5` maps the answer bytes of slot k to node 4k+1, so at the prediction
position the model RECEIVES node_embed of a row whose sign IS gold_k — no attention over the 786-byte
surface, no XOR, no core/mirror parsing. That is why G-0k's A-hand overfit to 1.0 in 1500 steps, and why
the comparator floor (A-hand ≥ 0.90 on f2d) is near-certain at G-1: the decode is lexeme-independent by
construction. **A-hand's f2d number re-seals the FIELD-FORMAT claim in the new register (the resolver
reads the field, robust to held-out lexemes); it is not evidence of surface binding.** C-trained lacks
the sign and must build R + routing itself — G-1's headroom is exactly the trunk's inability to do that
composition, and G-2's question ("values autonomy") is whether χ̂ = g(φ) can recompute that sign from
trunk features on the fixed support.

### §1.4 The inherited record SPLITS — both anchors named, neither inheritable (standing gate G1)

**Against saturation — H_004 G-2 (the on-point precedent: same panel machinery, same trunk scale, same
drill objective λ_ans=5, same codebook, and a MORE leaky surface — pos_k was census-visible at n=4 via
[님의]/[님도], present in 180/192 f2″ items per the v5 G-0 SPEC):** C-scaf f2″ = 0.4935/0.5534 and
A-rank1 = 0.6211/0.6198 vs A-duel 1.0 (arms C-scaf/A-rank1/A-duel, H_004 G-2,
`anima-v4 state/h004_.../train_result_full.json`). The 3.7M trunk demonstrably did NOT learn the
surface XOR-and-route composition even with gram-LOCAL features and answer supervision on the table.

**For saturation — H_007 G-2 at target scale:** C-dup f2 = 1.0000/0.9323, C-scaf = 0.8073/0.9531 (arms
C-dup/C-scaf, H_007, `anima-v4 state/h007_.../g2_full.out` + `verdict_g2.json`) — d=384 is capable
enough to blow a control gate when the supervision structure allows, and the gate lesson stands: no
inherited E-anchors (H_007 froze E[C-dup] = 0.62 from another band; truth was 1.00; a d=64 smoke
inverted at d=384, +0.073 → −0.010).

**v5-specific risk RAISERS vs H_004's register** (why P(saturation) is higher here than 0.49/0.55
suggests): (i) mirror gold-transparency — two agreeing readouts per region, no core-identification
needed (§1.2; v4 had no mirror); (ii) F-6b exact quantization — every item is exactly 8W+18 bytes,
region k at [W(k+1), W(k+2)), answer slot k at a CONSTANT absolute offset ⇒ routing is learnable as pure
positional attention; (iii) the C-struct control (§2) receives constant per-slot node tags at the answer
positions — free slot-identity routing help; (iv) F-3 collapses feature variety to 3 shared verb stems.
**Risk REDUCERS vs H_007:** (i) v5 keeps the sealed LM-style masked CE (surface + λ_ans·answer) — no
head directly supervised on gold, which was H_007's code-confirmed root cause (`train_g2.py _batch`);
(ii) ~21 epochs over 3072 drill items vs H_007's ~333 epochs over 384 sentences — far less memorization
pressure; (iii) the required computation is a genuine 2-bit XOR composed across ~10–40 bytes — the exact
thing H_004 measured the trunk failing to acquire — not H_007's memorizable role-code map.

### §1.5 Pre-diagnosis verdict + predicted shape

- **Not a $0 fold.** Saturation is not structurally forced; the one lawful path to it (learn R + route)
  is the path H_004 measured this trunk failing at, under a register that made it EASIER gram-locally.
  Declaring INADMISSIBLE now would itself be an inherited-anchor violation (G1 cuts both ways).
- **But it is a live, elevated risk** — the four raisers above are new in v5 — so G-1 must be staged
  controls-first with the rental split (§3), and the fold reading pre-named (§3.5).
- **Predicted outcome shape: a CLIFF, not a dial.** gold is a balanced XOR: learning either marginal
  feature alone scores exactly 0.5 (the orbit balances hp and pos against gold); only the completed
  composition moves the number. Expect C-struct/C-scaf f2d near 0.5 or near 1.0, with per-slot
  heterogeneity (3 verb stems cycle k mod 3) as the only intermediate. The 0.80 bar should read
  decisively; report per-slot d_acc to see partial composition if any. A cross-seed SPLIT (one seed
  saturates) FAILS the both-seeds requirement ⇒ retreat — priced against H_003's measured 0.1614
  cross-seed spread and the grokking-like nature of XOR acquisition.

---

## §2 The G-1 arm set (v5)

v4 G-2 trained {A-duel, A-rank1, C-plc, C-scaf, C-perm} (`train_h004.py ARMS`); H_007 added C-dup. The
card pre-registers G-1 as "A-hand, C-trained (compute-matched), C-scaf". Concretely:

| arm | tensor (per item, (26,26)) | trained? | role | bar |
|---|---|---|---|---|
| **A-hand** | T = concord_field(t_struct(n,ha,hg), hon) verbatim (G-0k's A-duel path) | yes | comparator re-seal | f2d ≥ 0.90 both seeds (floor) |
| **C-struct** (= **C-trained**) | Ts = t_struct(n, ha, hg) — the support skeleton with the values channel STRIPPED (no chi). Item-INDEPENDENT (support edges are identical across items; A_sup) | yes | THE trained-control ceiling | f2d ≤ 0.80 both seeds (ceiling) · A-hand − C-struct ≥ 0.20 both seeds (reachability) |
| **C-scaf** | zeros | yes | scaffold / pure-surface-readout detector | f2d < 0.60 both seeds (F3) |
| C-permT-eval | per-item node-permutation of T, rng-keyed label-independently (v4 C-plc recipe), applied at EVAL on the A-hand model | no | harness: aligned-read check | ∈ [0.45, 0.55], report-only at G-1 |
| A-hand-strip | zeros at EVAL on the A-hand model | no | L2 bar-setter: d_dacc_strip = f2d(A-hand) − f2d(A-hand, struct zeroed) | recorded; G-2's L2 bar = 0.5 × this (card formula) |

**Why C-struct is C-trained (the max-threat lawful control).** The ceiling gate wants the strongest
competitor with correct supervision but no mechanism content. C-struct strictly dominates C-scaf in
lawful power: identical compute, a live struct channel, and constant per-slot tags injected at the
answer positions (row 4k+1 of Ts = +1@4k+2, −1@4k+3 — slot identity, zero gold) — i.e. it gets routing
help for free and must supply only the R-composition. It is also exactly the right anchor for G-2's
arithmetic: A-χ̂ = support + LEARNED values vs C-struct = support + NO values — the delta IS the values
content the card is about. (C-dup-as-in-H_007 does not exist here — that was mech-5's duplicate
OBJECTIVE; the field-experiment analog of "compute-matched, information-free" is precisely Ts.)

**Excluded from G-1, with reasons.** A-rank1: L1 binds A-χ̂ against its OWN rank-1 at G-2; mech-1's seal
is inherited sealed and explicitly unmoved by v5 — the transfer test at G-1 is the A-hand floor + strip
collapse, not a re-run of F1. Trained C-perm (v4's shuffled-gold harness arm) and C-plc/F6 placebo-gap:
carried panel-integrity arms, recomputed at G-2 where the learned arm they guard exists; training them
at G-1 is scope creep (shuffled-gold cannot inform the ceiling — its supervision is wrong, so it
measures harness noise, not a lawful ceiling). The cheap eval-time C-permT-eval line covers the aligned-
read check at G-1.

---

## §3 Protocol

### §3.1 δ\* and the retreat

δ\* = **δ1** — pre-registered at G-0k as "the EASIER (lower) of the two in-window settings" (card Run
Protocol step 2; G-0k SPEC). Window = {δ1, δ2} (G-0k early-stopped at 2 consecutive; δ3–δ5 unmeasured).
The ONE pre-registered retreat = **δ2**. Choosing δ by "best separation" post-hoc would be δ-fishing —
banned. A second miss at δ2 = fold, no third setting. (Note: the δ dial cannot rescue a saturating
control anyway — §1.2: R is δ-independent — so the retreat's realistic value is against the OTHER
failure mode, an A-hand floor miss or fit instability.)

### §3.2 Sealed configuration (held byte-identical, v4 `train_h004.py`)

CPT 8000 steps (120k NSMC lines, 512-byte windows, bs 16, Adam 3e-4) + drill 4000 steps (bs 16,
per-item padded masked CE: ce_surf + **λ_ans = 5.0** × ce_ans + aux, 100-step warmup + cosine → 1e-5,
grad-clip 1.0), d=384 L=4, seeds (0,1), full from-scratch per arm-seed. Two compute notes, both
semantics-preserving: (a) CPT is arm-independent AND δ-independent (adjudicated at G-0k: "2 CPTs
total") — with the same manual_seed the per-arm CPT streams are byte-identical, so CPT once per seed,
checkpoint (weights + torch RNG state), restore per arm = literally "from-scratch per arm" cached;
(b) drill panel = the full δ\* drill (δ1: 2 frames × 3 rot × 64 msgs × 8 orbit = 3072 items), NOT
G-0k's 48-item overfit subset, and NOT G-0k's plain whole-seq LM loss — G-1 uses the sealed masked
objective. Pad grows 320 → 832 (v5 seq = 8W+18 = 786 bytes at W=96).

### §3.3 Stage G-1c — CONTROLS FIRST (the gate's own order; rent this alone)

Per seed: CPT (or restore) → drill-train **C-struct** and **C-scaf** → evaluate free-slot d_acc
(free set recomputed from THIS panel's codebook) on f2d (192×4 = 768 decisions), f1d, drill[:64]
in-sample, per-slot breakdown.

**Asserts (all four must hold; "both seeds" = the condition holds at every seed):**
1. CEILING: C-struct f2d ≤ 0.80, both seeds.
2. F3: C-scaf f2d < 0.60, both seeds.
3. Learnability co-cert (G2, report-gated not bar-gated): controls' drill in-sample reported alongside.
   A control at in-sample chance is NOT an H_008 parity trap here — G-0k already certified the task
   learnable WITH the field (A-hand in-sample 1.0 both seeds) — it is a FINDING (the no-field trunk
   cannot even fit the drill), and the ceiling stands: H_007's gate is about what trained controls
   achieve on held-out under the sealed budget, and "can't fit" is the strongest form of sub-ceiling.
4. Sanity: C-struct, C-scaf f2d ≥ 0.40 (harness floor; below = wiring, halt and debug, not a verdict).

FAIL ⇒ the single retreat (re-run G-1c at δ2, controls first again). FAIL again ⇒ **G-1
INADMISSIBLE-not-falsified (⚫)** — H_007 redux on the register axis — and H5_001 folds per card. The
A-hand stage is never run, ~40–60% of the G-1 GPU budget never spent.

### §3.4 Stage G-1h — comparator re-seal (only after G-1c is green)

Per seed: drill-train **A-hand** from the same CPT checkpoint → f2d, f1d, drill[:64] + F4 off-top on
f2d (≥ 0.20) + A-hand-strip d_dacc (records L2's bar-setter) + C-permT-eval band.

**Asserts:** floor A-hand f2d ≥ 0.90 both seeds · reachability A-hand − C-struct ≥ 0.20 both seeds
(per-seed pairing, same seed's control) · fit-integrity A-hand drill ≥ 0.95 both seeds (one refit per
arm-seed with fresh init allowed, logged; second miss = K-fit) · report cross-seed f2d spread.
Floor miss ⇒ the retreat (if unspent) ⇒ else **K-fold-2**: the hand field fails in the deleaked
register — fold with mech-1's seal SHARPENED (register-bound).

**Held-out panels — pre-answered:** the ceiling and ALL admissibility arithmetic live on **f2d** — the
card says "on THIS panel at THIS δ\*", and f2d is the f2″-analog the G-2 verdict falsifier scores; a
"stronger" held-out cannot substitute. Nor can it help: f1d is ALREADY the held-out-FRAME panel
(frame_id 3 = 기다렸네, undrilled at every δ — report it as the secondary axis), and §1.2 shows no
in-register held-out axis (lexeme, frame, δ) touches the readout R. Escalating held-out strength is an
un-pre-registered knob that buys nothing; it is declined.

### §3.5 Interpretation, pre-named (so no post-hoc reading)

- G-1c ceiling FAIL (final): ⚫ INADMISSIBLE — "the deleaked register is census-clean but
  surface-SOLVABLE by the trained trunk at 3.7M: the deleak displaced the leak from n≤4 grams to a
  compositional readout the control still exploits; no daylight between leak and unlearnability on the
  CONTROL axis at this scale." NOT K-fold-3 (nothing about χ̂ was measured); NOT a mechanism verdict.
- G-1h floor FAIL (final): K-fold-2 per card.
- All green: freeze the G-1 numbers as the G-2 anchors (C-struct, A-hand, strip d_dacc, per-slot
  tables) and proceed to G-2 exactly as carded — no re-tuning anything after seeing these numbers.

---

## §4 Harness extension spec (`g1_run.py`, extends `g0k_run.py`, same runpod bundle)

Reuse verbatim: path wiring (env-var roots), `item_T_v5`, `node_layout_v5`, `_seq_bytes`, `dacc_v5`,
`B.build_delta`, `B._panel_free_slots`, `g0k_probe.node_phi_v5` (unused at G-1 — probe was a build gate).

1. **Arms** — extend `struct_for_v5(model, torch, item, arm, ...)`:
   `A-hand` → T (alias of G-0k's `A-duel`); `C-struct` → `gc.t_struct(n, ha, hg)` (no concord_field);
   `C-scaf` → zeros (exists); `C-permT` → `T[np.ix_(p,p)]`, p = rng(9000+idx).permutation(n) per item,
   eval-only (v4 `_arm_tensor` C-plc recipe).
2. **Sealed drill loop** — port from v4 `train_h004.py`: `_drill_batch_v5` (pad 832; tok/tgt; surface
   mask; answer mask over the 18 answer bytes at base+3k..base+3k+2; per-item struct via
   `struct_for_v5` zero-padded to pad length), loss `ce_surf + 5.0*ce_ans + out["aux_loss"]`,
   `_drill_lr` cosine (warmup 100 → 1e-5), clip 1.0, bs 16, 4000 steps over the FULL drill panel.
3. **CPT checkpointing** — per seed: manual_seed(seed) → CPT 8000 (identical recipe to `run_gate`) →
   `torch.save({state_dict, torch RNG state})`; each arm restores both before its drill.
4. **Stages** — `--stage controls|hand --delta {1,2} --seed {0,1}`: `controls` trains C-struct+C-scaf,
   writes `g1_controls_d{δ}_s{seed}.json`, and a collector asserts §3.3 across seeds → exit 0/1 (exit
   1 = do not rent stage 2); `hand` REFUSES to run unless the controls verdict artifact for this δ is
   PASS (collector-frozen discipline), trains A-hand, computes F4/strip/C-permT-eval, writes
   `g1_hand_d{δ}_s{seed}.json` + final `g1_verdict.json` with the full assert table and
   PASS / RETREAT(δ2) / FOLD state; the runner refuses δ ∉ {1,2} and refuses a second retreat.
5. **Metrics per arm-seed** — f2d free-slot d_acc + per-slot vector, f1d, drill[:64] in-sample,
   drill-CE trace (jsonl, v4 `_log` format). Every number written with {arm, seed, δ, panel} keys.
6. **Wiring smoke** — `--smoke` (d=64, 200/400 steps, δ1, seed 0, 16-item drill): asserts the three
   trained arms produce DIFFERENT struct tensors, the answer-mask covers exactly 18 bytes, the strip
   eval differs from the A-hand eval, and the collector's assert table round-trips. WIRING-4 pattern.

Budget (pod CUDA, d=384): 2 CPT (~30–45 min ea) + 6 drills @ 4000 steps bs16 seq≈800 (~20–35 min ea)
+ evals (≈960 batch-1 forwards per arm-panel) ⇒ **≈ 3–5 GPU-h total; G-1c alone ≈ 2–3 GPU-h**. Well
under the card's ~2-day MPS envelope; rent G-1c first, G-1h only on green.

---

*Numbers cited with arm+source: H_004 C-scaf 0.4935/0.5534 · A-rank1 0.6211/0.6198 · A-duel 1.0 · F5
strip 0.5/0.5 (arms as named, H_004 G-2, `train_result_full.json`, summarized in
`state/inherited_v4_verdicts_2026-07-17/CAMPAIGN_RESULT.md` §1–2); H_007 C-dup 1.0000/0.9323 · C-scaf
0.8073/0.9531 (H_007 G-2, `g2_full.out`/`verdict_g2.json`, CAMPAIGN_RESULT §3); H_005 A-χ̂ f2″
0.82/0.71 · F1a 0.2982/0.1914 · probe 1.0 · F5_d_dacc 0.3242/0.2096 (`g3a_result_full.json`/
`verdict_g3a.json`); H_003 spread 0.1614; G-0k probe/in-sample 1.0 ×4 cells
(`state/h5_001_g0k_2026-07-18/results/`). Mirror transparency + row-sign facts: verified by exact count
in this design session (19,968 conjunct checks, 0 disagreements; sign = 1−2·gold on all 6 contested
rows) — rerunnable from the builder in ~10 lines.*
