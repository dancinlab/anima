<!-- @hypothesis-ok @canonical-ok — v2 rule-exempt zone; v2 hypotheses live here only.
     Owner: "v2 가설도 v2 안에서만 생성". See ../CLAUDE.md. -->

# V2_3 — 비선형 readout 으로 계기를 살린 뒤: 조회 다리는 학습으로만 버는가

**status:** 🟡 계기 생존(ORACLE 1.0) · C2 가 전 arm INVALID · **조회 다리 미학습이 진짜 결과** · P1 미계산
**scope:** 🔒 **DIRECTIONAL 상한** — `core/` 밖 toy. TERMINAL 아님.
**bars:** `../bars.json` (게이트 상수 동결 · V2_1 부터 불변). 바뀐 건 readout 아키텍처뿐.
**source:** [[V2_2]] 가 밝힌 근본원인(선형 readout × XOR 과제 → ORACLE 0.75 상한).

## V2_2 가 물려준 것 = 계기 수리 지점

과제 = `answer = polarity XOR operator`. 선형 `W_out·concat(v, hidden_q)` 은 곱항을 못 만들어
조회를 공짜로 줘도(ORACLE) 상한 0.756. **혼합도 logit 도 이 벽의 하류였다.**

## 개입 — 비선형 1층 readout

```
V2_1/V2_2 (죽음)              V2_3
─────────────────            ─────────────────
W_out · concat               W_out · GELU(W_h · concat)
= 선형 → XOR 불가             = 2층 MLP → v×hidden_q 상호작용 표현 가능
```

`--readout mlp` 플래그(cfg["readout"]). gradcheck **두 gate × mlp** 통과(mix 6e-06 · logit 1.8e-05 ·
W_h 오염 검출). gate 는 logit 유지(V2_2 의 희석-무관 확인 후 더 깨끗한 경로).

## 🟢 계기 생존 확인 (C0-e · P1 개봉 전제)

**MLP-readout ORACLE seed7 = 1.000** (loss 0.0001). 조회를 공짜로 주면 과제를 완벽히 푼다 →
**계기가 처음으로 살았다.** V2_1(0.74)·V2_2(0.49) 는 계기 사망이었고, 이제 C0-e ≥ 0.90 을
통과하므로 COTRAIN/BOLT 를 **읽을 자격**이 생긴다.

## 이제 읽는 진짜 질문 (V2_1 의 원래 물음)

C0-e PASS 하 · 양 seed 일치 · bars.json 동결:
| 결과 | 판정 |
|---|---|
| COTRAIN ≥ 0.90 ∧ BOLT ≤ 0.60 | 🟢 SUPPORTED — 다리는 **학습으로** 번다(부모 두-store 재설계 정당화) |
| COTRAIN ≥ 0.90 ∧ BOLT ≥ 0.90 | 🔵 BOLT-SUFFICIENT — 볼트온 충분, 부모 H_9392 발사 청신호 |
| COTRAIN ≤ 0.60 | 🔴 가설 사망 |
| 0.60–0.90 | ⚪ NO-VERDICT (모호역 · bar 재조정 금지) |

- `COTRAIN` = trunk+bridge 동시학습 · 예제마다 rotation (조회를 **학습**)
- `BOLT` = NOSTORE trunk 동결 + bridge 만 사후학습 (= 부모 H_9392 BRIDGE-BOLT)
- 셀별 분해 먼저 · 통제군(키-셔플·중립·λ=0·오답 store) C2 · SLOWROT 로 rotation 격리.

## 결과 — 🟡 계기는 살았고, 조회 다리는 안 배웠다 (진짜 결과 · P1 미계산)

전체 게이트(2 seed × 5 arm · logit+mlp):

| 게이트 | 실측 |
|---|---|
| C0-e ORACLE | **1.000 / 1.000** ✅ — 계기 생존(조회 공짜면 완벽) |
| C0-a/b/c | PASS (누수0 · NOSTORE 0.49/0.51 · 결정성) |
| C1 검정력 | PASS (MDE 0.031) |
| **C2 COTRAIN** | flip-coh **0.000** · key-shuf=neutral=λ0=0.491 → **INVALID** |
| C2 SLOWROT | flip-coh 0.004/0.006 → INVALID |
| C2 BOLT | flip-coh 0.783/0.236 · key-shuf 0.608>0.55 → INVALID |

**계기가 살아있는데(ORACLE 1.0) COTRAIN 의 store flip-coherence = 0.000.** 조회를 **학습**시키면
store 를 아예 안 쓴다 = **조회 다리를 못 만든다.** C2 가 전 arm INVALID → P1 미계산.

## 🎯 진짜 발견 — 예상과 반대 방향

| arm | store flip-coherence (store 뒤집을 때 답 변화) |
|---|---|
| COTRAIN (조회 학습) | **0.000** — 다리 전무 |
| BOLT (trunk 동결·bridge 사후학습) | **0.783 / 0.236** — 부분적으로 store 반응 |

**BOLT 가 COTRAIN 보다 store 를 더 쓴다.** 이건 V2_1 가설의 대립예측 (B)("학습으로만 번다,
볼트온은 실패")와 **반대**다. 해석(DIRECTIONAL · toy):
- trunk 를 함께 학습시키면(COTRAIN) trunk 가 **자기 우연 분포로 답을 다 흡수**해버려 조회 경로에
  경사가 안 남는다(logit-add 라도 trunk logit 이 답 위치를 지배). = **shortcut collapse.**
- trunk 를 동결하면(BOLT) trunk 가 답을 못 만들어 bridge 가 유일한 출구 → 조회를 **일부** 배운다.
- 단 BOLT 도 C2 통과 못 함(key-shuf 0.608 = 키를 진짜로 안 씀, 슬롯 순서에 과적합).

⚠️ **이 방향성을 cement 하지 마라** — C2 가 전 arm INVALID 라 **어느 것도 유효 측정이 아니다**.
"BOLT>COTRAIN" 은 flip-coherence 원시값의 관찰이지 판정이 아니다(FORM tunable · BIND earned).

## 🎯 계기가 이 세션에서 가르친 것 (v2 5-실험 누적)

1. 계기 결함을 **4겹** 벗겼다(연산자-맹 readout → 양성통제 부재 → 혼합-희석 오진 → 선형 XOR 벽) ·
   전부 **P1 개봉 전** C0/C2 가 잡음(앵커 미소각 · bar 무수정 · 4번 재설계).
2. 계기를 살리고 나서야(ORACLE 1.0) 진짜 질문이 드러났다: **trunk 공학습이 조회 경로를 굶긴다**
   (shortcut collapse) — 이건 부모 벽의 toy 미러일 수 있다(H_9359: 담체-기입이 동결 캐시).
3. **양성통제(ORACLE)가 세 번 구했다** — 매번 '개선'으로 박고 넘어갈 뻔한 걸 계기 사망으로 되돌림.

## NEXT — V2_4 후보 (조회 경로 굶주림 정면)

trunk 의 답-위치 shortcut 을 막아 bridge 에 경사를 강제:
(a) 답 위치에서 trunk logit **detach**(store 만 답을 만들게) · (b) auxiliary loss 로 조회
attention 을 정답 슬롯에 지도 · (c) key 를 학습 대신 고정(내용주소). C2 통과가 P1 의 전제.
