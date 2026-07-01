"""kv_parity.py — byte-exactness gate for the bytegpt_decode.py KV-cache (PR-twin
of core/bytegpt_decode.hexa PR #2602). Compares KV-cache ON vs OFF (forced
full-forward) on the SAME seed/prompt/gen → must be byte-identical (logits + token
stream). Also times before/after. Per a_engine_native_learning: divergence is a
result (not hidden) — KV bug isolated.

usage: python3 kv_parity.py <bin> <seed> <gen> [top_k] [temp] [seed_rng]
       default: argmax parity + sampled parity, small gen for the 303M wall.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import numpy as np
import bytegpt_decode as bg


def _argmax_off(W, seed_ids, gen):
    """forced full-forward greedy (KV-cache OFF) — the reference path verbatim."""
    vocab = W["vocab"]; block = W["block"]
    toks = bg._seed_to_ids(seed_ids); outl = []
    for _ in range(gen):
        n = len(toks); start = n - block if n > block else 0; T = n - start
        ids = toks[start:start + T]
        logits = bg.bg_forward_last_W(W, ids, T)
        nb = bg.bg_argmax(logits); toks.append(nb); outl.append(nb)
    return outl


def _sampled_off(W, seed_ids, gen, top_k, temp, seed_rng):
    """forced full-forward sampled (KV-cache OFF) — reference path verbatim."""
    vocab = W["vocab"]; block = W["block"]
    toks = bg._seed_to_ids(seed_ids); outl = []
    rng = bg._mix32(seed_rng)
    for _ in range(gen):
        n = len(toks); start = n - block if n > block else 0; T = n - start
        ids = toks[start:start + T]
        logits = bg.bg_forward_last_W(W, ids, T)
        nb, rng = bg._topk_sample(logits, vocab, top_k, temp, rng)
        toks.append(nb); outl.append(nb)
    return outl


def main(argv):
    binp = argv[1] if len(argv) > 1 else os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
    seed = argv[2] if len(argv) > 2 else "The capital of France is"
    gen = int(argv[3]) if len(argv) > 3 else 12
    top_k = int(argv[4]) if len(argv) > 4 else 40
    temp = float(argv[5]) if len(argv) > 5 else 0.7
    seed_rng = int(argv[6]) if len(argv) > 6 else 7

    print(f"# ckpt={binp}")
    print(f"# seed={seed!r} gen={gen} top_k={top_k} temp={temp} seed_rng={seed_rng}")
    t0 = time.time()
    W = bg.bg_load(binp)
    print(f"# bg_load: {time.time()-t0:.1f}s  hdr={ {k:W[k] for k in ('vocab','d','nlay','nh','block')} }")

    # ── ARGMAX parity ───────────────────────────────────────────────
    t = time.time(); off = _argmax_off(W, seed, gen); t_off = time.time() - t
    t = time.time(); on = bg._decode_argmax_W(W, seed, gen)["ids"]; t_on = time.time() - t
    arg_ident = (off == on)
    print(f"[ARGMAX] OFF={off}")
    print(f"[ARGMAX] ON ={on}")
    print(f"[ARGMAX] byte-identical={arg_ident}  t_off={t_off:.1f}s ({t_off/gen*1000:.0f}ms/tok)  t_on={t_on:.1f}s ({t_on/gen*1000:.0f}ms/tok)  speedup={t_off/max(t_on,1e-9):.1f}x")

    # ── logit-level parity at last seed position (no-gen, primes only) ──
    seed_ids = bg._seed_to_ids(seed); ns = len(seed_ids)
    lg_off = bg.bg_forward_last_W(W, seed_ids, ns)
    kv = bg._bg_kv_new(W["nlay"], W["block"], W["d"]); lg_on = None
    for sp in range(ns):
        lg_on = bg._bg_kv_step(W, kv, seed_ids[sp], sp)
    dmax = float(np.max(np.abs(np.asarray(lg_off) - np.asarray(lg_on))))
    print(f"[LOGITS] last-seed-pos max|Δ|={dmax:.3e}  argmax_off={bg.bg_argmax(lg_off)} argmax_on={bg.bg_argmax(lg_on)}")

    # ── SAMPLED parity ──────────────────────────────────────────────
    t = time.time(); soff = _sampled_off(W, seed, gen, top_k, temp, seed_rng); t_soff = time.time() - t
    t = time.time(); son = bg.bytegpt_decode_topk_sampled_W(W, seed, gen, top_k, temp, seed_rng)["ids"]; t_son = time.time() - t
    s_ident = (soff == son)
    print(f"[SAMPLE] OFF={soff}")
    print(f"[SAMPLE] ON ={son}")
    print(f"[SAMPLE] byte-identical={s_ident}  t_off={t_soff:.1f}s  t_on={t_son:.1f}s  speedup={t_soff/max(t_son,1e-9):.1f}x")

    # GATE (hexa standard): token streams byte-identical (the real byte-exactness gate)
    # AND last-pos argmax stable. The logit max|Δ| is FP-reassociation only (~e-14,
    # same class as the hexa ikj-vs-scalar 4.97e-14) — below argmax-flip tolerance.
    argmax_stable = (bg.bg_argmax(lg_off) == bg.bg_argmax(lg_on))
    ok = arg_ident and s_ident and argmax_stable and dmax < 1e-9
    print(f"\nPARITY {'PASS' if ok else 'FAIL'}: argmax_tok={arg_ident} sampled_tok={s_ident} "
          f"argmax_stable={argmax_stable} logits_max|Δ|={dmax:.3e} (FP-reassoc, <1e-9)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
