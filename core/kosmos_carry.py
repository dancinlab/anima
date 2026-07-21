#!/usr/bin/env python3
# ==========================================================================
# core/kosmos_carry.py — .kosmos anchor-store CARRY certifier (H_9843).
#
# WHY THIS EXISTS. H_9838 builds a CA3 heteroassociative store during ONE
# training run. If the .kosmos anchor store does not survive BETWEEN runs, that
# store is confined to a single run and can never ACCUMULATE. This module is the
# supply line: it certifies that a `.kosmos` store can be carried from run N into
# run N+1 without the carried bytes changing, and that what the carried store
# hands downstream is content-ADDRESSABLE rather than merely voluminous.
#
# ⚠ SCOPE — this is a DATA supply line, NOT an identity claim. The `a_kosmos`
# identity framing ("carry the self across runs") is DEAD: H_9789 measured the
# self-anchor as VOID. Nothing here reads on identity, continuity, or selfhood.
#
# ⚠ SEQUENCING — this fires only AFTER H_9838 is positive. There is no consumer
# of a carried store in the training loop today, so a certified carry is an
# ADMISSIBILITY statement about the format, never a capability result.
#
# It imports the REAL production writer/reader (core/kosmos_io.py) and the REAL
# disjoint store lane (core/hippo_lane.py) — nothing is re-implemented here, so a
# defect in the format is a defect this module MUST see (a_experiment_engine_native).
#
# $0: pure numpy + the two core modules. No torch, no GPU, no checkpoint.
# ==========================================================================
import hashlib
import os

import numpy as np

import kosmos_io as KIO                              # core/kosmos_io.py (core/ on sys.path)
import hippo_lane as HL                              # core/hippo_lane.py — the DISJOINT lane

# Exit codes (mirror core/pregates.py's PASS/REFUSE convention used by the H_9808 gate).
PASS = 0
REFUSE = 4

# ── PRE-REGISTERED battery geometry + bars ─────────────────────────────────
# Frozen here, not on the command line, so no knob on the CLI can move a verdict
# (no-tune-to-green). The battery is run at EVERY geometry and must certify at ALL
# of them; the carried-store headline is the MINIMUM across geometries. A readout
# that lives at one (dim, seed) is an artefact of the readout, exactly the defect
# H_9844 caught in mi-screen when over_floor flipped sign with the block size.
GEOMETRIES = ((256, 7), (256, 11), (512, 7), (512, 11))   # (code dim, projection seed)
N_CONTROL = 12                    # anchors per control arm (chance = 1/12 = 0.0833)
EMBED_DIM = 64                    # tension→key embedding width (kosmos_io fn)
ACTIVE_FRAC = 16                  # kWTA active bits = dim // ACTIVE_FRAC
# MEASURED, and the reason dg_decorrelate is not optional here: raw `.kosmos` key/value
# vectors are near-COLLINEAR (planted-control key cosines 0.28–0.98, value cosines
# 0.81–0.90) because a tension key lives in the 5-row span of one fixed projection and a
# text sketch is dominated by the shared prefix of an anchor family. Without the lane's own
# rung-2 whitening the positive control reads 0.0833 = chance — i.e. INSTRUMENT-DEAD, which
# is exactly what the first end-to-end run of this flag reported before this line existed.
DECORRELATE = "center_zscore"     # core/hippo_lane.py::dg_decorrelate rung-2 lens
PLANT_BAR = 0.90                  # positive control MUST reach this accuracy
PEDESTAL_SLACK = 0.10             # a zero-truth arm MUST stay <= chance + this
MIN_ANCHORS = 4                   # below this the readout is underpowered, full stop


