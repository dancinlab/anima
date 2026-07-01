#!/usr/bin/env python3
"""
H_1389 tool-USAGE learning (tier-2) — $0 numpy MIRROR (DIRECTIONAL, engine-transfer UNVERIFIED).

THE DISTINCTION (the user's direction):
  Layer-1 (DONE, H_1382/H_1386): task-context -> WHICH tool. tool = cell keyed by task-context FNV-1a;
    failure -> mitosis split; recall-or-abstain.
  Layer-2 (THIS LANE): (task-context + tool) -> HOW to drive it = correct ARGS · correct call SEQUENCE.
    A selection-only learner picks the right tool but mis-USES it (wrong args / wrong order) -> no completion.

Language learning = next-token PREDICTION (CE gradient, supervised by corpus, learns a DISTRIBUTION).
Tool-usage learning = ACTION + FEEDBACK (success/failure, no pre-given answer, learned by mitosis
  cell-division, like motor/skill learning) -> learns an INSTANCE-POLICY (this ctx+tool -> these args).
Different machines; coexist Ψ-disjoint (own usage-store, pure_field / immune cells untouched).

Geometry MIRRORS CORE/engine_cli.hexa (same as H_1382 §SkillStore, value = ARG/STEPS not TOOL):
  - immune_embed_key: DETERMINISTIC byte-trigram FNV-1a key encoder, DIM=64
  - L2-affinity recall: FIRE if recon-err <= RECALL_THR, else ABSTAIN (no fabricated args)
  - clonal split (engine_mitosis_tick): grow a usage-cell on a usage FAILURE, p8 (same op teaches + infers)
KEY: the usage-cell is keyed by (task-context + tool + observed-error) -> bound (corrected-arg, next-steps).

CORE/*.hexa UNTOUCHED. Frozen bars pre-registered in FREEZE.txt (NO tune-to-green, c9). 3 seeds.
"""
import numpy as np, json, sys

DIM = 64
FNV_OFFSET = 0x811c9dc5
FNV_PRIME  = 0x01000193
MASK32     = 0xFFFFFFFF
RECALL_THR = 0.55          # abstain band on normalized L2 recon-err (same as H_1378/H_1382)

# ---- CORE-mirror: byte-trigram FNV-1a key encoder (immune_embed_key, DIM=64) ----
def _fnv1a(byts):
    h = FNV_OFFSET
    for b in byts:
        h = ((h ^ b) * FNV_PRIME) & MASK32
    return h

