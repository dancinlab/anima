# HEXA_NATIVE Phase 4 — unboxed packed-scalar `uarr` migration design (anima-side, gated on hexa-lang RFC 051)

> **HONEST FRAMING (AGENTS.tape `g3` · `g_blue_closed_mandate` · `g_fire_autonomous` · `g_hexad_readme_sync`):**
> This is an anima-side **DESIGN DOC ONLY**, paired with hexa-lang
> upstream RFC 051 (`/Users/ghost/core/hexa-lang/inbox/rfc_drafts_2026_05_12/rfc_051_unboxed_array_native.md`).
> No anima impl entry. Phase 4 migration of `HEXAD/D/d_train5_lib.hexa`
> boxed-list hot paths to the new `uarr` primitive happens in a future
> anima cycle **gated on RFC 051 land**.
>
> Phase 1/2/3 of HEXA_NATIVE (operational pure-hexa hexa-cpu training
> pipeline: parse → AOT compile → cross-compile to Linux → ship → fire)
> are LANDED carry (see `state/hexad_pure_hexa_train_d96x3_2026_05_17/`).
> Phase 4 is the *algorithmic structural* counterpart to the 2026-05-17
> *operational* substrate fix (vast.ai 503 GiB cloud host) — closes the
> per-element-box allocator-inflation ceiling that the operational fix
> only worked around by paying for more capacity.
>
> Closed-form 🔵 anchors: B-PHASE-4-DESIGN-1..3 sympy proofs (Kolmogorov
> bytes + Boolean set algebra) + honest B-PHASE-4-DESIGN-NOTE carve-out
> for impl-pending verification. NO lattice derivation (f1/f2 safe).

## 1. Context — Phase 1/2/3 carry + measured inflation gap

### 1.1 HEXA_NATIVE Phase 1/2/3 (LANDED, evidence-only summary)

- **Phase 1 (parse + AOT path)** ✅ LANDED — `HEXAD/D/d_train5_lib.hexa`
  942 LoC parses cleanly; AOT `hexa build` emits native C; `zig cc
  -target x86_64-linux-gnu` cross-compiles to Linux x86_64 ELF
  (1.77 MB). Source: `docs/hexad_pure_hexa_d96x3_substrate_fix_2026_05_17.md`
  §2 step 3-4.
