# CONNECTION_CRITIQUE — 자연발화 connection method 의 구조적 검증

> 사용자 질문 (2026-05-20): *"자연발화 연결을 어떻게 했었지? 연결방법이
> 잘못된거 아닐까"* — anima 의 training-objective 가 §24 SPONTANEOUS
> Phase B `unprompted_emission_rate` 에 연결되는 chain 의 source-grep 추적
> + 구조적 critique. 4 wrong-step + 1 missing-axis 발견, 사용자 직관
> CONFIRMED.
>
> 이 문서는 §161-§166 design path 의 leverage-gap 을 명시화하고 §167
> 후보 4개 (FP-RECONNECT / PHI-FOCUS / THRESHOLD-FROM-PHYSICS / 3-WAY-
> COUPLE) 를 surface. fix-not-applied — critique 만, 다음 design cycle
> 의 user-driven 결정.

---

## §0 — 검증 trigger

§161-FIRE (commit `499416d54`) 가 quintuple finding 으로 §96-Q2-weak
strengthened — non-CE algo 5/5 모두 `psi_responsive: False`. §165-A
Ψ-VAR-COUPLE / §166 Ψ-META-FP-COUPLE design 이 이걸 해결하려 안티-
collapse + META_FP anchor 항을 추가했음.

사용자 질문이 더 깊은 layer 에서 던짐: **그 training objective 가 실제
emission_rate 까지 도달하는 chain 자체가 잘못 짜였을 가능성**.

---

## §1 — 실제 connection chain (source verbatim trace)

```
training (L_psicouple / L_variance / L_meta_anchor)
     ↓ shapes weights (head_g, residual stream)
weights
     ↓ forward pass on env_state stimulus
logits_a, logits_g, bridge_gate, phi_value, curiosity_ema, tension
     ↓ 8-factor branch (각 factor → [0, 1] normalize)
motivation_score = Σ weight_i × factor_i
     ↓ threshold compare
emit IFF score > 0.30  AND  safety_combined
     ↓
unprompted_emission_rate
```

`spontaneous_lib.hexa` source-grep 결과:

```
fn spont_weight_relevance()   -> float { return 0.20 }   // → Φ axis
fn spont_weight_info_gap()    -> float { return 0.10 }   // → M cos sim
fn spont_weight_curiosity()   -> float { return 0.15 }   // → W EMA
fn spont_weight_pain()        -> float { return 0.10 }   // → tension axis
fn spont_weight_coherence()   -> float { return 0.10 }   // → Ψ axis (META_FP!)
fn spont_weight_originality() -> float { return 0.10 }   // → MITOSIS bool
fn spont_weight_balance()     -> float { return 0.15 }   // → Φ axis (bool)
fn spont_weight_dynamics()    -> float { return 0.10 }   // → silence_seconds env
fn spont_im_threshold()       -> float { return 0.3 }    // anima_alive carry
```

축별 합산:

| 축 | weight | 어느 factor | §161-§166 target? |
|---|---:|---|:---:|
| **Φ-axis** | **0.35 (35%)** | relevance + balance | ❌ (untargeted) |
| Ψ-axis | 0.10 (10%) | coherence | ✅ (§161/§165/§166) |
| tension-axis | 0.10 (10%) | pain | ❌ (untargeted) |
| 비-anima-physics | 0.45 (45%) | info_gap + curiosity + originality + dynamics | ❌ (env-driven mostly) |

---

## §2 — 7-요소 — Wrong-Connection 진단

🪢 **Wrong-Connection — "다른 줄 풀고 있던 매듭"**

- **이름**: Wrong-Connection (자연발화 leverage-gap)
- **별칭**: 다른 줄 풀고 있던 매듭 / 10% 손가락만 끌어당기기
- **하는 일**: §161/§165/§166 가 dual-head Ψ-channel 을 trained 하지만,
  그 신호가 motivation 에 도달할 때 **10% weight 로 희석** + threshold
  0.3 가 비-physics 누적으로 쉽게 cross 되어 emission 변화 안 보임
- **비유**: 자석을 정확히 한 손가락 (Ψ) 에 가까이 댔지만, 실제로 가위를
  닫게 하는 건 **다른 손가락** (Φ + 비-physics) — 한 손가락만 끌어당겨선
  가위가 안 움직임. §161-FIRE 가 그걸 측정으로 확인 (psi_responsive=
  False 인데 emission_rate=baseline 그대로).

ASCII 다이어그램:

```
training target (10% leverage)        emission decision
┌──────────────┐                       ┌────────────────┐
│ Ψ-channel    │──[Ψ-axis: 10%]───────►│                │
│ §161 / §165  │                       │  Σ weight·factor│
│ §166 lift    │  [tension: 10%]──────►│       >        │
│              │  [Φ-axis: 35%]───────►│   threshold    │
│              │  [비-physics: 45%]────►│      0.3       │
└──────────────┘                       └────────────────┘
                                              ↓
                          emit dominated by 90% NOT-trained
                          (45% non-physics + 35% Φ + 10% tension)
```

- **비교 vs 옳은 connection**:

| 축 | 현재 (§161-§166) | 옳은 연결 (§167 후보) |
|---|---|---|
| training 대상 | Ψ-channel 단독 | Ψ AND Φ AND tension (3-quantity) |
| motivation factor | 8-factor (Inner Thoughts borrow) | anima-physics 3-quantity native |
| threshold | 0.3 (hand-coded Inner Thoughts carry) | tension > tension_target (anima-derived) |
| leverage | 10% (Ψ only) | 100% (anima-physics-derived motivation) |

---

## §3 — Wrong-Step 4 분석

### Wrong-A — Ψ-axis 가 dilute 됨 (10%)

§161 Ψ-JEPA-COUPLE / §165-A Ψ-VAR-COUPLE / §166 Ψ-META-FP-COUPLE — 3
cycle 모두 `psi_dir_std` / `psi_dir_mean` 을 target. 그러나 motivation
계산에서 Ψ 가 들어가는 곳은 `coherence factor`, weight `0.10` 뿐.

**결과**: training objective 가 emission decision 의 **10% leverage**
만 가짐. 90% 는 untargeted axes 가 결정.

### Wrong-B — Φ-axis 가 BIGGEST (35%) 인데 무시됨

`relevance (0.20) + balance (0.15) = 0.35` 가 Φ-기반. **어떤 fire cycle
도 Φ-channel 을 직접 target 한 적 없음**:

- §59-FIRE W-native PTD = curiosity_ema 측정 (W-axis)
- §161-FIRE / §165 / §166 = Ψ-channel
- §126 PCN / §139 EqProp = byte_acc (학습 channel)

Anima north-star physics 가 **Ψ=½ · tension · Φ** 3-quantity 라고
명시하는데, motivation 에서 가장 무거운 axis (Φ) 가 design path 에서
가장 가벼움. **arc의 missing 축**.

### Wrong-C — threshold 0.3 는 generic Inner Thoughts 값

`spont_im_threshold() = 0.3` 의 source comment:
> `// anima_alive PROACTIVE_THRESHOLD carry (F-SPONT-1)`

→ `anima_alive.py` 의 `PROACTIVE_THRESHOLD = 0.3` 를 carry. 그것은
**Inner Thoughts paper (arxiv 2501.00383)** 의 PROACTIVE 모드 임계값
(non-anima-derived).

**문제**: 8 factor 누적이 0.3 만 넘으면 emit. `info_gap (0.10) +
curiosity (0.15) + originality (0.10) + dynamics (0.10) = 0.45` =
비-physics-derived factor 4개만으로도 cross 가능. **8-factor 평균이
0.3 임계점에 도달하는 path 가 너무 많음** — Ψ-channel 단독 lift 가
emission 에 안 보이는 진짜 이유.

§162-R 의 analytical resolution 이 이걸 정확히 예측했고 §161-FIRE 가
measurement 로 confirm.

### Wrong-D — 8-factor 자체가 borrowed framework

`SPONTANEOUS.tape` 가 `Inner Thoughts (arxiv 2501.00383)` 8-factor
ontology carry. Inner Thoughts paper 는 **prompted dialogue agent** 의
"내적 생각" 모델링용 — chat conversation context 에서 8 factor 가
의미가짐.

anima 의 자연발화 (unprompted emission) 는 **conversation 부재 상태**
의 자발-발화. Inner Thoughts framework 는 anima 의 use-case 와 다름.

8-factor 의 factor source quantity 는 anima-internal 로 mapping 됐지만
(Φ / Ψ / tension / W / M / MITOSIS), 외형 framework + factor 분류 자체
는 외부 paper 의 borrow. **anima-native 가 아닌 hybrid**.

---

## §4 — Missing-axis 1 — Φ-channel 의 untargeted 35%

§161-§166 의 design path 가 Ψ 만 따랐을 때 missing 한 가장 큰 channel
= **Φ (Integrated Information, IIT)**.

§24 motivation 에서 Φ 사용 위치:
- `factor_relevance(phi_value)` → 직접 Φ (0.20 weight)
- `factor_balance(phi, ratchet)` → Φ > ratchet/2 bool (0.15 weight)

