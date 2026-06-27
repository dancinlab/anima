#!/usr/bin/env python3
"""h159x_g6_scaffold_repro.py — ENGINE-NATIVE reproduction of the H_1362 G6 ★ scaffold.

H_1362 reported G6 ★ "BREAKTHROUGH" (C_strong FALS=1.0, M1-M5 all PASS) but on the
gauge torch decode path (top-k=40 temp=0.7) = DIRECTIONAL, never engine-native
reconfirmed (the "R2 follow-on"). H_1381 wired the scaffold but only had a weak d768
ConvMoE .clm -> FALS bars FAILED engine-native (capacity floor). H_1587 documented that
torch GREEN != engine-native on the very same h1129.

This probe applies the EXACT H_1362 scaffold recipe (H_1305 6 composed conditional frames
+ best-of-K=3, FROZEN _is_falsifiable detector VERBATIM) to the SAME h1129 303M ByteGPT
ckpt, but via the **py 2-production engine** (core/g6_ideation.py <- core/bytegpt_decode.py),
which is numpy-only (NO torch, NO gauge_lib import) -> a_engine_native_learning TERMINAL.

  ARMS (H_1362 VERBATIM, bar 불변):
    A_flat       — flat IDEATION_SEEDS, single-sample (THIN baseline / sanity = fals must be 0)
    B_composed   — H_1305 5 composed frames, single-sample (prior-art reference)
    C_strong     — 6 composed frames + best-of-K=3  (the "breakthrough" arm)
    C_shuffle    — control: deranged concept pairing + best-of-K  (EARNED-PAIR)
    C_ablate     — control: lone concept, no conditional shell + best-of-K  (EARNED-COMP)
  PLUS decomposition controls (this probe's additions to isolate the lever):
    C_k1         — 6 composed frames + best-of-K=1  (best-of-K as plain single sample)
    cross-shuffle is C_shuffle above (H_1434/H_1449 decisive bar: if scaffold is real
                   binding, deranged pairing must collapse fals to the flat floor).

  FROZEN MOVE BARS (MODEL.md G6, NOT moved):
    M1 COUNT       DIST(C_strong) >= 5
    M2 DEPTH       FALS(C_strong) >= 1
    M3 LIFT        FALS(C_strong) >  FALS(B_composed)
    M4 EARNED-PAIR FALS(C_strong) >  FALS(C_shuffle)
    M5 EARNED-COMP FALS(C_strong) >  FALS(C_ablate)
    closed_G6 = M1 & M2 & M3 & M4 & M5

GREEN  iff closed AND C_shuffle collapses (real binding -> scaffold is the lever, decode-procedure).
RED    iff fals stays 0 engine-native (torch artifact, H_1587 confirmed), OR fals rises but
           C_shuffle does NOT collapse (token-presence artifact, not binding).

ckpt: h1129 303M ByteGPT .bin (sha 5cf07a36...). Pool host (aiden/summer), NOT mini.
$0 CPU numpy decode. 3 seeds [7,4302,4303]. Weights loaded ONCE per ckpt (reused via _W path).
"""
import sys, os, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
# locate core/ engine (worktree root: state/<slug>/.. -> root/core)
ROOT = os.path.dirname(os.path.dirname(HERE))
CORE = os.path.join(ROOT, "core")
sys.path.insert(0, CORE)

import g6_ideation as G6          # engine-native (numpy-only) G6 scoring ops
import bytegpt_decode as BG       # engine-native (numpy-only) ByteGPT decode

