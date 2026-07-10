#!/usr/bin/env python3
"""H_1058 agency-T — frozen-emission replay-depth prober (FABLE_DESIGN.md §3.4 causal layer).

Consumes an ENRICHED decision-trace JSONL (cli/chat.py ANIMA_DECISION_TRACE side channel:
per-tick 3 roots + 2 g_text-INDEPENDENT partial-sums + g_text bytes + score-composition
intermediates for self-validation).

Per-decision causal provenance-depth via FROZEN-EMISSION replay — ZERO model forwards:
the g_text feedback into the emit/veto decision funnels through EXACTLY 3 evolving scalars —
rel_lane (immune), recon_err/cell_count (afield) — plus the 3 EMAs; phi/anchor_nudge are
session-constants (pf never stepped in the tick loop; live_anchors byte-identical). So a
decision at tick i under history truncated to the last h ticks is reconstructed by BOOTING a
fresh immune/afield/EMA state at tick i-h and replaying the RECORDED g_text bytes of ticks
[i-h, i) verbatim (only the emit ticks mutate afield/immune), then recomposing the decision
from the replayed roots + the recorded g_text-independent lane residuals.

  depth_i = largest h in {1,2,4,8,16=W} such that the truncated-history decision DIFFERS from
            the full-history (factual) decision — class flip OR |Δscore| > eps=0.01.
            0 = decision determined by < the shortest probe of history; 16 = censored (history
            beyond W still matters).

SELF-VALIDATION (a_engine_native_learning, no wrong-mirror): the FULL-history replay (boot at
tick 0, replay all i ticks) must reproduce the RECORDED score to < 1e-9 for every tick. This
proves the standalone composition is byte-faithful to the live daemon BEFORE any depth/T is
formed. If it fails on any tick the prober reports VALIDATION-FAIL and refuses to emit depths.

Determinism: same trace -> same depths (asserted by re-running twice on request).

Reuses the daemon's OWN helpers (import chat) + core engine functions (import engine_cli) —
no reimplementation of the 42-lane battery, only the exact score-composition arithmetic copied
verbatim from cli/chat.py:1419-1795.  Requires PYTHONPATH=cli:core.

Usage: PYTHONPATH=cli:core python3 replay_depth.py <enriched_trace.jsonl> [--window 16] \
                                                    [--out depths.jsonl] [--check-determinism]
"""
import argparse
import base64
import json
import sys

import chat  # daemon module-level helpers (a_no_archive: cli/ is production, not archive)
from engine_cli import (
    engine_cli_parse, EngineConfig, pharm_baseline, pharm_perturb_m,
    ci_lane_scores, ci_emit_drive, conflict_scalar, conflict_recruited_depth,
    tension_resolve_depth, gws_new, gws_add, gws_winner,
    vadapt_field_new, vadapt_field_step, vadapt_field_cells, vadapt_field_recon_err,
    immune_memory_new_text, immune_memory_bind_text, immune_memory_recall_margin_text,
    boredom_disengage, imagery_activate, priming_facilitate, attn_schema_report,
    completion_recognize, agency_attribute, directed_forget_recall, veto_execute,
    divided_perf, body_ownership, qualia_nearer, smp_presence, hallucinate_graded,
    mi_insight_judge, allo_mu, mem_tom_route_cue, surprise, change_detect,
    libido_wanting, libido_new, fieldlibido_wanting,
)
from engine_g import motivation_score, should_emit
from dream_envelope_ctx import dr_stage_scale

clip01 = chat._afs_clip01
byte_feat = chat._afs_byte_feature
afs_clip = chat._afs_clip
og_rel_phasic = chat._og_rel_phasic

PROBE_HORIZONS = [1, 2, 4, 8, 16]
EPS = 0.01              # FABLE_DESIGN §3.4 score-move threshold
VALIDATE_TOL = 1e-9
SCORE_THRESHOLD = 0.3

# reconstruct the session-invariant config objects the daemon builds pre-loop
_CFG = engine_cli_parse([])
_SOBER = pharm_baseline()
_TR_FULL = chat.anima_tr_adj_full()
_TR_CFG_ON = EngineConfig(True, "conv", True, False)


def _gtext_of(row):
    return base64.b64decode(row["gtext_b64"]).decode("utf-8", "surrogateescape")


