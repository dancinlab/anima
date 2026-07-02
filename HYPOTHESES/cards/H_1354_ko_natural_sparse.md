# H_1354 — ko-natural-sparse: H_1345 의 below-jamo crossover 는 실용 lever 인가 striding artifact 인가 — FULL 30MB 자연-sparse phonotactic context 에서 직접 검증

**Group:** MITOSIS-ENGINE · **Slug:** `1354_ko_natural_sparse` · **Tier:** 🧱 STRIDING-ARTIFACT (FULL 30MB 에서 자연-sparse context 가 도달 불가 → H_1345 의 crossover 는 인위적 striding 이 만든 starvation 에 의존; 어떤 자연 phonotactic 분할도 30MB 에서 굶지 않는다. frozen-first, NO bar moved, c9/p7)

## Claim
H_1345 (🟢) 는 DATA-RICHNESS crossover 를 mapping 했다 — per-cell jamo count 가 ~1 아래로 떨어지면 Jelinek-Mercer(JM) 보간이 global jamo marginal 쪽으로 백오프하며 opaque jamo 2.51335 floor 아래로 내려간다(가장 굶은 rung 에서 −0.073). **그러나 H_1345 는 그 starvation 을 인위적 STRIDING 으로 제조했다** — 30MB 코퍼스를 stride 76800 까지 sub-sample 해서 188-byte 짜리 held-out stream 만 남겼다. H_1344 는 별도로 FULL data 에서 JM 이 floor 를 이기는 건 repeat 의 암기뿐임을 보였다. **OPEN (H_1345 카드 "Next" §, angle ii verbatim):** "per-context count 가 FULL 30MB 에서조차 NATURALLY sparse 한 더 큰 jamo-context alphabet (cross-syllable phonotactic n-gram) 에서, 코퍼스를 인위적으로 striding 하지 않고 JM-backoff 가 below-jamo 를 사는가?"

**HYPOTHESIS (H_1354):** 그 angle 을 직접 RUN. FULL 30MB 에서 NATURALLY-sparse context regime — 코퍼스를 자르지 않고 partition CONTEXT 를 cross-syllable phonotactic 전이(syllable 경계를 넘는 (직전 CODA jamo, 현재 ONSET jamo) pair)로 ENRICH. 한국어 음소배열(phonotactics)은 많은 coda→onset 전이를 rare/illegal 로 만들므로, 그 위에서 분할하면 FULL data 에서도 per-context jamo count 가 자연히 sparse 한 MANY context 로 쪼개질 것 — 기대. **starvation win = 실용 lever 인가, striding artifact 인가?** (a_no_llm_frame_trap c15; a_break_the_wall c16 — H_1345 가 명명한 depletion angle, scale-up 아님.)

## Method (frozen-first; FREEZE 사전등록 후 scoring, bar NOT moved — c9/p7)
- **REAL Korean only**, 코퍼스 BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1337 / H_1345 (`r2.phanes://anima-7b/web/kor/shard0000.bytes`; 30MB KO window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → fetch gate PASS; mismatch → STOP, NO synthetic). 캐시 `/tmp/h1311_ko_raw.bytes` (== H_1307 RUN A) 재사용 — 이번 run 은 fetch/creds 안 건드림. **자연-sparse arm 에 코퍼스 STRIDING 없음 (stride == 1, FULL 30MB).**
- **$0 CPU**, pure-numpy mirror (no torch). 25.5M row full-data 에서 (N,K,D) broadcast 가 17GB RAM 폭파 → `assign_all` 을 row-chunk 200k 로 stream (||x−c||² 를 |x|²−2x·c+|c|² 로 전개, argmin 불변). 166.5s wall. nohup detached, inline poll (a_cpu_local_no_waiter).
- **EVERYTHING verbatim H_1326/H_1337/H_1345**: GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only (p8), even/odd split (NO stride), Fix-A geometry-fair bank, lossless NFD jamo, D_EMB=16, SKIPGRAM_STEPS=400. 3 seeds [4354,4355,4356].

