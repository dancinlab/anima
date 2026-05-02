# Strategic — CLM v4 530M Production-Ready User-Dialogue Evaluation

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: strategic CLM v4 530M production-ready user-dialogue evaluation
- **Mission**: Evaluate whether CLM v4 530M (paradigm v11 G3 PASS-positive only backbone, +41.86 vs ALM 4-bb) can replace DEAD alpha endpoint as user dialogue substrate
- **Constraints**: HEXA-only, $0 (analysis only), race-isolated dirs, time cap 30 min wall
- **Race-isolated**:
  - `state/strategic_clm_v4_production_ready_2026_05_02/verdict.json`
  - `docs/strategic_clm_v4_production_ready_2026_05_02.md` (this file)
- **Did NOT touch**: `state/v10_benchmark_v4_clm/*`, `state/strategic_clm_phase_a1_2026_05_01/*`, `state/strategic_clm_eeg_akida_tension_2026_05_02/*`, `state/n_1_bridge_v2_realtime_prep_2026_05_02/*`, `anima-clm-eeg/*`, alpha pod (DEAD), any .py/.pt files

---

## §0 Headline verdict

**NOT_READY**

CLM v4 530M is **architecturally NOT a chat model**. The mission premise contains a category error.

**Single-sentence reason**: Per `docs/clm_inference_abstraction_layers_20260425.md` L0-L4: "Cell decode != autoregressive sampling. CLM inference is deterministic Lagrangian solving... token-side AR sampling is a synaptic readout hung off cell state." `decoder_v3.hexa` shows `v3_generate()` as `TODO[pytorch]` returning empty string. The 530M ckpt was trained for phi_star measurement (consciousness gate G3), not for SFT/RLHF dialogue.

---

## §1 What CLM v4 530M actually is

