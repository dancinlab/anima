# qmirror 2.0 closure synthesis spec — LANDED 2026-05-04 (handoff)

**Cycle:** anima qmirror 2.0 closure synthesis spec (pre-build, sister BGs running cond.11/12/13 in parallel)
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**Spec doc:** `anima/docs/qmirror_2_closure_spec_2026_05_04.md`
**Synth tool:** `anima/tool/qmirror_2_closure_synth.hexa`
**Marker:** `anima/state/markers/qmirror_2_closure_spec_landed.marker`
**Cost:** $0.00 (pure spec + dispatch logic; no execution)
**Wall:** ~1 cycle (spec author)

---

## TL;DR

Spec'd qmirror 2.0 closure synthesis BEFORE the 3 sister BG axes
(cond.11 stabilizer, cond.12 surface-d3, cond.13 CSCS) land. When they
land (in parallel) the dispatch tool `tool/qmirror_2_closure_synth.hexa`
fires (auto via 4 guards OR manual `hexa run`), reads all 5 verdict
files, computes composite verdict (FULL/PARTIAL/DEFERRED), and mutates
4 downstream artifacts plus the additive §10 append on the 1.0 closure
doc.

cond.9 (PASS) and cond.10 (PASS) are already landed; cond.11/12/13 are
pending sister BGs.

---

## Composite verdict logic (5 axes → 3 verdicts)

| n_pass | composite                      | semver bump        | publishability    |
|--------|--------------------------------|--------------------|-------------------|
| 5      | `qmirror_2_closure_FULL`       | 1.0.x → 2.0.0      | publishable       |
| 3-4    | `qmirror_2_closure_PARTIAL`    | 1.0.x → 2.0.0-rc.1 | rc with caveats   |
| ≤ 2    | `qmirror_2_closure_DEFERRED`   | NO bump            | 1.0 stable; backlog|

---

## F-QM-2-CLOSURE-1 (NEW composite falsifier)

```
F-QM-2-CLOSURE-1 PASSes IFF
  n_pass >= 4 AND
  state/markers/qmirror_closure_landed.marker exists AND
  docs/nexus_qmirror_closure_2026_05_03.md exists
```

Verifier:
```
jq -e '.composite_verdict | IN("qmirror_2_closure_FULL", "qmirror_2_closure_PARTIAL")' \
   state/qmirror_2_closure_2026_05_04/dispatch_audit.json \
&& test -f state/markers/qmirror_closure_landed.marker \
&& test -f docs/nexus_qmirror_closure_2026_05_03.md
```

---

## Files landed (this cycle, $0)

| file | LoC | purpose |
|------|-----|---------|
| `docs/qmirror_2_closure_spec_2026_05_04.md` | ~480 | spec doc, 10 sections |
| `tool/qmirror_2_closure_synth.hexa` | ~290 | dispatch synth, 7 steps, raw#9 STRICT |
| `state/qmirror_2_closure_spec_2026_05_04/spec_audit.json` | — | audit JSON |
| `state/qmirror_2_closure_spec_2026_05_04/dispatch_logic.json` | — | per-step + verdict→mutation table |
| `state/markers/qmirror_2_closure_spec_landed.marker` | — | marker |
| `docs/qmirror_2_closure_spec_landed_2026_05_04.ai.md` | — | this handoff |

---

## 5 honest C3 caveats (raw#10)

1. **Closure conditional on 3 sister BG landings.** Spec defers if any
   of cond.11/12/13 verdict.json is absent or partially-written. Synth
   marks PENDING and aborts unless `--force-on-missing`.

2. **Version bump irreversible per semver.** Once `hexa.toml` jumps
   `1.0.0 → 2.0.0` (FULL) or `1.0.0 → 2.0.0-rc.1` (PARTIAL) AND the
   `qmirror v2.0.0` git tag pushes, recovery is `2.0.1` patch — never
   silent yank. Idempotency guard 4 (marker absent) prevents
   double-bump.

