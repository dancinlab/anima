# H_9287 — 🔬 재조합 대수의 **물리** 담체 — 국소 관측만으로 오라클의 supply 이득에 도달할 수 있는가 (H_054/H_203의 끝 · $0)

- **tier:** 🔵 PRE-REGISTERED (미측정)
- **wired:** none.
- **family:** 🔋 ORGANELLE LANE 파생 — lane 자체는 CLOSED(licensed by equivalence · [[H_9285]])이나, **merge 대수 물음은 lane과 별개로 살아 있다**(선행 H_054 symbiogenesis · H_203 asymmetric merge의 미답 물음).
- **lens:** [[H_9274]] 5차가 **존재 증명**을 냈다 — 되먹임 있는 기질(LIVE)에서 **오라클이 총 supply를 실제로 올린다(+1.91, p=0.040)** 면서 overload는 안 올린다(−0.001 ns). ⇒ **재조합 대수가 물리 정보를 더할 수 있다는 것은 증명됐다.** 그러나 **국소 slack 담체(a_comp)는 그 채널을 못 탄다** — 장부(ATP)만 +12.8 올리고 물리는 개선 0 또는 **유의 악화**(overload +0.117, p=2.3e-5). 진단: a_comp는 장부 헤드라인 `Σmin(L,S)`의 순간기울기를 **capture 0.98**로 타는 정책이었다(순간-argmax 통제 `a_detgrad`에 오히려 짐) = **장부 항등식**.
- **artifacts:** `state/mito_organelle_lane/F14_physical_carrier/`
- **xref:** [[H_9274]](F2 1~5차 · sham 해결 · 오라클 물리채널 존재증명) · [[H_9285]](lane CLOSED licensed by equivalence) · H_054(symbiogenesis = mitosis MERGE) · H_203(host-preserve 비대칭 merge) · H_012(autopoietic closure — 외생 커플링 전제)
- **key:** `merge_physical_carrier`

## 1. 가설

**국소 관측만으로 계산되는 담체가 존재해, 오라클의 물리 이득(총 supply ↑ · overload 불변)에 도달한다.**

담체는 유닛이 **자기 자신에 대해 관측 가능한 양**(`L_i, cap_i, D_i, Λ_i, S_i, st_i`)만으로 계산되어야 하고, 오라클 gain의 **1차/2차 근사**여야 한다.

⊥ **Null (반증 · 이것도 정당한 결과):** 오라클 gain이 **국소 관측으로 근사 불가능한 항**(융합 후 부동점의 전역 재배치)에 지배된다 ⇒ **국소 담체는 존재하지 않는다**. 이 경우 재조합 대수의 물리 이득은 **전역 지식을 요구**하며, 그것이 H_054/H_203의 최종 답이다.

## 2. 기질 수식 (5차 run.py · 이게 전부)

```
L_i = Σ_{s∈i} d_s                          # load(질량)
Λ_i = Σ_{s∈i} d_s·f_s / L_i                # 취약도(질량가중 평균) — 융합이 희석한다
S_i = eq_supply(cap_i, D_i, L_i, Λ_i):     # 평형 supply
    ψ = 1 − exp(−repair)
    HET(되먹임 X):  φ = 1 − exp(−Λ/G);  S = cap·ψ/(φ+ψ)
    LIVE(되먹임 O): 8회 부동점 —
        st = L/S;  rate = Λ·(1 + B1·clip(st−1, 0, EXC));  φ = 1−exp(−rate/G);  S = cap·ψ/(φ+ψ)
융합: 질량보존 · Λ_ij = (L_i Λ_i + L_j Λ_j)/(L_i+L_j)  ← 희석
오라클: gain(i,j) = min(L_ij, S_eq(cap_ij, D_ij, L_ij, Λ_ij)) − min(L_i,S_i) − min(L_j,S_j)
        (= 부동점 8회 반복을 통째로 시뮬레이션 · 모델 전체 지식)
```

**HET에선 오라클조차 물리를 못 움직인다** = 파티션이 총 물리자원을 못 바꾸는 대수적 사실 ⇒ **되먹임(stress → 손상률 증폭)이 있어야 물리 채널이 열린다.** 따라서 후보 담체도 **HET에선 이득 0이어야 정합적**이다(그게 옳은 예측).

