# E1/G1 lane 조율 — F2 corpus는 rule-structured여야 (DATA-PATH-CONFIRMED)

## 왜 이 핸드오프 (한 줄)
E1 slot-303M build의 병목은 이미 "corpus 밀도"로 확정돼 있었는데(commits 897111ae0/5bb20e577: "E1병목=corpus밀도 F2 authoring, 메커니즘 아님"), 이번 세션이 그 F2 corpus가 **어떤 형태여야 하는지**를 실측으로 좁혔다: **dense가 아니라 rule-structured(체계적 compositional)** 여야 held-out 재조합이 열린다.

## 이번 세션 실측 (전부 origin/main 착지)
- **crux (#3032)**: REAL 303M joint pair-rep h(a,b)를 singles에서 FiLM(bilinear) 예측 = additive와 동일(0.866, Δ-0.0005). 303M 합성은 ADDITIVE — bind할 bilinear interaction 無. ⟹ 더 좋은 slot/readout 機構로 안 풀림. **벽은 TARGET/DATA-side.**
- **F2 (#3016)**: natural corpus 재조합 target = collocation-only, held-out 전이 0.
- **F2 poc (#3035, state/f2_authored_transferable/)**: 체계적 rule corpus는 held-out 전이 R² 0.425 vs collocation -0.508 (delta +0.93) = **DATA-PATH-CONFIRMED**. rule-structured 데이터가 벽을 깬다.
- **transfer sweep (#3031)**: bilinear/multiplicative 機構는 transferable target이면 전이 획득 — 즉 機構는 유능, 관건은 데이터 form.

## E1 lane에 대한 함의 (조율 요청)
1. **slot 機構만으로는 부족**: A11 fixed-role forward-slot은 실 303M --py 0/5 floored(H_9121); E1의 TRAINED gate도 corpus가 collocation이면 crux대로 additive로 붕괴한다. slot build의 성패는 **F2 corpus가 rule-structured인지**에 달렸다.
2. **F2 corpus 목표 재정의**: "dense δ_FM" (H_9128)만으로는 form-priming(템플릿 암기, ability 아님)에 그친다 — 공동 커버리지 303M이 🟠 form-priming이었던 이유. 목표 = **held-out 조합이 rule로 derivable한 systematic-compositional corpus** (F2 poc가 증명한 form).
3. **공유 recipe**: rule-structured corpus 설계(Fable)를 이 세션이 작성 중 → 착지하면 state/f2_authored_transferable/CORPUS_DESIGN.md. E1 lane과 **같은 recipe**를 쓰자(경쟁 corpus 아님). production authoring은 E1 lane 소유, 원리·측정 프로토콜은 이 세션 산출.
4. **측정 프로토콜**: held-out compositional split(train/test 개념+rule 공유·특정 조합만 held-out) + shuffle-rule 통제 = anima evaluate --py G1 ladder(composed_distinct≥2>max_single). form-priming 방지 = held-out 전이가 shuffle-rule 통제를 이겨야(pre-reg kill).

## 재개지점
- 이 세션: ING `F2 authored transferable-form corpus authoring` (rule-structured 설계→authoring→303M retrain owner GPU-go).
- E1 lane: ING `e1-303m-byte-context-scale` — F2 corpus를 rule-structured로 authoring한 뒤 slot-303M build.
- 접점: 두 lane이 state/f2_authored_transferable/CORPUS_DESIGN.md 공유 recipe로 F2 corpus를 함께 만든다.
