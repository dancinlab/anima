#!/usr/bin/env python3
"""
H_1378 agent-tool <-> mitosis teaching — $0 numpy MIRROR (DIRECTIONAL, engine-transfer UNVERIFIED).

Step B of the agent-tool/mitosis lane. Step A audit = REFERENCE-ONLY: the live agent-tool
layer (anima-agent-core/agent_tools.hexa) selects tools by a STATIC weighted dot-product over
hand-set affinity floats; tool failure updates only a scalar tension_delta log; engine_mitosis_tick
/ immune_memory_bind are NEVER called. This probe DESIGNS + direction-validates the missing
mechanism: a tool/skill is a CELL keyed by task-context; failure/abstain MITOSIS-SPLITS a
specialized skill-cell binding (task-context -> correct tool). SAME op teaches + infers (p8).

Geometry MIRRORS CORE/engine_cli.hexa:
  - immune_embed_key (L774): DETERMINISTIC byte-trigram FNV-1a key encoder, DIM=64
  - immune_memory_recall (L858): L2-affinity FIRE if recon-err <= recall_thr, else "" = ABSTAIN
  - clonal split: a new cell is grown (bind task->tool) on a failure/abstain (H_1227/H_1288)

CORE/*.hexa is UNTOUCHED. Frozen bars pre-registered in FREEZE.txt (NO tune-to-green, c9).
"""
import numpy as np, json, sys

DIM = 64
FNV_OFFSET = 0x811c9dc5
FNV_PRIME  = 0x01000193
MASK32     = 0xFFFFFFFF
RECALL_THR = 0.55          # abstain band on normalized L2 recon-err (cosine-distance proxy)

# ---- CORE-mirror: byte-trigram FNV-1a key encoder (immune_embed_key, DIM=64) ----
def _fnv1a(byts):
    h = FNV_OFFSET
    for b in byts:
        h = ((h ^ b) * FNV_PRIME) & MASK32
    return h

