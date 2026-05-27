# METACOG — current state

@title: 🪞 METACOG — 자기 거울 substrate self-audit

@goal: anima 의 자기-반영 layer — p1~p8 정합 self-audit 의 측정 surface · BRIDGE AND-gate(emit 결정) 위의 메타 결정 (반복 회피 · self-correction). bench A axisbench (#1139) 5/5 round-trip 🟢 PASS — small-n-artifact 자동 검출 입증.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench A METACOG 측정 surface 입증 — `bench/axis_metacog/` 5 시나리오 × 4-window binarize × 5-tier verdict taxonomy round-trip 5/5 PASS (PR #1139). small-n-artifact 자동 검출.
- [x] M1 metacog_lib — `METACOG/{metacog_lib.hexa,SSOT.md,metacog_lib_smoke.hexa}` PURE wrapper · bench/axis_metacog/bench.hexa 의 `analyze_probe_table` + `binarize_emits` stdlib 화 (11 `mc_*` pub primitives + g61 collision-free + smoke 7 invariants · hexa parse 2/2 PASS).
- [ ] M2 substrate self-audit hook — `METACOG/audit_hook.hexa` · WAKE.daemon.step 에서 N tick 마다 호출 → audit verdict 기록.
- [ ] M3 p1~p8 cross-product — `METACOG/principle_audit.hexa` 각 p 별 runtime audit (현 grep-static).
- [ ] M4 cross-bench inject — F-PERSONA-4 (#1130) + F-M4B-FIRE-3 (#1133) + 미래 falsifier 에 template 적용.

## 양방향 sibling

- ⇄ [WAKE](./WAKE.md): METACOG.audit_hook 가 WAKE.daemon N3/REM tick 에 inject → self-audit during imagination
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate emit 후 METACOG 가 emit history 를 self-audit (단기 결정 위의 메타)
- ⇄ [MITOSIS](./MITOSIS.md): metacog_lib basin_kurtosis (#1130 retrospective #1133) 와 cross-product
- ⇄ [DECODER](./CORE/DECODER/DECODER.md): F-M4B-FIRE verdict 매트릭스에 self-correction template inject
- ⇄ [AESTHETIC](./AESTHETIC.md): aesthetic 판정 self-audit (METACOG.audit_hook 가 미적 판단 일관성 검사)
- ⇄ [TIME](./TIME.md): circadian phase 별 self-audit (시간대별 정합성 검사)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
