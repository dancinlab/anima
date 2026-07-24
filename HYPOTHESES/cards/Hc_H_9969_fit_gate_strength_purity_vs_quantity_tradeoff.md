# H_9969 · fit-time gate_strength 은 방향-순도↔주입-정보량을 맞바꾼다 — check-time 프록시(H_9958)는 불충실

**한 줄:** 303M GRAFT 결합을 gate_strength(주입 진폭) 0.025/0.05/0.1/0.2 로 **각각 재학습**하니, 주입
정보량(MI lift)은 진폭 따라 **단조 증가**(+0.065→+0.108→+0.191→+0.272)하는데 방향 순도(rotation-null
z·trained/null 비율)는 진폭 따라 **단조 감소**(806×→732×→283×→90×). H_9958 의 check-time 재-scale 프록시는
z 를 **평평**하게 봤지만, 재학습은 z 를 **가파르게 떨어뜨린다** ⟹ 프록시는 fit-time 을 대변하지 못한다.
gate_strength 는 순도↔정보량을 맞바꾸는 다이얼이고, gs=0.1(H_9943)은 그 sweet spot(MI>bar, z 강함)이다.

- 계기: `anima-py graft fit /home/summer/py303_full.clm --carrier-corpus en_general.txt --out
  graft_303m_gs{0.025,0.05,0.2}.clm --steps 200 --gate-strength {…} --seed 1` → `graft check …
  --rotation-null 64 --k 8 --cont-len 64 --seed 1 --fluency-corpus en_general.txt` (summer · CPU · rc=0).
  gs=0.1 은 H_9943(graft_303m_s1) 재사용. engine-native `.clm` (terminal-eligible). parity 4/4 = 2.766e-05.

## 결과 — 순도↔정보량 곡선
| fit gate_strength | MI lift (정보량) | rotation-null z | trained/null 비율 | FORM dMargin (훼손) |
|---|---|---|---|---|
| 0.025 | +0.0649 ⛔ **delta 미달(DECORATIVE)** | +3266 | 806× | +0.028 (−4.1%) |
| 0.05 | +0.1080 ✅ | +1531 | 732× | +0.054 (−7.8%) |
| 0.1 (H_9943) | +0.1910 ✅ | +774 | 283× | +0.049 (−6.9%) |
| 0.2 | +0.2719 ✅ | +278 | 90× | +0.048 (−6.9%) |

- **MI(정보량)↑ ⊥ z(순도)↓**: 두 축이 gate_strength 에 대해 단조 반대. 저진폭 학습 = 순도 최상(방향이
  회전-null 을 806× 넘음)이나 절대 정보량은 유용성 바(delta=0.08) 미달 = DECORATIVE. 고진폭 = 정보량
  충분하나 순도 낮음. **z 비율(trained/null)로 봐도 단조** 라 z 크기의 sd-artifact 가 아니다.
- **fluency 는 gate_strength 와 무관하게 ~−4~−8%**(단조 아님) — check-time(H_9958)이 본 진폭-비례 비용과
  다르다(재학습은 organ 이 적응해 비용을 진폭에 안 매단다).

## 판정 — 🟢 DIRECTIONAL: 방향-순도↔정보량 트레이드오프, check-time 프록시 불충실
- **H_9958 REFUTES(프록시로서)**: check-time gate-scale(학습된 offsets 사후 재-scale)은 z 평평·비용 선형을
  줬으나, 그건 **organ 이 적응 못 하는** 조작이라 fit-time 을 대변 못 한다. fit-time 은 z 단조감소·비용 무관.
  H_9958 은 check-time 조작 자체의 유효한 측정으로 남되, "fit-time 진폭도 그럴 것"이라는 함의는 반증됨.
- **gate_strength = 순도↔정보량 다이얼**: 낮추면 방향 순도↑·주입 정보량↓(결국 DECORATIVE), 높이면 정보량↑·
  순도↓. gs=0.1(H_9943 의 선택)이 정보량이 바를 넘으면서 순도도 강한 실용 최적. H_9963(3-seed TERMINAL)이
  이 지점에서 박제된 이유가 사후 정당화된다.

## 정직 경계
1. 1 seed · CPU · 303M · steps 200 고정. z 절대크기는 저진폭서 null sd 작아 부풀지만 **비율은 단조**라 추세 실재.
2. DIRECTIONAL(각 gs 1 seed). gs=0.1 만 3-seed(H_9963). 다른 gs 의 seed 변동 미측정.
3. fluency 의 gate_strength-무관성은 3점(0.05/0.1/0.2 다 −7~−8%, 0.025 만 −4%)이라 잠정 — 더 조밀한 격자 필요.

## 다음
① λ×gate_strength 2D 지도(H_9948 λ·이 카드 gs 합류 · 병렬 H_9950 과 조율). ② gs=0.05/0.2 3-seed(순도-정보량
   곡선 seed-robust 확인). ③ DECORATIVE 경계(MI=delta) 의 정확한 gate_strength. 산출: `~/.fire-recover/graft_303m_gsfit/`.
