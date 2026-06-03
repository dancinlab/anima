#!/usr/bin/env python3
"""Lane A FULL-LM MULTI-STEP ROLLOUT RUNG — autoregressive on-chip generation, K>=3 chained hops on live AKD1000.

substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope.

WHERE WE ARE (the named gap, verbatim from the frontier):
  The GENERATION rung (onchip_xlm_generation.py, result_onchip_xlm_generation.json, verdict
  .verdicts/lane-a-generation/F-GEN.txt) PROVED a SINGLE on-chip open-vocab next-step generation:
  feed bind(code_t, NEUTRAL) -> the chip PRODUCES g_hat -> open-vocab decode over the FULL codebook beats
  BOTH the shuffle-NULL (gen ci_lo=0.4096 >> shuffle hi=0.0418, p=0.005, F-GEN-1 REFUTED) AND the
  identity-NULL echo (gen > id hi=0.3847, F-GEN-2 REFUTED). That is ONE hop: t -> t+1. A full LM must
  CHAIN: t -> t+1 -> t+2 -> ... feeding its OWN produced code back as the next input. The single-step
  rung explicitly held "multi-step roll-out UNVERIFIED" and did NOT flip the PUBLIC checkbox.

THIS RUNG (autoregressive rollout — does single-step generation COMPOUND or COLLAPSE on-chip?):
  Chain the EXACT generation path for K>=3 steps, fully on AKD1000, re-encoding each produced successor
  through the SAME trained 1-bit FC (NO GPU, NO sw fallback labelled on-chip, g63):
    step 0: x_0 = neutral_bind(code_t)            (the seed gen-input, identical to the gen rung)
    each k: g_hat_k = binarize(chip.forward(x_k))  (chip PRODUCES the predicted-successor code)
            pred_{k+1} = argmax_{c != banned} overlap(g_hat_k, codebook[c])  (open-vocab decode, FULL codebook)
            x_{k+1} = neutral_bind(g_hat_k)        (FEED the chip's OWN produced code back -> autoregress)
  The training (teacher-forced within-lang transition stream bind(code_t, code_{t+1})), encoder
  (enc_whitened, byte-match), binding (SHIFT=37), neutral_bind, codebook (successor-centroid in produced-code
  space), and decode are ALL byte-identical to onchip_xlm_generation.py. The ONLY new thing is the FEEDBACK
  LOOP: the chip's produced code becomes the next step's input. This is the core full-LM question —
  does the trajectory stay on-manifold for k=1..K or drift to noise after one autoregressive hop?

  Ground truth for hop k from seed concept t (index ti): gt_k = concept[ti + k] (within-lang sequential FLORES
  successor chain). A hop is a HIT iff the open-vocab decoded prediction == gt_k. We roll only from seeds with
  >= K real successors (ti <= NC-1-K) so every hop has a defined ground truth.

  DECODE BAN-SET (honest, no free wins): at each hop we ban the CURRENT decoded concept (the chip's own last
  prediction) from being re-predicted, matching the gen rung's c != t exclusion generalised to the rollout
  (you cannot trivially re-emit the token you just emitted). We do NOT ban the true successor.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: ROLL acc at hop k = P(open-vocab argmax decode of the AUTOREGRESSIVE g_hat at hop k == gt_k),
          over all (seed t, query-lang) rollout starts, k = 1..K. step-1 == the gen rung's single-step acc
          (sanity: must reproduce the gen-rung headline within trial noise).
  NULL-A (SHUFFLE), per hop k: the SAME hop-k decode with the (seed -> gt_k) successor labels permuted (B=200),
          breaking temporal adjacency, geometry preserved. mean +- sd + empirical p, computed INDEPENDENTLY
          per hop (a hop is "above-NULL" iff that hop's roll acc ci_lo > that hop's shuffle-NULL hi AND p<0.05).
  NULL-B (IDENTITY) per hop: roll the SAME feedback chain through an UNTRAINED (do_fit=False) FC -> if a hop's
          roll acc is at the identity-NULL, the chip at that hop is echoing its input, not producing a successor.
  CHANCE line: 1/(NC-1) (open-vocab uniform).
  FALSIFIER F-ROLL-1 (signal-survives-chaining, the headline): "the K-step autoregressive rollout acc at hop k
          does NOT stay above the shuffle-NULL for every k=1..K." -> REFUTED iff for ALL k in 1..K,
          roll_acc[k] ci_lo > shuffle_null[k] hi AND p[k] < 0.05. (i.e. the on-manifold signal SURVIVES K hops.)
  FALSIFIER F-ROLL-2 (no-catastrophic-collapse): "rollout collapses to chance by hop 2-3 (per-step degradation
          is catastrophic)." -> REFUTED iff roll_acc[K] ci_lo > chance AND roll_acc[K] >= 0.5 * roll_acc[1]
          (final hop retains >= half the single-step acc AND is above chance). HONEST: we ALWAYS report the
          full decay curve roll_acc[1..K], the per-hop chance line, the per-hop shuffle-NULL and identity-NULL,
          regardless of disposition.

DISPOSITION (a_paper_negative_ok — a clean COLLAPSE is a VALID closed-negative, NOT forced green):
  ALL hops above-NULL AND no catastrophic collapse -> AUTOREGRESSIVE ROLLOUT HOLDS on-chip (the produced code
    stays on-manifold when fed back); Lane A full-LM (multi-step) axis advances toward earned-green (still toy).
  step-1 above-NULL but signal lost by hop k (drops into shuffle-NULL OR collapses to chance) -> ROLLOUT
    COLLAPSE closed-negative: single-step generation works but does NOT compound under autoregression at
    1-bit/256-unit capacity -> QUANTIFIES the K at which the chain drifts to noise; NAMES the next bridge
    (paged/state-carrying generator, multi-FC depth, off-chip decode). Retrieval+single-step rungs UNAFFECTED.
  NO fabricated PUBLIC. NO sw fallback labelled on-chip. a_scale_honest_scope: toy 250-anchor / single FC.
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
UNITS, NW, LCOMP = 256, 8, 0.1     # byte-match generation rung
SHIFT = 37                          # byte-match onchip_xlm_generation / onchip_xlm_transition
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3                          # autoregressive hops (>=3, the held next-step question)
SEED = 20260602

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

# ---- PROVEN whitened encoder (byte-match onchip_xlm_generation.enc_whitened) ----
def enc_whitened(H):
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
    """test-time input with NO successor info — byte-match onchip_xlm_generation.neutral_bind."""
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

def chip_make(init_w, train_codes, do_fit=True):
    """map()+fit() ON CHIP, return a LIVE mapped model the rollout drives forward step-by-step."""
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    if do_fit:
        Xt = to_chip(train_codes)
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    learned = bool(np.any(post != pre))
    return m, learned

def chip_forward(m, Xb):
    Xe = to_chip(Xb)
    return np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])

def binarize_rows(out2d, med):
    """binarize against a FIXED per-feature median (computed once on the train-forward batch — byte-match the
    gen rung's column-median, but frozen so each autoregressive hop uses the SAME threshold)."""
    return (out2d > med[None, :]).astype(np.uint8)

def overlap(a_bin, b_soft):
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))

