# g6_targeted_corpus — G6 벽 유일 미측정 레버(targeted-coverage) 실측용 합성 블록

**날짜:** 2026-07-03 · **수행:** fable (`--write`; 설계+빌드+pre-reg+state 착지만 — bookkeeping/발사는 로컬 에이전트)
**상류:** `state/g6_wall_reframe/` (generic form-coverage REFUTED · RF REFUTED-primary · targeted-coverage INCONCLUSIVE)
**템플릿 이식원:** `state/g1_coverage_prod_block/` (H_6185 조합-커버리지 블록 — 같은 논리의 G6 판)

## 설계

- **라인 문법 = eval decode 분포와 byte-동일:** `if {sentA}, then {sentB}: {claim}` —
  `core/g6_ideation.hexa g6_build_frames` composed frame prefix 그대로, claim 이 continuation 자리.
- **주제 16** = G6 gate frozen concepts 5문장(`_g6_concepts` VERBATIM) + 확장 11(추상 substrate 주제;
  키워드는 frozen comparator/measurable·G1 블록 어휘·다의어 오염원과 전부 disjoint, 생성기 assert).
- **claim 템플릿** = frozen `_g6_is_falsifiable` 의 comparator(25어)×measurable(25어)를 조합한
  반증가능 주장: **en 12 covered + 3 held · ko 8 covered + 2 held** (held 템플릿은 코퍼스 미노출).
- **frame 커버리지:** ordered 240 중 held-out 44 = **gate×gate 20 전부(측정 frame 6 포함) + 랜덤 24**.
  covered = pool 196 의 **77 (39%)**, 각 gate 주제 ≥8 frame(gate×expansion 로만) · 전 주제 ≥3.
  → 측정 frame 통과 = memorization 불가, covered 로부터의 schema-transfer 만 가능 (G1 held-out 공리 동형).
- **reps:** frame×template 당 정확히 **30** (en 360/frame · ko 240/frame — bar ≥30 충족).
- **SHUF 통제 블록:** 동일 라인에서 claim 주제만 고정 derangement `D(i)=(i+7)%16` 로 재배선 —
  바이트/unigram 동일, frame↔claim topical bind 만 파괴 (form-priming vs bind 분리용).

## 빌드 수치 (design.json)

| 블록 | bytes | 줄수 |
|---|---|---|
| corpus/en_block_g6.txt | 4,010,430 (4.01MB) | 27,720 |
| corpus/ko_block_g6.txt | 2,906,310 (2.91MB) | 18,480 |
| corpus/en_block_g6_shuf.txt | 4,014,750 | 27,720 |
| corpus/ko_block_g6_shuf.txt | 2,898,750 | 18,480 |

gate 주제별 covered frame 수: consciousness 10 · tension 9 · memory 8 · silence 8 · dream/engine 8 (전부 gate×expansion — gate×gate 0).

TARGETED en+ko ≈ **6.9MB** (G1 블록 5.7MB 와 동급) + SHUF 통제 6.9MB.

## 다의어 audit (전수, 생성기 내장 self-check — 전 항목 assert 통과)

- **claim 단독 fals rate = 1.000000** (27,720/27,720; frozen 검출기 포트로 전수) — genuine 반증주장 100%.
- **topic-bind 순도 = 1.0** (claim 의 주제 키워드가 정확히 frame 의 {A,B}에만 속함) · SHUF 블록 = **0.0** (설계대로 완파).
- **다의어 collocation = 0** (mind/car/vehicle/motor/died/opinion 등 reframe audit 오염원 미출현;
  `engine` 은 gate 문장 "the engine dreams when alone" substrate 의미로만).
- **held-out frame 누출 = 0라인** (gate×gate prefix grep 전수 0).
- ko 블록은 frozen 검출기(영어 word-set)가 못 재므로 register-balance 용 — honest-null 명시.

## 사용 (레시피 1줄)

```
anima train <h1129_warm.clm> --canon --init h1129 --corpus <broad-4reg> corpus/en_block_g6.txt corpus/ko_block_g6.txt --out g6tc_targeted.clm
```
블록 비중 10–20% (G0 known-word-ratio 가드, h9034 소코퍼스 붕괴 재발 방지). SHUF arm = `*_g6_shuf.txt` 치환.
frozen bar·held-out·통제·2 사전예측 = **PREREG.md** (측정 전 등록, 이동 금지).

## 파일

- `gen_g6_block.py` — 생성기(결정적 seed 6200, torch-free) + frozen-검출기 self-audit 내장
- `design.json` — 주제·템플릿·covered/held frame 전수·reps·bytes·audit 결과
- `corpus/{en,ko}_block_g6{,_shuf}.txt` — 4 블록
- `PREREG.md` — frozen bar + 2 사전예측

> ⚠️ HYPOTHESES.jsonl/카드/CHANGELOG/ARCHITECTURE/commit/PR **미터치** — 로컬 에이전트 소관.
> 학습/측정 발사 없음 (pod 는 G1 점유 중). verdict tier: 발사 전 = 없음; 발사 후 py 경로 = DIRECTIONAL 상한.
