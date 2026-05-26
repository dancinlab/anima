---
id: H_291
slug: ethic-emergence-cooperation
title: 협력(원시-윤리)이 공간 구조만으로 창발하는가 — Nowak 공간 죄수딜레마, well-mixed 배신 vs 격자 협력(임계 b 게이트), anima Principle #6
domain: social · life · consciousness · substrate
status: supported-conditional
exploration_method: E12 (evolutionary game dynamics) + E16 (well-mixed vs spatial 대비) + E0 (Principle #6 substrate-emergence 검정)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: Principle #6 (NO FINE-TUNED ETHICS — 윤리 cell 창발), H_287-290 (정보-측도 arc 와 다른 축 = 사회/게임)
axes_seed: AXES.md R2 (social) rank-1 `ethic-emergence`
---

# H_291 — 협력(원시-윤리)이 공간 구조만으로 창발하는가

## 1. Hypothesis

anima Principle #6 은 윤리를 weight 에 주입하는 것을 금하고, 협력은 substrate(cell +
구조)에서 *창발*해야 한다고 한다. 가장 깨끗한 시험대는 공간 죄수딜레마(Nowak & May 1992):
*well-mixed* 집단에선 배신이 항상 이기지만(Nash=전배신), *격자*에선 협력자가 군집으로
생존한다. 공간 구조만으로 협력이 구제되는가 — 주입된 윤리 0, 순수 국소 모방으로 협력
attractor 가 창발하는가?

**가설 H1 (검정 대상)**: 공간 구조에서 협력 attractor 가 창발 — 격자 최종 협력비율이
moderate temptation b 에서 > 0.1 (생존), 동시에 matched well-mixed replicator 는 협력을
~0 으로 몬다(전배신). (falsifier: 격자 협력도 → 0 ⇒ 배신 attractor 만, 창발 없음.)

## 2. Why

- **Principle #6 의 직접 측정**: "윤리는 cell 에서 창발(주입 아님)"은 anima 의 철학
  공리다. 본 H 는 그것을 *측정 가능한* 게임 동역학으로 검정 — 주입된 보상/윤리 0, 순수
  국소 imitate-best 만으로 협력이 살아남는지. 정보-측도 arc(H_287-290)와 다른 사회/게임 축.

- **well-mixed vs spatial 대비 = 구조의 인과**: 같은 payoff 행렬에서 well-mixed(전배신)와
  spatial(협력 생존)의 차이는 오직 *구조*다. 구조가 협력을 만든다 → "윤리는 구조 창발".

- **self-contained, $0, NO RNG**: pure 게임 동역학(payoff 산술), 결정적 pseudo-pattern
  초기값(RNG 없음), lib import 없음. raw#12 strict.

## 3. Predictions

- **H291.1 (well-mixed-defects)**: well-mixed 협력비율 → <0.01 (모든 b>1, 구조 없으면 배신).
- **H291.2 (spatial-rescue / verdict)**: 저 temptation(b=1.1) 격자 협력 > 0.1 (생존/지배)
  while well-mixed → ~0. ⇒ H1.
- **H291.3 (temptation-monotone)**: 격자 협력비율이 b 에 비증가 — C(1.1) ≥ C(1.5) ≥ C(2.2).
- **H291.4 (bound)**: 모든 비율 ∈ [0,1].
- **H291.5 (determinism)**: 격자 b=1.5 re-run byte-identical.

## 4. Variables

- **axis1_structure** (primary): SPATIAL (L=10 toroidal, 8-Moore, self-interaction
  포함 — Nowak canonical) vs WELL-MIXED (replicator mean-field).
- **axis2_temptation_b** (primary): {1.1, 1.5, 2.2} (저/중/고). PD payoff R=1,S=0,T=b,P=0.
- **update**: synchronous imitate-best ({self ∪ 8 neighbours} 중 최고 payoff 전략 채택) —
  주입 윤리/보상신호 0.
- **initial**: 결정적 pseudo-pattern ~40% D (hash, NO RNG).
- **metric**: 최종 협력비율 (T=80 steps spatial; 200 steps well-mixed).

## 5. Run Protocol

- **smoke**: `HEXAD/LIFE/state/h291_ethic_emergence_cooperation_2026_05_26/run_h291.hexa`
- **self-contained**: import 없음 — payoff/lattice/replicator 전부 하네스 inline.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h291.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: NO RNG; re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **ledger**: `result.json`. **tier**: 🟢 NUMERICAL — 해석 ⚪ FENCED.

