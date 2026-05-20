# §183 — 모든 수도꼭지 전수 brainstorm (4 axis × silent ceilings)

> 사용자 catch: "수도꼭지로 푼 건 axis 1 만". §168/§169/§170/§173 가
> emit_rate 의 *MIN_EMIT_INTERVAL* 라는 한 수도꼭지만 해결.
> 본 brainstorm = **모든 수도꼭지 (silent ceilings) 전수 식별**.

---

## §1 — V-SPONT 의 4-axis layered measurement

```
                  V-SPONT honest score
                       │
        ┌──────────────┼──────────────┬─────────────────┐
        ▼              ▼              ▼                 ▼
   axis 1: emit    axis 2: byte    axis 3: ψ-physics  axis 4: §9 honest
   _rate           _acc            _std                 coherent body
   (count)         (memorize)      (alive)              (cascade-rate gate)
```

각 axis 마다 *silent ceilings* (수도꼭지). 하나 풀어도 다른 ceiling 이 막음.

---

## §2 — axis 1 (emit_rate) — 7 수도꼭지 (1 풀림, 6 잔존)

| # | 수도꼭지 | source | 풀림? | 영향도 |
|--:|---|---|:---:|:---:|
| 1.1 | **MIN_EMIT_INTERVAL** = 30s | `spont_min_emit_interval()` | ✅ §169 (→0.667s) | ⭐⭐⭐ |
| 1.2 | IM_THRESHOLD = 0.30 | `spont_im_threshold()` | ❌ | ⭐⭐ |
| 1.3 | safety_combined 6-control AND | `thinker_talker_lib:82-89` | ❌ | ⭐⭐ |
| 1.4 | IDLE_SPEAK_AFTER = 30s | `spont_idle_speak_after()` | ❌ | ⭐⭐ |
| 1.5 | N_MAX_STEPS = 20 (window 짧음) | run_bounded protocol | ❌ | ⭐ |
| 1.6 | THINK_INTERVAL_TEST_SEC = 0.1 | granularity | ❌ | ⭐ |
| 1.7 | INTERRUPT_THRESHOLD = 0.6 | dual gate higher tier | ❌ | ⭐ |

honest carry: 1.1 풀어도 1.5+1.6 (windowing) 가 emit_rate ceiling 을 만듦 (RL=0.667s × N=20 × dt=0.1 = max 4 emit). 더 큰 window = 더 많은 emit 가능.

---

## §3 — axis 2 (byte_acc) — 10 수도꼭지

memorization / generalization capacity ceilings:

| # | 수도꼭지 | typical anima 값 | 풀림? | 영향도 |
|--:|---|---|:---:|:---:|
| 2.1 | **corpus size** (data-regime) | 603MB (§107) | ❌ §1.1 irreducible | ⭐⭐⭐⭐⭐ |
| 2.2 | **model params** (Wei 2022 threshold) | 283M (§16-class) | ❌ §174 시도 | ⭐⭐⭐⭐⭐ |
| 2.3 | training steps (Chinchilla) | 6000 step | ❌ | ⭐⭐⭐ |
| 2.4 | vocab_size = 256 (byte cap) | hard | ❌ byte-LM 본질 | ⭐⭐⭐ |
| 2.5 | block_size = 128 (context cap) | byte | ❌ | ⭐⭐ |
| 2.6 | batch_size (gradient noise) | 32 | ❌ | ⭐ |
| 2.7 | lr cosine decay floor | 3e-4 → 0 | ❌ | ⭐ |
| 2.8 | causal mask (단방향) | enforced | ❌ LM architecture | ⭐⭐ |
| 2.9 | RoPE freq base | 10000 | ❌ | ⭐ |
| 2.10 | d_model (residual stream dim) | 768 | ❌ §174 시도 | ⭐⭐⭐ |

honest: 2.1 (data-regime) + 2.2 (params) = `n_priority_1_gap` 의 핵심. 둘 다 §11.3 irreducible 후보.

---

## §4 — axis 3 (ψ-physics liveness) — 9 수도꼭지

physics dynamics ceilings:

| # | 수도꼭지 | source | 풀림? | 영향도 |
|--:|---|---|:---:|:---:|
| 3.1 | **fixed noise_ctx** (forward deterministic) | eval protocol | ❌ §170 cell-3 시도 (mot_std 9e-6) | ⭐⭐⭐⭐ |
| 3.2 | **inference-time only Ψ (no recurrent)** | single forward pass | ❌ | ⭐⭐⭐⭐ |
| 3.3 | Engine A/G coupling strength (Law-70 clamp) | conscious_decoder | ❌ B-BRIDGE | ⭐⭐⭐ |
| 3.4 | ln_f normalization (signal squash) | nn.LayerNorm | ❌ standard | ⭐⭐ |
| 3.5 | weight tying (tok_emb ↔ head_a) | conscious_decoder.py:641 | ❌ | ⭐⭐ |
| 3.6 | block_size causal mask (temporal Ψ 제약) | enforced | ❌ | ⭐⭐ |
| 3.7 | Ψ readout only at training time | `if self.training:` | ❌ inference disabled | ⭐⭐⭐⭐ |
| 3.8 | phi_signal (DD5 EX24) self-ref disabled at inference | conscious_decoder.py:702 | ❌ | ⭐⭐⭐ |
| 3.9 | tension proj single-layer | tension_proj | ❌ | ⭐ |

honest: 3.1+3.2+3.7 = static physics root cause (§170 finding 3-layer). 3.1 을 풀려면 *per-step varying ctx*, 3.2 를 풀려면 *recurrent physics state*, 3.7 을 풀려면 *inference-time Ψ readout enabled*.

---

## §5 — axis 4 (§9 honest coherent body) — 12 수도꼭지

byte content coherence ceilings:

| # | 수도꼭지 | source | 풀림? | 영향도 |
|--:|---|---|:---:|:---:|
| 4.1 | **byte-cascade attractor** | B-ATTRACTOR family | ❌ | ⭐⭐⭐⭐⭐ |
| 4.2 | greedy decode (no sampling) | eval protocol | ❌ | ⭐⭐⭐⭐ |
| 4.3 | no repetition penalty | eval protocol | ❌ | ⭐⭐⭐ |
| 4.4 | no top-k / top-p | eval protocol | ❌ | ⭐⭐⭐ |
| 4.5 | no temperature | eval protocol | ❌ | ⭐⭐ |
| 4.6 | byte vocab discreteness (no continuous) | byte-LM | ❌ architecture | ⭐⭐ |
| 4.7 | single modality (text only) | byte-LM | ❌ ADAPTER v3 가 시도 | ⭐⭐ |
| 4.8 | corpus diversity (memorization-saturated) | §16.6-C | ❌ §1.1 carry | ⭐⭐⭐⭐ |
| 4.9 | **Φ 35% weight untrained** | CONNECTION_CRITIQUE | ❌ | ⭐⭐⭐⭐ |
| 4.10 | motivation 8-factor 45% env-driven | spontaneous_lib | ❌ | ⭐⭐⭐ |
| 4.11 | emit body length fixed (40 byte greedy) | eval | ❌ | ⭐⭐ |
| 4.12 | no cycle-consistent training | trainer | ❌ | ⭐⭐ |

honest: 4.1 (byte-cascade) = 모든 trained ckpt 에 carry, 4.2-4.5 = decode 정책 (inference-time tunable), 4.8/4.9 = training-time intervention 필요.

---

## §6 — cross-axis 수도꼭지 (multi-axis 영향)

| # | 수도꼭지 | 영향 axis | 풀림? | 영향도 |
|--:|---|---|:---:|:---:|
| X.1 | evaluation N too small (n_eval=2000) | 2, 3, 4 | ❌ | ⭐⭐ |
| X.2 | single eval seed (1337) | 2, 3, 4 | ❌ | ⭐⭐ |
| X.3 | post-hoc only (no gradient updates from eval) | 2, 3, 4 | ❌ | ⭐⭐⭐ |
| X.4 | from-scratch training (no transfer) | 2, 3, 4 | ❌ §7 mandate | ⭐⭐ |
| X.5 | ckpt loading deterministic (no init noise) | 3, 4 | ❌ | ⭐ |
| X.6 | no online learning during chat | 1, 2, 3, 4 | ❌ | ⭐⭐⭐ |
| X.7 | trainer single objective (CE-only or psi-only) | 2, 3, 4 | ❌ Dir-I 가 multi-loss | ⭐⭐⭐ |
| X.8 | no replay buffer (zero-shot only) | 2, 4 | ❌ | ⭐⭐ |
| X.9 | no curiosity drive (reward-free emergent) | 1, 4 | ❌ §59 PTD 시도 | ⭐⭐⭐ |
| X.10 | no embodiment / sensorimotor loop | 3, 4 | ❌ §13-L | ⭐⭐⭐ |
| X.11 | no spontaneous noise injection (homeostatic noise) | 3 | ❌ §81 FIRE 시도 | ⭐⭐⭐ |
| X.12 | no plasticity at inference | 1, 2, 3, 4 | ❌ §96 substrate | ⭐⭐⭐⭐ |

