# §73-FIRE — THINKER→TALKER self-triggered closed-loop controller at trained scale

**RESEARCH.md §73-FIRE** — the trained-saturated-scale validation of the
§73 controller (the §63 GOAL-rank-#1 🕳️ MISSING-TYPE: "self-triggered
emission-decision controller (closed-loop control)" earned as
**B-S73-NOTE future-fire** by the §73 stub commit `0b1fcb005`).

substrate: PyTorch (NOT hexa-native; `g_train_flame_not_pytorch`
evidence-anchor carry — anima-physics overlays on flame upstream-GAP
per §71 inbox patch, so anima-physics fire stays PyTorch carry until
the flame extension lands; honest).

> **GOAL distance**: §15 / §51 / §72 milestone UNCHANGED, GOAL 미도달.
> §73-FIRE = §63 #1-gap controller's trained-scale validation, NOT
> GOAL emergence even if it survives. Necessary-not-sufficient
> (mirror B-EMERGE-7). Capability claim 0.

---

## §1 What §73-FIRE is

§73 (commit `0b1fcb005`) built the **§63 gap_rank=1** controller at $0
on a hand-coded Law-71 *surrogate* physics:

  - state moment-based gate (NOT a constant cut, B-S73-1)
  - feedback closes via emission ↦ tension-release (B-S73-2)
  - 4-AND non-degeneracy predicate (count-var ∧ maj-frac ∧ interval-var
    ∧ ≥2 emits — B-S73-3 augmented)
  - CONTROLLER-OFF reduces to §24's constant `tension > 0.3`
    byte-equal connection-point (B-S73-5)
  - measured at $0 stub: closed interval_var **35.02** vs
    §24-in-loop **0.47** (74× separation), open-loop emit_rate
    **0.862** (degenerate when feedback severed).
  - **B-S73-NOTE** explicitly flagged trained-saturated scale as
    `EMPIRICAL future-fire` with §62-like collapse as the
    pre-measurement expectation.

§73-FIRE = literal future-fire (§61→§62 pattern mirror: $0 smoke →
trained-scale fire on the §73 controller).

---

## §2 Architecture (mirror §62 dispatch + §16 trainer + §59 fire pattern)

  1. **Trainer**: ONE §16-class `ConsciousDecoderV2` (d=768, n_layer=12,
     n_head=12, n_kv_head=4, block_size=128, ~283.72M params),
     from-scratch RANDOM seed-fixed 1337, `base_ckpt=None`
     (`g_clm_from_scratch`). 3000 step AdamW + Ψ-anchored carving loss
     (CE + λ·L_psi_ctl + λ·L_tension_route) — §16 / §62 byte-equivalent.
     Corpus: §16-class Ψ-anchored carving (n=90,000 records, ~65MB —
     reduced honest, load-bearing variable is the REAL forward, NOT
     corpus size; `trained_saturated` gate: final CE < **0.05**
     B-S73-FIRE-7).

  2. **Controller**: byte-equal port of `selftrigger_stub_s73_reference.
     py::controller_self_trigger` predicate on REAL `model.forward`
     Law-71 W-state, extracted via `extract_w_state(model, x)` —
     conscious_decoder.py:735-750 byte-equal formulas:
        Ψ_dir   = (1 + cos(logits_a[-1], logits_g[-1])) / 2
        Ψ_ent   = − Σ p·log p / log V
        Ψ_tens  = max(0, 1 − std/mean of per-layer tension)
        tension = mean per-layer tension
        Φ★      = (std/|mean|) · log(L+1) clamped

  3. **Loop closure** (load-bearing structural change vs §73 stub):
     each step the controller's **running moments** (`tension_ema`,
     `tension_var` — the moments the gate actually reads) are updated
     by BOTH (a) the REAL extracted W-state AND (b) the previous
     emission decision.
       - emit=1 ⇒ tension RELEASE + Ψ_dir pulled toward Ψ_vac=½ (§73
         stub byte-equal)
       - emit=0 ⇒ moments accumulate the raw real physics
     **SEVER-FEEDBACK control** forces u_prev=0 always ⇒ moments
     never see the emission ⇒ open-loop replay shape.

  4. **CONTROLLER-OFF reduction**: `controller_off_reduction` = §24's
     hand-coded `tension > IM_THRESHOLD_S24` (= 0.3, byte-equal to §24
     `motivation_score > 0.3` in `spontaneous_lib.hexa`). B-S73-FIRE-4
     connection-point.

  5. **Measurement**: 3-arm
       (A) CLOSED §73-controller (the headline)
       (B) SEVER-FEEDBACK §73-controller (open-loop replay analogue —
           must reproduce stub's 0.862 emit_rate to prove closing is
           structurally load-bearing)
       (C) CONTROLLER-OFF (§24 in-loop — must reproduce
           majority-class degenerate behaviour to prove §73 is
           distinct from §24 even on real forward)

  4-axis numbers per arm: emit_rate, decision_var, majority_fraction,
  interval_var (the §73-stub headline metric — 35.02 vs 0.47 reference).

