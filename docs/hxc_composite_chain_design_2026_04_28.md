# HXC Composite Chain Design — A29 + A30 + A23 Stack (Multi-Algorithm Pipeline)

**Date**: 2026-04-28
**Author**: anima research subagent (composite chain experiment scope)
**Mission anchor**: post-A29 v1 LIVE FIRE 61.99% / 78.65% gate residual 16.66pp; single-algorithm path saturated; min-of-N dispatcher exhausted; **composite chain (sequential algorithm stack on the SAME file)** = remaining axis to probe.
**Compliance**: raw 9 hexa-only · raw 18 self-host · raw 91 honest C3 STRICT · raw 92 sigil-line · raw 137 cmix-ban · raw 142 D2 try-revert · raw 156 placement-orthogonality · A28 TRANSCEND-FORBIDDEN
**Scope**: design + first-tick SKELETON only. **NO LIVE FIRE / NO 6-repo sweep / NO production deploy / NO catalog promotion.**
**Non-overlap**: a2c50860 (A29 v2 LIVE FIRE) + a8e5bf4d (A29 length codes); composite chain is a NEW module (`hxc_composite_chain.hexa`) with NEW sigil ^d, **read-only consuming** A29/A30/A23 modules.

---

## 0. Executive summary (TL;DR)

- 5 chain orderings surveyed (A29→A30, A30→A29, A23→A30, A30→A23, A29→A23).
- **Theoretical analysis**: every chain has TWO penalties — (i) base64url re-expansion (~33%) at every stage, (ii) header byte overhead (~80B per stage). For 1KB input, **2-stage chain net cost = ~+30% before any saving**. Chain wins ONLY if stage-2 saving on stage-1 output > 30% raw-cost-recovery threshold.
- **Pre-registered prediction (raw 71)**: across 5 chain orderings and 5 fixtures, **>= 4/5 chains will FAIL to outperform best single algorithm** (D2 try-revert hypothesis). The composite chain experiment is itself a **falsifier ledger entry**, NOT a saving claim.
- **2 candidate chains advanced for first-tick skeleton**:
  1. **C-PRIMARY: A29→A30** (DEFLATE LZ77+Huffman first, then BWT-MTF-RLE on the b64-decoded internal byte stream — **avoids double base64**). Theoretical lift +0..+3pp on text-heavy if A30 finds residual structure in DEFLATE bitstream byte-projection.
  2. **C-SECONDARY: A30→A23** (BWT clusters identical bytes → A23 sparse PPM exploits clustered context. Honest expectation: A30 -27pp underperform on natural text means A30 stage produces a longer intermediate, A23 must overcome both base-A30 loss and stage-2 overhead. **Expected D2 try-revert = identity** in most fixtures; included to falsify the "BWT context-clustering helps PPM" folk-hypothesis).
- Skeleton-level falsifier (raw 71): **F-CC-1** any chain encoded length >= identity → revert per raw 142 D2; **F-CC-2** round-trip non-byte-eq on any fixture → reject (raw 65 + 68); **F-CC-3** any chain output > best-single-algorithm output by > 5% → catalog as "chain-anti-lever, do not promote".
- Skeleton selftest **3/3** byte-eq round-trip on synthetic fixtures (English, Korean, JSON-mixed); production-class measurement DEFERRED.

---

## 1. Background — why composite chain now

### 1.1 The 80% target gap residual

Phase 13 P0 (A29 v1) closed at **61.99% MEASURED aggregate** post-LIVE FIRE on 6-repo sweep. The 78.65% raw-137-v8 gate was missed by **16.66pp**. Single-algorithm path is now SATURATED:

| Algorithm | Class winner | Lift on class | Aggregate effect |
|-----------|-------------|---------------|-----------------|
| A29 v1 DEFLATE | text-heavy | +2.09pp | +0.4pp aggregate (text-heavy is 19% weight) |
| A30 v1 BWT-MTF | (none — underperforms on natural text) | -27pp on natural English | -5.1pp aggregate (NEVER deployed in dispatcher) |
| A32 v1 static-Huffman | small-file <2KB | +1pp | +0.06pp aggregate (small-file is 6% weight) |
| A23 v1 sparse PPM | (Korean) | +0.81pp | +0.16pp aggregate (Korean is 20% weight) |
| A25 dispatcher (min-of-N) | per-file winner | aggregate 76.24% | (current SOTA) |

