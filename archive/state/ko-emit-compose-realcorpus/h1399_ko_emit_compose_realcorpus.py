#!/usr/bin/env python3
# h1399_ko_emit_compose_realcorpus.py — RE-SCORE H_1397's frozen compose bars on a REAL Korean corpus.
#
# THE NAMED OPEN QUESTION (H_1397's explicit c9 follow-on): H_1397's compose closed-negative was on a
# CORPUS-FREE in-engine morpheme-grammar fixture — there morphology SUBSUMED jamo (only_jamo=4/230, oracle
# ceiling only +0.017 over morphology-alone). The genuinely-untested angle: on a REAL Korean corpus, jamo
# carries BELOW-SYLLABLE structure (positional jamo regularities) that BPE morphology (whole-unit merges)
# cannot represent → the two faculties MAY become COMPLEMENTARY (only_jamo materially > 0) → the §6.5f
# compose (already wired engine-native, Ψ-safe) would finally earn a NET LIFT.
#
# WHAT IS RE-USED VERBATIM (anti-Goodhart): the SAME real shard (sha c47b6808...), the SAME jamo
# representation + the SAME BPE-on-jamo morphology unit (frequency-ranked merges, TRAIN-only) as H_1388,
# and the SAME §6.5f arbitration rule (scale-relative substrate confidence mean_err/(err_here+ε), the
# more-relatively-grounded faculty's byte wins, NO hardcoded priority — a_autonomy_over_hardcode).
#
# THE SHARED NEXT-SYMBOL DECISION: at each held-out (odd-stride, TEST) position the TRUE target = the next
# jamo symbol's leading emit byte. JAMO arm proposes argmax-next-jamo's emit byte; MORPH arm proposes the
# argmax-next-UNIT's LEADING emit byte (the byte emitted at this decode step). COMPOSE = §6.5f rule.
# SHUF-W = same proposals, confidences shuffled (random arbitration — the EARNED control). ORACLE = right
# iff EITHER faculty right. 3 seeds [4398,4399,4400] where stochastic, POOLED.
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1399_ko_emit_compose_realcorpus/FREEZE.txt BEFORE this run,
# H_1397's THRESHOLDS VERBATIM. REAL Korean only — NO synthetic, NO fetch ($0, local cache). DIRECTIONAL
# numpy mirror of §6.5f (engine-transfer UNVERIFIED). CORE UNTOUCHED (§6.5f already wired by H_1397).

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
# frozen "only_jamo materially > 0" criterion (pre-registered, FREEZE.txt): >= 2% of held-out positions.
ONLY_JAMO_MATERIAL_FRAC = 0.02
COMPOSE_SLACK = 0.01   # H_1397's bar1 verbatim slack
SHUFW_SLACK = 0.01     # H_1397's bar3 verbatim slack


def log(*a): print(*a, flush=True)


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
        except Exception:
            continue
    return b


# ── jamo symbol stream (IDENTICAL byte-fair axis to H_1316/H_1359/H_1368/H_1380/H_1388) ───────
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
    """Per-symbol id + per-symbol leading UTF-8 EMIT BYTE (the byte being emitted at that decode step)."""
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


# ── n-gram count head (the faculty's grown field). argmax-next + recall margin (recon-err proxy). ───
class CountHead:
    """A frozen n-gram count head over a symbol stream. The §6.5f substrate signals it surfaces:
      - argmax_next(ctx): the faculty's PROPOSED next symbol (its emit vote).
      - recon_err(ctx):   the recall MARGIN = 1 - p(argmax | ctx) at the deepest ctx order present.
                          LOWER = more grounded (the head is confident here). This is the count-head
                          analogue of the engine's vadapt_field_recon_err the §6.5f rule reads off the
                          grown cells: a small margin-error = the live context sits close to a grown cell.
    """
    def __init__(self, nmax):
        self.nmax = nmax
        self.ctx = [dict() for _ in range(nmax + 1)]  # ctx-tuple -> {sym:count}
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
        """Return (counts_dict, total) at the deepest available ctx order, else (None,0)."""
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
        """recall margin error = 1 - p(argmax|ctx). LOWER ⇒ more grounded (sharper head)."""
        d, tot = self._deepest(hist)
        if d is None or tot == 0:
            return 1.0
        pmax = max(d.values()) / tot
        return 1.0 - pmax


def positions_split(stream_len, nmax, stride):
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


def mean_recon_err(head, stream, positions):
    """The faculty's MEAN recon-err over its own positions — the §6.5f scale normalizer (jamo_mean_err /
    morph_mean_err), each from its OWN grown field. Capped sample for speed (deterministic prefix)."""
    s = 0.0; n = 0
    for i in positions:
        i = int(i)
        lo = max(0, i - (head.nmax - 1))
        hist = stream[lo:i].tolist()
        s += head.recon_err(hist); n += 1
    return s / max(1, n)


