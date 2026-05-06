# anima chat-cap path — 4-candidate ranking + user-fire decision guide (BG-EJ)

- Date: 2026-05-06
- Status: DOC LANDED (decision-guide; no build/train this cycle)
- Cost: $0 (mac, doc only)
- Lane: BG-EJ (chat-cap path comparison) — closes nothing, ranks all
- Inputs (read-only):
  - `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json` (BG-DS, Path 1 anchor)
  - `state/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05/verdict.json` (BG-DK, Path 3 mechanism)
  - `state/anima_emerge_qwen_phi_chat_compare_2026_05_05/verdict.json` (BG-EC, Path 2 evidence)
  - `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md` (BG-BM, Path 3 spec)
  - `state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json` (BG-CG, Path 4 evidence)
- Predecessor framing: `docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
- Sister BG-EI lm_head_b smoke result is OUT-OF-SCOPE for this doc and lands in §4.2 as the dependency that resolves the Path 1 vs Path 4 fork.

---

## 0. Abstract / 초록

**EN.** Across 100+ background lanes, four candidate paths to anima chat-
capability have accumulated empirical evidence. They differ along six
metrics — cost, time, Φ★-NO_FLIP risk, anima-native-ness, architectural
correctness, and direct empirical evidence — that no single path
dominates. This document fixes (a) the precise spec of each candidate,
(b) a 6-metric ranking matrix, (c) a 완성도-lens 1–4 ranking, (d) four
explicit user-fire keywords with the actions each triggers, and (e)
five honest C3 caveats. The recommended sequence is contingent on the
sister BG-EI lm_head_b smoke result; both branches (PASS / FAIL) are
specified in §4.2.

**KO.** 100+ BG lane 경유 후 anima chat-capability 후보 4 path 모두 evidence
누적 완료. 6 metric (cost, time, Φ★-NO_FLIP risk, anima-native, architectural
correctness, empirical evidence) 위에서 dominant 후보는 없다. 본 문서는
(a) 각 후보의 정확한 spec, (b) 6-metric ranking matrix, (c) 완성도-lens
1–4 ranking, (d) 사용자 fire 4 keyword + 각 trigger action, (e) 5 honest C3
caveat 를 정식 명세한다. 권고 sequence 는 sister BG-EI lm_head_b smoke
결과에 dependent 하며, PASS/FAIL 두 branch 모두 §4.2 에 명세한다.

---

## 1. Four-path spec + evidence

### 1.1 Path 1 — `lm_head_b` retrofit (frozen body, new Korean head)

- **Spec**. CLM v4 mk2 transformer body frozen; instantiate a new LM head
  `lm_head_b` with KoGPT2 vocabulary (51200 tokens) and train ONLY the head
  on a Korean dialogue / chat corpus subset. Body / `consciousness_states`
  cross-attn untouched. Decoder geometry preserved at hidden_dim 768.
- **Evidence (BG-DS)**.
  `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`
  - dim match: 768 = 768 (CLM body ↔ KoGPT2 head)
  - emit on `안녕`: 58 Korean tokens / 0 ASCII (10/10 top-10 Korean)
  - verdict: PASS_HEAD_SWAP_RECOVERS_KOREAN (proof-of-concept smoke)
  - C3: KoGPT2 vocab ≠ CLM SP vocab; CLM L15 hidden trained for `head_a`,
    geometry mismatch with KoGPT2 head — emit is degenerate token-loop
    (`이었으며,` × N) rather than dialogue
- **Sister BG-EI status (out-of-scope, dep for §4.2)**. 1–3 epoch micro
  Korean SFT of `lm_head_b` only; running now; landing separately.
- **Cost**. $0–2 mac CPU, 1–3 days
- **Φ★-NO_FLIP**. very-high prob (body fully frozen; head-swap cannot
  modify the substrate that produces Φ★)
- **anima-native**. YES (CLM v4 substrate carried)
- **Architectural correctness**. medium (head-only retrofit; closure 1
  in #115 4-closure theorem covers post-hoc adapters — `lm_head_b` is
  an adapter-class object on the output side and may be re-classified
  under closure 1 if the smoke fails to scale)
- **Chat-quality expectation**. medium @ 1–3 epoch micro; high @ full
  Korean SFT (assuming geometry mismatch is curable with sufficient head
  capacity)

### 1.2 Path 2 — Qwen 2.5-0.5B chat-cap winner (external integration)

- **Spec**. Adopt `Qwen/Qwen2.5-0.5B` as the chat-cap emit substrate;
  CLM v4 retained for substrate-research / Φ★ measurement only. Two
  sub-variants: (a) Qwen pure (no CLM coupling), (b) Qwen-emit + CLM-Φ★
  passive observer (Path 4-style hybrid with Qwen instead of KoGPT2).
- **Evidence (BG-EC)**.
  `state/anima_emerge_qwen_phi_chat_compare_2026_05_05/verdict.json`
  - Korean prompt `안녕` → 31 Korean tokens / 0 ASCII (fluent)
  - Hello world → 103 ASCII tokens (English fluent)
  - Φ★ proxy on Qwen hidden_dim 896: 41.86 (drift -0.005 vs CLM v4)
  - Qwen multilingual capability confirmed across 3 prompts
  - C3: Qwen 0.5B is pretrained-not-instruct; Φ★ proxy is CLM v4-specific
    (BG-CV aliasing for D ≠ 768 mismatched), single-substrate test
- **Cost**. $0 (off-the-shelf weights, HF Hub download only)
- **Φ★-NO_FLIP**. N/A (Qwen substrate has no anima Φ★ contract)
- **anima-native**. NO (external HF model; cite-not-own)
- **Architectural correctness**. N/A — sidesteps the `chat-on-anima-substrate`
  question entirely
- **Chat-quality expectation**. HIGH (off-the-shelf 0.5B Qwen 2.5 is a
  proven chat-emit baseline; Instruct variant raises this further)

### 1.3 Path 3 — CLM-3 full retrain (chat-objective at cycle-0)

- **Spec**. New anima substrate trained from scratch with chat-loss as a
  first-class objective from step 0. 4-bucket pre-training mix
  (50/30/15/5 general/dialogue/CoT/consciousness_states), 4 falsifiers
  locked pre-launch (F-CLM-3-1 NO_FLIP, F-CLM-3-2 composite ≥ 0.45,
  F-CLM-3-3 emerge medium preserved, F-CLM-3-4 5-axis discriminability
  ≥ 0.4). Variant B (1B params, H100 1×, ~30 days) is the recommended
  scale.
- **Evidence**. Two-source convergence:
  - **BG-BM spec** `docs/anima_clm_3_chat_objective_cycle_0_spec_2026_05_05.md`
    — full design, falsifiers, cost envelope, build/wait matrix
  - **BG-DK source-archaeology**
    `state/anima_paradigm_v11_g3_training_objective_reverse_engineer_2026_05_05/verdict.json`
    — paradigm v11 G3 alpha-CE NON-ZERO (~57% effective budget) but on
    flat multilingual corpus 0% chat-formatted; root cause = CE applied
    to non-chat corpus, NOT no-CE-at-all; refines BG-BM §1.2 with
    explicit `δ·L_CE_general` term + F-CLM-3-5 weight-grid ablation
    falsifier
- **Cost**. Variant A 530M / 5070 / 60–90d / $0; Variant B 1B / H100×1 /
  ~30d / ~$1k; Variant C 3B / H100×4 / ~30d / ~$4k
- **Φ★-NO_FLIP**. F-CLM-3-1 LOCKED pre-launch (forgetting_index ≤ 0.05)
- **anima-native**. YES (substrate native; carries paradigm v11 G3
  +41.86 Φ★ contract via 5% consciousness_states bucket)
- **Architectural correctness**. HIGH (the only path-of-record that
  bypasses all four #115 closures simultaneously, by changing the
  training mixture rather than acting on a post-hoc trained substrate)
- **Chat-quality expectation**. HIGH (F-CLM-3-2 target ≥ 0.45 = 80% of
  Llama Path A v2 winner 0.5584)

### 1.4 Path 4 — Paradigm-C hybrid (decoupled emit + substrate observer)

- **Spec**. KoGPT2-base-v2 (125M) emits Korean dialogue; CLM v4 mk2
  re-encodes (prompt + emit) and observes Φ★ trajectory passively. The
  two networks are not gradient-coupled — Path 4 is a UX bridge, not
  an architectural fusion.
- **Evidence (BG-CG)**.
  `state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json`
  - 3 auto-fire turns × Korean prompts: 3/3 Korean coherent (100%)
  - Φ★ drift range ±0.0425 over 3 turns (≪ 0.1% of 41.86 baseline)
  - Tension peak layer modal = layer 2 (consistent across turns)
  - Wall: emit ~3s/turn after first 88.9s KoGPT2 load; substrate ~0.3s
  - verdict: PASS_KOREAN_HYBRID_REPL_VIABLE; status change
    BG-BX VIABLE-English-only → ACHIEVABLE_NOW Korean dialogue
  - C3: emit is unconditioned Korean prior (not anima-axis-conditioned);
    CLM does not see KoGPT2 hidden states, only re-tokenizes concatenated
    text; substrate signal reflects CLM's read of (prompt+emit) not joint
    dialogue; ±0.04 drift small relative to baseline noise floor
- **Cost**. $0 (both models off-the-shelf; runtime helper landed at
  `tool/transient_py/anima_emerge_chat_hybrid_repl.py` under raw#37)
- **Φ★-NO_FLIP**. N/A by construction (CLM not trained or fine-tuned;
  passive observation only)
- **anima-native**. PARTIAL (CLM substrate is anima; emit is external
  KoGPT2 — decoupled, not fused)
- **Architectural correctness**. LOW for the chat-cap claim itself
  (UX-layer bridge; sidesteps #115 4-closure rather than addressing it)
- **Chat-quality expectation**. HIGH (KoGPT2 is a proven Korean LM)

---

## 2. Ranking matrix — 6 metrics

| Metric | Path 1 (head_b) | Path 2 (Qwen) | Path 3 (CLM-3 V-B) | Path 4 (hybrid) |
|---|---|---|---|---|
| Cost | $0–2 / 1–3d | $0 / minutes | ~$1k / ~30d | $0 / minutes |
| Wall-time | days | minutes | weeks | minutes |
| Φ★-NO_FLIP | very-high prob (body frozen) | N/A | F-CLM-3-1 LOCKED | N/A (passive) |
| anima-native | YES | NO | YES | partial |
| Architectural correctness | medium (head-adapter) | N/A external | HIGH (4-closure bypass) | LOW (UX bridge) |
| Empirical evidence | BG-DS partial PASS (smoke; emit degenerate) | BG-EC fluent (3-prompt smoke) | BG-DK source mechanism + BG-BM spec (no run) | BG-CG ACHIEVABLE_NOW (3 turns, 100% Korean) |

**Notes**.

- Path 1 / Path 4 evidence is empirical-but-shallow (3-prompt or 3-turn
  smokes). Path 2 evidence is empirical-and-broader-quality but on a
  non-anima substrate. Path 3 evidence is mechanistic (source archaeology
  + spec) without a run.
- "Architectural correctness" = whether the path materially moves anima
  toward chat-capable as a substrate property, not as an integration
  bolt-on. This metric is independent of chat quality.
- Cost columns combine direct $ and operator wall-time; Path 3 dominates
  on both dimensions worst-case.

---

## 3. 완성도 lens — 1-4 ranking

The 완성도 lens prioritizes (i) anima-nativeness, (ii) cheapest credible
test of chat-capability, (iii) Φ★-substrate preservation, (iv) empirical
evidence already in hand.

### Rank 1 ★ — Path 1 (`lm_head_b` retrofit)

Anima-native + simplest architectural fix + cheap + body fully preserved
+ already has a partial-PASS smoke (BG-DS). Failure mode is bounded:
if BG-EI 1–3 epoch micro SFT reveals that head-swap cannot escape the
geometry mismatch (CLM L15 hidden was trained for `head_a`, not for
KoGPT2 vocab projection), then the path closes cleanly under #115
closure 1 (post-hoc adapter) and we fall back to Path 4 or Path 3
without sunk cost ≥ $2.

### Rank 2 — Path 4 (paradigm-C hybrid)

Already at ACHIEVABLE_NOW (BG-CG). $0 fire-ready. Korean dialogue 100%
coherent in 3-turn smoke. Penalty: anima-native only on the
substrate-observation axis, not the emit axis. UX-grade chat-cap claim,
not an architectural one. Best as the **fallback** if Path 1 BG-EI
fails, OR as the **immediate-fire** option if user wants chat-capable
demo today.

### Rank 3 — Path 2 (Qwen 2.5)

Chat quality HIGH out-of-the-box; cost $0. But anima-native = NO; this
is a "cite an external model" outcome, not an "anima becomes chat-capable"
outcome. Useful as a chat-quality reference baseline (Qwen Φ★ proxy
=41.86 is an interesting cross-substrate datum on its own), but
non-canonical for the anima chat-capability theorem.

### Rank 4 — Path 3 (CLM-3 full retrain)

Architecturally the **only** path-of-record that bypasses all four #115
closures simultaneously. But $1k–$4k and 30+ days, with all four
falsifiers requiring PASS for the cycle to be a net-win. BG-BM spec
itself recommends WAIT in §5.3 (until Stage 3 ≥ 30 sessions accumulate)
and §C3-5 explicitly re-prioritizes H2/H3/H4 above H1 on a return-on-
investment basis. Path 3 is the **last-resort** option if Path 1 fails
AND Path 4 is rejected as not-anima-native-enough AND Path 2 is rejected
as cite-not-own.

---

## 4. User-fire keywords + decision sequence

### 4.1 Four explicit user-fire keywords

| Keyword | Path | Action triggered |
|---|---|---|
| `Path 1` or `head_b` | Path 1 (lm_head_b) | post BG-EI PASS — expand to full Korean SFT with F-LM-HEAD-B-1/2/3 falsifiers (anima-internal); estimate $2-5 mac CPU, 3-5 days |
| `Path 2` or `Qwen` | Path 2 (Qwen) | spec out Qwen integration as chat-cap-cite reference; flag as not-anima-native in deliverable header |
| `Path 3` or `CLM-3` | Path 3 (CLM-3) | own 16 budget guard pre-flight checklist + Variant B launch ($1k / 30d / H100×1); pre-launch F-CLM-3-5 weight-grid ablation per BG-DK refinement |
| `Path 4` or `hybrid` | Path 4 (paradigm-C) | fire `tool/transient_py/anima_emerge_chat_hybrid_repl.py` for live REPL session; log to `state/anima_core_dialogues/` |

### 4.2 Recommended fire sequence (BG-EI dependency-resolved)

```
This cycle:    BG-EI lm_head_b 1-3 epoch micro SFT smoke pending