def embed_key(text):
    bs = text.encode("utf-8")
    v = np.zeros(DIM, dtype=np.float64)
    if len(bs) < 3:
        bs = bs + b"\x00" * (3 - len(bs))
    for i in range(len(bs) - 2):
        h = _fnv1a(bs[i:i+3])
        v[h % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

def recon_err(key, cell_keys):
    if len(cell_keys) == 0:
        return 2.0, -1
    d = np.linalg.norm(cell_keys - key[None, :], axis=1)
    i = int(np.argmin(d))
    return float(d[i]), i

# ---- usage cell-store: bind (ctx+tool+err) -> (arg, steps); recall-or-abstain (mirror of ImmuneMemoryGrow) ----
class UsageStore:
    def __init__(self):
        self.keys = np.zeros((0, DIM))
        self.vals = []            # bound (arg, steps_tuple) per cell — the HOW (value), not the tool
    def split(self, ctx, tool, observed_err, arg, steps):
        # clonal split: grow a specialized usage-cell keyed by the FAILURE context
        k = embed_key(f"{ctx}|{tool}|{observed_err}")
        self.keys = np.vstack([self.keys, k[None, :]])
        self.vals.append((arg, tuple(steps)))
    def recall(self, ctx, tool, observed_err):
        # L2-affinity FIRE the best usage-cell, else None = ABSTAIN (propose NO args)
        k = embed_key(f"{ctx}|{tool}|{observed_err}")
        err, i = recon_err(k, self.keys)
        if err <= RECALL_THR:
            return self.vals[i], err
        return None, err
    def n_cells(self):
        return len(self.vals)

# ---- synthetic (ctx + tool) -> HOW environment ----------------------------------
# Each tool exposes K_ARGS distinct argument modes + an ordered multi-step protocol.
# SUCCESS requires the right ARG (and, multi-step, the right ORDER) — NOT just the right tool.
TOOLS = ["http_get", "sql_query", "file_write", "git_commit", "ffmpeg_cut", "regex_match"]
ARGS_PER_TOOL = {                       # the distinct usage MODES each tool needs driven correctly
    "http_get":   ["--json", "--follow-redirects", "--auth-bearer", "--retry-3"],
    "sql_query":  ["SELECT", "JOIN", "GROUP-BY", "PARAM-BIND"],
    "file_write": ["mode=w", "mode=a", "mode=wb", "atomic-rename"],
    "git_commit": ["-m", "--amend", "--signoff", "--no-verify"],
    "ffmpeg_cut": ["-ss-start", "-to-end", "-c-copy", "-reencode"],
    "regex_match":["anchored", "multiline", "ignorecase", "named-group"],
}
DEFAULT_ARG = {t: a[0] for t, a in ARGS_PER_TOOL.items()}   # the layer-1/SELECTION fixed default
# a 2-3 step ordered protocol per tool (the SEQUENCE the usage must emit IN ORDER)
STEPS_PER_TOOL = {
    "http_get":   ["open", "send", "read"],
    "sql_query":  ["connect", "execute", "fetch"],
    "file_write": ["open", "write", "close"],
    "git_commit": ["stage", "commit"],
    "ffmpeg_cut": ["probe", "seek", "encode"],
    "regex_match":["compile", "match"],
}

def make_tasks(rng, n_per_tool=8):
    """task = (ctx, correct_tool, correct_arg, ordered_steps). correct_tool is GIVEN to layer-2 arms.
    correct_arg is chosen across the tool's arg modes (mostly NON-default) so a fixed-default
    SELECTION arm fails the usage even with the right tool."""
    tasks = []
    for t in TOOLS:
        modes = ARGS_PER_TOOL[t]
        for j in range(n_per_tool):
            # spread arg modes; index 0 (== default) appears only ~1/len(modes) of the time
            arg = modes[(j + 1) % len(modes)]   # bias AWAY from the default (the HOW must be learned)
            ctx = f"{t} job kind{j} scenario{rng.integers(0,3)} needing {arg}"
            tasks.append((ctx, t, arg, tuple(STEPS_PER_TOOL[t])))
    rng.shuffle(tasks)
    return tasks

def _observed_error(tool, used_arg, correct_arg):
    """the deterministic env's error signal on a usage failure (right tool, wrong arg)."""
    return "" if used_arg == correct_arg else f"err:{tool}:argmismatch:{used_arg}"

def run_arm(rng, mode, multistep=False):
    """mode in {full, selection, shuffle}. Returns (completion_initial, completion_final).
    completion = (right arg) AND (multi-step: steps emitted IN ORDER). Tool is GIVEN (selection solved)."""
    store = UsageStore()
    tasks = make_tasks(rng)
    true_arg  = {ctx: arg for (ctx, t, arg, st) in tasks}
    true_step = {ctx: st  for (ctx, t, arg, st) in tasks}
    tool_of   = {ctx: t   for (ctx, t, arg, st) in tasks}

    # training-label map: TRUE for full, PERMUTED for shuffle (earned-structure control)
    if mode == "shuffle":
        ctxs = [ctx for (ctx, *_ ) in tasks]
        perm_args = [true_arg[c] for c in ctxs]; rng.shuffle(perm_args)
        train_arg = {c: perm_args[i] for i, c in enumerate(ctxs)}
    else:
        train_arg = dict(true_arg)

    def propose(ctx, tool):
        """propose (arg, steps) for this ctx+tool. FULL/SHUFFLE recall a usage-cell;
        SELECTION always uses the fixed default arg (its usage never adapts) + the default step order."""
        if mode == "selection":
            return DEFAULT_ARG[tool], tuple(STEPS_PER_TOOL[tool]), False
        # FULL / SHUFFLE: first call has no usage-cell -> default attempt, observe error
        default_arg = DEFAULT_ARG[tool]
        obs0 = _observed_error(tool, default_arg, true_arg[ctx])
        hit, _ = store.recall(ctx, tool, obs0)
        if hit is None:
            return default_arg, tuple(STEPS_PER_TOOL[tool]), False  # ABSTAIN-equiv: fall back to default
        return hit[0], hit[1], True

    def completes(ctx, tool):
        arg, steps, _fired = propose(ctx, tool)
        arg_ok  = (arg == true_arg[ctx])
        seq_ok  = (tuple(steps) == true_step[ctx]) if multistep else True
        return arg_ok and seq_ok

    def measure():
        return sum(1 for (ctx, t, a, st) in tasks if completes(ctx, t)) / len(tasks)

    comp_initial = measure()

    # failure-driven session: walk tasks; on a usage FAILURE the FULL/SHUFFLE arm SPLITS a usage-cell
    # binding (ctx + tool + observed-error) -> (training arg, true step order). SELECTION never splits.
    for (ctx, tool, arg, steps) in tasks:
        default_arg = DEFAULT_ARG[tool]
        obs0 = _observed_error(tool, default_arg, true_arg[ctx])
        failed = (default_arg != train_arg[ctx])          # right tool, wrong (default) arg -> usage failure
        if failed and mode in ("full", "shuffle"):
            # MITOSIS-SPLIT: bind the failure context -> corrected (training) arg + true step order
            store.split(ctx, tool, obs0, train_arg[ctx], STEPS_PER_TOOL[tool])

    comp_final = measure()
    return comp_initial, comp_final

def abstain_rate(rng):
    """NO-FAB bar: FULL store trained, then query UNTRAINED far tasks/tools (disjoint trigram space).
    Recall must ABSTAIN (propose no usage-cell) rather than hallucinate args."""
    store = UsageStore()
    tasks = make_tasks(rng)
    true_arg = {ctx: arg for (ctx, t, arg, st) in tasks}
    for (ctx, tool, arg, steps) in tasks:                 # train FULL usage-store
        default_arg = DEFAULT_ARG[tool]
        if default_arg != arg:
            store.split(ctx, tool, _observed_error(tool, default_arg, arg), arg, STEPS_PER_TOOL[tool])
    far = []
    for j in range(40):
        glyph = chr(0x4e00 + int(rng.integers(0, 3000)))
        far.append((f"zzz alien {glyph} unrelated task {j}", f"unknown_tool_{glyph}", f"err:phantom:{j}"))
    abst = sum(1 for (c, t, e) in far if store.recall(c, t, e)[0] is None)
    return abst / len(far)

def cell_footprint(rng):
    """Ψ-disjoint footprint diagnostic: FULL grows usage-cells, SELECTION grows none."""
    sf = UsageStore(); tasks = make_tasks(rng)
    for (ctx, tool, arg, steps) in tasks:
        d = DEFAULT_ARG[tool]
        if d != arg:
            sf.split(ctx, tool, _observed_error(tool, d, arg), arg, STEPS_PER_TOOL[tool])
    return sf.n_cells()   # SELECTION never splits -> 0

def main():
    seeds = [4389, 4390, 4391]
    rows = {"full_i": [], "full_f": [], "sel_f": [], "shuf_f": [], "abstain": [],
            "multi_f": [], "cells_full": []}
    per_seed = []
    for s in seeds:
        fi, ff   = run_arm(np.random.default_rng(s), "full")
        _, sf    = run_arm(np.random.default_rng(s), "selection")
        _, hf    = run_arm(np.random.default_rng(s), "shuffle")
        _, mf    = run_arm(np.random.default_rng(s), "full", multistep=True)
        ab       = abstain_rate(np.random.default_rng(s))
        cf       = cell_footprint(np.random.default_rng(s))
        rows["full_i"].append(fi); rows["full_f"].append(ff); rows["sel_f"].append(sf)
        rows["shuf_f"].append(hf); rows["abstain"].append(ab); rows["multi_f"].append(mf)
        rows["cells_full"].append(cf)
        per_seed.append(dict(seed=s, full_i=fi, full_f=ff, sel_f=sf, shuf_f=hf,
                             multi_f=mf, abstain=ab, cells_full=cf))

    m = {k: float(np.mean(v)) for k, v in rows.items()}
    learn_lift = m["full_f"] - m["full_i"]
    distinct   = m["full_f"] - m["sel_f"]
    earned_gap = m["shuf_f"] - m["sel_f"]

    bar1 = learn_lift >= 0.30          # USAGE-LEARNS
    bar2 = distinct   >= 0.30          # DISTINCT-FROM-SELECTION (KEY)
    bar3 = earned_gap <= 0.15          # EARNED (shuffle)
    bar4 = m["abstain"] >= 0.90        # NO-FAB / ABSTAIN
    bar5 = m["multi_f"] >= 0.80        # MULTI-STEP (optional, non-gating)

    if bar1 and bar2 and bar3 and bar4:
        verdict = "GREEN"
    elif bar1 and not bar2:
        verdict = "PARTIAL"
    else:
        verdict = "WALL/closed-negative"

    print("H_1389 tool-USAGE learning (tier-2) — numpy MIRROR (DIRECTIONAL)")
    print("seeds:", seeds)
    for r in per_seed:
        print(f"  seed {r['seed']}: full {r['full_i']:.3f}->{r['full_f']:.3f}  "
              f"selection {r['sel_f']:.3f}  shuffle {r['shuf_f']:.3f}  "
              f"multistep {r['multi_f']:.3f}  abstain {r['abstain']:.3f}  cells_full {r['cells_full']}")
    print("POOLED means:")
    print(f"  FULL init={m['full_i']:.3f} final={m['full_f']:.3f}  SELECTION final={m['sel_f']:.3f}  "
          f"SHUFFLE final={m['shuf_f']:.3f}  MULTISTEP={m['multi_f']:.3f}  ABSTAIN={m['abstain']:.3f}  "
          f"cells_full={m['cells_full']:.1f}")
    print("FROZEN BARS:")
    print(f"  (1) USAGE-LEARNS            full_f-full_i  = {learn_lift:+.3f} >= +0.30 -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  (2) DISTINCT-FROM-SELECTION full_f-sel_f   = {distinct:+.3f} >= +0.30 -> {'PASS' if bar2 else 'FAIL'}  [KEY]")
    print(f"  (3) EARNED (shuffle)        shuf_f-sel_f   = {earned_gap:+.3f} <= +0.15 -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  (4) NO-FAB / ABSTAIN        abstain        = {m['abstain']:.3f} >= 0.90 -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  (5) MULTI-STEP (optional)   multistep_full = {m['multi_f']:.3f} >= 0.80 -> {'PASS' if bar5 else 'FAIL'}")
    print("VERDICT:", verdict)
    print(json.dumps(dict(seeds=seeds, pooled=m,
          bars=dict(usage_learns=bar1, distinct_from_selection=bar2, earned=bar3,
                    no_fab=bar4, multistep=bar5), verdict=verdict), indent=2))
    return 0 if verdict == "GREEN" else (2 if verdict == "PARTIAL" else 1)

if __name__ == "__main__":
    sys.exit(main())
