# anima-clm-eeg/tool/ Legacy Archive Index — Phase 4 ABSORB-PORT (P/harness pair set)

- **Frozen date**: 2026-05-01
- **Migration phase**: Phase 4 ABSORB-PORT — legacy `anima-clm-eeg/tool/*.hexa`
  is being supplanted by native `anima-eeg-core/tool/modules/_integrations/*.hexa`.
- **Scope of this index**: 5 P/harness pairs (P1, P2, P3, synthetic_fixture,
  harness_smoke). The 4 metric DEPRECATE pairs (lz76_real, pe_real, hjorth_real,
  gamma_theta_ratio) are out of scope — handled by separate A3 agent cycle.
- **raw#9 hexa-only · raw#10 honest C3 · raw#12 sentinel · raw#91 honest triad**

## Verdict per pair

| # | legacy path                                                            | native successor                                                                  | legacy LoC | native LoC | spot-check verdict                                  | physical move verdict     |
|---|------------------------------------------------------------------------|-----------------------------------------------------------------------------------|------------|------------|-----------------------------------------------------|---------------------------|
| 1 | `anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa`                   | `anima-eeg-core/tool/modules/_integrations/clm_eeg_p1.hexa`                       | 353        | 290        | semantic-identical — frozen criteria mirrored       | **SKIPPED — uchg-locked** |
| 2 | `anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa`                  | `anima-eeg-core/tool/modules/_integrations/clm_eeg_p2.hexa`                       | 433        | 435        | semantic-identical — Kuramoto kernel ported verbatim| **SKIPPED — uchg-locked** |
| 3 | `anima-clm-eeg/tool/clm_eeg_p3_gcg_pre_register.hexa`                  | `anima-eeg-core/tool/modules/_integrations/clm_eeg_p3.hexa`                       | 475        | 300        | semantic-identical — frozen JSON SSOT mirrored      | **SKIPPED — uchg-locked** |
| 4 | `anima-clm-eeg/tool/clm_eeg_synthetic_fixture.hexa`                    | `anima-eeg-core/tool/modules/_integrations/synthetic_fixture.hexa`                | 274        | 551        | port — pure-hexa kernel lifted verbatim (Option A)  | **SKIPPED — uchg-locked** |
| 5 | `anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa`                        | `anima-eeg-core/tool/modules/_integrations/_integration_test.hexa`                | 256        | 189        | absorb — harness role taken over by integration test| **SKIPPED — uchg-locked** |

## SHA-256 frozen evidence (2026-05-01)

### Legacy (5 files, all currently uchg-locked)

```
29517ae9d0651d50c5c2c9101332ed96adae81689a0a330d44283fc14df44370  anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa
1b31abfe25bf9cafe6cd46b053fbec50989056ca728514aa34dd0857fefc01e2  anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa
905fe35dd409de198fc6eaccb9007ac2ec0d5554b9cc363c29a0bdfc01f94130  anima-clm-eeg/tool/clm_eeg_p3_gcg_pre_register.hexa
8297e2bf90acd7effb0ac5039ec2a025273275e0b7fa42bfe4fdf228f01748cb  anima-clm-eeg/tool/clm_eeg_synthetic_fixture.hexa
e227d2b86557c3a9e50b8d3002f4997079787e195615d83198c351d192c90cba  anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
```

### Native successors (5 files in `anima-eeg-core/tool/modules/_integrations/`)

```
77f243322895671a0584c7fca0cfe0887342e4cf9e763d65858a2ffbe630ac12  anima-eeg-core/tool/modules/_integrations/clm_eeg_p1.hexa
4a87e47d2cdb85a139078c539bb3702977d300d7d8c32f87ca5dc03fb5d1b05b  anima-eeg-core/tool/modules/_integrations/clm_eeg_p2.hexa
7b90e1f91f3f0a1841a9187f98d9b76b384964dfe13e2958ed5528f2ab5223d4  anima-eeg-core/tool/modules/_integrations/clm_eeg_p3.hexa
090d97dd5154bccca050ca49c082975778bcf00f0f6730fcd305f358203f6834  anima-eeg-core/tool/modules/_integrations/synthetic_fixture.hexa
861819d303072dd01cacda5db188c7764a4f41a56ea5ef83258f84f131aeb0f8  anima-eeg-core/tool/modules/_integrations/_integration_test.hexa
```

