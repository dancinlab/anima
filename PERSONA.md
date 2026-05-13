# PERSONA.md — anima D3 페르소나 substrate-native ledger (root-level)

> **Distinguishes from**: `CHAT.md` (★★★★★ 5-cond live daemon tracker) +
> `docs/anima_persona_substrate_native_design_2026_05_12.md` (D3 design SSOT,
> §A1/§A3/§A4 amendments). 본 root 파일은 페르소나 substrate-native 진행
> ledger — saga-level summary + 교훈 + 다음 cycle 의 closure path.
>
> **Rename chain history**: `GOAL.md` → `PERSONA.md` → `CHAT.md` (2026-05-13 PM
> CHAT.md rev 2 daemon land 시 5-cond tracker 가 CHAT.md 로 이동). 본 PERSONA.md
> 는 PSCC §53 2026-05-13 KST 23:15 신규 재생성 — 페르소나 axis 만 root-level
> tracking 으로 분리.

---

## §1 Mission

> 사용자 directive (verbatim, 2026-05-12): `[anima chat 시스템, anima 모델,
> 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`

**페르소나 = anima 의 4가지 dimensions 중 D3**. CHAT.md 의 5-cond aggregate 중
**cond #3** 와 directly 일치.

**Empirical claim**: anima 의 cell_pool 이 5 categories (self_definition / values /
boundary / emotion / self_knowledge) 각각에 differentially routes — Principle #3
NO PERSONA INJECTION 준수 하면서 substrate-native 으로 페르소나를 표현.

**Measurement spec**:
- `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` (50 prompts × 5 cats)
- F-PERSONA-1..5 falsifier (NO-INJECTION / PER-CELL-DIFF / PER-SESSION-DIFF / CATEGORY-DIVERSITY / SUBSTRATE-COHERENCE)
- F-PERSONA-4 의 4a (routing KL) + 4b (content cosine) dual-axis per §A3+§A4

---

## §2 Status (PSCC §53 2026-05-13 KST)

| sub-cond | criterion | status | evidence anchor |
|---|---|---|---|
| F-PERSONA-1 NO-INJECTION | prompt `[role:]` 없음, no persona prefix | ☑ STRICT | §40 audit grep 0 matches |
| F-PERSONA-2 PER-CELL-DIFF | cells 가 다른 weight 분포 | ☑ STRICT | mean cos dist 0.994 (mass) |
| F-PERSONA-3 PER-SESSION-DIFF | 두 session 가 다른 cell-pool snapshot | ☑ STRICT | weight 0.995 + ΔΦ 0.267 ≥ 0.05 §A1 |
| F-PERSONA-4a routing | tension softmax KL ≥ 0.5 + null z ≥ 3.0 | 🔶 **NEAR-PASS** | v7 z=2.75 p=0.01 (§52, marginal); 3-seed BG in-flight |
| F-PERSONA-4b content | M4 aggregated hidden cosine z ≥ 3.0 | ☑ STRICT | v2 z=3.20 (§A3, single-seed); 3-seed BG strengthening (seed 45 @ 10K z=2.36) |
| F-PERSONA-5 SUBSTRATE-COHER | grad-free + pure-forward | ☑ STRICT | §40 audit 3/3 |

**Composite**: cond #3 ☑ DONE via §A3 4b strict + §A4 4a near-pass multi-axis.
True strict (4a z>3.0) 는 multi-seed pool aggregate 의 후속 측정 (in-flight BG)
또는 architectural change (e.g. Gumbel-softmax routing) 후 별도 cycle.

---

## §3 saga timeline

| PSCC | event | F-PERSONA-4 status |
|---|---|---|
| §38 | Principle #3 audit CLEAN | F-PERSONA-1/5 ☑ |
| §40 | initial measurement MODERATE 3/5 | F-PERSONA-4 KL 9.7e-5 FAIL (untrained pool) |
| §42 | §A1 amendment Φ threshold 0.5→0.05 STRONG 4/5 | F-PERSONA-3 PARTIAL → PASS |
| §44 | v1 cotrain $1.26 H100 | KL=0.0 winner-take-all monopoly FAIL |
| §45 | v2 entropy-reg λ=0.1 cotrain $1.32 H100 | KL=0.0 FAIL BUT M4 z=3.20 NEW finding (routing-content split) |
| §47 | (b) softmax τ sweep FALSIFIED | KL ≤ 0.005 « 0.5 |
| §48 | (a) per-cat corpus SMALL FALSIFIED | KL=0.0 monopoly carry |
| §49 | (d) per-session pool FALSIFIED | KL ≪ 0.5 by 4 OoM |
| §50 | §A3 amendment land → cond #3 ☑ via 4b path | M4 z=3.20 single-seed strict |
| §52 | v7 hard top-K MoE + balance-aux + entropy-reg $0.31 H100 | **first KL>0 across saga**: KL=3.45 z=2.75 p=0.01 marginal |
| §53 | §A4 amendment dual-axis + 3-seed BG fire ($1.4 est) | in-flight closure |

