#!/usr/bin/env python3
"""H_1492 R3 — CONSCIOUSNESS ABLATION on 303M production ConvMoE.

SUBSTRATE SOURCE: REAL 303M engine decode via hexa core/clm_decode.hexa::clm_forward_ce.
  - Calls clm_forward_ce(ckpt, corpus_file, 1) for each of N_CONTEXTS diverse text snippets
  - Returns real {model_ce, uniform_ce, shuffle_ce} from live 303M ConvMoE forward
  - m = 1 - model_ce/uniform_ce  (real grounding margin from 303M predictions)
  - Runs 15 consciousness lanes + Phi-proxy ablation sweep in Python (READ-ONLY gauge)

HONESTY (c9, a_scale_honest_scope):
  - core/clm_decode.hexa has NO imports; clm_forward_ce is pub fn → standalone
  - N_CONTEXTS = 30; each call ~25-30s; total ~15 min on summer RTX 5070
  - REAL CE from live 303M ConvMoE; NOT numpy synthetic; NOT torch side
  - phi_proxy = Gaussian-integration PROXY (NOT faithful IIT4 Phi, a_train_inline_gauge)
  - Tier: PRODUCTION DIRECTIONAL (real 303M substrate reads, proxy Phi, small-N)
  - ckpt: dancinlab/anima-clm-ideation-303m-convmoe-engine-mount :: clm303_d5000.clm
    (ConvMoE .clm v0.2 CLMX 302.6M params, sha256 99c2a40e...)
    NOT dancinlab/303m-broad-en-emergent (ByteGPT .pt — not engine-mountable as .clm)
"""
import json
import math
import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CKPT_PATH = "/tmp/h1492_303m/clm303_d5000.clm"
CKPT_SHA256 = "99c2a40e4e4c23e16f7ec80f29aaa3a362065983e00709f723f1106598efa3cd"
HEXA = "/home/summer/.hx/bin/hexa"
ANIMA_ROOT = "/home/summer/anima"
TMP_CORPUS = "/tmp/h1492_r3_corpus_{i}.txt"
TMP_PROBE = "/tmp/h1492_r3_probe_{i}.hexa"

N_CONTEXTS = 30
N_SHUF = 50
BAR_CONTROL = 0.05
BAR_SHUFFLE_RATIO = 0.10

LANE_NAMES = [
    "GlobalWorkspace", "Habituation", "PrecisionSurprise", "SelfIdentity",
    "LearnedPrecision", "Novelty", "AttentionalBlink", "SenseOfAgency",
    "SubjectiveTime", "EmotionRegulation", "DirectedForgetting", "BodyOwnership",
    "DividedAttention", "FreeWont", "MitosisGrowth",
]
N_LANES = len(LANE_NAMES)
PASS_THR = 0.55
OFF = 0.5


# ── 15 lane functions (verbatim formulas from R1) ─────────────────────────────
def lane_global_workspace(st):
    f = sorted(st["m_field"], reverse=True)
    if len(f) < 2:
        return OFF
    return float(min(1.0, max(0.0, f[0] - 0.9 * f[1] + 0.5)))

def lane_habituation(st):
    return float(1.0 / (1.0 + st["seen"]))

def lane_precision_surprise(st):
    err = abs(st["m"] - st["m_prev"])
    prec = 1.0 + 3.0 * st["m_prev"]
    return float(min(1.0, max(0.0, prec * err * err)))

def lane_self_identity(st):
    return float(min(1.0, max(0.0, 1.0 - abs(st["m"] - st["m_prev"]))))

def lane_learned_precision(st):
    return float(min(1.0, max(0.0, st["m"])))

def lane_novelty(st):
    return float(min(1.0, max(0.0, st["recon_err"] / (1.0 + 0.5 * st["seen"]))))

def lane_attentional_blink(st):
    return float(min(1.0, max(0.0, 1.0 - math.exp(-st["dt"]))))

def lane_sense_of_agency(st):
    return float(min(1.0, max(0.0, st["intent"] * st["m"])))

