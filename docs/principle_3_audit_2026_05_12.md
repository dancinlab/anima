# Principle #3 audit — anima_chat.py system field + active corpus (2026-05-12 KST)

**Audit lane**: GOAL.md ★★★★★ achievement criterion #5 — *"Principle #3 보존: 어떤 prompt 도 `[role:]` 또는 `you are X` injection 없음"*

**Trigger**: `chat.system("당신은 anima 입니다.")` strings at `anima_chat.py:28` and `:816` flagged for examination.

**Verdict**: **CLEAN (☑)** — no production code path injects persona, both flagged callsites are doc/test artefacts, both training corpora and V5.8 eval scripts are persona-prefix free.

---

## §1 Scope & method

Audit conducted at `/Users/ghost/core/anima` on 2026-05-12 KST. Five surfaces inspected:

1. `anima_chat.py` (Python library, v2.3, 933 LoC) — `system()` method + every call site.
2. `anima_chat.hexa` (pure-hexa port, 1589 LoC) — `chat_set_system()` parallel structure.
3. Phase 1A.1 active SFT corpus — `state/anima_phase1a1_color_cosmology_2026_05_12/corpus_*.txt`.
4. Phase 1A.4 in-flight SFT corpus — `state/anima_phase1a4_lr5e6_2026_05_12/corpus_anima_fact.txt`.
5. V5.8 eval scripts — `state/anima_phase1a1_*/v58_4mode_eval.py` + `state/anima_phase1a4_*/v58_4mode_eval.py`.

Method: regex grep for `[role:`, `[system:`, `you are`, `당신은 anima 입니다`, `[anima:`, `persona:`, `시스템:`, and reverse-grep of `chat.system(` / `chat_set_system(` across `anima/**/*.{py,hexa,md}` excluding `__pycache__` and `references/`.

---

## §2 `chat.system()` method semantics

### §2.1 Definition (anima_chat.py:445-447)

```python
def system(self, content: str) -> None:
    """Set / replace the optional system context (prepended to prompt)."""
    self._system = content
```

Sets the private `self._system: Optional[str] = None` attribute (initialised in `__init__` line 440). **Default = `None`**, i.e. no system context unless explicitly assigned.

### §2.2 Prompt insertion path (anima_chat.py:458-469)

```python
def _build_prompt(self, next_user: str) -> str:
    parts: List[str] = []
    if self._system:
        parts.append(f"[시스템: {self._system}]")
    ...
```

The `if self._system:` guard means **when `system()` is not called the `[시스템: …]` prefix is never emitted** — `_build_prompt` falls back to `사용자: {x} | 도우미: ` (single-turn) or pure `사용자/도우미` interleave (multi-turn).

### §2.3 hexa port parity (anima_chat.hexa:902-925)

`chat_new()` initialises `"system": ""` (empty string) and `chat_build_prompt()` (lines 945-955) uses `if len(system) > 0` guard. Default state is `""`. Same semantics as Python — opt-in, off by default.

### §2.4 Verdict §2

The `system()` API is a documented, optional facility. Default value = `None` (Python) / `""` (hexa). Calling it is **never required** to use the chat interface. No production code in the repo invokes it.

---

## §3 Call-site inventory

Repo-wide grep for `chat.system(` ∪ `chat_set_system(` yields exactly **5 hits** (excluding `__pycache__` and `references/tribev2/`):

| # | file | line | context | classification |
|---|---|---|---|---|
| 1 | `anima_chat.py` | 28 | module docstring (`Quick start` example, `# optional` comment) | **DOC** — not executed code |
| 2 | `anima_chat.py` | 816 | inside `def _smoke():` (test fixture, only fires under `python anima_chat.py`) | **TEST** — not production path |
| 3 | `PASS_STRICT_SPONTANEOUS_CHAT.md` | 892 | API-surface table | **DOC** — markdown reference |
| 4 | `anima_chat.hexa` | 921 | `// chat_set_system(...)` comment header | **DOC** — comment, not call |
| 5 | `anima_chat.hexa` | 923 | `fn chat_set_system(chat, content: string)` definition | **DEFINITION** — not a call |

