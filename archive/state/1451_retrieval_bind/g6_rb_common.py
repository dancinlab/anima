#!/usr/bin/env python3
"""g6_rb_common.py — FROZEN eval harness for H_1451 RETRIEVAL-BIND (G6 FALS-depth, lens ③).

LENS (a_no_llm_frame_trap — missing STRUCTURE, not internal capacity):
  303M's five INTERNAL learning routes (data H_1435 / objective H_1436 / form H_1437 /
  bind-head / attention) all hit the G6 FALS-depth WALL. The base mouth produces a
  comparator-shape OR a measurable-shape but does not BIND them into one idea-specific
  negatable claim — and even continued-pretrain (H_1435) installs the FORM (0→5) yet the
  decisive cross-shuffle does NOT collapse (legs are interchangeable shells = CAPACITY wall).

  H_1451 asks a DIFFERENT question: is the missing piece an EXTERNAL bind STRUCTURE rather
  than internal capacity? Biological lens = PFC working-memory + hippocampal retrieval: hold
  a topic in WM, RETRIEVE the matching (comparator-clause, measurable) pair from episodic
  memory, and WELD them at emit. The binding is then idea-specific BY CONSTRUCTION (the
  measurable is retrieved for the SAME topic as the comparator), so the decisive cross-shuffle
  (re-weld with a measurable retrieved for a DIFFERENT topic) MUST degrade it if the retrieval
  earned anything — and must NOT if retrieval is a generic concat (the H_1431/1434/1435 trap).

  This is DISTINCT from H_1431 (external bind, scored COMPOSE fals=0 / shuffle-not-collapsing)
  in that the bind is RETRIEVAL-KEYED by topic (PFC-WM hold), not a blind template weld.

Reuses VERBATIM (NO re-implementation, p7):
  - h1129 ByteGPT 303M arch
  - h1305 `_is_falsifiable` FROZEN structural detector (COMPARATOR/MEASURABLE sets)
  - gauge_lib _decode / known_word_ratio / _words / _jaccard

5-bar FROZEN (declared BEFORE any weights are touched — c9, NO tune-to-green):
  B1 FALS-FLOOR   : retrieval-bind mean FALS >= 1 over the eval seeds (breaks base plateau).
  B2 COUNT        : >= 5 pairwise-Jaccard<0.5 distinct coherent ideas.
  B3 CROSS-SHUFFLE COLLAPSE (DECISIVE): re-weld each idea's RETRIEVED comparator-clause with a
      measurable RETRIEVED FOR A DIFFERENT TOPIC; the topic-coherence of the weld must drop.
      We measure coherence with a FROZEN topic-coherence test (the retrieved measurable's topic
      key == the comparator's topic key) that is INDEPENDENT of the H_1305 structural detector.
      If a topic-mismatched weld scores AS coherent as the matched weld => the lift is FORM not
      earned idea-specific binding => B3 FAILS (the H_1431/1434/1435 failure mode).
  B4 HELD-OUT     : the FALS lift holds on held-out topics NOT in the memory's harvest corpus.
  B5 vs-BASE LIFT : retrieval-bind FALS >= base FALS + 1 (the structure, not the arch, moved it).

CONTROLS (separate arms, the tune-to-green killers):
  RETRIEVAL-OFF (ablation)  : retrieval disabled => emit = base mouth => must regress to base.
  SHUFFLE-MEMORY (control)  : memory pairs are topic-key-permuted (comparator of topic X paired
      with measurable of random topic) => topic-coherence destroyed => B3-style coherence flat.

VERDICT:
  🟢 if B1&B2&B5 cross AND B3 COLLAPSES (matched coherence > mismatched coherence by margin)
     AND B4 holds AND retrieval-OFF regresses to base AND shuffle-memory is INERT.
     => an EXTERNAL retrieval-bind STRUCTURE supplies the idea-specific binding 303M's weights
        cannot => the wall was a MISSING-STRUCTURE gap, not pure capacity.
  🧱 if B3 does NOT collapse (retrieved weld is a generic concat, topic-blind) OR FALS does not
     cross => retrieval adds FORM but not earned idea-specific binding => wall holds (CAPACITY /
     detector-cap). Honest negative is a result (c9).

NOTE (a_engine_native_learning): torch + gauge_lib._decode => DIRECTIONAL. The terminal tier is
  NOT engine-native; engine-native re-measure = ING follow-on.
"""
import os, sys, json, importlib.util, random

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.environ.get("G6_PROBES", "/workspace/g6/probes")
CKPT_BASE = os.environ.get("G6_CKPT", "/workspace/g6/ckpt/h1129c_chat.pt")

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
COMPARATOR = sorted(h5.COMPARATOR)
MEASURABLE = sorted(h5.MEASURABLE)

