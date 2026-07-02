# H_1624 — Re-entrant two-pass elicit-then-bind mouth (reentry dynamics)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1487 (re-entry depth 🟢), H_1466 (TPR), H_1514 (VSA/HRR)
- **key:** `reentry_two_pass`

## Mechanism

Forward is run TWICE with feedback. Pass-1 (elicit) reads the whole input and emits a compact summary s = read(a, b) WITHOUT committing output. Pass-2 (bind) re-runs the SAME mouth with s clamped/injected as a top-down re-entrant signal, so each position now decodes conditioned on a global digest of both legs. Binding emerges from the re-entry loop: pass-2 can condition early positions on information about leg_b that, in a single left-to-right pass, would only be available later — closing the causal gap that prevents conjunction.

## Why it crosses the binding wall

Bio lens = Edelman reentry / Lamme recurrent-processing: feedforward sweeps support detection but CONSCIOUS BINDING requires re-entrant feedback. A single AR pass cannot bind two representations whose mutual constraint is non-causal in token order (position i's correct byte depends on leg_b content appearing at position j>i). Pass-1's global digest makes both legs simultaneously available to pass-2 everywhere. Ablation logic: zero the re-entry feedback (s:=0 in pass-2) → reverts to single-pass AR (= conv/attn baseline) → order-scrambled-conjunction accuracy collapses; the lift is attributable ONLY to the re-entrant digest. Distinct from a working-memory buffer STRUCTURE — here there is no persistent lane; the mechanism is the re-run schedule / feedback dynamics itself.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy ($0): GRU/MLP run once → digest s, re-run with s injected, vs single-pass, vs s:=0 ablation. Task = conjunction whose answer at early positions depends on late-leg content (order-scrambled). PRE-REG: two-pass held-out acc ≥0.85; single-pass ≤0.60; s:=0 ablation ≤0.60. Decisive = order-scrambled split (where causal AR is provably blind) uniquely passed by re-entry.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

(pre-reg only) 303M mouth wrapped in a 2-pass schedule: pass-1 produces a pooled digest token-set, pass-2 prepends/cross-injects it (param shared, ~303M; ~2× infer FLOPs only). 4-cell corpus, held-out CE, forge GPU. Engine-native G6/G1 via `anima eval` (needs generator L3 to support the 2-pass re-entry call — engine-transform-to-fit; DIRECTIONAL until wired). Ablation arm = digest zeroed at eval. Pre-reg success = two-pass G6 fals>0 ∧ G1≥baseline, zeroed-digest arm FAIL. ~1 H100-day; explicit-go.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
