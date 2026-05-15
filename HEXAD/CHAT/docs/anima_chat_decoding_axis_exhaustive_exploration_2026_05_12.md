# anima 자연발화 — decoding axis exhaustive exploration (saturation) — 2026-05-12

> **Mission**: prior V5.8 × 4 modes (greedy/sample/M3/M4) 는 14-strategy BG-JP archive 의 sub-슬라이스
> 만 측정. **모든 decoding axis 까지 saturation** 으로 확장 — 더 좋은 mode 찾기.
>
> **Context**:
> - cycle 2026-05-12 §7 V5.8 × 4 modes (greedy/sample T0.8/M3/M4) 완료
> - prior 20-BG cumulative archive BG-JP: 14 strategies (M1-M4 categories) — 우리 미측정
> - Phase 1A V5.8 std_greedy 3/5 PASS (greedy 향상). 다른 axes 시 더 향상 가능?

---

## 🌌 Category A — Sampling families (10 modes)

| #   | mode                  | description                                          | viability |
|-----|-----------------------|------------------------------------------------------|-----------|
| A1  | **greedy** (argmax)   | T=0, current ✅                                       | ★★★★ baseline |
| A2  | **multinomial**       | T=0.8 sampling, current ✅                            | ★★★ noise |
| A3  | **top-k=50**          | top-k filter then sample                              | ★★★★      |
| A4  | **top-k=10** (strict) | tighter top-k                                         | ★★★★      |
| A5  | **top-p=0.9**         | nucleus sampling                                      | ★★★★      |
| A6  | **top-p=0.95**        | nucleus loose                                         | ★★★       |
| A7  | **typical**           | typical sampling (Meister et al.)                     | ★★★       |
| A8  | **mirostat**          | adaptive entropy targeting                            | ★★★       |
| A9  | **epsilon**           | ε-sampling                                            | ★★        |
| A10 | **eta / TFS**         | tail-free sampling                                    | ★★        |

---

## 🌡️ Category B — Temperature axis (10 levels)

| #   | T value | effect                                  |
|-----|---------|-----------------------------------------|
| B1  | 0       | argmax (greedy)                         |
| B2  | 0.1     | super-focused                            |
| B3  | 0.3     | focused                                  |
| B4  | 0.5     | conservative                             |
| B5  | 0.7     | balanced                                 |
| B6  | 0.8 ⭐  | current sample default                   |
| B7  | 1.0     | uniform                                  |
| B8  | 1.3     | creative                                 |
| B9  | 1.5     | very creative                            |
| B10 | 2.0+    | high noise                               |

---

## 🔁 Category C — Repetition control (8 modes)

