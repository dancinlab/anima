"""Cheap deterministic state/logic soak for the workspace (no model forward pass)."""

from __future__ import annotations

import time
import tracemalloc

try:
    from .cognitive_workspace import Fact
    from .workspace_mouth import certify_divergence, select_divergence
    from .workspace_semantic import realizer_adversarial_panel, realizer_heldout_panel
except ImportError:
    from cognitive_workspace import Fact
    from workspace_mouth import certify_divergence, select_divergence
    from workspace_semantic import realizer_adversarial_panel, realizer_heldout_panel


def run_workspace_longrun(ticks: int = 500) -> dict:
    if ticks not in (100, 500):
        raise ValueError("workspace long-run ticks must be 100 or 500")
    panel = realizer_heldout_panel() + realizer_adversarial_panel()
    failures = []
    rejected = shuffled_inert = off_inert = 0
    tracemalloc.start()
    started = time.perf_counter()
    try:
        for tick in range(ticks):
            name, seed = panel[tick % len(panel)]
            certificate = certify_divergence(seed)
            baseline = select_divergence(seed)
            first = certificate["hypotheses"][0]
            if tick % 3 == 0:
                evidence = (Fact(first.spec.claim_id, "has_verdict", "contradicted", ("soak",)),)
                decision = select_divergence(seed, evidence)
                ok = decision is not None and first.spec.claim_id in decision.rejected_claim_ids
                rejected += int(ok)
            elif tick % 3 == 1:
                evidence = (Fact(first.spec.claim_id + ":shuffle", "has_verdict", "contradicted", ("soak",)),)
                decision = select_divergence(seed, evidence)
                ok = decision is not None and decision.selected_claim_id == baseline.selected_claim_id
                shuffled_inert += int(ok)
            else:
                decision = baseline
                ok = decision is not None and not decision.rejected_claim_ids
                off_inert += int(ok)
            if not certificate["ok"] or not ok:
                failures.append({"tick": tick, "case": name})
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return {
        "schema": "anima.workspace-longrun/v1", "scope": "workspace logic/state; no 303M forward",
        "ticks": ticks, "ok": not failures, "failures": failures,
        "contradiction_rejections": rejected, "shuffle_inert": shuffled_inert,
        "off_inert": off_inert, "elapsed_seconds": elapsed, "peak_bytes": peak,
    }
