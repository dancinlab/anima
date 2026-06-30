#!/usr/bin/env python3
"""h1557_oi_probe.py — engine-native OI-subspace / Binding-ID probe ORCHESTRATOR + SCORER.

a_engine_native_learning HARD-GATE: this file does ONLY torch-free / numpy-free arithmetic
(mean-difference, power-iteration PCA, cosine, bind-flip counting) over activations and patched
logits DUMPED BY THE LIVE ENGINE (core/bytegpt_decode.hexa via h1557_oi_engine_driver.hexa). It
NEVER touches the 303M weights itself — every Z_E/Z_A and every patched forward comes from the
engine. (grep'd by enforce gate: NO `import torch`, NO `import numpy`.)

Two-phase protocol (single resident model load per phase via the .hexa driver):
  PHASE 1 (dump): build controlled K=2 multi-bind prompts from the FROZEN h1305 vocab, emit D-jobs
                  (dump residual rows at the entity/attribute windows, mid-late layer sweep), run the
                  engine driver, parse Z_E(k,c)/Z_A(k,c).
  COMPUTE       : ΔE(k)=mean_c[Z_E(k,c)−Z_E(0,c)], ΔA(k) (identity cancels); PCA top-2 var ratio (B1);
                  cosine(ΔE,ΔA) (B2); build OI / shuffle / random / position patch deltas.
  PHASE 2 (patch): emit P-jobs (transplant patches + controls), run the engine driver, parse argmax;
                  bind-flip = does the patched argmax-continuation now read the OTHER attribute.
  SCORE         : apply the FROZEN 5-bar from h1557_oi_probe_scaffold.score().

usage:
  python3 h1557_oi_probe.py emit_dump   <jobs_out>                         # phase-1 jobs
  python3 h1557_oi_probe.py compute     <dump_in> <patch_jobs_out>         # ΔE/ΔA/PCA/cos + patch jobs
  python3 h1557_oi_probe.py score       <dump_in> <patch_in> <verdict_out> # final 5-bar
  python3 h1557_oi_probe.py all         <bin> <driver_hexa> <workdir>      # run the whole pipeline
"""
import os, sys, math, json, subprocess, importlib.util, random

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_MAIN = "/Users/mini/dancinlab/anima"

# FROZEN bars — import the pre-registered scorer (single source of truth).
_spec = importlib.util.spec_from_file_location("scaf", os.path.join(HERE, "h1557_oi_probe_scaffold.py"))
_scaf = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_scaf)

# ── FROZEN extraction config ──────────────────────────────────────────────
LAYERS = [10, 14, 18]          # mid-late layer sweep of the 24 (binding strongest mid-late, P-LOC)
N_PER_CELL = int(os.environ.get("H1557_N", "220"))   # >= 200 prompts/cell (P-DIR expectation); env override for smoke
SEED = 4557

# vocab families — FROZEN h1305 COMPARATOR/MEASURABLE sets, copied VERBATIM from
# state/universe-probes/h1305_g6_ideation_falsifiability.py lines 43-50 (that module
# import-torch's at load, which this torch-free scorer must NOT pull in). NO new
# authored content (p7) — identical literal sets, sorted for determinism.
COMPARATOR = sorted({"if", "when", "whenever", "than", "more", "less", "greater", "fewer",
              "higher", "lower", "increases", "decreases", "correlates", "predicts",
              "causes", "depends", "unless", "whereas", "versus", "compared",
              "proportional", "faster", "slower", "stronger", "weaker"})
MEASURABLE = sorted({"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"})
ENTITIES = ["the river", "the engine", "the field", "the signal", "the valve", "the rotor",
            "the cable", "the piston", "the magnet", "the beam"]

def _b(s):  # string -> byte-id list (vocab=256)
    return [c for c in s.encode("utf-8")]

def _find_span(prompt, sub, start=0):
    """byte span [lo,hi) of sub's first occurrence in prompt at/after byte `start`."""
    pb = prompt.encode("utf-8"); sb = sub.encode("utf-8")
    idx = pb.find(sb, start)
    if idx < 0: return None
    return (idx, idx + len(sb))

