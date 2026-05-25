# HXC Composite Chain — Option C A25-aware Routing (Design Delta)

**Date**: 2026-04-29
**Author**: anima/cyborg-eeg-core (composite-chain-pivot agent)
**Status**: PASS 1 design delta (skeleton + selftest follow in PASS 2/PASS 3)
**Disjoint from**: `docs/hxc_composite_chain_design_2026-04-29.md` (Option A
linear, 728 lines; LANDED)
**Module target**: `anima/tool/hxc_composite_chain_v_c.hexa` (NEW — does NOT
modify Option A `hxc_composite_chain.hexa`).

raw 9 hexa-only · raw 33 English commit + witness · raw 47 no-inflation · raw
65/68 round-trip · raw 71 falsifier preregister · raw 91 honest C3 STRICT ·
raw 92 sigil-line · raw 137 cmix-ban · raw 142 D2 try-revert · raw 156
placement-axis · raw 157 printable wire.

---

## 0. TL;DR

Option A linear chain (5-stage A35→A1..A15→A18 v6→A29 v3→A34 v2) was
SKELETON-IMPLEMENTED in PASS 2 (commit `1f9871a45`,
`tool/hxc_composite_chain.hexa`, 789 LoC). Selftest 9-fixture verdict:

```
chain  90.21% aggregate saving (in-sample, 9 fixtures)
A18 v6 92.03% standalone best
A29 v3 91.83% standalone
A34 v2 87.91% standalone
F-CHAIN-2 TRIPPED: chain - best_single = -1.82pp
```

Per-fixture trace shows ONLY Stage 3 (A18 v6) ever fires "active" — Stages 1
(A35), 2 (A1..A15), 4 (A29), 5 (A34) all `mode=identity` because A18 v6 LZ77
output is entropy-dense and downstream stages cannot lift further. The chain
loses to standalone A18 v6 by exactly the manifest-header overhead (5
per-stage manifest lines + envelope sigil ~ 500-600 B fixed, amortized poorly
against 4KB fixtures).

**Architectural pivot**: per-class deterministic switch chooses the single
best algorithm per class, paying ONE manifest line instead of FIVE. Saving
target = single-stage best per class (in-sample) — Option C aims for parity
or lift, NOT multiplicative chain gain.

---

## 1. Failure analysis — why Option A linear underperformed

### 1.1 Manifest header overhead

Option A header schema (`anima/tool/hxc_composite_chain.hexa:307-321`):

```
# cc2:s2 v=composite-v2 chain=A n=<N> stages=5
# cc2:stage1 mode=<m> sigil=^o param=<json>
# cc2:stage2 mode=<m> family=A1..A15 param=<json>
# cc2:stage3 mode=<m> sigil=^a18 param=<json>
# cc2:stage4 mode=<m> family=_a29v3 param=<json>
# cc2:stage5 mode=<m> sigil=^l param=<json>
^d<body-escaped>
```

Empirical measurement on F1 (4KB text):
- standalone A18 v6 wire: 397 B → saving 90.31%
- chain wire: 915 B → saving 77.66%
- delta: 518 B = manifest header (5 per-stage lines + envelope sigil + body
  escaping inflation) on a fixture where ONLY stage 3 contributes.

Header overhead amortizes asymptotically as N→∞ but in-sample 4-64 KB
fixtures pay 0.8-12.6% saving penalty.

### 1.2 Stage-3 dominance + downstream blocking

A18 v6 output is high-entropy LZ77 wire (literals + length/distance codes).
Per-fixture trace confirms:

| Fixture | s1 | s2 | s3 | s4 | s5 |
|---------|-----|-----|-----|-----|-----|
| F1..F9 (all 9) | identity | identity | active | identity | identity |

Stages 4 (A29 v3 Huffman) and 5 (A34 v2 sub-byte AC) consistently fail their
inner D2 try-revert (`enc_len >= n`) because A18 v6 LZ77 is already entropy-
dense. The 3-axis orthogonality assumption (raw 156) was sound IN THEORY but
empirically Stage 3 saturates the available bits before Stages 4/5 can
contribute.

### 1.3 Per-class single-stage best (in-sample 9-fixture)

