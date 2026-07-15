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