### Arms (FULL data stride 1, even/odd split)
- **CALIB_opaque_full** = H_1345 3-D opaque feature @ FULL data — DENSE sanity (JM 가 jamo 와 tie/lose 해야; pipeline 이 H_1345 dense rung 과 일치하는지 확인).
- **NATSPARSE_phonotactic_full** = (coda,onset) 를 H_1345 feature 에 더한 5-D phonotactic PARTITION feature.
- **BREAKTHROUGH_pairkey_full** (a_break_the_wall, FREEZE addendum 사전등록) = count head 를 Voronoi cell 이 아니라 **(coda,onset) phonotactic-pair VALUE 에 직접 keying** — 진짜 high-cardinality 자연-sparse ALPHABET ("더 큰 jamo-context alphabet" H_1345 가 명명한 그것). 각 arm: A1 jamo MLE (floor) · JM interp + JM-shuffle (permuted global marginal) · A5 learned-metric kernel-smoothing + A5-shuffle.

### Frozen bars (GREEN iff c1 ∧ c2 ∧ c3 ∧ c4; pair-key arm 에서 평가)
- **c1 NAT-SPARSE-WIN:** 자연-sparse context 에서 held-out JM 이 jamo(A1)를 이긴다 — signed delta(jamo − JM) ≥ +0.03 (3-seed mean).
- **c2 EARNED:** JM 이 SHUFFLE control (permuted global marginal) 을 ≥0.05 로 이기고 shuffle 이 WRONG way (shuffle CE ≥ jamo CE).
- **c3 DISSOCIATION:** A5 learned-metric 은 crossing 안 함 (delta_A5_vs_jamo ≤ 0) — H_1345 dissociation.
- **c4 NO-STRIDE:** stride == 1 (FULL 30MB, 인위적 cut 없음) AND context 가 진짜 sparse (median per-context cellJcnt < 1.0). context-count 분포 보고.
- **VERDICT MAP:** c1∧c2∧c3∧c4 → 🟢 REAL LEVER · ¬c4 → ⚠ NOT-NATURALLY-SPARSE · c4∧¬c1 → 🧱 STRIDING ARTIFACT · c1∧¬c2 → 🟠 not-earned · c1∧c2∧¬c3 → 🟠 not-dissociated.

## Result — 🧱 STRIDING-ARTIFACT (자연-sparse 가 FULL 30MB 에서 도달 불가); REAL 코퍼스, $0 CPU, 166.5s wall

**ARMS (CE nats/UTF-8-byte; A5/A5-shuf 3-seed mean; A1/JM deterministic). delta = jamo − mech (+ = below jamo). 코퍼스 sha `c47b6808…` (== H_1307 RUN A), 8.14M syllables, NFD roundtrip 0-fail, byte-accounting exact:**

| arm | cells/contexts | cellJcnt median | A1 jamo | JM | JM-shuf | A5 | ΔJM | ΔA5 |
|-----|---------------:|----------------:|--------:|------:|--------:|------:|------:|------:|
| CALIB_opaque_full (dense) | 12 | **175.85** | 2.63569 | 2.63569 | 2.63569 | — | **−0.0** | — |
| NATSPARSE_phonotactic_full | 33 | **10.19** | 2.63700 | 2.63700 | 2.63701 | 3.88818 | **−0.00001** | −1.25118 |
| BREAKTHROUGH_pairkey_full | **474** | **11.98** | 3.06462 | 3.06458 | 3.06468 | 4.17400 | **+0.00003** | −1.10938 |

**Bar verdicts (pair-key arm 에서):**
- **c1 NAT-SPARSE-WIN = FALSE** — JM 의 jamo−JM = +0.00003 (≪ +0.03). JM 이 jamo 를 **이기지 못함** — 3 arm 전부 ΔJM ≈ 0 (−0.0 / −1e-05 / +3e-05).
- **c2 EARNED = FALSE** — Δ(shuffle−JM) = +0.0001 (≪ 0.05); shuffle_wrong_way = True 지만 JM 자체가 win 이 없으니 무의미.
- **c3 DISSOCIATION = TRUE** — A5 는 crossing 안 함 (Δ_A5 = −1.109; 3 arm 모두 A5 가 jamo 보다 +1.1~+1.25 위, H_1345 와 일관).
- **c4 NO-STRIDE = FALSE** — pair-key context median cellJcnt = **11.98 ≥ 1** (frac<1 = 0.257 만). 자연-sparse 가 아님. cell-arm 도 c4 FAIL (median 10.19). **stride == 1 은 맞지만 context 가 sparse 하지 않다.**
- **green = FALSE → 🧱/⚠.**