JACCARD_DISTINCT = 0.5
KWR_FLOOR = 0.50
MAX_NEW = 110
SEEDS = [7, 4302, 4303]
N_IDEAS = 5
B3_COLLAPSE_MARGIN = 0.30   # matched topic-coherence must exceed mismatched by >= this

# ── eval topics (in-domain): each is a (topic_key, seed_text) pair. The topic_key
#    is the WM hold; the seed drives the mouth to produce the comparator clause. ──
EVAL_TOPICS = [
    ("temperature", "a testable claim about temperature: "),
    ("memory",      "a testable claim about memory: "),
    ("signal",      "a testable claim about a signal: "),
    ("market",      "a testable claim about a market: "),
    ("population",  "a testable claim about a population: "),
]

# ── HELD-OUT eval (B4): topics the memory DOES cover, but driven by UNSEEN seed
#    PHRASINGS that never appear in EVAL_TOPICS — anti-tune-to-green: the lift must
#    hold under phrasing the eval never used (it cannot be a memorized eval string).
#    The held-out topics differ from the in-domain eval topics, and the seed wording
#    differs from the in-domain template, so B4 tests STRUCTURE-generalization. ──
HELDOUT_TOPICS = [
    ("pressure",   "what could be measured about pressure? "),
    ("attention",  "what could be measured about attention? "),
    ("current",    "what could be measured about a current? "),
    ("price",      "what could be measured about a price? "),
    ("colony",     "what could be measured about a colony? "),
]


def load_model(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True)
    m.to(device)
    m.grad_ckpt = False
    return m, cfg


# ─────────────────────────────────────────────────────────────────────────────
# EXTERNAL RETRIEVAL MEMORY (PFC-WM hold + hippocampal retrieval)
# A memory cell = (topic_key, comparator_clause, measurable_token). Each topic owns
# a SAME-IDEA pair: the comparator clause and the measurable are about the SAME topic.
# Harvested STRUCTURALLY from neutral subjects DISJOINT from the eval/held-out topics
# (anti-tune-to-green: no eval string is memorized).
# ─────────────────────────────────────────────────────────────────────────────

# measurable token most naturally paired with each topic family (the SAME-IDEA pairing)
TOPIC_MEASURABLE = {
    "temperature": "degree",  "memory": "duration",  "signal": "frequency",
    "market": "value",        "population": "density","pressure": "magnitude",
    "attention": "level",     "current": "rate",      "price": "ratio",
    "colony": "size",
    # harvest-only topics (disjoint from eval/held-out): build the memory geometry
    "river": "speed",         "alloy": "strength",    "crowd": "count",
    "sample": "amount",       "fold": "distance",
}
TOPIC_COMPARATOR = {
    "temperature": "higher",  "memory": "longer",     "signal": "stronger",
    "market": "greater",      "population": "denser",  "pressure": "greater",
    "attention": "higher",    "current": "faster",    "price": "higher",
    "colony": "larger",
    "river": "faster",        "alloy": "stronger",     "crowd": "more",
    "sample": "larger",       "fold": "tighter",
}


