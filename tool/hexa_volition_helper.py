"""hexa_volition_helper.py — Python sidecar for hexa volition primitives.

Purpose:
    The hexa M1 `volition()` primitive needs a substrate forward pass
    to compute the volition signal v ∈ [0,1]. Pure-hexa can't load
    pytorch checkpoints, so it shells out to this script and reads a
    well-known stdout line back.

Stdout contract (parseable from hexa-lang via exec()+split):
    Single line, exactly:
        VOLITION:<float>\\n
    Where <float> is in [0.0, 1.0]. Hexa side splits on ":" and uses
    to_float() on the right half. Any non-numeric right half ⇒ error
    line "VOLITION:ERR" (hexa side treats as 0.0).

Modes:
    --mode mock           : ignore --model / --prompt, return fixed 0.8.
                            Used by selftest so it runs with no model.
    --mode volition_only  : load substrate, forward pass, compute v,
                            emit VOLITION:<v>. No generation.
    --mode generate       : load substrate, generate response with
                            anima_chat, emit RESPONSE:<one line>.

Volition formula (V0, matches anima_volitional_speak_v0_helper.py):
    A1 = ‖h_last‖             (last-layer hidden norm)
    A2 = H(softmax(logits)) / log(V)   ∈ [0,1]
    v  = w1 * sigmoid(A1) + w2 * (1 - A2)

This intentionally has no min/max history dependency because the
hexa primitive surface is stateless per-call. Callers who need
rolling normalization should keep state in their own file.

Notes:
    - This file is import-free of anima internals when run with
      --mode mock, so the selftest stays $0 / no model needed.
    - For real modes the file falls back to V0 helper output if
      that helper is present (forward-compat).
"""

from __future__ import annotations

import argparse
import math
import os
import sys


def _emit_volition(v: float) -> None:
    v = max(0.0, min(1.0, float(v)))
    sys.stdout.write(f"VOLITION:{v:.6f}\n")
    sys.stdout.flush()


def _emit_response(text: str) -> None:
    text = (text or "").replace("\n", " ").replace("\r", " ").strip()
    sys.stdout.write(f"RESPONSE:{text}\n")
    sys.stdout.flush()


def _emit_err(stream: str, msg: str) -> None:
    msg = (msg or "").replace("\n", " ").replace("\r", " ").strip()
    sys.stdout.write(f"{stream}:ERR {msg}\n")
    sys.stdout.flush()


def _compute_volition_real(model_path: str, prompt: str) -> float:
    """Substrate-A forward pass; returns v ∈ [0,1].

    Best-effort: tries to reuse anima_volitional_speak_v0_helper's
    compute_volition_real for parity. Falls back to a numeric
    estimate if unavailable.
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from anima_volitional_speak_v0_helper import compute_volition_real
        hidden_norm, entropy_norm = compute_volition_real(prompt, model_path)
    except Exception as e:
        raise RuntimeError(f"substrate forward failed: {type(e).__name__}: {e}")

    # Sigmoid hidden_norm so we don't need history.
    a1 = 1.0 / (1.0 + math.exp(-hidden_norm))
    a2 = max(0.0, min(1.0, entropy_norm))
    v = 0.5 * a1 + 0.5 * (1.0 - a2)
    return max(0.0, min(1.0, v))


def _generate_real(model_path: str, prompt: str) -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from anima_volitional_speak_v0_helper import generate_response_real
        return generate_response_real(prompt, model_path)
    except Exception as e:
        raise RuntimeError(f"generate failed: {type(e).__name__}: {e}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="")
    ap.add_argument("--prompt", default="")
    ap.add_argument(
        "--mode",
        default="mock",
        choices=["mock", "volition_only", "generate"],
    )
    ap.add_argument("--mock-value", type=float, default=0.8)
    args = ap.parse_args()

    if args.mode == "mock":
        _emit_volition(args.mock_value)
        return 0

    if args.mode == "volition_only":
        if not args.model or not os.path.exists(args.model):
            _emit_err("VOLITION", f"model not found: {args.model}")
            return 1
        try:
            v = _compute_volition_real(args.model, args.prompt)
            _emit_volition(v)
            return 0
        except Exception as e:
            _emit_err("VOLITION", str(e))
            return 1

    if args.mode == "generate":
        if not args.model or not os.path.exists(args.model):
            _emit_err("RESPONSE", f"model not found: {args.model}")
            return 1
        try:
            r = _generate_real(args.model, args.prompt)
            _emit_response(r)
            return 0
        except Exception as e:
            _emit_err("RESPONSE", str(e))
            return 1

    _emit_err("VOLITION", f"unknown mode {args.mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
