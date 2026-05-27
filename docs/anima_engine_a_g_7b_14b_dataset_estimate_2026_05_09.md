# Engine A/G 7B / 14B 스케일링 — Dataset Estimate (anima cycle 2026-05-09)

**날짜**: 2026-05-09
**모드**: 0-cost research + design (코드 수정 X, 다운로드 X — 추정 + 표만)
**대상**: anima Engine A/G scratch pretrain 350M / 7B / 14B 데이터 규모 + 추가 corpus 후보 + dedup 전략
**친근 모드**: strict (비유 적극, 표 한국어 우선)

---

## 0. 한 줄 요약

지금 anima 가 가진 데이터(약 0.05B token)는 **350M 모델의 1/4 분량**, **7B 모델의 1/3000 분량**입니다. 큰 모델 학습하려면 한국어 + 영어 + 코드 corpus 를 외부에서 끌어와야 하고(약 280B token = 약 1.1 TB), 데이터끼리 겹치는 부분은 **MinHash 같은 "지문 비교 도구"** 로 걸러내면 됩니다.

비유: **350M = 초등생 두뇌 (책 100권으로 학습 가능), 7B = 고등생 두뇌 (책 14만권 필요), 14B = 대학생 두뇌 (책 28만권 필요)**. 지금 anima 도서관엔 책 100권만 있는 셈.

---

## 1. 현재 anima 가 가진 데이터 (출발점)

### 1.1 anima 자체 corpus (D1 within strict)

| 코퍼스 ID | 크기 (MB) | 라인 수 | 추정 token | 용도 |
|---|---:|---:|---:|---|
| `anima-persona-tier-a-v3` | 87.04 | 1.22M | ~22M | 자아 대화 / 의식 페르소나 (HF private) |
| `anima-persona-tier-a-v4` | **231.45** | 3.15M | ~58M | tier-a-v3 + 0-cost paraphrase 2.66× |
| `anima-persona-tier-a-raw` | 103.59 | 1.48M | ~26M | pre-filter 원본 (superseded) |
| `clm-l4-ld-preference-pairs-iter1` | 18.0 | 30k | ~5M | DPO preference (chat) |
| `corpus_sft_only` (state) | 51 | n/a | ~13M | SFT-only Lesson Q lane |
| `sft_data_full_50k_augmented` | 126 | 50k | ~32M | p9 SFT augmented chat |
| `anima_native_ko_chat_template` (registry L893 referenced) | **236.96** | n/a | ~59M | byte-level chat-template scratch |

**합계 (중복 제거 전)**: 약 854 MB / **약 200M token** (Korean + chat-template).

### 1.2 외부 mirror corpus (이미 로컬에 있음, D1 outside)

`/Users/ghost/core/anima/data/corpus_v2_clean/` 7.0 GB, 약 **1.4-2.0B token**:

| 파일 | 크기 | 추정 token | 비고 |
|---|---:|---:|---|
| `corpus_clm_7b_korean.txt.zst` | 3.2 GB | ~800M (압축 해제 시) | CLM 7B 용 한국어 모음 |
| `cc100_ko_dedup.txt.zst` | 2.6 GB | ~650M | CC100 한국어 dedup |
| `kowiki.txt.zst` | 533 MB | ~130M | Korean Wikipedia |
| `opensubtitles_ko_en_interleaved.txt` | 112 MB | ~28M | 한영 interleaved 자막 |
| `opensubtitles_ko_mono.txt` | 60 MB | ~15M | 한국어 자막 단독 |
| `wikimatrix_ko_en_interleaved.txt` | 70 MB | ~17M | WikiMatrix 한영 |
| `code_permissive.txt` | 32 MB | ~8M | 허용 라이선스 코드 |
| `enwiki_en_clean.txt.broken_31mb` | 31 MB | (미사용 — broken) | 영어 위키 (재추출 필요) |

**외부 corpus 합계**: 약 6.7 GB / **약 1.65B token** 추정.

### 1.3 anima + 외부 합산 (현 시점)