def build_prompts(n_per_cell=N_PER_CELL):
    """Controlled K=2 multi-bind prompts. Each prompt binds entity E0->measurable M_a (bind 0) and
    E1->measurable M_b (bind 1). Records the entity-window + attribute-window LAST-byte position +1
    (binding smears one right, P-LOC → we read last-token AND next-token = a 2-pos window).
    Returns list of dicts with prompt bytes, K, and per-leg (entity/attribute) read positions."""
    rng = random.Random(SEED)
    prompts = []
    nM = len(MEASURABLE); nE = len(ENTITIES); nC = len(COMPARATOR)
    for i in range(n_per_cell):
        e0, e1 = rng.sample(ENTITIES, 2)
        a, bM = rng.sample(range(nM), 2)               # two DISTINCT measurables
        c0 = COMPARATOR[rng.randrange(nC)]; c1 = COMPARATOR[rng.randrange(nC)]
        m0 = MEASURABLE[a]; m1 = MEASURABLE[bM]
        # template (fixed structure; ground-truth bind = which (E,M) share a clause).
        # The query ENDS at "whenever the " so the NEXT byte the model predicts IS the
        # measurable bound to the queried entity e0 → single-forward bind readout (NO
        # autoregression). bind-flip = patched next-byte favors m1[0] over m0[0].
        body = (f"{e0} is {c0} whenever the {m0} grows. "
                f"{e1} is {c1} whenever the {m1} drops. ")
        query = f"query: {e0} is {c0} whenever the "
        prompt = body + query
        # entity windows: last byte of the entity subject in its DECLARING clause (in body)
        ely0 = _find_span(prompt, e0);  ely1 = _find_span(prompt, e1)
        # attribute windows: the measurable token in its DECLARING clause (in body)
        aly0 = _find_span(prompt, m0);  aly1 = _find_span(prompt, m1)
        if None in (ely0, ely1, aly0, aly1): continue
        # read position = last byte of the span AND the next byte (2-pos window, P-LOC smear-right)
        def win(span):
            last = span[1] - 1
            return sorted(set([last, last + 1]))
        m0b = _b(m0); m1b = _b(m1)
        if m0b[0] == m1b[0]:  # need distinct first byte for the single-forward readout
            continue
        prompts.append({
            "id": i, "prompt": prompt, "bytes": _b(prompt), "K": 2,
            "E": {0: win(ely0), 1: win(ely1)},
            "A": {0: win(aly0), 1: win(aly1)},
            "m0": m0, "m1": m1, "e0": e0, "e1": e1,
            "m0_first": m0b[0], "m1_first": m1b[0],
            # the query's LAST position (where the next-byte measurable prediction lives)
            "q_last_pos": len(_b(prompt)) - 1,
        })
    return prompts

# ── phase 1: dump jobs ────────────────────────────────────────────────────
def emit_dump(jobs_out, prompts=None):
    prompts = prompts or build_prompts()
    layers_csv = ",".join(str(l) for l in LAYERS)
    lines = []
    for p in prompts:
        T = len(p["bytes"])
        byte_csv = ",".join(str(x) for x in p["bytes"])
        # all positions we need: union of E/A windows for both binds (clamp < T)
        pos = set()
        for k in (0, 1):
            for w in p["E"][k] + p["A"][k]:
                if 0 <= w < T: pos.add(w)
        pos_csv = ",".join(str(x) for x in sorted(pos))
        lines.append(f"D\t{p['id']}\t{byte_csv}\t{layers_csv}\t{pos_csv}")
    with open(jobs_out, "w") as f: f.write("\n".join(lines) + "\n")
    # stash the prompt manifest next to the jobs so compute/score reuse the EXACT prompts
    with open(jobs_out + ".manifest.json", "w") as f:
        json.dump([{k: v for k, v in p.items()} for p in prompts], f)
    return len(prompts)

# ── parse engine dump ──────────────────────────────────────────────────────
def parse_dump(dump_in):
    """dump line: `<tag>|L<l>_p<t> \t v0 v1 ...`  → vecs[tag][(l,t)] = [floats]."""
    vecs = {}
    with open(dump_in) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or "\t" not in line: continue
            key, vals = line.split("\t", 1)
            tag, lp = key.split("|", 1)
            l = int(lp.split("_")[0][1:]); t = int(lp.split("_")[1][1:])
            vecs.setdefault(tag, {})[(l, t)] = [float(x) for x in vals.split()]
    return vecs

