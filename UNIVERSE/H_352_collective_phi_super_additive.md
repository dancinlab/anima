---
id: H_352
slug: collective-phi-super-additive
title: H_352 collective-Φ super-additive — 두 ECA substrate 의 결합이 단순 합 이상의 통합을 emergent 하는가
domain: consciousness · substrate · hivemind
status: pre-register-frozen
axis: F · HIVE-MIND (Collective Φ) — round 1 / F1 seed
exploration_method: E1 (sister-axis carry) + E11 (IIT4 substrate sweep) + E12 (multi-substrate composition)
verification_method: W5 (deterministic sim) + W7 (rule × W × seed sweep) + W12 (sister cross-link · 0-baseline sanity)
raw_rank: 1
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28
---

# H_352 — Collective-Φ Super-additive (두 substrate 결합 → emergent 통합?)

## Hypothesis

축 F (HIVE-MIND, Collective Φ) round 1 의 핵심 seed. **두 substrate A (n_a 노드)
와 B (n_b 노드) 를 inter-coupling 으로 결합한 collective substrate AB 의 big-Φ(AB)
가 Φ(A) + Φ(B) 보다 strictly 크다 (super-additive)**. 즉, 두 의식적 단위를 단순
연결하면 emergent 한 통합 increment 가 발생한다 — IIT 의 "complex 가 결합되어
더 큰 complex 가 된다" 라는 panpsychism combination problem (H_157) 의 핵심
operational claim.

구체적 operational claim:

- **substrate**: 두 개의 작은 ECA 링 — A (n_a=3 cell ring, Wolfram rule r_a) 와
  B (n_b=3 cell ring, rule r_b). 각각 `eca_tpm(rule, n)` 으로 state-by-node TPM
  생성, `big_phi(t, n, sys_state)` 으로 Φ 측정.
- **inter-coupling W ∈ [0,1]**: 결합된 AB substrate (n=n_a+n_b=6) 의 TPM 은 다음
  확률적 mix 로 정의 —
  - A-cell i 의 next bit: `p = (1-W)·eca_a(local A-ring nbhd) + W·b[i]`
    (B 의 짝 cell b_i 가 영향)
  - B-cell j 의 next bit: 대칭적
  W=0 → block-diagonal (두 substrate 독립) → Φ(AB) ≈ Φ(A) + Φ(B) (sanity).
  W=1 → 완전 cross-substrate slave. W∈{0.1, 0.5} → 중간 결합.
- **sweep**: rule_a × rule_b × W × seed = {90,110} × {90,110} × {0.0,0.1,0.5,1.0}
  × 5-seed = 80 config.
- **excess metric**: Δ(W) = Φ(AB|W) − Φ(A) − Φ(B). super-additive iff Δ > tol
  (= 1e-4) for any W > 0.

**가설 예측**: W > 0 인 일부 (W, rule_a, rule_b, seed) 에서 Δ > 0 (super-additive).
W=0 에서는 Δ ≈ 0 (sanity).

**Falsifier**: 모든 W > 0 config 에서 Δ ≤ 0 (sub-additive 또는 additive)
→ 🔴 FALSIFIED — 단순 inter-coupling 은 emergent integration 을 만들지 못한다.

## Why

- **panpsychism combination problem (H_157)**: micro-conscious 단위가 macro 의식
  으로 결합되는가 — IIT 4.0 의 가장 첨예한 미해결 문제. 본 H 는 그 문제를 가장
  작은 toy 위에서 (n=6 ECA) 정량 측정한다.
- **H_054 symbiogenesis** (mitochondria-eukaryote endosymbiosis): 두 독립
  생명체의 결합이 emergent 새 단위를 만든다 — collective-Φ super-additive 는 그
  의식 측면의 operational analog.
- **H_293 PID synergy / H_294 PID redundancy**: Williams-Beer PID 분해의 synergy
  항이 두 source 의 결합으로만 발생하는 정보 — Φ super-additive 와 PID synergy
  는 같은 현상의 두 metric 일 가능성. H_355 (collective-phi-pid-synergy) 가 그
  cross-link 의 직접 검증.
