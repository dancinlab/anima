# REFUTE — H_9274 / F2 **3차 발사** 적대적 검증 · 판정: ⚪️ **여전히 INVALID** (확정·독립 재현)

- **검증일:** 2026-07-12 · 적대적 검증자 (코드 직독 + result.json 원수치 재추출 · $0 · CPU-local)
- **대상:** `refire3/run.py` · `refire3/result.json` · `refire3/RESULT.md` (보고 판정 = **INVALID · sign_preserved=false**)
- **재현:** ✅ 보고 수치 전량 bit-level 일치. 수치 조작·은폐 없음. RESULT.md는 sham 3차 붕괴·부호 비불변·toy 스코프를 스스로 공시했다.
- **결론:** **판정을 뒤집을 수 없다. 이번엔 프레임이 실제로 유효해졌고, INVALID는 정직하고 강건한 음성이다.** 1·2차 REFUTE가 지목한 진범(무-창조 펌프·사망레짐·사후 span·오라클 패배)이 코드로 전부 제거됐고, 남은 실패(sham 3차 붕괴 + health 부호 비불변)는 **깨끗한 통제만으로도·살아있는 구간 안에서도 재현**된다. 채점 불가 = INVALID.

---

## 0. 1·2차 REFUTE 지적이 실제로 고쳐졌나 — 코드+수치로 전수 확인

| 원 INVALID 결함 | 수정 | 검증자 확인 (독립 재추출) |
|---|---|---|
| 무에서 supply 창조 = 회계착시 (1차) | ✅ 대수 EXACT 중립 | `_fusion` conservative: `cap[lo]+=cap[hi]; Dm[lo]+=Dm[hi]` ⇒ `created=(cap[lo]−Dm[lo])−sup_before ≡ 0`. **pump_max 전 arm ≤2.7e-13** (양 기질). `_fission`도 ca+cb=C·Da+Db=Dv ⇒ created≡0. **checklist #1(ops_supply_created) 통과 — 양성이 회계착시가 아니다.** |
| G1 위반 규약이 펌프 부활 | ✅ 자유도 0 실증 | D1 진단(unweighted-mean merge): pump/run **a3 +265.5 · a3b +100.0** vs conservative ~1e-13 ⇒ G1이 `D←D_a+D_b`를 유일해로 강제. 규칙⑥의 "융합규약축"은 실제로 자유도 없음 |
| 사망레짐(2차 c2_health 0.085) | ✅ | c2_health **0.805(HET)/0.700(LIVE)**·atp 57/49. G3 양쪽(하단 붕괴+상단 포화) 차단. 2차 병리 제거 |
| 사후 span 치환(2차) | ✅ | pilot seed 900–919 (분석 0–19와 **disjoint**), 처치 도달축(정책축) span, 코드에 abort 박음(`if not ok: abort.append`). span/MDE **8.22/5.91 >3** |
| 오라클이 blind에 짐(2차 −0.58) | ✅ | 오라클을 myopic-greedy→steady-state 예측(`_eq_supply` 8-iter)으로 교체 ⇒ o6−c2 **+13.43/+13.06** (p~1e-15) |

⇒ **1·2차 지적은 전부 반영됐다.** 그래서 남은 건 새 은폐가 아니라 **정직하게 공시된 두 구조 결함**이며, 그게 채점을 막는다.

---

## 1. ✅ INVALID는 실행가능 코드로 강제된다 (checklist #7) — 서사가 아니다

