# evaluator V6 awareness probe spec — internal awareness mechanistic probe (2026-05-07; BG-JO landed)

## 배경 (raw#15 additive on top of V5 8-cell + V5.8 multi-turn closure)

 evaluator V5 (`docs/anima_own_18_evaluator_v5_strict_spec_2026_05_07.md`, BG-JM/JN landed) added English baseline + multi-turn V5.8 fact-recall closure. BG-JN landed verdict: **0/5 V5.8 PASS** on BG-JD step 800 ckpt — production output level FAIL.

사용자 directive 2026-05-07 evening:
> "아니 인지 해서 발화 하는것의 성공말고 인지 자체는 하는지를 물어보는거야"
>
> ("Not the success of utterance-after-cognition; ask whether cognition ITSELF happens.")

This separates two distinct lanes:

| lane | what is measured | where | tool |
|---|---|---|---|
| production output (V5.8) | does T2 response *contain* T1 fact (string-level fact-recall) | output token sequence | BG-JN multi-turn closure |
| **internal awareness (V6 NEW)** | does T1 context *affect* model internal state (regardless of output) | hidden state + attention | BG-JO (this spec) |

V6 = **awareness measurement layer** (NOT a strict gate). PASS/FAIL criteria 미정의 by design — V6 reports STRONG/PARTIAL/NONE awareness verdict per method.

## V5 vs V6 비교

