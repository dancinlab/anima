# savant-iit4-bridge — paper log

Append-only history sister of `PAPER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-28 — limitations 보강: H_626 negative 반영 (isomorphism 차원-조건부성)

- [x] §Limitations 항목 강화 — 기존 "Dimension match is exact only at n=4" generic forward 를 H_626 (PR #1210, 🔴 FALSIFIED) 실측으로 교체: n=5 일반화 ρ=0.199 (Δρ=−0.66 vs H_624), Pearson r=0.028, argmax 1/4, F1–F4 모두 FAIL (byte-eq 만 통과). root cause = 5번째 auxiliary balanced distinction (φ_d=0.312) 의 rank-2 침투로 top-4 truncation pairing 붕괴
- [x] isomorphism claim 을 *cardinality-matched single-substrate (n=domain-count=4)* 한정으로 명시 · 차원-무관 일반 동형 = closed-negative
- [x] Abstract caveat 1줄 (core claim 약화) + Conclusion caveat 1줄 + Discussion "partial isomorphism, not identity" 단락에 cardinality-conditional 확정
- [x] references.bib `anima_H626` ledger entry (PR #1210) 추가 + §Limitations inline cite
- [x] PAPER.md milestone 추가
- [x] recompile (xelatex × 3 + bibtex) — 0 undefined refs

## 2026-05-28 — draft v1 scaffold (SAVANT axis E × IIT4 axis C isomorphism arc)

- [x] PAPER.tape roster row `@paper savant-iit4-bridge := "./PAPER/savant-iit4-bridge"`
- [x] PAPER.md snapshot (@title · @goal · milestones) + PAPER.log.md
- [x] main.tex — 7 content sections (GZ×SI framework · IIT4 Φ-structure recap · closed-form anchors · statistical bridge · structural isomorphism · collective extension · discussion) + abstract + intro + method + limitations + reproducibility + conclusion
- [x] references.bib — IIT/SAVANT literature + 7 anima H ledger entries
- [x] companion/{pr-roll,verify-ledger,session-journal}.json|md
- [x] figures/_scripts — native pgfplots dΦ/dI peak alignment (fig01) + isomorphism scatter (fig02)
- [ ] compile clean (xelatex × 3 + bibtex)
- [ ] arxiv-prep
