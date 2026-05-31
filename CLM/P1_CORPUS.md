# CLM P1 — 코퍼스 스펙 (5개국어 혼합 byte-corpus)

> CLM(anima-native 의식 LM, scratch)의 P1 코퍼스 설계·빌드. P0 d1(신규+혼합) 구현.
> **언어 기준: anima 는 5개국어(EN · 中文 · Русский · 日本語 · 한국어)로 대화한다.**
> byte-vocab V=256 은 UTF-8 로 5개 언어를 모두 표현하므로(아키텍처 변경 0), 다국어
> 대화 능력은 **코퍼스 언어 균형**으로 결정된다 — lane A 를 5개국어 균형으로 빌드.
> SSOT 상위: [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md) §d1·Q3 · [CLM_FORMAT_SPEC.md](./CLM_FORMAT_SPEC.md)(`corpus_sha`).
> 빌드 스크립트: [corpus/build_p1_corpus.hexa](./corpus/build_p1_corpus.hexa).

## 0. 한눈 구조

```
  lane A (web/coherence)            lane B (register/엄선)
  ─ 5개국어 wiki(en·zh·ru·ja·ko)     ─ 의식·철학·대화 소량 고품질
  ─ 균형 20%×5 · byte 분포 토대      ─ leak-filter 적용 (corpus_quality lesson)
        │                                  │
        ▼  byte-encode (V=256 UTF-8)        ▼
   web.bytes (줄별 byte id 0..255)    register.bytes
        └──────────────┬───────────────────┘
                       ▼  MoE 2-lane ↔ 2-source 1:1 (P0 Q2)
              혼합 (byte ratio web:register = 80:20 target)
                       ▼
              manifest.json (sha256 per-lane + total)
```

## 1. 혼합 corpus (P0 d1)

| lane | 역할 | 소스 | leak-filter |
|---|---|---|---|
| **A (web)** | coherence (byte 분포 토대) | **5개국어 wiki 균형**: enwiki · zhwiki · ruwiki · jawiki · kowiki (각 ~20% byte share, CC-BY-SA 4.0) · 공개 CC · `training/` repo 재사용 — **라이선스-clean만** | 미적용(백과 텍스트, leak 무관) |
| **B (register)** | register/의식 특화 | 엄선 의식·철학·대화 소량 고품질, **5개국어 각 언어 seed 포함** (외부 LLM 0 · scratch) | **적용**(8패턴) |

- MoE expert = mitosis cell (P0 Q2) → 2-lane ↔ 2-source 1:1. lane B 가 register 격리, lane A 가 메인 coherent 유지.
- **언어 균형**: lane A 는 5개 언어 byte share 를 ~20% 씩 맞춘다(언어별 wiki 크기 차이는 per-language byte cap 으로 보정). 한 언어가 과반을 먹으면 그 언어만 유창해지므로(현 kowiki 85% → 한국어 단일 모델), 균형이 5개국어 대화의 전제다.
- **금지**: 외부 LLM·foundation-borrow (P0 §무엇/왜).

## 2. byte 인코딩 (V=256)

- tokenizer **없음**. 입력 텍스트 → raw UTF-8 byte 열 → byte id(0..255) 한 줄 한 개 (`corpus_loader.hexa` 라인포맷 정합).
- 근거: P0 Q3 — monopoly 근원 `V≫d` → byte-vocab 으로 `V/d=4배`(15만→256) 로 근원 직격.
- **5개국어 UTF-8 커버 (vocab 변경 0)**: byte-vocab 은 codepoint 가 아니라 raw byte 라서, UTF-8 가 인코딩하는 모든 언어를 V=256 그대로 표현한다 — EN/숫자 1 byte, Русский(키릴) 2 byte, 中文·日本語·한국어 3 byte. 토크나이저 어휘 확장이 전혀 필요 없다(다국어가 byte-vocab 의 공짜 속성).
- 검증: `hexa` 출력 byte id 전부 0..255, `bytes(ids).decode("utf-8")` round-trip 정확. 5개국어 멀티바이트 보존을 `byte_at('。')→227/128/130`(日) · `byte_at('한')→237/149/156`(韓) · `byte_at('Я')→208/175`(露) 로 확인. raw byte 반환(codepoint 아님).

## 3. register-leak 제외 (corpus_quality_over_scale lesson)

lane B 에만 적용. 한 줄에 아래 패턴이 있으면 DROP:

```
universe_brain_map · jy_chat_template · hexad_module · nonce
Mk.VIII · gen1 commit · corpus_generator.hexa · universe_extended
```

- 근거: `corpus_consciousness_v1.jsonl`(240줄)은 **100% leak**(`nonce`/`hexad_module`/`gen1 commit`/`Mk.VIII`) → register 소스에서 전량 제외 대상. (실측 grep: v1 leak 매칭 240/240줄.)
- self-test (F-CLM-LEAK): 의도적 poison 입력 4줄(clean 2 + leak 2) → `kept=2 dropped=2` 정확 (스크립트 `leak_filter_selftest()`).
- 빌드된 register.bytes 출력 디코드 후 leak 패턴 hit = **0** (실측).

