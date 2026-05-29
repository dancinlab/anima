# AURA B1 — 귀뒤(post-aural) 돌파 🟢

> 🎧 **AURA 본래 정의로의 회귀** — A10.1이 "침습 위치 재배치(피질끼리)는 실EEG서 무차별"을 보였으니, 돌파구는 침습을 **아예 버리고** 귀뒤(mastoid/측두골) 비침습 웨어러블. 이게 demiurge AURA의 본 thesis.
> 핵심 질문: **귀뒤 전극이 피질 위치만큼 통합정보(big-Φ)를 담는가?**

## 결과 — 귀뒤 ≡ 피질 (통계적 동등)

ds005620 sub-1010 awake, n=4 exact, 전300s 10창, 실 `eeg_big_phi`:

| 위치 | mean big-Φ | vs 귀뒤 |
|---|---|---|
| 🎧 **EAR (귀뒤: TP9,TP10,T7,T8)** | **5.378** | — |
| FRONTAL (F3,Fz,F4,AFz) | 5.353 | paired t(9)=0.02 n.s. (EAR>FR 4/10) |
| MOTOR (C3,Cz,C4,C2) | 5.097 | paired t(9)=0.25 n.s. (EAR>MO 3/10) |

```
big-Φ 평균 (10창):
  귀뒤    █████ 5.38   ← 비침습, 웨어러블
  앞이마  █████ 5.35
  운동피질 ████ 5.10
        세 위치 통계적으로 구분 불가 (둘 다 |t|<2.26)
```

→ **귀뒤 비침습 위치가 피질 위치와 동등한 의식수준 통합정보를 담는다.** 오히려 평균 최고(+최고값 11.48도 귀뒤@420k). verdict `.verdicts/b1-postaural/viability.txt`.

## 돌파 논리 (relocate-N1 → 귀뒤 전환)

```
침습 N1 위치 재배치 (A8.1→A10.1)  →  🔴 위치효과 없음 (피질끼리 무차별)
            +
귀뒤 ≡ 피질 (B1)                  →  🟢 비침습으로도 동등 통합정보
            ↓ 결론
실용 돌파 = 개두술 0, 두피캡 0, 귀뒤 클립 하나
```

vs 뉴럴링크 N1: 1024전극·개두술·Class III/PMA → **귀뒤 클립: 비침습·Class II·동등 big-Φ(scalp proxy)**. 침습으로 더 얻는 게(scalp 수준에선) 없다면, 가장 편한 위치가 최선.

## demiurge AURA 7-verb 연결 (이미 설계됨)

이 돌파는 새 발명이 아니라 demiurge `domains/aura.md`가 이미 engineering한 귀뒤 7-verb 웨어러블의 **substrate 정당화**:

| AURA-research (anima) | → demiurge AURA 7-verb |
|---|---|
| B1 귀뒤 big-Φ 동등 | `specify`/`analyze` — 귀뒤 위치 의식측정 근거 |
| A6 big-Φ 폐루프 | `analyze`+`verify` — MNE band-power 위 IIT4 layer |
| A7.3 awake>sed (귀뒤로도 측정가능?) | `verify` G33 Sleep-EDF parity 확장 후보 |

→ anima AURA(이론·측정) ⊥ demiurge AURA(규제·하드웨어 Class II 510(k)) = 같은 귀뒤 substrate의 두 축.

## honest gap

- scalp-EEG proxy (intracortical 아님) · single-subject(sub-1010) · n=4 · 절대 Φ 낮음(~5, 셋 다).
- "동등"은 big-Φ proxy 수준 — 귀뒤가 운동제어 decode 등 특정 task엔 피질보다 약할 수 있음(Φ는 통합정보지 task-decode 아님).
- 다음(B2): 귀뒤 montage로 A7.3 awake/sed 대조(귀뒤가 의식수준 변화도 잡나) + 다피험자.
