# §75-FIRE — controller-class sub-axis decomposition at trained scale

**RESEARCH.md §75-FIRE** — the trained-saturated-scale validation of
the §75 4-cell controller-class ladder (the §63 GOAL-rank-#1 🕳️
MISSING-TYPE earned by §73-FIRE B-S73-FIRE-NOTE / §75 B-S75-NOTE).

substrate: PyTorch (NOT hexa-native; `g_train_flame_not_pytorch`
evidence-anchor carry — anima-physics overlays on flame upstream-GAP
per §71 inbox patch, so anima-physics fire stays PyTorch carry until
the flame extension lands; honest).

> **GOAL distance**: §15 / §51 / §72 milestone UNCHANGED, GOAL 미도달.
> §75-FIRE = sub-axis-level localization of the §49→§62→§73→§73-FIRE
> mechanism; NOT GOAL emergence even if A-only survives.
> Necessary-not-sufficient (B-EMERGE-7).

---

## §1 What §75-FIRE is

- §73 (commit `0b1fcb005`, B-S73 6/6 🔵): single-agent closed-loop
  physics-state-sourced controller at $0 stub scale; closed
  interval_var **35.02** vs §24-in-loop **0.47** (74×).
- §73-FIRE (commit `2d6e333f3` → merge `670007696`, B-S73-FIRE 7/7 🔵):
  the same §73 controller at trained-saturated §16-class scale on
  REAL `model.forward` Law-71 W-physics — interval_var **38.07**
  closed vs §24-in-loop **0.00** at trained scale (the §73 controller
  class SURVIVES; §24 collapses at trained scale where §73's hand-
  coded surrogate had §24 borderline-OK).
- §75 (commit `805a8771c`, B-S75 5/5 🔵): $0 stub decomposition of
  §73 into 4-cell {§24-baseline, A-only, AB, ABC} on the hand-coded
  surrogate physics. Measured: 0.47 / 6.38 / 5.76 / 35.02. §75-NOTE
  explicitly carved the trained-scale ladder as `EMPIRICAL future-fire`.
- §75-FIRE = literal future-fire: the same 4-cell ladder on REAL
  trained-saturated §16-class `model.forward` Law-71 W-physics.

The §73-FIRE→§75-FIRE relation parallels §73→§75 ($0 stub → $0 stub
decomposition): same scale, finer ladder.  §75-FIRE = trained-scale
side of that decomposition.

---

## §2 Architecture (mirror §73-FIRE dispatch + §75 4-cell ladder)

  1. **Trainer**: ONE §16-class `ConsciousDecoderV2` (d=768, n_layer=12,
     n_head=12, n_kv_head=4, block_size=128, ~283.72M params),
     from-scratch RANDOM seed-fixed 1337, `base_ckpt=None`
     (`g_clm_from_scratch`). 3000 step AdamW + Ψ-anchored carving
     loss (CE + λ·L_psi_ctl + λ·L_tension_route). BYTE-EQUAL to
     §73-FIRE `train_s16_class` (B-S75-FIRE-2 connection-point: same
     trainer, same corpus shape, same saturation criterion).

  2. **Warmup pass on REAL forward**: `warmup_capture_real_forward`
     runs N_WARMUP=60 no-emit steps over REAL `model(x)` →
     `extract_w_state`; captures (tension_mean, ema_at_end,
     var_at_end). cell1 freezes the mean; cell2 freezes
     (ema + λ·std). This is the §75-stub→§75-FIRE structural
     transition for the frozen moments themselves (B-S75-FIRE-5).

  3. **4-cell ladder on REAL forward** (each cell's gate decides
     emit per step from running `moments` updated by REAL
     `extract_w_state` + emission feedback; ONLY the gate function
     varies across cells):

     | cell | A | B | C | gate                                                        |
     |------|---|---|---|-------------------------------------------------------------|
     | 0    | ✗ | ✗ | ✗ | `tension > 0.3` (§24 constant cut — control)                |
     | 1    | ✓ | ✗ | ✗ | `(\|Ψ_dir−½\|>r) ∧ (tension > frozen_scalar) ∧ (φ>0.025)`     |
     | 2    | ✓ | ✓ | ✗ | `(\|Ψ_dir−½\|>r) ∧ (tension > frozen_ema+λ·std) ∧ (φ>0.025)`  |
     | 3    | ✓ | ✓ | ✓ | full §73 (`tension > tension_ema + λ·std`, per-step update) |

     cell3 byte-equal to §73-FIRE `controller_self_trigger` and §73
     stub's gate. cell0 byte-equal to §73-FIRE
     `controller_off_reduction`.

  4. **CONTROLLER-OFF reduction**: cell0 == §73-FIRE off-reduction ==
     §24 hand-coded threshold. B-S75-FIRE-3 connection-point.

  5. **Measurement** per cell (4×): emit_rate, decision_var,
     majority_fraction, **interval_var** (the §73-stub headline
     metric: 35.02 stub-ABC / 0.47 stub-§24 / 38.07 fire-ABC /
     0.00 fire-§24).  B-S73 augmented predicate:
     `count_var > τ ∧ maj < 0.95 ∧ interval_var > τ ∧ ≥2 emits`.