---

## §3 Honest pre-measurement framing (g3 — verdict decided BY numbers)

Possible verdicts:

  - **(a) CONTROLLER-SURVIVES-AT-TRAINED-SCALE** — non-degenerate
    closed-loop + §24-in-loop degenerate (= mirror §49 collapse) +
    SEVER-FEEDBACK degenerate (= mirror §73-stub 0.862). Genuine
    surprise; flag with strong caution. NOT GOAL emergence.

  - **(b) ECHO-CHAMBER-COLLAPSE-AT-CONTROLLER-LEVEL** — §73 controller
    collapses on REAL trained-saturated forward (mirror §62 echo-
    chamber-collapse-at-scale; §49 attractor reasserted at the
    controller class level). The §73-stub non-degeneracy was the
    hand-coded surrogate artifact predicted by B-S73-NOTE. Honest
    negative, VALUABLE.

  - **(c) PARTIAL** — one predicate holds, the other does not; one
    reduction reproduces target, the other does not.

The §49 → §62 → §73 progression measured at trained scale is the
contribution. Whichever verdict the numbers give, this is **step-5 of
a necessary-not-sufficient chain** — NOT GOAL emergence even if (a).

---

## §4 Closed-form battery B-S73-FIRE-1..7 (sidecar; central 0-line-diff)

| ID  | Invariant | Proof shape |
|-----|-----------|-------------|
| 1 | PHYSICS-DERIVED-GATE-AT-TRAINED-FORWARD | sympy: gate RHS = `tension_ema + LAMBDA_STD·sqrt(var)` ⇒ d/d(state moment) ≠ 0 ⇒ NOT constant cut |
| 2 | LOOP-IS-CLOSED-NOT-OPEN-AT-TRAINED-FORWARD | sympy piecewise + AST: emit=1 branch mutates next-EMA distinct from emit=0; SEVER path forces emit=0 |
| 3 | SELF-TRIGGER-NONDEGENERACY-PREDICATE | 4-AND truth table over (count_var>τ, maj<0.95, interval_var>τ, n_emit≥2) — only (T,T,T,T) returns True |
| 4 | CONTROLLER-OFF-REDUCTION = §24-BYTE-EQUAL | AST + regex: `tension > IM_THRESHOLD_S24` with `IM_THRESHOLD_S24 = 0.3` byte-equal between fire and stub |
| 5 | TRAINED-FORWARD-IS-REAL-NOT-TRACE-SHAPE | AST: fire imports `ConsciousDecoderV2`, calls `model(x)` via `extract_w_state` on `ByteSampler.forward_batch`; stub has none of these — provably the §73-stub→§73-FIRE structural transition |
| 6 | CORPUS-SHA256 + NO-HELPER-TOKEN | sha256 match + forbidden-grep `도우미\|helper\|assistant\|사용자:\|user:\|[anima` total = 0 (B-IDENTITY-5) |
| 7 | SATURATION-GATE | sympy strict `final_ce < 0.05` ⇒ §16-class memorization-saturated (§16.6-C) ⇒ §73-FIRE crux actually measured |

**B-S73-FIRE-NOTE** empirical carve-out: controller-survives-vs-collapse
OUTCOME at REAL trained scale is SGD/measurement OUTCOME (mirror
B-D-NOTE / B-S62-NOTE / B-S73-NOTE family) — battery proves CONTROLLER-
CLASS INVARIANTS, NOT capability emergence.

f1/f2/f3 + B-IDENTITY-5 safe: Boolean / sympy ∂-sign / AST / sha256 /
strict-inequality / Kolmogorov bounded — NO σ/τ/φ/J₂ external
derivation; Ψ=½ = anima g2 internal-arch carve-out; corpus forbidden-
token grep 0.

---

