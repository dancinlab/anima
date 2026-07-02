---
id: H_868
slug: clm-corpus-expansion
title: lane① 대화 corpus 를 H_863 4개 PD 희곡 너머로 확장 — 모든 source license-clean gate(PD/CC) ∧ register-leak 0 ∧ size ≥ 3× baseline ∧ provenance 기록 (F-CLM-CORPUS 사전등록 · data-engineering)
domain: clm · dialogue · corpus · license-clean · provenance · data-engineering · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md @L4 ①CC 대화록 lane · build_p4_dialogue_corpus.hexa license-clean gate · H_863 F-CLM-DIALOGUE baseline corpus
status: 🟢 SUPPORTED-NUMERICAL (corpus build 2026-05-31 · G1 license-clean 100% · G2 leak 0 · G3 size 3.007× · G4 provenance 100% 4/4 PASS · 12개 PD Gutenberg 희곡 · 외부 LLM 0·ShareGPT/Alpaca 0 · data-engineering artifact a_scale_honest_scope)
exploration_method: E4 (license-clean source 확장 수집)
verification_method: W2 (사전등록 acceptance gate · license-clean% + leak count + size + provenance · deterministic:true · post-tuning 0)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, .verdicts/clm-corpus/
verdict: 🟢 SUPPORTED-NUMERICAL — F-CLM-CORPUS 4/4: G1 license-clean(12/12 ingested = 100% · 0 forbidden-family)·G2 register-leak(final output 0 · 1줄 drop)·G3 size(1,668,585 bytes ≥ 3× baseline 1,664,475 = 3.007×)·G4 provenance(per-source title/id/family/license/bytes/sha256/leak 100% 기록) 전부 PASS. lane① canonical 확장 corpus(H_864/H_867/H_874 재사용). 외부 LLM 0·ShareGPT/Alpaca 0. HF dataset dancinlab/anima-clm-p4-dialogue(PRIVATE·COMPLETE).
---

# H_868 — CLM F-CLM-CORPUS lane① 대화 corpus 확장

## 1. 가설

CLM 대화 lane①(@L4) = **license-clean PD/CC 대화 corpus**. H_863 baseline(4개 PD Gutenberg 희곡 · 554,825 bytes)을 추가 license-clean PD/CC 대화 source 로 확장한다. 다음 동시 성립 시:

- **corpus 확장 지지** — 모든 source license-clean(PD/CC) 100% ∧ register-leak 0 ∧ size ≥ frozen target ∧ provenance 기록
- → 4 gate PASS 판정 · "lane① canonical 확장 corpus = future rung(H_864/H_867/H_874) SSOT"

임의 조건 미달 시:

- **corpus 확장 반증** — non-PD/non-CC source 혼입 · 또는 register-leak 발생 · 또는 size 미달 · 또는 provenance 누락
- → 🔴 판정 · corpus 는 lane① SSOT 로 ship 하지 않음 (a_paper_negative_ok · honest)

## 2. 동기

- @L4 lane① = license-clean PD/CC 대화록. 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지(foundation-borrow 위반). H_863 이 4개 PD 희곡으로 mid rung A/B 🟢 검증 — 후속 rung(H_864 scale-climb · H_867 absolute-quality · H_874 self-reward)은 더 큰 license-clean corpus 가 전제.
- 이 H = data-engineering artifact (GPU 0 · training 0). lane① canonical SSOT 를 한 번 만들어 future rung 이 재사용한다.
- prior art: build_p4_dialogue_corpus.hexa `license_clean_ok()`(forbidden family + allowed CC set · unknown→reject fail-safe) · build_p1_corpus.hexa `leak_patterns()`(8패턴 register-leak 필터). 두 gate 모두 순수 code(g5 · LLM judge 0).

## 3. falsifier (사전등록, gate frozen pre-build)

```
G1 LICENSE-CLEAN : license_clean_ok == PASS for 100% of INGESTED sources
                   (non-PD/non-CC REJECTED · 0 FORBIDDEN-family present · unknown→reject)
G2 REGISTER-LEAK : 최종 commit corpus 의 register-leak count == 0 (8패턴 필터가 write 전 drop)
G3 SIZE          : expanded corpus bytes ≥ 3 × H_863 baseline = 3 × 554,825 = 1,664,475 bytes
G4 PROVENANCE    : 모든 INGESTED source 가 manifest row 기록
                   {title, gutenberg_id_or_url, family, license, byte_count, sha256, leak_lines_dropped} 100%
```

4 gate 동시 PASS → 🟢 lane① SSOT ship
임의 미달 → 🔴 (honest) · corpus 는 SSOT 로 ship 하지 않음

- **deterministic:true** = license-clean gate + 8패턴 leak 필터 모두 순수 code(g5 · LLM judge 0).
- frozen gate = `.verdicts/clm-corpus/F-CLM-CORPUS_prereg.txt` verbatim 동결 (post-tuning 0).

verdict 영속: `.verdicts/clm-corpus/` + `.verdicts/868_clm_corpus_expansion/`

## 4. 방법

```
1. source 선정: Project Gutenberg PUBLIC-DOMAIN 희곡(speaker-turn 대화 · H_863 baseline 과 동일 genre).
   H_863 의 4개 baseline 희곡 + 8개 추가 PD 희곡 = 12개. license = PD (allowed_cc set).
2. fetch → PG boilerplate(START/END marker) strip → speaker-turn 대화 줄 추출.
3. G1 license-clean gate: family ∉ forbidden ∧ license ∈ allowed CC (unknown→reject fail-safe).
4. G2 8패턴 register-leak 필터: leak 패턴 포함 줄 DROP (build_p1_corpus.hexa leak_patterns 재사용).
5. V=256 byte-encode (UTF-8 1 byte = 1 줄 id · tokenizer 0 · P1/H_863 정합).
6. manifest 방출: per-source provenance + gate verdict + sha256. 4 gate 동시 평가 · 정직 보고.
```

