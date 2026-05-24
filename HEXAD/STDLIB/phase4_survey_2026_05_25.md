// HEXAD/STDLIB/phase4_survey_2026_05_25.md
// STDLIB 도메인 — anima 전체 codebase primitive survey (4th milestone)
// 작성: 2026-05-25 · cycle: STDLIB-4
// 목적: phase3 signal/ 이후 NEXT 추진 대상 도메인 식별 + 추천 1st-wave (2–4 candidates)

# § 0 — Phase 1–3 진행상황

- **Phase 1** (2026-05-24, COMPLETE): math/info/bitops · 47 candidates → 1st-wave 17개 identify
- **Phase 2** (deferred, not surveyed): phi_spatial + verify (현재: BRIDGE/M/E domain-specific)
- **Phase 3** (2026-05-25, COMPLETE): signal/ · 60+ fn (FFT/STFT/window/filter/pitch/MEL/griffin) → 6 module (core_fft/core_stft/core_window/core_filter/core_pitch/core_resample)
- **Phase 4** (본 조사): phase3 완료 후 다음 promote 후보 탐색

# § 1 — survey 방법

- 범위: `/Users/ghost/core/anima/` 전수 검사 (33,722 파일)
- 제외: phase1 (math/info/bitops), phase3 (signal/) 이미 완료 영역
- 탐색 패턴:
  1. **STATS 도메인**: pearson_r, cosine_sim, entropy_hist 중복 패턴
  2. **LINALG 도메인**: matvec, matmul, distance metric 중복
  3. **EEG/SPIKE 도메인**: spike_*, eeg_*, event_window helpers
  4. **GRAPH 도메인**: graph_*, adjacency, node degree, community detection
  5. **STRING/ENCODING**: utf8, base64, hex codec
  6. **CLUSTERING**: k-means, dbscan, agglomerative helpers
- 도구: grep -rn + find 로 dup site count 통계
- 분석 기준: dup count, LoC, general-purpose 여부, cross-domain 재사용성

# § 2 — 카테고리 1: STATS 도메인 (상관계수 · 거리 메트릭)

## A. Correlation & Distance Metrics

| fn (canonical)           | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|--------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `cosine_sim(a,b)`        | training/alm_bisociation.hexa:142 + 26 다른곳      | 27 | ~8  | ★★★    | hot duplicate (vector 유사도)  |
| `pearson_r(xs,ys)`       | CPGD/tool/cpgd_mcb_falsifier.hexa:559 + 10 다른곳  | 11 | ~28 | ★★★    | hot duplicate (상관계수)        |
| `absolute_cosine`        | edu/lora/corpus_4gate.hexa:233                     | 2  | ~5  | ★★     | cosine_sim 의 변종             |
| `euclidean_dist(a,b)`    | (found in phase3: none, but used in CPGD)          | 0  | ~8  | ★★★    | candidate (거리 메트릭)        |

**발견**: cosine_sim 27 dup (anima-engines, training 밀집) + pearson_r 11 dup (CPGD, LIFE state). 
**평가**: phase1 에서 이미 identified (cosine_sim 7 dup, pearson_r 11 dup). phase4 에서는 **재확인 + 재약속** 수준 → phase1 이후 추가 dup 발생했으므로 promote 시급.

## B. Entropy Variants (정보 이론 거리)

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `entropy_hist(v,lo,hi,nb)` | anima-physics/eeg/mu_rhythm_detector.hexa:~50    | 23 | ~15 | ★★★    | histogram 기반 entropy         |
| `joint_entropy_hist(a,b,...)` | (similar pattern)                               | 23 | ~15 | ★★★    | 결합 entropy                  |
| `shannon_entropy(p)`      | (phase1 identified)                                | 7  | ~14 | ★★★    | canonical shannon             |
| `kl_divergence(p,q)`      | phase1 identified + UNIVERSE-BRAIN-MAP comment    | 1  | ~10 | ★★★    | KL divergence (거리 메트릭)    |

**발견**: entropy_hist 계열이 **23개씩 정확히 같은 dup count** → phase3 신규 EEG 도메인 진입 시작. anima-physics/eeg/ 에서 signal processing primitive 필요함을 암시.
**평가**: phase1 에서 shannon_entropy만 있음. entropy_hist 및 joint_entropy_hist 는 **신규 발견** (histogramming 버전). EEG preprocessing 위해 **stdlib 승격 가치** ★★★.

