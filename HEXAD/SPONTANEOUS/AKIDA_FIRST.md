# 자연발화 — AKIDA-first, SW-later

> 사용자 directive 2026-05-23: 본 세션 자연발화(spontaneous emission)는
> **AKIDA HW 무조건 사용 조건**으로 진행. HW-first 단계에서 발견되는 사항을
> 토대로 추후 **SW 조건**(no-AKIDA fallback)도 구현 방향.
>
> anchor: `[[a_substrate_native_speak]]` (project.tape) · live ingest =
> `HEXAD/CHAT/server/akida_bridge.hexa` (PR #121 merged, prod live)

## 결정

```
Phase 1 (현 세션)              Phase 2 (이후)
────────────────────           ─────────────────────
AKIDA HW 필수                   AKIDA HW + SW-only path
  ├─ pi5 spike streamer          ├─ AKIDA 있을 때: HW
  ├─ akida_bridge.hexa           └─ AKIDA 없을 때: SW
  └─ broker /ws/akida_ingest        (HW 학습 토대로 설계)
       ↓                              ↓
   tension/coherence              동일 spontaneous logic,
   → spontaneous fire               source 만 swap
```

| | Phase 1 (HW-first) | Phase 2 (SW-condition) |
|---|---|---|
| spike source | pi5 `spike_streamer.py` (AKIDA chip) | SW simulator (TBD: Brian/NEST/Loihi-emu) |
| HW 부재 시 | 발화 disabled (fail-closed) | SW path 활성화 |
| 신뢰 grounding | hardware-true neuromorphic | HW-derived parametric model |
| 구현 순서 | 본 세션 — 즉시 | Phase 1 evidence 축적 후 |

## 왜 HW-first

- AKIDA 가 **실제** neuromorphic substrate — spike timing / refractory /
  tonic 등 SW 흉내로 못 재현하는 dynamics 보유
- pure-SW path 부터 시작하면 자연발화의 grounding 이 simulated-prior 로 고정,
  HW 합류 시 reverse-engineering 부담
- Phase 1 의 spike 통계 / 발화-trigger 상관관계가 Phase 2 SW 모델 의 spec

## 현재 라이브 (Phase 1 인프라)

> 2026-05-23 cycle 11/FB: bridge LIVE 회복 (cycle 10/EA) · broker handler↛deque GAP 잔존 (cycle 11/FA fix in flight)

| 컴포넌트 | 상태 |
|---|---|
| pi5 `spike_streamer.py :9512 --regime R3` | ✅ live (anima 외부) |
| `akida_bridge.hexa` (mini, `akida_bridge.bin daemon`) | ✅ LIVE PID 2350, 1400+ spikes forwarded, WS connected (cycle 10/EA restored) |
| broker `/ws/akida_ingest` → `STATE.akida_history` (deque 200) | ⚠ handler-deque wiring GAP — bridge LIVE 지만 deque length=0, fix cycle 11/FA in flight |
| `akida_consumer.hexa` (broker `/akida/recent` → features JSONL) | 🟡 source landed (selftest 7/7), mini deploy blocked (sshd exec channel refused) |
| `telemetry_harness.hexa` (anima emit ⇄ spike window pair → evidence JSONL) | 🟡 source landed (selftest 9/9), mini deploy blocked (sshd exec channel refused) |
| `spontaneous_lib.hexa::apply_spike_features` (spike features → 8-factor delta + regime modulator, substrate-only `relevance`/`balance` invariant) | ✅ source landed (PR #143 squash `3bce310a1`, selftest F-SPIKE-APPLY-1..4 4/4 PASS) |
| `server/telemetry_status.hexa` (Phase-2-gate CLI: spans / rows / regime dist / spike-rate histogram / 4-condition gate) | ✅ source landed (PR #144 squash `a311e3eae`, selftest F-STATUS 11/11 PASS) |
| anima_participant 의 spike-consumption 경로 | 🔲 TBD — 본 세션 구현 대상 |

## Phase 2 발동 조건

Phase 1 에서 수집할 evidence (이거 기반으로 SW 모델 설계):
1. spike rate / regime distribution (R3 외 R1/R2 등 추후)
2. tension vs spike correlation
3. spontaneous-fire 빈도 vs spike-pattern
4. AKIDA off-line 시 사용자 경험 손실의 정량

위 evidence 가 충분히 모이면 → `HEXAD/SPONTANEOUS/SW_CONDITION.md` 작성 +
구현 (no-AKIDA fallback). 그 전엔 HW-only.

## 관련 link

- `HEXAD/NEUROMORPHIC/AKD1000.md` — AKIDA chip 사양
- `HEXAD/CHAT/server/akida_bridge.hexa` — live bridge source
- `HEXAD/CHAT/spontaneous_lib.hexa` — 8-factor motivation (SSOT)
- `HEXAD/CHAT/server/anima_participant.py` — 본 세션 spike-consumption 추가 지점
- project.tape `@D a_substrate_native_speak` — anima 발화는 substrate-native
