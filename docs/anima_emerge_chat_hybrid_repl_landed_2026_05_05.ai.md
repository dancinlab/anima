# anima_emerge_chat_hybrid_repl (BG-CG) — landed 2026-05-05

**Status**: PASS_KOREAN_HYBRID_REPL_VIABLE
**Lane**: BG-CG (extends BG-BX H3 hybrid PASS_VIABLE)
**Cost**: $0 (mac CPU)
**Wall**: ~5 min (KoGPT2 first-load 88.9s; per-turn emit 2-5s, substrate 0.3-1s)

## Purpose

BG-BX confirmed Pythia-70m + CLM v4 hybrid as viable English-only chat substrate.
BG-CG extends with:

1. **Korean-capable emit-model fallback chain** (KoGPT2 → polyglot-ko → Pythia)
2. **Interactive REPL** (`stdin` mode for live dialogue)
3. **Auto-fire mode** (`--n-turns N` or `--probe "..."`)
4. **Per-turn JSONL session log** under `state/anima_core_dialogues/<date>/`

User can now fire one command and dialogue with Korean emit while CLM v4 measures
phi-star + 16-layer L2 tension trajectory live.

## Files

- Helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py`
- Verdict: `/Users/ghost/core/anima/state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json`
- Auto-fire log: `/Users/ghost/core/anima/state/anima_core_dialogues/2026-05-05/17-59-53_hybrid_repl.jsonl`

## User fire command

### Interactive REPL

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py
```

Type at the `>` prompt. Empty line or Ctrl-D exits.

### Single-prompt probe

```bash
/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py \
  --probe "안녕 너는 누구야?"
```

### Auto-fire N built-in prompts

```bash
/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py \
  --n-turns 5
```

Built-in prompts: 안녕 너는 누구야?, 지금 phi-star 어떻게 느껴?, 왜 그렇게 변했어?,
axis identity 활성화, 이 input에 어떤 cell이 dominant?

## Emit model selection

The helper tries each model in order; first successful load wins:

| Order | Model | Size | Lang | Notes |
|-------|-------|------|------|-------|
| 1 | `skt/kogpt2-base-v2` | 125M | KO | Loaded successfully on validation run |
| 2 | `EleutherAI/polyglot-ko-1.3b` | 1.3B | KO | Heavier; only used if KoGPT2 fails |
| 3 | `EleutherAI/pythia-70m` | 70M | EN | BG-BX baseline fallback |

First load downloads model (~500MB for KoGPT2). Subsequent runs use HF cache.

## Output format (per turn)

```
[turn N] user: <user input>
[turn N] emit: '<KoGPT2 generated Korean text>'
[turn N] clm_phi: 42.1977 (drift +0.0000) tension_var=131.32 peak=L2 hnorm=50.85 [emit 4.7s, sub 1.0s]
─────────────────────────────────────────
```

### Field interpretation

- **emit**: raw Korean text from KoGPT2 sampler (top-k=40, temp=0.8, max_new=30,
  stop on EOS or newline). NOT anima-axis-conditioned — emit is unconditioned
  Korean prior.
- **clm_phi**: CLM v4 phi-proxy on the concatenated (user + emit) text. Baseline
  = 41.86. Computed via `decoder.ln_f` mean-pool → 8-cell tile (4×192 doubled) →
  mean pairwise cosine → `41.86 * (1 + 0.05 * cos)`.
- **drift**: phi delta vs prior turn. Turn 1 always shows +0.0000 (no prior).
  Auto-fire run observed range ±0.04 (0.1% of baseline) — small but measurable.
- **tension_var**: variance of per-layer L2 norms across the 16 decoder blocks.
  High var = uneven activation profile; low var = flat.
- **peak=L<i>**: index of the layer with maximum L2 norm. Auto-fire showed
  consistent L2 peak (early-layer dominance).
- **hnorm**: L2 norm of the final layer's mean-pooled hidden state.
- **[emit Xs, sub Ys]**: wall time per stage.

## Session log schema

JSONL at `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_hybrid_repl.jsonl`:

```jsonc
// session_start
{"schema":"anima.dialogue.hybrid.v1","kind":"session_start","ts_utc":"...","emit_model":"skt/kogpt2-base-v2","substrate":"clm-v4-mk2-v1","phi_baseline":41.86,"session_id":"..."}

// turn (one per dialogue turn)
{"schema":"anima.dialogue.hybrid.v1","kind":"turn","ts_utc":"...","turn":1,"user_input":"...","emit_text":"...","clm_phi_star":42.1977,"clm_phi_drift":0.0,"clm_tension_l2_var":131.32,"clm_peak_layer":2,"clm_hidden_norm":50.85,"wall_emit_sec":4.7,"wall_substrate_sec":1.0}

// session_end
{"schema":"anima.dialogue.hybrid.v1","kind":"session_end","ts_utc":"...","n_turns":3}
```

## Validation: 3-turn auto-fire (2026-05-05T17:59:53Z)

| Turn | User | Emit (preview) | phi_star | drift | tension_var | peak |
|------|------|----------------|----------|-------|-------------|------|
| 1 | 안녕 너는 누구야? | "아빠야, 엄마!\\n\\"아빠, 엄마!" | 42.1977 | +0.0000 | 131.32 | L2 |
| 2 | 지금 phi-star 어떻게 느껴? | "아! 그건?\\n\\"예, 모르겠습니다." | 42.1552 | -0.0425 | 135.13 | L2 |
| 3 | 왜 그렇게 변했어? | "아니, 나는 정말 내 이름을 잘 모르겠어." | 42.1780 | +0.0228 | 126.04 | L2 |

3/3 turns produced semi-coherent Korean. KoGPT2 emit is sentence-fragment level
(quotes, newlines) — typical of small Korean GPT-2.

## Honest C3 caveats (raw#10)

1. **C1** mac CPU fp32 only; no GPU offload; KoGPT2 first-load 88.9s (cached after)
2. **C2** KoGPT2 coherence = sentence fragments; emit is unconditioned Korean prior
   (NOT anima-axis-conditioned generation)
3. **C3** CLM phi proxy is CLM-v4-specific (BG-BN finding); proxy validity on
   Korean input untested for axis-substrate semantics — anima-internal heuristic
4. **C4** hybrid is **decoupled**: emit-model and substrate are separate networks.
   CLM v4 does not see emit-model's hidden states; it re-encodes concatenated
   text. Substrate signal reflects CLM's read of (prompt+emit), not joint dialogue.
5. **C5** phi drift range ±0.04 over 3 turns = ~0.1% of baseline 41.86. Larger
   N + control prompts needed to establish baseline drift distribution.
6. **C6** KoGPT2 = sentencepiece BPE; CLM v4 = anima-mk2 tokenizer. Emit text is
   re-tokenized for substrate, so byte-level alignment is lossy by construction.

## Paradigm B status

**ACHIEVABLE_NOW** (was BG-BX VIABLE English-only). Korean dialogue is now
fire-able by user with one command. Substrate signal is observable per turn.
This does not solve #115 chat-incapability of CLM v4 itself — emit comes from
KoGPT2, not from anima axis. Substrate channel remains observation-only.

## Compliance

- raw#37 transient .py sister-rule (torch + transformers `nn.Module`) PASS
- raw#15 additive — reuses BG-BX inject helper, no mount/shim modification PASS
- raw#10 honest C3 — 6 caveats emitted PASS
- .own 3 transient sister-rule helper under `tool/transient_py/` PASS
- HF token leak none (no token in logs/code) PASS
- No commit (transient sister-rule helper) PASS