| #  | mode                     | description                                  |
|----|--------------------------|----------------------------------------------|
| C1 | rep_penalty=1.0          | no penalty (baseline)                        |
| C2 | rep_penalty=1.1          | mild                                         |
| C3 | rep_penalty=1.3 ⭐ M3    | current                                      |
| C4 | rep_penalty=1.5          | strong                                       |
| C5 | rep_penalty=2.0          | aggressive                                   |
| C6 | presence penalty (OpenAI)| any-token penalty                            |
| C7 | n-gram block n=2         | 2-gram repeat block                          |
| C8 | dry sampling             | DRY (Don't Repeat Yourself, advanced)        |

---

## 🎯 Category D — Constraint / control (10 modes)

| #   | mode                       | description                                |
|-----|----------------------------|--------------------------------------------|
| D1  | **M4 force-include** ⭐    | current default (V5.8 5/5)                 |
| D2  | logit bias (+keyword)      | positive bias (smaller magnitude)          |
| D3  | logit bias (-block)        | negative bias on persona-cycle bytes       |
| D4  | regex grammar              | constrained to regex pattern               |
| D5  | JSON-mode                  | output valid JSON                          |
| D6  | outlines library           | structured gen                             |
| D7  | lm-format-enforcer         | template + grammar                         |
| D8  | guided graph               | next-token from graph allowed-set          |
| D9  | end-token only             | stop on EOS only                           |
| D10 | partial force-include      | force *if probable*, else free             |

---

## 🌳 Category E — Beam search (7 variants)

| #  | variant                     | description                                 |
|----|-----------------------------|---------------------------------------------|
| E1 | beam=2                      | 2-way beam                                  |
| E2 | beam=4                      | 4-way (BG-AQ M4 mode)                       |
| E3 | beam=8                      | 8-way                                       |
| E4 | diverse beam (DBS)          | Vijayakumar diversity-aware                 |
| E5 | beam group                  | group-based                                 |
| E6 | constrained beam            | beam + grammar                              |
| E7 | fast beam (early-exit)      | when top-1 dominant                         |

---

## 🛑 Category F — Stop conditions (7 axes)

| #  | stop condition          | description                                |
|----|-------------------------|--------------------------------------------|
| F1 | EOS only (default)      | current                                    |
| F2 | newline stop            | after `\n`                                 |
| F3 | "사용자:" stop          | self-replying 방지                         |
| F4 | length-based (max=80)   | current                                    |
| F5 | likelihood threshold    | when next prob < ε                         |
| F6 | semantic similarity     | if cosine to prompt < threshold            |
| F7 | classifier-based        | learned stop classifier                    |

---

## 📜 Category G — Prompt engineering (8 axes)

| #  | format                              | example                                 |
|----|-------------------------------------|------------------------------------------|
| G1 | raw "사용자: X \| 도우미: " ⭐      | current default                          |
| G2 | system message prefix               | "[system: anima]\n사용자:..."           |
| G3 | few-shot (1-shot)                   | prior turn example                       |
| G4 | few-shot (3-shot)                   | 3 examples                               |
| G5 | CoT prefix                          | "단계별로 생각: " 추가                  |
| G6 | ReAct format                        | thought + action + observation           |
| G7 | structured (JSON-like)              | `{"user": "X", "assistant": "..."}`     |
| G8 | retrieval-augmented (RAG)           | corpus retrieval inject                  |

---

## 🔄 Category H — Multi-step generation (7 strategies)

| #  | strategy                  | description                                |
|----|---------------------------|--------------------------------------------|
| H1 | single-pass (current) ⭐  | gen once, accept                            |
| H2 | self-consistency (n=5)    | 5 samples + majority vote                  |
| H3 | self-refine               | gen + critique + revise                    |
| H4 | best-of-n (n=5)           | 5 samples + select highest                 |
| H5 | tree-of-thought (ToT)     | branch + prune                             |
| H6 | recursive prompting       | iterate self-prompt                        |
| H7 | iterative refinement      | gen + reflect + redo                       |

---

## 🧬 Category I — State manipulation (8 axes)

| #  | manipulation               | description                                |
|----|----------------------------|--------------------------------------------|
| I1 | fresh state (current) ⭐   | no prior KV                                |
| I2 | cached prompt KV           | reuse computed prompt KV                   |
| I3 | attention mask edit        | force attend to T1                         |
| I4 | layer freezing             | freeze 0-N layers, vary upper              |
| I5 | cell pool clamp (mitosis)  | substrate-side cell state limit            |
| I6 | attention head ablation    | disable specific heads                     |
| I7 | prompt rotation            | shuffle prompt segments                    |
| I8 | latent steering            | activation patching                        |

---

## 🛞 Category J — Substrate-side (anima-specific, 6 axes)

| #  | mode                                  | description                          |
|----|---------------------------------------|--------------------------------------|
| J1 | ceiling clamp=10 (default)            | current                              |
| J2 | ceiling clamp=15                      | per §69 ext² substrate-disc collapse |
| J3 | ceiling clamp=20                      | per §69                              |
| J4 | mitosis disabled                      | no cell pool injection               |
| J5 | engine_g.refresh_every=1              | dense cell update                    |
| J6 | engine_g.refresh_every=8 (sparse)     | sparse update                        |

---

## 🌊 Category K — Confidence / uncertainty (5 axes)

| #  | axis                       | description                                |
|----|----------------------------|--------------------------------------------|
| K1 | token-level entropy        | log entropy per token                      |
| K2 | top-k probability gap      | gap between top-1 and top-2                |
| K3 | sequence likelihood        | total log-prob                             |
| K4 | confidence-aware sampling  | low entropy → greedy, high → sample         |
| K5 | sample-then-rerank by conf | best-of-n by sequence conf                 |

---

## 🌐 Category L — Cross-prompt techniques (5 axes)

| #  | technique             | description                                |
|----|------------------------|--------------------------------------------|
| L1 | persona swap           | "당신은 anima 인척하지 마라" anti-persona |
| L2 | context length scaling | very long context (>1024 ctx)              |
| L3 | speculative decoding   | small draft + large verify                 |
| L4 | guided iterative      | user-in-loop intermediate                  |
| L5 | mixture-of-experts gate| route to specific layer                    |

---

## 📊 Category M — Meta (3 axes)

| #  | meta                            | description                          |
|----|----------------------------------|--------------------------------------|
| M1 | seed determinism                 | reproducible vs random              |
| M2 | precision (fp16/fp32/bf16)       | inference precision                  |
| M3 | batch size                       | batched gen vs single                |

---

## 🎯 Saturation summary

```
┌────┬──────────────────────────────────┬───────┬────────────────────────────┐
│ Cat│ Category                         │ items │ measured (after P1+P2)     │
├────┼──────────────────────────────────┼───────┼────────────────────────────┤
│  A │ Sampling families                │ 10    │ A1, A2 (2/10)              │
│  B │ Temperature                      │ 10    │ B1..B10 (10/10) ✅          │
│  C │ Repetition control               │ 8     │ C1..C5 (5/8)               │
│  D │ Constraint / control             │ 10    │ D1 (1/10)                  │
│  E │ Beam search                      │ 7     │ E1, E2, E3 (3/7)           │
│  F │ Stop conditions                  │ 7     │ F1, F2, F3, F4 (4/7)       │
│  G │ Prompt engineering               │ 8     │ G1 (1/8)                   │
│  H │ Multi-step generation            │ 7     │ H1, H2, H4 (3/7)           │
│  I │ State manipulation               │ 8     │ I1 (1/8)                   │
│  J │ Substrate-side (anima)           │ 6     │ J1, J2, J3 (3/6)           │
│  K │ Confidence / uncertainty         │ 5     │ 0/5                        │
│  L │ Cross-prompt                     │ 5     │ 0/5                        │
│  M │ Meta                             │ 3     │ M1, M2 (2/3)               │
├────┼──────────────────────────────────┼───────┼────────────────────────────┤
│ TOTAL                                  │ 94    │ 35/94 measured (37%)       │
└────┴──────────────────────────────────┴───────┴────────────────────────────┘
```

→ **94 axis items × ~37% 측정 완료** (was 19% before P1+P2 sweep). **59 items unmeasured**.

---

## 📊 P1+P2 axis exploration results (2026-05-12) — Phase 1A ckpt

비유: 27 mode 측정했지만 **모두 V5.8 PASS threshold (≥3/5) 미달**. saturation 의 한계.

### Ranking top 10 (27 new modes, V5.8 5-dialogue)

| rank | mode               | cat | n_pass | verdict |
|------|--------------------|-----|--------|---------|
| 🥇 1  | B1_T0.0_greedy     | B   | 2/5    | FAIL    |
| 🥈 2  | C_rep1.1_sample08  | C   | 2/5    | FAIL    |
| 🥉 3  | F1_eos_only_greedy | F   | 2/5    | FAIL    |
|  4   | F2_newline_greedy  | F   | 2/5    | FAIL    |
|  5   | F3_user_marker     | F   | 2/5    | FAIL    |
|  6-8 | E_beam2/4/8        | E   | 2/5    | FAIL    |
|  9   | H4_best_of_n5      | H   | 2/5    | FAIL    |

### Per-dialogue recall % (27 modes aggregate)

| dialogue   | recall %    | finding                                            |
|------------|-------------|----------------------------------------------------|
| anima_fact | 20/27 (74%) | substrate prior — "anima entity" 흔한 표현         |
| day        | 7/27  (26%) | "수요일" Korean date keyword                       |
| color      | 1/27   (4%) | H4 best-of-n5 only 1회 hit                          |
| profession | 0/27   (0%) | **catastrophic forget — 어떤 mode 도 recall 못함** |
| cosmology  | 1/27   (4%) | C_rep1.1_sample08 1회 sample 운                     |

### 핵심 발견

- 🟥 **PASS mode 0/27** — V5.8 threshold (≥3/5) 어느 axis 도 충족 못함
- 🟧 **profession 0%** — Phase 1A 가 직업 type recall 능력 부재 (corpus issue 의심)
- 🟨 **substrate prior dominant** — anima_fact 74% 가 SFT 결과 아니라 base substrate 의 cross-link
- 🟦 **sample T 단조 감소** — T=0.0 (2/5) > T=0.1-1.3 (1/5) > T=1.5/2.0 (0/5). 노이즈만 추가
- 🟪 **beam 등가** — beam=2/4/8 동일 result. greedy 와 같은 recall pattern
- 🟩 **strong rep_penalty (≥1.3) → markdown table 격자 출력 collapse** (불안정)
- ⚠️ **prior Phase 1A V5.8 4-mode (greedy 3/5) 와 1점 차이** — GPU (cu128 RTX 5070) vs Mac CPU fp32 argmax 비결정성, host 변경. 본 측정 self-consistent

### Honest interpretation

⚠️ **decoding axis 만으로 V5.8 PASS 달성 어려움**. corpus 개선 (Phase 1B) 또는 substrate 변경 (B'' FFN.gate cotrain 15/15 V4-lite winner) 가 더 효과적일 가능성.

⚠️ 본 saturation 측정은 **diminishing returns 한계** 확인 — H4 best-of-n 도 sample 운에 의존하여 color 가끔 hit 만 기여.

---

## 🥇 Priority recommendations (next exploration)

### High value × low cost (Mac CPU $0):
1. **Category B Temperature sweep** (10 levels × 5 dialogues × 2 substrates = 100 generations, ~30min)
2. **Category C Repetition control** (5 strengths × ~25min)
3. **Category F Stop conditions** (F3 "사용자:" stop 추가 — 5min impl + 측정)

### Medium value × medium cost ($0.50-2 Vast.ai):
4. **Category E Beam search** (beam=2/4/8 × dialogue, requires implementation)
5. **Category H Multi-step gen** (self-consistency, best-of-n — quick impl)
6. **Category K Confidence sample-rerank** (gen + rerank by likelihood)

### Long-term (next cycle):
7. **Category D Constraints** (regex grammar, outlines library)
8. **Category I State manipulation** (attention edit, layer freezing)
9. **Category L Cross-prompt** (speculative decoding, MoE gate)

---

## 🛤️ Implementation path

```
Phase 2.0 (immediate, $0):
  B+C+F sweep → V5.8 × ~20 modes (currently 4)
  Mac CPU, ~1-2h
  → 발견: optimal temperature, optimal rep_penalty, stop condition impact

Phase 2.1 (short, $1-2):
  E beam search + H best-of-n
  Vast.ai $0.50 fast test
  → 발견: beam search 가 substrate A 에 잘 맞는지

Phase 2.2 (mid, $5-10):
  K confidence rerank + D constraints
  → production-grade chat quality

Phase 2.3 (long):
  L cross-prompt techniques (speculative decoding 등)
```

---

## 🧪 Honest concerns

⚠️ **94 axes 의 over-saturation 위험**: 모든 axis 가 의미 있는 것 아님. Phase 1A V5.8 std_greedy 3/5
가 이미 좋은 quality. axis 탐색은 **diminishing returns** — top 10-20% modes 만 측정해도 충분.

⚠️ **measurement cost**: 94 modes × 5 dialogues × 2 modes (T) = 940 generations × 60s Mac CPU = ~16h.
실용성 위해 **선택적 sampling** 권고.

⚠️ **Goodhart's law**: V5.8 만 측정해서 V5.8 만 PASS 되도록 over-tune 시, 다른 quality metric 손상
가능. multi-metric eval (V4 + V5 + V5.8 + 사람 평가) 필요.

---

## 🔗 Cross-link

- `PASS_STRICT_SPONTANEOUS_CHAT.md` §7 (V5.8 × 4 modes baseline)
- `PASS_STRICT_SPONTANEOUS_CHAT.md` §10 (Phase 1A 결과)
- prior 20-BG archive BG-JP: 14 strategies — partially overlaps Categories A+B+C+D
- nexus drill (kick) 시도: cwd_unmappable + stdlib path issue (deferred)

