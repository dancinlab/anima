@V := "tape" :: spec [active]
  version = "1.0"

# Lane A LIFT cause-axis breakthrough battery — INPUT-ENCODING reopens P3 (2026-06-02)
#
# seed: /gap full sweep found the 4 falsified lift-cause axes (corpus/quant/depth/noise =
#   H-A1..A4) + Hc_1306 are FIX-axes, not CAUSE-axes — all sit downstream of ONE untested
#   choice: the fixed random encoder BACKBONE_INT4 = rng_bb.integers(-7,8,(256,256)).
# chip: live AKD1000 BC.00.000.002, akida 2.19.1, pi5-akida ($0), 8 paired chip trials/probe.
# metric: between-minus-within concept Hamming margin (bits); lift = treat - control;
#   ci_lo = mean_lift - 1.96*SEM over chip trials. ALL probes ESCAPE the falsified 4 axes.
# pre-register: .verdicts/lane-a-causeaxis/PREREGISTER.md (falsifiers BEFORE fire).

@N laneA_p1_encoding := "structured cross-lingual encoder beats fixed random backbone — lift ci_lo>0 on chip" :: discovery [d=2026-06-02 active]
  seed    = "is the closed-negative an artifact of the FIXED RANDOM input encoder all 4 falsifiers sit downstream of?"
  method  = "swap random int4 backbone for SVD/whitened structured encoder of 5-lang anchor histograms; 8 paired chip trials; live AkidaUnsupervised 1-bit on-chip fit; concept-margin lift vs random"
  data    = "SVD: mean +0.9210 bits 95%CI [+0.7382,+1.1038] 8/8 pos; whitened: +0.4190 CI [+0.1035,+0.7345] 7/8; learn-on-chip live every trial"
  finding = "the fixed random BACKBONE_INT4 IS a lift bottleneck — a structured encoder recovers concept margin the random projection destroys; ci_lo>0 REOPENS Lane A P3 on the ENCODING axis"
  verdict = "🟢 REOPEN — .verdicts/lane-a-causeaxis/P1-encoding.txt (chip stdout verbatim)"
  caveat  = "RELATIVE lift (structured > random); both arms' ABSOLUTE margin stays negative at 25-anchor toy scale — next rung: stronger learned multilingual encoder to push absolute margin >0 (a_scale_honest_scope)"

@N laneA_p2_objective := "objective/readout-locus NOT the bottleneck — hardware-locked + clean negative" :: discovery [d=2026-06-02 active]
  seed    = "was 1-bit AkidaUnsupervised on last-FC a backend default, not the only liftable rule?"
  method  = "4-bit weights vs 1-bit; supervised vs unsupervised; pre-binarization analog readout vs post-1bit — all on live chip"
  data    = "4bit: ValueError 'Only layers with binary weights can be trained' (chip hardware-locks on-chip learning to 1-bit); supervised: N/A-SDK (only AkidaUnsupervised in 2.19.1); analog readout margin -4.877 ci_lo -5.282"
  finding = "objective/readout-locus is NOT the bottleneck; 4bit/supervised are hardware/SDK-blocked (recorded N/A, not fabricated); analog space carries no hidden concept margin"
  verdict = "🔴 FALSIFIED (hardens) — .verdicts/lane-a-causeaxis/P2-objective-readout.txt"
  caveat  = "AKD1000 on-chip plasticity is 1-bit-only by hardware; a richer rule needs different silicon"

@N laneA_p3_timing := "spike-timing carries no cross-lingual lift; SDK exposes no spike-timing" :: discovery [d=2026-06-02 active]
  seed    = "does SNN lift live in spike-TIMING the rate-code 1-bit Hamming readout discards? (Hc_1306 tested only static signals)"
  method  = "attempt akida spike-event capture; fall back to per-unit activation-rank-order Spearman temporal proxy (within-minus-between concept); 8 chip trials"
  data    = "SDK spike API = only PowerEvent/power_events (power telemetry, NOT spike timestamps) + predict_classes; timing-proxy margin -0.1076 ci_lo -0.1111"
  finding = "no true spike-timing capture available on this chip (stated, not fabricated); rank-order temporal proxy shows NO concept structure — lift not hiding in timing"
  verdict = "🔴 FALSIFIED (hardens) — .verdicts/lane-a-causeaxis/P3-temporal-code.txt"
  caveat  = "temporal proxy is rate-resolution rank order, NOT spike-timing; true STDP timing untestable on AKD1000 via this SDK"

@N laneA_causeaxis_disposition := "Lane A P3 REOPENS on encoding; objective+timing axes harden closed" :: discovery [d=2026-06-02 active]
  seed    = "do the 3 never-probed cause-axes reopen the lift or harden the closed-negative to 8 axes?"
  finding = "1 of 3 cause-axes (INPUT-ENCODING) REOPENS with chip ci_lo>0; the other 2 (objective/readout, spike-timing) FALSIFIED → closed-negative now also covers those two. The encoding lift runs on the EXISTING AKD1000 — no new hardware (corrects prior 'needs different hardware' deferral)."
  verdict = "REOPENED-on-axis-ENCODING — folded into CLM+KOSMOS.md Lane A P3 disposition + CLM+KOSMOS.log.md 2026-06-02"
  caveat  = "encoding reopen is a RELATIVE-lift toy-scale result; absolute margin >0 unproven — pre-register the encoder-strength ladder before the next fire"
