# H_1380 — 🇰🇷 ko-data-ladder: novel-context CE 의 asymptote 가 >30MB 데이터로 2.51335 jamo floor 아래로 내려가는가?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1380_ko_data_ladder` · **Tier:** 🟠 DESCENDING-FLOOR-ABOVE — H_1368 의 30MB 데이터-풍부도 사다리를 **60/120/240/480MB** 로 확장했다. novel-context CE 는 30→240MB 에서 계속 내려가다(2.882→2.791) **240MB 에서 floor 위 +0.277 의 최저점을 찍고 480MB 에서 다시 +0.0099 올라**(2.791→2.801) — 즉 **240MB 부근에서 평탄화/반전**. 5-rung power-law fit 이 이제 RELIABLE (c_inf=**2.74703**, p=0.4, r²0.932) 이고 그 asymptote 는 2.51335 floor 보다 **위(ABOVE, +0.234)**. ⇒ **더 많은 데이터가 격차를 좁히지만 floor 를 BELOW 로 깨지 못한다** — H_1368 의 log-linear ~470MB→floor 예측은 **반증**되고, asymptote 는 jamo floor 위 ~2.75 에 앉는다. 표상 레버(H_1322 🧱)는 데이터로 재오픈되지 **않음**.

DIRECTIONAL numpy · REAL R2 KO 코퍼스(shard0000.bytes prefix, 30MB sha `c47b6808…` == H_1368/H_1316/H_1359 byte-fair) · $0 CPU (241s) · frozen-first (FREEZE 가 measuring 전에 작성·H_1368 기계 verbatim 재사용) · λ·표상·novel-filter·shift surrogate **모두 H_1368 와 동일 FROZEN** (rung 마다 재튜닝 안 함, anti-Goodhart) · c9/c16 NO tune-to-green · live CORE UNTOUCHED.

## Claim (falsifiable)
H_1368 은 novel-context CE 가 30MB 에서도 **여전히 내려가는** 것을 보였다(3.75→30MB: 3.153→2.882, gap 42% 축소; log-linear −0.0929/doubling → ~470MB 에서 floor 닿음 예측; power-fit UNDETERMINED). 유일하게 살아있던 한국어 레버 = **DATA VOLUME**. H_1380 은 사다리를 >30MB 로 확장해 asymptote 가 2.51335 의 **BELOW(🟢 후보, 표상 레버 데이터로 재오픈) / AT(🧱 floor terminal) / ABOVE(🟠 floor 위에서 holds)** 중 어디인지 결정한다 — 분기 규칙은 measuring 전 FREEZE 에 고정.

## Method (frozen-first; H_1368 기계 verbatim)
- **REAL Korean only**: 같은 R2 `anima-7b/web/kor/shard0000.bytes`(10.5GB REAL)의 **더 큰 PREFIX 서브윈도**. 30MB-prefix sha = `c47b6808…` ASSERTED (== H_1368). sha mismatch → STOP, NO synthetic padding. R2 fetch 은 prior 시도가 이미 완료(480MB cache, 30MB sha 재검증). 각 rung sha 기록.
- **jamo 표상 / JM / NOVEL-filter (H_1316/H_1344/H_1359/H_1368 전부 동일 FROZEN)**: Hangul→NFD jamo(id 256+rank)·non-Hangul→raw byte(byte-fair, Vj=323); Jelinek-Mercer recursive interp λ=[1,2,4,8,16]/31·nmax=5·Laplace1.0; stride=300 even=TRAIN/odd=TEST·top-order(4-jamo) context 가 TRAIN set 에 **없는** TEST 위치만 점수(== H_1359 TEST A genuine-generalization). vocab 은 FULL 480MB 윈도에서 한 번 고정(rung 간 drift 없음).
- **EXTENDED LADDER (5 rung)**: 30 / 60 / 120 / 240 / 480 MB. 30MB rung 은 H_1368 의 novel-CE 2.88190(±0.02) 재현 = methodology-drift anchor.

