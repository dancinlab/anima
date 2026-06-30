# h345-class-iv-scope — basin↔Φ coupling 의 scope 정정 (negative-result paper)

> UNIVERSE H_345/346 capstone 의 "state-강건 basin↔Φ 결합 (+0.55 / −0.95)"
> finding 의 scope 를 측정으로 정정. anima-side BENCH #1
> (8-rule, PR [#1122](https://github.com/dancinlab/anima/pull/1122)) 와
> BENCH #1-broader (16-rule × 4 Wolfram class, PR
> [#1131](https://github.com/dancinlab/anima/pull/1131)) 가 다음을 측정으로 확정:
>
> - `max_basin↔Φ` 의 + sign 은 H_346 의 curated 4-rule {110, 30, 105, 150}
>   에서만 성립 — 광역 16-rule 에서 overall r = **−0.896** (sign reversed).
> - `n_attr↔Φ` 의 magnitude (|r| > 0.6) 는 Wolfram-class 별 robust, 다만
>   **sign 은 class-determined**: I/II/III positive, **IV 단독 negative**.
> - H_346 의 `−0.951` 은 **class IV anchor (rule 110) 의 sign 을 반영** —
>   class-IV-specific, state-robust 아님.
>
> 본 논문은 a_paper_negative_ok 등급 — finding 의 존재를 부정하는 것이 아니라
> scope 를 좁히는 정정 (self-correction³).

## 한 줄 요지

H_346 의 `+0.550 / −0.951` capstone 은 Wolfram-canonical 4-rule frame
{110, 30, 105, 150} = 1 IV + 3 III mix 의 **우연한 정렬**에서 비롯됐고,
class-systematic broadening 시 `max_basin↔Φ` 부호 역전, `n_attr↔Φ`
sign 도 class IV 외에서는 reverse. robust signal 은 `|n_attr↔Φ|` 의
magnitude 뿐 (sign 은 class-IV-anchored).

## § 구조 (`a_paper_format`)

| 섹션 | 내용 | verdict 링크 (`a_paper_sections`) |
|------|------|-----------------------------------|
| §1 Introduction (sec:intro) | H_345/346 self-correction arc 와 original "state-robust" claim | H_345/346 본문 |
| §2 Method (sec:method) | bench #1 (4→8 rule) + broader (16 rule × 4 Wolfram class) substrate · phi 엔진 · rule-set pre-registration · verdict tier | `bench/basin_phi_broader/bench.hexa` |
| §3 Measurement (sec:measurement) | raw 16-rule 표 + per-class Pearson r 매트릭스 verbatim from PR #1131 result.json + realized verdict | `bench/basin_phi_broader/result.json` |
| §4 Finding (sec:finding) | F1 class-IV-specific · F2 magnitude robust + sign class-determined · F3 max_basin↔Φ curation-fragile · F4 H_346 +0.55 = accidental alignment + revised scope statement | `bench/basin_phi_broader/result.json::pearson` + PR #1129 (H_345/346 §11) |
| §5 Verdict Matrix (sec:verdict) | 모든 섹션 claim → verdict source pointer 표 | per-claim verbatim |
| §6 Honest caveats (sec:caveats) | result.json::honest_caveats 6 entries verbatim | `bench/basin_phi_broader/result.json::honest_caveats` |
| §7 Reproducibility (sec:repro) | substrate + engine + wall/cost + pre-registration + class atlas refs | `bench/basin_phi_broader/bench.hexa` + Wolfram (2002) |
| §8 Conclusion (sec:conclusion) | scope 정정 — `a_paper_negative_ok` tier · self-correction³ | PR #1129 |

§3 Measurement + §4 Finding + §5 Verdict Matrix + §6 Honest caveats + §7
Reproducibility + §8 Conclusion 은 scaffold 완료 (수치 frozen from
PR #1131 result.json verbatim). §1/§2 는 사람 작성 — 본 scaffold 의 TODO
블록을 그대로 두고 후속 PR 에서 sync.

## Verdict tier

- `a_paper_gate`: terminal 조건 OK — bench result 가 🔴 FAIL-REVERSED
  + diagnostic refinement (terminal closed-negative).
- `a_paper_significance`:
  - falsifiable hypothesis 사전등록 ✓ (verdict tier rule in source
    pre-measurement)
  - real measurement ✓ (256 `phi_structure` calls, 57s wall, Mac
    local, $0)
  - finding ✓ (Δ vs baseline = H_346 capstone + sign reversal + class
    sign switch + curation-fragility diagnostic)
- `a_paper_negative_ok`: closed-negative ruling (max_basin↔Φ broader
  robust ruled out) → 본 논문 framing 정당.

## Files

- `PAPER.md` — paper snapshot (status · milestones)
- `PAPER.log.md` — append-only history sister
- `main.tex` — arxiv-style LaTeX, 4-section spine (Intro · Method ·
  Measurement · Finding) + Verdict Matrix + Honest caveats + Repro +
  Conclusion. Numerical content frozen verbatim from PR #1131
  result.json.
- `references.bib` — 7 anima internal + 3 IIT foundational + 4 CA
  classification + 3 methodology = 17 entries (≥10 bar cleared).
- `Makefile` — pdflatex 3-pass + bibtex
- `figures/` — cover figure (TODO: fal.ai gpt-image-2 generation
  pending)

## Build

```bash
cd PAPER/h345-class-iv-scope
make            # → main.pdf (pdflatex × 3 + bibtex)
make clean      # remove intermediates (PDF preserved)
make distclean  # remove PDF + intermediates
```

## TODO (post-scaffold pass — human authoring + final touches)

- [ ] §1 Introduction: H_345/346 arc 본문 (self-correction arc 그림 +
  capstone 인용 + open question 명시) — placeholder TODO 블록을
  scaffold 에 그대로 둠
- [ ] §2 Method: bench #1 + broader method 상세 (사람 sync) —
  placeholder TODO 블록을 scaffold 에 그대로 둠
- [ ] cover figure (fal.ai gpt-image-2) — `figures/_prompts/cover.txt`
  prompt + `figures/cover.png` 생성
- [ ] `make` clean compile (pdflatex + bibtex)
- [ ] `make wordcount` + `make pages` ≥10p (commons g51)
- [ ] arxiv submit prep (`/paper arxiv-prep .`)

## Cross-link

- UNIVERSE H_341 — n=4, 4 rules, +0.776 (arc start)
- UNIVERSE H_343 — n=6 cycle-length proxy, sign reversal (proxy doubt)
- UNIVERSE H_345 — n=5 exact single-state, +0.251/−0.799 (proxy
  artifact resolved)
- UNIVERSE H_346 — n=5 state-averaged, +0.550/−0.951 🟢 capstone
  (scope corrected here)
- BENCH #1 (PR #1122) — n=4 state-avg, 8 mixed rules, −0.314/+0.122
  🟠 WEAK-REVERSED
- BENCH #1-broader (PR #1131) — n=4 state-avg, 16 rules × 4 classes,
  overall −0.896/+0.641 🔴-REVERSED (primary evidence base)
- PR #1129 — H_345/346 §11 scope-correction docs (companion to this
  paper)

## Honest stance

This paper is scope-narrowing, not result-overturning. The H_346
capstone's per-state-averaging closure remains valid within its
declared 4-rule frame; what is ruled out is the implicit ``rule-set
robust'' inference. The robust cross-class signal is the magnitude of
`n_attr↔Φ` (|r| > 0.6 in 3/4 classes), not its sign.
