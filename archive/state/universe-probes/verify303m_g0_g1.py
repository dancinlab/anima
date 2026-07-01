#!/usr/bin/env python3
"""verify303m_g0_g1.py — EVAL-ONLY G0 (coherence) + G1 (recombination) on the
SHIPPED anima-clm-chat-303m ckpt. Imports the FROZEN H_1129 metric VERBATIM
(run_ladder / gen / known_word_ratio / coverage / CONCEPTS) — NO new metric, NO
moved threshold. Does NOT train (the H_1129 script trains; we only score the
existing ckpt). Deterministic seed 7 (the frozen protocol). p7 (not perplexity).

The torch ByteGPT is the Lane-G REFERENCE mouth (a_clm_gen_pipeline); the MOUNT
parity proof (CORE/verify303m_mount_full byte-exact vs this same ckpt's golden)
licenses it as a faithful stand-in for the engine-mounted model.
"""
import sys, json, importlib.util
import torch

H1129 = "/Users/mini/dancinlab/anima-verify-303m/UNIVERSE/h1129_midcap_broad_converged_recombination.py"
spec = importlib.util.spec_from_file_location("h1129", H1129)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

CKPT = sys.argv[1] if len(sys.argv) > 1 else "/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt"

def main():
    dev = "cpu"  # MPS gen ok but cpu deterministic; H_1129 used cuda — seed-fixed gen identical logits path
    torch.manual_seed(7)
    ck = torch.load(CKPT, map_location=dev, weights_only=False)
    cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"]).to(dev)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=True); m.eval(); m.grad_ckpt = False
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[mouth] anima-clm-chat-303m {nparam:,} params cfg={cfg} dev={dev}", flush=True)
    print(f"[KNOWN] {len(h.KNOWN)} dict words for coherence", flush=True)

    max_single, ladder, emergent = h.run_ladder(m, dev, cfg["block"])

    # G0 = coherence: known-word-ratio >= 0.50 on >=4/5 single-concept seeds (no byte salad).
    # run_ladder prints per-seed kwr; recompute the 5 single seeds for the G0 tally.
    g0_kwrs = []
    for c, _ in h.CONCEPTS:
        o = h.gen(m, f"{c}. ", 80, dev, cfg["block"])
        g0_kwrs.append(h.known_word_ratio(o))
    g0_pass_n = sum(1 for r in g0_kwrs if r >= 0.50)
    g0_pass = g0_pass_n >= 4

    print("\n=== G0 COHERENCE ===", flush=True)
    print(f"  per-seed kwr = {[round(r,3) for r in g0_kwrs]}", flush=True)
    print(f"  kwr>=0.50 on {g0_pass_n}/5  -> G0 {'PASS' if g0_pass else 'FAIL'} (frozen >=4/5)", flush=True)

    print("\n=== G1 RECOMBINATION ===", flush=True)
    print(f"  max_single_distinct = {max_single}", flush=True)
    for k in (2,3,4,5):
        L = ladder[k]
        print(f"  k={k}: composed_distinct={L['composed_distinct']} cov={L['coverage']} kwr={L['kwr']} coherent={L['coherent']} clears={L['clears']}", flush=True)
    print(f"  G1 {'PASS' if emergent else 'FAIL'} (frozen: some k composed_distinct>=2 AND >max_single AND coherent)", flush=True)

    out = {"ckpt": CKPT, "nparam": nparam, "config": cfg,
           "G0": {"per_seed_kwr": g0_kwrs, "pass_n": g0_pass_n, "pass": bool(g0_pass)},
           "G1": {"max_single_distinct": max_single,
                  "ladder": {k: {kk:vv for kk,vv in L.items()} for k,L in ladder.items()},
                  "emergent": bool(emergent), "pass": bool(emergent)}}
    json.dump(out, open("/tmp/verify303m/g0_g1_result.json","w"), ensure_ascii=False, indent=2)
    print("\n[done] /tmp/verify303m/g0_g1_result.json", flush=True)

if __name__ == "__main__": main()
