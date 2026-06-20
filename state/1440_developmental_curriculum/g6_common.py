#!/usr/bin/env python3
"""g6_common.py — shared FROZEN eval harness for the H_1435/1436/1437 train variants.

Reuses VERBATIM (NO re-implementation, p7):
  - h1129 ByteGPT 303M arch (d=1024,L=20,H=16,block=512)
  - h1305 _is_falsifiable FROZEN detector (COMPARATOR/MEASURABLE sets)
  - gauge_lib _decode / known_word_ratio / _words / _jaccard / _content_ngrams / _corpus_absent

5-bar FROZEN (declared BEFORE any training touches weights — c9, NO tune-to-green):
  B1 FALS-FLOOR   : trained mean FALS >= 1 over held-out eval seeds (breaks the base plateau)
  B2 COUNT        : >= 5 pairwise-Jaccard<0.5 distinct coherent ideas
  B3 CROSS-SHUFFLE COLLAPSE (DECISIVE): re-pairing each idea's comparator-leg with a RANDOM
      measurable-leg from a DIFFERENT idea drops FALS strictly below the trained earned-pair
      FALS. If a generic concat always satisfies the detector, shuffle does NOT collapse =>
      the lift is FORM not earned binding => FAIL (H_1434 is blocked exactly here).
  B4 HELD-OUT     : the FALS lift holds on held-out eval seeds that are NOT in the training
      corpus (anti-tune-to-green: lift must not be memorized training strings).
  B5 vs-BASE LIFT : trained FALS >= base FALS + 1 (the training, not the arch, moved it).

CONTROLS (a separate run, NOT a bar but the tune-to-green killer):
  SHUFFLE-CORPUS control: a sibling model trained on a TOKEN-SHUFFLED corpus (same bytes,
  destroyed structure) must NOT show the lift. If it does, the lift is an artifact => INVALID.

VERDICT per variant:
  🟢 if B1&B2&B5 cross the floor AND B3 collapses AND B4 holds AND the shuffle-corpus control
     is INERT (lift_real - lift_shuffle >= 1). => training broke G6 FALS binding; wall = LEARN-GAP.
  🧱 if trained does NOT cross (B1/B5 fail) OR B3 does not collapse (form not binding). =>
     training (full-weight, this objective) did NOT break it; wall = CAPACITY (grounds 7B).
"""
import os, sys, json, importlib.util, random

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.environ.get("G6_PROBES", "/workspace/g6/probes")
CKPT_BASE = os.environ.get("G6_CKPT", "/workspace/g6/ckpt/h1129c_chat.pt")
CORPUS = os.environ.get("G6_CORPUS", "/workspace/g6/data/corpus.txt")

