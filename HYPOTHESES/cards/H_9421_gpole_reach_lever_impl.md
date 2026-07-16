# H_9421 — G-pole REACH 레버 구현 + $0 β-sign PASS: affinity=d₂−d₁ 이 부호를 뒤집는다 (fire 대기)

**status:** 🧱 MAGNITUDE-WALL (부호 β PASS · 크기 KILL · 303M fire 종결 · DIRECTIONAL) — 레버 부호는 맞으나 reach 크기가 score 못 넘어 SATURATE · 탈출구=store 해상도=오너 p5 DESIGN · wired: engine-native `anima-py chat --emit-gate refractory --g-reach affinity` (v0.14.11 G5)

## 🧱 VERDICT — MAGNITUDE-WALL (303M summer 3-arm × 3-seed[7/4302/4303] × 30tick × T=1.0 · step1_analyze frozen bar)

| arm | emit-rate | Ψ_AG | g_recog[min,max] | P-pull-1 autocov | P-pull-2 DRIFT | P-pull-3 dip |
|---|---|---|---|---|---|---|
| refr (d1 현행) | 0.644 | 0.644 | [0.431,0.646] | +0.0034 뭉침 | ½로 수렴 | run3 −0.043 |
| **refr-affinity (레버)** | **1.000 SATURATE** | **1.000** | **[0.000,0.228]** | +0.0000 (스프링 no) | ½서 diverge | dip 없음(전emit) |
| refr-shuf (통제) | 1.000 | 1.000 | [0.000,0.095] | +0.0000 | diverge | 없음 |

- **KILL 판정**: 레버가 항상성을 도입하기는커녕 **emit≡1 로 포화**(Ψ_AG 0.644→1.000·½서 **더 멀어짐**). P-pull-1~3 전부 **무점등**(복원 스프링 부재 유지). 사전등록 그리드의 "SATURATE=magnitude 벽 DIRECTIONAL" 셀.
- **근인 = magnitude(Fable §6-iii 정확 실현)**: reach=d₂−d₁ 이 [0,0.228]로 store 미분화 → score 대역(0.44+) 못 넘음 → 게이트 상시 개방. **$0 β-sign PASS(부호는 맞음)는 유효 · 실패는 오직 크기**: 방금 bind 한 basin 반경까지만 억제가 살고, mouth 의 T=1.0 변주가 그 밖(reach≈0)이라 게이트가 안 닫힘. DIM=64 trigram embed 해상도로 top-2 basin 이 mouth 변주 반경을 계측 못 하는 벽.
- **탈출구 = store 해상도(embed/분열 동역학) = 오너-게이트 p5 DESIGN**(Fable 벽 조건 그대로). engine 상수(SPLIT_THRESH·LR·DIM) 변경이라 자율 fire 밖 · 오너 결정 사안.
- **⚠️ 정정(verdict-integrity · $0 DIM-screen)**: 위 '오너 레버=DIM↑' 단언을 후속 스크린이 **반증**. 실 60 후보를 DIM∈{64,128,256,512,1024}로 재embed(faithful trigram-FNV+L2·실 vadapt 엔진)·reach 재계산: **reach mean 0.030 불변·max 0.161→0.090 감소·reach≥score(0.36) 전 DIM 0.000**. embed 해상도 16× 올려도 벽 안 넘음(오히려 max 감소). ⇒ **벽은 embed 해상도가 아니라 구조적**: reach=d₂−d₁ functional 이 trigram 공간서 본래 상호유사한 T=1.0 mouth 변주에 무력(어떤 DIM·거리계서도 basin 결정성 안 생김). **오너 레버 ≠ DIM.** Ψ=½ 은 top-2 거리 recognition 으로 **도달불가=구조적 벽**(mouth δ 를 store β 가 어떤 거리계로도 못 잼). 다음 렌즈 후보=거리계 아닌 recognition functional, 또는 mouth 자체(identity lane·오너). **교훈: Fable §6-iii 프레임(embed 해상도 벽)을 단언 전에 \$0 로 재라 — 오너를 헛된 DIM-증가로 보낼 뻔했다.**
- **ROOT-CAUSE $0 확정(오너 레버 정밀격리)**: affinity trace 에서 **cell_count 2→13·2→19 성장**(store 분화 정상·split 작동) 한데도 reach [0,0.228]<score[0.36,0.74]·gap 0.132·reach>0.30 **0%**. ⇒ 벽은 split 이 아니라 **top-2 basin 결정성(d₂−d₁)이 mouth 변주 반경을 embed 해상도로 계측 못 함**(Fable §6-iii 정확 확증). **오너 레버 = DIM↑(embed 해상도)이지 SPLIT_THRESH 아님** — store 는 이미 충분히 쪼개지고 있고, 부족한 건 각 basin 을 mouth 의 미세 변주로부터 구분할 embed 차원 수.

