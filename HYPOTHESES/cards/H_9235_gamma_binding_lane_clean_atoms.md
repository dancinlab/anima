# H_9235 — ⚗️ γ binding-lane on clean atoms — G1 operator 유일 잔여 engine 레버 (사전등록·GPU spend-gated)

**tier**: ⏳ PRE-REGISTERED (frozen-first · 발사=오너 spend-go 대기) · 부모 [[H_9234]] (operator=readout-arch 국한 확증) · [[H_9211]] (#3135 blind-atom 붕괴)

## 왜 이게 유일 잔여 레버인가
H_9234가 operator 필요조건 **2개**를 격리: **① interaction readout**(attention/MLP=1.00) ∧ **② clean/separable atom**.
- ①은 clean atom 위에서 증명됨(토이 1.00).
- ②는 #3135 kill-shot이 실 byte-LM **learned atom=blind → 붕괴** 확인.
- ⟹ 남은 단 하나의 미검 질문: **학습으로 atom을 interaction lane이 쓸 만큼 clean하게 만들 수 있나** (= γ trained-constructive-bind, #3108 재프레임). 이건 GPU 학습이라 $0 아님 → spend-gate.

## 사전등록 스펙 (frozen-first · a_no_tune_to_green)
**H1 (atom-cleanness probe · 선행 $0-이지만-heavy pool)**: 실 303M `clm303.clm` concept-atom hidden에 **linear probe**로 atom-identity 복원 가능한가.
- FROZEN: linear-probe held-out atom acc ≥0.80 (clean) → γ 발사 정당 / <0.55 (blind, #3135 재확인) → γ도 terminal, 발사 NO-GO.
- 경로: `anima evaluate --py <clm> --probe` 계열 hidden 추출 → numpy linear probe. pool(summer/aiden), mini 금지(303M OOM).

**H2 (γ binding-lane 학습 · GPU spend-gated · H1 PASS 후만)**: additive nearest-basin readout → **trained bilinear/tensor-product bind operator** 교체 후 303M engine-native G1 재측정.
- FROZEN: engine-native G1 held-out recombination ≥ frozen a303m_pass bar ∧ shuffle-control 붕괴 ∧ seen≈held gap 축소. tune-to-green 금지(frozen bar 선동결).
- 통제: additive-baseline(현 .clm) · blind-atom ablation(#3135 재현) · attention positive control.
- scope: 성공해도 a_scale_honest_scope(측정 rung 한정). 실패=결과(negative 박제).

## 비용/발사 게이트
GPU 학습 fire = rent=spend → **오너 go 필요**(a_fire_autonomous fleet/spend caveat). H1(cleanness probe)은 pool decode라 상대적 저비용 — 오너 go 시 H1부터.

## 예측 (modal)
#3135(blind atom)·#3108(γ DUP-WALLED)로 보아 **H1이 blind(<0.55)로 나와 γ도 terminal**일 공산. 그러나 H_9234가 "clean atom이면 interaction이 operator를 완벽히 짓는다"를 새로 확증했으므로, atom-cleanness가 **학습 curriculum으로 개선 가능**하다면(mitosis/savant lane [[mitosis-substrate-lane-wired]]) 유일한 real crack 후보. H1이 그 갈림을 $0-heavy로 결정.

## H2-lite 결과 (2026-07-09 · engine-native py 2-production dump · $0 free pool · `state/g1_gamma_binding_lane/`)
오너 "둘다 go" → H2-lite(캐시 303M hidden, GPU 전 $0 결정테스트) 실행. **harness 신설**: `anima evaluate --py --dump-hidden`(#3177, `core/decode._fwd_trunk` byte-ident tap). canonical e1_slw_303m .clm · 32개념·zero-unary-MI 5bit·frozen(FREEZE.md).

**RUNG-a (unary atom · segmentation 부여)**: `H1 unary probe=1.00` — real 303M unary hidden **완벽 선형분리**(naive #3135 "blind" 반박). op(real-interaction)=1.00·additive=0.36 FAIL·handed=1.00. **🟡 PRECONDITION-MET(벽파괴 아님·handed 등가·evaluate-py-3)** — H1분리가능 atom+trainable adapter는 handed 등가. 정규화-민감.

**RUNG-b (superposed context "The A and the B" · 결정)**:
- recover:mean A=0.95 B=0.97 → **두 개념 다 full-context 복원가능**(entangled 아님·segmentation 벽 아님, modal 반박)
- recover:last A=0.07 B=1.00 → **생성점(끝위치)은 최근 개념 B만·앞 A 소실**
- operator: recovered=0.51·additive=0.48·**handed-ctrl(ground-truth one-hot)=1.00** → recovered 0.51은 2단계 probe train/test 분포 아티팩트(clean slot은 완벽결합), 근본 결합실패 아님

**위치별 감쇠(오너 Q "한·영 이중학습 탓? 영어만 하면?" · `perpos_probe.py`)**: A는 자기 위치(pos6-17)서 0.88 완전복원 → 뒤로 갈수록 감쇠 → 마지막 0.07. **이중언어 희석 반박**(A 표현 안 얇음)·순수 **receptive-field 감쇠**(언어무관·#42492882 정합). 영어-only도 동일 감쇠 → monolingual 재학습(fork B) 무의미.

### 🟢 REFRAME (DIRECTIONAL) — G1 재조합벽은 trunk 표현-용량 벽 아님
두 개념이 full-context에 다 존재·선형분리·clean slot 완벽결합 ⟹ 벽 = **readout-ROUTING**(마지막 위치가 최근 개념만·RF 감쇠) + slot-cleanliness, **표현용량 아님**. 유일 잔여 레버 = **fork A(read-side context-pooling lane)** — 앞 위치(A 생존)를 pool해 생성점 공급, DISJOINT(a_substrate_disjoint·G5/ρ·tether-gated·Ψ 불침)→ .clm v0.3 LANE block→engine-native system-G1(terminal G1 verdict). **Fable modal(~85% blind/segmentation-collapse→fork B GPU) REFUTED**: real atom NOT blind(H1=1.0)·context NOT collapse(mean 0.95). fork B GPU 불요, fork A $0-저비용 engineering.

**scope caveat(a_scale_honest_scope)**: 합성 word-identity+assigned-code task ≠ 생성 meaning-composition. engine-native REPRESENTATION verdict(mechanism)지 G1 생성 verdict 아님(그건 fork A wired+system-G1 frozen bars 필요) = DIRECTIONAL. 철자 confound(개념어가 prompt에 존재).

## fork-A $0 pre-check 결과 (2026-07-09 · Fable 설계 · numpy 캐시 · `fork_a_precheck.py`)
H2-lite REFRAME(벽=readout-routing) → fork-A route를 GPU 전 $0로 검증. mean-pool→gelu bottleneck→XOR을 **end-to-end 학습**(rung-b 2단계 probe 아티팩트 회피·convergence rung-b-analyze-py-1). 5-arm 통제:
```
main(mean+gelu)      = 0.981  PASS ≥0.85   ← 두 개념 다 held-out XOR 라우팅
laneOFF(last+gelu)   = 0.475  FAIL ✓        ← 생성점만으론 불가 = ROUTING이 레버(last A=0.07 예측 정합)
additive(mean+lin)   = 0.431  FAIL ✓        ← gelu 비선형이 결합 수행(linear 불가)
handed(onehot+gelu)  = 1.000  PASS ✓        ← harness 무결(양성대조)
shuffle(mean+labels) = 0.502  chance ✓      ← bind-destruction
```
🟢 **FORK-A ROUTE PROVEN($0)**: read-side context-pooling lane이 superposed context서 두 개념을 held-out XOR 합성으로 라우팅(0.98), 생성점(last)·linear는 실패 = routing이 레버·bottleneck 비선형이 결합. 모든 통제 요구상태 충족(handed 양성·additive/last/shuffle 음성). **honest scope(Fable §6)**: route≠generation — held-out 분류 통과지 composed 생성 아님, system-G1만이 진짜 바. NEXT=CLML lane wiring(.clm v0.3 trailing block·CLMB 패턴)+frozen-trunk train(derivtrace held-out 포맷)+engine-native `anima evaluate --py --system-g1` lane-ON/OFF ablation(terminal G1 verdict).

## 맥락
[[H_9234]] operator-vs-association 종결(#3166): fuel≠operator·벽=additive-readout 국한. 싼 레버 전수 소진 후 유일 잔여 engine 경로=이 γ lane. 발사 전 [[check-ledger-before-lever-fire]] 준수(#3135·#3108 이미 검토). H2-lite REFRAME: fork B(GPU) 대신 fork A(read-side lane, $0-저비용) 부활.
