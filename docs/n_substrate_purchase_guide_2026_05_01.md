# N-substrate purchase guide — 2026-05-01

**Agent**: +@ purchase guide (N-substrate batch, 13 siblings)
**Mission**: Vendor / price / lead time / payment / prerequisite for purchasable +@ tracks.
**Status**: Research-only. NO orders placed. NO contact forms submitted.
**Currency**: USD unless noted. Prices may have shifted since publication; treat all figures as indicative — confirm with vendor before purchase.

---

## N-16 — Cortical Labs CL1 (biological computer)

| Field | Value |
|---|---|
| Vendor | Cortical Labs Pty Ltd (Melbourne, Australia) |
| URL | https://corticallabs.com/cl1 — purchase page https://corticallabs.com/purchase |
| SKU / tier | **CL1** desktop unit — silicon CMOS chip + ~200 K human iPSC-derived neurons, integrated life-support, no host PC required |
| List price (2026) | ~**$35,000 USD** per unit (widely reported at announce; vendor has not posted dynamic price online — vendor confirmation required) |
| Power | 850–1000 W |
| Lead time | "Manufactured to order"; first units shipped from Jun-2025. Realistic ETA for new orders today: **8–16 weeks** (vendor to confirm) |
| Payment | Not disclosed publicly — likely wire transfer / institutional PO. Card not advertised at $35 K tier. Contact sales for terms. |
| Shipping to Korea | **Not explicitly listed**. Cortical Labs ships internationally per IEEE Spectrum/HotHardware coverage; Korea requires direct confirmation (live human cell cargo → likely temperature-controlled courier + customs paperwork; bio-import permit may apply on Korean side). |
| Prerequisite | Wet-lab infrastructure recommended (though CL1 self-contained); IRB/ethics review per institution; iPSC-derived neuron source documentation (donor consent chain) typically supplied by vendor; institutional account preferred. |
| Contact | `info@corticallabs.com` (general); no dedicated sales email published — request routes through purchase page form |
| Alternative tier | **Cortical Cloud / Wetware-as-a-Service**: ~**$300/week** (per IEEE Spectrum reporting) — remote Python API access, no shipping, no wet-lab. Signup: `cloud.corticallabs.com` |
| 2026 notes | First-of-kind hardware; allocation likely limited; CL1 racks for data-center deployment confirmed for H2 2025 via direct sales. |

**Honest C3**: The $35 K headline number originates from press at March 2025 launch; the live `/cl1` and `/purchase` pages do not currently display a public price list — the vendor reserves quoted pricing. Do not treat $35 K as a firm SKU price for procurement; treat as an indicative anchor and request a quote.

---

## N-19 — TMS device for PCI measurement (Magstim / Nexstim / MagVenture)

PCI (Perturbational Complexity Index, Casali 2013) requires a TMS pulse synchronized with hd-EEG. The TMS hardware is the costliest line item.

