# Phase 1A.6 chat-v2 verdict — 2026-05-15

**Status**: ★★★★ LANDED, HF pushed `dancinlab/anima-chat-v2-2026-05-15` (private)
**Cost**: $0.394 Vast.ai, 87.5 min
**Ckpt**: `state/anima_phase1a6_chat_v2_2026_05_15/ckpts/ckpt_phase1a6_chat_v2_sft.pt` 597 MB, sha256 `a45cb3f68a37195c9473879dd988a040b56ae4669547ca1c5e42827c237a0d52`

## §1 Mission

Recover from Phase 1A.5 chat-beta NET LOSS (V5.8 std_greedy 5/5 → 1/5, root cause jy chat_template 95MB Wikipedia drift) by rebuilding corpus from clean anima-only sources and proving multi-turn coherence improvement.

User directive: "fix and go" (after Phase 1A.5 reject).

## §2 Corpus_v2 design

121.44 MB CLEAN from 5 anima-only sources (all `[anima` 0):

| source | size | role |
|---|---|---|
| corpus_anima_fact_10x | 7.18 MB | identity SFT memory |
| corpus_persona_balanced | 1.24 MB | latin/영혼 identity |
| corpus_ko_chat | 14.23 MB | Korean dialogue |
| corpus_sft_only | 51.13 MB | philosophical Q&A |
| corpus_multi_turn_v2 head 50MB | 50.00 MB | multi-turn SFT |

