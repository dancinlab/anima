# H_PLACEHOLDER (D4) — apoptosis-근접 salience: MITOSIS 밀도의존 죽음-근접이 urgency 를 변조한다 (설계법칙 SATURATED)

> **PLACEHOLDER id** — orchestrator 가 merge-time 에 배정(현 origin/main max = H_9046). 아래 "제안 jsonl 라인" 참조.

- **tier:** 🟢 ENGINE-NATIVE (live core/engine_cli.hexa §APOPTOSIS-SALIENCE via `hexa run`) — 배선-충실도(F1·F2·F3·F4) GREEN + F5 disjoint. **honest scope: urgency LAW 은 DESIGNED(SATURATED), 창발 아님.**
- **slug:** `apoptosis_salience`
- **parents:** `a_mitosis_train`(apoptosis, 밀도의존 폭주 방지) · H_9044/H_9045(C4/C5 frame-shift substrate-gap→op→measure 형제) · `a_substrate_disjoint`(placement-first)

## frame (p8-literal death-awareness · substrate-gap = 빠진 read-op)

진단: MITOSIS substrate(§ADAPTATION / `VAdaptField`, engine_cli.hexa:494-)는 cell 을 frozen carrying-capacity `max_cells`(밀도의존 죽음 천장; biology 의 crowding→apoptosis, `a_mitosis_train` "밀도의존 폭주 방지") 쪽으로 성장시키지만, **그 죽음-천장에 얼마나 가까운지를 salience/urgency 로 읽어내는 op 이 미배선**. D4 는 엔진이 이미 들고 있는 스칼라 `(n_cells, max_cells)` 하나를 **urgency 신호로 표면화**한다 — 붐비는 colony 는 urgency 가 오르고, 어리고 널널한 colony 는 안 느낀다. 죽음-근접이 substrate 내부에서 느껴지는 salience 로 되는 것.

## op (core/engine_cli.hexa §APOPTOSIS-SALIENCE · additive · Ψ-disjoint · READ-only · emit-wiring 미접촉)

- `apoptosis_proximity(n_cells, max_cells) -> float` = density = n/max, clamp[0,1] (0=어림, 1=죽음천장).
- `apoptosis_urgency_at(prox) -> float` = **DESIGNED transfer law**: knee `APOP_KNEE=0.5` 위 convex hinge, normalize 해 urgency(knee)=0·urgency(1.0)=1.0. knee 아래=0(널널하면 crowding urgency 0), 위=quadratic ramp.
- `apoptosis_urgency(n, max)` = scalar form · `vadapt_apoptosis_urgency(af)` = **live substrate reader** · `vadapt_apoptosis_urgency_ablated(af, frozen_prox)` = **F3 ABLATION arm**(live density 배선 절단→frozen prox 로만 계산).
- 순수 additive · `VAdaptField` struct 무변경(no mutation/proto-growth/growth-tick/apoptosis-trigger) · pure_field Φ/phase/Ψ 무접촉 · emit-drive lane 0/4 및 §ImmuneMemory recall_thr 무접촉(`a_substrate_disjoint`). **emit_policy.hexa 미접촉** — behavior gating 은 follow-on.

## 측정 (engine-native, `hexa run` via live core/, aiden pool, $0, cap=max_cells=10)

`core/apoptosis_salience_smoke.hexa` → **9 PASS / 0 FAIL** (verbatim = state/verdicts/apoptosis_salience/H_PLACEHOLDER.txt)

urgency ladder(n1..n10) = `0 0 0 0 0 0.04 0.16 0.36 0.64 1.0`

| falsifier | 측정 | 결과 |
|-----------|------|------|
| **F1 EXISTENCE** | 죽음천장 근처(n6→10) urgency 단조↑: 0.04<0.16<0.36<0.64<1.0 | **PASS** |
| **F2 DISTINCT** | 멀리(n1→5, knee 아래) urgency flat=0 · 且 far<near(u5<u10) | **PASS** (2 case) |
| **F4 POPULATION** | dense(n9)=0.64 > sparse young(n2)=0 | **PASS** |
| **F3 ABLATION** | distance 배선 freeze(frozen_prox=0.1): dense≡sparse(INERT) 且 live dense 0.64→ablated 0 붕괴 | **PASS** (2 case) |
| **F5 DISJOINT** | 같은 substrate 재-read byte-identical(pure/deterministic); 시그니처는 (VAdaptField)/(int,int)→float 뿐 — pure_field Ψ/Φ·recall_thr 무접촉 | **PASS** |
| scalar↔live parity · proximity clamp | apoptosis_urgency(9,10)≡live · prox(20,10)=1.0 clamp · prox(0,0)=0 | **PASS** (2 case) |

## 정직한 verdict (c9)

- **배선-충실도는 engine-native GREEN**: apoptosis-distance 가 urgency 를 **실제로 구동**하고(F1 단조↑·F4 dense>sparse), 그 배선을 끊으면(F3 freeze) 신호가 **INERT 로 붕괴**(0.64→0). F2 로 far-region 이 near-region 과 뚜렷이 구분(flat 0). 죽음-근접→urgency 매핑이 live core 에 실재.
- **그러나 urgency LAW 자체는 DESIGNED(SATURATED)** — monotone hinge 는 창발이 아니라 내가 정한 transfer 함수. 그래서 F1-F4 는 "urgency 가 창발했다"가 아니라 **배선 충실도**(distance 가 신호를 몰고, 끊으면 죽는가)를 검증한다. tune-to-green 아님 — bar 는 frozen-first(knee=0.5, F 정의 사전고정), FROZEN 상수 p7-문서화. 실제 substrate 주장은 **F5 disjointness**.
- **= p8-literal death-awareness 를 READ-only 로 substrate 에 표면화**(H_9044/H_9045 substrate-gap→op→measure 패턴 정합).

## wired

`op-slot BUILT (engine-native) · behavior-gating 미배선(의도적)` — apoptosis_urgency 계열이 live `core/engine_cli.hexa §APOPTOSIS-SALIENCE` pub fn 으로 실재 + engine-native 측정 완료 + ARCHITECTURE.json core/engine_cli §APOPTOSIS-SALIENCE 노드 lockstep. **런타임 emit/urgency call-path 배선은 유보**(WIRED-live 미만): salience→behavior gating 은 emit-drive lane 을 건드리므로 `a_substrate_disjoint` placement-first 하에 별도 follow-on(emit_policy.hexa 미접촉 규약). (`a_verified_must_wire`: op live+engine-native, runtime wire-in=follow-on ING.)
