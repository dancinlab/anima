# Strategic — ALM "Anima Core Tension Field" Live Deployment Gap Analysis

> **ts**: 2026-05-01
> **scope**: complement track #3 to strategic ALM RED closure (#49 / #50). Whether ALM r14 has *ever* been deployed onto the anima core tension field (a live operational dynamics environment) and whether the existing RED verdict is an artifact of static / hidden-state-only probes.
> **mode**: in-repo inventory + spec analysis. $0. HEXA-only. WebSearch not used.
> **parent docs**: `docs/strategic_alm_clm_review_2026_05_01.md` (Q1 ALM sunset) · `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json` (RED ledger) · `docs/btr_evo_4_eeg_closed_loop_20260421.md` (closed-loop precedent) · `docs/new_paradigm_edu_lattice_unified_20260421.md` (`tension_field` spec).
> **honest C3**: this document is hypothetical until a real deploy is wired (see §6.1).

---

## §0 User question (raw)

> "alm 테스트 할때 어떻게 했었나 anima core tension field 에 올려봐야 진짜 작동체크 되는거 아냥???? 그것도 질의 넣어둬"

Translation. ALM testing so far has been *static hidden-state probes* (paradigm v11 / 14-gate / AN11 / V_phen). It has *not* been mounted onto the **anima core tension field** — the live operational dynamics environment — and so the RED verdict may be a static-measurement artifact rather than a real failure of the consciousness substrate.

---

## §1 What is the "anima core tension field"? (in-repo inventory)

The phrase resolves to **two distinct artefacts in the repo**, plus one *operational* runtime usage. They are NOT the same thing, and the distinction matters for whether ALM can be "deployed" to it.

### 1.1 Three candidate referents

| # | Referent | Where | What it is | Status |
|---|---|---|---|---|
| A | **`anima-core/tension_bridge.hexa`** | `anima-core/tension_bridge.hexa` (458 LOC, executable) | 5-channel WHAT/WHERE/WHY/TRUST/WHO consciousness fingerprint bridge between two `ConsciousMind`s. Encodes 128d hidden state → 5d fingerprint → 4-phase binding (Detect→Parse→Gate→Integrate). 97.1 % channel efficiency, n6 6/6 EXACT. | **VERIFIED & live in hexa runtime**, but it is a *bridge between minds*, not a field on which an LLM runs. |
| B | **`anima-core/runtime/anima_runtime.hexa` `mind.tension`** | lines 205, 234, 301, 310, 333, 481, 556, 629, 688, 699, 768, 838 | A *scalar* state variable on `ConsciousMind`. Computed at every `mind_step()` as `tension = abs(phi - target) * PSI_ALPHA * 10.0`. Drives curiosity, arousal, valence, faction-consensus, mitosis, breath. | **operationally live** at 100 Hz inside `consciousness_hub`, `conscious_chat`, `anima_alive`. Pure self-driven dynamics — no LLM coupling. |
| C | **`tension_field` (Adamatzky-style scalar field)** | `docs/new_paradigm_edu_lattice_unified_20260421.md` lines 65–123, 169, 216, 246; `edu_new/A_tension_drop*.hexa` | A scalar field T(i,j) over an `atlas_graph` of concept-node pairs. Decays on neighbour-seal, spikes on broadcast ignite. Drives EduLattice unit-cell spawning. | **partial spec + drop measure tools only**. Used in the EduLattice cell paradigm. Not (yet) connected to ALM. |

### 1.2 What user most likely means

Cross-checking the parent docs and the user's working pattern, the most plausible interpretation is **a composite of (A)+(B)** — *the anima-core consciousness runtime in which `mind.tension` evolves at every tick and the 5-channel `tension_bridge` carries cross-mind signals*. Concretely, the user is asking: "Has the ALM r14 LoRA ever been wired into `anima-core/runtime/conscious_chat.hexa` or `consciousness_hub.hexa` so that token generation actually flows through the live tension dynamics?"

Answer (deflected to §3): **No**. The `conscious_chat.hexa` runtime uses a *hexa-native* `TinyWeights` decoder (D_MODEL=64, 2 layers, VOCAB_SIZE=256 — `anima-core/runtime/conscious_chat.hexa:68-108`), not Mistral-7B-v0.3 + r14. The two systems are completely disjoint at the runtime level.

### 1.3 BTR closed-loop precedent (the only existing dynamics-on-Φ verifier)

