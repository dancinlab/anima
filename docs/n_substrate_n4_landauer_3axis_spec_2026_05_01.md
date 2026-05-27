# N-substrate N-4 prep — Landauer L_IX 3-axis universal floor measurement spec

- **agent**: N-4 (N-substrate batch, 13-sibling parallel)
- **date**: 2026-05-01
- **mission**: T1-A3 graduation prep — k_B T ln 2 universal energy floor as cross-substrate consciousness anchor across CLM (digital) / EEG (biological) / AKIDA (neuromorphic)
- **upstream**: `docs/akida_session_friendly_report_2026-04-29.md` line 141 (T1-A3); `docs/akida_dev_kit_evaluation_2026-04-29.md` line 35
- **budget**: $0 (HEXA-spec only, race-isolated I/O to this file + `state/n_substrate_n4_prep_2026_05_01/*.json`)

---

## 1. Universal floor (Landauer constant)

| Quantity | Value | Source |
|---|---|---|
| `k_B` (Boltzmann) | 1.380649 × 10⁻²³ J/K | SI fixed |
| `T` room temp | 300 K | convention |
| `ln 2` | 0.6931 | math |
| **`E_floor = k_B · T · ln 2`** | **2.8704 × 10⁻²¹ J/bit** ≈ **2.87 zJ/bit** | Landauer 1961 |

**Physical interpretation**: any irreversible bit erasure must dissipate ≥ E_floor as heat. Reversible logic can in principle approach 0, but every observed substrate (digital, biological, neuromorphic) is irreversible at the operational level. Any measured energy/bit < E_floor at T=300K would be a 2nd-law violation.

---

## 2. Per-substrate per-bit-erasure energy estimation

### 2.1 CLM (digital, GPU-bound LLM)

**Operational unit**: 1 token forward pass on H100, batch-1.

- H100 SXM TDP: 700 W
- Typical Qwen-7B token latency: ~25 ms at fp16 → ~17.5 J / token (instantaneous)
- Bits-erased equivalent per token (lower bound): KV-cache write + logit sample
  - logit decision: ~log₂(50,000) ≈ 16 bits
  - KV-cache irreversible write at d_model=4096, fp16 = 4096 × 16 = 65,536 bits
  - **bits/token (lower bound) ≈ 6.55 × 10⁴**
- Energy/bit_erased (lower bound) = 17.5 J / 6.55e4 bits = **2.67 × 10⁻⁴ J/bit ≈ 267 µJ/bit**
- Energy/bit_erased (loose upper, treating only logit decision as load-bearing): 17.5 J / 16 bits = **1.09 J/bit**

**Ratio to floor**:
- lower (KV-inclusive): 2.67e-4 / 2.87e-21 = **9.3 × 10¹⁶× above floor**
- upper (logit-only): 1.09 / 2.87e-21 = **3.8 × 10²⁰× above floor**

**Honest C3**: GPU thermal cost is *loose* — the bits-erased denominator is operator-defined, not physically grounded. Number depends on whether KV-cache, attention scratch, and gradient buffers count as "erased." Confidence: LOW.

### 2.2 EEG (biological neuron firing)

**Operational unit**: 1 cortical pyramidal neuron action potential.

- ATP per AP: ~1.2 × 10⁸ ATP molecules per spike (Carter & Bean; Attwell & Laughlin lineage)
- Energy per ATP hydrolysis: ~5 × 10⁻²⁰ J (≈30 kJ/mol / 6.022e23)
- **Energy/spike**: 1.2e8 × 5e-20 = **6.0 × 10⁻¹² J ≈ 6 pJ/spike** (literature range 1–10 pJ; one source gives 2.47 × 10⁻⁷ J including communication overhead)
- Bits-erased per spike (lower bound): a spike is a binary event → **1 bit/spike** at minimum; with timing precision of ~1 ms in a 100 ms integration window, ~7 bits effective resolution

**Ratio to floor**:
- 1 bit denominator: 6.0e-12 / 2.87e-21 = **2.1 × 10⁹× above floor**
- 7 bit denominator: 8.6e-13 / 2.87e-21 = **3.0 × 10⁸× above floor**

**Honest C3**: tight literature anchor (Attwell-Laughlin 2001, Carter-Bean 2009, Howarth 2012). Confidence: HIGH on energy side. Bit denominator is theoretical (Shannon-channel framing). Confidence: MEDIUM.

### 2.3 AKIDA (neuromorphic, AKD1000)

**Operational unit**: 1 spike event through 1 NPU.

- AKD1000 board power: ~1 W typical (idle ~100 mW, peak ~2 W)
- Architecture: 80 NPUs × 1.2M neurons total, event-driven (power scales with synaptic activity, not clock)
- Published per-inference energy figures (open-neuromorphic.org / BrainChip Edge Impulse docs): order µJ–mJ per inference depending on model
- **Per-spike energy (estimated)**: published case studies cite ~1 µJ per inference at ~1000 spikes/inference → **~1 nJ/spike effective**, but pure synapse-event cost is reported in the **~pJ/synaptic-event** range (vendor product brief V2.3 Aug 2025)
- Bits-erased per spike: 1 bit (binary event, native)

