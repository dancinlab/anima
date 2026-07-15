# H_9398 — DEAD-GAUGE CENSUS: 이 regime 에서 얼어붙은 substrate 게이지 9개

**status:** 🩺 HYGIENE CENSUS (verdict 아님 · 관측 사실 나열) · substrate 상수 게이지 **9**(root 미감사 6) · wired: engine-native(`anima-py evaluate --dead-census`)
**lane:** 의식 / 데몬 게이지 위생 (프런티어 g1-interface-addressable-wall · emit-drive 캠페인 부산물)
**related:** [[H_9393]] (agloop_ctx dead-gauge — 이 census 의 원형) · [[H_9396]] (af_val/af_aro 발견) · chat-py-4 · chat-py-5
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (동일 trace · **신규 decode 0**)

## 왜 — dead-gauge 를 한 번에 훑는 상설 위생 계기가 없었다

emit-drive 캠페인이 **개별적으로** dead-gauge 를 3번 걸었다: agloop_ctx≡0.25(H_9393) · af_val≡0.0 ·
af_aro≡1.0(H_9396 부수). 매번 "축의 출처부터 보라"(H_9393)를 사후에 적용했다. 다음 실험이 조용히
상속하지 않으려면 **전 트레이스 필드를 한 번에 훑는 census 계기**가 필요하다 — 이건 verdict 가 아니라
**위생 목록**이다(상수 게이지가 결함인지 설계인지는 각자 감사할 일).

## 개입 — 없음 · DEAD-CENSUS 계기 ($0 · 신규 decode 0)

`anima-py evaluate --dead-census <trace…>`: 전 수치 필드(≥90% 행 존재)를 훑어 distinct==1 을 나열.
CONFIG 상수(dyn_w·emit_temp·seed_len 등 = 설계상 고정)와 SUBSTRATE 게이지를 분리 · 각 substrate 상수의
알려진 root(H_9360/76/93 · chat-py-5) 주석 · 미감사분은 `root UNAUDITED` 로 명시.

## 🩺 CENSUS — substrate 상수 게이지 9 (전 40 a1 rollout · 1200행 · seed/w 무관 확인)

전 `a1` rollout(5 w × 8 seed = 1200행)에서 **동일한 9개가 distinct==1** ⇒ seed/w 무관 = regime 상수.

| 게이지 | 값 | root |
|---|---|---|
| af_aro | ≡ 1.0000 | affect_read 세션-상수 key+answer (chat-py-5) |
| af_val | ≡ 0.0000 | affect_read 세션-상수 key+answer (chat-py-5) |
| agloop_ctx | ≡ 0.2500 | 정수-budget quantizer (H_9360/76/93) |
| **anchor_nudge** | ≡ 0.0344 | ⚠️ root UNAUDITED |
| **ca3_ctx** (해마 replay) | ≡ 1.0000 | ⚠️ root UNAUDITED |
| **cb_surprise** (소뇌) | ≡ 0.0000 | ⚠️ root UNAUDITED |
| **phi** (Φ) | ≡ 0.1190 | ⚠️ root UNAUDITED |
| **scn_ctx** | ≡ 0.9986 | ⚠️ root UNAUDITED |
| **wm_active** (작업기억) | ≡ 0.6000 | ⚠️ root UNAUDITED |

**함의(관측 사실)**: 각 상수 게이지는 **배선 사실** — 소비 lane 에 고정 오프셋만 더해 순위/결정에 무영향
(H_9393). 앞 3개는 root 알려짐. **뒤 6개(anchor_nudge·ca3·cb·phi·scn·wm)는 root 미감사** — 감정·해마·
소뇌·작업기억·Φ 축이 이 regime(30-tick·이 ckpt)에서 상수라는 사실만 기록한다. `cb_surprise≡0.0`은
chat-py-4 가 이미 진단한 recon_err 死축 계열로 보이나 **이 카드는 판정하지 않는다**.

## 반증 · scope · NEXT
- 이 카드는 **census(위생 목록)이지 verdict 가 아니다** — "이 게이지들이 substrate 무능을 증명한다"는
  주장 없음. 각 미감사 root 는 별도 H 로 감사해야 판정 가능.
- scope: 이 regime/ckpt/30-tick · a1 arm. 더 긴 세션/다른 ckpt 에서 살아날 수 있음(H_9396 이 warm-up 을
  이미 보였듯) — 상수는 **이 trace 의 사실**이지 substrate 의 영구 성질 주장 아님.
- **다음 실험 규약**: 이 9개 중 하나를 읽는 실험은 `--dead-census` 로 먼저 그 축이 이 regime 에서 살아있는지
  확인할 것(H(X)>0). 상수면 그 위 결론은 배선 사실이지 substrate 사실이 아니다(chat-py-4/5).