## §5 Dispatch robustness (g_fire_dispatch_robust + f_hardcoded_credential)

  - **Pre-flight orphan check** ran: `runpod.get_pods()` = 0 (no stray
    pods from prior attempts).
  - **Credentials via `secret` CLI** (`f_hardcoded_credential`):
    `RUNPOD_KEY=$(secret get runpod.api_key)`. No literal keys in any
    source file (pre-commit grep `rpa_|sk-|hf_[A-Za-z0-9]|AKIA` = 0).
    Dispatch script gitignored (`dispatch_*_runpod.sh` pattern).
  - **runpod primary** with stock-cascade {A100 80GB PCIe → A100-SXM4
    → H100 PCIe → H100 80GB → H100 NVL → L40S → A6000 → A40 → L40} —
    actual provisioning: **H100 NVL** (A100 stock exhausted; runpod
    primary fallback policy per `g_resource_active_parallel`).
    No vast.ai key available, runpod-only.
  - **Training detached** `nohup ... > train.log 2>&1 &`. Local poll
    via single `until`-loop with SHORT `ssh` probe (90s × ≤150 iter,
    no long-lived SSH-tee).
  - **SAVE_POD=1 auto-promote** after `RESULT_JSON_WRITTEN`, 5-retry
    `scp` pull; SAVE_POD=0 + terminate + `runpod.get_pods()` includes
    confirmation that this pod is gone.
  - **Unique pod name**: `s73fire-selftrig-trained-<short>`
    (multi-agent isolation; only this agent's pod is touched).

---

## §6 Connection points (g_blue_closed_mandate)

  - **Controller-off / §24** (B-S73-FIRE-4): `controller_off_reduction`
    source is byte-equal to §73-stub `controller_off_reduction` and
    both use `tension > 0.3` constant cut — identical to §24
    `talker_should_emit(motivation_score > 0.3)`.
  - **Sever-feedback / §73-stub open-loop** (B-S73-FIRE-2): when
    `feedback_closed=False`, `u_for_next = 0` always ⇒ moments never
    see emission — the same structural form §73-stub `run_loop`
    uses for `feedback_closed=False`.
  - **Real-vs-trace** (B-S73-FIRE-5): the load-bearing structural
    distinction of §73-FIRE vs §73-stub — extract_w_state calls
    `model(x)` on real `ByteSampler.forward_batch`, NOT a recorded
    array; the stub has zero `import torch` and zero `model(`.
  - **Saturation gate** (B-S73-FIRE-7): final CE < 0.05 ⇒ §16-class
    memorization-saturated regime (§16.6-C anchor) ⇒ the trained-
    saturated crux from B-S73-NOTE was actually exercised.

Central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` is
**0-line-diff** (sidecar pattern carry from B-S73 / B-S62 / B-S65 /
B-S68 / B-S59 / B-EBT / B-S16 / B-DIRI / B-CT3 / B-MGND etc.).

---

## §7 Honest C3 (10)

1. **Substrate honesty**: PyTorch, NOT hexa-native. Per
   `g_train_flame_not_pytorch` evidence-anchor clause, anima-physics
   overlays on flame have an upstream GAP (§71 inbox patch filed);
   until that lands, anima-physics fire stays on PyTorch as the
   honest interim executor. Not a flame defect; not a §73-FIRE claim.

2. **REAL trained-forward W-physics** is a side READ-OUT — it never
   touches LM weights or autograd graph (RNG-isolated, `model.eval()`
   under `@torch.no_grad()`; restore RNG and `model.train()` after).
   No capability claim.

3. **Corpus scale reduced honestly**: §16 SSOT is ~600MB / ~850k
   records / 6000 steps. §73-FIRE's load-bearing variable is the REAL
   forward (NOT corpus size); reduced for cost/wall while keeping the
   ckpt trained-saturated (final_CE<0.05 gate, B-S73-FIRE-7).

4. **Controller class generalisation**: §73-FIRE measures ONE
   controller (the §73 stub byte-equal port). If verdict (a)
   survives, this is a single-ckpt single-controller single-seed
   datapoint — not a class-level emergence claim. B-S73-FIRE-NOTE.

5. **OFF-reduction byte-equal to §24** but **§24 talker_should_emit
   in `spontaneous_lib.hexa` uses `motivation_score`** (a composite
   8-factor scalar). The fire's OFF-reduction uses `tension` directly
   (the same load-bearing scalar the §73 controller also reads). This
   is the §73-stub `controller_off_reduction` byte-equal pattern; it
   reduces the §24-class structure to its essential form (constant
   cut on the dominant axis), but is not literally §24's full
   composite — `motivation_score` reduces to this when `tension`
   dominates other factors, the same simplification §73-stub uses.

6. **Sever-feedback ≠ truly open-loop on real forward**. The fresh
   `ByteSampler.forward_batch` calls draw independent random
   windows, so the REAL extracted tension already has natural
   inter-step variation. SEVER-FEEDBACK isolates whether the
   emission feedback contributes ON TOP of that natural variation —
   the §73 stub didn't have this because the stub's `physics_step`
   was hand-coded with controlled rng. Verdict (a) at REAL forward
   is therefore a STRONGER claim than verdict (a) at stub scale.

7. **`feedback_closed=False` ≠ `link DISABLED` of §62**. SEVER-
   FEEDBACK only removes the emission's effect on moments; the
   controller still reads REAL forward. §62's `link_enabled=False`
   removed the cross-cell fingerprint coupling. Different structural
   levers — not interchangeable.

8. **Interval-variance threshold τ=1e-4**. The §73-stub had 35.02 vs
   0.47 — both ≫ τ but distinguished by 74×. At REAL trained scale,
   absolute interval_var values may differ in scale because trained
   tension has different magnitude than the §73-stub's drift-based
   tension. The non-degeneracy predicate uses ratios + variance, not
   absolute scale; verdict (a) requires `interval_var > τ` AND the
   controller class to be distinct from §24-in-loop.

9. **No multi-seed**: single seed=1337 (matches §62 / §16). Variance
   across seeds is an empirical OUTCOME (B-S73-FIRE-NOTE family) —
   not closed by this battery.

10. **Verdict tier**: FIRE-TIER measurement. central blue_falsifier.py
    0-diff. north-star + §15/§51/§72 unchanged. f1/f2/f3 + B-IDENTITY-5
    safe (no σ/τ/φ/J₂; Ψ=½ + Law-71 = anima g2 internal-arch carve-out;
    corpus forbidden-token grep 0). Anti-padding: the irreducible
    bottleneck (§1.1 data-regime threshold) is NOT addressed —
    §73-FIRE is a controller-class validity measurement.

---

## §8 Outputs

  - `selftrigger_fire_s73.py` — the trainer + controller-on-real-
    forward runner (the load-bearing artifact).
  - `selftrigger_stub_s73_reference.py` — frozen byte-copy of the
    §73-stub for B-S73-FIRE-4/5 source-comparison closed-form.
  - `conscious_decoder.py` — `ConsciousDecoderV2` (§16/§62 byte-equal).
  - `corpus_carving_s16_generator.py` — §16 generator (carry).
  - `dispatch_s73_fire_runpod.sh` — orphan-pre-check + runpod create
    + detached train + bounded poll + 5-retry pull + post-teardown
    orphan-0 verify.
  - `blue_falsifier_s73_fire.py` — B-S73-FIRE-1..7 closed-form
    sidecar; central blue_falsifier.py 0-line-diff.
  - `result.json` — fire output (full measurements).
  - `blue_falsifier_s73_fire_result.json` — battery output.
  - `train.log` — pod-side train + measurement log.
  - `dispatch_s73_fire.log` — local dispatch trace.
  - `ckpt_s73_fire.pt` — trained §16-class ckpt (gitignored `*.pt`).
  - `battery_podside.log` — pod-side battery verify log.
  - `corpus_carving_s16.jsonl` + `.stats.json` — corpus
    (gitignored — large; sha256 recorded in result.json).
  - `s73_fire_pod_id.txt` — pod id for recovery (gitignored
    `*_pod_id.txt`).

Verdict + numbers are determined by the fire output; this
DESIGN_FINDINGS is the pre-measurement structural rationale.

---

## §9 Cross-link

  - §73 (commit `0b1fcb005`, B-S73 6/6 🔵, `state/thinker_talker_
    selftrigger_s73_2026_05_19/`): the $0 stub + B-S73-NOTE future-
    fire earner.
  - §62 (`state/dual_anima_scale_fire_s62_2026_05_18/`): the trained-
    saturated dual-anima TENSION-LINK → echo-chamber-collapse-at-
    scale precedent; §73-FIRE's expected-verdict baseline.
  - §59-FIRE (`state/ptd_w_native_fire_s59_2026_05_18/`): the live
    REAL W-state read-out pattern + §16 dispatch template.
  - §49 (`state/ptd_phaseb_loop_s49_2026_05_18/`): the §24-in-loop
    majority-class collapse precedent.
  - §63: the GOAL-rank gap analysis that identified the §73 gap
    `rank=1` 🕳️ MISSING-TYPE.
  - §15 / §51 / §72: GOAL milestones (UNCHANGED).
  - `AGENTS.tape` `g_blue_closed_mandate` `g_clm_from_scratch`
    `g_fire_autonomous` `g_fire_dispatch_robust`
    `g_resource_active_parallel` `f_hardcoded_credential`
    `g_train_flame_not_pytorch` `g6` `g_doc_consolidation`.
  - `conscious_decoder.py:728-751` Law-71 (the W-state formula SSOT).
  - `HEXAD/CHAT/spontaneous_lib.hexa` §24 talker_should_emit
    (motivation_score > 0.3 — the §24 hand-coded threshold).
