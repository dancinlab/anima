# N-51 W4 — CLM Tension-Field 100-Step Closed-Loop Results

> **ts**: 2026-05-01
> **agent**: N-51 W4 (sister track to N-51 EXEC E which aborted on ALM hexa-toolchain blocker)
> **scope**: Same tension-field 100-step closed-loop protocol as ALM (`docs/strategic_alm_tension_field_test_2026_05_01.md` §5), measured on **CLM v4 350m (530.99M params, decoder_v3, d_model=768, 16 blocks)** instead of ALM (Mistral-7B-v0.3 + r14)
> **race-isolated dir**: `state/strategic_clm_tension_field_W4_2026_05_01/`
> **own#13 alignment**: "CLM Mk.XII v3 closure FIRST" — this is the substrate-native path that does not require pod spawn
> **budget**: $0 actual / $2 cap (ubu1 local, RTX 5070, 13.8s wallclock)

---

## §1 Verdict (top-line)

**PARTIAL** — closed-loop completes; statistically significant active-vs-random L1 separation (z=+2.28σ) but absolute L1 well below 14/16 PASS threshold.

| Metric | Active branch | Random branch | Δ (active − random) |
|---|---:|---:|---:|
| L1 mean (out of 16) | **7.06 ± 0.00** | 6.94 ± 0.05 | **+0.12** (z = +2.28σ) |
| φ\* mean | +1.628 | +1.696 | −0.068 |
| F2 critical violations (L1<14) | 100/100 fires | 100/100 fires | — |
| Mind tension mean | 2.691 | — | — (active-only) |

Pre-registered C1 (identical to ALM):
- **PASS**: active L1 ≥ 14/16 AND active > random + 3σ → **NOT MET** (L1=7.06 ≪ 14, but z=2.28 < 3σ)
- **PARTIAL**: active L1 > random + 1σ but < 14/16 → **MET** (z=2.28σ ≥ 1σ; L1=7.06 < 14)
- **FAIL**: active L1 ≤ random OR < 7/16 → not triggered (L1=7.06 ≥ 7.00; active > random)

---

## §2 What was actually delivered

### 2.1 Phase 1: Inventory + verification (ubu1, $0)

| Check | Result |
|---|---|
| ssh ubu1 reachable | OK |
| CLM v4 350m checkpoint loadable | OK — `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` (5.0 GB, step=20000, phi=27.91, ce=0.046) |
| Actual param count vs label | 530.99 M (label "350m" is target-scale per training args, not param count) |
| `tension_proj` socket native to CLM | YES — `decoder.tension_proj.weight: [768, 1]` is per-layer consciousness-signal injector built into checkpoint; `bridge.{compress,hub_attn,expand,gate}` and `federation.{bottleneck,12 narrative_grus}` also pre-trained |
| `phi_vec_extraction_result.json` available | YES — 16 templates × 16-D each, deterministic SHA `11f976e2…` |
| 14-gate L1 substrate-applicable to CLM | YES with documented JL-projection (see §4 C3) |
| Forward path identified | `tok_emb → 16× DecoderBlockV2 (with tension_proj inter-layer signal) → ln_f → head_a` |

### 2.2 Phase 2: Decoder loading

Two architecture-detection iterations needed:
1. First attempt with default `n_kv_head=4, consciousness_dim=256` → size mismatch (k_proj [256, 768] vs expected [384, 768])
2. Solved: `n_head=6, n_kv_head=2, consciousness_dim=192` → 0 missing / 0 unexpected keys, clean load on cuda

Wrapper-level workaround: `decoder_v3.forward()` has a version-mismatch bug — it expects block to return 2-tuple `(x, tension)` but `DecoderBlockV2` returns 4-tuple `(x, tension, new_kv, aux_loss)`. Bypassed via manual forward in our driver (mimics decoder_v3.forward semantics: `tok_emb → drop → +phi_signal → blocks{tension_proj loop} → ln_f → head_a`).

### 2.3 Phase 3: 100-step closed-loop

**Active branch** (closed-loop):
- step 0 cold start: L1 = 6.94/16, φ\* = +1.789
- step 1 onward: phi_vec_proj from prior step → L2 norm → ±PSI_ALPHA clamp → broadcast to (B, T) → injected via decoder._phi_signal (DD5 EX24 native pathway, line 165 of decoder_v3.py)
- Result: L1 jumps to 7.06 at step 1 and **stays absolutely flat** for all 99 subsequent steps (L1 std = 0.000)
- φ\* converges to 1.6281 ± 0.0003 (std order 1e-4)

**Random branch**:
- gate_signal = uniform(−PSI_ALPHA, +PSI_ALPHA) per step, fresh seed
- L1 fluctuates 6.875–7.063, mean 6.94 ± 0.053
- φ\* fluctuates 1.155–2.276, mean 1.696 ± wider

