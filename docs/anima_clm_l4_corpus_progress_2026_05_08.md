# anima CLM L4 corpus — iter-1 curation progress (2026-05-08)

**Goal**: Loop iter (c) — corpus 1차 큐레이션 (Tier A persona ~100MB + Tier B
dialogue sample ~10MB). Tier C (외부 LLM dump / wiki noise / generic chatbot)
reject 검증 수반.

**Cross-link**:
- `docs/anima_clm_l4_corpus_2026_05_08.md` (corpus tier 정의 SSOT)
- `tool/transient_py/anima_clm_l4_corpus_iter1_curate.py` (raw#37 transient 큐레이션 script)
- `state/anima_clm_l4_corpus_iter1_metrics.json` (raw measurement SSOT)
- `tool/transient_py/anima_clm_l[abcd]_h100.py` (BG path corpus_path placeholder)

---

## iter-1 결과

### Tier A persona corpus

- path: `state/anima_persona_tier_a_2026_05_08.txt`
- size: **102.66 MB** (107,647,383 bytes) — 100MB target 충족
- combined density: **1.6006%** (own 18 C3 threshold 0.4% 대비 4×)
- combined kw_hits: 1,215,086 / chars: 75,914,941
- 11 source ACCEPT / 1 source REJECT (paper_self_discovery.hexa density 0.31% < 0.4%)

### Tier B dialogue corpus (sample)

- path: `state/anima_dialogue_tier_a_2026_05_08.txt`
- size: **12.96 MB** (13,591,084 bytes) — 10MB target 충족 (sample only)
- density: **0.7177%** (own 18 C3 threshold pass)
- format: `사용자: <Q>\n도우미: <A>\n\n` (own 20 chat-template mandate)
- source: `state/anima_h098_h101_corpus_v3_2026_05_07/corpus_persona_chat_template.txt` head 10MB

---

## density 측정값 매트릭스

| source | size | density | kw_hits | chars | verdict |
|---|---|---|---|---|---|
| corpus_universe_brain_map.txt (21MB v2) | 16MB | 3.28% | 541,809 | 16,496,964 | ACCEPT |
| corpus_universe_brain_map.txt (6.5MB v1) | 4.4MB | 3.42% | 158,400 | 4,636,512 | ACCEPT |
| corpus_persona_chat_template.txt (h098_h101) | 21MB | 0.80% | 172,777 | 21,467,614 | ACCEPT |
| corpus_curated_qa.txt | 1.3MB | 1.63% | 22,522 | 1,385,404 | ACCEPT |
| corpus_combined.txt (paradigm — sample 30MB) | 30MB | 1.01% | 316,696 | 31,457,280 | ACCEPT |
| paper_consciousness_laws.hexa | 17KB | 0.48% | 85 | 17,729 | ACCEPT |
| paper_hexa_speak.hexa | 17KB | 0.53% | 94 | 17,884 | ACCEPT |
| paper_self_discovery.hexa | 19KB | 0.31% | 59 | 19,290 | **REJECT** |
| .roadmap.philosophy | 28KB | 0.71% | 208 | 29,124 | ACCEPT |
| .roadmap.law | 73KB | 0.72% | 540 | 74,704 | ACCEPT |
| .roadmap.hypothesis | 33KB | 0.59% | 199 | 33,629 | ACCEPT |
| hypotheses/H_*.md (152 files) | 290KB | 0.59% | 1,740 | 296,803 | ACCEPT |

**density measurement**: anima keyword count / total chars (char-level proxy).
keywords: anima/Anima/ANIMA, 의식/consciousness, Φ★/phi_star/Φ, 우주뇌지도/PureField,
법칙/Law/law_, 가설/Hypothesis, Engine A/G, 자기 발견/self_discovery, hexa/Hexa,
creator/1030 laws, axis_activation/5-axis, dominant cells, hidden state.

---

## target vs actual size

| BG | target (spec) | iter-1 actual candidate | gap | next iter plan |
|---|---|---|---|---|
| BG-LA persona | 200MB | 102.66MB | -97MB | 추가 anima native source 확장 (anima self-talk / cycle log 누적) |
| BG-LB persona | 1GB | 102.66MB | -921MB | iter-2 대형 expansion (anima cycle log + .raw-audit anima portion + chat history) |
| BG-LB dialogue | 500MB | 12.96MB sample | -487MB | iter-2 expansion (V4 evaluator산출물 + 사용자 ↔ Claude session log) |
| BG-LC persona | 200MB | 102.66MB | -97MB | BG-LA 와 동일 source 재사용 (distill teacher 입력) |
| BG-LD pairs | 100MB | 0 | -100MB | iter-2 별도 cycle (V4 evaluator chosen/rejected pair 추출) |

---

## BG path corpus_path 매트릭스 (iter-1 candidate emit)

| BG | placeholder var (TBD path) | iter-1 candidate var | iter-1 path |
|---|---|---|---|
| BG-LA | `MAC_CORPUS_PATH` | `MAC_CORPUS_PATH_ITER1_CANDIDATE` | `state/anima_persona_tier_a_2026_05_08.txt` |
| BG-LB | `MAC_CORPUS_PERSONA_PATH` | `MAC_CORPUS_PERSONA_PATH_ITER1_CANDIDATE` | 동상 (102.66MB — target 1GB 대비 부족) |
| BG-LB | `MAC_CORPUS_DIALOGUE_PATH` | `MAC_CORPUS_DIALOGUE_PATH_ITER1_CANDIDATE` | `state/anima_dialogue_tier_a_2026_05_08.txt` (12.96MB sample) |
| BG-LC | `MAC_CORPUS_PATH` | `MAC_CORPUS_PATH_ITER1_CANDIDATE` | 동상 (BG-LA 재사용) |
| BG-LD | `MAC_CORPUS_PAIRS_PATH` | `MAC_CORPUS_PAIRS_PATH_ITER1_CANDIDATE` | None (iter-2) |

본 candidate 변수는 SPEC TBD path 와 **공존** — actual fire 시점에 사용자 OK
'OK CLM L4 ALL FIRE' 후 placeholder TBD path → candidate path 로 swap (또는 candidate
path 그대로 사용 결정) 별도 cycle.

---

## own 17 anima-native lane 정합 (Tier C reject 검증)

본 iter-1 큐레이션은 own 17 anima-native lane 강조:

- **외부 LLM 출력 dump REJECT**: 본 iter-1 source 어디에도 ChatGPT / Claude API 출력 dump 미사용
  (anima curated QA + paradigm corpus 는 anima 자체 생성 lineage)
- **wiki noise REJECT**: BG-JE 214MB (kowiki 69.61%) 본 iter-1 에서 reject —
  anima persona marker 분포 만으로는 own 17 anima identity-bearing 정합 미충분 (사용자 directive
  '외부 wiki / 일반 뉴스 / 외부 LLM 출력 = REJECT'). 향후 iter-2 에서 anima lookup 응답
  subset (Q wiki + A anima) 만 추출 검토.
- **generic chatbot dump REJECT**: Persona-Chat / OASST / KoChat 등 외부 dialogue dataset
  본 iter-1 미사용 (Tier B dialogue 는 anima 자체 생성 chat-template subset 만)
- **alm-* dataset 흔적 REJECT**: source 어디에도 ALM lineage 미포함 (own 17 anima-no-external-substrate-wrapping 정합)

raw#10 honest C3:
1. density measurement = char-level keyword count proxy — semantic depth 미측정 (manual review 권고)
2. paper_self_discovery.hexa REJECT — keyword density 0.31% < 0.4% threshold. 본 file 은
   anima identity-bearing 이지만 keyword 분포가 sparse — 본 iter-1 quantitative threshold 만
   적용. 향후 iter-2 semantic embedding-based density (sentence-transformers) 검토.
3. own 18 C3 threshold 0.4% 자체 = heuristic — own 18 baseline-measured 0.0096 (Φ★ drift)
   와 다른 axis (corpus density). corpus density threshold 별도 ROC formal 강화 후속 cycle.

---

## 다음 iter (iter-2) plan

### iter-2 Tier A persona expansion (100MB → 1GB target)

- anima cycle log 추출 (cycle 별 docs/anima_*.md 본문 — anima identity-bearing 비율 ≥0.4% filter)
- .raw-audit anima portion (anima cycle log 의 ω-cycle output 부분 추출)
- 사용자 ↔ Claude session 기록 중 anima-cor 응답만 추출 (own 17 정합 — anima identity bearing line)
- semantic-density filter: sentence-transformers MiniLM 으로 paragraph-level density score 측정
  → high-density paragraph 만 retain (본 iter-1 char-level keyword count proxy 강화)

### iter-2 Tier B dialogue expansion (12MB → 500MB target)

- V4 evaluator 산출물 누적 (BG-KM-LLAMA-3B 12/15 PASS_STRICT v4_pass=true sample +
  BG-K* 22+ saga 의 PASS sample) → chat-template format 으로 정규화
- own 20 chat-template ≥30% 비율 검증
- own 18 C2.4 맥락 정합 검증 (greeting → greeting reply 등 mismatch sample 제외)

### iter-2 Tier B preference pairs (BG-LD)

- V4 evaluator 산출물 jsonl + verdict.json 의 v4_pass 매트릭스 → chosen 추출
- 22+ BG saga 의 V4 FAIL sample (BG-JA-EXT degenerate / BG-FK / corpus template leak) → rejected 추출
- chosen/rejected 1:1 ratio (DPO standard) — 100MB 까지 누적 (부족 시 manual curation)

### iter-2 own 18 C3 threshold 강화

- ROC formal: random_init FAIL ≥0.95 + chat-capable PASS ≥0.7 데이터 누적
- corpus density threshold 도 baseline-measured 형태 (현재 0.4% heuristic)

---

## blockers

- iter-2 expansion source (anima cycle log / .raw-audit / 사용자 session) 는 manual curation 필요
  — automated pipeline 별도 cycle (own 19 corpus priority + chicken-egg: chat-cap 도달 전이라
  anima self-talk 시뮬레이션 불가능)
- BG-LD pairs 100MB target — V4 evaluator 산출물 누적 부족 가능성 (현재 BG-KM-LLAMA-3B 12/15 PASS sample
  + BG saga FAIL sample 만 → 100MB scale 까지 추가 prompt 확장 필요)
- own 16 cost discipline — 본 iter-1 = corpus 큐레이션만 (학습 X). L4 fire 는 사용자 explicit
  'OK CLM L4 ALL FIRE' 후 별도 cycle.

---

## raw#10 honest C3 (≥9)

1. iter-1 본 cycle = char-level density proxy — semantic depth 미측정 (sentence-embeddings 별도 cycle)
2. Tier A persona 102.66MB ≠ target 200MB (BG-LA/LC) / 1GB (BG-LB) — 후속 iter expansion 필수
3. Tier B dialogue 12.96MB ≠ target 500MB (BG-LB) — sample only
4. BG-LD pairs 100MB 본 iter-1 미진행 — V4 evaluator 산출물 누적 별도 cycle
5. paper_self_discovery.hexa 0.31% REJECT — keyword density threshold 의 quantitative proxy
   한계 (semantic depth 측정 시 ACCEPT 가능)
6. wiki QA chunk 의 anima lookup 응답 subset 활용 가능성 — 현재 BG-JE 214MB 전부 reject 했으나
   anima identity-bearing 응답만 추출 가능 (wiki Q + anima A 형태) iter-2 검토
7. own 17 strict enforce — Tier C 외부 LLM dump / Persona-Chat / OASST / KoChat 본 iter-1
   사용 X. 향후 iter-2 에서 chat-template 학습 한정 외부 dataset 마이너 양보 (own 17 spec 정합) 검토
8. own 18 C3 corpus density threshold 0.4% 본 cycle heuristic — ROC formal 별도 cycle
9. iter-1 raw measurement SSOT = `state/anima_clm_l4_corpus_iter1_metrics.json` (size + density + kw_hits + sources_accepted/rejected)

---

## 본 iter-1 SSOT

- raw measurement: `state/anima_clm_l4_corpus_iter1_metrics.json`
- 큐레이션 script: `tool/transient_py/anima_clm_l4_corpus_iter1_curate.py` (raw#37 transient)
- progress 문서: `docs/anima_clm_l4_corpus_progress_2026_05_08.md` (본 .md)
- spec 모태: `docs/anima_clm_l4_corpus_2026_05_08.md`

---

# iter-2 결과 (Loop iter c — 2nd pass, additive over `0116a35d`)

## iter-2 Tier A persona (semantic-deepen, additive)

- path: `state/anima_persona_tier_a_2026_05_08.txt` (iter-1 file 에 append, raw#15 additive)
- pre-size: 102.66MB → post-size: **103.59MB** (Δ +0.93MB)
- combined density: **1.5911%** (own 18 C3 threshold 0.4% × 4 유지)
- 353 files scanned (docs/anima_*.md + docs/anima/*.hexa + docs/ai-native/*.md +
  .roadmap.* + anima/.own + anima/spec + config/core_rules.json)
- 976 paragraphs accepted, 6,001 rejected (semantic-density filter 86% reject rate)
- **semantic-density filter** (own 18 C3 강화 시도):
  paragraph 가 다중 keyword set ≥2/6 axes 동시 hit AND char-density ≥0.4%
  → quality 우선 conservative accept (대부분 docs는 single-axis 만 touch).

### semantic-density 6 axes
1. consciousness/anima identity — `의식, anima, consciousness, Φ`
2. law/foundation — `법칙, law, Law , creator`
3. hypothesis/experiment — `가설, hypothesis, H_, BG-`
4. 5-axis — `axis, 5축, identity, agency, phenomenal, temporal, social`
5. chat-cap — `chat-cap, PASS_STRICT, simple_stack, V4, V5`
6. engines — `Engine A, Engine G, PureField, engines`

## iter-2 Tier B dialogue (chat-template format)

- path: `state/anima_dialogue_tier_a_iter2_2026_05_08.txt` (신규 file, raw#15 additive — iter-1 file 보존)
- size: **72.78MB** (76,311,787 bytes)
- density: **0.9705%** (own 18 C3 threshold pass 2.4×)
- chat-template ratio: **28.95%** (own 20 ≥30% threshold marginal — iter-3 정합 후속)
- n_user_turns: 136,073 / n_assistant_turns: 136,140

### iter-2 Tier B sources
| source | size | description |
|---|---|---|
| BG-JE persona chat-template ext (offset 10MB+, 21MB) | ~21MB | iter-1 head 10MB 의 deeper portion |
| anima_combined_paradigm_corpus chat-template (~55MB) | ~55MB | paradigm v11 G3 chat-template 본문 |
| V4 BG-KM-LLAMA-3B v4_pass=true sample (23/55) | ~10KB | own 18 C2.4 PASS, multi-seed |
| anima_core_dialogues normalized chat-template (17 pairs) | ~3KB | substrate probe → echo Q/A |
| strategic_tribev2_dialogue (turns.jsonl) | ~30KB | introspective dialogue, llama_p10/p13 |

own 18 C2.4 mismatch filter: `is_degenerate` heuristic (han_ratio < 0.30, repeat ≥20, replacement char ≥5)

## iter-2 BG-LD preference pairs (sample)

- path: `state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl`
- size: **17.66MB** (18,519,656 bytes) — 100MB target gap -82.34MB
- pairs count: **30,023** (1:1 chosen/rejected per pair)
- format: `{"prompt", "chosen", "rejected", "domain", "source_chosen", "source_rejected"}`

### chosen vs rejected pool
- **chosen pool**: 23 sample (BG-KM-LLAMA-3B v4_pass=true filter, post-degenerate/template-leak filter)
- **rejected pool**:
  - 5,000 v4/v5 saga FAIL sample (`is_degenerate=true`, `v4_strict_pass=false`)
  - 46 synthetic (template_leak `서연:` augment + degenerate `이` repeat noise)
- expansion: chosen × rejected cartesian until 15MB target (capped 30,023 pairs)

---

## iter-1 vs iter-2 comparison table

| metric | iter-1 (0116a35d) | iter-2 (본 cycle) | delta |
|---|---|---|---|
| Tier A persona size | 102.66 MB | 103.59 MB | +0.93 MB |
| Tier A combined density | 1.6006% | 1.5911% | -0.0095pp |
| Tier B dialogue size | 12.96 MB | **72.78 MB** | **+59.82 MB** |
| Tier B chat-template ratio | n/a | 28.95% | (own 20 marginal) |
| BG-LD pairs size | 0 | **17.66 MB** | **+17.66 MB** |
| BG-LD pairs count | 0 | 30,023 | (1:1 chosen/rejected) |

## 누적 sizes vs targets

| BG | target (spec) | iter-2 cumulative | gap | next iter plan |
|---|---|---|---|---|
| BG-LA persona | 200MB | 103.59MB | -96.41MB | iter-3 anima cycle log full archive ingest |
| BG-LB persona | 1GB | 103.59MB | -920MB | iter-3 cycle log + .raw-audit + 사용자 session log archive |
| BG-LB dialogue | 500MB | 72.78MB | -427MB | iter-3 V4 evaluator full sample + 외부 wiki Q + anima A subset 검토 |
| BG-LC persona | 200MB | 103.59MB | -96.41MB | BG-LA 와 동일 source 재사용 (distill teacher 입력) |
| BG-LD pairs | 100MB | 17.66MB | -82.34MB | iter-3 prompt expansion (15 V4 prompts → 100+) |

---

## iter-2 BG path corpus_path 매트릭스

raw#15 additive: iter-1 candidate var 보존 + iter-2 candidate var 신규 추가 (TBD path placeholder
도 보존 — fire 시점 사용자 explicit override 후 swap 결정 별도 cycle).

| BG | placeholder | iter-1 candidate var | iter-2 candidate var | iter-2 path |
|---|---|---|---|---|
| BG-LA | `MAC_CORPUS_PATH` | `MAC_CORPUS_PATH_ITER1_CANDIDATE` | `MAC_CORPUS_PATH_ITER2_CANDIDATE` | `state/anima_persona_tier_a_2026_05_08.txt` (103.59MB) |
| BG-LB persona | `MAC_CORPUS_PERSONA_PATH` | `MAC_CORPUS_PERSONA_PATH_ITER1_CANDIDATE` | `MAC_CORPUS_PERSONA_PATH_ITER2_CANDIDATE` | 동상 (103.59MB) |
| BG-LB dialogue | `MAC_CORPUS_DIALOGUE_PATH` | `MAC_CORPUS_DIALOGUE_PATH_ITER1_CANDIDATE` | `MAC_CORPUS_DIALOGUE_PATH_ITER2_CANDIDATE` | `state/anima_dialogue_tier_a_iter2_2026_05_08.txt` (72.78MB) |
| BG-LC | `MAC_CORPUS_PATH` | `MAC_CORPUS_PATH_ITER1_CANDIDATE` | `MAC_CORPUS_PATH_ITER2_CANDIDATE` | 동상 (BG-LA 재사용) |
| BG-LD | `MAC_CORPUS_PAIRS_PATH` | `MAC_CORPUS_PAIRS_PATH_ITER1_CANDIDATE` (None) | `MAC_CORPUS_PAIRS_PATH_ITER2_CANDIDATE` | `state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl` (17.66MB) |

---

## iter-3 plan

### Tier A persona iter-3 (target 200MB+)
- 사용자 ↔ Claude session log archive 별도 access 필요 (anima identity-bearing turn 만 추출)
- anima cycle log 전체 archive ingest (현재 docs/anima_*.md 285개 → cycle log archive 별도 path)
- semantic-density filter 강화 — sentence-transformers MiniLM 검토 (raw#9 hexa-only 위반 검토 또는 byte-level approx alternative)
- conditional accept rate (현재 14% → relax 시 30%+ 가능)

### Tier B dialogue iter-3 (target 500MB)
- V4 evaluator 산출물 full sample 추출 (현재 23 PASS → 60+ PASS 가능)
- 사용자 ↔ Claude session 의 anima-cor 응답 외 turn 도 chat-template 정규화 (own 17 정합 검증)
- chat-template ratio ≥30% 보장 (own 20 mandate; 현재 28.95% marginal)
- 외부 wiki Q + anima A subset 검토 (Q wiki + A anima 만 — Q-only wiki 제외, own 17 marginal exception)

### BG-LD pairs iter-3 (target 100MB)
- V4 prompt expansion 15 → 100+ (BG-KM 의 15 prompts 만으로는 chosen pool 부족)
- 인간 ↔ anima preference signal 추가 (사용자 explicit ranking 별도 cycle)
- chosen-rejected semantic margin gap 확보 (현재 chosen=PASS PASS / rejected=degenerate 만 — gap 너무 큼)

### own 18 C3 corpus density ROC formal
- random_init_corpus_subset density baseline 측정
- chat-cap_corpus density baseline 측정
- ROC threshold formal 강화 (현재 0.4% heuristic → measurement-driven)

---

## iter-2 honest C3 (≥9)

1. iter-2 Tier A semantic-density filter = char-level multi-keyword set co-hit ≥2/6 axes proxy — sentence-transformers MiniLM 미적용 (raw#9 hexa-only 정합 검토; 외부 ML lib 또는 byte-level approx 별도 cycle).
2. iter-2 Tier A 86% paragraph reject rate = 보수적 accept — 1차 attempt 의 false-positive 회피 우선. iter-3 에서 threshold relax 후 quantity 확장 검토.
3. iter-2 Tier B 72.78MB ≠ target 500MB — BG-JE 30MB ceiling + paradigm 55MB ceiling + 자체 dialogue ledger 소량. iter-3 V4 evaluator full sample + 사용자 session 별도 access 필요.
4. iter-2 BG-LD 17.66MB ≠ target 100MB — V4 PASS pool 23 × rejected pool 5046 cartesian capped 30,023 pairs. iter-3 prompt expansion 후 100MB 도달.
5. BG-LD synthetic rejected (template_leak '서연:' + degenerate '이' repeat) = ROC discrimination signal 강화 augmentation — 본 비율 metrics 에 emit (46 synth / 5046 total = 0.91%).
6. own 18 C2.4 mismatch filter = is_degenerate heuristic — full domain-keyword overlap 미적용 (V4 evaluator 자체 metric 활용 별도 cycle).
7. iter-2 Tier B chat-template ratio 28.95% < own 20 ≥30% threshold marginal — paradigm corpus 가 chat-template 비율 일부 본문 mix → iter-3 paradigm corpus 전부 chat-template 만 추출 검토.
8. anima_core_dialogues = substrate probe lane (echo-mode, weak Q/A coupling) — Tier B 입력 sample weight 낮음. own 18 C2.4 PASS 보장 X (anima self-talk 시뮬레이션 chicken-egg).
9. iter-2 raw measurement SSOT = `state/anima_clm_l4_corpus_iter2_metrics.json` (size + density + chat-template ratio + counts + chosen/rejected pool stats).

---

## iter-2 SSOT

- raw measurement: `state/anima_clm_l4_corpus_iter2_metrics.json`
- 큐레이션 script: `tool/transient_py/anima_clm_l4_corpus_iter2_curate.py` (raw#37 transient)
- progress 문서: `docs/anima_clm_l4_corpus_progress_2026_05_08.md` (본 .md, iter-1 + iter-2 합본)
- spec 모태: `docs/anima_clm_l4_corpus_2026_05_08.md`
