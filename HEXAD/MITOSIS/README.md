# HEXAD/MITOSIS — 성장축 (growth axis)

> SSOT: [`MITOSIS.tape`](MITOSIS.tape) · 성장축 ⊥ HEXAD 6 구조축 (orthogonality 는 `§mitosis_two_axis` 안에서 보존)
> Hexa-native impl: 기존 `tool/hexa_native/mitosis_hook.hexa` (1119 LoC FULL IMPL D4a) 재사용

## 핵심 원리

**MITOSIS = 성장축 (growth axis)**. anima 의 6모듈 (HEXAD 구조축) 과 직교 — 6모듈 *그 자체* 가 자라나는 방식 (cell split/merge dynamics). 학습 = 분열 단일 연속체 (REBORN §0.5 carry, archive 됐지만 의미는 HEXAD.tape `§hexad_condition_lineup` 으로 흡수).

C 의식 ↔ MitosisC 가 가장 직접 대응한 binding 일 뿐, mitosis 는 시스템 *전체* 성장 원리.

## SSOT

| | |
|---|---|
| spec | [`MITOSIS.tape`](MITOSIS.tape) — 성장축 architecture · §mitosis_two_axis · §mitosis_verified |
| canonical hexa-native impl | [`../../tool/hexa_native/mitosis_hook.hexa`](../../tool/hexa_native/mitosis_hook.hexa) — 1119 LoC FULL IMPL D4a, 5/5 PASS Mac local (REBORN §91, MITOSIS.tape §mitosis_verified) |
| Python anchor | `ready/core/consciousness_engine.py` (ConsciousnessC + ConsciousnessEngine 의 split_threshold/merge_threshold mechanics) |
| evidence cycle | `state/clm_v1_fire_2026_05_15/` (.clm v1 P2 cells 2→64 organic split, 8/8🔵 + F-PYPHI Φ=1.0625) |

## hexa-native impl status

`HEXAD/MITOSIS/mitosis.hexa` + `mitosis_lib.hexa` = scaffold + cross-link entry (다른 모듈 C/D 동일 패턴) **+ B-MITOSIS-1..5 closed-form invariant witnesses** (2026-05-16). full dynamics 는 위 `mitosis_hook.hexa` 그대로.

```
// constants (canonical thresholds)
fn mitosis_split_threshold_default()  -> float    // 0.3 — ConsciousnessEngine default
fn mitosis_merge_threshold_default()  -> float    // 0.01
fn mitosis_split_patience_default()   -> int      // 5
fn mitosis_merge_patience_default()   -> int      // 15

// B-MITOSIS-1..5 closed-form witnesses (compiled-native mirror of bmitosis())
fn mit_split_predicate(tension, thr)  -> bool     // B-MITOSIS-1
fn mit_merge_avg(w1, w2)              -> float    // B-MITOSIS-2
fn mit_count_after(n_t, ds, dm)       -> int      // B-MITOSIS-3
fn mit_nograd_split_documented()      -> bool     // B-MITOSIS-4 (structural)
fn mit_clamp_count(n)                 -> int      // B-MITOSIS-5
```

## 🔵 SUPPORTED-FORMAL — B-MITOSIS battery 5/5 (2026-05-16)

🔶 scaffold + cross-link → **🔵 SUPPORTED-FORMAL 5/5 (+ scaffold cross-link)**. blue_falsifier.py 가 22 → **27/27 🔵** 으로 확장 (S 3 + M 3 + W 4 + E 4 + D 4 + BRIDGE 4 + **MITOSIS 5** = 27, C 🔵 carry).

