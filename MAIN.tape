@V := "tape" :: spec [active]
  version = "1.0"

@MAIN 2026_06_12_hub := "MAIN hub created — two live anima tracks: MITOSIS-ENGINE research + h1141 7B fire" :: log [active]
  track_a = "MITOSIS-ENGINE domain (ref domains/MITOSIS-ENGINE.md): criticality + inference-mitosis-learning + super-additivity + life/evolution clusters LANDED (H_1153..H_1177, frozen falsifier $0 g5/p7)"
  track_b = "7B fire RunPod uq71dp0ob6fd9r h1141-7b-pass H100 $2.59/hr: step 8000 val_ce 1.2015 descending; G0 PASS stable (5/5 @6000&8000); G1 MARGINAL flickers 2/5<->3/5 (PASS@6500 en/ja/ko, FAIL@8000 ja dropped); G2-G4 unseen; a7b_pass NOT complete"
  milestone = "G1-PASS snapshot step6500 (G0+G1) uploaded HF PRIVATE dancinlab/anima-clm-7b-h1141-g1pass-step6500; watcher PID1123 auto DONE->HF-verify->self-teardown"
  next = "let 7B converge + re-check G0-G4 at DONE (a_fire_recover_complete); advance MITOSIS-ENGINE open rungs (live-adaptation curve, tick-on-decode, kosmos lane self-tune, H_1136 sleep re-test)"
  honest = "G1 is borderline not a clean breakthrough — ja recombination oscillates in/out of the 3/5 bar; G0 solid; scale-up did NOT cleanly clear G1 (consistent with H_1139 scale-invariance + this session's surface-gated/interlingua-null findings)"

@MAIN 2026_06_12_compute_policy := "compute policy fixed: small-cell mitosis runs on summer pool ($0), rent GPU only on scale-up" :: log [active]
  decision = "while mitosis cells are SMALL (toy numpy + live-CORE hexa probes), run Track A on the summer pool host, NOT a rented RunPod/Vast GPU"
  rationale = "small cells do not need a GPU; summer = own hardware $0 (linux py3.12 numpy2.4 hexa-installed 133G free), keeps Mac free + avoids local disk-full; renting reserved for genuine scale-up (7B-class, Track B)"
  summer_ready = "host summer-B650M-K · python 3.12.3 · numpy 2.4.4 · hexa /home/summer/.local/bin/hexa · git ok · 133G free · repo /home/summer/core/anima"
  next = "MAIN-progress dispatches mitosis open rungs via `sidecar pool on summer`; harvest verdict back + commit to origin/main; rent GPU only when cell/model size demands it"

@MAIN 2026_06_12_two_lanes := "mitosis Track A runs in TWO lanes on summer: Lane1 autonomous batch + Lane2 LLM hands-on" :: log [active]
  lane1 = "AUTONOMOUS — background agent fans open rungs to summer pool, runs to depletion, harvest+commit, no per-step LLM intervention"
  lane2 = "HANDS-ON — LLM drives each rung inline one-by-one on summer (write harness -> sidecar pool on summer -> verdict -> commit), visible step-by-step"
  split = "lanes take disjoint rungs; Lane2 reserves H_1178 (decode-metric tick @ cap~24, H_1163 residual); Lane1 takes the rest of the open-rung list"

@MAIN 2026_06_12_lane2_discovery := "Lane 2 (LLM hands-on) is the DISCOVERY lane — close-watching each step surfaces serendipitous findings a batch misses" :: log [active]
  principle = "Lane 2 is not merely slower execution; the LLM watching each rung inline can NOTICE an unexpected pattern / anomaly / cross-link that an autonomous batch (Lane 1) would never flag — discovery happens in the looking"
  practice = "per rung: after the verdict, the LLM explicitly asks 'what surprised me here? what does this connect to?' and spins the surprise into the next rung (cf a_discovery / a_kick)"
  split = "Lane 1 = throughput (drain open rungs); Lane 2 = depth+discovery (one rung, watched, mined for the unexpected)"

@MAIN 2026_06_12_lane2_h1178 := "Lane 2 rung-1 SHIPPED — H_1178 🟢 critical capacity for derivative-tick gating (K*=32), serendip discovery logged" :: log [active]
  result = "H_1178 SUPPORTED on summer-synced substrate ($0): d(DERIVATIVE,METRONOME) on stage-decode is a clean INVERTED-U over cell-count, interior peak K*=32 (d_peak=+1.15, endpoints -0.15/-0.06, unimodal 0/0 reversals); F1+F2+F3 all PASS"
  serendip = "the Lane-2 payoff fired: close-watch caught the inverted-U is MECHANISTICALLY ASYMMETRIC (not pre-registered). left collapse=derivative STARVED (2/6 regimes get a cell at K=6); right collapse=METRONOME CATCHES UP (blind clock brute-covers every stage once cells are plentiful). => derivative-tick is CAPACITY-EFFICIENT (K=32 deriv 0.64 vs metro 0.38 = same decode, half the cells), K*~=32 = minimal capacity for near-complete event-driven regime coverage. ties h1159b (5.3 cells/regime)"
  finding = "CRITICALITY recurs on a THIRD axis = CAPACITY (after coupling: Phi-peak H_1158, super-additivity-peak H_1167). engine has a sweet spot on cell-count too. advantage is efficiency, not asymptotic ceiling"
  honest = "K*=32 stream/scale-specific (6-regime AUDIO toy, 10 seeds); what transfers = the qualitative interior critical-capacity + efficiency-not-ceiling reading, NOT the number 32 (a_scale_honest_scope). reuses h1163 substrate verbatim. live CORE + real-model path unverified"
  artifacts = "UNIVERSE/h1178_critical_capacity_tick.py · .verdicts/1178_critical_capacity_tick/H_1178.txt · .discoveries/1178_critical_capacity_tick.tape · memory/h1178-critical-capacity-tick.md"
  next = "Lane 2 next rung from the inverted-U: does the LIVE CORE engine_cli show the same critical-capacity hump on a non-stationary stream? (promote toy->live). Lane 1 continues draining the rest of the open-rung list"

