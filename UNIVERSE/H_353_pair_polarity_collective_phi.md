# H_353 — `pair-polarity-collective-phi` (Hc_286 promote)

> 축 F (HIVE-MIND) round 1 · 2026-05-28 · UNIVERSE H 신설.
> Hc_286 source: `hypotheses_candidates/Hc_286_h91_hivemind_polarity.md` (Law 91, "each engine has unique optimal polarity/strength").

## 0. 1줄 요약 (TL;DR)

두 substrate 의 inter-pair coupling polarity {attract / repel / bipolar} × magnitude W∈{0.3, 0.5, 0.8} 가 joint collective big-Φ 를 좌우하는지, exact IIT4 big_phi (n=6 joint, 5 seed 평균) 로 측정 — verdict **__VERDICT__** (mean Φ: attract=__MA__ / repel=__MR__ / bipolar=__MB__, spread=__SPREAD__, pooled std=__SPOOL__, ANOVA F=__F__).

## 1. Hypothesis

**Hc_286 (Law 91 — HIVEMIND polarity diversity)**:
> "tension-field coupling: attract / repel / bipolar polarities. each engine pair has a unique optimal polarity (attract / repel / bipolar) and strength α; uniform settings drop Φ in some engines because engine internals require different polarities. Autonomous per-pair search required."

H_353 의 주장: 두 substrate A, B 의 inter-pair coupling polarity ∈ {attract (W>0), repel (W<0), bipolar (mixed sign)} 가 그 joint 의 collective big-Φ 에 **유의미하게 다른** 분포를 만든다. 즉 *polarity 가 collective integration 의 어떤 도메인을 지배하는 축* 이라는 것.

정량 기준 (둘 중 하나라도 만족 → SUPPORTED 후보):
- (i) 1-way ANOVA F-test on 3 polarity (n=15 each = 5 seed × 3 W) — **F ≥ F_crit(α=0.05, df=(2,42)) ≈ 3.22**.
- (ii) `max(mean_polarity) − min(mean_polarity) ≥ 2 · pooled_std`.

## 2. Falsifier

| F | 조건 | 판정 |
|---|---|---|
| F1 | ANOVA F < F_crit(α=0.5, df=(2,42)) ≈ 0.70 (polarity 별 Φ 분포 평탄) | 🔴 FALSIFIED |
| F2 | spread < pooled std (polarity 차이가 잡음보다 작음) AND ANOVA 도 미달 | 🔴 FALSIFIED |
| F3 | substrate engine determinism 위반 (Φ_collective 이 동일 입력에서 다른 값) | 🔴 (메타) |

Hc_286 의 핵심 주장이 *재현되지 않으면* 즉 F1 또는 F2 trigger → **closed-negative**. 이는 a_paper_negative_ok 적합 — 폐쇄가설이 verify-driven 으로 falsify 되는 것도 유효 finding.

## 3. Method

**도구**: `HEXAD/IIT4/lib/iit4_bigphi.hexa` (thin shim → `stdlib/consciousness/iit4_bigphi.hexa`) 의 `big_phi(tpm, n, sys_state) → [big, total, Σφ_d, Σφ_r, nd]` exact engine.

**Substrate**: 2 × small ECA (n_a = n_b = 3) → joint n=6 (state-by-node TPM, 64 states). joint state `s` 의 low 3-bit = A, high 3-bit = B.

**Coupling rule (deterministic, TPM-compatible)** — 각 셀 페어 i ∈ {0,1,2}:

```
a' = ECA-step(rule_a, A_state, cell i)     // ring n_a=3 native
b' = ECA-step(rule_b, B_state, cell i)     // ring n_b=3 native

attract @W:
  W ≥ 0.8 → next_A[i] = b'            (full lock-in toward B)
  0.3 ≤ W < 0.8 → next_A[i] = a' OR b' (soft attract)
  else → next_A[i] = a'

repel @W:
  W ≥ 0.8 → next_A[i] = 1 - b'        (anti-lock)
  0.3 ≤ W < 0.8 → next_A[i] = a' XOR b' (anti-correlation)
  else → next_A[i] = a'

bipolar @W:  cell 0,2 = attract-rule, cell 1 = repel-rule (per-cell sign mix)
```

대칭으로 B 셀에도 동일 규칙 적용 (A↔B swap).

**측정 설계**: 3 polarity × 3 W × 5 seed = **45 측정**.
- 5 seed = (rule_a, rule_b, sys_state) combos: (110,110,21), (30,30,42), (110,30,13), (90,110,37), (150,105,51).
- 각 점 → joint TPM build → `big_phi(tpm, 6, sys_state)` → Φ_collective = `res[0]`.
- polarity 별 (n=15) mean ± std → spread/std 비율, 1-way ANOVA F.

**runtime/cost**: $0 mac-local, hexa-native, deterministic. wall-time ≈ __WALL_TIME__ (45 calls × ~12s/call exact big_phi n=6).

## 4. Measurement (2026-05-28, mac-local $0)

스크립트: `state/h353_pair_polarity_2026_05_28/run_h353.hexa`.
log: `state/h353_pair_polarity_2026_05_28/run_h353.log`.