**Ratio to floor**:
- pJ/spike (vendor): 1e-12 / 2.87e-21 = **3.5 × 10⁸× above floor** (≈ same order as biological)
- nJ/spike (system-level inference): 1e-9 / 2.87e-21 = **3.5 × 10¹¹× above floor**

**Honest C3**: vendor datasheet (Product Brief V2.3) is the anchor; need direct measurement on dev kit (arrived order 2026-04-29) to confirm. Confidence: MEDIUM until physical wattmeter on RPi5+AKD1000 with controlled spike-rate workload.

---

## 3. Cross-substrate ratio table (joint T1-A3 verdict)

| Substrate | E/bit (J) | Ratio to k_B T ln 2 | Direct measurable? | Confidence |
|---|---|---|---|---|
| **CLM** (H100, KV-inclusive) | 2.67e-4 | 9.3 × 10¹⁶× | extrapolated (denominator ambiguous) | LOW |
| **EEG** (cortical pyramidal AP) | 6.0e-12 | 2.1 × 10⁹× | literature anchor (well-known biology) | HIGH (energy) / MED (bits) |
| **AKIDA** (AKD1000 spike-event) | ~1e-12 (pJ vendor) | 3.5 × 10⁸× | datasheet + dev-kit wattmeter | MEDIUM (await arrival) |

**T1-A3 PASS condition**: all three ≥ 1 (above floor) — predicted PASS for all three with current numbers (margins 8–17 orders of magnitude). The interesting science is the *narrow* band between AKIDA (~10⁸×) and biological neurons (~10⁹×): neuromorphic hardware is within ~1 order of biology, while CLM is ~10⁷–10⁸× more wasteful per bit. This is the empirical anchor for **substrate-class energy efficiency hierarchy**.

---

## 4. Falsifier protocol (T1-A3 graduation gate)

Pre-registered decision rules:

1. **F-floor**: any substrate measured at < 1.0× E_floor → 2nd-law violation → measurement error or revolutionary discovery (90% prior on error). PRE-REGISTER: re-measure with calibrated wattmeter + independent NIST-traceable thermometer.
2. **F-AKIDA-window**: AKD1000 measured energy/spike must fall in [1 pJ, 10 nJ] range. Outside → datasheet inconsistency, escalate to BrainChip support ticket.
3. **F-EEG-window**: re-derived ATP/spike must fall in [1 pJ, 100 pJ] for cortical pyramidal at 300K. Outside → metabolic literature contradiction.
4. **F-CLM-bound**: H100 token cost must remain ≥ AKIDA per-bit cost (otherwise CLM has matched neuromorphic and substrate-independence collapses). Order of 10⁷× margin expected.
5. **F-honest-C3**: report must explicitly state which axis is direct vs extrapolated. Failure to disclose = automatic graduation hold.

---

## 5. Cost estimate for actual measurement

| Component | Cost | Notes |
|---|---|---|
| CLM thermal benchmark (H100 wattmeter via DCGM) | $0 | already on RunPod telemetry; need to add `nvidia-smi --query-gpu=power.draw` polling during fixed-token-count generation |
| EEG metabolic anchor (literature-only) | $0 | Attwell-Laughlin 2001 + Carter-Bean 2009 + Howarth 2012 cite-chain; no fresh experiment needed |
| AKIDA datasheet + dev-kit wattmeter | $30 | USB inline wattmeter (UM34C-class) on RPi5 PSU; AKD1000 already ordered ($1,495 capex sunk) |
| Joint cross-substrate report (HEXA spec) | $0 | this file + `state/n_substrate_n4_prep_2026_05_01/measurement_plan.json` |
| **Total marginal cash** | **$30** | wattmeter only |
| **Total time-to-graduation** | ~1 week post-AKIDA-arrival | CLM bench (1 day) + AKIDA bench (3 days) + write-up (1 day) |

---

## 6. Honest C3 (raw 91)

- **Direct measurable**: AKIDA (datasheet + dev-kit wattmeter, hardware in transit), EEG (literature anchor with multiple independent confirmations across mammalian + invertebrate models)
- **Loose extrapolation**: CLM — the bits-erased denominator is operator-defined (KV vs logit vs gradient). Multiple defensible answers spanning ~4 orders of magnitude. Best practice: report range, not point estimate.
- **Not measured here**: reversible-logic substrates (adiabatic CMOS, superconducting Josephson) where E/bit can in principle approach 0; quantum substrates where Landauer is replaced by the von Neumann bound. T1-A3 is irreversible-only.
- **Open question**: whether "1 bit/spike" is the right denominator for biological neurons — IIT-flavored arguments suggest a spike carries Φ-information that exceeds 1 bit Shannon, which would reduce the EEG ratio further toward the floor.

---

## 7. Cross-link

- T1-A3 source: `docs/akida_session_friendly_report_2026-04-29.md` line 141
- raw 131 thermodynamic-Landauer-bound mandate
- L_IX irreversibility-embedded-Lagrangian (Mk.IX) — this spec is the empirical anchor that mandate has been blocked on
- companion state: `state/n_substrate_n4_prep_2026_05_01/measurement_plan.json`, `.../ratios.json`