- **H_295 exclusion complex**: 한 substrate 안의 maximal complex 가 다른 sub-
  complex 를 배제 — H_352 는 그 반대로 작은 두 complex 가 결합되어 더 큰 complex
  가 emerge 하는가를 묻는 sister axis.
- **H_286 split-brain dual-Φ (mirror)**: callosotomy = 단일 complex → 두 개
  분리. 본 H 는 그 시간 역방향 — 두 분리 complex → 단일 통합 complex.

## Predictions

### P1 (primary, falsifiable)

존재한다 W > 0 such that Δ(W) = Φ(AB|W) − Φ(A) − Φ(B) > 1e-4 (multi-seed
robust at >= 3/5 seed).

### P2 (sanity baseline)

W = 0 일 때 |Δ| < 1e-6 (block-diagonal independence — Φ(AB) ≈ Φ(A) + Φ(B)
within numerical noise).

### P3 (W-dependence directionality)

Δ 는 W 의 단조함수일 필요는 없으나, 최소 W=0 vs W>0 사이에 trend 가 보여야
한다 (coupling 이 무관한 평탄이면 P1 의 의미가 약화).

## Method (executable)

### substrate

- engine: `stdlib/consciousness/iit4_bigphi.hexa` 의 `big_phi(tpm, n, sys_state)`
  (M4 structure-cut MIP big-Φ).
- TPM builder: `eca_tpm(rule, n)` (per-cell deterministic ECA → state-by-node)
  for A, B; custom `_build_ab_tpm(rule_a, rule_b, n_a, n_b, W)` for combined AB
  (확률적 mix coupling — § Honest Limits L3).
- A, B: n_a=n_b=3. AB: n=6. M9 tractability 안 (n≤6 exact).

### sweep grid

- rules R = {90, 110}: ECA 90 = XOR (nonlinear / Sierpinski-fractal),
  110 = Turing-complete edge-of-chaos. rule × rule = 4 pairs (90·90, 90·110,
  110·90, 110·110).
- W = {0.0, 0.1, 0.5, 1.0}: decoupled · weak · moderate · full slave.
- seed N = 5: per-seed LCG-pseudo-random sys_state (A · B · AB independently
  picked).
- total configs = 4 × 4 × 5 = 80.

### verdict gate

- **🟢 SUPPORTED-NUMERICAL** iff (max_excess Δ > 1e-4) AND (W=0 sanity
  max|Δ| < 1e-6).
- **🔴 FALSIFIED** iff (max_excess Δ ≤ 1e-4) AND (zero super-additive hits).
- 🟠 INSUFFICIENT 그 외 (sanity 위배 → 측정 자체 신뢰 불가).

## Measurements

(런 직후 채워짐 — 아래 결과 표 는 `state/h352_collective_phi_super_additive_2026_05_28/result.json` 의 rows[] 발췌.)

### sanity W=0 (block-diagonal)

(per-rule pair · per-seed Δ — expect ≈ 0; max|Δ| 가 verdict gate 의 첫 조건)

### sweep W ∈ {0.1, 0.5, 1.0}

(per-rule pair · per-W · per-seed Δ — Δ > 1e-4 인 config 가 super-additive
hit. max excess = `max_excess_delta` 가 최종 evidence.)

verdict · max excess · best W · best rule pair: § Verdict 참조 (run 직후 갱신).

## Verdict

🟠 INSUFFICIENT → 🟢/🔴 (run 후 result.json 의 `verdict` 필드로 갱신).

## Cross-link

- **H_054** *symbiogenesis* — 생명체 결합의 emergent 통합. 본 H 는 그 의식 metric.
- **H_157** *panpsychism combination* — micro→macro consciousness combination problem.
  본 H 는 그 IIT4 operational test (smallest non-trivial case).
