# `chflags uchg` Flag Audit — anima-eeg / anima-clm-eeg / anima-eeg-core

**Date**: 2026-05-03
**Author**: P5 BG (analyze_wrapper cycle)
**Trigger**: P4 BG (`a1e6ad14d0b8ddc8f`) reported that `analyze.hexa` was
`uchg`-locked, blocking write. P2 BG noted `clm_eeg_harness_smoke.hexa` is
similarly locked. Sweep audit requested to (a) catalogue locked files,
(b) detect intent pattern, (c) recommend flag-policy without modifying
state.

**Mode**: read-only. **No `chflags` mutations performed.**

---

## §1. Scope

`find ... -name "*.hexa" -type f -exec ls -lO {} \;` across:

| dir | total .hexa | locked (`uchg`) | ratio |
|-----|------------:|----------------:|------:|
| `anima-eeg/` (root, depth 1) | 30 | 8 | 27% |
| `anima-eeg/protocol/` (singular) | 1 | 1 | 100% |
| `anima-eeg/protocols/` (plural, P5 dir) | 33 | 1 | 3% |
| `anima-eeg/tool/` | 14 | 14 | **100%** |
| `anima-clm-eeg/tool/` | 31 | 28 | 90% |
| `anima-eeg-core/tool/` (root) | 1 | 1 | 100% |
| `anima-eeg-core/tool/modules/_core/` | 9 | 9 | **100%** |
| `anima-eeg-core/tool/modules/_gates/` | 5 | 5 | **100%** |
| `anima-eeg-core/tool/modules/_artifact/` | 11 | 10 | 91% |
| `anima-eeg-core/tool/modules/_paradigms/` | 5 | 5 | **100%** |
| `anima-eeg-core/tool/modules/_hw/` | 6 | 6 | **100%** |
| `anima-eeg-core/tool/modules/_metrics/` | 19 | 5 | 26% |
| `anima-eeg-core/tool/modules/_integrations/` | 10 | 3 | 30% |
| **TOTAL** | **175** | **96** | **55%** |

(Counts mid-2026-05-03 22:10 KST; per-dir totals do not double-count.)

---

## §2. Findings — locked files by group

### 2.1 `anima-eeg/` root (8 locked, 22 unlocked)

All locked are the **2026-04-28 helmet/cap/electrode batch** + **2026-05-03
realtime/closed-loop batch**. Unlocked are the actively-edited capture
pipeline (`collect.hexa`, `analyze.hexa`, `realtime.hexa`, `calibrate.hexa`,
`eeg_recorder.hexa`, `_session_manager.hexa`, etc.).

| file | size | mtime | flag |
|------|-----:|-------|------|
| `electrode_helper_rich.hexa` | 28507 | 2026-04-28 19:20 | uchg |
| `eeg_setup.hexa` | 8803 | 2026-04-28 20:26 | uchg |
| `headplot_helper.hexa` | 15819 | 2026-04-28 19:20 | uchg |
| `impedance_real_hardware_validation.hexa` | 28611 | 2026-04-28 18:55 | uchg |
| `full_helmet_view.hexa` | 31132 | 2026-04-28 19:19 | uchg |
| `dual_stream.hexa` | 17362 | 2026-05-03 14:32 | uchg |
| `rp_adaptive_response.hexa` | 19239 | 2026-05-03 14:32 | uchg |
| `experiment.hexa` | 36032 | 2026-05-03 14:31 | uchg |
| `closed_loop.hexa` | 20574 | 2026-05-03 14:32 | uchg |
| `neurofeedback.hexa` | 16089 | 2026-05-03 14:32 | uchg |

(P5 note: `analyze.hexa` is **NOT** in the current locked set — P4 must
have cleared it via `chflags nouchg` before their write, then it stayed
unlocked. Currently `flags=-` per `ls -lO`.)

### 2.2 `anima-eeg/tool/` — 14/14 locked (100%)

All `Apr 28` mtimes (2026-04-28 20:50–23:55). This is the
**daily-life / behavioural / longitudinal toolbox**, frozen as a
batch on 2026-04-28. Pattern: bulk-lock-after-batch-freeze.

```
behavioral_correlates_logger.hexa  cardiac_eeg_integrator.hexa
commit_msg_diff_alignment_lint.hexa  daily_life_context_logger.hexa
eeg_daily_life_verifier.hexa  eeg_feedback_loop.hexa
eye_tracker_webcam.hexa  long_duration_recorder.hexa
longitudinal_session_recorder.hexa  mobile_eeg_integrator.hexa
pre_post_task_recorder.hexa  resting_state_network_analyzer.hexa
sleep_tracker.hexa  wearable_health_integrator.hexa
```

### 2.3 `anima-eeg/protocols/` — 1/33 locked

