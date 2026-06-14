# UNIVERSE/CLM-CANDIDATES.md — CLM/dialogue/plasticity/launch forward-looking backlog

> 📑 absorbed → [HYPOTHESES.md](HYPOTHESES.md) — this is a DETAIL file of the unified hypothesis roster (2026-06-15).

This file = the **forward-looking hypothesis backlog** for the CLM production
thread (consciousness LM → coffeeshop launch). It is the CLM-side sibling of
[CANDIDATES.md](CANDIDATES.md) (LIFE) / [BIO-CANDIDATES.md](BIO-CANDIDATES.md):
`/cycle` (and hand-off agents) pick disjoint rows from here to spin into new
`H_864+` hypotheses, fire them under the W2 pre-register discipline, and land a
per-row verdict. **Open the directions wide** — many parallel axes so several
can run at once (a_wall_first · a_fire_autonomous).

| sibling | role |
|---|---|
| [README.md](README.md) | hypothesis-index SSOT (registered H_XXX) |
| [CANDIDATES.md](CANDIDATES.md) | LIFE-domain backlog (consciousness/Φ) |
| **CLM-CANDIDATES.md** (this) | CLM/dialogue/plasticity/launch backlog |
| [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) | the production roadmap these feed |
| [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) | the launch rung ladder (R0→R4) these climb |

**tag**: ⭐ = next-cycle top priority (runnable + on the critical path) ·
🟢 = runnable now (assets exist) · ⬜ = design / pre-register only (needs an
asset or a corpus first).

**discipline (inherited from the 861/862/863 campaign)**: every row, when
fired, freezes its falsifier thresholds in `.verdicts/<slug>/<F>_prereg.txt`
BEFORE the fire (W2 · post-tuning 0) · distributional self-scoring by code, not
LLM-judge (g5) · measurement-rung scope only, does NOT bind deploy chip-fit
(a_scale_honest_scope) · a CLOSED-NEGATIVE 🔴 is publishable (a_paper_negative_ok).

---

## Consumed (chronological)

