#!/usr/bin/env python3
"""OMEGA completeness SCALE LADDER (OΩ4 + OΩ5) — turn the single d512 OH1 point into a ≥3-rung curve.

WHY (a_scale_honest_scope):
  OH1 (#1801) measured the MINIMAL-GATE falsifier on ONE dim (d512, leak-free, competent):
      min_learned 0.8835  <=  a_only 1.1446  AND  < base 3.0978   → OH1_HOLDS=True
      Δ-vs-base = +2.2143 nats/byte · Δ-vs-a_only = +0.2607
  a_scale_honest_scope DEMANDS a ladder curve (≥3 rungs) before a scale-conclusion. A single
  toy point is INCOMPLETE. This driver adds rungs at OTHER dims and re-measures the SAME
  OH1 minimal-gate sweep on EACH, to see whether the A-wire advantage (min_learned Δ-vs-base)
  GROWS / SHRINKS / HOLDS with scale.

LADDER (OΩ4):  d384, d512(=baseline, re-measured here), d768, d1024
OΩ5 (one MORE-competent rung): a chosen dim trained with 2× steps (push val_ce notably lower).

METHOD (per rung, ONE H100, sequential — minimizes pod count + leak surface):
  1. train_to_competence (UNIVERSE/omega_trained_leakfree.run_rung) — leak-free causal_ca=True
     CDV2 at d_model, to competence (val_ce < uniform, leak self-test = 0.000), ckpt saved.
  2. on the FRESHLY-TRAINED frozen model, run the SAME K-form gate sweep
     (UNIVERSE/omega_gate_form_sweep.run_sweep): base / a_only / fixed_AmG / full_AG /
     min_learned / min_fixed on the held-out tail.
  3. per-rung OH1 falsifier: min_learned_HOLDS iff min_learned CE <= a_only CE AND < base CE.

NO d512-hardcoded cross-check here (that reference is dim-specific to #1800). Each rung is its
own internal apples-to-apples sweep; the d512 rung re-run here is itself the cross-check against
#1801 (we print |Δ| vs the #1801 numbers but do NOT gate on it for non-d512 rungs).

a_lane_akida_gpu_split: Lane-G / GPU (NOT Lane A AKIDA). GPU REQUIRED (g63, no silent CPU).
p7: CE is a held-out prediction number, NOT a verdict-of-truth — reported honestly, NO fabrication.
"""
import os, sys, json, math, time, hashlib, argparse
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from omega_trained_leakfree import run_rung  # train + closure_eval + ckpt, verbatim reuse
from omega_gpu_complete import fetch_corpus, UNIFORM_CE
from omega_gate_form_sweep import run_sweep, ALPHA  # the OH1 K-form gate sweep, verbatim reuse

# #1801 d512 OH1 reference (for the d512 re-run sanity print ONLY — not a gate for other dims)
D512_REF = {"base": 3.097779103749307, "a_only": 1.144181, "min_learned": 0.883525}


