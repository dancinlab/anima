#!/usr/bin/env python3
"""metric-leak audit — the check that would have caught H_9673 BEFORE it ran. $0, no model.

WHAT H_9673 WAS
---------------
"the archived faction engine shaved the negative term of its own score every step -- Phi
was not a measurement but a readout of the sync knob." An update path was writing to a
quantity that the metric SUBTRACTS, so the score rose for free. It was caught by a source
audit after the fact. This file is the same catch made mechanical and run in advance.

THE CHECK
---------
Declare two things and let the graph do the rest:

  * a METRIC: which quantities it consumes, and in what role
        term      -- enters additively; writing it inflates the score directly
        subtract  -- enters negatively; SHRINKING it inflates the score (the H_9673 shape)
        normalize -- enters as a denominator; shrinking it inflates the score
  * every UPDATE path (a loss term, a scheduler, a hand-set knob): which quantities it writes

Then flag any quantity that is both written by an update and reached by the metric --
including TRANSITIVELY, through a declared dependency graph. Transitivity is the point:
a direct overlap is visible by eye, and H_9673's was not direct.

WHAT A FLAG MEANS
-----------------
Not "the number is wrong". It means the number is not a MEASUREMENT of the system -- the
system contains a path that moves it by construction, so it cannot discriminate. It is
the independence conjunct of the measurability criterion, checked symbolically.

A clean audit is not a licence either. It says only: nothing in the DECLARED graph writes
the metric. Undeclared paths are invisible to it, so the declaration is the load-bearing
part and belongs in review.
"""
import sys

ROLE_EFFECT = {
    "term": "writing it inflates the score directly",
    "subtract": "SHRINKING it inflates the score (the H_9673 shape)",
    "normalize": "shrinking it inflates the score (denominator)",
}


def reachable(seed, deps):
    """Everything the metric transitively consumes. deps[q] = quantities q is computed from."""
    seen, stack = set(), list(seed)
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        seen.add(q)
        stack.extend(deps.get(q, []))
    return seen


def audit(name, metric, updates, deps=None, verbose=True):
    """metric = {quantity: role} · updates = {update_name: [quantities written]}."""
    deps = deps or {}
    consumed = reachable(list(metric), deps)
    hits = []
    for upd, written in updates.items():
        for q in written:
            if q in consumed:
                # name the role of the metric-side quantity this write reaches
                if q in metric:
                    role, via = metric[q], None
                else:
                    role, via = None, q
                    for m, r in metric.items():
                        if q in reachable([m], deps):
                            role, via = r, m
                            break
                hits.append((upd, q, role, via))
    if verbose:
        print("=" * 78)
        print("%s" % name)
        print("  metric consumes (transitively): %d quantities" % len(consumed))
        print("  update paths declared: %d" % len(updates))
        if not hits:
            print("  CLEAN - no declared update writes anything the metric reads.")
            print("          (Only as strong as the declaration; undeclared paths are invisible.)")
        for upd, q, role, via in hits:
            direct = via is None or via == q
            print("  LEAK - update %-22s writes %-18s" % ("'" + upd + "'", q))
            print("         role: %-10s %s" % (role, ROLE_EFFECT.get(role, "?")))
            print("         path: %s" % ("DIRECT (metric reads it)" if direct
                                          else "TRANSITIVE (reaches the metric through '%s')" % via))
    return hits


def h9673():
    """H_9673 as it actually was: the sync knob feeds the term Phi subtracts.

    Phi rewards integration and is penalised by within-part independence. The engine had a
    sync update writing faction correlation every step, and correlation is what the
    penalty is computed FROM -- so the penalty shrank on its own and Phi rose for free.
    Note the leak is TRANSITIVE: nothing wrote 'phi_penalty' by name.
    """
    metric = {"integration": "term", "phi_penalty": "subtract"}
    deps = {"phi_penalty": ["within_part_independence"],
            "within_part_independence": ["faction_corr"],
            "integration": ["cross_part_mi"]}
    updates = {"faction_sync_step": ["faction_corr"],
               "ce_loss": ["trunk_weights"]}
    return "H_9673 (archived faction engine) - POSITIVE CONTROL, must FLAG", metric, updates, deps


def rcfs_clean():
    """RCFS as the divergence scopes it: Phi is MEASURED, never optimized."""
    metric = {"integration": "term", "phi_penalty": "subtract"}
    deps = {"phi_penalty": ["within_part_independence"],
            "within_part_independence": ["core_partition_mi"],
            "integration": ["core_joint_mi"]}
    updates = {"form_ce": ["trunk_weights"],
               "comp_head_ce": ["comp_head_weights"],
               "core_dynamics": ["core_state"]}     # state evolves; no metric input is written
    return "RCFS (Phi measured, never maximized) - NEGATIVE CONTROL, must be CLEAN", metric, updates, deps


def phi_optimized():
    """H_1518-style: adopt the Phi-maximising topology. Legal at design time -- but the
    audit should still SAY it, because the number stops discriminating architectures."""
    metric = {"integration": "term", "phi_penalty": "subtract"}
    deps = {"integration": ["adjacency"], "phi_penalty": ["adjacency"]}
    updates = {"topology_hill_climb": ["adjacency"]}
    return "Phi-optimized topology (H_1518 shape) - must FLAG (design-time, but still a write)", metric, updates, deps


def main():
    print("metric-leak audit - does the system contain a path that writes its own score?\n")
    results = []
    for fn, must_flag in ((h9673, True), (rcfs_clean, False), (phi_optimized, True)):
        name, metric, updates, deps = fn()
        hits = audit(name, metric, updates, deps)
        ok = bool(hits) == must_flag
        results.append((name, ok))
        print("  -> auditor %s (expected %s)\n" % ("OK" if ok else "WRONG",
                                                    "FLAG" if must_flag else "CLEAN"))
    print("=" * 78)
    bad = [n for n, ok in results if not ok]
    if bad:
        print("AUDITOR FAILED its own controls: %s" % "; ".join(bad))
        return 1
    print("auditor passed its own positive and negative controls (%d/%d)." % (len(results), len(results)))
    print("H_9673 is caught, and caught TRANSITIVELY - nothing wrote 'phi_penalty' by name,")
    print("which is exactly why a by-eye review missed it for as long as it did.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
