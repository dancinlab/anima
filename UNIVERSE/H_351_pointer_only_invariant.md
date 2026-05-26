# H_351 — pointer-only invariant 🔵

영속성 7th — a_kosmos: anima 안에 kosmos spec duplicate 없음 (pointer only) — H_339 H3 의 commit-level invariant 강화.

## 가설
H1 ZERO-DUPLICATE: count(spec_body_duplicate(anima, kosmos)) ≡ 0
H2 URL-POINTER-ONLY: anima 의 kosmos reference 는 `github.com/dancinlab/kosmos` URL pointer 만 (spec body 미인라인)
H3 INVARIANT-UNDER-COMMIT: ∀ commit c on anima main, count(c) ≡ 0 (monotone-zero)
H4 DETERMINISTIC
H5 BOUND
