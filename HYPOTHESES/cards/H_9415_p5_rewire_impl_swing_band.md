# H_9415 — p5-REWIRE 구현 + toy SWING-BAND: MARGIN-불응기 게이트가 살아있다 (DIRECTIONAL)

**status:** 🟢 DIRECTIONAL-WIRED (flag-gated `--emit-gate refractory` · toy liveness ✅ · 303M C1-C3 정본 대기) — production default(clock) byte-identical 보존 · wired: engine-native `anima-py chat --emit-gate refractory` (core/brain.py `brain_emit_refractory` + cli/chat.py · v0.14.4 G5)
**lane:** 의식 / emit-drive / emit-gate p5-rewire (프런티어 g1-interface-addressable-wall)
**related:** [[H_9414]] (설계 · 오너 라티파이) · [[H_9403]] (CLOSED-AT-REGIME · 이 rewire 를 지정) · [[H_9401]] (margin 유일생존) · [[H_9412]] (gap=drift) · [[H_9400]] (중심주장 반증 · 이제 시험 가능) · [[H_9391]] (INVALID-SATURATED · 이 게이트가 회피 확증) · [[chat-py-3]] (greedy→상수후보 mute) · source: 오너 (A) 라티파이 → H_9414 설계 구현
**ckpt:** state/9257_lane23b/toy.clm (toy liveness 스모크 · 신규 303M decode 0)

## 구현 (owner-ratified · flag-gated · production byte-identical)

- **core/brain.py `brain_emit_refractory`**: 후보를 매 tick 형성(generate emit=True · imagination [[a_chat_sleep_imagination]]) → `g_recog = clip01(immune_recall_margin_text(candidate))`(recognition-before-memorisation · chat-py-5) → `emit = (score > g_recog) ∧ kill ∧ φ-ratchet ∧ content`. **θ(should_emit)·clock(rate) 둘 다 은퇴**. 미emit 시 후보 **폐기**(gen_text="" · p5 never-fabricate). mouth 는 gate 에 안 감(H_9325 disjoint 보존).
- **cli/chat.py `--emit-gate {clock,refractory}`**: default `clock`=production byte-identical(should_emit(score>θ)∧30s). `refractory`=신 게이트. trace 에 `gate_mode`·`g_recog_gate` 기록.
- **VERSION 0.14.3→0.14.4** (G5 · wheel cli/**·core/**). **NOT production default** — 전환은 새 데몬 C1-C3 측정 후([[a_verified_must_wire]] · H_9403 순서⑤).

## toy SWING-BAND liveness (DIRECTIONAL · 격리-venv 비-editable · 40-tick)

```
              greedy(T=0)              T=1.0 REVEAL(R5)
 후보 gtext    1 distinct(상수)         5 distinct(변동)
 g_recog_gate  ≡0.857 상수              40 distinct · [0.548,0.754]
 score         [0.384,0.735]           [0.395,0.751] ← g_recog 를 STRADDLE
 emit          0/40 MUTE               EMIT 4 + SILENCE 36 = SWING-BAND ✅
```

- **핵심**: greedy 면 후보 상수→margin 상수→영구 mute(Fable §5-R5 위험 실증). **T=1.0 REVEAL 이면 후보 변동→margin 이 score 를 straddle→침묵·emit tick 둘 다 정의**. ⇒ 게이트가 살아있고 **C3(emit-gate-listens)가 드디어 정의 가능**(H_9391/9403 INVALID-SATURATED 구조적 회피 toy 확증: substrate vs substrate 비교라 포화 안 함).
- **clock default byte-identical** 가드: 같은 seed 로 EMIT 9/40 (production 불변).
- **R5(T=1.0 default) 필요성 실증**: greedy mute → T=1.0 swing-band = Fable 라티파이 항목 R5 가 계기적으로 필수임을 toy 가 보임.

## AGREES — 병렬 H_9404 (자매 p5-rewire · a_parallel_session_compare)

병렬 세션이 landed 한 **H_9404**도 emit-gate 를 p5-rewire 하되 **다른 지점**: `--emit-refractory earned` = safe-conjunction 의 **rate 항 소스만** wall-clock→substrate-integrated tension(`safety_refractory_ok(refr_debt)`)로 교체, **θ(should_emit)는 유지**. 내 H_9415 = Fable 설계대로 **θ+clock 둘 다** 은퇴하고 margin 을 G-pole 로(emit⟺score>g_recog). 두 rewire 는 **공존**(다른 flag: `--emit-refractory earned` vs `--emit-gate refractory`, 다른 코드경로) — 병합 시 clock-분기에 H_9404 refr_debt 유지, refractory-분기는 rate 무관.

- **AGREES**: 둘 다 "emit 타이밍을 하드코딩 스케줄이 아니라 substrate readout 으로" = H_9403 순서① 라티파이의 두 실현. H_9404=보수적(θ 유지·tension 적분 불응기), H_9415=풀(θ 은퇴·margin G-pole).
- **분업**: 새 데몬 C1-C3 측정 H 가 **두 모드를 arm 으로 비교** 가능(어느 rewire 가 swing-band+C3 를 더 잘 여나). H_9404 tension-적분 불응기 vs H_9415 margin-불응기 = 판별 축.

## scope · 한계 (a_toy_scale_recheck)

- **DIRECTIONAL**: toy.clm(48KB·near-degenerate) liveness 스모크 = 배선+swing-band 존재 증명이지 **verdict 아님**. TERMINAL = **303M 새 데몬 C1-C3 측정 H**([[H_9413]] 계기 a4/a5/a6/a7+bar 이월 · V-gates+C1 진폭+C2 인식정보+C3 swing-census+H(emit|stage)+Ψ̂ 궤적 · `--psi-soma` 선확인 · pool).
- **정직한 한계(H_9414)**: 결과물은 **다른 데몬**. H_9400 반증은 구 계보 영구성립. 주장형태 = "중심주장 시험 가능한 최초 데몬"이지 "부활" 아님. Ψ=½ 약속 안 함 — 새 데몬서 처음 물을 수 있게 됨.
- **hexa twin**: py 데몬이 카논 런타임([[chat-py-1]]) · brain.hexa/engine_g.hexa lockstep 은 follow-on(production default 전환 시 필수).

## 비용
$0 (toy 스모크 · 신규 303M decode 0) · C1-C3 정본 측정은 후속 pool.