**Min-of-N dispatcher limit**: each algorithm's class winner is ALREADY captured. Adding more algorithms with the same per-file winner topology yields O(0) aggregate lift unless those algorithms own a NEW class (which Phase 14 candidates A33+ are exhausting).

### 1.2 The composite chain hypothesis

A composite chain runs algo_B on the OUTPUT of algo_A — not on the same raw file in parallel. The hope is:

> Algo_A produces an intermediate stream with structure that algo_B can exploit but the raw input did not expose.

**Example folk-claims** (literature-derived):

- **bzip2** (BWT→MTF→RLE→Huffman) — entire bzip2 algorithm IS a composite chain. The known wisdom: BWT-clustered byte stream is **highly compressible by entropy coders** because BWT permutes bytes into context-coherent groups.
- **zstd dictionary mode** — pre-trained dictionary + LZ77 chain. Different axis (dictionary is a static lookup), but proves chain composition is mainstream.
- **DEFLATE itself** — LZ77 → Huffman is a 2-stage chain inside one algorithm. A29 already does this internally.

### 1.3 What is genuinely NEW vs already-done

A29 (LZ77→Huffman) and A30 (BWT→MTF→RLE→Huffman-class entropy) are **already** internal multi-stage pipelines. Composite chain at the MODULE level (A29→A30) means running the *fully-encoded A29 wire* (header + sigil + base64url body) through A30 as if it were raw input. **This is qualitatively different** from internal multi-stage because:

1. **Interface mismatch**: A29's wire output is ASCII-printable base64url with header. A30 sees this as text-class, not as bitstream.
2. **Double base64 risk**: each stage emits b64 of an internal payload. Chained naively, the payload of stage-2 is a b64 string of (header + b64 of stage-1 payload). This is **provably anti-compressive** — b64 has 6 effective bits per byte with 8-bit envelope = 33% expansion baseline.

### 1.4 The honest C3 (raw 91) for composite chain

**Pre-registered honest expectation**: composite chain is **>=80% likely to FAIL the D2 try-revert (raw 142) gate** (i.e., chain output >= identity), at which point the composite_encode wrapper returns identity. The experiment is **valuable as falsification** (rules out chain-axis from Phase 14+ exhaustion) regardless of the verdict, per raw 71 + raw 142 + raw 91.

---

## 2. Survey — chain ordering candidates

### 2.1 Notation

Let `E_X(s)` denote algorithm X's encode wire (string→string) and `D_X(s)` its decode. Composite chain `Y∘X` is defined as:

```
encode_chain(s)  = E_Y(E_X(s))
decode_chain(z)  = D_X(D_Y(z))
```

Round-trip identity (raw 65/68): `D_X(D_Y(E_Y(E_X(s)))) == s`.

Header parse must be done by D_Y FIRST (its sigil is on the OUTSIDE), then D_X parses what's revealed.

### 2.2 Five candidate chain orderings

| Chain | Order | Hypothesis | Risk | Theoretical lift |
|-------|-------|------------|------|------------------|
| **C1** | **A29 → A30** | DEFLATE bitstream has periodic byte structure → BWT clusters it | Double-b64 cost ~+33% per stage | ±0% (high variance) |
| **C2** | A30 → A29 | BWT-clustered bytes → DEFLATE LZ77 finds longer matches | A30 wire is b64 — DEFLATE on b64 sees 6-bit alphabet structure | -2..+1pp |
| **C3** | **A30 → A23** | BWT context-clustering → A23 PPM order-5 exploits | A23 wire is order-1 byte coder; on b64 input, predicates collapse | -1..+1pp |
| **C4** | A23 → A30 | PPM-residual entropy → BWT permute → entropy | Triple-stage entropy = saturating return | -3..0pp |
| **C5** | A29 → A23 | DEFLATE residual → PPM order-5 | A23 v1 is order-1 only (order-5 is in-sample bits, not wire) | ±0pp |

### 2.3 Rejected orderings (raw 91 honest)

