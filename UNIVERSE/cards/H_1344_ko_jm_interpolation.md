# H_1344 — 🇰🇷 ko-jm-interpolation: NON-FRAGMENTING frozen-λ Jelinek-Mercer interpolation 이 jamo 2.51335 floor 아래로 내려가는가?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1344_ko_jm_interpolation` · **Tier:** 🟢 GREEN (frozen bar 통과) — 단, GREEN 의 이득은 **코퍼스 반복 암기**이지 더 깊은 합성적 진전이 아님 (honest scope 필수, c9)

DIRECTIONAL numpy · REAL R2 KO 코퍼스 sha `c47b6808…` (== H_1316 jamo baseline, byte-fair) · $0 CPU · frozen-first (FREEZE 가 scoring 전에 작성, λ FIXED) · c9/p7 NO tune-to-green · live CORE UNTOUCHED.

## Claim (falsifiable)
한국어 byte-LM floor 는 REPRESENTATION-bound 임이 밝혀졌다: raw-byte 2.95342 → NFD jamo 분해 2.51335 nat/UTF-8-byte (H_1316 🟢, wired H_1321). jamo 아래 분해(H_1322 featural)는 🧱(data-richness 한계, dense 30MB 에서 opaque count-MLE 가 정보-최적). 그러나 2.51335 floor 는 **고정용량 gradient-free Voronoi MITOSIS** 가 3-D 컨텍스트(직전 2 심볼) 위에서 도달한 값이다 — 이 메커니즘이 한 번도 묻지 않은 진짜 *언어모델링* 질문: **count-fragmentation 없는 frozen-λ Jelinek-Mercer interpolation 이 jamo n-gram 차수(1..N)를 섞으면** held-out 한국어에서 2.51335 아래로 내려가는가, 아니면 floor 를 재확인하는가?

WHY NOT MITOSIS: GROW_MAX cell 의 단일 Voronoi 분할은 고정 저차원 feature 에만 조건화할 수 있고, 희소한 고차 jamo 컨텍스트에서 밀집한 저차로 부드럽게 back-off 할 수 없다. Jelinek-Mercer interpolation 이 그 고전적 NON-FRAGMENTING 해법: 모든 차수의 count-MLE 를 FULL TRAIN 스트림에서 계산(cell 간 fragment 없음)하고 FROZEN λ 로 섞는다.

## Method (frozen-first; λ 는 scoring 전에 FIXED — 이것이 anti-Goodhart 의 핵심)
- **REAL Korean only**: `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` trim → sha256 ASSERTED `c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca` (== H_1307 RUN A / H_1316 jamo baseline, 29,999,999 bytes; mismatch → STOP, NO synthetic). R2 키는 keychain(`secret get r2.phanes.*`)에서 env-only fetch, 로그/커밋 안 됨(c7).
- **Representation (H_1316 과 동일, byte-fair axis)**: Hangul syllable → NFD jamo 심볼(id 256+rank), non-Hangul → raw byte(0..255); 심볼당 n_bytes 가 원본 UTF-8 byte 로 합산(3-jamo→[1,1,1], 2→[2,1], 1→[3]). CE axis = Σ(−log p)/Σ(n_bytes) on held-out — **2.51335 floor 와 동일한 nats/UTF-8-byte 축**. Vj=323 (67 distinct jamo).
- **Held-out split (H_1316 과 동일 구성)**: label 위치 idx 를 stride=300 decimate 후 even=TRAIN / odd=TEST. **결정적 수정**: 각 위치의 n-gram history 는 decimated 스트림이 아니라 **FULL-RESOLUTION 인접 jamo**(직전 N−1 심볼; H_1316 의 last/second-sym adjacency 와 동일). (초기 버그: 스트림을 먼저 decimate 후 n-gram 을 만들어 인접성을 파괴 → CE 4.34 의 거짓 🧱; 수정 후 정상.)
- **JM-interp (NON-FRAGMENTING)**: p_JM(s|h) = Σ_{k=1..N} λ_k·p̂_k(s | 직전 k−1 jamo); p̂_1 = Laplace(=1.0) unigram(zero 없음), k≥2 는 TRAIN order-k count-MLE, 컨텍스트 unseen 시 recursive back-off. count 는 FULL TRAIN 인접성에서(fragment 없음).
- **FROZEN λ (FREEZE 에 사전등록, TEST 로 튜닝 안 함)**: N=5, w_k=2^(k−1)→ λ=[1,2,4,8,16]/31 ≈ [0.032,0.065,0.129,0.258,0.516].
- **Arms**: A1 JM-interp(intact) · A0 unigram-only(λ=[1,0,..], sanity) · A2c **circular-shift surrogate**(TEST history 를 다른 TEST 위치로 decouple — marginal 유지, conditioning 파괴; EARNED control).

## Frozen bars (GREEN iff c1 ∧ c2; 아니면 c3 honest 🧱)
| bar | test | result (stride-300, byte-fair) | pass |
|-----|------|--------------------------------|------|
| **c1 PRESENCE** | A1 CE < 2.51335 − 0.01 = 2.50335 | **2.00562** (Δ **−0.50773** vs floor) | ✅ |
| **c2 EARNED** | A2c circular-shift ≥ 2.46335 (surrogate 가 같이 개선하면 안 됨) | A2c **5.10874**; A1 이 A2c 를 **3.10312** 차이로 이김 | ✅ |
| **c3 FLOOR-HONEST** | c1 거짓이면 honest 🧱 | c1 참 → 미적용 | — |

→ **🟢 GREEN** (c1 ∧ c2; FREEZE bar verbatim, 사후 이동 없음).

