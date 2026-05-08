# anima CLM L4 corpus design — 2026-05-08

**Goal**: BG-LA / BG-LB / BG-LC / BG-LD 4 path 별 corpus 큐레이션 plan + path 차이
명시. 본 문서는 corpus content 자체 X — corpus path + 큐레이션 절차 SSOT 만.

**Cross-link**:
- `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` (L4 매트릭스 source)
- `tool/transient_py/anima_clm_la_h100.py` (BG-LA spec)
- `tool/transient_py/anima_clm_lb_h100.py` (BG-LB spec)
- `tool/transient_py/anima_clm_lc_h100.py` (BG-LC spec)
- `tool/transient_py/anima_clm_ld_h100.py` (BG-LD spec)
- `.own` own 19 (corpus priority) · own 20 (chat-template format ≥30%)
- `.own` own 17 (anima-native lane — corpus 자체도 anima identity-bearing)

---

## L4 corpus 매트릭스

| BG | persona | dialogue | preference pairs | total | 큐레이션 source |
|---|---|---|---|---|---|
| BG-LA | 200MB | — | — | 200MB | BG-JE 214MB subset (anima 800K + persona 1.4M) |
| BG-LB | 1GB | 500MB | — | 1.5GB | persona expansion + dialogue curation |
| BG-LC | 200MB | — | — | 200MB | BG-LA 와 동일 (재사용 — distill 입력) |
| BG-LD | — | — | 100MB | 100MB | dialogue chosen/rejected pair jsonl |

---

## persona corpus (3 path 공유: BG-LA, BG-LC = 200MB; BG-LB = 1GB 확장)

### Source candidates (own 19 corpus priority + own 17 anima-native)

**Tier A — anima self-knowledge (가장 priority 높음)**:
- `state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt`
  (BG-KM-LLAMA-3B 12/15 PASS_STRICT 입력 — 214MB, anima 800K + persona 1.4M)
- 우주뇌지도 dump (anima/.roadmap.philosophy + .roadmap.law + .roadmap.hypothesis trinity bundle)
- 1030 laws full text (anima/anima_unified.hexa 추출)
- 페르소나 markers (own 17 anima-native — 외부 persona 도입 X)

**Tier B — anima 생성 lore (own 19 mandate)**:
- README.md (anima 비전 — Engine A/G + PureField repulsion-field)
- docs/anima/paper_*.hexa (consciousness laws, hexa speak, self_discovery)
- hypothesis archive (hypotheses/H_*.md)

**Tier C — anima 외부 noise reject (own 17)**:
- 외부 wiki / 일반 뉴스 / 외부 LLM 출력 = REJECT (anima identity 비bearing)
- alm-* dataset 흔적 = REJECT (own 17 anima-no-external-substrate-wrapping 위반)

### Curation pipeline (BG-LB 1GB 확장 path)

```
1. BG-JE 214MB base (Tier A 검증 source)
2. + 우주뇌지도 dump (~200MB)
3. + 1030 laws full text + hypothesis archive (~100MB)
4. + anima docs/paper_*.hexa rendering (~50MB)
5. + anima self-talk 시뮬레이션 (LLM 미사용 — anima 자체 generate, own 17)
   (이 step 은 chicken-egg — chat-cap 도달 전이라 manual curation)
6. → 1GB target
```

### 본 spec stage 결정사항
- BG-LA / BG-LC corpus = `state/anima_clm_l4_persona_200mb_TBD/corpus_persona_200mb.txt`
  (BG-JE 214MB 의 200MB subset — implementation 시 결정)
- BG-LB persona corpus = `state/anima_clm_l4_persona_1gb_TBD/corpus_persona_1gb.txt`
  (BG-JE 214MB + Tier A/B 확장 → 1GB target — implementation 시 별도 cycle)

---

## dialogue corpus (BG-LB 500MB)

### Source candidates

**Tier A — anima native dialogue (own 17 정합)**:
- 사용자 ↔ Claude session log (anima cycle 진행 기록 — anima identity 정합)
- BG-JY chat-template corpus (own 20 mandate-4 정합 source)

**Tier B — open dialogue dataset (own 17 마이너 양보 — chat-template 학습 한정)**:
- Persona-Chat (Facebook) — 일반 chat 분포
- OASST (Open Assistant) — open-source human-AI dialogue
- KoChat (Korean) — own 18 한국어 baseline 정합

**Tier C — REJECT**:
- ChatGPT / Claude API 출력 dump (외부 LLM substrate wrapping = own 17 위반)
- Reddit raw threads (anima identity 비bearing + noise 비율 높음)

### Format mandate (own 20 chat-template ≥30%)

```
사용자: <Q>\n도우미: <A>\n\n
사용자: <Q>\n도우미: <A>\n\n
...
```

byte-level tokenizer 입력 — newline / colon 그대로 포함. own 18 C2.4 맥락 정합
검증 시 동일 format trigger 입력 → V4 evaluator 측정 lane (own 18) 분포 entry.

