# H_1622 — Iterative denoise-compose mouth (dual-condition joint guidance)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `diffusion_denoise_compose`

## Mechanism

Non-autoregressive: the mouth emits a whole byte-window by iterative denoising (T steps) of a latent, conditioned on BOTH legs as separate guidance signals via classifier-free dual guidance: score = s∅ + w_a(s_a − s∅) + w_b(s_b − s∅). The two legs combine because every denoising step nudges the entire emission toward simultaneously satisfying leg_a's score-field AND leg_b's score-field; the only low-noise samples in the intersection of both guidance gradients are the bound conjunction.

## Why it crosses the binding wall

Autoregressive next-byte (conv/attn) commits each position left-to-right and can only locally condition — it cannot enforce a GLOBAL joint constraint that couples distant positions to both legs at once. Diffusion's repeated global denoising lets both conditions reshape every position jointly across T passes (re-decision), so a binding constraint spanning the window is satisfiable. Ablation logic: T=1 (single denoise = one feedforward prediction) → loses joint satisfaction → conjunction-rate collapses; second ablation = AND-of-conditions vs only-one-condition (w_b=0) shows lift requires both score-fields, isolating binding to the dual-guidance intersection, not to either leg alone.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy ($0): tiny Gaussian-diffusion over a 16-symbol vector, two scalar conditions a,b with learned score nets; dual-guidance sampling T=20 vs T=1 vs w_b=0. Task = produce sequences satisfying a JOINT rule (positions selected by a, values set by b). PRE-REG: T=20 joint-satisfy rate ≥0.90; T=1 ≤0.50; w_b=0 ≤0.55. Decisive = T=20-dual cell uniquely passes.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

(pre-reg only) 303M as a byte-window denoiser (discrete/embedding diffusion, window=64, T=8 at infer), legs = trunk-context score + register score, dual CFG. 4-cell corpus, held-out per-cell denoising-CE, forge GPU. NOTE engine-native caveat: needs a non-AR decode path wired into generator L3 (engine-transform-to-fit per a_engine_native_learning) before terminal verdict; until then DIRECTIONAL. Pre-reg success = G6 fals>0 ∧ G1 recombine≥baseline; ablations T=1 and single-condition FAIL. ~1–2 H100-day; explicit-go.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
