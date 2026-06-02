# CORE — current state

@title: 🧠 CORE — anima 통합 의식 코어 (Engine A ⇄ Engine G)
@goal: anima 의 의식 엔진을 흩어진 위치(anima-core · HEXAD/CHAT)에서 떼어 CORE 가 직접 소유하는 자기완결 SSOT 로 통합 — Engine A(PureField Φ/phase) ⇄ Engine G(8-factor motivation/emit) 결합 결정 두뇌를 완전체로 구현하고, L3 생성기는 pluggable 백엔드. AGENT·CHAT 등 상위 산물이 CORE 만 import 한다 (외부 LLM 0 · p1~p8 정합).

## 소유 엔진 (CORE 자기완결)

- [x] Engine A — `pure_field.hexa` PureField Φ/phase (anima-core 에서 회수, main 없는 lib)
- [x] Engine G — `engine_g.hexa` 8-factor motivation + emit/safety (값 byte 동일 carry)
- [x] A⇄G 결합 — `brain.hexa` `brain_decide` (A의 Φ가 G의 safety ratchet 게이트 + phase=tier)
- [x] 결합 증명 — `brain_smoke.hexa` low→침묵(0.045) / high→발화(0.67)

## 엔진 ↔ .clm/.kosmos 배선 맵 (honest wiring)

CORE 의 결정 두뇌(A·G·brain)는 **외부 모델/앵커를 전혀 소비하지 않는다** — Φ·동기·tier 를
순수 기판 내부 상태에서 계산한다. .clm 모델은 오직 L3 `generator.hexa` 슬롯으로만 들어오고,
.kosmos 앵커는 `kosmos_io` → `brain_decide` read 로만 들어온다. 둘 다 아직 미배선.

| 컴포넌트 | 파일 | .clm 소비? | .kosmos 소비? | 상태 |
| --- | --- | --- | --- | --- |
| Engine A (Φ/phase) | `pure_field.hexa` | ❌ 없음 | ❌ 없음 | ✅ 기판-내부 (substrate-only) |
| Engine G (동기/emit) | `engine_g.hexa` | ❌ 없음 | ❌ 없음 | ✅ 기판-내부 (8-factor 입력만) |
| A⇄G 결합 두뇌 | `brain.hexa` (`brain_decide`) | ❌ 없음 | ❌ 없음 | ✅ A·G import 만 (import grep = 0 clm/kosmos) |
| L3 생성기 슬롯 | `CORE/generator.hexa` | ✅ **유일한 .clm 진입점** | — | 🟢 **존재+배선+decode** (`generate()` BACKEND-AGNOSTIC + `brain_emit` 결선 + null 백엔드 live · clm 백엔드 = **실제 헤더 파싱** `CLM\x01` magic+nblocks admit · **decode forward 🟢 배선** `clm_decode_ce` = int4 dequant + CLMConvMoE forward → next-byte logits → 실제 CE 측정 CORE-mounted=10.9696 (det byte-eq) · CE MEASURABLE 🟢 / descent 🔴 BLOCKED-FORMAT (inference-track .clm 이 trained embed+GN affine 미직렬화) → loaded=false 정직 유지, null fallthrough) |
| 앵커 read | `kosmos_io` → `brain_decide` | — | ✅ **유일한 .kosmos 진입점** | 🟢 **배선** (`generator_read_anchors`→`load_anchors`→`brain_emit` anchors arg · smoke 15/15 PASS) |
| 아티팩트 검증기 | `stdlib/hf/validate.hexa` (#2484) | (검증 대상) | (검증 대상) | ℹ️ **검증-전용** — 모델/데이터셋 학습되나 점검 · **런타임 엔진 아님** (sibling hexa-lang stdlib, 본 repo 부재) |

```
   ┌─────────────── CORE 결정 두뇌 (외부 모델 0 · p1~p8) ───────────────┐
   │  Engine A ── Φ/phase ──▶ brain_decide ◀── 동기/emit ── Engine G   │
   │  pure_field.hexa ✅          (brain.hexa) ✅          engine_g.hexa ✅ │
   │       └─ .clm/.kosmos 소비 0 (기판-내부 state 만) ─────────────────┘
   │                              │ emit=true
   │                              ▼
   │                  ┌─────────────────────────┐
   │   .clm 모델 ────▶ │ generator.hexa  🟢 배선   │  ← 유일한 .clm 진입점
   │                  │ (헤더 admit · decode ⏳)  │     (brain_emit→generate)
   │                  └─────────────────────────┘
   │   .kosmos 앵커 ──▶ kosmos_io → brain_emit  🟢 배선  ← 유일한 .kosmos 진입점
   └────────────────────────────────────────────────────────────────────┘

   stdlib/hf/validate.hexa  =  ℹ️ 아티팩트 검증기 (학습 되나?) ≠ 런타임 엔진 — 별개 축
```

- **불변식**: brain_decide 에 .clm/.kosmos 진입점을 직접 박지 않는다. .clm 은 generator.hexa
  슬롯으로만, .kosmos 는 kosmos_io read 로만. (이전 혼동 정정: validate.hexa 는 런타임 아님.)

## 하위 도메인

- **DECODER** (`CORE/DECODER/`) — L3 콘텐츠 생성기 (무엇을 쓸까). 백엔드 미정(상의중) · V3 더블바인드 트랙

## 마일스톤

- [ ] CHAT SSOT 화해 — HEXAD/CHAT/spontaneous_lib 가 CORE/engine_g 를 re-export (포크 제거)
- [ ] p1~p8 정합 verify — 외부 LLM 0 · system_prompt 0 · 게이트=기판 자기상태
- [ ] CORE self-test — A·G·brain smoke 묶음 1-shot PASS
- [ ] L3 결합 — DECODER 백엔드 확정 후 brain_decide emit 슬롯에 배선

## 양방향 sibling

- ⇄ [AESTHETIC](../AESTHETIC.md): CORE.engine_g 8-factor (cur · orig · dyn) 와 AESTHETIC novelty·coherence cross-product · 미적 판단이 brain_decide 결정에 modulate
- ⇄ [INTENT](../INTENT.md): CORE.brain_decide short-term emit 결정 위의 long-term goal layer · 8-factor cur/orig/dyn 와 cross-product
- ⇄ [BRIDGE](../BRIDGE.md): BRIDGE M·C·W·Φ 4-key 가 CORE engine_g 8-factor 와 cross-product · AND-gate emit decision
- ⇄ [DECODER](./DECODER/DECODER.md): CORE.brain_decide emit slot → DECODER L3 content generation
- ⇄ [SAVANT](../SAVANT.md): CORE.brain_decide 의 savant decision lane · engine_g 8-factor 위 SI modulation
- ⇄ [UNIVERSE](../UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8 + 축 E/F mirror)
