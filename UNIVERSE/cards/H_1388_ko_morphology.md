# H_1388 — 🇰🇷 ko-morphology: morphology-aware 단위(BPE-on-jamo) 또는 longer-context 가 jamo-floor+0.28 잔여 격차를 깨는가?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1388_ko_morphology` · **Tier:** 🟢 GAP-REDUCED-CANDIDATE — H_1380 이 한국어 below-jamo 의 세 닫힌 레버(표상 H_1322 🧱 · interpolation H_1359 🧱 · data-volume H_1368/H_1380 🟠)가 전부 hit 한 **novel-context CE 잔여 격차 = jamo floor(2.51335)+0.28 = 2.79335** 를 못 뚫는다고 봉인하고, genuinely-NEW 두 각도 — **(1) morphology-aware 단위(형태소/BPE-on-jamo)** · **(2) cross-syllable long-range(nmax>5)** — 를 NEXT 로 명시했다. H_1388 의 **PRIMARY = BPE-on-jamo** 가 novel-context CE 를 **2.56603** 으로 끌어내려 잔여 격차를 **+0.28 → +0.05 (floor 위)** 로 붕괴시킨다 — 즉 +0.28 잔여를 **−0.227 마진으로 BEAT**. shuffle 대조(random equal-count merges, 3 seed)는 2.80159 로 잔여를 **못 뚫는다** → gain 은 merge 의 **언어적 구조(형태소-유사 sub-unit)**, 단순 coarse-granularity 아님. **morphology 가 한국어의 진짜 새 레버**다.

DIRECTIONAL numpy · REAL R2 KO 코퍼스 30MB sha `c47b6808…` (== H_1316/H_1359/H_1368/H_1380, byte-fair, 새 fetch 없음) · $0 CPU (206s) · frozen-first (FREEZE 가 measuring 전 작성) · jamo 표상·novel-filter·JM λ·shift surrogate **모두 H_1368/H_1380 와 동일 FROZEN** (anti-Goodhart) · c9/c16 NO tune-to-green · live CORE UNTOUCHED (DIRECTIONAL probe).

## Claim (falsifiable)
세 레버(표상·interpolation·data-volume)가 전부 novel-context 에서 jamo floor 위 ~+0.28 에서 막혔다(H_1380: asymptote ~2.747, 30MB novel-CE 2.88190). H_1380 이 남긴 두 각도는 **데이터/표상-at-jamo 가 아닌** 진짜 새 표상-변경: (1) **morphology-aware 단위** — jamo 보다 **coarse 한 언어 단위**(형태소/BPE-on-jamo)가 next-unit 예측에서 next-jamo 보다 더 많은 nats/byte 를 담는가? (2) **longer-context** — count-head 의 nmax=5 단거리 천장이 잔여의 원인인가? H_1388 은 PRIMARY=BPE-on-jamo + SECONDARY(non-gating)=nmax 스윕으로, 잔여 2.79335 를 frozen 마진 ≥0.05 로 BEAT 하는지(🟢) / 못 뚫는지(🧱) 결정한다.

## Method (frozen-first; H_1368/H_1380 기계 verbatim 재사용 + BPE 레이어)
- **REAL Korean only**: 같은 R2 `anima-7b/web/kor/shard0000.bytes` 의 30MB PREFIX (sha `c47b6808…` ASSERTED == H_1368). sha mismatch → STOP, NO synthetic. jamo-stream 길이 25,501,291 = H_1380 30MB rung 과 정확히 동일.
- **jamo 표상 / NOVEL-filter / JM λ / shift surrogate (H_1316/H_1359/H_1368/H_1380 전부 동일 FROZEN)**: Hangul→NFD jamo(id 256+rank)·non-Hangul→raw byte(byte-fair, Vj=323)·JM recursive interp λ=[1,2,4,8,16]/31·nmax=5·Laplace1.0·stride=300 even=TRAIN/odd=TEST·top-order(4-jamo) context TRAIN 부재 위치만 점수(== H_1359 TEST A genuine-generalization).
- **PRIMARY = BPE-on-jamo (morphology-aware 단위)**: TRAIN jamo 스트림 위에서 빈도-랭크 merge 2000개 학습(test 누출 0 — train slice only) → 그 merge 로 FULL 스트림 재인코딩 → 같은 JM count-head 를 BPE **단위** 위에서 fit → novel-only held-out CE 를 **nats/UTF-8-BYTE** 로 점수(confound-fair: BPE 단위는 byte 가 더 길므로 단위당이 아니라 단위의 byte span 으로 나눔 = jamo floor 와 직접 비교가능, 같은 axis). 효율적 position-indexed BPE(learn+apply, naive full-rescan 과 merge-order byte-exact 검증, byte 보존).
- **SHUFFLE 대조 (bar2 earned)**: random equal-COUNT merges — merge 개수·결과 vocab 밴드 동일하되 merge PAIR 를 관측 adjacent pair 위에서 RANDOM 선택(seed별). gain 이 merge 의 **언어 구조**인지 단순 coarse 단위인지 분리. 3 seed [4387,4388,4389].
- **SECONDARY (non-gating diagnostic)**: jamo 스트림 위 nmax ∈ {5,7,9} novel-CE 스윕 — 각도(2) cross-syllable long-range. tier 를 바꾸지 않음.