- **A23 → A29**: A23 wire is order-1 entropy-coded byte stream — already near Shannon for byte-level. A29 LZ77 finds matches of length>=3 in this byte stream — entropy floor blocks. **Anti-lever expected.**
- **A29 → A29 (self-stack)**: idempotent (raw 65/68) — A29's `if header == "# a29:s" { return text }` short-circuit prevents recursion. **Excluded.**
- **A30 → A30 (self-stack)**: same idempotency. **Excluded.**
- **3-stage A29 → A30 → A23**: design space exhausted; first-tick = 2-stage only.

### 2.4 Two surviving candidates → first-tick skeleton

After honest review:

- **C-PRIMARY = C1 (A29 → A30)**: DEFLATE first (proven +2.09pp text-heavy lift), then BWT on the *internal byte payload* (NOT the wire string). This requires composite_encode to **break the b64 envelope** between stages: extract A29's bitstream payload bytes, hand them to A30's `_a30_encode_force` directly, then re-wrap with composite header. **Avoids double base64 expansion.**
- **C-SECONDARY = C3 (A30 → A23)**: same internal-payload approach. A30's BWT-MTF-RLE byte stream → A23's order-5 sparse PPM in-sample bits (note: A23 v1 wire coder is order-1; pre-registered honest C3).

Both skeleton chains use **internal-payload composition** to dodge double-b64. Wire-level composition (string→string concatenation) is rejected as anti-compressive baseline.

---

## 3. Theoretical analysis

### 3.1 Base64url overhead model

Each stage's wire output is:
```
<header line>\n<sigil><base64url-body>\n
```

For input of N bytes:
- Header: ~50-80 bytes constant.
- Body: `b64_len = ceil(payload_bytes * 4 / 3)` ≈ `1.33 × payload_bytes`.

For internal-payload chain (C-PRIMARY/C-SECONDARY surviving form):
- A29 produces ~0.78N internal bytes (text-heavy class) + ~80B header overhead.
- Wrapped wire: header + ^a + b64(0.78N) ≈ 80 + 1.33 × 0.78N = 1.04N bytes.
- A30 on the **internal 0.78N bytes** (NOT the wrapped wire) — call this saving s2 (BWT effectiveness on a DEFLATE bitstream).
- Composite wire = 80 + 1.33 × (1 - s2) × 0.78N + 80 (one composite header).

Break-even s2 = `1 - 0.78 / (1.33 × 0.78)` ≈ 24.8% saving on the DEFLATE bitstream byte projection.

**Empirical sanity**: DEFLATE bitstream is approximately uniform byte distribution (entropy near 7.95 bits/byte by design). BWT/MTF/RLE on near-uniform bytes is **theoretically NULL-effect** (no clustering benefit on already-near-Shannon stream). Predicted s2 ∈ [-3%, +5%]. Therefore predicted composite NET = identity-revert in 4/5 cases.

### 3.2 Why A30→A23 (C-SECONDARY) is worth measuring

A30 produces an MTF-then-RLE byte stream BEFORE its order-1 entropy coder. The intermediate A30 byte stream IS clustered (BWT property) — A23's order-5 sparse PPM lookup-hit-rate metric should be MEASURABLY HIGHER on A30-BWT-clustered bytes than on raw text bytes. This is the **only theoretically defensible composite chain**:

- Hypothesis: A30 BWT byte stream has higher order-5 hit rate than raw text → A23 wire saving improves over A23-on-raw.
- Falsifier (F-CC-A30A23-1): hit_rate(A30(text)) <= hit_rate(text) → reject, fall back to identity.
- Caveat: A23 v1 wire is order-1, NOT order-5. Saving improvement is on the in-sample-bits estimator only this tick. To realize the saving in wire bytes, A23 v2 wire (order-5) must land FIRST. **First-tick = build skeleton + measure hit-rate-delta only; wire-byte saving deferred.**

### 3.3 D2 try-revert math (raw 142)

```
encode_composite(s) = let z = chain(s);
                     if len(z) < len(s) AND len(z) < min(E_A(s), E_B(s)):
                         return z
                     else:
                         return s   // identity revert
```

This guarantees composite never inflates aggregate vs current SOTA (76.24% A25 dispatcher). **Worst case = +0 aggregate effect.**

### 3.4 Chain idempotency contract

