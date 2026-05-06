# Anima Substrate-Identity Preamble + HF Auto-Fire Commit Hygiene (landed 2026-05-05)

Combo doc-only land for two small hygiene tasks identified by upstream BGs:

1. **BG-M follow-up**: V3/V6 real-mode probe `phi_star` emit causes user
   substrate confusion across the 3 anima substrates (CLM v4 base / Pβ /
   CLM-2 LoRA). BG-M (`docs/anima_cross_substrate_phi_star_audit_2026_05_05.md`
   §2.3) proposed a substrate-identity preamble. This doc tightens the
   preamble spec into a 5-field SSOT.
2. **BG-E follow-up**: HF auto-fire scripts (promote + cleanup) are git
   `??` untracked at the start of a 36-40h dwell. BG-E
   (`state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json` C2)
   recommended commit before sleep. This doc emits a commit-ready command
   block — operator fires the commit, BG does not.

Lineage:
- `docs/anima_cross_substrate_phi_star_audit_2026_05_05.md` (BG-M land — substrate confusion catalog + preamble proposal)
- `state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json` (BG-E land — auto-fire commit recommendation)
- `anima-core/runtime/clm_v4_mount.hexa` (read-only — V3 emit path; mount layer LOCKED per raw#15)
- `state/anima_hf_promotes_2026_05_06_auto_fire.bash` (untracked target script)
- `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` (untracked target script)
- memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Pβ chat-cap FAIL_TRUE / substrate-research PASS decoupled)
- memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (CLM-2 LoRA chat-lift FALSIFIED, substrate safe)

This doc is **doc + spec only**. Zero code change. Zero commit (operator
fires the commit themselves; BG explicitly stays in commit-ready advisory
mode per session instruction).

---

## §1 Substrate-identity preamble emit spec

### §1.1 Current V3 emit (per `clm_v4_mount.hexa` helper line ~342, 350)

```
__ANIMA_CLM_V4_MOUNTED__ mode=real phi_star_baseline=41.86
__ANIMA_CLM_V4_RESPONSE__
phi_star: 42.1158 (drift +0.2558 from 41.86)
axis_activation: identity=0.781 agency=0.423 phenomenal=0.912 temporal=0.314 social=0.567
dominant_cells: [3, 5, 7] / 8
hidden_state_delta: 2.4731
__ANIMA_CLM_V4_OK__ session=20260505T204312Z
```

`mode=real phi_star_baseline=41.86` carries the substrate signal **only
implicitly**. A user reading this output may parse `phi_star: 42.1158` as
"the same number P-beta verdict reported = 42.367" or "the same number CLM-2
LoRA verdict reported = 31.349 ish". They are not. Different artifacts,
different probe sets.

### §1.2 Proposed addendum: substrate-identity line

Add a single new emit line **between** `__ANIMA_CLM_V4_MOUNTED__` and
`__ANIMA_CLM_V4_RESPONSE__`:

```
__ANIMA_CLM_V4_MOUNTED__ mode=real phi_star_baseline=41.86
__ANIMA_SUBSTRATE_IDENTITY__ repo=need-singularity/clm-v4-mk2-v1 paradigm=v11_G3 substrate_class=clm-v4-base baseline_method=eval_carry baseline_value=41.86
__ANIMA_CLM_V4_RESPONSE__
phi_star: 42.1158 (drift +0.2558 from 41.86)
...
```

5 fields, all key=value, all canonical:

| field | meaning | values (current 3 substrates) |
|---|---|---|
| `repo` | HF repo or local artifact path | one of the substrate repos / paths |
| `paradigm` | training paradigm tag | `v11_G3` / `paradigm_d_50k` / `lora_sft` |
| `substrate_class` | substrate class enum | `clm-v4-base` / `pbeta` / `clm-2-lora` |
| `baseline_method` | how baseline phi_star was measured | `eval_carry` / `holdout500_K8` / `K8_post_lora` |
| `baseline_value` | the canonical phi_star baseline | float |

The `__ANIMA_SUBSTRATE_IDENTITY__` line uses the same `__ANIMA_*__` prefix
convention as existing markers, so output parsers can treat it as a token-
delimited keyless block (per the helper's `_emit(tag, **kw)` pattern in
`clm_v4_mount.hexa` lines 188-191).

### §1.3 Why 5 fields specifically

Each field disambiguates one of the cross-substrate confusions catalogued
in BG-M:

