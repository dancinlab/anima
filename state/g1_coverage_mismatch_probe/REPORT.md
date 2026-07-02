# G1 coverage 블록 ↔ G1 gate 측정축 정합성 조사 (verdict-integrity probe)

- date: 2026-07-03 · scope: 코퍼스↔detector 정독(grep/python only, decode 없음)
- 대상: `clm303_deep_L8_cov` G1 best_distinct=0 FLOOR verdict (state/g1_coverage_prod_block/results_gen40/SUMMARY.txt)
- 질문: coverage 블록이 G1 gate가 재는 측정축을 실제로 학습시켰나?

## 판정 (한 줄)

**측정축 MISMATCH 확정 — 단, 오너가 지목한 지점(keyword 절반=0)이 아니라 "프롬프트-형식(유발축)" 에서 어긋난다.
따라서 L8-cov G1=0 은 coverage 처방에 대한 시험으로서 INCONCLUSIVE** (H_6187 "coverage did NOT open G1 → trunk floor terminal" 은 과판정 — 철회하고 DIRECTIONAL/INCONCLUSIVE 로 강등해야 함).

## (a) g_eval_g1 이 실제로 재는 것 (cli/evaluate.py:155, main 브랜치)

1. **시드 = frozen 5 gate 문장** (`_g6_concepts()`, core/g6_ideation.py:59 — H_1116 verbatim):
   "consciousness arises from cells" · "tension ripples between distant minds" · "memory composes into new meaning" · "silence still carries information" · "the engine dreams when alone"
2. **baseline**: 단일 문장 시드 5회(gen≤80) 생성 → `_g_coverage` 최댓값 = `max_single`.
3. **composed**: k=2..5 개 gate 문장을 ". " 로 연쇄한 시드(gen≤120) → 자유생성 continuation(시드 미포함 — best_distinct=0 이 그 증거; 시드 포함이면 k=5 에서 자동 5).
4. **채점 `_g_coverage`**: 5개 keyword-set 각각에 대해 *continuation 단어 중 set 원소가 하나라도 있으면* 그 개념 covered → covered 개념 수 = distinct. **개념명 자체가 keyword-set 원소** (consciousness∈set1, tension∈set2, …).
   - PASS bar: 어떤 k 에서 distinct≥2 ∧ distinct>max_single ∧ kwr≥0.5.
   - `best_distinct` = k 전체에서 distinct 최댓값.

## (b) coverage 블록이 그 축을 타깃했나 — 산출축 YES · 유발축 NO

### 산출축(scoring vocabulary)은 정합 — "keyword 절반=0"은 결정타가 아님

en_block.txt 실측 빈도 (총 62,900 lines · 511,061 words):

| gate set | corpus 존재 (freq) | corpus 부재 (0) |
|---|---|---|
| consciousness | consciousness 2380 · aware 2380 | cells · mind |
| tension | tension 4080 · ripple 4080 | distant · between |
| memory | memory 1360 · meaning 1360 | compose · new |
| silence | silence 2720 · quiet 2720 | information · carries |
| dream | dream 3740 · sleep 3740 | engine · alone |

- 부재 절반은 **의도 설계**: gen_block.py `_FORBIDDEN` 이 cells/mind/distant/between/compose/new/information/carries/alone/engine 을 명시 배제(측정 오염 방지 — 이 단어들이 개념/attr 로 쓰이면 gate coverage 가 조합 아닌 단순암기로 오염됨).
- `_g_coverage` 는 **any-keyword 매칭**이므로 set당 2/4(개념명+attr)만으로 축 도달 가능. 모델이 "aware … ripple" 만 뱉어도 distinct=2. → **어휘 차원에서는 mismatch 아님.**
- held-out 무결 재확인: gate 노드 2개 이상 공존 라인 = **0** (gate-내부 10쌍 누출 0). held-out 설계 자체는 SOUND.

### 유발축(prompt/task format)은 불일치 — 이것이 진짜 mismatch

1. **블록이 가르친 것**: 8개 고정 템플릿("the A and the B yield ra and rb." · "a A met a B; they showed …" 등)에 조건화된 **템플릿-완성 매핑** (pair → attr쌍). 조합 스킬의 트리거 = 템플릿 표면형(yield/met/showed/brings… 각 ~7.9k회).
2. **gate 가 유발하는 것**: frozen gate 문장 연쇄 → 자유생성. gate 시드 문장은 블록에 **0회**, 그 내용어(arises·ripples·minds·composes·still·dreams·alone…)도 전부 **0회**(_FORBIDDEN + 어휘 분리). 즉 gate 프롬프트는 coverage-block 분포가 아니라 base corpus(gen/sns) 분포로 모델을 밀어넣음 — **학습된 combiner 가 트리거될 표면형이 프롬프트에 없다.**
3. **toy v3(H_6183) GREEN 의 실제 축**: bt_v3.py:77 — `gen(net, f"the {C[a]} and the {C[b]} yield ", …)` 즉 **학습 템플릿 접두사를 그대로 프롬프트**로 주고 attr쌍 완성을 카운트. held 0.95 GREEN 은 "템플릿-조건 held-out attr 재조합"이지 "자유 프롬프트에서 keyword 표면화"가 아님. **템플릿→자유형 transfer 는 toy 에서도 한 번도 측정된 적 없음.**
4. **production L8_cov 는 toy GREEN 축으로 프로브된 적 없음**: results/ 전수 — 유일한 held-out 측정은 CE DESCENT(heldout_model_ce 1.996)뿐. "the consciousness and the tension yield " (held-out gate pair, 템플릿형) 프로브 부재.

