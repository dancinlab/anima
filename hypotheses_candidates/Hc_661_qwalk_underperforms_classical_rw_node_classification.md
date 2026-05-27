---
id: Hc_661
slug: qwalk-underperforms-classical-rw-node-classification-pca
title: CTQW long-time-averaged occupation matrix 가 PCA-embed node classification 에서 classical RW 대비 underperform — F-QWALK-1 REJECTED
domain: anima-architecture
status: candidate-sparse
source_doc: docs/anima_qwalk_landed_2026_05_03.ai.md
source_lines: 1-80
promoted_at: 2026-05-11
linked_h: EEG16 PLV synthetic, SBM (3 blocks of 20)
notes: F-QWALK-1: quantum walk init Δ > +5% accuracy vs random walk → REJECTED (EEG16 Δ=-56.25pp, SBM Δ=-21.67pp). Mechanism: QW long-time-avg dilutes community eigenvector contribution by equal weighting.
cycle5_triage: "cycle #5 verify: FAIL — partial scaffolding (some F or L bullets) but no math identity; needs math axis OR atlas anchor to upgrade"
---

## Hypothesis (FALSIFIED)
Continuous-time quantum walk (CTQW) init `P_qw(i,j) = Σ_λ (Π_λ[i,j])²` 가 anima-relevant graphs (EEG16 coupling + 3-block SBM) 의 node embedding 으로서 classical random walk (`P_rw = D⁻¹A`) 대비 측정 가능 lift 제공. PCA-reduced (d=8/d=16) 후 stratified-K-fold logistic regression node classification 에서 Δ > +5pp.

## Falsifiable Tests (result)
- F-QWALK-1: Δ > +5pp on EEG16 → **REJECTED** (Δ=-56.25pp, RW 100% vs QW 43.75%)
- F-QWALK-1: Δ > +5pp on SBM → **REJECTED** (Δ=-21.67pp, RW 95% vs QW 73.33%)
- F-QWALK-mech: QW stationary uniform 1/N (vs RW d_i/2|E| carries degree info)

## Migration TODO
- [ ] Mechanism: QW long-time-avg dilutes community structure (no exponential decay vs heat kernel)
- [ ] Future tests: (a) finite-t snapshots, (b) coined discrete-time QW Grover coin, (c) Szegedy walks
- [ ] Real anima-eeg ≥60s artifact-rejected recording (synthetic substrate caveat)
- [ ] CTQW lane closure (under current embedding choice)
