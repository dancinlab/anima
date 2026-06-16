# H_1359 — 🇰🇷 ko-dedup-novel: NOVEL-ONLY / DE-DUP held-out 에서 JM interpolation 이 jamo 2.51335 floor 를 여전히 이기는가?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1359_ko_dedup_novel` · **Tier:** 🧱 FLOOR-CONFIRM (depletion, valid c9) — JM 이 truly-novel context 에서는 floor 를 **못 이긴다** → 2.51335 는 진짜 표상/데이터-풍부도 floor 로 **확정**, H_1344 의 JM-GREEN 은 **반복 암기 artifact**, "interpolation beats jamo" lane **DEPLETED**.

DIRECTIONAL numpy · REAL R2 KO 코퍼스 sha `c47b6808…` (== H_1316/H_1344, byte-fair) · $0 CPU (16.4s) · frozen-first (FREEZE 가 scoring 전에 작성) · λ = H_1344 와 **동일 FROZEN** (재튜닝 안 함, anti-Goodhart) · c9/p7 NO tune-to-green · live CORE UNTOUCHED.

## Claim (falsifiable, depletion test)
H_1344 🟢: non-fragmenting frozen-λ Jelinek-Mercer (JM) interpolation 이 held-out 한국어 next-symbol CE 를 **2.00562** 로 내려 jamo **2.51335 floor 아래로** 갔다. 그러나 H_1344 honesty 진단이 그 이득은 **반복 암기**임을 보였다 — held-out 의 70.1%가 TRAIN-SEEN top-order context 재사용(CE|seen=1.6474), 진짜 novel 30%는 CE|novel=**2.8819**(floor 보다 나쁨). H_1359 = H_1344 카드가 NEXT-1 으로 지목한 depletion 질문: **NOVEL-CONTEXT-ONLY held-out (TEST A, primary)** 과 **DE-DUP 코퍼스 (TEST B)** 에서 JM 이 2.51335 를 **여전히** 이기는가?
- YES → floor 가 truly-novel context 에서도 깨짐 = 진짜 표상 돌파 (loudly 보고).
- NO (H_1344 CE|novel=2.88 이 이미 가리킴) → 2.51335 는 진짜 표상/데이터-풍부도 floor 로 **확정**, H_1344 JM-GREEN 은 암기 artifact → lane **DEPLETED** (honest 🧱, valid c9).

## Method (frozen-first; λ FIXED == H_1344, scoring 전 FREEZE 작성)
- **REAL Korean only**: `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` trim → sha256 ASSERTED `c47b6808…`(== H_1307 RUN A / H_1316 / H_1344; 29,999,999 bytes; 캐시는 sha 일치 시만 재사용, mismatch → STOP, NO synthetic). R2 키 keychain env-only(c7).
- **Representation/JM (H_1344 와 동일)**: Hangul→NFD jamo(id 256+rank), non-Hangul→raw byte; n_bytes 합산=원본 UTF-8 byte; Vj=323. p_JM(s|h)=Σ_{k=1..5} λ_k·p̂_k(s|직전 k−1 jamo), p̂_1 Laplace(1.0), k≥2 TRAIN order-k count-MLE, unseen→recursive back-off, count 는 FULL TRAIN(fragment 없음). λ=[1,2,4,8,16]/31 — **H_1344 와 동일, 재튜닝 X**.
- **TEST A — NOVEL-ONLY (PRIMARY GATE)**: stride=300 even=TRAIN/odd=TEST + FULL-resolution adjacency(H_1344 동일)로 JM 학습. TEST 위치 중 **top-order(4-jamo) context 가 TRAIN top-order set 에 없는** 위치만 점수 → genuine-generalization 슬라이스를 게이트로 만듦.
- **TEST B — DE-DUP 코퍼스**: 스트림을 walk 하며 각 위치의 **top-order n-gram STRING(5-gram=4-jamo context+label)** 이 이미 등장했으면 그 위치를 eligible 에서 DROP(causal — prior occurrence 만으로 식별, TEST 누출 없음). 생존 위치 위에서 stride-300 even/odd 재분할 → JM 재학습 → 점수.

## Frozen bars (FREEZE verbatim, 사후 이동 없음)
| bar | test | result | pass |
|-----|------|--------|------|
| **c1 PRESENCE-or-FLOOR** (TEST A primary) | CE_A < 2.50335 → 🟢 break; ≥ → 🧱 | CE_A=**2.88190** (Δfloor **+0.36855**) | ❌ (floor 못 이김, → 🧱) |
| **c1b DE-DUP 일치** (TEST B) | CE_B vs 2.51335 delta+sign | CE_B=**4.71364** (Δfloor **+2.20029**) | floor 와 같은 방향(못 이김) ✅ |
| **c2 EARNED** (anti-Goodhart) | shift surrogate 가 반대로 가야: CE_A_shift≥2.46335 ∧ shift−novel≥0.05 | CE_A_shift=**5.81040** (shift−novel **+2.9285**) | ✅ (conditioning 파괴→나빠짐) |
| **c3 FLOOR-CONFIRM** | ¬c1 ∧ c1b 일치 ∧ c2 → honest 🧱 | 충족 | → **🧱 FLOOR-CONFIRM** |

