# anima corpus Q1 + Q2 stream filter spec — iter6

**Date**: 2026-05-08
**Cycle**: anima cycle 2026-05-08 iter6 task (c-redirected)
**Predecessor**: `docs/anima_corpus_iteration_iter5_2026_05_08.ai.md` (Q1–Q5 inventory + quality issues)
**Scope**: spec only — no file rewrite this iter (cost discipline). Apply on user directive.
**Trinity**: D-axis (D1 SCOPE_CLAMP enforce) / own-axis (mandate-2 wrapping 0) / H-axis (preserve iter5 quality findings, no regression)

---

## 1. Marker confirmation (read-only inspection)

Target file: `state/anima_persona_tier_a_2026_05_08.txt` (104 MB, 1,478,588 lines; gitignore L317-318, 326)

### Q1 — `config/core_rules.json` schema bleed (HIGH)

| Property | Value |
|---|---|
| First line of contaminated block | **1,478,043** |
| Block header | `=== SOURCE: config/core_rules.json \| char_density=0.6796% sem_sets=5/6 ===` |
| Last line of file | 1,478,588 |
| Span | **546 lines** (1,478,043 → 1,478,588 inclusive) |
| Preceding context | line 1,478,042 is blank; 1,478,041 ends the prior `emerge_paradigm.spec.yaml` block |
| Pollution surface | full JSON dump: `_meta`, `principles.P1–P4`, `ossification_layers.L0–L2`, `protected_paths`, `relationship.code_vs_assets`, `ssot.{code_rules,asset_status,conformance}` |

Marker uniqueness: the literal `=== SOURCE: config/core_rules.json` appears exactly **once** in the file (line 1,478,043) — single anchor, no false positives.

### Q2 — `[augmented]` persona-augmented + KMMLU multi-choice (MED)

| Pattern | Count | Notes |
|---|---|---|
| Lines containing `[augmented]` | **16,456** | Embedded in `사용자:` lines; persona-style augmented prompts ("Take a moment, then answer:", "Reflecting on your own architecture,", etc.) |
| Lines containing `다음 문제의 정답을 고르시오` | **7,298** | Canonical KMMLU MC stem (electrical / civil / biotech / chemistry domains) |
| Block format | 7-line variable | `[anima 역할: ...]` header → `사용자:` stem → blank → question prose → blank → `1) … 2) … 3) … 4) …` → `도우미: N번: …` → blank |

Single-line removal would orphan the surrounding question prose, MC options, and `도우미` answer. A **block-aware filter** is required.

### Block boundary anchor

Every persona-corpus dialogue (KMMLU and clean alike) is delimited by the line `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]` (or close variants — 129,075 occurrences total per iter5 §2). Blocks end at the blank line following the `도우미:` line. Between two `[anima 역할: …]` headers is exactly one dialogue turn.

---

## 2. Filter spec (0-cost stream, no rewrite this iter)

### 2.1 Q1 strip (single anchor, head-only)

Pure prefix-truncate to line 1,478,042:

```bash
awk 'NR < 1478043' \
  state/anima_persona_tier_a_2026_05_08.txt \
  > state/anima_persona_tier_a_v2_2026_05_08.txt
```

Removes 546 lines. Anchor verified by line-number AND header-string redundancy:

```bash
# Equivalent grep-anchored variant (defensive — if line numbers shift):
sed -n '1,/^=== SOURCE: config\/core_rules\.json/{/^=== SOURCE: config\/core_rules\.json/!p}' \
  state/anima_persona_tier_a_2026_05_08.txt \
  > state/anima_persona_tier_a_v2_2026_05_08.txt
```

### 2.2 Q2 strip (block-aware awk, two-pattern OR)

```bash
awk '
  BEGIN { buf=""; drop=0 }
  /^\[anima 역할:/ {
    if (buf != "" && !drop) printf "%s", buf
    buf = $0 ORS
    drop = 0
    next
  }
  {
    buf = buf $0 ORS
    if (index($0, "[augmented]") > 0) drop = 1
    if (index($0, "다음 문제의 정답을 고르시오") > 0) drop = 1
  }
  END {
    if (buf != "" && !drop) printf "%s", buf
  }
' state/anima_persona_tier_a_v2_2026_05_08.txt \
  > state/anima_persona_tier_a_v3_2026_05_08.txt
```

Logic: accumulate every block delimited by `[anima 역할:` headers; on header boundary, emit the accumulated buffer **only if** no contamination marker was seen inside; reset and start a new buffer.

