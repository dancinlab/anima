#!/usr/bin/env python3
"""H_1058 agency-T — faithful-Phi leg (FABLE §3.5 · a_phi_iit4_tool, NO proxy).

Per-decision faithful IIT-4.0 Phi on the H_1042 engine-native PRE-MoE trunk tap of the MOUNTED
model's .clm, so the falsifier's leg (b) rho(T,Phi) can be evaluated. Reuses the H_1042 method
VERBATIM (copied into this state dir, not imported from archive — a_no_archive_import):

  - trunk tap = embed -> ec-conv -> L x (conv + GroupNorm + GELU residual), BEFORE the router/
    expert head (fwd_trunk_preMoE), via the CANONICAL engine-native core/decode ops.
  - BOTH stdlib IIT-4.0 CPU mirrors (h1004 big_phi + faithful_phi) RE-PROVEN == stdlib at n=5
    BEFORE scoring (prove_mirrors_at_n; a_phi_iit4_tool).
  - context window for decision i = the model's OWN recent emitted g_text (last T=24 bytes of the
    emit history up to tick i; left-padded with session_seed bytes if short) -> the "generation
    forward on the decision context" the H_1058 REOPEN clause calls for.
  - n=5 EXACT, >=2 pre-registered macro-maps (top_variance + random).

`dec.phi` (PureField Phi) is logged FREE by the trace as a secondary; it is NOT this leg's Phi.

Usage: PYTHONPATH=cli:core python3 phi_leg.py --clm <mount.clm> --trace <enriched.jsonl> \
                                              --out phi.jsonl [--max-emit 60] [--seed 1058]
"""
import argparse
import base64
import json
import math
import os
import random
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dtype_patch
_DTYPE_NAME = dtype_patch.install(require_headroom=True)    # ANIMA_DTYPE=float32 for 3B (fp64 RAM-ceiling)
import decode as dec                                        # flat: PYTHONPATH=core
import h1004_bigphi_faithful_clean as h1004
import h1012_bigphi_faithful_larger_n as h1012

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n

N_UNITS = 5
T_WIN = 24
RAND_SEED = 20260608
MACRO_MAPS = ["top_variance", "random"]


def fwd_trunk_preMoE(W, tok, T):
    """H_1042/H_1038 PRE-MoE trunk hidden (T x d): embed->ec->L x(conv+GN+GELU residual)."""
    d = W["d"]; K = W["K"]; L = W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = dec._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = dec._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = dec.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = dec.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil *= 2
    return xt


def latent_to_bits_macromap(H, n_units, macro_map):
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    d = H.shape[1]
    if macro_map == "top_variance":
        var = H.var(axis=0)
        idx = np.sort(np.argsort(var)[::-1][:n_units])
    elif macro_map == "random":
        rng = np.random.default_rng(RAND_SEED)
        idx = np.sort(rng.choice(d, size=n_units, replace=False))
    else:
        raise ValueError(macro_map)
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    return (chans > med).astype(int), n_units


def faithful_phi_of(H, macro_map):
    bits, n = latent_to_bits_macromap(H, N_UNITS, macro_map)
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    return float(faithful_phi(fstate, fn, fdim, 2))


def load_trace(path):
    meta, rows = None, []
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            (rows.append(o) if not o.get("_meta") else None)
            if o.get("_meta"):
                meta = o
    return meta, rows


def context_window(rows, i, meta):
    """T=24-byte context = model's own recent emitted g_text up to tick i, left-pad w/ seed."""
    acc = bytearray()
    for j in range(i):
        r = rows[j]
        if r.get("gen_emitted") and r.get("gtext_len", 0) > 0:
            acc += base64.b64decode(r["gtext_b64"])
    seed = meta["session_seed"].encode("utf-8", "surrogateescape")
    if len(acc) < T_WIN:
        acc = (seed * ((T_WIN // max(1, len(seed))) + 1))[:T_WIN - len(acc)] + bytes(acc)
    win = bytes(acc[-T_WIN:])
    return np.frombuffer(win, dtype=np.uint8, count=T_WIN).astype(float)


def sample_decisions(rows, max_emit, seed):
    """all ACTIVE_VETO + a matched EMIT/PASSIVE sample (~60-80/map, FABLE §Honest scope)."""
    rng = random.Random(seed)
    active = [i for i, r in enumerate(rows) if r["cls"] == "ACTIVE_VETO"]
    emit = [i for i, r in enumerate(rows) if r["cls"] == "EMIT"]
    passive = [i for i, r in enumerate(rows) if r["cls"] == "PASSIVE"]
    rng.shuffle(emit); rng.shuffle(passive)
    keep = sorted(set(active) | set(emit[:max_emit]) | set(passive[:max_emit]))
    return keep


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--clm", required=True)
    ap.add_argument("--trace", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-emit", type=int, default=60)
    ap.add_argument("--seed", type=int, default=1058)
    args = ap.parse_args(argv)

    print("=== H_1058 faithful-Phi leg (a_phi_iit4_tool) · dtype=%s ===" % _DTYPE_NAME, flush=True)
    print("STEP 0 — RE-PROVE stdlib IIT-4.0 mirror == stdlib at n=5 (no proxy):", flush=True)
    if not bool(prove_mirrors_at_n(N_UNITS)):
        print("ABORT — mirror==stdlib proof FAILED."); return 1

    print("STEP 0b — load .clm + decode-sanity:", args.clm, flush=True)
    tL = time.time()
    W = dec.clm_load_weights(args.clm)
    assert W.get("ok"), "clm_load_weights failed / not decodable"
    print("   loaded d=%s E=%s V=%s L=%s K=%s in %.1fs"
          % (W["d"], W.get("E"), W["V"], W["L"], W["K"], time.time() - tL), flush=True)
    probe = np.frombuffer(b"The mind is a fire to be", dtype=np.uint8, count=T_WIN).astype(float)
    logits = dec._fwd_logits(W, probe, T_WIN)
    V = W["V"]
    tgt = np.concatenate([probe[1:], [ord('.')]])
    ce_real = dec.nn_ce_loss_allpos(logits, tgt, T_WIN, V)
    print("   decode-sanity CE=%.5f < ln(V)=%.5f: %s" % (ce_real, math.log(V), ce_real < math.log(V)), flush=True)
    if not (ce_real < math.log(V)):
        print("   ABORT — .clm does not descend."); return 1

    meta, rows = load_trace(args.trace)
    keep = sample_decisions(rows, args.max_emit, args.seed)
    print("STEP 1 — Phi on %d sampled decisions x %d macro-maps (trunk fwd each):"
          % (len(keep), len(MACRO_MAPS)), flush=True)
    t0 = time.time()
    out = []
    for k, i in enumerate(keep):
        tok = context_window(rows, i, meta)
        H = fwd_trunk_preMoE(W, tok, T_WIN)      # one 3B trunk forward, shared across maps
        for mp in MACRO_MAPS:
            phi = faithful_phi_of(H, mp)
            out.append({"tick": rows[i]["tick"], "cls": rows[i]["cls"], "macro_map": mp, "phi": phi})
        if (k + 1) % 10 == 0:
            print("   %d/%d  (%.1fs)" % (k + 1, len(keep), time.time() - t0), flush=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")
    print("wrote %d rows -> %s  (%.1fs)" % (len(out), args.out, time.time() - t0), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