# ── deterministic text → dense feature (the VALUE side of the pair) ────────
# Hashed byte-trigram sketch. Deterministic across processes and platforms (no
# Python hash randomization, no RNG), so a store certified in run N certifies
# identically in run N+1 — which is the whole point of a carry.
def text_features(text, dim=EMBED_DIM, seed=0):
    v = np.zeros(dim, dtype=np.float64)
    b = text.encode("utf-8", "surrogateescape")
    if not b:
        return v
    for i in range(len(b)):
        h = b[i] * 2654435761 + seed
        if i + 1 < len(b):
            h = (h * 65599 + b[i + 1]) & 0xFFFFFFFF
        if i + 2 < len(b):
            h = (h * 65599 + b[i + 2]) & 0xFFFFFFFF
        h &= 0xFFFFFFFF
        v[h % dim] += 1.0
        v[(h >> 13) % dim] -= 1.0
    n = float(np.linalg.norm(v))
    return v / n if n > 0 else v


# ── anchor store → (key, value) vector pairs ───────────────────────────────
# key   = the anchor's tension 5-channel fingerprint, lifted by the REAL
#         kosmos_io.tension_5ch_to_embedding (LCG + Box-Muller, carve-out K1).
# value = the anchor's payload text.
# An anchor with no tension payload has no address and is DROPPED (reported).
def store_pairs(anchors, embed_dim=EMBED_DIM):
    keys, vals, names, dropped = [], [], [], []
    for a in anchors:
        t = a.get("tension_5ch")
        if t is None:
            dropped.append(a.get("name", "?"))
            continue
        keys.append(KIO.tension_5ch_to_embedding(t, embed_dim, 9843))
        vals.append(text_features(a.get("text_payload", ""), embed_dim, 0))
        names.append(a.get("name", "?"))
    return (np.asarray(keys, dtype=np.float64), np.asarray(vals, dtype=np.float64),
            names, dropped)