| Class | Best | Saving |
|-------|------|--------|
| text-heavy (F1-F3) | A18 v6 | 92-98% |
| json-heavy (F4-F6) | A29 v3 | 79-91% (A29 wins F4/F5/F6 vs A18) |
| mixed (F7-F9) | A18 v6 | 84-93% |

A29 v3 beats A18 v6 on json-heavy fixtures by 1-7 pp consistently. A18 v6
beats A29 v3 on text-heavy and mixed. This is the empirical signal Option C
exploits.

---

## 2. Option C routing matrix

A25 v2 type-aware classifier
(`/Users/ghost/core/hexa-lang/self/stdlib/hxc_a25_type_aware.hexa`, 1065 LoC)
reads the input and emits a `class=<tag>` line. Option C reads ONLY the class
tag and routes to a fixed single-stage AOT call.

### 2.1 Class → primary path

| A25 class tag | Route | Algorithm | AOT path |
|---|---|---|---|
| `text-heavy` | TEXT | A18 v6 standalone | `.hxc_aot/hxc_a18` |
| `json-heavy` | JSON | A29 v3 standalone | `.hxc_aot/hxc_a29 --v3` |
| `mixed` | MIXED | A18 v6 standalone | `.hxc_aot/hxc_a18` |
| `struct-audit` | STRUCT | A18 v6 standalone | `.hxc_aot/hxc_a18` |
| `synthetic-repetitive` | SYN | A24 standalone | `.hxc_aot/hxc_a24` |
| `passthrough` (small / unclassifiable) | NONE | identity | (no call) |

A25 may also tag `schemaful-jsonl-subset` IF schema detection fires (deferred
— Option C v_c PASS 2 skeleton: schemaful subset → JSON route as default;
A35 pre-A1 transform integration deferred to follow-up PASS conditional on
A35 v2 LIVE FIRE landing).

### 2.2 Routing decision logic (deterministic switch — raw 137 cmix-ban
compliant)

```
Stage 0: A25 v2 classify (sigil + class tag)        — read-only AOT call
Stage 1: per-class route to primary algorithm        — single AOT call
Stage 2 (deferred): A35 v2 pre-A1 transform IF
         class=schemaful-jsonl-subset AND A35 AOT
         available AND PASS 5 schemaful-only lift    — NOT integrated v_c PASS 2
```

Decision is a fixed `switch(class) → algo`. NOT a mixer (no weighted sum of
multiple model outputs). raw 137 cmix-ban grep audit: `mixer|blend|
convex_combination|weighted_sum` = 0 hits in module source.

### 2.3 Try-revert semantics (Option C class-aware D2)

Two-level revert:

1. **Per-class route revert**: chain wire (manifest + algo wire) >= input →
   identity passthrough (top-level D2). Mirrors raw 142 D2 strict mode.
2. **Algo failure revert**: AOT call returns non-zero or output >= input →
   identity passthrough at envelope level.

Junction count is ZERO (single algo invocation per class — no inter-stage
junction). This eliminates F-CHAIN-7 (try-revert ordering bug) by
construction.

---

## 3. Module structure

### 3.1 Envelope wire format

```
# cc_c:s2 v=composite-v_c class=<tag> route=<algo> n=<N>
# cc_c:route mode=<active|identity> sigil=<algo_sigil> param=<json>
^d<body-escaped>
```

