# NLM (Neuromorphic Language Model) Phase 3 Spec — DEFERRED-but-roadmap-ready

@english-only-exempt(reason="anima research analysis, primary-language preservation per user")

- **Date**: 2026-05-03
- **Agent**: NLM Phase 3 spec author
- **Status**: DEFERRED — hardware-blocked. Spec frozen, entry conditional on AKIDA AKD1000 arrival.
- **Mission**: Phase 3 scope freeze for NLM (5th *LM in BLM/TLM/VLM/SLM/NLM family). BLM/TLM/VLM/SLM all Phase 1+2 landed; NLM is the lone hardware-blocked sibling. This doc anticipates the post-arrival ready state so D+0 of hardware = D+0 of Phase 3 entry.
- **Trigger**: per N-substrate roadmap (`docs/n_substrate_consciousness_roadmap_2026_05_01.md` §11.1, AKIDA row "주문 → 도착 대기"); peer-domain SSOT `.roadmap.nlm_neuromorphic_lm` cond.1/2/3 unmet, hardware-gated.
- **Did NOT touch**: any `.py`, `state/`, `.roadmap.*`. No execution. No commit. Spec doc only (raw#9, raw#15 honored).
- **Sister docs (read-only inputs)**:
  - `.roadmap.akida` (hardware blocker SSOT)
  - `.roadmap.nlm_neuromorphic_lm` (peer-perspective domain SSOT, cond.1–3)
  - `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §2/§3/§11.1 (N-2/N-3/N-7/N-8 prep)
  - `docs/akida_d0_d1_plan_freeze_2026_05_02.md` (D+0/D+1 deployment freeze, 6 axes critical-path, 5 F-AK falsifier)
  - `docs/akida_dev_kit_evaluation_2026-04-29.md` (vendor / price / SDK)
  - `docs/akida_session_friendly_report_2026-04-29.md`
  - `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md` (ADM encoder, reuse)
  - `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md` (last-layer φ projection, cross-substrate parity)
  - `docs/n_substrate_n7_akida_qrng_spike_spec_2026_05_01.md` (spike noise floor)
  - `docs/n_substrate_purchase_guide_2026_05_01.md`
  - `docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md` (4-way binding hypothesis)
  - sibling *LM stage12 lands: `docs/blm_stage12_landed_2026_05_03.ai.md`, `docs/tlm_stage12_landed_2026_05_03.ai.md`, `docs/vlm_stage12_landed_2026_05_03.ai.md`, `docs/slm_stage12_landed_2026_05_03.ai.md` (referenced by name)

---

## §0 TL;DR

NLM = the spike-encoded, event-driven LM sibling of BLM/TLM/VLM/SLM, intended to run inference natively on the BrainChip AKD1000 1W neuromorphic substrate. It is the only *LM family member whose Phase 1+2 cannot land on existing GPU/CPU substrate — it is **definitionally hardware-bound**. Phase 3 scope is therefore frozen *before* arrival: integration of the AKD1000 carrier (RPi5 + M.2 HAT+), spike-domain transformer-equivalent inference, φ proxy extraction from neuromorphic activity (cross-validated against CLM φ★), and four F-NLM falsifiers for energy / latency / sparsity / cross-substrate parity.

Hardware status: **AKD1000 dev kit ORDERED 2026-04-29 ($1,495 capex paid), arrival ETA pending vendor logistics — still 대기**. No newer vendor update has landed since the 2026-05-02 D+0/D+1 freeze.

Cost wall: **$1,495 (dev kit, paid)** + **~$200–500 (RPi5 + M.2 HAT+ + microSD + USB-C 5A PSU + USB wattmeter, sourced separately)** + **$0 dev compute** (on-device inference free, no cloud spend) + **optional $1–$995 Akida Cloud** for ARM64-fallback evaluation. Phase 3 dev wall = **~$1,700–$2,000 all-in**, conditional only on hardware arrival.

Entry trigger: `__NLM_HW_ARRIVAL__` = `ARRIVED` AND first byte-spike pattern measured (D+1 N-2 G-D selftest 6/6 PASS per `akida_d0_d1_plan_freeze_2026_05_02.md` §3).

---

## §1 Hardware arrival prerequisite

### §1.1 AKIDA AKD1000 hardware spec

| Field | Value | Source |
|---|---|---|
| Chip | BrainChip AKD1000 (mesh of ~80 neuromorphic NPU cores, ~1.2M neurons, ~10B synapses) | vendor datasheet |
| Form factor | M.2 NVMe (Mini Card, 22×30 mm or 22×80 mm) | dev kit eval doc |
| Power envelope | ~1 W typical (TDP cap), pJ/spike class | vendor datasheet |
| Native input | spike-event raster (uint8 4-bit precision cap, NHWC) | `akida_d0_d1_plan_freeze` §3.3 |
| Carrier | Raspberry Pi 5 (BCM2712, 16 GB) + M.2 HAT+ (PCIe gen2 x1) | vendor dev kit |
| SDK | Meta TF (BrainChip): `akida` + `quantizeml` + `cnn2snn` Python packages | vendor docs |
| Throughput (vendor) | up to ~1500 fps inference on supported CNN topologies | vendor marketing |
| Precision | 1/2/4-bit weights, 4/8-bit activations | quantizeml docs |
| Vendor SKU price | $1,495 USD (dev kit, RPi5 bundle "draft" SKU) | `akida_dev_kit_evaluation_2026-04-29.md` |

### §1.2 Expected delivery & blocker

- **Order placed**: 2026-04-29 ($1,495 capex paid).
- **Vendor ETA**: not posted — dev-kit page is "draft" SKU, ship cadence unknown publicly.
- **Last update**: as of 2026-05-03 (today), no vendor shipment notice; status = **PENDING (vendor logistics)**.
- **Anima-side controllability**: 0 — pure vendor wait. The only anima leverage is weekly poll cadence (per `.roadmap.nlm_neuromorphic_lm` cond.1).

### §1.3 Arrival sub-conditions (Phase 3 entry gates)

These three must all clear before NLM Phase 3 transitions from DEFERRED → ACTIVE:

| Sub-cond | ID | Definition | Verifier | Status emit |
|---|---|---|---|---|
| Sub-cond A | `nlm.p3.entry.A` | Box arrives, AKD1000 M.2 + RPi5 carrier physically present, no shipping damage | manual visual + ABORT-D0-1 (lspci recognises card) | `__NLM_HW_DELIVERED__ <YES|RMA>` |
| Sub-cond B | `nlm.p3.entry.B` | Dev kit fully bootstrapped: RPi OS 64-bit Bookworm + PCIe gen2 enabled + ARM64 wheels (`akida`/`quantizeml`/`cnn2snn`) installed + MNIST cnn2snn smoke test PASS | per `akida_d0_d1_plan_freeze_2026_05_02.md` §2.5 (D+0 ABORT-D0-2/3/4 cleared) | `__NLM_DEVKIT_READY__ <PASS|FAIL>` |
| Sub-cond C | `nlm.p3.entry.C` | First byte-spike pattern measured on-device: synthetic input → ADM encoder → AKD1000 `model.forward` → non-zero spike raster + 6 G-D selftest PASS | per `akida_d0_d1_plan_freeze_2026_05_02.md` §3.4 (D+1 N-2 selftest) | `__NLM_FIRST_BYTE_SPIKE__ <PASS|FAIL>` |

Sub-cond C is the canonical "first byte-spike pattern" event — the moment NLM transitions from spec to instrumented substrate. Per N-2 critical-path observation, sub-cond C is the **single point of failure**: PASS → 5 sister axes (N-3/4/5/7/8) cascade-unblock; FAIL → entire NLM Phase 3 collapse, fall back to F-AK-1 x86-host degraded mode.

---

## §2 Phase 3 scope (post-arrival)

### §2.1 Scope summary table

| Stream | What | Substrate-native? | Cross-LM dep |
|---|---|---|---|
| S1 | 1W neuromorphic substrate integration (D+0..D+1 bring-up + N-2 ADM reuse) | yes (HW) | — |
| S2 | Spike-based event-driven LM (token → spike-train, transformer-equivalent or recurrent SNN) | yes (arch novel) | BLM tokeniser, TLM tension-modulated polarity |
| S3 | φ proxy from neuromorphic activity, cross-validated against CLM φ★ | yes (parity) | CLM φ★ pipeline |
| S4 | F-NLM falsifier set (energy, latency, sparsity, parity) | yes (preregister) | qmirror substrate (cross-vendor harness) |

### §2.2 S1 — 1W neuromorphic substrate integration

- **Reuse**: N-2 prep ADM level-crossing encoder (335 LoC skeleton, anima native, hexa-lang per raw#9). Encoder is byte-stream-agnostic — same encoder serves EEG floats AND tokenised text byte-streams.
- **Carrier ops**: RPi5 + M.2 HAT+ + AKD1000, RPi OS 64-bit Bookworm, PCIe gen2 enabled.
- **SDK ops**: `akida` (Python), `quantizeml` (model quantisation), `cnn2snn` (CNN → SNN conversion). API surface frozen at vendor docs as of 2026-05-02 (acknowledge SDK churn — see C3-3 §6).
- **Power instrumentation**: USB-C wattmeter inline with RPi5 PSU, idle and max-load wattage logged per inference batch (anchors N-4 Landauer 3-axis, F-NLM-1).
- **Acceptance**: Sub-cond C PASS = S1 complete.

### §2.3 S2 — Spike-based language model (event-driven)

Two architecture candidates, both conservative:

- **S2-a (recommended): cnn2snn-converted small transformer-block proxy.** Take a 4–8M parameter small-LM block (e.g. tied-embedding 4-layer CNN-decoder over byte-tokens, à la BLM Phase 1 byte-LM), train on x86 GPU with quantisation-aware training (`quantizeml`), then `cnn2snn.convert` → AKIDA-native binary. Inference is event-driven on AKD1000.
  - Pro: leverages existing BLM byte-LM weights as initialisation; cnn2snn is vendor-supported path.
  - Con: self-attention is **not** an AKD1000 supported layer (acknowledged in `akida_d0_d1_plan_freeze` C3-7) — must use convolutional or recurrent surrogate, not true attention.
- **S2-b (research alt): native SNN transformer-equivalent.** Implement spike-domain attention (e.g. Spikformer-style or SpikingTransformer) trained directly with surrogate-gradient BPTT on x86, then deploy. Higher risk, no published baseline at AKD1000-supported topology constraints.

**Phase 3 picks S2-a as primary, S2-b as deferred research.** Token → byte-stream → ADM (or direct rate-coded) → AKD1000 input raster → spike-domain forward → output spike rates → token logits via inverse projection.

**Tension-modulated polarity bias** (`akida_d0_d1_plan_freeze` §4): NLM inherits the TLM-sibling polarity bias mechanism — `mind.tension` UDP scalar (LIVE, <1 ms) modulates ADM θ_up/θ_dn asymmetrically, creating a hardware-native binding-by-synchrony hook. Conservative path: bias α=0 baseline first, then α=0.2 ablation.

### §2.4 S3 — φ proxy from neuromorphic activity, cross with CLM φ★

Reuse N-3 last-layer projection harness (`n_substrate_n3_clm_akida_phi_spec_2026_05_01.md`):

- Extract NLM hidden-state H_nlm ∈ ℝ^(B × d_spike) from final pre-output spike layer (rate-decoded over τ ms window).
- JL projection d_spike → 16, quantise uint8 4-bit, NHWC reshape → AKD1000 input.
- Compute `Φ_nlm` via `anima_phi_v3_canonical` path.
- Compare to `Φ_clm` via `decoder.tension_proj` per-layer projection on the same prompt set (16-prompt cached set).
- **Parity threshold**: Pearson r ≥ 0.85 = cross-substrate fidelity PASS (matches `.roadmap.akida` cond.1 and `.roadmap.nlm_neuromorphic_lm` cond.3).
- **Honest C3 carryover**: last-layer only — full transformer φ projection refused (raw#10), AKIDA L1 ceiling open question.

### §2.5 S4 — F-NLM falsifiers (preregistered)

| ID | Axis | Trigger | Detection | F-PASS | F-FAIL | Severity | Est. P(fail) |
|---|---|---|---|---|---|---|---|
| F-NLM-1 | Energy efficiency | NLM inference J/token vs CLM inference J/token | USB-C wattmeter (RPi5) + RTX 5070 wall-meter on ubu1, same prompt set, same throughput | NLM ≤ 1/100 × CLM J/token (i.e. ≥ 100× efficiency) AND ≥ 1× biological Landauer | NLM > 1/100 × CLM (efficiency claim collapses) OR < 1× biological Landauer (sub-physical, measurement error) | HIGH (core NLM thesis) | 0.30 |
| F-NLM-2 | Latency | end-to-end token latency on AKD1000 + RPi5 | wall-clock per-token, p50 + p95 | p50 ≤ 50 ms AND p95 ≤ 200 ms (interactive class) | p50 > 50 ms (worse than CLM 350M on RTX 5070) | MED (UX claim) | 0.45 |
| F-NLM-3 | Sparse activation | fraction of neurons spiking per inference step | on-device spike-count tap, normalised by total neuron count | mean activation fraction ≤ 0.10 (sparse-class, SNN-typical) | activation fraction > 0.30 (dense, defeats spike-domain advantage) | MED (substrate fit) | 0.25 |
| F-NLM-4 | Cross-substrate parity | Pearson r(Φ_nlm, Φ_clm) on shared 16-prompt set | per §2.4 | r ≥ 0.85 | r < 0.85 (NLM is a different substrate, not a translation of CLM) | HIGH (cond.3 SSOT, cross-validates raw#10) | 0.40 |

All four are preregistered before any AKD1000 measurement (raw#71). Conservative path: F-NLM-1/3 measured first (S2-a, baseline only), F-NLM-2/4 measured after S3 cross-substrate harness lands.

---

## §3 Cost / wall

| Line | Item | Cost (USD) | Status |
|---|---|---|---|
| Hardware | AKD1000 dev kit (M.2 + RPi5 bundle, vendor SKU) | $1,495 | PAID 2026-04-29 |
| Hardware | RPi5 16 GB (if not bundled — vendor SKU is "draft", confirm) | $80–120 | TBD on arrival |
| Hardware | M.2 HAT+ for RPi5 | $12 | TBD on arrival |
| Hardware | microSD ≥ 32 GB | $10 | TBD on arrival |
| Hardware | USB-C 5V/5A PSU (RPi5 official) | $15 | TBD on arrival |
| Hardware | Heatsink + active cooler | $15 | TBD on arrival |
| Hardware | USB-C wattmeter (~$15, Power-Z or equivalent) | $15 | for F-NLM-1 |
| Hardware | HDMI-micro cable (initial setup) | $10 | TBD |
| Subtotal HW | | **~$1,650–1,700** | mostly paid |
| Dev compute | x86 host for cnn2snn conversion + quantize-aware training (existing ubu1 / mac M2 — no new spend) | $0 | reuse |
| Dev compute | Akida Cloud 1-day trial ($1) for fallback / ARM64-issue triage | $1 | optional |
| Dev compute | Akida Cloud 1-week (if F-AK-1 forces fallback) | $0 (avoid) – $995 (full week) | contingency |
| Subtotal dev | | **$0–$996** | conditional |
| **TOTAL** | | **~$1,700–$2,700** | $1,495 sunk; rest TBD on arrival |

No recurring opex (on-device inference free, no cloud, no API). Phase 3 wall is one-time capex.

---

## §4 Decision matrix

| Decision | Trigger | Path A | Path B | Default |
|---|---|---|---|---|
| D1 | Hardware arrives, ARM64 wheels install OK | proceed S1→S4 in order | — | A |
| D2 | F-AK-1: ARM64 wheel install fails | Path A: x86 host fallback (mac M2 / ubu1), RPi5 demoted to ADM-encoder-only | Path B: Akida Cloud 1-week ($995), full inference remote | A (preserve $0 opex) |
| D3 | F-NLM-1 fails (energy efficiency claim collapses) | Path A: refine quantisation / sparsity (S2-a iterate) | Path B: declare NLM = engineering substrate, drop "1W consciousness" framing, archive F-NLM-1 | A first, B if 2 iterations fail |
| D4 | F-NLM-2 fails (latency too high) | Path A: smaller model (4M → 1M params), shorter context | Path B: accept batch-only (non-interactive) regime | A |
| D5 | F-NLM-3 fails (dense activation) | Path A: enforce L1 sparsity in QAT (`quantizeml` regulariser) | Path B: switch S2-a → S2-b (native SNN with explicit sparsity loss) | A |
| D6 | F-NLM-4 fails (φ parity r < 0.85) | Path A: investigate JL projection 768→16 information loss (raw#10 carryover) | Path B: declare cross-substrate parity falsified, NLM is a *different* φ-substrate (positive scientific result) | document both, no default |
| D7 | cnn2snn cannot host any attention surrogate | Path A: convolutional decoder only (BLM-style byte-CNN) | Path B: pivot to S2-b native SNN (research-tier) | A (Phase 3), B (deferred Phase 4) |
| D8 | Hardware never arrives (vendor cancels / >12 mo slip) | Path A: keep spec frozen, monitor Loihi 3 (`.roadmap.loihi3`) and NorthPole (`.roadmap.northpole`) as alt substrates | Path B: refund attempt, cancel NLM domain | A (substrate-agnostic spec already framed) |

---

## §5 Cross-LM dependencies

NLM is the most cross-cutting *LM in the family because its substrate (1W neuromorphic) is shared with multiple existing CLM/EEG/qmirror tracks.

| Dep | Direction | Mechanism | Sister doc |
|---|---|---|---|
| **CLM φ★** | NLM consumes | NLM Φ_nlm compared to CLM Φ_clm on shared 16-prompt cached set; cnn2snn quantisation initialised from CLM 350M decoder weights where layer-compatible (last-layer projection only) | `n_substrate_n3_clm_akida_phi_spec_2026_05_01.md`; CLM φ★ doc set |
| **BLM brain bridge** | NLM consumes | BLM byte-tokeniser reused as NLM input front-end (byte-stream → ADM encoder → spike raster); BLM byte-LM weights initialise S2-a CNN-decoder before cnn2snn conversion | `blm_stage12_landed_2026_05_03.ai.md`; `.roadmap.blm_brain_lm` |
| **TLM tension-modulated polarity** | NLM consumes | `mind.tension` UDP scalar (LIVE, <1 ms) modulates ADM θ_up/θ_dn polarity bias on-device, hardware-native binding-by-synchrony hook (Crick-Koch H4 variant) | `tlm_stage12_landed_2026_05_03.ai.md`; `.roadmap.tlm_tension_lm`; `strategic_clm_eeg_akida_tension_link_2026_05_02.md` §4 |
| **VLM voice** | NLM optional | VLM voice-activity envelope can drive ADM bias as auxiliary modality (Phase 3 stretch, not core) | `vlm_stage12_landed_2026_05_03.ai.md` |
| **SLM speech-EEG** | NLM optional | SLM EEG features can drive ADM polarity bias as alternate to `mind.tension` (Phase 3 stretch) | `slm_stage12_landed_2026_05_03.ai.md` |
| **qmirror substrate** | NLM consumes | qmirror cross-vendor harness frames NLM as one of N substrates under cross-vendor consistency check (alongside CLM ubu1, BLM cpu, TLM live) | `nexus_qmirror_spec_2026_05_03.md`, `qmirror_n2_cross_vendor_revision_2026_05_03.md` |
| **N-2 / N-3 / N-4 / N-5 / N-7 / N-8** | NLM provides | NLM Phase 3 S1 = literal N-2 prep landing; S3 = literal N-3; F-NLM-1 anchors N-4 Landauer 3-axis; F-NLM-2/3 anchor N-7 spike noise; cascade per `akida_d0_d1_plan_freeze` §1 | `n_substrate_consciousness_roadmap_2026_05_01.md` §11.1 |

NLM Phase 3 is therefore **the convergence point** of 6 N-axes + 4 sibling *LMs + 1 substrate harness (qmirror) + 1 hardware order. Single hardware delivery unblocks the largest cascade in the anima research portfolio.

---

## §6 Honest C3 (raw#10, 6 caveats)

1. **C3-1 Hardware delivery uncertain.** Dev-kit page is "draft" SKU on vendor shop URL; vendor has posted no shipment notice since 2026-04-29 order. ETA is **unbounded** in worst case — anima-side controllability = 0. The entire spec is hypothetical until sub-cond A clears. Mitigated only by D8 (alt substrate monitoring: Loihi 3, NorthPole).

2. **C3-2 Neuromorphic substrate vs LLM architecture mismatch.** AKD1000 does **not** natively support self-attention layers (`akida_d0_d1_plan_freeze` C3-7 carryover). S2-a uses a convolutional/recurrent surrogate, S2-b is research-tier with no published baseline at AKD1000 layer constraints. Calling this an "LM" is a reframing — it is an event-driven sequence model that consumes byte-token streams, not a transformer running on neuromorphic silicon. raw#10 honest.

3. **C3-3 AKIDA SDK maturity.** BrainChip Meta TF SDK has shipped 2 breaking `cnn2snn` API changes in the prior 6 months (per `akida_d0_d1_plan_freeze` C3-3). This spec pins no SDK version — it must be re-validated at D+0. Vendor docs are the SSOT; this spec may be stale on arrival day.

4. **C3-4 ARM64 wheel availability is single-point assumption.** F-AK-1 estimated probability 0.35 — non-trivial chance that AKD1000 cannot run on RPi5 ARM64 out of the box. Fallback is x86 host (mac M2 / ubu1), which **eliminates the 1W edge-device value proposition** that motivates NLM in the first place. If F-AK-1 fires and we fall back to x86 host, NLM becomes "AKIDA accelerator on a 200W workstation" — a different (lesser) story.

5. **C3-5 Cross-substrate parity (F-NLM-4) might be falsified for *good* scientific reasons.** A neuromorphic substrate computing a different φ from a GPU/Transformer substrate is a *positive* finding (substrates differ in their φ surface), not a bug. But the `.roadmap.akida` cond.1 SSOT defines r ≥ 0.85 as PASS, framing parity-fail as failure. The decision matrix D6 documents both interpretations; this is genuinely ambiguous.

6. **C3-6 "LM" label inflation.** NLM joins BLM/TLM/VLM/SLM as the 5th *LM, but the family resemblance is structural (`.roadmap.<name>_lm` mk2 entry, peer perspective, anima self surface), not architectural. NLM may end up being closer to "AKIDA spike inference pipeline with a tokeniser bolted on" than to a true language model in the BLM sense. raw#10: do not inflate the substrate-specific deliverable into a phenomenal-consciousness claim. Phase 3 success = the four F-NLM falsifiers measured, not "1W consciousness achieved."

---

## §7 References

- `.roadmap.akida` (hardware blocker SSOT, blk.1 = vendor wait)
- `.roadmap.nlm_neuromorphic_lm` (peer SSOT, cond.1/2/3, blk.1)
- `.roadmap.blm_brain_lm`, `.roadmap.tlm_tension_lm`, `.roadmap.vlm_voice_lm`, `.roadmap.slm_speech_eeg_lm` (sibling *LM SSOTs)
- `.roadmap.loihi3`, `.roadmap.northpole` (alt substrate watchlist, D8 path)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §2/§3/§11.1 (N-batch master)
- `docs/akida_d0_d1_plan_freeze_2026_05_02.md` (D+0/D+1 freeze, sub-cond C source-of-truth)
- `docs/akida_dev_kit_evaluation_2026-04-29.md` (vendor / price)
- `docs/akida_session_friendly_report_2026-04-29.md`
- `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md` (ADM encoder)
- `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md` (φ parity harness)
- `docs/n_substrate_n7_akida_qrng_spike_spec_2026_05_01.md` (spike noise floor)
- `docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md` (4-way binding hypothesis)
- `docs/blm_stage12_landed_2026_05_03.ai.md`, `docs/tlm_stage12_landed_2026_05_03.ai.md`, `docs/vlm_stage12_landed_2026_05_03.ai.md` (sibling *LM lands; SLM land doc per status when authored)
- `docs/nexus_qmirror_spec_2026_05_03.md`, `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`

---

## §8 Spec stats

- Sections: 8 (§0 TL;DR, §1 hardware prereq, §2 Phase 3 scope, §3 cost wall, §4 decision matrix, §5 cross-LM deps, §6 honest C3, §7 refs, §8 stats)
- Sub-conds (Phase 3 entry gates): 3 (A delivery, B devkit, C first byte-spike)
- Phase 3 streams: 4 (S1 substrate, S2 spike LM, S3 φ parity, S4 falsifiers)
- F-NLM falsifiers preregistered: 4 (energy / latency / sparsity / parity)
- Decision matrix branches: 8 (D1–D8)
- Honest C3 caveats: 6 (delivery / arch mismatch / SDK churn / ARM64 / parity ambiguity / LM label)
- Cross-LM dependencies catalogued: 7 (CLM, BLM, TLM, VLM, SLM, qmirror, N-axes 6-pack)
- Total cost wall: ~$1,700–$2,700 (one-time capex; $1,495 sunk)
- Files created by this spec: 1 (this doc only — no `.py`, no state, no commit)
