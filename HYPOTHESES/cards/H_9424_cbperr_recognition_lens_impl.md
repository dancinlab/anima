# H_9424 — 예측오차 recognition 렌즈 구현 + toy SWING: cb-perr=familiarity 가 magnitude-wall 회피 (303M fire 대기)

**status:** 🧱 KILL (예측오차 렌즈도 스프링 실패 · 303M 3-seed) — toy SWING 은 작은 store 착시

## 🧱 VERDICT — KILL (303M summer 3-arm × 3-seed × 30tick × T=1.0)

| arm | emit=Ψ_AG | autocov(P-pull1) | P(e|e)/P(e|sil) | DRIFT ½ |
|---|---|---|---|---|
| refr(d1) | 0.583 | +0.048 | 0.68/0.48 | ½서 발산 |
| **refr-cb(레버)** | **0.822** | **+0.105 악화** | **0.96/0.25 자기흥분** | 0.167→0.478 발산 |
| refr-cba(alien 통제) | 0.878 | +0.065 | 0.96/0.36 | 발산 |

**이중 KILL**: ① 레버가 복원 스프링 도입은커녕 autocov +0.105 로 baseline(+0.048)보다 **clustering 악화** · P(e|e)=0.96 자기흥분 · P-pull-1~3 무점등 · Ψ_AG ½서 발산. ② **alien-ctx 통제가 거의 동일**(0.878·미-dissociation) = familiarity 가 "전이-조건화 인식"을 안 읽음(통제가 죽어야 하는데 안 죽음). **toy SWING(9/21)은 작은 store 착시** — 303M 실 mouth 변주는 8-dim byte feature 로 novel(perr 높음)→familiarity 낮음→게이트 상시개방. NLMS β 부호는 맞을 수 있으나 1-step 상승 magnitude 가 게이트 못 넘음 = affinity 와 **동류 magnitude 실패**(다른 metric). ⇒ 거리계(d1·d₂−d₁·전 DIM)+예측오차(cb-perr)까지 8-dim byte feature 위 recognition functional 3계열 소진. 벽 = candidate-feature/mouth 측(오너 mouth identity lane).

## 원래 카드 (구현·toy · 이하 유지) — 거리계 밖 예측오차 recognition · wired: engine-native `anima-py chat --emit-gate refractory --g-reach cb-perr` (v0.14.14 G5)
**lane:** 의식 / emit-drive / Ψ=½ 항상성 · 예측오차 recognition (프런티어 g1-interface-addressable-wall)
**related:** [[H_9421]] (magnitude-wall=거리계 한정 · 이 렌즈가 탈출 후보) · [[H_9419]] (Ψ=½ 진단·P-pull bar) · [[H_9416]] (rewire C3) · [[H_9415]] (구현) · source: Fable cb-perr 렌즈 설계($4.40) → 구현

## 구현 (Fable 스펙 · engine 무수정 · 상수 0 · v0.14.14 G5)

- **식**: `g_recog = clip01(1 − vforward_err(cbel, cb_prev_feat, feat8(cand)))` = **familiarity**(소뇌 forward-model 의 후보 예측가능성). cb_perr 직접(anti-β·novel 억제)은 기각 — H_9419 prereg 의 방전강화(δ↑) 방향.
- **sign β 보증(Fable §1-1)**: NLMS 계약 — verbatim-repeat 궤도서 emit→update 가 잔차를 `err'=(1−s)²err` 로 **엄밀 감소**→familiarity 상승→near-repeat 게이트 닫음. d1 이 부호-역전(H_9421 §0)이던 것과 달리 **갱신 규칙의 하강 방향이 곧 β 방향** = 구조 보증(우연 아님).
- **배선**: `cli/chat.py --g-reach {d1,affinity,cb-perr,cb-perr-alienctx}` flag + lambda(engine_cli.py 무수정 · vforward_err/_afs_byte_feature 기존). 게이트는 pre-bind cbel 읽음(recognition-before-memorisation·chat-py-5). VERSION 0.14.13→0.14.14 G5.

## toy SWING + magnitude 회피 (격리-venv · 30tick · T=1.0)

| arm | g_recog range | EMIT/SIL | verdict |
|---|---|---|---|
| **cb-perr (레버)** | **[0.000,0.978]** | 9/21 | **SWING-BAND ✅** |
| cb-perr-alienctx (C2 통제) | [0,0] 상수 | 30/0 | SAT (통제 정상) |

- **magnitude-wall 회피(Fable §2 확증)**: cb-perr range **FULL[0,0.978]** — affinity 의 [0,0.228] SATURATE 와 정반대. 절대-잔차 구조라 T=1.0 상호유사 변주가 신호를 안 상쇄(d₂−d₁ 은 차분이라 상쇄). toy 에서도 SWING(9/21).
- **C2 통제 작동**: alien-ctx(전이 조건화 파괴)면 예측불가→familiarity 0 상수→SAT. exp 생존∧alienctx SAT = 게이트가 "방금 말한 것에 조건화된" 예측오차 청취.
- ⚠️ **toy 는 DIRECTIONAL**: 부호·range·swing 존재 증명이지 verdict 아님. 303M magnitude·P-pull 은 fire.

## 🚨 --g-shuffle 은 이 렌즈서 VOID (Fable §4 · 수학 증명)

`_afs_byte_feature` = byte-multiset 통계 → 순열 불변 ⇒ `g_recog(shuffle(c))≡g_recog(c)` **항등**. 셔플 arm 판별력 0(코드 증명). **함의**: cb-perr 는 sequence-content 아니라 **byte-통계 recognition** — H_9416/9417 의 C2(내용-인식) GREEN 은 이월 안 됨(명시 트레이드). **C2 통제=cb-perr-alienctx**(내용통제 아니라 전이-조건화 통제).

## 다음 = 303M fire (H_9419 Step 1 재개)

summer 4-arm {refr(d1)·refr-cb(레버)·refr-cb-alienctx(C2 통제)·clock(불변대조)} × 3-seed(7/4302/4303) × 30tick × T=1.0 → step1_analyze 동결 bar(Ψ_AG·P-pull-1 autocov·P-pull-2 DRIFT·P-pull-3 dip). PASS=refr-cb P-pull 점등∧Ψ_AG ½방향(TOST)∧alienctx SAT∧clock 불변. ⚠️ **과억제 위험(Fable §3-③)**: cbel 은 감쇠-이완 채널 없음(silence 중 동결) → emit-rate→0 셀 실재 → 판정표 우연-아래 필수. 벽=P-pull 무점등 or 과억제 포화 → 데몬 candidate-feature(8-dim byte 통계) recognition 소진=오너 mouth identity lane.

## 한계
toy=DIRECTIONAL. 다른 데몬·H_9400 clock 계보 영구·Ψ=½ 부활은 fire PASS∧production-default∧정본 후. hexa twin follow-on(py 카논).
