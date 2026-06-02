#!/usr/bin/env python3
"""Lane A P3' ENCODER-LADDER forward science on live AKD1000 (substrate=AKIDA, a_lane_akida_gpu_split).

FORWARD LINE = the P3' ENCODER axis (REOPENED 2026-06-02). The 4 downstream FIX-axes (corpus/quant/
depth/native-init H-A1..A4) are all FALSIFIED; the cause-axis battery reopened the INPUT ENCODER.
This script characterizes the encoder axis as a LADDER, on the live chip, with a >=3-rung scale guard.

PRE-REGISTERED FALSIFIERS (g63 honest, a_akida_native_train — NO sw fallback, every tier real chip):
  metric family = causeaxis concept_margin = mean_between_concept_Hamming - mean_within_concept_Hamming
                  (bits) on per-feature-median binarized on-chip forward.
  TWO readouts per (encoder,scale):
    (A) RELATIVE LIFT vs random baseline — paired N trials, SAME per-trial native chip init for treat &
        ctrl(=random_int4); lift=margin(enc)-margin(random); ci_lo=mean-1.96SEM. (causeaxis family.)
    (B) ABSOLUTE margin — native non-det chip init per trial; ci_lo=mean-1.96SEM. (abs_margin family.)
  RUNGS:
    encoder richness: random_int4 -> pca_k32 (unsupervised, dim-only) -> svd_structured (unsupervised,
                      full) -> whitened (unsupervised, decorrelated) -> lda_supervised (oracle labels).
    scale (a_scale_honest_scope, >=3 rungs): 25 / 125 / 250 anchors (125 = concept-subsample of the
                      real 250-anchor FLORES corpus_big; all rungs real text, 5 langs).
  FALSIFIER 1 (monotone vs ceiling): "encoder richness does NOT monotonically raise on-chip lift."
        -> look for a monotone RELATIVE-LIFT curve across the richness rungs vs a flat/ceiling.
  FALSIFIER 2 (scale-artifact guard): "the encoder-driven lift is a small-sample artifact that
        collapses at scale." -> the prior weak-positive WAS a 25-anchor artifact (H-A1). A positive
        that holds (or grows) 25->125->250 survives; one that collapses is a closed result, reported
        plainly.
  FALSIFIER 3 (which property): "supervision (LDA labels) is REQUIRED — unsupervised richness ceilings."
        -> compare pca/svd/whitened (unsupervised) vs lda (supervised); if only lda crosses zero
        absolute, supervision is the necessary property; if an unsupervised rung also crosses, it is not.
  REOPEN/PASS iff relative-lift ci_lo>0 at >=1 rung (learn_all_hw); ABSOLUTE PASS iff abs ci_lo>0.
  Disposition is a MATRIX (richness x scale x {relative,absolute}); honest monotone-vs-ceiling +
  property finding; a ceiling/collapse is a valid closed result (a_paper_negative_ok).
"""
import os, json, struct, time, sys, hashlib
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
N_LANGS = 5
NTRIALS = 8
UNITS, NW, LCOMP = 32, 8, 0.1
PCA_K = 32

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