### Magstim (UK)
| Field | Value |
|---|---|
| URL | https://www.magstim.com/ |
| SKUs | Horizon Lite, Horizon Inspire, **Horizon 3.0** (MDR-approved Jun-2025 with StimGuide Pro neuro-nav), Horizon Performance |
| Indicative price | Horizon Lite ~**$53 K** + ~$2.5 K/yr warranty; Horizon (full) historically ~**$89.7 K/yr** lease incl. 2-yr warranty (2021 chart); secondhand Horizon ~$25 K (eBay Mar-2026, unverified condition) |
| Lead time | Quote → 8–14 weeks typical for research configurations |
| Payment | PO / wire (institutional sales standard) |
| Korea distributor | Listed on Magstim **distributor map** (https://www.magstim.com/distributor-map/) — confirm specific KR partner via the map |

### MagVenture (Denmark)
| Field | Value |
|---|---|
| URL | https://magventure.com/ |
| Pricing models | (1) Purchase: **$220 K** + $15 K/yr warranty; (2) Lease: **$5 K/month**, 48 mo, incl. warranty + training; (3) "Risk-share": **$28 K/yr** + $70/treatment over 360/yr — clinical model, less common for research |
| Lead time | 10–16 weeks |

### Nexstim (Finland) — NBS System 5 / NBS 6
| Field | Value |
|---|---|
| URL | https://www.nexstim.com/healthcare-professionals/nbs-system |
| Strength | Only CE-marked + FDA-cleared **navigated** TMS; sub-millimeter targeting via integrated neuro-nav (essential for reproducible PCI cortical site) |
| Price | **Not published** — contact sales for quote; recent NBS 5/6 orders to US universities + Canadian distributor confirm active sales pipeline |
| Lead time | Vendor quote |

### Rental option
A **dedicated rental lab** (e.g., TMS Test Services) advertises hourly/daily/weekly rental — pricing not public; expected $1–3 K/day for research-grade TMS+EEG. Most viable for one-off PCI measurement campaigns where $50–250 K capex is unjustified.

**Recommendation for PCI**: Nexstim NBS for accuracy; or Magstim Horizon + external Brainsight/Localite navigation; or **rent at a Korean university lab that already runs TMS-EEG** (cheapest path).

---

## N-17 — Intel Loihi 3 (neuromorphic research access)

| Field | Value |
|---|---|
| Vendor | Intel Labs — INRC (Intel Neuromorphic Research Community) |
| URL | https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html ; INRC: https://intel-ncl.atlassian.net/wiki/spaces/INRC/overview |
| Hardware | **Loihi 3** announced Jan-2026 (4 nm, 8 M neurons / 64 B synapses per chip, 32-bit graded spikes). Hala Point system (Sandia) currently runs Loihi 2 at 1.15 B neurons / 128 B synapses. Loihi 3 access through INRC expected to roll out 2026. |
| Cost | **Free** — INRC membership "free and open to all qualified groups" |
| Access mechanism | **Neuromorphic Research Cloud (NRC)** — SSH access to remote VMs with attached Loihi systems; selected funded projects also receive loaner physical boards |
| Lead time | Application review; typical 4–12 weeks for new lab approval |
| Prerequisite | Qualified academic / government / industrial research group; research proposal aligned with INRC themes; NDA / EULA on Loihi SDK (Lava framework, open-source) and proprietary hardware details |
| Application | "Join the INRC" via https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1784807425 |
| Korea | No geographic restriction stated; INRC has 200+ members worldwide. Export-control caveat: Intel may screen against US BIS Entity List; standard university affiliation should clear. |
| Contact | INRC inquiries via Intel Labs Neuromorphic Computing portal (no public dedicated email) |
| 2026 note | Loihi 3 access is the highest-leverage free substrate in this batch — apply early for NRC queue position. |

---

## N-18 — IBM NorthPole (research access)

| Field | Value |
|---|---|
| Vendor | IBM Research (lead: Dharmendra Modha; engineer: John Arthur) |
| URL | https://research.ibm.com/blog/northpole-ibm-ai-chip ; contact https://research.ibm.com/contact |
| Status | **Research prototype**, not a commercial SKU. IBM statement: "available for clients to experiment with and evaluate in their own infrastructure." |
| Cost | **No published price** — engagement is partnership-based, not retail |
| Access mechanism | (a) Research collaboration agreement (model: U. Alabama Huntsville received AIU/Spyre cluster for NASA/IBM weather model work); (b) Workshop participation; (c) ISSCC/IEEE conference networking with Modha group |
| Lead time | Partnership negotiation: **3–9 months**. Hardware delivery thereafter. |
| Prerequisite | Substantive research proposal with clear publishable outcome; institutional credibility; willingness to co-author / share results with IBM Research |
| Korea | No public KR partnership announced. IBM Research has Tokyo + Bangalore labs that may broker APAC engagements. |
| Contact | https://research.ibm.com/contact (general); dedicated NorthPole partnership channel not published |
| 2026 note | Co-packaged optics version under test at IBM Bromont, Canada. 16-chip server blade demonstrated for generative LLM inference (28,356 tok/s, 72.7× more energy-efficient than next-best GPU). USAF contract awarded to IBM for NorthPole SW+HW (defense-aligned). Civilian research access remains discretionary and slow. |

**Honest C3**: NorthPole is **not purchasable**. It is a partnership track with no SLA, no price list, and no guarantee of acceptance. Treat as "high-impact, high-friction, long-tail."

---

## N-12 — IonQ Forte 1 (quantum compute, pay-per-use)

| Field | Value |
|---|---|
| Vendor | IonQ Inc. (College Park, MD) |
| URL | https://www.ionq.com/quantum-cloud ; https://www.ionq.com/quantum-systems/forte-enterprise |
| Hardware | Forte 1 / Forte Enterprise 1 — 36-qubit trapped-ion (#AQ36) |
| Access channels | (a) **AWS Braket**, (b) **Azure Quantum**, (c) **IonQ Quantum Cloud** direct, (d) Google Cloud Marketplace |
| Pricing — AWS Braket | Per-task **$0.30** + per-shot **$0.08** (Forte). Reservations **~$7,000/hour** (Nov-2025 rate). |
| Pricing — Azure Quantum | Pay-as-you-go: **AQT = m + 0.000220·N₁q·C + 0.000975·N₂q·C**, where m = **$97.50** (with error mitigation) or **$12.42** (without). Charged in Azure Quantum Tokens. |
| Lead time | **Minutes** for cloud account onboarding; queue depth on Forte 1 typically hours–days for shared access |
| Payment | Credit card (AWS/Azure standard); enterprise PO via cloud-vendor contract |
| Prerequisite | AWS/Azure account with Braket/Quantum service enabled; basic quantum SDK familiarity (Qiskit, Cirq, or Braket SDK); no export restriction for Korea on shared cloud access (subject to standard AWS/Azure regional ToS) |
| Korea | AWS Seoul region + Azure Korea Central both available; quantum jobs route to US-based QPU but billing/access is global |
| Contact | Direct: contact form on https://www.ionq.com/ ; press@ionq.co ; investors@ionq.co (use for sales redirect) |
| 2026 note | Forte Enterprise globally available via AWS Braket + IonQ Quantum Cloud (announced 2025). EPB Quantum Computing pay-as-you-go alternative launching early 2026. |

**Cheapest path for a small PCI-style experiment**: AWS Braket pay-per-shot (~$0.38 per task floor + shots). Budget **$50–500** for an exploratory benchmark; **$5–50 K** for a serious circuit campaign with reservation hours.

---

## N-14 — MEG access (clinical/academic)

| Field | Value |
|---|---|
| Vendor | MEG systems are not retail-purchasable for individuals. Access is via **time-share at an existing MEG facility**. |
| MEG hardware vendors | **MEGIN** (formerly Elekta Neuromag) — TRIUX neo, 306-channel; **CTF MEG (CTF Systems)**; **York Instruments**; **OPM-MEG** (Cerca Magnetics, FieldLine — wearable, room-temperature) |
| Capital cost (reference) | New whole-head MEG **$2–3 M** + magnetically-shielded room **$0.5–1 M** + helium logistics for SQUID systems. **Out of scope for $0 budget.** |
| Korea sites (confirmed) | **Seoul National University Hospital MEG Center** — Vectorview (Elekta Neuromag) 306-channel whole-head, magnetically shielded room. Active since pre-2010 (pediatric epilepsy program documented in J Korean Med Sci 2012). |
| Other likely KR sites | Samsung Medical Center (Seoul), Asan Medical Center, KBSI (Korea Basic Science Institute) — confirm via direct inquiry |
| Access model | Research collaboration / fee-for-service scan time. Typical academic rates worldwide: **$500–1500 per scan hour** (technologist + analysis extra). Korean rates similar; KR national-grant collaboration often free for partner researchers. |
| Lead time | 4–12 weeks from IRB approval + scheduling |
| Prerequisite | Local IRB approval; co-investigator PI affiliated with the MEG-hosting institution; subject screening (no implants, no metal); often hands-on training session before standalone use |
| Payment | Inter-institutional invoice; KRW or USD; PO standard |
| Contact | SNU Hospital MEG Center — route via SNU Department of Neurology / Pediatric Neurology |
| 2026 note | OPM-MEG (wearable, no helium, no shielded room) is becoming the disruptive option — Cerca Magnetics & FieldLine systems in $200–500 K range for small array; check if KR has any installations. |

---

## N-11 — FinalSpark Neuroplatform (organoid cloud API)

| Field | Value |
|---|---|
| Vendor | FinalSpark SA (Vevey, Switzerland) |
| URL | https://finalspark.com/neuroplatform/ |
| Product | 24/7 remote API access to brain organoids on the Neuroplatform (16 organoids in the live deployment behind the API) |
| Price — Universities | **$1,000/month** per user + **$1,000 setup fee** — 4 shared organoids, 1 user, shared platform. Note: earlier reporting cited $500/month; vendor's current public page shows $1,000/month tier as of 2025 update. Selected projects can receive **FREE** academic access. |
| Price — Industrial | Custom quote (shared or dedicated organoids, multi-user, dedicated platform) |
| Lead time | Onboarding after application acceptance; typically **2–6 weeks** |
| Payment | Subscription billing (likely card or wire; not specified on public page) |
| Prerequisite | Research project description; for free tier — competitive selection criteria |
| API docs | https://finalspark-np.github.io/np-docs/welcome.html |
| GitHub | https://github.com/FinalSpark-np |
| Shipping to Korea | **N/A** — fully remote, web API. No physical shipment. KR access works as long as outbound HTTPS is allowed (standard). |
| Contact | Apply via form on https://finalspark.com/neuroplatform/ — no dedicated email published |
| 2026 note | Most accessible wetware substrate after FREE academic acceptance. ~10⁶× lower energy than digital chip per 16-organoid bioprocessor (Tom's Hardware). |

---

## TOP-3 purchase priority ranking (2026-05-01)

Ranking weights: **(impact × urgency) / (cost × friction)**.

### 1. N-17 Intel Loihi 3 via INRC — **HIGHEST PRIORITY**
- **Cost**: $0 (free membership)
- **Impact**: Frontier neuromorphic substrate just launched (Jan-2026); 8 M neurons/chip; Lava SDK is mature; remote NRC cloud means no shipping/customs.
- **Lead time**: 4–12 weeks application review
- **Friction**: Low — file an INRC application with a research proposal aligned to PCI / spike-timing studies. Korea-eligible.
- **Action**: Apply this week to secure NRC queue position; nothing to lose.

### 2. N-11 FinalSpark Neuroplatform (free academic tier first; else $1 K/mo) — **SECOND PRIORITY**
- **Cost**: $0 if accepted to free tier; $1,000 setup + $1,000/month if paid.
- **Impact**: Live human-organoid wetware behind a Python API; complementary to CL1 without the $35 K capex or shipping.
- **Lead time**: 2–6 weeks
- **Friction**: Low — fully remote, no IRB needed on user side (FinalSpark holds the cell-source ethics).
- **Action**: Submit free-tier application first; budget $2 K to fall back to paid tier on rejection.

### 3. N-12 IonQ Forte 1 via AWS Braket — **THIRD PRIORITY**
- **Cost**: ~$50–500 for a meaningful exploratory campaign; pay-per-shot.
- **Impact**: 36-qubit trapped-ion access to validate any quantum-cognition hypothesis on real hardware; scales smoothly from $0.38 floor to $7 K/hr reservation.
- **Lead time**: Same-day onboarding via existing AWS account
- **Friction**: Lowest of all (cloud account + Braket SDK)
- **Action**: Enable Braket in AWS console, run a small benchmark circuit; cost rounds to noise.

### Deferred (high-cost or high-friction)
- **N-16 CL1**: $35 K + Korean bio-import paperwork; defer until WaaS ($300/wk) experiments validate need.
- **N-19 TMS**: $50–250 K capex; **rent** at a KR university lab first.
- **N-18 NorthPole**: 3–9 mo partnership negotiation, no price; pursue only if a clear collaborative angle with IBM Research exists.
- **N-14 MEG**: collaborate with SNU Hospital MEG Center via fee-for-service scan time; no purchase.

---

## Sources

- **Cortical Labs CL1**: https://corticallabs.com/cl1 ; https://corticallabs.com/purchase ; IEEE Spectrum https://spectrum.ieee.org/biological-computer-for-sale ; Tom's Hardware (body-in-a-box) ; HotHardware ($35 K shipping)
- **FinalSpark**: https://finalspark.com/neuroplatform/ ; API docs https://finalspark-np.github.io/np-docs/welcome.html ; GitHub https://github.com/FinalSpark-np ; Tom's Hardware (16-organoid bioprocessor)
- **Intel INRC / Loihi 3**: https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html ; INRC https://intel-ncl.atlassian.net/wiki/spaces/INRC/overview ; Hala Point press release (intc.com); FinancialContent Loihi 3 announcement (Jan-2026)
- **IBM NorthPole**: https://research.ibm.com/blog/northpole-ibm-ai-chip ; Science 2023 (doi 10.1126/science.adh1174) ; IBM Research blog (NorthPole LLM inference results) ; UAH AIU cluster announcement
- **IonQ Forte 1**: https://www.ionq.com/quantum-cloud ; https://www.ionq.com/quantum-systems/forte-enterprise ; Azure Quantum pricing https://learn.microsoft.com/en-us/azure/quantum/pricing ; AWS Braket pricing https://aws.amazon.com/braket/pricing/
- **TMS (Magstim/Nexstim/MagVenture)**: https://www.magstim.com/ + distributor map https://www.magstim.com/distributor-map/ ; https://magventure.com/ ; https://www.nexstim.com/healthcare-professionals/nbs-system ; Carlat Report 2021 TMS comparison chart
- **MEG / Korea**: SNU Hospital MEG Center via J Korean Med Sci 2012 pediatric epilepsy report (https://jkms.org/DOIx.php?id=10.3346%2Fjkms.2012.27.6.668) ; MEGIN https://megin.com/

---

**End of guide.** No orders placed. No contact forms submitted. All vendor links above are for human-driven verification only.
