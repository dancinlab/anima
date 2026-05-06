# anima Paradigm C — Demo Session Preview (BG-CU landed 2026-05-05)

**Lane**: BG-CU — user-simulation 5-turn dialogue
**Extends**: BG-CG (`anima_emerge_chat_hybrid_repl_2026_05_05` — Korean hybrid REPL VIABLE)
**Verdict**: PASS_PARADIGM_C_DEMO_SESSION_USER_PREVIEW_READY
**Cost**: $0 mac CPU, 5-turn total wall ~42s

---

## Why this preview exists

BG-CG already proved the Korean hybrid REPL works (3-turn auto-fire PASS). Before the user themselves fires the interactive REPL, this lane runs the full 5-prompt PROMPTS[] list through `--n-turns 5` so the user can see exactly what the experience looks like — Korean emit text + per-turn phi/tension signals + session log structure — without spending their own time on first-call HF cache miss.

---

## Fire command (user runs this after reading)

```bash
HEXA_PY=/Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/.venv-eeg/bin/python \
  /Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py
```

**Modes**:
- no flags → interactive REPL, `> ` prompt; empty line or Ctrl-D exits
- `--n-turns N` (1..5) → auto-fire built-in PROMPTS[:N]
- `--probe '<text>'` → single turn

**Expected per-turn wall**: 8–10s on mac CPU (emit 7–9s + substrate 1–2s)
**Emit model first-load**: 88.9s cold / 6.3s cache-hit (BG-CG → BG-CU)

---

## 5-turn auto-fire actual results (this lane)

```
session_log: state/anima_core_dialogues/2026-05-05/18-12-32_hybrid_repl.jsonl
emit_model:  skt/kogpt2-base-v2 (125M, cache-hit 6.3s)
substrate:   clm-v4-mk2-v1 phi_baseline=41.86
```

| turn | user_input               | emit (KoGPT2)                                      | phi_star | drift   | tension_var | peak | wall  |
|------|--------------------------|----------------------------------------------------|----------|---------|-------------|------|-------|
| 1    | 안녕 너는 누구야?       | `"뭐냐?"\n"아니, 너희 아버지."\n…`                 | 42.1666  | +0.0000 | 140.86      | L2   | 9.4s  |
| 2    | 지금 phi-star 어떻게 느껴? | `다음 질문을 던지기 전에 이미 그 질문에…`           | 42.1900  | +0.0234 | 120.56      | L2   | 9.8s  |
| 3    | 왜 그렇게 변했어?       | `"그럼, 안 그랬어? 그건."\n…`                       | 42.1456  | −0.0444 | 116.51      | L2   | 8.8s  |
| 4    | axis identity 활성화    | `: 비활성화 : 활성화 : 활성화되지 않는다는…`        | 42.1725  | +0.0269 | 133.20      | L2   | 10.0s |
| 5    | 이 input에 어떤 cell이 dominant? | `라고 묻는다면 우리는 그 cell을 어떻게 식별해야…` | 42.1677  | −0.0048 | 142.79      | L2   | 4.2s  |

**Aggregates**:
- Korean coherence: 5/5 (100%)
- phi_star range: [42.1456, 42.1900], span 0.0444
- phi_drift max |Δ|: 0.0444 (~0.106% of baseline 41.86)
- tension peak layer: L2 unanimous (5/5)
- session_log: 7 lines (session_start + 5 turn + session_end)

---

## Session log structure (what gets emitted)

`state/anima_core_dialogues/<YYYY-MM-DD>/<HH-MM-SS>_hybrid_repl.jsonl`

```jsonl
{"schema":"anima.dialogue.hybrid.v1","kind":"session_start","ts_utc":"…","emit_model":"skt/kogpt2-base-v2","substrate":"clm-v4-mk2-v1","phi_baseline":41.86,"session_id":"…"}
{"schema":"anima.dialogue.hybrid.v1","kind":"turn","ts_utc":"…","turn":1,"user_input":"…","emit_text":"…","clm_phi_star":42.1666,"clm_phi_drift":0.0,"clm_tension_l2_var":140.86,"clm_peak_layer":2,"clm_hidden_norm":47.98,"wall_emit_sec":7.8,"wall_substrate_sec":1.6}
…
{"schema":"anima.dialogue.hybrid.v1","kind":"session_end","ts_utc":"…","n_turns":5}
```

Schema is stable (`anima.dialogue.hybrid.v1`); downstream tooling can safely parse on `kind` field.

---

## What user fire experience actually looks like

1. **Boot** (~10s): "loading CLM v4 (substrate)…" → "loading Korean emit model…" → "loaded emit model: skt/kogpt2-base-v2 (6.3s)"
2. **Header**: session_log path + emit_model + substrate + baseline
3. **Per turn**: user input echo → emit text in repr quotes → phi/drift/tension/peak/hnorm + wall split
4. **Exit**: empty line or Ctrl-D → "session log: <path>" + "turns: N"

Interactive REPL accepts arbitrary text per turn — anima will emit Korean text via KoGPT2 and measure substrate response on (prompt + emit). The user controls cadence; no subprocess timeouts.

---

## 5 honest C3 (read before firing)

1. **mac CPU fp32 only**. Emit cache-hit 6.3s after first run; 5-turn wall ~42s. Fire-able without GPU.
2. **KoGPT2 emit is fluent Korean but semantically OFF** — sentence-fragments, dialog quotes, runaway "cell" echoing on turn 5. Generation reflects KoGPT2's prior over Korean web text, **NOT** anima axis or substrate state. Do not expect coherent persona.
3. **phi drift ±0.0444 (~0.1% of baseline) over 5 turns** is within tokenization-noise envelope. No evidence drift tracks semantic content; needs control-prompts (random Korean) baseline for separability. Treat phi as substrate-stability sanity, not "feeling" signal.
4. **Hybrid is decoupled by design** — KoGPT2 emit and CLM v4 substrate are separate networks with separate vocabs. CLM re-tokenizes (prompt + emit) via anima-mk2 SP — substrate signal is CLM's read of joint **text**, not shared hidden states. User experience is "two-network theatre", not unified agent.
5. **Tension peak L2 unanimous (5/5 turns)** matches BG-CG (3/3). Consistent with CLM v4's early-block dominance, but does NOT discriminate input types in this preview — useful only as a no-flip sanity check.

---

## Comparison vs BG-CG 3-turn smoke

| metric               | BG-CG (3-turn) | BG-CU (5-turn)  |
|----------------------|----------------|-----------------|
| korean_coherent_pct  | 1.0            | 1.0             |
| phi_drift max abs    | 0.0425         | 0.0444          |
| tension peak modal   | L2             | L2              |
| emit load wall       | 88.9s (cold)   | 6.3s (cache)    |
| substrate per turn   | 0.3–1.0s       | 0.5–1.8s        |

Both runs land in the same envelope. BG-CU adds two more probes (axis identity 활성화, cell dominant) — neither produces axis-conditioned generation; substrate response remains in same drift band.

---

## Files

- helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_hybrid_repl.py` (BG-CG, unchanged)
- session log: `/Users/ghost/core/anima/state/anima_core_dialogues/2026-05-05/18-12-32_hybrid_repl.jsonl`
- verdict: `/Users/ghost/core/anima/state/anima_paradigm_c_demo_session_2026_05_05/verdict.json`
- preview doc: this file