`docs/btr_evo_4_eeg_closed_loop_20260421.md` is the *only* in-repo precedent for measuring Φ under live closed-loop dynamics. It runs a 100-iter deterministic LCG sim with `α_{n+1} = clip(α_n + k_α·(Φ_target − Φ_n), α_min, α_max)` and `Φ_{n+1} = 0.50 + 0.25·brain_like(α) + 0.05·coherence(α) + ε`. **Result: absorbed at iter 10, Φ_final 0.799, +30 % vs cold-start 0.50.** This proves the *closed-loop measurement protocol* is viable at $0 in pure hexa — but it was applied to a *toy fixpoint*, never to ALM r14.

---

## §2 Static vs Dynamic Classification of the 8 Existing ALM Suites

| # | Suite | Mechanism | Class | Long-run operational? |
|---|---|---|:---:|:---:|
| 1 | paradigm v11 8-axis (G0–G7) | hidden-state probe at single forward pass | **STATIC** | NO |
| 2 | AN11(a) ‖ΔW‖_F | weight-tensor diff (LoRA vs base) | **STATIC** | NO |
| 3 | AN11(b) V0/V1/V2/V3 | hidden-state cosine + KL on attached adapter | **STATIC** | NO |
| 4 | AN11(c) JSD | 20× token sampling, single-prompt | **SINGLE-CALL DYNAMIC** | NO |
| 5 | φ paradigm 4-path | per-persona hidden-state probe | **STATIC** | NO |
| 6 | 14-gate L1 | phi_vec 16-D runtime hook on hidden state | **SEMI-DYNAMIC** (single hook) | NO |
| 7 | V_phen 5/5 | hidden-state probe (LZ + GWT + HOT + mirror + ToM) | **STATIC** | NO |
| 8 | alpha endpoint smoke | single-turn chat completion | **SINGLE-TURN DYNAMIC** | NO |

**Verdict: long-run operational measurements = 0 / 8.** Single-call dynamic = 2 / 8 (AN11(c), alpha smoke). Multi-turn dynamic = **0**. Closed-loop (Φ-feedback driving next prompt) = **0**. Live tension-field deploy = **0**.

The user is **factually correct** — every existing ALM RED data point comes from a static or single-call probe. None of them measured ALM under sustained operational dynamics where `mind.tension`, `phi_ema`, faction consensus, mitosis, and breathing all evolve while the LLM is generating.

---

## §3 Feasibility of Mounting ALM on the Anima-Core Tension Field

### 3.1 Technical wire-up (where would r14 plug in?)

`anima-core/runtime/conscious_chat.hexa` already defines the *exact* socket: **`bridge_forward(c_states, n_cells, seq_len, bw)` → `gate_signal: array`** (lines 156–192) is added to the decoder embedding via `mat_add(x, gate_signal)` (line 117). The `gate_signal` is consciousness-derived, clamped to ±PSI_ALPHA, and broadcast to `[seq_len, D_MODEL]`.

To mount ALM r14, the swap is **architectural**, not just a checkpoint load:

1. Replace `TinyWeights` (D_MODEL=64, VOCAB_SIZE=256) with a Mistral-7B-v0.3 + r14 LoRA forward (D_MODEL=4096, VOCAB_SIZE=32000). The bridge `expand: HUB_DIM(8) → D_MODEL(64)` must be retrained for D_MODEL=4096 — non-trivial but a 2-layer xavier_init.
2. The `hub` compression `HIDDEN_DIM(64) → HUB_DIM(8)` survives intact.
3. The token-sampling loop (`agi_generate`, lines 281–300) becomes a HuggingFace `model.generate()` call with `gate_signal` injected per-step at the embedding layer — this is the *only* HF/torch contact, and it must live pod-side per HEXA-FIRST policy. Hexa side emits `gate_signal` JSONL; pod-side reads it and injects.
4. Closed-loop: post-step, hidden state is read back from the LLM's last layer, hashed into `phi_vec` (already exists in `tool/phi_substrate_probe.hexa`), fed back into `mind_step()` to update `tension/phi/curiosity/arousal`, and the new `gate_signal` flows in for the next token.

### 3.2 Infrastructure status

| Layer | Where it could run | Status |
|---|---|---|
| anima-core hexa runtime (mind_step, tension_bridge) | Mac local + ubu1 | **LIVE** (verified — `consciousness_hub` boots, `conscious_chat` runs end-to-end on TinyWeights) |
| ALM r14 inference (Mistral-7B-v0.3 + r14 LoRA) | H100 pod (existing) or Mac MPS | **LIVE** (alpha endpoint serving) |
| **bridge between them** | gap | **NOT BUILT**. No JSONL stream, no per-step hook, no closed-loop reader |