# ── the readout: content-addressed retrieval through the REAL CA3 lane ─────
# W is built from the pairing the store RECORDS; scoring is always against the
# TRUE partner. That asymmetry is what separates accumulated INFORMATION from
# accumulated VOLUME: permute the recorded pairing and the store is exactly as
# large, exactly as dense, and retrieves nothing.
def bind_readout(keys, vals, pairing, dim, seed):
    n = len(keys)
    if n == 0:
        return {"n": 0, "acc": 0.0, "chance": 0.0}
    active = max(2, dim // ACTIVE_FRAC)
    # Whiten BEFORE pattern separation with the lane's own rung-2 lens, identically on every
    # arm (plant, both pedestals, treatment) — a lens applied to one arm only would be the
    # instrument choosing its answer.
    kc = HL.dg_codes(HL.dg_decorrelate(keys, DECORRELATE), dim, active, seed)
    vc = HL.dg_codes(HL.dg_decorrelate(vals, DECORRELATE), dim, active, seed + 1000)
    codes = np.vstack([kc, vc])
    edges = [(i, n + int(pairing[i])) for i in range(n)]
    W = HL.hippo_build_store(codes, edges, dim)
    hit = 0
    for i in range(n):
        scores = [HL.hippo_relatedness(W, codes, i, n + j, 1, active) for j in range(n)]
        if int(np.argmax(scores)) == i:              # i = the TRUE partner of key i
            hit += 1
    return {"n": n, "acc": hit / float(n), "chance": 1.0 / float(n)}


# ── shipped control battery (runs FIRST; the carried row is refused without it) ──
def _synthetic_pairs(n, embed_dim, degenerate=False):
    keys, vals = [], []
    for i in range(n):
        if degenerate:
            # ZERO-TRUTH PEDESTAL: every anchor carries the SAME tension, i.e. the
            # store has volume but no addresses. Nothing is retrievable even from
            # the true pairing; an instrument that fires here MANUFACTURES signal.
            t = [0.25, 0.25, 0.25, 0.25, 0.25]
            txt = "structure-free payload"
        else:
            # Well-separated addresses AND payloads: a positive control's job is to carry a
            # signal that is unambiguously THERE. Derived from sha256 (deterministic, no RNG,
            # reproducible in any process) so the control is a fixture, not a draw.
            hh = hashlib.sha256(("plant %d" % i).encode()).hexdigest()
            t = [int(hh[c * 2:c * 2 + 2], 16) / 255.0 for c in range(5)]
            txt = "planted anchor %03d :: %s" % (i, hh[10:42])
        keys.append(KIO.tension_5ch_to_embedding(t, embed_dim, 9843))
        vals.append(text_features(txt, embed_dim, 0))
    return np.asarray(keys), np.asarray(vals)


def battery_liveness(n=N_CONTROL, embed_dim=EMBED_DIM):
    """Controls FIRST, frozen order, at EVERY geometry:
       ① plant_bound      — distinct addresses + the true pairing: MUST fire (>= PLANT_BAR).
       ② pedestal_flat    — structure-free store (one address for all): MUST refuse.
       ③ pedestal_shuffle — same count, same distribution, pairing PERMUTED, scored
                            against the truth: MUST refuse (volume is not information).
    """
    kb, vb = _synthetic_pairs(n, embed_dim)
    kd, vd = _synthetic_pairs(n, embed_dim, degenerate=True)
    ident = list(range(n))
    # fixed derangement (i -> i+1 mod n); no RNG, so the control is reproducible.
    perm = [(i + 1) % n for i in range(n)]
    per_geom, fires, flat_ref, shuf_ref = [], [], [], []
    for (dim, seed) in GEOMETRIES:
        b = bind_readout(kb, vb, ident, dim, seed)
        d = bind_readout(kd, vd, ident, dim, seed)
        s = bind_readout(kb, vb, perm, dim, seed)
        cap = b["chance"] + PEDESTAL_SLACK
        fires.append(b["acc"] >= PLANT_BAR)
        flat_ref.append(d["acc"] <= cap)
        shuf_ref.append(s["acc"] <= cap)
        per_geom.append({"dim": dim, "seed": seed, "chance": b["chance"],
                         "plant_bound": b["acc"], "pedestal_flat": d["acc"],
                         "pedestal_shuffle": s["acc"], "refuse_cap": cap})
    out = {
        "n": n, "geometries": len(GEOMETRIES), "per_geometry": per_geom,
        "plant_fires": bool(all(fires)),
        "pedestal_flat_refuses": bool(all(flat_ref)),
        "pedestal_shuffle_refuses": bool(all(shuf_ref)),
        "bars": {"plant_bar": PLANT_BAR, "pedestal_slack": PEDESTAL_SLACK},
    }
    out["certified"] = bool(out["plant_fires"] and out["pedestal_flat_refuses"]
                            and out["pedestal_shuffle_refuses"])
    return out


# ── format fidelity: is the READER the inverse of the WRITER? ──────────────
_MASK_PREFIXES = ("  emitted_at",)                   # wall-clock, masked by kosmos_io's own doc
_TITLE_PREFIX = "@anchor "


def _mask(body, mask_title):
    keep = []
    for ln in body.split("\n"):
        if ln.startswith(_MASK_PREFIXES):
            keep.append("  emitted_at    = <MASKED>")
            continue
        if mask_title and ln.startswith(_TITLE_PREFIX):
            keep.append("@anchor <MASKED>")
            continue
        keep.append(ln)
    return "\n".join(keep)


# MEASURED on the real 31-anchor store HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31: a
# hand-written .kosmos may carry a trailing `# comment` on a field line, and
# kosmos_io._ki_field_match does NOT strip it — `radius = 0.10   # α+β hybrid …` comes
# back as that whole STRING. The first end-to-end run of this flag on that store died with
# `ValueError: could not convert string to float`. A certifier must REPORT an unparseable
# field, never crash on it (and never "fix" it by guessing a number).
def _num(v, cast, default=0.0):
    try:
        return cast(v), True
    except (TypeError, ValueError):
        return default, False


def reemit_report(anchors, scratch_dir):
    """Re-emit every loaded anchor through the REAL create_anchor using ONLY what
    load_anchors returned, and diff the bytes against the file on disk.

    Two levels are reported and they are NOT the same question:
      strict_identical  — only the wall-clock `emitted_at` line is masked.
      payload_identical — `emitted_at` AND the `@anchor` header line are masked,
                          i.e. everything a downstream store actually consumes
                          (placement fields + payload text + tension).
    """
    rows, strict, payload, malformed = [], 0, 0, []
    for a in anchors:
        f = a.get("fields", {})
        coord = f.get("coord", [0.0, 0.0])
        bad = []
        # A coord that did not parse as a 2-list is REPORTED, never silently defaulted to
        # (0,0) — a substituted number is an invented measurement. MEASURED on e7_31:
        # `coord = [0.50, 0.50]   # α path …` fails kosmos_io's list-literal test (the
        # trailing comment breaks the closing `]`) and comes back as a raw string.
        if not (isinstance(coord, list) and len(coord) == 2):
            bad.append("coord")
            coord = [0.0, 0.0]
        cx, ok = _num(coord[0], float)
        if not ok:
            bad.append("coord[0]")
        cy, ok = _num(coord[1], float)
        if not ok:
            bad.append("coord[1]")
        rad, ok = _num(f.get("radius", 0.0), float)
        if not ok:
            bad.append("radius")
        tier, ok = _num(f.get("knuth_tier", 0), int, 0)
        if not ok:
            bad.append("knuth_tier")
        t = a.get("tension_5ch") or [0.0] * 5
        p = KIO.create_anchor(
            scratch_dir, a["name"], str(f.get("title", "")), cx, cy,
            str(f.get("lane", "")), rad, tier, str(f.get("category", "")),
            str(f.get("top_emotion", "")), a.get("text_payload", ""), t,
            str(f.get("closed_anchor", "")), str(f.get("cross_link", "")))
        orig = open(a["path"], "r", encoding="utf-8", errors="surrogateescape").read()
        re_ = open(p, "r", encoding="utf-8", errors="surrogateescape").read()
        s_ok = _mask(orig, False) == _mask(re_, False)
        p_ok = _mask(orig, True) == _mask(re_, True)
        strict += 1 if s_ok else 0
        payload += 1 if p_ok else 0
        if bad:
            malformed.append({"name": a["name"], "unparseable_fields": bad})
        rows.append({"name": a["name"], "strict_identical": bool(s_ok),
                     "payload_identical": bool(p_ok),
                     "orig_bytes": len(orig.encode("utf-8", "surrogateescape")),
                     "reemit_bytes": len(re_.encode("utf-8", "surrogateescape"))})
    n = len(anchors)
    return {
        "n": n, "strict_identical": strict, "payload_identical": payload,
        # MEASURED loss channels of the read→write path (this is NOT a bug report against
        # kosmos_io — it is the reason a carry must COPY FILES and never re-emit):
        #   title  — load_anchors skips every line starting with '@', and the title lives
        #            only on the `@anchor <name> := "<title>"` header, so the reader cannot
        #            return it. strict≠payload ⟹ the diff is exactly that line.
        #   escape — _ki_text_payload returns the payload STILL ESCAPED and there is no
        #            inverse of _escape_kosmos_string, so re-emitting a payload that
        #            contains " or \ or a newline escapes it a SECOND time.
        "reader_is_writer_inverse": bool(n > 0 and strict == n),
        "payload_reader_inverse": bool(n > 0 and payload == n),
        "n_title_only_diff": sum(1 for r in rows if not r["strict_identical"]
                                 and r["payload_identical"]),
        "n_payload_diff": sum(1 for r in rows if not r["payload_identical"]),
        "n_malformed": len(malformed),
        "malformed": malformed[:20],
        "per_anchor": rows,
    }


def store_key(store_dir):
    """Short stable key for a store path — names the re-emit scratch dir so repeated
    runs reuse ONE directory instead of stranding a new one each time."""
    return hashlib.sha256(os.path.abspath(store_dir).encode("utf-8")).hexdigest()[:12]


def sha_manifest(store_dir):
    """sha256 per .kosmos file — the file-level carry integrity ledger."""
    out = {}
    if not os.path.isdir(store_dir):
        return out
    for name in sorted(os.listdir(store_dir)):
        if not name.endswith(".kosmos"):
            continue
        fp = os.path.join(store_dir, name)
        if os.path.isfile(fp):
            out[name] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return out


# ── the provenance write (append mode) ─────────────────────────────────────
def append_run_anchor(store_dir, fingerprint):
    """Append ONE run-provenance anchor so the store ACCUMULATES one record per
    run. It writes a NEW file and never rewrites an existing one — which is the
    only carry discipline the format supports (see reemit_report: the reader is
    not the writer's inverse, so a read→rewrite carry would corrupt payloads)."""
    h = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
    t = [((int(h[i * 4:i * 4 + 4], 16)) % 1000) / 1000.0 for i in range(5)]
    name = "carry_run_" + h[:12]
    path = KIO.create_anchor(store_dir, name, "carry provenance " + h[:12],
                             0.0, 0.0, "carry", 0.0, 0, "carry_provenance",
                             "none", fingerprint, t, "H_9843-carry", "")
    return {"name": name, "path": path, "fingerprint_sha256": h}


# ── the preflight the CLI flag runs ────────────────────────────────────────
def carry_preflight(store_dir, mode, fingerprint, scratch_dir):
    """Returns the full JSON-able report. Order is FROZEN and load-bearing:
       ① controls  ② load + format fidelity  ③ carried-store readout + its own
       shuffle control  ④ the append write (never before the measurement)."""
    battery = battery_liveness()
    rep = {
        "instrument": "kosmos-carry",
        "hypothesis": "H_9843",
        "engine": "core/kosmos_io.py (writer/reader) + core/hippo_lane.py (CA3 readout)",
        "store": store_dir, "mode": mode,
        "battery": battery,
    }
    if not battery["certified"]:
        rep["status"] = ("INSTRUMENT-DEAD" if not battery["plant_fires"] else "INVALID")
        rep["why"] = ("plant_bound did NOT fire — the readout cannot retrieve a pairing that "
                      "IS there, so any null on a carried store would be a property of the "
                      "readout." if not battery["plant_fires"] else
                      "a zero-truth pedestal did NOT refuse — the readout reports retrieval on "
                      "a store with no addresses, or on a pairing permuted away from the truth.")
        return rep

    if not os.path.isdir(store_dir):
        rep["status"] = "NO-STORE"
        rep["why"] = "--kosmos-carry %r is not a directory. A .kosmos store is a DIRECTORY of " \
                     "anchors (core/kosmos_io.load_anchors takes dir_path), not one file." % store_dir
        return rep

    before = sha_manifest(store_dir)
    anchors = KIO.load_anchors(store_dir)
    keys, vals, names, dropped = store_pairs(anchors)
    rep["carried"] = {"n_files": len(before), "n_anchors": len(anchors),
                      "n_addressable": len(names), "dropped_no_tension": dropped}
    rep["fidelity"] = reemit_report(anchors, scratch_dir)
    rep["fidelity"]["reemit_scratch"] = scratch_dir      # the byte-diff stays inspectable

    n = len(names)
    underpowered = n < MIN_ANCHORS
    if underpowered:
        # An empty store IS the no-carry-over baseline arm — a row, not a crash. It is still
        # not certifiable (chance = 1/n is undefined / trivially met), so the run refuses.
        rep["readout"] = {
            "per_geometry": [], "addressable": False,
            "why": "the store carries %d addressable anchor(s); the readout needs >= %d "
                   "(chance = 1/n). n=0 is the NO-CARRY baseline." % (n, MIN_ANCHORS),
        }
    else:
        ident = list(range(n))
        perm = [(i + 1) % n for i in range(n)]
        per_geom = []
        for (dim, seed) in GEOMETRIES:
            t_row = bind_readout(keys, vals, ident, dim, seed)
            s_row = bind_readout(keys, vals, perm, dim, seed)
            per_geom.append({"dim": dim, "seed": seed, "acc": t_row["acc"],
                             "acc_shuffled": s_row["acc"], "chance": t_row["chance"]})
        acc_min = min(g["acc"] for g in per_geom)
        shuf_max = max(g["acc_shuffled"] for g in per_geom)
        rep["readout"] = {
            "per_geometry": per_geom,
            "acc_min_over_geometries": acc_min,
            "acc_shuffled_max_over_geometries": shuf_max,
            "chance": 1.0 / float(n),
            "separation": acc_min - shuf_max,
            "addressable": bool(acc_min >= PLANT_BAR
                                and shuf_max <= 1.0 / float(n) + PEDESTAL_SLACK),
        }

    # ④ the write comes LAST — never before the store has been measured as it arrived.
    if mode == "append":
        rep["appended"] = append_run_anchor(store_dir, fingerprint)
        after = sha_manifest(store_dir)
        rep["append_integrity"] = {
            "n_before": len(before), "n_after": len(after),
            "pre_existing_untouched": bool(all(after.get(k) == v for k, v in before.items())),
            "added": sorted(set(after) - set(before)),
        }
        ok = rep["append_integrity"]["pre_existing_untouched"] and len(after) == len(before) + 1
    else:
        after = sha_manifest(store_dir)
        rep["append_integrity"] = {"n_before": len(before), "n_after": len(after),
                                   "pre_existing_untouched": bool(after == before),
                                   "added": []}
        ok = bool(after == before)

    if not ok:
        rep["status"] = "CARRY-CORRUPT"
        rep["why"] = "the carried files did not survive the carry byte-for-byte."
        return rep
    if underpowered:
        rep["status"] = "NO-CARRY" if len(anchors) == 0 else "UNDERPOWERED"
        rep["why"] = rep["readout"]["why"]
        return rep
    if not rep["readout"]["addressable"]:
        rep["status"] = "NOT-ADDRESSABLE"
        rep["why"] = ("controls certified and the carried files are byte-stable, but the carried "
                      "store's own pairing is NOT retrievable at every geometry (colliding "
                      "addresses) — this store carries volume the readout cannot index.")
        return rep
    # The carry is file-level, so a lossy read→write path does not corrupt it — but it MUST be
    # said out loud, because it bounds every downstream use: a consumer that regenerates a
    # store from what load_anchors returns will silently lose the title and double-escape the
    # payload. Never fold that into a bare "CERTIFIED" (a_no_llm_frame_trap / honesty).
    if rep["fidelity"]["payload_reader_inverse"] and rep["fidelity"]["reader_is_writer_inverse"]:
        rep["status"] = "CERTIFIED"
        rep["why"] = ("controls certified; carried files byte-stable; the store's own pairing is "
                      "retrievable at every geometry and collapses under the shuffle; and the "
                      "reader round-trips the writer byte-for-byte on this store.")
    else:
        rep["status"] = "CERTIFIED-COPY-ONLY"
        rep["why"] = ("controls certified; carried files byte-stable; the store's own pairing is "
                      "retrievable at every geometry and collapses under the shuffle. BUT the "
                      "reader is NOT the writer's inverse on this store (%d/%d anchors differ on "
                      "the title line only, %d differ in the payload itself), so this store may "
                      "be carried ONLY by copying/adding FILES — a read→rewrite carry would "
                      "corrupt it." % (rep["fidelity"]["n_title_only_diff"], rep["fidelity"]["n"],
                                       rep["fidelity"]["n_payload_diff"]))
    return rep