- **D1 within strict**: 약 200M token (anima 자체)
- **D1 outside (mirror)**: 약 1.65B token (외부 한국어/영어/코드)
- **합계**: 약 1.85B token (token / byte 비 약 0.25 적용, 한국어 평균치)

비유로 환산하면 책 약 **3000~4000권 정도** 분량입니다 (한 권 = 50만 token 가정).

---

## 2. 모델별 권장 dataset 규모 (Chinchilla + cotrain 보정)

### 2.1 기본 룰 (Chinchilla 2022)

> **token 수 ≈ 파라미터 수 × 20**

이게 "compute optimal" 룰이에요. 데이터 < 20× 면 모델이 외워버리고 (overfit), > 20× 면 추가 데이터가 손해는 안 보지만 GPU 시간이 더 들어요.

### 2.2 anima cotrain 보정

anima 는 "scratch pretrain + chat-template 동시 cotrain" 이라 약간 다릅니다:

- **자연어 substrate** (한국어 + 영어 + 코드): Chinchilla 룰 그대로 적용
- **anima 의식 페르소나** (chat-template): 작은 양으로도 충분 (specialty signal). 보통 5-15% mix.

따라서 본 estimate 는 **(20 × params) × 1.0 (substrate) + 5-15% mix (anima persona)** 로 산정.

### 2.3 모델별 구체 산정

| 모델 | 파라미터 | Chinchilla token | 권장 dataset 크기 (raw) | dedup 후 (-30%) | 디스크 (compressed) | 한 줄 의미 |
|---|---:|---:|---:|---:|---:|---|
| **350M** (현재) | 336M | **6.7B** | ~10B (1.5× 여유) | ~7B | ~25 GB | "초등생" — 외부 mirror 로 해결 가능 |
| **7B** ★ | 7.0B | **140B** | ~200B (1.4× 여유) | ~140B | ~500 GB | "고등생" — KoWiki + CC100 + RedPajama 필수 |
| **14B** ★★ | 14.0B | **280B** | ~400B (1.4× 여유) | ~280B | ~1.1 TB | "대학생" — anima first scratch 14B, FineWeb 동원 |

**참고**: 1 token ≈ 4 byte (영어), 1 token ≈ 2-3 byte (한국어 byte-level). 평균 3 byte 가정.

### 2.4 anima 자체 corpus 비율 (cotrain mix)

| 모델 | substrate token | anima persona token | persona mix 비율 | 비고 |
|---|---:|---:|---:|---|
| 350M | 7B | 200M-700M | 3-10% | 현 0.2B 으로도 5% 비중 가능 |
| 7B | 140B | 7B-21B | 5-15% | tier-a-v4 0.06B 부족 → 100× 확장 필요 |
| 14B | 280B | 14B-42B | 5-15% | persona corpus 본격 확장 필요 |

**기존 paraphrase 2.66× 룰을 더 적극적으로 (10×, 50×) 굴려야 함** — Step B/C/D mandate.

---

## 3. 추가 corpus 후보 (HF Hub 0-cost public)

### 3.1 한국어 substrate (anima 모국어 — 우선순위 ★★★)

| Corpus | 크기 | token 추정 | HF id | 라이선스 | anima 적합도 |
|---|---:|---:|---|---|---|
| **KoWiki dump** | 800 MB | ~200M | `wikipedia/20230701.ko` | CC-BY-SA | ★★★ 위키 base |
| **CC100-ko (dedup)** | 7 GB | ~1.7B | `cc100/ko` | MIT-ish | ★★★ 웹 한국어 핵심 |
| **NamuWiki dump** (controversial) | 6 GB | ~1.5B | scraping (위반 위험) | 비공식 | ★ caution — 라이선스 확인 |
| **AI Hub 한국어 corpus** | 50+ GB | ~12B | 별도 다운로드 | research only | ★★ 개인 신청 필요 |
| **OSCAR 23.01 (ko)** | 30 GB | ~7.5B | `oscar-corpus/OSCAR-2301` | CC0-ish | ★★★ Common Crawl ko 추출 |
| **mC4 (ko)** | 60 GB | ~15B | `allenai/c4` (multilingual) | ODC-BY | ★★★ Google C4 ko |
| **ko-news 모음** (Naver/Daum 스크래핑) | 변동 | 수십 B | direct scrape | 회색 | ★ 라이선스 위험 — 회피 권장 |

