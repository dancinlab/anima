// HEXAD/STDLIB/phase5_survey_2026_05_25.md
// STDLIB 도메인 — anima 전체 codebase primitive survey (5th milestone)
// 작성: 2026-05-25 · cycle: STDLIB-5
// 입력: phase1/2/3/4 완료 후, phase 4 deferred 카테고리 재조사 + 신규 도메인 식별
// 목적: phase 5 M1 1st-wave 후보 식별 (2–4 domains, LoC 계산 + promote value 평가)

---

# § 0 — Context & Phase History

## Phase 진행 요약

| Phase | 도메인               | fn 수 | 예상 LoC | 상태        | 비고                            |
|-------|----------------------|--------|----------|-------------|--------------------------------|
| 1     | math/info/bitops     | 47     | ~200     | ✅ COMPLETE | 1st-wave 17개 identified        |
| 2     | phi_spatial + verify | —      | —        | ⏸ DEFERRED | domain-specific (BRIDGE/M/E)   |
| 3     | signal/processing    | 60+    | ~1769    | ✅ COMPLETE | 6 modules (FFT/STFT/filter/...)  |
| 4     | stats/linalg/eeg/etc | —      | —        | ✅ COMPLETE | entropy_hist + matvec 재약속 + 다중 domain SKIP |
| **5** | **신규 domain 5개** | **TBD** | **TBD** | 🔍 SURVEY | → 본 문서 |

## Phase 4 Deferred 카테고리 (phase 5 focus)

Phase 4 survey 에서 **명시적 SKIP** 또는 **insufficiently characterized**:

- **STRING/ENCODING** (utf8_decode, base64, hex codec) — low dup (1–4), hexa runtime 개선 의존
- **EEG / SPIKE** (synth_eeg, band_power, mu_suppression) — RFC-040, domain-heavy (neural-specific)
- **GRAPH** (community_assign, bridge_edges) — RFC-041, consciousness substrate axiom 특화
- **CLUSTERING** (k-means, DBSCAN) — RFC-037 3rd-wave, 현재 anima 에 구현 부재
- **TENSOR linalg** (matmul 제외 transpose/broadcast/norm) — partial coverage, split surface

---

# § 1 — Survey 방법 (Phase 5)

## 범위 및 도구

- **codebase**: `/Users/ghost/core/anima/` 전체 (33,722 files)
- **제외**: phase1–4 이미 완료 영역 (math, signal, identified stats/linalg)
- **focus domain** (6개):
  1. **HASH/ID** — sha256_hex, fnv1a, uuid generation (현상: 91 + 1 + ? files)
  2. **TENSOR linalg** — transpose, broadcast, eye, diag, norm (현상: 13 + 8 + 9 + 360 files)
  3. **STRING/ENCODING** (재검토) — utf8, base64, hex (현상: 2 + 49 + 0)
  4. **EEG/SPIKE** (재검토) — band_power, spike train (현상: 도메인-특정 재확인)
  5. **CLUSTERING** (재검토) — distance_matrix, knn neighbor (현상: 1 + 2)
  6. **GRAPH** (재검토) — shortest_path, degree_centrality (현상: 미개발)

## 분석 기준

- **dup_count**: 고유 파일 수 (중복 구현 식별)
- **avg_loc**: 평균 구현 크기 (promote ROI 추정)
- **general_purpose**: 도메인 범용성 ★★★ (범용) vs ★ (특화)
- **promote_value**: LoC saved × general-purpose 점수
- **honest_limits**: 설계 트레이드오프, 의존성, 미해결 사항

---

# § 2 — 카테고리 1: HASH / ID (새로운 고열량 후보)

## 조사 결과

