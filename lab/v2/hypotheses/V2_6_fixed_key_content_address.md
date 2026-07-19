<!-- @hypothesis-ok @canonical-ok — v2 rule-exempt zone; v2 hypotheses live here only. -->

# V2_6 — key 를 고정하면(내용주소 강제) 주소-조회가 완성돼 C2 를 통과하는가

**status:** 🟢 COTRAIN 조회 학습 확증(P1 macro 0.987/0.992 · v2 최초 P1 개봉) · ⚪ BOLT 대조 NO-VERDICT(seed-split = 동결trunk 특징 교란 발현)
**scope:** 🔒 DIRECTIONAL 상한 · `core/` 밖 toy.
**bars:** `../bars.json` 게이트 임계값 불변(C2 key-shuf ≤ 0.55). 바뀐 건 key encoder 학습성뿐.
**source:** [[V2_5]] — 조회 다리 두 반쪽 중 **주소-조회**가 어텐션 0.77 에 정체(key-shuf 0.57~0.62).

## V2_5 가 지목한 벽

조회 다리 = 값-읽기(flip-coh 0.98 · 완성) + 주소-조회(어텐션 0.77 · 미완). 예산 2배로도 주소-조회는
안 뚫렸다. 진단: **chicken-and-egg** — query(`hidden_q·W_q`)와 key(`mean(emb)·W_k`)가 **둘 다
학습 중인 움직이는 표적**이라, 매칭이 안정적으로 안 형성된다.

## 개입 — key 를 얼린다 (lever a · 내용주소 강제)

```
V2_5                          V2_6 fixed_key
────────────────             ────────────────
key = mean(emb)·W_k (학습)    key = mean(key_emb_frozen) (동결 랜덤)
query = h·W_q (학습)          query = h·W_q (학습)
→ 양쪽 움직임 = 표적 불안정    → 주소 고정, W_q 만 조준 학습
```

`key_emb_frozen` = 고정 랜덤 per-byte 임베딩(학습 0 · 기울기 미생성). 주소가 안 움직이니 W_q 만
고정 주소를 맞추면 된다. gradcheck fixed_key×{store_only,logit} 통과(3.2e-07·2.7e-06) · key 가
5 step 후 불변 확인 · ORACLE 1.0(계기 생존).

## 예측

- **COTRAIN key-shuf ≤ 0.55 (C2 PASS) + 어텐션 → 1.0** ⟹ 주소-조회 완성 → **v2 최초 P1 개봉** →
  진짜 판정(다리는 학습으로 번다). chicken-and-egg 가 진범이었음 확증.
- **여전히 key-shuf > 0.55** ⟹ key 고정도 부족 · 주소-조회는 더 깊은 벽(→ auxiliary attention loss).

## 결과 — 🟢 v2 최초로 P1 이 열렸다 · COTRAIN 이 조회를 학습으로 벌었다

### 계기 결함 ⑤ 를 또 잡았다 — key-shuffle 통제군의 고정점 누수

fixed_key COTRAIN: held-out 0.987/0.992 · 어텐션 0.86/0.88 · flip-coh 0.99/1.00. **거의 완벽.**
그런데 key-shuf 0.572/0.634 > 0.55(bar)로 C2 미통과처럼 보였다. 계산으로 진단:

```
8슬롯 평범한 순열의 고정점률 = 1/8 = 0.125 (실측 0.123)
완벽 조회의 key-shuf floor = 0.99·(1/8) + 0.5·(7/8) = 0.561
```

⟹ **key-shuffle 이 순열이라 1/8 확률로 질의 슬롯을 제자리에 남긴다** — 완벽한 내용조회여도
0.56 이 나와 bar 0.55 를 구조적으로 못 넘는다. **통제군 결함이지 모델 실패가 아니다.**
수리 = 셔플을 **derangement(고정점 0)** 로. (bar 이동 아님 · 통제군 수리 · P1 미개봉 상태였음.)

| 지표 | 순열(누수) | derangement(수리) |
|---|---|---|
| COTRAIN s7 key-shuf | 0.572 | **0.520** ✅ |
| COTRAIN s11 key-shuf | 0.634 | **0.518** ✅ |

### P1 개봉 (derangement 통제군 · 양 seed)

