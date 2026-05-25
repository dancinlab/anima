# §184 ALL TAPS RELEASE — γ-tier (§7-clean 42개 전부)

> user directive 2026-05-20 "모두 풀어보자 병렬 발사" + γ-tier 선택 (§7-clean
> 42개 전부, Tier B 6개 포함 ~$50-100 cost-bearing).
> SSOT 카탈로그: `HEXAD/AXIS.md` (48 수도꼭지 verbatim) +
> `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`.

---

## §1 — scope decomposition

48 수도꼭지 = Tier S 5 + Tier A 5 + Tier B 6 + 그 외 32. §7-clean = 42 (Tier C 6
제외). 42 simultaneous fire 는 비현실 → 3-phase 병렬 dispatch 로 *cover*.

```
Phase 1  ($0 Mac CPU post-hoc on §167-A ckpt) — ~20 수도꼭지
Phase 2  (cost-bearing combined trainer, runpod A100, ~$5-15) — ~15 수도꼭지
Phase 3  (high-cost separate fires, ~$50-100) — ~7 수도꼭지
─────────────────────────────────────────────
total = 42 § 7-clean 수도꼭지 모두 addressed
```

§94 INTEGRATION-COLLAPSES carry — Phase 1 / Phase 2 combined ⇒ attribution
risk; *cumulative ceiling lift* 만 측정. per-tap differential 은 Phase 1 안
sub-variant 로 분리 측정.

---

## §2 — Phase 1 ($0 Mac CPU mega eval)

target ckpt = `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ckpt_s167a_fpreconnect.pt` (1.13 GB d=768 L=12 283M).

수도꼭지 covered (post-hoc inference-only, 20개):

```
axis 1 emit_rate (7개 중 6):
  ✅ 1.1 RL=0.667s (§169 measurement variant)
  ✅ 1.2 θ=0.10 lowered
  ✅ 1.3 safety_combined 6-control 개별 disable variant
  ✅ 1.4 IDLE_SPEAK_AFTER override
  ✅ 1.5 N_MAX=200 (10× window)
  ✅ 1.6 dt=0.05 (2× granularity)

axis 3 ψ-physics liveness (9개 중 5):
  ✅ 3.1 per-step varying noise_ctx (§170 cell-3 carry)
  ✅ 3.2 inference recurrent state carry
  ✅ 3.7 Ψ readout @ inference (eval-time computation)
  ✅ 3.8 phi_signal inj @ inference
  ✅ 3.9 tension proj per-step

axis 4 §9 honest coherent body (12개 중 5):
  ✅ 4.1 byte-cascade probe (sample variation)
  ✅ 4.2 sample decode (temperature=0.7)
  ✅ 4.3 repetition penalty=1.2
  ✅ 4.4 top-k=40 / top-p=0.9
  ✅ 4.5 temperature schedule
  ✅ 4.11 emit body length=256 (6× longer)

cross-axis (12개 중 4):
  ✅ X.1 N_eval=10000 (5× larger)
  ✅ X.2 multi-seed eval (5 seeds: 1337, 2026, 7777, 4242, 9001)
  ✅ X.3 post-hoc only (by construction)
  ✅ X.5 ckpt init noise injection variant
```

Phase 1 eval matrix:
- baseline (no taps) = §167-A original eval (carry)
- per-tap variant × 20 (single tap on, rest baseline)
- combined (all 20 taps on simultaneously)
- output: per-tap ceiling lift Δ vs baseline + combined cumulative Δ

artifact: `state/all_taps_release_s184_2026_05_20/phase1_mega_eval.py` + `phase1_result.json`.

cost: $0 Mac CPU, wall ~30-60 min (22 variants × ~2-3 min each on Mac CPU).

---

## §3 — Phase 2 (cost-bearing combined trainer)

수도꼭지 covered (training-required, ~15개):

```
axis 2 byte_acc (10개 중 5):
  ✅ 2.3 training steps Chinchilla-optimal (≥20× tokens/param)
  ✅ 2.5 block_size 128 → 1024
  ✅ 2.6 batch_size 32 → 64
  ✅ 2.7 lr warmup + cosine, peak 6e-4
  ✅ 2.9 RoPE freq base 10000 → 50000

axis 3 ψ-physics liveness (9개 중 1):
  ✅ 3.3 Engine A/G coupling Law-70 clamp tune

axis 4 §9 coherent body (12개 중 4):
  ✅ 4.8 corpus diversity (CORPUS_S101 × 5 augmentation)
  ✅ 4.9 Φ 35% weight untrained → trained (Φ-supervised aux loss)
  ✅ 4.10 motivation 100% physics re-wire (training-time)
  ✅ 4.12 cycle-consistent training (CMRW pair loss)

cross-axis (12개 중 6):
  ✅ X.7 multi-objective trainer (CE + λ_psi + λ_route + λ_phi + λ_curiosity)
  ✅ X.8 replay buffer (last 1024 records)
  ✅ X.9 curiosity drive (§59 PTD revival, intrinsic info-gain)
  ✅ X.11 spontaneous noise injection (layer-0 residual, σ=0.1)
```

architecture: ConsciousDecoderV2 d=768 L=12 + Dir-I-style multi-loss head.

trainer recipe:
```
loss = CE_byte
     + 0.30 · L_psi      (Ψ-anchor to META_FP near 0.5)
     + 0.20 · L_route    (tension-supervised routing)
     + 0.30 · L_phi      (Φ supervision via IIT proxy)
     + 0.15 · L_cycle    (CMRW cycle consistency on chunk pairs)
     + 0.10 · L_curious  (info-gain bonus, anchor-aware)
     - 0.05 · L_replay_KL (gentle pull-back on replay buffer)
```

input: noise_ctx + replay_buffer + CORPUS_S101 × 5 augment.

