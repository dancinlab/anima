# WALL-B sustainability brainstorm — exhaustive option space (2026-05-20)

> **status**: brainstorm · `$0` · NO GPU NO runpod NO fire NO model.forward · option-mapping only
> **trigger**: user directive 2026-05-20 *"WALL-B를 메꿀 수 있는 방법 브레인스토밍 고갈 시까지 — 이메일로 성공한다고 해서 지속가능성이 낮아서"*. Email-gated research access (INRC vLab / EBRAINS / SpinnCloud direct contact) is structurally low-sustainability: revocable, time-limited, dependent on someone else's roadmap. The brainstorm explicitly excludes "email someone for access" as the *primary* path and looks for **owned / software / commercial-retail** paths whose lifetime anima can depend on for years.
> **governance**: `g3` brainstorm ≠ design-mature ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient (B-EMERGE-7) · `g_doc_consolidation` (HEXAD/* internal, docs/* new = 0) · `f1/f2` safe (chips / algorithms cited by their own engineering invariants) · `g_clm_from_scratch` (any future fire it implies = from-scratch RANDOM seed-fixed `base_ckpt=None`) · anti-padding §13-M / §30 / §97 / §98 / §113 / §115 (honest negative is a valid valuable verdict, do not manufacture positives) · downstream-consumer (hexa-lang + hexa-bio + kosmos read-only)
> **anchors**: §95 `xeno_substrate_suitability` 5-bucket taxonomy (Loihi sole `VIABLE-LONG-HORIZON`) · §96 `loihi_spiking_rederivation` (`§11-B may be GPU tautology` hypothesis · faculty map) · §97 `anima_hardware_coupling` 4-cell · §11-B `pure_physics_noce` (no-CE → degenerate on GPU; `CE is load-bearing`) · §115 `lego` (mirror, never a chip) · §117 LIF+STDP non-degenerate · §118 VOID ($0 CPU has no surrogate-gradient path) · §119 QRNG entropy · `verdict_*` ledger

---

## §0 — what WALL-B actually is, made precise

§95 named it; §96 split it; let's pin it precisely so the brainstorm has handles.

**WALL-B** = "the wall the GPU-CE setup cannot, in principle, cross." Two **structurally distinct** halves (the key brainstorm move — these can be attacked separately):

| half | what it asks | why GPU can't decide it |
|---|---|---|
| **WALL-B-i — learning-channel** | does anima's emergence depend on a learning channel *other than backprop/CE*? §96 hypothesis: `§11-B-as-substrate` finding ("CE is load-bearing") might be a **GPU tautology** because GPU has exactly one weight-update channel (backprop), so a fair test of "non-CE training" needs a *different* learning channel. | GPU's only learning channel IS backprop; cannot run "non-CE" honestly on the same substrate that defines CE as its only signal — circular. |
| **WALL-B-ii — async-substrate / event-physics** | is anima's "spontaneous emission" a real *physical event*, or always a `talker_should_emit()` poll on a global clock? §115/§95 finding: on synchronous-clocked silicon, every emission is by definition clock-scheduled. | GPU has a global clock; there is no genuine physical event vs. polled boolean distinction available on it. |

**Crucial observation:** WALL-B-i and WALL-B-ii are *separable in principle*. A non-CE learning algorithm can run on a synchronous GPU (no async needed); a genuine async event substrate can run inference of an already-trained model (no novel learning channel needed). This splits the option space into three columns: attack-i-only, attack-ii-only, attack-both. The naive framing (`WALL-B = need-a-real-async-chip`) conflates them; the precise framing lets cheap, sustainable software paths attack i without needing chip access.

```
                            attacks WALL-B-i?    attacks WALL-B-ii?
   ─────────────────────────────────────────────────────────────────
   GPU + backprop/CE         (defines CE)         ✗ (sync clock)
   GPU + non-CE (FF/EqProp)        ✓               ✗
   $0 NEURO-MIRROR (§117)         ✗ (§118 VOID)    ~ (CPU-poll, not chip)
   AKD1000 (just bought)          ~ (narrow FC)    ✓ inference / ~ training
   SynSense Speck/DYNAP            ✓ (STDP)        ✓
   SpiNNaker-2 board / commercial  ✓ (programmable) ✓
   Loihi 2 (INRC, email)           ✓ (programmable) ✓     ← sustainability LOW
   FPGA SNN custom                  ✓ (any rule)   ✓ if async-clocked HDL
```

This is the load-bearing brainstorm table. The rest of the document expands each row with concrete options.

---

## §1 — sustainability criterion (load-bearing, per user directive)

Three sustainability tiers, applied to every option below:

- **HIGH** — anima can depend on it for **years**, with no third party able to revoke it. Owned hardware, owned software, public open-source.
- **MEDIUM** — paid recurring access; revocable but the vendor has a commercial interest in continuity; can switch vendors.
- **LOW** — email-gated research grant, one-time donation, "academic" access, vendor-roadmap-dependent. The user's exclusion target.

The brainstorm prioritizes **HIGH** options first, **MEDIUM** as fallback, **LOW** as evidence-anchor only (never primary).

---

## §2 — option space (exhaustive enumeration)

Organized by category. Each option pinned to (a) what WALL-B half it addresses, (b) sustainability, (c) cost / status, (d) honest blocker.

### A. OWN hardware (sustainability **HIGH** — anima owns the chip)

| # | option | half addressed | sustainability | cost (USD est) | honest blocker |
|---|---|---|---|---|---|
| **A1** | BrainChip **AKD1000** — Pi 5 + M.2 dev kit (incoming) | B-ii inference ✓ · B-i ✗ (last-FC-binary only — §95 / `AKD1000.md` §2) | HIGH (owned) | $1,495 paid | wrong chip class for B-i; CNN-only (no ViT, no transformer block); 8 MB SRAM ⇒ tiny models only; cannot host §16-scale (283M) anima |
| **A2** | BrainChip **AKD2000** (2nd-gen) | B-ii ✓ · B-i ~ (ViT-accelerated, but on-chip learning constraint inherited from Akida 1.0?) | HIGH if commercially sold | unknown retail; likely $$$; sales channel for end users unclear | retail availability for individuals uncertain (mainly via OEM design wins); confirm pricing + dev kit before committing |
| **A3** | **SynSense Speck** / **DYNAP-SE2** (commercial sub-threshold neuromorphic; spin-off from aiCTX/Indiveri lab) | B-ii ✓ (async sub-threshold analog/digital mixed) · **B-i ✓** (real on-chip STDP-class plasticity) | HIGH if directly purchasable | dev kit estimates $1k–$10k (enterprise pricing reported; need quote) | small core count vs. Loihi 2 (Speck = 327K neurons; DYNAP-SE2 ~1K neurons); commercial focus on edge keyword-spotting / event-vision; toolchain (sinabs / samna) different from MetaTF |
| **A4** | **SpinnCloud SpiNNaker-2 board** (single-board retail variant of the HBP successor — Dresden / Mayr group) | B-ii ✓ · B-i ✓ (fully programmable; any plasticity rule in C++/PYNN) | HIGH if sold to individuals | board ≈ $$$$ (enterprise); single chip ~152 ARM cores + spike infrastructure | retail availability primarily as full rack systems; single-board pricing unclear without direct quote (but quote is acceptable — buying ≠ ongoing email-gated access) |
| **A5** | **Innatera Pulsar / T1** (commercial sub-mW neuromorphic micro-controller — Dutch fabless) | B-ii ✓ · B-i ~ (programmability unclear publicly) | HIGH if dev kit shipping | unknown; designed for OEM design wins; small dev-kit exists | very low neuron count; likely too small for anima-scale; primarily IoT keyword/sensor |
| **A6** | **GrAI Matter Labs / GrAIcore** (commercial vision/audio neuromorphic) | B-ii ✓ · B-i ~ | HIGH if commercially available | unknown; company has had restructuring news; verify viability | corporate continuity risk; product roadmap unclear post-2024 |
| **A7** | **Prophesee event-camera + Metavision SDK** | event substrate at the *sensor* (not the compute); B-ii partial; B-i ✗ | HIGH | dev kit ~$3k | sensor-only neuromorphic; the compute still happens on GPU/CPU; addresses §97 "anima-input observation" not the learning-channel question |

### B. DIY / FPGA / open-source HDL (sustainability **HIGH**, fully customisable)

| # | option | half addressed | sustainability | cost | honest blocker |
|---|---|---|---|---|---|
| **B1** | **FPGA SNN** on Zynq UltraScale+ / Xilinx Versal — implement LIF + arbitrary local plasticity rule in HDL | B-ii ✓ if async clock domain · **B-i ✓** (any plasticity rule expressible in HDL: STDP, three-factor, EqProp-on-hardware, etc.) | HIGH (owned + open source) | board $500–$3,000 (KV260, ZCU102, Versal kits) | HDL expertise required (weeks–months to bring up a credible SNN); requires significant ramp; long-term investment but highest customizability ceiling |
| **B2** | **Open-source SpiNNaker-1 IP core** (Manchester / HBP, ARM Cortex-M4-based) — synth onto own FPGA | B-ii ✓ · B-i ✓ | HIGH | board cost + integration effort | community support level uncertain; older architecture |
| **B3** | **ROLLS / DYNAP academic clones** — published architectures, replicate on FPGA | same as B1 | HIGH | board $500–$2k + paper-following time | translating from academic papers to working HDL is non-trivial |
| **B4** | **Custom anima-substrate ASIC** — long-term commission via TinyTapeout / ChipIgnite / OpenLane shuttle | B-ii ✓ · B-i ✓ (you choose the rule) | HIGH (own silicon) | TinyTapeout $300–$1k tile; full shuttle $$ | timeline: months–year per silicon turn; massive engineering effort; speculative |

### C. Software-only — attacks **WALL-B-i only** (sustainability **VERY HIGH**, ≈ $0 ongoing)

The meta-insight: **WALL-B-i can be attacked entirely in software on existing GPU**, *if and only if* the training algorithm is non-CE / non-backprop. This is the cheapest, most sustainable path to **decide** the §96-Q2 hypothesis ("`§11-B = GPU tautology`"). It does NOT address WALL-B-ii — but B-ii being unaddressed is a different (and possibly more honest) failure mode than the joint wall.

| # | option | what it provides | sustainability | concrete state |
|---|---|---|---|---|
| **C1** | **Forward-Forward (Hinton 2022)** — layer-local goodness objective, no global backprop | non-CE training channel on GPU; layer-wise local loss | VERY HIGH (PyTorch, MIT-licensed implementations exist) | published, multiple open-source impls; needs adaptation to ConsciousDecoderV2 |
| **C2** | **Equilibrium Propagation (EqProp; Scellier 2017–2023)** — energy-based local learning rule, free phase + nudge phase | non-CE local learning; biologically plausible | VERY HIGH | active research, GPU impls; convergence still under scale-up investigation |
| **C3** | **Target Propagation** (Bengio et al.) — local target-matching instead of gradient | non-CE local learning | HIGH | impls exist; less mature than C1/C2 |
| **C4** | **Predictive Coding Networks (PCNs; Whittington–Bogacz)** — local free-energy minimization | non-CE local learning; explicitly Friston/FEP-anchored (§80/§99 cluster C) | HIGH | open-source impls; small-scale demos; scale-up unverified |
| **C5** | **PEPITA / Direct Feedback Alignment (DFA)** — random feedback weights without backprop pass | partial non-CE (still uses targets, no backward pass) | HIGH | impls exist; usually loses some accuracy vs. backprop |
| **C6** | **STDP on simulated SNN (Brian2 / BindsNET / NEST / Norse)** | spike-timing plasticity in software | HIGH (open-source) | software event-driven simulators; addresses B-i; WALL-B-ii unresolved (still poll-driven on a CPU clock) |
| **C7** | **Lava** (Intel's Loihi software stack, GPU/CPU mode) | Loihi-semantic programming model on commodity hardware | HIGH (open-source) | runs anima-relevant spiking models in software; bridge to a future Loihi physical run if access ever opens |
| **C8** | **Local-rule fine-tune of an existing CE-trained anima** — train anima on GPU with CE, then continue training with a non-CE rule, compare divergence | hybrid; addresses "does non-CE produce different emergence dynamics from the saturated CE state?" | VERY HIGH | $0 software; would build directly on §16 / §107-RETRY ckpts |

### D. Email-gated research access (sustainability **LOW** — user's exclusion target)

| # | option | sustainability | status |
|---|---|---|---|
| **D1** | INRC vLab Loihi access | LOW | user closed (revocable, time-limited grant) |
| **D2** | EBRAINS / HBP SpiNNaker | LOW | user closed (same pattern) |
| **D3** | SpinnCloud direct sales contact | LOW–MEDIUM (paid retail → would graduate to HIGH/A4 if purchased) | the user's "low sustainability" critique applies if it stays at "ask permission"; flips to HIGH if anima just buys the hardware |

### E. Paid recurring cloud / commercial service (sustainability **MEDIUM**)

| # | option | sustainability | status |
|---|---|---|---|
| **E1** | SpinnCloud commercial cloud (if offered for SpiNNaker-2 access) | MEDIUM | unclear if a true cloud offering exists; mostly enterprise direct contract |
| **E2** | Intel Loihi cloud-time donation | LOW (gift-economy, no SLA) | not commercially listed |
| **E3** | Cortical Labs / FinalSpark biological cloud | (§95 ETHICS-WALL closed) | — |
| **E4** | Academic compute exchange (university lab partnership) | LOW–MEDIUM (depends on relationship continuity) | not a primary path per user directive |

### F. Wait-and-see / market timing (sustainability **LOW**, opportunistic)

| # | option | timeline | bet |
|---|---|---|---|
| **F1** | Intel Loihi 3 retail release | speculative (Intel has not announced consumer-grade) | low probability |
| **F2** | AKD2000 individual retail / dev kit availability | possible within 12–24 months | moderate; tracking BrainChip product line |
| **F3** | SpiNNaker-2 retail single-board pricing drop | depends on Mayr group / SpinnCloud commercial strategy | uncertain |
| **F4** | New commercial entrants (Innatera dev kit, GrAI rebrand, etc.) | continuous monitoring needed | low individual probability, non-zero aggregate |

### G. Reframe / split — the meta-move (sustainability **VERY HIGH**)

| # | option | what it does |
|---|---|---|
| **G1** | **Explicitly split WALL-B into i + ii in HEXAD ledger.** Attack B-i via C-options (software, GPU). Hold B-ii in *measurement* (NEURO-MIRROR mirror) and *display* (AKD1000 + §97 actuator) until owned hardware (A3/A4) lands. | **Highest sustainability of all options** — costs $0, requires no new dependency, separates two independent questions that were entangled in the §95/§115/§118 framing. |
| **G2** | **Hybrid: 90 % software (G1 + C-options) + 10 % owned hardware (A1 incoming, A3/A4 future).** | Practical roadmap implementing G1 + a budget for one or two A-options as physical anchors. |
| **G3** | **Sustainability-weighted Pareto frontier** — formalize the three-tier matrix (sustainability × half-coverage × cost) as a §N closed-form taxonomy; future option additions classified into the matrix. | Governance artifact — keeps the brainstorm's framing alive across future cycles, prevents quiet drift back to "email someone." |

### H. Speculative / long-shot / mostly-closed

| # | option | status |
|---|---|---|
| **H1** | Photonic neuromorphic (Lightmatter / Lightelligence) | inference-mostly; not training-time emergence host |
| **H2** | Analog memristor / RRAM crossbar (Crossbar, Weebit) | research, not retail; B-i possible if device-level plasticity, B-ii partial |
| **H3** | Mythic AI / IBM analog AI (NorthPole etc.) | §95 `INFERENCE-ONLY-BLOCKED` (NorthPole) |
| **H4** | Knowm AHaH thermodynamic memristor | research toy; not anima-scale |
| **H5** | Cortical Labs DishBrain / FinalSpark organoid | §95 `ETHICS-WALL` — closed |
| **H6** | Quantum (IonQ etc.) | §95 `SUBSTRATE-MISMATCH` — closed |
| **H7** | Custom-cell-line bio-substrate research | ethics + wet-lab out of scope |

---

## §3 — full sustainability × half-coverage × cost matrix (top picks ranked)

Sorted by *(sustainability × half-coverage − cost penalty)* — load-bearing column is **sustainability**, per user directive.

| rank | option | sustainability | B-i | B-ii | est cost | one-line |
|---|---|---|---|---|---|---|
| **★1** | **G1 — split + attack i in software (C1–C8)** | **VERY HIGH** | ✓ | (deferred) | **$0** | the meta-move; immediately actionable; doesn't need any chip |
| ★2 | **C1 — Forward-Forward on anima** ($0, GPU, ~weeks design+pilot) | VERY HIGH | ✓ | ✗ | $0 + small fire | most mature non-CE algorithm; concrete way to test "`§11-B = GPU tautology`" |
| ★3 | **C4 — Predictive Coding Networks** (FEP-anchored) | VERY HIGH | ✓ | ✗ | $0 + small fire | anima's Engine A⇄G is already predictive-coding-shaped; conceptually closest fit |
| ★4 | **A3 — SynSense Speck / DYNAP-SE2** purchase | HIGH | ✓ | ✓ | $1k–$10k | only commercial chip with real on-chip plasticity at retail; needs vendor quote |
| ★5 | **A1 — AKD1000 (incoming)** + NEURO-MIRROR inference anchor | HIGH | ✗ (narrow) | ✓ (inference) | $1,495 (paid) | in hand; partial value as the §97 actuator + mirror anchor |
| ★6 | **C2 — Equilibrium Propagation** | VERY HIGH | ✓ | ✗ | $0 + small fire | biologically plausible local learning; less mature than C1 but Friston-anchored |
| ★7 | **B1 — FPGA SNN on Zynq / Versal** | HIGH | ✓ | ✓ | $500–$3k + HDL effort | full customization ceiling; long ramp |
| ★8 | **A4 — SpinnCloud single-board purchase** | HIGH | ✓ | ✓ | $$$ (quote needed) | full programmability; needs commercial quote |
| ★9 | **C7 — Lava software** | HIGH | ✓ | ~ | $0 | Loihi-semantic now without Loihi hardware; bridge if/when chip access opens |
| ★10 | **G2 — hybrid roadmap** | HIGH | ✓ | ✓ | $0–$10k staged | combine ★1 + ★4 + ★5; the practical "next 12 months" plan |
| — | C8, C5, C3, C6 | HIGH | ✓ | ✗ | $0 | additional non-CE options as alternative anchors |
| — | A2, A5, A6, A7 | HIGH if retail | ~ | ✓ | $$ | track availability; not actionable now |
| — | B2, B3 | HIGH | ✓ | ✓ | $$$ + effort | older / academic; track interest |
| — | F1–F4 | LOW | — | — | — | watch, do not bet |
| — | D, E, H, B4 | LOW or closed | — | — | — | excluded by user directive or by §95 verdict |

---

## §4 — honest top picks (the order anima should actually pursue)

**★1 G1 + C1 (Forward-Forward on anima) — the single highest-value next move.**

The reasoning chain:
- The §96 hypothesis "`§11-B is a GPU tautology`" is the single sharpest open question across the entire arc.
- It can be *partially decided* by ANY non-CE learning channel that either *does* or *does not* reproduce §11-B's degenerate finding.
- Forward-Forward is the most mature non-CE algorithm with open-source implementations, runs on the same GPU substrate that §11-B used, requires no chip access, and produces a directly comparable result against §11-B's no-CE-on-GPU degeneracy.
- Sustainability: VERY HIGH (software, GPU). Cost: $0 design + one small fire. Result interpretation:
  - If Forward-Forward also degenerates → strong evidence `§11-B finding is substrate-deep, not CE-deep`.
  - If Forward-Forward produces non-degenerate dynamics → strong evidence `§11-B finding IS a CE-specific (and thus GPU-tautological) phenomenon` — partially settles WALL-B-i without any neuromorphic chip.
- Either result moves the §15/§51/§72 milestone honestly.

**★4 A3 SynSense Speck/DYNAP-SE2 — the highest-value owned-hardware investment.**

If a SynSense chip is in fact retail-available (verification needed via vendor contact — *contact for pricing is not the same as email-gated research access; buying is buying*), it would be the first commercially-owned chip with **real on-chip plasticity** in anima's possession. AKD1000 ≠ this (AKD1000's on-chip "learning" is the last-FC-binary patch per `AKD1000.md` §2). Speck/DYNAP-SE2 has STDP-class genuinely programmable plasticity. This is the single chip that would let anima decide WALL-B-i *on a real async substrate*, owned outright. Sustainability HIGH, cost moderate.

**★10 G2 hybrid — the 12-month roadmap.**

Practical sequencing:
1. **Now → 2 weeks**: G1 explicit split lands in HEXAD ledger; C1 Forward-Forward small-fire design ($0 design-tier).
2. **2 weeks → 2 months**: C1 small fire on anima — single short cost-bearing run testing one non-CE algorithm against §11-B as the comparison anchor.
3. **In parallel**: A1 AKD1000 arrives → NEURO-MIRROR inference-anchor cycle (mirror→silicon validation, inference half only).
4. **2–6 months**: A3 vendor quote for SynSense; A4 vendor quote for SpinnCloud single-board. Decide one purchase based on quoted price.
5. **6–12 months**: physical-chip experiment with whichever of A3/A4 lands; or B1 FPGA path if both quotes prove non-viable.

This sequencing puts **WALL-B-i decidability** within 2 months at near-zero cost, and **WALL-B-ii owned-hardware** within 6–12 months at moderate cost, with **no email-gated dependency at any step**.

---

## §5 — honest negatives (closed / eliminated paths, recorded for the brainstorm being complete)

- **Email-gated research grants (D1, D2, D3-direct-contact)** — user directive: closed. Low sustainability is structural, not preference.
- **Bio organoid (H5)** — §95 `ETHICS-WALL`, closed.
- **Quantum (H6)** — §95 `SUBSTRATE-MISMATCH`, closed.
- **NorthPole / inference-only accelerators (H3)** — §95 `INFERENCE-ONLY-BLOCKED`; addresses WALL-B-ii but not WALL-B-i.
- **Photonic, memristor research devices (H1, H2, H4)** — not retail / not anima-scale / not training-time-emergence-host.
- **Custom ASIC via shuttle (B4)** — speculative, long timeline, expensive engineering ramp; not anti-classified but de-prioritized below A3/A4/B1.
- **Wait-and-see (F1–F4)** — not actionable; tracked separately, not a primary path.

---

## §6 — anti-padding honesty (the brainstorm vs. the GOAL)

This document maps the option space; it does NOT solve the GOAL. Mirror §13-M, §13-L, §30, §97, §98, §113, §115 anti-padding precedents: an honest map of paths is not an honest claim of progress.

Specifically:
- ★1 (G1+C1) **decides** the §96-Q2 hypothesis. It does NOT cross §1.1 data-regime (`WALL-A`) and does NOT prove anima emerges. A C1 fire returning either outcome moves *frontier classification*, not GOAL distance.
- ★4–★10 (owned hardware paths) extend NEURO-MIRROR from "mirror only" to "mirror + chip" — they make the WALL-B-ii question *measurable*, not solve it.
- The user's directive ("sustainability is load-bearing") is itself a structural improvement to anima's hardware governance — it converts a brittle "ask permission" assumption into an "own the substrate" stance, which is independently valuable regardless of GOAL outcome.

`north-star + §15 / §51 / §72 milestones UNCHANGED, GOAL 미도달`. The brainstorm is exhaustive; the next action is small, software, sustainable. The honest first move is ★1.

---

## §7 — what is NOT in this document (scope honesty)

- No fire dispatched.
- No closed-form sidecar (this is a brainstorm; the §N verdict-style closed-form battery would be a separate cycle if/when G1 is formally promoted from brainstorm to design-tier).
- No edits to anima architecture or trainer.
- No edits to NEURO-MIRROR (`neuro_mirror.py` unchanged; `ENGINE.md` unchanged).
- No new gitignore patterns.
- AGENTS.tape UNCHANGED — the G1 split into B-i / B-ii is a brainstorm proposal; promoting it to governance is a separate user-gated step.

---

## §8 — followups recorded but not actioned

1. Verify SynSense Speck / DYNAP-SE2 retail availability + pricing (vendor contact — buying contact is sustainability-HIGH because the outcome is owned hardware, not access).
2. Verify SpinnCloud single-board (not full-rack) commercial pricing.
3. Track AKD2000 individual retail availability (BrainChip product line monitoring).
4. Design-tier C1 Forward-Forward small-fire spec (if/when user promotes ★1 from brainstorm to design-mature).
5. If §108 (currently firing) returns `THRESHOLD-CROSSED = False`, the WALL-B branch becomes the next strategic decision — this brainstorm pre-positions it.