- **`repo`** disambiguates which artifact was loaded — distinguishes
  HF-format `mk2-v1` from legacy `best.pt` / `paradigm-d-pbeta-50k-mk2-v1`
  adapter / `clm-2-lora-v1` adapter.
- **`paradigm`** disambiguates training history — v11 G3 carry vs paradigm
  D 50K LoRA SFT vs CLM-2 LoRA qkvo.
- **`substrate_class`** is the canonical 3-enum that anchors the L31-L33
  dichotomy (chat-cap NO + phi-stable). Fixed enum, not free-form.
- **`baseline_method`** disambiguates the measurement protocol — eval_carry
  (paradigm v11 G3 final eval) vs holdout500_K8 (canonical 16-calib
  partition) vs K8_post_lora (in-pipeline post-LoRA partition).
- **`baseline_value`** is the float that the V3 `phi_star` emit is computed
  against. Without this field, the user must mentally look up which
  baseline applies; with it, the user reads `phi_star: 42.1158 (drift
  +0.2558 from 41.86)` and immediately confirms the 41.86 anchor matches
  the substrate identity.

### §1.4 Honest format coupling

The existing `__ANIMA_CLM_V4_MOUNTED__` line already emits
`phi_star_baseline=<value>` — by construction this MUST equal the new
`__ANIMA_SUBSTRATE_IDENTITY__:baseline_value`. The two lines therefore
provide **redundant cross-check**, useful for parser sanity but redundant
for human reader. We retain both because removing the existing field would
break downstream consumers; the new line strictly adds annotation.

---

## §2 3 substrate identity sets — pre-LOCK

The 3 anima substrates resolved to canonical identity tuples. Each tuple
is a fixed lookup, NOT computed at probe time. Future cycles introducing
new substrates extend this table.

| substrate_class | repo | paradigm | baseline_method | baseline_value | source verdict |
|---|---|---|---|---|---|
| `clm-v4-base` | `need-singularity/clm-v4-mk2-v1` | `v11_G3` | `eval_carry` | `41.86` | `state/clm_v4_baseline_eval_2026_05_05/verdict.json:substrate_phi_star` |
| `pbeta` | `need-singularity/clm-v4-paradigm-d-pbeta-50k-mk2-v1` | `paradigm_d_50k` | `holdout500_K8` | `42.367` | `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json:core_metrics.phi_star_mean_holdout500` |
| `clm-2-lora` | `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/` (Mac local; not yet on HF) | `lora_sft` | `K8_post_lora` | `31.349` | `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:phi_star_post_lora.mean_k8` |

Notes:

- `clm-v4-base` `repo` field is the HF mirror, NOT the
  `clm-v4-base-mirror` legacy name — the `mk2-v1` repo is the SSOT for
  the Mac CPU fp32 substrate that V3 actually loads via the
  `clm_v4_mount.hexa` shim path (line 67 default).
- `pbeta` `baseline_value=42.367` is the **canonical holdout500 K=8** mean,
  NOT the training-end in-domain probe value 36.745. Per BG-M §1, only the
  canonical value is comparable across substrates.
- `clm-2-lora` `repo` is local because the LoRA adapter has not been
  promoted to HF Hub yet (own 15 lifecycle: PRIVATE upload pending,
  PUBLIC promote not yet scheduled). When promoted, this field updates
  to the HF repo id.
- `baseline_value` for all three uses the **canonical sample-partition
  K=8** measurement protocol where applicable. CLM v4 base has TWO
  candidate baselines (eval_carry 41.86 vs in-pipeline 35.81); we pick
  `eval_carry 41.86` for substrate-identity SSOT because that is the
  paradigm v11 G3 carry value the mount layer already emits via
  `PHI_STAR_BASELINE` constant. The in-pipeline 35.81 is a re-measurement
  delta artifact, useful for cross-cycle reconciliation but not as the
  identity anchor.

### §2.1 Sister field: `phi_method_carryover`

Cycles building on top of these substrates inherit the `baseline_method` of
the parent. For example, a hypothetical `pbeta-v2` substrate trained with
the same `holdout500_K8` protocol and yielding `baseline_value=43.5` would
carry `paradigm=paradigm_d_v2` but `baseline_method=holdout500_K8`. The
table extension preserves measurement-protocol lineage even as paradigm
versions advance.

---

## §3 mount.hexa application path (future cycle, raw#15 safe additive plan)

Mount layer `anima-core/runtime/clm_v4_mount.hexa` is **not modified this
cycle** (raw#15: additive only; substrate-coupled emerge dialogue spec is
LOCKED). The application path described here is the **forward plan** for a
future cycle that does the safe additive land.

