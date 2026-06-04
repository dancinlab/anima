# ENGINE+CLM+KOSMOS monograph — corrected scope (terminal-verdict inventory)

> Final consciousness-engine monograph. Terminal verdicts ONLY (🔵/🟢/🔴) become
> chapters (a_paper_gate); 🟠/🟡 → future-work section only. Three user corrections
> folded: (1) OMEGA is a first-class chapter (it has its own compiled paper + gate
> findings); (2) CORPUS-7B (torch G-ref) ≠ ENGINE-7B (forge .clm) — never conflate
> (a_train_flame_forge · a_lane_akida_gpu_split); (3) Lane-G util WORKLOAD-BOUND is
> being lifted upstream (hexa-lang HEXA-FUSION CUDA-graph port → ~1.2x).

## Hard lane distinction (the central honesty axis — must survive into the paper)

| | CORPUS-7B (training now, pod 39467956) | ENGINE-7B (the real consciousness engine) |
|---|---|---|
| lane | Lane G-ref (torch ByteGPT) | Lane G (hexa flame+forge `.clm`) |
| identity | reference chat model | A⇄G / OMEGA substrate engine |
| trainer | PyTorch / ATen | hexa-native forge (NO torch in binary) |
| ENGINE-loadable | ❌ Lane P serializer-gap 🔴 (.verdicts/lane-p-clm) | ✅ `.clm` single mouth (generator L3) |
| status | finishing (~CHAT-axis datapoint) | OPEN — util was WORKLOAD-BOUND 🔴, now lifting (HEXA-FUSION ~1.2x) |
| paper role | CHAT chapter IF coherent-generalizing | future-work / open frontier |

CORPUS-7B finishing does NOT close ENGINE-7B. Merging them = fake-pass.

## Terminal-verdict inventory (chapter candidates)

