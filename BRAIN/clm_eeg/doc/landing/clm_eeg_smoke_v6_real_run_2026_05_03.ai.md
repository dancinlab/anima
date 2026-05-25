# clm_eeg harness smoke v6-clean real-fixture run — 2026-05-03

**Cycle**: N+1 (post-transcoder-landing)
**Goal**: prove the v6-clean real fixture flows through the smoke harness end-to-end while preserving the institutional silent-edit dual-lock policy.
**Outcome**: dual-lock policy preserved; harness exit 0 / sentinel `HARNESS_OK`; honest finding that this harness aggregates synthetic-frozen pre-register manifests and does NOT directly consume `CLM_EEG_FIXTURE_PATH`.

---

## 1. Pre-condition: dual-lock unlock procedure

Per `anima-clm-eeg/docs/silent_edit_dual_lock_protocol.md`, eight Path-A frozen artefacts (3 manifests + 4 hexa tools + 1 fixture) carry `chflags uchg` plus `git add` tracking. The smoke harness `anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa` is among them.

User explicit approval ("all go" in chat) lifted the lock on the smoke harness ONLY for this cycle. Procedure followed:

```
ls -lO ... → "uchg 10633 Apr 29"
chflags nouchg anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
ls -lO ... → "- 10633 Apr 29"            # flag cleared, byte count unchanged
[ run smoke harness ]
chflags uchg anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
ls -lO ... → "uchg 10633 Apr 29"          # flag restored, byte count unchanged
```

**Critical contract preserved**:
- No content modification (byte count `10633` identical before/after).
- No cascade-unlock on the other 7 dual-lock artefacts (the upstream p1/p2/p3 pre-register hexa tools, the v1/v1.1 manifests, the synthetic fixture).
- L2 git tracking unaffected.

---

## 2. Run A: synthetic baseline (executed)

Default upstream paths consumed by the harness:

```
CLM_EEG_P1_PATH=state/clm_eeg_p1_lz_pre_register.json   (uchg, 2316B, p1_dry_run_pass=1)
CLM_EEG_P2_PATH=state/clm_eeg_p2_tlr_pre_register.json   (uchg, 1391B, p2_dry_run_pass=1)
CLM_EEG_P3_PATH=state/clm_eeg_p3_gcg_pre_register.json   (uchg, 1690B, p3_dry_run_pass=1)
```

Command (env vars passed for documentation; see §4 for honest finding on env propagation):

```
CLM_EEG_FIXTURE_PATH=anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json \
CLM_EEG_HARNESS_FIXTURE_MODE=real \
HEXA_RESOLVER_NO_REROUTE=1 \
hexa run anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa --selftest
```

Console emit:

```
  p1_bytes               = 2316    p1_dry_run_pass = 1
  p2_bytes               = 1391    p2_dry_run_pass = 1
  p3_bytes               = 1690    p3_dry_run_pass = 1
  composite_pass_count   = 3
  composite_required     = 2
  harness_ok             = 1
  chained_fingerprint    = 2804516380
  verdict                = HARNESS_OK
```

Exit code: `0`. Sentinel: `HARNESS_OK`.

---

## 3. Run B: real-fixture aggregation — NOT EXECUTED (honest skip)

Intended: re-point harness at real-side ledgers (`clm_eeg_p1_lz_pre_register_real.json`, `clm_eeg_p2_tlr_real.json`, no real p3 product) to surface real-data composite verdict.

Blockers (each documented honestly, none worked around):

1. **Env-override sandboxed**: hexa runtime under `HEXA_RESOLVER_NO_REROUTE=1` + darwin-bypass-marker mode does not propagate env() into the .hexa script (verified by re-running with `CLM_EEG_HARNESS_OUT=...` override — output path println still showed default `state/clm_eeg_harness_smoke.json`, and the default file mtime was Apr 27 epoch 1777291065, not refreshed). Therefore `CLM_EEG_P{1,2,3}_PATH` overrides are similarly inert.
2. **Path-swap blocked by uchg**: `state/clm_eeg_p1_lz_pre_register.json` / `_p2_tlr_*.json` / `_p3_gcg_*.json` are all `chflags uchg`. Swapping `_real.json` over them requires unlocking — which would cascade-violate the dual-lock contract on three additional artefacts.
3. **No real p3 product exists** — `state/slm_p3_a1_real_2026_05_03/` is unrelated SLM-paradigm scope, not the GCG (Granger causality) pre-register. p3_real evaluation is **D+5 deferred** per the pre-register `post_arrival_workflow.day` field.

Honest projected verdict if cascade-unlock were performed:

| upstream | real product | dry_run_pass equivalent |
|----------|--------------|-------------------------|
| p1 (LZ)  | `clm_eeg_p1_lz_pre_register_real.json` | `p1_pass=0` (C2 fail: `pct_delta_permille=432` ≫ C2 threshold 200) |
| p2 (TLR) | `clm_eeg_p2_tlr_real.json` | `p2_pass=0` (verdict=INSUFFICIENT; C1 PASS but C2 UNEVALUABLE under F_PLV_DESTROY ICA falsifier) |
| p3 (GCG) | (none — D+5 deferred) | unknown / would default 0 |