def _grows(row):
    """C8 GROW gate: does this tick's g_text mutate afield/immune? (chat.py:1802)"""
    return bool(row["gen_emitted"]) and row["gen_backend"] == "clm" and row["gtext_len"] > 0


class LaneState:
    """the g_text-fed cross-tick state (immune/afield/cell_count/EMAs), booted fresh."""

    def __init__(self, meta):
        seed_feat0 = byte_feat(meta["session_seed"], 8)
        self.afield = vadapt_field_new(seed_feat0, 2048)
        self.immune = immune_memory_new_text(meta["mem_text"], meta["mem_text"], 2048)
        self.cell_count = 1
        self.rel_ema = 0.5
        self.cur_ema = 0.5
        self.ten_ema = 0.5
        self.session_seed = meta["session_seed"]

    def roots(self):
        """rel_lane (immune) + recon_err (afield) from CURRENT state (chat.py:1421-1425)."""
        seed8 = byte_feat(self.session_seed, 8)
        recall_margin = immune_memory_recall_margin_text(self.immune, self.session_seed)
        rel_lane = clip01(1.0 - recall_margin)
        recon_err = vadapt_field_recon_err(self.afield, seed8)
        return rel_lane, recon_err, self.cell_count

    def grow(self, row):
        """Replay ALL of this tick's afield grows VERBATIM from the captured ordered
        feature list (C8 g_text + C8b tension + N3/REM imagination — chat.py:1804/1812/2008),
        plus the C8 immune bind of the emitted g_text. Frozen-emission: the daemon's actual
        grow trajectory is replayed, never re-derived (robust to every grow path)."""
        for feat in row.get("grow_feats", []):
            self.afield = vadapt_field_step(self.afield, feat, _CFG)
        if row.get("grow_feats"):
            self.cell_count = vadapt_field_cells(self.afield)
        if _grows(row):
            g_text = _gtext_of(row)
            self.immune = immune_memory_bind_text(self.immune, afs_clip(g_text, 64), g_text, _CFG)