def _vadd(a, b): return [x + y for x, y in zip(a, b)]
def _vsub(a, b): return [x - y for x, y in zip(a, b)]
def _vscale(a, s): return [x * s for x in a]
def _vmean(rows):
    n = len(rows); d = len(rows[0])
    out = [0.0] * d
    for r in rows:
        for i in range(d): out[i] += r[i]
    return [x / n for x in out]
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _norm(a): return math.sqrt(sum(x * x for x in a)) or 1e-12
def _cos(a, b): return _dot(a, b) / (_norm(a) * _norm(b))

def leg_vector(vecs_for_tag, layer, positions):
    """average the residual rows over the read positions at a given layer."""
    rows = [vecs_for_tag[(layer, t)] for t in positions if (layer, t) in vecs_for_tag]
    if not rows: return None
    return _vmean(rows)

def compute_deltas(vecs, prompts, layer):
    """ΔE(1), ΔA(1) at a layer: mean over contexts of (bind1 leg − bind0 leg). (K=2 ⇒ single k=1.)
    Returns (dE, dA, ZE0_list, ZE1_list, ZA0_list, ZA1_list) where the Z lists are per-prompt legs
    (used by the shuffle control)."""
    ZE0, ZE1, ZA0, ZA1 = [], [], [], []
    for p in prompts:
        tg = str(p["id"])
        if tg not in vecs: continue
        T = len(p["bytes"])
        e0 = leg_vector(vecs[tg], layer, [t for t in p["E"][0] if t < T])
        e1 = leg_vector(vecs[tg], layer, [t for t in p["E"][1] if t < T])
        a0 = leg_vector(vecs[tg], layer, [t for t in p["A"][0] if t < T])
        a1 = leg_vector(vecs[tg], layer, [t for t in p["A"][1] if t < T])
        if None in (e0, e1, a0, a1): continue
        ZE0.append(e0); ZE1.append(e1); ZA0.append(a0); ZA1.append(a1)
    if not ZE0: return None
    dE = _vmean([_vsub(e1, e0) for e0, e1 in zip(ZE0, ZE1)])
    dA = _vmean([_vsub(a1, a0) for a0, a1 in zip(ZA0, ZA1)])
    return dE, dA, ZE0, ZE1, ZA0, ZA1

# ── PCA top-2 variance ratio via power iteration + deflation (torch/numpy-free) ──
def pca_top2_var_ratio(rows):
    """rows = list of d-vectors. Center, then top-2 eigen-variance / total variance (trace of cov)."""
    n = len(rows); d = len(rows[0])
    mu = _vmean(rows)
    X = [_vsub(r, mu) for r in rows]
    # total variance = sum of per-dim variance = (1/n) Σ ||x||²
    total = sum(_dot(x, x) for x in X) / n
    if total <= 0: return 0.0
    def cov_mul(v):  # (1/n) Xᵀ X v  without materializing the d×d cov
        out = [0.0] * d
        for x in X:
            s = _dot(x, v)
            for i in range(d): out[i] += s * x[i]
        return [o / n for o in out]
    def power_iter(deflate):
        v = [random.Random(SEED + 7).random() - 0.5 for _ in range(d)]
        nv = _norm(v); v = [x / nv for x in v]
        ev = 0.0
        for _ in range(80):
            w = cov_mul(v)
            for (lam, u) in deflate:           # deflate previous components
                w = _vsub(w, _vscale(u, lam * _dot(u, v)))
            nv = _norm(w)
            if nv < 1e-12: break
            v = [x / nv for x in w]
            ev = _dot(v, cov_mul(v))
        return ev, v
    ev1, u1 = power_iter([])
    ev2, u2 = power_iter([(ev1, u1)])
    return max(0.0, (ev1 + ev2)) / total

# ── PATCH config (FROZEN) ──────────────────────────────────────────────────
PATCH_LAYER = 14               # mid-late layer for the transplant (in LAYERS sweep)
N_PATCH = int(os.environ.get("H1557_NPATCH", "120"))   # patched queries for the bind-flip rate

def _delta_csv(v):
    return ",".join(repr(x) for x in v)

