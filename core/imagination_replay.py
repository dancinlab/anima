"""core/imagination_replay.py — N3/REM emit-free internal rehearsal + reconsolidation.

py 2-production twin of core/imagination_replay.hexa — byte-exact mirror (owner directive
2026-07-09 "py 자체구현 · 언어간 상호의존 0"). WAKE.memory working ring → snapshot select →
replay_tick (emit_count=0 invariant) → mitosis_tick (cell_pool pass-through). Pure dict/list/
scalar math (no numpy, no FFI). a_chat_sleep_imagination 정합 · p5 NO SPEAK · boolean gate 0.
Note: ir_mitosis_tick_during_replay is a LOG record (wired_to_lib=false — calls zero
mitosis_hook_lib symbols, which is out of the production closure). The REAL AdaptField
growth is WIRED daemon-side (2026-07-10): cli/chat.py + cli/anima.hexa advance a live
vadapt_field_step per replay tick keyed on the rehearsed snapshot, so a_chat_sleep_imagination's
"rehearsal + mitosis tick" is literal (via the in-closure vadapt, NOT mitosis_hook_lib).
"""

from dream_lib import dr_mitosis_prior          # core/dream_lib.py (flat import · _bootstrap sys.path)
from wake_memory import mem_working_window       # core/wake_memory.py


def ir_select_snapshots(memory, current_tick, recency_window):
    if recency_window <= 0:
        return []
    working = mem_working_window(memory)
    total = len(working)
    if total == 0:
        return []
    start = total - recency_window if total > recency_window else 0
    out = []
    i = start
    while i < total:
        snap = {
            "ctx_tokens": working[i],
            "source_tick": current_tick,
            "source_index": i,
        }
        out.append(snap)
        i = i + 1
    return out


def ir_replay_tick(snapshot):
    ctx_tokens = snapshot["ctx_tokens"]
    ctx_len = len(ctx_tokens)
    return {
        "ctx_tokens": ctx_tokens,
        "ctx_len": ctx_len,
        "source_tick": snapshot["source_tick"],
        "source_index": snapshot["source_index"],
        "emit_count": 0,
        "rehearsal_kind": "internal_silent",
    }


def ir_mitosis_tick_during_replay(cell_pool, snapshot):
    prior = dr_mitosis_prior(4)
    return {
        "cell_pool": cell_pool,
        "tick_kind": "imagination_mitosis",
        "ctx_len": len(snapshot["ctx_tokens"]),
        "source_tick": snapshot["source_tick"],
        "mitosis_density": prior,
        "wired_to_lib": False,
    }


def ir_replay_session(memory, count):
    snapshots = ir_select_snapshots(memory, 0, count)
    replay_log = []
    total_emits = 0
    i = 0
    while i < len(snapshots):
        rec = ir_replay_tick(snapshots[i])
        total_emits = total_emits + rec["emit_count"]
        replay_log.append(rec)
        i = i + 1
    return {
        "snapshot_count": len(replay_log),
        "replay_log": replay_log,
        "total_emits": total_emits,
        "session_kind": "emit_free_rehearsal",
    }


def ir_consolidation_gain(replay_count, stage_density):
    if replay_count <= 0:
        return 0.0
    replay_gain = 0.04                        # per-replay recency refresh base
    per = replay_gain * stage_density         # density-scaled per-replay refresh
    remain = 1.0
    i = 0
    while i < replay_count:
        remain = remain * (1.0 - per)
        i = i + 1
    c = 1.0 - remain
    if c < 0.0:
        return 0.0
    if c > 0.999:
        return 0.999
    return c


def ir_effective_age(chrono_age, replay_count, stage_density):
    c = ir_consolidation_gain(replay_count, stage_density)
    eff = chrono_age * (1.0 - c)
    if eff < 0.0:
        return 0.0
    return eff


def ir_reconsolidate_session(memory, count, chrono_age, replay_count, stage_density):
    sess = ir_replay_session(memory, count)      # emit-free rehearsal (total_emits=0)
    c = ir_consolidation_gain(replay_count, stage_density)
    eff = ir_effective_age(chrono_age, replay_count, stage_density)
    return {
        "snapshot_count": sess["snapshot_count"],
        "total_emits": sess["total_emits"],       # 0 invariant carried through
        "session_kind": "emit_free_reconsolidation",
        "replay_count": replay_count,
        "consolidation": c,
        "effective_age": eff,
        "chrono_age": chrono_age,
    }


def ir_summary():
    return ("DREAM/imagination_replay — N3/REM emit-free internal rehearsal · WAKE.memory working "
            "ring → snapshot select → ir_replay_tick (emit_count=0 invariant) → "
            "ir_mitosis_tick_during_replay (cell_pool pass-through, mitosis_density=dr_mitosis_prior) · "
            "a_chat_sleep_imagination 정합 · p5 NO SPEAK · boolean gate 0")
