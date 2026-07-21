#!/usr/bin/env python3
"""H_003 training driver — CPT + drill + forced-choice d_acc, per arm × seed.

Consumes v1's CLMConvMoE (anima/core/model.py) and this repo's verified pieces:
span_policy_encode.encode() (arm byte streams), gen_drill.drill_grid.json (drill,
못=0), build_panels panels (f2'/f1'/f2b, F7 PASS). All arms train FROM SCRATCH
(C2 licenses it; the 388M base has the wrong d), so no warm-start reinit is needed.

Arms:
  A-atom : span policy off        (encode shatter=False)
  A-shat : negation spans -> jamo (encode shatter=True)
  C-plc  : placebo 진짜 -> jamo   (encode shatter=True, placebo_jamo=진짜)
  C-scaf : A-atom encoding, NO drill (leak check — F3)
  C-perm : A-atom encoding, drill gold PERMUTED (harness check — F4)

Falsifiers computed at the end: F1 (Δd_acc A-atom−A-shat ≥ 0.15), F2 (liveness
f1' ≥ 0.85), F6 (placebo A-atom−C-plc < 0.05).

  smoke:  python3 train_h003.py --smoke      (d=64, tiny corpus, ~1 min — WIRING only)
  full :  python3 train_h003.py               (d=384, ~6-8h — the verdict run)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANIMA = "/Users/mini/dancinlab/anima"
_NSMC = os.path.expanduser("~/g1_natem/nsmc_ratings_train.txt")

sys.path.insert(0, _HERE)
sys.path.insert(0, _ANIMA)

import span_policy_encode as spe  # verified arm encoder


def _load_torch_model():
    import torch
    import core.model as M
    return torch, M


def _codec(m, n_cpt_lines):
    """Train (or reuse) the jamo-BPE codec once; cache in-process."""
    lines = [l.split("\t")[1] for l in open(_NSMC, encoding="utf-8").read().splitlines()[1:]
             if len(l.split("\t")) > 2]
    merges = m.train_bpe(lines[:20000], 2048)
    merge_rank, tok2id, vocab = m.build_vocab(lines, merges)
    return lines[:n_cpt_lines], merge_rank, tok2id


def _arm_encode(m, line, merge_rank, tok2id, arm):
    jinjja = m.to_jamo("진짜")
    if arm in ("A-atom", "C-scaf", "C-perm"):
        return spe.encode(m, line, merge_rank, tok2id, shatter=False)
    if arm == "A-shat":
        return spe.encode(m, line, merge_rank, tok2id, shatter=True)
    if arm == "C-plc":
        return spe.encode(m, line, merge_rank, tok2id, shatter=True, placebo_jamo=jinjja)
    raise ValueError(arm)


def _windows(byte_stream, seq_len, torch):
    """Byte stream (V=256) -> (N, seq_len) long tensor of next-token windows."""
    b = list(byte_stream)
    n = (len(b) - 1) // seq_len
    if n <= 0:
        return None
    import numpy as np
    arr = np.frombuffer(bytes(b[: n * seq_len + 1]), dtype=np.uint8).astype("int64")
    x = torch.from_numpy(arr[:-1].reshape(n, seq_len))
    y = torch.from_numpy(arr[1:].reshape(n, seq_len))
    return x, y


def _nll_tail(model, torch, ctx_bytes, cont_bytes, device):
    """NLL of the continuation bytes given a real-byte left context (teacher forced)."""
    import numpy as np
    seq = list(ctx_bytes) + list(cont_bytes)
    t = torch.from_numpy(np.frombuffer(bytes(seq), dtype=np.uint8).astype("int64"))[None].to(device)
    with torch.no_grad():
        logits = model(t[:, :-1])["logits"]            # (1, V, T-1)
        logp = torch.log_softmax(logits, dim=1)
        tgt = t[0, 1:]
        # score only the continuation region
        start = len(ctx_bytes) - 1
        nll = -logp[0, tgt[start:], torch.arange(start, tgt.numel(), device=device)].sum()
    return float(nll)


def _dacc(model, torch, panel_items, m, merge_rank, tok2id, arm, ctx_line, device):
    ctx = _arm_encode(m, ctx_line, merge_rank, tok2id, arm)[:160]
    correct = 0
    for it in panel_items:
        seed = it["surface"]
        g = _arm_encode(m, seed + it.get("gold", "긍정."), merge_rank, tok2id, arm)
        c = _arm_encode(m, seed + it.get("counterfactual", "부정."), merge_rank, tok2id, arm)
        # first-divergence: score from where g and c differ
        p = 0
        while p < min(len(g), len(c)) and g[p] == c[p]:
            p += 1
        seed_enc = _arm_encode(m, seed, merge_rank, tok2id, arm)
        ng = _nll_tail(model, torch, ctx + seed_enc, g[len(seed_enc):], device)
        nc = _nll_tail(model, torch, ctx + seed_enc, c[len(seed_enc):], device)
        correct += int(ng < nc)
    return correct / max(1, len(panel_items))


def _panel_with_labels(items):
    """Attach gold/counterfactual 긍정./부정. from gold_sent (1=긍정)."""
    out = []
    for it in items:
        g = "긍정." if it["gold_sent"] == 1 else "부정."
        c = "부정." if it["gold_sent"] == 1 else "긍정."
        out.append({**it, "gold": g, "counterfactual": c})
    return out


def _enc_key(arm):
    """CPT encoding depends only on the SPAN POLICY, not the seed nor the training
    schedule. A-atom / C-scaf / C-perm all use shatter=False → identical CPT stream,
    so the 5 arms need only 3 distinct CPT encodings (cached across seeds)."""
    return {"A-atom": "atom", "C-scaf": "atom", "C-perm": "atom",
            "A-shat": "shat", "C-plc": "plc"}[arm]


def _stack_windows(streams, torch):
    """CONCATENATE the per-line byte streams into ONE continuous stream, then
    window. NSMC lines are ~53 bytes (min 2, max 244) — far shorter than seq_len,
    so per-LINE windowing dropped every line (0 windows → the model never trained,
    the 0.5-everywhere harness artifact). A byte-level LM trains on a continuous
    stream (v1 does the same, with sentinels); we join lines with a 0x0a separator."""
    big = bytearray()
    for s in streams:
        big += s
        big += b"\n"
    return _windows(bytes(big), cfg_seq, torch)


def train_arm(arm, seed, cfg, m, merge_rank, tok2id, drill, panels, cpt_cache, cpt_lines):
    torch, M = _load_torch_model()
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    torch.manual_seed(seed)
    model = M.CLMConvMoE(cfg).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    model.train()

    def train_on(xy, steps, label):
        if xy is None:
            return
        xs, ys = xy
        n = xs.size(0)
        for step in range(steps):
            idx = torch.randint(0, n, (cfg_batch,))
            out = model(xs[idx].to(dev), targets=ys[idx].to(dev))
            opt.zero_grad(); out["loss"].backward(); opt.step()
            if step % max(1, steps // 8) == 0:
                print(f"    {arm} s{seed} {label} step {step}/{steps} loss={out['loss'].item():.3f}",
                      flush=True)

    # CPT — reuse the cached windows for this arm's encoding key
    key = _enc_key(arm)
    if key not in cpt_cache:
        print(f"    encoding CPT for '{key}' ({len(cpt_lines)} lines)…", flush=True)
        streams = [_arm_encode(m, l, merge_rank, tok2id, arm) for l in cpt_lines]
        cpt_cache[key] = _stack_windows(streams, torch)
    train_on(cpt_cache[key], cfg_cpt_steps, "cpt")
    # drill (skip for C-scaf; permute gold for C-perm)
    if arm != "C-scaf":
        import random
        rng = random.Random(seed)
        ditems = list(drill)
        if arm == "C-perm":
            golds = [d["gold"] for d in ditems]; rng.shuffle(golds)
            ditems = [{**d, "gold": g} for d, g in zip(ditems, golds)]
        drill_streams = [_arm_encode(m, d["surface"] + d["gold"], merge_rank, tok2id, arm)
                         for d in ditems]
        train_on(_stack_windows(drill_streams, torch), cfg_drill_steps, "drill")

    model.eval()
    ctx_line = cpt_lines[0]
    res = {p: round(_dacc(model, torch, panels[p], m, merge_rank, tok2id, arm, ctx_line, dev), 4)
           for p in panels}
    return res


# config (module-level so train_on sees them)
cfg_seq = cfg_batch = cfg_cpt_steps = cfg_drill_steps = None


def main() -> int:
    global cfg_seq, cfg_batch, cfg_cpt_steps, cfg_drill_steps
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()

    torch, M = _load_torch_model()
    if a.smoke:
        d, L, E = 64, 2, 2
        cfg_seq, cfg_batch, cfg_cpt_steps, cfg_drill_steps = 128, 8, 30, 20
        n_cpt, seeds, arms = 1500, [0], ["A-atom", "A-shat", "C-plc"]
    else:
        d, L, E = 384, 4, 3
        cfg_seq, cfg_batch, cfg_cpt_steps, cfg_drill_steps = 512, 16, 8000, 2500
        n_cpt, seeds, arms = 120000, [0, 1], ["A-atom", "A-shat", "C-plc", "C-scaf", "C-perm"]

    cfg = M.CLMConfig(vocab_size=256, d_model=d, n_trunk_layers=L, n_experts=E)
    m = spe.load_codec()
    cpt_lines, merge_rank, tok2id = _codec(m, n_cpt)

    drill = json.load(open(os.path.join(_HERE, "drill_grid.json")))["items"]
    panels = {p: _panel_with_labels(json.load(open(os.path.join(_HERE, f"panel_{p}.json"))))
              for p in ["f2prime", "f1prime"]}

    print("=" * 70, flush=True)
    print(f"H_003 training driver — {'SMOKE (wiring only)' if a.smoke else 'FULL run'} · d={d} L={L}"
          f" · {len(seeds)} seeds × {len(arms)} arms", flush=True)
    print("=" * 70, flush=True)
    results = {}
    cpt_cache = {}  # {enc_key: (xs, ys)} — CPT windows reused across seeds/schedule-variant arms
    for seed in seeds:
        for arm in arms:
            r = train_arm(arm, seed, cfg, m, merge_rank, tok2id, drill, panels, cpt_cache, cpt_lines)
            results[f"{arm}.s{seed}"] = r
            print(f"  {arm:8s} s{seed}  f2'={r['f2prime']}  f1'={r['f1prime']}", flush=True)

    # falsifiers (per seed where available)
    def g(arm, seed, p):
        return results.get(f"{arm}.s{seed}", {}).get(p)
    verdicts = {}
    for seed in seeds:
        a_at, a_sh, a_plc = g("A-atom", seed, "f2prime"), g("A-shat", seed, "f2prime"), g("C-plc", seed, "f2prime")
        f1_live = g("A-atom", seed, "f1prime")
        verdicts[f"s{seed}"] = {
            "F1_delta_atom_minus_shat": round(a_at - a_sh, 4) if a_at is not None and a_sh is not None else None,
            "F2_liveness_f1prime": f1_live,
            "F6_placebo_atom_minus_plc": round(a_at - a_plc, 4) if a_at is not None and a_plc is not None else None,
        }
    print("\nfalsifier readout (per seed):")
    for s, v in verdicts.items():
        print(f"  {s}: {v}")
    if a.smoke:
        print("\nSMOKE: wiring verified iff every arm produced f2'/f1' numbers above (values are"
              " meaningless at d=64/30 steps). The full run is the verdict.")

    out = {"config": {"d": d, "L": L, "smoke": a.smoke}, "results": results, "verdicts": verdicts}
    tag = "smoke" if a.smoke else "full"
    with open(os.path.join(_HERE, f"train_result_{tag}.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"wrote train_result_{tag}.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
