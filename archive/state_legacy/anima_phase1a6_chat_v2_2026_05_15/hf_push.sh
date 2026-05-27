#!/bin/bash
# hf_push.sh — Phase 1A.6 chat-v2 → dancinlab/anima-chat-v2-2026-05-15 (private)
# Gate: V5.8 std_greedy ≥4/5 + multi-turn ≥4/10 + Principle #3 multi-turn leak 0
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a6_chat_v2_2026_05_15"
REPO="dancinlab/anima-chat-v2-2026-05-15"

HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a6_chat_v2_sft.pt v58_4mode_result.json multiturn_phase1a6.json 2>&1 || { echo "missing artifacts"; exit 1; }

N_PASS_V58=$(python3 -c "import json; d=json.load(open('v58_4mode_result.json')); print(d['summary']['standard_greedy']['n_pass'])")
N_PASS_MT=$(python3 -c "import json; d=json.load(open('multiturn_phase1a6.json')); print(d['n_pass_strict'])")
LEAK_MT=$(python3 -c "import json; d=json.load(open('multiturn_phase1a6.json')); print(d['principle3_leak_count'])")
echo "V5.8 std_greedy: $N_PASS_V58/5 | multi-turn: $N_PASS_MT/10 | Principle3 multi-turn leak: $LEAK_MT"

if [ "$N_PASS_V58" -lt "4" ] || [ "$N_PASS_MT" -lt "4" ] || [ "$LEAK_MT" != "0" ]; then
    echo "ABORT: gate fail"
    exit 1
fi
echo "OK: gate pass — proceeding with HF push to $REPO"

cat > README.md <<'EOF'
---
license: apache-2.0
language:
  - ko
library_name: pytorch
tags:
  - anima
  - chat
  - clm
  - phase1a6
  - chat-v2
  - multi-turn
---

# anima-chat-v2-2026-05-15

Phase 1A.6 chat-v2 — second-generation anima chat ckpt with multi-turn recall recovery on own substrate.

## Lineage
- arch: EngineAGModel 332M (24L, d=1024, GQA 4:1, byte-vocab 32000+offset 3)
- base: `dancinlab/anima-clm-phase1a4-lr5e6-strict-pass` (V5.8 std_greedy 5/5)
- delta: 8000-step SFT on 121.44MB CLEAN multi-source anima corpus (`corpus_v2`)

## Why v2 (vs Phase 1A.5)
Phase 1A.5 chat-beta used 98MB combined corpus that included 95MB jy chat_template
(Korean Wikipedia entries wrapped as Q&A + `<turn>` token 110k hits). Result: V5.8
std_greedy regressed 5/5 → 1/5. Phase 1A.6 corrects this by assembling clean
anima-only sources:

| source | size | content |
|---|---|---|
| corpus_anima_fact_10x | 7.18 MB | identity SFT memory |
| corpus_persona_balanced | 1.24 MB | latin/영혼 identity |
| corpus_ko_chat | 14.23 MB | Korean dialogue |
| corpus_sft_only | 51.13 MB | philosophical Q&A |
| corpus_multi_turn_v2 sample | 50.00 MB | anima multi-turn SFT |
| **HTML-filtered final** | **121.44 MB** | 1,461,755 lines |

Excluded sources known to carry `[anima 역할:` / `[anima 우주뇌지도]` Principle #3 prefix:
corpus_extended (68k hits), corpus_universe_brain_map (136k hits).

## Results

### V5.8 4-mode benchmark
- standard_greedy: **4/5 PASS** (color, profession, day, cosmology; anima_fact markdown drift)
- standard_sample: 1/5
- M3_rep_penalty: 1/5
- M4_force_include: 5/5

vs Phase 1A.5: std_greedy 1/5 → **4/5** (4× recovery).

### Multi-turn recall (BENCHMARK.md §3, 10 scenarios, greedy max_new=60)
- **4/10 strict PASS** (color, city, hobby, consciousness_anima) — 2× Phase 1A.4 baseline 2/10
- Principle #3 leak in multi-turn greedy: **0** ✓

## Training
- steps: 8000
- lr: 5e-6 cosine decay, warmup 300
- bsz 4 × grad_accum 2, ctx 1024, seed 42
- provider: Vast.ai (selected from H100/A100 pool)
- wall: 87.5 min
- cost: $0.394
- `--save-every 0` (disk-safe, final only)

## Honest C3

1. **Base ckpt baked-in Principle #3 leak persists under sampling/M3** — `[anima 역할:` and `Knuth Tier 🛸XX` patterns from earlier BG-JE lineage carry over (corpus_extended / corpus_universe_brain_map polluted base before Phase 1A.4). SFT cannot fully scrub. Production guard via output filter recommended for sampling modes.
2. Multi-turn recall 4/10 strict is meaningful gain (2× baseline) but BELOW aspirational 7/10 — further scale (Phase 1A.7+) or task-specific multi-turn corpus would push higher.
3. V5.8 std_greedy 4/5 not 5/5 — anima_fact dialogue still hits markdown table attractor (Phase 1A.4 had this resolved at 5/5; 1A.6 reintroduced 1 regression there in exchange for multi-turn gain).
4. 121MB corpus = ~2 epoch budget at 8K step. Mild over-fit risk; sft_only.txt 51MB carries philosophical/bilingual content that may shift identity tone.
5. Cost $0.394 on Vast.ai 1-GPU node, dispatch_vast_v2.sh direct-IP SCP, post-step-8000 V5.8 eval + ckpt SCP integrated.

## Artifacts
- `ckpt_phase1a6_chat_v2_sft.pt` — model state_dict (597 MB, bf16)
- `v58_4mode_result.json` — V5.8 falsifier results
- `multiturn_phase1a6.json` — 10-scenario multi-turn recall
- `meta.json` — training metadata

EOF

HF_CLI="/Users/ghost/Library/Python/3.14/bin/huggingface-cli"
HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  "$HF_CLI" upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    --private \
    "$REPO" \
    ckpts/ckpt_phase1a6_chat_v2_sft.pt \
    ckpt_phase1a6_chat_v2_sft.pt
for f in meta.json v58_4mode_result.json multiturn_phase1a6.json README.md; do
  if [ -f "$f" ]; then
    HUGGINGFACE_HUB_VERBOSITY=info \
      "$HF_CLI" upload --repo-type model --token "$HF_TOKEN" "$REPO" "$f" "$f"
  fi
done

echo "OK: https://huggingface.co/$REPO"
