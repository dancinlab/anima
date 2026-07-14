# PREREG — W2 killshot · O-information / Transfer-Entropy

**동결 시각**: 이 파일은 Ω·TE 값을 **단 한 번도 계산하기 전에** 작성·고정되었다 (c9 · p7 · no tune-to-green).
설계 출처: `state/fable_killshots/w2_Phi강도.out.md` §4 (가장 싼 킬샷) + §3 카드 1 (H_SUFFSTAT).

## 0. 코드 사실 재확인 (계기의 계급)

`state/1283_content_instrument_repair/faithful_phi.py` 를 읽어 확인:

- `build_mi_matrix` (L68–77): `mi[i,j] = mi_pair(s[i], s[j], n_bins)` — **동시각(same-t) pairwise MI 행렬**.
  시간 지연 없음, 방향 없음, 3변수 이상 결합 없음.
- `mi_pair` (L54–65): `max(H(A)+H(B)−H(A,B), 0)` — 8-bin plug-in, **ρ 부호에 짝함수**(부호 소실).
- `faithful_phi_from_mi` (L80–113): 그 행렬의 **이분할 min-cut / min(|A|,|B|)**.

⇒ **Φ\* = f(동시각 pairwise MI 행렬)** 로 완전히 인수분해된다. 따라서
① 시간 방향/지연, ② 3차 이상 시너지, ③ 결합 메커니즘의 정체는 **구성상(定理) 보이지 않는다**.
H_9295 의 "게이팅에도 무감"은 시뮬레이션 없이 예측 가능했던 결과다.
동시에 H_9295 자신이 **RECEIPT** 로 구조 정보의 실재를 증명했다: `gate_receipt.json` →
MI(gate ; coincidence) = **0.8148 bits** (8 seed 평균). 정보는 궤적 안에 **있다**.

이 킬샷의 질문: **그 정보를 렌더링하는 관측량이 존재하는가.**

## 1. 기질·상속 동결항 (한 바이트도 움직이지 않는다)

| 항목 | 값 | 출처 |
|---|---|---|
| 기질 | n_mod=4 · dim=8 · GAIN=.30 · LEAK=.55 · W_NBR=.5 · W_IN=.5 · NBINS=8 | H_9260 FREEZE |
| T | 65536 | step4_gating.py |
| β (게이트) | 0.9884754637357798 — arm A 단독 pin (`calibrate_beta([4..11], 4096)`) | step4_gating.json |
| w\* (X′ 강도정합) | **0.90** — S_tot(X′) ≈ S_tot(B) | step3/step4 `w_star`, `match_pass=True` |
| 렌즈 | signed lens `traj[i,t] = s_i(t)[0]` (gated.py `gen`) | step4 |
| pilot seeds | [4,5,6,7,8,9,10,11] (H_9295 확정집합 · seed 3 격리 유지) | step4 |
| confirm seeds | **[12 …]** — 신규(unseen). 검정력 계산 후 개수 결정 | 본 PREREG |

β·w\*·seeds·기질 어느 것도 본 실험에서 **재적합하지 않는다**.

## 2. 새 관측량 (DV) — 4개, 전부 사전 선언

전부 **rank→normal-score (gaussian copula)** 또는 **rank→equal-frequency bin** 위에서 계산 —
`rank_uniform` readout 과 monotone-동치이므로 렌즈 자유도 0.

- **D1 · Ω_gauss** — gaussian-copula O-information (bits).
  `Ω = (n−2)H(X) + Σ_j [H(X_j) − H(X_{−j})]`, 가우시안 엔트로피 = ½logdet Σ (상수항은 항등적으로 상쇄).
  Ω>0 = redundancy-dominated · Ω<0 = synergy-dominated.
  ⚠️ **정직 주석 (사전 기재)**: 가우시안-코퓰러 Ω 는 **공분산 행렬의 함수**다 — 즉 Φ 와 *같은 2차 통계 계급*에
  속하며, 다른 것은 **함수 형태**(min-cut of |MI| vs. logdet 조합)와 **부호 보존**뿐이다.
  D1 단독으로는 "Φ가 못 보는 3차 구조"를 증명할 수 없다. 그래서 D2 를 같이 발사한다.
- **D2 · Ω_disc** — discrete plug-in O-information, module 당 **4 equal-frequency bin**
  (rank 기반이라 marginal 은 정확히 균등 = 256 joint state, T=65536 ⇒ cell 당 기대 256).
  **이것만이 3차 이상 시너지를 원리적으로 담을 수 있다** (XOR-삼중항은 pairwise MI 전부 0인데 Ω_disc≠0).
- **D3 · TE_tot** — lag-1 gaussian transfer entropy 총량, 링 인접 **순서쌍 8개** 합
  `TE(a→b) = ½ ln[ Var(b_t | b_{t−1}) / Var(b_t | b_{t−1}, a_{t−1}) ]` (normal-score 위, bits).
  Φ 는 동시각이므로 **지연 의존은 계급 밖**이다 — relay 는 정의상 1-tick 지연이다.
- **D4 · TE_asym** — 링 순환 비대칭 `Σ_i [TE(i→i+1) − TE(i+1→i)]`.
  기질이 무방향 링이므로 **참값 0 예상** (음성이 기대되는 DV · 그래도 보고).