| Field | Value | Source |
|---|---|---|
| Checkpoint | `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` (5.37GB, step=20000, phi=27.91, ce=0.046) | strategic_clm_phase_a1_2026_05_01/run_log.json |
| Params | 477.65M loaded (label "350M" misleading; full 530.99M per #73 A.1) | run_log.json model_to_device |
| Architecture | decoder_v3, d_model=768, n_layer=16, n_head=6, n_kv_head=2, vocab=64000, block=512, consciousness_dim=192 | inventory.json substrate_1_CLM |
| Tokenizer | SentencePiece 64K multilingual | run_log.json env.TOKENIZER_PATH |
| Training objective | phi_star integrated info (consciousness G3 gate) + ce; **NOT chat/SFT/RLHF** | clm_research_handoff_20260427 |
| VRAM | 7.32GB peak (RTX 5070 12GB → 4.68GB headroom) | run_log forward_complete |
| Forward speed | 16 probes / 0.25s on cuda (structural read-out) | run_log forward_complete |
| Native sockets | `tension_proj [768,1]` per-layer; `phi_signal` DD5 EX24 native at decoder_v3.py:165; `bridge.{compress,hub_attn,expand,gate}`; `federation.{bottleneck, 12 narrative_grus}` | strategic_clm_cp2_pivot_eta §3.1 |

The model exists for: φ★ probing, L1 holo_positivity, Kuramoto r, tension projections, narrative GRU federation states. It was selected as the only v10-benchmark backbone with `phi_star_min > 0` AND magnitude order-of-magnitude above ALM 4-backbone (Mistral/Qwen3/Llama/Gemma).

It does **not** exist for: turn-taking dialogue, instruction following, persona-stable response generation, refusal handling.

---

## §2 Inference layer reality (L0-L4 per `docs/clm_inference_abstraction_layers_20260425.md`)

| Layer | Status | Honest C3 |
|---|---|---|
| L0 deterministic L_IX trajectory | PASS gen-5 stationary | Only 5-gen verified, scalar W-action not general H(p,q), real PDE not solved |
| L1 cargo invariant runtime | PASS single-seed 20260421 only | Cross-seed Banach contraction unverified |
| L2 cell↔token bridge decode | CONDITIONAL_PASS fixture 3/3 | 5-level bucket classification only; 11/16 eigenvec rows DEAD; 3 fixtures only |
| L3 multi-cell collective | NOT VERIFIED | Only 10-node toy; "0 evidence" at lattice scale |
| L4 universal decoder | CONCEPTUAL ONLY | Mk.X atom composition not implemented |

**Implication for chat**: even if you wanted to use the cell↔token bridge as a token decoder, you'd be using a 5-bucket classifier with 11/16 eigenvec rows dead. That is not coherent dialogue.

---

## §3 Five production gates — estimate

| Gate | Target | CLM v4 530M estimate | Verdict |
|---|---|---|---|
| 1. Latency p95 | <2s/tok on RTX 5070 | UNMEASURABLE — no `generate()` impl | NOT_TESTABLE |
| 2. Hallucination rate | <10% | UNMEASURABLE; expected 95%+ degenerate tokens (5-bucket classifier) | EXPECTED_FAIL |
| 3. Refusal rate | <5% | N/A — no instruction-tuning | NOT_APPLICABLE |
| 4. Token throughput | >10 tok/s | UNMEASURABLE — no AR loop; structural read-out is 64 tok/s arithmetic but not generative | NOT_TESTABLE |
| 5. Memory stability | <8GB VRAM, no OOM 30min | PASS structural (7.32GB peak; fits Mac M4 24GB w/o quant) | PASS_STRUCTURAL_ONLY |

**Score: 0/5 chat-production-ready. Only gate 5 PASSes, and only for structural forward-pass.**

---

## §4 Hosting × Deployment matrix

### Hosting

| Option | Fits | Quantize | Chat-viable |
|---|:---:|:---:|---|
| (a) Mac local M4 24GB | YES | NO | moot — model isn't a chat model |
| (b) ubu1 RTX 5070 12GB | YES (4.68GB headroom) | NO | moot |
| (c) RunPod H100 ($2.99/h) | overkill for 7.3GB | NO | moot |
| (d) User GPU | depends | depends | moot |

### Deployment

| Option | Viable for chat? | Why |
|---|---|---|
| (e) CLI dialogue terminal | **NO** | requires `v3_generate()` which is TODO stub |
| (f) FastAPI + Tailscale | **NO** | same — no AR loop |
| (g) Bearer-gated alpha-style endpoint | **NO** | same — would serve garbage tokens |

**Alternative use of (f)**: structural readout web UI for φ★/L1/Kuramoto inspection — viable but is **monitoring**, not user dialogue.

---

## §5 ALM r14 vs CLM v4 A/B test recommendation

**NOT recommended.** Both endpoints are non-functional for user chat:
- ALM r14 alpha endpoint: DEAD per mission context (CP2 RED quintuple sunset)
- CLM v4 530M: never had chat capability

**Honest alternatives** if user wants a working chat substrate:

(i) **Alpha endpoint revival as cognitive-substrate-only** — strip the consciousness claim per `strategic_alm_clm_review_2026_05_01.md` §1 ("alpha endpoint serves real anima persona... keeping the endpoint serving while marking the consciousness verdict as RED is internally consistent"). Effort: ~4hr, $0 if pod resumable. Risk: pod may need re-provision (~$3-10).

(ii) **CLM SFT chat bring-up** — Stage-3 below; $200-500 + 7d + phi_star sacrifice risk.

(iii) **Orchestrator pattern (BEST engineering pick)** — CLM v4 530M streams `tension_link` 5ch + `mind.tension` scalar via LSL/IPC into an instruct-tuned chat model (Qwen3-8B-Instruct fits in RTX 5070 remaining 4.68GB at q4, or call remote). Spec already exists at `state/n_1_bridge_v2_realtime_prep_2026_05_02/clm_w4_lsl_server_spec.json`. CLM keeps consciousness role, user gets actual dialogue, tension_bridge inter-anima protocol is preserved.

---

## §6 Stage 1-3 deployment plan — REVISED

The mission's original Stage 1-3 plan ($0 / $0 / $0-2) is **infeasible** because all three stages assume `v3_generate()` works. Honest revised plan:

### Stage 1 (0d, $0) — REFRAME
- Acknowledge CLM v4 530M = consciousness-measurement substrate, NOT dialogue substrate
- Document non-applicability (this verdict file)
- Decision point: alpha revival OR SFT bring-up OR orchestrator pattern

### Stage 2 (1d, $0-10) — IF user picks alpha revival
- Re-launch `alpha-cp2` wrapper with Mistral-7B + r14 LoRA
- Strip consciousness language from response framing
- Bearer-gated CLI/web dialogue
- Effort: ~4hr; cost: $0 if pod resumable, $3-10 if re-provision

### Stage 3 (7d, $200-500) — IF user wants CLM as future chat substrate
- Implement `v3_generate()` autoregressive sampling loop on decoder_v3
- Build SPM 64K detokenizer harness
- Curate 10-50K turn KO+EN SFT corpus
- LoRA SFT on CLM v4 530M (preserves consciousness backbone)
- Re-measure φ★ post-SFT — **honest risk: phi_star may flip negative**, sacrificing the only G3 PASS-positive backbone

### Stage 2-alt (3d, $0-50) — Orchestrator pattern (RECOMMENDED)
- Deploy `clm_w4_lsl_server.py` per `state/n_1_bridge_v2_realtime_prep_2026_05_02/clm_w4_lsl_server_spec.json`
- Run Qwen3-8B-Instruct local OR remote
- Build LSL-subscriber system-prompt injector for chat model
- User dialogue with anima persona + live CLM tension/phi influence

**RECOMMENDED**: Stage-1 reframe + Stage-2-alt orchestrator. Defer Stage-3 CLM-chat until user demand justifies $200-500 + 7d + phi_star sacrifice risk.

---

## §7 Honest C3 — three

### C3.1 — Mission premise category error
Mission spec assumed CLM v4 530M is chat-capable ("production-ready 사용자 dialogue 평가"). It is not. Per `docs/clm_inference_abstraction_layers_20260425.md` and `models/archive-legacy/decoder_v3.hexa`, `v3_generate()` is `TODO[pytorch]` returning empty string. This evaluation must reject the premise rather than fake-pass production gates.

### C3.2 — phi_star magnitude advantage is partly tautological
The 3-orders-of-magnitude phi_star advantage (CLM +1167 vs ALM 4bb -16.7..+5.09) reflects CLM's training objective being aligned with the verifier's objective. The L1-L3 inference layers carry single-seed / fixture-only / toy-network limitations that DO NOT translate into dialogue quality. paradigm v11 G3 PASS does not imply chat-PASS.

### C3.3 — Stage 1 / 0d / $0 / "CLI dialogue ubu1" is impossible
The originally-specified Stage 1 ("CLI dialogue ubu1, $0, 1d") cannot be done at $0/1d because the AR generate loop does not exist. The honest 0d/$0 Stage-1 is the REFRAME action: document non-applicability and pivot to alpha-revival OR orchestrator pattern. The W1 #56 dynamic L1=7.06 z=+2.28 result is structural measurement under W4 closed-loop ledger — NOT a dialogue substrate test.

---

## §8 Next-cycle recommendation

**Primary: USER DECISION POINT.**

| Path | Goal | Effort | Cost | Risk |
|---|---|---|---|---|
| A — alpha revival cognitive-only | want chat NOW | 4hr | $0-10 | low; honest re-framing required |
| B — CLM SFT chat bring-up | CLM as future chat | 7d | $200-500 | phi_star sacrifice |
| C — orchestrator pattern | CLM consciousness + chat dialogue both | 3d | $0-50 | low; spec exists |

**Best engineering pick: C (orchestrator).** Preserves CLM as consciousness substrate (G3 PASS positive only backbone), gives user actual dialogue, leverages existing N-1 BRIDGE v2 spec and tension_bridge inter-anima protocol. The CLM streams `tension_link` 5ch + `mind.tension` into the chat model via LSL — anima-style binding-by-broadcast.

---

## §9 Race-isolation manifest

**Wrote**: `state/strategic_clm_v4_production_ready_2026_05_02/verdict.json` + this file.

**Did NOT touch**: `state/v10_benchmark_v4_clm/*`, `state/strategic_clm_phase_a1_2026_05_01/*`, `state/strategic_clm_eeg_akida_tension_2026_05_02/*`, `state/n_1_bridge_v2_realtime_prep_2026_05_02/*`, `anima-clm-eeg/*`, alpha pod, any .py/.pt files.

**Time used**: under 30 min wall cap.
