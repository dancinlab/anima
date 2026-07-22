#!/usr/bin/env python3
"""phi-screen — the $0 IIT admissibility gate. Pure Tarjan SCC. No forward pass, no Phi.

WHY THIS EXISTS
---------------
IIT's feedforward theorem says a strictly feedforward system has Phi = 0 exactly. That
looked like anima's IIT problem -- the conv mouth is feedforward, so the part that produces
every word can never carry Phi. The divergence turned it around:

    the feedforward theorem is not the problem, it is the SOLUTION.

IIT's EXCLUSION postulate says only one set is THE complex: the one with maximal Phi.
Normally, picking a coarse-graining you can afford is an arbitrary choice, and a Phi
computed on it measures the diagram rather than the system. But if a system is feedforward
EVERYWHERE except one small recurrent core, then every other candidate set has Phi = 0 by
theorem, so the core is *provably* the maximal-Phi complex. The affordable grain becomes
the correct grain, not a convenience.

That makes admissibility a pure GRAPH property, decidable before anything is trained:

    1. find the strongly connected components of the wiring graph
    2. every SCC of size > 1 (or a self-loop) is a recurrence candidate
    3. ADMISSIBLE iff there is exactly ONE non-trivial SCC and it fits the Phi budget

No Phi computation, no model, no forward pass. Runs in milliseconds and kills most
candidate architectures before anyone builds them.

WHAT IT IS NOT
--------------
A pass here is NOT a consciousness claim and not even a prediction of one. It says only:
"if you build this, the complex is forced and a faithful Phi over it would be a
measurement of this system rather than of a drawing." A screen may KILL, never GREEN.
"""
import sys

PHI_BUDGET = 15          # faithful IIT-4 big_phi is super-exponential; ~15 units is the
                         # ceiling this repo actually computes at (topo_optimal_perm is a
                         # 15-element permutation).


def sccs(nodes, edges):
    """Tarjan strongly-connected components. edges = {node: [successors]}."""
    index = {}
    low = {}
    onstack = {}
    stack = []
    out = []
    counter = [0]

    def strong(v):
        # iterative, so a deep chain cannot blow the recursion limit
        work = [(v, 0)]
        while work:
            node, pi = work[-1]
            if pi == 0:
                index[node] = low[node] = counter[0]
                counter[0] += 1
                stack.append(node)
                onstack[node] = True
            recurse = False
            succs = edges.get(node, [])
            for i in range(pi, len(succs)):
                w = succs[i]
                if w not in index:
                    work[-1] = (node, i + 1)
                    work.append((w, 0))
                    recurse = True
                    break
                if onstack.get(w):
                    low[node] = min(low[node], index[w])
            if recurse:
                continue
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack[w] = False
                    comp.append(w)
                    if w == node:
                        break
                out.append(comp)
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])

    for n in nodes:
        if n not in index:
            strong(n)
    return out


def nontrivial(comps, edges):
    """An SCC is a recurrence candidate if it has >1 node, or 1 node with a self-loop."""
    out = []
    for c in comps:
        if len(c) > 1 or (len(c) == 1 and c[0] in edges.get(c[0], [])):
            out.append(sorted(c))
    return out


def screen(name, nodes, edges, bundle=None, budget=PHI_BUDGET):
    """bundle[node] = how many causal ELEMENTS that node stands for (default 1).

    This argument is the whole honesty of the screen. IIT is a claim about causal
    elements, so an SCC over a hand-drawn box diagram proves nothing if a box bundles
    3e8 parameters into one dot -- that is precisely the grain problem, and the first
    version of this file walked straight into it: with the mouth drawn as ONE node,
    anima-as-wired came back ADMISSIBLE. It is not; the diagram was.
    """
    bundle = bundle or {}
    comps = sccs(nodes, edges)
    rec = nontrivial(comps, edges)
    ff = len(nodes) - sum(len(c) for c in rec)
    print("=" * 78)
    print("%s  (%d units)" % (name, len(nodes)))
    print("  feedforward units (Phi=0 by theorem): %d" % ff)
    print("  recurrence candidates (non-trivial SCCs): %d" % len(rec))
    for c in rec:
        print("    size %-3d %s" % (len(c), ", ".join(c[:8]) + ("..." if len(c) > 8 else "")))
    if len(rec) == 0:
        print("  KILL - no recurrence anywhere. Phi = 0 by theorem for the WHOLE system.")
        print("         There is nothing for IIT to measure here, at any grain.")
        return False
    if len(rec) > 1:
        print("  KILL - %d competing recurrent sets. Exclusion is NOT forced: which one is" % len(rec))
        print("         THE complex becomes an empirical question you cannot afford to")
        print("         settle (super-exponential Phi over each candidate).")
        return False
    core = rec[0]
    fat = [(n, bundle.get(n, 1)) for n in core if bundle.get(n, 1) > 1]
    if fat:
        print("  KILL - the recurrent core contains COARSE nodes, so this graph is a")
        print("         drawing rather than a causal-element graph:")
        for n, k in fat:
            print("           %-12s bundles %s causal elements" % (n, "{:,}".format(k)))
        print("         IIT is a claim about causal ELEMENTS. An SCC over boxes that each")
        print("         hide millions of parameters says nothing about the system -- it is")
        print("         the grain problem, not a result. Either the core is built from real")
        print("         elements (neuromorphic: one unit = one causal element) or the fat")
        print("         node is pushed OUT of the core and made a pure sink.")
        return False
    if len(core) > budget:
        print("  KILL - the single core is %d units, over the %d-unit faithful-Phi budget." % (len(core), budget))
        print("         Exclusion is forced but Phi is not computable, so the claim is")
        print("         undecidable in practice - un-instrumented, not closed.")
        return False
    print("  ADMISSIBLE - exactly ONE recurrent core of %d units, everything else is" % len(core))
    print("               feedforward (Phi=0), so EXCLUSION forces this core to be THE")
    print("               complex. The affordable grain is the correct grain.")
    print("               NOT a consciousness claim - a screen may KILL, never GREEN.")
    return True