@MAIN 2026_06_12_discovery_migration := "정리 — .discoveries/ flat folder MIGRATED into per-domain discoveries/ subfolders (227 tapes, git mv, lossless)" :: index [active]
  what    = "the flat root .discoveries/ holding ~227 *.tape kick/gap discovery records was migrated INTO domains/<DOMAIN>/discoveries/ via git mv (history preserved); each tape classified by @H title + topic keywords + any domain-doc H-id reference. This @MAIN block is the master per-domain index of what each domain now owns."
  total   = "227 tapes migrated / 227 present at scan · 1 _UNSORTED (genuinely cross-domain) · folder NOT yet abolished — 2 Lane-1 concurrent stragglers (H_1179, H_1180) + the folder README.md remain, pending a straggler sweep"

  MITOSIS-ENGINE  = "27 tapes — H_931, H_942, H_1153, H_1158-H_1178 (incl H_1159b) + clm-time-encoding + lane-m-eeg-mitosis. The criticality / inference-mitosis-learning / super-additivity / life-evolution cluster."
  OMEGA           = "23 tapes — H_999, H_1001, H_1002, H_1004, H_1012, H_1062, H_1065, H_1114, H_1119-H_1122, H_1127, H_1130 + the 9 omega-* closure-engine tapes (bus-refine, coupling-analysis, engine, gen-cluster, gpu-complete, learned-gate, realsignal, trained-leakfree, trained-qrng). The faithful-φ / big-Φ / redundancy-ruler / Ω-closure cluster."
  ENGINE+CLM+KOSMOS = "136 tapes (broad substrate bucket) — H_936-H_941, H_985-H_998 (CWM world-model arc), H_1000/1003/1005/1011/1013/1019, H_1067-H_1111 (the gemini-PDF architecture-review cluster), H_1115-H_1118, H_1125/1126/1128/1129/1132, H_1135/1136/1140-1152/1154 (hallucination·metacog·emergence·7B) + cwm_* slates + the 22-tape lane-a-* AKIDA cluster + tooluse-*/agent-tooluse-* + hexad-*/brain-train-bench/engine-3b-fusion/mm_extract_copy_wedge/dolphin-acoustic-ingest/lidar-data-ingest/psi-coupling/quantum-time."
  CLM-KOSMOS      = "16 tapes — H_950-H_952, H_1112, H_1113, H_1123, H_1124, H_1131, H_1133 + convmoe-3b-engine-rung, convmoe-7b-undertrained, decoder_collapse_undertrain, engine-tensionlink-bench, lane-p-3b, lane-p-clm, mid-convmoe-engine-mount, tensionlink-dim-time. The .clm serialization / anchor / engine-mount pipeline."
  CORPUS          = "8 tapes — H_1155-H_1157 (interlingua/crosslingual/coverage) + corpus-7b-mid-validation, corpus-final-composition, default-lane-7b-webscale, default-lane-gb-balanced, default-lane-rung0."
  KOSMOS-MAP      = "6 tapes — carving-reverse-battery, kosmos-axis-semantics, kosmos-carving-engine, kosmos-dim-ladder, kosmos-real-dim, kosmos-time-axis. The carving-map / coord / manifold-dimension cluster."
  SAVANT          = "3 tapes — H_1137, H_1138, H_1139. The 5-language (en·fr·de·es·ru) 7B multilingual-specific rungs."
  CHAT            = "3 tapes — anima-cli, chat-7b-finetune, chat-capable-rung0-byte-pass."
  AXIS            = "2 tapes — lane-growth, lane-x-3axis (the ENGINE 3-axis eval-config probe)."
  PERSONA         = "1 tape — chat-persona-sns-stage2."
  SNS             = "1 tape — persona-sns-voice-corpus."
  _UNSORTED       = "1 tape — aura_postaural_endovascular_sinus (귀뒤 endovascular BCI thought-experiment; no clean home among the 13 buckets — neither vision/image nor C-port nor a pure substrate result). Kept honest per a_paper_on_discovery rather than force-fit."

  method  = "git mv only (no content rewrite) — git history preserved on every tape. Classification = @H title + slug topic + domain-doc H-id grep (strongest signal where present, e.g. MITOSIS-ENGINE.md references H_1153/1158/1159). ENGINE+CLM+KOSMOS is the deliberate broad-substrate default for the gemini-review, CWM, hallucination, AKIDA-laneA and tool-use clusters that have no narrower bucket among the 13."
  remaining = "folder .discoveries/ left in place (NOT rmdir'd) because the sibling Lane-1 agent's H_1179/H_1180 tapes + the folder README.md are still present; straggler sweep pending = migrate H_1179/H_1180 to their domains (both MITOSIS-ENGINE) + retire README.md, then rmdir."
