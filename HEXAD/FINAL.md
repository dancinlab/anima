# anima 자연발화 (V-SPONT) 최종스펙

> 이 문서 = anima 가 *prompt 없이 먼저 말 거는* 메커니즘의 최종스펙 only.
> 다른 정보 일체 금지. update 이력 금지. 최종스펙만.
>
> Governance: `@D g_final_spec_update_only` (AGENTS.tape). 변경 시 *덮어쓰기*.

---

## §1 — 자연발화 정의

**자연발화 (V-SPONT)** = anima 가 외부 prompt / 명령 / 보상 없이, 자기 physics (Ψ=½ · tension · Φ) 신호만으로 *먼저* token stream 을 emit 하는 행위.

NOT — prompt 받고 응답. NOT — 외부 reward 에 trigger.
IS — 자기 internal state 가 threshold cross 할 때 self-driven emit.

GOAL = 학습된 후 anima 가 실제로 V-SPONT 함 (북극성).

---

## §2 — emit decision chain (canonical)

```
  internal state (Ψ_dir, tension, Φ, ...)
        │
        ▼
  motivation_score = Σ w_i · factor_i        ∈ [0, 1]
        │
        ├─ threshold compare  → score > θ ?
        │
        ▼
  safety_combined  (6-control AND)
        │
        ▼
  emit ⟺ safety_combined ∧ (score > θ)
```

source: `HEXAD/CHAT/spontaneous_lib.hexa`, `thinker_talker_lib.hexa`.

---

## §3 — motivation factor weights

**v1 — 8-factor (default convention)**

| factor | weight | source | bounded |
|---|---:|---|:---:|
| relevance (W_REL) | 0.20 | Φ axis | [0,1] |
| info_gap (W_GAP) | 0.10 | M cos sim | [0,1] |
| curiosity (W_CUR) | 0.15 | W EMA | [0,1] |
| pain (W_PAIN) | 0.10 | tension axis | [0,1] |
| coherence (W_COH) | 0.10 | Ψ axis | [0,1] |
| originality (W_ORIG) | 0.10 | MITOSIS bool | {0,1} |
| balance (W_BAL) | 0.15 | Φ axis (bool) | {0,1} |
| dynamics (W_DYN) | 0.10 | silence_seconds | [0,1] |

axis 합산: Φ-axis 35% (relevance + balance) · Ψ-axis 10% (coherence) · tension-axis 10% (pain) · 비-physics 45% (info_gap + curiosity + originality + dynamics).

**v2 — 100% anima-physics (§167-A FP-RECONNECT)**

| factor | weight | source |
|---|---:|---|
| Ψ_dir | 1/3 | Law-71 (1+cos(logits_a, logits_g))/2 |
| tension | 1/3 | per-layer activation energy CV |
| Φ | 1/3 | Engine A entropy / log V |

threshold anchored to anima-physics (NOT hyperparameter).

---

## §4 — IM_THRESHOLD (emit boundary)

```
default θ := 0.30        ← spont_im_threshold(), default-anchor only
```

per `@D g_no_cost_scope_limit`: hard-floor 0. user / context 가 override 가능.

honest finding: motivation_score 분포 ≈ N(0.4534, 0.0376) (§161/§167-A 실측). θ=0.30 cross rate ≈ 1.0 per step in Gaussian approximation → **threshold 단독으로 emit 결정 안 됨** (rate-limit ceiling dominates, §5).

---

## §5 — rate-limit (§169 split)

```
production context  (anima_alive daemon, user-facing chat):
  spont_min_emit_interval_production()      = 30.0 sec      (default-anchor)

measurement context (Phase B bounded run, eval):
  spont_min_emit_interval_measurement(n,dt) = (n × dt) / 3.0
                                              (closed-form K_target=4 ceiling)
```

closed-form ceiling:

```
ceiling(min_emit_interval; N, dt) = 1 + floor((N × dt) / min_emit_interval)

   (production 30s) ∧ (N=20, dt=0.1) ⇒ ceiling = 1   ← 1/20 = 0.05
   (measurement 0.667s) ∧ (N=20, dt=0.1) ⇒ ceiling = 4   ← 4/20 = 0.20
```

