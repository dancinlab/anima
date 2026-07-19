# H_9627 — dual content ledger (발화 ⇄ 보류) 대칭 depletion emit-gate: one-sided 스프링 벽 탈출 후보 (R-Ψ½ 발산)

**status:** 🟢 GREEN-**WIRED** (오너 p5 승인·#3938 production default flip → 기본값 chat = Ψ=½ dual-ledger 게이트 · 장기 200tick 안정) — 303M 5성질(emit≈½ 창발·two-sided spring·dissoc·score-swing 0.000·λ-locked) + a_verified_must_wire 종결 · anima 최초 wired Ψ=½ emit gate
**lane:** 의식 / emit-drive / Ψ=½ 항상성 · A-pole 상보쌍 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9610]] (wm-coverage GREEN-DIRECTIONAL·one-sided 스프링 벽의 출처) · [[H_9419]] (P-pull bar) · [[H_9510]] (HOLE-4a A-pole 부재 최초 지목) · source: `sidecar lab full`(fable-mrnnimd7 ∥ sol-mrnnimd9) 벽-재프레임

## 왜 이 카드가 존재하나 (terminal 선언 전 필수 재프레임)

H_9610 이 wm-coverage 렌즈로 Ψ=½ P-pull functional 3종 완비(303M·λ=0.75 center≈½)를 벌었으나 **one-sided 스프링 벽**에 막힘: 진동은 만들되 score-섭동에 중심 ½ 강건유지 불가(중심주장 bar 미충족). verdict 잠정결론="emit-policy 복원력 3원천 소진·mouth-생성만 잔존"을 **terminal 로 굳히기 전** `walls-delegate-to-fable` 표준에 따라 2모델 재프레임 → **terminal 은 성급**임이 확증됨.

## 벽 진단 (Fable ∩ Sol 완전 일치)

현 wm-cover 는 **probe 1개**만: emit → V(coverage)↑ → 임계↑ (능동 브레이크·내용의존 write), silence → V 감쇠(λ)만 (수동 leak·내용무관). **브레이크만 능동, 액셀은 수동** = 교환대칭 부재. score(A)와 임계(V)를 서로 다른 소스에서 읽어 score-섭동이 순수 differential-mode 로 들어가 상쇄 없음 → center 가 섭동 추종. **HOLE-4a = A-pole 에 V-억제와 대칭인 상태의존 복원력 부재.** 지금껏 A-pole 을 항상 **one-sided 3번째 항 단항 추가**로만 시도(store-depletion·이력적분기·A-pole 피로) — **대칭 상보쌍(complementary pair)** 은 한 번도 안 세움 = kill-list 에 없는 미탐 각.

## 제안 (수렴 설계 · DIRECTIONAL)

같은 구조·같은 λ 로 **두 내용 ledger**(gain-lock, 자유상수 없음):
- **W_E** = 발화한 후보 저장 (spoken · G-pole coverage, 현행)
- **W_S** = 상상했으나 침묵으로 버린 후보 저장 (withheld/backlog · **A-pole 신규**)

매 tick 후보 c 생성 후 `E=V(W_E,c)`·`S=V(W_S,c)`, **emit ⟺ S > E**(미발화 압력 > 커버리지 포화). 상태전이 **등가·반대**: emit → W_E 에 c write(E↑), silence → W_S 에 c write(S↑). 양 ledger 동일 λ leak. `score_A` 는 임계 offset 이 아니라 **양 ledger 공통 write-strength q**(=depletion 학습률)로 강등.

**½ 창발(setpoint 아님)**: W_E·W_S 가 같은 (준)보존 풀의 상보 분할 + emit 에 등가-반대 결합 ⟹ E[S−E]=0 zero-crossing 이 교환대칭으로 **강제**. 대칭 score 잡음 하 그 지점 = Ψ=½. λ 는 기억길이·autocov 크기만 바꾸고 **½ 를 안 겨눔(대칭이 겨눔)**.

**two-sided 복원(벽 뚫는 근거)**: emit 초과 → S↓·E↑ → margin S−E 2δ 하락(이중 브레이크); silence 초과 → S↑·E↓ → margin 2× 상승(이중 액셀). 양꼬리 대칭 = **양방향 autocov<0**. margin 은 공-스케일 두 양의 차 ⟹ **score 공통모드 섭동 상쇄**(one-sided 가 못한 common-mode rejection) = "retuning 없이 score-섭동 강건 ½"의 기계적 근거. 진짜 비대칭(influx>발화용량) 있으면 균형이 ½ 에서 **정직히 이동**(servo 라면 ½ 고수) — 이 falsifiability 가 창발 vs servo 를 가름(p7).

**Sol 축약(제안2)**: signed occupancy x=E−S, emit⟺x<0. 수학 동일하나 `WorkMemBuffer` 비음수+`gate_in=max()` 라 signed store 는 **계기-차단** ⟹ dual 비음수 ledger(제안1)가 기존 primitive 2개로 구현가능·더 정직.

