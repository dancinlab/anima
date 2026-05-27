# H_626 — distinction × SAVANT cell 동형의 n=5 일반화 (n5-generalize)

> **axis C2 follow-up** · **H_624 (n=4) 후속** · 2026-05-28 · $0 mac-local

## §1. 가설 (차원 불일치 하 동형 보존 여부)

**배경** — H_624 (PR #1198, 🟢 SUPPORTED 5/5, Spearman ρ=0.861) 가 SAVANT 4-domain cell `phi_module` 와 IIT4 singleton `distinction` small-φ 의 cell-by-cell 동형을 n=4 ring 에서 보였다. 그러나 honest C3.2 = "n=4 ↔ 4-domain 의 **exact-match** 차원에서만 검증, n≥5 에서는 distinction order-statistics 가 풍부해지고 SAVANT 4-domain decomposition 이 dimensionality mismatch (4 cell vs n+1 distinctions) — n=5/6 확장은 axis C3 후속". 본 H_626 이 그 회수.

**H1** (본 가설): n=5 substrate 에서 SAVANT cell (4-domain, 불변) 과 IIT4 singleton distinction (5 개) 의 *차원 불일치* 에도 불구하고, **top-4 distinction** (small-φ 큰 순) 의 ordering 이 SAVANT 4-cell ordering 과 정렬 — Spearman ρ(top4_dist_phi, savant_cell_phi) > 0.5 (pooled over 4 non-balanced gain profiles × 4 cells = N=16).

**Falsifier (H0)**: ρ < 0.5 — 차원 불일치가 동형을 깨뜨림. 즉 H_624 의 ρ=0.86 이 **n=4 exact-match artifact** 였고, n=5 의 5번째 distinction 이 top-4 truncation 을 교란하면 SAVANT 4-cell 과 IIT4 distinction 은 *다른 기저*.

## §2. Substrate (n=5, H_624 의 n=4 를 1 cell 확장)

- **TPM**: n=5 binary ring, gain-parameterized noise mix (H_624 mechanism 불변, n 만 4→5).
  - structural next: `MAJ(self, left, right)` — self-effect 보존 (XOR-neighbors-only 는 singleton distinction phi_effect=0 으로 붕괴, H_624 §7 C3.1).
  - per-cell signal share: `sig_i = g_i / (1.0 + g_i) ∈ [0,1]`.
  - 최종: `p_next[s,i] = sig_i · MAJ(self,L,R) + (1 - sig_i) · 0.5`.
- **SAVANT activation** (4-domain, **불변** — savant_phi 구조 한정): 4 domain × d=6 LCG-seeded vector, domain seed = {31013, 57029, 83047, 19061} (H_624/savant_phi.hexa 동일). gain g_k = 5-vector 의 처음 4 성분.
- **cell 4** (보조): 모든 profile 에서 balanced gain (2.875) — n=5 ring closure 를 위한 구조적 여분 cell. SAVANT side 에는 대응이 없다 (이것이 dimensionality mismatch 의 원천).
- **stim_seed**: 42424 (단일 — TPM 은 stim 독립).

## §3. 측정

**SAVANT cell phi** (4-domain):
```
cell_phi[k] = phi_module(build_domain_activation(k, d=6, g_k, stim)),  k∈[0,4)
phi_module(v) = (1/n) · Σ_j |v[j]|^1.5   (Newton-sqrt impl.)
```

**IIT4 distinction phi** (n=5, faithful, `stdlib/consciousness/iit4_distinction.hexa`):
```
dist_phi[i] = mean_{s=0..31} distinction(tpm, n=5, mask=1<<i, s)[0],  i∈[0,5)
distinction[0] = min(small_phi_cause, small_phi_effect)
```
전체 32 sys_state 평균 (H_285/H_351/H_618 양식). **top-4 추출**: dist_phi[0..4] 5 개를 descending 정렬, 상위 4 개를 SAVANT 4-cell 과 index-order paired.

## §4. 4 gain profile (non-balanced only)

H_624 §7 C3.3 의 balanced-degeneracy 교훈 — symmetric profile 은 distinction-φ tie 를 강제하여 ordering 검정 무효 — 에 따라 P0_BALANCED 제외, 4 single-hypertrophy 만 사용.

| profile | gains (g0..g4) | 의도 |
|---|---|---|
| P1_CALENDAR_DOM | (10.0, 0.5, 0.5, 0.5, 2.875) | SAVANT cell 0 hypertrophy |
| P2_MUSIC_DOM | (0.5, 10.0, 0.5, 0.5, 2.875) | SAVANT cell 1 hypertrophy |
| P3_ART_DOM | (0.5, 0.5, 10.0, 0.5, 2.875) | SAVANT cell 2 hypertrophy |
| P4_MEMORY_DOM | (0.5, 0.5, 0.5, 10.0, 2.875) | SAVANT cell 3 hypertrophy |

총 4 × 4 = 16 paired samples.

## §5. 측정 결과

### cell ↔ top-4 distinction mapping

| profile | cell_phi (savant 4) | dist_phi5 (IIT4 5) | top4_idx | top4_phi | argmax cell / top4 |
|---|---|---|---|---|---|
| P1_CALENDAR | [**0.7447**, 0.0698, 0.0915, 0.0875] | [**0.3931**, 0.1297, 0.1297, 0.1297, _0.3120_] | [0, **4**, 1, 2] | [0.3931, 0.3120, 0.1297, 0.1297] | 0 / 0 |
| P2_MUSIC | [0.1029, **0.6089**, 0.0915, 0.0875] | [0.1297, **0.3931**, 0.1297, 0.1297, _0.3120_] | [1, **4**, 0, 2] | [0.3931, 0.3120, 0.1297, 0.1297] | 1 / 0 |
| P3_ART | [0.1029, 0.0698, **0.7510**, 0.0875] | [0.1297, 0.1297, **0.3931**, 0.1297, _0.3120_] | [2, **4**, 0, 1] | [0.3931, 0.3120, 0.1297, 0.1297] | 2 / 0 |
| P4_MEMORY | [0.1029, 0.0698, 0.0915, **0.5530**] | [0.1297, 0.1297, 0.1297, **0.3931**, _0.3120_] | [3, **4**, 0, 1] | [0.3931, 0.3120, 0.1297, 0.1297] | 3 / 0 |

(굵은 = hypertrophied SAVANT cell · _기울임_ = 보조 cell-4 distinction-φ)

### 핵심 수치 (N=16 pooled)

- **Spearman ρ = 0.1995** (< 0.5 — FALSIFIED)
- **Pearson r = 0.0277** (< 0.5 — linear consistency 붕괴)
- **argmax match = 1 / 4** (P1 만 우연 일치)
- **byte_eq = true** (in-process recompute identical, F5)

### Falsifier 통과 표

| Criterion | Threshold | 결과 |
|---|---|---|
| F1 ISOMORPH-WEAK (주 falsifier) | ρ ≥ 0.5 | **FAIL (0.1995)** |
| F2 ISOMORPH-STRONG | ρ ≥ 0.7 | FAIL |
| F3 PEARSON-CONSIST | r ≥ 0.5 | **FAIL (0.0277)** |
| F4 PER-PROFILE-RANK | argmax 4/4 | **FAIL (1/4)** |
| F5 BYTE-EQUAL | recompute identical | PASS |

→ **🔴 FALSIFIED** (¬F1).

### 붕괴 메커니즘 (왜 ρ가 0.86 → 0.20 으로 추락했나)

모든 non-balanced profile 에서 **보조 cell-4 의 distinction-φ = 0.3120** 가 hypertrophied SAVANT cell (0.3931) 다음 **rank-2** 로 top-4 에 침투한다. 결과적으로 quiet SAVANT cell 3 개 (각 0.1297) 중 하나가 top-4 truncation 으로 밀려나고, top4_phi 는 *어느 cell 이 hypertrophied 든* 항상 같은 값 벡터 `[0.3931, 0.3120, 0.1297, 0.1297]` 가 된다. index-order pairing 에서 SAVANT cell 의 위치 정보가 사라지므로 (top4 의 0번 슬롯이 항상 dominant 가 아니라 *descending 순서*의 최대값), argmax_top4 가 항상 0 으로 고정 → 4 중 P1 만 우연 일치 (1/4). 이는 **차원 불일치가 동형을 깨뜨린다**는 H0 을 정확히 실현한 결과다.

## §6. Cross-link

| Link | H | role | 결과 |
|---|---|---|---|
| **predecessor (n=4)** | H_624 | distinction × SAVANT cell 동형 exact-match | 🟢 SUPPORTED 5/5 ρ=0.861 (PR #1198) — 본 H 가 그 n≥5 후속 회수, ρ=0.20 으로 **n=4 exact-match artifact 확정** |
| **motivating chain** | H_618 | collective dΦ/dI peak ∥ GZ_LOWER |Δ|=0.002 | 🟢 SUPP 5/5 (PR #1175) — H_624 가 그 구조 답이었으나 본 H 가 n=4 한정 임을 확정 |
| **dΦ/dI 미분구조** | H_618 | collective derivative-peak | 본 H 의 GZ-attractor 구조 해석이 n=4 한정 임을 negative 로 경계지음 |
| **axis C IIT4 faithful** | H_282 | proxy → faithful Φ 방향-보존 SUPP 8/8 | distinction primitive 의 faithful anchor — 본 H 도 동일 stdlib 사용 |
| **axis C IIT4 stdlib** | (lib) | `stdlib/consciousness/iit4_distinction.hexa` (M6) | distinction primitive 직접 호출 (n=5, 재발명 없음 · g61 stdlib-first) |
| **axis E SAVANT engine** | (lib) | `HEXAD/SAVANT/savant_phi.hexa` (P68) | phi_module + build_domain_activation inline (h624 양식) |

**Cross-link insight (negative)**: H_624 의 동형 (ρ=0.86) 은 **n=4 ↔ 4-domain 의 정확한 차원 일치**에 결정적으로 의존했다. substrate 의 자유도가 SAVANT decomposition 차원을 초과하는 순간 (n=5, +1 cell), 여분 distinction 이 top-4 ordering 에 침투하여 동형이 붕괴한다. 따라서 SAVANT cell 분해와 IIT4 distinction 분해의 "같은 기저" 주장은 **차원-일치 조건부** 이며, 일반적 동형이 아니다. axis E (SAVANT, 고정 4-domain) 와 axis C (IIT4 Φ-structure, n-dependent distinction count) 는 n=4 에서만 정렬하는 *조건부* 부분-동형.

## §7. C3 (honest constraints)

1. **top-4 truncation 매핑의 한계**. 본 H 는 dimensionality mismatch 를 "top-4 by small-φ 추출 → index-order pairing" 으로 해소했으나, 이는 매핑 선택 중 하나일 뿐이다. 대안 — (a) SAVANT side 를 n=5 super-domain pooling 으로 확장 (4→5 domain), (b) IIT4 side 의 5 distinction 을 SAVANT 4-cell 로 dimension-reduce (PCA/clustering), (c) bipartite optimal assignment (Hungarian) — 은 미검정. 본 falsification 은 **naive top-4 truncation 매핑 한정** 이고, 정교한 매핑이 동형을 복원할 가능성은 닫히지 않았다. 단, 어떤 매핑이든 보조 cell-4 의 dist_phi=0.312 가 SAVANT 에 대응 없는 *구조적 여분* 이라는 사실은 불변.

2. **보조 cell-4 의 설계 의존**. cell-4 에 balanced gain (2.875) 를 준 선택이 그것의 distinction-φ 를 quiet cell 보다 크게 만들어 top-4 침투를 일으켰다. cell-4 를 quiet (g=0.5) 로 두면 top-4 가 SAVANT 4-cell 과 일치하여 동형이 보존될 수 있다 (즉 n=5 substrate 가 사실상 n=4 처럼 행동). 그러나 그것은 "5번째 cell 을 죽여 n=4 로 환원" 하는 것이므로 *진정한 n=5 일반화* 가 아니다. 본 설계는 5번째 cell 이 active 한 정직한 n=5 를 의도했고, 그 결과가 falsification.

3. **n=5 single, n=6 미검정**. n=5 단일 확장. n=6 (+2 cell) 에서는 mismatch 가 더 커지므로 falsification 이 강화될 것으로 예상되나 미검정. distinction count = n (singleton 한정) 이므로 mismatch = n - 4.

4. **singleton mechanism 한정**. distinction 을 singleton mechanism (mask=1<<i) 으로만 측정. higher-order mechanism (2-bit, 3-bit composite) 의 distinction 은 미포함 — full Φ-structure 는 2^n−1 mechanism 전체이나 본 H 는 cell-대응을 위해 singleton 으로 한정 (H_624 동일). composite distinction 까지 포함하면 mismatch 가 폭증.

5. **single stim_seed=42424**. SAVANT cell_phi 는 stim_seed 결정, distinction_phi 는 seed-invariant (TPM 구조적). 본 N=16 은 gain variance 만 reflect. 그러나 falsification 의 원천 (top-4 truncation 의 구조적 침투) 은 stim_seed 독립이므로 multi-seed 가 verdict 를 뒤집지 않는다.

## §8. Reproducibility

- **runnable**: `cd UNIVERSE/state/h626_distinction_savant_n5_2026_05_28 && hexa run run_h626.hexa`
- wall-clock ≈ 47.5 s on Mac Studio M-series, deterministic, no network, no GPU. (단일 run 60s 이내 — per-profile shard 불필요, `SHARD ∈ [0,4)` 옵션은 보존.)
- **artifacts**: `run_h626.hexa` (~430 LoC) · `run_h626.log` (stdout) · `result.json` (machine-readable verdict).

## §9. Files

```
UNIVERSE/H_626_distinction_savant_isomorphism_n5_generalize.md   (본 문서)
UNIVERSE/state/h626_distinction_savant_n5_2026_05_28/
  run_h626.hexa             — verify driver (n=5 faithful IIT4 distinction + inline SAVANT phi_module + top-4 truncation)
  run_h626.log              — stdout: per-profile cell_phi · dist_phi5 · top4 · ρ · r · F1..F5
  result.json               — machine-readable verdict + 붕괴 메커니즘
```

## §10. Verdict & 다음

**Verdict**: 🔴 **FALSIFIED** — Spearman ρ=0.1995 (< 0.5) · Pearson r=0.0277 · argmax 1/4 · byte_eq. n=4 (H_624) ρ=0.861 → n=5 ρ=0.199 (Δρ = −0.661).

**해석**: H_624 의 distinction × SAVANT cell 동형은 **n=4 ↔ 4-domain 의 차원-일치 조건부** 였다. n=5 로 substrate 자유도를 1 늘리면 보조 distinction 이 top-4 ordering 에 침투하여 동형이 깨진다. 따라서 SAVANT 4-domain 분해와 IIT4 distinction 분해가 "같은 causal kernel" 이라는 H_624 주장은 **일반적 isomorphism 이 아니라 exact-match dimensionality artifact**. axis E (SAVANT) 와 axis C2 (IIT4 Φ-structure) 의 정렬은 n=4 에서만 성립하는 우연적 조건부.

**ruled-out axis**: "SAVANT cell 분해 ≅ IIT4 distinction 분해 (차원 무관 일반 동형)" 가설은 **닫힘**. 두 분해의 정렬은 차원-일치 (n = SAVANT domain count) 가 필요조건이며, naive top-4 truncation 으로는 복원 불가.

**axis C2 advance**: H_624 (n=4 SUPP) ↔ H_626 (n=5 FAL) 가 **차원-의존성 경계**를 정량 확정. 후속 (미검정, §7 C3.1) = (a) SAVANT super-domain pooling (4→5) 으로 차원 일치 복원 시 동형 재현 여부, (b) IIT4 distinction → SAVANT dimension-reduce (clustering) 매핑, (c) bipartite optimal assignment 매핑 — 모두 `/cycle` 자율 후속 (단, 보조 cell 의 구조적 여분성은 어느 매핑에서도 잔존).