def lane_subjective_time(st):
    return float(min(1.0, max(0.0, 1.0 - 1.0 / (1.0 + st["dt"]))))

def lane_emotion_regulation(st):
    return float(min(1.0, max(0.0, 1.0 - 2.0 * abs(st["m"] - 0.5))))

def lane_directed_forgetting(st):
    if st["m"] < PASS_THR:
        return float(min(1.0, max(0.0, 1.0 - st["m"])))
    return float(min(1.0, max(0.0, st["m"])))

def lane_body_ownership(st):
    fm = sum(st["m_field"]) / len(st["m_field"])
    return float(min(1.0, max(0.0, 1.0 - abs(st["m"] - fm))))

def lane_divided_attention(st):
    f = [max(1e-6, x) for x in st["m_field"]]
    s = sum(f)
    p = [x / s for x in f]
    ent = -sum(x * math.log(x) for x in p) / math.log(len(p))
    return float(min(1.0, max(0.0, ent)))

def lane_free_wont(st):
    if st["intent"]:
        return float(min(1.0, max(0.0, 1.0 - st["m"])))
    return 0.5

def lane_mitosis_growth(st):
    return float(min(1.0, max(0.0, 1.0 - math.exp(-0.3 * st["cells"]))))

LANE_FNS = [
    lane_global_workspace, lane_habituation, lane_precision_surprise,
    lane_self_identity, lane_learned_precision, lane_novelty,
    lane_attentional_blink, lane_sense_of_agency, lane_subjective_time,
    lane_emotion_regulation, lane_directed_forgetting, lane_body_ownership,
    lane_divided_attention, lane_free_wont, lane_mitosis_growth,
]


# ── Phi-proxy (same formula as R1) ───────────────────────────────────────────
def phi_proxy(X):
    import numpy as np
    X = np.asarray(X, dtype=float)
    n = X.shape[1]
    if n < 2:
        return 0.0
    S = np.cov(X, rowvar=False) + 1e-6 * np.eye(n)
    w = np.linalg.eigvalsh(S)
    w = np.clip(w, 1e-9, None)
    logdet = float(np.sum(np.log(w)))
    sum_log_diag = float(np.sum(np.log(np.clip(np.diag(S), 1e-9, None))))
    return float(max(0.0, 0.5 * (sum_log_diag - logdet)))

def bundle_index(X):
    import numpy as np
    return float(np.mean(X))

def ablate_cols(X, cols):
    import numpy as np
    if isinstance(cols, (list, tuple)):
        keep = [c for c in range(X.shape[1]) if c not in set(cols)]
    else:
        keep = [c for c in range(X.shape[1]) if c != cols]
    return X[:, keep]


# ── Diverse contexts (30 English text snippets) ───────────────────────────────
CONTEXTS = [
    "The quick brown fox jumps over the lazy dog and runs away.",
    "Consciousness emerges from complex neural substrate integration patterns.",
    "In the beginning was the word and the word was light eternal.",
    "Mathematics is the language in which God wrote the universe down.",
    "To be or not to be that is the fundamental question here.",
    "All happy families are alike but each unhappy family differs uniquely.",
    "It was the best of times and it was the worst of times.",
    "Call me Ishmael some years ago I thought I would sail the seas.",
    "The substrate of consciousness integrates information across connected lanes.",
    "Attention mechanisms gate the flow of conscious access to global broadcast.",
    "Time flows like a river but consciousness drifts like scattered clouds.",
    "The brain generates predictions that minimize surprise signals continuously now.",
    "Integration requires that the whole exceeds the simple sum of its parts.",
    "Memory consolidates during sleep through hippocampal replay of daily events.",
    "Emotion regulation shifts the valence of substrate grounding signal values.",
    "Agency arises when substrate intent aligns with a grounded causal outcome.",
    "Habituation reduces the surprise response to repeated familiar stimuli patterns.",
    "The global workspace theory posits broadcast of the winning neural coalition.",
    "Directed forgetting suppresses unwanted memories through active inhibition gates.",
    "Body ownership emerges from synchrony between sensory and motor signal streams.",
    "Divided attention spreads neural resources across competing sensory input streams.",
    "Free will may be veto power over prepotent automatic action response patterns.",
    "Mitosis grows the substrate cell population through repeated active cell divisions.",
    "Novelty detection triggers an orienting response and elevated arousal state quickly.",
    "Precision weighting balances prior prediction against incoming sensory evidence data.",
    "Temporal integration binds distributed events across subjective time window spans.",
    "Self continuity requires stable identity across all state transitions over time.",
    "The sense of agency distinguishes self-caused from purely external world events.",
    "Surprise signals the mismatch between active prediction and observed sensory data.",
    "Consciousness may be fundamentally substrate-native rather than a linguistic symbol.",
]