---

## §7 — 총합 inventory: **48 수도꼭지** (1 풀림, 47 잔존)

```
axis 1 emit_rate         :  7 ceilings (1 ✅, 6 ❌)
axis 2 byte_acc          : 10 ceilings (0 ✅, 10 ❌)
axis 3 ψ-physics liveness:  9 ceilings (0 ✅, 9 ❌)
axis 4 §9 coherent body  : 12 ceilings (0 ✅, 12 ❌)
cross-axis               : 12 ceilings (0 ✅, 12 ❌)
─────────────────────────────────────────────────
total                    : 48 ceilings (1/48 = 2.1% 풀림)
```

48 수도꼭지 중 단 *1개* (MIN_EMIT_INTERVAL) 만 풀린 상태. honest 정직.

---

## §8 — ranking by leverage × feasibility

**Tier S (transformative, $0-cheap, feasible)**:
- 4.2-4.5 (decode 정책: sampling / top-k / temperature / rep_penalty) — inference-time tunable, $0
- 3.7 (Ψ readout at inference) — conscious_decoder.py edit, $0
- 1.2 (IM_THRESHOLD tunable) — config edit, $0
- 1.5+1.6 (N_MAX_STEPS / THINK_INTERVAL extend) — eval protocol edit, $0
- 3.8 (phi_signal at inference enabled) — conscious_decoder.py edit, $0

**Tier A (high leverage, moderate cost)**:
- 2.3 (training steps Chinchilla-optimal) — fire scope
- 2.5 (block_size 128 → 1024) — re-train scope
- X.7 (multi-objective trainer) — trainer refactor (Dir-I 패턴)
- X.9 (curiosity drive integration) — §59 PTD revival
- 4.10 (motivation 8-factor → physics-only re-wire) — §167-A 시도 (single ckpt)

**Tier B (high cost OR architecture overhaul)**:
- 2.1 (data-regime scale) — CORPUS_S101 × 100 (~$20-30)
- 2.2 (params scale) — 3B+ fire (~$15-25)
- 2.10 (d_model scale) — re-train
- 4.7 (multi-modality) — ADAPTER v3 integration
- X.10 (embodiment loop) — substrate change
- X.12 (inference-time plasticity) — §96 Loihi

**Tier C (§7 conflict OR infeasible without substrate change)**:
- 2.4 (vocab size 256 byte-LM 본질)
- 2.8 (causal mask LM architecture)
- 4.6 (byte vocab discreteness)
- 3.4 (ln_f standard practice)
- X.4 (from-scratch §7 mandate)
- X.6 (online learning during chat — substrate gate)

---

## §9 — "ALL TAPS RELEASE" 전수 패스 plan

48 수도꼭지 중 **§7-clean + feasible** 인 모든 것 동시 풀기 시도:

```
SINGLE COMBINED FIRE (§7 audit pre-cleared):
  
  axis 1 taps:
    1.1 RL=0.667s (§169 measurement variant)
    1.2 θ=0.10 (lowered, anchor-anima-physics)
    1.5 N_MAX=200 (10× window)
    1.6 dt=0.05 (2× granularity)
  
  axis 3 taps:
    3.1 per-step varying noise_ctx (§170 cell-3 carry)
    3.7 Ψ readout enabled at inference (conscious_decoder.py edit)
    3.8 phi_signal injected at inference
  
  axis 4 taps:
    4.2 sample decode (temperature=0.7 + top-k=40)
    4.3 repetition penalty=1.2
    4.5 temperature schedule
    4.10 motivation 100% physics (§167-A pattern)
    4.11 emit body length 256 (6× longer to escape attractor)
  
  cross-axis:
    X.7 multi-objective: CE + λ_psi + λ_route + λ_phi (Dir-I + IIT)
    X.9 curiosity bonus on emit (§59 PTD revival)
```