Only `p300_visual_oddball.hexa` (22732 bytes, 2026-04-28 21:08, has
`raw#12 frozen` marker in header). All 32 other protocol files are
**unlocked** — including `analyze_wrapper.hexa` (this cycle's new file),
`cap_fit_verify.hexa`, `master_preflight.hexa`, the `*_session_audio.hexa`
suite, the `*_emg.hexa` suite, etc. Pattern: only `raw#12 frozen`-marked
pre-registers locked.

### 2.4 `anima-eeg/protocol/` (singular dir) — 1/1 locked

`p300_auditory_oddball.hexa` (15139 bytes, 2026-04-28 21:05, `raw#12
frozen`). Companion to §2.3 — likely an older `protocol/` (singular)
location that has been superseded by `protocols/` (plural). The lock
preserves the historical pre-register manifest.

### 2.5 `anima-clm-eeg/tool/` — 28/31 locked (90%)

The **CLM-EEG path-A pre-register chain** (P0/P1/P2/P3 + harness) is
locked-as-a-batch per `anima-clm-eeg/docs/silent_edit_dual_lock_protocol.md`
(2026-04-27). Confirmed: 7/8 listed in §1 of that protocol have `flags=uchg`
(only `clm_eeg_pre_register_v1.json` was found unlocked — drift?).

The **3 unlocked** in this dir are the actively-edited targets:
```
mk_xii_hard_pass_composite.hexa     (last edit 2026-05-02 08:42)
welch_to_bandpower_transcoder.hexa  (last edit 2026-05-03 23:17 — N2 sibling owns)
clm_eeg_harness_realswap.hexa       (last edit 2026-05-03 22:47 — actively under realswap dev)
```

This is a **clean signal**: the lock policy correctly distinguishes
"frozen pre-register manifest" vs "actively-edited harness".

### 2.6 `anima-eeg-core/tool/modules/` — 44/65 locked

**Locked subdirs (100%)**:
- `_core/` (9/9): adapter, chflags_lock, eeg_export, falsifier_runner,
  filter_pipeline, jsonl_audit, npy_loader, pipeline_suggester,
  `_integration_test.hexa`. These are the **frozen core API** —
  changing any of these ripples through every consumer.
- `_gates/` (5/5): berger_alpha, composite_gate, hjorth_band, pe_saturation,
  rms_band — **frozen verdict gates**.
- `_paradigms/` (5/5): auditory_p300, daily_life, resting_baseline,
  visual_p300, `_integration_test.hexa` — frozen paradigm registry.
- `_hw/` (6/6): adjustment, board_health, headplot, impedance, recorder,
  `_integration_test.hexa` — frozen hardware drivers.

**Mostly-locked (90%)**:
- `_artifact/` (10/11): every detector locked except
  `rail_flat_detector.hexa` (7378 bytes, 2026-05-03 15:33 — actively
  edited per §2.6.unlocked).

**Mostly-unlocked (~26-30%)**:
- `_metrics/` (5/19): only `hjorth, lz76, gamma_theta,
  permutation_entropy, _integration_test` locked. Active dev: `*_native`
  variants (band_power_5, hjorth_native, pe_native, lz76_native,
  gamma_theta_native, phi_proxy_native), plus alpha/dmn/spectral
  variants — all unlocked.
- `_integrations/` (3/10): only `clm_eeg_p2, rsn_validate,
  artifact_pipeline` locked. Active dev: `cyborg_token_emit`,
  `clm_eeg_p1`, `clm_eeg_p3`, `berger_validate`, `synthetic_fixture`,
  `multi_subject_aggregate`, `_integration_test` — all unlocked.

Pattern matches: **frozen API surface = locked; active development
modules = unlocked.**

---

## §3. Pattern analysis

### 3.1 Confirmed institutional lock policy

The lock policy is **explicitly documented and intentional** in three
places:

1. `anima-clm-eeg/docs/silent_edit_dual_lock_protocol.md`
   (2026-04-27) — formalises Layer 1 (`chflags uchg`) + Layer 2
   (`git add`) as orthogonal silent-edit defenses. 8-file Path-A target list.
2. `anima-clm-eeg/tool/silent_edit_dual_lock.sh.txt` — the lock-applying
   script.
3. `anima-eeg-core/tool/modules/_core/chflags_lock.hexa` — runtime
   lock/unlock primitives (`_core_lock_file`, `_core_unlock_file`,
   `_core_is_uchg`) with raw#85 audit-ledger emission. Exposes
   `--unlock <p>` / `--lock <p>` / `--status <p>` CLIs.

This is **not accidental**. The lock is a deliberate "frozen-contract"
marker, applied institutionally.

### 3.2 Lock criterion (inferred from data)

A `.hexa` file is locked iff **any of**:
- Has `raw#12 frozen` (pre-register marker — see §2.3 P300 cases)
- Was part of a documented batch-freeze (Path A 8-file, §2.5; helmet/cap
  2026-04-28 batch, §2.1; daily-life tool batch §2.2)
- Is a `_core/` / `_gates/` / `_paradigms/` / `_hw/` API-surface module
  (frozen API contract — §2.6)
- Has a downstream consumer that depends on byte-identical signature

A file is **un**locked iff:
- Actively under development (recent mtime + active feature work) — see §2.6
  "Mostly-unlocked" or §2.5 "3 unlocked"
- New module not yet promoted to frozen-batch (e.g., `*_native.hexa` variants
  in `_metrics/`)
- Newly landed this cycle (e.g., `analyze_wrapper.hexa` in §2.3 — P5 own
  this; will request lock when batch-frozen)

### 3.3 Drift / outliers

- **`analyze.hexa`** — currently `flags=-`. P4 cleared it via
  `chflags nouchg` to land `detect_railed_channels` and did not relock.
  This is a **policy drift**: analyze.hexa is a frozen-API consumer
  (`g_band_*` schema referenced by `_metrics/`, `_paradigms/`, etc.) and
  should be relocked once P4's spec is settled.
- **`clm_eeg_pre_register_v1.json`** — listed in Path-A 8-file lock
  protocol but currently `flags=-`. Either (a) drift or (b) intentional
  unlock for v1.1 patch landing. Worth confirmation from user.
- **`rail_flat_detector.hexa`** — only unlocked file in `_artifact/`.
  Recent mtime (2026-05-03 15:33) suggests active development; likely
  pending batch-freeze — informational, not a flag policy violation.

---

## §4. Risk

### 4.1 Silent-fail risk for future BGs

When a BG attempts to write to a `uchg`-locked file:
- `Edit` / `Write` tool returns OS error `EPERM`
- Most agents propagate this as "permission denied" — easy to
  misinterpret as a `.gitignore` issue or umask problem
- BG may then attempt mitigation (chmod +w, sudo) instead of
  recognising "this file is intentionally frozen"

**Direct precedent**:
- P4 BG (analyze.hexa) — recognised `chflags uchg`, cleared, landed,
  but did not relock (§3.3)
- P2 BG (clm_eeg_harness_smoke.hexa) — recognised, deferred work to
  avoid touching frozen file (correct)

### 4.2 Recommended mitigations

**M1. Pre-flight `chflags` check in tool spec**

Future BG cycles should include a pre-flight `ls -lO <target>` check.
If `flags=uchg`, BG should explicitly reference the lock protocol and
either:
- (a) request user permission to unlock+edit+relock (write-with-policy)
- (b) defer the edit and document why (read-only)

**M2. `--silent-fail-on-uchg` global flag (optional)**

If a future tool wants to *gracefully degrade* rather than abort, a
global flag indicating "treat uchg as a soft-block, not an error"
could be useful. Lower-priority — current EPERM surface is loud
enough that recognition is feasible.

**M3. Inverse audit: surface lock-status in `git status`**

`chflags uchg` is invisible to `git status`. A pre-commit hook (or
just a periodic audit like this doc) that prints
`chflags uchg → 96 .hexa files` would surface the lock state visibly.

**M4. Audit ledger**

`anima-eeg-core/tool/modules/_core/chflags_lock.hexa` already
emits raw#85 audit ledger rows at every lock/unlock boundary. Recommend
**reading** `state/anima_eeg_core_chflags_audit.jsonl` (default ledger
path) at start of each cycle to surface recent flag transitions.

---

## §5. Recommendations

(C3 honest, **read-only audit only — DO NOT auto-clear without explicit
user policy decision**.)

### Top 3

1. **KEEP locked** (no action needed): all 96 currently-locked files.
   The pattern is institutional, documented, and serving its purpose.
   The Path-A 8-file silent-edit defense is the explicit motivation
   (see §3.1).

2. **USER DECISION on `analyze.hexa` relock**: P4 cleared it 2026-05-03
   to land `detect_railed_channels()`. With this cycle's
   `analyze_wrapper.hexa` consuming the rail-detect API, `analyze.hexa`
   may be batch-ready for relock. Recommend user decision: **relock
   analyze.hexa** to restore frozen-API contract OR **leave unlocked**
   if more rail-detect API edits are anticipated.

3. **USER DECISION on `clm_eeg_pre_register_v1.json` relock**: in
   Path-A protocol 8-file list but currently unlocked. Either (a) intentional
   unlock for v1.1 patch (then relock pending), or (b) drift. Recommend
   user confirms.

### Procedural

- New files this cycle (`analyze_wrapper.hexa`, helper `.py`) should
  remain unlocked until P5 batch-freeze (likely after wrapper
  integration with `master_preflight.hexa` lands).
- Future BG cycles touching any locked file SHOULD pre-flight the
  `ls -lO` check (M1) and document the unlock+relock cycle in the
  cycle summary.
- Recommend committing this audit doc to git so the lock census is
  versioned and visible to future cycles.

---

## §6. References

- `anima-clm-eeg/docs/silent_edit_dual_lock_protocol.md` (2026-04-27)
- `anima-clm-eeg/tool/silent_edit_dual_lock.sh.txt`
- `anima-eeg-core/tool/modules/_core/chflags_lock.hexa`
- `state/anima_eeg_core_chflags_audit.jsonl` (raw#85 audit ledger)
- This cycle: `anima-eeg/protocols/analyze_wrapper.hexa`,
  `state/.analyze_wrapper_npy_helper.py`
- P4 cycle (`a1e6ad14d0b8ddc8f`): `anima-eeg/analyze.hexa`
  `detect_railed_channels` landing