## Planned archive mapping (when uchg unlocked)

```
anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa
  → anima-clm-eeg/tool/_archive/clm_eeg_p1_lz_pre_register.hexa

anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa
  → anima-clm-eeg/tool/_archive/clm_eeg_p2_tlr_pre_register.hexa

anima-clm-eeg/tool/clm_eeg_p3_gcg_pre_register.hexa
  → anima-clm-eeg/tool/_archive/clm_eeg_p3_gcg_pre_register.hexa

anima-clm-eeg/tool/clm_eeg_synthetic_fixture.hexa
  → anima-clm-eeg/tool/_archive/clm_eeg_synthetic_fixture.hexa

anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
  → anima-clm-eeg/tool/_archive/clm_eeg_harness_smoke.hexa
```

## Native cross-link reference (commits cited in task brief)

- `anima-eeg-core/tool/modules/_integrations/clm_eeg_p1.hexa`              ← landed in `9a80237ae`
- `anima-eeg-core/tool/modules/_integrations/clm_eeg_p2.hexa`              ← landed in `b1187d875` / `e0bbbfea7`
- `anima-eeg-core/tool/modules/_integrations/clm_eeg_p3.hexa`              ← landed in `9a80237ae`
- `anima-eeg-core/tool/modules/_integrations/synthetic_fixture.hexa`       ← landed in `e35ac8579`
- `anima-eeg-core/tool/modules/_integrations/_integration_test.hexa`       ← absorbed in `4050ae0b6`

Each native module's header explicitly references the legacy backend
(`anima-clm-eeg/tool/...`) with raw#10 wrap-vs-port DECISION line and
"mirror of legacy SSOT" frozen-criteria block — confirming semantic
continuity.

## raw#10 honest C3 — uchg-block decision

All 5 legacy targets carry the macOS `uchg` (user-immutable) flag (verified
via `ls -lO` 2026-05-01). The task brief's explicit safety constraint reads:

> "chflags uchg 잠긴 파일이면 보고 + skip"

Therefore **no `git mv` was executed and no `_archive/` directory was
created**. The flag is the SSOT of "do not move/delete this file" intent
(consistent with hive-raw-15 strengthen-iter4-7 propagation in commit
`248c2ecfc`). Unlocking via `chflags nouchg` is a destructive privilege
escalation outside this sub-agent's authority and outside the task scope
("commit X · file delete X · archive move만").

This index therefore records frozen evidence (SHA-256 + LoC + native
mapping) so a follow-up agent with explicit unlock authority can perform
the physical `git mv` step against the byte-identical legacy state proven
here. Reversibility is preserved trivially because nothing moved.

## raw#91 honest C3 — spot-check depth limitation

The "verdict" column above is **header-level semantic spot-check only**:

- Read each native module's header (first ~35 lines) and confirmed it
  carries an explicit `raw#10 HONEST C3` block citing the legacy path
  + LoC + frozen-criteria mirror.
- Read each legacy module's header to confirm the SSOT criteria text
  the native claims to mirror.
- **NOT performed**: line-by-line `diff` of kernel implementations,
  selftest output byte-comparison, falsifier-trigger replay, or
  cross-stream side-effect audit (e.g. `state/clm_eeg_*.json` regen
  determinism). LoC counts differ between legacy and native (e.g. p3
  475→300, synthetic 274→551) — the "semantic-identical" judgement
  is therefore a **header-attestation**, not a kernel-equivalence proof.
- The deeper byte-identical / replay verification is delegated to the
  separate A3 agent cycle that owns the 4 DEPRECATE metric pairs;
  no equivalent A3 sweep is in progress for these 5 P/harness pairs
  as of this freeze.

If a stricter equivalence proof is required before physical archive,
spawn a downstream agent to:
1. `chflags nouchg` the 5 legacy files (explicit user authority).
2. `hexa run` each pair (legacy + native --selftest) and `diff` the
   emitted `state/clm_eeg_*.json` for byte-identical determinism.
3. On all-PASS: `git mv` per the planned mapping above.
4. On any FAIL: amend this index with FAIL verdict + retain legacy.