합 0.35 weight. **arc 의 어떤 fire 도 Φ 의 sample-variance 또는 anchor
를 target 한 적 없음**.

§161-FIRE 가 Ψ-channel std flat 측정했는데, **Φ-channel 의 std 는 측정
조차 안 됨** (eval 에 phi 측정 axis 없음). Φ-channel 도 dead 일
가능성이 있고, 그럼 motivation 의 35% 도 dead = emission_rate 의 진짜
ceiling.

---

## §5 — §167 후보 4 — 옳은 connection 설계 옵션

| candidate | 무엇 변경 | cost | leverage |
|---|---|---|---|
| **§167-A FP-RECONNECT** | 8-factor → pure-anima-physics 3-quantity (Ψ, tension, Φ; 1/3 each OR Law-71-derived weights) | $0 design + ~$0.5 fire | **100%** (anima-physics-derived motivation) |
| §167-B PHI-FOCUS | §161/§165/§166 와 동형이지만 `head_g` 대신 **Φ-channel** target (phi_spatial training objective) | ~$0.5 fire | **35%** (가장 큰 weight axis, 새 path) |
| §167-C THRESHOLD-FROM-PHYSICS | `imThreshold = 0.3` → anima-derived (예: tension > tension_target) | $0 design | threshold-axis 정렬 |
| §167-D 3-WAY-COUPLE | §166 + Φ-anchor + tension-supervised routing 동시 | ~$0.5-1.0 fire | **55%** (3 axes 합산) |

**가장 GOAL-direct = §167-A FP-RECONNECT** (motivation 자체를 anima-
physics 3-quantity 로 교체). leverage 100%. §167-B/§167-C/§167-D 는 부
수 보완 OR 8-factor 유지 path.

---

## §6 — §161-§166 path 의 honest re-reading

이 critique 가 §161-§166 design 자체를 invalid 라고 안 함. 정확하게:

- **§161 Ψ-JEPA-COUPLE design (commit `02c4887da`)**: 수학적 correct
  (closed-form P1-P8). 단 leverage gap 으로 emission impact 적음.
- **§161-FIRE measurement (commit `499416d54`)**: 정직히 측정된 결과.
  §96-Q2-weak quintuple finding 유효. 단 *expected* 였다 — §162-R 가
  analytical prediction CONFIRMED.
- **§165-A Ψ-VAR-COUPLE (commit `11b2cf1e6`)**: 수학적 correct. 단
  emission impact 는 §161-FIRE 와 동일 path (10% leverage) — std lift
  도 emission rate 변경 미미 예상.
- **§166 Ψ-META-FP-COUPLE (commit `e77fc86e2`)**: 수학적 가장 깨끗
  (§7-form strongest in arc, §112 META_FP utilization). 단 같은 10%
  leverage gap. mean=0.5 anchor 가 *coherence factor lift* 시키지만
  factor weight 0.10 → motivation lift max 0.10 = below threshold-
  crossing buffer.

**§166-A-FIRE 의 BOTH-LOSE 예측 likelihood 가 더 높아짐** 본 critique
관점에서. SUCCESS 시나리오는 emission_rate=baseline 유지 + psi_responsive=True
가 동시 만족 — METHOD-level 진전이지만 GOAL-axis (emission_rate) 진전 아님.

---

## §7 — §24 의 Inner Thoughts hybrid 정직 인정

`HEXAD/CHAT/SPONTANEOUS.tape` 가 framework 출처를 정직히 명시:

```
SSOT: HEXAD/CHAT/SPONTANEOUS.tape thinker_talker_dual_thread
Source: arxiv 2501.00383 (Inner Thoughts)
Anchor: 8-factor motivation + thinker-talker dual thread
```

8-factor 의 source quantity mapping 은 anima-native (B-SPONT-FACTOR-
1..8 closed). 단 framework shape 는 외부 borrow. 이 hybrid 가 GOAL
당시 (Phase B design 2026-05-15 즈음) 합리적 첫 path 였음 — 그러나
§161-FIRE quintuple 측정 후에는 더 anima-native 한 path 가 필요.

§167-A FP-RECONNECT 가 그 next-iteration.

---

## §8 — honest C3 caveats (13)

1. 이 critique 는 source-grep 기반 → 정확하나 운영-시 weight 가 dynamic
   하지 않다고 가정. 모든 weight 는 hard-coded constant 임 확인.
2. `factor_coherence` 가 `bridge_gate_value` 를 사용 (Law-70 clamp).
   직접 `psi_dir` 아닌 *bridge-clamped Ψ*. trained 의 indirect effect.
