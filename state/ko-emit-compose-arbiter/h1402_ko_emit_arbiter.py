#!/usr/bin/env python3
# h1402_ko_emit_arbiter.py — ARBITER-SWAP: can a NON-MAGNITUDE arbiter capture H_1399's oracle +0.043?
#
# THE PRECISE RECLASSIFICATION (a_break_the_wall taxonomy): H_1397 (fixture, morph⊇jamo) + H_1399 (REAL,
# jamo⊇morph, FLIPPED) closed the emit-COMPOSE arc 🧱 because the §6.5f substrate-confidence arbiter
# (scale-relative recall confidence mean_err/(err_here+ε)) DEGRADES below best-single. BUT H_1399's REAL
# oracle = 0.87142 > best_single = 0.82853 (+0.04289) PROVES a real complementarity EXISTS — the arbiter
# just cannot capture it. Both arbiters tried so far were confidence-MAGNITUDE based. This lane tries ONE
# genuinely-different, NON-magnitude arbiter — DECISIVENESS / top-2 GAP (the H_1398 lens that beat
# magnitude-margin for metacognition): each faculty's vote weight = the SHARPNESS of its own next-symbol
# posterior, gap_f = p(argmax|ctx) − p(2nd-argmax|ctx); arbitrate toward the MORE-DECISIVE faculty.
#
# REUSED VERBATIM from H_1399 (anti-Goodhart): the SAME real shard (sha c47b6808...), the SAME jamo rep, the
# SAME BPE-on-jamo morphology unit (2000 merges, TRAIN-only), the SAME odd-even stride-300 split, the SAME
# nmax=5 heads, the SAME 3 seeds [4398,4399,4400] POOLED. ONLY the conflict-arbitration rule changes.
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1402_ko_emit_arbiter/FREEZE.txt BEFORE this run, H_1399's
# thresholds VERBATIM (best_single=0.82853, oracle=0.87142, magnitude baseline=0.80853, Δ=0.01, shuf tol
# 0.01). REAL Korean only — NO synthetic, NO fetch ($0). DIRECTIONAL numpy mirror (engine-transfer
# UNVERIFIED). CORE UNTOUCHED (the §6.5f arbiter-swap is the named follow-on IF 🟢).

import argparse, hashlib, json, os, sys, time, unicodedata
from collections import Counter
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1368_KO_SHA_30M = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
KO_KEY = "anima-7b/web/kor/shard0000.bytes"
KO_STRIDE = 300
NMAX = 5
BPE_MERGES = 2000
SEEDS = [4398, 4399, 4400]
EPS = 1e-6
# frozen thresholds — H_1399 VERBATIM (NO bar moved).
BEST_SINGLE_FROZEN = 0.82853    # H_1399 best_single (reused, the bar1 reference)
ORACLE_FROZEN = 0.87142         # H_1399 oracle ceiling (reused diagnostic)
MAG_BASELINE_FROZEN = 0.80853   # H_1399 §6.5f magnitude arbiter acc_compose (reused diagnostic — to BEAT)
NETLIFT_DELTA = 0.01            # bar1: acc_compose_NEW >= best_single + Δ (0.01, same slack as H_1399 bar1)
SHUFW_SLACK = 0.01              # bar2 EARNED: acc_shufw <= acc_compose_NEW + 0.01 (H_1399 bar3 verbatim)


def log(*a): print(*a, flush=True)


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
        except Exception:
            continue
    return b


# ── jamo symbol stream (IDENTICAL byte-fair axis to H_1316/H_1359/H_1368/H_1380/H_1388/H_1399) ───────
def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        if HANGUL_LO <= ord(ch) <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}
    return jamo_to_id, jamo_sorted


def make_symbol_stream(text, jamo_to_id):
    syms, emit_byte = [], []
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            for jc in nfd:
                b0 = chr(ord(jc)).encode("utf-8")[0]
                syms.append(jamo_to_id[ord(jc)]); emit_byte.append(b0)
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); emit_byte.append(b)
    return np.asarray(syms, dtype=np.int64), np.asarray(emit_byte, dtype=np.int64)


