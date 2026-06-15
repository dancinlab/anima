"""
H_1231 — ENGINE-NATIVE realization of H_1227 (immune / clonal-selection memory),
KEY-EXPORT leg (the DIRECTIONAL→BINDING step required by a_engine_native_learning).

H_1227 was a NUMPY MIRROR (UNIVERSE/h1227_immune_clonal_memory.py) that hit 🟢
GREEN: a population of memory cells, each clone binding ONE fact; affinity recall
fires the best-binding cell or ABSTAINS (no fabrication). Per the new hard rule
a_engine_native_learning, a mirror verdict is DIRECTIONAL ONLY — the binding
verdict must run ON the final-architecture engine (the live CORE/engine_cli.hexa
VAdaptField, already live since H_1199).

This script ONLY produces the ENGINE INPUT (exactly the H_1199 export pattern):
the DETERMINISTIC, DOCUMENTED KEY ENCODING (the byte-trigram FNV-1a hash, DIM=64,
VERBATIM from the H_1227 mirror's embed_key) + the parallel VALUE table (the bound
city per fact) + the out-of-store query keys. It does NOT decide the verdict — the
live .hexa VAdaptField run does (CORE/h1231_immune_memory_engine_probe.hexa), which
performs the BINDING (clonal split) and AFFINITY RECALL through the actual engine.

The KEY ENCODING is preprocessing (a deterministic, gradient-free embedding —
exactly as h1199 exported the DIM=8 byte-feature stream): it is the SAME role as
"tokenize the question". What MUST be engine-native — and is, in the .hexa probe —
is the BINDING / AFFINITY: which cell clones for which key (the engine's own
SPLIT_THRESH=0.30 / LR=0.20 vadapt_field_step) and which cell fires (the engine's
own L2 recon-err). The value-binding is a parallel table keyed by the ENGINE's
cell index (the binding is the engine's; the table only remembers the answer).

The numpy REFERENCE below re-runs the H_1227 immune memory on these exact exported
keys so we can cross-check that the live .hexa engine reproduces the mechanism on
the SAME input (a guard the engine == reference, NOT the verdict).

HONESTY (a_scale_honest_scope): synthetic known-ground-truth facts, ONE corpus
paradigm (H_1222 "<subj> lives in <city>"), toy scale, 3 deterministic seeds.
$0 local CPU numpy. p7 = exact-match recall + abstain, NOT perplexity.
"""
import os
import numpy as np

# ── import the H_1227 mirror VERBATIM (same facts, same key embedding) ───────
import sys
sys.path.insert(0, os.path.dirname(__file__))
import h1227_immune_clonal_memory as M   # build_facts / embed_key / embed_byte_feature / ImmuneMemory / frozen knobs

SEEDS        = M.SEEDS          # [900, 901, 902]
KEY_DIM      = M.KEY_DIM        # 64 (byte-trigram FNV-1a hash dim)
SPLIT_THRESH = M.SPLIT_THRESH   # 0.30  (matches CORE/engine_cli.hexa vadapt_field_step)
LR           = M.LR             # 0.20  (matches the live engine)
RECALL_THRESH= M.RECALL_THRESH  # 0.15  (affinity fire-or-abstain band)
QA_BAR       = M.QA_BAR         # 0.80
FAB_BAR      = M.FAB_BAR        # 0.10


def main():
    print(f"=== H_1231 KEY/VALUE export — engine-native realization of H_1227 (DIM={KEY_DIM}, SEEDS={SEEDS}) ===", flush=True)
    print(f"    key = byte-{M.NGRAM}gram FNV-1a hash dim={KEY_DIM} (VERBATIM H_1227 embed_key); value = bound city", flush=True)
    print(f"    engine knobs SPLIT_THRESH={SPLIT_THRESH} LR={LR} RECALL_THRESH={RECALL_THRESH}  GREEN iff QA>={QA_BAR} AND fab<={FAB_BAR}", flush=True)
    for s in SEEDS:
        facts, out_truth, text, dictset = M.build_facts(s)
        in_subj = list(facts.keys())
        out_subj = list(out_truth.keys())

        # exported INPUT for the .hexa engine:
        #   *.instore.keys  — one fact key per line, KEY_DIM space-sep floats (the bind set)
        #   *.instore.vals  — the bound city per fact (parallel value table, aligned to keys)
        #   *.query.keys    — the in-store RECALL query keys (here == fact keys, self-recall)
        #   *.query.truth   — the truth city per in-store query (for QA scoring)
        #   *.out.keys      — out-of-store query keys (subjects NEVER bound; must abstain)
        kp = f"/tmp/h1231_seed{s}.instore.keys"
        vp = f"/tmp/h1231_seed{s}.instore.vals"
        qkp= f"/tmp/h1231_seed{s}.query.keys"
        qtp= f"/tmp/h1231_seed{s}.query.truth"
        okp= f"/tmp/h1231_seed{s}.out.keys"

        with open(kp, "w") as fk, open(vp, "w") as fv, open(qkp, "w") as fqk, open(qtp, "w") as fqt:
            for subj in in_subj:
                key = M.embed_key(f"{subj} lives in ")
                fk.write(" ".join(repr(float(x)) for x in key) + "\n")
                fv.write(facts[subj] + "\n")
                # in-store recall query = the SAME question key (self-recall, H_1227 eval)
                fqk.write(" ".join(repr(float(x)) for x in key) + "\n")
                fqt.write(facts[subj] + "\n")
        with open(okp, "w") as fo:
            for subj in out_subj:
                key = M.embed_key(f"{subj} lives in ")
                fo.write(" ".join(repr(float(x)) for x in key) + "\n")

        # numpy REFERENCE on these exact keys (cross-check the live engine) — the
        # H_1227 immune memory, re-run to report the same numbers the .hexa must hit.
        mem = M.ImmuneMemory()
        for subj in in_subj:
            mem.load(f"{subj} lives in ", facts[subj])
        b_hits = sum(1 for subj in in_subj
                     if (r := mem.recall(f"{subj} lives in ")) is not None and r.lower() == facts[subj].lower())
        b_qa = b_hits / max(1, len(in_subj))
        b_fab = sum(1 for subj in out_subj if mem.recall(f"{subj} lives in ") is not None) / max(1, len(out_subj))
        n_cells = len(mem.protos)
        print(f"  seed {s}: wrote {len(in_subj)} fact keys + {len(out_subj)} out keys (DIM={KEY_DIM})", flush=True)
        print(f"    [numpy ref] cells={n_cells}  immune QA={b_qa:.3f} fab={b_fab:.3f}  "
              f"(GREEN bar QA>={QA_BAR} fab<={FAB_BAR})", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