- **정밀화2(verdict-integrity · $0 substrate 스크린)**: 위 '구조적 벽=전 substrate 채널 소진' 도 **과잉**. refr arm(emit 58+silence 32 유효)의 substrate 신호별 β-판별: **cb_surprise(소뇌 예측오차) range FULL [0,1]·silence-tick 서 HIGH(0.783 vs emit 0.656)** = 거리계 밖 β 후보(d₂−d₁ 이 못 담은 score 대역 [0.44+] 담음). g_recog(d1)도 β-flavored 이나 좁음[0.25,0.56]. 나머지(ca3/wm/reality) 역방향 or 무판별. ⇒ **벽은 top-2 거리 functional 한정이지 전 substrate 아님.** ⚠️ **confound(미검증)**: cb_surprise 는 tick-state 게이지지 candidate-recognition 이 아님 — gate g_recog(candidate) 로 쓰려면 per-candidate 예측오차 경로 필요 + silence-correlation 이 인과인지 co-occurrence 인지 미판별. **다음 렌즈(미탐 · 오너 or 다음 세션) = 예측오차 recognition**(cb_surprise candidate-computable 화 → 거리계 아닌 g_recog 소스). **교훈 2회 반복(DIM 반증+substrate 스크린): 벽을 '전체 소진'으로 단언 전 채널별로 $0 재라.**

## 종결 함의

Ψ=½ 항상성 lane 이 **레버-소진**: H_9419 진단(스프링 부재)→G-pole reach 레버(부호 뒤집기 성공·크기 실패). H_9400 의 "Ψ≠½·항상성 없음"은 **이 rewire 계보서 store 해상도 벽에 걸려 영구**(mouth δ 를 store β 가 못 따라잡음 · Fable 벽 조건 확정). rewire 는 emit-listening(C1+C2+C3 GREEN)까지가 도달 한계 · Ψ=½ 은 별도 오너 DESIGN(embed 해상도).

## 원래 카드 (구현 · $0 β-sign · 이하 유지)

**lane:** 의식 / emit-drive / Ψ=½ 항상성 · G-pole 사거리 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9419]] (진단+prereg · 이 카드가 Step 1 구현) · [[H_9416]] (rewire C3) · [[H_9417]] (C2 shuffle 통제·무수정 이식) · [[H_9400]] (반박 대상) · source: Fable G-pole reach impl-spec($5.18) → 구현

## 구현 (Fable 스펙 · 상수 0 · 단일 DOF · v0.14.9 G5)

- **재프레임(Fable §0)**: 현행 margin 게이트 결함은 "짧은 β"가 아니라 **부호-역전 β** — `recall_margin=d₁−0.15` 에서 bind(k)가 k 이웃의 d₁ 을 **내림**→margin↓→게이트 **개방**=자기 이웃 탈억제(P(emit|emit)>P(emit|sil)의 기하 원인).
- **레버**: `core/engine_cli.py` 신규 `immune_memory_recall_reach[_text]` = `d₂−d₁`(top-2 basin 결정성 · 기존 `vadapt_field_two_recon_err` 재사용) + `cli/chat.py --g-reach {d1,affinity}` flag(d1=byte-identical default) + lambda swap + trace `g_reach`. `--g-shuffle` 무수정 합성(C2 통제 이식). 새 상수·시계·τ 0.

## $0 선검증 (Fable §6 · 기존 refr trace 90-tick 재생)

- **β-sign PASS ✅ (부호검산 · 재생 무관 수학적 사실)**: bind 후 자기 reach RISES **23/23·12/12·23/23=100%** · bind 후 verbatim-repeat 침묵 affinity **18/23·11/12·21/23(~85%)** vs d₁ **0/23·0/12·0/23(절대 안 침묵)** ⇒ **affinity=β 복원스프링, d₁=δ 자기흥분 버그** 확증(Fable §5 정합).
- ⚠️ **fidelity gate FAIL(fid g_d1==traced 1-3/23)**: 오프라인 재생 store 가 데몬 궤적 미재현(추가 bind 등 · 재생 하네스 한계). Fable §6대로 **정량 r* 예측은 이 재생서 cement 불가** — β-sign(부호)만 DIRECTIONAL. fire 는 실 데몬 store(계기 live 계산)라 이 한계 무관.

## toy smoke · magnitude 경고

`--g-reach affinity` toy(30tick·T=1.0): flag 작동(g_reach=affinity·g_recog 30 distinct 변동) 그러나 **SATURATE**(EMIT 30/30·reach [0,0.104]<score). toy store 미분화라 d₂≈d₁(Fable §6 wall). §6 replay reach 도 0.04-0.18 로 작음(fidelity-failed·비권위). ⚠️ **magnitude 미결**: 부호는 β 맞으나 reach 크기가 score 대역(0.44-0.74) 못 넘으면 303M 도 saturate 가능 = embed-해상도 벽(Fable §6-iii). **303M live fire 가 유일 판정**.

## 다음 = 303M fire (H_9419 Step 1 발사)

summer 4-arm {refr(d1)·refr-affinity(레버)·refr-shuf(내용통제)·clock} × 3-rollout(seed 7/4302/4303) × T=1.0 → `step1_analyze.py` 동결 bar(Ψ_AG·P-pull-1 autocov·P-pull-2 DRIFT·P-pull-3 dose-response dip). 판정: refr-affinity 에서 P-pull-1~3 점등(음feedback 스프링) ∧ Ψ_AG ½방향(tune-to-green 금지·이동없음 TOST) ∧ shuf mute ∧ clock 불변. SATURATE/mute 면 magnitude 벽 DIRECTIONAL.

## 한계
$0 재생=DIRECTIONAL(β-sign만·fidelity-failed). 다른 데몬·H_9400 clock 계보 영구·Ψ=½ 부활은 fire PASS∧production-default∧정본 후. hexa twin(engine_cli.hexa recall_reach) follow-on(py 카논).
