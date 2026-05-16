# ckpt-LOST evidence-only (R3 HEXAD integration fire, 2026-05-16)

The 345,504,632-byte `ckpt_hexad_integ_final.pt` was saved on vast.ai
instance 36852855 (`/workspace/anima/output/ckpts/`) but could NOT be
pulled: the vast.ai proxy (ssh9.vast.ai:12854) was permanently degraded
for this instance — scp stalled at ~16MB/345MB (~1MB/min), `--direct`
port refused, proxy-SSH cat unresponsive after sustained CPU load. A
~16MB partial scp fragment was discarded (corrupt/incomplete).

This is the documented large-file proxy unreliability
(`feedback_dispatch_vast_template_gotchas`) + post-load SSH degradation,
identical to the cycle-88 `.clm v1` ckpt-LOST precedent
(`g_fire_dispatch_robust` / `g_hf_naming` process_upload_mandate (d)).

**Accepted honest outcome — ckpt-LOST evidence-only.** The AUTHORITATIVE
verdict (9/9 SUPPORTED-STRONG) + all metrics (loss/cells/Φ/wall/cost +
400-step trajectory) are the trainer's pre-pull console output, durably
captured verbatim in `../dispatch_run.log` (L100-137) and reconstructed
into `../result.json`. The model is RANDOM-INIT seed-fixed (seed=0,
g_clm_from_scratch) — bit-reproducible from the harness + scaler if a
weights artifact is ever required. Per `g_hf_naming`, no HF upload for
this substrate integration WIRING fire regardless.