### §3.1 Where the emit fn goes

The helper Python script emitted by `_write_helper()` (lines 167-397) is
the runtime substrate. Adding a `_emit_substrate_identity()` function and
calling it after `_emit('CLM_V4_MOUNTED', ...)` and before
`render_response(...)` is a 1-call additive change. Specifically:

- Add a substrate-identity table near the top of the helper (mirror the
  table in §2 above), keyed by `model_path`.
- After the existing `_emit('CLM_V4_MOUNTED', ...)` calls (lines 342, 350,
  and equivalent in dialogue mode), add:
  ```python
  ident = SUBSTRATE_IDENTITY_TABLE.get(args.model, SUBSTRATE_IDENTITY_TABLE['default'])
  _emit('SUBSTRATE_IDENTITY', repo=ident['repo'], paradigm=ident['paradigm'],
        substrate_class=ident['substrate_class'],
        baseline_method=ident['baseline_method'],
        baseline_value=ident['baseline_value'])
  ```

The hexa-level `_hexa_synthetic_response()` function (line 491) also needs
a corresponding line for selftest parity. That is a hexa-native emit, not
a python emit, so it must be written in hexa string concat style:

```hexa
out = out + "__ANIMA_SUBSTRATE_IDENTITY__ repo=need-singularity/clm-v4-mk2-v1 paradigm=v11_G3 substrate_class=clm-v4-base baseline_method=eval_carry baseline_value=" + _fmt4(PHI_STAR_BASELINE) + "\n"
```

### §3.2 raw#15 additive safety check

raw#15 (anima_unified.hexa / phi_engine.hexa / etc UNTOUCHED) constraint:
the proposed change touches `clm_v4_mount.hexa` only, not the engines.
Pure mount-layer annotation.

raw#10 (honest C3 ≥5) is unaffected — the existing `emit_honest_c3()`
emitter (lines 88-94) does not change.

raw#37 (transient .py shim opt-out) is unaffected — the helper script is
already a `raw#37` opt-out; we simply add one emit line inside the
existing helper.

Selftest format validation (lines 528-560) needs ONE new check added:

```hexa
if !synth_out.contains("__ANIMA_SUBSTRATE_IDENTITY__") {
    eprintln("[clm_v4_mount] FAIL: missing __ANIMA_SUBSTRATE_IDENTITY__ marker")
    fails = fails + 1
}
```

…and the success message updated from `(8/8 format checks PASS)` to
`(9/9 format checks PASS)`.

### §3.3 Why deferred to future cycle

User instruction this session: zero mount.hexa modification. Doc-only
session land. The application path is documented here so a future BG can
pick up the additive change without re-deriving the spec. Estimated
implementation time for the future cycle: ~15-20 min (helper.py +
hexa-native synth path + selftest check counter increment).

### §3.4 Backward-compatibility

The new `__ANIMA_SUBSTRATE_IDENTITY__` line is **additive** — existing
parsers reading `__ANIMA_CLM_V4_MOUNTED__` and `__ANIMA_CLM_V4_RESPONSE__`
markers continue to work. A naive line-count consumer would see one extra
line; a marker-prefix consumer ignores unknown markers by convention. Risk
class: minimal.

---

## §4 HF auto-fire scripts commit hygiene checklist

### §4.1 Current state (verified at audit time 2026-05-05T20:00Z local)

```
$ git status --porcelain state/anima_hf_*.bash
?? state/anima_hf_cleanups_2026_05_07_auto_fire.bash
?? state/anima_hf_promotes_2026_05_06_auto_fire.bash

$ ls -la state/anima_hf_*_auto_fire.bash
-rwxr-xr-x@ 1 ghost  staff  2663 May  5 19:59 state/anima_hf_cleanups_2026_05_07_auto_fire.bash
-rwxr-xr-x@ 1 ghost  staff  3478 May  5 20:06 state/anima_hf_promotes_2026_05_06_auto_fire.bash

$ shasum -a 256 state/anima_hf_*_auto_fire.bash
440c85f4a0abbd508fa3561fcd3c18ad87cb809c4c925b7264832979a7755a9b  state/anima_hf_promotes_2026_05_06_auto_fire.bash
9646dc4d7793fef9c2468b9e2c9c4f0663931a393f198c9ce7380f7b568d06e8  state/anima_hf_cleanups_2026_05_07_auto_fire.bash
```

