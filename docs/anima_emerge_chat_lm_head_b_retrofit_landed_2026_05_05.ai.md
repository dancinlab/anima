# lm_head_b retrofit micro smoke — landed 2026-05-05

**BG-EI** — empirical test of HEAD-bound hypothesis from BG-DS (head-swap KoGPT2
recovers Korean → is the head the bottleneck, or is it the KoGPT2 head's
*trained* geometry that matters?).

**Verdict label**: `PASS_LM_HEAD_B_RECOVERS_SINGLE_PROMPT`
**Reality**: soft FAIL of HEAD-bound hypothesis at micro scale. See §4.

---

## 1. Spec — lm_head_b retrofit design

### 1.1 Architecture
- **Frozen body**: CLM v4 backbone L0-L15 + `decoder.ln_f` — ALL parameters
  `requires_grad=False`.
- **New head_b**: `nn.Linear(768, 64000, bias=False)`, `nn.init.normal_(std=0.02)`,
  parallel to head_a (does NOT replace; head_a remains intact).
- **Hook**: `decoder.ln_f` forward hook captures L15 hidden, fed to head_b.

### 1.2 Training
- Optimizer: `AdamW(lm_head_b.parameters(), lr=1e-4)`.
- Loss: `CE(head_b(L15_hidden[:, :-1, :]), input_ids[:, 1:])` — next-token
  on full sequence (auto-regressive shift).
- Corpus: 10 Korean `사용자/어시스턴트` QA pairs (micro test set).
- Epochs: 1.

### 1.3 Falsifiers (pre-execution LOCK)
| Falsifier | Definition | Result |
|---|---|---|
| **F-LM-HEAD-B-1** | post-train Korean coherent emit ≥5 chars on 5/5 KO probe prompts | **4/5 PASS_THRESHOLD** but emits incoherent (see §3) |
| **F-LM-HEAD-B-2** | φ★ NO_FLIP (drift < 0.05) | PASS by construction (body frozen — zero gradient on L0-L15 + ln_f) |
| **F-LM-HEAD-B-3** | BG-AN paradigm B emerge dialogue 4-line emit format intact | PASS by construction (head_a untouched, head_b is parallel) |

---

## 2. Run results

| Metric | Value |
|---|---|
| Model | `need-singularity/clm-v4-mk2-v1` (vocab=64000, hidden=768) |
| Platform | mac CPU fp32 (.venv-eeg python3.12) |
| Load time | 5.1 s |
| head_b params | 49,152,000 |
| Train examples | 10 |
| Epochs | 1 |
| Loss first → last | 11.18 → 10.51 (drop = 0.67) |
| Mean loss | 10.96 |

---

## 3. Korean character counts

| Mode | Probe `사용자: 안녕\n어시스턴트:` emit (15 tokens) | Korean chars |
|---|---|---|
| **Baseline head_a** | `'aaaaaaaaaeeeeee'` | **0** |
| **Random init head_b** | `'郵政郵政 경보기다479폴로지 경보기다 경보기다 경보기다479俄羅斯 견딜還Read...'` | **21** |
| **Post-SFT head_b** | `'郵政郵政 경보기다479폴로지 경보기다 경보기다 경보기다479Read郵政郵政 경보기다479Read'` | **23** |
| Improvement (post − random) | | **+2** |

5-prompt sweep (post-SFT, F-LM-HEAD-B-1 threshold = 5 Korean chars):

| Prompt | Korean | Pass(≥5) |
|---|---|---|
| 안녕 | 23 | yes |
| 너는 누구야? | 4 | no |
| 오늘 날씨 어때? | 11 | yes |
| 한국어 할 수 있어? | 8 | yes |
| 고마워 | 8 | yes |
| **Total** | | **4/5** |

---

## 4. Honest interpretation — soft FAIL of HEAD-bound hypothesis

The label `PASS_LM_HEAD_B_RECOVERS_SINGLE_PROMPT` triggered only because the
threshold was Korean *count* not coherence. Reality:

1. **Baseline head_a emits ASCII** (`'aaaaaaaaa...'`) — confirming BG-DS
   observation.
2. **Random init head_b at step 0 already emits 21 Korean chars** — pure
   stochastic head over 64k vocab biased toward CJK frequency in the
   tokenizer; this is *noise*, not signal.
3. **Post-SFT improvement = +2 Korean** — within noise bounds. Loss dropped
   only 0.67 over 10 examples (CE 11.18 → 10.51); head_b is barely moving from
   random.