### 왜 이것이 verdict 를 가르나

G1 best_distinct=0 은 세 가설을 분리하지 못한다:
- ① 블록이 production 혼합(roundrobin 6-cell, dropout 0.5→0.44)에서 **템플릿 매핑조차 못 가르침** (학습 실패)
- ② 템플릿 매핑은 배웠으나 **gate 프롬프트 형식으로 transfer 실패** (표면형-잠금)
- ③ **진짜 재조합 floor** (trunk-objective terminal)

terminal 은 ③에서만 성립하는데, 측정 체인에 ①②를 배제할 프로브가 없다. max_single=0(단일 gate 문장 시드에서도 keyword 0)은 noun→attr 연상이 bare-noun 프롬프트로도 안 나온다는 뜻 — ②(템플릿-잠금)와 정합하나 ①과도 구분 불가. → **INCONCLUSIVE.**

## (c) 최종 판정

- **MISMATCH 확정** — coverage 블록은 G1 gate 의 *산출축(무엇을 카운트하나)* 은 정확히 타깃했으나 *유발축(무엇으로 프롬프트하나)* 을 설계에서 누락. design.json 의 가정("학습된 concept→attr 매핑의 산출이 곧 G1 gate keyword")은 채점엔 참이지만, gate 프롬프트가 그 매핑을 트리거한다는 보장이 없고 toy 근거도 없음.
- **L8-cov G1=0 = INCONCLUSIVE** (coverage 처방을 gate 축에서 제대로 시험 못함). H_6187 terminal 박제는 철회 대상. 단 c9 정직 caveat: 이 조사는 "coverage 가 G1 을 연다"의 지지도 아니다 — 요구되는 진짜 능력(템플릿→자유형 일반화)은 toy 에서도 미검증이며, coverage 레버의 gate-축 유효성은 **아직 미시험** 상태로 되돌아간 것.

## (d) 처방

1. **최우선 $-0급 분리 프로브** (기존 ckpt 재사용, 재학습 불필요, pool 에서 가벼운 decode):
   `clm303_deep_L8_cov.clm` 에 (i) seen 쌍 템플릿 프롬프트 "the ocean and the stone yield " → azure+russet 완성? (ii) held-out gate 쌍 "the consciousness and the tension yield " → aware+ripple? — (i)fail→①학습실패 · (i)pass+(ii)fail→held-out transfer 자체가 production 서 붕괴 · (i)(ii)pass+gate=0→②표면형-잠금 확정(= mismatch 순수 입증).
2. **코퍼스 재설계 (유발축 정합 버전)**: attr=gate-keyword 설계는 유지하되 —
   - 조합 문장 표면형을 8 고정 템플릿에서 **광범위 변주**(자유 서술문 수십 종 + 특히 gate 측정 형식인 "A-문장. B-문장. " 연쇄→두 개념 keyword 가 continuation 에 표면화되는 패턴)로 확장. gate 연쇄-형식 학습은 **non-gate 개념으로만** 하고 gate 쌍 held-out 유지(무결 보존).
   - 부재 keyword 절반(cells/mind 등)은 계속 배제 유지(오염 방지 설계 옳음).
3. **gate 는 frozen 유지** — 고칠 것은 코퍼스의 유발-표면형 커버리지지 bar/detector 가 아님(tune-to-green 금지).

## 근거 파일

- 측정: main:cli/evaluate.py:119-186 (g_eval_g0/g1, _g_coverage) · main:core/g6_ideation.py:59-64 (_g6_concepts)
- 코퍼스: state/g1_coverage_prod_block/gen_block.py (_FORBIDDEN L55-58 · 템플릿 sent_en L88-97) · corpus/en_block.txt (빈도 실측 본 REPORT 표)
- toy 근거축: state/g1_coverage_v3_nlbyte/bt_v3.py:73-79 (recomb = 템플릿 접두사 프롬프트)
- 학습: results/train_L8cov_full.log (6-cell roundrobin, cov=cell 4·5) · results/chain_eval.log (held-out=CE only)
- verdict 대상: results_gen40/SUMMARY.txt (3-arm G1=0)