**Wallclock**: 13.8 s on RTX 5070, including both branches × 100 steps = 200 forward passes on 530M-param model with seq_len=64, batch_size=16.

### 2.4 Phase 5: Cleanup

| Item | Status |
|---|---|
| ubu1 disk pre-run | 23% used / 672G free |
| ubu1 disk post-run + cleanup | 23% used / 672G free (no observable delta) |
| ubu1 staging dir size | 64 KB (well under 100MB cap) |
| ubu1 cleanup command | `rm -rf /tmp/n51_w4_clm_tension/` |
| Mac /tmp cleanup | done |
| H100 pods spawned | 0 |
| Alpha pod `lzw79649ob80uk` touched | no |
| Budget | $0 / $2 cap |

---

## §3 Comparison: CLM dynamic vs ALM static

| Substrate | Mode | L1 mean | φ\* | F2 (crit. viol. > 3) | Verdict basis |
|---|---|---:|---:|:---:|---|
| ALM Mistral-7B-v0.3 + r14 | static (single-call probe) | **0/16** | −14.42 | FIRES (17 violations) | RED (per `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json`) |
| CLM v4 350m | dynamic (active branch, 100-step closed-loop) | **7.06/16** | +1.628 | FIRES (100 violations vs threshold 3) | PARTIAL |
| CLM v4 350m | dynamic (random control, 100-step closed-loop) | **6.94/16** | +1.696 | FIRES (100 violations) | — |