def embed_key(text):
    """DETERMINISTIC byte-trigram FNV-1a -> DIM=64 unit vector (mirror of immune_embed_key)."""
    bs = text.encode("utf-8")
    v = np.zeros(DIM, dtype=np.float64)
    if len(bs) < 3:
        bs = bs + b"\x00" * (3 - len(bs))
    for i in range(len(bs) - 2):
        tri = bs[i:i+3]
        h = _fnv1a(tri)
        v[h % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

def recon_err(key, cell_keys):
    """nearest-cell L2 recon-err on UNIT keys -> in [0,2]; <= RECALL_THR ⇒ FIRE else ABSTAIN."""
    if len(cell_keys) == 0:
        return 2.0, -1
    d = np.linalg.norm(cell_keys - key[None, :], axis=1)
    i = int(np.argmin(d))
    return float(d[i]), i

# ---- skill cell-store (mirror of ImmuneMemoryGrow: bind task->tool, recall-or-abstain) ----
class SkillStore:
    def __init__(self):
        self.keys = np.zeros((0, DIM))
        self.tools = []           # bound tool per cell (the "value")
    def bind(self, task, tool):   # clonal split: grow a new specialized skill-cell
        k = embed_key(task)
        self.keys = np.vstack([self.keys, k[None, :]])
        self.tools.append(tool)
    def recall(self, task):       # L2-affinity FIRE, else None = ABSTAIN (no fabricated tool)
        k = embed_key(task)
        err, i = recon_err(k, self.keys)
        if err <= RECALL_THR:
            return self.tools[i], err
        return None, err          # ABSTAIN

# ---- synthetic task->tool environment ----
TOOLS = ["web_search", "code_execute", "file_read", "memory_search", "shell_execute", "phi_measure"]
def make_tasks(rng, n_per_tool=6):
    """Each task is a context string; ground-truth tool = task's tool family."""
    tasks = []
    for t in TOOLS:
        for j in range(n_per_tool):
            # context phrasing varies but stays in-family (shared trigram neighborhood)
            tasks.append((f"{t} request variant {j} ctx{rng.integers(0,3)}", t))
    rng.shuffle(tasks)
    return tasks

def run_arm(rng, mode):
    """mode in {full, static, shuffle}. Returns (acc_initial, acc_final).

    SHUFFLE control: the store is TRAINED on a permuted task->tool label map (the
    task<->tool correspondence is destroyed) BUT it is always SCORED against the TRUE
    map (gt_true). A store taught the wrong bindings recalls the wrong tool -> the
    learning gain collapses to the no-split floor. This is the earned-structure control:
    only a store whose splits encode the REAL task->tool correspondence improves.
    """
    store = SkillStore()
    tasks = make_tasks(rng)
    gt_true  = {task: tool for task, tool in tasks}     # the TRUE map — always scored here
    gt_train = dict(gt_true)
    if mode == "shuffle":
        perm = list(gt_true.values()); rng.shuffle(perm) # permute labels USED FOR TRAINING only
        gt_train = {task: perm[i] for i, (task, _) in enumerate(tasks)}

    # seed BOTH arms with the same single initial cell (so static starts identically)
    t0, _ = tasks[0]
    store.bind(t0, gt_train[t0])

    def measure():
        correct = 0
        for task, _ in tasks:
            pred, _ = store.recall(task)
            if pred == gt_true[task]:        # scored vs the TRUE map (not the training labels)
                correct += 1
        return correct / len(tasks)

    acc_initial = measure()

    # failure-driven session: walk tasks; on miss/abstain, the FULL/SHUFFLE arm SPLITS
    # a new skill-cell (mitosis teaching) binding to its TRAINING label. STATIC never splits.
    for task, _ in tasks:
        pred, _ = store.recall(task)
        failed = (pred != gt_train[task])    # selected tool != the label the arm is trained toward
        if failed and mode in ("full", "shuffle"):
            store.bind(task, gt_train[task]) # MITOSIS-SPLIT: bind task-context -> (true|permuted) tool

    acc_final = measure()
    return acc_initial, acc_final

def abstain_rate(rng):
    """NO-FAB bar: FULL store, then query UNTRAINED far tasks (disjoint trigram space)."""
    store = SkillStore()
    tasks = make_tasks(rng)
    gt = {task: tool for task, tool in tasks}
    store.bind(tasks[0][0], gt[tasks[0][0]])
    for task, _ in tasks:                   # train FULL store
        pred, _ = store.recall(task)
        if pred != gt[task]:
            store.bind(task, gt[task])
    far = [f"zzz unrelated alien glyph {chr(0x4e00+rng.integers(0,3000))} far{j}" for j in range(40)]
    abst = sum(1 for q in far if store.recall(q)[0] is None)
    return abst / len(far)

def main():
    seeds = [1378, 1379, 1380]
    rows = {"full_i": [], "full_f": [], "static_f": [], "shuffle_f": [], "abstain": []}
    per_seed = []
    for s in seeds:
        rng = np.random.default_rng(s)
        fi, ff = run_arm(np.random.default_rng(s), "full")
        _, sf  = run_arm(np.random.default_rng(s), "static")
        _, hf  = run_arm(np.random.default_rng(s), "shuffle")
        ab     = abstain_rate(np.random.default_rng(s))
        rows["full_i"].append(fi); rows["full_f"].append(ff)
        rows["static_f"].append(sf); rows["shuffle_f"].append(hf); rows["abstain"].append(ab)
        per_seed.append(dict(seed=s, full_i=fi, full_f=ff, static_f=sf, shuffle_f=hf, abstain=ab))

    m = {k: float(np.mean(v)) for k, v in rows.items()}
    learn_lift = m["full_f"] - m["full_i"]
    distinct   = m["full_f"] - m["static_f"]
    earned_gap = m["shuffle_f"] - m["static_f"]

    bar1 = learn_lift >= 0.30
    bar2 = distinct   >= 0.30
    bar3 = earned_gap <= 0.15
    bar4 = m["abstain"] >= 0.90
    green = bar1 and bar2 and bar3 and bar4

    print("H_1378 agent-tool <-> mitosis teaching — numpy MIRROR (DIRECTIONAL)")
    print("seeds:", seeds)
    for r in per_seed:
        print(f"  seed {r['seed']}: full {r['full_i']:.3f}->{r['full_f']:.3f}  "
              f"static {r['static_f']:.3f}  shuffle {r['shuffle_f']:.3f}  abstain {r['abstain']:.3f}")
    print("POOLED means:")
    print(f"  FULL init={m['full_i']:.3f} final={m['full_f']:.3f}  STATIC final={m['static_f']:.3f}  "
          f"SHUFFLE final={m['shuffle_f']:.3f}  ABSTAIN={m['abstain']:.3f}")
    print("FROZEN BARS:")
    print(f"  (1) LEARNS              full_f-full_i = {learn_lift:+.3f} >= +0.30  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  (2) DISTINCT-FROM-STATIC full_f-static_f = {distinct:+.3f} >= +0.30 -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  (3) EARNED (shuffle)    shuffle_f-static_f = {earned_gap:+.3f} <= +0.15 -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  (4) NO-FAB / ABSTAIN    abstain = {m['abstain']:.3f} >= 0.90 -> {'PASS' if bar4 else 'FAIL'}")
    print("VERDICT:", "GREEN" if green else "RED/PARTIAL")
    print(json.dumps(dict(seeds=seeds, pooled=m, bars=dict(learns=bar1, distinct=bar2,
          earned=bar3, no_fab=bar4), verdict="GREEN" if green else "RED/PARTIAL"), indent=2))
    return 0 if green else 1

if __name__ == "__main__":
    sys.exit(main())
