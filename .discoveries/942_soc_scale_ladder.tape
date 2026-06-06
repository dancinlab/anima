@H 942_soc_scale_ladder := "H_931 SOC scale-up ladder" :: universe [active]
  id      = "H_942"
  seed    = "H_931 found 🟢 SOC (local firing-rate homeostat self-tunes to edge-of-chaos Φ-peak) on live AKD1000 but at ONE toy rung (N=16); does it hold across a pool-size ladder or is it toy-N-only?"
  method  = "reuse h927/h931 dynamics + phi_silicon_proxy + controller VERBATIM (local homeostat r*=0.5, NO peak knowledge) over N=16,64,256; perturb both sides (K0=2/12) + no-feedback control per rung; THRESHOLD scaled with IN so gap(K=4)=0 rung-invariant; scale-invariant K-space convergence gate; g5 CODE-measured"
  verdict = "🟢 F-H942-SOC-SCALE-ROBUST — homeostat self-tunes to sweet spot (|tailK-PEAK_K(4)|<0.4 everywhere, tailΦ 0.24-0.27 ≥0.5·rung-peak) from BOTH sides at ALL 3 rungs (N=16,64,256); no-feedback control fails every rung. SOC scale-robust (K-space scale-invariant). NOTE: absolute POT-gap secondary gate (N=16-frozen, 1 K-step=8 POT) flags larger N because POT∝IN — units artifact of N-naive tolerance, NOT SOC failure (homeostat lands K≈4 every rung)."
  tier    = "🟢 numerical (CPU-mirror, $0 local, no GPU/no chip)"
  scope   = "CPU-mirror NOT on-chip (AKD1000 unreachable from Mac + N>16 exceeds single NP→AKD1500); byte-exact mirror of h927/h931 LIF + phi_silicon_proxy; NO on-chip claim (a_lane_akida_gpu_split); on-chip + larger-N re-confirm = pi5-akida/hexa-lang handoff; 3-rung ladder (≥3 satisfied)"
  verdict_path = ".verdicts/942_soc_scale_ladder/soc_scale_ladder.txt"