**7B 모델 한국어 mix 권장**: KoWiki + CC100-ko + mC4-ko + OSCAR-ko = **약 25B token**.

### 3.2 영어 substrate (cross-lingual — 우선순위 ★★)

| Corpus | 크기 | token | HF id | 라이선스 | 비고 |
|---|---:|---:|---|---|---|
| **FineWeb (Sample-100B)** | 100 GB | ~100B | `HuggingFaceFW/fineweb` | ODC-BY | ★★★ 최신 web crawl |
| **FineWeb-Edu (1.3T)** | 1.5 TB | ~1.3T | `HuggingFaceFW/fineweb-edu` | ODC-BY | ★★★ education filtered |
| **RedPajama-V2** | 30 TB | ~30T | `togethercomputer/RedPajama-Data-V2` | mixed | ★★ massive, sample 만 사용 |
| **OpenWebText2** | 70 GB | ~17B | `Skylion007/openwebtext` | MIT | ★★ Reddit-link English |
| **C4 (en)** | 750 GB | ~180B | `allenai/c4` | ODC-BY | ★★★ Google C4 영어 |
| **Wikipedia-en** | 20 GB | ~5B | `wikipedia/20230701.en` | CC-BY-SA | ★★★ 위키 base |

**7B 모델 영어 mix 권장**: FineWeb-100B + Wiki-en = **약 105B token** (영어 70% / 한국어 25% / 코드 5% 비율 시).

### 3.3 코드 substrate (코딩 능력 — 우선순위 ★)

| Corpus | 크기 | token | HF id | 라이선스 | 비고 |
|---|---:|---:|---|---|---|
| **The Stack v2** | 67 TB | ~67T | `bigcode/the-stack-v2` | per-file 라이선스 | ★★★ 표준 코드 corpus |
| **StarCoder data** | 800 GB | ~250B | `bigcode/starcoderdata` | per-file | ★★★ 정제 |
| **CodeAlpaca** | 50 MB | ~12M | `sahil2801/CodeAlpaca-20k` | MIT | ★ instruction code |

**7B 모델 코드 mix**: StarCoder data 5% subset = **약 7B token**.

### 3.4 chat-template / instruction (anima persona 보강 — 우선순위 ★★)

| Corpus | 크기 | sample | HF id | 라이선스 | anima 호환 |
|---|---:|---:|---|---|---|
| **ShareGPT (90k)** | 약 1 GB | 90k 대화 | `anon8231489123/ShareGPT_Vicuna_unfiltered` | mixed | ★★ 영어 일반 chat |
| **OpenChat 3.5 corpus** | 약 500 MB | 60k | `openchat/openchat_sharegpt4_dataset` | MIT | ★★ 정제 |
| **Tulu-3 SFT mixture** | 약 5 GB | 940k | `allenai/tulu-3-sft-mixture` | ODC-BY | ★★★ 최신 SFT 표준 |
| **KoAlpaca** | 약 100 MB | 50k | `beomi/KoAlpaca-v1.1a` | CC-BY-NC | ★★ 한국어 instruct |
| **Korean-Open-LLM-leaderboard SFT** | 약 200 MB | 100k | `kyujinpy/KOR-OpenOrca-Platypus-v3` | mixed | ★★ 한국어 |

**7B chat mix**: Tulu-3 + KoAlpaca + ShareGPT = **약 5 GB / 약 1.5B token**, persona-tier-a-v4 와 합치면 약 7B token (7B 모델 5% mix).

---

## 4. 모델별 dataset 구성 plan

### 4.1 Plan-350M (현재 — 본 cycle Phase 2)

