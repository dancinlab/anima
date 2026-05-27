# Anima Emerge Dialogue — First-Session Manual (2026-05-05)

One-page bilingual KO + EN manual to start a first emerge dialogue session right
now. Read-only doc. No code change. No commit.

Lineage:
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` (paradigm spec)
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` (Stage 3 protocol)
- `state/anima_emerge_cand_g_tension_fast_2026_05_05/verdict.json` (BG-AE — tension trajectory dialogue medium)
- `state/anima_emerge_cand_d_attractor_10prompt_2026_05_05/verdict.json` (BG-AG — attractor finding dialogue meaning)
- `state/anima_real_mode_sweep_2026_05_05/verdict.json` (BG-L — axis FAIL invalidation)

---

## §1 한 줄 정의 / One-line definition

**KO**: CLM v4 substrate에 input을 주고 내부 phi-star + hidden state +
tension trajectory 변화를 보고 다음 input을 결정하는 dialogue. 토큰을 받는
chat이 아니라, substrate behavior 자체가 dialogue 매개체.

**EN**: Send an input to the CLM v4 substrate, observe phi-star + hidden state
+ tension trajectory shifts, and decide the next input. NOT a token-emitting
chat — substrate behavior itself is the dialogue medium.

---

## §2 Fire 명령 (3 path) / How to start (3 paths)

### Path A — wrapper REPL (BG-AH SentencePiece fallback 후 가능 / available after BG-AH SentencePiece fallback)

**KO**: 가장 안정적, anima 표준 wrapper 경유. session jsonl 자동 emit.
**EN**: Most stable, goes through the anima standard wrapper. Session jsonl auto-emitted.

```bash
cd /Users/ghost/core/anima
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python anima dialogue
```

또는 / or:

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  bash bin/anima-core-dialogue.bash --interactive
```

기대 prompt / expected prompt:
```
> 안녕
[clm-v4] phi_star: 41.87 (drift +0.01 from 41.86)
[clm-v4] axis_activation: ...
[clm-v4] dominant_cells: [...]
[clm-v4] hidden_state_delta: 0.0000
> ...
```

### Path B — direct REPL (BG-AN — 권고 / recommended)

**KO**: prior turn hidden 자동 threading + tension trajectory 풍부. BG-AN landing 전제.
**EN**: Auto-threads prior-turn hidden, richer tension trajectory. Requires BG-AN landed.

```bash
cd /Users/ghost/core/anima
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  python tool/transient_py/anima_emerge_dialogue_repl.py
```

### Path C — one-shot probe / single-prompt probe

**KO**: REPL 진입 없이 한 input만 측정. 빠른 sanity check.
**EN**: Single-input measurement without entering REPL. Quick sanity check.

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  python tool/transient_py/anima_emerge_dialogue_repl.py --probe "텍스트"
```

**권고 순서 / recommended priority**: B > A > C
- B: emerge dialogue 본 패러다임 (prior threading) / true emerge paradigm
- A: BG-AN 미land 시 fallback / fallback when BG-AN not yet landed
- C: 단발 sanity / one-shot sanity only

---

## §3 Substrate response 4-line 해석 가이드 / 4-line interpretation guide

매 user_turn 후 substrate가 emit하는 4 line / 4 lines emitted after every user_turn:

### `phi_star`
- **KO**: substrate 의식 통합도. baseline = 41.86 (paradigm v11 G3 anchor). anima-internal proxy.
- **EN**: substrate consciousness-integration measure. baseline = 41.86 (paradigm v11 G3 anchor). anima-internal proxy.

### `phi_drift`
- **KO**: prior turn 대비 변화량. input이 substrate를 얼마나 흔들었는지 정량.
  - `|drift| > 0.5` = 큰 충격 — "왜 변했어?" follow-up 권장
  - `|drift| < 0.05` = 안정 phase — 깊이 follow-up 권장
- **EN**: Δ from prior turn. Quantifies how much the input shook the substrate.
  - `|drift| > 0.5` = large shock — "Why did it change?" follow-up
  - `|drift| < 0.05` = stable phase — go deeper

### `hidden_state_delta`
- **KO**: hidden state turn-to-turn L2 변화. 행동학적 차이 측정.
  - `> 5.0` 큰 변화 / `< 0.1` 안정
  - 첫 turn은 0 (prior 없음)