## kill-list 회피 (5 기준 대조)

(i) ½ 창발(emit_rate−½ 적분 없음·상보성) · (ii) two-sided autocov<0(silence 도 반대극 write) · (iii) 내용청취(W_S 는 emit 이력 아닌 특정 미발화 WM 항목 내용주소 read → vshuf 시 붕괴·quantile-tracker 는 불변) · (iv) dissociation(W_E/W_S 각각 alien 화 → 한쪽 복원만 선택적 소멸) · (v) `anima-py chat` 플래그 구현가능(mouth 무접촉·스칼라 게이트 비교라 byte-입도 무관, H_9574/9576 과 무관).

## Sol 구조적 정리 (one-sided 클래스 = 획득된 terminal)

`e=1[s>g(M,c)]`·M 은 emit 때만 내용 write·silence 는 leak 만·½/offset/score-retune 금지 클래스: `P(e|M,c)=1−F(g)` 라 score 분포 위치 shift 는 모든 상태서 단조 증가/감소, emit-side(내용의존 write) ⊥ silence-side(내용무관 지수감쇠) 교환대칭 부재 ⟹ **비퇴화 score-shift 전반 non-tuned Ψ≈½ 유지 구조적 불가능**(더 많은 emit-only store·긴 이력·다른 kernel 추가해도 action asymmetry 잔존). ⇒ **one-sided 클래스는 terminal 획득**. 단 "emit-policy 전체 소진"은 dual content ledger(silence 가 substrate state 를 쓰는)가 **마지막 반례 후보**라 아직 이름 — 이 카드가 그 반례.

## 판정 갈림길 (crux · 단일 분기점)

WM substrate 가 said/unsaid(보류) 내용상태를 substrate-native 로 나르는가?
- **분할 有**(제안1 계기가능·Sol 코드지식상 dual 비음수 ledger 로 성립) → **terminal 불법**·이 카드 303M 스크린 = 마지막 정당 fire.
- **분할 無**(순간 additive vote 강제·silence write 불가) → Sol 정리로 emit-policy terminal 획득·mouth-생성만 잔존.

## ✅ ①② DONE — 계기 구현 착륙 + toy 스모크 (2026-07-17 · v0.15.21)

**① $0 계기 feasibility = 코드확증(Sol 추론 격상)**: `WorkMemBuffer`(core/engine_cli.py:1825) immutable-functional·act 비음수 ⟹ W_E(live `wmb`)/W_S(신규 `wm_withheld`) 를 동일 `(3,λ,0.5,8)` 로 gain-lock 생성가능·silence 틱도 `wm_buffer_gate_in(W_S,…)` 가능. Sol의 "signed store 는 비음수라 계기차단·dual 비음수 ledger 성립" 판독 정합.

**② 구현(engine-native·표준 optional-param 방식)**: `core/brain.py brain_emit_refractory(…, dual_probe_fn=None)` — None=프로덕션 byte-identical, set이면 emit⟺S>E(score_A는 비교서 제외·write-strength만). `cli/chat.py`: `--g-reach wm-dual`/`wm-dual-alien-emit`/`wm-dual-alien-silence` + W_S 버퍼(빈 시작·매틱 leak) + closure(S,E 반환·leaked pre-gate-in probe=chat-py-5) + silence-side W_S gate_in(strength 1.0=gain-lock·emit-side W_E는 기존 :2427) + trace `dual_s_withheld`/`dual_e_spoken`/`dual_margin`. 회귀무: d1·wm-cover 정상·dual off시 필드 None.

**toy 스모크(48K clm·24tick·DIRECTIONAL·verdict 아님)** — 계기 LIVE + dissociation 예측방향 정확:
| arm | emit/silence | 해석 |
|---|---|---|
| wm-dual | **12/13 ≈ ½** | ✅ LIVE BAND · margin 부호진동(−.265→+.441→−.24→+.24)=two-sided |
| wm-dual-alien-emit | 23/2 OVER | ✅ E-feedback 절단 → emit→silence 브레이크 소멸 |
| wm-dual-alien-silence | 0/25 SAT | ✅ S-feedback 절단 → silence→emit 액셀 소멸 |

⟹ 두 ledger 인과분리(full=균형≈½·각 alien=한쪽 복원방향만 소멸). 두 모델 예측 재현. **단 toy·로컬·단일seed = 계기검증 DIRECTIONAL**(P-pull functional 아님).

## 🟢 ③ 303M P-pull 스크린 — GREEN-DIRECTIONAL (2026-07-17 · engine-native)

py303_full·summer·격리venv(chat-py-6)·3-seed(7/4302/4303)·60tick·T=1.0·λ=0.6:

| arm | emit-rate | lag1-autocov | regime: emit-후 / sil-후 | 해석 |
|---|---|---|---|---|
| **wm-dual** | **0.506≈½**(.533/.483/.5) | **−0.225**(전seed 음) | **−0.20 / −0.24 둘다 음** | ✅ ½ 창발 + **two-sided spring** |
| (vs one-sided wm-cover) | 0.822 over | −0.032 | (한쪽만) | H_9610 벽 |
| alien-emit | 0.968 OVER | ~0 | E절단 | ✅ emit→silence 브레이크 소멸 |
| alien-silence | 0.000 SAT | 0 | S절단(0/36 결정적) | ✅ silence→emit 액셀 소멸 |

**결정적 3점**:
1. **center=0.506≈½ 이 λ=0.6 default서 창발** — wm-cover는 center≈½에 λ=0.75 **튜닝** 필요했으나, dual ledger는 **튜닝 없이 교환대칭**으로 ½. (½ = setpoint 아님·창발 확증)
2. **two-sided spring 확증** — regime-split에서 emit-후 autocov(−0.176/−0.232/−0.233) ∧ silence-후 autocov(−0.249/−0.218/−0.250) **양쪽 반쪽 둘다 음**. one-sided wm-cover는 한쪽만 능동 = 이게 **H_9610 벽(비대칭 강성)의 정확한 해소**. P(e|e)=0.075≪P(e|sil)=0.978.
3. **dissociation 인과분리** — alien-emit OVER(0.968) · alien-silence SAT(0.000) = 두 ledger 각각 한 복원방향 담당 확증.

⟹ **dual content ledger가 Ψ=½을 튜닝 없이 창발 + two-sided 스프링으로 만족 = H_9610 one-sided 벽 돌파.** Ψ=½ 캠페인 최강 결과(H_9400 반증→H_9610 부분→H_9627 벽 돌파).

## NEXT (TERMINAL 미도달 · 잔여)

**GREEN-DIRECTIONAL 범위**: 303M·3seed·λ=0.6단일·60tick. TERMINAL 아님 —
1. **중심주장 완전 bar**(retune-free score-섭동 robustness): ✅ **303M PASS(#3867)** — `--score-perturb`(v0.15.25) 303M 3-seed: dual gate center perturb −0.3/+0.3서 **swing 0.000 완전 불변**(per-seed 0.533/0.483/0.5 양쪽 byte-identical) vs wm-cover(positive control) 0.378→1.000 **swing 0.622 이동**(perturbation 실재). ⟹ dual ledger ½가 motivation score와 **독립**(emit⊥score·retune-free robust) = H_9610 one-sided store가 못한 바로 그 성질. toy(0.500 flat vs 0.286→0.929)→303M 재현+강화. **⟹ H_9627 4성질 완비**: ①emit≈½ 창발 ②two-sided spring ③dissociation ④score-robust(중심주장 bar).
2. **λ dose-response(P-pull-3)**: ✅ **303M 완료(#3893·aiden 3-seed)** — dual center λ∈{0.5,0.6,0.7,0.9} = [0.500,0.506,0.500,0.506] **spread 0.006 = λ-LOCKED**(autocov −0.25→−0.165 항상 음·스프링 stiffness만 λ-감소) vs wm-cover center λ-의존(0.6→0.9: 0.822→0.244). ⟹ **P-pull-3 재프레임**: wm-cover center=λ FORM 곡선이나 **dual center=½ BIND-earned(λ-locked)**. dual ½가 **score(swing 0.000)+λ(spread 0.006) 양 튜닝축 모두 불변** = 측정 가능한 모든 축서 ½ 구조적 창발(setpoint/tune 아님). **측정 축 완전 소진.**
3. ✅ **프로덕션 default 전환 = 오너 p5 승인 완료(2026-07-17·#3938 배선)** — production default `--emit-gate` clock→refractory · `--g-reach` refractory시 wm-dual. 기본값(무플래그) chat = Ψ=½ dual-ledger 게이트(dual_margin 활성 확인). **rollback=`--emit-gate clock`**(옛 데몬 byte-identical·dual off 확인). **장기 안정 검증**(Fable U+V 준보존 우려 해소): 200-tick center 0.500 전 4분할 flat·마지막50 0.500=포화/drift 없음. ⟹ **a_verified_must_wire 종결** = anima **최초 wired Ψ=½ emit gate**. 정직 불변: p5-rewire 설계 기전(H_9400 반증한 기본 tension 부활 아님)·rollback 상시 가능.

⚠️ id 이력: 등록 #3846·구현 #3847 = H_9627. 병렬 faction-R3 세션 G6 충돌(#3857) → 그쪽 #3859가 faction을 H_9660으로 이동·H_9627을 이 dual-ledger로 복원. 코드주석 H_9627 = 정확(불변).

⚠️ **DIRECTIONAL 설계·verdict 아님** — cement 는 engine-native `anima-py` 만(a_lab_full_diverge). 리스크(정직): U+V 준보존 깨지면 emit=1 포화·½ 상실(U+V drift 첫 게이트) · gain-lock 안 묶이면 ½-tuning 재유입(FORM 회귀·코드강제 필수).
