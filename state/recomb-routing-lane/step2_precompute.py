#!/usr/bin/env python3
"""H_9235 fork-A Step-2 (trained cross-attention retrieval lane) — PART 1: precompute frozen trunk states.

Fable Step-2 spec: a learned single-head cross-attention lane re-metricizes the frozen 303M hiddens so the
readout can RETRIEVE a distal concept's continuation (what Step-1's fixed dot-product cache could not, beyond
verbatim copy). The trunk stays frozen; only the ~3M-param lane trains. Since anima_py has no torch trunk .clm
loader, we precompute the trunk states ONCE per doc via the production numpy decode (byte-identical to eval),
store per-doc fp16 npz, and train the lane on GPU reading them (frozen yn reused across all epochs).

Corpus (Fable deltas on the retrain builder):
  FILLER + "concept: k1 k2 k3 k4 k5. " (5 of 8 kws SHOWN) + GAP(jitter 128-512) + concept-neutral STEM + TARGET
  - 70% retrieval: target = one of the 5 SHOWN kws (copy-across-gap; span only in pre-gap line, >=128 back)
  - 30% associative: target = one of the 3 UNSHOWN kws (anti-copy: assert span appears nowhere else in doc)
  - target span = the FULL keyword bytes (multi-byte; a single byte is a UTF-8-prior unigram shortcut)
  - stem concept-neutral (assert no >=3-byte ngram of any concept kw in stem)
  - 40 train / 8 lane-val concepts (concept-level; never the 12 eval concepts); ko+en both
Emits per-doc npz {yn fp16 [T,d], base_logits fp16 [T,V], gap_start, span_lo, span_hi, concept, retrieval, lang}.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "8")
import sys
import glob
import json
import random
import argparse

import numpy as np

_c = sorted(glob.glob(os.path.expanduser("~/.local/lib/python3.*/site-packages/anima_py")))
BASE = _c[-1] if _c else os.path.expanduser("~/.local/lib/python3.12/site-packages/anima_py")
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
import decode
import evaluate as E

RNG = random.Random(20260709)

# 40 train + 8 val english concepts (disjoint from the 12 eval concepts by keyword) + ko mirror keywords.
_WORDBANK = ("""
harbor pier anchor buoy trawler hull mast keel
meadow clover thistle bramble hedgerow pasture furrow haystack
turbine rotor bearing coil flange spindle bracket armature
opera aria cadence timbre baton libretto refrain motif
auction bidder tariff invoice broker vendor ledger receipt
clinic scalpel gauze suture vaccine syringe ointment splint
tundra permafrost lichen caribou taiga fjord scree bracing
telescope quasar pulsar meteor asteroid corona parallax zenith
bakery dough kneading yeast oven crust glaze crumb
tribunal plaintiff subpoena docket affidavit statute counsel bailiff
avalanche cornice serac icefall snowfield glissade couloir arete
transistor capacitor inductor breadboard oscillator relay heatsink jumper
orchard pruning grafting blossom pollen harvest cider bushel
foundry crucible smelter ingot slag bellows tongs mold
library archive folio manuscript catalog stack carrel binding
volcano magma caldera basalt fissure pumice vent lava
studio easel palette canvas pigment varnish brushwork sketch
railway locomotive signal platform sleeper junction siding gauge
brewery mash hops wort fermenter cask lager stout
observatory dome mirror aperture spectra nebula transit ephemeris
marsh reed heron cattail bog silt mudflat estuary
printshop press typeset galley folio2 quire deckle colophon
vineyard trellis tendril cellar vintage tannin cork must
quarry granite chisel derrick rubble seam blast talus
aquarium coral anemone tank filter reef fry brine
cannery retort seam2 brine2 label crate hopper skiff
cockpit altimeter throttle rudder aileron flap yoke seatbelt
apiary hive comb nectar drone forager swarm royal
smithy anvil forge hammer quench temper billet horseshoe
weaver loom warp weft shuttle spindle2 heddle selvage
pharmacy dosage tablet capsule compound remedy tincture lozenge
seismograph tremor fault epicenter magnitude aftershock rupture reading
starfield planetarium orbit comet stellar cosmos spiral halo
mill sluice weir flume paddle grist hopper2 chute
tannery hide vat lime scraper currier buffing awl
distillery still copper reflux congener proof column spirit
glassworks kiln blowpipe frit anneal gather punty marver
cartography meridian contour datum geoid azimuth graticule legend
hatchery roe alevin fingerling raceway ova milt weir3
refractor eyepiece finder mount tracking dew declination sidereal
loomery skein carding fleece roving distaff niddy hank
kilnworks refractory brick fireclay flue damper cinder grate
switchboard breaker fuse busbar conduit terminal ampere ground
cathedral nave transept apse buttress spire vault crypt
jetty groyne bollard fender slipway dredge lighthouse quay
telegraph sounder morse dispatch operator2 pole insulator wire2
skein2 carding2 fleece2 roving2 distaff2 niddy2 hank2 batt
foundry2 bloom puddle wrought fettle scarf ladle tuyere
""").split()

_EVAL_KW = set()
for kws in E._SG1_CONCEPTS.values():
    _EVAL_KW.update(kws)

_STEMS = ["the next thing that comes to mind is ", "what surfaces here is ",
          "the note that follows reads ", "a plain remark to set down is ",
          "here one might jot ", "the line recorded next is ",
          "and then simply ", "a small aside to add is ",
          "the closing word here is ", "one more item is "]
_FILLERS = ["a quiet log entry opens without fanfare. ",
            "here is an ordinary preface set down for later. ",
            "the small record below begins plainly. ",
            "a neutral header precedes the rest. "]
_GAP_WORDS = ("and so the discussion drifts along on unrelated matters touching nothing in particular "
              "and simply passing the time while the page fills with words of no special weight ").split()


def build_concepts():
    words = [w for w in _WORDBANK if w not in _EVAL_KW]
    concepts = {}
    i = 0
    for k in range(len(words) // 8):
        kws = words[k * 8:(k + 1) * 8]
        if len(kws) < 8 or (set(kws) & _EVAL_KW):
            continue
        concepts["C%02d" % i] = kws
        i += 1
        if i >= 48:
            break
    names = list(concepts)
    return {n: concepts[n] for n in names[:40]}, {n: concepts[n] for n in names[40:48]}


def _gap(nbytes):
    out = []
    n = 0
    while n < nbytes:
        w = RNG.choice(_GAP_WORDS)
        out.append(w)
        n += len(w) + 1
    return " ".join(out) + ". "


def make_doc(concept, kws):
    """returns (text, gap_start_byte, span_lo_byte, span_hi_byte, retrieval, target_kw)."""
    shown = RNG.sample(kws, 5)
    unshown = [k for k in kws if k not in shown]
    retrieval = RNG.random() < 0.7
    target = RNG.choice(shown) if retrieval else RNG.choice(unshown)
    filler = RNG.choice(_FILLERS)
    line = concept + ": " + " ".join(shown) + ". "
    gap = _gap(RNG.randint(128, 224))   # >=128 exceeds conv RF (distal) while capping T for forward cost
    # concept-neutral stem: reject any stem containing a >=3-byte ngram of any kw
    for _ in range(20):
        stem = RNG.choice(_STEMS)
        bad = any((k[:3] in stem) for k in kws)
        if not bad:
            break
    pre = filler + line + gap + stem
    text = pre + target
    pb = pre.encode("utf-8", "ignore")
    tb = target.encode("utf-8", "ignore")
    gap_start = len((filler + line).encode("utf-8", "ignore"))
    span_lo = len(pb)
    span_hi = span_lo + len(tb)
    # anti-copy for associative: target span must appear nowhere else
    if not retrieval:
        if target in (filler + line + gap + stem):
            return None
    return text, gap_start, span_lo, span_hi, retrieval, target


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm"))
    ap.add_argument("--per", type=int, default=100, help="docs per concept")
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_states"))
    ap.add_argument("--maxT", type=int, default=520)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    train_c, val_c = build_concepts()
    print("train concepts=%d val=%d" % (len(train_c), len(val_c)), flush=True)
    mouth = E._Mouth(a.ckpt)
    W = mouth.W
    manifest = {"train": list(train_c), "val": list(val_c), "docs": []}
    n = 0
    for split, cmap in (("train", train_c), ("val", val_c)):
        for concept, kws in cmap.items():
            made = 0
            tries = 0
            while made < a.per and tries < a.per * 3:
                tries += 1
                doc = make_doc(concept, kws)
                if doc is None:
                    continue
                text, gap_start, span_lo, span_hi, retrieval, target = doc
                tok = np.array([b for b in text.encode("utf-8", "ignore")], dtype=np.float64)
                T = len(tok)
                if T > a.maxT:
                    continue
                yn, logits = decode.clm_forward_hidden_logits(W, tok, T)
                fn = "%s_%06d.npz" % (split, n)
                np.savez(os.path.join(a.out, fn),
                         yn=yn.astype(np.float16), base=logits.astype(np.float16),
                         tok=tok.astype(np.int16),
                         meta=np.array([gap_start, span_lo, span_hi, int(retrieval), T], dtype=np.int32))
                manifest["docs"].append({"fn": fn, "split": split, "concept": concept,
                                         "target": target, "retrieval": bool(retrieval), "T": T})
                n += 1
                made += 1
                if n % 100 == 0:
                    print("  precomputed %d docs" % n, flush=True)
    json.dump(manifest, open(os.path.join(a.out, "manifest.json"), "w"))
    print("DONE precompute %d docs -> %s" % (n, a.out), flush=True)


if __name__ == "__main__":
    main()
