---
id: H_9679
title: GRAMMAR × CONTENT factorial — C3 entity-permutation arm (does +0.20 mean content?)
tier: PROPOSED (DIRECTIONAL design · lab-full CONVERGENT · $0 corpus / GPU fire · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9679 (R3) — 형태 × 내용 2×2 직교화

**Origin.** `sidecar lab full` 2026-07-17 — **Sol §2** ("Shape/content orthogonalization")
and **Fable #3** (C3 entity-permutation) converge. DESIGN ONLY · DIRECTIONAL.

**Claim (one line).** The current C2 destroys **content AND word order at once**, so
MAIN−C2 (+0.20) cannot separate meaning from grammatical form — a **C3 arm (vocabulary
preserved · conjunction destroyed)** is required before the residual can mean anything.

## Mechanism (structural)
A conv byte-LM trivially absorbs local n-gram / punctuation / sentence-boundary /
repeated-template gradients. `ρ·form` rising is fully explained by those local statistics
alone. C2 (word-shuffle) destroys word identity ⟹ MAIN−C2 may be **lexical distribution**
= still the FORM family. Only an arm that **keeps the vocabulary and breaks the
conjunction** aims at content.

## Minimal decisive experiment (new `study-replay` flag)
```bash
anima-py corpus study-replay --transcript T.jsonl --corpus BASE.txt --out F \
  --study-frac 0.05 --reps 40 --seed ${S} --teacher-transform intact
#   ... --teacher-transform grammatical-fact-swap   # form kept · content destroyed
#   ... --teacher-transform template-scramble       # form destroyed · atoms kept
#   ... --teacher-transform word-shuffle            # both destroyed (= current C2)
```
| arm | 문장 형태 | 원래 내용 |
|---|---|---|
| A MAIN | 보존 | 보존 |
| B grammatical-fact-swap | 보존 | **파괴** |
| C template-scramble | **파괴** | 원자/키 보존 |
| D word-shuffle (현 C2) | 파괴 | 파괴 |

`grammatical-fact-swap` = derangement of entity/value inside the **same POS · length ·
punctuation template** ⟹ fluent but false sentences.

## Frozen falsifier (pre-registered)
- **content effect**: `(A−B)−(C−D) ≥ +0.15`, paired 95% CI lower bound `> 0`
- **form effect**: `(A−C)−(B−D) ≥ +0.15`
- **A≈B with only C/D low ⟹ the H_9520 residual is grammar, not meaning** (kills it).
- same-root candidate requires the content effect to appear in **both** the
  teacher-content probe ([[H_9678]]) and G1 addressability.

## Controls (≥2)
① C1 replay-only ② grammatical-fact-swap ③ template-scramble ④ unseen-fact sham.

## De-quantization note (Fable · cheaper than seeds)
`ρ·form = n_coherent/5` ⟹ resolution **0.2**; the residual is literally **one probe cell**.
**Probe-set expansion buys more power per unit cost than more seeds** — do it before any
multi-seed CPT.

## Cost · kill-list
corpus transform + audit **$0**; 4-arm multi-seed = **GPU (owner go · rent=spend)**.
Kill-list: **no hit** — this is causal decomposition of an observed residual, not a
natural-corpus XOR rescue.
