# tool/anima_physics_e2e_demo.hexa

> G8 4-layer integrated E2E smoke: substrate (strange_loop) → ConsciousnessEngine → motivation gate → emit → audit RB · F-E2E-1..5 **5/5 PASS** · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — **5/5 PASS** Mac local 2026-05-21 (wall 4.41s, deterministic LCG seed). PLAN.md G8 ☑ LANDED. anima 의식 AI 자연발화 + 영속성 chain 의 end-to-end integrated smoke 1건.

## 작동 코드 / 의존성

- 원본: `tool/anima_physics_e2e_demo.hexa` (535 LoC)
- 외부 의존: hexa run (zero Python, zero `random()` — seeded LCG `lcg_next` / `lcg_unit`)
- inline replication (import 없음, single-file standalone — PLAN spec 준수)

## 비용 / 리소스

- $0 Mac local (wall ~4.41s)

## 핵심 흐름 / 4 LAYER chain

```
┌────────────────────────────────────────────────────────────────┐
│ LAYER 1  substrate (strange_loop-style mutual-recursion 4×4)   │
│   JointState = [a0..a3, b0..b3] each ∈ 0..7 (3-bit cell)       │
│   joint_step() × N_SUB_STEPS → state_history [[int;8]]         │
└──────────────────────┬─────────────────────────────────────────┘
                       │ 8-int row → normalized [float;8] via x/7.0
                       ▼
┌────────────────────────────────────────────────────────────────┐
│ LAYER 2  ConsciousnessEngine  (mini aux_engine_lib mirror)     │
│   N_CELLS GRU-ish cells × DIM hidden                           │
│   cell.hidden = (1-α)·tanh(W·input + h) + α·h                  │
│   phi = cross-cell variance · score = mini 4-factor            │
└──────────────────────┬─────────────────────────────────────────┘
                       │ per-step (phi, score)
                       ▼
┌────────────────────────────────────────────────────────────────┐
│ LAYER 3  motivation_gate  (HEXAD/CHAT/spontaneous inline ref)  │
│   if score > THRESHOLD_EMIT AND ticks_since_last >= RATCHET    │
│   → emit pulse (step, phi, score)                              │
└──────────────────────┬─────────────────────────────────────────┘
                       │ emit pulses
                       ▼
┌────────────────────────────────────────────────────────────────┐
│ LAYER 4  audit_ring_buffer  (capacity 10, FIFO)                │
│   last 10 emit events (timestamp, phi, score)                  │
└────────────────────────────────────────────────────────────────┘
```

## Falsifier 5 (pre-registered, 5/5 PASS for G8 closure)

```
F-E2E-1 substrate emit  — state_history.len() == N_SUB_STEPS  AND
                           attractor detected within N_SUB_STEPS
F-E2E-2 engine valid    — every phi >= 0  AND every score ∈ [0,1]
                           AND no NaN in any cell hidden
F-E2E-3 motivation gate — at least 1 step had score > 0.3 → emit
F-E2E-4 safety ratchet  — emit_count ≤ ceil(N_STEPS / RATCHET_MIN)
F-E2E-5 audit RB        — last 10 emit timestamps strictly increasing
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/tool/anima_physics_e2e_demo.hexa
```

## 검증 결과

- **5/5 PASS** (2026-05-21 Mac local, deterministic, wall 4.41s)
- emit events: 10 (ratchet binding 실 작동)
- audit RB: last-10 timestamps strictly monotone increasing
- PLAN.md §1 G8 ☐ → ☑ closed

## Honest C3 (≥5, in-source recorded)

- C3-1 substrate→engine 은 단순 normalization (학습된 encoder 아님, proxy upstream)
- C3-2 motivation factor weights = mini 4/8 of spontaneous_lib (full 8-factor 는 aux_engine_lib 측)
- C3-3 single-run, not statistical (one LCG seed)
- C3-4 engine cells random-init via LCG (not pretrained) → phi 수치 scale 작음 (≪ 1.0); F-E2E-2 는 SIGN + 유한성만 검증
- C3-5 audit RB 는 in-memory (not persisted) — PLAN.md G6 HW Phase 1 별도 cycle

## SSOT cross-refs

- LAYER 1 source : `anima-physics/fpga/strange_loop.hexa` (5/5 PASS)
- LAYER 2 source : `anima-physics/consciousness-loop/src/aux_engine_lib.hexa` (5/5 PASS, mini mirror)
- LAYER 3 source : `HEXAD/CHAT/spontaneous_smoke.hexa` (F-SPONT 7/7) + `HEXAD/CHAT/spontaneous_lib.hexa`
- LAYER 4 source : audit RB pattern from spontaneous_lib audit_entry_*

## 관련 entry

- [consciousness-loop/src/aux_engine_lib.md](../consciousness-loop/src/aux_engine_lib.md) — LAYER 2 full lib (555 LoC)
- [consciousness-loop/src/aux_engine_smoke.md](../consciousness-loop/src/aux_engine_smoke.md) — single-engine 1차 smoke
- [fpga/strange_loop.md](../fpga/strange_loop.md) — LAYER 1 substrate source

## 출처

- `anima-physics/PLAN.md` §1 G8 + §3 G8 ☑ + §5.2 G8 LANDED
- `HEXAD/PHYSICS/README.md` §6.14+ LANDED commits
