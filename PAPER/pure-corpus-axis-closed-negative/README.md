# pure-corpus-axis-closed-negative — corpus-dilution 축으로는 multilingual coherence 를 닫을 수 없다

> PURE 도메인의 첫 정식 논문 (closed-negative). corpus 희석 축(wiki_frac)
> 단독으로는 multilingual coherence 를 closure 하지 못한다 —
> **register collapse ⊥ multilingual coherence (직교)**. 음성 결과를 정직하게
> 보고하며, 축 하나를 탐색 공간에서 배제(rule-out)한다.

## 한 줄 요지

4-point sweep (wiki_frac ∈ {0.0, 0.3, 0.5, 1.0}) 전 지점에서 closure
판정은 FAIL (1/4 PASS). register collapse 는 **차단**되지만
(`n_anima_register_hits_total` = 0 @ wiki_frac {0.0, 0.3, 1.0}),
multilingual coherence 는 **WEAK 유지** (최고 단일 lang = ru 13/20 PARTIAL
@ wiki_frac=0, 전 sweep 통틀어 유일한 non-WEAK). 두 축은 직교 →
corpus-dilution 축은 충분한 lever 가 아니다 (closed-negative).

## § 구조 (`a_paper_format`)

| 섹션 | 내용 | verdict 링크 (`a_paper_sections`) |
|------|------|-----------------------------------|
| §hypothesis (sec:hypothesis) | falsifier 사전등록 — "corpus-dilution 축이 multilingual coherence 를 closure 한다(H0)" 를 반증. F-COHERENCE(≥4/5 lang PARTIAL+) · F-REGISTER(hits<4) | — (pre-register) |
| §method (sec:method) | 4 fire (v3 wiki=0 · j02 wiki=0.3 · E2 wiki=0.5 · E3 wiki=1.0) + `closure_auto_judge` 직접 실행 + jq field-extract | `closure.txt` |
| §measurement (sec:measurement) | 4-point 표 (hits vs per-lang coherence) + aggregate 1/4 PASS + 직교 schematic (Fig.1, inline TikZ) | `closure.txt` · `register.txt` |
| §finding (sec:finding) | closed-negative: register ⊥ coherence, 축 배제. wiki 0.0→0.3 은 유일 PARTIAL(ru) 마저 떨어뜨림 | `closure.txt` · `register.txt` |

모든 섹션 주장은 `.verdicts/pure-corpus-axis-closed-negative/{closure,register}.txt`
verbatim verdict 에 링크 (`a_paper_sections`). 데이터는 result.json /
verdict txt 에 있는 값만 — 없는 값(wiki 0.5/1.0 per-lang row, motivation,
phi)은 TODO 로 표시 (날조 금지).

## 데이터 출처 (verbatim only)

- `state/pure_phase_d_v3_result_2026_05_24/result.json` (wiki_frac=0.0, sha `2643bd72a5c0e5a9`)
- `state/p21h_v3_recover_2026_05_25/out_main/result.json` (wiki_frac=0.3, sha `ab35a06e072f5d62`)
- `HEXAD/LIFE/H_242` §A2 4-point 표 (wiki 0.5/1.0 register count 인용)
- `CLAIMS.tape` group=PURE — `pure_wiki_sweep` + `pure_register_orthogonal` (둘 다 🔴 CLOSED-negative terminal)

## 빌드

```bash
make            # → main.pdf (pdflatex × 3 + bibtex)
make clean      # .aux/.log/.bbl 제거 (PDF 보존)
make distclean  # PDF 도 제거
```

`/paper compile PAPER/pure-corpus-axis-closed-negative` 도 동일.

## Figures

- `figures/_prompts/cover.txt` — fal.ai 커버 figure 프롬프트 (**deferred**,
  실제 생성 안 함). 승격 시 `/paper fig square_hd figures/_prompts/cover.txt figures/cover.png` 로 생성 후 main.tex 에 include.
- Fig.1 (orthogonality schematic) 은 main.tex 내부 **inline TikZ** — Python
  figure 파이프라인 없음 (hexa-only authoring directive: 신규 .py/.sh 금지,
  template 의 `_scripts/fig01_example.py` 는 제거).

## g51 충족 여부 (정직하게)

**WIP scaffold — g51 미충족.** commons `g51` 의 이상적 목표는
**컴파일 ≥10 페이지 + fal.ai figure ≥1개** 이나, 본 스캐폴드는:

- 페이지: skeleton 단계 — 본문(4 §)+표 2개+TikZ 1개로 컴파일은 되나
  ≥10 페이지는 본문/TODO row 를 더 채워야 충족.
- fal.ai figure: **deferred** (프롬프트만 staged, 실제 raster 미생성).
  Fig.1 은 TikZ 라 g51 의 "fal.ai figure" 요건은 아직 미충족.

본문(wiki 0.5/1.0 per-lang TODO row 포함)을 채우고 cover 를 생성하면
g51 충족. 무리하게 placeholder 로 페이지를 부풀리지 않음 (`a_paper_*` 정직성).

## 정직성 (honest stance)

- 모든 수치는 result.json / verdict txt verbatim. 없는 값은 TODO.
- 4 closure criteria 중 2개(motivation_8factor · dream_stage)는 이 run 들에서
  미계측 → 고정 FAIL. 직교 결론은 criterion 1(coherence)·2(register)에만 의존
  (§Limitations L-4). aggregate "1/4 PASS" 는 계측된 2축 기준 실제 격차(1/2)를
  과대표시함 — 본문에 명시.
- closed-negative 프레이밍 (`a_paper_negative_ok`): 음성 결과를 finding 으로
  정직하게. 양성 recipe 는 주장하지 않음 — 축 하나를 배제할 뿐.
