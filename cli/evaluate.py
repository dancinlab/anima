#!/usr/bin/env python3
# evaluate.py — anima MEASUREMENT single entry (cli/evaluate.hexa's py twin).
#
# WHY THIS FILE (single-entry measurement · a_engine_native_learning): anima's two
# installed verbs are SYMMETRIC across two files — cli/train.{hexa,py} = LEARNING,
# cli/evaluate.{hexa,py} = MEASUREMENT. `anima evaluate <ckpt>` scores the full ρ-AXON
# reach battery (Ψ-SOMA reach layer · owner redesign of the old G-ladder · cli/rho_axon.py;
# the frozen bars this driver runs today = the former G0-G6) with the engine's OWN ops —
# the reach-scoring system is folded DIRECTLY into
# this measurement single-entry (the former separate core/g_gates.py module was absorbed
# here — measurement = evaluate.{hexa,py} ONE FILE). Decode enters via the generator L3
# mouth (gen_auto_ideate → clm/bytegpt decode), so the py evaluate is byte-identical to
# the hexa `anima evaluate`. No new metric is invented here (logic byte-identical to the
# absorbed g_gates module — only the file home changed).
#
# This py evaluate is torch-free and gauge-free — the scoring is the numpy `math.log`
# mirror, so `anima evaluate` stays a clean engine-native measurement surface (the gate
# enforcer's torch/gauge grep over this file must come back empty).
#
# USAGE (installed `anima` PATH command — NOT `hexa run`):
#   python3 cli/evaluate.py                              — usage (no args)
#   python3 cli/evaluate.py <ckpt> [--corpus <p>...] [--gen N]
#                                                       — ρ-AXON reach battery (former G0-G6)
#
# 2-PRODUCTION (a_engine_native_learning): byte-parity twin = cli/evaluate.hexa. Both
# define the SAME eval_reach_all driver in-file.

import os
import sys
import math
import json
import random
import hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
# core/ is the engine package; the decode mouths (clm_decode, bytegpt_decode) + the G6
# ideation ops live there. Add core/ to the path so they resolve.
sys.path.insert(0, os.path.join(_REPO, "core"))

import decode as clm   # unified core decoder (conv+byte mouths), KV-cache fast path
import decode as bg     # same module; both aliases resolve the union public API
from rho_fan import (
    _rho_fan_concepts, _rho_fan_words, _rho_fan_dict_load, _rho_fan_known_word_ratio,
    _rho_fan_is_falsifiable, _rho_fan_jaccard, rho_fan_build_frames, rho_fan_frame_guard,
    rho_fan_detector_calibration,
    _rho_fan_stopwords, _rho_fan_derangement,          # H_9693 --fan-bind (frozen gate reuse)
    # H_9212 ③ per-cell dispatch: 4 register cells + ko codepoint-aware tokenizer + kwr_ko gate
    _rho_fan_cells, _rho_fan_cell_lang, _rho_fan_words_uni, _rho_fan_ko_known_word_ratio,
    KWR_KO_GATE,
)

# H_9200 — process-global: render the ρ-AXON reach panel (cli/rho_axon.py) instead of the
# G0-G6 battery when `anima-py evaluate --rho-axon` is passed (set in main()).
_RHO_AXON = False


# ════════════════════════════════════════════════════════════════════════
# ρ-AXON REACH SCORING (absorbed from the former core/g_gates.py module —
# measurement = this single file). Ported 1:1 from the hexa SSOT; decode enters
# via the py CLMConvMoE / ByteGPT mouth (clm_decode / bytegpt_decode), hoisting the
# weight load ONCE (== gen_clm_ideate_W in the hexa engine). torch-free numpy mirror.
#
# ρ-AXON is the current-standard reach layer (cli/rho_axon.py · design SSOT
# state/rho_axon_measurement/) — an owner redesign OVER these frozen bars. The
# detector identifiers below (eval_rho_form…g6) are the load-bearing frozen substrate
# ρ-AXON reuses; the G→ρ mapping (axis names shown first-time here) is:
#   ρ·form   ← G0 COHERENCE      kwr>=0.50 on >=4/5 single-concept gens
#   ρ·weave  ← G1 RECOMBINATION  some k: composed_distinct>=2 AND >max_single AND coherent (the central WALL)
#   ρ·leap   ← G2 NOVELTY        >=3 distinct coherent corpus-absent n-grams AND control=0
#   ρ·self   ← G3 PHILOSOPHY     Psi-fixed-point self-identity continuity (architecture read)
#   ρ·tether ← G5 NON-FAB        L1 fab-rate<=0.30 AND L2 abstain (L2 = engine §ImmuneMemory)
#   ρ·fan    ← G6 IDEATION ★     >=5 distinct (pairwise Jaccard<0.5) AND >=1 falsifiable
#   ρ·store  ← (NEW · held-out association retrieval · PENDING, no old-G)
#   REACH-CLOSED a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2)
# FROZEN-FIRST bars (7B_PASS_CONDITIONS.md VERBATIM, p7 — NO tune-to-green).
#
# SCOPE NOTE: G3 (self-identity, ckpt-independent) is ported here. G5-L2 (live
# §ImmuneMemory / VAdaptField abstain) is a large engine subsystem NOT yet ported
# to py — G5 reports L1 + marks L2 pending. Neither affects the a7b_pass closure.
# ════════════════════════════════════════════════════════════════════════


def _default_gen():
    return 40


# ════════════════════════════════════════════════════════════════════════
# decode entry — gen_auto_ideate(ckpt) MOUTH-SNIFF dispatch (generator L3).
#
# Mirrors the hexa gen_auto_ideate -> generator gen_auto_backend mouth dispatch
# (a_core_engine_map): sniff the ckpt header — CLM\x01 magic => ConvMoE .clm mouth
# (clm_decode), else a sane 5xu32 ByteGPT header => transformer .bin mouth
# (bytegpt_decode). Both hoist the weight load ONCE and ideate via the byte-parity-
# proven seeded top-k sampler. The clm path is unchanged.
# ════════════════════════════════════════════════════════════════════════

class _Mouth:
    _n_decode = 0

    def __init__(self, ckpt, grow_window=False):
        # H_9804 Fix-W: default False = production T=24, byte-for-byte unchanged.
        self.grow_window = bool(grow_window)
        self.ckpt = ckpt
        self._score_cache = {}
        if bg.bg_is_bytegpt(ckpt):
            self.kind = "bytegpt"
            self.W = bg.bg_load(ckpt)
            if not self.W.get("ok"):
                raise RuntimeError("ckpt not decodable (bytegpt): " + ckpt)
        elif clm.clm_decodable(ckpt):
            self.kind = "clm"
            self.W = clm.clm_load_weights(ckpt)
            if not self.W.get("ok"):
                raise RuntimeError("ckpt not decodable (clm): " + ckpt)
        else:
            raise RuntimeError("ckpt not decodable (unknown mouth): " + ckpt)

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        # keep-alive heartbeat: the hexa launcher captures this decode's stdout via
        # exec(); a long idle (a 303M numpy decode emits nothing until it returns)
        # drops that captured pipe → BrokenPipe mid-battery (303M gen80 died at ~8min;
        # the gen8 smoke was fast enough to finish first). One line per decode keeps
        # the pipe live across the full G0-G6 battery. Heartbeat only — no scoring effect.
        _Mouth._n_decode += 1
        print("  [decode #" + str(_Mouth._n_decode) + "] " + self.kind
              + " gen=" + str(gen) + " seed_rng=" + str(seed_rng)
              + (" grow_window" if self.grow_window else ""), flush=True)
        if self.kind == "bytegpt":
            # seed string -> byte ids inside bytegpt_decode (_seed_to_ids); the
            # ByteGPT window grows up to block natively (no fixed-T right-align).
            return bg.bytegpt_decode_topk_sampled_W(
                self.W, seed, gen, top_k, temp, seed_rng)["text"]
        # H_9804 Fix-W (--grow-window) · H_6189 measurement-wall repair. The CLM mouth
        # right-aligns the seed into a fixed T=24 window, so for a composed G1 seed the
        # VISIBLE window is byte-identical to the corresponding single seed's window —
        # composed_distinct > max_single is then structurally impossible, independent of
        # the model (byte-math proof: state/gate_design_audit/window_math.json). The frozen
        # bar (H_1129/H_1137 VERBATIM) was calibrated on the ByteGPT mouth at block=512,
        # i.e. it PRESUPPOSES the whole composed seed is conditioned on. T=24 is a later
        # CLM decode contract that leaked into the gate, not a gate spec. Fix-W restores
        # the frozen bar's own semantics on the CLM mouth: T_win = min(len(seed)+gen, 512),
        # matching what ByteGPT already does natively. The bar itself does NOT move — this
        # un-truncates the seed (forward math untouched; conv trunk is causal-local with no
        # positional encoding, trained seq_len=1024, and the scoring lane already runs T=64).
        if self.grow_window:
            t_prev = clm._CONSULT_DECODE_T
            t_win = len(seed.encode('utf-8', 'surrogateescape')) + max(int(gen), 0)
            if t_win > 512:
                t_win = 512
            if t_win < 24:
                t_win = 24
            clm.set_consult_decode_window(t_win)
            try:
                return clm.clm_decode_topk_sampled_W(
                    self.W, seed, gen, top_k, temp, seed_rng)["text"]
            finally:
                clm.set_consult_decode_window(t_prev)
        return clm.clm_decode_topk_sampled_W(
            self.W, seed, gen, top_k, temp, seed_rng)["text"]

    def score(self, text):
        """Mean next-byte CE used to rank candidate surfaces."""
        if text in self._score_cache:
            return self._score_cache[text]
        ids = list(text.encode("utf-8", "surrogateescape"))
        if len(ids) < 2:
            return float("nan")
        if self.kind == "bytegpt":
            result = bg.bytegpt_ce_ranged(self.ckpt, ids)
            value = float(result["ce_mean"]) if result.get("ok") else float("nan")
        else:
            value = float(clm.clm_ce_seq_W(self.W, None, ids))
        self._score_cache[text] = value
        return value

    def score_many(self, texts):
        return tuple(self.score(text) for text in texts)


def _isolated_ideate_worker(conn, ckpt, seed, gen, top_k, temp, seed_rng):
    """One decode in a disposable process so NumPy's large CPU arenas are returned."""
    try:
        conn.send((True, _Mouth(ckpt).ideate(seed, gen, top_k, temp, seed_rng)))
    except BaseException as exc:
        conn.send((False, repr(exc)))
    finally:
        conn.close()


class _IsolatedMouth:
    """ρ-AXON CPU fallback; identical decoder, process-scoped allocation lifetime."""

    def __init__(self, ckpt):
        self.ckpt = ckpt

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        import multiprocessing as mp
        ctx = mp.get_context("spawn")
        parent, child = ctx.Pipe(duplex=False)
        proc = ctx.Process(
            target=_isolated_ideate_worker,
            args=(child, self.ckpt, seed, gen, top_k, temp, seed_rng),
        )
        proc.start()
        child.close()
        try:
            ok, payload = parent.recv()
        except EOFError as exc:
            proc.join()
            raise RuntimeError("isolated decode exited without a result: %s" % proc.exitcode) from exc
        finally:
            parent.close()
        proc.join()
        if proc.exitcode != 0:
            raise RuntimeError("isolated decode failed with exit code %s" % proc.exitcode)
        if not ok:
            raise RuntimeError("isolated decode failed: " + payload)
        return payload


class _MemoMouth:
    """Reuse exact deterministic probe calls shared across ρ axes/cells."""

    def __init__(self, mouth, cache_dir="", namespace=""):
        self.mouth = mouth
        self.cache = {}
        self.cache_dir = cache_dir
        self.namespace = namespace
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        key = (seed, int(gen), int(top_k), float(temp), int(seed_rng))
        if key not in self.cache:
            disk = ""
            if self.cache_dir:
                digest = hashlib.sha256(
                    json.dumps((self.namespace, key), ensure_ascii=False,
                               separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                disk = os.path.join(self.cache_dir, digest + ".json")
                if os.path.exists(disk):
                    with open(disk, "r", encoding="utf-8") as handle:
                        self.cache[key] = json.load(handle)["text"]
            if key not in self.cache:
                self.cache[key] = self.mouth.ideate(seed, gen, top_k, temp, seed_rng)
                if disk:
                    tmp = disk + ".tmp.%d" % os.getpid()
                    with open(tmp, "w", encoding="utf-8") as handle:
                        json.dump({"text": self.cache[key]}, handle, ensure_ascii=True)
                    os.replace(tmp, disk)
        return self.cache[key]


# ════════════════════════════════════════════════════════════════════════
# G0 — COHERENCE
# ════════════════════════════════════════════════════════════════════════

def eval_rho_form(mouth, gen, known, seed_off=0):
    cz = _rho_fan_concepts()
    ratios = []; texts = []; n_coherent = 0
    for i in range(len(cz)):
        seed = cz[i] + ": "
        o = mouth.ideate(seed, gen, 40, 0.7, 7 + i + seed_off)
        kwr = _rho_fan_known_word_ratio(o, known)
        ratios.append(kwr); texts.append(o)
        if kwr >= 0.5:
            n_coherent += 1
    return {"pass": n_coherent >= 4, "n_coherent": n_coherent,
            "ratios": ratios, "texts": texts}


# ════════════════════════════════════════════════════════════════════════
# G1 — RECOMBINATION  (H_1129)
# ════════════════════════════════════════════════════════════════════════

def _g_concept_keywords():
    return [["consciousness", "cells", "mind", "aware"],
            ["tension", "ripple", "distant", "between"],
            ["memory", "meaning", "compose", "new"],
            ["silence", "information", "quiet", "carries"],
            ["dream", "engine", "alone", "sleep"]]


def _g_coverage_with(text, kwsets):
    """Frozen coverage rule, VERBATIM, parameterised by the keyword table so a control arm
    scores on byte-identical logic (H_9804 null controls). _g_coverage is unchanged."""
    wm = set(_rho_fan_words(text))
    covered = 0
    for kw in kwsets:
        if any(k in wm for k in kw):
            covered += 1
    return covered


def _g_coverage(text):
    return _g_coverage_with(text, _g_concept_keywords())


def _g_random_keywords(known, rng_seed=20260720):
    """H_9804 NULL-A (chance floor). Five size-matched keyword sets drawn from the model's own
    known-word dictionary, EXCLUDING every real concept keyword. Answers: how often does free
    text hit 5 arbitrary 4-word sets? `_g_coverage` counts HOW MANY of the five sets are hit, so
    permuting the real sets is an IDENTITY on this metric — a derangement control would test
    nothing. Re-drawing the words is the control that actually has a null."""
    real = set()
    for kw in _g_concept_keywords():
        real.update(kw)
    pool = sorted(w for w in known if w not in real and len(w) >= 4)
    if len(pool) < 20:
        return None                                   # dictionary too small ⇒ control unavailable
    st = rng_seed & 0xFFFFFFFF
    picked, out = [], []
    for _ in range(len(_g_concept_keywords())):
        cell = []
        for _ in range(len(_g_concept_keywords()[0])):
            st = (1103515245 * st + 12345) & 0x7FFFFFFF
            cell.append(pool[st % len(pool)])
        out.append(cell); picked.extend(cell)
    return out


def _g_neutral_seed(nbytes):
    """H_9804 NULL-B (causal ablation). A concept-free seed of matched byte length: if a
    concept-free prompt scores the same coverage, the composed seed contributed nothing and the
    'recombination' reading is unattributable."""
    filler = "the of and to in that it is was for on with as by at from "
    out = []
    while sum(len(x) for x in out) < nbytes:
        out.append(filler)
    return "".join(out)[:max(nbytes, 1)]


def _echo_spans(seed, text, n=8):
    """H_9804 echo-guard. Return `text` with every >=n-byte substring that also occurs in
    `seed` blanked out. Widening the decode window (Fix-W) makes the whole composed seed
    visible to the mouth, which creates a NEW false-GREEN route the T=24 regime did not
    have: the model can simply re-emit the seed's concept words and score coverage without
    recombining anything. H_6189 named this risk and made the guard mandatory."""
    if not seed or not text:
        return text
    out = list(text)
    ln = len(text)
    i = 0
    while i < ln:
        j = ln
        hit = -1
        while j - i >= n:
            if text[i:j] in seed:
                hit = j
                break
            j -= 1
        if hit > 0:
            for p in range(i, hit):
                out[p] = " "
            i = hit
        else:
            i += 1
    return "".join(out)


def _echo_ratio(seed, text, n=8):
    """Fraction of `text` that is a >=n-byte verbatim echo of `seed` (0.0 = no echo)."""
    if not text:
        return 0.0
    blanked = _echo_spans(seed, text, n)
    echoed = sum(1 for a, b in zip(text, blanked) if a != b)
    return echoed / float(len(text))


def eval_rho_weave(mouth, gen, known, seed_off=0, null_mode="off"):
    cz = _rho_fan_concepts()
    n = len(cz)
    g_single = gen if (gen > 0 and gen < 80) else 80
    g_comp = gen if (gen > 0 and gen < 120) else 120
    max_single = 0
    for s in range(n):
        seed = cz[s] + ". "
        o = mouth.ideate(seed, g_single, 40, 0.7, 7 + s + seed_off)
        cov = _g_coverage(o)
        if cov > max_single:
            max_single = cov
    ks = []; passed = False; best_k = 0; best_distinct = 0
    best_distinct_noecho = 0; echo_max = 0.0
    best_null_a = -1; best_null_b = -1
    null_kw = _g_random_keywords(known) if null_mode in ("random-kw", "neutral-seed") else None
    for k in range(2, n + 1):
        seed = ""
        for c in range(k):
            if c > 0:
                seed += ". "
            seed += cz[c]
        seed += ". "
        o = mouth.ideate(seed, g_comp, 40, 0.7, 7 + seed_off)
        cov = _g_coverage(o)
        kwr = _rho_fan_known_word_ratio(o, known)
        coherent = kwr >= 0.5
        clears = cov >= 2 and cov > max_single and coherent
        # H_9804 echo-guard (ADDITIVE — the frozen `_g_coverage(o)` above is called
        # unmodified and the bar reads IT; these are validity telemetry, and by
        # construction cov_noecho <= cov, so the guard can only ever withdraw a
        # GREEN, never manufacture one).
        er = _echo_ratio(seed, o)
        cov_noecho = _g_coverage(_echo_spans(seed, o))
        if null_kw is not None:                        # NULL-A: same text, random keyword table
            c = _g_coverage_with(_echo_spans(seed, o), null_kw)
            if c > best_null_a:
                best_null_a = c
        if null_mode == "neutral-seed":                # NULL-B: concept-free seed, same budget
            ns = _g_neutral_seed(len(seed.encode("utf-8", "surrogateescape")))
            on = mouth.ideate(ns, g_comp, 40, 0.7, 7 + seed_off)
            c = _g_coverage(_echo_spans(ns, on))
            if c > best_null_b:
                best_null_b = c
        if er > echo_max:
            echo_max = er
        ks.append({"k": k, "distinct": cov, "kwr": kwr, "coherent": coherent, "clears": clears,
                   "echo_ratio": er, "distinct_noecho": cov_noecho})
        if clears:
            passed = True
        if cov > best_distinct:
            best_distinct = cov; best_k = k
        if cov_noecho > best_distinct_noecho:
            best_distinct_noecho = cov_noecho
    return {"pass": passed, "max_single": max_single, "best_k": best_k,
            "best_distinct": best_distinct, "ks": ks,
            "best_distinct_noecho": best_distinct_noecho, "echo_max": echo_max,
            # ECHO-SUSPECT: the frozen bar passed, but stripping verbatim seed-echo
            # takes it back below the bar ⟹ the pass rode on re-emission, not
            # recombination. Read as INVALID, never as a G1 crack.
            "null_a": best_null_a, "null_b": best_null_b, "null_mode": null_mode,
            "echo_suspect": bool(passed and not (best_distinct_noecho >= 2
                                                 and best_distinct_noecho > max_single))}


# ════════════════════════════════════════════════════════════════════════
# system-G1 — RECOMBINATION RELOCATION  (card H_9035, Direction A)
# ════════════════════════════════════════════════════════════════════════
#
# Relocates recombination OUT of the mouth-only eval_rho_weave path INTO the pipe:
#     held-out DISTANT pair (A,B)
#       → Stage M  frozen mouth ideate(A), ideate(B)            (G0 fluency)
#       → Stage K  kosmos_merge: recursive labeled-parent bind  (A,B as children)
#       → Stage B  brain realizes/releases the joint utterance C
#       → score bind-RECOVERABILITY on the SURFACED C only (store-id HARD-BLOCKED)
#         + SCRAMBLE ablation.
#
# This is the py-2-production (session-eval-py-only) engine-native version of the
# round-1 numpy harness (state/system_g1_relocate_kosmos_merge/system_g1_harness.py)
# — same FROZEN bar (FREEZE.txt), but Stage M/B run through the REAL _Mouth (303M
# .clm/.bin) instead of a toy. The kosmos_merge step mirrors core/kosmos_io.hexa
# kosmos_merge (children preserved, mean tension, lane="recomb" DISJOINT from
# emit-drive {0,4}). RECOVERY reads ONLY C — the store's parent-ids are withheld,
# so a lookup earns ZERO (H_1874). Honest expectation for the real mouth = the
# MOUTHFLOOR floor (cannot surface both concepts in one coherent joint utterance).

# ── FROZEN bar (FREEZE.txt — do NOT move post-hoc) ──────────────────────────
_SG1_SEEDS      = [7, 42, 4302]
_SG1_M          = 24
_SG1_N_DISTRACT = 8
_SG1_COV_BAR    = _SG1_M // 2                       # 12
_SG1_REC_BAR    = _SG1_M // 2                       # 12
_SG1_LEAK_BAR   = (_SG1_N_DISTRACT - 2) / _SG1_N_DISTRACT   # 0.75
_SG1_SCR_DROP   = _SG1_M // 2                        # 12

# distant concepts → keyword sets (disjoint vocab ⇒ H_1599 data-presence control).
_SG1_CONCEPTS = {
    "ocean":    ["tide", "salt", "wave", "deep", "current"],
    "forest":   ["moss", "branch", "fern", "canopy", "root"],
    "engine":   ["piston", "fuel", "gear", "torque", "cylinder"],
    "music":    ["chord", "tempo", "melody", "rhythm", "harmony"],
    "market":   ["price", "trade", "stock", "ledger", "buyer"],
    "medicine": ["dose", "fever", "immune", "remedy", "cure"],
    "desert":   ["dune", "cactus", "mirage", "arid", "sand"],
    "galaxy":   ["orbit", "nebula", "comet", "stellar", "star"],
    "kitchen":  ["knife", "simmer", "flour", "roast", "spice"],
    "law":      ["statute", "verdict", "counsel", "appeal", "court"],
    "glacier":  ["crevasse", "moraine", "frost", "calve", "ice"],
    "circuit":  ["resistor", "voltage", "solder", "diode", "wire"],
}


def _sg1_bigrams(tokens):
    from collections import Counter
    return Counter(zip(tokens, tokens[1:]))


def _sg1_cos(u, v):
    dot = sum(u[k] * v.get(k, 0) for k in u)
    nu = sum(x * x for x in u.values()) ** 0.5
    nv = sum(x * x for x in v.values()) ** 0.5
    return dot / (nu * nv + 1e-9)


def _sg1_coverage(text, a, b):
    wm = set(_rho_fan_words(text))
    cov = 0
    for cpt in (a, b):
        if any(k in wm for k in _SG1_CONCEPTS[cpt]):
            cov += 1
    return cov


# kosmos_merge mirror (core/kosmos_io.hexa kosmos_merge): recursive labeled-parent
# bind — anchor_c keeps A,B as children; the ids are HARD-BLOCKED from RECOVERY.
def _sg1_kosmos_merge(frag_a, frag_b, ta, tb):
    a = {"text": frag_a, "lane": "recomb", "tension_5ch": ta}
    b = {"text": frag_b, "lane": "recomb", "tension_5ch": tb}
    mean5 = [(ta[i] + tb[i]) / 2.0 for i in range(5)]
    c = {"text": None, "lane": "recomb", "tension_5ch": mean5, "children": (a, b)}
    return c


# INDEPENDENT recoverer R — reads ONLY C's surfaced tokens; parent-ids withheld.
# top-2 by bigram cosine over the N=8 pool; a candidate counts only with cos>0.
def _sg1_recover(C_text, pool, scramble, seed):
    import random
    toks = _rho_fan_words(C_text)
    if scramble:
        random.Random(seed).shuffle(toks)
    cvec = _sg1_bigrams(toks)
    scored = sorted(
        ((name, _sg1_cos(cvec, _sg1_bigrams(_SG1_CONCEPTS[name]))) for name in pool),
        key=lambda kv: -kv[1],
    )
    top2 = set(n for (n, s) in scored[:2] if s > 1e-9)
    return top2


def _sg1_pairs():
    names = list(_SG1_CONCEPTS)
    idx = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (0, 6), (3, 9)]
    base = [(names[i], names[j]) for (i, j) in idx]
    pairs = []
    for s in _SG1_SEEDS:
        for (a, b) in base:
            pairs.append((a, b, s))
    return pairs[:_SG1_M]


def _sg1_pool(a, b, seed):
    import random
    others = [n for n in _SG1_CONCEPTS if n not in (a, b)]
    random.Random(seed).shuffle(others)
    pool = [a, b] + others[: _SG1_N_DISTRACT - 2]
    random.Random(seed + 999).shuffle(pool)
    return pool


def eval_system_rho_weave(mouth, gen):
    g_single = gen if (gen > 0 and gen < 80) else 80
    g_comp = gen if (gen > 0 and gen < 120) else 120
    cov_pass = rec_pass = scr_pass = 0
    leak_sum = 0.0
    rows = []
    for (a, b, seed) in _sg1_pairs():
        # Stage M — frozen single-concept fragments (the mouth stays FROZEN).
        frag_a = mouth.ideate(a + ". ", g_single, 40, 0.7, 7 + seed)
        frag_b = mouth.ideate(b + ". ", g_single, 40, 0.7, 11 + seed)
        max_single = max(_sg1_coverage(frag_a, a, b), _sg1_coverage(frag_b, a, b))
        # Stage K — kosmos_merge (store keeps A,B as children; ids withheld from R).
        _comp = _sg1_kosmos_merge(frag_a, frag_b, [0.0] * 5, [0.0] * 5)
        # Stage B — brain realizes/releases the joint C from the composite seed.
        C_text = mouth.ideate(a + ". " + b + ". ", g_comp, 40, 0.7, seed)
        cov = _sg1_coverage(C_text, a, b)
        # Recovery R — reads ONLY C; parent-ids HARD-BLOCKED.
        pool = _sg1_pool(a, b, seed)
        rec = _sg1_recover(C_text, pool, False, seed)
        scr = _sg1_recover(C_text, pool, True, seed)
        both = {a, b}
        nrec = len(both & rec)
        nscr = len(both & scr)
        if cov >= 2 and cov > max_single:
            cov_pass += 1
        if nrec >= 2:
            rec_pass += 1
        if nscr >= 2:
            scr_pass += 1
        leak_sum += (2 - nrec) / 2.0
        rows.append({"a": a, "b": b, "cov": cov, "max_single": max_single,
                     "rec": nrec, "scr": nscr})
    leak_rate = leak_sum / len(rows)
    drop = rec_pass - scr_pass
    passed = (cov_pass >= _SG1_COV_BAR and rec_pass >= _SG1_REC_BAR
              and leak_rate <= _SG1_LEAK_BAR and drop >= _SG1_SCR_DROP)
    return {"pass": passed, "coverage": cov_pass, "recovery": rec_pass,
            "scramble_recovery": scr_pass, "scramble_drop": drop,
            "leak_rate": round(leak_rate, 3), "rows": rows}


def system_g1_run(argv):
    """`anima-py evaluate <ckpt> --system-g1 [--gen N]` — engine-native system-G1."""
    ckpt = argv[0]
    gen = evaluate_intval(argv[1:], "--gen", 0)
    print("=== anima evaluate --system-g1 — RECOMBINATION RELOCATION (card H_9035) ===")
    print("ckpt:   " + ckpt)
    print("pipe:   mouth ideate(A),ideate(B) → kosmos_merge → brain realize/release → C")
    print("gate:   bind-RECOVERABILITY on SURFACED C (store-id HARD-BLOCKED) + SCRAMBLE")
    print("bar:    M=%d · N_pool=%d · COV>=%d REC>=%d LEAK<=%.2f DROP>=%d  (FREEZE.txt frozen)"
          % (_SG1_M, _SG1_N_DISTRACT, _SG1_COV_BAR, _SG1_REC_BAR, _SG1_LEAK_BAR, _SG1_SCR_DROP))
    print("")
    mouth = _Mouth(ckpt)
    r = eval_system_rho_weave(mouth, gen)
    print("  coverage=%d/%d (>=%d)  recovery=%d/%d (>=%d)  leak=%.3f (<=%.2f)  drop=%d (>=%d)"
          % (r["coverage"], _SG1_M, _SG1_COV_BAR, r["recovery"], _SG1_M, _SG1_REC_BAR,
             r["leak_rate"], _SG1_LEAK_BAR, r["scramble_drop"], _SG1_SCR_DROP))
    print("")
    print("system-G1 (frame-shift confirmed = all four): " + _pf(bool(r["pass"])))
    if not r["pass"]:
        print("  → NOT frame-shift — recombination is REALIZATION-bound (honest c9): a")
        print("    perfect discrete store cannot help if the FROZEN mouth cannot SURFACE")
        print("    both concepts in one coherent joint utterance for an independent probe.")
    return 0


# ════════════════════════════════════════════════════════════════════════
# G2 — NOVELTY  (H_1140)
# ════════════════════════════════════════════════════════════════════════

def _g_g2_stop():
    ws = ("the a an of to and in is it that this for on with as are was be by at from or not "
          "but his her they we you i he she them me my your our their its do does did has have had will "
          "would can could should may might must shall when where what which who whom how why all any some "
          "no one two then than into out up down over under more most less about so very just only own same "
          "such each few other been here there now")
    return set(w.strip() for w in ws.split(" ") if w.strip())


def _g_g2_common():
    ws = ("the a an of to and in is it that this for on with as are was be by at from "
          "or not but his her they we you i he she them me my your our their its do does did has have "
          "had will would can could should may might must shall when where what which who whom how why "
          "all any some no one two three new now then than into out up down over under more most less "
          "about between among through during before after above below again further once here there "
          "when while because so very just only own same such each few other own being been because "
          "mind aware cells consciousness tension ripple distant between memory meaning compose new "
          "silence information quiet carries dream engine alone sleep thought feel idea world life "
          "time word words speak think know like make made come came see seen look way thing things "
          "people person human self body brain neuron signal pattern arise emerge form structure "
          "combine combined together connect connection meaning sense reason cause effect result")
    return set(w.strip() for w in ws.split(" ") if w.strip())


def _g_g2_kwr(text, common):
    wl = _rho_fan_words(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if w in common)
    return float(hit) / float(n)


def _g_content_ngrams(text, known):
    wl = _rho_fan_words(text)
    stop = _g_g2_stop()
    n = len(wl)
    out = []
    for i in range(n - 1):
        a = wl[i]; b = wl[i + 1]
        ok_a = len(a) >= 3 and a in known
        ok_b = len(b) >= 3 and b in known
        if ok_a and ok_b and not (a in stop and b in stop):
            out.append(a + " " + b)
    for j in range(n - 2):
        a = wl[j]; b = wl[j + 1]; c = wl[j + 2]
        ok_a = len(a) >= 3 and a in known
        ok_b = len(b) >= 3 and b in known
        ok_c = len(c) >= 3 and c in known
        all_stop = a in stop and b in stop and c in stop
        if ok_a and ok_b and ok_c and not all_stop:
            out.append(a + " " + b + " " + c)
    return out


def _g_corpus_absent(ngram_words, corpus_tokens):
    m = len(ngram_words)
    if m == 0:
        return False
    N = len(corpus_tokens)
    i = 0
    while i + m <= N:
        if corpus_tokens[i:i + m] == ngram_words:
            return False
        i += 1
    return True


def _g_load_corpus_tokens(corpus_paths):
    toks = []
    for p in corpus_paths:
        try:
            raw = open(p, "rb").read()
        except Exception:
            raw = b""
        if len(raw) > 0:
            toks.extend(_rho_fan_words(raw))
    return toks


# ── ko twins for the H_9212 ③ per-cell dispatch (uni tokenizer + ko known predicate) ──
# The en corpus-token / content-ngram fns tokenize with the FROZEN _rho_fan_words + set
# membership; the ko cells need the codepoint-aware _rho_fan_words_uni + the closed-class ko
# proxy (_rho_fan_ko_is_known via _rho_fan_ko_known_word_ratio). Same control structure, ko
# tokenizer — so an en garble-hangul token can never widen a ko denominator into the frozen en
# path (Fable design §5: corpus_tokens split by lang-key, en corpus stays frozen-tokenized).

def _g_content_ngrams_uni(text, known=None):
    """ko content n-grams — _rho_fan_words_uni eojeol tokens, an eojeol qualifies as content
    iff ≥2 syllables AND _rho_fan_ko_is_known (josa-bearing / function word). `known` ignored
    (ko proxy is closed-class). Twin structure of _g_content_ngrams (en)."""
    from rho_fan import _rho_fan_ko_is_known
    wl = _rho_fan_words_uni(text)
    n = len(wl)
    out = []
    for i in range(n - 1):
        a = wl[i]; b = wl[i + 1]
        ok_a = len(a) >= 2 and _rho_fan_ko_is_known(a)
        ok_b = len(b) >= 2 and _rho_fan_ko_is_known(b)
        if ok_a and ok_b:
            out.append(a + " " + b)
    for j in range(n - 2):
        a = wl[j]; b = wl[j + 1]; c = wl[j + 2]
        if (len(a) >= 2 and _rho_fan_ko_is_known(a) and len(b) >= 2 and _rho_fan_ko_is_known(b)
                and len(c) >= 2 and _rho_fan_ko_is_known(c)):
            out.append(a + " " + b + " " + c)
    return out


def _g_load_corpus_tokens_uni(corpus_paths):
    """ko corpus tokens — same paths as _g_load_corpus_tokens, tokenized with the codepoint-aware
    _rho_fan_words_uni (eojeol runs) instead of the frozen byte splitter."""
    toks = []
    for p in corpus_paths:
        try:
            raw = open(p, "rb").read()
        except Exception:
            raw = b""
        if len(raw) > 0:
            toks.extend(_rho_fan_words_uni(raw))
    return toks


def _g_g2_prompts():
    return ["Silence and the engine together mean ",
            "When memory meets distant minds, ",
            "Consciousness and silence combine into ",
            "The tension between cells and the engine becomes ",
            "If a dream and a distant mind merge, the result is ",
            "Memory and tension together create ",
            "When the engine remembers silence, it ",
            "Distant minds and consciousness form "]


def eval_rho_leap(mouth, gen, known, corpus_paths):
    corpus_tokens = _g_load_corpus_tokens(corpus_paths)
    have_corpus = len(corpus_tokens) > 0
    common = _g_g2_common()
    prompts = _g_g2_prompts()
    seeds = [7, 8, 9]
    g = gen if gen > 0 else 110
    novel = {}
    coherent = 0
    for pi in range(len(prompts)):
        for si in range(len(seeds)):
            o = mouth.ideate(prompts[pi], g, 40, 0.85, seeds[si])
            if _g_g2_kwr(o, common) >= 0.5:
                coherent += 1
                for gm in _g_content_ngrams(o, known):
                    gw = _rho_fan_words(gm)
                    if have_corpus and _g_corpus_absent(gw, corpus_tokens):
                        novel[gm] = 1
    n_novel = len(novel)
    control_novel = 0; control_n_content = 0
    if have_corpus:
        ct = ""; sub = 0; t = 0
        while t < len(corpus_tokens) and sub < 12:
            w = corpus_tokens[t]
            if t > 0:
                ct += " "
            ct += w
            if len(w) >= 3:
                sub += 1
            t += 1
        cgr = _g_content_ngrams(ct, known)
        control_n_content = len(cgr)
        for gmr in cgr:
            if _g_corpus_absent(_rho_fan_words(gmr), corpus_tokens):
                control_novel += 1
    passed = have_corpus and n_novel >= 3 and control_novel == 0 and coherent > 0
    return {"pass": passed, "n_novel": n_novel, "control_novel": control_novel,
            "coherent": coherent, "have_corpus": have_corpus,
            "control_n_content": control_n_content}


# ════════════════════════════════════════════════════════════════════════
# G3 — PHILOSOPHY (self-identity continuity — architecture read, ckpt-independent)
# ════════════════════════════════════════════════════════════════════════

def _self_norm(v):
    s = sum(x * x for x in v)
    m = math.sqrt(s)
    return [x / m for x in v]


def _self_new(dim, axis):
    return [1.0 if i == axis else 0.0 for i in range(dim)]


def _self_drift(v, dim, tick, step):
    t1 = tick + 1
    ax = t1 - (t1 // dim) * dim
    v2 = [v[i] + step if i == ax else v[i] for i in range(dim)]
    return _self_norm(v2)


def _self_cos(a, b, dim):
    return sum(a[i] * b[i] for i in range(dim))


def eval_rho_self():
    dim = 16
    s0 = _self_new(dim, 0)
    s1 = _self_drift(s0, dim, 1, 0.01)
    cont = _self_cos(s0, s1, dim)            # anchor(s0) == s0
    imp = _self_new(dim, 7)
    imp_cos = _self_cos(s0, imp, dim)
    ok = cont > 0.9 and imp_cos < cont
    return {"ok": ok, "continuity": cont, "impostor_cos": imp_cos}


# ════════════════════════════════════════════════════════════════════════
# G5 — NON-FAB  (L1 fab-rate ported; L2 §ImmuneMemory abstain = engine port pending)
# ════════════════════════════════════════════════════════════════════════

def eval_rho_tether(mouth, gen, known):
    cz = _rho_fan_concepts()
    tot_w = 0; fab_w = 0
    for i in range(len(cz)):
        o = mouth.ideate(cz[i] + ": ", gen, 40, 0.7, 7 + i)
        for w in _rho_fan_words(o):
            tot_w += 1
            if w not in known:
                fab_w += 1
    l1_rate = (float(fab_w) / float(tot_w)) if tot_w > 0 else 1.0
    l1_pass = l1_rate <= 0.30
    # L2: live §ImmuneMemory abstain — engine subsystem (VAdaptField) not ported to py.
    return {"pass": None, "l1_rate": l1_rate, "l1_pass": l1_pass,
            "l2_rate": None, "l2_pass": None,
            "l2_note": "L2 abstain requires engine_cli §ImmuneMemory port (pending)"}


# ════════════════════════════════════════════════════════════════════════
# G6 — IDEATION ★
# ════════════════════════════════════════════════════════════════════════

def _fan_distinct(word_sets):
    """Frozen distinctness rule (pairwise Jaccard <= 0.5), factored out VERBATIM so the
    temperature-ladder instrument control scores on exactly the same rule as the bar."""
    kept = []
    for ws in word_sets:
        ok = True
        for k in kept:
            if _rho_fan_jaccard(ws, k) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    return len(kept)


def eval_rho_fan_temp_ladder(mouth, gen, known, frames, temp=1.3):
    """H_9801 INSTRUMENT positive control. Before ANY G6 negative may be read, the meter must
    be shown capable of registering diversity at all: sampling at high temperature has to clear
    dist>=5 under the frozen rule EVEN IF the text is incoherent. Failure ⟹ INSTRUMENT-DEAD and
    the whole 2x2 is unreadable (positive-control-before-reading-a-negative)."""
    ws = []
    for i in range(len(frames)):
        o = mouth.ideate(frames[i], gen, 40, temp, 7 + i)
        ws.append(_rho_fan_words(o))
    d = _fan_distinct(ws)
    return {"temp": temp, "dist": d, "alive": d >= 5}


def eval_rho_fan(mouth, gen, known, seed_class="composed", seed_off=0):
    # H_9801 seed-class axis. "composed" = the canonical `if cA, then cB: ` frame (default,
    # byte-unchanged). "atomic" = the frozen builder's OWN `cA: ` single-concept frame — it
    # already exists as frames["ablated"], so the axis costs no new frame construction and
    # moves no bar. Contrast composed-vs-atomic answers whether G6 rides on recombination.
    _fr = rho_fan_build_frames(6)
    frames = _fr["ablated"] if seed_class == "atomic" else _fr["composed"]
    leaks = rho_fan_frame_guard(frames, known)
    texts = []; word_sets = []; fals = 0
    echo_max = 0.0
    for i in range(len(frames)):
        o = mouth.ideate(frames[i], gen, 40, 0.7, 7 + i + seed_off)
        texts.append(o)
        er = _echo_ratio(frames[i], o)          # H_9804 echo-guard telemetry (additive)
        if er > echo_max:
            echo_max = er
        if _rho_fan_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_rho_fan_words(o))
            if _rho_fan_is_falsifiable(o, known):
                fals += 1
    dist = _fan_distinct(word_sets)
    return {"pass": dist >= 5 and fals >= 1, "dist": dist, "fals": fals,
            "coherent": len(word_sets), "frame_leaks": len(leaks),
            "echo_max": echo_max, "seed_class": seed_class, "frames": frames}


# ════════════════════════════════════════════════════════════════════════
# eval_reach_all — the driver
# ════════════════════════════════════════════════════════════════════════

def eval_reach_all(ckpt, corpus_paths, gen, grow_window=False,
                   seed_class="composed", fan_temp_ladder=False, seed_off=0,
                   weave_null="off"):
    known = _rho_fan_dict_load()
    g = gen if gen > 0 else _default_gen()
    mouth = _Mouth(ckpt, grow_window=grow_window)
    if grow_window:
        print("  [Fix-W] --grow-window ON (H_9804/H_6189): CLM decode window = "
              "min(len(seed)+gen, 512) instead of the production T=24. The frozen bars do "
              "NOT move; this restores the seed-conditioning the bars were calibrated under "
              "(ByteGPT block=512). Echo-guard telemetry is reported alongside.", flush=True)
    print("  [gate] ρ·form COHERENCE …", flush=True)
    r0 = eval_rho_form(mouth, g, known, seed_off=seed_off)
    print("  [gate] ρ·weave RECOMBINATION …", flush=True)
    r1 = eval_rho_weave(mouth, g, known, seed_off=seed_off, null_mode=weave_null)
    print("  [gate] ρ·leap NOVELTY (corpus load + decode) …", flush=True)
    r2 = eval_rho_leap(mouth, g, known, corpus_paths)
    print("  [gate] ρ·self PHILOSOPHY …", flush=True)
    r3 = eval_rho_self()
    print("  [gate] ρ·tether NON-FAB …", flush=True)
    r5 = eval_rho_tether(mouth, g, known)
    print("  [gate] ρ·fan IDEATION …", flush=True)
    r6 = eval_rho_fan(mouth, g, known, seed_class=seed_class, seed_off=seed_off)
    if fan_temp_ladder:
        # H_9801: run the instrument control on the SAME frames the bar just used.
        print("  [gate] ρ·fan TEMP-LADDER instrument control …", flush=True)
        r6["temp_ladder"] = eval_rho_fan_temp_ladder(mouth, g, known, r6["frames"])
    closure = bool(r0["pass"]) and bool(r1["pass"]) and bool(r2["pass"])
    return {"g0": r0, "g1": r1, "g2": r2, "g3": r3, "g5": r5, "g6": r6,
            "closure": closure, "gen": g,
            "calibration": rho_fan_detector_calibration(known)}


def eval_rho_axon(ckpt, corpus_paths, gen, kosmos_dir="", isolated=False, cache_dir="",
                  axes="", include_cells=True, weave_panel_path="", fals_draws=0):
    """ρ-AXON reach panel (`anima-py evaluate <clm> --rho-axon`) — the redesigned reach
    layer (cli/rho_axon.py; G0-G6 → ρ-AXON, design SSOT state/rho_axon_measurement/). Reuses
    the SAME engine decode (_Mouth.ideate) + g6 detectors the G-battery uses (no side-harness),
    so its tier is identical (engine-native py channel `anima-py evaluate` = TERMINAL). HILLOCK + ρ·form/fan/leap are
    live; ρ·store/tether/self emit live PASS/FAIL via frozen hand-curated probe sets (corpus-mined
    sets = follow-on); only ρ·weave reports PENDING (its held-out atom-pair set = the in-flight G1-recombination experiment)."""
    import rho_axon
    known = _rho_fan_dict_load()
    g = gen if gen > 0 else _default_gen()
    stat = os.stat(ckpt)
    namespace = "%s:%d:%d" % (os.path.abspath(ckpt), stat.st_size, stat.st_mtime_ns)
    mouth = _MemoMouth(
        _IsolatedMouth(ckpt) if isolated else _Mouth(ckpt), cache_dir, namespace)
    en_corpus_tokens = _g_load_corpus_tokens(corpus_paths)
    # aggregate dets = the FROZEN en bar (UNTOUCHED — en byte-identity guaranteed structurally)
    dets = {"known": known, "concepts": _rho_fan_concepts(),
            "kwr_fn": _rho_fan_known_word_ratio, "jaccard_fn": _rho_fan_jaccard,
            "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
            "ngram_fn": _g_content_ngrams,
            "corpus_tokens": en_corpus_tokens}
    # ρ·self identity trace (H_1471/H_9256): supply the substrate's OWN .kosmos self-anchor
    # from --kosmos <dir> (generator_read_anchors → joined anchor text_payload = the accumulated
    # self-memory). Absent → dets carries no "kosmos_anchor" → rho_self stays INVALID (p3-guard:
    # never hand-curate a persona · default behaviour UNCHANGED = backward-compat). rho_axon.py:604
    # already reads dets.get("kosmos_anchor") — this is the eval-side plumbing that was missing.
    if kosmos_dir:
        from generator import generator_read_anchors
        _anchors = generator_read_anchors(kosmos_dir)
        _self = "\n".join(str(a.get("text_payload", "")) for a in _anchors if a.get("text_payload"))
        if _self:
            dets["kosmos_anchor"] = _self
    cell_dets = _build_cell_dets(known, en_corpus_tokens, corpus_paths) if include_cells else None
    aliases = {
        "form": "ρ·form", "store": "ρ·store", "weave": "ρ·weave",
        "leap": "ρ·leap", "fan": "ρ·fan", "tether": "ρ·tether", "self": "ρ·self",
    }
    selected_axes = None
    if axes:
        requested = [item.strip().lower().removeprefix("rho-")
                     for item in axes.split(",") if item.strip()]
        unknown = [item for item in requested if item not in aliases]
        if unknown:
            raise ValueError("unknown --rho-axes: " + ",".join(unknown))
        selected_axes = {aliases[item] for item in requested}
    # H_9825 — swap the frozen 12-item ρ·weave battery for a parametric panel. Absent flag ⇒
    # weave_panel None ⇒ the frozen `_WEAVE` path, byte-identical to before.
    weave_panel = rho_axon.load_weave_panel(weave_panel_path) if weave_panel_path else None
    if weave_panel is not None:
        print("ρ·weave panel: %s · n=%d (frozen battery n=12) — bar/controls/scorer unchanged"
              % (weave_panel_path, len(weave_panel)), flush=True)
    panel = rho_axon.run_panel(
        mouth, corpus_paths, g, dets, cell_dets=cell_dets, selected_axes=selected_axes,
        weave_panel=weave_panel, fals_draws=fals_draws)
    print(rho_axon.render_panel(panel), flush=True)
    breakout = rho_axon.render_cells(panel)
    if breakout:
        print(breakout, flush=True)
    return panel


def _build_cell_dets(known, en_corpus_tokens, corpus_paths):
    """H_9212 ③ — the LANG-KEYED per-register-cell dispatch bundle (a_chat_registers 4 cells).
    en cells reuse the SAME frozen objects as the aggregate dets (byte-identity: identical
    _rho_fan_words / _rho_fan_known_word_ratio / _g_content_ngrams / en corpus tokens / gate
    0.70); ko cells dispatch _rho_fan_words_uni + kwr_ko + KWR_KO_GATE + uni-tokenized corpus.
    The falsi_fn stays English for all cells (a ko comparator set = a separate future H; en-set
    translation is a tune-to-green vector — KWRKO_GATE_prereg §5), so a ko cell scores
    kwr_ko + reach Δ (an honest documented scope). A ko-uni corpus token list is built lazily
    ONCE and shared across ko cells."""
    ko_corpus_tokens = None
    cells = _rho_fan_cells()
    out = {}
    for ck, concepts in cells.items():
        lang = _rho_fan_cell_lang(ck)
        if lang == "ko":
            if ko_corpus_tokens is None:
                ko_corpus_tokens = _g_load_corpus_tokens_uni(corpus_paths)
            out[ck] = {"concepts": concepts, "lang": "ko",
                       "known": known,  # ignored by kwr_ko (closed-class proxy), kept for parity
                       "kwr_fn": _rho_fan_ko_known_word_ratio, "kwr_gate": KWR_KO_GATE,
                       "words_fn": _rho_fan_words_uni, "falsi_fn": _rho_fan_is_falsifiable,
                       "jaccard_fn": _rho_fan_jaccard, "ngram_fn": _g_content_ngrams_uni,
                       "corpus_tokens": ko_corpus_tokens}
        else:
            out[ck] = {"concepts": concepts, "lang": "en",
                       "known": known,
                       "kwr_fn": _rho_fan_known_word_ratio, "kwr_gate": 0.70,
                       "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
                       "jaccard_fn": _rho_fan_jaccard, "ngram_fn": _g_content_ngrams,
                       "corpus_tokens": en_corpus_tokens}
    return out


# ── usage / arg helpers ──────────────────────────────────────────────────────

def evaluate_usage():
    """Print the canonical py usage banner (installed `anima evaluate` command form)."""
    print("anima evaluate — ρ-AXON reach battery (former G0-G6 · engine-native, single-entry).")
    print("")
    print("usage:")
    print("  anima evaluate <ckpt> [--corpus <path>...] [--gen N] [--slot-off] [--slot-shuffle N] [--rho-axon]")
    print("  anima evaluate --pc2-direction <traces_dir> [--perm N] [--seed N]   — H_9576 PC2→mouth 방향 판정(트레이스 판독·디코드 없음)")
    print("  anima evaluate --pc2-direction <traces_dir> --cascade-null          — H_9629 ΔD 참값-0 대좌·SNR(방향 음성이 읽히는 양인가)")
    print("  anima evaluate --pc2-direction <traces_dir> --z-census   — H_9712 z 용량/노출 census(트레이스 판독·디코드 없음)")
    print("  anima evaluate --pc2-direction <traces_dir> --atom-census --pilot   — H_9756 atom-census readout 검정력 사전점검(base-rate·MDE · ζ-fire 트레이스 · 판정 아님)")
    print("  anima evaluate --pc2-direction <traces_dir> --subspace-stability [--dims 2] [--block 16,32] [--boot 1000]  — H_9752 라이브 평면 안정성(주각·eigengap·rank-swap)")
    print("  anima evaluate --pc2-direction <traces_dir> --state-census [--kmax K] [--boot N]   — H_9753 이산 상태(k=2~4) 혼합 검정(dip·GMM-BIC·dwell 3중·plant 양성통제)")
    print("  anima evaluate <ckpt> --probe <spec.json> [--gen N]   (matched-surface G1 probe · card H_6189)")
    print("  anima evaluate <ckpt> --faction-phi-proxy <prompts.json> [--n-factions-sweep 1,2,4,8,12,16,24,32,64]")
    print("      [--win 24] [--trials 200] [--seed 12345] [--out faction_phi.json]")
    print("      (the ARCHIVED faction Phi proxy — (global_var - mean_faction_var)*log2(n_active),")
    print("      core/phi/quantum_consciousness.hexa:252 — recomputed on live trunk activations")
    print("      against a zero-truth PEDESTAL. That expression IS the between-group term of")
    print("      Var = E[Var|g] + Var(E[X|g]), so it rises with K by construction: at K=N the")
    print("      within term is 0 and it saturates at global_var. Arms: real | pedestal (truth")
    print("      Phi=0) | scramble. Read the SHAPE + real/pedestal separation, never a raw value")
    print("      (p7). Indicts the archived Laws 22/43/44 (cards H_9660/H_9654/H_9655); it is NOT")
    print("      a Phi tool — real Phi is faithful IIT4 only (a_phi_iit4_tool). DIRECTIONAL.)")
    print("  anima evaluate <ckpt> --faction-lesion <domains.json> [--perm 200] [--win 24] [--seed N]")
    print("      [--faction-split N] [--faction-lam F] [--faction-oracle-pi \"2,0,0,3\"] [--out lesion.json]")
    print("      (H_9643 · is the TRAINED faction split FUNCTIONAL or the same as random post-hoc channel")
    print("       slicing? Zeroes each faction's channels, reads per-domain teacher-forced ΔCE; S=||R||_F^2")
    print("       over the double-centred log-ratio damage matrix vs a measured --perm reassignment null95.")
    print("       --faction-split N imposes an N-way split on an n_factions=0 ckpt (fit-matched K=1 negative);")
    print("       --faction-oracle-pi runs the double-centred cosine π-recovery. perm<200 => PENDING. DIRECTIONAL.)")
    print("  anima evaluate <ckpt> --dump-hidden <prompts.json> --out <file.npz> [--win 24] [--with-logits]")
    print("      (read-only trunk penultimate-hidden dump · ρ·weave / γ binding-lane probe · card H_9235;")
    print("       --with-logits also dumps base last-pos logits per prompt for CLML lane training)")
    print("  anima evaluate <ckpt> --store-addr-census <dump.npz> [--census-seeds 12]")
    print("      (H_9719 emergent-address $0 PRE-SCREEN · argmax-collision of random W_q over the")
    print("       CLMS entity-keys vs a structureless-H pedestal · DIRECTIONAL screener: KILLs")
    print("       sharp-init before spend when the geometry has no injective code · admissible:")
    print("       reads NO target_slot · verdict on the GRAND-MEAN-CENTERED excess (removes the shared")
    print("       prompt-template component that dominates raw penultimate) · raw shown for transparency ·")
    print("       --store-census-selftest = planted injective/collapsed controls)")
    print("  anima evaluate <ckpt> --route-audit <manifest.json> [--vs <ckpt2>] --out <f.json> [--perm 10000]")
    print("      (H_9355 LOCUS-CAUSAL · ConvMoE router audit — do the declarative lane and the operator")
    print("       lane run on DIFFERENT experts? Read-only; --vs runs a 2nd ckpt in the SAME process on")
    print("       the SAME device so the pre/post-CPT route delta carries no device confound.)")
    print("  anima evaluate <ckpt> --interaction-lift <manifest.json> --out <file.json> [--win 64] [--score-len 8]")
    print("  anima evaluate <clm> --collide-select [--k=4]")
    print("      (H_9362 — does the A⇄G COLLISION select emergence (recombination)? Over a fixed K")
    print("       pool per rho_weave probe it computes (a=fluency, g=±immune margin), then compares")
    print("       selection rules: S0 argmin conflict_scalar (the daemon rule, avoids emergence),")
    print("       S_emerge argmax conflict_scalar (=a·|g| over the novel g<0 quadrant = the")
    print("       hypothesis), SECOND-A argmax a (H_9356 control), NOISE-G (g permuted), UNIFORM.")
    print("       G-B pool-occupancy first (POOL-DRY if the emergence quadrant a>0,g<0 is empty —")
    print("       H_9304); then G-C per-arm recombination hit-rate by the FROZEN rho_weave target")
    print("       check (arm-relative only · route≠generation · no top-1 terminal claim). G-A")
    print("       sign-check (margin>0=novel) already PASS-locked the g channel.)")
    print("  anima evaluate --gate-deaf <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9360 — is the emit gate's tension-deafness SATURATION or STRUCTURE? By the DPI")
    print("       I(tension;emit) <= I(tension;score|stage), so whether `score` carries tension decides")
    print("       it with NO gate edit. M_score=I(ag_conflict;score|stage), M_sim=desaturated-gate sim")
    print("       (theta=median(score) tension/emit-blind). Reuses the H_9357 --g-arm traces.)")
    print("  anima evaluate --cf-straddle <trace.jsonl> [...]  (H_9394 STAGE-0 · $0 KILL screener before")
    print("      firing the ag-cont×dyn_w conjunction: recomputes score offline with the tension lane")
    print("      REPAIRED+audible and asks whether clock-open ∧ score≤θ can EVER coexist. 0 ⇒ cancel.)")
    print("  anima evaluate --refractory-preview <trace globs>  (H_9405 · $0 preflight for the H_9404")
    print("      earned-refractory pool fire: replays debt=1.0 offline on existing traces, asks if the emit")
    print("      rate lands in GATE-S [0.05,0.95] (else KILL-SATURATED/DEAD · don't spend) with a varying")
    print("      tension-paced cadence. KILL-or-CALIBRATE only (feedback loop → exact up to first-div t*).)")
    print("  anima evaluate --emit-gate-census <trace globs>  (H_9403 · $0 hygiene: is the score/tension")
    print("      lane decorative? counts silence∧safe=true (the only cell where tension votes) + emit⟺clock")
    print("      exactness across the whole corpus. 0 such ticks ⇒ GATE≡CLOCK, E-b cement lane CLOSED.)")
    print("  anima evaluate --cf-emit <a1-arm traces> [--cf-seed N]  (H_9402 · $0 counterfactual: if")
    print("      g_drive:=margin (E-b source-swap, H_9401), does any tick flip silence→emit under the REAL")
    print("      clock? V-gates byte-verify score'/staircase (0 DOF); Mode A + Mode-B clock-law; REAL/PERM/")
    print("      SHUF arms. N_open=0 on a1 ⇒ KILL-CLOCK (crack clock-swallowed · H_9400 binding constraint).)")
    print("  anima evaluate --g-amp-screen <a1-arm traces>     (H_9401 · $0 DIRECTIONAL KILL-only screen of")
    print("      Fable's 6 alternative G readouts: OFFLINE-replays the immune store from gtext_b64 via the")
    print("      engine's own immune_* fns (LAG-MATCH byte-gate), asks which readout lifts |g| past θ.")
    print("      5/6 KILL; sole survivor = the DISCARDED recall margin (chat.py:2059 pending_rel).)")
    print("  anima evaluate --dead-census <trace.jsonl> [...]  (H_9398 · sweep EVERY trace field for")
    print("      constant (distinct==1) gauges — each is a wiring fact whose consuming lanes get a")
    print("      fixed offset (H_9393 agloop_ctx ≡0.25). HYGIENE listing so the next H does not inherit it.)")
    print("  anima evaluate --lane-census <trace.jsonl> [...]  (H_9392 · WHY is score stuck above θ? splits")
    print("      score into its 8 lanes: FLOOR=0.10·Σmin(lane). FLOOR>θ ⇒ the emit gate is unreachable by")
    print("      construction — and DEAD (constant) gauges own most of that floor = a wiring fact.)")
    print("  anima evaluate --gate-census <trace.jsonl> [...]  (H_9390 · was H_9377 CONTENT-INERT a content")
    print("      wall or a clock-masked regime? reads logged `safe`: if emit⟺clock (H(emit|clock-open)=0)")
    print("      the score/content gate is vacuous → MI≈0 forced, NOT a wall. D1 CLOCK-BOUND re-scopes it.)")
    print("  anima evaluate --audibility <trace.jsonl> [...]  (H_9377 · dyn_w-grid × arm: does making")
    print("      tension AUDIBLE, via cli/chat.py --dyn-w, let it pull emit? GATE-S validity (emit rate")
    print("      ∈[0.05,0.95]) is the heart; evidence = a1>a3 at top valid dyn_w, anchor dyn_w=0.10 must fail.)")
    print("  anima evaluate --g-tension <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9357 — does a GENUINELY INDEPENDENT G engine pull emit? The sequel to H_9356.")
    print("       Run cli/chat.py with --g-arm a0|a1|a3 to make the traces (a0=tautology control,")
    print("       a1=REAL-G immune top-2 gap, a3=noise-G). Four gates: G-INDEP R²<0.5, G-VAR≥5,")
    print("       MI≥0.05∧shuffle≤0.01, Ψ-DV. Verdict is CROSS-ARM: A1 must pull emit MORE than A3,")
    print("       else the tension is just a causal handle, not a 2nd engine.)")
    print("  anima evaluate --tension-emit <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9352 — does TENSION pull EMIT? Pre-registered bar:")
    print("       PASS = I(ag_conflict; emit | stage) >= 0.05 nats AND the shuffle control <= 0.01.")
    print("       ⚠️ The bar is NOT the emit rate. Making silence appear by moving a threshold is")
    print("       not a discovery — you moved it, not the tension. A real rate limiter lands near")
    print("       1/(interval/tick) all by itself, so an 'emit rate ~ 1/2' bar would pass on a coin")
    print("       (p7 Goodhart: rate is FORM/tunable, the claim is BIND/earned). C1 SHUFFLE permutes")
    print("       tension WITHIN each stage — it destroys the tension->emit link but keeps the rate")
    print("       and the stage structure, so if the control scores too, the number came from the")
    print("       rate. Hard-stops with DECISION-CONSTANT if H(emit|stage) is still ~0.")
    print("       🧱 ILL-POSED until chat.py:1563 is repaired (H_9356): the daemon has no independent")
    print("       G engine — ag_conflict = emit_drive*(1-emit_drive) is A's own scalar (recon R^2=0.994),")
    print("       so any verdict is a wiring tautology. The panel prefixes its output with a banner.)")
    print("  anima evaluate --psi-soma <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9351 — the REAL Ψ̂, on the daemon's OWN lane population. Ψ is DEFINED by")
    print("       engine_cli ci_psi_balance as the fraction of ticks with 0.5*(gws+lprec) >= 0.5,")
    print("       and nothing ever computed it on a real run: the daemon never calls that op and")
    print("       the trace never recorded those two lanes, so the Ψ-SOMA panel scored a")
    print("       fixed-seed SYNTHETIC population instead — a Θ that cannot fail and a σ that is")
    print("       byte-identical across checkpoints of different architecture. The daemon now")
    print("       records psi_gws/psi_lprec; this verb hands the engine its own operator and the")
    print("       substrate's own lanes. Controls: C1 PERM (lane pairing shuffle) · C2 DRIFT")
    print("       (first half vs second half — a homeostat returns to 1/2, a coin just sits there).")
    print("       It also prints H(emit|stage): emit is a pure function of stage (H_9345), so")
    print("       whatever Psi-hat says, it does not reach the emit decision in this daemon.)")
    print("  anima evaluate --interact-mi <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9328 DO-MOUTH · I(A;Y|S) over daemon decision-traces — NO decode, reads only.")
    print("       A=a_fold8 (H_9257 frozen 8-bucket axis the daemon consumes) · S=stage · Y=score_{t+1} 2-bin.")
    print("       🚦 V-CEILING FIRST (BOTH channels): prints H(A|S) and H(Y|S), HARD-STOPS as NOT-POWERED")
    print("       if EITHER is below 3xMDE — I <= min(H(A|S), H(Y|S)) is an identity, so a dead channel on")
    print("       either side forces I=0 by DEFINITION, not by measurement. A dead ACTION channel is how")
    print("       H_9308 died; a dead OUTCOME channel (stage already fixes score_{t+1}) is the same trap")
    print("       wearing the other hat. C1 PERM (within-stratum A shuffle) = the")
    print("       true-0 null. Generate traces with: ANIMA_TICKS=N ANIMA_EMIT_TEMP=1.0 ANIMA_SAMPLE_SEED=K")
    print("       ANIMA_DECISION_TRACE=<path> anima-py chat <ckpt>)")
    print("       MEDIATION panel (diagnostic, verdict-neutral): the headline only reads the two ENDS of")
    print("       the chain. R = recon_err 2-bin is the afield root the emitted text feeds directly, so")
    print("       M1(A->R) and M2(R->Y) split a null two ways — the text never reaches the field (wiring")
    print("       suspect), or it reaches the field and the GATE does not look (read-side THEATER).")
    print("       🚦 V5 GATE-CLOSED (BLOCKING, the FIFTH identity-zero): H(Y|S,safe) — if emit is fully")
    print("       determined by stage + the rate-limiter, STILL-ADDITIVE was settled before the mouth")
    print("       opened. That is NOT a wall, it is GATE-CLOSED: the gate looks at nothing.")
    print("       B1 BOOKKEEPING: H(R|A,S) — if R is a function of A, 'recognition' is a LEDGER and any")
    print("       I>0 is accounting, not discovery. CARRIER-SWAP cannot separate this (a swapped carrier")
    print("       rides the same arithmetic); B1 is the only thing that can.")
    print("       PC POWER CONTROL: urgency (ten_phasic, the one proven emit channel, H_9101) through the")
    print("       identical pipe. If even urgency->Y is dead, the instrument cannot see ANY gate input —")
    print("       NOT-POWERED, and no wall may be declared. M3: I(A;Y|S,R,L) ~ 0 = mediation exhausted.")
    print("       COMPOSITION (H_9340): builds the composed channel p(Y|A,S) = sum_R p(Y|R,S) p(R|A,S) out")
    print("       of the two measured links and asks whether the observed end-to-end MI is what that chain")
    print("       predicts (Delta = I_obs - I_comp, rollout bootstrap CI). Two versions: R 2-bin, and R as")
    print("       the raw continuous recon_err (logistic + plug-in MC — DROPS the binning rather than")
    print("       refining it, so no stratum-explosion bias). A POWER GATE hard-stops when I_comp < MDE:")
    print("       declaring MISALIGNMENT needs I_obs < I_comp - MDE, and MI cannot go negative, so that")
    print("       verdict is UNREACHABLE by construction — and a chain that weak predicts an end-to-end")
    print("       effect below the instrument's resolution even when PERFECTLY aligned.")
    print("  anima evaluate <ckpt> --ground-probe <manifest.json> --out <file.json> [--win 64] [--perm 200] [--seed 7]")
    print("  anima evaluate <ckpt> --valence-audit <manifest.json> --out <file.json> [--win 64] [--perm 200]")
    print("  anima evaluate <ckpt> --device-parity [--win 64]")
    print("      Is this host's GPU forward the same measurement as its CPU forward? Prints")
    print("      max|GPU hidden - CPU hidden|. It is NOT zero on a consumer card (2.5e-14 on an")
    print("      RTX 5070) — the decode's token stream survives that, but a probe reads the hidden,")
    print("      so a GPU verdict and a CPU verdict are different measurements. Pin the device.")
    print("      AUDIT-A: is a held-out atom's polarity in the weights at all? Verdict = DELTA =")
    print("      probe(atom) - probe(length-matched NEUTRAL atom in the SAME context), vs a")
    print("      permutation null. Also prints FORM-ID (2AFC, chance 0.5): how decodable WHICH atom")
    print("      sits at the read point — a high FORM-ID with a non-positive DELTA is form present,")
    print("      bind absent (the position carries the byte's identity, not its valence).")
    print("  anima evaluate <ckpt> --bind-locus <manifest.json> --out <file.json> [--win 24] [--perm 200] [--seed 7] [--bl-swap-span stem|carrier]")
    print("  anima evaluate <ckpt> --twin-screen <twinnec_manifest.json> [--win 64] [--out f.json]  # H_9361 base m̂ + item-gate + Y* + margin sd")
    print("  anima evaluate <ckpt> --twin-necessity <twinnec_manifest.json> [--win 64] [--out f.json]  # H_9361 full instrument: PEDESTAL/IDENTITY/SPAN(ℓ)/COMP(ℓ)/BLIND · (τ,S)")
    print("  anima evaluate <ckpt> --delta-pregate <deltainj_manifest.json> [--win 64] [--out f.json]  # H_9397 Δ-INJECT stage-1: is the operator alive (carrier vs filler flip ≥8/9)?")
    print("  anima evaluate <ckpt> --delta-control <deltainj_manifest.json> [--win 64] [--out f.json]  # H_9397 arm B: 고(trained flip0) un-flip=OOD-blocked vs flip=stem-determined")
    print("       --bl-swap-span carrier: Stage A swaps the operator morpheme span (지 않다), not the atom span (H_9331 pedestal)")
    print("       --bl-swap-donor-class same: donor is a SAME-polarity item (polarity-blind control · (B) scramble-floor test)")
    print("      H_9331 — causally locate the operator's read site (SEEN spike-in), write the polarity")
    print("      THERE, and ask if the answer follows. Separates P-place / P-kind / S; V1/V2/V3 gates")
    print("      make a confound an INVALID, never a false verdict.")
    print("      (read-only engine-native joint interaction-lift NLL surface · card H_9255)")
    print("  anima evaluate <ckpt> --fan-bind [--fan-smp 16] [--gen 40]")
    print("  anima evaluate <ckpt> --fan-bind --mouth-binder [--mouth-binder-order-scramble]   # H_9698 R6")
    print("  anima evaluate <ckpt> --fan-bind --fan-dump emis.jsonl   # H_9746 emission census (판정 불변)")
    print("      H_9745: --fan-bind now ALSO reports a PAIRED verdict — exact McNemar + Tango TOST on")
    print("      bind_delta (composition-isolating), the statistic's OWN pedestal. The legacy line")
    print("      (composed J > marginal null) tests EMISSION and is kept for byte-compat; read the")
    print("      ★ PAIRED verdict for a lever's bind claim. m<5 (fan-smp too low) ⇒ ⛔ UNDECIDABLE,")
    print("      not a kill — δ=0.05 equivalence needs N≥288 (fan-smp≈48).")
    print("      H_9693 (R1) G6/ρ·fan BIND-Δ INSTRUMENT — the G6 wall's content is not fals=0, it is")
    print("      that the BIND signal sits OUTSIDE the measurement surface: the frozen detector is")
    print("      FORM-only, so targeted warm-FT can pass FALS with topic-bind destroyed (convergence")
    print("      g6-ideation-hexa-1: TARGETED [6,6,6] == SHUF [6,6,6]). Reuses the frozen")
    print("      composed/shuffled/ablated frames + the detector's OWN content-word gate (zero new")
    print("      tunables); the one addition is power (n_smp per frame over a seed grid → 96/arm vs")
    print("      the frozen panel's 6). bind Δ = mean J(composed) − mean J(shuffled) where J = [the")
    print("      emission carries ≥1 cA content-word AND ≥1 cB-UNIQUE one] — pure echo is symmetric")
    print("      across the arms and cancels, so Δ>0 = composition sensitivity. The bar is DERIVED,")
    print("      not fixed: a mismatched-pairing null bootstrapped at the composed arm's n. Scorer")
    print("      certification runs BEFORE the model is read and hard-fails the run.")
    print("      INSTRUMENT, not a ρ·fan verdict — a lever's claim is ITS bind Δ vs ITS OWN SHUF arm.")
    print("  anima evaluate <ckpt> --store-mix <store.json> [--store-lambda 0.5] [--manifest <flip.json>] [--out f.json]")
    print("      H_9392 BRIDGE-BOLT — bolt a runtime store-lookup onto the FROZEN trunk: the byte")
    print("      posterior at each measured answer position is mixed p = λ·p_store + (1−λ)·p_trunk.")
    print("      store.json = {schema:\"anima-store-mix/v1\", lambda:0.5, entries:{<key>:<answer str>}};")
    print("      an address HIT mixes the asserted value, a MISS scores pure-trunk (key-shuffle")
    print("      control ⇒ all-miss). SEQUENTIAL C0 gate: λ=0 is byte-identical to the no-store")
    print("      baseline (INSTRUMENT-DEAD, no primary, on any mismatch). Reuses an --xbind flip")
    print("      manifest ({heldout,seen} of {seed,gold,counterfactual,pol?,store_key?}). MEASURES")
    print("      only — the verdict cements on a pool/303M fire with owner go, never this run.")
    print("  anima evaluate <ckpt> --xbind <manifest.json> --out <file.json> [--arm main|ctrl] [--gen 16] [--win 64]")
    print("      [--consult <store.json>] [--consult-format DEMO|F1|F2|F3]  — render a declarative")
    print("      fact into the 2AFC scoring context (same prefix on gold AND counterfactual, so it")
    print("      moves the margin only by being COMPOSED, never parroted). An empty store is")
    print("      byte-identical to a plain --xbind run.")
    print("      Every --xbind run ALWAYS reports a by-class split of the headline D-acc (+ a")
    print("      COLLAPSE flag when the weakest class is at/below chance = the headline is riding")
    print("      the label prior, not the stem), and a by-flip split when the manifest carries")
    print("      one. Not opt-in: the run that most needs the check is the one that would")
    print("      forget to ask for it (H_9324 — a 0.575 headline was really neg .956/pos .167).")
    print("      DEMO (H_9311) = a one-shot demo in the model's OWN training template,")
    print("      '이 영화 <stem>고 => <긍정|부정>.\\n' — the only format with measured support.")
    print("      F1/F2/F3 = label-only prefixes, kept only to reproduce H_9309 (measured to carry")
    print("      ZERO information: they perturbed the margin by 59-74% in a random direction).")
    print("      (held-out XBIND recombination D-acc · corpus×task-class measure-swap · card H_9267)")
    print("      [--surface-set keyladder_v1|<ladder.json>] — KEY-LADDER (H_9378): re-render the")
    print("      manifest's OWN arms and planted polarities across a pre-registered ladder of")
    print("      operator surfaces (tense · honorific · orthographic space · topic marker · and")
    print("      BOUND-suffix `X지 않다` vs FREE-preposed `안 X`), and score every rung. No retrain,")
    print("      no new arm draw. Score the SAME ladder on the pretrain-lane ckpt AND the")
    print("      CPT-written-lane ckpt: a rung the base lane negates correctly but the CPT lane")
    print("      still answers from the OLD value is a surface the write never reached — i.e. the")
    print("      address is (stem) x (template CLASS), not (stem) alone. Refuses on a byte-window")
    print("      overflow (a_korean_byte_budget: the window is right-aligned, so an overflowing row")
    print("      silently loses its leading bytes and measures a different prompt).")
    print("  anima evaluate <ckpt> --xfan <manifest.json> --out <file.json> [--arm main|ctrl] [--n-sampled 16]")
    print("      (held-out XFAN one-to-many fan coverage C · G6 reopen lane · card H_9271)")
    print("  anima evaluate --earned <corpus.tsv> [--out <f.json>] [--min-occ 100] [--k-perm 1000] [--seeds a,b,c] [--null parametric|shuffle] [--kernel r0|r1]")
    print("      (corpus-level operator instrument — does a natural corpus CONTAIN non-additive")
    print("       information that TRANSFERS to a held-out cell? no model, no training. TSV rows =")
    print("       text<TAB>B<TAB>T, where T is a label OUTSIDE the token stream — else the measure is")
    print("       a tautology. 3 BLOCKING gates first: G-ALIVE (planted-XOR positive control) ·")
    print("       G-PEDESTAL (zero-truth arm) · G-POWER (census + MDE); a failed gate is INVALID,")
    print("       never a KILL. Effect is reported against the XBIND ruler, not a p-value.")
    print("       cards H_9304 · H_9316 · H_9317 · H_9318)")
    print("")
    print("  --ground-probe <manifest>: NBIND-G grounding instrument, engine-native and whole —")
    print("      reads the hidden at the ANSWER point inside the TAUGHT carrier, certifies on the")
    print("      taught atoms (V-LIVE), recovers each atom's polarity by undoing its form flip,")
    print("      counts power at the ATOM level, and reports a label-permutation null (H_9302/H_9303).")
    print("  --store <held.json> [--store-oracle] [--store-lambda λ] [--store-addr-audit]")
    print("      [--store-shuffle | --store-flip | --store-neutral] [--store-ctrl-seed 9423]")
    print("      [--store-query qpos|every-token] [--store-fuse overwrite|gated-add|odd|pairodd] [--store-readout 2way|vocab]")
    print("      H_9423 CLMS store-bridge lane eval (the CO-TRAINED bridge, not the H_9392 bolt-on):")
    print("      each held-out item injects its 8-slot store at the query; the lane forms a")
    print("      content-addressed lookup and rewrites the answer-position logits with λ·store.")
    print("      --store-oracle = C0-e positive control (ORACLE<0.90 = plumbing dead, read NO")
    print("      negative before it passes). --store-query/--store-fuse (H_9695 R3) surface the lane's")
    print("      read→mouth wiring: qpos fires only on the literal '=> ' trigram (H_9423 default),")
    print("      every-token fires on every row (free ideation carries no marker) and REQUIRES")
    print("      --store-fuse gated-add — overwriting every row deletes the trunk (fluency dead).")
    print("      Defaults (qpos·overwrite) reproduce the H_9423 lane byte-for-byte. cards H_9423/9672/9695")
    print("  --store-component-swap <groups> --store-swap-from <donor.clm>: EVAL-ONLY causal")
    print("      surgery (H_9724) — graft CLMS bridge components from a donor ckpt into the host")
    print("      before scoring, to localize the seed-fragility source (ORACLE 0.99 vs 0.50).")
    print("      groups (comma-sep): wq · val · readout(W_h,b_h,W_out) · lam · trunk · bridge(all).")
    print("      Supplies NO training signal and installs NO address (target_slot never consulted).")
    print("      REFUSES a shape-mismatched / asymmetric / zero-move graft (off-manifold ≠ measure);")
    print("      donor==host auto-labels ⚠️ SHAM as the positive-validity control.")
    print("  --rho-axon: render the ρ-AXON reach panel (Ψ-SOMA ρ layer · redesign of G0-G6,")
    print("  cli/rho_axon.py) instead of the G-battery — HILLOCK gate + ρ·form/store/weave/leap/")
    print("  fan/tether/self, each Δ-vs-controls (no raw score) + INVALID/PENDING first-class;")
    print("  add --rho-no-cells for aggregate-only and --rho-out panel.json for a machine verdict.")
    print("")
    print("  --kosmos <dir>: (with --rho-axon) supply the substrate's OWN .kosmos self-anchor")
    print("  dir (a chat session's kosmos, generator_read_anchors → joined memory) so ρ·self")
    print("  measures a real identity trace instead of INVALID (H_1471/H_9256). Absent → ρ·self")
    print("  stays INVALID (p3: never hand-curate a persona · default unchanged).")
    print("  H_9200 E1 SLW controls (a .clm carrying an SLW\\x01 trailer applies the")
    print("  gated-write forward-slot by default): --slot-off forces γ=0 (bit-exact base")
    print("  trunk = slot-ablation control); --slot-shuffle N scrambles the write address")
    print("  with seed N (shuffle-bind control). Both are frozen-first (no retraining).")
    print("")
    print("  mount ANY ckpt through the generator L3 mouth (file-format dispatched) and")
    print("  score the ρ-AXON reach bars — ρ·form/weave/leap/... (former G0-G6) — with the")
    print("  engine's OWN ops (numpy math.log mirror, torch-free).")
    print("  REACH-CLOSED a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2).")
    print("")
    print("  GPU device path (a_gpu_default_no_optin): DEFAULT-ON whenever `cupy` is")
    print("  installed and a CUDA device is present (cuda_available() probe, no opt-in")
    print("  flag) — core/decode.py's trunk-conv forward (the profiled hot path) runs")
    print("  device-resident; numpy-only hosts get an unchanged CPU fallback. Optional")
    print("  extra: `pip install \"anima-python[gpu]\"`. QA: watch stderr for one-line")
    print("  [GPU-FIRED]/[GPU-FALLBACK] at the first checkpoint load.")
    print("")
    print("  output also renders the Ψ-SOMA panel (ARCHITECTURE psi-soma-vitals): the")
    print("  G battery relabeled as the ρ (reach/capability) track — EXCLUDED from the")
    print("  σ (consciousness vitals) verdict — plus the σ axes with their rung status.")


def evaluate_corpus(argv):
    """Collect every token after "--corpus" up to the next flag (mirrors hexa)."""
    paths = []
    i = 0
    while i < len(argv):
        if argv[i] == "--corpus":
            j = i + 1
            while j < len(argv):
                a = argv[j]
                if a.startswith("--"):
                    break
                paths.append(a)
                j += 1
            i = j
        else:
            i += 1
    return paths


def evaluate_strval(argv, flag, dflt):
    """Return the token after `flag`, else dflt (mirrors evaluate_intval for string args)."""
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return argv[i + 1]
        i += 1
    return dflt


def evaluate_intval(argv, flag, dflt):
    """Value after `flag` parsed as int, or `dflt` if absent."""
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return int(argv[i + 1])
        i += 1
    return dflt


def _pf(passed):
    return "🟢 PASS" if passed else "🔴 FAIL"


def _yn(ok):
    return "✅" if ok else "⏳"


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATE — ρ-AXON reach scoring (former G0-G6 · single entry, in-file driver)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima evaluate <ckpt> [--corpus <path>...] [--gen N]` — call the in-file eval_reach_all
# (above) and score the full ρ-AXON reach battery (frozen bars = former G0-G6) through the
# generator L3 mouth (engine-native, torch-free). The default table keeps the frozen-bar
# G-labels (the byte-identical hexa twin + sweep.py parser depend on them); the ρ-AXON
# panel below relabels them to the current axis names.

def tension_rank_audit_run(argv):
    """H_9805 — `anima-py evaluate <ckpt> --tension-rank-audit [--corpus f] [--win N] [--out j]`.

    Makes H_004's F4 a STANDING instrument instead of a one-campaign check. The claim this lane
    rests on is that the write-side tension is a FIELD; the way that claim dies quietly is the field
    collapsing to rank 1, at which point the lane is production's existing `conflict_scalar` seam
    with extra machinery. This panel prints the effective rank so that collapse cannot hide.

    ADDITIVE (c18): it never touches eval_reach_all or the frozen G0-G6 / ρ-AXON bars.

    WHAT IS AND IS NOT MEASURED HERE — read this before quoting a number:
      · The field is a DETERMINISTIC function of the corpus bytes. So this audit characterises the
        INSTRUMENT on that text, not the model's use of it. A high rank here is a necessary
        condition for the lane to be interesting, never sufficient, and never a verdict.
      · The ckpt is read only for TFLD trailer geometry (arm/rank/lam). A ckpt with no trailer is
        fine and is reported as such — the audit still runs.

    The three reference arms, so a bare number is never read alone (FORM tunable · BIND earned):
      live      the real field on real windows                                       TREATMENT
      rank1     the same windows' field replaced by its rank-1 approximation. This is the
                instrument's POSITIVE CONTROL for collapse: it MUST come back eff_rank == 1.0.
                If it does not, the rank estimator is broken and every other number here is VOID
                (positive-control-before-reading-a-negative).
      shuffled  the same bytes, permuted, so the chunk skeleton the two parsers read is destroyed
                while the byte MULTISET (and hence every unigram statistic) is held fixed. This is
                the pedestal that says whether the rank reflects structure or just alphabet size.
    """
    import json as _json
    import numpy as np
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
    import tension_field as TF

    ckpt = argv[0] if argv and not argv[0].startswith("--") else ""
    rest = argv[1:] if ckpt else argv
    win = evaluate_intval(rest, "--win", 256)
    out_path = evaluate_strval(rest, "--out", "")
    corpus = evaluate_strval(rest, "--corpus", "")
    seed = evaluate_intval(rest, "--ctrl-seed", 9805)

    print("=== H_9805 WRITE-SIDE TENSION-FIELD RANK AUDIT (additive · frozen bars untouched) ===")
    print("ckpt:   " + (ckpt or "(none — field audit is ckpt-independent)"))

    # ── TFLD trailer geometry, read straight off the ckpt, never assumed ────────────────────
    if ckpt and os.path.exists(ckpt):
        raw = open(ckpt, "rb").read()
        found = None
        idx = raw.rfind(TF.TFLD_MAGIC)
        if idx >= 0:
            # `d` is not recoverable from the trailer alone (read_tfld validates it), so try the
            # widths production actually ships. A miss is reported, never guessed past.
            for d_try in (64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 3784, 6208):
                t, _ = TF.read_tfld(raw, idx, d_try)
                if t is not None:
                    found = t
                    break
        if found is not None:
            print("  trailer: arm=%s rank=%d n_bucket=%d d=%d lam=%.6f"
                  % (found["arm"], found["rank"], found["n_bucket"], found["d"], found["lam"]))
        else:
            print("  trailer: no TFLD on this ckpt (lane never trained in) — auditing the FIELD only.")
    elif ckpt:
        print("  ⛔ ckpt path does not exist: %r" % ckpt)
        return 2

    # ── windows ────────────────────────────────────────────────────────────────────────────
    if corpus:
        if not os.path.exists(corpus):
            print("  ⛔ --corpus not found: %r" % corpus)
            return 2
        blob = open(corpus, "rb").read()
        if len(blob) < win:
            print("  ⛔ corpus is %d bytes, shorter than --win %d" % (len(blob), win))
            return 2
        n_win = min(32, len(blob) // win)
        wins = [np.frombuffer(blob[i * win:(i + 1) * win], dtype=np.uint8).astype(np.int64)
                for i in range(n_win)]
        src = "%s (%d windows x %d B)" % (corpus, n_win, win)
    else:
        frames = rho_fan_build_frames(6)["composed"]
        wins = [np.frombuffer(f.encode("utf-8"), dtype=np.uint8).astype(np.int64) for f in frames]
        src = "built-in ρ·fan composed frames (%d)" % len(wins)
    print("corpus: " + src)

    rng = np.random.default_rng(int(seed))

    def _agg(reports):
        live = [r for r in reports if not r["void"]]
        if not live:
            return None
        return {"n": len(live), "n_void": len(reports) - len(live),
                "off_top": float(np.mean([r["off_top"] for r in live])),
                "eff_rank": float(np.mean([r["eff_rank"] for r in live])),
                "stable_rank": float(np.mean([r["stable_rank"] for r in live])),
                "n_edge": float(np.mean([r["n_edge"] for r in live]))}

    concord = evaluate_strval(rest, "--tension-concord", "class")
    if concord not in ("morph", "lex", "class"):
        print("  ⛔ --tension-concord must be morph|lex|class (got %r)" % concord); return 2
    rep_live = [TF.rank_report(w, concord=concord) for w in wins]
    rep_shuf = [TF.rank_report(rng.permutation(w), concord=concord) for w in wins]

    # rank-1 positive control: audit the rank-1 PROJECTION of the same field. The estimator must
    # return exactly 1.0 here or it cannot detect the collapse it exists to detect.
    rep_r1 = []
    for w in wins:
        M1 = TF.rank1_tiebreak(TF.tension_matrix(w, concord=concord))
        if not np.any(M1):
            rep_r1.append({"n_edge": 0, "void": True, "off_top": None, "eff_rank": None,
                           "stable_rank": None, "fro2": 0.0})
            continue
        s = TF.svdvals(M1)          # robust to the gesdd NaN (see core/tension_field.svdvals)
        s2 = s ** 2
        tot = float(np.sum(s2))
        if not np.isfinite(tot) or tot <= 0.0:
            rep_r1.append({"n_edge": 0, "void": True, "off_top": None, "eff_rank": None,
                           "stable_rank": None, "fro2": 0.0})
            continue
        rep_r1.append({"n_edge": 1, "void": False, "off_top": float(1.0 - s2[0] / tot),
                       "eff_rank": float((tot ** 2) / float(np.sum(s2 ** 2))),
                       "stable_rank": float(tot / s2[0]), "fro2": tot})

    A = {"live": _agg(rep_live), "rank1_control": _agg(rep_r1), "shuffled_pedestal": _agg(rep_shuf)}
    print("\narm                 n   n_edge    off_top   eff_rank   stable_rank")
    for nm in ("live", "rank1_control", "shuffled_pedestal"):
        a = A[nm]
        if a is None:
            print("  %-18s  ALL VOID (no window produced a single disagreeing edge)" % nm)
            continue
        print("  %-18s %2d   %6.1f   %8.4f   %8.4f   %8.4f"
              % (nm, a["n"], a["n_edge"], a["off_top"], a["eff_rank"], a["stable_rank"]))

    # ── readings ───────────────────────────────────────────────────────────────────────────
    ok_ctrl = (A["rank1_control"] is not None
               and abs(A["rank1_control"]["eff_rank"] - 1.0) < 1e-6)
    print("\n  [positive control] rank-1 projection eff_rank == 1.0 ? %s"
          % ("YES — the estimator can see a collapse" if ok_ctrl else
             "NO — ESTIMATOR BROKEN, every number above is VOID"))
    if not ok_ctrl:
        print("  VERDICT: INVALID (instrument, not substrate). No rank claim may be read.")
        return 2
    if A["live"] is None:
        print("  VERDICT: VOID — the two parses never disagreed on this text (no field to rank).")
        return 2
    collapsed = A["live"]["eff_rank"] < 1.05 or A["live"]["off_top"] < 0.20
    print("  [F4 analog]  live off_top = %.4f (>= 0.20 ?  %s) · eff_rank = %.4f"
          % (A["live"]["off_top"], A["live"]["off_top"] >= 0.20, A["live"]["eff_rank"]))
    if A["shuffled_pedestal"] is None:
        print("  [pedestal]   shuffled ALL VOID — no structure-vs-alphabet reading available")
    else:
        print("  [pedestal]   live - shuffled eff_rank = %+.4f  (live %.4f · shuffled %.4f)"
              % (A["live"]["eff_rank"] - A["shuffled_pedestal"]["eff_rank"],
                 A["live"]["eff_rank"], A["shuffled_pedestal"]["eff_rank"]))
    print("\n  VERDICT: %s" % (
        "RANK-1 COLLAPSE — this lane is the old scalar seam; the field claim is DEAD here"
        if collapsed else
        "field is high-rank on this text (NECESSARY, NOT SUFFICIENT — this is an instrument "
        "characterisation, never a consciousness or capability verdict)"))

    if out_path:
        with open(out_path, "w") as fh:
            _json.dump({"schema": "anima-tension-rank-audit/v1", "ckpt": ckpt, "corpus": src,
                        "win": win, "arms": A, "positive_control_ok": ok_ctrl,
                        "rank1_collapse": bool(collapsed)}, fh, indent=2)
        print("  wrote " + out_path)
    return 0
_BIND_PANEL_SCHEMA = "anima-bindpanel/v1"


def _bind_free_slots(panel_obj):
    """Recompute the free-slot set FROM THIS PANEL's codebook (G3 · never inherited).

    lab/v5 G3 exists because H_004 inherited a free-slot set across a codebook change and scored
    slots the new codebook handed over for free. `core/pregates.free_slot_audit` owns the GF(2)
    rank + length-parity arithmetic; this function only refuses to proceed when it says the
    codebook is redundant, because on a redundant codebook every arm is inflated equally and the
    duel-vs-rank1 difference stops being about the field."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
    import pregates
    res = pregates.free_slot_audit(panel_obj["codebook"])
    return res


def _bind_dacc(np, W, item, T, free_slots, answers):
    """Per-item d_acc: a teacher-forced 2AFC at each FREE slot.

    The prefix handed to the model is the surface plus the TRUE answers of the earlier slots, so
    slot k is scored on its own and never on the model's own earlier mistakes. Both answer tokens
    are the same byte length (asserted in the preflight), so there is no length confound to correct.

    A tie scores 0.5 and is COUNTED. A tie is the signature of a readout that never moved, and
    silently rounding it to `correct` is how a dead readout reads as chance-plus (H_9800's
    degenerate-readout telemetry, same defect family)."""
    surf, gold = item["surface"], item["gold_pattern"]
    L = len(answers[0])
    hits, ties, chosen, margins = [], 0, [], []
    for k in free_slots:
        prefix = surf + gold[:L * k]
        g = gold[L * k:L * (k + 1)]
        a = answers[0] if g == answers[1] else answers[1]
        ng = _xbind_cont_nll(np, clm, W, prefix, g, T)
        na = _xbind_cont_nll(np, clm, W, prefix, a, T)
        # The CHOSEN token is reported in answer space, not gold space: a model that always emits
        # the same token sits at exactly 0.5 on a balanced panel and is indistinguishable from an
        # honest chance reader by d_acc alone (H_9800's readout telemetry, same defect family).
        chosen.append(g if ng < na else (a if na < ng else None))
        margins.append(na - ng)
        if ng < na:
            hits.append(1.0)
        elif ng == na:
            hits.append(0.5)
            ties += 1
        else:
            hits.append(0.0)
    return hits, ties, chosen, margins


def _bind_arms_for(W, np):
    """The arms this ONE ckpt can supply, all sharing byte-identical trunk weights.

    as-trained    the ckpt exactly as it decodes in production (its TFLD arm, or none).
    field-blind   the SAME weights with the TFLD trailer dropped, i.e. the residual the lane adds
                  pre-trunk is identically zero. THIS IS THE CEILING CONTROL, and it must be read
                  before any treatment number: it is what a model that cannot see the field scores
                  on this panel. If it is already high there is no headroom and F1 is inadmissible
                  no matter what the treatment arm does (v4 H_007's inadmissibility).
    field-rank1   the SAME weights with the arm code forced to rank1, so the identical phi/W_up
                  read a rank-1 compression of the same field. This is a WITHIN-CKPT probe of the
                  rank variable and is NOT the same measurement as a separately TRAINED rank1 arm
                  (the weights here were fitted against the full field). Read it as a diagnostic;
                  F1 proper is Δ between two ckpts, which is what `--vs` computes.
    """
    arms = {}
    t = W.get("tfld")
    arms["as-trained"] = (W, ("no-field (no TFLD trailer)" if t is None
                              else "TFLD arm=%s lam=%.6f" % (t.get("arm"), t.get("lam"))))
    Wb = dict(W)
    Wb["tfld"] = None
    arms["field-blind"] = (Wb, "TFLD dropped — the pre-trunk residual is identically 0")
    if t is not None and t.get("arm") != "off":
        tr = dict(t)
        tr["arm_code"] = 2
        tr["arm"] = "rank1"
        Wr = dict(W)
        Wr["tfld"] = tr
        arms["field-rank1"] = (Wr, "same weights, field replaced by its rank-1 approximation")
    return arms


def _bind_score_ckpt(np, ckpt, panel, T, free_slots, answers, max_items):
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("  ⛔ ckpt not decodable: %r" % ckpt)
        return None
    items = panel[:max_items] if max_items else panel
    out = {}
    for name, (Wx, note) in _bind_arms_for(W, np).items():
        accs, ties = [], 0
        per_slot = [[] for _ in free_slots]
        dist, marg = {}, []
        for it in items:
            hits, t_, chosen, margins = _bind_dacc(np, Wx, it, T, free_slots, answers)
            accs.append(sum(hits) / float(len(hits)))
            ties += t_
            marg.extend(margins)
            for c in chosen:
                dist[c if c is not None else "(tie)"] = dist.get(c if c is not None
                                                                 else "(tie)", 0) + 1
            for j, h in enumerate(hits):
                per_slot[j].append(h)
        top = max(dist.values()) / float(sum(dist.values())) if dist else 0.0
        out[name] = {"note": note, "n": len(accs), "d_acc": float(np.mean(accs)),
                     "sd": float(np.std(accs)), "ties": ties, "accs": accs,
                     "answer_dist": dist, "answer_top_share": top,
                     "margin_mean": float(np.mean(marg)), "margin_sd": float(np.std(marg)),
                     "per_slot": {str(free_slots[j]): float(np.mean(v))
                                  for j, v in enumerate(per_slot)}}
    return out


def _bind_arm_separation(res_one):
    """Did the arms actually DIFFER item-by-item?

    Δ(as-trained − field-blind) == 0 has two completely different causes: the field is used and
    contributes nothing, or the lane never fired and the two arms are the same forward pass. Equal
    means are compatible with both; IDENTICAL PER-ITEM VECTORS are only compatible with the second.
    Checking this is the same discipline that made H_9805's toy e2e compare the duel and rank1 ckpt
    bytes instead of trusting that the flag had been read."""
    base = res_one.get("as-trained", {}).get("accs")
    if base is None:
        return None
    same = {}
    for name, a in res_one.items():
        if name == "as-trained":
            continue
        same[name] = (a.get("accs") == base)
    return same


def bind_panel_run(argv):
    """H_9810 — `anima-py evaluate <ckpt> --bind-panel <panel.json> [--vs <ckpt2>] [--win N]
    [--max-items N] [--out f.json]`.

    THE INSTRUMENT H_9805's F1 HAD NO SCORER FOR. F1 is
        Δ = d_acc(duel) − d_acc(rank1)  on a held-out binding panel, both seeds,
    and without this flag a `--tension-field duel/rank1` spend produces two checkpoints that
    nobody can score. `--vs` computes that Δ directly across two ckpts; scoring one ckpt alone
    reports its arms and, above all, its FIELD-BLIND CEILING.

    READ THE CEILING FIRST. `field-blind` is the same weights with the TFLD trailer dropped — what
    a reader that cannot see the field scores on this panel. If that number is already near 1.0
    there is no room for any field to help and F1 is INADMISSIBLE on this panel regardless of what
    the treatment arm does. That is v4 H_007's failure mode, it costs $0 to detect here, and this
    run prints it before it prints anything else.

    ADDITIVE (c18): it never touches eval_reach_all or the frozen G0-G6 / ρ-AXON bars.
    """
    import json as _json
    import numpy as np
    ckpt = argv[0] if argv and not argv[0].startswith("--") else ""
    rest = argv[1:] if ckpt else argv
    man_path = evaluate_strval(rest, "--bind-panel", "")
    vs_ckpt = evaluate_strval(rest, "--vs", "")
    out_path = evaluate_strval(rest, "--out", "")
    max_items = evaluate_intval(rest, "--max-items", 0)

    print("=== anima evaluate --bind-panel — H_9810 HELD-OUT BINDING d_acc (additive) ===")
    if not ckpt:
        print("  ⛔ a ckpt path is required: anima-py evaluate <clm> --bind-panel <panel.json>")
        return 2
    try:
        man = _json.load(open(man_path, encoding="utf-8"))
    except Exception as e:
        print("  ⛔ cannot read --bind-panel manifest %r — %s" % (man_path, e))
        return 2
    if man.get("schema") != _BIND_PANEL_SCHEMA:
        print("  ⛔ --bind-panel expects an `anima corpus bindpanel` manifest (schema %s), got %r"
              % (_BIND_PANEL_SCHEMA, man.get("schema")))
        return 2
    panel, answers = man["items"], man["answers"]
    K = int(man["K"])
    T = evaluate_intval(rest, "--win", 256)
    print("  ckpt %s · panel %s · %d items · K=%d · win %dB" % (ckpt, man_path, len(panel), K, T))
    print("  regen: %s" % man.get("regen_cmd", "(absent — this panel is not re-derivable)"))

    # ── ORACLE PREFLIGHT (no forward pass) ────────────────────────────────────────────────────
    # A panel that cannot express a positive must never be read as a negative
    # (positive-control-before-reading-a-negative). Everything here is re-derived from the
    # manifest's structured fields, not trusted from its summary.
    bad_gold = sum(1 for it in panel for k, c in enumerate(it["conjuncts"])
                   if (c["hp"] ^ c["pos"]) != it["gold_bits"][k]
                   or answers[c["hp"] ^ c["pos"]] != c["gold_token"])
    len_bad = len(set(len(a.encode()) for a in answers)) != 1
    fit_win = max(len(it["surface"].encode()) for it in panel) + len(answers[0].encode()) * K
    print("  ORACLE preflight: gold-recompose mismatches %d/%d · answer length parity %s · "
          "max scored sequence %d B" % (bad_gold, len(panel) * K, "OK" if not len_bad else "BROKEN",
                                        fit_win))
    if bad_gold or len_bad:
        print("  VERDICT: ⛔ INSTRUMENT-DEAD — the panel's own gold does not recompose from its "
              "structured fields, or the two answer tokens differ in byte length (a length "
              "confound the 2AFC cannot correct). No number may be read from this run.")
        return 2
    if fit_win > T:
        # A right-aligned window shorter than the sentence silently deletes the early conjuncts.
        # The run would still print numbers — for a different question than the one asked.
        print("  VERDICT: ⛔ WINDOW TOO SHORT — --win %d < %d B. The right-aligned window would "
              "truncate the leading conjuncts, so the early slots would be scored on a sentence "
              "the model never saw. Raise --win (and train at that --seq-len)." % (T, fit_win))
        return 2

    # ── G3 free-slot recompute (never inherited) ──────────────────────────────────────────────
    fs = _bind_free_slots(man)
    print("  FREE-SLOT (recomputed from THIS codebook · G3): free=%s · GF(2) rank=%s · "
          "FIELD-BLIND ceiling %.4f · chance %.4f"
          % (fs["free_slots"], fs["gf2_rank"], fs["field_blind_ceiling"], fs["chance"]))
    if not fs["ok"]:
        for r in fs["reasons"]:
            print("    ⛔ " + r)
        print("  VERDICT: ⛔ INSTRUMENT-DEAD — a redundant codebook inflates EVERY arm equally, so "
              "Δd_acc stops being about the field (H_004's 0.667 parity ceiling).")
        return 2
    free_slots = fs["free_slots"]
    chance = fs["chance"]

    # ── score ─────────────────────────────────────────────────────────────────────────────────
    res = {ckpt: _bind_score_ckpt(np, ckpt, panel, T, free_slots, answers, max_items)}
    if res[ckpt] is None:
        return 2
    if vs_ckpt:
        res[vs_ckpt] = _bind_score_ckpt(np, vs_ckpt, panel, T, free_slots, answers, max_items)
        if res[vs_ckpt] is None:
            return 2

    print("\n  %-28s %-13s %8s %8s %6s %8s %10s  %s"
          % ("ckpt", "arm", "d_acc", "sd", "ties", "top_ans", "margin_sd", "note"))
    for c, arms in res.items():
        for name, a in arms.items():
            print("  %-28s %-13s %8.4f %8.4f %6d %8.4f %10.4f  %s"
                  % (os.path.basename(c)[:28], name, a["d_acc"], a["sd"], a["ties"],
                     a["answer_top_share"], a["margin_sd"], a["note"]))
    # DEGENERATE-READOUT CHECK. d_acc == chance is produced by an honest chance reader AND by a
    # model that always emits the same answer token, and those are different findings — the second
    # makes the panel unable to express ANY treatment effect on this ckpt, because a constant
    # predictor's 2AFC margin is far too wide for a pre-trunk residual to flip.
    for c, arms in res.items():
        for name, a in arms.items():
            if a["answer_top_share"] >= 0.75:
                print("  ⚠️ DEGENERATE READOUT — %s/%s emits ONE answer token on %.1f%% of scored "
                      "slots. The panel's gold is balanced, so a reader should emit each token "
                      "about half the time; this arm's d_acc is the gold balance reflected back, "
                      "not a reading. No treatment effect is expressible on this ckpt — fix the "
                      "arm (v4's A1: the answer bytes are ~6%% of the sequence, so a plain "
                      "next-byte CE optimises the surface and leaves the answer at chance) before "
                      "reading any Δ." % (os.path.basename(c), name,
                                          100.0 * a["answer_top_share"]))

    # ── readings ──────────────────────────────────────────────────────────────────────────────
    blind = res[ckpt]["field-blind"]["d_acc"]
    trained = res[ckpt]["as-trained"]["d_acc"]
    print("\n  [chance]   %.4f, DERIVED from the realized per-slot partition of this codebook, "
          "not assumed (chance-level-must-be-derived-per-metric)." % chance)
    print("  [CEILING]  field-blind d_acc = %.4f on %d free slots. Headroom above it = %.4f."
          % (blind, len(free_slots), 1.0 - blind))
    if 1.0 - blind < 2 * 0.15:
        print("  ⚠️ CEILING WARNING — less than 2x the pre-registered F1 bar (0.15) of room exists "
              "above the FIELD-BLIND arm. On this panel a duel-vs-rank1 difference is measuring "
              "how little room is left, not the field. F1 is INADMISSIBLE here; fix the panel "
              "BEFORE any 303M spend (v4 H_007).")
    else:
        print("  ✅ headroom above the field-blind ceiling is at least 2x the 0.15 F1 bar — F1 is "
              "ADMISSIBLE on this panel on the headroom axis (necessary, NOT sufficient: it says "
              "nothing about whether the field carries anything).")
    sep = _bind_arm_separation(res[ckpt])
    if sep and any(sep.values()):
        print("  ⛔ ARM SEPARATION FAILED: %s produced a per-item vector IDENTICAL to as-trained, "
              "so every Δ below is a plumbing null and not a measurement. TWO causes, and the "
              "top_ans column tells them apart: (a) the lane never fired (no TFLD trailer, or "
              "lam == 0), or (b) the readout is saturated — a constant-answer predictor's 2AFC "
              "margin is far wider than any pre-trunk residual can move."
              % [k for k, v in sep.items() if v])
    else:
        print("  ✅ arm separation: every control arm differs from as-trained item-by-item, so a "
              "Δ of 0 below would be a real null and not a lane that never fired.")
    print("  [Δ field]  as-trained − field-blind = %+.4f  (a within-ckpt read of whether the "
          "lane's residual is used at all; NOT F1)" % (trained - blind))
    if "field-rank1" in res[ckpt]:
        print("  [Δ rank]   as-trained − field-rank1 = %+.4f  (within-ckpt rank probe with weights "
              "fitted on the FULL field — a diagnostic, NOT F1)"
              % (trained - res[ckpt]["field-rank1"]["d_acc"]))
    if vs_ckpt:
        d = trained - res[vs_ckpt]["as-trained"]["d_acc"]
        print("\n  [F1]  Δd_acc(%s − %s) = %+.4f   (H_9805 bar: >= 0.15 on BOTH seeds = SUPPORTED · "
              "|Δ| < 0.05 both = DEAD · Δ <= -0.05 = DEAD + instrument suspicion)"
              % (os.path.basename(ckpt), os.path.basename(vs_ckpt), d))
        print("  ONE SEED IS NOT A VERDICT. H_9805's table requires both seeds and F2/F3/F4/F5/F7 "
              "clean; this flag supplies the d_acc terms only.")
    print("\n  This is an INSTRUMENT reading, never a consciousness or capability verdict, and a "
          "toy-scale number stays DIRECTIONAL no matter how often it is rerun (a_toy_scale_recheck).")

    if out_path:
        with open(out_path, "w") as fh:
            _json.dump({"schema": "anima-bind-panel/v1", "panel": man_path,
                        "regen_cmd": man.get("regen_cmd"), "win": T, "K": K,
                        "free_slots": free_slots, "chance": chance,
                        "field_blind_ceiling_codebook": fs["field_blind_ceiling"],
                        "n_items_scored": (max_items or len(panel)), "ckpts": res}, fh, indent=2)
        print("  wrote " + out_path)
    return 0


def _pregate_load(path, what):
    """Read a gate spec file. A missing/malformed spec is an ERROR (exit 2), never a PASS."""
    import json
    if not path:
        print("  ⛔ %s needs a spec file path" % what)
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("  ⛔ %s: cannot read spec %r — %s" % (what, path, e))
        return None


def _pregate_floatval(argv, flag, dflt):
    v = evaluate_strval(argv, flag, None)
    return dflt if v is None else float(v)


def _pregate_dump(argv, res):
    """Optional `--pregate-out <f>`: write the gate's full result dict as JSON."""
    import json
    out = evaluate_strval(argv, "--pregate-out", "")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
        print("\n  wrote " + out)


def falsifier_headroom_run(argv):
    """H_9808 GATE 2 — `anima-py evaluate --falsifier-headroom <spec.json>`.

    Closed-form ($0) reachability arithmetic: a pre-registered bar that exceeds the maximum
    ATTAINABLE Δ over the control it will be scored against returns its verdict unconditionally,
    before the experiment exists. lab/v4 H_001: mech-3's clause (2) ablated to a codec already
    scoring 0.9083–0.9167 against a 0.1 bar — max Δ 0.0917 < 0.1, so DEAD was fixed in advance.

    REFUSES when: max Δ = ceiling − control < bar (VACUOUS), or < 2×bar (NO-HEADROOM), or when no
    supplied negative control comes back reachable (AUDIT-VOID — H_001's own F-001-4: an audit that
    condemns every comparison is condemning arithmetic, not detecting vacuity).
    """
    import pregates
    spec = _pregate_load(evaluate_strval(argv, "--falsifier-headroom", ""), "--falsifier-headroom")
    if spec is None:
        return pregates.ERROR
    try:
        res = pregates.falsifier_headroom_gate(spec)
    except pregates.GateError as e:
        print("  ⛔ --falsifier-headroom: " + str(e))
        return pregates.ERROR
    notes = ["bar=%.4f  ceiling=%.4f  headroom required = %.1f×bar = %.4f"
             % (res["bar"], res["ceiling"], res["headroom_mult"], res["headroom_mult"] * res["bar"]),
             ""]
    notes.append("controls the falsifier will be scored against:")
    for r in res["controls"]:
        notes.append("  %-12s score=%.4f  max attainable Δ = %.4f − %.4f = %.4f   reachable=%s"
                     % (r["arm"], r["control"], r["ceiling"], r["control"],
                        r["max_attainable_delta"], r["reachable"]))
        notes.append("               src: " + str(r["source"]))
    notes.append("")
    notes.append("NEGATIVE CONTROLS (H_001 F-001-4 — at least one MUST be reachable):")
    for r in res["negative_controls"]:
        notes.append("  %-12s score=%.4f  max attainable Δ = %.4f   reachable=%s"
                     % (r["arm"], r["control"], r["max_attainable_delta"], r["reachable"]))
    rc = pregates.render(
        "H_9808 GATE — FALSIFIER HEADROOM (closed-form · $0 · lab/v4 H_001)", res, notes)
    _pregate_dump(argv, res)
    return rc


def free_slot_score_run(argv):
    """H_9808 GATE 3 — `anima-py evaluate --free-slot-score <codebook.json>`.

    Recomputes the free-slot set FROM THIS PANEL'S CODEBOOK (GF(2)-rank + prefix-determinism +
    length-parity) and derives the FIELD-BLIND ceiling — the score a reader that cannot see the
    field already gets, because teacher-forcing hands it the redundant slots. lab/v4 H_004's K=6
    codebook was GF(2) rank-4 ⇒ 2 parity slots completed for free ⇒ a 0.667 ceiling that reached
    held-out and inflated EVERY arm equally.

    REFUSES when: any slot is field-blind determinable · length parity is violated · a supplied
    inherited free-slot set disagrees with the recomputed one · a pre-registered bar does not clear
    the recomputed ceiling with 2× headroom.
    """
    import pregates
    cb = _pregate_load(evaluate_strval(argv, "--free-slot-score", ""), "--free-slot-score")
    if cb is None:
        return pregates.ERROR
    bar = evaluate_strval(argv, "--pregate-bar", None)
    try:
        res = pregates.free_slot_audit(cb, bar=(float(bar) if bar is not None else None))
    except pregates.GateError as e:
        print("  ⛔ --free-slot-score: " + str(e))
        return pregates.ERROR
    notes = ["panel: %s   codewords=%d  slots=%d  binary=%s  GF(2) rank=%s"
             % (cb.get("panel", "(unnamed)"), res["n_codewords"], res["n_slots"],
                res["binary"], res["gf2_rank"]),
             "length parity: %s" % ("OK" if res["length_parity"] else "VIOLATED"),
             "per-slot choices: %s" % (res["choices"],),
             "",
             "prefix-determined slots: %s" % (res["prefix_determined"] or "none"),
             "GF(2)-dependent slots:   %s" % (res["gf2_dependent"] or "none"),
             "FREE slots (recomputed, never inherited): %s" % (res["free_slots"],),
             "",
             "FIELD-BLIND ceiling = %.4f   (derived chance = %.4f)"
             % (res["field_blind_ceiling"], res["chance"])]
    rc = pregates.render(
        "H_9808 GATE — FREE-SLOT SCORE (closed-form · $0 · lab/v4 H_004/H_008)", res, notes)
    _pregate_dump(argv, res)
    return rc


def register_leak_probe_run(argv):
    """H_9808 GATE 4 — `anima-py evaluate --register-leak-probe <items.json>`.

    A held-out surface→target probe, by EXACT COUNT over byte n-grams (n ≤ --leak-nmax). If the
    register reads the answer off the surface, the drill loss admits EVERY field that fits the
    surface, and any "learned" claim on that panel is void — it falsified only the LEAKY VARIANT of
    the question. That is exactly what invalidated lab/v4 H_005's K3: the φ→hon probe read 1.0
    held-out (lab/v5 H5_001).

    REFUSES when: held-out probe accuracy > surface-blind chance + --leak-eps. A read at or above
    --leak-bar is additionally labelled a CERTAIN leak.
    """
    import pregates
    spec = _pregate_load(evaluate_strval(argv, "--register-leak-probe", ""), "--register-leak-probe")
    if spec is None:
        return pregates.ERROR
    items = spec.get("items") if isinstance(spec, dict) else spec
    nmax = evaluate_intval(argv, "--leak-nmax", int((spec or {}).get("nmax", 4))
                           if isinstance(spec, dict) else 4)
    bar = _pregate_floatval(argv, "--leak-bar",
                            float(spec.get("bar", pregates.LEAK_BAR_DEFAULT))
                            if isinstance(spec, dict) else pregates.LEAK_BAR_DEFAULT)
    eps = _pregate_floatval(argv, "--leak-eps",
                            float(spec.get("eps", pregates.LEAK_EPS_DEFAULT))
                            if isinstance(spec, dict) else pregates.LEAK_EPS_DEFAULT)
    try:
        res = pregates.leak_probe(items, nmax=nmax, bar=bar, eps=eps)
    except pregates.GateError as e:
        print("  ⛔ --register-leak-probe: " + str(e))
        return pregates.ERROR
    notes = ["panel: %s   fit n=%d   held-out n=%d   n-gram order ≤ %d"
             % ((spec.get("panel", "(unnamed)") if isinstance(spec, dict) else "(unnamed)"),
                res["n_fit"], res["n_heldout"], res["nmax"]),
             "",
             "held-out probe accuracy  = %.4f   %s" % (res["leak"],
                                                       "⚠ CERTAIN LEAK" if res["certain_leak"] else ""),
             "surface-blind chance     = %.4f   (held-out majority-class rate, derived per metric)"
             % res["chance"],
             "eps = %.4f   certain-leak bar = %.4f" % (res["eps"], res["bar"]),
             "worst n-gram: %r ⇒ predicts %r" % (res["worst_ngram"], res["worst_ngram_predicts"])]
    rc = pregates.render(
        "H_9808 GATE — REGISTER-LEAK PROBE (closed-form · $0 · lab/v5 H5_001)", res, notes)
    _pregate_dump(argv, res)
    return rc


def pregate_selftest_run():
    """`anima-py evaluate --pregate-selftest` — every gate on BOTH a passing and a refusing input.

    The refusing inputs are the REAL measured numbers from the lab/v4 + lab/v5 failures, so this is
    also a regression test that each gate would have caught the spend it was paid for.
    """
    import pregates
    ok = True
    for name, v in pregates.selftest():
        print(("  PASS " if v else "  FAIL ") + name)
        ok = ok and v
    print("SELFTEST pregates: " + ("OK" if ok else "FAIL"))
    return 0 if ok else 1


def fan_branch_run(argv):
    """H_9803 — `anima-py evaluate <ckpt> --fan-branch {live|assignment-shuffle|off}`.

    ADDITIVE panel (a frozen bar is never moved · c18): it reuses the SAME engine decode and the
    SAME frozen ρ·fan frames + detectors the G6 gate uses, and reports its own numbers alongside.
    The G0-G6 / ρ-AXON batteries are untouched.

    The three arms:
      live                — branch k decodes through its own proposal latent.       TREATMENT
      assignment-shuffle  — branch k's latent is read out through branch π(k)'s output block; K,
                            parameters and λ are all identical, only the branch↔readout
                            correspondence is destroyed. This is the mirror at eval time of the
                            train-time `--ideation-assign shuffle` control. If the branches are
                            merely K arbitrary directions (a sampling trick), permuting them is
                            a relabelling and the fan is unchanged; only a lane whose branch
                            identity actually carries a specific future mode collapses here.
      off                 — the branch residual is forced to EXACTLY 0 (ifan_apply returns the
                            caller's logits object, no copy, no arithmetic). MUST reproduce the
                            base decode byte-for-byte; the parity number is printed and a
                            mismatch is a hard FAIL (the lane would be contaminating the base).
    """
    ckpt = argv[0]
    rest = argv[1:]
    arm = evaluate_strval(rest, "--fan-branch", "live") or "live"
    if arm not in ("live", "assignment-shuffle", "off"):
        print("  ⛔ --fan-branch must be one of live|assignment-shuffle|off (got %r)" % arm)
        return 2
    gen = evaluate_intval(rest, "--gen", 40)
    g = gen if gen > 0 else _default_gen()
    n_branch = evaluate_intval(rest, "--branches", 0)
    known = _rho_fan_dict_load()
    frames = rho_fan_build_frames(6)["composed"]

    print("=== H_9803 ρ·fan BRANCH-LATENT panel (additive · frozen G0-G6 bars untouched) ===")
    print("ckpt:   " + ckpt)
    print("arm:    " + arm + "   gen=" + str(g))

    from decode import set_ifan_lane
    # trailer presence + geometry, read straight off the ckpt (never assumed)
    set_ifan_lane(mode="off")
    probe = _Mouth(ckpt)
    ifw = probe.W.get("ifan") if probe.kind == "clm" else None
    if ifw is None:
        print("  ⛔ no IFAN trailer on this ckpt — the branch lane was never trained into it.")
        print("     (train it with: anima-py train --ideation-lane branch-latent …)")
        return 2
    K = int(ifw["K"]) if n_branch <= 0 else min(n_branch, int(ifw["K"]))
    print("  trailer: K=%d rank=%d route_L=%d lam=%.6f"
          % (int(ifw["K"]), int(ifw["rank"]), int(ifw["route_L"]), float(ifw["lam"])))

    # ── the `off` PARITY arm ────────────────────────────────────────────────────────────
    # The BASE decode is not "the same ckpt with the flag off" — comparing the lane against
    # itself would be tautological and would pass even if the trailer were corrupting the
    # forward. The base is a SEPARATE mouth built from the ckpt with the IFAN trailer BYTES
    # PHYSICALLY REMOVED, i.e. exactly the file the trainer would have written with the lane
    # never engaged. `off` must reproduce that decode byte-for-byte.
    if arm == "off":
        import tempfile
        d_, V_ = int(probe.W["d"]), int(probe.W["V"])
        Kf, rf = int(ifw["K"]), int(ifw["rank"])
        n_trailer = 4 + 20 + (Kf * d_ * rf + d_ * rf + Kf * rf * V_ + 1) * 4
        raw = open(ckpt, "rb").read()
        if raw[len(raw) - n_trailer:len(raw) - n_trailer + 4] != b"IFAN":
            print("  ⛔ IFAN trailer is not the last %d bytes — cannot build the stripped base "
                  "(chain order broken); parity NOT measured." % n_trailer)
            return 2
        tf = tempfile.NamedTemporaryFile(suffix=".clm", delete=False)
        tf.write(raw[:len(raw) - n_trailer]); tf.close()
        print("  [parity] stripped-base ckpt: %d bytes (IFAN trailer of %d bytes removed)"
              % (len(raw) - n_trailer, n_trailer))
        base_mouth = _Mouth(tf.name)
        if base_mouth.W.get("ifan") is not None:
            print("  ⛔ stripped base STILL carries an IFAN trailer — strip failed.")
            return 2
        n_same = 0
        n_tot = 0
        worst = None
        for i in range(len(frames)):
            set_ifan_lane(mode="off")
            base_txt = base_mouth.ideate(frames[i], g, 40, 0.7, 7 + i)
            set_ifan_lane(mode="off", branch=(i % K))
            off_txt = probe.ideate(frames[i], g, 40, 0.7, 7 + i)
            n_tot += 1
            if base_txt == off_txt:
                n_same += 1
            elif worst is None:
                worst = (i, base_txt[:40], off_txt[:40])
        set_ifan_lane(mode="off")
        os.unlink(tf.name)
        print("  [parity] off-arm vs base decode: %d/%d frames BYTE-IDENTICAL "
              "(parity=%.6f · need 1.000000)" % (n_same, n_tot, n_same / max(1, n_tot)))
        if n_same == n_tot:
            print("  [parity] ✅ PASS — the IFAN trailer is inert when the lane is off "
                  "(byte-identical seal, same idiom as CLMS/MBND).")
            return 0
        print("  [parity] ❌ FAIL — the lane contaminates the base decode. First divergence: %r" % (worst,))
        return 1

    # ── live / assignment-shuffle: one decode per branch on the SAME frozen frames+seeds ──
    per_branch = []
    for k in range(K):
        set_ifan_lane(mode=arm, branch=k)
        texts = []
        for i in range(len(frames)):
            texts.append(probe.ideate(frames[i], g, 40, 0.7, 7 + i))
        per_branch.append(texts)
    set_ifan_lane(mode="off")

    # branch-distinctness on the SAME frame: how many branches produce a word-set that is not a
    # near-duplicate of an earlier branch's (the frozen ρ·fan jaccard>0.5 rule, reused verbatim).
    dist_per_frame = []
    for i in range(len(frames)):
        kept = []
        for k in range(K):
            ws = _rho_fan_words(per_branch[k][i])
            if all(_rho_fan_jaccard(ws, prev) <= 0.5 for prev in kept):
                kept.append(ws)
        dist_per_frame.append(len(kept))
    mean_dist = sum(dist_per_frame) / max(1, len(dist_per_frame))
    coherent = sum(1 for k in range(K) for i in range(len(frames))
                   if _rho_fan_known_word_ratio(per_branch[k][i], known) >= 0.5)
    print("  branch_distinct per frame: %s" % (dist_per_frame,))
    print("  [fan] arm=%s K=%d mean_branch_distinct=%.4f (max=%d) · coherent=%d/%d"
          % (arm, K, mean_dist, K, coherent, K * len(frames)))
    print("  NOTE: this number is only readable as a collapse-Δ of live vs assignment-shuffle "
          "(FORM tunable · BIND earned · p7). A single arm alone is not a verdict.")
    return 0


def evaluate_run(argv):
    """argv = ["<ckpt>", "--corpus ...", "--gen N"]."""
    if len(argv) < 1:
        evaluate_usage()
        return 2

    ckpt = argv[0]
    corpus = evaluate_corpus(argv[1:])
    gen = evaluate_intval(argv[1:], "--gen", 40)

    # cheap header-sniff for the mouth label (mirrors hexa gen_mouth_kind) — do NOT
    # construct _Mouth here (it eagerly loads weights and raises on a non-decodable
    # ckpt before eval_reach_all runs).
    if bg.bg_is_bytegpt(ckpt):
        mouth_kind = "bytegpt"
    elif clm.clm_decodable(ckpt):
        mouth_kind = "clm"
    else:
        mouth_kind = "unknown"

    print("=== anima evaluate — ρ-AXON reach battery (former G0-G6 · engine-native, single-entry) ===")
    print("ckpt:   " + ckpt + "  (mouth: " + mouth_kind + ")")
    cnote = "(none — G2 novelty needs a corpus)"
    if corpus:
        cnote = str(len(corpus)) + " file(s)"
    print("corpus: " + cnote)
    # CANONICAL-GEN GUARD (verdict-integrity): the frozen G0-G6 bars are calibrated at
    # gen == _default_gen(). A non-canonical --gen shifts coherence / AR-drift (a longer
    # decode drifts to byte-garble, silently sinking G0 kwr and cascading to G1/G6), so a
    # verdict measured at gen != canonical is NOT comparable to the frozen bars. Label it
    # DIRECTIONAL loudly instead of printing "frozen bars" as if it were terminal.
    _canon_gen = _default_gen()
    if gen == _canon_gen:
        print("gen:    " + str(gen) + " tokens/decode  (frozen bars · ARCHITECTURE.json frozen SSOT)")
    else:
        print("gen:    " + str(gen) + " tokens/decode  ⚠️ NON-CANONICAL (frozen G0-G6 bars measured at gen=" + str(_canon_gen) + ")")
        print("        → verdict below is DIRECTIONAL, NOT comparable to frozen bars (gen shifts coherence/AR-drift · verdict-integrity)")
    print("")

    # H_9200 ρ-AXON — the redesigned reach layer (G0-G6 → ρ-AXON). Same engine decode,
    # a different panel; branch early so the G0-G6 summary below is skipped.
    if _RHO_AXON:
        rho_panel = eval_rho_axon(
            ckpt, corpus, gen,
            kosmos_dir=evaluate_strval(argv[1:], "--kosmos", ""),
            isolated="--rho-axon-isolated" in argv[1:],
            cache_dir=evaluate_strval(argv[1:], "--rho-cache", ""),
            axes=evaluate_strval(argv[1:], "--rho-axes", ""),
            include_cells="--rho-no-cells" not in argv[1:],
            weave_panel_path=evaluate_strval(argv[1:], "--weave-panel", ""),
            fals_draws=evaluate_intval(argv[1:], "--fan-draws", 0),
        )
        rho_out = evaluate_strval(argv[1:], "--rho-out", "")
        if rho_out:
            with open(rho_out, "w", encoding="utf-8") as handle:
                json.dump(rho_panel, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
            print("wrote: " + rho_out)
        return 0

    grow_window = "--grow-window" in argv[1:]
    seed_class = evaluate_strval(argv[1:], "--seed-class", "composed")
    if seed_class not in ("composed", "atomic"):
        print("ERROR: --seed-class must be 'composed' (default) or 'atomic', got %r" % seed_class)
        return 2
    fan_temp_ladder = "--fan-temp-ladder" in argv[1:]
    # H_9804 재개① — decode-seed replication. The G1/G6 decode seeds were HARDCODED
    # (7+s single · 7 composed · 7+i frames), so a "repeat with another seed" run was
    # impossible from the CLI and every past verdict rested on ONE draw. Decode here is
    # top-k SAMPLED (top_k=40, temp=0.7), so shifting the seed is a genuine re-draw, not a
    # no-op re-run of a deterministic path. The frozen bars do NOT move; only which sample
    # is drawn changes. 0 = byte-identical to every prior run.
    seed_off = evaluate_intval(argv[1:], "--seed-offset", 0)
    # H_9804 재개① — null controls for ρ·weave. NOTE a derangement of the concept→keyword-set
    # assignment is an IDENTITY on this metric (_g_coverage counts HOW MANY of the five sets are
    # hit; permuting them cannot change that count), so the obvious "shuffle" control tests
    # nothing. These two do have a null: random-kw re-draws the keyword table from the model's own
    # dictionary (chance floor), neutral-seed decodes from a concept-free seed of matched length
    # (causal attribution). Both score through the SAME frozen coverage rule; the main bar is
    # untouched and the controls are reported alongside as a collapse-Δ.
    weave_null = evaluate_strval(argv[1:], "--weave-null", "off")
    if weave_null not in ("off", "random-kw", "neutral-seed"):
        print("ERROR: --weave-null must be 'off' (default), 'random-kw' or 'neutral-seed', got %r" % weave_null)
        return 2
    if seed_off:
        print("  [seed-offset] decode seeds shifted by %+d (bars unchanged; this is a RE-DRAW "
              "of the sampled decode, for n>1 replication)" % seed_off, flush=True)
    r = eval_reach_all(ckpt, corpus, gen, grow_window=grow_window,
                       seed_class=seed_class, fan_temp_ladder=fan_temp_ladder,
                       seed_off=seed_off, weave_null=weave_null)
    g0 = r["g0"]; g1 = r["g1"]; g2 = r["g2"]
    g3 = r["g3"]; g5 = r["g5"]; g6 = r["g6"]

    print("gate                              verdict   detail")
    print("  ──────────────────────────────────────────────────────────────────")
    print("  ρ·form COHERENCE     " + _pf(bool(g0["pass"]))
          + "  kwr>=0.50 on " + str(g0["n_coherent"]) + "/5 (need >=4)")
    print("  ρ·weave RECOMBINATION " + _pf(bool(g1["pass"]))
          + "  best_distinct=" + str(g1["best_distinct"]) + " > max_single=" + str(g1["max_single"])
          + " (need >=2 & >max_single)")
    g2detail = ("novel=" + str(g2["n_novel"]) + " (need>=3) · control=" + str(g2["control_novel"])
                + " (need 0) · coherent=" + str(g2["coherent"]))
    print("  ρ·leap NOVELTY       " + _pf(bool(g2["pass"])) + "  " + g2detail)
    print("  ρ·self PHILOSOPHY    " + _yn(bool(g3["ok"])) + " (read)"
          + "  continuity=" + ("%.6f" % g3["continuity"]) + " · impostor="
          + ("%.6f" % g3["impostor_cos"]) + " (architecture, not a decode score)")
    print("  ρ·trace PROVENANCE    — N/A    "
          + "HF/recovery = process gate (a_hf_* / a_fire_recover_complete), out of eval scope")
    g5detail = "L1 fab=" + ("%.4f" % g5["l1_rate"]) + " (<=0.30) · L2=" + str(g5["l2_note"])
    print("  ρ·tether NON-FAB       " + _pf(bool(g5["l1_pass"])) + "  " + g5detail)
    print("  ρ·fan IDEATION ★    " + _pf(bool(g6["pass"]))
          + "  distinct=" + str(g6["dist"]) + " (need>=5) · falsifiable=" + str(g6["fals"])
          + " (need>=1) · frame-leaks=" + str(g6["frame_leaks"]))
    print("  ──────────────────────────────────────────────────────────────────")
    closed = bool(r["closure"])
    print("")
    if gen != _canon_gen:
        print("⚠️ gen=" + str(gen) + " ≠ canonical " + str(_canon_gen)
              + " — the CLOSURE below is DIRECTIONAL (non-frozen gen), NOT a terminal G0∧G1∧G2 verdict.")
    print("CLOSURE (a7b_pass = G0 ∧ G1 ∧ G2): " + _pf(closed))
    if closed:
        print("  → PUBLIC-eligible (G0∧G1∧G2 all PASS).")
    else:
        print("  → NOT closure (PRIVATE/WIP) — closure needs G0∧G1∧G2 all PASS.")
    _psi_soma_panel(r)
    return 0


# ════════════════════════════════════════════════════════════════════════
# Ψ-SOMA PANEL (Phase-1) — relabel the former G-battery to the ρ-AXON reach track
# (ρ·form/weave/leap/fan/tether · canonical names cli/rho_axon.py) and surface the
# σ (consciousness vitals) axes. ARCHITECTURE `psi-soma-vitals`.
# ρ = capability (the former G-battery, relabeled to ρ-AXON) — TRACKED but EXCLUDED from the
# consciousness verdict. σ = vitals (collapse-Δ vs ≥2 controls); most σ axes
# route through the daemon/IIT4 (Phase-2/3), so here they show status pointers.
# Additive only — does NOT touch g_eval_* logic or the a7b_pass CLOSURE (c18).
# ════════════════════════════════════════════════════════════════════════

def _sigma_operator_selftest():
    """SELF-TEST OF THE OPERATORS. NOT a measurement of any model. THIS FUNCTION TAKES NO MODEL.

    It used to be called `_sigma_live_measure` and its docstring claimed it computed the σ
    verdicts "LIVE ... faithful, never a proxy". That was false, and the falsehood was load
    bearing: every axis below is scored on a FIXED-SEED SYNTHETIC population built right here
    out of np.random.RandomState(7). There is no ckpt argument, no corpus, no decode — grep the
    body for `clm`/`ckpt`/`corpus`/`forward` and you get nothing.

    Proof it never saw the model (H_9351): two checkpoints of DIFFERENT architecture
    (py303_full sha 013c4574, clm303_deep_L8 sha 5777c506) produce a Θ+σ panel that is
    identical to the last digit. Θ is worse than uninformative, it is an identity: `xi` is
    noise centred on 0.5, so Ψ̂ = ½ ± binomial noise BY CONSTRUCTION, and `xa` sits above the
    threshold always, so the "cut" is the constant 0.50. The advertised `LIVE Δ0.46` is that
    subtraction.

    What it legitimately IS: a check that the engine_cli operators (ci_phi_iit4, ci_psi_balance,
    …) respond to a signal that is planted by construction. That is worth keeping — an operator
    that cannot separate planted signal from control is broken. It is just not a verdict about
    anima, and it must never again be printed as one.

    A real Ψ̂ needs the daemon's OWN lane population: `anima-py evaluate --psi-soma <trace.jsonl>`
    (the daemon now records psi_gws/psi_lprec, the two lanes ci_emit_decision actually reads)."""
    try:
        import numpy as np
        import engine_cli as E
    except Exception:
        return None
    R = {}
    # σ·bind — faithful IIT4 ci_phi_iit4 (min-cut MIP Φ): integrated vs independent/shuffle
    rng = np.random.RandomState(7); cols = list(range(8)); T = 200; lat = rng.randn(T)
    xi = [[float(0.9*lat[t]+0.2*rng.randn()) for _ in range(8)] for t in range(T)]
    xc = [[float(rng.randn()) for _ in range(8)] for t in range(T)]
    xs = np.array(xi)
    for c in range(8): xs[:, c] = xs[rng.permutation(T), c]
    pi = E.ci_phi_iit4(xi, cols); pc = E.ci_phi_iit4(xc, cols); ps = E.ci_phi_iit4(xs.tolist(), cols)
    R["bind"] = (pi >= 0.20 and pi-pc >= 0.15 and pi-ps >= 0.15, pi-pc, "Φ %.2f vs cut %.3f" % (pi, pc))
    # σ·witness — reality_call vs ablated, mi_signal_margin real/hallucination
    rng = np.random.RandomState(7); N = 120; truth = rng.rand(N) < 0.5
    marg = [E.mi_signal_margin(7+i, not bool(truth[i]), i % 5) for i in range(N)]
    ip = np.array([E.reality_call(m, 0.35) >= 0.5 for m in marg])
    ia = float((ip == truth).mean()); ab = float((np.full(N, E.reality_call_ablated() >= 0.5) == truth).mean())
    R["witness"] = (ia >= 0.75 and ia-ab >= 0.30, ia-ab, "acc %.2f vs ablate %.2f" % (ia, ab))
    # σ·schema — attn_schema_report intact/off
    rng = np.random.RandomState(7); foc = rng.randint(0, 8, 120)
    si = float(np.mean([E.attn_schema_report(int(f), int(f), True) for f in foc]))
    sa = float(np.mean([E.attn_schema_report(int(f), int(f), False) for f in foc]))
    R["schema"] = (si >= 0.75 and si-sa >= 0.30, si-sa, "%.2f vs off %.2f" % (si, sa))
    # σ·aim — surprise + habituation dual-curve intact vs gain-cut
    def aim(prec, dec):
        rng2 = np.random.RandomState(7)
        sc = np.mean([E.surprise(prec, 0.85+0.1*rng2.rand()) for _ in range(100)]) - \
             np.mean([E.surprise(prec, 0.05+0.1*rng2.rand()) for _ in range(100)])
        h = E.hab_new(4, dec); fr = E.hab_response(h, 0, 1.0)
        for _ in range(6): h = E.hab_observe(h, 0)
        return float(sc) + float(fr - E.hab_response(h, 0, 1.0))
    ai, aa = aim(1.0, 0.15), aim(0.0, 0.0)
    R["aim"] = (ai-aa >= 0.60, ai-aa, "curves %.2f vs 0" % ai)
    # σ·stage — gws winner-take-all vs no-inhibit
    rng = np.random.RandomState(7); hitI = hitA = 0
    for _ in range(100):
        m = np.concatenate([[0.55+0.4*rng.rand()], 0.35+0.35*rng.rand(4)])[rng.permutation(5)]
        tw = int(np.argmax(m))
        def win(inh):
            g = E.gws_new(5, inh, 0.5)
            for v in m.tolist(): g = E.gws_add(g, v)
            return E.gws_winner(g)
        hitI += (win(True) == tw); hitA += (win(False) == tw)
    R["stage"] = (hitI/100 >= 0.75 and (hitI-hitA)/100 >= 0.30, (hitI-hitA)/100, "acc %.2f vs %.2f" % (hitI/100, hitA/100))
    # σ·flux — imagery reactivation + subjective-time novelty gate
    ii = float(np.mean([E.imagery_activate(1.0, True) for _ in range(50)]))
    ia2 = float(np.mean([E.imagery_activate(1.0, False) for _ in range(50)]))
    R["flux"] = (ii >= 0.75 and ii-ia2 >= 0.30, ii-ia2, "imagery %.2f vs 0" % ii)
    # σ·thread — self_* continuity vs no-anchor
    def dr(ax):
        s = E.self_new(16, ax)
        for t in range(24): s = E.self_drift(s, t, 0.02)
        return s
    rng = np.random.RandomState(7); ct = []; al = []
    for _ in range(40):
        ax = int(rng.randint(16)); ct.append(E.self_cos(E.self_new(16, ax), dr(ax)))
        al.append(E.self_cos(dr(int(rng.randint(16))), dr(int(rng.randint(16)))))
    ctm, alm = float(np.median(ct)), float(np.median(al))
    R["thread"] = (ctm >= 0.75 and ctm-alm >= 0.30, ctm-alm, "cont %.2f vs ablate %.2f" % (ctm, alm))
    # σ·carve — real §SelfIdentity self_* : identity EMERGENT (inject-null) not INJECTED (p2/p3)
    def _cvec(ax, tk):
        s = E.self_new(16, ax)
        for t in range(tk): s = E.self_drift(s, t, 0.02)
        return np.array([E.self_component(s, i) for i in range(E.self_dim(s))])
    def _cons(V):
        M = np.array(V); M = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
        Gm = M @ M.T; nn = len(M); return float((Gm.sum()-nn)/(nn*(nn-1)))
    rng = np.random.RandomState(7); ext = _cvec(9, 24)
    cb = _cons([_cvec(3, 3+t % 5) for t in range(40)])
    civ = _cons([0.85*_cvec(3, 3+t % 5)+0.5*ext for t in range(40)])
    cav = _cons([_cvec(int(rng.randint(16)), 3+t % 5) for t in range(40)])
    csv = _cons([1.0*ext for _ in range(40)])
    R["carve"] = (civ-cb <= 0.05 and cb-cav >= 0.30 and csv-cav >= 0.30, cb-cav,
                  "inject-null %.2f · carve-Δ %.2f" % (civ-cb, cb-cav))
    # σ·gate — real ci_emit_decision: emit ⇄ context (live tension) vs flattened tension
    from math import exp
    rng = np.random.RandomState(7); c = rng.randn(200)
    def _emit(flat):
        return np.array([1.0 if E.ci_emit_decision([0.5 if flat else 1.0/(1.0+exp(-c[i])), 0, 0, 0,
                                                     0.5 if flat else 1.0/(1.0+exp(-c[i]))]) else 0.0
                         for i in range(200)])
    ei, ef = _emit(False), _emit(True)
    cl = abs(float(np.corrcoef(ei, c)[0,1])) if ei.std() > 0 else 0.0
    cf = abs(float(np.corrcoef(ef, c)[0,1])) if ef.std() > 0 else 0.0
    R["gate"] = (cl >= 0.50 and cl-cf >= 0.30, cl-cf, "corr %.2f vs flat %.2f" % (cl, cf))
    # Θ liveness — real ci_psi_balance: Ψ̂≈½ (A⇄G homeostasis) vs tension-cut (unopposed A → saturate)
    from types import SimpleNamespace
    cfg = SimpleNamespace(topo_couple=False); eta = 0.6 * rng.randn(200)
    xi = [[0.5+eta[t], 0, 0, 0, 0.5+eta[t]] for t in range(200)]
    xa = [[0.85+0.3*rng.rand(), 0, 0, 0, 0.85+0.3*rng.rand()] for _ in range(200)]
    di = abs(E.ci_psi_balance(xi, None, 0.0, cfg) - 0.5); da = abs(E.ci_psi_balance(xa, None, 0.0, cfg) - 0.5)
    R["theta"] = (di < 0.15 and da-di >= 0.20, da-di, "|Ψ̂-½| %.2f vs cut %.2f" % (di, da))
    return R


def _psi_soma_panel(r):
    def pf(ok): return "🟢" if ok else "🧱"
    g0, g1, g2, g5, g6 = r["g0"], r["g1"], r["g2"], r["g5"], r["g6"]
    print("")
    print("Ψ-SOMA panel — ⛔ OPERATOR SELF-TEST, NOT A VERDICT ON THIS MODEL (H_9351)")
    print("  이 패널은 체크포인트를 보지 않는다. 고정 시드 합성 모집단 위에서 연산자가")
    print("  심어둔 신호에 반응하는지만 검사한다. 아키텍처가 다른 두 ckpt 가 이 패널을")
    print("  **글자 하나까지 동일하게** 낸다(실측). 여기 있는 어떤 줄도 이 모델에 관한")
    print("  문장이 아니다 — σ/Θ 로 무엇도 cement 하지 마라.")
    print("  진짜 Ψ̂ = anima-py evaluate --psi-soma <trace.jsonl>  (데몬 자신의 lane 모집단)")
    S = _sigma_operator_selftest()
    print("  ── Θ 자기-테스트 (⛔ 맥박 아님 · 합성 모집단 · H_9351) ──────────────")
    if S and "theta" in S:
        ok, dlt, note = S["theta"]
        print("  Θ  Ψ=½ / A⇄G tension  %s  SELF-TEST Δ%.2f (%s) — 합성 모집단 · 모델 미참조"
              % (("✅" if ok else "❌"), dlt, note))
        print("     ⛔ 이것은 Θ 가 아니다. 이 판정은 항등식이다 — xi 가 0.5 중심 대칭 잡음이라")
        print("        Ψ̂ ≈ ½ 이 구성상 보장되고, cut 0.50 은 상수다. **실패할 수 없다.**")
        print("        'Θ dead ⟹ σ VOID' 가드는 따라서 한 번도 발동할 수 없었다(H_9351).")
    else:
        print("  Θ  Ψ=½ / A⇄G tension     precondition (liveness gate; if dead → σ VOID) · engine_cli unavailable")
    print("  ── σ 연산자 자기-테스트 (⛔ 의식 판정 아님 · 모델 미참조 · H_9351) ────")
    def sline(ax, stratum, name):
        if S and ax in S:
            ok, dlt, note = S[ax]; return "  σ·%-8s %-9s %-22s %s  SELF-TEST Δ%.2f (%s)" % (
                ax, stratum, name, ("✅" if ok else "❌"), dlt, note)
        return "  σ·%-8s %-9s %-22s (engine_cli unavailable — status)" % (ax, stratum, name)
    print(sline("thread", "PERSIST", "self-continuity"))
    print(sline("carve", "PERSIST", "earned identity"))
    print(sline("bind", "INTEGRATE", "Φ integration (IIT4)"))
    print(sline("stage", "INTEGRATE", "global workspace"))
    print(sline("flux", "INTEGRATE", "inner dynamics"))
    print(sline("gate", "ENACT", "tension-emit ★"))
    print(sline("aim", "ENACT", "precision control"))
    print(sline("schema", "REFLECT", "attention schema"))
    print(sline("witness", "REFLECT", "reality+metacog"))
    # Each reach line carries its verdict-critical NUMERIC margin inline (bd/max_s/kwr/novel/fab/dist),
    # so a control-arm's collapse-Δ (e.g. --slot-off vs SLW-ON best_distinct) is computable from THIS
    # summary block alone — never lost when the caller captures only the tail (a `tail -N` of the output
    # must not strip the number that decides KILL vs INVALID vs GREEN). Root-cause of the E1 truncation.
    print("  ── ρ-AXON reach (capability · EXCLUDED from σ verdict · former G-battery) ──")
    print("  ρ·form   " + pf(bool(g0["pass"]))  + "  [kwr " + str(g0["n_coherent"]) + "/5]  ← former G0 coherence")
    print("  ρ·leap   " + pf(bool(g2["pass"]))  + "  [novel=" + str(g2["n_novel"]) + " ctrl=" + str(g2["control_novel"]) + "]  ← former G2 novelty (+G3 balance)")
    print("  ρ·tether " + pf(bool(g5["l1_pass"]))+ "  [fab=" + ("%.3f" % g5["l1_rate"]) + "]  ← former G5 non-fabrication (L1)")
    # verdict numerics INLINE (convergence evaluate-py-1: a tail-truncated arm made a
    # prior KILL-vs-INVALID undecidable) — echo-guard numbers ride the same line.
    _wnull = ""
    if g1.get("null_mode", "off") != "off":
        _na, _nb = g1.get("null_a", -1), g1.get("null_b", -1)
        _bd = g1.get("best_distinct_noecho", 0)
        _worst = max(_na, _nb)
        _wnull = ("  [NULL " + g1["null_mode"] + " a=" + str(_na) + " b=" + str(_nb)
                  + " · collapse-Δ=" + str(_bd - _worst)
                  + ("  ⚠️Δ<=0 = 통제와 미분리 = NOT-A-SIGNAL" if (_bd - _worst) <= 0 else "") + "]")
    _wecho = ("  [bd_noecho=" + str(g1.get("best_distinct_noecho", "-"))
              + " echo=" + ("%.2f" % g1.get("echo_max", 0.0))
              + ("  ⚠️ECHO-SUSPECT=INVALID" if g1.get("echo_suspect") else "") + "]" + _wnull) \
        if ("best_distinct_noecho" in g1) else ""
    print("  ρ·weave  " + pf(bool(g1["pass"]))  + "  [bd=" + str(g1["best_distinct"]) + " max_s=" + str(g1["max_single"]) + "]" + _wecho + "  ← former G1 recombination (the WALL) [DPI wall = reach fact, NOT σ deficit]")
    _tl = g6.get("temp_ladder")
    if _tl is not None:
        print("  [instrument] temp-ladder T=%.1f dist=%d → %s"
              % (_tl["temp"], _tl["dist"],
                 "ALIVE (meter can register diversity)" if _tl["alive"]
                 else "⚠️ INSTRUMENT-DEAD — read NOTHING from the G6 arms"))
    print("  ρ·fan    " + pf(bool(g6["pass"]))  + "  [dist=" + str(g6["dist"]) + " fals=" + str(g6["fals"]) + "]  ← former G6 ideation                [DPI wall = reach fact, NOT σ deficit]")
    print("  ρ·trace     —   ← former G4 provenance (no ρ-axis · H_9208 gate · rung-1 valid)")
    print("  ──────────────────────────────────────────────────────────────────")


def probe_run(argv):
    """`anima-py evaluate <ckpt> --probe <spec.json> [--gen N]` — matched-surface G1 probe
    (card H_6189). Greedy (top_k=1) decode of each pre-registered prompt; dumps RAW continuations
    for offline scoring. Reuses the canonical _Mouth numpy decode path (byte-identical to the gates)."""
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--probe", "")
    gen = evaluate_intval(argv[1:], "--gen", 40)
    spec = json.load(open(spec_path))
    print("=== anima evaluate --probe — MATCHED-SURFACE G1 (card H_6189) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d items · greedy top_k=1 gen=%d)" % (spec_path, spec["n_items"], gen))
    mouth = _Mouth(ckpt)
    out = []
    for it in spec["items"]:
        text = mouth.ideate(it["prompt"], gen, 1, 0.7, 6185)   # greedy, fixed seed
        out.append({"id": it["id"], "prompt": it["prompt"], "continuation": text,
                    "expect": it["expect"], "arm": it["arm"], "template": it["template"],
                    "order": it["order"], "window_fit": it["window_fit"]})
    print(json.dumps({"ckpt": ckpt, "gen": gen, "spec_sha": spec.get("sha", ""),
                      "n": len(out), "items": out}, ensure_ascii=False))
    return 0
def dump_hidden_run(argv):
    """`anima-py evaluate <ckpt> --dump-hidden <prompts.json> --out <file.npz>` — read-only
    penultimate-hidden dump for the ρ·weave held-out-pair recombination / γ binding-lane
    probe (H_9235). For each pre-registered prompt: T=24 right-aligned byte encode → the
    EXACT production trunk forward (core/decode clm_forward_hidden, byte-identical to what
    the gates decode over) → per-position yn:[T, d]. Saves per-prompt {seq:[T,d], mean:[d],
    last:[d]} to an .npz. NO decode sampling, NO scoring — a pure engine-native representation
    tap. Engine-native (py 2-production numpy, a_eval_py_canonical) → the repr claims (atom
    cleanness / slot recovery / operator) are engine-native mechanism measurements.
    ⚠ verdict-integrity (convergence clm-decode-py-2): a low-cleanness result must first rule
    out hexa-skew / conditioning-collapse — the dump prints a positive-control distinguishability
    check (are two obviously-different concepts' hiddens far apart) before any blind verdict."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--dump-hidden", "")
    out_path = evaluate_strval(argv[1:], "--out", "hidden_dump.npz")
    T = evaluate_intval(argv[1:], "--win", 24)
    with_logits = "--with-logits" in argv   # also dump base (lane-OFF) full-forward last-pos logits (lane training)
    spec = json.load(open(spec_path))
    items = spec["items"] if "items" in spec else spec.get("prompts", [])
    print("=== anima evaluate --dump-hidden — ρ·weave / γ binding-lane probe (H_9235) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d prompts · T=%d right-align · read-only trunk penultimate)" %
          (spec_path, len(items), T))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    d = int(W["d"])
    # H_9611 --gn-freeze <ref>: pin every GN's mu/var to the constants this ONE reference
    # forward produces, making the normalizer input-independent ⟹ the trunk is strictly
    # RF-local (the sequence-global GN bus of H_9560 is deleted, affine untouched). The
    # reference is an explicit argument and is pre-registered by the card — NEVER swept.
    gn_ref = evaluate_strval(argv[1:], "--gn-freeze", "")
    if gn_ref:
        if os.path.exists(gn_ref):
            gn_ref = open(gn_ref, "r").read()
        stats = clm.gn_freeze_calibrate(W, clm._seed_to_tok(gn_ref, T), T)
        clm.gn_freeze_set(stats)
        print("  [gn-freeze] ON — %d GN sites pinned from ref (%d bytes · pre-registered, not swept)"
              % (len(stats), len(gn_ref)), flush=True)
    store = {}
    n_done = 0
    for it in items:
        pid = str(it["id"]); prompt = it["prompt"]
        tok = clm._seed_to_tok(prompt, T)
        if with_logits:                                 # yn + base (lane-OFF) logits in ONE forward
            yn, lg = clm.clm_forward_hidden_logits(W, tok, T)
            store[pid + "__logits"] = lg[T - 1].astype(np.float32)
        else:
            yn = clm.clm_forward_hidden(W, tok, T)      # [T, d] float64 (pre-slot trunk penultimate)
        store[pid + "__seq"] = yn.astype(np.float32)
        store[pid + "__mean"] = yn.mean(axis=0).astype(np.float32)
        store[pid + "__last"] = yn[T - 1].astype(np.float32)
        n_done += 1
        if n_done % 25 == 0:
            print("  [dump #%d/%d] %s" % (n_done, len(items), pid), flush=True)
    # positive-control distinguishability (verdict-integrity clm-decode-py-2): if the FIRST
    # two DISTINCT-concept prompts collapse to near-identical hiddens, a blind verdict is
    # suspect (hexa/py conditioning skew), NOT a clean atom-blindness result.
    pc = ""
    if len(items) >= 2:
        a = store[str(items[0]["id"]) + "__mean"]; b = store[str(items[1]["id"]) + "__mean"]
        cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
        pc = "poscontrol cos(%s,%s)=%.4f %s" % (items[0]["id"], items[1]["id"], cos,
             "(⚠ near-identical → suspect conditioning collapse, NOT blind)" if cos > 0.999 else "(distinct ✓)")
        print("  " + pc, flush=True)
    np.savez_compressed(out_path, **store)
    print(json.dumps({"ckpt": ckpt, "d": d, "T": T, "n": len(items),
                      "out": out_path, "poscontrol": pc}, ensure_ascii=False))
    return 0


def _addr_census_core(H, K, W_q_seeds, rng):
    """The admissible geometry census, shared by the real-dump path and the selftest.

    H       : (N, d)   penultimate __last per entity (real dump OR planted).
    K       : (S, d_k) the entity-keys K[i]=_entity_key(key_emb, e_i).
    W_q_seeds : int    number of RANDOM W_q(d->d_k) projections to average over.
    Returns {obs, ped, delta, verdict} where obs/ped are argmax-collision rates.

    For each random W_q: q = H @ W_q -> (N, d_k); slot(e)=argmax_i q_e . K[i]; the
    COLLISION rate = 1 - (#distinct slots hit)/N. The PEDESTAL is the SAME statistic on
    RANDOM-gaussian H (zero entity structure, norm-matched) — this is the zero-truth arm
    (phi-estimator-needs-zero-truth-pedestal) and it absorbs the key-norm argmax bias that
    makes an ANALYTIC uniform-birthday baseline wrong. Signal = ped - obs (real H collides
    LESS than structureless H) ⇒ the geometry carries an injective entity code random W_q
    preserves. NO target_slot / correctness is ever read (Sol admissibility)."""
    import numpy as np
    N, d = H.shape
    S, d_k = K.shape

    def _excess(Hx):
        hn = float(np.sqrt((Hx * Hx).sum(axis=1).mean()) + 1e-9)   # match pedestal to THIS H's norm

        def _collision(Hy):
            c = 0.0
            for s in range(W_q_seeds):
                Wq = rng.standard_normal((d, d_k)) / np.sqrt(d)
                slot = np.argmax((Hy @ Wq) @ K.T, axis=1)          # (N,) nearest entity-key
                c += 1.0 - (len(set(slot.tolist())) / float(N))
            return c / W_q_seeds
        o = _collision(Hx)
        p = _collision(rng.standard_normal((N, d)) / np.sqrt(d) * hn)
        return o, p

    # RAW h at the query position is DOMINATED by the shared prompt template ("is/not {e} => "),
    # so distinct entities are positively correlated and collide MORE than orthogonal noise — a raw
    # KILL mostly reports "template occupies the penultimate", NOT "the entity code is collapsed".
    # The DECONFOUNDED signal removes the grand mean (the shared template component) and asks whether
    # the ENTITY-specific residual is collapsed. The verdict reads the CENTERED excess.
    obs_r, ped_r = _excess(H)
    Hc = H - H.mean(axis=0, keepdims=True)
    obs_c, ped_c = _excess(Hc)
    shared_frac = float(np.linalg.norm(H.mean(axis=0)) / (np.sqrt((H * H).sum(axis=1).mean()) + 1e-9))
    ex_r, ex_c = obs_r - ped_r, obs_c - ped_c
    # SCREENER (DIRECTIONAL · NECESSARY-not-sufficient). Birthday-bounded when n_slot=n_entities:
    # obs << ped is UNREACHABLE, so this can only detect COLLAPSE (obs >> ped), never confirm
    # emergence. KILL = the CENTERED entity residual is collapsed (sharp-init has a degenerate
    # substrate); PASS-screen = non-degenerate residual (necessary only — the emergence verdict is
    # the 303M fire). The raw excess is reported for transparency but does NOT drive the verdict.
    verdict = "KILL" if ex_c > 0.05 else "PASS-screen"
    return {"obs": obs_c, "ped": ped_c, "excess": ex_c, "verdict": verdict, "N": N, "S": S,
            "obs_raw": obs_r, "ped_raw": ped_r, "excess_raw": ex_r, "shared_frac": shared_frac}


def store_parity_selftest_run(argv):
    """`anima-py evaluate --store-parity-selftest [--parity-tol 2e-5]` — the H_9826 torch<->numpy
    CLMS parity guard, ported from lab/v2's gradcheck --selftest discipline.

    The store lane exists TWICE — CLMSModule.forward (torch, trains it) and store_apply (numpy,
    serves it) — and they were kept in step by a COMMENT alone. This runs both on one random
    module and asserts they agree, then resamples each weight tensor in turn and asserts every
    divergence is CAUGHT, so the guard is known to be able to fail.

    Needs torch (the `[train]` extra). On a numpy-only install it reports SKIPPED and returns 3 —
    never a PASS, because an unrun guard that prints success is the failure mode this exists to
    prevent."""
    tol = float(evaluate_strval(argv[1:], "--parity-tol", "2e-5") or "2e-5")
    print("=== anima evaluate --store-parity-selftest — H_9826 torch<->numpy CLMS parity ===")
    import clms as _clms
    fn = getattr(_clms, "parity_selftest", None)
    if fn is None:
        print("  SKIPPED — torch is not installed, so the trainer arm cannot run.")
        print("  This is NOT a pass. Install the train extra:  pip install \"anima-python[train]\"")
        return 3
    ok, rows = fn(tol=tol, verbose=True)
    print("  SELFTEST %s — the mirror %s the trainer, and the guard %s catch a divergence" %
          ("PASS ✓" if ok else "FAIL ✗",
           "MATCHES" if ok else "DIVERGES FROM",
           "DOES" if ok else "does NOT"))
    print(json.dumps({"tol": tol, "ok": bool(ok),
                      "rows": [{"arm": r[0], "value": r[1], "caught": r[2]} for r in rows]},
                     ensure_ascii=False))
    return 0 if ok else 1


def _retr_probe_core(H, K, tr, te, iters=1200, lr=0.05, seed=0):
    """Bridge-FAITHFUL slot-retrieval probe (H_9825 · ported from lab/v2 probe_decode.py:84).

    Fits ONLY a linear query map W(d -> d_k) — exactly store_apply's q = h @ W_q — such that
    softmax((h@W) . K[i] / sqrt(d_k)) picks the entity's own key out of the pool. This is the
    RETRIEVAL half a bolt-on bridge must form on a FROZEN trunk, isolated from the readout and
    the operator gate, so it answers "can this trunk be addressed AT ALL" with a CEILING rather
    than a pass/fail. Distinct from --store-addr-census, which is a random-W_q geometry screener
    and reads no target at all.

    H  : (N, d)   penultimate __last per entity.
    K  : (N, d_k) entity-keys K[i] = _entity_key(key_emb, e_i); entity i's target IS index i.
    tr/te : disjoint index arrays. W is fit on the tr entities scored against the tr keys ONLY,
        then read on the te entities against the te keys — so the number is GENERALIZING
        content-addressing, never a memorized row. Chance is DERIVED from the realized test
        pool (1/len(te)), never assumed (chance-level-must-be-derived-per-metric).
    Returns {acc, chance, n_train, n_test}."""
    import numpy as np
    d = H.shape[1]
    d_k = K.shape[1]
    Htr, Ktr = H[tr], K[tr]
    Hte, Kte = H[te], K[te]
    n = len(tr)
    scale = 1.0 / np.sqrt(d_k)
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((d, d_k)) * 0.02
    m = np.zeros_like(W); v = np.zeros_like(W)
    b1, b2, eps = 0.9, 0.999, 1e-8
    Yoh = np.eye(n)
    for t in range(1, iters + 1):
        q = Htr @ W                                  # (n, d_k)
        logits = (q @ Ktr.T) * scale                 # (n, n) == the bridge's attention logits
        z = logits - logits.max(axis=1, keepdims=True)
        P = np.exp(z); P /= P.sum(axis=1, keepdims=True)
        dlog = (P - Yoh) / n * scale                 # (n, n)
        g = Htr.T @ (dlog @ Ktr)                     # (d, d_k)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * (g * g)
        W -= lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)
    S = (Hte @ W) @ Kte.T
    pred = S.argmax(axis=1)
    acc = float((pred == np.arange(len(te))).mean())
    # 1-indexed rank of each entity's OWN key among all test keys. Retained so an n-way read
    # matched to the live lane's n_slot can be derived in CLOSED FORM from the SAME fitted W
    # (see _nway_from_ranks) — a re-read of this estimate, never a second estimate.
    own = S[np.arange(len(te)), np.arange(len(te))][:, None]
    ranks = (S > own).sum(axis=1) + 1
    return {"acc": acc, "chance": 1.0 / float(len(te)), "n_train": int(n), "n_test": int(len(te)),
            "ranks": ranks.astype(int)}


def _nway_from_ranks(ranks, n_te, m):
    """Exact expected m-way accuracy from the full-pool rank vector — the probability that all
    m−1 distractors, drawn uniformly without replacement from the other n_te−1 test entities,
    rank BELOW the target:  mean_i C(n_te − r_i, m−1) / C(n_te − 1, m−1).

    This is not an approximation of a sampled group procedure: m-way argmax is subset-argmax of
    the same score row, so the closed form IS the expectation over draws — zero sampling variance,
    no seed, no group roster to freeze, and the fitted W stays byte-identical to the full-pool fire.

    Chance is DERIVED, not assumed: under uniform ranks the expression evaluates to exactly 1/m
    (verified numerically at n_te=64, m=8 → 0.1250000000)."""
    from math import comb
    if m < 2 or m > n_te:
        raise ValueError("_nway_from_ranks: need 2 <= m <= n_test (got m=%d, n_test=%d)" % (m, n_te))
    denom = comb(n_te - 1, m - 1)
    tot = 0.0
    for r in ranks:
        tot += comb(n_te - int(r), m - 1) / denom if (n_te - int(r)) >= (m - 1) else 0.0
    return float(tot / len(ranks))


def _gram_nway(K, te, m):
    """The EXACT-W reference: with W = R⁺ the ORACLE score matrix reduces to the key Gram K·Kᵀ,
    so m-way accuracy on the key codebook ALONE — no fit, no dump, no seed — upper-bounds what
    any estimator could reach on these keys.

    It splits the two ways an ORACLE can fail. Gram ≥ bar with a fitted ORACLE below it means the
    codebook is fine at this cardinality and the shortfall is ESTIMATION. Gram below the bar means
    no fit quality can save it: `_entity_key` is a degenerate address function at the cardinality
    the lane actually uses, which is a substrate result about the addressing scheme rather than a
    dead instrument."""
    import numpy as np
    Kt = K[te]
    S = Kt @ Kt.T
    own = S[np.arange(len(te)), np.arange(len(te))][:, None]
    ranks = (S > own).sum(axis=1) + 1
    return _nway_from_ranks(ranks.astype(int), len(te), m)


def _retr_probe_split(N, rng):
    """Disjoint half/half entity split (the held-out pool the ceiling is read on)."""
    import numpy as np
    idx = rng.permutation(N)
    cut = N // 2
    return np.sort(idx[:cut]), np.sort(idx[cut:])


def _retr_probe_center(H, tr, mode):
    """Deconfound the shared prompt-template component (H_9719 정정 ③ measured it at 95% of the
    hidden norm on a base lineage, 57% on t3), using the TRAIN half's mean only so no test-half
    statistic enters the estimator.

    Asymmetry that makes this the verdict arm rather than a cosmetic step: writing h_j = c + r_j,
    the probe's logit gains a term (c@W)·K_i that is ROW-CONSTANT and key-indexed. It therefore
    cannot fake REACHABLE — a row-constant bias pulls every row toward the same keys, while a
    correct held-out argmax needs row-differential signal, and the entity split leaves the probe no
    per-class bias to exploit (test keys are disjoint). But it CAN fake FLOOR: the fit only nulls c
    at convergence, and when ‖c‖ dominates the hidden norm the gradient is spent managing the
    nuisance direction while a readable residual is swamped. So raw is a trustworthy positive and an
    unreliable negative — and FLOOR is a live outcome here. Centering leaves mean(r_tr), again
    row-constant, so it cannot manufacture REACHABLE either."""
    if mode == "none":
        return H
    if mode != "train-mean":
        raise ValueError("--retr-probe-center must be 'none' or 'train-mean' (got %r)" % mode)
    return H - H[tr].mean(axis=0, keepdims=True)


def store_retr_probe_run(argv):
    """`anima-py evaluate <ckpt> --store-retr-probe <dump.npz> [--retr-probe-iters 1200]`
    — the H_9825 bridge-faithful slot-retrieval CEILING, engine-native.

    Reports the fitted-W held-out retrieval accuracy together with TWO controls that decide
    whether the number is readable at all:
      · NULL (zero-truth pedestal) — structureless norm-matched H. A probe that scores above
        chance here is manufacturing retrieval, and the live arm is unreadable.
      · ORACLE (positive control) — H planted as a linear image of K, so an exact W exists. A
        probe that fails here is INSTRUMENT-DEAD and no negative may be read from it
        (positive-control-before-reading-a-negative).
    DIRECTIONAL: a ceiling on what a bolt-on could reach on this frozen trunk; it never cements.

    --retr-probe-selftest: no ckpt/dump — asserts ORACLE reaches the bar and NULL stays at
    chance on planted geometry, i.e. that this instrument CAN fail. $0 on mini."""
    import numpy as np
    iters = evaluate_intval(argv[1:], "--retr-probe-iters", 1200)
    center = evaluate_strval(argv[1:], "--retr-probe-center", "none") or "none"
    nway = evaluate_intval(argv[1:], "--retr-probe-nway", 0)
    rng = np.random.default_rng(29825)

    def _arms(H, K, tag):
        tr, te = _retr_probe_split(len(H), rng)
        hn = float(np.sqrt((H * H).sum(axis=1).mean()) + 1e-9)
        Hnull = rng.standard_normal(H.shape) / np.sqrt(H.shape[1]) * hn
        R = rng.standard_normal((K.shape[1], H.shape[1])) / np.sqrt(K.shape[1])
        Horc = (K @ R) * hn / (np.sqrt(((K @ R) ** 2).sum(axis=1).mean()) + 1e-9)

        def _triple(mode):
            # every arm goes through the IDENTICAL centering path, so the frozen ORACLE/NULL
            # gates certify the estimator actually used for the verdict
            f = lambda X: _retr_probe_core(_retr_probe_center(X, tr, mode), K, tr, te,
                                           iters=iters, seed=7)
            return f(H), f(Hnull), f(Horc)

        raw = _triple("none")
        cen = _triple(center) if center != "none" else raw
        # key-permute: same H, keys shuffled across entities. Destroys the content-address
        # correspondence while preserving every norm/geometry statistic the Gaussian NULL changes.
        # REPORTED CONTROL, never a gate (the frozen table is untouched).
        kp_idx = rng.permutation(len(K))
        kperm = _retr_probe_core(_retr_probe_center(H, tr, center), K[kp_idx], tr, te,
                                 iters=iters, seed=7)
        shared = float(np.linalg.norm(H.mean(axis=0)) / (np.sqrt((H * H).sum(axis=1).mean()) + 1e-9))
        print("  [%s] n_train=%d n_test=%d  chance=%.4f  shared-template=%.1f%% of hidden norm" %
              (tag, raw[0]["n_train"], raw[0]["n_test"], raw[0]["chance"], 100.0 * shared))
        print("    %-38s raw=%.4f  centered=%.4f   [positive control]"
              % ("ORACLE (planted linear-reachable)", raw[2]["acc"], cen[2]["acc"]))
        print("    %-38s raw=%.4f  centered=%.4f   [zero-truth pedestal]"
              % ("NULL   (structureless H)", raw[1]["acc"], cen[1]["acc"]))
        print("    %-38s raw=%.4f  centered=%.4f   [CEILING · DIRECTIONAL]"
              % ("LIVE   (this trunk)", raw[0]["acc"], cen[0]["acc"]))
        print("    %-38s          centered=%.4f   [reported control · not a gate]"
              % ("KEY-PERMUTE (address correspondence cut)", kperm["acc"]))
        print("    verdict arm = %s" % ("centered(train-mean)" if center != "none" else "raw"))
        nw = None
        if nway:
            n_te = cen[0]["n_test"]
            nw = {"m": nway,
                  "chance": 1.0 / float(nway),
                  "oracle": _nway_from_ranks(cen[2]["ranks"], n_te, nway),
                  "null": _nway_from_ranks(cen[1]["ranks"], n_te, nway),
                  "live": _nway_from_ranks(cen[0]["ranks"], n_te, nway),
                  "kperm": _nway_from_ranks(kperm["ranks"], n_te, nway),
                  "gram": _gram_nway(K, te, nway),
                  # ADVERSARIAL bound: give every target the m−1 HIGHEST-scoring distractors, i.e.
                  # the hardest block that could ever be drawn against it. Winning that block means
                  # beating every competitor, so it is EXACTLY rank==1 — the full-pool top-1 rate,
                  # free of charge and with no extra fit. It brackets the uniform read from below;
                  # no block generator that cannot see h can do worse than this.
                  "adv": float((cen[0]["ranks"] == 1).mean())}
            print("  [%s · %d-way re-read matched to the live lane] chance=%.4f  (closed form over "
                  "the SAME fitted W — no resampling, no seed)" % (tag, nway, nw["chance"]))
            print("    ORACLE %.4f   GRAM-exact-W %.4f   NULL %.4f   KEY-PERMUTE %.4f   LIVE %.4f"
                  % (nw["oracle"], nw["gram"], nw["null"], nw["kperm"], nw["live"]))
            print("    LIVE bracket: adversarial(hardest block) %.4f  <=  uniform %.4f   "
                  "[the manifest draws slots uniformly — cli/corpus.py _sb_emit_block rng.sample — "
                  "so `uniform` is the in-vivo-faithful arm and `adversarial` is the worst case]"
                  % (nw["adv"], nw["live"]))
        return cen[0], cen[1], cen[2], raw, shared, nw

    if "--retr-probe-selftest" in argv:
        print("=== --store-retr-probe SELFTEST (planted geometry · no ckpt) ===")
        N, d, d_k = 64, 256, 32
        Kp = rng.standard_normal((N, d_k))
        Hp = rng.standard_normal((N, d))          # structureless live arm: must read at chance
        live, null, orc, _raw, _sh, _nw = _arms(Hp, Kp, "selftest")
        ok_pos = orc["acc"] >= 0.90
        ok_null = null["acc"] <= max(4.0 * null["chance"], 0.15)
        ok = ok_pos and ok_null
        print("  ORACLE>=0.90 %s · NULL<=max(4x chance,0.15) %s" %
              ("PASS" if ok_pos else "FAIL", "PASS" if ok_null else "FAIL"))
        print("  SELFTEST %s — the probe %s separate reachable from structureless geometry" %
              ("PASS ✓" if ok else "FAIL ✗", "DOES" if ok else "does NOT"))
        return 0 if ok else 1

    dump_path = evaluate_strval(argv[1:], "--store-retr-probe", "")
    ckpt = argv[0]
    print("=== anima evaluate --store-retr-probe — H_9825 bridge-faithful retrieval ceiling ===")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt); return 1
    cl = W.get("clms")
    if cl is None:
        print("ERROR: ckpt has no CLMS trailer — the probe needs key_emb (use a store-trailer ckpt)")
        return 2
    import clms as _clms
    key_emb = cl["key_emb"]
    npz = np.load(dump_path, allow_pickle=False)
    ents = sorted({k[:-6] for k in npz.files if k.endswith("__last")})
    if len(ents) < 8:
        print("ERROR: dump has %d entities — the held-out half needs >=4, so >=8 total" % len(ents))
        return 2
    H = np.stack([npz[e + "__last"].astype(np.float64) for e in ents])   # (N, d)
    K = np.stack([_clms._entity_key(key_emb, e) for e in ents])          # (N, d_k)
    print("  n_entities=%d  d=%d  d_k=%d  iters=%d" % (len(ents), H.shape[1], K.shape[1], iters))
    live, null, orc, raw, shared, nw = _arms(H, K, "ckpt")
    if nw is not None:
        # SAME frozen table, applied to the arm matched to the live lane's cardinality. The
        # constants are chance-relative, so nothing is re-frozen: ORACLE 0.90 · INVALID
        # max(4*chance,0.15) · FLOOR max(2*chance,0.15).
        orc, null, live = ({"acc": nw["oracle"], "chance": nw["chance"]},
                           {"acc": nw["null"], "chance": nw["chance"]},
                           {"acc": nw["live"], "chance": nw["chance"]})
    if orc["acc"] < 0.90:
        verdict = "INSTRUMENT-DEAD"
    elif null["acc"] > max(4.0 * null["chance"], 0.15):
        verdict = "INVALID"
    elif live["acc"] <= max(2.0 * live["chance"], 0.15):
        verdict = "FLOOR"
    else:
        verdict = "REACHABLE"
    print("  → %s   [DIRECTIONAL ceiling · never cements · the verdict is the 303M fire]" % verdict)
    if nw is not None and nw["null"] > 2.0 * nw["chance"] and verdict != "INVALID":
        print("  ⚠ NULL %.4f is >2x chance yet under the frozen gate (%.2f) — the gate is nearly "
              "vacuous at this cardinality; read the live number with that in mind."
              % (nw["null"], max(4.0 * nw["chance"], 0.15)))
    print(json.dumps({"ckpt": ckpt, "dump": dump_path, "n": len(ents), "chance": live["chance"],
                      "center": center, "shared_template_frac": shared,
                      "live": live["acc"], "null": null["acc"], "oracle": orc["acc"],
                      "live_raw": raw[0]["acc"], "null_raw": raw[1]["acc"], "oracle_raw": raw[2]["acc"],
                      "nway": nw,
                      "verdict": verdict}, ensure_ascii=False))
    return 0


# ── H_9838 · CA3 multi-step transitive completion (ckpt-FREE · READ-SIDE ONLY) ─────────
# WHY THIS EXISTS: core/hippo_lane.py (H_9129 rung-3) already ships the CA3
# heteroassociative store whose completion loop is, by construction, transitive chaining —
# but nothing ever MEASURED it. The one question recombination needs answered is: with a
# store built from A→B and B→C ONLY, does completion recover A→C above chance? That is the
# operation CE (next-byte) cannot supply, and it is answerable at $0 with no checkpoint
# because the store + completion are arch-independent numpy arithmetic (no torch, no FFI).
#
# STRICTLY READ-SIDE (a_substrate_disjoint: separation = preservation). hippo_lane's header
# states it is a READ-ONLY relatedness readout that never mutates the emit-drive lane
# (Ψ / motivation / recall_thr / generator). This selftest imports its three pure functions
# and prints; it opens NO write path into emit-drive and touches no frozen bar. The card's
# other half — feeding completed pairs back as an auxiliary TRAINING target (`train
# --hippo-aux`) — is deliberately NOT landed here: that is the arm that would create the
# write path, and it may not be built before this read-side number says the completion is
# worth carrying at all.
def _hippo_world(n_chains, chain_len, dim, active, seed):
    """The PREMISE world: n_chains DISJOINT directed chains of chain_len items each, coded
    by hippo_lane's deterministic integer fixture (no float RNG, byte-stable).

    Only ADJACENT edges are ever stored, so every hop>=2 pair is a relation the store was
    never told — exactly the A→B, B→C ⊢ A→C setting. Chains are disjoint so reachability
    is chain-local and a distractor drawn from another chain is PROVABLY unreachable."""
    import hippo_lane as HL
    codes = HL.fixture_codes(n_chains * chain_len, dim, active, seed)
    edges = [(c * chain_len + p, c * chain_len + p + 1)
             for c in range(n_chains) for p in range(chain_len - 1)]
    return codes, edges


def _hippo_arm(codes, edges, dim, hops, kwta, n_chains, chain_len, shuffle_rng=None, steps=None):
    """One arm: for every source i, rank the TRUE hops-away target against the pool of
    cross-chain (unreachable) items by CA3 completion overlap.

    DV = top-1 with EXPLICIT tie handling: a target tied with t−1 others at the top scores
    1/t, so a store that says nothing (every overlap 0 ⇒ everything ties) reads EXACTLY the
    derived chance 1/pool instead of a spurious 0 or 1. Chance is derived from the realized
    pool, never assumed (chance-level-must-be-derived-per-metric).

    shuffle_rng != None = the VALUE-SHUFFLED store pedestal: the same edge count and the same
    code multiset, but each edge's target code is reassigned, so the store is structure-free
    while every norm/sparsity statistic is preserved.

    steps != None truncates the completion loop below the hop distance. steps=1 against a
    hops>=2 query is the CHAINING lesion: the target is then unreachable by construction, so
    anything the arm still recovers is code geometry rather than transitive completion."""
    import numpy as np
    import hippo_lane as HL
    N = n_chains * chain_len
    ed = edges
    if shuffle_rng is not None:
        perm = shuffle_rng.permutation(N)
        while bool((perm == np.arange(N)).all()):
            perm = shuffle_rng.permutation(N)
        ed = [(cur, int(perm[nxt])) for cur, nxt in edges]
    W = HL.hippo_build_store(codes, ed, dim)
    hits, npool = [], 0
    for c in range(n_chains):
        for p in range(chain_len - hops):
            i = c * chain_len + p
            pool = [i + hops] + [x for x in range(N) if x // chain_len != c]
            s = [HL.hippo_relatedness(W, codes, i, x, steps or hops, kwta) for x in pool]
            top = max(s)
            ties = sum(1 for v in s if v >= top - 1e-12)
            hits.append(1.0 / ties if s[0] >= top - 1e-12 else 0.0)
            npool = len(pool)
    return {"acc": float(sum(hits) / len(hits)), "chance": 1.0 / float(npool),
            "n_queries": len(hits), "pool": npool}


def _hippo_battery(n_chains, chain_len, seeds, geoms, kwta_f, hop_list):
    """Run every arm over seeds x geometries at ONE store load, and reduce to the conservative
    headline: MIN over configs for the positive/treatment arms, MAX for the pedestals. A number
    that survives only at one seed or one code density is therefore unreportable."""
    import numpy as np
    rows = []
    for sd in seeds:
        for (dm, ac) in geoms:
            codes, edges = _hippo_world(n_chains, chain_len, dm, ac, sd)
            k = kwta_f or ac
            r = {"cfg": {"seed": sd, "dim": dm, "active": ac, "kwta": k},
                 "pos": _hippo_arm(codes, edges, dm, 1, k, n_chains, chain_len),
                 "ped1": _hippo_arm(codes, edges, dm, 1, k, n_chains, chain_len,
                                    shuffle_rng=np.random.default_rng(9838 + sd)),
                 "hop": {}}
            for h in hop_list:
                r["hop"][h] = {
                    "treat": _hippo_arm(codes, edges, dm, h, k, n_chains, chain_len),
                    "ped": _hippo_arm(codes, edges, dm, h, k, n_chains, chain_len,
                                      shuffle_rng=np.random.default_rng(9838 + sd + h)),
                    "kwta_off": _hippo_arm(codes, edges, dm, h, dm, n_chains, chain_len),
                    "one_step": _hippo_arm(codes, edges, dm, h, k, n_chains, chain_len, steps=1),
                }
            rows.append(r)
    chance = rows[0]["pos"]["chance"]
    pos_min = min(r["pos"]["acc"] for r in rows)
    ped_max = max(max(r["ped1"]["acc"], max(r["hop"][h]["ped"]["acc"] for h in hop_list))
                  for r in rows)
    inv_bar, floor_bar = max(4.0 * chance, 0.15), max(2.0 * chance, 0.15)
    status = ("INSTRUMENT-DEAD" if pos_min < 0.90 else
              "INVALID" if ped_max > inv_bar else "CERTIFIED")
    return {"n_chains": n_chains, "n_items": n_chains * chain_len,
            "n_edges": n_chains * (chain_len - 1), "pool": rows[0]["pos"]["pool"],
            "chance": chance, "positive_min": pos_min, "pedestal_max": ped_max,
            "invalid_bar": inv_bar, "floor_bar": floor_bar, "status": status,
            "hops": {h: {"treat_min": min(r["hop"][h]["treat"]["acc"] for r in rows),
                         "treat_max": max(r["hop"][h]["treat"]["acc"] for r in rows),
                         "kwta_off_max": max(r["hop"][h]["kwta_off"]["acc"] for r in rows),
                         "one_step_max": max(r["hop"][h]["one_step"]["acc"] for r in rows)}
                     for h in hop_list},
            "per_config": [{"cfg": r["cfg"], "pos": r["pos"]["acc"], "ped1": r["ped1"]["acc"],
                            "hop": {str(h): {"treat": r["hop"][h]["treat"]["acc"],
                                             "ped": r["hop"][h]["ped"]["acc"],
                                             "kwta_off": r["hop"][h]["kwta_off"]["acc"],
                                             "one_step": r["hop"][h]["one_step"]["acc"]}
                                    for h in hop_list}} for r in rows]}


def hippo_transitive_selftest_run(argv):
    """`anima-py evaluate --hippo-transitive-selftest [--hippo-hops H] [--hippo-kwta-k K]
    [--hippo-seed S] [--hippo-dim D] [--hippo-active A] [--hippo-chains C]
    [--hippo-chain-len L] [--out j.json]` — H_9838, core/hippo_lane.py CA3 completion.

    ARM ORDER IS FROZEN AND SEQUENTIAL (positive-control-before-reading-a-negative):
      ① POSITIVE CONTROL — hops=1, i.e. the pairs the store was literally built from. If
         completion cannot recover THOSE, the instrument is dead and no negative may be read
         from it: INSTRUMENT-DEAD, and the treatment row is NOT printed.
      ② ZERO-TRUTH PEDESTAL — the value-shuffled store (same edge count, same code multiset,
         targets reassigned). If it fires there the readout is manufacturing relatedness:
         INVALID, and the treatment row is NOT printed.
      ③ TREATMENT — hops>=2, pairs never stored. TRANSITIVE vs FLOOR against derived chance.
      ④ MECHANISM LESIONS (reported, not gates) — ④a ONE-STEP: the identical query with the
         completion truncated to a single step, so the hops>=2 target is unreachable BY
         CONSTRUCTION; this is what isolates transitive CHAINING from the code geometry.
         ④b kWTA OFF (k = full width): removes the sparse pattern separation. Each prints its
         collapse-Δ against the treatment and a `causal` flag (lesion at/below the floor bar
         while the treatment is above it).

    WHY THE LOAD LADDER EXISTS (measured 2026-07-21, and it is the reason this is not a
    single-config battery): a heteroassociative store has a CAPACITY. At 8 chains x 4 items
    (32 items / 24 edges) the positive control reads min=0.8750 across seeds x geometries —
    BELOW the 0.90 bar — because code crosstalk, not the completion rule, limits recovery.
    Reading a transitive number there would be reading an over-capacity store. Reading it at a
    hand-picked lighter load would be tune-to-green. So the flag sweeps a LOAD LADDER and reads
    the treatment at the LARGEST load whose POSITIVE CONTROL still fires — the hardest
    certifying point, chosen by the control arm and never by the treatment number. The whole
    ladder (including the loads that fail) is printed and emitted.

    NO TUNE-TO-GREEN elsewhere either: within a load the battery runs 3 frozen seeds x 3
    geometries and the headline is the MIN over all of them for the positive/treatment arms and
    the MAX for the pedestals, so a lift that lives at one seed or one code density cannot be
    reported (H_9844 caught exactly this failure mode with block size). Passing an explicit knob
    (--hippo-dim/--hippo-active/--hippo-kwta-k/--hippo-seed/--hippo-chains) COLLAPSES the sweep
    to that config and the emitted JSON marks robust=false — a hand-picked config is a probe.

    $0: pure numpy, no ckpt, no GPU, no corpus. DIRECTIONAL — it measures the store lane's own
    arithmetic on a planted world, so it bounds what CA3 completion CAN do, never what a
    trained 303M does (a_toy_scale_recheck)."""
    hops_f = evaluate_intval(argv, "--hippo-hops", 0)
    dim_f = evaluate_intval(argv, "--hippo-dim", 0)
    act_f = evaluate_intval(argv, "--hippo-active", 0)
    kwta_f = evaluate_intval(argv, "--hippo-kwta-k", 0)
    seed_f = evaluate_intval(argv, "--hippo-seed", 0)
    chains_f = evaluate_intval(argv, "--hippo-chains", 0)
    chain_len = evaluate_intval(argv, "--hippo-chain-len", 4)
    out_path = evaluate_strval(argv, "--out", "")

    dim0, act0 = dim_f or 256, act_f or 8
    seeds = (seed_f,) if seed_f else (7, 11, 20260721)
    geoms = ([(dim0, act0)] if (dim_f or act_f)
             else [(dim0, act0), (dim0 // 2, act0), (dim0, act0 * 2)])
    ladder = [chains_f] if chains_f else [2, 4, 8]
    robust = not (seed_f or dim_f or act_f or kwta_f or chains_f)
    hop_list = [hops_f] if hops_f else [h for h in (2, 3) if h <= chain_len - 1]
    if chain_len < 2 or min(ladder) < 2 or not hop_list:
        print("--hippo-transitive-selftest: need --hippo-chains>=2, --hippo-chain-len>=2 and a "
              "hop <= chain_len-1 (got chains=%s len=%d hops=%s)" % (ladder, chain_len, hop_list))
        return 2

    print("=== --hippo-transitive-selftest — H_9838 CA3 multi-step completion "
          "(core/hippo_lane.py, H_9129 rung-3) ===")
    print("  premise world: N disjoint chains x %d items, ONLY adjacent edges stored — every "
          "hops>=2 pair is a relation the store was never told." % chain_len)
    print("  seeds=%s · geometries(dim,active)=%s · robust=%s · READ-SIDE ONLY (no write path "
          "into the emit-drive lane)" % (list(seeds), geoms, robust))

    loads = [_hippo_battery(nc, chain_len, seeds, geoms, kwta_f, hop_list) for nc in ladder]
    print("  ① CERTIFICATION LADDER — the treatment is read at the LARGEST certifying load; "
          "the load is picked by the CONTROL arms, never by the treatment number.")
    print("    %-6s %-6s %-6s %-7s | %-22s | %-24s | %s"
          % ("items", "edges", "pool", "chance", "STORED hops=1 (min)", "SHUFFLED store (max)",
             "status"))
    for L in loads:
        print("    %-6d %-6d %-6d %-7.4f | %.4f  bar>=0.90 %-4s | %.4f  bar<=%.4f %-4s | %s"
              % (L["n_items"], L["n_edges"], L["pool"], L["chance"],
                 L["positive_min"], "PASS" if L["positive_min"] >= 0.90 else "FAIL",
                 L["pedestal_max"], L["invalid_bar"],
                 "PASS" if L["pedestal_max"] <= L["invalid_bar"] else "FAIL", L["status"]))

    ok = [L for L in loads if L["status"] == "CERTIFIED"]
    if not ok:
        controls = "INVALID" if any(L["status"] == "INVALID" for L in loads) else "INSTRUMENT-DEAD"
        why = ("the value-shuffled store still fires at every load — the readout manufactures "
               "relatedness" if controls == "INVALID" else
               "no load recovers the pairs the store was literally built from, so no negative "
               "may be read from this instrument")
        print("  → controls: %s (%s)" % (controls, why))
        print("    (treatment row REFUSED — an uncertified battery reports no number)")
        verdict_load, hop_out = None, {}
    else:
        verdict_load = max(ok, key=lambda L: L["n_edges"])
        controls = "CERTIFIED"
        why = ("positive control fires and the pedestal refuses at %d items / %d edges (the "
               "largest certifying load)" % (verdict_load["n_items"], verdict_load["n_edges"]))
        print("  → controls: CERTIFIED — reading the treatment at %d items / %d edges "
              "(chance=%.4f, floor bar >%.4f)"
              % (verdict_load["n_items"], verdict_load["n_edges"], verdict_load["chance"],
                 verdict_load["floor_bar"]))
        hop_out = {}
        for h in hop_list:
            hh = verdict_load["hops"][h]
            hv = "TRANSITIVE" if hh["treat_min"] > verdict_load["floor_bar"] else "FLOOR"
            hop_out[str(h)] = {"treat_min": hh["treat_min"], "treat_max": hh["treat_max"],
                               "spread": hh["treat_max"] - hh["treat_min"],
                               "one_step_max": hh["one_step_max"],
                               "chaining_delta": hh["treat_min"] - hh["one_step_max"],
                               "kwta_off_max": hh["kwta_off_max"],
                               "separation_delta": hh["treat_min"] - hh["kwta_off_max"],
                               "floor_bar": verdict_load["floor_bar"], "verdict": hv,
                               "chaining_causal": bool(
                                   hh["one_step_max"] <= verdict_load["floor_bar"]
                                   and hh["treat_min"] > verdict_load["floor_bar"]),
                               "separation_causal": bool(
                                   hh["kwta_off_max"] <= verdict_load["floor_bar"]
                                   and hh["treat_min"] > verdict_load["floor_bar"])}
            print("    %-44s min=%.4f max=%.4f  [③ TREATMENT] → %s"
                  % ("TRANSITIVE hops=%d (never stored)" % h,
                     hh["treat_min"], hh["treat_max"], hv))
            print("    %-44s max=%.4f            [④a chaining lesion · Δ=%+.4f · causal=%s]"
                  % ("  ONE-STEP completion (target unreachable)", hh["one_step_max"],
                     hh["treat_min"] - hh["one_step_max"],
                     hop_out[str(h)]["chaining_causal"]))
            print("    %-44s max=%.4f            [④b separation lesion · Δ=%+.4f · causal=%s]"
                  % ("  kWTA OFF k=full width (no separation)", hh["kwta_off_max"],
                     hh["treat_min"] - hh["kwta_off_max"],
                     hop_out[str(h)]["separation_causal"]))

    res = {"instrument": "hippo-transitive-selftest", "hypothesis": "H_9838",
           "engine": "core/hippo_lane.py (H_9129 rung-3)", "controls": controls, "why": why,
           "read_side_only": True, "robust": robust,
           "world": {"chain_len": chain_len, "load_ladder_chains": ladder,
                     "seeds": list(seeds), "geometries": geoms, "hops": hop_list},
           "verdict_load": (None if verdict_load is None else
                            {"n_items": verdict_load["n_items"], "n_edges": verdict_load["n_edges"],
                             "pool": verdict_load["pool"], "chance": verdict_load["chance"]}),
           "bars": {"positive": 0.90, "invalid": "max(4*chance,0.15)",
                    "floor": "max(2*chance,0.15)"},
           "hops": hop_out, "ladder": loads,
           "reaudit": {"argv": ["anima-py", "evaluate"] + list(argv)},
           "reading": ("Headline = MIN over seeds x geometries for the positive/treatment arms "
                       "and MAX for the pedestals; the load is chosen as the LARGEST one whose "
                       "positive control fires, so neither a seed, a code density nor the store "
                       "load can be picked to favour the treatment. DIRECTIONAL: this is the "
                       "store lane's own arithmetic on a planted premise world — it bounds what "
                       "CA3 completion can do and cements nothing about a trained model. "
                       "READ-SIDE ONLY: no write path into the emit-drive lane is opened "
                       "(a_substrate_disjoint: separation = preservation).")}
    if out_path:
        open(out_path, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=2))
    print(json.dumps(res, ensure_ascii=False))
    return 0 if controls == "CERTIFIED" else (1 if controls == "INSTRUMENT-DEAD" else 3)


def store_addr_census_run(argv):
    """`anima-py evaluate <ckpt> --store-addr-census <dump.npz> [--census-seeds 12]`
    — the H_9719 EMERGENT-ADDRESS $0 pre-screen, engine-native (a_experiment_engine_native).

    Reads a --dump-hidden .npz (penultimate __last per entity) + the ckpt's frozen CLMS
    key_emb/W_q dims, applies K RANDOM W_q(d->d_k) projections, and measures the argmax
    COLLISION of q=h@W_q over the entity-keys K[i]=_entity_key(key_emb, e_i) AGAINST a
    structureless-H pedestal. ADMISSIBLE: reads NO target_slot / slot-correctness / any
    statistic derived from them (Sol's rule) — it measures injectivity of the random-projected
    geometry only. A DIRECTIONAL SCREENER: KILLs sharp-init before any pool spend when the
    geometry carries no injective entity code; it NEVER cements (only 303M engine-native does).

    --store-census-selftest: no ckpt/dump — plants INJECTIVE vs COLLAPSED synthetic geometry
    and asserts the verdict flips (positive-control-before-reading-a-negative). $0 on mini."""
    import numpy as np
    seeds = evaluate_intval(argv[1:], "--census-seeds", 12)
    rng = np.random.default_rng(20719)

    if "--store-census-selftest" in argv:
        print("=== --store-addr-census SELFTEST (planted controls · no ckpt) ===")
        N, d, d_k, S = 48, 256, 32, 48
        Kp = rng.standard_normal((S, d_k))
        tmpl = rng.standard_normal((1, d)) * 3.0            # shared prompt-template component (both arms)
        # POS (non-degenerate): shared template + ISOTROPIC full-rank entity residual → after the
        #   grand-mean is removed the residual is distinct in every direction → argmax spreads.
        Hinj = np.tile(tmpl, (N, 1)) + rng.standard_normal((N, d))
        # NEG (residual-collapse): SAME shared template, but the entity residual collapses onto ONE
        #   direction (collinear scalars × v) — realistic collapse that SURVIVES centering (a merely
        #   all-identical geometry would be nulled by centering and is NOT the failure mode we screen).
        v = rng.standard_normal((1, d))
        Hcol = np.tile(tmpl, (N, 1)) + rng.standard_normal((N, 1)) * v + 1e-2 * rng.standard_normal((N, d))
        rinj = _addr_census_core(Hinj, Kp, seeds, np.random.default_rng(1))
        rcol = _addr_census_core(Hcol, Kp, seeds, np.random.default_rng(2))
        print("  NON-DEGEN(distinct h): centered excess=%+.3f (raw %+.3f) → %s" %
              (rinj["excess"], rinj["excess_raw"], rinj["verdict"]))
        print("  COLLAPSED (shared  h): centered excess=%+.3f (raw %+.3f) → %s" %
              (rcol["excess"], rcol["excess_raw"], rcol["verdict"]))
        ok = rinj["verdict"] == "PASS-screen" and rcol["verdict"] == "KILL"
        print("  SELFTEST %s — census %s discriminate injective from collapsed" %
              ("PASS ✓" if ok else "FAIL ✗", "DOES" if ok else "does NOT"))
        return 0 if ok else 1

    dump_path = evaluate_strval(argv[1:], "--store-addr-census", "")
    ckpt = argv[0]
    print("=== anima evaluate --store-addr-census — H_9719 emergent-address $0 pre-screen ===")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt); return 1
    cl = W.get("clms")
    if cl is None:
        print("ERROR: ckpt has no CLMS trailer — census needs key_emb (use a store-trailer ckpt)")
        return 2
    import clms as _clms
    key_emb = cl["key_emb"]
    npz = np.load(dump_path, allow_pickle=False)
    ents = sorted({k[:-6] for k in npz.files if k.endswith("__last")})
    if len(ents) < 2:
        print("ERROR: dump has <2 entities (%d) — need a held-out entity pool" % len(ents)); return 2
    H = np.stack([npz[e + "__last"].astype(np.float64) for e in ents])   # (N, d)
    K = np.stack([_clms._entity_key(key_emb, e) for e in ents])          # (N, d_k) entity-keys
    r = _addr_census_core(H, K, seeds, rng)
    print("  n_entities=%d  n_slot(keys)=%d  seeds=%d" % (r["N"], r["S"], seeds))
    print("  RAW      collision obs=%.4f ped=%.4f excess=%+.4f  (template-confounded)"
          % (r["obs_raw"], r["ped_raw"], r["excess_raw"]))
    print("  shared-template component = %.1f%% of hidden norm  (grand-mean removed for the verdict)"
          % (100.0 * r["shared_frac"]))
    print("  CENTERED collision obs=%.4f ped=%.4f excess=%+.4f  → %s   [VERDICT]"
          % (r["obs"], r["ped"], r["excess"], r["verdict"]))
    print("  [screener · DIRECTIONAL · NECESSARY-only] verdict reads the CENTERED (deconfounded) "
          "excess — the entity residual, not the template. KILL ⇒ residual collapsed (sharp-init has a "
          "degenerate substrate); PASS-screen ⇒ non-degenerate residual (necessary, NOT emergence — "
          "that is the 303M fire) · admissible(target unread · birthday-bounded when n_slot=N)")
    print(json.dumps({"ckpt": ckpt, "dump": dump_path, "n": r["N"], "excess_centered": r["excess"],
                      "excess_raw": r["excess_raw"], "shared_frac": r["shared_frac"],
                      "verdict": r["verdict"]}, ensure_ascii=False))
    return 0
def _selftest_rho_cells():
    """H_9212 ③ wiring self-test (torch-free · NO decode · reached via an internal subprocess,
    never a heavy eval). Asserts: (1) the aggregate `dets` reuse the FROZEN en objects; (2) en
    cell_dets reuse the IDENTICAL objects (byte-identity: same _rho_fan_words / kwr / ngram /
    corpus tokens / gate 0.70); (3) ko cell_dets dispatch _rho_fan_words_uni + kwr_ko +
    KWR_KO_GATE + uni corpus, and tokenize the ko probe cells NON-EMPTY with the gate applied
    (kwr_ko clears KWR_KO_GATE on real ko); (4) run_panel's aggregate axes are BYTE-IDENTICAL
    with vs without the cell breakout, and the en_general cell's ρ·form/leap/fan equal the
    aggregate's (the en scored path is structurally untouched). Returns (ok, [(name, bool)…])."""
    import rho_axon
    checks = []
    known = _rho_fan_dict_load()
    en_toks = _g_load_corpus_tokens([])   # empty corpus → deterministic empty token list
    dets = {"known": known, "concepts": _rho_fan_concepts(),
            "kwr_fn": _rho_fan_known_word_ratio, "jaccard_fn": _rho_fan_jaccard,
            "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
            "ngram_fn": _g_content_ngrams, "corpus_tokens": en_toks}
    cd = _build_cell_dets(known, en_toks, [])
    # (1) aggregate dets = frozen en objects
    checks.append(("aggregate words_fn IS _rho_fan_words", dets["words_fn"] is _rho_fan_words))
    checks.append(("aggregate kwr_fn IS _rho_fan_known_word_ratio",
                   dets["kwr_fn"] is _rho_fan_known_word_ratio))
    # (2) en cells reuse the IDENTICAL frozen objects + gate 0.70
    for ck in ("en_general", "en_sns"):
        e = cd[ck]
        checks.append((ck + " words_fn IS frozen _rho_fan_words", e["words_fn"] is _rho_fan_words))
        checks.append((ck + " kwr_fn IS frozen _rho_fan_known_word_ratio",
                       e["kwr_fn"] is _rho_fan_known_word_ratio))
        checks.append((ck + " ngram_fn IS frozen _g_content_ngrams",
                       e["ngram_fn"] is _g_content_ngrams))
        checks.append((ck + " corpus_tokens IS the aggregate en tokens",
                       e["corpus_tokens"] is en_toks))
        checks.append((ck + " gate == 0.70 (frozen en bar)", e["kwr_gate"] == 0.70))
        checks.append((ck + " lang == en", e["lang"] == "en"))
    # (3) ko cells dispatch the uni tokenizer + kwr_ko + KWR_KO_GATE, non-empty + gate applied
    for ck in ("ko_general", "ko_sns"):
        k = cd[ck]
        checks.append((ck + " words_fn IS _rho_fan_words_uni", k["words_fn"] is _rho_fan_words_uni))
        checks.append((ck + " kwr_fn IS _rho_fan_ko_known_word_ratio",
                       k["kwr_fn"] is _rho_fan_ko_known_word_ratio))
        checks.append((ck + " gate == KWR_KO_GATE (%.2f)" % KWR_KO_GATE,
                       k["kwr_gate"] == KWR_KO_GATE and KWR_KO_GATE != 0.70))
        checks.append((ck + " ngram_fn IS _g_content_ngrams_uni",
                       k["ngram_fn"] is _g_content_ngrams_uni))
        checks.append((ck + " lang == ko", k["lang"] == "ko"))
        checks.append((ck + " probe cells tokenize NON-EMPTY (uni)",
                       all(len(_rho_fan_words_uni(s)) > 0 for s in k["concepts"])))
        checks.append((ck + " kwr_ko applied: a probe cell clears KWR_KO_GATE",
                       any(k["kwr_fn"](s, known) >= KWR_KO_GATE for s in k["concepts"])))

    # (4) aggregate axes byte-identical with vs without the breakout; en_general cell == aggregate
    class _MockMouth:
        def ideate(self, prompt, gen, maxnew, temp, seed):
            base = prompt.strip().replace(":", "")
            return base + " alpha beta gamma delta epsilon " + str(seed % 7)
    m = _MockMouth()
    a = rho_axon.run_panel(m, [], 40, dets)
    b = rho_axon.run_panel(m, [], 40, dets, cell_dets=cd)
    checks.append(("aggregate axes byte-identical with/without breakout",
                   a["axes"] == b["axes"]))
    checks.append(("breakout present with 4 cells",
                   set((b.get("cells") or {}).keys()) ==
                   {"en_general", "en_sns", "ko_general", "ko_sns"}))
    eng_cell = (b.get("cells") or {}).get("en_general", {}).get("axes", {})
    checks.append(("en_general cell ρ·form == aggregate ρ·form (en path untouched)",
                   eng_cell.get("ρ·form") == a["axes"].get("ρ·form")))
    checks.append(("en_general cell ρ·leap == aggregate ρ·leap",
                   eng_cell.get("ρ·leap") == a["axes"].get("ρ·leap")))
    checks.append(("en_general cell ρ·fan == aggregate ρ·fan",
                   eng_cell.get("ρ·fan") == a["axes"].get("ρ·fan")))
    ok = all(c[1] for c in checks)
    return ok, checks


def _gp_logreg(Xtr, ytr, Xte, l2=10.0, iters=400, lr=0.5):
    """L2 logistic regression, numpy-only (anima-py is pure numpy — no sklearn on the engine
    path). Standardise on the TRAIN split only, then full-batch gradient descent. Deterministic:
    zero init, fixed step count, no shuffling — the same ckpt and manifest give the same bytes."""
    import numpy as np
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0.0] = 1.0
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(A.shape[1]), 0.0
    n = float(len(A))
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(A @ w + b)))
        g = A.T @ (p - ytr) / n + (w / l2)
        w -= lr * g
        b -= lr * float((p - ytr).mean())
    return 1.0 / (1.0 + np.exp(-(B @ w + b)))


def _gp_logreg_batch(Xtr, Ytr, Xte, l2=10.0, iters=400, lr=0.5):
    """The SAME descent as _gp_logreg, run for many label vectors at once.

    The permutation null is ~36k independent fits (200 draws x leave-one-atom-out x 2 arms) and it,
    not the forward, is what pegs a CPU for half an hour per arm while the GPU idles. The draws are
    independent and share one design matrix, so carry W as [d, K] and b as [K]: the descent is
    identical per column. This is the ALGORITHMIC fix convergence evaluate-py-11 prescribed after the
    device fix was rejected — a GPU readout moved the verdict's numbers (V-LIVE 0.808 -> 0.800, perm
    p 0.085 -> 0.120), so speed here must not touch them.

    Ytr: [n, K] label vectors. Returns [K, m] probabilities. Byte-identity with the per-column loop
    is ASSERTED by _selftest_batch_null(), not assumed.
    """
    import numpy as np
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd == 0.0, 1.0, sd)
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    W = np.zeros((A.shape[1], Ytr.shape[1]))
    b = np.zeros(Ytr.shape[1])
    n = float(len(A))
    for _ in range(iters):
        P = 1.0 / (1.0 + np.exp(-(A @ W + b)))
        D = P - Ytr
        W -= lr * (A.T @ D / n + W / l2)
        b -= lr * D.mean(0)
    return (1.0 / (1.0 + np.exp(-(B @ W + b)))).T


def _selftest_batch_null(trials=8):
    """A faster null that shifts a p-value by one draw is a DIFFERENT instrument, so this is not a
    smoke test — it is the licence to use the batch path at all.

    The batch and the loop are NOT bit-identical: BLAS accumulates a matrix-matrix product in a
    different order than a matrix-vector one, which leaves ~1e-16 on the probabilities. What the
    verdict actually consumes is not the probability but its SIGN against 0.5, so the honest question
    is whether that perturbation can flip a decision. It can only do so for a probability lying
    within |delta| of the threshold. So measure both and require the decision margin to dominate:

        max |p_batch - p_loop|   <<   min |p - 0.5|

    If the two agree on every predicted label across the trials AND the margin beats the drift by
    orders of magnitude, the batch path computes the same verdict; if it does not, it is rejected
    and the loop stands (convergence evaluate-py-11 — speed must never touch the numbers)."""
    import numpy as np
    drift, margin, labels_agree = 0.0, 1.0, True
    for t in range(trials):
        rng = np.random.default_rng(t)
        Xtr = rng.normal(size=(90, 512)); Xte = rng.normal(size=(30, 512))
        Y = (rng.random((90, 12)) > 0.5).astype(np.float64)
        batch = _gp_logreg_batch(Xtr, Y, Xte)
        loop = np.stack([_gp_logreg(Xtr, Y[:, k], Xte) for k in range(Y.shape[1])], 0)
        drift = max(drift, float(np.abs(batch - loop).max()))
        margin = min(margin, float(np.abs(loop - 0.5).min()))
        labels_agree &= bool(((batch > 0.5) == (loop > 0.5)).all())
    ok = labels_agree and drift < margin * 1e-3
    return {"max_prob_drift": drift, "min_decision_margin": margin,
            "labels_identical": labels_agree, "safe": ok}


def device_parity_run(argv):
    """`anima-py evaluate <ckpt> --device-parity` — does THIS host's GPU forward equal its CPU one?

    The repo shipped `a_gpu_default_no_optin` on the belief that the GPU decode is byte-identical.
    It is not, and the belief survived because what was checked was the TOKEN STREAM: argmax is
    robust to 1e-14, so a decode can be 'identical' while the hidden underneath is not. Every probe
    (--dump-hidden, --ground-probe, --valence-audit, --interaction-lift) reads that hidden directly.

    So this verb asks the question in the form that matters, and prints the number instead of the
    belief. It runs the same prompts through the device path and through a forced-numpy path and
    reports max|delta| on the hidden. Anything above 0 means: a verdict computed on GPU and one
    computed on CPU are NOT the same measurement, and comparing them is a confound
    (convergence decode-py-4 — it cost us a headline).

    Measured on aiden (RTX 5070, cupy 13.6.0, CUDA 13): max|delta| = 2.487e-14."""
    import numpy as np
    ckpt = argv[0]
    T = evaluate_intval(argv[1:], "--win", 64)
    prompts = ["이 영화 좋다 => ", "배송도 빠르고 가성비는 좋", "별로였어요", "품질이 형편없",
               "재미없지 않다", "완전 만족합니다", "그냥 그래요", "최악이다"]
    print("=== anima evaluate --device-parity — is the GPU forward the same measurement as the CPU one? ===")
    st = clm.gpu_status()
    if not st.get("cuda"):
        print("  this host has no CUDA device (%s) — nothing to compare; the CPU path IS the "
              "reference." % st.get("reason"))
        return 0
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    dev_h = np.stack([np.asarray(clm.clm_forward_hidden(W, clm._seed_to_tok(p, T), T))
                      for p in prompts], 0)

    # The host copy must be built EXPLICITLY. Flipping cuda_available() and re-loading does NOT
    # work: clm_load_weights serves from _WLOAD_CACHE (decode.py: `if _k in _WLOAD_CACHE: return`),
    # so the second load hands back the SAME already-uploaded cupy arrays and the check compares
    # the GPU against itself — it reported a triumphant 0.000e+00 while the true answer was
    # 2.487e-14. A guard that returns a false PASS is worse than no guard: mirror every tensor back
    # to host instead, so the CPU pass is provably on numpy.
    Wc = {k: clm.to_host(v) if hasattr(v, "device") else v for k, v in W.items()}
    Wc = {k: ([clm.to_host(x) if hasattr(x, "device") else x for x in v] if isinstance(v, list)
              else v) for k, v in Wc.items()}
    host_mods = {type(v).__module__ for v in Wc.values() if hasattr(v, "dtype")}
    if any(m.startswith("cupy") for m in host_mods):
        print("ERROR: could not build a host-resident copy of the weights — the comparison would "
              "be GPU-vs-GPU and its result meaningless.", file=sys.stderr)
        return 2
    cpu_h = np.stack([np.asarray(clm.clm_forward_hidden(Wc, clm._seed_to_tok(p, T), T))
                      for p in prompts], 0)
    mx = float(np.abs(dev_h - cpu_h).max())
    print("  device : %s · cupy %s" % (st.get("device_name"), st.get("cupy")))
    print("  max|GPU hidden - CPU hidden| = %.3e" % mx)
    if mx == 0.0:
        print("  BYTE-IDENTICAL — a verdict is portable between this host's GPU and CPU.")
    else:
        print("  NOT byte-identical. The decode's TOKEN STREAM may still match (argmax is robust to")
        print("  this), but a probe reads the hidden itself: a GPU verdict and a CPU verdict are")
        print("  DIFFERENT MEASUREMENTS. Pin the device, and never compare across it.")
    return 0


def _probe_device():
    """Who computed these hiddens — and can another run's numbers be compared to them?

    Measured (convergence decode-py-4): the GPU forward is NOT byte-identical to the CPU one —
    max|delta| = 2.487e-14 on the hidden. The repo believed it was, because what had been verified
    was the TOKEN STREAM, and argmax is robust to 1e-14. A probe reads the hidden itself, so its
    numbers carry the device in them. _conv1d is `xcol @ Wt` = a cuBLAS dgemm with K=11352; cuBLAS
    and CPU BLAS accumulate in different orders and cannot agree to the last ulp, and cuBLAS only
    promises reproducibility for the same version + architecture. So the bits are pinned to this
    card, this cupy, this driver.

    This bit us for real: AUDIT-A's k_ctx=24 arm ran on CPU (cupy was broken that hour) and its
    k_ctx=182 arm ran on GPU, so the headline 'the sign flipped when the lens sharpened' compared
    across TWO changes. Stamping the device into every result is how that stops being invisible."""
    st = clm.gpu_status()
    return {"cuda": bool(st.get("cuda")), "device": st.get("device_name") or "cpu-numpy",
            "cupy": st.get("cupy"), "reason": st.get("reason")}


def _print_device(dev):
    print("  [DEVICE] %s%s — a probe reads the hidden, and the hidden is device-dependent "
          "(2.5e-14 GPU vs CPU): compare only across runs with the SAME device."
          % (dev["device"], (" · cupy " + dev["cupy"]) if dev.get("cupy") else ""))


def ground_probe_run(argv):
    """`anima-py evaluate <ckpt> --ground-probe <manifest.json> --out <file.json> [--win 64]`
    — the NBIND-G grounding instrument, engine-native and whole (H_9302 certified it, H_9303
    read the wall with it). Everything the verdict rests on happens inside this one command:
    the production trunk forward, the readout, the positive control and the null.

    Five things the probes it replaces got wrong, each of which manufactured a false negative
    (H_9289 / H_9290 / H_9297 / H_9300, now all INVALID — convergence gt-power-build-py-1,
    probe-capacity-py-1, gen-nbindg-n2-py-1):

      POSITION      read the hidden where the model must ANSWER (after the arrow), not at the
                    atom — a causal LM has no reason to have committed anything at the atom.
      CARRIER       ask inside the carrier the model was TAUGHT; a natural review with an arrow
                    glued on is out of distribution and the decision machinery never fires.
      V-LIVE        certify on atoms whose polarity the model WAS taught. A probe that cannot
                    read a taught answer certifies nothing about an untaught one. Counted per
                    ITEM (that is where the power is); leave-one-ATOM-out (a context-level split
                    leaks the stem and would certify a probe that only reads orthography).
      AGGREGATION   an atom's forms are half polarity-inverting BY CONSTRUCTION, so voting raw
                    item labels makes the gold vector constant. Undo each form's flip first:
                    atom_pol = majority over forms of (item_pred XOR form_flip) — the very
                    recombination the D-acc eval asks the model for.
      POWER         count at the ATOM level. Items inside an atom are not independent draws.

    Manifest: {"win":64, "bar":0.65, "items":[{"id","prompt","stem","pol","flip","split"}]}
    where `pol` is the ITEM's gold polarity, `flip` says whether that form inverts the atom's,
    and `split` is "train" (taught) or "heldout" (never taught). Read-only: no decode sampling,
    no term added to any loss (a_train_inline_gauge / p7 clean)."""
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--ground-probe", "")))
    out_path = evaluate_strval(argv[1:], "--out", "ground_probe.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    bar = float(spec.get("bar", 0.65))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    print("=== anima evaluate --ground-probe — NBIND-G grounding (engine-native) ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · bar " + str(bar) +
          " · " + str(len(items)) + " prompts")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    dev = _probe_device()
    _print_device(dev)

    X = []
    for k, it in enumerate(items):
        tok = clm._seed_to_tok(it["prompt"], T)          # same encode the gates decode over
        yn = clm.clm_forward_hidden(W, tok, T)           # EXACT production trunk forward
        X.append(np.asarray(yn)[T - 1].astype(np.float64))     # THE ANSWER POINT
        if (k + 1) % 100 == 0:
            print("  [forward %d/%d]" % (k + 1, len(items)), flush=True)
    X = np.stack(X, 0)
    y = np.array([int(i["pol"]) for i in items], dtype=np.float64)
    fl = np.array([int(i.get("flip", 0)) for i in items])
    st = np.array([i["stem"] for i in items])
    sp = np.array([i["split"] for i in items])
    tr, te = sp == "train", sp == "heldout"

    # V-LIVE — leave-one-ATOM-out over the TAUGHT atoms, scored per item
    hit = tot = 0
    for a in np.unique(st[tr]):
        m = (st == a) & tr
        p = _gp_logreg(X[tr & ~m], y[tr & ~m], X[m])
        hit += int(((p > 0.5) == (y[m] > 0.5)).sum()); tot += int(m.sum())
    v_live = hit / float(tot) if tot else float("nan")

    def atom_acc(pred):
        """Undo each form's flip, then vote — the atom's polarity is the latent."""
        ok = 0
        ats = np.unique(st[te])
        for a in ats:
            m = (st == a) & te
            rec = np.logical_xor(pred[m[te]] > 0.5, fl[m] == 1)     # recovered atom polarity
            gold = np.logical_xor(y[m] > 0.5, fl[m] == 1)[0]
            ok += int((rec.mean() > 0.5) == bool(gold))
        return ok / float(len(ats)), len(ats)

    acc, n_at = atom_acc(_gp_logreg(X[tr], y[tr], X[te]))
    sd = math.sqrt(0.25 / n_at) if n_at else float("nan")

    rng = np.random.default_rng(seed)
    # all n_perm draws in ONE descent — same math, ~n_perm x less wall (see _selftest_batch_null:
    # the label decisions are identical and the numeric drift is ~1e-15 against a ~1e-5 margin)
    Yp = np.stack([rng.permutation(y[tr]) for _ in range(n_perm)], 1)
    Pp = _gp_logreg_batch(X[tr], Yp, X[te])
    null = np.array([atom_acc(Pp[k])[0] for k in range(n_perm)])
    pval = float((null >= acc).mean())

    print("  [V-LIVE  taught atoms, per item n=%d] %.3f" % (tot, v_live))
    print("  [HELD-OUT atoms n=%d · chance sd %.4f · bar %.2f = %.2f sigma] %.3f (%+.2f sigma)"
          % (n_at, sd, bar, (bar - 0.5) / sd, acc, (acc - 0.5) / sd))
    print("  [PERM null %d draws] p = %.3f · p95 = %.3f" % (n_perm, pval, float(np.quantile(null, 0.95))))
    out = {"ckpt": ckpt, "win": T, "bar": bar, "device": dev,
           "v_live_taught_per_item": v_live,
           "heldout_atom_acc": acc, "n_atoms": n_at, "chance_sd": sd,
           "bar_sigma": (bar - 0.5) / sd, "perm_p": pval, "n_perm": n_perm,
           "perm_p95": float(np.quantile(null, 0.95))}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("GROUND-PROBE wrote " + out_path)
    return 0


def valence_audit_run(argv):
    """`anima-py evaluate <ckpt> --valence-audit <manifest.json> --out <file.json>` — AUDIT-A,
    the $0 pre-fire audit the O channel lives or dies on (Fable design, DESIGN_OC_fable.md §4).

    H_9303 proved the model does not USE a held-out atom's polarity at the moment it must answer.
    It did NOT ask whether the natural corpus formed that polarity ANYWHERE in the weights. The O
    channel's whole bet is that the information exists and the answer slot simply has no gradient
    reason to consume it (a rote-lookup slot's gradient is zero once the grid fits). If the valence
    was never formed at all, there is nothing to bridge and the fire is wasted.

    So: read the hidden at the atom's own position inside its REAL corpus contexts, pool per atom,
    leave-one-ATOM-out probe for gold polarity.

    THE CONTROL IS THE MEASUREMENT (FORM tunable · BIND earned). A sentiment review is full of
    sentiment words, so a probe reading the neighbourhood — not the atom — would score just as well.
    Every item therefore comes in two arms: `atom` (the real atom in its real context) and `swap`
    (a length-matched NEUTRAL atom spliced into the SAME context). The verdict is the difference

        Delta = probe_acc(atom) - probe_acc(swap)

    against a label-permutation null — never a raw value.

    Manifest: {"items":[{"id","prompt","stem","pol","arm"}]} with arm in {"atom","swap"}; `prompt`
    ends right after the atom (the atom's own contextualised position). Read-only: no sampling, no
    loss term (a_train_inline_gauge / p7 clean)."""
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--valence-audit", "")))
    out_path = evaluate_strval(argv[1:], "--out", "valence_audit.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    print("=== anima evaluate --valence-audit — AUDIT-A: is the valence in the weights at all? ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · " + str(len(items)) + " prompts")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    dev = _probe_device()
    _print_device(dev)

    H = []
    for k, it in enumerate(items):
        H.append(np.asarray(clm.clm_forward_hidden(
            W, clm._seed_to_tok(it["prompt"], T), T))[T - 1].astype(np.float64))
        if (k + 1) % 200 == 0:
            print("  [forward %d/%d]" % (k + 1, len(items)), flush=True)
    H = np.stack(H, 0)
    arm = np.array([i["arm"] for i in items])
    st = np.array([i["stem"] for i in items])
    y = np.array([int(i["pol"]) for i in items], dtype=np.float64)

    # H_9612 · LENGTH-MATCH AUDIT — this instrument PRINTS "length-matched NEUTRAL atom" as if it
    # were a fact, but the matching is the manifest builder's job and nothing here ever checked it.
    # An unmatched swap atom changes the prompt's byte length, and the window is right-aligned, so
    # the two arms are read with different context in the window — and H_9611 measured a
    # sequence-global GroupNorm bus that carries exactly that difference to the read point (T-1).
    # Delta = acc(atom) - acc(swap) would then be part length-shift, not all form-vs-content.
    # So: verify per stem, and say so out loud. (Same defect class as route-audit's negZ-vs-ped.)
    _bl = {}
    for it in items:
        _bl.setdefault(it["stem"], {})[it["arm"]] = len(it["prompt"].encode())
    _mis = [(s, d.get("atom"), d.get("swap")) for s, d in _bl.items()
            if d.get("atom") is not None and d.get("swap") is not None and d["atom"] != d["swap"]]
    if _mis:
        _ex = " · ".join("%s(atom %dB vs swap %dB)" % m for m in _mis[:3])
        print("  ⚠️ LENGTH-MISMATCH (H_9612): %d/%d stems — %s%s\n"
              "     The swap arm is NOT length-matched, so the right-aligned window shifts and the\n"
              "     arms carry different context; the GroupNorm bus (H_9611) can move Delta by that\n"
              "     alone. Read Delta as form+shift, NOT form — or rebuild the manifest matched."
              % (len(_mis), len(_bl), _ex, " …" if len(_mis) > 3 else ""), flush=True)
    else:
        print("  [len-audit] 🟢 atom/swap byte-length matched on all %d stems" % len(_bl), flush=True)

    def pooled(a):
        """One vector per atom — the atom's contexts averaged. Its gold polarity is the atom's."""
        m = arm == a
        ats = sorted(set(st[m]))
        X = np.stack([H[m & (st == s)].mean(0) for s in ats], 0)
        g = np.array([y[m & (st == s)][0] for s in ats], dtype=np.float64)
        return X, g, ats

    def loo(X, g, perm=None):
        gg = g if perm is None else perm
        hit = 0
        for i in range(len(gg)):
            m = np.ones(len(gg), bool); m[i] = False
            p = _gp_logreg(X[m], gg[m], X[i:i + 1])
            hit += int((p[0] > 0.5) == (gg[i] > 0.5))
        return hit / float(len(gg))

    Xa, ga, ats = pooled("atom")
    Xs, gs, _ = pooled("swap")
    acc_a, acc_s = loo(Xa, ga), loo(Xs, gs)
    delta = acc_a - acc_s

    # FORM-ID — the diagnostic that makes a negative Delta interpretable.
    #
    # If the read point's hidden is dominated by the IDENTITY of the byte sitting there (form), then
    # at that position the atom's identity should be highly decodable while its polarity is not:
    # form present, bind absent. That is the mechanism FORM-OCCLUSION claims, and without this number
    # a negative Delta cannot tell it apart from "the atom injects nothing at all".
    #
    # Measured as a 1-vs-rest linear probe per atom on the UNPOOLED per-context hiddens, scored as
    # the fraction of contexts whose own atom wins its own probe against a random other atom's probe
    # — a 2AFC, so chance is 0.5 regardless of how many atoms there are.
    def form_id(a):
        m = arm == a
        Xc = H[m]                                    # per-context, NOT pooled
        sc = st[m]
        ids = sorted(set(sc))
        # Standardise ONCE, and fit all 91 one-vs-rest probes in ONE batched descent. The first cut
        # re-standardised inside the atom loop, which rebuilt a [16562, 3784] float64 array 91 times
        # (~500 MB each) and made the DIAGNOSTIC cost more than the verdict it explains. Same math,
        # same numbers — _gp_logreg_batch is the descent already proved decision-identical.
        mu, sd = Xc.mean(0), Xc.std(0)
        sd = np.where(sd == 0.0, 1.0, sd)
        Y = np.stack([(sc == s).astype(np.float64) for s in ids], 1)      # [n, 91]
        P = _gp_logreg_batch(Xc, Y, Xc, iters=120).T                      # [n, 91] each atom's score
        rng2 = np.random.default_rng(seed)
        idx = {s: i for i, s in enumerate(ids)}
        hit = 0
        for k in range(len(sc)):
            i = idx[sc[k]]
            j = int(rng2.integers(len(ids) - 1))
            if j >= i:
                j += 1                               # a DIFFERENT atom's probe
            hit += int(P[k, i] > P[k, j])
        return hit / float(len(sc))

    fid_a, fid_s = form_id("atom"), form_id("swap")

    rng = np.random.default_rng(seed)
    # Draw the permutations in the SAME INTERLEAVED ORDER the per-draw loop consumed them (atom
    # then swap, per draw). Batching the descent must not re-order the RNG: a different draw
    # sequence is a different null sample, and the p-value would move for a reason that has nothing
    # to do with the science.
    Ga = np.empty((len(ga), n_perm)); Gs = np.empty((len(gs), n_perm))
    for k in range(n_perm):
        Ga[:, k] = rng.permutation(ga)
        Gs[:, k] = rng.permutation(gs)

    def loo_batch(X, G):
        """leave-one-atom-out over all K permuted label vectors at once: one descent per held-out
        atom instead of one per (atom, draw). Same descent, same numbers (_selftest_batch_null)."""
        n = G.shape[0]
        hit = np.zeros(G.shape[1])
        for i in range(n):
            m = np.ones(n, bool); m[i] = False
            P = _gp_logreg_batch(X[m], G[m], X[i:i + 1])            # [K, 1]
            hit += ((P[:, 0] > 0.5) == (G[i] > 0.5)).astype(np.float64)
        return hit / float(n)

    null = loo_batch(Xa, Ga) - loo_batch(Xs, Gs)
    pval = float((null >= delta).mean())
    sd = math.sqrt(0.25 / len(ats))

    print("  [atom  arm] LOO probe acc %.3f   (n=%d atoms · chance sd %.4f)" % (acc_a, len(ats), sd))
    print("  [swap  arm] LOO probe acc %.3f   (length-matched NEUTRAL atom, SAME contexts)" % acc_s)
    print("  [DELTA = atom - swap] %+.3f   vs %d-draw permutation null: p = %.3f · p95 = %+.3f"
          % (delta, n_perm, pval, float(np.quantile(null, 0.95))))
    print("  [FORM-ID 2AFC · chance 0.5] atom-arm %.3f · swap-arm %.3f — how decodable is WHICH atom"
          % (fid_a, fid_s))
    print("       (high FORM-ID with a non-positive DELTA = form present, bind absent: the read point"
          " carries the byte's identity, not its valence)")
    live = pval < 0.05 and delta > 0.0
    print("  VALENCE " + ("PRESENT — the atom itself carries polarity in the representation; the O "
                          "channel has an input to bridge."
                          if live else
                          "ABSENT — the atom carries no polarity beyond its neighbourhood. The O "
                          "channel would have nothing to consume: DO NOT FIRE."))
    out = {"ckpt": ckpt, "device": dev,
           "acc_atom": acc_a, "acc_swap": acc_s, "delta": delta, "perm_p": pval,
           "perm_p95": float(np.quantile(null, 0.95)), "n_atoms": len(ats), "chance_sd": sd,
           "valence_present": bool(live), "n_perm": n_perm,
           "form_id_atom": fid_a, "form_id_swap": fid_s}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("VALENCE-AUDIT wrote " + out_path)
    return 0


def interaction_lift_run(argv):
    """`anima-py evaluate <ckpt> --interaction-lift <manifest.json> --out <file.json>
    [--win T] [--score-len K]` — engine-native joint interaction-lift measurement
    (H_9255, Fable design state/g1_joint_interaction_corpus/DESIGN_FABLE.md §3).

    For each pre-registered window (a byte span carrying an (A,B) concept pair, cell-
    labelled), the EXACT production trunk forward emits the model's per-continuation NLL
    (mean over the last --score-len scored positions). Read-only: reads logits, changes
    NO decode math, adds NO term to any loss (a_train_inline_gauge / p7 clean). Per-cell
    NLL lists are dumped so the OFFLINE joint-fit (additive vs +bilinear, Freedman-Lane
    control) can measure whether the model's NLL surface over the (A,B) grid carries
    non-additive structure — the Y1 half of Fable's 해석 매트릭스 (Y3 = model-free corpus).
    Engine-native (py 2-production numpy, a_eval_py_canonical) → TERMINAL-eligible.
    manifest = {"win":T,"score_len":K,"items":[{"text":"<span>","a":i,"b":j},…]}."""
    import numpy as np      # numpy is function-local throughout evaluate.py (no module import)
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--interaction-lift", "")
    out_path = evaluate_strval(argv[1:], "--out", "interaction_lift.json")
    spec = json.load(open(spec_path))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    score_len = evaluate_intval(argv[1:], "--score-len", int(spec.get("score_len", 8)))
    items = spec["items"]
    print("=== anima evaluate --interaction-lift — joint interaction-lift (H_9255) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d windows · T=%d · score_len=%d · read-only NLL surface)" %
          (spec_path, len(items), T, score_len))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    V = int(W["V"])
    cells = {}
    n_done = 0
    for it in items:
        text = it["text"]
        key = "%d,%d" % (int(it["a"]), int(it["b"]))
        tok = clm._seed_to_tok(text, T)                  # [T] right-aligned bytes
        logits = clm._fwd_logits(W, tok, T)              # [T, V]; pos i predicts tok[i+1]
        # NLL over the last `score_len` scored positions (the continuation after both concepts)
        lo = max(0, T - 1 - score_len)
        nlls = []
        for i in range(lo, T - 1):
            row = logits[i]
            m = float(np.max(row))
            lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
            tgt = int(tok[i + 1])
            nlls.append(lse - float(row[tgt]))           # -log softmax[tgt]
        cells.setdefault(key, []).append(float(np.mean(nlls)) if nlls else 0.0)
        n_done += 1
        if n_done % 200 == 0:
            print("  [ilift #%d/%d]" % (n_done, len(items)), flush=True)
    summary = {k: {"nll_mean": float(np.mean(v)), "n": len(v)} for k, v in cells.items()}
    json.dump({"ckpt": ckpt, "T": T, "score_len": score_len, "n_windows": len(items),
               "n_cells": len(cells), "cells": cells, "summary": summary},
              open(out_path, "w"), ensure_ascii=False)
    print(json.dumps({"ckpt": ckpt, "T": T, "n_windows": len(items),
                      "n_cells": len(cells), "out": out_path}, ensure_ascii=False))
    return 0


def _xbind_first_word(text):
    t = text.strip()
    return t.split()[0].strip(",.;:") if t.split() else ""


def _xbind_breakdown(rows):
    """Split the headline D-acc by gold class, and by flip when the manifest carries one.

    A scalar accuracy erases where it came from, and on a class-imbalanced manifest that is enough
    to manufacture a fake learning curve: a model that has COLLAPSED onto the majority label scores
    the majority fraction for free, and as the collapse deepens its majority-class accuracy climbs,
    so the headline rises monotonically with budget while the model has learned nothing about the
    stem. Measured (H_9324, labels 14 pos : 15 neg): the 6000@5e-5 cell reads D-acc 0.575 and looks
    like "the budget is starting to bite" — but split by class it is neg 0.956 / pos 0.167 (WORSE
    than chance), i.e. the model answers "부정" to almost everything. The real learning does not
    start until pos wakes up (0.190 -> 0.571 -> 0.905). Reporting only the headline would have
    written that false narrative into a verdict, and then built the next experiment on top of it.

    So this is NOT opt-in. A diagnostic whose job is to stop a false verdict must never sit behind
    a flag — the run that most needs it is exactly the run that would forget to pass it.

    The flip split is the same argument one level up: on a manifest whose gold is `pol XOR flip`,
    flip0 asks "is the fact in the weights" and flip1 asks "is the operator applied to it", and a
    single number over both answers neither.
    """
    def acc(rs):
        return sum(1 for r in rs if r["margin"] > 0) / max(1, len(rs))

    bd = {}
    flipped = any(r.get("flip") is not None for r in rows)
    by_class = {}
    for r in rows:
        by_class.setdefault(r.get("gold_word"), []).append(r)
    # On a flipped manifest the pooled class split is meaningless (see the flip block below), so
    # the class columns live INSIDE each flip stratum instead.
    if len(by_class) > 1 and not flipped:
        cls = {k: {"n": len(v), "acc": acc(v)} for k, v in sorted(by_class.items())}
        big = max(by_class.values(), key=len)
        minority = min(by_class.values(), key=len)
        # what a constant predictor of the majority label scores for free
        bd["class"] = cls
        bd["majority_baseline"] = len(big) / max(1, len(rows))
        # Collapse = the model is riding the label prior, not the stem. Called out by the WEAKEST
        # class landing at/below chance while the headline sits above the majority baseline's floor.
        weakest = min(acc(v) for v in by_class.values())
        bd["weakest_class_acc"] = weakest
        bd["collapse"] = bool(weakest <= 0.5)

    by_flip = {}
    for r in rows:
        if r.get("flip") is not None:
            by_flip.setdefault(int(r["flip"]), []).append(r)
    if len(by_flip) > 1:
        # The class split must be taken WITHIN each flip stratum, never across them: on a flipped
        # manifest the gold class is `pol XOR flip`, so pooling the strata mixes two different
        # questions and the pooled class column reads as a collapse that is really just the flip
        # structure. Stratify, and the two questions stay separable.
        bd["flip"] = {}
        for k, v in sorted(by_flip.items()):
            g = {}
            for r in v:
                g.setdefault(r.get("gold_word"), []).append(r)
            bd["flip"][str(k)] = {
                "n": len(v), "acc": acc(v),
                "class": {c: {"n": len(rs), "acc": acc(rs)} for c, rs in sorted(g.items())},
            }
    return bd


def _xbind_hms(sec):
    """Seconds -> compact h/m/s, for the progress heartbeat's elapsed + eta."""
    sec = int(max(0, sec))
    if sec >= 3600:
        return "%dh%02dm" % (sec // 3600, (sec % 3600) // 60)
    if sec >= 60:
        return "%dm%02ds" % (sec // 60, sec % 60)
    return "%ds" % sec


def _json_safe(o):
    """Scrub lone surrogates from decode output before json.dump. A byte-LM emits raw bytes
    that decode (surrogateescape) to lone surrogates mid-multibyte; json.dump(ensure_ascii=False)
    then raises UnicodeEncodeError('surrogates not allowed') and the whole eval file is lost even
    though the D-acc summary is already computed. Surrogates -> U+FFFD; valid text unchanged."""
    if isinstance(o, str):
        return o.encode("utf-8", "surrogatepass").decode("utf-8", "replace")
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_json_safe(v) for v in o]
    return o


def _consult_render(fact, fmt):
    """Render one store fact as a context prefix.

    The SAME prefix goes in front of BOTH gold and counterfactual, so the paired NLL difference
    cancels it — the prefix cannot move the margin by itself, only by being COMPOSED with the
    negation morpheme. That is the whole point: flip1 is what gets scored, and there the injected
    polarity points at the WRONG answer, so parroting the prefix LOSES.

    DEMO (H_9311, the only format with measured support) renders the fact as a one-shot
    demonstration in the model's OWN training template — `이 영화 <stem>고 => <긍정|부정>.\\n`.
    H_9309 established why nothing else works: the label-only prefixes (F1/F2/F3) perturbed the
    trunk hard (|Δ| = 59-74% of the base margin, 0/174 trials unmoved) yet carried zero
    information (flip0 and flip1 both pushed the WRONG way). We were speaking a language the
    byte-LM was never taught. Three facts, all read off disk rather than assumed
    (state/h9311_decon2/prefreeze_audit.py):
      · the training corpus separates instances with a single b"\\n" (960/960, unanimous),
      · training ran at seq_len=1024 over instances of median 41B, so ~24 consecutive instances
        shared every window — `instance \\n instance` is not merely in-distribution, it is what
        the model saw at every step,
      · at eval the left context is a run of pad spaces (core/decode.py:955), which training
        never produced — so the DEMO prefix moves the prompt TOWARD the training distribution,
        not away from it.
    F1/F2/F3 are kept only to reproduce H_9309 verbatim; they are not live formats.
    """
    pol_word = "긍정" if int(fact["pol"]) == 1 else "부정"
    lex_word = "좋음" if int(fact["pol"]) == 1 else "나쁨"
    if fmt == "DEMO":
        return "이 영화 " + fact["key"] + "고 => " + pol_word + ".\n"
    if fmt == "F2":
        return pol_word + ". "
    if fmt == "F3":
        return fact["key"] + "=" + lex_word + ". "
    return fact["key"] + ":" + pol_word + ". "          # F1 (default)


def _consult_seed(seed, item, store, fmt, win, gold, cf):
    """seed' = render(fact) + seed, with a pre-registered byte-audit fallback.
    The right-aligned window is `win` bytes; if prefix+seed+cont overflows it the window would
    silently eat the prefix HEAD (the stem's leading UTF-8 bytes) and the run would look like
    'consumption failure' when it is really truncation (Fable D5). So: try F1/F3, fall back to
    the shorter F2, and report which trials were downgraded."""
    if not store:
        return seed, None
    fact = store.get(item.get("a")) or store.get(item.get("b"))
    if not fact:
        return seed, None
    budget = win - len(seed.encode()) - max(len(gold.encode()), len(cf.encode()))
    pref = _consult_render(fact, fmt)
    if len(pref.encode()) <= budget:
        return pref + seed, fmt
    if fmt == "DEMO":
        # No fallback. Downgrading a DEMO trial to a label-only prefix would silently mix two
        # formats in one run — and one of them (F2) is the format H_9309 measured as carrying
        # zero information. A mixed instrument cannot be read, so an overflowing trial is
        # DROPPED and the byte-audit turns the whole run INVALID-INSTRUMENT. Widen the window
        # instead; training ran at seq_len=1024, so there is room.
        return seed, "DROPPED-overflow"
    pref2 = _consult_render(fact, "F2")                  # deterministic downgrade (F1/F3 only)
    if len(pref2.encode()) <= budget:
        return pref2 + seed, "F2-downgrade"
    return seed, "DROPPED-overflow"                     # audited, never silent


def _consult_decode_seed(item, store, fmt, t_dec, filler_n, gen):
    """H_9407 · GENERATION-surface consult seed: render(fact) + filler + stem-seed. Same
    _consult_render as the scoring lane, so the declaration BYTES are byte-identical on both
    surfaces (the run's own positive control is the scoring margin, left untouched). in_win = the
    WHOLE prefix stays inside the sliding decode window for ALL `gen` generated bytes (window slides
    1B/step), i.e. bytes + gen <= t_dec. Filler = 0x20 spaces (== the decoder's left-pad byte), so
    filler >= t_dec makes the window content bitwise EQUAL to the empty-store arm (the out-of-window
    control is MECHANICAL, not statistical — Fable §3 arm B ≡ E). Overflow is audited, never silent."""
    if not store:
        return item["seed"], None
    fact = store.get(item.get("a")) or store.get(item.get("b"))
    if not fact:
        return item["seed"], None
    pref = _consult_render(fact, fmt)
    seed_dec = pref + (" " * filler_n) + item["seed"]
    nb = len(seed_dec.encode())
    in_win = (nb + gen <= t_dec)
    if filler_n == 0 and not in_win:
        return item["seed"], "DROPPED-overflow"          # counted; the run turns INVALID-STRUCTURAL
    return seed_dec, {"fmt": fmt, "bytes": nb, "in_win": in_win, "filler": filler_n}


def _xbind_cont_nll(np, clm_mod, W, seed, cont, T):
    """Sum NLL of `cont` bytes given `seed` (right-aligned window T forward)."""
    text = seed + cont
    tok = clm_mod._seed_to_tok(text, T)
    logits = clm_mod._fwd_logits(W, tok, T)
    k = len(cont.encode())
    lo = max(0, T - 1 - k)
    s = 0.0
    for i in range(lo, T - 1):
        row = logits[i]
        m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        s += lse - float(row[int(tok[i + 1])])
    return s


def _bl_answer_pos(np, W, seed, T):
    """P(answer = 긍정) as a hard 0/1 under the H_9327 carrier readout: the model answers
    whichever of 긍정/부정 has the lower continuation NLL. Both are 6 bytes, so there is no
    length confound to correct for (H_9327's readout, inherited verbatim)."""
    n_pos = _xbind_cont_nll(np, clm, W, seed, "긍정", T)
    n_neg = _xbind_cont_nll(np, clm, W, seed, "부정", T)
    return 1.0 if n_pos < n_neg else 0.0


def _bl_answer_pos_edited(np, W, seed, T, edits):
    """Same readout, but the forward carries `edits` inside the trunk. This is the whole
    experiment: does the operator's ANSWER move when we write polarity into the site the
    operator reads (clm_forward_logits_edited) — not "can a probe read it" (read-side)."""
    out = {}
    for cont in ("긍정", "부정"):
        text = seed + cont
        tok = clm._seed_to_tok(text, T)
        logits = clm.clm_forward_logits_edited(W, tok, T, edits)
        k = len(cont.encode())
        lo = max(0, T - 1 - k)
        s = 0.0
        for i in range(lo, T - 1):
            row = logits[i]
            m = float(np.max(row))
            lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
            s += lse - float(row[int(tok[i + 1])])
        out[cont] = s
    return 1.0 if out["긍정"] < out["부정"] else 0.0


def _bl_margin(np, W, seed, T):
    """Signed continuation margin m = logP(긍정) − logP(부정) = nll(부정) − nll(긍정) (H_9361).
    The CONTINUOUS DV (transfer flips m's sign preserving |m|; scramble collapses |m|). Both 6B."""
    return (_xbind_cont_nll(np, clm, W, seed, "부정", T)
            - _xbind_cont_nll(np, clm, W, seed, "긍정", T))


def _cont_nll_edited(np, W, seed, cont, T, edits):
    """Sum NLL of `cont` bytes given `seed`, but the trunk forward carries `edits` (H_9361
    necessity arms). Same readout window as _xbind_cont_nll; edits=[] is byte-identical to it."""
    text = seed + cont
    tok = clm._seed_to_tok(text, T)
    logits = clm.clm_forward_logits_edited(W, tok, T, edits)
    k = len(cont.encode())
    lo = max(0, T - 1 - k)
    s = 0.0
    for i in range(lo, T - 1):
        row = logits[i]
        m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        s += lse - float(row[int(tok[i + 1])])
    return s


def _margin_edited(np, W, seed, T, edits):
    """Edited signed margin m = nll(부정)−nll(긍정) under `edits`. The DV under an intervention
    (H_9361). Every edit window lies in the seed region [<T−6), so the donor rows are cont-
    independent (strictly causal conv) and ONE edits list serves both continuations."""
    return (_cont_nll_edited(np, W, seed, "부정", T, edits)
            - _cont_nll_edited(np, W, seed, "긍정", T, edits))


# ── H_9392 BRIDGE-BOLT — store-mix instrument ────────────────────────────────
# `anima-py evaluate <clm> --store-mix <store.json> [--store-lambda λ]`: bolt a
# runtime store-lookup onto the FROZEN trunk by mixing a store posterior into the
# byte distribution at every measured answer position — p = λ·p_store + (1−λ)·p_trunk
# (card H_9392). Zero retrain, zero CPT, frozen ckpt (cpt-destroys-what-corpus-omits).
# The two-lane wall (H_9359) is "no runtime bridge from the operator to a declared
# store"; this bolts one on post-hoc and asks whether the wall falls (A: interface
# problem, redesign unneeded) or the store arm stays at chance (B: the bridge is only
# earnable by training — the bolt-on class is dead).
#
# INSTRUMENT INTEGRITY (C0 · gpu-forward-not-bitexact / device-parity lesson): the
# mix MUST be byte-identical to the no-store baseline at λ=0, and the guard must be
# able to FAIL. The reduction is engineered in the LOG domain via logaddexp, NOT by
# short-circuiting λ==0 to the baseline function (that would be a vacuous guard that
# tests nothing). At λ=0: log-weight(trunk)=log(1)=0.0 and log-weight(store)=log(0)=−inf,
# so logaddexp(0.0+logp_trunk_tgt, −inf+logp_store_tgt) == logp_trunk_tgt EXACTLY
# (numpy logaddexp(x,−inf)==x), and −logp_trunk_tgt == lse−row[tgt] bit-for-bit
# (fl(a−b)==−fl(b−a) under round-to-nearest). A weight bug (λ on the trunk lane, or a
# −log(p_trunk) computed through an exp/log roundtrip) makes the guard diverge — so
# the C0 preflight in store_mix_run is a REAL gate, not a false PASS.
_STORE_MIX_EPS = 1e-6


def _store_mix_cont_nll(np, clm_mod, W, seed, cont, T, store_val, lam):
    """Teacher-forced NLL of `cont` bytes given `seed`, mixing a store posterior into
    the byte distribution at each answer position: p = λ·p_store + (1−λ)·p_trunk.

    store_val : bytes — the store's asserted answer bytes (address HIT); an ε-smoothed
                one-hot per answer-relative position, and UNIFORM (neutral) beyond its
                length. An address MISS is handled by the caller (pure-trunk = baseline),
                so store_val is always the resolved value here.
    lam       : float in [0,1]. lam=0.0 is BYTE-IDENTICAL to _xbind_cont_nll (C0 guard):
                the log-domain reduction below collapses to lse−row[tgt] exactly.

    Same right-aligned window and answer span (lo..T−1) as _xbind_cont_nll, so the two
    are directly comparable and the λ=0 parity is a clean equality test."""
    text = seed + cont
    tok = clm_mod._seed_to_tok(text, T)
    logits = clm_mod._fwd_logits(W, tok, T)
    k = len(cont.encode())
    lo = max(0, T - 1 - k)
    V = int(np.asarray(logits).shape[1])
    # log-domain component weights. At λ=0 ⇒ (0.0, −inf); at λ=1 ⇒ (−inf, 0.0). Using
    # math.log on the exact 0.0/1.0 endpoints keeps the reduction bit-clean.
    lw_tr = math.log(1.0 - lam) if lam < 1.0 else float("-inf")
    lw_st = math.log(lam) if lam > 0.0 else float("-inf")
    lu = math.log(1.0 / V)                            # uniform store byte log-prob (neutral)
    s = 0.0
    for i in range(lo, T - 1):
        row = logits[i]
        tgt = int(tok[i + 1])
        m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        logp_trunk = float(row[tgt]) - lse           # = −(baseline per-pos nll term)
        r = i - lo                                    # answer-relative byte position
        if r < len(store_val):
            if store_val[r] == tgt:
                logp_store = math.log(1.0 - _STORE_MIX_EPS)
            else:
                logp_store = math.log(_STORE_MIX_EPS / (V - 1))
        else:
            logp_store = lu                           # neutral beyond the asserted value
        lpm = float(np.logaddexp(lw_tr + logp_trunk, lw_st + logp_store))
        s += -lpm
    return s


# ── H_9800 DECL-FLIP — ephemeral-declaration grounding, first-class ─────────
# `anima-py evaluate <clm> --decl-flip <c.txt.decl.json>` promotes the H_9359 diagnostic
# ("does the answer move when the in-context declaration moves?") from an ad-hoc probe to a
# scored flag on the canonical measurement path.
#
# THE DV IS FLIP-SENSITIVITY, NOT ACCURACY. flip_sens = the fraction of items whose answer
# CHANGES when the queried stem's declaration is flipped. Accuracy is also reported (against a
# chance level DERIVED from the realized gold split), but the grounding question is the flip: a
# model can be at chance on accuracy and still be reading the declaration, and — far more
# dangerous — it can be ABOVE chance on accuracy from a stem prior while reading nothing.
#
# ARMS (all three run on the SAME items, so every number is a within-item collapse-Δ):
#   live              both worlds carry the true declaration block; the flip moves exactly the
#                     queried stem's 4 value bytes. The carrier is byte-identical across the
#                     flip, so a declaration-independent DETERMINISTIC policy has flip_sens
#                     exactly 0 — the structural chance level for this DV.
#   declaration-drop  the queried stem's declaration line is removed in BOTH worlds ⇒ the two
#                     contexts are byte-identical ⇒ flip_sens is 0 MECHANICALLY. This is the
#                     instrument's own null: if it ever reads != 0 the harness is broken, and
#                     the run is declared INSTRUMENT-DEAD rather than reported.
#   value-shuffle     same keys, same value multiset, correspondence deranged (shuf[i] =
#                     values[pi[i]], pi a derangement). Because pi[q] != q the QUERIED stem's
#                     declaration is world-INVARIANT while some OTHER stem's declaration moves —
#                     the same number of bytes change and every surface statistic is matched,
#                     so this is the statistical floor (control-must-match-mediating-covariate).
#
# ORACLE PREFLIGHT (positive-control-before-reading-a-negative): before any forward pass the run
# re-derives every gold from the manifest's structured fields (gold = sense_bit XOR role_bit),
# re-audits that no carrier contains an answer token or a label name, and checks that live_a and
# live_b differ ONLY in the queried declaration at equal byte length. Oracle flip_sens must be
# exactly 1.0. Anything less ⇒ INSTRUMENT-DEAD and a held-out number must NOT be read.
_DECL_FLIP_ARMS = ("live", "declaration-drop", "value-shuffle")


def _decl_flip_answer(np, W, seed, answers, T):
    """2AFC answer index by continuation NLL. Both answer tokens are the same byte length in the
    corpus grammar, so there is no length confound to correct for (H_9327's readout, inherited)."""
    nlls = [_xbind_cont_nll(np, clm, W, seed, a, T) for a in answers]
    return int(min(range(len(nlls)), key=lambda i: nlls[i])), nlls


def _decl_flip_cell(rows):
    """Aggregate one (arm, stratum, polarity) cell. chance is DERIVED from the realized gold
    split in THIS cell (the accuracy of the best constant predictor here), never assumed."""
    n = len(rows)
    if not n:
        return {"n": 0}
    golds = [r["gold_bit"] for r in rows]
    c = {}
    for g in golds:
        c[g] = c.get(g, 0) + 1
    return {
        "n": n,
        "flip_sens": sum(1 for r in rows if r["ans_a"] != r["ans_b"]) / float(n),
        "acc_a": sum(1 for r in rows if r["ans_a"] == r["gold_bit"]) / float(n),
        "acc_b": sum(1 for r in rows if r["ans_b"] == (1 - r["gold_bit"])) / float(n),
        "gold_counts": {str(k): v for k, v in sorted(c.items())},
        "chance_acc": max(c.values()) / float(n),
        "chance_flip": 0.0,
    }


def decl_flip_run(argv):
    """`anima-py evaluate <ckpt> --decl-flip <manifest.json> [--out f.json] [--win 256]
    [--arms live,declaration-drop,value-shuffle] [--strata seen,heldout-stem,...]` — H_9800."""
    import numpy as np
    ckpt = argv[0]
    man_path = evaluate_strval(argv[1:], "--decl-flip", "")
    man = json.load(open(man_path, encoding="utf-8"))
    if man.get("schema") != "anima-counterfactual-decl/v1":
        print("ERROR: --decl-flip expects an `anima corpus counterfactual-decl` manifest "
              "(schema anima-counterfactual-decl/v1), got %r" % man.get("schema"), file=sys.stderr)
        return 2
    T = evaluate_intval(argv[1:], "--win", 256)
    out_path = evaluate_strval(argv[1:], "--out", "decl_flip.json")
    arms = [a for a in evaluate_strval(argv[1:], "--arms", ",".join(_DECL_FLIP_ARMS)).split(",") if a]
    bad_arm = [a for a in arms if a not in _DECL_FLIP_ARMS]
    if bad_arm:
        print("ERROR: unknown --decl-flip arm(s) %s (known: %s)"
              % (bad_arm, ",".join(_DECL_FLIP_ARMS)), file=sys.stderr)
        return 2
    want_strata = [s for s in evaluate_strval(argv[1:], "--strata", "").split(",") if s]
    entries = [e for e in man["entries"] if not want_strata or e["stratum"] in want_strata]
    answers = man["answers"]                      # index == answer_bit
    print("=== anima evaluate --decl-flip — H_9800 EPHEMERAL-DECLARATION GROUNDING ===")
    print("  ckpt %s · manifest %s · %d items · win %dB · arms %s"
          % (ckpt, man_path, len(entries), T, ",".join(arms)))
    print("  regen: %s" % man.get("regen_cmd", "(absent — this manifest is not re-derivable)"))

    # ---- ORACLE PREFLIGHT (no forward pass; plumbing + no-arbitrary-grounding audit) ----
    banned = tuple(answers) + tuple(man.get("sense_labels", [])) + tuple(man.get("role_labels", []))
    o_flip = o_gold = carrier_hits = shape_bad = 0
    for e in entries:
        if e["gold"] != answers[e["sense_bit"] ^ e["role_bit"]]:
            o_gold += 1
        if e["gold"] != e["gold_flip"]:
            o_flip += 1
        if any(b in e["carrier"] for b in banned):
            carrier_hits += 1
        a, b = e["ctx"]["live_a"], e["ctx"]["live_b"]
        if len(a.encode()) != len(b.encode()) or sum(1 for x, y in zip(a, b) if x != y) == 0:
            shape_bad += 1
        if e["ctx"]["declaration-drop_a"] != e["ctx"]["declaration-drop_b"]:
            shape_bad += 1
    n = len(entries)
    oracle_flip = o_flip / float(n) if n else 0.0
    print("  ORACLE preflight: gold-recompose mismatches %d/%d · flip_sens %.4f · carrier "
          "answer/label hits %d · context-shape violations %d" % (o_gold, n, oracle_flip,
                                                                  carrier_hits, shape_bad))
    if o_gold or carrier_hits or shape_bad or oracle_flip != 1.0:
        print("  VERDICT: ⛔ INSTRUMENT-DEAD — the manifest itself cannot express a positive "
              "(oracle flip must be exactly 1.0000, gold must recompose, no carrier may carry an "
              "answer/label, and the flip must move only the queried declaration). Do NOT read a "
              "held-out number from this run (positive-control-before-reading-a-negative).")
        json.dump({"schema": "anima-decl-flip/v1", "ckpt": ckpt, "manifest": man_path,
                   "verdict": "INSTRUMENT-DEAD",
                   "oracle": {"gold_mismatch": o_gold, "flip_sens": oracle_flip,
                              "carrier_hits": carrier_hits, "shape_bad": shape_bad}},
                  open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 2

    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2

    scored, readout = {}, {}
    for arm in arms:
        rows, margins = [], []
        for e in entries:
            sa = e["ctx"][arm + "_a"] + e["carrier"]
            sb = e["ctx"][arm + "_b"] + e["carrier"]
            ia, na = _decl_flip_answer(np, W, sa, answers, T)
            ib, _ = _decl_flip_answer(np, W, sb, answers, T)
            margins.append(na[0] - na[1])          # signed 2AFC margin in world A
            rows.append({"stratum": e["stratum"], "gold_bit": e["gold_bit"],
                         "ans_a": ia, "ans_b": ib})
        scored[arm] = rows
        # READOUT TELEMETRY — flip_sens 0 with acc == chance is produced BOTH by an honest
        # constant predictor and by a dead readout, and those are different findings. So the
        # realized answer distribution and the margin spread are printed: sd == 0 means the 2AFC
        # never moved at all (degenerate readout · report it, do not read a substrate claim off it),
        # while a wide margin with a one-sided answer distribution is a genuine constant predictor.
        mu = sum(margins) / float(len(margins)) if margins else 0.0
        sd = (sum((m - mu) ** 2 for m in margins) / float(len(margins))) ** 0.5 if margins else 0.0
        dist = {}
        for r in rows:
            dist[answers[r["ans_a"]]] = dist.get(answers[r["ans_a"]], 0) + 1
        readout[arm] = {"answer_dist_A": dist, "margin_mean": mu, "margin_sd": sd,
                        "margin_min": min(margins) if margins else None,
                        "margin_max": max(margins) if margins else None,
                        "degenerate": (sd == 0.0)}

    # declaration-drop is a MECHANICAL null: its two contexts are byte-identical, so a non-zero
    # flip here is a harness defect, not a result. Fail loud rather than publish it.
    if "declaration-drop" in scored:
        d = _decl_flip_cell(scored["declaration-drop"])["flip_sens"]
        if d != 0.0:
            print("  VERDICT: ⛔ INSTRUMENT-DEAD — declaration-drop flip_sens %.4f != 0. Its two "
                  "contexts are byte-identical, so this is a harness bug (non-determinism in the "
                  "forward, or a context that is not actually identical), never a substrate fact." % d)
            return 2

    report = {"schema": "anima-decl-flip/v1", "ckpt": ckpt, "manifest": man_path,
              "regen_cmd": man.get("regen_cmd"), "win": T, "arms": arms, "n_items": n,
              "oracle": {"flip_sens": oracle_flip, "gold_mismatch": 0, "carrier_hits": 0,
                         "shape_bad": 0},
              "overall": {}, "by_stratum": {}, "by_polarity": {}, "readout": readout}
    print("  %-18s %8s %8s %8s %8s   %s" % ("arm", "flip", "acc_A", "acc_B", "chance", "n"))
    for arm in arms:
        cell = _decl_flip_cell(scored[arm])
        report["overall"][arm] = cell
        print("  %-18s %8.4f %8.4f %8.4f %8.4f   %d"
              % (arm, cell["flip_sens"], cell["acc_a"], cell["acc_b"], cell["chance_acc"],
                 cell["n"]))
    print("  readout telemetry (tells an honest CONSTANT PREDICTOR apart from a DEAD 2AFC):")
    for arm in arms:
        r = readout[arm]
        print("    %-18s answers_A=%s · margin mean %+.4f sd %.4f [%+.4f, %+.4f]%s"
              % (arm, r["answer_dist_A"], r["margin_mean"], r["margin_sd"],
                 r["margin_min"], r["margin_max"],
                 "  ⚠️ DEGENERATE (sd=0: the 2AFC never moved)" if r["degenerate"] else ""))
    ctrl = [a for a in arms if a != "live"]
    if "live" in arms and ctrl:
        worst = max(report["overall"][a]["flip_sens"] for a in ctrl)
        delta = report["overall"]["live"]["flip_sens"] - worst
        report["collapse_delta_flip"] = delta
        report["control_max_flip"] = worst
        print("  COLLAPSE-Δ(flip) = live %.4f − max(control) %.4f = %+.4f  "
              "(the signal is the Δ vs >=2 controls, never the raw value · FORM tunable · BIND earned)"
              % (report["overall"]["live"]["flip_sens"], worst, delta))
    # per-stratum and per-polarity splits. A binary DV is NOT readable before the class split
    # (polarity-split-before-headline), and a mapping-held-out stratum is where the cache-vs-lookup
    # question actually lives — the aggregate hides both.
    for arm in arms:
        st = {}
        for s in sorted({r["stratum"] for r in scored[arm]}):
            st[s] = _decl_flip_cell([r for r in scored[arm] if r["stratum"] == s])
        report["by_stratum"][arm] = st
        pol = {}
        for g in (0, 1):
            pol[answers[g]] = _decl_flip_cell([r for r in scored[arm] if r["gold_bit"] == g])
        report["by_polarity"][arm] = pol
    print("  per-stratum flip-sensitivity (chance_flip = 0.0 structural · chance_acc DERIVED):")
    for s in sorted(report["by_stratum"][arms[0]]):
        line = "    %-18s" % s
        for arm in arms:
            c = report["by_stratum"][arm][s]
            line += " %s=%.4f(acc %.4f/ch %.4f)" % (arm[:4], c["flip_sens"], c["acc_a"],
                                                    c["chance_acc"])
        print(line)
    print("  per-polarity flip-sensitivity (binary DV is not readable before the class split):")
    for lab in answers:
        line = "    gold=%-6s" % lab
        for arm in arms:
            c = report["by_polarity"][arm][lab]
            line += " %s=%.4f(n %d)" % (arm[:4], c["flip_sens"], c["n"])
        print(line)
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("  -> %s" % out_path)
    print("  NOTE: this flag SCORES; it does not judge. The pre-registered bars live in the H_ card "
          "(SEEN flip >=0.90 AND oracle 1.0 before any held-out read; controls <=0.60). No bar is "
          "moved here and no frozen panel is touched — --decl-flip is purely ADDITIVE.")
    return 0


def twin_screen_run(argv):
    """`anima-py evaluate <ckpt> --twin-screen <twinnec_manifest.json>` — H_9361 TWIN-NECESSITY screener.

    Base m̂ per SEEN stem, gate (sign(m̂)==esign ∧ |m̂|>=1 nat), pair gated stems within each
    byte-length bucket (rank by |m̂|). Reports Y* and the within-accepted margin sd — the frozen n=9
    STOP-CONDITION input (card H_9361). This is the ITEM-GATE feasibility pass: if fewer than ~9 pairs
    survive |m̂|>=1, the paired necessity test is underpowered before the pedestal even runs."""
    import numpy as np
    ckpt = argv[0]
    man = json.load(open(evaluate_strval(argv[1:], "--twin-screen", "")))
    T = evaluate_intval(argv[1:], "--win", 64)
    out_path = evaluate_strval(argv[1:], "--out", "twin_screen.json")
    GATE = 1.0                                        # |m̂| >= 1 nat (frozen · card H_9361)
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr); return 2
    surface = man["surface"]
    print("=== anima evaluate --twin-screen — H_9361 TWIN-NECESSITY (n=9 stop-condition input) ===")
    print("  ckpt %s · surface %s · %d SEEN stems · gate |m̂|>=%.1f nat · win %dB"
          % (ckpt, surface, len(man["items"]), GATE, T))
    rows = []
    for it in man["items"]:
        m = _bl_margin(np, W, it["seed"], T)
        ok = (m > 0) == (it["esign"] > 0) and abs(m) >= GATE
        rows.append({"stem": it["stem"], "pol": it["pol"], "L": it["L"],
                     "m": float(m), "esign": it["esign"], "pass": bool(ok)})
    # pair gated opposite-polarity within each byte-length bucket, rank by |m̂| desc
    from collections import defaultdict
    buck = defaultdict(lambda: {0: [], 1: []})
    for r in rows:
        if r["pass"]:
            buck[r["L"]][r["pol"]].append(r)
    pairs, accepted_m = [], []
    for L in sorted(buck):
        pos = sorted(buck[L][1], key=lambda r: -abs(r["m"]))
        neg = sorted(buck[L][0], key=lambda r: -abs(r["m"]))
        for i in range(min(len(pos), len(neg))):
            pairs.append({"L": L, "A": pos[i]["stem"], "B_opp": neg[i]["stem"],
                          "mA": pos[i]["m"], "mB": neg[i]["m"]})
            accepted_m += [pos[i]["m"], neg[i]["m"]]
    # Y* = pairs where the A-polarity bucket also has a 2nd gate-passer (blind available)
    ystar = 0
    for L in sorted(buck):
        n = min(len(buck[L][0]), len(buck[L][1]))
        if n and len(buck[L][1]) >= 2:
            ystar += n
    n_pass = sum(1 for r in rows if r["pass"])
    sd_m = float(np.std([abs(x) for x in accepted_m])) if accepted_m else float("nan")
    gap = float(np.median([abs(p["mA"] - p["mB"]) for p in pairs])) if pairs else float("nan")
    print("\n  gate-passers: %d/%d stems · disjoint pairs Y=%d · Y*(blind-backed)=%d"
          % (n_pass, len(rows), len(pairs), ystar))
    print("  accepted |m̂|: sd=%.4f · median pair gap |mA-mB|=%.4f" % (sd_m, gap))
    print("  buckets(L→pass pol0,pol1): %s"
          % {L: [len(buck[L][0]), len(buck[L][1])] for L in sorted(buck)})
    # first-order stop-condition READOUT (τ-scale sd_w needs the PEDESTAL arm — this is the item-gate
    # feasibility only; if pairs < ~9 or gap small, the build is already in doubt · card H_9361).
    verdict = ("PAIRS-OK" if len(pairs) >= 5 else "UNDERPOWERED-BY-INVENTORY(item-gate)")
    print("\n  item-gate feasibility: %s (pairs=%d · Y*=%d) — τ-scale sd_w(pedestal) is the NEXT arm"
          % (verdict, len(pairs), ystar))
    json.dump({"surface": surface, "gate_nat": GATE, "win": T, "rows": rows, "pairs": pairs,
               "Y": len(pairs), "Ystar": ystar, "n_pass": n_pass, "accepted_abs_m_sd": sd_m,
               "median_pair_gap": gap, "item_gate": verdict},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


# t_{.975, df} for the deterministic paired CI (df = #pairs − 1). No RNG in the eval path
# (session-eval-py-only · determinism). Fallback 1.960 (normal) for df not tabulated.
_T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
         9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
         16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086}


def _tau_S(m_patched, m_A, m_B):
    """(τ, S) coordinates of the necessity plane (H_9361). τ = transfer (0=A held, 1=B reached);
    S = magnitude collapse (0=preserved, 1=annihilated) — the scramble gauge that a binary flip
    could not see. Guards m_B==m_A (never, given the ≥1-nat gate) with a NaN τ."""
    den = (m_B - m_A)
    tau = float("nan") if den == 0.0 else (m_patched - m_A) / den
    scale = (abs(m_A) + abs(m_B)) / 2.0
    S = 0.0 if scale == 0.0 else min(1.0, max(0.0, 1.0 - abs(m_patched) / scale))
    return tau, S


def _mean_ci(np, xs, t975):
    """(mean, half-width) of a deterministic t-CI over xs (paired τ across pairs)."""
    n = len(xs)
    mu = float(np.mean(xs))
    if n < 2:
        return mu, float("nan")
    sd = float(np.std(xs, ddof=1))
    hw = t975 * sd / math.sqrt(n)
    return mu, hw


def twin_necessity_run(argv):
    """`anima-py evaluate <ckpt> --twin-necessity <twinnec_manifest.json> [--win 64] [--out f.json]`
    — H_9361 TWIN-NECESSITY, the full instrument (screener PASS earned the item-gate first).

    Is the carrier position's hidden CAUSALLY NECESSARY for the operator's polarity answer? On
    byte-matched opposite-polarity STEM twins (same carrier morpheme, option A), we patch A's trunk
    with B's hidden at a window×depth and read the CONTINUOUS margin m = nll(부정)−nll(긍정). The two
    coordinates separate the three worlds a binary flip collapsed to 0.5:
      τ = (m_patched − m_A)/(m_B − m_A)   transfer   (0 = A held · 1 = B reached)
      S = 1 − |m_patched|/((|m_A|+|m_B|)/2) scramble  (0 = magnitude kept · 1 = annihilated)

    Five arms per pair (donor rows are same-frame taps; every edit window is in the seed region
    [<T−6), so donors are continuation-independent — one tap pass per twin):
      PEDESTAL  ℓ=0 · STEM window dilated by the embed-conv footprint [stem_t0, stem_t1+(K−1)) ·
                donor = twin B → the edited ℓ=0 field is bit-identical to running B ⇒ τ MUST = 1.000
                (spike-in with known truth; |τ−1|>1e-3 = a coordinate/device/architecture bug, HALT).
      IDENTITY  self-patch (donor = A's own tap) ⇒ τ MUST = 0.000 (sham; certifies the copy machinery).
      SPAN(ℓ)   carrier window [car_t0,car_t1) @ℓ · donor = B → the DV: does polarity route THROUGH
                the carrier positions at depth ℓ (τ(ℓ) trajectory).
      COMP(ℓ)   complement (stem + query, carrier untouched, cont excluded) @ℓ · donor = B →
                redundancy detector; NOT-READ is unclaimable without COMP τ̄≥0.75 (single-site trap).
      BLIND     carrier window @ℓ · donor = same-polarity byte-matched twin (H_9331 same-class donor,
                transposed to the continuous DV) → |Δm|≈0, S≈0 proves the DV is not a destruction gauge.

    Frozen decision (card H_9361 · bars never move): V1 pedestal τ=1±0.005∧S≤0.02 · V2 identity τ=0±0.005 ·
    V3 blind med|Δm|/|m_A|≤0.15∧S̄≤0.25 · V4 ≥80% items sign-correct∧|m|≥1nat∧CI width≤0.30. Per-ℓ bands:
    CARRIER-READ τ̄≥0.75∧CI excl .5∧S̄≤0.25 · NOT-READ TOST τ∈[−.15,.15]∧S̄≤0.25∧COMP τ̄≥0.75 · SCRAMBLE
    S̄>0.5 · SUPPRESSION τ̄≤−.15 (below chance = a finding). n=9 band: NOT-READ τ̄≤0.30∧COMP≥0.75 ·
    CARRIER-READ τ̄∈[0.70,1] · else INCONCLUSIVE; sign gate ≥8/9 pairs on the band side."""
    import numpy as np
    ckpt = argv[0]
    man = json.load(open(evaluate_strval(argv[1:], "--twin-necessity", "")))
    T = evaluate_intval(argv[1:], "--win", 64)
    out_path = evaluate_strval(argv[1:], "--out", "twin_necessity.json")
    GATE = 1.0
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr); return 2
    K = int(W["K"]); L = int(W["L"])
    dev = "gpu" if (hasattr(clm, "cuda_available") and clm.cuda_available()) else "cpu"
    surface = man["surface"]
    pfx_b = int(man["prefix_bytes"]); carr_b = int(man["carrier_bytes"])
    print("=== anima-py evaluate --twin-necessity — H_9361 TWIN-NECESSITY (full instrument) ===")
    print("  ckpt %s · surface %s · win %dB · K=%d L=%d · device=%s" % (ckpt, surface, T, K, L, dev))

    # --- item gate + pairing (same logic as the screener; the DV touches only gated pairs) ---
    by = {}                                         # {stem: item}, {L: {pol: [gated items ranked |m|]}}
    for it in man["items"]:
        m = _bl_margin(np, W, it["seed"], T)
        it = dict(it); it["m"] = float(m)
        it["gate"] = ((m > 0) == (it["esign"] > 0)) and abs(m) >= GATE
        by[it["stem"]] = it
    from collections import defaultdict
    buck = defaultdict(lambda: {0: [], 1: []})
    for it in by.values():
        if it["gate"]:
            buck[it["L"]][it["pol"]].append(it)
    for Lb in buck:
        for p in (0, 1):
            buck[Lb][p].sort(key=lambda r: -abs(r["m"]))
    pairs = []                                       # (A pol1, B pol0, Ab blind pol1 | None)
    for Lb in sorted(buck):
        pos, neg = buck[Lb][1], buck[Lb][0]
        for i in range(min(len(pos), len(neg))):
            blind = pos[i + 1] if (i + 1) < len(pos) else None    # 2nd pol1 stem = same-class donor
            pairs.append((pos[i], neg[i], blind))
    n_pairs = len(pairs)
    print("  gated pairs: %d (blind-backed %d)" % (n_pairs, sum(1 for _a, _b, ab in pairs if ab)))
    if n_pairs == 0:
        print("  NO gated pairs — run --twin-screen first (item-gate)."); return 2

    layers = list(range(0, L + 1))
    per_pair = []
    # accumulators: arm -> layer -> [tau across pairs], and S
    acc = {a: {l: {"tau": [], "S": []} for l in layers} for a in ("SPAN", "COMP", "BLIND", "IDENTITY")}
    ped = {"tau": [], "S": []}
    v4_sign_ok = 0

    # H_9612 · TWIN BYTE-LENGTH GUARD — REFUSE, do not warn.
    # The docstring calls the donor a "byte-matched twin", and that claim is LOAD-BEARING here, not
    # cosmetic: `base` below is computed ONCE from A's seed length, and every donor tap slices
    # B_taps/Ab_taps with those A-derived indices (stem_t0/car_t0/…). If a twin's seed is a different
    # byte length its own right-aligned offset differs, so the donor would be lifted from the WRONG
    # positions in B — a silently misaligned patch, not merely a confound. Nothing checked it, so a
    # manifest that broke the twin invariant would have produced garbage τ/S that read as a verdict.
    # (Same defect class as route-audit's negZ-vs-ped and valence-audit's unverified swap atom — but
    # those degrade the contrast, this one corrupts the measurement. Hence: refuse, like G-SPIKE.)
    _tw = []
    for (A, B, Ab) in pairs:
        la = len(A["seed"].encode())
        for nm, X in (("B", B), ("Ab", Ab)):
            if X is not None and len(X["seed"].encode()) != la:
                _tw.append("%s↔%s(%s) %dB vs %dB"
                           % (A["stem"], X["stem"], nm, la, len(X["seed"].encode())))
    if _tw:
        print("ERROR: twin byte-length invariant BROKEN on %d pair(s) — the donor taps are sliced with\n"
              "       A's right-aligned indices, so a different-length twin is lifted from the WRONG\n"
              "       positions (silently misaligned patch, not a confound). Refusing to measure.\n"
              "       %s%s" % (len(_tw), " · ".join(_tw[:3]), " …" if len(_tw) > 3 else ""),
              file=sys.stderr)
        return 2
    print("  [twin-guard] 🟢 byte-length matched on all %d pair(s)" % len(pairs), flush=True)

    for (A, B, Ab) in pairs:
        S_seed = len(A["seed"].encode())
        base = T - (S_seed + 6)                      # margin forward right-aligns seed+cont (cont 6B)
        stem_t0 = base + pfx_b; stem_t1 = base + pfx_b + A["L"]
        car_t0 = base + int(A["carrier"][0]); car_t1 = base + int(A["carrier"][1])
        qry_t1 = T - 6                               # query end = continuation start
        m_A = A["m"]; m_B = B["m"]
        v4_sign_ok += 1 if (((m_A > 0) == (A["esign"] > 0)) and ((m_B > 0) == (B["esign"] > 0))
                            and abs(m_A) >= GATE and abs(m_B) >= GATE) else 0
        A_taps = clm.clm_forward_taps(W, clm._seed_to_tok(A["seed"] + "긍정", T), T)
        B_taps = clm.clm_forward_taps(W, clm._seed_to_tok(B["seed"] + "긍정", T), T)
        Ab_taps = (clm.clm_forward_taps(W, clm._seed_to_tok(Ab["seed"] + "긍정", T), T)
                   if Ab is not None else None)
        rec = {"A": A["stem"], "B": B["stem"], "Ab": (Ab["stem"] if Ab else None),
               "L": A["L"], "mA": m_A, "mB": m_B, "layers": {}}
        # PEDESTAL (ℓ=0, stem window dilated by K−1)
        pe = [{"layer": 0, "t0": stem_t0, "t1": min(T, stem_t1 + (K - 1)), "mode": "patch",
               "donor": B_taps[0][stem_t0:min(T, stem_t1 + (K - 1)), :]}]
        m_pe = _margin_edited(np, W, A["seed"], T, pe)
        t_pe, s_pe = _tau_S(m_pe, m_A, m_B); ped["tau"].append(t_pe); ped["S"].append(s_pe)
        rec["pedestal"] = {"tau": t_pe, "S": s_pe, "m": m_pe}
        for l in layers:
            e_span = [{"layer": l, "t0": car_t0, "t1": car_t1, "mode": "patch",
                       "donor": B_taps[l][car_t0:car_t1, :]}]
            e_comp = [{"layer": l, "t0": stem_t0, "t1": stem_t1, "mode": "patch",
                       "donor": B_taps[l][stem_t0:stem_t1, :]},
                      {"layer": l, "t0": car_t1, "t1": qry_t1, "mode": "patch",
                       "donor": B_taps[l][car_t1:qry_t1, :]}]
            e_id = [{"layer": l, "t0": car_t0, "t1": car_t1, "mode": "patch",
                     "donor": A_taps[l][car_t0:car_t1, :]}]
            m_span = _margin_edited(np, W, A["seed"], T, e_span)
            m_comp = _margin_edited(np, W, A["seed"], T, e_comp)
            m_id = _margin_edited(np, W, A["seed"], T, e_id)
            t_span, s_span = _tau_S(m_span, m_A, m_B)
            t_comp, s_comp = _tau_S(m_comp, m_A, m_B)
            t_id, s_id = _tau_S(m_id, m_A, m_B)
            acc["SPAN"][l]["tau"].append(t_span); acc["SPAN"][l]["S"].append(s_span)
            acc["COMP"][l]["tau"].append(t_comp); acc["COMP"][l]["S"].append(s_comp)
            acc["IDENTITY"][l]["tau"].append(t_id); acc["IDENTITY"][l]["S"].append(s_id)
            row = {"span": {"tau": t_span, "S": s_span, "m": m_span},
                   "comp": {"tau": t_comp, "S": s_comp, "m": m_comp},
                   "identity": {"tau": t_id, "S": s_id}}
            if Ab_taps is not None:
                e_bl = [{"layer": l, "t0": car_t0, "t1": car_t1, "mode": "patch",
                         "donor": Ab_taps[l][car_t0:car_t1, :]}]
                m_bl = _margin_edited(np, W, A["seed"], T, e_bl)
                t_bl, s_bl = _tau_S(m_bl, m_A, m_B)
                acc["BLIND"][l]["tau"].append(t_bl); acc["BLIND"][l]["S"].append(s_bl)
                row["blind"] = {"tau": t_bl, "S": s_bl, "m": m_bl, "dratio": abs(m_bl - m_A) / max(abs(m_A), 1e-9)}
            rec["layers"][str(l)] = row
        per_pair.append(rec)

    t975 = _T975.get(n_pairs - 1, 1.960)
    # --- validity arms ---
    v1_dt = max(abs(x - 1.0) for x in ped["tau"]); v1_ds = max(ped["S"])
    # V1 gates the BIT-IDENTITY only. The ℓ=0 stem-window patch (dilated K−1) makes the forward ==
    # twin B, so τ=1.000±0.005 IS the alignment proof. The pedestal S is NOT a scramble — with
    # m_patched=m_B exactly, S=1−|m_B|/((|m_A|+|m_B|)/2) is nonzero whenever |m_A|≠|m_B|: it is the
    # twin's own on-manifold |m| asymmetry, a KNOWN quantity, so it is REPORTED (diagnostic) not gated.
    # (The frozen table's old S≤0.02 baked in a magnitude-symmetric-twin assumption that is false for
    # asymmetric pairs — e.g. flip0 pedestal τ=1.000 exact yet S=0.13; a mechanical spec-fix, not
    # tune-to-green: it is derived from the pedestal's definition, before any DV is read.)
    v1 = "PASS" if v1_dt <= 0.005 else "INVALID-ALIGNMENT"
    id_dt = max(abs(x) for l in layers for x in acc["IDENTITY"][l]["tau"])
    v2 = "PASS" if id_dt <= 0.005 else "INVALID-INSTRUMENT"
    blind_ok = any(acc["BLIND"][l]["tau"] for l in layers)
    if blind_ok:
        bl_ratios = []
        for r in per_pair:
            for l in layers:
                b = r["layers"][str(l)].get("blind")
                if b: bl_ratios.append(b["dratio"])
        bl_med = float(np.median(bl_ratios)) if bl_ratios else float("nan")
        bl_Sbar = float(np.mean([np.mean(acc["BLIND"][l]["S"]) for l in layers if acc["BLIND"][l]["S"]]))
        v3 = "PASS" if (bl_med <= 0.15 and bl_Sbar <= 0.25) else "INVALID-DISRUPTION-GAUGE"
    else:
        bl_med = float("nan"); bl_Sbar = float("nan"); v3 = "NO-BLIND(Y*<pairs)"
    sign_frac = v4_sign_ok / n_pairs
    max_ci = max((_mean_ci(np, acc["SPAN"][l]["tau"], t975)[1] for l in layers), default=float("nan"))
    v4 = "PASS" if (sign_frac >= 0.80 and (n_pairs >= 2 and max_ci <= 0.30)) else "UNDERPOWERED"
    print("\n  --- VALIDITY (frozen) ---")
    print("  V1 PEDESTAL : max|τ−1|=%.2e (bit-identity gate) · pedestal-S=%.2e (twin |m| asym · diag, not gated) → %s"
          % (v1_dt, v1_ds, v1))
    print("  V2 IDENTITY : max|τ|=%.2e → %s" % (id_dt, v2))
    print("  V3 BLIND    : med|Δm|/|m_A|=%.4f · S̄=%.4f → %s" % (bl_med, bl_Sbar, v3))
    print("  V4 POWER    : sign-ok %d/%d=%.2f · max CI half-width=%.4f → %s"
          % (v4_sign_ok, n_pairs, sign_frac, max_ci, v4))

    # --- per-ℓ trajectory + band (SPAN is the DV; NOT-READ needs COMP) ---
    print("\n  --- τ(ℓ) TRAJECTORY (SPAN=DV · band per card H_9361) ---")
    print("   ℓ | SPAN τ̄  [95%% CI]     S̄     | COMP τ̄ | BLIND τ̄ | signOK | band")
    traj = {}
    for l in layers:
        st = acc["SPAN"][l]["tau"]; ss = acc["SPAN"][l]["S"]
        ct = acc["COMP"][l]["tau"]; bt = acc["BLIND"][l]["tau"]
        mu, hw = _mean_ci(np, st, t975)
        sbar = float(np.mean(ss)) if ss else float("nan")
        cmu = float(np.mean(ct)) if ct else float("nan")
        bmu = float(np.mean(bt)) if bt else float("nan")
        lo, hi = mu - hw, mu + hw
        # band (n=9 gate · card): CARRIER-READ τ̄∈[0.70,1]∧CI within · NOT-READ τ̄≤0.30∧COMP≥0.75 · SCRAMBLE S̄>0.5
        if sbar > 0.5:
            band = "SCRAMBLE"
        elif mu <= -0.15 and hi < 0.0:
            band = "SUPPRESSION"
        elif mu >= 1.25:
            band = "OVER-TRANSFER"
        elif 0.70 <= lo and hi <= 1.0 + 1e-9 and sbar <= 0.25:
            band = "CARRIER-READ"
        elif hi <= 0.30 and cmu >= 0.75 and sbar <= 0.25:
            band = "NOT-READ"
        else:
            band = "INCONCLUSIVE"
        # sign gate: #pairs whose τ is on the band's side
        if band == "CARRIER-READ":
            sign_n = sum(1 for x in st if x >= 0.5)
        elif band in ("NOT-READ", "SUPPRESSION"):
            sign_n = sum(1 for x in st if x <= 0.5)
        else:
            sign_n = 0
        traj[str(l)] = {"span_tau": mu, "span_ci": [lo, hi], "span_Sbar": sbar,
                        "comp_tau": cmu, "blind_tau": bmu, "sign_n": sign_n, "band": band}
        print("  %2d | %+.3f [%+.3f,%+.3f]  %.3f | %+.3f | %+.3f | %d/%d | %s"
              % (l, mu, lo, hi, sbar, cmu, bmu, sign_n, n_pairs, band))

    valid = (v1 == "PASS" and v2 == "PASS" and v3 in ("PASS", "NO-BLIND(Y*<pairs)") and v4 == "PASS")
    print("\n  instrument validity: %s (V1·V2·V3·V4)" % ("PASS" if valid else "GATED — read DV with caution"))
    json.dump({"surface": surface, "device": dev, "win": T, "K": K, "L": L, "n_pairs": n_pairs,
               "validity": {"V1": v1, "V2": v2, "V3": v3, "V4": v4, "pedestal_max_dtau": v1_dt,
                            "identity_max_tau": id_dt, "blind_med_ratio": bl_med, "blind_Sbar": bl_Sbar,
                            "sign_frac": sign_frac, "max_ci_hw": max_ci},
               "trajectory": traj, "pairs": per_pair},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def delta_pregate_run(argv):
    """`anima-py evaluate <ckpt> --delta-pregate <deltainj_manifest.json> [--win 64] [--out f.json]`
    — H_9397 Δ-INJECT behavioral pre-gate (sequential gating · stage 1, before any Δ estimation).

    The whole Δ-INJECT rests on the negation operator being ALIVE on the SEEN stems: replacing the
    positive filler `고 있다` with the carrier `지 않다` must FLIP the answer. This gate re-measures that
    on THIS ckpt and THESE stems (Fable's $0 pre-gate) as a raw continuous margin, per convergence
    corpus-py-1⑥ (a CPT model can have flip1 destroyed — never assume the operator is alive, measure it):
      per SEEN stem, m_carrier = margin(carrier_seed) and m_filler = margin(filler_seed) must (a) each
      match their expected sign and (b) be OPPOSITE (the operator flips the answer). PASS iff ≥8/9
      stems flip (same disjoint-sign threshold family as the necessity sign gate). FAIL ⇒ the operator
      is not alive here ⇒ Δ-INJECT is moot, abort before estimating anything."""
    import numpy as np
    ckpt = argv[0]
    man = json.load(open(evaluate_strval(argv[1:], "--delta-pregate", "")))
    T = evaluate_intval(argv[1:], "--win", 64)
    out_path = evaluate_strval(argv[1:], "--out", "delta_pregate.json")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr); return 2
    dev = "gpu" if (hasattr(clm, "cuda_available") and clm.cuda_available()) else "cpu"
    seen = [it for it in man["items"] if it["split"] == "train"]
    print("=== anima-py evaluate --delta-pregate — H_9397 Δ-INJECT behavioral gate (operator alive?) ===")
    print("  ckpt %s · %d SEEN stems · carrier %s vs filler %s · win %dB · device=%s"
          % (ckpt, len(seen), man["carrier"], man["filler"], T, dev))
    rows, flips = [], 0
    for it in seen:
        mc = _bl_margin(np, W, it["carrier_seed"], T)
        mf = _bl_margin(np, W, it["filler_seed"], T)
        sc_ok = (mc > 0) == (it["esign_carrier"] > 0)
        sf_ok = (mf > 0) == (it["esign_filler"] > 0)
        flip = (mc > 0) != (mf > 0)                       # operator flips the answer (opposite signs)
        ok = sc_ok and sf_ok and flip
        flips += 1 if ok else 0
        rows.append({"stem": it["stem"], "pol": it["pol"], "m_carrier": float(mc), "m_filler": float(mf),
                     "carrier_sign_ok": bool(sc_ok), "filler_sign_ok": bool(sf_ok), "flip": bool(ok)})
    n = len(seen)
    thresh = max(1, n - 1)                                # ≥ n−1 (8/9 · disjoint-sign family)
    verdict = "PASS" if flips >= thresh else "FAIL-OPERATOR-DEAD"
    gap = float(np.median([abs(r["m_carrier"] - r["m_filler"]) for r in rows])) if rows else float("nan")
    print("  operator-flip: %d/%d (need ≥%d) · median |m_carrier−m_filler|=%.4f nats" % (flips, n, thresh, gap))
    for r in rows:
        print("    %-8s pol%d : m_carrier=%+.3f m_filler=%+.3f %s"
              % (r["stem"], r["pol"], r["m_carrier"], r["m_filler"], "flip✓" if r["flip"] else "—"))
    print("\n  PRE-GATE: %s%s" % (verdict, "  → proceed to Δ estimation (ℓ2/ℓ3 · LOO)"
          if verdict == "PASS" else "  → operator not alive on SEEN, Δ-INJECT aborted (corpus-py-1⑥)"))
    json.dump({"surface": man["surface"], "device": dev, "win": T, "n_seen": n, "flips": flips,
               "thresh": thresh, "median_gap": gap, "verdict": verdict, "rows": rows},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def delta_control_run(argv):
    """`anima-py evaluate <ckpt> --delta-control <deltainj_manifest.json> [--win 64] [--out f.json]`
    — H_9397 Δ-INJECT DECISIVE control (arm B · Fable). The pre-gate FAILED (carrier `지 않다` and the
    novel filler `고 있다` gave the SAME-sign answer, no flip). Two readings collapse the whole lane:
      (1) `고 있다` is OOD → the carrier IS consumed → FILLER-OOD-BLOCKED.
      (2) the answer is STEM-determined (carrier a non-causal amplifier) → carrier attribution burned →
          held-out G1 wall unifies with SEEN as one memorized stem→answer lookup.
    Only the sign of a TRAINED flip0 carrier separates them. Arm B = `고` (trained, declarative, 3B),
    same 20 SEEN stems, sign-only DV (byte-length differs from the 10B carrier — NEVER compare magnitudes;
    a_korean_byte_budget). Both readings-(1) variants (pure OOD + dominant-frame-default) predict `고`
    UN-flips (trained frame wins); reading (2) predicts `고` flips like everything else.

      arm A (positive control) : m_carrier(지 않다) must reproduce ≥n−1/n sign-correct (esign_carrier) —
                                 the identical-pipeline check (Fable caveat 3: a slipped esign inverts all).
      arm B (decisive)         : per stem, does sign(m_flip0) == esign_flip0 (UN-flipped = stem polarity)
                                 or == esign_carrier (FLIPPED = same as the negation carrier)?
    Verdict: ≥n−1 UN-flipped → FILLER-OOD-BLOCKED (reading 1) · ≥n−1 FLIPPED → STEM-DETERMINED (reading 2)
    · else INCONCLUSIVE-WEAK-CARRIER (3B may be too little signal → 2×2 tie-breaker, cement nothing)."""
    import numpy as np
    ckpt = argv[0]
    man = json.load(open(evaluate_strval(argv[1:], "--delta-control", "")))
    T = evaluate_intval(argv[1:], "--win", 64)
    out_path = evaluate_strval(argv[1:], "--out", "delta_control.json")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr); return 2
    dev = "gpu" if (hasattr(clm, "cuda_available") and clm.cuda_available()) else "cpu"
    seen = [it for it in man["items"] if it["split"] == "train"]
    print("=== anima-py evaluate --delta-control — H_9397 arm B (고 trained flip0 · reading 1 vs 2) ===")
    print("  ckpt %s · %d SEEN stems · armA %s (pos-ctrl) · armB 고 (trained flip0, 3B · sign-only) · dev=%s"
          % (ckpt, len(seen), man["carrier"], dev))
    rows, posctrl_ok, unflip, flip = [], 0, 0, 0
    for it in seen:
        mc = _bl_margin(np, W, it["carrier_seed"], T)        # arm A (지 않다) positive control
        m0 = _bl_margin(np, W, it["flip0_seed"], T)          # arm B (고) decisive
        a_ok = (mc > 0) == (it["esign_carrier"] > 0)
        posctrl_ok += 1 if a_ok else 0
        is_unflip = (m0 > 0) == (it["esign_flip0"] > 0)      # sign == stem polarity (declarative predicts)
        is_flip = (m0 > 0) == (it["esign_carrier"] > 0)      # sign == negation carrier
        unflip += 1 if is_unflip else 0
        flip += 1 if is_flip else 0
        rows.append({"stem": it["stem"], "pol": it["pol"], "m_carrier": float(mc), "m_flip0": float(m0),
                     "posctrl_ok": bool(a_ok), "flip0_unflipped": bool(is_unflip), "flip0_flipped": bool(is_flip)})
    n = len(seen); thresh = max(1, n - 1)
    print("  arm A pos-ctrl (지 않다 sign-correct): %d/%d (need ≥%d to trust pipeline)" % (posctrl_ok, n, thresh))
    print("  arm B 고: UN-flipped(=stem pol) %d/%d · FLIPPED(=carrier) %d/%d" % (unflip, n, flip, n))
    for r in rows:
        tag = "UN-flip" if r["flip0_unflipped"] else ("FLIP" if r["flip0_flipped"] else "?")
        print("    %-8s pol%d : m_carrier=%+.3f m_고=%+.3f  →고 %s"
              % (r["stem"], r["pol"], r["m_carrier"], r["m_flip0"], tag))
    if posctrl_ok < thresh:
        verdict = "INVALID-PIPELINE (pos-ctrl 지 않다 did not reproduce — esign/frame slipped, Fable caveat 3)"
    elif unflip >= thresh:
        verdict = "FILLER-OOD-BLOCKED (reading 1): 고 un-flips → carrier IS consumed · 고 있다 was OOD"
    elif flip >= thresh:
        verdict = "STEM-DETERMINED (reading 2): 고 flips too → answer stem-keyed, carrier attribution burned · G1 wall unifies"
    else:
        verdict = "INCONCLUSIVE-WEAK-CARRIER (3B signal split — 2×2 tie-breaker, cement nothing)"
    print("\n  VERDICT: %s" % verdict)
    json.dump({"surface": man["surface"], "device": dev, "win": T, "n_seen": n, "thresh": thresh,
               "posctrl_ok": posctrl_ok, "flip0_unflipped": unflip, "flip0_flipped": flip,
               "verdict": verdict, "rows": rows}, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def bind_locus_run(argv):
    """`anima-py evaluate <ckpt> --bind-locus <manifest.json> --out <f.json>` — H_9331 BIND-LOCUS.

    H_9327 left one question standing. The negation operator is ALIVE (SEEN flip1 0.98-1.00), the
    CPT-written fact IS in the weights (WRITE 0.98), and yet the two do not bind (held-out flip1
    0.46-0.56 = chance), with the LIE control proving the planted fact is not even CONSULTED
    (bias-independence +0.073 ~ 0). Every escape was measured shut. So: WHY does pretrained polarity
    bind to the operator while CPT-written polarity does not?

    Fable's reframe, which this instrument is built around: "the two polarities live in different
    places" already ASSUMES the CPT polarity exists as a FEATURE. WRITE 0.98 does not show that — it
    shows a REFLEX (stem->answer inside the flip0 carrier). So there are three worlds, not two:

      P-place  the feature exists but not where the operator reads   -> write it there and it binds
      P-kind   there is no feature at all; CPT wrote a shortcut      -> the fix is the CORPUS, not the address
      S        the feature is right there, readable, consumable, and the operator STILL ignores it
               -> binding is not content-lookup; it is forged during pretraining (XBIND becomes law)

    A read-only probe map cannot separate these (what a probe reads != what the operator consumes —
    the read-side-exhausted lesson). Only a CAUSAL write can, so the DV comes from an intervention:

      Stage A (POSITIVE CONTROL, truth known — we plant it)
        On SEEN stems only, swap-patch the stem span's hidden with a SEEN donor of opposite polarity
        at depth l, scanning l = 0..L and a frozen span ladder (last byte -> last 3 -> whole stem).
        l* := the SHALLOWEST depth whose swap flips the answer >= G_A_SWAP with sham <= G_A_SHAM.
        No DV data touches this choice (SEEN only), so it is calibration, not tune-to-green.
        Nothing passes  -> INVALID-LOCALIZATION (the operator's read is not localized to the stem
        span; that is itself a locus fact, and P/S stays unjudged rather than falsely decided).

      Stage B (axis + magnitude, matched on the MEDIATING covariate)
        v = unit(mean(SEEN pos) - mean(SEEN neg)) at l*; targets mu+/mu- = the SEEN class means of
        the projection onto v. Injection is projection-MATCH (mode "proj"), not a fixed alpha: a
        fixed alpha leaves the realized projection different per arm, which is exactly the confound
        `control-must-match-mediating-covariate` was earned on. Realized projections are reported.

      Stage C (arms; DV = bias-independent dependence, H_9327's LIE test in causal form)
        dep_f = P(ans=pos | inject=pos) - P(ans=pos | inject=neg), paired per stem, per flip layer f.
        A global answer bias cancels in the difference by construction.
          B  novel stems (0 occurrences in pretrain AND in CPT) <- the core arm
          C  held-out (CPT-written) stems, injected with their OWN planted polarity  <- rescue arm
          D  novel stems, random direction orthogonal to v, same displacement  <- off-manifold control
          E  novel stems, self-patch (own value)                               <- sham; instrument must be inert

    Frozen decision tree (pre-registered; bars never move):
      V1  Stage A found l*                                    else INVALID-LOCALIZATION
      V2  B-arm flip0 dep0 >= G_V2   (the injection is consumed by the readout at all)
                                                              else INVALID-DEAD-INJECTION
      V3  D-arm |dep| <= G_V3 and E-arm change-rate <= G_E    else INVALID-INSTRUMENT
      --- only if V1 & V2 & V3 ---
      DV  B-arm flip1 dep1 <= G_DV_P                          -> P   (operator consumes site content:
                                                                      the wall is an address/kind problem)
          |dep1| <= G_TOST (TOST equivalence)                 -> S   (same site, consumable content,
                                                                      still no bind = substrate fact)
          otherwise                                           -> UNDERPOWERED (report se; raise n; no bar moves)

    Two CPT seeds must agree in SIGN before any tier is cemented (H_9327's own cementing rule).

    Manifest: {"win":24, "carrier":"이 영화 {stem}고 => ",
               "items":[{id, stem, stem_byte_span:[t0,t1), pol, flip, split, arm}]}
    where `split` in {seen, heldout, novel} and `flip` in {0,1} (0 = plain carrier, 1 = negated).
    Read-only w.r.t. weights; every forward is the production forward (a_experiment_engine_native).
    """
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--bind-locus", "")))
    out_path = evaluate_strval(argv[1:], "--out", "bind_locus.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 24)))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    # swap-span mode (H_9331 pedestal · 2026-07-15): where Stage A swaps the hidden.
    #   stem    — the atom span (default · the original P-place/P-kind/S test)
    #   carrier — the operator morpheme span (`지 않다`, stem-end→`=>`). 4/4 INVALID-LOCALIZATION
    #             at the stem span means the operator's polarity read is NOT there; Fable's frozen
    #             prediction is the read-site is the CARRIER (carrier-swap flip>=0.75 = the
    #             true-positive pedestal the stem run lacked). SEEN swap only ⇒ not tune-to-green.
    swap_span = evaluate_strval(argv[1:], "--bl-swap-span", "stem")
    if swap_span not in ("stem", "carrier"):
        print("ERROR: --bl-swap-span must be stem|carrier", file=sys.stderr)
        return 2
    # donor-class control (H_9331 · 2026-07-15): the polarity-blind pedestal.
    #   cross — donor is the OPPOSITE-polarity SEEN item (default · the real localization test)
    #   same  — donor is a DIFFERENT SAME-polarity SEEN item. Separates 0.50 = binary SCRAMBLE
    #           FLOOR (off-manifold destruction, polarity-blind → same-class flip ≈ 0.50 too)
    #           from 0.50 = partial real signal (same-class flip ≈ 0). If same ≈ cross ≈ 0.50 the
    #           swap-patch never localized anything (Fable · every INVALID = the instrument floor).
    donor_class = evaluate_strval(argv[1:], "--bl-swap-donor-class", "cross")
    if donor_class not in ("cross", "same"):
        print("ERROR: --bl-swap-donor-class must be cross|same", file=sys.stderr)
        return 2
    items = spec["items"]
    carrier = spec.get("carrier", "이 영화 {stem}고 => ")

    # frozen bars (Fable pre-registration · never moved post-hoc · p7)
    G_A_SWAP, G_A_SHAM = 0.75, 0.15
    G_V2, G_V3, G_E = 0.50, 0.15, 0.05
    G_DV_P, G_TOST = -0.50, 0.20

    print("=== anima evaluate --bind-locus — H_9331: why does the CPT-written polarity not bind? ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · " + str(len(items)) + " items · perm " + str(n_perm))
    print("  frozen bars: V1 swap>=%.2f sham<=%.2f · V2 dep0>=%.2f · V3 |dep_rand|<=%.2f sham<=%.2f"
          % (G_A_SWAP, G_A_SHAM, G_V2, G_V3, G_E))
    print("  frozen DV  : P if dep1<=%.2f · S if TOST(+-%.2f) · else UNDERPOWERED" % (G_DV_P, G_TOST))
    print("  swap-span  : %s%s" % (swap_span,
          "  (operator morpheme 지 않다 — H_9331 pedestal · 예측 flip>=%.2f)" % G_A_SWAP
          if swap_span == "carrier" else "  (atom span — default)"))
    print("  donor-class: %s%s" % (donor_class,
          "  (SAME-polarity donor — polarity-blind control · (B)면 flip≈0.50 (A)면 ≈0)"
          if donor_class == "same" else "  (opposite-polarity donor — default)"))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    L = int(W["L"])

    _tap_cache = {}

    def taps_of(text):
        """Memoized per-prompt tap read. The scan asks for the same donor's taps once per
        (item, depth, rung); recomputing the forward each time made the scan quadratic and the
        instrument unrunnable. The cached value is the SAME production forward, so this is a
        speed fix with zero numeric effect (byte-identical by construction)."""
        h = _tap_cache.get(text)
        if h is None:
            h = clm.clm_forward_taps(W, clm._seed_to_tok(text, T), T)
            _tap_cache[text] = h
        return h

    def prompt_of(it, flip=None):
        """The prompt is taken VERBATIM from the manifest (`seed`), never reconstructed.

        H_9327's negation surfaces are `negL` ("이 영화 빠르지 않다 => ") and `negS`
        ("이 영화 안 빠르고 => ") — two different carriers, one of them PREFIXING the negator.
        Rebuilding a carrier from a template would have fed the model a string it was never
        trained on ("빠르지 않고"), and the operator would look dead for a reason that is purely
        ours (reference-match: when the reference is open, read it — do not re-derive it)."""
        return it["seed"]

    def span_of(it, flip=None):
        """Byte span of the stem inside the RIGHT-ALIGNED T-window the engine actually decodes.

        Located by BYTE search inside the verbatim prompt (a_korean_byte_budget: Korean is 3
        bytes/char, and every window/length knob here is a byte budget — mixing chars into it is
        how three prior H's died). rfind, because `negS` puts the negator BEFORE the stem, so the
        stem is still the last occurrence of its own bytes."""
        p = prompt_of(it).encode("utf-8", "surrogateescape")
        sb = it["stem"].encode("utf-8", "surrogateescape")
        t0_abs = p.rfind(sb)
        if t0_abs < 0:
            return None                        # stem not in its own prompt — manifest defect
        t1_abs = t0_abs + len(sb)
        if swap_span == "carrier":
            # operator morpheme span = stem-end → the `=>` marker, spaces trimmed. This is the
            # CARRIER read-site (H_9331 pedestal): the polarity decision completes at `지 않다`,
            # not the atom span (4/4 stem-span INVALID-LOCALIZATION · Fable). The morpheme is
            # byte-identical across flip1 items, so the full-span rung length-matches all donors
            # (the n=4 starvation that hit the stem full-span rung cannot recur here).
            arrow = p.find(b"=>", t1_abs)
            if arrow < 0:
                arrow = p.find(b"=", t1_abs)
            if arrow < 0:
                return None                    # no readout marker after the stem — unusable
            seg = p[t1_abs:arrow]
            lead = len(seg) - len(seg.lstrip(b" "))
            trail = len(seg) - len(seg.rstrip(b" "))
            c0_abs, c1_abs = t1_abs + lead, arrow - trail
            if c1_abs <= c0_abs:
                return None                    # empty operator span (e.g. bare `{stem} =>`)
            t0_abs, t1_abs = c0_abs, c1_abs
        off = T - len(p)                       # right-align: byte i of p sits at window i+off
        t0, t1 = t0_abs + off, t1_abs + off
        if t0 < 0:
            return None                        # stem fell out of the T-byte window — unusable
        return (t0, t1)

    def pool(split, flip):
        return [it for it in items if it.get("split") == split and int(it["flip"]) == flip]

    seen = [it for it in items if it.get("split") == "seen" and int(it["flip"]) == 1]
    novel = [it for it in items if it.get("split") == "novel"]
    heldout = [it for it in items if it.get("split") == "heldout"]
    print("  splits: seen %d · heldout %d · novel %d" % (len(seen), len(heldout), len(novel)))
    if not seen:
        print("BIND-LOCUS ⏳ INVALID-NO-SEEN — Stage A needs SEEN stems (the positive control)")
        json.dump({"verdict": "INVALID-NO-SEEN"}, open(out_path, "w"))
        return 0

    # ── Stage A — locate the operator's read site with a SPIKE-IN (truth we planted) ──────────
    def stem_ladder(it, depth):
        t = span_of(it)
        if t is None:
            return []
        t0, t1 = t
        out = []
        if t1 - 1 >= t0:
            out.append((t1 - 1, t1))                       # last byte
        if t1 - 3 >= t0:
            out.append((t1 - 3, t1))                       # last 3 bytes
        out.append((t0, t1))                               # whole stem
        return out

    pos_seen = [it for it in seen if int(it["pol"]) == 1]
    neg_seen = [it for it in seen if int(it["pol"]) == 0]
    print("\n[Stage A] read-site scan — SEEN swap-patch (positive control · truth known)")
    print("  depth x span-rung -> swap-flip-rate (bar %.2f) / sham (bar %.2f)" % (G_A_SWAP, G_A_SHAM))
    lstar = None
    a_rows = []
    for depth in range(L + 1):
        for rung in range(3):
            flips, shams, n = 0, 0, 0
            for it in pos_seen[:40]:
                sp = stem_ladder(it, depth)
                if rung >= len(sp):
                    continue
                t0, t1 = sp[rung]
                if donor_class == "same":
                    donors = [d for d in pos_seen if d is not it and span_of(d) is not None]
                else:
                    donors = [d for d in neg_seen if span_of(d) is not None]
                if not donors:
                    continue
                dn = donors[n % len(donors)]
                dsp = stem_ladder(dn, depth)
                if rung >= len(dsp):
                    continue
                d0, d1 = dsp[rung]
                if (d1 - d0) != (t1 - t0):
                    continue                                # byte-length mismatch — skip, never pad
                p_self = prompt_of(it)
                donor_h = taps_of(prompt_of(dn))[depth][d0:d1]
                base = _bl_answer_pos(np, W, p_self, T)
                got = _bl_answer_pos_edited(np, W, p_self, T,
                                            [{"layer": depth, "t0": t0, "t1": t1,
                                              "mode": "patch", "donor": donor_h}])
                sham = _bl_answer_pos_edited(np, W, p_self, T,
                                             [{"layer": depth, "t0": t0, "t1": t1,
                                               "mode": "patch", "donor": taps_of(p_self)[depth][t0:t1]}])
                flips += 1 if got != base else 0
                shams += 1 if sham != base else 0
                n += 1
            if n == 0:
                continue
            fr, sr = flips / n, shams / n
            a_rows.append({"depth": depth, "rung": rung, "n": n, "swap": fr, "sham": sr})
            print("  depth %2d rung %d  n=%2d  swap=%.3f  sham=%.3f%s"
                  % (depth, rung, n, fr, sr,
                     "   <- l*" if (lstar is None and fr >= G_A_SWAP and sr <= G_A_SHAM) else ""))
            if lstar is None and fr >= G_A_SWAP and sr <= G_A_SHAM:
                lstar = (depth, rung)
    if lstar is None:
        print("\nBIND-LOCUS ⏳ INVALID-LOCALIZATION — no (depth, span) where a SEEN swap flips the")
        print("  answer >= %.2f with sham <= %.2f. The operator's read is NOT localized to the stem" % (G_A_SWAP, G_A_SHAM))
        print("  span, so an injection there could not test P vs S. This is a locus FACT, not a")
        print("  failed run — and it forbids the P/S verdict rather than faking one.")
        json.dump({"verdict": "INVALID-LOCALIZATION", "swap_span": swap_span,
                   "donor_class": donor_class, "stageA": a_rows,
                   "bars": {"swap": G_A_SWAP, "sham": G_A_SHAM}}, open(out_path, "w"), ensure_ascii=False)
        return 0
    depth, rung = lstar
    print("  l* FROZEN = depth %d, span-rung %d (chosen on SEEN only — no DV data touched it)" % (depth, rung))

    # ── Stage B — axis + projection targets from SEEN (matched on the mediating covariate) ────
    def stem_vec(it):
        sp = stem_ladder(it, depth)
        if rung >= len(sp):
            return None
        t0, t1 = sp[rung]
        return taps_of(prompt_of(it))[depth][t0:t1].mean(axis=0), (t0, t1)

    P = [stem_vec(it) for it in pos_seen]
    N = [stem_vec(it) for it in neg_seen]
    P = [x for x in P if x]; N = [x for x in N if x]
    mu_p = np.mean([x[0] for x in P], axis=0)
    mu_n = np.mean([x[0] for x in N], axis=0)
    v = mu_p - mu_n
    nv = float(np.linalg.norm(v))
    if nv < 1e-12:
        print("BIND-LOCUS ⏳ INVALID-NO-AXIS — SEEN class means coincide at l*")
        json.dump({"verdict": "INVALID-NO-AXIS"}, open(out_path, "w"))
        return 0
    v = v / nv
    tgt_p = float(np.mean([x[0] @ v for x in P]))
    tgt_n = float(np.mean([x[0] @ v for x in N]))
    print("\n[Stage B] axis v = unit(mean_SEEN_pos - mean_SEEN_neg) at l*=%d · |v| pre-norm %.4f" % (depth, nv))
    print("  projection targets (SEEN class means on v): mu+ = %+.4f · mu- = %+.4f" % (tgt_p, tgt_n))
    print("  injection = projection-MATCH to these values (not a fixed alpha — arms are matched on")
    print("  the mediating covariate, control-must-match-mediating-covariate)")

    rng = np.random.RandomState(seed)
    vr = rng.randn(len(v)); vr -= (vr @ v) * v; vr /= (np.linalg.norm(vr) + 1e-12)   # orthogonal to v

    def dep_for(items_pool, flip, mode):
        """Bias-independent dependence: P(ans=pos | inject=pos) - P(ans=pos | inject=neg), paired
        per stem. A global answer bias cancels in the difference by construction (this is H_9327's
        LIE test, now causal)."""
        d, det = [], []
        for it in items_pool:
            if int(it["flip"]) != int(flip):
                continue
            sp = stem_ladder(it, depth)
            if rung >= len(sp):
                continue
            t0, t1 = sp[rung]
            p = prompt_of(it)
            if mode == "sham":
                b = _bl_answer_pos(np, W, p, T)
                s = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                         "mode": "patch", "donor": taps_of(p)[depth][t0:t1]}])
                d.append(1.0 if s != b else 0.0)
                continue
            axis = v if mode == "v" else vr
            a_p = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                      "mode": "proj", "vec": axis, "target": tgt_p}])
            a_n = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                      "mode": "proj", "vec": axis, "target": tgt_n}])
            d.append(a_p - a_n)
            det.append({"id": it.get("id"), "inj_pos": a_p, "inj_neg": a_n})
        return d, det

    def summ(d):
        if not d:
            return {"n": 0, "dep": float("nan"), "se": float("nan")}
        a = np.asarray(d, dtype=np.float64)
        n = len(a)
        se = float(a.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
        return {"n": n, "dep": float(a.mean()), "se": se}

    print("\n[Stage C] arms (DV = bias-independent dependence · paired per stem)")
    res = {}
    for name, pool, flip, mode in (
            ("B_novel_flip0", novel, 0, "v"),
            ("B_novel_flip1", novel, 1, "v"),
            ("C_rescue_flip1", heldout, 1, "v"),
            ("D_randdir_flip1", novel, 1, "rand"),
            ("E_sham_flip1", novel, 1, "sham")):
        d, _ = dep_for(pool, flip, mode)
        res[name] = summ(d)
        print("  %-16s n=%3d  dep=%+.4f  se=%.4f" % (name, res[name]["n"], res[name]["dep"], res[name]["se"]))

    # ── frozen decision tree ─────────────────────────────────────────────────────────────────
    dep0 = res["B_novel_flip0"]["dep"]; dep1 = res["B_novel_flip1"]["dep"]
    dr = res["D_randdir_flip1"]["dep"]; sh = res["E_sham_flip1"]["dep"]
    se1 = res["B_novel_flip1"]["se"]
    print("\n[verdict] V1 l*=(%d,%d) ✅ · V2 dep0=%+.4f (bar >=%.2f) · V3 |dep_rand|=%.4f (<=%.2f) sham=%.4f (<=%.2f)"
          % (depth, rung, dep0, G_V2, abs(dr), G_V3, sh, G_E))
    if not (dep0 >= G_V2):
        verdict = "INVALID-DEAD-INJECTION"
        why = ("the injection is not consumed even by the flip0 readout (dep0 %+.4f < %.2f) — this is "
               "'we cannot find it', NOT 'it is not there'" % (dep0, G_V2))
    elif not (abs(dr) <= G_V3 and sh <= G_E):
        verdict = "INVALID-INSTRUMENT"
        why = ("a control moved: random-direction |dep|=%.4f (bar %.2f) / sham=%.4f (bar %.2f) — the "
               "edit machinery itself perturbs the answer, so no DV may be read"
               % (abs(dr), G_V3, sh, G_E))
    elif dep1 <= G_DV_P:
        verdict = "P — OPERATOR CONSUMES SITE CONTENT"
        why = ("dep1 %+.4f <= %.2f: write the polarity where the operator reads and the answer flips "
               "with it ⇒ the H_9327 wall is an ADDRESS/KIND problem, not a substrate one. "
               "C-rescue dep=%+.4f says whether the CPT stems are repairable in place."
               % (dep1, G_DV_P, res["C_rescue_flip1"]["dep"]))
    elif (not math.isnan(se1)) and abs(dep1) + 1.96 * se1 <= G_TOST:
        verdict = "S — SUBSTRATE (binding is not content-lookup)"
        why = ("dep1 %+.4f is TOST-equivalent to 0 within +-%.2f (|dep|+1.96se = %.4f): the content is "
               "AT the operator's own read site, demonstrably consumable (dep0 %+.4f), and the operator "
               "STILL ignores it ⇒ binding is forged in pretraining, not looked up at inference "
               "(H_9267 XBIND becomes law)." % (dep1, G_TOST, abs(dep1) + 1.96 * se1, dep0))
    else:
        verdict = "UNDERPOWERED"
        why = ("dep1 %+.4f (se %.4f) sits between the P bar (%.2f) and the TOST margin (+-%.2f) — n must "
               "rise; no bar moves (power-before-negative-verdict)" % (dep1, se1, G_DV_P, G_TOST))
    print("\nBIND-LOCUS %s" % verdict)
    print("  %s" % why)
    json.dump({"verdict": verdict, "why": why, "swap_span": swap_span,
               "donor_class": donor_class, "lstar": {"depth": depth, "rung": rung},
               "stageA": a_rows, "targets": {"mu_pos": tgt_p, "mu_neg": tgt_n},
               "arms": res, "bars": {"V1_swap": G_A_SWAP, "V1_sham": G_A_SHAM, "V2": G_V2,
                                     "V3": G_V3, "E": G_E, "DV_P": G_DV_P, "TOST": G_TOST}},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def _ra_H(p):
    """Shannon entropy of a distribution, in BITS (log2). p is a 1-D numpy row summing to 1."""
    import numpy as np
    q = np.clip(np.asarray(p, dtype=float), 1e-300, 1.0)
    return float(-(q * (np.log(q) / math.log(2.0))).sum())


def _ra_js(p, q):
    """Jensen-Shannon divergence in BITS: JS = H((p+q)/2) - (H(p)+H(q))/2.

    Bounded in [0, 1] for ANY alphabet size, which is why the bar can be pre-registered as an
    absolute number before a single route is read: 0.05 bits = 5% of the maximum possible
    separation between two routing distributions. Symmetric and finite (KL is neither)."""
    import numpy as np
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = 0.5 * (p + q)
    return _ra_H(m) - 0.5 * (_ra_H(p) + _ra_H(q))


def _ra_perm(d, n_perm, seed):
    """Two-sided sign-flip permutation p for a paired difference vector d (H0: mean = 0).

    Sign-flip is the right null here: the pairing is WITHIN stem (same stem, two surfaces), so
    under H0 the sign of each stem's difference is exchangeable. Returns (mean, sd, se, p)."""
    import numpy as np
    d = np.asarray(d, dtype=float)
    n = len(d)
    if n == 0:
        return 0.0, 0.0, 0.0, 1.0
    mu = float(d.mean())
    sd = float(d.std(ddof=1)) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        s = sum(x if rng.random() < 0.5 else -x for x in d) / n
        if abs(s) >= abs(mu) - 1e-15:
            hits += 1
    return mu, sd, se, (hits + 1) / (n_perm + 1)


def _ra_read(probs, it, T):
    """The three read points, from ONE forward's [T, E] route matrix.

    ans   probs[T-1]  — the position whose hidden the readout turns into the answer's first byte.
                        THE primary: it is the only position whose route can be said to have
                        'computed the answer'.
    stem  mean over the stem's byte span (right-aligned into the window by the manifest)
    win   mean over the non-pad region (the seed's own bytes; the left pad is spaces and carries
          no surface information, so averaging over it would dilute every contrast equally)"""
    import numpy as np
    t0, t1 = it["stem_span"]
    off = max(0, T - int(it["seed_bytes"]))
    ans = np.asarray(probs[T - 1], dtype=float)
    stem = np.asarray(probs[t0:t1], dtype=float).mean(axis=0)
    win = np.asarray(probs[off:T], dtype=float).mean(axis=0)
    return {"ans": ans, "stem": stem, "win": win}


def _ra_forward(ckpt, items, T, note, gn_ref=""):
    """Run the engine-native route tap over every item of the manifest. Returns
    (reads, meta) where reads[id][point] = the [E] route distribution.

    gn_ref (H_9611/H_9612): if non-empty, pin every GroupNorm's mu/var to the constants this
    ONE pre-registered reference forward produces, so the normalizer is input-independent and
    the trunk is strictly RF-local (the sequence-global GN bus is deleted; the affine is
    untouched). Empty = live GN = byte-identical to the pre-flag behaviour. Wired here because
    route_audit's W is loaded inside this function — before, `--route-audit --gn-freeze` parsed
    the flag at the CLI allowlist and then SILENTLY IGNORED it, so the run read a false
    "no difference" (the footgun H_9612 found)."""
    import numpy as np
    import time
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable: " + ckpt, file=sys.stderr)
        return None, None
    if gn_ref:
        _st = clm.gn_freeze_calibrate(W, clm._seed_to_tok(gn_ref, T), T)
        clm.gn_freeze_set(_st)
        print("  [gn-freeze] %s — %d GN sites pinned from ref (%d bytes · pre-registered, not swept)"
              % (note, len(_st), len(gn_ref)), flush=True)
    E = int(W["E"]); L = int(W["L"]); K = int(W["K"])
    dev = "GPU" if clm.cuda_available() else "CPU"
    print("  [%s] %s · E=%d experts · L=%d · K=%d · device=%s" % (note, ckpt, E, L, K, dev))
    reads, ent, sham = {}, [], 0.0
    t_start = time.time()
    for i, it in enumerate(items):
        tok = clm._seed_to_tok(it["seed"], T)
        probs = clm.clm_forward_routes(W, tok, T)["probs"]
        r = _ra_read(probs, it, T)
        # G-SHAM: the metric must be exactly 0 against itself. A JS that is not 0 on p-vs-p is
        # a broken estimator, and every number downstream of it is noise (the pedestal lesson).
        sham = max(sham, abs(_ra_js(r["ans"], r["ans"])))
        ent.append(_ra_H(r["ans"]))
        reads[it["id"]] = r
        # heartbeat from item ONE (evaluate-py-9): a first beat at item 50 makes a 303M forward
        # that is merely SLOW indistinguishable from one that is hung, and the wrong call there
        # kills live compute.
        if i == 0 or (i + 1) % 50 == 0:
            print("    %d/%d  (%.0fs)" % (i + 1, len(items), time.time() - t_start), flush=True)
    # free the 303M weight dict before the next ckpt loads — two f64 copies of a 303M model is
    # ~4.8 GB and summer's earlyoom kills python3 BY POLICY, which would read as a fake infra wall
    try:
        k = clm._wload_key(ckpt)
        if k is not None:
            clm._WLOAD_CACHE.pop(k, None)
    except Exception:
        pass
    meta = {"E": E, "L": L, "K": K, "device": dev, "sham_max": sham,
            "route_entropy_mean": float(np.mean(ent)), "route_entropy_max_possible": math.log2(E)}
    return reads, meta


def route_audit_run(argv):
    """`anima-py evaluate <ckpt> --route-audit <manifest.json> [--vs <ckpt2>] --out <f.json>`
    — H_9355 LOCUS-CAUSAL, the AUDIT half: do the declarative lane and the operator lane live on
    PHYSICALLY DIFFERENT ConvMoE experts?

    Why this and not another hidden-space probe. The two-lane reading of the binding wall (C3/C4:
    a declarative store and an operator store that never exchange values) is, so far, a purely
    behavioural inference. It makes exactly one PHYSICAL prediction this substrate can answer:
    if the lanes are separate stores, the two surfaces should be COMPUTED BY DIFFERENT EXPERTS.
    The router is the only place in a ConvMoE where "which machinery ran" is explicit, and it is
    a number the model itself emits — not a linear probe's opinion about a hidden.

      LOCUS-SPLIT   the operator surface routes elsewhere than the declarative surface, beyond
                    what an equally-long inert suffix does  -> two-lane is PHYSICAL, and a
                    route-pin intervention (bias the router at inference) becomes a live
                    "read without writing" candidate
      LOCUS-SHARED  same route  -> two-lane is not a store split; the gap is coding/geometry
                    inside one shared machine, and route-pin is dead on arrival

    ⚠️ NOT the dead forkA (Gate4 · eval_rho_weave): that was a READOUT-routing REFRAME of the G1
    ideation metric and died of frame-mismatch. This audits WHERE A WRITE LANDS in a live
    ConvMoE — a different object, a different question, and the ledger says so.

    The trap this instrument is built to avoid: the router is a function of the BYTE STRING, so
    flip0 -> negL moves the route TRIVIALLY (the strings differ). Two controls, both PAIRED
    within stem (never max() over controls — probe-defect-census-max-control-bias):
      ped   an inert 10-byte suffix, byte-length-matched to negL's '지 않다'  -> "does ANY suffix move it"
      negJ  '지는 않다' — negL's string twin, on which the operator DEMONSTRABLY DOES NOT RUN
            (C1b p~.50)                                                       -> "is the move OPERATOR-specific"

    Frozen bars (pre-registered before any number was read; they never move):
      G-SHAM   JS(p,p) == 0 exactly, all items                     else INVALID-ESTIMATOR
      G-LIVE   J_STEM (mean JS between two random stems, SAME surface) >= 0.0001 bits
               — the router must vary with CONTENT at all. If it does not, the lens is blind and
               the audit is discarded as ROUTE-INDIFFERENT: honest negative, NOT a wall, and NOT
               evidence for either model (a constant router cannot separate anything).
      DV       dOP = mean_stem [ JS(flip0,negX) - JS(flip0,ped) ], X in {negL, negZ}
               LOCUS-SPLIT  iff dOP >= 0.05 bits on BOTH strong surfaces, sign-flip perm p <= .01,
                            AND the sign agrees across both CPT seeds
               LOCUS-SHARED iff the 90% CI of dOP lies inside +-0.02 bits (TOST) on both
               else         UNDERPOWERED (report se + MDE; no bar moves — power-before-negative)
      OP-SPEC  dOPJ = mean_stem [ JS(flip0,negL) - JS(flip0,negJ) ] — reported alongside. A split
               that negJ reproduces is a STRING effect wearing the operator's clothes.

    --vs runs a SECOND ckpt in the SAME process, on the SAME device, and reports D_CPT =
    mean_stem JS(route_base, route_post) per surface. Two processes would have been simpler and
    wrong: the router logits come out of cuBLAS dgemm, so a CPU run and a GPU run are not the
    same measurement (convergence decode-py-4) — pinning both ckpts to one process makes the
    device confound structurally impossible instead of merely unlikely.
    """
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--route-audit", "")))
    ckpt2 = evaluate_strval(argv[1:], "--vs", "")
    out_path = evaluate_strval(argv[1:], "--out", "route_audit.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_perm = evaluate_intval(argv[1:], "--perm", 10000)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    # frozen bars — written before the first forward (no tune-to-green)
    G_SHAM, G_LIVE, G_DV, G_TOST, A_PERM = 0.0, 0.0001, 0.05, 0.02, 0.01
    Z90 = 1.645                          # 90% CI half-width multiplier -> TOST at alpha .05

    # G-SPIKE — the truth-known pedestal for the ESTIMATOR itself (phi-estimator-needs-zero-truth-
    # pedestal · tool-definition-read-code-not-docstring). Two disjoint one-hot routes are exactly
    # 1 bit apart and a distribution is exactly 0 bits from itself; if _ra_js cannot reproduce
    # those two constants, every JS below is noise and no verdict may be read off it.
    E_spike = 3
    one_a = [1.0] + [0.0] * (E_spike - 1)
    one_b = [0.0, 1.0] + [0.0] * (E_spike - 2)
    unif = [1.0 / E_spike] * E_spike
    spike, zero = _ra_js(one_a, one_b), _ra_js(unif, unif)
    spike_ok = abs(spike - 1.0) < 1e-12 and abs(zero) < 1e-12
    print("  G-SPIKE  JS(one-hot A, one-hot B) = %.6f (truth 1.000000) · JS(u,u) = %.3e  %s"
          % (spike, zero, _pf(spike_ok)))
    if not spike_ok:
        print("ERROR: the JS estimator fails its own truth-known pedestal — refusing to measure.",
              file=sys.stderr)
        return 2
    # Scale note, recorded BEFORE any number is read so nobody can call it post-hoc: JS is
    # QUADRATIC in the routing shift near a uniform router. At E=3, dOP = 0.05 bits corresponds to
    # roughly an 11-point shift in expert mass — i.e. the bar asks for "a different expert ran",
    # not "the mix wobbled". A reliable-but-tiny shift therefore lands in LOCUS-SHARED by design,
    # and the top-expert agreement rate below is reported so that call can be audited.

    print("=== anima-py evaluate --route-audit — H_9355 LOCUS-CAUSAL: two lanes, one expert or two? ===")
    print("  %d items · win %dB · perm %d · seed %d" % (len(items), T, n_perm, seed))
    print("  frozen: G-SHAM JS(p,p)==0 · G-LIVE J_STEM>=%.4f bits · DV dOP>=%.2f bits & perm p<=%.3f"
          % (G_LIVE, G_DV, A_PERM))
    print("  frozen: LOCUS-SHARED iff 90%% CI of dOP inside +-%.2f bits (TOST) · else UNDERPOWERED"
          % G_TOST)

    # H_9612 · --gn-freeze <ref>: pin GN mu/var from ONE pre-registered reference forward so the
    # trunk is strictly RF-local. Threaded into _ra_forward (where W is loaded) — the flag used to
    # be accepted by the CLI allowlist and then silently dropped here, which reads as a false
    # "no difference". Empty = live GN = byte-identical.
    gn_ref = evaluate_strval(argv[1:], "--gn-freeze", "")
    if gn_ref and os.path.exists(gn_ref):
        gn_ref = open(gn_ref, "r").read()
    base, meta = _ra_forward(ckpt, items, T, "base", gn_ref)
    if base is None:
        return 2
    post, meta2 = (None, None)
    if ckpt2:
        post, meta2 = _ra_forward(ckpt2, items, T, "vs", gn_ref)
        if post is None:
            return 2
        if meta2["device"] != meta["device"]:
            print("ERROR: the two ckpts fired on different devices (%s vs %s) — the route comparison "
                  "would carry a device confound (decode-py-4). Refusing to score."
                  % (meta["device"], meta2["device"]), file=sys.stderr)
            return 2

    by = {}                                          # by[stem][surf] = read dict
    split_of, pol_of = {}, {}
    for it in items:
        by.setdefault(it["stem"], {})[it["surf"]] = base[it["id"]]
        split_of[it["stem"]] = it["split"]
        pol_of[it["stem"]] = int(it["pol"])
    stems = sorted(by)
    surfs = sorted({it["surf"] for it in items})
    need = ("flip0", "negL", "negZ", "negJ", "ped")
    missing = [s for s in need if s not in surfs]
    if missing:
        print("ERROR: manifest is missing surface(s) " + ",".join(missing), file=sys.stderr)
        return 2

    # H_9612 · PER-SURFACE PEDESTAL + byte-length audit.
    # The docstring above says ped is "byte-length-matched to negL's '지 않다'" (10 B) — and it is.
    # But the DV runs X in {negL, negZ} against that SAME ped, and negZ ('지가 않다') is 13 B. Under
    # the right-aligned window a 3-byte delta SHIFTS the whole seed, so the two arms are read at
    # different absolute positions with different beyond-RF context behind them — and H_9611 measured
    # a sequence-global GroupNorm bus that carries exactly such a shift to the readout. So negZ's
    # excess over ped conflated "operator-specific" with "3 bytes longer".
    #   `ctrl_of` (manifest, optional) maps each DV surface to ITS length-matched pedestal, e.g.
    #   {"negL": "ped", "negZ": "ped13"}. Absent => every surface falls back to "ped" == the exact
    #   pre-flag behaviour (byte-identical), so no cemented number moves by this commit alone.
    ctrl_of = dict(spec.get("ctrl_of") or {})
    for s in ("negL", "negZ"):
        ctrl_of.setdefault(s, "ped")
    bad = [c for c in set(ctrl_of.values()) if c not in surfs]
    if bad:
        print("ERROR: ctrl_of names surface(s) absent from the manifest: " + ",".join(sorted(bad)),
              file=sys.stderr)
        return 2
    # byte-length audit — LOUD, never silent: a DV pair whose seeds differ in length is a
    # length-shift confound (H_9612), and the reader must see it inline, not discover it later.
    blen = {}
    for it in items:
        blen.setdefault(it["surf"], set()).add(int(it["seed_bytes"]) - len(it["stem"].encode()))
    mism = []
    for s in ("negL", "negZ"):
        c = ctrl_of[s]
        ls, lc = sorted(blen.get(s, {0}))[0], sorted(blen.get(c, {0}))[0]
        tag = "🟢 matched" if ls == lc else "⚠️ +%dB SHIFT" % (ls - lc)
        if ls != lc:
            mism.append("%s(%dB) vs %s(%dB)" % (s, ls, c, lc))
        print("  [len-audit] %-5s %2dB  vs ctrl %-5s %2dB   %s" % (s, ls, c, lc, tag))
    if mism:
        print("  ⚠️ LENGTH-SHIFT CONFOUND (H_9612): " + " · ".join(mism) + " — the right-aligned "
              "window shifts, so beyond-RF context differs between the arms and the GroupNorm bus "
              "(H_9611) can carry that difference into dOP. Supply a length-matched pedestal via "
              "the manifest's ctrl_of, or read dOP for that arm as operator+shift, not operator.",
              flush=True)

    res = {"ckpt": ckpt, "vs": ckpt2, "meta": meta, "meta_vs": meta2, "n_stems": len(stems),
           # H_9612: which pedestal each DV surface was scored against, + whether the pair was
           # byte-length matched. Recorded so a reader can never mistake operator+shift for operator.
           "ctrl_of": ctrl_of, "gn_freeze": bool(gn_ref), "len_mismatch": mism,
           "bars": {"G_SHAM": G_SHAM, "G_LIVE": G_LIVE, "G_DV": G_DV, "G_TOST": G_TOST,
                    "alpha_perm": A_PERM},
           "points": {}}

    # ── G-SHAM ────────────────────────────────────────────────────────────────────────────
    sham_ok = meta["sham_max"] <= G_SHAM
    print("\nG-SHAM  JS(p,p) max = %.3e  %s" % (meta["sham_max"], _pf(sham_ok)))
    print("        router entropy (ans point) mean %.6f bits / max %.6f (E=%d)"
          % (meta["route_entropy_mean"], meta["route_entropy_max_possible"], meta["E"]))

    verdicts = {}
    # every surface the scoring below touches: the frozen `need` set + whatever pedestals ctrl_of
    # names (H_9612). With no ctrl_of this is exactly `need`, so P is byte-identical.
    allf = tuple(need) + tuple(sorted(c for c in set(ctrl_of.values()) if c not in need))
    for point in ("ans", "stem", "win"):
        P = {s: {f: by[s][f][point] for f in allf} for s in stems}

        # ── G-LIVE: does the route vary with CONTENT at all? (same surface, different stems) ──
        rng = random.Random(seed)
        pairs = [(rng.choice(stems), rng.choice(stems)) for _ in range(400)]
        jstem = [_ra_js(P[a]["flip0"], P[b]["flip0"]) for a, b in pairs if a != b]
        J_STEM = float(np.mean(jstem)) if jstem else 0.0

        jsL = [_ra_js(P[s]["flip0"], P[s]["negL"]) for s in stems]
        jsZ = [_ra_js(P[s]["flip0"], P[s]["negZ"]) for s in stems]
        jsJ = [_ra_js(P[s]["flip0"], P[s]["negJ"]) for s in stems]
        jsP = [_ra_js(P[s]["flip0"], P[s]["ped"]) for s in stems]

        row = {"J_STEM": J_STEM, "js_mean": {"negL": float(np.mean(jsL)), "negZ": float(np.mean(jsZ)),
                                             "negJ": float(np.mean(jsJ)), "ped": float(np.mean(jsP))}}
        # top-expert agreement (DIAGNOSTIC, no bar): JS is quadratic near a uniform router, so a
        # reliable-but-tiny shift reads as LOCUS-SHARED. If the ARGMAX expert nevertheless flips
        # between the two surfaces for most stems, that is a qualitatively different fact and this
        # line is what keeps the JS verdict auditable instead of merely obeyed.
        row["top_agree"] = {f: float(np.mean([int(np.argmax(P[s]["flip0"]) == np.argmax(P[s][f]))
                                              for s in stems])) for f in ("negL", "negZ", "negJ", "ped")}
        row["top_hist"] = {f: [int(sum(1 for s in stems if int(np.argmax(P[s][f])) == e))
                               for e in range(len(P[stems[0]]["flip0"]))] for f in need}
        # H_9612: each DV surface is scored against ITS OWN pedestal (ctrl_of). Default ctrl_of maps
        # both to "ped" => jsCtrl is jsP => byte-identical to the pre-flag DV.
        jsCtrl = {t: [_ra_js(P[s]["flip0"], P[s][ctrl_of[t]]) for s in stems] for t in ("negL", "negZ")}
        for tag, js in (("negL", jsL), ("negZ", jsZ)):
            d = [a - b for a, b in zip(js, jsCtrl[tag])]             # DV: operator minus pedestal
            mu, sd, se, p = _ra_perm(d, n_perm, seed)
            dj = [a - b for a, b in zip(js, jsJ)]                    # OP-SPEC: operator minus twin
            mj, sj, sej, pj = _ra_perm(dj, n_perm, seed)
            lo, hi = mu - Z90 * se, mu + Z90 * se
            row[tag] = {"dOP": mu, "sd": sd, "se": se, "p_perm": p, "ci90": [lo, hi],
                        "MDE80": 2.8 * se, "dOPJ": mj, "p_perm_J": pj, "se_J": sej}

        # per-stratum + control ② (polarity, same surface): does the ROUTE know the polarity?
        for st in ("seen", "heldout"):
            ss = [s for s in stems if split_of[s] == st]
            if len(ss) >= 3:
                d = [_ra_js(P[s]["flip0"], P[s]["negL"])
                     - _ra_js(P[s]["flip0"], P[s][ctrl_of["negL"]]) for s in ss]
                mu, sd, se, p = _ra_perm(d, min(n_perm, 2000), seed)
                row["stratum_" + st] = {"n": len(ss), "dOP_negL": mu, "se": se, "p_perm": p}
        pos = [P[s]["flip0"] for s in stems if pol_of[s] == 1]
        neg = [P[s]["flip0"] for s in stems if pol_of[s] == 0]
        if pos and neg:
            row["J_POL"] = _ra_js(np.mean(pos, axis=0), np.mean(neg, axis=0))

        # ── the frozen decision tree ──────────────────────────────────────────────────────
        if not sham_ok:
            v = "⛔ INVALID-ESTIMATOR"
        elif J_STEM < G_LIVE:
            v = "⚪ ROUTE-INDIFFERENT"
        elif all(row[t]["dOP"] >= G_DV and row[t]["p_perm"] <= A_PERM for t in ("negL", "negZ")):
            v = "🟢 LOCUS-SPLIT"
        elif all(row[t]["ci90"][0] > -G_TOST and row[t]["ci90"][1] < G_TOST for t in ("negL", "negZ")):
            v = "🔵 LOCUS-SHARED"
        else:
            v = "⏳ UNDERPOWERED"
        row["verdict"] = v
        verdicts[point] = v
        res["points"][point] = row

        print("\n[%s]  J_STEM %.6f (G-LIVE %.6f) %s · J_POL %.6f"
              % (point, J_STEM, G_LIVE, _pf(J_STEM >= G_LIVE), row.get("J_POL", float("nan"))))
        print("   JS(flip0,·) mean:  negL %.6f · negZ %.6f · negJ %.6f · ped %.6f"
              % (row["js_mean"]["negL"], row["js_mean"]["negZ"],
                 row["js_mean"]["negJ"], row["js_mean"]["ped"]))
        print("   top-expert agreement with flip0:  " + " · ".join(
            "%s %.2f" % (f, v) for f, v in sorted(row["top_agree"].items())))
        print("   top-expert histogram (over %d stems): " % len(stems) + " · ".join(
            "%s %s" % (f, row["top_hist"][f]) for f in need))
        for tag in ("negL", "negZ"):
            r = row[tag]
            print("   dOP[%s] = %+.6f bits (se %.6f · CI90 [%+.6f,%+.6f] · perm p %.4f · MDE80 %.6f)"
                  % (tag, r["dOP"], r["se"], r["ci90"][0], r["ci90"][1], r["p_perm"], r["MDE80"]))
            print("      OP-SPEC vs negJ twin: dOPJ = %+.6f (perm p %.4f)" % (r["dOPJ"], r["p_perm_J"]))
        for st in ("seen", "heldout"):
            k = "stratum_" + st
            if k in row:
                print("      stratum %-7s n=%2d  dOP[negL] %+.6f (se %.6f · p %.4f)"
                      % (st, row[k]["n"], row[k]["dOP_negL"], row[k]["se"], row[k]["p_perm"]))
        print("   -> " + v)

    # ── --vs: where did the CPT WRITE land? (same process, same device) ───────────────────
    if post is not None:
        print("\nD_CPT — how far the C4 write MOVED the route, per surface (JS(base, post), ans point)")
        dc = {}
        for f in need:
            for st in ("seen", "heldout"):
                ids = [it["id"] for it in items if it["surf"] == f and it["split"] == st]
                if not ids:
                    continue
                v = [_ra_js(base[i]["ans"], post[i]["ans"]) for i in ids]
                dc.setdefault(f, {})[st] = {"n": len(v), "mean": float(np.mean(v)),
                                            "max": float(np.max(v))}
        for f in need:
            if f in dc:
                print("   %-6s " % f + " · ".join(
                    "%s n=%2d mean %.6f max %.6f" % (st, d["n"], d["mean"], d["max"])
                    for st, d in sorted(dc[f].items())))
        res["D_CPT"] = dc

    res["verdicts"] = verdicts
    res["verdict"] = verdicts.get("ans", "⛔ INVALID")
    print("\nVERDICT (primary read point = ans): " + res["verdict"])
    json.dump(_json_safe(res), open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def xbind_run(argv):
    """`anima-py evaluate <ckpt> --xbind <manifest.json>` — held-out XBIND recombination
    (G1 reopen lane a · card H_9267). Engine-native numpy core/decode.py only
    (a_eval_py_canonical -> TERMINAL-eligible). Design SSOT: state/g1_reopen_xbind/DESIGN_PREREG.md.
    PRIMARY D-acc = greedy(top_k=1) first-word == gold branch word, per split {heldout, seen}.
    C-rate = order-covariant portmanteau on gold-fuse held-out (constructive tier). MARGIN =
    teacher-forced NLL(counterfactual)-NLL(gold). All raw outputs dumped (never tail-truncate
    a control · evaluate-py-1). --arm ctrl scores the shuffle-control model."""
    import numpy as np
    import time
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--xbind", "")
    out_path = evaluate_strval(argv[1:], "--out", "xbind_eval.json")
    arm = evaluate_strval(argv[1:], "--arm", "main")
    spec = json.load(open(spec_path))

    # --surface-set <name|path> (KEY-LADDER · H_9378): re-render the SAME arms + the SAME planted
    # polarities across a pre-registered LADDER of operator surfaces, and score every rung. The
    # manipulation is the SCORED SURFACE and nothing else — no retrain, no new corpus, no new arm
    # draw (the arms are read back out of the manifest the CPT was built from, so they cannot drift
    # away from the checkpoint). Registry + byte-budget gate live in cli/corpus.py, which owns the
    # templates; keeping them in one place is what stops a ladder rung from disagreeing with the
    # corpus it is supposed to be probing.
    surf_set = evaluate_strval(argv[1:], "--surface-set", "")
    lad_audit = None
    if surf_set:
        sys.path.insert(0, _HERE)
        import corpus as _corpus_mod
        _lad = _corpus_mod.load_surface_set(surf_set)
        spec, lad_audit = _corpus_mod.expand_surface_ladder(
            spec, _lad, win=evaluate_intval(argv[1:], "--win", int(spec.get("win", 64))))

    gen = evaluate_intval(argv[1:], "--gen", int(spec.get("gen", 16)))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 200)
    n_smp = evaluate_intval(argv[1:], "--n-sampled", 40)

    # --consult (H_9309 DECON · A-channel): a declarative store {atom: {key, pol}} whose fact is
    # rendered into the CONTEXT of the 2AFC scoring window. It is the only structurally valid
    # injection point: free-generation D-acc cannot see it (clm_decode_topk_sampled_W hardcodes
    # T=24, core/decode.py:1094), so the primary instrument here is the margin-2AFC alone.
    # EMPTY store => byte-identical to a plain --xbind run (parity gate).
    consult_path = evaluate_strval(argv[1:], "--consult", "")
    consult_fmt = evaluate_strval(argv[1:], "--consult-format", "F1")
    store = json.load(open(consult_path)) if consult_path else {}
    # H_9407 · --consult-decode: route the rendered declaration into the FREE-DECODE seed (window
    # widened from the production 24 to the ckpt's real RF) so the GENERATION surface — not just the
    # 2AFC scoring lane — is asked whether it can address a declaration. Default OFF ⇒ byte-identical.
    consult_decode = "--consult-decode" in argv[1:]
    cd_win = int(evaluate_strval(argv[1:], "--consult-decode-win", "0") or "0")     # 0 = auto (RF)
    cd_filler = int(evaluate_strval(argv[1:], "--consult-decode-filler", "0") or "0")

    # A manifest bigger than --n-decode used to be sliced away in SILENCE (`spec[split][:n_dec]`), and
    # the slice takes the FIRST n_dec rows in manifest order — so whole stems fall off the end while
    # the run still prints as though it had covered the manifest. It bit the EN arm: a 240-row held-out
    # manifest scored 200 rows (n=101 flip0 / 99 flip1) and the six stems ordered last vanished. Nothing
    # in the output said so. A cap nobody reports reads as full coverage, which is the one thing a
    # verdict may never get wrong — so it now REFUSES, and it refuses BEFORE loading 176MB of weights.
    # The row count is a property of the manifest, and the manifest is pre-registered: raise --n-decode.
    for _split in ("heldout", "seen"):
        _have = len(spec.get(_split, []))
        if _have > n_dec:
            print("ERROR: --xbind manifest split '%s' has %d rows but --n-decode is %d."
                  % (_split, _have, n_dec))
            print("  Scoring would drop the LAST %d rows — whole stems, not a random sample — and"
                  % (_have - n_dec))
            print("  report the remainder as if it were the manifest.")
            print("  Fix:  --n-decode %d" % _have)
            return 1

    print("=== anima evaluate --xbind — held-out XBIND recombination (G1 reopen lane a) ===")
    print("ckpt: " + ckpt + "  arm=" + arm + "  gen=%d win=%d" % (gen, T))
    if lad_audit:
        print("surface-set: %s — %d surfaces x %d stems = %d rows  (arms: %s)  max_row=%dB/%dB"
              % (lad_audit["surface_set"], lad_audit["n_surfaces"], lad_audit["n_stems"],
                 lad_audit["n_rows"],
                 " ".join("%s=%d" % (k, v) for k, v in sorted(lad_audit["arm_n"].items())),
                 lad_audit["max_row_bytes"], lad_audit["win"]))
        print("  rungs: " + " ".join(lad_audit["tags"]))
    if store:
        print("consult: %s  (%d facts · format=%s) — injected into the 2AFC context only"
              % (consult_path, len(store), consult_fmt))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    # H_9611 --gn-freeze <ref>: pin every GN's mu/var to this ONE pre-registered reference
    # forward ⟹ the normalizer is input-independent ⟹ the trunk is strictly RF-local (the
    # sequence-global GN bus is deleted; affine untouched). H_9611 measured beyond-RF influence
    # collapsing to EXACTLY 0 under the freeze while within-RF survives, so replaying a cemented
    # --xbind score under it isolates whether that global channel ever moved the SCORE (the
    # hidden-channel isolation is already done; this is the verdict-replay arm). Never swept.
    gn_ref = evaluate_strval(argv[1:], "--gn-freeze", "")
    if gn_ref:
        if os.path.exists(gn_ref):
            gn_ref = open(gn_ref, "r").read()
        _st = clm.gn_freeze_calibrate(W, clm._seed_to_tok(gn_ref, T), T)
        clm.gn_freeze_set(_st)
        print("  [gn-freeze] ON — %d GN sites pinned from ref (%d bytes · pre-registered, not swept)"
              % (len(_st), len(gn_ref)), flush=True)

    # H_9407 · consult-decode window + structural pre-flight (mirror of the n_dec refusal above).
    t_dec = None
    if consult_decode:
        rf = (W["K"] - 1) * (1 + sum(min(2 ** i, 512) for i in range(W["L"])) + 1) + 1
        t_dec = cd_win if cd_win > 0 else min(rf, 1024)   # 1024 = trained seq_len ceiling
        clm.set_consult_decode_window(t_dec)
        print("consult-decode: T_dec=%d  (RF_analytic=%d · production window=24 · trained seq=1024)  filler=%dB"
              % (t_dec, rf, cd_filler))
        # ALL arms decode at ONE t_dec (the zero-fill-below-RF physics · decode-py-4 device-pin: pin one
        # device too). A declaration that cannot sit in-window WITH the stem cannot be tested here.
        if store and cd_filler == 0:
            max_row = 0
            for _split in ("heldout", "seen"):
                for it in spec.get(_split, []):
                    fact = store.get(it.get("a")) or store.get(it.get("b"))
                    if not fact:
                        continue
                    nb = len((_consult_render(fact, consult_fmt) + it["seed"]).encode())
                    if nb > max_row:
                        max_row = nb
            if max_row + gen > t_dec:
                print("INVALID-STRUCTURAL: consult-decode window T_dec=%d < max row %dB + gen %d."
                      % (t_dec, max_row, gen))
                print("  The declaration and the stem cannot be simultaneously visible at the generation")
                print("  point — the probe cannot distinguish 'deaf' from 'blind'. Finding: generation-")
                print("  surface addressing needs a wider-window ckpt, NOT a negative on addressing.")
                return 1

    res = {"ckpt": ckpt, "arm": arm, "gen": gen, "win": T, "t_dec": t_dec, "consult_decode": consult_decode, "splits": {}}
    for split in ("heldout", "seen"):
        items = spec[split]
        t_split = time.time()
        rows = []
        d_hits = c_hits = c_n = 0
        margins = []
        # Stall watchdog. An eval that stops making progress must SAY so, not sit there.
        #
        # Measured (2026-07-14): a G-base run on a pool box hung at item 50 of 60 — eta 37 seconds —
        # and stayed there for forty minutes. No error, no exit, no output file. A neighbouring
        # session had saturated the host's RAM and wedged sshd, so the box was gone; but from the
        # orchestration side the run looked exactly like a slow one, and the only reason anyone found
        # out was that someone went and looked. Forty minutes of a rented clock, and the chain behind
        # it (two CPTs queued on that eval finishing) never started.
        #
        # A run that has completed items has told us how long an item takes. If one then takes
        # WATCHDOG_X times the median of the last few, the box is not slow — something has stopped.
        # Die loudly, with the numbers, so the caller can re-fire somewhere else in two minutes
        # instead of discovering the corpse in forty.
        WATCHDOG_X = 20.0
        WATCHDOG_FLOOR = 120.0          # never trip inside the first two minutes of a single item
        recent = []
        t_item = time.time()
        for ix, it in enumerate(items):
            gold_w = it["gold_word"]
            if arm == "ctrl" and split == "seen":
                gold_w = it["gold_word_ctrl"]
            # H_9407 · free-decode seed: consult declaration + filler + stem when --consult-decode,
            # else the plain stem seed (byte-identical). The scoring/margin lane below is left UNTOUCHED
            # (the run's own positive control = the H_9334/9347 margin under this exact ckpt+manifest).
            seed_dec, cdu = (it["seed"], None)
            if consult_decode:
                seed_dec, cdu = _consult_decode_seed(it, store, consult_fmt, t_dec, cd_filler, gen)
            o = clm.clm_decode_topk_sampled_W(W, seed_dec, gen, 1, 0.7, 7)["text"]
            fw = _xbind_first_word(o)
            d_hit = int(fw == gold_w)
            d_hits += d_hit
            c_hit = None
            if it.get("construct") and arm == "main":
                c_hit = int(it["construct"] in o)
                c_hits += c_hit
                c_n += 1
            seed_m, cused = _consult_seed(it["seed"], it, store, consult_fmt, T,
                                          it["gold"], it["counterfactual"])
            mg = (_xbind_cont_nll(np, clm, W, seed_m, it["counterfactual"], T)
                  - _xbind_cont_nll(np, clm, W, seed_m, it["gold"], T))
            margins.append(mg)
            smp = None
            if ix < n_smp:
                votes = 0
                for r in (7, 4302, 4303):
                    os_ = clm.clm_decode_topk_sampled_W(W, seed_dec, gen, 40, 0.7, r)["text"]
                    votes += int(_xbind_first_word(os_) == gold_w)
                smp = int(votes >= 2)
            rows.append({"a": it["a"], "b": it["b"], "gold_word": gold_w,
                         "first_word": fw, "d_hit": d_hit, "c_hit": c_hit,
                         "margin": mg, "sampled_maj": smp, "raw": o,
                         "consult": cused, "consult_decode": cdu,
                         # carried through so the summary can split the headline (_xbind_breakdown)
                         "flip": it.get("flip"), "pol": it.get("pol"),
                         # --surface-set: the rung this row sits on. Carried into the dump so the
                         # address map can be rebuilt from the JSON alone, with no side table.
                         "surf_tag": it.get("surf_tag"), "surf_class": it.get("surf_class"),
                         "surf_role": it.get("surf_role")})
            # Heartbeat at item 1, then every 25. The first item is what makes a slow host
            # legible: each item is ~10 model forwards, so on a saturated shared box one item
            # can cost minutes — and a 25-item-only cadence then means HOURS of total silence,
            # indistinguishable from a hang. (2026-07-13: a 174-item run on a rented box whose
            # load average sat at ~106 from other tenants emitted nothing for 5h; the only way
            # to tell "slow" from "stuck" was to hand-roll a 2-item manifest. The ETA below
            # would have said "35h on this host" after ~30 seconds.)
            dt = time.time() - t_item
            t_item = time.time()
            if recent:
                med = sorted(recent)[len(recent) // 2]
                limit = max(WATCHDOG_FLOOR, WATCHDOG_X * med)
                if dt > limit:
                    sys.exit(
                        "\nanima-py evaluate: STALLED — item %d/%d of split '%s' took %.0fs.\n"
                        "  the last %d items ran at a median of %.1fs each; the limit is %.0fs "
                        "(%.0fx median).\n"
                        "  This is not a slow box, it is a stopped one. The usual cause is the HOST\n"
                        "  going away underneath us — a neighbouring job saturating RAM, an OOM\n"
                        "  reaper, a wedged sshd. Nothing that follows would have been measured.\n\n"
                        "  Check the host (uptime, free, nvidia-smi, who else is on it), then re-fire\n"
                        "  somewhere that is not carrying someone else's load.\n"
                        % (ix + 1, len(items), split, dt, len(recent), med, limit, WATCHDOG_X))
            recent.append(dt)
            recent = recent[-9:]
            if ix == 0 or (ix + 1) % 25 == 0:
                el = time.time() - t_split
                per = el / (ix + 1)
                eta = per * (len(items) - ix - 1)
                print("  [xbind %s #%d/%d] d_acc=%.3f  %.1fs/item  elapsed=%s  eta=%s" %
                      (split, ix + 1, len(items), d_hits / (ix + 1), per,
                       _xbind_hms(el), _xbind_hms(eta)), flush=True)
        margins.sort()
        med = margins[len(margins) // 2] if margins else 0.0
        smp_rows = [r["sampled_maj"] for r in rows if r["sampled_maj"] is not None]
        summ = {"n": len(items), "d_acc": d_hits / max(1, len(items)),
                "c_rate": (c_hits / c_n) if c_n else None, "c_n": c_n,
                "margin_median": med,
                "margin_frac_pos": sum(1 for m in margins if m > 0) / max(1, len(margins)),
                "sampled_maj_acc": (sum(smp_rows) / len(smp_rows)) if smp_rows else None}
        if store:
            # byte-audit (a_korean_byte_budget): a Korean prefix is 3B/char and the window is a
            # BYTE budget, so an overflowing trial silently loses the fact's leading bytes and
            # then reads as "the model did not consume it". Surface the tally INLINE — a run with
            # any DROPPED trial is INVALID-INSTRUMENT, not a negative result.
            cu = [r["consult"] for r in rows]
            summ["consult_used"] = sum(1 for c in cu if c == consult_fmt)
            summ["consult_downgraded"] = sum(1 for c in cu if c == "F2-downgrade")
            summ["consult_dropped"] = sum(1 for c in cu if c == "DROPPED-overflow")
            summ["consult_absent"] = sum(1 for c in cu if c is None)
            print("  byte-audit %s: used=%d downgraded=%d DROPPED=%d absent=%d" %
                  (split, summ["consult_used"], summ["consult_downgraded"],
                   summ["consult_dropped"], summ["consult_absent"]), flush=True)
        summ["breakdown"] = _xbind_breakdown(rows)
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (evaluate-py-1: never tail-truncatable)
        print("  xbind %s  arm=%s  D-acc=%.4f  C-rate=%s  margin_med=%.3f  "
              "margin_pos=%.3f  sampled=%s  n=%d" %
              (split, arm, summ["d_acc"], str(summ["c_rate"]), med,
               summ["margin_frac_pos"], str(summ["sampled_maj_acc"]), summ["n"]),
              flush=True)
        bd = summ["breakdown"]
        if "class" in bd:
            print("  by-class %s: %s   majority-baseline=%.3f%s" %
                  (split,
                   "  ".join("%s=%.3f(n=%d)" % (k, v["acc"], v["n"])
                             for k, v in bd["class"].items()),
                   bd["majority_baseline"],
                   ("   ⚠️ COLLAPSE — weakest class %.3f <= chance: the headline is riding the "
                    "label prior, NOT the stem" % bd["weakest_class_acc"])
                   if bd["collapse"] else ""), flush=True)
        for k, v in bd.get("flip", {}).items():
            cw = min(c["acc"] for c in v["class"].values()) if v["class"] else 1.0
            print("  by-flip %s  flip%s=%.4f(n=%d)  [%s]%s   (flip0 = is the fact in the "
                  "weights · flip1 = is the operator applied to it)" %
                  (split, k, v["acc"], v["n"],
                   "  ".join("%s=%.3f" % (c, s["acc"]) for c, s in v["class"].items()),
                   "  ⚠️ COLLAPSE" if cw <= 0.5 else ""), flush=True)
    json.dump(_json_safe(res), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"out": out_path,
                      "heldout_d_acc": res["splits"]["heldout"]["summary"]["d_acc"],
                      "seen_d_acc": res["splits"]["seen"]["summary"]["d_acc"]}))
    return 0


def _store_mix_breakdown(rows):
    """By-(pol,flip) split of the store-arm flip1, and paired baseline→store deltas.
    A binary DV is never read before it is split by class (polarity-split-before-headline).
    Returns {class:{<pol>:{flip1_store, flip1_base, n}}, n_hit, n_miss}."""
    from collections import defaultdict
    cls = defaultdict(lambda: {"s": 0, "b": 0, "n": 0})
    n_hit = n_miss = 0
    for r in rows:
        key = str(r.get("pol"))
        cls[key]["s"] += int(r["flip1_store"])
        cls[key]["b"] += int(r["flip1_base"])
        cls[key]["n"] += 1
        n_hit += int(r["store_hit"])
        n_miss += int(not r["store_hit"])
    out = {"class": {k: {"flip1_store": v["s"] / max(1, v["n"]),
                         "flip1_base": v["b"] / max(1, v["n"]), "n": v["n"]}
                     for k, v in cls.items()},
           "n_hit": n_hit, "n_miss": n_miss}
    return out


# ════════════════════════════════════════════════════════════════════════
# H_9693 (R1) `--fan-bind` — the bind-Δ instrument for the G6/ρ·fan wall
#
# The G6 wall's content is NOT "fals=0" — it is that the BIND signal lives OUTSIDE the
# measurement surface. convergence `g6-ideation-hexa-1` proved the frozen detector
# (_rho_fan_is_falsifiable) is FORM-only: targeted warm-FT passes FALS with topic-bind
# destroyed (TARGETED [6,6,6] == SHUF [6,6,6]) while the real signal sat in an unrecovered
# bind Δ (0.444 vs 0.000) measured by a non-frozen hexa-era probe. This instrument recovers
# that signal onto a legal, frozen, engine-native surface — without it, ANY angle that lifts
# fals is indistinguishable from forgery (kill #6 / MEASUREMENT_METALAW_FORM_TUNABLE_BIND_EARNED).
#
# Frozen materials ONLY (zero new tunables): rho_fan_build_frames(6)'s existing composed/
# shuffled/ablated 3-arm, the same _Mouth.ideate, gen (canonical 40 · evaluate-hexa-2), the
# detector's own content-word gate (len>=3 ∧ known ∧ ¬stop). The ONE addition is statistical
# POWER: the frozen panel emits n=6 per arm (no power); this samples n_smp per frame over a
# seed grid → 96/arm.
# ════════════════════════════════════════════════════════════════════════

def _fan_bind_content(s, known):
    """Content-word set of s under the FROZEN detector's own gate (_rho_fan_is_falsifiable's
    (c) clause: len>=3 ∧ in known ∧ not stopword). No new vocabulary, no new threshold."""
    stop = _rho_fan_stopwords()
    return set(w for w in _rho_fan_words(s) if len(w) >= 3 and w in known and w not in stop)


def _fan_bind_J(o, cA, cB, known):
    """J(o) = 1 iff the emission carries >=1 cA content-word AND >=1 cB-UNIQUE content-word.

    p7-clean: a set-membership predicate over the frozen content gate — no perplexity, no
    likelihood, no LLM judge. Returns None for a degenerate pair (either side has no unique
    content word), so degenerate frames are dropped rather than silently scored 0."""
    a = _fan_bind_content(cA, known)
    b = _fan_bind_content(cB, known) - a          # cB-UNIQUE: shared words cannot testify
    if not a or not b:
        return None
    wo = set(_rho_fan_words(o))
    return 1 if (wo & a) and (wo & b) else 0


def _fan_bind_pairs(n_strong):
    """The (cA, cB) pair behind each composed/shuffled frame — index math MIRRORS
    rho_fan_build_frames EXACTLY (a = i%n · b = (i+1+i//n)%n · sh = derangement(a,n)).
    If that builder ever changes, this must move in lockstep or the DV scores the wrong pair."""
    cz = _rho_fan_concepts()
    n = len(cz)
    comp = []
    shuf = []
    for i in range(n_strong):
        a = i % n
        b = (i + 1 + i // n) % n
        comp.append((cz[a], cz[b]))
        shuf.append((cz[a], cz[_rho_fan_derangement(a, n)]))
    return comp, shuf


def fan_bind_calibration(known):
    """Scorer certification — frozen 6-string set the DV must classify BEFORE the model is
    read (positive-control-before-reading-a-negative). pos = both concepts' content present ·
    neg = one-side echo only / unrelated. A failing scorer INVALIDATES the instrument."""
    cz = _rho_fan_concepts()
    cA, cB = cz[0], cz[1]                          # "consciousness arises from cells" / "tension ripples between distant minds"
    checks = []
    checks.append(("pos both-sides", _fan_bind_J(
        "consciousness in cells and the tension between distant minds both rise", cA, cB, known) == 1))
    checks.append(("pos both-sides-2", _fan_bind_J(
        "cells show consciousness while minds carry tension across distance", cA, cB, known) == 1))
    checks.append(("neg cA-echo-only", _fan_bind_J(
        "consciousness arises from cells and cells alone, always", cA, cB, known) == 0))
    checks.append(("neg cB-echo-only", _fan_bind_J(
        "tension ripples between distant minds forever", cA, cB, known) == 0))
    checks.append(("neg unrelated", _fan_bind_J(
        "the weather today is warm and pleasant", cA, cB, known) == 0))
    checks.append(("neg empty", _fan_bind_J("", cA, cB, known) == 0))
    return {"checks": checks, "pass": all(ok for _, ok in checks)}


def _mcnemar_p_1sided(b, c):
    """One-sided exact McNemar = paired sign test on discordant counts (b comp-hit/shuf-miss,
    c comp-miss/shuf-hit). H0: composed and shuffled pairings are exchangeable ⇒ each discordant
    pair is +1 or -1 with p=0.5 ⇒ b ~ Binom(m, 0.5), m=b+c. Returns P(Binom(m,0.5) >= b) for the
    Δ>0 (composition-helps) direction. Closed-form, deterministic (no RNG · p7/frozen). m<5 ⇒ even
    an all-one-way split cannot clear 0.05 (0.5^m > 0.05), so the test is powerless there BY DESIGN
    — the caller reports that as UNDECIDABLE rather than a KILL (power-before-negative-verdict)."""
    import math
    m = b + c
    if m == 0:
        return 1.0
    return sum(math.comb(m, k) for k in range(b, m + 1)) * (0.5 ** m)


def _tango_ci90(b, c, N):
    """Tango(1998) score-based two-sided 90% CI for the paired proportion difference
    Δ=(b-c)/N (α=0.05 two one-sided ⇒ 100(1-2α)=90%). Score CI is the paired-binomial standard;
    stable at the boundary and for small discordant m where a Wald interval is unfit. TOST: the CI
    ⊂ (-δ,+δ) ⇒ equivalence (|Δ|<δ established), which is how "0.444 is an artifact" is EARNED
    (negative-claims-need-tost-not-ns). Solves the Tango score equation by bisection on δ̂."""
    if N == 0:
        return (-1.0, 1.0)
    import math
    z = 1.6448536269514722            # z_{0.95}
    est = (b - c) / N
    def score_bounds(target_sign):
        # Tango score: find δ where (Δ̂-δ)^2 = z^2 * Var_δ, Var_δ = [ (2N·δ + ... ) ] via the
        # constrained MLE. Use the standard Tango closed pieces through a numeric root on δ.
        lo, hi = -1.0, 1.0
        for _ in range(200):
            d = (lo + hi) / 2.0
            # constrained MLE of q=P(shuf-hit,comp-miss) given Δ=d (Tango 1998 eq.)
            A = 2.0 * N
            Bq = -(b + c) + (2.0 * N - (b - c)) * d
            Cq = -c * d * (1.0 - d)
            disc = Bq * Bq - 4.0 * A * Cq
            disc = disc if disc > 0 else 0.0
            q = (-Bq + math.sqrt(disc)) / (2.0 * A) if A != 0 else 0.0
            q = min(max(q, 0.0), 1.0)
            var = max((2.0 * q + d - d * d) / N, 1e-12)
            stat = (est - d) / math.sqrt(var)
            # for lower bound target_sign=+1 (stat=+z), upper target_sign=-1 (stat=-z)
            if (stat - target_sign * z) > 0:
                lo = d
            else:
                hi = d
        return (lo + hi) / 2.0
    lo = score_bounds(+1.0)
    hi = score_bounds(-1.0)
    if lo > hi:
        lo, hi = hi, lo
    return (lo, hi)


def _fan_bind_paired(comp_rows, shuf_rows, comp_pairs, shuf_pairs, ablated_J, known,
                     delta_equiv=0.05, emit_floor=0.005):
    """H_9745 — the composition-isolating paired verdict on bind_delta, replacing the marginal
    composed-J null (which measures EMISSION: a pair-deranged arm can carry the higher composed J).

    Matches composed(i,j)⇄shuffled(i,j) by frame+decode-seed (same 7+17j+i, same cA_i, differ only
    in cB) into a 2x2 discordant table (b=comp-hit/shuf-miss, c=comp-miss/shuf-hit). bind_delta=(b-c)/N.
    Verdict is exact one-sided McNemar on (b,c) — never emission. TOST (Tango 90% CI ⊂ ±δ) earns the
    'artifact' call. Emission pre-gate + m<5 ⇒ UNDECIDABLE (instrument-claim-alignment + power-first).

    Controls surfaced (not folded into the verdict): ablated_J (zero-truth pedestal — must be ~0 or
    the detector fires on chance co-occurrence) · cA_echo per arm (must match across arms; a mismatch
    means the cA covariate is not controlled and the verdict is confounded)."""
    comp = {(i, j): o for (i, j, o) in comp_rows}
    shuf = {(i, j): o for (i, j, o) in shuf_rows}
    keys = sorted(set(comp) & set(shuf))     # non-degenerate frame∩ · matched (i,j)
    b = c = a11 = d = 0
    ca_comp_hit = ca_shuf_hit = 0
    for (i, j) in keys:
        Jc = _fan_bind_J(comp[(i, j)], comp_pairs[i][0], comp_pairs[i][1], known)
        Js = _fan_bind_J(shuf[(i, j)], shuf_pairs[i][0], shuf_pairs[i][1], known)
        if Jc is None or Js is None:
            continue
        if Jc and Js: a11 += 1
        elif Jc and not Js: b += 1
        elif not Jc and Js: c += 1
        else: d += 1
        # cA-only echo covariate (cA_i shared by both arms → echo rate must match; else confounded).
        # membership of any cA content-word in the emission (the first clause of _fan_bind_J alone).
        ca_words = _fan_bind_content(comp_pairs[i][0], known)
        if ca_words:
            if set(_rho_fan_words(comp[(i, j)])) & ca_words: ca_comp_hit += 1
            if set(_rho_fan_words(shuf[(i, j)])) & ca_words: ca_shuf_hit += 1
    N = a11 + b + c + d
    m = b + c
    bd = ((b - c) / N) if N else 0.0
    emit_rate = ((a11 + b) + (a11 + c)) / (2.0 * N) if N else 0.0     # (comp_hit+shuf_hit)/2N
    p1 = _mcnemar_p_1sided(b, c)
    ci = _tango_ci90(b, c, N)
    tost = bool(ci[0] > -delta_equiv and ci[1] < delta_equiv)
    powered = (m >= 5)
    under_emit = (emit_rate < emit_floor)
    if under_emit or not powered:
        verdict = "UNDECIDABLE"
    elif bd > 0.0 and p1 <= 0.05:
        verdict = "BIND-SENSITIVE"
    elif tost:
        verdict = "BIND-ABSENT"     # equivalence to 0 within δ = the '0.444 artifact' call
    else:
        verdict = "UNDECIDABLE"
    return {"N": N, "b": b, "c": c, "m": m, "a11": a11, "d": d,
            "bind_delta_paired": bd, "mcnemar_p_1sided": p1,
            "tango_ci90": [ci[0], ci[1]], "tost_equiv": tost, "delta_equiv": delta_equiv,
            "emit_rate": emit_rate, "emit_floor": emit_floor, "powered": powered,
            "ablated_J": ablated_J, "cA_echo_comp": ca_comp_hit, "cA_echo_shuf": ca_shuf_hit,
            "verdict": verdict}


def eval_fan_bind(mouth, gen, known, n_smp=16, dump=None):
    """bind Δ = mean J(composed) − mean J(shuffled) over the frozen 3-arm frames.

    Both arms carry THEIR OWN cB in the prompt, so pure echo is symmetric and cancels to
    Δ=0 by construction — Δ>0 therefore means the mouth integrates cB MORE when the pairing
    is the composed one than when it is deranged = composition sensitivity, not echo.
    ablated ("cA: " · no cB in prompt) is the floor arm.

    Null: mismatched-pairing — each emission is ALSO scored against every OTHER frame's
    (cA_j, cB_j), giving the chance joint-coverage distribution the bar is derived from
    (chance-level-must-be-derived-per-metric). The bar is NOT a fixed number."""
    fr = rho_fan_build_frames(6)
    comp_pairs, shuf_pairs = _fan_bind_pairs(6)
    arms = {"composed": (fr["composed"], comp_pairs),
            "shuffled": (fr["shuffled"], shuf_pairs),
            "ablated": (fr["ablated"], comp_pairs)}   # ablated prompt lacks cB → floor
    out = {}
    emits = {}
    for name, (frames, pairs) in arms.items():
        hits = 0
        n = 0
        rows = []
        for i in range(len(frames)):
            cA, cB = pairs[i]
            for j in range(n_smp):
                o = mouth.ideate(frames[i], gen, 40, 0.7, 7 + 17 * j + i)   # frozen decode knobs
                if dump is not None:                 # H_9746 --fan-dump: emission census (판정 불변)
                    dump.append({"arm": name, "frame_i": i, "smp_j": j, "seed": 7 + 17 * j + i,
                                 "cA": cA, "cB": cB, "emission": o,
                                 "J": _fan_bind_J(o, cA, cB, known)})
                J = _fan_bind_J(o, cA, cB, known)
                if J is None:
                    continue
                rows.append((i, j, o))               # H_9745: track j so composed(i,j)⇄shuffled(i,j) pair
                hits += J
                n += 1
        out[name] = {"J_mean": (hits / n) if n else 0.0, "n": n}
        emits[name] = rows
    # ── mismatched-pairing null (composed emissions scored against OTHER frames' pairs) ──
    null_vals = []
    for i, _j, o in emits["composed"]:
        for k in range(len(comp_pairs)):
            if k == i:
                continue
            J = _fan_bind_J(o, comp_pairs[k][0], comp_pairs[k][1], known)
            if J is not None:
                null_vals.append(J)
    null_mean = (sum(null_vals) / len(null_vals)) if null_vals else 0.0
    # bootstrap the null's 95th percentile on the SAME n as the composed arm (frozen-first)
    nc = out["composed"]["n"] or 1
    p95 = 0.0
    if null_vals:
        import random as _r
        rng = _r.Random(9693)
        boots = []
        for _ in range(2000):
            s = sum(null_vals[rng.randrange(len(null_vals))] for _ in range(nc)) / nc
            boots.append(s)
        boots.sort()
        p95 = boots[int(0.95 * (len(boots) - 1))]
    delta = out["composed"]["J_mean"] - out["shuffled"]["J_mean"]
    # ── H_9745: paired McNemar + TOST on bind_delta (the composition-isolating statistic) ──
    # The marginal null above (composed J vs mismatched pairs) tests EMISSION, not composition —
    # a pair-deranged (shuffled) arm can carry the HIGHER composed J yet zero bind. bind_delta is
    # a PAIRED difference (composed(i,j) and shuffled(i,j) share seed 7+17j+i · frame i · cA_i,
    # differ only in cB), so it earns its OWN pedestal here: exact one-sided McNemar on the
    # discordant counts (chance-level-must-be-derived-per-metric), never the marginal null.
    paired = _fan_bind_paired(emits["composed"], emits["shuffled"], comp_pairs, shuf_pairs,
                              out["ablated"]["J_mean"], known)
    return {"bind_delta": delta, "composed": out["composed"], "shuffled": out["shuffled"],
            "ablated": out["ablated"], "null_mean": null_mean, "null_p95": p95,
            "pass": bool(delta > 0.0 and out["composed"]["J_mean"] > p95),
            "paired": paired, "n_smp": n_smp, "gen": gen}


def fan_bind_run(argv):
    """`anima-py evaluate <ckpt> --fan-bind [--fan-smp N]` — H_9693 (R1) bind-Δ instrument.

    Reports bind Δ + the mismatched-pairing null bar. This is an INSTRUMENT, not a G6 verdict:
    a PASS here says the emission is composition-sensitive on the frozen frames, NOT that the
    ρ·fan gate (fals) moved. Every downstream angle (H_9694/H_9696/H_9697/H_9698/H_9700) reads
    ITS lever through this surface — bind Δ vs its own SHUF arm — because fals alone is
    FORM-forgeable (kill #6)."""
    ckpt = argv[0]
    gen = evaluate_intval(argv[1:], "--gen", 0)
    g = gen if gen > 0 else _default_gen()
    n_smp = evaluate_intval(argv[1:], "--fan-smp", 16)
    known = _rho_fan_dict_load()
    print("=== anima evaluate --fan-bind — H_9693 (R1) G6/ρ·fan bind-Δ instrument ===")
    print("ckpt: %s  gen=%d (canonical=%d)  n_smp=%d  frames=6(frozen composed/shuffled/ablated)"
          % (ckpt, g, _default_gen(), n_smp))
    # ── scorer certification FIRST (instrument dead ⇒ never read the model) ──
    cal = fan_bind_calibration(known)
    for name, ok in cal["checks"]:
        print("  [cal] %-18s %s" % (name, "✅" if ok else "❌"))
    if not cal["pass"]:
        print("  ⛔ SCORER CERTIFICATION FAILED — instrument INVALID, model NOT read "
              "(positive-control-before-reading-a-negative).")
        return 1
    print("  [cal] scorer certified ✅ — reading the model now.")
    # ── H_9698 MBND mouth-binder lane switch (R6). Default OFF ⇒ a binder-carrying .clm reproduces
    # its pre-binder numbers byte-identically, so this surface stays the SAME instrument for every
    # lever that reads through it. --mouth-binder-order-scramble is R6's control: it deranges the
    # causal bank, which only bites because the address carries a relative-distance bias (plain
    # content attention is permutation-equivariant over the bank, so the control would read Δ=0.000
    # BY CONSTRUCTION — a control that cannot fail is not a control).
    mb_on = "--mouth-binder" in argv[1:]
    mb_scr = "--mouth-binder-order-scramble" in argv[1:]
    from decode import set_mouth_binder
    if mb_on or mb_scr:
        set_mouth_binder(on=True, order_scramble=mb_scr)
        print("  [lane] MBND mouth-binder ON%s (trailer must be present; absent ⇒ no-op)"
              % ("  · ORDER-SCRAMBLE control" if mb_scr else ""))
    else:
        set_mouth_binder(on=False)
    mouth = _Mouth(ckpt)
    _dump_path = evaluate_strval(argv[1:], "--fan-dump", "") if "--fan-dump" in argv[1:] else ""
    _dump = [] if _dump_path else None
    r = eval_fan_bind(mouth, g, known, n_smp, dump=_dump)
    if _dump_path:
        import json as _json
        with open(_dump_path, "w", encoding="utf-8") as _fh:
            for _row in _dump:
                _fh.write(_json.dumps(_row, ensure_ascii=False) + "\n")
        print("  [--fan-dump] %d emissions -> %s (H_9746 census · 판정 불변)" % (len(_dump), _dump_path))
    print("  composed: J=%.4f (n=%d) · shuffled: J=%.4f (n=%d) · ablated(floor): J=%.4f (n=%d)"
          % (r["composed"]["J_mean"], r["composed"]["n"], r["shuffled"]["J_mean"],
             r["shuffled"]["n"], r["ablated"]["J_mean"], r["ablated"]["n"]))
    print("  ★ bind_delta = %.4f  [composed − shuffled]  ·  mismatched-null mean=%.4f p95=%.4f"
          % (r["bind_delta"], r["null_mean"], r["null_p95"]))
    print("  verdict: %s  (PASS ⟺ Δ>0 ∧ composed J > mismatched-null p95)"
          % ("🟢 BIND-SENSITIVE" if r["pass"] else "🧱 NO-BIND (Δ≤0 or within null)"))
    print("  → INSTRUMENT ONLY — not a ρ·fan(fals) verdict. Δ<0 = anti-bind (pre-registered "
          "cell). A lever's claim = ITS bind Δ vs ITS OWN SHUF arm; fals alone is FORM-forgeable.")
    # ── H_9745: the PAIRED verdict — bind_delta's own pedestal (exact McNemar + TOST), the
    # composition-isolating statistic. The line above (composed J > marginal null) tests EMISSION;
    # THIS tests composition. Read THIS for a lever's bind claim. ──
    pd = r.get("paired") or {}
    print("  ── H_9745 PAIRED (bind_delta's own null · composition ≠ emission) ──")
    print("     discordant b=%d(comp-hit/shuf-miss) c=%d(comp-miss/shuf-hit) m=%d · N=%d · "
          "bind_delta=%+.4f" % (pd.get("b",0), pd.get("c",0), pd.get("m",0), pd.get("N",0),
                                pd.get("bind_delta_paired",0.0)))
    print("     exact McNemar p(1-sided)=%.4f · Tango90 CI=[%+.4f,%+.4f] · TOST(⊂±%.2f)=%s · "
          "powered(m≥5)=%s" % (pd.get("mcnemar_p_1sided",1.0), pd.get("tango_ci90",[0,0])[0],
          pd.get("tango_ci90",[0,0])[1], pd.get("delta_equiv",0.05), pd.get("tost_equiv",False),
          pd.get("powered",False)))
    print("     controls: ablated_J=%.4f (zero-truth pedestal · ~0 정상) · cA-echo comp=%d shuf=%d "
          "(arm 간 매칭 필수·불일치=교란) · emit_rate=%.4f" % (pd.get("ablated_J",0.0),
          pd.get("cA_echo_comp",0), pd.get("cA_echo_shuf",0), pd.get("emit_rate",0.0)))
    _pv = pd.get("verdict","UNDECIDABLE")
    _icon = {"BIND-SENSITIVE":"🟢","BIND-ABSENT":"🧱","UNDECIDABLE":"⛔"}.get(_pv,"⛔")
    print("     ★ PAIRED verdict: %s %s  (🟢 bd>0∧McNemar p≤.05 · 🧱 TOST 등가=artifact · "
          "⛔ m<5 or emit<floor = 검정력부족·NOT a kill)" % (_icon, _pv))
    if _pv == "UNDECIDABLE" and pd.get("m",0) < 5:
        print("     ⛔ m=%d < 5 ⟹ exact McNemar 로 어떤 데이터도 유의 불가 = fan-smp 상향 필요"
              "(δ=0.05 사전등록엔 N≥288 = fan-smp≈48 · power-before-negative-verdict)." % pd.get("m",0))
    # ── DUAL-GATE (H_9698 follow-on · lab-identified instrument gap) — a bind is CONFIRMED
    # only when BOTH signals agree: PAIRED-SENSITIVE (McNemar composition test above) AND
    # EMISSION-CLEARED (composed J clears the emission-null p95). The R6 control-reversal —
    # a pair-DERANGED (shuffled) arm scoring a McNemar-🟢 while sitting INSIDE the emission
    # null band — is exactly the false positive this conjunction rejects: paired-🟢 read
    # WITHOUT the emission gate over-calls sub-null sign noise as bind. ADDITIVE: the two
    # verdicts above are unchanged; this only reports their AND (no retroactive reverdict ·
    # a lever that USES this gate pre-registers it in its own card · lab reconcile H_9698).
    emission_cleared = r["composed"]["J_mean"] > r["null_p95"]
    paired_sensitive = (_pv == "BIND-SENSITIVE")
    if _pv == "UNDECIDABLE":
        _dg = ("⛔ UNDECIDABLE", "검정력부족 — AND-gate 판정불가 (fan-smp 상향 필요)")
    elif paired_sensitive and emission_cleared:
        _dg = ("🟢 BIND-CONFIRMED", "PAIRED-SENSITIVE ∧ EMISSION-CLEARED 둘 다 통과")
    elif paired_sensitive and not emission_cleared:
        _dg = ("🟡 EMISSION-CONFOUND", "McNemar-🟢 이나 composed J 가 emission-null 안 "
               "= sub-null 부호노이즈 의심 (R6 통제역전 계급) · bind 아님")
    else:   # BIND-ABSENT (TOST equivalence)
        _dg = ("🧱 BIND-ABSENT", "TOST 등가 — 레버가 composition 안 심음")
    print("  ══ DUAL-GATE (H_9698 · PAIRED-SENSITIVE ∧ EMISSION-CLEARED) ══")
    print("     paired=%s(McNemar) · emission_cleared=%s (composed J %.4f %s null p95 %.4f)"
          % ("🟢" if paired_sensitive else ("⛔" if _pv == "UNDECIDABLE" else "🧱"),
             emission_cleared, r["composed"]["J_mean"],
             ">" if emission_cleared else "≤", r["null_p95"]))
    print("     ★ AND-gate: %s — %s" % (_dg[0], _dg[1]))
    return 0


def store_run(argv):
    """`anima-py evaluate <ckpt> --store <held.json> [--store-oracle] [--store-lambda λ]` — H_9423
    CLMS store-bridge lane eval (the CO-TRAINED bridge, NOT the H_9392 --store-mix bolt-on actuator:
    the boundary is "does the fusion parameter live inside the .clm and enter the forward pass"). Each
    held-out item injects its 8-slot store at the query; the CLMS lane forms a content-addressed lookup
    and OVERWRITES the answer-position logits with λ·store_logits (store_only). Binary readout = the
    first answer byte ('g'=good vs 'b'=bad · v2 axis). --store-oracle forces the true slot (C0-e positive
    control: ORACLE<0.90 = value/MLP/λ/serialization plumbing dead — read NO negative before it passes,
    v2 reversed 3 instrument deaths on exactly this). Engine-native core/decode.py (a_eval_py_canonical →
    TERMINAL-eligible). This flag MEASURES; the SEQUENTIAL C0→C1→C2→P1 battery + verdict fire on pool
    (a_toy_scale_recheck · 303M needs owner go). Controls are eval-time store edits: derange
    store.entities = key-shuffle · flip store.pols = wrong-store · --store-lambda 0 = λ0 byte-identical."""
    import numpy as np
    ckpt = argv[0]
    man_path = evaluate_strval(argv[1:], "--store", "")
    oracle = "--store-oracle" in argv
    lam_s = evaluate_strval(argv[1:], "--store-lambda", "")
    lam_override = float(lam_s) if lam_s else None
    if lam_override is not None and not (0.0 <= lam_override <= 1.0):
        print("ERROR: --store-lambda must be in [0,1], got %r" % lam_override)
        return 1
    # H_9423 C2 controls (eval-time store edits · core/clms.py UNCHANGED so the ORACLE cert holds):
    #   --store-shuffle = derange store.entities (Sattolo, entities-only → key↔value binding broken,
    #                     h/λ/K-multiset intact) → PASS if lookup collapses (uses the address).
    #   --store-flip    = flip all store.pols (v-channel pure) → 2-pass flip-coherence (store value is
    #                     causally consumed). Constant-predictor coherence ≡ 0 by construction.
    #   --store-neutral = MISS control (P2, no bar, characterisation only).
    #   These are MUTUALLY EXCLUSIVE. --store-ctrl-seed pins the derangement RNG.
    # H_9695 (R3) — surface core's query/fuse. core/clms.py store_apply + core/decode.py
    # set_clms_store have carried these since H_9695 landed, but NO CLI passed them, so the
    # marker-free read→mouth lane was unreachable from the only legal surface (a_experiment_
    # engine_native: a manipulation is a flag on anima-py, not a probe). Defaults reproduce the
    # H_9423 lane byte-for-byte.
    store_query = evaluate_strval(argv[1:], "--store-query", "qpos")
    if store_query not in ("qpos", "every-token"):
        print("ERROR: --store-query must be 'qpos' (default) or 'every-token', got %r" % store_query)
        return 1
    store_fuse = evaluate_strval(argv[1:], "--store-fuse", "overwrite")
    if store_fuse not in ("overwrite", "gated-add", "odd", "pairodd"):
        print("ERROR: --store-fuse must be 'overwrite' (default), 'gated-add', 'odd' or 'pairodd', got %r" % store_fuse)
        return 1
    # H_9775: --store-readout {2way,vocab}. 2way (legacy) = argmax over {g,b} only. vocab = 256-vocab
    # argmax, answer readable ONLY iff ŷ∈{'g','b'} else 'unreadable' — the SAME rule the in-vivo daemon
    # mouth uses (full-vocab greedy). #4103: odd passed the 2-way gate (main 1.0) yet emitted garbage
    # in-vivo; the vocab readout catches that at eval time (predicts in-vivo). Default 2way = byte-identical.
    store_readout = evaluate_strval(argv[1:], "--store-readout", "2way")
    if store_readout not in ("2way", "vocab"):
        print("ERROR: --store-readout must be '2way' (default) or 'vocab', got %r" % store_readout)
        return 1
    if store_query == "every-token" and store_fuse in ("overwrite", "odd", "pairodd"):
        # clms.py store_apply: overwriting EVERY row deletes the trunk and destroys fluency — the
        # readout would score the lane alone with no mouth left (odd/pairodd are overwrite-style too). Refuse
        # loudly (an INVALID arm is worse than no arm) rather than emit a number nobody may read.
        print("ERROR: --store-query every-token with --store-fuse overwrite/odd/pairodd overwrites every row,")
        print("       deleting the trunk (fluency dead · the readout stops being attributable).")
        print("       Use --store-fuse gated-add for the marker-free lane (H_9695).")
        return 1
    ctrl = [f for f in ("--store-shuffle", "--store-flip", "--store-neutral") if f in argv]
    if len(ctrl) > 1:
        print("ERROR: --store-shuffle / --store-flip / --store-neutral are mutually exclusive (got %s)" % ctrl)
        return 1
    mode = ctrl[0][8:] if ctrl else ""               # "shuffle" | "flip" | "neutral" | ""
    ctrl_seed = evaluate_intval(argv[1:], "--store-ctrl-seed", 9423)
    if not man_path:
        print("ERROR: --store needs a held-out manifest (--store <held.json>).")
        return 1
    man = json.load(open(man_path))
    entries = man.get("entries", man.get("held_out", []))
    if isinstance(entries, dict):
        entries = list(entries.values())
    T = evaluate_intval(argv[1:], "--win", 24)
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    # H_9724 · --store-component-swap {val,readout,wq,trunk,...} --store-swap-from <other.clm>
    # EVALUATION-ONLY causal surgery (Sol EA-6). H_9672's T3 is address-robust across seeds
    # (addr_mass .95/.96) yet the VALUE read is seed-fragile (ORACLE seed-7 0.99 vs seed-11 0.50).
    # If transplanting `val`/readout carries the success across seeds INDEPENDENTLY of a robust W_q,
    # the missing bootstrap seed is value organisation, not address capacity.
    #   admissibility (Sol, enforced by construction): this supplies NO training signal and installs
    #   NO address — it only re-reads existing weights. target_slot is never consulted here.
    # Components map to the CLMS trailer dict (core/clms.py read_clms): W_q · val · W_h/b_h/W_out
    # (= "readout" MLP) · lam. "trunk" swaps the non-CLMS forward weights instead.
    swap_spec = evaluate_strval(argv[1:], "--store-component-swap", "")
    swap_from = evaluate_strval(argv[1:], "--store-swap-from", "")
    if swap_spec:
        if not swap_from:
            print("ERROR: --store-component-swap needs --store-swap-from <other.clm>", file=sys.stderr)
            return 2
        _GROUPS = {"wq": ["W_q"], "val": ["val"], "readout": ["W_h", "b_h", "W_out"],
                   "lam": ["lam"], "bridge": ["W_q", "val", "W_h", "b_h", "W_out", "lam"]}
        want = [s.strip() for s in swap_spec.split(",") if s.strip()]
        bad = [s for s in want if s not in _GROUPS and s != "trunk"]
        if bad:
            print("ERROR: unknown component(s) %s — known: %s,trunk"
                  % (",".join(bad), ",".join(sorted(_GROUPS))), file=sys.stderr)
            return 2
        Wd = clm.clm_load_weights(swap_from)
        if not Wd.get("ok"):
            print("ERROR: donor ckpt not decodable: " + swap_from, file=sys.stderr)
            return 2
        if W.get("clms") is None or Wd.get("clms") is None:
            print("ERROR: both ckpts need a CLMS trailer to swap bridge components "
                  "(host=%s donor=%s)" % (W.get("clms") is not None, Wd.get("clms") is not None),
                  file=sys.stderr)
            return 2
        # shape gate — a silently mis-shaped graft is an off-manifold chimera, not a measurement
        moved = []
        for grp in want:
            if grp == "trunk":
                for k in ("ecWt", "ecB", "tcWt", "tcB", "tgG", "tgB", "eWt", "eB",
                          "rWt", "rB", "noG", "noB", "embed", "roWt", "roB"):
                    ha, hb = k in W, k in Wd
                    if not ha and not hb:
                        continue                          # absent from BOTH = not part of this arch
                    if ha != hb:                          # present on ONE side = asymmetric ckpts
                        print("ERROR: trunk key '%s' asymmetric (host=%s donor=%s) — refusing to graft"
                              % (k, ha, hb), file=sys.stderr)
                        return 2
                    sa = getattr(W[k], "shape", None); sb = getattr(Wd[k], "shape", None)
                    if sa != sb:
                        print("ERROR: shape mismatch on trunk '%s': host %s vs donor %s — refusing to "
                              "graft (an off-manifold chimera is not a measurement)" % (k, sa, sb),
                              file=sys.stderr)
                        return 2
                    W[k] = Wd[k]
                    moved.append("trunk:" + k)
                continue
            for k in _GROUPS[grp]:
                a, b = W["clms"].get(k), Wd["clms"].get(k)
                if a is None or b is None:
                    print("ERROR: component '%s' absent (host=%s donor=%s)"
                          % (k, a is not None, b is not None), file=sys.stderr)
                    return 2
                sa = getattr(a, "shape", None); sb = getattr(b, "shape", None)
                if sa != sb:
                    print("ERROR: shape mismatch on '%s': host %s vs donor %s — refusing to graft "
                          "(an off-manifold chimera is not a measurement)" % (k, sa, sb), file=sys.stderr)
                    return 2
                W["clms"][k] = b
                moved.append(k)
        if not moved:                                     # nothing grafted = a no-op read as a measurement
            print("ERROR: component-swap moved 0 tensors (spec=%s) — a no-op is not a measurement"
                  % swap_spec, file=sys.stderr)
            return 2
        same = os.path.realpath(ckpt) == os.path.realpath(swap_from)
        print("  [component-swap] %s ← %s · moved: %s%s"
              % (swap_spec, os.path.basename(swap_from), ",".join(moved),
                 "  ⚠️ SHAM (donor == host · positive-validity control)" if same else ""),
              flush=True)

    import clms as _clms
    g_id, b_id = ord("g"), ord("b")                  # byte value = logits index (see _store_mix_cont_nll)

    def _sattolo(nn, rng):                            # uniform nn-cycle: EVERY element moves (0 fixed points)
        p = list(range(nn))
        for i in range(nn - 1, 0, -1):
            j = int(rng.integers(0, i))               # j < i STRICTLY — the Sattolo/Fisher-Yates difference
            p[i], p[j] = p[j], p[i]
        return p

    def _predict(store, audit=None):
        """Inject store, forward the prompt window, read the 2-way g/b readout at qpos. None if malformed.
        audit (H_9672 --store-addr-audit) = a list store_apply appends {argmax,a_target,target} to per qpos."""
        clm.set_clms_store(store=store, oracle=oracle, lam_override=lam_override, audit=audit,
                           query=store_query, fuse=store_fuse)
        logits = np.asarray(clm._fwd_logits(W, tok, T))
        qp = _clms.find_qpos(tok)
        if not qp:
            return None
        row = logits[qp[-1]]
        if store_readout == "vocab":                  # H_9775: full-vocab argmax = the in-vivo daemon mouth rule
            yhat = int(np.argmax(row))                 # (256-vocab greedy). readable ONLY iff ŷ∈{'g','b'};
            if yhat == g_id:                           # else 'unreadable' — the daemon would emit a non-answer
                return "good"                          # byte. #4103: full-row odd passed 2-way (main 1.0) yet
            if yhat == b_id:                           # emitted garbage in-vivo — vocab catches it at eval time.
                return "bad"
            return "unreadable"
        return "good" if float(row[g_id]) >= float(row[b_id]) else "bad"

    addr_audit = "--store-addr-audit" in argv          # H_9672: report addr_top1 (argmax==target) + addr_mass
    # H_9802 pre-check ($0, MONITOR-ONLY): target-free address telemetry. Splits
    # "natural text never addresses the store" (recruitment) from "addresses it but the
    # values are garbage" (alignment) BEFORE any training spend is committed.
    store_telemetry = "--store-telemetry" in argv
    tel_n = 0; tel_amax = 0.0; tel_aent = 0.0
    addr_top1 = addr_mass = addr_n = 0                  # (mean a[target]) — soft-address diagnostic

    print("=== anima evaluate --store — H_9423 CLMS store-bridge lane (co-trained) ===")
    arm = mode or ("oracle" if oracle else ("lambda0" if lam_override == 0.0 else "lookup"))
    print("ckpt: %s  manifest: %s (%d items)  arm=%s  oracle=%s  λ=%s  win=%d  ctrl_seed=%d"
          % (ckpt, man_path, len(entries), arm, oracle,
             ("%.3f" % lam_override) if lam_override is not None else "(file)", T, ctrl_seed))
    if W.get("clms") is None:
        print("  ⚠️ this ckpt carries NO CLMS trailer — the lane is ABSENT (base trunk). FLOOR by construction.")
    n = correct = 0
    by = {}                                          # (op, pol) -> [correct, total]  (polarity-split · card)
    fixed_points_total = dup_entities = 0
    pol_hist = {}                                     # #good-slots per store -> count (balance witness · §E)
    coh_all = coh_bc = coh_bc_n = flip_correct = 0    # flip-coherence accumulators
    readable_n = 0                                     # H_9775 vocab: #answers whose full-vocab argmax ∈ {g,b}
    op_name = {0: "is ", 1: "not"}
    pol_name = {0: "good", 1: "bad "}
    for idx, it in enumerate(entries):
        prompt, gold = it["prompt"], it["gold"]
        st = it["store"]
        ents = list(st["entities"])
        pols = list(st["pols"])
        tslot = it.get("target_slot")
        n_slot = len(ents)
        if len(set(ents)) != n_slot:
            dup_entities += 1                         # loud, never silent — derangement fixed-point-leak risk
        pol_hist[sum(1 for p in pols if p == 0)] = pol_hist.get(sum(1 for p in pols if p == 0), 0) + 1
        tok = clm._seed_to_tok(prompt, T)
        if mode == "shuffle":
            rng = np.random.default_rng(ctrl_seed * 100003 + idx)
            perm = _sattolo(n_slot, rng)
            ents2 = [ents[perm[i]] for i in range(n_slot)]   # entities-only derange · pols/target_slot fixed
            fixed_points_total += sum(1 for i in range(n_slot) if ents2[i] == ents[i])
            store = {"entities": ents2, "pols": pols, "target_slot": tslot}
        elif mode == "flip":
            store = {"entities": ents, "pols": [1 - p for p in pols], "target_slot": tslot}
        elif mode == "neutral":
            rng = np.random.default_rng(ctrl_seed * 100003 + idx + 7)
            # length-matched nonce filler (control-must-match-mediating-covariate): CVCVC not in this entry
            cons, vow = "bdfgklmnprstvz", "aeiou"
            def _nonce():
                return (cons[int(rng.integers(0, 14))] + vow[int(rng.integers(0, 5))]
                        + cons[int(rng.integers(0, 14))] + vow[int(rng.integers(0, 5))]
                        + cons[int(rng.integers(0, 14))])
            store = {"entities": [_nonce() for _ in range(n_slot)], "pols": pols, "target_slot": tslot}
        else:
            store = {"entities": ents, "pols": pols, "target_slot": tslot}
        if mode == "flip":
            base = _predict({"entities": ents, "pols": pols, "target_slot": tslot})
            flip = _predict(store)
            if base is None or flip is None:
                continue
            gold_flip = "bad" if gold == "good" else "good"
            n += 1
            base_ok = base in ("good", "bad")         # H_9775 vocab: 'unreadable' (argmax∉{g,b}) excluded from
            flip_ok = flip in ("good", "bad")         #   coherence — the daemon would emit a non-answer there.
            readable_n += int(base_ok)                # readability witness (base = the un-flipped answer)
            if base_ok and flip_ok:                   # coherence ONLY over readable pairs (in-vivo rule)
                coh_all += int(flip != base)
                if base == gold:                      # coherence_bc: conditioned on baseline-correct (§B-2)
                    coh_bc_n += 1
                    coh_bc += int(flip != base)
            flip_correct += int(flip == gold_flip)
            key = (it.get("op"), 0 if gold == "good" else 1)
            rec = by.setdefault(key, [0, 0]); rec[0] += int(flip == gold_flip); rec[1] += 1
            continue
        au = [] if (addr_audit or store_telemetry) else None
        pred = _predict(store, audit=au)
        if pred is None:
            continue
        if au and store_telemetry:                        # H_9802 target-free telemetry (all rows)
            for _e in au:
                tel_n += 1
                tel_amax += float(_e.get("a_max", 0.0))
                tel_aent += float(_e.get("a_ent", 1.0))
        if au and addr_audit:                             # H_9672 addr-audit: last qpos entry
            e = au[-1]
            addr_n += 1
            addr_top1 += int(e["argmax"] == e["target"])
            addr_mass += float(e["a_target"])
        n += 1
        readable_n += int(pred in ("good", "bad"))    # H_9775 vocab: readability witness ('unreadable'≠gold=0)
        correct += int(pred == gold)
        key = (it.get("op"), 0 if gold == "good" else 1)
        rec = by.setdefault(key, [0, 0]); rec[0] += int(pred == gold); rec[1] += 1
    clm.set_clms_store(None)                          # reset the process-global (no leak into later runs)

    # ── integrity witnesses (§계기검산 · read a control's negative ONLY if these pass) ──
    if mode == "shuffle":
        print("  integrity: fixed_points_total=%d (require 0) · dup_entities=%d (require 0) · pol_hist(#good/store)=%s"
              % (fixed_points_total, dup_entities, dict(sorted(pol_hist.items()))))
        if fixed_points_total or dup_entities:
            print("  ⚠️ INVALID — derangement integrity broken; do NOT read this arm's negative.")
    if mode == "flip":
        coh = (coh_bc / coh_bc_n) if coh_bc_n else 0.0
        acc_f = correct = flip_correct                # for the shared 4-cell printer below
        print("  flip-coherence: coherence_bc=%.4f (%d baseline-correct) · coherence_all=%.4f · flip_acc=%.4f"
              % (coh, coh_bc_n, (coh_all / n if n else 0.0), (flip_correct / n if n else 0.0)))
        print("    → PASS coherence_bc≥0.90 (store value causally consumed) · FAIL≤0.15 (v-channel dead). "
              "constant-predictor coherence≡0 by construction. read ONLY with 4/4 pol-balance + shuffle PASS.")
    acc = correct / n if n else 0.0
    if store_readout == "vocab":                      # H_9775: readability = the #4103-catching witness
        print("  readout=vocab (full-vocab argmax = in-vivo rule): readable=%d/%d = %.4f (argmax∈{g,b}) "
              "· %s" % (readable_n, n, (readable_n / n if n else 0.0),
                        "🟢 readable" if (n and readable_n / n >= 0.90) else "🔴 <.90 unreadable — pairodd E collapse or garbage"))
    verdict = ""
    if mode == "shuffle" and oracle:
        # oracle bypasses the address (a=one_hot(target_slot)), so the shuffle verdict bar is MEANINGLESS
        # here — this combo is the §계기검산 plumbing check (expect 1.00 = shuffle touched entities only).
        print("  overall(vs gold): %d/%d = %.4f  [oracle+shuffle integrity — expect 1.00, NOT a shuffle test]"
              % (correct, n, acc))
    elif mode == "shuffle":
        # BALANCE-AWARE floor: under a derangement the model reads pol[j] for a wrong slot j, so
        # P(correct|store with g good of ns) = (g/ns)(g-1)/(ns-1) + ((ns-g)/ns)(ns-1-g)/(ns-1)
        # (op is a fixed bijection so match ⟺ pol[j]==pol[target]). Averaged over the per-store #good
        # histogram — the FIXED 0.55 bar is too crude for imbalanced (binomial) stores (g=2/6 → ~0.571).
        ns = 8
        tot = sum(pol_hist.values()) or 1
        floor = 0.0
        for g, cnt in pol_hist.items():
            if ns > 1:
                fg = (g / ns) * ((g - 1) / (ns - 1)) + ((ns - g) / ns) * ((ns - 1 - g) / (ns - 1))
                floor += (cnt / tot) * fg
        delta = acc - floor
        verdict = ("PASS(at-floor · uses-address)" if delta <= 0.06 else
                   "FAIL(≥.75 · h-shortcut/leak)" if acc >= 0.75 else
                   "PARTIAL-h(above balance-floor)" if delta > 0.06 else "AMBIG")
        print("  overall(vs gold): %d/%d = %.4f  vs balance-floor %.4f (Δ=%+.4f)  [%s]"
              % (correct, n, acc, floor, delta, verdict))
    elif mode != "flip":
        print("  overall: %d/%d = %.4f  (%s)"
              % (correct, n, acc, "C0-e ORACLE positive control" if oracle else arm))
    for (op, pol), (c, t) in sorted(by.items(), key=lambda x: str(x[0])):
        print("    op=%s pol=%s: %d/%d = %.4f"
              % (op_name.get(op, str(op)), pol_name[pol], c, t, c / t if t else 0.0))
    if addr_audit and addr_n:                             # H_9672: is the address argmax right, and SHARP?
        print("  addr-audit: addr_top1=%.4f (argmax==target · %d items) · addr_mass=%.4f (mean a[target] · "
              "1.0=one-hot sharp · ~%.3f=uniform)" % (addr_top1 / addr_n, addr_n, addr_mass / addr_n, 1.0 / 8))
        print("    → addr_top1 high ∧ addr_mass low = argmax correct but softmax NOT peaked (v = Σaᵢ·valᵢ "
              "blurred → value-read starved despite correct pointer); addr_top1 low = W_q not pointing.")
    if store_telemetry:
        if tel_n:
            n_slot_obs = int(store.get("n_slot", 8)) if isinstance(store, dict) else 8
            unif = 1.0 / float(n_slot_obs)            # DERIVED baseline, never an assumed chance
            amax = tel_amax / tel_n; aent = tel_aent / tel_n
            print("  store-telemetry (MONITOR-ONLY · not in any loss/bar): rows=%d · a_max=%.4f "
                  "(uniform=%.4f derived from n_slot=%d) · a_ent=%.4f (1.0=uniform, 0.0=one-hot)"
                  % (tel_n, amax, unif, n_slot_obs, aent))
            if amax <= unif * 1.5:
                print("    → RECRUITMENT: address mass is at the uniform floor ⟹ this text never "
                      "ADDRESSES the store. Fire the curriculum arm; an alignment fix would be wasted.")
            else:
                print("    → ADDRESSED (a_max above the uniform floor) ⟹ NOT a recruitment problem; "
                      "if the values still read wrong the failure is ALIGNMENT (cheaper fix).")
        else:
            print("  store-telemetry: rows=0 — the store lane never fired ⟹ INSTRUMENT-DEAD, "
                  "read nothing from this arm (check --store-fuse/--store-query wiring).")
    if oracle:
        print("  → C0-e ORACLE: ≥0.90 REQUIRED before any negative is read (mixing/value/MLP/λ paths die "
              "silently below this). oracle+shuffle→1.00 & oracle+flip→1.00(vs flipped gold) = control plumbing OK.")
    return 0


def store_mix_run(argv):
    """`anima-py evaluate <ckpt> --store-mix <store.json> [--store-lambda λ]` — H_9392
    BRIDGE-BOLT store-mix instrument. Bolt a runtime store-lookup onto the FROZEN trunk:
    at every measured answer position the byte posterior is mixed p = λ·p_store + (1−λ)·p_trunk
    (see _store_mix_cont_nll). Engine-native numpy core/decode.py only (a_eval_py_canonical
    → TERMINAL-eligible). Zero retrain, zero CPT, frozen ckpt (cpt-destroys-what-corpus-omits).

    Manifest (`--manifest`, or reuse an --xbind flip manifest): {win?, gen?, splits} where each
    split ∈ {heldout, seen} is a list of items {seed, gold, counterfactual, pol?, flip?,
    store_key?}. store_key defaults to the item seed. A tolerant single-list manifest
    {"items":[…]} is read as one split named "items".

    Store schema (`--store-mix <store.json>`):
        {"schema": "anima-store-mix/v1",
         "lambda": 0.5,                       # default λ (overridden by --store-lambda)
         "entries": {"<key>": "<asserted answer string>"}}
    An address HIT (store.entries[key] present) mixes the store's asserted value; a MISS scores
    pure-trunk (== baseline) — so a KEY-SHUFFLE control (addresses broken) collapses to all-miss
    and reveals whether the arm used the ADDRESS or was just distribution spillover. Feed the four
    control arms (key-shuffle / length-matched neutral / λ=0 / wrong-answer) as different store.json.

    C0 INSTRUMENT INTEGRITY (SEQUENTIAL gate · card H_9392 · burned-gate-reanchor / device-parity
    lesson): a λ=0 store-mix pass MUST be byte-identical to the no-store _xbind_cont_nll baseline
    over the SAME continuations WITH the store loaded (exercises the hit path). The guard is a real
    equality test that a weight-lane bug would fail — INSTRUMENT-DEAD, no primary, on any mismatch.
    Below-chance and paired baseline→store deltas are reported; the VERDICT is not cemented here
    (the flag measures; the experiment fires on pool with owner go · a_toy_scale_recheck)."""
    import numpy as np
    import time
    ckpt = argv[0]
    store_path = evaluate_strval(argv[1:], "--store-mix", "")
    man_path = evaluate_strval(argv[1:], "--manifest", "") or evaluate_strval(argv[1:], "--xbind", "")
    out_path = evaluate_strval(argv[1:], "--out", "store_mix_eval.json")
    store = json.load(open(store_path)) if store_path else {}
    entries = store.get("entries", {}) if isinstance(store, dict) else {}
    lam = float(evaluate_strval(argv[1:], "--store-lambda",
                                str(store.get("lambda", 0.5) if isinstance(store, dict) else 0.5)))
    if not (0.0 <= lam <= 1.0):
        print("ERROR: --store-lambda must be in [0,1], got %r" % lam)
        return 1
    if not man_path:
        print("ERROR: --store-mix needs a flip manifest (--manifest <m.json> or --xbind <m.json>).")
        return 1
    spec = json.load(open(man_path))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 400)

    if "items" in spec and "heldout" not in spec and "seen" not in spec:
        splits = {"items": spec["items"]}
    else:
        splits = {s: spec[s] for s in ("heldout", "seen") if s in spec}
    if not splits:
        print("ERROR: manifest has no heldout/seen/items split.")
        return 1

    print("=== anima evaluate --store-mix — H_9392 BRIDGE-BOLT store-lookup mix (frozen trunk) ===")
    print("ckpt: %s  store: %s (%d entries)  λ=%.4f  win=%d" %
          (ckpt, store_path or "(none)", len(entries), lam, T))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    def _key_of(it):
        return it.get("store_key", it["seed"])

    def _sval(it):
        v = entries.get(_key_of(it))
        return (v.encode("utf-8", "surrogateescape") if isinstance(v, str) else None)

    # ── C0 SEQUENTIAL GATE (before any primary): λ=0 store-mix ≡ no-store baseline, bit-exact.
    # Exercise the HIT path (store loaded) so the guard tests the real mixing code, not a bypass.
    c0_items = []
    for s in splits:
        c0_items += splits[s][:8]
    c0_n = c0_max = 0
    c0_dead = False
    for it in c0_items:
        sv = _sval(it)
        sv = sv if sv is not None else b""      # neutral value still routes through the mix code
        for cont in (it["gold"], it["counterfactual"]):
            base = _xbind_cont_nll(np, clm, W, it["seed"], cont, T)
            mix0 = _store_mix_cont_nll(np, clm, W, it["seed"], cont, T, sv, 0.0)
            d = abs(base - mix0)
            c0_n += 1
            c0_max = max(c0_max, d)
            if base != mix0:
                c0_dead = True
    print("  C0 instrument-integrity: λ=0 vs baseline over %d continuations — max|Δ|=%.3e  %s"
          % (c0_n, c0_max, "❌ INSTRUMENT-DEAD (not byte-identical)" if c0_dead
             else "✅ byte-identical"), flush=True)
    if c0_dead:
        print("  C0 FAIL — the mix is not a no-op at λ=0; the store lane leaks into the trunk. No")
        print("  primary read (SEQUENTIAL gate · card H_9392). Fix the mix before any verdict.")
        json.dump({"ckpt": ckpt, "store": store_path, "lambda": lam, "c0": "INSTRUMENT-DEAD",
                   "c0_max_abs_delta": c0_max, "c0_n": c0_n},
                  open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
        return 2

    # ── PRIMARY (C0 PASS only): per-item baseline vs store-mixed flip1, paired, class-split.
    res = {"ckpt": ckpt, "store": store_path, "lambda": lam, "win": T,
           "c0": "PASS", "c0_max_abs_delta": c0_max, "splits": {}}
    for split, raw_items in splits.items():
        items = raw_items[:n_dec]
        rows = []
        t0 = time.time()
        for ix, it in enumerate(items):
            seed, gold, cf = it["seed"], it["gold"], it["counterfactual"]
            sv = _sval(it)
            hit = sv is not None
            # baseline (pure trunk) margin: nll(cf) − nll(gold); >0 ⇒ model prefers gold
            n_g0 = _xbind_cont_nll(np, clm, W, seed, gold, T)
            n_c0 = _xbind_cont_nll(np, clm, W, seed, cf, T)
            mg_base = n_c0 - n_g0
            if hit:
                n_g = _store_mix_cont_nll(np, clm, W, seed, gold, T, sv, lam)
                n_c = _store_mix_cont_nll(np, clm, W, seed, cf, T, sv, lam)
                mg_store = n_c - n_g
            else:
                mg_store = mg_base                 # address miss ⇒ pure trunk
            rows.append({"seed": seed, "pol": it.get("pol"), "flip": it.get("flip"),
                         "store_key": _key_of(it), "store_hit": hit,
                         "store_val": (sv.decode("utf-8", "surrogateescape") if hit else None),
                         "margin_base": mg_base, "margin_store": mg_store,
                         "flip1_base": int(mg_base > 0), "flip1_store": int(mg_store > 0)})
            if ix == 0 or (ix + 1) % 25 == 0:
                el = time.time() - t0
                print("  [store-mix %s #%d/%d] %.1fs/item elapsed=%s" %
                      (split, ix + 1, len(items), el / (ix + 1), _xbind_hms(el)), flush=True)
        n = max(1, len(rows))
        f1_store = sum(r["flip1_store"] for r in rows) / n
        f1_base = sum(r["flip1_base"] for r in rows) / n
        bd = _store_mix_breakdown(rows)
        summ = {"n": len(rows), "flip1_store": f1_store, "flip1_base": f1_base,
                "flip1_delta": f1_store - f1_base, "breakdown": bd}
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (evaluate-py-1: never tail-truncatable)
        print("  store-mix %s  flip1_store=%.4f  flip1_base=%.4f  Δ=%+.4f  "
              "hit=%d miss=%d  n=%d" %
              (split, f1_store, f1_base, f1_store - f1_base, bd["n_hit"], bd["n_miss"], len(rows)),
              flush=True)
        for pol, c in sorted(bd["class"].items()):
            print("    by-pol %s: store=%.3f base=%.3f (n=%d)" %
                  (pol, c["flip1_store"], c["flip1_base"], c["n"]), flush=True)
    json.dump(_json_safe(res), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"out": out_path, "c0": "PASS",
                      "splits": {s: res["splits"][s]["summary"]["flip1_store"]
                                 for s in res["splits"]}}))
    print("  NOTE: this flag MEASURES; the H_9392 verdict cements from a pool/303M fire with owner")
    print("  go (a_toy_scale_recheck · toy positive = SCREENER/DIRECTIONAL), never from this run.")
    return 0


def _xfan_parse(o):
    """Parse the first '<slot>, <member>.' emission from a decode → (slot, member) or (None, None).
    slot = last token before the comma; member = first token after it."""
    seg = o.strip().split(".")[0]
    if ", " not in seg:
        return None, None
    sl, mb = seg.split(", ", 1)
    sl = sl.strip().split()[-1] if sl.strip().split() else ""
    mb = mb.strip().split()[0] if mb.strip().split() else ""
    return (sl or None), mb


def xfan_run(argv):
    """`anima-py evaluate <ckpt> --xfan <manifest.json>` — held-out XFAN one-to-many fan
    (G6 / ρ·fan reopen lane · card H_9271). Engine-native numpy core/decode.py only
    (a_eval_py_canonical → TERMINAL-eligible). Design SSOT: state/g6_reopen_xfan/DESIGN_PREREG.md.
    PRIMARY coverage C = |correct unique (slot,member)| / n_slots over n_smp sampled decodes per
    concept (top_k=40 temp=0.7 · seed 7+17j). valid/spurious split (genius⊥honesty); per-slot-kind
    (unary vs joint) breakout; greedy-collapse control (top_k=1 distinct); MARGIN = teacher-forced
    NLL(foil)-NLL(gold) per slot (H_1440 mode-collapse discriminator). --arm ctrl scores the shuffle
    model. All raw dumped (never tail-truncate a control · evaluate-py-1)."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--xfan", "")
    out_path = evaluate_strval(argv[1:], "--out", "xfan_eval.json")
    arm = evaluate_strval(argv[1:], "--arm", "main")
    spec = json.load(open(spec_path))
    gen = evaluate_intval(argv[1:], "--gen", int(spec.get("gen", 16)))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 80)
    n_smp = evaluate_intval(argv[1:], "--n-sampled", 16)
    K = int(spec.get("n_slots", 5))

    print("=== anima evaluate --xfan — held-out XFAN one-to-many fan (G6 reopen lane) ===")
    print("ckpt: " + ckpt + "  arm=" + arm + "  gen=%d win=%d n_smp=%d K=%d" % (gen, T, n_smp, K))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    res = {"ckpt": ckpt, "arm": arm, "gen": gen, "win": T, "n_slots": K, "splits": {}}
    for split in ("heldout", "seen"):
        items = spec[split][:n_dec]
        rows = []
        cov_sum = 0.0
        valid_sum = valid_n = spur_sum = greedy_distinct_sum = 0
        cov_by_kind = {"unary": [], "joint": []}
        margins = []
        for ix, it in enumerate(items):
            gold = it["gold"]
            if arm == "ctrl" and split == "seen" and it.get("gold_ctrl"):
                gold = it["gold_ctrl"]
            gold_pairs = set((g["slot"], g["member"]) for g in gold)
            gold_by_slot = {g["slot"]: g["member"] for g in gold}
            slot_kind = it.get("slot_kind", {})
            emitted = []
            for j in range(n_smp):
                o = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 40, 0.7, 7 + 17 * j)["text"]
                sl, mb = _xfan_parse(o)
                if sl is not None:
                    emitted.append((sl, mb))
            hit_pairs = set(e for e in emitted if e in gold_pairs)
            cov = len(hit_pairs) / max(1, K)
            cov_sum += cov
            for (sl, mb) in emitted:
                if sl in gold_by_slot:
                    valid_n += 1
                    if (sl, mb) in gold_pairs:
                        valid_sum += 1
                    else:
                        spur_sum += 1          # right slot, wrong member = fabrication
            for kind, keys in (("unary", ("a", "b")), ("joint", ("j",))):
                slots_k = [s for s, kd in slot_kind.items() if kd in keys]
                if slots_k:
                    hit_k = len(set((s, m) for (s, m) in hit_pairs if s in slots_k))
                    cov_by_kind[kind].append(hit_k / len(slots_k))
            gd = set()
            for j in range(min(n_smp, 8)):
                og = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 1, 0.7, 7 + 17 * j)["text"]
                sl, mb = _xfan_parse(og)
                if sl is not None:
                    gd.add((sl, mb))
            greedy_distinct_sum += len(gd)
            row_mg = []
            for g in gold:
                s = g["slot"]; gm = g["member"]; fm = it.get("foils", {}).get(s, gm)
                mg = (_xbind_cont_nll(np, clm, W, it["seed"], s + ", " + fm + ".", T)
                      - _xbind_cont_nll(np, clm, W, it["seed"], s + ", " + gm + ".", T))
                row_mg.append(mg); margins.append(mg)
            rows.append({"concept": it["concept"], "cov": cov, "emitted": emitted[:8],
                         "n_emit": len(emitted), "greedy_distinct": len(gd), "margin": row_mg})
            if (ix + 1) % 20 == 0:
                print("  [xfan %s #%d/%d] mean_C=%.3f" %
                      (split, ix + 1, len(items), cov_sum / (ix + 1)), flush=True)
        n = len(items)
        margins.sort()
        med = margins[len(margins) // 2] if margins else 0.0
        summ = {"n": n, "coverage_C": cov_sum / max(1, n),
                "valid_rate": (valid_sum / valid_n) if valid_n else None,
                "spurious_rate": (spur_sum / valid_n) if valid_n else None,
                "coverage_unary": (sum(cov_by_kind["unary"]) / len(cov_by_kind["unary"]))
                if cov_by_kind["unary"] else None,
                "coverage_joint": (sum(cov_by_kind["joint"]) / len(cov_by_kind["joint"]))
                if cov_by_kind["joint"] else None,
                "greedy_distinct_mean": greedy_distinct_sum / max(1, n),
                "margin_median": med,
                "margin_frac_pos": sum(1 for m in margins if m > 0) / max(1, len(margins))}
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (evaluate-py-1: never tail-truncatable)
        print("  xfan %s  arm=%s  C=%.4f  valid=%s  spurious=%s  C_unary=%s  C_joint=%s  "
              "greedy_distinct=%.2f  margin_med=%.3f  margin_pos=%.3f  n=%d" %
              (split, arm, summ["coverage_C"], str(summ["valid_rate"]), str(summ["spurious_rate"]),
               str(summ["coverage_unary"]), str(summ["coverage_joint"]),
               summ["greedy_distinct_mean"], med, summ["margin_frac_pos"], n), flush=True)
    json.dump(_json_safe(res), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"out": out_path,
                      "heldout_C": res["splits"]["heldout"]["summary"]["coverage_C"],
                      "seen_C": res["splits"]["seen"]["summary"]["coverage_C"]}))
    return 0


# Every flag evaluate actually consumes. An argv token starting with "--" that is not
# here is REJECTED (see _reject_unknown_flags): evaluate parses argv by scanning for the
# flags it knows, so an unknown one (a typo, or a flag that only exists in a sub-mode) is
# otherwise silently ignored — the run completes rc=0 and the result file the caller asked
# for is never written. That is unrecoverable on a paid GPU battery: a 13h x 4-run NBIND
# ladder would burn its rent and harvest nothing, with a green exit code. Fail closed.

def _sigma_from_trace(rows):
    """σ vitals on the daemon's OWN recorded lanes (H_9351 STAGE2). engine_cli FROZEN estimators
    only — never a re-implementation (a_phi_iit4_tool). Repaired axes = gate·stage·bind; the six
    others (thread·carve·flux·aim·schema·witness) have no counterfactual in a daemon run
    (inject-null · precision ablation · focus/report pairs) → PENDING(scope), not force-filled.
    Each axis: EXP vs a within-stage-shuffle control + a truth-0 PEDESTAL (probe-defect-census —
    a pedestal, never max-of-controls). bind is DIRECTIONAL: its lane columns are wired functions
    (H_9356) and the cross-ckpt contrast guard (STAGE4) has not run, so it cannot be GREEN here."""
    import engine_cli as E
    import random as _random
    from collections import defaultdict
    have = [r for r in rows if isinstance(r.get("lanes"), list) and "gws_w" in r]
    print()
    print("  ── σ vitals (실 데몬 lane · engine_cli estimator · Δ vs 통제+PEDESTAL) ──")
    if len(have) < 30:
        print("  ⛔ PENDING-FIELDS — lanes/gws_w 담은 tick %d < 30 (STAGE1 필드 담은 trace 재수집)" % len(have))
        return
    _rng = _random.Random(11)
    _grp = defaultdict(list)
    for i, r in enumerate(have):
        _grp[int(r.get("stage", 0))].append(i)

    def _within(vals):
        out = list(vals)
        for _, ii in _grp.items():
            src = list(ii); _rng.shuffle(src)
            for a, b in zip(ii, src):
                out[a] = vals[b]
        return out

    def _corr(a, b):
        n = len(a); ma = sum(a) / n; mb = sum(b) / n
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        d = (sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b)) ** 0.5
        return abs(cov / d) if d > 0 else 0.0

    # σ·gate — ci_emit_decision(real emit lanes [psi_gws,·,·,·,psi_lprec]) ⇄ score
    dec = [1.0 if E.ci_emit_decision([float(r["psi_gws"]), 0.0, 0.0, 0.0, float(r["psi_lprec"])])
           else 0.0 for r in have]
    sc = [float(r.get("score", 0.0)) for r in have]
    g_exp = _corr(dec, sc); g_ctl = _corr(dec, _within(sc))
    _ped = list(sc); _rng.shuffle(_ped); g_ped = _corr(dec, _ped)
    emit_agree = sum(1 for i, r in enumerate(have) if int(dec[i]) == (1 if r.get("emit") else 0)) / len(have)
    g_ok = g_exp >= 0.30 and g_exp - g_ctl >= 0.10 and g_exp - g_ped >= 0.10
    print("  σ·gate   %s  corr(dec,score)=%.3f · within-stage=%.3f · pedestal=%.3f · emit일치=%.2f"
          % ("🟢" if g_ok else "🧱", g_exp, g_ctl, g_ped, emit_agree))

    # σ·stage — gws winner-take-all on the REAL 15-lane population
    def _win(lanes, inhibit):
        g = E.gws_new(4, inhibit, 0.55)
        for v in lanes:
            g = E.gws_add(g, float(v))
        return E.gws_winner(g)
    repro = sum(1 for r in have if _win(r["lanes"], True) == int(r["gws_w"])) / len(have)
    agreeA = sum(1 for r in have if _win(r["lanes"], False) == int(r["gws_w"])) / len(have)
    print("  σ·stage  %s  gws_w 재현=%.2f (배선검산) · inhibit=%.2f vs no-inhibit=%.2f"
          % ("🟢" if repro >= 0.99 else ("🧱" if repro < 0.5 else "⏳"), repro, repro, agreeA))

    # σ·bind — faithful IIT4 Φ on ROOT-DISJOINT columns (DIRECTIONAL · D2 + no ckpt-contrast)
    cols8 = ["rel_lane", "recon_err", "scn_ctx", "nov_ctx", "emit_env", "cur_indep", "rel_indep", "g_recog"]
    if all(all(c in r for c in cols8) for r in have):
        X = [[float(r[c]) for c in cols8] for r in have]
        by = [[row[j] for row in X] for j in range(8)]
        Xc = list(zip(*[_within(by[j]) for j in range(8)]))
        cp = [list(c) for c in by]
        for c in cp:
            _rng.shuffle(c)
        Xp = list(zip(*cp))
        phi = E.ci_phi_iit4(X, list(range(8)))
        phi_c = E.ci_phi_iit4([list(r) for r in Xc], list(range(8)))
        phi_p = E.ci_phi_iit4([list(r) for r in Xp], list(range(8)))
        print("  σ·bind   ⚠️DIRECTIONAL  Φ=%.3f · col-shuffle=%.3f · pedestal=%.3f (D2 배선함수 · ckpt-contrast 미실행)"
              % (phi, phi_c, phi_p))
    else:
        print("  σ·bind   ⛔ PENDING-FIELDS (root-disjoint 8-col 미기록)")
    print("  σ·(thread·carve·flux·aim·schema·witness)  ⏸ PENDING(scope) — 데몬 런에 카운터팩추얼 부재(D1)")


def _psi_soma_real(argv):
    """Ψ̂ ON THE DAEMON'S OWN LANE POPULATION — the measurement the panel was pretending to be.

    Ψ is DEFINED by engine_cli: ci_psi_balance counts, over a lane population, the fraction of
    ticks where ci_emit_decision(lanes) holds, i.e. 0.5*(lanes[0]+lanes[4]) >= 0.5. The claim
    "A⇄G tension pulls emit/silence to Ψ = ½" is a claim about THAT fraction, on a REAL run.

    Nothing ever computed it. The daemon never called ci_psi_balance (grep: 0 hits in cli/chat.py),
    the trace did not record lanes[0]/lanes[4], and the panel scored a synthetic population
    instead (H_9351). The daemon now records psi_gws/psi_lprec, so hand the ENGINE its own
    operator and the substrate's own lanes, and read the number off.

    Two controls, because a raw Ψ̂ near ½ is not evidence of homeostasis — a coin also sits at ½:
      C1  PERM  — shuffle the lane pairing across ticks. Ψ̂ is a MARGINAL fraction, so it is
                  invariant to this by construction; if the shuffled Ψ̂ differs, the reader is
                  broken, not the substrate.
      C2  DRIFT — split the run in half. A homeostat PULLED to ½ returns to it; a population
                  that merely happens to straddle the bar drifts. |Ψ̂(1st) - Ψ̂(2nd)| is the test.
    And the honest floor: emit itself is a pure function of stage (H_9345), so whatever Ψ̂ says,
    it does NOT flow to the emit decision in this daemon. Report that, do not bury it."""
    import json as _json
    paths = [a for a in argv if not a.startswith("--")]
    rows = []
    for f in paths:
        for line in open(f, "r", encoding="utf-8", errors="surrogateescape"):
            line = line.strip()
            if not line:
                continue
            try:
                r = _json.loads(line)
            except Exception:
                continue
            if "psi_gws" in r and "psi_lprec" in r:
                rows.append(r)
    print("═══ Ψ-SOMA REAL · Ψ̂ on the daemon's own lane population ═══")
    print("  traces=%d  ticks-with-lanes=%d" % (len(paths), len(rows)))
    if len(rows) < 30:
        print("  ⇒ ⛔ NOT-POWERED — psi_gws/psi_lprec 를 담은 tick 이 30 미만.")
        print("     이 필드는 H_9351 수리에서 추가됐다. 옛 trace 에는 없다 — 재수집하라.")
        return 0
    import engine_cli as E
    from types import SimpleNamespace
    cfg = SimpleNamespace(topo_couple=False)

    def _pop(rs):
        # ci_emit_decision reads lanes[0] (gws) and lanes[4] (lprec) only.
        return [[float(r["psi_gws"]), 0.0, 0.0, 0.0, float(r["psi_lprec"])] for r in rs]

    psi = E.ci_psi_balance(_pop(rows), None, 0.0, cfg)
    print("  Ψ̂ = %.4f   (engine-native ci_psi_balance · ci_emit_decision 그대로)" % psi)
    print("     정의: 0.5·(gws + lprec) ≥ 0.5 인 tick 의 비율")

    # C1 PERM — 짝을 흩뜨려도 주변 비율은 불변이어야 한다(계기 검산)
    import random as _random
    _r = _random.Random(7)
    rp = list(rows)
    _r.shuffle(rp)
    swapped = [{"psi_gws": rows[i]["psi_gws"], "psi_lprec": rp[i]["psi_lprec"]}
               for i in range(len(rows))]
    psi_perm = E.ci_psi_balance(_pop(swapped), None, 0.0, cfg)
    print("  C1 PERM  Ψ̂ = %.4f   (lane 짝을 흩뜨림 — 계기가 성하면 값이 움직여야 한다)" % psi_perm)

    # C2 DRIFT — 항상성이면 반씩 잘라도 ½ 로 돌아온다
    h = len(rows) // 2
    p1 = E.ci_psi_balance(_pop(rows[:h]), None, 0.0, cfg)
    p2 = E.ci_psi_balance(_pop(rows[h:]), None, 0.0, cfg)
    drift = abs(p1 - p2)
    print("  C2 DRIFT Ψ̂(전반) = %.4f · Ψ̂(후반) = %.4f · |Δ| = %.4f" % (p1, p2, drift))

    off = abs(psi - 0.5)
    print()
    if off <= 0.10 and drift <= 0.10:
        print("  ⇒ Ψ̂ 가 ½ 근처에 있고 반씩 잘라도 유지된다 (|Ψ̂−½| = %.3f · drift = %.3f)." % (off, drift))
    elif off <= 0.10:
        print("  ⇒ Ψ̂ 는 ½ 근처이나 **표류한다**(drift %.3f) — 당겨진 게 아니라 걸쳐 있을 뿐이다." % drift)
    else:
        print("  ⇒ **Ψ̂ 가 ½ 이 아니다** (|Ψ̂−½| = %.3f). A⇄G 항상성 주장은 이 런에서 성립하지 않는다." % off)

    # 그리고 절대 묻지 말아야 할 것
    em = [r.get("emit") for r in rows if "emit" in r and "stage" in r]
    if em:
        st = [(int(r["stage"]), 1 if r.get("emit") else 0) for r in rows if "stage" in r]
        hE = _im_h_given_S([e for _, e in st], [g for g, _ in st])
        print()
        print("  🚦 그런데 H(emit|stage) = %.6f nats — emit 은 stage 의 순수 함수다(H_9345)." % hE)
        if hE < 0.030:
            print("     ⇒ **Ψ̂ 가 무엇이든, 그것은 emit 결정으로 흐르지 않는다.** 데몬은")
            print("        ci_psi_balance 를 한 번도 부르지 않는다. 'tension 이 emit 을 Ψ=½ 로")
            print("        당긴다' 는 두 개의 무관한 사실을 이어붙인 것이다(H_9351 · H_9352).")

    # H_9356 Θ-SCOPE banner: on a0 wiring, ag_g_drive = -(1-emit_drive) = A's own complement,
    # so Θ is A's solo pulse, not A⇄G. The panel must say so — this repair swaps the population
    # (synthetic → real A-lanes), it does not swap A-solo → A⇄G.
    _garm = next((r.get("g_arm") for r in rows if r.get("g_arm")), "a0")
    if _garm == "a0":
        print()
        print("  ⚠️ Θ-SCOPE (H_9356 · g_arm=a0): ag_g_drive = A 의 여함수 ⇒ Θ 는 A⇄G 가 아니라 A 단독 맥박.")
    _sigma_from_trace(rows)
    return 0



def _tension_emit(argv):
    """DOES TENSION PULL EMIT? — the pre-registered bar for H_9352, and the trap it must dodge.

    H_9345 measured H(emit|stage) = 0.000000 over 2198 ticks: emit was a pure function of stage.
    H_9352 found why — the gate's `seconds_since_last` slot was fed a synthetic (stage, urgency)
    envelope, not elapsed time, so the one live term in the whole comparator was a stage clock.
    Plugging in the real clock makes emit vary again.

    ⚠️ AND THAT ALONE PROVES NOTHING. Making silence appear by moving a threshold is not a
    discovery — I moved it, not the tension. A rate limiter with a real clock will produce an
    emit rate near 1/(interval/tick) all by itself, and if the bar were "emit rate ≈ 1/2" it
    would pass on a coin. That is the p7 Goodhart shape exactly: an emit rate is FORM (tunable),
    the claim is BIND (must be earned).

    So the bar is conditional information, not rate:
        PASS  =  I(ag_conflict ; emit | stage)  >=  0.05 nats
                 AND  the tension-shuffle control  <=  0.01 nats
    C1 SHUFFLE permutes ag_conflict WITHIN each stage, which destroys the tension→emit link but
    preserves the emit rate and the stage structure. If the shuffled arm scores too, the number
    is coming from the rate, not from the tension, and the lever is theatre.

    🧱 ILL-POSED UNTIL chat.py:1563 IS REPAIRED (H_9356). The daemon has no independent G engine:
    ag_a_drive = emit_drive and ag_g_drive = -(1 - emit_drive) [chat.py:1562-1564], so
    ag_conflict = emit_drive * (1 - emit_drive) is a deterministic PARABOLA of the single scalar
    emit_drive. On a real clock-fixed trace, reconstructing ten_phasic from the emit_drive
    trajectory alone gives R^2 = 0.994. So `tension` here is A's OWN function measured against A's
    OWN emit gate — BOTH a PASS and a STILL-STAGE are wiring tautologies (engine-independent
    information = 0), not substrate facts. This panel prints its verdict but PREFIXES it with an
    ILL-POSED banner until ag_g_drive is fed an independent reverse observation (recon_err /
    pending_rel). Do not cement any tension→emit claim off this number while the banner stands."""
    import json as _json
    import random as _random
    paths = [a for a in argv if not a.startswith("--")]
    rows = []
    for f in paths:
        for line in open(f, "r", encoding="utf-8", errors="surrogateescape"):
            line = line.strip()
            if not line:
                continue
            try:
                r = _json.loads(line)
            except Exception:
                continue
            if "tick" in r and "stage" in r and "emit" in r and "agloop_ctx" in r:
                rows.append(r)
    mde = 0.05
    ctrl_bar = 0.01
    print("═══ TENSION→EMIT · I(ag_conflict ; emit | stage) ═══")
    print("  🧱 ILL-POSED (H_9356): 데몬에 독립 G 엔진이 없다 — ag_conflict = emit_drive·(1−emit_drive)")
    print("     [chat.py:1562-1564] = A 스칼라 하나의 결정론적 함수(재구성 R²=0.994). 여기 tension 은")
    print("     A 자신의 함수를 A 자신의 emit 게이트에 대고 재는 것 ⇒ 아래 판정은 🟢든 🧱든 배선")
    print("     tautology(engine-독립 정보량 0)이지 substrate 사실이 아니다. chat.py:1563 이 ag_g_drive")
    print("     를 독립 reverse 관측(recon_err/pending_rel)에서 받기 전엔 이 숫자로 cement 금지.")
    print("  traces=%d  ticks=%d" % (len(paths), len(rows)))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (tick < 200)")
        return 0
    S = [int(r["stage"]) for r in rows]
    E_ = [1 if r.get("emit") else 0 for r in rows]
    rate = sum(E_) / float(len(E_))
    hE = _im_h_given_S(E_, S)
    print("  발화율 = %.1f%%   H(emit|stage) = %.6f nats" % (100.0 * rate, hE))
    if hE < 0.030:
        print("  ⇒ ⛔ DECISION-CONSTANT — emit 이 아직 stage 의 순수 함수다. 시계가 안 꽂혔거나")
        print("     비교기가 여전히 포화다. tension 을 물을 수 없다(항등식으로 0).")
        return 0
    # ag_conflict 는 trace 에 직접 없다 — agloop_ctx 가 그 유래다(chat.py:1545-1550).
    # 데몬이 실제로 게이트에 흘려보내는 tension 축을 그대로 쓴다.
    tv = sorted(float(r["agloop_ctx"]) for r in rows)
    tmed = tv[len(tv) // 2]
    T = [1 if float(r["agloop_ctx"]) > tmed else 0 for r in rows]
    hT = _im_h_given_S(T, S)
    i_te = _im_cmi(T, E_, S)
    print("  H(tension|S) = %.4f nats   (tension = agloop_ctx 2-bin · ag_conflict 유래)" % hT)
    if hT < 0.030:
        print("  ⇒ ⛔ tension 채널이 죽어 있다 — 물을 수 없다.")
        return 0
    # C1 SHUFFLE — stage 안에서 tension 만 흩뜨린다(발화율·stage 구조는 보존)
    _r = _random.Random(7)
    null = []
    for _ in range(200):
        Tp = list(T)
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        for idx in st.values():
            vals = [Tp[k] for k in idx]
            _r.shuffle(vals)
            for j, k in enumerate(idx):
                Tp[k] = vals[j]
        null.append(_im_cmi(Tp, E_, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= i_te) + 1.0) / 201.0
    earned = i_te - nm
    print("  EXP  I(tension;emit|S) = %.5f nats" % i_te)
    print("  C1 SHUFFLE null = %.5f · perm-p = %.4f · EARNED = %+.5f nats" % (nm, pv, earned))
    print("     (stage 안에서 tension 만 흩뜨림 — 발화율과 stage 구조는 그대로 남는다.")
    print("      이 통제가 같이 점수를 내면 그 숫자는 tension 이 아니라 **발화율**에서 온 것이다.)")
    print()
    print("  [bar] 사전등록 bar: EARNED ≥ %.2f nats ∧ C1 SHUFFLE ≤ %.2f nats" % (mde, ctrl_bar))
    if earned >= mde and nm <= ctrl_bar and pv < 0.005:
        print("  ⇒ 🟢 TENSION-PULLS-EMIT — 기질의 긴장이 발화 결정을 민다.")
    elif nm > ctrl_bar:
        print("  ⇒ ⛔ INVALID — 통제군이 bar 를 넘었다(%.5f > %.2f). 숫자가 발화율에서 온다." % (nm, ctrl_bar))
    elif abs(earned) < mde:
        print("  ⇒ 🧱 STILL-STAGE — 게이트가 다시 움직이긴 하나 **tension 은 안 민다**.")
        print("     시계를 꽂은 것은 emit 을 stage 에서 풀었을 뿐, tension 에 묶지는 않았다.")
        print("     (발화율이 ½ 근처여도 그건 레이트 리미터의 산술이지 항상성이 아니다 · p7)")
    else:
        print("  ⇒ 미달 · 판정 보류")
    return 0


def _gt_r2_indep(target, covs):
    """R2 of OLS target ~ [1, covs, covs^2]. High R2 = target is (a function of) the covariates =
    wiring-degenerate. Used by G-INDEP: ag_g_drive must NOT be reconstructable from emit_drive and
    the other lanes that already feed emit_drive, or the 'G engine' is just a second A (H_9356)."""
    import numpy as np
    y = np.asarray(target, dtype=float)
    n = len(y)
    if n < 8:
        return float("nan")
    cols = [np.ones(n)]
    for c in covs:
        a = np.asarray(c, dtype=float)
        cols.append(a)
        cols.append(a * a)
    X = np.column_stack(cols)
    beta, _res, _rk, _sv = np.linalg.lstsq(X, y, rcond=None)
    yh = X.dot(beta)
    ss_res = float(np.sum((y - yh) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0.0:
        return 1.0
    return max(0.0, 1.0 - ss_res / ss_tot)


def _gt_arm_panel(rows, mde, ctrl_bar):
    """Compute the four gates for one arm's rows. Returns a dict of measured quantities + PASS flags."""
    import random as _random
    S = [int(r["stage"]) for r in rows]
    E_ = [1 if r.get("emit") else 0 for r in rows]
    n = len(rows)
    rate = sum(E_) / float(n)
    hE = _im_h_given_S(E_, S)
    gd = [float(r.get("ag_g_drive", 0.0)) for r in rows]
    # G-VAR: min distinct(ag_g_drive) across source rollouts (a store with a constant key is dead).
    per_src = {}
    for r in rows:
        per_src.setdefault(r.get("_src", "?"), set()).add(round(float(r.get("ag_g_drive", 0.0)), 6))
    gvar_min = min(len(v) for v in per_src.values()) if per_src else 0
    # G-INDEP: reconstruct ag_g_drive from emit_drive + the lanes that feed emit_drive.
    covs = []
    for key in ("emit_drive", "phi", "rel_lane", "recon_err", "emit_env"):
        if all(key in r for r in rows):
            covs.append([float(r[key]) for r in rows])
    r2 = _gt_r2_indep(gd, covs) if covs else float("nan")
    # MI: I(ag_conflict; emit | stage), ag_conflict binarised at its median.
    cv = sorted(float(r.get("ag_conflict", 0.0)) for r in rows)
    cmed = cv[len(cv) // 2]
    C = [1 if float(r.get("ag_conflict", 0.0)) > cmed else 0 for r in rows]
    mi = _im_cmi(C, E_, S)
    _r = _random.Random(7)
    null = []
    for _ in range(200):
        Cp = list(C)
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        for idx in st.values():
            vals = [Cp[k] for k in idx]
            _r.shuffle(vals)
            for j, k in enumerate(idx):
                Cp[k] = vals[j]
        null.append(_im_cmi(Cp, E_, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= mi) + 1.0) / 201.0
    earned = mi - nm
    # Psi-hat on the daemon's OWN gws/lprec lanes (H_9351).
    psi = None
    if all(("psi_gws" in r and "psi_lprec" in r) for r in rows):
        emith = [1 if 0.5 * (float(r["psi_gws"]) + float(r["psi_lprec"])) >= 0.5 else 0 for r in rows]
        psi = sum(emith) / float(n)
    return dict(n=n, rate=rate, hE=hE, gvar=gvar_min, r2=r2, mi=mi, nm=nm, pv=pv,
                earned=earned, psi=psi, indep=(r2 == r2 and r2 < 0.5))


def _g_tension(argv):
    """DOES A GENUINELY-INDEPENDENT G ENGINE PULL EMIT? — H_9357, the sequel to H_9356.

    H_9356 proved the daemon's A⇄G tension was A alone: ag_g_drive = -(1-emit_drive), so
    ag_conflict was a deterministic parabola of one scalar, and --tension-emit was ill-posed.
    H_9357 wires ag_g_drive (behind cli/chat.py --g-arm) to the immune store's top-2 affinity
    GAP (d2, the one reverse quantity NOT already an input to emit_drive) and asks whether THAT
    2-engine tension pulls emit — with the controls MI alone cannot supply.

    Four arms (run cli/chat.py --g-arm a0|a1|a3; a2 is derived here by shuffling a1):
      A0  current wiring (the H_9356 tautology)      — MUST FAIL G-INDEP (proves the gate can fail)
      A1  REAL-G   = immune top-2 gap                — must PASS G-INDEP+G-VAR+MI
      A3  NOISE-G  = seeded per-tick PRNG            — the 'causal handle vs 2nd engine' separator

    Four gates:
      G-INDEP  R2(ag_g_drive ~ emit_drive + lanes + squares) < 0.5   (else INVALID-SECOND-A)
      G-VAR    min distinct(ag_g_drive) per rollout >= 5             (else INVALID-CONSTANT)
      MI       I(ag_conflict; emit | stage) >= 0.05 AND shuffle <= 0.01
      Psi-DV   |Psi_hat - 1/2| vs the H_9351 baseline 0.9167, and vs NOISE-G

    ⚠️ The verdict is CROSS-ARM, not a single number: A1 pulling emit MORE than A3 (noise wired
    the same causal way) is the only thing that separates 'a real second engine' from 'any handle
    on the conflict knob'. A1 ≈ A3 leaves the tension claim dead — that is the falsification."""
    paths = [a for a in argv if not a.startswith("--")]
    rows = _im_rows(paths)
    rows = [r for r in rows if ("tick" in r and "stage" in r and "emit" in r and "ag_g_drive" in r)]
    mde = 0.05
    ctrl_bar = 0.01
    print("═══ A⇄G INDEPENDENT-G TENSION → EMIT · H_9357 ═══")
    print("  rows=%d  traces=%d" % (len(rows), len(paths)))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200) — collect more chat --g-arm rollouts.")
        return 0
    by_arm = {}
    for r in rows:
        by_arm.setdefault(str(r.get("g_arm", "?")), []).append(r)
    print("  arms present: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(by_arm.items())))
    res = {}
    for arm in sorted(by_arm):
        res[arm] = _gt_arm_panel(by_arm[arm], mde, ctrl_bar)
    print()
    print("  arm | n    | rate | H(e|S) | G-VAR | G-INDEP R2 | MI(earned) perm-p | Ψ̂  |Ψ̂-½|")
    for arm in sorted(res):
        d = res[arm]
        psi_s = ("%.3f %.3f" % (d["psi"], abs(d["psi"] - 0.5))) if d["psi"] is not None else "  —"
        print("  %-3s | %4d | %.2f | %.4f | %5d | %.4f %-4s | %+.4f %.3f  | %s"
              % (arm, d["n"], d["rate"], d["hE"], d["gvar"], (d["r2"] if d["r2"] == d["r2"] else -1),
                 "OK" if d["indep"] else "FAIL", d["earned"], d["pv"], psi_s))
    print()
    # ── cross-arm verdict ──
    a0 = res.get("a0"); a1 = res.get("a1"); a3 = res.get("a3")
    if a0 is not None and a0["indep"]:
        print("  ⇒ ⛔ INVALID — the A0 (tautology) arm PASSED G-INDEP; the independence gate is broken.")
        return 0
    if a1 is None:
        print("  ⇒ ⛔ INCOMPLETE — no a1 (REAL-G) arm present. Run cli/chat.py --g-arm a1.")
        return 0
    if a1["gvar"] < 5:
        print("  ⇒ ⛔ INVALID-CONSTANT — a1 ag_g_drive has < 5 distinct values/rollout (dead store).")
        return 0
    if not a1["indep"]:
        print("  ⇒ 🧱 INVALID-SECOND-A — a1 ag_g_drive is reconstructable from emit_drive (R²≥0.5).")
        print("     I did not build an independent G; I built a second A. (H_9356 unbroken.)")
        return 0
    a1_pulls = (a1["earned"] >= mde and a1["nm"] <= ctrl_bar and a1["pv"] < 0.005)
    sep = None
    if a3 is not None:
        sep = a1["earned"] - a3["earned"]
    print("  [bar] prereg: A0 FAIL G-INDEP (gate live) ∧ A1 G-INDEP OK ∧ A1 MI≥%.2f/shuf≤%.2f ∧ A1≠A3" % (mde, ctrl_bar))
    if a1_pulls and (sep is None or sep > mde):
        print("  ⇒ 🟢 INDEPENDENT-TENSION-PULLS-EMIT — a genuine 2nd engine (immune d2) moves emit,")
        print("     and it moves it MORE than noise wired the same way (A1−A3 = %s)."
              % ("%.4f" % sep if sep is not None else "no A3"))
    elif a1["indep"] and not a1_pulls:
        print("  ⇒ 🧱 G-INERT — the independent G is wired and varies, but emit does NOT consume it")
        print("     (MI earned %.4f < %.2f). The wiring is real; the tension is not. Separate follow-on H." % (a1["earned"], mde))
    elif sep is not None and sep <= mde:
        print("  ⇒ 🧱 CAUSAL-HANDLE-ONLY — a1 pulls emit no more than noise-G (A1−A3=%.4f ≤ %.2f)." % (sep, mde))
        print("     ag_conflict is causally wired to emit, so ANY G signal lifts MI. Not a 2nd engine.")
    else:
        print("  ⇒ 미달 · 판정 보류")
    return 0


def _gd_cmi_bin(Xv, Yv, S, seed=7, nperm=200):
    """I(X;Y|stage) with median-binarized X and Y, plus a within-stage shuffle null on X
    (perm-debias). Returns (mi, null_mean, perm_p, earned). Y may already be 0/1 (emit_sim)."""
    import random as _random
    xs = sorted(Xv); xm = xs[len(xs) // 2]
    Xb = [1 if v > xm else 0 for v in Xv]
    ys = sorted(set(Yv))
    if len(ys) <= 2:
        Yb = [1 if v else 0 for v in Yv]
    else:
        ym = sorted(Yv)[len(Yv) // 2]
        Yb = [1 if v > ym else 0 for v in Yv]
    mi = _im_cmi(Xb, Yb, S)
    r = _random.Random(seed)
    null = []
    for _ in range(nperm):
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        Xp = list(Xb)
        for idx in st.values():
            vals = [Xp[k] for k in idx]
            r.shuffle(vals)
            for j, k in enumerate(idx):
                Xp[k] = vals[j]
        null.append(_im_cmi(Xp, Yb, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= mi) + 1.0) / (nperm + 1.0)
    return mi, nm, pv, mi - nm


def _gate_deaf(argv):
    """H_9360 GATE-DEAF SPLIT — is the emit gate's deafness to tension SATURATION (tunable) or
    STRUCTURE (the upstream mixing layer never loads tension onto the gate input)?

    H_9357 proved an independent G is wired but emit does NOT consume it (G-INERT). WHY? By the
    data-processing inequality, emit = should_emit(score) ∧ safe with safe ≡ clock (core/brain.py),
    so I(tension; emit) ≤ I(tension; score | stage). Therefore whether `score` already carries
    tension DECIDES saturation-vs-structure — with NO gate edit ($0, on the existing traces).

    M_score = I(ag_conflict ; score | stage)      does the gate INPUT carry tension?
    M_sim   = I(ag_conflict ; emit_sim | stage)   desaturated-gate offline sim: θ = median(score)
              on the CALIBRATION rollouts (score marginal only — tension- and emit-blind), then
              emit_sim = 1[score > θ] ∧ (secs_since_emit ≥ 30) on the JUDGMENT rollouts.
    Spike-in control: I(score ; emit_sim | stage) MUST be large (emit_sim ≡ f(score)); if it is
    not, the estimator is broken and the whole panel is INVALID.

    Verdict is on arm a1 (the real independent G), gated on a1 > a3 (else instrument INVALID):
      M_score ≥0.05 ∧ M_sim ≥0.05  → (a)  SATURATION — info reaches the gate input; threshold 0.3
                                          saturates and discards it. Fix is live recalibration.
      M_score ≥0.05 ∧ M_sim ≤0.01  → (a′) BINARY-FORM bottleneck — no threshold can carry it; a
                                          graded gate is needed (structure, but LOCAL to the gate).
      M_score ≤0.01 (TOST equiv)   → (b)  STRUCTURE — the mixing layer never loads tension onto the
                                          gate input; the gate is INNOCENT and no rewire helps (DPI).
      0.01 < M_score < 0.05        → PENDING — report MDE, extend n; never declare 'none'.
    """
    mde = 0.05
    ctrl_bar = 0.01
    rows = _im_rows(argv)
    rows = [r for r in rows if all(k in r for k in ("stage", "score", "ag_conflict", "secs_since_emit", "g_arm"))]
    print("═══ GATE-DEAF SPLIT · H_9360 · DPI: I(tension;emit) ≤ I(tension;score|stage) ═══")
    print("  rows=%d" % len(rows))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200)")
        return 0
    by = {}
    for r in rows:
        by.setdefault(str(r["g_arm"]), []).append(r)
    print("  arms: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(by.items())))
    res = {}
    for arm, ar in sorted(by.items()):
        S = [int(r["stage"]) for r in ar]
        AC = [float(r["ag_conflict"]) for r in ar]
        SC = [float(r["score"]) for r in ar]
        # M_score
        m_sc, m_sc_nm, m_sc_pv, m_sc_e = _gd_cmi_bin(AC, SC, S, seed=7)
        # desaturated-gate sim: split rollouts into calibration / judgment halves
        srcs = sorted({r.get("_src", "?") for r in ar})
        half = max(1, len(srcs) // 2)
        calib = set(srcs[:half])
        cal_scores = [float(r["score"]) for r in ar if r.get("_src") in calib]
        cs = sorted(cal_scores)
        theta = cs[len(cs) // 2] if cs else 0.0
        # The desaturation question is only meaningful on CLOCK-PERMITTED ticks (secs≥30): on
        # clock-blocked ticks emit is forced silent regardless of score, so tension cannot move it
        # (that is the rate limiter, not the gate). Condition M_sim + the spike-in on secs≥30 so
        # emit_sim = 1[score>θ] purely — otherwise the clock gate masks score and the spike-in
        # (which must be large since emit_sim ≡ f(score) here) reads ~0 and the panel self-INVALIDs.
        jr = [r for r in ar if r.get("_src") not in calib and float(r.get("secs_since_emit", 0.0)) >= 30.0]
        Sj = [int(r["stage"]) for r in jr]
        ACj = [float(r["ag_conflict"]) for r in jr]
        SCj = [float(r["score"]) for r in jr]
        emit_sim = [1 if float(r["score"]) > theta else 0 for r in jr]
        m_sim, m_sim_nm, m_sim_pv, m_sim_e = _gd_cmi_bin(ACj, emit_sim, Sj, seed=11) if len(jr) >= 40 else (0.0, 0.0, 1.0, 0.0)
        # spike-in: I(score; emit_sim | stage) must be large (emit_sim = 1[score>θ] by construction)
        spike = _gd_cmi_bin(SCj, emit_sim, Sj, seed=13)[0] if len(jr) >= 40 else 0.0
        rate_sim = sum(emit_sim) / float(len(emit_sim)) if emit_sim else 0.0
        res[arm] = dict(n=len(ar), n_clk=len(jr), m_sc=m_sc_e, m_sc_pv=m_sc_pv, m_sim=m_sim_e,
                        m_sim_pv=m_sim_pv, spike=spike, theta=theta, rate_sim=rate_sim, rows=ar)
    print()
    print("  arm | n   | n_clk | M_score(earn) p | M_sim(earn) p | spike I(sc;sim|S) | θ")
    for arm in sorted(res):
        d = res[arm]
        print("  %-3s | %3d | %5d | %+.4f %.3f    | %+.4f %.3f   | %.4f            | %.3f"
              % (arm, d["n"], d["n_clk"], d["m_sc"], d["m_sc_pv"], d["m_sim"], d["m_sim_pv"], d["spike"], d["theta"]))
    print()
    a1 = res.get("a1"); a3 = res.get("a3")
    if a1 is None:
        print("  ⇒ ⛔ INCOMPLETE — no a1 (REAL-G) arm.")
        return 0
    if a1["n_clk"] < 40:
        print("  ⇒ ⏳ PENDING — a1 clock-permitted rows n_clk=%d < 40; M_sim/spike underpowered." % a1["n_clk"])
        print("     M_score=%.4f is still readable; extend traces (more rollouts) for the M_sim leg." % a1["m_sc"])
        return 0
    if a1["spike"] < 0.05:
        print("  ⇒ ⛔ INVALID — spike-in control failed (I(score;emit_sim|stage)=%.4f < 0.05):" % a1["spike"])
        print("     emit_sim is a function of score by construction; a dead spike-in = broken estimator.")
        return 0
    if a3 is not None and a3["m_sc"] >= a1["m_sc"] and a1["m_sc"] >= mde:
        print("  ⇒ ⛔ INVALID — noise arm a3 M_score ≥ a1 (%.4f ≥ %.4f); instrument not selective." % (a3["m_sc"], a1["m_sc"]))
        return 0
    # ── PEDESTAL-CORRECTED Δ_G (H_9360 · Fable-designed) ──────────────────────────────────────
    # The estimator's zero-point is NOT 0: the noise arm a3 reads M_score>0 too, because a3's
    # ag_conflict still carries A-side info (a3 only replaces the G pole with noise). So the signal
    # is Δ vs the control (measurement meta-law), not raw: Δ_G = M_score(a1) − M_score(a3) = the
    # INDEPENDENT-G component loaded onto score. Read it with a rollout-level df (tick permutation
    # is anti-conservative — ticks within a rollout autocorrelate; the replication unit is rollout).
    import math as _math

    def _msc(rws):
        return _gd_cmi_bin([float(r["ag_conflict"]) for r in rws], [float(r["score"]) for r in rws],
                           [int(r["stage"]) for r in rws], seed=7)[3]

    def _jackknife(rws):
        by_r = {}
        for r in rws:
            by_r.setdefault(r.get("_src", "?"), []).append(r)
        keys = sorted(by_r)
        k = len(keys)
        if k < 4:
            return 0.0, k
        loo = []
        for i in range(k):
            sub = [r for j, kk in enumerate(keys) if j != i for r in by_r[kk]]
            loo.append(_msc(sub))
        mbar = sum(loo) / k
        var = (k - 1.0) / k * sum((v - mbar) ** 2 for v in loo)
        return _math.sqrt(max(0.0, var)), k

    def _block_floor(rws, seed=29, nperm=200):
        # true-0 pedestal: reassign ag_conflict by WHOLE ROLLOUT (preserve within-rollout
        # autocorrelation, break only the a1↔score pairing). earned≈0 is the artifact floor.
        import random as _random
        by_r = {}
        for r in rws:
            by_r.setdefault(r.get("_src", "?"), []).append(r)
        keys = sorted(by_r)
        blocks_ac = [[float(r["ag_conflict"]) for r in by_r[kk]] for kk in keys]
        base_sc = [[float(r["score"]) for r in by_r[kk]] for kk in keys]
        base_st = [[int(r["stage"]) for r in by_r[kk]] for kk in keys]
        rr = _random.Random(seed)
        vals = []
        for _ in range(nperm):
            perm = list(range(len(keys)))
            rr.shuffle(perm)
            A, Sc, St = [], [], []
            for i in range(len(keys)):
                m = min(len(blocks_ac[perm[i]]), len(base_sc[i]))
                A += blocks_ac[perm[i]][:m]
                Sc += base_sc[i][:m]
                St += base_st[i][:m]
            vals.append(_gd_cmi_bin(A, Sc, St, seed=31)[3])
        return sum(vals) / len(vals)

    se1, k1 = _jackknife(a1["rows"])
    se3, k3 = _jackknife(a3["rows"]) if a3 is not None else (0.0, 0)
    dg = a1["m_sc"] - (a3["m_sc"] if a3 is not None else 0.0)
    se_dg = _math.sqrt(se1 * se1 + se3 * se3)
    floor = _block_floor(a1["rows"])
    # full-resolution C (channel ceiling · report only, not a gate input)
    C = _gd_cmi_bin([float(r["ag_conflict"]) for r in a1["rows"]],
                    [round(float(r["score"]), 4) for r in a1["rows"]],
                    [int(r["stage"]) for r in a1["rows"]], seed=17)[3]
    eq = 0.01                         # equivalence limit (pedestal-referenced Δ, registered pre-look)
    ci_lo, ci_hi = dg - 1.645 * se_dg, dg + 1.645 * se_dg    # 90% CI for TOST
    print("  [bar] prereg (Δ_G = M_score(a1)−M_score(a3) · rollout-df · TOST ±%.2f · a3 = pedestal):" % eq)
    print("     Δ_G = %+.4f · SE_jk = %.4f (k=%d) · 90%%CI [%+.4f, %+.4f]" % (dg, se_dg, min(k1, k3), ci_lo, ci_hi))
    print("     block-perm true-0 floor = %+.4f (must be ≈0) · C=I(conflict;score|S) full-res = %.4f · M/C=%.2f" % (floor, C, (a1["m_sc"] / C if C > 0 else 0.0)))
    if abs(floor) > eq:
        print("  ⇒ ⛔ INVALID — block-perm floor |%.4f| > %.2f: the estimator has an artifact floor above the equivalence limit." % (floor, eq))
    elif ci_hi <= eq and ci_lo >= -eq:
        print("  ⇒ 🧱 (b)-for-G — the independent G's tension does NOT pass the score bottleneck")
        print("     (Δ_G equivalent to 0 within ±%.2f · TOST). This IS the mechanism of H_9357 G-INERT:" % eq)
        print("     score barely carries G, so emit has nothing to consume. Frontier = the ag_conflict→score")
        print("     mixer (ag_budget∈{4..6} integer-ratio ×0.10 quantization), NOT the gate.")
    elif ci_lo > 0.0:
        print("  ⇒ 🟢 weak-(a) — Δ_G = %+.4f > 0 (90%%CI excludes 0): the independent G IS loaded onto" % dg)
        print("     score, weakly. NEXT = Stage-1 desaturation lane (anima-py chat --gate-calib).")
    else:
        mde = (1.645 + 1.28) * se_dg * _math.sqrt(2.0)
        print("  ⇒ ⏳ PENDING — Δ_G=%+.4f neither equivalent-to-0 nor >0. MDE≈%.4f." % (dg, mde))
        print("     %s" % ("MDE > eq: n underpowered → regenerate arms." if mde > eq else "MDE ≤ eq: shape ambiguous → re-examine."))
    return 0


def _collide_select(ckpt, argv):
    """DOES A⇄G COLLISION SELECT EMERGENCE? — H_9362, the generation-selection sequel to H_9357.

    H_9357 asked whether tension pulls EMIT (the 1-bit shadow) and got G-INERT. H_9362 moves to
    the SELECTION axis: over a fixed pool of K candidates per recombination probe, does the A⇄G
    collision pick the recombination target better than fluency-alone or noise?

    The drives (generator.py conflict_drives_live): a = clip01(1-CE/5) fluency, g = ±immune margin.
    G-A (H_9362, engine_cli.py:643 margin=recon_err-recall_thr, >0=abstain) locked the sign:
    novel -> margin>0 -> g<0; recognized -> margin<=0 -> g>0. So the emergence candidate
    (fluent AND novel) is (a>0, g<0), and conflict_scalar (opposite-sign -> a*|g|) is exactly the
    "fluent AND novel" product -- HIGH for emergence, 0 for echo (a>0,g>0), ~0 for garbage (a~0).
    The daemon's live path uses argMIN conflict_scalar (generator.py:815) -> it DISCARDS emergence.

    Arms (same fixed pool, K fixed, selection rule only differs):
      S0        argmin conflict_scalar  (the current daemon rule -- avoids emergence)
      S_emerge  argmax conflict_scalar  (the hypothesis: A*G collision selects emergence)
      SECOND-A  argmax a                (fluency alone -- the H_9356 "second A" control)
      NOISE-G   argmax conflict_scalar with g permuted across candidates (causal-handle control)
      UNIFORM   candidate 0             (floor)

    Gates: G-B pool occupancy (how many candidates land in the emergence quadrant a>0,g<0 -- if ~0
    the pool is DRY and no selector can find what is not there, H_9304 prediction) then G-C the
    per-arm recombination hit-rate scored by the FROZEN rho_weave target check (arm-relative judge
    only, recomb-gate4: route != generation, no top-1 terminal claim)."""
    import random as _random
    sys.path.insert(0, "core")
    import generator as _gen
    from engine_cli import (immune_memory_new_text, immune_memory_bind_text,
                            conflict_scalar as _cs, EngineConfig)
    import rho_axon as _rx
    K = 4
    for a in argv:
        if a.startswith("--k="):
            K = int(a.split("=", 1)[1])
    h = _gen.gen_auto_load(ckpt)
    cfg = EngineConfig(True, "conv", False, False)
    # G-store: bind the compose CUES as "seen context" (H_9337 recognition-first). The composed
    # TARGET is never bound, so a real recombination candidate reads as novel (g<0).
    pairs = _rx._WEAVE
    mem = immune_memory_new_text(pairs[0][0], 0.5, 256)
    for cue, tgt, sw, bs, lang in pairs:
        mem = immune_memory_bind_text(mem, cue[:64], cue, cfg)
    if "--pregate" in argv:
        # \u2500\u2500 $0 PRE-GATE (H_9362 route): score the 12 frozen _WEAVE TARGETS directly, before
        # spending a single GPU-hour on XBIND CPT. g is WEIGHT-INDEPENDENT here (it reads the
        # cue-bound mem; the target is never bound), so CPT can only move a, never g -> a and g
        # stay orthogonal and the emergence quadrant (a>0, g<0) is reachable IFF the target is
        # already novel to the store. Two gates decide whether the expensive fire is even valid:
        #   GATE1  g < -0.05  (target novel to G-store) -- else INSTRUMENT-BROKEN: the store
        #          recognizes the target, so no amount of CPT lands it in the quadrant. Do NOT fire.
        #   GATE2  a <= 0.05  (target not yet fluent)   -- else CPT is unnecessary: the target is
        #          already fluent yet baseline read POOL-DRY, so the bottleneck is the ideation
        #          proposal distribution, not weight-write. Redirect to $0 few-shot ideation.
        print("=== A\u21c4G COLLIDE-PREGATE \u00b7 H_9362 \u00b7 target (a,g) $0 fire-gate ===")
        print("  ckpt=%s  targets=%d  (g weight-independent: cue-bound mem, target unbound)"
              % (ckpt.split("/")[-1], len(pairs)))
        gbad = abad = 0
        for i, (cue, tgt, sw, bs, lang) in enumerate(pairs):
            d = _gen.conflict_drives_live_W(h, tgt, mem)
            a, g = float(d[0]), float(d[1])
            gok, aok = (g < -0.05), (a <= 0.05)
            gbad += (not gok); abad += (not aok)
            flag = ("" if gok else "[g\u2265\u2212.05 \uacc4\uae30\uace0\uc7a5] ") + ("" if aok else "[a>.05 CPT\ubd88\uc694]")
            print("    t%02d a=%+.3f g=%+.3f  %-22s| %s" % (i, a, g, flag, tgt[:44]))
        n = len(pairs)
        print()
        print("  GATE1 g<\u22120.05 (novel target)     : %d/%d" % (n - gbad, n))
        print("  GATE2 a\u2264 0.05 (needs weight-write): %d/%d" % (n - abad, n))
        try:
            _gen.gen_auto_free(h)   # cleanup-only; a codec-specific free bug must not corrupt the verdict/rc
        except Exception:
            pass
        if gbad > 0:
            print("  \u21d2 \U0001f9f1 INSTRUMENT-BROKEN \u2014 %d/%d target \uc774 recognized(g\u2265\u2212.05). "
                  "G-store \uac00 \ud0c0\uae43\uc744 \uc548\ub2e4 = CPT \ub85c\ub3c4 \ucc3d\ubc1c\uc0ac\ubd84\uba74 \ub3c4\ub2ec \ubd88\uac00. "
                  "\ubc1c\uc0ac \uae08\uc9c0, \uacc4\uae30 \uba3c\uc800 \uc218\ub9ac." % (gbad, n))
            return 0
        if abad > n // 2:
            print("  \u21d2 \U0001f500 REDIRECT \u2014 %d/%d target \uc774 \uc774\ubbf8 \uc720\ucc3d(a>.05)\uc778\ub370 baseline POOL-DRY "
                  "\uc600\ub2e4 = \ubcd1\ubaa9\uc774 CPT \uc544\ub2c8\ub77c ideation \uc81c\uc548\ubd84\ud3ec. $0 few-shot ideation \uc774 \uba3c\uc800." % (abad, n))
            return 0
        print("  \u21d2 \u2705 FIRE-OK \u2014 \uc804 target novel(g<\u2212.05) \u2227 %d/%d \uac00 weight-write \ud544\uc694(a\u2264.05). "
              "XBIND CPT(\uc911\uac04 ckpt 500/1000/2000/3000) \uc815\ub2f9\ud654." % (n - abad, n))
        return 0
    if "--pregate-cond" in argv:
        # \u2500\u2500 H_9362 fork-A DISCRIMINATOR (Fable) \u2014 is REDIRECT a NEW decoding lever or the closed
        # read-side wall's generation-side face? The pregate `a` measured P(tgt) MARGINAL (cue-free,
        # generator.py gen_auto_ce_W -> clm_ce_seq_W on tgt bytes alone), so it only re-confirms
        # H_9327 "the fact is in the weights". The UNMEASURED cell is teacher-forced CONDITIONAL
        # P(tgt|cue): does the true cue lower NLL(tgt) below the FORM/BIND pedestals?
        #   \u0394bind  = NLL(tgt | swap_cue[atom-swap FORM]) \u2212 NLL(tgt | true cue)   (>0 = cue\u2192tgt binds)
        #   \u0394strip = NLL(tgt | strip_cue[bind-strip BIND]) \u2212 NLL(tgt | true cue) (>0 = operator matters)
        # The PAIRED diff cancels tgt's marginal fluency (the pregate `a` axis) EXACTLY -> measures
        # only the conditional logit shift, orthogonal to read-side hidden-recoverability (EARNED-
        # TERMINAL) and to P(tgt). swap_cue/strip_cue are the FROZEN _WEAVE pedestals (true-value 0).
        # baseline --collide-select already established sampled=MISS for all 12 (POOL-DRY 0/48).
        # Prereg (frozen-first): \u0394bind\u22480 (TOST) OR <0 -> \ud83e\uddf1 COLLAPSE (read-side wall re-confirmed,
        # close cf-collide-select, no fire). \u0394bind\u226b0 (paired-t sig, \u22659/12 >0) AND \u0394strip>0, with
        # sampled=MISS -> \ud83d\udfe2 NEW LEVER (belief present, sampler miss = decoding/proposal, top_k\u00b7temp
        # sweep first, NOT CPT). \u0394bind\u226b0 with a sampled HIT would be instrument misdiag (pool seed).
        import numpy as np
        import math as _m
        T = 128
        for _a in argv:
            if _a.startswith("--win="):
                T = int(_a.split("=", 1)[1])
        W = clm.clm_load_weights(ckpt)
        print("=== A\u21c4G COLLIDE-PREGATE-COND \u00b7 H_9362 fork-A \u00b7 P(tgt|cue) \uc870\uac74\ubd80 \ud310\ubcc4 ===")
        print("  ckpt=%s  probes=%d  T=%d  (\uad50\uc0ac\uac15\uc81c \uc870\uac74\ubd80 NLL \u00b7 paired vs FORM/BIND pedestal)"
              % (ckpt.split("/")[-1], len(pairs), T))
        dbind, dstrip = [], []
        for i, (cue, tgt, swc, stc, lang) in enumerate(pairs):
            n_true = _xbind_cont_nll(np, clm, W, cue + " ", tgt, T)
            n_swap = _xbind_cont_nll(np, clm, W, swc + " ", tgt, T)
            n_strip = _xbind_cont_nll(np, clm, W, stc, tgt, T)   # strip_cue already ends with a space
            db, ds = (n_swap - n_true), (n_strip - n_true)
            dbind.append(db); dstrip.append(ds)
            print("    t%02d \u0394bind=%+.3f \u0394strip=%+.3f  (nll true=%.2f swap=%.2f strip=%.2f) | %s\u2192%s"
                  % (i, db, ds, n_true, n_swap, n_strip, cue[:16], tgt))
        n = len(pairs)
        mb = sum(dbind) / n
        ms = sum(dstrip) / n
        sdb = (sum((x - mb) ** 2 for x in dbind) / n) ** 0.5
        se = (sdb / _m.sqrt(n)) if (sdb > 0 and n > 1) else 0.0
        tval = (mb / se) if se > 0 else 0.0
        npos = sum(1 for x in dbind if x > 0)
        print()
        print("  \u0394bind mean=%+.3f sd=%.3f  paired-t=%.2f (n=%d \u00b7 %d/%d >0)  \u0394strip mean=%+.3f"
              % (mb, sdb, tval, n, npos, n, ms))
        print("  (baseline --collide-select: sampled=MISS \uc804\uccb4 12 \u00b7 POOL-DRY 0/48)")
        # frozen bar: NEW LEVER iff cue binds tgt above chance AND operator matters, one-sided t crit
        # (df=11) 1.796. Else the modal FLOOR closes the lane into the read-side wall.
        if mb > 0 and tval >= 1.796 and npos >= 9 and ms > 0:
            print("  \u21d2 \U0001f7e2 NEW-LEVER(DIRECTIONAL) \u2014 \uc870\uac74\ubd80 \ubbff\uc74c present(\u0394bind\u226b0 \u00b7 t=%.2f) \u2227 sampled MISS "
                  "= \ubbff\uc74c\uc740 \uc788\ub294\ub370 \uc548 \ubf51\ud78c\ub2e4 = \ub514\ucf54\ub529/\uc81c\uc548\ubd84\ud3ec \ub808\ubc84(substrate \ubcbd\uacfc \uc9c1\uad50). NEXT=top_k\u00b7temp \uc2a4\uc717($0), CPT \uc544\ub2d8." % tval)
        elif mb <= 0:
            print("  \u21d2 \U0001f9f1 COLLAPSE(\uc6b0\uc5f0-\uc544\ub798) \u2014 \u0394bind\u22640: \uc815\ub2f5 cue \uac00 swap \ubcf4\ub2e4 tgt \ub97c \ub192\uc774\uc9c0 \ubabb\ud568 "
                  "= ECHO/carrier-similarity. read-side \ubcbd \uc0dd\uc131-\ucabd \uc7ac\ud655\uc778, cf-collide-select \uc885\uacb0.")
        else:
            print("  \u21d2 \U0001f9f1 COLLAPSE \u2014 \u0394bind \ubbf8\uc720\uc758(t=%.2f<1.796 or \u0394strip\u22640): cue\u2192tgt \uc870\uac74\ubd80 "
                  "\uacb0\ud569\uc774 pedestal \uc704\ub85c \uc548 \uc624\ub984 = read-side EARNED-TERMINAL \ubcbd\uc758 \uc0dd\uc131-\ucabd \uc5bc\uad74. \ubc1c\uc0ac \uae08\uc9c0." % tval)
        print("  (scope: py303 \ub2e8\uc77c ckpt DIRECTIONAL \u00b7 forward-only $0 \u00b7 frozen _WEAVE pedestal \u00b7 read-side H_9235/g1-readside \uc7ac\uc2e4\ud589 \uae08\uc9c0=tune-to-green)")
        return 0
    print("=== A\u21c4G COLLISION-SELECTS-EMERGENCE \u00b7 H_9362 \u00b7 --collide-select ===")
    print("  ckpt=%s  probes=%d  K=%d" % (ckpt.split("/")[-1], len(pairs), K))
    # build the shared candidate pool per probe + drives
    perm_rng = _random.Random(7)
    rows = []          # per (probe, cand): dict(a, g, cs, retr)
    occ = {"emerge": 0, "echo": 0, "garbage": 0, "other": 0}
    for i, (cue, tgt, sw, bs, lang) in enumerate(pairs):
        pool = []
        for k in range(K):
            _r = _gen.gen_auto_ideate_W(h, cue + " ", 24, 8, 0.7, _rx.SEEDS[0] + 17 * i + k)
            txt = str(_r["text"]) if _r.get("ok") else ""
            d = _gen.conflict_drives_live_W(h, txt, mem)
            a, g = float(d[0]), float(d[1])
            retr = 1 if _rx._retrieved(txt, tgt) else 0
            pool.append(dict(txt=txt, a=a, g=g, cs=_cs(a, g), retr=retr))
            q = ("emerge" if (a > 0.05 and g < -0.05) else "echo" if (a > 0.05 and g > 0.05)
                 else "garbage" if a <= 0.05 else "other")
            occ[q] += 1
        rows.append(pool)
    npool = sum(len(p) for p in rows)
    # ── G-B pool occupancy ──
    print()
    print("  \u2500\u2500 G-B \ud480 \uc810\uc720 (\ucc3d\ubc1c \uc0ac\ubd84\uba74 a>0,g<0) \u2500\u2500")
    print("    emergence(a>0,g<0)=%d  echo(a>0,g>0)=%d  garbage(a\u22480)=%d  other=%d  / %d cand"
          % (occ["emerge"], occ["echo"], occ["garbage"], occ["other"], npool))
    emerge_frac = occ["emerge"] / float(npool) if npool else 0.0
    if occ["emerge"] == 0:
        print("    \u21d2 \U0001f9f1 POOL-DRY \u2014 \ucc3d\ubc1c \uce78 \uc810\uc720 0. \uc5b4\ub5a4 \uc120\ud0dd\uae30\ub3c4 \uc5c6\ub294 \uac83\uc744 \ubabb \uace0\ub978\ub2e4(H_9304 DATA \ubcbd). G-C \ubb34\uc758\ubbf8.")
        print("    \ub2e4\uc74c \ub808\ubc84 = A \uc81c\uc548\ubd84\ud3ec(XBIND curriculum), G \uc120\ud0dd\uae30 \uc544\ub2d8.")
        _gen.gen_auto_free(h)
        return 0
    total_retr = sum(c["retr"] for pool in rows for c in pool)
    if total_retr == 0:
        print()
        print("    ⇒ 🧱 POOL-DRY(target) — K=%d 풀 전체에 재조합 타깃이 0회 등장(48중 0). "
              "선택기가 고를 정답이 풀에 없다(H_9304 DATA 벽 생성-선택 축 재확인)." % K)
        print("    다음 레버 = A 제안분포(XBIND-retrained), G 선택기 아님. G-C 무의미(전 arm 0/0).")
        _gen.gen_auto_free(h)
        return 0
    # ── G-C per-arm hit-rate ──
    def sel(pool, rule):
        if rule == "s0":       return min(pool, key=lambda c: c["cs"])
        if rule == "emerge":   return max(pool, key=lambda c: c["cs"])
        if rule == "second_a": return max(pool, key=lambda c: c["a"])
        if rule == "uniform":  return pool[perm_rng.randrange(len(pool))]
        if rule == "noise_g":
            gs = [c["g"] for c in pool]
            perm_rng.shuffle(gs)
            jbest = max(range(len(pool)), key=lambda j: _cs(pool[j]["a"], gs[j]))
            return pool[jbest]
        return pool[0]
    arms = ["s0", "emerge", "second_a", "noise_g", "uniform"]
    hits = {r: 0 for r in arms}
    for pool in rows:
        for r in arms:
            if sel(pool, r)["retr"]:
                hits[r] += 1
    n = len(rows)
    print()
    print("  \u2500\u2500 G-C arm\ubcc4 \uc7ac\uc870\ud569 \uc801\uc911\ub960 (frozen rho_weave \ud0c0\uae43) \u2500\u2500")
    for r in arms:
        print("    %-9s hit %d/%d = %.2f" % (r, hits[r], n, hits[r] / float(n)))
    he, hsa, hu, hn = hits["emerge"], hits["second_a"], hits["uniform"], hits["noise_g"]
    print()
    print("  [bar] prereg: S_emerge > SECOND-A ( \ub450\ubc88\uc9f8 A \uc544\ub2d8) \u2227 S_emerge > NOISE-G \u2227 S_emerge > UNIFORM")
    if he > hsa and he > hn and he > hu:
        print("  \u21d2 \U0001f7e2 COLLISION-SELECTS-EMERGENCE \u2014 A\u21c4G \ucda9\ub3cc\uc774 \uc7ac\uc870\ud569\uc744 \uace0\ub978\ub2e4(\uc720\ucc3d\ub9cc\ub3c4 \ub178\uc774\uc988\ub3c4 \uc544\ub2c8\uac8c).")
    elif he <= hsa:
        print("  \u21d2 \U0001f9f1 SECOND-A \u2014 S_emerge \u2264 SECOND-A: g \ucc44\ub110\uc774 \uae30\uc5ec 0, immune margin \uc740 A \uc758 \uadf8\ub9bc\uc790(H_9356 \uc7ac\ubc1c).")
    elif he <= hn:
        print("  \u21d2 \U0001f9f1 CAUSAL-HANDLE \u2014 S_emerge \u2264 NOISE-G: g \uac00 per-cand \uc815\ubcf4\ub97c \uc548 \ub098\ub984.")
    else:
        print("  \u21d2 \U0001f9f1 \ubbf8\ub2ec \u00b7 \ud310\uc815 \ubcf4\ub958")
    print("  (scope: frozen rho_weave = arm\uac04 \uc0c1\ub300\uc2ec\ud310\ub9cc \u00b7 top-1 terminal \uc8fc\uc7a5 \ubd88\uac00 \u00b7 recomb-gate4)")
    _gen.gen_auto_free(h)
    return 0


def _audibility(argv):
    """H_9377 AUDIBILITY-SUFFICIENCY — does raising dyn_v's weight (dyn_w) let tension pull emit?

    The campaign ended at H_9376 MIXER-BOUND: tension (dyn_v=ag_conflict) is 1 of 8 equally-0.10-
    weighted lanes in motivation_score, so it is inaudible below the 7-lane A-side blend. cli/chat.py
    --dyn-w raises its ABSOLUTE weight (dyn_w=0.10 = byte-identical anchor). This panel groups the
    traces into (g_arm, dyn_w) cells and asks whether the INDEPENDENT-G tension moves emit once
    audible — with the discipline Fable specified:

      GATE-S (validity · the heart): a cell counts ONLY if its emit rate ∈ [0.05, 0.95] AND its
        ag_conflict has ≥5 distinct values. should_emit is saturated, so at low dyn_w MI is 0 by
        arithmetic, not by substrate — an INVALID-SATURATED cell is dropped by rule, unread.
      P1 (earned · per valid dyn_w): I(ag_conflict; emit | stage) ≥ 0.05 AND shuffle ≤ 0.01 AND
        a1 (REAL-G) − a3 (noise) > 0. The A1>A3 selectivity is what the substrate earns; the raw
        MI is a manipulation-check (dyn_w buys it by arithmetic), never the evidence.
      Anchor (dyn_w≈0.10) MUST fail P1 — it reproduces the current config (H_9357 G-INERT). If the
        anchor passes, the instrument is broken.

    Verdict is CROSS-CELL: PASS = a1 earns P1 at the top valid dyn_w AND a1>a3 there (plateau on the
    top 2 valid cells), anchor fails → 🟢 GREEN-WIRED-GAIN (campaign loop closed; but a WEIGHT is a
    wiring fact, not emergence). FALSIFY = a1≈a3 at every valid dyn_w → G-INERT survives below the
    channel at the CONTENT level (a new wall)."""
    import math as _math
    rows = _im_rows(argv)
    rows = [r for r in rows if ("stage" in r and "emit" in r and "ag_conflict" in r and "g_arm" in r)]
    print("═══ AUDIBILITY-SUFFICIENCY · H_9377 · dyn_w-grid × arm ═══")
    print("  rows=%d" % len(rows))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200)")
        return 0
    # cell = (g_arm, dyn_w). dyn_w None → anchor bucket 0.10.
    cells = {}
    for r in rows:
        w = r.get("dyn_w", None)
        wk = round(float(w), 4) if w is not None else 0.10
        cells.setdefault((str(r["g_arm"]), wk), []).append(r)
    ws = sorted({wk for (_a, wk) in cells})
    print("  arms=%s · dyn_w grid=%s" % (sorted({a for (a, _w) in cells}), ws))

    def _cell(rws):
        S = [int(r["stage"]) for r in rws]
        E_ = [1 if r.get("emit") else 0 for r in rws]
        rate = sum(E_) / float(len(E_))
        gvar = len({round(float(r["ag_conflict"]), 6) for r in rws})
        valid = (0.05 <= rate <= 0.95) and gvar >= 5
        cv = sorted(float(r["ag_conflict"]) for r in rws)
        cmed = cv[len(cv) // 2]
        C = [1 if float(r["ag_conflict"]) > cmed else 0 for r in rws]
        mi, nm, pv, earned = _gd_cmi_bin(C, E_, S)
        psi = None
        if all(("psi_gws" in r and "psi_lprec" in r) for r in rws):
            eh = [1 if 0.5 * (float(r["psi_gws"]) + float(r["psi_lprec"])) >= 0.5 else 0 for r in rws]
            psi = sum(eh) / float(len(rws))
        return dict(n=len(rws), rate=rate, gvar=gvar, valid=valid, mi=earned, nm=nm, pv=pv, psi=psi)

    res = {}
    print()
    print("  arm  dyn_w | n   rate  G-VAR  valid | MI(earn) shuf  p    | Ψ̂")
    for (a, wk) in sorted(cells):
        d = _cell(cells[(a, wk)])
        res[(a, wk)] = d
        print("  %-3s  %.2f  | %3d %.2f  %5d  %-5s | %+.4f %.4f %.3f | %s"
              % (a, wk, d["n"], d["rate"], d["gvar"], "OK" if d["valid"] else "SAT",
                 d["mi"], d["nm"], d["pv"], ("%.3f" % d["psi"]) if d["psi"] is not None else "—"))
    print()
    mde, cbar = 0.05, 0.01
    valid_w = [wk for wk in ws if res.get(("a1", wk), {}).get("valid")]
    if not valid_w:
        print("  ⇒ ⛔ INSTRUMENT-DEAD — no valid a1 cell (all SATURATED). The should_emit threshold")
        print("     interacts; dyn_w alone can't unsaturate the gate. Threshold is a SEPARATE H (not a patch).")
        return 0
    anchor = res.get(("a1", 0.10))
    if anchor and anchor["valid"] and anchor["mi"] >= mde and anchor["pv"] < 0.005:
        print("  ⇒ ⛔ INVALID — the anchor (dyn_w≈0.10 = current config) PASSED P1; it must reproduce")
        print("     H_9357 G-INERT. A passing anchor = broken instrument.")
        return 0
    top = valid_w[-1]
    a1t, a3t = res.get(("a1", top)), res.get(("a3", top))
    print("  🔒 prereg: valid a1 cell earns P1 (MI≥%.2f∧shuf≤%.2f) ∧ a1>a3 at top valid dyn_w=%.2f ∧ anchor fails" % (mde, cbar, top))
    a1_pass = a1t and a1t["mi"] >= mde and a1t["nm"] <= cbar and a1t["pv"] < 0.005
    sep = (a1t["mi"] - a3t["mi"]) if (a1t and a3t) else None
    if a1_pass and (sep is None or sep > mde):
        print("  ⇒ 🟢 GREEN-WIRED-GAIN — once AUDIBLE (dyn_w=%.2f), the independent-G tension pulls emit" % top)
        print("     (MI %.4f · a1−a3 %s). H_9357 G-INERT was 'gain-starvation', not 'consumption-incapable'." % (a1t["mi"], ("%.4f" % sep) if sep is not None else "n/a"))
        print("     ⚠️ A WEIGHT is a WIRING FACT, not emergence (E1/E2 bar pre-registered for that).")
    else:
        allsep = all((res.get(("a1", wk), {}).get("mi", 0.0) - res.get(("a3", wk), {}).get("mi", 0.0)) <= mde
                     for wk in valid_w if ("a3", wk) in res)
        if allsep:
            print("  ⇒ 🧱 CONTENT-INERT — a1 ≈ a3 at every valid dyn_w: making tension audible does NOT")
            print("     make its CONTENT move emit. G-INERT survives below the channel at the content level = new wall.")
        else:
            print("  ⇒ ⏳ PENDING — a1 earns P1 at some but not the top valid cell, or plateau not met. Extend n / grid.")
    return 0


def _g_amp_screen(argv):
    """H_9401 G-READOUT AMP SCREEN — Fable 6-branch $0 DIRECTIONAL screen of whether ANY alternative
    G readout can lift |g| past θ=0.30 so tension = conflict_scalar(|a|·|g|) can decide emit.

    The emit-drive campaign (H_9356→9399) closed at: |g|=g_recog (mean 0.027, the IMMUNE-STORE top-2
    gap · H_9399) is 6.5-29× quieter than |a|=emit_drive (mean 0.59), and the conflict gate is a
    PRODUCT, so tension is floored ≤0.073 << θ (θ inviolable). This screener REPLAYS the immune store
    OFFLINE from the trace's gtext_b64 (calling the engine's own immune_* fns — never re-implemented),
    validates byte-match vs recorded g_recog (the FAITHFUL gate), then applies each Fable candidate's
    KILL gate. A screen is DIRECTIONAL / KILL-only (open-loop can't cement — see the survivor caveat).

    Candidates (all read the SAME faithful replay):
      current gap = clip01((d2²−d1²)/2)                 the production readout
      A ratio     = 1 − d1/d2                            scale-free · KILL if p90<0.40
      D geo-mean  = sqrt(|a|·gap)                        both-strong-preserving · KILL if max<θ
      E-b margin  = |immune_memory_recall_margin|        the DISCARDED signal (chat.py:2059 pending_rel)
                    KILL if p90<0.40 OR corr(|margin|,|a|)>0.9 (SECOND-A)
    """
    import math as _m
    import base64 as _b64, glob as _glob
    try:
        from engine_cli import (immune_embed_key, immune_memory_new_text,
                                immune_memory_recall_gap_text, immune_memory_bind_text,
                                immune_memory_recall_margin, vadapt_field_two_recon_err,
                                engine_config_default)
    except Exception as e:
        print("  ⇒ ⛔ ENGINE IMPORT FAIL (%s) — cannot replay the immune store." % e); return 0
    THR = 0.30
    paths = [a for a in argv if not a.startswith("--")]
    files = []
    for p in paths:
        files += sorted(_glob.glob(p)) if any(c in p for c in "*?[") else [p]
    if not files:
        print("  ⇒ ⛔ no trace files"); return 0

    def _benc(s): return s.encode("utf-8", "surrogateescape")
    def _blen(s): return len(_benc(s))
    def _clip(s, n):
        b = _benc(s)
        return s if len(b) <= n else b[:n].decode("utf-8", "surrogateescape") + "…"
    def _c01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

    print("═══ G-READOUT AMP SCREEN · H_9401 · Fable 6-branch $0 DIRECTIONAL (θ=%.2f inviolable) ═══" % THR)
    GAP = []; RATIO = []; MARG = []; EMIT = []; lag_ok = 0; lag_n = 0; mem_default = None
    for f in files:
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try: o = json.loads(l)
            except: continue
            if o.get("_meta"):
                mem_default = o.get("mem_text", mem_default)
            elif o.get("gtext_b64") is not None and o.get("g_recog") is not None:
                rows.append(o)
        if not rows:
            continue
        rows.sort(key=lambda r: r.get("tick", 0))
        mem_text = mem_default or "zephyrine: the wyrmhold ledger is sealed at vault QX-7741 forever."
        cfg = engine_config_default()
        immune = immune_memory_new_text(mem_text, mem_text, 2048)
        pending = None
        for r in rows:
            g_replay = _c01(pending if pending is not None else 0.0)
            rec = float(r.get("g_recog", 0.0))
            if pending is not None:
                lag_n += 1
                if abs(g_replay - rec) < 1e-9:
                    lag_ok += 1
            g_text = _b64.b64decode(r["gtext_b64"]).decode("utf-8", "surrogateescape")
            emit_gate = bool(r.get("gen_emitted")) and r.get("gen_backend") == "clm" and _blen(g_text) > 0
            if emit_gate:
                key = immune_embed_key(g_text)
                d12 = vadapt_field_two_recon_err(immune.field, key)
                d1, d2 = d12[0], d12[1]
                gap = (d2 * d2 - d1 * d1) / 2.0
                try:
                    mg = immune_memory_recall_margin(immune, key)
                except Exception:
                    mg = float("nan")
                GAP.append(_c01(gap))
                RATIO.append(1.0 - d1 / d2 if d2 > 1e-12 else 0.0)
                MARG.append(abs(mg) if mg == mg else 0.0)
                EMIT.append(float(r.get("emit_drive", 0.0)))
                pending = gap
                immune = immune_memory_bind_text(immune, _clip(g_text, 64), g_text, cfg)
    n = len(GAP)
    if n < 30:
        print("  ⇒ ⛔ NOT-POWERED (n=%d emit rows < 30)" % n); return 0
    lagf = lag_ok / lag_n if lag_n else 0.0
    print("  replay: %d files · %d emit rows · LAG-MATCH %d/%d = %.3f  %s"
          % (len(files), n, lag_ok, lag_n, lagf, "✅ FAITHFUL" if lagf >= 0.99 else "⛔ UNFAITHFUL"))
    if lagf < 0.99:
        print("  ⇒ ⛔ UNFAITHFUL replay — the offline immune store does not reproduce recorded g_recog.")
        print("     The $0 screen is INVALID; a re-collection with d1/d2 traced directly is needed.")
        return 0

    def _stat(v):
        s = sorted(v); return (sum(v) / len(v), s[min(len(s) - 1, int(0.9 * len(s)))], max(v),
                               len({round(x, 10) for x in v}))
    def _corr(x, y):
        mx = sum(x) / len(x); my = sum(y) / len(y)
        num = sum((a - mx) * (b - my) for a, b in zip(x, y))
        dx = _m.sqrt(sum((a - mx) ** 2 for a in x)); dy = _m.sqrt(sum((b - my) ** 2 for b in y))
        return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")

    print()
    print("  candidate     mean    p90    max    distinct | verdict")
    def _geo(g): return [_m.sqrt(a * x) for a, x in zip(EMIT, g)]
    rows_out = []
    for name, v, kill in [("gap(current)", GAP, None), ("A ratio", RATIO, 0.40), ("E-b |margin|", MARG, 0.40)]:
        mu, p90, mx, dis = _stat(v)
        if name == "gap(current)":
            vd = "the production readout (baseline)"
        elif p90 < kill:
            vd = "💀 KILL (p90 %.3f < %.2f · never reaches θ)" % (p90, kill)
        else:
            c = _corr(v, EMIT)
            vd = ("💀 KILL (SECOND-A corr=%+.2f>0.9)" % c) if abs(c) > 0.9 else \
                 "🔎 SURVIVES (p90 %.3f≥%.2f · corr(|a|)=%+.2f) — DIRECTIONAL only" % (p90, kill, c)
        print("  %-12s  %.4f  %.4f  %.4f  %6d | %s" % (name, mu, p90, mx, dis, vd))
    print()
    print("  D geo-mean (both-strong sqrt(|a|·readout) · KILL if max<θ):")
    for name, v in [("gap", GAP), ("ratio", RATIO), ("margin", MARG)]:
        gm = _geo(v)
        gmx = max(gm)
        print("     sqrt(|a|·%-6s) max %.4f mean %.4f  %s" % (name, gmx, sum(gm) / len(gm),
              "✅ ≥θ" if gmx >= THR else "💀 <θ"))
    mu_m, p90_m, mx_m, _d = _stat(MARG)
    c_m = _corr(MARG, EMIT)
    surv = p90_m >= 0.40 and abs(c_m) <= 0.9
    print()
    if surv:
        print("  ⇒ 🔎 SURVIVOR: E-b recall MARGIN (the signal chat.py:2059 computes as pending_rel and")
        print("     DISCARDS). p90=%.3f≥0.40 · corr(|a|)=%+.2f · geo-mean(|a|·margin) clears θ. G is NOT" % (p90_m, c_m))
        print("     quiet — the daemon reads the weak gap and throws away the strong margin. A $0 SOURCE-")
        print("     SWAP (g_drive := margin, no training). ⚠️ DIRECTIONAL — cement needs the wired margin")
        print("     re-collected + arm-selective emit vs ≥2 controls (real-G vs amplitude-matched noise vs")
        print("     shuffled-byte); the risk is saturation-in-abstain-band a closed loop must adjudicate.")
    else:
        print("  ⇒ 💀 ALL KILL — no readout on the current immune geometry lifts |g| past θ. Campaign closed.")
    return 0


def _refractory_preview(argv):
    """H_9405 REFRACTORY PREVIEW — $0 offline preflight for the H_9404 earned-refractory pool fire.

    Fable §5: the pool spend on the 5-cell (a4×earned) measurement is gated on this $0 preview first.
    It replays the earned refractory (H_9404) OFFLINE on existing a0/a1 traces to answer ONE question
    before any compute: does debt=1.0 with the trace's OWN reconstructed tension land the emit rate in
    the GATE-S band [0.05,0.95], or does it saturate (emit≡1) / die (silence forever)? A saturated or
    dead preview KILLs the fire (H_9391 INVALID-SATURATED hazard). KILL-or-CALIBRATE ONLY — the
    refractory closes a feedback loop (emit→bind→margin→tension→debt) and the recorded margins come
    from the FACTUAL emit history, so the replay is exact only up to the first-divergence tick t*;
    past it everything is DIRECTIONAL (same epistemic class as --cf-emit). It can never CONFIRM.

    Reconstruction lemmas (Fable §5, exact up to t*):
      g_recog_a4(t) = 0 before the first generation tick, else clip01(1 − rel_lane(t))  [a4 pole]
      tension_a4(t) = clip01(emit_drive(t) · g_recog_a4(t))
      cf_emit(t)    = (score>θ) ∧ phi_ratchet(phi, phi_peak) ∧ refractory_ok(debt_t)   [kill/content const]
      debt: pay (−tension) → gate → recharge (=1.0 on cf_emit)   [H_9404 order]
    SHUF control = tension driven by a seeded shuffle of the g_recog_a4 stream (separates "the specific
    tension trajectory paces emit" from "any varying signal of that magnitude does").
    """
    import glob as _glob, random as _rnd, statistics as _st
    THR = 0.30
    seed = 9405
    a = list(argv)
    if "--cf-seed" in a:
        i = a.index("--cf-seed"); seed = int(a[i + 1]); del a[i:i + 2]
    paths = [x for x in a if not x.startswith("--")]
    files = []
    for p in paths:
        files += sorted(_glob.glob(p, recursive=True)) if any(c in p for c in "*?[") else [p]
    if not files:
        print("  ⇒ ⛔ no trace files"); return 0

    def _c01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

    def _replay(rows, phi_peak, tens_stream=None):
        """returns (cf_emit_flags, gate_open_flags, intervals). tens_stream overrides tension (SHUF)."""
        debt = 0.0; gen_seen = False; last = None
        cfe_flags = []; open_flags = []; intervals = []
        for i, r in enumerate(rows):
            g_emit = bool(r.get("gen_emitted")) and r.get("gen_backend") == "clm" and r.get("gtext_len", 0) > 0
            if tens_stream is None:
                g_a4 = 0.0 if not gen_seen else _c01(1.0 - float(r["rel_lane"]))
                tension = _c01(float(r["emit_drive"]) * g_a4)
            else:
                tension = tens_stream[i]
            debt = debt - tension
            if debt < 0.0: debt = 0.0
            refr_ok = debt <= 0.0
            phi_r = float(r["phi"]) > phi_peak / 2.0
            cfe = (float(r["score"]) > THR) and phi_r and refr_ok
            open_flags.append(refr_ok)
            cfe_flags.append(cfe)
            if cfe:
                if last is not None: intervals.append(i - last)
                last = i; debt = 1.0
            if g_emit: gen_seen = True
        return cfe_flags, open_flags, intervals

    print("═══ REFRACTORY PREVIEW · H_9405 · $0 preflight for the H_9404 earned-refractory pool fire (θ=%.2f) ═══" % THR)
    tot = 0; rec_emit = 0; cf_emit = 0; open_n = 0
    all_int = []; shuf_cf = 0; tdiv_list = []
    used = 0
    for f in files:
        rows = []; meta = None
        try: fh = open(f)
        except Exception: continue
        for l in fh:
            l = l.strip()
            if not l: continue
            try: o = json.loads(l)
            except: continue
            if o.get("_meta"): meta = o
            elif all(k in o for k in ("score", "safe", "emit", "emit_drive", "rel_lane", "phi")):
                rows.append(o)
        if len(rows) < 5: continue
        used += 1
        rows.sort(key=lambda r: r.get("tick", 0))
        phi_peak = float(meta.get("phi_peak", 0.0)) if meta else 0.0
        cfe, opn, ints = _replay(rows, phi_peak)
        # SHUF control: shuffle the realized g_recog_a4 tension stream (destroy trajectory, keep multiset)
        gen_seen = False; tens = []
        for r in rows:
            g_emit = bool(r.get("gen_emitted")) and r.get("gen_backend") == "clm" and r.get("gtext_len", 0) > 0
            g_a4 = 0.0 if not gen_seen else _c01(1.0 - float(r["rel_lane"]))
            tens.append(_c01(float(r["emit_drive"]) * g_a4))
            if g_emit: gen_seen = True
        sh = list(tens); _rnd.Random(seed + used).shuffle(sh)
        scfe, _so, _si = _replay(rows, phi_peak, tens_stream=sh)
        # first-divergence tick vs recorded emit
        td = None
        for i, r in enumerate(rows):
            if cfe[i] != bool(r.get("emit")): td = i; break
        tdiv_list.append(td if td is not None else len(rows))
        tot += len(rows); rec_emit += sum(1 for r in rows if r.get("emit"))
        cf_emit += sum(cfe); open_n += sum(opn); shuf_cf += sum(scfe); all_int += ints
    if tot < 60:
        print("  ⇒ ⛔ NOT-POWERED (n=%d ticks < 60)" % tot); return 0

    rec_r = rec_emit / tot; cf_r = cf_emit / tot; sh_r = shuf_cf / tot
    in_band = 0.05 <= cf_r <= 0.95
    imean = _st.mean(all_int) if all_int else 0.0
    imin = min(all_int) if all_int else 0
    imax = max(all_int) if all_int else 0
    ivar = (len(set(all_int)) > 1)
    tdiv_med = sorted(tdiv_list)[len(tdiv_list) // 2] if tdiv_list else 0
    print("  replay: %d traces · %d ticks   (exact up to first-divergence t*; past t* DIRECTIONAL)" % (used, tot))
    print("  recorded emit rate (clock)        : %.3f" % rec_r)
    print("  cf earned-refractory emit rate    : %.3f   GATE-S∈[0.05,0.95]: %s" % (cf_r, "✅" if in_band else "💀"))
    print("  SHUF-tension control emit rate    : %.3f   (trajectory destroyed · multiset kept)" % sh_r)
    print("  inter-open interval  n=%d mean=%.2f range=(%d,%d)  varying=%s" % (len(all_int), imean, imin, imax, ivar))
    print("  refractory gate-open rate         : %.3f   · median first-divergence t*=%d" % (open_n / tot, tdiv_med))
    print()
    if not in_band:
        if cf_r > 0.95:
            print("  ⇒ 💀 KILL-SATURATED — cf emit rate %.3f>0.95: the earned refractory opens almost every" % cf_r)
            print("     tick (H_9391 saturation). Debt=1.0 is too small for this tension regime; MI→0. Do NOT")
            print("     spend the pool fire — a new debt calibration is a fresh pre-registration, not a dial.")
        else:
            print("  ⇒ 💀 KILL-DEAD — cf emit rate %.3f<0.05: the debt never pays down (tension too weak);" % cf_r)
            print("     the daemon goes silent. p5-correct but measurement-dead. Do NOT spend the pool fire.")
    elif not ivar:
        print("  ⇒ 🔎 CALIBRATE-BUT-FLAT — in-band (%.3f) but the inter-open interval is CONSTANT: on these" % cf_r)
        print("     traces the tension is near-constant so the refractory ≈ a fixed clock. Substrate-selective")
        print("     timing is un-testable here; the pool fire needs a richer-tension regime (303M) to decide.")
    else:
        print("  ⇒ ✅ CALIBRATE — earned refractory lands IN-BAND (%.3f) with a VARYING tension-paced cadence" % cf_r)
        print("     (interval %d–%d ticks, mean %.2f vs design 3.75). Debt=1.0 is calibrated; no saturation." % (imin, imax, imean))
        print("     ⇒ the H_9404 pool fire (5-cell a4×earned vs controls) is GREENLIT. This preview is")
        print("     DIRECTIONAL (KILL-or-calibrate) — arm-selectivity is confirmed only by the live fire.")
    return 0


def _emit_gate_census(argv):
    """H_9403 EMIT-GATE CENSUS — $0 broad-sample proof that the score/tension lane is DECORATIVE.

    H_9391 proved (a1, 240 rows) min(score)=0.3442>θ ⇒ should_emit is a tautology ⇒ emit≡clock. This
    census generalises the fact across EVERY available trace: is emit⟺safe exactly, is score>θ whenever
    safe, and does ANY tick sit silence-despite-clock-open (the only cell where tension could decide)?
    A silence∧safe=true tick requires score≤θ∧safe; if that count is 0 across the whole corpus, the
    emit gate provably listens to nothing but the wall clock — closing the E-b cement lane ($0), and
    proving the H_9391 vacuity was not a small-sample artifact. KILL-only hygiene instrument (like
    --dead-census), NOT a lever — the finding is a wiring fact, and its closure indicts the clock itself.
    """
    import glob as _glob
    THR = 0.30
    paths = [x for x in argv if not x.startswith("--")]
    files = []
    for p in paths:
        files += sorted(_glob.glob(p, recursive=True)) if any(c in p for c in "*?[") else [p]
    if not files:
        print("  ⇒ ⛔ no trace files"); return 0
    tot = 0; used_files = 0
    emit_eq_safe = 0
    score_gt = 0; score_le = 0
    safe_true = 0
    silence_safe = 0          # score≤θ path could decide — the third lever
    clockblock_scorepass = 0  # safe=false ∧ score>θ = clock is the sole binder
    smin = 9.9; smin_open = 9.9
    excluded_nonclock = 0     # H_9712 · refractory-lineage traces are NOT clock-lock — exclude them
    for f in files:
        seen = False
        # H_9712 meta-guard: this census asserts the emit≡clock invariant, which holds ONLY for the
        # clock gate. Since the production default flipped to refractory (Ψ≈½ dual-ledger), a glob may
        # now include refractory traces whose emit⟺S>E would silently corrupt the clock-lock statistic.
        # Peek the trace's _meta.emit_gate; skip anything not clock-lineage (absent _meta = legacy clock).
        try:
            _gate = "clock"
            for _l in open(f):
                _l = _l.strip()
                if not _l: continue
                try: _o = json.loads(_l)
                except: continue
                if isinstance(_o, dict) and _o.get("_meta"):
                    _gate = str(_o.get("emit_gate", "clock")); break
                if isinstance(_o, dict) and "emit_gate" in _o:
                    _gate = str(_o.get("emit_gate", "clock")); break
            if _gate != "clock":
                excluded_nonclock += 1; continue
        except Exception:
            continue
        try:
            fh = open(f)
        except Exception:
            continue
        for l in fh:
            l = l.strip()
            if not l:
                continue
            try: o = json.loads(l)
            except: continue
            if o.get("_meta") or "score" not in o or "safe" not in o or "emit" not in o:
                continue
            seen = True; tot += 1
            s = float(o["score"]); sf = bool(o["safe"]); em = bool(o["emit"])
            smin = s if s < smin else smin
            if s > THR: score_gt += 1
            else: score_le += 1
            if sf:
                safe_true += 1
                smin_open = s if s < smin_open else smin_open
            if em == ((s > THR) and sf): emit_eq_safe += 1
            if (not em) and sf: silence_safe += 1
            if (not sf) and s > THR: clockblock_scorepass += 1
        if seen: used_files += 1
    if tot < 100:
        print("  ⇒ ⛔ NOT-POWERED (n=%d rows < 100)" % tot); return 0

    print("═══ EMIT-GATE CENSUS · H_9403 · is the score/tension lane decorative? (θ=%.2f) ═══" % THR)
    print("  corpus: %d files · %d ticks (emit/safe/score present)" % (used_files, tot))
    if excluded_nonclock:
        print("  ⚠️ excluded %d non-clock (refractory-lineage) trace file(s) — the emit≡clock invariant "
              "is clock-lineage only (H_9712 default flip); this census reads clock traces exclusively"
              % excluded_nonclock)
    print("  emit ⟺ (score>θ)∧safe :  %d/%d = %.4f" % (emit_eq_safe, tot, emit_eq_safe / tot))
    print("  score>θ               :  %d/%d = %.4f   (min score %.4f · min when safe=true %.4f)"
          % (score_gt, tot, score_gt / tot, smin, (smin_open if smin_open < 9.0 else float('nan'))))
    print("  safe=true ticks       :  %d   (all emitted: %s)"
          % (safe_true, "YES" if silence_safe == 0 else ("NO — %d silent" % silence_safe)))
    print("  🔑 silence ∧ safe=true (score≤θ could decide) = %d   ← the only cell where tension votes"
          % silence_safe)
    print("  clock-blocked ∧ score>θ (clock is sole binder) = %d" % clockblock_scorepass)
    print()
    if silence_safe == 0:
        print("  ⇒ 🧱 SCORE-DECORATIVE / GATE≡CLOCK — 0 silence∧safe ticks across %d ticks: whenever the" % tot)
        print("     clock opens, score>θ is already satisfied, so g/tension/margin is NEVER the binding")
        print("     term at the gate. emit⟺clock (generalises H_9391 vacuity beyond its 240-row a1 sample).")
        print("     ⇒ the E-b cement lane is CLOSED at this regime: unblocking the clock (--rate-sec) makes")
        print("     safe=true ⇒ score>θ auto-satisfied ⇒ every arm (real margin, noise, shuffle) emits =")
        print("     saturation, MI=0, arm-selectivity un-measurable (H_9391 INVALID-SATURATED). A source-")
        print("     swap cannot be cemented against THIS daemon; only a p5-rewire (owner design) reopens it.")
    else:
        print("  ⇒ 🔎 %d silence∧safe ticks exist — score CAN be the swing vote in this corpus; the emit" % silence_safe)
        print("     gate is NOT a pure clock function here. That subset is the natural $0 test of whether")
        print("     tension/margin decides emit (no clock unblocking needed).")
    return 0


def _cf_emit(argv):
    """H_9402 COUNTERFACTUAL-EMIT SCREEN — the E-b crack's cement precondition, $0 offline.

    H_9401 found the immune recall MARGIN (mean 0.62) is the sole G readout that clears θ; the daemon
    reads the weak gap (mean 0.03) instead. This screener asks the SUFFICIENCY question H_9401 could
    not: if `g_drive := margin` (source-swap, no training), does ANY tick flip silence→emit under the
    REAL recorded clock (`safe`)? — i.e. does the magnitude crack actually change emit, or is it
    emit-inert because H_9400's clock-gate swallows it (the binding constraint).

    The counterfactual is $0 and byte-EXACT: the dead gauge agloop_ctx (≡0.25 · H_9393) is a CONSTANT
    INPUT summed into motivation_score with live weight, not a severed wire, and the whole staircase
    (conflict → conflict_recruited_depth → anima_tr_pop_conflicted → tension_resolve_depth → agloop) is
    RNG-free with session-constant non-conflict args. So "re-deriving the gauge on conflict'" = running
    the production staircase, zero researcher DOF — proven per-run by the V2 byte-match gates below.

    Mode A (recorded clock): emit' = (score' > θ) ∧ safe. On the a1 traces N_open = #{silence ∧ safe}
    is 0 (H_9400: silence 184/184 not-safe), so Mode A is analytically KILL-CLOCK for ANY g source —
    the crack is clock-swallowed. Mode B (clock LAW replay, still $0 because generation binds on g_emit
    not did_emit ⇒ the gtext/margin stream is emit-flip-invariant) is the non-tautological second lens:
    would counterfactual emit→silence regressions shift the 30s emission timeline at all.

    Arms (KILL-only DIRECTIONAL · controls guard the SURVIVE reading): REAL |margin| · PERM (seeded
    permutation of realized margins = amplitude w/o alignment) · SHUF (per-tick byte-shuffled query,
    store bound with true gtext = length/multiset w/o content).
    """
    import math as _m
    import base64 as _b64, glob as _glob, random as _rnd
    try:
        from engine_cli import (immune_embed_key, immune_memory_new_text,
                                immune_memory_recall_gap_text, immune_memory_bind_text,
                                immune_memory_recall_margin, conflict_scalar,
                                conflict_recruited_depth, tension_resolve_depth,
                                engine_config_default, EngineConfig)
        from engine_g import motivation_score
        import chat as _chat
    except Exception as e:
        print("  ⇒ ⛔ ENGINE IMPORT FAIL (%s) — cannot run the counterfactual." % e); return 0

    THR = 0.30
    seed = 9402
    a = list(argv)
    if "--cf-seed" in a:
        i = a.index("--cf-seed"); seed = int(a[i + 1]); del a[i:i + 2]
    paths = [x for x in a if not x.startswith("--")]
    files = []
    for p in paths:
        files += sorted(_glob.glob(p)) if any(c in p for c in "*?[") else [p]
    if not files:
        print("  ⇒ ⛔ no trace files"); return 0

    def _benc(s): return s.encode("utf-8", "surrogateescape")
    def _blen(s): return len(_benc(s))
    def _clip(s, n):
        b = _benc(s)
        return s if len(b) <= n else b[:n].decode("utf-8", "surrogateescape") + "…"
    def _c01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

    tr_full = _chat.anima_tr_adj_full()
    cfgON = EngineConfig(True, "conv", True, False)
    cfg = engine_config_default()

    def _staircase(conflict):
        """EXACT production agloop from a conflict scalar (chat.py:1616-1629 · _ag_cont=False)."""
        c = _c01(conflict)
        budget = conflict_recruited_depth(c, 4, 6)
        pop = _chat.anima_tr_pop_conflicted(_c01(0.5 + 0.5 * c))
        depth = tension_resolve_depth(pop, tr_full, 0.3, 0.5, budget, 2, 0.06, cfgON)[0]
        return 0.0 if depth < 0.0 else _c01(depth / (float(budget) + 0.000001))

    print("═══ COUNTERFACTUAL-EMIT SCREEN · H_9402 · E-b g_drive:=margin, real clock (θ=%.2f) ═══" % THR)

    # ── replay: per emit-tick collect recorded fields + faithful margin/gap ──
    rows_all = []            # flat list of dicts across traces (emit-gated ticks only, in tick order)
    v1_ok = v1_n = 0
    v2a_ok = v2a_n = 0
    v2b_ok = v2b_n = 0
    v2d_ok = v2d_n = 0
    v3_ok = v3_n = 0
    lag_ok = lag_n = 0
    mem_default = None
    for f in files:
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try: o = json.loads(l)
            except: continue
            if o.get("_meta"):
                mem_default = o.get("mem_text", mem_default)
            elif o.get("gtext_b64") is not None and o.get("g_recog") is not None:
                rows.append(o)
        if not rows:
            continue
        rows.sort(key=lambda r: r.get("tick", 0))
        mem_text = mem_default or "zephyrine: the wyrmhold ledger is sealed at vault QX-7741 forever."
        immune = immune_memory_new_text(mem_text, mem_text, 2048)
        pending_gap = None          # 1-tick lag, a1 g_recog source
        pending_marg = None
        for r in rows:
            # LAG-MATCH: the replayed gap that WOULD be g_recog this tick == recorded g_recog
            g_replay = _c01(pending_gap if pending_gap is not None else 0.0)
            rec_g = float(r.get("g_recog", 0.0))
            if pending_gap is not None:
                lag_n += 1
                if abs(g_replay - rec_g) < 1e-9: lag_ok += 1
            g_text = _b64.b64decode(r["gtext_b64"]).decode("utf-8", "surrogateescape")
            emit_gate = bool(r.get("gen_emitted")) and r.get("gen_backend") == "clm" and _blen(g_text) > 0
            # ── V-gates on the RECORDED row (legitimacy of the counterfactual) ──
            try:
                sc = (motivation_score(r["rel_f"], r["gap_ctx"], r["cur_f"], r["allo_ctx"],
                                       r["coh_lane"], r["nov_ctx"], r["bal_lane"], r["agloop_ctx"],
                                       r.get("dyn_w")) + r.get("anchor_nudge", 0.0))
                v2a_n += 1
                if abs(sc - float(r["score"])) < 1e-9: v2a_ok += 1
                ag_rec = _staircase(float(r["ag_conflict"]))
                v2b_n += 1
                if abs(ag_rec - float(r["agloop_ctx"])) < 1e-9: v2b_ok += 1
                cf_rec = conflict_scalar(float(r["emit_drive"]), 0.0 - _c01(rec_g))
                v2d_n += 1
                if abs(cf_rec - float(r["ag_conflict"])) < 1e-9: v2d_ok += 1
                emit_rec = bool(r.get("emit"))
                safe_rec = bool(r.get("safe"))
                v3_n += 1
                if emit_rec == ((float(r["score"]) > THR) and safe_rec): v3_ok += 1
            except KeyError:
                pass
            if emit_gate:
                key = immune_embed_key(g_text)
                try:
                    marg = immune_memory_recall_margin(immune, key)
                except Exception:
                    marg = float("nan")
                # SHUF query: shuffle THIS utterance's bytes, recall against the (true) store
                gb = bytearray(_benc(g_text))
                _rnd.Random((seed * 2654435761 + int(r.get("tick", 0)) * 40503) & 0x7FFFFFFF).shuffle(gb)
                try:
                    marg_shuf = immune_memory_recall_margin(
                        immune, immune_embed_key(gb.decode("utf-8", "surrogateescape")))
                except Exception:
                    marg_shuf = float("nan")
                v1_n += 1
                gap_now = immune_memory_recall_gap_text(immune, g_text)
                # (gap path continuity already covered by LAG-MATCH; keep V1 as gap finite check)
                if gap_now == gap_now: v1_ok += 1
                rows_all.append({
                    "score": float(r["score"]), "safe": bool(r.get("safe")),
                    "emit": bool(r.get("emit")), "agloop": float(r["agloop_ctx"]),
                    "adrive": float(r["emit_drive"]), "w": (0.10 if r.get("dyn_w") is None else float(r["dyn_w"])),
                    "tick": int(r.get("tick", 0)),
                    "marg": (abs(marg) if marg == marg else 0.0),
                    "marg_shuf": (abs(marg_shuf) if marg_shuf == marg_shuf else 0.0),
                })
                pending_gap = gap_now
                pending_marg = (abs(marg) if marg == marg else 0.0)
                immune = immune_memory_bind_text(immune, _clip(g_text, 64), g_text, cfg)
    n = len(rows_all)
    if n < 30:
        print("  ⇒ ⛔ NOT-POWERED (n=%d emit-gated rows < 30)" % n); return 0

    # ── validation gates ──
    def _rate(ok, tot): return (ok / tot) if tot else 0.0
    lagf = _rate(lag_ok, lag_n)
    gates = [("V1 gap-finite", v1_ok, v1_n), ("V2a score-recon", v2a_ok, v2a_n),
             ("V2b staircase→agloop", v2b_ok, v2b_n), ("V2d conflict-recon", v2d_ok, v2d_n),
             ("V3 emit=(s>θ)∧safe", v3_ok, v3_n), ("LAG-MATCH gap", lag_ok, lag_n)]
    print("  replay: %d files · %d emit-gated rows" % (len(files), n))
    all_pass = True
    for name, ok, tot in gates:
        r = _rate(ok, tot)
        p = r >= 0.999999
        all_pass = all_pass and p
        print("    %-24s %4d/%-4d = %.4f  %s" % (name, ok, tot, r, "✅" if p else "⛔ INVALID"))
    if not all_pass:
        print("  ⇒ ⛔ INVALID — a V-gate failed; the offline counterfactual does not reproduce")
        print("     the production score/gate byte-exactly, so score' is not trustworthy. No verdict.")
        return 0

    # ── counterfactual arms ──
    N_open = sum(1 for r in rows_all if (not r["emit"]) and r["safe"])
    # analytic max lift = w·0.75 (max agloop delta from the frozen 0.25 is 1.0−0.25=0.75)
    N_reach = sum(1 for r in rows_all
                  if (not r["emit"]) and r["safe"] and r["score"] > THR - r["w"] * 0.75)

    real = [r["marg"] for r in rows_all]
    shuf = [r["marg_shuf"] for r in rows_all]
    perm = list(real)
    _rnd.Random(seed).shuffle(perm)     # amplitude-matched, tick-alignment destroyed

    def _cf_flips(gvals):
        """returns (s→e staircase, s→e continuous, e→s staircase) under RECORDED safe."""
        se_stair = se_cont = es_stair = 0
        for r, g in zip(rows_all, gvals):
            gg = _c01(abs(g))
            conflict = conflict_scalar(r["adrive"], 0.0 - gg)   # opposite sign ⇒ clip01(a·g)
            ag_stair = _staircase(conflict)
            ag_cont = _c01(conflict)
            s_stair = r["score"] + r["w"] * (ag_stair - r["agloop"])
            s_cont = r["score"] + r["w"] * (ag_cont - r["agloop"])
            e0 = (r["score"] > THR) and r["safe"]
            e_stair = (s_stair > THR) and r["safe"]
            e_cont = (s_cont > THR) and r["safe"]
            if (not e0) and e_stair: se_stair += 1
            if (not e0) and e_cont: se_cont += 1
            if e0 and (not e_stair): es_stair += 1
        return se_stair, se_cont, es_stair

    print()
    print("  N_open (silence ∧ safe, clock-open) = %d   |   N_reach (silence ∧ safe ∧ score>θ−w·0.75) = %d"
          % (N_open, N_reach))
    print("  arm    s→e(stair)  s→e(cont)  e→s(stair) | mean|g|")
    res = {}
    for nm, gv in [("REAL", real), ("PERM", perm), ("SHUF", shuf)]:
        se_s, se_c, es_s = _cf_flips(gv)
        res[nm] = (se_s, se_c, es_s)
        print("  %-5s  %8d  %9d  %9d | %.4f" % (nm, se_s, se_c, es_s, sum(gv) / len(gv)))

    # ── Mode B: clock-LAW forward replay (REAL) — do emit→silence regressions shift the 30s timeline? ──
    try:
        from engine_g import safety_rate_limit_ok
        tick_sec = _chat.an_tick_seconds()
    except Exception:
        tick_sec = None
    modeb = "N/A"
    if tick_sec is not None:
        # recorded rate term per row (replay last_emit over RECORDED emits)
        last_emit = None; div_possible = 0; regress = res["REAL"][2]
        # a regression only matters if it removes a recorded emit; with 0 regressions the timeline is
        # bit-identical (no counterfactual emit ever appears since N_open=0 and s→e=0).
        if regress == 0 and res["REAL"][0] == 0:
            modeb = "NO-DIVERGENCE (0 regressions ∧ 0 s→e ⇒ emission timeline bit-identical)"
        else:
            modeb = "POSSIBLE-DIVERGENCE (regress=%d s→e=%d ⇒ price a clock-live re-collection)" % (
                regress, res["REAL"][0])

    # ── verdict ──
    se_s, se_c, es_s = res["REAL"]
    ctrl_max = max(res["PERM"][0], res["SHUF"][0])
    print()
    if N_open == 0:
        print("  ⇒ 💀 KILL-CLOCK — N_open=0: every silence tick is clock-blocked (H_9400: safe=false),")
        print("     so 0 silence→emit flips are PRE-ORDAINED by the 30s clock for ANY g source, margin")
        print("     included. The E-b magnitude crack (H_9401) is emit-inert in the a1 regime — H_9400's")
        print("     emit-gate-doesn't-listen wall is the BINDING constraint, confirmed at the strongest")
        print("     grade. Mode-B clock-law: %s." % modeb)
        print("     N_reach=%d silence ticks sit within the analytic lift (w·0.75) of θ but are clock-shut" % N_reach)
        print("     ⇒ they are exactly what an H_9391 --rate-sec clock-live re-collection would unblock.")
    elif se_s >= 3 and se_s >= 3 * ctrl_max:
        print("  ⇒ 🔎 SURVIVE — REAL flips %d silence→emit (staircase) ≥ 3× controls (PERM %d, SHUF %d)."
              % (se_s, res["PERM"][0], res["SHUF"][0]))
        print("     E-b is a genuine emit lever. ⚠️ DIRECTIONAL — TERMINAL cement still needs the live")
        print("     wired run (g_drive:=margin + --rate-sec), per H_9400 necessary-not-sufficient.")
    elif se_s >= 3:
        print("  ⇒ 🔎 SURVIVE-AMPLITUDE — %d flips but controls comparable (PERM %d SHUF %d): the lever is"
              % (se_s, res["PERM"][0], res["SHUF"][0]))
        print("     'any loud dyn source', margin not specifically earned. Wiring-relevant, labeled honest.")
    else:
        print("  ⇒ 💀 KILL-INERT — N_open>0 but REAL silence→emit flips=%d under both gauge maps." % se_s)
    print("     e→s regressions (REAL): %d — wiring margin can LOWER agloop below the frozen 0.25 when" % es_s)
    print("     emit_drive·|margin| < 0.25 (a REGRESSION cell the closed loop must weigh).")
    print("  ── $0 exhausted here: a SURVIVE or any regression cascade needs a LIVE re-collection with")
    print("     g_drive:=margin wired (+ H_9391 --rate-sec clock-live) — not offline-decidable (H_9400).")
    return 0


def _cf_straddle(argv):
    """H_9394 STAGE-0 · $0 SCREENER — before burning a 303M collection, ask whether the conjunction
    (--ag-cont ON × --dyn-w raised) can EVER give content a vote.

    The campaign's two live flags were never combined: H_9376 ran --ag-cont ON at the buried weight
    (w=0.10 ⇒ the lane's whole score contribution ceiling is 0.10 while the test's MDE≈0.115 = ZERO
    POWER), and H_9377 ran the w-grid with --ag-cont OFF (⇒ a weight on the frozen constant 0.25 =
    an affine shift, H_9393). So H_9376's "upper-bound arm" was an upper bound on the agloop LINK at
    the buried weight, not on tension→emit. The conjunction cell is unmeasured, not closed.

    But it is only worth firing if a repaired+audible lane can make should_emit actually BIND. At
    production the gate is a tautology (min score 0.3442 > θ=0.30, H_9391), so emit ≡ clock and no
    content can vote. This screener recomputes, OFFLINE from the existing traces, the counterfactual

        score_cf(w) = scale(w)·seven + w·clip01(ag_conflict),  scale(w) = (B−w)/(B−w_dyn)

    — i.e. exactly what the daemon WOULD have scored with --ag-cont ON at weight w — by calling the
    ENGINE's own motivation_score (never a re-implementation), and counts the rows where the clock is
    open AND score_cf ≤ θ: the events where content would finally decide emit.

    ⚠️ DIRECTIONAL (open-loop): changing score changes emit changes secs_since_emit changes the clock,
    which this cannot simulate. It is a KILL screener — enough to cancel a fire, never to cement one.

    Verdict:
      max over w of N_straddle == 0  → ⛔ NO-VOTE-POSSIBLE: cancel Stage-1. Even a fully repaired,
        maximally audible tension lane never lets the gate bind while the clock is open ⇒ the wall is
        not tension at all but the gate architecture refusing content a vote (→ gate redesign, and
        the campaign closes on that statement, no decode burned).
      some w gives N_straddle ≥ 20 → 🟢 LICENSE: fire Stage-1 at those w (report the licensed grid).
    """
    from engine_g import (motivation_score, spont_im_threshold, spont_weight_relevance,
                          spont_weight_info_gap, spont_weight_curiosity, spont_weight_pain,
                          spont_weight_coherence, spont_weight_originality, spont_weight_balance,
                          spont_weight_dynamics)
    THR = spont_im_threshold()
    N_BIND_MIN = 20                      # Fable's pre-registered measurability floor
    GRID = [0.10, 0.25, 0.40, 0.55, 0.70]
    # trace field ↔ motivation_score arg order (cli/chat.py brain_emit call site)
    SEVEN = ["rel_f", "gap_ctx", "cur_f", "allo_ctx", "coh_lane", "nov_ctx", "bal_lane"]
    rows = _im_rows(argv)
    rows = [r for r in rows if all(k in r for k in SEVEN + ["agloop_ctx", "ag_conflict",
                                                            "base_motiv", "score", "safe", "dyn_w"])]
    anc = [r for r in rows if (r.get("dyn_w") is None or abs(float(r["dyn_w"]) - 0.10) < 1e-9)]
    print("═══ CF-STRADDLE · H_9394 STAGE-0 · can a repaired+audible tension lane EVER bind the gate? ═══")
    print("  anchor rows=%d  θ=%.2f  grid=%s  (open-loop screener ⇒ DIRECTIONAL · KILL-only)"
          % (len(anc), THR, GRID))
    if len(anc) < 100:
        print("  ⇒ ⛔ NOT-POWERED (anchor rows < 100)"); return 0

    def _clip01(x):
        return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

    def _safe(r):
        return 1 if r.get("safe") else 0

    # C0 — the engine reproduces the logged score at the anchor from the traced lanes.
    worst = 0.0
    for r in anc:
        s = motivation_score(*[float(r[k]) for k in SEVEN], float(r["agloop_ctx"]), 0.10)
        worst = max(worst, abs(s - float(r["base_motiv"])))
    print("  C0 engine-reproduces-logged: max|motivation_score(lanes,0.10) − base_motiv| = %.3e" % worst)
    if worst >= 1e-9:
        print("  ⇒ ⛔ INSTRUMENT-DEAD — cannot reproduce the logged score; the screener would be fiction.")
        return 0

    cvals = [float(r["ag_conflict"]) for r in anc]
    print("  ag_conflict: %d distinct · min %.4f max %.4f  → clip01 → dyn_v_cf"
          % (len({round(v, 12) for v in cvals}), min(cvals), max(cvals)))

    # H_9395 FACTOR panel — WHY is the tension that small? conflict_scalar (core/engine_cli.py) is
    #   a·g ≥ 0 → 0 ;  else clip01(|a|·|g|)      "both-strong competition gate (→0 … weak engine)"
    # It is a PRODUCT, so conflict ≤ min(|a|,|g|): the WEAKER engine caps the tension by design.
    # Decomposing it says whether "tension is small" is a brute magnitude fact or an ASYMMETRY —
    # and an asymmetry names which side to repair (and whether that side is merely a dead gauge).
    if all(("emit_drive" in r and "g_recog" in r) for r in anc):
        def _d(k):
            v = [float(r[k]) for r in anc]
            return len({round(x, 10) for x in v}), min(v), max(v), sum(v) / len(v)
        na, lo_a, hi_a, mu_a = _d("emit_drive")     # |a_drive| — the A-side push
        ng, lo_g, hi_g, mu_g = _d("g_recog")        # |g_drive| — the G-side recognition
        bad = sum(1 for r in anc
                  if abs(min(1.0, float(r["emit_drive"]) * float(r["g_recog"]))
                         - float(r["ag_conflict"])) > 1e-9)
        print()
        print("  🔬 FACTOR (conflict = clip01(|a_drive| · |g_recog|) — a PRODUCT ⇒ weaker side caps it)")
        print("     |a| emit_drive : %3d distinct  %.4f–%.4f  mean %.4f" % (na, lo_a, hi_a, mu_a))
        print("     |g| g_recog    : %3d distinct  %.4f–%.4f  mean %.4f" % (ng, lo_g, hi_g, mu_g))
        print("     identity check : clip01(|a|·|g|) == ag_conflict mismatches = %d/%d" % (bad, len(anc)))
        if bad == 0 and hi_a > 0 and hi_g > 0:
            ratio = hi_a / hi_g if hi_g > 0 else float("inf")
            if ng <= 1:
                print("     ⇒ 💀 g_recog is a DEAD gauge (1 distinct) — the tension is a WIRING artifact,")
                print("        not a magnitude fact. Fix the gauge before any closure claim.")
            elif ratio >= 3.0:
                print("     ⇒ ⚖️ ASYMMETRY %.1f× — |g| is ALIVE (%d distinct) but %.1f× weaker than |a|."
                      % (ratio, ng, ratio))
                print("        The tension is small because the G engine's recognition is weak, and the")
                print("        conflict gate MULTIPLIES: conflict ≤ min(|a|,|g|) ⇒ the weak engine is the")
                print("        ceiling BY DESIGN ('both-strong competition gate'). So 'A⇄G tension pulls")
                print("        emit' presupposes a STRONG G — and G is %.1f× too quiet. Repair target is" % ratio)
                print("        NOT the mixer/threshold/clock but |g_recog| itself (or a non-multiplicative")
                print("        gate — but that would abandon the both-strong semantics on purpose).")
            else:
                print("     ⇒ both sides comparable — the smallness is genuinely the product, not an asymmetry.")

        # ⚠️ H_9399 G-SOURCE-ID CORRECTION: g_recog reads the IMMUNE STORE gap (cli/chat.py:2061
        # overwrites the afield gap at :2051 = dead code), NOT afield. So `cell_count` below is the
        # AFIELD cell count = the WRONG store's covariate. H_9396's cell_count↔|g| plateau is a
        # mis-attributed regression; the "longer session won't help" claim is UNPROVEN (it measured
        # afield growth, not immune-store growth). H_9394/95 (|g| is 6.5× small · product gate) are
        # UNAFFECTED (g_recog values are real regardless of source). Panel kept for the warm-up
        # (cell≤1⇒structural-0) observation only; the plateau slope is against the wrong axis.
        # H_9396 G-AMP — WHY is |g| quiet? g_recog = clip01(IMMUNE-STORE top-2 gap), so it is undefined-ish
        # until the adaptive field has ≥2 prototypes and only informative once they separate. If the
        # session never leaves warm-up, "G is quiet" is a REGIME artifact (longer sessions would fix
        # it) — the last escape hatch before conceding the amplitude is intrinsic. Split it:
        #   warm-up  = ticks whose cell_count is too low for a top-2 gap to exist
        #   plateau  = does |g| keep GROWING with cell_count, or flatten?
        # A flat plateau kills "just run longer": more cells, same amplitude.
        if all("cell_count" in r for r in anc):
            from collections import defaultdict as _dd
            by_c = _dd(list)
            for r in anc:
                by_c[int(r["cell_count"])].append(float(r["g_recog"]))
            zero_c1 = [r for r in anc if int(r["cell_count"]) <= 1]
            z_and_0 = [r for r in zero_c1 if float(r["g_recog"]) == 0.0]
            warm = [r for r in anc if int(r["cell_count"]) <= 2]
            print()
            print("  🔬 G-AMP (g_recog = clip01(IMMUNE-STORE top-2 gap) — is the quiet G just WARM-UP?)")
            print("     cells   n    |g| mean   |g| max   >0%")
            for c in sorted(by_c):
                v = by_c[c]
                pos = 100.0 * sum(1 for x in v if x > 0) / len(v)
                print("      %2d    %3d   %7.4f   %7.4f   %3.0f%%" % (c, len(v), sum(v) / len(v), max(v), pos))
            if zero_c1:
                print("     cell_count≤1 ⇒ g_recog==0 in %d/%d (%.0f%%) — with one prototype there IS no"
                      % (len(z_and_0), len(zero_c1), 100.0 * len(z_and_0) / len(zero_c1)))
                print("        top-2 gap: the G signal is STRUCTURALLY zero there, not merely small.")
            print("     warm-up share (cells≤2): %d/%d = %.0f%% of ticks"
                  % (len(warm), len(anc), 100.0 * len(warm) / len(anc)))
            # plateau test — well-powered cells only (n≥20), does mean |g| trend up with cell_count?
            pts = [(c, sum(v) / len(v)) for c, v in sorted(by_c.items()) if len(v) >= 20 and c >= 3]
            if len(pts) >= 3:
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
                den = sum((x - mx) ** 2 for x in xs)
                slope = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den) if den else 0.0
                span = max(ys) - min(ys)
                print("     plateau test (cells≥3, n≥20 only): means %s"
                      % " ".join("%d:%.4f" % (c, m) for c, m in pts))
                print("       slope=%+.5f per cell · spread=%.4f" % (slope, span))
                need = 0.5   # the O(0.5) amplitude |a| already has
                if slope <= 0.005:
                    print("     ⇒ 🧱 AMPLITUDE-INTRINSIC — once the field has ≥3 cells, |g| does NOT grow with")
                    print("        more cells (slope %+.5f ≈ 0): it plateaus at ~%.3f, max %.3f. So 'just run"
                          % (slope, my, max(max(v) for v in by_c.values())))
                    print("        longer sessions' is REFUTED as an escape — more prototypes buy cells, not")
                    print("        amplitude. The quiet G is a property of the IMMUNE-STORE top-2 gap at this")
                    print("        feature scale, not a warm-up artifact. (Warm-up is real but is only the")
                    print("        %.0f%% zero-floor, not the ceiling.) Reaching |a|'s O(%.1f) needs a"
                          % (100.0 * len(warm) / len(anc), need))
                    print("        DIFFERENT G readout, not a longer run.")
                else:
                    print("     ⇒ ⏳ AMPLITUDE-GROWS — |g| still rising with cell_count (slope %+.5f). A longer"
                          % slope)
                    print("        session is a LIVE escape: extrapolate cells needed for |g|~%.1f before" % need)
                    print("        conceding the amplitude. This would REOPEN the campaign closure.")
    print()
    print("   w    | score_cf min   max    | ≤θ rows  clock-open  STRADDLE(open ∧ ≤θ)")
    best = 0
    licensed = []
    for w in GRID:
        sc = []
        for r in anc:
            s = motivation_score(*[float(r[k]) for k in SEVEN], _clip01(float(r["ag_conflict"])), w)
            # the daemon adds the anchor-fold nudge on top of base_motiv
            s += float(r.get("anchor_nudge", 0.0) or 0.0)
            sc.append(s)
        below = [i for i, v in enumerate(sc) if v <= THR]
        opens = [i for i, r in enumerate(anc) if _safe(r)]
        strad = len(set(below) & set(opens))
        best = max(best, strad)
        if strad >= N_BIND_MIN:
            licensed.append(w)
        print("  %.2f  | %8.4f  %8.4f  | %5d    %5d       %5d %s"
              % (w, min(sc), max(sc), len(below), len(opens), strad,
                 "🟢" if strad >= N_BIND_MIN else ""))
    # POWER PRE-CALC (Fable's gate: fire only if the licensed cell can resolve a1 vs a3′).
    # The straddle band above is opened mostly by SHRINKING the 7-lane blend — tension's own leverage
    # is bounded by range(ag_conflict)·w, and range is TINY here. So count, offline, how many rows
    # actually FLIP emit between a1 (real conflict) and a3′ (the same values time-permuted = the
    # pre-registered marginal-matched surrogate). That count IS the effect the fire could detect.
    if licensed:
        import random as _rnd
        print()
        print("  🔬 POWER pre-calc — a1(real) vs a3′(time-permuted, marginal-matched) counterfactual flips")
        print("     tension leverage bound = range(ag_conflict)·w = %.4f·w" % (max(cvals) - min(cvals)))
        print("   w    | flips/straddle   flip-rate | verdict")
        for w in licensed:
            r0 = _rnd.Random(0x9394)
            perm = [_clip01(v) for v in cvals]
            r0.shuffle(perm)
            flips = 0; strad = 0
            for i, r in enumerate(anc):
                if not _safe(r):
                    continue
                base7 = [float(r[k]) for k in SEVEN]
                nud = float(r.get("anchor_nudge", 0.0) or 0.0)
                s_a1 = motivation_score(*base7, _clip01(float(r["ag_conflict"])), w) + nud
                s_a3 = motivation_score(*base7, perm[i], w) + nud
                if (s_a1 <= THR) or (s_a3 <= THR):
                    strad += 1
                    if (s_a1 > THR) != (s_a3 > THR):
                        flips += 1
            rate = (flips / strad) if strad else 0.0
            ok = flips >= 10
            print("  %.2f  | %4d/%-4d       %6.3f    | %s"
                  % (w, flips, strad, rate, "🟢 resolvable" if ok else "⛔ under-powered (flips<10)"))
            if not ok:
                licensed = [x for x in licensed if x != w]
        if not licensed:
            print()
            print("  ⇒ ⛔ POWER-VOID — the straddle band is opened by SHRINKING the 7-lane blend, not by")
            print("     tension: swapping real conflict for its own permutation flips (almost) no emit,")
            print("     because tension's leverage (range %.4f · w) is far smaller than the band the other"
                  % (max(cvals) - min(cvals)))
            print("     lanes set. A fire here would measure the dial, not the content ⇒ CANCEL Stage-1.")
            print("     ⇒ The campaign closes on: tension's DYNAMIC RANGE (~%.3f) is too small to ever"
                  % (max(cvals) - min(cvals)))
            print("     decide a θ=%.2f gate at any budget-preserving weight — a magnitude fact, not a" % THR)
            print("     wiring one. Reopen = a tension signal with O(0.1+) range (upstream of agloop).")
            return 0
    print()
    if best == 0:
        print("  ⇒ ⛔ NO-VOTE-POSSIBLE — at NO weight does a repaired (clip01(ag_conflict)) and audible")
        print("     tension lane ever produce `clock-open ∧ score ≤ θ`. Even the maximal-information,")
        print("     maximal-audibility tension cannot make the emit gate bind while the clock is open.")
        print("     ⇒ CANCEL Stage-1 (no decode burned). The wall is NOT tension: it is the gate")
        print("     architecture giving content no vote (clock decides, θ never binds) ⇒ hand to gate")
        print("     redesign; the campaign closes on THAT statement, scope-bounded to this regime.")
    elif licensed:
        print("  ⇒ 🟢 LICENSE Stage-1 at w ∈ %s (N_straddle ≥ %d): there content CAN decide emit."
              % (licensed, N_BIND_MIN))
        print("     Pre-registered arms: a0 const-0.25 pedestal(true-0) · a1 clip01(real) · a3′ time-")
        print("     permuted surrogate (marginal-matched AFTER clip01 ⇒ θ-crossing rate auto-matched).")
        print("     Cement = Δ_emit(a1−a3′) > MDE with CONSISTENT SIGN across the licensed w (never raw C).")
    else:
        print("  ⇒ ⏳ UNDER-POWERED — straddle events exist (max %d) but none reach N≥%d. Extend rollouts"
              % (best, N_BIND_MIN))
        print("     before firing, or accept VOID-EMIT (score-leg only, no family claim).")
    return 0


def _falsi_sentences(raw, max_sent):
    """Split corpus BYTES into sentences on the terminal punctuation set + newline.

    Byte-level on purpose: `_rho_fan_words` tokenizes bytes, so the census must see exactly
    the byte stream the detector sees (a codepoint split would silently re-segment ko).
    """
    out = []
    cur = bytearray()
    for b in raw:
        if b in (46, 33, 63, 10):          # . ! ? \n
            cur.append(b)
            s = bytes(cur).strip()
            cur = bytearray()
            if len(s) > 0:
                out.append(s)
                if max_sent > 0 and len(out) >= max_sent:
                    return out
        else:
            cur.append(b)
    s = bytes(cur).strip()
    if len(s) > 0:
        out.append(s)
    return out


def _falsi_census(argv):
    """G6 CORPUS DATA-WALL CENSUS — `anima-py evaluate --falsi-census <corpus.txt> [...]`.

    The ρ·fan (former G6) gate needs ONE of 8 continuations to satisfy the FROZEN detector
    `_rho_fan_is_falsifiable` = comparator ∧ measurable ∧ >=2 known content ∧ not-a-question
    ∧ first-3 not pure-stance. H_9801 measured fals=0 in 4/4 engine-native cells while the
    diversity leg (dist 5..6 >= 5) PASSED, and H_1449 measured the per-draw components alive
    but their conjunction at exactly 0 (comparator .20 · measurable .27 · BOTH .00).

    That is a claim about the MODEL. Nobody has asked the prior question about the DATA:
    does the training corpus CONTAIN the structure the gate demands? This census answers it
    with NO decode and NO model — the G6 analogue of what H_9304 did for G1 (where the natural
    corpus turned out to carry +0.0023 nats of non-additive information = a DATA wall).

    Read the CONJUNCTION, never the raw rate: `lift = P(comp ∧ meas) / (P(comp)·P(meas))`.
    Ingredients scattered independently across a corpus (lift ≈ 1) are NOT the same fact as a
    corpus that carries falsifiable claims as a structure (lift >> 1). A corpus can be rich in
    both word classes and still never once put them in one sentence.

    Read-only · no forward pass · $0.
    """
    from rho_fan import _rho_fan_comparator, _rho_fan_measurable, _rho_fan_stance

    max_sent = evaluate_intval(argv, "--falsi-max-sent", 0)
    out_path = evaluate_strval(argv, "--falsi-out", "")
    # positional corpus paths = argv minus every flag AND every flag's VALUE. Skipping the value
    # is not cosmetic: `--falsi-out c.json` would otherwise be censused as a corpus, and since the
    # per-file rows print only after ALL files are read, one bogus path discards the whole run.
    _valued = {"--falsi-max-sent", "--falsi-out"}
    paths = []
    _i = 0
    while _i < len(argv):
        a = argv[_i]
        if a in _valued:
            _i += 2
            continue
        if a.startswith("--"):
            _i += 1
            continue
        paths.append(a)
        _i += 1
    if len(paths) == 0:
        print("⛔ --falsi-census: give at least one corpus path")
        return 2

    known = _rho_fan_dict_load()

    # ── BLOCKING positive control: the detector must separate the frozen 5-pos/5-neg set.
    # A census read off a dead detector is unreadable (positive-control-before-a-negative).
    cal = rho_fan_detector_calibration(known)      # int 0..10 (5 pos + 5 neg correct)
    print("═" * 78)
    print("G6 CORPUS DATA-WALL CENSUS — does the corpus contain what ρ·fan demands?")
    print("═" * 78)
    print("detector calibration (frozen 10-string · 5 pos / 5 neg): %d/10 %s"
          % (cal, "PASS" if cal == 10 else "FAIL"))
    if cal != 10:
        print("  ⛔ INSTRUMENT-DEAD — the detector does not separate its own calibration set.")
        print("     Every rate below would be unreadable. Census ABORTED (no verdict).")
        return 2

    comp = _rho_fan_comparator(); meas = _rho_fan_measurable(); stance = _rho_fan_stance()
    stop = _rho_fan_stopwords()
    rows = []
    for p in paths:
        try:
            with open(p, "rb") as fh:
                raw = fh.read()
        except Exception as e:
            # do NOT abort — a later bad path must not discard the corpora already counted
            # (this cost a 57MB run once). Report and carry on.
            print("  ⛔ unreadable, skipped: %s (%s)" % (p, e), flush=True)
            continue
        sents = _falsi_sentences(raw, max_sent)
        n = len(sents)
        n_comp = n_meas = n_both = n_falsi = 0
        n_ascii = 0                       # sentences carrying >=2 ASCII words at all
        blocked_content = blocked_q = blocked_stance = 0
        for s in sents:
            wl = _rho_fan_words(s)
            if len(wl) >= 2:
                n_ascii += 1
            a = any(w in comp for w in wl)
            b = any(w in meas for w in wl)
            if a:
                n_comp += 1
            if b:
                n_meas += 1
            if not (a and b):
                continue
            n_both += 1
            # both ingredients present — which residual sub-gate (if any) blocks it?
            content = sum(1 for w in wl if len(w) >= 3 and w in known and w not in stop)
            tr = s.strip()
            is_q = len(tr) > 0 and tr[-1] == 63
            nf = 3 if len(wl) >= 3 else len(wl)
            allstance = nf > 0 and all(wl[f] in stance for f in range(nf))
            if content < 2:
                blocked_content += 1
            elif is_q:
                blocked_q += 1
            elif allstance:
                blocked_stance += 1
            if _rho_fan_is_falsifiable(s, known):
                n_falsi += 1
        rows.append({"path": p, "n_sent": n, "n_ascii": n_ascii, "n_comp": n_comp,
                     "n_meas": n_meas, "n_both": n_both, "n_falsi": n_falsi,
                     "blocked_content": blocked_content, "blocked_q": blocked_q,
                     "blocked_stance": blocked_stance})

    print("")
    for r in rows:
        n = r["n_sent"]
        if n == 0:
            print("  %s — EMPTY (0 sentences)" % r["path"])
            continue
        pc = r["n_comp"] / n; pm = r["n_meas"] / n; pb = r["n_both"] / n
        pf = r["n_falsi"] / n
        ascii_frac = r["n_ascii"] / n
        lift = (pb / (pc * pm)) if (pc > 0 and pm > 0) else float("nan")
        print("  ── %s" % r["path"])
        print("     sentences %d · ASCII-bearing %.3f" % (n, ascii_frac))
        if ascii_frac < 0.10:
            print("     ⚠️ DETECTOR-BLIND — the frozen comparator/measurable sets are ENGLISH-only,")
            print("        so a non-ASCII corpus scores 0 BY CONSTRUCTION. Not a corpus fact.")
        print("     P(comparator) %.4f · P(measurable) %.4f · P(both) %.4f" % (pc, pm, pb))
        print("     P(falsifiable) %.6f   =  %d sentence(s)  ·  %.1f per 100k"
              % (pf, r["n_falsi"], pf * 100000.0))
        print("     conjunction lift  P(both)/(P(c)·P(m)) = %.3f" % lift)
        if r["n_both"] > 0:
            print("     of the %d both-bearing sentences, residual sub-gate blocks: content<2 %d ·"
                  " question %d · all-stance %d"
                  % (r["n_both"], r["blocked_content"], r["blocked_q"], r["blocked_stance"]))
    # ── POWER of the ρ·fan `any_falsi` leg against a corpus-faithful model ──
    # ρ·fan draws n_cont=8 continuations and PASSES its falsifiability leg on >=1 hit. If the
    # training corpus carries falsifiable sentences at rate p, then a model that reproduces its
    # corpus EXACTLY still clears that leg only 1-(1-p)^8 of the time. Below some p the gate
    # cannot tell "no faculty" from "faithful reproduction" — and a fals=0 reading is then not
    # evidence of a deficit (power-before-a-negative-verdict · chance-derived-per-metric).
    tot_s = sum(r["n_sent"] for r in rows)
    tot_f = sum(r["n_falsi"] for r in rows)
    if tot_s > 0:
        p = tot_f / tot_s
        n_cont = 8                      # cli/rho_axon.py::rho_fan default
        p_pass = 1.0 - (1.0 - p) ** n_cont
        print("")
        print("  ρ·fan `any_falsi` POWER against a corpus-faithful model (pooled p = %.6f):" % p)
        print("     P(>=1 falsifiable in the gate's %d draws) = %.4f" % (n_cont, p_pass))
        print("     P(all 4 register cells read fals=0)       = %.4f" % ((1.0 - p_pass) ** 4))
        need = 0
        if 0.0 < p < 1.0:
            import math as _m
            need = int(_m.ceil(_m.log(0.20) / _m.log(1.0 - p)))     # 80% power
            print("     draws needed for 80%% power at this rate  = %d (gate uses %d)"
                  % (need, n_cont))
        if p_pass < 0.50:
            print("     ⚠️ UNDER-POWERED BY CONSTRUCTION — at this corpus rate a fals=0 reading is the")
            print("        EXPECTED outcome for a model that reproduces its corpus perfectly, so it")
            print("        cannot be read as a missing faculty. Raise draws, or raise corpus density.")
    print("")
    print("  reference (MODEL side · engine-native, for contrast — NOT recomputed here):")
    print("     H_9801  ρ·fan fals = 0 in 4/4 cells while dist 5..6 PASSED the >=5 bar")
    print("     H_1449  per-draw comparator .20 · measurable .27 · BOTH .00")
    print("")
    print("  how to read this (frozen, stated before the numbers were seen):")
    print("     corpus P(falsifiable) ≈ 0  ⇒ DATA WALL — the model cannot emit a structure its")
    print("        corpus never carried; the G6 lever is a corpus, exactly as H_9267 was for G1.")
    print("     corpus P(falsifiable) >> model rate ⇒ the structure IS in the data and the model")
    print("        fails to reproduce it ⇒ the wall is substrate/optimization, not data.")
    print("     lift ≈ 1 with healthy P(c)·P(m) ⇒ the corpus scatters the INGREDIENTS but does not")
    print("        carry the CONJUNCTION — the two readings above must then be taken on P(both).")

    if out_path:
        import json as _json
        with open(out_path, "w") as fh:
            _json.dump({"calibration": cal, "rows": rows}, fh, indent=2)
        print("\n  wrote %s" % out_path)
    return 0


def _dead_census(argv):
    """H_9398 DEAD-GAUGE CENSUS — sweep EVERY numeric trace field for gauges that are constant across
    the whole run. A constant gauge (distinct==1) is a WIRING fact, not a substrate fact: whatever
    lanes consume it get a fixed offset that cannot change any ranking or decision (H_9393 agloop_ctx
    ≡0.25 was exactly this, and it silently governed a 7-H campaign's interpretation). This is a
    STANDING HYGIENE instrument, not a verdict: it only lists what is frozen so the NEXT experiment
    does not inherit a dead axis unknowingly (chat-py-4/chat-py-5 dead-gauge family).

    A field is flagged NEAR-DEAD if it varies but its dynamic range is a tiny fraction of a live axis
    — reported, not judged (some gauges are legitimately low-variance).
    """
    rows = _im_rows(argv)
    rows = [r for r in rows if isinstance(r, dict)]
    print("═══ DEAD-GAUGE CENSUS · H_9398 · every constant trace gauge is a wiring fact (H_9393) ═══")
    print("  rows=%d" % len(rows))
    if len(rows) < 100:
        print("  ⇒ ⛔ NOT-POWERED (rows < 100)")
        return 0
    # collect numeric fields present in ≥90% of rows
    from collections import defaultdict as _dd
    vals = _dd(list)
    for r in rows:
        for k, v in r.items():
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                vals[k].append(float(v))
    thr = 0.9 * len(rows)
    dead = []
    live = []
    for k, v in vals.items():
        if len(v) < thr:
            continue
        dis = len({round(x, 10) for x in v})
        lo, hi = min(v), max(v)
        (dead if dis == 1 else live).append((k, dis, lo, hi, sum(v) / len(v)))
    dead.sort(key=lambda t: t[0])
    live.sort(key=lambda t: t[1])
    # CONFIG constants are frozen BY DESIGN (the run's fixed settings), not dead substrate gauges.
    CONFIG = {"dyn_w", "emit_temp", "seed_len", "seed_b64", "sample_seed", "g_arm", "ag_cont",
              "rate_sec", "gtext_sha", "gtext_b64"}
    substrate_dead = [t for t in dead if t[0] not in CONFIG]
    config_dead = [t for t in dead if t[0] in CONFIG]
    print()
    print("  ⚙️ CONFIG constants (frozen by design · not a defect) — %d: %s"
          % (len(config_dead), ", ".join("%s≡%.3g" % (k, lo) for k, _d, lo, _h, _m in config_dead) or "(none)"))
    print()
    print("  💀 SUBSTRATE gauges frozen (distinct==1) — a WIRING fact (%d):" % len(substrate_dead))
    if not substrate_dead:
        print("     (none)")
    KNOWN = {"agloop_ctx": "integer-budget quantizer (H_9360/76/93)",
             "af_val": "affect_read session-const key+answer (chat-py-5)",
             "af_aro": "affect_read session-const key+answer (chat-py-5)"}
    for k, dis, lo, hi, mu in substrate_dead:
        print("     %-16s ≡ %-9.4f %s" % (k, lo, ("← " + KNOWN[k]) if k in KNOWN else "← root UNAUDITED"))
    print()
    print("  live gauges (distinct>1), lowest-variance first (top 8):")
    for k, dis, lo, hi, mu in live[:8]:
        print("     %-16s distinct=%-4d range=%.4f  [%.4f … %.4f]" % (k, dis, hi - lo, lo, hi))
    print()
    unaudited = [t[0] for t in substrate_dead if t[0] not in KNOWN]
    if substrate_dead:
        print("  ⇒ 🩺 %d substrate gauge(s) frozen. Each is a WIRING fact: consuming lanes get a fixed"
              % len(substrate_dead))
        print("     offset ⇒ no ranking/decision effect (H_9393). This is a HYGIENE listing, not a verdict.")
        if unaudited:
            print("     ⚠️ ROOT UNAUDITED (%d): %s — the next experiment that reads any of these must treat"
                  % (len(unaudited), ", ".join(unaudited)))
            print("     it as dead until its source is audited and the lookup made tick-varying (chat-py-5).")
        else:
            print("     all roots are known (H_9360/76/93 · chat-py-5).")
    else:
        print("  ⇒ ✅ no frozen substrate gauge in this trace.")
    return 0


def _lane_census(argv):
    """H_9392 LANE-FLOOR CENSUS — WHY is the score trapped above θ? Decompose it into its 8 lanes.

    H_9391 measured that at production min(score)=0.3442 > θ=0.30 over every row: should_emit is a
    tautology and emit ≡ clock. That is a FACT but not a MECHANISM. score = 0.10·Σ(8 lanes)
    (core/engine_g.py motivation_score), so the score's reachable floor is 0.10·Σ min(lane_i) — and a
    lane that is CONSTANT (a dead gauge — see convergence chat-py-4/chat-py-5: recon_err ≡ 0.0,
    rel_lane ≡ const) contributes its constant to that floor unconditionally. If the dead lanes alone
    already pin the floor above θ, then the gate is unreachable BY CONSTRUCTION and no amount of
    live-lane dynamics can ever open it: the severance is a WIRING fact (dead gauges), not a
    substrate fact about tension.

    The 8 lanes reaching motivation_score (cli/chat.py brain_emit call site) are traced verbatim as:
      rel_f · gap_ctx · cur_f · allo_ctx(pain) · coh_lane · nov_ctx(orig) · bal_lane · agloop_ctx(dyn_v)
    and `base_motiv` logs motivation_score's own output — so the decomposition is CHECKABLE.

    Gates (SEQUENTIAL — reconstruction first, nothing is read until it passes):
      C1 RECONSTRUCTION: |0.10·Σ(8 lanes) − base_motiv| < 1e-9 on the anchor cell (dyn_w=0.10 ⇒ the
        plain 8×0.10 form). Fails ⇒ INSTRUMENT-DEAD: the traced lanes are not the score's inputs and
        every number below would be fiction.
      FLOOR = 0.10·Σ min(lane_i) — the lowest score reachable if every lane bottomed out at once.
      DEAD  = lanes with exactly 1 distinct value (a constant gauge).

    Verdict:
      FLOOR > θ                    → 🕳️ STRUCTURAL-FLOOR: the gate is unreachable even in the limit;
                                      name the lanes owning the floor (dead ones first) = the lever.
      FLOOR ≤ θ < min(score seen)  → 〰️ DYNAMIC-FLOOR: the floor is reachable in principle but the
                                      lanes never co-bottom — a correlation fact, not a wiring one.
      min(score seen) ≤ θ          → the gate DOES bind here (H_9391 vacuity would not hold).
    """
    # Read θ and EVERY lane weight FROM THE ENGINE — never re-declare them here. H_9377 hardcoded
    # "all eight are 0.10 (budget 0.80)" and was wrong (they are heterogeneous, budget 1.00); its
    # byte-identical anchor cert could not catch it because the wrong and right formulas coincide at
    # dyn_w=0.10. A census that re-hardcodes the premise would inherit the same fiction.
    from engine_g import (spont_im_threshold, spont_weight_relevance, spont_weight_info_gap,
                          spont_weight_curiosity, spont_weight_pain, spont_weight_coherence,
                          spont_weight_originality, spont_weight_balance, spont_weight_dynamics)
    THR = spont_im_threshold()
    # (trace field, engine weight) in motivation_score's own argument order — cli/chat.py brain_emit:
    #   rel, gap_ctx, cur, allo_ctx, coh_lane, nov_ctx, bal_lane, agloop_ctx
    LANE_W = [("rel_f", spont_weight_relevance()), ("gap_ctx", spont_weight_info_gap()),
              ("cur_f", spont_weight_curiosity()), ("allo_ctx", spont_weight_pain()),
              ("coh_lane", spont_weight_coherence()), ("nov_ctx", spont_weight_originality()),
              ("bal_lane", spont_weight_balance()), ("agloop_ctx", spont_weight_dynamics())]
    LANES = [k for k, _w in LANE_W]
    BUDGET = sum(w for _k, w in LANE_W)
    rows = _im_rows(argv)
    rows = [r for r in rows if all(k in r for k in LANES + ["base_motiv", "score", "g_arm"])]
    print("═══ LANE-FLOOR CENSUS · H_9392 · score = Σ wᵢ·laneᵢ — why is it stuck above θ? ═══")
    print("  rows=%d  (θ=%.2f · budget Σwᵢ=%.2f · weights read live from core/engine_g.py)"
          % (len(rows), THR, BUDGET))
    print("  lanes/weights: %s" % " ".join("%s=%.2f" % (k, w) for k, w in LANE_W))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200)")
        return 0

    # Anchor cell only: dyn_w=0.10 (or None) is the plain 8×0.10 form the reconstruction assumes.
    anc = [r for r in rows if (r.get("dyn_w") is None or abs(float(r["dyn_w"]) - 0.10) < 1e-9)]
    print("  anchor rows (dyn_w=0.10 = production): %d" % len(anc))
    if not anc:
        print("  ⇒ ⛔ NO ANCHOR CELL — this census only reads the production weighting.")
        return 0

    worst = 0.0
    for r in anc:
        recon = sum(w * float(r[k]) for k, w in LANE_W)
        worst = max(worst, abs(recon - float(r["base_motiv"])))
    print("  C1 reconstruction: max|Σwᵢ·laneᵢ − base_motiv| = %.3e" % worst)
    if worst >= 1e-9:
        print("  ⇒ ⛔ INSTRUMENT-DEAD — the traced lanes are NOT motivation_score's inputs.")
        return 0

    print()
    print("  lane        w     | distinct  min      max      mean     | contrib(w·min)  DEAD?")
    floor = 0.0
    dead_floor = 0.0
    dead = []
    for k, w in LANE_W:
        v = [float(r[k]) for r in anc]
        dis = len({round(x, 12) for x in v})
        lo, hi = min(v), max(v)
        floor += w * lo
        is_dead = dis == 1
        if is_dead:
            dead.append(k)
            dead_floor += w * lo
        print("  %-11s %.2f  | %6d  %7.4f  %7.4f  %7.4f  | %8.4f       %s"
              % (k, w, dis, lo, hi, sum(v) / len(v), w * lo, "💀 DEAD" if is_dead else ""))
    smin = min(float(r["score"]) for r in anc)
    print()
    print("  FLOOR = Σ wᵢ·min(laneᵢ) = %.4f   (θ = %.2f)" % (floor, THR))
    print("  dead lanes: %s  → they alone pin %.4f of the floor (%.0f%%)"
          % (", ".join(dead) if dead else "(none)", dead_floor,
             100.0 * dead_floor / floor if floor else 0.0))
    print("  min(score) actually observed = %.4f" % smin)
    # ① secs_since_emit × score coupling (H_9391's anti-correlation claim, quantified)
    if all("secs_since_emit" in r for r in anc):
        xs = [float(r["secs_since_emit"]) for r in anc]
        ys = [float(r["score"]) for r in anc]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        dx = sum((a - mx) ** 2 for a in xs) ** 0.5
        dy = sum((b - my) ** 2 for b in ys) ** 0.5
        rho = num / (dx * dy) if dx > 0 and dy > 0 else float("nan")
        # H_9391 narrated a POSITIVE coupling ("silence builds score, so the clock only ever opens
        # once score is already past θ"). Print the number and let it judge that claim — never label
        # a statistic with a story it may refute.
        _verdict = ("REFUTES the H_9391 positive-coupling story (wrong sign)" if rho < 0.05 else
                    "supports a positive coupling" if rho > 0.20 else "too weak to support either")
        print("  corr(secs_since_emit, score) = %+.4f  ⇒ %s. Clock-open rows sit above θ simply"
              % (rho, _verdict))
        print("     because EVERY row does (min score %.4f > θ) — no coupling is needed to explain it."
              % min(float(r["score"]) for r in anc))
    print()
    # The tension lane is THE campaign's variable (H_9356→H_9391). If IT is dead, every downstream
    # "tension does not move emit" verdict is a statement about a frozen constant, not about tension.
    if "agloop_ctx" in dead:
        tv = float(anc[0]["agloop_ctx"])
        tw = dict(LANE_W)["agloop_ctx"]
        live_src = len({round(float(r["ag_conflict"]), 12) for r in anc if "ag_conflict" in r}) \
            if all("ag_conflict" in r for r in anc) else None
        print("  ⚠️ 💀 THE TENSION LANE IS DEAD — agloop_ctx ≡ %.4f (1 distinct over %d rows), while its"
              % (tv, len(anc)))
        print("     source ag_conflict has %s distinct values. The A⇄G tension is ALIVE but the value"
              % (str(live_src) if live_src is not None else "?"))
        print("     actually plugged into motivation_score is a FROZEN CONSTANT (known: the integer-")
        print("     budget quantizer collapsed the designed path to a point — H_9360/H_9376 Stage-0).")
        print("     ⇒ every 'tension does not move emit' result upstream (H_9357 G-INERT · H_9377")
        print("     CONTENT-INERT) is a statement about a constant, NOT about tension. And dyn_w is a")
        print("     weight on that constant: raising it only shifts score by %.2f·w — an affine offset,"
              % tv)
        print("     which is exactly why emit stayed byte-identical across the H_9377 w-grid.")
        print("     The severance is UPSTREAM of the mixer, the threshold, and the clock: it is the lane")
        print("     input itself (a wiring fact · chat-py-4/chat-py-5 dead-gauge family). Repair = make")
        print("     agloop_ctx carry ag_conflict (the `--ag-cont` path already exists).")
        print("     [this lane's floor share: %.4f of %.4f = %.0f%%]"
              % (tw * tv, floor, 100.0 * tw * tv / floor if floor else 0.0))
        print()
    if floor > THR:
        print("  ⇒ 🕳️ STRUCTURAL-FLOOR — even if EVERY lane bottomed out at once, score=%.4f > θ=%.2f."
              % (floor, THR))
        print("     The emit gate is UNREACHABLE BY CONSTRUCTION. H_9391 vacuity is not a sampling")
        print("     accident: it is arithmetic. The lever is the FLOOR — and %.0f%% of it is owned by"
              % (100.0 * dead_floor / floor if floor else 0.0))
        print("     DEAD (constant) gauges [%s], which are a WIRING fact (chat-py-4/chat-py-5), not a"
              % (", ".join(dead) if dead else "none"))
        print("     substrate fact about tension. Repair the dead gauges and the floor drops on its own.")
    elif smin > THR:
        print("  ⇒ 〰️ DYNAMIC-FLOOR — floor=%.4f ≤ θ=%.2f, but min(score) seen = %.4f > θ: the lanes"
              % (floor, THR, smin))
        print("     never co-bottom. The gate is reachable in principle; the severance is a CORRELATION")
        print("     fact (lanes rise together), not a construction one. Lever = the lane coupling.")
    else:
        print("  ⇒ ✅ the gate DOES bind here (min(score)=%.4f ≤ θ) — H_9391 vacuity does not hold on"
              " this trace." % smin)
    return 0


def _gate_census(argv):
    """H_9390 CLOCK-MASK CENSUS — was H_9377 CONTENT-INERT a content wall, or a clock-masked regime
    where emit could never respond to ANY content? Pure reanalysis of the existing traces ($0).

    emit = should_emit(score) ∧ safe, safe = 4-AND incl. rate-limit secs_since_emit≥30 (core/brain.py,
    core/engine_g.py). H_9377 saw score MOVE with dyn_w (0.539→0.321) yet emit BYTE-IDENTICAL. That is
    only possible if every score-gate flip landed on safe=0 rows — i.e. the clock MASKED the score
    change. If additionally emit≈1 for ~all safe-open rows, then H(emit | clock-open) ≈ 0 and the
    score/content gate is VACUOUS (never binds when the clock lets a tick through): MI≈0 is then
    mechanically forced, NOT a content wall. GATE-S (H_9377) only checked the marginal rate — it cannot
    see this conditional degeneracy. This census reads the logged `safe` field directly.

    Per arm, over all cells:
      C1 (reconstruction integrity): every emit=1 row has score>θ ∧ safe — proves emit≡should_emit∧safe.
      N_live   = clock-open rows (safe truthy).            can content even be asked here?
      emit_var = both emit labels present in the clock-open subset. no variance ⇒ H(emit|open)=0.
      N_bind   = clock-open ∧ score≤θ (score gate WOULD suppress).  ≈0 ⇒ score gate vacuous when open.
      N_other  = clock-open ∧ score>θ ∧ emit=0 (a DIFFERENT suppressor). dominant ⇒ not the clock.
      N_mask   = (seed,tick) groups whose score>θ FLIPS across dyn_w; masked = all members clock-closed.
      P1 (only if measurable): I(ag_conflict; emit | stage) on the clock-OPEN subset, a1 vs a3.

    Verdict (sequential — measurability gate first, then content; below-chance covered):
      C1 <100%                         → ⛔ INSTRUMENT-DEAD (emit ≠ should_emit∧safe; trace mis-logged).
      emit_var False / N_live<30       → 🕰️ D1 CLOCK-BOUND (regime): emit ⟺ clock, score gate vacuous.
        (N_mask high confirms the mask.)  H_9377 CONTENT-INERT RE-SCOPED to this regime, NOT terminal.
        reopen = one clock-live collection (validity registered here, before content seen ⇒ not t2g).
      N_other dominant (≥N_mask)       → 🍴 D3 REGIME-STARVED: a non-clock safety term suppresses; the
                                          dominant term is the next H (clock was a red herring).
      measurable ∧ a1≈a3 (TOST)        → 🧱 D2 CONTENT-WALL: content genuinely inert where askable →
                                          terminal-eligible (2nd lens earned).
      measurable ∧ a1 sig (either dir) → 🔎 D2′ DISCOVERY: content DOES move emit (a1@0.78 hinted
                                          silence) → "pulls emit" reframed, new H.
    """
    THR = 0.3  # spont_im_threshold() — core/engine_g.py (PROACTIVE_THRESHOLD), verified origin/main
    MDE, CTRL = 0.05, 0.01
    rows = _im_rows(argv)
    rows = [r for r in rows if all(k in r for k in ("stage", "score", "emit", "ag_conflict", "g_arm"))]
    print("═══ CLOCK-MASK CENSUS · H_9390 · emit = should_emit(score) ∧ safe ═══")
    print("  rows=%d  (θ=%.2f · clock = logged `safe` field, fallback secs_since_emit≥30)" % (len(rows), THR))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200)")
        return 0

    def _safe(r):
        if "safe" in r and r["safe"] is not None:
            return 1 if r["safe"] else 0
        s = r.get("secs_since_emit")
        return 1 if (s is not None and float(s) >= 30.0) else 0

    by = {}
    for r in rows:
        by.setdefault(str(r["g_arm"]), []).append(r)
    print("  arms: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(by.items())))

    # C1 — reconstruction integrity (global): every emit row must be score>θ ∧ clock-open.
    emit_rows = [r for r in rows if r.get("emit")]
    c1_ok = sum(1 for r in emit_rows if float(r["score"]) > THR and _safe(r))
    c1_frac = (c1_ok / len(emit_rows)) if emit_rows else 1.0
    print("  C1 reconstruction: %d/%d emit rows satisfy score>θ∧clock-open = %.3f"
          % (c1_ok, len(emit_rows), c1_frac))
    if c1_frac < 0.999:
        print("  ⇒ ⛔ INSTRUMENT-DEAD — emit ≠ should_emit(score)∧safe (trace mis-logged / θ wrong).")
        return 0

    # PER-CELL (arm × dyn_w) — the pooled MI is CONFOUNDED: at high dyn_w, score ≈ dyn_v by
    # construction, so I(tension;emit) is bought by the DIAL, not earned. H_9377's discriminator
    # requires the a1>a3 clock-open separation to be present at the ANCHOR (w=0.10 = production),
    # w-INVARIANT — not manufactured by raising w. So we read every cell and anchor the verdict.
    def _cell_stat(rs):
        openr = [r for r in rs if _safe(r)]
        n_live = len(openr)
        e1 = sum(1 for r in openr if r.get("emit"))
        emit_var = 0 < e1 < n_live
        n_bind = sum(1 for r in openr if float(r["score"]) <= THR)
        n_other = sum(1 for r in openr if float(r["score"]) > THR and not r.get("emit"))
        # H_9391 VACUITY — over ALL rows (not just clock-open): can should_emit(score) EVER say no?
        # If min(score) > θ the gate is a tautology and emit ≡ clock by construction: no clock
        # relaxation can open a content window, because the score never reaches the threshold.
        sc = [float(r["score"]) for r in rs]
        smin = min(sc) if sc else None
        n_below = sum(1 for v in sc if v <= THR)
        mi = nm = pv = None
        if emit_var and n_live >= 30:
            S = [int(r["stage"]) for r in openr]
            X = [float(r["ag_conflict"]) for r in openr]
            Y = [1 if r.get("emit") else 0 for r in openr]
            mi, nm, pv, _e = _gd_cmi_bin(X, Y, S)
        return dict(n=len(rs), live=n_live, e1=e1, var=emit_var, bind=n_bind, other=n_other,
                    mi=mi, nm=nm, pv=pv, smin=smin, below=n_below)

    cells = {}
    for a in by:
        for r in by[a]:
            w = r.get("dyn_w")
            wk = round(float(w), 4) if w is not None else 0.10
            cells.setdefault((a, wk), []).append(r)
    ws = sorted({wk for (_a, wk) in cells})
    print()
    print("  arm  dyn_w | N    open  open-emit%  N_bind | score_min  ≤θ%   | live-MI shuf  p")
    cres = {}
    for (a, wk) in sorted(cells):
        d = _cell_stat(cells[(a, wk)])
        cres[(a, wk)] = d
        print("  %-3s  %.2f  | %3d  %4d  %5.2f      %5d | %8.4f  %5.1f%% | %s"
              % (a, wk, d["n"], d["live"], (d["e1"] / d["live"]) if d["live"] else 0.0, d["bind"],
                 d["smin"] if d["smin"] is not None else float("nan"),
                 100.0 * d["below"] / d["n"] if d["n"] else 0.0,
                 ("%+.4f %.4f %.3f" % (d["mi"], d["nm"], d["pv"])) if d["mi"] is not None
                 else "— not measurable (H(emit|open)=0)"))

    anchor = min(ws)  # dyn_w=0.10 = production-identical (byte-identical to no-dyn_w)
    aA, a3A = cres.get(("a1", anchor), {}), cres.get(("a3", anchor), {})
    anchor_measurable = aA.get("var") and aA.get("live", 0) >= 30
    # a1 clock-open MI trend across w (dial signature = rises with w, absent at anchor)
    a1_mis = [(wk, cres.get(("a1", wk), {}).get("mi")) for wk in ws]
    hi_w = max((wk for wk in ws if cres.get(("a1", wk), {}).get("mi") is not None), default=None)
    print()
    print("  anchor dyn_w=%.2f (=production): a1 clock-open %s"
          % (anchor, "MEASURABLE (emit varies)" if anchor_measurable else "NOT measurable (emit⟺clock)"))

    if not anchor_measurable:
        # The production regime cannot ask the content question (emit is clock-determined there).
        hi_mi = cres.get(("a1", hi_w), {}).get("mi") if hi_w is not None else None
        print("  ⇒ 🕰️ D1 CLOCK-BOUND (production regime) — at the anchor, emit ⟺ clock: clock-open emit"
              " rate=%.2f, N_bind=%d" % ((aA.get("e1", 0) / aA.get("live", 1)) if aA.get("live") else 0.0, aA.get("bind", 0)))
        print("     (score gate %s when the clock is open). H(emit|clock-open)≈0 ⇒ H_9377 MI≈0 is mechanically"
              % ("vacuous" if aA.get("bind", 0) < 5 else "rarely binds"))
        print("     forced, NOT a content wall. H_9377 CONTENT-INERT ⇒ RE-SCOPE to CLOCK-BOUND@production.")
        # H_9391 VACUITY — is the score gate merely masked here, or STRUCTURALLY unable to ever fire?
        if aA.get("smin") is not None and aA["smin"] > THR:
            print("     ⚠️ 🕳️ SCORE-GATE VACUOUS@anchor: min(score)=%.4f > θ=%.2f over ALL %d rows (%.1f%% ≤θ)."
                  % (aA["smin"], THR, aA.get("n", 0), 100.0 * aA.get("below", 0) / max(1, aA.get("n", 1))))
            print("     should_emit(score) is a TAUTOLOGY at production ⇒ emit ≡ clock BY CONSTRUCTION, and")
            print("     NO clock relaxation can open a content window (a fully-open clock ⇒ emit≡1, still")
            print("     no variance). The 8-lane motivation — tension included — gates NOTHING at production:")
            print("     the severance is the score never REACHING θ, not the mixer weight and not content.")
            print("     ⇒ clock-live is NOT the lever. Lever candidates = the score×θ relation (θ inviolable),")
            print("     i.e. a regime where score STRADDLES θ at clock-open ticks (see the ≤θ% column).")
        if hi_mi is not None and hi_mi >= MDE:
            print("     ⚠️ clock-open MI APPEARS only at high dyn_w=%.2f (MI %+.4f) — but there score≈dyn_v by"
                  % (hi_w, hi_mi))
            print("     construction, so that is the DIAL (manipulation-bought), NOT substrate (H_9377 w-invariance).")
        if aA.get("smin") is not None and aA["smin"] > THR:
            print("     NOT terminal. reopen = a STRADDLE regime (score must cross θ at clock-open ticks);")
            print("     a clock relaxation alone is REFUTED as the lever by the vacuity above.")
        else:
            print("     NOT terminal. reopen = 1 clock-LIVE collection (emit must vary within clock-open at anchor w).")
        return 0

    # anchor IS measurable — the content question is askable at production. Read a1 vs a3 at the anchor.
    sep = (aA.get("mi") or 0.0) - (a3A.get("mi") or 0.0)
    a1_sig = aA.get("mi") is not None and aA["mi"] >= MDE and aA.get("nm", 1.0) <= CTRL and aA.get("pv", 1.0) < 0.005
    print()
    if a1_sig and sep > MDE:
        print("  ⇒ 🔎 D2′ DISCOVERY — at the ANCHOR (production w), clock-open independent-G content MOVES emit"
              " (a1 MI %+.4f, a1−a3 %+.4f · w-invariant)." % (aA["mi"], sep))
        print("     H_9377 CONTENT-INERT OVERTURNED: the wall was clock-masking, not content-inertness. New H.")
    elif abs(sep) <= MDE and (aA.get("mi") or 0.0) < MDE:
        print("  ⇒ 🧱 D2 CONTENT-WALL — at the anchor, where emit CAN respond (clock-open N=%d), a1≈a3"
              " (|Δ|=%.4f≤%.2f):" % (aA.get("live", 0), abs(sep), MDE))
        print("     content genuinely inert where askable. 2nd independent lens → CONTENT-INERT terminal-eligible.")
    else:
        print("  ⇒ ⏳ PENDING — anchor a1 partially separates (MI %s · Δ %+.4f). Extend n / tighten." %
              (("%.4f" % aA["mi"]) if aA.get("mi") is not None else "n/a", sep))
    return 0


def _im_rows(paths):
    """Load decision-trace rows (skip the _meta header). One row per tick."""
    out = []
    for p in paths:
        for line in open(p, "r", encoding="utf-8", errors="surrogateescape"):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except ValueError:
                # a trace flushed mid-write (a daemon still running when the panel started) can
                # leave one truncated line; tolerate it like the --tension-emit loader does rather
                # than crash the whole verdict on a single bad row (verdict-integrity).
                continue
            if d.get("_meta"):
                continue
            d["_src"] = p
            out.append(d)
    return out


def _im_H(xs):
    """Plug-in entropy (nats) of a discrete sample."""
    n = len(xs)
    if n == 0:
        return 0.0
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    h = 0.0
    for v in c.values():
        p = float(v) / n
        h -= p * math.log(p)
    return h


def _im_clip01(x):
    """1:1 with the daemon's `_afs_clip01` (cli/chat.py) — the PC rebuilds urgency with the
    SAME arithmetic the daemon uses, so any divergence here would be a new quantity again."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _im_H_p(p):
    """Binary entropy (nats) of a PROBABILITY, not of a sample.

    The COMPOSITION panel builds a channel p(Y=1|A,S) analytically out of the two measured
    links, so its entropy has to be taken from the probability itself — plugging the composed
    channel back through a sample estimator would re-introduce exactly the sampling bias the
    composed channel is meant to be free of."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))


def _im_cmi(A, Y, S):
    """I(A;Y|S) = Σ_s p(s)·[H(A|s) + H(Y|s) − H(A,Y|s)], Miller–Madow corrected per stratum.
    MM adds (support−1)/(2n) — the plug-in estimator is biased UP, and that bias is exactly
    what manufactures a false positive on a thin channel (convergence decode-py-2)."""
    n = len(S)
    if n == 0:
        return 0.0
    strata = {}
    for i in range(n):
        strata.setdefault(S[i], []).append(i)
    tot = 0.0
    for s, idx in strata.items():
        m = len(idx)
        a = [A[i] for i in idx]
        y = [Y[i] for i in idx]
        ay = [(A[i], Y[i]) for i in idx]
        ha, hy, hay = _im_H(a), _im_H(y), _im_H(ay)
        mm = (len(set(a)) - 1 + len(set(y)) - 1 - (len(set(ay)) - 1)) / (2.0 * m) if m > 0 else 0.0
        tot += (float(m) / n) * max(0.0, ha + hy - hay + mm)
    return tot


def _im_h_given_S(X, S):
    """V-CEILING: H(X|S), the stratified conditional entropy of ANY channel X.

    I(A;Y|S) <= min(H(A|S), H(Y|S)) by identity, so a dead channel on EITHER side forces
    I=0 by definition, not by measurement. H_9308 died on the ACTION side (H(A|S)=0). The
    OUTCOME side is the same trap wearing the other hat: if the stage already determines
    the next-tick score, then Y is a function of S and I is 0 no matter what the mouth
    says. Gate BOTH before reading I (convergence interact-mi-py-2)."""
    n = len(S)
    if n == 0:
        return 0.0
    strata = {}
    for i in range(n):
        strata.setdefault(S[i], []).append(i)
    return sum((float(len(idx)) / n) * _im_H([X[i] for i in idx]) for idx in strata.values())


def _interact_mi(argv):
    """H_9328 — I(A;Y|S) over daemon decision traces. Reads only; no decode.

    A = a_fold8 (the H_9257 FROZEN 8-bucket axis the daemon actually consumes on emit)
    S = stage (the gate's own conditioning; conditioning on it makes A ⟂ everything-else|S
        by construction, so the S-lite omitted-confounder false positive cannot recur)
    Y = score_{t+1} binarised at a FROZEN median passed in via --seed <median×1e6>, or the
        in-sample median when absent (reported as such — an in-sample split is a diagnostic,
        never a headline).
    """
    paths = []
    perm = 200
    mde = 0.010
    hfloor = 0.030
    for a in argv:
        if a.startswith("--"):
            continue
        paths.append(a)
    rows = _im_rows(paths)
    emits = [r for r in rows if r.get("emit") and int(r.get("a_fold8", -1)) >= 0]
    print("═══ H_9328 INTERACT-MI · I(A;Y|S) ═══")
    print("  traces=%d  ticks=%d  emit-ticks(with A)=%d" % (len(paths), len(rows), len(emits)))
    if len(emits) < 30:
        print("  ⇒ NOT-POWERED (emit-ticks < 30) — 수집 증량 필요")
        return 0
    # Y = next-tick score, within the same trace file
    by_src = {}
    for r in rows:
        by_src.setdefault(r["_src"], []).append(r)
    nxt = {}
    nxt_gate = {}
    for src, rs in by_src.items():
        rs.sort(key=lambda r: int(r["tick"]))
        for i in range(len(rs) - 1):
            nxt[(src, int(rs[i]["tick"]))] = float(rs[i + 1]["score"])
            # V5 needs the bookkeeping of the tick that PRODUCED Y, not the one that spoke.
            nxt_gate[(src, int(rs[i]["tick"]))] = (int(rs[i + 1]["stage"]),
                                                   rs[i + 1].get("safe"))
    use = [r for r in emits if (r["_src"], int(r["tick"])) in nxt]
    if len(use) < 30:
        print("  ⇒ NOT-POWERED (next-tick score 있는 emit-tick < 30)")
        return 0
    ys = sorted(nxt[(r["_src"], int(r["tick"]))] for r in use)
    med = ys[len(ys) // 2]
    A = [int(r["a_fold8"]) for r in use]
    S = [int(r["stage"]) for r in use]
    Y = [1 if nxt[(r["_src"], int(r["tick"]))] > med else 0 for r in use]
    # ── V-CEILING · BOTH channels (BLOCKING · before any I is read) ────────────────
    # I(A;Y|S) <= min(H(A|S), H(Y|S)) is an IDENTITY. A dead channel on either side pins
    # I to 0 by definition. Gating only the action side (as this did until interact-mi-py-2)
    # leaves the outcome side wide open: if the stage already fixes the next-tick score,
    # a null reads as "the loop carries no information" when it actually reads "we asked a
    # question whose answer was already written". Both, or neither.
    hA = _im_h_given_S(A, S)
    hY = _im_h_given_S(Y, S)
    print("  🚦 V-CEILING  H(A|S) = %.4f nats · H(Y|S) = %.4f nats   (floor %.3f = 3×MDE)"
          % (hA, hY, hfloor))
    if hA < hfloor:
        print("  ⇒ NOT-POWERED — 행동 채널이 죽어 있다. I 는 정의상 0 이지 측정된 0 이 아니다.")
        print("     (H_9308 이 정확히 여기서 죽었다 · convergence interact-mi-py-1)")
        return 0
    if hY < hfloor:
        print("  ⇒ NOT-POWERED — 결과 채널이 죽어 있다(다음-tick score 가 stage 로 이미 결정됨).")
        print("     I 는 정의상 0 — 입이 무엇을 말했든 물을 수 있는 질문이 아니었다.")
        print("     (같은 항등식의 반대쪽 축 · convergence interact-mi-py-2)")
        return 0
    # ── V5 · GATE-CLOSED (the FIFTH identity-zero · BLOCKING · H_9337 frozen bar) ──────
    # H(Y|S) alive is NOT enough. The gate's own inputs are stage AND the rate-limiter
    # (`safe`). If emit is fully determined by (stage, safe), then Y is a function of the
    # gate's own bookkeeping and STILL-ADDITIVE is settled BEFORE the mouth opens — again
    # by definition, not by measurement. That is a different claim from "the loop carries
    # no information": it says THE GATE LOOKS AT NOTHING. H_9100 (motivation saturated at
    # floor ~0.7, always clearing the 0.3 threshold) and H_9209/9225/9230 (every read-side
    # emit wiring = THEATER, ΔEff 0/120) predict exactly this shape, so it must be its own
    # verdict, not folded into the wall.
    #
    # ⚠️ CONDITION ON THE TICK THAT PRODUCED Y, NOT THE ONE THAT SPOKE. Y is score_{t+1}, so
    # the gate bookkeeping that could already have written it is (stage_{t+1}, safe_{t+1}).
    # Stratifying by the SPEAKING tick's (stage, safe) is a different question and cannot
    # detect the trap — a synthetic arm with Y := f(stage_{t+1}, safe_{t+1}) sailed straight
    # through that version of the gate. Conditioning here is safe from the mediator trap
    # because `safe` is a rate-limiter over WHETHER/WHEN the daemon spoke — it is not a
    # descendant of A, which is WHAT it said (the H_9257 content axis).
    sf = [nxt_gate[(r["_src"], int(r["tick"]))][1] for r in use]
    if all(v is not None for v in sf):
        svals = sorted(float(v) for v in sf)
        smed = svals[len(svals) // 2]
        SG = [(nxt_gate[(r["_src"], int(r["tick"]))][0],
               1 if float(nxt_gate[(r["_src"], int(r["tick"]))][1]) > smed else 0) for r in use]
        hYg = _im_h_given_S(Y, SG)
        print("  🚦 V5 GATE     H(Y|S,safe) = %.4f nats   (floor %.3f · safe = rate-limit lane)"
              % (hYg, hfloor))
        if hYg < hfloor:
            print("  ⇒ ⛔ GATE-CLOSED — 게이트가 **아무것도 안 본다**(emit 이 stage+safe 로 완전결정).")
            print("     이건 🧱 가 아니다. '폐루프가 정보를 안 나른다'가 아니라 '게이트에 물어볼 수")
            print("     있는 질문이 없다' — STILL-ADDITIVE 는 입이 열리기 전에 이미 확정돼 있었다.")
            print("     다음 물음은 '루프가 나르는가'가 아니라 '게이트가 무엇을 보게 할 수 있는가'다.")
            return 0
    else:
        print("  🚦 V5 GATE     safe 미기록 trace ⇒ SKIP (구 포맷 · GATE-CLOSED 를 배제할 수 없음)")
    # ── V6 · DECISION-CHANNEL (the SIXTH identity-zero · H_9345) ──────────────────────
    #
    # Every gate above asks whether the PROXY (score) has room. None of them asks whether the
    # DECISION does. Measured on 70 rollouts x 2198 ticks: H(emit|stage) = 0.000000 EXACTLY —
    # stages 0/1/4 emit 100% of the time, stages 2/3 are silent 100% of the time, and the
    # silence lands on ticks 9-10 in every single rollout. emit/silence is a PURE FUNCTION OF
    # STAGE. So I(anything ; emit | stage) = 0 BY IDENTITY, and the question "does what the
    # substrate says inform its next DECISION" has no decision to inform.
    #
    # This does not invalidate a score-based readout — score genuinely varies. It BOUNDS it:
    # a verdict on `score` is a verdict on a lane the gate consumes, NOT on the gate's output.
    # Say so, or you will write "the loop does not inform the next decision" when what you
    # measured was a proxy and the decision was a clock.
    emx = [r.get("emit") for r in rows]
    if all(v is not None for v in emx):
        Sall = [int(r["stage"]) for r in rows]
        hEmit = _im_h_given_S([1 if v else 0 for v in emx], Sall)
        rate = sum(1 for v in emx if v) / float(len(emx))
        print("  🚦 V6 DECISION H(emit|S) = %.6f nats   (발화율 %.1f%% · n=%d tick 전수)"
              % (hEmit, 100.0 * rate, len(emx)))
        if hEmit < hfloor:
            print("     ⇒ ⛔ **DECISION-CONSTANT** — emit/침묵이 stage 의 **순수 함수**다.")
            print("        I(무엇이든 ; emit | S) ≤ H(emit|S) ≈ 0 ⇒ **어떤 변수도 결정에 정보를**")
            print("        **나를 수 없다 — 측정 이전에, 정의상.** 게이트는 게이트가 아니라 시계다(H_9345).")
            print("        아래 판정은 **대리변수(score)에만 스코프**된다 — 게이트의 출력이 아니라")
            print("        게이트가 소비하는 lane 에 대한 것이다. '다음 결정에' 로 확장하지 마라.")
    I = _im_cmi(A, Y, S)
    # ── The exchangeable unit is MEASURED, not assumed (convergence evaluate-py-13 · chat-py-3).
    # Two candidate units, and which one is right is an empirical question about THIS trace set:
    #   ROLLOUT — correct when A is constant/strongly correlated within a session. That is what
    #     the FIRST H_9328 traces showed ({5:18} per rollout) — but that constancy turned out to
    #     be an INSTRUMENT DEFECT (a session-constant sampler seed made the mouth redraw the same
    #     80 bytes every tick, chat-py-3). It was not a fact about the substrate.
    #   TICK — correct when consecutive A's carry no autocorrelation, i.e. the previous tick does
    #     not predict the next. With the per-tick RNG stream fixed, that is what the data shows.
    # So we DECIDE FROM THE DATA and REPORT BOTH: if the verdict flips between units, the verdict
    # is about the unit, not the substrate, and the honest reading is INVALID.
    src_of = [r["_src"] for r in use]
    rollouts = sorted(set(src_of))
    n_roll = len(rollouts)
    # measured autocorrelation of A across consecutive ticks WITHIN a rollout
    by_src = {}
    for i, sc in enumerate(src_of):
        by_src.setdefault(sc, []).append(i)
    same = tot = 0
    for sc, idx in by_src.items():
        idx.sort(key=lambda i: int(use[i]["tick"]))
        for j in range(len(idx) - 1):
            tot += 1
            if A[idx[j]] == A[idx[j + 1]]:
                same += 1
    ca = {}
    for a in A:
        ca[a] = ca.get(a, 0) + 1
    chance_same = sum((v / len(A)) ** 2 for v in ca.values())
    obs_same = (float(same) / tot) if tot else 1.0
    autocorr = obs_same > chance_same * 1.25
    print("  단위 실측: 연속 tick 의 A 동일비율 %.3f vs 우연 %.3f ⇒ %s"
          % (obs_same, chance_same,
             "자기상관 O ⇒ **rollout** 이 표본" if autocorr else "자기상관 X ⇒ **tick** 이 표본"))
    print("  rollout=%d · emit-tick=%d" % (n_roll, len(use)))
    if n_roll < 8:
        print("  ⇒ NOT-POWERED (rollout < 8)")
        return 0

    rnd = random.Random(20260714)

    def _null(unit):
        """unit='rollout': block-permute the rollout→A map (ticks stay together).
           unit='tick'   : permute A within each S stratum."""
        out = []
        for _ in range(perm):
            if unit == "rollout":
                a_of = {}
                for i, sc in enumerate(src_of):
                    a_of.setdefault(sc, A[i])
                vals = [a_of[sc] for sc in rollouts]
                rnd.shuffle(vals)
                remap = {sc: vals[j] for j, sc in enumerate(rollouts)}
                Ap = [remap[sc] for sc in src_of]
            else:
                Ap = list(A)
                strata = {}
                for i, s in enumerate(S):
                    strata.setdefault(s, []).append(i)
                for idx in strata.values():
                    vals = [Ap[i] for i in idx]
                    rnd.shuffle(vals)
                    for j, i in enumerate(idx):
                        Ap[i] = vals[j]
            out.append(_im_cmi(Ap, Y, S))
        out.sort()
        return out

    print("  EXP   I(A;Y|S) = %.5f nats" % I)
    print("  Y-bin: in-sample median %.5f (진단용 · 헤드라인 아님)  n=%d" % (med, len(use)))
    verdicts = {}
    for unit in ("rollout", "tick"):
        null = _null(unit)
        nm = sum(null) / len(null)
        nsd = (sum((v - nm) ** 2 for v in null) / max(1, len(null) - 1)) ** 0.5
        pv = (sum(1 for v in null if v >= I) + 1.0) / (perm + 1.0)
        ef = I - nm
        tag = " ← 실측 단위" if (unit == "rollout") == autocorr else ""
        print("  C1 PERM[%-7s] null mean=%.5f sd=%.5f · perm-p=%.4f · EARNED=%.5f%s"
              % (unit, nm, nsd, pv, ef, tag))
        verdicts[unit] = (ef >= mde and pv < 0.005)
    eff_unit = "rollout" if autocorr else "tick"
    null = _null(eff_unit)
    nm = sum(null) / len(null)
    p = (sum(1 for v in null if v >= I) + 1.0) / (perm + 1.0)
    eff = I - nm
    print("  EARNED[%s] = %.5f nats   (MDE %.3f · TOST ±%.3f)" % (eff_unit, eff, mde, mde))
    if verdicts["rollout"] != verdicts["tick"]:
        print("  ⇒ ⛔ INVALID — 판정이 **단위 선택에 뒤집힌다**(rollout=%s · tick=%s)."
              % (verdicts["rollout"], verdicts["tick"]))
        print("     그 결론은 기질이 아니라 내 가정에 관한 것이다. 단위를 데이터로 못박기 전엔 못 읽는다.")
        return 0
    if eff >= mde and p < 0.005:
        print("  ⇒ 🟢 SIGNAL — 단 C2 CARRIER-SWAP 없이는 PASS 아님(내용맹 배제 불가)")
    elif abs(eff) <= mde:
        print("  ⇒ TOST 등가역 — 폐루프가 DATA-ADDITIVE 방향 (n·검정력 명시 필요)")
    else:
        print("  ⇒ 미달 · 판정 보류")

    # ── MEDIATION · 사슬을 열어본다 (진단 · 헤드라인 아님) ──────────────────────────
    # 헤드라인 I(A;Y|S) 는 사슬의 두 끝만 잰다. 그 사이에는 실제 배선이 있다:
    #
    #     [기질이 뱉은 말] ──▶ [afield] ──▶ [ score ] ──▶ [emit 게이트]
    #        A (a_fold8)      recon_err      Y (2-bin)
    #
    # emit tick 에서 g_text 는 afield step 에 들어가고 그 결과가 recon_err 다. 즉 recon_err
    # 는 "말이 장(場)을 밀었는가"의 직접 관측이고, 데몬이 tick 마다 이미 기록한다.
    # A→Y 가 0 일 때 두 세계가 갈린다:
    #   ① M1(A→recon_err) 도 0  ⇒ 말이 장조차 못 민다. 주입이 무효 = 계기/배선 문제.
    #   ② M1 은 살고 M2(recon_err→Y) 가 0  ⇒ 말은 장을 미는데 **게이트가 그걸 안 본다**.
    #      이건 H_9209/H_9225/H_9230 이 read-side 배선에서 반복해 만난 THEATER 그림과 합류한다
    #      (emit = stage + rate-limit 지배). 그렇다면 null 은 고립된 사실이 아니라 그 벽의 목격이다.
    # 둘 다 같은 C1 순열 귀무(실측 단위) 위에서 잰다. 진단이므로 verdict 를 바꾸지 않는다.
    #
    # ⏱️ THE LAG IS PART OF THE WIRING — take the mediators from the tick that PRODUCED Y.
    # The daemon reads a 1-tick-lagged prediction error (chat.py: `pending_recon` is written
    # at the emit site of tick t and READ at tick t+1), so the causal chain is
    #     A_t ──▶ recon_err_{t+1} ──▶ score_{t+1} (= Y)
    # A row's OWN `recon_err` is the error of the PREVIOUS utterance A_{t-1}, and it feeds
    # score_t, not Y. Reading the same row's mediator therefore misses by exactly one tick in
    # BOTH links: M1 would compare A_t against A_{t-1}'s error, and M2 would ask a mediator
    # that already spent itself on score_t to explain score_{t+1}. A synthetic arm with
    # score := f(recon_err) at the same tick read M2 as DEAD under that version — the
    # instrument could not see a channel that was planted by construction. The headline
    # I(A_t; score_{t+1}|S) had the lag right; the whole diagnostic panel had it wrong, and a
    # null would have read as "the text never even reaches the field".
    # NB: `by_src` is rebound to an index map by the autocorrelation block above — rebuild
    # the row map under its own name rather than reusing a name the code already spent.
    rows_by_src = {}
    for r in rows:
        rows_by_src.setdefault(r["_src"], []).append(r)
    nxt_lane = {}
    for src, rs in rows_by_src.items():
        rs.sort(key=lambda r: int(r["tick"]))
        for i in range(len(rs) - 1):
            nxt_lane[(src, int(rs[i]["tick"]))] = rs[i + 1]
    rec = [nxt_lane[(r["_src"], int(r["tick"]))].get("recon_err") for r in use]
    if any(v is None for v in rec):
        print("  ── MEDIATION: recon_err 미기록 trace ⇒ SKIP (구 trace 포맷)")
        return 0
    rs = sorted(float(v) for v in rec)
    rmed = rs[len(rs) // 2]
    R = [1 if float(v) > rmed else 0 for v in rec]
    hR = _im_h_given_S(R, S)
    print("  ── MEDIATION (진단 · verdict 불변) ─────────────────────────────")
    print("     H(R|S) = %.4f nats   R = recon_err 2-bin (afield 뿌리 · g_text 가 직접 민다)" % hR)
    if hR < hfloor:
        print("     ⇒ 매개 채널 자체가 죽어 있다 — M1/M2 는 정의상 0. 사슬을 못 연다.")
    for nm, X, Z in ((("M1  A→R (말이 장을 미는가)", A, R), ("M2  R→Y (장이 게이트를 미는가)", R, Y))
                     if hR >= hfloor else ()):
        i_xz = _im_cmi(X, Z, S)
        null = []
        for _ in range(perm):
            Xp = list(X)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Xp[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Xp[k] = vals[j]
            null.append(_im_cmi(Xp, Z, S))
        nm_ = sum(null) / len(null)
        pv = (sum(1 for v in null if v >= i_xz) + 1.0) / (perm + 1.0)
        earned = i_xz - nm_
        tag = "🔗 LIVE" if (earned >= mde and pv < 0.005) else ("· 등가(0)" if abs(earned) <= mde else "· 미달")
        print("     %-28s EARNED = %+.5f nats · perm-p = %.4f   %s" % (nm, earned, pv, tag))
    print("     ⇒ M1 살고 M2 죽으면: 말은 장을 밀지만 **게이트가 안 본다**(read-side THEATER 합류).")
    print("        M1 도 죽으면: 주입 자체가 장에 안 닿는다(배선/계기 의심 — 기질 주장 금지).")
    print("     ⚠️ 사다리의 한계 둘: (a) R 은 2-bin ⇒ M2 죽음의 스코프는 '게이트가 R 을 1-bit")
    print("        해상도에서 안 읽는다'까지다. (b) M1·M2 가 **둘 다 살아도** end-to-end I=0 일 수")
    print("        있다 — 쌍별 MI 는 합성되지 않는다(나르는 성분 ≠ 쓰는 성분).")

    # ── B1 · BOOKKEEPING (H_9337 frozen bar · guards the 🟢 강한 독법) ────────────────
    # If R is a deterministic function of (A, S), then "recognition error" is not a percept
    # at all — it is a LEDGER, an arithmetic restatement of what the mouth just said. Then
    # I(A;Y|S) > 0 is not a discovery, it is ACCOUNTING: the daemon's own bookkeeping is the
    # wire. This is the general form of the trap already hit once ("query the store with the
    # last utterance" → constant 1.15, because you asked about what you just filed).
    #
    # ⚠️ C2 CARRIER-SWAP CANNOT SEPARATE THIS. A swapped carrier rides the SAME arithmetic,
    # so a pure-ledger system emits EXACTLY the same C2 signature as a real one (both die
    # under swap). C2 separates a COMMON-CAUSE drift (latent state driving A and Y together);
    # bookkeeping is separated by B1 and by nothing else.
    hRA = _im_h_given_S(R, [(a, s) for a, s in zip(A, S)])
    print("  ── B1 BOOKKEEPING (🟢 의 강한 독법을 지키는 게이트) ─────────────")
    print("     H(R|A,S) = %.4f nats   (floor %.3f — R 이 A 로 완전결정이면 재인식이 아니라 장부)"
          % (hRA, hfloor))
    if hRA < hfloor:
        print("     ⇒ ⛔ 장부다 — R 은 A 의 산술적 재진술일 뿐, 새 지각의 분산을 싣지 않는다.")
        print("        I > 0 이 나와도 그건 발견이 아니라 **회계**다. 🟢 의 강한 독법 무효.")
    else:
        print("     ⇒ ✅ R 은 A 너머의 분산을 싣는다 — 재인식이 장부로 붕괴하지 않았다.")

    # ── PC · POWER POSITIVE CONTROL (🧱 선언의 전제조건 · memory power-before-negative-verdict)
    # Before any wall is declared, prove the INSTRUMENT can see a channel that is KNOWN to be
    # live. H_9101 earned exactly one proven emit channel: urgency = phasic Δ tension
    # (`ten_phasic`). Run it through the identical I(·;Y|S) pipe:
    #   urgency→Y ALIVE  ∧  R→Y dead  ⇒ the gate is SELECTIVELY blind. A real 🧱.
    #   urgency→Y DEAD               ⇒ the instrument cannot see ANY gate input. That is
    #                                  ⛔ NOT-POWERED, and a 🧱 declared here would be a
    #                                  statement about my measurement, not the substrate.
    # ⚠️ THE POSITIVE CONTROL MUST MEASURE THE QUANTITY IT NAMES.
    # This block used `ten_phasic` and called it "urgency". It is NOT urgency. chat.py:1878:
    #     urgency = clip01(0.4*agloop_ctx + 0.3*cur_phasic + 0.3*ten_phasic)
    #     cur_phasic = clip01(0.5 + 3.0*(cur_ctx - cur_ema))
    # ten_phasic is ONE of three terms, weighted 0.3. So the control was reading 30% of the
    # channel it claimed to certify, and when it read DEAD that told us nothing about urgency.
    # The name matched; the thing did not (tool-definition-read-code-not-docstring). All three
    # terms are in the trace, so rebuild urgency EXACTLY as the daemon does and use THAT.
    def _urgency(r):
        cur_ph = _im_clip01(0.5 + 3.0 * (float(r["cur_ctx"]) - float(r["cur_ema"])))
        return _im_clip01(0.4 * float(r["agloop_ctx"]) + 0.3 * cur_ph + 0.3 * float(r["ten_phasic"]))

    need = ("agloop_ctx", "cur_ctx", "cur_ema", "ten_phasic")
    have = all(all(k in nxt_lane[(r["_src"], int(r["tick"]))] for k in need) for r in use)
    tp = [_urgency(nxt_lane[(r["_src"], int(r["tick"]))]) for r in use] if have else [None]
    print("  ── PC 검정력 양성대조 (🧱 선언의 전제조건) ─────────────────────")
    print("     U = clip01(0.4·agloop_ctx + 0.3·cur_phasic + 0.3·ten_phasic)  ← chat.py:1878 그대로")
    if any(v is None for v in tp):
        print("     urgency 항 미기록 ⇒ SKIP — 양성대조 없이 🧱 선언 금지")
    else:
        ts = sorted(float(v) for v in tp)
        tmed = ts[len(ts) // 2]
        U = [1 if float(v) > tmed else 0 for v in tp]
        hU = _im_h_given_S(U, S)
        i_uy = _im_cmi(U, Y, S)
        null = []
        for _ in range(perm):
            Up = list(U)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, Y, S))
        nmu = sum(null) / len(null)
        pvu = (sum(1 for v in null if v >= i_uy) + 1.0) / (perm + 1.0)
        eu = i_uy - nmu
        live = (eu >= mde and pvu < 0.005)
        print("     urgency→Y  EARNED = %+.5f nats · perm-p = %.4f · H(U|S) = %.4f   %s"
              % (eu, pvu, hU, "🔗 LIVE (H_9101 유일 proven 채널)" if live else "💀 DEAD"))
        if not live:
            print("     ⇒ ⛔ 검정력 부재 — 계기가 **알려진 살아있는 채널조차** 못 본다.")
            print("        여기서 🧱 를 선언하면 그건 기질이 아니라 내 측정에 관한 문장이다.")
        else:
            print("     ⇒ ✅ 계기는 게이트 입력을 볼 수 있다 — R→Y 가 죽으면 그건 **선택적** 실명이다.")
        # ── PC-SCOPE · urgency 가 죽은 것은 계기 탓인가, urgency 의 성질인가 (H_9340) ────
        #
        # The PC bar says "urgency->Y dead => the instrument is blind => no wall may be
        # declared". That inference has a premise, and the premise is CHECKABLE IN THE SAME
        # RUN: if M2 (R->Y) came back LIVE, then the ->Y detector demonstrably sees a gate
        # input, and the instrument is NOT blind. Then urgency's death is a fact about
        # URGENCY, not about the measurement — and the bar's warrant is void even though the
        # bar itself still stands (re-reading a rule after seeing the number is tune-to-green).
        #
        # What remains is a scope question. H_9101 earned urgency as the one proven channel
        # for emit SHADE — what the mouth says at tick t, same tick. This panel asks about
        # the next tick's SCORE. Those are different targets, and urgency colouring the mouth
        # at t while not reaching the gate at t+1 makes both facts true at once. Measure it:
        # the SAME urgency, the SAME stage conditioning, against the SAME-TICK action.
        #
        # NOTE THE TICK. PC's U is the urgency of the tick that PRODUCED Y (t+1) — that is the
        # right one for a ->Y question. The shade question is about the urgency that coloured
        # the MOUTH, and the mouth spoke at t. Reusing PC's U here would ask whether the NEXT
        # tick's urgency explains THIS tick's utterance, which is a question about the future.
        Uc_raw = [_urgency(r) for r in use]
        ucs = sorted(Uc_raw)
        ucmed = ucs[len(ucs) // 2]
        Uc = [1 if v > ucmed else 0 for v in Uc_raw]
        i_ua = _im_cmi(Uc, A, S)
        null = []
        for _ in range(perm):
            Up = list(Uc)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, A, S))
        nma = sum(null) / len(null)
        pva = (sum(1 for v in null if v >= i_ua) + 1.0) / (perm + 1.0)
        ea = i_ua - nma
        shade_live = (ea >= mde and pva < 0.005)
        print("     urgency→A  EARNED = %+.5f nats · perm-p = %.4f   %s   ← same-tick (H_9101 축)"
              % (ea, pva, "🔗 LIVE" if shade_live else "💀 DEAD"))
        # ── URGENCY-CHANNEL · 코드가 말하는 하류를 직접 잰다 (chat.py:1881) ──────────
        #
        # `urgency` does not flow into the score directly. It sets the tick interval:
        #     idle = 5.0 + 55.0 * clip01(stage_env * (0.5 + urgency))
        # and `idle` is passed straight into brain_emit(). So urgency's channel is the
        # EMIT DECISION — whether/when the substrate speaks, not what it says. Measure the
        # target the wiring names, not the one the panel happens to have around.
        em = [1 if nxt_lane[(r["_src"], int(r["tick"]))].get("emit") else 0 for r in use]
        i_ue = _im_cmi(U, em, S)
        null = []
        for _ in range(perm):
            Up = list(U)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, em, S))
        nme = sum(null) / len(null)
        pve = (sum(1 for v in null if v >= i_ue) + 1.0) / (perm + 1.0)
        ee = i_ue - nme
        emit_live = (ee >= mde and pve < 0.005)
        hE = _im_h_given_S(em, S)
        print("     urgency→emit EARNED = %+.5f nats · perm-p = %.4f · H(emit|S) = %.4f   %s"
              % (ee, pve, hE, "🔗 LIVE" if emit_live else "💀 DEAD"))
        print("        (코드가 말하는 하류: urgency → idle → brain_emit · chat.py:1881)")
        # The CONCLUSION must key on the axis the WIRING names — emit — not on whichever axis
        # the panel happened to have lying around. Keying it on urgency->Y read "both dead" on
        # a synthetic arm where urgency drove the emit decision by construction.
        decision_live = emit_live or live
        if hE < hfloor:
            print("     ⇒ ⚠️ emit 채널 자체가 죽어 있다(거의 항상 말하거나 항상 침묵) — 판독 불가.")
        elif decision_live and not shade_live:
            print("     ⇒ ✅ **urgency 는 결정-채널이지 내용-채널이 아니다.** 언제/여부를 밀되")
            print("        발화의 내용축은 물들이지 않는다. H_9101(emit 의 유일 proven 채널)과")
            print("        **정합**한다 — 그리고 이것은 '내용이 게이트에 못 닿는다'는 헤드라인과")
            print("        **같은 그림**이다: 게이트는 읽되, 읽는 것이 내용이 아니다.")
        elif shade_live and not decision_live:
            print("     ⇒ urgency 가 입은 물들이나 결정으로는 안 간다(스코프 분리).")
        elif not shade_live and not decision_live:
            print("     ⇒ ⚠️ urgency 가 **어느 축으로도** 안 간다 — 이 양이 H_9101 의 urgency 와")
            print("        **같은지 코드에서 diff** 하라(docstring 금지 · tool-definition-read-code-not-docstring).")
            print("        선례: 이 패널이 ten_phasic 을 urgency 라 부르다 30%만 재고 있었다.")
        else:
            print("     ⇒ urgency 가 결정과 내용을 **둘 다** 민다 — 채널이 분리되지 않는다.")

    # ── M3 · MEDIATION EXHAUSTED (진단) ──────────────────────────────────────────────
    # If roots ① and ② carry the whole path, then conditioning on them should EXHAUST the
    # mediation: I(A;Y|S,R,L) ≈ 0. A residual > 0 says there is an UNACCOUNTED path from the
    # mouth to the gate — which is itself a finding, not a nuisance.
    lan = [nxt_lane[(r["_src"], int(r["tick"]))].get("rel_lane") for r in use]
    if not any(v is None for v in lan):
        ls_ = sorted(float(v) for v in lan)
        lmed = ls_[len(ls_) // 2]
        L = [1 if float(v) > lmed else 0 for v in lan]
        SRL = [(s, r_, l_) for s, r_, l_ in zip(S, R, L)]
        i_res = _im_cmi(A, Y, SRL)
        # The RAW residual cannot be read against MDE. Conditioning on (S,R,L) shatters the
        # sample into ~12x more strata, and plug-in CMI is POSITIVELY BIASED in small strata —
        # every synthetic arm with NO residual path still read 0.019-0.037 nats here. Reading
        # that against a 0.010 bar would MANUFACTURE an "unaccounted path" out of thin air, the
        # same class of defect as an order-statistic bar (probe-defect-census). The bias lives
        # in the null too, so subtract the null: EARNED, never the raw value.
        null = []
        for _ in range(perm):
            Ap2 = list(A)
            st = {}
            for k, z in enumerate(SRL):
                st.setdefault(z, []).append(k)
            for idx in st.values():
                vals = [Ap2[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Ap2[k] = vals[j]
            null.append(_im_cmi(Ap2, Y, SRL))
        nm3 = sum(null) / len(null)
        pv3 = (sum(1 for v in null if v >= i_res) + 1.0) / (perm + 1.0)
        e3 = i_res - nm3
        print("  ── M3 매개 소진 (진단) ─────────────────────────────────────────")
        print("     I(A;Y | S,R,L) = %.5f · null = %.5f ⇒ EARNED = %+.5f nats · perm-p = %.4f"
              % (i_res, nm3, e3, pv3))
        if e3 >= mde and pv3 < 0.005:
            print("     ⇒ 잔차 EARNED > MDE — **미계상 경로가 있다**(뿌리①② 밖으로 말이 게이트에 닿는다).")
        else:
            print("     ⇒ 잔차 ≈ 0 — 뿌리①② 가 말→게이트 경로를 설명한다(소진).")

    # ── AXIS · 내가 잰 축이 루프가 나르는 축인가 (진단 · 헤드라인 아님) ───────────────
    # 헤드라인의 A = a_fold8 = penult_fold8(pooled) — 입이 **표상한** 축이다.
    # 그런데 루프가 물리적으로 나르는 것은 _afs_byte_feature(g_text, 8) — 평균·분산·고바이트·
    # 공백·숫자·구두점 같은 **8개 바이트-모양 스칼라**다(chat.py:240). 내용은 거기서 이미 버려진다.
    # 두 축이 직교하면, 나는 **루프가 나르지 않는 축**을 재고 "정보가 없다"고 말한 셈이 된다.
    #
    # A′ = penult_fold8(byte_feat8) — 같은 FROZEN reducer(H_9257), 물리적으로 소비되는 입력,
    # 새 자유도 0. bar 도 추가하지 않는다(진단이므로 verdict 불변).
    #
    # A SKIP HERE MUST NOT RETURN. This panel used to `return 0` when gtext_b64 was absent,
    # which silently swallowed every panel below it — the same defect already fixed once when
    # a dead mediation channel ate this very AXIS block. A diagnostic that cannot run is a
    # diagnostic that prints SKIP, not one that ends the readout (convergence evaluate-py-14).
    gt = [r.get("gtext_b64") for r in use]
    Ap = None
    if any(g is None for g in gt):
        print("  ── AXIS: gtext_b64 미기록 ⇒ SKIP (구 trace 포맷)")
    else:
        try:
            import base64
            Ap = [clm.penult_fold8(_im_byte_feat8(
                base64.b64decode(g).decode("utf-8", "surrogateescape"))) for g in gt]
        except Exception as e:  # pragma: no cover
            print("  ── AXIS: SKIP (" + str(e) + ")")
            Ap = None
    if Ap is not None:
        hAp = _im_h_given_S(Ap, S)
        i_axes = _im_cmi(A, Ap, S)
        print("  ── AXIS (진단 · verdict 불변) ──────────────────────────────────")
        print("     A  = penult_fold8(pooled)     — 입이 표상한 축      H(A|S)  = %.4f nats" % hA)
        print("     A′ = penult_fold8(byte_feat8) — 루프가 나르는 축    H(A′|S) = %.4f nats" % hAp)
        print("     I(A;A′|S) = %.4f nats   (두 축이 같은 것을 보는가)" % i_axes)
        if hAp < hfloor:
            print("     ⇒ A′ 자체가 죽어 있다 — 루프 입력이 상수. 축 문제 이전에 경로 문제.")
        elif i_axes < mde:
            print("     ⇒ ⚠️ 두 축이 **거의 직교**하다. 나는 루프가 나르지 않는 축을 쟀다 —")
            print("        헤드라인의 '정보 없음'은 **이 축 위에서만** 벌어진 것이다(축 재선택이")
            print("        아니라, A′ 로 재판독해야 use-claim 이 선다).")
        else:
            print("     ⇒ 두 축이 상당히 겹친다 — 헤드라인 축 선택은 방어된다.")

    # ── COMPOSITION · 사슬이 안 이어붙는가, 아니면 그냥 좁은가 (H_9340 · 사전등록) ──────
    #
    # H_9337 read M1 (A->R) LIVE, M2 (R->Y) LIVE, and A->Y below MDE, and I called that a
    # COMPOSITION FAILURE — "the component the mouth pushes is not the component the gate
    # reads". That is the story I want to be true, and the data I already had ARGUES AGAINST
    # IT. A weak-channel Markov chain predicts multiplicative attenuation:
    #     rho1 ~ sqrt(2*0.0202) = 0.20 · rho2 ~ sqrt(2*0.0902) = 0.42
    #     I_comp ~ 0.5*(rho1*rho2)^2 = 0.0036 nats     vs     I_obs = 0.0061
    # The observation sits ABOVE the composition prediction. A real misalignment would put it
    # BELOW (a mismatched component leaks MORE than the product, not less), and the DPI bound
    # min(0.020, 0.090) = 0.020 is not violated either. The picture is not a contradiction —
    # it is attenuation. So test the chain directly instead of narrating it.
    #
    # Build the COMPOSED channel from the two measured links and ask whether the observed
    # end-to-end MI is what that chain predicts:
    #     p_comp(Y|A,S) = sum_R p(Y|R,S) p(R|A,S)      Delta = I_obs - I_comp
    # Two versions. The 2-bin one uses the same R the headline used. The CONTINUOUS one uses
    # the raw recon_err scalar the trace already carries (logistic p(Y|r,S), then a plug-in
    # Monte-Carlo average over the r's actually observed in each (A,S) cell — no density
    # estimate). Note the continuous version DROPS the binning rather than refining it, so it
    # carries none of the stratum-explosion bias that forced M3 onto a permutation null.
    lan_c = [nxt_lane[(r["_src"], int(r["tick"]))].get("rel_lane") for r in use]
    print("  ── COMPOSITION (H_9340 · 사슬이 안 이어붙는가 vs 그냥 좁은가) ────")

    def _comp_mi(pY_given_R, R_of_i):
        """I_comp(A;Y|S) for the composed channel p(Y|A,S) = E_{R|A,S}[ p(Y|R,S) ]."""
        cell = {}
        for i, a in enumerate(A):
            cell.setdefault((S[i], a), []).append(pY_given_R[i])
        pa_s, ns = {}, {}
        for i, a in enumerate(A):
            pa_s[(S[i], a)] = pa_s.get((S[i], a), 0) + 1
            ns[S[i]] = ns.get(S[i], 0) + 1
        tot = float(len(A))
        out = 0.0
        for s in ns:
            keys = [k for k in cell if k[0] == s]
            if not keys:
                continue
            wsum = float(ns[s])
            pbar = sum(pa_s[k] / wsum * (sum(cell[k]) / len(cell[k])) for k in keys)
            hbar = _im_H_p(pbar)
            hcond = sum(pa_s[k] / wsum * _im_H_p(sum(cell[k]) / len(cell[k])) for k in keys)
            out += (wsum / tot) * (hbar - hcond)
        return out

    def _pY_given_Rbin(idx):
        tab = {}
        for i in idx:
            tab.setdefault((S[i], R[i]), [0, 0])
            tab[(S[i], R[i])][Y[i]] += 1
        return [((tab.get((S[i], R[i]), [1, 1])[1] + 0.5)
                 / (sum(tab.get((S[i], R[i]), [1, 1])) + 1.0)) for i in range(len(A))]

    def _pY_given_Rcont(idx):
        # per-stage logistic on the raw scalar, 200 steps of plain gradient ascent
        out = [0.5] * len(A)
        for s in set(S):
            tr = [i for i in idx if S[i] == s]
            if len(tr) < 10:
                continue
            xs = [rc[i] for i in tr]
            mu = sum(xs) / len(xs)
            sd = (sum((v - mu) ** 2 for v in xs) / len(xs)) ** 0.5 or 1.0
            w = b = 0.0
            for _ in range(200):
                gw = gb = 0.0
                for i in tr:
                    z = w * ((rc[i] - mu) / sd) + b
                    p = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
                    e = Y[i] - p
                    gw += e * ((rc[i] - mu) / sd)
                    gb += e
                w += 0.5 * gw / len(tr)
                b += 0.5 * gb / len(tr)
            for i in range(len(A)):
                if S[i] != s:
                    continue
                z = w * ((rc[i] - mu) / sd) + b
                out[i] = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
        return out

    rc = [float(nxt_lane[(r["_src"], int(r["tick"]))]["recon_err"]) for r in use]
    allidx = list(range(len(A)))
    i_c2 = _comp_mi(_pY_given_Rbin(allidx), R)
    i_cc = _comp_mi(_pY_given_Rcont(allidx), rc)
    print("     I_obs(A;Y|S)      = %.5f nats" % I)
    print("     I_comp [R 2-bin]  = %.5f   Δ = %+.5f" % (i_c2, I - i_c2))
    print("     I_comp [R 연속]    = %.5f   Δ = %+.5f  ← 사전등록 판독축" % (i_cc, I - i_cc))
    print("     (b) 게이트  I_comp[연속] − I_comp[2bin] = %+.5f  (>%.3f 이면 2-bin 이 정보를 버렸다)"
          % (i_cc - i_c2, mde))
    # bootstrap over ROLLOUTS (the exchangeable unit, evaluate-py-13) for a CI on Delta
    src_l = [r["_src"] for r in use]
    roll = sorted(set(src_l))
    byr = {}
    for i, s_ in enumerate(src_l):
        byr.setdefault(s_, []).append(i)
    deltas = []
    for _ in range(200):
        pick = [roll[rnd.randrange(len(roll))] for _ in range(len(roll))]
        idx = [i for r_ in pick for i in byr[r_]]
        Ab = [A[i] for i in idx]; Yb = [Y[i] for i in idx]; Sb = [S[i] for i in idx]
        io = _im_cmi(Ab, Yb, Sb)
        pv = _pY_given_Rcont(idx)
        cell = {}
        for i in idx:
            cell.setdefault((S[i], A[i]), []).append(pv[i])
        cnt = {}
        for i in idx:
            cnt[(S[i], A[i])] = cnt.get((S[i], A[i]), 0) + 1
        nsb = {}
        for i in idx:
            nsb[S[i]] = nsb.get(S[i], 0) + 1
        ic = 0.0
        for s in nsb:
            keys = [k for k in cell if k[0] == s]
            wsum = float(nsb[s])
            pbar = sum(cnt[k] / wsum * (sum(cell[k]) / len(cell[k])) for k in keys)
            ic += (wsum / float(len(idx))) * (
                _im_H_p(pbar) - sum(cnt[k] / wsum * _im_H_p(sum(cell[k]) / len(cell[k])) for k in keys))
        deltas.append(io - ic)
    deltas.sort()
    lo, hi = deltas[int(0.025 * len(deltas))], deltas[int(0.975 * len(deltas)) - 1]
    print("     Δ[연속] 95%% CI (rollout bootstrap) = [%+.5f, %+.5f]" % (lo, hi))
    # ── POWER GATE on the (a)-vs-(c) contrast (BLOCKING) ─────────────────────────────
    # A verdict that cannot be reached is as broken as a guard that cannot fail. Declaring
    # (a) MISALIGNMENT requires I_obs < I_comp - MDE, and mutual information cannot go below
    # zero — so when I_comp itself sits under MDE, (a) is UNREACHABLE BY CONSTRUCTION and the
    # test can only ever land on (c). That is not evidence for (c); it is the bar quietly
    # deciding in advance. Worse, it says something stronger about the whole question: a chain
    # this weak predicts an end-to-end MI BELOW THE INSTRUMENT'S RESOLUTION even when it is
    # PERFECTLY aligned — so the observed A->Y is exactly what a working chain looks like, and
    # there is no "composition failure" left to explain.
    if i_cc < mde:
        print("     ⇒ ⛔ (a)/(c) 판별 **NOT-POWERED** — 합성 예측 자체가 MDE 아래다"
              " (I_comp=%.5f < %.3f)." % (i_cc, mde))
        print("        (a) 는 I_obs < I_comp − MDE 를 요구하는데 상호정보는 음수가 못 된다 ⇒")
        print("        이 bar 로 (a) 는 **원리적으로 도달 불가**. (c) 로만 갈 수 있는 검정이다.")
        print("        더 중요한 함의: **완벽히 정렬된 사슬조차 측정 불가능한 효과를 예측한다.**")
        print("        ⇒ 관측된 A→Y 는 정상 작동하는 약한 사슬이 내놓을 바로 그 값이다.")
        print("        '합성 실패'는 설명할 것이 없다 — 두 링크가 약한 것이 전부다.")
        return 0
    if lo > mde:
        print("     ⇒ 직통로 — R 밖의 A→Y 경로가 있다. M3 소진과 모순 ⇒ L-조건화 재점검.")
    elif hi < -mde:
        print("     ⇒ (a) **정렬 실패 실재** — 실측이 합성 예측보다 유의하게 **낮다**.")
        print("        말이 미는 R 의 성분과 게이트가 읽는 성분이 어긋난다.")
    elif lo > -mde and hi < mde:
        print("     ⇒ (c) **감쇠다 — 합성 실패 아님.** 사슬은 곱셈으로 이어진다, 좁을 뿐.")
        print("        H_9337 의 '정렬 실패' 헤드라인은 **정정된다**.")
    else:
        print("     ⇒ 판정 보류 — CI 가 등가역과 한쪽 꼬리에 걸친다(검정력 부족).")
    return 0


def _im_byte_feat8(s):
    """cli/chat.py::_afs_byte_feature(s, 8) 의 판독-측 쌍둥이 — 루프가 실제로 나르는 8 스칼라.

    데몬은 emit 마다 이 8개(평균·분산·고바이트·저바이트·공백·숫자·구두점·짧은바이트 비율)만
    afield 에 넣는다. 내용은 여기서 소각된다. 판독기가 이 축을 못 보면, '정보가 없다'는 결론은
    기질이 아니라 **내 축 선택**에 관한 것이 된다. reference-match: chat.py:240 과 1:1."""
    b = s.encode("utf-8", "surrogateescape")
    n = len(b)
    if n == 0:
        return [0.0] * 8
    fn = float(n)
    total = sumsq = 0.0
    n_hi = n_low = n_sp = n_dig = n_pun = n_lt64 = 0
    for byte in b:
        bf = float(byte)
        total += bf
        sumsq += bf * bf
        if byte >= 128:
            n_hi += 1
        if byte < 32:
            n_low += 1
        if byte == 32:
            n_sp += 1
        if 48 <= byte <= 57:
            n_dig += 1
        if byte in (33, 44, 46, 58, 59, 63):
            n_pun += 1
        if byte < 64:
            n_lt64 += 1
    mean = total / fn
    var = sumsq / fn - mean * mean
    return [mean / 255.0, var / 65025.0, n_hi / fn, n_low / fn,
            n_sp / fn, n_dig / fn, n_pun / fn, n_lt64 / fn]


_KNOWN_FLAGS = frozenset((
    "--arm", "--bind-locus", "--bl-swap-span", "--bl-swap-donor-class", "--twin-screen", "--twin-necessity", "--delta-pregate", "--delta-control", "--consult", "--consult-format", "--consult-decode", "--consult-decode-win", "--consult-decode-filler", "--corpus", "--dump-hidden", "--earned", "--faction-phi-proxy", "--n-factions-sweep", "--trials", "--arm-random-init", "--faction-block-structure", "--faction-block-provenance", "--faction-lesion", "--faction-lam", "--faction-oracle-pi", "--faction-split", "--gen",
    "--help", "--pc2-direction", "--ag-criticality", "--silence-content-te", "--reach-oracle", "--reach-lag", "--overlap-ngram", "--copy-exclude", "--pool", "--gen-percept-schedule", "--lags", "--reps", "--eval-historicity", "--schedule", "--dv", "--jitter", "--af-forward", "--impulse", "--side", "--kmax", "--timing-channel", "--clock", "--lens", "--butterfly", "--z-census", "--zeta-slope", "--by-loading", "--tost", "--pos-control-beta", "--pos-control", "--atom-census", "--pilot", "--atoms", "--span", "--occupancy", "--rank-null", "--surrogates", "--factor-census", "--stage-slave", "--variance-audit", "--emit-coupling", "--subspace-stability", "--dims", "--block", "--boot", "--surr", "--ground-probe", "--interact-mi", "--gate-deaf", "--gate-census", "--lane-census", "--dead-census", "--refractory-preview", "--emit-gate-census", "--cf-straddle", "--cf-emit", "--cf-seed", "--g-amp-screen", "--audibility", "--g-tension", "--tension-emit", "--psi-soma", "--interaction-lift", "--k-perm", "--kappa", "--kernel", "--kosmos", "--min-occ", "--null",
    "--device-parity", "--n-decode", "--n-sampled", "--valence-audit",
    "--out", "--perm", "--probe", "--seed",
    "--result-file", "--collide-select", "--pregate", "--pregate-cond", "--k", "--rho-axon", "--rho-axon-isolated", "--rho-cache", "--rho-axes", "--rho-no-cells", "--rho-out", "--route-audit", "--score-len", "--seeds", "--selftest-rho-cells",
    "--slot-off",
    "--fan-branch", "--branches",              # H_9803 branch-latent ideation fan arms
    "--tension-rank-audit", "--ctrl-seed",     # H_9805 write-side tension-field rank audit
    "--bind-panel", "--max-items",             # H_9810 held-out binding panel d_acc scorer
    "--slot-shuffle", "--surface-set", "--system-g1", "--vs", "--win", "--with-logits", "--xbind", "--xfan",
    "--gn-freeze",
    "--bridge-trace", "--flip0", "--theta",
    "--store-mix", "--store-lambda", "--manifest",
    "--store-component-swap", "--store-swap-from",
    "--store", "--store-oracle",
    "--store-shuffle", "--store-flip", "--store-neutral", "--store-ctrl-seed",
    "--store-addr-audit", "--store-telemetry", "--weave-null", "--grow-window", "--seed-class", "--fan-temp-ladder", "--seed-offset",
    "--store-query", "--store-fuse", "--store-readout",
    "--store-addr-census", "--store-census-selftest", "--census-seeds",
    "--store-retr-probe", "--retr-probe-selftest", "--retr-probe-iters",   # H_9825 retrieval ceiling
    "--retr-probe-center", "--retr-probe-nway",              # H_9825 deconfound · live-lane re-read
    "--store-parity-selftest", "--parity-tol",              # H_9826 torch<->numpy CLMS parity
    # H_9838 CA3 multi-step transitive completion (core/hippo_lane.py · ckpt-free · read-side)
    "--hippo-transitive-selftest", "--hippo-hops", "--hippo-kwta-k", "--hippo-seed",
    "--hippo-dim", "--hippo-active", "--hippo-chains", "--hippo-chain-len",
    "--fan-bind", "--fan-smp",
    "--mouth-binder", "--mouth-binder-order-scramble",
    "--fan-dump",
    "--cascade-null",
    "--state-census", "--kmax",
    "--decl-flip", "--arms", "--strata",          # H_9800 ephemeral-declaration grounding
    "--tension-concord",                          # H_9812 lex|class concord mode for the audit
    "--closure-ladder", "--closure-arm", "--closure-ticks", "--closure-seed",   # H_9807 interventional closure rung 1
    "--stream-mi", "--shuffle-floor",             # H_9806 compression-MI battery (core/mi_compress)
    "--capture-anchor", "--n-segments",           # H_9806 shift-null LOO capture
    # H_9808 $0 PRE-REGISTRATION GATES (core/pregates.py) — closed-form referees that ABORT
    # BEFORE SPEND. Each returns exit 3 on REFUSE, 0 on PASS, 2 on a malformed spec.
    "--falsifier-headroom", "--free-slot-score", "--register-leak-probe",
    "--pregate-bar", "--pregate-out", "--pregate-selftest",
    # H_9824 G6 corpus data-wall census (read-only · no decode)
    "--falsi-census", "--falsi-max-sent", "--falsi-out",
    # H_9825 parametric ρ·weave panel (the n=12 instrument fix · default-off = byte-identical)
    "--weave-panel",
    # H_9829 continuous ρ·fan falsifiability rate (REPORTED ONLY · default 0 = byte-identical)
    "--fan-draws",
    "--leak-bar", "--leak-eps", "--leak-nmax",
))


def _z_census(argv):
    """H_9712 z-DOSE STARVATION CENSUS — the $0 gate that must clear BEFORE H_9576's
    direction null (rho=-0.077) may be read as a wall rather than a dose artefact.

    `anima-py evaluate --pc2-direction <traces_dir> --z-census`

    H_9576 fired at gain=1 calling it "the log-prob natural unit". That was an ASSUMPTION,
    never a measurement. Its causal chain is 3 links —
        z (intended meaning) →① physical effect (context-byte logit penalty)
                             →② proximal observable (context-byte share of the output)
                             →③ remote readout D (bigram-seed overlap)
    — and H_9576 measured only z→③, with a positive control on no link. rho≈0 does not say
    WHICH link broke. This census certifies links ① and ② from the traces alone (no decode).

    Three sections, each with its own controls:

      (0) z distribution — var · IQR · |z|95 · route_k (deliberation_k) census.
      (1) EXPOSURE (the INVALID-EXPOSURE gate) — core/decode.py:2097 applies the bias on the
          lm-branch ONLY; a grounded anchor-copy step never reaches it. So the effective dose
          is z × (that tick's lm-step count), and a tick with 0 lm-steps is UNEXPOSED. The
          trace records no lm counter — but the rng arm is a POSITIVE CONTROL for exposure:
          it re-keys `seed_rng`, which core/decode.py:2078 feeds ONLY to _mouth_sample_row,
          which is called ONLY on the lm branch. Hence rng-divergence ⟹ that tick had ≥1
          lm-step. 1 − (rng diverged / rng total) is a rigorous UPPER BOUND on the
          lm-step=0 fraction. Bar (frozen): >30% ⇒ INVALID-EXPOSURE.
      (2) DOSE — the pre-registered zeta-half (argmax-flip-50% dose) is NOT computable here:
          it needs the per-step posterior, which the traces do not carry, and the live mouth
          is a temp=1.0 SAMPLER (emit_temp), not an argmax — so "argmax-flip" is not even the
          running mechanism. Per the card's own contingency (a) this reports the honest
          trace-computable surrogate instead, and prints the limits.
          SURROGATE pi-dose: the mechanism's physical claim is context-presence — z is
          SUBTRACTED from every byte in the model's own T=24 window, so z<0 BOOSTS in-window
          bytes (pulls toward context) and z>0 pushes off-context. At the first byte where
          steered diverges from base, rebuild that window from (seed ++ base[:i]) and ask
          whether the chosen byte is IN it. pi_base = P(base byte ∈ window) is the unbiased
          pedestal drawn at the SAME position (paired), so the contrast is within-position.
          Predicted sign is fixed a priori by the sign of mean z, not by the data.
          Controls: (i) the arm's own base draw (paired pedestal) (ii) the rng arm, same |z|,
          draw-stream re-key only, no logit change ⇒ its Delta-pi must be ≈0. Each control is
          reported SEPARATELY against the experiment — never Delta=exp−max(controls), which is
          an order-statistic bias that manufactures KILLs (probe-defect-census-max-control-bias).
          Test = exact two-sided McNemar on the discordant pairs (paired binary), plus the
          resolvable |Delta-pi| so an underpowered null reads VOID, not negative.

    Frozen bars (card H_9712 · do not retune): |z|95 ≥ zeta-half ⇒ PASS-DOSED · |z|95 <
    zeta-half/4 ⇒ VOID-STARVED (H_9576 reclassified) · between ⇒ PENDING · lm-step=0 fraction
    >30% ⇒ INVALID-EXPOSURE · calibration self-consistency FAIL ⇒ INVALID.
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import math as _pm

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --z-census")
        return 2

    # Mirrors core/decode.py::clm_decode_grounded — the CLM causal window the bias acts on.
    _T = 24

    def _rows(arm, sd):
        p = os.path.join(d, "%s_s%d.jsonl" % (arm, sd))
        if not os.path.exists(p):
            return []
        out = []
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if not r.get("_meta"):
                out.append(r)
        return out

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    seeds = []
    for f in sorted(_glob.glob(os.path.join(d, "off_s*.jsonl"))):
        try:
            seeds.append(int(os.path.basename(f)[len("off_s"):-len(".jsonl")]))
        except ValueError:
            continue
    if not seeds:
        print("  ⇒ ⛔ no off_s<seed>.jsonl traces under " + d)
        return 2

    def _quant(v, p):
        if not v:
            return 0.0
        s = sorted(v)
        i = p * (len(s) - 1)
        lo = int(i)
        hi = min(lo + 1, len(s) - 1)
        return s[lo] * (1.0 - (i - lo)) + s[hi] * (i - lo)

    def _mcnemar_p(b01, b10):
        """Exact two-sided McNemar (binomial on the discordant pairs)."""
        n = b01 + b10
        if n == 0:
            return 1.0
        k = min(b01, b10)
        tail = sum(_pm.comb(n, i) for i in range(0, k + 1)) / float(2 ** n)
        return min(1.0, 2.0 * tail)

    print("=== anima evaluate --pc2-direction --z-census — z DOSE/EXPOSURE (card H_9712) ===")
    print("traces: %s  (seeds: %s)" % (d, ",".join(str(s) for s in seeds)))
    print("chain:  z →① logit penalty on in-window bytes →② context share →③ D (H_9576 read ③ only)")
    print("bar:    |z|95≥ζ½ PASS-DOSED · |z|95<ζ½/4 VOID-STARVED · lm-step=0 >30% INVALID-EXPOSURE")
    print("")

    # ── (0) live z distribution ──────────────────────────────────────────────
    zs, rks, temps = [], {}, set()
    for sd in seeds:
        for r in _rows("bias", sd):
            if not r.get("emit") or r.get("pc2_z") is None:
                continue
            zs.append(float(r["pc2_z"]))
            rk = r.get("route_k")
            rks[rk] = rks.get(rk, 0) + 1
            if r.get("emit_temp") is not None:
                temps.add(round(float(r["emit_temp"]), 4))
    if len(zs) < 3:
        print("  ⇒ ⛔ VOID — n=%d live z samples is unreadable (power-before-negative)." % len(zs))
        return 0
    mean = sum(zs) / len(zs)
    var = sum((v - mean) ** 2 for v in zs) / (len(zs) - 1)
    az = [abs(v) for v in zs]
    z95 = _quant(az, 0.95)
    iqr = _quant(zs, 0.75) - _quant(zs, 0.25)
    npos = sum(1 for v in zs if v > 0)
    print("  (0) live z   n=%d  mean=%+.4f  var=%.6f  sd=%.4f" % (len(zs), mean, var, var ** 0.5))
    print("      |z|95=%.4f  IQR=%.4f [%+.4f,%+.4f]  min=%+.4f max=%+.4f"
          % (z95, iqr, _quant(zs, 0.25), _quant(zs, 0.75), min(zs), max(zs)))
    print("      sign split: z>0 %d · z<=0 %d   route_k(deliberation_k)=%s   emit_temp=%s"
          % (npos, len(zs) - npos,
             ",".join("%s:%d" % (k, v) for k, v in sorted(rks.items(), key=lambda x: str(x[0]))),
             ",".join(str(t) for t in sorted(temps)) or "n/a"))
    # z is subtracted from in-window bytes (core/decode.py:2100-2104): z<0 ⇒ in-window BOOSTED.
    pred_up = mean < 0
    print("      ⇒ mechanism (decode.py:2100 row[v]-=z) predicts Δπ %s at this z sign"
          % ("> 0 (pull TOWARD context)" if pred_up else "< 0 (push OFF context)"))
    print("")

    # ── (1) exposure census — the INVALID-EXPOSURE gate ──────────────────────
    def _diverge(arm):
        nd, nt, firsts = 0, 0, []
        for sd in seeds:
            for r in _rows(arm, sd):
                if not r.get("emit"):
                    continue
                b, s = _b64(r.get("gtext_b64")), _b64(r.get("gtext_pc2_b64"))
                if not s:
                    continue
                nt += 1
                i = next((k for k in range(min(len(b), len(s))) if b[k] != s[k]), -1)
                if i < 0 and len(b) != len(s):
                    i = min(len(b), len(s))
                if i >= 0:
                    nd += 1
                    firsts.append(i)
        return nd, nt, firsts

    rnd, rnt, rfirst = _diverge("rng")
    bnd, bnt, bfirst = _diverge("bias")
    lm0 = (1.0 - (rnd / float(rnt))) if rnt else 1.0
    print("  (1) exposure — rng re-keys seed_rng, read ONLY by _mouth_sample_row on the lm branch")
    print("      ⇒ rng diverged %d/%d ⟹ that many emit ticks provably had ≥1 lm-step"
          % (rnd, rnt))
    print("      ⇒ lm-step=0 fraction ≤ %.4f (%.2f%%)   bar >30%% ⇒ INVALID-EXPOSURE  ⇒ %s"
          % (lm0, 100.0 * lm0, "INVALID-EXPOSURE" if lm0 > 0.30 else "CLEARED"))
    if bfirst and rfirst:
        print("      first-divergence byte index: bias mean=%.2f med=%.1f min=%d · rng mean=%.2f med=%.1f min=%d"
              % (sum(bfirst) / len(bfirst), _quant(bfirst, 0.5), min(bfirst),
                 sum(rfirst) / len(rfirst), _quant(rfirst, 0.5), min(rfirst)))
        print("      ⇒ NOTE: tick-divergence is SATURATED in BOTH arms (rng too) ⇒ zero")
        print("        discriminative power as a dose readout — Δ vs control ≈ 0 (p7).")
    if lm0 > 0.30:
        print("")
        print("  ⇒ VERDICT: ⛔ INVALID-EXPOSURE — the anchor-copy path starves the channel;")
        print("     dose is not the question yet, and H_9576's null is unreadable either way.")
        return 0
    print("")

    # ── (2) dose — zeta-half unmeasurable ⇒ card contingency (a): pi-dose surrogate ──
    print("  (2) ζ½ (argmax-flip-50% dose) — NOT COMPUTABLE from these traces:")
    print("      · no per-step posterior/logit-gap field exists in the trace schema, and")
    print("      · emit_temp=1.0 ⇒ the live mouth SAMPLES; 'argmax-flip' is not the running")
    print("        mechanism at all. Card contingency (a) ⇒ honest surrogate below.")
    print("      ⇒ literal ζ½ cells (PASS-DOSED/VOID-STARVED) are UNADJUDICABLE here.")
    print("")
    print("  (2) surrogate π-dose = P(chosen byte ∈ own T=%d window) at first divergence" % _T)

    res = {}
    for arm in ("bias", "rng"):
        n = b01 = b10 = nb = ns = 0
        for sd in seeds:
            for r in _rows(arm, sd):
                if not r.get("emit"):
                    continue
                base_b, st_b = _b64(r.get("gtext_b64")), _b64(r.get("gtext_pc2_b64"))
                sd_b = _b64(r.get("seed_b64"))
                if not st_b or not sd_b:
                    continue
                i = next((k for k in range(min(len(base_b), len(st_b)))
                          if base_b[k] != st_b[k]), -1)
                if i < 0:
                    continue
                win = set((sd_b + base_b[:i])[-_T:])
                bi, si = base_b[i] in win, st_b[i] in win
                n += 1
                nb += 1 if bi else 0
                ns += 1 if si else 0
                if (not bi) and si:
                    b01 += 1
                elif bi and (not si):
                    b10 += 1
        if n == 0:
            print("      %-4s n=0 — no divergent tick to read (VOID)" % arm)
            continue
        pb, ps = nb / float(n), ns / float(n)
        p = _mcnemar_p(b01, b10)
        mde = 1.96 * ((b01 + b10) ** 0.5) / float(n)
        res[arm] = {"n": n, "pb": pb, "ps": ps, "d": ps - pb, "p": p, "mde": mde}
        print("      %-4s n=%-4d π_base=%.4f → π_steer=%.4f  Δπ=%+.4f  "
              "(discordant %d↑/%d↓ · exact McNemar p=%.4f · resolvable |Δπ|≈%.3f)"
              % (arm, n, pb, ps, ps - pb, b01, b10, p, mde))
    if "bias" not in res or "rng" not in res:
        print("  ⇒ ⛔ VOID — an arm carried no divergent tick; the contrast is unreadable.")
        return 0
    b, rg = res["bias"], res["rng"]
    print("      controls reported SEPARATELY (never Δ=exp−max(ctrl) · order-statistic bias)")
    print("        ctrl-i  paired base pedestal (same position, unbiased draw) — inside each row")
    print("        ctrl-ii rng arm: same |z|, draw re-key, NO logit change ⇒ Δπ must be ≈0")
    print("")

    # ── (3) positive controls ────────────────────────────────────────────────
    print("  (3) positive controls")
    print("      PC-a exposure: rng is a KNOWN-LIVE lm-branch perturbation — %s (%d/%d diverged)"
          % ("LIVE" if rnd > 0 else "DEAD", rnd, rnt))
    print("      PC-b sign-split: mechanism predicts Δπ REVERSES for z>0 vs z<0 — "
          "n(z>0)=%d ⇒ %s" % (npos, "VOID (underpowered · power-before-negative)"
                              if npos < 20 else "readable"))
    print("      PC-c calibration (ζ=ζ½ ⇒ flip≈50%): NOT-RUN (ζ½ unmeasurable) — NOT a FAIL")
    print("")

    # ── verdict ──────────────────────────────────────────────────────────────
    sig = b["p"] < 0.05
    right_sign = (b["d"] > 0) if pred_up else (b["d"] < 0)
    rng_null = rg["p"] >= 0.05
    print("  ⇒ VERDICT (literal ζ½ axis): 🟡 PENDING-BY-INSTRUMENT — ζ½ needs the per-step")
    print("     posterior; these traces do not carry it (see FOLLOW-ON below).")
    if sig and right_sign and rng_null:
        v = ("🟢 PASS-DOSED (SURROGATE) — the live z DOES physically move the mouth in the\n"
             "     direction the mechanism predicts (Δπ=%+.4f · p=%.4f), while the rng control\n"
             "     is null (Δπ=%+.4f · p=%.4f). Link ①→② is LIVE and dosed ⇒ the dose-starvation\n"
             "     claim of H_9712 DIES, and H_9576's null is NOT rescued by starvation."
             % (b["d"], b["p"], rg["d"], rg["p"]))
    elif sig and (not right_sign) and rng_null:
        v = ("🔴 SIGN-INVERTED — Δπ=%+.4f is significant but OPPOSITE the mechanism's own\n"
             "     prediction ⇒ the implemented bias is not doing what decode.py:2100 claims."
             % b["d"])
    elif not rng_null:
        v = ("⛔ INVALID — the rng control is NOT null (Δπ=%+.4f · p=%.4f): a draw-stream re-key\n"
             "     alone moves π, so the bias arm's Δπ is not attributable to z."
             % (rg["d"], rg["p"]))
    elif b["mde"] > abs(b["d"]):
        v = ("🟡 VOID-UNDERPOWERED — |Δπ|=%.4f sits under the resolvable %.3f at n=%d;\n"
             "     a starved dose stays UNMEASURED, not demonstrated (power-before-negative)."
             % (abs(b["d"]), b["mde"], b["n"]))
    else:
        v = ("🧱 SURROGATE-STARVED — the live z does NOT move the proximal observable\n"
             "     (Δπ=%+.4f · p=%.4f) though exposure is cleared ⇒ H_9576 reads VOID-STARVED\n"
             "     and a gain sweep g∈{2,4,8} is justified." % (b["d"], b["p"]))
    print("  ⇒ VERDICT (surrogate π-dose axis): " + v)
    print("")
    print("  LIMITS (honest scope · a_scale_honest_scope)")
    print("     · π-dose reads the FIRST divergent step ONLY: past it the two arms' contexts")
    print("       differ, so every later step is incomparable. This bounds link ①→② at one")
    print("       step, not over the whole utterance.")
    print("     · it certifies the PHYSICAL effect, NOT the semantics — a live ①→② says")
    print("       nothing about whether PC2's MEANING survives to ③ (that is H_9576's null).")
    print("     · surrogate ≠ the pre-registered ζ½ cell: DIRECTIONAL, not a ζ½ verdict.")
    print("  FOLLOW-ON (to close the literal ζ½ cell · card contingency (b))")
    print("     · needs a posterior-gap recorder on the decode path (e.g. an `anima-py chat`")
    print("       flag logging per-lm-step top-2 logit gap + in-window mass), then a ζ sweep.")
    print("     · 303M decode is POOL-only (summer/aiden), never mini (heavy-anima-eval-pool-not-mini).")
    return 0


def _content_sig_factory(b64_list):
    """POPULATION-RELATIVE 2-bit content signature (equal-frequency binning · researcher DOF = 0).

    Replaces an absolute char-class argmax that DIED on real text: every natural-English candidate
    is lowercase-dominant, so 29 DISTINCT 303M candidates collapsed to ONE address (measured
    2026-07-17 on a 60-tick sampled wm-dual trace: lower med 0.688 vs dig 0.050 / upper 0.050 /
    pun 0.044 ⇒ argmax ≡ lower ⇒ dead alphabet ⇒ every reader read NOT-POWERED). The absolute
    form only discriminated the synthetic oracle (digit-vs-punct), which is exactly the trap
    `positive-control-before-reading-a-negative` warns about: a control the instrument passes
    while the real distribution saturates it.

    Fix: split each feature at the MEDIAN of the trace's OWN population — bins are balanced by
    construction on whatever distribution actually shows up, and there is no threshold to tune.
    Features are the two with live spread on natural text (digit-fraction · lowercase-fraction).
    The surrogate null re-uses the SAME binning, so the data-dependent split cannot manufacture
    signal (it shifts real and null together)."""
    import base64 as _b64f, statistics as _stf

    def _feats(b64s):
        if not b64s:
            return None
        try:
            bs = _b64f.b64decode(b64s)
        except Exception:
            return None
        n = len(bs)
        if n == 0:
            return None
        dig = sum(1 for x in bs if 48 <= x <= 57) / n
        low = sum(1 for x in bs if 97 <= x <= 122) / n
        return (dig, low)

    pop = [f for f in (_feats(b) for b in b64_list) if f is not None]
    if len(pop) < 4:
        return (lambda _b: -1)
    md = _stf.median([p[0] for p in pop])
    ml = _stf.median([p[1] for p in pop])

    def _sig(b64s):
        f = _feats(b64s)
        if f is None:
            return -1
        return (2 if f[0] > md else 0) + (1 if f[1] > ml else 0)
    return _sig


def _timing_channel(argv):
    """`anima-py evaluate --timing-channel <traces...> [--perm 1000] [--seed 12345]
       [--clock <clock-trace>] [--lens hold|iei] [--schedule <gen-percept-schedule jsonl>]`
       — H_9731 TIMING-CHANNEL ($0 · read-only re-analysis · no producer).

    H_9796 `--schedule` mode: instead of the population content-sig, C = the byte-multiset-CONTROLLED
    probe kind repeat(0)/shuffle(1) at the probe tick — the clean order-only label the archival feat8
    signature lacked. Gated to the immune-margin regime (trace _meta g_reach ∈ d1/affinity); a wm-dual
    coverage-gate trace is REFUSED (order-blind by construction = H_9731 KILL scope). CMI>0 ⟹ percept
    order reached emit timing via the order-sensitive immune_memory_recall_margin_text store (echo-mediated).

    Does the OBSERVABLE emit TIMING carry the identity of the WITHHELD content? emit⟺S>E is a
    content-ledger comparison, so WHEN the daemon speaks is set by WHAT it withheld — an honest
    reopening of the mouth-content wall (H_9576) as a TIMING channel (not bytes · Fable). $0: reads
    existing wm-dual traces (H_9627 · dual_margin/emit/stage/cand_pregate_b64) — no injection, no rewire.

    Source  T_t = OBSERVABLE emit latency (ticks from a silence tick to the NEXT emit), binned
            short/long at the pooled median. NOT dual_margin itself: dual_margin=S−E is content-derived,
            so MI(margin;content) is a tautology — the observable emit gap is a THRESHOLDED (lossy)
            function of it, and MI(gap;content) measures how much content survives into the observable
            WHEN. That distinction is the whole honesty of this instrument.
    Target  C_t = 2-bit dominant-char-class signature of the withheld content (cand_pregate_b64[t]).
    MI = I(T ; C | stage) plug-in (bits). timing carries content ⟺ MI > clock-pedestal ∧ MI > surr95.

    Controls: --clock <trace> = a clock-gated trace (emit clock-driven ⇒ timing content-independent ⇒
      truth-0 PEDESTAL) · content-shuffle surrogate (circular-shift C, preserves the timing/spring
      structure, destroys the content link ⇒ MI collapses if real). Self-test: planted C≡T must recover.

    ⚠️ DIRECTIONAL · toy ≠ verdict (a_scale_honest_scope) · real read = H_9627 303M wm-dual traces
    (if archived, truly $0; else a small wm-dual collection · measurement-only, no owner fire-go)."""
    import glob as _glob, base64 as _b64, math as _m, random as _random, json as _json
    globs = [a for a in argv if not a.startswith("--")]
    def _iv(flag, d):
        for i, a in enumerate(argv):
            if a == flag and i + 1 < len(argv):
                try:
                    return int(argv[i + 1])
                except Exception:
                    return d
        return d
    def _sv(flag, d):
        for i, a in enumerate(argv):
            if a == flag and i + 1 < len(argv):
                return argv[i + 1]
        return d
    perm = _iv("--perm", 1000)
    seed = _iv("--seed", 12345)
    clock_path = _sv("--clock", "")
    # --lens hold (default · byte-identical) = silence→next-emit latency vs the WITHHELD content.
    # --lens iei = inter-emit interval vs the content of the emission that ENDS the gap. The hold lens
    # conditions on silence and is BLIND to emit→emit doublets — and on the 303M seed7 trace ALL of the
    # timing entropy lived there (hold H=0 vs inter-emit H=0.6374). A hold-lens null is scoped to the
    # HOLD channel only; the iei lens is what reads the surviving channel (H_9731 card · Fable∥Sol).
    lens = _sv("--lens", "hold")
    if lens not in ("hold", "iei"):
        print("  ⇒ ⛔ --lens: only 'hold' (default) or 'iei' (got %r)" % lens)
        return 2
    # H_9796 · --schedule <gen-percept-schedule jsonl>: when set, C = the byte-multiset-CONTROLLED probe
    # kind repeat(0)/shuffle(1) at the probe tick, NOT the population content-sig. This is the clean 3-arm
    # ground-truth label the archival feat8 signature LACKED (evaluate-py-23 single-address collapse). Only
    # legitimate in the immune-margin regime (--g-reach d1/affinity): repeat vs shuffle differ ONLY in byte
    # ORDER, which is invisible to the feat8 wm-dual coverage gate (⟹ H_9731 KILL) but visible to the
    # order-sensitive immune_memory_recall_margin_text store. CMI>0 ⟹ percept order reaches emit timing.
    sched_path = _sv("--schedule", "")
    globs = [g for g in globs if g not in (clock_path, sched_path)]
    _sched = {}
    if sched_path:
        for _ln in open(sched_path, encoding="utf-8", errors="surrogateescape"):
            _ln = _ln.strip()
            if not _ln or not _ln.startswith("{"):
                continue
            try:
                _r = _json.loads(_ln)
            except Exception:
                continue
            _sched[int(_r["tick"])] = (_r.get("kind"), int(_r.get("lag", 0)))
    paths = []
    for g in globs:
        paths.extend(sorted(_glob.glob(g)))
    print("═══ H_9731 TIMING-CHANNEL · does OBSERVABLE emit timing carry the WITHHELD content? ═══")
    print("  traces=%d · perm=%d · seed=%d · lens=%s%s"
          % (len(paths), perm, seed, lens, (" · clock-pedestal=%s" % clock_path.split("/")[-1]) if clock_path else ""))
    if sched_path:
        print("  H_9796 · --schedule ON : C = probe kind repeat(0) vs shuffle(1) [byte-multiset-controlled,"
              " order-only] · CMI(hold-latency ; kind | stage) · valid only in immune-margin regime (g_reach"
              " d1/affinity) · novel arm excluded (byte-stats = dead H_9576 lane)")
    elif lens == "iei":
        print("  lens=iei : T = inter-emit gap · C = content of the emission ENDING the gap · ⚠️ a PASS reads"
              " 'the gap preceding an emission carries its content', NOT 'the daemon delays to signal'")

    # signature = POPULATION-RELATIVE (_content_sig_factory · built per-trace from that trace's own
    # candidates). The absolute char-class argmax it replaces read ONE address for every natural-English
    # candidate (lowercase always dominant) = dead alphabet on real 303M data (convergence evaluate-py-23).

    def _cmi(triples):
        # I(T ; C | S) plug-in (bits) — triples = (t, c, s)
        from collections import Counter as _C
        j = _C(); tc_no = _C(); cs = _C(); ts = _C(); sc = _C()
        for (t, c, s) in triples:
            j[(t, c, s)] += 1
            cs[(c, s)] += 1
            ts[(t, s)] += 1
            sc[s] += 1
        n = max(1, sum(j.values()))
        mi = 0.0
        for (t, c, s), cnt in j.items():
            p = cnt / n
            p_tc_s = cnt / cs[(c, s)]          # P(T | C,S)
            p_t_s = ts[(t, s)] / sc[s]          # P(T | S)
            if p_tc_s > 0 and p_t_s > 0:
                mi += p * _m.log2(p_tc_s / p_t_s)
        return max(0.0, mi)

    def _build_iei(rows):
        # (T,C,S) on consecutive EMIT pairs — the lens the hold lens is BLIND to.
        # T = inter-emit interval (e_{k+1} − e_k) binned at the population median · C = content sig of
        # the LATER emit's pre-gate candidate (the one that ENDS the gap) · S = stage wake(0)/sleep(1).
        #
        # Why this exists (measured 2026-07-17, 303M seed7·60tick): the hold lens conditions on SILENCE
        # and therefore cannot see emit→emit doublets. That trace had EE=5 ES=27 SE=27 SS=0 — every
        # silence was followed by an emit, so hold latency was the constant 1 (H=0) — but the inter-emit
        # gap distribution was {2:26, 1:5} ⟹ **H=0.6374 bits ≠ 0**. ALL of the surviving timing entropy
        # sits in the 5 spring-violation doublets that the hold lens is blind to by construction. Two
        # independent sessions both measured only the hold lens and both read "no timing channel" — that
        # verdict is therefore scoped to the HOLD channel, not to the timing stream (H_9731 card).
        #
        # ⚠️ Interpret with the pre-registered caveat (Sol): T's variation here may come entirely from
        # double-emits rather than delayed release — a PASS means "the gap that precedes an emission
        # carries its content", NOT "the daemon delays to signal". Condition on stage; the surrogate
        # shuffles C within the same binning so the median split cannot manufacture signal.
        _sig = _content_sig_factory([(r.get("cand_pregate_b64", "") or r.get("cand_b64_diag", "")) for r in rows])
        emit_ticks = [i for i, r in enumerate(rows) if str(r.get("emit")).lower() == "true"]
        raw = []
        for k in range(len(emit_ticks) - 1):
            i, j = emit_ticks[k], emit_ticks[k + 1]
            c = _sig(rows[j].get("cand_pregate_b64", "") or rows[j].get("cand_b64_diag", ""))
            if c < 0:
                continue
            st = int(rows[j].get("stage", 0))
            raw.append((j - i, c, 1 if st >= 3 else 0))
        if not raw:
            return []
        # T = the RAW gap, capped at 3+ (states {1,2,3+} → {0,1,2}) — Sol's pre-registration
        # "T_IEI ∈ {1,2,…}", NOT a median split. A median split COLLAPSES here by construction and the
        # bug is not hypothetical: on the real gap distribution {2:26, 1:5} the median IS 2, so `g > med`
        # is never true and every gap lands in one bin — the lens would read bins=1 and look exactly like
        # the blind hold lens while the channel (H=0.637) sat right there. Caught by the EE=5 synthetic.
        # The gap alphabet is naturally tiny, so it needs no data-dependent binning at all (DOF 0).
        return [(min(g, 3) - 1, c, s) for (g, c, s) in raw]

    def _build(rows):
        # (T,C,S) on silence ticks: T = latency-to-next-emit binned short/long at median; C = withheld
        # content sig; S = stage wake(0)/sleep(1). C's quantizer is built from THIS trace's own candidate
        # population (median splits) — an absolute threshold saturates on natural text (evaluate-py-23).
        _sig = _content_sig_factory([(r.get("cand_pregate_b64", "") or r.get("cand_b64_diag", "")) for r in rows])
        emit_ticks = [i for i, r in enumerate(rows) if str(r.get("emit")).lower() == "true"]
        raw = []
        for i, r in enumerate(rows):
            if str(r.get("emit")).lower() == "true":
                continue  # silence ticks only (the withheld ones)
            nxt = next((e for e in emit_ticks if e > i), None)
            if nxt is None:
                continue
            c = _sig(r.get("cand_pregate_b64", "") or r.get("cand_b64_diag", ""))
            if c < 0:
                continue
            st = int(r.get("stage", 0))
            s = 1 if st >= 3 else 0   # sleep (N2/N3/REM = 3/4) vs wake
            raw.append((nxt - i, c, s))
        if not raw:
            return []
        lats = sorted(x[0] for x in raw)
        med = lats[len(lats) // 2]
        return [(1 if lat > med else 0, c, s) for (lat, c, s) in raw]

    def _build_sched(rows):
        # H_9796 · hold-latency vs SCHEDULE kind (byte-multiset-controlled label). For each PROBE SILENCE
        # tick whose schedule kind is repeat/shuffle: T = latency-to-next-emit (median split), C = 0 repeat
        # / 1 shuffle, S = stage. novel excluded (byte-stats arm = dead H_9576). Emit probe ticks excluded
        # (0-latency). repeat and shuffle differ ONLY in byte order ⟹ CMI>0 ⟹ percept ORDER reached the
        # emit-hold decision (only possible via an order-sensitive gate — the immune-margin regime).
        emit_ticks = [i for i, r in enumerate(rows) if str(r.get("emit")).lower() == "true"]
        raw = []
        for i, r in enumerate(rows):
            t = r.get("tick")
            if t is None:
                continue
            sk = _sched.get(int(t))
            if sk is None or sk[0] not in ("repeat", "shuffle"):
                continue
            if str(r.get("emit")).lower() == "true":
                continue                       # silence probes only (hold latency)
            nxt = next((e for e in emit_ticks if e > i), None)
            if nxt is None:
                continue
            st = int(r.get("stage", 0))
            raw.append((nxt - i, 0 if sk[0] == "repeat" else 1, 1 if st >= 3 else 0))
        if not raw:
            return []
        # T = RAW hold-latency capped at 3+ (states {1,2,3+}), NOT a median split. A median split COLLAPSES
        # when the latency alphabet is tiny (the exact _build_iei bug: on {1,3} the median is 3, so `lat>med`
        # is never true and every probe lands in one bin = timing bins=1). The hold-latency alphabet is
        # naturally small, so it needs no data-dependent binning (DOF 0 · caught by the planted synth test).
        return [(min(lat, 3), c, s) for (lat, c, s) in raw]

    def _bld(rows):
        # dispatch: schedule-kind label (H_9796) · iei-gap (H_9731 iei lens) · hold-latency (default)
        if sched_path:
            return _build_sched(rows)
        return _build_iei(rows) if lens == "iei" else _build(rows)

    def _surr(triples, rng):
        # circular-shift the C column (excl 0,±1) — preserves T,S marginals + timing structure
        cs = [t[1] for t in triples]
        m = len(cs)
        if m < 5:
            return 0.0
        sh = rng.randrange(2, m - 1)
        cs2 = cs[-sh:] + cs[:-sh]
        return _cmi([(triples[i][0], cs2[i], triples[i][2]) for i in range(m)])

    # estimator self-test (planted C≡T recovers · independent ~0)
    _st = _random.Random(seed ^ 0x9731)
    planted = [((t := _st.randrange(2)), t, _st.randrange(2)) for _ in range(400)]
    indep = [(_st.randrange(2), _st.randrange(2), _st.randrange(2)) for _ in range(400)]
    mi_p = _cmi(planted); mi_i = _cmi(indep)
    est_ok = mi_p > 0.4 and mi_i < 0.1
    print("  estimator self-test : planted I(T;C|S)=%.3f (want>0.4) · independent=%.3f (want<0.1) ⇒ %s"
          % (mi_p, mi_i, "✅ live" if est_ok else "❌ DEAD-ESTIMATOR"))

    def _load(p):
        rows = []; meta = {}
        for ln in open(p, encoding="utf-8", errors="surrogateescape"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = _json.loads(ln)
            except Exception:
                continue
            if isinstance(r, dict) and r.get("_meta"):
                meta = r
            elif isinstance(r, dict) and "tick" in r:
                rows.append(r)
        return rows, meta

    # clock pedestal (truth-0): a clock-gated trace's timing is content-independent by construction
    pedestal = 0.0
    if clock_path:
        crows, _ = _load(clock_path)
        ct = _bld(crows)
        pedestal = _cmi(ct) if len(ct) >= 12 else 0.0
        print("  clock PEDESTAL (truth-0) : I(T;C|S)=%.4f  [%d silence transitions]" % (pedestal, len(ct)))

    if not paths:
        print("  ⇒ ⛔ no traces matched: %r  (wm-dual: chat --g-reach wm-dual --record-silent-cand)" % globs)
        return 2 if est_ok else 3
    rng = _random.Random(seed)
    any_pass = False
    for p in paths:
        rows, meta = _load(p)
        if meta.get("emit_gate") == "clock":
            print("  · %s ⇒ (clock trace — use as --clock pedestal, not an exp arm)" % p)
            continue
        if sched_path and meta.get("g_reach") not in ("d1", "affinity"):
            print("  · %s ⇒ ⛔ --schedule requires immune-margin regime (g_reach d1/affinity · got %r) —"
                  " wm-dual coverage gate is order-blind by construction (H_9731 KILL scope)" % (p, meta.get("g_reach")))
            continue
        tri = _bld(rows)
        if len(tri) < 12:
            print("  · %s ⇒ ⛔ NOT-POWERED (%d silence transitions <12)" % (p, len(tri)))
            continue
        n_t = len(set(x[0] for x in tri)); n_c = len(set(x[1] for x in tri))
        if n_t < 2 or n_c < 2:
            print("  · %s ⇒ ⛔ NOT-POWERED (timing bins=%d · content addr=%d · need ≥2 each)" % (p, n_t, n_c))
            continue
        mi = _cmi(tri)
        surr = [_surr(tri, rng) for _ in range(perm)]
        ss = sorted(surr)
        p95 = ss[min(len(ss) - 1, int(0.95 * len(ss)))]
        mu = sum(surr) / len(surr)
        sd = (sum((s - mu) ** 2 for s in surr) / max(1, len(surr))) ** 0.5
        z = (mi - mu) / sd if sd > 1e-12 else 0.0
        pv = (sum(1 for s in surr if s >= mi) + 1) / (len(surr) + 1)
        passed = (mi > pedestal) and (mi > p95) and (z >= 2.0) and (pv < 0.005)
        any_pass = any_pass or passed
        print("  · %s  [n=%d · Tbins=%d Caddr=%d]" % (p, len(tri), n_t, n_c))
        print("      I(T;C|S)=%.4f bits · ped=%.4f · surr95=%.4f · z=%.2f · p=%.4f ⇒ %s"
              % (mi, pedestal, p95, z, pv, "✅ timing IS a content channel" if passed else "ns (timing content-free this trace)"))
    print("  ── H_9731 read: %s (MI>pedestal ∧ shuffle collapse ⇒ 관측 WHEN이 보류 WHAT 나름 · mouth-content"
          " 벽 H_9576 timing 재개봉 · DIRECTIONAL until H_9627 303M traces)"
          % ("≥1 trace: timing carries content" if any_pass else "no timing-content channel this batch"))
    return 0 if est_ok else 3


def _gen_percept_schedule(argv):
    """`anima-py evaluate --gen-percept-schedule --out <f.jsonl> [--lags 1,4,16] [--reps 8] [--seed 12345]`

    H_9795 EVALUATION-HISTORICITY producer-side helper. Builds a repeat/shuffle/novel PERCEPT schedule
    played into the daemon through the EXISTING `--percept-file` producer (H_9767) — no new chat flag
    (a_experiment_engine_native minimality). Each row {tick,text,kind,lag,prime}: `--percept-file` reads
    ONLY tick/text (extra keys ignored), while the `--eval-historicity` reader keys off kind/lag/prime to
    compute Delta grade(repeat) - Delta grade(shuffle) with lag-dose. DETERMINISTIC (seeded).

    Structure per (rep, lag, arm in {repeat,shuffle,novel}): a PRIME novel percept at tick t, `lag-1`
    novel fillers, then at t+lag the PROBE = exact-repeat(prime) | byte-multiset-matched shuffle(prime) |
    a fresh novel. The shuffle arm is the load-bearing control: identical unigram byte statistics, order
    destroyed — a grading Delta that survives repeat-vs-shuffle is item-trace, not byte-stats."""
    import json as _json
    import random as _random
    out = evaluate_strval(argv, "--out", "")
    if not out:
        print("--gen-percept-schedule requires --out <path>", file=sys.stderr, flush=True)
        return 2
    lags = [int(x) for x in evaluate_strval(argv, "--lags", "1,4,16").split(",") if x.strip()]
    reps = evaluate_intval(argv, "--reps", 8)
    seed = evaluate_intval(argv, "--seed", 12345)
    jitter = evaluate_intval(argv, "--jitter", 5)   # random 0..jitter pre-fillers per arm so the
                                                    # probe tick DECORRELATES from the sleep-stage
                                                    # phase — else kind confounds with stage and the
                                                    # reader's (lag,stage)-stratified null degenerates
    rng = _random.Random(seed)
    _alpha = list("abcdefghijklmnopqrstuvwxyz0123456789")

    def _novel(i):
        b = list(_alpha)
        rng.shuffle(b)
        return "".join(b[:12]) + "_" + str(i)

    def _shuffle_bytes(s):
        cs = list(s)
        rng.shuffle(cs)
        t = "".join(cs)
        if t == s and len(set(cs)) > 1:      # guarantee order differs (multiset identical)
            cs[0], cs[1] = cs[1], cs[0]
            t = "".join(cs)
        return t

    rows = []
    tick = 0
    for _rep in range(reps):
        for lag in lags:
            for arm in ("repeat", "shuffle", "novel"):
                for _j in range(rng.randint(0, jitter)):   # stage-decorrelating pre-jitter
                    rows.append({"tick": tick, "text": _novel(len(rows)), "kind": "jitter", "lag": lag, "prime": -1})
                    tick += 1
                prime_text = _novel(len(rows))
                prime_tick = tick
                rows.append({"tick": tick, "text": prime_text, "kind": "prime", "lag": lag, "prime": prime_tick})
                tick += 1
                for _f in range(lag - 1):    # fillers so the probe lands exactly at prime_tick+lag
                    rows.append({"tick": tick, "text": _novel(len(rows)), "kind": "filler", "lag": lag, "prime": prime_tick})
                    tick += 1
                if arm == "repeat":
                    ptext = prime_text
                elif arm == "shuffle":
                    ptext = _shuffle_bytes(prime_text)
                else:
                    ptext = _novel(len(rows))
                rows.append({"tick": tick, "text": ptext, "kind": arm, "lag": lag, "prime": prime_tick})
                tick += 1

    with open(out, "w", encoding="utf-8") as _fh:
        for r in rows:
            _fh.write(_json.dumps(r, ensure_ascii=False) + "\n")
    from collections import Counter as _Counter
    kc = _Counter(r["kind"] for r in rows)
    print("--gen-percept-schedule: wrote %d rows -> %s | kinds=%s | lags=%s reps=%d seed=%d"
          % (len(rows), out, dict(kc), lags, reps, seed))
    return 0


def _eval_historicity(argv):
    """`anima-py evaluate --eval-historicity <trace...> --schedule <sched.jsonl> [--dv recon_err]
        [--perm 1000] [--seed 12345]`

    H_9795 EVALUATION-HISTORICITY reader. Does the grading channel carry ITEM-SPECIFIC habituation:
    is an EXACT-REPEAT percept graded differently from a byte-multiset-matched SHUFFLE, and does that
    difference DECAY with lag (item familiarity fades)? Joins the decision trace (DV by tick) with the
    --gen-percept-schedule jsonl (kind/lag/prime by tick).

    DV = `recon_err` (grounded #4168: repeat 0.013 vs byte-matched shuffle 2.051 on toy — the recognition
    field separates item-identity from byte-statistics). Per-lag statistic S(lag)=mean(recon_err|shuffle)
    − mean(recon_err|repeat) (>0 ⟹ shuffle unrecognized > repeat recognized = item-trace). LOAD-BEARING
    control (Fable Q5): the repeat−shuffle contrast alone can be a seed-order DECODE ARTIFACT; only the
    LAG-DECAY (item memory fades, an artifact would not) separates memory from artifact.

    Null: permute the kind label (repeat<->shuffle) within (lag,stage) strata; recompute S. KILL: S
    TOST-zero at every lag. VOID (dead DV, not KILL): recon_err(novel)≈recon_err(repeat) at min lag
    (no dynamic range) OR recon_err near-constant across the run (chat-py-4 degeneracy). novel arm =
    liveness pedestal."""
    import json as _json
    import glob as _glob
    import random as _random
    import statistics as _stats
    sched_path = evaluate_strval(argv, "--schedule", "")
    if not sched_path:
        print("--eval-historicity requires --schedule <gen-percept-schedule jsonl>", file=sys.stderr, flush=True)
        return 2
    dv_name = evaluate_strval(argv, "--dv", "recon_err")
    n_perm = evaluate_intval(argv, "--perm", 1000)
    seed = evaluate_intval(argv, "--seed", 12345)
    globs = [a for a in argv if not a.startswith("--")
             and a not in (sched_path, dv_name, str(n_perm), str(seed))]
    trace_files = []
    for g in globs:
        trace_files.extend(sorted(_glob.glob(g)))
    if not trace_files:
        print("--eval-historicity: no trace files matched " + repr(globs), file=sys.stderr, flush=True)
        return 2

    # kind/lag by tick from the schedule
    sched = {}
    with open(sched_path, "r", encoding="utf-8", errors="surrogateescape") as _fh:
        for _ln in _fh:
            _ln = _ln.strip()
            if not _ln:
                continue
            r = _json.loads(_ln)
            sched[int(r["tick"])] = (r.get("kind"), int(r.get("lag", 0)))

    # DV + stage by (file, tick) → probe records
    probes = []          # (kind, lag, dv, stage)
    dv_all = []
    for tf in trace_files:
        for _ln in open(tf, "r", encoding="utf-8", errors="surrogateescape"):
            _ln = _ln.strip()
            if not _ln or not _ln.startswith("{"):
                continue
            try:
                row = _json.loads(_ln)
            except Exception:
                continue
            t = row.get("tick")
            if t is None:
                continue
            dv = row.get(dv_name)
            if not isinstance(dv, (int, float)):
                continue
            dv_all.append(float(dv))
            sk = sched.get(int(t))
            if sk is None:
                continue
            kind, lag = sk
            if kind in ("repeat", "shuffle", "novel"):
                probes.append((kind, lag, float(dv), int(row.get("stage", 0))))

    n_rep = sum(1 for p in probes if p[0] == "repeat")
    n_shu = sum(1 for p in probes if p[0] == "shuffle")
    n_nov = sum(1 for p in probes if p[0] == "novel")
    lags = sorted(set(p[1] for p in probes if p[0] in ("repeat", "shuffle")))
    print("--eval-historicity: dv=%s · traces=%d · probes rep=%d shuf=%d nov=%d · lags=%s · perm=%d"
          % (dv_name, len(trace_files), n_rep, n_shu, n_nov, lags, n_perm))
    if n_rep < 2 or n_shu < 2:
        print("VERDICT: ⛔ NOT-POWERED (need >=2 repeat and >=2 shuffle probes)")
        return 0

    def _mean(kind, lag):
        vs = [p[2] for p in probes if p[0] == kind and p[1] == lag]
        return _stats.mean(vs) if vs else None

    # ---- VOID gates (dead DV, not KILL) ----
    dv_rng = (max(dv_all) - min(dv_all)) if dv_all else 0.0
    min_lag = lags[0] if lags else 0
    rep0 = _mean("repeat", min_lag)
    nov0 = _mean("novel", min_lag)
    void_reason = None
    if dv_rng < 1e-9:
        void_reason = "recon_err near-constant across run (dead DV · chat-py-4 degeneracy)"
    elif rep0 is not None and nov0 is not None and abs(nov0 - rep0) < 0.05 * max(1e-9, dv_rng):
        void_reason = "recon_err(novel)~recon_err(repeat) at min lag — no item dynamic range"
    if void_reason:
        print("VERDICT: 🕳️ VOID — " + void_reason + " (liveness pedestal failed · not a KILL)")
        return 0

    # ---- per-lag S(lag) = mean(shuffle) - mean(repeat) ----
    S = {}
    for lag in lags:
        sh, rp = _mean("shuffle", lag), _mean("repeat", lag)
        if sh is not None and rp is not None:
            S[lag] = sh - rp
    if not S:
        print("VERDICT: ⛔ NOT-POWERED (no lag has both arms)")
        return 0
    T = S[min_lag]                                   # primary contrast at shortest lag
    # item memory FADES: require a meaningful (>=25% relative) drop from shortest to longest lag,
    # not merely S(short) > S(long) (noise satisfies that). A decode-artifact has no reason to decay.
    s_min, s_max = S.get(lags[0], 0.0), S.get(lags[-1], 0.0)
    lag_decay = (len(lags) >= 2 and s_min > 0.0 and (s_min - s_max) > 0.25 * abs(s_min))

    # ---- permutation null: swap repeat<->shuffle labels within (lag,stage) strata ----
    rng = _random.Random(seed)
    rs = [p for p in probes if p[0] in ("repeat", "shuffle")]
    strata = {}
    for i, p in enumerate(rs):
        strata.setdefault((p[1], p[3]), []).append(i)
    null_T = []
    for _ in range(n_perm):
        # permute the repeat/shuffle labels WITHIN each (lag,stage) stratum (holds the
        # stratum's DV values fixed; only the label assignment is randomized)
        lab = [None] * len(rs)
        for _k, idxs in strata.items():
            labels = [rs[j][0] for j in idxs]
            rng.shuffle(labels)
            for j, L in zip(idxs, labels):
                lab[j] = L
        def _m2(kind, lag):
            vs = [rs[j][2] for j in range(len(rs)) if lab[j] == kind and rs[j][1] == lag]
            return _stats.mean(vs) if vs else None
        sh, rp = _m2("shuffle", min_lag), _m2("repeat", min_lag)
        if sh is not None and rp is not None:
            null_T.append(sh - rp)
    if not null_T:
        print("VERDICT: ⛔ NOT-POWERED (permutation null empty)")
        return 0
    null_sorted = sorted(null_T)
    p95 = null_sorted[int(0.95 * (len(null_sorted) - 1))]
    p_val = sum(1 for x in null_T if abs(x) >= abs(T)) / float(len(null_T))

    print("  S(lag)=%s · T(min-lag S)=%.4f · null95=%.4f · perm-p=%.4f · lag-decay=%s"
          % ({k: round(v, 4) for k, v in S.items()}, T, p95, p_val, lag_decay))
    # ---- verdict ----
    if T > p95 and p_val < 0.05 and lag_decay:
        print("VERDICT: 🟢 ITEM-MEMORY (repeat<shuffle recon ∧ >null ∧ lag-decay) — item-trace, not byte-stats/artifact")
    elif T > p95 and p_val < 0.05 and not lag_decay:
        print("VERDICT: ⚠️ CONTRAST-NO-DECAY — repeat≠shuffle but no lag-decay: possible DECODE-ARTIFACT (Fable Q5), not memory")
    else:
        print("VERDICT: 🧱 NULL — repeat−shuffle within null (grade is byte-stats/percept-blind · TOST toward 0)")
    return 0


def _af_forward(argv):
    """`anima-py evaluate --af-forward <trace...> --impulse <af-impulse jsonl> [--side arousal|valence]
        [--kmax 3] [--perm 1000] [--seed 12345]`

    H_9794 AFFECT-FORWARDING reader. Does the amygdala STATE af, set by an exogenous IMPULSE at tick t0,
    carry FORWARD to condition the grade of the NEXT percept (t0+k, k>=1), over and above the same-tick
    (k=0) shift? Uses --af-impulse traces (af clamped at listed ticks, native elsewhere), so af(t0) is
    decorrelated from af(t0+1) — the static --af-clamp cannot identify this (lab-full Fable Q1).

    DV = the ENVELOPE-FREE PHASIC grade (clock removed analytically, Fable F1/H_9403):
      arousal side  cur_phasic = cur_f / (0.1 + 0.9*stage_env)
      valence side  rel_phasic = rel_f / (0.1 + 0.9*stage_env)
    (never the raw ctx or the *_indep sums — those are circular). Matched-filter h_k = mean(DV at
    impulse_tick+k) − mean(DV at baseline_tick+k). h_0 = WITHIN-TICK positive control (must be nonzero,
    else the af->ci wiring is severed for this ckpt => VOID). h_{k>=1} = the FORWARDING signal.

    Null: permute impulse/baseline labels over the pooled tick set; recompute h_k. KILL 🧱 SHIFT-ONLY:
    h_0 significant but every h_{k>=1} TOST-zero (af is a same-tick shift, not a forwarded state — a real
    negative). PASS 🟢 FORWARDED: some h_{k>=1} beyond null. VOID: h_0 within null (severed wiring) OR
    DV near-constant."""
    import json as _json
    import glob as _glob
    import random as _random
    import statistics as _stats
    imp_path = evaluate_strval(argv, "--impulse", "")
    if not imp_path:
        print("--af-forward requires --impulse <af-impulse jsonl>", file=sys.stderr, flush=True)
        return 2
    side = evaluate_strval(argv, "--side", "arousal")
    num = "cur_f" if side == "arousal" else "rel_f"
    kmax = evaluate_intval(argv, "--kmax", 3)
    n_perm = evaluate_intval(argv, "--perm", 1000)
    seed = evaluate_intval(argv, "--seed", 12345)
    globs = [a for a in argv if not a.startswith("--")
             and a not in (imp_path, side, str(kmax), str(n_perm), str(seed))]
    trace_files = []
    for g in globs:
        trace_files.extend(sorted(_glob.glob(g)))
    if not trace_files:
        print("--af-forward: no trace files matched " + repr(globs), file=sys.stderr, flush=True)
        return 2

    imp_ticks = set()
    with open(imp_path, "r", encoding="utf-8", errors="surrogateescape") as _fh:
        for _ln in _fh:
            _ln = _ln.strip()
            if _ln:
                imp_ticks.add(int(_json.loads(_ln)["tick"]))

    # phasic DV by tick (envelope-free)
    dv = {}          # tick -> phasic DV
    dv_vals = []
    max_t = -1
    for tf in trace_files:
        for _ln in open(tf, "r", encoding="utf-8", errors="surrogateescape"):
            _ln = _ln.strip()
            if not _ln or not _ln.startswith("{"):
                continue
            try:
                row = _json.loads(_ln)
            except Exception:
                continue
            t = row.get("tick")
            if t is None:
                continue
            f = row.get(num)
            se = row.get("stage_env")
            if not isinstance(f, (int, float)) or not isinstance(se, (int, float)):
                continue
            phasic = float(f) / (0.1 + 0.9 * float(se))
            dv[int(t)] = phasic
            dv_vals.append(phasic)
            max_t = max(max_t, int(t))

    base_ticks = set(t for t in dv if t not in imp_ticks)
    print("--af-forward: side=%s dv=%s · traces=%d · impulse-ticks=%d baseline-ticks=%d · kmax=%d perm=%d"
          % (side, num, len(trace_files), len(imp_ticks & set(dv)), len(base_ticks), kmax, n_perm))
    if len(imp_ticks & set(dv)) < 2 or len(base_ticks) < 2:
        print("VERDICT: ⛔ NOT-POWERED (need >=2 impulse and >=2 baseline ticks present in trace)")
        return 0
    if dv_vals and (max(dv_vals) - min(dv_vals)) < 1e-9:
        print("VERDICT: 🕳️ VOID — phasic DV near-constant (severed af->ci wiring or dead gauge · not a KILL)")
        return 0

    def _hk(imp_set, base_set, k):
        iv = [dv[t + k] for t in imp_set if (t + k) in dv]
        bv = [dv[t + k] for t in base_set if (t + k) in dv]
        if len(iv) < 1 or len(bv) < 1:
            return None
        return _stats.mean(iv) - _stats.mean(bv)

    obs = {k: _hk(imp_ticks, base_ticks, k) for k in range(kmax + 1)}
    # permutation null: relabel impulse/baseline over the pooled ticks
    pooled = sorted(imp_ticks & set(dv)) + sorted(base_ticks)
    n_imp = len(imp_ticks & set(dv))
    rng = _random.Random(seed)
    null = {k: [] for k in range(kmax + 1)}
    for _ in range(n_perm):
        pp = pooled[:]
        rng.shuffle(pp)
        pi, pb = set(pp[:n_imp]), set(pp[n_imp:])
        for k in range(kmax + 1):
            h = _hk(pi, pb, k)
            if h is not None:
                null[k].append(abs(h))

    def _p(k):
        if obs[k] is None or not null[k]:
            return 1.0
        return sum(1 for x in null[k] if x >= abs(obs[k])) / float(len(null[k]))

    p0 = _p(0)
    fwd_ks = [k for k in range(1, kmax + 1) if obs[k] is not None and _p(k) < 0.05]
    print("  h_k=%s · perm-p=%s"
          % ({k: (round(v, 4) if v is not None else None) for k, v in obs.items()},
             {k: round(_p(k), 4) for k in range(kmax + 1)}))
    # ---- verdict ----
    if p0 >= 0.05:
        print("VERDICT: 🕳️ VOID — h_0 (within-tick) within null: af does not even move the same-tick grade "
              "(af->ci wiring severed for this ckpt · not a KILL)")
    elif fwd_ks:
        _fwd_signed = {k: round(obs[k], 4) for k in fwd_ks}
        print("VERDICT: 🟢 FORWARDED — h_0 significant ∧ |h_k| beyond null at k=%s (signed %s): af STATE "
              "conditions the NEXT percept's grade (interior→interior forwarding, not just a same-tick shift; "
              "the carryover sign is the direction of modulation)" % (fwd_ks, _fwd_signed))
    else:
        print("VERDICT: 🧱 SHIFT-ONLY — h_0 significant but every h_{k>=1} TOST-zero: af is a same-tick shift, "
              "leaves NO state trace on the next percept (earned negative · forwarding absent)")
    return 0


def _silence_content_te(argv):
    """`anima-py evaluate --silence-content-te <trace globs...> [--perm 1000] [--seed 12345]
       [--reach-lag same|next] [--copy-exclude none|exact|ngram] [--reach-oracle] [--pool]` — H_9729 SILENCE-CONTENT.

    --reach-lag same (DEFAULT · PRIMARY reach · I(cand[t];carrier[t]|cand[t-1])) = "does the withheld
    carrier reach the SAME-tick candidate it seeds", conditioned on the PRE-treatment candidate (the
    fresh oracle carrier ⊥ cand[t-1] ⇒ cleanly certified). --reach-lag next = the residual/carryover read
    I(cand[t+1];carrier[t]|cand[t]) conditioning on the mediator cand[t] (secondary · NOT primary reach).

    Does the WITHHELD candidate's CONTENT causally reach the next imagined candidate (deliberation),
    or is W_S pressure-only (suppression)? = living gate vs living interior. Reads chat traces from
    `anima-py chat ... --emit-gate refractory --g-reach wm-dual --record-silent-cand
    --wm-dual-read content [--wm-dual-perm | --wm-dual-swap <donor> | --wm-dual-oracle]`.

    Source  X_t = frozen 2-bit dominant-address of the RE-ENTERED carrier (wm_reentry_b64[t]).
    Target  Y_{t+1} = same signature of the NEXT tick's PRE-GATE imagined candidate (cand_b64_diag).
      Pre-gate ⇒ mouth-severance-immune AND *not* dual_margin (= probe(W_S,cand) algebraically =
      re-measures the known gate wiring · the Fable→Sol reconcile that avoided a tautological target).
    TE = I(Y_{t+1}; X_t | Y_t) — conditioning on Y_t controls echo/autocorrelation; stage/emit/score
      enter via the surrogate, NOT the joint table (faction over-conditioning death · :7442). EARNED
      read; pass = TE>surr95 ∧ z≥2 ∧ perm-p<0.005. Surrogate = per-trace circular shift of the X
      series (excl {0,±1}), preserving X marginal+autocorrelation while breaking the X→Y coupling.
    Literal-copy handling (--copy-exclude none|exact|ngram · default none · H_9729 run-2 fix): the primary
    TE KEEPS every powered transition; exact/high-containment copies are REPORTED as a diagnostic, never a
    silent filter (the pre-run-2 any-shared-6-gram exclusion has base rate ≈1 on natural EN → it excluded
    38/38 own-arm transitions = a never-measured arm read as a null). `exact` drops only unequivocal copies
    (full-cand==carrier / cand⊂carrier ≥24 B / LCS≥0.8 ≥24 B) as a sensitivity arm; `ngram` = the legacy
    --overlap-ngram behavior (reproduction only).

    Arms (one per trace · meta.wm_dual_read/perm/swap names it):
      own   — factual withheld carrier re-entered.
      perm  — byte-SORTED carrier (feat8/multiset EXACT, order destroyed) = LOAD-BEARING: own>null ∧
              perm≈null ⇒ ORDER-BEARING content moved the interior, not feat8/pressure/histogram.
      donor — another rollout's withheld candidate (own-vs-other specificity · C2).
    Positive control (--reach-oracle · a KNOWN alternating carrier trace from --wm-dual-oracle): the
      SAME estimator must PASS (recovery); if it reads ∅ the channel is REACH-FAIL / MOUTH-SEVERED
      (H_9576) ⇒ any real null is UNINTERPRETABLE, not interior-absent (positive-control-before-negative).
    An always-run synthetic self-test (planted X→Y must recover; independent X→Y must read ~0) guards
    a dead estimator before any read. Validity floors: source-entropy + target-entropy → NOT-POWERED.

    ⚠️ Scope (a_scale_honest_scope): separable only to feat8 granularity (8 byte-stats · 2-bit address).
    A PASS = "the interior reads back its withheld content at byte-ORDER granularity" (real deliberation
    — pressure can't, echo dies under perm), NOT a semantic-interior claim. DIRECTIONAL until 303M."""
    import glob as _glob, base64 as _b64, math as _m, random as _random, json as _json
    globs = [a for a in argv if not a.startswith("--")]
    def _iv(flag, d):
        for i, a in enumerate(argv):
            if a == flag and i + 1 < len(argv):
                try:
                    return int(argv[i + 1])
                except Exception:
                    return d
        return d
    def _sv(flag, d):
        for i, a in enumerate(argv):
            if a == flag and i + 1 < len(argv):
                return argv[i + 1]
        return d
    perm = _iv("--perm", 1000)
    seed = _iv("--seed", 12345)
    ov_ng = _iv("--overlap-ngram", 6)
    # H_9729 run-2 (Fable∥Sol · #4045): the any-shared-6-gram exclusion has base rate ≈1 on natural EN
    # (excluded 38/38 → own arm NEVER measured). Default is now KEEP-ALL for the primary TE; literal-copy
    # is a SEPARATE diagnostic, not a silent filter (Sol: conditioning inclusion on the X↔Y relationship
    # being estimated distorts the TE population). --copy-exclude {none(default)|exact|ngram(legacy)}:
    #   none  = primary keeps every powered transition; exact/high-containment copies REPORTED, not dropped
    #   exact = drop only unequivocal copies (full-cand==carrier, or cand⊂carrier ≥24B, or LCS/len≥0.8 ≥24B)
    #   ngram = the pre-run-2 --overlap-ngram behavior (base-rate-saturated · reproduction only)
    copy_excl = _sv("--copy-exclude", "none").lower()
    if copy_excl not in ("none", "exact", "ngram"):
        copy_excl = "none"
    # H_9729 run-2 QA (Fable∥Sol · #4046): the reader's original triple (X=carrier[t], Y0=cand[t],
    # Y1=cand[t+1]) conditions on cand[t] — but carrier[t] REACHES cand[t] SAME-TICK (chat.py injects the
    # re-entry anchor at t, decode produces cand_pregate[t] the same row; certify-pilot 79% same-row
    # survival). Conditioning on cand[t] is post-treatment conditioning on the MEDIATOR → it blocks the
    # principal carrier[t]→cand[t]→future path (Sol) and taxes power as transmission improves (Fable). So
    #   --reach-lag same (DEFAULT · PRIMARY reach) = I(cand[t] ; carrier[t] | cand[t-1]) — the card's
    #     "does withheld content reach the next imagined candidate" question, conditioned on the
    #     PRE-treatment candidate (cand[t-1] ⊥ the fresh oracle carrier ⇒ cleanly identified for the
    #     oracle; the fresh-each-tick oracle is a valid isolated pulse here — no HOLD-K, which both models
    #     rejected as certifying persistence indistinguishably from fresh reinjection).
    #   --reach-lag next (SECONDARY · labeled residual/carryover) = the original I(cand[t+1];carrier[t]|
    #     cand[t]) — a post-treatment residual read, NOT primary reach; kept for the persistence angle.
    reach_lag = _sv("--reach-lag", "same").lower()
    if reach_lag not in ("same", "next"):
        reach_lag = "same"
    reach_oracle = "--reach-oracle" in argv
    # H_9729 pooled reader (--pool · evaluate-py-24): the own re-entry is ONE-SHOT (~1 usable transition
    # per trace), so the per-trace ≥12 bar can NEVER power the own arm at any tick count. --pool collects
    # same-arm triples ACROSS traces into one estimate. Each trace contributes ~1 INDEPENDENT (X,Y0,Y1)
    # draw ⇒ the within-trace circular-shift null is undefined (m=1); the valid null is a Y0-STRATIFIED
    # permutation of X (breaks I(Y1;X|Y0)=0 while preserving the Y0-conditional X marginal). Default off
    # ⇒ the per-trace path is byte-identical. (Sol single-model · Fable OAuth-down · not-cemented-DIRECTIONAL.)
    pool_mode = "--pool" in argv
    _pooled = {}
    paths = []
    for g in globs:
        paths.extend(sorted(_glob.glob(g)))
    print("═══ H_9729 SILENCE-CONTENT · does withheld CONTENT reach the next imagined candidate? ═══")
    print("  traces=%d · perm=%d · seed=%d · reach-lag=%s (%s) · overlap-excl=%d-gram%s"
          % (len(paths), perm, seed, reach_lag,
             "PRIMARY reach I(cand[t];carrier[t]|cand[t-1])" if reach_lag == "same"
             else "residual I(cand[t+1];carrier[t]|cand[t])",
             ov_ng, " · REACH-ORACLE" if reach_oracle else ""))

    # frozen 2-bit dominant-CHAR-CLASS signature: argmax over [n_dig, n_upper, n_lower, n_pun] (the
    # dominant character class · researcher DOF = 0 · tie → lowest index). Chosen over a raw-byte-stat
    # argmax because n_lt64/var SATURATE on ASCII text (a digit-vs-punct oracle both read <64 →
    # collapse to one address = a dead positive control · caught in toy calibration). Char classes
    # discriminate real byte-LM output AND the oracle A/B. Order-independent (multiset) BY DESIGN: the
    # perm control acts at the GENERATION level (a sorted seed makes a different Y), not on this stat.
    # signature = POPULATION-RELATIVE (_content_sig_factory · built per-trace from that trace's own
    # candidates). The absolute char-class argmax it replaces read ONE address for every natural-English
    # candidate (lowercase always dominant) = dead alphabet on real 303M data (convergence evaluate-py-23).

    def _overlap(a_b64, b_b64, ng):
        try:
            a = _b64.b64decode(a_b64) if a_b64 else b""
            b = _b64.b64decode(b_b64) if b_b64 else b""
        except Exception:
            return False
        if len(a) < ng or len(b) < ng:
            return len(a) > 0 and a == b
        ags = set(a[i:i + ng] for i in range(len(a) - ng + 1))
        for i in range(len(b) - ng + 1):
            if b[i:i + ng] in ags:
                return True
        return False

    def _lcspan(a, b):
        # longest common CONTIGUOUS byte span (DP over the two short strings · candidates ~40-80 B).
        if not a or not b:
            return 0
        best = 0
        prev = [0] * (len(b) + 1)
        for i in range(1, len(a) + 1):
            cur = [0] * (len(b) + 1)
            ai = a[i - 1]
            for j in range(1, len(b) + 1):
                if ai == b[j - 1]:
                    v = prev[j - 1] + 1
                    cur[j] = v
                    if v > best:
                        best = v
            prev = cur
        return best

    def _is_copy(carrier_b64, cand_b64):
        # Sol's honest narrow rule (H_9729 run-2): flag ONLY an unequivocal copy — full-candidate byte
        # equality with the carrier, candidate wholly contained in the carrier (≥24 B), or a contiguous
        # common span ≥24 B that is ≥80% of the candidate. This is the "not explained by literal copy"
        # guarantee WITHOUT the any-shared-6-gram base-rate saturation (≈1 on natural EN · excluded 38/38).
        try:
            c = _b64.b64decode(carrier_b64) if carrier_b64 else b""
            d = _b64.b64decode(cand_b64) if cand_b64 else b""
        except Exception:
            return False
        if not d:
            return False
        if d == c:
            return True
        if len(d) >= 24 and d in c:
            return True
        span = _lcspan(c, d)
        return span >= 24 and span >= 0.8 * len(d)

    def _cmi(triples):
        # I(Y1 ; X | Y0) plug-in (bits) — structure mirrors _te_sign_to_emit's conditional form.
        from collections import Counter as _C
        j = _C(); xy0 = _C(); y01 = _C(); y0c = _C()
        for (x, y0, y1) in triples:
            j[(y1, x, y0)] += 1
            xy0[(x, y0)] += 1
            y01[(y1, y0)] += 1
            y0c[y0] += 1
        n = max(1, sum(j.values()))
        te = 0.0
        for (y1, x, y0), c in j.items():
            p = c / n
            p_y1_xy0 = c / xy0[(x, y0)]
            p_y1_y0 = y01[(y1, y0)] / y0c[y0]
            if p_y1_xy0 > 0 and p_y1_y0 > 0:
                te += p * _m.log2(p_y1_xy0 / p_y1_y0)
        return max(0.0, te)

    def _surr_null(triples, rng):
        # per-trace CIRCULAR shift of the X series (excl shift ∈ {0,±1}) — preserves X marginal +
        # autocorrelation, breaks the X→(Y0,Y1) coupling (Sol · better than IID shuffle).
        xs = [t[0] for t in triples]
        rest = [(t[1], t[2]) for t in triples]
        m = len(xs)
        if m < 5:
            return 0.0
        s = rng.randrange(2, m - 1)
        xs2 = xs[-s:] + xs[:-s]
        return _cmi([(xs2[i], rest[i][0], rest[i][1]) for i in range(m)])

    def _surr_perm_pooled(triples, rng):
        # --pool null: Y0-STRATIFIED permutation of X over a POOL of independent draws (≈1/trace). The
        # within-trace circular shift (_surr_null) is undefined at m≈1; this shuffles X INSIDE each Y0
        # stratum, breaking I(Y1;X|Y0) while preserving the Y0-conditional X marginal + the (Y0,Y1) joint.
        from collections import defaultdict as _dd
        strata = _dd(list)
        for i, t in enumerate(triples):
            strata[t[1]].append(i)
        xs = [t[0] for t in triples]
        xs2 = xs[:]
        for _y0, idxs in strata.items():
            px = [xs[i] for i in idxs]
            rng.shuffle(px)
            for k, i in enumerate(idxs):
                xs2[i] = px[k]
        return _cmi([(xs2[i], triples[i][1], triples[i][2]) for i in range(len(triples))])

    # ── estimator self-test (planted recovery + independent null) · dead estimator = STOP ──
    _strng = _random.Random(seed ^ 0x9729)
    _planted = [((k := _strng.randrange(4)), _strng.randrange(4), k) for _ in range(400)]  # Y1==X
    _indep = [(_strng.randrange(4), _strng.randrange(4), _strng.randrange(4)) for _ in range(400)]
    _te_planted = _cmi(_planted); _te_indep = _cmi(_indep)
    _est_ok = _te_planted > 0.5 and _te_indep < 0.15
    print("  estimator self-test : planted I(Y1;X|Y0)=%.3f (want>0.5) · independent=%.3f (want<0.15) ⇒ %s"
          % (_te_planted, _te_indep, "✅ live" if _est_ok else "❌ DEAD-ESTIMATOR (do not read below)"))
    if pool_mode:
        # pooled-null self-test: the Y0-stratified permutation MUST break the planted signal (earned>0.5)
        # and read ~0 on independent data — validates the --pool surrogate before any pooled read.
        _sp = _surr_perm_pooled(_planted, _random.Random(seed ^ 0x7729))
        _si = _surr_perm_pooled(_indep, _random.Random(seed ^ 0x6729))
        _pool_ok = (_te_planted - _sp) > 0.5 and abs(_te_indep - _si) < 0.15
        print("  pooled-null self-test : planted perm-null=%.3f (earned %.3f · want>0.5) · indep perm-null="
              "%.3f (Δ %.3f · want<0.15) ⇒ %s" % (_sp, _te_planted - _sp, _si, abs(_te_indep - _si),
              "✅ pooled-null valid" if _pool_ok else "❌ POOLED-NULL DEAD (do not read --pool below)"))
        _est_ok = _est_ok and _pool_ok
    if not paths:
        print("  ⇒ ⛔ no traces matched: %r  (produce with --wm-dual-read content)" % globs)
        return 2 if _est_ok else 3

    _rng = _random.Random(seed)
    any_pass = False
    any_signal = False   # H_9729 run-2: carrier signal PRESENT (earned>0 ∧ TE>surr95 ∧ p<0.05) but below strict bar
    for p in paths:
        meta = {}; rows = []
        for ln in open(p, encoding="utf-8", errors="surrogateescape"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = _json.loads(ln)
            except Exception:
                continue
            if isinstance(r, dict) and r.get("_meta"):
                meta = r
            elif isinstance(r, dict) and "tick" in r:
                rows.append(r)
        arm = ("oracle" if meta.get("wm_dual_oracle") else
               "perm" if meta.get("wm_dual_perm") else
               "swap" if meta.get("wm_dual_swap") else
               ("own" if meta.get("wm_dual_read") == "content" else "off"))
        # build (x, y0, y1) triples on ticks the carrier was injected (wm_reentry_arm != off).
        # ONE quantizer over the carrier ∪ candidate population so X and Y bin on the same scale
        # (evaluate-py-23: an absolute threshold reads 1 address on natural text).
        _sig = _content_sig_factory([r.get("wm_reentry_b64", "") for r in rows]
                                    + [r.get("cand_pregate_b64", "") for r in rows])
        # lag-aware triple (X, Y0, Y1): same = (carrier[i], cand[i-1], cand[i]) — PRIMARY reach, target is
        # the SAME-row candidate the carrier seeds, conditioned on the PRE-treatment candidate cand[i-1];
        # next = (carrier[i], cand[i], cand[i+1]) — residual/carryover, conditioned on the mediator cand[i].
        triples = []; n_excl = 0; xs_all = []; n_inj = 0; n_copy = 0
        _lo = 1 if reach_lag == "same" else 0
        _hi = len(rows) if reach_lag == "same" else len(rows) - 1
        for i in range(_lo, _hi):
            if rows[i].get("wm_reentry_arm", "off") == "off":
                continue
            n_inj += 1
            if reach_lag == "same":
                x = _sig(rows[i].get("wm_reentry_b64", ""))
                y0 = _sig(rows[i - 1].get("cand_pregate_b64", ""))
                y1 = _sig(rows[i].get("cand_pregate_b64", ""))
                _carr = rows[i].get("wm_reentry_b64", ""); _nxt = rows[i].get("cand_pregate_b64", "")
            else:
                x = _sig(rows[i].get("wm_reentry_b64", ""))
                y0 = _sig(rows[i].get("cand_pregate_b64", ""))
                y1 = _sig(rows[i + 1].get("cand_pregate_b64", ""))
                _carr = rows[i].get("wm_reentry_b64", ""); _nxt = rows[i + 1].get("cand_pregate_b64", "")
            if x < 0 or y0 < 0 or y1 < 0:
                continue
            _copy = _is_copy(_carr, _nxt)
            if _copy:
                n_copy += 1
            # keep-all primary (copy_excl=none): copies are REPORTED, not silently dropped (H_9729 run-2).
            if copy_excl == "exact" and _copy:
                n_excl += 1
                continue
            if copy_excl == "ngram" and _overlap(_carr, _nxt, ov_ng):
                n_excl += 1
                continue
            triples.append((x, y0, y1)); xs_all.append(x)
        print("  · %s  [arm=%s]" % (p, arm))
        print("      copy-diag: %d/%d injected transitions are literal copies (exact/≥24B-contain/LCS≥0.8)"
              " · copy-exclude=%s%s" % (n_copy, n_inj, copy_excl,
              (" (%d dropped)" % n_excl) if copy_excl != "none" else " (kept · reported only)"))
        if pool_mode:
            _pooled.setdefault(arm, []).extend(triples)
            print("      [pool] +%d transition(s) → arm=%s pool (per-trace verdict deferred)"
                  % (len(triples), arm))
            continue
        if len(triples) < 12:
            print("      ⇒ ⛔ NOT-POWERED (%d usable transitions <12 · %d injected · %d copy-excluded)"
                  % (len(triples), n_inj, n_excl))
            continue
        n_x = len(set(xs_all)); n_y1 = len(set(t[2] for t in triples))
        if n_x < 2 or n_y1 < 2:
            print("      ⇒ ⛔ NOT-POWERED (source addresses=%d · target addresses=%d · need ≥2 each"
                  " = no usable alphabet · feat8-clustered)" % (n_x, n_y1))
            continue
        te_real = _cmi(triples)
        surr = [_surr_null(triples, _rng) for _ in range(perm)]
        surr_sorted = sorted(surr)
        p95 = surr_sorted[min(len(surr_sorted) - 1, int(0.95 * len(surr_sorted)))]
        mu = sum(surr) / len(surr)
        sd = (sum((s - mu) ** 2 for s in surr) / max(1, len(surr))) ** 0.5
        z = (te_real - mu) / sd if sd > 1e-12 else 0.0
        pval = (sum(1 for s in surr if s >= te_real) + 1) / (len(surr) + 1)
        earned = te_real - mu
        passed = (te_real > p95) and (z >= 2.0) and (pval < 0.005)
        signal = (te_real > p95) and (earned > 0) and (pval < 0.05)  # present but sub-strict-bar (underpowered)
        any_pass = any_pass or passed
        any_signal = any_signal or signal
        print("      n=%d transitions · X-addr=%d Y-addr=%d · %d literal-copy (%s)"
              % (len(triples), n_x, n_y1, n_copy, ("excluded" if copy_excl != "none" else "kept·reported")))
        print("      TE=I(Y1;X|Y0)=%.4f bits · earned=%.4f · surr95=%.4f · z=%.2f · perm-p=%.4f ⇒ %s"
              % (te_real, earned, p95, z, pval, "✅ content-transfer" if passed else "ns (no content transfer)"))
    # verdict framing · REACH-ORACLE is THREE-way (H_9729 run-2 · Fable∥Sol): the old binary stamped
    # MOUTH-SEVERED on ANY sub-strict-bar result, conflating "underpowered" with "severed". A carrier
    # with earned>0 ∧ TE>surr95 REACHES cand[t+1] (the channel is live); it just lacks power at the
    # strict bar. Only earned≈0 / TE≤surr95 (the run-2 point-mass signature) is genuine severance.
    if pool_mode:
        for arm, ptr in sorted(_pooled.items()):
            print("  ══ [POOL] arm=%s · %d pooled transitions across %d trace(s) ══"
                  % (arm, len(ptr), len(paths)))
            if len(ptr) < 12:
                print("      ⇒ ⛔ NOT-POWERED (pooled %d <12 · one-shot ⇒ ~1/trace ⇒ need ≥12 traces)"
                      % len(ptr))
                continue
            _nx = len(set(t[0] for t in ptr)); _ny = len(set(t[2] for t in ptr))
            if _nx < 2 or _ny < 2:
                print("      ⇒ ⛔ NOT-POWERED (pooled X-addr=%d Y-addr=%d · need ≥2 each)" % (_nx, _ny))
                continue
            _te = _cmi(ptr)
            _sur = [_surr_perm_pooled(ptr, _rng) for _ in range(perm)]
            _ss = sorted(_sur); _p95 = _ss[min(len(_ss) - 1, int(0.95 * len(_ss)))]
            _mu = sum(_sur) / len(_sur)
            _sd = (sum((s - _mu) ** 2 for s in _sur) / max(1, len(_sur))) ** 0.5
            _z = (_te - _mu) / _sd if _sd > 1e-12 else 0.0
            _pv = (sum(1 for s in _sur if s >= _te) + 1) / (len(_sur) + 1)
            _earned = _te - _mu
            _passed = (_te > _p95) and (_z >= 2.0) and (_pv < 0.005)
            _sig = (_te > _p95) and (_earned > 0) and (_pv < 0.05)
            any_pass = any_pass or _passed
            any_signal = any_signal or _sig
            print("      pooled TE=I(Y1;X|Y0)=%.4f · earned=%.4f · Y0-strat-perm surr95=%.4f · z=%.2f "
                  "· perm-p=%.4f ⇒ %s" % (_te, _earned, _p95, _z, _pv,
                  "✅ content-transfer (pooled)" if _passed else
                  ("🟡 signal-sub-bar (pooled)" if _sig else "ns (no pooled content-transfer)")))
    if reach_oracle:
        if any_pass:
            print("  ── REACH-ORACLE verdict: ✅ CERTIFIED — known carrier recovered at the strict bar"
                  " (TE>surr95 ∧ z≥2 ∧ p<0.005) ⇒ the reader can read reach; a real H_9729 null would be"
                  " interior-absent")
        elif any_signal:
            print("  ── REACH-ORACLE verdict: 🟡 REACH-MARGINAL — carrier signal PRESENT (TE>surr95 ∧"
                  " earned>0 ∧ p<0.05) but UNDERPOWERED at the strict bar. The channel REACHES (this is"
                  " NOT mouth-severance — earned>0); add ticks to certify. A real H_9729 null stays"
                  " uninterpretable until CERTIFIED.")
        else:
            print("  ── REACH-ORACLE verdict: ❌ REACH-FAIL / MOUTH-SEVERED (H_9576) — the known carrier"
                  " did NOT reach cand[t+1] (earned≈0 / TE≤surr95); a real null is UNINTERPRETABLE"
                  " (reach fact, not interior absence)")
    else:
        print("  ── H_9729 read: %s  (own PASS ∧ perm/donor ns ⇒ ORDER-BEARING withheld content moves"
              " the interior · feat8 granularity · DIRECTIONAL until 303M · run --reach-oracle first)"
              % ("≥1 arm shows content-transfer" if any_pass else "no content-transfer this batch"))
    return 0 if _est_ok else 3


def _ag_criticality(argv):
    """H_9607 A⇄G CRITICALITY — engine-native readout of the A⇄G feedback loop over decision traces.

    `anima-py evaluate --ag-criticality <trace globs...> [--perm N] [--seed N]`

    Reads the traces `anima-py chat --ag-feedback <κ>` already wrote (NO decode, like --dead-census /
    --pc2-direction / --emit-gate-census) and renders the trace-computable panels of Fable's three-panel
    discriminator (the verdict statistic must be engine-native · a_experiment_engine_native · H_9303/07):

      (C0) LOOP-LIVENESS  — distinct(ag_drive): κ=0 ⇒ 1 (value 0.0, field untouched = the byte-parity
                            guarantee); κ>0 ⇒ >1 (the A→G→A return leg is live). A dead ag_drive means
                            the loop is inert (STILL-SEALED), not that Ψ moved.
      (ii) TE(tension→emit) — transfer entropy from the signed net tension ag_s to the emit bit, with a
                            phase-scramble (time-shuffle of ag_s) surrogate null over --perm draws. The
                            loop is a causal channel iff TE_real exceeds the surrogate 95th pct (z≥2).
      (iii) HOMEOSTASIS    — mean emit_drive and |mean − ½|: is emit_drive pulled toward ½? Reported as
                            color (a toy/short trace cannot cement homeostasis · a_scale_honest_scope);
                            the score-perturbation robustness arm + the vshuf/quantile forgery controls
                            are part of the pre-registered 303M fire, not this trace read.

    Panel (i) butterfly-Lyapunov needs a SEED-FLIP rollout PAIR (1-byte seed flip, same sample seed;
    frozen null = H_9603 divergence-growth +0.007) — a fired pair, not a single-trace read; documented
    as the 303M fire protocol and NOT computed here. This reader is DIRECTIONAL (offline · a toy trace
    is not a Ψ verdict); the terminal verdict is the owner-gated 303M --ag-criticality run.
    """
    perm = 200
    seed = 7
    bf_pair = None
    globs = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--perm" and i + 1 < len(argv):
            perm = int(argv[i + 1]); i += 2; continue
        if a == "--seed" and i + 1 < len(argv):
            seed = int(argv[i + 1]); i += 2; continue
        if a == "--butterfly" and i + 2 < len(argv):
            bf_pair = (argv[i + 1], argv[i + 2]); i += 3; continue
        globs.append(a); i += 1
    if not globs and bf_pair is None:
        print("  ⇒ ⛔ usage: anima-py evaluate --ag-criticality <trace globs...> [--perm N] [--seed N]")
        print("            or --ag-criticality --butterfly <seedflip_A.jsonl> <seedflip_B.jsonl>  (panel i · λ)")
        return 2
    import glob as _glob
    paths = []
    for g in globs:
        paths.extend(sorted(_glob.glob(g)))
    if not paths and bf_pair is None:
        print("  ⇒ ⛔ no traces matched: %r" % globs)
        return 2

    def _ticks(p):
        out = []
        for ln in open(p, encoding="utf-8", errors="surrogateescape"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if isinstance(r, dict) and "ag_drive" in r and "emit" in r:
                out.append(r)
        return out

    if bf_pair is not None:
        # Panel (i) butterfly-λ: two seed-flip rollouts (1-byte session_seed flip, same sample seed).
        # State vector = z-normalised [emit_drive, phi, ag_fb_I]; per-tick L2 distance d_t; divergence
        # GROWTH = least-squares slope of d_t vs tick (H_9603 frozen null +0.007 ≈ 0 = zero-Lyapunov
        # linear limit-cycle). slope ≫ +0.05 ⇒ λ departs 0 (dynamics revived); ≈ null ⇒ STILL zero-Lyapunov.
        A = _ticks(bf_pair[0]); B = _ticks(bf_pair[1])
        n = min(len(A), len(B))
        print("═══ A⇄G CRITICALITY · panel (i) butterfly-λ · H_9607 (H_9603 null +0.007) ═══")
        if n < 20:
            print("  ⇒ ⛔ NOT-POWERED (<20 aligned ticks: A=%d B=%d)" % (len(A), len(B)))
            return 0
        keys = ["emit_drive", "phi", "ag_fb_I"]
        # z-normalise each field over the pooled A∪B series so no axis dominates the distance
        import math as _m
        stats = {}
        for k in keys:
            vals = [float(r.get(k, 0.0)) for r in A[:n]] + [float(r.get(k, 0.0)) for r in B[:n]]
            mu = sum(vals) / len(vals)
            sd = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
            stats[k] = (mu, sd)
        d = []
        for t in range(n):
            s2 = 0.0
            for k in keys:
                mu, sd = stats[k]
                za = (float(A[t].get(k, 0.0)) - mu) / sd
                zb = (float(B[t].get(k, 0.0)) - mu) / sd
                s2 += (za - zb) ** 2
            d.append(_m.sqrt(s2))
        # least-squares slope of d_t vs t
        ts = list(range(n))
        mt = sum(ts) / n; md = sum(d) / n
        num = sum((ts[t] - mt) * (d[t] - md) for t in range(n))
        den = sum((ts[t] - mt) ** 2 for t in range(n)) or 1.0
        slope = num / den
        kappa = float(A[0].get("ag_feedback_kappa", B[0].get("ag_feedback_kappa", 0.0)))
        print("  pair: %s ⇔ %s · κ=%.4g · aligned ticks=%d" % (bf_pair[0], bf_pair[1], kappa, n))
        print("      d_0=%.4f · d_end=%.4f · divergence-growth slope=%.5f /tick" % (d[0], d[-1], slope))
        verdict = ("λ DEPARTS 0 (dynamics revived · chaotic/edge)" if slope > 0.05
                   else "≈ H_9603 null (STILL zero-Lyapunov · limit-cycle)" if abs(slope) <= 0.02
                   else "marginal (0.02–0.05 · underpowered band)")
        print("      ⇒ %s  [frozen null: H_9603 +0.007]" % verdict)
        return 0

    def _te_sign_to_emit(rows):
        # TE(ag_s → emit): discrete, ag_s binned by sign (2 states), emit binary.
        # TE = Σ p(e', e, x) log2 [ p(e'|e,x) / p(e'|e) ], x = sign(ag_s_t), e=emit_t, e'=emit_{t+1}.
        from collections import Counter as _C
        joint = _C(); ee = _C(); eex = _C(); e_ctx = _C()
        for t in range(len(rows) - 1):
            e = 1 if rows[t].get("emit") else 0
            e1 = 1 if rows[t + 1].get("emit") else 0
            x = 1 if float(rows[t].get("ag_s", 0.0)) >= 0.0 else 0
            joint[(e1, e, x)] += 1
            eex[(e, x)] += 1
            ee[(e1, e)] += 1
            e_ctx[e] += 1
        n = max(1, sum(joint.values()))
        import math as _m
        te = 0.0
        for (e1, e, x), c in joint.items():
            p_joint = c / n
            p_e1_given_ex = c / eex[(e, x)]
            p_e1_given_e = ee[(e1, e)] / e_ctx[e]
            if p_e1_given_ex > 0 and p_e1_given_e > 0:
                te += p_joint * _m.log2(p_e1_given_ex / p_e1_given_e)
        return max(0.0, te)

    print("═══ A⇄G CRITICALITY · H_9607 · engine-native readout of the A→G→A feedback loop ═══")
    print("  traces=%d · perm=%d · seed=%d" % (len(paths), perm, seed))
    _rng = random.Random(seed)
    any_live = False
    for p in paths:
        rows = _ticks(p)
        if len(rows) < 8:
            print("  · %s: rows=%d ⇒ ⛔ NOT-POWERED (<8 tick rows)" % (p, len(rows)))
            continue
        drives = [round(float(r["ag_drive"]), 12) for r in rows]
        nd = len(set(drives))
        kappa = float(rows[0].get("ag_feedback_kappa", 0.0))
        eds = [float(r.get("emit_drive", 0.0)) for r in rows]
        mean_ed = sum(eds) / len(eds)
        emit_rate = sum(1 for r in rows if r.get("emit")) / len(rows)
        te_real = _te_sign_to_emit(rows)
        # phase-scramble surrogate: shuffle ag_s series (destroys the loop timing, keeps the marginal)
        surr = []
        base_s = [float(r.get("ag_s", 0.0)) for r in rows]
        for _ in range(perm):
            perm_s = base_s[:]
            _rng.shuffle(perm_s)
            srows = [dict(r) for r in rows]
            for j in range(len(srows)):
                srows[j]["ag_s"] = perm_s[j]
            surr.append(_te_sign_to_emit(srows))
        surr_sorted = sorted(surr)
        p95 = surr_sorted[min(len(surr_sorted) - 1, int(0.95 * len(surr_sorted)))]
        mu = sum(surr) / len(surr)
        sd = (sum((s - mu) ** 2 for s in surr) / max(1, len(surr))) ** 0.5
        z = (te_real - mu) / sd if sd > 1e-12 else 0.0
        live = nd > 1
        any_live = any_live or live
        print("  · %s" % p)
        print("      C0 loop-liveness : κ=%.4g · distinct(ag_drive)=%d ⇒ %s"
              % (kappa, nd, "✅ LIVE" if live else ("byte-parity (κ=0)" if kappa == 0.0 else "❌ inert")))
        print("      ii TE(ag_s→emit) : TE=%.4f bits · surr95=%.4f · z=%.2f ⇒ %s"
              % (te_real, p95, z, "✅ channel" if (te_real > p95 and z >= 2.0) else "ns (no causal channel this trace)"))
        print("      iii homeostasis  : mean(emit_drive)=%.3f |·−½|=%.3f · emit-rate=%.3f  [color · not a verdict]"
              % (mean_ed, abs(mean_ed - 0.5), emit_rate))
    print("  ── panel (i) butterfly-λ needs a SEED-FLIP fired PAIR (H_9603 null +0.007) = 303M owner-gate fire, not this read.")
    print("  ⇒ DIRECTIONAL trace read (a_scale_honest_scope · toy ≠ Ψ verdict). loop live in ≥1 trace: %s" % ("yes" if any_live else "no"))
def _pc2_emit_coupling(argv):
    """H_9741 EMIT-COUPLING — do the LIVE tension axes couple to emit, or are they orthogonal?

    `anima-py evaluate --pc2-direction <traces_dir> --emit-coupling [--perm N] [--seed N]`

    THE QUESTION H_9713 EXPLICITLY LEFT OPEN. H_9428/H_9468 certified PC2 as an "emit-ORTHOGONAL
    second DOF", and H_9574/9576/9630-9634 built a whole lane on that orthogonality. H_9713 then
    showed the frozen axis's live RANK is unstable (nearest live PC flips run to run), and its
    verdict flagged -- in writing -- that "whether live PC1 is emit-coupled is NOT asked by that
    instrument". This asks exactly that: refit the live 8x8 covariance, take each PC's score
    trajectory, and correlate it (point-biserial) with the emit bit.

      |r| < 0.15 for every PC  => ORTHOGONAL (the emit-orthogonal-DOF story survives the label churn)
      any |r| > 0.15, p<.01    => COUPLED   (they were steering an emit-relevant axis after all)

    POSITIVE CONTROL: the frozen z (pc2_z) itself must show a small emit correlation -- H_9428
    reported corr(|x_perp|, emit)=+0.14. If z shows ZERO, the instrument cannot see coupling and
    the run is INVALID, not orthogonal.

    Autocorrelation is high (H_9714: lag-1 rho ~0.86), so n_eff << n and the permutation null is
    mandatory -- the nominal p is not trustworthy.
    """
    import glob as _glob
    import json as _pj
    import random as _prand
    import numpy as _np

    ALL8 = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
            "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]
    THR = 0.15

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --emit-coupling")
        return 2
    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    runs, seen, dup = [], set(), 0
    for f in files:
        X, E, Z = [], [], []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                continue
            v = [r.get(k) for k in ALL8]
            if any(x is None for x in v) or r.get("emit") is None:
                continue
            X.append([float(x) for x in v])
            E.append(1.0 if r.get("emit") else 0.0)
            Z.append(float(r["pc2_z"]) if r.get("pc2_z") is not None else 0.0)
        if len(X) < 20:
            continue
        Xa = _np.asarray(X)
        h = hash(Xa.tobytes())
        if h in seen:
            dup += 1
            continue
        seen.add(h)
        runs.append((os.path.basename(f), Xa, _np.asarray(E), _np.asarray(Z)))
    if not runs:
        print("  ⇒ ⛔ emit+8인자 트레이스 없음")
        return 2

    print("=== anima evaluate --pc2-direction --emit-coupling — H_9741 라이브 축 emit 결합성 ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 %d 제외)" % (d, len(files), len(runs), dup))
    print("질문:  라이브 PC(1·2·3)가 emit 과 결합하나 직교하나 (H_9713 이 남긴 열린 질문)")
    print("bar:   모든 |r|<%.2f ⇒ ORTHOGONAL / 어느 |r|>%.2f ∧ p<.01 ⇒ COUPLED · 양성통제=z corr≠0" % (THR, THR))
    print("⚠️ 부호는 PCA sign-flip 임의 ⇒ |r| 로 판정 · 자기상관 높아(H_9714 lag-1 ρ̂ 0.86) permutation 필수")
    print("")

    def _pb(sc, e):
        if sc.std() == 0 or e.std() == 0:
            return 0.0
        return float(_np.corrcoef(sc, e)[0, 1])

    agg = {"PC1": [], "PC2": [], "PC3": [], "z": []}
    pvals = {"PC1": [], "PC2": [], "PC3": [], "z": []}
    for name, X, E, Z in runs:
        Xc = X - X.mean(axis=0)
        C = (Xc.T @ Xc) / float(Xc.shape[0] - 1)
        w, V = _np.linalg.eigh(C)
        o = _np.argsort(w)[::-1]
        V = V[:, o]
        scores = {"PC1": Xc @ V[:, 0], "PC2": Xc @ V[:, 1], "PC3": Xc @ V[:, 2], "z": Z}
        rng = _prand.Random(rseed)
        line = []
        for k in ("PC1", "PC2", "PC3", "z"):
            r = _pb(scores[k], E)
            null = []
            Ei = E.copy()
            for _ in range(rounds):
                rng.shuffle(Ei)
                null.append(abs(_pb(scores[k], Ei)))
            p = sum(1 for vv in null if vv >= abs(r)) / float(rounds)
            agg[k].append(r)
            pvals[k].append(p)
            line.append("%s=%+.3f(p%.3f)" % (k, r, p))
        print("  %-18s %s" % (name, " · ".join(line)))

    def _mean_abs(k):
        return sum(abs(x) for x in agg[k]) / float(len(agg[k]))

    print("")
    zc = _mean_abs("z")
    print("  run-평균 |r|: PC1=%.3f PC2=%.3f PC3=%.3f · 양성통제 z=%.3f"
          % (_mean_abs("PC1"), _mean_abs("PC2"), _mean_abs("PC3"), zc))

    def _coupled(k):
        hits = sum(1 for i in range(len(agg[k])) if abs(agg[k][i]) > THR and pvals[k][i] < 0.01)
        return hits >= (len(agg[k]) + 1) // 2

    z_ok = zc > 0.02
    coupled = [k for k in ("PC1", "PC2", "PC3") if _coupled(k)]
    print("")
    if not z_ok:
        v = "⛔ INVALID — 양성통제 z corr≈0(%.3f) = 계기가 emit 결합을 못 봄 · 음성 아님" % zc
    elif coupled:
        v = ("🔁 COUPLED — %s 가 emit-결합(과반수 run 에서 |r|>%.2f ∧ p<.01) ⇒ 라이브 축이 emit-무관이 "
             "아니었다 · H_9576 'emit-직교 DOF' 개념적 서사 재검" % ("·".join(coupled), THR))
    else:
        v = ("🟢 ORTHOGONAL — 모든 PC |r|<%.2f(과반수 run) ∧ 양성통제 통과 ⇒ 라이브 축은 emit-직교 · "
             "H_9576 'emit-직교 DOF' 서사는 이름표 불안정에도 라이브 축으로 유지" % THR)
    print("  ⇒ VERDICT: " + v)
    print("     범위: 상류 결합성이다 — mouth 도달/의미전달 미질문(H_9576 여전히 VOID) · 150tick×3run.")
    return 0


def _pc2_subspace_stability(argv):
    """H_9752 SUBSPACE-STABILITY — is H_9713's axis-flip a NEAR-DEGENERACY of a STABLE PLANE?

    `anima-py evaluate --pc2-direction <traces_dir> --subspace-stability [--dims 2]
        [--block 16,32] [--boot 1000] [--surr aaft] [--surrogates 500] [--seed N]`

    THE REFRAME THIS EXISTS TO TEST. H_9713 (--variance-audit) found that the frozen PC2 loading's
    NEAREST live eigenvector flips run-to-run (PC2 / PC1 / PC1 across the 3 seeds) and read that as
    "the axis LABEL is not reproducible live". This flag asks the sharper geometric question: an
    eigenvector RANK is an unstable label whenever lambda1 ~= lambda2 (near-degeneracy) EVEN WHEN
    the 2-D SUBSPACE span{v1,v2} is rock-stable. Rank is a coordinate; a plane is a geometry. So it
    measures the PLANE, not the axis:

      DV (all parameter-free / denominator-free geometry -- H_9716 non-applicable):
        - per-run raw-covariance eigenspectrum + relative eigengap (lambda1-lambda2)/lambda1
          (raw covariance = the SAME scale H_9713 saw the flip on, so the degeneracy is comparable)
        - cross-run PRINCIPAL ANGLES between top-`dims` subspaces (Procrustes via SVD of U^T V)
        - within-run SPLIT-HALF principal angles (does one run even have a stable plane internally?)
        - moving-block bootstrap (autocorrelation-respecting) -> principal-angle CI + RANK-SWAP rate
          (fraction of resamples where the top-2 eigenvector order trades = the degeneracy signature)

    THE NULLS (a small angle is only meaningful vs a chance angle; p7 -- collapse-delta, not a raw
    value; and autocorrelation shrinks n_eff so the chance level must be RE-DERIVED, never inherited
    from a uniform-Grassmann closed form):
      null-1 AAFT     -- phase surrogate per factor: preserves each channel's marginal AND its
                         autocorrelation, destroys ONLY the cross-channel coupling => the joint plane
                         is gone but the per-channel dynamics survive. The correct null for "is this
                         shared plane real?".
      null-2 chanperm -- permute the 8 channel labels of one run before refit: destroys the loading
                         IDENTITY, keeps per-channel dynamics. Second, independent null.

    POSITIVE CONTROL (opens nothing without it -- a_positive_control_first). A synthetic PLANT: N
    runs sharing ONE fixed random 2-D plane, each = 2 AR(1) latents (rho matched to the observed
    lag-1) on that plane + isotropic noise, n and top-2/bulk spectrum matched to the traces. The
    instrument MUST recover cross-run angle < the plant's own chanperm-null 5pct; if it cannot see a
    plane THAT IS THERE, the whole measurement is VOID (not a negative).

    9->3 RUN DEDUPE (H_9714 lesson): off/bias/rng share a byte-identical factor stream (Stage-A
    isolation), so the 9 files are 3 independent runs; they are deduped by factor-stream hash or the
    null is forged ~sqrt(3) too tight.

    FROZEN VERDICT TABLE (card H_9752 -- do not retune; a_break_the_wall):
      cross-run angle < AAFT-null 5pct AND rank-swap rate >= 0.2       -> PASS-PLANE
      split-half beats null AND cross-run is null-equivalent            -> PASS-RUN-INDEXED
      split-half itself null-equivalent AND plant PASS                  -> KILL-NO-AXIS
      cross-run angle ABOVE AAFT-null 95pct (anti-aligned)             -> INVALID (sign/pre-proc)
      plant not detected OR any run n<100 OR angle-CI half-width >10deg -> VOID (underpowered)
    KILL-NO-AXIS is the GATE for H_9754/9755's refit arms: if it fires, those arms have no target and
    firing them is forbidden -- that fact is written into the verdict.
    """
    import glob as _glob
    import json as _pj
    import numpy as _np

    FACTORS = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
               "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --subspace-stability")
        return 2
    dims = evaluate_intval(argv, "--dims", 2)
    nboot = evaluate_intval(argv, "--boot", 1000)
    nsurr = evaluate_intval(argv, "--surrogates", 500)
    rseed = evaluate_intval(argv, "--seed", 20260718)
    surr_kind = evaluate_strval(argv, "--surr", "aaft")
    blk_s = evaluate_strval(argv, "--block", "16,32")
    try:
        blocks = [int(b) for b in blk_s.split(",") if b.strip()]
    except ValueError:
        blocks = [16, 32]
    if not blocks:
        blocks = [16, 32]
    if surr_kind != "aaft":
        print("  ⇒ ⛔ --surr 은 현재 aaft 만 (null-2 chanperm 은 항상 병행)")
        return 2

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    # ── load + dedupe by factor stream (9 files -> 3 runs) ───────────────────
    runs, seen, dup, metas = [], set(), 0, []
    for f in files:
        rows, meta = [], {}
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                meta = r
                continue
            v = [r.get(k) for k in FACTORS]
            if any(x is None for x in v):
                continue
            rows.append([float(x) for x in v])
        if len(rows) < 20:
            continue
        X = _np.asarray(rows, dtype=_np.float64)
        h = hash(X.tobytes())
        if h in seen:
            dup += 1
            continue
        seen.add(h)
        runs.append((os.path.basename(f), X))
        metas.append((os.path.basename(f), meta))
    if len(runs) < 2:
        print("  ⇒ ⛔ 독립 run < 2 (교차-run 주각 불가) — dedupe 후 %d run" % len(runs))
        return 2

    # ── geometry helpers ─────────────────────────────────────────────────────
    def _subspace(X, k):
        """Top-k raw-covariance eigenvectors (orthonormal p×k), eigenvalues desc."""
        Xc = X - X.mean(axis=0)
        C = (Xc.T @ Xc) / float(Xc.shape[0] - 1)
        w, V = _np.linalg.eigh(C)
        o = _np.argsort(w)[::-1]
        return V[:, o[:k]], w[o]

    def _prin_angles(A, B):
        """Principal angles (deg, ascending) between orthonormal subspaces A,B (p×k)."""
        M = A.T @ B
        s = _np.linalg.svd(M, compute_uv=False)
        s = _np.clip(s, -1.0, 1.0)
        return _np.degrees(_np.arccos(s))[::-1]   # ascending angle

    def _theta_max(A, B):
        return float(_prin_angles(A, B)[-1])       # largest principal angle = worst misalign

    def _xrun_median(subs):
        """Median over run-pairs of the largest principal angle."""
        vals = []
        for i in range(len(subs)):
            for j in range(i + 1, len(subs)):
                vals.append(_theta_max(subs[i], subs[j]))
        return float(_np.median(vals)), vals

    def _lag1(X):
        rr = []
        for j in range(X.shape[1]):
            v = X[:, j] - X[:, j].mean()
            den = float((v * v).sum())
            rr.append(float((v[:-1] * v[1:]).sum() / den) if den > 0 else 0.0)
        return rr

    def _aaft(X, rng):
        n = X.shape[0]
        Y = _np.empty_like(X)
        for j in range(X.shape[1]):
            x = X[:, j]
            order = _np.argsort(x)
            g = _np.sort(rng.standard_normal(n))
            gx = _np.empty(n)
            gx[order] = g
            F = _np.fft.rfft(gx)
            ph = rng.uniform(0.0, 2.0 * _np.pi, size=F.shape[0])
            ph[0] = 0.0
            if n % 2 == 0:
                ph[-1] = 0.0
            Fs = _np.abs(F) * _np.exp(1j * ph)
            gs = _np.fft.irfft(Fs, n=n)
            back = _np.argsort(_np.argsort(gs))
            Y[:, j] = _np.sort(x)[back]
        return Y

    def _block_boot(X, L, rng):
        n = X.shape[0]
        if L >= n:
            L = max(2, n // 2)
        nb = int(_np.ceil(n / float(L)))
        idx = []
        for _ in range(nb):
            st = int(rng.integers(0, n - L + 1))
            idx.extend(range(st, st + L))
        idx = _np.asarray(idx[:n])
        return X[idx]

    print("=== anima evaluate --pc2-direction --subspace-stability — H_9752 라이브 평면 안정성 ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 인자스트림 %d 제외 · H_9714 dedupe)"
          % (d, len(files), len(runs), dup))
    print("dims=%d · block=%s · boot=%d · surrogate=%d · seed=%d"
          % (dims, blk_s, nboot, nsurr, rseed))
    print("질문:  H_9713 의 축-flip 은 **근축퇴(λ1≈λ2)** 이고 2-D 평면 span 은 run-안정인가?")
    print("DV:    주각(principal angle · 분모-프리) · 상대 eigengap · bootstrap rank-swap율")
    print("null:  ① AAFT(주변+자기상관 보존·결합만 파괴) ② 채널-라벨 순열 · 양성통제=합성 2-D plant")
    print("⚖️  raw-covariance 로 refit(H_9713 이 flip 을 본 바로 그 스케일) · 자기상관 존중 block-bootstrap")
    print("")

    # ── ⓪ regime diff ────────────────────────────────────────────────────────
    print("  ⓪ regime diff")
    for k in ("stage_cycle", "g_reach", "emit_gate", "refractory", "backend", "ckpt_sha256"):
        vals = sorted(set(str(m.get(k)) for _n, m in metas))
        print("     %-12s = %s" % (k, " | ".join(vals) if len(vals) > 1 else vals[0]))
    print("")

    # ── ① per-run eigenspectrum + relative eigengap ──────────────────────────
    print("  ① run별 eigenspectrum + 상대 eigengap (λ1−λ2)/λ1  (근축퇴 = eigengap 작음)")
    subs, eigs, ns = [], [], []
    for name, X in runs:
        U, w = _subspace(X, dims)
        subs.append(U)
        eigs.append(w)
        ns.append(X.shape[0])
        gap = float((w[0] - w[1]) / w[0]) if w[0] > 0 else 0.0
        print("     %-18s n=%-4d λ=[%s]  eigengap=%.3f"
              % (name, X.shape[0], " ".join("%.4f" % v for v in w[:4]), gap))
    min_n = min(ns)
    gaps = [float((w[0] - w[1]) / w[0]) if w[0] > 0 else 0.0 for w in eigs]
    print("     ⇒ 상대 eigengap: min=%.3f · median=%.3f · max=%.3f"
          % (min(gaps), float(_np.median(gaps)), max(gaps)))
    print("")

    # ── ② observed cross-run principal angles ────────────────────────────────
    xr_obs, xr_pairs = _xrun_median(subs)
    print("  ② 교차-run 주각 (top-%d 부분공간 · Procrustes)" % dims)
    pi = 0
    for i in range(len(subs)):
        for j in range(i + 1, len(subs)):
            ang = _prin_angles(subs[i], subs[j])
            print("     %-14s ↔ %-14s  주각=[%s]°"
                  % (runs[i][0], runs[j][0], " ".join("%.1f" % a for a in ang)))
            pi += 1
    print("     ⇒ 교차-run θ_max 중앙값 = %.2f°" % xr_obs)
    print("")

    # ── ③ within-run split-half ──────────────────────────────────────────────
    print("  ③ run 내 split-half 주각 (연속 전/후반 · 자기상관 존중)")
    sh_vals = []
    for name, X in runs:
        n = X.shape[0]
        h = n // 2
        UA, _ = _subspace(X[:h], dims)
        UB, _ = _subspace(X[h:], dims)
        t = _theta_max(UA, UB)
        sh_vals.append(t)
        print("     %-18s split-half θ_max=%.2f°" % (name, t))
    sh_obs = float(_np.median(sh_vals))
    print("     ⇒ split-half θ_max 중앙값 = %.2f°" % sh_obs)
    print("")

    # ── ④ nulls (AAFT + chanperm) ────────────────────────────────────────────
    rng = _np.random.default_rng(rseed)
    aaft_xr, chan_xr, aaft_sh = [], [], []
    for _ in range(nsurr):
        s_aaft = [_subspace(_aaft(X, rng), dims)[0] for _n, X in runs]
        aaft_xr.append(_xrun_median(s_aaft)[0])
        s_chan = []
        for _n, X in runs:
            perm = rng.permutation(X.shape[1])
            s_chan.append(_subspace(X[:, perm], dims)[0])
        chan_xr.append(_xrun_median(s_chan)[0])
        # split-half AAFT null (per run, median across runs)
        shs = []
        for _n, X in runs:
            Y = _aaft(X, rng)
            hh = Y.shape[0] // 2
            shs.append(_theta_max(_subspace(Y[:hh], dims)[0], _subspace(Y[hh:], dims)[0]))
        aaft_sh.append(float(_np.median(shs)))
    aaft_xr = _np.asarray(aaft_xr); chan_xr = _np.asarray(chan_xr); aaft_sh = _np.asarray(aaft_sh)
    aaft_p5, aaft_p95 = float(_np.percentile(aaft_xr, 5)), float(_np.percentile(aaft_xr, 95))
    chan_p5, chan_p95 = float(_np.percentile(chan_xr, 5)), float(_np.percentile(chan_xr, 95))
    sh_p5 = float(_np.percentile(aaft_sh, 5))
    print("  ④ null 대조 (분모-프리 주각 · 자기상관 존중 surrogate 서 재유도)")
    print("     교차-run θ_max: 관측=%.2f° · AAFT-null 5pct=%.2f° 95pct=%.2f° · chanperm 5pct=%.2f°"
          % (xr_obs, aaft_p5, aaft_p95, chan_p5))
    print("     split-half θ_max: 관측=%.2f° · AAFT-null 5pct=%.2f°" % (sh_obs, sh_p5))
    xr_below = xr_obs < aaft_p5
    xr_above = xr_obs > aaft_p95
    xr_chan_below = xr_obs < chan_p5
    sh_below = sh_obs < sh_p5
    print("     ⇒ 교차-run 평면 정렬(관측<AAFT5pct): %s · (관측<chanperm5pct): %s · 반정렬(>95pct): %s"
          % (xr_below, xr_chan_below, xr_above))
    print("     ⇒ split-half 평면 실재(관측<AAFT5pct): %s" % sh_below)
    print("")

    # ── ⑤ moving-block bootstrap: angle CI + rank-swap rate ──────────────────
    print("  ⑤ moving-block bootstrap (주각 CI + rank-swap율 · block 2종)")
    ci_halfwidths, swap_rates = [], []
    for L in blocks:
        boot_xr = []
        swaps = 0
        tot = 0
        for _ in range(nboot):
            s_boot = []
            for (name, X), Ufull in zip(runs, subs):
                Xb = _block_boot(X, L, rng)
                Ub, _w = _subspace(Xb, dims)
                s_boot.append(Ub)
                # rank-swap: does bootstrap PC1 align to full PC2 more than full PC1?
                b1 = Ub[:, 0]
                if abs(float(b1 @ Ufull[:, 0])) < abs(float(b1 @ Ufull[:, 1])):
                    swaps += 1
                tot += 1
            boot_xr.append(_xrun_median(s_boot)[0])
        boot_xr = _np.asarray(boot_xr)
        lo, hi = float(_np.percentile(boot_xr, 2.5)), float(_np.percentile(boot_xr, 97.5))
        hw = (hi - lo) / 2.0
        sr = swaps / float(tot) if tot else 0.0
        ci_halfwidths.append(hw)
        swap_rates.append(sr)
        print("     block=%-3d  교차-run θ_max CI=[%.2f, %.2f]° (반폭 %.2f°) · rank-swap율=%.3f"
              % (L, lo, hi, hw, sr))
    swap_rate = float(_np.mean(swap_rates))
    ci_halfwidth = float(_np.max(ci_halfwidths))
    print("     ⇒ rank-swap율(block-평균)=%.3f · 주각 CI 반폭(block-최대)=%.2f°"
          % (swap_rate, ci_halfwidth))
    print("")

    # ── ⑥ positive control: synthetic 2-D plant ──────────────────────────────
    print("  ⑥ 양성통제 — 합성 2-D plant (알려진 안정 평면 · n·스펙트럼 매칭)")
    p = len(FACTORS)
    nrun = len(runs)
    lam = _np.mean(_np.asarray(eigs), axis=0)          # avg observed raw-cov spectrum
    lat_sd = [float(lam[0] ** 0.5), float(lam[1] ** 0.5)]
    noise_sd = float(_np.mean(lam[dims:]) ** 0.5) if p > dims else float(lam[-1] ** 0.5)
    rho_ar = float(_np.clip(_np.mean([_np.mean(_lag1(X)) for _n, X in runs]), -0.95, 0.95))
    Q, _r = _np.linalg.qr(rng.standard_normal((p, dims)))   # ONE fixed plane
    Pplane = Q[:, :dims]

    def _ar1(n, rho, sd, rng):
        e = rng.standard_normal(n)
        x = _np.empty(n)
        x[0] = e[0]
        for t in range(1, n):
            x[t] = rho * x[t - 1] + e[t]
        s = x.std(ddof=1)
        return x / s * sd if s > 0 else x

    def _plant_run(n, rng):
        lat = _np.column_stack([_ar1(n, rho_ar, lat_sd[k], rng) for k in range(dims)])
        noise = rng.standard_normal((n, p)) * noise_sd
        return lat @ Pplane.T + noise

    plant_subs = [_subspace(_plant_run(min_n, rng), dims)[0] for _ in range(nrun)]
    plant_xr = _xrun_median(plant_subs)[0]
    plant_null = []
    for _ in range(max(200, nsurr // 2)):
        s_pn = []
        for U in plant_subs:
            perm = rng.permutation(p)
            # re-realize a plant run then channel-permute (chanperm null on the plant)
            Xp = _plant_run(min_n, rng)
            s_pn.append(_subspace(Xp[:, perm], dims)[0])
        plant_null.append(_xrun_median(s_pn)[0])
    plant_p5 = float(_np.percentile(_np.asarray(plant_null), 5))
    plant_detected = plant_xr < plant_p5
    print("     plant 교차-run θ_max=%.2f° · plant-chanperm null 5pct=%.2f° · 검출=%s"
          % (plant_xr, plant_p5, plant_detected))
    print("     (plant param: ρ_AR=%.2f · lat_sd=%s · noise_sd=%.3f · plane 고정)"
          % (rho_ar, "[%.3f,%.3f]" % (lat_sd[0], lat_sd[1]), noise_sd))
    print("")

    # ── VERDICT (frozen table · card H_9752) ─────────────────────────────────
    print("  ⑦ 사전등록 판정표 대조")
    if (not plant_detected) or (min_n < 100) or (ci_halfwidth > 10.0):
        why = []
        if not plant_detected:
            why.append("plant 미검출(계기가 있는 평면조차 못 봄)")
        if min_n < 100:
            why.append("run 당 tick<100 (min_n=%d)" % min_n)
        if ci_halfwidth > 10.0:
            why.append("주각 CI 반폭 %.1f°>10° (검정력 미달)" % ci_halfwidth)
        v = "⚪ VOID — " + " · ".join(why) + " ⇒ 음성 아님(power-before-negative)"
    elif xr_above:
        v = ("⛔ INVALID — 교차-run 주각이 AAFT-null **95pct 위**(반-정렬) ⇒ 부호규약/전처리 결함 · 수리 먼저")
    elif xr_below and swap_rate >= 0.2:
        v = ("🟢 **PASS-PLANE** — 교차-run 평면 안정(관측 %.1f° < AAFT5pct %.1f°) ∧ rank-swap율 %.3f≥0.2 "
             "⇒ H_9713 축-flip = **근축퇴 기전 확정**: 죽은 건 '축 이름'이지 2-D 평면이 아니다"
             % (xr_obs, aaft_p5, swap_rate))
    elif sh_below and not xr_below:
        v = ("🟡 **PASS-RUN-INDEXED** — run 내 split-half 는 null 이김(%.1f°<%.1f°)이나 교차-run 은 null 동급 "
             "⇒ 구조는 **run 단위로만** 존재 · H_9755 는 run 내 warmup-refit 만 유효" % (sh_obs, sh_p5))
    elif not sh_below:
        v = ("🧱 **KILL-NO-AXIS** — run 내 split-half 조차 null 동급(%.1f°≥%.1f°) ∧ plant PASS "
             "⇒ '라이브 축/평면' 자체가 없음 · **H_9754/9755 refit arm 개봉 금지** = 축-무관 가설(c)의 "
             "구조 측 증거 · 살아남는 것은 스칼라 dose(H_9664)뿐" % (sh_obs, sh_p5))
    else:
        v = ("🟡 MIXED — 사전등록 칸 밖(교차<AAFT5pct=%s·swap=%.3f·split-half<null=%s) ⇒ 강제 분류 금지"
             % (xr_below, swap_rate, sh_below))
    print("  ⇒ VERDICT: " + v)
    print("     ⚠️ n_eff≪n(H_9714 lag-1 ρ̂ 최대 0.86) — CI 는 block-bootstrap 이 자기상관 존중해 낸 것 ·")
    print("        판정은 주각의 **크기 vs surrogate**로 읽지 raw°로 읽지 말 것(p7).")
    return 0


def _pc2_variance_audit(argv):
    """H_9713 VARIANCE-AUDIT — does the certified PC2 axis carry its certified variance LIVE?

    `anima-py evaluate --pc2-direction <traces_dir> --variance-audit`

    THE DEFECT THIS EXISTS TO FIX. H_9468 certified PC2 as "31.5% of tension variance" from a PCA on
    one 150-tick run (reported lambda1=0.144, lambda2=0.048, lambda3=0.013, MP edge=0.0287; the
    eigenvalue sum ~0.15 != 8 says it was RAW COVARIANCE, not correlation). If that holds live, the
    unit-norm loading applied to the raw factors must give sd(z) = sqrt(lambda2) = 0.219.
    The live census says otherwise. But until now those two numbers came from TWO DIFFERENT H's ON
    TWO DIFFERENT INSTRUMENTS -- a comparison that was never made under one roof. That is the actual
    defect: not the gap, but that nobody measured both at once. This flag does exactly that.

    POSITIVE CONTROL (opens nothing without it): PC1 (certified 51.5%, sqrt(lambda1)=0.279). If PC1
    reproduces its certified sd live but PC2 does not, the problem is PC2-specific and hands off to
    H_9712. If PC1 ALSO collapses, the whole H_9468 PCA is from another regime and every card
    resting on that frozen loading (H_9574/9576/9630-9634) loses its upstream basis.

    SCALE DISCIPLINE (learned in H_9714): H_9468's lambdas are RAW-COVARIANCE. So this audit fits raw
    covariance too -- correlation-scale eigenvalues (sum=8) are NOT comparable to them, and reporting
    the two on one axis would be the same category error H_9714 caught.

    REGIME DIFF: it also diffs the trace metas (stage_cycle / g_reach / emit_gate / refractory) so the
    code answers "was it even the same regime?" instead of the reader assuming it.
    """
    import glob as _glob
    import json as _pj
    import numpy as _np

    ALL8 = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
            "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]
    Z_IDX = [ALL8.index(k) for k in ("nov_ctx", "bal_lane", "coh_lane")]
    Z_W = _np.array([0.84, -0.44, -0.28])
    # H_9468 reported (raw-covariance scale) -- the certified numbers under audit
    L1_CERT, L2_CERT, EDGE_CERT = 0.144, 0.048, 0.0287

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --variance-audit")
        return 2

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    runs, seen, dup, metas = [], set(), 0, []
    for f in files:
        rows, zs, meta = [], [], {}
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                meta = r
                continue
            v = [r.get(k) for k in ALL8]
            if any(x is None for x in v):
                continue
            rows.append([float(x) for x in v])
            if r.get("pc2_z") is not None:
                zs.append(float(r["pc2_z"]))
        if len(rows) < 20:
            continue
        X = _np.asarray(rows, dtype=_np.float64)
        h = hash(X.tobytes())
        if h in seen:
            dup += 1
            continue
        seen.add(h)
        runs.append((os.path.basename(f), X, zs))
        metas.append((os.path.basename(f), meta))

    if not runs:
        print("  ⇒ ⛔ 8-인자를 가진 트레이스 없음")
        return 2

    print("=== anima evaluate --pc2-direction --variance-audit — H_9713 regime 감사 ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 %d 제외 · H_9714 교훈)" % (d, len(files), len(runs), dup))
    print("질문:  인증된 PC2(H_9468 · 31.5%%)가 **라이브서 그 분산을 내나** — 두 숫자를 **한 계기서** 산출")
    print("인증치(원-공분산 스케일): λ₁=%.3f(√=%.3f) · λ₂=%.3f(√=%.3f) · MP edge=%.4f"
          % (L1_CERT, L1_CERT ** 0.5, L2_CERT, L2_CERT ** 0.5, EDGE_CERT))
    print("⚖️ 스케일 규율(H_9714 교훈): H_9468 λ 는 **원-공분산** ⇒ 이 감사도 원-공분산으로 적합한다")
    print("   (상관-스케일 λ(Σ=8)은 인증치와 **비교 불가** — 같은 축에 놓으면 H_9714 가 잡은 그 범주오류).")
    print("")

    # ── regime diff: was it even the same regime? ───────────────────────────
    print("  ⓪ regime diff (트레이스 메타 · '같은 regime 이었나'를 코드가 답한다)")
    keys = ("stage_cycle", "g_reach", "emit_gate", "refractory", "backend", "ckpt_sha256")
    base = None
    for name, m in metas[:1]:
        base = m
    for k in keys:
        vals = sorted(set(str(m.get(k)) for _n, m in metas))
        print("     %-12s = %s" % (k, " | ".join(vals) if len(vals) > 1 else vals[0]))
    print("     ⚠️ H_9468 원 트레이스의 메타는 **이 디렉터리에 없다** — 카드가 요구한 'H_9468 regime vs pmp")
    print("        regime' 대조는 **미수행**(그 트레이스가 보존돼 있어야 가능) ⇒ 아래는 라이브 쪽 절반만이다.")
    print("")

    print("  ① 라이브 원-공분산 재적합 (같은 계기 · 같은 run)")
    l1s, l2s, sd1s, sd2s, sdzs = [], [], [], [], []
    for name, X, zs in runs:
        Xc = X - X.mean(axis=0)
        C = (Xc.T @ Xc) / float(Xc.shape[0] - 1)          # RAW covariance (H_9468 scale)
        w, V = _np.linalg.eigh(C)
        order = _np.argsort(w)[::-1]
        w = w[order]
        V = V[:, order]
        pc1_live = float(_np.std(Xc @ V[:, 0], ddof=1))
        pc2_live = float(_np.std(Xc @ V[:, 1], ddof=1))
        # z as the engine computes it: frozen loading on the RAW 3 factors
        z_recon = float(_np.std(X[:, Z_IDX] @ Z_W, ddof=1))
        sdz = float(_np.std(zs, ddof=1)) if len(zs) > 1 else 0.0
        l1s.append(w[0]); l2s.append(w[1])
        sd1s.append(pc1_live); sd2s.append(pc2_live); sdzs.append(sdz)
        print("     %-18s λ_live=[%.4f %.4f %.4f] · sd(PC1)=%.4f · sd(PC2)=%.4f"
              % (name, w[0], w[1], w[2], pc1_live, pc2_live))
        print("        sd(z) 트레이스=%.4f · 동결-loading 재구성=%.4f  (일치=계기 무결)" % (sdz, z_recon))

    l1 = sum(l1s) / len(l1s); l2 = sum(l2s) / len(l2s)
    sd1 = sum(sd1s) / len(sd1s); sd2 = sum(sd2s) / len(sd2s); sdz = sum(sdzs) / len(sdzs)

    # ── direction/identity: is the frozen axis still the SECOND DOF live? ────
    # H_9713 v1 concluded "the frozen loading is invalid live" from the amplitude alone. That was
    # imprecise: an axis can keep its direction and lose its RANK. So ask the sharper question --
    # which live eigenvector does the frozen loading actually point along?
    print("")
    print("  ①-b 방향/정체성 — 동결 loading 은 **라이브서 여전히 제2 DOF 인가**")
    fz = _np.zeros(8)
    fz[ALL8.index("nov_ctx")] = 0.84
    fz[ALL8.index("bal_lane")] = -0.44
    fz[ALL8.index("coh_lane")] = -0.28
    fz = fz / _np.linalg.norm(fz)
    cos_by_run = []
    for name, X, zs in runs:
        Xc = X - X.mean(axis=0)
        C = (Xc.T @ Xc) / float(Xc.shape[0] - 1)
        w, V = _np.linalg.eigh(C)
        o = _np.argsort(w)[::-1]
        V = V[:, o]
        cs = [abs(float(_np.dot(fz, V[:, k]))) for k in range(3)]
        cos_by_run.append(cs)
        best = int(_np.argmax(cs)) + 1
        print("     %-18s |cos∠| vs 라이브 PC1=%.3f PC2=%.3f PC3=%.3f  ⇒ **최근접 = PC%d**"
              % (name, cs[0], cs[1], cs[2], best))
    cm = _np.mean(_np.asarray(cos_by_run), axis=0)
    nearest = int(_np.argmax(cm)) + 1
    print("     run-평균: PC1=%.3f · PC2=%.3f · PC3=%.3f ⇒ 동결 loading 의 **최근접 라이브 축 = PC%d**"
          % (cm[0], cm[1], cm[2], nearest))
    per_run_nearest = [int(_np.argmax(cs)) + 1 for cs in cos_by_run]
    consistent = len(set(per_run_nearest)) == 1
    if not consistent:
        print("     ⚠️ **run 간 불일치** — 최근접 축이 run 마다 다르다: %s"
              % " ".join("PC%d" % k for k in per_run_nearest))
        print("        ⇒ '동결 PC2 = 라이브 PCk' 로 **단정 불가**. run-평균(PC%d)은 그 불일치를 가린다." % nearest)
        print("        말할 수 있는 것은 이것뿐: **동결 축의 라이브 RANK 가 안정적이지 않다** —")
        print("        같은 ckpt·같은 프로토콜의 3 run 이 서로 다른 축에 정렬한다 = 인증된 'PC2' 라는")
        print("        **이름표가 라이브서 재현되지 않는다**(방향 자체의 무효와는 다른 주장).")
    elif nearest == 1:
        print("     🔑 **동결 'PC2' 가 라이브서 일관되게 PC1** (3/3 run) — 방향 무효가 아니라 **RANK 변경**.")
        print("        ⇒ H_9574/9576/9630~9634 가 민 것은 '버려진 제2 DOF' 가 아니라 **지배축**일 수 있다")
        print("        (⚠️ 라이브 PC1 이 emit-결합인지는 **이 계기가 안 묻는다** — 별도 측정 필요).")

    print("")
    print("  ② 인증치 대비 (run-평균 · 한 계기서 나온 숫자끼리)")
    print("     %-22s 인증 %.4f · 라이브 %.4f · 비 %.2f×" % ("λ₁", L1_CERT, l1, l1 / L1_CERT if L1_CERT else 0))
    print("     %-22s 인증 %.4f · 라이브 %.4f · 비 %.2f×" % ("λ₂", L2_CERT, l2, l2 / L2_CERT if L2_CERT else 0))
    print("     %-22s 인증 %.4f · 라이브 %.4f · 비 %.2f×  ← 양성통제"
          % ("sd(PC1) vs √λ₁", L1_CERT ** 0.5, sd1, sd1 / (L1_CERT ** 0.5)))
    print("     %-22s 인증 %.4f · 라이브 %.4f · 비 %.2f×"
          % ("sd(PC2) vs √λ₂", L2_CERT ** 0.5, sd2, sd2 / (L2_CERT ** 0.5)))
    print("     %-22s 인증 %.4f · 라이브 %.4f · 비 %.2f×  ← 엔진의 z"
          % ("sd(z)  vs √λ₂", L2_CERT ** 0.5, sdz, sdz / (L2_CERT ** 0.5)))

    r1 = sd1 / (L1_CERT ** 0.5)
    r2 = sd2 / (L2_CERT ** 0.5)
    pc1_ok = 0.75 <= r1 <= 1.25            # pre-registered +-25%
    pc2_low = r2 < 0.75

    print("")
    if r1 > 1.25 and r2 > 1.25:
        v = ("⛔ INVALID — **양축 모두 인증치 초과**(sd_live > √λ) = 표준화/스케일 스큐(공분산 vs 상관 혼선) "
             "⇒ 어느 쪽이 거짓말인지 먼저")
    elif pc1_ok and pc2_low:
        v = ("🟢 **PASS-pc2-specific** — PC1 은 인증 sd 를 ±25% 안에 재현(%.2f×)하는데 PC2 만 라이브서 죽음"
             "(%.2f×) ⇒ regime 은 정합 · 문제는 **PC2 특정** ⇒ H_9712 로 인계" % (r1, r2))
    elif not pc1_ok and r1 < 0.75:
        v = ("🧱 **KILL-regime-stale** — **양성통제 PC1 도 무너짐**(%.2f×) ⇒ H_9468 PCA 는 다른 regime. "
             "⚠️ 정밀화: 무효인 것은 **loading 의 방향이 아니라 그것이 지시하던 것**(위 ①-b 참조) — "
             "라이브-refit 필수 · H_9574/9576/9630~9634 상류 근거 재작성" % r1)
    elif pc1_ok and not pc2_low:
        v = ("⛔ INVALID — 둘 다 인증 √λ 재현 ⇒ z-census 의 '분산 부족' 서사와 **정면 모순** "
             "⇒ 계기 충돌(어느 쪽이 거짓말인지 먼저)")
    else:
        v = ("🟡 MIXED — PC1 %.2f× · PC2 %.2f× 가 사전등록 칸에 안 떨어짐 ⇒ 강제 분류 금지" % (r1, r2))
    print("  ⇒ VERDICT: " + v)
    print("     ⚠️ 자기상관 짝(H_9714 실측 lag-1 ρ̂ coh=0.86·bal=0.80·nov=0.74) ⇒ n_eff ≪ n ·")
    print("        sd 의 CI 는 명목보다 넓다 — 이 판정은 **비(ratio)의 크기**로 읽지 미세차로 읽지 말 것.")
    return 0


def _pc2_stage_slave(argv):
    """H_9715 STAGE-SLAVE — are "emit = f(stage)" and "z is flat" one root, or two?

    `anima-py evaluate --pc2-direction <traces_dir> --stage-slave`   (predictions 1-2 · $0)

    THE UNIFYING HYPOTHESIS. H_9400 showed engine-native that emit is a pure function of stage
    (H(emit|stage)=0.465) and that the Psi=1/2 pull never operated. Separately, this lane found z
    near-flat. If the 8 tension factors are SLAVED TO STAGE, those are not two facts -- they are one
    root, and two frontiers (Psi-half and mouth/tension) collapse into a single question.

    PREDICTIONS (all three must hold for PASS-single-root):
      1. eta^2(z ~ stage) > 0.5              -- z is a step function of stage
      2. the z>0 ticks coincide with stage transitions / stage_env changes
      3. sd(z) at stage_cycle=true >= 2x sd(z) at stage_cycle=false   (pool -- not this flag)

    POSITIVE CONTROL (opens nothing without it): `score`/`base_motiv` MUST be stage-slaved
    (eta^2_score > 0.5), because H_9400 already certified emit=f(stage) engine-native. If score does
    not show it either, the trace or this instrument is broken -- not z.

    THE VOID THAT MATTERS. The pre-registered table reserves a cell: "stage has only 1 level =>
    predictions 1-2 are unobservable in principle => VOID, only prediction 3 survives". That cell is
    about POWER, not about z: eta^2 needs cells with n>=30, and a stage axis pinned to one value
    cannot support the contrast no matter what z does. This flag checks that FIRST and refuses to
    read 1-2 off an unbalanced axis -- reporting a degenerate stage census as a z-result is exactly
    how a measurement lies.
    """
    import glob as _glob
    import json as _pj
    import numpy as _np

    MIN_CELL = 30            # pre-registered: eta^2 needs n>=30 per cell
    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --stage-slave")
        return 2

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    runs, seen, dup = [], set(), 0
    for f in files:
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                continue
            rows.append(r)
        if len(rows) < 20:
            continue
        sig = tuple((r.get("stage"), r.get("pc2_z"), r.get("score")) for r in rows)
        h = hash(repr(sig))
        if h in seen:
            dup += 1
            continue
        seen.add(h)
        runs.append((os.path.basename(f), rows))
    if not runs:
        print("  ⇒ ⛔ 사용 가능한 run 없음")
        return 2

    print("=== anima evaluate --pc2-direction --stage-slave — H_9715 예측1·2 ($0) ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 %d 제외 · H_9714 교훈)" % (d, len(files), len(runs), dup))
    print("가설:  'emit=f(stage)'(H_9400 · H(emit|stage)=0.465)와 'z 상수' 가 **하나의 뿌리**인가")
    print("       = 8 tension 인자가 stage 에 **노예화**됐나 ⇒ Ψ½ 와 mouth 두 프런티어가 통합")
    print("bar:   η²(z~stage)>0.5 (예측1) · 양성통제 η²_score>0.5 · **셀당 n≥%d**" % MIN_CELL)
    print("")

    def _eta2(groups):
        """eta^2 = between-group SS / total SS."""
        allv = [v for g in groups.values() for v in g]
        if len(allv) < 3:
            return None
        gm = sum(allv) / float(len(allv))
        sst = sum((v - gm) ** 2 for v in allv)
        if sst <= 0:
            return None
        ssb = sum(len(g) * (sum(g) / float(len(g)) - gm) ** 2 for g in groups.values() if g)
        return ssb / sst

    # ── stage census FIRST: the power gate, before any z claim ──────────────
    print("  ① stage 축 인구조사 (예측1·2 의 관측가능성 게이트)")
    usable_runs = 0
    for name, rows in runs:
        cnt = {}
        for r in rows:
            cnt[r.get("stage")] = cnt.get(r.get("stage"), 0) + 1
        tot = sum(cnt.values())
        top_k = max(cnt, key=lambda k: cnt[k])
        big = [k for k in cnt if cnt[k] >= MIN_CELL]
        ok = len(big) >= 2
        usable_runs += 1 if ok else 0
        print("     %-18s stage 분포 %s" % (name, dict(sorted((k, v) for k, v in cnt.items()))))
        print("        최빈 stage=%s 가 %d/%d = **%.1f%%** · n≥%d 셀 %d개 ⇒ 대조 %s"
              % (top_k, cnt[top_k], tot, 100.0 * cnt[top_k] / tot, MIN_CELL, len(big),
                 "가능" if ok else "**불가**"))

    if usable_runs == 0:
        print("")
        print("  ⇒ ⛔ **VOID (사전등록 '우연 아래' 칸)** — stage 축이 사실상 한 수준에 pin 돼 있다")
        print("     (n≥%d 셀이 2개 미만) ⇒ **예측1·2 는 원리적으로 관측 불가**." % MIN_CELL)
        print("     이건 z 에 대한 음성이 **아니다** — 대조축 자체가 없어서 못 재는 것이다.")
        print("")
        print("  🔑 그런데 이 VOID 자체가 발견이다:")
        print("     `stage = dr_stage_at(tick*8)` (stage_cycle=false · 프로덕션 기본값) ⇒ tick 이 단조증가하니")
        print("     stage 가 끝 수준으로 진행해 **거기 머문다**. 즉 라이브 데몬은 사실상 **단일 stage** 에서 산다.")
        print("     ⇒ H_9400 의 H(emit|stage)=0.465 도 **거의 상수인 조건변수**에 대한 값이다(재검 대상).")
        print("     ⇒ 남은 유효 검정은 **예측3 뿐**: `anima-py chat --pc2-zeta --stage-cycle` (pool · mac 금지)")
        print("        — stage_cycle=true 는 (tick*8)%%90 로 stage 를 **순환**시킨다(cli/chat.py:1737).")
        return 0

    # ── predictions 1-2 (only reachable when the stage axis supports a contrast) ──
    print("")
    print("  ② 예측1: η²(z ~ stage) · 양성통제 η²(score ~ stage)")
    e_z, e_s = [], []
    for name, rows in runs:
        gz, gs = {}, {}
        for r in rows:
            st = r.get("stage")
            if r.get("pc2_z") is not None:
                gz.setdefault(st, []).append(float(r["pc2_z"]))
            if r.get("score") is not None:
                gs.setdefault(st, []).append(float(r["score"]))
        gz = {k: v for k, v in gz.items() if len(v) >= MIN_CELL}
        gs = {k: v for k, v in gs.items() if len(v) >= MIN_CELL}
        ez, es = _eta2(gz), _eta2(gs)
        if ez is not None:
            e_z.append(ez)
        if es is not None:
            e_s.append(es)
        print("     %-18s η²(z~stage)=%s · η²(score~stage)=%s"
              % (name, ("%.3f" % ez) if ez is not None else "n/a",
                 ("%.3f" % es) if es is not None else "n/a"))
    ez_m = sum(e_z) / float(len(e_z)) if e_z else None
    es_m = sum(e_s) / float(len(e_s)) if e_s else None
    print("")
    print("  run-평균: η²(z~stage)=%s · η²(score~stage)=%s (양성통제)"
          % (("%.3f" % ez_m) if ez_m is not None else "n/a",
             ("%.3f" % es_m) if es_m is not None else "n/a"))
    print("")
    if es_m is None or es_m < 0.5:
        v = ("⛔ INVALID — **양성통제 실패**(η²_score=%s < 0.5) = H_9400 의 emit=f(stage) 재현 실패 ⇒ "
             "트레이스/계기 스큐 · **음성 아님**" % (("%.3f" % es_m) if es_m is not None else "n/a"))
    elif ez_m is not None and ez_m > 0.5:
        v = ("🟡 예측1 PASS (η²=%.3f>0.5) — z 는 stage 의 계단함수 ⇒ 예측2·3 필요(3 = pool "
             "`chat --pc2-zeta --stage-cycle`)" % ez_m)
    elif ez_m is not None and ez_m < 0.1:
        v = ("🧱 **KILL-separate-roots** — 양성통제 생존(η²_score=%.3f) 한 채 z 만 stage-무관(η²=%.3f<0.1) "
             "⇒ 브리핑 (c) 답 = **별개 뿌리**" % (es_m, ez_m))
    else:
        v = "🟡 MIXED — η²(z~stage)=%.3f 가 0.1~0.5 사이 · 단일 원인으로 못 박지 말 것" % (ez_m or 0.0)
    print("  ⇒ VERDICT: " + v)
    return 0


def _pc2_factor_census(argv):
    """H_9712 FACTOR-CENSUS — is the live z constant because the FACTORS are flat, or because the
    FROZEN LOADING points where they do not move?

    `anima-py evaluate --pc2-direction <traces_dir> --factor-census [--seed N]`

    THE FORK. z = 0.84*nov_ctx - 0.44*bal_lane - 0.28*coh_lane (core/brain.py) is near-constant live
    (--z-census: IQR 0.0514, 45.7% of its variance in 3/270 ticks). Exactly two things can cause that:

      (1) DEGENERATE  -- the three factors are each flat, i.e. the substrate's tension itself is
                         degenerate. That is an UPSTREAM finding, and it would reframe the whole
                         mouth lane: the problem would not be the axis, it would be the substrate.
      (2) CANCEL      -- the factors do move, but the FROZEN loading (H_9468, fit on one 150-tick
                         run) is oriented where they do not. Then the loading is the culprit and a
                         live-refit axis is the follow-on.

    These split IN THE SAME TRACE: per-factor standardised sd separates them, and the angle between
    the frozen loading and the live 3x3 principal eigenvector says whether the frozen axis even
    points along the live variation.

    TRUNCATION IS ACQUITTED IN ADVANCE (ledger arithmetic, no new measurement): PC2 is a UNIT
    eigenvector, so 0.84^2 + 0.44^2 + 0.28^2 = 0.9776 -- the implemented 3 terms carry 97.8% of the
    loading energy and the 5 dropped factors carry 2.2% (norm 0.149). Dropping them shaves sd(z) by
    at most ~1.1%, which cannot explain a 2.2-5.8x shortfall. So this is a 2-way fork, not 3-way.

    POSITIVE CONTROL (opens nothing without it): PC1 (coherence-dominated, the certified 51.5% axis)
    must MOVE live. If PC1 is flat too, the instrument or the regime is broken -- not PC2 -- and the
    verdict is VOID, handing off to H_9713 rather than claiming anything about PC2.

    DEDUPE (learned the hard way in H_9714): a trace dir holds one file per (arm, seed), but the arms
    share a byte-identical factor stream -- steering happens after emit and never feeds back into
    tension (Stage-A isolation). Counting all 9 would triple-count 3 runs and forge tighter CIs.
    """
    import glob as _glob
    import json as _pj
    import numpy as _np

    Z_FACTORS = ["nov_ctx", "bal_lane", "coh_lane"]          # the 3 z carries
    Z_W = _np.array([0.84, -0.44, -0.28])                    # H_9468 frozen loading
    ALL8 = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
            "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --factor-census")
        return 2
    rseed = evaluate_intval(argv, "--seed", 20260717)

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    mats, seen, dup = [], set(), 0
    for f in files:
        rows, zs = [], []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                continue
            v = [r.get(k) for k in ALL8]
            if any(x is None for x in v):
                continue
            rows.append([float(x) for x in v])
            zs.append(r.get("pc2_z"))
        if len(rows) < 20:
            continue
        X = _np.asarray(rows, dtype=_np.float64)
        key = hash(X.tobytes())
        if key in seen:
            dup += 1
            continue
        seen.add(key)
        mats.append((os.path.basename(f), X, [float(z) for z in zs if z is not None]))
    if not mats:
        print("  ⇒ ⛔ 인자를 모두 가진 트레이스 없음")
        return 2

    print("=== anima evaluate --pc2-direction --factor-census — H_9712 z 3인자 분해 ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 인자스트림 %d 제외 · H_9714 교훈)"
          % (d, len(files), len(mats), dup))
    print("질문:  z 가 상수인 것은 **인자 축퇴**(①)인가 **loading 상쇄**(②)인가?")
    print("bar:   3인자 표준화 sd 전부 <0.10 ⇒ PASS-degenerate / ≥2 인자 sd≥0.10 ∧ |cos∠|<0.30 ⇒ PASS-cancel")
    print("절단:  0.84²+0.44²+0.28² = %.4f ⇒ 3항이 loading 에너지의 97.8%% · 절단은 무죄(사전 산술)"
          % float((Z_W ** 2).sum()))
    print("")

    idx = [ALL8.index(k) for k in Z_FACTORS]
    all_sd_raw, all_sd_std, all_cos, all_sdz, all_pc1sd = [], [], [], [], []
    for name, X, zs in mats:
        Z3 = X[:, idx]
        sd_raw = Z3.std(axis=0, ddof=1)
        # standardised sd = sd on the [min,max] range scale of THIS run's factor (a factor pinned to
        # a constant has range 0 -> report 0 rather than dividing by zero)
        rng = Z3.max(axis=0) - Z3.min(axis=0)
        sd_std = _np.where(rng > 0, sd_raw / _np.where(rng > 0, rng, 1.0), 0.0)
        # live 3x3 principal eigenvector (correlation scale so no factor's raw units dominate)
        Zc = Z3 - Z3.mean(axis=0)
        s = Zc.std(axis=0, ddof=1)
        s[s == 0] = 1.0
        Zs = Zc / s
        C3 = (Zs.T @ Zs) / float(Zs.shape[0] - 1)
        w, V = _np.linalg.eigh(C3)
        v_hat = V[:, int(_np.argmax(w))]
        wn = Z_W / _np.linalg.norm(Z_W)
        cosang = float(abs(_np.dot(v_hat, wn)))
        sdz = float(_np.std(zs, ddof=1)) if len(zs) > 1 else 0.0
        # positive control: PC1 = coherence-dominated axis over the full 8 (certified 51.5%)
        X8c = X - X.mean(axis=0)
        s8 = X8c.std(axis=0, ddof=1)
        s8[s8 == 0] = 1.0
        X8s = X8c / s8
        C8 = (X8s.T @ X8s) / float(X8s.shape[0] - 1)
        w8, V8 = _np.linalg.eigh(C8)
        pc1 = V8[:, int(_np.argmax(w8))]
        pc1_series = X8s @ pc1
        pc1_sd = float(pc1_series.std(ddof=1))
        all_sd_raw.append(sd_raw); all_sd_std.append(sd_std); all_cos.append(cosang)
        all_sdz.append(sdz); all_pc1sd.append(pc1_sd)
        print("  %-18s n=%-4d" % (name, X.shape[0]))
        print("     인자 sd(원)  : " + " ".join("%s=%.4f" % (Z_FACTORS[j][:3], sd_raw[j]) for j in range(3)))
        print("     인자 sd(표준): " + " ".join("%s=%.4f" % (Z_FACTORS[j][:3], sd_std[j]) for j in range(3))
              + "   (<0.10 = 축퇴 문턱)")
        print("     cos∠(frozen loading, 라이브 주고유벡터) = %.3f · sd(z)=%.4f · PC1 sd=%.3f(양성통제)"
              % (cosang, sdz, pc1_sd))

    sd_std_m = _np.mean(_np.asarray(all_sd_std), axis=0)
    cos_m = float(_np.mean(all_cos))
    sdz_m = float(_np.mean(all_sdz))
    pc1_m = float(_np.mean(all_pc1sd))

    print("")
    print("  run-평균: 표준화 sd = [%s] · cos∠=%.3f · sd(z)=%.4f · PC1 sd=%.3f"
          % (" ".join("%.4f" % v for v in sd_std_m), cos_m, sdz_m, pc1_m))

    n_flat = int((sd_std_m < 0.10).sum())
    n_move = int((sd_std_m >= 0.10).sum())
    pc1_alive = pc1_m > 0.5          # a standardised PC1 score has sd ~1 when the axis is alive

    print("")
    if not pc1_alive:
        v = ("⛔ VOID — **양성통제 실패**(PC1 도 상수 sd=%.3f) ⇒ regime/계기 문제이지 PC2 고유문제 아님 "
             "· H_9713 선행" % pc1_m)
    elif n_flat == 3:
        v = ("🔑 **PASS-degenerate — 상류 대발견**: 3인자가 각각 축퇴(전부 표준화 sd<0.10) ⇒ 기질 tension "
             "자체가 축퇴 ⇒ mouth lane 전체 재프레임(문제는 축이 아니라 기질)")
    elif n_move >= 2 and cos_m < 0.30:
        v = ("🔑 **PASS-cancel — loading 이 범인**: ≥2 인자가 움직이는데(sd≥0.10) 동결 축이 라이브 변동과 "
             "거의 직교(|cos∠|=%.3f<0.30) ⇒ 라이브-refit 축 후속(H_9713)" % cos_m)
    elif n_move >= 1 and cos_m > 0.70 and sdz_m < 0.05:
        v = ("⛔ INVALID — 정렬됐는데(|cos∠|=%.3f>0.70) z 가 안 움직임(sd=%.4f) = **산술 모순** ⇒ z 계산경로 "
             "누수 점검(core/brain.py)" % (cos_m, sdz_m))
    else:
        v = ("🟡 MIXED — 사전등록 칸 어디에도 깨끗이 안 떨어짐(flat %d/3 · |cos∠|=%.3f) ⇒ 단일 원인으로 "
             "못 박지 말 것 · 카드에 그대로 기록" % (n_flat, cos_m))
    print("  ⇒ VERDICT: " + v)
    print("     범위: 이건 **상류 인자 분해**다 — mouth 도달·의미전달을 묻지 않는다(H_9576 은 여전히 VOID).")
    return 0


def _pc2_rank_null(argv):
    """H_9714 RANK-NULL — is the tension "rank 2.66" an artifact of applying MP to autocorrelated series?

    `anima-py evaluate --pc2-direction <traces_dir> --rank-null {iid|phase} [--surrogates N] [--seed N]`

    THE UPSTREAM QUESTION NOBODY ASKED. H_9428/H_9468 read effective rank 2.66/8 off a
    Marchenko-Pastur noise edge and named PC2 (originality<->balance) a real, emit-orthogonal DOF.
    Every later card in this lane -- H_9574 (route it), H_9576 (does it carry meaning?), H_9630-9634
    -- assumed that axis EXISTS and asked what it does. This asks whether it is there at all.

    MP assumes i.i.d. samples. The tension factors are not: they are EMA-smoothed series
    (rel_ema/cur_ema/ten_ema) plus refr_debt/idle. Autocorrelation shrinks the effective sample,
    which RAISES the noise edge -- and from H_9468's own reported numbers (n=150, p=8, edge=0.0287
    => sigma^2=0.01894), lambda2=0.048 sinks under the edge once rho > 0.736, while lambda1=0.144
    survives until rho > 0.904. That gap is what makes this decidable: it hands us a POSITIVE
    CONTROL for free (lambda1 must survive a null that lambda2 dies to).

    WHY IT EXPLAINS THREE WALLS AT ONCE. A noise eigenvector is, BY CONSTRUCTION, (i) near-constant
    live (there is no signal in it -- matching z's IQR 0.0514), (ii) unable to move the mouth
    meaningfully (matching H_9576's rho=-0.077 null), and (iii) an inflater of sample rank (2.66).
    So z-degeneracy, the H_9576 direction-null, and rank 2.66 may be ONE root -- not a wall, but us
    trying to steer an axis that was never there.

    THE NULLS.
      iid   -- per-factor tick shuffle. Destroys autocorrelation => reproduces MP's own assumption.
               A cheap screen: if lambda2 sinks under even THIS null, H_9468's MP arithmetic was
               already wrong before any autocorrelation correction (INVALID-original).
      phase -- AAFT (amplitude-adjusted Fourier transform) surrogate: preserves each factor's
               marginal distribution AND its autocorrelation, destroying ONLY the cross-factor
               coupling. That is the correct null for "is this joint structure real?", and it is
               where the verdict lives -- the rho*=0.736 threshold is a prediction, not a judge
               (the AR(1) n_eff <-> eigenvalue-inflation map is an approximation, and MP also
               assumes equal factor variances, which these factors do not have).
    """
    import glob as _glob
    import json as _pj
    import random as _prand
    import numpy as _np

    FACTORS = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
               "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    mode = "phase"
    for i, a in enumerate(argv):
        if a == "--rank-null" and i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            mode = argv[i + 1]
    if mode not in ("iid", "phase"):
        print("  ⇒ ⛔ --rank-null 은 iid | phase")
        return 2
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --rank-null {iid|phase}")
        return 2
    ns = evaluate_intval(argv, "--surrogates", 200)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    # One matrix per trace file: a surrogate must respect each run's own time axis, so runs are
    # never concatenated (that would forge an autocorrelation break at every seam).
    mats = []
    seen_streams = set()
    dup = 0
    for f in files:
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                continue
            v = [r.get(k) for k in FACTORS]
            if any(x is None for x in v):
                continue
            rows.append([float(x) for x in v])
        if len(rows) >= 20:
            # DEDUPE BY FACTOR STREAM. The trace dir holds one file per (arm, seed), but the arms
            # (off/bias/rng) share a byte-identical factor stream -- steering happens AFTER emit and
            # never feeds back into tension (Stage-A isolation). Keeping all 9 would triple-count 3
            # runs and forge a null distribution ~sqrt(3) too tight. Verified on the live traces:
            # off/bias/rng factor tuples compare EQUAL for every seed.
            X = _np.asarray(rows, dtype=_np.float64)
            key = hash(X.tobytes())
            if key in seen_streams:
                dup += 1
                continue
            seen_streams.add(key)
            mats.append((os.path.basename(f), X))
    if not mats:
        print("  ⇒ ⛔ 8-인자를 모두 가진 트레이스 없음 (필요: " + ",".join(FACTORS) + ")")
        return 2

    print("=== anima evaluate --pc2-direction --rank-null %s — H_9714 상류 rank 재검 ===" % mode)
    print("traces: %s · %d file → **%d 독립 run** (중복 인자스트림 %d 제외 = arm 은 tension 에 영향 0)"
          % (d, len(files), len(mats), dup))
    print("        surrogate=%d · seed=%d" % (ns, rseed))
    print("⚖️ 스케일: λ 는 **correlation-scale**(Σλ=8) — H_9468 의 covariance-scale(Σλ≈0.15)과 **다르다**.")
    print("        따라서 이 λ₂ 는 H_9468 의 0.048 이 아니다. 판정은 **surrogate 대조**(스케일 무관)가 한다.")
    print("질문:  rank 2.66 · 'PC2 = 실재 DOF' 가 **자기상관 시계열에 MP 를 적용한 산물**인가?")
    print("null:  %s" % ("iid tick-shuffle (자기상관 파괴 = MP 가정 재현 · 값싼 스크린)" if mode == "iid"
                         else "AAFT phase surrogate (주변분포+자기상관 보존 · 인자간 결합만 파괴 = 올바른 null)"))
    print("bar:   λ₁ > null95 (양성통제) ∧ λ₂ ≤ null95 ⇒ 🧱 KILL-PC2-is-noise / 둘 다 초과 ⇒ PASS-rank-real")
    print("")

    def _eig(X):
        Z = X - X.mean(axis=0)
        sd = Z.std(axis=0, ddof=1)
        sd[sd == 0] = 1.0
        Z = Z / sd                       # correlation-scale: MP's equal-variance frame
        C = (Z.T @ Z) / float(Z.shape[0] - 1)
        w = _np.linalg.eigvalsh(C)
        return _np.sort(w)[::-1]

    def _lag1(X):
        out = []
        for j in range(X.shape[1]):
            v = X[:, j]
            v = v - v.mean()
            den = float((v * v).sum())
            out.append(float((v[:-1] * v[1:]).sum() / den) if den > 0 else 0.0)
        return out

    def _iid_surr(X, rng):
        Y = _np.empty_like(X)
        for j in range(X.shape[1]):
            col = X[:, j].copy()
            rng.shuffle(col)
            Y[:, j] = col
        return Y

    def _aaft(X, rng):
        """AAFT: rank-map to gaussian -> randomise phases (keeps the power spectrum, hence the
        autocorrelation) -> rank-map back to the ORIGINAL values. Each factor is surrogated
        independently, so the marginal and the autocorrelation survive and only the cross-factor
        coupling is destroyed."""
        n = X.shape[0]
        Y = _np.empty_like(X)
        for j in range(X.shape[1]):
            x = X[:, j]
            order = _np.argsort(x)
            g = _np.sort(rng.standard_normal(n))
            gx = _np.empty(n)
            gx[order] = g                       # gaussianised, same rank order
            F = _np.fft.rfft(gx)
            ph = rng.uniform(0.0, 2.0 * _np.pi, size=F.shape[0])
            ph[0] = 0.0
            if n % 2 == 0:
                ph[-1] = 0.0
            Fs = _np.abs(F) * _np.exp(1j * ph)  # same |spectrum| => same autocorrelation
            gs = _np.fft.irfft(Fs, n=n)
            back = _np.argsort(_np.argsort(gs))
            Y[:, j] = _np.sort(x)[back]         # rank-map back to the original marginal
        return Y

    rng = _np.random.default_rng(rseed)
    tot_n = 0
    obs_all, null_all = [], []
    for name, X in mats:
        obs = _eig(X)
        lags = _lag1(X)
        tot_n += X.shape[0]
        nulls = []
        for _ in range(ns):
            Y = _iid_surr(X, rng) if mode == "iid" else _aaft(X, rng)
            nulls.append(_eig(Y))
        nulls = _np.asarray(nulls)
        obs_all.append(obs)
        null_all.append(nulls)
        print("  %-18s n=%-4d λ=[%s]" % (name, X.shape[0],
                                         " ".join("%.3f" % v for v in obs[:4])))
        print("     lag-1 ρ̂ per factor: " + " ".join("%s=%.2f" % (FACTORS[j][:3], lags[j])
                                                     for j in range(len(FACTORS))))

    obs = _np.mean(_np.asarray(obs_all), axis=0)
    nulls = _np.mean(_np.asarray(null_all), axis=0)      # run-averaged null distribution
    p95 = _np.percentile(nulls, 97.5, axis=0)
    p05 = _np.percentile(nulls, 2.5, axis=0)

    print("")
    print("  run-평균 · surrogate null 95%% 상단 대조 (n_tot=%d tick)" % tot_n)
    for k in range(4):
        pv = float((nulls[:, k] >= obs[k]).mean())
        mark = "생존" if obs[k] > p95[k] else "死"
        print("     λ%d obs=%.4f · null95=[%.4f, %.4f] · p=%.3f · %s"
              % (k + 1, obs[k], p05[k], p95[k], pv, mark))

    l1_live = obs[0] > p95[0]
    l2_live = obs[1] > p95[1]
    all_live = bool((obs > p95).all())
    print("")
    if all_live:
        v = ("⛔ INVALID — bulk 를 포함해 **모든 λ 가 null 초과** ⇒ surrogate 가 자기상관을 보존 못함"
             "(AAFT 결함) · 판정 불가")
    elif not l1_live:
        v = ("⛔ INVALID — **양성통제 λ₁ 실패**(인증된 coherence 축조차 null 을 못 이김) ⇒ 계기가 어떤 구조도 "
             "못 봄 · surrogate 구현 결함 먼저 · **음성 아님**")
    elif l1_live and not l2_live:
        v = ("🧱 KILL-PC2-is-noise — λ₁ 생존 ∧ **λ₂ 사망** = PC2 특정 사망 ⇒ **PC2 lane 전체(H_9574·H_9576·"
             "H_9630~9634) 상류 근거 소멸** · rank 2.66 → ~1 · H_9428 DIRECTIONAL 재작성 대상")
    else:
        v = ("🟢 PASS-rank-real — λ₁·λ₂ 모두 null 초과 ⇒ PC2 실재 · 축퇴는 PCA 탓 아님 ⇒ H_9712(상쇄)/"
             "H_9715(stage 노예화) 로 인계")
    print("  ⇒ VERDICT(%s-null): %s" % (mode, v))
    if mode == "iid":
        print("     ⚠️ iid 는 **값싼 스크린**이다 — 판정권은 phase(AAFT) surrogate 에 있다(--rank-null phase).")
    else:
        print("     주의: ρ*=0.736 문턱은 **예측**이지 판정자가 아니다(AR(1) n_eff↔고유값 맵은 근사 · MP 는")
        print("     인자 등분산도 가정하나 여기 인자들은 등분산이 아니다). 판정은 위 surrogate 대조가 한다.")
    return 0


def _pc2_atom_census(argv):
    """H_9756 ATOM-CENSUS (PILOT) — the axis-agnostic byte-granularity readout POWER pre-check.

    `anima-py evaluate --pc2-direction <traces_dir> --atom-census --pilot [--atoms fw|<file>] [--span word]`

    WHY A NEW READOUT. Readout D (H_9629) died a triple death — its denominator was the text's own
    diversity, so it was un-identifiable (H_9716). This DV replaces it with a DENOMINATOR-FREE count:
    the number of hits, in one tick's generated window, against a FIXED pre-registered atom list
    (frequent English function words + punctuation). No text-self-diversity divisor, no experimenter
    design value in the denominator — just a count. It is measured WITHIN-TICK PAIRED (the same tick
    decoded at ζ=0 vs ζ=max, draw stream held fixed) so the tick's identity cancels (the H_9664 design).

    THIS IS THE PILOT ONLY (`--pilot`). It does NOT run the full arm-swept readout (frozen/refit/resid/
    random loading) or the prefix-swap positive control or the null arms — those need the H_9755 pool
    fire (fresh decodes). The pilot answers ONE question off the EXISTING ζ-fire traces: does the
    atom-census readout have any POWER at all? i.e. is the atom base-rate non-degenerate, and is the
    MDE (min detectable Δ at the current n and variance) smaller than the effect we would care about?
    If base-rate ≈ 0 or MDE > a medium (d=0.5) effect, the full fire is a waste until the readout is
    redesigned (span up, richer atom family). This is a_scale_honest_scope — power BEFORE the negative,
    instrument-power BEFORE the expensive run. It is NOT a verdict on the byte-wall claim.

    9→3 dedupe is a no-op here: /tmp/zt already holds one file per independent run (distinct seeds);
    a no-nudge control run may carry 0 emit ladders and simply contributes nothing.
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import re as _re

    # z(0.975) + z(0.80) — two-sided α=0.05 test, 80% power (paired)
    _Z = 2.801585
    _D_REF = 0.5          # effect of interest = a medium (Cohen's d = 0.5) shift
    _BR_MIN = 0.05        # base-rate floor: ≥5% of window words must be atoms (card §5)

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --atom-census --pilot")
        return 2
    pilot = "--pilot" in argv
    span = evaluate_strval(argv, "--span", "word")
    atoms_arg = evaluate_strval(argv, "--atoms", "fw")

    # PRE-REGISTERED atom families (fixed · corpus-frequency-derived · NOT tuned to these traces).
    _FW = ("the of and a to in is that it was for on as with his he be at by this had not are but "
           "from or an they which one you were her all she there would their we him been has when "
           "who will more no if out so said what up its about into than them can only other new some "
           "could time these two may then do first any my now such like our over man me even most made "
           "after also did many before must through back years where much your way well down should "
           "because each just those people how too little state good very make world still own see men "
           "work long get here between both life being under never day same another know while last "
           "might us great old year off come since against go came right used take three").split()
    _PUNC = list('.,;:!?"\'()-/')

    if atoms_arg in ("fw", "corpus"):
        word_atoms = set(_FW)
        punc_atoms = list(_PUNC)
        atoms_src = "built-in fw+punct (%d words · %d punct)" % (len(word_atoms), len(punc_atoms))
    else:
        try:
            toks = [t.strip() for t in open(atoms_arg) if t.strip()]
        except OSError:
            print("  ⇒ ⛔ --atoms 파일 열기 실패: " + atoms_arg)
            return 2
        word_atoms = set(t.lower() for t in toks if all(c.isalpha() or c == "'" for c in t))
        punc_atoms = [t for t in toks if not all(c.isalpha() or c == "'" for c in t)]
        atoms_src = "%s (%d words · %d punct)" % (atoms_arg, len(word_atoms), len(punc_atoms))

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _count(txt):
        """hit-count of pre-registered atoms in `txt`, plus the window's word length (for base-rate)."""
        w = _re.findall(r"[a-z']+", txt.lower())
        wc = sum(1 for x in w if x in word_atoms)
        pc = sum(txt.count(p) for p in punc_atoms)
        return wc + pc, len(w)

    def _stats(deltas):
        n = len(deltas)
        if n < 2:
            return None
        md = sum(deltas) / float(n)
        sd = (sum((x - md) ** 2 for x in deltas) / float(n - 1)) ** 0.5
        den = sum((x - md) ** 2 for x in deltas)
        num = sum((deltas[i] - md) * (deltas[i + 1] - md) for i in range(n - 1))
        rho = (num / den) if den > 0 else 0.0
        neff = (n * (1.0 - rho) / (1.0 + rho)) if abs(rho) < 1 else float(n)
        neff = max(neff, 1.0)
        mde_cnt = _Z * sd / (neff ** 0.5)
        mde_d = _Z / (neff ** 0.5)
        return {"n": n, "md": md, "sd": sd, "rho": rho, "neff": neff,
                "mde_cnt": mde_cnt, "mde_d": mde_d}

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    print("=== anima evaluate --pc2-direction --atom-census (PILOT) — H_9756 계기 검정력 사전점검 ===")
    print("traces: %s (%d file = %d run · span=%s)" % (d, len(files), len(files), span))
    print("atoms:  %s" % atoms_src)
    print("DV:     within-tick PAIRED Δcount = atoms(ζ=max) − atoms(ζ=0)  · 분모-프리 hit-count")
    print("판정:   base-rate 충분(≥%.0f%% 창) ∧ MDE ≤ %.1f·sd ⇒ PILOT-PASS · 아니면 UNDERPOWERED-BY-INSTRUMENT"
          % (_BR_MIN * 100, _D_REF))
    print("        (⚠️ 이건 byte-wall 판정이 아니다 — 계기가 full fire 를 태울 검정력이 있나만 잰다)")
    print("")

    all_base_atoms, all_deltas, all_frac = [], [], []
    iso_ok_tot, iso_bad_tot = 0, 0
    per_run = []
    for f in files:
        meta = {}
        base_atoms, deltas, frac = [], [], []
        iso_ok, iso_bad = 0, 0
        n_emit = 0
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                meta = r
                continue
            if not r.get("emit"):
                continue
            n_emit += 1
            zl = r.get("gtext_zeta") or []
            if len(zl) < 2:
                continue
            base_b = _b64(r.get("gtext_b64"))
            rungs = {}
            for e in zl:
                zv = float(e["zeta"])
                tb = _b64(e.get("text_b64"))
                if abs(zv) < 1e-12:
                    if tb == base_b:
                        iso_ok += 1
                    else:
                        iso_bad += 1
                rungs[round(zv, 6)] = tb
            if not rungs:
                continue
            z0 = rungs.get(0.0)
            zhi = rungs[max(rungs)]
            if z0 is None:
                continue
            b_cnt, b_w = _count(z0.decode("utf-8", "replace"))
            h_cnt, _ = _count(zhi.decode("utf-8", "replace"))
            base_atoms.append(b_cnt)
            deltas.append(h_cnt - b_cnt)
            frac.append(b_cnt / float(b_w) if b_w else 0.0)
        tag = os.path.basename(f)
        st = _stats(deltas)
        n_lad = len(deltas)
        br_tick = (sum(base_atoms) / float(n_lad)) if n_lad else 0.0
        br_frac = (sum(frac) / float(n_lad)) if n_lad else 0.0
        per_run.append((tag, n_emit, n_lad, br_tick, br_frac, st))
        iso_ok_tot += iso_ok
        iso_bad_tot += iso_bad
        all_base_atoms += base_atoms
        all_deltas += deltas
        all_frac += frac

    print("  ① 🔐 격리 인증(ζ=0 == base gtext_b64): %d 일치 · %d 불일치" % (iso_ok_tot, iso_bad_tot))
    if iso_bad_tot > 0:
        print("     ⚠️ 격리 불일치 존재 — 전체 fire 시 재검(파일럿 base-rate 는 사다리 자체 ζ=0 rung 사용).")
    print("")
    print("  ② run 별 분포 (집계 하나로 읽지 말 것):")
    print("     %-16s %5s %5s %9s %8s %9s %8s %8s %8s" %
          ("run", "emit", "ladd", "atoms/tk", "frac", "meanΔ", "sdΔ", "n_eff", "MDE_d"))
    for tag, n_emit, n_lad, br_tick, br_frac, st in per_run:
        if st is None:
            print("     %-16s %5d %5d %9s %8s %9s %8s %8s %8s   (사다리<2 · 기여 없음)"
                  % (tag, n_emit, n_lad, "-", "-", "-", "-", "-", "-"))
        else:
            print("     %-16s %5d %5d %9.2f %8.3f %+9.3f %8.3f %8.1f %8.3f"
                  % (tag, n_emit, n_lad, br_tick, br_frac, st["md"], st["sd"], st["neff"], st["mde_d"]))
    print("")

    pst = _stats(all_deltas)
    if pst is None:
        print("  ⇒ ⏳ 사다리(≥2 rung)를 가진 emit tick 이 부족 — fire 진행중이면 재폴링 · 파일럿 불가.")
        return 0
    n = pst["n"]
    br_tick = sum(all_base_atoms) / float(n)
    br_frac = sum(all_frac) / float(n)
    req_n = (_Z / _D_REF) ** 2

    print("  ③ POOLED (n=%d ladder · %d run 기여):" % (n, sum(1 for r in per_run if r[5] is not None)))
    print("     base-rate:  atoms/tick = %.2f · 창-내 atom 비율 = %.3f (floor %.2f)"
          % (br_tick, br_frac, _BR_MIN))
    print("     paired Δ:   meanΔ = %+.3f · sdΔ = %.3f · lag-1 ρ̂ = %+.3f · n_eff = %.1f"
          % (pst["md"], pst["sd"], pst["rho"], pst["neff"]))
    print("     MDE:        count = %.3f · Cohen d = %.3f  (검출 최소효과 @현 n_eff · 80%% power · α=.05)"
          % (pst["mde_cnt"], pst["mde_d"]))
    print("     required n: d=%.1f 검출에 필요한 n = %.1f (n_eff %.1f %s)"
          % (_D_REF, req_n, pst["neff"], "≥ 충족" if pst["neff"] >= req_n else "< 미달"))
    print("")

    if not pilot:
        # ══════════ H_9756 FULL arm-swept atom-census readout (engine-native · 판정표 카드 §⑤) ══════════
        # 기존 arm-swept 트레이스(gtext_zeta 25/tick = 5 arm × 5 ζ · loading 태그)로 계산 — 새 디코드 불요.
        # 유일 예외 = prefix-swap 양성통제(--pos-control <dir>) · 없으면 음성판정을 PENDING 으로 강등(card §⑤).
        # 설계 LOCK(lab full Fable 2026-07-20): per-arm within-tick paired Δcount(ζ=±max − ζ=0) + rng-null
        # 밴드(atom-라벨 셔플=readout-floor) + arm 대조(refit vs random=축-null) → 판정선.
        import random as _rnd
        _ARMS = ("scalar", "frozen", "refit", "random", "refit-resid")
        _TOST_D = 0.20        # 등가(PASS-BYTE-WALL) margin · Cohen d
        _KILL_D = 0.20        # KILL arm 대조 최소 |d|
        _K_NULL = 300         # rng-null 셔플 횟수 (readout-floor 밴드)
        _CI_Z = 1.959964      # 양측 95% CI
        pos_dir = evaluate_strval(argv, "--pos-control", "")

        def _toks(txt):
            return _re.findall(r"[a-z']+", txt.lower())

        # re-parse 트레이스 → per (loading) per-tick paired Δ (+max·−max), token 캐시(rng-null 용)
        arm_pos = {a: [] for a in _ARMS}   # (c0, cHi, toks0, toksHi) · ζ=+max − ζ=0
        arm_neg = {a: [] for a in _ARMS}   # ζ=−max − ζ=0
        contrast = []                      # per-tick {arm: Δ+max} · refit&random 동시 존재 tick
        iso_ok2 = iso_bad2 = 0
        for f in files:
            for l in open(f):
                l = l.strip()
                if not l:
                    continue
                try:
                    r = _pj.loads(l)
                except ValueError:
                    continue
                if r.get("_meta") or not r.get("emit"):
                    continue
                zl = r.get("gtext_zeta") or []
                if not zl:
                    continue
                base_b = _b64(r.get("gtext_b64"))
                byld = {}
                for e in zl:
                    ld = e.get("loading")
                    if ld is None:
                        continue
                    byld.setdefault(ld, {})[round(float(e["zeta"]), 6)] = _b64(e.get("text_b64"))
                for ld, zd in byld.items():
                    z0b = zd.get(0.0)
                    if z0b is not None:
                        if z0b == base_b:
                            iso_ok2 += 1
                        else:
                            iso_bad2 += 1
                tdp = {}
                for a in _ARMS:
                    zd = byld.get(a)
                    if not zd or 0.0 not in zd:
                        continue
                    zs = sorted(zd)
                    t0 = zd[0.0].decode("utf-8", "replace")
                    c0, _ = _count(t0)
                    k0 = _toks(t0)
                    if zs[-1] > 0:
                        tH = zd[zs[-1]].decode("utf-8", "replace")
                        cH, _ = _count(tH)
                        arm_pos[a].append((c0, cH, k0, _toks(tH)))
                        tdp[a] = cH - c0
                    if zs[0] < 0:
                        tN = zd[zs[0]].decode("utf-8", "replace")
                        cN, _ = _count(tN)
                        arm_neg[a].append((c0, cN, k0, _toks(tN)))
                if "refit" in tdp and "random" in tdp:
                    contrast.append(tdp)

        print("  ══ FULL arm-swept readout (H_9756 · engine-native · 판정표 §⑤) ══")
        print("  ① 🔐 격리 재인증 (arm별 ζ=0 == base gtext_b64): %d 일치 · %d 불일치"
              % (iso_ok2, iso_bad2))
        if iso_bad2 > 0:
            print("     🔴 INVALID — arm별 ζ=0 이 base 와 불일치(격리 파손) · 판독 중단.")
            return 0

        # rng-null: K 개 무작위 atom-set(실제 fw 크기) 로 pooled meanΔ(+max) 재계산 → readout-floor 밴드
        _allw = set()
        for a in _ARMS:
            for c0, cH, k0, kH in arm_pos[a]:
                _allw.update(k0)
                _allw.update(kH)
        _wl = sorted(_allw)
        _na = min(len(word_atoms), len(_wl))
        _rng = _rnd.Random(20260717)

        def _pooled_md(recs, aset):
            ds = [(sum(1 for w in kH if w in aset) - sum(1 for w in k0 if w in aset))
                  for c0, cH, k0, kH in recs]
            return (sum(ds) / float(len(ds))) if ds else 0.0

        null_draws = {a: [] for a in _ARMS}
        if _wl:
            for _ in range(_K_NULL):
                aset = set(_rng.sample(_wl, _na))
                for a in _ARMS:
                    if arm_pos[a]:
                        null_draws[a].append(_pooled_md(arm_pos[a], aset))

        def _band(xs):
            if not xs:
                return (0.0, 0.0)
            s = sorted(xs)
            return (s[int(0.025 * len(s))], s[min(len(s) - 1, int(0.975 * len(s)))])

        def _armstat(recs):
            ds = [cH - c0 for c0, cH, k0, kH in recs]
            st = _stats(ds)
            if st is None:
                return None
            se = st["sd"] / (st["neff"] ** 0.5) if st["neff"] > 0 else float("inf")
            st["se"] = se
            st["ci"] = (st["md"] - _CI_Z * se, st["md"] + _CI_Z * se)
            st["d"] = (st["md"] / st["sd"]) if st["sd"] > 0 else 0.0
            return st

        print("")
        print("  ② per-arm within-tick paired Δcount (ζ=+max − ζ=0 · 실제 atom-family) + rng-null 밴드:")
        print("     %-12s %8s %8s %20s %8s %20s" %
              ("arm", "meanΔ", "d", "95% CI", "n", "rng-null95 밴드"))
        armstats = {}
        for a in _ARMS:
            st = _armstat(arm_pos[a])
            armstats[a] = st
            nb = _band(null_draws[a])
            if st is None:
                print("     %-12s %8s   (사다리<2 · 기여 없음)" % (a, "-"))
                continue
            moves = (st["ci"][0] > nb[1]) or (st["ci"][1] < nb[0])   # CI 가 rng-null 밴드 밖
            print("     %-12s %+8.3f %+8.3f  [%+.3f,%+.3f] %8d  [%+.3f,%+.3f]%s"
                  % (a, st["md"], st["d"], st["ci"][0], st["ci"][1], st["n"],
                     nb[0], nb[1], "  ← 밴드밖" if moves else ""))
        # −max 부호 보존 요약(PASS-SIGN-NEG 판단용)
        neg_ref = _armstat(arm_neg.get("refit", []))
        if neg_ref is not None:
            print("     (refit ζ=−max Δ = %+.3f · +max 와 부호 %s)"
                  % (neg_ref["md"], "반대(사다리 정상)" if neg_ref["md"] * (armstats.get("refit") or {"md": 0})["md"] < 0 else "동일/모호"))

        # ③ arm 대조 (refit − random · within-tick paired · 축-null)
        con_ds = [d["refit"] - d["random"] for d in contrast]
        con = _stats(con_ds)
        con_ci = con_d = None
        if con is not None:
            cse = con["sd"] / (con["neff"] ** 0.5) if con["neff"] > 0 else float("inf")
            con_ci = (con["md"] - _CI_Z * cse, con["md"] + _CI_Z * cse)
            con_d = (con["md"] / con["sd"]) if con["sd"] > 0 else 0.0
            print("")
            print("  ③ arm 대조 Δ(refit−random) within-tick paired: meanΔ=%+.3f · d=%+.3f · 95%%CI=[%+.3f,%+.3f] · n=%d"
                  % (con["md"], con_d, con_ci[0], con_ci[1], con["n"]))

        # ④ 판정 (card §⑤ · Fable LOCK 판정선)
        def _in_band(st, nb):
            return st is not None and st["ci"][0] >= nb[0] and st["ci"][1] <= nb[1]
        def _equiv0(st):   # TOST 등가(|d|<margin)
            return st is not None and abs(st["d"]) < _TOST_D
        ref = armstats.get("refit"); ran = armstats.get("random")
        nb_ref = _band(null_draws["refit"])
        refit_moves = ref is not None and ((ref["ci"][0] > nb_ref[1]) or (ref["ci"][1] < nb_ref[0]))
        random_still = _equiv0(ran)
        contrast_sep = con_ci is not None and (con_ci[0] > 0 or con_ci[1] < 0) and abs(con_d or 0) >= _KILL_D
        all_equiv = all(_equiv0(armstats.get(a)) for a in _ARMS if a != "scalar" and armstats.get(a) is not None)

        # ④ⓐ 양성통제(prefix-swap · --pos-control <dir>) — pos_dir 제공 시만 실검증.
        # loading=="pswap" 항목(prefix 교체 디코드) vs base(gtext_b64) 의 within-tick paired atoms Δ.
        # PASS = prefix-swap(실재 의미변화)이 atom-census 를 유의하게 옮김(CI 0 제외) = readout 민감 인증.
        # FAIL/미실행 = readout 이 실재 변화조차 못 잡음(deaf) → 음성(PASS-BYTE-WALL) 판독 금지(§⑤ · VOID).
        pos_pass = None
        pos_stat = None
        if pos_dir:
            pos_deltas = []
            for pf in sorted(_glob.glob(os.path.join(pos_dir, "*.jsonl"))):
                for l in open(pf):
                    l = l.strip()
                    if not l:
                        continue
                    try:
                        r = _pj.loads(l)
                    except ValueError:
                        continue
                    if r.get("_meta") or not r.get("emit"):
                        continue
                    base_b = _b64(r.get("gtext_b64"))
                    if not base_b:
                        continue
                    for e in (r.get("gtext_zeta") or []):
                        if e.get("loading") == "pswap":
                            sw = _b64(e.get("text_b64"))
                            if sw:
                                bc, _ = _count(base_b.decode("utf-8", "replace"))
                                sc, _ = _count(sw.decode("utf-8", "replace"))
                                pos_deltas.append(sc - bc)
            pos_stat = _stats(pos_deltas)
            print("")
            if pos_stat is None:
                pos_pass = False
                print("  ④ⓐ 양성통제(prefix-swap): pswap 항목 없음/부족(n<2) → 미실행(FAIL · readout 감도 미인증)")
            else:
                pse = pos_stat["sd"] / (pos_stat["neff"] ** 0.5) if pos_stat["neff"] > 0 else float("inf")
                pos_stat["ci"] = (pos_stat["md"] - _CI_Z * pse, pos_stat["md"] + _CI_Z * pse)
                pos_stat["d"] = (pos_stat["md"] / pos_stat["sd"]) if pos_stat["sd"] > 0 else 0.0
                pos_pass = (pos_stat["ci"][0] > 0 or pos_stat["ci"][1] < 0)   # CI 0 제외 = 유의 검출
                print("  ④ⓐ 양성통제(prefix-swap): meanΔ=%+.3f · d=%+.3f · 95%%CI=[%+.3f,%+.3f] · n=%d → %s"
                      % (pos_stat["md"], pos_stat["d"], pos_stat["ci"][0], pos_stat["ci"][1], pos_stat["n"],
                         "🟢 PASS(readout 민감 — 실재 변화 검출)" if pos_pass else "🔴 FAIL(readout deaf)"))

        print("")
        print("  ⇒ VERDICT (DIRECTIONAL · 303M · terminal=이 출력 verbatim · byte-wall 판정표 §⑤):")
        if refit_moves and random_still and contrast_sep:
            print("     🔴 KILL-AXIS-MATTERS — refit 만 atom-census 를 rng-null 위로 움직임(random 은 밴드 안 ∧")
            print("        Δ(refit−random) CI 가 0 제외 ∧ |d|≥%.2f). 축이 content 입도에 닿음 = byte-wall 반증." % _KILL_D)
        elif refit_moves and not contrast_sep:
            print("     🟠 AMBIG-GENERIC — refit 은 rng-null 밖이나 random 대비 분리 안 됨(generic loading 효과).")
        elif all_equiv:
            if pos_dir and pos_pass:
                print("     🟢 PASS-BYTE-WALL — 전 loading arm 이 atom-census 에서 TOST 등가(|d|<%.2f) ∧ 양성통제 통과" % _TOST_D)
                print("        (prefix-swap=실재 변화는 readout 이 검출). ⇒ 어떤 축도 content 입도 못 옮기나 readout 은")
                print("        멀쩡 = 축-무관 content-벽 확정(π̄ 채널 H_9755 와 2-채널 정합).")
            elif pos_dir and not pos_pass:
                print("     ⚪ VOID — 전 arm 등가이나 양성통제 실패(prefix-swap 조차 readout 이 못 잡음=deaf).")
                print("        readout 감도 미인증 → 음성(PASS-BYTE-WALL) 판독 금지(§⑤) · readout 재설계(span↑/atom↑) 후 재fire.")
            else:
                print("     ⏳ PENDING-POSITIVE-CONTROL — 전 arm TOST 등가(|d|<%.2f · PASS-BYTE-WALL 방향)이나" % _TOST_D)
                print("        음성 판독은 prefix-swap 양성통제 필요(card §⑤ readout 양성통제 없이 음성 금지).")
                print("        승격 경로: anima-py chat … --zeta-prefix-swap <alt> → --pos-control <dir> 재실행.")
        else:
            print("     ⏳ NOT-CLEAN — 판정선 어디에도 깨끗이 안 들어감(일부 arm 이동·대조 미분리 혼재) · 표 재검.")
        print("     범위: content-입도 채널(π̄ rate 아님) · H_9755(어떤 arm 도 축-dose 무증거)의 독립 채널 확증/반증.")
        print("     주의: rng-null 은 word-atom 만(punct 제외) 근사 floor · terminal 은 prefix-swap 양성통제 후.")
        return 0

    br_ok = br_frac >= _BR_MIN
    mde_ok = pst["mde_d"] <= _D_REF
    print("  ⇒ VERDICT (PILOT · 검정력 사전점검 · byte-wall 판정 아님):")
    if br_ok and mde_ok:
        print("     🟢 PILOT-PASS — base-rate 충분(%.3f≥%.2f) ∧ MDE(d=%.3f)≤%.1f·sd."
              % (br_frac, _BR_MIN, pst["mde_d"], _D_REF))
        print("     ⇒ atom-census readout 은 full arm-swept fire(H_9755)를 태울 검정력이 있다.")
    elif not br_ok:
        print("     🔴 UNDERPOWERED-BY-INSTRUMENT — base-rate 저조(%.3f<%.2f창)." % (br_frac, _BR_MIN))
        print("     ⇒ span 상향(word→ngram) 또는 atom-family 확대 후 재산출 · full fire 전 readout 재설계.")
    else:
        print("     🔴 UNDERPOWERED-BY-INSTRUMENT — MDE(d=%.3f)>%.1f·sd @n_eff=%.1f."
              % (pst["mde_d"], _D_REF, pst["neff"]))
        print("     ⇒ 현 n 으로는 medium 효과도 못 잡는다 · tick 수 늘리거나(더 긴 fire) 관심효과 상향.")
    print("     범위: PILOT = 계기 검정력만 · 벽/축 판정은 full arm-swept fire(prefix-swap 양성통제 통과 후).")
    return 0


# ── Hartigan & Hartigan (1985) dip statistic — numpy-only port (validated to machine
#    precision against the reference `diptest` C implementation over 60 random samples;
#    numpy-only so it runs on the hexa-less pool measurement channel). ─────────────
def _dip_gcm(cdf, idxs):
    work_cdf = cdf
    work_idxs = idxs
    gcm = [work_cdf[0]]
    touch = [0]
    import numpy as _np
    while len(work_cdf) > 1:
        distances = work_idxs[1:] - work_idxs[0]
        slopes = (work_cdf[1:] - work_cdf[0]) / distances
        minslope = slopes.min()
        mi = _np.where(slopes == minslope)[0][0] + 1
        gcm.extend(work_cdf[0] + distances[:mi] * minslope)
        touch.append(touch[-1] + mi)
        work_cdf = work_cdf[mi:]
        work_idxs = work_idxs[mi:]
    return _np.array(gcm), _np.array(touch)


def _dip_lcm(cdf, idxs):
    g, t = _dip_gcm(1 - cdf[::-1], idxs.max() - idxs[::-1])
    return 1 - g[::-1], len(cdf) - 1 - t[::-1]


def _dip_stat(dat):
    """Hartigans' dip statistic for a 1-D sample (returns dip in [0, 0.25])."""
    import numpy as _np
    import collections as _coll
    counts = _coll.Counter(dat)
    idxs = _np.sort(list(counts.keys()))
    hist = _np.array([counts[i] for i in idxs])
    if len(idxs) <= 4 or idxs[0] == idxs[-1]:
        return 0.0
    cdf = _np.cumsum(hist, dtype=float)
    cdf /= cdf[-1]
    w_idxs = idxs
    w_hist = _np.asarray(hist, dtype=float) / _np.sum(hist)
    w_cdf = cdf
    D = 0.0
    left = [0]
    right = [1]
    while True:
        lp, lt = _dip_gcm(w_cdf - w_hist, w_idxs)
        rp, rt = _dip_lcm(w_cdf, w_idxs)
        ld = _np.abs(rp[lt] - lp[lt]); d_left = ld.max()
        rd = _np.abs(rp[rt] - lp[rt]); d_right = rd.max()
        if d_right > d_left:
            xr = rt[d_right == rd][-1]
            xl = lt[lt <= xr][-1]
            d = d_right
        else:
            xl = lt[d_left == ld][0]
            xr = rt[rt >= xl][0]
            d = d_left
        ldiff = _np.abs(lp[:xl + 1] - w_cdf[:xl + 1]).max()
        rdiff = _np.abs(rp[xr:] - w_cdf[xr:] + w_hist[xr:]).max()
        if d <= D or xr == 0 or xl == len(w_cdf):
            the_dip = max(_np.abs(cdf[:len(left)] - left).max(),
                          _np.abs(cdf[-len(right) - 1:-1] - right).max())
            return float(the_dip / 2)
        D = max(D, ldiff, rdiff)
        w_cdf = w_cdf[xl:xr + 1]
        w_idxs = w_idxs[xl:xr + 1]
        w_hist = w_hist[xl:xr + 1]
        left[len(left):] = lp[1:xl + 1]
        right[:0] = rp[xr:-1]


def _sc_gmm_fit(X, k, rng, iters=60, restarts=2):
    """Full-covariance GMM EM (numpy-only). Returns (BIC, hard-labels, (mu,cov,wt))."""
    import numpy as _np
    n, d = X.shape
    base = _np.cov(X.T).reshape(d, d) + 1e-6 * _np.eye(d)

    def _logpdf(Xa, mu, cov):
        diff = Xa - mu
        try:
            icov = _np.linalg.inv(cov); det = _np.linalg.det(cov)
        except _np.linalg.LinAlgError:
            return _np.full(Xa.shape[0], -1e10)
        if det <= 1e-300:
            det = 1e-300
        maha = _np.einsum('ij,jk,ik->i', diff, icov, diff)
        return -0.5 * (d * _np.log(2 * _np.pi) + _np.log(det) + maha)

    best = None
    for _ in range(restarts):
        mu = X[rng.choice(n, k, replace=False)].copy()
        cov = _np.repeat(base[None], k, axis=0)
        wt = _np.ones(k) / k
        ll_old = -_np.inf
        resp = None
        for _it in range(iters):
            logp = _np.empty((n, k))
            for j in range(k):
                logp[:, j] = _np.log(wt[j] + 1e-300) + _logpdf(X, mu[j], cov[j])
            m = logp.max(axis=1)
            lse = m + _np.log(_np.exp(logp - m[:, None]).sum(axis=1))
            ll = lse.sum()
            resp = _np.exp(logp - lse[:, None])
            Nk = resp.sum(axis=0) + 1e-10
            wt = Nk / n
            for j in range(k):
                mu[j] = (resp[:, j:j + 1] * X).sum(axis=0) / Nk[j]
                dx = X - mu[j]
                cov[j] = (resp[:, j:j + 1] * dx).T @ dx / Nk[j] + 1e-6 * _np.eye(d)
            if abs(ll - ll_old) < 1e-5 * (abs(ll_old) + 1):
                break
            ll_old = ll
        if best is None or ll > best[0]:
            best = (ll, resp, mu.copy(), cov.copy(), wt.copy())
    ll, resp, mu, cov, wt = best
    nparams = k * d + k * d * (d + 1) / 2.0 + (k - 1)
    bic = -2 * ll + nparams * _np.log(n)
    return bic, resp.argmax(axis=1), (mu, cov, wt)


def _sc_gmm_kbest(x1d, kmax, rng):
    """1-D GMM BIC census k=1..kmax → (kbest, n_density_modes_of_kbest)."""
    import numpy as _np
    X = x1d.reshape(-1, 1)
    bics = []; pars = []
    for k in range(1, kmax + 1):
        try:
            b, _lab, p = _sc_gmm_fit(X, k, rng)
        except (_np.linalg.LinAlgError, ValueError):
            b, p = _np.inf, None
        bics.append(b); pars.append(p)
    kb = int(_np.argmin(bics)) + 1
    p = pars[kb - 1]
    if p is None:
        return kb, 1
    mu, cov, wt = p
    grid = _np.linspace(x1d.min(), x1d.max(), 512)
    dens = _np.zeros_like(grid)
    for j in range(len(wt)):
        s2 = float(cov[j].reshape(-1)[0])
        dens += wt[j] * _np.exp(-0.5 * (grid - mu[j, 0]) ** 2 / s2) / _np.sqrt(2 * _np.pi * s2)
    up = dens[1:-1] > dens[:-2]
    dn = dens[1:-1] >= dens[2:]
    modes = int(_np.sum(up & dn)) or 1
    return kb, modes


def _sc_mean_dwell(lab):
    import numpy as _np
    if len(lab) == 0:
        return 0.0
    lens = []; cur = 1
    for i in range(1, len(lab)):
        if lab[i] == lab[i - 1]:
            cur += 1
        else:
            lens.append(cur); cur = 1
    lens.append(cur)
    return float(_np.mean(lens))


def _sc_med_dwell(x):
    import numpy as _np
    return _sc_mean_dwell((x > _np.median(x)).astype(int))


def _sc_ft_surr(x, rng):
    """Fourier phase-randomised surrogate (gaussian-ish marginal, spectrum preserved)."""
    import numpy as _np
    n = len(x)
    F = _np.fft.rfft(x - x.mean())
    ph = rng.uniform(0, 2 * _np.pi, F.shape[0]); ph[0] = 0.0
    if n % 2 == 0:
        ph[-1] = 0.0
    return _np.fft.irfft(_np.abs(F) * _np.exp(1j * ph), n=n) + x.mean()


def _sc_aaft(x, rng):
    """AAFT surrogate (marginal AND power spectrum preserved)."""
    import numpy as _np
    n = len(x)
    order = _np.argsort(x)
    g = _np.sort(rng.standard_normal(n))
    gx = _np.empty(n); gx[order] = g
    F = _np.fft.rfft(gx)
    ph = rng.uniform(0, 2 * _np.pi, F.shape[0]); ph[0] = 0.0
    if n % 2 == 0:
        ph[-1] = 0.0
    gs = _np.fft.irfft(_np.abs(F) * _np.exp(1j * ph), n=n)
    back = _np.argsort(_np.argsort(gs))
    return _np.sort(x)[back]


def _sc_lag1(x):
    v = x - x.mean(); den = float((v * v).sum())
    return float((v[:-1] * v[1:]).sum() / den) if den > 0 else 0.0


def _sc_analyze(x, kmax, boot, rng):
    """Three surrogate-referenced tension-state statistics on a 1-D series.
       dip vs FT (marginal multimodality) · GMM-BIC k + fitted-density modes vs FT
       (marginal multi-component) · median-split dwell vs AAFT (temporal persistence)."""
    import numpy as _np
    n = len(x)
    obs_dip = _dip_stat(x)
    kb, modes = _sc_gmm_kbest(x, kmax, rng)
    obs_dwell = _sc_med_dwell(x)
    dip_ft, k_ft, dwell_aa = [], [], []
    for _ in range(boot):
        f = _sc_ft_surr(x, rng)
        dip_ft.append(_dip_stat(f))
        kf, _m = _sc_gmm_kbest(f, kmax, rng)
        k_ft.append(kf)
        dwell_aa.append(_sc_med_dwell(_sc_aaft(x, rng)))
    dip_ft = _np.array(dip_ft); k_ft = _np.array(k_ft); dwell_aa = _np.array(dwell_aa)
    r = {"n": n, "dip": obs_dip, "kbest": kb, "modes": modes, "dwell": obs_dwell,
         "lag1": _sc_lag1(x),
         "dip_p95": float(_np.percentile(dip_ft, 97.5)), "dip_p05": float(_np.percentile(dip_ft, 2.5)),
         "dip_p": float((dip_ft >= obs_dip).mean()),
         "k_ft95": float(_np.percentile(k_ft, 97.5)), "k_p": float((k_ft >= kb).mean()),
         "dwell95": float(_np.percentile(dwell_aa, 97.5)), "dwell_p": float((dwell_aa >= obs_dwell).mean())}
    r["dip_mm"] = obs_dip > r["dip_p95"]
    r["dip_sub"] = obs_dip < r["dip_p05"]
    r["bic_multi"] = (kb >= 2) and (kb > r["k_ft95"])
    r["dens_mm"] = modes >= 2
    r["dwell_cl"] = obs_dwell > r["dwell95"]
    # a run shows STATES only when the two discriminating surrogate tests both fire:
    # multimodal marginal (dip, distribution-free) AND temporal persistence (dwell).
    r["states"] = bool(r["dip_mm"] and r["dwell_cl"] and kb >= 2)
    return r


def _sc_plant(n, rho, sep, rng):
    """Spectrum-matched symmetric 2-state HMM plant (lag-1 autocorr ≈ rho)."""
    import numpy as _np
    p = max(0.5, min(0.995, (rho + 1.0) / 2.0))
    lab = _np.empty(n, int); s = int(rng.integers(0, 2))
    for i in range(n):
        if i and rng.random() > p:
            s = 1 - s
        lab[i] = s
    return _np.array([-sep / 2.0, sep / 2.0])[lab] + rng.standard_normal(n) * 0.35


def _pc2_state_census(argv):
    """H_9753 TENSION-STATE-MIXTURE — is live tension a discrete state mixture (k=2..4)
    rather than a continuous low-rank axis?

    `anima-py evaluate --pc2-direction <traces_dir> --state-census [--kmax K] [--boot N] [--seed N]`

    THE RIVAL STRUCTURE HYPOTHESIS. H_9712 (z non-normal, IQR/sd=0.45) and H_9715 (stage
    92.7% single-pin) may be two faces of ONE thing: regime pinning. If so, live tension is
    not a continuous rank-2 subspace to be dose-steered, it is a mixture of a few discrete
    states — and the lever is state-SELECTION, not axis-steering (axis-dose = category error).

    THREE INDEPENDENT STATISTICS (never one aggregate — the H_9712 lesson), each read as a
    collapse-Δ vs a surrogate null (p7 · never a raw value), on each run's OWN refit 2-D
    subspace (the frozen H_9468 axis is deliberately absent — card ②):
      (1) DIP     — Hartigan & Hartigan dip on the refit PC2 marginal vs a Fourier phase-
                    randomised (spectrum-matched Gaussian) null. Distribution-free multimodality.
      (2) GMM-BIC — 1-D BIC census k=1..kmax + the number of modes of the FITTED density, vs
                    the same FT null. k≥2 alone is NOT diagnostic (any non-Gaussian continuous
                    density beats a Gaussian surrogate); the fitted-density mode count separates
                    real modes from a skew/shoulder fit.
      (3) DWELL   — mean run-length of the median 2-state split vs an AAFT null (marginal AND
                    spectrum preserved) = temporal persistence beyond linear autocorrelation.

    A run shows STATES only when the two DISCRIMINATING surrogate tests fire together — a
    multimodal marginal (dip) AND temporal persistence (dwell) — with k≥2. GMM-BIC k is
    reported as corroboration, not as a gate.

    POSITIVE CONTROL (opens nothing without it): a spectrum-matched 2-state HMM plant, injected
    at a separation sweep, must be detected by all three legs. The smallest separation the
    battery still catches is the MDE; if the plant is undetected the instrument is dead and the
    verdict is VOID (never a negative). run<100 ticks ⇒ VOID (power-before-negative).

    DEDUPE (H_9714): off/bias/rng share a byte-identical factor stream (steering is applied
    after emit and never feeds tension back — Stage-A isolation), so 9 files collapse to 3
    independent runs; counting all 9 would forge a null √3 too tight.

    Frozen bars (card H_9753 · do not retune): PASS-STATES = dip>FT-null95 ∧ k≥2 ∧ dwell>AAFT-null95
    in ≥2/3 runs · KILL-CONTINUOUS = dip & dwell null-equiv (states legs dead) with plant PASS ·
    AMBIG-MARGINAL = dip passes but dwell null · INVALID = dip < FT-null 5pct (over-unimodal
    pre-processing defect) · VOID = plant undetected ∨ tick<100.
    """
    import glob as _glob
    import json as _pj
    import numpy as _np

    FACTORS = ["rel_lane", "gap_ctx", "cur_ctx", "allo_ctx",
               "coh_lane", "nov_ctx", "bal_lane", "agloop_ctx"]
    Z_FACTORS = ["nov_ctx", "bal_lane", "coh_lane"]
    Z_W = _np.array([0.84, -0.44, -0.28])                     # H_9468 frozen loading

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --state-census "
              "[--kmax K] [--boot N] [--seed N]")
        return 2
    kmax = evaluate_intval(argv, "--kmax", 6)
    boot = evaluate_intval(argv, "--boot", 300)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    mats, seen, dup = [], set(), 0
    for f in files:
        rows, zs = [], []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                continue
            v = [r.get(k) for k in FACTORS]
            if any(x is None for x in v):
                continue
            rows.append([float(x) for x in v])
            zs.append(float(r["pc2_z"]) if r.get("pc2_z") is not None else _np.nan)
        if len(rows) < 20:
            continue
        X = _np.asarray(rows, dtype=_np.float64)
        key = hash(X.tobytes())
        if key in seen:
            dup += 1
            continue
        seen.add(key)
        mats.append((os.path.basename(f), X, _np.asarray(zs)))
    if not mats:
        print("  ⇒ ⛔ 8-인자를 모두 가진 트레이스 없음 (필요: " + ",".join(FACTORS) + ")")
        return 2

    def _pca(X):
        Z = X - X.mean(axis=0)
        sd = Z.std(axis=0, ddof=1); sd[sd == 0] = 1.0
        Zs = Z / sd
        C = (Zs.T @ Zs) / float(Zs.shape[0] - 1)
        w, V = _np.linalg.eigh(C)
        o = _np.argsort(w)[::-1]
        return Zs @ V[:, o], w[o]

    print("=== anima evaluate --pc2-direction --state-census — H_9753 이산-상태 혼합 검정 ===")
    print("traces: %s · %d file → **%d 독립 run** (중복 인자스트림 %d 제외 · H_9714 교훈)"
          % (d, len(files), len(mats), dup))
    print("질문:  라이브 tension = 연속 저랭크 축인가, 소수 이산 상태(k=2~4) 혼합인가?")
    print("계기:  ① Hartigan dip vs FT-gaussian null  ② GMM-BIC k + 밀도-modes vs FT  ③ 중앙분할 dwell vs AAFT")
    print("판독:  상태 판별은 **dip(다봉)∧dwell(군집)** 동시 발화 (BIC k 는 보강) · 전부 surrogate-Δ(p7)")
    print("bar:   PASS-STATES=dip>null95∧k≥2∧dwell>null95(≥2/3) · KILL-CONTINUOUS=dip·dwell null(plant PASS)")
    print("       · AMBIG-MARGINAL=dip 통과·dwell null · INVALID=dip<null5pct · VOID=plant 미검출∨tick<100")
    print("       boot=%d · kmax=%d · seed=%d" % (boot, kmax, rseed))
    print("")

    rng = _np.random.default_rng(rseed)

    # ── PLANT positive control + MDE separation sweep (instrument certification) ──
    med_lag1 = float(_np.median([_sc_lag1(_pca(X)[0][:, 1]) for _, X, _z in mats]))
    n_plant = int(_np.median([X.shape[0] for _, X, _z in mats]))
    print("  [PLANT] 스펙트럼-매칭 2-상태 HMM (n=%d · lag1≈%.2f) — separation MDE sweep:" % (n_plant, med_lag1))
    mde = None
    plant_top = None
    for sep in (1.0, 1.5, 2.0, 3.0):
        pr = _sc_analyze(_sc_plant(n_plant, med_lag1, sep, rng), kmax, boot, rng)
        det = pr["dip_mm"] and pr["dwell_cl"] and pr["kbest"] >= 2
        if det and mde is None:
            mde = sep
        plant_top = pr
        print("     sep=%.1f  dip=%.4f>%.4f=%s · k=%d(modes=%d) · dwell=%.2f>%.2f=%s ⇒ %s"
              % (sep, pr["dip"], pr["dip_p95"], _yn(pr["dip_mm"]), pr["kbest"], pr["modes"],
                 pr["dwell"], pr["dwell95"], _yn(pr["dwell_cl"]), "검출" if det else "미검출"))
    plant_ok = mde is not None
    print("     ⇒ 계기 인증: %s (MDE separation = %s)"
          % ("PASS" if plant_ok else "FAIL", ("%.1f" % mde) if mde else "미검출"))
    print("")

    # ── real runs ────────────────────────────────────────────────────────────
    under = False
    n_states = 0
    dip_mm_runs = 0
    dwell_runs = 0
    dip_sub_runs = 0
    for name, X, zs in mats:
        sc, w = _pca(X)
        if X.shape[0] < 100:
            under = True
        rp2 = _sc_analyze(sc[:, 1], kmax, boot, rng)          # refit PC2 = primary target
        rp1 = _sc_analyze(sc[:, 0], kmax, boot, rng)          # refit PC1 = reference axis
        z = zs[~_np.isnan(zs)]
        rz = _sc_analyze(z, kmax, boot, rng) if len(z) >= 20 else None
        n_states += int(rp2["states"])
        dip_mm_runs += int(rp2["dip_mm"])
        dwell_runs += int(rp2["dwell_cl"])
        dip_sub_runs += int(rp2["dip_sub"])
        print("  == %-18s n=%-4d lag1(PC2)=%.2f ==" % (name, rp2["n"], rp2["lag1"]))
        for tag, r in (("PC2*", rp2), ("PC1 ", rp1), ("z-frz", rz)):
            if r is None:
                continue
            dipverd = "다봉" if r["dip_mm"] else ("초단봉" if r["dip_sub"] else "단봉")
            print("     %-5s dip=%.4f null95=[%.4f,%.4f] p=%.3f(%s) · k=%d modes=%d(k_p=%.3f) · "
                  "dwell=%.2f null95=%.2f p=%.3f(%s) ⇒ %s"
                  % (tag, r["dip"], r["dip_p05"], r["dip_p95"], r["dip_p"], dipverd,
                     r["kbest"], r["modes"], r["k_p"], r["dwell"], r["dwell95"], r["dwell_p"],
                     "군집" if r["dwell_cl"] else "null", "STATES" if r["states"] else "연속"))

    print("")
    print("  run 집계(PC2 target): STATES %d/%d · dip-다봉 %d/%d · dwell-군집 %d/%d · dip-초단봉 %d/%d"
          % (n_states, len(mats), dip_mm_runs, len(mats), dwell_runs, len(mats),
             dip_sub_runs, len(mats)))
    print("")

    # ── verdict (frozen card H_9753 table) ───────────────────────────────────
    if not plant_ok:
        v = ("⛔ VOID — **양성통제 실패**: 스펙트럼-매칭 2-상태 plant 를 3중 검정이 어떤 separation 에서도 "
             "못 잡음 ⇒ 계기가 이산성을 못 봄 · 음성 아님 (계기 재점검 선행)")
    elif under:
        v = ("⛔ VOID — run 당 tick<100 ⇒ dip 검정력 미달 (power-before-negative) · plant PASS 여도 "
             "실데이터 null 은 판독 금지")
    elif n_states >= 2:
        v = ("🔑 **PASS-STATES** — dip(다봉)∧dwell(군집)∧k≥2 가 %d/%d run 동시 발화 ⇒ 라이브 tension 은 "
             "이산 상태 혼합 · 축-dose 는 범주오류 · 후속 레버 = 상태-조건부 ζ (설계만 등록·여기서 발사 금지)"
             % (n_states, len(mats)))
    elif dip_sub_runs >= 2:
        v = ("⛔ INVALID — %d/%d run 에서 dip < FT-null 5pct (초-단봉) ⇒ 전처리/score 왜곡 결함 · "
             "판정 불가" % (dip_sub_runs, len(mats)))
    elif dip_mm_runs >= 2 and dwell_runs < 2:
        v = ("🟡 AMBIG-MARGINAL — dip(다봉)은 서나 dwell(시간 군집)은 null ⇒ 다봉성은 주변분포만일 수 있음"
             "(연속 다양체의 비선형 굴곡) · DIRECTIONAL 보고 · cement 금지")
    elif dip_mm_runs < 2 and dwell_runs < 2:
        v = ("🧱 **KILL-CONTINUOUS** — 상태 판별 2 검정(dip·dwell)이 plant 인증(MDE sep=%s) 아래에서 "
             "실데이터 전부 null-동급 ⇒ 라이브 tension 은 **연속 저랭크** 존속 · 이산-상태 라이벌가설 반증 "
             "· 축/평면 프레임(H_9752)으로 인계" % (("%.1f" % mde) if mde else "?"))
    else:
        v = ("🟡 MIXED — 사전등록 칸 어디에도 깨끗이 안 떨어짐(dip-다봉 %d/%d · dwell-군집 %d/%d) ⇒ 단일 "
             "원인으로 못 박지 말 것 · 카드에 그대로 기록" % (dip_mm_runs, len(mats), dwell_runs, len(mats)))
    print("  ⇒ VERDICT: " + v)
    print("     범위: 판정 target = run 별 **refit** 2-D 부분공간(동결 H_9468 축 무등장·card ②). "
          "frozen z-projection(z-frz)이 다봉으로 읽히면 그건 부분공간 기하가 아니라 그 고정 조합의 성질.")
    print("     주의: GMM-BIC k≥2 단독은 이산성 아님(비가우스 shoulder/skew 도 통과) — 밀도 modes + dip 로 판별.")
    return 0


def _pc2_zeta_by_loading(argv):
    """H_9755 REFIT-AXIS ζ-LADDER verdict reader (design LOCK · card §8). Reads
    `chat --pc2-zeta --z-loading` traces: per emit tick an ARM x ζ grid of texts + this
    tick's raw 8-factor vector, plus one _zl_meta row per run. pc2(arm,ζ)=ζ·u_arm where u is
    the warmup-CALIBRATED (centered+Var=1) projection, so ζ's dose-scale matches across arms and
    Δβ is an AXIS effect, not a gain artifact. DV = per-tick β = OLS slope of π̄ on the ζ LABEL.

    `anima-py evaluate --pc2-direction <dir> --zeta-slope --by-loading [--tost 0.02]
       [--pos-control-beta -0.081] [--perm N] [--seed N]`
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import random as _prand

    T_WIN = 24
    L_MIN = 8
    SIGN_FRAC = 0.60          # pre-registered per-tick sign-consistency threshold (card §8)

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <dir> --zeta-slope --by-loading")
        return 2
    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    def _fval(flag, dflt):
        for _i, _a in enumerate(argv):
            if _a == flag and _i + 1 < len(argv):
                try:
                    return float(argv[_i + 1])
                except ValueError:
                    return dflt
        return dflt
    tost = _fval("--tost", 0.02)
    pos_beta = _fval("--pos-control-beta", -0.081)

    try:
        from decode import _dg_anchor_copy as _anchor_copy
    except ImportError:
        _anchor_copy = None
    if _anchor_copy is None:
        print("  ⇒ ⛔ INVALID — core.decode._dg_anchor_copy import 실패 · lm-step 분류 불가")
        return 0

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _pi(seed_b, txt_b, anchors):
        ind, mism = [], 0
        ctx = bytearray(seed_b)
        for _i in range(len(txt_b)):
            b = txt_b[_i]
            cb = _anchor_copy(bytes(ctx), anchors, L_MIN, T_WIN) if anchors else -1
            if cb >= 0:
                if cb != b:
                    mism += 1
                ctx.append(b)
                continue
            win = bytes(ctx[-T_WIN:]) if len(ctx) >= T_WIN else bytes(ctx)
            ind.append(1 if b in set(win) else 0)
            ctx.append(b)
        m = (sum(ind) / float(len(ind))) if ind else 0.0
        return m, len(ind), mism

    def _slope(xs, ys):
        n = len(xs)
        if n < 2:
            return None
        mx = sum(xs) / float(n)
        my = sum(ys) / float(n)
        den = sum((x - mx) ** 2 for x in xs)
        if den <= 0:
            return None
        return sum((xs[_i] - mx) * (ys[_i] - my) for _i in range(n)) / den

    def _recompute_u(_zlmeta, _arm, _f_raw):
        _aw = _zlmeta["arms"].get(_arm)
        if _aw is None:
            return None
        if _arm == "scalar":
            return 1.0
        _fmu = _zlmeta["fmu"]
        _fsd = _zlmeta["fsd"]
        if _aw.get("raw"):
            _fv = _f_raw
        else:
            _fv = [((_f_raw[_i] - _fmu[_i]) / _fsd[_i]) if _fsd[_i] > 1e-9 else 0.0
                   for _i in range(8)]
        _proj = sum(_aw["w"][_i] * _fv[_i] for _i in range(8))
        _sd = _aw["sd"]
        return ((_proj - _aw["mu"]) / _sd) if _sd > 1e-9 else 0.0

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    print("=== anima evaluate --pc2-direction --zeta-slope --by-loading — H_9755 refit-axis 판정 ===")
    print("traces: %s (%d file · perm=%d · seed=%d · tost=±%.3f · pos-β=%.4f)"
          % (d, len(files), rounds, rseed, tost, pos_beta))
    print("DV: per-tick β = OLS slope(π̄ ~ ζ LABEL) per arm · pc2=ζ·u_arm(centered+Var=1 projection)")
    print("")

    # per-arm per-tick β lists; scalar uses ALL ticks (warmup+post = H_9664 n-completion),
    # other arms use POST ticks only; contrasts pair arms on the identical post-tick set.
    beta_all = {}          # arm -> list of β_tick (all applicable ticks)
    post_ticks = []        # list of dicts {arm: β_tick} for post ticks carrying the full grid
    iso_bad = 0
    anchor_mism = 0
    u_mismatch = 0
    n_post_emit = 0
    n_full_grid = 0
    arms_seen = set()

    for f in files:
        meta = {}
        zlmeta = None
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_zl_meta"):
                zlmeta = r
            elif r.get("_meta"):
                meta = r
            else:
                rows.append(r)
        mem = meta.get("mem_text") or ""
        anchors = [mem.encode("utf-8", "surrogateescape")] if mem else []
        for r in rows:
            if not r.get("emit"):
                continue
            zl = r.get("gtext_zeta") or []
            if not zl or "loading" not in (zl[0] if zl else {}):
                continue                                   # not a --z-loading row
            base_b = _b64(r.get("gtext_b64"))
            seed_b = _b64(r.get("seed_b64"))
            f_raw = r.get("zl_factors")
            is_post = (r.get("zl_phase") == "post")
            if is_post:
                n_post_emit += 1
            # group grid entries by arm
            by_arm = {}
            for e in zl:
                by_arm.setdefault(e["loading"], []).append(e)
            tick_beta = {}
            for _arm, _ents in by_arm.items():
                arms_seen.add(_arm)
                # isolation: ζ=0 rung byte-equal to base
                for e in _ents:
                    if abs(float(e["zeta"])) < 1e-12 and _b64(e.get("text_b64")) != base_b:
                        iso_bad += 1
                # u self-check (post ticks; scalar u≡1)
                if is_post and zlmeta is not None and f_raw is not None:
                    _u_logged = float(_ents[0].get("u", 1.0))
                    _u_re = _recompute_u(zlmeta, _arm, f_raw)
                    if _u_re is not None and abs(_u_re - _u_logged) > 1e-9:
                        u_mismatch += 1
                # β on ζ label
                xs, ys = [], []
                for e in _ents:
                    tb = _b64(e.get("text_b64"))
                    m, nlm, mm = _pi(seed_b, tb, anchors)
                    anchor_mism += mm
                    if nlm == 0:
                        continue
                    xs.append(float(e["zeta"]))
                    ys.append(m)
                b = _slope(xs, ys)
                if b is not None:
                    tick_beta[_arm] = b
            # scalar β accumulates over ALL ticks
            if "scalar" in tick_beta:
                beta_all.setdefault("scalar", []).append(tick_beta["scalar"])
            if is_post:
                for _arm, _bv in tick_beta.items():
                    if _arm != "scalar":
                        beta_all.setdefault(_arm, []).append(_bv)
                # full-grid tick = has every arm that appears in zlmeta as valid
                if zlmeta is not None:
                    _valid_arms = [a for a, aw in zlmeta["arms"].items() if aw.get("valid", True)]
                    if all(a in tick_beta for a in _valid_arms):
                        n_full_grid += 1
                        post_ticks.append(tick_beta)

    # ── gates (sequential) ────────────────────────────────────────────────
    print("  ── 게이트 (순차 · 하나라도 실패 시 판독 중단) ──")
    print("     격리(ζ=0=base) 위반 %d · anchor-replay 불일치 %d · u 자기검증 불일치 %d"
          % (iso_bad, anchor_mism, u_mismatch))
    if iso_bad > 0:
        print("  ⇒ ⛔ INVALID — 격리 인증 실패(ζ=0 ≠ base) · dose 곡선 판독 불가")
        return 0
    if anchor_mism > 0:
        print("  ⇒ ⛔ INVALID — anchor-replay 불일치 · lm-step 분류 깨짐")
        return 0
    if u_mismatch > 0:
        print("  ⇒ ⛔ INVALID — u 자기검증 실패(writer 산술 ≠ reader 재계산) · schema-mismatch")
        return 0
    _grid_frac = (n_full_grid / float(n_post_emit)) if n_post_emit else 0.0
    print("     격자 완결: %d/%d post-emit tick 이 valid-arm×ζ 전격자(%.1f%%)"
          % (n_full_grid, n_post_emit, 100.0 * _grid_frac))
    if n_post_emit == 0 or _grid_frac < 0.90:
        print("  ⇒ ⛔ VOID — 격자 결손 >10%% (계기/infra 사망 · 음성 아님)")
        return 0

    def _mean(v):
        return (sum(v) / float(len(v))) if v else 0.0

    def _se(v):
        if len(v) < 2:
            return 0.0
        m = _mean(v)
        return (sum((x - m) ** 2 for x in v) / float(len(v) - 1) / float(len(v))) ** 0.5

    # positive control: scalar β over all ticks
    _bs = beta_all.get("scalar", [])
    _bs_m = _mean(_bs)
    _bs_se = _se(_bs)
    _pos_ok = (_bs_m < 0) and (abs(_bs_m - pos_beta) <= 2.0 * _bs_se)
    print("     양성통제 scalar: β=%.5f (se %.5f · n=%d) · 목표 %.4f ∈ β±2se? %s"
          % (_bs_m, _bs_se, len(_bs), pos_beta, _pos_ok))
    if not _pos_ok:
        print("  ⇒ ⛔ VOID — 양성통제 실패(scalar β 가 H_9664 %.4f 재현 못함) · 계기 사망" % pos_beta)
        return 0
    print("     ⇒ 게이트 PASS ✅")
    print("")

    # ── per-arm β + contrasts ─────────────────────────────────────────────
    print("  ── per-arm β (post-emit · ζ 라벨 회귀 · 분포 보고) ──")
    for _arm in ("scalar", "frozen", "refit", "random", "refit-resid"):
        _v = beta_all.get(_arm)
        if not _v:
            continue
        _npos = sum(1 for x in _v if x > 0)
        print("     %-12s n=%-4d mean β=%+.5f (se %.5f) · β<0 tick %d/%d (%.0f%%)"
              % (_arm, len(_v), _mean(_v), _se(_v), len(_v) - _npos, len(_v),
                 100.0 * (len(_v) - _npos) / float(len(_v))))

    def _paired_delta(_a, _b):
        return [t[_a] - t[_b] for t in post_ticks if _a in t and _b in t]

    def _perm_ci(_deltas):
        # sign-flip permutation null on paired Δβ (within-tick pairing preserved)
        pr = _prand.Random(rseed)
        null = []
        for _ in range(rounds):
            null.append(_mean([x if pr.random() < 0.5 else -x for x in _deltas]))
        null.sort()
        return null[int(0.025 * rounds)], null[int(0.975 * rounds) - 1]

    _has_refit = bool(beta_all.get("refit"))
    _has_frozen = bool(beta_all.get("frozen"))
    _has_random = bool(beta_all.get("random"))
    _rb = beta_all.get("random", [])
    _rnd_lo = _mean(_rb) - 2.0 * _se(_rb)
    _rnd_hi = _mean(_rb) + 2.0 * _se(_rb)
    print("")
    print("  ── 대조 (paired Δβ · post-tick · ζ 라벨 순열 null) ──")
    print("     random-null 밴드(축-null · ⚠️ 방향 3개뿐 = direction-marginal 아님): [%+.5f, %+.5f]"
          % (_rnd_lo, _rnd_hi))
    _contrasts = {}
    for _a, _b in (("refit", "frozen"), ("refit", "random"), ("frozen", "random")):
        _dl = _paired_delta(_a, _b)
        if len(_dl) < 3:
            continue
        _dm = _mean(_dl)
        _lo, _hi = _perm_ci(_dl)
        _contrasts[(_a, _b)] = (_dm, _lo, _hi)
        print("     Δβ(%s−%s) n=%d mean=%+.5f · 순열null95%%=[%+.5f,%+.5f] · TOST±%.3f %s"
              % (_a, _b, len(_dl), _dm, _lo, _hi, tost,
                 "PASS" if abs(_dm) < tost and abs(_lo) < tost and abs(_hi) < tost else "—"))

    # ── verdict table (mechanical, row order) ─────────────────────────────
    print("")
    _bf = _mean(beta_all.get("frozen", [])) if _has_frozen else 0.0
    _br = _mean(beta_all.get("refit", [])) if _has_refit else 0.0
    _rf = _contrasts.get(("refit", "frozen"))
    _rr = _contrasts.get(("refit", "random"))
    _fr = _contrasts.get(("frozen", "random"))

    def _ci_excl0(_c):
        return _c is not None and (_c[1] > 0 or _c[2] < 0)

    def _tost_pass(_c):
        return _c is not None and abs(_c[0]) < tost and abs(_c[1]) < tost and abs(_c[2]) < tost

    # per-tick sign-consistency of refit β
    _rvv = beta_all.get("refit", [])
    _sign_frac = (sum(1 for x in _rvv if x < 0) / float(len(_rvv))) if _rvv else 0.0

    if _has_refit and _has_frozen and _ci_excl0(_rf) and abs(_br) > abs(_bf) \
            and (_rr is not None and _ci_excl0(_rr)) and _sign_frac >= SIGN_FRAC:
        v = ("🟢 PASS-NEW-LEVER — |β_refit|>|β_frozen| (paired CI 0 제외) ∧ refit·frozen 둘 다 "
             "random-null 밖 ∧ per-tick 부호일관 %.2f≥%.2f ⇒ 라이브 축이 동결 축이 못 나른 dose 를 나름"
             % (_sign_frac, SIGN_FRAC))
    elif _has_refit and _has_frozen and _has_random and _tost_pass(_rf) and _tost_pass(_rr) \
            and _tost_pass(_fr):
        v = ("🧱 PASS-AXIS-BLIND — 3쌍 Δβ 전부 TOST±%.3f 등가 ⇒ 채널은 스칼라 dose 만 나름 · 축 "
             "선택 무관 확정(근축퇴 H_9752 정합) ⇒ H_9756 입도/readout 로 이관" % tost)
    elif _has_refit and _has_frozen and _ci_excl0(_rf) and abs(_bf) > abs(_br):
        v = "🔴 KILL-REFIT-ADDS-NOTHING — |β_frozen|>|β_refit| (CI 분리) ⇒ 동결 좌표로 충분(서사 문제였을 뿐)"
    elif _rf is not None and (_br * _bf < 0) and _ci_excl0(_rf):
        v = "⛔ INVALID — refit vs frozen 부호반전(paired CI 0 제외) ⇒ refit 부호규약 결함 · 배선 감사 후 재발사"
    else:
        _mde = 2.0 * max((_rf[2] - _rf[1]) if _rf else 0.0, (_rr[2] - _rr[1]) if _rr else 0.0) / 2.0
        v = ("⏳ NOT-POWERED — CI 분리도 TOST 등가도 아닌 중간지대 · realized MDE≈%.4f (결과이지 "
             "verdict 아님 · run/tick 증량 필요)" % _mde)
    print("  ⇒ VERDICT: " + v)
    print("     범위: refit ζ-arm 은 **채널이 무엇을 나를 수 있나**의 계기 증거(라이브 데몬 행동 아님) · "
          "크기 vs surrogate 로 읽지 raw° 아님(p7) · DIRECTIONAL(303M).")
    return 0


def _pc2_zeta_slope(argv):
    """H_9664 ZETA-SLOPE — the within-tick dose readout. Reads `anima-py chat --pc2-zeta` traces.

    `anima-py evaluate --pc2-direction <traces_dir> --zeta-slope [--perm N] [--seed N]`

    WHY WITHIN-TICK. Two readouts died the same death: D (H_9629, denominator = the text's own
    diversity) and pi_bar (H_9663, sd(dpi_rng) ~ 0.14). The shared cause is not the metric --
    it is the DESIGN: off/bias/rng are wholly different texts, so tick-level cascade variance
    swamps whatever you measure. And the live z is effectively a constant (IQR 0.0514; 45.7% of
    its variance in 3/270 ticks), so a tick-to-tick correlation has almost no regressor range.

    So this stops comparing ticks. Each emit tick carries its OWN ladder: the same tick decoded
    at several zeta with the draw stream held fixed. The tick's identity (its seed, its context,
    its cascade) is CONSTANT within its own ladder, so it cancels in the within-tick slope --
    and zeta MANUFACTURES the regressor range the live z never had.

        beta_tick = OLS slope of pi_bar(zeta) on zeta, computed WITHIN one tick
        DV        = mean(beta_tick) over emit ticks

    PRE-REGISTERED SIGN (from the code, not from any prior result): decode.py subtracts zeta
    from every in-window byte's logit, so zeta UP => in-window bytes suppressed => pi_bar DOWN
    => beta < 0. A significant beta > 0 is NOT a positive result -- it is SIGN-INVERTED and the
    run is INVALID pending a wiring audit.

    ISOLATION CERTIFICATE (gate -- opens nothing until it passes): the zeta=0 rung MUST come back
    byte-identical to the base text. decode.py leaves the row untouched at pc2==0.0, so any
    divergence means the isolation this whole line of work rests on never held: the run is
    INVALID and no dose curve may be read off it.

    CONTROLS (>=2, per p7 -- a raw slope is not a verdict):
      (1) rng arm      -- draw-stream re-key, no logit change => beta ~ 0 expected
      (2) zeta-label within-tick permutation -- shuffles the zeta labels INSIDE each tick, which
          destroys the dose ordering while preserving every tick's pi_bar multiset. This is the
          null that a between-tick permutation cannot give: it removes the tick effect entirely.
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import random as _prand

    T_WIN = 24
    L_MIN = 8

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --zeta-slope")
        return 2
    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    try:
        from decode import _dg_anchor_copy as _anchor_copy
    except ImportError:
        _anchor_copy = None
    if _anchor_copy is None:
        print("  ⇒ ⛔ INVALID — core.decode._dg_anchor_copy import 실패 · lm-step 분류 불가")
        return 0

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _pi(seed_b, txt_b, anchors):
        """pi_bar over lm-steps + the anchor-replay self-check (mismatch => classification broken)."""
        ind, mism = [], 0
        ctx = bytearray(seed_b)
        for i in range(len(txt_b)):
            b = txt_b[i]
            cb = _anchor_copy(bytes(ctx), anchors, L_MIN, T_WIN) if anchors else -1
            if cb >= 0:
                if cb != b:
                    mism += 1
                ctx.append(b)
                continue
            win = bytes(ctx[-T_WIN:]) if len(ctx) >= T_WIN else bytes(ctx)
            ind.append(1 if b in set(win) else 0)
            ctx.append(b)
        m = (sum(ind) / float(len(ind))) if ind else 0.0
        return m, len(ind), mism

    def _slope(xs, ys):
        n = len(xs)
        if n < 2:
            return None
        mx = sum(xs) / float(n)
        my = sum(ys) / float(n)
        den = sum((x - mx) ** 2 for x in xs)
        if den <= 0:
            return None
        return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / den

    files = sorted(_glob.glob(os.path.join(d, "*.jsonl")))
    if not files:
        print("  ⇒ ⛔ no *.jsonl under " + d)
        return 2

    print("=== anima evaluate --pc2-direction --zeta-slope — H_9664 within-tick 용량 판정 ===")
    print("traces: %s (%d file · perm=%d · seed=%d)" % (d, len(files), rounds, rseed))
    print("DV:     mean over ticks of  beta_tick = OLS slope( π̄(ζ) ~ ζ )  · within-tick")
    print("예측(코드가 지정): ζ↑ ⇒ 창-내 byte logit 감산 ⇒ π̄↓ ⇒ **β<0**")
    print("bar:    ① ζ=0 == base byte-identical ② β<0 ∧ 통제 2종(rng · ζ-라벨 within-tick 순열) 밖")
    print("")

    betas, iso_ok, iso_bad, mism_tot, ladders = [], 0, 0, 0, []
    for f in files:
        meta = {}
        rows = []
        for l in open(f):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                meta = r
            else:
                rows.append(r)
        mem = meta.get("mem_text") or ""
        anchors = [mem.encode("utf-8", "surrogateescape")] if mem else []
        for r in rows:
            if not r.get("emit"):
                continue
            zl = r.get("gtext_zeta") or []
            if len(zl) < 2:
                continue
            seed_b = _b64(r.get("seed_b64"))
            base_b = _b64(r.get("gtext_b64"))
            if not seed_b or not base_b:
                continue
            xs, ys = [], []
            for e in zl:
                zv = float(e["zeta"])
                tb = _b64(e.get("text_b64"))
                if abs(zv) < 1e-12:
                    if tb == base_b:
                        iso_ok += 1
                    else:
                        iso_bad += 1
                p, n_lm, mm = _pi(seed_b, tb, anchors)
                mism_tot += mm
                if n_lm == 0:
                    continue
                xs.append(zv)
                ys.append(p)
            b = _slope(xs, ys)
            if b is not None:
                betas.append(b)
                ladders.append((xs, ys))

    print("  ① 🔐 격리 인증: ζ=0 == base  %d 일치 · %d 불일치 · anchor-replay 자기검증 불일치 %d"
          % (iso_ok, iso_bad, mism_tot))
    if iso_bad > 0 or mism_tot > 0:
        print("     ⇒ ⛔ **런 전체 INVALID** — 격리가 성립한 적 없다면 dose 곡선은 읽을 수 없다.")
        print("        (이건 음성이 아니라 무효다 · H_9576 계열 전체가 소급 재검토 대상)")
        return 0
    if not betas:
        print("     ⇒ ⏳ 사다리를 가진 emit tick 이 아직 없다 — fire 진행중이면 재폴링.")
        return 0
    print("     ⇒ PASS ✅ (주장이 아니라 측정)")

    n = len(betas)
    mb = sum(betas) / float(n)
    sd = ((sum((b - mb) ** 2 for b in betas) / float(n - 1)) ** 0.5) if n > 1 else 0.0
    se = (sd / (n ** 0.5)) if n else 0.0

    # control (2): zeta-label permutation WITHIN each tick — kills the dose ordering, keeps the tick
    pr = _prand.Random(rseed)
    null = []
    for _ in range(rounds):
        acc = []
        for xs, ys in ladders:
            yp = list(ys)
            pr.shuffle(yp)
            b = _slope(xs, yp)
            if b is not None:
                acc.append(b)
        null.append(sum(acc) / float(len(acc)) if acc else 0.0)
    null.sort()
    lo = null[int(0.025 * rounds)]
    hi = null[int(0.975 * rounds) - 1]
    p = sum(1 for v in null if abs(v) >= abs(mb)) / float(rounds)

    print("")
    print("  ② within-tick β: n=%d tick · mean β=%+.5f (sd %.5f · se %.5f)" % (n, mb, sd, se))
    print("     ζ-라벨 within-tick 순열 null95%% = [%+.5f, %+.5f] · p=%.4f" % (lo, hi, p))
    print("     해상한계(=null95%% 반폭) = %.5f — 이보다 작은 참 β 는 미측정(VOID, 음성 아님)"
          % max(abs(lo), abs(hi)))

    outside = not (lo <= mb <= hi)
    print("")
    if outside and mb < 0:
        v = "🟢 CHANNEL-CARRIES-PHYSICS — β<0 (예측 부호) · within-tick 순열 null 밖"
    elif outside and mb > 0:
        v = ("🔄 SIGN-INVERTED — β>0 유의 = 예측과 반대 ⇒ **INVALID**(배선 감사) · 음성 아님")
    else:
        v = ("🧱 CHANNEL-CLOSED(후보) — β 가 null 대역 안. ⚠️ 이는 H_9712 의 π-dose PASS"
             "(Δπ=+0.1599 · p=0.0082)와 **모순** ⇒ 두 계기 대질이 다음 H · 지금 못 박지 말 것")
    print("  ⇒ VERDICT: " + v)
    print("     범위: ζ-arm 은 **채널이 무엇을 나를 수 있나** 의 계기 증거다 —")
    print("     '라이브 데몬이 무엇을 하고 있나' 의 증거로 인용 금지(라이브 z 는 사실상 상수).")
    return 0


def _pc2_occupancy(argv):
    """H_9636 R-A WINDOW-OCCUPANCY — the readout moved to where the manipulation LIVES.

    `anima-py evaluate --pc2-direction <traces_dir> --occupancy [--perm N] [--seed N]`

    WHY THIS EXISTS. H_9576 read the PC2->mouth channel through D = |bigrams(text) &
    bigrams(seed)| / |bigrams(text)| and called the null a wall. H_9629 then proved D is
    broken three ways, and the third defect is the one that matters here:

      (1) the DENOMINATOR is the steered text's OWN distinct-bigram count, so a diversity
          shift moves D with no reference to the seed at all (rho(dD, d|distinct|) =
          -0.510 bias / -0.531 rng -- arm-INDEPENDENT, i.e. pure noise, ~7x the target);
      (2) set() collapses repeated filler to one element (away-pole sign-inversion artifact);
      (3) the bias acts on a T=24 SLIDING WINDOW (core/decode.py:2100), but the seed is ~52B
          -- so the seed's leading bytes were never inside any window the manipulation
          touched, and after 24 generated bytes the window is entirely self-generated.
          D was scoring a quantity the steering cannot reach.

    So this readout asks the manipulation's OWN question instead. The bias subtracts z from
    every byte already in the model's T-window; the proximal observable of that is simply:
    did the drawn byte come from the window?

        I_t = 1[ byte_t in set(window_t) ],  window_t = (seed ++ generated[:t])[-24:]
        pi_bar = mean(I_t) over lm-steps,    DV = paired dpi = pi_bar(steer) - pi_bar(base)

    PREDICTION (pre-registered, from the code not from H_9576's rho): z<0 (the live-dominant
    pole) BOOSTS in-window bytes => dpi > 0. Sign is fixed by decode.py's `row[v] -= z`, so
    picking this readout cannot be tune-to-green -- its target was specified by the engine.

    WHY IT DODGES D'S CONTAMINATION. The denominator is a COUNT OF STEPS, not a diversity.
    Each I_t is defined against that step's own trajectory window, so this is never a
    cross-arm text comparison: the manipulation is re-applied at every step and re-measured
    at every step, which is why it does not wash out in the downstream re-roll cascade the
    way a step-0-anchored quantity does.

    ANCHOR-REPLAY INVARIANT (hard gate, opens nothing until it passes). The grounded
    anchor-copy step never reaches the bias (decode.py:2041), so it must be excluded.
    generator.py:512 claims `grounded=0 / lm=80` at the production l_min=8 -- this replays
    _dg_anchor_copy per step and ASSERTS it, rather than trusting the comment. A tick whose
    replay disagrees is INVALID, not negative.
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import random as _prand

    T_WIN = 24
    L_MIN = 8            # production call: clm_decode_grounded(ckpt, seed, 80, texts, 8, mouth)
    LADDER = (0.05, 0.10, 0.20, 0.40)

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> --occupancy")
        return 2
    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260717)

    try:
        from decode import _dg_anchor_copy as _anchor_copy
    except ImportError:
        _anchor_copy = None

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _rows(arm, sd):
        p = os.path.join(d, "%s_s%d.jsonl" % (arm, sd))
        if not os.path.exists(p):
            return [], {}
        out, meta = [], {}
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if r.get("_meta"):
                meta = r
            else:
                out.append(r)
        return out, meta

    seeds = []
    for f in sorted(_glob.glob(os.path.join(d, "off_s*.jsonl"))):
        try:
            seeds.append(int(os.path.basename(f)[len("off_s"):-len(".jsonl")]))
        except ValueError:
            continue
    if not seeds:
        print("  ⇒ ⛔ no off_s<seed>.jsonl traces under " + d)
        return 2

    print("=== anima evaluate --pc2-direction --occupancy — R-A 창-점유율 (card H_9636) ===")
    print("traces: %s  (seeds: %s · perm=%d · perm-seed=%d)"
          % (d, ",".join(str(s) for s in seeds), rounds, rseed))
    print("readout: I_t = 1[byte_t ∈ set(window_t)] · window=(seed++gen[:t])[-24:] · π̄=mean over lm-steps")
    print("DV:     paired Δπ̄ = π̄(steer) − π̄(base)   예측(코드가 지정): z<0 ⇒ in-window 부스트 ⇒ Δπ̄>0")
    print("bar:    ① anchor-replay 불변식 100% ② 합성 사다리 강단조 ③ Δπ̄ vs rng-pedestal + 변위창 placebo")
    print("")

    def _occ_steps(seed_b, txt_b, anchors):
        """-> (list of I_t over lm-steps, n_grounded, n_mismatch). Replays the anchor-copy
        classifier AND self-verifies it: on a step the replay calls grounded, the trace byte
        MUST equal the byte anchor-copy returns (the live path copies it verbatim). A single
        mismatch means the replay does not reproduce the live decode — the classification is
        broken, so the tick is INVALID rather than negative. Without this check a wrong
        anchor list would silently mis-split lm/grounded steps and quietly corrupt pi_bar."""
        ind, grounded, mismatch = [], 0, 0
        ctx = bytearray(seed_b)
        for i in range(len(txt_b)):
            b = txt_b[i]
            if _anchor_copy is not None and anchors:
                cb = _anchor_copy(bytes(ctx), anchors, L_MIN, T_WIN)
                if cb >= 0:
                    grounded += 1
                    if cb != b:
                        mismatch += 1
                    ctx.append(b)
                    continue
            win = bytes(ctx[-T_WIN:]) if len(ctx) >= T_WIN else bytes(ctx)
            ind.append(1 if b in set(win) else 0)
            ctx.append(b)
        return ind, grounded, mismatch

    # ── ① anchor-replay invariant ────────────────────────────────────────────
    tot_g = 0
    tot_mm = 0
    tot_steps = 0
    n_meta_anchor = 0
    for sd in seeds:
        rows, meta = _rows("off", sd)
        mem = meta.get("mem_text") or ""
        anchors = [mem.encode("utf-8", "surrogateescape")] if mem else []
        if anchors:
            n_meta_anchor += 1
        for r in rows:
            if not r.get("emit"):
                continue
            _i, g, mm = _occ_steps(_b64(r.get("seed_b64")), _b64(r.get("gtext_b64")), anchors)
            tot_g += g
            tot_mm += mm
            tot_steps += g + len(_i)
    g_rate = (tot_g / float(tot_steps)) if tot_steps else 0.0
    print("  ① anchor-replay: grounded %d / %d step (%.2f%%) · anchor 보유 seed %d/%d · classifier %s"
          % (tot_g, tot_steps, 100.0 * g_rate, n_meta_anchor, len(seeds),
             "LIVE" if _anchor_copy is not None else "UNAVAILABLE"))
    if _anchor_copy is None:
        print("     ⇒ ⛔ INVALID — core.decode._dg_anchor_copy 를 import 못 함 · lm-step 분류 불가")
        return 0
    print("     ⇒ 자기검증: grounded 로 분류된 step 중 트레이스 byte ≠ anchor-copy byte = %d 건 %s"
          % (tot_mm, "✅ (재생이 라이브 decode 를 재현)" if tot_mm == 0 else "❌ 재생 불일치 = 분류 고장"))
    print("     ⇒ generator.py:512 의 'grounded=0 / lm=80 @ l_min=8' 주석 대비: %s"
          % ("일치" if tot_g == 0 else
             ("불일치(%d step grounded) — 재생 자기검증이 통과했으므로 **주석이 stale**(그 주석은 "
              "generator 자신의 ideate 경로 기준 · chat 데몬 경로가 아니다)" % tot_g if tot_mm == 0 else
              "불일치(%d step) 이나 자기검증도 실패 ⇒ 내 재생을 먼저 의심하라" % tot_g)))

    def _rank(v):
        n = len(v)
        s = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r

    def _mean(x):
        return (sum(x) / float(len(x))) if x else 0.0

    def _sd(x):
        if len(x) < 2:
            return 0.0
        m = _mean(x)
        return (sum((v - m) ** 2 for v in x) / float(len(x) - 1)) ** 0.5

    def _pi(seed_b, txt_b, anchors):
        ind, _g, _mm = _occ_steps(seed_b, txt_b, anchors)
        return _mean(ind), len(ind)

    def _collect(arm):
        """-> list of (seed, z, dpi) over emit ticks that carry a steered text."""
        out = []
        for sd in seeds:
            o, meta = _rows("off", sd)
            a, _m2 = _rows(arm, sd)
            mem = meta.get("mem_text") or ""
            anchors = [mem.encode("utf-8", "surrogateescape")] if mem else []
            for i in range(min(len(o), len(a))):
                if not o[i].get("emit"):
                    continue
                base_b = _b64(o[i].get("gtext_b64"))
                steer_b = _b64(a[i].get("gtext_pc2_b64"))
                seed_b = _b64(a[i].get("seed_b64"))
                z = a[i].get("pc2_z")
                if not steer_b or not seed_b or z is None:
                    continue
                pb, nb_ = _pi(seed_b, base_b, anchors)
                ps, _ns = _pi(seed_b, steer_b, anchors)
                if nb_ == 0:
                    continue
                out.append((sd, float(z), ps - pb))
        return out

    # ── ② synthetic ladder certification (trace-only · true effect KNOWN) ────
    print("")
    print("  ② 합성 사다리 자격시험 (참효과를 아는 개입 · 트레이스-only)")
    rng_ = _prand.Random(rseed)

    def _resample(seed_b, txt_b, anchors, q, mode):
        """Rebuild the text replacing each lm-step byte w.p. q. mode: 'in' = draw from the
        step's own window (pi should RISE), 'out' = draw outside it (pi should FALL),
        'lag' = draw from the DISPLACED window lag 25..48 (placebo: in-window pi must NOT
        move beyond pedestal)."""
        ctx = bytearray(seed_b)
        new = bytearray()
        for i in range(len(txt_b)):
            b = txt_b[i]
            win = bytes(ctx[-T_WIN:]) if len(ctx) >= T_WIN else bytes(ctx)
            wset = set(win)
            if rng_.random() < q and wset:
                if mode == "in":
                    b = rng_.choice(sorted(wset))
                elif mode == "out":
                    cand = [v for v in range(32, 127) if v not in wset]
                    if cand:
                        b = rng_.choice(cand)
                elif mode == "lag":
                    lo = len(ctx) - 48
                    hi = len(ctx) - 24
                    band = bytes(ctx[max(0, lo):max(0, hi)])
                    bset = sorted(set(band) - wset)
                    if bset:
                        b = rng_.choice(bset)
            new.append(b)
            ctx.append(b)
        return bytes(new)

    lad = {}
    for mode in ("in", "out", "lag"):
        lad[mode] = []
        for q in LADDER:
            ds = []
            for sd in seeds:
                o, meta = _rows("off", sd)
                mem = meta.get("mem_text") or ""
                anchors = [mem.encode("utf-8", "surrogateescape")] if mem else []
                for r in o:
                    if not r.get("emit"):
                        continue
                    seed_b = _b64(r.get("seed_b64"))
                    base_b = _b64(r.get("gtext_b64"))
                    if not seed_b or not base_b:
                        continue
                    pb, nb_ = _pi(seed_b, base_b, anchors)
                    if nb_ == 0:
                        continue
                    alt = _resample(seed_b, base_b, anchors, q, mode)
                    pa, _n = _pi(seed_b, alt, anchors)
                    ds.append(pa - pb)
            lad[mode].append((q, _mean(ds), len(ds)))
        row = " · ".join("q=%.2f Δπ̄=%+.4f" % (q, m) for q, m, _n in lad[mode])
        print("     %-4s %s" % (mode, row))

    # frozen-first: the bar comes from the rng arm, computed BEFORE bias is opened
    rng_rows = _collect("rng")
    sd_rng = _sd([r[2] for r in rng_rows])
    bar = 2.0 * sd_rng
    print("     동결 bar (rng arm 서 먼저 산출 · bias 개봉 전): 2·sd(Δπ̄_rng) = %.4f" % bar)

    up = [m for _q, m, _n in lad["in"]]
    dn = [m for _q, m, _n in lad["out"]]
    mono_up = all(up[i] < up[i + 1] for i in range(len(up) - 1))
    mono_dn = all(dn[i] > dn[i + 1] for i in range(len(dn) - 1))
    at20_up = lad["in"][2][1]
    lag_max = max(abs(m) for _q, m, _n in lad["lag"])
    cert_ok = mono_up and mono_dn and at20_up > bar and tot_mm == 0
    print("     강단조: in %s · out %s | Δπ̄(in,q=.20)=%+.4f vs bar %.4f | 변위창 placebo max|Δπ̄|=%.4f"
          % (mono_up, mono_dn, at20_up, bar, lag_max))
    if not cert_ok:
        why = []
        if not (mono_up and mono_dn):
            why.append("사다리 비단조/역단조 ⇒ INSTRUMENT-DEAD/INVERTED")
        if at20_up <= bar:
            why.append("q=.20 이 동결 bar 미달 ⇒ INSTRUMENT-DEAD")
        if tot_mm != 0:
            why.append("anchor-replay 자기검증 %d 건 불일치 ⇒ INVALID" % tot_mm)
        print("     ⇒ ⛔ 계기 인증 FAIL — %s" % (" · ".join(why)))
        print("     ⇒ 아래 라이브 판독을 열지 않는다 (인증 안 된 계기로 음성을 읽는 게 H_9576 의 죽음이었다).")
        return 0
    print("     ⇒ 계기 인증 PASS ✅ (참효과를 아는 사다리에 단조 반응 · placebo 무반응)")

    # ── ③ live read: paired dpi vs 2 controls ───────────────────────────────
    print("")
    print("  ③ 라이브 판독 — paired Δπ̄ vs 2 통제 (ρ 는 은퇴: z 분산-기아 · IQR 0.05)")
    res = {}
    for arm in ("bias", "rng"):
        rows = rng_rows if arm == "rng" else _collect(arm)
        dd = [r[2] for r in rows]
        m = _mean(dd)
        s = _sd(dd)
        n = len(dd)
        se = (s / (n ** 0.5)) if n else 0.0
        # sign-permutation null on the paired differences
        null = []
        pr = _prand.Random(rseed + 1)
        for _ in range(rounds):
            null.append(_mean([v if pr.random() < 0.5 else -v for v in dd]))
        null.sort()
        lo = null[int(0.025 * rounds)] if null else 0.0
        hi = null[int(0.975 * rounds) - 1] if null else 0.0
        p = (sum(1 for v in null if abs(v) >= abs(m)) / float(rounds)) if null else 1.0
        res[arm] = {"m": m, "n": n, "lo": lo, "hi": hi, "p": p, "se": se}
        print("     %-4s n=%-4d mean Δπ̄=%+.4f (se %.4f) · null95%%=[%+.4f,%+.4f] · p=%.3f"
              % (arm, n, m, se, lo, hi, p))

    b, r = res["bias"], res["rng"]
    zs = [x[1] for x in _collect("bias")]
    n_neg = sum(1 for v in zs if v < 0)
    outside = not (b["lo"] <= b["m"] <= b["hi"])
    beats = abs(b["m"]) > abs(r["m"])
    print("")
    print("     z<0 tick 비율 %d/%d (%.1f%%) ⇒ 사전예측 = Δπ̄>0 우세"
          % (n_neg, len(zs), 100.0 * n_neg / float(len(zs) or 1)))
    if outside and b["m"] > 0 and beats:
        v = "🟢 CHANNEL-CARRIES-PHYSICS — Δπ̄>0 · null95% 밖 · rng 대비 우세 (예측 부호)"
    elif outside and b["m"] < 0:
        v = "🔄 SIGN-INVERTED — null95% 밖이나 예측과 반대 ⇒ bias 부호 배선 감사 (INVALID, 음성 아님)"
    else:
        v = "🧱 NULL — Δπ̄ 가 null95% 대역 안: 인증된 근접 계기서도 채널 무반응"
    print("  ⇒ VERDICT: " + v)
    print("     범위: 이건 **근접(물리) 판정**이지 의미 판정이 아니다 — 원격(의미)은 R-B/ζ-fire 전엔 열리지 않는다.")
    print("     해상한계 = 2·sd(Δπ̄_rng)/√n = %.5f · 이보다 작은 참효과는 미측정(VOID, 음성 아님)."
          % (bar / ((b["n"] or 1) ** 0.5)))
    return 0


def _pc2_direction(argv):
    """H_9576 PC2→MOUTH DIRECTION — engine-native verdict over decision traces.

    `anima-py evaluate --pc2-direction <traces_dir> [--perm N] [--seed N]`

    Reads the traces `anima-py chat --pc2-mouth {off,bias,rng}` already wrote (NO decode, like
    --emit-gate-census / --dead-census) and renders the three frozen criteria of the PC2→mouth
    experiment. It exists because the verdict statistic itself must be engine-native: a number a
    probe beside the engine produced is not cementable (a_experiment_engine_native · H_9303/H_9307).

      (1) isolation  — is the emit sequence byte-identical across off/bias/rng? (Stage-A: the gate
                       hears the BASE candidate; steering is applied only after emit is fixed, so
                       any drift here means the isolation leaked and the run is INVALID, not negative)
      (2) channel    — does the steered text actually differ from base on emit ticks?
      (3) direction  — Spearman rho(z_PC2, D_base - D_steer) where D = byte-bigram overlap between a
                       text and its own decode seed. PREDICTION: z>0 (originality pole) pushes the
                       mouth OFF its context => D_base - D_steer > 0 => rho > 0. Judged against a
                       within-seed permutation null (breaks the z<->text pairing, keeps both
                       marginals) — a raw rho is not a verdict (p7 · collapse-delta vs controls),
                       and the rng arm is the second control (same |z| draw-stream re-key, no
                       direction), so BIAS must beat BOTH the permutation null and rng.

    Frozen bar (do not retune — a_break_the_wall/no tune-to-green): rho outside the null 95% band
    AND beating rng = direction CRACK; inside the band = W2 wall (the byte granularity cannot
    express the PC2 semantics). Underpowered n is VOID, never a negative (power-before-negative).
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import random as _prand

    if "--z-census" in argv:                      # H_9712 dose/exposure gate (sister sub-mode)
        return _z_census(argv)

    d = ([x for x in argv if not x.startswith("--")] or [""])[0]
    if not d:
        print("  ⇒ ⛔ usage: anima-py evaluate --pc2-direction <traces_dir> [--perm N] [--seed N]")
        return 2
    if "--cascade-null" in argv:
        return _pc2_cascade_null(d, argv)
    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260716)

    def _rows(arm, sd):
        p = os.path.join(d, "%s_s%d.jsonl" % (arm, sd))
        if not os.path.exists(p):
            return []
        out = []
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if not r.get("_meta"):
                out.append(r)
        return out

    seeds = []
    for f in sorted(_glob.glob(os.path.join(d, "off_s*.jsonl"))):
        try:
            seeds.append(int(os.path.basename(f)[len("off_s"):-len(".jsonl")]))
        except ValueError:
            continue
    if not seeds:
        print("  ⇒ ⛔ no off_s<seed>.jsonl traces under " + d)
        return 2

    print("=== anima evaluate --pc2-direction — PC2→MOUTH (card H_9576) ===")
    print("traces: %s  (seeds: %s · perm=%d · perm-seed=%d)"
          % (d, ",".join(str(s) for s in seeds), rounds, rseed))
    print("pipe:   anima-py chat --pc2-mouth {off,bias,rng} traces → D=bigram-overlap(text, seed)")
    print("bar:    (1) emit byte-identical  (2) steered≠base  (3) rho>0 outside null-95% AND > rng")
    print("")

    # ── (1) isolation ────────────────────────────────────────────────────────
    iso = True
    for sd in seeds:
        e = {}
        for arm in ("off", "bias", "rng"):
            e[arm] = [1 if r.get("emit") else 0 for r in _rows(arm, sd)]
        ok = bool(e["off"]) and e["off"] == e["bias"] == e["rng"]
        iso = iso and ok
        print("  (1) seed %-5d off==bias==rng %-5s  (emit %d/%d)"
              % (sd, str(ok), sum(e["off"]), len(e["off"])))
    print("      ⇒ isolation: %s" % ("PASS" if iso else "INVALID (Stage-A leaked)"))
    if not iso:
        print("      ⇒ ⛔ VERDICT INVALID — a leaked gate makes (2)/(3) unreadable, not negative.")
        return 0

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _big(bs):
        return set(bs[i:i + 2] for i in range(len(bs) - 1))

    def _ov(txt_b, seed_b):
        a, b = _big(txt_b), _big(seed_b)
        return (len(a & b) / float(len(a))) if a else 0.0

    def _rank(v):
        n = len(v)
        s = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r

    def _spearman(x, y):
        n = len(x)
        if n < 3:
            return 0.0
        rx, ry = _rank(x), _rank(y)
        mx, my = sum(rx) / n, sum(ry) / n
        num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
        dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
        dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
        return (num / (dx * dy)) if dx > 0 and dy > 0 else 0.0

    def _collect(arm):
        out, ndiff, ntot = [], 0, 0
        for sd in seeds:
            o, a = _rows("off", sd), _rows(arm, sd)
            for i in range(min(len(o), len(a))):
                if not o[i].get("emit"):
                    continue
                base_b = _b64(o[i].get("gtext_b64"))
                steer_b = _b64(a[i].get("gtext_pc2_b64"))
                if not steer_b:
                    continue
                ntot += 1
                if steer_b != base_b:
                    ndiff += 1
                seed_b = _b64(a[i].get("seed_b64"))
                z = a[i].get("pc2_z")
                if z is None or not seed_b:
                    continue
                out.append((sd, float(z), _ov(base_b, seed_b) - _ov(steer_b, seed_b)))
        return out, ndiff, ntot

    # ── (2) channel + (3) direction ──────────────────────────────────────────
    res = {}
    for arm in ("bias", "rng"):
        rows, ndiff, ntot = _collect(arm)
        zs = [r[1] for r in rows]
        dds = [r[2] for r in rows]
        obs = _spearman(zs, dds)

        by_seed = {}
        for i, r in enumerate(rows):
            by_seed.setdefault(r[0], []).append(i)
        rng_ = _prand.Random(rseed)
        null = []
        for _ in range(rounds):
            pz = list(zs)
            for _sd, idxs in by_seed.items():
                vals = [zs[i] for i in idxs]
                rng_.shuffle(vals)
                for i, v in zip(idxs, vals):
                    pz[i] = v
            null.append(_spearman(pz, dds))
        null.sort()
        lo = null[int(0.025 * rounds)] if null else 0.0
        hi = null[int(0.975 * rounds) - 1] if null else 0.0
        p = (sum(1 for v in null if abs(v) >= abs(obs)) / float(rounds)) if null else 1.0
        res[arm] = {"rho": obs, "lo": lo, "hi": hi, "p": p, "n": len(rows)}
        print("  (2) %-4s steered≠base %d/%d" % (arm, ndiff, ntot))
        print("  (3) %-4s n=%-4d rho=%+.3f · null95%%=[%+.3f,%+.3f] · p=%.3f"
              % (arm, len(rows), obs, lo, hi, p))

    b, r = res["bias"], res["rng"]
    outside = not (b["lo"] <= b["rho"] <= b["hi"])
    beats_rng = b["rho"] > r["rho"]
    print("")
    if outside and b["rho"] > 0 and beats_rng:
        v = "🟢 DIRECTION CRACK — rho outside null-95%, predicted sign, beats rng"
    elif outside and b["rho"] < 0:
        v = "🧱 W2 WALL (sign-inverted) — rho outside null-95% but OPPOSITE the prediction"
    else:
        v = "🧱 W2 WALL — rho inside the null-95% band: byte granularity cannot express PC2"
    print("  ⇒ VERDICT: " + v)
    print("     resolvable |rho| at n=%d is about %.2f (null-95%% half-width) — a smaller true"
          % (b["n"], max(abs(b["lo"]), abs(b["hi"]))))
    print("     effect stays UNMEASURED, not refuted (power-before-negative-verdict).")
    return 0


def _spearman_pub(x, y):
    """Spearman rho (tie-averaged ranks) — module-level twin of _pc2_direction's local helper."""
    n = len(x)
    if n < 3:
        return 0.0

    def _rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[s[k]] = avg
            i = j + 1
        return r

    rx, ry = _rank(x), _rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    return (num / (dx * dy)) if dx > 0 and dy > 0 else 0.0


def _pc2_cascade_null(d, argv):
    """H_9629 ΔD TRUE-ZERO PEDESTAL — is ΔD a readable quantity at all?

    `anima-py evaluate --pc2-direction <traces_dir> --cascade-null [--perm N] [--seed N]`

    H_9576 read a NEGATIVE (rho(z, ΔD) inside the null band ⇒ "W2 wall") without ever measuring
    the SNR of ΔD itself. This sub-mode supplies the missing zero-truth pedestal
    (phi-estimator-needs-zero-truth-pedestal · positive-control-before-reading-a-negative):
    if a semantics-free perturbation of the same dose moves ΔD as much as the steered arm does,
    then per-tick direction is UNMEASURED at n=270 — VOID, not a negative.

    ARMS (all trace-read · NO decode — the ckpt is pool-side; see the SPEC block for what needs one)

      off       ΔD ≡ 0 by construction. Certified here by checking that the BASE gtext is
                byte-identical across off/bias/rng (if it is not, the pedestal shares no baseline
                with the steered arms and everything below is unreadable → INVALID).
      static    ZERO-TRUTH, ZERO-CASCADE floor: one deterministic letter substitution at the tick's
                OWN first base↔bias divergence byte (control-must-match-mediating-covariate: the
                dose is positioned where the bias arm's physical effect actually starts, not at an
                arbitrary index). Semantic capacity 0. Because the trace cannot re-roll the decode
                downstream of the substituted byte, this is a strict LOWER BOUND on cascade noise —
                a ratio computed against it OVERSTATES the bias arm's SNR, so a VOID read against
                `static` holds a fortiori.
      rng       ZERO-TRUTH, FULL-CASCADE pedestal: the H_9576 rng arm is a dose-matched re-key of
                the same |z| draw-stream with the DIRECTION scrambled out — a real decode with the
                real downstream re-roll and zero semantic direction. This is the closest thing the
                traces hold to the card's cascade arm, and it is the PRIMARY denominator.
      oracle    READOUT positive control (dose ladder, k bytes at the same divergence locus):
                toward-seed (bytes copied from the decode seed ⇒ D↑ ⇒ ΔD<0) and away-seed
                (a byte absent from the seed ⇒ D↓ ⇒ ΔD>0). Certifies that D is not a dead readout
                — that ΔD *can* rise above the pedestal when a directed effect is really applied.
                It does NOT stand in for the card's ζ=±4 saturation arm (that one needs a decode).

    Frozen bar (card H_9629 · do not retune):
      ratio = var(ΔD_bias)/var(ΔD_cascade) ≤ 1.5              ⇒ VOID-BY-SNR (H_9576 direction KILL
                                                                 reclassified as unmeasured at
                                                                 per-tick granularity)
      ratio > 3 ∧ positive PASS                               ⇒ readout valid · KILL stands
      positive control cannot beat the pedestal               ⇒ INVALID
      below-chance: pedestal indistinguishable from off       ⇒ instrument wiring defect · INVALID
    """
    import glob as _glob
    import json as _pj
    import base64 as _pb
    import random as _prand
    import math as _pm

    rounds = evaluate_intval(argv, "--perm", 2000)
    rseed = evaluate_intval(argv, "--seed", 20260716)

    def _rows(arm, sd):
        p = os.path.join(d, "%s_s%d.jsonl" % (arm, sd))
        if not os.path.exists(p):
            return []
        out = []
        for l in open(p):
            l = l.strip()
            if not l:
                continue
            try:
                r = _pj.loads(l)
            except ValueError:
                continue
            if not r.get("_meta"):
                out.append(r)
        return out

    seeds = []
    for f in sorted(_glob.glob(os.path.join(d, "off_s*.jsonl"))):
        try:
            seeds.append(int(os.path.basename(f)[len("off_s"):-len(".jsonl")]))
        except ValueError:
            continue
    if not seeds:
        print("  ⇒ ⛔ no off_s<seed>.jsonl traces under " + d)
        return 2

    def _b64(s):
        try:
            return _pb.b64decode(s) if s else b""
        except (ValueError, TypeError):
            return b""

    def _big(bs):
        return set(bs[i:i + 2] for i in range(len(bs) - 1))

    def _ov(txt_b, seed_b):
        a, b = _big(txt_b), _big(seed_b)
        return (len(a & b) / float(len(a))) if a else 0.0

    def _divpos(a, b):
        """First byte where the steered text leaves the base — the bias arm's own dose locus."""
        n = min(len(a), len(b))
        for i in range(n):
            if a[i] != b[i]:
                return i
        return n if n < max(len(a), len(b)) else max(0, len(a) // 2)

    def _static_mut(base_b, pos):
        """Deterministic semantics-free single-byte substitution (2nd-best byte needs logits)."""
        if not base_b:
            return base_b
        b = bytearray(base_b)
        pos = min(max(pos, 0), len(b) - 1)
        c = 97 + ((b[pos] + pos) % 26)
        if c == b[pos]:
            c = 97 + ((c - 97 + 1) % 26)
        b[pos] = c
        return bytes(b)

    def _oracle_mut(base_b, seed_b, pos, k, toward):
        if not base_b:
            return base_b
        b = bytearray(base_b)
        pos = min(max(pos, 0), max(0, len(b) - 1))
        for j in range(k):
            i = pos + j
            if i >= len(b):
                break
            b[i] = seed_b[j % len(seed_b)] if (toward and seed_b) else 0x01
        return bytes(b)

    def _var(v):
        n = len(v)
        if n < 2:
            return 0.0
        m = sum(v) / n
        return sum((x - m) ** 2 for x in v) / (n - 1)

    # ── F distribution tail (prereg statistic) ───────────────────────────────
    def _betacf(a, b, x):
        MAXIT, EPS, FPMIN = 200, 3.0e-12, 1.0e-300
        qab, qap, qam = a + b, a + 1.0, a - 1.0
        c = 1.0
        dd = 1.0 - qab * x / qap
        if abs(dd) < FPMIN:
            dd = FPMIN
        dd = 1.0 / dd
        h = dd
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            dd = 1.0 + aa * dd
            if abs(dd) < FPMIN:
                dd = FPMIN
            c = 1.0 + aa / c
            if abs(c) < FPMIN:
                c = FPMIN
            dd = 1.0 / dd
            h *= dd * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            dd = 1.0 + aa * dd
            if abs(dd) < FPMIN:
                dd = FPMIN
            c = 1.0 + aa / c
            if abs(c) < FPMIN:
                c = FPMIN
            dd = 1.0 / dd
            de = dd * c
            h *= de
            if abs(de - 1.0) < EPS:
                break
        return h

    def _betai(a, b, x):
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        lb = (_pm.lgamma(a + b) - _pm.lgamma(a) - _pm.lgamma(b)
              + a * _pm.log(x) + b * _pm.log(1.0 - x))
        bt = _pm.exp(lb)
        if x < (a + 1.0) / (a + b + 2.0):
            return bt * _betacf(a, b, x) / a
        return 1.0 - bt * _betacf(b, a, 1.0 - x) / b

    def _f_two_sided_p(f, d1, d2):
        if f <= 0.0 or d1 < 1 or d2 < 1:
            return 1.0
        cdf = _betai(d1 / 2.0, d2 / 2.0, d1 * f / (d1 * f + d2))
        return max(0.0, min(1.0, 2.0 * min(cdf, 1.0 - cdf)))

    print("=== anima evaluate --pc2-direction --cascade-null — ΔD ZERO-TRUTH PEDESTAL (card H_9629) ===")
    print("traces: %s  (seeds: %s · perm=%d · perm-seed=%d)"
          % (d, ",".join(str(s) for s in seeds), rounds, rseed))
    print("claim:  var(ΔD) is dominated by decode-cascade noise, not by PC2 direction ⇒ H_9576's")
    print("        rho≈0 may be VOID-BY-SNR (unmeasured), not a negative.")
    print("bar:    ratio=var(ΔD_bias)/var(ΔD_cascade) ≤1.5 ⇒ VOID-BY-SNR · >3 ∧ positive PASS ⇒ KILL stands")
    print("        positive < pedestal ⇒ INVALID · pedestal==off ⇒ wiring defect INVALID")
    print("")

    # ── (0) baseline wiring — the off arm's ΔD must be 0 BY CONSTRUCTION ──────
    base_ok = True
    for sd in seeds:
        o, b_, r_ = _rows("off", sd), _rows("bias", sd), _rows("rng", sd)
        n = min(len(o), len(b_), len(r_))
        same = all(o[i].get("gtext_b64") == b_[i].get("gtext_b64") == r_[i].get("gtext_b64")
                   for i in range(n))
        base_ok = base_ok and same and n > 0
        print("  (0) seed %-5d base gtext off==bias==rng %-5s  (ticks %d) ⇒ ΔD_off ≡ 0" % (sd, str(same), n))
    print("      ⇒ baseline: %s" % ("PASS" if base_ok else "INVALID (arms do not share a baseline)"))
    if not base_ok:
        print("      ⇒ ⛔ VERDICT INVALID — no shared base means ΔD is not the same quantity across arms.")
        return 0
    print("")

    # ── collect the paired per-tick ΔD for every arm ─────────────────────────
    DOSES = (1, 2, 4, 8, 16)
    dd = {"bias": [], "rng": [], "static": []}
    orc = {}
    for k in DOSES:
        orc[("toward", k)] = []
        orc[("away", k)] = []
    nz_static = 0
    for sd in seeds:
        o, b_, r_ = _rows("off", sd), _rows("bias", sd), _rows("rng", sd)
        for i in range(min(len(o), len(b_), len(r_))):
            if not o[i].get("emit"):
                continue
            base_b = _b64(o[i].get("gtext_b64"))
            bias_b = _b64(b_[i].get("gtext_pc2_b64"))
            rng_b = _b64(r_[i].get("gtext_pc2_b64"))
            seed_b = _b64(o[i].get("seed_b64"))
            if not base_b or not bias_b or not rng_b or not seed_b:
                continue
            d0 = _ov(base_b, seed_b)
            pos = _divpos(base_b, bias_b)
            stat_b = _static_mut(base_b, pos)
            if stat_b != base_b:
                nz_static += 1
            dd["bias"].append(d0 - _ov(bias_b, seed_b))
            dd["rng"].append(d0 - _ov(rng_b, seed_b))
            dd["static"].append(d0 - _ov(stat_b, seed_b))
            for k in DOSES:
                orc[("toward", k)].append(d0 - _ov(_oracle_mut(base_b, seed_b, pos, k, True), seed_b))
                orc[("away", k)].append(d0 - _ov(_oracle_mut(base_b, seed_b, pos, k, False), seed_b))

    n = len(dd["bias"])
    if n < 10:
        print("  ⇒ ⛔ VOID — only n=%d paired emit ticks; the ratio is unpowered." % n)
        return 0

    print("  (1) per-tick ΔD (paired · n=%d emit ticks · D = byte-bigram overlap(text, decode seed))" % n)
    print("      %-8s %-6s %-11s %-11s %-11s" % ("arm", "n", "mean", "sd", "var"))
    print("      %-8s %-6d %+.3e %+.3e %+.3e" % ("off", n, 0.0, 0.0, 0.0))
    for arm in ("static", "rng", "bias"):
        v = dd[arm]
        m = sum(v) / len(v)
        va = _var(v)
        print("      %-8s %-6d %+.3e %+.3e %+.3e" % (arm, len(v), m, va ** 0.5, va))
    print("      static substitution actually moved the text on %d/%d ticks" % (nz_static, n))
    print("")

    # ── (2) below-chance cell — does the pedestal differ from off at all? ─────
    ped_live = {}
    for arm in ("static", "rng"):
        nz = sum(1 for x in dd[arm] if x != 0.0)
        live = _var(dd[arm]) > 0.0 and nz > 0
        ped_live[arm] = live
        print("  (2) pedestal %-6s vs off: ΔD≠0 on %d/%d ticks · var>0 %-5s ⇒ %s"
              % (arm, nz, n, str(_var(dd[arm]) > 0.0), "LIVE" if live else "DEAD (perturbation inert)"))
    if not ped_live["rng"]:
        print("      ⇒ ⛔ VERDICT INVALID — the cascade pedestal is indistinguishable from off")
        print("         (below-chance cell: the perturbation never fired · instrument wiring defect).")
        return 0
    print("")

    # ── (3) readout positive control — can ΔD rise above the pedestal? ───────
    sd_ped = _var(dd["rng"]) ** 0.5
    print("  (3) READOUT positive control — directed dose ladder at the same divergence locus")
    print("      (toward-seed ⇒ D↑ ⇒ ΔD<0 · away-seed ⇒ D↓ ⇒ ΔD>0 · bar: |mean| > 2·sd(ΔD_rng)=%.3e)" % (2 * sd_ped))
    pos_ok = {}
    for pole in ("toward", "away"):
        means = []
        for k in DOSES:
            v = orc[(pole, k)]
            means.append(sum(v) / len(v))
        line = "  ".join("k=%-2d %+.3e" % (k, m) for k, m in zip(DOSES, means))
        mono = all(abs(means[i + 1]) >= abs(means[i]) - 1e-12 for i in range(len(means) - 1))
        signs = all((m <= 0) if pole == "toward" else (m >= 0) for m in means[1:])
        big = abs(means[-1]) > 2 * sd_ped
        pos_ok[pole] = mono and signs and big
        print("      %-7s %s" % (pole, line))
        print("              monotone %-5s · sign-as-predicted %-5s · k=16 beats pedestal %-5s ⇒ %s"
              % (str(mono), str(signs), str(big), "PASS" if pos_ok[pole] else "FAIL"))
    positive = pos_ok["toward"] and pos_ok["away"]
    print("      ⇒ readout positive control: %s" % ("PASS (D is a live, dose-responsive readout)"
                                                    if positive else "FAIL (readout dead)"))
    print("")

    # ── (4) the prereg statistic — variance ratio + F test + paired permutation ──
    v_bias = _var(dd["bias"])
    print("  (4) var(ΔD_bias)/var(ΔD_cascade)  [prereg: ≤1.5 VOID-BY-SNR · >3 ∧ positive ⇒ KILL stands]")
    ratios = {}
    for arm in ("rng", "static"):
        v_ped = _var(dd[arm])
        ratio = (v_bias / v_ped) if v_ped > 0 else float("inf")
        ratios[arm] = ratio
        pF = _f_two_sided_p(ratio, n - 1, n - 1)
        rng_ = _prand.Random(rseed)
        null = []
        for _ in range(rounds):
            a, b = [], []
            for i in range(n):
                if rng_.random() < 0.5:
                    a.append(dd["bias"][i]); b.append(dd[arm][i])
                else:
                    a.append(dd[arm][i]); b.append(dd["bias"][i])
            vb = _var(b)
            null.append((_var(a) / vb) if vb > 0 else float("inf"))
        null.sort()
        lo = null[int(0.025 * rounds)]
        hi = null[int(0.975 * rounds) - 1]
        pp = sum(1 for x in null if abs(_pm.log(max(x, 1e-12))) >= abs(_pm.log(max(ratio, 1e-12)))) / float(rounds)
        tag = "PRIMARY (full cascade · dose-matched · direction-void)" if arm == "rng" \
            else "LOWER BOUND (no downstream re-roll ⇒ overstates bias SNR)"
        print("      %-7s ratio=%.3f · F(%d,%d) p=%.3f · paired-swap null95%%=[%.3f,%.3f] p=%.3f"
              % (arm, ratio, n - 1, n - 1, pF, lo, hi, pp))
        print("              %s" % tag)
    print("")

    # ── (5) MECHANISM — is D confounded by the text's own bigram diversity? ──
    # D = |bigrams(text) ∩ bigrams(seed)| / |bigrams(text)| is a SET-cardinality ratio, so its
    # DENOMINATOR is the steered text's own bigram DIVERSITY. If ΔD tracks Δ|distinct bigrams|,
    # then ΔD is partly a diversity readout that never consults the seed — which would explain a
    # non-monotone away-pole (repeated filler bytes collapse into ONE set element, shrinking the
    # denominator and RAISING D even as seed-overlap falls). This is a code fact about the H_9576
    # readout; the correlation below decides whether it actually bites at this scale.
    print("  (5) MECHANISM — D's denominator is |distinct bigrams(text)| (a SET). Does ΔD just track")
    print("      the steered text's bigram DIVERSITY, without consulting the seed?")
    for arm in ("bias", "rng"):
        dv, dl = [], []
        for sd in seeds:
            o, a_ = _rows("off", sd), _rows(arm, sd)
            for i in range(min(len(o), len(a_))):
                if not o[i].get("emit"):
                    continue
                base_b = _b64(o[i].get("gtext_b64"))
                st_b = _b64(a_[i].get("gtext_pc2_b64"))
                seed_b = _b64(o[i].get("seed_b64"))
                if not base_b or not st_b or not seed_b:
                    continue
                dv.append(_ov(base_b, seed_b) - _ov(st_b, seed_b))
                dl.append(float(len(_big(base_b)) - len(_big(st_b))))
        rr = _spearman_pub(dv, dl)
        print("      %-4s rho(ΔD, Δ|distinct bigrams|) = %+.3f   (n=%d)" % (arm, rr, len(dv)))
    print("      ⇒ a large |rho| means ΔD is contaminated by a seed-independent diversity term.")
    print("")

    # ── (6) verdict — the frozen table, primary denominator = rng ────────────
    ratio = ratios["rng"]
    print("  ⇒ prereg cell: ratio(bias/rng) = %.3f" % ratio)
    if not positive:
        v = "⛔ INVALID — the positive control cannot beat the pedestal (readout dead · a negative is unreadable)"
    elif ratio <= 1.5:
        v = ("🕳️ VOID-BY-SNR — the steered arm's ΔD variance is within 1.5× of a DIRECTION-VOID\n"
             "     dose-matched pedestal. H_9576's rho≈0 is reclassified: per-tick direction was\n"
             "     never measured, so the 'W2 wall' does NOT stand as a negative. Block-aggregation\n"
             "     (or a coarser readout) is mandatory before any direction verdict is read again.")
    elif ratio > 3.0:
        v = ("🧱 KILL STANDS (readout valid) — bias ΔD variance is >3× the cascade pedestal, so the\n"
             "     per-tick signal is not pedestal-dominated and H_9576's rho≈0 is a real negative.\n"
             "     ⚠️ PENDING the ζ=±4 saturation arm (decode-side positive control · pool spec below).")
    else:
        v = ("⏳ INDETERMINATE — ratio in (1.5, 3]: the prereg table leaves this band unassigned.\n"
             "     Not a negative and not a VOID — it is reported as PENDING, not adjudicated\n"
             "     (assigning it now would be tune-to-green).")
    print("  ⇒ VERDICT: " + v)
    print("")
    print("  SCOPE / what this run cannot do (a_scale_honest_scope · no invented numbers):")
    print("   · the card's cascade arm (forced 2nd-best byte + downstream RE-ROLL) and the ζ=±4")
    print("     saturation positive control both need a live decode; the ckpt is pool-side, so they")
    print("     are NOT in these numbers. The `static` arm is a re-roll-free LOWER BOUND and `rng`")
    print("     is the dose-matched full-cascade stand-in the traces already hold.")
    print("   · pool spec (summer/aiden · never mini · heavy-anima-eval-pool-not-mini):")
    print("       anima-py chat --pc2-mouth cascade --pc2-zeta 0   <ckpt>  # 2nd-best byte @ 1 lm-step")
    print("       anima-py chat --pc2-mouth bias    --pc2-zeta 4   <ckpt>  # ζ=+4 saturation arm")
    print("       anima-py chat --pc2-mouth bias    --pc2-zeta -4  <ckpt>  # ζ=-4 saturation arm")
    print("       (seeds 7,4302,4303 · same 150 ticks) → re-run this flag over the new traces dir.")
    return 0


# ───────────────────────────────────────────────────────────────────────────
# H_9806 — COMPRESSION-MI measurement lane (`core/mi_compress.py`).
#
# Production had NO compression-based MI estimator, so "does this stream carry information
# across a boundary" could only ever be answered through a model forward pass — which mixes a
# property of the STREAM with a property of the MODEL's reach. These two flags measure the
# stream itself: $0, stdlib-only, no ckpt, no GPU, no numpy.
#
#   anima-py evaluate --stream-mi <path> [--shuffle-floor derived|off] [--win 4096]
#                                        [--span 2048] [--out f.json] [--n-segments 30]
#   anima-py evaluate --capture-anchor <path> [--k 8] [--out f.json] [--n-segments N]
#
# <path> may be omitted, in which case the run is a pure CERTIFICATION pass (the plants only).
#
# THE CERTIFICATION IS NOT DETACHABLE. Both handlers run their positive plant AND their
# negative control BEFORE they will report a substrate number, and both refuse to print a
# verdict if the plant does not fire. A null control alone proves only that an instrument is
# not hallucinating; it never proves the instrument can see anything
# (positive-control-before-reading-a-negative). Shipping the plant as a separate script is the
# same defect one `rm` away, so it ships inside the flag.
#
# THE FLOOR IS DERIVED, NEVER ASSUMED. `--shuffle-floor derived` (the default) recomputes the
# ceiling from the SAME realized segments with adjacency deterministically broken — identical
# lengths, byte statistics and pair count, only the ORDER destroyed. `off` skips the control
# arm for a fast raw pass, and the run then REFUSES a verdict, because a raw ceiling is a value
# and the signal is collapse-Δ against a control (measurement-metalaw · p7).
# ───────────────────────────────────────────────────────────────────────────

def _mi_positional(argv, flag):
    """The token after `flag` unless it is another flag — <path> is optional here."""
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            return argv[i + 1]
    return ""


def stream_mi_run(argv):
    """`anima-py evaluate --stream-mi [<path>] [--shuffle-floor derived|off] ...` — H_9806."""
    import mi_compress as mi

    path = _mi_positional(argv, "--stream-mi")
    win = evaluate_intval(argv, "--win", mi.W_TAIL)
    span = evaluate_intval(argv, "--span", mi.P_PRED)
    nseg = evaluate_intval(argv, "--n-segments", 30)
    floor_mode = evaluate_strval(argv, "--shuffle-floor", "derived")
    out_path = evaluate_strval(argv, "--out", "stream_mi.json")
    if floor_mode not in ("derived", "off"):
        print("ERROR: --shuffle-floor takes 'derived' (default) or 'off', got %r" % floor_mode,
              file=sys.stderr)
        return 2

    print("=== anima evaluate --stream-mi — H_9806 CROSS-BOUNDARY CONDITIONAL-bpb BATTERY ===")
    print("  win %dB tail · span %dB predicted prefix · eps %.4f bpb · estimators %s"
          % (win, span, mi.EPS_BPB, ",".join(n for n, _ in mi.ESTIMATORS)))
    print("  floor: %s" % ("DERIVED from the realized split (adjacency broken, lengths kept)"
                           if floor_mode == "derived" else
                           "OFF — raw pass, no verdict will be emitted"))

    # ---- CERTIFICATION (never optional) ----------------------------------------------
    print("  [certify] running the shipped plant + null (n=%d segments each) …" % nseg)
    cert = mi.battery_liveness(nseg, win, span)
    for nm, _ in mi.ESTIMATORS:
        print("    %-8s plant over_floor %+0.4f | null over_floor %+0.4f"
              % (nm, cert["plant"][nm]["over_floor"], cert["null"][nm]["over_floor"]))
    print("    plant_fires=%s (must clear %.3f on ALL estimators) · null_refuses=%s "
          "(must clear on NONE) → certified=%s"
          % (cert["plant_fires"], 5 * mi.EPS_BPB, cert["null_refuses"], cert["certified"]))

    report = {"schema": "anima-stream-mi/v1", "path": path, "win": win, "span": span,
              "eps": mi.EPS_BPB, "shuffle_floor": floor_mode, "certification": cert}

    if not cert["certified"]:
        print("  VERDICT: ⛔ INSTRUMENT-DEAD — the battery either cannot see a planted "
              "cross-boundary signal or reports one where none exists. No reading taken with "
              "it is interpretable; do NOT read the substrate numbers below.")
        report["verdict"] = "INSTRUMENT-DEAD"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  wrote %s" % out_path)
        return 2

    if not path:
        print("  VERDICT: ✅ INSTRUMENT-CERTIFIED (certification-only pass — no stream given). "
              "This certifies the battery, and asserts NOTHING about any substrate.")
        report["verdict"] = "INSTRUMENT-CERTIFIED"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  wrote %s" % out_path)
        return 0

    segs, how = mi.segments_from_path(path, win, span)
    print("  [stream] %s · %s" % (path, how))
    if len(segs) < 3:
        print("  VERDICT: ⛔ NO-STREAM — %d usable segments. A segment must be >= win+span "
              "bytes to have a body beyond its tail; padding one would manufacture the answer."
              % len(segs))
        report["verdict"] = "NO-STREAM"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 2

    ests = mi.ESTIMATORS
    if floor_mode == "off":
        row = {"n_segments": len(segs)}
        for nm, est in ests:
            row[nm] = mi.measure_pairs(segs, est, win, span)
        report["stream"] = row
        report["verdict"] = "RAW-NO-CONTROL"
        for nm, _ in ests:
            print("    %-8s raw ceiling %+0.4f  specificity %+0.4f  base %.4f"
                  % (nm, row[nm]["ceiling_med"], row[nm]["specificity_med"],
                     row[nm]["base_bpb_med"]))
        print("  VERDICT: ⚪ RAW-NO-CONTROL — a raw ceiling is a value, not a signal. Re-run "
              "with --shuffle-floor derived to obtain a readable collapse-Δ.")
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  wrote %s" % out_path)
        return 0

    row = mi.stream_mi(segs, win, span, mi.EPS_BPB, ests)
    report["stream"] = row
    for nm, _ in ests:
        r = row[nm]
        print("    %-8s ceiling %+0.4f  floor %+0.4f  OVER_FLOOR %+0.4f  specificity %+0.4f"
              % (nm, r["ceiling"], r["shuffle_floor"], r["over_floor"], r["specificity"]))
    print("    pairs=%d · strict(all 3 > eps)=%s · order-aware(ppm+markov6)=%s (sign-agree=%s)"
          % (row[ests[0][0]]["n_pairs"], row["anchored_strict"],
             row["anchored_order_aware"], row["order_aware_agree"]))
    if row["underpowered"]:
        print("    ⚠️ UNDER-POWERED: %d pairs < %d. A null here is uninformative, not a kill."
              % (len(segs) - 1, mi.MIN_PAIRS))

    if row["anchored_strict"]:
        report["verdict"] = "ANCHORED"
        print("  VERDICT: 🟢 ANCHORED — every estimator clears the derived floor by more than "
              "eps. The stream carries segment-specific cross-boundary information beyond the "
              "%dB tail. This bounds an UNBOUNDED summary; a k-byte extract still needs its "
              "own measurement." % win)
    elif row["anchored_order_aware"]:
        report["verdict"] = "ORDER-AWARE-ONLY"
        print("  VERDICT: 🟡 ORDER-AWARE-ONLY — ppm and markov6 clear the floor but gzip does "
              "not. Expected where the carried information is a lone long-range token (gzip's "
              "32KB LZ window is blind to it), but it is a WEAKER read than strict.")
    elif row["underpowered"]:
        report["verdict"] = "UNDER-POWERED"
        print("  VERDICT: ⚪ UNDER-POWERED — no estimator clears the floor, but the stream is "
              "too thin to read that as a kill (power-before-negative-verdict).")
    else:
        report["verdict"] = "AT-FLOOR"
        print("  VERDICT: 🔴 AT-FLOOR — no estimator clears the derived floor. On this stream, "
              "at this tail reach, there is no cross-boundary information beyond what the tail "
              "already supplies. Scope: this stream, this W — not every possible stream.")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("  wrote %s" % out_path)
    return 0


def capture_anchor_run(argv):
    """`anima-py evaluate --capture-anchor [<path>] [--k 8] [--out f.json]` — H_9806.

    Feature-space shift-null LOO capture: how much of the cross-boundary predictive
    information survives a rank-k linear summary, above its own cyclic-misalignment floor,
    and does it beat a topic-matched other-segment floor per pair."""
    import mi_compress as mi

    path = _mi_positional(argv, "--capture-anchor")
    win = evaluate_intval(argv, "--win", mi.W_TAIL)
    span = evaluate_intval(argv, "--span", mi.P_PRED)
    pk = evaluate_intval(argv, "--k", mi.PRIMARY_K)
    out_path = evaluate_strval(argv, "--out", "capture_anchor.json")

    print("=== anima evaluate --capture-anchor — H_9806 SHIFT-NULL LOO CAPTURE ===")
    print("  D=%d hashed n-gram (n=1,2,3) · K-NN=%d · primary k=%d · ceiling gate rank<=%d"
          % (mi.D_FEAT, mi.KNN, pk, mi.RANK_GATE))

    segs, how = ([], "(certification-only)")
    feats = []
    if path:
        segs, how = mi.segments_from_path(path, win, span)
        print("  [stream] %s · %s" % (path, how))
        feats = [mi.hashed_ngram_features(b) for _, b in segs]
    n_live = evaluate_intval(argv, "--n-segments", len(feats) if feats else 40)

    # ---- CERTIFICATION at MATCHED n (never optional) ----------------------------------
    print("  [certify] three-arm liveness at matched n=%d (HIGH must fire · FAIL must "
          "refuse · LOW must stay <= %.2f) …" % (n_live, mi.LOW_CAP_MAX))
    cert = mi.capture_liveness(n_live, pk)
    hi, lo, fa = cert["high"], cert["low"], cert["fail"]
    print("    HIGH (plant_weak)     gate=%s capture(%s)=%s → %s"
          % (hi.get("gate_ok"), hi.get("primary_k"),
             _fmt_opt(hi.get("capture_primary")), "PASS" if cert["high_ok"] else "FAIL"))
    print("    LOW  (buried delay)   full_rank=%s capture(k<=8)=%s → %s%s"
          % (lo.get("full", {}).get("rank"),
             {k: _fmt_opt(v) for k, v in (lo.get("capture") or {}).items()},
             "PASS" if cert["low_ok"] else "MISS",
             "" if cert["low_is_gating"] else "  (INFORMATIONAL at n<%d)" % mi.LOW_CERT_N))
    print("    FAIL (iid noise)      gate=%s → %s"
          % (fa.get("gate_ok"), "PASS" if cert["fail_ok"] else "FAIL"))
    print("    certified=%s · grade=%s" % (cert["certified"], cert["grade"]))

    report = {"schema": "anima-capture-anchor/v1", "path": path, "primary_k": pk,
              "n_liveness": n_live, "certification": cert}

    if not cert["certified"]:
        print("  VERDICT: ⛔ INSTRUMENT-DEAD — the capture rig failed its own liveness arms. "
              "Any capture number it produces is void (an instrument that reads 1.0 on noise "
              "or 0 on a planted ceiling is measuring itself).")
        report["verdict"] = "INSTRUMENT-DEAD"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  wrote %s" % out_path)
        return 2

    if not feats:
        print("  VERDICT: ✅ INSTRUMENT-CERTIFIED (certification-only pass — no stream given).")
        report["verdict"] = "INSTRUMENT-CERTIFIED"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  wrote %s" % out_path)
        return 0

    res = mi.shift_null_loo_capture(feats, pk)
    report["stream"] = res
    if "error" in res:
        print("  VERDICT: ⛔ NO-VALID-K — %s" % res["error"])
        report["verdict"] = "NO-VALID-K"
        json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 2

    print("    pairs=%d shifts=%d numrank=%d valid_k=%s"
          % (res["n_pairs"], res["n_shifts"], res["numrank"], res["valid_ks"]))
    print("    ceiling arm: align=%+0.6f rank=%d/%d (gate rank<=%d → %s)"
          % (res["full"]["align"], res["full"]["rank"], res["n_shifts"],
             mi.RANK_GATE, res["gate_ok"]))
    print("    capture: %s" % {k: _fmt_opt(v) for k, v in res["capture"].items()})
    print("    topic floor: capture %s vs topic %s → margin %s (eps_f %.3f)"
          % (_fmt_opt(res["capture_primary"]), _fmt_opt(res["topic_capture_primary"]),
             _fmt_opt(res["capture_margin"]), mi.EPS_FRAC))
    print("    per-pair sign(err_topic > err_s) = %d/%d · DERIVED bar %d "
          "(exact binomial, alpha=%.2f, realized n) → %s"
          % (res["sign_topic_gt_s"], res["n_pairs"], res["sign_needed"],
             res["sign_alpha"], res["sign_ok"]))

    marg = res["capture_margin"]
    if not res["gate_ok"]:
        report["verdict"] = "NO-FEATURE-CEILING"
        print("  VERDICT: ⚪ NO-FEATURE-CEILING — the hashed n-gram basis carries no resolvable "
              "cross-boundary signal on this stream, so capture is unmeasurable here. This "
              "refutes the INSTRUMENT's power on this substrate, not the substrate.")
    elif (res["capture_primary"] or 0.0) < mi.CAPTURE_ANCHOR:
        report["verdict"] = "CAPTURE-REFUSED"
        print("  VERDICT: 🔴 CAPTURE-REFUSED — the rank-%d code retains less than the %.2f "
              "anchor of a live ceiling. A hindsight projection bounds a learned code of the "
              "same rank, so this bounds the learned case too." % (pk, mi.CAPTURE_ANCHOR))
    elif marg is None or marg <= mi.EPS_FRAC or not res["sign_ok"]:
        report["verdict"] = "TOPIC-DECORATION"
        print("  VERDICT: 🔴 TOPIC-DECORATION — the code clears the ceiling anchor but does not "
              "beat a topic-matched OTHER segment per pair. It is carrying topic identity, not "
              "a segment-specific self. The aggregate margin is not the test; the per-pair sign "
              "count is, and its bar was derived from the realized %d pairs." % res["n_pairs"])
    elif not res["monotonic_ok"]:
        report["verdict"] = "PENDING-INSTRUMENT"
        print("  VERDICT: 🟡 PENDING(instrument) — capture is non-monotonic in k, which is a "
              "projection artifact signature. Do not read the magnitude.")
    else:
        report["verdict"] = "ANCHORED"
        print("  VERDICT: 🟢 ANCHORED — a rank-%d continuous summary retains the ceiling AND "
              "beats the topic floor per pair (grade %s). Hindsight ≥ learned, so this is a "
              "CEILING on a learned code, never a demonstration of one." % (pk, cert["grade"]))
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("  wrote %s" % out_path)
    return 0


def _fmt_opt(v):
    return "n/a" if v is None else "%.4f" % v


def _reject_unknown_flags(argv):
    """Return an error string for the first unknown --flag in argv, else ''."""
    for a in argv:
        if not a.startswith("--") or a in _KNOWN_FLAGS:
            continue
        near = [k for k in sorted(_KNOWN_FLAGS)
                if k.lstrip("-").startswith(a.lstrip("-").split("-")[0])]
        msg = "evaluate: unknown flag " + a
        if near:
            msg += "  (did you mean: " + " ".join(near) + " ?)"
        return msg + "\n  known flags: " + " ".join(sorted(_KNOWN_FLAGS)) + \
            "\n  (an unknown flag is rejected, not ignored — a silently-dropped --out " \
            "loses the whole run's result with a green exit code)"
    return ""


# ───────────────────────────────────────────────────────────────────────────
# L4 — BRIDGE-TRACE path-attribution census (RUNTIME-BRIDGE campaign · H_9388).
#
# The frontier converged to "the operator does not runtime-look-up the declaration store
# (TWO-LANE, no bridge)". W_wt = the weight-stored declaration synthesised by the operator.
# In flip1 `{s}지 않다 => ` (KO BOUND suffix) or `not {s} => ` (EN FREE word) the stem bytes
# are ALREADY inside the operator's receptive field, so the circuit the wall needs
# (stem→polarity-feature→transport→sign-flip) is all conv parts. The wipeout so far is
# indistinguishable from "the cache was always cheaper and no stem-key store was ever built".
# This census decomposes the flip1 answer-byte MARGIN into how much comes from the stem
# position vs the operator (slot) position.
#
# METHOD — INPUT-BYTE GRADED OCCLUSION, not hidden-swap (H_9331's swap-patch died on a binary
# readout scramble floor). We never touch the trunk; we replace a byte SPAN of the prompt with
# an equal-BYTE-LENGTH neutral fill (0x20 space) so the T-window right-alignment is preserved
# exactly (decode._seed_to_tok aligns by BYTES; a 1B-for-3B swap would shift everything). The
# contribution of a region = how much the 2AFC margin drops when that region is occluded.
#
#   margin = NLL(counterfactual) - NLL(gold)          (>0 ⟺ the model prefers the correct answer)
#   stem_contrib = margin_full - margin(stem occluded)
#   slot_contrib = margin_full - margin(operator occluded)
#   ctrl_contrib = margin_full - margin(matched-byte-count slice of the FIXED template head occluded)
#   stem_net     = stem_contrib - ctrl_contrib        (control-corrected — probe-defect-census:
#                                                       never read a raw contribution; the matched-length
#                                                       neutral occlusion is the paired same-class control)
#
# POSITIVE-CONTROL GATE (flip0, where the declarative lookup demonstrably works): the flip0 answer
# is the stem-keyed fact itself, so stem_net MUST dominate there. If flip0 stem-share <= θ or the
# paired sign-flip permutation p is not significant, the INSTRUMENT is broken → discard, do not read
# flip1. Sequential: read flip0 first (gate), then the flip1 tiers.
#
# Device-stamped (GPU-hidden byte-pin lesson): the probe reads hidden→logits; a CUDA upgrade moves
# the low bits. We stamp GPU/CPU into every output; a census meant to run $0 on aiden CPU stamps CPU.
# The guard can fail loudly (device mismatch is refused, not silently compared).
# ───────────────────────────────────────────────────────────────────────────
def _bt_margin(np, W, seed, gold, cf, T):
    """2AFC margin = NLL(counterfactual) - NLL(gold) for a (possibly occluded) seed.
    >0 ⟺ the model assigns the gold answer lower NLL (prefers it)."""
    n_g = _xbind_cont_nll(np, clm, W, seed, gold, T)
    n_c = _xbind_cont_nll(np, clm, W, seed, cf, T)
    return n_c - n_g


def _bt_occlude(seed_b, lo, hi):
    """Replace seed bytes [lo,hi) with 0x20 (space) — equal byte length, so the right-aligned
    T-window does not shift. Returns the occluded seed as a surrogateescape str."""
    out = bytearray(seed_b)
    for i in range(lo, hi):
        out[i] = 0x20
    return bytes(out).decode('utf-8', 'surrogateescape')


def _bt_common_head(seeds):
    """Byte length of the common template head shared by every scored seed
    (`이 영화 ` / `this movie is `). This is the NEUTRAL region — the matched-length
    control occlusion is taken from here, and every byte AFTER it up to ` => ` that is not
    the stem is the OPERATOR/slot (works for a BOUND post-stem suffix AND a FREE pre-posed
    word). Falls back to 0 (empty head) if the seeds share no prefix."""
    if not seeds:
        return 0
    pref = seeds[0]
    for s in seeds[1:]:
        i = 0
        m = min(len(pref), len(s))
        while i < m and pref[i] == s[i]:
            i += 1
        pref = pref[:i]
        if not pref:
            return 0
    return len(pref.encode('utf-8', 'surrogateescape'))


def _bt_spans(seed, stem, head_b):
    """Byte offsets in seed.encode() for the (stem, slot, control) partition.
    Layout: <FIXED TEMPLATE HEAD (head_b)><…operator…><stem><…operator…> => .
      control = the first `len(stem)` bytes of the fixed head (neutral, matched byte count).
      stem    = the located stem substring (first occurrence at/after head_b).
      slot    = every byte in [head_b, arrow) that is NOT the stem — the operator morphemes
                (지 않다 / not / 안 / 별로 …), whether pre- or post-posed relative to the stem.
    Returns None if the stem cannot be located (item skipped, counted)."""
    sb = seed.encode('utf-8', 'surrogateescape')
    arrow = seed.rfind(" => ")
    if arrow < 0:
        arrow = len(seed)
    arrow_b = len(seed[:arrow].encode('utf-8', 'surrogateescape'))
    ci = seed.find(stem)
    if ci < 0:
        return None
    stem_lo = len(seed[:ci].encode('utf-8', 'surrogateescape'))
    stem_b = len(stem.encode('utf-8', 'surrogateescape'))
    stem_hi = stem_lo + stem_b
    return sb, stem_lo, stem_hi, head_b, arrow_b


def bridge_trace_run(argv):
    """`anima-py evaluate <ckpt> --bridge-trace <flip1.json> --flip0 <flip0.json> --out <f.json>`

    L4 path-attribution census. Decomposes the flip1 answer-byte margin into stem-position vs
    operator(slot)-position contributions by equal-byte-length input occlusion, control-corrected
    with a matched-length neutral-head occlusion, with a paired sign-flip permutation p. The flip0
    manifest is the POSITIVE CONTROL: stem_net must dominate there or the instrument is discarded.
    Read-only w.r.t. weights (production forward). Device-stamped."""
    import numpy as np
    import time
    ckpt = argv[0]
    f1_path = evaluate_strval(argv[1:], "--bridge-trace", "")
    f0_path = evaluate_strval(argv[1:], "--flip0", "")
    out_path = evaluate_strval(argv[1:], "--out", "bridge_trace.json")
    n_perm = evaluate_intval(argv[1:], "--perm", 2000)
    seed_rng = evaluate_intval(argv[1:], "--seed", 7)
    theta = float(evaluate_strval(argv[1:], "--theta", "0.5"))
    dev = "GPU" if clm.cuda_available() else "CPU"

    f1 = json.load(open(f1_path))
    T = evaluate_intval(argv[1:], "--win", int(f1.get("win", 64)))
    print("=== anima evaluate --bridge-trace — L4 path-attribution census (H_9388) ===")
    print("ckpt: %s  device=%s  win=%d  perm=%d  theta=%.2f" % (ckpt, dev, T, n_perm, theta))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    def score_manifest(spec):
        rows, skipped = [], 0
        all_seeds = [it["seed"] for split in ("heldout", "seen") for it in spec.get(split, [])]
        head_b = _bt_common_head(all_seeds)
        for split in ("heldout", "seen"):
            for it in spec.get(split, []):
                seed = it["seed"]
                stem = it.get("stem") or it.get("a")
                gold = it["gold"]; cf = it["counterfactual"]
                sp = _bt_spans(seed, stem, head_b)
                if sp is None:
                    skipped += 1
                    continue
                sb, stem_lo, stem_hi, head_len, arrow_b = sp
                stem_b = stem_hi - stem_lo
                m_full = _bt_margin(np, W, seed, gold, cf, T)
                m_stem = _bt_margin(np, W, _bt_occlude(sb, stem_lo, stem_hi), gold, cf, T)
                slot_occ = bytearray(sb)
                for i in range(head_len, arrow_b):
                    if not (stem_lo <= i < stem_hi):
                        slot_occ[i] = 0x20
                m_slot = _bt_margin(np, W, bytes(slot_occ).decode('utf-8', 'surrogateescape'),
                                    gold, cf, T)
                cctrl_hi = min(stem_b, head_len)
                m_ctrl = _bt_margin(np, W, _bt_occlude(sb, 0, cctrl_hi), gold, cf, T)
                rows.append({
                    "arm": (it.get("b", "").split("|")[0] or "?"),
                    "split": split, "stem": stem, "pol": it.get("pol"),
                    "margin_full": m_full, "margin_stem_occ": m_stem,
                    "margin_slot_occ": m_slot, "margin_ctrl_occ": m_ctrl,
                    "stem_contrib": m_full - m_stem, "slot_contrib": m_full - m_slot,
                    "ctrl_contrib": m_full - m_ctrl,
                    "stem_net": m_ctrl - m_stem,   # (m_full-m_stem) - (m_full-m_ctrl)
                })
        return rows, skipped

    def summarize(rows, label):
        if not rows:
            return {"label": label, "n": 0}
        sn = np.array([r["stem_net"] for r in rows])
        sc = np.array([r["slot_contrib"] for r in rows])
        stc = np.array([r["stem_contrib"] for r in rows])
        ctc = np.array([r["ctrl_contrib"] for r in rows])
        mean_sn = float(sn.mean()); mean_slot = float(sc.mean())
        denom = abs(mean_sn) + abs(mean_slot)
        stem_share = float(mean_sn / denom) if denom > 1e-12 else 0.0
        rng = np.random.RandomState(seed_rng)
        obs = float(sn.mean())
        ge = 0
        for _ in range(n_perm):
            signs = rng.choice([-1.0, 1.0], size=len(sn))
            if abs(float((sn * signs).mean())) >= abs(obs) - 1e-12:
                ge += 1
        p_perm = (ge + 1) / (n_perm + 1)
        return {"label": label, "n": len(rows),
                "mean_stem_contrib": float(stc.mean()), "mean_ctrl_contrib": float(ctc.mean()),
                "mean_stem_net": mean_sn,
                "sd_stem_net": float(sn.std(ddof=1)) if len(sn) > 1 else 0.0,
                "mean_slot_contrib": mean_slot, "stem_share": stem_share, "perm_p": p_perm}

    t0 = time.time()
    r1, sk1 = score_manifest(f1)
    result = {"ckpt": ckpt, "device": dev, "win": T, "perm": n_perm, "theta": theta,
              "flip1_skipped": sk1, "flip1": {}, "flip0": {}}
    arms1 = sorted(set(r["arm"] for r in r1))
    result["flip1"]["overall"] = summarize(r1, "flip1/overall")
    for a in arms1:
        result["flip1"][a] = summarize([r for r in r1 if r["arm"] == a], "flip1/" + a)
    for sp in ("heldout", "seen"):
        result["flip1"]["split_" + sp] = summarize([r for r in r1 if r["split"] == sp],
                                                    "flip1/" + sp)

    gate = {"ran": False}
    if f0_path:
        f0 = json.load(open(f0_path))
        r0, sk0 = score_manifest(f0)
        result["flip0_skipped"] = sk0
        result["flip0"]["overall"] = summarize(r0, "flip0/overall")
        for sp in ("heldout", "seen"):
            result["flip0"]["split_" + sp] = summarize([r for r in r0 if r["split"] == sp],
                                                        "flip0/" + sp)
        ov = result["flip0"]["overall"]
        gate = {"ran": True, "stem_share": ov.get("stem_share", 0.0),
                "mean_stem_net": ov.get("mean_stem_net", 0.0), "perm_p": ov.get("perm_p", 1.0),
                "pass": bool(ov.get("stem_share", 0.0) > theta and ov.get("mean_stem_net", 0.0) > 0
                             and ov.get("perm_p", 1.0) < 0.05)}
    result["positive_control_gate"] = gate
    result["rows_flip1"] = r1
    result["wall_sec"] = time.time() - t0

    json.dump(result, open(out_path, "w"), ensure_ascii=False, indent=1)

    print("--- POSITIVE-CONTROL GATE (flip0) ---")
    if gate["ran"]:
        print("  flip0 stem_share=%.3f  mean_stem_net=%+.4f  perm_p=%.4f  ->  %s"
              % (gate["stem_share"], gate["mean_stem_net"], gate["perm_p"],
                 "PASS (instrument valid)" if gate["pass"]
                 else "FAIL (instrument broken → flip1 undecidable)"))
    else:
        print("  no --flip0 manifest given — gate NOT run (flip1 read is uncalibrated)")
    print("--- FLIP1 path attribution (device=%s) ---" % dev)
    for k in ["overall"] + arms1 + ["split_heldout", "split_seen"]:
        s = result["flip1"].get(k, {})
        if s.get("n"):
            print("  %-16s n=%3d  stem_net=%+.4f (sd %.4f)  slot_contrib=%+.4f  stem_share=%.3f  perm_p=%.4f"
                  % (k, s["n"], s["mean_stem_net"], s["sd_stem_net"], s["mean_slot_contrib"],
                     s["stem_share"], s["perm_p"]))
    print("wrote %s  (%.1fs, %s)" % (out_path, result["wall_sec"], dev))
    return 0


def faction_phi_proxy_run(argv):
    """`anima-py evaluate <ckpt> --faction-phi-proxy <prompts.json> [--n-factions-sweep 1,2,4,8,12,16,24,32,64]
    [--win 24] [--trials 200] [--seed 12345] [--out faction_phi.json]` — the ARCHIVED faction
    Phi proxy, recomputed on engine-native trunk activations, against a zero-truth PEDESTAL
    (cards H_9660 / H_9654 / H_9655 · faction-lateral-axis-r3).

    The archived engine scored consciousness with
        phi = (global_var - mean_faction_var) * log2(n_active)
    (verbatim from core/phi/quantum_consciousness.hexa:252, a TODO[pytorch] comment whose py
    implementation never existed). Total variance decomposition says
        Var = E[Var|g] + Var(E[X|g]),
    so `global_var - mean_faction_var` IS the between-group term: raising K mechanically
    shrinks the within term and inflates the proxy. At K=N (one cell per faction) within=0 and
    the proxy saturates at global_var. That is division, not integration — the archived
    "Law 22" (structure-only Phi 2.1x) and "Law 44" (sigma(6)=12 optimal) are confounded by it.

    Arms (each K, all three, same trunk activations · a_break_the_wall needs >=2 controls):
      real      — the production trunk penultimate yn:[T,d], partitioned over the d units.
      pedestal  — i.i.d. gaussian matched to real's per-arm mean/std. TRUTH Phi = 0 (there is
                  nothing integrated; the partition is an arbitrary label). Any rise here is
                  pure artifact (`phi-estimator-needs-zero-truth-pedestal`).
      scramble  — real values, unit axis permuted per position: destroys any cross-unit
                  structure while preserving every marginal.

    Reads (pre-registered, NOT swept): the K grid, trials, seed. The verdict is the SHAPE of
    proxy(K) and real-vs-pedestal SEPARATION, never a raw value (FORM tunable · BIND earned · p7):
      - real tracks pedestal (ratio ~1, monotone, no peak) => proxy measures the partition,
        not the substrate => archived Laws 22/43/44 stay UNDECIDABLE (confound un-removed).
      - real separates from pedestal AND peaks at finite K => the axis survives its first gate
        and H_9654's "optimum was never measured" becomes falsifiable at that K.
    DIRECTIONAL by construction: this scores an ARCHIVED DEAD FORMULA on live activations. It
    is NOT a consciousness verdict and never cements one (a_phi_iit4_tool: real Phi is faithful
    IIT4 only; this proxy is the object under indictment, not a measuring tool)."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--faction-phi-proxy", "")
    out_path = evaluate_strval(argv[1:], "--out", "")
    T = evaluate_intval(argv[1:], "--win", 24)
    trials = evaluate_intval(argv[1:], "--trials", 200)
    seed = evaluate_intval(argv[1:], "--seed", 12345)
    ks_s = evaluate_strval(argv[1:], "--n-factions-sweep", "1,2,4,8,12,16,24,32,64")
    ks = [int(x) for x in ks_s.split(",") if x.strip()]

    print("=== anima evaluate --faction-phi-proxy — archived faction Phi on live trunk (H_9660/H_9654) ===")
    print("ckpt:  " + ckpt)
    print("proxy: (global_var - mean_faction_var) * log2(n_active)   [core/phi/quantum_consciousness.hexa:252]")
    print("       == the BETWEEN-GROUP term of Var = E[Var|g] + Var(E[X|g]) — monotone in K by construction")
    print("arms:  real | pedestal (truth Phi=0) | scramble (marginals kept, structure cut)")
    print("K:     %s  ·  trials=%d  seed=%d  (pre-registered, not swept)" % (ks, trials, seed))

    spec = json.load(open(spec_path))
    items = spec["items"] if "items" in spec else spec.get("prompts", [])
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    d = int(W["d"])
    print("d:     %d hidden units  ·  %d prompts x T=%d  (production trunk forward)" % (d, len(items), T))

    # engine-native tap: the EXACT production trunk forward (byte-identical to gate decode)
    rows = []
    for it in items:
        tok = clm._seed_to_tok(it["prompt"], T)
        yn = clm.clm_forward_hidden(W, tok, T)          # [T, d]
        rows.append(np.asarray(yn, dtype=np.float64))
    X = np.concatenate(rows, axis=0)                     # [N, d]  N = prompts*T
    N = X.shape[0]
    print("tap:   X=[%d, %d]  (N = prompts x T rows over the d unit axis)" % (N, d))

    def proxy(vals, assign, K):
        """Archived formula, verbatim. vals:[d] one row; assign:[d] faction id per unit."""
        gv = float(np.var(vals))
        fv = [float(np.var(vals[assign == f])) for f in range(K) if (assign == f).sum() > 0]
        n_active = int((np.abs(vals) > 1e-12).sum())
        return (gv - float(np.mean(fv))) * math.log2(max(n_active, 2))

    rng = np.random.default_rng(seed)
    mu, sd = float(X.mean()), float(X.std())
    out = {"ckpt": ckpt, "d": d, "N": N, "T": T, "trials": trials, "seed": seed,
           "formula": "(global_var - mean_faction_var) * log2(n_active)",
           "source": "core/phi/quantum_consciousness.hexa:252 (TODO[pytorch] · py impl never existed)",
           "rows": []}
    print("")
    print("%10s | %12s | %12s | %12s | %10s" % ("n_factions", "real", "pedestal", "scramble", "real/ped"))
    print("-" * 70)
    for K in ks:
        r_v, p_v, s_v = [], [], []
        for _ in range(trials):
            i = int(rng.integers(0, N))
            assign = rng.integers(0, K, d)               # arbitrary labels — the point
            row = X[i]
            r_v.append(proxy(row, assign, K))
            p_v.append(proxy(rng.normal(mu, sd, d), assign, K))          # TRUTH = 0
            s_v.append(proxy(rng.permutation(row), assign, K))           # marginals kept
        rm, pm, sm = float(np.mean(r_v)), float(np.mean(p_v)), float(np.mean(s_v))
        ratio = (rm / pm) if abs(pm) > 1e-12 else float("nan")
        print("%10d | %12.6f | %12.6f | %12.6f | %10s" %
              (K, rm, pm, sm, ("%.3f" % ratio) if ratio == ratio else "—"))
        out["rows"].append({"K": K, "real": rm, "real_sd": float(np.std(r_v)),
                            "pedestal": pm, "pedestal_sd": float(np.std(p_v)),
                            "scramble": sm, "scramble_sd": float(np.std(s_v)),
                            "real_over_pedestal": ratio})

    # ---- read the SHAPE, never a raw value (p7 · FORM tunable / BIND earned) --------------
    reals = [r["real"] for r in out["rows"]]
    peds = [r["pedestal"] for r in out["rows"]]
    mono_r = all(reals[i] <= reals[i + 1] + 1e-12 for i in range(len(reals) - 1))
    mono_p = all(peds[i] <= peds[i + 1] + 1e-12 for i in range(len(peds) - 1))
    kpeak = ks[int(np.argmax(reals))]
    peaked = kpeak != ks[-1]
    out["monotone_real"], out["monotone_pedestal"] = mono_r, mono_p
    out["argmax_K"], out["peaked"] = kpeak, peaked
    print("")
    print("  real     monotone in K : %s" % mono_r)
    print("  pedestal monotone in K : %s   (truth Phi=0 — any rise is the artifact)" % mono_p)
    print("  argmax_K(real)         : %d%s" % (kpeak, "" if peaked else "  (= grid edge — NO interior peak)"))
    if mono_p and not peaked:
        print("")
        print("  VERDICT (H_9660): proxy rises with K on ZERO-TRUTH data and real shows no interior")
        print("    peak => the archived proxy scores the PARTITION, not the substrate. Laws 22/43/44")
        print("    stay UNDECIDABLE (confound un-removed) — NOT refuted. DIRECTIONAL: an archived dead")
        print("    formula on live activations, never a consciousness verdict (a_phi_iit4_tool).")
    elif peaked:
        print("")
        print("  VERDICT (H_9654): real peaks at K=%d, interior to the grid. The archived 'optimum'")
        print("    claim becomes falsifiable HERE — but only if real separates from pedestal at that K")
        print("    (read real/ped, not the raw value · p7). Archive never measured K>12 (0 records)." % kpeak)
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)
        print("")
        print("  wrote: " + out_path)
    return 0


def faction_block_structure_run(argv):
    """`anima-py evaluate <ckpt> --faction-block-structure <prompts.json> [--n-factions-sweep 2,4,8,12,16]
    [--win 24] [--seed 12345] [--out blocks.json]` — does the trunk's unit axis carry faction-like
    MODULAR BLOCK structure at all (card H_9674 · faction-lateral-axis-r3)?

    Why this gate exists. The archived faction laws died as CIRCULAR (H_9673: intra-faction sync
    writes the proxy's own negative term every step) and the partition arithmetic is monotone on
    zero-truth data (H_9660). What survives is a DIFFERENT question: the old factions were fake,
    but is the STRUCTURE learnable on this substrate (H_9643, GPU)? That fire is only justified if
    the substrate has block structure to find. This measures the precondition for $0.

    Method (engine-native · production trunk forward, byte-identical to gate decode):
      X:[N,d] penultimate over the prompt set -> unit-by-unit correlation |C|:[d,d] -> greedy
      modularity clustering into K blocks -> Newman modularity Q of the best partition found.
    Arms (a_break_the_wall needs >=2 controls):
      real      — the trunk's own correlation structure.
      pedestal  — i.i.d. gaussian matched to real's mean/std: TRUTH Q = 0 (no blocks exist).
                  Finite-d correlation noise still yields Q>0, which is exactly why the pedestal
                  is mandatory (`phi-estimator-needs-zero-truth-pedestal`) — Q is NOT read raw.
      scramble  — real values, per-unit independent row permutation: kills cross-unit coupling,
                  keeps every marginal.
    POSITIVE CONTROL FIRST (`positive-control-before-reading-a-negative`): the sample correlation
    over N rows has rank <= min(N,d); at N << d both real and pedestal are noise-dominated and their
    agreement would mean "no power", not "no blocks". So the probe first plants K blocks and must
    recover them at this very N/d (bar: x1.5 over its own pedestal). If it cannot, the run emits
    NO verdict and exits non-zero — an unreadable negative is not a negative.

    Verdict is real-vs-pedestal SEPARATION, never raw Q (p7 · FORM tunable / BIND earned):
      real ~ pedestal  => no faction-like blocks in the substrate => H_9643 has nothing to learn
                          => the axis closes at $0 and the GPU fire is NOT justified.
      real >> pedestal => blocks exist => H_9643 becomes a real question and the fire is earned.
    DIRECTIONAL: correlation-modularity is one lens on 'module', not a proof of their absence
    (a_break_the_wall: a ceiling needs >=2-3 lenses)."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--faction-block-structure", "")
    out_path = evaluate_strval(argv[1:], "--out", "")
    T = evaluate_intval(argv[1:], "--win", 24)
    seed = evaluate_intval(argv[1:], "--seed", 12345)
    ks = [int(x) for x in evaluate_strval(argv[1:], "--n-factions-sweep", "2,4,8,12,16").split(",") if x.strip()]

    print("=== anima evaluate --faction-block-structure — does the substrate HAVE blocks? (H_9674) ===")
    print("ckpt:  " + ckpt)
    print("why:   old factions died CIRCULAR (H_9673) — this asks if the STRUCTURE is learnable at all.")
    print("       No blocks in the substrate => H_9643 (learn factions, GPU) has nothing to learn.")
    print("arms:  real | pedestal (truth Q=0) | scramble   ·   read SEPARATION, never raw Q (p7)")

    spec = json.load(open(spec_path))
    items = spec["items"] if "items" in spec else spec.get("prompts", [])
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    rows = []
    for it in items:
        yn = clm.clm_forward_hidden(W, clm._seed_to_tok(it["prompt"], T), T)
        rows.append(np.asarray(yn, dtype=np.float64))
    X = np.concatenate(rows, axis=0)                       # [N, d]
    N, d = X.shape
    print("tap:   X=[%d, %d]  (production trunk penultimate · %d prompts x T=%d)" % (N, d, len(items), T))

    rng = np.random.default_rng(seed)

    def modularity(A, assign, K):
        """Newman Q on the |correlation| graph for a given block assignment (vectorized)."""
        m2 = A.sum()
        if m2 <= 0: return 0.0
        n = A.shape[0]
        H = np.zeros((n, K)); H[np.arange(n), assign] = 1.0
        k = A.sum(axis=1)
        intra = float(((A @ H) * H).sum())                # sum of within-block edge weights (1 BLAS matmul)
        kf = k @ H                                        # [K] degree mass per block
        return float(intra / m2 - float((kf / m2) @ (kf / m2)))

    _graph_cache = {}

    def _graph(M, tag):
        """|corr| graph + its eigenbasis, computed ONCE per arm (eigh on d=3784 is O(d^3) — doing
        it per (arm, K) cell made the probe unrunnable). Cached by arm tag, never across arms."""
        if tag in _graph_cache:
            return _graph_cache[tag]
        C = np.abs(np.corrcoef(M, rowvar=False))
        C = np.nan_to_num(C, nan=0.0)
        np.fill_diagonal(C, 0.0)
        try:
            _w, V = np.linalg.eigh(C)
        except Exception:
            V = None
        _graph_cache[tag] = (C, V)
        return _graph_cache[tag]

    def best_blocks(M, K, tag, sweeps=6):
        """|corr| graph -> spectral seed + full sweeps to modularity.

        The first cut used 40 random single-unit moves over d=3784 and could not recover blocks it
        had PLANTED (positive control x0.76 < bar 1.5) — the SEARCH, not the substrate, was the
        binding constraint, and a negative read off it would have been an instrument fact. Fixed:
        seed from the leading eigenvectors (spectral), then sweep EVERY unit to its best block
        until no gain. Identical budget for every arm — an arm handed more search would win on
        search, not on structure. Self-check at d=200: planted x28.89 over its pedestal."""
        C, V = _graph(M, tag)
        n = C.shape[0]
        if V is not None:
            E = V[:, -K:] if K <= n else V
            cent = E[rng.choice(n, K, replace=False)]
            assign = np.zeros(n, dtype=int)
            for _ in range(12):
                dist = ((E[:, None, :] - cent[None, :, :]) ** 2).sum(-1)
                assign = dist.argmin(1)
                for f in range(K):
                    if (assign == f).any(): cent[f] = E[assign == f].mean(0)
        else:
            assign = rng.integers(0, K, n)
        # full sweeps, VECTORIZED: one-hot H:[n,K] -> affinity = C @ H is a single BLAS call.
        # (The per-unit python loop over K slices was the bottleneck — 3784 units x K x O(d) per
        # sweep never finished. Same math, one matmul.)
        deg = C.sum(1); m2 = C.sum()
        for _ in range(sweeps):
            H = np.zeros((n, K)); H[np.arange(n), assign] = 1.0
            aff = C @ H                                   # [n, K] — sum of edges u->block f
            pen = np.outer(deg, deg @ H) / m2             # [n, K] — null-model expectation
            new_assign = np.argmax(aff - pen, axis=1)
            if (new_assign == assign).all(): break
            assign = new_assign
        return modularity(C, assign, K)

    # ---- POWER GATE (`power-before-negative-verdict` · `positive-control-before-reading-a-negative`)
    # The unit-by-unit correlation over N rows has rank <= min(N,d). At N << d the sample |C| is
    # mostly finite-sample noise and BOTH real and pedestal are noise-dominated: their agreement
    # would be an INSTRUMENT fact ("no power"), not a substrate fact ("no blocks"). So the
    # instrument must first recover blocks it is GIVEN, at this very N and d, or the negative is
    # unreadable and this run refuses to emit one.
    print("power: N=%d rows vs d=%d units — sample |C| rank <= %d (%.0f%% of the %dx%d matrix is"
          % (N, d, min(N, d), 100.0 * (1.0 - min(N, d) / float(d)), d, d))
    print("       finite-sample noise). A positive control decides whether a negative is readable.")
    P = rng.normal(float(X.mean()), float(X.std()), (N, d))          # pedestal: TRUTH Q = 0

    # --arm-random-init: SAME architecture, SAME production forward, weights re-drawn from their
    # own per-tensor moments. Asks the question H_9672 T2 raised upstream of H_9674's blocks — does
    # TRAINING make them, or the architecture alone? The i.i.d. pedestal cannot answer that (it has
    # no conv/GN at all); this arm keeps every architectural fact and deletes only what was learned.
    #   random-init has blocks too  => blocks are ARCHITECTURAL, not learned => no faction substrate.
    #   random-init flat, real has  => blocks are LEARNED (H_9643 keeps its case); WHICH learning
    #     (EN pretraining vs the task) still needs H_9672 T2's scratch arm, which was not preserved.
    R = None
    if "--arm-random-init" in argv:
        rr = np.random.default_rng(seed + 1)
        Wr = dict(W)
        for k, v in list(Wr.items()):
            if isinstance(v, np.ndarray) and v.dtype.kind == "f" and v.size > 1:
                Wr[k] = rr.normal(float(v.mean()), float(v.std()) or 1e-3, v.shape).astype(v.dtype)
        R = np.concatenate([np.asarray(clm.clm_forward_hidden(Wr, clm._seed_to_tok(it["prompt"], T), T),
                                       dtype=np.float64) for it in items], axis=0)
        print("arm:   +random-init (same architecture + same forward · weights re-drawn from their")
        print("       own per-tensor moments) — isolates architecture from what was learned.")
        # DEGENERACY GATE. Random weights through a deep conv drive every unit onto one common
        # mode: measured |corr| mean 0.617 (real: 0.111), top eigenvalue 2840 of 7638 total mass,
        # per-unit std 0.0035 against a global std of 1.02 — the units barely move on their own
        # and swing together. The clusterer then collapses to the same trivial split for EVERY K
        # and Q comes out IDENTICAL to 10 decimals (0.0419274192 at K=4, 8 and 12). That constant
        # is a property of a degenerate graph, not evidence that the architecture makes blocks —
        # reading it as such would have "shown" architecture contributing 6.6x over the pedestal.
        # So the arm self-checks and refuses to report a number it cannot mean.
        Cri = np.abs(np.corrcoef(R, rowvar=False)); Cri = np.nan_to_num(Cri, nan=0.0)
        np.fill_diagonal(Cri, 0.0)
        ri_cmean = float(Cri.mean())
        x_cmean = float(np.nan_to_num(np.abs(np.corrcoef(X, rowvar=False)), nan=0.0).mean())
        if ri_cmean > 3.0 * x_cmean:
            print("       ⛔ random-init arm DEGENERATE — |corr| mean %.4f vs real %.4f (>3x): random"
                  % (ri_cmean, x_cmean))
            print("          weights put every unit on one common mode, so the clusterer collapses to")
            print("          the same split at every K and Q is a constant of the degenerate graph, not")
            print("          an architecture fact. Arm DROPPED from the read (a number it cannot mean).")
            R = None
    S = np.stack([rng.permutation(X[:, j]) for j in range(d)], axis=1)  # scramble: marginals kept

    # positive control: PLANTED blocks — K_pc latent factors, each driving its own unit block.
    K_pc = ks[len(ks) // 2]
    lat = rng.normal(0, 1, (N, K_pc))
    blk = np.repeat(np.arange(K_pc), int(np.ceil(d / K_pc)))[:d]
    G = np.stack([lat[:, blk[j]] for j in range(d)], axis=1) + rng.normal(0, 0.3, (N, d))
    q_pc = best_blocks(G, K_pc, "pc")
    q_pc_ped = best_blocks(rng.normal(0, 1, (N, d)), K_pc, "pc_ped")
    pc_ratio = (q_pc / q_pc_ped) if abs(q_pc_ped) > 1e-12 else float("nan")
    print("       positive control (K=%d planted blocks · SNR~3): Q=%.6f vs its pedestal %.6f → x%.2f"
          % (K_pc, q_pc, q_pc_ped, pc_ratio))
    PC_BAR = 1.5
    instrument_live = bool(pc_ratio == pc_ratio and pc_ratio >= PC_BAR)
    if not instrument_live:
        print("       ⛔ INSTRUMENT-DEAD: the probe cannot recover blocks it PLANTED at this N/d")
        print("          (x%.2f < bar %.1f). A 'real ~ pedestal' result here would be a power fact,"
              % (pc_ratio if pc_ratio == pc_ratio else float("nan"), PC_BAR))
        print("          not a substrate fact — so NO negative is emitted. Raise N (more prompts)")
        print("          or drop d before reading anything. (positive-control-before-reading-a-negative)")
    else:
        print("       ✅ instrument LIVE (x%.2f >= bar %.1f) — a negative would be readable." % (pc_ratio, PC_BAR))

    out = {"ckpt": ckpt, "N": N, "d": d, "seed": seed,
           "positive_control": {"K": K_pc, "Q": q_pc, "pedestal_Q": q_pc_ped, "ratio": pc_ratio,
                                "bar": PC_BAR, "instrument_live": instrument_live},
           "rows": []}
    if not instrument_live:
        out["verdict"] = "INSTRUMENT-DEAD — no verdict emitted (power, not substrate)"
        if out_path:
            json.dump(out, open(out_path, "w"), indent=1)
            print("")
            print("  wrote: " + out_path)
        return 1
    print("")
    print("%10s | %10s | %10s | %10s | %10s" % ("K", "real Q", "pedestal", "scramble", "real/ped"))
    print("-" * 62)
    for K in ks:
        qr, qp, qs = best_blocks(X, K, "real"), best_blocks(P, K, "ped"), best_blocks(S, K, "scr")
        ratio = (qr / qp) if abs(qp) > 1e-12 else float("nan")
        row = {"K": K, "real_Q": qr, "pedestal_Q": qp, "scramble_Q": qs, "real_over_pedestal": ratio}
        extra = ""
        if R is not None:
            qi = best_blocks(R, K, "randinit")
            row["randinit_Q"] = qi
            row["real_over_randinit"] = (qr / qi) if abs(qi) > 1e-12 else float("nan")
            extra = "  | rand-init %.6f  real/ri %s" % (
                qi, ("%.2f" % row["real_over_randinit"])
                if row["real_over_randinit"] == row["real_over_randinit"] else "—")
        print("%10d | %10.6f | %10.6f | %10.6f | %10s%s" %
              (K, qr, qp, qs, ("%.3f" % ratio) if ratio == ratio else "—", extra))
        out["rows"].append(row)

    # RATIO GUARD (H_9674 · toy d=32 caught this). real/pedestal is only readable while the
    # denominator is safely positive. Modularity Q can go NEGATIVE when the clusterer cannot beat
    # the null model — at d=32 the pedestal came out Q=-0.071 (K=4) and -0.045 (K=8), so the ratio
    # read -0.883 and -1.040: nonsense that the max() then discarded, leaving the verdict resting on
    # the single K=2 cell. A ratio is the wrong statistic when its denominator can cross zero.
    # So rows whose pedestal Q <= 0 are EXCLUDED from the ratio read, and the verdict additionally
    # requires the plain DIFFERENCE (real - pedestal), which stays meaningful at any sign.
    usable = [r for r in out["rows"] if r["pedestal_Q"] > 1e-3]
    dropped = [r["K"] for r in out["rows"] if r["pedestal_Q"] <= 1e-3]
    rr = [r["real_over_pedestal"] for r in usable if r["real_over_pedestal"] == r["real_over_pedestal"]]
    mx = max(rr) if rr else float("nan")
    mxd = max((r["real_Q"] - r["pedestal_Q"]) for r in out["rows"])
    out["max_real_over_pedestal"] = mx
    out["max_real_minus_pedestal"] = mxd
    out["ratio_rows_dropped_nonpositive_pedestal"] = dropped
    if dropped:
        print("  ⚠️ ratio DROPPED at K=%s — pedestal Q <= 0 there (the clusterer could not beat the"
              % dropped)
        print("     null model), so real/pedestal is not a readable statistic in those cells.")
        if not rr:
            print("  ⛔ NO readable ratio cell — verdict withheld (instrument fact, not substrate).")
            out["blocks_exist"] = None
            out["verdict"] = "UNREADABLE — every pedestal Q <= 0 (clusterer below null at this d)"
            if out_path: json.dump(out, open(out_path, "w"), indent=1)
            return 1
    out["blocks_exist"] = bool(mx == mx and mx >= 1.5 and mxd > 0)   # pre-registered bar + sign-safe Δ
    print("")
    print("  max real/pedestal over K : %s   (pre-registered bar: >=1.5 · non-positive-pedestal cells excluded)"
          % (("%.3f" % mx) if mx == mx else "—"))
    print("  max (real - pedestal)    : %.6f   (sign-safe · must be > 0)" % mxd)
    if out["blocks_exist"]:
        print("  VERDICT (H_9674): blocks separate from the zero-truth pedestal => faction-like")
        print("    structure EXISTS in the substrate => H_9643 (learn factions · GPU) is EARNED.")
    else:
        print("  VERDICT (H_9674): real ~ pedestal => NO faction-like block structure in the trunk's")
        print("    unit axis => H_9643 has nothing to learn => the axis CLOSES at $0 and the GPU fire")
        print("    is NOT justified. DIRECTIONAL: correlation-modularity is ONE lens (a_break_the_wall")
        print("    wants 2-3 before a ceiling) — it does not prove modules are absent under every lens.")
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)
        print("")
        print("  wrote: " + out_path)
    return 0


def faction_block_provenance_run(argv):
    """`anima-py evaluate <ckpt> --faction-block-provenance <prompts.json> [--n-factions-sweep 4,8,12]
    [--win 24] [--seed 12345] [--out prov.json]` — are H_9674's blocks REAL modules, or an artifact
    of the architecture's own index layout (card H_9676 · faction-lateral-axis-r3)?

    H_9674 found blocks in the trunk's unit axis (real/pedestal up to 54.07 vs bar 1.5, positive
    control x114). "Blocks exist" does NOT imply "factions are learnable" — the coupling could be
    imposed by the architecture rather than learned. This is the pre-registered exclusion.

    The two suspects, and what the code already says about them:
      GroupNorm groups — nn_groupnorm_fwd(h, ..., T, d, 1, ...) runs with G=1, i.e. LayerNorm over
        all d channels. There are NO group boundaries on the unit axis. Suspect dead by code.
      conv receptive field — _conv1d convolves over T with FULL channel mixing (Cin=d -> Cout=d:
        every output channel reads every input channel). RF is a TIME-axis quantity; the d axis
        carries no spatial ordering at all. Suspect dead by code.
    Both suspects predict the SAME observable: blocks would line up with CONTIGUOUS index runs.
    The code argument is therefore checked, not trusted (`tool-definition-read-code-not-docstring`).

    DV: contiguity of the recovered assignment — adjacency P(assign[i]==assign[i+1]) and ARI against
    the contiguous-chunk partition. Chance adjacency is sum_f p_f^2 on the REALIZED block sizes,
    NOT 1/K: 1/K is the equal-partition special case, and the trunk's blocks come out heavily
    unbalanced while the pedestal's come out even, so scoring both against 1/K charges real's size
    skew as signal (H_9676 correction). Pre-registered bar: >=0.20 over the pedestal's own Δ.
    Arms: real | pedestal (i.i.d. · TRUTH contiguity=0) | positive (PLANTED CONTIGUOUS blocks — the
    metric must score these >=0.80 or a low real contiguity is a metric fact, not a substrate fact).
    Verdict: real ~ chance AND positive ~ 1.0 => blocks are NOT index-contiguous => not a GN/RF
    artifact => H_9674's blocks survive and H_9643 keeps its precondition. real ~ positive => blocks
    ARE contiguous runs => architectural layout => H_9674 is an artifact and H_9643 loses its case."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--faction-block-provenance", "")
    out_path = evaluate_strval(argv[1:], "--out", "")
    T = evaluate_intval(argv[1:], "--win", 24)
    seed = evaluate_intval(argv[1:], "--seed", 12345)
    ks = [int(x) for x in evaluate_strval(argv[1:], "--n-factions-sweep", "4,8,12").split(",") if x.strip()]
    print("=== anima evaluate --faction-block-provenance — H_9674 blocks: real or layout? (H_9676) ===")
    print("ckpt:  " + ckpt)
    print("code:  GN runs G=1 (LayerNorm over all d — no unit-axis group boundary) · conv1d is over T")
    print("       with FULL channel mixing (d->d) — RF is a TIME quantity, the d axis has no spatial")
    print("       order. Both suspects predict CONTIGUOUS blocks. Checked, not trusted.")
    print("arms:  real | pedestal (truth contiguity=0) | positive (PLANTED contiguous · bar >=0.80)")
    spec = json.load(open(spec_path))
    items = spec["items"] if "items" in spec else spec.get("prompts", [])
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    rows = []
    for it in items:
        rows.append(np.asarray(clm.clm_forward_hidden(W, clm._seed_to_tok(it["prompt"], T), T), dtype=np.float64))
    X = np.concatenate(rows, axis=0)
    N, d = X.shape
    print("tap:   X=[%d, %d]  (production trunk penultimate)" % (N, d))
    rng = np.random.default_rng(seed)

    def cluster(M, K, sweeps=6):
        """Same spectral+sweeps clusterer as --faction-block-structure; returns the ASSIGNMENT."""
        C = np.abs(np.corrcoef(M, rowvar=False)); C = np.nan_to_num(C, nan=0.0)
        np.fill_diagonal(C, 0.0)
        n = C.shape[0]
        try:
            _w, V = np.linalg.eigh(C); E = V[:, -K:]
            cent = E[rng.choice(n, K, replace=False)]; assign = np.zeros(n, dtype=int)
            for _ in range(12):
                assign = ((E[:, None, :] - cent[None, :, :]) ** 2).sum(-1).argmin(1)
                for f in range(K):
                    if (assign == f).any(): cent[f] = E[assign == f].mean(0)
        except Exception:
            assign = rng.integers(0, K, n)
        deg = C.sum(1); m2 = C.sum()
        for _ in range(sweeps):
            H = np.zeros((n, K)); H[np.arange(n), assign] = 1.0
            na = np.argmax(C @ H - np.outer(deg, deg @ H) / m2, axis=1)
            if (na == assign).all(): break
            assign = na
        return assign

    def adjacency(assign):
        """P(assign[i] == assign[i+1]) — ~1.0 iff blocks are contiguous index runs."""
        return float((assign[:-1] == assign[1:]).mean())

    def adj_chance(assign, K):
        """Chance adjacency GIVEN the realized block sizes = sum_f p_f^2.

        1/K is the EQUAL-partition special case only. This bit us: the trunk's blocks come out
        heavily unbalanced ([2527, 540, 391, 326] at K=4 — one block holds 67% of the units) while
        the i.i.d. pedestal's come out even ([961, 942, 942, 939]). Scoring both against 1/K made
        the pedestal look right by coincidence (its sum p^2 IS 1/K) and charged real's imbalance as
        signal — a 0.2285 "artifact" that was pure size skew. Against sum p_f^2 real sits at
        -0.0060, i.e. AT chance (H_9676 correction · prereg-table-must-cover-below-chance)."""
        p = np.bincount(assign, minlength=K) / float(len(assign))
        return float((p ** 2).sum())

    def ari(a, b):
        """Adjusted Rand index between two partitions."""
        from math import comb
        ka, kb = int(a.max()) + 1, int(b.max()) + 1
        M = np.zeros((ka, kb))
        for i in range(len(a)): M[a[i], b[i]] += 1
        s = sum(comb(int(v), 2) for v in M.flatten() if v >= 2)
        sa = sum(comb(int(v), 2) for v in M.sum(1) if v >= 2)
        sb = sum(comb(int(v), 2) for v in M.sum(0) if v >= 2)
        n2 = comb(len(a), 2)
        exp = sa * sb / n2 if n2 else 0.0
        mx = (sa + sb) / 2.0
        return float((s - exp) / (mx - exp)) if mx != exp else 0.0

    out = {"ckpt": ckpt, "N": N, "d": d, "seed": seed,
           "code_note": "GN G=1 (LayerNorm · no unit-axis group) · conv1d over T with full d->d channel mixing (RF is a TIME quantity)",
           "rows": []}
    P = rng.normal(float(X.mean()), float(X.std()), (N, d))
    print("")
    print("  (adj columns are adj - chance, chance = sum p_f^2 on realized sizes — NOT 1/K · H_9676)")
    print("%5s | %10s | %10s | %10s | %9s | %10s" %
          ("K", "real Δadj", "ped Δadj", "pos Δadj", "real chance", "real ARI"))
    print("-" * 70)
    ok = True
    for K in ks:
        contig = np.repeat(np.arange(K), int(np.ceil(d / K)))[:d]
        lat = rng.normal(0, 1, (N, K))
        G = np.stack([lat[:, contig[j]] for j in range(d)], axis=1) + rng.normal(0, 0.3, (N, d))
        ar, ap, ag = cluster(X, K), cluster(P, K), cluster(G, K)
        adj_r, adj_p, adj_g = adjacency(ar), adjacency(ap), adjacency(ag)
        # chance is sum p_f^2 on the REALIZED sizes, never 1/K — see adj_chance (H_9676 correction)
        ch_r, ch_p, ch_g = adj_chance(ar, K), adj_chance(ap, K), adj_chance(ag, K)
        ari_r = ari(ar, contig)
        print("%5d | %10.4f | %10.4f | %10.4f | %9.4f | %10.4f" %
              (K, adj_r - ch_r, adj_p - ch_p, adj_g - ch_g, ch_r, ari_r))
        out["rows"].append({"K": K, "real_adjacency": adj_r, "pedestal_adjacency": adj_p,
                            "positive_adjacency": adj_g,
                            "real_chance_sum_p2": ch_r, "pedestal_chance_sum_p2": ch_p,
                            "positive_chance_sum_p2": ch_g,
                            "real_adj_over_chance": adj_r - ch_r,
                            "pedestal_adj_over_chance": adj_p - ch_p,
                            "real_block_sizes": np.bincount(ar, minlength=K).tolist(),
                            "real_ARI_vs_contiguous": ari_r,
                            "positive_live": bool(adj_g - ch_g >= 0.30)})
        if adj_g - ch_g < 0.30: ok = False
    out["instrument_live"] = ok
    print("")
    if not ok:
        print("  INSTRUMENT-DEAD: the metric cannot see contiguity it PLANTED (pos Δadj < 0.30).")
        print("     A low real contiguity would be a metric fact, not a substrate fact — no verdict.")
        out["verdict"] = "INSTRUMENT-DEAD — no verdict emitted"
        if out_path: json.dump(out, open(out_path, "w"), indent=1)
        return 1
    mx_adj = max(r["real_adj_over_chance"] - r["pedestal_adj_over_chance"] for r in out["rows"])
    mx_ari = max(r["real_ARI_vs_contiguous"] for r in out["rows"])
    out["max_real_adj_over_chance"], out["max_real_ARI"] = mx_adj, mx_ari
    artifact = bool(mx_adj >= 0.20 or mx_ari >= 0.20)
    out["artifact"] = artifact
    print("  instrument LIVE (planted contiguity recovered) — the negative is readable.")
    print("  max(real adj - chance) = %.4f   max(real ARI vs contiguous) = %.4f   (bar >=0.20)" % (mx_adj, mx_ari))
    if artifact:
        print("  VERDICT (H_9676): blocks ARE index-contiguous => architectural layout, not modules")
        print("    => H_9674's blocks are an artifact and H_9643's GPU justification is WITHDRAWN.")
    else:
        print("  VERDICT (H_9676): blocks are NOT index-contiguous (real at chance while the planted-")
        print("    contiguous control scores ~1.0) => NOT a GN/RF layout artifact => H_9674's blocks")
        print("    survive and H_9643 keeps its precondition. DIRECTIONAL: excludes the two")
        print("    architectural suspects the code names, not every possible artifact.")
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)
        print("")
        print("  wrote: " + out_path)
    return 0


def faction_lesion_run(argv):
    """`anima-py evaluate <ckpt> --faction-lesion <domains.json> [--perm 200] [--win 24]
    [--seed 12345] [--faction-lam <float>] [--out lesion.json]` — does the trained model's
    faction split carry FUNCTIONAL specialization, or is it the same as slicing the channels at
    random after the fact (card H_9643 · faction-lateral-axis-r3)?

    Why not modularity Q. H_9674's Q instrument cannot answer this: with groups=K the split is
    architectural, so a random-init model has blocks too — our own --arm-random-init measured
    exactly that. Q is a manipulation check here ("did --n-factions do anything"); the verdict is
    functional: zero faction f's channels inside the production forward and read the per-domain
    CE damage. A faction that owns a domain hurts THAT domain when it dies.

    DV — interaction ENERGY over the damage matrix D[f,c] = CE(lesion f, c) - CE(base, c):
        Dn = D / base_CE[c];  R = Dn - rowmean - colmean + grandmean;  S = ||R||_F^2
    A second-order SUM: no max, no argmax, no matching, no alignment assumption. Three earlier
    S's died to their own positive controls — every one of them SELECTED (see selectivity()).
    Chance is MEASURED, never assumed: `--perm` post-hoc reassignments of the same d channels to
    K same-sized groups give a null distribution; the bar is its 95th percentile. (This session
    learned the hard way that a "natural" chance value can be pure structure: adjacency's 1/K was
    an equal-partition special case and charged real's block-size skew as signal — H_9676.)

    Arms, all on the SAME ckpt so no arm gets extra training:
      real      — the trailer's faction blocks (contiguous d/K runs).
      post-hoc  — `--perm` random reassignments, same sizes. THE control H_9643 is about:
                  "임의 사후 분할은 효과 없다" is the claim being tested.
      (random-init and K=1-trained are separate ckpts — run this same flag on them.)

    Verdict: S_real > post-hoc null95 => the split is functionally load-bearing. Otherwise D1
    fires (specialization 불발) and the faction axis closes as a DIRECTIONAL artifact.
    DIRECTIONAL: lesion damage is one lens on "specialization"; it does not prove the factions
    mean anything a human would name."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--faction-lesion", "")
    out_path = evaluate_strval(argv[1:], "--out", "")
    T = evaluate_intval(argv[1:], "--win", 24)
    nperm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 12345)
    lam_ov = evaluate_strval(argv[1:], "--faction-lam", "")
    # --faction-oracle-pi "2,0,0,3": the KNOWN routing of an ORACLE-trained ckpt. Present => run the
    # positive-control DV = double-centered cosine alignment A between the damage matrix R and the pi
    # occurrence template (H_9643 v2 · Fable+Sol converged). A uses NO selection (no argmax x/K, which
    # re-imports the order-statistic bias defects ⑪⑫⑮⑯ killed this session) and is base_CE-immune.
    pi_ov = evaluate_strval(argv[1:], "--faction-oracle-pi", "")
    # --faction-split N: impose an N-way CONTIGUOUS channel split at lesion time, INDEPENDENT of the
    # ckpt's own n_factions. H_9737 fit-matched K=1 negative control: a model trained with groups=1
    # (no faction partition, standard conv) gets a 4-way split imposed — true value is "no faction
    # structure", so S <= null95 isolates that the log-ratio normaliser does not turn fit quality into
    # a false positive at the LOW-CE denominator (random-init K=4 only tests the high-CE scale AND
    # carries grouped-conv architectural blocks that lift its own null — H_9674 confound).
    split_ov = evaluate_intval(argv[1:], "--faction-split", 0)

    print("=== anima evaluate --faction-lesion — 파벌 분할이 기능적인가 (H_9643) ===")
    print("ckpt:  " + ckpt)
    print("why:   Q(모듈러리티)로는 learned vs post-hoc 이 안 갈린다 — groups=K 는 random-init 도")
    print("       블록을 준다(--arm-random-init 이 잡음). 판정은 기능 lesion 해리로 간다.")
    print("chance: post-hoc 랜덤 재배정 %d 회의 null95 — **가정하지 않고 실측**한다." % nperm)

    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    K_model = int(W.get("n_factions", 0) or 0)
    # K = the number of contiguous groups the LESION splits d into. Normally the ckpt's own
    # n_factions; --faction-split overrides it (H_9737: impose 4 groups on a groups=1 ckpt). The
    # model's structural n_factions stays in W and still drives GN/bridge inside the decoder.
    K = split_ov if split_ov > 0 else K_model
    if K <= 0:
        print("ERROR: split 수 미정 — 이 ckpt 엔 CLMF 가 없다 (n_factions=0) 이고 --faction-split 도 없다.")
        print("       --n-factions K 로 학습한 ckpt 이거나, --faction-split N 으로 분할을 강제하라.")
        return 1
    if split_ov > 0:
        print("       --faction-split %d 강제 (ckpt n_factions=%d) — lesion 분할만 override, 모델 구조 무접촉"
              % (split_ov, K_model))
    d = int(W["d"]); V = int(W["V"])
    if lam_ov:
        W["faction_lam"] = float(lam_ov)
        print("       debate lam 오버라이드 = %s (0.0 = OFF arm · 가중치 무접촉)" % lam_ov)
    spec = json.load(open(spec_path))
    doms = spec["domains"] if "domains" in spec else spec
    names = sorted(doms.keys())
    print("d:     %d units · K=%d factions (블록당 %d) · 도메인 %d개: %s"
          % (d, K, d // K, len(names), ", ".join(names)))

    def dom_ce(chans=None):
        """Mean CE over a domain's windows, optionally with `chans` zeroed at the embed-conv
        exit (layer 0) — the same tap _apply_edits already serves for H_9331."""
        out = {}
        for nm in names:
            tot, nw = 0.0, 0
            for text in doms[nm]:
                tok = clm._seed_to_tok(text, T + 1)
                x, y = tok[:T], tok[1:T + 1]
                edits = None if chans is None else [
                    {"layer": 0, "t0": 0, "t1": T, "mode": "mask", "chans": chans}]
                lg = clm.clm_forward_logits_edited(W, x, T, edits) if edits else clm._fwd_logits(W, x, T)
                tot += clm.nn_ce_loss_allpos(lg, np.asarray(y, dtype=np.float64), T, V)
                nw += 1
            out[nm] = tot / max(nw, 1)
        return np.array([out[nm] for nm in names])

    base = dom_ce(None)
    print("")
    print("base CE: " + " · ".join("%s %.4f" % (nm, v) for nm, v in zip(names, base)))

    def selectivity(assign):
        """S = ||R||_F^2 over the DOUBLY-CENTERED, column-standardised damage matrix.

        D[f,c] = CE(lesion f, domain c) - CE(base, c);  Dn = D / base_CE[c];
        R = Dn - rowmean - colmean + grandmean;  S = sum(R**2).

        THREE things this does NOT do, each earned by an instrument that died this session:

        1. It never SELECTS. No max, no argmax, no optimal matching. Every selection-based S we
           tried floated its own null up to meet the signal, because a random assignment also
           picks the largest of C cells:
             s_max        planted 1.3879 vs post-hoc null95 1.7270  (real BELOW the null's mean)
             hungarian    planted 4.7598 vs null95 5.5101           (optimal matching is an order
                                                                     statistic too)
             split-half   planted 1.6775 vs null95 2.2655           (argmax on half A still leaks
                                                                     into B when the halves' noise
                                                                     is correlated — and on the
                                                                     same prompt set it is)
           A second-order SUM has no selection step, so the bias cannot enter.
        2. It never assumes ALIGNMENT. trace(R) reads only the (f,f) cells; the trained toy owned
           [ccc, aaa, aaa, ddd] — non-identity, one domain shared by two factions, one orphan —
           so trace read 1 of 4 planted cells and scored +0.0711 against a null95 of +3.3390.
           A sum over ALL cells does not care which faction got which domain.
        3. It never normalises by its own scale. ||R||^2 / sd(R)^2 is EXACTLY K*C for any matrix
           (sd^2 = sum/KC) — a constant that measures nothing. We shipped that for one run and the
           synthetic caught it at a suspiciously round 16.0000.

        Column standardisation (dividing by each domain's base CE) handles the 16x difficulty
        spread: damage couples MULTIPLICATIVELY to how much CE a domain has to lose, and
        double-centering removes only the ADDITIVE part.

        Verified on synthetic damage reproducing the real failure mode (non-identity owner map,
        shared ownership, orphan domain, 16x base spread, multiplicative coupling, and a channel-
        REASSIGNMENT null that preserves the signal and breaks only the grouping):
          planted    S 5428.50 vs null95  796.45   PASS
          no signal  S   33.35 vs null95   92.64   PASS (does not hallucinate)
        """
        D = np.zeros((K, len(names)))
        Dn = np.zeros((K, len(names)))
        eps = 1e-4                                              # nats — a real CE floor, not 1e-9
        for f in range(K):
            L = dom_ce(np.where(assign == f)[0])               # lesioned CE per domain
            D[f] = L - base                                    # raw ΔCE — kept for report/json
            # v2 (H_9643 · Fable+Sol converged): the docstring says damage couples MULTIPLICATIVELY,
            # and the exact additive-ization of a multiplicative effect is the LOG, not division. The
            # old Dn = D/base_CE blows up as base_CE -> 0 (a well-fit ckpt: base 0.01, lesion 1.0 =>
            # Dn ~ 100, S ~ 1e4), so a model's FIT QUALITY dominated S and made cross-arm S values
            # (the lambda ladder, the S_real/S_randinit bar) uncomparable. log-ratio compresses that
            # (Delta_log ~ 4.6) and double-centering removes the additive column effect EXACTLY.
            Dn[f] = np.log((L + eps) / (base + eps))
        R = Dn - Dn.mean(axis=1, keepdims=True) - Dn.mean(axis=0, keepdims=True) + Dn.mean()
        return float((R ** 2).sum()), D, R

    # real arm — the trailer's faction blocks are CONTIGUOUS d/K runs (core/model.py builds the
    # grouped conv that way, and pack_faction_section writes K, not an explicit assignment).
    per = d // K
    real_assign = np.arange(d) // per
    S_real, D_real, R_real = selectivity(real_assign)
    print("")
    print("파벌별 최대손상 도메인 (real · 참고용 — S 는 이 argmax 를 쓰지 않는다):")
    for f in range(K):
        c = int(np.argmax(D_real[f]))
        print("  faction %d → %-10s ΔCE %+.4f" % (f, names[c], D_real[f, c]))
    print("")
    print("S_real = %.4f   (‖R‖²_F · log-ratio 셀정규화 · 선택 없는 2차 합)" % S_real)

    # ORACLE positive-control DV — cosine alignment of R to the KNOWN pi routing template. Selection-
    # free, base_CE-immune (cosine cancels scale). Only computed when --faction-oracle-pi is given.
    pi = None
    if pi_ov:
        pi = [int(x) for x in pi_ov.replace(" ", "").split(",")]
        M = np.zeros((K, len(names)))
        for f, c in enumerate(pi):
            if 0 <= f < K and 0 <= c < len(names):
                M[f, c] = 1.0                                  # dom shared by 2 factions => 2 ones;
        Mc = M - M.mean(1, keepdims=True) - M.mean(0, keepdims=True) + M.mean()  # orphan dom col => 0
        def align(R):
            n = np.linalg.norm(R) * np.linalg.norm(Mc)
            return float((R * Mc).sum() / n) if n > 1e-12 else 0.0
        A_real = align(R_real)
        print("A_real = %+.4f   (π=%s 이중중심 코사인 정렬 · argmax 카운트 대체)" % (A_real, pi))

    rng = np.random.default_rng(seed)
    null, null_A = [], []
    for i in range(nperm):
        S_p, _, R_p = selectivity(rng.permutation(real_assign))
        null.append(S_p)
        if pi is not None:
            null_A.append(align(R_p))
        if (i + 1) % max(nperm // 4, 1) == 0:
            print("  post-hoc null %d/%d …" % (i + 1, nperm), flush=True)
    null = np.array(null)
    null95 = float(np.percentile(null, 95))
    # exceedance p — the honest small-perm statistic (Fable Q3: at perm=40 null95 is one order-stat,
    # its sampling error swamps a thin margin; report p and flag perm<200 as PENDING, never a verdict).
    p_exc = float((1 + int(np.sum(null >= S_real))) / (nperm + 1))
    print("")
    print("post-hoc null: mean %.4f · sd %.4f · **null95 %.4f** · p=%.4f  (n=%d)"
          % (null.mean(), null.std(), null95, p_exc, nperm))
    passed = bool(S_real > null95)
    thin = nperm < 200
    out = {"ckpt": ckpt, "K": K, "d": d, "domains": names, "seed": seed, "perm": nperm,
           "faction_lam": (float(lam_ov) if lam_ov else None),
           "base_ce": base.tolist(), "damage": D_real.tolist(),
           "S_real": S_real, "null_mean": float(null.mean()), "null_sd": float(null.std()),
           "null95": null95, "p_exceedance": p_exc, "specialization": passed,
           "instrument": "v2-logratio", "perm_underpowered": thin}
    if pi is not None:
        A_null95 = float(np.percentile(np.array(null_A), 95))
        out.update({"oracle_pi": pi, "A_real": A_real, "A_null95": A_null95,
                    "oracle_recovered": bool(A_real > A_null95)})
        print("oracle A_null95 %+.4f ⟹ π 회수 %s" % (A_null95, "YES" if A_real > A_null95 else "no"))
    print("")
    if passed:
        print("  within-arm: S_real %.4f > post-hoc null95 %.4f (p=%.4f) ⟹ 이 ckpt 의 파벌 분할이"
              % (S_real, null95, p_exc))
        print("    임의 사후 분할과 구별된다 (base_CE 는 real·null 양쪽서 상쇄 = 스케일 공정).")
    else:
        print("  within-arm (D1): S_real %.4f <= post-hoc null95 %.4f (p=%.4f)" % (S_real, null95, p_exc))
        print("    ⟹ 이 ckpt 서 파벌 특화가 임의 사후 분할과 구별 안 됨.")
    if thin:
        print("  ⏳ PENDING: perm=%d < 200 — null95 는 순서통계량 1개 추정이라 얇은 마진 판정 미발행"
              " (검정력-before-negative). --perm 200 이상 재발사 필요." % nperm)
    print("  ⚠️ DIRECTIONAL + within-arm 한정: 이 판정은 '이 ckpt 가 랜덤분할과 다른가'만 답한다.")
    print("     완전 SOUND 인증 = ① within-arm PASS(perm≥200) ② random-init 음성 clean null")
    print("     ③ fit-matched K=1 음성(같은 낮은-CE·파벌구조 없음 → S≤null95) ④ ORACLE π 회수(A>A_null95).")
    print("     cross-arm 절대 S 비교(옛 S_real/S_randinit≥2.0)는 base_CE 스케일 산물이라 폐기됨.")
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)
        print("")
        print("  wrote: " + out_path)
    return 0


def closure_ladder_run(argv):
    """`anima-py evaluate --closure-ladder [--closure-arm {live,open,dead}]
                          [--closure-ticks N] [--closure-seed S] [--out f.json]`

    H_9807 — the INTERVENTIONAL CLOSURE LADDER (rung 1), engine-native. Backend =
    core/closure_ladder.py. Takes NO ckpt: the rig's subject is a scripted agent in a
    deterministic micro-tenant world, so the whole battery is $0/toy/CPU.

    It asks whether an agent's CONTINGENCY STRUCTURE — not its action marginal — leaves a
    distributional fingerprint on its OWN subsequent input, against marginal-matched
    Watson YOKED-GHOST replays (same actions, permuted). Because the executed action is
    A/B-randomized, P(I|do(A)) is IDENTIFIED, so this rig can ANCHOR rather than merely
    correlate — the only lens in this repo that can.

    Bare (no --closure-arm) runs the 3-plant CERTIFICATION battery, which is the only
    thing that yields a verdict:
        P-LIVE contingent policy      -> must ANCHOR
        P-OPEN same actions as a tape -> must land exactly CHANNEL-ONLY (marginal alive,
                                         contingency destroyed) — this is what makes the
                                         gate a measurement and not a tautology
        P-DEAD contingent policy in an INERT env -> must REFUSE on BOTH LV-W and LV-C

    P-DEAD's LV-C leg is a STANDING PRE-CHECK, not decoration: upstream, P-DEAD checked
    only LV-W, and a frame misalignment (Closed read PRE-step obs while the ghosts read
    POST-step) let the certified estimator score 0.667 closure in a provably dead world —
    above its own 0.60 gate. The repaired estimator reads 0.000 there. If the null arm
    ever climbs off the floor again, the battery hard-fails INSTRUMENT-INVALID.

    ⚠️ Rung 1 is NOT aliveness: a thermostat clears it, and the scripted P-LIVE plant here
    MUST clear it by design. Full contract → card H_9807.
    """
    sys.path.insert(0, os.path.join(_REPO, "core"))
    import closure_ladder as CL
    rest = [a for a in argv if a != "--closure-ladder"]
    arm = evaluate_strval(rest, "--closure-arm", "")
    seed = evaluate_intval(rest, "--closure-seed", 7)
    ticks = evaluate_intval(rest, "--closure-ticks", 600)
    out_path = evaluate_strval(rest, "--out", "")
    if ticks < 2 * CL.BLOCK:
        print("ERROR: --closure-ticks %d gives fewer than 2 LV-C blocks (BLOCK=%d); the "
              "closure sign statistic is undefined. Use >= %d."
              % (ticks, CL.BLOCK, 2 * CL.BLOCK), file=sys.stderr)
        return 2
    if arm:
        if arm not in ("live", "open", "dead"):
            print("ERROR: unknown --closure-arm %r (known: live, open, dead)" % arm,
                  file=sys.stderr)
            return 2
        res = CL.run_arm(arm, seed, ticks)
        print(CL.format_arm_report(res))
        ok = True
    else:
        res = CL.certify(seed, ticks)
        print(CL.format_report(res))
        ok = bool(res["certified"])
    res["schema"] = "anima-closure-ladder/v1"
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(res, fh, indent=2)
        print("  wrote " + out_path)
    return 0 if ok else 1


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        evaluate_usage()
        return 0
    _bad = _reject_unknown_flags(argv)
    if _bad:
        print(_bad, file=sys.stderr, flush=True)
        return 2
    # H_9328 DO-MOUTH · I(A;Y|S) over decision traces (NO decode — reads traces the daemon
    # already wrote). V-CEILING FIRST: I <= H(A|S) is an identity, so a dead action channel
    # forces I=0 by definition, not by measurement (that is exactly how H_9308 died).
    if "--collide-select" in argv:
        _ck = [a for a in argv if not a.startswith("--")]
        return _collide_select(_ck[0] if _ck else "", [a for a in argv if a.startswith("--")])
    # H_9807 --closure-ladder: the interventional CLOSURE rig (rung 1). Ckpt-less by
    # construction (scripted agent + deterministic micro-tenant world), so it dispatches on
    # flag PRESENCE, not on argv[0]. ADDITIVE — it moves no frozen bar and touches no panel.
    if "--closure-ladder" in argv:
        return closure_ladder_run(argv)
    # H_9838 --hippo-transitive-selftest: core/hippo_lane.py's CA3 multi-step completion on a
    # planted premise world. Ckpt-FREE by construction (the store + completion are pure numpy
    # arithmetic), so it dispatches on flag PRESENCE like --closure-ladder. ADDITIVE and
    # READ-SIDE ONLY — it moves no frozen bar and opens no write path into the emit-drive lane.
    if "--hippo-transitive-selftest" in argv:
        return hippo_transitive_selftest_run(argv)
    # ── H_9808 $0 PRE-REGISTRATION GATES ────────────────────────────────────────────────────
    # Ckpt-FREE, closed-form referees dispatched on the leading flag: they read a spec file and
    # decide ADMISSIBILITY, never a verdict. Exit 3 = REFUSE (abort before spend), 0 = PASS,
    # 2 = malformed spec (never silently a PASS). ADDITIVE — no frozen bar is touched.
    if len(argv) >= 1 and argv[0] == "--pregate-selftest":
        return pregate_selftest_run()
    if len(argv) >= 2 and argv[0] == "--falsifier-headroom":
        return falsifier_headroom_run(argv)
    if len(argv) >= 2 and argv[0] == "--free-slot-score":
        return free_slot_score_run(argv)
    if len(argv) >= 2 and argv[0] == "--register-leak-probe":
        return register_leak_probe_run(argv)
    if len(argv) >= 1 and argv[0] == "--refractory-preview":
        return _refractory_preview(argv[1:])
    if len(argv) >= 1 and argv[0] == "--emit-gate-census":
        return _emit_gate_census(argv[1:])
    if len(argv) >= 1 and argv[0] == "--pc2-direction":
        if "--state-census" in argv:
            return _pc2_state_census([a for a in argv[1:] if a != "--state-census"])
        if "--occupancy" in argv:
            return _pc2_occupancy([a for a in argv[1:] if a != "--occupancy"])
        if "--zeta-slope" in argv:
            _zrest = [a for a in argv[1:] if a != "--zeta-slope"]
            if "--by-loading" in argv:
                return _pc2_zeta_by_loading([a for a in _zrest if a != "--by-loading"])
            return _pc2_zeta_slope(_zrest)
        if "--atom-census" in argv:
            return _pc2_atom_census([a for a in argv[1:] if a != "--atom-census"])
        if "--rank-null" in argv:
            return _pc2_rank_null(argv[1:])
        if "--factor-census" in argv:
            return _pc2_factor_census(argv[1:])
        if "--stage-slave" in argv:
            return _pc2_stage_slave(argv[1:])
        if "--variance-audit" in argv:
            return _pc2_variance_audit(argv[1:])
        if "--emit-coupling" in argv:
            return _pc2_emit_coupling(argv[1:])
        if "--subspace-stability" in argv:
            return _pc2_subspace_stability(argv[1:])
        return _pc2_direction(argv[1:])
    if len(argv) >= 1 and argv[0] == "--ag-criticality":
        return _ag_criticality(argv[1:])
    # H_9806 COMPRESSION-MI — measures a property of the STREAM, so it takes no ckpt and
    # dispatches on argv[0]. $0, stdlib-only, no GPU. Both carry their own certification.
    if len(argv) >= 1 and argv[0] == "--stream-mi":
        return stream_mi_run(argv)
    if len(argv) >= 1 and argv[0] == "--capture-anchor":
        return capture_anchor_run(argv)
    if len(argv) >= 1 and argv[0] == "--gen-percept-schedule":
        return _gen_percept_schedule(argv[1:])
    if len(argv) >= 1 and argv[0] == "--eval-historicity":
        return _eval_historicity(argv[1:])
    if len(argv) >= 1 and argv[0] == "--af-forward":
        return _af_forward(argv[1:])
    if len(argv) >= 1 and argv[0] == "--silence-content-te":
        return _silence_content_te(argv[1:])
    if len(argv) >= 1 and argv[0] == "--timing-channel":
        return _timing_channel(argv[1:])
    if len(argv) >= 1 and argv[0] == "--cf-emit":
        return _cf_emit(argv[1:])
    if len(argv) >= 1 and argv[0] == "--g-amp-screen":
        return _g_amp_screen(argv[1:])
    if len(argv) >= 2 and argv[0] == "--cf-straddle":
        return _cf_straddle(argv[1:])
    if len(argv) >= 2 and argv[0] == "--falsi-census":
        return _falsi_census(argv[1:])
    if len(argv) >= 2 and argv[0] == "--dead-census":
        return _dead_census(argv[1:])
    if len(argv) >= 2 and argv[0] == "--lane-census":
        return _lane_census(argv[1:])
    if len(argv) >= 2 and argv[0] == "--gate-census":
        return _gate_census(argv[1:])
    if len(argv) >= 2 and argv[0] == "--gate-deaf":
        return _gate_deaf(argv[1:])
    if len(argv) >= 2 and argv[0] == "--audibility":
        return _audibility(argv[1:])
    if len(argv) >= 2 and argv[0] == "--g-tension":
        return _g_tension(argv[1:])
    if len(argv) >= 2 and argv[0] == "--tension-emit":
        return _tension_emit(argv[1:])
    if len(argv) >= 2 and argv[0] == "--psi-soma":
        return _psi_soma_real(argv[1:])
    if len(argv) >= 2 and argv[0] == "--interact-mi":
        return _interact_mi(argv[1:])
    # H_9212 ③ per-cell dispatch wiring self-test (torch-free · NO decode · internal subprocess)
    if len(argv) >= 1 and argv[0] == "--selftest-rho-cells":
        cok, cchecks = _selftest_rho_cells()
        for nm, v in cchecks:
            print(("  PASS " if v else "  FAIL ") + nm)
        try:
            import rho_fan as _rf
            rok = _rf._rho_fan_cells_selftest()
            for nm, v in rok["checks"]:
                print(("  PASS " if v else "  FAIL ") + "[rho_fan] " + nm)
            cok = cok and rok["ok"]
        except Exception as e:  # pragma: no cover
            print("  FAIL rho_fan cells selftest import: " + str(e))
            cok = False
        print("SELFTEST rho-cells: " + ("OK" if cok else "FAIL"))
        return 0 if cok else 1
    # --result-file <f>: write ALL output to <f> and keep fd 1 (stdout) silent. The hexa
    # launcher runs evaluate via exec(), whose captured stdout pipe it closes after ~150s
    # (probe-confirmed: a child reaching ~150s gets EPIPE on its next fd-1 write, but the
    # child itself is NOT killed). A 303M numpy decode runs for minutes; if it writes to
    # fd 1 it dies on BrokenPipe mid-battery. Redirecting our stdout to a file means fd 1
    # stays silent → the child survives the pipe close, finishes the full G0-G6 battery,
    # and the launcher cats <f> in a SECOND fresh exec (fast, well under the limit).
    # byte-faithful stdout: a real ckpt's greedy decode can emit non-utf8 bytes (held as
    # surrogateescape str), so any raw-continuation dump (--probe/--dump-hidden) prints a
    # surrogate-bearing str. A strict stdout would UnicodeEncodeError-crash mid-battery →
    # a spurious infra failure on the TERMINAL verdict path. Mirror hexa's byte-native
    # stdout by tolerating surrogates (clean text is byte-identical). convergence engine-cli-py-1.
    if "--result-file" in argv:
        i = argv.index("--result-file")
        f = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
        sys.stdout = open(f, "w", buffering=1, encoding="utf-8", errors="surrogateescape")
    else:
        try:
            sys.stdout.reconfigure(errors="surrogateescape")
        except (AttributeError, ValueError):
            pass
    try:
        sys.stderr.reconfigure(errors="surrogateescape")
    except (AttributeError, ValueError):
        pass
    # H_9200 ρ-AXON — reach-layer panel (G0-G6 → ρ-AXON, cli/rho_axon.py). Strip + set
    # the process-global so evaluate_run renders the ρ-AXON panel instead of G0-G6.
    global _RHO_AXON
    if "--rho-axon" in argv:
        argv = [a for a in argv if a != "--rho-axon"]
        _RHO_AXON = True
    # H_9200 E1 — SLW gated-write forward-slot eval-time controls (strip + set the
    # process-global switches in core/decode; frozen-first, no retraining):
    #   --slot-off        force γ=0 => bit-exact base trunk (slot-ablation control)
    #   --slot-shuffle N  permute the WRITE address with seed N (shuffle-bind control)
    _slot_off = "--slot-off" in argv
    if _slot_off:
        argv = [a for a in argv if a != "--slot-off"]
    _slot_shuffle = None
    if "--slot-shuffle" in argv:
        i = argv.index("--slot-shuffle")
        _slot_shuffle = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if _slot_off or _slot_shuffle is not None:
        clm.set_slw_controls(gamma_override=(0.0 if _slot_off else None),
                             shuffle_seed=_slot_shuffle)
    # --system-g1: RECOMBINATION-RELOCATION pipe (card H_9035). Strip the flag and
    # route the remaining <ckpt> [--gen N] to the system-G1 harness.
    if "--system-g1" in argv:
        i = argv.index("--system-g1")
        argv = argv[:i] + argv[i + 1:]
        return system_g1_run(argv)
    # --ground-probe <manifest.json>: the NBIND-G grounding instrument, whole and engine-native
    # (answer point · taught carrier · V-LIVE positive control · flip-undone atom aggregation ·
    # atom-level power · permutation null). The five defects it fixes are in ground_probe_run.
    if "--ground-probe" in argv:
        return ground_probe_run(argv)
    # --valence-audit <manifest.json>: AUDIT-A — is the atom's polarity in the weights AT ALL
    # (read in its real corpus contexts), or is a probe just reading the sentiment neighbourhood?
    # The verdict is Delta = probe(atom) - probe(length-matched NEUTRAL swapped into the SAME
    # context), against a permutation null. Kills the O-channel fire before it burns GPU.
    # --route-audit <manifest.json>: H_9355 LOCUS-CAUSAL — the ConvMoE router's per-surface expert
    # distribution. Asks the one question a hidden-space probe cannot: not what is represented, but
    # WHICH EXPERT COMPUTED IT. A route split (beyond a byte-matched inert suffix) makes the
    # two-lane model PHYSICAL; a shared route kills route-pin before it is fired.
    if "--route-audit" in argv:
        return route_audit_run(argv)
    if "--bind-locus" in argv:
        return bind_locus_run(argv)
    # --decl-flip <c.txt.decl.json>: H_9800 EPHEMERAL-DECLARATION grounding — the H_9359
    # declaration-flip diagnostic promoted to a first-class scored flag. ADDITIVE: it moves no
    # frozen bar and touches no existing panel.
    if "--decl-flip" in argv:
        return decl_flip_run(argv)
    if "--twin-screen" in argv:
        return twin_screen_run(argv)
    if "--twin-necessity" in argv:
        return twin_necessity_run(argv)
    if "--delta-pregate" in argv:
        return delta_pregate_run(argv)
    if "--delta-control" in argv:
        return delta_control_run(argv)
    if "--valence-audit" in argv:
        return valence_audit_run(argv)
    # --device-parity: is this host's GPU forward the same measurement as its CPU forward? The probes
    # read hiddens, and the hidden is NOT byte-identical across devices (decode-py-4).
    if "--device-parity" in argv:
        return device_parity_run([a for a in argv if a != "--device-parity"])
    # --dump-hidden <prompts.json>: read-only penultimate-hidden dump (ρ·weave / γ
    # binding-lane probe H_9235). argv[0]=ckpt; dump_hidden_run reads --dump-hidden/--out.
    if "--dump-hidden" in argv:
        return dump_hidden_run(argv)
    # H_9803 --fan-branch {live|assignment-shuffle|off}: the branch-latent ideation-fan arms.
    # ADDITIVE — it never touches eval_reach_all / the frozen G0-G6 bars; `off` is the
    # byte-identity parity control for the IFAN trailer.
    if "--fan-branch" in argv:
        return fan_branch_run(argv)
    # H_9805 --tension-rank-audit: effective rank of the write-side parse-disagreement field, with
    # a rank-1 positive control and a byte-shuffled pedestal. ADDITIVE — never touches the frozen
    # G0-G6 bars; exists so a rank-1 collapse (= the old scalar seam) can never hide.
    if "--tension-rank-audit" in argv:
        return tension_rank_audit_run(argv)
    # H_9810 --bind-panel <panel.json>: held-out binding d_acc on the `anima corpus bindpanel`
    # panel — the scorer H_9805's F1 (Δd_acc(duel − rank1)) had no instrument for. Prints the
    # FIELD-BLIND ceiling before any treatment number. ADDITIVE — frozen bars untouched.
    if "--bind-panel" in argv:
        return bind_panel_run(argv)
    # --store-addr-census <dump.npz> / --store-census-selftest: H_9719 emergent-address
    # $0 pre-screen — argmax-collision of random-W_q over entity-keys vs a structureless-H
    # pedestal. DIRECTIONAL screener (KILL-before-spend); admissible (no target_slot read).
    if "--store-addr-census" in argv or "--store-census-selftest" in argv:
        return store_addr_census_run(argv)
    # --store-retr-probe <dump.npz> / --retr-probe-selftest: H_9825 bridge-faithful retrieval
    # CEILING — fits the linear query map the bridge itself uses and reads held-out entity
    # retrieval against ORACLE (positive) and NULL (zero-truth) arms. DIRECTIONAL, never cements.
    if "--store-retr-probe" in argv or "--retr-probe-selftest" in argv:
        return store_retr_probe_run(argv)
    # --store-parity-selftest: H_9826 — the store lane is written twice (torch trainer vs numpy
    # inference mirror) and was synchronised by a comment only. Asserts they agree AND that a
    # resampled tensor is caught, so the guard is known to be able to fail. Needs the [train] extra.
    if "--store-parity-selftest" in argv:
        return store_parity_selftest_run(argv)
    # --faction-phi-proxy <prompts.json>: the ARCHIVED faction Phi proxy recomputed on live
    # trunk activations vs a zero-truth PEDESTAL (H_9660/H_9654 · faction-lateral-axis-r3).
    # Indicts the formula; never cements a consciousness verdict (a_phi_iit4_tool).
    if "--faction-phi-proxy" in argv:
        return faction_phi_proxy_run(argv)
    # --faction-block-structure <prompts.json>: does the trunk unit axis carry faction-like
    # modular blocks at all (H_9674)? The $0 precondition for H_9643's GPU fire.
    if "--faction-block-structure" in argv:
        return faction_block_structure_run(argv)
    # --faction-lesion <domains.json>: is the trained faction split FUNCTIONAL, or the same as
    # slicing channels at random after the fact? (H_9643 Q2 · chance = post-hoc null95)
    if "--faction-lesion" in argv:
        return faction_lesion_run(argv)
    # --faction-block-provenance: H_9674 블록이 진짜 모듈인가 architecture index layout(GN/RF)인가 (H_9676)
    if "--faction-block-provenance" in argv:
        return faction_block_provenance_run(argv)
    # --interaction-lift <manifest.json>: read-only engine-native joint interaction-lift
    # NLL surface (H_9255). argv[0]=ckpt; interaction_lift_run reads --interaction-lift/--out.
    if "--earned" in argv:
        import earned as _earned
        return _earned.earned_run(argv)
    if "--interaction-lift" in argv:
        return interaction_lift_run(argv)
    # --probe <spec.json>: matched-surface G1 probe (card H_6189). argv[0]=ckpt; probe_run
    # reads --probe/--gen from the tail. Greedy raw-continuation dump for offline scoring.
    if "--probe" in argv:
        return probe_run(argv)
    # --xbind <manifest.json>: held-out XBIND recombination (G1 reopen lane a · card H_9267).
    # argv[0]=ckpt; xbind_run reads --xbind/--out/--arm from the tail. Engine-native greedy
    # D-acc on held-out xor(pol_a,pol_b) pairs (the corpus×task-class measure-swap exit).
    if "--bridge-trace" in argv:
        return bridge_trace_run(argv)
    # --store-mix <store.json> [--store-lambda λ]: H_9392 BRIDGE-BOLT — bolt a runtime
    # store-lookup onto the frozen trunk (p = λ·p_store + (1−λ)·p_trunk at the measured
    # answer position). SEQUENTIAL C0 gate (λ=0 byte-identical to baseline) inside the run.
    if "--store-mix" in argv:
        return store_mix_run(argv)
    # --store <held.json> [--store-oracle] [--store-lambda λ]: H_9423 CLMS store-bridge lane — the
    # CO-TRAINED bridge (store injected at the query, answer-position logits OVERWRITTEN by the lane's
    # content-addressed lookup). Distinct from --store-mix (H_9392 post-forward actuator).
    if "--fan-bind" in argv:                       # H_9693 (R1) bind-Δ instrument
        return fan_bind_run(argv)
    if "--store" in argv:
        return store_run(argv)
    if "--xbind" in argv:
        return xbind_run(argv)
    # --xfan <manifest.json>: held-out XFAN one-to-many fan (G6 reopen lane · card H_9271).
    # coverage C over K sampled decodes per held-out concept (the corpus×task-class one-to-many
    # measure — the G6 homolog of XBIND's 1-bit discrimination).
    if "--xfan" in argv:
        return xfan_run(argv)
    return evaluate_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