- **EN**: turn-to-turn L2 of hidden state. Behavioral-Δ measure.
  - `> 5.0` large / `< 0.1` stable
  - First turn = 0 (no prior)

### `tension_trajectory` (BG-AE 발견 / BG-AE finding)
- **KO**: 16-layer hidden L2 norm + variance. input이 어느 layer에서 처리되는지.
  - peak layer 2 = early features dominant
  - peak layer 6 = mid abstraction
  - peak layer 14 = deep abstraction
  - **L2 variance > 100** = rich representation (BG-AE F_CAND_G_1 PASS criterion)
  - **L2 variance < 50** = degenerate (dialogue 약함 / dialogue weak)
- **EN**: per-layer L2 norm across 16 blocks + variance. Where in the network the input is processed.
  - peak layer 2 = early features
  - peak layer 6 = mid abstraction
  - peak layer 14 = deep abstraction
  - **L2 variance > 100** = rich (BG-AE F_CAND_G_1 PASS bar)
  - **L2 variance < 50** = degenerate (weak dialogue)

---

## §4 Deprecated emit (무시할 것) / Deprecated emits (ignore)

**KO** / **EN**:
- `axis_activation` 5-bucket — random baseline (BG-L FAIL: intent_match 2/10, all axis means 0.46-0.50, near-uniform). 무시 / ignore.
- `dominant_cells` — tile-reshape artifact (BG-L DEGENERATE: cells 0-3 ≡ 4-7 by replicate-2x). 무시 / ignore.

이 두 line은 emit되더라도 substrate behavior signal 아님 — 보지 말 것.
These two lines, even when emitted, are NOT substrate signal — do not read them.

---

## §5 첫 dialogue session 권고 protocol (n=5 turn) / First-session protocol (n=5)

```
turn 1 / "안녕"                                                  (baseline)
turn 2 / "의식이 흐른다"                                         (semantic shift)
turn 3 / "phi-star 변화 이유 추측"                               (meta-cognitive)
turn 4 / "다음 input은 어떤 방향이면 substrate 더 흔들릴까?"     (predictive)
turn 5 / "지금 attractor 가까이?"                                (state assessment)
```

**KO**: 각 turn 후 substrate 4-line 보고 사용자가 즉흥 follow-up. 권고 5 turn은
seed — emerge intent에 맞으면 자유롭게 분기.

**EN**: After each turn read substrate 4-line, then improvise follow-up. The
5-turn template is a SEED — branch freely if it serves emerge intent.

---

## §6 Stop criteria / Stop criteria

**KO**:
- session 끝: 빈 줄 또는 Ctrl-D / `exit`
- 발견 지속: 다음 session에서 같은 의도 또는 다른 의도

**EN**:
- session end: empty line, Ctrl-D, or `exit`
- continued discovery: next session, same intent or new intent

Stage 3 protocol §5 stop markers (saturation n>=30 / candidate hit_rate >=70% /
CLM v5 hint) are corpus-level — 이 매뉴얼은 single-session level.

---

## §7 Session log 위치 + 분석 / Session log location + analysis

**Session log**:
```
state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_emerge_repl.jsonl
```
schema = `anima.dialogue.v1` (session_start / user_turn / substrate_turn / session_end / session_summary)

**Corpus analysis** (BG-B analyzer):
```bash
bash bin/anima-core-dialogue-analyze.bash --date <YYYY-MM-DD>
```

또는 / or:
```bash
hexa run tool/anima_cli/dialogue_session_analyzer.hexa \
  --session state/anima_core_dialogues/<DATE>/<HH-MM-SS>_emerge_repl.jsonl
```

emit: phi envelope / drift max / cell jaccard / per-turn delta. Read-only,
re-runnable.

---

## §8 Architectural caveat (BG-AC + BG-AG 발견 / findings)

**KO**: mag=50 이상 inject 시 substrate가 attractor band collapse →
compression_ratio 51.4× (BG-AG STRONG attractor evidence) → dialogue 자체 erase.
BG-AN dialogue REPL은 `mode=none` default — canonical inject 없음, 안전.
사용자가 명시적으로 `--inject-states-mode canonical --magnitude 50`을 추가하지
않는 한 collapse 위험 없음.