# ── n-gram count head — argmax-next + recall margin (magnitude, H_1399) + DECISIVENESS GAP (H_1402 NEW) ──
class CountHead:
    """A frozen n-gram count head over a symbol stream. Surfaces TWO substrate signals at the deepest ctx:
      - recon_err(ctx)  = 1 - p(argmax|ctx)             — the MAGNITUDE signal H_1399's §6.5f arbiter read.
      - decisiveness(ctx) = p(argmax|ctx) - p(2nd|ctx)  — the NON-MAGNITUDE GAP signal (H_1398 lens, H_1402
                            NEW): how SHARP the head's own posterior is here (top-1 vs top-2 separation).
                            HIGHER = more decisive = more trustworthy (a faculty whose #1≫#2). This is the
                            count-head analogue of the engine's top-2 affinity gap (immune_memory_recall_gap).
    """
    def __init__(self, nmax):
        self.nmax = nmax
        self.ctx = [dict() for _ in range(nmax + 1)]
        self.tot = [dict() for _ in range(nmax + 1)]

    def fit(self, stream, train_positions):
        S = stream
        for i in train_positions:
            i = int(i); s = int(S[i])
            for k in range(1, self.nmax + 1):
                if i - (k - 1) < 0:
                    continue
                c = tuple(S[i - k + 1: i].tolist()) if k > 1 else ()
                d = self.ctx[k].get(c)
                if d is None:
                    d = {}; self.ctx[k][c] = d; self.tot[k][c] = 0
                d[s] = d.get(s, 0) + 1
                self.tot[k][c] += 1

    def _deepest(self, hist):
        for k in range(self.nmax, 0, -1):
            c = tuple(hist[-(k - 1):]) if k > 1 else ()
            d = self.ctx[k].get(c)
            if d is not None and self.tot[k][c] > 0:
                return d, self.tot[k][c]
        return None, 0

    def argmax_next(self, hist):
        d, tot = self._deepest(hist)
        if d is None:
            return -1
        return max(d.items(), key=lambda kv: (kv[1], -kv[0]))[0]

    def recon_err(self, hist):
        """recall margin error = 1 - p(argmax|ctx). LOWER ⇒ more grounded (the H_1399 MAGNITUDE signal)."""
        d, tot = self._deepest(hist)
        if d is None or tot == 0:
            return 1.0
        pmax = max(d.values()) / tot
        return 1.0 - pmax

    def decisiveness(self, hist):
        """top-1 ↔ top-2 GAP = p(argmax|ctx) - p(2nd-argmax|ctx). HIGHER ⇒ sharper posterior = more
        decisive (the H_1398 NON-MAGNITUDE GAP signal, H_1402's new arbiter weight). If only one symbol
        fires here, gap = pmax (2nd = 0). If the head doesn't fire, gap = 0 (uninformative)."""
        d, tot = self._deepest(hist)
        if d is None or tot == 0:
            return 0.0
        counts = sorted(d.values(), reverse=True)
        p1 = counts[0] / tot
        p2 = (counts[1] / tot) if len(counts) > 1 else 0.0
        return p1 - p2


def positions_split(stream_len, nmax, stride):
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


