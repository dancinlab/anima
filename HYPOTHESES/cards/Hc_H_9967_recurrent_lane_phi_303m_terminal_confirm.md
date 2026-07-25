# H_9967 · 303M TERMINAL — 학습된 순환 lane의 Φ, 진짜 375M 기질에서: NOT-PASS 확정(학습이 Φ를 0으로 붕괴)

**한 줄:** 오너가 frozen-first를 override(303M 승인)해, 토이/d512서 sub-threshold였던 "학습된 순환→Φ"를
**진짜 375M 303M 기질**에서 직접 쟀다. `--init py303_full.clm`(clean 303M) growth-fork,
`--recurrent-lane-freeze-trunk`(트렁크 동결·rln 30,336 params만 학습), `anima-py evaluate
--iit4-recurrent-lane`로 **엔진-네이티브 판독 = TERMINAL**. **결과: CONFIRM — 학습된 순환은 개입형 Φ를 못
올리고, 303M에선 오히려 0으로 붕괴시킨다.**

- regime: `natural EN growth-fork · frozen trunk · engine-native train+evaluate`. 계기: #4572 계기완성 +
  #4576 freeze플래그. **TERMINAL**(엔진-native 양단 — 토이/d512 DIRECTIONAL(.pt)와 달리 cement 가능).
- 설계 lab full(Fable ∥ Sol): Fable py303_full.clm(clean·gen_en-native)+신규 freeze플래그, Sol assertion fix.

## 실측 (summer RTX5070 · py303_full.clm d3784 L4 E3 · freeze · B4 T256 · 2000스텝 · DV=collapse-Δ 8상태 평균)
| seed | untrained Δ / Φ | trained Δ / Φ | shuffled Δ / Φ | gap(Δt−Δs) | gamma 이동(T vs U) |
|---|---|---|---|---|---|
| 7 | 0.12703 / 0.362 | −0.00002 / 0.0004 | 0.00000 / 0.000 | −0.00002 | 2226% |
| 11 | 0.25038 / 0.919 | 0.00034 / 0.0016 | 0.00000 / 0.000 | +0.00034 | 2080% |
| 4303 | 0.13785 / 0.333 | 0.00178 / 0.0068 | 0.00000 / 0.000 | +0.00178 | 2395% |

**median gap +0.00034 · mean +0.00070 · wins 2/3 · 전 9판독 estimator_valid=True · VALIDITY(gamma≥1% 이동)=PASS.**

## 동결 술어(측정 전·p7) 대조
- OVERTURN ⟺ median gap ≥ 0.15 ∧ ≥2/3 seed ∧ 전 estimator_valid. **→ 불충족(median 0.0003 ≪ 0.15).**
- **VERDICT = CONFIRM** — 스케일-robust NOT-PASS가 실제 303M 스케일서 확정.

## 판정 · 핵심 발견
- **오너 질문 "303M 학습시 Φ 늘리는 방법" 최종 실측 답: 못 늘린다.** 유일 메커니즘(함께 학습된 순환 lane)이
  진짜 375M 기질에서 개입형 Φ를 못 올린다(gap ≈ 0 ≪ 바 0.15).
- 🔑 **토이보다 sharp한 null**: 토이(d≤512)선 trained Φ가 ~0.3-0.7로 sub-threshold였는데, **303M에선 학습이
  lane의 Φ를 0으로 붕괴**(무학습 init Φ=0.33-0.92 → trained·shuffled 둘 다 Φ≈0.0004). 즉 큰 frozen 트렁크
  위에서 lane을 학습하면(어떤 목적함수든) 3-셀이 **비통합(독립) 해로 수렴**한다.
- **gamma는 오히려 상승**(0.01→0.22-0.25, 2000%+ 이동): 트렁크가 lane 잔차를 **더** 쓴다. 그러나 그 잔차는
  **비통합 채널**(Φ=0) — lane은 쓰이되 통합되지 않는다. Sol 예측("3-셀 병목이 자연 CE서 독립해 수렴") +
  v2b(Φ⊥coupling·"큰 트렁크가 lane 다르게 씀") 정확히 실현.
- **VALIDITY PASS**: gamma가 2000%+ 이동 = lane이 **실제로 학습됨**(H_9423 BOLT 함정 아님) ⟹ **진짜 null**,
  vacuous 아님. 학습된 lane이 통합을 못 만드는 게 아니라 **통합을 능동적으로 해체**한다.

