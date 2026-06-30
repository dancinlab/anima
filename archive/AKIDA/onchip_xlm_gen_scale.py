#!/usr/bin/env python3
"""Lane A-single SCALE-TRANSFER RUNG — single-step open-vocab GENERATION across an ANCHOR-COUNT ladder on live AKD1000.

substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope (>=3-rung ladder).

WHERE WE ARE (verbatim frontier): the single-step open-vocab GENERATION rung (onchip_xlm_generation.py) PROVED an
above-NULL on-chip next-step DECODE at the FULL corpus_big (250 anchors / 50 concepts): gen_acc ci_lo=0.4096 >>
shuffle-NULL hi=0.0418, > identity-NULL hi=0.3847 (F-GEN-1 + F-GEN-2 REFUTED). That is a SINGLE scale point. Per
a_scale_honest_scope a scale-dependent conclusion needs a LADDER curve (>=3 rungs), not one point.

THIS RUNG (the next honest A-single rung): does single-step generation HOLD ABOVE shuffle-NULL as the codebook /
anchor count GROWS? We sweep ANCHOR-COUNT = (n_concepts x 5 langs) over a >=3-rung ladder and report, AT EACH RUNG,
the held-out single-step gen_acc with a shuffle-NULL + 95% CI, learning-on-chip every trial (encoder_learned per
trial). The on-chip pipeline is BYTE-IDENTICAL to onchip_xlm_generation.py (enc_whitened encoder, bind/neutral_bind,
256-unit AkidaUnsupervised FC, open-vocab full-codebook decode); only the concept subset (codebook size) varies.

PRE-REGISTERED FALSIFIER (declared BEFORE the run, g63 honest):
  metric per rung: gen_acc = P(argmax_{c!=t, open-vocab} overlap(g_hat_t, codebook[c]) == t+1).
  NULL-A (SHUFFLE): same open-vocab decode with t->t+1 labels permuted (B=200); hi = mean+1.96sd; empirical p.
  FALSIFIER F-GEN-SCALE-1 (the headline): "single-step on-chip GENERATION does NOT hold above the shuffle-NULL as
    the anchor count grows" -> REFUTED iff, at EVERY rung, gen ci_lo > NULL hi AND p<0.05 (signal SURVIVES scale).
  FALSIFIER F-GEN-SCALE-2 (no collapse): "gen_acc COLLAPSES toward chance as anchors grow" -> REFUTED iff the
    largest-rung gen ci_lo stays above BOTH its shuffle-NULL hi AND >= 2x its own chance (1/(NC-1)).
DISPOSITION:
  all rungs above-NULL -> single-step generation SCALE-SURVIVES on silicon (A-single ceiling holds across scale).
  a rung drops into NULL -> honest CLOSED-NEGATIVE naming the anchor-count at which 1-bit/256-unit generation caps
    (a_paper_negative_ok; the on-chip ceiling is QUANTIFIED, finding-either-direction valid).
  NO fabricated PUBLIC. NO sw fallback labelled on-chip.
"""
import os, json, struct, time, sys
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
NTRIALS = 8
UNITS, NW, LCOMP = 256, 8, 0.1     # byte-match onchip_xlm_generation generator FC
SHIFT = 37
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
SEED = 20260602
# anchor-count ladder: each rung uses the first N_CONCEPTS sorted concepts x 5 langs -> N_CONCEPTS*5 anchors.
# default rungs -> 50 / 100 / 250 anchors (n_concepts 10 / 20 / 50). override via LANE_A_GEN_NCONCEPTS="10,20,50".
NCONCEPTS_LADDER = [int(x) for x in os.environ.get("LANE_A_GEN_NCONCEPTS", "10,20,50").split(",")]

def read_limen(path):
    blob = open(path, "rb").read(); assert blob[:8] == LIMEN_MAGIC
    off = 8; struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode()); recs.append((head, rec[4+hlen:]))
    return count, recs

def byte_hist(payload):
    pres = np.zeros(INC, dtype=np.float64)
    for b in payload: pres[b] += 1.0
    return pres