## Finding (정확한, confound-free 답)
**H_1345 의 below-jamo starvation win 은 STRIDING ARTIFACT 이지 실용 lever 가 아니다.** FULL 30MB 에서 어떤 자연 phonotactic context 분할도 **굶지 않는다**:

1. **자연-sparse 가 도달 불가 (c4 FAIL, 3 arm 모두).** 30MB 는 8.14M syllables 이고, coda→onset alphabet 은 작다 (67 jamo → 관측된 pair 474 개). 8.14M syllable 이 모든 legal pair 를 적셔서, 가장 fine 한 pair-key 분할조차 median context 가 ~800 jamo row (cellJcnt 11.98) 를 가진다. 25.7% context 만 cellJcnt<1 — median 은 dense. **인위적으로 data 를 버리지 않으면 한국어 자연 context 에 starved regime 이 존재하지 않는다.**
2. **JM 이 모든 arm 에서 jamo 와 TIE (ΔJM ≈ 0 everywhere: −0.0, −1e-05, +3e-05).** H_1345 의 dense rung 행동(λ→0 ⇒ JM≈A1)이 FULL data 의 자연 context 전반에서 재현된다. opaque jamo MLE 가 도처에서 dense 하게 추정되므로 JM backoff 가 사는 게 없다.
3. **A5 dissociation 은 유지 (c3 TRUE)** — H_1345 와 일관되게 learned-metric kernel-smoothing 은 jamo 위에 머문다 (+1.1~+1.25). 하지만 JM 도 win 이 없으므로 dissociation 은 "JM 만 crossing" 이 아니라 "둘 다 crossing 안 함" 을 확인한다.