## Frozen bars (FREEZE verbatim, 사후 이동 없음)
| bar | test | result | pass |
|-----|------|--------|------|
| **1 GAP-REDUCED** | BPE-on-jamo novel-CE ≤ 2.79335 − 0.05 = **2.74335** | BPE novel-CE = **2.56603** (≤2.74335, Δresidual **−0.22732**) | ✅ |
| **2 EARNED (shuffle)** | shuffle mean-CE NOT ≤2.74335 **AND** (shuffle−BPE) ≥0.03 | shuffle mean **2.80159** (Δresidual +0.00824, 못 뚫음) · structured gain **+0.23556** ≥0.03 | ✅ |
| **3 CONTROL** | jamo anchor 재현 |Δ|≤0.02 (2.88190) **AND** shift surrogate earned (≥0.05) | anchor **2.88190** (|Δ|=**0.0**) · shift−novel **+0.39060** ≥0.05 | ✅ |

→ **🟢 GAP-REDUCED-CANDIDATE** (bar1✅ ∧ bar2✅ ∧ bar3✅). FREEZE TIER 매핑의 사전등록 분기 — tune-to-green 아님.

## Results (verbatim)
| measure | units/jamo | novel-CE | Δ vs floor 2.51335 | Δ vs +0.28 residual 2.79335 |
|---|---|---|---|---|
| jamo floor anchor (nmax5) | 1.000 | **2.88190** | +0.36855 | +0.08855 |
| **BPE-on-jamo structured (PRIMARY)** | **0.3391** | **2.56603** | **+0.05268** | **−0.22732** |
| shuffle seed 4387 | 0.9466 | 2.80589 | +0.29254 | +0.01254 |
| shuffle seed 4388 | 0.9233 | 2.81473 | +0.30138 | +0.02138 |
| shuffle seed 4389 | 0.9311 | 2.78414 | +0.27079 | −0.00921 |
| **shuffle mean (3 seed)** | ~0.93 | **2.80159** | +0.28824 | +0.00824 |
| nmax=7 jamo (secondary) | 1.000 | 2.77788 | +0.26453 | −0.01547 |
| nmax=9 jamo (secondary) | 1.000 | 3.05141 | +0.53806 | +0.25806 |

- **structured gain over shuffle = +0.23556** (2.80159 − 2.56603). 구조적 BPE 는 0.3391 units/jamo 로 압축(≈3 jamo/단위 = 형태소-유사)하며 2.566 에 도달, random merge 는 0.93 units/jamo 로 거의 압축 못 하고 2.80 에 머묾 → **lift 는 merge 의 언어 구조**.
- **SECONDARY 진단 (non-gating)**: nmax=7 이 잔여를 살짝(−0.015) 넘지만 nmax=9 는 over-sparse 로 악화(+0.258, novel_frac 0.855 — context 가 거의 unseen) → long-range 단독은 약하고 비단조. BPE 가 결정적 레버.
- jamo anchor 2.88190 = H_1380 30MB 와 byte-exact(|Δ|=0.0) → methodology-drift anchor PASS, 누출 0.