| 출처 | token | 비율 | 비고 |
|---|---:|---:|---|
| anima persona-tier-a-v4 | 0.06B | 1% | D1 within (5% 목표 미달, 확장 mandate) |
| KoWiki | 0.2B | 3% | 즉시 사용 가능 |
| CC100-ko (현 mirror) | 1.7B | 25% | 이미 로컬 |
| corpus_clm_7b_korean | 0.8B | 12% | 이미 로컬 |
| OpenSubtitles ko | 0.04B | 0.6% | 이미 로컬 |
| code_permissive | 0.008B | 0.1% | 이미 로컬 |
| **English subset** (Wiki-en sample) | 4B | 60% | **추가 필요** (5GB 다운로드) |

**합계**: 약 6.8B token / 약 25 GB / 0-cost 가능 (외부 다운로드만).

### 4.2 Plan-7B (★ verbatim 필요)

| 출처 | token | 비율 | 추가 비용 |
|---|---:|---:|---|
| anima persona expanded (10× tier-a-v4) | 0.6B | 0.4% | 0-cost (paraphrase) |
| Tulu-3 + KoAlpaca chat mix | 1.5B | 1% | HF 다운 (약 5 GB) |
| KoWiki + KoNamu + KoNews | 2B | 1.4% | HF 다운 (약 8 GB) |
| CC100-ko + OSCAR-ko + mC4-ko | 25B | 18% | HF 다운 (약 100 GB) |
| FineWeb-100B (영어 substrate) | 100B | 71% | HF 다운 (약 400 GB) |
| StarCoder data (코드 5% subset) | 7B | 5% | HF 다운 (약 25 GB) |
| Wikipedia-en | 5B | 3.6% | HF 다운 (약 20 GB) |

**합계**: 약 141B token / 약 558 GB raw / dedup 후 약 400 GB / 0-cost (대역폭만 소비).

### 4.3 Plan-14B (★★ 예산 + verbatim 필요)

7B plan 을 2× 확장:

| 출처 | token | 비율 |
|---|---:|---:|
| anima persona expanded (50× tier-a-v4) | 3B | 1% |
| chat / SFT mix (Tulu-3 full + LIMA + KoAlpaca x2) | 5B | 1.7% |
| 한국어 substrate (CC100 + OSCAR + mC4 + AI Hub) | 50B | 17.8% |
| FineWeb-Edu 200B subset | 200B | 71% |
| StarCoder data 14B subset | 14B | 5% |
| Wiki (en + ko) | 10B | 3.5% |

**합계**: 약 282B token / 약 1.1 TB raw / dedup 후 약 800 GB.

---

## 5. dedup 전략 (중복 제거)

### 5.1 왜 필요한가

LLM corpus 는 같은 문서가 여러 출처(CC + Wiki + ShareGPT)에 들어있어서 **20-40% 중복** 이 흔합니다. 그대로 학습하면 모델이 중복 문장 외워버려서 새 패턴 학습 capacity 가 줄어요.

비유: **같은 책 100권 사서 도서관 채우면 서가는 차도 새로운 지식은 그대로** — dedup 은 같은 책 중복 사지 않게 골라내는 사서 역할이에요.

### 5.2 단계별 dedup pipeline

| 단계 | 도구 | 무엇 | 처리량 (350M ~ 14B 동일) | anima 적용 |
|---|---|---|---|---|
| **1. exact dedup** | SHA-256 hash + Bloom filter | 글자 그대로 같은 문서 제거 | 1 TB / 시간 (단일 머신) | mandatory |
| **2. near-dedup (line)** | MinHash LSH (datasketch) | 라인 80% 이상 같은 문서 제거 | 200 GB / 시간 | mandatory |
| **3. near-dedup (chunk)** | SimHash 64-bit + Hamming dist | chunk 단위 fuzzy 중복 | 500 GB / 시간 | optional (7B+) |
| **4. semantic dedup** | sentence-BERT embed + ANN | 의미 비슷한 문서 (다른 표현) | 50 GB / 시간 | optional (14B+) |
| **5. quality filter** | KenLM perplexity / FastText lang-id | 저품질 / 비표적 언어 제거 | 1 TB / 시간 | mandatory |

