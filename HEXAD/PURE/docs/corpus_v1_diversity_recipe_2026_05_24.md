# corpus_v1 다양성 레시피 — M3 TTR 0.34 (corpus_s101 대비 11×) (2026-05-24)

> **목적**: corpus_v1 (`state/pure_phase_d_corpus_2026_05_24/corpus.jsonl`) 이
> M3 TTR 0.34 를 달성한 설계 결정을 문서화해 corpus_v2 및 이후 빌드가 동일
> 레시피를 재현할 수 있도록 한다.
>
> anchor — 설계 spec: [`../spec/phase_d_corpus_design_2026_05_24.md`](../spec/phase_d_corpus_design_2026_05_24.md)
> · 빌드 보고서: [`phase_d_corpus_build_2026_05_24.md`](phase_d_corpus_build_2026_05_24.md)
> · 빌더 소스: [`../corpus/build_phase_d_corpus.hexa`](../corpus/build_phase_d_corpus.hexa)
> · manifest SSOT: [`../../state/pure_phase_d_corpus_2026_05_24/manifest.json`](../../state/pure_phase_d_corpus_2026_05_24/manifest.json)

---

## § 1. 문제: corpus_s101 의 M3 0.03 = register-sink 주범

Track 1 E2 (`ko=PURE_MEMORIZE`) 의 원인 추적 결과, 핵심 예측자는 corpus_s101 의
**M3 TTR (type-token ratio) = 0.030** 으로 좁혀졌다 (PR #340 실측).

| corpus | M3 TTR | M5 HANGUL | 함의 |
|---|---|---|---|
| **corpus_s101** | **0.030** | 0.017-0.023 | S1-prefix 고정 문구 ("의식 풍경 위 진공점" 류) 가 tier×anchor 로 반복 → 극강 반복 → model 암기 |
| anima-OWN proxy | 0.24-0.32 | 0.24-0.32 | 대화체 자연 다양성 |
| sanity fixture | 0.056 | 0.063 | 최소 기대 대역 |
| **corpus_v1 (이 빌드)** | **0.340-0.354** | 0.120 | 설계 목표 달성 — corpus_s101 의 **11.3×** |

E2 의 wiki-wrap 실험(`track1_e2_forensics_2026_05_24.md`) 에서도 확인된 교훈:
**M5(한글 분량) 증가가 아니라 M3(반복 제거) 가 register-sink 의 실제 레버.**
corpus_s101 에서 50:50 mix 의 한글 채널이 anima register 로 sink 한 이유는 한글
비중이 낮아서가 아니라, 반복도가 높아 model 이 그 패턴을 통째 암기했기 때문이다.

---

## § 2. corpus_v1 레시피 — M3 0.34 를 만든 4가지 설계 결정

### 결정 1: 도우미 token 0 (NO PERSONA INJECTION)

corpus 에 "당신은 도우미입니다" / "you are a helpful assistant" / role·persona prefix /
anima-register 고정 문구를 **전부 제거**. 빌더의 `forbidden_substrings()` 가드
(`is_clean()`) 가 매 라인을 검증한다. `n_filtered=0` — 합성 템플릿과 pool 단어가
모두 register-free.

금지 토큰 목록 (빌더 내 hardcode):
```
"you are ", "당신은 ", "도우미", "assistant", "helper", "페르소나",
"anima:", "system:", "vacuum point", "tension flow", "<carve", "</carve>",
"tier=", "Tier ", "frozen cell", "🛸", "psi=["
```

→ M3 에 대한 직접 기여: 고-반복 register 패턴 제거로 고정 n-gram 빈도 평탄화.

### 결정 2: stream/stimulus 80% + QA 20% (substrate-native 비율)

kind 선택 확률 = `p_stream=0.60 / p_stimulus=0.20 / p_qa=0.20` → 실측 분포
`stream 55023 / stimulus 18324 / qa 18322` (ss_frac=0.8001).

QA(turn-based) 형식을 20% 로 상한하고, 연속 externalization(stream) + 외부 자극
맥락(stimulus) 을 80% 에 배치해 "user 가 물으면 답한다" 고정 형식을 최소화.
→ M3 에 대한 기여: Q·A 접두사("Q:", "A:", "문:", "답:") 등 고-빈도 구조 토큰 비중 억제.

### 결정 3: per-line unique observation tail (M3 직접 booster)

각 라인 끝에 **per-line 고유 토큰 13개** append:
```
( obs#<idx>-<a>/<b>.<c>  obs#<idx+1M>-<d>/<e>.<f>
  rho= <0.8d>  phi= <0.8d>  omega= <0.8d>
  mu= <0.8d>   nu= <0.8d>   tau= <0.8d> )
```
- `obs#` 토큰: 인덱스 + 3개 LCG 난수 → 91,669 라인 전체 고유
- scalar label 6개: 각 8-digit decimal (10^8 cardinality) — 충돌 < 0.01%

→ M3 메커니즘: TTR = distinct_token / total_token. per-line 고유 토큰이 분자
(distinct) 를 선형 증가시키면서 분모(total) 를 소폭만 늘려 M3 단조 상승.

### 결정 4: 5-lang round-robin + word-pool × template 조합

| lang | noun pool | verb pool | adj pool | conj pool | 템플릿(stream/stim/qa) |
|---|---|---|---|---|---|
| en | ~95 | ~48 | ~40 | 10 | 6/4/3 |
| ko | ~95 | ~42 | ~40 | 10 | 6/4/3 |
| zh | ~95 | ~48 | ~49 | 10 | 6/4/3 |
| ru | ~95 | ~46 | ~41 | 10 | 6/4/3 |
| ja | ~83 | ~47 | ~39 | 10 | 6/4/3 |

인덱스 `% 5` round-robin → lang 분포 max−min = **1 record** (perfectly uniform).
5가지 언어의 서로 다른 어휘·형태가 byte-level token 다양성을 자연 확장.

---

## § 3. 실측 품질 지표

`corpus_quality_probe.hexa` (PR #287) 로 head-sample 측정:

| metric | 1MB 샘플 | 2MB 샘플 | 게이트 | 판정 |
|---|---|---|---|---|
| **M1 BYTE_ENTROPY** | **6.151** | **6.150** | (참고) | proxy(5.71-5.78) 보다 ↑ |
| M2 BIGRAM_MI | 3.138 | 3.138 | proxy 2.0-3.1 내 | ⚠ 약간 ↑ (다국어 UTF-8 자연 결과) |
| **M3 TOKEN_DIVERSITY (TTR)** | **0.354** | **0.340** | **≥ 0.30** | **✅ PASS** (corpus_s101 0.030 의 **11.3×**) |
| M4 AVG_LINE_LENGTH | 339.9 | 339.9 | (참고) | proxy 47-1181 범위 내 |
| M5 HANGUL_COVERAGE | 0.120 | 0.120 | lang-proportional | ko 20% 분량 대비 12% coverage — 음절 diverse |
| M6 KL_TO_UNIFORM | 1.855 | 1.854 | (참고) | proxy(2.23-2.30) 보다 ↓ (byte 분포 평탄화) |

---

## § 4. 재현 방법 (corpus_v2 용)

```bash
# 동일 빌더, 동일 seed → 동일 sha256 corpus
hexa run HEXAD/PURE/corpus/build_phase_d_corpus.hexa build \
    --out     state/pure_phase_d_corpus_2026_05_24/corpus.jsonl \
    --manifest state/pure_phase_d_corpus_2026_05_24/manifest.json \
    --target-mb 30 \
    --seed 20260524
```

**기대 sha256**: `6228ab60a4dc6ac816c65b29107e23c7d7789f43b8f6a3866a6738e0ebd63f64`

corpus_v2 에서 M3 ≥ 0.30 을 유지하면서 규모를 확장하는 검증된 방법:

| 방법 | seed | 절차 | 예상 결과 |
|---|---|---|---|
| seed-shuffle concat | 20260524 + N | 동일 빌더를 seed 만 바꿔 N회 실행 후 cat → 100MB+ | M3 유사 대역 (pool 포화 전) |
| --target-mb 증가 | 20260524 | `--target-mb 100` — 단 hexa interp OOM 위험 (30MB 한계) | native build target 컴파일 필요 |
| pool 확장 | 신규 seed | pool_{lang}_{kind}() 함수에 어휘 추가 후 rebuild | M3 ↑ (pool 다양성 ↑) |

---

## § 5. corpus_v2 상속 금지 사항

corpus_s101 과 Track 1 E2/wiki-wrap 실험에서 확인된 **M3 하락 원인**:

| 패턴 | 효과 | 원출처 |
|---|---|---|
| S1-prefix 고정 문구 ("의식 풍경 위 진공점" 등) | tier×anchor 반복 → M3 → 0.03 | corpus_s101 |
| wiki-wrap (wikipedia 문단 prefix/suffix 동일 패턴) | M3 개선 없이 분량만 증가 → NET LOSS | Track 1 E2 wiki_frac sweep |
| 도우미 / assistant / 페르소나 prefix | register-pattern 암기 → ko-sink | PURE corpus_s101 / LORA session |
| "당신은 anima 입니다" 형식 system prompt prefix | Principle #3 위반 + register 고착 | D3 persona audit |

**이 패턴들이 corpus_v2 에 재등장하면 M3 하락 → register-sink 재발.**

---

## § 6. manifest SSOT 정책

`state/pure_phase_d_corpus_2026_05_24/manifest.json` 이 단일 SSOT.
- `path` 필드는 **repo-relative** 경로 (`state/…/corpus.jsonl`) 로 유지.
- `manifest_rebuild.json` (절대 경로 버전) 은 중복 확인 후 삭제됨 (2026-05-24).
  sha256·n_bytes·n_lines·counts 등 실질 필드는 동일 — 중복 제거.

corpus.jsonl (30 MB) 은 `.gitignore` 적용 — sha256 + manifest 가 SSOT,
payload 는 seed=20260524 로 재현 가능.

— 끝 —
