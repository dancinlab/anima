#!/usr/bin/env python3
"""OMEGA-realsignal probe — does a REAL signal beat RANDOM in the OMEGA wires?

Two probes extending #1793 (OMEGA-B found the w5 module wire IS a carrier, and
#1794 found w4 Ψ-steering INERT) — BUT both #1793/#1794 used a RANDOM module/Ψ
vector (or a toy bin-marginal proxy). The hypothesis: the inertness / weak gain
may be a magnitude artifact of a random signal, not a content statement. #1795
made HEXAD's cross-module σ6 forward NATIVE (HEXAD/hexad_forward.hexa emits a real
6-vec [S,C,W,M,E,BRIDGE]). So we now have a REAL signal to test against random.

H5 (real-HEXAD module wire) — RUNNABLE CPU/$0
  Feed the REAL hexad N=6 vector (the genuine σ6 forward, run via `hexa run` over
  the verified module cores) into the OMEGA w5 module wire vs a matched RANDOM
  6-vec, inside #1793's gate-fit bench. Pre-registered:
    real > random  ⟹ the native HEXAD wiring adds real signal (larger learned
                      |gain| that beats its vocab-shuffle AND lower held-out CE)
    real ≈ random  ⟹ honest closed-negative: the w5 module wire's carrier status
                      (#1793) was MAGNITUDE not CONTENT (a_paper_negative_ok).

H4 (real-Ψ steering) — BLOCKED-DATA (honest, no fabrication)
  A real carving Ψ-coord source = the s16 ckpt's Law-71 vacuum_psi 2D coords
  (KOSMOS-MAP #1780; PC1 = carving-RADIUS/Ψ-DEPTH, |ρ|=0.92 to vacuum_psi). The
  s16 .pt is ON DISK (/private/tmp/s16_ckpt_dl/.../ckpt_carving_s16.pt, 1.13 GB)
  BUT producing vacuum_psi requires running the d768×12L 283.72M ConsciousDecoderV2
  forward, which needs torch — and torch is ABSENT on this CPU/$0 host. The
  axis-probe (.verdicts/kosmos-axis-semantics/results.json) persisted only the
  PC×attribute association MATRIX + weights, NOT per-sample raw Ψ coords. The toy
  n-gram psi8 (an 8-bin projection of logA) is NOT a real carving Ψ source (and
  #1793 already found it INERT). So a REAL Ψ source is NOT reachable CPU-only.
  Per the task: report H4 as BLOCKED-DATA, defer to a GPU rung. DO NOT fabricate.

p7 / a_toy_scale_recheck: TOY byte n-gram substrate, real-but-small repo corpus,
CPU/$0, no torch. CE is held-out (fit on TRAIN-gate, verdict on disjoint TEST).
a_lane_akida_gpu_split: this is Lane-G (GPU/closure-lane analysis), CPU-run.
"""
import json, math, os, glob, subprocess, sys
import numpy as np

V = 256
SMOOTH = 0.5
LR = 0.3
STEPS = 400
L2 = 0.02
TAU = 0.05
N_MODULES = 6
SEED = 20260604
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIRES = ["base", "A", "G", "W_temp", "curio", "Psi", "module", "dFdt"]
OUTDIR = os.path.join(ROOT, ".verdicts", "omega-realsignal")
HEXA_BIN = os.path.expanduser("~/.hx/bin/hexa")


