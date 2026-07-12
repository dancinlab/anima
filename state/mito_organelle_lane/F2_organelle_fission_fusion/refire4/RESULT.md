# H_9274 / F2 — 4차 발사 결과 · ⚪️ **여전히 INVALID** (sham 통제 4번째 붕괴) + 담체 재정의는 **결정적으로 성공**

- **일시:** 2026-07-12 · $0 numpy · mini CPU-local · OMP=2 · wall 94s · n=20 paired-CRN
- **질문:** 재조합(merge) 대수가 정보를 더하는가 (H_054 · H_203)
- **이번 재설계:** (1) 담체 health → **load-공급 상보성** slack=S−L (오라클의 실현가능 국소근사 a_comp)
  (2) sham 스칼라 tag → **범주 tag(K=5) + 대형모 상속**(평균 금지)
- **판정:** 사전등록 PRIMARY(a_comp) = **INVALID** — 단, 3차와 질적으로 다르다: PRIMARY 부호가
  뒤집혀서가 아니라, **sham 통제(②)가 4번째로 붕괴**해 hard-gate `V_sham_distinct_from_blind` FAIL.
  **담체 재정의 자체는 3차가 지목한 exit 그대로 결정적으로 성공했다** (아래 §1).

---

## 0. 게이트 전수 — sham 하나만 FAIL

| 게이트 | HET | LIVE | 근거 |
|---|---|---|---|
| **G1** 대수중립 pump | ✅ 2.7e-13 | ✅ 2.4e-13 | ≤1e-9 |
| **G2** self-remerge | ✅ 0.000 | ✅ 0.000 | sibling-ban+COOL=2 · guard_off 대조 |
| **G3** live-regime 양쪽 | ✅ h=0.805 atp=57.5 | ✅ h=0.700 atp=48.8 | control만 보고 선등록 repair=0.12 |
| **POWER** span>3×MDE | ✅ 6.99× | ✅ 5.68× | pilot 900–919 disjoint · 사후 span 미사용 |
| **ORACLE** 도달범위 | ✅ +13.43 (p=1e-15) | ✅ +13.06 (p=4e-15) | 3차 +13 재현 |
| **comp 정보채널**(④) | ✅ slack_sel_ratio 3.70 | ✅ 3.64 | 선택쌍 slack-gap이 pop-std의 3.6×(var>0) |
| **tag ⊥ slack**(④) | ✅ corr +0.001 | ✅ +0.001 | sham 축이 담체와 무관 |
| **sham distinct-from-blind** | 🔴 **FAIL** tag_gap 0.000 | 🔴 **FAIL** 0.000 | ↓ §2 |

⇒ 3게이트+검정력+오라클+comp-정보채널+tag⊥slack **전수 통과**. 유일 실패 = sham distinctness.

---

## 1. ✅✅ 담체 재정의 성공 — a_comp(load-상보성)가 **전 자유축에서 부호안정 +13** (health가 뒤집힌 바로 그 곳에서)

깨끗한 통제 **c2_blind** 대비 a_comp 부호를 **sign-sweep 전 점**에서:

| 축 | HET a_comp−c2 mean-range | LIVE a_comp−c2 mean-range | 부호 |
|---|---|---|---|
| **repair**(live band 전 구간) | [ +8.74 .. +14.87 ] | [ **+1.99** .. +16.06 ] | ✅ 전부 + |
| sigma{0,.5,1} | [ +11.12 .. +14.17 ] | [ +11.14 .. +14.07 ] | ✅ + |
| capsplit{sym,load} | [ +2.61 .. +13.69 ] | [ +4.41 .. +13.92 ] | ✅ + |
| rho{.7,.85,1} | [ +10.21 .. +14.64 ] | [ +8.04 .. +17.29 ] | ✅ + |
| frag_sigma{.5,.9} | [ +11.79 .. +14.59 ] | [ +10.78 .. +14.74 ] | ✅ + |
| EXC{1,2,6}·B1{1.5,3} [LIVE] | — | [ +11.85 .. +14.82 ] | ✅ + |

- **SIGN_ALL_POS = True · 양 기질 · 모든 점 (signs = {1}, 단 한 점도 음수/영점 없음).**
- **대조(3차 health a3, 같은 repair 축):** HET −2.78→+4.73 · LIVE −2.93→+8.14 = **살아있는 band 안에서 0을 지남.**
  → 3차가 "담체=health 아니라 load-상보성 + 부호-불변 정책 차원에서만 유효"라고 특정한 **바로 그 exit이
  실증됐다.** slack은 L을 직접 포함하므로 부호가 기질(되먹임 on/off)에 묶이지 않는다 (사전예측 적중).
- **정량:** a_comp vs c2_blind = HET **+13.69±0.51 (t=26.96, p=1.3e-16, 20/20)** · LIVE **+13.92±0.48 (t=29.07, p=3.2e-17, 20/20)**.
- **오라클 상한 도달:** a_comp atp 71.15 ≈ o6_oracle 70.89 (HET) · 62.75 ≈ 61.89 (LIVE) —
  **국소관측(L,S)만 쓰는 모델-free myopic 정책이 전상태·전모델 오라클 천장에 붙었다.** health 정책(o_health)은
  59.2/50.2로 blind(57.5/48.8) 근처.
