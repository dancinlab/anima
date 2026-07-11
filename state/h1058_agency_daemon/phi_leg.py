#!/usr/bin/env python3
"""H_1058 agency-T — faithful-Phi leg (FABLE §3.5 · a_phi_iit4_tool, NO proxy).

Per-decision faithful IIT-4.0 Phi on the H_1042 engine-native PRE-MoE trunk tap of the MOUNTED
model's .clm, so the falsifier's leg (b) rho(T,Phi) can be evaluated. Reuses the H_1042 method
VERBATIM (copied into this state dir, not imported from archive — a_no_archive_import):

  - trunk tap = embed -> ec-conv -> L x (conv + GroupNorm + GELU residual), BEFORE the router/
    expert head (fwd_trunk_preMoE), via the CANONICAL engine-native core/decode ops. KEPT
    (H_1042 canonical; demonstrably transmits input differences) — NO tap-shopping DoF.
  - BOTH stdlib IIT-4.0 CPU mirrors (h1004 big_phi + faithful_phi) RE-PROVEN == stdlib at n=5
    BEFORE scoring (prove_mirrors_at_n; a_phi_iit4_tool). n=5 EXACT (faithful-IIT4 bound).

── H_9269 Φ-LEG REDESIGN (this file · FABLE Φ-leg redesign · ALL knobs FROZEN, no tune-to-green) ──
Root cause the redesign fixes: Φ was decision-INVARIANT because (i) the daemon's decode-seed bytes
were constant per session by construction and (ii) the context window read own-emit bytes only, so
the scored suffix was a session-constant → sd(Φ)=0 → the leg-b F-shuffle null collapsed to zero
width (rendered as a false PASS before the #3331 VOID guard). Unitization/IIT4 were INNOCENT.

  1. Context source  = the TRUE consumed bytes (per-tick decode `seed_b64` + the emitted `gtext_b64`,
     as actually fed to the mouth), last-T window. Backward-compat: if `seed_b64` is absent the leg
     falls back to the old own-emit-only reconstruction (still at the new T).
  2. Window T        = 64 bytes (was 24) — spans seed + emission tail, ~3x the MI sample count.
     Trunk-forward cost is linear in T (trivial); IIT4 cost is unchanged (exponential only in n).
  3. n_units         = 5 EXACT (faithful-IIT4 bound; prove_mirrors_at_n(5) stays the STEP-0 gate).
  4. Unit selection  = FROZEN ONCE per session on a CALIBRATION slice (first CALIB_TICKS decisions,
     EXCLUDED from scoring; calibration ∩ scored = ∅). Rank dims by the variance of the per-window
     time-mean ACROSS calibration decisions, take top-5. Signal-blind (never sees T / labels / Φ) —
     NOT per-decision re-selection, NOT within-window variance.
  5. Binarization    = FROZEN per-unit thresholds = each unit's median over the POOLED calibration
     slice (NOT a per-decision median, which would erase cross-decision level info).
  6. Macro-maps      = 2, both frozen pre-scoring: `top_calib_variance` (the top-5 above) + a seeded
     `random` 5-dim map.

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
T_WIN = 64                 # H_9269: 24 -> 64 (spans seed + emission tail; ~3x MI samples)
CALIB_TICKS = 50           # first N decisions = signal-blind unit-selection slice (EXCLUDED from scoring)
RAND_SEED = 20260608
MACRO_MAPS = ["top_calib_variance", "random"]


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


# ════════════════════════════════════════════════════════════════════════
# H_9269 FROZEN unitization — calibrate ONCE, score with the frozen maps.
# Pure numpy (no .clm): directly unit-testable on synthetic latents.
# ════════════════════════════════════════════════════════════════════════

def calibrate_units(calib_H, n_units=N_UNITS, rand_seed=RAND_SEED):
    """FROZEN unit selection + binarization thresholds from the calibration slice.

    calib_H : list of (T x d) PRE-MoE trunk-hidden arrays, one per CALIBRATION decision
              (the first CALIB_TICKS decisions; EXCLUDED from scoring — calib ∩ scored = ∅).

    Returns {map_name: {"idx": (n_units,) int, "thr": (n_units,) float}} — frozen before any
    scored Φ is computed. Signal-blind: this fn never sees T, labels, or Φ.

      * top_calib_variance : rank dims by the variance of the per-window time-mean ACROSS
        calibration decisions (cross-decision level variance, NOT within-window variance),
        take the top-`n_units`.
      * random             : a seeded random `n_units`-dim map (frozen pre-scoring).
      * thresholds         : per-unit median over the POOLED calibration slice (all calib
        decisions × T rows), NOT a per-decision median.
    """
    mats = [np.asarray(H, float) for H in calib_H]
    if len(mats) < 2:
        raise ValueError("calibrate_units: need >=2 calibration decisions, got %d" % len(mats))
    d = mats[0].shape[1]
    # per-decision time-mean -> (n_calib x d); variance ACROSS calibration decisions
    M = np.stack([H.mean(axis=0) for H in mats], axis=0)
    var_across = M.var(axis=0)
    idx_top = np.sort(np.argsort(var_across)[::-1][:n_units])
    rng = np.random.default_rng(rand_seed)
    idx_rand = np.sort(rng.choice(d, size=n_units, replace=False))
    pooled = np.concatenate(mats, axis=0)          # (n_calib*T x d) pooled calibration slice
    frozen = {}
    for name, idx in (("top_calib_variance", idx_top), ("random", idx_rand)):
        thr = np.median(pooled[:, idx], axis=0)    # per-unit median over the pooled slice
        frozen[name] = {"idx": idx, "thr": thr}
    return frozen


def bits_from_frozen(H, idx, thr):
    """Binarize a (T x d) window at the FROZEN units/thresholds -> (T x n_units) int."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    chans = H[:, idx]
    return (chans > thr).astype(int)