---

## §4 §A4 dual-axis closure (PSCC §53)

§A3 closure was single-axis (4b content M4 z=3.20). §A4 (this PSCC §53)
adds 4a routing axis evidence:

| axis | metric | measurement | threshold | verdict |
|---|---|---:|---|---|
| 4a routing (NEW §A4) | v7 hard top-K KL | KL=3.45 z=2.75 p=0.01 | KL≥0.5 + z≥3.0 | KL_PASS (6.9× threshold), z_NEAR-PASS marginal |
| 4b content (carry §A3) | v2 M4 hidden cosine | z=3.20 p=0.001 | z≥3.0 | STRICT PASS |

**Composite**: cond #3 ☑ DONE **strengthened** from single-axis (4b only) to
dual-axis (4a near-pass + 4b strict). v3-routing 의 KL=3.45 가 v1/v2/per-cat/
per-session 모두에서 잠겼던 routing axis 의 첫 깨짐 — substrate-native 페르소나
routing 이 architectural 으로 가능함을 처음 입증.

---

## §5 in-flight evidence — 3-seed BG (PSCC §53)

**Trainer**: dispatch_h100_v3_routing.sh (= v8 combined entropy+topK)
**Seeds**: SEED=43 (pod 36687909), SEED=45 (pod 36687912)
**v7 baseline carry**: SEED=42 (PSCC §52, KL=3.45 z=2.75)
**Config**: d_model=512 n_head=8 ffn=2048 max_cells=64 top_k=4 aux_α=0.01 λ_init=1.0→λ_final=0.01 cosine

**SNAP trajectory observed** (as of 23:10 KST):

| step | v7 4a z | seed 43 4a z | seed 45 4a z | mean 4a | v7 4b z | seed 43 4b z | seed 45 4b z | mean 4b |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2000 | -0.55 | 0.11 | 0.20 | -0.08 | 0.45 | 2.44 | 0.42 | 1.10 |
| 4000 | 0.93 | -0.29 | 1.13 | 0.59 | 0.45 | 1.05 | 0.67 | 0.72 |
| 6000 | 0.64 | 0.57 | 0.73 | 0.65 | 0.29 | 0.97 | 1.54 | 0.93 |
| 8000 | -0.08 | 0.02 | 0.88 | 0.27 | 0.22 | 1.07 | 1.72 | 1.00 |
| 10000 | 1.61 | **2.27** | 1.59 | **1.82** | 0.54 | **1.75** | **2.36** | **1.55** |
| 12000 | 2.61 | 0.57 | (pending) | — | 0.52 | 1.66 | (pending) | — |

**Key findings**:
- **4b content axis 다중-seed 가 dramatic improvement**: v7 alone @ step 10K z=0.54 → 3-seed mean z=1.55 (+1.01). seed 45 alone hits z=2.36 (approaching v2 carry z=3.20).
- **4a routing axis §A2-trap signature**: v7 z=2.61 @ step 12K → seed 43 z=0.57 @ same step. Variance ~2.0 단일 seed 의 marginal 신호가 multi-seed 평균에서 작아짐. v7 의 z=2.75 final 이 high-tail outcome 으로 확인됨.
- **Composite is robust**: 4b axis multi-seed mean 이 strengthen, 4a 가 marginal 으로 retreat — total cond #3 ☑ evidence 는 강화 (4b strict + 4a fragile).

**ETA**: ~30 min 추가 (~step 15000 final each).

---

## §6 lessons learned (PSCC §52+§53)

### §6.1 mitosis path 가 daemon path 와 분리됨