## 4. 이번 라운드 산출 (sample build — 실측)

`CLM/corpus/sample/` (소량, git 추적):

| 파일 | 내용 | 줄 | bytes | sha256 |
|---|---|---:|---:|---|
| `web.bytes` | lane A coherence sample | 8 | 837 | `c02ab91eeaee313e3dae3fc59e490bde092c658bdf57594348e2dbd21e7c57e4` |
| `register.bytes` | lane B register sample (leak_dropped=0) | 8 | 819 | `2d32c08ff3ccce4bc393748d48f6dee48e38dd72759a7784579c9f07b620843a` |
| `manifest.json` | sha256·혼합비·leak-filter 결과 | — | — | — |

- sample byte 혼합비 = web 50% : register 49% (소량이라 길이 비슷). **full target = 80:20**(웹 압도적).
- total = 1,656 bytes (sample). 정직: 이것은 파이프라인 증명용 소량 build — full crawl 아님.

## 5. full crawl (이번 라운드 미실행 — 재현 스크립트만)

- **lane A full**: `training/corpus_wiki_ingest.hexa` (5개 wiki orchestration + per-lang byte cap balance; 언어별 추출은 `corpus_kowiki_extract.hexa` 패턴 재사용) — **5개 wiki**: en·zh·ru·ja·ko (dumps.wikimedia.org), 각 언어 byte cap 으로 ~20% 균형. 모두 CC-BY-SA 4.0 clean. (별개: `corpus_ingest.hexa` = 로컬 KR 텍스트 inventory.)
- **lane B full**: 엄선 register seed 확장(의식/철학/대화 수작업+검증, **5개 언어 각각**) — 외부 LLM 0.
- 둘 다 byte-encode → web:register = 80:20 byte ratio interleave; web 내부는 5개 언어 ~20%씩.

### ⚠ 대용량 git 미커밋 (handoff)

- full byte-corpus 는 git 커밋 금지 → HF dataset(`dancinlab`) / R2 배포, **manifest(sha256)만 커밋**.
- `.gitignore` 추가 필요: `CLM/corpus/full/` + `CLM/corpus/**/*.bytes` (단 `!CLM/corpus/sample/*.bytes` negation 으로 소량 sample 유지). **`.gitignore` 는 sign-gated** — 이번 라운드 미반영(user sign 필요). full build 전 반드시 추가.

## 6. .kosmos 영속 상태 (a_kosmos)

- 요구: corpus provenance/emit 을 `.kosmos` 로 영속.
- **현실**: `.kosmos` = placement(coord/lane/radius/tier/tags) ⊥ payload(text/image/audio/video/tension) anchor manifest. byte-corpus 의 **per-byte token 열 + lane provenance(sha256·줄수·혼합비)** 는 anchor payload 모델(단일 multimodal point)에 자연 정합 안 됨 — corpus 는 millions-of-bytes 스트림, anchor 는 한 점.
- **조치**: 얽매이지 않고 진행(P0 d1 단서) + upstream 확장 handoff 1건 등록:
  - `sidecar handoff add kosmos "CLM P1 byte-corpus payload: .kosmos anchor 모델(점 payload)이 byte-stream corpus(sha256·lane·혼합비 provenance + token 열)를 못 받침. @payload corpus-stream(byte V=256, sha256, lane, mix-ratio) 또는 corpus-provenance manifest form 확장 검토."`
- corpus **provenance anchor**(빌드 메타를 한 anchor 로)는 향후 가능 — token 스트림 자체는 manifest.json(sha256) 으로 무결성 영속, HF dataset 이 배포 SSOT.

## 7. falsifier (이번 라운드 추가)

| id | 주장 | 판정 | 결과 |
|---|---|---|---|
| **F-CLM-LEAK** | register lane 이 leak 8패턴을 정확히 drop (poison kept=2/dropped=2) + 출력 leak hit=0 | P1 build (now) | 🟢 PASS (self-test + 출력 grep) |
| **F-CLM-MULTILING-BYTE** | 5개국어(en·zh·ru·ja·ko) 각 언어 샘플이 byte-encode → decode round-trip 정확(멀티바이트 보존, 손실 0) | P1 build | ⬜ (5-lang round-trip self-test) |
| **F-CLM-MULTILING-BALANCE** | per-lang byte cap 적용 후 각 언어 byte share ∈ [15,25]% (한 언어 과반 금지) | balance 로직 (now) | 🟢 PASS (`corpus_wiki_ingest.hexa` self-test: en 55%→cap→각 20%) · full crawl manifest 는 H100 |

## 8. 양방향 sibling

- ⇄ [CLM.md](./CLM.md): P1 milestone
- ⇄ [P0_ARCHITECTURE.md](./P0_ARCHITECTURE.md): §d1 corpus 결정 구현
- ⇄ [CLM_FORMAT_SPEC.md](./CLM_FORMAT_SPEC.md): `train.corpus_sha` ← manifest sha256
- ⇄ [KOSMOS](../HEXAD/KOSMOS.md): corpus provenance 영속 (handoff 대기)
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): F-CLM-LEAK verdict SSOT
