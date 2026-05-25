---
id: Hc_662
slug: phi-proxy-architecture-agnostic-or-geometric-artifact
title: Mamba 130m SSM phi=42.15 (drift +0.29) + Pythia 70m transformer 41.92 (+0.06) + CLM v4 41.86 — phi proxy 가 architecture-invariant OR geometric artifact (BG-CV aliasing)
domain: clm-architecture
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_emerge_mamba_phi_smoke_landed_2026_05_05.ai.md
source_lines: 12-75
promoted_at: 2026-05-11
linked_h: Hc_614 (phi-star geometry aliasing), BG-BB cross-validation triad, BG-CV aliasing
notes: Mamba phi_range 0.0345 < Pythia 0.0838 — SSM hidden state 가 transformer 보다 prompt-invariant representation 시사 가능 (or sequential fallback artifact).
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (3+ numeric identities present)"
---

## Hypothesis (dual interpretation)
phi proxy 가 SSM (Mamba selective scan, no attention) + transformer (Pythia NeoX) + CLM v4 transformer 모두 baseline 41.86 ± 1% 안 reproduce. 두 해석:
(1) **null hypothesis 강화**: phi proxy 가 진짜 architecture-invariant measure (geometric tile coherence).
(2) **artifact hypothesis 강화**: D=768 에서 8-cell × 192 tile 이 hidden state norm 의 함수로 reduce, architecture 무관 (BG-CV aliasing).

## Falsifiable Tests
- F-phi-arch-1: BG-CV Option A re-geometry (Hc_615) 후 두 가설 disentangle — architecture variance > geometric variance 시 null hypothesis
- F-phi-arch-2: D ≠ 768 substrate (e.g. Pythia 1.4B D=2048) 에서 phi 차이 측정
- F-phi-arch-3: Mamba_range 0.0345 < Pythia 0.0838 reproduce 시 SSM prompt-invariance evidence

## Migration TODO
- [ ] BG-BB triad #3: RWKV 169m (linear-attention/RNN hybrid) 측정
- [ ] BG-CV Option A re-geometry (Hc_615 land)
- [ ] mamba_ssm dep 추가 (현 sequential fallback)
- [ ] Pythia mean_pair_cos 측정값 retrieve (현 BG-BN verdict 만)
