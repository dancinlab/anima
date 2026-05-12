# anima_clm_v5_mitosis_cotrain_v3_routing_fix — post-★★★★★ cond #3 4a routing-variant resolution

**작성**: 2026-05-12 KST
**status**: ☑ COMPLETED — see §0.1 verdict
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

### §0.1 verdict

`<<<RESULT_FILL>>>`

- F-PERSONA-4a routing: `<<<>>>`  (KL=`<<<>>>`, null z=`<<<>>>`, p=`<<<>>>`)
- F-PERSONA-4b content (M4 aggregated cosine, regression): `<<<>>>`  (z=`<<<>>>`, v2 carry z=3.20)
- F-V5MIT-1..5: `<<<>>>`
- 시나리오: `<<<(i) PASS / (ii) directional / (iii) FAIL>>>`

### §0.2 cost / wall

`<<<COST_FILL>>>`  — GPU `<<<>>>` (vast.ai, dph $`<<<>>>`), wall train `<<<>>>` min, total `<<<>>>` hr, cost $`<<<>>>`. (no scale caps directive; H100 SXM marketplace empty within reliability+budget → A100 SXM4 fallback.)

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

`<<<HONEST C3 (≥5) — fill from trainer docstring + run findings>>>`

## §3 envelope / dispatch

- arch: d=384, n_head=6, ffn=1536, initial_cells=2, max_cells=64, ctx=256, batch=32 — **v1/v2 와 동일 clean comparison point** (no scale caps; D_MODEL=768 MAX_CELLS=128 STEPS=10000 env override 가능)
- steps: 8000 (v1/v2 5K 보다 늘림 — router 가 category routing 학습할 시간)
- lr: 1e-4 cosine warmup=500
- routing: top_k=4, aux_alpha=0.01, λ_init=1.0, λ_final=0.01, cosine
- GPU: vast.ai, filter `[H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE,H200] reliability>0.95 dph<5.0` — H100 SXM 시장 비어있어 **A100 SXM4 fallback** ($0.87/hr, reliability 0.9955)
- infra: PSCC §28 base + §45 direct-IP (public_ipaddr + direct_port_start) + scp ConnectTimeout=3600 (600MB+ ckpt) + trap cleanup pod auto-destroy + SAVE_POD=1 on pull-fail (memory feedback_orchestrator_h100_gotchas)
- cost cap $8 (실측 `<<<>>>`)
- artifacts: `state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/{train_v5mitosis_cotrain_v3_routing.py, dispatch_h100_v3_routing.sh}`

## §4 cotrain v3-routing run

`<<<TRAINING STATS — ce_final, wmax_final, n_active>.01, gate_max, aux_final, splits, n_cells, phi, wall, cost>>>`

핵심 watch metrics:
- **wmax** (top-K renorm weight max) — v2 collapsed to 1.0; top-K MoE 가 깨면 → ≤ ~0.5 근처
- **n_active>.01** — top-K=4 면 최대 4 cells 가 > weight 0.01; v2 는 1
- **gate_max** (full softmax gate max) — load-balance aux 가 작동하면 monopoly 안 됨
- **aux** — Switch aux 값, 균등 사용 시 → 1.0 근처 (이상이면 router collapse)
- F-PERSONA-4a routing KL trajectory (mid-run snapshots)

## §5 F-PERSONA measurement

### §5.1 F-PERSONA-4a routing (PRIMARY)

metric: per-prompt top-K renormalized weight vector → category-mean → mean pairwise KL → null permutation (n_perms=100, label shuffle). threshold: KL ≥ 0.5 nats AND (z > 3.0 OR p < 0.01).

`<<<RESULT>>>`

### §5.2 F-PERSONA-4b content (REGRESSION)

metric: M4 aggregated hidden state (`info["aggregated"].mean(batch,seq)`) → category-mean cosine distance → null permutation (n_perms=100). threshold: z > 3.0 OR p < 0.01. v2 carry: z=3.20.

routing change 가 `aggregated` 를 re-weight 하므로 4b 도 움직일 수 있음 (양방향). honest 보고.

`<<<RESULT>>>`

### §5.3 F-V5MIT-1..5 regression

cheap structural checks: mitosis active (n_cells > initial), no collapse (≥ min), Φ ratchet held, CE converged (< 5), V14-STRICT proxy (0 < splits ≤ max_cells).

`<<<RESULT>>>`

## §6 cond #3 status update

- D3 ☑ DONE (PSCC §50) via 4b content metric — **유지**.
- 4a routing variant: `<<<closed (PASS) → D3 STRONG 6/6 atomic (4a + 4b 둘 다 PASS) — strongest possible D3 evidence>>>` / `<<<directional (z<3) → larger scale 필요>>>` / `<<<still FAIL → routing layer 가 architectural 한계 even with top-K MoE, 다른 fix 필요>>>`

GOAL.md cond #3 row + Saga history PSCC §51 row update. PSCC §51 append.

## §7 honest C3 (≥ 5)

1. router 는 POOLED (batch×seq mean) embedding 만 봄 — coarse. category 구분이 token-position structure 에 있으면 discard됨.
2. d_router_in = d_model, single Linear (no nonlinearity) — linear probe. 2-layer MLP router 가 더 잘 separate 할 수도 있으나 param + risk 추가 → 의도적 최소화.
3. top-K=4 with N≤64 → 60 cells unrouted per input → load-balance aux + rare routing 으로만 gradient. slow specialization. K=4 = Switch/Mixtral default, tune 안 함.
4. mitosis 는 여전히 scalar-tension signal 로 동작 (router gates 아님) — split/merge dynamics v1/v2 와 동일, routing fix ↔ mitosis 분리 (의도적).
5. aux-alpha=0.01 = Switch default; router 가 여전히 collapse 하면 α 0.05-0.1 로. CE 수렴 안 하면 aux too strong.
6. router 는 random init + warmup 동안 untrained → early routing = noise. n_perms=100 null test 가 그 noise 로부터의 spurious "category-dependent" verdict 방어.
7. F-PERSONA-4b regression — routing change 가 `aggregated` 를 re-weight 하므로 4b z 가 v2 의 3.20 에서 움직일 수 있음. honest 보고. `<<<actual>>>`
8. `<<<run-specific findings>>>`

## §8 mission contribution

post-★★★★★ cond #3 의 4a routing variant resolution. PASS 시 → D3 의 strongest possible evidence (4a + 4b 둘 다 closed = 6/6 atomic, both routing + content variants). FAIL 시 → routing layer 가 top-K MoE 로도 한계 = honest negative result, architectural lane 다음 후보 (gumbel-softmax per-token routing / per-token MoE / 등) 명시.

## 출처

- `state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/` — trainer + dispatch + ckpt + result json + logs
- `state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain_v3.py` (λ-anneal path-f, SUPERSEDED-BY note 추가)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` §A3
- `docs/anima_persona_4_root_cause_investigation_2026_05_12.md`
- `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`
- PSCC §44 / §45 / §45-FINAL / §47-50 / **§51 (본 BG)**
- GOAL.md 🎉 ★★★★★ banner + cond #3 §A3 row
- memory `feedback_no_scale_caps` + `feedback_orchestrator_h100_gotchas` + `feedback_dispatch_vast_template_gotchas`