3. **qmirror 1.0 stability not affected.** Spec MUST NOT mutate any
   1.0 cond verdict file or 1.0 closure doc semantics. The 1.0
   closure doc gets exactly one additive `## 10` section appended
   pointing to the 2.0 closure doc — body above line 558 untouched.

4. **IBM hardware anchor optional NOT required.** cond.13 default $0
   Aer path is the closure-eligible substrate. The optional $25 IBM
   Heron 2-pair anchor is opt-in; if engaged AND fails, do NOT
   band-revise without separate physics-aware cycle (mirrors 1.0
   cond.3 pain).

5. **qmirror 3.0 roadmap speculative.** Closure doc §7 lists
   candidates (magic-state distillation, FFI retirement, IIT
   scale-up) but they are NOT pre-registered conditions. Sister
   cycle must produce `qmirror_3_axes_spec_2026_05_XX.md` following
   2.0 axes spec methodology before any 3.0 work begins.

---

## Dispatch trigger (sister BG completion)

When all 3 sister BGs (cond.11/12/13) land, choose one:

**Auto:** if 4 guards hold (5 verdict files exist + hash-stable
≥ 60s + qmirror version is 1.0.x + 2.0 marker absent), a sister anima
cycle agent invokes `hexa run tool/qmirror_2_closure_synth.hexa`.

**Manual:** `hexa run tool/qmirror_2_closure_synth.hexa [flags]`
- `--dry-run`           — composes doc + audit; no artifact mutation
- `--force-on-missing`  — treats absent verdict.json as FAIL
- `--force-rewrite`     — overwrites existing closure doc + re-mutates

---

## Artifact mutations queued (gated on FULL or PARTIAL)

1. `docs/nexus_qmirror_closure_2026_05_03.md` — additive §10 append
2. `qmirror/CHANGELOG.md` — v2.0.0 or v2.0.0-rc.1 entry
3. `qmirror/hexa.toml` — version + closure block bump
4. `hexa-lang/tool/pkg/registry.tsv` — qmirror row version bump
5. `state/markers/qmirror_2_closure_landed.marker` — marker
6. `docs/qmirror_2_closure_landed_2026_05_04.ai.md` — closure handoff
7. `docs/qmirror_2_closure_2026_05_04.md` — NEW dedicated 2.0 closure doc

For DEFERRED: only items 5/6/7 fire; no version bump.

---

## Constraints honored

- raw#9 STRICT: 0 .py files added on Mac repo this cycle
- raw#10: 5 honest C3 caveats embedded in spec §6 (synth-time output adds 6th)
- raw#15: no personal paths in spec doc / audit JSONs / marker bodies
- $0: pure spec + dispatch logic
- DO NOT execute closure this cycle (deferred to sister BG landings)
- DO NOT mutate 1.0 closure doc semantics (additive append only)

---

## Pointers

- Spec: `docs/qmirror_2_closure_spec_2026_05_04.md`
- Synth tool: `tool/qmirror_2_closure_synth.hexa`
- Spec audit: `state/qmirror_2_closure_spec_2026_05_04/spec_audit.json`
- Dispatch logic: `state/qmirror_2_closure_spec_2026_05_04/dispatch_logic.json`
- Marker: `state/markers/qmirror_2_closure_spec_landed.marker`
- Sister cond 1.0 closure: `docs/nexus_qmirror_closure_2026_05_03.md`
- 2.0 axes spec: `docs/qmirror_2_axes_spec_2026_05_03.md`
- cond.9 verdict (PASS): `state/qmirror_2_cond9_tomography_2026_05_03/verdict.json`
- cond.10 verdict (PASS): `state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json`
- cond.11 expected: `state/qmirror_2_cond11_stabilizer_2026_05_04/verdict.json` (sister BG)
- cond.12 expected: `state/qmirror_2_cond12_surface_2026_05_04/verdict.json` (sister BG)
- cond.13 expected: `state/qmirror_2_cond13_cscs_2026_05_04/verdict.json` (sister BG)
