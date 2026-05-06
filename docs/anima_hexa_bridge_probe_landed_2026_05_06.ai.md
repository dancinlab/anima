# anima hexa bridge probe — landed 2026-05-06

**Status:** PROBE_COMPLETE_3_OF_3_PASS / Cost $0 / Wall ~30min
**Lane:** anima_clm_3_original_ubu1_path
**Trigger:** BG-FH hexa runner / anima-hexad bridge probe + .own opt-out fallback

## Summary

Three-sub-task probe answering "can train_clm.hexa be the fire artifact, or do we route to .py via opt-out?". Verdict: use Path C (existing ready/training/train_clm.py via ssh; own 1 ready/ jurisdiction-out + ssh substrate-exempt; zero new work). Path B (emit-py-pattern wrapper) is anima official long-term recommendation but yields no smoke quality benefit. Path A (direct hexa-port fill) is infeasible at current hexa-lang maturity (numeric stdlib proposal-only; 624/643 audit pairs STUB; train_clm.hexa is 14.4% LoC scaffolding with 8 TODOs and 5 critical execution-path blockers).

## Sub-1: hexa runner / bridge

| target | result |
|--------|--------|
| `which hexa` mac | `/Users/ghost/.hx/bin/hexa` (0.1.0-dispatch shim -> hexa.real) |
| `which hexa` ubu1 | EMPTY (no binary) |
| anima-hexad PyTorch FFI bridge | NONE — bridge/__init__.hexa is pure hexa re-export |
| anima-hexad runtime model | description/shape layer; numeric ops delegate to .py on substrate |
| hexa_port_audit.json (2026-04-10) | 643 pairs / STUB 624 / PARTIAL 17 / COMPLETE 2 / 0.31% complete |

## Sub-2: train_clm.hexa TODO density

- 311 LoC hexa vs 2165 LoC .py (14.4% ratio)
- 8 TODO markers; 5 are execution-path blockers (load_corpus, get_batch, save_checkpoint, train_step, train_scale)
- Header self-declares "Phase 2c structural port; PyTorch ops -> TODO comments"
- ~85% structural scaffolding (ScaleConfig × 5, PhaseManager P1/P2/P3, struct definitions, verify_phi_non_destructive Law 49 impl) PRESENT
- Path A direct fill estimate: ~3000 LoC, 2-4 weeks, blocked on numeric stdlib

## Sub-3: .own opt-out

- `/Users/ghost/core/anima/.own` is single root-level SSOT (633 LoC, mk2 frontmatter)
- own 1 line 83 ALREADY contains: `opt-out ready/ — historical corpus archive, .gitignore'd; raw 9 jurisdiction-out (1431 files)`
- `ready/training/train_clm.py` is covered by this opt-out — NO new declaration needed
- `emit_smoke_command.txt` is raw 9 / own 1 compliant as written
- Memory feedback decision tree confirms: "Archive / grandfathered (ready/)? -> Already .own 1, leave alone"

## Three-path comparison

| Path | LoC | Wall | Cost | Feasibility |
|------|-----|------|------|-------------|
| A direct hexa fill | 3000 | 2-4 weeks | $0 | BLOCKED on numeric stdlib |
| B emit-py-pattern wrapper | 600 | 3-5h (1-2d realistic) | $0 | VIABLE (anima official rec) |
| C use .py via own 1 + ssh | 0 | 0 min | $0 | ZERO-COST IMMEDIATE |

## User decisions

- D1 fire_path = **C** default (B optional later cycle for .hexa-source-of-truth purity)
- D2 emit_smoke_command.txt comment = OPTIONAL cosmetic
- D3 train_clm.hexa fire-ready upgrade = DEFER (no measurement benefit)

## Honest C3

C1 read-only probe (ubu1 hexa absence verified by which-empty, not by failed run)
C2 train_clm.hexa is scaffolding not runtime — treating fire-ready violates raw 10
C3 .own audit scoped to anima local; hive raw 9 base + hexa-lang stdlib referenced indirectly
C4 hexa_port_audit.json 26 days stale; current may differ
C5 Path B 3-5h estimate borrowed from design doc; train_clm specifically may be 1-2d realistic

## Next fire recommendation

**Path C — proceed with emit_smoke_command.txt as-written.** Real blockers per preflight.json
are (a) ubu1 repo sync gap (mac HEAD 2f246b79 vs ubu1 HEAD 6407920; ready/ empty on ubu1)
and (b) corpus_mix_70wiki_30dialogue.txt build (does not exist on mac yet). Neither blocker
is raw 9 / own related; both are operational gating. User kick = FALSIFIER-LOCK-UBU1 sign-off
+ corpus build BG launch.

## Outputs

- /Users/ghost/core/anima/state/anima_hexa_bridge_probe_2026_05_06/verdict.json
- /Users/ghost/core/anima/state/anima_hexa_bridge_probe_2026_05_06/hexa_runner_findings.txt
- /Users/ghost/core/anima/state/anima_hexa_bridge_probe_2026_05_06/train_clm_hexa_todo_audit.txt
- /Users/ghost/core/anima/state/anima_hexa_bridge_probe_2026_05_06/own_opt_out_plan.txt
- /Users/ghost/core/anima/docs/anima_hexa_bridge_probe_landed_2026_05_06.ai.md (this file)

## raw_compliance

- raw 9: own 1 grandfather analysis only — no new tool/.py landed
- raw 10: honest disclosure — train_clm.hexa scaffolding status documented, NOT obscured
- raw 15: no LOCKED files modified
- raw 37: transient outputs under state/ namespace
- no token leak, no commit
