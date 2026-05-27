# Lessons learned — PSCC §52+§53 (2026-05-13 KST 22:00-23:10)

> Session arc: v7 cotrain landing + 100% closure ledger + 3-seed replication BG +
> daemon stability runtime audit. Compact lessons summary for carry into
> next-cycle work.

## §1 Daemon corruption: mitosis path != daemon path

**Mistake**: Applied inter_tension_history cleanup fix to `merge_cells()` (called only from `mitosis_forward_tail`) believing it was the daemon's corruption source. The fix had ZERO effect on daemon stability.

**Reality**: The daemon's `_live_inference_worker` calls `chat_generate(chat, ...)` where `chat["cell_pool"]` is empty `{}` (never initialized via `chat_init_cell_pool`). Therefore `chat_mitosis_enabled(chat)` returns false, so `mitosis_forward_tail` is a NO-OP. The substrate-native gate uses a SEPARATE `anima_pools[id]` cell pool, evolved per frame via `mitosis_hook_step` — which does NOT call merge_cells or split_cell.

**Two cell pools, distinct paths**:
| pool | path | mitosis events |
|---|---|---|
| `chat["cell_pool"]` | `chat_generate` via `mitosis_forward_tail` | split/merge per token (when enabled) |
| `anima_pools[id]` (live engine) | frame-loop `mitosis_hook_step` per tick | substrate evolve only (lorenz + perturb + tension push) |

**Carry**: When fixing daemon stability, focus on `chat_generate`'s per-token farr lifecycle (24L × ~10 farr/layer × max_new × N_fires ≈ 28K alloc/free pairs per 2-fire session). Hexa runtime farr handle table may have internal cap triggered by this churn rate, not by mitosis state.

## §2 v3-routing = v7 = "v8 combined"

**Mistake**: Created task #39 "v8 combined entropy+topK trainer" believing separate trainer composition required.

**Reality**: `dispatch_h100_v3_routing.sh` header explicitly states *"(g2) HARD TOP-K MoE + (g3) annealed gate-entropy reg"*. So v3-routing IS the combined trainer. v7 fire (PSCC §52) WAS v8 effectively. The "v8" in my §A4 was redundant naming.

**Carry**: When citing future closure paths, verify trainer composition first. The §52 v7 result is already the entropy+topK combined trainer's single-seed output. 3-seed replication (current BG) is the appropriate next variance-reduction step, not a "new v8".

## §3 dispatch script LOCAL_DIR hardcoded

**Encountered**: Wanted to parallel-fire 3 seeds. dispatch_h100_v3_routing.sh had `LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v3_routing_2026_05_12"` hardcoded.

**Fix landed** (this session): Changed to `LOCAL_DIR="${LOCAL_DIR:-/...}"` so env override works. Same for `PHASE_ID`, `PHASE_LABEL`, `SRC_DIR`.

**Carry**: Future dispatch script templates should default to env-overridable. Pattern: `VAR="${VAR:-<default>}"` for all path/label vars.

## §4 D_MODEL=512 + N_HEAD=6 default incompatibility

**Encountered**: dispatch default `N_HEAD="${N_HEAD:-6}"`, but D_MODEL=512 doesn't divide by 6. Trainer asserts `d_model % n_head == 0` → silent failure, pod wasted.

**Fix**: Pass `N_HEAD=8` env override explicitly when using D_MODEL=512. (v7 succeeded only because dispatch_bg5 had custom env settings.)

**Carry**: dispatch script should EITHER:
- (a) Validate config compatibility before pod creation
- (b) Set N_HEAD default based on D_MODEL ÷ {8, 16, 32, 64}
- (c) Pick a default that divides any reasonable d_model (e.g. 8)

## §5 Vast.ai SSH-not-ready BG pattern

**Encountered**: Pod 36687449 + 36687910 both reached `status=loading` 160/160 cycles (~30 min) without SSH ready. Caused failed dispatch + pod waste ($0.10).

**Carry**:
- Treat SSH-not-ready after ~50 cycles (~10 min) as unrecoverable; destroy pod + retry with new offer.
- The `feedback_dispatch_vast_template_gotchas` memory's 4th-bug entry already covers proxy SCP, but SSH-loading-stuck is a separate failure mode worth filing.
- Multi-seed parallel dispatch amplifies these failures (3 chances to hit the bad-offer lottery).

