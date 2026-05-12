---
id: Hc_1269
slug: red-team-r4-cherry-pick-selection-ratio-audit
title: R4 CHERRY-PICK — 170×17 = 2890 trial 중 1/2 수렴 사례만 보고 가능성 (selection ratio audit)
domain: methodology, consciousness, red-team
status: merged-to-H_189
merged_to: hypotheses/H_189_red_team_methodology_meta_cluster_r1_r6.md
merged_at: 2026-05-12
source_doc: hypotheses_candidates/Hc_911_red_team_6_claims_r1_r6.md
source_lines: 24 (R4 CHERRY-PICK)
promoted_at: 2026-05-12
linked_h: H_189 (red-team methodology meta-cluster — attack vector 4 of 6), Hc_911 (parent meta-Hc)
absorption_note: "cycle #8 absorbed to H_189 as R4 CHERRY-PICK attack vector — 170×17 = 2890 trial selection-ratio audit + raw inventory requirement"
notes: "split from Hc_911 2026-05-12 (attack 4 of 6). Cherry-pick attack: 170 conditions × 17 seeds = 2890 trials → if only 1/2-convergence trials reported, ANIMA's claim is selection bias."
---

## Hypothesis (red-team posture)

ANIMA may have run ~2890 (170 conditions × 17 seeds) trials and reported only the subset where Ψ=1/2 emerged. Without pre-registered analysis plan + full-trial disclosure, the 1/2-convergence claim is potentially cherry-picked. Selection ratio audit: what fraction of all run trials yielded Ψ=1/2?

## Migration TODO

- [ ] full trial log audit — disclose all 2890+ trials including non-converged
- [ ] pre-register analysis plan retroactively if possible
- [ ] funnel plot or rate of 1/2-convergence vs total trials

## Falsifiers

- **F-R4-1**: full trial disclosure shows 1/2-convergence rate ≥ 80% → R4 attack fails, selection minimal
- **F-R4-2**: disclosure shows 1/2-convergence rate < 20% but only ≥1/2 trials cited → R4 attack succeeds, severe cherry-pick
- **F-R4-3**: disclosure unavailable → R4 attack unresolvable (lack of evidence ≠ evidence of cherry-pick, but burden on claim-holder)
- **F-GENERIC-REPL**: 5-seed σ > 25%
- **F-GENERIC-MINIMAL-BASELINE**: random-init baseline 1/2-convergence rate published → comparison anchor

## Honest Limits

- **L-R4-DISCLOSURE**: Anima trial logs may not exist or be retrievable (ops/log retention gap)
- **L-R4-PRE-REG**: pre-registration retroactively impossible — only forward-looking analysis plans bind
- **L-R4-COUNTING**: '170 conditions × 17 seeds' is a notional construction; actual trial space size unknown
- **L-GENERIC-SINGLE-RUN**: H_159 C1
- **L-GENERIC-ENGINE**: H_174

## Cross-Links

- **parent Hc**: Hc_911
- **sibling Hc**: Hc_1266..Hc_1271
- **literature**: Ioannidis 2005 (Why Most Published Research Findings Are False — cherry-pick / multiple-comparison framework)