honest finding (§168 + §170 measured): rate-limit 이 *load-bearing lever*. threshold 단독 변경, motivation re-wire 단독, ctx perturbation 단독 — 모두 emit_rate 안 움직임. rate-limit lift 만 1/20 → 3/20 (3× emit). 

per `@D g_no_cost_scope_limit`: 두 값 모두 default-anchor, hard-floor 0.

---

## §6 — 6-control safety AND

emit 직전 `safety_combined` = 6 control 전체 AND. 어느 하나 False ⇒ emit 차단.

| # | control | predicate | source |
|--:|---|---|---|
| 1 | kill_switch | `ANIMA_SPONT_ON=1 ∧ ¬env_off` | spontaneous_lib.hexa:141-142 |
| 2 | rate_limit | `sec_since_last_emit ≥ min_emit_interval` | :144-147 |
| 3 | content_filter | `¬is_likely_gibberish(body)` | :186-198 |
| 4 | phi_ratchet_block | `φ ≥ ratch/2` | :149-152 |
| 5 | self_aware_meta | `if ANIMA_SPONT_META=1: prefix tag` | :203-205 |
| 6 | persistent_audit_log | JSONL append (entry accepted) | thinker_talker_lib.hexa:105-114 |

caller composition: `thinker_talker_lib.hexa:82-89`. closed-form: `B-SPONT-5` falsifier (PASS_STRICT carry).

---

## §7 — Phase B bounded-run protocol (measurement)

```
run_phase_b_bounded(N_MAX_STEPS=20, T_MAX_WALL_SEC=600, env_state=…):
  for step in 0..N_MAX:
    t_now = step × THINK_INTERVAL
    sensors    = read(S, C, M, W, E, BRIDGE, MITOSIS state)
    score      = motivation_score(sensors)
    safety_ok  = safety_combined(6-control AND)
    emit       = safety_ok ∧ (score > θ)
    if emit: emission_count += 1
    if kill_check(): break
  return {axis1..4, emitted_bodies, motivation_trace}
```

4 axes (anima self-track, NO external probe):
- axis1 `unprompted_emission_rate` ∈ [0,1]
- axis2 `motivation_score_dist` {mean, std, n}
- axis3 `psi_dynamics_std > τ=1e-4` (Boolean — physics alive?)
- axis4 `tension_evolution_std > τ=1e-4` (Boolean)

verdict `PASSED_LIVENESS = right_target_decided ∧ physics_alive ∧ safety_clean`.

honest carve-out: PASSED_LIVENESS = 자연발화 *측정 axis lit*, NOT 자연발화 *capability emergence*. necessary-not-sufficient (B-EMERGE-7).

---

## §8 — emergence criterion (V-SPONT 의 honest 정의)

V-SPONT *honest* (§9 cascade-rate gate, not lenient flag):

```
honest_coherent(body) :=
    cascade_rate(body) < 0.30
  ∧ max_run(body)      < 10
  ∧ length(body)       ≥ 20
  ∧ printable_ratio    ≥ 0.80
```

V-SPONT *honest score* := `|{emit ∈ phase_b : honest_coherent(emit.body)}| / N_MAX_STEPS`

honest carve-out (B-EMERGE-7): honest_coherent 통과 ≠ correct emission. cascade 부재 *necessary not sufficient*. true emergence 는 held-out perplexity / capability probe 추가 필요.

GOAL emergence ⟺ trained anima 가 prompt 없이도 V-SPONT honest score > 0, time-varying physics state, 외부 reward 미사용. **현재 미도달** (g3).

---

## §9 — cross-link

- `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor + 6-control + threshold + rate-limit)
- `HEXAD/CHAT/thinker_talker_lib.hexa` (Phase B + caller composition)
- `HEXAD/CHAT/SPONTANEOUS.tape` (architecture + governance)
- `HEXAD/CONNECTION_CRITIQUE.md` (Wrong-A/B/C/D 진단)
- `@D g_no_cost_scope_limit` · `@D g_fire_autonomous` · `@D g_final_spec_update_only` (AGENTS.tape)