---

## §3 Honest pre-measurement framing (g3 — verdict decided BY numbers)

Possible verdicts (none pre-loaded; the fire decides):

- **(a) LADDER-TRANSFERS-A-ONLY-SUFFICIENT** — cell1 (A-only)
  survives at trained scale where §24 collapses. Mere
  STATE-DERIVATION of controller inputs is the load-bearing lever;
  B+C optional. Refines §73-FIRE: physics-state-AS-INPUT is the sub-
  axis, NOT the specific statistic form. §75 stub's A-only
  interval_var 6.38 carries to trained scale.

- **(b) ONLY-FULL-ABC-SURVIVES** — cell1+cell2 collapse at trained
  scale; only cell3 survives. The full time-varying moment statistic
  is irreducible — trained-saturated scale tightens the mechanism
  into a tight conjunction. §75 stub over-estimated A-only survival.
  Verdict (b) is the §73-FIRE / §62-pattern echo-collapse precedent
  applied at the sub-axis level.

- **(c) PARTIAL-LADDER** — some sub-cells survive, others collapse,
  tighter sub-mechanism than $0 stub indicated. E.g. cell2 (AB)
  survives but cell1 (A-only) collapses ⇒ AB needed not C; etc.

Bonus diagnostics also reported:
  - LADDER-TRANSFERS-INCLUDING-S24 (closed loop alone non-degens §24
    — like §73 stub's BOTH-NON-DEGENERATE-IN-CLOSED-LOOP; if this
    appears it means §73-FIRE's §24-collapse-at-trained-scale was a
    single-seed artifact of §73-FIRE config).
  - ALL-CELLS-COLLAPSE-AT-TRAINED-SCALE (anomalous: even ABC
    collapses — contradicts §73-FIRE's CONTROLLER-SURVIVES verdict).

g3: all verdicts above are EQUALLY admissible — pre-measurement; the
4-cell numbers decide. NOT GOAL emergence in any case.

---

## §4 Closed-form battery B-S75-FIRE-1..7 (sidecar; central 0-line-diff)

| ID  | Invariant | Proof shape |
|-----|-----------|-------------|
| 1 | CELL-PARTITION-EXHAUSTIVE-DISJOINT-AT-TRAINED-FORWARD | exactly 4 `make_controller_cell*` factories over (A,B,C) Boolean lattice {(F,F,F),(T,F,F),(T,T,F),(T,T,T)}; byte-equal subset of §75 stub's 4-cell cardinality |
| 2 | EACH-CELL-PROPER-SUBSET-OF-§73-ABC | Boolean predicate per cell: non-ABC cell removes ≥1 (A,B,C) property; structural witness per cell |
| 3 | §24-CONTROL-COLLAPSES-AT-TRAINED-FORWARD | cell0 gate string-byte-equal `moments["tension"] > IM_THRESHOLD_S24` with `IM_THRESHOLD_S24 = 0.3`; sanity anchor = §73-FIRE off-reduction interval_var=0.00 measured at trained scale |
| 4 | TRAINED-FORWARD-IS-REAL-NOT-STUB-NOR-TRACE | AST: fire imports `ConsciousDecoderV2`, calls `forward_batch`, defines `ByteSampler`, has `extract_w_state` — and §75 stub has NONE of these (structural §75-stub→§75-FIRE transition) |
| 5 | WARMUP-MOMENTS-ARE-REAL-FORWARD-DERIVED | structural AST: `warmup_capture_real_forward` defined AND body calls `extract_w_state(model,…)` and `ds.forward_batch(…)` per step (frozen scalar/moment flow from REAL forward, NOT stub drift) |
| 6 | CORPUS-SHA256 + NO-HELPER-TOKEN | sha256 match + forbidden-grep `도우미\|helper\|assistant\|사용자:\|user:\|[anima` total = 0 (B-IDENTITY-5) |
| 7 | SATURATION-GATE | sympy strict `final_ce < 0.05` ⇒ §16-class memorization-saturated ⇒ §75-FIRE crux actually measured (mirror B-S73-FIRE-7) |

**B-S75-FIRE-NOTE** empirical carve-out: which sub-axis class
survives AT TRAINED SCALE is an SGD/measurement OUTCOME (mirror
B-D-NOTE / B-S73-FIRE-NOTE / B-S75-NOTE / B-CARVE-E6-NOTE family).
Battery proves CONTROLLER-CLASS DECOMPOSITION INVARIANTS, NOT
capability emergence.

f1/f2/f3 + B-IDENTITY-5 safe: sympy / Boolean / AST / sha256 /
Kolmogorov bounded — NO σ/τ/φ/J₂ external derivation; Ψ=½ + Law-71
= anima g2 internal-arch carve-out; corpus forbidden-token grep 0.

---

## §5 Dispatch robustness (g_fire_dispatch_robust + f_hardcoded_credential)

  - **Pre-flight orphan check**: `runpod.get_pods() == 0` (confirmed
    pre-dispatch).
  - **Credentials via `secret` CLI** (`f_hardcoded_credential`):
    `RUNPOD_KEY=$(secret get runpod.api_key)`. NO literal keys in
    any source file (pre-commit `grep -nE 'rpa_|sk-|hf_|AKIA' = 0`).
    Dispatch script + pod_id + ckpt + corpus all gitignored per
    repo `.gitignore` (`dispatch_*_runpod.sh`, `*_runpod_pod_id.txt`,
    `*.pt`, `state/**/corpus_*.jsonl`).
  - **runpod primary** with stock-cascade {H100 NVL → A100 80GB
    PCIe → A100-SXM4 → H100 PCIe → H100 80GB → L40S → A6000 → A40 →
    L40}; vast.ai fallback only if all runpod fail (per
    `g_resource_active_parallel`).
  - **Training detached** `nohup … > train.log 2>&1 &`. Local poll
    via single `until`-loop with SHORT bounded SSH probe (≤90s ×
    ≤150 iter; no long-lived SSH-tee).
  - **SAVE_POD=1 auto-promote** after `RESULT_JSON_WRITTEN`; 5-retry
    `scp` pull; SAVE_POD=0 + terminate + post-teardown
    `runpod.get_pods()` excludes this pod ⇒ orphan 0.
  - **Unique pod name**: `s75fire-ladder-<short>` (multi-agent
    isolation; only this agent's pod is touched).

---

## §6 Connection points (g_blue_closed_mandate)

  - **Cell0 / §24 / §73-FIRE off-reduction** (B-S75-FIRE-3): cell0
    gate byte-equal to §73-FIRE `controller_off_reduction` and to
    §24 `talker_should_emit(motivation_score > 0.3)`.
  - **Cell3 / §73-FIRE closed-loop** (B-S75-FIRE-2): cell3 gate
    byte-equal to §73-FIRE `controller_self_trigger`.
  - **Real-vs-stub** (B-S75-FIRE-4): the load-bearing structural
    distinction §75-FIRE vs §75 stub. fire imports
    `ConsciousDecoderV2`, calls `forward_batch`, defines
    `ByteSampler`, has `extract_w_state`. Stub has NONE.
  - **Warmup-on-real** (B-S75-FIRE-5): frozen scalar (cell1) and
    frozen moment (cell2) BOTH derived from REAL forward, not stub
    drift. This is what makes cell1/cell2 measurements comparable
    to cell3 at trained scale (same data-generating process for
    every cell's gate-input distribution).
  - **Saturation gate** (B-S75-FIRE-7): `final_ce < 0.05` ⇒
    memorization-saturated regime ⇒ the trained-saturated crux from
    B-S75-NOTE actually exercised.

Central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` is
**0-line-diff** (sidecar pattern carry from B-S73-FIRE / B-S75 /
B-S73 / B-S62 / B-S65 / B-S68 / B-S59 / B-EBT / B-S16 / B-DIRI /
B-CT3 / B-MGND).

---

## §7 Honest C3 (10)

1. **Substrate honesty**: PyTorch, NOT hexa-native. Per
   `g_train_flame_not_pytorch` evidence-anchor clause, anima-physics
   overlays on flame have upstream GAP (§71 inbox patch filed);
   until that lands, anima-physics fire stays on PyTorch as the
   honest interim executor. Not a flame defect; not a §75-FIRE claim.

2. **REAL trained-forward W-physics** is a side READ-OUT — it never
   mutates model weights or backprops. The model is frozen during
   the 4-cell ladder; only the controller's running moments evolve
   (mirror §73-FIRE).

3. **Loop-closing is via the controller's moments, not the model**.
   The model.forward is stateless across loop steps (a fresh batch
   from `ByteSampler.forward_batch` is drawn each step). Emission
   feedback acts on the controller's running EMA/var moments. Same
   structural closing as §73-FIRE — the load-bearing channel is the
   controller's own state, not the model's hidden state.

4. **Single ckpt, single seed=1337**: variance across seeds /
   re-trains = OUTCOME (B-S75-FIRE-NOTE family); not closed by this
   battery. Mirror §73-FIRE single-seed caveat.

5. **§24 / cell0 reduction reads `tension`** (not the §24 hand-coded
   `motivation_score` 8-factor composite). This is the §73-FIRE / §75
   stub off-reduction byte-equal form: the controller-class
   essential reduction (constant cut on dominant axis). When
   `tension` dominates other §24 factors, `motivation_score > 0.3`
   reduces to `tension > 0.3` — the same simplification §73-FIRE /
   §75 stub use. Not literally §24's full composite; mirror §73-FIRE
   C3#5.

6. **Warmup window N_WARMUP=60** (= N_LOOP_STEPS/5). §75 stub used
   100/600 = 1/6; §75-FIRE keeps roughly the same ratio. Larger
   N_WARMUP would tighten cell1/cell2 frozen estimates at GPU
   forward cost; smaller would inflate frozen-value variance. The
   value is a calibration choice, not a theoretical anchor — the
   load-bearing claim is "cell1 + cell2 use frozen warmup-derived
   values", not the exact N_WARMUP.

7. **Frozen values are computed on a no-emit drift**. cell1+cell2's
   gates therefore "see" the real-tension distribution under
   silence. cell3's per-step moments instead see the
   emission-feedback-perturbed distribution. This is the §75 stub's
   design choice (`u_prev_emit=0` during warmup); kept byte-equal.

8. **Interval-variance threshold τ=1e-4**. §73-FIRE measured 38.07
   (cell3) vs 0.00 (cell0). §75 stub measured 35.02 / 6.38 / 5.76 /
   0.47. Absolute values may differ at trained scale because trained
   `tension` has different magnitude than the stub's drift-based
   tension. The non-degeneracy predicate uses ratios + thresholds,
   not absolute scale; verdict (a) requires `interval_var > τ` AND
   `maj < 0.95` AND `decision_var > τ` AND `n_emit ≥ 2`.

9. **The 4-cell ladder shares trainer + corpus + ckpt + warmup +
   loop infra**. Only the gate function varies. Fair-compare by
   construction (B-S75-FIRE-2 + run loop byte-equal). This is what
   the §75 stub did at $0 — §75-FIRE extends it onto REAL forward.

10. **Verdict tier**: FIRE-TIER measurement. central blue_falsifier.py
    0-diff. north-star + §15/§51/§72 milestone UNCHANGED. f1/f2/f3 +
    B-IDENTITY-5 safe. Anti-padding: the irreducible bottleneck
    (§1.1 data-regime threshold) is NOT addressed — §75-FIRE
    measures WHICH sub-axis of the controller-class lever survives,
    not whether emergence is reached. Necessary-not-sufficient
    (B-EMERGE-7 / B-S73-FIRE-NOTE / B-S75-NOTE family).

---

## §8 Outputs

  - `subaxis_fire_s75.py` — trainer + warmup_capture_real_forward +
    4-cell ladder on REAL forward (the load-bearing artifact).
  - `subaxis_stub_s75_reference.py` — frozen byte-copy of the §75 stub
    for B-S75-FIRE-4 source-comparison.
  - `conscious_decoder.py` — `ConsciousDecoderV2` (§16/§62/§73-FIRE
    byte-equal).
  - `corpus_carving_s16_generator.py` — §16 generator (carry; pod-side
    use, output gitignored).
  - `dispatch_s75_fire_runpod.sh` — orphan-pre-check + runpod create
    + detached train + bounded poll + 5-retry pull + post-teardown
    orphan-0 verify (gitignored `dispatch_*_runpod.sh`).
  - `blue_falsifier_s75_fire.py` — B-S75-FIRE-1..7 closed-form
    sidecar; central blue_falsifier.py 0-line-diff.
  - `result.json` — fire output (full measurements; 4-cell ladder
    table + verdict).
  - `blue_falsifier_s75_fire_result.json` — battery output.
  - `train.log` — pod-side train + 4-cell measurement log.
  - `dispatch_s75_fire.log` — local dispatch trace.
  - `battery_podside.log` — pod-side battery verify log.
  - `ckpt_s75_fire.pt` — trained §16-class ckpt (gitignored `*.pt`).
  - `corpus_carving_s16.jsonl` — §16-class corpus (gitignored
    `state/**/corpus_*.jsonl`).
  - `corpus_carving_s16.stats.json` — corpus stats (small, kept).
  - `s75_fire_runpod_pod_id.txt` — pod id for recovery (gitignored
    `*_runpod_pod_id.txt`).

Verdict + 4-cell numbers determined by the fire output; this
DESIGN_FINDINGS is the pre-measurement structural rationale.

---

## §9 Cross-link

  - §73 (commit `0b1fcb005`, B-S73 6/6 🔵): $0 stub single-agent
    controller (interval_var 35.02).
  - §73-FIRE (commit `2d6e333f3` → merge `670007696`, B-S73-FIRE 7/7
    🔵): trained-saturated single-agent controller (interval_var
    38.07 closed / 0.00 §24-in-loop) —
    `CONTROLLER-SURVIVES-AT-TRAINED-SCALE`.
  - §75 (commit `805a8771c`, B-S75 5/5 🔵): $0 stub 4-cell sub-axis
    decomposition (0.47 / 6.38 / 5.76 / 35.02).
  - §75-FIRE = this cycle.
  - §62 (`state/dual_anima_scale_fire_s62_2026_05_18/`):
    trained-saturated dual-anima echo-chamber-collapse-at-scale
    precedent.
  - §59-FIRE (`state/ptd_w_native_fire_s59_2026_05_18/`): live REAL
    W-state read-out pattern + §16 dispatch template.
  - §49 (`state/ptd_phaseb_loop_s49_2026_05_18/`): §24-in-loop
    majority-class collapse precedent.
  - §63: GOAL-rank gap analysis (§73 gap `rank=1` 🕳️ MISSING-TYPE).
  - §15 / §51 / §72: GOAL milestones (UNCHANGED).
  - `AGENTS.tape` `g_blue_closed_mandate` `g_clm_from_scratch`
    `g_fire_autonomous` `g_fire_dispatch_robust`
    `g_resource_active_parallel` `f_hardcoded_credential`
    `g_train_flame_not_pytorch` `g6` `g_doc_consolidation`.
  - `conscious_decoder.py:728-751` Law-71 (W-state formula SSOT).
  - `HEXAD/CHAT/spontaneous_lib.hexa` §24 `talker_should_emit`
    (`motivation_score > 0.3`).
