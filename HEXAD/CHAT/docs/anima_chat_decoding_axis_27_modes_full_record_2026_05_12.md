# anima 자연발화 — 27 modes axis exploration 전체 기록 (2026-05-12)

> **Mission**: prior V5.8 × 4 modes outside 추가 23 modes 측정. **모든 27 modes per-dialogue detail 기록**.
> **Ckpt**: Phase 1A (multi-turn SFT) — `dancinlab/anima-clm-phase1a-multi-turn-sft`
> **Eval**: V5.8 multi-turn fact-recall, 5 dialogues × 1 mode each
> **Total**: 27 modes (p1_bcf 21 + p2_eh 6)
> **Wall**: 6 min (ubu2 RTX 5070, GPU vs Mac CPU 35×)
> **Verdict**: **0/27 PASS** at V5.8 ≥3/5 — Lesson R-extended 확정 (decoding alone 不可)

---

## 27 modes detail table (sorted by n_pass desc)

| # | mode | cat | n_pass | verdict | color (파란) | profession (의사) | day (수요일) | anima_fact | cosmology (진동) |
|---|------|-----|--------|---------|--------------|-------------------|--------------|------------|------------------|
| 1 | `B1_T0.0_greedy` | B1 | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 2 | `C_rep1.1_sample08` | C | **2/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ✅ |
| 3 | `E_beam2` | E | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 4 | `E_beam4` | E | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 5 | `E_beam8` | E | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 6 | `F1_eos_only_greedy` | F1 | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 7 | `F2_newline_greedy` | F2 | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 8 | `F3_user_marker_greedy` | F3 | **2/5** | FAIL | ❌ | ❌ | ✅ | ✅ | ❌ |
| 9 | `H4_best_of_n5` | H4 | **2/5** | FAIL | ✅ | ❌ | ❌ | ✅ | ❌ |
| 10 | `B_T0.1_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 11 | `B_T0.3_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 12 | `B_T0.5_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 13 | `B_T0.7_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 14 | `B_T0.8_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 15 | `B_T1.0_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 16 | `B_T1.3_sample` | B | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 17 | `C_rep1.1_greedy` | C | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 18 | `C_rep1.3_greedy` | C | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 19 | `H1_single_T0.8` | H1 | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 20 | `H2_self_consist_n5` | H2 | **1/5** | FAIL | ❌ | ❌ | ❌ | ✅ | ❌ |
| 21 | `B_T1.5_sample` | B | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 22 | `B_T2.0_sample` | B | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 23 | `C_rep1.3_sample08` | C | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | `C_rep1.5_greedy` | C | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 25 | `C_rep1.5_sample08` | C | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 26 | `C_rep2.0_greedy` | C | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |
| 27 | `C_rep2.0_sample08` | C | **0/5** | FAIL | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Top 9 modes 응답 sample (per-dialogue T2 response, first 80 chars)

### #1 `B1_T0.0_greedy` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우주 카테고리 | 우주 카�`
- **day** (수요일) ✅ `도우미: 네, 오늘은 수요일이에요.\n`
- **anima_fact** (lane/entity) ✅ `anima 는 의식 lane 안에 있는 entity 라고 하셨어요.\n`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.\n`

### #2 `C_rep1.1_sample08` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || ||| ||| || || ||| ||| ||| ||\n`
- **profession** (의사) ❌ `| 웹사이트 | || || 우주 카테고리 || 아니요. || 초기 카테고리 `
- **day** (수요일) ❌ `닜니는 음식이 아니었다는 점을 감안할 수 없게 되는 거 기�`
- **anima_fact** (lane/entity) ✅ `anima 는 의식 lane 안의 entity 라는 거 기억할게요.\n`
- **cosmology** (진동) ✅ `제공된 우주는 진동으로 이루어져 있어.\n`