- 2 manifest lines (vs Option A's 6) → 4× header overhead reduction.
- `v=composite-v_c` disjoint from `v=composite-v2` (Option A) and
  `v=composite-v1` (2026-04-28 A29+A30+A23 chain). Decode dispatcher reads
  `v=` field to disambiguate.
- Body is escaped algo wire (newlines + backslashes).

### 3.2 Decode flow

1. Parse manifest (2 lines + `^d` body line).
2. Read `class=` and `route=` from header.
3. Read `mode=` from route line.
4. If `mode=identity` → return body unchanged (passthrough).
5. If `mode=active` → unescape body, call `<algo> decode`, return result.

### 3.3 Module file

- Path: `/Users/ghost/core/anima/tool/hxc_composite_chain_v_c.hexa`
- Target LoC: ~700 (single algo dispatch is simpler than 5-stage chain).
- Sigil: `^d` envelope (shared with Option A; disambiguation via `v=` field).
- AOT target: `/Users/ghost/core/anima/.hxc_aot/hxc_composite_chain_v_c`.

### 3.4 Read-only dependencies (DO NOT modify)

- `/Users/ghost/core/anima/.hxc_aot/hxc_a25` — A25 v2 classifier
- `/Users/ghost/core/anima/.hxc_aot/hxc_a18` — A18 v6 LZ77+PPM
- `/Users/ghost/core/anima/.hxc_aot/hxc_a29` — A29 v3 length-codes Huffman
- `/Users/ghost/core/anima/.hxc_aot/hxc_a24` — A24 grammar PCFG (synthetic)

NOT integrated this PASS:
- `hxc_a33` — PASS 5 in-flight, do not modify
- `hxc_a34` — production FALSIFIED (-5.53pp vs A29 v3, RSS jetsam)
- `hxc_a35` — schemaful subset only, LIVE FIRE in-flight

---

## 4. raw 156 placement-axis declaration

Option C does NOT compose multiple placement axes — it deterministically
selects ONE axis per class:

| Class | Axis |
|---|---|
| text-heavy / mixed / struct-audit | axis #1 (cross-file LZ77) via A18 v6 |
| json-heavy | axis #4 (byte-Huffman) via A29 v3 — NOT one of verdict's 3 paths |
| synthetic-repetitive | grammar PCFG (A24) — outside 3-axis verdict |

Axis #2 (sub-byte) NOT integrated — A34 production FALSIFIED.
Axis #3 (source H_n) NOT integrated — A35 schemaful-only, deferred.

This is intentionally NOT the 3-axis-multiplicative claim of Option A. Option
C is the **per-class best-single fallback** when 3-axis composition fails its
F-CHAIN-2 falsifier.

---

## 5. F-CHAIN-V_C-1..6 falsifier preregistration (raw 71)

### 5.1 F-CHAIN-V_C-1 — round-trip byte-eq fail

**Trip condition**: any 9-fixture `decode(encode(x)) != x`.
**Impact**: critical — wire is broken, abandon module.
**Mitigation**: byte-eq selftest mandatory PASS 2 gate.

### 5.2 F-CHAIN-V_C-2 — Option C aggregate < single-stage best

**Trip condition**: aggregate saving over 9 fixtures < max(A18, A29, A24)
standalone aggregate.
**Impact**: high — Option C provides no lift over picking the global best
single algorithm. Manifest overhead unjustified.
**Honest C3**: if F-CHAIN-V_C-2 trips, Option C ALSO falsified — pivot
abandoned and Option A linear remains the documented composite skeleton with
F-CHAIN-2 already TRIPPED (i.e., NEITHER chain approach beats picking the
right standalone algorithm).
**Mitigation**: per-class routing should at least match best-single-per-
class. PASS 2 verdict test.

### 5.3 F-CHAIN-V_C-3 — A25 mis-classification produces inverted lift

**Trip condition**: A25 routes a json-heavy fixture to A18 (or vice-versa)
AND the wrong-route saving is < right-route saving by >= 5pp on any
fixture.
**Impact**: medium — class boundary is fuzzy. Mitigation via top-level D2
revert (if route hurts net, identity passthrough wins). But hurts saving.
**Mitigation**: log A25 class tag per fixture in selftest ledger; manual
audit. PASS 4 LIVE FIRE will widen exposure.

### 5.4 F-CHAIN-V_C-4 — manifest decode-side ambiguity

**Trip condition**: `v=composite-v_c` parser accidentally accepts
`v=composite-v2` or `v=composite-v1` wires (or vice-versa), producing wrong
decode dispatch.
**Impact**: critical — silent corruption.
**Mitigation**: exact-string compare on `v=composite-v_c`; mismatch → return
input unchanged (passthrough). PASS 2 selftest cross-check: encode with
Option A skeleton, attempt decode with Option C skeleton → MUST refuse.

### 5.5 F-CHAIN-V_C-5 — RSS budget exceeded (raw 42 mac jetsam)

**Trip condition**: any selftest fixture causes RSS > 100 MB measured by
external probe.
**Impact**: high — production block.
**Mitigation**: 9-fixture max 64 KB << 100 MB; PASS 2 not at risk. PASS 4
LIVE FIRE 5MB stratified will measure; deferred.

### 5.6 F-CHAIN-V_C-6 — raw 137 cmix-ban grep violation

**Trip condition**: source contains `mixer\|blend\|convex_combination\|
weighted_sum\|softmax_combine` matching code paths (NOT comments).
**Impact**: high — architectural violation, design must be revised.
**Mitigation**: PASS 2 audit step `grep -nE 'mixer|blend|
convex_combination|weighted_sum' tool/hxc_composite_chain_v_c.hexa` →
expected 0 hits in code (comment refs allowed for documentation purposes
explicitly stating "NOT a mixer").

### 5.7 Falsifier matrix — Option A vs Option C

| Falsifier | Option A | Option C |
|---|---|---|
| Round-trip byte-eq | F-CHAIN-1 | F-CHAIN-V_C-1 |
| chain < best_single | F-CHAIN-2 (TRIPPED) | F-CHAIN-V_C-2 (PASS 2 verdict) |
| Manifest ambiguity | F-CHAIN-3 | F-CHAIN-V_C-4 |
| File-order dep (A33) | F-CHAIN-4 (N/A — A33 not used) | N/A — no A33 |
| RSS 300MB | F-CHAIN-5 (deferred) | F-CHAIN-V_C-5 |
| Latency 2000ms/KB | F-CHAIN-6 (deferred) | (deferred) |
| Try-revert ordering | F-CHAIN-7 (N/A linear) | N/A by construction |
| cmix-ban | F-CHAIN-8 | F-CHAIN-V_C-6 |
| A25 mis-classify | (n/a — no classifier) | F-CHAIN-V_C-3 (NEW) |

---

## 6. PASS roadmap

| PASS | Scope | Status |
|---|---|---|
| 1 | This design delta doc | LANDED (this commit) |
| 2 | Skeleton ~700 LoC + 9-fixture selftest + ledger | THIS TURN |
| 3 | AOT byte-identical via hexa.real self/main.hexa build | THIS TURN (best-effort; bypass if hexa.real fails) |
| 4 | LIVE FIRE 5MB stratified per-class measurement | DEFERRED — gated on PASS 2 ≥ best-single |
| 5 | A35 schemaful subset integration | DEFERRED — gated on A35 v2 LIVE FIRE landing |
| 6 | A33 cross-repo dict integration | DEFERRED — gated on A33 PASS 5 landing |

---

## 7. raw 91 honest C3 STRICT mandate

- in-sample 9-fixture only (3 classes × 3 sizes — same corpus as Option A
  skeleton for fair head-to-head).
- design projection: per-class routing matches best-single-per-class minus
  manifest overhead. Expected aggregate ≈ `max(A18_aggregate, A29_aggregate)
  - 2/N pp` where N = avg fixture bytes.
- 80% reachability NOT claimable (in-sample only; PASS 4 LIVE FIRE deferred).
- if Option C 9-fixture aggregate < max(A18, A29, A24) standalone aggregate
  → F-CHAIN-V_C-2 TRIPPED + Option C also falsified honest C3.
- if Option C ≥ best-single-aggregate → PASS 4 LIVE FIRE candidate (still
  deferred, NOT auto-promoted).

---

## 8. Disjoint operation guard

Concurrent in-flight workstreams (DO NOT modify):

- `hxc_a33` PASS 5 (cross-repo dict, fixed-array follow-on)
- `hxc_a34` v2 (production FALSIFIED, no further changes)
- `hxc_a35` v2 (schemaful subset LIVE FIRE)
- `hxc_composite_chain.hexa` (Option A linear, sigil ^d v=composite-v2)
- hexa upstream proposal (separate)

This module creates ONLY:
- `anima/docs/hxc_composite_chain_option_c_2026-04-29.md` (this doc)
- `anima/tool/hxc_composite_chain_v_c.hexa` (skeleton)
- `anima/state/format_witness/2026-04-29_composite_option_c_skeleton.jsonl`
  (witness ledger)

---

*End of design delta. Skeleton implementation follows in PASS 2.*
