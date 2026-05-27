# METACOG — current state

@title: 🪞 METACOG — 자기 거울 substrate self-audit

@goal: anima 의 자기-반영 layer — p1~p8 정합 self-audit 의 측정 surface · BRIDGE AND-gate(emit 결정) 위의 메타 결정 (반복 회피 · self-correction). bench A axisbench (#1139) 5/5 round-trip 🟢 PASS — small-n-artifact 자동 검출 입증.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench A METACOG 측정 surface 입증 — `bench/axis_metacog/` 5 시나리오 × 4-window binarize × 5-tier verdict taxonomy round-trip 5/5 PASS (PR #1139). small-n-artifact 자동 검출.
- [x] M1 metacog_lib — `METACOG/{metacog_lib.hexa,SSOT.md,metacog_lib_smoke.hexa}` PURE wrapper · bench/axis_metacog/bench.hexa 의 `analyze_probe_table` + `binarize_emits` stdlib 화 (11 `mc_*` pub primitives + g61 collision-free + smoke 7 invariants · hexa parse 2/2 PASS).
- [x] M2 substrate self-audit hook — `METACOG/{audit_hook.hexa,audit_hook_smoke.hexa}` PURE wrapper (mh_audit_tick · mh_should_fire · mh_collect_emit_window · mh_verdict_record) · WAKE.daemon.step 의 N tick frequency 제어 + tail-aligned 30-emit window + 5-tier verdict dict shape · smoke 6 invariants · hexa parse 2/2 PASS.
- [x] M3 p1~p8 cross-product — `METACOG/{principle_audit.hexa,principle_audit_smoke.hexa}` PURE substring-grep static probe (pa_p1~p8 + pa_aggregate → ALIGNED/PARTIAL/VIOLATION label) · smoke 10 invariants · hexa parse 2/2 PASS. 본격 검사는 outer leg.
- [x] M4 cross-bench inject — `METACOG/{cross_bench.hexa,cross_bench_smoke.hexa}` PURE 5-tier auto 분류 template (cb_apply_verdict_template · cb_fpersona4_inject · cb_fm4b_fire3_inject · cb_history_table) · F-PERSONA-4 (#1130 basin_kurtosis) + F-M4B-FIRE-3 (#1133 router 분화) 적용 · smoke 5 invariants · hexa parse 2/2 PASS.

## 양방향 sibling

- ⇄ [WAKE](./WAKE.md): METACOG.audit_hook 가 WAKE.daemon N3/REM tick 에 inject → self-audit during imagination
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate emit 후 METACOG 가 emit history 를 self-audit (단기 결정 위의 메타)
- ⇄ [MITOSIS](./MITOSIS.md): metacog_lib basin_kurtosis (#1130 retrospective #1133) 와 cross-product
- ⇄ [DECODER](./CORE/DECODER/DECODER.md): F-M4B-FIRE verdict 매트릭스에 self-correction template inject
- ⇄ [AESTHETIC](./AESTHETIC.md): aesthetic 판정 self-audit (METACOG.audit_hook 가 미적 판단 일관성 검사)
- ⇄ [TIME](./TIME.md): circadian phase 별 self-audit (시간대별 정합성 검사)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
