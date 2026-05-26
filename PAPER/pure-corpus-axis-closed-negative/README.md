# pure-corpus-axis-closed-negative — corpus-dilution 축으로는 multilingual coherence 를 닫을 수 없다

> PURE 도메인의 첫 정식 논문 (closed-negative). corpus 희석 축(wiki_frac)
> 단독으로는 multilingual coherence 를 closure 하지 못한다 —
> **register collapse ⊥ multilingual coherence (직교)**. 음성 결과를 정직하게
> 보고하며, 축 하나를 탐색 공간에서 배제(rule-out)한다.

## 한 줄 요지

4-point sweep (wiki_frac ∈ {0.0, 0.3, 0.5, 1.0}) 전 지점에서 closure
판정은 FAIL (1/4 PASS). register collapse 는 **차단**되지만
(`n_anima_register_hits_total` = 0 @ wiki_frac {0.0, 0.3, 1.0}),
multilingual coherence 는 어느 지점에서도 **1/5 langs PARTIAL+ 를 넘지
못함** (4/5 closure bar 대비 1/4 수준). 최고 단일 PARTIAL = ru 13/20 @
wiki_frac=0, 그리고 ko PARTIAL @ wiki_frac=1.0 (E3) — 둘 다 1/5 에 그침.
두 축은 직교 → corpus-dilution 축은 충분한 lever 가 아니다 (closed-negative).

## § 구조 (`a_paper_format`)

| 섹션 | 내용 | verdict 링크 (`a_paper_sections`) |
|------|------|-----------------------------------|
| §related (sec:related) | persona/style FT mode-collapse · multilingual LM/cross-lingual transfer · corpus dilution data-mixing 선행 위치 | — (background) |
| §hypothesis (sec:hypothesis) | falsifier 사전등록 — "corpus-dilution 축이 multilingual coherence 를 closure 한다(H0)" 를 반증. F-COHERENCE(≥4/5 lang PARTIAL+) · F-REGISTER(hits<4) | — (pre-register) |
| §method (sec:method) | 4 fire (v3 wiki=0 · j02 wiki=0.3 · E2 wiki=0.5 · E3 wiki=1.0) + corpus/model config(Qwen2.5-1.5B+mitosis) + `closure_auto_judge` 직접 실행 + jq field-extract | `closure.txt` |
| §measurement (sec:measurement) | 4-point 표 (hits vs per-lang coherence) + aggregate 1/4 PASS + per-lang bar(Fig.2 TikZ) + 직교 schematic (Fig.3 TikZ) | `closure.txt` · `register.txt` |
| §finding (sec:finding) | closed-negative: register ⊥ coherence, 축 배제. wiki 0.0→0.3 은 PARTIAL(ru) 마저 떨어뜨림 | `closure.txt` · `register.txt` |
| §discussion (sec:discussion) | 왜 corpus 축이 coherence 못 잡는지 (register=surface n-gram ⊥ coherence=cross-lingual semantic) + redirected search | — (analysis) |
| §limitations (sec:limits) | 4-point(not 5) · 2-point anti-helpful · coarse metric · motivation/dream 미계측(2/4 고정 FAIL) · E2/E3 per-lang n.c. | — (caveats) |

Fig.1 = fal.ai cover (`figures/cover.png`, gpt-image-2) · Fig.2/3 = inline TikZ.

모든 섹션 주장은 `.verdicts/pure-corpus-axis-closed-negative/{closure,register}.txt`
verbatim verdict 에 링크 (`a_paper_sections`). 데이터는 result.json /
verdict txt / PURE.log / H_242 에 기록된 값만.

### TODO placeholder → 실측치 치환 결과 (정직하게)

| placeholder | 처리 | 출처 |
|-------------|------|------|
| wiki 0.5 (E2) register_hits | **4/20** (실측 인용) | PURE.log L21 · H_242 §A2 |
| wiki 0.5 (E2) coherence aggregate | **0/5 PARTIAL+ (all WEAK)** (실측 인용) | PURE.log L18 `E2 FAIL(0/5)` |
| wiki 1.0 (E3) register_hits | **0/20** (실측 인용) | PURE.log L16/L21 · H_242 §A2 |
| wiki 1.0 (E3) coherence aggregate | **1/5 PARTIAL+ (ko PARTIAL, PURE_MEMORIZE→PARTIAL)** (실측 인용) | PURE.log L16 `E3 FAIL(1/5: ko만)` |
| wiki 0.5/1.0 per-lang `n_lang_coherent` 정수 | **n.c. (not captured)** 유지 — aggregate 만 기록됨, per-lang 정수 미persist | (어느 소스에도 없음 → 날조 금지) |
| motivation_8factor score | **missing** 유지 — embed 미실행 (criterion 미계측 고정 FAIL) | closure.txt |
| dream_stage Φ | **missing** 유지 — embed 미실행 (criterion 미계측 고정 FAIL) | closure.txt |

