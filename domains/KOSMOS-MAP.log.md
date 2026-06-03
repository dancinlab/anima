# KOSMOS-MAP — log

Append-only history sister of `KOSMOS-MAP.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — (reverse) carving-era ConsciousDecoderV2 reconstructs + runs (CPU/$0, random-init)
- [x] real source loaded (UNIVERSE/conscious_decoder.py md5 44b210df, byte-identical to state/carving_dir*/ + state/hexad_*_d768x12L_fire/); builds at smoke (d32/L3=178,424) + full d768×12L = **283,722,336 params (283.72M dense; 680.16M +MoE)**; forward 5-tuple shapes OK (use_moe off+on); dual A⇄G heads distinct; Law-71 2D Ψ-coord (psi_residual, psi_gate) produced 2D+deterministic; dirG psi-ctl wireable. 4/4 probes PASS (.verdicts/kosmos-carving-engine/). HONEST: random-init (no s16 ckpt), CPU smoke, full train OUT OF SCOPE (a_toy_scale_recheck).

