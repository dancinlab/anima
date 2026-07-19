<!-- @hypothesis-ok @canonical-ok — v2 rule-exempt zone; v2 hypotheses live here only. -->

# V2_4 — trunk shortcut 을 끊으면(store-only) COTRAIN 이 조회를 배우는가

**status:** 🟢 SHORTCUT COLLAPSE 확증 (COTRAIN flip-coh 0.00→0.79/0.93) · 단 키조회 미완(key-shuf 0.61) · C2 미통과·P1 미계산
**scope:** 🔒 DIRECTIONAL 상한 · `core/` 밖 toy.
**bars:** `../bars.json` (동결 · 불변). 바뀐 건 답-위치 경로뿐.
**source:** [[V2_3]] — 계기 생존(ORACLE 1.0) 하에서 COTRAIN flip-coh 0.000 = shortcut collapse 가설.

## V2_3 가 물려준 것

계기가 살았는데도 COTRAIN 은 store 를 안 썼다(flip-coh 0.000). 가설: **trunk 를 함께 학습하면
trunk 가 답-위치를 지배**해 조회 경로에 경사가 안 남는다(shortcut collapse). BOLT(trunk 동결)가
오히려 store 를 더 쓴 것(0.783)이 방증.

## 개입 — 답 첫 바이트를 store 만 만들게 (`gate=store_only`)

```
V2_3 logit                        V2_4 store_only
────────────────                  ────────────────
comb = trunk_logit + λ·store       comb = λ·store   (답 위치서 trunk logit 제거)
= trunk 우회로 존재                 = bridge 가 유일 출구 → 조회 안 배우면 loss 정체
```

backward 에서 답-위치 trunk 기울기 = 0(우회로 차단). 나머지 위치·다른 답 바이트는 trunk 그대로.
gradcheck store_only+mlp 통과(7.6e-07). **store_only ORACLE = 1.0** 확인(계기 생존).

## 예측

- **COTRAIN flip-coh 크게 상승 + C2 통과 + 높은 held-out** ⟹ shortcut collapse 확증 ·
  다리는 학습으로 벌 수 있다(우회로만 막으면). = V2_1 대립예측 (A) 쪽 첫 positive(DIRECTIONAL).
- **여전히 flip-coh 낮음/우연** ⟹ shortcut 이 진범 아님 · 조회 학습 자체가 어렵다(chicken-and-egg:
  hidden_q 가 엔티티 안 담으면 W_q 못 배우고, W_q 경사 없으면 hidden_q 가 엔티티 안 담음).

C0-e ORACLE ≥ 0.90 통과 하에서만 P1 을 읽는다. 판정표·통제군 = [[V2_3]] 와 동일.

## 결과 — 🟢 shortcut 을 끊자 COTRAIN 이 조회를 배웠다 (방향 반전)

계기 생존(ORACLE 1.0/1.0) 하에서:

| arm | store flip-coherence | V2_3(logit) 대비 |
|---|---|---|
| **COTRAIN** (조회 학습) | **0.794 / 0.926** | 0.000 → **급등** 🟢 |
| BOLT (trunk 동결) | 0.000 / 0.000 | 0.783 → **소멸** (반전) |
| SLOWROT | 0.000 / 0.006 | — |

**shortcut collapse 가설 확증**: 답-위치 trunk 우회로를 끊자(store_only) COTRAIN 이 store 를
**쓰기 시작**했다(flip-coh 0.79~0.93). V2_3 에서 trunk 가 답을 흡수해 굶겼던 조회 경로가 살아났다.
BOLT 는 반대로 죽었다 — trunk 동결 + answer store-only 면 bridge 가 학습 신호를 못 받는다.

## 그런데 아직 C2 미통과 — 조회의 절반만 배웠다

COTRAIN key-shuf = **0.613/0.617 > 0.55** (bar). flip-coh 는 높은데 키를 섞어도 안 무너진다 ⟹
**store 값(극성)은 읽되, 키 조회(주소)는 슬롯 순서에 과적합.** 진짜 내용주소 조회가 아니라
"질의 엔티티가 대체로 그 슬롯에 있다"는 위치 지름길. 조회 다리의 **읽기 절반(값)만 배우고 주소
절반은 미완.** + COTRAIN loss 0.139 는 3600 step 까지 정체 후 막 하강 = **예산 부족** 신호도 겸함.

## 🎯 발견 (DIRECTIONAL · toy · cement 아님)

1. **다리는 학습으로 벌 수 있다 — 단 우회로를 막았을 때만.** V2_1 대립예측 (A)("인터페이스 문제")
   쪽 첫 positive 신호. 자연 학습(shortcut 존재)에선 trunk 가 조회를 굶긴다 = 부모 H_9359
   "담체-기입이 동결 캐시"의 가능한 toy 미러(trunk shortcut = 캐시, 조회 = 미형성 다리).
2. **조회는 두 반쪽** — 값 읽기(배웠다 · flip-coh↑)와 주소 조회(미완 · key-shuf↑)가 분리 학습.
3. C2 미통과라 P1 은 여전히 미계산. **"COTRAIN 이 조회를 배웠다"는 방향 관찰이지 판정 아님.**

## NEXT — V2_5 후보 (키 조회 강제)

주소 과적합을 깨서 C2(key-shuf ≤ 0.55) 통과 겨냥:
(a) **예산 2배**(8000 step · loss 아직 하강 중) · (b) 슬롯 위치 **셔플**을 학습에도 도입
(질의 엔티티 슬롯을 매 예제 랜덤화 → 위치 지름길 원천 차단) · (c) key 고정(내용주소 강제).
(b) 가 가장 직접적 — 위치 정보를 학습에서 없애면 키 조회가 유일 경로가 된다.