→ **🧱 FLOOR-CONFIRM** (c1 거짓 ∧ c1b 일치 ∧ c2 earned). FREEZE 의 c3 사전등록 분기 — tune-to-green 아님.

## Results
| arm / diagnostic | CE (nats/UTF-8-byte) | Δ vs 2.51335 floor | note |
|---|---|---|---|
| raw-byte ceiling (ref) | 2.95342 | — | H_1316 G0 |
| **jamo floor (locked)** | **2.51335** | 0 | H_1316 mitosis, depletion test 대상 |
| H_1344 GATE 복제 (full TEST) | 2.00562 | −0.50773 | H_1344 GREEN 재현(seen+novel 혼합) |
| ↳ seen-context 슬라이스 (70.1%) | 1.64740 | −0.86595 | **암기** 슬라이스 |
| **TEST A: novel-only (12,706 위치, 29.9%)** | **2.88190** | **+0.36855** | **floor 못 이김 — c1 ❌** |
| TEST A: shift surrogate (novel) | 5.81040 | +3.29705 | conditioning 파괴 → 나빠짐 (c2 ✅) |
| **TEST B: DE-DUP 코퍼스 (6.8% kept, test 98.5% still-novel)** | **4.71364** | **+2.20029** | **floor 못 이김 — c1b 일치 ✅** |
| TEST B: shift surrogate | 6.37434 | +3.86099 | (참조) |

핵심: novel-only CE_A=2.8819 는 H_1344 의 CE|novel 과 **정확히 일치**(슬라이스 격리가 올바름을 확인). de-dup 은 반복 문자열 제거 후 위치의 6.8%만 남고 TEST 의 98.5%가 여전히 novel → JM 이 floor 보다 한참 위(4.71). 두 독립 경로(novel-filter · corpus de-dup) 모두 같은 결론.

## ⚠ HONEST SCOPE — 무엇이 확정되고 무엇이 아닌가 (c9)
- **확정**: JM interpolation 이 jamo floor 를 이긴 H_1344 GREEN 은 **코퍼스 반복 문자열 암기**다. 반복을 제거(novel-only / de-dup)하면 JM 은 floor 를 **못 이긴다**(2.88·4.71 ≫ 2.513). 따라서 2.51335 는 (이 코퍼스 윈도·이 표상에서) **진짜 표상/데이터-풍부도 floor** — non-fragmenting interpolation 으로도 깨지지 않는다. "interpolation beats jamo" lane은 **DEPLETED**.
- **c2 가 살아있음**: shift surrogate 가 novel 에서 더 나빠짐(+2.93) → 남은 (작은) 조건화 신호조차 진짜 jamo-순서 구조에서 옴(랜덤 artifact 아님). 즉 floor 는 "JM 이 아무것도 못 배운다"가 아니라 "novel context 에서 count-MLE 가 줄 수 있는 것이 floor 위에서 끝난다".
- **확정 아님**: DIRECTIONAL numpy, toy stride-300 byte-substrate next-symbol CE(fluent decoder 아님, 한국어 유창성 주장 없음). 단일 코퍼스 윈도·단일 frozen λ·단일 stride. de-dup 은 top-order STRING causal de-dup(의미 de-dup 아님). 더 큰 데이터/다른 표상(sub-jamo featural 은 H_1322 🧱)/엔진-transfer 는 UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).

## 결론 / next angle
**2.51335 jamo floor 는 진짜 representation floor 로 확정** — non-fragmenting frozen-λ JM interpolation 도 truly-novel context 에서는 못 이긴다(novel-only +0.369 / de-dup +2.200 vs floor). H_1344 의 🟢 는 메커니즘 차이(반복 저장 능력)를 드러냈을 뿐 표상 floor 를 깨지 않았다. "interpolation beats jamo" lane DEPLETED.
- **NEXT-1**: floor 를 깨려면 더 풍부한 데이터(반복 아닌 신규 문자열량 증가)거나 jamo 아래/옆의 다른 표상축이 필요 — H_1322 featural 은 이미 🧱(dense 30MB 에서 opaque count-MLE 가 정보-최적). 즉 이 윈도에서 표상 lever 는 소진 방향. data-richness lever(더 큰 윈도)에서 novel-context CE 가 내려가는지가 남은 진짜 질문(a_scale_honest_scope ladder).
- **NEXT-2**: engine-native — 이 floor-confirm 은 H_1321 VAdaptField 가 가변-차수 back-off 를 표현하도록 확장해도 표상 floor 자체는 안 바뀜을 시사(메커니즘이 아니라 표상/데이터가 bound). a_engine_native_learning follow-on.

## Pointers
- 카드: `UNIVERSE/cards/H_1359_ko_dedup_novel.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1359)
- 코드: `state/ko-dedup-novel/h1359_ko_dedup_novel.py`
- 증거: `.verdicts/1359_ko_dedup_novel/{H_1359_FREEZE.txt, result.txt, H_1359.txt}`
- CLAIMS: `CLAIMS.tape` @C h1359_ko_dedup_novel
- xref: h1344(JM GREEN=암기, 이 카드가 depletion)·h1316(jamo floor)·h1321(jamo wire)·h1322(featural 🧱)·h1345(data-starved convergent)·a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c9·c15
