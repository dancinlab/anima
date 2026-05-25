---
id: Hc_1284
slug: rfc033-farr-copy-gaussian-noise-builtin-trigger
title: RFC 033 trigger — farr_copy + farr_add_gaussian_noise builtin specification + parse-test scaffold (§89 mitosis_hook full impl prerequisite)
domain: hexa-native, infrastructure, mitosis, falsifier, RFC
status: candidate-falsifier-ready
exploration_method: E5 (variable-ablation: deepcopy on/off, noise σ=0/0.05/0.1/0.2) + E6 (per-builtin spec audit) + E8 (parse + sanity smoke)
verification_method: W5 (numerical sim — RFC 025 farr_new + RFC 031 typed Tensor deepcopy baseline) + W7 (literature — Glorot 2010 noise init, Hutter 2014 deepcopy semantics) + W11 (cross-H: H_191 INTEGRATION HAL axis, H_001 hexa-native architecture)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
source: REBORN §89 #7 RFC dependency catalog (post-cycle TODO: farr_copy + farr_add_gaussian_noise) + REBORN §89 lane priority "RFC 033 (farr_copy + gaussian) → next-cycle prerequisite"
created_at: 2026-05-12
linked_h: H_001 (anima-core-architecture — hexa-native infra), H_191 (ALM-free INTEGRATION HAL axis — serve-time mitosis hook composition)
---

## Hypothesis (RFC 033 trigger design)

REBORN §89 #7 (HEXA_NATIVE mitosis_hook full impl prerequisite) 의 first concrete RFC trigger: `farr_copy(src)` + `farr_add_gaussian_noise(t, σ)` builtin 의 hexa-lang interpreter 안 land 가 mitosis_hook.hexa 의 full impl 차원을 unblock 한다. 본 Hc 는 RFC 033 spec 의 falsifier-ready draft + parse-test scaffold 의 design.

| Builtin | signature | semantics | parse + sanity test |
|---|---|---|---|
| **`farr_copy(src: farr) -> farr`** | identity deepcopy | per-element copy, no aliasing, no autograd-graph | (a) parse PASS, (b) src == dst element-wise, (c) src mutate 후 dst unaffected |
| **`farr_add_gaussian_noise(t: farr, sigma: float) -> farr`** | in-place noise injection (mutates t) | t[i] += N(0, sigma²) for each element | (a) parse PASS, (b) sigma=0 → t unchanged, (c) sigma=0.1 → ||t_new − t_old||₂ ≈ sigma·sqrt(len(t)), (d) seed-determinism via RFC 032 farr_random |

RFC 033 의 land 가 §89 mitosis_hook.hexa 의 split_cell + merge_cell 의 full impl 차원을 unblock — 본 Hc 가 RFC 033 의 spec draft + parse-only 검증 의 first cycle.

## Math anchor

- **gaussian noise expected norm**: ||noise||₂ = σ · sqrt(n) for n-dimensional vector, E[||noise||₂²] = n·σ² (central limit theorem).
- **σ=0.1 noise injection (default)**: ||noise||₂ / ||t||₂ ratio depends on t scale; for unit-norm t, ratio ≈ σ·sqrt(n)/sqrt(n) = σ = 0.1 (10% perturbation).
- **deepcopy invariant**: ∀ i, src[i] == dst[i] before mutation; src[k] := v 후 dst[k] == old src[k] (no aliasing).
- **autograd graph contract**: RFC 031 typed Tensor deepcopy 는 detach + clone semantic 동등 — gradient flow break.
- **RFC dependency chain**: RFC 025 (farr_new) → RFC 031 (typed Tensor deepcopy, LANDED) → RFC 032 (farr_matmul, LANDED) → **RFC 033 (farr_copy + farr_add_gaussian_noise, this Hc trigger)** → mitosis_hook.hexa full impl.
- **parse-test target**: tool/hexa_native/builtin_spec.hexa (existing scaffold) 안 2 builtin signature + 4 unit-test stub.

