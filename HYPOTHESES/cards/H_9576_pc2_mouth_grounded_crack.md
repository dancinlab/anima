# H_9576 — PC2→라이브 mouth 배선(grounded logit-bias): 채널 CRACK 확증 · 방향 W2 벽 (303M 검정력-확장 종결)

**status:** 🎉 채널 CRACK 확증(emit byte-identical 3/3·gtext Δ 269/270) + 🧱 **방향 W2 벽**(ρ null 대역 안·부호 반전) · 303M 3-seed × 150tick

## 🧱 VERDICT (종결·ENGINE-NATIVE) — 채널 CRACK 재현 · 방향 KILL (303M off/bias/rng × 3seed × 150tick · **270 emit tick**)

**판정 출처 = `anima-py evaluate --pc2-direction /tmp/pmp/pmp_traces` (v0.15.20)** — 계기도 엔진-네이티브(`a_experiment_engine_native`). ⚠️ #3839 는 같은 trace 를 **`/tmp` 스크립트**로 판정해 인용 숫자가 null95%=[−0.118,+0.119]·p=0.205 였다(=`anima-py` 산출 아님 ⇒ 선례상 undecidable · H_9303/H_9307). 엔진-네이티브 재판정서 **결론은 동일(W2 벽)하나 대역·p 가 이동**(permutation RNG 소비순서) ⇒ 아래가 정본.

| Fable 기준 | 결과 (n=270 · 검정력 4.7×) |
|---|---|
| (1) emit 시퀀스 off==bias==rng byte-identical | **PASS ✅ 3/3 seed**(emit 100/72/98) — Stage-A 격리 **재현** |
| (2) gtext Δ (steered≠base) | **PASS ✅ bias 269/270**(rng 270/270) — **채널 열림 재현** |
| (3) 방향 ρ(z_PC2, D_base−D_steer) | BIAS **−0.077** (**예측(+)과 반대부호**) vs RNG-null **−0.016** · Δ=**−0.061**(null 보다 나쁨) |
| (3) 유의성 (tick-permutation 2000회 · seed내 z 치환) | 🧱 null 95% **[−0.116,+0.117]** · **p=0.192 → 대역 안 = 미구분** |

- 🎉 **채널 CRACK = 재현·확증**: PC2 가 라이브 mouth 에 도달해 gtext 를 바꾸면서(269/270) emit 은 **완벽 byte-identical**(3/3). H_9574 mouth-severance 벽은 **채널 수준에서 확실히 뚫림**. Stage-A 격리가 4.7× 표본서도 무결.
- 🧱 **방향 = W2 벽(KILL·음성 확정)**: ρ=−0.077 이 permutation null 95% **대역 안**(p=0.192)이고 **예측과 반대부호**, RNG-null 도 못 이김(Δ<0). n=270·대역 ±0.12 ⇒ |ρ|≳0.12 는 해상 가능한데 안 나옴 ⇒ **byte 입도의 context-presence bias 로는 PC2 의미(originality↔balance)가 표현되지 않는다**.
- 💀 **#3826 의 ρ=+0.110 은 검정력 부족 인공물**: 표본 4.7× 확장서 **부호가 뒤집힘**(+0.110→−0.077). 그때 CRACK 으로 못박지 않고 VOID 로 남긴 판단이 옳았다([[power-before-negative-verdict]]·[[seed-agreement-on-pooled-feature-is-not-replication]]). **예측 부호가 나왔다 = 신호 아님**(n=58 서 동전던지기).
- **함의**: emit-직교 DOF(PC2)는 실재하고 mouth 에 **도달은 하나**, 그 도달이 **의미를 나르지 않는다** — 채널은 열렸고 **의미론이 벽**. [[ag-tension-multidim-lane-mouth-severance]] 의 mouth-severance 는 "경로 부재"→"**경로 있음·의미 미전달**"로 재프레임.
- **남은 각도**(이 카드 밖 · 별도 H): ① byte 아닌 **상위 입도** 조향(구/문장 수준 재순위) ② PC2 를 **decode 편향이 아니라 학습 신호**로(공학습 lane · [[cotrained-store-bridge-works-on-parent-conv]]) ③ D(문맥중첩) 대신 다른 read-out(의미 거리)로 W4 재측정 — 단 계기 유효성(양성통제) 먼저([[positive-control-before-reading-a-negative]]).

