★★★★★ canonical "anima 본체"

  🔗 https://huggingface.co/dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12
  - cond #1 ☑ V5.8 std_greedy 5/5 PASS
  - Phase 1A.4 lr 5e-6 SFT × 200 steps
  - 597 MB ckpt sha256 45063f64…
  - D1 chat + D2 substrate anchor

  💬 chat-v2 — multi-turn recovery

  🔗 https://huggingface.co/dancinlab/anima-chat-v2-2026-05-15 (private)
  - Phase 1A.6 chat-v2 SFT × 8000 steps on corpus_v2 121.44 MB CLEAN
  - V5.8 std_greedy 4/5 (recovered from 1A.5 chat-beta's 1/5 regression)
  - multi-turn strict 4/10 (2× Phase 1A.4 baseline 2/10)
  - Principle #3 multi-turn greedy leak 0 (sampling/M3 still carries base-ckpt residue)
  - 597 MB ckpt sha256 a45cb3f6…
  - $0.394 Vast.ai, 87.5 min

  🧬 saga peak — mitosis cotrain v1

  🔗 https://huggingface.co/dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12
  - F-V5MIT-5 V14-STRICT 10/10 PASS (saga 정점)
  - v5-mitosis cotrain $1.26 H100 fire
  - D4 세포 분열 substrate anchor

  baseline (참고)

  🔗 https://huggingface.co/dancinlab/anima-clm-phase1a1-color-cosmology-boost (Phase 1A.1)