def enc_whitened(H):  # byte-match onchip_xlm_generation.enc_whitened
    Hc = H - H.mean(axis=0, keepdims=True)
    cov = (Hc.T @ Hc)/max(1, Hc.shape[0]-1) + 1e-3*np.eye(INC)
    w, V = np.linalg.eigh(cov)
    W = V @ np.diag(1.0/np.sqrt(np.maximum(w, 1e-9))) @ V.T
    scale = 7.0/(np.max(np.abs(W))+1e-12)
    Pq = np.clip(np.round(W*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def bind(a, b):
    return (a.astype(np.uint8) ^ np.roll(b.astype(np.uint8), SHIFT)).astype(np.uint8)
def neutral_bind(a):
    return (a.astype(np.uint8) ^ np.roll(a.astype(np.uint8), NEUTRAL_ROLL)).astype(np.uint8)

def build_fc(wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]

def to_chip(Xb):
    Xb = np.atleast_2d(Xb).astype(np.uint8)
    return Xb.reshape(Xb.shape[0], 1, 1, INC)

def fit_forward(Xtrain, Xeval, init_w, do_fit=True):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    if do_fit:
        Xt = to_chip(Xtrain)
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    Xe = to_chip(Xeval)
    out = np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
    learned = bool(np.any(post != pre))
    del m
    return out, learned

def binarize(out2d):
    return (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
def overlap(a_bin, b_soft):
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))
def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

# ---- load corpus once ----
# default = corpus_big (real 50-concept FLORES cross-lingual, byte-eq prior rungs). LANE_A_CORPUS overrides the
# corpus dir for the CHIP-CAPACITY frontier (e.g. "corpus_synth" — distinguishable synthetic anchors past the
# 250-anchor real-corpus ceiling; labelled synthetic in RESULTS["corpus"], NOT a semantic claim).
CORPUS_DIR = os.environ.get("LANE_A_CORPUS", "corpus_big")
count, recs = read_limen(os.path.join(ROOT, CORPUS_DIR, "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted_full = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
codes_enc_full = enc_whitened(H)   # encoder computed ONCE over the full corpus (byte-eq); subset by concept below
print("[gen-scale] SUBSTRATE = AKIDA (on-chip 1-bit Hebbian) — NOT HYBRID, NOT Lane G")
print("[gen-scale] akida %s device %s ip %s  corpus concepts=%d langs=%d  ladder(n_concepts)=%s -> anchors=%s"
      % (akida.__version__, DEV.version, DEV.ip_version, len(concepts_sorted_full), len(langs),
         NCONCEPTS_LADDER, [n*len(langs) for n in NCONCEPTS_LADDER])); sys.stdout.flush()

def code_of_full(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc_full[idx[0]] if len(idx) else None

def run_one_rung(NCONC):
    concepts_sorted = concepts_sorted_full[:NCONC]
    NC = len(concepts_sorted)
    n_anchors = NC * len(langs)
    def code_of(c, l): return code_of_full(c, l)
    # teacher-forced within-lang transition stream bind(code_t, code_{t+1})
    train_codes = []
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            train_codes.append(bind(a, b))
    train_codes = np.stack(train_codes); n_train = train_codes.shape[0]
    # gen probes: bind(code_t, NEUTRAL) — NO successor info
    gen_rows, gen_inputs = [], []
    for ti in range(NC - 1):
        t = concepts_sorted[ti]
        for ql in langs:
            a = code_of(t, ql)
            if a is None: continue
            gen_rows.append((t, ql, ti)); gen_inputs.append(neutral_bind(a))
    gen_inputs = np.stack(gen_inputs)

    def build_codebook(chip_train_bin):
        cb = {}; k = 0
        for l in langs:
            for ci_ in range(NC - 1):
                a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
                if a is None or b is None: continue
                cb.setdefault(concepts_sorted[ci_ + 1], []).append(chip_train_bin[k]); k += 1
        return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}

    def gen_decode_acc(g_hat_bin, codebook):
        hit, tot = 0, 0
        cand = [c for c in concepts_sorted if c in codebook]
        for k, (t, ql, ti) in enumerate(gen_rows):
            succ = concepts_sorted[ti + 1]
            scores = [(overlap(g_hat_bin[k], codebook[c]), c) for c in cand if c != t]
            if not scores: continue
            hit += int(max(scores)[1] == succ); tot += 1
        return hit / max(1, tot), tot

    def shuffle_null(g_hat_bin, codebook, B=B_SHUFFLE, seed=SEED):
        rng = np.random.default_rng(seed)
        cand = [c for c in concepts_sorted if c in codebook]
        preds = []
        for k, (t, ql, ti) in enumerate(gen_rows):
            scores = [(overlap(g_hat_bin[k], codebook[c]), c) for c in cand if c != t]
            preds.append(max(scores)[1] if scores else None)
        null = []
        for _ in range(B):
            perm = rng.permutation(NC)
            succ_map = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
            hit, tot = 0, 0
            for k, (t, ql, ti) in enumerate(gen_rows):
                if preds[k] is None: continue
                hit += int(preds[k] == succ_map[t]); tot += 1
            null.append(hit / max(1, tot))
        return np.array(null)

    gen_list, ident_list, learn_all = [], [], True
    last_ghat, last_cb = None, None
    for tr in range(NTRIALS):
        init = get_w(build_fc(1))
        both = np.concatenate([train_codes, gen_inputs], axis=0)
        out_both, learned = fit_forward(train_codes, both, init, do_fit=True)
        out_bin = binarize(out_both)
        chip_train_bin = out_bin[:n_train]; g_hat_bin = out_bin[n_train:]
        codebook = build_codebook(chip_train_bin)
        gacc, gtot = gen_decode_acc(g_hat_bin, codebook)
        out_id, _ = fit_forward(train_codes, gen_inputs, init, do_fit=False)
        iacc, _ = gen_decode_acc(binarize(out_id), codebook)
        gen_list.append(gacc); ident_list.append(iacc); learn_all = learn_all and learned
        last_ghat, last_cb = g_hat_bin, codebook
        print("[gen-scale] NC=%d (anchors=%d) trial %d: gen_acc=%.4f identity=%.4f learn=%s (q=%d)"
              % (NC, n_anchors, tr, gacc, iacc, learned, gtot)); sys.stdout.flush()
    null = shuffle_null(last_ghat, last_cb)
    null_mean, null_sd = float(null.mean()), float(null.std()); null_hi = null_mean + 1.96*null_sd
    gm, gsd, gsem, glo, ghi = ci(gen_list)
    im, isd, isem, ilo, ihi = ci(ident_list)
    p_gen = float((null >= gm).sum() + 1) / (len(null) + 1)
    chance = 1.0/(NC - 1)
    above_shuffle = bool(learn_all and glo > null_hi and p_gen < 0.05)
    above_identity = bool(learn_all and glo > ihi)
    above_2x_chance = bool(glo >= 2.0 * chance)
    summ = {"n_concepts": NC, "n_anchors": n_anchors, "learn_all_hw": learn_all, "chance": chance,
            "gen_acc": {"mean": gm, "sd": gsd, "ci95": [glo, ghi], "ci_lo": glo},
            "identity_null": {"mean": im, "hi": ihi}, "shuffle_null": {"mean": null_mean, "sd": null_sd, "hi": null_hi, "p": p_gen, "B": B_SHUFFLE},
            "above_shuffle_null": above_shuffle, "above_identity_null": above_identity, "above_2x_chance": above_2x_chance}
    print("[gen-scale] NC=%d anchors=%d: gen ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | identNULL hi=%.4f | chance=%.4f | aboveShuf=%s aboveIdent=%s above2xChance=%s"
          % (NC, n_anchors, glo, null_hi, p_gen, ihi, chance, above_shuffle, above_identity, above_2x_chance)); sys.stdout.flush()
    return summ

RESULTS = {"substrate": "AKIDA (on-chip 1-bit Hebbian)", "rung": "SINGLE-STEP open-vocab GENERATION ANCHOR-COUNT scale ladder",
           "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "encoder": "whitened (byte-match onchip_xlm_generation.enc_whitened)",
           "metric": "gen_acc=P(argmax_{c!=t} overlap(g_hat_t, codebook[c])==t+1), open-vocab cross-lingual; shuffle-NULL B=200",
           "ladder_n_concepts": NCONCEPTS_LADDER,
           "corpus": ("corpus_big 250 anchors / 50 FLORES concepts x 5 langs (REAL cross-lingual semantic)"
                      if CORPUS_DIR == "corpus_big" else
                      "%s (SYNTHETIC distinguishable byte-pattern anchors — CHIP-CODE-CAPACITY probe past the "
                      "250-anchor real-corpus ceiling; NOT a semantic/cross-lingual claim, a_scale_honest_scope)" % CORPUS_DIR),
           "corpus_dir": CORPUS_DIR,
           "rungs": []}
print("[gen-scale] ===== ANCHOR-COUNT LADDER (a_scale_honest_scope, %d rungs) =====" % len(NCONCEPTS_LADDER)); sys.stdout.flush()
for NCONC in NCONCEPTS_LADDER:
    summ = run_one_rung(NCONC)
    RESULTS["rungs"].append(summ)
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_gen_scale.json"), "w"), indent=2)

all_above = all(r["above_shuffle_null"] for r in RESULTS["rungs"])
big = RESULTS["rungs"][-1]
F_SCALE_1 = bool(all_above)
F_SCALE_2 = bool(big["above_shuffle_null"] and big["above_2x_chance"])
RESULTS["headline"] = {
    "F_GEN_SCALE_1_holds_above_null_across_scale": (
        "REFUTED: at EVERY rung single-step gen ci_lo>shuffle-NULL hi AND p<0.05 -> single-step on-chip "
        "GENERATION SCALE-SURVIVES (A-single ceiling holds across anchor count)" if F_SCALE_1 else
        "NOT-REFUTED: at >=1 rung gen DROPS INTO shuffle-NULL -> single-step generation does NOT hold across "
        "scale at 1-bit/256-unit (CLOSED-NEGATIVE quantifying the anchor-count cap, a_paper_negative_ok)"),
    "F_GEN_SCALE_2_no_collapse_at_largest": (
        "REFUTED: largest rung gen ci_lo > shuffle-NULL hi AND >= 2x chance -> no collapse toward chance" if F_SCALE_2 else
        "NOT-REFUTED: largest rung gen collapses toward chance -> capacity cap reached at this anchor count"),
    "F_GEN_SCALE_1_pass": F_SCALE_1, "F_GEN_SCALE_2_pass": F_SCALE_2,
    "scale_survives": bool(F_SCALE_1 and F_SCALE_2),
    "ladder_gen_ci_lo": [r["gen_acc"]["ci_lo"] for r in RESULTS["rungs"]],
    "ladder_shuffle_null_hi": [r["shuffle_null"]["hi"] for r in RESULTS["rungs"]],
    "ladder_anchors": [r["n_anchors"] for r in RESULTS["rungs"]],
}
if F_SCALE_1 and F_SCALE_2:
    disp = ("SINGLE-STEP GENERATION SCALE-SURVIVES (substrate=AKIDA on-chip): across a >=3-rung anchor-count "
            "ladder the on-chip open-vocab next-step decode stays ABOVE the shuffle-NULL at every rung and does "
            "not collapse toward chance at the largest. The A-single on-chip ceiling is a SCALE-ROBUST single-step "
            "result, not a single-point artefact. STILL toy vocab (a_scale_honest_scope); production full-LM ladder "
            "separate. substrate=AKIDA, NOT HYBRID, NOT Lane G.")
else:
    disp = ("SINGLE-STEP GENERATION SCALE-CAP (a_paper_negative_ok, closed-negative): single-step on-chip "
            "generation %s as anchor count grows -> the 1-bit/256-unit on-chip ceiling is QUANTIFIED at the "
            "rung where it drops into the shuffle-NULL. Finding-either-direction valid; the anchor-count cap is "
            "now a measured number, not an assumption. substrate=AKIDA, NOT HYBRID, NOT Lane G."
            % ("HOLDS above-NULL but collapses toward chance at the largest rung" if F_SCALE_1 else "DROPS into the shuffle-NULL"))
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_gen_scale.json"), "w"), indent=2)
print("\n[gen-scale] ========== DISPOSITION ==========")
print("[gen-scale] SUBSTRATE            : AKIDA (on-chip 1-bit Hebbian)")
print("[gen-scale] ladder anchors       :", RESULTS["headline"]["ladder_anchors"])
print("[gen-scale] gen ci_lo per rung   :", [round(x,4) for x in RESULTS["headline"]["ladder_gen_ci_lo"]])
print("[gen-scale] shuffle-NULL hi/rung :", [round(x,4) for x in RESULTS["headline"]["ladder_shuffle_null_hi"]])
print("[gen-scale] F-GEN-SCALE-1        :", RESULTS["headline"]["F_GEN_SCALE_1_holds_above_null_across_scale"])
print("[gen-scale] F-GEN-SCALE-2        :", RESULTS["headline"]["F_GEN_SCALE_2_no_collapse_at_largest"])
print("[gen-scale] DISPOSITION          :", RESULTS["DISPOSITION"])
print("[gen-scale] wrote " + os.path.join(OUT, "result_onchip_xlm_gen_scale.json"))