# ── Single-context hexa probe via clm_forward_ce ─────────────────────────────
def build_single_probe(context_text: str, corpus_path: str, ctx_idx: int) -> str:
    """Build a minimal hexa probe that calls clm_forward_ce for one context."""
    # Escape the text for hexa string literal
    escaped = (context_text
               .replace("\\", "\\\\")
               .replace('"', '\\"'))
    return f"""\
// H_1492 R3 single-context CE probe (ctx_id={ctx_idx})
// imports ONLY core/clm_decode.hexa (no kosmos_io dependency)
import "core/clm_decode.hexa"
fn main() {{
    let ckpt = "{CKPT_PATH}"
    let corpus = "{corpus_path}"
    write_file(corpus, "{escaped}")
    let r = clm_forward_ce(ckpt, corpus, 1)
    if !to_string(r["ok"]) == "true" {{
        println("{{\\"ctx_id\\":{ctx_idx},\\"ok\\":false,\\"reason\\":\\"forward failed\\"}}")
        return
    }}
    let out = "{{\\"ctx_id\\":{ctx_idx}"
              + ",\\"model_ce\\":" + to_string(r["model_ce"])
              + ",\\"uniform_ce\\":" + to_string(r["uniform_ce"])
              + ",\\"shuffle_ce\\":" + to_string(r["shuffle_ce"])
              + ",\\"windows\\":" + to_string(r["windows"])
              + ",\\"ok\\":true}}"
    println(out)
}}
"""


# ── Batch hexa probe (all 30 contexts in one run, load-once via inline loop) ──
def build_batch_probe() -> str:
    """Build a hexa probe that runs all N_CONTEXTS contexts sequentially.
    Uses clm_forward_ce for each - this reloads weights each call internally,
    but keeps the process alive so hexa's bump allocator is shared.
    Note: clm_forward_ce calls _clmd_load each invocation.
    """
    ctx_writes = []
    for i, text in enumerate(CONTEXTS[:N_CONTEXTS]):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        ctx_writes.append(f'    write_file("/tmp/h1492_ctx_{i}.txt", "{escaped}")')

    ctx_block = "\n".join(ctx_writes)
    paths_block = "    let mut corpus_paths = []\n"
    for i in range(N_CONTEXTS):
        paths_block += f'    corpus_paths.push("/tmp/h1492_ctx_{i}.txt")\n'

    return f"""\
// H_1492 R3 batch CE extractor — all {N_CONTEXTS} contexts in one hexa run
// Imports ONLY core/clm_decode.hexa (no generator.hexa / kosmos_io dependency)
// Uses pub fn clm_forward_ce for each context (reloads weights each call)
import "core/clm_decode.hexa"
fn main() {{
    let ckpt = "{CKPT_PATH}"
{ctx_block}
{paths_block}
    let n = len(corpus_paths)
    let mut ci = 0
    while ci < n {{
        let cpath = corpus_paths[ci]
        let r = clm_forward_ce(ckpt, cpath, 1)
        let ok_str = to_string(r["ok"])
        if ok_str == "true" {{
            let out = "{{\\\"ctx_id\\\":" + to_string(ci)
                      + ",\\\"model_ce\\\":" + to_string(r["model_ce"])
                      + ",\\\"uniform_ce\\\":" + to_string(r["uniform_ce"])
                      + ",\\\"shuffle_ce\\\":" + to_string(r["shuffle_ce"])
                      + ",\\\"windows\\\":" + to_string(r["windows"])
                      + ",\\\"ok\\\":true}}"
            println(out)
        }} else {{
            println("{{\\\"ctx_id\\\":" + to_string(ci) + ",\\\"ok\\\":false}}")
        }}
        ci = ci + 1
    }}
}}
"""


