#!/usr/bin/env python3
# state/9119_fm_b50_measure/fm_b50_py.py — --py numpy mirror of fm_b50.hexa (H_9119 §2 b50).
# DIRECTIONAL (numpy, NOT engine-native per a_engine_native_learning) — the authorized --py
# fallback when the engine-native hexa run is CPU-scalar-bound-impractical (owner 2026-07-04).
# 1:1 port of fm_b50.hexa (b50_of, gen_fm_rerank, fm_prefix_decodability, distractors_for) reusing
# core/decode.py numpy primitives (clm_load_weights, _fwd_logits, nn_ce_loss_allpos,
# clm_decode_topk_sampled_W). Weights hoisted ONCE per ckpt. b50 result is DIRECTIONAL either way
# (H_9118 external-oracle-mediated). Same OFF/ON/SHUFFLE comparison + printed format as the hexa.
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import numpy as np
import decode as D   # core/decode.py

V = 256

def text_to_bytes(s):
    return list(s.encode("utf-8", "surrogateescape"))

def clm_ce_bytes_W(W, seq_bytes):
    # mirror clm_decode_ce(listener, seq): mean next-byte CE of seq_bytes under W.
    T = len(seq_bytes)
    if T < 2:
        return float(np.log(V))
    tok = np.array(seq_bytes[:T - 1], dtype=np.float64)
    tgt = np.array(seq_bytes[1:T], dtype=np.float64)
    logits = D._fwd_logits(W, tok, T - 1)
    return float(D.nn_ce_loss_allpos(logits, tgt, T - 1, W["V"]))

def clm_argmax_W(W, seed, gen):
    # mirror clm_decode_argmax with hoisted W (T=24 right-aligned seed, greedy).
    Vv = W["V"]; T = 24
    seed_b = seed.encode("utf-8", "surrogateescape")
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    for _ in range(gen):
        logits = D._fwd_logits(W, tok, T)
        row = logits[T - 1]
        besti = int(np.argmax(row))
        out.append(besti)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(besti)
    return out.decode("utf-8", "surrogateescape")

def fm_prefix_decodability(margins, decay):
    acc = 0.0; w = 1.0
    for m in margins:
        acc += w * m; w *= decay
    return acc

def gen_fm_rerank_py(spkW, lisW, seed, gen, k, base_seed, target, distractors, decay):
    offsets = [0, 101, 202, 303]
    grid = [4, 8, 16, 32]
    kk = min(k, 4)
    best_text = ""; best_score = -1e6; best_i = -1; got = False
    for oi in range(kk):
        rs = D.clm_decode_topk_sampled_W(spkW, seed, gen, 8, 0.7, base_seed + offsets[oi])
        ts = rs["text"] if rs.get("ok") else ""
        if not rs.get("ok"):
            continue
        cb = text_to_bytes(ts); nb = len(cb)
        margins = []
        for g in grid:
            pb = min(g, nb)
            pfx = cb[:pb]
            ce_t = clm_ce_bytes_W(lisW, pfx + text_to_bytes(" " + target))
            best_d = 1e6
            for dstr in distractors:
                ce_d = clm_ce_bytes_W(lisW, pfx + text_to_bytes(" " + str(dstr)))
                if ce_d < best_d:
                    best_d = ce_d
            margins.append(best_d - ce_t)
        score = fm_prefix_decodability(margins, decay)
        if (not got) or score > best_score:
            best_score = score; best_text = ts; best_i = oi; got = True
    if not got:
        return {"text": clm_argmax_W(spkW, seed, gen), "selected": -1, "fm_score": 0.0}
    return {"text": best_text, "selected": best_i, "fm_score": best_score}

def b50_of_py(lisW, emit, target, distractors):
    grid = [2, 4, 8, 16, 32, 64]
    eb = text_to_bytes(emit)
    for g in grid:
        pfx = eb[:min(g, len(eb))]
        ce_t = clm_ce_bytes_W(lisW, pfx + text_to_bytes(" " + target))
        best_d = 1e6
        for dstr in distractors:
            ce_d = clm_ce_bytes_W(lisW, pfx + text_to_bytes(" " + str(dstr)))
            if ce_d < best_d:
                best_d = ce_d
        if ce_t < best_d:
            return float(g)
    return 999.0

def distractors_for(concepts, ti):
    n = len(concepts)
    return [str(concepts[(ti + j) % n]) for j in (1, 2, 3)]

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: fm_b50_py.py <speaker.clm> <listener.clm> [gen] [base] [nconcepts]")
        return
    speaker, listener = args[0], args[1]
    gen = int(args[2]) if len(args) > 2 else 24
    base = int(args[3]) if len(args) > 3 else 12345
    concepts = ["volcano", "glacier", "library", "violin", "spider", "lighthouse", "umbrella",
                "beehive", "telescope", "avalanche", "compass", "cactus", "harbor", "thunderstorm"]
    if len(args) > 4:
        concepts = concepts[:int(args[4])]
    n = len(concepts)
    decay = 0.75  # ep_fm_prefix_decay
    print("=== H_9119 §2 forward-model b50 measurement (--py numpy mirror, DIRECTIONAL) ===")
    print("speaker=%s listener=%s gen=%d k=8 nconcepts=%d" % (speaker, listener, gen, n))
    sys.stdout.flush()
    spkW = D.clm_load_weights(speaker)
    lisW = D.clm_load_weights(listener)
    sum_on = sum_off = sum_shuf = 0.0
    for ti in range(n):
        target = str(concepts[ti])
        distr = distractors_for(concepts, ti)
        eoff = clm_argmax_W(spkW, target, gen)
        ron = gen_fm_rerank_py(spkW, lisW, target, gen, 8, base + ti * 17, target, distr, decay)
        eon = ron["text"]
        b_off = b50_of_py(lisW, eoff, target, distr)
        b_on = b50_of_py(lisW, eon, target, distr)
        wrong = str(concepts[(ti + 1) % n])
        b_shuf = b50_of_py(lisW, eon, wrong, distractors_for(concepts, (ti + 1) % n))
        sum_off += b_off; sum_on += b_on; sum_shuf += b_shuf
        print("%s: b50_off=%s b50_on=%s b50_shuffle=%s fm_score=%.4f"
              % (target, b_off, b_on, b_shuf, ron["fm_score"]))
        sys.stdout.flush()
    m_on = sum_on / n; m_off = sum_off / n; m_shuf = sum_shuf / n
    print("--- mean b50: OFF=%.4f ON=%.4f SHUFFLE=%.4f ---" % (m_off, m_on, m_shuf))
    print("VERDICT: %s | shuffle control %s"
          % ("b50 LOWERED by rerank (ON<OFF)" if m_on < m_off else "no b50 drop (ON>=OFF)",
             "OK (referential)" if m_shuf > m_on else "FAIL (b50 not referential)"))
    print("NOTE: --py numpy mirror = DIRECTIONAL (a_engine_native_learning); external-mind b50 = DIRECTIONAL (H_9118).")

if __name__ == "__main__":
    main()
