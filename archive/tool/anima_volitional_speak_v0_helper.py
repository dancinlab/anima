"""anima_volitional_speak_v0_helper.py — V0 volition gate (substrate A).

Purpose:
    one-shot helper: load substrate A → forward pass on seed prompt →
    compute volition signal v = w1*norm(‖h_last‖) + w2*(1-norm_entropy).
    If v > τ AND not in refractory: generate response. Else: emit silent.
    Print single-line JSON to stdout (the hexa main loop parses it).

Volition formula (V0, 2026-05-12):
    A1 = ‖h_last‖  (last-layer hidden norm, scalar)
    A2 = H(softmax(logits_last)) / log(V)   ∈ [0,1]
    norm(A1) using min/max from --history-file (rolling buffer)
    v = w1 * norm_A1 + w2 * (1 - A2)         # low entropy ⇒ confident ⇒ want-to-say
    speak iff v > τ AND (now - last_emit) ≥ refractory_s

Dry-run mode (--dry-run):
    bypass model load; simulate hidden_norm and entropy from numpy random.
    used when substrate not available or for fast hexa smoke test.

Output JSON keys:
    iter, ts, hidden_norm, norm_A1, entropy_norm, v_raw, v_smoothed, tau,
    refractory_blocked, decision, response, elapsed_s, dry_run, error
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np


def _ts_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_history(path: str) -> list:
    p = Path(path)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text())
    except Exception:
        return []


def save_history(path: str, hist: list, cap: int = 32) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(hist[-cap:]))


def min_max_norm(x: float, samples: list) -> float:
    if len(samples) < 2:
        return 0.5
    lo = min(samples)
    hi = max(samples)
    if hi - lo < 1e-9:
        return 0.5
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def compute_volition_dry(seed: str, iter_idx: int) -> tuple:
    rng = np.random.default_rng(seed=hash((seed, iter_idx)) % (2**32))
    hidden_norm = float(rng.uniform(0.5, 2.5))
    entropy_norm = float(rng.uniform(0.3, 0.9))
    return hidden_norm, entropy_norm


def compute_volition_real(seed: str, ckpt_path: str) -> tuple:
    import torch

    anima_root = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
    sys.path.insert(0, str(anima_root))
    sys.path.insert(0, str(anima_root / "training"))
    from training.engine_a_g_arch import EngineAGModel, EngineAGConfig  # noqa: E402

    ck = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg = (
        EngineAGConfig(**ck["cfg"])
        if isinstance(ck.get("cfg"), dict)
        else EngineAGConfig()
    )
    model = EngineAGModel(cfg).to("cpu")
    model.load_state_dict(ck["model"], strict=False)
    model.eval()

    ids = [1] + [b + 3 for b in seed.encode("utf-8")] + [2]
    if ids and ids[-1] == 2:
        ids = ids[:-1]
    x = torch.tensor([ids[-cfg.ctx :]], dtype=torch.long)

    with torch.no_grad():
        out = model(x, output_hidden_states=True)
    hs = out["hidden_states"]
    h_last = hs[-1][0, -1]
    hidden_norm = float(h_last.norm().item())

    logits = out["logits"][0, -1]
    p = torch.softmax(logits.float(), dim=-1)
    eps = 1e-12
    H = float(-(p * (p + eps).log()).sum().item())
    H_max = math.log(logits.shape[-1])
    entropy_norm = H / H_max if H_max > 0 else 0.0
    return hidden_norm, entropy_norm


def generate_response_real(seed: str, ckpt_path: str, max_new: int = 60) -> str:
    anima_root = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
    sys.path.insert(0, str(anima_root))
    from anima_chat import AnimaChat  # noqa: E402

    chat = AnimaChat(ckpt_path=ckpt_path)
    return chat(seed, max_new=max_new, mode="M4_force_include")


def _resolve_default_ckpt() -> str:
    candidates = [
        "/Users/ghost/.cache/anima/clm_v5_remapped/"
        "phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
        str(Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
            / ".cache/anima/clm_v5_remapped/"
              "phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="도우미: ")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--tau", type=float, default=0.7)
    ap.add_argument("--w1", type=float, default=0.5)
    ap.add_argument("--w2", type=float, default=0.5)
    ap.add_argument("--refractory-s", type=int, default=30)
    ap.add_argument("--history-file", default="")
    ap.add_argument("--last-emit-file", default="")
    ap.add_argument("--iter", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-generate", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    err = None
    response = None
    hidden_norm = 0.0
    entropy_norm = 0.0

    try:
        if args.dry_run:
            hidden_norm, entropy_norm = compute_volition_dry(args.seed, args.iter)
        else:
            ckpt = args.ckpt or os.environ.get("ANIMA_VOLITION_CKPT", "") or _resolve_default_ckpt()
            if not ckpt or not os.path.exists(ckpt):
                raise FileNotFoundError("substrate A ckpt not found (tried defaults)")
            hidden_norm, entropy_norm = compute_volition_real(args.seed, ckpt)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"

    hist_path = args.history_file or "/tmp/_volition_hist.json"
    hist = load_history(hist_path)
    hist_norms = [h.get("hidden_norm", 0.0) for h in hist]
    norm_A1 = min_max_norm(hidden_norm, hist_norms)
    hist.append({"ts": _ts_iso(), "hidden_norm": hidden_norm,
                 "entropy_norm": entropy_norm})
    try:
        save_history(hist_path, hist)
    except Exception:
        pass

    v_raw = args.w1 * norm_A1 + args.w2 * (1.0 - entropy_norm)
    v_smoothed = v_raw

    refractory_blocked = False
    last_emit_path = args.last_emit_file or "/tmp/_volition_last_emit"
    if os.path.exists(last_emit_path):
        try:
            last_ts = float(Path(last_emit_path).read_text().strip())
            if time.time() - last_ts < args.refractory_s:
                refractory_blocked = True
        except Exception:
            pass

    decision = "silent"
    if err is None and v_smoothed > args.tau and not refractory_blocked:
        decision = "emit"
        if not args.no_generate:
            try:
                if args.dry_run:
                    response = f"[dry-run emit @ iter={args.iter}] v={v_smoothed:.3f}"
                else:
                    ckpt = args.ckpt or _resolve_default_ckpt()
                    response = generate_response_real(args.seed, ckpt)
            except Exception as e:
                err = f"generate_failed: {type(e).__name__}: {e}"
                response = None
        try:
            Path(last_emit_path).parent.mkdir(parents=True, exist_ok=True)
            Path(last_emit_path).write_text(str(time.time()))
        except Exception:
            pass

    rec = {
        "iter": args.iter,
        "ts": _ts_iso(),
        "hidden_norm": round(hidden_norm, 4),
        "norm_A1": round(norm_A1, 4),
        "entropy_norm": round(entropy_norm, 4),
        "v_raw": round(v_raw, 4),
        "v_smoothed": round(v_smoothed, 4),
        "tau": args.tau,
        "w1": args.w1,
        "w2": args.w2,
        "refractory_blocked": refractory_blocked,
        "decision": decision,
        "response": response,
        "elapsed_s": round(time.time() - t0, 3),
        "dry_run": args.dry_run,
        "error": err,
    }
    print("VOLITION_JSON " + json.dumps(rec, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
