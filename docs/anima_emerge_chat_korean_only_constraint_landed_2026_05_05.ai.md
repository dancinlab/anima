# anima_emerge_chat_korean_only_constraint — landed 2026-05-05

## status
- **verdict**: PASS_KOREAN_FORCED (heuristic) / FAIL_SEMANTIC (qualitative)
- **lane**: anima_emerge / chat-cap Korean-only vocab restriction
- **substrate**: need-singularity/clm-v4-mk2-v1, mac CPU fp32
- **cost**: $0
- **runtime**: ~20min
- **output dir**: `state/anima_emerge_chat_korean_only_constraint_2026_05_05/`

## hypothesis under test
Counter-experiment to BG-CO (`ban 0-1000` exposed CJK + Roman-numeral attractor
but kept Korean glyph count = 0). If Korean weight exists at all in this
substrate, restricting softmax support to **Korean-only tokens (5701 ids)** and
sampling among them should surface that weight. If output is coherent Korean
→ substrate has meaningful Korean ranking masked by deeper attractors. If
incoherent → BG-CA "uniform top-1000 Korean" finding holds: no semantic Korean
weight, just glyph-level uniform noise.

## protocol
- vocab restriction: build mask over all 64000 ids where any char in cleaned
  piece is in `'가'..'힣'` Hangul-syllable range → 5701 Korean ids
- pre-argmax: `logits[~mask] = -inf` for every step
- 3 prompts: `안녕`, `안녕하세요. 오늘 날씨가`, `Hello` (EN OOD test)
- 2 decoders per prompt: greedy, top-k=40 sampling (temp=0.7, seed=42)
- 25 new tokens each
- coherence heuristic: `>=5 Korean glyphs AND most-frequent char <= 50% of length`

## results
### Korean-token count by prompt × decoder

| prompt | decode | korean_glyphs (of 25 toks decoded) | qualitative |
|---|---|---|---|
| `안녕` | greedy | 50 | `수행 비로소 수행 수행잔 하이 하이 ...` (`하이` collapse) |
| `안녕` | top-k | 50 | `수행 문자겁 상태 흐 진짜로좌 양측의 예상 화면 ...` (varied) |
| `안녕하세요. 오늘 날씨가` | greedy | 50 | `하이 하이 하이 ...` (full collapse) |
| `안녕하세요. 오늘 날씨가` | top-k | 61 | `하이 난제 상태 새벽에겁꼈다 ...` (varied, no syntax) |
| `Hello` | greedy | 54 | `원인이다 흥미로운 하이 하이 하이 ...` (collapse after 2 toks) |
| `Hello` | top-k | 60 | `수양 동 컴포넌트 해방감이다빈 타임아웃 ...` (varied, no syntax) |

### emitted Korean tokens — observation
Greedy from all 3 prompts **collapses to `하이` (loanword "hi")** within 2-4
steps. Top-k diverges to a stable surface vocabulary: `수행`, `상태`, `자체`,
`인공지능이`, `퍼졌다`, `흥미로운`, `시각을`, `양측의`, `꼈다` (frequent), and
filler glyphs `좌`, `겁`, `깊`, `빈`, `잔`. Token co-occurrence shows no
particle/verb-ending agreement, no clause structure, no topic-comment plausibility.

## findings
1. **Korean weight exists, but is rank-uniform within the Korean subspace**.
   Top-k draws from a wide pool — confirms BG-CA finding that Korean is in the
   substrate ranking (just not in the top-K of the unrestricted vocab) but
   without semantic structure: no morphological agreement, no syntactic
   coherence.
2. **Greedy collapses to `하이`** across all 3 prompts. The Korean argmax is a
   loanword interjection — substrate has selected a low-information attractor
   even within the Korean subset.
3. **EN prompt `Hello` produces same `하이` greedy collapse and same top-k
   surface vocab as Korean prompts** — prompt-conditioning is collapsed in the
   Korean subspace exactly as BG-CO observed in the unrestricted ban. The
   substrate has no language-flexibility coupling between prompt and Korean
   continuation.
4. **Heuristic PASS, semantic FAIL**. The `n_coherent=3` heuristic verdict
   means each prompt produced ≥5 Korean glyphs without single-char monopoly —
   but qualitative inspection shows no plausible Korean utterance. Glyph
   density alone is insufficient.
5. **#115 architectural confirmed from a third angle**. After (a) BG-CA Korean
   ranking uniform across top-1000, (b) BG-CO ban 0-1000 still no Korean,
   now (c) Korean-forced still no semantic Korean — the substrate genuinely
   lacks Korean capability at any level: ranking, attractor competition, AND
   subspace-internal structure. Path A v2 / CLM-2 chat-cap dependency is
   confirmed; CLM v4 = substrate-research only.

## verdict
**PASS_KOREAN_FORCED** by the anima-internal `>=5 glyphs + <50% mono` heuristic
(`n_coherent=3/3`). **Substantively FAIL_KOREAN_INCOHERENT** by qualitative
inspection: greedy `하이` collapse, no syntax, no prompt-language coupling.

The decoupling between (heuristic PASS) and (semantic FAIL) is itself the
finding — confirms #115 chat-incapability is architectural and that Korean
weight is present-but-uniform-without-structure, not absent.

## honest C3 (5)
- **C1**: mac CPU fp32 only — H100 BF16 distribution may differ
- **C2**: forced Korean = vocab subset constraint, NOT semantic recovery; PASS
  here is structural-emission, not language production
- **C3**: substrate may have meaningful Korean ranking that requires more
  sensitive heuristics — current method counts glyphs only, doesn't measure
  morphology / syntax / valid Korean
- **C4**: EN prompt `Hello` with Korean-only emit is OOD; same-attractor
  result validates "no prompt-language coupling" but doesn't prove substrate
  cannot encode Korean given proper conditioning
- **C5**: `coherent` threshold (`>=5 glyphs + <50% mono-char`) is anima-
  internal — all 3 prompts trivially passed despite obvious gibberish

## artifacts
- `tool/transient_py/anima_emerge_chat_korean_only_constraint.py` (script)
- `state/anima_emerge_chat_korean_only_constraint_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_korean_only_constraint_2026_05_05/verdict.json`

## linked landed
- `anima_emerge_chat_korean_rank_survey` (BG-CA, top-30 100% byte, top-1000
  Korean uniform 86 ≈ 8.9% baseline)
- `anima_emerge_chat_byte_0_255_ban` (BG-CO, ban 0-1000 → CJK attractor, Korean 0)
- `clm_v4_lora_sft_chat_lift_falsified_substrate_safe` (#115 architectural)

## constraints respected
- raw#37 transient_py opt-out (script in `tool/transient_py/`)
- raw#15 / raw#10 PASS (no commit, no leak, no concurrent destructive ops)
- HEXA_PY=.venv-eeg/bin/python invocation
- $0 mac CPU only
- no commit