## ⚠ HONEST SCOPE — 무엇이 확정되고 무엇이 아닌가 (c9)
- **확정 (이 라운드가 H_1380 의 NEXT-1 morphology 각도를 RESOLVE)**: jamo-floor+0.28 잔여(2.79335)는 세 닫힌 레버 전부에서 hit 됐지만 **morphology-aware 단위(BPE-on-jamo)로 깨진다** — novel-context CE 가 2.566 까지 내려가 잔여를 −0.227 마진으로 BEAT, floor 위 +0.05 로 격차 붕괴. shuffle 대조가 못 뚫음(+0.236 구조 gain) → **언어 구조(형태소-유사 단위)**가 원인, 단순 coarse-granularity 아님. **morphology 는 한국어의 진짜 새 레버.**
- **HONEST byte-fair (load-bearing, c9)**: CE 는 nats/UTF-8-BYTE — BPE 단위가 byte 를 더 많이 덮으므로 단위당 CE 가 아니라 단위 byte span 으로 나눠 jamo floor 와 동일 axis 로 비교(confound 제거). units/jamo 0.3391 = 단위가 평균 ~3 jamo 를 묶음(형태소 규모). bar2 shuffle 이 이 byte-fair 마진에서도 못 뚫음을 확인.
- **확정 아님 (scope)**: DIRECTIONAL numpy, toy stride-300 byte-substrate next-symbol CE(fluent decoder 아님, 한국어 유창성 주장 없음). ONE 30MB 윈도 · 단일 frozen λ · 단일 stride · BPE merge=2000 frozen · 단일 표상(jamo→BPE). **engine-transfer UNVERIFIED** — 이 BPE-on-jamo 단위는 CORE 의 jamo/byte substrate 가 아니므로 엔진-native 실현(generator L3 / decode 단위)이 binding verdict 의 follow-on (a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck).

## 결론 / next angle
**한국어 below-jamo 잔여 +0.28 는 데이터/표상/보간으로 안 깨졌지만 morphology-aware 단위(BPE-on-jamo)로 깨진다** — novel-context CE 2.88190 → 2.56603 (격차 +0.28 → +0.05), shuffle-earned. 이는 H_1380 이 명시한 두 새 각도 중 **morphology 각도가 LIVE** 임을 의미 (DIRECTIONAL). long-range(nmax) 단독은 약·비단조(secondary 진단).
- **NEXT-1 (a_engine_native_learning · a_verified_must_wire)**: 이 곡선은 DIRECTIONAL numpy mirror — gap-reduced 결론이 binding 이려면 BPE-on-jamo 단위를 엔진-native(CORE decode 단위/generator L3 슬롯)로 실현해 frozen bars 재확인. 🟢-candidate 이므로 wire 우선순위 높음(레버 열림, vs H_1380 의 닫힌 negative).
- **NEXT-2 (a_scale_honest_scope)**: merge-count 사다리(500/2000/8000) + 윈도 사다리(30/120MB) 로 morphology lift 가 scale 에서 holding 하는지, jamo floor 자체에 닿는지.
- **DEPLETION**: 한국어 below-jamo 질문은 이제 데이터·표상·interpolation·**morphology**·long-range 다섯 각도가 모두 측정됨 — morphology 가 **격차를 줄임**(🟢-candidate), long-range 는 약함. 잔여가 morphology 로 깨졌으므로 이 arc 는 더 이상 terminal-🧱 가 아니라 **morphology 레버 열림** → 엔진-native 재확인이 닫는 follow-on.

## Pointers
- 카드: `UNIVERSE/cards/H_1388_ko_morphology.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1388)
- 코드: `state/ko-morphology/h1388_ko_morphology.py`
- 증거: `.verdicts/1388_ko_morphology/{FREEZE.txt, result.txt}`
- xref: h1380(이 카드의 PARENT·+0.28 잔여 + 명시한 morphology/long-range 각도·30MB novel-CE 2.88190 anchor)·h1368(data-richness, 30MB anchor)·h1359(JM=암기 🧱, novel filter)·h1322(featural 🧱)·h1316(jamo floor 2.51335 locked)·h1307(raw ceiling 2.95342·KO shard)·h1336(cross-syllable long-range)·a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire·a_core_engine_map·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c9·c15·c16
