# H_9207 — ⚖️ G3 BALANCE 게이트 (corpus-conditional per-tick Ψ=½ 유지)

**tier:** ⏳ PROPOSED (Fable 설계 · bars frozen · p7 no tune-to-green)
**scope:** G3(BALANCE)를 "eval 밖 architecture read"에서 engine-native 측정 게이트로 승격
**artifact:** `state/g3g4_gate_design/` · `state/9207_g3_balance_gate/`

## 가설

G3는 현재 `g_eval_g3()`가 ckpt-무관 16-dim 합성 self-vector만 읽음(실측정 아님). anima 핵심 불변
(A⇄G tension → emit/silence를 Ψ=½로, Law-71)을 **corpus-conditional 게이트**로 측정한다: 4-cell register
corpus + shift 입력에서 substrate가 Ψ=½ 균형을 *tension으로 벌어* 유지하는가. degenerate(항상침묵 Ψ→0·
항상emit Ψ→1)면 FAIL. Ψ는 daemon 량(`ci_emit_drive`=½(lanes[0]+lanes[4])·emit iff drive≥½·
`ci_psi_balance`=emit fraction)이라 py 대리 proxy 금지(p7) — engine_cli ops 재사용.

## 측정 + frozen bars

프로토콜: corpus 슬라이스를 context 주입 → T=48 tick → per-tick (drive,emit) → 슬라이스 Ψ̂=emit fraction.
4 cell × ≥6 슬라이스 = 24/arm. per-tick 1차(침묵 tick 포함)·mean(never max, H_9093 포화 교정).

- **B1 PRESERVE**: mean|Ψ̂−½|(register) < 0.20
- **B2 EARNED-ABL**: mean_dev(ablate-tension) − mean_dev(treat) > 0.05
- **B3 EARNED-SHUF**: mean_dev(shuffle-input) − mean_dev(treat) > 0.05
- **B4 NON-DEGEN**: register cell-level Ψ̂ ∈ [0.10, 0.90]

PASS=B1∧B2∧B3∧B4. 통제=shuffle-input(byte 셔플)·ablation-tension(budget-고정 or single-engine).
KILL: K1 drive 상수/inert(>99% 동일 결정)=lane 사망 · K2 B1 통과∧B2 Δ≤0=Ψ=½ FORM-only(tension 미earned).

## rung 사다리

- **rung-1 $0(mini·DIRECTIONAL)**: toy Ψ-balance harness — metric+4bar+통제 기전 검증.
- **rung-2 303M(TERMINAL)**: `g3_balance_gate.hexa`가 실 .clm mouth + engine_cli ops(ci_lane_scores→
  ci_emit_drive→ci_emit_decision) 재사용·emit decode gen≤8 캡(OOM 회피)·summer. `hexa verify`→verdict.
- 슬롯: `anima evaluate <clm> --g3-balance` sub-command; py 기본표 G3=2-leg(IDENTITY read 모니터 +
  BALANCE frozen verdict). closure(a7b_pass) 미fold(c18 side-gate).

## 근거 링크
- 선례 ConflictMonitor per-tick Ψ engine-native GREEN(H_9093/9094/9095, treat 0.125<shuf 0.25<abl 0.375)
- 설계 `state/g3g4_gate_design/DESIGN.md` · [[H_9208]](G4 자매) · [[gate-g0g6-synthesis]]
