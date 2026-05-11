# anima quantum-walk node init PoC + benchmark — LANDED

**Date**: 2026-05-03
**Cost**: $0 (Mac local, 0.41 s wall, no GPU, no quantum SDK)
**Falsifier**: F-QWALK-1 — quantum walk init Δ > +5% accuracy vs random walk
**Decision**: **F-QWALK-1 FAIL** on both tested substrates (Δ < 0 for both).

<!-- [Hc_661 qwalk-underperforms-classical-rw-node-classification-pca — moved to hypotheses_candidates/Hc_661_qwalk_underperforms_classical_rw_node_classification.md on 2026-05-11] -->

## TL;DR

Built a continuous-time quantum walk (CTQW) on two anima-relevant graphs (synthetic
EEG 16-channel coupling + 3-block SBM, n=60), computed the long-time-averaged
occupation matrix `P_qw(i,j) = Σ_λ (Π_λ[i,j])²` with proper degeneracy handling,
verified `P_qw` is doubly stochastic to 1e-15. Compared its rows against the
classical random-walk transition `P_rw = D⁻¹A` as PCA-reduced (d=8 / d=16) node
embeddings under stratified-K-fold logistic regression node classification. **CTQW
init underperformed classical random-walk init on both substrates** (–56.25 pp on
EEG16, –21.67 pp on SBM). Falsifier rejected.

## Substrates

| Substrate | n | edges | task |
|---|---|---|---|
| EEG16 coupling (synthetic PLV, 4 functional clusters of 4) | 16 | 35 | 4-cluster node classification |
| SBM (3 blocks of 20, p_in=0.35, p_out=0.04) | 60 | 220 | 3-block node classification |

## Numerical results

### Stationary distributions

|  | KL(qw‖rw) | JS | TVD |
|---|---|---|---|
| EEG16 | 0.0170 | 0.0041 | 0.069 |
| SBM   | 0.0384 | 0.0093 | 0.112 |

QW stationary is uniform (1/N) on both graphs — expected: the long-time average from
*any* starting site averages every distinct-eigenvalue projector contribution, and
when starting from the maximally-mixed state the marginal is exactly 1/N. RW
stationary is the classic π_i = d_i / 2|E|, which actually carries degree
information — and **degree information turns out to be precisely what the
downstream classifier exploits**.

### Downstream node classification (CV mean acc)

| Substrate | RW acc | QW acc | Δ pp |
|---|---|---|---|
| EEG16 | **1.0000** | 0.4375 | **−56.25** |
| SBM   | **0.9500** | 0.7333 | **−21.67** |

Threshold +5 pp not crossed. Falsifier F-QWALK-1: **FAIL**.

## Mechanism (why QW lost)

The CTQW long-time-average projects onto eigenspaces of H = A. For SBM/EEG-cluster
graphs, the dominant low-frequency eigenvectors carry the community structure but
their contribution is diluted by averaging over *all* eigenvalue projectors with
equal weight (no exponential decay — unlike the heat kernel `exp(-tL)`). The
classical RW row vectors, in contrast, are sharply localized on a node's
neighborhood and inherit degree contrast directly, which is highly discriminative
for both block-recovery and degree-correlated-cluster tasks.

## Files

- `state/anima_qwalk_2026_05_03/qwalk_poc.py` — full implementation
- `state/anima_qwalk_2026_05_03/walk_comparison.json` — full numerics (both substrates)
- `state/anima_qwalk_2026_05_03/verdict.json` — slim verdict
- `/tmp/anima_qwalk_2026_05_03/{...}` — mirror (per spec)
- `state/markers/anima_qwalk_landed.marker`

## Caveats (3)

1. **Synthetic EEG substrate, not held-out empirical recordings.** The 16×16 PLV
   matrix uses cluster-conditional Beta draws — it is a structural toy, not anima-eeg
   real channel data. A repeat against a recorded session (anima-eeg `eeg_recorder.hexa`
   output, ≥60 s artifact-rejected) is required before any anima-domain claim.
2. **Embedding choice penalizes QW.** Using row-of-`P_qw` → PCA is the most
   apples-to-apples baseline against row-of-`P_rw` → PCA, but it discards the
   *amplitude/phase* structure of the unitary `e⁻ⁱᴴᵗ` at finite t. A fairer next
   round should also test (a) finite-t snapshots, (b) coined discrete-time QW with
   Grover coin (asymmetric mixing), and (c) Szegedy walks (which provably quadratically
   speed up classical hitting times on some graphs).
3. **Falsifier set on absolute-Δ at +5 pp regardless of baseline saturation.** RW
   already saturates at 1.0 on EEG16 and 0.95 on SBM, so any positive Δ is structurally
   capped. Re-running on harder substrates (noisier SBM with p_in close to p_out, or
   the actual tribev2 cross-modal alignment graph once it is exported as adjacency)
   would give the falsifier real headroom — the current FAIL is real for these
   substrates but should not be over-generalized.

## Handoff

Next-cycle candidates if anima-domain QW work continues:
- (Q1) Replace synthetic EEG16 with real `anima-eeg` 16-channel session (1 min,
  band-passed 4–40 Hz, Hjorth-referenced; export PLV as adjacency).
- (Q2) Add coined DTQW + Szegedy walks + heat-kernel as further baselines, all under
  the same PCA-row-embedding protocol.
- (Q3) If tribev2 emits a true knowledge-graph adjacency (currently it is an fMRI
  prediction transformer, not a relational graph), re-run on that.
- (Q4) Calibrate F-QWALK-1 threshold against baseline-headroom (require Δ > 5 pp **of
  remaining headroom**, i.e. Δ / (1 − rw_acc) > 0.05) before re-spawning.

Constraints honored: raw#9 (no GPU/no remote spend), raw#15 (deterministic seed,
falsifier pre-declared), raw#10 (artifacts at both spec'd paths + marker + handoff).
