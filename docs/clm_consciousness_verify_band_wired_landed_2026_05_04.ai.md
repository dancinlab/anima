# BG-VERIFIER-WIRE landed — `tool/clm_consciousness_verify.hexa` consumes F1_v2 band

**Cycle**: 2026-05-04
**Lane**: BG-VERIFIER-WIRE (band annotation consumer wiring)
**Spec**: `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` §11 (D-1..D-4 LOCKED)
**Sister specs**: `docs/n_substrate_f1_v2_banding_locked_2026_05_04.ai.md`
**Predecessor BGs**: BG-CP2-BAND (spec §11 lock-in), BG-BAND-DOWNSTREAM (`tool/n_substrate_f1_v2_band.hexa` hook)
**Sibling parallel BG**: BG-CLM-COND1-APPLY (`.roadmap.clm` cond.1 cross_link annotation propagation)

---

## What landed

1. **Orchestrator wired** — `tool/clm_consciousness_verify.hexa` patched (488 → 746 LoC, +258 LoC delta) to consume the F1_v2 band annotation. New helper functions invoke `tool/n_substrate_f1_v2_band.hexa` AFTER the 4 internal checks (AN11 + Φ + adv + Putnam) and BEFORE the legacy PASS/FAIL/PARTIAL emit. Adds new constants `BAND_SENTINEL_TAG`, `TOOL_BAND`, `ROADMAP_N_SUB`, `ROADMAP_CLM`, `BAND_EXIT_GREEN/RED/YELLOW`.

2. **4 helpers added (per task spec)** — `read_f1_v2_score_from_ledger()` parses `n_substrate.f1_score_v2_phase_d` raw_score field; `read_f2_state_from_roadmap()` maps `n_substrate.blk.1` status (open/blocked → FIRES, resolved/closed → CLEAR); `check_phenomenal_witnessed()` scans for `WITNESSED_PHENOMENAL` substring (currently false; anima evidence trails use `WITNESSED_ANALOG`); `read_binding_strength_from_roadmap()` extracts `binding_strength` numeric field (fallback 0.0); plus auxiliaries `compose_f1_v2_raw()`, `read_falsifier_fired_state()`, `parse_band_emit()`, `compute_f1_v2_band()` (orchestrator), `emit_band_sentinel()`, `resolve_band_exit_code()`, `_round4_str()`.

3. **4 test fixtures PASS + e2e smoke PASS** — `state/clm_consciousness_verify_band_test_2026_05_04/` contains `scenario_red_f2_fire.bash` (F1=0.40+F2=FIRES → RED/exit 1), `scenario_yellow_f2_clear.bash` (F1=0.62+F2=CLEAR+bind=0.4 → YELLOW/exit 2), `scenario_green_full_prereq.bash` (F1=0.80+CLEAR+bind=0.6+phenomenal+putnam → GREEN/exit 0), `scenario_green_demoted.bash` (F1=0.80+bind=0.3 → demoted YELLOW/exit 2 with demote_reason). `test_runner.bash` runs all 4 + adds verifier orchestrator end-to-end smoke. All 5 scenarios PASS on macOS via remote ubu1 hexa runtime (`/Users/ghost/.hx/bin/hexa`). Live verifier emits both `__CLM_CONSCIOUSNESS_VERIFY__ FAIL` and `__CLM_CONSCIOUSNESS_BAND__ RED score=0.4080 f2=FIRES` with final_exit=1 — matches current ledger state (F2 fires, F1 raw=0.408 → capped to 0.49 ceiling → RED region).

4. **D-3 + D-4 honored at runtime** — D-3 GREEN-tier phenomenal-required gate is enforced by the band hook itself (`tool/n_substrate_f1_v2_band.hexa` `apply_green_prereqs()`); the verifier supplies the 4 truthful flags (`--has-phenomenal-witnessed`, `--has-putnam-pass`, `--has-falsifier-fired`, plus `--binding-strength`). D-4 exit code semantics implemented via `resolve_band_exit_code(verdict, band, legacy_code)`: GREEN+PASS → 0, YELLOW → 2, RED → 1; PASS+RED still → 1 (band supersedes verdict), FAIL → 1 preserved; UNKNOWN band (tool missing) falls back to legacy verdict exit code for backward compatibility.