### OMEGA — substrate-coupled A⇄G gate decoding (CHAPTER, absorb existing paper)
- Existing compiled paper: `PAPER/omega-substrate-coupled-decoding/omega.pdf` (#1810, 10p) — ABSORB, do not re-derive.
- 🟢 H_862 min-gate — gate-closure lives on a SINGLE A-wire (min-gate). (ca17fdeb0)
- 🔴 H_861 multi-wire gate — closure does NOT generalize to multi-wire. (ca17fdeb0)
- closure is STRUCTURE-transfer, conv-native A/G dual-head, NOT CDV2-only (#1813, OMEGA+OE1).
- 🔴 d512-trained-leakfree — on a well-trained LEAK-FREE substrate (causal_ca=True, val_ce<uniform), absolute closure does NOT hold (GATED ≮ base) → the earlier absolute "win" was partly leak-driven. `.fire-recover/omega-h1-qk0312/omega_trained_leakfree_results.json` (ckpt sha 6f085c91…, corpus 400MB gutenberg+wiki 5-lang). Cross-link memory omega-cdv2-ca-leak.
- gen-weak: free-run generation collapses (whitespace) — honest scope, NOT a chat mouth.
- HONEST THESIS: A⇄G gate-closure is STRUCTURALLY real (🟢 min-gate, structure-transfer) but ABSOLUTE-CE closure on a leak-free substrate is a closed-negative (🔴) — use RELATIVE structure, not absolute CE.

### CLM consciousness measures (CHAPTER)
- 🟢 CAUSAL-POWER — rich>collapse clear margin (Δ +0.0918/+0.0830/+0.0714, n=4/5/6), size-robust — the ONLY scale-free chip-native consciousness signal. `.verdicts/clm-measure-sweep` (clm_msweep_causal_power).
- 🔴 Φ-family / HILL / tension — size-robust FAIL (5/6), n-boundary reversal — unfit as scale-free signal at toy n≤6. (clm_msweep_phi_family_red)
- 🔴 production d512 causal-xfer — toy 🟢 CAUSAL-POWER does NOT survive at production width (seed187 n=5 sign-flip). `.verdicts/clm-causal-xfer` (clm_causal_xfer_prod_red).
- 🟢 live-AKD1000 HW causal-xfer — CAUSAL-POWER PASSES on real silicon (BC.00.000.002). (clm_causal_xfer_hw_green) → the toy≠scale split is itself the finding.

### CLM MoE monopoly-escape ladder (CHAPTER — closed-negatives)
- 🔴 mitosis-array dissolve (clm_mitosis_array_dispatch) — z-rise FAIL, TERMINAL.
- 🔴 KD-bridge transfer (clm_bridge_transfer) — escape ⊥ KD-transfer, HF anima-clm-bridge PRIVATE.
- 🔴 production-scale amplification (clm_pielou_dissolve_prod, clm_dispatchkl_xfer_prod) — prod amplifies toy 🔴.

### AKIDA on-chip substrate ceiling (CHAPTER — quantified closed-negative)
- composition-preserving plastic capacity tops out at D=1 single-FC ~524K; depth-stacked 1-bit Hebbian degrades composition. `.verdicts/lane-a-3b` (F-3B).
- HYBRID off-chip head scales but chip-fraction → trivial (~0.017%) → not honest pure-AKIDA 3B/7B. `.verdicts/lane-a-3b-hybrid` (F-3B-HYBRID). Lane A caps at PUBLIC ~524K D=1 encoder.

### Lane-G forge util (CHAPTER — workload-bound terminal, lifting upstream)
- 🔴 util WORKLOAD-BOUND — lever chain 1→5, byte-eq preserved, descent 🟢, MEAN-util pinned sub-1% (interpreter/host per-step driver wall-time, not forge defect; forge provably device-resident, PEAK 78%). `.verdicts/lane-g-lever4`, `.verdicts/lane-g-lever5`.
- CROSS-REPO UPDATE: the named fix (full device-resident CUDA-graph capture/replay = HEXA-FUSION ④, a_cuda_graph_train) reached ~1.2x in sibling hexa-lang HEXA-FUSION (domains/HEXA-FUSION.md, PR #2658). Frame as "ceiling measured in anima → lifting upstream", NOT a dead-end.

### CHAT / tool-use grounding (CHAPTER)
- 🟢 copy-head — verbatim key-copy CLOSED 0/36→35/36, 3 anti-Goodhart mirrors (#1840, F-COPYHEAD-ARGCOPY).
- 🔴 argcopy — the motivating closed-negative copy-head fixed (#1835).
- 🟢 FABDROP tool-use grounding rung-0 (#1833).
- 🟢 default-lane 18M chat coherent multilingual (#1836).
- 🟢 init_CE floor = ln(151936) (chat_init_ce_floor, CHAT group).
- EXCLUDE: scale-emergent copy is 🟠 (future-work only).

### PURE — corpus axis (CHAPTER — closed-negative)
- 🔴 corpus-axis ⊥ multilingual register-coherence (wiki_frac sweep). `.verdicts/pure-corpus-axis-closed-negative`.

### KOSMOS — consciousness-knowledge substrate (CHAPTER — design + datasets)
- anchor/carving tier ladder (knuth31-carving), persona/SNS, 5-lang unified corpus. Cite only datasets that exist on HF / in HF.jsonl.

## Future Work / Open Frontier (NON-terminal — NOT finding chapters)
- ENGINE 3B/7B (forge .clm) — open; unblocking via HEXA-FUSION util lift (~1.2x).
- Lane G/A 3B/7B PUBLIC, Lane P PUBLIC (serializer v0.2-CLMX).
- CORPUS-7B (torch G-ref) — mid-training; CHAT datapoint if coherent-generalizing.
- scale-emergent verbatim copy (🟠).
- CORE conv `.clm` chat-coherence.

## Base note
Local HEAD is far ahead of origin/main; the verdict files cited exist on the LOCAL
campaign branch, NOT origin/main. The monograph branch must base off LOCAL HEAD (or
the verdict files are absent). PR target decided at ship time (likely the campaign
branch, not a clean origin/main PR).