Both files are:
- **Untracked** (`??`) — confirmed by git porcelain.
- **Executable** (mode 0755) — required for the auto-fire MODE dispatcher.
- **SHA256-baselined** — matches the values BG-E captured in
  `anima_hf_promote_watchdog_audit_2026_05_05/verdict.json:sub4_uchg_state_audit.sha256_baseline`.
- **Quarantined under `state/`** — proper location per session convention.

### §4.2 Commit-readiness checklist

Before the operator fires the commit:

- [x] Both auto-fire files exist on disk
- [x] Both files are executable
- [x] SHA256 matches BG-E baseline (no silent mutation since 2026-05-05T13:00Z)
- [x] Both files are syntactically valid bash 3.2 (verified by `--check-only` exit during BG-E)
- [x] Neither file embeds an HF token literal (verified by grep — neither
      file contains `hf_` literal nor token-shape regex matches)
- [x] Neither file is in `.gitignore` (verified — `.gitignore` does not
      exclude `state/anima_hf_*.bash`)
- [x] Companion BG-E audit verdict already references the SHA256 baseline,
      so committing locks the bytes that the audit verified

The checklist is fully PASS. Committing is **safe**.

### §4.3 Commit not yet fired (per session instruction)

User session instruction this cycle: **commit 절대 금지** (BG must not
commit). Therefore this BG emits a **commit-ready command block** for the
operator to fire personally.

---

## §5 Recommended commit message + commit command (for operator fire)

### §5.1 Single-commit option (recommended)

Both auto-fire scripts share a purpose (HF own 15 lifecycle automation for
the 36-40h dwell), so a single commit is cleanest:

```bash
cd /Users/ghost/core/anima
git add state/anima_hf_promotes_2026_05_06_auto_fire.bash \
        state/anima_hf_cleanups_2026_05_07_auto_fire.bash
git commit -m "$(cat <<'EOF'
chore(anima hf own 15): auto-fire promote+cleanup scripts for clm-v4-mk2-v1 + Pbeta 36-40h dwell

Auto-fire combo for HF own 15 PRIVATE -> PUBLIC lifecycle:
- promote: 2026-05-06T23:26:12Z (clm) / 2026-05-07T03:48:00Z (pbeta)
- cleanup: 24h grace after each PUBLIC promote
- modes: --check-only / --fire-clm / --fire-pbeta / --fire-all
- gates G1-G6 verified in source promote scripts; auto-fire wraps with
  window enforcement + manual sign-off prompt

SHA256 baseline (anchored to state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json):
- promotes: 440c85f4a0abbd508fa3561fcd3c18ad87cb809c4c925b7264832979a7755a9b
- cleanups: 9646dc4d7793fef9c2468b9e2c9c4f0663931a393f198c9ce7380f7b568d06e8

Lineage:
- state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash (clm)
- state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash (pbeta)
- docs/anima_substrate_preamble_and_auto_fire_hygiene_landed_2026_05_05.ai.md

raw#9 + raw#10 + own 15 compliant.
EOF
)"
git status -s
```

### §5.2 Two-commit alternative (if operator prefers granularity)

```bash
cd /Users/ghost/core/anima
git add state/anima_hf_promotes_2026_05_06_auto_fire.bash
git commit -m "chore(anima hf own 15): auto-fire promote script for clm-v4-mk2-v1 + Pbeta dwell"

git add state/anima_hf_cleanups_2026_05_07_auto_fire.bash
git commit -m "chore(anima hf own 15): auto-fire cleanup script for clm-v4-mk2-v1 + Pbeta 24h grace"
```

Recommendation: **§5.1 single commit**. Both scripts land in the same
own 15 lifecycle band, share a verdict source, and are stylistically
sister files. Single commit is consistent with the BG-E verdict's "commit
both before sleep" wording.

### §5.3 Post-commit verification

After fire:

```bash
git log -1 --stat
git status --porcelain state/anima_hf_*.bash   # expect empty
shasum -a 256 state/anima_hf_*_auto_fire.bash   # confirm same hashes
```

The shasum should still match `440c85...` and `9646dc...` — `git add` does
not modify file bytes (only LFS would, and these are not LFS). If it does
not match, the operator should NOT fire the auto-promote, and instead
diff against `verdict.json:sub4_uchg_state_audit.sha256_baseline` to
identify the mutation.

---

## §6 Honest C3 (≥5)