→ Projected composite: `pass_count=0` (or 1 if p3 spurious-PASS by missing-key default-0 logic) `< required=2` → **HARNESS_FAIL**.


---

## 4. Honest finding: harness aggregator semantics

Reading the source (`anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa` lines 147–254):

```
fn main() {
    let p1_path = env_str("CLM_EEG_P1_PATH", "state/clm_eeg_p1_lz_pre_register.json")
    let p2_path = env_str("CLM_EEG_P2_PATH", "state/clm_eeg_p2_tlr_pre_register.json")
    let p3_path = env_str("CLM_EEG_P3_PATH", "state/clm_eeg_p3_gcg_pre_register.json")
    ...
    let p1_pass = extract_int_after_key(p1_json, "\"p1_dry_run_pass\":")
    ...
    let harness_ok = if pass_count >= 2 { 1 } else { 0 }
}
```

The harness is a **pure aggregator**:
- It only consumes `p<n>_dry_run_pass` keys from upstream JSONs.
- It does NOT compute any of the 5 metrics (berger_sanity, gamma_theta_ratio, hjorth_real, lz76_real, pe_real) — those live in separate `clm_eeg_*_real.hexa` tools and pre-register tools.
- The `CLM_EEG_FIXTURE_PATH` env is never read by this tool. Fixture-vs-real is an upstream concern.

Combined with the env-sandbox finding (§3.1), the smoke harness in its current form CANNOT be re-pointed at real-side data via env override under any condition. The dual-lock policy is, in this sense, **structurally redundant** with the harness's behavior under the resolver bypass: even unlocked, env injection has no effect.


---


From `anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json`:

| field | value |
|-------|-------|
| `tier` | `functional_analog` |
| `n_subjects` | 1 |
| `f1_status` (LZ-on-binarized-EEG) | `FAIL` |
| `f2_status` (α-coh) | `PASS` |
| `f3_status` (γ/θ ratio) | `FAIL` |
| `rail_quarantined_rows_1idx` | [1, 5, 6, 8, 16] (Fp1, P7, P8, O2, P4) |
| `rail_quarantine_policy` | zero-fill (NOT interpolation) |
| `clean_channel_count` | 11 of 16 |

These caveats DO NOT propagate into the smoke harness composite under the current run path. Anyone reading `state/clm_eeg_harness_smoke.json` (Apr 27 mtime, byte-identical to today's emission) sees `harness_ok=1` — but this attests synthetic-frozen pre-register dry-runs, not real-data evaluation.


---

## 6. Re-lock confirmed (CRITICAL)

```
chflags uchg anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
ls -lO → "uchg 10633 Apr 29 00:06"
```

- Byte count `10633` identical to pre-unlock state.
- mtime `Apr 29 00:06` unchanged (no write occurred during unlock window).
- L1 (chflags) lock restored.
- L2 (git tracked) unaffected.
- Institutional dual-lock contract preserved.

---

## 7. Next-cycle dependencies

Three orthogonal options (ranked by completion-quality lens):

1. **[recommended]** Introduce parallel harness `anima-clm-eeg/tool/clm_eeg_harness_real_smoke.hexa` that defaults to real-side ledger paths (`clm_eeg_p1_lz_pre_register_real.json`, `clm_eeg_p2_tlr_real.json`, future real p3) and aggregates accordingly. Preserves dual-lock contract on the synthetic harness; surfaces real composite cleanly.
2. **[deferred]** B-track v7 fixture with electrode-contact remediation → reduce 5/16 rail-quarantined to ≤2/16 → re-transcode → re-evaluate F1/F2/F3 → if FAIL→PASS transitions surface, emit p{1,2,3}_*_pre_register.json under v2 SSOT (signed freeze, not silent).
3. **[escape-hatch]** Refactor `extract_int_after_key` consumer in smoke harness to accept either `p<n>_dry_run_pass` OR `p<n>_pass` (real-side key naming) — minor source change but requires unlock + re-freeze of the harness itself, which is a v2 SSOT event.

Until one of these lands, the realswap path remains:
- transcoder LANDED (cycle N)
- smoke run EXECUTED but not predictive of real-data composite (cycle N+1, this doc)
- real-data composite verdict NOT YET ESTABLISHED

---

## 8. Provenance

- run log: `state/clm_eeg_smoke_v6_real_2026_05_03/run.log`
- verdict: `state/clm_eeg_smoke_v6_real_2026_05_03/verdict.json`
- README update: `anima-clm-eeg/state/realswap_pending_2026_05_03/README.md`
- this ledger: `docs/ai-native/clm_eeg_smoke_v6_real_run_2026_05_03.ai.md`
- dual-lock protocol SSOT: `anima-clm-eeg/docs/silent_edit_dual_lock_protocol.md`
- transcoder fixture: `anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json`

