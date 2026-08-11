#!/usr/bin/env python3
"""cli/sweep.py — the CANONICAL anima multi-GPU lever-sweep orchestrator (`anima sweep`).

>>> This file promotes the ad-hoc scratch shell orchestration (fire_4gpu_big.sh and
>>> friends) into a proper, reproducible single-entry subcommand, SYMMETRIC to
>>> cli/train.py (LEARNING) and cli/evaluate.py (MEASUREMENT). `anima sweep <args>`
>>> dispatches HERE. No scratch fire_*.sh sprawl.
>>>
>>> WHAT IT DOES: run a ρ·weave-lever sweep (recombination wall · frozen bar = former G1 ·
>>> H_1129) over the matrix  ARMS × OBJECTIVES. Each
>>> (arm, objective) pair is one "cell". Cells are pinned round-robin to the GPUs in
>>> --gpus and run concurrently (max-concurrent = number of GPUs). Each cell:
>>>   (1) TRAINS a 303M CLMConvMoE via `python3 cli/train.py …` (CUDA_VISIBLE_DEVICES
>>>       pinned to its GPU), serializing <out-dir>/<tag>.clm.
>>>   (2) if --measure, ρ-AXON reach-MEASURES (former G0-G6) the resulting .clm via `python3 cli/evaluate.py
>>>       <clm> --corpus … --gen N` (CPU, torch-free numpy) -> <out-dir>/<tag>.meas.log.
>>>   (3) touches a per-cell done flag.
>>> After every cell finishes, the orchestrator PARSES each <tag>.meas.log for the
>>> reach-bar lines (ρ·form/weave/leap/fan, parsed by their frozen-bar G-labels) and prints
>>> + writes a summary TABLE (SWEEP_SUMMARY.md),
>>> flagging any ρ·weave-PASS candidate (former G1 · best_distinct >= 2 AND > max_single) and any
>>> overfit-collapse INVALID cell (ρ·form/G0 FAIL + collapsed train CE).
>>>
>>> DESIGN INVARIANT (single-entry discipline, a_engine_native_learning): sweep is
>>> ONLY an orchestrator. It NEVER imports torch / the model / the scorers — it shells
>>> out to the two canonical engines (cli/train.py, cli/evaluate.py) as SUBPROCESSES,
>>> exactly as the hexa anima_train_mode / anima_evaluate_mode dispatch shells out.
>>> This keeps sweep torch-free (pure orchestration + subprocess + text parsing) and
>>> makes the trainer/evaluator the single sources of truth. The engine-native TERMINAL
>>> verdict is the .clm re-measure via cli/evaluate.py (already the measure step here);
>>> the torch-side training CE is DIRECTIONAL only (a_engine_native_learning).
>>>
>>> bf16 vs fp32 (convergence lesson): objective==constructive_bind uses torch.fft
>>> (HRR circular convolution), which has NO bf16 kernel — bf16 there silently dies
>>> (H_1823). So the orchestrator AUTO-DROPS --bf16 for constructive_bind (fp32) and
>>> keeps --bf16 for every other objective. This mirrors fire_4gpu_big.sh (B_CBIND ran
>>> with an empty bf16 flag).

USAGE (installed canonical `anima-py` command):
  anima sweep --arms ctrl --objectives ce_marginal,composed_nce,infonce,constructive_bind \\
      --steps 8000 --gpus 0,1,2,3 \\
      --corpus dancinlab/anima-corpus-5lang-unified-v2 dancinlab/anima-corpus-ko-general \\
      --cell-label general-5lang ko-general --measure
"""
from __future__ import annotations
import argparse
import os
import re
import subprocess
import glob
import sys
import threading
import time

# ── canonical engine paths (resolved relative to THIS file so it works installed) ──
_HERE = os.path.dirname(os.path.abspath(__file__))            # …/cli
_REPO = os.environ.get("ANIMA_SRC") or os.path.dirname(_HERE)  # repo root (parent of cli/)
_TRAIN_PY = os.path.join(_HERE, "train.py")                    # canonical trainer
_EVAL_PY = os.path.join(_HERE, "evaluate.py")                  # canonical evaluator

# objectives whose loss uses torch.fft (HRR bind) → NO bf16 kernel → force fp32.
_FP32_ONLY_OBJECTIVES = {"constructive_bind"}