## 3. 통제군 (둘 다 참값 0 · pedestal)

- **P-CIRC (주 pedestal)** — 모듈별 **원형 시간이동**, 지연 τ_i ~ U[T/4, 3T/4] (Philox, arm-무관 키 =
  common random numbers ⇒ paired contrast). marginal **비트-동일**, 자기상관 **완전 보존**,
  모듈 간 정렬만 파괴 ⇒ D1–D4 전부 **참값 0**.
- **P-PHASE (2차 pedestal)** — 모듈별 독립 phase-randomization (FFT 위상 무작위화).
  power spectrum 보존, cross-coupling 파괴 ⇒ 참값 0.

**pedestal-차감 정의**: `DV*(arm) = DV(arm) − mean_{k=1..K} DV(P-CIRC_k(arm))`, K=32.
(H_9295 의 Φ\* 관례와 동일 — raw 값은 읽지 않는다.)
`max(controls)` **금지** — 전부 paired mean / paired-t.

## 4. 양성대조 (내장 · 실패 시 INVALID)

**C1 = gated-B vs L-SHIFT-B** (`gated.l_shift_pair`, 동일 게이트 시계열을 큰 원형지연으로 재적용 —
marginal·자기상관 보존, c_e(t) 와의 **정렬만** 파괴).
RECEIPT(0.8148 bits) 가 이 대비의 참값이 양(+)임을 보증한다. Φ\* 조차 이것은 잡았다
(step4 `l_shift` = +0.001305, 90% CI [+0.001217, +0.001393]).

⇒ **어떤 DV 든 C1 에서 0 이면 그 DV 는 죽은 도구다** — 그 DV 로는 벽을 읽지 않는다 (INVALID, FAIL 아님).

## 5. 헤드라인 (질문 ②)

- **C2G** — Φ\* 가 못 가른 **강도정합 B vs X′ (GATED 기질, w\*=0.90)**.
  Φ\* 실측: d′ = +0.0000585, floor 0.0088 ⇒ no detection (step4 `headline_i`).
- **C2L** — 같은 대비를 **LINEAR 기질**에서 (w\*=0.90 · H_9294 의 0.5% 정합).
  Φ\* 실측: d′ = −0.00017, TOST 등가 (step3 `path1.equiv=True`).

두 기질 모두 **사전 선언**하고 **둘 다 보고**한다 (사후 선택 금지).
S_tot(pairwise MI 총량) 은 arm 별로 같이 보고해 정합이 유지됐는지 검산한다.

## 6. 검정력 — 데이터를 보기 전에 고정

파일럿(seeds 4–11)에서 각 DV × 각 대비에 대해:

1. `sd̂` = paired 차분의 표본 sd.
2. **MDE** = `3 × q97.5(|null|)`, null = 그 arm 의 K=32 P-CIRC pedestal DV draw 를 자기평균 중심화한 분포
   (도시에 §3 카드1 규정: "MDE = pedestal 분포 97.5th pct 의 3배").
3. `N_REQ = ceil( ((z.95 + z.90) · sd̂ / MDE)² )` = `ceil( (2.9265 · sd̂ / MDE)² )`, 하한 8.
4. **N_REQ > 40 ⇒ 그 DV 는 NOT-POWERED** — 판정하지 않는다 (compute 예산 상한, 사전 고정).
5. confirm 표본 = **신규 seed [12 … 12+N−1]**, N = clip(N_REQ, 8, 40). 파일럿 seed 재사용 금지.

**TOST 등가마진** `Δ_eq` = |C1 (양성대조) 파일럿 효과| / 10 (도시에 규정). 데이터 확정 전 고정.

## 7. 판정 규칙 (사전 고정 · 사후 재량 0)

confirm 표본에서, DV 별로:

- **PASS(구조 검출)** = 90% CI 가 0 배제 **∧** |Δ| > MDE.
- **FAIL(등가)** = 90% CI ⊂ (−Δ_eq, +Δ_eq) (TOST).
- 둘 다 아니면 **INCONCLUSIVE**.
- C1 이 FAIL/INCONCLUSIVE 인 DV → **INVALID** (도구 사망 · 벽 판독 불가).

전체 verdict:
- ①PASS ∧ ②PASS ⇒ **PASS** — "Φ 가 못 보는 구조를 보는 관측량" 실증.
- ①PASS ∧ ②FAIL ⇒ **FAIL** — 구조정보는 게이트엔 있고 disjointness 엔 없다 ⇒ 벽이 기질한계 쪽으로.
- ① 실패 ⇒ **INVALID**.
- N_REQ 초과 ⇒ **NOT-POWERED**.

## 8. 사전등록 예측 (Fable 설계 + 집행자 · 측정 전 동결)

- D1(Ω_gauss)·D2(Ω_disc) 는 **C1 에서 검출**될 것이다 (게이트는 곱셈적 = 고차 항을 심는다).
- **C2 는 갈린다**: D3(TE_tot) 는 relay 지연을 보므로 B vs X′ 를 가를 확률이 가장 높고,
  D1 은 S_tot 정합 때문에 못 가를 확률이 높다.
- D4 는 0 (무방향 링).