`run.py:687-700` 판정 분기:
```
hard = all(gt[k] for k in (...,"V_sham_distinct_from_blind",...))   # ← 이게 False
if not hard: vd="INVALID"          # sig/neg·부호와 무관하게 즉시 INVALID
elif sig and sok_pos: "DIRECTIONAL-POSITIVE"
elif neg and sok_neg: "KILL"       # 도달불가 (hard=False라 진입 못함)
```
`V_sham_distinct_from_blind = |tagpick_sham − 0.5|>0.05` → sham_tp=**0.492** ⇒ False ⇒ **hard=False ⇒ 4/4 arm 모두 INVALID**. PASS/KILL 분기는 도달 불가. **KILL 분기가 실행가능한지(#7)의 반대 방향도 확인: 이번엔 INVALID 분기가 실제로 실행돼 나온 값이지 문구가 아니다.**

---

## 2. 🔴 진짜 실패 ①: sham 통제가 **3번째로**, 또 다른 기전으로 붕괴 (실효 통제 2개)

- 1차 sham: FUSION=`AND`(카드 부정) · 2차 sham: 균등순열 argsort ≡ blind 분포동일 · **3차 sham: 질량보존 융합이 frozen tag를 평균으로 죽임**(`tag[lo]=(clo·tag[lo]+chi·tag[hi])/(clo+chi)`, run.py:363) → 측정창서 tag→~0.5 수렴 → argsort 퇴화 → tagpick **0.492≈0.5**.
- 실측: sham_tp 0.492 / blind_tp 0.537 (둘 다 |·−0.5|≈0 = 무구별). `V_sham_distinct_from_blind=False` 양 기질.
- ⇒ 헤드라인 대비 `a3 vs sham`(−3.05/−3.27)은 **오염**. 깨끗한 통제는 c2_blind 하나. **"aware가 blind를 이김"에서 'health 정보'와 '임의의 지속 타깃팅'을 분리할 유효 sham이 이 레인엔 아직 없다.** 질량보존 merge가 어떤 스칼라 신호든 평균으로 죽이는 게 구조적 원인 — 정직하게 공시됨(§2 RESULT.md).

## 3. 🔴 진짜 실패 ②: health 부호 비불변 — **깨끗한 통제만·살아있는 점만으로도 재현**

원수치 재추출(a3 vs **c2_blind만**, sham 배제):

| repair | 0.03 | 0.05 | 0.08 | 0.12(등록) | 0.20 | 0.30 |
|---|---|---|---|---|---|---|
| HET Δ (c2_h) | −2.78(.53) | −0.61(.65) | **+0.14(.74)** | +1.75(.81) | +3.49(.87) | +4.73(.90) |
| LIVE Δ (c2_h) | −2.93(.30†) | −3.78(.46†) | −1.20(.60) | **+1.34(.70)** | +5.70(.80) | +8.14(.85) |

†=LIVE 기질서 c2_health<0.5 = 사망(band는 HET로 등록됨). **하지만 LIVE를 자기 살아있는 점(h>0.5: 0.08→0.30)만 봐도 부호가 −1.20→+1.34로 교차** — band 차용 아티팩트 아님. HET도 전점 h>0.5, 0.05↔0.08서 교차. ⇒ **checklist #3(도달축·live) 통과한 위에서 부호가 죽는다.**

추가 자유축(a3 vs c2_blind)도 뒤집힘: HET capsplit sym +1.75/load −0.25 · LIVE rho 0.7 +4.98/1.0 −0.25 · LIVE frag_sigma 0.5 +1.10/0.9 −0.10. **규칙⑥: 부호를 뒤집는 자유축이 repair·capsplit·rho·frag_sigma·기질(feedback on/off) 다수 = 결과가 아니라 좌표 = INVALID.** 2차의 "영점 위 헤드라인"은 아티팩트가 아니라 **내재 법칙**임이 확정됨(상수 이동으로 못 고침).

---

## 4. ⚠️ 내가 추가로 깎는 것 — "오라클 +13 licensed 양성"은 거의 항진적 계측기다

- o6 선택기준 = `gain = fm − f0` = **정상상태 ATP 예측 최대화** = 헤드라인 detector(창평균 ATP)를 **직접 최적화**. ATP를 최대화하도록 짠 오라클이 랜덤을 +13 이기는 건 "모델에 착취가능 구조가 있다"는 준-동어반복이지 **"재조합이 정보를 더한다"의 생물학적 증거가 아니다.** (2차 오라클이 진 유일 이유는 myopic이었고, 3차는 steady-state 예측으로 그 버그만 고친 것 = 발견이 아니라 계측기 수리.)
- ORACLE-VALID 게이트는 구조가 조금이라도 있으면 **실패할 수 없는** 약한 게이트다. 통과는 가설에 대해 아무것도 증명하지 않는다 — degeneracy 배제용으로만 유효.
- **단, RESULT.md는 이걸 이미 강하게 hedge했다:** 담체=load-공급 상보성(health 아님)·실현가능 정책 없음·engine-native 0(toy numpy)⇒ 통과해도 **DIRECTIONAL 상한**. 그래서 over-reach가 티어를 못 올린다. **오라클은 "부호안정 licensed 양성"이 아니라 "축이 degenerate 아님"의 계측기로만 읽어야 한다.**

---

## 5. 체크리스트 판정

| # | 항목 | 판정 |
|---|---|---|
| 1 | 3게이트 코드 통과 · supply 무창조 | ✅ pump≤2.7e-13(회계착시 아님)·G2 self_remerge=0·G3 h0.81/0.70·V_cap·n_units 전부 코드 확인 |
| 2 | 부호 자유축 전부 열거? 잔여 자유상수? | 🔴 **뒤집힘 다수**(repair·capsplit·rho·frag_sigma·기질). 미스윕 상수(S·N0·G·K_EV·NOISE_K·drift…) 잔존하나 **이미 뒤집혔으므로 INVALID만 강화** |
| 3 | MDE disjoint pilot · 사후 span 無 · 도달축 | ✅ pilot 900–919(disjoint)·정책축 span·abort 코드·8.22/5.91×MDE. 2차 사후치환 제거됨 |
| 4 | live-regime (c2 health>0.5) | ✅ 0.805/0.700 (2차 사망 0.085 제거). †LIVE 저repair 점은 죽지만 그건 부호교차를 **강화** |
| 5 | sham ≠ blind 분포 구별 | 🔴 **FAIL(3차 붕괴)** tagpick 0.492·blind 0.537 = 무구별. 실효 통제 2개 |
| 6 | Δ = max(controls)? | ✅ 미사용 — `contrasts()`가 control별 `paired()` 전부 + `_pooled_mean` |
| 7 | KILL/PASS 분기 실행가능? | ✅ INVALID 분기가 hard=False로 실제 실행돼 나온 값(서사 아님). PASS/KILL은 도달불가 |
| — | tune-to-green/red | ✅ 흔적 0 — 상수·seed·규약·PASS식 실행 전 고정, 자기 PASS=false 정직 보고 |
| — | p5 | ✅ emit/silence 경로 부재 (구조 레인) |

---

## 6. 최종 판정 — ⚪️ **여전히 INVALID** (`still_invalid=true` · `refuted=false`)

- **판정을 뒤집지 못했다.** 이건 실패가 아니라 확정이다: 보고 verdict(INVALID)를 독립 재추출로 **재현·강화**했다. 앞선 두 REFUTE가 scoreable verdict(KILL·THEATER)를 INVALID로 강등한 것과 달리, **이번 보고 verdict는 이미 INVALID = 강등할 scoreable 주장이 없다.**
- **프레임 개선은 진짜다.** G1 무-창조 실증·live 레짐·disjoint pilot·오라클 reach — 1·2차 진범 4종을 코드로 제거. 이제 실패는 measurement-point가 아니라 **담체(carrier) 구조**에 있다.
- **채점 불가 확정 이유 2건 (독립 재현):** ① sham 통제 3차 구조붕괴(질량보존 merge가 스칼라 신호 평균사) → 유효 sham 부재 → 정보 vs 지속타깃팅 분리 불가. ② health 정책 부호가 **깨끗한 통제만·살아있는 점만으로도** repair·capsplit·rho·frag_sigma·기질에서 0을 지남 → 결과 아닌 좌표.
- **유일 부호안정 신호(오라클 +13)는 detector를 직접 최적화하는 준-동어반복 계측기** — degeneracy 배제용으로만 유효하고, 담체=load-공급 상보성(health 아님)·실현정책 없음·toy numpy(engine-native 0) ⇒ **어떤 티어도 cement 불가**. RESULT.md가 이미 이 스코프를 정직히 달았다.
- **정직성 인정:** sham 3차 붕괴·부호 비불변·toy 스코프를 스스로 공시하고 PASS=false를 그대로 냈다. 데이터 조작 0.

### 다음 발사 전 필수(사전등록)
1. **질량보존 merge를 견디는 sham** — 스칼라 tag 금지(평균사). 범주 라벨+다수결 상속 또는 매 이벤트 재추첨.
2. **담체를 health→load-공급 상보성**으로 재정의하되 **국소관측만 쓰는 실현가능 greedy**로(오라클은 상한이지 정책 아님). 그 정책이 **양 기질·전 live-repair 점 부호안정**으로 blind를 이기는지만 후보.
3. engine-native(303M py-channel) 없이는 통과해도 DIRECTIONAL 상한 — cement 금지.

> 측정 메타법칙(3차 확정): F2의 실패는 매번 **부호를 뒤집는 미등록 자유축**(1차 연산자규약 · 2차 sink상수 · 3차 담체구조) 위에 헤드라인이 얹혀 있던 것. 3차는 그 자유축을 **전 구간 스윕**해 부호교차가 아티팩트가 아니라 health 대리정책의 **내재 성질**임을 확정했다 = health는 부호-불변 담체가 아니다. 답은 health 차원이 아니라 load-상보성 담체 차원에서만 가능.