# overfit-collapse heuristic (convergence train-py-3): a memorized/collapsed run drives
# the TRAIN CE toward ~0 while the model is garbage (held-out never descends, ρ·form/G0 fails).
# So ρ·form/G0 FAIL + a collapsed final train CE => the ρ-AXON reach measurement (former G0-G6) is INVALID (not a real
# capability floor, just corpus starvation / memorization). Threshold is frozen, documented.
_OVERFIT_LOSSF_THRESH = 0.5


# ════════════════════════════════════════════════════════════════════════════
#  GPU discovery
# ════════════════════════════════════════════════════════════════════════════
def _default_gpus() -> list[str]:
    """Default GPU index list = all visible. Honor CUDA_VISIBLE_DEVICES if set, else
    probe `nvidia-smi -L`, else fall back to a single ['0']."""
    cvd = os.environ.get("CUDA_VISIBLE_DEVICES")
    if cvd:
        # pass the visible physical indices through as-is — each becomes a child's
        # CUDA_VISIBLE_DEVICES (do NOT re-index, or a user's pre-restriction is lost).
        vis = [g.strip() for g in cvd.split(",") if g.strip()]
        if vis:
            return vis
    try:
        out = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True, timeout=15)
        n = len([ln for ln in out.stdout.splitlines() if ln.strip().startswith("GPU ")])
        if n > 0:
            return [str(i) for i in range(n)]
    except Exception:
        pass
    return ["0"]


# ════════════════════════════════════════════════════════════════════════════
#  one cell = one (arm, objective) train (+ optional measure)
# ════════════════════════════════════════════════════════════════════════════
def _cell_tag(arm: str, objective: str, seed: int) -> str:
    return f"{arm}_{objective}_s{seed}"


def _build_train_cmd(a, arm: str, objective: str, tag: str, out_dir: str) -> list[str]:
    clm = os.path.join(out_dir, tag + ".clm")
    pt = os.path.join(out_dir, tag + ".pt")
    gj = os.path.join(out_dir, tag + ".json")
    cmd = [sys.executable, _TRAIN_PY,
           "--arm", arm, "--objective", objective,
           "--tlora-rank", str(a.tlora_rank),
           "--seed", str(a.seed),
           "--steps", str(a.steps),
           "--sample", a.sample,
           "--val-frac", str(a.val_frac),
           "--val-every", str(a.val_every),
           "--dbes-every", str(a.dbes_every),
           "--out", clm, "--ckpt-out", pt, "--gauges-out", gj]
    if a.canon:
        cmd.append("--canon")
    if a.corpus:
        cmd += ["--corpus", *a.corpus]
    if a.cell_label:
        cmd += ["--cell-label", *a.cell_label]
    # bf16 EXCEPT for fft-based objectives (constructive_bind → fp32, H_1823 lesson).
    if a.bf16 and objective not in _FP32_ONLY_OBJECTIVES:
        cmd.append("--bf16")
    # N6 regularization-floor passthrough: force a CONSTANT dropout/weight-decay
    # (>=0 overrides the savant decay schedule) — needed to escape the 8000-step
    # generation-collapse (train-py-4) by holding inhibition at a floor.
    if a.dropout_floor >= 0.0:
        cmd += ["--dropout-floor", str(a.dropout_floor)]
    if a.wd_floor >= 0.0:
        cmd += ["--wd-floor", str(a.wd_floor)]
    # step-window multiplex: train.py dumps <clm>.step<N>.clm every N steps so ONE run
    # yields the 2000/4000/… checkpoints (train-py-4 confound isolation, no re-train).
    if a.ckpt_every > 0:
        cmd += ["--ckpt-every", str(a.ckpt_every)]
    return cmd


def _ckpt_step(path: str):
    """Extract N from a `<clm>.step<N>.clm` intermediate-checkpoint path (else None)."""
    m = re.search(r"\.step(\d+)\.clm$", path)
    return int(m.group(1)) if m else None


def _build_measure_cmd(a, tag: str, out_dir: str) -> list[str]:
    clm = os.path.join(out_dir, tag + ".clm")
    cmd = [sys.executable, _EVAL_PY, clm, "--gen", str(a.gen)]
    if a.corpus:
        cmd += ["--corpus", *a.corpus]
    return cmd