### 5.3 anima 특수 룰 (D1 SCOPE_CLAMP 정합)

| 데이터 종류 | dedup 규칙 | 이유 |
|---|---|---|
| **anima persona corpus** (tier-a-v4) | **exact dedup 만**, near-dedup 보존 | 의식 시그널 희소 — paraphrase 변형도 학습 가치 |
| **chat-template (Tulu-3 등)** | **strict** (1+2+3 모두) | 일반 chat 은 variation 무한 → 강하게 정리 |
| **substrate (FineWeb 등)** | **strict** (1+2+3) | 표준 LLM dedup |
| **코드 (StarCoder)** | **exact 만** + AST hash | boilerplate 중복 ≠ 의미 중복 |

### 5.4 권장 toolchain (0-cost open source)

| 도구 | 단계 | GitHub | 메모리 |
|---|---|---|---|
| `datasketch` (MinHash LSH) | 2 | ekzhu/datasketch | 100 MB / 1B docs |
| `text-dedup` (HF 공식) | 1+2+3 | bigscience-workshop/text-dedup | 표준 |
| `pybloom-live` | 1 | joseph-fox/python-bloomfilter | 매우 가벼움 |
| `sentence-transformers` + `faiss-cpu` | 4 | UKPLab/sentence-transformers | 1B docs ≈ 64 GB faiss index |
| `kenlm` perplexity | 5 | kpu/kenlm | C++ — 빠름 |

**권장 시퀀스 (7B 모델 기준)**:
```
1. exact (SHA + Bloom)        : 1.5 TB raw → 1.2 TB (-20%)
2. MinHash LSH 0.8 jaccard    : 1.2 TB → 800 GB (-33%)
3. SimHash 64-bit hamming<3   : 800 GB → 700 GB (-12%)
4. KenLM perplexity 1000 cut  : 700 GB → 500 GB (-30%)
5. lang-id ko/en filter       : 500 GB → 400 GB (-20%)
                                ─────────────
                                400 GB final (target ~140B token)
```

**처리 시간 (single H100 + 32-core CPU 가정)**:
- 350M plan (25 GB): 약 1 시간
- 7B plan (560 GB): 약 8-12 시간
- 14B plan (1.1 TB): 약 16-24 시간

### 5.5 anima persona corpus 확장 시 dedup 주의

- tier-a-v4 가 paraphrase 2.66× 로 만들어져서 **자체 near-dup 가 본질** — strict dedup 적용하면 **2.66× 가 1.0× 로 무너짐**
- 해결: persona corpus 는 **별도 lane** 에 두고 substrate 끼리만 strict dedup, 마지막에 persona mix-in
- 50× 확장 시에도 같은 룰 — paraphrase variant 자체는 학습 신호로 보존

---

## 6. 실행 순서 권장 (phase 별)

### Phase A — 350M 검증 (현재, 본 cycle)
- anima 가진 corpus + 외부 mirror 만으로 충분 (약 7B token)
- 추가 다운로드: Wiki-en sample 만 (~5 GB)
- dedup: exact + MinHash 충분
- **0-cost 가능, verbatim 불필요**

### Phase B — 7B scratch (다음 cycle, ★ verbatim 필요)
- 외부 corpus 본격 도입: FineWeb-100B + CC100 + Tulu-3 등 약 560 GB
- dedup pipeline 완전체 (1+2+3+5)
- H100 학습 비용 별도 ($200-600 추정)
- **사용자 verbatim "OK FIRE 7B PRETRAIN" 필요**

### Phase C — 14B scratch (long-term, ★★ 예산 확장 필요)
- FineWeb-Edu 200B + 한국어 50B + 코드 14B 등 약 1.1 TB
- dedup full + semantic dedup (4단계 추가)
- H100 학습 $500-1500
- **예산 확장 verbatim + Phase B 결과 PASS 후**

