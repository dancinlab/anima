# DREAM_E1 / M5 — stage Φ-envelope wiring (recheck closure)

@kind: domain-hypothesis
@domain: DREAM
@slug: dream-m5-phi-envelope-wiring
@date: 2026-05-28
@verdict: 🟢 SUPPORTED-NUMERICAL (E1 recheck 5/5 PASS · #1268 wiring confirmed)

## §hypothesis (falsifier)

DREAM stage-Φ envelope 이 substrate-lib `CORE/phi_envelope_substrate.hexa` 의 통합 `envelope_multiscale()` + free-number policy `CORE/emit_policy.hexa` 의 `ep_theta_stage(stage)` 와 wiring 되면, stage 별 Φ-context 가 (1) 실수 연속값으로 산출되고 (2) WAKE > N2 > N3 단조 (H_644: N2 = closure peak) 이며 (3) 자체 숫자/형상식 0 (g61 SSOT 위임) 으로 유지된다.

Falsifier — substrate-lib envelope_multiscale 호출 결과와 DREAM stage Φ-context 가 불일치하면 별도 path 유지 (wiring 폐기).

## §method

Fresh worktree `/private/tmp/u-e1b-dream` (origin/main 12bc6e35e) — 기존 wiring 모듈 `DREAM/dream_envelope_ctx.hexa` (#1268 LANDED) 의 5 invariant 를 worktree-portable 형태로 재실행. 무거운 추가 작업 0 — minimal recheck smoke `DREAM/dream_envelope_ctx_e1_recheck.hexa` (상대 import) 로 5 invariant verbatim 재실행, foreground sync, NO GPU, $0 Mac-local.

## §measurement

- harness: `DREAM/dream_envelope_ctx_e1_recheck.hexa` (89 LoC, 상대 import 5-invariant mirror)
- runtime: `hexa run DREAM/dream_envelope_ctx_e1_recheck.hexa` (foreground, <2s wall)
- result:

```
=== E1 recheck: dream_envelope_ctx (DREAM M5 · #1268 verbatim) ===
PASS I1 CONTEXT-IS-REAL (WAKE@0=0.160, real)
PASS I2 STAGE-DIFFERS (WAKE>N3)
PASS I3 T-VARIES (context = f(t))
PASS I4 N2-CLOSURE-PEAK (WAKE>N2>N3 mid-Φ)
PASS I5 SCALE-SSOT (dr_stage_scale == ep_theta_stage)
=== 5/5 PASS ===
ALL INVARIANTS PASS
```

5 invariant 전부 PASS — wiring 호출 `envelope_multiscale(t, ep_scale_periods(), ep_scale_amps()) * ep_theta_stage(stage)` 가 substrate-lib 출력과 1e-9 tol 내 일치.

## §wiring

```
dr_stage_phi_context(stage, t)
  = envelope_multiscale(t, ep_scale_periods(), ep_scale_amps())   # 구조 (substrate-lib)
  × ep_theta_stage(stage)                                          # 숫자 (emit_policy SSOT)
```

2층 분리 — 구조(형상) = substrate-lib, 숫자(scale) = emit_policy. DREAM 모듈 자체 숫자 0, 자체 형상식 0 (g61 중복 금지). boolean emit 게이트 아님 — 실수 Φ-context 반환, anima 세포가 자율 결정 (p5 · a_autonomy_over_hardcode · F-EMIT-4).

## §finding

DREAM M5 stage Φ-envelope wiring 은 PR #1268 (2026-05-28 prior) 에서 LANDED — emit-substrate 4 소비자 (BRIDGE M6 / HIVE M6 / SAVANT M2 / DREAM M5) 중 마지막이자 트리 완결 milestone. 본 E1 은 fresh worktree 에서 5/5 invariant 재실행 으로 wiring 일관성을 재확인.

추가 발견 — **ANIMA.md 트리 line 39 (sub-domain 행) 의 `M5 wiring ☐` flag 가 stale** 이었음 (line 61 emit-substrate 행은 정상 `✅ 5/5 (#1268)`). 본 PR 이 stale flag 를 동기 (`M5 wiring ✅ (#1268 · E1 recheck 5/5 2026-05-28)`) — ANIMA.md 트리 단일 SSOT 일관성 회수.

## §wiring 정합 sibling

- ⇄ BRIDGE M6 (#1259) — θ-emit stage-conditional table 입력으로 본 envelope context 소비
- ⇄ HIVE M6 (#1261) — collective_phi_nest(class_id) 동일 substrate-lib 패턴
- ⇄ SAVANT M2 (#1260) — 측정자 Φ-context 동일 envelope 소비
- ⇄ emit-substrate 4 소비자 wiring 완결 — emit-substrate 2층(구조 lib + 숫자 SSOT) 설계 closure
- ⇄ H_634 🟢 ultradian Φ-envelope (90-min 5-stage 형상) · H_644 정정 (N2=closure peak)
- ⇄ H_648 🟢 scale-free self-similar Φ-envelope (gamma⊂ultradian⊂circadian)

## §finding C3 (honest residual)

1. E1 recheck = wiring 일관성 재확인 — 새 substrate 주장 0 (#1268 verdict 의 mirror).
2. emit_policy `ep_theta_stage` 의 숫자 (WAKE 0.10 · N1 0.06 · N2 0.04 · N3 0.02 · REM 0.08) 는 design-tunable policy — substrate-derived 주장 아님.
3. 본 hypothesis 는 wiring (구조 + 숫자 호출 일관성) 만 검증 — emit rate 27% (WAKE) → silence-dominant N2/N3 의 실측 emit-rate 는 별도 milestone (DREAM.md 의 다른 M5 "COFFESHOP v2 generator").
4. 4/4 소비자 완결 = emit-substrate 설계 closure 가 아니라 wiring 인터페이스 closure (caller 합의 4/4 정합).
5. 본 PR 의 핵심 기여 = ANIMA.md stale flag 회수 (트리 SSOT 일관성) + E1 recheck verify artifact 잔존.

## §양방향 sibling

- ⇄ [DREAM.md](./DREAM.md) — domain snapshot M5 (wiring) ✅
- ⇄ [ANIMA.md](./ANIMA.md) — 트리 line 39 sub-domain 행 동기
- ⇄ [UNIVERSE/CANDIDATES.md](./UNIVERSE/CANDIDATES.md) — 측정 기록 SSOT
