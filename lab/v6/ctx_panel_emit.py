"""V6_19 -- emit the natural transport panel in the EXISTING weave-panel schema, and record the
one mismatch that would otherwise make its bar unreadable.

V6_18 established the panel is constructible. This asks the a_experiment_engine_native question:
can it be scored by an existing `anima-py` flag instead of a script beside the engine?

It nearly can. H_9825 already added `--weave-panel <file>`, which swaps the frozen 12-item
battery for a manifest, "bar, controls and scorer UNTOUCHED -- only n moves". Its item shape is
{cue, target, swap_cue, bind_cue, lang}, and the correspondence to what BOTH divergence models
independently demanded is exact:

    swap_cue  atom-swap[FORM]   one atom changed so target is WRONG   ==  shuffled-referent arm
    bind_cue  bind-strip[BIND]  atoms present, compose-op removed     ==  truncated-context arm
    null                        base rate unprompted                  ==  truth-zero floor

So no new engine code is needed to RUN it. This script emits the manifest.

*** THE MISMATCH, recorded before anything is fired ***

The weave scorer is `mouth.ideate(cue, 24 tokens)` then "did the target string surface" -- FREE
IDEATION, not a forced choice among the candidates. V6_18's census computed realized chance
0.2391 and its copy-only baselines under a FORCED-CHOICE readout. Those are different readouts
and their numbers are not interchangeable:

  forced choice over K candidates : chance = (1/N) sum 1/K_i = 0.2391
  free ideation, does gold surface: chance = the null base rate, near zero

Reading V6_18's numbers against the frozen 0.30 bar / 0.15 control cap would compare a quantity
computed under one readout to a threshold calibrated for the other. That is exactly
instrument-claim-alignment-before-reading-a-bar, and it is also how the G6 gate failed. The bar
for this panel must be derived from ITS realized readout and frozen BEFORE the first run --
never re-anchored afterwards (burned-gate-no-refreeze-sequential-gating).

ON-STANDARD (p9): eval-side harvest from held-out natural documents; training corpus untouched.
"""
import json
import re
import sys
from collections import Counter

from corpus_path import natural_corpus

RF = 35
ENT = re.compile(rb"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")


def harvest(lines, limit=None):
    out = []
    for di, l in enumerate(lines):
        ms = [(m.start(), m.group(1)) for m in ENT.finditer(l)]
        if len(ms) < 3:
            continue
        first = {}
        for k, (p, e) in enumerate(ms):
            key = e.lower()
            if key in first:
                gap = p - first[key][0]
                prior = [x for _, x in ms[:k]]
                cands = list(dict.fromkeys(x.lower() for x in prior))
                if gap > RF and len(cands) >= 2 and p >= RF:
                    out.append({
                        "doc": di, "pos": p, "gold": e.decode("utf-8", "replace"),
                        "first_at": first[key][0], "first_len": len(first[key][1]),
                        "line": l, "cands": [x.decode("utf-8", "replace") for x in prior],
                    })
            else:
                first[key] = (p, e)
        if limit and len(out) >= limit:
            break
    return out


def build(site, rng_pick):
    """cue        = the document up to the target -- the earlier mention IS in it (transport possible)
       swap_cue   = same, with EVERY occurrence of the gold entity replaced by a different
                    candidate (FORM control: the gold is now the wrong answer AND is not copyable
                    from anywhere in the cue). Replacing only the FIRST mention was the version
                    this script shipped first, and the round-trip check caught it: entities are
                    routinely mentioned three or more times, so 24.8% of items kept the gold
                    elsewhere in the swapped cue and a pure copier would have scored on the FORM
                    arm for a reason having nothing to do with transport.
       bind_cue   = only the local RF window before the target (BIND control: the earlier mention is
                    gone, so anything correct came from the local window, not from transport)"""
    l, p, a, alen = site["line"], site["pos"], site["first_at"], site["first_len"]
    cue = l[:p].decode("utf-8", "replace")
    other = rng_pick(site)
    gold = site["gold"].encode("utf-8")
    swap = re.sub(re.escape(gold), other.encode("utf-8"), l[:p], flags=re.I).decode("utf-8", "replace")
    bind = l[max(0, p - RF):p].decode("utf-8", "replace")
    return {"cue": cue, "target": site["gold"], "swap_cue": swap, "bind_cue": bind, "lang": "en"}


def main():
    import random
    lines = [l for l in open(natural_corpus(), "rb").read().split(b"\n") if l.strip()]
    sites = harvest(lines)
    print(f"harvested {len(sites):,} transport sites across "
          f"{len(set(s['doc'] for s in sites)):,} independent documents")

    rnd = random.Random(9825)

    def pick(site):
        """The replacement must not REINTRODUCE the gold. Excluding only exact equality left 66
        items where the gold survived as a substring of its own replacement ("Alexander" replaced
        by "Alexander the Great"), which the emit guard caught."""
        g = site["gold"].lower()
        pool = [c for c in site["cands"]
                if c.lower() != g and g not in c.lower() and c.lower() not in g]
        return rnd.choice(pool) if pool else None

    items, nocand = [], 0
    for s in sites:
        if pick(s) is None:      # every candidate overlaps the gold -> no clean FORM control
            nocand += 1
            continue
        items.append(build(s, pick))
    print(f"  sites with no gold-disjoint distractor : {nocand} -- dropped (no clean FORM control)")
    # sanity the controls actually differ from the cue -- an identical control is a dead arm
    same_swap = sum(1 for i, it in enumerate(items) if it["swap_cue"] == it["cue"])
    same_bind = sum(1 for it in items if it["bind_cue"] == it["cue"])
    print(f"  swap_cue identical to cue : {same_swap}  (must be 0 -- else the FORM arm is dead)")
    print(f"  bind_cue identical to cue : {same_bind}  (must be 0 -- else the BIND arm is dead)")
    if same_swap or same_bind:
        raise SystemExit("dead control arm -- refusing to emit")

    # gold must not already sit inside the BIND control window, or the arm answers itself
    leak = sum(1 for it in items if it["target"].lower() in it["bind_cue"].lower())
    print(f"  gold visible inside bind_cue window : {leak} "
          f"({100*leak/len(items):.2f}%) -- these are dropped")
    items = [it for it in items if it["target"].lower() not in it["bind_cue"].lower()]
    # the FORM arm is only a control if the gold cannot be copied from the swapped cue at all
    swap_leak = sum(1 for it in items if it["target"].lower() in it["swap_cue"].lower())
    print(f"  gold still copyable from swap_cue   : {swap_leak} "
          f"(must be 0 -- a pure copier would score on the FORM arm)")
    if swap_leak:
        raise SystemExit("FORM control leaks the gold -- refusing to emit")

    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ctx_transport_panel.json"
    payload = {"schema": "anima-weavepanel/v1-ctxtransport", "n": len(items), "items": items}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print(f"\nemitted {len(items):,} items -> {out}")
    print("\nrun (engine-native, no new engine code):")
    print(f"  anima-py evaluate <clm> --rho-axon --weave-panel {out}")
    print("\n*** the bar is NOT readable yet: the weave scorer is free ideation, V6_18's chance")
    print("    0.2391 is forced choice. Derive and FREEZE this panel's own bar first. ***")


main()