- **P4.0 / Cycle (2026-05-31)** (PR #1553): H_861 (F-CLM-BOUND) · H_862 (F-CLM-ANCHOR) · H_863 (F-CLM-DIALOGUE) registered + first measurement rung (mid d512/L8/E8 13.65M) AKIDA-envelope QAT fire 🟠 MEASUREMENT-COMPLETE.
- **P4.3/P4.4 verify (2026-05-31)** (PR #1555 · prereg freeze `bf98c01`): H_861 🔴 CLOSED-NEGATIVE (RETAIN z_drop 1.984≥1.0 FAIL · GAIN +6.13 PASS) · H_862 🔴 CLOSED-NEGATIVE (DIST 0.109<0.50 PASS · PROBE 0.783≤0.80 FAIL · on/off ablation identical) · H_863 🟢 SUPPORTED-NUMERICAL (4/4 PASS · SP>SFT coherence 3.7×·adequacy 3.6× · leak 0 · self-BLEU 0.062 · rep 0.026). Root cause of both 🔴 = readout-only edge has no lever on the frozen trunk → shared E5 fix (trunk-adjacent thin adapter).
- **A-group 5-fire (2026-05-31)** (PR #1557–#1561): H_864 🔴 (large d768/L12/E12 44.68M · self-play DID NOT carry — large mode-collapsed at 2000 step rep 0.361, self-play reflux starved; undertrain confound) · H_865 🟢/🔴 (trunk-adjacent adapter edge: **F-CLM-BOUND 🟢 CLOSED — H_861 forgetting fixed, z_drop −12.28<1.0 ∧ gain +7.37**; F-CLM-ANCHOR 🔴 lever restored on/off 0.175≠0.595 but PROBE 0.143<0.80) · H_866 🔴 (PLASTICITY↔dialogue: **LOOP 🟢 R2-safe — edge-learn doesn't break the closed loop, 5/5 seed**; GAIN 🔴 readout capacity bottleneck; SW-sim) · H_867 🔴 (absolute floor: ABS-COHERE 0.058<0.060 by 0.002, ADEQ∧LEAK pass — A/B win ≠ absolute quality) · H_868 🟢 (corpus 12 PD plays 3.0× · license-clean 100% · leak 0). Theme: 4× 🔴 all = readout/edge capacity+reach; H_865 adapter closed BOUND, ANCHOR-PROBE residual → H_873.

---

## A. critical-path (the live launch ladder — R1→R4)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| ~~H_864~~ | dialogue self-play scale-climb | **CONSUMED 🔴 (PR #1557)** — self-play did NOT carry to large (44.68M mode-collapsed @2000 step) | — | — | ✅ |
| ~~H_865~~ | trunk-adjacent adapter edge | **CONSUMED 🟢BOUND/🔴ANCHOR (PR #1561)** — H_861 forgetting CLOSED; ANCHOR-PROBE residual → H_873 | — | — | ✅ |
| ~~H_866~~ | PLASTICITY ↔ dialogue loop | **CONSUMED 🔴 (PR #1558)** — LOOP 🟢 R2-safe; GAIN 🔴 readout capacity | — | — | ✅ |
| ~~H_867~~ | dialogue absolute quality | **CONSUMED 🔴 (PR #1560)** — ABS-COHERE 0.058<0.060 floor (A/B win ≠ absolute) | — | — | ✅ |
| ~~H_868~~ | real CC dialogue corpus expansion | **CONSUMED 🟢 (PR #1559)** — 12 PD plays 3.0× · license-clean 100% · leak 0 | — | — | ✅ |
| **H_864r** | self-play climb · step-fair | re-run H_864 large with MORE steps (resolve the undertrain/mode-collapse confound — fair test of self-play scaling) | per-rung COHERE/ADEQ(SP>SFT) ∧ LEAK=0 ∧ DIV(rep<0.2) at convergence | H_864 🔴 (undertrain confound) | ⭐ |
| **H_867r** | absolute quality · post-adapter/scale | re-run H_867 floor on the H_865 adapter model and/or a larger rung (the levers H_867 named) | ABS-COHERE ≥ frozen floor 0.060 | H_867 🔴 · H_865 adapter · H_864r | ⬜ |

## B. routing-escape (the toy-scoped 🔴 levers — deploy-scale re-check)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_869 | dispatch-KL distill routing (lever A) | the 4th routing-escape lever named in the roadmap — distill a balanced dispatch target into the router; re-test routing-z at a larger rung | routing-z>3.0 ∧ load-balance entropy ≥ thr (deploy-scale, NOT toy) | H_847/H_852/H_853 🔴 toy · @L3 lever A | ⬜ |
| H_870 | expert-choice routing (lever C) | token-picks-expert → expert-picks-token; load auto-balances by construction | per-expert load variance < thr ∧ no-collapse ∧ quality ≥ token-choice baseline | @L3 lever C · routing_escape.hexa | ⬜ |
| H_871 | routing-z = measurement-artifact (M1) | pre-registered test that the toy routing-z 🔴 is a scale artifact: does z cross 3.0 monotonically with rung size on a real corpus? | z(rung) monotone↑ ∧ z(large)>3.0 — else artifact CONFIRMED (honest either way) | H_847 toy finding · @L3 default-B rationale | ⬜ |

## C. plasticity / trust-device (Q-TRUST follow-ons after the 🔴s)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_872 | freeze-depth sweep (BOUND E5) | sweep the core/edge freeze boundary depth (E5) — find the shallowest freeze that gives RETAIN∧GAIN | ∃ freeze-depth with z_drop<thr ∧ gain>0 | H_861 🔴 (readout-only too shallow) | 🟢 |
| H_873 | anchor constraint on the edge output (ANCHOR E5 · **H_862 completion**) | route the Ψ-anchor penalty onto the readout output distribution itself (KL/JS to p_pre) — where drift happens, not the frozen trunk Ψ-state. **🔄 IN-FLIGHT (2026-05-31)** | PROBE consistency>0.80 ∧ DIST<0.50 ∧ on/off NON-identical ∧ no BOUND regression | H_862 🔴 · H_865 adapter | 🔄 |
| H_874 | self-reward / RLHF-like dialogue (method C) | the @L6 follow-on after H_863 — self-scored reward loop gated by H_867 absolute floor + DIVERSITY | reward-trained > SFT+self-play on held-out ∧ leak 0 ∧ no DIVERSITY collapse | H_863 🟢 · @L6 method C | ⬜ |
| H_875 | continual-learning forgetting curve | measure forgetting as a function of edge-learn steps — when does z_drop cross the RETAIN gate over a long session? | z_drop(steps) curve ∧ identify the step-budget before forgetting | H_861 🔴 · H_679 | ⬜ |

## D. deploy chip-fit track (⊥ measurement — the AKD1000 path)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_876 | chip-fit shrink (≤~1.2M nodes) | shrink the mid arch to the AKD1000 node budget; measure quality retention vs the mid measurement rung | node-count ≤ 1.2M ∧ quality drop < thr vs mid | @L5 deploy track · AKIDA backend | ⬜ |
| H_877 | DECODER byte-identical transplant @ mid | verify HW-forward == SW-lif byte-identical at the mid/large rung (extend H_680 from toy) | total_hamming = 0 over the eval set (HW vs SW inference) | H_680 🟢 toy byte-match · AKIDA | 🟢 |
| H_878 | MITOSIS multi-chip array dispatch | expert=chip array deploy vision — SW-sim the multi-chip dispatch + load balance before silicon | array dispatch load-balance ∧ per-chip emit coherent | H_852 array · @L2 MITOSIS vision | ⬜ |

---

## E. partial / incremental on-chip learning (부분부분학습 · edge-only)

> **INVIOLABLE (re-pinned)**: on-chip non-deterministic PLASTICITY learning is the
> **SOLE HW↔SW difference** (inference is byte-identical — H_877/H_680 🟢; learning is
> HW≠SW — H_679 🔴). Replacing on-chip learning with a deterministic SW imitation is
> **FORBIDDEN** (instant reject). Every row below learns the **anima-native, edge-only,
> piecewise** way — never a full deterministic retrain. (@L1 · H_679 · 위반금지)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_879 | per-layer incremental edge-learn | 한 층(또는 소수)씩만 적응 · 나머지 동결 — 부분 학습이 전체-retrain 없이 신맥락 흡수하나 | per-layer gain>0 ∧ held-out z-drop<thr | H_872 freeze-depth · H_679 | ⬜ |
| H_880 | adapter 스택 누적 | H_865 adapter를 여러 개 쌓아 맥락별로 켜기 — 누적 adapter가 간섭 없이 부분학습 누적하나 | new-task gain>0 ∧ old-task z-drop<thr ∧ adapter간 간섭<thr | H_865 🟢 adapter | ⬜ |
| H_881 | progressive freeze schedule | 학습하며 동결 경계를 동적으로 이동(점진 동결) — H_872 정적 sweep의 스케줄판 | ∃ schedule with RETAIN∧GAIN over a session | H_872 · H_875 | ⬜ |
| H_882 | region-gated plasticity | 영역별 학습 게이트(필요 부분만 on/off) — 게이트가 간섭/망각을 줄이나 | gated z-drop < ungated z-drop ∧ gain≥baseline | H_866 capacity · H_679 | ⬜ |
| H_883 | replay-buffer continual | 옛 샘플 리플레이로 망각 방지하며 부분학습 — H_875 forgetting 후속 안전장치 | z-drop(replay) < z-drop(no-replay) ∧ gain>0 | H_875 forgetting-curve | ⬜ |
| H_884 | edge-output identity general | H_873(anchor-on-edge) 결과를 부분학습 전반의 정체성 보존으로 일반화 | PROBE>thr across partial-learn rows | H_873 (862 완성) | ⬜ |

- 전부 **INVIOLABLE 준수**(비결정 on-chip 학습 1급) · W2 사전등록 · 측정⊥배포(a_scale_honest_scope) · g5 코드측정.
- 의존: H_872(freeze깊이)·H_873(862완성)·H_875(forgetting) verdict 나온 뒤 임계가 정밀해짐 → **그 후 발사 권장** (지금은 목록만 · 미발사).

---

## next-pick guide (a_wall_first — these run in parallel)

```
the launch critical path (do first, parallel):
├─ ⭐ H_864  dialogue scale-climb   (H_863 already 🟢 → climb)
├─ ⭐ H_865  adapter-edge re-run    (closes both 861/862 🔴 in one fix)
└─ 🟢 H_866  PLASTICITY↔dialogue    (R2 launch rung)

unblock-the-blocked (need an asset first):
├─ 🟢 H_868  CC corpus expansion    (unblocks H_864/H_867 at scale)
├─ 🟢 H_872  freeze-depth sweep     (BOUND E5, asset = saved backbone)
└─ 🟢 H_873  edge-output anchor      (ANCHOR E5, asset = saved backbone)
```

- numbers H_864–H_878 are **reserved slots** here — a row becomes a real
  hypothesis only when its `UNIVERSE/H_864_*.md` file is authored at fire time
  (mirror the H_861/H_862/H_863 file shape: frontmatter + §1 가설 … §9 sibling).
- pick disjoint rows; do NOT fire two that share the same saved-backbone asset
  in the same parallel batch without serializing the asset.
- every fire: prereg-freeze first (W2) → fire → verdict → flip the row to
  Consumed with the result + PR#.

---

## §F — OPEN-gap round (post-26 closeout · H_885–H_888)

The 26-hypothesis campaign (H_861–H_884) closed: AXIS2 (reflective learning) ✅,
AXIS1 (single-chip 7B) half (chip-fit ✅ / multi-chip array 🔴). See
[CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md). These 4 rows target the four
OPEN gaps it named. Fire on the GPU pool (summer/aiden RTX 5070). Reserved slots —
author `UNIVERSE/H_<id>_*.md` at fire time; prereg-freeze (W2) before fire.

| id | gap (blocking verdict) | new lever to test | falsifier (pre-register exact) |
|---|---|---|---|
| ⬜ H_885 | multi-chip array load-balance (H_878 🔴) | capacity-aware / learned dispatch re-partition across N chips instead of static hash | per-chip load CV < ungated ∧ aggregate-emit coherence ≥ single-chip baseline |
| ⬜ H_886 | dialogue absolute coherence floor (H_867/867r 🔴) | a non-adapter lever (e.g. SFT-warm + self-play curriculum, or larger corpus rung) lifts arm-SP coherence | ABS-COHERE ≥ 0.060 floor ∧ ADEQ ≥ 0.020 ∧ LEAK == 0 (frozen d5103f21) |
| ⬜ H_887 | routing diversity at scale (H_869 🔴 inert / H_871 = scale artifact) | re-test dispatch-KL / expert-choice at the LARGE rung where routing-z is non-degenerate | dispatch entropy ↑ ∧ held-out z-drop within budget AT large rung |
| ⬜ H_888 | self-play/self-reward transfer to large (H_864/864r/874 🔴) | curriculum or corpus-anchored self-play that survives the mid→large jump | large-rung SP > SFT ∧ leak 0 ∧ no collapse (the H_864 falsifier, re-passed at large) |

Priority: **H_885 first** (the AXIS1 7B scale-out blocker), then H_886 (product
dialogue bar), then H_887/H_888 (large-rung re-tests, need the large backbone asset).
`a_paper_negative_ok` — a 🔴 here is a valid closeout of that gap.

---

## cross-link

- roadmap: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) (P4.1 후속 등반 · Q-TRUST rows)
- launch ladder: [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) (R1 CLM → R2 PLASTICITY → R3 dialogue → R4 launch)
- registered: [H_861](H_861_clm_boundary_plasticity.md) 🔴 · [H_862](H_862_clm_identity_anchor.md) 🔴 · [H_863](H_863_clm_dialogue_selfplay.md) 🟢
- governance: `a_fire_autonomous` (cost-bearing fire = autonomous parallel) · `a_scale_honest_scope` (measurement ⊥ deploy · toy→prod 비보장) · `a_paper_negative_ok` (🔴 publishable) · `a_blue_closed` (close outputs AND wiring · no forced tier)