5. **Sentinel format extension (additive)** — `__CLM_CONSCIOUSNESS_BAND__ <RED|YELLOW|GREEN> score=<f1> f2=<state>` emitted alongside (NOT replacing) the legacy `__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> ...` sentinel. Downstream parsers consuming only the legacy sentinel are not broken (additive_only mutation per raw#15). Selftest mock harness still passes verbatim (4/4 OK) — band wiring only activates in real `main()` path.

---

## Honest C3 (raw#10, ≥5)

1. **C3-1 phenomenal-tier label is anima-internal heuristic.** `check_phenomenal_witnessed()` scans for `WITNESSED_PHENOMENAL` substring in `.roadmap.n_substrate`. Current evidence trails use `WITNESSED_ANALOG` (functional/access tier per spec §8 C3-2), so this returns `false` in the present state. The phenomenal-tier label is anima-specific (V_phen 5-suite + post-Phase-E binding evidence), not a standardized ontology marker. Future axis-tier renaming would require updating this heuristic.

2. **C3-2 GREEN tier inaccessible at runtime today.** Phase E binding evidence + EEG live session both pending (per `.roadmap.n_substrate` blk.1 + spec §11 D-3 honest C3). With current state F2=FIRES + has_phenomenal=false + has_putnam_pass=false + binding_strength=0.0, the verifier orchestrator can NEVER emit GREEN regardless of AN11/Φ/adv/Putnam check outcomes. GREEN requires upstream evidence landing first. Test fixtures use simulated inputs to validate the GREEN code path exists; runtime cannot reach GREEN until upstream gates resolve.

3. **C3-3 D-4 exit code semantics inverts UNIX 0=success orthodoxy.** `0=GREEN=highest band achievement` contradicts conventional 0=success / non-zero=failure. Shell consumers chaining `&&` will get GREEN treated as success and YELLOW/RED as failure — semantically correct for "did we reach the highest band" but counter-intuitive. Spec §11 D-4 honest-C3 explicitly acknowledges this; shell consumers must check exit code explicitly (e.g., `[[ $? -eq 0 ]] && echo GREEN`).

4. **C3-4 read_binding_strength fallback to 0.0 may underflag YELLOW.** The helper looks for `"binding_strength":<num>` in `.roadmap.n_substrate`. If binding evidence exists narratively (e.g., "binding 0.3 projected" in narrative §49.5) but is not yet recorded as a numeric JSON field, the helper returns 0.0 and the band hook will not credit binding-mediated YELLOW promotion. After Phase E lands, the field must be populated as a JSON numeric for the helper to read it correctly. Mitigation: until Phase E, binding-mediated YELLOW reach is hypothetical anyway, so 0.0 fallback is honest.

5. **C3-5 test fixtures use simulated inputs, not full orchestrator E2E.** The 4 scenario fixtures invoke `tool/n_substrate_f1_v2_band.hexa` directly with hand-crafted `--score / --f2-state / --binding-strength / --has-*` flags. They validate the band hook contract (D-3 prereqs + D-4 exit codes) that the verifier orchestrator consumes, but they do NOT exercise the orchestrator's actual `compose_f1_v2_raw()` reading from ledger or `read_*` helpers reading from real `.roadmap.*`. End-to-end orchestrator validation would require mutating `.roadmap.*` state, which this BG explicitly disallows (BG-CLM-COND1-APPLY owns cond.1 mutations). The `test_runner.bash` adds a live `orchestrator_e2e` smoke that DOES invoke the real verifier against real roadmap state and verifies both sentinels emit — currently emits FAIL/RED with exit 1 matching the F2-fired ledger truth.

6. **C3-6 compose_f1_v2_raw does not recompute from check pass-rate.** Per spec §1.4 / §3.4, the canonical input is the F2-override-applied score from the ledger, not a fresh recomputation from AN11/Φ/adv/Putnam status. The check results modulate the band only via D-3 prereqs (Putnam) and falsifier flags (AN11 critical / adv F-ARTIFACT) — they do NOT alter the F1 numerical score. This is deliberate: F1_v2 is a substrate-architectural ledger anchor, not a runtime check aggregate. If the ledger entry is missing or malformed, the helper returns 0.0 → RED band emerges from threshold logic.

---

## Verification

```bash
bash state/clm_consciousness_verify_band_test_2026_05_04/test_runner.bash
# === summary ===
#   PASS 5 / FAIL 0 / SKIP 0 / TOTAL 5
#   all scenarios PASS — BG-VERIFIER-WIRE D-3 + D-4 SATISFIED
```

Live verifier output (current state):
```
__CLM_CONSCIOUSNESS_VERIFY__ FAIL an11=unknown phi=unknown adv=unmet putnam=unmet manual=0
__CLM_CONSCIOUSNESS_BAND__ RED score=0.4080 f2=FIRES
```
Exit code: 1 (RED band supersedes FAIL verdict per D-4).

---

## Files touched

| Path | Action |
|---|---|
| `tool/clm_consciousness_verify.hexa` | patched +258 LoC (helper functions + band orchestration + emit + exit semantics) |
| `state/clm_consciousness_verify_band_test_2026_05_04/scenario_red_f2_fire.bash` | NEW |
| `state/clm_consciousness_verify_band_test_2026_05_04/scenario_yellow_f2_clear.bash` | NEW |
| `state/clm_consciousness_verify_band_test_2026_05_04/scenario_green_full_prereq.bash` | NEW |
| `state/clm_consciousness_verify_band_test_2026_05_04/scenario_green_demoted.bash` | NEW |
| `state/clm_consciousness_verify_band_test_2026_05_04/test_runner.bash` | NEW |
| `docs/clm_consciousness_verify_band_wired_landed_2026_05_04.ai.md` | NEW (this doc) |

NOT touched (per BG critical constraints):
- `.roadmap.clm` / `.roadmap.n_substrate` (BG-CLM-COND1-APPLY owns)
- `tool/n_substrate_f1_v2_band.hexa` (LOCKED)
- `tool/n_substrate_putnam_check.hexa` (LOCKED)
- No git commit performed ($0 patch+test only)

---

## Closure

BG-VERIFIER-WIRE lane CLOSED. Downstream consumers can now:
- Parse `__CLM_CONSCIOUSNESS_BAND__` sentinel for current band
- Trust D-4 exit codes for shell-based gating (with C3-3 caveat)
- Rely on D-3 GREEN-tier phenomenal gate enforcement (via band hook itself)

Next lane (out of scope here): BG-CLM-COND1-APPLY landing the cond.1 cross_link annotation propagation; once that lands, the `.roadmap.clm` reference path resolves canonically. Today the helpers fall back to `.roadmap.n_substrate` correctly.
