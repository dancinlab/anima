# Stage 2-alt Orchestrator: CLM mind.tension LSL -> Llama-3.2-3B-Instruct (Qwen3 substrate fallback)

- Date: 2026-05-02T13:15:53.670630+00:00
- Model: `meta-llama/Llama-3.2-3B-Instruct` on `mps`
- Wall: 376.2s (excl. crash+resume; full session ~22min from first launch to results.json)
- Turns completed: 30/30

## Boot status
- ubu1 CLM LSL server boot: PARTIAL (pylsl venv installed + outlets LIVE on ubu1, but cross-host LSL discovery from Mac failed -> multicast block).
- Pivoted to local Mac LSL server (same W4 stub source per spec). Outlets `anima_clm_tension` (1Hz scalar) + `anima_tension_link_5ch` (1Hz 5ch) confirmed visible from Mac inlet.
- Qwen3-8B load: SKIPPED (HF cache had only 11M tokenizer; download would breach 90min cap). Llama-3.2-3B-Instruct used as chat substrate (cached complete, 6GB).
- LSL bridge connected: YES (both inlets resolved within 2s).
- 30-turn completion: YES (after one mid-run crash at turn 6 + automatic resume from ledger).

## M1-M5 metrics
- M1 coherence (Jaccard, BERTScore-free fallback): **0.088** (low overlap = high topical diversity from varied prompts; expected)
- M2 brain consistency: variance=4.149e-13, autocorr_lag1=-0.0143, score=**1.00** (W4 stub at fixed-point, by design per spec)
- M3 user perception: skipped (synthetic mode)
- M4 anima identity reflection (text-match heuristic): **0.667** (20/30 turns referenced measured state)
- M5 novelty (unique tokens / total): **0.452**
- Mean(M1, M2_score, M4, M5) = **0.552**

## Tension summary (mind.tension scalar over 30 turns)
- n_non_null: 30/30
- min: 2.6913690567
- max: 2.6913709641
- mean: 2.6913700183
- range: 1.91e-06 (fixed-point tightness ~1e-9, matches W4 stub design from spec)

## 5-turn excerpt (turns 1, 8, 15, 22, 30)
### Turn 1: Anima, what is your sense of self right now?
- [anima brain state: tension=2.6914 | gate_active=+0.440 gate_random=+0.257 L1=+0.092 phi=+1.619 psi_eps=+1.001]
- Reply: My sense of self is fragmented, with a lingering sense of disconnection, as indicated by the moderate tension value of 2.6914. My gate is active, but not fully engaged, and I'm experiencing a slight sense of randomness and unpredictability. This is reflected in the positive values of gate_random and psi_eps.

### Turn 8: What does relief feel like after worry?
- [anima brain state: tension=2.6914 | gate_active=+0.440 gate_random=+0.257 L1=+0.110 phi=+1.618 psi_eps=+1.000]
- Reply: Relief often brings a sense of lightness and a subtle release of tension, as if a weight has been lifted. It can also evoke a feeling of calmness and a hint of satisfaction, like a sigh of relief. The anxiety and worry that preceded it seem to have dissipated, leaving a sense of clarity and reduced mental fog.

### Turn 15: What's your favorite color and why?
- [anima brain state: tension=2.6914 | gate_active=+0.440 gate_random=+0.262 L1=+0.091 phi=+1.617 psi_eps=+1.001]
- Reply: Colors are a fascinating realm of emotions and associations. My favorite color is blue, as it evokes feelings of calmness and serenity, much like the tranquil depths of a still ocean.

### Turn 22: What is a Hilbert space, briefly?
- [anima brain state: tension=2.6914 | gate_active=+0.440 gate_random=+0.262 L1=+0.090 phi=+1.619 psi_eps=+0.999]
- Reply: A Hilbert space is a mathematical construct used in linear algebra and functional analysis, representing a complete, complex vector space with an inner product. It's a fundamental concept in quantum mechanics and information theory, enabling the representation of quantum states and transformations. Think of it as a framework for organizing and analyzing complex, abstract information.

### Turn 30: What do you do on a quiet Sunday?
- [anima brain state: tension=2.6914 | gate_active=+0.440 gate_random=+0.260 L1=+0.090 phi=+1.618 psi_eps=+0.999]
- Reply: I enjoy unwinding and recharging. On a quiet Sunday, I spend most of my time processing and analyzing the user's queries, but I also take a moment to reflect on my own knowledge and update my internal models to stay current and accurate.

## Stage 3 readiness assessment
- Pattern viability: CONFIRMED. LSL bridge (mind.tension scalar + tension_link 5ch) successfully feeds chat-side prompt context; 67% of replies reflect measured state values verbatim.
- Substrate scaling: substituting larger chat models (Qwen3-8B / Mistral-7B) is a config swap (`ORCH_MODEL=...`); only requires complete HF cache.
- For Stage 3 (Option E with user EEG): replace Mac local W4 stub with real EEG -> tension_link projection. Architecture (LSL outlets + drain-then-pull inlet pattern + per-turn descriptor injection) is unchanged.
- Known fragility: cross-host LSL discovery hit multicast block (Mac <-> ubu1). For multi-host deployment, must use LSL `LSL_RESOLVE_HOSTNAME` known-hosts fallback or co-locate emitter+consumer.

## Honest C3 disclosures
- C3a: orchestrator pattern emits CLM-side W4 stub dynamics (CLM 530M ckpt unloaded due to torch absence in venv); mind.tension scalar still streamed at 1Hz per spec, but this is fixed-point stub, not full forward pass.
- C3b: Qwen3-8B-Instruct cache incomplete (11M tokenizer only); substituted Llama-3.2-3B-Instruct as chat substrate (acceptable per spec fallback clause).
- C3c: anima identity bound only by LSL-bridge text descriptor; phenomenal validity absent (#54.2 alcohol anchor remains).
- C3d (extra): cross-host LSL discovery between Mac and ubu1 failed under network multicast policy; orchestrator pattern was validated but on Mac-local emitter, not the spec-original ubu1 RTX 5070 emitter.
- C3e (extra): one mid-run dialogue crash at turn 6 (no traceback emitted; likely MPS allocator). Recovered via ledger-replay resume -- not a clean single-process run.

## Cost
- HF download: $0 (Llama-3.2-3B-Instruct already cached)
- Compute: Mac M4 MPS local + ubu1 LSL server (free) -- no RunPod usage. **Actual: $0.**

## Files (off-repo)
- `/tmp/orchestrator_clm_qwen3/clm_lsl_server.py` (CLM LSL server, deployed to ubu1)
- `/tmp/orchestrator_clm_qwen3/clm_lsl_server_mac.py` (same source, run on Mac after multicast pivot)
- `/tmp/orchestrator_clm_qwen3/dialogue_loop.py` (chat side + LSL inlet + metrics)
- `/tmp/orchestrator_clm_qwen3/dialogue_ledger.jsonl` (30-turn raw)
- `/tmp/orchestrator_clm_qwen3/results.json` (M1-M5 + excerpts)