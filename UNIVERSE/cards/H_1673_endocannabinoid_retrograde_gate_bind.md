# H_1673 — Retrograde Coincidence Gate (postsynaptically-detected, presynaptically-applied within-pass feedback)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** synaptic neuromodulation / endocannabinoid retrograde signaling (DSI/DSE) — within-pass backward coincidence-gated fixed point
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `endocannabinoid_retrograde_gate_bind`

## Mechanism

Two sub-steps per block. Forward: postsynaptic unit p integrates both legs p=f(a+b) and computes a coincidence detector c=relu(a·b − θ) (high only when BOTH co-drive). Retrograde: c is sent BACKWARD as a multiplicative gain on the PREsynaptic inputs of the next micro-iteration within the SAME forward pass — DSI-style suppression a'=a·(1−α·c_pool), b'=b·(1−α·c_pool), or DSE-style capture a'=a·(1+α·c). Iterate 2–3 micro-steps to a fixed point. The retrograde signal is a sign-flipped, coincidence-triggered messenger flowing opposite to the feedforward path; only joint-supported bindings survive the loop, spurious single-leg activations are retrogradely vetoed.

## Why it crosses the binding wall

attention depth stacks feedforward transforms only — there is no backward, coincidence-gated modulation of the INPUTS within a pass, so a layer cannot retroactively veto a representation that lacked joint support (single-leg activations propagate). The retrograde loop builds a within-pass fixed point that is a function of the JOINT state (c∝a·b); single-leg ablation → c=0 → no retrograde modulation → binding-specific suppression vanishes → the unbound failing baseline returns. Ablation logic: (1) cut the retrograde EDGE — apply c as an ordinary feedforward gate instead of backward onto inputs; if conjunction selectivity drops, the DIRECTION (not just the coincidence detector) is load-bearing — this is what distinguishes it from any feedforward gate; (2) replace c=relu(a·b−θ) with c=relu(a+b−θ) (additive trigger) → conjunction specificity drops, isolating the product trigger. Both restoring failure = the retrograde coincidence loop is the operator. Distinct from fast_weight_hebbian (forward persistent weight write) and short_term_facilitation (use-dependent presynaptic enhancement, no coincidence-triggered backward sign-flip).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, frozen-first, CPU. Same synthetic 2-factor held-out-combo task. Implement the 2–3-step retrograde fixed-point combine vs a DEPTH-MATCHED 2–3-step feedforward block (same param count, no backward edge). Pre-registered bar: retrograde held-out novel-combo CE lower by ≥0.15 nats than the depth-matched control AND fixed-point convergence |state_{t+1}−state_t|<1e-3 within 3 steps. GO only if removing the backward edge (ablation 1) erases the gain — the feedforward-matched control MUST fail while retrograde passes, proving direction not extra compute.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated, NOT fired. 303M custom mouth: conv trunk + retrograde-gate blocks (3 micro-iterations, α learned per block). 4-cell corpus, held-out DESCENT + engine-native G1/G6. Control arm = identical params with retrograde replaced by extra feedforward depth (depth-matched) to prove mechanism not FLOPs. 1×H100 ~$35. Frozen bar: G6 fals > 0 AND > depth-matched control. PULL ckpt before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
