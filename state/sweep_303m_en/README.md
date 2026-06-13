# state/sweep_303m_en — 303M-EN recipe sweep ledger

`ledger.jsonl` = the leaderboard + crash-recovery record for the 303M-EN ByteGPT recipe sweep
(MODEL.md `anima-303M-RETRO`, ENGLISH-FIRST, A-language layer). One JSONL row per run event:
`{config, host, step, val, G0_kwr, G1, G2, status, ckpt_path, nparam, axes, ts}`.

Sweep finds the A (language) recipe — coherent (G0 kwr>=0.50) + emergent recombination
(G1 super-additive) + corpus-absence novelty (G2). The anti-fabrication layer (A3/G5) is
RETRO and gated separately on H_1147. RETRO head NOT added here (RETRO-ready, not RETRO).

Harness: `UNIVERSE/sweep_303m_en_{prep_corpus,train,run.sh}.py` — reuse the H_1129 model +
frozen evaluators verbatim. Trains detached (nohup) on aiden so it survives an SSH drop.
The live ledger lives on aiden at `state/sweep_303m_en/ledger.jsonl`; harvested back here.
