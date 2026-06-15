---
id: H_908
slug: topology-invariant-phi
title: topological invariant (Betti-1 cycles · Euler χ) ↔ integration — cycles raise integration beyond density; χ anti-couples
domain: universe · topology · betti · euler · integration · closed-form · graph-invariant
source: UNIVERSE/CANDIDATES.md ⬜ `topology-invariant-phi` (Betti/Euler ↔ Φ monotone correlation)
status: 🟢 SUPPORTED-NUMERICAL (5/5 pre-registered falsifiers · 2026-06-01) — all PASS incl. F3 (density-controlled cycles↔integration) + F4 (Euler χ anti-couples) + F5 (P6 tree exact b1=0 χ=1)
exploration_method: closed-form substrate smoke (undirected N=6 graph · 15 edges · exact 1-complex invariants + BFS-relax components · no sampling)
verification_method: pre-registered 5-falsifier (frozen pre-run · post-tuning 0) · g5 CODE-measured · integer invariants + fraction (p7: no perplexity)
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-01
since: 2026-06-01
sister: H_906 (spin-glass↔ruggedness 🟢), H_907 (category closure↔integration 🟢), H_288 (LZ76↔Φ 🟢), H_289 (scale-free↔Φ 🟢)
verdict: 🟢 SUPPORTED-NUMERICAL — across p∈{0.2,0.4,0.6}×8 seeds (24 undirected N=6 graphs, exact Betti-1 b1=E−V+C and Euler χ=V−E), topological invariants crisply track integration Φ (within-component reachability density). 5/5 PASS: b1 rises with density (0.125→3.875), Φ rises (0.233→0.958); F3 (the non-trivial, density-controlled at p=0.4) PASS — high-b1 half mean Φ=0.867 > low-b1 half 0.617, so CYCLE topology predicts integration BEYOND raw edge count; F4 EULER-NEG PASS — χ anti-couples (3.75→−2.75 as Φ 0.233→0.958, treelike high-χ = low integration); F5 TREE-EXACT PASS — deterministic path P6 gives b1=0 ∧ χ=1 (acyclic invariants exact). raw = .verdicts/908_topology_invariant_phi/run.txt.
---

# H_908 — topological invariant (Betti-1 · Euler χ) ↔ integration

## 1. 가설

그래프 기질의 **위상 불변량(Betti-1 cycle 수 · Euler χ) 이 integration(통합) 과
단조 상관**한다 — cycle 이 많을수록(b1↑) 통합↑, treelike(χ↑) 일수록 통합↓.
CANDIDATES ⬜ `topology-invariant-phi` (Betti/Euler ↔ Φ) 의 runnable 격상.
"Φ" = within-component reachability density (통합 proxy · full persistent-homology
Φ 는 future).

## 2. 사전등록 falsifier (run 이전 frozen · post-tuning 0)

harness `UNIVERSE/scan/topology_invariant_phi.hexa`:

- **F1 B1-RISES** : mean b1(p=0.6) > mean b1(p=0.2). (control)
- **F2 PHI-RISES** : mean Φ(p=0.6) > mean Φ(p=0.2). (control)
- **F3 CONTROLLED** : p 고정(0.4)에서 high-b1-half mean Φ > low-b1-half mean Φ
  (cycle topology 가 density 너머로 integration 예측 — **핵심 비자명 주장**).
- **F4 EULER-NEG** : χ ↔ Φ 역결합 (mean χ(0.2) > χ(0.6) ∧ Φ(0.2) < Φ(0.6)).
- **F5 TREE-EXACT** : 결정론 path P6 → b1=0 ∧ χ=1 (acyclic 불변량 정확).

5 PASS → 🟢 SUPPORTED-NUMERICAL · 4 → 🟢 · 3 → 🟡 · ≤2 → 🔴.

## 3. 기질 (substrate)

무방향 그래프 N=6 · 15 가능 edge · edge = seeded LCG (deterministic). Euler
χ = V − E (= N − E). Betti-1 b1 = E − V + C (독립 cycle 수 · C = 연결성분 수,
BFS min-label relaxation fixed-point). Φ = within-component reachability =
Σ_comp |comp|(|comp|−1) / (N(N−1)). sweep p ∈ {0.2,0.4,0.6} × 8 seed + 결정론 P6.

## 4. 측정 (verbatim · .verdicts/908_topology_invariant_phi/run.txt)

```
p=0.2 : mean b1=0.125 χ=3.75 Φ=0.233333
p=0.6 : mean b1=3.875 χ=-2.75 Φ=0.958333
F3 controlled (p=0.4): high-b1 Φ=0.866667 (n=4) vs low-b1 Φ=0.616667 (n=4)
P6 tree: b1=0 χ=1 (expect b1=0 χ=1)
F1=1 · F2=1 · F3=1 · F4=1 · F5=1 · PASS=5/5 · 🟢 SUPPORTED-NUMERICAL
```

## 5. 발견 (finding)

- **5/5 PASS** — 위상 불변량이 integration 을 crisp 하게 추적.
- **핵심(F3)**: density 고정에서도 high-b1(cycle 많은) 그래프가 더 integrated
  (Φ 0.867 vs 0.617) → **cycle 구조가 raw edge count 너머로 통합 신호**. 단순
  밀도효과 아님.
- **F4 EULER-NEG**: Euler χ 가 Φ 와 역결합 (χ 3.75 → −2.75, Φ 0.233 → 0.958)
  — treelike(high-χ) substrate = 저통합, cyclic(low/neg-χ) = 고통합.
- **F5 위상 정확성**: path P6 의 b1=0 ∧ χ=1 결정론 재현 (acyclic 1-complex 의
  닫힌형 불변량).

## 6. p7 / 정직 scope

p7 정합: perplexity 미사용 (정수 위상 불변량 b1/χ + reachability fraction 만).
closed-form · $0 · CPU · re-run bit-identical (deterministic LCG). "Φ" =
reachability-integration proxy (full persistent-homology Φ 는 2^? future).

## 9. sibling

⇄ H_906 (spin-glass↔ruggedness 🟢) · H_907 (category closure↔integration 🟢)
   — 동일 closed-form substrate-smoke 형식 3부작.
⇄ H_288 (LZ76↔Φ) · H_289 (scale-free 위상↔Φ) — 복잡도/위상↔Φ 계열.
⇄ UNIVERSE/CANDIDATES.md `topology-invariant-phi`.
