#!/usr/bin/env python3
"""H_008 G-1.5 — controls-first BAND-EXISTENCE pre-run ($0 cash, local MPS, ~1.5h/phase).

DESIGN_fable5_seed.md §5. The trained-control-ceiling gate (the fix mech-5/H_007 lacked) made structural:
before ANY mechanism arm, train ONLY the zero-mechanism controls at TARGET scale (d=384) across the answer
budget B(k), and require a budget k* where the compute-matched control's held-out f2 d_acc sits stably in
the band [0.60, 0.80] across seeds — else H_008 CLOSES near-$0 (K1) and the campaign stays CONCLUDED.

No mechanism arm (no A-tug). Controls only:
  C-dup   head-G = forward surface (duplicate)         the compute-matched control whose ceiling gates F1
  C-scaf  head-G present, λ_G = 0 (pure forward)        the not-free floor / L2 arm
  C-shuf  head-G = swap of a DIFFERENT sentence         the placebo (K1b: if ≤0.80 fails, generic-aux story)

The budget knob: items in B(k) train seq = surf + ans (head-A CE covers the answer suffix); items NOT in
B(k) are answer-TRUNCATED (seq = surf only, forward LM). head-G's aux is NEVER rationed. Everything else
(model, steps, init, sampling stream) byte-identical across k and arm. Metric = head-A forced-choice
free-slot d_acc on SWAP-XOR-B f2 (heads dropped at eval).

Phases:  --phase a  (seed0 C-dup @ k∈{24,96,192,384} — first kill)
         --phase b  (seed1 C-dup @ a chosen k set — cross-seed stability)
         --phase c  (C-scaf + C-shuf @ k* — contrast pricing)
         --tiny     (d=48, few steps, 1 job — plumbing)
Writes/appends g1_5_result.json.

Run:  python3 state/h008_supervision_budget_sample_efficiency_2026-07-17/train_g1_5.py --phase a
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_H007 = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "state",
                     "h007_gradient_tug_role_code_drill_2026-07-17")
sys.path.insert(0, _H007)
sys.path.insert(0, _HERE)
import train_g2 as tg2               # reuse _load (d=384 TwoHead) + g1 helpers + bx
g1 = tg2.g1
bx = tg2.bx


def _load_panels():
    drill = json.load(open(os.path.join(_HERE, "swapc_drill.json")))["drill"]
    f2 = json.load(open(os.path.join(_HERE, "swapc_f2.json")))["panel"]
    raw = json.load(open(os.path.join(_HERE, "swapc_budgets.json")))
    budgets = {int(k): set(v) for k, v in raw.items()}
    return drill, f2, budgets


def _batch_budget(torch, items, glob_idx, arm, device, pad, answered_set, perm):
    B = len(items)
    tok = np.zeros((B, pad), np.int64)
    tgtA = np.zeros((B, pad), np.int64); tgtG = np.zeros((B, pad), np.int64)
    mA = np.zeros((B, pad), np.float32); mG = np.zeros((B, pad), np.float32)
    for bi, it in enumerate(items):
        surf = it["surface"].encode("utf-8"); Ls = len(surf)
        if glob_idx[bi] in answered_set:
            ans = bx.AGREE[it["cell"]["gold"]].encode("utf-8")
            seq = (surf + ans)[:pad]
        else:
            seq = surf[:pad]                          # answer-TRUNCATED
        Lseq = len(seq)
        tok[bi, :Lseq] = list(seq)
        tgtA[bi, :Lseq - 1] = list(seq[1:]); mA[bi, :Lseq - 1] = 1.0
        g = items[perm[bi]]["swap_target"].encode("utf-8") if arm == "C-shuf" else surf
        n = min(Ls, len(g))
        tgtG[bi, :n - 1] = list(g[1:n]); mG[bi, :n - 1] = 1.0
    t = lambda a: torch.tensor(a, device=device)
    return t(tok), t(tgtA), t(tgtG), t(mA), t(mG)


def train_control(arm, k, seed, cfg_tuple, drill, budgets, f2, cpt_win, steps, device):
    torch, M, cfg, TwoHead = cfg_tuple
    torch.manual_seed(seed)
    model = TwoHead(cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    cpt_steps, drill_steps = steps
    pad = 48
    answered = budgets[k]
    lam_g = 0.0 if arm == "C-scaf" else 1.0

    bs = 16 if device != "cpu" else 8
    for step in range(cpt_steps):
        idx = torch.randint(0, cpt_win.shape[0], (bs,)); w = cpt_win[idx].to(device)
        la, _, aux = model.both_logits(w[:, :-1])
        loss = torch.nn.functional.cross_entropy(la, w[:, 1:]) + aux
        opt.zero_grad(); loss.backward(); opt.step()

    rng = np.random.RandomState(seed); Bsz = 32
    ce_curve = []
    ans_items = [drill[i] for i in sorted(answered)]
    # PLATEAU precondition (lab-full 2026-07-17): held-out f2 must be stable over the last 40% of training
    # (max−min ≤ 0.05) — guards the endpoint-only-eval trap that let the k=384 tail spike corrupt a read.
    plateau_steps = {int(drill_steps * 0.60), int(drill_steps * 0.80), drill_steps - 1}
    plateau = []
    for step in range(drill_steps):
        bidx = rng.randint(0, len(drill), size=Bsz)
        items = [drill[i] for i in bidx]
        bperm = list(range(Bsz)); rng.shuffle(bperm)
        tok, tgtA, tgtG, mA, mG = _batch_budget(torch, items, list(bidx), arm, device, pad, answered, bperm)
        la, lg, aux = model.both_logits(tok)
        ceA = g1._masked_ce(torch, la, tgtA, mA)
        ceG = g1._masked_ce(torch, lg, tgtG, mG)
        loss = ceA + lam_g * ceG + aux
        opt.zero_grad(); loss.backward(); opt.step()
        # dense tail CE (final 1000 steps every 100) + coarse elsewhere every 500 — resolves tail transients
        if step % 500 == 0 or step == drill_steps - 1 or (step >= drill_steps - 1000 and step % 100 == 0):
            ce_curve.append({"step": step, "ceA": round(float(ceA.detach()), 4)})
        if step in plateau_steps:
            plateau.append({"step": step, "f2": round(g1._f2_dacc(torch, model, f2, device, pad), 4)})
            model.train()

    f2_d = round(g1._f2_dacc(torch, model, f2, device, pad), 4)
    insample = round(g1._f2_dacc(torch, model, ans_items, device, pad), 4)   # reachability = in-sample fit
    pf = [p["f2"] for p in plateau]
    plateau_ok = (max(pf) - min(pf) <= 0.05) if len(pf) >= 2 else None
    return {"f2_dacc": f2_d, "insample_dacc": insample, "ce_curve": ce_curve,
            "plateau": plateau, "plateau_ok": plateau_ok,
            "valid": insample >= 0.95}                                        # F2 run-validity guard


def _jobs(phase):
    if phase == "tiny":
        return [("C-dup", 96, 0)]
    if phase == "a":
        return [("C-dup", k, 0) for k in (24, 96, 192, 384)]     # phase-a: seed-0 exploratory sweep (done)
    if phase == "b":
        # G-1.5b four-point clause (lab-full 2026-07-17): k*=96 RE-INSTRUMENTED both seeds (replaces the
        # phase-a k=96 read, replacement-not-selection) + factor-2 neighbor k=48 both seeds. k=192 is out of
        # band (0.9167) so k=48 is the only admissible neighbor; k=24/384 read no gate.
        return [("C-dup", k, s) for k in (48, 96) for s in (0, 1)]
    if phase == "c":
        return [(arm, 96, s) for arm in ("C-scaf", "C-shuf") for s in (0, 1)]   # k=96 ONLY (k=192 out of band)
    raise SystemExit(f"unknown phase {phase}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="a", choices=["a", "b", "c", "tiny"])
    args = ap.parse_args()
    tiny = args.phase == "tiny"

    torch, M, cfg, TwoHead = tg2._load(tiny)
    import torch as _t
    device = "mps" if _t.backends.mps.is_available() else "cpu"
    cfg_tuple = (torch, M, cfg, TwoHead)
    steps = (60, 80) if tiny else (3000, 4000)
    n_cpt = 400 if tiny else 4000
    cpt_win = g1._cpt_windows(g1._nsmc_lines(n_cpt), 128, torch)
    drill, f2, budgets = _load_panels()

    print("=" * 80)
    print(f"H_008 G-1.5 phase={args.phase} — device={device} d={cfg.d_model} steps={steps} "
          f"drill={len(drill)} f2={len(f2)} budgets={sorted(budgets)}")
    print("BAND target: control f2_dacc ∈ [0.60, 0.80] stable across seeds ⇒ k* exists; else K1 CLOSE.")
    print("=" * 80, flush=True)

    out_path = os.path.join(_HERE, "g1_5_result.json")
    results = json.load(open(out_path)).get("jobs", []) if os.path.exists(out_path) else []
    for arm, k, seed in _jobs(args.phase):
        print(f"\n--- {arm} k={k} seed={seed} …", flush=True)
        r = train_control(arm, k, seed, cfg_tuple, drill, budgets, f2, cpt_win, steps, device)
        dacc = r["f2_dacc"]; band = 0.60 <= dacc <= 0.80
        last_ce = r["ce_curve"][-1]["ceA"] if r["ce_curve"] else None
        rec = {"arm": arm, "k": k, "seed": seed, "f2_dacc": dacc, "insample_dacc": r["insample_dacc"],
               "in_band": band, "last_ceA": last_ce, "valid": r["valid"], "plateau_ok": r["plateau_ok"],
               "plateau": r["plateau"], "ce_curve": r["ce_curve"]}
        results.append(rec)
        print(f"  {arm} k={k} s{seed}: f2_dacc={dacc} in_sample={r['insample_dacc']} in_band={band} "
              f"valid={r['valid']} plateau_ok={r['plateau_ok']} last_ceA={last_ce}", flush=True)
        json.dump({"config": {"d": cfg.d_model, "steps": steps, "band": [0.60, 0.80]}, "jobs": results},
                  open(out_path, "w"), ensure_ascii=False, indent=1)

    # band summary
    print("\n" + "=" * 80)
    cdup = [r for r in results if r["arm"] == "C-dup"]
    for r in sorted(cdup, key=lambda x: (x["k"], x["seed"])):
        print(f"  C-dup k={r['k']} s{r['seed']}: {r['f2_dacc']} {'← IN BAND' if r['in_band'] else ''}")
    print("wrote g1_5_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