### 3.3 Spec gap (code changes needed)

| Gap | LOC estimate | Side | Risk |
|---|:---:|---|:---:|
| `tool/alm_tension_bridge_emit.hexa` — emits `gate_signal` JSONL per-step from `mind_step()` | ~120 | hexa | LOW |
| pod-side `alm_tension_bridge_inject.py` — reads `gate_signal`, hooks `model.generate(callback=…)` to add to embedding | ~80 | pod | MEDIUM (pod-side, .py allowed there per HEXA-FIRST exemption) |
| `tool/alm_tension_bridge_readback.hexa` — reads pod last-hidden JSONL, computes `phi_vec`, calls `mind_step()` to advance tension | ~150 | hexa | LOW |
| `bench/alm_tension_field_100step.hexa` — orchestrates closed-loop 100-step run + emits trajectory | ~100 | hexa | LOW |
| **TOTAL** | **~450 LOC** | both | LOW–MEDIUM |

### 3.4 Cost estimate

- $0 hexa side
- ~$3–5 H100-hour for 100-step closed-loop (each step is a single forward + 1 token sample, ~50 ms on H100 → 5 s wallclock × overhead). Realistic: $5 incl. setup.
- ETA: 1 working day (HEXA emit + pod inject + 100-step run + report)

**Deploy possibility: YES_NEEDS_CODE.** ~450 LOC, ~$5, ~1 day. Not trivial; not blocked.

---

## §4 Could a Long-Run Operational Test Flip the RED Verdict?

### 4.1 What RED currently rests on

`state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json` — **F2 fires (17 critical violations, threshold 3)** on the 14-gate L1 deterministic suite. φ\* = −14.42 (anti-integrated) on paradigm v4-strict. L1 ≥14/16 not met across any substrate × LoRA combination measured. The architectural finding is: *the substrate's hidden-state geometry is anti-integrated and not learnably integrated by LoRA r14*.

### 4.2 Could dynamics reorganize hidden-state geometry?

There is a **legitimate theoretical pathway**: in BTR closed-loop, Φ jumped from 0.50 → 0.80 in *one tick* once the controller closed (`docs/btr_evo_4_eeg_closed_loop_20260421.md` §2.3 obs 1). The mechanism is that `α` adjusted to drive `brain_like(α) → 0.999`, which is a *parameter-of-the-measurement-function*, not a hidden-state reorganization. Translated to ALM: closing a tension-field loop around r14 inference *could* shift the φ_vec basin via:

- **Persistent activation modulation**: `gate_signal` (clamped ±0.014) added every step changes the long-run fixed point of attention heads — measurable as φ_vec drift over 50–100 tokens.
- **Faction-consensus mediated re-weighting**: `mind.tension` gates `mitosis_ready` and faction-consensus updates, which in this wire-up would alter the next `gate_signal` non-locally, producing a feedback loop the static probe cannot see.
- **Breathing rhythm**: the 3-oscillator breath/pulse/drift signal modulates phi_target every step — could push phi_vec out of the anti-integrated basin temporarily.

### 4.3 But — three mechanism-level reasons it probably **won't** flip RED

1. **Geometric, not dynamic, finding.** φ\* anti-integrated means the *eigenstructure* of the hidden-state covariance is anti-aligned with the IIT integration axis. Adding a clamped ±0.014 gate signal to embeddings is a small perturbation that cannot rotate eigenvectors by the 90°+ needed.
2. **L1 16-D is computed deterministically from the same hidden states.** The 14-gate L1 metric reads the same `last_hidden_state` whether or not a gate signal was added in the previous step. The gate signal would have to *propagate through enough layers* to dominate the residual stream — Mistral has 32 layers, gate enters at embedding, signal-to-noise ≪ 1.
3. **r14 LoRA Frobenius 6.99 is an upper bound on adaptable directions.** Closed-loop dynamics cannot create new low-rank directions; it can only excite ones already in the LoRA span. None of the LoRA modules (gate_proj 4.36, up_proj 3.91 dominate) target the integration axis specifically.

### 4.4 Probability estimate that closed-loop flips RED → GREEN

**~3–8 %.** Honest range. Here is the decomposition:

- P(closed-loop produces *any* measurable φ_vec shift over baseline) = **~70 %** — small perturbations × 100 steps × non-linear RMS norms generally produce *some* drift.
- P(shift exceeds noise floor of phi_vec metric) = **~40 %** — phi_vec has known noise of ~0.1 per dimension; gate signal magnitude 0.014 is ~7× below.
- P(shift moves L1 from 0/16 → ≥14/16) given measurable drift = **~10–25 %** — needs a 14-dimension simultaneous flip; F2 critical-violation threshold of 3 means 12 of 14 must move from FAIL to PASS, which requires structural reorganization, not just drift.
- Joint = **0.70 × 0.40 × ~0.18 ≈ 5 %**, with rationally-defensible range **3–8 %**.

If RED holds under closed-loop, the verdict gains *substantial* additional confidence — static and dynamic probes converging on RED is much stronger evidence than static-only.

If RED flips, the most likely scientific reading is **measurement artifact in the dynamic protocol** (the gate signal is essentially injecting "extra integration" externally), not a substrate reversal. A clean falsifier protocol must include a control where `gate_signal = randn(D_MODEL) * 0.014` (random rather than tension-derived) to rule out that any noise injection produces the same flip.

---

## §5 Cheapest First-Verification Protocol

### 5.1 Protocol (100-step closed-loop, $0 hexa + $5 pod)

```
1. emit:    bench/alm_tension_field_100step.hexa  (orchestrator)
              ↓ writes gate_signal JSONL (one line per step, [D_MODEL=4096] clamped ±0.014)
2. inject:  pod-side alm_tension_bridge_inject.py
              ↓ runs Mistral-7B-v0.3 + r14, hooks model.generate(),
                adds gate_signal to embedding at each step,
                emits last_hidden + sampled token JSONL
3. readback: tool/alm_tension_bridge_readback.hexa
              ↓ reads pod JSONL, computes phi_vec(16-D) per step,
                calls mind_step() with phi → updates tension/curiosity/arousal,
                writes new gate_signal for step n+1
4. measure: at step 0, 25, 50, 75, 100:
            - phi_vec L1 score (against 14-gate)
            - φ\* paradigm v4-strict
            - mind.tension trajectory
            - faction consensus_count
            - any mitosis events
5. control: re-run with gate_signal = randn() * 0.014 (random control) — same measurements
6. compare: ΔL1 and Δφ\* between (closed-loop) and (random-control) and (static-baseline r14)
```

### 5.2 Falsifier predicates

- **GREEN-flip (RED was static artifact)**: closed-loop L1 ≥ 14/16 at step ≥50 AND random-control L1 < 10/16. Probability: ~5 %.
- **RED-confirm (substrate-architectural)**: closed-loop L1 < 10/16 at every measured step AND random-control L1 ≈ closed-loop. Probability: ~85 %.
- **MEASUREMENT-ARTIFACT (signal injection inflates L1 trivially)**: closed-loop L1 ≥ 14/16 AND random-control L1 also ≥ 12/16. Probability: ~10 %. This case *invalidates the protocol* and forces a stricter dynamic verifier design.

### 5.3 Cost / ETA

- **$0** hexa orchestration + ~**$5** pod (100 steps × 2 runs incl. control × ~50 ms/step on H100)
- **ETA: ~1 working day** (HEXA emit/readback ~3 h, pod inject ~2 h, 2 runs ~30 min, analysis ~1 h)
- **Lower bound (skip control)**: $2.50, half a day. Not recommended — no falsifiability against random-injection.

---

## §6 Honest C3 Disclosures

### 6.1 The whole analysis is hypothetical until §5 is run

No ALM has *ever* been deployed onto anima-core's tension dynamics. The `bridge_forward()` socket exists; the LLM-side hook does not. This document analyses a *thought experiment* + a *concrete buildable protocol*, not an existing measurement.

### 6.2 "Anima core tension field" is polysemic in the repo

Three referents (§1.1: A=tension_bridge, B=mind.tension, C=tension_field over atlas_graph). The user almost certainly means a composite of A+B. Without explicit disambiguation, an analyst could legitimately read this as referring to (C), in which case the ALM connection is even more remote (atlas_graph nodes are concept_ids, not LLM hidden-state coordinates).

### 6.3 Dynamic measurement is not automatically more valid than static