# ── BPE-on-jamo (morphology-aware unit) — frequency-ranked merges, TRAIN slice only (== H_1399) ──────
def learn_bpe(base_ids, num_merges, rng=None):
    sym = list(map(int, base_ids))
    N = len(sym)
    if N < 2:
        return []
    nxt = list(range(1, N)) + [-1]
    prv = [-1] + list(range(0, N - 1))
    alive = bytearray([1]) * N
    pair_counts = Counter()
    pair_pos = {}
    for i in range(N - 1):
        pr = (sym[i], sym[i + 1])
        pair_counts[pr] += 1
        pair_pos.setdefault(pr, set()).add(i)
    next_id = max(sym) + 1
    merges = []

    def _add(p, i):
        pair_counts[p] += 1
        pair_pos.setdefault(p, set()).add(i)

    def _rem(p, i):
        if p in pair_pos:
            pair_pos[p].discard(i)
        pair_counts[p] -= 1
        if pair_counts[p] <= 0:
            pair_counts.pop(p, None); pair_pos.pop(p, None)

    for _ in range(num_merges):
        if not pair_counts:
            break
        if rng is None:
            best = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        else:
            pairs = list(pair_counts.keys())
            best = pairs[int(rng.integers(0, len(pairs)))]
        a, b = best
        nid = next_id; next_id += 1
        merges.append((a, b, nid))
        positions = sorted(pair_pos.get((a, b), set()))
        for i in positions:
            if not alive[i]:
                continue
            j = nxt[i]
            if j == -1 or not alive[j] or sym[i] != a or sym[j] != b:
                continue
            p = prv[i]; k = nxt[j]
            if p != -1:
                _rem((sym[p], sym[i]), p)
            if k != -1:
                _rem((sym[j], sym[k]), j)
            _rem((a, b), i)
            sym[i] = nid
            nxt[i] = k
            if k != -1:
                prv[k] = i
            alive[j] = 0
            if p != -1:
                _add((sym[p], nid), p)
            if k != -1:
                _add((nid, sym[k]), i)
    return merges


def apply_bpe(base_ids, base_emit, merges):
    N = len(base_ids)
    if N == 0:
        return np.zeros(0, np.int64), np.zeros(0, np.int64)
    sym = list(map(int, base_ids)); lead = list(map(int, base_emit))
    nxt = list(range(1, N)) + [-1]
    prv = [-1] + list(range(0, N - 1))
    alive = bytearray([1]) * N
    pair_pos = {}
    for i in range(N - 1):
        pair_pos.setdefault((sym[i], sym[i + 1]), set()).add(i)
    for (a, b, nid) in merges:
        positions = pair_pos.pop((a, b), None)
        if not positions:
            continue
        for i in sorted(positions):
            if not alive[i]:
                continue
            j = nxt[i]
            if j == -1 or not alive[j] or sym[i] != a or sym[j] != b:
                continue
            p = prv[i]; k = nxt[j]
            if p != -1 and (sym[p], sym[i]) in pair_pos:
                pair_pos[(sym[p], sym[i])].discard(p)
            if k != -1 and (sym[j], sym[k]) in pair_pos:
                pair_pos[(sym[j], sym[k])].discard(j)
            sym[i] = nid
            nxt[i] = k
            if k != -1:
                prv[k] = i
            alive[j] = 0
            if p != -1:
                pair_pos.setdefault((sym[p], nid), set()).add(p)
            if k != -1:
                pair_pos.setdefault((nid, sym[k]), set()).add(i)
    out_s, out_lead = [], []
    i = 0
    while i != -1 and i < N:
        if alive[i]:
            out_s.append(sym[i]); out_lead.append(lead[i])
        i = nxt[i]
    return np.asarray(out_s, np.int64), np.asarray(out_lead, np.int64)


def unit_lead_byte_map(unit_ids, unit_lead):
    m = {}
    for u, lb in zip(unit_ids.tolist(), unit_lead.tolist()):
        if u not in m:
            m[u] = lb
    return m


def bemit_for_sym(sym_id, jamo_to_id, jamo_sorted):
    if sym_id < 0:
        return -1
    if sym_id < 256:
        return sym_id
    rank = sym_id - 256
    if 0 <= rank < len(jamo_sorted):
        return chr(jamo_sorted[rank]).encode("utf-8")[0]
    return -1


