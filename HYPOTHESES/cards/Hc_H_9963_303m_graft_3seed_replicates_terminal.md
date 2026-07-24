# H_9963 · 303M GRAFT 3-seed 복제: rotation-null 지배가 3/3 재현 — H_9943 을 full-TERMINAL 로 박제

**한 줄:** H_9943(303M engine-native GRAFT · rotation-null z=+774 · 1-seed=DIRECTIONAL)을 seed 2·3 으로
동일 파라미터 재학습+재측정하니, **rotation-null z 가 3/3 강하게 재현**(seed1 +774 / seed2 +917 / seed3
+762 · 전부 PASS>q99)·MI lift 도 일관(+0.19/+0.18/+0.18)·parity 동일(2.766e-05). ⟹ z=+774 는 seed 우연이
아니며, GRAFT 결합이 anima 자기 303M substrate 서 실재하는 강한 상태방향을 학습한다는 결론이
**full-TERMINAL** 로 굳는다(프런티어 cement=engine-native anima-py · toy H_9937 도 3-seed 였음).

- 계기: `anima-py graft fit /home/summer/py303_full.clm --carrier-corpus en_general.txt --out
  graft_303m_s{2,3}.clm --steps 200 --n-states 8 --state-gap 13 --ctx 128 --cont-len 64 --carrier-k 4
  --gate-strength 0.1 --seed {2,3}` → `graft check … --rotation-null 64 --k 8 --cont-len 64 --seed {2,3}
  --fluency-corpus en_general.txt` (summer · CPU · 무-GPU · rc=0). engine-native `.clm` (terminal 지점).

## 결과 — 3/3 rotation-null PASS
| seed | parity | MI lift | ROTATION-NULL z (n=64) | fluency FORM dMargin |
|---|---|---|---|---|
| 1 (H_9943) | 2.766e-05 | +0.191 | **+774** PASS(>q99) | +0.049 (form **−6.9%**) |
| 2 | 2.766e-05 | +0.177 | **+917** PASS(>q99) | +0.009 (form **−1.3%**) |
| 3 | 2.766e-05 | +0.181 | **+762** PASS(>q99) | +0.041 (form **−5.7%**) |

- **방향(z) tight 재현**: +762~+917, 전부 displacement-exact null 을 압도(>q99). MI lift +0.177~+0.191 일관.
- **유창성 비용은 seed 변동**: form −1.3%~−6.9%(평균 ~−4.6%). 방향은 굳게 재현되나 언어 훼손 정도는
  seed 마다 다르다 — 정직 기록(`single-retrain-outlier` 반대 방향: 여기선 3/3 이 다 PASS 라 outlier 없음,
  다만 fluency 는 point-estimate 로 인용 금지, 범위로 인용).

## 판정 — 🟢🏁 TERMINAL: 303M GRAFT 결합의 상태방향 학습은 seed-robust (engine-native · 3/3)
- **H_9943 을 DIRECTIONAL → full-TERMINAL 로 승격**: 프런티어의 cement 기준(engine-native anima-py · 실제
  303M)을 3-seed 복제로 충족. rotation-null(norm·Gram·평균·변위 보존, 방향만 파괴)을 3/3 넘는다는 것은
  진폭/변위 artifact 가 아니라 학습된 **방향**의 재현 가능한 실재.
- **이 세션 GRAFT 결론의 박제된 코어**: LANE-BUS 사망(V6_38/39) 후, GRAFT 가 anima 자기 substrate 서
  강한 통제결합을 학습함이 terminal 로 확정. 부속(방향 진폭-불변 H_9958 · λ 이득영역 H_9948 · 7B priced-out
  H_9940)은 DIRECTIONAL 로 이 코어를 둘러싼다.

## 정직 경계
1. **fluency 는 seed 변동**(−1.3%~−6.9%) — "상태정보가 언어를 흔든다"는 방향은 확실하나 그 크기는 범위로만.
   비용의 seed-변동 자체가 다음 질문(무엇이 그 변동을 결정하나).
2. TERMINAL 은 **이 결합의 상태방향-학습**에 대한 것이지 "그 상태가 의식/agency"라는 주장이 아니다(p9).
   C-state=PureField 원시 16-D 의 정렬이 실재·강함·재현됨까지가 박제된 것.
3. 계기·carrier(en_general 자연문)·303M(byte-LM) scope. gate_strength 0.1 · λ=1 · cont-len 64.

## 다음
① fit-time gate_strength 재학습 스윕(H_9958 의 check-time 프록시 검증). ② λ×gate_strength 2D 이득-비용
   지도(H_9948·H_9958·병렬 H_9950 합류). ③ fluency seed-변동의 원인. 산출: `~/.fire-recover/graft_303m_3seed/`.