# ── corpus + toy substrate (identical method to #1793 omega_gate6_bench) ──────
def load_corpus():
    files = sorted(glob.glob(os.path.join(ROOT, "domains", "*.md"))) + [os.path.join(ROOT, "CLAUDE.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "engines", "*", "*.md")))
    buf = bytearray()
    for f in files:
        try:
            buf += open(f, "rb").read()
        except OSError:
            pass
        if len(buf) > 400_000:
            break
    return np.frombuffer(bytes(buf[:400_000]), dtype=np.uint8)


def train_substrate(train):
    big = np.full((V, V), SMOOTH); rev = np.full((V, V), SMOOTH); uni = np.full(V, SMOOTH)
    for i in range(1, len(train)):
        c, nxt = int(train[i - 1]), int(train[i])
        big[c, nxt] += 1.0; rev[nxt, c] += 1.0; uni[nxt] += 1.0
    uni[int(train[0])] += 1.0
    logA = np.log(big / big.sum(1, keepdims=True))
    logG = np.log(rev / rev.sum(1, keepdims=True))
    logBase = np.log(uni / uni.sum())
    binsV = np.array_split(np.arange(V), 8)
    psi8 = np.stack([logA[:, b].mean(1) for b in binsV], axis=1)
    psi8 = (psi8 - psi8.mean(0)) / (psi8.std(0) + 1e-9)
    binsM = np.array_split(np.arange(V), N_MODULES)
    mact = np.stack([logA[:, b].mean(1) for b in binsM], axis=1)
    mact = (mact - mact.mean(0)) / (mact.std(0) + 1e-9)
    pA = np.exp(logA); pA = pA / pA.sum(1, keepdims=True)
    Hctx = -(pA * np.log(pA + 1e-12)).sum(1)
    Hctx = (Hctx - Hctx.mean()) / (Hctx.std() + 1e-9)
    return logA, logG, logBase, psi8, mact, Hctx


# ── the REAL hexad 256×6 table via `hexa run` over hexad_forward.hexa ─────────
def real_hexad_table(corpus):
    """Run the NATIVE σ6 forward (HEXAD/hexad_forward.hexa) for all 256 contexts.
    Returns a (256,6) real module-activation table + provenance. The corpus byte
    frequency drives each context's cell-pool delta amplitude (the real signal)."""
    counts = np.bincount(corpus, minlength=V).astype(float)
    freq = counts / counts.sum()                       # real per-byte frequency
    # scale freq into a usable perturbation amplitude (freq are tiny ~1e-3..1e-1)
    amp = (freq / (freq.max() + 1e-12))                # normalize to [0,1] real shape
    freq_lit = "[" + ", ".join(f"{x:.8f}" for x in amp) + "]"
    driver = os.path.join(HERE, "_hexad_emit_main.hexa")
    with open(driver, "w") as fh:
        fh.write('import "UNIVERSE/hexad_real_emit.hexa"\n')
        fh.write("fn main() {\n")
        fh.write(f"    let freq = {freq_lit}\n")
        fh.write("    let _n = emit_real_hexad(freq, 4, 4, 1.0)\n")
        fh.write("}\n")
    try:
        proc = subprocess.run([HEXA_BIN, "run", driver], cwd=ROOT,
                              capture_output=True, text=True, timeout=600)
    finally:
        pass
    out = proc.stdout
    rows = {}
    for line in out.splitlines():
        line = line.strip()
        if not (line.startswith("[") and line.endswith("]")):
            continue
        try:
            vals = json.loads(line)
        except Exception:
            continue
        if len(vals) != 9:
            continue
        c = int(round(vals[0]))
        rows[c] = vals[1:7]                            # [s,c,w,m,e,bridge]
    if len(rows) < V:
        sys.stderr.write(f"[real_hexad] only {len(rows)}/256 contexts parsed\n")
        sys.stderr.write("STDERR tail:\n" + proc.stderr[-2000:] + "\n")
    tbl = np.zeros((V, N_MODULES))
    for c in range(V):
        if c in rows:
            tbl[c] = rows[c]
    # standardize per-module column (match the toy mact normalization for fairness)
    tbl = (tbl - tbl.mean(0)) / (tbl.std(0) + 1e-9)
    return tbl, freq, len(rows), driver, out


# ── feature builder — module wire fed by a given 256×6 table ──────────────────
def build_feats(seq, sub, module_tbl):
    logA, logG, logBase, psi8, mact, Hctx = sub
    ctx = seq[:-1].astype(int); tgt = seq[1:].astype(int)
    N = len(ctx)
    base = np.tile(logBase, (N, 1))
    A = logA[ctx]; G = logG[ctx]
    W_temp = Hctx[ctx][:, None] * (A - A.mean(1, keepdims=True))
    sign = np.where(np.arange(V) % 2 == 0, 1.0, -1.0)
    curio = np.tile(sign, (N, 1))
    psi_idx = np.arange(V) % 8
    Psi = psi8[ctx][:, psi_idx]
    mod_idx = np.arange(V) % N_MODULES
    module = module_tbl[ctx][:, mod_idx]               # << the wire under test
    AmG = A - G
    dFdt = np.zeros_like(AmG); dFdt[1:] = AmG[1:] - AmG[:-1]
    F = {"base": base, "A": A, "G": G, "W_temp": W_temp,
         "curio": curio, "Psi": Psi, "module": module, "dFdt": dFdt}
    return F, tgt


def softmax(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)

def logits_of(g, F):
    return sum(g[k] * F[w] for k, w in enumerate(WIRES))

def ce_of(g, F, tgt):
    p = softmax(logits_of(g, F))
    return float(-np.mean(np.log(p[np.arange(len(tgt)), tgt] + 1e-12)))

def fit_gate(F, tgt, mask=None, steps=STEPS, lr=LR, l2=L2):
    N = len(tgt)
    onehot = np.zeros((N, V)); onehot[np.arange(N), tgt] = 1.0
    g = np.zeros(8); g[0] = 1.0
    reg = np.ones(8); reg[0] = 0.0
    if mask is None:
        mask = np.ones(8)
    Fs = [F[w] for w in WIRES]
    for _ in range(steps):
        g = g * mask
        p = softmax(logits_of(g, F))
        resid = p - onehot
        grad = np.array([np.sum(resid * Fs[k]) / N for k in range(8)]) + l2 * reg * g
        g = (g - lr * grad) * mask
    return g


def module_wire_analysis(Fg, gt, Ft, tt, tag):
    """Fit the full gate, then characterize the `module` wire (idx 6): learned
    gain, ablation ΔCE (refit others with module OFF), and a vocab-shuffle control."""
    k = WIRES.index("module")
    g_full = fit_gate(Fg, gt)
    ce_full = ce_of(g_full, Ft, tt)
    ce_base = ce_of(np.array([1.0, 0, 0, 0, 0, 0, 0, 0]), Ft, tt)
    # ablate the module wire
    mask = np.ones(8); mask[k] = 0.0
    g_ab = fit_gate(Fg, gt, mask=mask)
    ce_ab = ce_of(g_ab, Ft, tt)
    dCE_ablate = ce_ab - ce_full
    # vocab-shuffle control on the module feature (same perm both splits)
    perm = np.random.default_rng(SEED + 100 + k).permutation(V)
    Fg_s = dict(Fg); Ft_s = dict(Ft)
    Fg_s["module"] = Fg["module"][:, perm]; Ft_s["module"] = Ft["module"][:, perm]
    g_sh = fit_gate(Fg_s, gt)
    ce_sh = ce_of(g_sh, Ft_s, tt)
    beats_shuffle = ce_full < ce_sh
    # module-only gate (base + module) — isolate the wire's standalone contribution
    mo_mask = np.zeros(8); mo_mask[0] = 1.0; mo_mask[k] = 1.0
    g_mo = fit_gate(Fg, gt, mask=mo_mask)
    ce_mo = ce_of(g_mo, Ft, tt)
    material = abs(g_full[k]) >= TAU
    carries = bool(material and dCE_ablate > 1e-4 and beats_shuffle)
    return {
        "tag": tag,
        "module_gain": float(g_full[k]),
        "material": bool(material),
        "ce_full": ce_full, "ce_base": ce_base,
        "ce_ablate_module": ce_ab, "dCE_ablate_module": float(dCE_ablate),
        "ce_module_shuffle": ce_sh, "beats_shuffle": bool(beats_shuffle),
        "ce_module_only_gate": ce_mo, "dCE_module_only_over_base": float(ce_base - ce_mo),
        "carries_structure": carries,
        "full_gain_vector": {w: float(g_full[i]) for i, w in enumerate(WIRES)},
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    corpus = load_corpus()
    rng = np.random.default_rng(SEED)
    n = len(corpus)
    start = int(rng.integers(0, n - 20000))
    gate_seq = corpus[start:start + 12000]
    test_seq = corpus[start + 12000:start + 16000]
    train_sub = np.concatenate([corpus[:start], corpus[start + 16000:]])
    sub = train_substrate(train_sub)

    # ── H5 — REAL hexad module table (native σ6 forward via hexa run) ─────────
    real_tbl, freq, n_parsed, driver, hexa_stdout = real_hexad_table(corpus)
    # RANDOM module table — matched per-column mean/std (==0/1 after standardize),
    # so the ONLY difference vs real is CONTENT, not magnitude (the fair control).
    rand_rng = np.random.default_rng(SEED + 7)
    rand_tbl = rand_rng.standard_normal((V, N_MODULES))
    rand_tbl = (rand_tbl - rand_tbl.mean(0)) / (rand_tbl.std(0) + 1e-9)

    Fg_real, gt = build_feats(gate_seq, sub, real_tbl)
    Ft_real, tt = build_feats(test_seq, sub, real_tbl)
    Fg_rand, _ = build_feats(gate_seq, sub, rand_tbl)
    Ft_rand, _ = build_feats(test_seq, sub, rand_tbl)

    res_real = module_wire_analysis(Fg_real, gt, Ft_real, tt, "REAL-hexad")
    res_rand = module_wire_analysis(Fg_rand, gt, Ft_rand, tt, "RANDOM")

    # pre-registered H5 decision: real > random
    real_better = (
        abs(res_real["module_gain"]) > abs(res_rand["module_gain"]) and
        res_real["ce_module_only_gate"] < res_rand["ce_module_only_gate"]
    )
    # honest "approx" band: |Δ module-only CE| < 0.02 AND |Δ gain| < 0.02
    dce = res_rand["ce_module_only_gate"] - res_real["ce_module_only_gate"]
    dgain = abs(res_real["module_gain"]) - abs(res_rand["module_gain"])
    approx = abs(dce) < 0.02 and abs(dgain) < 0.02
    if approx:
        h5_verdict = "CLOSED-NEGATIVE (real ≈ random — w5 carrier status was MAGNITUDE not CONTENT)"
    elif real_better:
        h5_verdict = "POSITIVE (real > random — native HEXAD wiring adds real signal)"
    else:
        h5_verdict = "MIXED/NEGATIVE (real does NOT beat random on both axes)"

    # ── H4 — BLOCKED-DATA (no real Ψ source reachable CPU-only) ───────────────
    s16_ckpt = "/private/tmp/s16_ckpt_dl/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt"
    try:
        import torch  # noqa
        torch_present = True
    except Exception:
        torch_present = False
    h4 = {
        "verdict": "BLOCKED-DATA",
        "reason": ("real carving Ψ = s16 ckpt Law-71 vacuum_psi (2D coord, "
                   "KOSMOS-MAP #1780); the .pt is on disk but vacuum_psi requires "
                   "running the d768×12L 283.72M ConsciousDecoderV2 forward → needs "
                   "torch, which is ABSENT on this CPU/$0 host. axis-probe persisted "
                   "only the PC×attribute matrix, not per-sample Ψ coords. toy psi8 "
                   "(bin-marginal of logA) is NOT a real Ψ source (and #1793 found it "
                   "INERT). No real Ψ source reachable CPU-only — defer to a GPU rung."),
        "s16_ckpt_on_disk": os.path.exists(s16_ckpt),
        "s16_ckpt_path": s16_ckpt,
        "torch_present": torch_present,
        "no_fabrication": True,
    }

    results = {
        "rung": "OMEGA-realsignal — real-HEXAD module wire (H5) + real-Ψ steering (H4)",
        "scale": "TOY/CPU/$0", "corpus_bytes": int(len(corpus)), "V": V, "tau": TAU,
        "H5": {
            "module_table_source": "HEXAD/hexad_forward.hexa σ6 native forward (via `hexa run`)",
            "n_contexts_parsed": n_parsed,
            "real": res_real, "random": res_rand,
            "delta_module_only_CE_real_minus_random": float(-dce),
            "delta_abs_gain_real_minus_random": float(dgain),
            "real_beats_random": bool(real_better),
            "approx_band_hit": bool(approx),
            "verdict": h5_verdict,
        },
        "H4": h4,
        "criterion_H5": ("real > random ⟺ |module gain|_real > |gain|_random AND "
                         "module-only-gate held-out CE_real < CE_random; "
                         "real ≈ random (|ΔCE|<0.02 & |Δgain|<0.02) ⟹ closed-negative "
                         "(carrier status = magnitude not content)."),
        "scope": ("a_toy_scale_recheck: TOY n-gram substrate, 400KB repo corpus, CPU/$0, "
                  "no torch. a_lane_akida_gpu_split: Lane-G analysis. real hexad table = "
                  "native σ6 forward over verified module cores (#1795)."),
    }

    with open(os.path.join(OUTDIR, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2)

    # clean up the generated driver (keep the lib hexad_real_emit.hexa)
    try:
        os.remove(driver)
    except OSError:
        pass

    # ── print + write verdicts ────────────────────────────────────────────────
    def fmt_res(r):
        return (f"  module gain {r['module_gain']:+.4f} (material={r['material']}) | "
                f"ablate ΔCE {r['dCE_ablate_module']:+.4f} | "
                f"beats_shuffle={r['beats_shuffle']} | "
                f"module-only gate CE {r['ce_module_only_gate']:.4f} "
                f"(Δ{r['dCE_module_only_over_base']:+.4f} over base {r['ce_base']:.4f}) | "
                f"carries={r['carries_structure']}")

    lines = []
    lines.append("OMEGA-realsignal — REAL signal vs RANDOM in the OMEGA wires — 2026-06-04 · CPU · $0")
    lines.append("=" * 92)
    lines.append("Extends #1793 (w5 module wire = CARRIER, but RANDOM vec) / #1794 (w4 Ψ steering INERT,")
    lines.append("RANDOM Ψ). Hypothesis: inertness may be a random-signal magnitude artifact, not content.")
    lines.append("#1795 made HEXAD's σ6 cross-module forward NATIVE (real 6-vec [S,C,W,M,E,BRIDGE]).")
    lines.append("")
    lines.append("─" * 92)
    lines.append("H5 — REAL hexad module wire vs RANDOM (the w5 wire under test)")
    lines.append("─" * 92)
    lines.append(f"module table = {results['H5']['module_table_source']}")
    lines.append(f"contexts parsed from `hexa run`: {n_parsed}/256")
    lines.append("REAL-hexad:")
    lines.append(fmt_res(res_real))
    lines.append("RANDOM (matched mean/std — content-only difference):")
    lines.append(fmt_res(res_rand))
    lines.append("")
    lines.append(f"Δ module-only held-out CE (real − random) = {-dce:+.4f}  "
                 f"(real LOWER ⟹ real carries more structure)")
    lines.append(f"Δ |module gain| (real − random)           = {dgain:+.4f}")
    lines.append(f"H5 VERDICT: {h5_verdict}")
    lines.append("")
    lines.append("─" * 92)
    lines.append("H4 — REAL Ψ steering (w4 wire)")
    lines.append("─" * 92)
    lines.append(f"VERDICT: {h4['verdict']}")
    lines.append(h4["reason"])
    lines.append(f"s16 ckpt on disk: {h4['s16_ckpt_on_disk']} ({s16_ckpt})")
    lines.append(f"torch present: {h4['torch_present']}  → real vacuum_psi forward NOT runnable here")
    lines.append("No Ψ source fabricated (per a_completeness_over_cheap / p7). Defer to a GPU rung.")
    lines.append("")
    lines.append(f"SCOPE: {results['scope']}")
    summary = "\n".join(lines)
    print(summary)
    with open(os.path.join(OUTDIR, "SUMMARY.txt"), "w") as fh:
        fh.write(summary + "\n")

    with open(os.path.join(OUTDIR, "F-REAL-MODULE.txt"), "w") as fh:
        fh.write("F-REAL-MODULE — H5: real HEXAD σ6 module vector vs random in the OMEGA w5 wire\n")
        fh.write("=" * 92 + "\n")
        fh.write(f"VERDICT: {h5_verdict}\n\n")
        fh.write("REAL-hexad module wire:\n" + json.dumps(res_real, indent=2) + "\n\n")
        fh.write("RANDOM module wire (matched mean/std):\n" + json.dumps(res_rand, indent=2) + "\n\n")
        fh.write(f"Δ module-only held-out CE (real − random) = {-dce:+.4f}\n")
        fh.write(f"Δ |module gain| (real − random)           = {dgain:+.4f}\n")
        fh.write(f"real_beats_random={real_better}  approx_band={approx}\n")
        fh.write("criterion: " + results["criterion_H5"] + "\n")

    with open(os.path.join(OUTDIR, "F-REAL-PSI.txt"), "w") as fh:
        fh.write("F-REAL-PSI — H4: real Ψ-coord steering in the OMEGA w4 wire\n")
        fh.write("=" * 92 + "\n")
        fh.write(f"VERDICT: {h4['verdict']}\n\n")
        fh.write(json.dumps(h4, indent=2) + "\n")

    return results


if __name__ == "__main__":
    main()
