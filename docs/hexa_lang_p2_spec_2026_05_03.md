---
title: hexa-lang stdlib P2 spec — `@quantum_substrate` attribute + native `complex` primitive
date: 2026-05-03
mode: doc-only deliverable (SPEC ONLY; no impl, no hexa-lang patch, no .py)
status: forward-spec for a later cycle
authors: anima cycle agent (qmirror substrate review follow-up)
substrate refs:
  - docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md (predecessor — P0/P1/P2 split + ROI table)
  - docs/nexus_qmirror_spec_2026_05_03.md (consumer — qmirror Phase 1/2 surface)
  - hexa-lang/doc/spec.md v0.1 (8 primitives, 13 attrs, σ·τ+sopfr=53 keywords)
  - hexa-lang/doc/ai-native-attrs.md (parser/lexer/ai_native_pass file map)
  - hexa-lang/stdlib/registry_autodiscover.hexa (Phase α landed 2026-05-02 — autodiscover host)
  - hexa-lang/stdlib/linalg/{reference,ffi,dispatch,mod}.hexa (BLAS-lite host for complex extension)
  - hexa-lang/stdlib/matrix/{construct,mod,stack}.hexa
  - nexus/modules/qrng/{anu,hardware_qrng,mock_qrng}.hexa (current `tier: int = 0|1|3` convention to retrofit)
gate: raw#9 (no .py here — spec only), raw#15 (no personal absolute paths in body)
scope: P2 = "later cycle, after qmirror Phase 1+2 land". This is a forward-only specification; implementation timing is P3 / Phase α+2 stdlib quarter.
---

# 0. TL;DR

Two **independent** P2 hexa-lang surface additions are specified here. **Neither is required for qmirror Phase 1/2** (P0/P1 stdlib patches in the predecessor review unblock everything qmirror needs through the calibration anchor). Both are deferred to a later cycle because each carries a non-trivial **cascading cost** that is wrong to pay opportunistically:

| Item | Surface | Cascading cost | Land-with prerequisite |
|------|---------|----------------|------------------------|
| **`@quantum_substrate(tier: T1\|T2\|T3)`** attr | metadata-only (G2 semantic group); ~80 LOC across 4 files | **registry_autodiscover extension** must consume the attr or the attr is dead-code; ~120 LOC in `stdlib/registry_autodiscover.hexa` + retrofit of 5 existing nexus modules | qmirror Phase 1 + Phase 2 landed → registry has ≥6 typed substrate modules to classify; `@deprecated`-style auto-injection policy decided |
| **native `complex` primitive** | new 9th primitive type; literal syntax `1.0+2.0i`; 6 builtin ops; cascades into linalg/matrix complex variants | **linalg cgemm / cgemv / cdotc / caxpy / cnrm2** + matrix complex constructors + parser literal + interp+AOT codegen + ai_native_pass type-classification table; 6+ files, 400-600 LOC | qmirror tomography / iit_mip have shown the `struct Complex { re, im }` wrap is genuinely friction (≥3 callsites of parallel-array bookkeeping noise) |

**Why P2 not P1:** both are convenience wins, not unblockers. The struct-wrap and `tier: int` field-based conventions remain *honest* (predecessor review §3.1, §2.4, caveat 6). Premature land risks (a) new convention + old convention coexistence in nexus, (b) parser regression on the existing 13 official attrs, (c) `complex` literal syntax forcing a lexer state-machine change that touches every numeric token rule.

**Recommended landing cycle:** **Phase α+2 stdlib quarter** (after Phase α+1 = P0/P1 from the predecessor review, after Phase α+1.5 = qmirror Phase 1 land). If `@quantum_substrate` lands solo without registry consumer, mark it `@deprecated` candidate immediately — that is the failure mode this spec exists to prevent.

---

# 1. `@quantum_substrate(tier: T1|T2|T3)` — full spec

## 1.1 Grammar

