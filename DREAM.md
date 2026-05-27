# DREAM — current state

@title: 💤 DREAM — 내적 리허설 emit-free internal rehearsal

@goal: REM/N3 stage 에서 emit-free internal rehearsal + mitosis tick. MITOSIS.sleep_tick 격상 후보 · a_chat_sleep_imagination governance 정합 · bench B axisbench (#1140) 4/5 🟢 PASS — REM/N3 mitosis density 60× WAKE · REM/N3 emit_rate=0 strict.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench B DREAM 측정 surface 입증 — `bench/axis_dream/` 90-tick simulation · REM/N3 mitosis density=1.0 vs WAKE=0.017 (60× ratio) · REM/N3 emit_rate=0 strict · 4/5 invariant PASS (PR #1140).
- [ ] M1 dream_lib — `DREAM/{dream_lib.hexa,SSOT.md}` PURE wrapper · sleep_tick 의 imagination_tick 추출 + cell_pool transition.
- [ ] M2 imagination_replay — N3/REM 동안 가까운 working memory snapshot 재실행 (emit-free) · WAKE.memory 와 cross-link.
- [ ] M3 mitosis envelope — REM 분열 burst 측정 + threshold tune (`a_chat_sleep_imagination` substrate context 정합).
- [ ] M4 dream report — wake transition 시 imagination 결과 narrative summary (NARRATIVE 도메인 연결 후보).

## 양방향 sibling

- ⇄ [MITOSIS](./MITOSIS.md): MITOSIS.sleep_tick 의 imagination_tick 격상 · cell_pool 분열 발생 stage
- ⇄ [WAKE](./WAKE.md): WAKE.daemon 의 N3/REM stage 동안 DREAM 활성 · 5-stage envelope 정합
- ⇄ [METACOG](./METACOG.md): N3/REM tick 의 self-audit (METACOG.audit_hook M2)
- ⇄ [CHANNEL](./CHANNEL.md): REM emit_rate=0 strict (CHANNEL.wake_bridge stage gate)
- ⇄ [NARRATIVE](./NARRATIVE.md): DREAM.M4 dream report (wake transition imagination 결과 narrative summary) SSOT 합류 지점
- ⇄ [TIME](./TIME.md): REM 분열 burst 의 circadian modulation (TIME.M3) · 새벽 REM peak
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