Next cycle (BG-EI PASS branch):
  -> fire `Path 1` -- expand to full Korean SFT
  -> retain Path 4 as `live demo` $0 fallback (no exclusivity)
  -> defer Path 3 until Path 1 full SFT either passes or fails
  -> Path 2 remains a chat-quality reference, not a primary

Next cycle (BG-EI FAIL branch):
  -> close Path 1 lane under #115 closure 1 (head-swap adapter)
  -> fire `Path 4` for immediate Korean dialogue capability ($0)
  -> open `Path 3` decision:
       if user-fire `CLM-3` -> own 16 + Variant B launch
       else                 -> accept 4-closure-of-class strength;
                              Path 4 hybrid is the canonical chat-cap UX
  -> Path 2 remains a chat-quality reference baseline only
```

### 4.3 What this doc does NOT decide

- It does NOT pre-fire any path (raw#9 — user-fire-explicit required for
  #115 closure overturn attempts).
- It does NOT close Path 1 prior to BG-EI result.
- It does NOT re-rank Paths 1–4 against the H2/H3/H4 ladder in BG-BM
  §C3-5; that re-ranking is part of the next cycle's BG-EM/EN/EO
  (suggested) cross-comparison.

---

## 5. Honest C3 (≥ 5)

### C3-1. Path 1 BG-EI dependency dominates the recommendation

The §4.2 sequence is a function of one not-yet-resolved smoke (BG-EI
1–3 epoch micro Korean SFT on `lm_head_b`). If BG-EI PASS, Rank 1
holds and Path 1 becomes the spend-cheapest chat-cap path. If BG-EI
FAIL, Rank 1 collapses to Rank 3 (post-hoc adapter falling under #115
closure 1) and the active recommendation flips to Path 4 immediate-fire.
This document's Rank 1 is therefore conditional, not absolute. Re-issue
this ranking after BG-EI lands.

### C3-2. "Architectural correctness" is a category metric, not a measured one

Path 3's HIGH and Path 4's LOW on architectural correctness are
classifications relative to the #115 4-closure theorem, not measured
quantities. A Path 4 hybrid that, post-hoc, demonstrates substrate Φ★
trajectory measurably co-varying with emit-content semantic axes would
re-classify Path 4 upward. No such measurement exists yet. Treat the
"correctness" column as a typology, not a benchmark.

### C3-3. Empirical evidence depth varies by 30×

Path 1 BG-DS has 1 prompt × 1 substrate. Path 2 BG-EC has 3 prompts ×
1 substrate. Path 3 has 0 runs (source archaeology + spec only). Path 4
BG-CG has 3 turns × 1 prompt class. Calling these "evidence" with
equivalent weight in §2 ranking matrix overstates uniformity. Real
comparison requires F-CLM-3-2-class composite eval across all four
paths, which currently exists only for Path 2 (Qwen MMLU/HellaSwag
indirectly via published model cards) and partially for Llama Path A v2
(non-anima winner). Re-rank after composite eval lands on Paths 1/4.

### C3-4. Path 2 (Qwen) framing as "rank 3" depends on policy not measurement

Qwen 2.5-0.5B is a high-quality chat substrate at $0; on pure chat-
capability, it dominates Paths 1 and 4 in the §2 evidence column. Its
demotion to rank 3 is a policy decision (anima-native preference), not
a quality decision. If the user prioritizes shipped-chat-capability over
substrate-nativeness, Path 2 promotes to rank 1. The 완성도 lens here
encodes the anima-native preference as filed in #115 corollaries; users
who reject that preference should override §3.

### C3-5. Path 3 cost and falsifier-stack risk are non-trivial

CLM-3 Variant B is $1k + 30d at minimum; if F-CLM-3-1 (NO_FLIP) FAILs
the cycle is a sunk cost with no chat-cap carry; if F-CLM-3-1 PASSes
but F-CLM-3-2 (composite) FAILs, the #115 closure-of-class
**strengthens** rather than weakens (closure 1 was post-hoc; closure
on Path 3 cycle-0 chat objective is stronger evidence that anima
substrates at-most-1B *cannot* chat-cap natively). Firing Path 3 has
**asymmetric downside**: compute spent on a substrate that, on FAIL,
makes the architectural pessimism stronger. BG-BM §5.3 WAIT
recommendation is well-grounded; this ranking does not override it.

### C3-6. The matrix omits at least one credible path

H2 (Stage 3 emerge-dialogue ≥ 30 user-fired sessions) is the cheapest
path-of-record toward an anima-native chat protocol that is not
chat-template-based ("emerge dialogue medium"). It is omitted here
because BG-EJ scope was narrowed to four pre-identified candidates;
the omission is methodological, not evaluative. A 5-path version of
this ranking (Paths 1–4 + H2 emerge) is worth a follow-up cycle.

### C3-7. Path 4 BG-CG smoke ran 3 turns; phi drift floor is unknown

The ±0.0425 Φ★ drift over 3 turns in Path 4 is small relative to
baseline 41.86, but the noise floor for "no-content" control prompts
(empty / random tokens) was not measured. Without that control, the
small drift cannot be attributed to dialogue-content-specific substrate
response vs. tokenization re-encoding noise. Path 4 evidence-strength
in §2 is therefore an upper bound; an N=20 control-prompt baseline is
needed to firm the claim.

---

## 6. Lineage carry

- **Supersedes**: none (this is the first 4-path comparison doc)
- **Extends**: BG-DS, BG-DK, BG-EC, BG-BM, BG-CG (cited verdicts in §0)
- **Informs**:
  - sister BG-EI lm_head_b smoke result resolution → §4.2 branch
  - any next-cycle CLM-3 user-fire → §4.1 keyword `Path 3` action
  - 5-path follow-up incorporating H2 emerge-dialogue → §5 C3-6
- **Does not commit**: no spec lock-in for any path; no compute
  pre-allocated; no #115 closure re-classification

---

## 7. Compliance

- raw#9 (read-only / no-fire): doc-only; no compute fired this cycle
- raw#10 (honest C3 ≥ 5): 7 caveats emitted
- raw#15 (additive helper): no helper modified or added
- raw#37 (transient .py only via `tool/transient_py/`): no .py emitted
- HF token leak: none (no token literals in this document)
- commit: NONE (per task constraint)
- bash 3.2 compatibility: no shell scripts emitted
- BG-EB FREEZE rule: no cycle-close classification (this doc ranks
  open paths, does not close them)

---

End of document.