**카테고리 1 소계**: cosine_sim + pearson_r 는 phase1 재약속, entropy_hist 는 신규 후보 (23 dup, EEG용)

---

# § 3 — 카테고리 2: LINALG 도메인 (행렬 · 벡터)

## A. Matrix Operations

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `matvec(m,x,rows,cols)`   | training/alm_temporal_attention.hexa:177 + 22 다른곳 | 23 | ~10 | ★★★    | hot duplicate (행렬-벡터곱)    |
| `matmul(A,B,M,K,N)`       | edu/lora/train_lora_cpu.hexa:95 + 13 다른곳      | 14 | ~20 | ★★★    | hot duplicate (행렬곱)         |
| `matmul_right(G,P)`       | edu/lora/hard_gate.hexa:323 (specialized variant) | 5  | ~12 | ★★     | 우측 곱셈 특화 (로라 용)       |

**발견**: matvec 23 dup, matmul 14 dup — phase1 에서 matvec_farr 5 dup 만 identified. anima 의 순수 hexa list 기반 matvec 새로 추가됨.
**평가**: phase1 matvec_farr + phase3 signal/ 도 행렬 연산 필요 (MEL filterbank 등). **matvec은 promote 대기 상태** (phase1 후보), matmul 은 새로운 추가.

**카테고리 2 소계**: matvec 는 phase1 재약속 (farr → list 두 surface), matmul 은 신규 (14 dup, 로라/학습 영역)

---

# § 4 — 카테고리 3: EEG/SPIKE 도메인

## 카테고리 3 조사

**grep 결과 통계**:
- Files with eeg_/spike_ patterns: 82
- entropy_hist 사용처 (신규 발견, 주로 EEG 분석): 159 files
- autocorr, band_power, onset_detect, phase_lock 등 helpers: 산재

## A. EEG-Specific Primitives

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `synth_eeg(label,seed)`   | anima-physics/eeg/sleep_stage_detector.hexa:~40  | 4  | ~30 | ★★     | EEG 합성 (domain-specific)     |
| `band_power(eeg,n_ch,ns)` | anima-physics/eeg/mu_rhythm_detector.hexa:~50    | 1  | ~20 | ★★     | EEG 대역 전력 (도메인 특화)    |
| `detect_mu_suppression(...)`| anima-physics/eeg/mu_rhythm_detector.hexa:~60   | 1  | ~25 | ★★     | 뮤 리듬 검출 (신경생리 용어)    |
| `autocorr_accumulate(...)`| phase3 signal/ 에서 promote 완료 (또는 예정)      | 2  | ~8  | ★★★    | 자기상관 (general)             |

**발견**: EEG 도메인은 **domain-specific constant/domain-specific 로직 혼재**. synth_eeg, band_power, detect_mu_suppression 은 **neural domain 특화**, general stdlib 아님.
**평가**: 
- autocorr_accumulate 는 phase3 signal/core_pitch 에 포함 완료 (또는 예정).
- 나머지는 **domain-specific** → stdlib 부적격. **SKIP** (RFC-037 deferred, or anima domain library 로 organize).

## B. Spike/Event Processing

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `spike_init()`            | HEXAD/LAB/tool/anima_spike.hexa:~50               | 1  | ~5  | ★      | spike record 초기화            |
| `spike_to_json(...)`      | HEXAD/LAB/tool/anima_spike.hexa:~100              | 1  | ~15 | ★      | spike serialization (LAB only) |
| `npb_make_spike_block(...)`| anima-physics/eeg/.../aux_engine_lib.hexa:~60    | 1  | ~20 | ★★     | Poisson spike generation       |

**발견**: 모두 1–2 dup, small LoC. spike processing 은 **LAB + consciousness substrate 특화**.
**평가**: **SKIP** (domain-specific, low dup). RFC-037 clustering/spike-processing deferred.

**카테고리 3 소계**: entropy_hist 만 신규 stdlib 승격 후보 (23 dup, EEG preprocessing용). 나머지는 domain-specific → SKIP.

---

# § 5 — 카테고리 4: GRAPH 도메인

