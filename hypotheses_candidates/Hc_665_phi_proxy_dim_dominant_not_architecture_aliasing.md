---
id: Hc_665
slug: phi-proxy-dim-dominant-not-architecture-aliasing-bg-cv
title: RWKV 169m phi=42.14 (drift +0.28) ≈ Mamba 130m +0.29 (둘 다 D=768) vs Pythia 70m +0.06 (D=512) — phi drift 가 architecture 아닌 hidden_dim sensitive (BG-CV aliasing 강화)
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_emerge_rwkv_phi_smoke_landed_2026_05_05.ai.md
source_lines: 1-80
promoted_at: 2026-05-11
linked_h: Hc_662 (dual interpretation), Hc_614 (geometry aliasing), BG-CV
notes: 3 architecture classes (transformer/SSM/linear-attn-RNN) 모두 41.86~42.15 band. Mamba vs RWKV drift 차이 0.6% (둘 다 D=768). Pythia D=512 만 outlier.
---

## Hypothesis (artifact hypothesis 강화)
phi drift 가 architecture 가 아닌 hidden_dim sensitive — D=768 substrate (Mamba +0.2863, RWKV +0.2806) drift 거의 동일 (차이 0.6%), D=512 (Pythia) 만 다른 band (+0.0616). 8-cell × 192 tile 이 hidden state geometry 의 함수로 reduce, architecture 무관. D=768 substrate 는 tile boundary 가 동일 위치, D=512 는 wraparound 다름 (BG-CV aliasing 강화).

## Falsifiable Tests (triad complete)
- F-phi-arch-dim-1: D=1024 substrate (e.g. Pythia 410m, LLaMA-tiny) drift 가 D=768 과 다른지
- F-phi-arch-dim-2: D=192 multiple (e.g. D=384, D=1152) 가 D=768 과 동일 drift 면 tile-boundary-함수 확정
- F-phi-arch-dim-3: BG-CV Option A re-geometry (Hc_615) 후 D-sensitivity 사라지면 artifact 확정

## Migration TODO
- [ ] Hc_615 Option A rank-invariant partition 후 D-sensitivity 측정
- [ ] D=1024 / D=1280 / D=2048 substrate 추가 측정 (Pythia 410m / GPT-Neo / Pythia 1.4B)
- [ ] tile boundary phase mismatch (D mod 192) 와 drift 의 상관계수 산출
- [ ] null hypothesis (architecture-invariant) 정식 reject