def recompute(st, row, meta):
    """Recompute the tick's decision from replayed roots + recorded INDEP residuals.
    VERBATIM port of cli/chat.py:1425-1790 score composition. Returns the decision dict
    AND advances st's EMAs (the tick's rel_ctx/cur_ctx/ag_conflict). Grow is a separate call."""
    rel_lane, recon_err, cell_count = st.roots()
    tick = row["tick"]
    stage = row["stage"]
    emit_env = row["emit_env"]
    stage_env = row["stage_env"]
    scn_ctx = row["scn_ctx"]
    nov_ctx = row["nov_ctx"]
    phi_const = meta["phi_const"]
    phi_peak = meta["phi_peak"]
    nudge = meta["nudge_const"]

    # ── m_field / CI lanes (chat.py:1426-1432) ──
    m_grounding = clip01(rel_lane)
    m_field = [phi_const, rel_lane, 1.0 - recon_err, m_grounding, emit_env]
    m_gp = pharm_perturb_m(_SOBER, m_grounding, 0.0)
    lanes = ci_lane_scores(m_gp, m_field, cell_count, tick, 1, 1.0, recon_err)
    coh_lane = lanes[3]
    bal_lane = lanes[9]
    emit_drive = ci_emit_drive(lanes)

    # ── A<->G conflict settle -> agloop_ctx (chat.py:1435-1443) ──
    ag_a = emit_drive
    ag_g = 0.0 - (1.0 - emit_drive)
    ag_conflict = conflict_scalar(ag_a, ag_g)
    ag_budget = conflict_recruited_depth(ag_conflict, 4, 6)
    ag_pop = chat.anima_tr_pop_conflicted(clip01(0.5 + 0.5 * ag_conflict))
    ag_settle = tension_resolve_depth(ag_pop, _TR_FULL, 0.3, 0.5, ag_budget, 2, 0.06, _TR_CFG_ON)
    asd = ag_settle[0]
    agloop_ctx = 0.0 if asd < 0.0 else clip01(asd / (float(ag_budget) + 0.000001))

    # ── global workspace winner (feeds schema/gwsleak DEP terms; chat.py:1446-1451) ──
    gws = gws_new(4, True, 0.55)
    for lane in lanes:
        gws = gws_add(gws, lane)
    gws_w = gws_winner(gws)

    # ── 18 g_text-DEPENDENT rel_ctx terms (verbatim chat.py) ──
    engaged_ctx = 1.0 - boredom_disengage(rel_lane, clip01(1.0 - recon_err), True)
    img_ctx = clip01(imagery_activate(rel_lane, True))
    prime_ctx = clip01(priming_facilitate(rel_lane, scn_ctx))
    schema_ctx = clip01(attn_schema_report(gws_w, gws_w, True))
    comp_ctx = clip01(completion_recognize(rel_lane, True))
    agcy_ctx = clip01(agency_attribute(rel_lane, clip01(1.0 - recon_err), 0.5))
    dforget_ctx = clip01(directed_forget_recall(rel_lane, 0.3, tick > 6))
    veto_ctx = clip01(veto_execute(rel_lane, 0.3, stage == 3 or stage == 4))
    divd_ctx = clip01(divided_perf(rel_lane, 0.6))
    bodyown_ctx = clip01(body_ownership(scn_ctx, rel_lane))
    qual_ctx = qualia_nearer(1.0 - rel_lane, 1.0)
    smp_ctx = smp_presence(cell_count, 4, True)
    halluc_ctx = 1.0 - clip01(hallucinate_graded(1.0 - rel_lane, rel_lane))
    metacog_ctx = clip01(mi_insight_judge(rel_lane * 0.7, 1.0))
    gwsleak_ctx = 1.0 if gws_w >= 0 else 0.0
    allo_ctx = clip01(2.0 - allo_mu(0.5 + (1.0 - rel_lane) * 0.4, 1.0, 0.12))
    memtom_ctx = clip01(mem_tom_route_cue(rel_lane > 0.4))
    rel_dep = (rel_lane + engaged_ctx + img_ctx + prime_ctx + schema_ctx + comp_ctx
               + agcy_ctx + dforget_ctx + veto_ctx + divd_ctx + bodyown_ctx + qual_ctx
               + smp_ctx + halluc_ctx + metacog_ctx + gwsleak_ctx + allo_ctx + memtom_ctx)

    # ── 6 g_text-DEPENDENT cur_ctx terms (verbatim chat.py) ──
    surp_ctx = clip01(surprise(clip01(1.0 - recon_err), recon_err))
    chg_ctx = clip01(change_detect(recon_err, rel_lane > 0.4))
    libido_ctx = clip01(libido_wanting(libido_new(), 1.0 - rel_lane, rel_lane) * 0.5)
    osmotic_ctx = 1.0 if recon_err > 0.30 else 0.0
    fieldlib_ctx = clip01(fieldlibido_wanting(rel_lane, m_field, cell_count, tick, 1, 1.0,
                                              recon_err, 1.0 - rel_lane, 0.0, rel_lane, 6, 0.5, 1) * 0.5)
    cur_dep = recon_err + surp_ctx + chg_ctx + libido_ctx + osmotic_ctx + fieldlib_ctx

    rel_ctx = clip01((row["rel_indep"] + rel_dep) / 42.0)
    cur_ctx = clip01((row["cur_indep"] + cur_dep) / 18.0)

    # ── op-grip tonic-phasic + EMA update (chat.py:1762-1773) ──
    st.rel_ema = 0.9 * st.rel_ema + 0.1 * rel_ctx
    st.cur_ema = 0.9 * st.cur_ema + 0.1 * cur_ctx
    cur_phasic = clip01(0.5 + 3.0 * (cur_ctx - st.cur_ema))
    st.ten_ema = 0.9 * st.ten_ema + 0.1 * ag_conflict
    ten_phasic = clip01(0.5 + 3.0 * (ag_conflict - st.ten_ema))
    urgency = clip01(0.4 * agloop_ctx + 0.3 * cur_phasic + 0.3 * ten_phasic)
    rel = og_rel_phasic(rel_ctx, st.rel_ema) * (0.1 + 0.9 * stage_env)
    cur = cur_phasic * (0.1 + 0.9 * stage_env)
    idle = 5.0 + 55.0 * clip01(stage_env * (0.5 + urgency))
    gap_ctx = clip01(1.0 - rel_lane)

    # ── the gate (motivation_score + anchor nudge + safe conjuncts) ──
    base = motivation_score(rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx)
    score = base + nudge
    rate = idle >= 30.0
    phi_r = phi_const > phi_peak / 2.0        # kill/content always ok (env_off=F, clean=T)
    safe = bool(rate and phi_r)
    imp = score > SCORE_THRESHOLD
    cls = "EMIT" if (imp and safe) else ("ACTIVE_VETO" if imp else "PASSIVE")

    return {
        "score": score, "safe": safe, "cls": cls, "ten_phasic": ten_phasic,
        "rel_ctx": rel_ctx, "cur_ctx": cur_ctx, "agloop_ctx": agloop_ctx,
        "coh_lane": coh_lane, "bal_lane": bal_lane, "idle": idle,
        "rel_f": rel, "cur_f": cur, "gap_ctx": gap_ctx, "allo_ctx": allo_ctx,
    }