- `decode_composite(encode_composite(s)) == s` for all s. (Falsifier F-CC-2.)
- `encode_composite(encode_composite(s)) == encode_composite(s)` (header-detect short-circuit, mirroring A29/A30 pattern).
- Non-composite input → composite_decode passes through unchanged (raw 65 + 68).

---

## 4. Wire format design

### 4.1 Composite header

```
# cc:s1 v=composite-v1 chain=<C1|C3> n=<input_bytes> n1=<inner_payload_bytes> n2=<final_payload_bytes>
^d<base64url-of-final-payload>
```

Sigil **^d** (lowercase, raw 92 sigil-line compliant; disjoint from ^a/^b/^c which belong to A29/A30/A32). The `chain=` field is mandatory: composite_decode dispatches the inverse pipeline based on this tag.

### 4.2 Internal-payload extraction (the critical primitive)

Composite chain CANNOT naively chain wire strings (double-b64 anti-compressive). Instead it requires **payload extraction** from stage-1's wire and **payload injection** into stage-2:

```
stage1_payload_bytes = decode_b64_body(E_A(s).split("^a")[1])
stage2_input = stage1_payload_bytes  // NOT the wrapped wire
stage2_wire = E_B(byte_array_to_string(stage2_input))   // hand bytes to B
```

Decode mirrors:

```
stage2_payload = decode_b64_body(z.split("^d")[1])
stage1_payload = D_B(string_from(stage2_payload))   // B's decode reveals A's bytes
result_bytes = D_A_internal(stage1_payload)           // A's internal-form decoder
```

This requires composite_encode/decode to know how to call A29's `_a29_decode_to_bytes` / A30's `_a30_decode_to_bytes` (the **byte-array-returning decoders**, NOT the string-wrapped ones).

### 4.3 Why string-level chaining is rejected

A naive wire-level composite (treating E_A(s) as a string and feeding to E_B) means E_B sees ASCII characters from the b64 alphabet (64 symbols). E_B's compression on this text is fundamentally limited:

- A30 BWT on b64-alphabet text: 64-character alphabet permutes → MTF rank stream → RLE → entropy. The b64 alphabet is uniform-distribution by design (entropy near 6 bits/char). **No saving.**
- A29 LZ77 on b64 alphabet: matches of length≥3 in random b64 are rare. Backreference savings minimal.

**Falsified preregistration (F-CC-WIRE-1)**: any wire-level composite chain saving > 0 on uniform-b64 input → REVISIT theory; this should empirically yield -1..0 saving across all fixtures.

---

## 5. First-tick skeleton scope

Per raw 91 honest C3, this tick is **build + selftest** ONLY:

| Pass | Status | Notes |
|------|--------|-------|
| PASS 1: chain dispatcher (C1/C3 selector) | IMPLEMENTED skeleton | `cc_dispatch(chain_tag, s) -> string` |
| PASS 2: C-PRIMARY (A29→A30) wrapper | SKELETON (calls into A29/A30) | Internal-payload extraction stub. Not full optimization. |
| PASS 3: C-SECONDARY (A30→A23) wrapper | SKELETON (calls into A30/A23) | Hit-rate-delta probe only; wire-byte saving deferred. |
| PASS 4: encode/decode wire (^d sigil + composite header) | IMPLEMENTED | Header v=composite-v1 chain={C1,C3}. |
| PASS 5: byte-eq selftest (3 fixtures) | IMPLEMENTED | English / Korean / JSON-mixed round-trip. |
| PASS 6: LIVE FIRE on 5MB stratified corpus | **DEFERRED** | raw 91 honest C3; this tick is build-only. |
| PASS 7: 6-repo full sweep | **DEFERRED** | Only after PASS 6 verdict. |
| PASS 8: A25 dispatcher integration | **DEFERRED** | Only if PASS 6 + PASS 7 yield > 0pp aggregate. |

### 5.1 Skeleton intentional simplifications

- **No internal-byte fast-path**: skeleton uses the **string-level** chain (E_B(E_A(s))) for round-trip correctness on minimum LoC, accepting the double-b64 anti-lever. The internal-byte fast-path is the FOLLOW-ON tick refinement.
- **C-PRIMARY = wire-level** A29→A30 in skeleton (simpler; faithful round-trip; expected to inflate; D2 try-revert returns identity in selftest measurement).
- **C-SECONDARY = wire-level** A30→A23 in skeleton (same).
- The skeleton's job is to **establish the encode/decode contract + sigil + selftest** so the follow-on tick can swap in internal-byte composition without redesigning the wire.