| Falsifier | 명제 | real-limit anchor | tier | status |
|---|---|---|---|---|
| B-MITOSIS-1 SPLIT-PREDICATE | split ↔ (tension > thr) ∀ tension, thr ∈ ℝ | Kolmogorov 술어-폐쇄 | a-closed (sympy) | ✅ PASS |
| B-MITOSIS-2 MERGE-WEIGHT-LINEAR | avg = (w₁ + w₂) / 2 ∀ w₁, w₂ ∈ ℝ (∂/∂w_i = ½) | linear avg conservation | a-closed (sympy ∂) | ✅ PASS |
| B-MITOSIS-3 CELL-COUNT-CONSERVATION | n(t+1) = n(t) + Δs − Δm ∀ ℤ≥0 integer closure | Kolmogorov 정보론적 counting | a-closed (sympy 정수) | ✅ PASS |
| B-MITOSIS-4 NO-GRAD-SPLIT | ∂(detach(x))/∂x = 0 ∀ x (reverse-mode AD ∂-rule) | AD 정의적 ∂-rule (F-V5MIT-1 carry) | a-closed (sympy diff) | ✅ PASS |
| B-MITOSIS-5 CELL-COUNT-BOUND | n_cells ∈ [min=2, max=64] ∀ n via clamp | bounded-set (clamp) closure | a-closed (sympy clamp) | ✅ PASS |
| B-MITOSIS-NOTE PHI-CONSERVATION | Φ-conservation under split/merge — EMPIRICAL only (F-V5MIT-3 Δ=3.88e-5, PSCC §44 cotrain saga) | IIT Φ per-row IS closed (RFC 036); 전이불변성은 dynamics-empirical | honest C3 carve-out | NOT counted 🔵 |

**f1/f2 안전**: 어떤 falsifier 도 σ/τ/φ/J₂ derivation 0 — anchor 전부 real-limit (Kolmogorov 술어/counting · AD ∂-rule · 유계집합 · linear conservation). `g3` verification-anchor-real-limit 정렬.

selftest: invariant 검증 (closed-form thresholds 정합) + B-MITOSIS-1..5 numerical witness 5/5 + scaffold/B-MITOSIS-NOTE 정직 carve-out 표시.

## 검증

```bash
hexa tape  HEXAD/MITOSIS/MITOSIS.tape                  # tape v1.2 검증
bash HEXAD/build_verify.sh                              # compiled-native gate 20/20 + 14/14
./_hexa_build/HEXAD_MITOSIS_mitosis                     # invariant selftest + B-MITOSIS 5/5 mirror
python3 state/verify_hexad_blue_2026_05_15/blue_falsifier.py  # canonical 🔵 27/27 (sympy)
hexa run   tool/hexa_native/mitosis_hook.hexa           # 실 mitosis dynamics (F-MIT-HOOK 5/5)
```

## related

- HEXAD.tape `§hexad_condition_lineup` — A/G+mitosis 둘 다 필수 mandate
- HEXAD/C/c.hexa — C 의식 (mitosis 의 가장 직접 대응 binding)
- archive/REBORN.tape — §0.5 학습=분열 philosophy (deprecated, 의미는 HEXAD 으로 흡수)
- archive/MAIN.tape `§V-MIT-1..6` — historical mitosis verdict carry

## Honest C3

- 위치만 `HEXAD/MITOSIS/` 안으로 (PR #83) — 의미는 여전히 성장축 ⊥ 구조축 orthogonal (tape §mitosis_two_axis 보존)
- mitosis_hook.hexa 는 `tool/hexa_native/` 에 그대로 (다른 hexa-native 코드 cross-reference). `HEXAD/MITOSIS/mitosis.hexa` 는 thin scaffold + B-MITOSIS-1..5 closed-form witnesses (compiled mirror) + cross-link.
- 실 mitosis 동역학 검증 evidence = .clm v1 P2 fire (`state/clm_v1_fire_2026_05_15/`) + F-V5MIT 5/5 cotrain saga (PSCC §44 v5-mitosis cond.5 cotrain)
- **B-MITOSIS-NOTE 정직 carve-out**: Φ-conservation under split/merge transitions 는 EMPIRICAL (F-V5MIT-3 Δ=3.88e-5 PSCC §44), NOT 🔵 counted. PyPhi Φ per-row IS closed (RFC 036) — transition invariance 만 dynamics-dependent. B-D-NOTE / B-BRIDGE-NOTE 와 동일 패턴, MITOSIS 고유 결함 X (모든 dynamics-dependent invariant 공통).