def faithful_phi_frozen(H, frozen_map):
    """Faithful IIT-4.0 Φ of a window under one frozen macro-map (n_units EXACT)."""
    bits = bits_from_frozen(H, frozen_map["idx"], frozen_map["thr"])
    n = bits.shape[1]
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
    """T-byte context for decision i = the TRUE consumed bytes as fed to the mouth.

    H_9269 context source: per-tick decode `seed_b64` (Part A1 side-channel) + the emitted
    `gtext_b64`, last-T window (spans seed + emission tail). Backward-compat: if `seed_b64` is
    absent, reconstruct from own-emit bytes only (the old behavior), still at the new T. Short
    windows are left-padded with the session seed."""
    seed_pad = meta["session_seed"].encode("utf-8", "surrogateescape")
    r = rows[i]
    if r.get("seed_b64"):
        consumed = bytearray(base64.b64decode(r["seed_b64"]))
        if r.get("gen_emitted") and r.get("gtext_len", 0) > 0 and r.get("gtext_b64"):
            consumed += base64.b64decode(r["gtext_b64"])
        acc = bytes(consumed)
    else:
        buf = bytearray()
        for j in range(i):
            rj = rows[j]
            if rj.get("gen_emitted") and rj.get("gtext_len", 0) > 0:
                buf += base64.b64decode(rj["gtext_b64"])
        acc = bytes(buf)
    if len(acc) < T_WIN:
        acc = (seed_pad * ((T_WIN // max(1, len(seed_pad))) + 1))[:T_WIN - len(acc)] + acc
    win = bytes(acc[-T_WIN:])
    return np.frombuffer(win, dtype=np.uint8, count=T_WIN).astype(float)


def sample_decisions(rows, max_emit, seed, calib_ticks=CALIB_TICKS):
    """all ACTIVE_VETO + a matched EMIT/PASSIVE sample, EXCLUDING calibration ticks (<calib_ticks).
    calib ∩ scored = ∅ (frozen-unit slice never re-enters scoring)."""
    rng = random.Random(seed)
    def elig(i):
        return i >= calib_ticks
    active = [i for i, r in enumerate(rows) if r["cls"] == "ACTIVE_VETO" and elig(i)]
    emit = [i for i, r in enumerate(rows) if r["cls"] == "EMIT" and elig(i)]
    passive = [i for i, r in enumerate(rows) if r["cls"] == "PASSIVE" and elig(i)]
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

    print("=== H_1058 faithful-Phi leg (a_phi_iit4_tool · H_9269 redesign) · dtype=%s ===" % _DTYPE_NAME, flush=True)
    print("STEP 0 — RE-PROVE stdlib IIT-4.0 mirror == stdlib at n=5 (no proxy):", flush=True)
    if not bool(prove_mirrors_at_n(N_UNITS)):
        print("ABORT — mirror==stdlib proof FAILED."); return 1

    print("STEP 0b — load .clm + decode-sanity:", args.clm, flush=True)
    tL = time.time()
    W = dec.clm_load_weights(args.clm)
    assert W.get("ok"), "clm_load_weights failed / not decodable"
    print("   loaded d=%s E=%s V=%s L=%s K=%s in %.1fs"
          % (W["d"], W.get("E"), W["V"], W["L"], W["K"], time.time() - tL), flush=True)
    _pt = b"The mind is a fire to be kindled, not a vessel to be filled by us."
    probe = np.frombuffer((_pt + b" " * T_WIN)[:T_WIN], dtype=np.uint8, count=T_WIN).astype(float)
    logits = dec._fwd_logits(W, probe, T_WIN)
    V = W["V"]
    tgt = np.concatenate([probe[1:], [ord('.')]])
    ce_real = dec.nn_ce_loss_allpos(logits, tgt, T_WIN, V)
    print("   decode-sanity CE=%.5f < ln(V)=%.5f: %s" % (ce_real, math.log(V), ce_real < math.log(V)), flush=True)
    if not (ce_real < math.log(V)):
        print("   ABORT — .clm does not descend."); return 1

    meta, rows = load_trace(args.trace)

    # STEP 1 — FROZEN calibration (signal-blind; calib ∩ scored = ∅)
    calib_idx = list(range(min(CALIB_TICKS, len(rows))))
    if len(calib_idx) < 2:
        print("   ABORT — <2 calibration decisions (need >=2 for frozen unit selection)."); return 1
    print("STEP 1 — calibrate frozen units on the first %d decisions (EXCLUDED from scoring):"
          % len(calib_idx), flush=True)
    tC = time.time()
    calib_H = []
    for k, i in enumerate(calib_idx):
        tok = context_window(rows, i, meta)
        calib_H.append(fwd_trunk_preMoE(W, tok, T_WIN))
    frozen = calibrate_units(calib_H)
    for mp in MACRO_MAPS:
        print("   [%s] units=%s thr=%s"
              % (mp, list(map(int, frozen[mp]["idx"])),
                 [round(float(x), 3) for x in frozen[mp]["thr"]]), flush=True)
    print("   calibrated in %.1fs" % (time.time() - tC), flush=True)

    # STEP 2 — score with the FROZEN maps
    keep = sample_decisions(rows, args.max_emit, args.seed)
    if not keep:
        print("   WARN — 0 scored decisions after excluding calibration slice (leg -> VOID downstream).")
    print("STEP 2 — Phi on %d scored decisions x %d frozen macro-maps (trunk fwd each):"
          % (len(keep), len(MACRO_MAPS)), flush=True)
    t0 = time.time()
    out = []
    for k, i in enumerate(keep):
        tok = context_window(rows, i, meta)
        H = fwd_trunk_preMoE(W, tok, T_WIN)      # one 3B trunk forward, shared across maps
        for mp in MACRO_MAPS:
            phi = faithful_phi_frozen(H, frozen[mp])
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
