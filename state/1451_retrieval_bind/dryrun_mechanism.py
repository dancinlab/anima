#!/usr/bin/env python3
"""Local CPU dry-run of the H_1451 retrieval-bind MECHANISM (no real ckpt / no GPU / no torch).

Validates the harness logic end-to-end with a STUB mouth (deterministic content), so the
B3 cross-shuffle / retrieval-OFF / shuffle-memory CONTROLS are proven to behave correctly
BEFORE spending GPU. This is NOT a verdict (no real 303M mouth) — it is a frozen-first wiring
check that the cross-shuffle COLLAPSE is measured correctly and is not a coding artifact.

It execs g6_rb_common's body with the three PROBES imports (gauge/h1129/h1305) pre-stubbed,
so retrieval / weld / B3 instrument / bars run the SAME code as the real GPU run.
"""
import os, sys, types, re

HERE = os.path.dirname(os.path.abspath(__file__))

# ── gauge stub (mouth + word helpers) ──
gauge = types.ModuleType("gauge")
_KNOWN = set(("temperature memory signal market population pressure attention current price "
              "colony river alloy crowd sample fold higher longer stronger greater denser "
              "larger faster tighter more degree duration frequency value density magnitude "
              "level rate ratio size speed strength count amount distance changes measurable "
              "influences outcome under load stress the of by if when than").split())
def _words(s):
    return [w for w in re.findall(r"[a-zA-Z]+", s.lower())]
def known_word_ratio(t):
    ws = _words(t)
    return (sum(1 for w in ws if w in _KNOWN) / len(ws)) if ws else 0.0
def _jaccard(a, b):
    return (len(a & b) / len(a | b)) if (a | b) else 1.0
_TOPIC_CONTENT = {  # distinct content per topic so DIST / held-out logic is exercised
    "temperature": "rises and falls across the seasons here",
    "memory": "fades slowly over many repeated trials",
    "signal": "propagates through the noisy channel today",
    "market": "swings widely between the open and close",
    "population": "spreads outward into the new region",
    "pressure": "builds inside the sealed chamber walls",
    "attention": "drifts away after a short interval",
    "current": "flows around the bend in the river",
    "price": "climbs after the harvest report lands",
    "colony": "expands toward the warmer southern slope",
}
def _decode(model, seed, max_new, torch, block=512, seed_rng=7, **kw):
    low = seed.lower()
    for t, c in _TOPIC_CONTENT.items():
        if t in low:
            return f"{t} {c}"
    return "the thing influences the outcome under load"
gauge._words = _words; gauge.known_word_ratio = known_word_ratio
gauge._jaccard = _jaccard; gauge._decode = _decode
gauge._KNOWN = _KNOWN; gauge._STOPWORDS = set("the a an of by if when than".split())

# ── h1305 stub (real structural detector shape) ──
h5 = types.ModuleType("h1305")
h5.COMPARATOR = {"if","when","whenever","than","more","less","greater","fewer","higher",
                 "lower","increases","decreases","correlates","predicts","causes","depends",
                 "unless","whereas","versus","compared","proportional","faster","slower",
                 "stronger","weaker","longer","denser","larger","tighter"}
h5.MEASURABLE = {"measure","measured","rate","number","count","amount","level","degree",
                 "threshold","ratio","frequency","probability","magnitude","score","value",
                 "quantity","percent","times","fraction","distance","duration","speed",
                 "size","strength","density"}
def _is_falsifiable(text):
    wl = _words(text)
    if not wl: return False
    wset = set(wl)
    a = bool(wset & h5.COMPARATOR); b = bool(wset & h5.MEASURABLE)
    content = [w for w in wl if len(w) >= 3 and w in _KNOWN and w not in gauge._STOPWORDS]
    c = len(content) >= 2 and not text.rstrip().endswith("?")
    return a and b and c
h5._is_falsifiable = _is_falsifiable

# ── h1129 stub (model arch unused — decode is stubbed) ──
h1129 = types.ModuleType("h1129")
class _Stub:
    training = False
    def to(self, d): return self
    def eval(self): return self
    def train(self): return self
h1129.ByteGPT = lambda **kw: _Stub()

# exec g6_rb_common body with stubs pre-injected (skip the heavy _load calls)
ns = {"__name__": "g6_rb_common", "__file__": os.path.join(HERE, "g6_rb_common.py")}
src = open(os.path.join(HERE, "g6_rb_common.py")).read()
# neutralize the torch import + _load calls so it runs torch-free
src = src.replace("import torch\n", "torch = None\n")
src = src.replace('g = _load("gauge", os.path.join(PROBES, "gauge_lib.py"))', "g = _GAUGE")
src = src.replace('h = _load("h1129", os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py"))', "h = _H1129")
src = src.replace('h5 = _load("h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))', "h5 = _H1305")
ns["_GAUGE"] = gauge; ns["_H1129"] = h1129; ns["_H1305"] = h5
exec(compile(src, ns["__file__"], "exec"), ns)


def main():
    C = types.SimpleNamespace(**ns)
    stub = _Stub(); cfg = {"block": 512}
    base = C.evaluate(stub, cfg, "base", mem=None, topics=C.EVAL_TOPICS)
    mem = C.build_memory(shuffle=False)
    rb = C.evaluate(stub, cfg, "retr_bind", mem=mem, topics=C.EVAL_TOPICS)
    off = C.evaluate(stub, cfg, "retr_off", mem=None, topics=C.EVAL_TOPICS)
    shuf = C.build_memory(shuffle=True)
    shufmem = C.evaluate(stub, cfg, "shuf_mem", mem=shuf, topics=C.EVAL_TOPICS)
    C.print_bars("DRYRUN MECHANISM (stub mouth — NOT a verdict)", base, rb,
                 off_eval=off, shufmem_eval=shufmem)
    print("\n[DRYRUN] base.FALS_in=%s rb.FALS_in=%s rb.COH_m=%s rb.COH_x=%s shufmem.COH_m=%s"
          % (base["FALS_in"], rb["FALS_in"], rb["COH_matched"], rb["COH_mismatched"],
             shufmem["COH_matched"]))
    print("[DRYRUN] sample welded:", rb["per_seed"][0]["in_texts"][0])
    print("[DRYRUN] cross-shuffle measurables:", rb["per_seed"][0]["cross_meas"])


if __name__ == "__main__":
    main()