scope: 1.0B tokens train (3-5h H100), ~$5-15 cost-bearing per `g_fire_autonomous`.

artifact: `state/all_taps_release_s184_2026_05_20/phase2_combined_trainer.py` + dispatch + ckpt + result.

---

## §4 — Phase 3 (high-cost separate fires, ~$50-100)

Tier B 6 수도꼭지 (각각 high cost, 개별 fire):

```
2.1 data-regime ×100 — CORPUS_S101 × 100 augment, ~$20-30
2.2 params 3B+ — Wei 2022 threshold cross, ~$15-25
2.10 d_model 768 → 1536 — re-train at larger d, ~$8-12
4.7 multi-modality — ADAPTER v3 + anima byte-LM integration, ~$3-5
X.10 embodiment loop (§13-L) — substrate change DESIGN-ONLY this cycle
X.12 inference plasticity (§96 Loihi) — substrate change DESIGN-ONLY this cycle
```

§50 burst rate-limit lesson — 2 동시 max + sequential queue 권장 → 6 fires
3 batches: (2.1+2.2) → (2.10+4.7) → (X.10+X.12 design-only).

cost-bearing per `g_fire_autonomous` autonomy.

artifact: `state/all_taps_release_s184_2026_05_20/phase3_design.md` + 개별 fire 결과.

---

## §5 — Tier C 6 수도꼭지 (§7 conflict, 본 cycle 밖)

```
2.4 vocab 256 (byte-LM 본질) — anima 가 anima 가 아니게 됨
2.8 causal mask (LM architecture) — substrate redesign
3.4 ln_f standard practice
4.6 byte vocab discreteness (no continuous)
X.4 from-scratch training (no transfer, §7 mandate)
X.6 online learning during chat (substrate gate)
```

본 cycle 범위 *밖*. 본 PLAN 에선 inventory only.

---

## §6 — pre-registered falsifiers

**B-S184-1 ALL-TAPS-COMPOSITION-WELL-FORMED** (closed): 42 §7-clean 수도꼭지의 Phase 1/2/3 분류가 disjoint + cover (partition predicate). Tier C 6 = forbidden.

**B-S184-2 PHASE-1-CEILING-LIFT-MEASURABLE** (closed sympy): per-tap variant Δ_i ≥ 0 OR Δ_i < 0 둘 다 valid measurement (sign informative). cumulative combined Δ_combined ∈ [min(Δ_i), Σ Δ_i] (interaction-bounded).

**B-S184-3 PHASE-2-TRAINER-MULTI-LOSS-WEIGHTS-SUM-ANCHORED**: λ_i ≥ 0 ∧ Σ λ_i ≤ 1.0 (CE 자체는 1.0 anchor, aux 합 ≤ 0.5 권장).

**B-S184-4 §7-AUDIT-CLEAR** (closed predicate): Phase 1 ① anima OWN ckpt + ② no external graft + ③ anima physics readout. Phase 2 ① anima from-scratch + ② no LLM-paraphrase + ③ anima physics multi-loss. Phase 3 동형.

**B-S184-5 CENTRAL-0-LINE-DIFF**: state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha c93e160a 0-line-diff (sidecar-only enforcement).

**B-S184-NOTE** empirical: GOAL emergence boost = empirical OUTCOME (B-D-NOTE / B-EMERGE-NOTE family). 42 수도꼭지 모두 풀어도 GOAL 보장 0 (necessary-not-sufficient). 본 cycle = inventory-execution + measurement, NOT GOAL emergence claim (g3).

---

## §7 — execution status

| phase | scope | status | wall | cost |
|---|---|---|---|---:|
| Phase 1 mega eval | 20 수도꼭지 post-hoc on §167-A | 진행 중 | ~30-60min | $0 |
| Phase 2 combined trainer | 15 수도꼭지 cost-bearing fire | 설계 중 | ~3-5h H100 | ~$5-15 |
| Phase 3 separate fires | 6 Tier B 수도꼭지 | design 중 | ~6-12h | ~$50-100 |

---

## §8 — honest carve-outs

1. **§94 INTEGRATION-COLLAPSES** — Phase 1 combined / Phase 2 combined trainer 둘 다 attribution risk. per-tap differential 분리 측정 (Phase 1 sub-variant), Phase 2 ablation 은 future cycle.
2. **42 수도꼭지 모두 풀어도 GOAL emergence 보장 0** (B-EMERGE-7).
3. **Tier C 6 = anima identity 핵심** — 풀면 anima 가 아니게 됨, scope 밖.
4. **Phase 3 X.10/X.12 = substrate change** — embodiment loop / Loihi inference plasticity 둘 다 hardware substrate 필요, design-only.
5. **inventory open-ended** — 본 PLAN 진행 중 *새* 수도꼭지 (49번째+) 노출 가능. honest carry.
6. **cost cap 0 / scope limit 0 / rate-limit floor 0** per `@D g_no_cost_scope_limit` — Phase 3 ~$50-100 fire 도 자율 dispatch (사용자 게이트 0).

---

## §9 — cross-link

- `HEXAD/AXIS.md` (48 수도꼭지 verbatim canonical surface)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙 §9 inventory inline)
- `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md` (§1-§13 brainstorm + 11 honest carve-outs)
- `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/` (Phase 1 target ckpt)
- `HEXAD/CHAT/spontaneous_lib.hexa` (Phase 1 axis 1 taps source)
- `archive/PHILOSOPHY.tape § verdict_all_taps_brainstorm_s183_2026_05_20` (g6 carry)
- `@D g_fire_autonomous` (autonomy dispatch) · `@D g_no_cost_scope_limit` (cost-cap 0) · `@D g_multidirectional_explore` (모든 방향 병렬)