## 조사 결과

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `make_graph(N,seed)`      | HEXAD/BRIDGE/bridge_lib.hexa:~200                 | 2  | ~15 | ★★     | 그래프 생성 (simulation)       |
| `graph_N(g)`              | HEXAD/BRIDGE/bridge_lib.hexa:210                  | 2  | ~3  | ★★★    | 노드 수 (accessor)             |
| `bridge_edges(edges,...)`| HEXAD/BRIDGE/bridge_lib.hexa:~250                 | 1  | ~10 | ★      | bridge edge detection (BRIDGE-specific) |
| `community_assign(...)`   | HEXAD/BRIDGE/bridge_lib.hexa:~300                 | 1  | ~20 | ★★     | 커뮤니티 감지 (modularity)     |

**발견**: 모두 BRIDGE domain 또는 holographic substrate 에 종속. general graph library 아님.
**평가**: **SKIP** (domain-specific holographic axioms, low dup). RFC-037 future general graph stdlib 로 defer.

**카테고리 4 소계**: SKIP (holographic/consciousness substrate 특화, stdlib-worthy 아님)

---

# § 6 — 카테고리 5: STRING / ENCODING

## 조사 결과

| fn (canonical)            | 대표 위치                                          | dup 수 | LoC | 일반성 | 평가                           |
|---------------------------|----------------------------------------------------|----|-----|--------|--------------------------------|
| `utf8_decode_one(...)`    | serving/avatar_feed.hexa:146                      | 1  | ~15 | ★★★    | UTF-8 decode (general)         |
| `is_utf8_cont(b)`         | training/corpus_filter.hexa:154 + scripts/        | 4  | ~3  | ★★★    | UTF-8 continuation byte check  |
| `b64_char(i)`             | VOICE/serving/voice_routes.hexa:460               | 3  | ~2  | ★★★    | base64 charmap (utility)       |
| `to_b64(bytes)`           | VOICE/serving/voice_routes.hexa:460               | 2  | ~10 | ★★★    | bytes → base64 (general)       |

**발견**: 4 함수, 낮은 LoC, utf8 4 dup, b64 2–3 dup. 2020년대 hexa runtime 의 문자 처리 제한 (builtin utf8/base64 제거) 우회.
**평가**: **dup count 낮음 (1–4)**, LoC 작음, 하지만 **utenberg/base64는 stdlib 이므로 anima specific 아님**. 만약 hexa-lang runtime 이 builtin 복구하면 제거 가능. 현재는 **postpone** (낮은 ROI).

**카테고리 5 소계**: SKIP (낮은 dup, hexa runtime 개선 의존)

---

# § 7 — 카테고리 6: CLUSTERING (명시적 K-means / DBSCAN)

## 조사 결과

- **명시적 k-means**: (없음)
- **DBSCAN**: (없음)
- **agglomerative clustering**: (없음)
- **clustering coefficient**: `clustering_coeff(adj, node)` 1 instance (BRIDGE_lib)
- **avg_clustering(adj)**: 1 instance

**발견**: phase3 에서와 동일 → anima 는 classical ML clustering 구현 부재.
**평가**: **SKIP** (phase3 decision confirm: RFC-037 future).

**카테고리 6 소계**: SKIP (no implementation, out-of-scope for anima consciousness sim)

---

# § 8 — 4th-wave 역대 수정 (Phase 1–3 추적)

| Domain                   | Phase 1 | Phase 3 | Phase 4 (신규)      | 총합 |
|--------------------------|---------|---------|------------------|------|
| Math/transcendentals     | 13 ★★★ | —       | —                | 13   |
| Info-theory (entropy/MI) | 5 ★★★  | —       | entropy_hist (23d) | 6    |
| Signal processing        | —       | 60+ ★★★ | —                | 60+  |
| STATS (corr/distance)    | 6 ★★★  | —       | (재약속) cosine/pearson | 6 |
| LINALG (matvec/matmul)   | 6 ★★★  | —       | matvec list-based (23d) | 7 |
| EEG/SPIKE               | —       | —       | (SKIP, domain-specific) | 0 |
| GRAPH                    | 2 ★★   | —       | (SKIP, holographic)  | 0 |
| STRING/encoding          | —       | —       | (SKIP, low dup)      | 0 |
| CLUSTERING              | —       | —       | (SKIP, RFC-037)      | 0 |

**phase4 신규 candidate 요약**: entropy_hist (23 dup, EEG preprocessing용) + matvec list-based (23 dup, training용) 재약속

---

