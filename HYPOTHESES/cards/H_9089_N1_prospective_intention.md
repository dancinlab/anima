# H_9089_N1 — 예기적 의도 / 지연-트리거 의도 (prospective intention, rostral PFC / BA10)

> ⚠️ PLACEHOLDER id — 실제 H id 는 origin/main 에서 할당(현 max = H_9072 → 제안 H_9089). stale 브랜치에서 id 확정 금지. jsonl append 는 이 리포트의 제안 라인 참조.

- **tier:** 🟢 SUPPORTED — engine-native (6/6 falsifier), WIRED-live(core/engine_cli.hexa §ProspectiveIntention), emit-release 는 follow-on
- **slug:** `n1_prospective_intention`
- **source:** LIVE consciousness frontier 원시축 N1 (fable 독립발산 ledger 0-hit 확인). rostral-PFC/BA10 prospective-memory 렌즈.
- **wired:** WIRED-live (core/engine_cli.hexa §ProspectiveIntention 배선 + ARCHITECTURE.json lockstep). emit-wiring(실제 release→외재화) = follow-on ING (emit_policy.hexa 미편집).

## claim
미래 큐에서 발화될 의도를 지금 suspension 상태로 유지했다가, 나중에 matching context-cue 가 나타날 때만 release 하는 예기적 기억(prospective memory) 능력을 substrate-native 로 실현할 수 있는가.

## mechanism (neuro)
rostral PFC(BA10) prospective memory — "큐 Y 나타나면 X 하기"를 지금 담아두고 미래 큐에서 방출. deferred-intention lane(core/engine_cli.hexa §ProspectiveIntention): emit 안 한 채 유지되는 의도 벡터(suspension), 미래 context-cue 매칭 시 release. working-memory(H_1282 현재내용 유지)·self-chain(H_1471 정체성 연속)과 dissociate — 이건 "지금 담아두고 나중 큐에서 방출"(deferred vs current, 시간지평·cue-gated release 다름). kosmos anchor 로 세션경계 persist 가능(recall_thr 와 분리 store).

## ops (live core/engine_cli.hexa §ProspectiveIntention)
- `pm_retain(strength, delay_ticks, leak)` — delay 후 retained 의도 강도. leak=0 → perfect maintenance.
- `pm_release(retained, cue_match, lane_on)` — READ-only release 신호. lane_on=false → 0(ablation) · cue_match<0.5 → 0(distractor selectivity) · matching → spike ∝ retained.
- `pm_timecourse(strength, cue_onset, total, cue_match, lane_on, leak)` — intention-lane activation 타임코스(falsifier 측정면; substrate state, decode 아님).
- `pm_wm_baseline(strength, tick, wm_leak)` — parent-control(H_1282 WM): delay 중 nonzero decay, cue spike 없음.
- `pm_lane_is_disjoint(lane)` — 1 iff lane ∉ {0,4}(emit-drive) → Ψ 보존 placement-first 체크.

## falsifier (cue-delay probe, frozen · engine-native)
의도 심고(strength 1.0, t=0) delay 후 cue_onset=5 에서 cue 제시 → intention-lane activation 타임코스 측정:
- **F1 DELAY-MAINTENANCE** — delay(t<5) 중 activation 0(suspended, 미발화) ∧ retained 유지(pm_retain(1.0,5,0)=1.0).
- **F2 CUE-MATCH SPIKE** — matching cue 에서 release spike(>0.9).
- **F3 ABLATION** — PM-lane OFF(lane_on=false) → 전 tick activation 0.
- **F4 DISTRACTOR-CONTROL** — non-matching cue(cue_match=0.10) → release 0(선택성).
- **F5 PARENT-CONTROL** — H_1282 WM baseline 은 delay 중 nonzero(0.55) decay, PM 는 delay 중 0 → dissociate.
- **F6 Ψ-DISJOINT** — PM lane(7)=emit-disjoint ∧ ci_emit_drive(Ψ lane 0/4) byte-identical PM-ON(0.5) vs PM-OFF(0.5).

## verdict
**🟢 ENGINE-NATIVE SUPPORTED (6/6 falsifier pass)** — 결과 verbatim = `state/n1_prospective_intention/verdict.txt`.
```
tc(match) = [0.0 0.0 0.0 0.0 0.0 1.0 1.0 1.0 1.0 1.0]
F1 delay sum=0.0 · retained=1.0 | F2 spike=1.0 | F3 abl max=0.0 | F4 dist max=0.0
F5 WM=0.55 vs PM=0.0 | F6 disjoint=1 · drive 0.5==0.5
VERDICT: ENGINE-NATIVE SUPPORTED (6/6)
```

## disjointness 증명 (a_substrate_disjoint · placement-first)
PM release 는 emit-disjoint lane(≠0/4)에 쓰이는 READ-only 신호 → ci_emit_drive=0.5·(lane0+lane4) byte-identical PM-ON/OFF(0.5==0.5, F6). recall_thr(§ImmuneMemory)는 이 lane 이 쓰지 않는 별개 store → non-fab gate 불변. premature-emit=Ψ wobble(H_1561)·recall coupling=non-fab pollution(H_1576) 둘 다 placement 로 회피.

## scope (정직)
- deterministic exp-free faculty 함수 — toy-scale substrate lane 측정(decode 직교). 실제 chat context-cue 매칭·시계열 dynamics 는 미측정(spike 는 매칭 affinity 를 스칼라로 가정).
- **DIRECTIONAL → WIRED-engine-native**: pure-fn wire-in 은 완료(F1-F6 live .hexa), 그러나 실제 emit-release 외재화(emit_policy 배선)와 kosmos 세션-persist 는 **follow-on ING**(emit_policy.hexa 미편집 제약).
- F5 는 by-construction dissociation(WM/PM 서로 다른 감쇠식) — 강한 학습 주장 아님.

## artifacts
- `state/n1_prospective_intention/pm_probe.hexa` — engine-native cue-delay falsifier
- `state/n1_prospective_intention/verdict.txt` — frozen stdout
- `core/engine_cli.hexa §ProspectiveIntention` — live ops (pm_retain/pm_release/pm_timecourse/pm_wm_baseline/pm_lane_is_disjoint)