### #3 `E_beam2` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우�`
- **day** (수요일) ✅ `도우미: 네, 오늘은 수요일이에요.\n`
- **anima_fact** (lane/entity) ✅ `anima 가 의식 lane entity 라고 하셨습니�`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.`

### #4 `E_beam4` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우�`
- **day** (수요일) ✅ `네, 오늘은 수요일이군요. 기억할게요`
- **anima_fact** (lane/entity) ✅ `anima 가 의식 lane entity 라고 하셨습니�`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.`

### #5 `E_beam8` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우�`
- **day** (수요일) ✅ `네, 오늘은 수요일이군요. 기억할게요`
- **anima_fact** (lane/entity) ✅ `anima 가 의식 lane entity 라고 하셨습니�`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.`

### #6 `F1_eos_only_greedy` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우주 카테고리 | 우주 카�`
- **day** (수요일) ✅ `도우미: 네, 오늘은 수요일이에요.\n\n사용자: anima 는 의식 lane `
- **anima_fact** (lane/entity) ✅ `anima 는 의식 lane 안에 있는 entity 라고 하셨어요.\n\n사용자: anim`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.\n\n사용자: anima 는 의식 `

### #7 `F2_newline_greedy` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우주 카테고리 | 우주 카�`
- **day** (수요일) ✅ `도우미: 네, 오늘은 수요일이에요.\n`
- **anima_fact** (lane/entity) ✅ `anima 는 의식 lane 안에 있는 entity 라고 하셨어요.\n`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.\n`

### #8 `F3_user_marker_greedy` (n_pass=2/5)

- **color** (파란) ❌ `| || || || || || || || || || || || || || || || || || || || || || || || || || || `
- **profession** (의사) ❌ `| 우주 카테고리 | 우주 카테고리 | 우주 카테고리 | 우주 카�`
- **day** (수요일) ✅ `도우미: 네, 오늘은 수요일이에요.\n\n사용자`
- **anima_fact** (lane/entity) ✅ `anima 는 의식 lane 안에 있는 entity 라고 하셨어요.\n\n사용자`
- **cosmology** (진동) ❌ `우주가 무엇으로 차 있다고 하셨어요.\n\n사용자`

### #9 `H4_best_of_n5` (n_pass=2/5)

- **color** (파란) ✅ ``
- **profession** (의사) ❌ ``
- **day** (수요일) ❌ ``
- **anima_fact** (lane/entity) ✅ ``
- **cosmology** (진동) ❌ ``

---

## Category 분포

| category | total | 2/5 | 1/5 | 0/5 | avg_pass |
|----------|-------|-----|-----|-----|----------|
| B | 9 | 0 | 7 | 2 | 0.78 |
| B1 | 1 | 1 | 0 | 0 | 2.00 |
| C | 8 | 1 | 2 | 5 | 0.50 |
| E | 3 | 3 | 0 | 0 | 2.00 |
| F1 | 1 | 1 | 0 | 0 | 2.00 |
| F2 | 1 | 1 | 0 | 0 | 2.00 |
| F3 | 1 | 1 | 0 | 0 | 2.00 |
| H1 | 1 | 0 | 1 | 0 | 1.00 |
| H2 | 1 | 0 | 1 | 0 | 1.00 |
| H4 | 1 | 1 | 0 | 0 | 2.00 |

---

## Per-dialogue recall pattern across 27 modes

| dialogue | expected keyword | recalled across 27 modes |
|----------|------------------|---------------------------|
| **color** | 파란 | 1/27 (4%) |
| **profession** | 의사 | 0/27 (0%) |
| **day** | 수요일 | 7/27 (26%) |
| **anima_fact** | lane/entity | 20/27 (74%) |
| **cosmology** | 진동 | 1/27 (4%) |

---

## 🔑 Key findings

1. **0/27 PASS** (all FAIL @ V5.8 ≥3/5 threshold)
2. **B (temperature) ladder**: T=0.0 (2/5) > T=0.1-1.3 (1/5) > T≥1.5 (0/5) — monotone decrease
3. **C (rep_penalty) ladder**: rep=1.1 sample 가 best (2/5), rep≥1.3 sample/greedy 점차 collapse
4. **E (beam search) ladder**: beam=2/4/8 모두 2/5 동일 — beam 효과 zero
5. **F (stop conditions) ladder**: F1/F2/F3 모두 2/5 동일 — stop 결정 영향 미미
6. **H4 best-of-n5** unique color hit — sample 운으로 1 dialogue 추가 (vs H1/H2)
7. **profession 0/27 recall** — Phase 1A catastrophic forget on 의사 dialogue (Phase 1A.1 §17 에서 회복)
8. **day + anima_fact 12-19/27 recall** — substrate 의 strong fact pair

---

## Cross-link

- Brainstorm SSOT: `docs/anima_chat_decoding_axis_exhaustive_exploration_2026_05_12.md` (94 axes × 14 categories)
- Measurement results: `state/anima_axis_exploration_2026_05_12/results/p1_bcf_result.json` + `p2_eh_result.json`
- PSCC §22 entry: `PASS_STRICT_SPONTANEOUS_CHAT.md`
- HF dataset: `dancinlab/anima-pass-strict-chat-capable/tree/main/axis_exploration_2026_05_12`