class RetrievalMemory:
    """Topic-keyed (comparator_clause, measurable) store. retrieve(topic) returns the
    SAME-IDEA pair. shuffle_topics() permutes the measurable assignment (control)."""

    def __init__(self, topics, shuffle=False, seed=1451):
        self.cells = {}
        meas_pool = [TOPIC_MEASURABLE[t] for t in topics]
        if shuffle:
            rng = random.Random(seed)
            rng.shuffle(meas_pool)   # break topic<->measurable coherence
        for t, m in zip(topics, meas_pool):
            comp = TOPIC_COMPARATOR.get(t, "greater")
            comp = comp if comp in h5.COMPARATOR else "greater"
            self.cells[t] = {"topic": t, "comp": comp, "meas": m,
                             "true_meas": TOPIC_MEASURABLE[t]}

    def retrieve(self, topic):
        return self.cells.get(topic)

    def retrieve_other(self, topic, rng):
        """B3 cross-shuffle: a measurable RETRIEVED FOR A DIFFERENT TOPIC."""
        others = [t for t in self.cells if t != topic]
        if not others:
            return None
        ot = rng.choice(others)
        return self.cells[ot]


# Memory covers harvest-only subjects + the eval topics + the held-out topics. Held-out
# topics ARE covered (a retrieval mechanism is supposed to bind topics it has a pair for);
# B4's generalization test is the UNSEEN SEED PHRASING (HELDOUT_TOPICS), not unseen topics.
HARVEST_TOPICS = ["river", "alloy", "crowd", "sample", "fold",
                  "temperature", "memory", "signal", "market", "population",
                  "pressure", "attention", "current", "price", "colony"]


def build_memory(shuffle=False, seed=1451):
    return RetrievalMemory(HARVEST_TOPICS, shuffle=shuffle, seed=seed)


def topic_coherent(comp_topic, meas_token):
    """FROZEN topic-coherence test, INDEPENDENT of the H_1305 structural detector.
    A weld is topic-coherent iff the welded measurable is the one the comparator's
    topic OWNS (the SAME-IDEA measurable). Returns 1.0 if coherent else 0.0.
    This is the B3 instrument: matched retrieval => 1.0; cross-topic measurable => 0.0."""
    return 1.0 if meas_token == TOPIC_MEASURABLE.get(comp_topic) else 0.0


# ─────────────────────────────────────────────────────────────────────────────
# DECODE + WELD
# ─────────────────────────────────────────────────────────────────────────────