## Frozen bars (FREEZE verbatim, 사후 이동 없음)
| bar | test | result | pass |
|-----|------|--------|------|
| **1 LADDER-EXTENDED** | ≥2 NEW rung >30MB on REAL KO (MB+sha) | **4** new rungs (60/120/240/480MB, sha 각 기록) | ✅ |
| **2 ASYMPTOTE** (사전등록 분기) | 두 estimator fit + floor 대비 분류 BELOW/AT/ABOVE/UNRESOLVED | power-fit c_inf=**2.74703** (p=0.4, r²0.932, **RELIABLE**) → **ABOVE** floor +0.234. log-fit b=−0.0228/doubling(r²0.902) | ✅ ABOVE |
| **3 HELD-OUT** | novel-only odd-stride, top-order ctx absent from TRAIN | == H_1368/H_1359 TEST A, NO leakage | ✅ (structural) |
| **4 CONTROL** | 30MB anchor 재현(|Δ|≤0.02) + shift earned 전 rung + floor 재측정 | anchor **2.88190** (|Δ|=**0.0**) · shift−novel earned **5/5** [+2.93~+3.58] · floor 재측정 보고(아래) | ✅ |

→ **🟠 DESCENDING-FLOOR-ABOVE** (bar1✅ ∧ bar4 anchor+earned✅ ∧ bar2=ABOVE). FREEZE TIER 매핑의 사전등록 분기 — tune-to-green 아님.

## Results (verbatim per-rung)
| rung | window bytes | sha256 (prefix) | stream len | novel_frac | **novel-CE** | Δ vs 2.51335 | shift−novel |
|---|---|---|---|---|---|---|---|
| 30MB | 29,999,999 | `c47b6808…` | 25,501,291 | 0.299 | **2.88190** | +0.36855 | +2.9285 |
| 60MB | 59,999,999 | `b8795598…` | 50,970,283 | 0.217 | **2.85579** | +0.34244 | +3.0786 |
| 120MB | 119,999,998 | `466fcdd2…` | 101,984,723 | 0.1577 | **2.83189** | +0.31854 | +3.2438 |
| 240MB | 239,999,999 | `cbf7545a…` | 203,955,630 | 0.1121 | **2.79069** | **+0.27734** (최저) | +3.4156 |
| 480MB | 480,000,000 | `c18a55be…` | 407,890,084 | 0.0808 | **2.80056** | +0.28721 | +3.5835 |

- step ΔCE = [−0.02611, −0.02390, −0.04120, **+0.00987**] → **bar2_DIRECTION = NON-MONOTONE** (30→240MB 단조 감소, **240→480MB 반전 +0.0099**).
- 30MB novel-CE=**2.88190** 는 H_1368 와 **정확히 일치**(|Δ|=0.0) → 기계 동일성 확인 (anchor PASS).
- power-law fit (이제 5 rung): c_inf=**2.74703**, amp=134.56, p=0.4, r²=0.932, **RELIABLE** (c_inf 가 raw-ceiling 위·p grid edge 아님). → asymptote = jamo floor 위 **+0.234**.
- log-linear fit: b=**−0.0228** nats/doubling (r²0.902, H_1368 의 −0.0929 보다 훨씬 완만 — 곡선이 펴짐). 이 완만한 추세로 floor 닿으려면 ~12.6 doublings(~3,000,000MB)=**비현실적**. H_1368 의 ~470MB 예측은 **반증**.

## ⚠ HONEST SCOPE — 무엇이 확정되고 무엇이 아닌가 (c9)
- **확정 (이번 라운드가 H_1368 의 UNRESOLVED 를 RESOLVE)**: asymptote 는 2.51335 jamo floor **위(ABOVE, ~2.747)**. 더 많은 REAL 데이터(30→480MB, 16×)는 격차를 좁히지만(+0.369→+0.277 까지) **floor 를 BELOW 로 깨지 못한다**. 한국어 below-jamo 레버 셋(표상 H_1322 🧱 · interpolation H_1359 🧱 · data-richness)에서 **데이터 레버도 floor 를 BELOW 로 못 뚫음** → H_1322 표상 레버는 데이터로 재오픈되지 **않는다**.
- **HONEST 비단조 (load-bearing, c9)**: 240MB 가 최저점(+0.277), 480MB 에서 +0.0099 반전 = FREEZE 의 "FLATTENS at some window → that window IS the empirical asymptote" 조건 발동. 즉 경험적 asymptote 는 ~240–480MB 부근, novel-CE ≈ 2.79–2.80, floor 위 ~+0.28. power-fit c_inf 2.747 은 이보다 약간 낮은 외삽치(둘 다 floor 위).
- **HONEST floor-shift (보고-전용, bar4 fail 아님)**: bar4 의 floor 재측정(480MB, **in-distribution all-gate** count-MLE, novel-filter 없음)=**1.60137**, 2.51335 대비 **−0.912** = floor_stable **FALSE**. 이는 **in-distribution** CE 가 480MB 의 풍부한 n-gram coverage 로 크게 내려간 것(데이터-풍부도 효과 그 자체) — 단 H_1316 floor 2.51335 는 **novel/held-out** 기준이 아니라 30MB count-MLE 기준이라 정의가 다르고, novel-context asymptote 2.747 결론은 영향받지 않음. floor 참조 자체가 데이터-의존적임을 정직히 기록(FREEZE bar4 가 예고).
- **확정 아님 (scope)**: DIRECTIONAL numpy, toy stride-300 byte-substrate next-symbol CE(fluent decoder 아님, 한국어 유창성 주장 없음). 사다리는 **ONE shard0000 의 PREFIX 서브윈도**(byte-fair 동일 코퍼스 family). 단일 frozen λ·단일 stride·단일 표상(jamo). asymptote=5-point 외삽(wide CI, 비단조 tail). engine-transfer UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).

