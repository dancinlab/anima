# deep-mouth depth-ladder — harvest manifest

GPU lane (runpod kcuz5s3ebgh1w7 `anima-g6-deep-1399`, H100-NVL, $2.59/hr) — depth-isolation
ConvMoE ladder testing whether conv-DEPTH (vs the H_1394 L1 single-trunk-layer) reaches the
G6 FALS floor the L24 ByteGPT (H_1362) reached. Width compensated to hold params ≈303M constant
(clean depth isolation). Training COMPLETE (LADDER_ALL_DONE 2026-06-16T17:19:16Z); harvested +
sha256-verified byte-identical; pod terminated.

| rung | n_trunk_layers | d_model | n_params | final_eval_ce | wall_s | .clm sha256 | .pt sha256 |
|---|---|---|---|---|---|---|---|
| L4 | 4 | 3784 | 302,701,338 | 1.37688 | 1916.97 | 34d40c9f…f48a53 | 930abe6e…37dd67 |
| L8 | 8 | 3020 | 302,613,318 | 1.36468 | 1957.21 | 42f2dc3f…a52095 | 95acedd8…af19b4 |

substrate=GPU-torch Lane-P · torch 2.4.1+cu124 · bf16 · 6000 steps · batch64 · seq256 · lr3e-4 ·
corpus=/workspace/corpus_en_dom.bytes (2,262,561,660 B, english-dominant, == H_1394 script-controlled recipe).

artifacts (ckpts gitignored = HF-only per a_hf_registry; jsons+log git-tracked here):
- clm303_L4_d3784.{clm 148M, pt 1.2G} · clm303_L8_d3020.{clm 147M, pt 1.2G}
- L4_train.json · L8_train.json · ladder.log

NEXT (the science payoff): decode each .clm via the now-fixed H_1403 streaming decode + run the
H_1392/H_1403 FROZEN G6 FALS detector VERBATIM → does conv-DEPTH (L4/L8) lift FALS over the L1
H_1394 FALS=0? CE alone (L8 1.365 ≈ L4 1.377, both ≈ L1) suggests depth barely moves next-byte CE;
the FALS-vs-depth verdict is the open deep-mouth question (a_toy_scale_recheck · a_verified_must_wire).
