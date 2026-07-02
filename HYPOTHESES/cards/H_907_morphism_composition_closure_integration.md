---
id: H_907
slug: category-emergence
title: morphism composition-closure ↔ integration — closure predicts integration beyond density, but random graphs do NOT self-form closed categories
domain: universe · category-theory · composition-closure · integration · closed-form · emergence
source: UNIVERSE/CANDIDATES.md ⬜ `category-theory-emergence` (morphism composition density vs Φ — Yoneda substrate)
status: 🟢 SUPPORTED-NUMERICAL (4/5 pre-registered falsifiers · 2026-06-01) — F3 (density-controlled closure↔integration) PASS = the real claim; F4 (random→closed-category) falsified = closed categories need structure, not random density
exploration_method: closed-form substrate smoke (N=6 directed graph · 30 morphisms · exact enumeration + transitive-closure BFS · no sampling)
verification_method: pre-registered 5-falsifier (frozen pre-run · post-tuning 0) · g5 CODE-measured · count/fraction measures (p7: no perplexity)
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-01
since: 2026-06-01
sister: H_906 (spin-glass frustration↔ruggedness 🟢), H_288 (LZ76↔Φ 🟢), H_275 (causality-pearl-graph-Φ)
verdict: 🟢 SUPPORTED-NUMERICAL — across p∈{0.2,0.4,0.6}×8 seeds (24 N=6 directed graphs, exact composition-closure + transitive-reachability), composition closure D and integration Φ both rise with edge density (D 0.236→0.322→0.576 · Φ 0.388→…→1.0). The NON-TRIVIAL F3 (density-controlled, p fixed at 0.4): high-closure half mean Φ=0.958 > low-closure half 0.775 → closure predicts integration BEYOND raw edge count (PASS). F1/F2/F5 PASS. F4 CATEGORY-FORM FALSIFIED: even p=0.6 gives mean D=0.576 (<0.85) — random morphism graphs do NOT self-organize into composition-closed (genuine) categories at these densities; closure needs designed structure, not density alone. a_paper_negative_ok (F4 closed-negative). raw = .verdicts/907_morphism_composition_closure_integration/run.txt.
---

# H_907 — morphism composition-closure ↔ integration

## 1. 가설

작은 카테고리 기질에서 **morphism composition closure(합성 닫힘) 가 클수록
integration(통합) 이 크다** — 그리고 그 관계는 raw edge density 너머로 성립한다.
CANDIDATES ⬜ `category-theory-emergence` (composition density vs Φ · Yoneda) 의
runnable 격상. "Φ" 는 **transitive-reachability density(통합 proxy)** 로 운용.

## 2. 사전등록 falsifier (run 이전 frozen · post-tuning 0)

harness `UNIVERSE/scan/category_emergence.hexa`:

- **F1 CLOSURE-RISES** : mean D(p=0.6) > mean D(p=0.2). (control · trivial-ok)
- **F2 INTEG-RISES** : mean Φ(p=0.6) > mean Φ(p=0.2). (control)
- **F3 CONTROLLED** : p 고정(0.4)에서 high-D-half mean Φ > low-D-half mean Φ
  (closure↔integration 가 density 너머로 — **핵심 비자명 주장**).
- **F4 CATEGORY-FORM** : ∃ p 에서 mean D ≥ 0.85 (near-closed = emergent category).
- **F5 SPARSE-OPEN** : mean D(p=0.2) < 0.6 (sparse = 닫힌 category 와 거리).

5 PASS → 🟢 SUPPORTED-NUMERICAL · 4 → 🟢 · 3 → 🟡 · ≤2 → 🔴.

## 3. 기질 (substrate)

N=6 object 방향그래프 · 30 가능 morphism (self-loop 제외 · identity 암묵) ·
edge = seeded LCG (deterministic). D = composition closure = present(A→C) /
composable(A→B ∧ B→C, A≠B≠C) — exact enum. Φ = reachability density =
#{(A,B),A≠B: A⇝B 경로} / 30 — transitive closure (Floyd boolean). sweep
p ∈ {0.2,0.4,0.6} × 8 seed.

## 4. 측정 (verbatim · .verdicts/907_morphism_composition_closure_integration/run.txt)

```
p=0.2 : mean D=0.236174 mean Φ=0.3875
p=0.4 : mean D=0.321602 (F3 split @ medD=0.321602)
p=0.6 : mean D=0.576475 mean Φ=1.0
F3 controlled (p=0.4): high-D Φ=0.958333 (n=4) vs low-D Φ=0.775 (n=4)
F1=1 · F2=1 · F3=1 · F4=0 · F5=1 · PASS=4/5 · 🟢 SUPPORTED
```

## 5. 발견 (finding)

- **핵심(F3) SUPPORTED**: density 고정(p=0.4)에서도 high-closure 그래프가 더
  integrated (Φ 0.958 vs 0.775) → composition closure 는 raw edge count 가
  설명 못 하는 integration 신호를 담는다 (비자명 · 단순 밀도효과 아님).
- **F4 falsified = 진짜 발견**: p=0.6 에서도 mean D=0.576 (<0.85) — **무작위
  morphism 그래프는 합성-닫힌(진짜) category 로 자발 조직되지 않는다**. 닫힘은
  density 만으로 안 되고 designed structure 필요 (Yoneda-emergence 는 무작위
  substrate 위에선 안 일어남).
- post-tuning 0. F1/F2/F5 = density control PASS (sanity).

## 6. p7 / 정직 scope

p7 정합: perplexity 미사용 (count/fraction 측정자만). closed-form · $0 · CPU ·
re-run bit-identical (deterministic LCG). "Φ" = reachability-integration proxy
(full IIT-Φ 는 future). a_paper_negative_ok: F4 closed-negative publishable.

## 9. sibling

⇄ H_906 (spin-glass frustration↔ruggedness 🟢) — 동일 closed-form substrate-smoke 형식.
⇄ H_288 (LZ76↔Φ 🟢) · H_275 (causality-pearl-graph-Φ) — graph/complexity↔Φ 계열.
⇄ UNIVERSE/CANDIDATES.md `category-theory-emergence`.