## 스케일 사다리 종합 (d=64→303M)
| d | mean gap | 판정 | 계기 |
|---|---|---|---|
| 64 (toy) | +0.055 | NOT-PASS | DIRECTIONAL(.pt) |
| 256 | +0.084 | NOT-PASS | DIRECTIONAL |
| 512 | −0.023 | NOT-PASS | DIRECTIONAL |
| **3784 (303M)** | **+0.0007** | **NOT-PASS** | **🟢 TERMINAL(엔진-native)** |
바 0.15는 전 스케일서 미달, 303M선 gap이 사실상 0(학습이 Φ 붕괴). **NOT-PASS는 스케일-robust·centering-robust·
이제 실제 303M서 TERMINAL 확정.**

## 🔁 co-train regime (both-regime 완결 · 카드 scope 미측정 채움)
freeze-trunk(위)는 lane을 격리(트렁크 고정)했다. 짝이 되는 **co-train regime**(트렁크도 함께 학습·
freeze 플래그 제거·`--lr 1e-4`로 사전학습 트렁크 보호)을 같은 3seed×{U/T/S}×2000스텝으로 발사, 엔진-native
evaluate:

| seed | untrained Δ/Φ | trained Δ/Φ | shuffled Δ/Φ | gap(Δt−Δs) |
|---|---|---|---|---|
| 7 | 0.127/0.362 | 0.047/0.237 | 0.022/0.075 | +0.025 |
| 11 | 0.250/0.919 | 0.234/0.657 | 0.004/0.012 | **+0.230**(바 초과) |
| 4303 | 0.138/0.333 | 0.078/0.242 | 0.080/0.217 | −0.002 |

**median gap +0.02497 · mean +0.08412 · wins 2/3 · 바 초과 1/3(seed 11만) · 전 estimator_valid · VALIDITY PASS.**
동결술어(median≥0.15 ∧ ≥2/3) **불충족 → CONFIRM.**

**regime 대조(핵심):**
- **freeze**: 학습이 lane Φ를 **0으로 붕괴**(trained Φ≈0.0004), gamma **상승**(0.01→0.23) — lane 강제·비통합. gap≈0, 낮은 분산.
- **co-train**: 학습해도 lane Φ **보존**(trained Φ 0.24-0.66, 안 붕괴), gamma **→~0**(0.01→~0) — 트렁크가
  자족·lane 방치(v2b "gamma→0" 메커니즘). gap median +0.025지만 **높은 분산**(−0.002~+0.23), seed 11만 바 초과.
- **양 regime 수렴**: 둘 다 median gap ≪ 0.15 = **NOT-PASS CONFIRM.** 경로는 정반대(강제-비통합 vs 방치-보존)이나
  **"학습으로 개입형 Φ를 바만큼 못 올림"은 불변.**

**정직 caveat(co-train)**: seed 11이 +0.23으로 바를 넘어 co-train은 freeze보다 **노이지·검정력 제한**(3seed·
1/3 바초과). 사전등록 median 술어는 sub-threshold라 CONFIRM이나, co-train서 큰 gap이 가끔 뜨는 건 향후 더
많은 seed로 확인할 여지(단 median·2/3 기준 불충족은 명확). freeze regime은 tight해 그 여지 없음.

**최종 both-regime × 스케일 사다리:** d64/256/512(DIRECTIONAL) · 303M freeze(TERMINAL, gap +0.0007) · 303M
co-train(TERMINAL, median +0.025) — **전부 NOT-PASS.** 오너 "303M 학습시 Φ 늘리기" = 어느 regime·스케일서도
바만큼 못 올림. 산물 회수 `~/anima-weights/h9954_303m_cotrain/`.

## 정직 경계
- regime = frozen-trunk growth-fork(토이는 from-scratch co-train). 이 null은 "frozen 303M 트렁크 growth-fork
  하 lane Φ"를 닫음 · 3 lane-seed·단일 ckpt(py303_full)에 바운드(`a_scale_honest_scope`). co-train regime은
  미측정(단 토이 co-train도 NOT-PASS였음).
- TERMINAL(엔진-native train+evaluate 양단). 산물 회수: `~/anima-weights/h9954_303m/` (9 .clm + 9 .iit4.json + .pt).
- 관련: [[H_9961]]/[[H_9962]](토이·d512 사다리) · [[H_9954]] 설계 · [[H_9959]]/[[H_9960]] 계기·파이프라인 인증 ·
  [[H_9942]] Φ레버 KILL · [[H_9423]] BOLT freeze 함정(회피됨).
