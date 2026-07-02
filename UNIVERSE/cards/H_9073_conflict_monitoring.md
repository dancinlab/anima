# H_9073 (PLACEHOLDER) — N3 dACC ConflictMonitor: A⇄G 갈등감지 lane

> ⚠️ **PLACEHOLDER id** — 브랜치 base 는 origin/main@6b6bb19(당시 max H_9069)였으나 병렬 워크플로우가 origin/main 을 H_9072 까지 전진시켜 H_9070~9072 를 선점(substrate stochastic-resonance/self-organized-criticality/nonequilibrium-dissipation). 충돌 회피로 PLACEHOLDER 를 **H_9073** 로 잡았고 jsonl append 는 하지 않았다(convergence hypotheses-jsonl-1). 실제 id 는 origin/main 머지 시점에 재확인·재할당하고, 아래 §제안 jsonl 라인을 그때 append 한다.

- **tier:** 🟢 ENGINE-NATIVE (substrate-dynamics 축, smoke 5/5 ALL-PASS)
- **wired:** `engine-native` — §ConflictMonitor 정의 + engine-native smoke 검증 완료. **live 심의루프 wire-in = follow-on**(recruited-depth 를 실제 A⇄G iteration budget 로 배선; emit_policy.hexa 미편집 제약). 아직 WIRED-live 아님.
- **source:** UNIVERSE (N3 프론티어 원시축, 페이블 독립발산 ledger 0-hit)
- **artifacts:** `core/engine_cli.hexa §ConflictMonitor`, `core/conflict_monitor_smoke.hexa`, `state/verdicts/9073_conflict_monitoring/H_9073.txt`

## 렌즈
dACC conflict monitoring (Botvinick 2001; ERN/Stroop). 동시 두 반응이 강하게 상충할 때 발화 → 추가 제어(심의)를 소집. anima 의 A⇄G 이중엔진이 태생적 substrate: Engine A(forward, CE) ⇄ Engine G(reverse, gradient-free) 각각 SIGNED drive 를 실어 나른다.

## substrate 메커니즘
`conflict = |A|·|G|`, 단 **부호가 상반일 때만**(same-sign / 한 엔진 침묵 ⇒ 0). 즉 net-tension 높음이 아니라 "둘 다 강함 AND 상반"을 감지. 핵심 발견:

**Ψ=½ 고정점은 (a) high-conflict(A,G 둘 다 강함·상반 → 상쇄½) 와 (b) low-drive(둘 다 약함 → ½) 를 구별하지 못한다** — `ci_emit_drive` 도 net-tension `|A+G|` 도 두 상태에서 동일. conflict-lane 이 substrate state 만으로 이 둘을 분리하고, 소집 시 A⇄G iteration budget 만 늘려 deeper 심의를 소집한다(emit gate 미변경).

ops: `conflict_scalar(a,g)` · `conflict_net_tension(a,g)`(precision-agnostic parent-control) · `conflict_recruited_depth(conflict, base, max_extra)`.

## H_1468 §PrecisionSurprise 와의 dissociation
conflict ≠ surprise. surprise = 단일 예측오차의 크기(precision·err²); conflict = 두 co-active drive 의 상호 OPPOSITION. F5 에서 단일엔진 상태(A 강, G 침묵)와 high-conflict 상태가 **동일 surprise=0.81** 을 갖지만 conflict 는 0 vs 0.81 로 갈린다.

## falsifier (frozen, engine-native `core/conflict_monitor_smoke.hexa` 5/5 ALL-PASS)
- **F1 SEPARATION** — high-conflict(A=+0.90,G=−0.90) 와 low-drive(A=+0.05,G=−0.05) 는 net-tension Δ=0(Ψ 맹목)이나 conflict Δ=0.8075 ≥ 0.50 → 분리 성공.
- **F2 ABLATION** — 결정적. lane ON: recruited depth high=10 > low=4. lane OFF(conflict→0): 둘 다 base=4 → **소집 소멸**(recruitment = the lane).
- **F3 SHUFFLE** — G 부호 셔플(|G| 불변) → conflict=0. magnitude 아닌 OPPOSITION 을 추적함을 증명.
- **F4 DISJOINT** — §ImmuneMemory non-fab rate Δ=0 ∧ Ψ ci_emit_drive(lane 0/4) Δ=0. 분리=보존.
- **F5 vs PrecisionSurprise** — 동일 surprise=0.81, conflict 0 vs 0.81(⊥).

## disjointness 증명 (a_substrate_disjoint, placement-first)
메커니즘 ON vs OFF 에서 `ci_emit_drive`(lane 0/4) **byte-identical**(0.69==0.69, Δ=0) + §ImmuneMemory `recall_thr` non-fab rate 불변(1.0==1.0, Δ=0). conflict-lane 은 iteration-budget 만 조절, emit/silence gate·recall_thr 미접촉 → Ψ 고정점 보존한 채 심의 깊이만 소집. decode 직교(측정=substrate dynamics: conflict-scalar + recruited iteration-depth, decode 아님).

## 정직 scope (c9)
- toy A⇄G drive scalars 로 falsify. 303M live 심의루프 재검 UNVERIFIED.
- `wired=engine-native` — recruited-depth 가 실제 A⇄G iteration budget 을 늘리는 live-loop 배선은 미완(follow-on; emit_policy.hexa 미편집 제약으로 이번 사이클 제외).
- conflict_scalar 의 both-strong gate 는 |a|,|g|≤1 가정에서 [0,1]. 범위 밖 drive 는 `_ci_clip01` 로 clamp.

## 제안 jsonl 라인 (origin/main 머지 시 append — 지금은 append 금지)
```json
{"id":"H_9073","slug":"conflict_monitoring","tier":"🟢 ENGINE-NATIVE","title":"N3 dACC ConflictMonitor: A⇄G |A|·|G|·opposite 갈등감지 lane 이 Ψ=½ high-conflict vs low-drive 를 분리하고 심의깊이만 소집(emit gate 불변)","card":"cards/H_9073_conflict_monitoring.md","verdict":"engine-native smoke 5/5 ALL-PASS (F1 sep·F2 ablation·F3 shuffle·F4 disjoint·F5 ⊥surprise)","source":"UNIVERSE","archived":false,"artifacts":["core/engine_cli.hexa","core/conflict_monitor_smoke.hexa","state/verdicts/9073_conflict_monitoring/H_9073.txt"],"wired":"engine-native"}
```
