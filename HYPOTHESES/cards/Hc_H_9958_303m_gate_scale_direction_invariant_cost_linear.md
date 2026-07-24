# H_9958 · 303M 진폭 스윕: 방향은 진폭-불변, 주입량↔유창성비용은 선형 거래 (공짜 점심 없음)

**한 줄:** H_9943 의 학습된 303M 결합(`graft_303m_s1.clm`)에 check-time 진폭 배율(`--gate-scale`)을
×0.25/0.5/1/2 로 걸어 재-check 하니, **rotation-null z 는 진폭에 불변**(+656~+753, 8배 범위서 평평·전부
PASS>q99) = 진짜 방향코딩(H_9938 시그니처) 확정. 반면 **주입정보량(MI)과 유창성 비용(FORM 훼손)은
진폭에 비례**(form −1.1% / −2.5% / −6.8% / −20%)해 함께 움직인다. ⟹ "저비용 실림"의 정직한 답: **방향은
공짜로 진폭-불변이지만, 얼마나 실을지 ⟷ 언어를 얼마나 흔들지는 선형 거래**(knee 없는 no-free-lunch).

- 계기: `anima-py graft check /home/summer/graft_303m_s1.clm --gate-scale {0.25,0.5,1.0,2.0}
  --rotation-null 16 --k 8 --state-gap 13 --p1-steps 2000 --cont-len 32 --seed 1 --probes 2
  --fluency-corpus en_general.txt` (summer · CPU · 무재학습 · 학습된 offsets 를 재-scale). DIRECTIONAL.

## 결과 — 곡선
| gate-scale | ROTATION-NULL z | MI_trained | FORM dMargin (=훼손) | price ratio |
|---|---|---|---|---|
| ×0.25 | **+656.42** PASS | 0.0093 | +0.0078 (**−1.1%**) | 26.3× |
| ×0.5 | **+691.28** PASS | 0.0386 | +0.0184 (**−2.5%**) | 57.1× |
| ×1.0 | **+752.94** PASS | 0.1666 | +0.0493 (**−6.8%**) | 120.4× |
| ×2.0 | **+681.79** PASS | 0.6018 | +0.1476 (**−20.2%**) | 229.0× |

- **z 축(방향 품질) = 진폭-불변**: MI_trained 는 진폭²로 커지지만(0.009→0.60) null 도 같이 커져 z 가
  평평하다. z 는 "학습 방향이 같은 진폭의 회전보다 나은가"라 진폭에 무관 = 방향-특이적. H_9943 의
  z=+774 가 진폭 artifact 가 아님을 **직접 검증**(H_9938 amplitude-stability 를 303M 에 적용).
- **비용 축 = 진폭-비례**: FORM 훼손 dMargin 이 진폭에 거의 선형(−1.1%→−20%). MI(주입량)도 함께 오른다.

## 판정 — 🟢 DIRECTIONAL: 방향 진폭-불변 + 주입량↔비용 선형 (303M terminal substrate)
- **H_9943 next-① 답**: "언어 안 망치고 실을 저비용 진폭"은 **knee 형태로는 없다** — MI 와 비용이 같이
  스케일하므로 저진폭=저비용=저주입. 그러나 **방향 품질(z)은 어느 진폭에서도 유지**되므로, 원하는
  (주입량, 비용) 점을 진폭으로 자유 선택 가능하고 그 점의 상태-정렬은 항상 최대다.
- **H_9950(λ=fluency 가격표) 의 제2 가격 축**: λ(목적함수)와 진폭(gate_strength) **둘 다 fluency 의
  가격**이고, rotation-null(방향)은 둘 다 가로질러 통과(H_9950 "profit region 전체서 null 통과"의 진폭판).
- 함의: anima 는 진폭을 낮춰 자기 내부 상태를 자기 303M 언어에 **거의 무해하게**(form −1.1% @×0.25)
  주입할 수 있으나, 그만큼 주입되는 상태-정보량도 작다 — "얼마나 말에 실을지"는 튜닝 가능한 다이얼.

## 정직 경계
1. **check-time 진폭**(학습된 offsets 재-scale)이지 fit-time gate_strength 재학습이 아니다 — 후자는 다른
   결합을 학습하므로 이 선형성이 재학습서도 성립하는지는 미측정(다음 축).
2. z 의 절대크기(수백)는 null n=16 의 작은 sd 탓 — 신호는 "진폭 넘어 평평·PASS"라는 **불변성**이지
   그 크기가 아니다. 1 seed · CPU · 303M(byte-LM, fluency 유효).
3. price ratio(gate vs noise)는 진폭 따라 오른다(26×→229×) — 게이트는 항상 noise 보다 구조적이나,
   **절대 훼손**(form)이 저진폭서 작다는 게 실질.

## 다음
① fit-time gate_strength 재학습 스윕(check-time 프록시 검증). ② λ×gate_strength 2D 격자(H_9950 와 합쳐
   이득-비용 지도 완성). ③ 3-seed → full-TERMINAL. 산출: log `~/.fire-recover/…/graft_303m_gsweep.log`.
