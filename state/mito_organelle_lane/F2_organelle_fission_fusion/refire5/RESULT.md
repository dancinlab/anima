# H_9274 / F2 — 5차 발사 결과 · ⚪️ **INVALID (사전등록 분기 · 물리 DV 결론불가)** + **sham 결함 해결(최초)**

- 2026-07-12 · $0 numpy · mini CPU-local · OMP=2 · wall **79s** · n=20 paired-CRN
- prereg sha256 `3b910ee0e60feb43950b66a78c8beac4d918062411305f577ff882f66f935cba` (실행 전 동결 · PREREG.md)
- seed main 200–219 · pilot 950–969 = 4차와 **DISJOINT**(규칙⑨). 4차 run.py 기질 그대로, sham·통제·DV만 재설계.

## 1. ✅ sham 수리 성공 — 융합-불변 담체 + 분포적 sham≠blind 실증 (5발 만에 최초)

**설계:** 유닛에 신호를 실으면 보존적 융합이 반드시 동질화한다(4차 메타진단) ⇒ 신호를 유닛에서 빼서
**외생 site-field**로: init 시 site별 `z_s ~ N(0,1)` 동결(d·f·cap 과 독립, 상속/갱신 없음), 유닛 점수
`Z_i = Σ_{s∈i} d_s z_s / L_i` 를 **매 이벤트 재계산**(유닛 상태 저장 0). Z는 L·S 와 **같은 대수 class**
(질량가중 site 집계)라 융합·분열을 견딘다. sham = a_comp 와 **동일 극단매칭 기계**(min-Z × max-Z),
신호만 인과무관.

| 실측 | HET | LIVE |
|---|---|---|
| zratio(=E‖ΔZ_sel‖/std Z) **sham** | **3.56** | **3.56** |
| zratio **blind** | 1.25 | 1.25 |
| sham−blind zgap paired-t | **t=18.8 · p=9.4e-14 · 20/20** | 동일 |
| corr(Z, slack) 중립성 | −0.074 | −0.073 |
| **V_sham_distinct_from_blind** | ✅ **PASS** | ✅ **PASS** |

⇒ sham은 blind와 **분포적으로 다르고**(같은 극단짝짓기 구조를 지속 수행), **담체와는 무관**하다.
3·4차에서 붕괴한 tag(스칼라·범주)와 달리 융합 평균에 살아남았다.

**격리 결과(sham의 존재 이유):** `sham − blind` ATP = **+1.18 (p=0.20, ns)** HET · **−0.07 (p=0.93, ns)** LIVE
⇒ **"선택 행위 자체(융합 횟수·극단 짝짓기 구조)"의 이득 ≈ 0.** 따라서 a_comp의 +12.8은 **구조가 아니라
신호**에서 온다 — 4차가 못 한 격리가 licensed로 성립.

## 2. 게이트 전수 (양 기질) — 5발 만에 hard 게이트 ALL PASS

G1 pump ≤1e-9 (2.7e-13/3.4e-13) ✅ · G2 self_remerge=0 ✅(guard_off 대조 작동) · G3 live band 선등록
(repair=0.12 · c2_health 0.798/0.683) ✅ · cap 보존·n_units=16 고정 ✅ · comp 정보채널(slack_sel_ratio) ✅ ·
**sham distinct** ✅ · sham 중립 ✅ · POWER(ATP span 5.1×/4.3× MDE, pilot disjoint) ✅ · ORACLE_VALID
(+12.32/+13.24) ✅.

## 3. H-A (장부 DV = ATP = Σmin(L,S)) — 통과, 그러나 이것이 답이 아니다

| | HET | LIVE |
|---|---|---|
| a_comp − c2_blind | **+12.96 ± 0.69** (t=18.9, p=9.3e-14, 20/20) | **+12.81 ± 0.90** (t=14.2, p=1.5e-11, 20/20) |
| a_comp − a5_sham(유효) | **+11.78 ± 0.79** (t=15.0, p=5.7e-12, 20/20) | **+12.87 ± 0.74** (t=17.5, p=3.6e-13, 20/20) |
| 부호보존 전 축(repair·sigma·capsplit·rho·frag_sigma·EXC·B1) | ✅ 전 점 + | ✅ 전 점 + |

4차 +13.7을 **새 disjoint seed에서 재현**. 즉 "a_comp는 blind와 유효한 sham 둘 다를 전 축에서 유의 우세".