The attribute grammar is **a strict subset of `@bounded(N)`** (current spec.md G1 #7). Reusing the same parser path keeps the patch trivial and eliminates an entire class of grammar regression risk.

```ebnf
quantum_substrate_attr  ::=  "@quantum_substrate" "(" "tier" ":" tier_lit ")"
tier_lit                ::=  "T1" | "T2" | "T3"
```

**Position:** function-prefix attribute (same as `@pure`, `@hot`). Stacks freely with `@tool`, `@usage`, `@sentinel`, `@resolver-bypass` (the 4 existing nexus convention attrs).

**Example — current `nexus/modules/qrng/anu.hexa` retrofit:**

```hexa
@tool(slug="qrng_anu", desc="ANU quantum vacuum-fluctuation REST stream")
@usage(hexa run nexus/modules/qrng/anu.hexa --selftest)
@sentinel(__QRNG_ANU__ <PASS|FAIL>)
@resolver-bypass(reason="selftest gated to mock fixture")
@quantum_substrate(tier: T1)
fn qrng_anu_pull(n: int) -> QrngBytes { ... }
```

**Example — qmirror `engine_aer.hexa`:**

```hexa
@quantum_substrate(tier: T2)
fn engine_aer_run(circ: QasmCircuit, shots: int) -> CountsResult { ... }
```

**Example — qmirror IBM hardware backend:**

```hexa
@quantum_substrate(tier: T3)
fn engine_ibm_run(circ: QasmCircuit, shots: int) -> CountsResult { ... }
```

## 1.2 Tier semantics (T1 / T2 / T3)

| Tier | Meaning | Examples in current nexus tree |
|------|---------|--------------------------------|
| **T1** | Live external quantum measurement (REST / hardware QRNG over USB) | `qrng/anu.hexa`, `qrng/hardware_qrng.hexa` |
| **T2** | Local quantum simulator (Aer / Cirq / MPS) executing real quantum circuits classically | `qmirror/engine_aer.hexa`, `qmirror/engine_cirq.hexa`, `qmirror/engine_mps.hexa` |
| **T3** | Live remote quantum hardware (IBM Quantum, IonQ) — paid queue access, real qubits | `qmirror/engine_ibm.hexa` (P3 calibration anchor) |

**T0 deliberately omitted.** `tier=0` in the existing `qrng_meta_make()` convention means "deterministic mock fixture / classical PRNG." A `@quantum_substrate(tier: T0)` would be self-contradictory ("classical-substrate quantum-substrate"). Mock modules (`mock_qrng.hexa`) **do not get the attr** — their absence from the registry-autodiscover output is the signal.

## 1.3 Compiler integration

| Compiler stage | Change | LOC | File |
|----------------|--------|-----|------|
| **Lexer** | None — `@` → `Attribute` token already covers `quantum_substrate` (alphabetic identifier follows `@`) | 0 | `self/lexer.hexa` |
| **Parser** | `parse_attribute_prefix()` (parser.hexa L3372) gets a 3rd named branch alongside `symbol` / `link`. Parses `(tier: <ident>)` and stores `p_pending_substrate_tier: str = "T1"\|"T2"\|"T3"`. Drained by next `fn` decl into `annotations` map. | ~25 | `self/parser.hexa` |
| **ai_native_pass** | New milestone (e.g. M340) classifies into G2-semantic group counter `ai_substrate_t1 / t2 / t3`. Validates tier literal. Conflict check: `@quantum_substrate` + `@pure` warning (T1/T2/T3 by definition observe external state — non-pure). | ~30 | `self/ai_native_pass.hexa` |
| **AOT C codegen** | None — metadata-only attr, no runtime emission. Exposed via existing `// @substrate=Tn` comment in generated C (parallel to existing `// @symbol=...` annotation at parser.hexa L4417). | ~5 | `self/build_c.hexa` |
| **Interpreter** | None — accessible via existing `node["annotations"]` map at runtime introspection sites. | 0 | `self/interpreter.hexa` |

**Total new LOC:** ~60 (within hexa-lang). **Test additions:** 4 cases (T1/T2/T3 happy path + `@quantum_substrate` + `@pure` conflict warning). Insert into `self/test_bootstrap_compiler.hexa` series.

## 1.4 Registry autodiscover integration (the **point** of the attr)

`stdlib/registry_autodiscover.hexa` currently stops at file enumeration (`registry_scan_dir`, `registry_build_dispatch`). The substrate attr is **inert without a consumer.** Spec'd consumer extension:

```hexa
// stdlib/registry_autodiscover.hexa (additive — new pub fn, ~120 LOC)

// registry_classify_substrate(dir, suffix) -> {tier: str, modules: [str]}
//
// Reads each *.hexa file under dir, scans for `@quantum_substrate(tier: T?)`
// attribute (line-grep, no full parse), and bins module basenames by tier.
//
// Limitations (raw#10):
//   1. Line-grep (regex `^@quantum_substrate\(tier: (T[123])\)`) — does
//      NOT walk multi-line comment escapes. Modules embedding the
//      attribute string in a docstring will misclassify.
//   2. One attr per fn — fn with multiple @quantum_substrate (illegal but
//      not enforced at parse-time) → first wins.
//   3. Module file may declare multiple substrate-tagged fns; module is
//      classified by the *highest* observed tier (T3 > T2 > T1).
//   4. Result map keys: "T1" / "T2" / "T3" / "untagged".
//   5. Suffix match identical to registry_scan_dir (.hexa case-sensitive).
//   6. Returns {} on missing dir (silent, parallels existing convention).
pub fn registry_classify_substrate(dir: string, suffix: string) -> map { ... }

// registry_dispatch_by_tier(dir, suffix, want_tier) -> map
//
// Higher-level helper: return name → path map filtered to a single tier.
// Wraps registry_build_dispatch + registry_classify_substrate.
pub fn registry_dispatch_by_tier(dir: string, suffix: string, want_tier: string) -> map { ... }
```

**Cross-repo impact:** `nexus/modules/qrng/__registry.hexa` (currently 339 LOC of hand-rolled switch per the autodiscover comment block L5-9) shrinks to a single `registry_dispatch_by_tier(modules_dir, ".hexa", "T1")` call. Same pattern applies to the qmirror engine_* dispatcher.

## 1.5 Why P2 (not P1, not P3)

| Question | Answer |
|----------|--------|
| Why not P1 (alongside qmirror Phase 1)? | qmirror Phase 1 ships 3 substrate modules total (`engine_aer`, `tomography`, `entropy`). 3 modules do not motivate an autodiscover-typed registry — a hand-written 3-arm dispatch is shorter than the attr machinery. Registry autodiscover only earns its keep at ≥6 substrate modules. |
| Why not P3 / postpone indefinitely? | Phase α+2 lands qmirror Phase 2 (`engine_cirq`, `engine_mps`, `iit_mip`, `chsh`) — substrate count crosses 6. At that point hand-rolled dispatchers begin to duplicate logic across qrng/qmirror/(future) qkd modules. P2 land is ROI-positive precisely at that crossover. |
| Why bind tier semantics into the attr at all (vs `@substrate("kind") + tier as struct field`)? | Tier is the *only* axis the registry autodiscover consumer cares about. Encoding it in the attr lets the consumer be a line-grep (no hexa-lang parser dependency in the consumer) — see §1.4 limitation 1. A free-form string `kind` would force the consumer to re-parse semantics per-deployment. |

## 1.6 Implementation cost estimate

| Component | Files touched | Net LOC | Risk band |
|-----------|---------------|---------|-----------|
| hexa-lang parser branch | `self/parser.hexa` | +25 | **low** (mirrors `@symbol`/`@link`) |
| ai_native_pass classification | `self/ai_native_pass.hexa` | +30 | **low-medium** (must not reorder existing M-numbers) |
| AOT C codegen comment-emit | `self/build_c.hexa` | +5 | **low** |
| Test cases (4) | `self/test_bootstrap_compiler.hexa` | +60 | **low** |
| `registry_classify_substrate` + tier dispatch | `stdlib/registry_autodiscover.hexa` | +120 | **medium** (line-grep regex robustness) |
| stdlib test for classifier | `stdlib/test/test_registry_substrate.hexa` (new) | +80 | **low** |
| nexus retrofit (5 modules) | `nexus/modules/qrng/{anu,hardware_qrng}.hexa` + `qmirror/engine_{aer,cirq,mps}.hexa` (cycle-coupled — qmirror modules might not exist yet at land time) | +5 per file = +25 | **low** (additive lines only) |
| **Total (hexa-lang + stdlib)** |  | **~320 LOC** | |
| **Total (with nexus retrofit, conditional on Phase 2 land)** |  | **~345 LOC** | |

## 1.7 Backward compatibility

- **Existing 13 official attrs:** zero impact. `@quantum_substrate` is name-namespaced.
- **Existing nexus convention attrs (`@tool`, `@usage`, `@sentinel`, `@resolver-bypass`):** zero impact. Stack independently.
- **Existing `tier: int = 0|1|3` struct field:** the field stays. The attr is *redundant metadata* on the function, not a replacement for the struct field. Two-source-of-truth risk noted under §1.9.
- **Existing modules without the attr:** continue to work identically; absent attr = `untagged` bin in registry classifier.
- **AOT codegen:** the new comment line in generated C is informational and ignored by `cc`.

## 1.8 Migration plan for existing modules

**Phase A (single PR, post-attr-land):** Retrofit the 5 currently-IMPLEMENTED substrate modules in one sweep:
- `nexus/modules/qrng/anu.hexa` → add `@quantum_substrate(tier: T1)` to `qrng_anu_pull`
- `nexus/modules/qrng/hardware_qrng.hexa` → add `@quantum_substrate(tier: T1)` to `qrng_hw_pull`
- `nexus/modules/qrng/mock_qrng.hexa` → **deliberately none** (T0 mock — see §1.2)
- (qmirror modules retrofit deferred to that cycle's own land PR)

**Phase B (continuous):** New substrate modules ship with the attr from creation. Honest-C3 lint rule (§3.6 of predecessor review — `tool/honest_c3_lint.hexa`) extended with a check: if a fn name matches `qrng_*_pull` / `engine_*_run` heuristic AND module path under `nexus/modules/{qrng,qmirror,qkd}/`, emit warning when `@quantum_substrate` is missing.

**Phase C (deprecation, optional, post-stable):** Once registry classifier becomes the *primary* dispatch surface, the `tier: int` struct field on `QrngSourceMeta` etc. becomes redundant. Mark with `@deprecated("use @quantum_substrate(tier:) on the fn instead")` — but only if Phase A+B have been stable for 2+ cycles and the attr-based path is genuinely the primary read.

## 1.9 Honest C3 caveats (substrate attr)

1. **Two-source-of-truth interim.** During Phase A→B, `tier: int` struct field and `@quantum_substrate(tier: T?)` attr coexist. Drift is possible (struct field says T1, attr says T2). No compile-time check enforces equivalence — they're at different abstraction layers (instance metadata vs. fn classification). Mitigation: Phase A retrofit PR review explicitly verifies parity; Phase C deprecation eventually removes the struct field.
2. **Line-grep classifier is fragile.** §1.4 limitation 1 — multi-line comment containing the literal string `@quantum_substrate(tier: T2)` would misclassify. Mitigation: registry classifier doc-comment warns; integration test covers comment-embedded false-positive.
3. **Tier enum is closed.** T1/T2/T3 hard-coded. Adding T4 (e.g., "post-quantum cryptographic substrate") = parser change. Mitigation: 3-tier closed set is appropriate for the foreseeable physical-substrate taxonomy (live external / local sim / remote hardware); extension is a deliberate cycle event, not a shortcut.
4. **AI-native intent paradigm tension.** spec §3.12 (`intent/generate/verify/optimize`) envisions auto-attr-injection. Should the AI compiler auto-inject `@quantum_substrate` based on body content (e.g., spotting `exec("curl https://qrng.anu.edu.au")` → infer T1)? Predecessor review caveat 4 flagged this; this spec leaves the policy decision to the AI-native subsystem owner (recommendation: **manual-only** at land — auto-injection waits one more cycle).
5. **Registry classifier dependency-cycle risk.** If `stdlib/registry_autodiscover.hexa` consumers ever live in `self/` (compiler internals), and the compiler itself uses `@quantum_substrate`, a chicken-and-egg load order emerges. Mitigation: **prohibit** `@quantum_substrate` use in `self/` (compiler) and `stdlib/` — substrate attr is exclusively a nexus-application-layer concern. Document in the attr's own doc-comment.
6. **`@deprecated` attr is itself parser/classification-only.** If Phase C deprecation messages are needed, Phase α+2 must also land `@deprecated` runtime-warning emission (currently ai-native-attrs.md L131 says "호출 시 경고 출력은 미구현"). This is a hidden prerequisite.

---

# 2. native `complex` primitive — full spec

## 2.1 Type signature

Add `complex` as the 9th primitive (current count σ-τ = 8 per spec.md §2). Doing so **breaks the σ-τ = 8 invariant** documented in spec.md §2 — see §2.6 below for the n=6-arithmetic justification.

```hexa
// Type form
let z: complex = 1.0 + 2.0i      // canonical literal — float + float * imaginary unit
let zero: complex = 0.0i         // pure imaginary literal allowed
let real_as_complex: complex = 3.0 + 0.0i   // explicit real-only complex

// Equivalent struct form (current P0/P1 era)
struct Complex { re: float, im: float }
let z2: Complex = Complex { re: 1.0, im: 2.0 }
```

**Internal representation:** two contiguous IEEE 754 f64 (re, im), 16 bytes. Same memory layout as a hexa `struct Complex { re: float, im: float }` — guaranteeing zero-copy interop with existing struct-wrap call sites during migration.

## 2.2 Literal grammar

```ebnf
complex_literal  ::=  float_literal "+" float_literal "i"
                   |  float_literal "-" float_literal "i"
                   |  float_literal "i"                       // pure imaginary
                   |  "(" float_literal "," float_literal ")" "c"   // tuple-form fallback (parser-easy)
```

**Lexer impact:** the literal `1.0+2.0i` requires the lexer to recognize `i` immediately following a float as a **type suffix**, NOT an identifier. This is the single hardest lexer change in this spec — current hexa lexer treats trailing alphabetics as identifier-start. Cleanest path: lex `<float>i` as a fused `ImagLiteral` token; parser composes `<float> "+" <ImagLiteral>` → `ComplexLiteral`. Tuple-form `(re, im)c` exists as a fallback for any module the lexer change is too invasive for.

## 2.3 Built-in arithmetic operators

| Op | Hexa surface | Semantics |
|----|--------------|-----------|
| `+` | `complex + complex` | `(a+bi) + (c+di) = (a+c) + (b+d)i` |
| `-` | `complex - complex` | analogous |
| `*` | `complex * complex` | `(a+bi)·(c+di) = (ac-bd) + (ad+bc)i` |
| `/` | `complex / complex` | `(a+bi)/(c+di) = ((ac+bd) + (bc-ad)i) / (c²+d²)` |
| `==` | `complex == complex` | exact float equality on both components (raw#9 honest — no epsilon) |
| `!=` | `complex != complex` | analogous |
| `+`, `-`, `*`, `/` | `complex op float` and `float op complex` | implicit promote float → `(f, 0.0)` |

**No `<` / `>` / `<=` / `>=`** — complex numbers are not totally ordered. Compile-time error.

## 2.4 Built-in unary / utility functions

| Function | Signature | Semantics | Notes |
|----------|-----------|-----------|-------|
| `complex(re: float, im: float)` | constructor | returns `complex` value | named constructor for non-literal contexts |
| `re(z: complex)` | float | real part | |
| `im(z: complex)` | float | imaginary part | |
| `conj(z: complex)` | complex | `(a+bi) → (a-bi)` | |
| `abs(z: complex)` | float | `sqrt(re² + im²)` | overload of existing `abs(int)` / `abs(float)` |
| `arg(z: complex)` | float | atan2(im, re) | radians, range (-π, π] |
| `norm_sq(z: complex)` | float | `re² + im²` (no sqrt — for inner-product hot loops) | |
| `polar(r: float, theta: float)` | complex | `r·(cos θ + i sin θ)` | factory |

**Stdlib (not built-in) extensions** in `stdlib/math.hexa` (additive):

| Function | Signature |
|----------|-----------|
| `cexp(z: complex)` | complex (`e^z = e^a · (cos b + i sin b)`) |
| `clog(z: complex)` | complex (principal branch) |
| `csqrt(z: complex)` | complex |
| `cpow(z: complex, w: complex)` | complex (= `cexp(w * clog(z))`) |
| `csin / ccos / ctan` | complex |

## 2.5 Linalg / matrix interaction (the **cascading cost**)

Adding `complex` without complex-typed BLAS-lite kernels **strands every quantum-state-vector / density-matrix call site**. The cascade is non-optional:

| Surface | Real (`float`) version exists at | Complex extension required |
|---------|----------------------------------|----------------------------|
| `sgemm` (M·N matmul) | `linalg/reference.hexa::sgemm_ref`, `linalg/ffi.hexa::sgemm_ffi` | **`cgemm`** ref + ffi (~80 LOC ref, ~50 LOC ffi or ref-defer) |
| `sgemv` (M·N matvec) | `linalg/reference.hexa::sgemv_ref`, `ffi.hexa::sgemv_ffi` | **`cgemv`** ref + ffi (~50 LOC ref) |
| `sdot` (real inner product) | `linalg/reference.hexa::sdot_ref` | **`cdotc`** (conjugate inner product, x* · y) + **`cdotu`** (unconjugated) — quantum amplitude inner product needs cdotc (~30 LOC each) |
| `saxpy` (scaled add) | `linalg/reference.hexa::saxpy_ref` | **`caxpy`** (~25 LOC) |
| `snrm2` (Euclidean norm) | `linalg/reference.hexa::snrm2_ref` | **`cnrm2`** (returns `float`, not `complex` — matches BLAS) (~30 LOC) |
| `linalg_backend_name()` | `dispatch.hexa` | extend env var: `HEXA_LINALG_BACKEND=ref\|ffi\|auto` already covers complex transparently |
| matrix construct | `matrix/construct.hexa` | `complex_zeros(m, n)`, `complex_eye(n)`, etc. (~40 LOC) |
| matrix stack | `matrix/stack.hexa` | hstack/vstack on complex arrays — generic if array element-type-agnostic (likely 0 LOC if generic, ~30 LOC if not) |
| native runtime builtin | `matmul(A, B, m, n, k)` (real) | **no complex builtin in current runtime** — `cgemm_ffi` defers to `cgemm_ref` until runtime gets `cmatmul`. Honest perf caveat. |

**Linalg/matrix net new LOC:** **~340 LOC** across 5+ files. **Test additions:** 5 cgemm/cgemv/cdotc/caxpy/cnrm2 tests + ref-vs-ffi parity tests.

## 2.6 Why P2 (not P1)

| Question | Answer |
|----------|--------|
| Why not P1 alongside qmirror Phase 1? | Predecessor review §2.4 explicitly classifies as P2: "struct `Complex { re: float, im: float }` + parallel `[Complex]` array" is sufficient for Aer amplitude binding through tomography. The struct-wrap is *honest C3* — no precision loss, no semantic gap. The cost is ergonomic only. |
| Why not P3 / never? | At ≥3 callsites of complex-arithmetic-heavy code (`tomography.hexa` ρ-matrix Cholesky, `iit_mip.hexa` partition trace, `chsh.hexa` correlator algebra), the per-callsite parallel-array bookkeeping (`re_out[i] = re_a[i]*re_b[i] - im_a[i]*im_b[i]; im_out[i] = ...`) becomes a *correctness hazard* — easy to swap a sign and pass tests on the no-op case. Native primitive eliminates the class. |
| Why does spec.md §2 σ-τ=8 invariant break? | spec.md derives 8 primitives from the n=6 arithmetic identity σ(6)-τ(6) = 12-4 = 8. Adding `complex` makes 9. **Resolution:** complex is *not* a fundamental primitive in the same sense — it's a **product type fixed at 2 floats**. The n=6 spec language can be amended to read "8 fundamental + 1 quantum-extension type" or the count revised to σ-τ+1 = 9 with a footnote. This spec recommends the **footnote path** (annotate, do not destabilize the n=6 derivation). |
| Why fuse with linalg complex extension? | Without `cgemm`/`cgemv`/`cdotc`, the `complex` primitive gives quantum-circuit code a nicer literal but no path to do real work — every state-vector evolution still falls back to manual `(re, im)` array twiddling. Either both or neither. |

## 2.7 Implementation cost estimate

| Component | Files | LOC | Risk band |
|-----------|-------|-----|-----------|
| Lexer: `<float>i` token fusion | `self/lexer.hexa` | +40 | **medium-high** (every numeric literal path interacts) |
| Parser: ComplexLiteral node, type annotation `complex` | `self/parser.hexa` | +60 | **medium** |
| Type system: 9th primitive entry, ordering rejection (`<` etc.) | `self/parser.hexa` (type table), `self/ai_native_pass.hexa` | +50 | **medium** |
| Interpreter: complex value boxing, 4 binary ops, 4 unary builtins | `self/interpreter.hexa` | +180 | **medium** |
| AOT C codegen: emit as `_Complex double` (C99) or as `struct { double re, im; }` | `self/build_c.hexa` | +120 | **high** (C99 _Complex is gcc/clang OK, MSVC not — pick struct path for portability) |
| ai_native_pass classification | `self/ai_native_pass.hexa` | +30 | **low** |
| stdlib `math.hexa` complex transcendentals (cexp, clog, csqrt, cpow, csin, ccos, ctan) | `stdlib/math.hexa` | +120 | **low-medium** |
| linalg complex kernels (cgemm/cgemv/cdotc/cdotu/caxpy/cnrm2 ref + ffi-defers) | `stdlib/linalg/{reference,ffi,dispatch}.hexa` | +240 | **medium** |
| matrix complex constructors | `stdlib/matrix/construct.hexa` | +60 | **low** |
| Tests | `self/test_bootstrap_compiler.hexa` + new `stdlib/test/test_complex_*.hexa` | +250 | **low** |
| **Total** | **~10 files** | **~1150 LOC** | |

**This is a genuinely large patch.** Predecessor review caveat 6 sized it at "6+ file scope, 수백 LOC" — with linalg/matrix cascade fully accounted for, ≥1100 LOC is the realistic figure.

## 2.8 Backward compatibility

- **Existing 8 primitives:** unchanged.
- **Existing modules using `struct Complex { re, im }`:** continue to work. Memory layout parity (§2.1) means a future migration helper can `unsafe_cast<struct Complex, complex>()` zero-copy if AOT codegen picks the struct emission path.
- **Existing real-typed linalg (`sgemm` etc.):** zero impact. Complex kernels are name-distinct (`cgemm`, `cdotc`).
- **AOT C codegen choice — `_Complex double` vs `struct { double, double }`:** **recommend struct path** (portable, no MSVC blocker, identical perf on x86_64/ARM64 with `-O2`). C99 `_Complex` would force MSVC users into a separate codepath.
- **JSON serialization:** `json_stringify(z: complex)` emits `{"re": 1.0, "im": 2.0}` (object form). Parsing back is the caller's job (no `json_parse_complex` builtin — keep parse-side dumb).
- **n=6 spec invariant:** §2.6 footnote path preferred. Communicate as "8 fundamental + 1 extension primitive" in spec.md §2 update.

## 2.9 Migration plan for existing modules

**Phase A (concurrent with land):** No retrofit required — existing struct-wrap code keeps working. New code may use either form.

**Phase B (per-module opt-in, 1+ cycle later):** As `tomography.hexa`, `iit_mip.hexa`, etc. land in qmirror Phase 2/3, they use the native `complex` from creation. The parallel `[float] re + [float] im` pattern from predecessor review §2.4 is **forbidden in new modules** post-land (lint rule).

**Phase C (eventual struct sunset, optional, multi-cycle horizon):** If/when struct-wrap pattern is fully drained from the tree, mark `struct Complex` as `@deprecated` in any reference impls. Not urgent — the two coexist forever cheaply.

## 2.10 Honest C3 caveats (complex primitive)

1. **n=6 spec.md invariant breakage.** §2.6 — complex makes 9th primitive. Either the spec.md derivation language is amended (preferred) or the σ-τ=8 → σ-τ+1=9 numerology is officially deprecated. Either choice is a *philosophical* commit beyond a stdlib patch.
2. **Lexer regression risk is the highest single risk in this spec.** §2.7 — `<float>i` fusion touches every numeric token rule. Test matrix must cover: `1.0i`, `1.0+2.0i`, `1.0 + 2.0i` (whitespace), `1.0+2.0` (no `i` — must remain float-add), `i` as identifier in user code (must remain identifier when not preceded by float), `int + float * i` (operator precedence interaction).
3. **AOT codegen MSVC concern.** §2.8 — picking `struct { double, double }` over `_Complex double` is a deliberate portability choice that costs perhaps 5-10% on aggressive auto-vectorization paths gcc can do with `_Complex`. Honest perf disclosure.
4. **No complex runtime builtin.** §2.5 — `cgemm_ffi` defers to `cgemm_ref` indefinitely until runtime grows `cmatmul`. Real `sgemm_ffi` benefits from native `matmul` builtin. Complex kernels run at reference speed only — perf parity with real BLAS is **out of scope** for this P2 land.
5. **Cascading downstream pressure.** Once `complex` lands, every numerical stdlib that has a real-typed kernel will face a "where is the complex variant?" pressure. `nn.hexa`, `optim.hexa`, FFT (when added), signal processing — the requested-extensions queue grows. This spec covers linalg + math transcendentals only; downstream complex extensions are explicitly *not* committed to.
6. **JSON round-trip is asymmetric.** §2.8 — emit is built-in, parse is caller-side. A user calling `json_parse(s)` on `{"re": 1.0, "im": 2.0}` gets back a `map`, not a `complex`. Convention-only; no enforcement.
7. **Equality is exact-float (raw#9 honest).** §2.3 — `z1 == z2` requires bit-identical `re` and `im`. Numerical-physics code expecting tolerance must call `abs(z1 - z2) < eps` explicitly. This matches existing `float` equality behaviour and is documented but easy to miss.

---

# 3. Combined recommended landing cycle

**Phase α+1 (current cycle, qmirror Phase 1+2 enablement):**
- P0 + P1 stdlib patches from predecessor review (`proc_run_with_stdin`, `json_stringify`, `http_get_with_headers`, `stdlib/bytes.hexa`)
- qmirror Phase 1 + Phase 2 modules ship using P0/P1 stdlib + `struct Complex` + `tier: int` field convention
- **No P2 work in this cycle.**

**Phase α+2 (next cycle, stdlib quarter — recommended P2 land window):**
- `@quantum_substrate(tier)` attr: parser + ai_native_pass + registry_classify_substrate + 5-module nexus retrofit (Phase A migration)
- (decision point) native `complex` primitive: land **only if** qmirror Phase 2 actually showed ≥3 callsites of parallel-array bookkeeping noise. Otherwise defer to Phase α+3.
  - If complex lands: linalg cgemm/cgemv/cdotc/caxpy/cnrm2 land **same PR** (no half-state where primitive exists without kernels)

**Phase α+3 (later, conditional):**
- `complex` primitive land if deferred above
- `@quantum_substrate` Phase C struct-field deprecation if Phase A+B stable

**Anti-pattern to avoid (raw#9 violation):** landing `@quantum_substrate` solo without the registry consumer extension, or landing `complex` primitive without the linalg complex kernels. Both produce a "feature exists but does no work" surface — the worst kind of stdlib bloat.

---

# 4. Honest C3 (raw#91, ≥5 caveats — **document-level**, on top of per-section caveats)

1. **This is forward-spec, not a commitment.** No code is being changed and no roadmap entry is being created by this document. The substrate review predecessor explicitly flagged both items as P2 with "land only with prerequisite" gates; this spec just makes the prerequisites concrete enough to evaluate later.

2. **Cascading-cost honesty matters more than the headline LOC.** §1.6 says ~320 LOC for the attr but the *retrofit* of 5 nexus modules and the *registry consumer extension* are what actually justify the patch. The attr alone is ~60 LOC of dead code without the consumer. Land discipline = atomicity (attr + consumer + ≥1 retrofit in one PR).

3. **`complex` cost is in §2 the largest single stdlib commit ever proposed.** §2.7 ~1150 LOC. Predecessor review caveat 6 sized at "수백 LOC" — when linalg+matrix+math+lexer+codegen are summed honestly, the figure crosses 1k. This is not a "quick win"; it's a quarter-scale stdlib feature.

4. **n=6 spec philosophy commitment.** §2.6 — adding the 9th primitive is a public deviation from the spec.md §2 "8 primitives derived from σ-τ" derivation. Hexa-lang's identity is partly mathematical aesthetic; this commit costs aesthetic capital and should be acknowledged at land.

5. **Both items are convenience, not unblockers — by design.** Predecessor review confirms qmirror Phase 1+2+3 (through calibration anchor) ships fine without either. The case for landing P2 at all is: *cumulative* future-cycle ergonomics, not present-cycle delivery. If `nexus.qmirror` is the only consumer ever, P2 might never earn its keep.

6. **Registry classifier line-grep is the weakest link.** §1.4 + §1.9.2 — implementing the consumer as a hexa-lang full-parse-pass instead would be more robust but introduces a stdlib → compiler internals dependency (caveat §1.9.5). The line-grep choice trades robustness for layering cleanliness; this is a deliberate trade-off, not an oversight.

7. **AI-native auto-injection policy is unresolved.** §1.9.4 — both `@quantum_substrate` and complex-typed inference are candidates for AI-native auto-derivation (spec §3.12 `intent` block). Punting the policy to P3 leaves a known gap; reviewers should explicitly confirm "manual-only at land" in the P2 PR description.
