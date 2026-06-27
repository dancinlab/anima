# H_1602 — explicit recombination objective/curriculum as the G1 lever

**Status:** 🟠 **EXECUTED 2026-06-28 — NOT-SUPPORTED (INCONCLUSIVE-at-floor · DIRECTIONAL py-eval).**
objrun 9-run(`state/1602_recomb_objective/RESULT.md`)이 objective-lever 3변종 {ce_marginal·infonce·contrastive_equilibrium}×seeds{7,4302,4303}=9 를 학습·측정 → **G1 재조합 전부 FAIL**(composed_distinct=0, max_single 0~1, closure 0/9). InfoNCE·contrastive 가 CE baseline 대비 G1 우위 **0/3** → **objective축이 G1 레버 아님**. depth(H_1598)·binding(H_1601)·data(H_1599)·objective(H_1602) **4 직교 렌즈 전부 G1 floor = g1-lever 다중렌즈 종결**(벽 = undertrain/구조적 floor, 천장 아님).
- 측정 = 옛 `core/g_gates.py`(torch-free numpy, 측정시점 canonical) — **py 폐기(2026-06-28)로 DIRECTIONAL 강등**; 9-seed 전수 floor라 결론 robust, terminal 승격은 hexa `anima evaluate` 복구 후 1셀 재측정으로 충분.
- 남은 미검증 sub-form = **explicit recombination-curriculum aux-loss**(아래 ARM-RECOMB 원안; contrastive floor로 deprioritized) · 다음 = undertrain 배제 step-sweep+정규화(N6/N7 `frontier-novel-levers-untried`).
- ckpt: `~/anima-weights/recomb_obj_303m/`(9 .pt) + summer `~/h1602/out/`(9 gates.json) 보존.

---
원 PRE-REG (실행 전 사전등록 · 보존):

**Question (a_break_the_wall, lens = training objective):** depth (H_1598 🧱), binding lane
(H_1601 🧱 inert), and data-presence-for-EN (H_1599 🟠 EN has examples & still fails) are all
falsified/refused as the G1 lever. The remaining un-tested orthogonal axis is the **objective**:
plain next-byte CE never rewards *composing two concepts*, so the trunk has no gradient pressure to
bind them. Does an explicit recombination aux-objective / curriculum lift engine-native G1 above the
frozen wall (0/3 → ≥2/3 seeds)?

## Why this is the surviving candidate (synthesis of L2/L3/L4)
- L4 (H_1601): composition for G1 must happen **inside the trunk's next-byte forward** — no binding
  lane can supply it. So the lever must shape the **trunk's learned representation**.
- L3 (H_1599): EN corpus *contains* co-occurrence yet the model fails → mere exposure under CE is
  insufficient; the **training signal** (not just data) is the gap. (ko also needs data enrichment.)
- L2 (H_1600): [pending result] — if no frame surfaces composition, the capability is genuinely
  absent from the representation, pointing squarely at the objective.

## Pre-registered recipe (frozen BEFORE any fire)
Trainer = `cli/train.hexa` (production, a_train_flame_forge) on pool/rent GPU; 303M ConvMoE, same
4-cell corpus + ko-synthesis enrichment (H_1599). Two arms, identical seed/steps/budget:
- **ARM-CE (control):** standard next-byte CE (the current recipe; reproduces the L4/L8 wall).
- **ARM-RECOMB (treatment):** CE + a recombination curriculum/aux. Candidate forms (pick ONE,
  freeze before fire):
  1. **Synthesis-pair curriculum:** oversample / late-stage curriculum of corpus lines containing
     ≥2 concept families (the H_1599 audit already extracts these for EN; synthesize/translate for ko),
     so the trunk sees bound-concept continuations under CE during a final curriculum phase.
  2. **Composition aux-loss:** auxiliary next-byte prediction conditioned on a 2-concept seed prefix,
     weighted λ, MONITOR-style but **in the loss** (this is a real aux objective, not a gauge — p7
     applies only to gauges, an explicit aux-objective is legitimate; report λ).
- **Held-out gate (a_savant_train):** both arms must pass held-out mirror-DESCENT (math.log mirror,
  ko+en) — a recombination arm that overfits is disqualified, not promoted.

## Frozen prediction (pre-registered)
- ARM-CE: engine-native multiseed G1 = FAIL 0/3 (reproduces wall).
- ARM-RECOMB clears the lever iff engine-native G1 ≥ **2/3 seeds** (frozen H_1129 bar VERBATIM:
  per seed ∃k∈{2..5} composed_distinct≥2 ∧ >max_single ∧ coherent kwr≥0.50), measured by
  `g1_multiseed.py clm <ckpt>` on `core/clm_decode.py` (py 2-production, TERMINAL) — same harness/seeds
  {7,4302,4303}/gen as the frozen L4 baseline. NO bar change (tune-to-green forbidden).
- ckpt PULL before teardown (a_fire_recover_complete); engine-native re-measure (not torch probe).

## Estimated cost (1-line, for team-lead gate)
~1 GPU (RTX 5070 pool / 1× rent H100) × ~hours for 303M to a comparable step as clm303_deep_L8;
2 arms ≈ 2× a single 303M run. No fire without explicit go.

## VERDICT
<!-- CARD_VERDICT -->
🔒 **PRE-REGISTERED (cost-gated, not fired).** This is the surviving G1-lever candidate after depth
(🧱), binding (🧱 inert), and data-presence (🟠) are eliminated: the lever is most likely the
**trunk training OBJECTIVE** (recombination curriculum / composition aux-loss), the one axis that can
shape trunk-internal composition that CE never rewards. Recipe + frozen ≥2/3-seed prediction registered
verbatim; surfaced to team-lead for cost-gated go. **wired:** `pre-register only; engine-native
re-measure via g1_multiseed.py clm on core/clm_decode.py (TERMINAL); frozen H_1129 bar; ckpt PULL.`