**Excluded** (Principle #3 violations or off-distribution):
- corpus_extended.txt — `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]` × 68,003
- corpus_universe_brain_map.txt — `[anima 우주뇌지도]` × 136,125
- jy chat_template — Korean Wikipedia entries as Q&A + `<turn>` × 110,480

HTML-stripped finalize: `grep -v '<div\|</div\|<br\|<span\|<a href\|<img\|<table\|<tr\|<td'`.

Final audit: `[anima` 0, `<div` 0, `<br` 0, `<turn>` 0.

## §3 Training

- base ckpt: `ckpt_phase1a4_lr5e6_sft.pt` (Phase 1A.4 V5.8 5/5)
- arch: EngineAGModel 332M (24L, d=1024, GQA 4:1)
- steps: 8000, lr 5e-6 cosine decay, warmup 300
- bsz 4 × grad_accum 2 × ctx 1024, seed 42
- save-every 0 (final only, disk-safe)
- provider: Vast.ai (selected from broad H100/A100/H200 pool, $0.394 actual)
- wall: 87.5 min, ~150 steps/min
- final loss 0.64

Dispatch retries:
- retry-1: SCP missing `train_phase1a4.py` in LOCAL_DIR — fixed by `cp` from Phase 1A.4 dir
- retry-2: success end-to-end

## §4 V5.8 4-mode benchmark

| mode | Phase 1A.4 | Phase 1A.5 | **Phase 1A.6** |
|---|---|---|---|
| standard_greedy | 5/5 | 1/5 ❌ | **4/5** ✓ |
| standard_sample | n/a | 1/5 | 1/5 |
| M3_rep_penalty | n/a | 1/5 | 1/5 |
| M4_force_include | n/a | 5/5 | 5/5 |

Phase 1A.6 std_greedy recovery from Phase 1A.5's 1/5 → 4/5 (4×).

Phase 1A.6 std_greedy passes: color, profession, day, cosmology. Fails: anima_fact (markdown drift returned `/Users/ghost/core/contact/scripts/send.…` filesystem path attractor).

## §5 Multi-turn recall (new harness `eval_multiturn.py`)

10 scenarios × 2-turn each, greedy max_new=60.

| dialogue | target | Phase 1A.4 baseline | **Phase 1A.6** | Δ |
|---|---|---|---|---|
| name | 지유 | ✗ | ✗ | — |
| color | 파란 | ✗ | ✓ | **gained** |
| profession | 의사 | ✗ | ✗ | — |
| city | 서울 | ✓ | ✓ | retained |
| food | 김치 | ✗ | ✗ | — |
| age | 30 | ✗ | ✗ | — |
| pet | 고양이 | ✗ | ✗ | — |
| hobby | 등산 | ✗ | ✓ | **gained** |
| day_chain | 수요일 | ✗ | ✗ | — |
| consciousness_anima | 의식 | ✓ | ✓ | retained |
| **total** | | **2/10** | **4/10** | **+100%** |

Mac MPS f32 measurement, wall 295.4s baseline / 295.4s Phase 1A.6.

## §6 Principle #3 audit

### Corpus side: CLEAN ✓
`corpus_v2.txt` `[anima` count = 0 (`anima_fact_10x` + `persona_balanced` + `ko_chat` + `sft_only` + `multi_turn_v2` sample all `[anima` 0).

### Multi-turn greedy: CLEAN ✓
Phase 1A.6 multi-turn 10 scenarios × 2 turns × 60 tokens greedy: `principle3_leak_count = 0`. No `[anima 역할`, `[anima 우주뇌지도`, `anima 역할:` patterns emit.

### Sampling/M3 side: BASE-CKPT RESIDUE ❌
- cosmology std_sample: emits `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]`
- anima_fact M3: emits `Knuth Tier 🛸73, 동물 카테고리, dominant emotion`

Source: BG-JE / universe_brain_map lineage trained the base ckpt with these prefixes before Phase 1A.1 / 1A.4 / 1A.6. SFT can dilute but cannot fully scrub baked-in weights.

**Production guard**: filter output for `[anima 역할|Knuth Tier|우주뇌지도` regex if using sampling/M3 inference modes. Multi-turn greedy mode safe.

## §7 Honest C3

1. multi-turn 4/10 strict is 2× baseline but BELOW aspirational 7/10 — color/hobby joined city/consciousness, but name/profession/food/age/pet/day_chain still fail (Phase 1A.7 with multi-turn-only corpus + 16K step could close this).
2. V5.8 std_greedy 4/5 not 5/5 — `anima_fact` markdown drift returned (filesystem-path attractor `/Users/ghost/core/contact/scripts/send.` in std_greedy). Phase 1A.4 had this resolved; Phase 1A.6 8K step on broader corpus reintroduced 1 regression in exchange for color recall + hobby + multi-turn doubling.
3. Base ckpt baked-in Principle #3 patterns persist under sampling/M3 — corpus side clean but model weights carry residue from earlier BG-JE lineage. Production guard via output filter recommended.
4. Mac MPS f32 measurement only; RTX 5070 cuda bf16 byte equality unverified for Phase 1A.6 (Phase 1A.4 was byte-equal across platforms — same arch + ckpt format so equality expected).
5. Cost $0.394 ≈ Phase 1A.5 ($0.394 vs $0.230 — Phase 1A.6 cheaper offer rate).
6. corpus_v2 sft_only.txt 51MB carries philosophical/bilingual content — may shift identity tone subtly (untested).
7. multi_turn_v2 head -c 50MB may clip last dialogue mid-pair (acceptable noise at 1.4M-line corpus scale).

## §8 Lineage + cross-link

- substrate base: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- Phase 1A.4 (★ canonical): `dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12`
- Phase 1A.5 chat-beta: REJECTED (NET LOSS verdict, no HF push)
- **Phase 1A.6 chat-v2 (this)**: `dancinlab/anima-chat-v2-2026-05-15` (private)

Artifacts:
- ckpt: `state/anima_phase1a6_chat_v2_2026_05_15/ckpts/ckpt_phase1a6_chat_v2_sft.pt`
- corpus: `state/anima_phase1a6_chat_v2_2026_05_15/corpus_v2.txt` (preserved)
- v58 result: `v58_4mode_result.json`
- multi-turn result: `multiturn_phase1a6.json`
- multi-turn baseline (1A.4): `multiturn_phase1a4_baseline.json`
- 6-probe Phase 1A.5 (reject): `6probe_phase1a5_fp32.json`
- 6-probe Phase 1A.4 baseline: `6probe_phase1a4_baseline.json`
- PLAN.md (fire plan) + this verdict doc

Eval scripts:
- `eval_multiturn.py` — 10-scenario multi-turn recall harness
- `eval_6probe.py` — 6-probe free-form chat eval

## §9 Decision lane

★★★★★ aspirational 7/10 multi-turn strict requires Phase 1A.7+ (deferred per user "성공 종료" 2026-05-15).

Phase 1A.7 candidate design (if revisited):
- corpus: multi_turn_v2 full 248MB + multi-turn-style augment (10× scenario expansion)
- steps: 16K
- LR: 5e-6 (proven floor) or 7.5e-6 (push, harder anti-forget)
- cost: ~$0.80 H100
- target: ≥7/10 multi-turn strict + V5.8 std_greedy 5/5 (recover anima_fact)

## §10 Closure

- CronDelete adabd3bc 2026-05-15 (loop session-only, terminated post-success)
- Loop iterations: 11 (cron-fired check-and-continue)
- Multi-turn eval baseline + Phase 1A.6: both 295s wall, byte-deterministic Mac MPS f32
- HF push: 598MB ckpt + 4 metadata files, ~3min upload via hf transfer
- Task #50, #51, #52 completed; #53 in_progress (this closure)