### 5.2 Non-overlap re-affirmed

- Composite chain module = `hxc_composite_chain.hexa` (NEW file).
- Sigil = `^d` (NEW).
- A29 module = read-only consumed via `a29_encode/a29_decode`.
- A30 module = read-only consumed via `a30_encode/a30_decode`.
- A23 module = read-only consumed via `a23_encode/a23_decode`.
- No edits to a875c76c (A29 v1) / a8e5bf4d (A29 length codes) / a2c50860 (A29 v2 LIVE FIRE).

---

## 6. Falsifiers (raw 71 preregistration)

**Skeleton-tick falsifiers** (verified this turn):

- **F-CC-1**: round-trip byte-eq fails on any of 3 selftest fixtures → REJECT (raw 65 + 68).
- **F-CC-2**: composite encode for any fixture > identity wrapper → revert to identity per raw 142 D2 (verified by selftest assertion).
- **F-CC-3**: header parse ambiguity (composite header collides with A29/A30/A23 header) → REJECT; sigil ^d enforced disjoint.

**Follow-on-tick falsifiers** (LIVE FIRE deferred):

- **F-CC-4**: aggregate < 78.65% on 6-repo sweep when chain enabled in dispatcher → REJECT raw 137 v8.
- **F-CC-5**: any chain ordering yields composite > best single algorithm by > 5% → catalog as "chain anti-lever, do not promote".
- **F-CC-6**: wire-level chain saving > 0 on uniform-b64 input → REVISIT theory (theoretical contradiction).
- **F-CC-7**: internal-byte chain (follow-on) yields s2 < 24.8% on DEFLATE bitstream byte projection → REJECT C-PRIMARY (theoretical break-even).
- **F-CC-8**: A23 hit_rate(A30(text)) <= hit_rate(text) → REJECT C-SECONDARY hypothesis (BWT context clustering does NOT help PPM).

---

## 7. Pre-registered honest C3 (raw 91)

**Predicted outcomes for composite chain experiment** (logged BEFORE skeleton selftest):

1. **C-PRIMARY (A29→A30) wire-level skeleton**: composite encode > identity for all 3 fixtures → D2 try-revert returns identity → composite saving = 0pp. **PRE-REGISTERED FALSIFICATION OF NAIVE WIRE-CHAIN.**
2. **C-SECONDARY (A30→A23) wire-level skeleton**: same → 0pp.
3. **Selftest 3/3 byte-eq PASS** is the primary first-tick gate (correctness, not saving).
4. **Internal-byte composition** (follow-on tick): C-PRIMARY predicted ±0..+3pp; C-SECONDARY predicted -1..+1pp; **neither predicted to advance 78.65% gate.**

**Composite chain experiment outcome ledger entry (pre-registered):**
```
{
  "experiment": "hxc_composite_chain_skeleton_2026_04_28",
  "scope": "first-tick skeleton + 3-fixture selftest",
  "candidates": ["C1=A29→A30", "C3=A30→A23"],
  "level": "wire-level (skeleton); internal-byte deferred",
  "predicted_skeleton_verdict": "D2 try-revert = identity for all fixtures (saving=0)",
  "primary_gate": "F-CC-1 byte-eq round-trip 3/3",
  "production_promotion": "BLOCKED until follow-on internal-byte tick + LIVE FIRE",
  "honest_c3_label": "skeleton scope ONLY, no measured class lift, no aggregate claim"
}
```

---

## 8. Recommendation — 1-2 chains

### 8.1 Primary recommendation: C1 (A29→A30) — internal-byte version

**Rationale**: A29's internal byte payload is the LZ77 + canonical Huffman bitstream. While near-Shannon, it has known periodic byte boundaries (RFC 1951 §3.2 specifies byte-aligned blocks). BWT on byte-aligned periodic data CAN find structure if the periodicity matches a BWT block boundary cycle.