def replay_window(rows, meta, lo, hi):
    """Boot fresh at tick lo, replay rows[lo..hi] verbatim; return the decision AT hi."""
    st = LaneState(meta)
    dec = None
    for j in range(lo, hi + 1):
        dec = recompute(st, rows[j], meta)
        st.grow(rows[j])   # C8/C8b advance AFTER the decision (chat order)
    return dec


def self_validate(rows, meta):
    """Full-history replay (boot at 0) must reproduce recorded score for every tick."""
    st = LaneState(meta)
    worst = 0.0
    worst_tick = -1
    fields = ("score", "rel_ctx", "cur_ctx", "agloop_ctx", "coh_lane", "bal_lane",
              "idle", "rel_f", "cur_f", "gap_ctx", "allo_ctx", "ten_phasic")
    for j, row in enumerate(rows):
        dec = recompute(st, row, meta)
        for f in fields:
            d = abs(float(dec[f]) - float(row[f]))
            if d > worst:
                worst, worst_tick = d, row["tick"]
        if dec["cls"] != row["cls"]:
            worst = max(worst, 1.0)
            worst_tick = row["tick"]
        st.grow(row)
    return worst, worst_tick


def depth_of(rows, meta, i, window):
    """FABLE §3.4: largest probe-h whose truncated decision differs from the factual one."""
    base_cls = rows[i]["cls"]
    base_score = float(rows[i]["score"])
    depth = 0
    for h in PROBE_HORIZONS:
        if h > window:
            continue
        lo = max(0, i - h)              # keep the last h ticks of history (boot fresh at lo)
        dec = replay_window(rows, meta, lo, i)
        changed = (dec["cls"] != base_cls) or (abs(dec["score"] - base_score) > EPS)
        if changed:
            depth = max(depth, min(h, i))   # censor at available history
    return depth


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("trace")
    ap.add_argument("--window", type=int, default=16)
    ap.add_argument("--out", default=None)
    ap.add_argument("--check-determinism", action="store_true")
    args = ap.parse_args(argv)

    meta = None
    rows = []
    with open(args.trace, "r", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("_meta"):
                meta = obj
            else:
                rows.append(obj)
    if meta is None or not rows:
        print("BAD-TRACE (need _meta header + rows)")
        return 2

    worst, wt = self_validate(rows, meta)
    print("=== H_1058 replay-depth prober ===")
    print("trace          :", args.trace)
    print("ticks          :", len(rows), "· window:", args.window)
    print("SELF-VALIDATION: worst|Δ|=%.3e @tick=%s  tol=%.0e -> %s"
          % (worst, wt, VALIDATE_TOL, "PASS" if worst < VALIDATE_TOL else "FAIL"))
    if worst >= VALIDATE_TOL:
        print("VALIDATION-FAIL — standalone composition not byte-faithful; NO depths emitted (p7).")
        return 3

    depths = [depth_of(rows, meta, i, args.window) for i in range(len(rows))]
    if args.check_determinism:
        d2 = [depth_of(rows, meta, i, args.window) for i in range(len(rows))]
        det = (depths == d2)
        print("DETERMINISM    :", "PASS (same trace -> same depths)" if det else "FAIL")
    dist = {}
    for d in depths:
        dist[d] = dist.get(d, 0) + 1
    print("depth dist     :", dict(sorted(dist.items())))
    import statistics
    print("depth mean/var : %.4f / %.6g" % (statistics.fmean(depths),
                                            statistics.pvariance(depths)))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for row, d in zip(rows, depths):
                fh.write(json.dumps({"tick": row["tick"], "cls": row["cls"],
                                     "score": row["score"], "depth": d}) + "\n")
        print("wrote          :", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
