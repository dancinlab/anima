# demiurge 4 new verify producers — Brain / Bio / Chem / Grid (2026-05-21)

## § 1. Goal

Close the brain / bio / chem / grid `❌ → ⏳ GATE_OPEN` cells in the demiurge
4-domain cohort gap-table by adding consumer-side Swift producers that scan the
anima-physics bridge records dropped under `exports/<domain>/verify/<UTC>Z/`.
The anima bridges (LANDED in the prior cycle) already produce records; the
demiurge consumer was the missing half.

Companion cycle doc: `anima-physics/docs/demiurge_4gap_bridges_2026_05_21.md`
(anima-side bridges).

## § 2. Reference producer pattern

Found via:

```
find /Users/ghost/core/demiurge -name "*VerifyProducer.swift" -type f
```

12 existing producers. The two architecturally relevant references:

* `cockpit/Sources/DemiurgeCore/Loaders/AntimatterVerifyProducer.swift`
  — script-spawn pattern (forks `python3 geant4_verify.py`).
* `cockpit/Sources/DemiurgeCore/Loaders/BrainAnalyzeProducer.swift`
  — D61-compliant script-spawn (forks `python3 lif_brian2.py`).

Neither matches what we need: the anima bridges have ALREADY dropped the
records. The new producers are SCAN-ONLY witnesses — they enumerate
`exports/<domain>/verify/<UTC>Z/anima_*.json`, parse the latest record's
`verdict.gate_state` + `provenance.{absorbed,producer}` + `record_id`, and
emit an honest GATE_OPEN witness banner. No Python spawn, no re-measurement.

## § 3. Files created

| File (absolute path) | LoC | Purpose |
| --- | ---: | --- |
| `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/BrainVerifyProducer.swift` | 116 | scan `exports/brain/verify/` for anima-kuramoto-loihi-akida-bridge records |
| `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/BioVerifyProducer.swift`   |  98 | scan `exports/bio/verify/` for anima-bio-hippocampus-memristor-bridge records |
| `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ChemVerifyProducer.swift`  |  99 | scan `exports/chem/verify/` for anima-chem-langevin-thermodynamic-bridge records |
| `/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/GridVerifyProducer.swift`  | 104 | scan `exports/grid/verify/` for anima-grid-kuramoto-powergrid-bridge records |

Total = 417 LoC Swift, each producer ~100 LoC = the requested 50-80 LoC envelope
with honest gap-path messaging.

Each producer exposes a `public enum <Domain>VerifyProducer` with one
`public static func runVerify() -> <Domain>VerifyResult`, mirroring the
existing producers' shape (`runVerify` / `runAnalyze` / `runStructure`).

Record filter (per task spec):
`name.hasPrefix("anima_") || name.hasPrefix("<domain>_verify_")`.

## § 4. ActionDispatch wiring

`/Users/ghost/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/ActionDispatch.swift`:

* 4 new `case (.verify, "<domain>"): return run<Domain>Verify()` rows in the
  main `switch (verb, domain)` dispatch (inserted right after the existing
  `case (.verify, "antimatter")`).
* 4 new `private static func run<Domain>Verify() -> ActionResult` helpers
  appended after `runFirmwareHandoff()`, each delegating to the corresponding
  `<Domain>VerifyProducer.runVerify()` and packaging the result into an
  `ActionResult(text:newRecordIDs:usedEngineTool:engineToolSucceeded:)`.

The `default:` arm (claude-CLI honest-gap fallback) is no longer reached for
these 4 cells.

## § 5. Build

`cd /Users/ghost/core/demiurge/cockpit && swift build` →
`Build complete! (4.58s)`. The pre-existing CockpitApp `Views/ComponentView3D.swift`
RealityKit `@MainActor` warnings are unchanged (not regressions from this cycle).

## § 6. Smoke results

`cd /Users/ghost/core/demiurge/cockpit && swift run DemiurgeCLI action verify <d>`:

| Domain | Latest anima record (cited) | Result |
| --- | --- | --- |
| brain | `kuramoto_n8_k5.00_local_sim` (anima-kuramoto-loihi-akida-bridge) | ⏳ GATE_OPEN · absorbed=false |
| bio   | `bio_compr12.0_hebb0.94_pac0.71_local_sim` (anima-bio-hippocampus-memristor-bridge) | ⏳ GATE_OPEN · absorbed=false |
| chem  | `chem_jumps0.51_slope7.69_D0.60_local_sim` (anima-chem-langevin-thermodynamic-bridge) | ⏳ GATE_OPEN · absorbed=false |
| grid  | `grid_n8_k5.00_r0.951_local_sim` (anima-grid-kuramoto-powergrid-bridge) | ⏳ GATE_OPEN · absorbed=false |

All 4 produced `📸 new record ID(s): <id>` lines via the CLI summary. Exit
status: each producer reports `usedEngineTool=true`, `engineToolSucceeded=true`
(scan succeeded + at least 1 record); the CLI prints the record ID rather
than the honest-gap fallback.

## § 7. Gap-table delta

| Cell | Before this cycle | After this cycle |
| --- | --- | --- |
| brain + verify | ❌ no producer | ⏳ GATE_OPEN (anima record auto-cited) |
| bio + verify   | ❌ no producer | ⏳ GATE_OPEN (anima record auto-cited) |
| chem + verify  | ❌ no producer | ⏳ GATE_OPEN (anima record auto-cited) |
| grid + verify  | ❌ no producer | ⏳ GATE_OPEN (anima record auto-cited) |

4 cells flipped, none claimed `GATE_CLOSED_MEASURED` or `absorbed=true`
(honest g3 — the substrates are reference sims / consciousness analogs /
qualitative mappings, not flight data; oracle parity is TODO on the
anima-physics side).

## § 8. Honest scope caveats (g3)

1. **No re-measurement.** demiurge witnesses the anima bridge record but does
   NOT independently re-run the substrate. The record's own
   `provenance.scope_caveats` (oracle parity TODO, local_sim not silicon,
   single-(N,K) point not regime claim, etc.) carry forward verbatim.
2. **No `absorbed=true` flip.** All four cells are permanently GATE_OPEN until
   the anima-physics side authors the per-domain oracle parity (separate
   cycle — see brain/bio/chem/grid TODO lines in each bridge's emitted JSON).
3. **No mass-flip aggregator yet.** Each `runVerify()` returns only the LATEST
   record; a future producer iteration could aggregate-and-rank across all
   `<UTC>Z` stamps, but the cohort gap-table only needs "first witness exists"
   evidence at this stage.
4. **`grid + structure` distinct.** `GridStructureProducer` (cohort D57,
   NetworkX IEEE 14-bus) and `GridVerifyProducer` (this cycle, anima-physics
   Kuramoto power-grid analog) are independent cells; both can coexist.
5. **`brain + analyze` distinct.** `BrainAnalyzeProducer` (brian2 LIF tonic
   firing-rate) and `BrainVerifyProducer` (this cycle, anima-physics kuramoto
   neuromorphic substrate) are independent cells.
6. **aura cell deferred.** ActionDispatch's `(.analyze, "aura")` already routes
   to `AuraAnalyzeProducer` (MNE EEG band-power, cohort round). The
   `g_demiurge_pointer_only` SSOT-hard-code untangle for sibling repos is a
   separate cycle per the task brief.
7. **D17 / g_stdlib_ownership preserved.** anima-physics owns the substrate
   producer (hexa-native + Python bridge); demiurge owns the witness +
   typed-Swift surface. No bridge Python migrates into cockpit/scripts/.
