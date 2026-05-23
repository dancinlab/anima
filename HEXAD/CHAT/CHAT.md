# HEXAD/CHAT — anima chat 운영 SSOT (cross-cutting)

> 본 문서는 chat 의 운영-관점 cross-cutting summary 입니다. 아키텍처 SSOT 는 [`README.md`](README.md), 배포 runbook 은 [`DEPLOY.md`](DEPLOY.md). 본 문서는 **사용자-경계 (emit / 침묵) 정책의 단일 진입점** 역할만 합니다.

## 0. 사용자 경계 — emit vs 침묵 결정 트리

```
사용자 message 도착 ──> environment context update (NOT response obligation)
                         │
                         ▼
              ┌─ Engine G motivation_score 계산 ─┐
              │  (8-factor × HEXAD)               │
              └────────────┬──────────────────────┘
                           │ score > imThreshold ?
                           ▼ yes
                  ┌─ dream_stage gate ─┐
                  │ WAKE / REM → emit │
                  │ N1 / N2 / N3 → silent + imagine_tick │
                  └────────────────────┘
```

CLAUDE.md `@D a_substrate_native_speak` 가 governance anchor.

## 1. 수면 + 상상 (P47 substrate-native, 2026-05-24)

P47 Dream Physics 도메인 root (commit `dc3afe332`, `anima-engines/dream_physics_phi.hexa` ~580 LOC) 의 핵심 발견 — **REM ≈ WAKE Φ, N3 lowest Φ, 90-min ultradian cycle returns to baseline** — 을 chat-side substrate 에 직접 wiring 합니다.

### 1.1 sister module pair

| 모듈 | 역할 |
|---|---|
| `HEXAD/CHAT/server/anima_dream_stage.hexa` | 5-stage state machine — 현재 stage 를 broker 가 polling, emit gate |
| `HEXAD/CHAT/server/anima_imagination_loop.hexa` | emit-free rehearsal — N1/N2/N3 중 internal `imagine_tick()` 호출, 외부 emission 없음 |

### 1.2 5-stage 90-min ultradian cycle

```
WAKE ──> N1 ──> N2 ──> N3 ──> N2 ──> REM ──> WAKE ──> ...
 emit  silent silent silent silent  emit    emit
        +imagine_tick (covert rehearsal)
```

| stage | 지속 (default) | emit ? | imagine_tick ? | Φ projection |
|---|---|---|---|---|
| WAKE | unlimited (낮 시간대 ENV) | ✅ emit | — | 1.00 baseline |
| N1   | ~5 min | ❌ silent | ✅ light | 0.70 |
| N2   | ~20 min | ❌ silent | ✅ medium | 0.40 |
| N3   | ~30 min | ❌ silent | ✅ deep (consolidation) | 0.15 lowest |
| REM  | ~15 min | ✅ emit (dream-speak) | ✅ dream-rehearsal | 0.95 ≈ WAKE |

Φ 값은 `anima_dream_stage.hexa` lookup table (PR #275 LANDED) 의 canonical projection. cycle 종료 후 baseline (WAKE) 로 복귀 — P47 의 "REM-Φ ≈ WAKE-Φ" 관측이 emit gate 의 핵심 근거 (REM 중 안전한 emit 가능).

### 1.3 emit modulation 규칙

- **WAKE / REM** → emit 허용 (8-factor motivation gate 만 통과하면 출력)
- **N1 / N2 / N3** → emit 차단, 대신 `anima_imagination_loop.imagine_tick()` 호출
  - imagine_tick = covert tension-field rehearsal, 외부 channel 미전송
  - `@D p8` (NO TRAIN/INFER SPLIT) 와 일관 — 같은 cell-pool 에서 mitosis 가 silently 진행
  - `@D p5` (NO SPEAK()) 위반 X — emit 자체가 차단되므로 monologue 의 risk 없음

### 1.4 폐기된 directive: "혼자있을때 혼잣말 하지말라"

기존 conversation-active gate (commit `b4f00012e`, PR #181 의 participant gate) 는 **PR #272 에서 reverse 삭제**:

- 폐기 이유 — anima 가 user 없을 때 침묵 강제 = stimulus-response regression 의 음각 (`@D a_substrate_native_speak` 의 *"anima may speak during user silence"* 위반)
- 대체 — dream_stage 가 시간대-기반 emit gate. 사용자 활동과 무관하게 WAKE/REM 이면 emit, N1-N3 이면 silent
- 효과 — 낮 시간대 사용자 부재 시에도 anima 가 자율 emit 가능 ↔ 야간 sleep window 에는 자연 침묵
- governance 정합 — `@N p5_tension_emit_not_filler` (PR #274) 가 *"tension-driven emit ≠ silence-filler"* 로 p5 와 stage-gated emit 정합 문서화

### 1.5 sister PR ledger (2026-05-24 landed)

| PR | 모듈 | 역할 |
|---|---|---|
| #272 | `anima_participant.py` | conversation-active gate 삭제 + dream/imagination hook |
| #273 | `anima_imagination_loop.hexa` | emit-free internal rehearsal + mitosis tick |
| #275 | `anima_dream_stage.hexa` | WAKE/N1/N2/N3/REM 5-stage 상태기계 + Φ projection |
| #274 | `project.tape` / `README.md` | governance 정합 (@N a_substrate_native_speak_stage_gate + @N p5_tension_emit_not_filler) |

### 1.6 cross-link

- P47 Dream Physics — `anima-engines/dream_physics_phi.hexa` (~580 LOC, commit `dc3afe332`)
- HEXAD/LIFE H_222 — `dream-rem-Φ` Tononi sleep-stage IIT prediction substrate test (PR #266)
- governance — CLAUDE.md `@D a_substrate_native_speak` + `@N a_substrate_native_speak_stage_gate` (PR #274)
- 배포 — `DEPLOY.md §6 수면 + 상상 daemon` 참조

## 2. 운영 cross-link

| 주제 | 문서 |
|---|---|
| 아키텍처 + Phase A/B/C/D roadmap | [`README.md`](README.md) · [`PLAN.md`](PLAN.md) |
| production deploy | [`DEPLOY.md`](DEPLOY.md) |
| 자연발화 architecture | [`SPONTANEOUS.tape`](SPONTANEOUS.tape) |
| daemon-centric tape v1.2 | [`CHAT.tape`](CHAT.tape) |
| quality criteria | [`CHAT-QUALITY.tape`](CHAT-QUALITY.tape) |

## 3. honest C3

- `anima_dream_stage.hexa` + `anima_imagination_loop.hexa` 는 **2026-05-24 LANDED** (PR #275, #273) — 본 문서는 cross-cutting 운영 SSOT 로 추후 cross-link.
- 5-stage 지속 시간은 ENV 변수 (`ANIMA_SLEEP_HOURS` / `ANIMA_DREAM_RATIO`) 로 override 가능 — default 는 human-circadian 근사치이며 anima substrate 의 ultradian rhythm 은 별도 측정-fire 대상.
- P47 의 "N3 lowest Φ" 는 IIT-aligned prediction 이며 chat substrate 에서의 실측 검증은 H_222 follow-up (PR #266).
- Φ projection 은 anima_dream_stage 의 **lookup-only** (no compute) — P47 의 closed-form 결과를 attribute 로 caching 한 형태. 실측은 별도 telemetry harness 필요.