## Results
| arm / diagnostic | CE (nats/UTF-8-byte) | note |
|---|---|---|
| raw-byte ceiling (ref) | 2.95342 | H_1316 G0 |
| **jamo floor (locked)** | **2.51335** | H_1316 mitosis, 깨야 할 대상 |
| **A1 JM-interp (GATE, stride-300)** | **2.00562** | **Δ −0.50773 vs floor** (c1) |
| A0 unigram-only (GATE) | 3.21153 | sanity — 컨텍스트 없으면 floor 위 |
| A2c circular-shift (GATE) | 5.10874 | conditioning 파괴 → 안 좋아짐 (c2) |
| A1 JM-interp (DENSE, stride-6, 2.1M train, **NON-GATING**) | **1.47042** | Δ −1.04293 — 데이터 늘면 더 내려감 |

**차수 sweep (GATE, A1)**: nmax 2→3→4→5 = 4.319 → 3.326 → 2.584 → **2.006**. 이득은 전적으로 **고차(order-5)** 에서 나온다.

## ⚠ HONEST SCOPE — GREEN 의 정체는 "코퍼스 반복 암기" (c9, 카드의 핵심)
NON-GATING 진단(`context_seen_diag`): TEST 위치의 top-order(4-jamo) 컨텍스트를 TRAIN 에서 본 비율 = **70.1%**.
- **CE | seen-context = 1.6474** (반복 문자열 암기 슬라이스, 70%)
- **CE | novel-context = 2.8819** (진짜 generalization 슬라이스, 30%) — **이 novel 슬라이스는 floor 2.51335 보다 나쁘다.**

즉 30MB 한국어 web 코퍼스는 **반복적**(boilerplate/템플릿/반복 구절)이고, 고차 n-gram 은 반복되는 jamo 문자열을 **암기**해서 held-out 의 70%(같은 문자열 재등장)를 1.65 로 맞춘다. 고정용량 mitosis 분할은 이 반복 문자열을 **구조적으로 저장할 수 없어서** floor 에 갇혔던 것이다. 그러므로:
- **사실 1 (bar 통과)**: non-fragmenting JM interpolation 은 held-out CE 를 floor 아래로 내린다(2.006 < 2.513, surrogate 대조로 EARNED). → 🟢
- **사실 2 (honest)**: 그 이득은 **코퍼스 중복 암기**이지 한국어의 더 깊은 합성 모델이 아니다. 진짜 novel 컨텍스트에서는 floor 를 못 이긴다(2.88 > 2.51).
둘 다 참이고 둘 다 카드에 남는다. A2c 가 c2 를 살린 이유도 동일: history-label 쌍을 깨면 암기 테이블이 자신만만하게 틀린다(그래서 5.11, unigram 3.21 보다 높음) — 이것이 "이득이 jamo-순서 구조에서 온다"의 증거.

## Scope / caveats (a_scale_honest_scope · a_toy_scale_recheck)
- **DIRECTIONAL numpy**; held-out next-symbol CE on toy stride-300 byte-substrate, NOT fluent decoder; NO Korean-fluency claim. Engine-transfer to live `CORE/*.hexa` A⇄G + MITOSIS VAdaptField = follow-on (a_engine_native_learning · a_verified_must_wire). **CORE UNTOUCHED.**
- λ 단일 schedule(frozen), 단일 corpus window, 단일 stride 게이트. λ 는 FREEZE 에 고정, scoring 후 이동 없음.
- floor(2.51335)와 JM 는 같은 stride-300 byte-fair 축에서 비교(게이트). DENSE(stride-6)는 밀도가 달라 NON-GATING — floor 가 부분적으로 investment artifact(데이터 부족)임을 보여줄 뿐.

## 결론 / next angle
NON-FRAGMENTING frozen-λ Jelinek-Mercer interpolation 은 **held-out 한국어에서 jamo 2.51335 floor 아래로 내려간다(🟢, bar EARNED)** — 그러나 그 이득은 고정용량 mitosis 가 담지 못한 **코퍼스 반복 문자열 암기**이고, 진짜 novel 컨텍스트에서는 floor 를 못 이긴다(2.88). 그러므로 "한국어의 정보 floor 가 2.513 아래로 진짜 내려간다"는 강한 주장은 **여전히 미증명** — JM 의 GREEN 은 메커니즘(반복 저장 능력)의 차이를 드러낼 뿐 표상 floor 를 깨지 않았다.
- **NEXT-1 (depletion test)**: novel-context-only held-out 에서 2.51335 를 이기는 메커니즘이 있는가? (반복 암기 제거 후에도 floor 아래로 가야 진짜 floor-break.) depletion = de-duplicated 코퍼스(반복 문자열 제거)에서 c1 재시험 — 통과 못 하면 2.513 은 진짜 표상 floor.
- **NEXT-2**: engine-native wiring — H_1321 의 VAdaptField 가 가변-차수 back-off 를 표현하도록 확장(a_engine_native_learning, engine-transform-to-fit-the-learning).

## Pointers
- 카드: `UNIVERSE/cards/H_1344_ko_jm_interpolation.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1344)
- 코드: `state/ko-jm-interpolation/h1344_ko_jm_interpolation.py`
- 증거: `.verdicts/1344_ko_jm_interpolation/{H_1344_FREEZE.txt, result.txt, H_1344.txt}`
- CLAIMS: `CLAIMS.tape` @C h1344_ko_jm_interpolation
- xref: h1316(jamo floor)·h1321(jamo wire)·h1322(featural 🧱)·a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c9·c15
