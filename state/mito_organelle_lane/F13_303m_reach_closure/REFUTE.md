# H_9285 적대적 재검증 (REFUTE) — verdict=INVALID 반박

**결론: 반박됨(refuted=true). 원 verdict `INVALID`(lane KILL 유보)는 자초한 order-statistic 헤드라인이
만든 인공물이며, 실 데이터는 검출력 있는 정당한 NEGATIVE = `KILL`(reach-lever 가설 종결)이다.**

계측 규칙(max-control 금지·SEM/paired-t·사전 MDE·정보채널·V-gate) 자체는 대체로 잘 지켜졌다.
그러나 **금지 지표의 정신(순서통계량이 하향편향을 기계적으로 만든다)이 헤드라인 detector 정의 안으로
이전(relocate)되어** verdict를 뒤집었다.

---

## 1. 치명타 — 헤드라인 `m_conj = min(m_A_conj, m_B_conj)` 자체가 order statistic

규칙 1은 `Δ = exp − max(controls)`를 금지한다(최댓값 순서통계량이 편향을 만들기 때문). 저자는
control 축에서는 이를 지켰다(control별 paired-t 전부 보고 O). **그러나 헤드라인 detector를
두 branch의 `min()`으로 정의**했다 — 같은 순서통계량 죄를 detector 축으로 옮긴 것이다.

재계산(item-level, n=120):
- c0: mean(m_A)=+0.009, mean(m_B)=+1.083, **mean(min)=−0.422**.
  → min이 낮은 branch 평균보다 **0.431 아래**에 앉는다(per-item sd: mA=2.00, mB=2.71).
- 즉 헤드라인의 음수(−0.42)와 "죽음"은 처치 효과가 아니라 **noisy 두 변수의 min이 만드는 하향편향**이다.
  처치 delta는 ~0.08 규모인데 order-statistic 편향이 −0.43 — 헤드라인은 편향에 지배된다.

## 2. "channel-visibility V-gate FAIL"은 detector 맹목이 아니라 min() 인공물

같은 두 branch를 다른 aggregator로 보면 처치 채널(SHOCK=router 파괴)이 **명확히 보인다**:

| aggregator | SHOCK−c0 Δ±SEM | t | 판정 |
|---|---|---|---|
| m_conj = **min()** (헤드라인) | +0.011 ± 0.035 | +0.32 | "안 보임" |
| m_mean (같은 두 branch) | +0.066 ± 0.034 | +1.93 | 경계 |
| m_B_conj (live branch) | **+0.100 ± 0.040** | **+2.48** | **p_t19=0.023** |

⇒ detector는 처치 채널을 **p<0.05로 본다**. min()을 통과시킬 때만 사라진다.
"router를 완전 파괴해도 헤드라인이 안 움직인다 ⇒ INVALID"는 **잘못된 진단**이다 —
헤드라인이 스스로 눈을 감은 것(min이 죽은 branch를 67.5% 집는다)이지, 채널이 안 보이는 게 아니다.
V-gate(규칙 5)는 "헤드라인 그 자체"에 걸렸지만, **그 헤드라인이 order-statistic이라 게이트 출력이
{PASS,INVALID}로 붕괴**했다 — 규칙 5가 막으려던 바로 그 실패 모드다.

## 3. 검출력은 실재했고, 실 데이터는 검출력 있는 NEGATIVE

- live branch m_B_conj: c0=+1.083 (t=+4.69), MDE 0.190 ≪ 1.083 ⇒ 검출력 O.
- 그 위에서 **모든 capacity 처치가 열화** — EXP−c0 = −0.209 (t=−2.30, **p_t19=0.033**),
  c1_k2−c0 = −0.142 (t=−3.20, p_t19=0.005). EXP가 최악이고 **자기 시간축 셔플(c2)도 못 이긴다**
  ⇒ schedule 정렬에 정보 0.
- router 파괴(SHOCK)가 오히려 **개선**(+0.100, t=+2.48) ⇒ 학습된 MoE mixing은 read-side 축이 아니다.
- 방향 전수 음성. EXP > control은 20개 비교 중 6개(전부 약한 상수 arm 대비 dacc, |t|<2.7·금지지표).
  **숨은 양성 없음** ⇒ THEATER/DIRECTIONAL-POSITIVE 아님.

이것은 카드가 사전등록한 FAIL 시나리오(`Δ≈0/음성 ⇒ organelle lane CLOSED`, H_9283 예측 일치)
**바로 그것**이다. 헤드라인을 m_mean이나 m_B_conj로 등록했으면 곧장 검출력 있는 음성 종결이었다.
min() 선택이 "결착"을 "INVALID"로 변환한 유일한 장치다.

## 4. 반박 체크리스트 적용

1. Δ=max(controls)? — control 축은 아니오(양호). **그러나 헤드라인=min()=order statistic → 정신 위반. INVALID의 근거는 이 인공물.**
2. MDE<동적범위? — 표면상 O(0.17≪4.448). 단 4.448은 per-position **치팅 oracle**(타깃에 k를 맞춤)이라 상한이 부풀려짐. 현실 작동범위(m_B_conj 처치효과 ~0.21)에서도 검출력은 충분했고 실제로 음성을 p=0.03으로 검출했다 → 검출력 0 아님, 결론에 유리하지 않게 작용.
3. 항진적 arm? — 아니오. k_t=f(router mass), Var(k_t)=0.196 실측. 양호.
4. c1(best constant)=grid 최선? — O. k1/k2/k3 전수, k3=c0 dense 선택. 양호.
5. 양성이 tunable FORM? — 양성 자체가 없음. EXP≈0.733·k1+0.267·k2 선형보간(resid −0.06) — schedule에 구조적 정보 없음 재확인.
6. seed 부족? — n=20 blocks paired-CRN. 순서통계량 인공물은 seed가 아니라 **detector 정의(min)**에서 발생.
7. 인프라 벽을 verdict로? — 아니오. parity=0, wall 2941s 정상완주. BLOCKED 아님.

## 5. 정직한 verdict

- 원 `INVALID`는 **엄격 pre-registration 규율 하에서는 방어 가능**(등록 헤드라인이 해석불가하면 tier
  cement 금지)하나, **그 해석불가성의 원인이 저자가 고른 order-statistic 헤드라인 자체**다. 이는
  census가 경계한 결함 클래스의 재발이며 "측정 못 함"이 아니라 "측정 도구를 스스로 무디게 함"이다.
- lane 관련 실제 질문(배분이 held-out reach를 올리는가)은 **live·검출력 있는 채널에서 명확히 답**됐다:
  올리기는커녕 열화·schedule 무정보·router 파괴가 개선. = 사전등록 FAIL = **KILL(lane 종결)**.
- 부수 substrate 사실(distal cue 채널 죽음, m_A_conj≈0)은 진짜지만 arm-무관이며, 그것이 뜻하는 바는
  "2-cue conjunction 헤드라인이 애초 doomed"였다는 것 — INVALID의 근거가 아니라 **헤드라인 설계 오류의
  근거**다.

**⟹ refuted=true · 올바른 판정 = KILL** (INVALID는 order-statistic 헤드라인이 만든 오라벨).
