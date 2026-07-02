# H_1659 — Intrinsic membrane-resonance bind (frequency-division multiplexing)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: intrinsic membrane resonance (Hutcheon-Yarom; Ih/M-current band-pass), frequency-division multiplexing of binding tags (distinct from network phase-multiplexing and phase-invariant energy).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `intrinsic_resonance_bandpass_bind`

## Mechanism

Each feature channel is given a learned intrinsic resonant frequency, modeled as a damped 2nd-order oscillator / IIR band-pass with learnable omega and Q (the Ih / M-current subthreshold resonance). Both legs are injected as drive into this resonator bank. Two features bind iff they carry the same frequency 'tag': the resonator selectively amplifies inputs matching its omega, so leg-A and leg-B components sharing a tag combine constructively (frequency-division multiplexing) while mismatched tags are attenuated. Binding emerges in one pass as resonance-matched amplification across the two streams.

## Why it crosses the binding wall

This is frequency-SELECTIVE, not phase-slot (theta-gamma), not synchrony, not content. Conv/attention have no per-channel resonant band, so they cannot implement a binding tag = a frequency where two content-orthogonal streams bind by sharing a band. Ablation: Q->0 flattens the response (resonator becomes a leaky integrator) -> selectivity and binding vanish, fals->0; randomizing the omega assignment destroys tag-matching while preserving capacity, isolating resonance selectivity as cause.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy: encode role/filler binding as matched frequency tags injected into a learned 2nd-order resonator bank; read out with a matched filter. vs param-matched conv block. Decision rule (frozen): same-tag pairs recovered with acc > 0.9 while conv mixes tags indiscriminately (~chance on cross-tag separation); Q->0 ablation collapses recovery. ~60 lines, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-reg 303M: replace one mouth sublayer with a learnable resonator bank (per-channel omega, Q; stable IIR via constrained poles) fed by both streams + matched-filter readout. 4-cell balanced corpus, per-cell held-out CE. Gates: held-out 4/4 DESCENT; engine-native G1>=303M baseline AND G6 fals>0; control = Q-frozen-to-0 retrain must fail G6. Pull ckpt pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