## 3. 담체 후보의 필수 요건 (하나라도 어기면 그 후보는 사전 탈락)

1. **국소성** — 유닛 자기 관측량만. 융합 후 부동점 재계산 금지(그건 오라클).
2. **부호-불변** — repair · σ(격리강도) · capsplit 규약 · ρ(부하) · frag_sigma · 기질(HET/LIVE) 전 축에서 부호 보존. **PASS 조건에 내장**(사후 체리픽 금지 · 이전 실패의 진범).
3. **장부 항등식 아닐 것** — 순간 ΔATP(`a_detgrad`)와 **선형독립**. capture(순간-argmax 일치율)가 높으면 그건 또 장부다. **capture를 실측해 보고**하고 `V_detector_collinear` > 0.90이면 항등식으로 해석.
4. **되먹임 의존성** — HET 이득 0 · LIVE에서만 양성(오라클과 같은 패턴).

## 4. probe 설계 ($0 numpy · 5차 하네스 재사용)

| arm | 내용 |
|---|---|
| **EXP** | 후보 국소 담체 (Fable 도출 · TOP-1) |
| **c2_blind** | health/신호 blind 무작위 짝짓기 (동일 이벤트 예산) |
| **a5_sham** | **외생 site-field sham**(5차에서 유효성 실증: zratio 3.56 vs blind 1.25 · t=18.8 · corr(Z,slack)=−0.074) — 선택 *형태*는 동일, 신호만 인과무관 ⇒ **"선택 행위 자체"의 이득을 격리** |
| **a_detgrad** | 순간 ΔATP argmax (**장부 기울기 정책** — 이걸 못 이기면 장부 항등식) |
| **o6_oracle** | 전모델 부동점 시뮬 (천장 · control 아님) |
| **a_comp** | slack 극단매칭 (5차 실패 담체 · 음성대조) |

- **DV = supply(= Σ(cap − D)) / overload(stress>1 비율)** — **파티션-불변 물리량**. 🚫 **장부 ATP(Σmin(L,S)) 금지**(항등식만 재발견).
- **도달성 게이트(PHYS_REACHABLE)**: 그 셀에서 `o6_oracle − c2_blind`의 supply Δ가 0이면 **측정 불가 셀**(HET가 그랬다) ⇒ 그 셀은 채점하지 않는다.
- 3게이트 유지: G1 pump ≤1e-9 · G2 self_remerge=0 · G3 live band 선등록. + V_sham_distinct · V_sham_neutral · V_POWER · ORACLE_VALID.
- seed ≥20 paired-CRN · disjoint pilot로 MDE 사전계산 · 코드 sha256 동결.

**PASS(DIRECTIONAL-POSITIVE):** EXP가 `blind` · `sham` · **`a_detgrad`** 셋 다를 supply에서 유의 우세 **AND** overload 악화 없음 **AND** 부호보존 전 축 **AND** capture < 0.90(장부 항등식 아님) ⇒ **재조합 대수가 물리 정보를 더하며, 국소 관측으로 도달 가능하다**(H_054/H_203의 답).
**NULL(사전등록 TOST):** EXP가 오라클의 물리 이득에 도달하지 못하고 blind/sham과 **등가** ⇒ **국소 담체 부재 = 재조합의 물리 이득은 전역 지식을 요구한다**(이것도 licensed 결론).
**KILL:** EXP가 물리를 유의하게 악화(a_comp처럼) ⇒ 그 담체 클래스 사망.

## 5. 계측 규칙 (11종 · ARCHITECTURE `organelle-lane-probe-defects` · convergence `synthesis-md-1`)

순서통계량 detector 금지 · SEM/paired-t만 · MDE를 인과 도달축에서 disjoint pilot로 사전계산 · 정보채널 증명 · V-gate는 헤드라인 그 자체에 · 부호보존 PASS 내장 · 분기 실행가능 · 연산자 자원보존(ops ≤1e-13) · **사후 detector/판정변수 교체 금지(sha256 동결 + disjoint seed)** · **음성은 사전등록 TOST로** · **헤드라인 DV가 처치의 최적화 대상과 항등식이 아닐 것(장부형 DV 금지)**.

engine-native 0 → 통과해도 상한 **DIRECTIONAL**(cement엔 303M py-channel).
