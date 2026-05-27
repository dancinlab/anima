---
schema: anima/monitor/module/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:               monitor/module/law_gate_auto.hexa
  inputs:
    convergence_state: shared/convergence/anima.json
    laws_ssot:         config/consciousness_laws.json
status: live — single-file unattended absorption-gate automation; line-based JSON walker
roadmap_entry: 270
raws:
  - R18 minimal
  - R1 hexa-native
  - AN7 safe path
---

# anima monitor modules (AI-native)

Unattended absorption-gate automation for Anima laws. Single-file hexa engine that turns the manual `stage_1 → stage_2 → stage_3 → stage_4` law promotion pipeline into an autonomous monitor.

## TL;DR for an agent reading this cold

- **1 file**, 589 LOC: `law_gate_auto.hexa`.
- Read-only on inputs (`shared/convergence/anima.json`, `config/consciousness_laws.json`); writes promoted laws to `consciousness_laws.json` once stage_4 reached.
- **Line-based JSON walker** — NO byte/char arithmetic. Every field lookup iterates already-split line list within a clearly-bounded sub-block. Survives concurrent edits from Agent B safely.
- Currently scans + verifies; **promotion (stage_2 → stage_3 → stage_4) eventual goal**, present implementation is read-side audit + advisory.
- Schema v1.0 fields: `.stage (1..4)` / `.status (PROVISIONAL|STABLE|FAILED)` / `.grade (EXACT|CLOSE|...)` / `.cross_domain_exact[]` / `.stage_2_verified_at` + `.stage_2_evidence` / `.stage_3_pass` + `.stage_3_evidence`.

## Architecture map

```
monitor/module/
└── law_gate_auto.hexa     589 LOC — absorption-gate automation engine
```

Inputs (read-only):
```
shared/convergence/anima.json     ← absorbed_open[] schema v1.0
config/consciousness_laws.json    ← promoted laws SSOT (laws.{id}: text)
```

Output (write — eventual):
```
config/consciousness_laws.json    ← append promoted law row at stage_4
```

## API contract

```hexa
// CLI invocation (no public fns; whole-file driver)
hexa run monitor/module/law_gate_auto.hexa [--scan | --watch] [--dry-run]
//   --scan      one-shot pass over absorbed_open[]
//   --watch     repeat every N seconds (default 60)
//   --dry-run   print intended promotions, don't write

// Internal: line-based field walker
fn find_field(lines: [string], key: string, sub_block_start: int, sub_block_end: int) -> Option<string>
```

## Stage promotion logic

```
Stage 1 (PROVISIONAL grade=EXACT|CLOSE)
  → check cross_domain_exact[] non-empty (≥2 domains agree)
       → promote to Stage 2, set .stage_2_verified_at + .stage_2_evidence
            → manual review gate (human-in-loop, currently)
                 → Stage 3: stage_3_pass=true
                      → Stage 4: append to consciousness_laws.json laws.{id}
```

## Failure modes

- **Concurrent edit from Agent B** — line-walker is robust by design (sub-block scoped, no byte arithmetic). A row appended mid-scan is either fully visible or fully invisible; never partially-corrupt.
- **Missing schema field** → walker returns `None`; row skipped with WARN log. No promotion attempted.
- **`config/consciousness_laws.json` write race** — currently no file lock. Two concurrent monitors can race; recommended: run from cron exclusive.
- **`status=FAILED` rows skipped silently.** Verify by inspecting the input json; FAILED rows do NOT trigger demotion logic (one-way pipeline).

## raw#10 caveats

1. **Promotion is currently advisory only.** Engine identifies eligible candidates; actual promotion to `consciousness_laws.json` requires explicit `--commit` flag (or human gate). Don't expect autonomous law writes today.
2. **Schema v1.0 frozen.** Adding fields (e.g. `stage_3_pass`) requires walker updates — no auto-discovery of new keys.
3. **Hexa-native line walker is slower than JSON parse.** For large absorbed_open[] (>10k rows), batch parse is preferable. Current scale (~100 rows) is fine.
4. **No timestamp validation.** `stage_2_verified_at` accepted as-is; clock-skew between hosts can produce out-of-order promotion.
5. **AN7 safe path** — engine refuses to write outside `config/consciousness_laws.json` even with `--commit`. Other paths require source edit.
6. **Single-monitor assumption.** No leader-election. Running 2 instances → race + duplicate audit rows.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `law_gate_auto.hexa` | `1adfc668dccb6ec5cc4189d33bfd0276f5a37466cd5e43e98dc3162760c2fb58` | 589 |

shas pinned 2026-05-02.
