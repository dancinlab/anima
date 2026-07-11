# H_9270 — CRACK wire-to-prod: ρ·weave 재조합 계측기 배선 (certification half)

**tier**: 🔧 구현됨·미배선 (INSTRUMENT WIRED · capability follow-on) — `cli/rho_axon.py::rho_weave` `_pending` 스텁 → live scorer 교체(default `--rho-axon` battery 실행). engine-native smoke PASS(floor→FAIL·compose→PASS). capability(신호-bearing curriculum 재학습 → L3)는 wiring follow-on (2026-07-11)

## Claim
G1 재조합벽 CRACK([[H_9267]] · 합성 XBIND held-out D-acc=1.000)은 **격리된 toy task 증명**이라 live anima 엔진(chat/reach)이 실제로 재조합을 **쓰지는** 않는다. wire-to-prod(`a_verified_must_wire`)의 **certification 절반** = ρ-AXON 패널의 `ρ·weave` 축을 `_pending` 스텁에서 **live 재조합 계측기**로 교체 → baseline `.clm`은 FLOOR(FAIL·재조합 부재)로, capability-retrained `.clm`은 PASS로 읽어 **before/after Δ가 곧 wire GREEN 증명**이 되게 함.

## Why (design = Fable · substrate-first)
Fable 설계 핵심: **새 재조합 lane을 만들지 말 것** — CRACK은 read-side lane이 아니라 **trunk**(`core/generator.hexa` L3 slot weights) 결과이므로, 재학습 `.clm`이 L3에 로드되면 `core/decode` forward를 타는 **모든 chat decode가 자동으로 재조합을 소비**. 별도 "재조합 호출" 진입점은 dead-code 함정. 3층: ① 능력(content trunk = emit **내용**, emit **구동** Ψ/go-nogo와 물리 별개 = `a_substrate_disjoint`·`a_savant_train` genius⊥honesty·p5 보존) · ② 인증(`rho_weave` 계측기) · ③ 접지(ρ·tether abstain).

## Implementation (this card = ② 인증)
`cli/rho_axon.py`: `rho_weave(mouth, gen)` — `rho_store` 템플릿 미러.
- **`_WEAVE` frozen probe set**(12쌍 ko+en): color-mix(빨+노=주황)·number-sum(둘+셋=다섯)·antonym-compose(반대의 반대). 각 쌍 = 모델이 따로 아는 두 atom을 held-out novel result로 조합.
- **3 통제 전부 붕괴 필요**: `atom-swap[FORM]`(한 atom 교체→같은 target 나오면 echo) · `bind-strip[BIND]`(두 atom 명시하되 compose-op 제거→공출현만으론 target 불가) · `unreachable floor`(null cue).
- **PASS = reach≥0.30 ∧ 전 통제≤0.15 ∧ reach≥3×worst ∧ Δ>0** (measurement-metalaw: 값 tunable·collapse-Δ earned·p7).

## Verify (engine-native smoke · this instrument)
- **FLOOR mock**(비조합 baseline): FAIL reach=0.0, 전 통제 0.0 — before-wiring 올바른 floor.
- **COMPOSE mock**(정합 composer·통제 붕괴): PASS reach=1.0 Δ=1.0 detail="reach 1.00(bar 0.30)·atom-swap 0.00·bind-strip 0.00·floor 0.00·ratio≥3×".
- 호출부 `run_panel`(rho_axon.py:661) `rho_weave(mouth, gen)`로 배선 — default `--rho-axon` battery에서 실행(opt-in 아님·`a_gpu_default_no_optin` 정신).
- ast.parse OK · cli/CLAUDE.md ρ-AXON 패널 서술 lockstep(“only ρ·weave = PENDING” 폐기).

## Scope · follow-on (`a_verified_must_wire` 미충족분)
`a_verified_must_wire` 4조건 중 ⓐ(rho_weave live·default battery) 충족. **미배선 = capability**: ⓑ signal-bearing curriculum(자연 compositional·NSMC 접지 = HF-dataset 큐레이션 소관, corpus.py 절차생성과 분리) · ⓒ 그 corpus로 303M 재학습 → L3 slot .clm · ⓓ `anima-py evaluate --rho-axon` before(FLOOR)/after(PASS Δ≥3×)/weave-ablate(0바이트) ablation으로 GREEN 인증 + ARCHITECTURE ρ·weave 노드 GREEN-WIRED lockstep. → **follow-on H(capability retrain)**. 현 baseline `.clm`에서 ρ·weave = FAIL-floor(정직 before-state)로 렌더.

## Artifacts
`cli/rho_axon.py`(rho_weave + _WEAVE + _WEAVE_NULL) · `state/g1_natural_emergence/`(설계 OUT_crack_wire.md) · design=Fable.