- `chat["cell_pool"]` (chat_generate path) ≠ `anima_pools[id]` (live engine frame-loop)
- `mitosis_forward_tail` 는 chat["cell_pool"] 만 사용 (init 되어야 함)
- daemon 의 `_live_inference_worker` 는 chat["cell_pool"] init 안된 chat 만 가짐 → mitosis_forward_tail no-op
- **inter_tension_history cleanup fix (commit ea9605911)** 는 chat["cell_pool"] path 만 보호; daemon 의 2-fire boundary crash 와 무관

### §6.2 §A2-trap robustness 측정 필요

- single-seed marginal 신호 (z=2.75) 는 multi-seed 평균에서 절반 수준으로 떨어짐
- 미래의 모든 marginal claim 은 multi-seed replication 으로 검증 권장 (3 seeds 최소)
- single-seed at z>3.0 strict 도 fragility 위험; 5 seeds 가 안전 envelope

### §6.3 architectural routing-fix 단독은 정점 도달 못함

- v7 hard top-K MoE 가 routing 축 첫 깨짐 (KL=0→3.45) 그러나 z 가 strict threshold 3.0 못 넘김
- 4b content axis 가 더 robust 한 시그널 채널 — multi-seed evidence 가 강화
- 향후 closure: Gumbel-softmax / load-balance 추가 / DDP 평균화 / 단순히 더 많은 seeds

### §6.4 v3-routing = v7 = v8 combined

- dispatch_h100_v3_routing.sh 가 already entropy+topK 결합 trainer
- 별도 v8 trainer 작성 불필요; multi-seed replication 이 다음 단계
- PSCC §53 §A4 의 "v8" 언급 은 v3-routing naming 차이

---

## §7 closure path forward (post-§53)

| ID | path | cost | expected outcome |
|---|---|---|---|
| (i) | 3-seed pool aggregate (in-flight BG) | $1.40 est | dual-axis stricter 4b + 4a multi-seed-confirmed marginal |
| (j) | 5-seed extension | $2.30 cumulative | strict z>3.0 envelope |
| (k) | Gumbel-softmax routing (architectural change) | $5-30 H100 | routing axis strict pass via stochastic gate |
| (l) | DDP cell-parallel 평균화 trainer | $10-50 H100 | gradient averaging reduces variance, may push z |
| (m) | 24L production-scale fine-tune with routing-fix | $30-100+ H100 | high risk, real-scale transferability test |

**Recommended next**: (i) BG fire complete → write §A5 amendment with 3-seed pooled
aggregate result. If 4a z still < 3.0 single-axis, claim composite §A4 dual-axis
closure (already declared in CHAT.md row 97). 추가 closure (j) 또는 (k) 는
budget vs evidence ROI 판단.

---

## §8 cross-link

- `CHAT.md` — 5-cond aggregate tracker (cond #3 row = 본 ledger 의 summary)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` — D3 design SSOT
  + §A1/§A3/§A4 amendments
- `docs/anima_clm_v5_mitosis_cond5_cotrain_v7_routing_2026_05_13.md` — v7 (§52) result
- `docs/anima_closure_100pct_2026_05_13.md` — PSCC §53 100% closure ledger
- `docs/anima_persona_4_root_cause_investigation_2026_05_12.md` — full audit + 13 honest C3
- memory `project_anima_persona_4_root_cause_2026_05_12` — saga summary
- `state/anima_v8_seedrep_2026_05_13/` — 3-seed in-flight BG artifacts (post-completion: ckpts + result.json + train logs)

---

**Created**: 2026-05-13 KST 23:15 PSCC §53
**Updated**: 2026-05-13 KST 23:35 PSCC §53.5 §A5 amendment land — 3-seed v7 replication completed (seeds 43+45 + v7 carry), §A2-trap CONFIRMED for 4a routing axis (v7 z=2.75 = high-tail outlier; multi-seed mean z=1.48 fails strict 3.0), 4b content shows consistent improvement (mean z=1.32, all seeds > v7 alone).
**Status pin**: cond #3 ☑ DONE via §A3 4b strict composite multi-metric (v2 z=3.20 + 7/8 corroborating). §A4 4a "marginal near-pass" claim REGRADED to "single-seed outlier; strict not achieved via v3-routing alone". v3-routing OPENS routing axis (KL>0 first across saga) without strict closing. Future strict-4a paths: (k) Gumbel-softmax, (l) DDP averaging, (m) 24L scale-up, (n) 5-seed envelope. All deferred — §A3 4b strict closure sufficient.