def measure_rung(rung_spec, train_data, val_data, held, block, device, out_dir):
    """Train one rung to competence, then run the OH1 K-form sweep on the frozen trained model.
    rung_spec: dict(label, d_model, n_layer, n_head, n_kv_head, bs, lr, steps)."""
    label = rung_spec["label"]
    ckpt_path = os.path.join(out_dir, f"omega_cdv2_{label}.pt")

    # ── (1) train to competence + the trainer's own closure_eval (no gen, faster) ──
    r = run_rung(
        d_model=rung_spec["d_model"], n_layer=rung_spec["n_layer"], n_head=rung_spec["n_head"],
        n_kv_head=rung_spec["n_kv_head"], block=block, bs=rung_spec["bs"], lr=rung_spec["lr"],
        steps=rung_spec["steps"], device=device, train_data=train_data, val_data=val_data,
        held=held, label=label, ckpt_path=ckpt_path,
    )

    # ── (2) re-load the saved ckpt FROZEN and run the OH1 K-form sweep (apples-to-apples) ──
    from conscious_decoder import ConsciousDecoderV2
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ck["config"]
    model = ConsciousDecoderV2(
        vocab_size=cfg["vocab_size"], d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"], n_kv_head=cfg["n_kv_head"],
        consciousness_dim=cfg.get("consciousness_dim", 128), causal_ca=cfg.get("causal_ca", True),
    ).to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)

    rows, meta = run_sweep(model, held, block, device, max_pos=12000)

    min_ce = rows["min_learned"]["ce"]
    aonly_ce = rows["a_only"]["ce"]
    base_ce = rows["base"]["ce"]
    le_aonly = min_ce <= aonly_ce + 1e-6
    lt_base = min_ce < base_ce
    holds = bool(le_aonly and lt_base)

    print(f"\n=== RUNG {label} OH1 K-form sweep (frozen leak-free, nats/byte) ===", flush=True)
    print(f"  {'form':<12} {'gB':>9} {'gA':>9} {'gG':>9} {'test_CE':>10}", flush=True)
    for name in ["base", "a_only", "fixed_AmG", "full_AG", "min_learned", "min_fixed"]:
        rr = rows[name]
        star = "  ★OH1" if name == "min_learned" else ""
        print(f"  {name:<12} {rr['gB']:>9.4f} {rr['gA']:>9.4f} {rr['gG']:>9.4f} {rr['ce']:>10.6f}{star}", flush=True)
    print(f"  {'uniform':<12} {'':>9} {'':>9} {'':>9} {UNIFORM_CE:>10.6f}", flush=True)
    print(f"  OH1: min_learned({min_ce:.6f}) <= a_only({aonly_ce:.6f})={le_aonly}  AND  "
          f"< base({base_ce:.6f})={lt_base}  ->  min_learned_HOLDS={holds}", flush=True)
    print(f"  Δ-vs-base={base_ce - min_ce:+.4f}  Δ-vs-a_only={aonly_ce - min_ce:+.4f}", flush=True)

    return {
        "label": label,
        "d_model": rung_spec["d_model"], "n_layer": rung_spec["n_layer"],
        "n_head": rung_spec["n_head"], "n_kv_head": rung_spec["n_kv_head"],
        "steps": rung_spec["steps"], "params": r["params"],
        "leak_self_test": r["leak_self_test"], "leak_free": r["leak_free"],
        "train": {"first_ce_a": r["train"]["first_ce_a"], "final_ce_a": r["train"]["final_ce_a"],
                  "final_val_ce": r["train"]["final_val_ce"],
                  "below_uniform": r["train"]["below_uniform"], "competent": r["train"]["competent"],
                  "wall_s": r["train"]["wall_s"]},
        "ckpt": {"path": ckpt_path, "sha256": r["ckpt_sha256"]},
        "forms": rows,
        "oh1": {"min_learned_ce": min_ce, "a_only_ce": aonly_ce, "base_ce": base_ce,
                "le_aonly": bool(le_aonly), "lt_base": bool(lt_base),
                "min_learned_HOLDS": holds,
                "delta_vs_base": base_ce - min_ce, "delta_vs_a_only": aonly_ce - min_ce},
        "config": cfg,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--corpus_mb", type=int, default=400)
    ap.add_argument("--out_dir", default="/workspace/omega-scale")
    ap.add_argument("--out", default=None)
    # rung ladder: "label:d_model:n_layer:n_head:n_kv_head:bs:lr:steps" comma-sep
    ap.add_argument("--rungs", default=(
        "d384:384:8:8:4:48:6e-4:12000,"
        "d512:512:8:8:4:48:6e-4:12000,"
        "d768:768:8:12:4:40:5e-4:12000,"
        "d1024:1024:8:16:4:32:4e-4:12000,"
        "d768x2:768:8:12:4:40:5e-4:24000"
    ))
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    out_json = args.out or os.path.join(args.out_dir, "omega_scale_ladder_results.json")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("!!! NO CUDA — refusing to fake a GPU train (g63). Reporting BLOCKED.", flush=True)
        json.dump({"BLOCKED": "no_cuda", "device": device}, open(out_json, "w"), indent=2)
        sys.exit(2)
    gpu_name = torch.cuda.get_device_name(0)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    print(f"=== OMEGA SCALE LADDER (OΩ4+OΩ5) — leak-free OH1 minimal-gate vs d_model ===", flush=True)
    print(f"device={device}  gpu={gpu_name}  torch={torch.__version__}", flush=True)

    target = args.corpus_mb * 1_000_000
    corpus, prov = fetch_corpus(target, os.path.join(args.out_dir, "omega_corpus_big.bin"))
    sha = hashlib.sha256(corpus.tobytes()).hexdigest()
    n = len(corpus)
    print(f"corpus: {n}B ({n/1e6:.1f}MB)  prov={prov}  sha256={sha[:16]}", flush=True)

    cut = int(n * 0.9)
    train_data = corpus[:cut]
    held = corpus[cut:]
    val_data = held[:len(held) // 2]

    rungs = []
    for tok in args.rungs.split(","):
        p = tok.split(":")
        rungs.append({"label": p[0], "d_model": int(p[1]), "n_layer": int(p[2]),
                      "n_head": int(p[3]), "n_kv_head": int(p[4]), "bs": int(p[5]),
                      "lr": float(p[6]), "steps": int(p[7])})

    t_start = time.time()
    rung_results = []
    for spec in rungs:
        print(f"\n{'#'*30} LADDER RUNG {spec['label']} {'#'*30}", flush=True)
        rr = measure_rung(spec, train_data, val_data, held, args.block, device, args.out_dir)
        rung_results.append(rr)
        # checkpoint the partial ledger after EVERY rung (commit-early survivability)
        partial = {
            "lane": "Lane-G", "substrate": "GPU", "gpu": gpu_name, "torch": torch.__version__,
            "corpus": {"bytes": int(n), "mb": n / 1e6, "prov": prov, "sha256": sha},
            "question": "does the OH1 minimal-gate A-wire advantage (min_learned Δ-vs-base) grow/shrink/hold with scale?",
            "falsifier_per_rung": "min_learned_HOLDS iff min_learned CE <= a_only CE AND < base CE",
            "d512_ref_1801": D512_REF,
            "rungs": rung_results,
            "partial": True, "rungs_done": len(rung_results), "rungs_total": len(rungs),
            "total_wall_s": time.time() - t_start,
        }
        json.dump(partial, open(out_json, "w"), indent=2, ensure_ascii=False)
        print(f"  [checkpoint] {len(rung_results)}/{len(rungs)} rungs -> {out_json}", flush=True)

    # ── ladder trend ──
    by_d = sorted([r for r in rung_results if not r["label"].endswith("x2")], key=lambda r: r["d_model"])
    trend = [{"label": r["label"], "d_model": r["d_model"], "val_ce": r["train"]["final_val_ce"],
              "min_learned_ce": r["oh1"]["min_learned_ce"], "a_only_ce": r["oh1"]["a_only_ce"],
              "base_ce": r["oh1"]["base_ce"], "delta_vs_base": r["oh1"]["delta_vs_base"],
              "delta_vs_a_only": r["oh1"]["delta_vs_a_only"],
              "HOLDS": r["oh1"]["min_learned_HOLDS"]} for r in by_d]
    all_hold = all(r["oh1"]["min_learned_HOLDS"] for r in rung_results)

    ledger = {
        "lane": "Lane-G", "substrate": "GPU", "gpu": gpu_name, "torch": torch.__version__,
        "corpus": {"bytes": int(n), "mb": n / 1e6, "prov": prov, "sha256": sha},
        "question": "does the OH1 minimal-gate A-wire advantage (min_learned Δ-vs-base) grow/shrink/hold with scale?",
        "falsifier_per_rung": "min_learned_HOLDS iff min_learned CE <= a_only CE AND < base CE",
        "d512_ref_1801": D512_REF,
        "rungs": rung_results,
        "ladder_trend_by_d": trend,
        "min_learned_HOLDS_all_rungs": bool(all_hold),
        "scope": "a_scale_honest_scope — multi-rung ladder (≥3 dims) of the leak-free OH1 minimal-gate; "
                 "p7: CE is a held-out prediction number, NOT a verdict-of-truth.",
        "partial": False,
        "total_wall_s": time.time() - t_start,
    }
    json.dump(ledger, open(out_json, "w"), indent=2, ensure_ascii=False)

    print(f"\n{'='*70}\n=== OMEGA SCALE LADDER SUMMARY ===", flush=True)
    print(f"  {'rung':<8} {'d':>5} {'val_ce':>8} {'base':>8} {'a_only':>8} {'min_learn':>10} "
          f"{'Δvbase':>8} {'Δva_only':>9} {'HOLDS':>6}", flush=True)
    for r in rung_results:
        o = r["oh1"]
        print(f"  {r['label']:<8} {r['d_model']:>5} {r['train']['final_val_ce']:>8.4f} "
              f"{o['base_ce']:>8.4f} {o['a_only_ce']:>8.4f} {o['min_learned_ce']:>10.4f} "
              f"{o['delta_vs_base']:>+8.4f} {o['delta_vs_a_only']:>+9.4f} "
              f"{str(o['min_learned_HOLDS']):>6}", flush=True)
    print(f"  >>> min_learned_HOLDS across ALL {len(rung_results)} rungs = {all_hold}", flush=True)
    print(f"results -> {out_json}", flush=True)


if __name__ == "__main__":
    main()