**Proceed-conditions** (gates for follow-on tick):
- Skeleton selftest 3/3 byte-eq PASS (this tick).
- Internal-byte fast-path lands.
- 5KB stratified fixture micro-LIVE-FIRE shows s2 ≥ 24.8% (theoretical break-even).
- Only then: 5MB stratified + 6-repo full sweep.

### 8.2 Secondary recommendation: C3 (A30→A23) — hit-rate-delta probe

**Rationale**: BWT-clustering theoretically should improve PPM order-5 hit rate. Even if WIRE saving is null (A23 v1 wire is order-1), the **hit-rate metric** is a valid PPM-axis lever indicator. A23 v2 wire (order-5) is the operational follow-on if hit-rate-delta is positive.

**Proceed-conditions**:
- Skeleton selftest 3/3 byte-eq PASS.
- Hit-rate(A30(text)) - hit-rate(text) >= +5pp on text fixtures (F-CC-8 inverse).
- A23 v2 wire (order-5) lands.
- Only then: full pipeline measurement.

### 8.3 Recommendation summary

> **Do build the skeleton this tick (PASS 1-5).** The skeleton's job is to establish the wire format + sigil + correctness gate, not to measure saving. **Do NOT promote to LIVE FIRE this tick.** The honest C3 expectation is composite chain is a **falsification candidate** as much as a saving candidate.

---

## 9. Cumulative caveats (raw 91 explicit)

1. Skeleton uses wire-level chaining for minimum LoC; **inflated baseline expected**, D2 try-revert returns identity.
2. Internal-byte fast-path = follow-on tick. Skeleton deliberately does NOT optimize.
3. C-PRIMARY break-even s2 ≈ 24.8% on DEFLATE bitstream — empirically untested, theoretically marginal.
4. C-SECONDARY hit-rate-delta probe is in-sample-bits estimator only; A23 v1 wire byte saving NOT measured.
5. Composite chain operates on the **product** of two algorithms' wire formats — any future A29 v2/v3 + A30 v2 wire-format change requires composite re-validation.
6. raw 142 D2 try-revert MEASURED structurally (returns identity if composite > identity); **empirical D2 falsification rate** = pre-registered prediction, NOT verified at skeleton tick.
7. NO LIVE FIRE / NO 6-repo sweep / NO catalog promotion / NO A25 dispatcher integration this tick.
8. The composite chain experiment EXPECTED OUTCOME = falsification of "chain-axis closes 16.66pp gap"; if so, Phase 14+ must seek lift on a NEW axis (semantic dictionary / cross-file federation v3 / paradigm-orthogonal coder).

---

## 10. Cross-references

- A29 design: `anima/docs/hxc_phase13_p0_a29_deflate_design_*.md` (a875c76c, a9aa0085 v2, a8e5bf4d length codes).
- A30 design: `anima/docs/hxc_phase12_secondary_a30_design_*.md`.
- A23 design: `anima/docs/hxc_phase12_p4_a26_sparse_ppmd_design.md` + sibling A23 docs.
- A25 dispatcher: `hxc_a25_type_aware.hexa`.
- Phase 14 forward design: `anima/docs/hxc_phase14_forward_*.md` (if any).
- Falsification ledger v2: `anima/docs/hxc_falsification_ledger_v2_20260428.md` — composite chain falsifier set added.
- Self-host self-decoding contract: `anima/docs/hxc_a4_structural_20260428_landing.md`.

---

## 11. End of design — first-tick skeleton mandate

This tick:
- Land `hxc_composite_chain.hexa` skeleton.
- Verify selftest 3/3 byte-eq round-trip.
- Pre-register falsifiers F-CC-1..8.
- DO NOT measure aggregate; DO NOT deploy in dispatcher; DO NOT promote.

Follow-on ticks (separate decision-gate):
- (T+1) Internal-byte fast-path on C-PRIMARY → micro-LIVE-FIRE 5KB → s2 ≥ 24.8% gate.
- (T+2) C-SECONDARY hit-rate-delta probe with A23 v1 in-sample-bits estimator.
- (T+3) ONLY IF micro-LIVE-FIRE passes: 5MB stratified, then 6-repo full sweep.

raw 91 honest C3 lock: this design + skeleton ARE the deliverables; no measured saving claim is made by this turn.