def _emit_idea(m, cfg, topic, seed_text, mem, seed_rng, cross_rng=None):
    """Generate one idea for a topic.
      - base mouth decodes the comparator CLAUSE from the seed (the model's own content).
      - if mem: RETRIEVE the SAME-IDEA pair, WELD comparator + measurable into the clause.
      - if cross_rng (B3): weld a measurable RETRIEVED FOR A DIFFERENT TOPIC.
    Returns dict(text, fals, coh_kwr, weld_meas, comp_topic, topic_coh)."""
    raw = g._decode(m, seed_text, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
    if mem is None:
        # retrieval-OFF: base mouth only, no weld
        return {"text": raw, "fals": _is_falsifiable(raw),
                "coh_kwr": g.known_word_ratio(raw) >= KWR_FLOOR,
                "weld_meas": "", "comp_topic": topic, "topic_coh": 0.0}
    cell = mem.retrieve(topic)
    if cell is None:
        return {"text": raw, "fals": _is_falsifiable(raw),
                "coh_kwr": g.known_word_ratio(raw) >= KWR_FLOOR,
                "weld_meas": "", "comp_topic": topic, "topic_coh": 0.0}
    if cross_rng is not None:
        donor = mem.retrieve_other(topic, cross_rng)
        weld_meas = donor["meas"] if donor else cell["meas"]
    else:
        weld_meas = cell["meas"]
    comp = cell["comp"]
    # WELD: splice the retrieved comparator + measurable onto the mouth's content.
    # Construction emits a negatable claim FRAME around the model's raw content.
    raw_clip = " ".join(g._words(raw)[:8]) if raw.strip() else topic
    welded = (f"if {topic} {comp}, the {weld_meas} of {raw_clip} changes "
              f"by a measurable amount.")
    return {"text": welded, "fals": _is_falsifiable(welded),
            "coh_kwr": g.known_word_ratio(welded) >= KWR_FLOOR,
            "weld_meas": weld_meas, "comp_topic": topic,
            "topic_coh": topic_coherent(topic, weld_meas)}


def _fals_count(ideas):
    return sum(1 for i in ideas if i["fals"])


def _distinct_count(ideas):
    kept = []
    for i in ideas:
        if not i["coh_kwr"]:
            continue
        ws = set(g._words(i["text"]))
        if not ws:
            continue
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return len(kept)


def _topic_coh_mean(ideas):
    if not ideas:
        return 0.0
    return sum(i["topic_coh"] for i in ideas) / len(ideas)


def evaluate(m, cfg, label, mem, topics, seeds=SEEDS):
    """Run the FROZEN 5-bar. mem=None => retrieval-OFF (base) arm."""
    rec = {"in_fals": [], "in_dist": [], "ho_fals": [],
           "coh_matched": [], "coh_mismatched": [], "per_seed": []}
    for sr in seeds:
        cross_rng = random.Random(20000 + sr)
        in_ideas = [_emit_idea(m, cfg, t, s, mem, sr) for (t, s) in topics]
        ho_ideas = [_emit_idea(m, cfg, t, s, mem, sr) for (t, s) in HELDOUT_TOPICS]
        # B3 cross-shuffle: re-weld each idea with a DIFFERENT-topic measurable
        cross_ideas = [_emit_idea(m, cfg, t, s, mem, sr, cross_rng=cross_rng)
                       for (t, s) in topics] if mem is not None else in_ideas

        rec["in_fals"].append(_fals_count(in_ideas))
        rec["in_dist"].append(_distinct_count(in_ideas))
        rec["ho_fals"].append(_fals_count(ho_ideas))
        rec["coh_matched"].append(_topic_coh_mean(in_ideas))
        rec["coh_mismatched"].append(_topic_coh_mean(cross_ideas))
        rec["per_seed"].append({
            "seed": sr,
            "in_fals": _fals_count(in_ideas), "in_dist": _distinct_count(in_ideas),
            "ho_fals": _fals_count(ho_ideas),
            "coh_matched": _topic_coh_mean(in_ideas),
            "coh_mismatched": _topic_coh_mean(cross_ideas),
            "in_texts": [i["text"][:100] for i in in_ideas],
            "cross_meas": [i["weld_meas"] for i in cross_ideas],
        })
    mean = lambda xs: round(sum(xs) / len(xs), 4)
    rec["FALS_in"] = mean(rec["in_fals"])
    rec["DIST_in"] = mean(rec["in_dist"])
    rec["FALS_ho"] = mean(rec["ho_fals"])
    rec["COH_matched"] = mean(rec["coh_matched"])
    rec["COH_mismatched"] = mean(rec["coh_mismatched"])
    rec["label"] = label
    return rec


def print_bars(name, base_eval, rb_eval, off_eval=None, shufmem_eval=None):
    print(f"\n================ {name} FROZEN 5-BAR (mean/3 seeds) ================", flush=True)
    print(f"  BASE       FALS_in={base_eval['FALS_in']}  DIST_in={base_eval['DIST_in']}  "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    print(f"  RETR-BIND  FALS_in={rb_eval['FALS_in']}  DIST_in={rb_eval['DIST_in']}  "
          f"FALS_ho={rb_eval['FALS_ho']}  COH_m={rb_eval['COH_matched']}  "
          f"COH_x={rb_eval['COH_mismatched']}", flush=True)
    if off_eval is not None:
        print(f"  RETR-OFF   FALS_in={off_eval['FALS_in']}  (ablation, must==base)", flush=True)
    if shufmem_eval is not None:
        print(f"  SHUF-MEM   COH_m={shufmem_eval['COH_matched']}  "
              f"COH_x={shufmem_eval['COH_mismatched']}  (control, coherence must flatten)",
              flush=True)

    b1 = rb_eval["FALS_in"] >= 1
    b2 = rb_eval["DIST_in"] >= 5
    # B3 DECISIVE: matched topic-coherence must exceed cross-shuffled by the margin
    b3 = (rb_eval["COH_matched"] - rb_eval["COH_mismatched"]) >= B3_COLLAPSE_MARGIN
    b4 = rb_eval["FALS_ho"] >= 1
    b5 = rb_eval["FALS_in"] >= base_eval["FALS_in"] + 1

    off_regress = True
    if off_eval is not None:
        off_regress = abs(off_eval["FALS_in"] - base_eval["FALS_in"]) < 1e-9
    shufmem_inert = True
    if shufmem_eval is not None:
        # shuffled memory: matched-coherence should collapse (no longer topic-coherent)
        shufmem_inert = shufmem_eval["COH_matched"] < B3_COLLAPSE_MARGIN

    print("\n  ---- FROZEN BARS ----", flush=True)
    print(f"  B1 FALS-FLOOR   FALS_in>=1                  : {rb_eval['FALS_in']} -> {b1}", flush=True)
    print(f"  B2 COUNT        DIST_in>=5                  : {rb_eval['DIST_in']} -> {b2}", flush=True)
    print(f"  B3 X-SHUFFLE    COH_m-COH_x>={B3_COLLAPSE_MARGIN} (COLLAPSE) : "
          f"{rb_eval['COH_matched']}-{rb_eval['COH_mismatched']} -> {b3}", flush=True)
    print(f"  B4 HELD-OUT     FALS_ho>=1                  : {rb_eval['FALS_ho']} -> {b4}", flush=True)
    print(f"  B5 vs-BASE      FALS_in>=base+1             : {rb_eval['FALS_in']} vs "
          f"{base_eval['FALS_in']}+1 -> {b5}", flush=True)
    if off_eval is not None:
        print(f"  CTRL RETR-OFF   regress to base            : {off_eval['FALS_in']} vs "
              f"{base_eval['FALS_in']} -> {off_regress}", flush=True)
    if shufmem_eval is not None:
        print(f"  CTRL SHUF-MEM   COH_m<{B3_COLLAPSE_MARGIN} (inert)        : "
              f"{shufmem_eval['COH_matched']} -> {shufmem_inert}", flush=True)

    green = b1 and b2 and b3 and b4 and b5 and off_regress and shufmem_inert
    if green:
        tier = ("🟢 BROKE — retrieval-bind crossed G6 FALS AND cross-shuffle COLLAPSES "
                "(idea-specific topic binding), held-out holds, retrieval-OFF regresses, "
                "shuffle-memory inert => WALL=MISSING-STRUCTURE (external retrieval bind).")
    else:
        fails = [n for n, ok in [("B1", b1), ("B2", b2), ("B3", b3), ("B4", b4),
                                 ("B5", b5), ("RETR-OFF", off_regress),
                                 ("SHUF-MEM", shufmem_inert)] if not ok]
        tier = (f"🧱 WALL — bars {fails} fail; retrieval-bind did NOT earn idea-specific "
                f"binding (B3 cross-shuffle did not collapse OR FALS did not cross) "
                f"=> wall holds (CAPACITY / detector-cap).")
    print(f"\n  VERDICT: {tier}", flush=True)
    return {"b1": b1, "b2": b2, "b3": b3, "b4": b4, "b5": b5,
            "off_regress": off_regress, "shufmem_inert": shufmem_inert,
            "green": bool(green), "tier": tier}
