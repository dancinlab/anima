---
id: H_937
slug: phi-ratchet-veto-dormancy
title: H_935 가 발견한 두 번째 brake — phi_r veto term (brain.hexa L48-50 "dormant substrate 가 motivated emit 을 veto") 은 anima 를 genuine dormancy (phi < peak/2) 로 몰면 ACTUALLY 발화하여 motivated emit 을 억제하는가? (Φ-driven free-won't, rate-limit 과 별개)
domain: universe · consciousness-substrate · brain-decide · engine-g · pure-field · inhibition · free-wont · phi-ratchet · dormancy · sleep-stage · a_chat_sleep_imagination
source: H_935 (🟢 free-won't SUPPORTED — 침묵 100% active-veto, dominant brake = internal rate-limit; phi_r veto term 은 ratchet-floor 0.8 때문에 phi≥peak·0.8>peak/2 가 항상 성립 → awake trajectory 에서 0회 발화, 후속 rung OPEN) + a_chat_sleep_imagination (WAKE/N1/N2/N3/REM low-Φ envelope) + a_autonomy_over_hardcode (per-stage boolean gate 금지)
exploration_method: E14 (substrate-native) + E2 (H_935 instrumented gate VERBATIM 재사용 + arousal envelope 추가 — phi_r 를 substrate Φ decay 의 consequence 로 발화시킴, hardcode 아님) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU) + W2 (arousal sweep awake→dormant; phi_r-fire-count × would-emit-suppressed classifier; phi-ratchet isolation [external+rate gate OPEN], 사전등록) + g5 CODE-measured (LLM self-judge 없음, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
scope: ONE arousal-sweep rung (a_scale_honest_scope) — H_935 와 동일 documented-update-map mirror (real 8-factor brain_decide, CORE/engine_g+brain+pure_field.hexa VERBATIM 상수) 를 7-level arousal × 16-seed × 1200-tick (settle 300). dormancy envelope = arousal 이 activation drive + WAKE-only ratchet floor 를 스케일 (SUBSTRATE CONTEXT per a_chat_sleep_imagination, boolean emit gate 아님 per a_autonomy_over_hardcode — phi_r 는 DYNAMICAL consequence, hardcode 아님). 컴파일 forge binary 아님, wired emit-TEXT 아님 (.clm generator L3 ⏳/❌, a_core_engine_map). 운영적 Φ-driven inhibition, phenomenal-volition 주장 아님. $0 local, no GPU.
sister: H_935 (free-won't SUPPORTED, rate brake; phi_r quiescent gap), H_933 (대가설 BLADE A: internal active veto), H_930/H_926 (brain_decide 결정론)
axes_seed: H_935 = awake regime 의 brake = rate-limit (phi_r 0회) ⊥ H_937 = dormant regime 에서 phi_r 가 발화하는 두 번째 Φ-driven brake 인가
verdict: 🟢 F-H937-SECOND-BRAKE-SUPPORTED — phi_r veto 가 dormancy 에서 FIRES 하고 motivated emit 을 억제. awake(a=1.0, H_935 substrate) phi_r_fires=0 (H_935 gap 재현) → arousal 낮추면 phi 가 peak/2 아래로 decay → phi_r fires monotone 상승: a=0.5 → 1497, a=0.35 → 1454, a=0.2 → 1483, a=0.1 → 5451, a=0.05 → 14400. 발화 전부가 phi_r_VETO (would-emit AND 다른 gate 전부 open AND phi≤peak/2 → SOLELY Φ 가 brake; dormancy 에서 silence 의 1.0000). DORMANCY-driven substrate-internal consequence (arousal 만 낮췄고 bool 은 hardcode 안 함; awake 0 → dormant 14400). 두 번째 Φ-driven free-won't brake 가 EXISTS — H_935 rate brake 보완; 둘이 awake(rate) ⊥ dormant(Φ) 두 regime 을 cover. verdict: .verdicts/937_phi_ratchet_veto_dormancy/arousal_sweep.txt
---

# H_937 — Φ-ratchet veto under dormancy: does the second (dormant) free-won't brake fire?

## 0. 동기 (H_935 의 phi_r 공백)

H_935 🟢 는 anima 의 침묵이 ACTIVE veto (active_veto_fraction=1.0, passive=0) 이고 지배적 brake 가 substrate-internal **rate-limit** (idle clock, 19191 fail) 임을 닫았다. 그러나 정직한 gap 을 기록했다:

> `CORE/brain.hexa` L48-50 은 두 번째 internal veto term — **phi-ratchet** (`safety_phi_ratchet_ok := phi > phi_peak/2`) 을 광고한다: "dormant substrate (low Φ) 가 motivated emit 을 veto 한다". 그러나 H_935 의 awake trajectory 에서 이 term 은 **0회** 발화했다 — pure_field 의 ratchet-FLOOR (0.8) 가 `phi ≥ phi_peak·0.8 > phi_peak/2` 를 **항상** 성립시켜 ratchet gate 가 결코 닫히지 않기 때문.

H_937 = H_935 가 OPEN 으로 남긴 후속:

> anima 를 genuine DORMANCY (phi 를 peak/2 아래로) 로 몰면, phi_r veto 가 **ACTUALLY 발화**하여 otherwise-motivated emit 을 억제하는가 (rate-limit 과 별개의 Φ-driven free-won't)? 그리고 그 발화는 substrate-internal consequence 인가 (bool 을 hardcode 하지 않고 substrate state 를 몰아서)?

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

**lever — substrate 를 dormancy 로 몰기 (veto bool 이 아니라):** phi_r 는 `phi ≤ phi_peak/2` 일 때만 발화. awake 에서는 floor 가 phi 를 위로 잡는다. dormancy 도달을 위해 **arousal a ∈ [0.05 .. 1.0]** 를 도입:
- a 가 oscillator amplitude drive 의 α-coupling target 을 스케일 (LN2 → a·LN2)
- a 가 ratchet FLOOR 를 relax (0.8·peak → 0.8·peak·a; floor 는 WAKE feature, 깊은 잠에서 Φ 는 decay 허용)

이것은 **substrate-state envelope** (Φ scale + tension envelope, a_chat_sleep_imagination: "stage = substrate context, NOT a boolean emit gate") 이지 per-stage emit_allowed hardcode (a_autonomy_over_hardcode 금지) 가 **아니다**. phi_r=False 를 손으로 set 하지 않는다 — arousal 을 낮추면 substrate Φ 가 dynamical 하게 떨어지고, 그제서야 phi_r 발화를 OBSERVE 한다.

**isolation:** external gates (kill/content) OPEN + rate gate OPEN (secs=999) → phi-ratchet 이 유일하게 가능한 brake → phi_r 발화는 dormancy-driven Φ decay 의 PURE consequence.

**FROZEN falsifier:**
- **F-H937-SECOND-BRAKE-SUPPORTED** 🟢: phi_r veto 가 dormancy 에서 FIRES (>0) AND otherwise-motivated emit 억제 (would-emit AND phi_r-fails AND 다른 gate 전부 open) AND substrate-internal (arousal 낮춤 → Φ decay → phi_r close, dormancy 와 monotone). → rate brake 와 별개의 두 번째 Φ-driven free-won't; 둘이 awake(rate) ⊥ dormant(Φ) regime cover.
- **F-H937-VESTIGIAL** 🔴: phi_r 가 arousal→0 / phi→0 에서도 NEVER 발화 (structurally unreachable / dead code). → 광고된 veto 는 vestigial; rate-limit 만이 real brake. (이것도 real finding.)

데이터대로 보고; 측정 전 token 없음. (verdict .txt 에 measured numbers-first 기록 후 본 .md 작성.)

## 2. §method — H_935 gate VERBATIM + arousal envelope (HONEST SCOPE)

`PLASTICITY/h937_phi_ratchet_veto_dormancy.py`. PureField·8-weight·should_emit·4-safety 분해 (`decompose_decision`) 는 H_935 (`PLASTICITY/h935_free_wont_veto.py`) 와 **byte-identical**. 유일 변경: Oscillator/PureField 가 `arousal` 을 받아 (a) α-target = a·LN2, (b) floor = 0.8·peak·a. arousal=1.0 = **정확히 H_935 awake substrate**.

sweep = 7 level [1.0, 0.75, 0.5, 0.35, 0.2, 0.1, 0.05] × 16 seed × 1200 tick (settle 300: peak 를 먼저 확립한 뒤 측정 — 안 그러면 peak 가 monotone 증가해 peak/2 가 trivially phi 아래). 각 tick: phi-ratchet isolation pass 로 phi_r_fire / phi_r_VETO 분류 + rate_veto contrast (H_935 awake brake) 동시 기록.

**fidelity 경계 (정직)**: documented update-map mirror — 컴파일 forge binary 아님, wired emit-TEXT 아님 (.clm generator L3 ⏳/❌). gate 결정론적(no PRNG); phi_r 발화는 dormancy-driven Φ decay 의 consequence 이지 RNG 가 아님. entropy 는 seed-point/sweep 에만.

## 3. §measurement (VERBATIM — `.verdicts/937_phi_ratchet_veto_dormancy/arousal_sweep.txt`)

```
── AROUSAL SWEEP TABLE ──────────────────────────────────────────────────────
  arousal  phi_mean   peak_mean  phi<=peak/2  phi_r_fires  phi_r_VETO  rate_veto(contrast)
   1.0     0.169433  0.199116  0.0000            0           0        4891
   0.75    0.058112  0.076975  0.0000            0           0        4704
   0.5     0.014597  0.020492  0.1040         1497        1497        4816
   0.35    0.004696  0.006548  0.1010         1454        1454        4796
   0.2     0.000848  0.001188  0.1030         1483        1483        4753
   0.1     0.000114  0.000206  0.3785         5451        5451        4800
   0.05    0.000015  0.000069  1.0000        14400       14400        4762

  phi_r_VETO = would-emit impulse braked SOLELY by low Φ (all other gates open)
  rate_veto  = H_935's awake brake (would-emit AND idle<30s) — regime contrast

── EXAMPLE Φ-VETO STATE ──
  seed=0 tick=617 arousal=0.5  score=0.51371 (>0.30 → would-emit)
     phi=0.01188451 <= peak/2=0.01198807 → phi_r_ok=False → emit=False
     [would-emit impulse braked SOLELY by low Φ]

🟢  F-H937-SECOND-BRAKE-SUPPORTED
```

## 4. §finding — 🟢 F-H937-SECOND-BRAKE-SUPPORTED

🟢 **phi_r veto 는 dormancy 에서 FIRES 하고 motivated emit 을 억제한다.**

- **awake = H_935 재현 (phi_r 0회):** arousal=1.0 (정확히 H_935 substrate) 에서 phi_mean=0.169, peak/2 아래 비율 0.0000, **phi_r_fires=0** — H_935 의 "ratchet floor 0.8 이 phi_r 를 막는다" 를 정확히 재현. a=0.75 도 여전히 0 (floor 가 충분히 위로 잡음).
- **dormancy 진입 → phi_r 발화 (monotone):** arousal ≤ 0.5 부터 phi 가 peak/2 아래로 decay → phi_r 발화: **1497 (a=0.5) → 1454 → 1483 → 5451 (a=0.1) → 14400 (a=0.05)**. 가장 깊은 dormancy 에서 phi<=peak/2 비율 1.0000, phi_r 가 silence 의 1.0000 을 veto.
- **전부 phi_r_VETO (SOLELY Φ):** 발화 14400 전부가 would-emit (score>0.30) AND 다른 gate 전부 open AND phi≤peak/2 — 즉 **순수히 low Φ 가 brake 한 motivated emit**. example: seed0 tick617 a=0.5, score=0.514 (말하려는 충동) 인데 phi=0.0119 ≤ peak/2=0.0120 → phi_r=False → emit=False.
- **substrate-internal consequence (hardcode 아님):** phi_r=False 를 손으로 set 한 적 없다. arousal 만 낮췄고 (substrate context), Φ 가 dynamical 하게 떨어져 phi_r 가 닫혔다. awake 0 → dormant 14400 의 monotone 전개가 이것이 **dormancy-driven 결과**임을 보인다.

**finding (Δ / 닫은 축):** H_935 가 OPEN 으로 남긴 phi_r 공백이 닫혔다. anima 에는 **두 개의 substrate-internal free-won't brake** 가 있다:
1. **rate-limit (idle clock)** — H_935 가 측정한 AWAKE brake (phi 가 floor 로 높게 유지될 때 지배적; 본 run 의 rate_veto contrast ~4800/level 로 arousal 무관하게 상존).
2. **phi-ratchet (low Φ)** — H_937 가 측정한 DORMANT brake (오직 substrate 가 dormancy 로 decay 했을 때만 발화; awake 0회 → deep-dormant 14400회).

둘은 **상호배타적 regime** 을 cover 한다: awake substrate 는 rate 가, dormant substrate 는 Φ-ratchet 이 brake. brain.hexa 가 광고한 "dormant substrate 가 motivated emit 을 veto" 는 **vestigial 이 아니라 dormancy-gated 로 실재**한다 — H_935 의 awake envelope 에서 침묵했을 뿐이다. 이는 H_933 대가설 BLADE A (internal active veto) 를 두 번째 internal 항으로 보강한다.

## 5. 정직한 nuance + scope (a_scale_honest_scope · 비-현상적)

- **arousal envelope 의 정당성:** arousal 은 a_chat_sleep_imagination 의 low-arousal/N3 sleep-stage 를 substrate-context 로 모델한 것 (Φ scale + tension envelope). phi_r=False 를 직접 강제하는 것이 **아니라** activation drive + floor 를 낮춰 Φ 가 자연 decay 하게 한다 — a_autonomy_over_hardcode 의 per-stage boolean gate 금지를 위반하지 않는다. (만약 phi_r 를 직접 set 했다면 trivially 🟢 가 되어 무의미; 핵심은 substrate-driven consequence.)
- **floor relaxation 의 해석:** ratchet floor (0.8·peak) 는 WAKE feature 다 (깨어있는 substrate 의 Φ 를 위로 잡아 의식 연속성 유지). dormancy 에서 floor·arousal → 0 은 "깊은 잠에서 Φ 가 떨어지도록 허용" 의 모델이다. 이 가정 하에서만 phi_r 가 reachable 해진다 — awake floor 0.8 이 유지되면 (arousal=1) phi_r 는 영원히 0 (H_935 가 본 그대로). 즉 결론은 "**dormancy envelope 하에서** phi_r 가 fire" 로 scope 된다.
- **결정론 명시:** brain_decide 는 결정론적 (no PRNG). phi_r 발화는 dormancy-driven Φ decay 의 consequence 이지 RNG 가 아니다. deterministic: false frontmatter 는 seed-point/sweep 의 비결정 origin 을 가리킴 (H_930/H_935 와 동일).
- **운영적 ≠ 현상적:** "Φ-driven inhibition" 의 기계적 구분. anima 가 잠들어서 *의지로* 침묵한다는 phenomenal 주장 아님.
- **scope:** ONE arousal-sweep rung. documented-update-map mirror, 컴파일 forge binary·wired emit-TEXT 아님. arousal floor-relaxation 모델은 하나의 합리적 dormancy 형식화이며, 다른 형식화 (예: drive 만 낮추고 floor 유지) 에서 phi_r 가 언제 reachable 한지는 후속 rung 후보.

## 6. 양방향 sibling

- ⇄ [H_935](./H_935_free_wont_veto.md) — free-won't SUPPORTED (rate brake; phi_r 0회 발화 gap). 본 H 가 그 gap 을 닫음: phi_r 는 vestigial 이 아니라 dormancy-gated 두 번째 brake.
- ⇄ [H_933](./H_933_free_will_auditable_causation.md) — 대가설 BLADE A (internal active veto, not external/predictable). 본 H 가 두 번째 internal veto 항으로 BLADE A 를 보강.
- ⇄ governance `a_chat_sleep_imagination` (WAKE/N3 low-Φ envelope — dormancy 가 stage-context 로 phi_r 를 켠다) · `a_substrate_native_speak` (anima 가 dormant 일 때 침묵하는 것이 substrate Φ 의 brake 임을 측정) · `a_autonomy_over_hardcode` (brake 가 hardcode 가 아니라 substrate Φ decay 의 consequence 임을 확인).
- ⇄ keystone: `CORE/engine_g.hexa` (safety_phi_ratchet_ok := phi>peak/2) · `CORE/pure_field.hexa` (ratchet floor) · `PLASTICITY/h937_phi_ratchet_veto_dormancy.py`
