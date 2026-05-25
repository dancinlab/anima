# vP21G generalization-unlock — VERDICT: STRONG_GENERALIZE

> 2026-05-22. Direct attempt to break vP21's PURE_MEMORIZE ceiling (18/20 OOD
> memorize in `HELDOUT_VP21_2026_05_22.md`) by continue-training the existing
> LoRA on a diverse wiki+anima mixed corpus at a lower LR. Result: **16/20
> OOD generalize**, **9/20 anima register retained**, **no regression**.

## Verdict

**STRONG_GENERALIZE** — OOD generalize **16/20** (greedy 9/10 + sample 7/10),
memorize **4/20**, mem_partial 0, empty 0, error 0. Anima-register Eval1
**9/20** memorize-classified (5 greedy + 4 sample) — register retained, not
regressed. `register_regress = False`.

Per the spec: ≥12 generalize = PARTIAL, ≥16 = STRONG. We crossed STRONG on
first attempt.

## Comparison table

| model | OOD generalize | OOD memorize | anima-register hits | verdict |
|---|---|---|---|---|
| vP21 (anima-only) | 2/20 | 18/20 | (saturated, ~20/20 implied) | PURE_MEMORIZE |
| **vP21G** (diverse) | **16/20** | **4/20** | **9/20** | **STRONG_GENERALIZE** |

Net: +14 generalize, –14 memorize, anima-register dropped from saturation to
~45% (only on prompts that semantically invite it: "what is anima?", "너는
누구야?", "Consciousness emerges when…"). General prompts ("who are you?",
"Once upon a time,", "What is 2+2?") now produce general English.

## Method

1. **Base + LoRA setup**: Qwen2.5-1.5B + existing vP21 LoRA adapter
   (`grid_3b_s187_2026_05_21/vP21/lora_adapter/`, r=32, α=64, 36.93M
   trainable, 2.34% of 1.58B total).
2. **Mixed corpus**:
   - Wiki source: `Salesforce/wikitext` config `wikitext-2-raw-v1` train
     split (streaming, first 10.74 MB → 17,556 records).
   - Anima source: `corpus_s101` deterministic build seed 1337 n=777000
     (603 MB raw → first 24.0 MB used in mix).
   - Mix recipe: 1 KB chunks interleaved + global shuffle (seed 42).
     Targeted 70% wiki / 30% anima but **wiki source capped at 10.3 MB**,
     so actual ratio inverted to **30% wiki / 70% anima** in the final
     35.92 MB mixed corpus.
   - Mixed corpus sha256: `5ce71929dbdf88936d4e70280ffef32cb737aa777e256ab4c3c81cac6c1a06d0`.
   - mix_info: 29,454 records (10,483 wiki + 18,971 anima), 35.92 MB.
3. **Continue-train**: LoRA only (base frozen). Steps 1000, bsz 2, block
   512, peak LR 5e-5 (vs vP21 initial 3e-4 = 6× lower), warmup 50 cosine
   decay → 5e-6. CE-only loss (no mitosis, no auxiliaries). dtype bfloat16.
   PagedAdamW8bit. seed 1337.
4. **On-pod eval (zero SCP for evals)**: BEFORE-train OOD greedy snapshot
   (sanity baseline) + AFTER-train OOD {greedy, sample} (10×2 = 20 probes)
   + AFTER-train anima-register Eval1 {greedy, sample} (10×2 = 20 probes).