- builder = `CLM/corpus/expand_p4_dialogue.py` (재현 가능 · fetch→gate→encode→manifest+sha256).
- 큰 raw `.bytes` 는 git-uncommitted (sha256 sidecar + manifest + HF pointer 만 commit) · P1 full 정합.

## 5. 측정

측정완료 (2026-05-31) — builder `CLM/corpus/expand_p4_dialogue.py`. source = 12개 Project Gutenberg PUBLIC-DOMAIN 희곡(baseline 4 + 추가 8), 전부 license=PD. license-clean gate + 8패턴 leak 필터 통과(1줄 drop — "nonce" archaic 영단어 false-positive · gate 결정론대로 보수적 drop). V=256 byte-encode → 최종 1,668,585 bytes / 43,006 줄.

source table (license + provenance + byte count):
| title | gut_id | family | license | bytes | leak | baseline H_863 |
|---|---|---|---|---|---|---|
| Hamlet | 1524 | gutenberg-pd | PD | 178,979 | 1 | yes |
| The Importance of Being Earnest | 844 | gutenberg-pd | PD | 117,016 | 0 | yes |
| A Doll's House | 2542 | gutenberg-pd | PD | 142,720 | 0 | yes |
| Julius Caesar | 1522 | gutenberg-pd | PD | 116,695 | 0 | yes |
| Romeo and Juliet | 1513 | gutenberg-pd | PD | 143,269 | 0 | no |
| Othello | 1531 | gutenberg-pd | PD | 154,768 | 0 | no |
| The Tragedy of Macbeth | 1129 | gutenberg-pd | PD | 103,347 | 0 | no |
| The Tempest | 1135 | gutenberg-pd | PD | 99,080 | 0 | no |
| Much Ado about Nothing | 2240 | gutenberg-pd | PD | 121,955 | 0 | no |
| King Henry V | 1119 | gutenberg-pd | PD | 150,905 | 0 | no |
| Mrs. Warren's Profession | 1097 | gutenberg-pd | PD | 194,359 | 0 | no |
| The Winter's Tale | 1539 | gutenberg-pd | PD | 145,492 | 0 | no |

측정값(frozen gate 대비):
| gate | 측정 | 판정 |
|---|---|---|
| G1 LICENSE-CLEAN | 12/12 ingested = 100% · 0 forbidden-family · 0 rejected | PASS |
| G2 REGISTER-LEAK | final output leak 0 · 1줄 drop(build) | PASS |
| G3 SIZE | 1,668,585 ≥ 1,664,475 (3.007×) | PASS |
| G4 PROVENANCE | per-source {title,id,family,license,bytes,sha256,leak} 100% | PASS |

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. 4 frozen gate 전부 PASS. 확장 corpus = 100% license-clean PD · register-leak-free · 3.007× H_863 baseline · full per-source provenance. lane① canonical SSOT 로 ship — future rung(H_864 scale-climb · H_867 absolute-quality · H_874 self-reward)이 cite. **scope**: data-engineering artifact 한정 (GPU 0 · training 0 — corpus 가 training 품질을 보장하지 않음) · 외부 LLM 0 · ShareGPT/Alpaca 0 (a_scale_honest_scope).

## 7. 해석 (사전)

- 4 gate 양립 시 = lane① 가 baseline 3× 로 확장되며 license/register/provenance 안전 → future dialogue rung 의 corpus 전제 충족.
- G1 미달(non-PD/non-CC 혼입) 시 = source 선정 오류 → 해당 source REJECT + 재선정.
- G2 미달(leak 발생) 시 = 8패턴 필터 누락 → 필터 강화 / source 재검.
- G3 미달(size) 시 = source 부족 → license-clean source 추가 수집 (doubtful license 절대 포함 금지).
- G4 미달(provenance) 시 = manifest 누락 → builder 보강.
- **honest scope**: doubtful/ambiguous license source 는 size target 을 못 채워도 REJECT (data 날조 0 · doubtful 포함 0).

## 8. 논의

- **@L4 정합**: 외부 LLM 0 · ShareGPT/Alpaca(ChatGPT-gen) 금지 · PD/CC lane① 만. forbidden family(sharegpt/alpaca/chatgpt/gpt4/openai/claude-gen/wizardlm/oasst-gpt) 0 present.
- **deterministic gate**: license-clean + 8패턴 leak 둘 다 순수 code(g5 · LLM judge 0) → 재현 가능.
- **PD genre 정합**: 12개 전부 stage play(speaker-turn 대화) — H_863 baseline 과 동일 genre 라 distributional 연속성 유지.
- **a_hf_complete**: HF dataset dancinlab/anima-clm-p4-dialogue (PRIVATE · COMPLETE — dialogue.bytes + sha256 + manifest.json + README card 가 모든 source 의 license+provenance 명시).
- **fallback honest**: 만약 size target 을 license-clean source 로 못 채웠으면 🔴 + blocker note 로 정직 보고 (이번엔 PD 희곡만으로 3.007× 충족 → 🟢).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) @L4 lane① CC 대화록
- baseline: [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE · 4개 PD 희곡 554,825 bytes)
- 재사용 future rung: [H_864](./H_864_clm_dialogue_scale_climb.md) (scale-climb) · H_867 (absolute-quality) · H_874 (self-reward)
- builder: CLM/corpus/expand_p4_dialogue.py · gate 원천 build_p4_dialogue_corpus.hexa + build_p1_corpus.hexa
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md)