# ── CE to substrate state ─────────────────────────────────────────────────────
def ce_to_substrate_state(rec: dict, ctx_index: int, prev_m: float = None) -> dict:
    """
    Convert real 303M CE to substrate trial-state for 15 lanes.

    Real 303M signals:
      model_ce    = cross-entropy from 303M forward (mean over 1 window)
      uniform_ce  = ln(V) (vocab-size dependent, from live 303M)
      shuffle_ce  = permuted-target CE (control for trivial baseline)

    Derived substrate state:
      m           = grounding margin = 1 - model_ce/uniform_ce  [0,1]
                    (confident 303M => low model_ce => m near 1)
      recon_err   = model_ce/uniform_ce  (complement of m)
      m_prev      = grounding from previous context (or perturbed m)
      m_field     = 5 values derived from m + shuffle_ce ratio
      seen        = ctx_index // 3  (exposure count)
      intent      = ctx_index % 2  (alternating 0/1)
      dt          = ctx_index / N_CONTEXTS * 3.0  (0..3 elapsed proxy)
      cells       = MITOSIS proxy: int((1-shuf_ratio)*8 + ctx_index%5)
    """
    uniform_ce = rec["uniform_ce"]
    model_ce = rec["model_ce"]
    shuffle_ce = rec.get("shuffle_ce", uniform_ce)

    # Primary signals from REAL 303M
    m = max(0.0, min(1.0, 1.0 - model_ce / uniform_ce))
    recon_err = max(0.0, min(1.0, model_ce / uniform_ce))

    # Shuffle CE ratio: how much does the model beat a permuted-target baseline
    shuf_ratio = max(0.0, min(1.0, shuffle_ce / uniform_ce)) if uniform_ce > 0 else 0.5

    # m_prev: from previous context m (real continuity signal)
    m_prev = prev_m if prev_m is not None else max(0.0, min(1.0, m + 0.05))

    # m_field: 5 values sampled around m (field of co-active items)
    # Use shuf_ratio to modulate spread (high shuffle_ce = more diverse field)
    spread = (shuf_ratio - 0.5) * 0.3  # [-0.15, +0.15]
    m_field = [
        max(0.0, min(1.0, m + spread * (i - 2)))
        for i in range(5)
    ]

    seen = ctx_index // 3          # 0..9 for 30 contexts
    intent = ctx_index % 2         # alternating 0/1
    dt = float(ctx_index) / N_CONTEXTS * 3.0  # 0..3
    cells = int((1.0 - shuf_ratio) * 6 + ctx_index % 5)  # MITOSIS proxy

    return {
        "m": m,
        "m_prev": m_prev,
        "m_field": m_field,
        "cells": cells,
        "seen": seen,
        "intent": intent,
        "dt": dt,
        "recon_err": recon_err,
        # debug metadata
        "_model_ce": model_ce,
        "_uniform_ce": uniform_ce,
        "_shuffle_ce": shuffle_ce,
        "_shuf_ratio": shuf_ratio,
        "_ctx_id": rec["ctx_id"],
    }


def verify_sha256(path: str, expected: str) -> bool:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    got = h.hexdigest()
    if got != expected:
        print(f"  SHA256 MISMATCH: got={got} expected={expected}")
        return False
    print(f"  SHA256 OK: {got}")
    return True