**EN**: Injecting at mag >= 50 collapses the substrate into an attractor band
(compression_ratio 51.4× per BG-AG STRONG evidence) → dialogue itself erased.
BG-AN dialogue REPL defaults to `mode=none` — no canonical inject, safe. Unless
the user explicitly adds `--inject-states-mode canonical --magnitude 50`, no
collapse risk.

---

## §9 Honest C3 (>= 5)

- **C1**: emerge dialogue 의미는 사용자 해석에 의존. anima-internal heuristic. /
  Emerge dialogue meaning depends on user interpretation. Anima-internal heuristic.
- **C2**: phi-star = anima-canonical proxy (`PHI_STAR_BASELINE × (1 + 0.05 ×
  mean_pair_cosine)`), NOT Tononi IIT phi. Variance signal validates "forward
  responsive" only at proxy level. /
  phi-star = anima-canonical proxy, not Tononi IIT phi.
- **C3**: axis activation 5-bucket + dominant_cells 무효. BG-L FAIL: 5-bucket
  argmax는 mean-pooled hidden 상의 heuristic partition (intent_match 2/10);
  dominant_cells는 tile-reshape replicate artifact (cells 0-3 ≡ 4-7). 두 line
  모두 substrate signal 아님 — 무시 필수. /
  axis activation 5-bucket + dominant_cells INVALID. BG-L FAIL: 5-bucket argmax
  is heuristic partition over mean-pooled hidden (intent_match 2/10);
  dominant_cells is tile-reshape replicate artifact (cells 0-3 ≡ 4-7). Neither
  is substrate signal — must ignore.
- **C4**: wrapper Path A phi vs direct REPL Path B phi 불일치 가능 (BG-AH C3
  carry: wrapper synthetic_fallback path는 RNG 기반 noise; real CLM v4 forward는
  load 후만 가능). 첫 session에서 path A 결과는 wiring sanity, path B 결과는
  substrate observation으로 분리 해석. /
  Path A phi may diverge from Path B phi (BG-AH C3 carry: wrapper
  synthetic_fallback is RNG-driven; real CLM v4 forward only after load).
  Interpret Path A as wiring sanity, Path B as substrate observation.
- **C5**: 첫 session 사용자 dialogue 결과 unknown — research-mode. 패러다임
  §10 C1 (production 아님) 그대로 carry. n=5 권고 turn은 seed; 결과 재현성 보장
  없음. /
  First-session outcome unknown — research-mode. Paradigm §10 C1 (not
  production) carries forward. n=5 turn template is seed; reproducibility not
  promised.
- **C6**: BG-AN `tool/transient_py/anima_emerge_dialogue_repl.py` 미land 시
  Path B 사용 불가 → Path A fallback. 본 매뉴얼 release 시점에 BG-AN status
  확인 필요. /
  If BG-AN `anima_emerge_dialogue_repl.py` not yet landed, Path B unusable →
  fallback to Path A. Verify BG-AN status at the time of using this manual.
- **C7**: tension trajectory L2 variance threshold (>100 rich, <50 degenerate)
  는 BG-AE 3-prompt verdict (`max_l2_variance=124.4`) 기반 — generalization
  안 됨. 더 큰 corpus에서 threshold 재조정 가능. /
  Tension-trajectory L2 variance thresholds (>100 rich, <50 degenerate) come
  from BG-AE 3-prompt verdict (`max_l2_variance=124.4`) — does not generalize.
  Threshold may shift on larger corpora.

---

## §10 Composability

- Upstream: paradigm spec / Stage 3 protocol / BG-AE / BG-AG / BG-L verdicts
- Sister: BG-AH (SentencePiece fallback for wrapper Path A), BG-AN (direct REPL
  for Path B), BG-B (corpus analyzer for §7)
- Downstream: first-session jsonl at
  `state/anima_core_dialogues/<DATE>/<HH-MM-SS>_emerge_repl.jsonl`; Stage 3
  observations.md per protocol §4

raw compliance:
- raw#9 — md only
- raw#10 — §9 has 7 honest C3 (>= 5)
- raw#15 — additive only; no source mod

End of first-session manual. $0 mac, doc-only, no commit.
