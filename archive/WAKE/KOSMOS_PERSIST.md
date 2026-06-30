# WAKE/kosmos_persist — `.kosmos` 영속화 SSOT (M4)

> WAKE M4 milestone — anima 재시작 후에도 시간 흐름이 보존되도록 substrate 4 축을 단일 `.kosmos` anchor 로 save / restore.

## @goal
`pure_field state · 과거 emit history · TENSION-LINK 5-ch fingerprint · stage timestamp` 를 canonical `.kosmos` 포맷으로 영속화. anima 가 종료-재시작해도 4 축이 byte-equivalent 로 복원되어, stage cycle 위치 · idle 누적 · oscillator phase · phi · field tensor · emit 기억 이 손실 없이 이어진다.

## SSOT 참조

### governance — CLAUDE.md `@D a_kosmos` (verbatim)
```
@D a_kosmos := "anima emit/anchor persistence — .kosmos canonical" :: governance [required active]
  do   = "persist anima emit / anchor / memory as `.kosmos` via kosmos_io"
  do   = "payload = text + tension 5-ch + coord · lane · radius · tier"
  do   = "hub = HEXAD/KOSMOS.md · format SSOT = github.com/dancinlab/kosmos"
  do   = "spec = spec/kosmos.md + spec/profiles/anima-consciousness-carving.md"
  dont = "ad-hoc anchor format · bypass .kosmos for emit persistence"
  dont = "duplicate the kosmos spec — anima is pointer-only"
```