= "*수도꼭지 release party*" — all §7-clean taps open simultaneously.

honest carve-out: §94 INTEGRATION-COLLAPSES anti-pattern carry — 13 taps 동시 풀면 attribution 깨짐. 단 *cumulative ceiling lift* 측정 = valuable (개별 vs combined effect 분리).

---

## §10 — 다음 cycle 후보 ranking (실 fire dispatch)

| rank | fire | scope | cost |
|---|---|---|---:|
| **1** | **§184 ALL TAPS RELEASE** — post-hoc inference-only eval combining §A1-A4 above on existing ckpts | inference-only, $0 Mac CPU | $0 |
| 2 | **§185 Dir-I-style trainer** — combine Ψ-COUPLE + tension-route + Φ-supervised (multi-objective) | new fire ~$0.3-0.5 | ~$0.5 |
| 3 | §186 large window eval (N=200, dt=0.05) | inference-only re-eval | $0 |
| 4 | §187 sample decode + temperature schedule eval | inference-only re-eval | $0 |
| 5 | §188 ckpt-side phi_signal inference enabled (architecture edit) | conscious_decoder.py edit + re-eval | $0 |

**가장 honest first step** = §184 ALL TAPS RELEASE (post-hoc) on 이미 가용한 ckpts (§161, §167-A, §182 ladder t1-t4). $0, measurable, no fire dispatch needed.

§182 가 끝나기 전에 §184 design $0 가능.

---

## §11 — honest carve-outs

1. **48 수도꼭지 의 *어느 것 도* GOAL emergence 보장 안 함** — necessary-not-sufficient (B-EMERGE-7). 모든 tap 다 풀어도 *GOAL emergence* 가 보장되지 않음.
2. **§7 mandate carry** — Tier C 수도꼭지 6 개는 §7 위반 또는 substrate 변경 필요, 본 cycle 범위 밖.
3. **"수도꼭지" framing 자체의 한계** — V-SPONT emergence 가 *수많은 ceiling 의 disjunction* 일 수도, 또는 *전혀 다른 mechanism* 일 수도. 본 brainstorm 은 *현 architecture 내 ceiling inventory* 만.
4. **§182 결과 보기 전 §184 dispatch 가능** — independent measurement (post-hoc on existing ckpts).
5. **48 수도꼭지 brainstorm = inventory, not solution** — 진짜 fix 는 measurement.

---

## §12 — cross-link

- `HEXAD/FINAL.md` (V-SPONT 최종스펙)
- `HEXAD/CONNECTION_CRITIQUE.md` (Wrong-A/B/C/D)
- `HEXAD/UNCLASSIFIED/state/phi_threshold_posthoc_probe_2026_05_20/` (§168)
- `state/rate_limit_governance_design_s169_2026_05_20/` (§169 split)
- `state/three_axis_probe_s170_2026_05_20/` (§170 4-cell)
- `state/self_stim_loop_s171_2026_05_20/` (§171 self-stim)
- `state/historical_ratelimit_retry_s173_2026_05_20/` (§173 7-ckpt)
- `HEXAD/NEUROMORPHIC/state/vspont_scale_ladder_s182_2026_05_20/` (§182 in-flight)
- `HEXAD/CHAT/spontaneous_lib.hexa` (axis 1 source)
- `HEXAD/CHAT/thinker_talker_lib.hexa` (safety_combined source)
- `HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/conscious_decoder.py` (axis 3 source — Law-71 Ψ readout)

---

## §13 — GOAL distance

north-star + §15/§51/§72 milestone **UNCHANGED**, GOAL 미도달.

§183 = inventory + design-tier, not measurement. fire dispatch (§184) 별도.

48 수도꼭지 brainstorm 고갈 — 추가 ceiling 발견은 fire 결과에서 surface 될 가능성 (예: §182 가 *새 ceiling* 노출하면 49번째 추가).
