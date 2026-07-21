"""H5_001 G-0k — full window pre-check: phi->hon probe AND control in-sample fit, per delta, per seed.

The mount/fold referee (SPEC state/h5_001_g0k_design_2026-07-18/). Per (delta, seed): one CPT'd byte
trunk, then (A) frozen-trunk probe phi[CONTESTED_V=4k+1] -> raw hp (>= 0.90), and (B) an A-hand run —
the hand field injected via node_spans scatter — overfit on the drill to in-sample free-slot d_acc
(>= 0.95). A delta PASSES only if BOTH thresholds clear on BOTH seeds; the gate mounts iff >= 2
CONSECUTIVE delta pass (pre-registered early-stop, ascending delta).

Adapts the sealed v4 harness (imported read-only) to the v5 4-node layout: hand field from the
builder support_edges + hon vector; struct injection scattered by BUILDER node_spans (not v4's eojeol
walk); UNMAPPED filler/prefix/tail bytes get a ZERO struct row (NULL sentinel, no extra graph node).

Run:  python3 g0k_run.py --smoke                 # d=64, short, delta1 — WIRING-4 (minutes)
      python3 g0k_run.py --delta 1 --seed 0      # d=384 real (per delta, per seed)
      python3 g0k_run.py --sweep                 # d=384, delta 1..5 x 2 seeds, early-stop (the gate)
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# Portable: env vars override local defaults (deploy bundle points all three at the bundle dir).
_ANIMA = os.environ.get("ANIMA_ROOT", "/Users/mini/dancinlab/anima")
_V4H = os.environ.get("V4H_ROOT", "/Users/mini/dancinlab/anima-v4/state/h004_parser_duel_tension_rank_drill_2026-07-16")
_BUILDER = os.environ.get("BUILDER_ROOT", os.path.join(os.path.dirname(_HERE), "h5_001_g0_deleaked_register_2026-07-18"))
for _p in (_ANIMA, _V4H, _BUILDER, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# sys.path wired above (core.model in anima, sealed v4 harness in _V4H, v5 builder in _BUILDER).
import numpy as np
import train_h004 as H
import g1_core_check as gc
from train_g3a import _phi_encode
import build_deleaked_register as B
from g0k_probe import node_phi_v5

_ANS = ["앞", "뒤"]                                    # gold tokens (v4 answer alphabet)


def item_T_v5(item):
    """(T (26,26), gold list, n=26) — the v5 hand field. hon[4k+1]=hp, hon[4k+2]=pos1, hon[4k+3]=1-pos1,
    hon[4k]=0 (ADV field-inert), TAIL/ANS=0 (SPEC 4). Support from the builder support_edges."""
    K = len(item["conjuncts"])
    n = 4 * K + 2
    se = item["support_edges"]
    ha = {int(k): v for k, v in se["head_a"].items()}
    hg = {int(k): v for k, v in se["head_g"].items()}
    hon = np.zeros(n)
    gold = []
    for k, c in enumerate(item["conjuncts"]):
        hon[4 * k + 1] = int(c["hp"])
        pos1 = 1.0 if int(c["honored_position"]) == 1 else 0.0
        hon[4 * k + 2] = pos1
        hon[4 * k + 3] = 1.0 - pos1
        gold.append(int(c["gold_flip"]))
    T = gc.concord_field(gc.t_struct(n, ha, hg), hon)
    return T, gold, n


def node_layout_v5(item, gold, seq_bytes_len):
    """(seq_bytes_len,) node id per byte, from BUILDER node_spans. UNMAPPED bytes -> NULL=26 (a zero
    struct row, appended in struct_for_v5). Answer byte k -> its CONTESTED_V node (4k+1) at the
    prediction position (v4's 3k off-by-one rule, train_h004.py:146, with 3k -> 4k+1)."""
    full = np.full(seq_bytes_len, 26, dtype=np.int64)        # default NULL (zero-injection)
    for s, e, nid in item["node_spans"]:
        full[s:e] = nid
    base = len(item["surface"].encode("utf-8"))
    K = len(gold)
    for k in range(K):
        full[max(base + 3 * k - 1, 0): base + 3 * k + 3] = 4 * k + 1
    return full


def struct_for_v5(model, torch, item, arm, device, seq_bytes_len):
    """(seq_bytes_len, 64) struct rows = node_embed(arm_tensor(T)) scattered by node_layout_v5, with a
    zero row for NULL (index 26). arm in {A-duel (hand field), C-scaf (zeros = no field)}."""
    T, gold, n = item_T_v5(item)
    # A-duel/A-hand = hand field verbatim; C-scaf/C-trained = zero field (trunk-only, the ceiling control);
    # C-perm = row/col-permuted field (a field-shaped but wrong control) — SPEC G-1 arm set.
    if arm in ("C-scaf", "C-trained"):
        Ta = np.zeros_like(T)
    elif arm == "C-perm":
        rng = np.random.default_rng(90210 + n)
        perm = rng.permutation(n)
        Ta = T[np.ix_(perm, perm)]
    else:
        Ta = T
    emb = model.node_embed(torch.tensor(Ta, dtype=torch.float32))     # (n,64), on model device
    emb = torch.cat([emb, torch.zeros(1, emb.shape[1], device=emb.device)], dim=0)   # +NULL zero row
    full = node_layout_v5(item, gold, seq_bytes_len)
    struct = emb[torch.tensor(full, device=emb.device)]     # (seq_bytes_len, 64)
    return struct, gold


def _seq_bytes(item):
    return item["surface"].encode("utf-8"), item["gold_pattern"].encode("utf-8")


def dacc_v5(model, torch, panel, arm, device, free_slots):
    """Forced-choice free-slot d_acc (v4 protocol, node_spans struct). Per item, per free slot k:
    gold answer token vs its flip; correct if NLL(gold) <= NLL(flip). Mean over items x free slots."""
    correct = tot = 0
    for it in panel:
        surf_b, gold_b = _seq_bytes(it)
        base = len(surf_b)
        K = len(gold_b) // 3
        seq = surf_b + gold_b
        struct, gold = struct_for_v5(model, torch, it, arm, device, len(seq))
        struct = struct.to(device)

        def _nll(byte_seq):
            toks = torch.tensor(list(byte_seq), dtype=torch.long, device=device)[None]
            with torch.no_grad():
                out = model(toks, struct=struct[None])
            logp = torch.log_softmax(out["logits"][0], dim=0)
            res = []
            for k in range(K):
                s = base + 3 * k
                res.append(sum(-logp[byte_seq[s + j], s + j - 1].item() for j in range(3)))
            return res
        nll_gold = _nll(seq)
        for k in free_slots:
            flip = _ANS[1 - gold[k]].encode("utf-8")
            alt = bytearray(seq); alt[base + 3 * k: base + 3 * k + 3] = flip
            if nll_gold[k] <= _nll(bytes(alt))[k]:
                correct += 1
            tot += 1
    return correct / max(tot, 1)


def run_gate(delta, seed, smoke):
    torch, M, cfg, Struct = H._load(smoke=smoke)
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    panels = B.build_delta(delta)
    drill = panels["drill"]
    free_slots = B._panel_free_slots(panels["f2d"])         # {0,1,2,4} recomputed
    cpt_steps = 200 if smoke else 8000
    drill_steps = 400 if smoke else 1500
    fit_items = 16 if smoke else 48

    # shared CPT (delta-independent; NSMC or fallback corpus)
    cpt_win = H._cpt_windows(H._nsmc_lines(2000 if smoke else 120000), 512, torch)
    torch.manual_seed(seed)
    model = Struct(cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=H._BASE_LR)
    for _ in range(cpt_steps):
        w = cpt_win[torch.randint(0, cpt_win.shape[0], (16,))].to(device)
        out = model(w[:, :-1], targets=w[:, 1:])
        opt.zero_grad(); out["loss"].backward(); opt.step()

    # (A) frozen-trunk probe phi[4k+1] -> hp
    fm = model.eval()
    X, y = [], []
    for it in drill[:200]:
        phi = node_phi_v5(fm, torch, it, device).cpu().numpy()
        for k, c in enumerate(it["conjuncts"]):
            X.append(phi[4 * k + 1]); y.append(int(c["hp"]))
    X = np.asarray(X, np.float32); y = np.asarray(y, np.float32)
    rng = np.random.default_rng(seed); perm = rng.permutation(len(X)); X, y = X[perm], y[perm]
    ntr = int(0.7 * len(X))
    probe = torch.nn.Linear(X.shape[1], 1).to(device)
    po = torch.optim.Adam(probe.parameters(), lr=1e-2)
    Xt = torch.tensor(X[:ntr], device=device); yt = torch.tensor(y[:ntr], device=device)
    for _ in range(500):
        po.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy_with_logits(probe(Xt).squeeze(-1), yt) \
            + 1e-3 * probe.weight.pow(2).sum()
        loss.backward(); po.step()
    with torch.no_grad():
        Xv = torch.tensor(X[ntr:], device=device); yv = torch.tensor(y[ntr:], device=device)
        probe_acc = float(((probe(Xv).squeeze(-1) > 0).float() == yv).float().mean())

    # (B) control in-sample fit: A-hand field injected, overfit fit_items, in-sample free-slot d_acc.
    torch.manual_seed(seed + 1)
    model2 = Struct(cfg).to(device)
    model2.load_state_dict(model.state_dict())              # start from the CPT'd trunk
    opt2 = torch.optim.Adam(model2.parameters(), lr=H._BASE_LR)
    fit = drill[:fit_items]
    for _ in range(drill_steps):
        it = fit[int(torch.randint(0, len(fit), (1,)))]
        surf_b, gold_b = _seq_bytes(it)
        seq = surf_b + gold_b
        struct, _ = struct_for_v5(model2, torch, it, "A-duel", device, len(seq))
        toks = torch.tensor(list(seq), dtype=torch.long, device=device)[None]
        out = model2(toks[:, :-1], targets=toks[:, 1:], struct=struct[None][:, :-1])
        opt2.zero_grad(); out["loss"].backward(); opt2.step()
    insample = dacc_v5(model2.eval(), torch, fit, "A-duel", device, list(free_slots))

    p_ok = probe_acc >= 0.90
    f_ok = insample >= 0.95
    res = {"delta": delta, "seed": seed, "smoke": smoke, "d": cfg.d_model,
           "probe_acc": round(probe_acc, 4), "probe_pass": p_ok,
           "insample_dacc": round(insample, 4), "insample_pass": f_ok,
           "pass": p_ok and f_ok, "free_slots": list(free_slots), "n_fit": fit_items}
    tag = "smoke" if smoke else f"d{delta}_s{seed}"
    json.dump(res, open(os.path.join(_HERE, f"g0k_{tag}.json"), "w"), indent=2)
    print(f"G-0k d{delta} s{seed} (d={cfg.d_model}): probe={round(probe_acc,4)} (>=0.90:{p_ok}) - "
          f"in-sample d_acc={round(insample,4)} (>=0.95:{f_ok}) - PASS={p_ok and f_ok}")
    return res


def _train_arm(torch, Struct, cfg, cpt_state, arm, drill, steps, device, seed):
    """Fresh model clone from the shared CPT state, trained on the FULL drill with `arm`'s struct field."""
    torch.manual_seed(seed)
    m = Struct(cfg).to(device)
    m.load_state_dict(cpt_state)
    opt = torch.optim.Adam(m.parameters(), lr=H._BASE_LR)
    for _ in range(steps):
        it = drill[int(torch.randint(0, len(drill), (1,)))]
        surf_b, gold_b = _seq_bytes(it)
        seq = surf_b + gold_b
        struct, _ = struct_for_v5(m, torch, it, arm, device, len(seq))
        toks = torch.tensor(list(seq), dtype=torch.long, device=device)[None]
        out = m(toks[:, :-1], targets=toks[:, 1:], struct=struct[None][:, :-1])
        opt.zero_grad(); out["loss"].backward(); opt.step()
    return m.eval()


def run_g1(delta, seed, smoke):
    """G-1 CONTROLS-FIRST kill-fast (SPEC G-1 protocol). Train the CEILING control (C-trained = zero field)
    on the full drill FIRST, measure HELD-OUT f2d free-slot d_acc; only if it is sub-ceiling (<=0.80) do we
    spend the hand arm (A-hand) — the H_007-lesson-respecting order. Gates (both seeds, f2d never trained):
    C-trained f2<=0.80 (ceiling) · A-hand-C>=0.20 (reachability) · A-hand f2>=0.90 (floor)."""
    torch, M, cfg, Struct = H._load(smoke=smoke)
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    panels = B.build_delta(delta)
    drill = panels["drill"]
    free = list(B._panel_free_slots(panels["f2d"]))
    cpt_steps = 200 if smoke else 8000
    drill_steps = 400 if smoke else 4000

    cpt_win = H._cpt_windows(H._nsmc_lines(2000 if smoke else 120000), 512, torch)
    torch.manual_seed(seed)
    model = Struct(cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=H._BASE_LR)
    for _ in range(cpt_steps):
        w = cpt_win[torch.randint(0, cpt_win.shape[0], (16,))].to(device)
        out = model(w[:, :-1], targets=w[:, 1:])
        opt.zero_grad(); out["loss"].backward(); opt.step()
    cpt_state = {k: v.clone() for k, v in model.state_dict().items()}

    def _ev(m, arm):
        return {"f2": round(dacc_v5(m, torch, panels["f2d"], arm, device, free), 4),
                "f1": round(dacc_v5(m, torch, panels["f1d"], arm, device, free), 4),
                "drill": round(dacc_v5(m, torch, drill[:64], arm, device, free), 4)}

    # CONTROLS-FIRST: the ceiling control
    ct = _train_arm(torch, Struct, cfg, cpt_state, "C-trained", drill, drill_steps, device, seed + 10)
    cte = _ev(ct, "C-trained")
    ceiling_ok = cte["f2"] <= 0.80
    res = {"delta": delta, "seed": seed, "smoke": smoke, "d": cfg.d_model,
           "C_trained": cte, "ceiling_pass": ceiling_ok}
    if not ceiling_ok:
        res["verdict"] = "INADMISSIBLE-saturated"        # H_007 redux — kill-fast, hand arm NOT trained
        res["A_hand"] = None
    else:
        ah = _train_arm(torch, Struct, cfg, cpt_state, "A-duel", drill, drill_steps, device, seed + 20)
        ahe = _ev(ah, "A-duel")
        reach = ahe["f2"] - cte["f2"] >= 0.20
        floor = ahe["f2"] >= 0.90
        valid = ahe["drill"] >= 0.95 and cte["drill"] >= 0.95   # run-integrity: both arms actually fit
        if not valid:
            verdict = "INVALID-fit"                              # undertrained (e.g. d=64 smoke) — retrain
        elif reach and floor:
            verdict = "ADMISSIBLE"
        else:
            verdict = "FAIL-headroom"                            # hand arm has no exclusive held-out edge
        res.update({"A_hand": ahe, "reach_pass": reach, "floor_pass": floor, "fit_valid": valid,
                    "verdict": verdict})
    tag = "smoke" if smoke else f"d{delta}_s{seed}"
    json.dump(res, open(os.path.join(_HERE, f"g1_{tag}.json"), "w"), indent=2)
    ah_f2 = res.get("A_hand", {}).get("f2") if res.get("A_hand") else "—(kill-fast)"
    print(f"G-1 d{delta} s{seed} (d={cfg.d_model}): C-trained f2={cte['f2']} (<=0.80:{ceiling_ok}) - "
          f"A-hand f2={ah_f2} - VERDICT={res['verdict']}")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--g1", action="store_true", help="G-1 controls-first ceiling protocol")
    ap.add_argument("--delta", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.g1:
        r = run_g1(a.delta, a.seed, a.smoke)
        return 0 if r["verdict"] == "ADMISSIBLE" else 1
    if a.smoke:
        r = run_gate(1, 0, True)
        return 0 if r["pass"] else 1
    if a.sweep:
        consec = 0
        for d in range(1, 6):
            seeds = [run_gate(d, s, False) for s in (0, 1)]
            dpass = all(r["pass"] for r in seeds)
            consec = consec + 1 if dpass else 0
            print(f"  delta{d}: both-seed PASS={dpass} - consecutive={consec}")
            if consec >= 2:
                print("MOUNT: >=2 consecutive delta pass (probe>=0.90 AND in-sample>=0.95 both seeds)")
                return 0
        print("FOLD (K-fold-1): no >=2 consecutive in-window delta")
        return 1
    r = run_gate(a.delta, a.seed, False)
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