- health-불변 확인: a_comp health(0.805/0.695) ≈ blind(0.805/0.700) — 이김은 health가 아니라 min(L,S) 상보성.

⇒ **"재조합 대수가 정보를 더하는가"의 답은 이 담체에서 YES이고, 그 정보는 부호-불변이며 국소 도달가능하다.**

---

## 2. 🔴 그런데 sham 통제가 **4번째로** 붕괴했다 (이번엔 범주 tag 동질화)

- 2차 sham: 균등순열 = blind와 분포동일. 3차 sham: 스칼라 tag가 cap-가중 평균으로 0.492≈0.5 수렴.
- **4차 sham: 범주 tag(K=5) + 대형모 상속.** 보존적 융합이 매번 큰-cap 부모 tag를 흡수 → warm 150스텝×2융합
  동안 **tag 다양성이 단일값으로 붕괴** → 선택 시점 min-tag == max-tag → **선택쌍 |Δtag| = 0.000**(blind 0.002)
  → 극단매칭 기계가 **저-index 결정적 picker로 퇴화** (3차와 동일 종착).
- 그래도 sham은 blind를 **+1.9(HET)/+2.1(LIVE)** 이긴다 = "지속 구조화 매칭 자체"의 순수-구조 이득 ~+2.
  ⇒ a_comp−sham = **+11.79(HET)/+11.85(LIVE)** (20/20, 전 축 부호+)이 **정보-격리분**이고, ~+2는 구조분.
- **판정 영향:** sham−blind tag_gap이 임계(>0.30) 미달 = sham을 blind와 **분포적으로 구별 못 함** →
  hard-gate FAIL → 사전등록상 INVALID. (사후에 gate를 풀면 F8/F13 진범 = 금지. 그대로 INVALID.)

**메타 진단 (4차 수렴):** **보존적(질량보존) 융합은 유닛에 실린 어떤 상속 신호든 동질화한다** — 스칼라는
평균으로, 범주는 대형모 흡수로. ⇒ "같은-기계·무정보·지속·blind-구별" sham은 **유닛-상속 tag로는 구축 불가**.
다음 발사 조건: sham을 **유닛 밖 외생 relabel 스트림**(융합에 상속되지 않는 매-스텝 재배정 라벨)으로 두거나,
c2_blind + 오라클-상한(sham−blind≤+2 bound)만으로 격리를 인정.

---

## 3. ✅ 부수 확정 — 융합 규약 자유도 0 (3차 재현)

`unweighted-mean merge`(G1 위반)로 바꾸면 순간 pump/run = a_comp **+48.4**(보존적 ~1e-13) ⇒
G1(총 supply EXACT 보존)이 merge 순간 D←D_a+D_b를 유일해로 강제. 융합 규약 축 자유도 없음 확정.

---

## 4. 무엇이 지금 답을 막는가 (핵심 특정 · 한 칸 더 이동)

프레임 유효 + 담체 재정의 성공 + PRIMARY 부호안정 +13. **남은 유일한 결함 = sham 통제의 구축 불가능성**.
- 3차: PRIMARY(health)가 부호 뒤집힘 = 담체 문제 (해결됨).
- 4차: PRIMARY(a_comp) 부호안정 성공, 그러나 sham이 붕괴 = **통제 문제**로 결함이 한 칸 이동.
- a_comp의 +13.7(vs 깨끗한 blind, 전 축 부호안정, 오라클 도달)은 **licensed DIRECTIONAL-POSITIVE 물증**이나,
  사전등록 헤드라인이 "vs sham distinct"를 hard-gate로 못박았고 그게 FAIL이므로 **형식적으로 INVALID**.

⇒ **답:** 담체를 load-상보성으로 재정의하니 재조합 대수가 **부호-불변·국소도달·오라클급(+13) 정보**를 나른다는
것이 깨끗한 blind 통제 대비 결정적으로 나타났다(3차 exit 실증). 단, 이 정보에서 "지속 구조화 매칭 아티팩트"를
분리하는 sham 통제가 보존적 융합의 신호 동질화로 4번째 붕괴 ⇒ 사전등록상 미채점(INVALID). PASS까지 **딱
sham 하나 남았다** — 그리고 그 sham은 유닛-상속으로는 불가함이 확정됐다.

---

## 5. 재발사 조건 (다음 발사 전 사전등록)
1. **sham을 유닛-상속 tag에서 분리** — 융합에 실려 동질화되지 않는 **외생 relabel 스트림**(매 융합 이벤트 전
   무관 라벨을 유닛에 재배정, 상태 무관·지속 시드 고정)으로 "같은-기계·무정보·지속·blind-구별" 4조건 동시충족.
   또는 sham을 폐기하고 c2_blind + sham−blind≤+2 상한(구조분 bound)으로 격리 인정을 사전등록.
2. a_comp(담체) · 부호보존 설계는 그대로 유지 — 이번에 통과. 재튜닝 금지.
3. engine-native 0(toy numpy) ⇒ 통과해도 상한 DIRECTIONAL. cement엔 303M py-channel 필요.

### 재현
- `run.py` — HET/LIVE 두 기질 · 7 arm · sweep 5~7축 · G1~G3+오라클+comp정보채널+sham distinct 게이트
- `result.json` — 전 수치. `verdict.{HET,LIVE}.sign_detail` = a_comp 축별 부호표(전부 +).
- `run.log` — 콘솔. `run.err` — stderr.
