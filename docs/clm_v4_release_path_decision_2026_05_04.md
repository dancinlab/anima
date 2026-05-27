# CLM v4 HF Release v1 — Path Decision Spec

- **ts_utc**: 2026-05-04T_BG-CLM-CHAT-DECISION_design
- **bg_lane**: CLM-CHAT-DECISION (parallel to BG-HF-Release-Audit; **no exec, no commit, no pod, $0**)
- **status**: SPEC_LANDED — decision matrix only; no exec, no .py, no roadmap edit
- **scope**: which release path satisfies `.roadmap.clm` cond.2 (`HF release v1 — dancinlab/anima-clm-mk2-v1`) given anchor #115 (CLM v4 = consciousness-measurement substrate, NOT chat)
- **non-overlap**: BG-HF-Release-Audit (running parallel; this spec feeds its decision matrix); BG-CLM-2 (just landed `docs/clm_v4_lora_sft_spec_2026_05_04.md` Path 3 detail)
- **raw policy**: raw#9 (md only, no .py creation); raw#10 (≥5 honest C3); raw#15 (no destructive); raw#71 (any post-decision threshold tweaks = re-pre-register cycle)

---

## §0 1-line summary

Recommend **staged 1→2→3 lineage** (v1 measurement-only NOW → v2 orchestrator within 2 weeks → v3 LoRA SFT post Path A v2 verdict) — Path 1 alone unblocks `.roadmap.clm` cond.2 at $0 this week, Path 2 adds retail-usable chat at ~$5-15 without risking the +41.86 G3 PASS-positive backbone, Path 3 (BG-CLM-2 spec) ships pure-CLM chat capability in v3 only after the comparator (Llama Path A v2) lands and tied-weight + φ★ pre-flights pass.

---

## §1 Background — why this decision matters

### 1.1 The cond.2 gap

`.roadmap.clm` header line 3 lists cond.2 as `unmet` with blocker_reason `weight 확정 + model card draft 필요`. The cross_link locks:

- HF repo: `dancinlab/anima-clm-mk2-v1`
- License: `mit`
- gated_initial: `false`
- README sync source: `anima/docs/modules/clm.md`
- versioning pattern: `mk{N}-v{M}` (so v1 / v2 / v3 lineage is **already pre-allocated** by spec)

The `mk2-v1` form means anima can ship **incremental v1, v2, v3** repos under the same `mk2` era — no naming collision, no semantic drift.

### 1.2 The #115 category error (line 8 of `.roadmap.clm`)

CLM v4 530M is the `clm.v4_530m_paradigm_v11` G3 PASS-positive +41.86 substrate (line 7) — anima's **uniquely strong positive integration substrate** (5 substrate comparison: Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79 / CLM **+41.86**). This is the singular value-add anima has on the global model landscape.