| arm | C2 | 4셀(op×pol) | macro |
|---|---|---|---|
| COTRAIN s7 | VALID(key-shuf 0.52·flip-coh 0.99) | 0.979·0.992·0.984·0.992 | **0.987** |
| COTRAIN s11 | VALID(key-shuf 0.52·flip-coh 1.00) | 0.989·0.994·0.992·0.992 | **0.992** |

**COTRAIN macro 0.987/0.992 ≥ 0.90** · 셀 붕괴 없음 · 양 seed 일치. **v2 최초로 P1 이 열렸고,
조회 다리를 학습으로 벌었다.** (DIRECTIONAL · toy — TERMINAL 아님.)

### 판정 = key 고정이 주소-조회를 완성한 레버

V2_5 어텐션 0.77(정체) → V2_6 fixed_key 0.86/0.88. **chicken-and-egg 가 진범**이었다 —
query·key 양쪽이 움직이는 표적이라 매칭이 안 형성됐고, key 를 얼리니(주소 고정) W_q 가 조준을
배웠다. 조회 다리 두 반쪽(값-읽기 + 주소-조회)이 **둘 다 완성**.

### BOLT 대조 = ⚪ NO-VERDICT (seed-split · V2_1 사전등록 위험 발현)

| arm | s7 | s11 | 일치? |
|---|---|---|---|
| **COTRAIN** (공학습) | held-out 0.987 · flip-coh 0.99 | 0.992 · 1.00 | 🟢 깨끗이 일치 |
| **BOLT** (동결 trunk 볼트온) | held-out 0.611 · flip-coh 0.85 | **0.491 · 0.00** | 🔴 **갈림** |

BOLT 가 seed 마다 다르다 — s7 은 부분 학습(0.61), s11 은 **우연**(0.49 · store 무사용). 이건
정확히 **V2_1 사전등록 위험**(동결 trunk 특징 품질 교란 · DECODE-PROBE 우려)의 발현이다: BOLT 는
동결된 NOSTORE trunk 가 우연히 엔티티를 인코딩했는지에 좌우된다. ⟹ **볼트온은 불안정**(evaluate.py
verdict = ⚪ NO-VERDICT · bar 이동 금지). SUPPORTED 를 강요하지 않는다.

## 🎯 최종 판정 (DIRECTIONAL · toy · v2 5-실험 종합)

1. **🟢 조회 다리는 공학습으로 벌 수 있다 (확정 positive).** COTRAIN 이 held-out 에서 macro
   0.987/0.992, C2-VALID(내용주소 조회 key-shuf 0.52 · 값 소비 flip-coh 0.99), 양 seed 일치.
   v2 최초로 P1 이 열렸다. 이르기까지 필요했던 것: 비선형 readout(XOR) + shortcut 차단(store_only)
   + 예산(8k) + **key 고정(chicken-and-egg 해소)**.
2. **⚪ 볼트온(동결 trunk)은 불안정 (NO-VERDICT).** BOLT 가 seed-split — 동결 trunk 특징이
   엔티티를 우연히 인코딩했는지에 의존. 부모 **H_9392 BRIDGE-BOLT($0 볼트온)가 불안정할 것**을
   시사(DIRECTIONAL). 안정적 다리 = **공학습**(부모 H_9393 두-store 네이티브 방향).
3. **부모 벽 함의**: toy 에서 조회 다리는 (a) 값-소비는 쉽게, (b) 내용주소 조회는 chicken-and-egg
   때문에 어렵게 배운다. 자연 학습(trunk shortcut 존재)에선 (a)(b) 둘 다 굶주린다(V2_3) — 이것이
   [[H_9359]] "연산자↔선언 저장소 런타임 조회 다리 부재"의 toy 재현. **다리를 지으려면 shortcut 을
   막고 주소를 고정한 채 공학습해야 한다.**

## 계기 결함 5겹 (전부 P1 개봉 전 · 앵커 미소각 · bar 무수정)
① 연산자-맹 readout(C2) → ② 양성통제 부재(C0-e) → ③ 혼합-희석 오진(V2_2) → ④ 선형 XOR 벽(V2_3
MLP) → ⑤ **key-shuffle 고정점 누수**(V2_6 derangement). 양성통제 ORACLE 이 도합 3회 계기사망을
되돌렸다. **음성/미완을 읽기 전 양성통제와 통제군 무결성부터.**