**단, REFUTE_v2 R1 통제(a_detgrad = 순간 ΔATP argmax)를 넣자 그 의미가 바뀐다:**
- a_comp의 순간 ΔATP **capture = 0.982 / 0.978** (획득가능 최대의 98%) · argmax 정확일치 0.65/0.56
- `a_comp − a_detgrad` ATP = **−0.50 (p=0.29)** HET · **−1.54 (p=0.011)** LIVE — a_comp는 detgrad를
  **못 이긴다**(LIVE는 유의하게 진다). ⇒ a_comp는 사실상 **헤드라인의 기울기를 타는 정책**이다.

## 4. 🔴 H-B (파티션-불변 물리 DV) — 이득 없음 / 악화. 사전등록상 **INVALID**

| 물리 DV | HET | LIVE |
|---|---|---|
| supply Δ vs blind | −0.26 ± 0.34 (p=0.46) · **부호 전 축 음성(32/32 점)** | −1.44 ± 1.29 (p=0.28) · 혼합 |
| TOST(δ=1.0) vs blind | **EQUIVALENT=True** (p=0.021) | False (p=0.63) |
| TOST(δ=1.0) vs sham | False (p=0.29) | False (p=0.57) |
| **overload Δ vs blind** | **+0.051 (p=0.0013) — 유의하게 악화** | **+0.117 (p=2.3e-05) — 유의하게 악화** |

⇒ 장부(+12.9)는 오르는데 **물리 상태는 개선이 0이거나 유의하게 나쁘다.** 사전등록 분기
`H-A ∧ ¬B_POS ∧ ¬B_EQUIV → INVALID` 그대로 적용(HET는 vs-sham TOST 미충족, LIVE는 등가도 미성립) —
사후에 THEATER로 바꾸지 않는다. **실질 방향은 THEATER(장부 항등식)이며 GREEN은 어떤 경로로도 아니다.**

## 5. ★ 신규 결정적 사실 — 물리 채널은 **오라클에게는 열려 있다**

| | supply Δ vs blind | overload Δ vs blind | ATP Δ |
|---|---|---|---|
| **o6_oracle** (전모델) LIVE | **+1.91 (p=0.040)** | −0.001 (ns) | +13.24 |
| **a_comp** (국소 slack) LIVE | −1.44 (ns) | **+0.117 (p=2e-5)** | +12.81 |
| o6_oracle HET | −0.26 (ns · 정책축 span 0.52 < MDE 1.09 ⇒ **HET에선 물리 DV 자체가 도달불가**) | +0.044 | +12.32 |

⇒ **되먹임 있는 기질(LIVE)에서는 재조합 대수가 물리 정보를 더할 수 있다**(오라클이 실제로 총 supply를
올리며 overload를 안 올림 = 존재 증명). 그러나 **국소 slack 담체(a_comp)는 그 채널을 못 탄다** — 같은
장부 이득을 내면서 물리적으로는 더 나빠진다. HET(되먹임 없음)에선 오라클조차 못 움직인다 = 파티션이
총 물리자원을 못 바꾸는 대수적 사실.

## 6. 결론 (정직)

- **sham 물음:** 해결. 융합-불변 외생 site-field sham이 blind와 분포적으로 구별되고(t=18.8) 담체와
  중립(|corr|<0.08)이다. ⇒ merge 물음은 이제 **licensed**하게 물을 수 있다.
- **merge 대수 물음:** 그 licensed 물음의 답은 **"장부에는 YES, 물리에는 NO"** 다. a_comp의 +12.8은
  선택 구조(sham≈0)가 아니라 신호에서 오지만, 그 신호는 헤드라인 Σmin(L,S)의 기울기(capture 0.98)이고
  파티션-불변 물리량엔 이득 0/악화다. 사전등록 판정 = **INVALID**(물리 DV 결론불가), 실질 = THEATER.
- **다음 발사가 물어야 할 것(레인 재조준):** "국소 관측만으로 오라클의 **물리** 이득(+1.91 supply,
  overload 불변)에 도달하는 담체가 존재하는가" — DV는 supply/overload(장부 ATP 금지), 통제는 blind +
  외생-Z sham + **a_detgrad**(이번 5차에서 유효성 확인). 장부 DV로 되돌아가면 항등식만 재발견한다.

### 재현
- `run.py`(sha 위) · `PREREG.md`(데이터 전 동결) · `result.json`(전 수치·부호표) · `run.log`
