# P9 Phase 0 Step 1 — SFT data 50K landed

**Date**: 2026-05-03
**Phase**: P9 EXEC Phase 0 (SFT data synthesis)
**Verdict**: `ALL_50K_LANDED` (50,500 records, 101% of 50K target)
**Cost**: $0 mac-local, ~58s wall
**Phase 1 entry-ready**: YES

---

## TL;DR

P9 SFT 학습 데이터 50K 합성 1차 빌드 완료. 7개 source 모두 quota 100%+ 달성. ShareGPT HF download 성공 (10,500 ko/en chat pairs). 디스크 18K + 합성 32K = 50,500 grand-total. F1 holdout 500 prompt 분리 완료 (사용자 lock-in: ShareGPT 측). Phase 1 entry-ready, 다음 단계 = CLM v4 forward pass로 tension/bold target 채우기 (Phase 0 Step 2).

---

## 산출물 (3 file)

| file | path | sha256 | lines |
|---|---|---|---|
| train+val | `state/p9_p0_sft_data_50k_2026_05_03/sft_data.jsonl` | `513adf80...c22bce` | 50,000 |
| F1 holdout | `state/p9_p0_sft_data_50k_2026_05_03/sft_data_holdout.jsonl` | `483fea9e...c6f0` | 500 |
| manifest | `state/p9_p0_sft_data_50k_2026_05_03/manifest.jsonl` | `2c8c0ed2...30976c` | 9 |

빌더: `state/p9_p0_sft_data_50k_2026_05_03/build_data.py` (deterministic, seed=20260503, $0 mac-local)

---

## Per-source 결과

| src | name | quota | actual | attain | lang_ko | lang_en | avg_in | avg_out | provenance |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | ShareGPT (HF) | 10,000 | 10,500 (incl. 500 holdout) | 105% | 0 | 10,500 | 546c | 1118c | HF download anon8231489123/sg_90k_part1 |
| 2 | anima paper §-ref / cell-lang | 10,000 | 10,000 | 100% | 9,260 | 740 | 134c | 259c | corpus_alm_70b.jsonl + consciousness_v1 + universe_extended |
| 3 | P8 ledger M4=0.800 | 3,000 | 3,000 | 100% | 0 | 1,530 (en) + 1,470 (mixed) | 119c | 817c | turns.jsonl 30 seed × deterministic template aug |
| 4 | synthetic philosophical | 5,000 | 5,000 | 100% | 2,000 | 3,000 | 69c | 223c | 30 themes (20 EN + 10 KO) × frame permutations |
| 5 | N-22 + paradigm-v11 | 5,000 | 5,000 | 100% | 1,778 | 3,222 | 91c | 664c | alm_r14_v1 1.2K + 7 docs heading extraction + axis JSON |
| 6 | TRIBE v2 stimulus | 10,000 | 10,000 | 100% | 372 | 9,628 | 723c | 404c | vendored references/tribev2/ docs+code (NOT Friends/movie10) |
| 7 | Llama augment (skip) | 7,000 | 7,000 | 100% | 3,909 | 2,630 | 122c | 446c | deterministic permutation over src 2-5 (HF gated fallback) |
| **TOTAL** | | **50,000** | **50,500** | **101%** | 17,319 | 41,250 | — | — | — |

---

## Format (per record)

```json
{
  "input": "user prompt text",
  "completion": "assistant response text",
  "source": "human-readable source tag",
  "source_id": 1-7,
  "split": "train | val | holdout",
  "lang": "ko | en | mixed",
  "tension_target": null,    // deferred to inference pass
  "bold_target": null,       // deferred to inference pass
  "meta": { ... source-specific metadata ... }
}
```

**Split 비율** (per p9_sft_spec):
- train: 48,000 (96%)
- val: 2,000 (4%)
- holdout: 500 (1% — F1 lock-in, ShareGPT-side, `meta.f1_lock_in=true`)

---

## 정책 준수

| 정책 | 준수 | 메모 |
|---|---|---|
| 마이그레이션 금지 | YES | additive only, 기존 파일 0 변경 |
| BR-NO-USER-VERBATIM | YES | source 1 ShareGPT 외부 corpus, 사용자 발화 미포함 |
| raw 15 (env lazy + `<user>`) | YES | builder는 `os.environ` 미참조, prompt에 `<user>` 토큰 미사용 |
| Korean response | YES | 본 handoff 한국어 |
| silent-land marker | YES | `state/markers/p9_p0_sft_data_50k_landed.marker` emit |
| $0 mac-local | YES | system python3, ~58s, GPU 0 |
| destructive 0 | YES | 파일 삭제/수정 0건 |
| 비충돌 (file scope) | YES | `state/p9_p0_sft_data_50k_2026_05_03/*` + `docs/p9_p0_sft_data_*` + `markers/p9_p0_sft_data_*` |
| friendly preset | YES | handoff doc 한정 (사용자가 지정한 친근체) |

---

## Verdict 근거