def build_base2unit(bsym, merges):
    N = len(bsym)
    sym = list(map(int, bsym))
    nxt = list(range(1, N)) + [-1]
    prv = [-1] + list(range(0, N - 1))
    alive = bytearray([1]) * N
    pair_pos = {}
    for i in range(N - 1):
        pair_pos.setdefault((sym[i], sym[i + 1]), set()).add(i)
    for (a, b, nid) in merges:
        positions = pair_pos.pop((a, b), None)
        if not positions:
            continue
        for i in sorted(positions):
            if not alive[i]:
                continue
            j = nxt[i]
            if j == -1 or not alive[j] or sym[i] != a or sym[j] != b:
                continue
            p = prv[i]; k = nxt[j]
            if p != -1 and (sym[p], sym[i]) in pair_pos:
                pair_pos[(sym[p], sym[i])].discard(p)
            if k != -1 and (sym[j], sym[k]) in pair_pos:
                pair_pos[(sym[j], sym[k])].discard(j)
            sym[i] = nid; nxt[i] = k
            if k != -1:
                prv[k] = i
            alive[j] = 0
            if p != -1:
                pair_pos.setdefault((sym[p], nid), set()).add(p)
            if k != -1:
                pair_pos.setdefault((nid, sym[k]), set()).add(i)
    base2unit = np.zeros(N, dtype=np.int64)
    unit_start_base = []
    i = 0; uidx = 0
    while i != -1 and i < N:
        start = i
        unit_start_base.append(start)
        nb = nxt[i]
        end = nb if nb != -1 else N
        for bpos in range(start, end):
            base2unit[bpos] = uidx
        uidx += 1
        i = nb
    return base2unit, unit_start_base