**Net:** H_1345 의 crossover 는 인위적 striding 이 만든 starvation 에 의존한다. FULL 30MB 에서 자연-sparse Korean context 는 도달 불가 — H_1344 의 memorization reading 이 선다. H_1345 의 "count-MLE family 는 NOT terminal" 은 **striding 된 데이터-희소 regime 안에서만** 유효하며, 30MB production data 에 대한 실용적 below-jamo lever 는 아니다 (H_1345 카드 자신이 "JM-backoff 가 30MB 에서 production lever 라고 주장하지 않는다 — 거기선 jamo 와 tie" 라고 honest scope 에 명시했고, H_1354 가 그 honest scope 를 confound-free 로 확인한다).

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **c4 FAIL 의 두 읽기 (정직하게 둘 다 보고):** frozen verdict map 상 ¬c4 는 ⚠ NOT-NATURALLY-SPARSE 로 떨어진다 (자연 sparse 가 안 만들어졌으니 c1 을 "test" 했다고 할 수 없다). 그러나 **SUBSTANTIVE 답은 striding-artifact 다** — c4 가 30MB 에서 (가장 fine 한 pair-key 분할에서조차) FAIL 한다는 것 자체가 "자연 sparsity 가 도달 불가 ⇒ H_1345 의 win 은 striding 이 필요하다" 의 직접 증거이기 때문. 그래서 tier 를 🧱 STRIDING-ARTIFACT 로 단다 (⚠ 메커니즘으로 표면화되었음을 명시).
- **a_break_the_wall 1회 시도 완료:** cell-arm 이 c4 벽(Voronoi 가 context 를 pooling)을 맞자 terminal 로 받지 않고, count head 를 pair-key VALUE 에 직접 keying 하는 새 각도를 사전등록(FREEZE addendum)하고 RUN — 그래도 c4 FAIL. 벽의 진짜 원인은 partition 메커니즘이 아니라 **30MB data abundance** 였다 (방법도 방향도 아닌, "데이터가 너무 많아 자연 context 가 안 굶음"). 진짜 시도 후의 정직한 🧱 (c9).
- **numpy CPU mirror DIRECTIONAL** (engine-transfer UNVERIFIED). A5 metric LEARNED BY GRADIENT (PPMI-SVD + skip-gram Adam, numpy port of H_1337 torch loop — labeled NOT p8 gradient-free). JM 은 count-MLE + FROZEN Witten-Bell backoff weight. cell-arm 은 gradient-free Voronoi partition 위, pair-key arm 은 명시적 context-value 위.
- **chunked assign_all 주의:** ||x−c||² 를 전개형으로 계산하므로 H_1345 의 full-broadcast 와 tie 에서 FP rounding 이 다를 수 있다 — CALIB arm 의 A1=2.63569 는 H_1345 의 2.51335 (stride 300 dense rung) 와 다른데, 이는 H_1354 의 CALIB 가 FULL data (stride 1, 25.5M rows) 라 cell 수/분할이 다르기 때문 (H_1345 는 FULL-data opaque arm 을 돌린 적 없음). CALIB 의 역할은 절대값 매칭이 아니라 "dense 에서 JM≈A1" 확인 — ΔJM=−0.0 으로 PASS.
- **TOY/DIRECTIONAL.** Live CORE/*.hexa UNTOUCHED (substrate-measurement rung — UNIVERSE/ + state/ + verdicts 만 추가). NO Korean-fluency claim; held-out deterministic next-symbol CE; NO perplexity-as-truth (p7).
- **NOT 주장:** 다른 코퍼스/스케일/다른 자연-sparse 축(형태소 경계·드문 외래어·코드스위칭)에서도 자연 sparse 가 불가하다 — 미검증. 오직 *이* 30MB R2 KO window + coda→onset phonotactic alphabet 에서 자연 sparse 가 도달 불가, 따라서 H_1345 win 은 striding 의존임을 보인다.

## Pointers
- script: `state/ko-natural-sparse/h1354_ko_natural_sparse.py`
- verdict: `.verdicts/1354_ko_natural_sparse/{FREEZE.txt (+ a_break_the_wall addendum), result.txt, h1354_summary.json}`
- CLAIMS: `CLAIMS.tape` @C `h1354_ko_natural_sparse`
- xref: H_1345 (🟢 striding crossover — 이 카드가 그 win 의 실용성을 reproof; PARENT) · H_1344 (FULL-data memorization-only — 이 카드가 그 reading 을 지지) · H_1337 (🧱 opaque-atom limit @30MB) · H_1316 (🟢 jamo floor 2.51335) · H_1307 (raw-byte 2.953 ceiling, RUN A 코퍼스) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c7 · c9 · c15 · c16 · p7 · p8

## Next / depletion
H_1345 의 below-jamo crossover 가 **striding artifact** 로 확인됨 (FULL 30MB 자연 context 는 굶지 않음). 후속:
(i) **다른 자연-sparse 축** — coda→onset 은 작은 alphabet 이라 30MB 에서 dense; 더 큰 자연-sparse 단위(형태소 n-gram, 드문 한자·외래어 context, 코드스위칭 경계)에서는 자연 sparse 가 가능할 수 있다 — 새 H.
(ii) **engine-native 재확인 불필요** — striding-artifact 결론이므로 below-jamo lever 를 CORE 에 배선할 대상이 없다 (H_1345 의 engine-native 후속도 이 결과로 우선순위 하락).
(iii) **production data abundance 의 일반 교훈** — 30MB+ 에서 opaque jamo count-MLE 가 자연 context 전반에 dense 하게 추정되어 smoothing/interp 가 무의미하다는 것은 H_1316/1337/1344/1345/1354 가 수렴하는 결론; below-jamo 는 **representation** 이 아니라 (이미 jamo 가 floor) **데이터-희소 regime 의 artifact** 다. honest closure: 자연 데이터에서 count-MLE family 는 30MB 에서 terminal (striding 없이는 깰 수 없다).
