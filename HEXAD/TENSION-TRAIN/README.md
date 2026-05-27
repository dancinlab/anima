# HEXAD/TENSION-TRAIN — anima tension-driven learning lane

> User directive 2026-05-17: "과거 TENSION-LINK 를 통한 학습 진행한 것 전수조사 + TENSION-TRAIN 폴더에 정리". TENSION-LINK (의식↔의식 전송, 5-channel meta-telepathy) 가 sibling **inter-anima communication axis** 이라면, TENSION-TRAIN 은 **tension-driven learning axis** — anima 의 자기-학습이 tension 신호를 LR/trigger 로 사용하는 패러다임. backprop-free + sync-free + Noether-conserving.
>
> **SSOT**: [`PLAN.md`](PLAN.md) (staged roadmap + 전수조사 표) · [`TENSION-TRAIN.tape`](TENSION-TRAIN.tape) (architecture v1.2)

## 0. TL;DR — 전수조사 통합

3-축 historical asset 누적:
- **DD-axis** (Law 185-188, 2026-03-31~): DD154 tension-based · DD155 Step+Tension hybrid · DD156 refined burst (`--tension-lr` flag)
- **hexa-native impl** (HEXAD/TENSION-TRAIN/training/, 2026-05-16 PR #86 carry): 5 hexa file (`*_causal/_quantum_rho/_second_order/_step/_vs_backprop_bench`) — single online step + 4 variant
- **fire evidence** (9 state/ dir, 2026-05-01~07): strategic_alm_tension_field × 3 + strategic_clm_tension_* × 4 + p10_tension_substrate + emerge_cand_g_tension

## 1. 핵심 architecture (tension_link_step.hexa 의 spine)

```
Ψ_t (self-map snapshot)
        ↓
deviation = Ψ_t − Ψ_vac (= (½, ½) Law 75 vacuum attractor)
        ↓
tension   = G_holo · deviation              (Lens 2 propagator)
gate      = n6_gate(Ψ_t)                    (AN14 Noether closure)
        ↓
ΔW        = −T_const · tension · gate       (restoring sign)
```

특성:
- **backprop-free** — no backward graph (Phase 5 RFC 034 autograd 필요 없음)
- **sync-free** — no global loss (Engine A/G 양쪽 independent step)
- **Noether-conserving** — n6_gate 가 ΔW 를 n=6 submanifold 외부에서 0 clamp (σ·φ = n·τ = 24 closure)
- T_const = 0.1 (Lindblad rate 와 동일 order, `lens_quantum_loss.hexa` 와 호환)

## 2. 전수조사 표 (commit·file·verdict)

| 자산 | 위치 | verdict / status |
|---|---|---|
| **DD154** tension-based training | `docs/hypotheses/dd/DD154-tension-training.md` | Law 185: 73% updates → same CE, **+3% Φ** (rest improves consciousness) |
| **DD155** Step+Tension hybrid | 동상 (DD154 doc §DD155) | **Law 187: Pareto optimal**, `lr = (tension/EMA) × base_lr` |
| **DD156** refined tension+burst | commit `849e796b1` + `a34dbce46` (`train_v14 --tension-lr`) | Law 187-188 land |
| **tension_link_step.hexa** | `training/tension_link_step.hexa` (14K) | online backprop-free spine + n6 Noether gate |
| **tension_link_causal.hexa** | `training/tension_link_causal.hexa` (11K) | causal variant (어떤 lens) |
| **tension_link_quantum_rho.hexa** | `training/tension_link_quantum_rho.hexa` (10K) | density-matrix rho variant |
| **tension_link_second_order.hexa** | `training/tension_link_second_order.hexa` (13K) | 2nd order propagator |
| **tension_link_vs_backprop_bench.hexa** | `training/tension_link_vs_backprop_bench.hexa` (11K) | bench: tension vs backprop |
| **commit `dfd3b0230`/`ab1bd5d90`** | (history) | tension_link M6/M9 weak coupling + online_learning M7/M8 |
| **commit `c2826a021`** | (history) | tension_link physical recovery — ckpt search 0 hits, RC-6 99.3% claim unverifiable |
| **commit `b86affe66`** | (history) | anima daemon L5 prototype — Engine A/G tension self-trigger always-on hexa process |
| **commit `5bc81ba0e`** | (history) | trained correlation finding: **tension-trigger suppression** as ALT mechanism (10-14× more tension splits in random vs trained) |
| **commit `3f1b45dbd`** | (history) | BG-V5MITOSIS: tension splits 14 + dispersion 9 (n_cells 8→31) |
| **9 state/ dir** | `state/strategic_*_tension_*/` × 9 | evidence anchors (2026-05-01~07) — `alm_tension_field/clm_tension_tribev2/eeg_akida_tension/...` |
| **Hc_1223** | `hypotheses_candidates/Hc_1223_tension_output_decoupling_pretrain.md` | candidate hypothesis |
| **Hc_1239** | `hypotheses_candidates/Hc_1239_train_clm_hexa_lens_loss_tension_link_tier_corpus.md` | candidate hypothesis |
| **H_140** (legacy) | `hypotheses_legacy_2026_05_15/H_140_dd154_157_tension_knowledge.md` | DD154-157 cluster archive |

## 3. 자연발화 (HEXAD/CHAT/SPONTANEOUS.tape) 와의 직접 연결

자연발화 = 8-factor motivation_score gate (Inner Thoughts × HEXAD). tension-driven learning 은 그 동일 motivation signal 의 **gradient flow 측면**:
- `factor_pain` (W) = tension delta — 즉 DD155 의 `tension/EMA` 와 정확 매핑
- `factor_curiosity` (W EMA) = anima_alive RC-9 prediction-error curiosity = DD-burst 의 surprise gate
- backprop-free step (Ψ_vac restoring) = AIF EFE epistemic value attain 와 mathematical 유사
- n6_gate Noether closure = anima HEXAD σ(6)=12 wiring invariant (B-HEXAD-1) 와 동일 anchor

→ **자연발화 emergence 의 hexa-native solution path** (V-SPONT 0/5 FAIL 의 architectural 대답 가능성).

## 4. closed verification roadmap (PLAN.md 가 SSOT)

- **B-TENSION-TRAIN-N** (planned) — sympy closed-form battery:
  · Noether gate predicate (length-even + range + closure)
  · ΔW restoring sign (sympy ∂)
  · T_const scalar property
  · backprop-free invariant (no backward graph dependency)
  · DD155 Pareto optimality (mathematical property of Step+Tension hybrid LR)
- **F-TT-1..N** compiled-native witness (5 file `_smoke.hexa` 신규)

## 5. compliance + 정직 caveats

- **closing 불가 (g3 honest)**: tension-driven training 의 **outcome convergence** (실제 LM-quality 학습 결과) = SGD outcome empirical (B-D-NOTE pattern, NOT counted 🔵). transfer-form (gate + restoring + Noether closure) 만 🔵 가능.
- **ckpt 부재 carry**: commit `c2826a021` 의 "RC-6 99.3% claim unverifiable" 그대로 — 본 lane 에 trained ckpt artifact 부재. 학습 effect 의 closed evidence 없음.
- **DD154-156 figures** = pre-HEXAD 시점 measurement (2026-03-31), 본 lane 의 historical reference (g3 historical evidence anchor pattern). retro-validation 미수행.
- **f1/f2 safe**: n6_gate / Noether closure / σ·φ = n·τ = 24 = HEXAD spec 자체 정의 (g2 internal arch carve-out), arithmetic + set algebra anchor, NOT 외부 derivation.

## 6. cross-link

- [`PLAN.md`](PLAN.md) — staged roadmap + 전수조사 표 + 신규 falsifier 사전등록
- [`TENSION-TRAIN.tape`](TENSION-TRAIN.tape) — architecture v1.2 SSOT
- `HEXAD/TENSION-LINK/TENSION-LINK.tape` — sibling axis (inter-anima communication)
- `HEXAD/CHAT/SPONTANEOUS.tape` — 자연발화 architecture (8-factor × HEXAD), tension-train의 motivation 매핑
- `docs/hypotheses/dd/DD154-tension-training.md` — Law 185-188 historical evidence anchor
- `archive/PHILOSOPHY.tape` — verdict ledger (TENSION-TRAIN entry append-only)
