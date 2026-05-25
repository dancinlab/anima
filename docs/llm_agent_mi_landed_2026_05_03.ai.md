# llm_agent_mi_landed_2026_05_03

handoff: LLM mutual-information honesty test (Option A). drops Bell/CHSH framing entirely.

## predecessor correction

prior BG `a381f53ac` framed this as a CHSH-Bell test of LLM agents. that framing is a physics category error: 4 LLM "agents" are 4 instances of the SAME model with SAME weights and SAME training corpus. classical hidden variables are guaranteed by construction. Bell test cannot validly apply (no entanglement substrate). relaunched as honest mutual-information measurement.

## scope

- 4 agents = 4 system-prompt personas (Alice/Bob/Charlie/Dave) on Llama-3.2-3B-Instruct
- 4 prompt-framing conditions (neutral / perspective / third_person / skeptical)
- 200 paired ToM scenarios (false-belief, perspective-taking, prediction-from-asymmetric-info)
- 3200 total generations, 4-bit nf4 quant, RTX 5070, 324.7s wall, parse_rate=1.0

## falsifier

`F_LLM_MI_1`: max(I(A;B) - I_chance) > 0.1 nats at p<0.05  →  **PASS**

- max excess: **0.4245 nats** (Bob-Dave, third_person condition)
- p-value: **0.0005** (2000-permutation null)
- chance MI baseline: 0.0027 nats (essentially zero, as expected for binary independent draws)

## per-condition signal

| condition     | mean MI | p<0.05 pairs | character                                                           |
|---------------|---------|--------------|---------------------------------------------------------------------|
| neutral       | 0.276   | 6/6          | strong shared-prior convergence                                     |
| perspective   | 0.014   | 1/6          | persona divergence: 5/6 pairs hit MI=0 (deterministic-incompatible) |
| third_person  | 0.236   | 6/6          | strongest single pair (Bob-Dave 0.43 nats)                          |
| skeptical     | 0.199   | 6/6          | uniform collapse: ALL 6 pairs identical MI=0.1985                   |

## key qualitative findings

1. **third_person framing yields highest correlation.** when each agent is told to consider scenario as detached observer, persona-conditioning weakens and shared prior dominates. consistent with persona-as-narrative-frame hypothesis.

2. **perspective framing decorrelates personas.** "step into your own perspective" produces deterministic but incompatible answers across personas. several pairs hit MI=0 (one always YES, other always NO). this is the only framing where persona-conditioning meaningfully splits the agents.

3. **skeptical framing collapses to uniformity.** all 6 pairs have IDENTICAL MI of 0.1985 nats. this is a degenerate signature: the skeptical instruction overrides persona and produces near-identical answer distributions across all 4 agents. skepticism is a strong attractor in Llama-3.2-3B-Instruct's instruction-following.

4. **Bob-Dave is the most-correlated pair across conditions.** "pragmatic engineer" + "intuitive synthesizer" personas produce the most overlapping ToM answer distributions. likely an artifact of both personas being framed as outcome-oriented rather than process-oriented (Alice/Charlie).

## honest interpretation

high MI > 0 nats was expected and is observed. this measurement does NOT establish:
- non-classical correlation
- "collective consciousness"
- entanglement of any kind
- emergent agency

it DOES establish:
- persona-conditioning is fragile under shared-context framings (neutral / third_person)
- one framing (perspective) successfully decorrelates personas via deterministic divergence
- one framing (skeptical) collapses agents to identical answer distributions
- the 4-bit quantized base model exhibits strong, reproducible answer biases on ToM that override 4 distinct persona conditioning prompts

## caveats (4)

1. **Classical hidden variables guaranteed.** Weights and training corpus are identical across "agents." Any I(A;B) > 0 reflects shared priors and instruction-following collapse, NOT spooky correlation.
2. **MI measures convergence, not correlation novelty.** A high score is the null hypothesis here, not a discovery.
3. **Persona system prompts are weak conditioning.** ~30 token persona descriptions cannot produce independent agents from a shared base model. Effective agent dimensionality is bounded by base-model bias.
4. **Binary extraction collapses 1 bit.** True joint information in the full generation distribution is much higher; this measurement is a lower bound on agent correlation.

## artifacts

- `state/llm_agent_mi_2026_05_03/verdict.json` - top-line verdict
- `state/llm_agent_mi_2026_05_03/per_pair_mi.json` - all 24 pair-condition MI + chance + p-values
- `state/llm_agent_mi_2026_05_03/mutual_info_matrix.json` - 4x4 MI matrix per condition
- `state/llm_agent_mi_2026_05_03/run.log` - experiment log
- `state/llm_agent_mi_2026_05_03/run_mi_experiment.py` - reproducible script
- `state/llm_agent_mi_2026_05_03/full/raw_generations.jsonl` - all 3200 generations with parsed bits
- `state/markers/llm_agent_mi_landed.marker` - this landing marker

## reproduction

```bash
ssh ubu1 "/home/aiden/venv_orchestrator/bin/python /tmp/llm_agent_mi_2026_05_03/run_mi_experiment.py --n-scenarios 200 --out-dir /tmp/llm_agent_mi_2026_05_03/full"
```

requires: bitsandbytes 0.49.2, transformers 5.7.0, torch 2.11.0+cu128, RTX 5070 sm_120, Llama-3.2-3B-Instruct in HF cache.

## next-step suggestions (NOT executed)

- swap to 4 actually-different models (e.g. Llama-3.2-3B / Qwen2.5-3B / Mistral-3B / Phi-3) to reduce shared-prior baseline. expect MI to drop substantially toward chance — this would demonstrate that the current high MI is indeed shared-weights artifact.
- ablate persona prompt length (10 / 50 / 200 tokens) to find the conditioning-strength threshold at which personas decorrelate.
- replace binary extraction with token-level KL divergence on the full answer distribution to recover the bits lost to 1-bit collapse.