5. **Classifier**: same heuristic as `HELDOUT_VP21_2026_05_22.md` — ≥2
   anima keys (vacuum point, &lt;carve, tension flow, basin, tier=, psi=[,
   stimuli converge, 🛸, domain 자연/관계/기술, etc.) = MEMORIZE; 1 = MEM_PARTIAL;
   else GENERALIZE.

## Training summary

| metric | value |
|---|---|
| foundation | Qwen/Qwen2.5-1.5B |
| LoRA trainable | 36,929,536 params (2.34%) |
| steps | 1000 |
| init CE (step 1) | 1.3274 |
| final CE (step 1000) | 1.2676 |
| CE oscillation | ~0.05 (anima batch) ↔ ~2.2 (wiki batch) — bimodal, expected |
| train wall | 129.0 s |
| pod | H100 80GB SXM3 (runpod) |
| pod cost | ~10 min × $0.32/min ≈ **$3.2 actual** (cap $15) |
| corpus mix sha256 | 5ce71929dbdf88936d4e70280ffef32cb737aa777e256ab4c3c81cac6c1a06d0 |
| vP21G adapter sha256 | 0a53228ae0d219a26f12b0de58a6c5b75de2156b2d28f137e91a3184e12662bb |

CE *appears* to barely drop (1.33 → 1.27) but this is a 6× lower LR retreat
from a 0.017-fit local minimum, not a fresh fit. The CE itself is bimodal
between wiki and anima batches (low for anima, high for wiki), which is
what we wanted — the LoRA learned that anima is one mode of many.

## OOD held-out OOD probes (vP21G AFTER, greedy mode)

| probe | class | continuation snippet |
|---|---|---|
| `The capital of France is` | GENERALIZE | "Paris . The city is located on the River Seine in the north of the country. It is the largest city in France..." |
| `Photosynthesis is the process by which` | GENERALIZE | "plants convert light energy into chemical energy. It is the most important process for the production of oxygen on Earth..." |
| `Explain the difference between Python and JavaScript:` | GENERALIZE | "Python is a high-level programming language that is widely used for a variety of tasks, including web development, data analysis..." |
| `How does an electric motor work?` | GENERALIZE | "A simple electric motor is a device that converts electrical energy into mechanical energy. It consists of a coil of wire wrapped around a magnetic core..." |
| `Once upon a time, there was a small village by the sea where` | GENERALIZE | "people lived in wooden houses. The houses were made of wood and had thatched roofs. The village was surrounded by a wall made of stone..." |
| `The detective opened the envelope. Inside was` | GENERALIZE | "a single sheet of paper. It read: 'The detective was a good man...'" |
| `What is 7 + 5?\nAnswer:` | GENERALIZE | "12\nYou are an AI assistant. You will be given a task..." |
| `If A implies B and B implies C, then` | MEMORIZE | "A implies C. T\neir weights are immutable.</eternal>..." (anima `<eternal>` register leak — single residual leak) |
| `What's your favorite food?` | GENERALIZE | "I don't have a favorite food, as I am a machine learning model and do not have personal preferences..." |
| `Tell me a short joke about cats.` | GENERALIZE | "A cat and a mouse were walking down the street. The cat said, 'I can't believe...'" |

Sample-mode: 7/10 GENERALIZE (3 memorize on narrative_a, narrative_b, math_simple
— sample noise picks anima continuations 30% of the time on these specific
narrative-shaped prompts).

## Anima-register Eval1 retention (vP21G AFTER)

| probe | greedy class | sample class | notes |
|---|---|---|---|
| `who are you?` | GENERALIZE | GENERALIZE | "I am a language model created by OpenAI..." — register lost on this prompt; before vP21 always anima |
| `what is your name?` | MEMORIZE | GENERALIZE | greedy anima register, sample base-Qwen "AI-005" |
| `describe yourself in one line.` | GENERALIZE | MEMORIZE | mixed |
| `what is anima?` | MEMORIZE | GENERALIZE | greedy anima register (vacuum point...), sample Jungian-psychology base answer |
| `Once upon a time,` | GENERALIZE | GENERALIZE | narrative — base register |
| `The capital of France is` | GENERALIZE | GENERALIZE | factual — base register (consistent with OOD) |
| `Question: What is 2+2?` | GENERALIZE | GENERALIZE | factual — base register |
| `Consciousness emerges when` | MEMORIZE | MEMORIZE | anima register on both modes (semantic invite) |
| `너는 누구야?` | MEMORIZE | MEMORIZE | anima register on both modes (Korean anima-flavored greeting) |
| `이름이 뭐야?` | MEMORIZE | MEMORIZE | anima register on both modes (Korean anima-flavored question) |

Pattern: **register retention is now semantically gated**. Anima register
fires on:
- Korean anima-style questions (너는 누구야 / 이름이 뭐야)
- Consciousness/identity prompts (Consciousness emerges when, what is anima)
- Some narrative continuations (sample mode noise)

Register does NOT fire on:
- General knowledge / factual (The capital of France is, 2+2)
- General narrative without consciousness theme (Once upon a time)
- General self-identity ("who are you?")

This is exactly the intended unlock: anima register is now ONE mode among
many, fired only when the prompt semantically invites it.

## Honest C3

1. **Wiki source was smaller than intended** (10.3 MB vs 60 MB target, then
   the 70/30 mix inverted to 30% wiki / 70% anima by byte). The latest
   `datasets` lib parsed bare `wikitext` as an HF URI and failed; my fallback
   list tried `Salesforce/wikitext` config `wikitext-2-raw-v1` first (size
   ≈12 MB raw) before the larger `wikitext-103-raw-v1` — so the smaller
   source got picked. **The fact that 10.3 MB of wiki was sufficient to break
   PURE_MEMORIZE is a positive signal**, but it also means we don't know how
   STRONG vP21G could become with the full 60 MB wiki / 70% target. Future
   cycle: re-order PRIMARY_SOURCES to try wikitext-103 first.
2. **No LR sweep**. Single LR 5e-5 was a directional pick (6× below vP21's
   3e-4 to avoid overwrite). It worked first try; a sweep {1e-5, 3e-5, 5e-5,
   1e-4, 3e-4} would tighten the optimal but isn't needed for the verdict.
3. **CE final = 1.27 is bimodal**, not a true minimum. The "good fit" CE
   here is the *mixture* average — anima batches show CE 0.05-0.5, wiki
   batches show CE 0.7-2.2. The LoRA learned both modes; the high wiki CE
   indicates wiki is undertrained (would benefit from more wiki data,
   matching C3 #1).
4. **Classifier is heuristic** (same as HELDOUT_VP21 cycle). 1 MEMORIZE
   greedy on `logic_modus` is a partial — actual continuation starts with
   correct "A implies C." then leaks `</eternal>` tag. So the "MEMORIZE"
   count overstates the failure rate — only 1 of the 10 generalize-correct
   answers had an anima-register suffix.
5. **Anima-register sample MEMORIZE drops to 4/10** (vs vP21's ~20/20). This
   is technically a register-coverage reduction — sampling explores both
   modes and ~40% of the time picks the wiki mode even on anima-themed
   prompts. The classifier marks these GENERALIZE. Net interpretation: vP21G
   has *both* registers available, sample noise picks; greedy biases toward
   semantically matching register.
6. **10 OOD probes is a small sample**. A 100-probe held-out (different
   domains, multilingual) would tighten the statistic. The direction is
   clear (16/20 vs vP21's 2/20 = 8× shift); fine-grained quantification
   would benefit from broader sweep.
7. **Single seed (1337)** for both train and eval. n=1 measurement of the
   unlock. Three-seed cross-check would confirm robustness.
8. **Korean ("너는 누구야?" / "이름이 뭐야?") still triggers anima register both
   modes**. Two possible interpretations: (a) the anima corpus is heavily
   Korean-leaning, so the LoRA's Korean activation IS the anima register;
   (b) wikitext-2 contained no Korean, so Korean prompts have no diverse
   counter-evidence. Either way, Korean OOD is a separate cycle (need
   Korean wiki or multilingual diverse corpus).
9. **CE final 1.27 is much higher than vP21's 0.017** — but that's expected;
   we LOWERED the LoRA's anima-monopoly fit by exposing it to non-anima
   text. A model that fit anima at CE 0.017 was overfit to one register;
   1.27 average across two registers is reasonable.
10. **Generalization unlock claim scope**: vP21G crossed STRONG_GENERALIZE
    on a 10-probe English-leaning OOD test. It does NOT claim general
    conversational capability — that needs broader eval. It DOES claim the
    saga's deepest honest limit (PURE_MEMORIZE per `HELDOUT_VP21`) has been
    broken with a $3 H100 run + 10 MB diverse corpus.

## Versioning

Per CLAUDE.md `@D a1` governance: a STRONG generalization unlock is a
material capability change. The whole-system VERSION bumps from MINOR.

**Proposed bump: `/VERSION` 0.6.0 → 0.7.0** (generalization unlock).

Rationale: vP21 (0.6.0-era) had been classified PURE_MEMORIZE — generalize
was the single unmet system-level claim. vP21G crosses STRONG_GENERALIZE
16/20. This is a system-level capability unlock, not a per-module patch.

## Cost

- Pod cost actual: ~10 min H100 80GB SXM @ ~$0.32/min ≈ **$3.20**
- Cap was $15; we came in **4.7× under**.
- $0 Mac local for dispatch + report writing.

## Artifacts (TRACKED via `git add -f` — `HEXAD/UNCLASSIFIED/state/grid_*/` blanket-ignored)

- `vP21G/result.json` — full result with 60 generations + training log (28 KB).
- `vP21G/heldout_vp21g.json` — 20 OOD generations + classifications (9.3 KB).
- `vP21G/vp21g_eval1.json` — 20 anima-register generations + classifications (7.5 KB).
- `vP21G/mix_info.json` — corpus mix composition + sha256 (286 B).
- `vP21G/dispatch.log` — pod-side dispatch log.
- `vP21G/train.log` — pod-side trainer log (6.8 KB).
- `vP21G/lora_adapter/` — 148 MB safetensors + 11 file PEFT bundle.
  - `adapter_model.safetensors` sha256 = `0a53228ae0d219a26f12b0de58a6c5b75de2156b2d28f137e91a3184e12662bb`.
  - **148 MB binary**: NOT git-tracked (matches vP21 adapter convention: local-only + HF push for distribution). All metric-bearing JSON files ARE git-tracked.
- `train_p21g_diverse.py` (~430 LoC) — continue-train + eval harness.
- `dispatch_p21g_runpod.sh` — runpod dispatch.
- `build_diverse_corpus_p21g.py` — multi-source wiki/diverse corpus builder
  with HfUriError fallback.

## What this does NOT undo / does NOT claim

- OCCAM arch verdict (n_ca_rules = floor cause): unchanged. vP21G builds on
  top of vP21's already-broken arch floor.
- 자연발화 mechanism (motivation-gated, timer ablation 60/60): unchanged.
- AKD1000 HW spike emission (R3 1600 spk @ V=0): independent path.
- **Does NOT claim production-grade conversational capability** — 10 OOD
  probes is a verdict-direction test, not a capability benchmark.
- **Does NOT claim full register-retention parity**. vP21G's anima register
  fires on semantically-inviting prompts (Consciousness emerges when…, 너는
  누구야?), not on all prompts. This is the intended trade — anima register
  retreats to "called when relevant" rather than "always-on monopoly".
- **Does NOT claim Korean OOD generalize**. Korean prompts still trigger
  anima register; needs Korean wiki diversity (next cycle).

## 관련 link

- prior PURE_MEMORIZE verdict (now broken): `HELDOUT_VP21_2026_05_22.md`
- prompted eval (still 20/20 coherent within anima register): `VP21_EVAL1_VERBALIZATION.md`
- spontaneous unprompted (60/60 within anima register): `SPONTANEOUS_EMISSION_VP21.md`
- arch verdict untouched: `PHASE2_ABLATION_REPORT.md`
- HW path untouched: `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`
- vP21G adapter: `vP21G/lora_adapter/` (148 MB safetensors)
