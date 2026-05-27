# DREAM — current state

@title: 💤 DREAM — 내적 리허설 emit-free internal rehearsal

@goal: REM/N3 stage 에서 emit-free internal rehearsal + mitosis tick. MITOSIS.sleep_tick 격상 후보 · a_chat_sleep_imagination governance 정합 · bench B axisbench (#1140) 4/5 🟢 PASS — REM/N3 mitosis density 60× WAKE · REM/N3 emit_rate=0 strict.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench B DREAM 측정 surface 입증 — `bench/axis_dream/` 90-tick simulation · REM/N3 mitosis density=1.0 vs WAKE=0.017 (60× ratio) · REM/N3 emit_rate=0 strict · 4/5 invariant PASS (PR #1140).
- [x] M1 dream_lib — `DREAM/{dream_lib.hexa,SSOT.md,dream_lib_smoke.hexa}` PURE wrapper · sleep_tick 의 imagination_tick 추출 + cell_pool transition (11 `dr_*` pub primitives — 5-stage 90-tick + mitosis_prior + emit_envelope + density ratio · smoke 10 invariants · hexa parse 2/2 PASS).
- [x] M2 imagination_replay — N3/REM 동안 가까운 working memory snapshot 재실행 (emit-free) · WAKE.memory 와 cross-link. `DREAM/imagination_replay.hexa` (4 `ir_*` pub primitives — select_snapshots / replay_tick / mitosis_tick_during_replay / replay_session) · 7 invariants smoke (emit_count=0 CRITICAL · cell_pool pass-through · recency_window 정합) · hexa parse 2/2 PASS.
- [x] M3 mitosis envelope — REM 분열 burst 측정 + threshold tune (`a_chat_sleep_imagination` substrate context 정합). `DREAM/mitosis_envelope.hexa` (4 `me_*` pub primitives — burst_intensity / threshold_tune / envelope_window / governance_check) · 60× WAKE ratio carry (PR #1140) · boolean-gate-free invariant (a_autonomy_over_hardcode) · 6 invariants smoke · hexa parse 2/2 PASS.
- [x] M4 dream report — wake transition 시 imagination 결과 narrative summary (NARRATIVE 도메인 연결 후보). `DREAM/dream_report.hexa` (4 `dr_*` pub primitives — collect_replay_log / summarize / wake_transition_report / kosmos_persist_dream) · NARRATIVE future hook spec · .kosmos anchor stub (a_kosmos 정합) · 6 invariants smoke (emit-free carry · transition logic · anchor format) · hexa parse 2/2 PASS.
- [ ] M5 COFFESHOP v2 generator — `mitosis_envelope` (M3) 가 silence-dominant N2/N3 시나리오 (phi_scale 0.4/0.15) 의 emit-case generator (mining @P2 · COFFESHOP v2 anchor). DREAM stage 별 envelope 에서 emit-rate 가 27%(WAKE) → N2/N3 silence-dominant 로 scaling 하는 case 를 생성 — BRIDGE M6 θ_emit stage-conditional table 의 입력 시드. sibling: BRIDGE (θ_emit stage table · M6) · MITOSIS (mitosis_envelope burst) · CHANNEL (emit-rate scaling).

## 양방향 sibling

- ⇄ [MITOSIS](./MITOSIS.md): MITOSIS.sleep_tick 의 imagination_tick 격상 · cell_pool 분열 발생 stage
- ⇄ [WAKE](./WAKE.md): WAKE.daemon 의 N3/REM stage 동안 DREAM 활성 · 5-stage envelope 정합
- ⇄ [METACOG](./METACOG.md): N3/REM tick 의 self-audit (METACOG.audit_hook M2)
- ⇄ [CHANNEL](./CHANNEL.md): REM emit_rate=0 strict (CHANNEL.wake_bridge stage gate)
- ⇄ [NARRATIVE](./NARRATIVE.md): DREAM.M4 dream report (wake transition imagination 결과 narrative summary) SSOT 합류 지점
- ⇄ [TIME](./TIME.md): REM 분열 burst 의 circadian modulation (TIME.M3) · 새벽 REM peak
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
