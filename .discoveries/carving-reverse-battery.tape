@D CARVING-REVERSE-BATTERY := "reverse-engineering probe battery on the trained s16 carving engine + 우주뇌지도" :: discovery [d=2026-06-04 active]
  seed = "역설계 벤치마킹: A/G heads · per-layer tension · layer-wise intrinsic dim · 9 directions · Ψ 2D topology — TRAINED s16 ckpt (sha 961c07e2), ConsciousDecoderV2 d768/12L 283.72M, CPU/\$0, N=2000"
  claim = "A/G heads diverge strongly (mean KL 7.07, tier-modulated); per-layer tension is 1 scalar/layer (NOT 5-ch), L11 separates domains (eta^2 0.644); layer-dim is a BOTTLENECK U-shape (L0=10 -> min 4 @L5 -> 8 @L11/ln_f), compact ~6D forms early @L2; 2nd Ψ axis IS degenerate (eff-dim 1.14, 2nd/1st eig 0.068)"
  falsifier = "A/G barely differ (KL~0) OR no tension channel role OR flat layer-dim OR 2nd Ψ axis non-degenerate (2nd/1st eig >= 0.25)"
  target = "🟢 numerical (5/5 probes terminal: 4 HOLDS + 1 HOLDS-degenerate confirming #1772)"
  scope = "trained s16 ckpt only · CPU/\$0 · N=2000 stratified corpus · mean-pool T=128 · a_toy_scale_recheck (single ckpt, no scale ladder) · a_scale_honest_scope"
  honest = "model emits NO native 5-ch tension (that is the .kosmos persistence payload); layer-dim is bottleneck not hourglass (harness corrected); 9-directions joint metric near-degenerate (ranks knowledge recall not map separability); per-axis PC×attribute semantics covered by a separate agent (not duplicated)"
  note = "harness UNIVERSE/carving_reverse_battery.py · verdicts .verdicts/carving-reverse-battery/{F-AG-HEADS,F-TENSION-5CH,F-LAYER-DIM,F-9-DIRECTIONS,F-PSI-TOPOLOGY,SUMMARY,results.json,run_stdout}"