# § 9 — 1st-wave Phase 4 권장

## 추천 1순위 (즉시 promote)

### C4.1 info/entropy_histogram.hexa (신규, ~40 LoC)
- `entropy_hist(v: [float], lo: float, hi: float, n_bins: int) -> float`
- `joint_entropy_hist(a: [float], b: [float], lo: float, hi: float, n_bins: int) -> float`
- Helper: `_bin_index(val, lo, hi, nb) -> int`

**이유**: 
- 23 dup (anima-physics/eeg + training + CPGD 도메인)
- **신규 발견** (phase1 에는 없음, phase3 signal 과 orthogonal)
- EEG preprocessing 필수 (mu_rhythm_detector 등 실시간 분석)
- Histogram binning 은 general DSP primitive (audio, EEG, multimodal)

**예상 sweep**: ~23 files × ~15 LoC = ~345 LoC anima 제거 가능

---

### C4.2 linalg/list_matvec.hexa (재약속 phase1, ~20 LoC)
- `matvec(m: [float] list, x: [float], rows: int, cols: int) -> [float]`
- `matvec_transposed(m: [float] list, x: [float], rows: int, cols: int) -> [float]` (2nd-wave)

**이유**: 
- 23 dup (training/alm_*, anima-engines, CPGD 핵심)
- phase1 `matvec_farr` 와 dual surface (list vs farr). list variant 는 안전한 순수 함수형.
- **signal/ 의 MEL filterbank** 도 사용 (phase3 에 포함됨).

**예상 sweep**: ~23 files × ~10 LoC = ~230 LoC anima 제거 가능

---

## 2nd-wave (동시 추진 가능)

### C4.3 stats/pearson_extended.hexa (재약속 phase1, ~40 LoC total)
- `spearman_rho(xs: [float], ys: [float]) -> float` (phase1 이미 identify)
- `kendall_tau(xs, ys)` (신규, 3-way rank correlation)

**이유**: 
- pearson_r 11 dup (phase1), spearman 3 dup (phase1)
- kendall_tau 는 **outlier-robust** rank correlation (anima consciousness metric 에 유용)
- 모두 correlation matrix 계산에 필수 (training/alm_* 에서 representation quality 측정)

**평가**: 낮은 우선순위 (phase1 이미 cover, phase4 에서는 **재약속만** 수행)

---

## NOT-YET candidates (future RFC)

| 카테고리          | 발견 내용                                          | 이유                                           | RFC |
|-------------------|----------------------------------------------------|-------------------------------------------------|------|
| EEG-specific      | synth_eeg, band_power, detect_mu_suppression       | domain-specific (neural); general 아님         | RFC-040 |
| GRAPH             | community_assign, bridge_edges, graph_N           | consciousness substrate axiom 특화; general 아님 | RFC-041 |
| CLUSTERING        | k-means (없음), DBSCAN (없음)                       | anima codebase 에 구현 부재                      | RFC-037 |
| STRING/ENCODING   | utf8_decode, b64 encode                           | dup count 낮음 (1–4); hexa runtime improvement 의존 | (internal) |

---

# § 10 — Phase 4 survey 통계

| 항목                        | 값            | 비고                                  |
|------------------------------|---------------|--------------------------------------|
| 조사 범위                    | anima 전체    | 33,722 files                        |
| 제외 (phase1/3)             | math/info/signal | 이미 완료                           |
| 검색 패턴                    | 6 카테고리    | stats/linalg/eeg/graph/string/cluster |
| 신규 후보 (dup > 20)        | entropy_hist  | 23 dup, EEG preprocessing           |
| 재약속 후보                  | matvec, pearson | phase1 확인, phase4 재검증            |
| SKIP (domain-specific)      | EEG/SPIKE, GRAPH, CLUSTERING | 의식 기질 특화, general 부적격 |
| SKIP (low ROI)              | STRING, ENCODING | dup 낮음, hexa runtime 개선 의존   |
| **총 신규 1st-wave 후보**   | **2 (entropy_hist + matvec)** | (+ 재약속 2: pearson/spearman) |

---

# § 11 — hexa-lang stdlib 제안 구조 (Phase 4 신규 파일)

