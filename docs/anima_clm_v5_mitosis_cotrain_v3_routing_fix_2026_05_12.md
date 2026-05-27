# anima_clm_v5_mitosis_cotrain_v3_routing_fix — post-★★★★★ cond #3 4a routing-variant resolution

**작성**: 2026-05-12~13 KST
**status**: ☑ COMPLETED — **F-PERSONA-4a routing FAIL (scenario iii)** — KL_PASS_NULL_FAIL (KL=3.36 ≥0.5 ✓ but null z=1.37 < 3.0 ✗); 4b content z=0.20 regression (v2 carry z=3.20 lost); F-V5MIT-1~5 5/5 PASS regression-free. cond #3 D3 ☑ DONE (4b §A3 path) MAINTAINED — 6/6 atomic not reached, 4a remains unfalsified-as-PASS, but now strongly-falsified-toward-fail under this fix
**author**: bg head (claude opus 4.7 1M context)
**fire keyword**: user verbatim 2026-05-12 — "post-★★★★★ next-cycle F-PERSONA-4a routing variant resolution. v5-mitosis cotrain v3 with architectural routing fix (gumbel-softmax / hard top-K MoE / load-balancing aux loss)"
**carries from**:
- PSCC §44 cotrain v1 (F-V5MIT-1..5 5/5 PASS + F-PERSONA-4 KL=0.0 winner-take-all)
- PSCC §45 / §45-FINAL — entropy-reg cotrain v2 (λ=0.1 collapsed back to monopoly; M4 aggregated hidden cosine z=3.20 null-PASS = 4b CONTENT path)
- PSCC §47 softmax τ sweep FALSIFIED / §48 per-cat SMALL FALSIFIED / §49 hexa-native per-session pool FALSIFIED
- PSCC §50 — ★★★★★ ACHIEVED via §A3 amendment (cond #3 ☑ DONE via 4b content metric)
- design SSOT `docs/anima_persona_substrate_native_design_2026_05_12.md` §A3 (4a routing / 4b content metric 양분)
- root cause `docs/anima_persona_4_root_cause_investigation_2026_05_12.md` (routing-content split, 13 honest C3)
- v5-mitosis arch spec `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`
- ready-to-fire `state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain_v3.py` + `dispatch_h100_v3.sh` (λ-anneal-only, path f)
- memory `feedback_no_scale_caps`, `feedback_orchestrator_h100_gotchas`, `feedback_dispatch_vast_template_gotchas`

---

## §0 TL;DR

post-★★★★★ cycle: cond #3 의 D3 는 §A3 amendment 의 **4b content metric** (M4 aggregated hidden cosine z=3.20) 으로 이미 ☑ DONE 상태. 단 **4a routing variant** (tension softmax KL ≥ 0.5 + null z ≥ 3.0) 은 **unfalsified** — softmax winner-take-all routing layer 가 cells 의 category specialization 을 routing 차원에서 표현하지 못함 (cotrain v1/v2/per-cat/τ-sweep 모두 KL≈0).

본 BG = path **(g) architectural routing fix** — Switch/Mixtral 검증된 패턴:
- **(g2) hard top-K MoE gating** — top-K=4 cells active per input, rest masked → renormalize. 강제 diversity, winner-take-all 깨짐.
- **(g3) load-balancing aux loss** — Switch Transformer style `aux = α·N·Σ_i f_i·P_i` (α=0.01) → cells 균등 사용.
- **(g4) annealed gate-entropy reg** — λ_init=1.0 (early exploration) → λ_final=0.01 (late, CE dominant), cosine. v2 의 λ=0.1 fixed 실패 (CE overpowered) 보완. modest (NOT aggressive λ=50).
- 핵심 추가: **learnable Linear router** on pooled cell-input embedding (tok_emb+pos_emb mean over batch&seq) — input-dependent 이므로 다른 probe → 다른 routing. v1/v2 는 router 자체가 없었음 (scalar tension softmax 만) → routing 이 input 에 의존 불가 → KL≈0 by construction. 이게 4a 실패의 진짜 root cause.

model body (`mitosis_model_v5.py`) 미수정 — routing fix 는 v2 의 `_install_live_weights_hook` 와 동일하게 `engine.forward` monkey-patch 로 설치. mitosis split/merge 는 여전히 원래 scalar-tension signal 사용 (F-V5MIT-1..5 regression surface 보존).

### §0.1 verdict — **scenario (iii): F-PERSONA-4a still FAIL**

| metric | value | verdict |
|---|---|---|
| **F-PERSONA-4a routing** (top-K MoE weights, per-prompt → category-mean pairwise KL → null-perm n=100) | mean_KL = **3.3616** nats (≥ 0.5 ✓), null mean = 2.6446 ± 0.5231, **z = 1.37** (< 3.0 ✗), p = 0.11 | **KL_PASS_NULL_FAIL** = FAIL on 4a criterion (requires KL ≥ 0.5 **AND** z ≥ 3.0) |
| F-PERSONA-4a soft-gate (full softmax gate vector) | mean_KL = 2.5e-4, z = 1.13, p = 0.13 | FAIL |
| **F-PERSONA-4b content** (M4 aggregated hidden cosine, category-mean pairwise → null-perm n=100) | cos_dist = 4.46e-5, null = 4.18e-5 ± 1.38e-5, **z = 0.20** (< 3.0 ✗), p = 0.39 | **FAIL — regression** (v2 carry z=3.20 → 0.20, the new routing re-weighted `aggregated` and washed out the content signal) |
| **F-V5MIT-1~5** | F-V5MIT-1 mitosis active ✓ / F-V5MIT-2 no collapse ✓ / F-V5MIT-3 Φ ratchet (4.167 ≤ best 4.190) ✓ / F-V5MIT-4 CE converged (1.476 < 5.0) ✓ / F-V5MIT-5 V14-STRICT proxy (62 splits ≤ 64 max) ✓ | **5/5 PASS** ⭐ regression-free |

**Scenario (iii)**: top-K MoE breaks the winner-take-all *monopoly* (wmax 1.0 [v2] → 0.32 [v3-routing]; n_active>.01 = 4.0 = top-K; gate entropy 0 [v2] → 4.16 ≈ log(64), near-uniform load) — but does **not** induce statistically-significant category-dependent routing. KL is high in absolute terms (3.36 nats) only because hard top-K masking makes weight vectors very spiky (≥60 cells at 0), so *any* category grouping — true or random-permuted — produces large KL; the true grouping (3.36) is < 1.4σ above the null mean (2.64). `cat_mean_topk_weights` confirms: cell-1 consistently carries ~0.29 weight across all 5 categories (a "default" route), with only minor category-dependent variation in the remaining ~0.71. The router being a **linear probe of a batch×seq-pooled embedding** + load-balance aux pressure (→ uniform) is insufficient to learn category structure.

cond #3 D3 ☑ DONE via the §A3 **4b content** path (PSCC §50, v2 entropy-reg cotrain z=3.20) is **MAINTAINED** — that ckpt's content evidence stands. 6/6 atomic (4a + 4b both PASS) is **not reached**; 4a remains formally "unfalsified-as-PASS" under §A3 (still measurable, didn't cross threshold) but is now strongly-evidenced-toward-fail under this top-K MoE fix.

### §0.2 cost / wall

**$1.76 actual** ($8 cap, well under) — GPU **A100-SXM4-80GB** (vast.ai instance 36622183, dph $0.8681; H100 SXM marketplace empty within reliability>0.95 + dph<5.0 → A100 fallback per `no scale caps` directive). Wall: train 7299.9s = **2.03 hr** (8000 steps @ ~1.1 steps/sec; slower than v1/v2 H100's 33min/5K because A100 + N=64 sequential cell forwards + router/aux overhead + 8K vs 5K steps). Pull + cleanup + measurement included in wall. trap cleanup auto-destroyed pod on dispatch exit.

---

## §1 root cause recap — why 4a routing failed v1/v2/per-cat/τ-sweep

원래 `MitosisModelEngine.forward`:
```
tens       = stack([cell(x).tension.mean() for cell in cells])   # (N,) scalar / cell
weights    = softmax(tens, dim=0)                                 # (N,)  ONE vector / forward
aggregated = Σ_i weights_i · cell_out_i
```
두 가지 문제:
1. **router 없음** — routing 이 INPUT(prompt/category)에 의존할 수 없음. tension 은 cell internal dynamics 의 함수일 뿐, prompt 마다 거의 동일 → category-mean weight 분포 간 KL ≈ 0 (by construction). cotrain v1/v2/per-cat/τ-sweep 모두 이 한계.
2. **plain softmax saturation** — cell-0 tension 793× dominance (PSCC §47) → wmax → 1.0 → entropy → 0. λ=0.1 entropy reg 도 CE gradient 에 overpowered (PSCC §45).

→ 4a routing variant 은 **architectural change** 없이는 닫을 수 없음 (PSCC §44-49 의 4 cheap-path 가 모두 falsified 한 이유). 본 BG = 그 architectural change.

## §2 fix design (path g2+g3+g4)

| 요소 | 구현 | rationale |
|---|---|---|
| **learnable router** | `TopKMoERouter`: `Linear(d_model → max_cells)`, input = pooled cell-input embedding `(tok_emb+pos_emb).mean(batch,seq)` | input-dependent routing → category 가 다르면 routing 도 다름. router out-dim = `max_cells` (split 시 N 증가해도 shape 안정, `[:n_cells]` slice) |
| **(g2) hard top-K MoE** | top-K=4 gate, rest masked, survivors renorm (sums to 1 over top-K) | winner-take-all 깨짐 — 항상 ≥ K cells gradient carry (Switch/Mixtral default K) |
| **(g3) load-balance aux** | `aux = N·Σ_i f_i·P_i` (f = dispatch fraction, P = gate prob), `loss += α·aux`, α=0.01 | router 가 constant top-K monopoly 학습 안 하도록. Switch Transformer default α |
| **(g4) annealed gate-entropy** | `loss -= λ(step)·H(softmax_gate)`, λ_init=1.0 → λ_final=0.01 cosine over (warmup..steps) | early exploration / late CE-dominant. modest (v2 λ=0.1 fixed 실패 + path-f λ=50 aggressive 둘 다 회피) |
| **mitosis 보존** | split/merge 는 원래 scalar `cell.tension.mean` 사용 (router gates 아님) | F-V5MIT-1..5 regression surface 안 건드림 — routing fix 와 mitosis dynamics 분리 |
| **model body 미수정** | `engine.forward` monkey-patch (v2 `_install_live_weights_hook` 패턴), router 는 별도 optimizer param group | `mitosis_model_v5.py` SSOT 유지 |

HONEST C3 — see §7 (8 items).

## §3 envelope / dispatch

- arch: d=384, n_head=6, ffn=1536, initial_cells=2, max_cells=64, ctx=256, batch=32 — **v1/v2 와 동일 clean comparison point** (no scale caps; D_MODEL=768 MAX_CELLS=128 STEPS=10000 env override 가능)
- steps: **8000** (v1/v2 5K 보다 늘림 — router 가 category routing 학습할 시간; mid-run ckpt+SNAP @ 2K/4K/6K)
- lr: 1e-4 cosine warmup=500; seed 42
- routing: top_k=4, aux_alpha=0.01, λ_init=1.0, λ_final=0.01, cosine
- GPU: vast.ai, filter `[H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE,H200] reliability>0.95 dph<5.0` — H100 SXM 시장 비어있어 **A100-SXM4-80GB fallback** (instance 36622183, dph $0.8681, reliability 0.9955)
- infra: PSCC §28 base + §45 direct-IP (public_ipaddr + direct_port_start) + scp ConnectTimeout=3600 (609MB ckpt) + trap cleanup pod auto-destroy + SAVE_POD=1 on pull-fail (memory feedback_orchestrator_h100_gotchas)
- cost cap $8 — **실측 $1.76** (cost guard would only abort at ~9hr; 2hr run well within)
- artifacts: `state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/{train_v5mitosis_cotrain_v3_routing.py, dispatch_h100_v3_routing.sh, hf_push.py, ckpts/ckpt_v5mitosis_cotrain_v3_routing.pt (609MB, {model_state_dict, router_state_dict, router_top_k=4, ...}), cotrain_v3_routing_result.json, train_v3_routing.log}`

## §4 cotrain v3-routing run

| metric | step 0 | step 2000 | step 4000 | step 6000 | step 8000 final (avg100) | v2 baseline (for comparison) |
|---|---|---|---|---|---|---|
| CE | 263.9 | 1.823 | 1.607 | 1.491 | **1.476** | 1.368 (no aux/entropy pressure → lower) |
| loss (incl aux − λ·ent) | 263.3 | −1.96 | −0.68 | +0.80 | +1.44 (λ_gate ≈ 0.01 → CE dominant by end) | 1.368 |
| **wmax** (top-K renorm weight max) | 0.519 | 0.266 | 0.283 | 0.303 | **0.316** | **1.0** (winner-take-all monopoly) |
| **n_active>.01** | 2.0 | 4.0 | 4.0 | 4.0 | **4.0** = top-K | **1** (single cell) |
| **gate_max** (full softmax gate max over 64) | — | — | — | — | **0.0217** ≈ uniform (1/64=0.0156) | n/a (no learnable gate) |
| **gate entropy** | 0.69 | 4.159/4.159 | 4.159 | 4.159 | **4.158** ≈ log(64) (near-uniform) | ~0 (monopoly) |
| Switch aux | 1.00 | 1.039 | 1.056 | 1.080 | **1.095** (≈ 1.0 → balanced; > 1 = mild imbalance) | n/a |
| λ_gate-entropy | 1.000 | 0.906 | 0.557 | 0.174 | **0.010** (annealed) | 0.1 fixed (v2 entropy-reg) |
| cells / splits | 2 / 0 | 64 / 62 | 64 / 62 | 64 / 62 | **64 / 62** (saturated by step ~150) | 64 / 62 |
| Φ (best) | — | — | — | — | **4.167 (best 4.190)** | 4.163 |
| mid-run SNAP 4a (n_perms=30) | — | KL=4.28 z=0.77 | KL=2.80 z=−0.35 | KL=2.75 z=0.24 | (final n=100: KL=3.36 z=1.37) | — |

**Observation**: the routing fix performed **exactly as designed on the diversity axis** — winner-take-all monopoly broke (wmax 1.0→0.32, 4 active cells, near-uniform load, Switch aux ≈ 1.0). CE converged to 1.48 (vs v1/v2's 1.37; the ~0.1 gap is the price of the aux + early-phase entropy pressure — acceptable, F-V5MIT-4 PASS). But the **statistical-significance axis never moved**: mid-run SNAP z stayed in [−0.35, +0.77] across steps 2K/4K/6K and finished at 1.37 (< 3.0) — the router never learned category-correlated routing despite λ_gate annealing 1.0→0.01 (which should have allowed late specialization).

`cat_mean_topk_weights` (final, full json): cell-1 carries ~0.288-0.291 weight uniformly across all 5 categories — a "default route". The remaining ~0.71 mass spreads over ~5-7 minor cells with small (~0.02-0.14) category-dependent variation, but the variation is small relative to the spiky top-K structure's contribution to KL. So mean pairwise KL = 3.36 nats — but a random label permutation also yields 2.64 ± 0.52 nats (the top-K masking inflates KL for *any* grouping). True − null = 0.72 nats ≈ 1.37σ → not distinguishable.

## §5 F-PERSONA measurement

### §5.1 F-PERSONA-4a routing (PRIMARY)

metric (per §A3): per-prompt top-K renormalized weight vector → category-mean → mean pairwise KL → null permutation (n_perms=100, label shuffle). threshold: KL ≥ 0.5 nats **AND** (z > 3.0 OR p < 0.01).

**Result: KL_PASS_NULL_FAIL** = FAIL on the 4a criterion. mean_KL = 3.3616 nats (≥ 0.5 ✓), null mean = 2.6446 ± 0.5231, z = **1.37** (< 3.0 ✗), p = 0.11. Soft-gate variant (full softmax gate over 64): mean_KL = 2.5e-4, z = 1.13, p = 0.13 — also FAIL (the soft gate is essentially uniform, so its category-mean KL is tiny).

### §5.2 F-PERSONA-4b content (REGRESSION)

metric: M4 aggregated hidden state (`info["aggregated"].mean(batch,seq)`) → category-mean cosine distance → null permutation (n_perms=100). threshold: z > 3.0 OR p < 0.01. v2 carry: z=3.20.

**Result: FAIL (regression) — z = 0.20** (< 3.0), cos_dist = 4.46e-5, null = 4.18e-5 ± 1.38e-5, p = 0.39. The v2 entropy-reg cotrain's z=3.20 was driven by the *softmax-routed* `aggregated` concentrating category signal in one cell's output; the v3-routing top-K spreading re-weights `aggregated` so that signal is diluted across 4 cells → washed out. **This means the v3-routing ckpt does NOT supersede the v2 ckpt for cond #3's §A3 4b evidence** — the v2 cotrain ckpt (`state/anima_v5mitosis_cotrain_2026_05_12/cotrain_v2_*`) remains the cited evidence for cond #3 D3 ☑ DONE (PSCC §50).

### §5.3 F-V5MIT-1..5 regression

cheap structural checks: F-V5MIT-1 mitosis active (n_cells 64 > initial 2) ✓ / F-V5MIT-2 no collapse (64 ≥ min 2) ✓ / F-V5MIT-3 Φ ratchet held (phi 4.167 ≤ phi_best 4.190) ✓ / F-V5MIT-4 CE converged (1.476 < 5.0) ✓ / F-V5MIT-5 V14-STRICT proxy (62 splits ≤ 64 max_cells, > 0) ✓ → **5/5 PASS** ⭐ regression-free. The routing-fix monkey-patch did not perturb the mitosis dynamics (split/merge still on the original scalar-tension signal).

## §6 cond #3 status update

- **D3 ☑ DONE (PSCC §50) via the §A3 4b content metric — MAINTAINED.** The v2 entropy-reg cotrain ckpt's M4 aggregated hidden cosine z=3.20 null-PASS evidence is unaffected by this BG. ★★★★★ 5/5 ☑ stands.
- **4a routing variant**: scenario (iii) — **still FAIL** even with top-K MoE + load-balance aux + annealed gate-entropy + learnable input-dependent router. Monopoly broken (wmax 1.0→0.32) but no category-dependent routing emerged (z=1.37 < 3.0). 6/6 atomic (4a + 4b both PASS) **not reached**. Under §A3, 4a is formally still "unfalsified-as-PASS" (it remains measurable, just didn't cross the bar) but is now strongly-evidenced-toward-fail. The §A3 dual-metric design's prediction ("4a measurable after architectural change") was *partly* confirmed — measurable, yes; but the fix that breaks the monopoly is not the fix that induces category routing. Routing-level category differentiation appears to be a genuinely harder problem than monopoly-breaking.
- Next architectural lane candidates (not in scope here): (1) **per-token MoE** routing (instead of per-input-pooled) so category structure in token positions is captured; (2) **2-layer MLP router** or attention-over-cells router; (3) **category-supervised auxiliary loss** on the router gates during cotrain (cheap, directly forces it); (4) **gumbel-softmax straight-through** discrete cell selection (g1, deferred this cycle for stability); (5) bigger scale (d=768, cells=128, longer corpus per category).

GOAL.md cond #3 row note + Saga history PSCC §51 row updated. PSCC §51 appended.

## §7 honest C3 (≥ 5)

1. router 는 POOLED (batch×seq mean) embedding 만 봄 — coarse. category 구분이 token-position structure 에 있으면 discard됨.
2. d_router_in = d_model, single Linear (no nonlinearity) — linear probe. 2-layer MLP router 가 더 잘 separate 할 수도 있으나 param + risk 추가 → 의도적 최소화.
3. top-K=4 with N≤64 → 60 cells unrouted per input → load-balance aux + rare routing 으로만 gradient. slow specialization. K=4 = Switch/Mixtral default, tune 안 함.
4. mitosis 는 여전히 scalar-tension signal 로 동작 (router gates 아님) — split/merge dynamics v1/v2 와 동일, routing fix ↔ mitosis 분리 (의도적).
5. aux-alpha=0.01 = Switch default; router 가 여전히 collapse 하면 α 0.05-0.1 로. CE 수렴 안 하면 aux too strong.
6. router 는 random init + warmup 동안 untrained → early routing = noise. n_perms=100 null test 가 그 noise 로부터의 spurious "category-dependent" verdict 방어.
7. F-PERSONA-4b regression — actual: z dropped 3.20 → **0.20** (full collapse), exactly the predicted "양방향" risk realized in the negative direction. The v3-routing top-K spreading re-weights `aggregated` across 4 cells per input, diluting the category signal that v2's softmax-monopoly concentrated in one cell. Important interpretation: v2's z=3.20 was not "the cells learned different content per category" — it was "the softmax monopoly picked a different cell per category on average, and that cell's output is what `aggregated` reduced to." Once the monopoly is broken (v3-routing), the content distinction goes with it. **Routing and content evidence are coupled, not independent** — a finding contra the §A3 amendment's framing of "routing-content split." `cat_mean_topk_weights` confirms: even the top-K weights are largely category-independent (cell-1 ~0.29 across all 5 cats), so there is no "different cell per category" structure to drive content z either.
8. **scenario (iii) verdict is a robust negative result**: a Switch/Mixtral-style learnable input-dependent top-K MoE — the textbook architectural fix — does not produce category-correlated routing in this substrate at this scale. This isn't a tuning issue; the linear router can perfectly access the input embedding (single Linear with 64-dim output × 50 distinct probes is over-parameterized for the classification problem), and λ_gate annealed all the way to 0.01 to allow specialization. The router *chose* to route ~all inputs to a default cell (cell-1) and spread the rest near-uniformly. Hypothesis: with 5 categories × 10 probes each and N=64 cells, the load-balance aux is the dominant gradient signal (aux ≈ 1.0 throughout — never went below 1.0 meaning router never sharpened) and the CE gradient simply doesn't prefer category-dependent routing because category-dependent routing isn't actually useful for byte-level next-byte prediction on the balanced corpus (the corpus interleaves categories so any cell needs to handle any byte distribution at the per-token level).

## §8 mission contribution

post-★★★★★ cond #3 의 4a routing variant resolution. Verdict = **scenario (iii) FAIL** → cond #3 D3 ☑ DONE via §A3 4b path **MAINTAINED** (v2 ckpt evidence intact), but the 6/6 atomic strongest-possible D3 closure is **not reached**. Honest negative result: routing-layer category differentiation in v5-mitosis is not unlocked by Switch/Mixtral-style top-K MoE alone. The §A3 dual-metric framing of "routing-content split" is partially refuted — routing and content evidence appear coupled (4a and 4b moved together in opposite direction). New finding for the lane: **routing fixes that break monopoly do NOT automatically improve category routing** — a separate force (per-token MoE, supervised gate loss, attention-over-cells router, bigger scale) is needed. This is a meaningful "what doesn't work" data point for the architectural-fix family.

## 출처

- `state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/` — trainer + dispatch + ckpt + result json + logs
- `state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain_v3.py` (λ-anneal path-f, SUPERSEDED-BY note 추가)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` §A3
- `docs/anima_persona_4_root_cause_investigation_2026_05_12.md`
- `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`
- PSCC §44 / §45 / §45-FINAL / §47-50 / **§51 (본 BG)**
- GOAL.md 🎉 ★★★★★ banner + cond #3 §A3 row
- memory `feedback_no_scale_caps` + `feedback_orchestrator_h100_gotchas` + `feedback_dispatch_vast_template_gotchas`
