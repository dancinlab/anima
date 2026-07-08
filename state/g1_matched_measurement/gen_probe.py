#!/usr/bin/env python3
"""H_6189 — matched-surface + window-resident G1 probe generator (Fable spec).
Derives probe_spec.json from state/g1_coverage_prod_block/design.json (seed 6185, deterministic).
NO ckpt touched here — pure prompt construction + window-fit + integrity greps. Frozen-first:
templates + pair set + window arithmetic are fixed by rule BEFORE any decode.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DESIGN = os.path.join(ROOT, "state/g1_coverage_prod_block/design.json")
BLOCKS = [os.path.join(ROOT, "state/g1_coverage_prod_block/corpus/en_block.txt")]

WINDOW = 24   # decode-window bytes (matches canonical numpy decode semantics)

d = json.load(open(DESIGN))
C = d["concepts_en"]; A = d["attrs_en"]          # 40 concepts, 40 attrs (index-aligned)
HELD = [tuple(p) for p in d["held_out"]]          # 40 held-out index pairs
COVERED = [tuple(p) for p in d["covered_pairs"]]  # 185 covered pairs

# ── templates (truncated at completion point; expect attr(first), attr(second)) ──
# chosen by window arithmetic (gap = bytes from end of first concept to completion):
TEMPLATES = {
    "T0": lambda a, b: f"the {a} and the {b} yield ",     # counterexample form (ember+dune)
    "T3": lambda a, b: f"each {a} with {b} turns ",       # best window (shortest gap)
    "T7": lambda a, b: f"a {a} met a {b}; they showed ",  # worst window (window-dose arm)
}
UNARY = lambda a: f"{a} brings "                          # control (b): expect attr(a) only

def concept_suffix_unique(name, k):
    """Is the last k bytes of `name` a suffix of ONLY this concept among all 40?"""
    if k >= len(name): return True
    suf = name[-k:]
    return sum(1 for c in C if c.endswith(suf)) == 1

def window_fit(prompt, first_concept):
    """Fit iff the first concept's visible suffix in the last WINDOW bytes uniquely IDs it."""
    pb = prompt.encode()
    # byte end position of the first concept occurrence
    end = prompt.index(first_concept) + len(first_concept)
    end_b = len(prompt[:end].encode())
    gap = len(pb) - end_b                      # bytes from end of concept to completion
    visible = WINDOW - gap                     # bytes of the concept inside the window
    if visible <= 0: return False, visible
    return concept_suffix_unique(first_concept, visible), visible

def build():
    items = []
    def add(pair, order, tkey, arm):
        a_i, b_i = (pair if order == 0 else (pair[1], pair[0]))
        A1, B1 = C[a_i], C[b_i]
        prompt = TEMPLATES[tkey](A1, B1)
        fit, vis = window_fit(prompt, A1)
        items.append(dict(id=f"{arm}_{a_i}_{b_i}_{tkey}_{order}", prompt=prompt,
                          expect=[A[a_i], A[b_i]], arm=arm, template=tkey, order=order,
                          first=A1, second=B1, window_fit=bool(fit), visible=vis))
    # held-out arm: all 40 pairs, both orders, T0/T3/T7
    for p in HELD:
        for o in (0, 1):
            for t in ("T0", "T3", "T7"):
                add(p, o, t, "heldout")
    # seen arm: deterministic sample of covered pairs (index-strided for reproducibility)
    seen_sample = COVERED[::5][:40]   # 37 pairs, deterministic
    for p in seen_sample:
        for t in ("T0", "T3"):
            add(p, 0, t, "seen")
    # unary arm: all 40 concepts
    for i in range(len(C)):
        prompt = UNARY(C[i])
        items.append(dict(id=f"unary_{i}", prompt=prompt, expect=[A[i]], arm="unary",
                          template="unary", order=0, first=C[i], second=None,
                          window_fit=True, visible=WINDOW))
    return items

def integrity(items):
    """held-out pairs must be absent from the coverage blocks (by construction)."""
    block_text = ""
    for b in BLOCKS:
        if os.path.exists(b): block_text += open(b, encoding="utf-8").read()
    lines = block_text.splitlines()
    viol = []
    for p in HELD:
        A1, B1 = C[p[0]], C[p[1]]
        for ln in lines:
            if A1 in ln and B1 in ln:
                viol.append((A1, B1)); break
    return dict(block_lines=len(lines), heldout_cooccur_violations=viol)

if __name__ == "__main__":
    items = build()
    integ = integrity(items)
    assert not integ["heldout_cooccur_violations"], f"held-out leaked into blocks: {integ['heldout_cooccur_violations']}"
    out = os.path.join(HERE, "probe_spec.json")
    payload = dict(window=WINDOW, n_items=len(items),
                   arms={a: sum(1 for it in items if it["arm"] == a) for a in ("heldout", "seen", "unary")},
                   fit_counts={a: sum(1 for it in items if it["arm"] == a and it["window_fit"])
                               for a in ("heldout", "seen")},
                   integrity=integ, items=items)
    json.dump(payload, open(out, "w"), ensure_ascii=False, indent=1)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"probe_spec.json: {len(items)} items · arms={payload['arms']} · fit={payload['fit_counts']}")
    print(f"integrity: {integ['block_lines']} block lines · held-out cooccur violations={len(integ['heldout_cooccur_violations'])}")
    print(f"sha256={sha}")
    # ember+dune consistency check (⭐ counterexample must be held-out + T0 fit)
    ed = [it for it in items if it["first"] in ("ember", "dune") and it["second"] in ("ember", "dune")
          and it["template"] == "T0"]
    print("ember/dune T0 cells:", [(it["first"], it["second"], it["window_fit"], it["visible"]) for it in ed])