def run_cell(a, arm: str, objective: str, gpu: str, out_dir: str, log_lock: threading.Lock):
    """Train (GPU-pinned) then optionally measure (CPU) one (arm,objective) cell."""
    tag = _cell_tag(arm, objective, a.seed)
    clm = os.path.join(out_dir, tag + ".clm")
    train_log = os.path.join(out_dir, tag + ".log")
    meas_log = os.path.join(out_dir, tag + ".meas.log")
    bf = "fp32" if objective in _FP32_ONLY_OBJECTIVES else ("bf16" if a.bf16 else "fp32")

    def _say(msg):
        with log_lock:
            print(f"[{time.strftime('%H:%M:%S')}] [gpu{gpu}] {tag}: {msg}", flush=True)

    # ── (1) TRAIN (CUDA_VISIBLE_DEVICES pinned to this cell's GPU) ────────────
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu)
    _say(f"TRAIN start ({arm}/{objective}, {bf}) -> {os.path.basename(clm)}")
    with open(train_log, "w") as lf:
        rc = subprocess.run(_build_train_cmd(a, arm, objective, tag, out_dir),
                            cwd=_REPO, env=env, stdout=lf, stderr=subprocess.STDOUT).returncode
    have_clm = os.path.exists(clm) and os.path.getsize(clm) > 0
    _say(f"TRAIN done rc={rc} clm={'OK' if have_clm else 'MISSING'}")
    open(os.path.join(out_dir, tag + ".done"), "w").close()   # per-cell train done flag

    # ── (2) MEASURE (CPU, torch-free numpy evaluate — CUDA hidden) ────────────
    # step-window: measure the FINAL <tag>.clm AND every intermediate --ckpt-every
    # checkpoint (<tag>.clm.step<N>.clm), each into its own <label>.meas.log so the
    # aggregate can plot ρ·form/ρ·weave (former G0/G1) across steps (train-py-4 confound: where does ρ·form/G0 break?).
    if a.measure:
        menv = os.environ.copy()
        menv["CUDA_VISIBLE_DEVICES"] = ""                    # force CPU numpy path
        menv.setdefault("OMP_NUM_THREADS", "8")
        targets = []
        for cp in sorted((p for p in glob.glob(clm + ".step*.clm")), key=_ckpt_step):
            n = _ckpt_step(cp)
            targets.append((cp, f"{tag}__s{n}"))
        if have_clm:
            targets.append((clm, tag))                       # final full-run (bare tag)
        if not targets:
            with open(meas_log, "w") as lf:
                lf.write("NO CKPT — train produced no .clm; measure skipped\n")
        for cpath, label in targets:
            ml = os.path.join(out_dir, label + ".meas.log")
            with open(ml, "w") as lf:
                lf.write(f"=== [{label}] ρ-AXON reach measure · former G0-G6 ({time.strftime('%H:%M:%S')}) ===\n")
                lf.flush()
                mcmd = [sys.executable, _EVAL_PY, cpath, "--gen", str(a.gen)]
                if a.corpus:
                    mcmd += ["--corpus", *a.corpus]
                mrc = subprocess.run(mcmd, cwd=_REPO, env=menv, stdout=lf,
                                     stderr=subprocess.STDOUT).returncode
                lf.write(f"\n=== [{label}] measure rc={mrc} ===\n")
        open(os.path.join(out_dir, tag + ".meas.done"), "w").close()  # per-cell measure flag
        _say(f"MEASURE done ({len(targets)} checkpoint(s))")


# ════════════════════════════════════════════════════════════════════════════
#  aggregate — parse each <tag>.meas.log (+ <tag>.log) into a summary table
# ════════════════════════════════════════════════════════════════════════════
_RE_G1 = re.compile(r"best_distinct=(\d+)\s*>\s*max_single=(\d+)")
_RE_G2 = re.compile(r"novel=(\d+)")
_RE_G6 = re.compile(r"distinct=(\d+)\s*\(need>=5\).*?falsifiable=(\d+)")
_RE_G0N = re.compile(r"on\s+(\d+)/5")
_RE_LOSSF = re.compile(r"lossF=([0-9.]+)")
_RE_VALPOOL = re.compile(r"FINAL val_CE\(pooled\)=(\S+)")


def _gate_pass(line: str) -> bool:
    # evaluate.py prints 🟢 for PASS, 🔴 for FAIL on G0/G1/G2/G6.
    return "🟢" in line


