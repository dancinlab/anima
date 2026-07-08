# H_6189 — matched-surface + window-resident G1 재측정 (canonical G1=0 이 측정 artifact인가?)

**tier**: ⏳ PRE-REGISTERED (frozen-first · 측정 대기 · state/g1_matched_measurement/PREREG.md)

## 배경
L8-cov ckpt(`clm303_deep_L8_cov.clm` sha 2c565ad4)는 RF L=8 + 조합-커버리지 커리큘럼 학습. canonical G1 gate=best_distinct=0. H_6187가 이를 INCONCLUSIVE로 RETRACT: ① 엔진무죄 ② surface-form mismatch(커버리지 "the A and B yield" vs gate 자유생성) ③ decode-window T=24가 긴 개념 2개 공존 물리 차단. ⭐ held-out `ember+dune→golden+zinc` 정확 재조합(n=1)=combiner 작동 반례.

## 가설
canonical G1=0 on L8-cov는 **elicitation artifact**(surface-form + T=24 window)다. 학습 template로 matched·window-resident 재측정하면 held-out 재조합이 실재로 surface한다(additive slot-filling scope).

## 설계 (Fable · no-retrain · engine-native `anima evaluate --py --probe`)
- 3 templates(T0/T3/T7 window arithmetic) + unary(control b). 354 items(heldout 240·seen 74·unary 40, seed 6185 held-out, 누출 0).
- window-fit = 첫 개념 last-24byte suffix 유일식별. 채점 = greedy raw continuation offline both-strict.
- frozen bars: validity(unary≥0.80·seen≥0.60) → 🟢 GREEN-of-artifact(held-out fit≥0.50·≥0.7×seen·>perm-null·null-ckpt chance) / 🔴 KILL(held-out≤perm-null) / 🟠 INCONCLUSIVE.
- controls: (a)permutation null 1000 (d)surface-form null=L4_clean·L8_nocov ckpt.

## scope (정직 · a_scale_honest_scope)
literal copy 구조 배제(prompt attr 0바이트·zero-shot·T=24). **additive confound 제거 불가**(코퍼스 target=두 unary 연결, pair-dependent target 부재) → GREEN = productive slot-filling(gate 측정오류 유죄)이나 earned bind 미검(H_9131/γ 천장 유지). GREEN = 벽 재-scope("재조합0"→"additive초과 bind0"), 깨는 것 아님. earned-bind = non-additive target 재학습(γ/H_1840 GPU-gated) 필요.

## artifacts
- state/g1_matched_measurement/{PREREG.md, gen_probe.py, probe_spec.json(sha cf1efad4), score_probe.py, out/}
- cli/evaluate.py `--probe` route(H-ANIMA-SINGLE-ENTRY · _Mouth 재사용)