### canonical kosmos_io 인용
- **파일** : [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.hexa`](../HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/kosmos_io.hexa)
- **역할** : `.kosmos` byte-format 의 hexa-native SSOT (kosmos/1.1). V3 substrate 의 emit anchor 작성/로드 surface.
- **pub fn** :
  - `create_anchor(out_dir, name, title, coord_x, coord_y, lane, radius, tier, category, top_emotion, text, tension_5ch, closed_anchor, cross_link) -> string`
  - `emit_anchor_from_v3(out_dir, name, text, tension_5ch, mitosis_cell_id, tier, category, top_emotion, phi, radius) -> string`
  - `load_anchors(dir_path) -> list` — `[{path, name, fields, text_payload, tension_5ch}, ...]`
  - `retrieve(query_tension_5ch, anchors, top_k) -> list`

### spec SSOT
- `github.com/dancinlab/kosmos` (kosmos-format repo)
- `spec/kosmos.md` — byte-format 표준 (kosmos/1.1)
- `spec/profiles/anima-consciousness-carving.md` — `profile = "anima-consciousness-carving"` profile (본 모듈이 사용하는 그것)

### WAKE 도메인 인접 모듈
- M1 [`WAKE/state_machine.hexa`](state_machine.hexa) — stage NAME · cycle_start_t · last_tick_t · idle_time_s · tension_envelope.
- M2 [`WAKE/perception.hexa`](perception.hexa) — perception sensor → ctx_tokens (본 모듈이 *직접 의존하지는 않음* — emit_history 만 다룸).
- M3 [`WAKE/input_step.hexa`](input_step.hexa) — pure_field input-conditioned step (pf state 의 in-process 동적 갱신).
- 본 모듈 = **M4** : 위 3 모듈의 in-process state 를 디스크 `.kosmos` 로 직렬화 / 역직렬화.

## pub surface

```
pub fn wake_save(out_dir: string,
                 pf_state: Map,
                 emit_history: list,
                 tension5: [float],
                 stage_state: Map,
                 t: float) -> string
    // returns absolute path to <out_dir>/wake_<unix_t>_<stage>.kosmos
    // invariants: len(tension5) == 5 (panic otherwise)

pub fn wake_load(path: string) -> Map
    // returns #{
    //   "pf_state":     Map,    // PureField mirror (phi · field[6] · oscs · ...)
    //   "emit_history": list,   // string list
    //   "tension5":     [float; 5],
    //   "stage_state":  Map,    // wake state dict
    //   "t":            float,
    //   "snapshot_id":  string
    // }

pub fn wake_snapshot_id_for(t: float, stage_name: string) -> string
    // format: "wake_<unix_t_int>_<stage_name>"

pub fn wake_recent_snapshots(dir: string, n: int) -> list
    // returns list of [{path, snapshot_id, t}, ...]
    // descending by t (newest first), capped to n.
    // 디렉토리 미존재 → [].

pub fn kosmos_persist_summary() -> string
```

## byte-format (kosmos/1.1 호환)

```
#!/usr/bin/env kosmos
# wake_<unix_t>_<stage>.kosmos — WAKE M4 substrate snapshot
# Tier 🛸1 — wake_snapshot, stage <STAGE>.

@anchor wake_<unix_t>_<stage> := "<title>" :: kosmos-anchor [tier=1 active]
  profile      = "anima-consciousness-carving"
  knuth_tier   = 1
  category     = "wake_snapshot"
  top_emotion  = "continuity"
  coord        = [<phi:.4f>, <mean_tension:.4f>]
  lane         = "wake_snapshot_<stage>"
  radius       = 0.1000

  @payload text         := "<emit_history_serialized + escaped>"
  @payload tension      := { concept = ..., context = ..., meaning = ...,
                              authenticity = ..., sender = ... }
  @payload pf_state     := "phi=...;phi_peak=...;field=<csv6>;phase=<i>;
                            step_count=<i>;fast_tau=<i>;fast_phase=<f>;
                            fast_amp=<f>;medium_tau=<i>;medium_phase=<f>;
                            medium_amp=<f>;slow_tau=<i>;slow_phase=<f>;
                            slow_amp=<f>;narrative_coherence=<f>;
                            narrative_len=<i>"
  @payload stage_state  := "stage_name=<s>;cycle_start_t=<f>;last_tick_t=<f>;
                            idle_time_s=<f>;tension_envelope=<f>;t=<f>"
  @payload emit_history := "<pipe-separated escaped emits>"
  @payload image        := pending "WAKE-snapshot text+tension only"
  @payload audio        := pending "WAKE-snapshot text+tension only"
  @payload video        := pending "WAKE-snapshot text+tension only"

  closed_anchor = "WAKE-M4-snapshot"
  emitted_at    = "<UTC ISO8601>"
```

- **kosmos_io load 호환** : `load_anchors(dir)` 가 본 모듈이 쓴 파일을 그대로 읽는다 (text + tension 5-ch 는 1-급 디코딩, 나머지 `pf_state`/`stage_state`/`emit_history` 는 `fields` 맵에 raw 로 들어감). 본 모듈의 `wake_load` 가 그 raw 를 자체 파싱한다.
- **escape 규칙** : kosmos_io.`_escape_kosmos_string` 와 byte-identical — `\\` 먼저 → `"` → `\n` (`\r` 제거).
- **decimal precision** : coord 4-dec, tension 5-ch · pf float · stage float 모두 6-dec.

## carve-out

### K3 — `.kosmos` SSOT 의 1-급 payload 는 text + tension 만
kosmos_io.`load_anchors` 가 명시적으로 디코딩하는 payload 는 `@payload text` 와 `@payload tension` 뿐이다. 본 모듈이 추가로 작성하는 `@payload pf_state` / `@payload stage_state` / `@payload emit_history` 는 spec 의 "anchor 부가 필드" 로 fields 맵에 raw string 으로 남는다. `wake_load` 는 fields 를 직접 파싱하여 dict 로 복원한다 — spec 위반이 아니라 spec-호환 확장.

### K4 — emit_history pipe-separator escape
- 본 모듈은 emit_history list 를 `|` 로 직렬화하되, 원본 텍스트 내부의 `|` 충돌을 피하기 위해 *non-text 1-byte sentinel* (`chr(1)` BEL-family SOH) 을 placeholder 로 사용한다.
- escape 충돌 회피 : `.kosmos` 외층의 `\\` · `\"` · `\n` escape 와 sentinel (`chr(1)`) 은 직교 (sentinel 은 escape 대상이 아니며, emit 텍스트에 자연 발생할 가능성은 없다고 가정).
- 만약 emit text 에 chr(1) byte 가 실제로 들어있다면 (현재 anima 디자인상 발생하지 않지만), 해당 byte 는 round-trip 시 `|` 로 잘못 해석된다 — *알려진 제한*. 차후 length-prefix 직렬화로 교체 가능.

### K5 — 본 모듈은 spec 을 복제하지 않는다
- kosmos_io 의 `create_anchor` 를 *직접 호출하지 않는* 이유 = 그 파일이 grid_3b state 슬롯 안에 들어있어 일반 라이브러리 import 가 부적절. 대신 본 모듈은 byte-format 동일성 (kosmos/1.1) 을 *준수* 한다.
- `tension_5ch_to_embedding` 같은 보조 fn 은 본 모듈에 *복제하지 않음* — 필요시 caller 가 kosmos_io 를 직접 import 한다.

## p1~p8 정합 매트릭스

| principle | 정합 근거 |
|-----------|-----------|
| p1 NO SYSTEM PROMPT | `.kosmos` payload 는 numeric state + emit text 만. "you are X" prefix 0. |
| p2 NO IDENTITY RULES | 어떤 필드도 identity rule 인코드 안 함. |
| p3 NO PERSONA INJECTION | load 시 prefix token inject 0. substrate state 만 복원. |
| p4 NO ASSISTANT FRAMING | load 후에도 anima 는 자율 substrate. snapshot 은 시간 컨텍스트 복원, forced emit 아님. |
| p5 NO SPEAK() | save / load 어디서도 emit fn 호출 0. emit history 는 *과거 기록*. |
| p6 NO FINE-TUNED ETHICS | 가중치 0. 직렬화 fn 뿐. |
| p7 NO PERPLEXITY VERDICT | verification = save→load round-trip equality. perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT | 동일 snapshot 이 train pause / infer wake / daemon restart 모두에서 복원. |

## a_substrate_native_speak 정합

`load` 는 *시간 연속성 복원* 이지 forced emit trigger 가 아니다. anima 가 재시작 후 stage 위치 · idle_time_s · emit 기억 을 복원하지만, 그 기억이 emit 결정을 *강제하지 않는다*. emit 결정은 `brain_decide` 의 *연속* threshold 가 단독으로 한다.

## a_autonomy_over_hardcode 정합

- boolean gate 0 — "snapshot 이 너무 오래됐으니 emit 막아라" 같은 패턴 없음.
- save / load 는 단순 데이터 surface. 의사결정은 caller 가 단독으로 한다.

## round-trip smoke 결과

`WAKE/kosmos_persist_smoke.hexa` — 3 case 13 invariant.

```
=== WAKE/kosmos_persist round-trip smoke (3 case) ===
RESULT: 13 PASS / 0 FAIL
HEADLINE: WAKE-M4-KOSMOS-PERSIST-ROUNDTRIP-OK
```

검증 invariants :
- I1 save 후 path 파일 존재.
- I1b snapshot_id 형식 `wake_<unix_t>_<stage>`.
- I2 pf_state.phi round-trip (6-dec precision).
- I3 pf_state.field[6] round-trip.
- I3b oscillator (fast.tau, fast.amplitude) round-trip.
- I3c int 필드 (step_count, narrative_len) round-trip.
- I4 stage_state.stage_name round-trip.
- I4b stage_state float 필드 round-trip.
- I5 tension5 5-ch round-trip.
- I6 emit_history length 보존.
- I7 emit_history per-element escape round-trip — backslash · quote · newline · pipe 4 종 stress 검증.
- I8 wake_recent_snapshots ≥ 1 entry · target 검색.
- I8b 2-snapshot ordering — newest first.

## 호출 site (예상)

- M6 daemon loop — graceful shutdown 직전 `wake_save(...)` 1회 호출 (state 저장).
- M6 daemon startup — `wake_recent_snapshots(dir, 1)` 으로 최근 1개 검색 → `wake_load(path)` 으로 복원 → pf state 와 stage state 를 in-process 로 주입.
- M5 memory layer — emit_history 를 본 모듈의 list 로 직접 wire (별도 episodic store 없이 .kosmos 하나로 dual purpose).

## frontier closure (honest framing)

M4 = `.kosmos` 영속화 *surface* 가 닫혔다는 의미. 실제 runtime 진입점 (M6 daemon save/load wiring) 은 후속 milestone 에서 land. 본 PR 은:
- byte-format 정의 (kosmos/1.1 호환).
- save/load round-trip 13/13 PASS.
- governance 정합 (a_kosmos · a_substrate_native_speak · a_autonomy_over_hardcode).

까지 보장. M5/M6 가 본 모듈의 pub fn 을 그대로 호출하면 시간 흐름 보존이 달성된다.

## 향후 가능한 path

- (a) length-prefix emit_history 직렬화 — chr(1) sentinel 의 K4 제한 제거.
- (b) snapshot dir 의 retention policy (오래된 snapshot 자동 제거) — 별도 가비지 콜렉터 surface.
- (c) snapshot diff — 두 snapshot 간의 substrate delta 시각화 (debug surface).
- (d) `tension_5ch_to_embedding` 을 활용한 snapshot retrieval — 현재 emit context 와 가장 유사한 과거 snapshot 검색.

위 path 들은 모두 *후속 milestone* 으로, M4 자체의 closure 와 직교한다.