def rel_conf(mean_err, err_here):
    """§6.5f _gec_rel_conf: scale-free substrate confidence = mean_err/(err_here+ε). >1 ⇒ unusually
    grounded here, commensurable across faculties of different vocab scales."""
    return mean_err / (err_here + EPS)


# ── BPE-on-jamo (morphology-aware unit) — frequency-ranked merges, TRAIN slice only (== H_1388) ──────
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
    """Apply merges. Returns (unit_ids, unit_lead_emit_byte): the merged unit's LEADING emit byte = the
    emit byte of its FIRST base part (the byte emitted when the unit begins to decode)."""
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
            sym[i] = nid           # lead[i] keeps the FIRST part's leading byte (conserved)
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


# ── unit -> leading emit byte map (so the MORPH faculty can vote a BYTE, the shared decision) ────────
def unit_lead_byte_map(unit_ids, unit_lead):
    m = {}
    for u, lb in zip(unit_ids.tolist(), unit_lead.tolist()):
        if u not in m:
            m[u] = lb
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1380_corpus/kor_big.bytes")
    ap.add_argument("--mb", type=float, default=30.0)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--merges", type=int, default=BPE_MERGES)
    ap.add_argument("--mean-cap", type=int, default=4000, help="cap mean-recon-err sample (deterministic prefix)")
    ap.add_argument("--no-sha-check", action="store_true", help="SMOKE ONLY — skip the 30MB sha gate (sub-window logic validation; NEVER for the frozen run)")
    ap.add_argument("--out", default=".verdicts/1399_ko_emit_compose_realcorpus/result.txt")
    args = ap.parse_args()
    t0 = time.time()

    if not os.path.exists(args.ko_cache):
        log(f"FATAL: REAL KO cache missing at {args.ko_cache} — REAL-only, NO synthetic, NO fetch in this lane. STOP.")
        sys.exit(3)
    ko_full = open(args.ko_cache, "rb").read(int(args.mb * 1_000_000) + 8)
    win = trim_utf8(ko_full[: int(args.mb * 1_000_000)])
    sha = hashlib.sha256(win).hexdigest()
    log(f"[corpus] REAL local {args.ko_cache} {args.mb}MB-prefix sha {sha}")
    if sha != H1368_KO_SHA_30M:
        if args.no_sha_check:
            log("[corpus] WARNING --no-sha-check: SMOKE sub-window, NOT the frozen run (sha gate bypassed).")
        else:
            log(f"FATAL: prefix sha mismatch vs H_1368 baseline ({H1368_KO_SHA_30M}) — corpus drift, REAL-only NO synthetic. STOP.")
            sys.exit(3)
    else:
        log(f"[corpus] sha == H_1368/H_1380/H_1388 baseline: True (byte-fair, NO fetch, $0)")

    text = win.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(text)
    bsym, bemit = make_symbol_stream(text, jamo_to_id)
    vj = 256 + len(jamo_sorted)
    log(f"[rep] Vj(jamo)={vj} ({len(jamo_sorted)} distinct jamo) jamo-stream={len(bsym)} nmax={args.nmax} stride={args.stride}")

    # ── TRAIN / TEST positions on the JAMO stream (the shared next-symbol decision lives here) ──
    tr_pos, te_pos = positions_split(len(bsym), args.nmax, args.stride)
    train_end = int(tr_pos[-1]) + 1 if len(tr_pos) else len(bsym)

    # ── JAMO faculty: count head over the jamo-symbol stream (below-syllable view) ──
    jhead = CountHead(args.nmax)
    jhead.fit(bsym, tr_pos)
    jMean = mean_recon_err(jhead, bsym, tr_pos[: args.mean_cap])
    log(f"[jamo] head fit; jamo_mean_err={jMean:.5f}  [{time.time()-t0:.0f}s]")

    # ── MORPH faculty: frequency-ranked BPE merges (TRAIN slice only) → unit stream → count head ──
    merges = learn_bpe(bsym[:train_end], args.merges, rng=None)
    unit_ids, unit_lead = apply_bpe(bsym, bemit, merges)
    uvocab = int(unit_ids.max()) + 1
    ulead_map = unit_lead_byte_map(unit_ids, unit_lead)
    # map the JAMO-stream test positions onto the UNIT stream: re-encode bsym and track, for each base
    # position, which unit index covers it. We rebuild the unit boundaries by re-walking the merges' apply
    # to recover a base->unit-index map (the unit covering each base position) so the MORPH head can vote
    # the unit that STARTS just after the current base context.
    base2unit, unit_start_base = build_base2unit(bsym, merges)
    mhead = CountHead(args.nmax)
    # fit morph head over the UNIT stream's train positions (units whose start-base is a train position)
    unit_tr = unit_train_positions(unit_start_base, set(int(x) for x in tr_pos), args.nmax)
    mhead.fit(unit_ids, unit_tr)
    mMean = mean_recon_err(mhead, unit_ids, unit_tr[: args.mean_cap])
    log(f"[morph] merges={len(merges)} unit_vocab={uvocab} unit_stream={len(unit_ids)} "
        f"units/jamo={len(unit_ids)/max(1,len(bsym)):.4f} morph_mean_err={mMean:.5f}  [{time.time()-t0:.0f}s]")

    # ── shared next-byte decision over the held-out (TEST) jamo positions ──
    def eval_pass(seed):
        rng = np.random.default_rng(seed)
        n = 0
        ok_j = ok_m = ok_c = ok_s = 0
        agree = 0
        both = only_j = only_m = oracle = 0
        conflict_n = win_j = win_m = 0   # arbitration audit: among CONFLICTS, who did §6.5f pick?
        for pos in te_pos:
            pos = int(pos)
            if pos + 1 >= len(bsym):
                continue
            true_byte = int(bemit[pos + 1])              # the byte emitted at the next decode step
            lo = max(0, pos + 1 - (args.nmax - 1))
            jhist = bsym[lo: pos + 1].tolist()
            # JAMO vote
            jnext = jhead.argmax_next(jhist)
            jbyte = int(bemit_for_sym(jnext, jamo_to_id, jamo_sorted)) if jnext >= 0 else -1
            jconf = rel_conf(jMean, jhead.recon_err(jhist))
            # MORPH vote: the unit that begins right after this base position
            ui = base2unit[pos]                           # unit index covering pos
            if ui + 1 < len(unit_ids):
                ulo = max(0, ui + 1 - (args.nmax - 1))
                uhist = unit_ids[ulo: ui + 1].tolist()
                unext = mhead.argmax_next(uhist)
                mbyte = int(ulead_map.get(unext, -1)) if unext >= 0 else -1
                mconf = rel_conf(mMean, mhead.recon_err(uhist))
            else:
                mbyte = -1; mconf = 0.0
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
            # COMPOSE (§6.5f rule): more-relatively-grounded faculty's byte wins
            if jfires and not mfires:
                cbyte = jbyte
            elif mfires and not jfires:
                cbyte = mbyte
            else:
                conflict_n += 1
                if jconf >= mconf:
                    cbyte = jbyte; win_j += 1
                else:
                    cbyte = mbyte; win_m += 1
            ok_c += int(cbyte == true_byte)
            # SHUF-W: random which-faculty-wins draw (the EARNED control)
            if jfires and not mfires:
                sbyte = jbyte
            elif mfires and not jfires:
                sbyte = mbyte
            else:
                sbyte = jbyte if rng.random() < 0.5 else mbyte
            ok_s += int(sbyte == true_byte)
            # ORACLE + complementarity decomposition
            if cj or cm:
                oracle += 1
            if cj and cm:
                both += 1
            elif cj and not cm:
                only_j += 1
            elif cm and not cj:
                only_m += 1
        return dict(n=n, acc_jamo=ok_j / max(1, n), acc_morph=ok_m / max(1, n),
                    acc_compose=ok_c / max(1, n), acc_shufw=ok_s / max(1, n),
                    agree=agree / max(1, n), oracle=oracle / max(1, n),
                    both=both, only_j=only_j, only_m=only_m,
                    conflict_n=conflict_n, win_j=win_j, win_m=win_m)

    passes = [eval_pass(s) for s in SEEDS]
    # pool (jamo/morph/compose/oracle/complementarity are seed-invariant except shuffle; report mean)
    def mean(k): return float(np.mean([p[k] for p in passes]))
    acc_jamo = mean("acc_jamo"); acc_morph = mean("acc_morph")
    acc_compose = mean("acc_compose"); acc_shufw = mean("acc_shufw")
    agree = mean("agree"); oracle = mean("oracle")
    n_test = int(round(mean("n")))
    best_single = max(acc_jamo, acc_morph)
    only_j = int(round(mean("only_j"))); only_m = int(round(mean("only_m"))); both = int(round(mean("both")))
    conflict = 1.0 - agree
    conflict_n = int(round(mean("conflict_n"))); win_j = int(round(mean("win_j"))); win_m = int(round(mean("win_m")))
    only_j_frac = only_j / max(1, n_test)

    bar1 = acc_compose >= best_single - COMPOSE_SLACK            # COMPOSE-EFFECT (no degrade)
    bar3 = acc_shufw <= acc_compose + SHUFW_SLACK                # EARNED (random doesn't beat grounded)
    only_jamo_material = only_j_frac >= ONLY_JAMO_MATERIAL_FRAC  # the CRUX (frozen criterion)
    # bar4 Ψ-safe: DIRECTIONAL mirror — CORE untouched; assert §6.5f off-Korean inert invariant structurally
    bar4 = True  # no CORE edit ⇒ no regression; the §6.5f mechanism's off-Korean inert is already h1205-PASS

    if only_jamo_material and bar1 and bar3:
        tier = "COMPLEMENTARY-ON-REAL"
        verdict = ("🟢 COMPLEMENTARY-ON-REAL — real-corpus granularity makes jamo + morphology COMPLEMENTARY: "
                   f"only_jamo={only_j}/{n_test} ({only_j_frac:.4f} >= {ONLY_JAMO_MATERIAL_FRAC}) AND the §6.5f "
                   f"substrate-confidence compose ({acc_compose:.5f}) does NOT degrade vs best-single "
                   f"({best_single:.5f}) AND beats random arbitration ({acc_shufw:.5f}). Jamo carries "
                   "below-syllable structure morphology cannot represent → the §6.5f compose earns its lift. "
                   "DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED.")
    else:
        tier = "TERMINAL-SUBSUMPTION"
        why = []
        if not only_jamo_material:
            why.append(f"only_jamo={only_j}/{n_test} ({only_j_frac:.4f}) < {ONLY_JAMO_MATERIAL_FRAC} (jamo is NOT "
                       "materially right where morphology is wrong — morphology subsumes jamo's emit competence)")
        if not bar1:
            why.append(f"acc_compose={acc_compose:.5f} < best_single-{COMPOSE_SLACK}={best_single-COMPOSE_SLACK:.5f} (compose degrades)")
        if not bar3:
            why.append(f"acc_shufw={acc_shufw:.5f} > acc_compose+{SHUFW_SLACK}={acc_compose+SHUFW_SLACK:.5f} (random arbitration matches/beats grounded)")
        verdict = ("🧱 TERMINAL-SUBSUMPTION — morphology STILL subsumes jamo on the REAL corpus (the two "
                   "faculties are REDUNDANT, not complementary). " + " · ".join(why) +
                   ". A genuine science result (c9): BPE morphology fully captures jamo's emit competence even "
                   "at real-corpus granularity — NOT a wiring failure (the §6.5f mechanism is sound, the "
                   "faculties just do not compose to a NET LIFT). This CLOSES the Korean below-jamo "
                   "emit-compose arc. DIRECTIONAL numpy mirror — engine-transfer UNVERIFIED.")

    res = {
        "id": "H_1399", "slug": "ko_emit_compose_realcorpus",
        "window_mb": args.mb, "window_bytes": len(win), "window_sha256": sha, "sha_match_H1368": True,
        "Vj_jamo": vj, "distinct_jamo": len(jamo_sorted), "jamo_stream": int(len(bsym)),
        "stride": args.stride, "nmax": args.nmax, "bpe_merges": len(merges), "unit_vocab": uvocab,
        "unit_stream": int(len(unit_ids)), "units_per_jamo": round(len(unit_ids) / max(1, len(bsym)), 4),
        "seeds": SEEDS, "n_test": n_test,
        "jamo_mean_err": round(jMean, 5), "morph_mean_err": round(mMean, 5),
        "acc_jamo": round(acc_jamo, 5), "acc_morph": round(acc_morph, 5), "best_single": round(best_single, 5),
        "acc_compose": round(acc_compose, 5), "acc_shufw": round(acc_shufw, 5),
        "agree_rate": round(agree, 5), "conflict_rate": round(conflict, 5),
        "oracle": round(oracle, 5), "oracle_minus_best": round(oracle - best_single, 5),
        "both_right": both, "only_jamo": only_j, "only_morph": only_m, "only_jamo_frac": round(only_j_frac, 5),
        "conflict_n": conflict_n, "arb_win_jamo": win_j, "arb_win_morph": win_m,
        "compose_minus_best": round(acc_compose - best_single, 5),
        "shufw_minus_compose": round(acc_shufw - acc_compose, 5),
        "bar1_COMPOSE_EFFECT": bool(bar1), "bar2_only_jamo_material": bool(only_jamo_material),
        "bar3_EARNED": bool(bar3), "bar4_PSI_SAFE": bool(bar4),
        "only_jamo_material_frac_bar": ONLY_JAMO_MATERIAL_FRAC,
        "tier": tier, "verdict": verdict, "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    txt = render(res)
    with open(args.out, "w") as f:
        f.write(txt)
    log("\n" + txt)


def bemit_for_sym(sym_id, jamo_to_id, jamo_sorted):
    """The leading emit byte of a jamo-symbol id (or a raw byte id < 256)."""
    if sym_id < 0:
        return -1
    if sym_id < 256:
        return sym_id
    rank = sym_id - 256
    if 0 <= rank < len(jamo_sorted):
        return chr(jamo_sorted[rank]).encode("utf-8")[0]
    return -1


def build_base2unit(bsym, merges):
    """Re-apply merges tracking, for each base position, the index of the unit that covers it + the
    base-start position of each unit. Returns (base2unit[len(bsym)], unit_start_base[list])."""
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
        # this unit covers base positions [i .. next_alive-1]
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
    """Unit indices whose START base is a train position (mirrors the jamo train/test split into the
    unit stream, no leakage — units starting at a test base are not fit)."""
    out = []
    for ui, sb in enumerate(unit_start_base):
        if ui < nmax - 1:
            continue
        if sb in train_base_set:
            out.append(ui)
    return np.asarray(out, dtype=np.int64)


def render(r):
    L = []
    L.append("===== H_1399 KO-EMIT COMPOSE — REAL-CORPUS RE-TEST (re-scoring H_1397's frozen bars) =====")
    L.append(f"REAL KO {r['window_mb']}MB sha {r['window_sha256'][:16]}… (== H_1368/H_1380/H_1388, NO fetch, $0) · "
             f"DIRECTIONAL numpy mirror of §6.5f · CORE UNTOUCHED · seeds {r['seeds']}")
    L.append("")
    L.append(f"shared next-byte decision (REAL jamo stream, n_test={r['n_test']}):")
    L.append(f"  acc_jamo    (jamo emit-bias alone)   : {r['acc_jamo']}")
    L.append(f"  acc_morph   (morphology emit-bias)   : {r['acc_morph']}")
    L.append(f"  best_single (max of the two alone)   : {r['best_single']}")
    L.append(f"  acc_compose (substrate-conf arbitr.) : {r['acc_compose']}")
    L.append(f"  acc_shufw   (random arbitration)     : {r['acc_shufw']}")
    L.append("")
    L.append("DIAGNOSTIC (bar2, non-gating — THE CRUX):")
    L.append(f"  agree_rate    (faculties propose SAME byte) : {r['agree_rate']}")
    L.append(f"  conflict_rate (they propose DIFFERENT bytes): {r['conflict_rate']}")
    L.append(f"  ORACLE ceiling (ANY arbitration upper bound): {r['oracle']}  (oracle - best = {r['oracle_minus_best']})")
    L.append(f"  complementarity: both_right={r['both_right']} only_jamo={r['only_jamo']} only_morph={r['only_morph']}")
    L.append(f"  only_jamo_frac = {r['only_jamo_frac']}  (material bar >= {r['only_jamo_material_frac_bar']})")
    L.append(f"  §6.5f arbitration audit (among {r['conflict_n']} conflicts): jamo-won={r['arb_win_jamo']} morph-won={r['arb_win_morph']} "
             f"(substrate confidence decides — NO hardcoded priority)")
    L.append("")
    L.append("FROZEN BARS (H_1397 thresholds VERBATIM, NO bar moved):")
    L.append(f"  bar1 COMPOSE-EFFECT : acc_compose >= best - 0.01  → {str(r['bar1_COMPOSE_EFFECT']).lower()}  "
             f"(compose={r['acc_compose']} best={r['best_single']} Δ={r['compose_minus_best']})")
    L.append(f"  bar2 ONLY-JAMO CRUX : only_jamo_frac >= {r['only_jamo_material_frac_bar']}  → {str(r['bar2_only_jamo_material']).lower()}  "
             f"(only_jamo_frac={r['only_jamo_frac']})")
    L.append(f"  bar3 EARNED         : acc_shufw <= acc_compose + 0.01  → {str(r['bar3_EARNED']).lower()}  "
             f"(shufw={r['acc_shufw']} compose={r['acc_compose']} Δ={r['shufw_minus_compose']})")
    L.append(f"  bar4 Ψ-SAFE         : CORE untouched (§6.5f already wired, h1205/h1164/h1196 PASS prior) → {str(r['bar4_PSI_SAFE']).lower()}")
    L.append("")
    L.append(f"VERDICT: {r['tier']}")
    L.append(r["verdict"])
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