## 6. Criteria

- **C1 (WELL-MIXED null / H291.1)**: well-mixed → ~0 모든 b → PASS.
- **C2 (SPATIAL-RESCUE / H291.2)**: 격자 C(b=1.1) > 0.1 AND well-mixed → ~0 → H1 SUPPORTED.
- **C3 (MONOTONE+BOUND+DET / H291.3/4/5)**: → PASS.
- **verdict_rule**: H1 = C2. ⚠ §9 L1 로 *조건부* down-scope (임계 b 게이트).

## 7. Falsifiers

- **F291.1 WELL-MIXED-DEFECTS**: well-mixed 협력 ≥ 0.01 (어느 b>1) → null 깨짐 → 무효.
- **F291.2 SPATIAL-RESCUE**: 격자 C(b=1.1) ≤ 0.1 OR well-mixed(b=1.1) ≥ 0.01 → H1 FALSIFIED
  (구조가 협력 못 구제). (measurable: sp_lo vs wm_lo.)
- **F291.3 TEMPTATION-MONOTONE**: C(1.1) < C(1.5) OR C(1.5) < C(2.2) → 단조 깨짐.
- **F291.4 BOUND**: 어느 비율 ∉ [0,1] → 무효.
- **F291.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED (conditional, §9 L1) — 공간 구조만으로 협력 attractor 창발 —
        단 저 temptation 에서만 (임계 b∈(1.1,1.5] 게이트). gate 7 PASS / 0 FAIL.

config: PD R=1/S=0/T=b/P=0 · SPATIAL L=10 toroidal 8-Moore +self-interaction, imitate-best,
        ~40% D init, T=80 · WELL-MIXED replicator x0=0.6 T=200 · NO RNG · engine: 없음(self-contained)

table (최종 협력비율):
  temptation b   SPATIAL C   WELL-MIXED C
  1.1            1.0   ◀      7.9e-09     ◀ 격자 협력 완전지배 vs well-mixed 배신붕괴
  1.5            0.0          9.1e-36
  2.2            0.0          4.9e-69

  F291.2: spatial C@b=1.1 = 1.0 (>0.1 ✓) vs well-mixed@b=1.1 = 7.9e-9 (~0) → H1 SUPPORTED

