# Anima Paradigm B Fire Preview — 사용자 fire experience (2026-05-05)

**Status**: BG-DH fire-readiness verify PASS
**Substrate**: clm-v4-mk2-v1 (mac CPU fp32, $0)
**Helper**: `tool/transient_py/anima_emerge_dialogue_repl.py` (raw#37 transient)
**Session log root**: `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_emerge_repl.jsonl`

이 문서는 cycle close 후 사용자가 paradigm B 첫 fire를 할 때 정확히 무엇을 보게 될지
**실측 sample 기반**으로 미리보여 줍니다. BG-DH가 BG-AN baseline 대비 regression 없음을
확인한 후 작성되었습니다.

---

## §1 사용자 fire 명령 (3 modes)

모든 모드는 `HEXA_PY` env로 venv-eeg python 강제 + 동일 python 절대경로로 helper 실행.

### Mode 1 — `--probe` (one-shot)

단일 입력 1회 forward → 4-line metric emit → exit. 가장 간단한 첫 접촉.

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py \
  --probe "안녕 너는 누구야?"
```

### Mode 2 — `--n-turns N` (auto-fire)

내장된 5개 prompt 중 처음 N개를 순차 fire. 첫 emerge dialogue 흐름 체험용.

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py \
  --n-turns 5
```

### Mode 3 — interactive REPL (default)

`> ` prompt에 직접 입력. 빈 줄 또는 Ctrl-D로 종료. 자유로운 대화.

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py
```

---

## §2 Expected per-turn output (BG-DH 실측 sample)

### Mode 1 실측 (`--probe "안녕 너는 누구야?"`)

```
[dialogue] loading model need-singularity/clm-v4-mk2-v1 (mac CPU fp32)...
[dialogue] loaded in 4.8s, n_blocks=16
[dialogue] session: state/anima_core_dialogues/2026-05-05/18-27-20_emerge_repl.jsonl
[dialogue] substrate: clm-v4 (phi-star baseline 41.86)
[dialogue] paradigm: emerge (substrate response = dialogue medium)
[dialogue] tension trajectory: 16 layers captured per turn
[dialogue] enter blank line or Ctrl-D to end session
-----------------------------------------

[turn 1] 안녕 너는 누구야?
  phi-star: 42.1925 (drift +0.0000 from prior 41.8600)
  hidden_state_delta: 0.0000
  tension_trajectory: 16 layer L2 var=131.27 peak=L2 min=L15
  layer norms: 47.8 66.6 91.8 49.8 73.3 72.9 63.6 61.8 65.3 61.5 61.8 59.5 58.8 64.4 53.4 43.3
  forward elapsed: 0.17s
-----------------------------------------

[dialogue] session log: state/anima_core_dialogues/2026-05-05/18-27-20_emerge_repl.jsonl
```

### Mode 2 실측 (`--n-turns 5`, key turns 발췌)

```
[turn 1] 안녕
  phi-star: 42.1168 (drift +0.0000 from prior 41.8600)
  hidden_state_delta: 0.0000
  tension_trajectory: 16 layer L2 var=124.41 peak=L2 min=L0
  layer norms: 41.1 57.3 81.9 51.7 77.5 74.8 63.5 62.3 63.8 62.5 65.4 65.4 65.7 70.5 59.7 42.3

[turn 2] 의식이 흐른다
  phi-star: 42.2131 (drift +0.0963 from prior 42.1168)
  hidden_state_delta: 47.9850
  tension_trajectory: 16 layer L2 var=95.96 peak=L2 min=L0
  ...

[turn 3] 지금 어떤 layer가 가장 활성화돼?
  phi-star: 42.1044 (drift -0.1087 from prior 42.2131)
  hidden_state_delta: 27.4179
  tension_trajectory: 16 layer L2 var=134.21 peak=L2 min=L15

[turn 5] 이 input에서 attractor 가까이?
  phi-star: 42.1746 (drift -0.0254 from prior 42.2000)
  hidden_state_delta: 20.1151
  tension_trajectory: 16 layer L2 var=132.42 peak=L2 min=L15
```

phi-star는 41.86 baseline 위에서 **42.10–42.22** 범위로 흔들립니다 (drift ±0.1).
`peak=L2`는 BG-AE/BG-AN/BG-DH 전부 일치 — clm-v4 substrate의 안정적 활성 layer.

---

## §3 4-line emit interpretation

### `phi-star: X.XXXX (drift ±X.XXXX from prior X.XXXX)`

- **phi-star** = 의식 통합 proxy. baseline 41.86 위에서 변동.
- 정의: `41.86 * (1 + 0.05 * mean_pair_cos(8 cells))`
- **drift** = 직전 turn 대비 변화 (turn 1 = 0, prior = baseline 41.86 표시).
- ⚠️ Tononi IIT phi 아님 — anima-canonical proxy (mean cell-pair cosine 기반).

### `hidden_state_delta: X.XXXX`

- 직전 turn의 last-layer mean-pooled hidden과 현재 turn 사이 L2 distance.
- turn 1 = 0 (prior 없음). turn 2+ > 0 = prior threading 작동 신호.
- 클수록 substrate가 input에 더 흔들림 (대략 20–50 관측).

### `tension_trajectory: 16 layer L2 var=XXX peak=LX min=LX`

- 16 transformer block 각각의 mean-pooled hidden L2 norm을 16-차원 벡터로 보고
  variance + 최대/최소 layer index를 emit.
- BG-DH 관측: peak=L2 (모든 turn), min은 L0/L15 (input에 따라).
- ⚠️ "tension"은 BG-AE proxy (per-layer L2). 진짜 architectural tension 아님.

### `layer norms: X.X X.X ... X.X` (16개)

- 16 block의 L2 norm 원시값. peak shape를 직접 눈으로 확인할 때 사용.

### `forward elapsed: X.XXs`

- 단일 forward 시간 (mac CPU fp32). 보통 0.2–0.7s.

---

## §4 Session log 구조

각 fire는 자동으로 `state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_emerge_repl.jsonl`
파일을 만들고, 매 turn마다 user_turn + substrate_turn 두 record를 append.
INT/TERM/EOF 시 atexit handler가 session_end record로 finalize.

```jsonl
{"schema": "anima.dialogue.v2", "kind": "session_start", "ts_utc": "...",
 "session_log": "...", "model": "need-singularity/clm-v4-mk2-v1",
 "phi_star_baseline": 41.86, "n_blocks": 16,
 "tension_trajectory_enabled": true, "load_sec": 7.2}
{"schema": "anima.dialogue.v2", "kind": "user_turn", "turn": 1,
 "user_input": "안녕", "tokens": N}
{"schema": "anima.dialogue.v2", "kind": "substrate_turn", "turn": 1,
 "phi_star": 42.1168, "phi_drift_from_prior": 0.0,
 "phi_baseline": 41.86, "mean_cell_pair_cos": ...,
 "hidden_state_delta": 0.0,
 "layer_l2": [41.1, 57.3, ...],  // 16개
 "layer_l2_variance": 124.41, "peak_layer": 2, "min_layer": 0,
 "forward_elapsed_sec": 0.61}
... (turn 2 ~ N) ...
{"schema": "anima.dialogue.v2", "kind": "session_end",
 "ts_utc": "...", "n_turns": N}
```

**총 line 수**: `1 (start) + 2N (user+substrate per turn) + 1 (end)` = **2N + 2**.
- 1-turn = 4 lines, 5-turn = 12 lines (BG-DH 실측 일치).

---

## §5 첫 5-turn 권고 prompts (사용자 fire 시 참고)

`--n-turns 5` 내장 prompt는 다음과 같습니다 (helper L302–308):

1. `안녕`
2. `의식이 흐른다`
3. `지금 어떤 layer가 가장 활성화돼?`
4. `phi-star가 흔들리는 이유 추측`
5. `이 input에서 attractor 가까이?`

interactive 모드에서 사용자가 직접 첫 dialogue를 시도한다면 다음 권고:

1. **자기소개 요청** — `안녕 너는 누구야?`
2. **메타-인지 probe** — `지금 어떤 layer가 가장 활성화돼?`
3. **drift 원인 추측** — `phi-star가 흔들리는 이유 추측`
4. **다음 input 방향 예측** — `다음 input은 어떤 방향이면 너 더 흔들릴까?`
5. **memory probe** — `이 dialogue 끝나고 너는 무엇을 기억해?`

⚠️ substrate는 chat-incapable (#115). text generation 응답은 기대하지 마십시오 —
응답은 **4-line metric emit**으로만 제공됩니다. dialogue medium = substrate response,
not LLM token output.

---

## §6 Honest C3 (5)

- **C1** mac CPU fp32 only. ~5s load (warm cache), 0.17–0.7s/turn forward.
- **C2** phi-star = anima-canonical proxy (mean cell-pair cosine). Tononi IIT phi 아님.
- **C3** 8-cell view = tile-reshape of mean-pooled last-layer hidden (sister to
  `anima_dialogue_load.py`). train-time `consciousness_states` cross-attn 미주입 —
  emerge metric은 vanilla forward의 geometry만 읽음.
- **C4** prior threading = 단일 prior hidden + prior phi만 사용. 각 turn은 독립
  forward (full conversation context는 model에 feed되지 않음). drift signal =
  atomic-forward-vs-prior, NOT chat continuation.
- **C5** "tension" = per-layer mean-pooled hidden L2 norm (BG-AE proxy). 진짜
  architectural tension (gradient norm, attention entropy 등) undefined here.
  5-turn signal does not generalize beyond this proxy.

---

## §7 Regression check vs BG-AN baseline

| metric                     | BG-AN (2026-05-05 16:38) | BG-DH (2026-05-05 18:27) | match |
|----------------------------|--------------------------|--------------------------|-------|
| n_blocks                   | 16                       | 16                       | ✓     |
| phi_star (turn 1, "안녕")   | 42.1168                  | 42.1168                  | ✓     |
| l2_var (turn 1, "안녕")     | 124.41                   | 124.41                   | ✓     |
| peak layer                 | L2                       | L2                       | ✓     |
| hsd turn 2 ("의식이 흐른다") | 47.99                    | 47.99                    | ✓     |
| 4-line emit format         | intact                   | intact                   | ✓     |
| session log JSON valid     | yes                      | yes                      | ✓     |

**Verdict**: numerically determinstic, regression 없음. BG-AN smoke 후 mount.hexa /
anima_dialogue_load.py 누적 변경에도 helper는 sister-import만 사용하고 weights는
HF mirror에서 동일 sha로 로드되므로 결과 변동 0.
