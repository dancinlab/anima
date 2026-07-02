# H_6185 follow-on — 정확한 HF 4칸 production 코퍼스 재측정 (proxy→정확HF 승격)

**날짜:** 2026-07-02 · **수행:** fable(자율, write/network 권한 세션) · **방법:** H_6185 reference-match
**목적:** H_6185 가 로컬 프록시 trainset 으로만 측정해 DIRECTIONAL-**proxy** 강등 → 정확한 HF 코퍼스 직접 측정으로 proxy 딱지 제거.

## TLDR — verdict

**임계 한참 아래 (BELOW) 확정 — 결론 불변, proxy 딱지 제거 가능.**
정확 HF 4칸(127.6MB · 674,797라인)에서 G1 frozen 개념쌍 10쌍의 HEAD-tier 공동출현 = **총 15라인**(7/10쌍 ≥1 · 쌍당 0~7회), 쌍-밀도 = **0.118 pair-lines/MB ≈ toy 임계(HIGH arm 17,143/MB) 의 1/145,000**. 프록시의 "0/10=0%"는 정확 HF 에서 "sparse-nonzero"로 스케일됐지만(예측대로 수치만 스케일), toy 임계 체계(쌍-type ≥20% × ~30 reps + 밀도)와 4~5자릿수 격차는 그대로 → **커버리지-bound 활성 판정 불변**. RF-bound(31B ≪ 72B)는 코퍼스 무관이라 재측정 불요(H_6185 확정 유지). 표기는 여전히 **DIRECTIONAL**(engine-native 아님) — 단 "-proxy" 한정자는 제거.

## (a) 확보한 HF 코퍼스 (exact production 4칸, `hf download dancinlab/anima-corpus-*`)

| cell | bytes | lines | words |
|---|---|---|---|
| en-general | 60,049,637 (60.0MB) | 279,429 | 10,088,193 |
| ko-general | 60,000,356 (60.0MB) | 340,512 | 6,765,669 |
| ko-sns | 6,183,822 (5.9MB) | 47,994 | 695,507 |
| en-sns | 1,326,111 (1.3MB) | 6,862 | 210,355 |
| **합계** | **127.6MB** | **674,797** | **17.76M** |

H_6185 외삽 가정 검증: en-general 60MB = 프록시 영어분(≈4MB)의 **~15배** ✓ · "HF-only 128MB" ✓ · **HEAD 공동출현 15라인 전부 en-general 발**(ko-general·en-sns·ko-sns = 0쌍) = "G1 유효 셀은 en-general 하나" ✓.

## (b) 수치 — HEAD-tier (본판정, 개념 헤드어 라인-window · \b · case-insensitive)

**marginals (HF 합계):** consciousness 139 · tension 156 · memory 699 · silence 169 · dream|engine 1,256

**10쌍 공동출현 (HF exact | 프록시 재현):**

| 쌍 | 라인-window | ±5라인 | 프록시(라인) |
|---|---|---|---|
| consciousness×tension | 1 | 3 | 0 |
| consciousness×memory | 3 | 12 | 0 |
| consciousness×silence | 1 | 5 | 0 |
| consciousness×dream\|engine | 1 | 13 | 0 |
| tension×memory | 0 | 8 | 0 |
| tension×silence | 1 | 2 | 0 |
| tension×dream\|engine | 0 | 7 | 0 |
| memory×silence | 1 | 5 | 0 |
| memory×dream\|engine | 7 | 44 | 0 |
| silence×dream\|engine | 0 | 9 | 0 |
| **합계** | **15** | **108** | **0** |

**실라인 전수 검수(15라인, `cooc_lines_head.txt`):** 대부분 자연 web 의 일상적 공동사용(소설·가사·뉴스: "tension-filled silence" · "consciousness shook, cracks in my memory" · "childhood memory → seed of a dream")이고, 최소 1건은 순수 다의어 충돌(patent: spool **memory** × print **engine**), "stream-of-consciousness" 복합어 매칭 포함. 즉 15라인조차 관대한 상한이다.

**FULL-tier (4키워드 any×any, 관대 상한):** C1×C2=146 · C1×C3=317 · C1×C4=116 · C1×C5=99 · C2×C3=593 · C2×C4=204 · C2×C5=126 · C3×C4=582 · C3×C5=298 · C4×C5=81 — 합계 2,562라인(0.38%), 프록시와 동일하게 new/between/information 범용어 충돌 지배.

**control 일반쌍 (파이프라인 무결):** government×war=**125** · music×(school|history)=**133** · water×(city|energy)=**208** — 전부 >0 ✓. 동시에 일반쌍조차 밀도 ~1-1.6/MB = 자연 web 텍스트의 본질적 pair-희박성 재확인.

**silence 정직 audit:** HF en-general silence 163라인 중 프랑스어 힌트 **1건뿐**(영어 문맥 162) — H_6185 의 "le silence" 오염(프록시 enrichment 511중 402 프랑스어)은 **프록시 특유 artifact** 였고 정확 HF 에는 사실상 없음. HF silence marginal 은 깨끗한 영어다.

## (c) 프록시 대조 + 임계 판정

- **프록시 재현 = H_6185 원수치와 완전 일치** (marginals 3/6/9/514/76 · HEAD 10쌍 0 · FULL 5/4/0/1/18/30/5/67/2/7 · control 15/4/2) — reference-match 성립.
- **차이:** 프록시 0/10 → HF 7/10쌍 sparse-nonzero(쌍당 0~7). H_6185 의 외삽 예측("기대 ≈0~1라인/쌍")과 자릿수 일치(memory×dream|engine 만 7로 소폭 상회, 다의어 포함).
- **임계 대비:** toy HIGH(상전이 위) = 17,143 pair-lines/MB vs HF exact = 0.118/MB → **1/145,000**. ±5win(108 events)로 봐도 1/20,000. "쌍당 ~30 reps" bar 는 라인-window 기준 10쌍 전부 미달(최대 7).
- **minor delta (정직):** 원보고 "±5라인 window 도 0" vs 본 재현 프록시 ±5win 에서 silence×dream|engine=7 검출 — 전수 검수 결과 **동일 2행 시 모티프**("lucid dream / the silence keeps for itself") 영어 5반복+프랑스어 2 = 유니크 1텍스트. window 카운팅 구현 차이며, 유니크-type 관점에선 원보고와 정합. 결론 무영향.

## (d) 산출물

- `measure_hf_exact.py` — 단일-패스 측정기(HEAD/FULL/±5win/control/silence-audit, HF 4칸+프록시 3파일 동시)
- `results.json` — per-file + aggregate 전수치 (HF 4칸 · 프록시 3파일)
- `extract_cooc_lines.py` + `cooc_lines_head.txt` — HEAD 공동출현 15라인 원문(검수 증거)
- `measure.log` — 실행 로그 (mini 로컬, 19.2s)
- 코퍼스 자체는 착지 안 함(127.6MB, `hf download dancinlab/anima-corpus-{ko,en}-{general,sns} --repo-type dataset` 로 재현)

## (e) bookkeeping 지시 (로컬 에이전트)

H_6185 verdict: DIRECTIONAL-**proxy** → DIRECTIONAL(**정확HF**) 승격. BELOW 판정·이중 bound(커버리지+RF 과잉결정)·처방(L=8 RF 먼저 + 조합-커버리지 블록 합성) 전부 불변. engine-native 재검은 별도 follow-on 유지.