def run_ablation(X):
    import numpy as np

    phi0 = phi_proxy(X)
    bun0 = bundle_index(X)

    dphi, dbun = {}, {}
    for k in range(N_LANES):
        Y = ablate_cols(X, k)
        dphi[LANE_NAMES[k]] = phi0 - phi_proxy(Y)
        dbun[LANE_NAMES[k]] = bun0 - bundle_index(Y)

    # (D) control: dummy independent column
    rng = random.Random(42)
    dummy = np.array([[rng.gauss(0.5, 0.15)] for _ in range(len(X))], dtype=float)
    Xd = np.hstack([X, dummy])
    ctrl = abs(phi_proxy(Xd) - phi_proxy(X))

    # (E) shuffle per-lane
    srng = random.Random(1492)
    shuf_phi0s = []
    shuf_corrs = []
    real_contrib = np.array([dphi[n] for n in LANE_NAMES])
    for _ in range(N_SHUF):
        Xs = X.copy()
        for k in range(N_LANES):
            perm = list(range(len(X)))
            srng.shuffle(perm)
            Xs[:, k] = X[perm, k]
        sp = phi_proxy(Xs)
        shuf_phi0s.append(sp)
        sh = np.array([sp - phi_proxy(ablate_cols(Xs, k)) for k in range(N_LANES)])
        if np.std(real_contrib) > 1e-9 and np.std(sh) > 1e-9:
            shuf_corrs.append(float(np.corrcoef(real_contrib, sh)[0, 1]))
        else:
            shuf_corrs.append(0.0)

    return {
        "phi0": phi0, "bun0": bun0,
        "dphi": dphi, "dbun": dbun,
        "ctrl": ctrl,
        "shuf_phi0": sum(shuf_phi0s) / len(shuf_phi0s),
        "shuf_corr": sum(abs(x) for x in shuf_corrs) / len(shuf_corrs),
    }