def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

# ---- load corpus_big: 250 anchors, 50 concepts x 5 langs ----
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC = len(concepts_sorted)
print("[roll] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d K=%d" % (count, NC, len(langs), SHIFT, UNITS, K_ROLL)); sys.stdout.flush()

codes_enc = enc_whitened(H)

def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None

# ---- TRAIN: teacher-forced within-lang transition stream bind(code_t, code_{t+1}) (byte-match gen rung) ----
train_codes, train_succ = [], []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b)); train_succ.append(concepts_sorted[ci_ + 1])
train_codes = np.stack(train_codes)
n_train = train_codes.shape[0]
print("[roll] teacher-forced train transitions=%d" % n_train); sys.stdout.flush()

# ---- ROLLOUT seeds: (seed-concept ti, query-lang). only seeds with >=K real successors (ti <= NC-1-K). ----
roll_starts = []   # (ti, ql, seed_code)
for ti in range(NC - K_ROLL):
    t = concepts_sorted[ti]
    for ql in langs:
        a = code_of(t, ql)
        if a is None: continue
        roll_starts.append((ti, ql, a))
print("[roll] rollout starts (>=%d real successors)=%d" % (K_ROLL, len(roll_starts))); sys.stdout.flush()

def build_codebook(chip_train_bin):
    cb = {}; k = 0
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            cb.setdefault(concepts_sorted[ci_ + 1], []).append(chip_train_bin[k]); k += 1
    return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}

