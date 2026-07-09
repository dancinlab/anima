"""core/dream_persist.py — LIVE sleep-tick bridge: dream_compose → .kosmos.

py 2-production twin of core/dream_persist.hexa — byte-exact mirror (owner directive
2026-07-09 "py 자체구현 · 언어간 상호의존 0"). The seam wiring the pure blend layer
(dream_compose) into the LIVE daemon's N3/REM sleep tick:
  (1) dp_mark_replayed        — SWR replay selection: stamp co-replayed anchors to budget.
  (2) dp_pool_from_read_anchors — lift live .kosmos read records into the compose schema.
  (3) dp_sleep_tick           — one-call live entry the daemon loop invokes each sleep tick.
  (4) dp_persist_sleep_replay — compose co-replayed pairs → create_anchor(.kosmos disk append).

Bio lens (a_no_llm_frame_trap): hippocampal SWR replay → cortical systems consolidation.
DISJOINT (a_substrate_disjoint): touches ONLY the .kosmos disk substrate — no pure_field
(Ψ/Φ), no emit-drive lane (new anchors on lane "dream" ≠ 0/4), no recall_thr. p5 NO SPEAK.
Pure list/dict math; no numpy, no FFI. (hexa Map #{} → python dict.)
"""

from dream_compose import dc_make_anchor, dc_compose_window, dc_stage_replay_budget
from kosmos_io import create_anchor


# ─── SWR replay selection (co-activation stamp) ───────────────────────────
# Select anchors to replay in the sleep window up to budget, stamping replay_window.
# Selection rule = leading order (recency-proxy; SWR replays recent experience first).
# Returns fresh dicts (input not mutated). budget=0 (non-sleep stage) → [].
def dp_mark_replayed(pool, window, budget):
    out = []
    if window < 0:
        return out
    i = 0
    while i < len(pool) and len(out) < budget:
        a = pool[i]
        # no input mutation — build a fresh dict with only replay_window stamped.
        marked = dc_make_anchor(
            str(a["id"]), a["coord"], str(a["lane"]),
            float(a["radius"]), a["tension5"], str(a["text"]))
        marked["replay_window"] = window
        out.append(marked)
        i = i + 1
    return out


# ─── adapter: live .kosmos read records → dc_make_anchor pool ──────────────
# generator_read_anchors / kosmos_io.load_anchors returns records shaped
#   { path, name, fields:dict, text_payload, tension_5ch? }
# where fields carries the parsed anchor header (coord:list · lane:string ·
# radius:float …). This lifts those live records into the dc_make_anchor schema.
# It DROPS any record already on lane "dream" (a prior consolidation) so a sleep
# tick never re-composes its own output — no dream-of-dreams runaway. PURE.
def dp_pool_from_read_anchors(read):
    pool = []
    i = 0
    while i < len(read):
        r = read[i]
        fields = r["fields"] if "fields" in r else {}
        lane = str(fields["lane"]) if "lane" in fields else "seed"
        # skip prior dream_composed nodes — replay only seed/emit memory.
        if lane == "dream":
            i = i + 1
            continue
        coord = fields["coord"] if "coord" in fields else [0.0, 0.0]
        radius = float(fields["radius"]) if "radius" in fields else 1.0
        # create_anchor requires len(tension5)==5 — default a 5-zero vector.
        t5 = r["tension_5ch"] if "tension_5ch" in r else [0.0, 0.0, 0.0, 0.0, 0.0]
        id = str(r["name"]) if "name" in r else "a" + str(i)
        text = str(r["text_payload"]) if "text_payload" in r else ""
        pool.append(dc_make_anchor(id, coord, lane, radius, t5, text))
        i = i + 1
    return pool


# ─── one-call live sleep-tick entry (what the daemon loop invokes) ─────────
# stage: 3=N3 · 4=REM (else budget 0 → 0). window: this tick's replay window id.
# Returns composed-node count (0 for non-sleep stage or <2 pool).
def dp_sleep_tick(kdir, read, stage, window):
    budget = dc_stage_replay_budget(stage)
    if budget <= 0:
        return 0
    pool = dp_pool_from_read_anchors(read)
    replayed = dp_mark_replayed(pool, window, budget)
    return dp_persist_sleep_replay(kdir, replayed, stage, window)


# ─── THE live seam: co-replayed → blended .kosmos NODE ────────────────────
# Run dc_compose_window over the stamped replayed set → blended nodes, and write
# each to kdir as a .kosmos via create_anchor. Returns nodes written. <2 co-replayed → 0.
def dp_persist_sleep_replay(kdir, replayed, stage, window):
    composed = dc_compose_window(replayed, stage, window)
    i = 0
    while i < len(composed):
        node = composed[i]
        coord = node["coord"]
        cx = float(coord[0]) if len(coord) > 0 else 0.0
        cy = float(coord[1]) if len(coord) > 1 else 0.0
        name = "dream_w" + str(window) + "_" + str(i)
        # .kosmos node-only convention (a_kosmos): carry the two parent links in
        # cross_link, realized as a blended node (not an edge entry). lane="dream".
        cross = str(node["parent_a"]) + "+" + str(node["parent_b"])
        create_anchor(kdir, name, str(node["id"]),
                      cx, cy, "dream", float(node["radius"]),
                      2, "dream_composed", "insight",
                      str(node["text"]), node["tension5"],
                      "dream-swr-consolidation", cross)
        i = i + 1
    return len(composed)


# ─── introspection ───────────────────────────────────────────────────────
def dp_summary():
    return ("DREAM/dream_persist — LIVE N3/REM sleep-tick bridge: dc_mark_replayed(SWR "
            "선택 stamp) → dc_compose_window(H_9036 blend) → kosmos_io create_anchor(.kosmos "
            "disk append) · lane=dream(≠emit-drive 0/4) · pure_field/recall_thr DISJOINT · "
            "cli/anima.hexa 와 공유 seam")