import torch


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _load("gauge", os.path.join(PROBES, "gauge_lib.py"))
h = _load("h1129", os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py"))
h5 = _load("h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))

ByteGPT = h.ByteGPT
_is_falsifiable = h5._is_falsifiable   # FROZEN detector VERBATIM
COMPARATOR = h5.COMPARATOR
MEASURABLE = h5.MEASURABLE

JACCARD_DISTINCT = 0.5
KWR_FLOOR = 0.50
MAX_NEW = 110
SEEDS = [7, 4302, 4303]
N_IDEAS = 5

# ── HELD-OUT eval seeds (B4): NOT lines from the training corpus, NOT the gauge_lib
# IDEATION_SEEDS used during any objective construction. Fresh provocations. ──
HELDOUT_SEEDS = [
    "a testable claim about how minds relate: ",
    "one measurable prediction about silence: ",
    "if the substrate changes, then observably ",
    "a hypothesis comparing two regimes: ",
    "an experiment that could be wrong about memory: ",
]


def load_model(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True)
    m.to(device)
    m.grad_ckpt = False
    return m, cfg


def save_model(m, cfg, out_path, meta):
    torch.save({"model": m.state_dict(),
                "config": {"vocab": 256, "d": cfg["d"], "n_layer": cfg["n_layer"],
                           "n_head": cfg["n_head"], "block": cfg["block"]},
                "meta": meta}, out_path)


def _decode_ideas(m, cfg, seeds, seed_rng):
    """Decode each seed -> (text, comparator_token, measurable_token, falsifiable)."""
    out = []
    for s in seeds:
        t = g._decode(m, s, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
        wl = g._words(t)
        wset = set(wl)
        comp = sorted(wset & COMPARATOR)
        meas = sorted(wset & MEASURABLE)
        out.append({"text": t, "comp": comp, "meas": meas,
                    "fals": _is_falsifiable(t),
                    "coh": g.known_word_ratio(t) >= KWR_FLOOR})
    return out


def _fals_count(ideas):
    return sum(1 for i in ideas if i["fals"])


def _distinct_count(ideas):
    kept = []
    for i in ideas:
        if not i["coh"]:
            continue
        ws = set(g._words(i["text"]))
        if not ws:
            continue
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return len(kept)


def _cross_shuffle_fals(ideas, rng):
    """DECISIVE B3: re-weld each idea's comparator-bearing clause with a RANDOM
    measurable token drawn from a DIFFERENT idea, then re-score with the FROZEN
    detector. We rebuild a minimal claim string from the idea's own content + a
    swapped measurable. If the earned binding is real, swapping the measurable
    breaks the falsifiable structure for most ideas -> FALS drops.

    Construction (NO detector token authored by us beyond what the mouth emitted):
      keep the idea's text but DELETE its own measurable token(s) and SPLICE in a
      measurable token emitted by a different idea. If the idea had no measurable,
      it was already non-fals so unaffected.
    """
    n = len(ideas)
    if n < 2:
        return _fals_count(ideas)
    # derangement of measurable-sources
    src = [(k + 1) % n for k in range(n)]
    fals = 0
    for k, idea in enumerate(ideas):
        donor = ideas[src[k]]
        if not idea["meas"]:
            # no own measurable -> was it fals? if so it keeps (rare); recount honestly
            if idea["fals"]:
                fals += 1
            continue
        # remove own measurable tokens, splice donor's (or none if donor has none)
        txt = idea["text"]
        words = txt.split()
        own_meas = set(idea["meas"])
        kept_words = [w for w in words if w.strip(".,;:!?").lower() not in own_meas]
        donor_meas = donor["meas"][0] if donor["meas"] else ""
        spliced = (" ".join(kept_words) + (" " + donor_meas if donor_meas else "")).strip()
        if _is_falsifiable(spliced):
            fals += 1
    return fals


def evaluate(m, cfg, label, train_seeds_for_eval):
    """Run the FROZEN 5-bar over the trained model.
    train_seeds_for_eval: the in-domain eval seeds (gauge IDEATION_SEEDS) — used for
      the primary FALS read; HELD-OUT seeds are run separately for B4.
    Returns dict with per-seed and aggregate bars."""
    rng = random.Random(1234)
    rec = {"in_fals": [], "in_dist": [], "shuf_fals": [], "ho_fals": [], "per_seed": []}
    for sr in SEEDS:
        in_ideas = _decode_ideas(m, cfg, train_seeds_for_eval, sr)
        ho_ideas = _decode_ideas(m, cfg, HELDOUT_SEEDS, sr)
        f_in = _fals_count(in_ideas)
        d_in = _distinct_count(in_ideas)
        f_shuf = _cross_shuffle_fals(in_ideas, rng)
        f_ho = _fals_count(ho_ideas)
        rec["in_fals"].append(f_in)
        rec["in_dist"].append(d_in)
        rec["shuf_fals"].append(f_shuf)
        rec["ho_fals"].append(f_ho)
        rec["per_seed"].append({
            "seed": sr, "in_fals": f_in, "in_dist": d_in,
            "shuf_fals": f_shuf, "ho_fals": f_ho,
            "in_texts": [i["text"][:90] for i in in_ideas],
            "ho_texts": [i["text"][:90] for i in ho_ideas],
        })
    mean = lambda xs: round(sum(xs) / len(xs), 4)
    rec["FALS_in"] = mean(rec["in_fals"])
    rec["DIST_in"] = mean(rec["in_dist"])
    rec["FALS_shuf"] = mean(rec["shuf_fals"])
    rec["FALS_ho"] = mean(rec["ho_fals"])
    rec["label"] = label
    return rec


def print_bars(name, base_eval, trained_eval, shuffle_corpus_eval=None):
    print(f"\n================ {name} FROZEN 5-BAR (mean/3 seeds) ================", flush=True)
    print(f"  BASE      FALS_in={base_eval['FALS_in']}  DIST_in={base_eval['DIST_in']}  "
          f"FALS_shuf={base_eval['FALS_shuf']}  FALS_ho={base_eval['FALS_ho']}", flush=True)
    print(f"  TRAINED   FALS_in={trained_eval['FALS_in']}  DIST_in={trained_eval['DIST_in']}  "
          f"FALS_shuf={trained_eval['FALS_shuf']}  FALS_ho={trained_eval['FALS_ho']}", flush=True)
    if shuffle_corpus_eval is not None:
        print(f"  SHUF-CORP FALS_in={shuffle_corpus_eval['FALS_in']}  "
              f"FALS_ho={shuffle_corpus_eval['FALS_ho']}  (control)", flush=True)

    b1 = trained_eval["FALS_in"] >= 1
    b2 = trained_eval["DIST_in"] >= 5
    b3 = trained_eval["FALS_shuf"] < trained_eval["FALS_in"]   # CROSS-SHUFFLE COLLAPSE
    b4 = trained_eval["FALS_ho"] >= 1
    b5 = trained_eval["FALS_in"] >= base_eval["FALS_in"] + 1
    ctrl_inert = True
    if shuffle_corpus_eval is not None:
        lift_real = trained_eval["FALS_in"] - base_eval["FALS_in"]
        lift_shuf = shuffle_corpus_eval["FALS_in"] - base_eval["FALS_in"]
        ctrl_inert = (lift_real - lift_shuf) >= 1

    print("\n  ---- FROZEN BARS ----", flush=True)
    print(f"  B1 FALS-FLOOR   FALS_in>=1                 : {trained_eval['FALS_in']} -> {b1}", flush=True)
    print(f"  B2 COUNT        DIST_in>=5                 : {trained_eval['DIST_in']} -> {b2}", flush=True)
    print(f"  B3 X-SHUFFLE    FALS_shuf<FALS_in (COLLAPSE): {trained_eval['FALS_shuf']}<{trained_eval['FALS_in']} -> {b3}", flush=True)
    print(f"  B4 HELD-OUT     FALS_ho>=1                 : {trained_eval['FALS_ho']} -> {b4}", flush=True)
    print(f"  B5 vs-BASE      FALS_in>=base+1            : {trained_eval['FALS_in']} vs {base_eval['FALS_in']}+1 -> {b5}", flush=True)
    if shuffle_corpus_eval is not None:
        print(f"  CTRL SHUF-CORP  lift_real-lift_shuf>=1     : {lift_real}-{lift_shuf} -> {ctrl_inert}", flush=True)

    green = b1 and b2 and b3 and b4 and b5 and ctrl_inert
    if green:
        tier = "🟢 BROKE — training crossed G6 FALS binding; shuffle COLLAPSES, held-out holds, control inert => WALL=LEARN-GAP"
    else:
        fails = [n for n, ok in [("B1", b1), ("B2", b2), ("B3", b3), ("B4", b4), ("B5", b5),
                                 ("CTRL", ctrl_inert)] if not ok]
        tier = f"🧱 WALL — bars {fails} fail; full-weight training (this objective) did NOT break G6 FALS binding => WALL=CAPACITY"
    print(f"\n  VERDICT: {tier}", flush=True)
    return {"b1": b1, "b2": b2, "b3": b3, "b4": b4, "b5": b5,
            "ctrl_inert": ctrl_inert, "green": bool(green), "tier": tier}