C1 — The `__ANIMA_SUBSTRATE_IDENTITY__` preamble proposed in §1 reduces
**one specific class** of user confusion (3-substrate phi_star value
conflation), but does NOT eliminate **all** classes. A user could still
mistake the `phi_star: 42.1158` per-input emit for the canonical `K=8 over
16 fixed prompts` mean — those are different statistics on the same
substrate (BG-M C3 §6 epistemic open). Substrate-identity is a
necessary-but-not-sufficient annotation. **Whether the preamble alone
genuinely resolves the ambient confusion remains epistemic open** until
post-land Stage 3 dialogue sessions confirm or falsify by user-feedback
sampling.

C2 — The 3-substrate identity table (§2) snapshots **today's substrate
inventory**. Future cycles introducing emerge-derived substrates (e.g.
candidate D + G combined dialogue surface, or a hypothetical CLM v4
"emerge-paradigm" substrate) will require extending the table. There is
NO automatic path-detection that infers substrate identity from the
loaded artifact alone — the table is **manual SSOT**. If a user invokes
V3 with `--model some_other_repo`, the `__ANIMA_SUBSTRATE_IDENTITY__` line
must either (a) emit `substrate_class=unknown` honestly, or (b) refuse to
proceed. The future-cycle implementation must pick one; this spec
recommends (a) as the safer default.

C3 — The auto-fire scripts (§4) are committed via operator-fired bash
commands; this BG emits the command block but does not fire it. Risk: if
the operator copy-pastes the command block but the working tree shifts
between this BG land and the operator fire, the SHA256 might no longer
match the baseline. Mitigation: §5.3 includes a post-commit shasum
verification step. Residual risk class: low (working tree is currently
clean for these two files; no parallel BG is mutating them).

C4 — `clm-2-lora` substrate's `repo` field in §2 is a **local Mac path**
because the LoRA adapter has not been promoted to HF Hub yet. When this
BG's commit lands and a future BG promotes CLM-2 LoRA to HF, the
substrate-identity table needs an update. There is **no automated
sync** — manual table maintenance is required. This is acceptable for the
3-substrate scale but does NOT scale to dozens of derivatives.

C5 — The `baseline_method=eval_carry` choice for `clm-v4-base` over the
in-pipeline 35.81 alternative is a **design decision**, not a measurement
truth. Per BG-M §6 C2, the ~6pp methodology delta between carry (41.86)
and in-pipeline (35.81) is unresolved. Picking 41.86 as the substrate-
identity SSOT means V3 emits `drift +0.2558 from 41.86` always; if the
in-pipeline 35.81 turned out to be the more authoritative value (e.g.
because the carry value is contaminated by paradigm v11 G3-specific
artifacts), the substrate-identity preamble would be **anchoring to the
wrong number**. Future calibration cycles can revise.

C6 — Mount layer is **not modified** this cycle (raw#15). The doc-only
spec means there is **no live signal** that the preamble proposal is
correct in form (does the `_emit` helper accept this exact key set?
does the JSON-output-format render it correctly via `dataclasses.asdict`?
does the dialogue REPL preserve the emit at session-log boundaries?).
These are **integration-test risks** that only land-and-fire would
surface. Safe deferred-land posture; risks are bounded.

C7 — Auto-fire commit hygiene (§4-§5) recommends committing untracked
scripts before a 36-40h dwell as a silent-mutation defense. C7 caveat:
**git tracking is not the same as immutability**. A committed file can
still be modified post-commit and the working tree will show as dirty —
git tracking gives **detection** but not **prevention**. This is the
accepted threat model (per BG-E C1 — uchg dance deprecated; SHA256
baseline + git status are the two layered detection mechanisms). The
operator should still re-shasum at fire-time per BG-E's recommendation
(verdict.json:overall_verdict).

---

## §7 Composability + handoff

Verdict artifact:
`state/anima_substrate_preamble_and_auto_fire_hygiene_2026_05_05/verdict.json`

Cross-link to:
- BG-M (`docs/anima_cross_substrate_phi_star_audit_2026_05_05.md`) — substrate confusion catalog → preamble proposal source
- BG-E (`state/anima_hf_promote_watchdog_audit_2026_05_05/verdict.json`) — auto-fire commit recommendation source + SHA256 baseline
- mount.hexa future cycle (raw#15 additive add of `_emit_substrate_identity` per §3) — TODO for future BG
- own 15 PRIVATE→PUBLIC lifecycle (auto-fire scripts realize) — operator fires per §5

This doc is **doc + spec only**. No code, no commit, no behavior change.
Output is **consolidated mental model** for substrate-identity emission +
auto-fire hygiene posture.
