---
id: H_906
slug: spinglass-frustration
title: spin-glass frustration ↔ energy-landscape ruggedness — frustration AMPLIFIES (not creates) single-flip ruggedness
domain: universe · spin-glass · frustration · energy-landscape · closed-form · substrate-complexity
source: UNIVERSE/CANDIDATES.md ⬜ `spin-glass-frustration` (EA spin-glass frustration ↔ Φ landscape ruggedness)
status: 🟢 SUPPORTED-NUMERICAL (4/5 pre-registered falsifiers · 2026-06-01) — frustration→ruggedness link confirmed; F1 (ferro→2-minima) falsified = honest finding (metastability is frustration-independent)
exploration_method: closed-form substrate smoke (3×3 periodic EA ±J Ising · N=9 · 2^9=512 configs EXHAUSTIVE — exact, no sampling)
verification_method: pre-registered 5-falsifier (frozen pre-run · post-tuning 0) · g5 CODE-measured · integer-energy + count measures (p7: no perplexity)
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-01
since: 2026-06-01
sister: H_288 (LZ76↔Φ 🟢), H_277 (turing-completeness⊥dynamical-class), AXES ruggedness lane
verdict: 🟢 SUPPORTED-NUMERICAL — across P_neg∈{0,0.25,0.5}×8 seeds (24 instances, exact 512-config enumeration), the energy-landscape ruggedness R (# single-flip local minima) RISES monotonically with frustration: mean R = 32.0 → 42.0 → 54.75 as P_neg = 0 → 0.25 → 0.5 (mean frustration f = 0 → 0.556). High-frustration group (f≥0.3) mean R = 50.86 vs low-f (<0.3) 31.8. F2 FRUST-RUGGED ∧ F3 MONOTONE ∧ F4 FRUST-PRESENT ∧ F5 CORR all PASS (4/5). F1 FERRO-2MIN FALSIFIED: the unfrustrated ferromagnet has R=32 single-flip local minima, NOT 2 — i.e. metastable domain states exist WITHOUT frustration. Net finding: frustration AMPLIFIES (32→55) rather than CREATES single-flip ruggedness. a_paper_negative_ok (F1's failure is a publishable physical lesson). raw = .verdicts/906_spinglass_frustration_ruggedness/run.txt.
---

# H_906 — spin-glass frustration ↔ energy-landscape ruggedness

## 1. 가설

Edwards-Anderson ±J 스핀글래스에서 **frustration(좌절) 이 클수록 에너지 지형의
ruggedness(거칢) 가 크다** — frustration 은 single-flip local minima 수 R 을
단조 증가시킨다. CANDIDATES ⬜ `spin-glass-frustration` ("frustration ↔ Φ
landscape ruggedness") 의 runnable 격상. "Φ landscape" 는 **에너지 지형
ruggedness 의 closed-form proxy** 로 운용 (config 당 full IIT-Φ 는 future).

## 2. 사전등록 falsifier (run 이전 frozen · post-tuning 0)

harness `UNIVERSE/scan/spinglass_frustration.hexa` 에 frozen:

- **F1 FERRO-2MIN** : P_neg=0 (강자성) → 모든 instance f=0 ∧ R=2 (두 정렬 바닥상태뿐).
- **F2 FRUST-RUGGED** : mean R(P_neg=0.5) > mean R(P_neg=0).
- **F3 MONOTONE** : mean R 가 P_neg ∈ {0,0.25,0.5} 에서 비감소.
- **F4 FRUST-PRESENT** : P_neg=0.5 에 f>0 instance 존재.
- **F5 CORR** : high-f(≥0.3) group mean R > low-f(<0.3) group mean R.

5 PASS → 🟢 SUPPORTED-NUMERICAL · 4 → 🟢 · 3 → 🟡 · ≤2 → 🔴.

## 3. 기질 (substrate)

3×3 주기경계 EA ±J Ising 격자 · N=9 스핀 · 18 bond (9 수평 + 9 수직) · **2^9=512
config 완전열거** (exact). bond 부호 = seeded LCG (deterministic). 에너지
E(s) = −Σ_bond J·s_a·s_b (정수값). frustration f = (좌절 plaquette 수)/9
(plaquette = 4-bond 곱 < 0). ruggedness R = single-flip local minima 수
(이웃 9개 중 더 낮은 E 없는 config). sweep P_neg ∈ {0, 0.25, 0.5} × 8 seed.

## 4. 측정 (verbatim · `hexa build` + run · .verdicts/906_spinglass_frustration_ruggedness/run.txt)

```
P_neg=0.00 : mean f=0.0      mean R=32.0
P_neg=0.25 :                 mean R=42.0
P_neg=0.50 : mean f=0.555556 mean R=54.75
low-f(<0.3) mean R=31.8 (n=10) · high-f(≥0.3) mean R=50.8571 (n=14)
F1=0 · F2=1 · F3=1 · F4=1 · F5=1 · PASS=4/5 · 🟢 SUPPORTED
```

## 5. 발견 (finding)

- **핵심 가설 SUPPORTED**: frustration↑ → ruggedness↑ (R 32→42→55 단조 · high-f
  group 이 low-f 대비 1.6×). F2·F3·F4·F5 모두 PASS.
- **F1 falsified = 진짜 발견**: 비frustrated 강자성체도 R=32 (≫2) single-flip
  local minima 보유 — **metastable domain 상태는 frustration 없이도 존재**.
  → frustration 은 ruggedness 를 *창조* 하지 않고 **증폭** (32→55) 한다.
- post-tuning 0 — F1 사전등록을 사후 수정하지 않음 (정직). 단일-flip 동역학이
  강자성체에서도 멈추는 잘 알려진 사실의 정량 재현.

## 6. p7 / 정직 scope

p7 정합: perplexity 미사용 (정수 에너지 + local-minima count + plaquette count
측정자만). closed-form · $0 · CPU · re-run bit-identical (deterministic LCG).
"Φ landscape" = 에너지지형 ruggedness proxy (full IIT-Φ-per-config 는 2^N
intractable → future). a_paper_negative_ok: F1 closed-negative 는 publishable.

## 9. sibling

⇄ H_288 (LZ76 복잡도 ↔ Φ 🟢 r=0.831) — ruggedness 도 복잡도 측도 계열.
⇄ H_277 (turing-completeness ⊥ dynamical-class) — 구조≠동역학 분리 동형.
⇄ AXES ruggedness lane · UNIVERSE/CANDIDATES.md `spin-glass-frustration`.