## 결론 / next angle
**2.51335 floor 는 데이터로도 BELOW 로 깨지지 않는다** — novel-context CE asymptote 는 jamo floor **위 ~2.747** 에 앉고, 30→480MB(16×)는 격차를 좁히되 닫지 못한다(240MB 부근 평탄화·480MB 반전). H_1368 의 ~470MB→floor 예측은 반증. 한국어 below-jamo arc 의 세 레버(표상·interpolation·data-richness) **전부 floor 를 BELOW 로 못 뚫음** → below-jamo 는 데이터로 재오픈되지 않는, novel-context 에서 jamo floor **위**에 holds 하는 진짜 한계. **DATA-VOLUME 레버 DEPLETED (valid 🟠, c9/c16 — 진짜 돌파 시도 후의 정직한 한계).**
- **NEXT-1 (a_break_the_wall · a_no_llm_frame_trap)**: 마지막 한국어 각도는 더-이상 "데이터/표상/interpolation" 이 아님(3 레버 전부 floor-above/terminal). novel-context 에서 floor 위 ~+0.28 의 잔여 격차는 **morphology-aware 단위(형태소·BPE-on-jamo)** 또는 **cross-syllable 장거리 의존(H_1336 계열)** 이 substrate 렌즈로 남은 후보 — n-gram(nmax=5) 의 단거리 천장일 수 있음. 단 이건 표상/모델 변경이라 별도 가설.
- **NEXT-2 (a_engine_native_learning · a_verified_must_wire)**: 이 곡선은 DIRECTIONAL numpy mirror — asymptote-ABOVE 결론이 binding 이려면 engine-native(CORE VAdaptField count-MLE)에서 재확인. 단 floor 가 **데이터로 안 깨진다**는 negative 라 엔진-wire 우선순위 낮음(레버 닫힘).
- **DEPLETION TEST**: 한국어 압축 레버 셋(표상 H_1322 · interpolation H_1359 · data-richness H_1368/H_1380) **전부 floor 를 BELOW 로 못 뚫음** = 이 arc 의 "데이터/표상/보간" 축은 DEPLETED; 남은 후보는 **다른 표상 단위(morphology)** 뿐이고 그건 새 substrate 렌즈 가설.

## Pointers
- 카드: `UNIVERSE/cards/H_1380_ko_data_ladder.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1380)
- 코드: `state/ko-data-ladder/h1380_ko_data_ladder.py`
- 증거: `.verdicts/1380_ko_data_ladder/{FREEZE.txt, result.txt}`
- xref: h1368(이 카드의 NEXT-1·30MB novel-CE 2.882 anchor·log-linear 470MB 예측을 반증)·h1359(JM=암기, novel-CE 2.882 floor-confirm)·h1344(JM GREEN=반복 암기)·h1316(jamo floor 2.51335 locked)·h1322(featural 🧱, 데이터로 재오픈 안 됨)·h1307(raw ceiling 2.95342·KO shard)·h1336(cross-syllable, next-1 후보)·a_no_llm_frame_trap·a_break_the_wall·a_fire_autonomous·a_engine_native_learning·a_verified_must_wire·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c9·c15·c16
