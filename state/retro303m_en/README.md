# anima-303M-RETRO ledger — one JSONL row per eval (created on first queue fire).
# axis-4 of the 303M campaign: H_1129 303M ByteGPT backbone + H_1147 RETRO copy/cross-attn head
# over a PRIOR-WINDOW self-retrieval anchor stream (inference: retrieved kosmos anchor via kosmos_io->brain).
# fire condition: ByteGPT sweep 4/4 done AND (ConvMoE queue returned OR GPU idle); consumes the sweep winner recipe.