def compute(dump_in, patch_jobs_out, manifest=None):
    """Compute ΔE(1)/ΔA(1) + PCA (B1) + cosine (B2) at PATCH_LAYER from the engine dump,
    then emit the phase-2 patch jobs: OI-patch / shuffle / random / position controls,
    plus the no-patch reference per query. Stashes geometry to patch_jobs_out+'.geom.json'."""
    if manifest is None:
        manifest = dump_in + ".manifest.json" if os.path.exists(dump_in + ".manifest.json") else None
    # the manifest sits next to the DUMP JOBS file; resolve it
    man_path = manifest
    if man_path is None:
        # try the jobs manifest alongside the dump
        cand = os.path.join(os.path.dirname(dump_in), "dump_jobs.jsonl.manifest.json")
        man_path = cand
    prompts = json.load(open(man_path))
    # JSON keys for E/A are strings → coerce back to ints
    for p in prompts:
        p["E"] = {int(k): v for k, v in p["E"].items()}
        p["A"] = {int(k): v for k, v in p["A"].items()}

    vecs = parse_dump(dump_in)
    cr = compute_deltas(vecs, prompts, PATCH_LAYER)
    if cr is None:
        raise SystemExit("compute: no usable dumped legs at PATCH_LAYER")
    dE, dA, ZE0, ZE1, ZA0, ZA1 = cr

    # B1: PCA top-2 var ratio over the per-prompt leg-difference vectors (the OI cloud).
    # rows = {ZE1−ZE0} ∪ {ZA1−ZA0} — the binding shifts whose subspace must be low-rank.
    oi_rows = [_vsub(e1, e0) for e0, e1 in zip(ZE0, ZE1)] + [_vsub(a1, a0) for a0, a1 in zip(ZA0, ZA1)]
    b1_pca = pca_top2_var_ratio(oi_rows)
    # B2: cosine(ΔE, ΔA)
    b2_cos = _cos(dE, dA)

    # SHUFFLE control: recompute ΔE/ΔA with bind labels k shuffled across prompts.
    rng = random.Random(SEED + 13)
    sh_rows = []
    sE0, sE1, sA0, sA1 = [], [], [], []
    for e0, e1, a0, a1 in zip(ZE0, ZE1, ZA0, ZA1):
        if rng.random() < 0.5:                 # randomly swap which leg is "bind1"
            e0, e1 = e1, e0; a0, a1 = a1, a0
        sE0.append(e0); sE1.append(e1); sA0.append(a0); sA1.append(a1)
    sh_dE = _vmean([_vsub(e1, e0) for e0, e1 in zip(sE0, sE1)])
    sh_dA = _vmean([_vsub(a1, a0) for a0, a1 in zip(sA0, sA1)])
    sh_cos = _cos(sh_dE, sh_dA)

    # OI transplant delta: re-tag entity bound to bind0 as bind1 → add (ΔE(1)−ΔE(0)) = ΔE(1)
    # (ΔE(0)=0 by construction since legs are differenced against bind0). i.e. push e0's
    # entity-residual along the binding axis toward bind1.
    oi_delta = dE
    # RANDOM control: a random unit vector at the SAME norm as the OI delta.
    rnd = random.Random(SEED + 29)
    rvec = [rnd.gauss(0, 1) for _ in range(len(oi_delta))]
    rscale = _norm(oi_delta) / _norm(rvec)
    rand_delta = _vscale(rvec, rscale)

    # emit patch jobs for the first N_PATCH prompts that have a dumped entity leg.
    used = [p for p in prompts if str(p["id"]) in vecs][:N_PATCH]
    lines = []
    for p in used:
        T = len(p["bytes"])
        byte_csv = ",".join(str(x) for x in p["bytes"])
        # patch position = e0's entity read position (last byte of e0 span in body)
        epos = [t for t in p["E"][0] if t < T]
        ppos = epos[0] if epos else 0
        # 1) no-patch reference (delta sentinel "-" → no patch, robust to trailing-tab split)
        lines.append(f"P\t{p['id']}_ref\t{byte_csv}\t{PATCH_LAYER}\t{ppos}\t-")
        # 2) OI transplant (re-tag e0 → bind1)
        lines.append(f"P\t{p['id']}_oi\t{byte_csv}\t{PATCH_LAYER}\t{ppos}\t{_delta_csv(oi_delta)}")
        # 3) shuffle-direction patch (ΔE from shuffled labels — must be inert)
        lines.append(f"P\t{p['id']}_shuf\t{byte_csv}\t{PATCH_LAYER}\t{ppos}\t{_delta_csv(sh_dE)}")
        # 4) random-direction patch (same norm — must be inert, B5)
        lines.append(f"P\t{p['id']}_rand\t{byte_csv}\t{PATCH_LAYER}\t{ppos}\t{_delta_csv(rand_delta)}")
        # 5) position control: OI delta applied at e1's position instead of e0's (binding≠position)
        e1pos = [t for t in p["E"][1] if t < T]
        pos2 = e1pos[0] if e1pos else ppos
        lines.append(f"P\t{p['id']}_pos\t{byte_csv}\t{PATCH_LAYER}\t{pos2}\t{_delta_csv(oi_delta)}")
    with open(patch_jobs_out, "w") as f: f.write("\n".join(lines) + "\n")

    geom = {"b1_pca": b1_pca, "b2_cos": b2_cos, "sh_cos": sh_cos,
            "n_oi_rows": len(oi_rows), "patch_layer": PATCH_LAYER,
            "used_ids": [p["id"] for p in used],
            "queries": {str(p["id"]): {"q_last_pos": p["q_last_pos"],
                                       "m0_first": p["m0_first"], "m1_first": p["m1_first"]}
                        for p in used}}
    json.dump(geom, open(patch_jobs_out + ".geom.json", "w"))
    print(json.dumps({"b1_pca": round(b1_pca, 4), "b2_cos": round(b2_cos, 4),
                      "sh_cos": round(sh_cos, 4), "n_patch_jobs": len(lines)}, indent=2))
    return geom