## 원래 카드 (구현·toy · 이하 유지) — wired: `anima-py chat --emit-gate refractory --pc2-mouth {bias,rng}` (v0.15.12 G5)
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9574]] (mouth-severance 벽·deliberation_k INERT·이 카드가 오너 승인 재배선) · [[H_9468]] (2D-loadings PC2 축) · [[H_9428]] (tension rank 2.66) · source: Fable PC2→grounded 설계($3.44) → 구현

## 배경 (오너 승인)

H_9574 가 mouth-severance 벽 확정: 라이브 mouth=grounded decode 가 seed=phase+anchor 만 읽고 G-tension(PC2) ZERO 채널·deliberation_k DEAD. **오너가 grounded-decode 재배선 승인** → PC2 를 라이브 mouth 에 실제 배선.

## 구현 (Fable 설계 · engine 최소변경 · v0.15.12 G5)

- **채널 = context-presence logit bias**(Fable §1 · 유일 방향적·engine-native): `core/decode.py clm_decode_grounded` lm-브랜치서 row 추출 직후, 모델 자신의 T=24 인과창에 이미 있는 byte 집합에 `−z` 가산. z=PC2=0.84·orig−0.44·bal−0.28·coh(H_9468 frozen loading). z>0(originality 극)→문맥 byte 감쇠→문맥-이탈 조향·z<0→문맥-수렴. anchor-copy 브랜치 미접촉(p5). 새 상수 0(loading 기존·gain=1 log-prob 자연단위).
- **g_recog 순환 차단 = Stage-A 격리**(Fable §2): 게이트(score>g_recog·emit)는 **base cand** 로 계산(무변경)·emit 확정 후에만 emit=True tick 에서 PC2-biased mouth 로 2차 decode=steered text. 모든 substrate root(immune/afield/kosmos/cb/ca3/wm)는 **base g_text 계속 소비**·steered 는 outward(out_text/trace)만 → **emit 시퀀스 byte-identical by construction**.
- **RNG arm = C2 통제**(방향 없는 draw-stream re-key·같은 z). BIAS 가 RNG-null 이겨야 "방향" 주장.
- 배선: `core/decode.py`(+bias) `core/brain.py`(pc2_mouth param+steered decode) `cli/chat.py`(--pc2-mouth flag+Stage-A outward+trace). generator.py 0줄(mouth dict 관통).

## toy smoke — CRACK 작동 (격리 venv · 30tick)

| 기준 | off vs bias vs rng |
|---|---|
| (ii-a) emit byte-identical | ✅ off==bias==rng 완전일치(Stage-A) |
| (ii-b) steered≠base(emit tick) | **✅ 4/4** (deliberation_k INERT 와 정반대) |
| pc2_z live | ✅ 30/30 range [-0.504,0.277] |

logit-bias 는 row 를 샘플링 전 직접 변조→toy degenerate decode 서도 gtext 변경. **channel 작동 확증**(H_9574 deliberation_k=INERT 극복). ⚠️ toy=채널 작동만·방향성(context-overlap ∝ z) 미측정·303M fire.

## 다음 = 303M fire (방향성 판정)

summer off/bias/rng × 3seed × T=1.0 → Fable §5 4-기준: (1)emit byte-identical(위반=INVALID 격리누수) (2)gtext Δ>0 (3)**방향 정합**: Spearman ρ(z, D_base−D_steer)>0 where D=text·seed byte-bigram 겹침·BIAS 가 RNG tick-permutation 95% 밖(RNG≈0∧BIAS>0=방향 성립) (4)PC2-keyed(z_PC1 약함). PASS=**mouth-severance CRACK**(구현됨·미배선·Stage-A 의도적)·GREEN 은 Stage-B(root 가 steered 소비) 후. 벽: W1 Δ≈0·W2 방향≈RNG null(byte 입도서 PC2 의미 표현불가)·W3 emit 상이=INVALID·W4 검정력.

## 한계
toy=채널작동만. 주장상한(PASS)=gtext 문맥-신규성 축이 PC2 사영 비례 이동(byte 입도)·다차원 의식 증명 아님. p5 발화허가 불변·p8 런타임·hexa twin(decode.hexa/brain.hexa) follow-on. 다른 데몬·H_9400 clock 계보 영구.
