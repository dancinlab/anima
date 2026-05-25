#!/usr/bin/env python3
"""§30 — Lateral L1 cumulative ckpt lineage — STRUCTURAL SKETCH (DESIGN-TIER).

RUNTIME-GUARDED: this file is a reference structure, NOT an executable
trainer. Running it directly exits 0 with an explanatory message. It is
importable so the closed-form battery (blue_falsifier_lineage.py) and any
future reviewer can reference the structural API without executing a fire.

L1 mechanism (DESIGN_L1.md §2): anima ckpt N inherits ckpt N-1's weights as
init, building a generation lineage DAG that roots at a gen=0 RANDOM-init
anima node. The MITOSIS cell-pool is merged across cycle-versions.

VERDICT (DESIGN_L1.md §7): path (b) DESIGN-CLOSE — governance-blocked
(contradicts g_clm_from_scratch's letter; no design self-grants exceptions)
AND premature (anima has no non-saturated ckpt; a lineage today is a lineage
of the byte-cascade defect, not of memory — §16.6-C / B-ATTRACTOR evidence).

NO fire, NO GPU, NO ckpt training. $0 design-tier.
"""
import sys

# ── MITOSIS cell-pool bounds (mirror B-MITOSIS-5 verification spec) ──────
CELL_MIN = 2          # CB1 invariant
CELL_MAX = 64         # .clm v1 P2 spec (lib max_cells=128; battery uses 64)

# parent_source enum — the governance-distinguishing partition (B-LINEAGE-2)
SOURCE_SELF = "anima_self"     # parent ckpt is an anima-own lineage node
SOURCE_EXTERNAL = "external"   # foundation model / non-anima ckpt — FORBIDDEN
PARENT_SOURCE_ENUM = (SOURCE_SELF, SOURCE_EXTERNAL)


# ── ckpt lineage node ───────────────────────────────────────────────────
class LineageCkpt:
    """A node in anima's ckpt lineage DAG.

    gen=0  : true from-scratch RANDOM-init anima ckpt (current g_clm regime).
    gen=N  : init_weights loaded from a gen=(N-1) anima-self parent.
    """

    def __init__(self, ckpt_id, gen, parent=None, parent_source=None,
                 cell_count=CELL_MIN):
        self.ckpt_id = ckpt_id
        self.gen = int(gen)
        self.parent = parent                    # LineageCkpt | None
        self.parent_source = parent_source      # SOURCE_* | None at gen 0
        self.cell_count = int(cell_count)
        # gen-0 reduction invariant (B-LINEAGE-4): a gen-0 node has no parent
        # and init_weights = RANDOM seed-fixed — byte-equal to g_clm_from_scratch.
        if self.gen == 0:
            assert self.parent is None and self.parent_source is None, \
                "gen-0 must be parentless RANDOM-init (g_clm_from_scratch)"
        else:
            assert self.parent is not None and self.parent_source is not None


def make_root(ckpt_id="anima_gen0", cell_count=CELL_MIN):
    """gen=0 from-scratch RANDOM-init ckpt — the current regime (B-LINEAGE-4)."""
    return LineageCkpt(ckpt_id, gen=0, cell_count=cell_count)


def inherit(parent, child_id, parent_source, child_cell_count=0):
    """ckpt N -> ckpt (N+1) inheritance edge (B-LINEAGE-1 monotone depth).

    parent_source MUST be SOURCE_SELF for an admissible anima lineage
    (B-LINEAGE-2). An external parent is the contamination g_clm_from_scratch
    guards against — rejected here structurally.
    """
    if parent_source not in PARENT_SOURCE_ENUM:
        raise ValueError(f"parent_source must be in {PARENT_SOURCE_ENUM}")
    child_gen = parent.gen + 1                          # B-LINEAGE-1: +1
    merged = clamp_cells(parent.cell_count + child_cell_count)  # B-LINEAGE-3
    return LineageCkpt(child_id, gen=child_gen, parent=parent,
                       parent_source=parent_source, cell_count=merged)


def clamp_cells(n):
    """Generational cell-pool merge cardinality clamp (B-LINEAGE-3).

    clamp(x, MIN, MAX) = min(MAX, max(MIN, x)) — mirrors mitosis_hook_lib.
    """
    return min(CELL_MAX, max(CELL_MIN, int(n)))


# ── governance-distinguishing predicate (B-LINEAGE-2) ───────────────────
def root_is_gen0_random(ckpt):
    """Walk parent pointers — True iff the chain roots at a gen=0 node."""
    node = ckpt
    while node.parent is not None:
        node = node.parent
    return node.gen == 0


def lineage_is_anima_self(ckpt):
    """admissible(lineage) := every ancestor edge is anima_self AND the
    chain roots at a gen=0 RANDOM-init anima node.

    This is the THE governance invariant: it cleanly separates anima-self
    lineage (permitted under DESIGN_L1.md §3 Reading A) from external-
    precursor inheritance (the contamination g_clm_from_scratch forbids).
    A clean PASS here is necessary — NOT sufficient (DESIGN_L1.md §4/§6:
    a clean self-ckpt may still be memorization-saturated => lineage of
    defects).
    """
    node = ckpt
    while node.parent is not None:
        if node.parent_source != SOURCE_SELF:
            return False
        node = node.parent
    return root_is_gen0_random(ckpt)


# ── gen-0 reduction (B-LINEAGE-4 connection-point) ──────────────────────
def is_current_from_scratch_regime(ckpt):
    """L1 at gen=0 IS the current g_clm_from_scratch regime, byte-equal:
    parentless, RANDOM seed-fixed init, no inheritance. The current regime
    is exactly the gen=0 slice of L1's design space (DESIGN_L1.md §7 C3#6).
    """
    return ckpt.gen == 0 and ckpt.parent is None


# ── runtime guard — design-tier, NOT a trainer ──────────────────────────
if __name__ == "__main__":
    print(__doc__)
    print("\n[design-tier guard] lineage_sketch.py is a STRUCTURAL SKETCH — "
          "no fire, no GPU, no training. See DESIGN_L1.md §6/§7: L1 is "
          "design-closed (governance-blocked + premature). Importable for "
          "reference only.")
    sys.exit(0)