def parse_cell(tag: str, out_dir: str) -> dict:
    """Parse one cell's measure log (+ train log) into a result dict."""
    meas_log = os.path.join(out_dir, tag + ".meas.log")
    # a checkpoint label is "<base>__s<N>"; its train log is the base cell's <base>.log
    base_tag = tag.split("__s")[0]
    train_log = os.path.join(out_dir, base_tag + ".log")
    r = {"tag": tag, "form": None, "form_n": None, "weave": None, "weave_bd": None,
         "weave_ms": None, "leap": None, "leap_novel": None, "fan": None, "fan_dist": None,
         "fan_fals": None, "closure": None, "lossf": None, "val_pool": None,
         "status": "?", "note": ""}

    # train log → collapse signals
    if os.path.exists(train_log):
        tl = open(train_log, encoding="utf-8", errors="replace").read()
        m = _RE_LOSSF.search(tl)
        if m:
            r["lossf"] = float(m.group(1))
        m = _RE_VALPOOL.search(tl)
        if m and m.group(1) not in ("None", "nan"):
            try:
                r["val_pool"] = float(m.group(1))
            except ValueError:
                pass

    if not os.path.exists(meas_log):
        r["status"] = "NO-MEAS"
        r["note"] = "no measure log"
        return r
    txt = open(meas_log, encoding="utf-8", errors="replace").read()
    if "NO CKPT" in txt:
        r["status"] = "NO-CKPT"
        r["note"] = "train produced no .clm"
        return r

    for line in txt.splitlines():
        if "ρ·form COHERENCE" in line:
            r["form"] = _gate_pass(line)
            mm = _RE_G0N.search(line)
            if mm:
                r["form_n"] = int(mm.group(1))
        elif "ρ·weave RECOMBINATION" in line:
            r["weave"] = _gate_pass(line)
            mm = _RE_G1.search(line)
            if mm:
                r["weave_bd"] = int(mm.group(1)); r["weave_ms"] = int(mm.group(2))
        elif "ρ·leap NOVELTY" in line:
            r["leap"] = _gate_pass(line)
            mm = _RE_G2.search(line)
            if mm:
                r["leap_novel"] = int(mm.group(1))
        elif "ρ·fan IDEATION" in line:
            r["fan"] = _gate_pass(line)
            mm = _RE_G6.search(line)
            if mm:
                r["fan_dist"] = int(mm.group(1)); r["fan_fals"] = int(mm.group(2))
        elif line.strip().startswith("CLOSURE"):
            r["closure"] = _gate_pass(line)

    # status classification
    # overfit-INVALID applies to the FINAL run only (lossf is the end-of-run CE; an
    # intermediate step-window checkpoint keeps its own ρ·form/ρ·weave · former G0/G1 row, not an overfit verdict).
    overfit = ("__s" not in tag and r["form"] is False and r["lossf"] is not None
               and r["lossf"] < _OVERFIT_LOSSF_THRESH)
    weave_cand = (r["weave_bd"] is not None and r["weave_ms"] is not None
               and r["weave_bd"] >= 2 and r["weave_bd"] > r["weave_ms"])
    if r["form"] is None:
        r["status"] = "INCOMPLETE"
        r["note"] = "measure did not finish (no gate lines)"
    elif overfit:
        r["status"] = "INVALID"
        r["note"] = (f"overfit collapse — G0 FAIL + train CE→{r['lossf']:.3f} "
                     f"(<{_OVERFIT_LOSSF_THRESH}); measurement invalid (corpus starvation)")
    elif weave_cand:
        r["status"] = "ρ·weave-PASS?"
        r["note"] = (f"ρ·weave-PASS candidate: best_distinct={r['weave_bd']} > "
                     f"max_single={r['weave_ms']}")
    elif r["closure"]:
        r["status"] = "CLOSURE"
    else:
        r["status"] = "OK"
    return r


def _fmt(v, dash="—"):
    return dash if v is None else str(v)


def _pf(v):
    if v is None:
        return "—"
    return "🟢" if v else "🔴"


def _row_sortkey(lbl: str):
    base = lbl.split("__s")[0]
    st = lbl.split("__s")[1] if "__s" in lbl else None
    return (base, int(st) if (st and st.isdigit()) else 10 ** 9)  # final (no __s) sorts last