### 2.3 Combined one-shot (Q1 + Q2 fused)

```bash
awk '
  NR == 1478043 { exit_now = 1 }
  exit_now { exit }
  /^\[anima 역할:/ {
    if (buf != "" && !drop) printf "%s", buf
    buf = $0 ORS; drop = 0; next
  }
  { buf = buf $0 ORS
    if (index($0, "[augmented]")) drop = 1
    if (index($0, "다음 문제의 정답을 고르시오")) drop = 1 }
  END { if (buf != "" && !drop) printf "%s", buf }
' state/anima_persona_tier_a_2026_05_08.txt \
  > state/anima_persona_tier_a_v3_2026_05_08.txt
```

Cost: ~3–6 sec stream (104 MB sequential). Memory: O(1 block) ≈ ≤ 4 KB peak buffer.

---

## 3. Expected output line count

| Stage | Lines | Δ |
|---|---|---|
| Source `tier_a` | 1,478,588 | (baseline) |
| After Q1 strip | 1,478,042 | −546 |
| After Q2 `[augmented]` block strip | ≈ 1,412,000 | −66,000 (16,456 marker lines × ~4 lines/block; some overlap with KMMLU) |
| After Q2 KMMLU stem block strip | ≈ 1,361,000 | −51,000 (7,298 marker lines × ~7 lines/block) |
| **Final v3** estimate | **≈ 1,361,000** | **−117,588 (≈ 8.0% reduction)** |

Conservative estimate: brief stated `1,478,588 − 546 − 16,456 = 1,461,586` assuming single-line drops. Block-aware filter removes more (full dialogue turn around each marker), which is the **correct** semantic — orphan question/option lines must not survive. Exact post-filter count to be verified empirically when applied.

Size estimate: ~95 MB → ~88 MB (uncompressed UTF-8).

---

## 4. Application procedure (deferred — user directive required)

1. Pre-flight: confirm `state/anima_persona_tier_a_2026_05_08.txt` SHA256 matches iter5 inventory baseline (no upstream mutation since 2026-05-08 iter5).
2. Run §2.3 fused awk; redirect to `state/anima_persona_tier_a_v3_2026_05_08.txt`.
3. Verify post-conditions:
   - `wc -l v3` ≈ 1,361k ± 5k
   - `grep -c "config/core_rules.json" v3` == 0
   - `grep -c "\\[augmented\\]" v3` == 0
   - `grep -c "다음 문제의 정답을 고르시오" v3` == 0
   - `grep -c "^\\[anima 역할:" v3` ≈ 105k (down from 129,075; block-drop accounting)
4. Update `.gitignore` — pattern `state/anima_*_persona_*.txt` (L317) + `state/anima_*_tier_*.txt` (L326) already covers `tier_a_v3`. **No gitignore edit needed** — verified.
5. Hand-off to next training run as superseding artifact; retain v1 for audit trail until v3 consumed by ≥ 1 successful BG run.

 mandate-2 destination obligation: v3 corpus uploaded to `dancinlab/anima-corpus-tier-a` HF dataset (not git). Local-only retention until HF push.

---

## 5. own-axis confirmations

- cost discipline: held — 0 LLM calls, 0 file rewrites, only doc commit (this file, < 10 KB).
- mandate-2 wrapping 0: held — corpus files never staged, never committed; this doc only.
- mandate-2: held — gitignore patterns L307–328 confirmed cover all tier_a_v* + persona_* + corpus_* artifacts.
- visibility lifecycle: not relevant (no HF promote action this iter).
- D1 SCOPE_CLAMP: this filter ENFORCES D1 by removing infrastructure-metadata bleed (Q1) before training surface absorption.

---

## 6. Out-of-scope (deferred)

- Q3 preference-pair prompt diversity (needs LLM gen budget, see iter5 §3 Q3 / §4 step 3).
- Q4 bare-string vs chat-template wrap (separate regex pass on `.jsonl`, not this filter's scope).
- Q5 factuality tag schema bump (downstream training script change required).
- KOBEST-like `다음 지문을 읽고 질문에 참/거짓` contamination (1,110 lines, parallel signal to Q2; not in iter5 Q2 mandate but candidate for iter7 Q2-extended).

## 7. next_action

User directive `OK APPLY Q1+Q2 FILTER` → execute §2.3 awk + §4 verification → emit `tier_a_v3` snapshot + write iter6-applied report. Until then: spec frozen, source corpus untouched.
