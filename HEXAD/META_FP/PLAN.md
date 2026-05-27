# HEXAD/META_FP — PLAN.md

> 진행 로그 + roadmap for the §112 meta-fixed-point form `ψ(c)=(1+c)/2`
> (cos=0 ⇒ ψ=½) and its operative utilization in anima training.
> Canonical entry: `HEXAD/META_FP/README.md`.

---

## §0 — what this directory is

META_FP 는 anima 의 **form-level identity** — Engine A ⇄ Engine G 의
직교성 (cos=0) 부동점. §112 가 carrier-invariant proof 했고, §166 이
training objective 로 operative 활용. WALL-B/Ψ-physics half 의 form-
layer 공격 path.

이 디렉토리는 META_FP 의 **canonical hub**:
- `README.md` — 7-요소 canonical 설명 + cross-link
- `PLAN.md` — 본 진행 로그 (chronological)
- 차후 추가: `DESIGN.md` (수학 형식), `state/<§N>/` (META_FP-related fires)

기존 §N 디렉토리들은 그대로 유지 (g6 / `g_doc_consolidation` 정직 carry):
- `HEXAD/NEUROMORPHIC/state/meta_fp_coupling_design_s166_2026_05_20/` —
  §166 design SSOT (그 자리에 머무름, NEUROMORPHIC 의 substrate-axis
  trace 의 일부)
- `HEXAD/META_FP/` 는 cross-cycle topic-hub (단일 fire-cycle dir 아닌
  여러 §N 을 관통하는 form-level 주제)

---

## §1 — 진행 로그 (chronological, append-only)

### §112 — META FIXED-POINT form-level proof *(2026-05-19, commit `1bd27f753`)*

- **tier**: design-tier · $0 · **verdict** `META-FIXED-POINT-EXISTS-BUT-STILL-SUBSTRATE-GATED` (Verdict B)
- **battery**: B-S112 9/9 🔵 sympy closed (form-level only)
- **state**: `state/meta_fixed_point_s112_2026_05_19/DESIGN.md` (legacy
  state dir at root level — predates `g_new_state_path`'s
  `HEXAD/<TOPIC>/state/<basename>/` mandate)