def aggregate(a, cells, out_dir: str):
    # one row per measured checkpoint: glob every <label>.meas.log (final <tag> +
    # step-window <tag>__s<N>), so --ckpt-every runs expand into per-step rows.
    labels = sorted((os.path.basename(p)[:-len(".meas.log")]
                     for p in glob.glob(os.path.join(out_dir, "*.meas.log"))),
                    key=_row_sortkey)
    if labels:
        rows = [parse_cell(lbl, out_dir) for lbl in labels]
    else:
        rows = [parse_cell(_cell_tag(arm, obj, a.seed), out_dir) for (arm, obj) in cells]

    # console + markdown table
    header = ("| tag | ρ·form | ρ·weave bd/ms | ρ·leap novel | ρ·fan dist/fals | closure | status |")
    sep = ("|---|---|---|---|---|---|---|")
    lines = [header, sep]
    for r in rows:
        weave = f"{_fmt(r['weave_bd'])}/{_fmt(r['weave_ms'])}"
        fan = f"{_fmt(r['fan_dist'])}/{_fmt(r['fan_fals'])}"
        lines.append(
            f"| {r['tag']} | {_pf(r['form'])} | {weave} | {_fmt(r['leap_novel'])} | "
            f"{fan} | {_pf(r['closure'])} | {r['status']} |")

    weave_cands = [r for r in rows if r["status"] == "ρ·weave-PASS?"]
    invalids = [r for r in rows if r["status"] == "INVALID"]

    md = []
    md.append(f"# anima sweep summary — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("")
    md.append(f"- matrix: arms={a.arms} × objectives={a.objectives} "
              f"(seed={a.seed}, steps={a.steps}, gen={a.gen})")
    md.append(f"- cells: {len(rows)}  ·  out-dir: `{out_dir}`")
    md.append(f"- engines: `cli/train.py` (GPU) + `cli/evaluate.py` (CPU numpy, torch-free)")
    md.append("")
    md += lines
    md.append("")
    md.append("## flags")
    if weave_cands:
        md.append("**🟢 ρ·weave-PASS candidate(s)** (best_distinct ≥ 2 AND > max_single — "
                  "engine-native recombination signal, verify byte-exact before cementing):")
        for r in weave_cands:
            md.append(f"- `{r['tag']}` — {r['note']}")
    else:
        md.append("- ρ·weave-PASS candidates: none (all cells floored best_distinct ≤ max_single).")
    if invalids:
        md.append("")
        md.append("**⚠️ INVALID (overfit collapse — measurement not trustworthy):**")
        for r in invalids:
            md.append(f"- `{r['tag']}` — {r['note']}")
    md.append("")
    md.append("> HONESTY (a_engine_native_learning / c9): the ρ-AXON reach measure (former G0-G6) here IS the "
              "engine-native `.clm` re-measure (cli/evaluate.py numpy mirror = terminal-eligible). "
              "The torch-side training CE (in each `<tag>.log`) is DIRECTIONAL only. A ρ·weave-PASS (former G1) "
              "candidate still needs the frozen-bar verdict cemented from THIS measure output "
              "verbatim (no tune-to-green).")
    md_text = "\n".join(md) + "\n"

    summary_path = os.path.join(out_dir, "SWEEP_SUMMARY.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print("")
    print("════════════════════════════════════════════════════════════════")
    print(f"  anima sweep aggregate ({len(rows)} cells)")
    print("════════════════════════════════════════════════════════════════")
    for ln in lines:
        print("  " + ln)
    print("")
    if weave_cands:
        print("  🟢 ρ·weave-PASS candidate(s):")
        for r in weave_cands:
            print(f"     {r['tag']} — {r['note']}")
    else:
        print("  ρ·weave-PASS candidates: none.")
    if invalids:
        print("  ⚠️ INVALID (overfit collapse):")
        for r in invalids:
            print(f"     {r['tag']} — {r['note']}")
    print("")
    print(f"  summary -> {summary_path}")
    return rows


# ════════════════════════════════════════════════════════════════════════════
def _csv(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="anima sweep",
        description="canonical multi-GPU lever-sweep orchestrator — the arms×objectives "
                    "matrix, GPU-pinned round-robin, subprocess-shells cli/train.py + "
                    "cli/evaluate.py, aggregates the ρ-AXON reach bars · former G0-G6 (replaces scratch fire_*.sh).")
    ap.add_argument("--arms", default="ctrl",
                    help="comma list of train.py --arm values (default ctrl)")
    ap.add_argument("--objectives", default="ce_marginal,composed_nce,infonce,constructive_bind",
                    help="comma list of train.py --objective values (matrix = arms × objectives)")
    ap.add_argument("--steps", type=int, default=8000)
    ap.add_argument("--ckpt-every", type=int, default=0,
                    help="0=final .clm only; N=also dump+measure a checkpoint every N steps "
                         "(step-window: one run → ρ·form/ρ·weave · former G0/G1 across 2000/4000/… — train-py-4 isolation)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--corpus", nargs="*", default=[],
                    help="corpus paths / HF ids passed through to train.py + evaluate.py")
    ap.add_argument("--cell-label", nargs="*", default=[],
                    help="per-corpus register labels passed through to train.py")
    ap.add_argument("--gpus", default="",
                    help="comma list of GPU indices to pin round-robin (default = all visible)")
    ap.add_argument("--out-dir", default="./sweeprun",
                    help="dir for .clm/.pt/.log/.meas.log + SWEEP_SUMMARY.md")
    ap.add_argument("--gen", type=int, default=80, help="measure decode budget (tokens)")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.02)
    ap.add_argument("--val-every", type=int, default=500)
    ap.add_argument("--dbes-every", type=int, default=100000)
    ap.add_argument("--tlora-rank", type=int, default=8)
    # N6 regularization floor (savant decay override) — forwarded to train.py only when >=0.
    ap.add_argument("--dropout-floor", type=float, default=-1.0,
                    help="force constant dropout (>=0 overrides savant decay; escapes 8000-step collapse)")
    ap.add_argument("--wd-floor", type=float, default=-1.0,
                    help="force constant weight-decay (>=0 overrides savant decay)")
    # bf16 default ON (train.py toy default is fp32, but a 303M GPU sweep wants bf16);
    # constructive_bind is auto-forced fp32 regardless (fft has no bf16 kernel).
    bf = ap.add_mutually_exclusive_group()
    bf.add_argument("--bf16", dest="bf16", action="store_true", default=True)
    bf.add_argument("--no-bf16", dest="bf16", action="store_false")
    ap.add_argument("--canon", dest="canon", action="store_true", default=True,
                    help="303M CLMConvMoE (d3784·L4) — default ON")
    ap.add_argument("--no-canon", dest="canon", action="store_false",
                    help="toy shape (d64·L2) for a CPU smoke of the orchestration")
    ms = ap.add_mutually_exclusive_group()
    ms.add_argument("--measure", dest="measure", action="store_true", default=True,
                    help="after each train, ρ-AXON reach-measure · former G0-G6 the .clm (default)")
    ms.add_argument("--no-measure", dest="measure", action="store_false",
                    help="train only, skip measurement")
    a = ap.parse_args(argv)

    a.arms = _csv(a.arms)
    a.objectives = _csv(a.objectives)
    gpus = _csv(a.gpus) if a.gpus else _default_gpus()
    out_dir = os.path.abspath(a.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # matrix = arms × objectives (each a cell)
    cells = [(arm, obj) for arm in a.arms for obj in a.objectives]

    print("=== anima sweep (canonical multi-GPU lever-sweep orchestrator) ===", flush=True)
    print(f"  engines : train={_TRAIN_PY}", flush=True)
    print(f"            eval ={_EVAL_PY}", flush=True)
    print(f"  matrix  : arms={a.arms} × objectives={a.objectives} = {len(cells)} cells", flush=True)
    print(f"  gpus    : {gpus}  (max-concurrent = {len(gpus)})", flush=True)
    print(f"  cfg     : steps={a.steps} seed={a.seed} gen={a.gen} bf16={a.bf16} "
          f"canon={a.canon} measure={a.measure} sample={a.sample}", flush=True)
    print(f"  out-dir : {out_dir}", flush=True)
    for i, (arm, obj) in enumerate(cells):
        g = gpus[i % len(gpus)]
        bfnote = "fp32(fft)" if obj in _FP32_ONLY_OBJECTIVES else ("bf16" if a.bf16 else "fp32")
        print(f"    cell[{i}] {_cell_tag(arm, obj, a.seed):<32s} -> gpu{g}  [{bfnote}]", flush=True)
    print("", flush=True)

    # ── round-robin assign cells to GPUs; one worker thread per GPU runs its cells
    #    sequentially (train then measure). max-concurrent = number of GPUs. ────────
    per_gpu: dict[str, list] = {g: [] for g in gpus}
    for i, cell in enumerate(cells):
        per_gpu[gpus[i % len(gpus)]].append(cell)

    log_lock = threading.Lock()

    def gpu_worker(gpu: str, assigned: list):
        for (arm, obj) in assigned:
            run_cell(a, arm, obj, gpu, out_dir, log_lock)

    threads = [threading.Thread(target=gpu_worker, args=(g, per_gpu[g]), daemon=True)
               for g in gpus if per_gpu[g]]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if a.measure:
        aggregate(a, cells, out_dir)
    else:
        print("  --no-measure: trained only, no ρ-AXON reach aggregate (former G0-G6).", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