def unit_train_positions(unit_start_base, train_base_set, nmax):
    out = []
    for ui, sb in enumerate(unit_start_base):
        if ui < nmax - 1:
            continue
        if sb in train_base_set:
            out.append(ui)
    return np.asarray(out, dtype=np.int64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1380_corpus/kor_big.bytes")
    ap.add_argument("--mb", type=float, default=30.0)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--merges", type=int, default=BPE_MERGES)
    ap.add_argument("--no-sha-check", action="store_true", help="SMOKE ONLY — skip the 30MB sha gate (NEVER for the frozen run)")
    ap.add_argument("--out", default=".verdicts/1402_ko_emit_arbiter/result.txt")
    args = ap.parse_args()
    t0 = time.time()

    if not os.path.exists(args.ko_cache):
        log(f"FATAL: REAL KO cache missing at {args.ko_cache} — REAL-only, NO synthetic, NO fetch. STOP.")
        sys.exit(3)
    ko_full = open(args.ko_cache, "rb").read(int(args.mb * 1_000_000) + 8)
    win = trim_utf8(ko_full[: int(args.mb * 1_000_000)])
    sha = hashlib.sha256(win).hexdigest()
    log(f"[corpus] REAL local {args.ko_cache} {args.mb}MB-prefix sha {sha}")
    if sha != H1368_KO_SHA_30M:
        if args.no_sha_check:
            log("[corpus] WARNING --no-sha-check: SMOKE sub-window, NOT the frozen run.")
        else:
            log(f"FATAL: prefix sha mismatch vs H_1368 baseline ({H1368_KO_SHA_30M}) — corpus drift. STOP.")
            sys.exit(3)
    else:
        log(f"[corpus] sha == H_1368/H_1380/H_1388/H_1399 baseline: True (byte-fair, NO fetch, $0)")

    text = win.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(text)
    bsym, bemit = make_symbol_stream(text, jamo_to_id)
    vj = 256 + len(jamo_sorted)
    log(f"[rep] Vj(jamo)={vj} ({len(jamo_sorted)} distinct jamo) jamo-stream={len(bsym)} nmax={args.nmax} stride={args.stride}")

    tr_pos, te_pos = positions_split(len(bsym), args.nmax, args.stride)
    train_end = int(tr_pos[-1]) + 1 if len(tr_pos) else len(bsym)

    jhead = CountHead(args.nmax)
    jhead.fit(bsym, tr_pos)
    log(f"[jamo] head fit  [{time.time()-t0:.0f}s]")

    merges = learn_bpe(bsym[:train_end], args.merges, rng=None)
    unit_ids, unit_lead = apply_bpe(bsym, bemit, merges)
    uvocab = int(unit_ids.max()) + 1
    ulead_map = unit_lead_byte_map(unit_ids, unit_lead)
    base2unit, unit_start_base = build_base2unit(bsym, merges)
    mhead = CountHead(args.nmax)
    unit_tr = unit_train_positions(unit_start_base, set(int(x) for x in tr_pos), args.nmax)
    mhead.fit(unit_ids, unit_tr)
    log(f"[morph] merges={len(merges)} unit_vocab={uvocab} unit_stream={len(unit_ids)} "
        f"units/jamo={len(unit_ids)/max(1,len(bsym)):.4f}  [{time.time()-t0:.0f}s]")

    # ── shared next-byte decision; TWO NEW arbiters (decisiveness, agreement-aware) + magnitude baseline ──
    def eval_pass(seed):
        rng = np.random.default_rng(seed)
        n = 0
        ok_j = ok_m = 0
        ok_arbA = ok_arbB = ok_shufA = 0
        agree = 0
        both = only_j = only_m = oracle = 0
        # arbitration audit for ARB-A (decisiveness) among CONFLICTS:
        conflict_n = winA_j = winA_m = winA_tie = 0
        # shuffle control storage: collect (gap-decision-correct-on-which) to permute the gap↔correctness pair
        conflict_records = []  # (jbyte, mbyte, true_byte, gapj, gapm)
        for pos in te_pos:
            pos = int(pos)
            if pos + 1 >= len(bsym):
                continue
            true_byte = int(bemit[pos + 1])
            lo = max(0, pos + 1 - (args.nmax - 1))
            jhist = bsym[lo: pos + 1].tolist()
            jnext = jhead.argmax_next(jhist)
            jbyte = int(bemit_for_sym(jnext, jamo_to_id, jamo_sorted)) if jnext >= 0 else -1
            gapj = jhead.decisiveness(jhist)                    # NON-MAGNITUDE decisiveness (H_1402)
            ui = base2unit[pos]
            if ui + 1 < len(unit_ids):
                ulo = max(0, ui + 1 - (args.nmax - 1))
                uhist = unit_ids[ulo: ui + 1].tolist()
                unext = mhead.argmax_next(uhist)
                mbyte = int(ulead_map.get(unext, -1)) if unext >= 0 else -1
                gapm = mhead.decisiveness(uhist)
            else:
                mbyte = -1; gapm = 0.0
            jfires = jbyte >= 0
            mfires = mbyte >= 0
            if not jfires and not mfires:
                continue
            n += 1
            cj = jfires and jbyte == true_byte
            cm = mfires and mbyte == true_byte
            ok_j += int(cj); ok_m += int(cm)
            if jfires and mfires and jbyte == mbyte:
                agree += 1
            # ── ARB-A: DECISIVENESS / top-2 GAP arbiter (the more-decisive faculty wins conflicts) ──
            if jfires and not mfires:
                aA = jbyte
            elif mfires and not jfires:
                aA = mbyte
            else:
                conflict_n += 1
                conflict_records.append((jbyte, mbyte, true_byte, gapj, gapm))
                if gapj > gapm:
                    aA = jbyte; winA_j += 1
                elif gapm > gapj:
                    aA = mbyte; winA_m += 1
                else:
                    aA = jbyte; winA_tie += 1   # exact tie → default jamo (NO seed coin; deterministic)
            ok_arbA += int(aA == true_byte)
            # ── ARB-B: AGREEMENT-AWARE decisiveness (agree→take; conflict→decisiveness gap, == ARB-A) ──
            if jfires and mfires and jbyte == mbyte:
                aB = jbyte                       # agreement leg (mostly both-right mass)
            elif jfires and not mfires:
                aB = jbyte
            elif mfires and not jfires:
                aB = mbyte
            else:
                aB = aA                          # conflict → defer to decisiveness (same as ARB-A here)
            ok_arbB += int(aB == true_byte)
            # ── SHUF-A: shuffle the gap↔correctness pairing (the EARNED control for ARB-A) ──
            # singleton-fire positions are deterministic in ARB-A (no gap used); only conflicts get shuffled
            # below in a SECOND pass once all conflict records collected. Here accumulate singleton hits.
            if jfires and not mfires:
                ok_shufA += int(jbyte == true_byte)
            elif mfires and not jfires:
                ok_shufA += int(mbyte == true_byte)
            # conflict shuffle contribution added after the loop.
            if cj or cm:
                oracle += 1
            if cj and cm:
                both += 1
            elif cj and not cm:
                only_j += 1
            elif cm and not cj:
                only_m += 1
        # ── shuffle control: permute which faculty the gap rule would pick across conflicts ──
        # We break the gap↔correctness link by randomly assigning the winner among conflicts (50/50),
        # which is exactly "the arbiter's decisiveness signal carries no per-position right-faculty info".
        for (jbyte, mbyte, true_byte, gapj, gapm) in conflict_records:
            pick = jbyte if rng.random() < 0.5 else mbyte
            ok_shufA += int(pick == true_byte)
        return dict(n=n, acc_jamo=ok_j / max(1, n), acc_morph=ok_m / max(1, n),
                    acc_arbA=ok_arbA / max(1, n), acc_arbB=ok_arbB / max(1, n),
                    acc_shufA=ok_shufA / max(1, n),
                    agree=agree / max(1, n), oracle=oracle / max(1, n),
                    both=both, only_j=only_j, only_m=only_m,
                    conflict_n=conflict_n, winA_j=winA_j, winA_m=winA_m, winA_tie=winA_tie)

    passes = [eval_pass(s) for s in SEEDS]
    def mean(k): return float(np.mean([p[k] for p in passes]))
    acc_jamo = mean("acc_jamo"); acc_morph = mean("acc_morph")
    acc_arbA = mean("acc_arbA"); acc_arbB = mean("acc_arbB"); acc_shufA = mean("acc_shufA")
    agree = mean("agree"); oracle = mean("oracle")
    n_test = int(round(mean("n")))
    best_single = max(acc_jamo, acc_morph)
    only_j = int(round(mean("only_j"))); only_m = int(round(mean("only_m"))); both = int(round(mean("both")))
    conflict = 1.0 - agree
    conflict_n = int(round(mean("conflict_n")))
    winA_j = int(round(mean("winA_j"))); winA_m = int(round(mean("winA_m"))); winA_tie = int(round(mean("winA_tie")))

    # the NEW arbiter we PRIMARILY test = ARB-A (decisiveness); pick the better of ARB-A/ARB-B for the
    # bar1 NET-LIFT decision (≤2 principled arbiters — the verdict reopens if EITHER clears the bar).
    acc_new = max(acc_arbA, acc_arbB)
    new_name = "ARB-A_decisiveness" if acc_arbA >= acc_arbB else "ARB-B_agreement_aware_decisiveness"

    bar1 = acc_new >= best_single + NETLIFT_DELTA        # NET-LIFT (positive, H_1399 best_single + Δ)
    bar2 = acc_shufA <= acc_arbA + SHUFW_SLACK           # EARNED (shuffle does NOT beat the gap arbiter)
    bar3 = True                                          # Ψ-SAFE: DIRECTIONAL mirror, CORE untouched

    if bar1 and bar2:
        tier = "ARC-REOPENS"
        verdict = (f"🟢 ARC-REOPENS [taxonomy (a) confirmed — wrong-arbiter wall] — the NON-magnitude "
                   f"DECISIVENESS arbiter ({new_name}) CAPTURES a net lift: acc_compose_NEW={acc_new:.5f} "
                   f">= best_single+{NETLIFT_DELTA}={best_single+NETLIFT_DELTA:.5f} (best_single={best_single:.5f}), "
                   f"partially closing toward oracle {oracle:.5f}, AND the shuffle control collapses "
                   f"(acc_shufA={acc_shufA:.5f} <= acc_arbA+{SHUFW_SLACK}={acc_arbA+SHUFW_SLACK:.5f}). The "
                   f"+{oracle-best_single:.5f} oracle complementarity IS substrate-capturable by a decisiveness "
                   f"arbiter — the §6.5f MAGNITUDE arbiter ({MAG_BASELINE_FROZEN}) was the WRONG method. "
                   f"BINDING FOLLOW-ON: engine-native §6.5f arbiter-swap (magnitude → top-2 decisiveness gap, "
                   f"the H_1398 lens) on live CORE/generator.hexa (a_verified_must_wire). DIRECTIONAL numpy "
                   f"mirror — engine-transfer UNVERIFIED.")
    else:
        tier = "TERMINAL-SUBSUMPTION-CONFIRMED"
        why = []
        if not bar1:
            why.append(f"best new arbiter ({new_name}) acc_compose_NEW={acc_new:.5f} < best_single+{NETLIFT_DELTA}="
                       f"{best_single+NETLIFT_DELTA:.5f} (ARB-A={acc_arbA:.5f}, ARB-B={acc_arbB:.5f}; "
                       f"§6.5f magnitude baseline was {MAG_BASELINE_FROZEN}) — decisiveness does NOT predict "
                       "the per-position right faculty here")
        if not bar2:
            why.append(f"acc_shufA={acc_shufA:.5f} > acc_arbA+{SHUFW_SLACK}={acc_arbA+SHUFW_SLACK:.5f} "
                       "(shuffled arbitration matches/beats the gap arbiter — its signal carries no per-position info)")
        verdict = (f"🧱 (d)-CONFIRMED — TRUE SUBSUMPTION CEILING (honest terminal, c9). Neither principled "
                   f"NON-magnitude arbiter (ARB-A decisiveness={acc_arbA:.5f}, ARB-B agreement-aware="
                   f"{acc_arbB:.5f}) beats best_single ({best_single:.5f}) by Δ={NETLIFT_DELTA}. " +
                   " · ".join(why) + f". The oracle's +{oracle-best_single:.5f} complementarity is REAL but "
                   "NOT capturable by ANY substrate-derived arbiter tried — the per-position right-faculty "
                   "signal is NOT in the substrate (decisiveness/top-2 gap is uninformative for WHICH "
                   "faculty is right here, just as confidence-magnitude was). The emit-compose wall is a "
                   "genuine (d) subsumption ceiling, NOT a wrong-arbiter (a) wall. The Korean below-jamo "
                   "emit-compose arc is GENUINELY terminal — a clean closed-negative, NOT a failure. "
                   "DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED.")

    res = {
        "id": "H_1402", "slug": "ko_emit_arbiter",
        "window_mb": args.mb, "window_bytes": len(win), "window_sha256": sha, "sha_match_H1368": (sha == H1368_KO_SHA_30M),
        "Vj_jamo": vj, "distinct_jamo": len(jamo_sorted), "jamo_stream": int(len(bsym)),
        "stride": args.stride, "nmax": args.nmax, "bpe_merges": len(merges), "unit_vocab": uvocab,
        "unit_stream": int(len(unit_ids)), "units_per_jamo": round(len(unit_ids) / max(1, len(bsym)), 4),
        "seeds": SEEDS, "n_test": n_test,
        "acc_jamo": round(acc_jamo, 5), "acc_morph": round(acc_morph, 5), "best_single": round(best_single, 5),
        "magnitude_baseline_H1399": MAG_BASELINE_FROZEN,
        "acc_arbA_decisiveness": round(acc_arbA, 5), "acc_arbB_agreement_aware": round(acc_arbB, 5),
        "acc_compose_NEW": round(acc_new, 5), "new_arbiter": new_name,
        "acc_shufA_shuffle_control": round(acc_shufA, 5),
        "agree_rate": round(agree, 5), "conflict_rate": round(conflict, 5),
        "oracle": round(oracle, 5), "oracle_minus_best": round(oracle - best_single, 5),
        "both_right": both, "only_jamo": only_j, "only_morph": only_m,
        "conflict_n": conflict_n, "arbA_win_jamo": winA_j, "arbA_win_morph": winA_m, "arbA_win_tie": winA_tie,
        "new_minus_best": round(acc_new - best_single, 5),
        "new_minus_magnitude": round(acc_new - MAG_BASELINE_FROZEN, 5),
        "shuf_minus_arbA": round(acc_shufA - acc_arbA, 5),
        "netlift_delta": NETLIFT_DELTA, "shufw_slack": SHUFW_SLACK,
        "bar1_NET_LIFT": bool(bar1), "bar2_EARNED": bool(bar2), "bar3_PSI_SAFE": bool(bar3),
        "tier": tier, "verdict": verdict, "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    txt = render(res)
    with open(args.out, "w") as f:
        f.write(txt)
    log("\n" + txt)


def render(r):
    L = []
    L.append("===== H_1402 KO-EMIT COMPOSE ARBITER-SWAP — can a NON-MAGNITUDE arbiter capture oracle +0.043? =====")
    L.append(f"REAL KO {r['window_mb']}MB sha {r['window_sha256'][:16]}… (== H_1368/H_1380/H_1388/H_1399, NO fetch, $0) · "
             f"DIRECTIONAL numpy mirror · CORE UNTOUCHED · seeds {r['seeds']}")
    L.append("")
    L.append(f"shared next-byte decision (REAL jamo stream, n_test={r['n_test']}):")
    L.append(f"  acc_jamo    (jamo emit-bias alone)        : {r['acc_jamo']}")
    L.append(f"  acc_morph   (morphology emit-bias alone)  : {r['acc_morph']}")
    L.append(f"  best_single (max of the two alone)        : {r['best_single']}   (H_1399 frozen ref {BEST_SINGLE_FROZEN})")
    L.append(f"  §6.5f MAGNITUDE arbiter (H_1399, to BEAT) : {r['magnitude_baseline_H1399']}   (DEGRADED below best-single)")
    L.append(f"  ── NEW NON-MAGNITUDE arbiters (H_1402) ──")
    L.append(f"  ARB-A decisiveness / top-2 GAP            : {r['acc_arbA_decisiveness']}")
    L.append(f"  ARB-B agreement-aware decisiveness        : {r['acc_arbB_agreement_aware']}")
    L.append(f"  acc_compose_NEW (best of ARB-A/ARB-B)     : {r['acc_compose_NEW']}  [{r['new_arbiter']}]")
    L.append(f"  acc_shufA   (gap↔correctness SHUFFLED)    : {r['acc_shufA_shuffle_control']}   (EARNED control)")
    L.append("")
    L.append("DIAGNOSTIC (non-gating):")
    L.append(f"  agree_rate    : {r['agree_rate']}    conflict_rate : {r['conflict_rate']}")
    L.append(f"  ORACLE ceiling (ANY arbitration upper bound) : {r['oracle']}  (oracle - best = {r['oracle_minus_best']})")
    L.append(f"  complementarity: both_right={r['both_right']} only_jamo={r['only_jamo']} only_morph={r['only_morph']}")
    L.append(f"  ARB-A arbitration audit (among {r['conflict_n']} conflicts): jamo-won={r['arbA_win_jamo']} "
             f"morph-won={r['arbA_win_morph']} tie-default-jamo={r['arbA_win_tie']} (decisiveness decides — NO hardcoded priority)")
    L.append(f"  new − best = {r['new_minus_best']}   ·   new − magnitude(0.80853) = {r['new_minus_magnitude']}")
    L.append("")
    L.append("FROZEN BARS (H_1399/H_1397 thresholds VERBATIM, NO bar moved):")
    L.append(f"  bar1 NET-LIFT : acc_compose_NEW >= best_single + {r['netlift_delta']}  → {str(r['bar1_NET_LIFT']).lower()}  "
             f"(new={r['acc_compose_NEW']} best={r['best_single']} Δ={r['new_minus_best']})")
    L.append(f"  bar2 EARNED   : acc_shufA <= acc_arbA + {r['shufw_slack']}  → {str(r['bar2_EARNED']).lower()}  "
             f"(shufA={r['acc_shufA_shuffle_control']} arbA={r['acc_arbA_decisiveness']} Δ={r['shuf_minus_arbA']})")
    L.append(f"  bar3 Ψ-SAFE   : CORE untouched (DIRECTIONAL mirror; §6.5f arbiter-swap = named follow-on IF 🟢) → {str(r['bar3_PSI_SAFE']).lower()}")
    L.append("")
    L.append(f"VERDICT: {r['tier']}")
    L.append(r["verdict"])
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
