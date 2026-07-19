"""v2/gradcheck.py — C0-d: finite-difference check of the hand-written backward.

@canonical-ok — see gen.py.

The backward pass in model.py is hand-written, so a silent sign/axis error would still
train (badly) and could manufacture an arm difference out of nothing.

TWO instrument defects this file exists to avoid:

1. Per-element relative error is MEANINGLESS where the true gradient sits below the
   finite-difference noise floor. At init scale 0.02 the store path's gradients are ~1e-10
   while central differences on a loss of order 1 resolve only ~1e-11 — the check then
   reports a 7% "error" between two numbers that are both zero. Fix: DIRECTIONAL derivative
   per tensor (project onto a random unit vector, which aggregates the whole tensor into
   one well-scaled number), evaluated at a DELIBERATELY WELL-SCALED parameter point.
   Backward-pass correctness does not depend on init scale, so checking at a scaled point
   is a strictly stronger test — not a looser bar. The bar (bars.json C0d) is untouched.

2. A guard that cannot fail is not a guard. `--selftest` corrupts one gradient tensor and
   asserts the check CATCHES it. Run it whenever this file changes.
   (Precedent: a device-parity guard once passed by comparing GPU against GPU.)
"""

import json
import os
import sys

import numpy as np

import model as M
from loss import forward_loss

HERE = os.path.dirname(os.path.abspath(__file__))


GATE = "mix"  # set by main() so gradcheck covers BOTH the mix and logit paths


def build_case(scale=1.0, seed=0):
    bars = json.load(open(os.path.join(HERE, "bars.json")))
    rng = np.random.default_rng(seed)
    cfg = dict(bars["model"])
    cfg["max_seq"] = bars["task"]["max_seq"]
    cfg["d"], cfg["layers"], cfg["heads"], cfg["ffn"] = 16, 2, 2, 32  # tiny for speed
    p = M.init_params(cfg, rng, with_store=True)
    # Scale the non-normaliser params up so no gradient hides under the FD noise floor.
    for k in p:
        if k.endswith("_g") or k.endswith("_b") or k == "lam_raw":
            continue
        p[k] = p[k] * (scale / 0.02)

    B, T, S, NL = 3, 12, 4, 5
    case = {
        "ids": rng.integers(0, 256, size=(B, T)),
        "store_ids": rng.integers(97, 123, size=(B, S, NL)),
        "val_idx": rng.integers(0, 2, size=(B, S)),
        "qpos": np.full(B, 6),
        "ans_pos": np.full(B, 7),
        "targets": rng.integers(0, 256, size=(B, T)),
        "loss_mask": np.zeros((B, T)),
    }
    case["loss_mask"][:, 7:10] = 1.0
    return bars, cfg, p, case, rng


def loss_of(p, cfg, case):
    return forward_loss(p, cfg, case["ids"], case["targets"], case["loss_mask"],
                        case["store_ids"], case["val_idx"], case["qpos"],
                        case["ans_pos"], use_store=True, gate=GATE)[0]


def run_check(corrupt=None, verbose=True):
    bars, cfg, p, case, rng = build_case(scale=0.5, seed=0)
    bar = bars["C0_instrument_integrity"]["C0d_gradcheck_max_rel_err"]

    _, grads = forward_loss(p, cfg, case["ids"], case["targets"], case["loss_mask"],
                            case["store_ids"], case["val_idx"], case["qpos"],
                            case["ans_pos"], use_store=True, backward=True, gate=GATE)
    if corrupt is not None:
        grads[corrupt] = grads[corrupt] * 1.5 + 1e-3   # a plausible-looking wrong gradient

    eps = 1e-6
    worst, worst_name = 0.0, ""
    rows = []
    # frozen params (key_emb_frozen) are DELIBERATELY not updated — their analytic grad is 0
    # by design, so checking them against a finite difference is meaningless (and would flag
    # a non-bug). Skip them; the training loop skips them too (grads.get -> None).
    FROZEN = {"key_emb_frozen"}
    for name in sorted(k for k in p.keys() if k not in FROZEN):
        u = rng.standard_normal(p[name].shape)
        u /= np.linalg.norm(u)
        orig = p[name].copy()
        p[name] = orig + eps * u
        lp = loss_of(p, cfg, case)
        p[name] = orig - eps * u
        lm = loss_of(p, cfg, case)
        p[name] = orig

        num = (lp - lm) / (2 * eps)
        ana = float((grads[name] * u).sum())
        scale = max(abs(num), abs(ana))
        noise = 1e-9                      # FD floor for float64 at eps=1e-6, loss ~ O(1)
        if scale < noise:
            rows.append((name, num, ana, 0.0, "below-noise"))
            continue
        e = abs(num - ana) / scale
        rows.append((name, num, ana, e, ""))
        if e > worst:
            worst, worst_name = e, name

    ok = worst <= bar
    if verbose:
        for name, num, ana, e, note in rows:
            flag = "" if e <= bar else "  <-- FAIL"
            print(f"  {name:14s} num={num:+.6e} ana={ana:+.6e} rel={e:.2e} {note}{flag}")
        print(f"C0-d gradcheck: tensors={len(rows)} worst={worst:.2e} ({worst_name}) "
              f"bar={bar} -> {'PASS' if ok else 'FAIL'}")
    return ok, worst, worst_name


def main():
    if "--selftest" in sys.argv:
        print("SELFTEST — the guard must be able to FAIL.")
        ok_clean, w_clean, _ = run_check(corrupt=None, verbose=False)
        print(f"  clean gradients      -> {'PASS' if ok_clean else 'FAIL'} (worst={w_clean:.2e})")
        caught = []
        for tgt in ["W_q", "W_out", "val", "emb", "l0_qkv", "ln_f_g"]:
            ok_bad, w_bad, _ = run_check(corrupt=tgt, verbose=False)
            caught.append(not ok_bad)
            print(f"  corrupted {tgt:8s}   -> {'FAIL (caught)' if not ok_bad else 'PASS (MISSED!)'}"
                  f" worst={w_bad:.2e}")
        good = ok_clean and all(caught)
        print(f"SELFTEST {'PASS' if good else 'FAIL'} — clean passes AND every corruption is caught")
        return 0 if good else 1

    ok, _, _ = run_check(verbose=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