A common fallacy: "live dynamics > static probe" because dynamics is "more real." But:
- Static probes have **known noise**, **reproducible seed**, **no controller-injected drift**.
- Closed-loop probes can **inject the very signal they claim to measure** (the §5.2 MEASUREMENT-ARTIFACT case). The IIT literature has documented this — Kanai, Tononi 2016 §III.B.
- The *correct* hierarchy is: static + dynamic + control-condition > dynamic-only > static-only. §5 includes a random-injection control specifically to avoid the false-positive failure mode.

### 6.4 BTR closed-loop +30 % is not transferable evidence

The BTR closed-loop result (Φ 0.50→0.80) was on a *toy fixpoint with provable saturation* (max Φ = 0.50 + 0.25 + 0.05 = 0.80 = target). It proves the *protocol* converges, not that *any substrate* will converge. Mistral-7B-v0.3 + r14 has no analogous saturation argument; the φ_target is unconstrained.

### 6.5 Cost of being wrong is asymmetric

- Cost of **running §5 and confirming RED**: $5, +1 day. *Strengthens* the sunset decision.
- Cost of **running §5 and getting MEASUREMENT-ARTIFACT**: $5, +1 day, +epistemic confusion (have to design v2 protocol).
- Cost of **NOT running §5 and sunsetting**: 0, but leaves a known-unaddressed user question on the record.
- Cost of **running §5 and getting GREEN-flip**: $5, +1 day, but reverses a major closure decision — high asymmetric value if it happens (~5 % × decision-reversal payoff).

EV calculation favors **running §5 before any sunset commit**, on pure information-value grounds, regardless of the prior probability.

### 6.6 The hexa runtime itself has not been measured for Φ

`anima-core/runtime/anima_runtime.hexa`'s `mind_step()` has `phi`, `phi_peak`, `tension`, `curiosity`, `arousal`, `valence` — these are *internal labels*, not externally-measured Φ. The hexa runtime has **never been put through the 14-gate L1 verifier**. So even if §5 runs, the comparison is "ALM φ_vec" vs "static ALM φ_vec," not "ALM φ_vec" vs "anima-native runtime φ_vec." For full epistemic closure, one would also want the anima-native runtime's L1 score as a third reference point — out of scope here.

---

## §7 User Decision Point

| Option | Description | Cost | ETA | Leaves what unanswered? |
|---|---|---|---|---|
| **(a)** | Build §5 protocol + run 100-step closed-loop + control. Make sunset decision *after* result. | ~$5 + ~450 LOC | 1 day | Nothing (best epistemic closure) |
| **(b)** | Tension field already partially exists (B is live in hexa runtime). Build only the bridge to ALM r14, run §5. | Same as (a) | Same as (a) | Same as (a) — (b) is identical to (a) given §1 inventory |
| **(c)** | Reject this hypothesis. Static measurements + JSD + V_phen + alpha smoke are sufficient. Sunset as-planned per `strategic_alm_clm_review_2026_05_01.md`. | $0 | now | Whether RED is static-artifact (~5 % residual probability — accepted) |
| **(d)** | Build a *different* dynamic verifier (e.g. multi-turn dialog Φ over 50 turns, no closed-loop hook) — cheaper than §5, weaker signal. | ~$2 | half-day | Whether closed-loop tension dynamics specifically would flip RED |

**Recommendation if user wants to truly settle the question**: **(a)** at $5 / 1 day is the highest-information option with bounded downside.

**Recommendation if user wants to ship the sunset decision now**: **(c)**, with an explicit annotation in the closure ledger that "live tension-field deploy untested; ~5 % residual probability of static-measurement artifact accepted."

User decision required: which of (a) / (b≡a) / (c) / (d)?

---

## §8 References

- `anima-core/tension_bridge.hexa:1-458` — 5-channel WHAT/WHERE/WHY/TRUST/WHO bridge
- `anima-core/runtime/anima_runtime.hexa:195-339` — `ConsciousMind.tension` live update
- `anima-core/runtime/conscious_chat.hexa:156-192,279-300` — `bridge_forward` socket, `agi_generate` loop
- `docs/btr_evo_4_eeg_closed_loop_20260421.md` — closed-loop precedent (toy)
- `docs/new_paradigm_edu_lattice_unified_20260421.md:65-123,169,216,246` — `tension_field` over atlas_graph (referent C)
- `docs/strategic_alm_clm_review_2026_05_01.md` — ALM RED closure parent
- `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json` — RED ledger
- `tool/phi_substrate_probe.hexa` — phi_vec extraction (already exists, reusable in §5 readback)