def parse_patch(patch_in):
    """patch line: `<tag>|PATCH \t argmax \t l0 l1 ...` → logits[tag] = [floats]."""
    out = {}
    with open(patch_in) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or "|PATCH" not in line: continue
            key, rest = line.split("\t", 1)
            tag = key.split("|")[0]
            am, logits = rest.split("\t", 1)
            out[tag] = {"argmax": int(am), "logits": [float(x) for x in logits.split()]}
    return out

def _bind_score(logits, m0_first, m1_first):
    """logit mass toward m0's first byte minus m1's first byte. >0 = favors m0 (correct bind)."""
    return logits[m0_first] - logits[m1_first]

def score(patch_in, verdict_out, geom_path=None):
    if geom_path is None: geom_path = patch_in + ".geom.json"
    # geom is stashed next to the patch JOBS file, not the results — accept an override
    if not os.path.exists(geom_path):
        cand = os.path.join(os.path.dirname(patch_in), "patch_jobs.tsv.geom.json")
        geom_path = cand
    geom = json.load(open(geom_path))
    P = parse_patch(patch_in)
    Q = geom["queries"]

    def flip_rate(suffix):
        """fraction of queries where the patched bind_score FLIPS sign vs the no-patch ref
        in the bind1 direction (ref favors m0 (>0) AND patched favors m1 (<0))."""
        flips = 0; n = 0
        for qid, q in Q.items():
            rk = f"{qid}_ref"; pk = f"{qid}_{suffix}"
            if rk not in P or pk not in P: continue
            r = _bind_score(P[rk]["logits"], q["m0_first"], q["m1_first"])
            v = _bind_score(P[pk]["logits"], q["m0_first"], q["m1_first"])
            n += 1
            if r > 0 and v < 0: flips += 1     # bind FLIPPED from m0 to m1
        return (flips / n) if n else 0.0, n

    oi_flip, n_oi   = flip_rate("oi")
    shuf_flip, _    = flip_rate("shuf")
    rand_flip, _    = flip_rate("rand")
    pos_flip, _     = flip_rate("pos")

    b1 = geom["b1_pca"]; b2 = geom["b2_cos"]; shuf_cos = geom["sh_cos"]
    out = _scaf.score(pca_var_ratio=b1, leg_cos=b2, oi_flip=oi_flip,
                      shuf_cos=shuf_cos, shuf_flip=shuf_flip, rand_flip=rand_flip, pos_flip=pos_flip)
    out["_meta"] = {"n_oi_queries": n_oi, "patch_layer": geom["patch_layer"],
                    "layers_swept": LAYERS, "n_per_cell": N_PER_CELL,
                    "oi_flip": oi_flip, "shuf_flip": shuf_flip, "rand_flip": rand_flip, "pos_flip": pos_flip,
                    "b1_pca": b1, "b2_cos": b2, "shuf_cos": shuf_cos}
    with open(verdict_out, "w") as f: json.dump(out, f, indent=2)
    # also write the frozen raw verdict txt (verbatim numbers for the card/jsonl)
    txt_out = os.path.join(os.path.dirname(verdict_out), "H_1557.txt")
    with open(txt_out, "w") as f:
        f.write("H_1557 — OI-SUBSPACE / Binding-ID READ-OUT (G6 lens 9, Family-1) — ENGINE-NATIVE R2\n")
        f.write("substrate: 303M ByteGPT h1129c, live core/bytegpt_decode.hexa (bg_dump_hidden_W + bg_forward_patched_W)\n")
        n_dump_prompts = geom.get("n_oi_rows", 0) // 2   # 2 leg-diff rows per dumped prompt (ΔE,ΔA)
        f.write(f"bin: base.bin | N_dump_prompts={n_dump_prompts} | N_patch_queries={n_oi} | layers_swept={LAYERS} | patch_layer={geom['patch_layer']}\n")
        f.write("=" * 80 + "\n")
        f.write(f"B1 OI-AXIS PRESENT   top-2 PCA var ratio = {b1:.4f}   (>= 0.60 ?) -> {out['B1_pca'][1]}\n")
        f.write(f"B2 LEG-SHARED WELD   mean cos(dE,dA)     = {b2:.4f}   (>= 0.30 ?) -> {out['B2_cos'][1]}\n")
        f.write(f"B3 TRANSPLANT (DEC)  OI-patch flip rate  = {oi_flip:.4f}  (>= 0.50 ?) -> {out['B3_oi_flip'][1]}\n")
        f.write(f"B4 SHUFFLE COLLAPSE  shuf_cos={shuf_cos:.4f} shuf_flip={shuf_flip:.4f}  (cos<0.10 AND flip<0.15 ?) -> {out['B4_shuffle'][1]}\n")
        f.write(f"B5 RANDOM-PATCH      rand_flip={rand_flip:.4f}  (rand<0.15 AND OI-rand>=0.35 ?) -> {out['B5_random'][1]}\n")
        f.write(f"POS control (diag)   pos_flip ={pos_flip:.4f}  (< 0.15 ?) -> {out['pos_control'][1]}\n")
        f.write("=" * 80 + "\n")
        f.write(f"VERDICT: {out['verdict']}\n{out['tier']}\n")
    print("[verdict txt]", txt_out)
    return out