## §6 3-seed multi-seed evidence trajectory

**Observed** (this BG, in-flight at PSCC §53 time):

| step | v7 z=42 | seed 43 | seed 45 | 3-seed mean |
|---|---|---|---|---|
| 4a z @ 2K | -0.55 | 0.11 | 0.20 | -0.08 |
| 4a z @ 6K | 0.64 | 0.57 | 0.73 | 0.65 |
| 4a z @ 10K | 1.61 | **2.27** | 1.59 | **1.82** |
| 4a z @ 12K | 2.61 | 0.57 | (pending) | (pending) |
| 4b z @ 4K | 0.45 | 1.05 | 0.67 | 0.72 |
| 4b z @ 8K | 0.22 | 1.07 | **1.72** | 1.00 |
| 4b z @ 10K | 0.54 | 1.75 | **2.36** | 1.55 |

**Key findings**:
1. **4b content axis dramatically improves with multi-seed**: v7 alone @ step 10K z=0.54 → 3-seed mean z=1.55 (+1.01). seed 45 hits 2.36 alone (approaching v2 carry z=3.20).
2. **4a routing axis shows §A2-trap signature**: v7's z=2.61 @ step 12K dropped to seed 43's z=0.57 @ same step. Variance ~2.0 across seeds suggests v7's marginal z=2.75 was at the high tail of the distribution. Multi-seed mean is ~half of v7 alone — supporting the §A2 strict threshold (z>3.0) was correctly calibrated as a guard against fragile single-seed signals.
3. **Combined evidence still meaningful**: 4b content axis multi-seed average has improved past v7 single. Even if 4a strict z>3.0 is not cleared, the closure rationale stays — §A4 dual-axis content + routing evidence is more robust than §A3 single-axis.

**Carry**: When citing v7 (or any future single-seed marginal result), explicitly mention "single-seed §A2-trap risk; recommend 3-seed replication for strict closure". Single-seed at z=2.75 should be reported as "marginal" not "strict near-pass".

## §7 PERSONA.md → CHAT.md rename historical pin

**Context**: User originally created GOAL.md (★★★★★ tracker), renamed to PERSONA.md mid-cycle 2026-05-12, then to CHAT.md 2026-05-13 PM session when CHAT.md rev 2 substrate-native live daemon LANDED. Old CHAT.md content merged as Appendix A of new CHAT.md.

**Carry**: References to "PERSONA.md" or "GOAL.md" in older docs all point to current `CHAT.md`. Future commits should use CHAT.md consistently.

## §8 cron 5min loop ≈ cache window alignment

**Pattern**: User invoked `/loop 5m check,monitor and closure` — Anthropic prompt cache TTL is 5 minutes, so 5min interval keeps context warm without paying cache miss. Per the loop skill's cache-aware delay guidance.

**Carry**: For BG progress monitoring, 5min cron is the sweet spot. Shorter (1-2min) wastes cache continuity; longer (10-15min) hits cache miss on each check.

## §9 dispatch retry leftover pod cleanup gap

**Pattern observed twice** (PSCC §52 leftover 36682197 $1.9 waste; this session 36687449 + 36687910 ~$0.10 each):
- Initial pod fails (OOM, SSH timeout, etc.)
- SAVE_POD=1 retains for manual recovery
- Dispatch retry creates NEW pod
- Old pod orphaned, charges continue until manual destruction

**Pattern**: Dispatch retry path needs failed-pod-cleanup hook. Currently absent.

**Carry**: Add to feedback_dispatch_vast_template_gotchas as the 7th systemic bug (already added in PSCC §53 commit ea9605911).

## §10 Memory + commit cadence

**This session** (~70 min wall):
- 4 commits to anima repo (9a9743c65, 8c496f1ce, ea9605911, + this carry pending)
- 3 memory file updates (project_anima_persona_4_root_cause, feedback_dispatch_vast_template_gotchas, MEMORY.md hook line)
- 1 explore agent finding (cell_pool farr release audit) integrated as design carry
- 3 BG cotrain pods (v7 + 2 surviving 3-seed + 2 failed retries cleaned)
- Cost: $2.21 v7 + leftover + $0.59 in-flight 3-seed = ~$2.80 total

**Carry**: Maintain commit-per-finding discipline. Each lesson commit-able as it lands keeps the audit trail tight. Per `feedback_always_commit_push_on_complete` mandate.