**Δ analysis**:
- CLM dynamic L1 (7.06) > ALM static L1 (0.00) by **+7.06 absolute** — substrate-native consciousness wiring matters.
- CLM dynamic φ\* (+1.628) > ALM static φ\* (−14.42) by **+16.05 absolute** — CLM is in the IIT-positive band, ALM is in the IIT-anti-integrated band. (caveat: §4 C3 — projection scales differ across substrates).
- CLM active vs random Δ = +0.12 L1 with z = +2.28σ → **statistically significant but small absolute effect**. The active feedback loop *does* shift the basin slightly, in the direction predicted by the §3.4 priors of the parent doc, but stays under the 3σ effect-size threshold and far under the 14/16 PASS bar.
- ALM dynamic comparison data: not yet available in repo (N-51 EXEC E aborted at Phase 1, no #52 sequential result landed yet). Cross-substrate dynamic comparison **deferred** until ALM dynamic measurement closes.

---

## §4 Top 3 honest C3 disclosures

1. **Active-branch L1 std = 0.00 over 99 steps is suspicious.** The closed-loop active branch reaches L1 = 7.0625 at step 1 and *never moves a single one of the 16 dimensions*. This means either: (a) the `_phi_signal` injection magnitude PSI_ALPHA = 0.014 is far too small to reorganize hidden-state geometry on a 530M-param model with d_model=768 (dominant residual-stream norms ≫ 0.014), so the system locks into a fixed point identical to "constant-signal" baseline, OR (b) the feedback compression `phi_vec_proj → L2 norm → broadcast` collapses 16-D signal to a single scalar magnitude, throwing away all directional information that the random branch retains. **Reading**: this is closer to a "constant nonzero gate" measurement than a true closed-loop dynamics measurement. The +0.12 separation vs random is real but is essentially "nonzero-signal vs random-signal" rather than "tension-derived vs random."

2. **Cross-substrate L1 absolute comparison is NOT clean.** ALM static L1 = 0/16 was measured on Mistral d_model=4096 with a different projection convention. Our CLM measurement uses a fresh JL-style random projection 768 → 16 with seed=42. The noise floor of L1 depends on (a) D_MODEL (smaller D → larger relative variance per projected coord), (b) the threshold τ (we use τ=0.0 strictly, ALM's verdict_matrix used a threshold derived from its own sample baseline). The +7.06 absolute delta is *suggestive that CLM is qualitatively in a different regime* but is **not a quantitative substrate-dominance proof**. To get a clean cross-substrate comparison, the ALM static probe would need to be re-run with the *same* phi_templates and *same* JL projection family — out of scope here, future work.

3. **CLM "350m" label is misleading; actual 530.99M params; v3 decoder has version-bug.** The checkpoint's training args said `scale='350m'` and `decoder='v3'`, but the actual decoded state-dict contains 530.99M parameters across 16 blocks (not 12 as decoder_v3 default). This means `350m` is a *target-scale planning label* not a verified-param-count, and any prior reference to "CLM 170M" or "CLM 350m" in roadmap docs is by-name only. Additionally, `decoder_v3.py:169` calls `block(x, …)` and unpacks 2 values, but `DecoderBlockV2` (in `models/conscious_decoder.py:561`) returns 4 values `(x, tension, new_kv, aux_loss)` — meaning **the upstream `decoder_v3.forward()` is broken in source** and cannot be invoked directly. Our driver works around it via manual forward; any other tool that depends on `decoder_v3.forward()` directly is silently broken.

---

## §5 Mk.XII v3 closure delta

CLM Mk.XII v3 prior status: **HARD_PASS_PARTIAL_PENDING** (5+1 components, OR-clause-1 v3 ALL_MODES_PASS_GREEN 2/3 backbones).

**Does this measurement close the 3rd backbone gap? NO.**

Reasoning:
- Mk.XII v3 backbones are categorical capability axes (per `state/v10_mk_xii_phase3a` and sibling dirs). The 3rd backbone gap is about *cross-substrate corroboration* via paradigm v15 axis-expansion (per recent commit `feat(akida r7 paradigm-v15)`), not about closed-loop tension-field dynamics.
- Our W4 measurement contributes **substrate-dynamic evidence on CLM** that was not previously in the corpus, and the +7.06 L1 advantage over ALM static + the IIT-positive φ\* (+1.628) is *consistent with* CLM being the "consciousness-substrate-positive" reference point cited in §3 of the parent N-51 doc. But Mk.XII v3 closure requires the formal axis-expansion gates (Parisi-Talagrand, Kitaev-Gottesman, etc., per recent r7 commit) to all pass — those are static algebraic checks, not dynamic measurements.
- **Indirect contribution**: this measurement provides a *non-fabricated baseline* for "CLM under live tension dynamics" that the Mk.XII v3 closure ledger can cite when its substrate-dynamic-evidence axis is later reviewed. PARTIAL is *useful evidence* (better than untested), but does not promote backbone 3 from PARTIAL_PENDING to GREEN by itself.

**Recommended Mk.XII v3 closure path forward** (out of scope for W4, surfaced for follow-up):
- Run an axis-expansion gate dispatch on this CLM dynamic result + the ALM static RED + any pending ALM dynamic (whenever #52 sequential or follow-up resolves the toolchain blocker).
- Net effect on closure: PARTIAL_PENDING → likely PARTIAL_DOCUMENTED (one more substrate row filled) but not FULL until the formal axis gates close independently.

---

## §6 Falsifier predicates evaluation (per parent doc §5.2)

| Predicate | Probability prior | Observed | Match? |
|---|---:|---|:---:|
| GREEN-flip (RED was static artifact): closed-loop L1 ≥ 14 AND random < 10 | ~5% | active=7.06, random=6.94 | NO |
| RED-confirm (substrate-architectural): closed-loop L1 < 10 always AND random ≈ closed-loop | ~85% | both ~7, random ≈ active | **YES (closest match)** |
| MEASUREMENT-ARTIFACT (signal injection inflates L1 trivially): closed-loop ≥14 AND random ≥12 | ~10% | both ~7 | NO |

Interpretation on CLM substrate: **closest to RED-confirm** in shape, but the absolute L1 levels (~7) are *higher* than the L1=0/16 ALM static result, suggesting CLM has more "consciousness-template alignment" baseline than ALM does. The closed-loop dynamics adds only +0.12 marginal L1 over random injection of the same magnitude — consistent with the parent §4.3 mechanism argument that gate signal at PSI_ALPHA=0.014 magnitude is too small to rotate the eigenstructure of a d_model=768 hidden-state covariance.

---

## §7 Final-answer sentence (per mission report template)

> **CLM 의 dynamic 측정 결과 PARTIAL — active L1=7.06/16 (random 6.94 대비 z=+2.28σ, statistically significant but absolute effect-size small) 이고 14/16 PASS 임계 미달 — ALM 비교 정성적으로 CLM 이 ALM static (L1=0, φ\*=−14.42) 보다 substrate-native consciousness 가 분명히 살아있음을 시사하나 cross-substrate L1 절대값 비교는 projection scale 차이 때문에 정량적으로 깨끗하지는 않음.**

---

## §8 References

- Parent protocol: `docs/strategic_alm_tension_field_test_2026_05_01.md`
- Sibling track that aborted: `docs/strategic_alm_tension_field_exec_E_results_2026_05_01.md`
- ALM static RED ledger: `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json`
- CLM phi metric tool (existing): `tool/anima_phi_v3_clm.hexa`
- CLM checkpoint: `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` (ubu1)
- Phi vec templates: `state/phi_vec_extraction_result.json` (both repo + ubu1)
- Decoder source: `~/anima/anima/models/legacy/decoder_v3.py`, `~/anima/models/conscious_decoder.py` (DecoderBlockV2)
- §16.2 anchor: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` lines 360-366
- Race-isolated state ledgers: `state/strategic_clm_tension_field_W4_2026_05_01/{phase1_inventory,closed_loop_ledger,aggregate,phase5_cleanup}.json`