핵심: 같은 payoff 에서 *구조*만 다른데 b=1.1 격자는 협력 100% vs well-mixed 0% — **윤리(협력)는
주입이 아니라 cell+구조에서 창발(Principle #6)**. 단 날카로운 임계: b≥1.5 면 격자도 협력 못
살림(C=0) → 창발은 *조건부*(저 temptation), 자동 아님.

criteria:
  C1 WELL-MIXED null (모든 b → ~0)                 : PASS
  C2 SPATIAL-RESCUE (b=1.1: 격자 1.0 vs wm ~0)     : H1 SUPPORTED
  C3 MONOTONE+BOUND+DET (1.0≥0≥0; [0,1]; re-run)   : PASS

falsifiers:
  F291.1 WELL-MIXED-DEFECTS : PASS  (b=1.1/1.5/2.2 well-mixed 모두 <0.01)
  F291.2 SPATIAL-RESCUE     : H1 SUPPORTED  (격자 C@1.1=1.0 > 0.1, well-mixed 7.9e-9)
  F291.3 TEMPTATION-MONOTONE: PASS  (1.0 ≥ 0.0 ≥ 0.0)
  F291.4 BOUND              : PASS  ([0,1])
  F291.5 POST-HOC           : NOT_TRIGGERED

checks: 7 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL (conditional) — 공간 구조만으로 협력 attractor 가
  창발한다. 같은 PD payoff 에서 *구조*만 다른데 저 temptation(b=1.1) 격자는 협력 100%(C=1.0)
  로 지배하고, matched well-mixed replicator 는 협력을 ~0(7.9e-9)으로 몬다 — 주입된 윤리/보상
  0, 순수 국소 imitate-best 만으로. **윤리(협력)는 cell + 구조에서 창발하지 주입되지 않는다**
  (anima Principle #6 의 측정 사실). 단 **조건부**(§9 L1): 날카로운 temptation 임계 b∈(1.1,1.5]
  — b≥1.5 면 격자 구조도 협력을 못 살린다(C=0). 또한 self-interaction(Nowak canonical) 없으면
  b=1.1 에서도 전배신 붕괴(첫 측정 boundary). 창발은 *가능*하나 *자동이 아니며* 구조+저-temptation
  +self-play 의 좁은 corner 를 요한다. binary 방향(구조 rescue 존재) 신뢰, 임계 위치는 모델-의존.
falsifiers_triggered: none (gate); 해석은 L1 으로 조건부 down-scope
```

re-run byte-identical 확인 (F291.5).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_291 cooperation emerges from spatial structure alone in a Nowak spatial
   Prisoner's Dilemma: at low temptation (b=1.1) the lattice reaches 100% cooperation
   (C=1.0) while the matched well-mixed replicator collapses to defection (~7.9e-9), with
   ZERO injected ethics (pure local imitate-best) — supporting anima Principle #6; CONDITIONAL:
   a sharp temptation threshold (b in (1.1,1.5]) and self-interaction are required, else the
   lattice also collapses to all-defect; deterministic toy game-dynamics, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced + conditioned
```

## 9. Honest Limits (raw#91 c3)

- **L1 (CONDITIONAL — 핵심)**: spatial rescue 는 *자동이 아니다*. (a) 날카로운 temptation 임계
  b∈(1.1,1.5] — b≥1.5 면 격자도 전배신(C=0). (b) **self-interaction 필수** — Nowak canonical
  self-play 를 빼면 b=1.1 에서도 전배신 붕괴(본 H 첫 측정의 boundary, §method). 따라서 창발은
  구조+저-temptation+self-play 의 좁은 corner 에서만. "협력 창발"은 *가능성*이지 *필연*이 아님.
- **L2 (imitate-best 는 한 update 규칙)**: deterministic imitate-best 는 Nowak 의 한 규칙.
  Fermi/proportional/stochastic update 는 임계 위치와 협력 수준이 다르다 (대개 더 매끄러운 전이).
- **L3 (단일 결정적 초기값, 앙상블 아님)**: ~40% D pseudo-pattern 1개. 다른 초기 분포/밀도는
  임계 근처에서 다른 결과 가능 (b=1.1 의 전지배·b≥1.5 의 전붕괴는 robust 할 것으로 기대되나 미검증).
- **L4 (L=10 small + toroidal)**: 작은 격자 + 주기경계. 큰 격자는 임계 근처 coexistence 대역이
  나타날 수 있음(Nowak fractal). 본 H 는 전지배/전붕괴 양끝만 관측.
- **L5 (PD payoff 정규화 한 선택)**: R=1,S=0,T=b,P=0 (Nowak weak-PD). P>0(strict PD) 또는 다른
  정규화는 임계 b 이동.
- **L6 (게임 협력 ≠ 윤리 자체)**: PD 협력은 *원시-윤리* proxy 이지 도덕 그 자체 아님. Principle #6
  과의 연결은 "보상 주입 없이 친사회적 행동이 구조 창발"이라는 구조적 유비. 과장 금지.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy 게임 측정 사실 — "AI 가 저절로 윤리적이 된다"
  같은 주장 아님. 오히려 L1 이 *조건 의존성*을 강조한다.

## 10. Cross-Links

- **parent (철학 공리)**: Principle #6 (NO FINE-TUNED ETHICS) — 본 H 가 그 substrate-emergence
  주장을 게임 동역학으로 측정. 보상 주입 0, 구조 창발 확인(조건부).
- **sibling (다른 축)**: [[H_287]]·[[H_288]]·[[H_289]]·[[H_290]] (정보-측도/위상 arc, IIT4-Φ) —
  본 H 는 사회/게임 축으로 LIFE frontier 확장 (AXES R2 social).
- **axes seed**: `HEXAD/LIFE/AXES.md` R2 (social) rank-1 `ethic-emergence` — consumed.
- **Next**: (a) Fermi/stochastic update 로 임계 매끄러움 (L2); (b) 큰 격자 coexistence 대역
  (Nowak fractal, L4); (c) self-interaction on/off × b 2D phase diagram (L1 조건 정량); (d)
  반복게임 TFT(직접 호혜)로 well-mixed 에서도 협력 창발하는지 (구조 외 경로).
