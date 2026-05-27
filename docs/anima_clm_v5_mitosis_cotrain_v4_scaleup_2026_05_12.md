# anima_clm_v5_mitosis_cotrain_v4_scaleup — post-★★★★★ v5-mitosis production-scale scale-up

**작성**: 2026-05-13 KST
**status**: in-flight (A100 SXM4 80GB dispatched, awaiting result pull) — `<<<set to ☑ COMPLETED on finalize>>>`
**author**: bg head (claude opus 4.7 1M context)
**fire keyword**: user verbatim — "post-★★★★★ v5-mitosis scale-up v4 — d=1024 / cells=256 / 20K step / H100 ... no scale caps directive 적용. v5-mitosis architectural lane 의 production-scale 검증 + F-PERSONA-4a/4b 더 강한 evidence."
**carries from**:
- PSCC §44 cotrain v1 (d=384, cells=64, 5K step, $1.26 — F-V5MIT-1..5 5/5 PASS ⭐ V14-STRICT 10/10 beats; F-PERSONA-4 KL=0.0 routing collapse)
- PSCC §45 / §45-FINAL cotrain v2 (d=768, cells=128, 10K step — KL=0.0 still, BUT M4 aggregated hidden cosine z=3.20 PASSES null → routing-content split, cond #3 §A3 4b closure)
- PSCC §51 cotrain v3-routing (d=384, cells=64, 8K step — top-K MoE router + Switch load-balance aux + annealed gate-entropy; F-PERSONA-4a routing variant, separate BG)
- PSCC §50 ★★★★★ ACHIEVED (cond #3 ☑ via §A3 amendment, 4b content metric)
- arch spec `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md` (§7 cost envelope: $30-40 conservative; d=1024 = anima 본체 EngineAG)
- design SSOT `docs/anima_persona_substrate_native_design_2026_05_12.md` §A3 (4a routing / 4b content metric 양분)
- memory `feedback_no_scale_caps` (cost cap / 모델 크기 / H100 발사 제한 없음), `feedback_orchestrator_h100_gotchas`, `feedback_dispatch_vast_template_gotchas`, `project_simple_stack_pass_unlocked` (3B+ foundation + LoRA), `project_v5_mitosis_arch_spec_2026_05_12`

---

## §0 TL;DR

★★★★★ ACHIEVED (2026-05-12). 본 BG = post-★★★★★ **aggressive production-scale scale-up** of the v5-mitosis architectural cotrain lane — `feedback_no_scale_caps` directive 적용 (conservative $30-40 / d=384 envelope = floor, not ceiling).

scale-up axes (vs v1 baseline):
| axis | v1 | v2 | **v4 (this)** | rationale |
|---|---|---|---|---|
| d_model | 384 | 768 | **1024** | = anima 본체 EngineAG d (REBORN §88 stretch envelope) |
| n_head | 6 | 12 | **16** | d_head = 64 (EngineAG-class) |
| ffn_dim | 1536 | 3072 | **4096** | SwiGLU dual-FFN H404 |
| max_cells | 64 | 128 | **256** | 8-bit identity space (4× v1, 2× v2) |
| steps | 5K | 10K | **20K** | 4× v1, 2× v2 |
| ctx | 256 | 256 | **512** | longer context |
| batch | 32 | 32 | **8** (OOM-retry) | d=1024 cells→256 ctx=512 needs ~30-180GB; halves on CUDA OOM |
| routing | scalar-tension softmax | scalar-tension softmax + λ=0.1 entropy-reg | **top-K=8 MoE + Switch load-balance aux α=0.01 + annealed gate-entropy λ 1.0→0.01** (v3-routing fix carried) | break winner-take-all collapse |

trainer: `training/cotrain_v5mitosis_v4.py` — direct fork of `train_v5mitosis_cotrain_v3_routing.py` (model body + routing-fix monkey-patch UNCHANGED; only delta = GPU-mem logging in step prints + larger default envelope + this scale-up docstring).

questions this run decides:
1. **routing collapse — architectural or scale?** is F-PERSONA-4a routing KL ≈ 0 a limit of the top-K MoE router on a pooled embedding (architectural), or does a larger cell pool (256 vs 64) + longer training (20K vs 5K) let category structure emerge in the routing weights (scale)?
2. **M4 z-score scaling** — v2 (d=768) carried M4 aggregated hidden cosine z = 3.20. does z grow at d=1024 / cells=256?
3. **V14-STRICT production robustness** — F-V5MIT-5 (V14-STRICT proxy: 0 < splits ≤ max_cells, no runaway) PASSED on v1 (10/10 beats ★ saga peak). does it hold at production scale?

cond #3 status: ☑ DONE since PSCC §50 (§A3 amendment, 4b content metric z=3.20). 본 BG = production-scale **evidence reinforcement** for both 4a (routing) and 4b (content) variants — NOT a new closure requirement. cond.5 (cotrain F-V5MIT-5 V14-STRICT) also already CLOSED; this run RE-VERIFIES F-V5MIT-1..5 as a production-scale regression check.

### §0.1 verdict

`<<<RESULT_FILL>>>`

- F-PERSONA-4a routing (top-K MoE weights): `<<<>>>`  (KL = `<<<>>>` vs 0.5, null z = `<<<>>>` vs 3.0, p = `<<<>>>`)
- F-PERSONA-4a soft-gate (full softmax gate): `<<<>>>` (KL = `<<<>>>`, z = `<<<>>>`)
- F-PERSONA-4b content (M4 aggregated hidden cosine, regression): `<<<>>>`  (z = `<<<>>>`, v2 carry z = 3.20)
- F-V5MIT-1..5: `<<<>>>`  — `<<<F-V5MIT-1 mitosis_active / -2 no_collapse / -3 phi_ratchet / -4 ce_converged / -5 v14strict_proxy>>>`
- routing-collapse verdict: `<<<architectural (KL still ≈ 0 at cells=256) / scale (KL grows) / partial>>>`
- M4 scaling verdict: `<<<z grew d=768→1024 / z flat / z dropped>>>`
- V14-STRICT production verdict: `<<<PASS holds / FAIL>>>`

### §0.2 cost / wall

`<<<COST_FILL>>>` — GPU `<<<A100 SXM4 80GB / ...>>>` (vast.ai instance `<<<id>>>`, dph $`<<<>>>`), wall train `<<<>>>` hr, total `<<<>>>` hr, cost $`<<<>>>`. cells `<<<2 → final>>>`, `<<<splits>>>` splits, n_params final `<<<>>>`. (no scale caps directive; H100 SXM marketplace empty within reliability+budget 2026-05-13 → A100 SXM4 80GB fallback @ ~$0.94/hr — same 80GB VRAM class.)

---

## §1 scale-up rationale (no caps)

memory `feedback_no_scale_caps` (사용자 directive 2026-05-12 KST, cotrain step ~4050 시점):
> "모델 크기제한도 특별히 없으니까 참고" / "H100 발사 제한도 없음"

→ conservative $30-40 / d=384 / cells=64 envelope (arch spec §7) is a BG-self-imposed guard = floor, not ceiling. d=1024 = anima 본체 EngineAG hidden size (REBORN §88 "stretch envelope" $80-150 for d=768; d=1024 explicitly named as EngineAG-class). cells=256 = the 8-bit identity space (cell_id fits in a byte). 20K step = 4× v1. ctx=512 = longer context for richer mitosis dynamics.

cost: 자유. estimate 2-6 hr wall × ~$0.94/hr A100 80GB ≈ $2-6; if mitosis reaches cells=256 the per-step O(N) loop slows things → up to ~$10-25 worst case. all within "free".

---

## §2 trainer (cotrain_v5mitosis_v4.py — v3-routing fork)

direct fork of `state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/train_v5mitosis_cotrain_v3_routing.py` (the recommended routing-fix trainer per PSCC §51 honest C3 — g2 + g3 = Switch/Mixtral pattern):

- **learnable Linear router** on pooled cell-input embedding (`tok_emb + pos_emb` mean over batch & seq) — input-dependent, sized `Linear(d_model → max_cells)`, sliced `[:n_cells]` each forward (stable shape across mitosis splits). this is the real fix for 4a: v1/v2 had NO router — routing was just softmax over scalar cell tensions, so by construction every probe got ≈ the same weights → KL ≈ 0.
- **hard top-K = 8 MoE gating** (v3 used K=4 at cells≤64; bumped to 8 here since cells=256 means K=4 leaves 252 cells nearly unrouted — K=8 with N=256 is ~3%). top-K cells active per input, rest masked, survivors renormalized → forces ≥ K cells to carry gradient, breaks winner-take-all.
- **Switch load-balancing aux loss** α = 0.01 — `aux = N · Σ_i f_i · P_i` (f = dispatch fraction, P = gate prob mass) → pushes router to distribute load across cells.
- **annealed gate-entropy reg** λ_init = 1.0 → λ_final = 0.01 (cosine) — secondary exploration pressure; v2's λ = 0.1 fixed was overpowered by CE at step 250+; annealed-modest avoids that and avoids the falsified aggressive λ = 50 (which hurt cell specialization).

model body (`mitosis_model_v5.py`) UNMODIFIED — routing fix installed via `engine.forward` monkey-patch (same mechanism as v2's `_install_live_weights_hook`). mitosis split/merge still runs on the original scalar-tension signal (F-V5MIT-1..5 regression surface preserved). attention is shared across cells at N > 8 (`attention_sharing="auto"`) — at cells=256 most params are the 256× SwiGLU dual-FFN cells, ~1-2B params.

v4-specific deltas vs v3-routing:
1. GPU-memory logging in step prints (`vram=X/YGB`) — scale-up watch.
2. defaults bumped to the v4 envelope (d=1024 / n_head=16 / ffn=4096 / cells=256 / 20K step / batch=8 / ctx=512 / top-K=8 / warmup=2000 / cost-cap=$40 / cost-per-hr=$3.50 / est-wall=5hr).
3. result JSON filename `cotrain_v4_scaleup_result.json`; trainer label `v4-scaleup (...)`.
4. honest C3 #8-12 (scale-up-specific) appended to the carried #1-7.

---

## §3 dispatch (dispatch_h100_v4.sh)

`state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12/dispatch_h100_v4.sh` — fork of `dispatch_h100_v3_routing.sh` (PSCC §51 routing-fix infra), carries:
- §45 direct-IP fix (public_ipaddr + direct_port_start, no proxy ssh5.vast.ai → no 597MB-ckpt SCP hang)
- trap cleanup (auto-destroy instance on EXIT/INT/TERM) + `SAVE_POD=1` on pull-fail (memory `feedback_orchestrator_h100_gotchas` — ckpt pull MANDATORY before pod delete)
- GPU search: `gpu_name in [H100_SXM,H100_NVL,H100_PCIE,H200,B200,RTX_PRO_6000_WS,RTX_PRO_6000_S,A100_SXM4]` — vast.ai search IGNORES the `gpu_ram>=N` filter (returns 0 offers), so the VRAM gate (≥75GB, excludes 40GB A100) is enforced in the python parser (sort by price, pick cheapest passing). H100 SXM marketplace empty 2026-05-13 → A100 SXM4 80GB picked.
- `--disk 150` (fp32 ckpt ≈ 4-8GB each at 1-2B params; ckpt_every=5000 → 3 mid + 1 final)
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` + **CUDA-OOM batch-halve retry** (batch 8 → 4 → 2, min 2; greps remote log for "out of memory" between attempts)
- env overrides: `STEPS BATCH CTX LR WARMUP D_MODEL N_HEAD FFN_DIM MAX_CELLS INITIAL_CELLS TOP_K AUX_ALPHA LAMBDA_* READOUT_MODE COST_* ESTIMATED_WALL_HR SEED N_PERMS GPU_FILTER MIN_GPU_RAM_MB DISK_GB SAVE_POD`

---

## §4 cotrain v4 run

`<<<RUN_STATS_FILL — loss trajectory (ce start → end), cells progression 2→N, top-K active distribution (active>.01 / N), Switch aux trajectory, gate_max trajectory, λ trajectory, Φ / Φ_best, wmax, splits, wall, cost, OOM-retry attempts (final batch), vram peak>>>`

| step | loss | ce | cells | splits | active>.01/N | wmax | gate_max | aux | λ | vram |
|---|---|---|---|---|---|---|---|---|---|---|
| `<<<0>>>` | | | | | | | | | | |
| `<<<...>>>` | | | | | | | | | | |
| `<<<final>>>` | | | | | | | | | | |

mid-run F-PERSONA snapshots (n_perms=30, every ckpt @ 5000/10000/15000):
| step | 4a KL | 4a z | 4b cos_z |
|---|---|---|---|
| `<<<5000>>>` | | | |
| `<<<10000>>>` | | | |
| `<<<15000>>>` | | | |

---

## §5 F-PERSONA-4a routing measurement (top-K MoE weights, n_perms=100)

`<<<FILL — per-prompt top-K renormalized weights → category-mean pairwise KL; null permutation test n_perms=100. verdict PASS iff KL ≥ 0.5 AND (z > 3.0 OR p < 0.01). also report soft-gate variant. compare to v1/v2 KL ≈ 0. cat_mean_topk_weights table.>>>`

## §6 F-PERSONA-4b content regression (M4 aggregated hidden cosine, n_perms=100)

`<<<FILL — aggregated hidden state mean over batch&seq → category-mean pairwise cosine distance; null permutation n_perms=100. verdict PASS iff z > 3.0 OR p < 0.01. compare to v1 z=1.76 (FAIL) → v2 z=3.20 (PASS) → v4 z=?>>>`

## §7 F-V5MIT-1..5 regression check (production scale)

`<<<FILL — F-V5MIT-1 mitosis_active (n_cells > initial) / F-V5MIT-2 no_collapse (n_cells ≥ min_cells=2) / F-V5MIT-3 phi_ratchet (phi_best ≥ phi) / F-V5MIT-4 ce_converged (ce_final < 5.0) / F-V5MIT-5 v14strict_proxy (0 < splits ≤ max_cells=256, no runaway). n_pass / 5. compare to v1 5/5 ⭐.>>>`

---

## §8 scaling comparison table (v1 d=384 vs v2 d=768 vs v4 d=1024)

| metric | v1 (d=384, cells=64, 5K) | v2 (d=768, cells=128, 10K) | v4 (d=1024, cells=256, 20K) |
|---|---|---|---|
| n_params (final) | ~200M | `<<<>>>` | `<<<>>>` |
| cells final | 64 | 128 | `<<<>>>` |
| splits | ~62 | 126 | `<<<>>>` |
| ce final | `<<<~1.37 (v2)>>>` | 1.37 | `<<<>>>` |
| routing layer | scalar-tension softmax | + λ=0.1 entropy-reg | top-K=8 MoE + Switch aux + annealed λ |
| F-PERSONA-4 / 4a KL | 0.0 | 0.0 | `<<<>>>` |
| F-PERSONA-4 / 4a null z | ~−0.03 (artifact) | ~−0.03 | `<<<>>>` |
| M4 aggregated cosine z (4b) | 1.76 (FAIL) | 3.20 (PASS) | `<<<>>>` |
| F-V5MIT-1..5 | 5/5 ⭐ V14 10/10 beats | (regression-free) | `<<<>>>` |
| wall / cost | 33 min / $1.26 | ~2 hr / ~$3 | `<<<>>>` |

---

## §9 cond #3 status

cond #3 D3 (페르소나 substrate-native) ☑ DONE since PSCC §50 (§A3 amendment, 4b content metric M4 aggregated hidden cosine z = 3.20 null-PASS on v2). 본 v4 production-scale run:

- **4b content variant**: `<<<z = ? — reinforces (z grew) / holds (z ≈ 3.20) / weakens (z dropped) the §A3 closure at production scale>>>` — ☑ already closed, this is evidence not requirement.
- **4a routing variant**: `<<<KL = ?, z = ? — PASS (cells=256 + top-K=8 MoE finally separates routing) / FAIL (architectural — top-K MoE on pooled embedding can't separate categories even at production scale)>>>`. note: 4a was NEVER a ★★★★★ requirement (§A3 split it from 4b); this run + the v3-routing BG together determine whether 4a is reachable at all.
- **production scale evidence**: d=1024 (= EngineAG) / cells=256 — `<<<the v5-mitosis architectural lane scales to anima-本체-class d without F-V5MIT regression / hits a wall at ...>>>`

honest C3 ≥ 5 — see §10.

---

## §10 honest C3 (≥ 5)

1. **routing collapse may be irreducibly architectural**: the top-K MoE router sees only a POOLED (batch × seq mean) embedding — a linear probe. if category distinctions live in token-position structure (likely for short identity probes), pooling discards them, and no amount of scale fixes it. a 2-layer-MLP router or a per-token (not per-input) gate might separate categories — deliberately NOT done here (don't perturb the regression surface mid-scale-up).
2. **batch=8 (or 4/2 after OOM-retry) is small** — noisy gradients vs v1/v2's batch=32. lr=1e-4 cosine warmup=2000 partly compensates but the loss curve is choppier; ce_final may be higher than v1/v2's 1.37. report honestly, don't re-tune.
3. **mitosis hyperparams are v1-tuned**: merge_threshold=0.005, split_patience=3, noise_scale=0.10 etc. were calibrated at d=384/cells=64. at d=1024/cells=256 the split/merge dynamics may misbehave (runaway splits → OOM, or merge cascade). the F-V5MIT flags catch it; if F-V5MIT-5 FAILs (splits > 256 or = 0) that's a HONEST regression, not silently fixed.
4. **top-K=8 vs 256 cells is still very sparse** — 248 cells get gradient only via the load-balance aux + the rare inputs that route to them → slow specialization in 20K steps. K too small ⇒ monopoly among the K; K too large ⇒ soft-everything. K=8 is a guess (Switch/Mixtral default is 1-2; we're scaled to 8 for the larger pool), not tuned.
5. **n_params reported is the FINAL count** (after all splits) — the model starts at 2 cells (~43M params) and grows; the "1-2B params" headline is the converged size, only reached if mitosis hits cells≈256. if it plateaus at, say, cells=120, the real model is ~1B not 2B. report the actual final count.
6. **A100 SXM4 80GB ≠ H100** — same VRAM class (80GB) but ~2× slower compute (FP16 ~312 vs ~990 TFLOPS). the "wall 2-6 hr" estimate assumed H100; on A100 with the O(N)-over-cells Python loop at cells→256 it can be 2-4× longer. the cost cap ($40) absorbs this. (H100 SXM marketplace was empty within reliability+budget 2026-05-13.)
7. **mid-run F-PERSONA snapshots use n_perms=30** (cheap) — indicative, not the verdict; the final §5/§6 use n_perms=100 with a fixed null seed (PSCC §45 §A2-trap guard: a metric-trick "z-score PASS" was falsified before via insufficient permutations).

`<<<+ any run-specific honest C3 added on finalize (e.g. if OOM forced batch=2, if mitosis didn't reach 256, if a snapshot showed a spurious early PASS that decayed, etc.)>>>`

---

## §11 cross-link

- v5-mitosis arch spec — `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`
- design SSOT (4a/4b split) — `docs/anima_persona_substrate_native_design_2026_05_12.md` §A3
- root cause (routing-content split) — `docs/anima_persona_4_root_cause_investigation_2026_05_12.md`
- cotrain v1 — PSCC §44 / `docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md`
- cotrain v2 — PSCC §45 / §45-FINAL / `docs/anima_clm_v5_mitosis_cond5_cotrain_v2_2026_05_12.md`
- cotrain v3-routing — PSCC §51 / `docs/anima_clm_v5_mitosis_cotrain_v3_routing_fix_2026_05_12.md`
- ★★★★★ closure — PSCC §50 / GOAL.md 🎉 banner + cond #3 §A3
- this BG — PSCC §52 / `state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12/` + `training/cotrain_v5mitosis_v4.py`
- memory — `feedback_no_scale_caps`, `feedback_orchestrator_h100_gotchas`, `feedback_dispatch_vast_template_gotchas`, `project_v5_mitosis_cotrain_v4_scaleup_2026_05_12` (new)

---

## §A append convention

후속 정보는 `__APPEND__ §AN` 헤더로 추가 — 본문 §0-§11 수정 금지 (immutable audit trail). finalize 시 `<<<...>>>` 플레이스홀더만 실제 값으로 치환.