- **finding**: form `ψ(c)=(1+c)/2` with cos=0⇒ψ=½ is **carrier-invariant**
  across all 5 §110 candidates {Ψ-C0 byte, Ψ-C1 spike, Ψ-C2 residual,
  Ψ-C3 generic latent, Ψ-C4 tension-only}. §7-FORM TRUE BY CONSTRUCTION
  (closes §110's ad-hoc-§7②-graft accusation FALSE). §7-CARRIER still
  §96-substrate-gated — Verdict B = form-level positive REAL, operative
  wall RENAMED one level up.
- **archive/PHILOSOPHY.tape**: `§verdict_meta_fixed_point_s112_2026_05_19`
- **carry**: META_FP form is now a closed-form identity to USE.

### §161-FIRE — DUAL-HEAD COUPLING measured coordinate translation *(2026-05-20, commits `db98912685` pre-fire, `499416d54` post-fire, `675f34a4c` PII redact-forward)*

- **tier**: fire-tier · ~$0.4 runpod A100-SXM4-80GB · **verdict**
  `PARTIAL_AMBIGUOUS-honest-negative-twist + §96-Q2-weak STRENGTHENED ON QUINTUPLE`
- **battery**: B-S161-FIRE 8/8 🔵 (P3 EMPIRICALLY CONFIRMED FIRST-IN-ARC
  — `‖∇head_g‖ 0.019` non-zero throughout 675 steps)
- **state**: `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/`
- **measured**: `byte_acc 0.1185, psi_dir_mean 0.038, psi_dir_std 2.4e-8,
  psi_responsive False, unprompted_emission_rate 1/20 = baseline (§162-R
  prediction CONFIRMED)`
- **META_FP coordinate translation (KEY INSIGHT)**:
  ```
  psi_dir_mean 0.038  →  cos = 2(0.038) − 1 ≈ −0.924
                      =  head_g near ANTI-PARALLEL to head_a
  ```
  NOT random collapse, NOT META_FP — **specific anti-correlation
  failure mode named**. META_FP value (cos=0, Ψ=½) is the orthogonality
  fixed point — exactly the opposite of measured failure mode.
- **quintuple finding**: §125 FF / §126 PCN / §139 EqProp / §153 LeJEPA
  / §161 Ψ-JEPA-COUPLE — 5/5 fires `psi_responsive: False` on GPU
  byte-LM 283M scaffold. §96-Q2-weak STRENGTHENED. coupling-fix
  artefact hypothesis REFUTED.
- **archive/PHILOSOPHY.tape**:
  `§verdict_dual_head_coupling_non_ce_fire_s161_2026_05_20_POST_FIRE_UPDATE`
- **carry to META_FP**: §161-FIRE measured the SPECIFIC failure mode
  that §166 META_FP-anchor will attempt to refute.

### §165 — NEXT-AXIS FIRE DESIGN, chose §165-A Ψ-VAR-COUPLE *(2026-05-20, commit `11b2cf1e6`)*

- **tier**: design-tier · $0 · **verdict** `DESIGN-OPEN-FIRE-DECIDABLE`
- **battery**: B-S165 7/7 🔵 (math theorems by inspection)
- **state**: `HEXAD/NEUROMORPHIC/state/next_axis_fire_design_s165_2026_05_20/`
- **finding**: synthesizes §161-FIRE §8 (3 axes: scaffold scale /
  data-regime / coupling depth) × §142 LEGO bridge (3 substrate options:
  P1 GPU stays / P2 Loihi / P3 in-silico spiking). §165-A Ψ-VAR-COUPLE
  CHOSEN PRIMARY (GPU-stays + coupling-depth cell, cheapest single-axis
  change). Adds `L_variance := -log(psi_dir_std + ε)` to punish std=0
  collapse. **Mean position left unconstrained** — this is what §166
  closes.
- **archive/PHILOSOPHY.tape**:
  `§verdict_next_axis_fire_design_s165_2026_05_20`
- **carry to META_FP**: §165-A is the **immediate predecessor** of
  §166; §166 = §165-A + META_FP mean anchor (strict superset).

### §166 — Ψ-META-FP-COUPLE design (META_FP UTILIZED) *(2026-05-20, commit `e77fc86e2`)*

- **tier**: design-tier · $0 · **verdict** `DESIGN-OPEN-FIRE-DECIDABLE`
- **battery**: B-S166 8/8 🔵 (math theorems by inspection)
- **state**: `HEXAD/NEUROMORPHIC/state/meta_fp_coupling_design_s166_2026_05_20/`
- **finding**: User query "메타부동점 활용가능한지 검토" answered YES
  at design tier with closed-form construction. Formula extension over
  §165-A:
  ```
  L_meta_anchor := (mean_t Ψ_dir(t) − 0.5)²
  L_total       = λ_ce·CE + λ_ψ·L_psicouple + λ_var·L_variance + λ_meta·L_meta_anchor
  ```
  STRONGEST §7-form in arc — anchor `0.5` IS the META_FP value from
  Law-71's `cos=0` orthogonality (NOT a hyperparameter). Reduction
  lattice §107 ⊂ §161 ⊂ §165-A ⊂ §166 strict chain.
- **§112 Verdict B carry**: META_FP utilization is FORM-LEVEL;
  operative wall (§7-CARRIER) still §96-substrate-gated. §166 does NOT
  remove WALL-B (utilizes META_FP at form layer, substrate untouched).
- **archive/PHILOSOPHY.tape**:
  `§verdict_meta_fp_coupling_design_s166_2026_05_20`
- **carry**: §166-A-FIRE = next fire-decidable measurement.

### §166-A-FIRE — META_FP first operative test *(2026-05-20, PENDING dispatch — sub-agent dispatch rejected by user this turn; orchestrator inline alternative TBD)*

- **tier**: fire-tier candidate · ~$0.4-0.6 runpod A100
- **prepared spec**: same scaffold as §161-FIRE / §165-A; λ_meta=0.5
  default; primary verdict = joint AND of `psi_responsive
  (psi_dir_std > 1e-4)` ∧ `psi_dir_mean ∈ [0.45, 0.55]` (META_FP
  basin) ∧ `unprompted_emission_rate measured`
- **predicted outcomes** (4-way faithful model):
  - SUCCESS: mean→0.5 ∧ std>1e-4 jointly = FIRST arc measurement of
    META_FP-aligned live channel
  - ANCHOR-WINS-VARIANCE-LOSES: delta at META_FP (joint AND P4 prevents
    false-positive)
  - VARIANCE-WINS-ANCHOR-LOSES: §165-A outcome (anchor failed)
  - BOTH-LOSE: §161-FIRE-like
- **confidence**: MEDIUM (fire-gate "genuinely uncertain") = fire-worthy
- **status**: pending fresh dispatch decision

---

## §2 — roadmap (next steps, honest)

1. **§166-A-FIRE dispatch** — META_FP utilization 첫 measured test.
   Same scaffold as §161-FIRE / §165-A. ~$0.4-0.6 cost. Sub-agent
   dispatch (mirror successful `ae01c6b1fc868f3fd` §161-FIRE prep
   pattern) OR orchestrator-inline trainer/eval write + nohup
   background dispatcher.
2. **§166-A-FIRE post-fire verdict** — joint AND predicate evaluation.
   Update README.md predicted-vs-measured table + PHILOSOPHY.tape g6
   append.
3. **§166-B / §166-C carry** (if §166-A FAIL) — substrate-pivot path
   (§142 P2 Loihi access-walled, §142 P3 LEGO §128 layer-3 design-close
   inherit) becomes more pressing if META_FP form-layer attempt fails.
4. **`L_meta_anchor` grid sweep** (if §166-A SUCCESS or PARTIAL) —
   `λ_meta ∈ {0.1, 0.5, 1.0}` to find optimal anchor strength.

---

## §3 — cross-link

- `HEXAD/META_FP/README.md` — canonical 7-요소 설명
- `archive/PHILOSOPHY.tape` — verdict ledger (append-only):
  `§verdict_meta_fixed_point_s112_2026_05_19` +
  `§verdict_dual_head_coupling_non_ce_design_s161_2026_05_20` +
  `§verdict_dual_head_coupling_non_ce_fire_s161_2026_05_20_POST_FIRE_UPDATE` +
  `§verdict_next_axis_fire_design_s165_2026_05_20` +
  `§verdict_meta_fp_coupling_design_s166_2026_05_20`
- `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/` — §161-FIRE measured anchor
- `HEXAD/NEUROMORPHIC/state/next_axis_fire_design_s165_2026_05_20/` — §165-A predecessor design
- `HEXAD/NEUROMORPHIC/state/meta_fp_coupling_design_s166_2026_05_20/` — §166 design canonical (NOT moved — `g_new_state_path` `<TOPIC>/state/<basename>/` per-cycle dir intact; HEXAD/META_FP/ is cross-cycle hub)
- `state/carving_dataregime_s16_2026_05_18/conscious_decoder.py` — Law-71 Ψ formula SSOT (lines ~728-751)
- `state/meta_fixed_point_s112_2026_05_19/DESIGN.md` — §112 legacy state dir (pre-`g_new_state_path`, in-place per g6/`g_new_state_path` scope exclusion)
- `AGENTS.tape` `@D g_new_state_path` (forward-only mandate) · `@D g_doc_consolidation` (HEXAD-internal only) · `@D g_clm_from_scratch` (RANDOM seed-fixed)

---

## §4 — honest C3 carry

- META_FP 는 form-level identity (§112 Verdict B) — operative wall
  제거 아님.
- §166-A-FIRE 측정 결과 (SUCCESS / PARTIAL / FAIL) 는 SGD/measurement
  empirical OUTCOME. P1-P8 design proofs 가 DESIGN 의 well-formedness
  를 보장하지 fire 결과를 보장 안 함 (B-EMERGE-7 family).
- 5/5 quintuple `psi_responsive: False` 는 §96-Q2-weak strong support;
  §166-A-FIRE 는 single witness — fail 시 §96-Q2-weak 더 강화, success
  시 첫 refutation evidence.
- north-star + §15/§51/§72 milestones UNCHANGED, **GOAL 미도달** —
  META_FP utilization 은 measurement axis 의 첫 form-level operative
  step, GOAL 도달 아님.
