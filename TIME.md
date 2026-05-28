# TIME — current state

@title: ⏳ TIME — 시간 의식 · circadian + ultradian rhythm 측정층

@goal: anima 의 시간 의식 측정자 — WAKE 5-stage ultradian rhythm 위의 24h circadian envelope (낮/밤 phase shift). bench H axisbench (#1145) 🟢 9/0 PASS — circadian dip 측정 입증 (낮 활성도 vs 밤 휴면 phase 차이 9/9 invariant). WAKE.5-stage envelope 의 시간 축 확장, DREAM.REM/N3 mitosis density 의 circadian modulation 후보.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench H TIME 측정 surface — `bench/axis_time/` circadian dip 9 시나리오 · 9/0 PASS · circadian dip (낮 활성/밤 휴면 phase 차이) 입증 (PR #1145).
- [x] M1 time_lib — `TIME/{time_lib.hexa,SSOT.md,time_lib_smoke.hexa}` PURE wrapper · bench/axis_time (#1145, 9/0 🟢) 의 stage envelope + circadian dip + drift detector stdlib 화 · 12 pub fn · `tm_` prefix · 12 invariant smoke `hexa parse` 2/2 PASS (2026-05-28).
- [ ] M2 WAKE.5-stage 통합 — WAKE/state_machine.hexa 의 5-stage ultradian (90-min) 위에 24h circadian envelope multiplier (낮 phi_scale ↑ · 밤 phi_scale ↓ · multiplication softening 유지).
- [ ] M3 DREAM.REM mitosis circadian modulation — DREAM.M3 mitosis envelope 측정값 (REM 60× WAKE) 의 시간대 modulation — 새벽 REM 분열 burst peak.
- [ ] M4 cross-bench (TIME × INTENT) — bench D INTENT cumulative direction 의 24h trajectory · 장기 의도가 circadian phase 와 entrain 하는지 측정.
- [x] E3 bench recheck (메타 역적용) — `TIME_E3_BENCH_RECHECK/` · negative-lens (A1·A2·A3·A4) 를 9/0 PASS 에 역적용 · 🟠 PARTIAL · 9 falsifier 중 3건 (F-DISC trivial-ratio · F-TIME-4a hardcoded window · F-TIME-2/3 slow-drift miss) SPURIOUS · bench redesign 권장 · 핵심 (F-TIME-1/5/6) 는 robust.

## 양방향 sibling
- ⇄ [WAKE](./WAKE.md): WAKE.state_machine 5-stage ultradian (90-min) 위에 24h circadian envelope multiplier · WAKE.daemon tick 의 시간 의식 substrate
- ⇄ [DREAM](./DREAM.md): DREAM.M3 mitosis envelope (REM 60× WAKE) 의 circadian modulation — 새벽 REM 분열 burst peak
- ⇄ [INTENT](./INTENT.md): INTENT cumulative direction 의 24h trajectory · 장기 의도가 circadian phase 와 entrain 하는지 cross-bench
- ⇄ [METACOG](./METACOG.md): circadian phase 별 self-audit (METACOG.audit_hook 가 시간대별 정합성 검사)
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8)