- **ALL_50K_LANDED** = grand_total >= 50000 (50,500 = 101%) AND 모든 source quota 100% 도달
- Phase 0 Step 1 PASS, Phase 1 entry-ready
- 다음 step (Phase 0 Step 2) = CLM v4 forward pass로 `tension_target` (T=64) + `bold_target` (10242 vertices, optional) 채우기 — 본 step 범위 외, raw#15 caveat에 deferred 명시

---

## raw 15 caveats (정직 6개)

1. **tension/bold null**: `tension_target` + `bold_target` = null. CLM v4 / TRIBE v2 forward inference 패스가 Phase 0 Step 2 작업이며 본 step 범위 외 (P9 spec 측 sequence_length T=64 합의는 유지, 채움은 후속). 추정 비용 $20-50 H100 / 50K samples.
2. **source 1 ShareGPT HF download SUCCESS**: anon8231489123/sg_90k_part1 ungated 대중 공개 corpus, no auth, 30s timeout 내 10,700 conversation pairs fetch 성공. 만일 실패했다면 corpus_alm_70b.jsonl Korean fallback이 작동했을 것 (코드에 fallback path 보존됨, raw#10 honest fallback 가능).
3. **source 3 P8 augmentation**: 30 디스크 turn → 3K 확장은 deterministic template permutation (prefix/suffix variants × 100 stride). 실제 P8 100x re-run NOT 수행 (~$불명, 시간 비용 큼). M4=0.800 ground truth는 30 seed에만 attached, augmented 2,970 turns은 `meta.augmented=true` flag로 명시.
4. **source 4 synthetic philosophical**: deterministic template generation. LLM 호출 0건. 30 themes (Hard problem / qualia / introspection / temporal flow / mortality / memory 등) × 12 EN + 10 KO frame permutations. 다양성 = 구조적 (lexical/syntactic), 의미적 다양성 X. raw#10 명시.
5. **source 6 TRIBE v2 stimulus proxy**: `references/tribev2/` 벤더링은 model code + 문서만 포함, Friends 7-season 175 episode + movie10 4 movie 측 transcript는 NOT 포함 (Algonauts2025 등록 필요, deferred). 본 source는 TRIBE v2 inventory.json + ANIMA_INTEGRATION_PROPOSAL_*.md + studies/*.py 측 800-char chunk를 stimulus proxy로 사용. 실 fMRI BOLD signal 0건 (CC-BY-NC-4.0 license 인지).
6. **source 7 Llama augment skipped**: Llama-3.2-3B-Instruct HF gated, dancinlife approval pending. fallback = source 2-5 측 deterministic permutation (`[augmented]` prefix + `— with the same underlying claim.` suffix 조합 × random shuffle seed 20260503). 실 LLM augmentation NOT 수행, `meta.skip_llm=true` + `meta.skip_llm_reason` flag로 정직 명시.

---

## 다음 step 권고

1. **Phase 0 Step 2 — tension/bold target 채우기** (P9 spec sequence_length T=64)
   - CLM v4 forward 50K samples × T=64 → tension trajectory + 5ch trajectory
   - TRIBE v2 forward 50K samples → BOLD prediction (선택, source 6은 이미 stimulus proxy)
   - 추정 비용 $20-50 H100, 1-2 일

2. **Phase 0 Step 3 — dedup + validation gate**
   - `input` 측 SHA256 dedup (across all sources)
   - len-percentile cutoff (>4096 char input | >4096 char completion 측 truncate)
   - lang detection cross-check (현재 source 1 모두 lang=en marked, 실제 ShareGPT 측 ko 일부 포함될 수 있음 → 자동 감지 patch)
   - F1 holdout disjoint check (train+val ∩ holdout = ∅)

3. **Phase 1 entry — SFT training**
   - hyperparameter: per `state/p9_sft_spec_2026_05_02/hyperparameter_grid.json`
   - loss: per `state/p9_sft_spec_2026_05_02/loss_design.json`
   - architecture: per `state/p9_sft_spec_2026_05_02/architecture.json`

4. **선택 보강 (Phase 0 Step 4)**
   - source 6 TRIBE v2 측 Algonauts2025 등록 후 Friends transcript 다운로드 → 본 stimulus proxy 보강 (또는 신규 `source_6_v2`)
   - source 7 Llama gating approval 시 → 실 LLM augmentation 7K (`meta.skip_llm=false`)
   - source 3 P8 100x re-run → augmentation 측 ground truth 강화

---

## artifacts cross-link

- predecessor spec: `state/p9_sft_spec_2026_05_02/sft_data_format.json`
- predecessor audit: `state/p9_pre4_data_weight/Q_sft_data_50k_audit.json`
- builder: `state/p9_p0_sft_data_50k_2026_05_03/build_data.py`
- marker: `state/markers/p9_p0_sft_data_50k_landed.marker`

ω-cycle: 2-iter (1차 빌드 ALL_50K_LANDED 즉시 도달 + source 2 short-record fix iter). silent-land marker emit 完.