v3(wiki=0)·j02(wiki=0.3) per-lang 정수는 register.txt verbatim 으로 완전 채움
(`2/6/0/13/6` · `0/9/1/3/2`). E2/E3 는 **aggregate verdict 만** 기록에 존재하므로
표에 aggregate(0/5 · 1/5)는 채우고 per-lang 정수 칸은 `n.c.` 로 정직 표기 —
없는 값을 억지로 채우지 않음.

## 데이터 출처 (verbatim only)

- `state/pure_phase_d_v3_result_2026_05_24/result.json` (wiki_frac=0.0, sha `2643bd72a5c0e5a9`)
- `state/p21h_v3_recover_2026_05_25/out_main/result.json` (wiki_frac=0.3, sha `ab35a06e072f5d62`)
- `UNIVERSE/H_242` §A2 4-point 표 (wiki 0.5/1.0 register count 인용)
- `CLAIMS.tape` group=PURE — `pure_wiki_sweep` + `pure_register_orthogonal` (둘 다 🔴 CLOSED-negative terminal)

## 빌드

```bash
make            # → main.pdf (pdflatex × 3 + bibtex)
make clean      # .aux/.log/.bbl 제거 (PDF 보존)
make distclean  # PDF 도 제거
```

`/paper compile PAPER/pure-corpus-axis-closed-negative` 도 동일.

## Figures

- **Cover (Fig. 1, `figures/cover.png`)** — **생성 완료**. fal.ai
  `gpt-image-2` 로 `figures/_prompts/cover.txt` 프롬프트에서 생성
  (`/imagine ... -s landscape_16_9`, 654 KB PNG). main.tex 에
  `\includegraphics` + provenance 캡션(`% generated via fal.ai gpt-image-2`)
  으로 포함. 두 직교 축(register collapse 가로 · multilingual coherence
  세로) + closure bar + 5-lang glyph(ru 만 점등) 렌더 확인.
- **Fig. 2 (per-language coherence bar chart)** — main.tex 내부 **inline
  TikZ**. v3·j02 두 endpoint 의 `n_lang_coherent`(verbatim) 막대그래프 —
  wiki 0.0→0.3 에서 ru 13→3 하락 시각화.
- **Fig. 3 (orthogonality schematic)** — main.tex 내부 **inline TikZ**.
- Python figure 파이프라인 없음 (hexa-only authoring directive: 신규 .py/.sh
  금지). 모든 비-cover figure 는 inline TikZ.

## g51 충족 여부

**✅ g51 충족.** commons `g51` = **컴파일 ≥10 페이지 + fal.ai figure ≥1개**:

- 페이지: **11 페이지** (`pdfinfo main.pdf` → `Pages: 11`). 본문 확장(related
  work · 확장 method · per-language measurement · mechanistic discussion ·
  limitations · outlook)으로 채움 — placeholder 부풀리기 없이 분석/배경으로만.
- fal.ai figure: **✅ `figures/cover.png` 1개** (fal.ai gpt-image-2,
  Fig. 1, provenance 캡션 포함). g51 의 "fal.ai figure ≥1" 요건 충족.
- undefined ref/citation **0** (`make` 최종 패스 main.log verbatim).
- bibtex error **0** (references.bib header 의 at-sign 토큰 제거 후 clean).

## 정직성 (honest stance)

- 모든 수치는 result.json / verdict txt verbatim. 없는 값은 TODO.
- 4 closure criteria 중 2개(motivation_8factor · dream_stage)는 이 run 들에서
  미계측 → 고정 FAIL. 직교 결론은 criterion 1(coherence)·2(register)에만 의존
  (§Limitations L-4). aggregate "1/4 PASS" 는 계측된 2축 기준 실제 격차(1/2)를
  과대표시함 — 본문에 명시.
- closed-negative 프레이밍 (`a_paper_negative_ok`): 음성 결과를 finding 으로
  정직하게. 양성 recipe 는 주장하지 않음 — 축 하나를 배제할 뿐.