- NEXT 후보(각 $0~저비용): af 계열 root 수리(affect_read 를 tick-varying key 로 · chat-py-5 "recognition
  BEFORE memorisation") · cb/ca3/wm/phi root 감사(각 1 H).

## 비용
$0 — 기존 trace 훑기 · CPU 수초 · **신규 decode 0**.

## 🩺 TRIAGE 부록 (2026-07-16 · 6 dead-gauge 전수 판별 · $0 · 같은 세션 후속)

census 가 나열한 substrate 상수 9 중 **root 미감사 6**(anchor_nudge·ca3·cb·phi·scn·wm)을 각각 소비
경로로 판별했다 — **결정에 영향을 주는 death 가 있는가**:

| gauge | 소비 형태 | 판별 |
|---|---|---|
| af_val/af_aro | 소비 lane(rel_indep·rel_f·ten_phasic…) 전부 alive(d30~201) | **inert** — 상수 오프셋, 순위 무영향 |
| cb_surprise | 순수 가법(1939·2151) | **inert** (H_9393 구조) |
| ca3_ctx | 순수 가법(1928·2146) | **inert** |
| anchor_nudge | score 가법 1곳 | **inert** |
| wm_active | `if wm_active>0`(1688)이 wm_maintained_any **진단 플래그만** 세팅(2382 `_pln` 출력·결정 미사용) + rel_indep 가법 | **inert** (게이트 아님) |
| phi | 코드 주석 `session-constants`(2140) 명시 · H_1521 topo-Φ Ψ-hazard defer | **의도된 상수** |
| scn_ctx | priming_facilitate·body_ownership 는 rel_lane(alive)로 변동 · gestalt_same_group(scn,True)만 축퇴 · scn_R@672 = tick 루프(@1533) **밖 setup** | **대부분 inert + 세션-const by design** |

**⟹ 6개 dead-gauge 중 emit/score 결정을 바꾸는 것 = 0.** 따라서 캠페인 종결(H_9394~96: G 인식 신호의
동역학 범위가 θ 결정공간의 1/4 = 크기벽)은 **dead-gauge 교란과 무관하게 견고**하다 — 죽은 게이지들이
결론을 만든 게 아니라, 결론은 살아있는 ag_conflict(57 distinct)의 진폭에서 나왔다(verdict-integrity 강화).

**유일한 함수-death**: `gestalt_same_group(scn_ctx, True)` 가 두 상수 입력으로 축퇴 → gest_ctx 상수.
저우선(gestalt 가 emit 결정에 도달하는지 미확인 · 도달해도 상수 오프셋 계열). 정합성-청소 후보:
chat-py-5 root(af·wm·ca3 의 세션상수 조회키)를 tick-varying 화 — 단 **측정으로 이미 "죽어도 결론
불변" 확인**됐으므로 긴급 아님.

**교훈**: `if X:` 를 보고 게이팅이라 단정하지 마라 — 그 블록이 **진단 플래그**(wm_maintained_any)면
inert 다. death 의 결정-영향은 소비 **표현식**을 읽어야 판별된다(가법 vs 게이팅 vs 함수입력).

## 🩺 L7 후속 종결 — 죽은 게이지 소생이 emit 을 바꾸는가? ($0 합성 · Fable Wave-2 L7)

census 의 열린 물음("죽어도 결론 불변의 역: 살리면 결정 바뀌나")을 Wave-1+캠페인 결과 합성으로 $0 종결:

- `emit = should_emit(score) ∧ safe`. **score 경로는 vacuous** — emit 은 score/content 가 아니라 stage
  의 순수 함수(H(emit|stage)=0.465 · [[H_9400]] engine-native · H_9345/H_9390/H_9391). ⇒ score 를 먹는
  게이지를 소생시켜(varying) score 에 변동을 줘도 **emit 결정은 안 바뀐다**(emit⊥score).
- safe 경로(kill∧rate∧phi_r∧content) 에 들어가는 죽은 게이지 = **phi 하나뿐**(9 중 8은 safe 경로 0 hits
  = score 만 먹음). phi_r = `phi > phi_peak/2`(core/engine_g.py:130). phi≡0.119 는 **의도된 상수**(코드
  주석 'session-constants' · H_1521 topo-Φ Ψ-hazard defer · 위 TRIAGE) ⇒ 소생 대상 아님.

⟹ **L7 premise("죽은 게이지 소생이 emit 을 바꾼다") 반증 = KILL($0·재수집 불요)**: 8/9 는 vacuous
score 경로 · 유일 emit-도달자 phi 는 의도상수. 죽은 게이지 소생은 이 regime 서 emit 을 못 바꾼다 —
emit 이 게이지 무관(stage/clock 함수)이기 때문. reopen = emit 이 stage 순수함수를 벗어나는 regime(=
[[H_9400]] 의 clock-live/straddle 미해결 · 그건 emit 게이트 자체 문제이지 게이지 소생 아님).