CHUNK = int(os.environ.get("H1557_CHUNK", "20"))   # prompts per driver invocation (bounds memory → no OOM-kill)

def _done_tags(out_path, kind):
    """tags already present in out_path. kind='dump' → the `<id>` before '|', 'patch' → '<id>_<suffix>'."""
    done = set()
    if not os.path.exists(out_path): return done
    with open(out_path) as f:
        for line in f:
            if "\t" not in line: continue
            key = line.split("\t", 1)[0]
            tag = key.split("|", 1)[0]
            done.add(tag)
    return done

def run_driver_chunked(bin_path, driver_hexa, all_job_lines, out_path, done_tag_of, append=True):
    """run the LOAD-ONCE .hexa driver over all_job_lines in CHUNK-sized batches, APPENDING to
    out_path (commit-early/resumable). Skips lines whose tag is already in out_path. Each chunk is
    a fresh driver invocation (fresh model load) → bounded peak memory, robust to OOM-kill mid-batch.
    cwd = worktree root so the driver's `import core/...` resolves; all paths absolute."""
    repo_root = os.path.abspath(os.path.join(HERE, "..", ".."))
    driver_abs = driver_hexa if os.path.isabs(driver_hexa) else os.path.join(repo_root, driver_hexa)
    done = _done_tags(out_path, None)
    pending = [ln for ln in all_job_lines if done_tag_of(ln) not in done]
    print(f"[driver] {len(all_job_lines)} jobs, {len(done)} already done, {len(pending)} pending, chunk={CHUNK}")
    tmp_jobs = out_path + ".chunk_jobs"
    tmp_out  = out_path + ".chunk_out"
    i = 0
    while i < len(pending):
        chunk = pending[i:i + CHUNK]
        with open(tmp_jobs, "w") as f: f.write("\n".join(chunk) + "\n")
        if os.path.exists(tmp_out): os.remove(tmp_out)
        cmd = ["hexa", "run", driver_abs, "--",
               os.path.abspath(bin_path), os.path.abspath(tmp_jobs), os.path.abspath(tmp_out)]
        r = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, timeout=7200)
        if r.returncode != 0:
            print(f"[driver] chunk {i//CHUNK} rc={r.returncode} stderr={r.stderr.strip()[-300:]}")
            # if killed (rc<0), retry this chunk once smaller; else abort
            if r.returncode < 0 and len(chunk) > 1:
                print("[driver] OOM/kill suspected — retrying chunk at half size")
                half = max(1, len(chunk) // 2)
                # re-run the FIRST half now; the rest stay pending (i advances by half)
                with open(tmp_jobs, "w") as f: f.write("\n".join(chunk[:half]) + "\n")
                if os.path.exists(tmp_out): os.remove(tmp_out)
                r = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, timeout=7200)
                if r.returncode != 0:
                    raise SystemExit(f"driver chunk failed even at half size rc={r.returncode}")
                with open(tmp_out) as fo, open(out_path, "a") as fa: fa.write(fo.read())
                i += half
                continue
            raise SystemExit(f"engine driver chunk failed rc={r.returncode}")
        # append the chunk's rows to the cumulative out (commit-early)
        with open(tmp_out) as fo, open(out_path, "a") as fa: fa.write(fo.read())
        i += len(chunk)
        print(f"[driver] +{len(chunk)} ({i}/{len(pending)} pending; cumulative file appended)")
    for p in (tmp_jobs, tmp_out):
        if os.path.exists(p): os.remove(p)

