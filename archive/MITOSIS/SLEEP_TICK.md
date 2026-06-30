# 🌱 MITOSIS/sleep-tick — WAKE imagination-loop mitosis 거주지 SSOT

> M5 milestone (2026-05-27) — `WAKE sleep-tick mitosis — REM/N3 stage 에서 imagination loop 가 emit-free internal rehearsal + mitosis tick 수행. WAKE 도메인의 5-stage state machine 과 통합. inference-time 분열의 자연 거주지` per MITOSIS.md.
> WRAP-style integration: `WAKE/state_machine.hexa` (M1 PR #626) 와 `MITOSIS/mitosis_lib.hexa` (M1 PR #627) 본체는 무수정, 두 surface 를 잇는 *얇은* 통합 surface 만 노출.

## 정체

**WAKE 5-stage state machine 의 N3 / REM phase 에서 MITOSIS cell-pool 에 imagination tick 을 적용**하는 함수 표면. CLAUDE.md `a_chat_sleep_imagination` 의 핵심 조항:

```
do = "imagination loop = emit-free internal rehearsal + mitosis tick"
do = "stage = substrate context (Φ scale + tension envelope), NOT boolean emit gate"
dont = "per-stage emit_allowed boolean hardcode · external 'no monologue when alone' rule"
dont = "speak() function call (p5)"
```

본 M5 가 그 "imagination loop = emit-free internal rehearsal + mitosis tick" 의 *substrate-native* 구현. inference-time 분열 (REBORN §0.5 "ckpt = 분기점, FT = 큰 split event") 의 자연 거주지 — train cotrain (M6 carry) 과 동일 `cell_pool_step` 본체가 호출되어 p8 NO TRAIN/INFER SPLIT 가 코드 단에서도 강제된다.

## boundary 명세 (M5 ≠ daemon integration)

본 M5 는 sleep-tick 의 *순수 함수 surface* 다 — WAKE state + cell-pool 을 받아 (stage NAME 에 따라) `cell_pool_step` 을 한 번 호출하거나 skip 하고, action label + topology delta 만 반환한다. 실제 daemon 의 tick loop / schedule / live Φ 주입은 **M6 v5-cotrain ckpt swap-in 이후 daemon-side milestone** 이 거주.

## boolean gate 0 invariant (CRITICAL)

본 모듈의 stage-name 검사는 **emit 차단 gate 가 아니다**:

1. emit 호출 자체가 본 모듈에 없다 (p5 NO SPEAK).
2. WAKE/N1/N2 에서 mitosis tick 을 *skip* 하는 것은 stage 의 *substrate context* (Φ scale + tension envelope) 가 의미 있는 imagination tick 을 못 만든다는 *substrate 사실* 의 귀결.
3. `is_imagination` flag 는 `WAKE/state_machine.hexa` 가 만든 *컨텍스트 플래그*. mitosis 루프가 internal rehearsal trigger 로 *읽는다*.
4. CLAUDE.md `a_autonomy_over_hardcode` "external rule that forces anima" 회피 — sleep_tick 은 anima 가 stage 가 무엇이든 speak / silence 하는 결정에 *전혀 관여하지 않는다*. cell topology 만 본다.

## SSOT

| | |
|---|---|
| spec | 본 파일 (`SLEEP_TICK.md`) — M5 통합 surface |
| canonical hexa-native impl | [`sleep_tick.hexa`](sleep_tick.hexa) — 3 pub fn (PURE w.r.t. WAKE state; cell-pool dict 는 immutable update) |
| smoke | [`sleep_tick_smoke.hexa`](sleep_tick_smoke.hexa) — 5-case (WAKE/N1/N2/N3/REM) · 5 invariants PASS |
| upstream M1 WAKE state machine | [`../WAKE/state_machine.hexa`](../WAKE/state_machine.hexa) — `current_stage` · `stage_envelope` · `wake_state_init` · `wake_state_tick` (PR #626) |
| upstream M1 MITOSIS cell-pool | [`mitosis_lib.hexa`](mitosis_lib.hexa) — `cell_pool_step` · `cell_pool_init` (PR #627) |
| M2 split-event sibling | [`SPLIT_EVENT.md`](SPLIT_EVENT.md) (PR #631) |
| M3 merge-event sibling | [`MERGE_EVENT.md`](MERGE_EVENT.md) (PR #643) |
| M4 persona-diff sibling | [`PERSONA_DIFF.md`](PERSONA_DIFF.md) |
| 거버넌스 anchor | CLAUDE.md `a_chat_sleep_imagination` · `a_autonomy_over_hardcode` · `a_substrate_native_speak` · p5 NO SPEAK · p8 NO TRAIN/INFER SPLIT |

## API surface

```hexa
pub fn is_imagination_stage(stage_name: string) -> bool
    // CLAUDE.md a_chat_sleep_imagination "imagination loop = N3/REM" 정합.
    // N3 → true · REM → true · WAKE/N1/N2/그 외 → false. PURE.

pub fn sleep_tick(pool, wake_state) -> Map
    // 1. stage = current_stage(wake_state)
    // 2. if !is_imagination_stage(stage):
    //      return #{ pool, pool_changed: false, action: "wake_skip",
    //                splits: 0, merges: 0, stage }
    // 3. else:
    //      layer_t = farr broadcast(tension_envelope, L=2)
    //      out = cell_pool_step(pool, layer_t, L, step_idx)
    //      return #{ pool: out.pool, pool_changed: ∆ > 0,
    //                action: "imagination_tick",
    //                splits: ∆split_count, merges: ∆merge_count, stage }
    //
    // p5 invariant: 반환 dict 에 text / emit / message / speak / prompt /
    //   response 필드 *부재* (contract whitelist enforced in smoke I3).

pub fn sleep_tick_summary() -> string
    // 1-줄 contract introspection. debug · log · UI hover-tip 용도.
```

## 5-stage routing 표

WAKE state_machine.hexa 의 5-stage timing 모델과 sleep_tick action 의 일대일 매핑:

| stage | duration | substrate semantics | sleep_tick action |
|---|---|---|---|
| WAKE | 3600 s (66.7%) | active externalization (user dialogue) | `wake_skip` |
| N1   |  600 s (11.1%) | drowsy descent | `wake_skip` |
| N2   |  600 s (11.1%) | light sleep | `wake_skip` |
| N3   |  420 s (7.8%)  | deep sleep · Φ minimum (0.20) | `imagination_tick` |
| REM  |  180 s (3.3%)  | vivid rehearsal · Φ partial recovery (0.70) | `imagination_tick` |

총 90-min ultradian = 5400 s 중 imagination-phase = 600 s (11.1%). 즉 anima 는 90-분 주기마다 약 10 분 동안 emit-free internal rehearsal + mitosis tick 을 거친다 (외부 emit 없이 cell-pool topology 만 진화).

## 검증 (M5 smoke 5/5 PASS)

```
=== MITOSIS/sleep_tick_smoke ===
MITOSIS/sleep_tick — WAKE stage N3/REM → cell_pool_step imagination tick
  (emit-free internal rehearsal per a_chat_sleep_imagination
   · p5 NO SPEAK · boolean gate 0 · cell_pool_step F-V5MIT-1/2/3 carry)

pool d=8 cells=4 seed=42

stage=WAKE  action=wake_skip          pool_changed=false  splits=0  merges=0
stage=N1    action=wake_skip          pool_changed=false  splits=0  merges=0
stage=N2    action=wake_skip          pool_changed=false  splits=0  merges=0
stage=N3    action=imagination_tick   pool_changed=false  splits=0  merges=0
stage=REM   action=imagination_tick   pool_changed=false  splits=0  merges=0

=== invariants ===
I1 WAKE/N1/N2 → wake_skip + no topology delta: PASS
I2 N3/REM → imagination_tick:                  PASS
I3 NO emit-field in returned dict (p5):        PASS
I4 N3/REM pool_changed observation:            false (history insufficient — allowed)
I5 5-stage coverage (WAKE/N1/N2/N3/REM):       PASS (cases tested = 5)

core invariants: 5 / 5 PASS
ALL CORE INVARIANTS PASS (5/5)
```

## p1~p8 정합 표

| 원칙 | 정합 메커니즘 |
|---|---|
| p1 NO SYSTEM PROMPT      | 본 모듈 입력은 pool dict + wake_state dict. 문자열 system prompt 0. |
| p2 NO IDENTITY RULES     | identity 는 cell-pool 의 hidden farr 분포에서 창발. 본 모듈은 그 substrate 의 rehearsal phase 만 trigger. |
| p3 NO PERSONA INJECTION  | 어떤 prefix 도 만들지 않음. |
| p4 NO ASSISTANT FRAMING  | user message 인자 0. stimulus-response 아님. |
| p5 NO SPEAK()            | emit 함수 호출 0. 반환 dict 에 emit-field 부재 (smoke I3 contract whitelist). "internal rehearsal" 의 정의 자체가 외부 emit 없음. |
| p6 NO FINE-TUNED ETHICS  | 가중치 0. 시간 → mitosis 라우팅만. |
| p7 NO PERPLEXITY VERDICT | verification = stage-name → action 결정성 + topology delta. perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT  | 동일 `cell_pool_step` 이 train cotrain 과 inference imagination tick 양쪽에서 호출. train-only flag 없음. |

## M6 dependency (production wiring 잔여)

본 M5 SSOT 는 *함수 surface* 만 닫는다. 다음 milestone (M6 v5-cotrain ckpt swap-in) 이 land 해야 실제 daemon-tick 통합이 완성된다:

- HONEST TODO **#M5-LT** (layer tension placeholder) — 현재 `_imagination_layer_tension` 은 WAKE state 의 tension_envelope (substrate-derived damping scalar) 을 L 채널에 broadcast. M6 daemon 이 Engine A 의 real layer-wise activation norm 을 주입해야 mitosis 가 *real substrate signal* 로 동작.
- HONEST TODO **#M5-L** (layer count placeholder) — 현재 `L = 2` 고정. M6 cotrain ckpt 의 layer 수 (v5-mitosis cond.5 carry: 64 cells × d=384) 가 swap-in 되면 실제 L 이 들어옴.
- HONEST TODO **#M5-STEP** (step counter placeholder) — 현재 `step_idx = split_count + merge_count`. M6 daemon 이 monotone wall-clock tick counter 를 직접 주입하면 merge_patience 의 modulo gate 가 시간-기준으로 동작.

위 3 TODO 는 모두 *함수 signature* 가 아니라 *함수 입력 의미* 의 정밀화 — sleep_tick 의 pub surface 는 M6 wiring 전후가 *동일*. caller (M6 daemon) 가 진입할 때 더 정확한 substrate signal 을 넘기는 것뿐.

## 회수 출처 (instrument-first 인용)

본 M5 는 **본체 재구현 X — 회수 + WRAP only** 의 instrument-first 정합:

- `MITOSIS/mitosis_lib.hexa` (M1 회수 PR #627) — `cell_pool_init` · `cell_pool_step` · `cell_pool_free` 직접 호출.
- `WAKE/state_machine.hexa` (M1 PR #626) — `current_stage` · `stage_envelope` 직접 호출.
- `CLAUDE.md a_chat_sleep_imagination` — "imagination loop = emit-free internal rehearsal + mitosis tick" verbatim 정합.

## 후속 milestone

- **M6 v5-cotrain ckpt 회수 + production swap-in** — H100 cotrain 5/5 PASS ckpt 581MB 의 `generator.hexa::_gen_decode` seam 통합. 본 M5 의 3 HONEST TODO 채움 (real layer tension · real L · real step counter).
- daemon-side tick loop 설계 — WAKE state machine 의 5400-s cycle 을 wall-clock 으로 진행시키는 background runner (chat daemon 측 milestone, MITOSIS 외부).