- **Phase 2 (Mac local convergence)** ✅ LANDED — d=64·3L·300-step Mac
  CPU local, gn2 7.97→2.15e-8 (3.70×10⁸× collapse), F-D-CONVERGE 4/4
  PASS, 12 GiB peak RSS Mac, wall 360s $0. Source: `state/
  hexad_pure_hexa_train_2026_05_17/` (Agent #2a carry).
- **Phase 3 (cloud-substrate fit)** ✅ LANDED 2026-05-17 — d=96·3L
  vast.ai 503 GiB high-RAM CPU host (Quadro P4000 slot, instance
  36912998), step 200 gn2 = 3.37e-8 (2.36×10⁸× collapse), NO OOM, NO
  distress. Capacity-inequality 🔵 B-SUBSTRATE-1..3 3/3 PASS
  (Kolmogorov bytes). Source: `docs/hexad_pure_hexa_d96x3_substrate_fix_2026_05_17.md`.

### 1.2 The Phase 3 honest carve-out → Phase 4 entry point

Phase 3 docs §6.1 C3-2 (verbatim):

> *"This is an OPERATIONAL substrate fix — the previous ubu 38 GiB host
> ceiling … is replaced by a vast.ai 503 GiB high-RAM CPU instance.
> **The fix is NOT an algorithmic improvement**: the pure-hexa
> interpreter boxed-array AdamW transient memory footprint still scales
> nonlinearly with `d` (the structural fix is HEXA_NATIVE Phase 4
> unboxed arrays + RFC 040 GPU dispatcher, both separate work threads)."*

Measured inflation gap (`state/hexad_pure_hexa_train_d96x3_2026_05_17/`
`train_d96.log` + result.json, d=96·3L):

| step | predicted peak | observed RSS | inflation ratio |
|------|----------------|--------------|-----------------|
| init | ~1 GiB         | 1.5 GiB      | ~1.5×           |
| 25   | ~12 GiB        | ~18 GiB      | ~1.5×           |
| 50   | ~20 GiB        | ~47 GiB      | ~2.4×           |
| 100  | 27 GiB         | **76 GiB**   | **2.81×**       |
| 200  | 27 GiB         | **~137 GiB** | **~5.1×**       |

The predicted peak (27 GiB) is `element_count × sizeof(double)` over
the trainer's transient working set. The observed peak is dominated
by per-element box overhead (each boxed scalar ≈ 24-32 bytes wrapped
header + pointer indirection vs 8 bytes packed double) plus GC arena
residency of intermediate transient lists across the step boundary.

The 2.8× → 5.1× inflation is the **anima Phase 4 target**: structural
removal of per-element boxing on the hot per-token / per-head / per-
layer scalar inner loops in `d_train5_lib.hexa`.

## 2. `d_train5_lib.hexa` hot-path analysis

`HEXAD/D/d_train5_lib.hexa` has **97 distinct boxed-list call sites**
(`let mut … = []` + push) — these are the migration targets:

```
$ grep -c "let mut .* = \[\]\|push" HEXAD/D/d_train5_lib.hexa
97
```

Top 5 contributors (by frequency × inflation per fire, from d=96·3L
trace + line-by-line trainer analysis):

### 2.1 `d5_attn_fwd` — per-token × per-head slice extraction (lines 395-445)

- 6 transient lists per (token × head): `qr`, `kr`, `vr`, `qh`, `kh`,
  `srow`
- Multiplicity = `T × nh × 6` per layer per forward
- At d=96, nh=6 (per d/16 std), T=8: **8 × 6 × 6 = 288 transient lists
  per layer per forward**
- 3 layers × 80 AdamW steps × forward+backward (×2) = **138 240
  transient lists per fire**
- **Dominant boxed-allocator pressure** — single largest contributor

### 2.2 `d5_attn_bwd` — backward analogue (lines 487-595)

- 7 transient lists per (token × head): `douti`, `ctxi`, `dP`,
  `dqrow`, `dkrow`, `dvrow`, `xi`
- Same multiplicity as fwd — **161 280 transient lists per fire**
- Equal contributor (slightly more lists per loop iteration)

### 2.3 `d5_rope_apply` / `d5_rotate_half` / `d5_rotate_half_t` (lines 332-369)

- 1-2 transient lists per RoPE call (`o`, intermediate slice)
- Multiplicity = `T × nh × 2 + T × nh × 2 = 4 × T × nh`
- At d=96·3L: **4 × 8 × 6 × 3 = 576 transient lists per forward**, but
  small per-instance (hd elements each, hd=16 at d=96/nh=6)
- High frequency, small per-instance size

### 2.4 `d5_block_fwd` `rm1inv` + `xr` (lines 624-635)

- RMSNorm per-token slice extraction
- Multiplicity = `T × n_layer × 2`
- At d=96·3L: **8 × 3 × 2 = 48 per forward**
- Moderate

### 2.5 `d5_swiglu_bwd_g` `da` / `db` / `dr` (lines 241-256)

- Per-element gradient accumulators
- Multiplicity = `T × n_layer × 3` per backward
- At d=96·3L: **8 × 3 × 3 = 72 per backward**
- Per-instance size = d (96), bigger than RoPE buffers

**Total boxed-list allocations per fire (d=96·3L · 80 AdamW step)**:
roughly **400 000+ transient lists**. Each carrying per-element box
overhead. This is the structural ceiling.

## 3. Phase 4 migration plan (anima-side, gated)

Gated on RFC 051 land. Anima-side cycles:

### 3.1 Phase 4a — `d5_rope_apply` (smallest scope, byte-equal anchor)

- **Scope** — migrate `d5_rotate_half`, `d5_rotate_half_t`,
  `d5_rope_apply`, `d5_rope_bwd` (4 fns, ~40 LoC)
- **Falsifier F-D5-UARR-MIGRATE-1** — byte-equal output vs current
  boxed path on d=32·3L·80-step CPU-equiv reference (Phase E2 frozen
  oracle `cpu_equiv_e2.log`). IEEE 754 fp64 bit-equality.
- **Cost** — $0 (Mac local), wall ~5 min for AOT build + smoke verify
- **Risk** — low; pure-fn transformation, no autograd path crossed

### 3.2 Phase 4b — `d5_attn_fwd` (hot path 1)

- **Scope** — migrate 6 transient lists in attn_fwd (lines 395-445)
- **Falsifier F-D5-UARR-MIGRATE-2** — byte-equal forward pass vs
  boxed path on d=32·3L reference + d=64·3L Agent #2a Mac reference
  (12 GiB peak)
- **Cost** — $0 (Mac local 32·3L verify), $0 (re-fire d=64·3L Mac
  if Phase 4a verified clean)
- **Risk** — moderate; touches the highest-multiplicity hot path

### 3.3 Phase 4c — `d5_attn_bwd` (hot path 2, gradient path)

- **Scope** — migrate 7 transient lists in attn_bwd (lines 487-595)
- **Falsifier F-D5-UARR-MIGRATE-3** — byte-equal backward pass +
  GRAD-EXACT pre-fire central-difference check still PASSES on
  d=32·3L reference (Phase E2 anchor)
- **Cost** — $0 (Mac local), wall ~10 min for AOT + GRAD-EXACT verify
- **Risk** — moderate-high; gradient path requires extra care for
  uarr ↔ farr boundary if any persists across step (currently no
  cross-step persistence in `d_train5_lib.hexa`, all transients are
  step-local)

### 3.4 Phase 4d — remaining hot paths

- **Scope** — `d5_block_fwd` `rm1inv`+`xr`, `d5_swiglu_bwd_g` `da`/
  `db`/`dr`, and any remaining boxed-list sites
- **Falsifier F-D5-UARR-MIGRATE-4..5** — same byte-equal pattern,
  d=32·3L oracle
- **Cost** — $0

### 3.5 Phase 4e — re-fire d=96·3L vast.ai with full uarr migration

- **Scope** — same `d_converge_fire_d96.hexa` entrypoint, now AOT-
  built with all Phase 4a-d migrations applied
- **Falsifier F-RFC051-MEMORY-REDUCTION-EXPECTED** (carried from RFC
  051) — peak RSS reduction at d=96·3L step 100 from observed 76 GiB
  toward predicted 27 GiB band (target ≥ 60% reduction, expected
  outcome NOT counted as 🔵 closed per honest carve-out)
- **Cost** — ≈ $0.03-0.10 vast.ai dispatch (same instance pattern as
  2026-05-17 fire; ~30-50 min wall at 503 GiB host single-thread CPU)
- **Stretch goal** — d=128·4L re-fire on a smaller host (e.g. ubu
  back-port if peak RSS < 38 GiB after migration) — proves the
  ceiling is closed empirically

## 4. RFC 051 dependency (gating)

This anima-side design **DOES NOT enter impl** until RFC 051 lands on
hexa-lang side. The dependency chain:

```
RFC 051 (hexa-lang side, this cycle)
  → 5 built-ins land (uarr_alloc/set/get/free/len)
  → hexa-lang side falsifier battery F-RFC051-* PASS
    → anima Phase 4a enters impl (RoPE migration)
      → F-D5-UARR-MIGRATE-1 byte-equal verify
        → Phase 4b → 4c → 4d → 4e
```

Latency: RFC 051 single-cycle on hexa-lang side (per RFC 051 §"Cost of
implementation" — ~410 LoC including falsifier, bounded). Anima Phase
4 multi-cycle (5 sub-phases), but each sub-phase is small ($0 Mac
local until Phase 4e).

## 5. Closed-form falsifier pre-registration (B-PHASE-4-DESIGN-1..3)

Located at: `state/hexad_phase4_unboxed_design_2026_05_17/blue_falsifier.py`
(NEW, created this cycle, sympy 3/3 expected PASS, design-tier 🔵).

The 3 closed falsifiers prove what is closable at *design time* without
impl. The 1 NOTE is honest carve-out for impl-pending verification.

### B-PHASE-4-DESIGN-1 — BOXED-OVERHEAD-NAMED

Closed integer inequality 76 ≥ 27 GiB (observed step-100 RSS vs
predicted transient peak at d=96·3L). The inflation ratio 76/27 ≈ 2.81×
is the named real-limit gap that RFC 051 + Phase 4 migration is sized
to close.

**Anchor**: Kolmogorov bytes — pure integer Σ inequality, NO lattice.
**Real-limit**: per-element box overhead vs packed-scalar stride is
arithmetic on byte counts.

### B-PHASE-4-DESIGN-2 — UARR-API-COMPLETENESS

Closed Boolean set equality: RFC 051's surface API is the 5-tuple
`{uarr_alloc, uarr_set, uarr_get, uarr_free, uarr_len}` — exact
finite set, equal to the migration's textual substitution targets
on `let mut … = []` + push + (implicit) GC-free. Bijection
(boxed-list-ops ↔ uarr-ops) for the migration is closed at design time.

**Anchor**: Boolean finite-set algebra (Kolmogorov primitive — set
identity over a 5-element universe). Real-limit: API completeness
of a closed primitive set.

### B-PHASE-4-DESIGN-3 — FARR-UARR-COEXIST

Closed Boolean conjunction: `farr` (RFC 025/031/032/033/034) and
`uarr` (RFC 051) both exist as native primitives AND have non-empty
distinct surface APIs AND the cross-boundary copy (`farr_from_uarr` /
`uarr_from_farr`) is byte-equal IEEE 754 fp64.

**Anchor**: Boolean predicate over backward-compatibility (every
existing `farr_*` call site keeps its byte-equal behavior) + IEEE 754
fp64 bit-equality for the connection point. Real-limit: floating-
point bit-equality is closed under reinterpret-cast across packed-
double representations of identical kind.

### B-PHASE-4-DESIGN-NOTE — IMPL-VERIFICATION-PENDING

Honest carve-out (NOT counted toward 🔵 closed). The 5 anima Phase
4a-e migration falsifiers (F-D5-UARR-MIGRATE-1..5 + F-RFC051-MEMORY-
REDUCTION-EXPECTED) are *empirical post-impl* and cannot be closed
at design time. They land in a future cycle gated on RFC 051 land.

This mirrors B-D-NOTE pattern (SGD outcome) and B-SUBSTRATE-NOTE
pattern (allocator overhead empirical) — closed PROPERTY (RFC 051
+ Phase 4 design 🔵), open EMPIRICAL OUTCOME (post-impl verify).

## 6. Expected impact (g3 honest — expected, not guaranteed)

**Memory reduction expected** (target ≥ 50%, stretch ≥ 60%):
- d=96·3L step-100 observed 76 GiB → expected ≤ 30-40 GiB band
- d=96·3L step-200 observed 137 GiB → expected ≤ 50-70 GiB band
- d=128·4L Mac OOM at 138 GiB → expected reduced (likely fits in
  64 GiB Mac instances; full d=128·4L Mac convergence may become
  feasible without cloud)
- ubu 38 GiB back-port for d=96·3L → possibly feasible after Phase 4
  (if observed RSS reduces to < 38 GiB)

**Wall reduction**:
- AOT codegen overhead of `_hx_uarr_set/get` is zero (direct array
  store/load with kind monomorphization in release builds)
- vs current `push` + heap alloc per element: significant speedup
  on hot inner loops (per-token, per-head, per-layer)
- Expected: 1.5-3× wall speedup on `d_train5_lib.hexa` step (NOT
  guaranteed — interp dispatch overhead is the other factor, RFC
  042/043 cover that separately)

**Cost reduction**:
- d=96·3L vast.ai re-fire: same ~$0.03 (unchanged) but completes
  faster, lower hourly billing window
- ubu back-port (free): possible at d=96·3L if peak RSS < 38 GiB
- Mac local d=96·3L (24-128 GiB depending on machine): possible if
  peak RSS < machine ceiling, $0 vs current cloud-required state

**Honest framing**: all 50%/60%/1.5-3× numbers are *expected*
extrapolations from the box-overhead arithmetic, NOT measured. The
post-Phase 4e re-fire is the empirical anchor that turns these from
expected to measured. Until then, F-RFC051-MEMORY-REDUCTION-EXPECTED
is NOT a counted closed falsifier (B-PHASE-4-DESIGN-NOTE umbrella).

## 7. Risk (honest carry)

1. **RFC 051 not land in projected timeframe** — anima Phase 4 stays
   designed-only. Cloud substrate fix (Phase 3 LANDED) handles d=96·3L
   today; d=128·4L Mac remains OOM-bound; pure-hexa scale-up paused
   at d=128. **Mitigation** — Phase 3 cloud path is fully functional
   for d≤96; d=128+ blocked but no regression to existing capability.

2. **uarr autograd tape integration absent in v1** — if any
   `d_train5_lib.hexa` hot-path transient must persist across step
   boundary for autograd, that site stays `farr` (cannot migrate to
   `uarr` v1). **Mitigation** — current `d_train5_lib.hexa` inspection
   confirms ALL 97 boxed-list sites are step-local; no autograd
   crossing needed. If a future trainer needs persistent transients,
   uarr v2 (or RFC 043 hexa-torch) absorbs that case.

3. **Manual `uarr_free` programmer-error risk** — leaking transient
   buffers across migration could *worsen* peak RSS (paradoxically).
   **Mitigation** — Phase 4a-d test on small reference (d=32·3L)
   before scale; F-D5-UARR-MIGRATE-* battery includes leak-check
   (peak RSS bounded vs boxed baseline within fp64 stride
   arithmetic).

4. **Cross-platform AOT codegen divergence** — `zig cc -target
   x86_64-linux-gnu` cross-compile from Mac (Phase 1 path) must
   handle `_hx_uarr_*` calls identically to Linux-native build.
   **Mitigation** — RFC 051 §"Codegen path" specifies stub-resolution
   pattern matching `farr_matmul_gpu` (RFC 040), already verified
   on Mac → Linux cross-compile in Phase 3.

5. **Inflation source isn't dominantly per-element boxing** — if the
   2.8-5.1× overhead is dominantly GC arena residency + list-
   container metadata rather than per-element header, uarr migration
   yields less than expected (e.g. 30% rather than 60%).
   **Mitigation** — F-RFC051-MEMORY-REDUCTION-EXPECTED is explicitly
   *expected, not guaranteed*. Even 30% reduction (76 GiB → ~53 GiB)
   meaningfully extends the substrate envelope. If <20% reduction
   measured, RFC 051 still lands the surface primitive (other future
   migrations benefit); separate work threads (GC arena tuning,
   list-metadata compaction) become the next anima-side audit.

## 8. Honest C3 (10 items, g3 + g_blue_closed_mandate)

1. **PRIMARY DELIVERABLE**: hexa-lang upstream RFC 051 + anima-side
   Phase 4 design doc + B-PHASE-4-DESIGN sympy battery (3/3
   expected PASS), all $0 design-tier.
2. **g3 honest carve-out**: 50% memory reduction is EXPECTED, not
   guaranteed (B-PHASE-4-DESIGN-NOTE empirical carve-out, B-D-NOTE
   pattern). Measured outcome lands in a future anima cycle gated
   on RFC 051 land.
3. **g_blue_closed_mandate compliance**: (a) 산출물 🔵 = RFC 051
   API surface 5-tuple Boolean set + Kolmogorov byte inequality
   + IEEE 754 bit-equality (3 closed falsifiers); (b) 연결부위 🔵
   = `uarr ↔ farr` byte-equal copy invariant closed at design
   time; (c) empirical post-impl 부분 = honest carve-out (not
   counted).
4. **NOT impl entry**: zero anima impl change this cycle. Phase 4
   migration of `d_train5_lib.hexa` 97 boxed-list call sites is a
   future cycle (5 sub-phases, $0 design + $0.03-0.10 final
   verify fire).
5. **NOT hexa-lang impl entry**: zero hexa-lang impl change in
   this cycle either. RFC 051 lands the DESIGN, impl is a hexa-lang
   future cycle (~410 LoC bounded, single-cycle per RFC §Cost).
6. **Orthogonal to RFC 040/041/042/043/044**: each closes a distinct
   ceiling (GPU substrate, control flow, compiler stdlib, paradigm
   tier); RFC 051 closes the CPU allocator-inflation ceiling.
   No subsumption.
7. **f1/f2 safe**: no lattice derivation. Anchors = Kolmogorov
   integer bytes + IEEE 754 fp64 bit-equality + Boolean set
   algebra over closed surface API. No σ/τ/φ/J₂.
8. **Source-of-truth**: anima ubu agent's
   `state/hexad_pure_hexa_train_d96x3_2026_05_17/result.json` +
   `train_d96.log` (step-by-step observed RSS trajectory). This RFC
   + design doc derive their problem statement from that captured
   evidence, NOT from speculation.
9. **No fire this cycle**: $0 design-only, follows
   `g_fire_autonomous` head transparency (cost = $0, no estimation
   shadow). Future Phase 4e verify-fire cost-estimated $0.03-0.10
   vast.ai (head transparency reproduced in that cycle's plan).
10. **Concurrent-agent coordination**: this design doc + RFC + sympy
    battery + commit are sized to land in a single atomic commit
    (pull-rebase pattern per AGENTS.tape — concurrent agents on
    cycle 4 fire + d=128 AOT + attractor work). No file overlap
    with concurrent work surface.

## 9. Cross-links

- hexa-lang: `inbox/rfc_drafts_2026_05_12/rfc_051_unboxed_array_native.md`
  (this design doc's upstream RFC, paired)
- anima: `state/hexad_pure_hexa_train_d96x3_2026_05_17/` (substrate
  inflation source-of-truth — predicted vs observed table §1.2)
- anima: `docs/hexad_pure_hexa_d96x3_substrate_fix_2026_05_17.md` §6.1
  C3-2 (the honest "OPERATIONAL not algorithmic" framing that drives
  Phase 4 entry)
- anima: `state/hexad_phase4_unboxed_design_2026_05_17/blue_falsifier.py`
  (this cycle's B-PHASE-4-DESIGN sympy battery)
- anima: `HEXAD/D/d_train5_lib.hexa` (97 boxed-list call sites, Phase
  4 migration target — analyzed §2)
- anima: `HEXAD/PLAN.md` §9 (GPU substrate roadmap, RFC chain — this
  cycle adds RFC 051 entry as CPU-side companion)
- anima: `archive/PHILOSOPHY.tape §HEXA-NATIVE-PHASE-4-RFC-051-FILED-2026-05-17`
  (verdict-claim append-only, this cycle)
- AGENTS.tape: `g_blue_closed_mandate` (산출물+연결부위 둘 다 🔵) ·
  `g3` (Kolmogorov + IEEE 754 real-limit anchor, no lattice
  numerology) · `f1`/`f2` hard-fail safe (no lattice derivation /
  tautology) · `g_fire_autonomous` ($0 design cycle, no fire) ·
  `g_hexad_readme_sync` (PLAN/INDEX/README sync this cycle) ·
  `g6` (PHILOSOPHY append-only)