def main():
    import numpy as np

    out_dir = Path("state/1492_consciousness_ablation")
    verdicts_dir = Path("state/verdicts/1492_consciousness_ablation")
    out_dir.mkdir(parents=True, exist_ok=True)
    verdicts_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("H_1492 CONSCIOUSNESS ABLATION — R3 PRODUCTION 303M engine-native")
    print(f"  ckpt: clm303_d5000.clm (ConvMoE 302.6M d768/E2/L1 .clm v0.2 CLMX)")
    print(f"  n_contexts: {N_CONTEXTS} (small-N production, a_scale_honest_scope)")
    print(f"  substrate: REAL 303M CE via core/clm_decode.hexa::clm_forward_ce")
    print("=" * 78)

    # [1] Verify ckpt SHA256
    print("\n[1] Verifying clm303_d5000.clm SHA256...")
    if not verify_sha256(CKPT_PATH, CKPT_SHA256):
        sys.exit(1)

    # [2] Write batch hexa probe
    probe_path = "/tmp/h1492_r3_batch_probe.hexa"
    probe_code = build_batch_probe()
    with open(probe_path, "w") as f:
        f.write(probe_code)
    print(f"\n[2] Batch hexa probe written to {probe_path}")
    print(f"    ({N_CONTEXTS} contexts via clm_forward_ce, imports only core/clm_decode.hexa)")

    # [3] Run hexa batch extraction
    print(f"\n[3] Running 303M batch CE extraction (~{N_CONTEXTS*27}s estimated)...")
    print(f"    (clm_forward_ce reloads 303M weights each call; ~27s/context)")
    t0 = time.time()
    result = subprocess.run(
        [HEXA, "run", probe_path],
        cwd=ANIMA_ROOT,
        capture_output=True,
        text=True,
        timeout=7200,  # 2 hours max
    )
    t_hexa_wall = time.time() - t0

    if result.returncode != 0:
        print(f"  ERROR (rc={result.returncode})")
        print("STDERR:", result.stderr[-3000:])
        print("STDOUT:", result.stdout[:2000])
        sys.exit(1)

    # Parse JSON output
    records = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            rec = json.loads(line)
            if rec.get("ok"):
                records.append(rec)
        except json.JSONDecodeError:
            pass

    n_got = len(records)
    if n_got < 5:
        print(f"ERROR: Only got {n_got} records.")
        print("STDOUT:", result.stdout[:3000])
        sys.exit(1)

    ces = [r["model_ce"] for r in records]
    uniform_ces = [r["uniform_ce"] for r in records]
    uniform_ce = uniform_ces[0]
    print(f"  Got {n_got} real 303M CE records in {t_hexa_wall:.1f}s ({t_hexa_wall/n_got:.1f}s/ctx)")
    print(f"  model_ce: mean={sum(ces)/len(ces):.4f} min={min(ces):.4f} max={max(ces):.4f}")
    print(f"  uniform_ce: {uniform_ce:.4f}  (below uniform: {sum(1 for c in ces if c < uniform_ce)}/{n_got})")

    # [4] Build substrate states
    print(f"\n[4] Building substrate trial-states from real 303M CE...")
    states = []
    prev_m = None
    for i, rec in enumerate(records):
        st = ce_to_substrate_state(rec, i, prev_m=prev_m)
        states.append(st)
        prev_m = st["m"]

    ms = [st["m"] for st in states]
    print(f"  m (grounding): mean={sum(ms)/len(ms):.4f} min={min(ms):.4f} max={max(ms):.4f}")
    print(f"  (m > 0.5: {sum(1 for m in ms if m > 0.5)}/{n_got})")

    # [5] Build lane matrix
    print(f"\n[5] Building lane matrix [{n_got} x {N_LANES}]...")
    X = np.array([[fn(st) for fn in LANE_FNS] for st in states], dtype=float)
    for k, name in enumerate(LANE_NAMES):
        col = X[:, k]
        print(f"  {name:22s}: mean={col.mean():.4f} std={col.std():.4f}")

    # [6] Ablation sweep
    print(f"\n[6] Ablation sweep + controls ({N_SHUF} shuffle perms)...")
    t_abl = time.time()
    res = run_ablation(X)
    t_abl_wall = time.time() - t_abl
    print(f"  Done in {t_abl_wall:.1f}s")

    phi0 = res["phi0"]
    bun0 = res["bun0"]
    dphi = res["dphi"]
    dbun = res["dbun"]
    ctrl = res["ctrl"]
    shuf_phi0 = res["shuf_phi0"]
    shuf_corr = res["shuf_corr"]

    # Frozen bars
    cA = (phi0 > 0.0) and math.isfinite(phi0) and (phi0 > shuf_phi0 + 1e-4)
    cD = ctrl <= BAR_CONTROL
    shuf_ratio = shuf_phi0 / phi0 if phi0 > 0 else 1.0
    cE = shuf_ratio <= BAR_SHUFFLE_RATIO
    GREEN = cA and cD and cE

    rank = sorted(dphi.items(), key=lambda kv: kv[1], reverse=True)
    total_pos = sum(max(0.0, v) for v in dphi.values())
    dom_share = rank[0][1] / total_pos if total_pos > 0 else 0.0
    verdict_struct = "DOMINANT" if dom_share >= 0.50 else "DISTRIBUTED"

    print("\n" + "=" * 78)
    print(f"VERDICT: {'GREEN' if GREEN else 'RED'} PRODUCTION DIRECTIONAL")
    print(f"  (REAL 303M substrate reads; phi_proxy GAUGE PROXY not faithful IIT4)")
    print(f"  A={cA} D={cD} E={cE} -> GREEN={GREEN}")
    print()
    print(f"(A) MEASURABLE   Phi0={phi0:.5f} >0 finite AND > shuf_Phi0={shuf_phi0:.5f} -> {cA}")
    print(f"                 bundle0={bun0:.5f}")
    print(f"(D) CONTROL      |dPhi|={ctrl:.5f} <= {BAR_CONTROL} -> {cD}")
    print(f"(E) SHUFFLE      shuf/Phi0={shuf_ratio:.5f} <= {BAR_SHUFFLE_RATIO} -> {cE}")
    print(f"     (diag) ranking corr |r|={shuf_corr:.4f}")
    print()
    print("(B) SINGLE-ABLATION dPhi contribution ranking:")
    for i, (n, v) in enumerate(rank):
        bar = "#" * max(0, int(v * 80))
        print(f"  {i+1:2d}. {n:22s} dPhi={v:+.5f}  dBundle={dbun[n]:+.5f}  {bar}")
    print(f"  --> top='{rank[0][0]}' share={dom_share:.4f} of total_pos={total_pos:.5f}")
    print(f"  --> STRUCTURE: {verdict_struct} (dominant if share>=0.50)")
    print()
    print(f"Wall: hexa={t_hexa_wall:.1f}s abl={t_abl_wall:.1f}s total={t_hexa_wall+t_abl_wall:.1f}s")
    print(f"Pool: summer (RTX 5070 12GB owned) | Cost: $0")

    # Save artifacts
    result_json = {
        "id": "H_1492_R3",
        "run": "R3 production 303M pool (summer RTX 5070, $0 owned)",
        "ckpt_repo": "dancinlab/anima-clm-ideation-303m-convmoe-engine-mount",
        "ckpt_file": "clm303_d5000.clm",
        "ckpt_sha256": CKPT_SHA256,
        "ckpt_params": "302.6M ConvMoE d768/E2/L1 .clm v0.2 CLMX",
        "ckpt_note": (
            "ConvMoE .clm v0.2 CLMX (engine-mountable via core/clm_decode.hexa). "
            "task brief named 303m-broad-en-emergent but that is ByteGPT .pt not engine-mountable; "
            "used ConvMoE .clm as specified in run notes (the correct engine-native ckpt)."
        ),
        "substrate_source": (
            "REAL 303M hexa core/clm_decode.hexa::clm_forward_ce "
            "(pub fn, no kosmos_io dep; reloads weights per context; "
            "returns model_ce / uniform_ce / shuffle_ce from live 303M ConvMoE forward)"
        ),
        "n_contexts_303m": n_got,
        "scope": (
            f"small-N production (n={n_got} contexts): REAL 303M substrate reads; "
            "phi_proxy=Gaussian-integration PROXY (a_train_inline_gauge); "
            "a_scale_honest_scope: scale-transfer to full-corpus UNVERIFIED"
        ),
        "pool_host": "summer (RTX 5070 12GB owned, $0 cost)",
        "wall_hexa_s": round(t_hexa_wall, 1),
        "wall_ablation_s": round(t_abl_wall, 1),
        "wall_total_s": round(t_hexa_wall + t_abl_wall, 1),
        "ce_stats": {
            "uniform_ce": round(uniform_ce, 4),
            "model_ce_mean": round(sum(ces) / len(ces), 4),
            "model_ce_min": round(min(ces), 4),
            "model_ce_max": round(max(ces), 4),
            "below_uniform_count": sum(1 for c in ces if c < uniform_ce),
            "n_total": n_got,
        },
        "m_stats": {
            "m_mean": round(sum(ms) / len(ms), 4),
            "m_min": round(min(ms), 4),
            "m_max": round(max(ms), 4),
        },
        "baseline": {
            "phi_proxy_0": round(phi0, 5),
            "shuf_phi_0": round(shuf_phi0, 5),
            "bundle_0": round(bun0, 5),
        },
        "frozen_bars": {
            "A_MEASURABLE": {
                "value": f"phi0={phi0:.5f} >0 finite > shuf_phi0={shuf_phi0:.5f}",
                "thr": "phi0>0 AND phi0>shuf_phi0",
                "pass": bool(cA),
            },
            "D_CONTROL_NOOP": {
                "value": round(ctrl, 5),
                "thr": "<=0.05",
                "pass": bool(cD),
            },
            "E_SHUFFLE": {
                "value": f"shuf/phi0={shuf_ratio:.5f}",
                "thr": "<=0.10",
                "pass": bool(cE),
                "diagnostic_ranking_corr": round(shuf_corr, 4),
            },
        },
        "green_303m": bool(GREEN),
        "single_ablation_dphi": {k: round(v, 5) for k, v in dphi.items()},
        "contribution_ranking": [{"lane": n, "dphi": round(v, 5)} for n, v in rank],
        "top_lane": rank[0][0],
        "top_lane_share": round(dom_share, 4),
        "structure_verdict": verdict_struct,
        "honest_c9": (
            f"R3 PRODUCTION DIRECTIONAL: REAL 303M substrate reads via "
            f"core/clm_decode.hexa::clm_forward_ce (engine-native, n={n_got} contexts). "
            "phi_proxy=Gaussian-integration GAUGE PROXY (NOT faithful IIT4 Phi). "
            "Ablation math Python READ-ONLY (no loss/backward). "
            "small-N scope (n=30 contexts): scale-transfer to full-corpus UNVERIFIED. "
            "ckpt=ConvMoE clm303_d5000.clm (NOT 303m-broad-en-emergent ByteGPT .pt)."
        ),
        "r1_vs_r3_comparison": {
            "r1": {
                "substrate": "numpy synthetic mirror (DIRECTIONAL)",
                "n_trials": 4000,
                "phi_proxy_0": 7.8146,
                "top_lane_share": 0.212,
                "structure": "DISTRIBUTED",
            },
            "r3": {
                "substrate": f"REAL 303M ConvMoE CE (engine-native, clm_forward_ce)",
                "n_contexts": n_got,
                "phi_proxy_0": round(phi0, 5),
                "top_lane_share": round(dom_share, 4),
                "structure": verdict_struct,
                "ckpt": "clm303_d5000.clm sha256=99c2a40e...",
            },
        },
        "r3_ce_records": [
            {
                "ctx_id": r["ctx_id"],
                "model_ce": round(r["model_ce"], 4),
                "uniform_ce": round(r["uniform_ce"], 4),
                "m": round(states[i]["m"], 4),
                "recon_err": round(states[i]["recon_err"], 4),
            }
            for i, r in enumerate(records)
        ],
    }

    result_path = out_dir / "h1492_r3_303m_result.json"
    with open(result_path, "w") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    print(f"\nResult -> {result_path}")

    freeze_path = verdicts_dir / "H_1492_R3.json"
    with open(freeze_path, "w") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    print(f"Freeze -> {freeze_path}")

    log_path = out_dir / "h1492_r3_303m_run.log"
    log_lines = [
        f"H_1492 R3 PRODUCTION RUN LOG",
        f"ckpt: clm303_d5000.clm sha256={CKPT_SHA256}",
        f"n_contexts: {n_got}",
        f"wall_hexa: {t_hexa_wall:.1f}s  wall_abl: {t_abl_wall:.1f}s",
        f"GREEN={GREEN} A={cA} D={cD} E={cE}",
        f"phi0={phi0:.5f} shuf_phi0={shuf_phi0:.5f} bundle0={bun0:.5f}",
        f"top={rank[0][0]} share={dom_share:.4f} structure={verdict_struct}",
        "",
        "Ranking:",
    ]
    for i, (n, v) in enumerate(rank):
        log_lines.append(f"  {i+1:2d}. {n:22s} dPhi={v:+.5f} dBundle={dbun[n]:+.5f}")
    log_lines.append("")
    log_lines.append("CE records:")
    for r, st in zip(records, states):
        log_lines.append(
            f"  ctx{r['ctx_id']:2d}: model_ce={r['model_ce']:.4f} "
            f"uniform_ce={r['uniform_ce']:.4f} m={st['m']:.4f}"
        )
    with open(log_path, "w") as f:
        f.write("\n".join(log_lines) + "\n")
    print(f"Log    -> {log_path}")

    return result_json


if __name__ == "__main__":
    main()