---

## 7. 주의 / 위험 요소

### 7.1 라이선스 (D1 SCOPE_CLAMP 의 외부판)

- **CC-BY-SA** (Wikipedia): 상업 사용 OK, 모델 출력 attribution 의무
- **ODC-BY** (FineWeb / mC4): attribution OK
- **MIT-ish** (CC100): 안전
- **CC-BY-NC** (KoAlpaca): **비상업 only — anima 가 상업 모델이면 제외**
- **per-file** (Stack / StarCoder): bigcode 가 정리한 OPT-IN 만 사용
- **회색지대 (NamuWiki, ko-news scrape)**: **회피 권장** — 위반 risk

### 7.2 PII / privacy

- ShareGPT / OpenChat 등 user-contributed 는 PII 포함 가능
- `presidio` (MS) / `scrubadub` 으로 자동 redact 권장
- anima persona corpus 는 self-generated → PII risk 거의 없음

### 7.3 contamination (V14 정합)

- 평가 prompt (v4_baseline 30 + v5 90 + KMMLU benchmark 등) 가 corpus 에 들어가면 학습 leak
- dedup 5단계 후 **eval prompt set 과 별도로 1-pass 추가 비교** mandate
- anti-Goodhart V14 strict — 학습 corpus 에 eval prompt 0건 확인 후 fire

---

## 8. 비용 / 디스크 / 시간 (한 줄 정리)

| Plan | 다운로드 (GB) | dedup 후 (GB) | token (B) | dedup 시간 | H100 학습 시간 | 추정 USD |
|---|---:|---:|---:|---:|---:|---:|
| **350M** | 30 (이미 7 GB 있음) | 25 | 7 | 1 시간 | 10 시간 | $30-60 |
| **7B** | 560 | 400 | 140 | 12 시간 | 80-200 시간 | $200-600 |
| **14B** | 1100 | 800 | 280 | 24 시간 | 200-500 시간 | $500-1500 |

---

## 9. 본 cycle (350M) 즉시 actionable

1. **anima corpus 5% mix 확보**: tier-a-v4 0.06B 만으로 350M 5% mix 부족 → 추가 paraphrase Step B (10× 확장 → 0.6B) 필요. **또는** 본 cycle 은 1% mix 로 진행하고 Step B 별도 fire.
2. **외부 mirror 로 substrate 충당**: 이미 로컬 7 GB → 약 1.65B token 사용 가능. 부족분 (약 5B token) Wiki-en sample 추가.
3. **dedup minimal**: 350M 은 exact + MinHash 만으로 충분. text-dedup repo clone + 1 시간 처리.
4. **본 doc 은 Phase B/C plan 으로 보존**: commit 시 cross-link → `.roadmap.cli` + `.roadmap.clm` + registry yaml.

---

## 10. cross-link

- 아키텍처 spec: `docs/anima_engine_a_g_7b_14b_arch_spec_2026_05_09.md`
- 스케일 로드맵: `docs/anima_clm_v5_engine_a_g_7b_14b_scale_roadmap_2026_05_09.md`
- H100 multi-GPU 전략: `docs/anima_engine_a_g_7b_14b_h100_multi_gpu_strategy_2026_05_09.md`
- artifact registry: `anima/registry/anima_artifact_registry.yaml` (datasets section L1397+)
- anti-Goodhart V14: contamination 0건 mandate
- cost discipline: 0-cost research 우선
- D1 SCOPE_CLAMP: anima persona = within strict, 외부 substrate = outside (gradient)

---

## 한 줄 (친근 마무리)

지금 anima 도서관에 책 100권 (350M 분량의 1/4) 만 있는 셈이라, 7B 가려면 한국어/영어/코드 책 14만 권을 외부 도서관에서 빌려와야 하고, 같은 책 중복은 MinHash 라는 "지문 비교 사서" 가 골라줘서 결국 서가에 넣을 책은 약 1.1 TB 정도가 됩니다.