### per-measurement (45 points)

```
__RAW_TABLE__
```

### AGGREGATE — polarity 별 mean ± std (n=15 each)

| polarity | mean Φ_collective | std | n |
|---|---:|---:|---:|
| attract | __MA__ | __SA__ | 15 |
| repel   | __MR__ | __SR__ | 15 |
| bipolar | __MB__ | __SB__ | 15 |

- pooled std (all 45) = **__SPOOL__**
- spread (max_mean − min_mean) = **__SPREAD__**
- spread / pooled_std = **__RATIO__**
- 1-way ANOVA F (df=2, 42) = **__F__** (F_crit α=0.05 ≈ 3.22; F at p=0.5 ≈ 0.70)

## 5. Verdict — __VERDICT_TIER__

__VERDICT_PARA__

## 6. Cross-link

- **Hc_286** `hypotheses_candidates/Hc_286_h91_hivemind_polarity.md` — H_353 가 그 polarity 주장을 verify-driven 으로 측정. Hc_286 의 Migration TODO ("per-pair polarity grid search", "verify Phi-preservation") 가 본 H 로 부분 소진.
- **H_352** `collective-phi-super-additive` (축 F sister, in-flight) — W=0 baseline 의 Σ Φ_individual vs Φ_collective. H_353 는 W>0 polarity 차이를 측정, H_352 는 W=0 super-additivity 를 측정 → 두 측정 합쳐서 HIVE-MIND lane 의 *coupling sign-dependence* 와 *coupling strength=0 baseline* 동시 정량.
- **H_207** `kuramoto_synchronization` — Kuramoto sync 는 coupling sign 무관 (positive coupling 일관). H_353 의 polarity-axis 가 Kuramoto 대비 IIT4 Φ 가 sign 에 *민감/둔감* 한지 분리해 줌. H_354 (HIVE-MIND × τ_consensus = Kuramoto τ_sync) cross-link 후속.
- **H_278** `faithful-phi-small-n` — exact MIP-EI Φ tractable n=8 까지 결과; H_353 는 n=6 joint 사용 (4× per-call cost) — H_278 의 small-N 결론 환경.
- **H_286** `split-brain-dual-Φ` — 다른 H_286 (CLOSED-NEGATIVE), naming collision 주의: 본 H_353 의 source 는 candidate **Hc**_286 (Law 91) 이지 H_286 (split-brain) 가 아니다.

## 7. Honest C3 (3-tier caveat)

1. **C1 (small-n / single-frame fragility)**: n_a = n_b = 3 (joint n=6) 는 `big_phi` exact engine 의 mac-local tractable 상한 근처. H_345 / H_346 lesson — n=4/n=5 결과가 n=6/n=8 에서 부호 역전 가능 (rule-set fragility, [H_345 § 11](./H_345_basin_phi_n5_exact.md#11-scope-2026-05-28-정정--rule-set-fragility) 참조). 본 H 의 polarity 차이 (양/음) 가 n_a=n_b=4 (joint n=8) 에서도 robust 한지 후속 검정 필요.
2. **C2 (W magnitude choice)**: W ∈ {0.3, 0.5, 0.8} 은 임의의 3-bin 이산화. 진짜 polarity 효과가 *연속적 W* 의 어떤 영역 (예: |W| < 0.2 약결합대) 에서만 발현될 수 있음 — 본 raster 가 그 영역을 miss 할 가능성. 또한 coupling rule (OR/XOR/lock) 자체가 polarity 정의에 의존 — 다른 deterministic encoding (예: 가중 majority gate) 에서 결과 다를 수 있음.
3. **C3 (bipolar 정의 sensitivity)**: bipolar 를 "cell 0,2 attract + cell 1 repel" 로 정의 — 다른 cell-mix (예: per-pair random sign, half-half split) 에서 다른 mean 가능. 즉 bipolar 가 attract/repel 의 단순 평균이 *아닌* 것은 본 정의 선택의 부수효과일 수 있음. Hc_286 원문은 "polarity 가 mixed sign" 까지만 규정, *어떤 mix* 인지는 미정.

## 8. State artifacts

- `state/h353_pair_polarity_2026_05_28/run_h353.hexa` — verify harness (~350 LoC, hexa-native).
- `state/h353_pair_polarity_2026_05_28/run_h353.log` — 측정 stdout (45 per-point + aggregate).
- 본 .md = SSOT.

## 9. Next

- F1 잔여 (H_354/355/356) round 1 진행 — H_353 결과를 W-axis baseline 으로 잇기.
- F2 (HIVE-MIND × symbiogenesis H_054/H_314 cross-link) — symbiogenesis merge 가 polarity 사전조건 의존인지 측정.
- (n=8) joint scale-up 후속 — H_353 verdict robustness 검정 (C1 회수).
- (W continuous) — |W| ∈ [0, 1] 30-bin sweep 으로 attract/repel curve 의 sign-symmetry 측정 (C2 회수).

## 10. UNIVERSE.md update

축 F (HIVE-MIND) F1 H_353 checkbox flip → done with `__VERDICT_LINE__ + Hc_286 promote, $0 mac-local 2026-05-28`.