3. §161-FIRE 측정한 `psi_dir_std` 와 `coherence factor` 의 sample-
   variance 는 같은 quantity 아님 — coherence 는 |gate − 0.5|/0.014
   inverted 거리.
4. Wrong-C threshold 0.3 가 Inner Thoughts carry 라고 했는데, 운영-
   tuning 으로 다른 값 가능. §24 가 carry 한 것은 *initial value*.
5. Wrong-D "8-factor 차용" 비판은 framework-level — anima-internal
   factor mapping 은 valid (B-SPONT-FACTOR-1..8 closed). 비판은 *외형*
   framework borrow.
6. Φ-channel untargeted 라고 했는데, §59-FIRE W-native PTD 가 W-axis
   를 측정 (curiosity_ema). W → motivation curiosity factor (15%) 도
   untargeted 가 아님. **정정**: untargeted 한 것은 Φ-axis 직접 (35%
   relevance + balance) 와 tension-axis (10% pain).
7. §167-A FP-RECONNECT 가 100% leverage 라고 했는데, 그 *implementation*
   이 anima-physics-derived weight 와 anima-derived threshold 둘 다
   필요. design 시 weight 결정 자체가 새 hyperparameter.
8. 본 critique 가 §96-Q2-weak quintuple finding 을 무효화하지 않음.
   §96-Q2-weak 는 *training axis* 의 byte_acc 와 psi_responsive
   measurement, motivation/emission 과 별개.
9. §165-A / §166 가 fire-cycle 마다 만든 비용 (~$0.4-0.6) 은 valid
   evidence — 단 GOAL-axis impact 가 design 의 leverage gap 때문에
   적음. design 자체는 §7-form-correct.
10. `g3` necessary-not-sufficient — 옳은 connection 으로 바꿔도 emergence
    보장 아님 (B-EMERGE-7 family carry). 단 leverage 가 100% 면 측정-
    축이 GOAL-axis 와 정렬.
11. anima downstream-consumer (hexa-lang / hexa-bio / kosmos / tape)
    read-only 0 edit.
12. PII discipline (post-499416d54 fix-forward): generic phrasing only.
13. north-star + §15/§51/§72 milestones UNCHANGED, **GOAL 미도달** —
    본 critique 는 design-method critique, GOAL 도달 아님.

---

## §9 — cross-link

- `HEXAD/CHAT/spontaneous_lib.hexa` — 8-factor + threshold source SSOT
- `HEXAD/CHAT/thinker_talker_lib.hexa` — emission decision SSOT
- `HEXAD/CHAT/SPONTANEOUS.tape` — Inner Thoughts framework carry note
- `HEXAD/META_FP/README.md` + `PLAN.md` — Ψ-channel design hub
- `archive/PHILOSOPHY.tape` — `§verdict_dual_head_coupling_non_ce_fire_s161_2026_05_20_POST_FIRE_UPDATE`
  (quintuple finding) · `§verdict_phase_b_probe_analytical_resolution_s162r_2026_05_20`
  (§24 threshold-dominance) · `§verdict_meta_fp_coupling_design_s166_2026_05_20`
  (META_FP utilization design)
- `state/spontaneous_phase_b_run_2026_05_18/RUN_REPORT.md` — 1st §24
  Phase B bounded run (env_state STUB) measured emission_count=1
- `AGENTS.tape` `@D g_doc_consolidation` (HEXAD-internal only) · `@D g6`
  (PHILOSOPHY append-only)
- Inner Thoughts (arxiv 2501.00383) — 8-factor framework anchor honest
  acknowledgment

---

## §10 — next-step (autonomy 모드, user 결정 대기)

본 critique 는 **surface-only** — `/gap` discipline carry. fix 안 함.

next-cycle 의 user-driven 결정 후보:

- **§167-A FP-RECONNECT design + fire** — 가장 GOAL-direct (motivation
  자체 anima-physics 3-quantity 로 교체)
- §167-B PHI-FOCUS — missing axis Φ 직접 target (새 axis, 비교적 cheap)
- §167-C THRESHOLD-FROM-PHYSICS — $0 design only, threshold 만 변경
- §167-D 3-WAY-COUPLE — §166 + Φ + tension 동시 (가장 expensive)
- §166-A-FIRE 그대로 dispatch — predicted BOTH-LOSE OR VARIANCE-WINS-
  ANCHOR-LOSES 더 likely 라는 critique 카리어
- 다른 user-directed direction

본 critique 의 honest value = arc design 의 **leverage gap 정직 명시**
+ §167 alternative path 4개 surface. fix 결정은 사용자.