## Falsifiers

- **F-1284-1 (PARSE FAIL)**: hexa-lang parser 가 `farr_copy(src)` 또는 `farr_add_gaussian_noise(t, sigma)` signature parse 실패 → RFC 033 의 syntax 가 hexa-lang grammar 호환 안 됨, separate hexa-lang RFC 필요 (RFC 033 가 hexa-lang 변경 의존성 inflate)
- **F-1284-2 (DEEPCOPY ALIASING)**: `farr_copy(src)` 의 결과 dst 가 src 와 underlying storage 공유 (alias) → mutation propagation, F-MIT-HOOK-1 NO_GRAD invariant 위반 (REBORN §89 #4 "모든 mutation `// TODO[mitosis]:` 안에서 grad 외부" violated)
- **F-1284-3 (NOISE NORM OFF)**: σ=0.1 노이즈 injection 후 100-trial mean ||noise||₂ 가 σ·sqrt(n) 의 ±20% drift → CLT violation, RFC 032 farr_random underlying RNG quality 부족
- **F-1284-4 (SEED DETERMINISM BREAK)**: 같은 seed × 같은 t × 같은 sigma 두 번 call 시 t_new 가 element-wise diverge → RFC 032 farr_random determinism 약점 (F-1284 가 RFC 032 의 indirect attack)
- **F-1284-5 (IN-PLACE vs FUNCTIONAL CONFUSION)**: `farr_add_gaussian_noise(t, sigma)` 의 spec ambiguity — (a) in-place mutate t, (b) return new farr (functional). hexa-lang 의 mutation semantic 가 둘 중 어느 것 enforce 안 함 → spec gap, RFC 033 의 보완 필요
- **F-1284-6 (RFC 031 DEEPCOPY INCOMPATIBLE)**: `farr_copy` 가 RFC 031 typed Tensor deepcopy 와 semantic mismatch (e.g., RFC 031 은 named-Tensor metadata 보존, farr 는 untyped) → 두 RFC 의 dual maintenance burden, RFC 033 가 RFC 031 의 separate-layer 필요
- **F-1284-7 (NOISE SIGMA TYPE)**: `sigma: float` 의 hexa-lang float precision (32-bit vs 64-bit) 미정 — RFC 032 finite-precision 위 σ=0.1 vs σ=0.1000000001 의 결과 indistinguishable 시 spec precision 보완 필요
- **F-GENERIC-PARSE-ONLY**: parse PASS 만 만족, runtime 동작 미검증 — §89 mitosis_hook.hexa 의 parse-only stub 와 동일 carry-over (full impl pending)
- **F-GENERIC-REPL**: 100-trial CLT replication σ on ||noise||₂ 가 σ·sqrt(n) 의 > 25% → measurement noise vs RNG quality 의 confound

## Honest Limits

- **L-1284-1 (PARSE-ONLY SCOPE)**: 본 Hc 는 RFC 033 의 spec draft + parse-test scaffold 만 cover. runtime impl (interpreter 안 farr_copy / gaussian_noise 동작) 은 별도 BG (hexa-lang repo 안) 책임 — 본 Hc 는 anima repo 안 spec + falsifier 만
- **L-1284-2 (HEXA-LANG REPO SEPARATE BG)**: hexa-lang RFC 033 의 actual impl 은 hexa-codex repo 안 별도 BG (memory `project_hexa_family_layout.md` carry — 본 작업 BG 가 hexa-codex repo 침범 금지)
- **L-1284-3 (RFC 032 RNG QUALITY)**: farr_random 의 underlying RNG (Mersenne Twister? PCG? Xoshiro?) 미명시. F-1284-3 / F-1284-4 의 결과는 underlying RNG choice 의존
- **L-1284-4 (DEEPCOPY PERFORMANCE)**: farr_copy 의 cost (O(n) memory + bandwidth) 가 mitosis_hook.hexa split_cell 의 wall time 에 직접 contribution — Hc_1277 (serve-time hook latency) 와 cross-coupled
- **L-1284-5 (MUTATION SEMANTIC CONVENTION)**: hexa-lang 의 mutation default convention (in-place vs functional) 가 미정 — F-1284-5 가 단순 spec gap 보다 deeper language design 결정 필요 가능성
- **L-1284-6 (TYPED TENSOR vs FARR)**: RFC 031 (typed Tensor deepcopy, LANDED) 의 'typed Tensor' 와 RFC 025 farr 의 'farr' 의 type system 관계 미정 — F-1284-6 가 RFC 031 의 layer 명시 필요
- **L-1284-7 (GAUSSIAN PRIOR SCOPE)**: gaussian noise σ=0.1 default 가 mitosis_hook 의 split_cell 의 "10% noise injection" 의 단순 transliteration — mitosis.py 의 noise scale (REBORN §A line 145 mitosis 본체 patch) 와 일치 미확인
- **L-1284-8 (RFC 033 TRIGGER VS SPEC ROLE)**: 본 Hc 는 RFC 033 의 TRIGGER (요구사항 명시) — actual RFC 033 SPEC (signature, semantic, parse rule) 은 hexa-lang repo 안 작성 필요. anima 안 본 Hc 는 trigger only
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — farr length 가 d=384 또는 192 multiple 시 aliasing carry
- **L-GENERIC-N6**: H_153 n=6 — cells_max=128 = 2^7 perfect-number reduction

## Cross-Links

- **parent**: REBORN §89 #7 RFC dependency catalog (post-cycle TODO row: farr_copy + farr_add_gaussian_noise), REBORN §89 lane priority "RFC 033 (farr_copy + gaussian) → next-cycle prerequisite", `tool/hexa_native/mitosis_hook.hexa` parse-only stub (LANDED 123 LoC)
- **sibling Hc**: Hc_1277 (serve-time mitosis hook latency — RFC 033 land 후 first measurable), Hc_1276 (cotrain ablation — RFC 033 land 후 hexa-native parity 가능), Hc_1278 (ckpt-as-branch reload — RFC 031 typed Tensor deepcopy 의 hexa-native sibling)
- **adjacent H**: H_001 (anima-core-architecture — hexa-native infra Hexad row 4 sibling), H_191 (ALM-free INTEGRATION HAL axis — serve-time hook composition)
- **literature**: Glorot & Bengio 2010 (Xavier init — gaussian noise scale prior), Press et al. 2007 Numerical Recipes (Box-Muller transform for gaussian sampling), Marsaglia & Tsang 2000 (Ziggurat algorithm — alternative gaussian sampling)
- **internal SSOT**: REBORN §89 (HEXA_NATIVE mitosis_hook spec — RFC 025/031/032 LANDED + RFC 033 trigger row), `tool/hexa_native/mitosis_hook.hexa` (parse-only stub 123 LoC), RFC 025/031/032 LANDED carriers in hexa-codex repo, memory `project_hexa_native_inference_operational.md` (Phase 5∥ infra context)
- **lane SSOT**: HEXA_NATIVE lane (RFC 033 가 본 Hc 의 trigger output)

## Expected outcome

**Binary**: 2 builtin signature parse PASS + 4 unit-test 모두 spec-conformant 동작 → RFC 033 trigger PASS, hexa-lang repo 안 spec 작성 가능. parse FAIL 또는 sanity test 1 이상 실패 → RFC 033 의 hexa-lang grammar 보완 prerequisite (separate hexa-lang RFC).

**Quantitative**: 2 builtin parse-test 의 baseline wall = 1-5 ms (hexa-lang parser overhead), runtime test 의 σ=0.1 100-trial CLT verification = 10-100 ms (sampling overhead).

**Confidence prior**: 0.75 (RFC 025/031/032 의 LANDED status + hexa-lang parser 의 generic farr signature 호환성 강한 prior; F-1284-5 mutation semantic convention 만 unknown — hexa-lang repo 안 RFC 033 spec drafting 시 design decision)