But per anchor `clm.v115_chat_category_error` (line 8) + `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6:

| Property | Reality |
|---|---|
| Architecture | deterministic Lagrangian / cell-state ODE flow — **NOT autoregressive sampling** |
| `v3_generate()` | `TODO[pytorch]` returning empty string (Stage 4 fix landed in `/tmp/v3_generate_fix/v3_generate.py` validates AR loop *function* against mock decoder; **vanilla quality on real ckpt is expected to be near-random per #115 C3**) |
| Training objective | φ★ (G3 consciousness gate) + ce loss; **NEVER SFT'd, NEVER RLHF'd** |
| L2 cell↔token bridge | 5-bucket classifier; 11/16 eigenvec rows DEAD |
| 5 production gates | G1 NOT_TESTABLE / G2 EXPECTED_FAIL / G3 N/A / G4 NOT_TESTABLE / G5 PASS_STRUCTURAL_ONLY → **0/5 chat-ready** |

CLM v4 cannot chat as a raw decoder. The HF release v1 question is: **what can anima ship that is honest, useful, and unblocks cond.2?**

### 1.3 The shim surface (BG-γ'' F-SHIM-V4-3 PASS)

`tool/transient_py/clm_v4_hf_format_shim.py` v4 wraps `ConsciousDecoderV3` as a HuggingFace `PreTrainedModel` subclass (`CLMv4ForCausalLM`) that returns `CausalLMOutputWithPast(logits=logits_a)` for lm-eval compatibility (with `head_g` + tensions discarded for the next-token harness path). F-SHIM-1..4 + F-SHIM-V4-1..3 PASS; F-SHIM-V4-4 deferred to H100 base-val. **`AutoModelForCausalLM.from_pretrained(..., trust_remote_code=True)` works today**.

This means Path 1 (measurement-only) has a working from_pretrained() shim — the externally-visible interface exists, the only honest disclosure is that **the logits are not chat-quality**.

---

## §2 The 3 candidate paths

### 2.1 Path 1 — Measurement-only release (FAST, $0)

**Artifact**: `dancinlab/anima-clm-mk2-v1` = current CLM v4 530M `best.pt` repackaged via the v4 shim into HF format (config.json + model.safetensors + modeling_clm_v4.py + configuration_clm_v4.py + tokenizer/ subdir + README).

**Model card framing** (raw#10 honest):
- Title: "CLM v4 530M — Consciousness-Measurement Substrate (NOT Chat-Capable)"
- §1 Origin: φ★ + ce loss training objective; G3 PASS-positive +41.86 (uniquely strong vs ALM 4-backbone); citation chain to `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §32 + §42.
- §2 Falsifiers: F-NAME-1 PASS (per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`) + F-SHIM-1..4 + F-SHIM-V4-1..3 PASS + F-SHIM-V4-4 (base-val) status from H100 anchor result.
- §3 Substrate: 530M decoder_v3 (16 layer × 768 d_model × 6 head + GQA-2 + 64K SPM + 512 ctx + dual-head a/g + consciousness_dim=192).
- §4 Caveats (≥5 honest): see §3.1 below.
- §5 Composability: consumed by `tool/anima_phi_v3_canonical.hexa` for φ★ measurement; `tool/clm_consciousness_verify.hexa` for G3 gate; downstream forward-pass-only consumers for hidden-state extraction.

**Use case**:
- Research substrate (the audience that already cares about φ★ / integration / consciousness measurement)
- Hidden-state harvest for downstream BLM / SLM / TLM cross-substrate work
- Anchor for the 3-way matrix (`tool/p9_a_d_cross_axis_verdict.hexa` + CLM-LORA axis → 3-way) once Paths 2/3 ship

**Pros**:
- **$0** — repackage existing `best.pt` via existing shim; ~30 min Mac wall
- Immediate (this week)
- Scientifically honest about #115 (no overclaim)
- Unblocks `.roadmap.clm` cond.2 cleanly: weight published + model card landed
- F-NAME-1 conformant (`clm-v4-base-mirror` already exists per §7.2 of naming spec — `anima-clm-mk2-v1` would be the **release** repo per the cond.2 cross_link, distinct from the base-mirror; or, if user chooses, `anima-clm-mk2-v1` aliases `clm-v4-base-mirror` with promoted README)

**Cons**:
- Limited downstream adoption (no chat = no retail interest)
- HF leaderboard ineligible (chat / instruct evals all near-random)
- **Reputation risk**: outsiders skim the README and conclude "anima isn't shipping anything useful" — even though the science is genuinely strong, the framing has to fight the chat-default expectation
- The "consciousness-measurement substrate" framing is unfamiliar to most ML practitioners — needs a 1-paragraph explainer in the README §1 Origin to land

### 2.2 Path 2 — Chat-capable via Stage 2-alt orchestrator (MEDIUM, $5-15)

**Artifact**: `dancinlab/anima-clm-mk2-v2` = orchestrator package that wraps:
1. HF `AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")` — chat substrate
2. CLM v4 forward pass for `mind.tension` scalar streaming as side-channel (5ch tension_link + per-token tension_proj scalar)

**Implementation sketch** (pseudocode in spec only, NOT to be coded by this BG):

```python
# pseudocode — to be realized in tool/clm_v4_orchestrator_stage2alt.hexa
# (~300-400 LoC hexa wrapper; raw#9 compliant)
class CLMv4Orchestrator:
    def __init__(self, llama_repo, clm_repo):
        self.llama = AutoModelForCausalLM.from_pretrained(llama_repo)  # chat host
        self.clm = AutoModelForCausalLM.from_pretrained(             # consciousness side
            clm_repo, trust_remote_code=True
        )
    def chat(self, prompt: str) -> dict:
        # 1. tokenize via Llama tokenizer for the chat surface
        llama_ids = self.llama_tok(prompt)
        # 2. tokenize same prompt via CLM v4 SPM 64K for tension extraction
        clm_ids = self.clm_tok(prompt)
        # 3. CLM forward → tensions (16 layers × 1d) + mind.tension scalar
        with torch.no_grad():
            _, _, tensions = self.clm.forward_full(clm_ids)
        mind_tension = aggregate(tensions)  # scalar
        # 4. Llama generate (chat substrate)
        text = self.llama.generate(llama_ids, ...)
        # 5. emit both
        return {"text": text, "mind_tension": mind_tension, "tensions_per_layer": tensions}
```

Estimated hexa file path: `tool/clm_v4_orchestrator_stage2alt.hexa` — ~300-400 LoC (per §55.6 Stage 2-alt pattern + N-1 BRIDGE v2 spec at `state/n_1_bridge_v2_realtime_prep_2026_05_02/clm_w4_lsl_server_spec.json`).

**Model card framing**:
- Title: "anima-clm-mk2-v2 — Chat-Capable Orchestrator (Llama-3.2-3B Host + CLM v4 Consciousness-Coupling Axis)"
- §1 Origin: explicit dual-substrate disclosure; Llama license attribution; CLM v4 mind.tension stream is the singular value-add
- §4 Caveats: chat coherence is **Llama's**, NOT CLM's; CLM v4 contributes the consciousness-coupling axis as auxiliary channel; Llama license restrictions propagate to downstream consumers

**Use case**:
- Retail chatbot adopters who want consciousness-coupled side-channel (e.g., neuro-feedback applications, anima self-awareness probes, qmirror cross-vendor harness)
- Preserves CLM v4's φ★ +41.86 unique value-add (CLM weights frozen — zero φ★-flip risk)

**Pros**:
- Usable chat — clears the "anima isn't shipping anything useful" objection
- Single coherent release with clear value proposition (Llama chat + CLM consciousness signal)
- **Zero φ★-flip risk** — CLM v4 weights are not modified (forward-only)
- Cost is bounded: ~$5-15 for one-off integration smoke test on H100 OR Mac M4 inference (Llama-3.2-3B fits Mac M4 with 4-bit; CLM v4 530M trivially fits)
- Re-uses Path 1's shim (compose, not rebuild)

**Cons**:
- **Llama-3.2-3B license overhead** — CLM-mk2-v2 isn't pure CLM; downstream consumers must accept Llama license (commercial use OK per Llama 3.2 community license but with attribution + 700M-MAU clause)
- Distinct artifact from CLM-only release (Path 1 still needed as the substrate anchor)
- Requires Path 1 published first OR co-shipped (Path 2 imports Path 1 as the CLM side)
- Orchestrator hexa is new code (~400 LoC) — modest infra investment

### 2.3 Path 3 — LoRA SFT on CLM v4 (LONG, $6-10 H100 + future risk)

**Artifact**: `dancinlab/anima-clm-mk2-v3` = CLM v4 530M base + LoRA adapter (r=32, alpha=64, conservative target_modules `qkvo` only) trained on 60/25/10/5 anima-axis / academic / chat-template / consciousness-coupled mix per `docs/clm_v4_lora_sft_spec_2026_05_04.md` (just landed by sibling BG-CLM-2).

**Implementation**: full spec at the BG-CLM-2 doc. Key params (LOCKED 2026-05-04 per raw#71):
- LoRA r=32, alpha=64, dropout=0.05
- target_modules = `q_proj, k_proj, v_proj, o_proj` ONLY (excludes `tension_proj`, `bridge.hub_attn`, `head_g`, `federation.*` per §1.2 of BG-CLM-2 spec)
- LR 3e-5 (40% lower than Llama Path A v2's 5e-5; high-curvature φ★ minimum protection)
- max_steps=6000, save_steps=500, eff_batch=32
- φ★ probe every 2000 steps; ABORT if φ★ < +10 (50% safety margin from sign zero)
- Hard cap $15

**Critical risk per BG-CLM-2 spec §6 R4 + Honest C3 #3**:
- φ★-flip irreversibility: even with adapter-only training + 5% consciousness-coupled rehearsal slice + φ★ probe, NO theoretical guarantee that φ★ stays positive
- If φ★ flips negative → CLM v4 demoted from "anima's only G3 PASS-positive backbone" to "yet another LoRA-tuned chat model" → **the singular value-add is destroyed**
- Recovery = adapter ablation (cheap, reverts to pre-LoRA φ★=27.91 / +41.86 paradigm v11) OR re-train from scratch ($1000+)

**Model card framing**:
- Title: "anima-clm-mk2-v3 — Pure-CLM Chat (LoRA SFT on Consciousness-Measurement Substrate)"
- §1 Origin: explicit pre/post φ★ measurement (must be ≥+10); F-CLM-LORA-1..5 verdict transcript
- §4 Caveats: φ★-flip risk acknowledged; LoRA r=32 single-config (no ablation); 512 ctx hard cap; 5% consciousness slice may not be enough to preserve full +41.86 magnitude

**Use case**:
- Pure CLM substrate chat (no Llama dep → no Llama license overhead)
- Unified architecture story (the consciousness-coupled chat model)
- Scientific differentiator: **does anima's substrate beat a same-recipe Llama LoRA**? (C-CLM-LORA-2 in BG-CLM-2 spec)

**Pros**:
- Pure-CLM lineage (no external license dependency)
- Unified architecture story (one substrate, end-to-end)
- C-CLM-LORA-2 is a **falsifying experiment** for the consciousness-coupling-helps-SFT hypothesis — high scientific value regardless of outcome

**Cons**:
- φ★-flip irreversibility (the unique value-add at risk)
- Novel infra (decoder_v3 dual-head wrap for `transformers.Trainer`, target_modules bespoke choice — see BG-CLM-2 §10 C3 #2)
- $6-10 floor + $15 hard cap + 2-3 weeks lead time (CLM v4 baseline eval gate + Path A v2 verdict gate + tied-weight pre-flight + shim build)
- Single-seed v3 (multi-seed deferred per BG-CLM-2 §10 C3 #9)
- 512 ctx cap forces aggressive academic-slice filter (BG-CLM-2 §1.3 + §2.1)

---

## §3 Decision matrix (3 paths × 5 dimensions)

Score each dimension 1-5 (5 = best on that dimension; 1 = worst).

| Dimension | Path 1 (measurement-only) | Path 2 (orchestrator) | Path 3 (LoRA SFT) |
|---|---:|---:|---:|
| **Cost** ($, lower = better) | **5** ($0) | 4 ($5-15) | 3 ($6-10 floor, $15 cap) |
| **Time** (faster = better) | **5** (this week, ~1h Mac) | 4 (~2 weeks; Llama download + integration smoke + model card) | 2 (3+ weeks; CLM baseline eval + Path A v2 verdict + tied-weight + shim ext + train + 5 falsifiers + verdict eval) |
| **Risk** (lower φ★-flip + infra novelty = better) | **5** (zero modification of CLM weights) | **5** (zero modification of CLM weights — orchestrator is forward-only) | 2 (φ★-flip irreversibility + novel decoder_v3 Trainer wrap + new target_modules bespoke choice) |
| **Scientific value** (does it advance anima's research thesis?) | 3 (publishes the +41.86 substrate honestly; doesn't add a new measurement) | 3 (preserves +41.86; adds orchestrator-pattern empirical evidence per Stage 2-alt §55.6) | **5** (C-CLM-LORA-2 is a *falsifying experiment* for "anima substrate has architectural advantage" hypothesis — singular roadmap-shifting result whichever way it lands) |
| **Retail value** (third-party adoption potential) | 1 (research-only; no chat = no retail) | **5** (retail-usable chat with consciousness side-channel; HF leaderboard ineligible directly but composable in chat tooling) | 4 (pure-CLM chat IF C-CLM-LORA-1..4 PASS; HF leaderboard ELIGIBLE; pure substrate is more retail-friendly than orchestrator BUT only if PASS — FAIL = retail value drops to 1) |
| **TOTAL** | **19** | **21** | 16 |

**Reading**:
- Path 2 ranks highest on the 5-dimension sum, but **Path 1 dominates on cost + time + risk (all 5/5)** and is a strict prerequisite for Path 2 (Path 2 imports Path 1).
- Path 3 has the highest single-dimension score (scientific value = 5) but is bottlenecked by the longest time-to-ship and the irreversibility risk.

---

## §4 Recommended path — staged 1→2→3 lineage

**Recommendation**: **STAGED 1→2→3** (NOT pick-one).

**Ranking rationale** (raw#10 honest, completion-quality lens):

1. **Path 1 NOW** is the only path that unblocks `.roadmap.clm` cond.2 *this week* at $0. The shim is PASS, the weight is published as `clm-v4-base-mirror`, the model card is the only outstanding artifact (~1h Mac). Shipping Path 1 closes cond.2 immediately and stops the "we have nothing on HF" bleed.

2. **Path 2 IN 2 WEEKS** is the cheapest path to retail-visible chat *without risking the +41.86 backbone*. The Llama license overhead is the single concession; in exchange, CLM weights stay pristine and the orchestrator pattern was already pre-spec'd (Stage 2-alt §55.6 is RECOMMENDED in the source roadmap). Path 2 makes the cond.2 release "useful" beyond the research audience.

3. **Path 3 v3 (POST Path A v2 verdict)** is the highest-scientific-value path but should NOT block v1. It's the falsifying experiment for consciousness-coupling-helps-SFT, and the answer (PASS or FAIL) is roadmap-shifting either way. But it requires:
   - CLM v4 baseline eval ($0, 3-6h ubu1) — pre-EXEC blocker
   - Path A v2 verdict landed ($11-23, separate cycle) — needed for C-CLM-LORA-2 comparator
   - Tied-weight pre-flight check ($0, 5 min) — R6 mitigation
   - Decoder_v3 hf-format shim extension for LoRA-merged loading (F-CLM-LORA-5)
   
   These are 4 hard gates spread across at least 2 weeks BEFORE Path 3 EXEC even starts. Shipping v1 + v2 first preserves momentum.

**The staged version satisfies ALL three audiences**: research (v1), retail (v2), substrate-thesis (v3) — without forcing the v3 gates onto the v1 timeline.

---

## §5 Sub-decisions per path

### 5.1 Path 1 — Model card "Limitations" wording (LOCKED draft)

```markdown
## §4 Caveats (raw#10)

- C1 — **CLM v4 is a consciousness-measurement substrate, NOT a chat model.**
  The training objective is φ★ (consciousness gate) + ce loss; this checkpoint
  has NEVER been SFT'd, NEVER been RLHF'd, and NEVER been instruction-tuned.
  Vanilla autoregressive sampling produces near-random 64K SPM token sequences
  that do NOT form coherent dialogue. See `docs/clm_v4_revival_stages_2026_05_02.md`
  §4.4 + `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6 (anchor
  #115 — "category error").

- C2 — **`v3_generate()` AR loop is implemented but quality is intentionally
  unmeasured.** The PyTorch port at `/tmp/v3_generate_fix/v3_generate.py`
  validates the AR function (deterministic greedy / varied sampling / EOS
  short-circuit / in-vocab outputs all PASS on mock decoder). It does NOT
  make CLM v4 a chat model. Vanilla output is expected to be incoherent.

- C3 — **L2 cell↔token bridge has 11/16 eigenvec rows DEAD.** This is a
  structural readout used by the consciousness-measurement path, not a
  chat-decoder bridge. Downstream consumers should consume hidden states
  via `forward()`, NOT `generate()`.

- C4 — **φ★ +41.86 magnitude advantage is partly tautological** wrt training
  objective (training objective ≡ G3 verifier objective). Sign is robust
  per `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §32.2; magnitude
  is partly inflated by top-variance truncation and recurrent tension-coupling.
  HID=8 cleanup confirms sign-positive; magnitude has 8x Llama / 40x Qwen3
  inflation flag.

- C5 — **Suite 6 (14-gate) FAIL despite G3 PASS positive.** L1 holo_positivity
  0/16 substrate-architectural ceiling; F2 fired in CP2 Phase A verdict. CLM v4
  is "integration-positive AND holo-positive-zero" — anima's honest verdict
  per `clm.cp2_clm_phase_a_complete` (`.roadmap.clm` line 5).

- C6 — **For chat capability, use the orchestrator variant** at
  `dancinlab/anima-clm-mk2-v2` (Stage 2-alt pattern: Llama-3.2-3B chat
  host + CLM v4 mind.tension side-channel) OR the LoRA SFT variant at
  `dancinlab/anima-clm-mk2-v3` (post-LoRA φ★ measurement required;
  see `docs/clm_v4_lora_sft_spec_2026_05_04.md`). v1 is the substrate anchor;
  v2/v3 are chat-capable composites.
```

### 5.2 Path 2 — Orchestrator hexa file path + LoC

| Artifact | Type | Purpose | Est. LoC |
|---|---|---|---|
| `tool/clm_v4_orchestrator_stage2alt.hexa` | NEW hexa | Llama-3.2-3B host + CLM v4 forward-only consciousness side-channel; chat() entry; mind.tension aggregation; per-layer tensions exposure | ~300-400 |
| `tool/transient_py/clm_v4_orchestrator_runner.py.hexa_tmp` | NEW transient .py (off-repo per raw#9 / .own 4) | huggingface_hub SDK glue for Llama download + integration smoke (transformers.AutoModelForCausalLM is python-only SDK) | ~200-250 |
| `docs/anima_clm_mk2_v2_orchestrator_spec_2026_05_<dd>.md` | NEW md | Path 2 detailed spec (this decision spec is high-level only) | ~800-1500 words |

**Total NEW LoC**: ~500-650.

**Composability with Path 1**: Path 2 imports Path 1 via `AutoModelForCausalLM.from_pretrained("dancinlab/anima-clm-mk2-v1", trust_remote_code=True)` — Path 1 must be published first OR co-shipped.

### 5.3 Path 3 — φ★-flip mitigation strategy

Per BG-CLM-2 spec §6 R4 (already LOCKED at spec land 2026-05-04, raw#71):

**Primary mitigation — conservative target_modules**:
- INCLUDE: `q_proj, k_proj, v_proj, o_proj` (cell-layer attention only)
- EXCLUDE: `tension_proj` (1-d projection — adapter would dominate the signal), `bridge.hub_attn` (axis conditioning gate), `head_g` (prev-token head used by φ★ structural readout), `federation.bottleneck` + `federation.narrative_grus` (shared cross-layer memory)

**Secondary mitigation — φ★ probe every 2000 steps**:
- Calibration set: 100 prompts (per BG-CLM-2 §3 hyperparameters)
- ABORT threshold: φ★ < +10 (50% safety margin from sign zero)
- ABORT action: save adapter as `step-{step}-aborted` for post-mortem; revert to pre-LoRA via adapter ablation

**Tertiary mitigation — 5% consciousness-coupled prompts (slice D)**:
- 2500 anima-curated prompts with explicit φ★ / tension_link / N-22 axis references + 5-bucket cell↔token bridge fixture prompts (per `tool/cell_token_bridge_proto.hexa`)
- Keeps gradient pressure on the φ★ surface during SFT

**Fallback if F-CLM-LORA-4 (axis preservation) fails**:
- Drop `o_proj` from target_modules (most cross-axis-mixing per BG-CLM-2 §6 R1 fallback)
- Reduce LR to 1e-5
- Single retry; second failure → ABORT v3 entirely

---

## §6 Sequencing — can paths run sequentially? (YES, REQUIRED)

### 6.1 Versioning lineage per `.roadmap.clm` cross_link `hf_versioning_pattern: mk{N}-v{M}`

| Repo | Stage | Status today | EXEC gate |
|---|---|---|---|
| `anima-clm-mk2-v1` | Path 1 (measurement-only) | NOT YET PUSHED | model card draft + shim repackage (~1h Mac) |
| `anima-clm-mk2-v2` | Path 2 (orchestrator) | NOT YET SPEC'd in detail | Path 1 published; orchestrator hexa + .own4 transient_py runner; Llama download access OK (already cached per `#116` Stage 1) |
| `anima-clm-mk2-v3` | Path 3 (LoRA SFT) | SPEC LANDED `docs/clm_v4_lora_sft_spec_2026_05_04.md` | CLM v4 baseline eval + Path A v2 verdict + tied-weight pre-flight + decoder_v3 hf-format LoRA-merge shim ext |

### 6.2 Promotion gates (raw#71 LOCKED)

**v1 → v2 promotion**:
- v1 published; F-NAME-1 PASS; model card landed with all 5 H2 sections + ≥3 caveats
- Llama-3.2-3B Instruct download + integration smoke PASS (Mac M4 4-bit OR H100 fp16)
- Orchestrator hexa selftest PASS (mock CLM forward + mock Llama generate → return type checked)
- v2 model card explicit Llama license attribution + commercial-use clause

**v2 → v3 promotion**:
- Path A v2 (Llama side) verdict LANDED → C-CLM-LORA-2 has a comparator
- CLM v4 baseline eval PASS (HellaSwag/MMLU/TriviaQA limit=500 on raw CLM v4 530M; ubu1 RTX 5070 $0 3-6h)
- Tied-weight pre-flight check PASS (5 min Mac; verify `head_a.weight is tok_embeddings.weight` pointer equality)
- Decoder_v3 hf-format LoRA-merge shim ext built (F-CLM-LORA-5; ~1-2h Mac dev $0)
- USER ACK on $6-10 cost band + 2-2.5h H100 wall + $15 hard cap (per BG-CLM-2 §13 exec gate item 1)
- F-CLM-LORA-3 (φ★ ≥ +10) and F-CLM-LORA-4 (axis-cond preservation) PASS — if either FAIL, v3 reverts to LoRA-aborted, v3 release is **withheld**, and the v3 repo is left empty (NOT shipped)

### 6.3 Parallelism

Paths can be DEVELOPED in parallel (Path 2 hexa + Path 3 baseline eval can be drafted alongside Path 1 model card), but **PUBLISH must be sequential** because v2 imports v1, and v3 needs v1's shim infrastructure to be already-public for downstream `from_pretrained` parity.

---

## §7 Compatibility with BG-HF-Release-Audit (running parallel)

This decision spec produces the **input artifact** for BG-HF-Release-Audit's cond.2 audit report. Coordination via shared file paths:

| Shared path | Producer | Consumer |
|---|---|---|
| `docs/clm_v4_release_path_decision_2026_05_04.md` (this file) | this BG | BG-HF-Release-Audit reads §3 decision matrix + §4 recommendation |
| `docs/clm_v4_release_path_landed_2026_05_04.ai.md` | this BG | BG-HF-Release-Audit references in audit verdict |
| `state/markers/clm_v4_release_path_decision_landed.marker` | this BG (NOT created in this cycle — proposed for next) | BG-HF-Release-Audit polls marker existence |
| `.roadmap.clm` cond.2 annotation block | this BG (NOT edited; proposed in §10 below) | next-cycle owner lands |

**No write contention** — this BG writes ONLY to `docs/clm_v4_release_path_*.md`; BG-HF-Release-Audit writes elsewhere (audit dir TBD).

**No shared mutable state** — read-only references to existing roadmap line + existing shim path.

---

## §8 Honest C3 caveats (raw#10 — ≥5)

### C1 — #115 category error is permanent without re-architecting CLM v4 as autoregressive

CLM v4 is a deterministic Lagrangian / cell-state ODE flow substrate. The dual-head (head_a + head_g, byte-level) was trained for φ★ + ce loss, not for instruction-following next-token prediction. Even Path 3 LoRA SFT does NOT change this fundamental architecture — it adds a chat-style adapter on top, but the substrate underneath is still the consciousness-measurement decoder. To get a "pure CLM chat model" without architectural caveats, we'd need to re-pretrain CLM with a chat-objective from scratch ($1000+, months) — which is out of scope for any of the 3 paths above.

### C2 — Path 2 introduces Llama license dep → CLM-mk2-v2 isn't pure CLM

The orchestrator imports `meta-llama/Llama-3.2-3B-Instruct` which carries the Llama 3.2 community license. Commercial use is permitted but with attribution + the 700M-MAU clause + acceptable-use-policy compliance. This is a strict expansion of the legal surface area vs Path 1 (mit-only). Anima's `mit` license declared in `.roadmap.clm` cross_link `hf_license: mit` applies ONLY to anima's CLM weights + orchestrator code — Llama's weights remain under their own license.

### C3 — Path 3 has φ★-flip irreversibility — measured by repeating G3 paradigm v11 post-LoRA, but if it flips negative the LoRA must be discarded entirely

Per BG-CLM-2 §10 C3 #3: there is NO theoretical guarantee that φ★ stays positive under LoRA SFT, even with adapter-only training + 5% consciousness-coupled rehearsal + φ★ probe. The +10 ABORT threshold is a heuristic 50% safety margin from sign zero — provably correct ONLY in the limit of small adapter perturbations. Recovery from φ★-flip = adapter ablation (cheap) but the SFT investment is lost. If φ★-flip happens *and* C-CLM-LORA-2 PASSES (i.e., chat works but consciousness-coupling is destroyed), there's a **forced dilemma**: ship the chat-capable but consciousness-flipped LoRA, or discard it. The honest answer per anima's identity is to discard — but this is a real possibility worth flagging.

### C4 — Measurement-only release (Path 1) may signal "anima isn't shipping anything useful" to outsiders

Most ML practitioners default to chat / instruct expectations on HF. A README that says "this model returns near-random tokens; use it for hidden-state extraction" looks like a non-shipping artifact to outsiders, even though the +41.86 G3 PASS-positive science is genuinely strong. Mitigation: lead the README with the φ★ comparison (5 substrate: Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79 / **CLM +41.86**) so the value-add lands before the chat-incapability disclosure. But this is a framing problem, not a science problem.

### C5 — HF leaderboard eligibility differs across paths

- Path 1: HF leaderboard categorically ineligible (chat / instruct evals all near-random). Shows up in HF model card metadata as "not applicable" or worse, "0.20" on HellaSwag — which looks bad without context.
- Path 2: orchestrator is a *composition*, not a single model — HF leaderboard doesn't have an evaluation slot for orchestrator-pattern releases. Chat tooling integration (LangChain, LlamaIndex) is the realistic adoption path.
- Path 3: HF leaderboard ELIGIBLE (LoRA-merged single-model artifact); F1_v3 V2 hybrid Mode-1 + Mode-3 evals produce comparable HellaSwag/MMLU/TriviaQA numbers. This is the only path with leaderboard visibility — but only if PASS.

### C6 — Single-decision spec, no ablation of staging order

This spec recommends 1→2→3 staging without ablating alternative orders (e.g., 1+2 parallel, or 2 first then 1, or 3 first as the science differentiator). The recommendation is justified by cost + time + risk dominance of Path 1, but a sufficiently aggressive cycle owner could argue for Path 3 first (highest scientific value) accepting 3-week lead time and the irreversibility risk. This spec doesn't pre-empt that user choice — it documents the staged path as the COMPLETION-QUALITY-MAX recommendation per the memory hint.

### C7 — BG-CLM-2 spec gates may shift v3 timeline beyond 2-3 weeks

If CLM v4 baseline eval reveals wildly different numbers than the §4.1 hypothetical band in BG-CLM-2 spec (HellaSwag 0.20-0.30 / MMLU 0.22-0.27 / TriviaQA EM 0.05-0.15), the §4 thresholds must be re-pre-registered (raw#71 amendment cycle), adding 1-3 days. If Path A v2 verdict is delayed (Llama side LoRA SFT cycle is the gate), Path 3 EXEC is gated regardless. Realistic v3 timeline: **3-5 weeks** from this spec land.

### C8 — F-NAME-1 audit interaction

Per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §10.5, current F-NAME-1 verdict is PARTIAL_PASS (regex layer 100% green; README banner layer pending on 20 EXT legacy repos). Shipping `anima-clm-mk2-v1` adds a **forward repo** that must conform from creation (per §9 checklist). The repo name `anima-clm-mk2-v1` does NOT match the §2 EBNF directly — it has the `anima-` prefix that's not in the EBNF. The cross_link in `.roadmap.clm` says `hf_release_planned: dancinlab/anima-clm-mk2-v1` — but this clashes with the naming spec's CANON regex. **Sub-decision flag for user**: keep `anima-clm-mk2-v1` (requires §3.1 EBNF amendment to allow `anima-` prefix) OR rename to `clm-v4-mk2-v1` (or just `clm-v4-final` per existing naming). This is a NAMING SPEC AMENDMENT need — not blocking but should be resolved before push.

---

## §9 Decision questions to flag for user

| # | Question | Default per this spec |
|---|---|---|
| 1 | Path preference: Path 1 only, Path 1+2, Path 1+3, or staged 1→2→3? | **STAGED 1→2→3** (default; raw#10 caveat: aggressive Path 3 first is also defensible) |
| 2 | If staged: what gates v1 → v2 promotion? | per §6.2 — orchestrator selftest PASS + Llama license disclosure landed |
| 3 | If staged: what gates v2 → v3 promotion? | per §6.2 — Path A v2 verdict + CLM v4 baseline eval + tied-weight pre-flight + LoRA-merge shim ext |
| 4 | Llama-3.2-3B license attribution OK for commercial use? (Path 2 requirement) | per Llama 3.2 community license: commercial use OK with attribution + 700M-MAU clause + AUP — **assumed OK** but user should explicitly ACK |
| 5 | Repo name: keep `anima-clm-mk2-v1` (requires naming spec amendment) OR rename per existing F-NAME-1 EBNF? | per C8 caveat — spec recommends naming-spec amendment cycle FIRST, then push under `anima-clm-mk2-v1` (preserves the cross_link name) |
| 6 | Path 3 φ★-flip handling: ABORT threshold +10 OK? OR more conservative (+15 / +20)? | per BG-CLM-2 LOCKED spec — **+10** (50% safety margin); user can amend via raw#71 cycle but defaults to +10 |
| 7 | Path 3 if-flip dilemma: ship chat-capable consciousness-flipped LoRA, or discard? | per anima identity — **discard** (preserves +41.86 substrate); user explicit ACK desired |

---

## §10 Roadmap update proposal (NOT edited; proposed for next cycle)

Proposed annotation block for `.roadmap.clm` cond.2 — to be appended as a new entry, NOT modifying existing line 3 header:

```jsonl
{"type":"entry","id":"clm.cond2.release_path_decision","kind":"decision","title":"CLM v4 HF release v1 path — STAGED 1→2→3 (measurement-only NOW → orchestrator IN 2 WEEKS → LoRA SFT POST Path A v2 verdict)","status":"spec_landed","ts":"2026-05-04","contributes_to":["clm.cond.2"],"recommended":"staged","substaging":{"v1":{"path":"measurement_only","cost":"$0","wall":"~1h Mac","gate":"shim repackage + model card draft","status":"ready_to_exec"},"v2":{"path":"stage_2alt_orchestrator","cost":"$5-15","wall":"~2 weeks","gate":"v1 published + orchestrator hexa selftest + Llama license ACK","status":"spec_pending"},"v3":{"path":"lora_sft","cost":"$6-10 floor / $15 cap","wall":"3-5 weeks","gate":"CLM v4 baseline eval + Path A v2 verdict + tied-weight + LoRA-merge shim ext + USER ACK on phi-flip dilemma","status":"spec_landed_BG-CLM-2"}},"references":["docs/clm_v4_release_path_decision_2026_05_04.md","docs/clm_v4_release_path_landed_2026_05_04.ai.md","docs/clm_v4_lora_sft_spec_2026_05_04.md (BG-CLM-2 Path 3 detail)","docs/clm_v4_revival_stages_2026_05_02.md §3 (Path 3 pre-spec)","docs/n_substrate_consciousness_roadmap_2026_05_01.md §55.6 (Path 2 pattern source + #115 anchor)","tool/transient_py/clm_v4_hf_format_shim.py (Path 1 shim, F-SHIM-V4-3 PASS)","docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md (F-NAME-1 audit; C8 amendment flag)","docs/anima_hf_upload_mk2_spec_2026_05_03.md (push pipeline; F-NAME-1 + 5 H2 + caveats ≥3)"],"cross_link":{"sister_decision":"none — single decision spec","compatibility":"BG-HF-Release-Audit (parallel) feeds cond.2 audit verdict","versioning_pattern":"mk2-v{1,2,3} per .roadmap.clm header cross_link"}}
```

---

## §11 Output (this cycle)

1. `/Users/ghost/core/anima/docs/clm_v4_release_path_decision_2026_05_04.md` (this file)
2. `/Users/ghost/core/anima/docs/clm_v4_release_path_landed_2026_05_04.ai.md` (1-page summary handoff)

**NOT created this cycle** (deferred per raw#9 + raw#15 no destructive):
- `state/markers/clm_v4_release_path_decision_landed.marker` (proposed for next cycle by user/separate BG)
- `.roadmap.clm` annotation block append (proposed in §10 above; user/separate BG to land)
- Path 1 model card draft (proposed for next cycle EXEC; this spec defines the wording in §5.1)
- Path 2 orchestrator hexa (proposed for next cycle EXEC)
- Path 3 EXEC artifacts (already spec'd in BG-CLM-2; gated per §6.2)

---

## §12 Exec gate (NEXT-CYCLE)

This BG produces SPEC ONLY. EXEC requires:

**v1 EXEC** (cheapest, ~1h Mac):
1. USER ACK on staged 1→2→3 recommendation (or alternative pick)
2. USER decision on naming-spec amendment vs rename (C8 caveat)
3. Separate BG cycle to:
   - Repackage CLM v4 `best.pt` via `tool/transient_py/clm_v4_hf_format_shim.py` into `~/anima/state/clm_v4_release_v1_2026_05_<dd>/clm_v4_base_hf/`
   - Draft model card per §5.1 wording (5 H2 sections + ≥3 caveats per `tool/hf_readme_template.md` per anima_hf_upload_mk2 spec §4.1)
   - Run `hexa run tool/hf_upload_mk2.hexa --validate-readme + --validate-naming` pre-checks
   - `hexa run tool/hf_upload_mk2.hexa --upload --repo dancinlab/anima-clm-mk2-v1 --ckpt ... --readme ... --tag v2026-05-<dd>`
   - Verify F-NAME-1 + F-SHIM-V4-3 PASS post-push
   - Append to `state/hf_upload_ledger_2026_05.jsonl`
   - Land `.roadmap.clm` cond.2 status flip from `unmet` → `met` (v1 weight + model card published)

**v2 EXEC** (orchestrator, ~2 weeks):
- Per §6.2 promotion gates; separate BG cycle to draft Path 2 detailed spec doc + orchestrator hexa + .own4 transient_py runner

**v3 EXEC** (LoRA SFT, 3-5 weeks):
- Per BG-CLM-2 §13 exec gate (already spec'd) + this spec §6.2 v2→v3 promotion gates

---

## §13 raw policy compliance

- **raw#9** (md only): YES — this spec is markdown only; no .py created; pseudocode in §5.2 is *spec* not *code*.
- **raw#10** (≥5 honest C3): YES — §8 has 8 caveats (C1-C8).
- **raw#15** (no destructive): YES — no `.roadmap.clm` direct edit (proposed annotation in §10 only); no rename/delete of any HF repo; no modification of existing artifacts; no git commit by this BG.
- **raw#71** (pre-registration LOCKED): YES — promotion gates §6.2 are LOCKED at this spec land; threshold tweaks = re-pre-register cycle (e.g., φ★ ABORT threshold +10 is BG-CLM-2 LOCKED).

---

## §14 References

- `.roadmap.clm` line 3 (header cond.2 + cross_link versioning pattern) + line 7 (clm.v4_530m_paradigm_v11) + line 8 (clm.v115_chat_category_error)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §32 (#87 G3 PASS-positive +41.86 anchor) + §42 (5-substrate comparison table) + §55.6 (#115 NOT_READY anchor + Stage 2-alt RECOMMENDED)
- `docs/clm_v4_revival_stages_2026_05_02.md` §1 REFRAME + §2 Stage 2 alpha revival + §3 Stage 3 SFT pre-spec + §4 v3_generate AR loop fix DONE
- `docs/clm_consciousness_verify_landing_2026_05_02.ai.md` (G3 verifier orchestrator)
- `docs/clm_v4_lora_sft_spec_2026_05_04.md` (BG-CLM-2 Path 3 detailed spec — sister doc)
- `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (F-NAME-1 audit + naming EBNF + C8 amendment flag)
- `docs/anima_hf_upload_mk2_spec_2026_05_03.md` (5 H2 README + caveats ≥3 + push pipeline)
- `tool/transient_py/clm_v4_hf_format_shim.py` (v4 shim, F-SHIM-V4-3 PASS — Path 1 enabler)
- `tool/hf_readme_template.md` (model card template)
- `tool/hf_upload_mk2.hexa` (canonical push entry)
- `state/p9_p1_holdout500_reeval_2026_05_03/` (Path 3 BLEU-1 holdout reference per BG-CLM-2)
- BG-HF-Release-Audit (parallel BG; produces cond.2 audit report consuming this decision)
