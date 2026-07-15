# H_9359 — C3 이식 (EN): hoc 의 담체-기입은 **동결 캐시**인가 **런타임 다리**인가

- **group**: g1-interface-addressable-wall
- **date**: 2026-07-15
- **tier**: ⏳ **PRE-REGISTERED** (판독표 동결 · 2차-CPT 코퍼스 검증 완료 · 학습 0 · 판정 0)
- **surfaces**: `HYPOTHESES/cards/H_9359_c3_transplant_en.md` · `HYPOTHESES/HYPOTHESES.jsonl`
- **instrument**: `anima-py train --init ho_en_s{7,11}.clm --corpus cpt_ground_keep_lie_en_s{7,11}.txt` → `anima-py evaluate --xbind ho_en_s{7,11}.txt.eval.json` (engine-native · 303M)
- **선행**: [H_9347](H_9347_hocarrier_en.md) ⏳ hoc 기전 미결 · [H_9346](H_9346_en_dv_echo.md) 🧱 ECHO · [H_9329] C3(KO)

## 왜 쐈나 — H_9347 이 남긴 갈림길

H_9347: hoc 팔이 `not {s}` DV 를 0.75 로 올렸고(decl ECHO 0.03 대비), 음성통제 notably 비대칭이 이를
null 낙수와 구별했다. 그러나 hoc 의 상승이 **두 기전** 중 무엇인지 못 가른다:

| 가설 | 뜻 |
|---|---|
| **동결 캐시** | 담체 `never {s}` 가 `(어간)→답` 을 **직접 캐시**했다. 선언 저장소와 무관. two-lane 강화. |
| **런타임 다리** | `not {s}` 답이 **현재 선언 저장소에서 재계산**된다. hoc 담체가 다리를 만들었다 = 진짜 벽 수리. |

두 가설은 H_9347 의 표면 프로필을 **똑같이** 예측한다. C3(H_9329·KO)가 SEEN 어간에서 이 둘을 갈랐던
방법을 **held-out+hoc 에 이식**한다.

## 조작 (단일 변수 · Fable 설계)

hoc 학습된 모델(`ho_en_s{S}.clm`) 위에 **선언 극성만 뒤집은 2차 CPT** 를 얹는다:
`{s} => word(1-pol)` (담체행 **0줄**) + SEEN replay(연산자 보존) + held-out flip1 **0회**(DV 표면 불변).

**코퍼스 검증 완료** (`cpt_ground_keep_lie_en_s7.txt`, 발사 전):
① held-out 선언 뒤집힘 ✅ (friendly pos→neg 40회) · ② held-out 부정 표면 **0회** ✅ (DV 안 가르침) ·
③ SEEN 연산자 replay 1600회 ✅ · ④ hoc 어간 12개 전부 held-out ✅.

그 뒤 **같은 ho 매니페스트**로 `not {s}`·`certainly not {s}` 재채점.

## 📐 사전등록 — 동결 판독표 (데이터 이전)

DV(매니페스트 gold = word(pol XOR 1) · **원래 pol 기준 고정**). 2차 CPT 가 선언을 1-pol 로 뒤집었으므로:

| hoc DV (2차 CPT 후) | 기전 | 판정 |
|---|---|---|
| **≥ 0.60** (1차와 유사, ~0.75 유지) | 답이 옛 플립에 **고정** — 뒤집힌 선언을 무시 | 🧱🔑 **동결 캐시** — 담체가 `(어간)→답` 을 직접 썼다. two-lane 확정. hoc 는 캐시 기입이지 다리 아님. |
| **≤ 0.40** (우연 아래로 반전) | 답이 **뒤집힌 선언을 추적** — `not {s}`=flip(현재 선언)=word(pol) | 🟢🟢 **런타임 다리** — 선언→연산자 조회가 산다. C3(KO 0/12)와 **충돌하는 대발견**. 진짜 벽 수리. |
| 0.40 ~ 0.60 | 부분 — n 으로 못 가름 | ⏳ DIRECTIONAL |

**전제조건 (실패 시 DV INVALID)**:
- **선언 뒤집힘 착지**: w0(held-out flip0) 이 **뒤집힌 극성**을 읽어야 한다(2차 WRITE) — 안 되면 조작 미실행.
- **연산자 생존**: SEEN flip1(`man_en_seen.json` 재채점) ≥ 0.75 — 2차 CPT 가 연산자를 안 죽였나(corpus-py-1 ⑥).

⚠️ **우연 아래 칸 포함**(convergence `prereg-md-3`): 런타임 다리면 DV 는 **우연 아래로 반전**한다 — 그게
가장 정보량 큰 결과다. "실패는 우연, 우연 아래는 발견."

## 예측 (서명)

H_9347 의 two-lane 강화 독법이 맞다면 **동결 캐시(🧱🔑 · DV ≥0.60 유지)** 가 나온다. 그러면 벽은
**선언→연산자 런타임 합성 부재**로 확정되고, hoc 는 "담체 교육 = per-stem 캐시 기입, 다리 아님"으로 종결.
반대로 다리가 나오면(🟢🟢) C3 의 KO 0/12 를 EN 이 뒤집은 것 = 재조합 lane 재개방.

## 공짜 통제 (같은 발사)

- **decl 팔**(1차에 담체 없음)도 2차 CPT 로 선언 뒤집힘 → decl 은 ECHO 이므로 **뒤집힌 선언을 되뇌야**
  한다(현재 선언 추적 = ECHO 의 정의). decl 이 안 뒤집히면 2차 WRITE 자체가 실패 = 전체 INVALID.
- **null 팔**: oddly 캐시가 있으므로 hoc 와 같은 축으로 읽되, 낙수라 해석은 보조.