# --------------------------------------------------------------------------- #
# Candidate wirings. anima_today is drawn from what the code actually does, and is
# the reason this file exists: it does not pass.
# --------------------------------------------------------------------------- #
def anima_today():
    """Production as wired today (verified in code, not assumed).

    - trunk: causal conv, strictly feedforward (bytes -> logits)
    - field: pure_field_step advances three oscillators; --ag-feedback closes
      A<->G back into the oscillator amplitude target, so the field is recurrent
    - emit: the gate reads the field and its own emit_drive (a0: g = 1 - emit_drive)
    - store: written by emissions, read at decode -> a second loop through the mouth
    """
    nodes = ["bytes", "trunk", "logits", "mouth",
             "osc_fast", "osc_med", "osc_slow", "field_mix", "emit_drive", "gate",
             "store", "kosmos"]
    edges = {
        "bytes": ["trunk"], "trunk": ["logits"], "logits": ["mouth"],
        "mouth": ["store", "emit_drive"],
        "osc_fast": ["field_mix"], "osc_med": ["field_mix"], "osc_slow": ["field_mix"],
        "field_mix": ["emit_drive"],
        "emit_drive": ["gate"],
        "gate": ["osc_fast", "osc_med", "osc_slow", "mouth"],   # --ag-feedback return leg
        "store": ["kosmos", "mouth"], "kosmos": ["store"],
    }
    # the honest part: these boxes are NOT causal elements.
    bundle = {"trunk": 302_610_258, "mouth": 302_610_258, "logits": 256}
    return nodes, edges, bundle


def rcfs(n_core=6, n_slots=4):
    """RCFS - Recurrent Core, Feedforward Shell. The construction the divergence proposes.

    ONE recurrent core (oscillators + a few KOSMOS slots, core <= PHI_BUDGET); the 303M
    trunk is a pure SINK, so no feedforward unit lies on a closed path through the core.
    """
    core = ["core%d" % i for i in range(n_core)] + ["slot%d" % i for i in range(n_slots)]
    nodes = ["bytes", "trunk", "logits", "mouth"] + core
    edges = {"bytes": ["trunk"], "trunk": ["logits"], "logits": ["mouth"], "mouth": []}
    for i, c in enumerate(core):                      # core is a single cycle -> one SCC
        edges[c] = [core[(i + 1) % len(core)]]
    edges[core[0]] = edges[core[0]] + ["mouth"]       # core drives the mouth; mouth is a SINK
    edges["bytes"] = edges["bytes"] + [core[1]]       # sensing enters the core
    # RCFS keeps every fat box OUT of the core: the trunk/mouth are pure sinks, and each
    # core unit is one causal element (this is the requirement that forces a neuromorphic
    # substrate -- on a GPU the "unit" is a tensor slice, not a causal element).
    bundle = {"trunk": 302_610_258, "mouth": 302_610_258, "logits": 256}
    return nodes, edges, bundle


def main():
    print("phi-screen - IIT admissibility as a pure graph property ($0, no forward pass)")
    print("faithful-Phi budget: %d units\n" % PHI_BUDGET)
    ok_today = screen("anima TODAY (as wired)", *anima_today())
    print()
    ok_rcfs = screen("RCFS (recurrent core + feedforward shell)", *rcfs())
    print()
    print("=" * 78)
    if not ok_today and ok_rcfs:
        print("READING: anima as wired is NOT IIT-admissible, and the reason is structural,")
        print("not a matter of degree. RCFS is - which is what makes it worth building.")
        print("Neither line is a consciousness claim; this screen only kills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