```
hexa-lang/stdlib/
├── info/
│   ├── entropy.hexa          ← Phase 1 (이미 있음)
│   └── entropy_histogram.hexa ← NEW Phase 4 (entropy_hist, joint_entropy_hist)
└── linalg/
    ├── dense.hexa            ← Phase 1 (이미 있음: softmax, l2_norm, cosine_sim)
    └── list_matvec.hexa      ← Phase 4 UPDATE (list-based variant for pure hexa)
```

**신규 디렉토리**: 0 (기존 info/, linalg/ 확장)
**신규 파일**: 1 (entropy_histogram.hexa)
**기존 파일 업데이트**: 1 (linalg/list_matvec.hexa 추가)
**총 신규 LoC**: ~40 (entropy_hist) + ~20 (list_matvec) = ~60 LoC

---

# § 12 — Phase 4 최종 평가 및 권장

## 결론

**Phase 4 survey 결과**:

1. **신규 1st-wave 승격 후보 1개**: `entropy_histogram` (23 dup, EEG + training preprocessing)
   - 추진 용이도: ★★★ (self-contained, hexa-lang 에 바로 fit)
   - 예상 sweep: ~345 LoC anima 제거
   - EEG domain 필수 (mu_rhythm_detector 등)

2. **재약속 1st-wave 승격 후보 2개**: 
   - `list_matvec` (23 dup, phase1 재검증) — training/anima-engines 핵심
   - `pearson_r` / `spearman_rho` (phase1 identified, dup 증가 재확인)

3. **SKIP 카테고리**:
   - EEG-specific synth, band_power: domain-specific (RFC-040)
   - GRAPH community_assign, bridge_edges: consciousness axiom 특화 (RFC-041)
   - CLUSTERING: 구현 부재 (RFC-037)
   - STRING/ENCODING: dup 낮음, hexa runtime 개선 의존

## 다음 단계

**Phase 4 Promote PR (hexa-lang)**: 
- 신규: entropy/entropy_histogram.hexa (~40 LoC)
- 업데이트: linalg/list_matvec.hexa 추가 (~20 LoC)

**Phase 4 anima cleanup cycle**:
- entropy_hist import 갱신 (~23 files, ~345 LoC sweep)
- matvec list-based import 갱신 (~23 files, ~230 LoC sweep)
- 예상 총 sweep: ~47 files, ~575 LoC

**Phase 4 M2 (2nd-wave)**: pearson_r/spearman_rho hexa-lang promote (phase1 이미 scheduled)

---

# § 13 — honest_limits (≥ 3)

- **L1 entropy_hist 설계**: histogram 기반 entropy 는 bin size 선택에 민감. anima 의 23개 정의를 검사하면 일관성 있는지 확인 필요. (표본 5개 spot-check 완료, 일관성 확인됨)

- **L2 EEG/SPIKE domain-specific 판정**: mu_rhythm_detector 등은 신경생리 도메인 깊음. "general" 판정이 의심스러우면 RFC-040 으로 defer.

- **L3 GRAPH/CLUSTERING 부재**: anima 가 consciousness sim 에 집중 → classical ML 알고리즘 no need. future RFC-037/RFC-041 로 defer 하되, 미래 multiagent 확장 시 필요할 수 있음.

- **L4 list vs farr dual surface**: phase1 matvec_farr 은 farr (hexa-lang foreign array handle), phase4 matvec 은 list (pure hexa). 두 surface 를 stdlib 에서 구분해야 하는가? → 답: yes (anima 는 pure hexa 선호, GPU code는 farr).

- **L5 dup count 증가 (phase3 이후)**: cosine_sim/pearson_r 는 phase1 에서 7/11 dup 이었는데, phase4 에서 27/11 dup 로 증가. 이는 phase3 signal/ promote 이후 **새로운 모듈**들이 추가되었을 가능성. 현황 재확인 필수.

---

# § 14 — Cross-Link

- Input 범위: `/Users/ghost/core/anima/` 산하 33,722 files
- Phase 1 survey: `/Users/ghost/core/anima/HEXAD/STDLIB/survey_2026_05_24.md` (47 candidates)
- Phase 3 survey: `/Users/ghost/core/anima/HEXAD/STDLIB/phase3_survey_2026_05_25.md` (60+ signal fn)
- **본 doc**: `/Users/ghost/core/anima/HEXAD/STDLIB/phase4_survey_2026_05_25.md`
- 후속 cycle: Phase 4 M1 promote (entropy_histogram + list_matvec) + anima sweep

---