def cmd_all(bin_path, driver_hexa, workdir):
    os.makedirs(workdir, exist_ok=True)
    dump_jobs = os.path.join(workdir, "dump_jobs.jsonl")
    dump_out  = os.path.join(workdir, "dump_out.tsv")
    patch_jobs = os.path.join(workdir, "patch_jobs.tsv")
    patch_out  = os.path.join(workdir, "patch_out.tsv")
    verdict    = os.path.join(workdir, "verdict.json")

    # PHASE 1: build prompts + dump jobs (resumable; reuse existing manifest/jobs if present)
    if os.path.exists(dump_jobs + ".manifest.json") and os.path.exists(dump_jobs):
        n = len(open(dump_jobs).read().strip().splitlines())
        print(f"[phase1] reusing {n} existing dump jobs (resume)")
    else:
        n = emit_dump(dump_jobs)
        print(f"[phase1] {n} dump prompts (fresh)")
    dump_lines = [ln for ln in open(dump_jobs).read().splitlines() if ln.strip()]
    run_driver_chunked(bin_path, driver_hexa, dump_lines, dump_out,
                       done_tag_of=lambda ln: ln.split("\t")[1])   # D\t<id>\t...
    # COMPUTE geometry + patch jobs
    compute(dump_out, patch_jobs, manifest=dump_jobs + ".manifest.json")
    # PHASE 2: run engine patches (resumable, chunked)
    patch_lines = [ln for ln in open(patch_jobs).read().splitlines() if ln.strip()]
    run_driver_chunked(bin_path, driver_hexa, patch_lines, patch_out,
                       done_tag_of=lambda ln: ln.split("\t")[1])   # P\t<id>_<suffix>\t...
    # SCORE
    out = score(patch_out, verdict, geom_path=patch_jobs + ".geom.json")
    print("\n=== VERDICT ===")
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "emit_dump":
        n = emit_dump(sys.argv[2]); print(f"emitted {n} dump prompts")
    elif cmd == "compute":
        compute(sys.argv[2], sys.argv[3])
    elif cmd == "score":
        score(sys.argv[2], sys.argv[3])
    elif cmd == "all":
        cmd_all(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "selftest":
        # tiny synthetic check of the arithmetic (NOT engine — just validates PCA/cos math)
        random.seed(1)
        base = [random.gauss(0, 1) for _ in range(32)]
        axis = [random.gauss(0, 1) for _ in range(32)]
        rows = []
        for _ in range(200):
            s = random.gauss(0, 3)
            rows.append([b + s * a + random.gauss(0, 0.05) for b, a in zip(base, axis)])
        print("PCA top-2 var ratio (should be ~1.0):", round(pca_top2_var_ratio(rows), 4))
    else:
        print(__doc__)