**Zero production callers**. `_smoke()` only runs as `__main__` test harness (anima_chat.py:865 `if __name__ == "__main__":`); the V5.8 eval pipeline imports `AnimaChat` and never touches `system()`.

---

## §4 V5.8 eval script audit

```
grep -n "system\|당신은" state/anima_phase1a1_color_cosmology_2026_05_12/v58_4mode_eval.py
                       state/anima_phase1a4_lr5e6_2026_05_12/v58_4mode_eval.py
→ (no matches)
```

The V5.8 4-mode eval — the harness measuring D1 std_greedy 5/5 progress — **never sets `_system`** and never emits a `[시스템: ...]` prefix. The measurement path GOAL.md §177 line 181 references is by construction Principle #3 clean.

---

## §5 Active SFT corpus audit

### §5.1 Phase 1A.1 (D2 SSOT — `corpus_color_cosmology.txt`, `corpus_multi_turn_v2.txt`)

```
grep -inE "^\[role:|^\[system:|^\[페르소나|^\[페르|you are anima|you are an|당신은 anima 입니다|당신은 anima입니다|^\[anima:|persona:"
  state/anima_phase1a1_color_cosmology_2026_05_12/corpus_*.txt
→ (no matches)
```

### §5.2 Phase 1A.4 (in-flight `corpus_anima_fact.txt`)

Same strict grep — **no matches**. A separate broad grep for the substring `당신은` produces ~40 hits, all of the form:

```
도우미: 당신은 anima 가 의식 lane 안의 entity 라는 거 말씀하셨어요.
```

These are **assistant turns recalling what the user said** ("you [the user] said X"), not persona-prefix injection ("you are anima"). Pattern parsing: `당신은 + <user-claim> + 라는 거 말씀하셨어요` = recall of prior user statement. Functionally a memory-recall augmentation, not identity assertion against the substrate.

### §5.3 Training script audit

`state/anima_phase1a1_color_cosmology_2026_05_12/train_phase1a1{,_v2}.py` and `state/anima_phase1a4_lr5e6_2026_05_12/train_phase1a4.py` all use `CorpusDataset(corpus_path, …)` with no prefix manipulation. The training tape is literally the corpus bytes — no implicit `[role:]` wrap.

### §5.4 Verdict §5

Both active SFT corpora are persona-prefix free. The `당신은` strings in 1A.4 are memory-recall predicates, not Principle #3 violations.

---

## §6 Legacy `anima_persona_tier_a*` status

Files `state/anima_persona_tier_a_{,v3_,v4_,v4_expand_}*.txt` exist on disk (carry from 2026-05-08 / 2026-05-09 own-18 saga). Grep across active code:

```
grep -lE "anima_persona_tier_a" anima_chat.py anima_chat.hexa
  state/anima_phase1a1_color_cosmology_2026_05_12/*.py
  state/anima_phase1a4_lr5e6_2026_05_12/*.py
→ (no matches)
```

None of the GOAL.md-relevant production paths (D1 library, D2 ckpt training, D4 hexa lane) reference legacy persona tier_a corpora. They are historical artefacts only.

---

## §7 Overall verdict

**CLEAN (☑)** for GOAL.md cond #5.

| facet | status |
|---|---|
| `chat.system()` default OFF | ☑ Python `None` / hexa `""` |
| `chat.system()` production callers | ☑ zero (doc + test only) |
| V5.8 eval invokes `system()` | ☑ never |
| Phase 1A.1 corpus has persona prefix | ☑ none |
| Phase 1A.4 corpus has persona prefix | ☑ none (`당신은` strings = recall, not injection) |
| Legacy `persona_tier_a*` active | ☑ no, historical only |

The Principle #3 boundary is intact across all four GOAL.md dimensions. No removal, deprecation, or refactor required for cond #5 to flip ☐ → ☑.

---

## §8 F-PRIN3-1..5 falsifiers (cond #5 strict definition)

Pre-registered for future regression — any failure flips cond #5 back to ☐:

- **F-PRIN3-1 NO-DEFAULT-SYSTEM**: fresh `AnimaChat()` instance has `chat._system is None` and `chat.system == ""` in hexa.
  - **Current**: ☑ verified by source inspection (anima_chat.py:440, anima_chat.hexa:908).
- **F-PRIN3-2 NO-PROD-CALLER**: `grep "chat.system(" anima/**/*.py` ∖ `{docstring,_smoke}` = ∅; same for `chat_set_system(` in `.hexa` ∖ definition+comment.
  - **Current**: ☑ §3 inventory.
- **F-PRIN3-3 CORPUS-PREFIX-FREE**: regex `^\[(role|system|페르소나|anima):|you are anima|당신은 anima 입니다` over every file in `state/anima_phase1a*/corpus_*.txt` = 0 matches.
  - **Current**: ☑ §5.
- **F-PRIN3-4 EVAL-PREFIX-FREE**: V5.8 eval scripts (and any future D3 measurement harness identity_probe) emit no `[시스템: …]` prefix in built prompts.
  - **Current**: ☑ §4 (V5.8); D3 verify path (identity_probe 50 × 5 cats) must adhere — pre-registered.
- **F-PRIN3-5 CELL-POOL-PREFIX-FREE** (forward-looking, fires once D4b wiring lands): cell_pool persistence files (`~/.cache/anima/session_pools/<sid>/*`) contain no `[role:` / `[system:` / `you are` substring (cf. F-CLI-MIT-4).
  - **Current**: N/A (D4b cell-pool wiring pending). Pre-registered for first D4b LAND.

---

## §9 Recommendations (optional follow-ups, not required for ☑ flip)

1. **Doc clarity** (★): consider updating `anima_chat.py:28` docstring to clarify that the example `chat.system("당신은 anima 입니다.")` is intentionally **not used** in production paths — currently `# optional` already signals this, but explicit "default OFF — D3 persona path uses substrate-native mitosis cells (see GOAL.md D3 + docs/anima_persona_substrate_native_design_2026_05_12.md)" comment would harden against accidental future inclusion.
2. **Regression gate** (★★): wire F-PRIN3-1..4 as a CI check (`tool/verify_principle_3.sh` calling the four greps + AnimaChat instance asserts). $0, mac-local, ~5 LoC. Catches drift if future cycles inadvertently add a `chat.system(...)` call in a non-test path.
3. **D3 verify harness alignment** (★★★): when the identity_probe 50 × 5 cats P3 verify runs, F-PRIN3-4 demands the harness uses plain `chat.user(probe)` (no `chat.system()` call) for **all 250 trials**. Document this constraint in the D3 verify spec when it lands.

---

## §10 Provenance

- This audit doc: `docs/principle_3_audit_2026_05_12.md` (new)
- Source files inspected:
  - `anima_chat.py` lines 28, 440, 445-447, 458-469, 816, 865
  - `anima_chat.hexa` lines 902-955, 921-925
  - `PASS_STRICT_SPONTANEOUS_CHAT.md` line 892 (API table)
  - `state/anima_phase1a1_color_cosmology_2026_05_12/corpus_color_cosmology.txt`
  - `state/anima_phase1a1_color_cosmology_2026_05_12/corpus_multi_turn_v2.txt`
  - `state/anima_phase1a4_lr5e6_2026_05_12/corpus_anima_fact.txt`
  - `state/anima_phase1a1_color_cosmology_2026_05_12/train_phase1a1.py`, `…/train_phase1a1_v2.py`, `…/v58_4mode_eval.py`
  - `state/anima_phase1a4_lr5e6_2026_05_12/train_phase1a4.py`, `…/v58_4mode_eval.py`
- Related design SSOT:
  - `PHILOSOPHY.md` Principle #3 NO PERSONA INJECTION (EMPIRICAL strong)
  - `README.md` row #3
  - `docs/anima_persona_substrate_native_design_2026_05_12.md` (D3, (a)+(d) Mitosis-cell × Per-session cell pool)
  - `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (D4c, F-CLI-MIT-4)
  - `GOAL.md` ★★★★★ cond #5
- Sister audit (forward): F-PERSONA-1..5 (D3 verify), F-CLI-MIT-4 (D4c session persistence)