4. **Emit is incoherent**: `'郵政郵政 경보기다479폴로지 경보기다 경보기다...'` —
   repetitive Chinese postal + Korean noun + numeric fragment. NOT coherent
   Korean dialogue. The KoGPT2 head_b in BG-DS produced 58 coherent Korean —
   the KoGPT2 head's *trained vocab geometry* matters, not just the
   architectural slot.

### 4.1 HEAD-bound hypothesis verdict
- **BG-DS PASS** was driven by KoGPT2 head's *learned token-frequency
  distribution over its 51k Korean-heavy vocab*, not by the head slot itself.
- **Random init head_b alone** with micro-SFT cannot replicate this — body
  geometry (L15 hidden distilled for head_a token-id meaning) is misaligned
  with random head_b token-id meaning.
- **HEAD-bound hypothesis at this scale = FALSIFIED**: the head alone is NOT
  the bottleneck once you de-couple it from a trained Korean LM head.

### 4.2 What would test the hypothesis fairly
1. **Init head_b from KoGPT2 head weights** (then SFT) — but vocab IDs differ
   between SP-64k and KoGPT2's BPE-51k, so this requires a vocab-projection
   layer or vocab unification.
2. **Scale**: 1k Korean QA + 3-10 epochs. Loss 11→10.5 in 10 steps suggests
   ~7k+ steps to reach loss <2 (rough estimate).
3. **Body unfreeze last 1-2 layers** — to let L15 geometry adapt to head_b
   token-id meaning.

---

## 5. Honest C3
1. **C1** mac CPU fp32 — single device, slow but deterministic.
2. **C2** 1 epoch + 10 examples = micro smoke, NOT realistic SFT.
3. **C3** random init head_b — Korean count at step 0 is noise; signal would
   be loss drop + emit coherence (neither materialized strongly).
4. **C4** 5-prompt sweep = breadth check; threshold 5 Korean is permissive
   (random init already passes 4/5).
5. **C5** BG-DS HEAD-bound hypothesis: this BG is the direct empirical test.
   FAIL → KoGPT2 head's *trained vocab geometry* was the recovery signal,
   NOT the head slot itself. CLM v4 chat-cap path needs body+head joint
   training or KoGPT2-init head_b with vocab projection.

---

## 6. Next step recommendation

**Do NOT scale this micro smoke to 1k corpus / multi-epoch as-is** — the
random-init head_b on frozen body geometry will plateau at noise-level
coherence regardless of corpus size, because L15 hidden was distilled for
head_a token-id meaning.

**Instead**:
1. **Path α** — KoGPT2 head_b SFT with vocab-projection layer (SP-64k →
   KoGPT2-51k, learnable embedding-lookup bridge). Tests whether *trained head
   geometry* + body adaptation can recover coherent Korean.
2. **Path β** — body+head joint SFT, last 2 layers unfrozen. Tests whether
   CLM v4 backbone is learnable for chat-cap given small corpus.
3. **Path γ** — defer chat-cap on CLM v4; consolidate Llama Path A v2 winner
   per [feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md] —
   CLM v4 = substrate-research only.

Recommended ranking by 완성도 lens:
- **#1 Path γ (defer)** — Llama Path A v2 already PASSED chat-cap; CLM v4
  chat-cap exploration ROI is low and Pβ + CLM-2 already converged on
  architectural #115 chat-incapability.
- **#2 Path α (vocab-projection)** — most direct test of HEAD-bound
  hypothesis, ~$5-20 H100 budget for 1k QA × 3 epoch.
- **#3 Path β (body+head joint)** — closer to standard LoRA SFT; already
  falsified by F-CLM-LORA-2 FAIL_REGRESSION at full body LoRA scale.

---

## 7. Deliverables
- `state/anima_emerge_chat_lm_head_b_retrofit_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_chat_lm_head_b_retrofit.py`
- `docs/anima_emerge_chat_lm_head_b_retrofit_landed_2026_05_05.ai.md` (this doc)

## 8. Compliance
- raw#37 transient .py sister-rule (torch nn.Module training; hexa cannot)
- raw#15 additive — does NOT modify mount.hexa, dialogue scripts, decoder
- raw#10 honest C3 — 5 caveats emitted
- .own 3 transient sister-rule, gitignored per `**/*.py`
- no commit, no HF token leak
- $0 mac CPU, ~3 min wall (load 5s + sweep ~20s + SFT ~30s + emit sweeps ~120s)