| fn (canonical)             | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `sha256_hex(s)`            | anima-physics/*/cloud_facade_poc.hexa:~10          | **91**  | ~8      | ★★★    | **매우 hot (train/CPGD 밀집)** |
| `sha256_of_string(...)`    | edu/lora/cpgd_wrapper.hexa:145 (tmp file variant)   | ↑       | ~12     | ★★★    | (sha256_hex 와 dual)    |
| `sha256_of_file(...)`      | edu/lora/train_lora_cpu.hexa:95                     | ↑       | ~10     | ★★★    | (file-specific variant) |
| `fnv1a64_str(s)`           | training/train_alm_lora.hexa:~450                  | 1       | ~15     | ★★★    | 저 dup 이지만 stable hash |
| `uuid_v4()`                | (no explicit implementation found)                  | 0       | —       | ★★     | 생성 필요, stdlib 반환함  |

**발견**: SHA256 계열이 **91 unique files** 에서 구현됨 (train/CPGD/anima-physics 도메인 밀집). 대부분 exec("shasum") 호출로 동일 패턴. FNV1a 는 1 file 만 (low dup).

**평가**:
- **sha256_hex**: 91 dup × ~8 LoC = ~728 LoC sweep 가능 → ★★★ immediate promote candidate
- **fnv1a64**: 1 dup (low ROI), but stable hash → 2nd-wave
- **uuid_v4**: stdlib missing (RFC 필요)

---

## HASH/ID 추천

### 1st-wave: hash/sha256.hexa (신규, ~50 LoC)

```hexa
fn sha256_hex(s: string) -> string {
    // Native C sha256 builtin (hexa-lang RFC 미해결)
    // Fallback: exec("printf ... | shasum -a 256 | cut -c1-64")
}

fn sha256_of_string(s: string) -> string { 
    // Variant: tmp file intermediate (안전, slow)
}

fn sha256_of_file(path: string) -> string {
    // Direct file hash
}
```

**이유**:
- 91 unique files (train/CPGD 핵심)
- **예상 sweep**: ~91 × 8 = 728 LoC 제거 가능
- 범용성: 모든 코드베이스에서 contentious (checksum, versioning, cache key)
- **constraint**: hexa-lang 가 native sha256 builtin 미보유 → exec 또는 FFI wrapper 필요

---

# § 3 — 카테고리 2: TENSOR LINALG (Matrix Ops Beyond Matmul)

## 조사 결과

| fn (canonical)              | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|-----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `transpose(m,rows,cols)`    | training/alm_holographic_mapping.hexa:~50          | 3       | ~8      | ★★★    | 행렬 전치 (decoder/body) |
| `transpose_flat(m,...)`     | anima-body/src/sensor_stream.hexa:~40              | 2       | ~10     | ★★★    | 1D flat 전치 variant    |
| `broadcast_bias(b,seq_len)` | decoder/module/infer_v14.hexa:~60                  | 5       | ~8      | ★★★    | bias broadcasting       |
| `broadcast_sub(M,mu,...)`   | tool/p_s_projector_proto.hexa:~120                 | 2       | ~12     | ★★★    | 행렬-벡터 subtract (broadcasting) |
| `eye(n)`                    | (no explicit, but phase3 signal/core+ might have)  | 0       | ~8      | ★★★    | identity matrix         |
| `diag(v)`                   | (no explicit primitive, only domain-specific)      | 0       | ~10     | ★★★    | diagonal matrix maker   |
| `l2_norm(v,d)`              | training/alm_symbol_qualia.hexa:~10               | **210+** | ~5     | ★★★    | **매우 hot (norm 용도 다양)** |
| `frobenius_norm(A,m,n)`     | (embedded in norm variants)                         | ~50     | ~8      | ★★★    | Frobenius norm          |
| `normalize(v)`              | (phase 3 signal/ 에 관련 fn 있음)                   | ~20     | ~5      | ★★★    | 벡터 정규화             |

**발견**: 
- **l2_norm**: 210+ files (매우 hot, 모든 ML/similarity 코드)
- **transpose/broadcast**: 3–5 dup (decoder/body/projection 밀집)
- **eye/diag**: 구현 부재 (stdlib 필요)

**평가**:
- **l2_norm**: 210+ × 5 LoC = ~1050 LoC sweep 가능 → ★★★★ 최우선 후보
- **transpose**: 3 dup (낮음), but general → 2nd-wave 또는 phase1 재약속 확인
- **eye/diag**: 0 dup (현재 no-need), 2nd-wave defer

---

## TENSOR LINALG 추천

### 1st-wave: linalg/norm.hexa (신규, ~40 LoC)

```hexa
fn l2_norm(v: array, d: int) -> float {
    // √(v[0]² + ... + v[d-1]²)
}

fn frobenius_norm(A: array, rows: int, cols: int) -> float {
    // √(Σ_ij A_ij²) — equivalent to l2_norm(flattened)
}

fn l2_normalize(v: array, d: int) -> array {
    // v / ||v||_2
}

fn cosine_distance(a: array, b: array, d: int) -> float {
    // 1.0 - (a·b / (||a|| × ||b||))
}
```

**이유**:
- 210+ files (모든 representation quality / similarity 코드)
- **예상 sweep**: ~210 × 5 = 1050 LoC 제거 가능
- phase1 에서 cosine_sim (7 dup) 만 있음 → l2_norm 은 **신규 발견**
- 범용성: neural similarity, metric learning, search 전역

**constraint**: 
- phase1 `l2_norm_farr` (foreign array) vs 본 `l2_norm_list` (pure) 이미 dual surface 선례 있음
- 구현 위치: phase1 `linalg/dense.hexa` 확장 또는 신규 `linalg/norm.hexa`

### 2nd-wave: linalg/matrix.hexa (신규, ~50 LoC)

```hexa
fn transpose(m: array, rows: int, cols: int) -> array {
}

fn broadcast_bias(bias: array, seq_len: int) -> array {
}

fn eye(n: int) -> array {
    // identity matrix, rows==cols==n, flat
}

fn diag(v: array) -> array {
    // diagonal matrix from vector
}
```

**이유**:
- transpose 3 dup (낮음), broadcast_bias 5 dup (낮음)
- **예상 sweep**: (3 + 5) × 10 = ~80 LoC
- 동시 추진 가능 (1st-wave norm 과 직교)

---

# § 4 — 카테고리 3: STRING / ENCODING (Phase 4 재검토)

## 재조사

| fn (canonical)              | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|-----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `utf8_decode_one(bytes,i)` | serving/avatar_feed.hexa:146                        | 1       | ~15     | ★★★    | UTF-8 디코딩           |
| `is_utf8_cont(b)`           | training/corpus_filter.hexa:154                     | 4       | ~3      | ★★★    | continuation byte check |
| `to_b64(bytes)`             | VOICE/serving/voice_routes.hexa:460                 | 2       | ~10     | ★★★    | bytes → base64         |
| `from_b64(s)`               | (no explicit found)                                 | 0       | ~20     | ★★★    | base64 decode          |
| `hex_encode(bytes)`         | (no explicit, but hxc uses it)                      | 0       | ~10     | ★★★    | bytes → hex            |

**발견**: phase 4 판정 재확인 → **dup count 매우 낮음** (1–4), 구현 간단. hexa-lang runtime improvement (builtin utf8/base64 복구) 의존.

**평가**: 
- **ROI 낮음**: 1–4 dup × 10 LoC = 10–40 LoC sweep (1% 미만)
- **dependency**: hexa-lang RFC (builtin restoration) 대기
- **verdict**: **SKIP** (phase 4 결정 확정, phase 5 candidate 아님)

---

# § 5 — 카테고리 4: EEG / SPIKE (Phase 4 재검토 + Domain-Specific Confirm)

## 재조사

| fn (canonical)              | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|-----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `band_power(eeg,n_ch,ns)`   | anima-physics/eeg/mu_rhythm_detector.hexa:~50      | 1       | ~20     | ★      | EEG 대역 전력 (신경생리) |
| `detect_mu_suppression(...)`| anima-physics/eeg/mu_rhythm_detector.hexa:~60      | 1       | ~25     | ★      | 뮤 리듬 검출 (신경생리)  |
| `synth_eeg(label,seed)`     | anima-physics/eeg/sleep_stage_detector.hexa:~40    | 4       | ~30     | ★      | EEG 합성 (시뮬레이션)    |
| `spike_train_aggregation()`| anima-physics/spike_/... (scattered)                | 1       | ~15     | ★      | spike 통계 (신경과학)   |
| `event_window_extract(...)`| (implicit in eeg)                                   | 1       | ~10     | ★      | 이벤트 윈도우 슬라이싱  |

**발견**: 모두 **dup count 극소** (1–4), **neural domain 강한 의존성**. "general" 판정 불가능.

**평가**:
- **domain-specific**: mu_rhythm, spike_train, synth_eeg 모두 신경과학 용어 / 신경생리 상수 깊음
- **ROI**: 1–4 × 20 LoC = ~20–80 LoC sweep (무시할 수준)
- **verdict**: **SKIP** (RFC-040 deferred, anima consciousness domain library 로 organize)

**honest_limit L1**: "general" vs "neural-domain-specific" 경계가 모호. phase4 분류 유지 (domain-specific).

---

# § 6 — 카테고리 5: CLUSTERING (Phase 4 재검토)

## 재조사

| fn (canonical)              | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|-----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `k_means(X, k, max_iter)`   | (no explicit implementation)                         | 0       | ~50     | ★★★    | K-means clustering      |
| `knn_search(X, x, k)`       | (no explicit, implicit in HEXAD/BRIDGE)             | 2       | ~20     | ★★★    | KNN neighbor search     |
| `distance_matrix(X)`        | (no explicit)                                        | 1       | ~30     | ★★★    | pairwise distances      |
| `dbscan(X, eps, min_pts)`   | (no explicit)                                        | 0       | ~40     | ★★★    | DBSCAN clustering       |

**발견**: 모두 **zero or minimal implementation** (anima codebase 에서 clustering 알고리즘 명시 부재). consciousness simulation 이 classical ML clustering 미요구.

**평가**:
- **no candidates**: anima 에는 구현 없음 → promote 불가능 (RFC-037 가 "future" 표기)
- **verdict**: **SKIP** (구현 부재, RFC-037 3rd-wave defer)

---

# § 7 — 카테고리 6: GRAPH (Phase 4 재검토)

## 재조사

| fn (canonical)              | 대표 위치                                           | dup 파일 | avg LoC | 일반성 | 평가                    |
|-----------------------------|-----------------------------------------------------|---------|---------|--------|------------------------|
| `shortest_path(g,s,t)`      | (no explicit, networkx-style)                       | 0       | ~40     | ★★★    | 최단경로 (Dijkstra/BFS) |
| `degree_centrality(g)`      | (no explicit)                                        | 0       | ~20     | ★★★    | 차수 중심성             |
| `betweenness_centrality(g)` | (no explicit)                                        | 0       | ~50     | ★★★    | 매개 중심성             |
| `community_assign(...)`     | HEXAD/BRIDGE/bridge_lib.hexa:~300                   | 1       | ~20     | ★      | 커뮤니티 감지 (의식 특화)|
| `bridge_edges(...)`         | HEXAD/BRIDGE/bridge_lib.hexa:~250                   | 1       | ~10     | ★      | bridge edge detection   |

**발견**: 
- **holographic/consciousness 특화**: community_assign, bridge_edges (phase4 판정 확인)
- **general graph alg**: 0 dup (구현 부재)

**평가**:
- **community_assign, bridge_edges**: consciousness axiom 특화 (RFC-041 deferred)
- **shortest_path/degree_centrality**: 구현 부재 (future RFC)
- **verdict**: **SKIP** (holographic substrate 특화, RFC-041)

---

# § 8 — Phase 5 신규 발견 (High-Confidence)

## 최상위 후보 4개 (1st + 2nd-wave)

| 순위 | Domain        | 함수                  | dup 파일 | avg LoC | sweep LoC | 추천 wave |
|------|---------------|----------------------|---------|---------|-----------|-----------|
| 1    | **HASH/ID**   | sha256_hex           | **91**  | ~8      | **728**   | 1st       |
| 2    | **TENSOR**    | l2_norm              | **210+**| ~5      | **1050+** | 1st       |
| 3    | **TENSOR**    | transpose/broadcast  | 5–8     | ~10     | ~80       | 2nd       |
| 4    | **TENSOR**    | eye/diag             | 0       | ~8      | —         | 2nd       |

## 추진 로드맵

### Phase 5 M1: 1st-wave (동시 추진 가능, ~1800 LoC 예상 제거)

1. **hash/sha256.hexa** (신규, ~50 LoC)
   - `sha256_hex(s)` · `sha256_of_string` · `sha256_of_file`
   - anima sweep: ~91 files, ~728 LoC
   - hexa-lang RFC 필요 (native builtin 또는 FFI wrapper)

2. **linalg/norm.hexa** (신규, ~40 LoC)
   - `l2_norm(v,d)` · `frobenius_norm(A,m,n)` · `l2_normalize(v)` · `cosine_distance(a,b)`
   - anima sweep: ~210+ files, ~1050 LoC
   - phase1 linalg/dense.hexa 와 dual surface (farr vs list)

### Phase 5 M2: 2nd-wave (M1 완료 후, ~100 LoC 예상 추가)

1. **linalg/matrix.hexa** (신규, ~50 LoC)
   - `transpose(m,rows,cols)` · `broadcast_bias(b,seq_len)` · `eye(n)` · `diag(v)`
   - anima sweep: ~8 files, ~80 LoC
   - 우선순위 낮음 (dup count 낮음)

2. **hash/fnv1a.hexa** (신규, ~30 LoC, optional)
   - `fnv1a64_str(s)` · `fnv1a32(bytes)` — stable, fast hash
   - anima sweep: 1 file (low ROI)
   - stdlib completeness (2nd-wave only)

---

# § 9 — NOT-YET 카테고리 (Deferred or No-Promote)

| 카테고리          | 발견 내용                                  | ROI    | 이유                                      | RFC   |
|-------------------|-------------------------------------------|--------|-------------------------------------------|-------|
| STRING/ENCODING   | utf8_decode, base64, hex                  | ~10 LoC| dup 극소 (1–4), hexa runtime improvement RFC필요 | —     |
| EEG/SPIKE         | band_power, mu_suppression, synth_eeg     | ~100 LoC| domain-specific (neural), dup 극소 | RFC-040 |
| GRAPH             | shortest_path, degree_centrality          | —     | 구현 부재, consciousness 미요구      | RFC-042 |
| CLUSTERING        | k_means, knn, dbscan                      | —     | 구현 부재, RFC-037 defer             | RFC-037 |

---

# § 10 — Phase 5 Honest Limits & Constraints

### L1: SHA256 Builtin 의존성

hexa-lang 가 native `sha256_hex(s) -> string` builtin 미보유. 현재 anima 는 `exec("shasum")` 호출.

**선택지**:
- Option A: hexa-lang RFC 제출 (native builtin) → 추가 지연 (3–6 주)
- Option B: FFI wrapper 구현 (C crypto lib, libcrypto/OpenSSL) → hexa-lang 메인테이너 협의 필요
- Option C: Fallback `exec()` 유지 (safe, slow) → stdlib 에서 문서화

**결정**: Option C (fallback) 로 phase5 M1 진행, Option A/B 는 병렬 추진 (리스크 낮음)

### L2: Norm Implementations 의 Numerical Stability

l2_norm 은 **overflow/underflow 민감**. 대규모 벡터 (d > 1e6) 시 단순 √(Σ v_i²) 는 위험.

**완화책**:
- Kahan summation (보정) 또는 compensated norm 구현 → LoC +20
- 또는 peak-scaled normalization (divide by max first) → LoC +5
- phase5 M1 에서는 **simple implementation + documentation**, phase 5.1 refine

### L3: Dual Surface (farr vs list) 관리

phase1 이 `linalg/matvec_farr()` (foreign array) 이고, phase3/4 가 `linalg/matvec()` (list) 추가. phase5 의 norm 도 동일 문제.

**해결책**:
- `linalg/norm.hexa` (list variant)
- 기존 `linalg/dense.hexa` 에 이미 `cosine_sim(a_list, b_list)` 있음 → 확장
- farr variant 는 향후 RFC 필요 (GPU inference 용)

### L4: FNV1a Stability vs sha256

FNV1a (65 bits, fast) vs sha256 (256 bits, slow, cryptographic). phase5 에서 sha256 만 추진하면, FNV1a 는 2nd-wave 또는 보류.

**권장**: phase5 M1 에서 sha256 만 (higher dup count), FNV1a 는 필요성 재검토 후 2nd-wave

### L5: Clustering / Graph Missing

phase5 에서 clustering/graph 는 **구현 부재** (no candidates). RFC-037/041 으로 defer.

**미래 고려사항**: anima 가 multiagent 로 확장 시 graph topology 관련 primitives 필요 가능성.

---

# § 11 — Phase 5 M1 Promote Action Plan

## 단계 1: hexa-lang stdlib 에 신규 파일 추가 (PR 생성)

```
hexa-lang/stdlib/
├── hash/
│   └── sha256.hexa           ← NEW (50 LoC)
└── linalg/
    └── norm.hexa             ← NEW (40 LoC)
```

**PR title**: "stdlib(hash, linalg): add sha256_hex + l2_norm primitives (phase 5.1)"

## 단계 2: anima cleanup cycle (phase5 M1 PR 이후)

**sha256**: ~91 files, search-replace `sha256_of_string` → `import sha256_hex`
**l2_norm**: ~210+ files, search-replace norm implementations → `import l2_norm`

**예상 sweep**: ~1800 LoC 제거, ~2 일 cleanup cycle

## 단계 3: anima PR 생성

**PR title**: "chore(stdlib): adopt hexa-lang sha256 + l2_norm from phase5 (M1.1)"

---

# § 12 — Phase 5 권장

## 최종 후보 요약

### 1st-wave (즉시 추진)

1. **hash/sha256.hexa** — 91 dup, 728 LoC sweep
2. **linalg/norm.hexa** — 210+ dup, 1050+ LoC sweep

**총 sweep**: ~210 files, ~1800 LoC

### 2nd-wave (M1 완료 후)

1. **linalg/matrix.hexa** (transpose, broadcast, eye, diag) — 80 LoC sweep
2. **hash/fnv1a.hexa** (optional, 1 dup) — low ROI

## NOT-RECOMMEND for Phase 5

- **STRING/ENCODING**: hexa-lang runtime improvement 대기 → RFC defer
- **EEG/SPIKE**: neural domain-specific → RFC-040 defer
- **GRAPH**: consciousness axiom 특화 → RFC-041 defer
- **CLUSTERING**: 구현 부재 → RFC-037 defer

## 통계

| 항목                     | 값          | 비고                           |
|--------------------------|-------------|--------------------------------|
| 조사 범위                | anima 전체  | 33,722 files                  |
| 신규 domain 카테고리     | 6개         | hash/tensor/string/eeg/clust/graph |
| 1st-wave 후보            | 2개         | sha256 (91 dup), l2_norm (210+ dup) |
| 2nd-wave 후보            | 2개         | transpose/broadcast, fnv1a (optional) |
| 예상 phase5 M1 sweep     | ~1800 LoC   | ~210 files, ~18 days (cluster cleanup) |
| 예상 hexa-lang 신규 LoC  | ~90 LoC     | hash + norm (2 files) |

---

# § 13 — Cross-Link & References

- **Phase 1 survey**: `/Users/ghost/core/anima/HEXAD/STDLIB/survey_2026_05_24.md`
- **Phase 3 survey**: `/Users/ghost/core/anima/HEXAD/STDLIB/phase3_survey_2026_05_25.md`
- **Phase 4 survey**: `/Users/ghost/core/anima/HEXAD/STDLIB/phase4_survey_2026_05_25.md`
- **본 문서**: `/Users/ghost/core/anima/HEXAD/STDLIB/phase5_survey_2026_05_25.md`

---