CKPT = os.environ.get("H1129_CKPT", os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin"))
SEEDS = [7, 4302, 4303]
GEN = int(os.environ.get("G6_GEN", "110"))   # H_1362 MAX_NEW=110 VERBATIM
N_STRONG = 6
K_OFFSETS = [0, 101, 202]

# flat IDEATION_SEEDS — string literals (no torch/gauge import; the A_flat baseline arm).
FLAT_SEEDS = [
    "a new idea about consciousness: ",
    "an unexpected way minds could connect: ",
    "imagine a substrate that ",
    "what if memory could ",
    "a strange hypothesis worth testing: ",
]


def main():
    t0 = time.time()
    print(f"[engine] core/g6_ideation.py + core/bytegpt_decode.py (numpy-only, NO torch)", flush=True)
    print(f"[ckpt] {CKPT}", flush=True)
    if not BG.bg_is_bytegpt(CKPT):
        raise SystemExit(f"ABORT: {CKPT} is not a ByteGPT .bin (header sniff failed)")
    hdr = BG.bg_header(CKPT)
    print(f"[header] {hdr}", flush=True)

    # Load weights ONCE (303M is heavy; reuse W for every frame/seed/K offset).
    print(f"[load] bg_load (303M)…", flush=True)
    W = BG.bg_load(CKPT)
    print(f"[load] done vocab={W['vocab']} block={W['block']} ({time.time()-t0:.1f}s)", flush=True)

    known = G6._g6_dict_load()
    cal = G6.g6_detector_calibration(known)
    print(f"\n=== FROZEN _is_falsifiable DETECTOR CALIBRATION (engine-native, advisory>=8/10) = {cal}/10 ===", flush=True)

    frames = G6.g6_build_frames(N_STRONG)
    c_composed, c_shuffle, c_ablate = frames["composed"], frames["shuffled"], frames["ablated"]
    b_composed = G6.g6_build_frames(5)["composed"]   # H_1305 5-frame prior-art reference

    leaks = G6.g6_frame_guard(c_composed, known)
    print(f"\n=== p7 FRAME GUARD (no measurable / not self-falsifiable in frame) ===", flush=True)
    if leaks:
        print(f"  !! FRAME LEAK: {leaks}", flush=True)
        raise SystemExit("ABORT: scaffold frame would cheat the detector (p7)")
    print("  CLEAN — frames carry only if/then FORM scaffold", flush=True)
    print("\n=== STRENGTHENED FRAMES (ARM C, K=3, 6 frames) ===", flush=True)
    for f in c_composed:
        print(f"  {f!r}", flush=True)

    # ── decode primitives bound to the PRE-LOADED W (engine-native, single typed mouth) ──
    def ideate_W(frame, gen, seed_rng):
        return BG.bytegpt_decode_topk_sampled_W(W, frame, gen, 40, 0.7, seed_rng)["text"]

    def best_of_k_W(frame, gen, base_seed, kk, known):
        best = ""; best_fals = -1; best_kwr = -1.0
        for oi in range(kk):
            o = ideate_W(frame, gen, base_seed + K_OFFSETS[oi])
            kwr = G6._g6_known_word_ratio(o, known)
            fals = 1 if (kwr >= 0.5 and G6._g6_is_falsifiable(o, known)) else 0
            if fals > best_fals or (fals == best_fals and kwr > best_kwr):
                best_fals, best_kwr, best = fals, kwr, o
        return best

    def score_arm(frames_list, base_seed, k=1, best_of_k=False, tag=""):
        """engine-native DIST/FALS scoring (g6_score_arm logic, W-bound decode)."""
        texts = []; word_sets = []; fals = 0
        for i, f in enumerate(frames_list):
            tf = time.time()
            if best_of_k:
                o = best_of_k_W(f, GEN, base_seed, k, known)
            else:
                o = ideate_W(f, GEN, base_seed)
            print(f"      .. {tag} frame {i+1}/{len(frames_list)} ({time.time()-tf:.0f}s)", flush=True)
            texts.append(o)
            if G6._g6_known_word_ratio(o, known) >= 0.5:
                word_sets.append(G6._g6_words(o))
                if G6._g6_is_falsifiable(o, known):
                    fals += 1
        kept = []
        for ws in word_sets:
            if all(G6._g6_jaccard(ws, kk) <= 0.5 for kk in kept):
                kept.append(ws)
        return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "texts": texts}

    arms = {
        "A_flat":     dict(frames=FLAT_SEEDS, k=1, bok=False),
        "B_composed": dict(frames=b_composed, k=1, bok=False),
        "C_strong":   dict(frames=c_composed, k=3, bok=True),
        "C_k1":       dict(frames=c_composed, k=1, bok=True),   # best-of-K=1 decomposition
        "C_shuffle":  dict(frames=c_shuffle,  k=3, bok=True),
        "C_ablate":   dict(frames=c_ablate,   k=3, bok=True),
    }
    per_seed = {a: [] for a in arms}
    for base_seed in SEEDS:
        print(f"\n######## seed_rng={base_seed} ({time.time()-t0:.0f}s) ########", flush=True)
        for a, sp in arms.items():
            r = score_arm(sp["frames"], base_seed, k=sp["k"], best_of_k=sp["bok"], tag=a)
            per_seed[a].append(r)
            print(f"  [{a:11s}] DIST={r['dist']} FALS={r['fals']} coh={r['coherent']}/{len(sp['frames'])}", flush=True)
            for t in r["texts"]:
                fl = "F" if G6._g6_is_falsifiable(t, known) else "."
                print(f"        ({fl}) {t[:96]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds, ENGINE-NATIVE) ================", flush=True)
    for a in arms:
        print(f"  {a:11s}  DIST={DIST[a]}  FALS={FALS[a]}  per-seed FALS={[r['fals'] for r in per_seed[a]]}", flush=True)

    m1 = DIST["C_strong"] >= 5
    m2 = FALS["C_strong"] >= 1
    m3 = FALS["C_strong"] > FALS["B_composed"]
    m4 = FALS["C_strong"] > FALS["C_shuffle"]
    m5 = FALS["C_strong"] > FALS["C_ablate"]
    closed = m1 and m2 and m3 and m4 and m5
    shuffle_collapsed = FALS["C_shuffle"] < FALS["C_strong"]   # binding test
    bok_lift = FALS["C_strong"] > FALS["C_k1"]                 # best-of-K真 lever vs single sample

    print("\n---- FROZEN MOVE BARS (G6 ★ CLOSE = ALL M1..M5) ----", flush=True)
    print(f"  M1 COUNT       DIST(C)>=5            : {DIST['C_strong']} -> {m1}", flush=True)
    print(f"  M2 DEPTH       FALS(C)>=1            : {FALS['C_strong']} -> {m2}", flush=True)
    print(f"  M3 LIFT        FALS(C)>FALS(B)       : {FALS['C_strong']} vs {FALS['B_composed']} -> {m3}", flush=True)
    print(f"  M4 EARNED-PAIR FALS(C)>FALS(shuffle) : {FALS['C_strong']} vs {FALS['C_shuffle']} -> {m4}", flush=True)
    print(f"  M5 EARNED-COMP FALS(C)>FALS(ablate)  : {FALS['C_strong']} vs {FALS['C_ablate']} -> {m5}", flush=True)
    print(f"\n  closed_G6={closed} | cross-shuffle collapsed={shuffle_collapsed} | best-of-K lift(K3>K1)={bok_lift}", flush=True)

    # ── verdict (frozen-first; honest) ──
    if closed and shuffle_collapsed:
        verdict = ("GREEN — scaffold reproduces ENGINE-NATIVE (C fals>=1, M1-M5 PASS, cross-shuffle "
                   "collapsed = real binding). G6벽 lever = decode-procedure/scaffold; no retrain needed.")
    elif FALS["C_strong"] < 1:
        verdict = ("RED — scaffold gives FALS=0 engine-native on h1129 (torch H_1362 FALS=1.0 was a "
                   "torch artifact; H_1587 divergence CONFIRMED). lever != decode = attention-capacity.")
    else:
        verdict = ("RED — fals rose but cross-shuffle did NOT collapse (token-presence artifact, not "
                   "binding; H_1434/H_1449 control). scaffold != real lever = attention-capacity.")
    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"hypothesis": "H_159x_g6_scaffold_repro", "engine": "core/g6_ideation.py+bytegpt_decode.py (numpy-only)",
           "ckpt": CKPT, "ckpt_sha_expect": "5cf07a36", "seeds": SEEDS, "gen": GEN,
           "n_strong": N_STRONG, "calibration": f"{cal}/10",
           "DIST": DIST, "FALS": FALS,
           "M1_count": m1, "M2_depth": m2, "M3_lift": m3, "M4_earned_pair": m4, "M5_earned_comp": m5,
           "closed_G6": bool(closed), "cross_shuffle_collapsed": bool(shuffle_collapsed),
           "best_of_k_lift_K3_over_K1": bool(bok_lift), "verdict": verdict,
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"], "coherent": r["coherent"], "texts": r["texts"]}
                            for r in per_seed[a]] for a in arms},
           "wall_seconds": round(time.time() - t0, 1)}
    od = os.path.join(HERE)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json ({time.time()-t0:.0f}s total)", flush=True)


if __name__ == "__main__":
    main()