def decode(g_hat_bin_row, codebook, ban):
    cand = [c for c in codebook if c != ban]
    scores = [(overlap(g_hat_bin_row, codebook[c]), c) for c in cand]
    return max(scores)[1] if scores else None

def rollout_chip(m, codebook, med, do_decode=True):
    """drive the LIVE chip autoregressively for K hops over every rollout start.
    returns preds[k] = list of (ti, ql, decoded_concept) per start, k=1..K (1-indexed list len K)."""
    preds = [[] for _ in range(K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        x = neutral_bind(seed_code)
        banned = concepts_sorted[ti]  # cannot trivially re-emit the seed token at hop 1
        for k in range(K_ROLL):
            g_soft = chip_forward(m, x)              # (1,256)
            g_bin = binarize_rows(g_soft, med)[0]    # (256,) frozen-threshold binarize
            pred = decode(g_bin, codebook, banned) if do_decode else None
            preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            x = neutral_bind(g_bin)                  # FEED produced code back -> autoregress
    return preds

def acc_at(preds, k0):
    """0-indexed hop k0 (=> ground truth concept[ti + k0 + 1]). returns acc, n."""
    hit, tot = 0, 0
    for (ti, ql, pred) in preds[k0]:
        if pred is None: continue
        gt = concepts_sorted[ti + k0 + 1]
        hit += int(pred == gt); tot += 1
    return hit / max(1, tot), tot

def shuffle_null_at(preds, k0, B=B_SHUFFLE, seed=SEED):
    """permute the (seed-concept -> gt) successor mapping for hop k0; decode preds fixed (label-independent)."""
    rng = np.random.default_rng(seed + 1009 * (k0 + 1))
    null = []
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (ti, ql, pred) in preds[k0]:
            if pred is None: continue
            # shuffled ground truth for this seed at this hop
            hit += int(pred == smap[concepts_sorted[ti]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "K_roll": K_ROLL,
           "binding": "bind(a,b)=a XOR roll(b,%d); neutral=a XOR roll(a,%d); feedback x_{k+1}=neutral_bind(g_hat_k)" % (SHIFT, NEUTRAL_ROLL),
           "encoder": "whitened (byte-match onchip_xlm_generation.enc_whitened)",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "task": "AUTOREGRESSIVE on-chip ROLLOUT: K-hop chained generation, chip's produced code fed back as next input; "
                   "open-vocab decode (full codebook, NO shortlist) per hop; per-hop shuffle-NULL + identity-NULL",
           "metric": "roll_acc[k]=P(open-vocab decode of autoregressive g_hat at hop k == concept[ti+k]), k=1..K",
           "trials": []}
print("[roll] akida %s device %s ip %s N=%d trials units=%d K=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS, K_ROLL)); sys.stdout.flush()

# per-trial per-hop accuracies (trained + identity), plus the last-trial preds for the NULLs
roll_trials = [[] for _ in range(K_ROLL)]   # roll_trials[k0] = list over trials
ident_trials = [[] for _ in range(K_ROLL)]
learn_all = True
last_preds, last_id_preds = None, None

for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    # trained chip: fit, build codebook + frozen binarize-median from the train forward
    m, learned = chip_make(init, train_codes, do_fit=True)
    train_soft = chip_forward(m, train_codes)
    med = np.median(train_soft, axis=0)
    chip_train_bin = binarize_rows(train_soft, med)
    codebook = build_codebook(chip_train_bin)
    preds = rollout_chip(m, codebook, med, do_decode=True)
    del m
    # identity control: SAME feedback rollout through an UNTRAINED FC, decode vs the TRAINED codebook
    mid, _ = chip_make(init, train_codes, do_fit=False)
    id_train_soft = chip_forward(mid, train_codes)   # untrained forward, only for a consistent median frame
    id_med = np.median(id_train_soft, axis=0)
    id_preds = rollout_chip(mid, codebook, id_med, do_decode=True)
    del mid
    learn_all = learn_all and learned
    trial_row = {"trial": tr, "learned_hw": learned, "roll_acc": [], "identity_acc": [], "n_q": []}
    for k0 in range(K_ROLL):
        ra, n = acc_at(preds, k0); ia, _ = acc_at(id_preds, k0)
        roll_trials[k0].append(ra); ident_trials[k0].append(ia)
        trial_row["roll_acc"].append(ra); trial_row["identity_acc"].append(ia); trial_row["n_q"].append(n)
    RESULTS["trials"].append(trial_row)
    last_preds, last_id_preds = preds, id_preds
    print("[roll] trial %d: roll_acc(k1..K)=%s identity=%s learn=%s" %
          (tr, ["%.4f" % x for x in trial_row["roll_acc"]], ["%.4f" % x for x in trial_row["identity_acc"]], learned)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_rollout.json"), "w"), indent=2)

chance = 1.0/(NC - 1)
per_hop = []
print("[roll] computing per-hop shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
all_above_null = True
for k0 in range(K_ROLL):
    rm, rsd, rsem, rlo, rhi = ci(roll_trials[k0])
    im, isd, isem, ilo, ihi = ci(ident_trials[k0])
    null = shuffle_null_at(last_preds, k0, B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= rm).sum() + 1) / (len(null) + 1)
    above_shuf = bool(learn_all and rlo > nhi and p < 0.05)
    above_id = bool(learn_all and rlo > ihi)
    all_above_null = all_above_null and above_shuf
    per_hop.append({"hop": k0 + 1,
                    "roll_acc": {"mean": rm, "sd": rsd, "ci_lo": rlo, "ci_hi": rhi},
                    "identity_null": {"mean": im, "hi": ihi},
                    "shuffle_null": {"mean": nmean, "sd": nsd, "hi": nhi, "p_value": p, "B": B_SHUFFLE},
                    "chance": chance, "above_shuffle_null": above_shuf, "above_identity_null": above_id})
    print("[roll] hop %d: roll=%.4f ci_lo=%.4f | shuffle hi=%.4f p=%.4f | identity hi=%.4f | chance=%.4f | aboveShuf=%s aboveId=%s"
          % (k0 + 1, rm, rlo, nhi, p, ihi, chance, above_shuf, above_id)); sys.stdout.flush()

roll1 = per_hop[0]["roll_acc"]["mean"]
rollK = per_hop[-1]["roll_acc"]
F_ROLL_1 = bool(all_above_null)   # every hop above shuffle-NULL
no_collapse = bool(rollK["ci_lo"] > chance and rollK["mean"] >= 0.5 * roll1)
F_ROLL_2 = no_collapse

RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "K_roll": K_ROLL,
    "decay_curve_roll_acc": [round(per_hop[k]["roll_acc"]["mean"], 4) for k in range(K_ROLL)],
    "per_hop": per_hop,
    "F_ROLL_1_signal_survives_chaining": (
        "REFUTED: autoregressive rollout stays ABOVE shuffle-NULL for ALL hops k=1..%d "
        "(every hop ci_lo>NULL hi AND p<0.05) -> the produced code stays on-manifold under feedback" % K_ROLL
        if F_ROLL_1 else
        "NOT-REFUTED: the K-step rollout DROPS INTO the shuffle-NULL at some hop -> autoregressive signal does "
        "NOT survive chaining at 1-bit/%d-unit (CLOSED-NEGATIVE: single-step works, rollout drifts to noise)" % UNITS),
    "F_ROLL_2_no_catastrophic_collapse": (
        "REFUTED: final-hop acc above chance AND >= 0.5x the single-step acc -> no catastrophic collapse "
        "(degradation bounded across %d hops)" % K_ROLL
        if F_ROLL_2 else
        "NOT-REFUTED: rollout COLLAPSES by hop %d (final acc <= chance OR < half the single-step acc) -> "
        "catastrophic autoregressive decay at this scale (a_paper_negative_ok)" % K_ROLL),
    "F_ROLL_1_pass": F_ROLL_1, "F_ROLL_2_pass": F_ROLL_2,
    "rollout_holds": bool(F_ROLL_1 and F_ROLL_2),
}
if F_ROLL_1 and F_ROLL_2:
    disp = ("AUTOREGRESSIVE ROLLOUT HOLDS on-chip (all %d hops above-NULL, no catastrophic collapse) -> the "
            "chip's produced code stays on-manifold when fed back; Lane A full-LM (multi-step) advances toward "
            "earned-green (STILL toy 250-anchor / single 1-bit/%d-unit FC; PUBLIC checkbox NOT flipped)" % (K_ROLL, UNITS))
elif per_hop[0]["above_shuffle_null"] and not (F_ROLL_1 and F_ROLL_2):
    disp = ("ROLLOUT COLLAPSE closed-negative (a_paper_negative_ok): single-step generation works (hop-1 above "
            "shuffle+identity NULL) but does NOT compound under autoregression at 1-bit/%d-unit — the chained "
            "produced code drifts off-manifold. Decay curve QUANTIFIES the K at which signal is lost; NAMES next "
            "bridge = state-carrying/paged generator or off-chip decode. Retrieval+single-step rungs UNAFFECTED "
            "(a_lane_akida_gpu_split: Lane A on-chip)." % UNITS)
else:
    disp = ("ROLLOUT CLOSED-NEGATIVE at this scale (a_paper_negative_ok): even hop-1 fails to clear the NULL in "
            "this run -> re-check seed/threshold; honest decay curve reported. Lane A on-chip, toy scale.")
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_rollout.json"), "w"), indent=2)

print("\n[roll] ========== DISPOSITION ==========")
print("[roll] learn_all_hw       :", learn_all)
print("[roll] chance             : %.4f  K=%d" % (chance, K_ROLL))
print("[roll] decay curve (k1..K):", ["%.4f" % per_hop[k]["roll_acc"]["mean"] for k in range(K_ROLL)])
for k0 in range(K_ROLL):
    h = per_hop[k0]
    print("[roll] hop %d  roll=%.4f ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | idNULL hi=%.4f | aboveShuf=%s aboveId=%s"
          % (h["hop"], h["roll_acc"]["mean"], h["roll_acc"]["ci_lo"], h["shuffle_null"]["hi"],
             h["shuffle_null"]["p_value"], h["identity_null"]["hi"], h["above_shuffle_null"], h["above_identity_null"]))
print("[roll] F-ROLL-1 survives  :", RESULTS["summary"]["F_ROLL_1_signal_survives_chaining"])
print("[roll] F-ROLL-2 no-collapse:", RESULTS["summary"]["F_ROLL_2_no_catastrophic_collapse"])
print("[roll] DISPOSITION        :", RESULTS["DISPOSITION"])
print("[roll] wrote " + os.path.join(OUT, "result_onchip_xlm_rollout.json"))