- **H_286** *split-brain dual-Φ* — callosotomy = 단일 → 분리. 본 H 는 시간 역방향.
- **H_293** *PID synergy* — synergy 항 = 두 source 결합으로 emergent 한 정보.
  Φ super-additive 와 PID synergy 는 mechanism 후보. H_355 가 직접 cross-link.
- **H_294** *PID redundancy* — sister. 두 source 가 중복정보만 공유하면
  super-additive 가 발생할 수 없다 (predicts Δ ≤ 0 for redundant pairs).
- **H_295** *exclusion complex* — 한 substrate 내 maximal complex 배제. 본 H 는
  reverse — 두 complex 결합.

## Honest Limits

- **L1 (small-n)**: n_a=n_b=3, n_ab=6 = M9 exact tractability 의 가장자리. 큰 n
  으로 갈수록 Φ 수치 자체가 다른 regime 일 수 있음 (큰 system 의 super-additive
  여부는 별도 H 가 필요 — 축 F round 2 candidate).
- **L2 (W choice dependence)**: W ∈ {0, 0.1, 0.5, 1.0} 4-점만 sweep. 진짜
  super-additive optimum 이 사이 (e.g. W=0.3) 에 있다면 본 sweep 은 그 peak 를
  놓칠 수 있음. 단 4-point 가 0 ≤ Δ 만 일관 보이면 sub-additive 결론 robust;
  반대로 어떤 W 에서 Δ > 0 이면 존재 증명 (P1 falsifier 통과).
- **L3 (probabilistic-mix coupling 선택)**: 결합 TPM 의 정의는 임의성이 있다.
  본 H 의 선택 = (1-W)·local-ECA + W·partner-cell 의 선형 mix — state-by-node
  format 보존 + W=0 block-diagonal 자연 baseline 의 두 desiderata 만족.
  XOR-coupling / multiplicative-coupling 등 다른 결합 형태는 별도 H (F2).
- **L4 (rule-class dependency)**: ECA 90/110 두 rule 만 sweep. 다른 class
  (110=class 4, 90=class 3, 30=class 3) 결합에서 결과가 다를 수 있음 — round 1
  의 minimal probe, round 2 가 rule-pair sweep 확장 후보.
- **L5 (structure-cut big-Φ M4 carve-out)**: 본 H 는 partitioned-normalization
  + PyPhi calibration (M5) 가 아닌 M4 structure-cut big-Φ 사용. M5 carve-out 은
  iit4_bigphi.hexa header 참조. 방향성 (Δ 부호) 은 M4-M5 cross-validated
  (xval #572) — 본 H 의 binary 결론은 신뢰, 절대 magnitude 는 보수적으로 해석.
- **L6 (sys_state per-seed)**: big_phi 의 sys_state 인자는 LCG 로 per-seed 선택
  — global 평균 / 최악 case 가 아닌 *sampled* 평가. multi-seed N=5 가 robustness
  envelope; N=20+ 로 확장은 round 2 후보.
- **L7 (no human / no LLM)**: 본 H 는 완전 hexa-only deterministic. 본 결과는
  단지 IIT4 4.0 의 big-Φ 함수 + 정의된 결합 substrate 의 closed-form 측정 — 그
  자체로 의식의 진실 주장 아님, IIT4 모델 내부 정리.

## Verification Provenance

- runner: `UNIVERSE/state/h352_collective_phi_super_additive_2026_05_28/run_h352.hexa`
- engine: `stdlib/consciousness/iit4_bigphi.hexa` (M4 via anima shim
  `HEXAD/IIT4/lib/iit4_bigphi.hexa` · `HEXAD/IIT4/lib/iit4_eca.hexa`)
- output: `state/.../result.json` (per-config Δ rows + verdict)
- cost: $0 mac local, wall < 10 min expected (4 rule-pair × 4 W × 5 seed × 80ms big_phi)
- llm: none · deterministic: true · hexa_only: true
