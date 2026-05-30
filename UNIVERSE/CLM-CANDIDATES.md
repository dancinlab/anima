# UNIVERSE/CLM-CANDIDATES.md — CLM/dialogue/plasticity/launch forward-looking backlog

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

## cross-link

- roadmap: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) (P4.1 후속 등반 · Q-TRUST rows)
- launch ladder: [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) (R1 CLM → R2 PLASTICITY → R3 dialogue → R4 launch)
- registered: [H_861](H_861_clm_boundary_plasticity.md) 🔴 · [H_862](H_862_clm_identity_anchor.md) 🔴 · [H_863](H_863_clm_dialogue_selfplay.md) 🟢
- governance: `a_fire_autonomous` (cost-bearing fire = autonomous parallel) · `a_scale_honest_scope` (measurement ⊥ deploy · toy→prod 비보장) · `a_paper_negative_ok` (🔴 publishable) · `a_blue_closed` (close outputs AND wiring · no forced tier)