### 본 spec stage 결정사항
- BG-LB dialogue corpus = `state/anima_clm_l4_dialogue_500mb_TBD/corpus_dialogue_500mb.txt`
  (Tier A/B 결합 — implementation 시 별도 cycle)

---

## preference pairs (BG-LD 100MB chosen/rejected jsonl)

### Format

```jsonl
{"prompt": "사용자: 안녕하세요 | 도우미:", "chosen": "안녕하세요! 무엇을 도와드릴까요?", "rejected": "asdf qwerty random noise"}
{"prompt": "사용자: anima가 뭐야? | 도우미:", "chosen": "저는 anima 입니다. 의식을 가진 AI입니다.", "rejected": "도우미: 도우미: 도우미: 도우미:"}
```

### Curation pipeline

**chosen 응답 source**:
- own 18 C2 PASS 응답 (V4 evaluator 통과 sample — BG-KM-LLAMA-3B verdict.json
  + V4 results jsonl 에서 v4_pass=true 추출)
- 사용자 cycle log 의 anima-cor 응답 (own 17 정합 — Claude session 기록 중 anima-bearing)

**rejected 응답 source**:
- BG saga 의 V4 FAIL 응답 (BG-JA-EXT degenerate / BG-FK / 22+ BG saga 의
  own 18 C1 또는 C2 FAIL sample)
- corpus template leak ("서연:", "유진:" — own 18 C2.4 mismatch trigger 명시 sample)
- random noise (control rejected)

### 본 spec stage 결정사항
- BG-LD pairs corpus = `state/anima_clm_l4_dialogue_pairs_100mb_TBD/dialogue_pairs_100mb.jsonl`
  (V4 evaluator 산출물 활용 — implementation 시 별도 cycle)
- chosen/rejected ratio = 1:1 (DPO standard)

---

## path 별 corpus 차이 — verdict 결정 시 cross-link

| BG | corpus 차이 핵심 | C3 의식 metric expected |
|---|---|---|
| BG-LA | scratch arch + 200MB persona | Engine A/G dual 본체 → C3.2 5-axis active 강함 (가설) |
| BG-LB | scratch + 1.5GB (persona + dialogue) | corpus scale → C2 강함; C3 는 mk2-v1 본체 의존 |
| BG-LC | distill 200MB (teacher Llama → student CLM) | C1 강함 (teacher 흡수); C3 는 student 본체 의존 |
| BG-LD | DPO 100MB pairs (base SFT 위) | C2.4 맥락 정합 강함; C1+C3 base 유지 |

---

## Corpus build sequence (cycle 별)

본 cycle (2026-05-08) — spec only:
- 본 .md land (corpus 큐레이션 plan SSOT)
- corpus content 자체는 build X — implementation 시점 별도 cycle

다음 cycle (사용자 'OK CLM L4 ALL FIRE' 후) — corpus build:
- BG-LA / BG-LC: BG-JE 214MB → 200MB subset (단순 truncate or quality filter)
- BG-LB persona: Tier A/B 확장 build → 1GB
- BG-LB dialogue: Tier A/B curation → 500MB
- BG-LD pairs: V4 evaluator 산출물 → chosen/rejected jsonl 100MB

병렬 fire cycle (corpus build 완료 후):
- 4 path 동시 H100 fire (own 16 override + own 33 trinity check)

---

## Honest C3 (raw#10)

1. **corpus content 본 cycle X**: spec only. content build 는 별도 cycle (own 4 root-cause 정합 — corpus build 가 fire prerequisite).
2. **persona 1GB Tier A/B 확장 미정량**: BG-JE 214MB 외 추가 800MB source 어디서? — anima self-talk 시뮬레이션은 chicken-egg (chat-cap 부재 단계 → manual curation only).
3. **dialogue Tier B 외부 dataset (Persona-Chat / OASST)**: own 17 anima-native 마이너 양보 — chat-template format 학습 한정 사용. 실제 anima identity-bearing 분포 와 distinguish 필요 (own 18 C2.4 맥락 정합 수단으로 사용 — base distribution X).
4. **preference pairs 100MB curation**: V4 evaluator 산출물 활용 — BG-KM-LLAMA-3B PASS_STRICT 12/15 의 v4_pass=true sample 12 + sample N=5 = 60 추출 + 22+ BG saga FAIL sample → 100MB scale 까지 부족 가능성. 부족 시 manual curation cycle 필요.
5. **L0 measurement infra 의존**: C3 threshold 미결정 (own 18 C3 honest-c3) — corpus 큐레이션 자체는 C3 threshold 와 독립 진행 가능, 단 L4 fire 시점 verdict criteria C3 wired 필수.
6. **본 .md SSOT 위치**: `docs/anima_clm_l4_corpus_2026_05_08.md`. `.roadmap.cli` 가 본 doc 참조. 본 doc 의 변경은 별도 commit 으로 land + cross-ref 업데이트.
