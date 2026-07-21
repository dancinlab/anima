"""H5_001 G-0k — phi->hon probe on the F-6 deleaked register (SPEC state/h5_001_g0k_design_2026-07-18/).

The mount/fold referee's learnability half: CPT the byte trunk (NSMC, delta-independent per SPEC finding),
freeze it, pool per-node phi via the BUILDER-emitted node_spans (NOT v4's eojeol walk — the slot orbit
makes node-order != surface-order), and probe phi[CONTESTED_V=4k+1] -> raw hp. Pass = held-out acc >= 0.90,
BOTH seeds. The mirror ADV (4k) is EXCLUDED (F-1 makes a both-site pool hp-invariant).

This runner IMPORTS the sealed v4 harness as a read-only library (model arch + CPT windows) and adds
only the v5-specific node mapping + probe. It never edits v4.

Run:  python3 g0k_probe.py --smoke            # d=64, short CPT, delta1 — wiring (minutes)
      python3 g0k_probe.py --delta 1 --seed 0 # d=384 real probe (per delta, per seed)
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# Portable: env vars override the local defaults (on a deploy bundle, point all three at the bundle dir,
# which holds core/, the flat v4 harness .py, the v5 builder .py, and the g0k .py side by side).
_ANIMA = os.environ.get("ANIMA_ROOT", "/Users/mini/dancinlab/anima")
_V4H = os.environ.get("V4H_ROOT", "/Users/mini/dancinlab/anima-v4/state/h004_parser_duel_tension_rank_drill_2026-07-16")
_BUILDER = os.environ.get("BUILDER_ROOT", os.path.join(os.path.dirname(_HERE), "h5_001_g0_deleaked_register_2026-07-18"))
for _p in (_ANIMA, _V4H, _BUILDER, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Imports below intentionally follow the sys.path wiring above (core.model lives in the anima repo,
# the sealed v4 harness in _V4H, the v5 builder in _BUILDER) — they cannot precede it.
import numpy as np
import train_h004 as H                                # sealed v4 harness — model arch + CPT windows
from train_g3a import _phi_encode                      # frozen pre-readout encode — reused as-is
import build_deleaked_register as B                    # v5 F-6 panels (emits node_spans)


def node_phi_v5(fm, torch, item, device):
    """(26, d) per-node phi = mean-pool of the frozen top-layer state over each node's node_spans byte
    interval. UNMAPPED bytes (filler/prefix/tail-pad) never enter any node's pool (SPEC 2.4). Nodes with
    no span stay 0. This REPLACES v4's _node_of_byte — spans come from construction, not a re-parse."""
    surf_b = item["surface"].encode("utf-8")
    toks = torch.tensor(list(surf_b), dtype=torch.long, device=device)[None]
    x = _phi_encode(fm, torch, toks)[0]                # (C, L)
    d = x.shape[0]
    phi = torch.zeros(26, d, device=device)
    for s, e, nid in item["node_spans"]:
        if e > s:
            phi[nid] = x[:, s:e].mean(dim=1)
    return phi                                         # (26, d), no grad (frozen encoder)


def run_probe(delta, seed, smoke):
    torch, M, cfg, Struct = H._load(smoke=smoke)       # d=64 smoke / d=384 real; core.model arch
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    panels = B.build_delta(delta)
    drill = panels["drill"]

    # CPT (delta-independent; NSMC raw utf-8 windows, smoke-fallback corpus if NSMC absent) — SPEC finding.
    cpt_steps = 300 if smoke else 8000
    cpt_win = H._cpt_windows(H._nsmc_lines(2000 if smoke else 120000), 512, torch)
    torch.manual_seed(seed)
    model = Struct(cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=H._BASE_LR)
    for step in range(cpt_steps):
        idx = torch.randint(0, cpt_win.shape[0], (16,))
        w = cpt_win[idx].to(device)
        out = model(w[:, :-1], targets=w[:, 1:])
        opt.zero_grad(); out["loss"].backward(); opt.step()
    fm = model.eval()

    # Probe phi[4k+1] -> raw hp (mirror EXCLUDED). Report-only canary: phi[4k] -> mirror_hp (span-bug det).
    X, y, Xc, yc = [], [], [], []
    for it in drill[:200]:
        phi = node_phi_v5(fm, torch, it, device).cpu().numpy()
        for k, c in enumerate(it["conjuncts"]):
            X.append(phi[4 * k + 1]); y.append(int(c["hp"]))       # CONTESTED_V -> hp
            Xc.append(phi[4 * k]); yc.append(1 - int(c["hp"]))     # ADV -> mirror_hp (canary)

    def _probe_acc(Xa, ya, sd):
        Xa = np.asarray(Xa, np.float32); ya = np.asarray(ya, np.float32)
        rng = np.random.default_rng(sd); perm = rng.permutation(len(Xa)); Xa, ya = Xa[perm], ya[perm]
        ntr = int(0.7 * len(Xa))
        Xt = torch.tensor(Xa[:ntr], device=device); yt = torch.tensor(ya[:ntr], device=device)
        Xv = torch.tensor(Xa[ntr:], device=device); yv = torch.tensor(ya[ntr:], device=device)
        probe = torch.nn.Linear(Xa.shape[1], 1).to(device)
        po = torch.optim.Adam(probe.parameters(), lr=1e-2)
        for _ in range(500):
            po.zero_grad()
            loss = torch.nn.functional.binary_cross_entropy_with_logits(probe(Xt).squeeze(-1), yt) \
                + 1e-3 * probe.weight.pow(2).sum()
            loss.backward(); po.step()
        with torch.no_grad():
            return float(((probe(Xv).squeeze(-1) > 0).float() == yv).float().mean())

    acc = _probe_acc(X, y, seed)
    canary = _probe_acc(Xc, yc, seed)
    ok = acc >= 0.90
    res = {"delta": delta, "seed": seed, "smoke": smoke, "d": cfg.d_model, "cpt_steps": cpt_steps,
           "probe_acc": round(acc, 4), "threshold": 0.90, "pass": ok, "n": len(X),
           "canary_adv_mirror_hp_acc": round(canary, 4)}
    tag = "smoke" if smoke else f"d{delta}_s{seed}"
    json.dump(res, open(os.path.join(_HERE, f"g0k_probe_{tag}.json"), "w"), indent=2)
    print(f"G-0k probe phi[4k+1]->hp d{delta} seed{seed} (d={cfg.d_model}): held-out acc={round(acc,4)} "
          f"(>=0.90: {'PASS' if ok else 'FAIL'}) - canary phi[4k]->mirror_hp={round(canary,4)} - n={len(X)}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--delta", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    return run_probe(a.delta, a.seed, a.smoke)


if __name__ == "__main__":
    raise SystemExit(main())