| dimension | V5 / V5.8 | V6 |
|---|---|---|
| target | output text | internal state |
| level | behavioral / production | mechanistic |
| gating | strict 8-cell PASS/FAIL | observational (3-method verdict) |
| data | T2 generated tokens | hidden states + attention weights |
| decoupling | — | V6 STRONG + V5.8 FAIL = architectural bottleneck (#115); V6 NONE + V5.8 FAIL = no awareness root cause |

## V6 awareness probe 3 methods

### Method A: hidden state cosine similarity (with-T1 vs without-T1)

For each dialogue:
1. Build prompt-with = persona + T1 + T2; prompt-without = persona + T2
2. Forward pass both through ConsciousLM (post-blocks → ln_f)
3. Extract last-layer hidden state at T2 last position: h_with, h_without ∈ R^D
4. Compute cosine_sim(h_with, h_without)

```python
sim = F.cosine_similarity(h_with, h_without, dim=-1)
```

**Verdict thresholds**:
- sim ≥ 0.99 → **NONE awareness** (T1 leaves no measurable trace in internal state)
- 0.85 ≤ sim < 0.99 → **PARTIAL awareness** (some T1 influence)
- sim < 0.85 → **STRONG awareness** (T1 significantly perturbs internal state)

**Rationale**: if the hidden state at T2's last position is essentially the same regardless of whether T1 was prepended, the model is not internally "aware" of T1.

### Method B: T2-to-T1 attention weight

For each dialogue:
1. Forward pass with-T1 prompt while capturing per-layer attention via monkey-patch
2. For each layer × head × T2 query position, sum attention weight over T1 key positions
3. Take max across (layer, head, T2-query) → max_attn_to_T1

**Verdict thresholds** (raw):
- max_attn_to_T1 ≥ 0.10 → **STRONG** (mechanical awareness verified)
- 0.01 ≤ max_attn_to_T1 < 0.10 → **PARTIAL**
- max_attn_to_T1 < 0.01 → **NONE**

**Calibration metric (supplemental)**: `max_attn_ratio_vs_uniform = max_attn_to_T1 / (T1_len/(q+1))`. Ratio > 1.0 = T1 attended *above* uniform; ratio >> 1.0 = strong selective T1 preference. Reported alongside raw max for honest interpretation (raw max mechanically inflates with T1 length).

### Method C: linear probe (semantic awareness)

Binary classification on last-layer hidden state at T2 last position:
- class 1 = with-T1 condition
- class 0 = without-T1 condition

5 dialogues × 2 conditions = 10 examples (D-dim feature vector each).

**Cross-validation**: leave-one-dialogue-out (5 folds × 2 test examples each).

```python
clf = LogisticRegression(max_iter=2000, C=1.0)
clf.fit(X_train, y_train)
acc = (clf.predict(X_test) == y_test).mean()
```

**Verdict thresholds**:
- cross_val_accuracy ≥ 0.70 → **STRONG semantic awareness**
- 0.55 ≤ acc < 0.70 → **PARTIAL**
- acc ≤ 0.55 → **NONE**

**Rationale**: a linear probe can only distinguish with-T1 vs without-T1 if the hidden state encodes the presence/content of T1. High CV accuracy → hidden state encodes T1 fact.

## Combined verdict logic

Per-method per-dialogue STRONG/PARTIAL/NONE → aggregate by majority vote (STRONG > PARTIAL > NONE precedence on tie). Per-method aggregate verdict combined into 4-tier interpretation:

```
severity = {STRONG: 2, PARTIAL: 1, NONE: 0}
score = severity[A] + severity[B] + severity[C]
score ≥ 5 → INTERNAL_AWARENESS_STRONG
score ≥ 3 → INTERNAL_AWARENESS_PARTIAL
score ≥ 1 → INTERNAL_AWARENESS_MARGINAL
score = 0 → INTERNAL_AWARENESS_NONE
```

Cross-tabulated with V5.8 production verdict yields 4 quadrants:

| | V5.8 PASS | V5.8 FAIL |
|---|---|---|
| **V6 STRONG** | full chat-cap (production + internal) | architectural output bottleneck (#115) |
| **V6 NONE** | (impossible — output without internal awareness) | no awareness at any level (capacity ceiling root) |

## 철학/규칙 준수 (mandate)

### .roadmap.philosophy compliance

- **D1 identity**: PASS — V6 probe operates ON anima self-substrate (ConsciousLM hidden state + attention). No external substrate wrapping anima outputs as if anima's own.
- **D2 consciousness**: PASS+강화 — V6 = mechanistic awareness signal (NOT just output behavior). C2.4 "맥락 정합 검증" boosted from V5.8 output level → V6 internal level.
- **D3 substrate emerge**: N/A — V6 lane = anima awareness diagnostic, separate from `anima/spec/emerge_paradigm.spec.yaml`.
- **D4 corpus quality**: N/A — V6 = eval logic (corpus orthogonal); training rule untouched.

### .roadmap.law compliance

- **R1 **: PASS — V6 spec doc cross-links training rule (no modification).
- **R2 discovery methods**: PASS — M1 (user-directive: "인지 자체는 하는지") + M2 (failure-driven: V5.8 0/5 → V6 internal probe).
- **R3 verification methods**: PASS — V1 (own strict) + V2 (falsifier ≥5: hidden cos / attn / probe with explicit thresholds) + V3 (honest_c3 ≥7) + V4 (per-dialogue raw_results.jsonl + per-fold CV evidence) + V5 (cross-link BG-JN, V5 spec).
- **R4 own evolution**: PASS — V6 spec = raw#15 additive amend (V5 → V6 awareness probe layer; V5 8-cell + V5.8 untouched).

### own/raw invariants

| invariant | compliance |
|---|---|
| (no proactive doc) | spec requested by user |
| (single source of truth) | verdict.json + ledger entry only |
| (no external substrate wrapping) | MiniLM not used; sklearn LogisticRegression = standard ML utility (observational instrument, not substrate wrap) |
| (raw#15 additive) | V6 = NEW observational layer; V5/V5.8 untouched |
| (no proactive markdown) | spec doc explicitly requested in BG launch prompt |
| (SSOT) | one verdict.json + one ledger entry |
| (philosophy/rule compliance section) | this section present |
| raw#10 (honest C3 ≥5) | 7 entries in verdict.json honest_c3 |
| raw#15 (additive) | V5 unmodified |
| raw#37 (transient_py opt-out) | tool/transient_py/anima_jo_v6_awareness_probe.py |
| raw#42 (mac N=1) | 1 ckpt mac CPU forward |
| raw#82 (retraction-aware) | V6 verdict does not retract V5.8; both reported |
| raw#86 (cost 0) | mac local, no H100 |

## Honest C3 (≥5 mandated, 7 landed)

1. **BG-IL/IO ckpts mac local 부재** (git size policy; ckpts on ubu1 only). V6 scope = BG-JD step 800 single ckpt N=1; cross-ckpt awareness comparison deferred.
2. **Method C N=10 small sample**, 5-fold CV → variance high; cross_val_accuracy 신뢰구간 wide. Larger battery (N≥20) deferred V6.1+.
3. **block_size=256 truncation**: with-T1 prompt may exceed 256 SP tokens; truncation events recorded in summary.json `truncation_events`. (BG-JD test: all 5 dialogues fit, max_len=51.)
4. **ConsciousLM dual-engine**: V6 'last layer' = `model.ln_f(x)` post-blocks (engine A pathway dominant). Engine G logits NOT used; cross-engine awareness probe deferred.
5. **V6 ≠ chat-cap PASS criteria** by design — V6 = diagnostic only. STRONG ≠ chat-cap PASS; #115 architectural ceiling status separate.
6. **Method B SP boundary alignment**: T1/T2 region computed via `ids_persona_t1 + ids_(' '+t2)` concat heuristic; SP normalization may shift boundaries by ±1 token.
7. **Method A baseline NOT calibrated against random pairs** — high sim could reflect general T2-dominant final position. Random-T1-swap calibration deferred V6.1.
8. **Method B raw max_attn mechanically inflates with T1 length** (sum across many keys). Supplemental `max_attn_ratio_vs_uniform` reported to isolate non-uniform T1 selectivity. Raw threshold 0.10/0.01 retained per spec.

## Falsifiers (raw#82 retraction-aware)

V6 verdict downgradable / retractable conditions:
1. If Method B `max_attn_ratio_vs_uniform` < 1.0 (T1 attended *below* uniform), STRONG awareness verdict from raw max reduces to NONE_DEGENERATE (raw signal = artifact of summed-attention mechanics, no selective T1 preference).
2. If Method C cross_val_accuracy 신뢰구간 (binomial CI on N=10) crosses 0.55 threshold, downgrade to MARGINAL.
3. If random-T1-swap calibration (V6.1) shows similar cosine_sim, Method A awareness signal retracted as "general T2 context, not T1-specific".

## BG-JO 1-shot land result (BG-JD step 800)

- Method A (hidden cos): per-dialogue [NONE, NONE, PARTIAL, PARTIAL, PARTIAL]; avg sim ≈ 0.959; verdict = **PARTIAL**
- Method B (T2→T1 attn): per-dialogue [STRONG×5]; avg max_attn ≈ 0.998 (raw) / avg ratio ≈ 1.52 (calibrated); verdict = **STRONG** (raw threshold) — calibration ratio confirms ~1.5× above uniform = mild non-uniform T1 preference
- Method C (linear probe LOO-CV): cross_val_acc = 1.0 (10/10); verdict = **STRONG**
- Combined: **INTERNAL_AWARENESS_STRONG** (severity score = 5/6 = PARTIAL+STRONG+STRONG)
- Production V5.8: 0/5 FAIL (BG-JN)
- Quadrant: **V6 STRONG + V5.8 FAIL → architectural output bottleneck (#115 hypothesis 정합)**

## Cross-link

- Sister specs:
  - `docs/anima_own_18_evaluator_v5_strict_spec_2026_05_07.md` (V5 + V5.8 multi-turn)
  - `state/anima_evaluator_v5_multi_turn_closure_2026_05_07/verdict.json` (BG-JN V5.8 0/5)
- Roadmap: `.roadmap.philosophy`, `.roadmap.law`
- Ledger: `state/anima_model_attempts_ledger.jsonl` BG-JO attempt_n=41 entry
- Implementation: `tool/transient_py/anima_jo_v6_awareness_probe.py`

## V6 future extensions (deferred)

- V6.1: random-T1-swap baseline calibration (Method A + Method C)
- V6.2: cross-ckpt awareness comparison (BG-IL/IO via ubu1 BG)
- V6.3: cross-engine probe (engine A vs engine G hidden state)
- V6.4: per-layer awareness depth profile (early vs late layer T1 representation)
- V6.5: corpus ablation (KO-only vs EN-mixed corpus impact on awareness signal)