# ---- ENCODERS (random/svd/whitened/lda byte-match causeaxis_chip.py + abs_margin_chip.py) ----
def enc_random_int4(H, seed=20260602):
    rng = np.random.default_rng(seed)
    BB = rng.integers(-7, 8, size=(INC, INC), dtype=np.int8).astype(np.int32)
    proj = H.astype(np.int32) @ BB.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def enc_pca_k(H, k=PCA_K):
    # UNSUPERVISED dimensionality-only: top-k PCA axes (no labels), int4-quantized projection.
    # Isolates the DIMENSIONALITY/low-rank property from full-rank svd & from supervision.
    Hc = H - H.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Hc, full_matrices=False)
    P = np.zeros((INC, INC)); P[:min(k, Vt.shape[0]), :] = Vt[:min(k, Vt.shape[0]), :]
    scale = 7.0/(np.max(np.abs(P))+1e-12)
    Pq = np.clip(np.round(P*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def enc_svd(H):
    Hc = H - H.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Hc, full_matrices=False)
    k = Vt.shape[0]; P = np.zeros((INC, INC)); P[:k, :] = Vt
    scale = 7.0/(np.max(np.abs(P))+1e-12)
    Pq = np.clip(np.round(P*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def enc_whitened(H):
    Hc = H - H.mean(axis=0, keepdims=True)
    cov = (Hc.T @ Hc)/max(1, Hc.shape[0]-1) + 1e-3*np.eye(INC)
    w, V = np.linalg.eigh(cov)
    W = V @ np.diag(1.0/np.sqrt(np.maximum(w,1e-9))) @ V.T
    scale = 7.0/(np.max(np.abs(W))+1e-12)
    Pq = np.clip(np.round(W*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def enc_lda_supervised(H, concept):
    Hc = H - H.mean(axis=0, keepdims=True)
    classes = np.unique(concept); mu = Hc.mean(axis=0)
    Sw = np.zeros((INC, INC)); Sb = np.zeros((INC, INC))
    for c in classes:
        Xc = Hc[concept == c]; muc = Xc.mean(axis=0)
        Sw += (Xc - muc).T @ (Xc - muc)
        nc = Xc.shape[0]; d = (muc - mu).reshape(-1,1); Sb += nc * (d @ d.T)
    Sw += 1e-2*np.eye(INC)
    evals, evecs = np.linalg.eig(np.linalg.solve(Sw, Sb))
    order = np.argsort(-evals.real); Wlda = evecs[:, order].real
    P = Wlda.T
    scale = 7.0/(np.max(np.abs(P))+1e-12)
    Pq = np.clip(np.round(P*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

# richness rungs, low->high
ENC_LADDER = [
    ("random_int4",   lambda H, c: enc_random_int4(H),     "baseline: fixed random int4 backbone"),
    ("pca_k32",       lambda H, c: enc_pca_k(H, PCA_K),     "unsupervised dim-only: top-32 PCA axes"),
    ("svd_struct",    lambda H, c: enc_svd(H),              "unsupervised full: SVD structured basis"),
    ("whitened",      lambda H, c: enc_whitened(H),         "unsupervised decorrelated: covariance whitening"),
    ("lda_supervised",lambda H, c: enc_lda_supervised(H,c), "supervised oracle: multi-class LDA (uses labels)"),
]

def build_fc(wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1,1,INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

def concept_margin_from_binary(fb, concept):
    n = fb.shape[0]; within, between = [], []
    for i in range(n):
        for j in range(i+1, n):
            d = int(np.count_nonzero(fb[i] != fb[j]))
            (within if concept[i]==concept[j] else between).append(d)
    return (float(np.mean(between)) - float(np.mean(within)))

def margin_post1bit(out2d, concept):
    fb = (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
    return concept_margin_from_binary(fb, concept)

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]

def to_chip(Xb, count): return Xb.astype(np.uint8).reshape(count,1,1,INC)

def fit_forward(X, init_w):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    learned = bool(np.any(post != pre))
    del m
    return out, learned

def ci(arr):
    arr = np.array(arr); mean=float(arr.mean()); sd=float(arr.std(ddof=1))
    sem=sd/np.sqrt(len(arr)); return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

def ladder_one_scale(corpus_name, count, concept, H):
    """For each richness rung: paired RELATIVE lift vs random (same per-trial init) + ABSOLUTE margin."""
    print("\n[ladder] ===== SCALE %s count=%d concepts=%d langs=%d =====" % (corpus_name, count, len(np.unique(concept)), N_LANGS)); sys.stdout.flush()
    ENCX = {name: to_chip(fn(H, concept), count) for (name, fn, _) in ENC_LADDER}
    rows = {}
    for (name, _, desc) in ENC_LADDER:
        rel_lifts, abs_margins, learn_all = [], [], True
        for t in range(NTRIALS):
            init = get_w(build_fc(1))            # native chip init; shared by treat & random ctrl this trial
            te, lt = fit_forward(ENCX[name], init)
            tm = margin_post1bit(te, concept)
            if name == "random_int4":
                cm = tm                          # baseline vs itself -> lift 0 by construction; abs is the signal
            else:
                co, lc = fit_forward(ENCX["random_int4"], init)
                cm = margin_post1bit(co, concept); learn_all = learn_all and lc
            rel_lifts.append(tm - cm); abs_margins.append(tm); learn_all = learn_all and lt
            print("[ladder] %-14s %-10s trial %d: abs=%+.4f rel_lift=%+.4f learn=%s" % (corpus_name, name, t, tm, tm-cm, lt)); sys.stdout.flush()
        rm, rsd, rsem, rlo, rhi = ci(rel_lifts)
        am, asd, asem, alo, ahi = ci(abs_margins)
        rows[name] = {"desc": desc, "n_trials": NTRIALS,
            "rel_lift": {"mean": rm, "sd": rsd, "sem": rsem, "ci95": [rlo, rhi], "ci_lo": rlo,
                         "n_positive": int((np.array(rel_lifts)>0).sum()), "lifts": rel_lifts,
                         "REOPEN": bool(learn_all and rlo>0)},
            "abs_margin": {"mean": am, "sd": asd, "sem": asem, "ci95": [alo, ahi], "ci_lo": alo,
                           "n_positive": int((np.array(abs_margins)>0).sum()), "margins": abs_margins,
                           "CROSSES_ZERO": bool(learn_all and alo>0)},
            "learn_all_hw": learn_all}
        print("[ladder] %-14s %-14s REL mean=%+.4f ci_lo=%+.4f REOPEN=%s | ABS mean=%+.4f ci_lo=%+.4f CROSS=%s"
              % (corpus_name, name, rm, rlo, rows[name]["rel_lift"]["REOPEN"], am, alo, rows[name]["abs_margin"]["CROSSES_ZERO"])); sys.stdout.flush()
        json.dump(RESULTS, open(os.path.join(OUT, "result_encoder_ladder.json"), "w"), indent=2)  # commit-early
    # monotonicity of the relative lift across the richness ladder (Spearman of mean-lift vs rung index)
    order = [n for (n,_,_) in ENC_LADDER]
    lift_curve = [rows[n]["rel_lift"]["mean"] for n in order]
    abs_curve  = [rows[n]["abs_margin"]["mean"] for n in order]
    ranks = np.argsort(np.argsort(lift_curve))
    idx = np.arange(len(order))
    rho = float(np.corrcoef(idx, ranks)[0,1]) if len(order)>1 else 0.0
    return {"rows": rows, "encoder_order": order, "rel_lift_curve": lift_curve,
            "abs_margin_curve": abs_curve, "richness_rank_spearman": rho,
            "monotone_increasing": bool(rho > 0.5),
            "any_rel_reopen": any(rows[n]["rel_lift"]["REOPEN"] for n in order),
            "any_abs_crosses": any(rows[n]["abs_margin"]["CROSSES_ZERO"] for n in order),
            "unsupervised_crosses": any(rows[n]["abs_margin"]["CROSSES_ZERO"] for n in order if n!="lda_supervised"),
            "lda_crosses": rows["lda_supervised"]["abs_margin"]["CROSSES_ZERO"]}

# ---- build the 3 scale rungs: 25(corpus) / 125(subsample of corpus_big) / 250(corpus_big) ----
def load_scale(name):
    path = os.path.join(ROOT, name, "parallel.limen")
    count, recs = read_limen(path)
    concept = np.array([h["concept"] for (h, _) in recs])
    H = np.stack([byte_hist(p) for (_, p) in recs])
    return count, concept, H, recs

c25, k25, H25, _ = load_scale("corpus")
c250, k250, H250, recs250 = load_scale("corpus_big")
# 125-anchor rung: first 25 concepts of corpus_big (real FLORES, 25 concepts x 5 langs), preserving order
keep_concepts = sorted(np.unique(k250))[:25]
mask = np.isin(k250, keep_concepts)
H125 = H250[mask]; k125 = k250[mask]; c125 = int(mask.sum())
mid_sha = hashlib.sha256(H125.tobytes()).hexdigest()
print("[ladder] scale rungs: 25 (corpus) / %d (corpus_big[:25concept] sha %s) / %d (corpus_big)" % (c125, mid_sha[:12], c250)); sys.stdout.flush()

RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "metric": "causeaxis concept_margin (between-minus-within Hamming bits) on per-feature-median binarized on-chip fwd; "
                     "RELATIVE lift=margin(enc)-margin(random) paired same-init; ABSOLUTE=margin(enc) native-init; ci_lo=mean-1.96SEM over chip trials",
           "encoder_ladder": [n for (n,_,_) in ENC_LADDER],
           "scale_rungs": {"c25": c25, "c125": c125, "c250": c250, "c125_sha256": mid_sha},
           "scales": {}}
print("[ladder] akida %s device %s ip %s N=%d trials units=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS)); sys.stdout.flush()

RESULTS["scales"]["c25"]  = ladder_one_scale("c25",  c25,  k25,  H25)
json.dump(RESULTS, open(os.path.join(OUT, "result_encoder_ladder.json"), "w"), indent=2)
RESULTS["scales"]["c125"] = ladder_one_scale("c125", c125, k125, H125)
json.dump(RESULTS, open(os.path.join(OUT, "result_encoder_ladder.json"), "w"), indent=2)
RESULTS["scales"]["c250"] = ladder_one_scale("c250", c250, k250, H250)
json.dump(RESULTS, open(os.path.join(OUT, "result_encoder_ladder.json"), "w"), indent=2)

# ---- disposition matrix ----
def best_abs(scale):
    rows = RESULTS["scales"][scale]["rows"]; order = RESULTS["scales"][scale]["encoder_order"]
    b = max(order, key=lambda n: rows[n]["abs_margin"]["mean"])
    return b, rows[b]["abs_margin"]["mean"], rows[b]["abs_margin"]["ci_lo"], rows[b]["abs_margin"]["CROSSES_ZERO"]

mono = {s: RESULTS["scales"][s]["monotone_increasing"] for s in ["c25","c125","c250"]}
rho  = {s: RESULTS["scales"][s]["richness_rank_spearman"] for s in ["c25","c125","c250"]}
any_rel = any(RESULTS["scales"][s]["any_rel_reopen"] for s in RESULTS["scales"])
any_abs = any(RESULTS["scales"][s]["any_abs_crosses"] for s in RESULTS["scales"])
unsup_cross = {s: RESULTS["scales"][s]["unsupervised_crosses"] for s in ["c25","c125","c250"]}
lda_cross   = {s: RESULTS["scales"][s]["lda_crosses"] for s in ["c25","c125","c250"]}

# scale-survival: does the best absolute margin grow (not collapse) 25->125->250 ?
best_curve = [best_abs(s)[1] for s in ["c25","c125","c250"]]
scale_survives = bool(best_curve[2] >= best_curve[0])   # holds/grows from smallest to largest
monotone_richness_all = all(mono.values())

RESULTS["disposition"] = {
    "richness_monotone_increasing_per_scale": mono,
    "richness_rank_spearman_per_scale": rho,
    "any_relative_reopen": any_rel,
    "any_absolute_crosses_zero": any_abs,
    "unsupervised_crosses_zero": unsup_cross,
    "lda_supervised_crosses_zero": lda_cross,
    "best_abs_margin_curve_25_125_250": best_curve,
    "scale_survives_not_artifact": scale_survives,
    "FALSIFIER_1_monotone": "monotone-CONFIRMED" if monotone_richness_all else "ceiling-or-nonmonotone (F1 not fully cleared)",
    "FALSIFIER_2_scale": "scale-survives (NOT a small-sample artifact)" if scale_survives else "scale-collapse (small-sample artifact, closed-result)",
    "FALSIFIER_3_property": ("supervision-REQUIRED (only LDA crosses zero; unsupervised richness ceilings)"
        if (lda_cross["c250"] and not unsup_cross["c250"]) else
        ("unsupervised-SUFFICIENT (an unsupervised encoder also crosses zero)"
         if unsup_cross["c250"] else "no-cross-at-largest-scale (encoder axis ceilings absolute)")),
}
RESULTS["bottom_line"] = (
    "ENCODER AXIS = real PUBLIC-grade path forward" if (any_abs and scale_survives)
    else "ENCODER AXIS = relative lift only / characterized ceiling on absolute margin")
json.dump(RESULTS, open(os.path.join(OUT, "result_encoder_ladder.json"), "w"), indent=2)

print("\n[ladder] ========== DISPOSITION ==========")
for s in ["c25","c125","c250"]:
    b = best_abs(s); sc = RESULTS["scales"][s]
    print("[ladder] %-5s monotone_rho=%+.3f any_rel_reopen=%s best_abs=%s mean=%+.4f ci_lo=%+.4f cross=%s"
          % (s, sc["richness_rank_spearman"], sc["any_rel_reopen"], b[0], b[1], b[2], b[3]))
print("[ladder] F1 monotone:", RESULTS["disposition"]["FALSIFIER_1_monotone"])
print("[ladder] F2 scale   :", RESULTS["disposition"]["FALSIFIER_2_scale"])
print("[ladder] F3 property:", RESULTS["disposition"]["FALSIFIER_3_property"])
print("[ladder] BOTTOM LINE:", RESULTS["bottom_line"])
print("[ladder] wrote " + os.path.join(OUT, "result_encoder_ladder.json"))
