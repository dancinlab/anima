"""
H_1192 — the FIRST real "summer training" run: de-toy the H_1187 saccadic-reading
GREEN by swapping its order-4 COUNT n-gram for a REAL TRAINED next-byte predictor
(a numpy MLP trained by SGD), and re-running the H_1187 saccadic-reading test
VERBATIM with the trained model's surprise. Runs on the SUMMER pool host (CPU
linux, python3.12 + numpy); $0 (no GPU rent — production-GPU a_train_flame_forge is
a LATER escalation, this is the toy→small CPU bridge).

WHY (the user asked "when do we train on summer?" — the answer is NOW, this run is
it): H_1187 (MITOSIS-ENGINE 🟢 SACCADIC-READING-HOLDS) found that a LEARNED-surprise
gate (skip predictable bytes, fixate on informative ones = a saccade) beats a
uniform metronome scan on real-text stage-decode AND is temporally grounded
(killed by a time-shuffle): K*=24, d_real=+1.015, drop=+0.512. BUT its "learned"
reader was a Laplace-smoothed order-4 COUNT n-gram — a memorized look-up table,
the WEAKEST possible "learned" predictor. a_toy_scale_recheck demands the next
rung: does the result SURVIVE a GENUINE TRAINED model (gradient-descended weights,
generalizing parameters, not a count table)? If yes, the saccadic-reading finding
de-toys one rung. If no, the n-gram green was a count-table artifact (a_paper_negative_ok).

THE TRAINED READER ($0 CPU, real SGD — this IS the "학습"/training): a one-hidden-
layer numpy MLP. Context = the last K_ORDER bytes, one-hot encoded (K_ORDER*256
inputs) → tanh hidden (H_HID units) → softmax over 256 next-byte classes. Trained
by minibatch SGD with cross-entropy loss on the HELD-OUT first half of the corpus
(NOT the test span make_text_stream reads), for N_EPOCHS epochs. We REPORT the
train-loss curve + a not-degenerate check (loss must DROP meaningfully below the
uniform log2(256)=8-bit baseline, and the model must beat a unigram baseline on a
val split). The model's loss is NOT the verdict (p7) — the verdict is STAGE-DECODE,
exactly the H_1187/H_1163 metric. The trained model is a genuine step UP from the
count table: shared hidden features across contexts, gradient-learned, generalizing.

surprise[t] = −log2 P_model(byte_t | last K_ORDER bytes) from the TRAINED MLP on the
test span, position-aligned to make_text_stream's `start` EXACTLY as H_1187 (anchor
to data[p], p = start + i*STRIDE, conditioned on the preceding K_ORDER bytes).

SUBSTRATE REUSE (VERBATIM): H_1163 (imported as H) supplies grow_arm METRONOME arm /
stage_decode_accuracy / cohen_d_paired / make_text_stream / SEEDS / N_STAGES_TEXT /
WARMUP / T / DIM / CORPUS / WIN_BYTES / STRIDE. H_1187 (imported as R) supplies
grow_arm_surprise (the surprise-gated DERIVATIVE arm), the cap ladder, the eval +
time-shuffle protocol, SURPRISE_SIGMA, SURPRISE_REFRAC, HELDOUT_FRAC, corpus_bytes,
the position-aligned surprise track — ALL reused VERBATIM; the ONLY swap is the
SURPRISE SOURCE: H_1187's NgramReader.surprise → this file's trained-MLP surprise.
The saccadic-reading test, the metronome baseline, the K* cap ladder, the
time-shuffle are byte-identical to H_1187.

FROZEN FALSIFIER (pre-registered BEFORE measuring; do NOT move — SAME bars as
H_1187; metric = STAGE-DECODE accuracy, p7, NOT the model's loss):
  Find K* = argmax over the cap ladder R.CAP_LADDER of
    d_surprise_vs_metro = cohen_d_paired(decode_surprise, decode_metro)  (text's own cap).
  F1 SACCADIC-WINS : d_surprise_vs_metro(K*) >= 0.5.
  F2 TEMPORAL      : drop = d_real − d_shuf >= 0.5 at K* (advantage destroyed by a
                     seeded time-shuffle = genuinely temporal).
  SUPPORTED (SACCADIC-READING-HOLDS-AT-LESS-TOY-SCALE) iff F1 AND F2 — a REAL
  TRAINED reader (not a toy count n-gram) reproduces H_1187's saccadic-reading
  result, de-toying it one rung. Else CLOSED-NEGATIVE (a_paper_negative_ok): the
  n-gram result did NOT survive a real trained predictor (scale-sensitivity,
  a_toy_scale_recheck). Report numbers verbatim + compare to H_1187 (K*=24,
  d_real=+1.015, drop=+0.512).

cohen_d_paired is PAIRED on per-seed deltas; POSITIVE => SURPRISE arm (1st arg) is
BETTER (higher stage-decode). d(SURPRISE, METRONOME) so a POSITIVE d = surprise wins.

HONESTY (a_scale_honest_scope): still toy-ISH — a small CPU MLP, ONE corpus, NOT a
production LLM. But a GENUINE TRAINED model (SGD-learned weights, generalizing
parameters), a real step up from the count n-gram. a_completeness_over_cheap: any
construction defect (degenerate model, flat surprise, misaligned positions) is FIXED
BEFORE scoring and stated — never tune-to-green after seeing the stage-decode score.
The model's loss is NOT the verdict; stage-decode is (p7). Deterministic seeds.
Lane-M gradient-free GROWTH lane for the mitosis arm (the reader's SGD is a separate
predictor, not the growth substrate) — recorded SEPARATELY from Lane A AKIDA / Lane G
forge / Lane P torch (a_lane_akida_gpu_split). Ran on SUMMER pool host (CPU linux).
"""
import json, math, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H            # substrate: grow_arm/stage_decode/cohen_d/make_text_stream/config
import h1187_learned_surprise_reader as R       # grow_arm_surprise / CAP_LADDER / eval protocol / config

np.seterr(all="ignore")

# ---- frozen training config (the "학습") --------------------------------------------
K_ORDER = R.K_ORDER            # SAME context length as H_1187's n-gram (4 bytes) — fair de-toy comparison
H_HID = 64                     # MLP hidden width
N_EPOCHS = 8                   # SGD epochs over the held-out (train) span
BATCH = 256
LR_MLP = 0.30                  # SGD learning rate (tanh+softmax, one-hot input — robust at this LR)
TRAIN_SEED = 1192              # deterministic init + minibatch shuffle
MAX_TRAIN_SAMPLES = 120_000    # cap train pairs for CPU wall (held-out span has ~200k bytes)
VAL_FRAC = 0.10                # last 10% of the train span held out FROM TRAINING for a val-loss not-degenerate check


# ====================================================================================
# THE TRAINED READER — a one-hidden-layer numpy MLP next-byte predictor.
#   input  : last K_ORDER bytes, one-hot (K_ORDER*256 dims)
#   hidden : tanh, H_HID units
#   output : softmax over 256 next-byte classes
# Trained by minibatch SGD + cross-entropy on the HELD-OUT first half of the corpus.
# A GENUINE trained model (gradient-learned weights, shared hidden features) — the
# de-toy of H_1187's order-k COUNT table. Its loss is NEVER the verdict (p7).
# ====================================================================================
class MLPReader:
    def __init__(self, k=K_ORDER, hid=H_HID, seed=TRAIN_SEED):
        self.k = k
        self.hid = hid
        self.din = k * 256
        rng = np.random.default_rng(seed)
        # Xavier-ish init
        self.W1 = (rng.standard_normal((self.din, hid)) * (1.0 / math.sqrt(self.din))).astype(np.float64)
        self.b1 = np.zeros(hid)
        self.W2 = (rng.standard_normal((hid, 256)) * (1.0 / math.sqrt(hid))).astype(np.float64)
        self.b2 = np.zeros(256)
        self.train_curve = []     # per-epoch train CE (bits/byte)
        self.val_curve = []       # per-epoch val CE (bits/byte)
        self.rng = rng

    def _onehot_ctx(self, ctx_idx):
        """ctx_idx: (n, k) int array of byte values -> (n, k*256) one-hot float."""
        n = ctx_idx.shape[0]
        oh = np.zeros((n, self.k * 256), dtype=np.float64)
        rows = np.repeat(np.arange(n), self.k)
        cols = (np.tile(np.arange(self.k), n) * 256 + ctx_idx.reshape(-1))
        oh[rows, cols] = 1.0
        return oh

    def _forward(self, oh):
        z1 = oh @ self.W1 + self.b1
        a1 = np.tanh(z1)
        z2 = a1 @ self.W2 + self.b2
        z2 -= z2.max(axis=1, keepdims=True)
        ez = np.exp(z2)
        p = ez / ez.sum(axis=1, keepdims=True)
        return a1, p

    def _ce_bits(self, ctx_idx, nb):
        """mean cross-entropy in BITS/byte over (ctx_idx, nb) — the not-degenerate yardstick."""
        oh = self._onehot_ctx(ctx_idx)
        _, p = self._forward(oh)
        pt = np.clip(p[np.arange(len(nb)), nb], 1e-12, 1.0)
        return float(np.mean(-np.log2(pt)))

    def train(self, data_bytes):
        b = np.frombuffer(data_bytes, dtype=np.uint8).astype(np.int64)
        k = self.k
        n_pairs = len(b) - k
        if n_pairs <= 0:
            raise ValueError("train span too short")
        # build (context, next) index pairs
        ctx = np.stack([b[i:i + k] for i in range(n_pairs)], axis=0)  # (n_pairs, k)
        nxt = b[k:k + n_pairs]                                        # (n_pairs,)
        # subsample deterministically for CPU wall if huge
        if n_pairs > MAX_TRAIN_SAMPLES:
            sel = self.rng.choice(n_pairs, size=MAX_TRAIN_SAMPLES, replace=False)
            sel.sort()
            ctx, nxt = ctx[sel], nxt[sel]
            n_pairs = MAX_TRAIN_SAMPLES
        # train/val split (last VAL_FRAC held FROM TRAINING for an honest val-loss curve)
        n_val = max(1, int(n_pairs * VAL_FRAC))
        ctx_tr, nxt_tr = ctx[:-n_val], nxt[:-n_val]
        ctx_va, nxt_va = ctx[-n_val:], nxt[-n_val:]
        n_tr = len(ctx_tr)

        for ep in range(N_EPOCHS):
            order = self.rng.permutation(n_tr)
            for s in range(0, n_tr, BATCH):
                idx = order[s:s + BATCH]
                cb = ctx_tr[idx]; yb = nxt_tr[idx]
                oh = self._onehot_ctx(cb)
                a1, p = self._forward(oh)
                m = len(yb)
                # softmax-CE gradient
                dz2 = p.copy()
                dz2[np.arange(m), yb] -= 1.0
                dz2 /= m
                gW2 = a1.T @ dz2
                gb2 = dz2.sum(axis=0)
                da1 = dz2 @ self.W2.T
                dz1 = da1 * (1.0 - a1 * a1)         # tanh'
                gW1 = oh.T @ dz1
                gb1 = dz1.sum(axis=0)
                self.W2 -= LR_MLP * gW2
                self.b2 -= LR_MLP * gb2
                self.W1 -= LR_MLP * gW1
                self.b1 -= LR_MLP * gb1
            tr_ce = self._ce_bits(ctx_tr[:5000], nxt_tr[:5000])
            va_ce = self._ce_bits(ctx_va, nxt_va)
            self.train_curve.append(tr_ce)
            self.val_curve.append(va_ce)
            print(f"    epoch {ep+1}/{N_EPOCHS}  train_ce={tr_ce:.4f}  val_ce={va_ce:.4f}  bits/byte",
                  flush=True)
        # unigram baseline on the TRAIN span (the model must beat memoryless)
        counts = np.bincount(nxt_tr, minlength=256).astype(np.float64) + 1.0
        pu = counts / counts.sum()
        self.unigram_val_ce = float(np.mean(-np.log2(np.clip(pu[nxt_va], 1e-12, 1.0))))
        self.final_val_ce = self.val_curve[-1]
        self.n_train_pairs = int(n_tr)

    def surprise(self, ctx_bytes, next_byte):
        """−log2 P_model(next_byte | ctx) from the TRAINED MLP. ctx_bytes = bytes of len k."""
        ci = np.frombuffer(ctx_bytes, dtype=np.uint8).astype(np.int64)[None, :]   # (1,k)
        oh = self._onehot_ctx(ci)
        _, p = self._forward(oh)
        pv = float(np.clip(p[0, int(next_byte)], 1e-12, 1.0))
        return float(-math.log2(pv))

    def degenerate(self):
        """Construction-defect guard (a_completeness_over_cheap): the TRAINED model must
        have learned real structure — val CE meaningfully below the 8-bit uniform baseline
        AND below the unigram (memoryless) baseline. Returns (is_degenerate, reason)."""
        if self.final_val_ce >= 8.0 - 0.5:
            return True, f"val_ce {self.final_val_ce:.3f} not below uniform 8.0 (model learned nothing)"
        if self.final_val_ce >= self.unigram_val_ce - 0.05:
            return True, (f"val_ce {self.final_val_ce:.3f} >= unigram {self.unigram_val_ce:.3f} "
                          "(no context structure learned)")
        return False, ""


# ====================================================================================
# Train ONCE on the held-out (first-half) span — shared across seeds (deterministic).
# Reuses H_1187's corpus_bytes() (same self-tiling as make_text_stream) VERBATIM.
# ====================================================================================
_DATA = R.corpus_bytes()
_HELDOUT_END = int(len(_DATA) * R.HELDOUT_FRAC)
print(f"--- TRAINING the reader (the '학습') on summer/CPU: MLP k={K_ORDER} hid={H_HID}, "
      f"{N_EPOCHS} epochs, train span = first {R.HELDOUT_FRAC:.0%} of corpus "
      f"({_HELDOUT_END} bytes) ---", flush=True)
_t0 = time.time()
_READER = MLPReader(K_ORDER, H_HID, TRAIN_SEED)
_READER.train(_DATA[:_HELDOUT_END])
_TRAIN_WALL = time.time() - _t0
print(f"  trained in {_TRAIN_WALL:.1f}s  final val_ce={_READER.final_val_ce:.4f}  "
      f"unigram_val_ce={_READER.unigram_val_ce:.4f}  bits/byte\n", flush=True)


def surprise_track_for_seed(seed):
    """VERBATIM H_1187 surprise_track_for_seed, but reading from the TRAINED MLP _READER
    instead of the count n-gram. SAME `start` draw as make_text_stream (position-aligned),
    SAME anchor (data[p] conditioned on preceding K_ORDER bytes), SAME fallback 8.0."""
    rng = np.random.default_rng(seed)
    need = H.WARMUP + H.T + 1
    span = H.WIN_BYTES + H.STRIDE * need
    start = int(rng.integers(0, max(1, len(_DATA) - span - 1)))   # MUST match make_text_stream's draw
    surp = np.empty(need, dtype=float)
    for i in range(need):
        p = start + i * H.STRIDE
        if p - K_ORDER < 0:
            surp[i] = 8.0
            continue
        ctx = _DATA[p - K_ORDER:p]
        nb = _DATA[p]
        surp[i] = _READER.surprise(ctx, nb)
    return surp


def _verify_position_alignment(seed):
    """SAME alignment check as H_1187: surprise track uses the same `start` as make_text_stream."""
    need = H.WARMUP + H.T + 1
    span = H.WIN_BYTES + H.STRIDE * need
    a = int(np.random.default_rng(seed).integers(0, max(1, len(_DATA) - span - 1)))
    b = int(np.random.default_rng(seed).integers(0, max(1, len(_DATA) - span - 1)))
    return a == b


# ====================================================================================
# EVAL — surprise(TRAINED MLP) vs metronome on stage-decode, at the text's own cap K*,
# plus the seeded time-shuffle control at K*. This is H_1187.eval_at_cap with the
# surprise source = the trained MLP (via the module-local surprise_track_for_seed). We
# inline it (rather than monkeypatching R) so the trained-MLP surprise is unambiguous;
# the GROW arm (R.grow_arm_surprise), the METRONOME arm (H.grow_arm), the decode metric,
# the shuffle, and CAP_LADDER are reused VERBATIM from H_1187/H_1163.
# ====================================================================================
def eval_at_cap(cap):
    saved = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_surp, dec_metro = [], []
    dec_surp_sh, dec_metro_sh = [], []
    surp_fires = []
    for s in H.SEEDS:
        X, stages = H.make_text_stream(s)
        surprise = surprise_track_for_seed(s)                       # TRAINED-MLP surprise
        st_su, cs_su = R.grow_arm_surprise(X, stages, surprise, s)  # VERBATIM H_1187 surprise-gated arm
        st_me, cs_me = H.grow_arm(X, stages, "METRONOME", s)        # VERBATIM metronome baseline
        dec_surp.append(H.stage_decode_accuracy(st_su, cs_su, X, stages, H.N_STAGES_TEXT))
        dec_metro.append(H.stage_decode_accuracy(st_me, cs_me, X, stages, H.N_STAGES_TEXT))
        surp_fires.append(int(len([c for c in cs_su if c >= 0])))
        # time-shuffle control (X, stages, surprise permuted TOGETHER) — VERBATIM H_1187
        rngs = np.random.default_rng(s + 99991)
        perm = rngs.permutation(H.T)
        Xs = X.copy(); ss = stages.copy(); sps = surprise.copy()
        Xs[H.WARMUP:H.WARMUP + H.T] = X[H.WARMUP:H.WARMUP + H.T][perm]
        ss[H.WARMUP:H.WARMUP + H.T] = stages[H.WARMUP:H.WARMUP + H.T][perm]
        sps[H.WARMUP:H.WARMUP + H.T] = surprise[H.WARMUP:H.WARMUP + H.T][perm]
        st_su_s, cs_su_s = R.grow_arm_surprise(Xs, ss, sps, s)
        st_me_s, cs_me_s = H.grow_arm(Xs, ss, "METRONOME", s)
        dec_surp_sh.append(H.stage_decode_accuracy(st_su_s, cs_su_s, Xs, ss, H.N_STAGES_TEXT))
        dec_metro_sh.append(H.stage_decode_accuracy(st_me_s, cs_me_s, Xs, ss, H.N_STAGES_TEXT))
    H.MAX_CELLS = saved
    return {
        "cap": cap,
        "dec_surp": dec_surp, "dec_metro": dec_metro,
        "dec_surp_sh": dec_surp_sh, "dec_metro_sh": dec_metro_sh,
        "mean_surp": float(np.mean(dec_surp)), "mean_metro": float(np.mean(dec_metro)),
        "mean_surp_cells": float(np.mean(surp_fires)),
        "d_real": H.cohen_d_paired(dec_surp, dec_metro),
        "d_shuf": H.cohen_d_paired(dec_surp_sh, dec_metro_sh),
    }


def main():
    print("=== H_1192 — summer-trained REAL reader de-toys H_1187: does a TRAINED numpy-MLP "
          "surprise gate (not a count n-gram) still beat a uniform scan, temporally? ===", flush=True)
    print(f"  reader = one-hidden-layer MLP (k={K_ORDER} one-hot ctx → tanh {H_HID} → softmax 256), "
          f"SGD {N_EPOCHS} epochs on held-out first {R.HELDOUT_FRAC:.0%}; surprise = −log2 P_MLP(byte|ctx)",
          flush=True)
    print(f"  surprise-gated split (mean+{R.SURPRISE_SIGMA}σ saccade, refrac {R.SURPRISE_REFRAC}) vs "
          f"METRONOME on TEXT stage-decode ({H.N_STAGES_TEXT} stages); {len(H.SEEDS)} seeds; "
          f"metric = STAGE-DECODE (p7, NOT model loss)\n", flush=True)

    # --- CONSTRUCTION GUARDS (a_completeness_over_cheap: fix-before-score) ---
    degen, reason = _READER.degenerate()
    align = all(_verify_position_alignment(s) for s in H.SEEDS)
    s0 = surprise_track_for_seed(H.SEEDS[0])
    surp_spread = float(np.std(s0))
    print("--- CONSTRUCTION GUARDS ---", flush=True)
    print(f"  TRAINED MLP: train_pairs={_READER.n_train_pairs}  final_val_ce={_READER.final_val_ce:.4f}  "
          f"unigram_val_ce={_READER.unigram_val_ce:.4f}  uniform=8.0 bits/byte", flush=True)
    print(f"  train curve (bits/byte) = {[round(x,3) for x in _READER.train_curve]}", flush=True)
    print(f"  val   curve (bits/byte) = {[round(x,3) for x in _READER.val_curve]}", flush=True)
    print(f"  degenerate = {degen} ({reason or 'ok — val_ce below uniform AND unigram'})", flush=True)
    print(f"  position-alignment (surprise track ↔ make_text_stream `start`) = {align}", flush=True)
    print(f"  surprise spread (std over seed0) = {surp_spread:.3f} bits  "
          f"mean = {float(np.mean(s0)):.3f} bits  (flat<=0.1 would be degenerate)", flush=True)
    if degen or not align or surp_spread <= 0.1:
        print("  !! CONSTRUCTION DEFECT — must be fixed before scoring (a_completeness_over_cheap)\n",
              flush=True)
    else:
        print("  guards PASS — TRAINED model learned real structure, positions aligned, surprise has spread\n",
              flush=True)

    # --- cap ladder: find text's OWN coverage cap K* = argmax d_real (H_1187 own-cap protocol) ---
    print("--- CAP LADDER (find K* = argmax d_surprise_vs_metro on real-ordered text) ---", flush=True)
    ladder = {}
    for cap in R.CAP_LADDER:
        r = eval_at_cap(cap)
        ladder[cap] = r
        print(f"  cap={cap:3d}  surp_decode={r['mean_surp']:.4f}  metro_decode={r['mean_metro']:.4f}  "
              f"d_real={r['d_real']:+.2f}  surp_cells={r['mean_surp_cells']:.1f}", flush=True)

    kstar = max(R.CAP_LADDER, key=lambda c: ladder[c]["d_real"])
    r = ladder[kstar]
    d_real = r["d_real"]; d_shuf = r["d_shuf"]; drop = d_real - d_shuf
    chance = 1.0 / H.N_STAGES_TEXT

    f1 = d_real >= 0.5
    f2 = drop >= 0.5
    supported = bool(f1 and f2)

    # H_1187 reference numbers (the n-gram result we are de-toying)
    REF = {"Kstar": 24, "d_real": 1.015, "drop": 0.512}

    print(f"\n--- K* = {kstar} (text's own coverage cap; argmax d_real) ---", flush=True)
    print(f"  d_real (surprise vs metronome, real-ordered) = {d_real:+.3f}   F1 (>=0.5) = {f1}", flush=True)
    print(f"  d_shuf (surprise vs metronome, time-shuffled) = {d_shuf:+.3f}", flush=True)
    print(f"  drop  (d_real - d_shuf)                       = {drop:+.3f}   F2 (>=0.5) = {f2}", flush=True)
    print(f"  surp_decode={r['mean_surp']:.4f}  metro_decode={r['mean_metro']:.4f}  chance={chance:.4f}",
          flush=True)
    print(f"  H_1187 n-gram ref: K*={REF['Kstar']}  d_real={REF['d_real']:+.3f}  drop={REF['drop']:+.3f}",
          flush=True)

    if supported:
        ruling = ("SUPPORTED (SACCADIC-READING-HOLDS-AT-LESS-TOY-SCALE): a REAL TRAINED numpy-MLP "
                  f"surprise reader (SGD-learned weights, val_ce={_READER.final_val_ce:.2f} < unigram "
                  f"{_READER.unigram_val_ce:.2f} < uniform 8.0 bits/byte) reproduces H_1187's "
                  f"saccadic-reading result at the text's own cap K*={kstar}: it BEATS a uniform "
                  f"metronome scan (F1 d_real={d_real:+.2f}>=0.5) AND that advantage is TEMPORAL — "
                  f"destroyed by a time-shuffle (F2 drop={drop:+.2f}>=0.5). The H_1187 finding was NOT "
                  "a count-table artifact: surprise-driven saccadic reading de-toys ONE rung to a "
                  "genuine gradient-trained predictor. (Model loss is NOT the verdict; stage-decode is.)")
    else:
        why = []
        if not f1:
            why.append(f"F1 fail: trained-MLP surprise does NOT beat metronome on decode "
                       f"(d_real={d_real:+.2f} < 0.5)")
        if not f2:
            why.append(f"F2 fail: advantage NOT temporal (drop={drop:+.2f} < 0.5; d_shuf={d_shuf:+.2f})")
        ruling = ("CLOSED-NEGATIVE (a_paper_negative_ok): the H_1187 saccadic-reading GREEN did NOT "
                  f"survive a REAL trained predictor at the text's own cap K*={kstar} — " +
                  " | ".join(why) + f". The order-{K_ORDER} COUNT n-gram beat the metronome (H_1187 "
                  f"d_real={REF['d_real']:+.2f}) but a gradient-trained MLP surprise (val_ce="
                  f"{_READER.final_val_ce:.2f} bits/byte, genuinely learned) does not — the n-gram "
                  "result is scale-sensitive (a_toy_scale_recheck), likely a count-table sharpness "
                  "artifact the smoother MLP surprise washes out. Real-LLM surprise UNVERIFIED.")

    verdict = {
        "H": "H_1192",
        "title": "the FIRST summer-trained run — de-toy H_1187: does a REAL TRAINED numpy-MLP "
                 "next-byte surprise reader (not a count n-gram) reproduce the saccadic-reading "
                 "result (beat a uniform metronome scan on real-text stage-decode, temporally)?",
        "compute_host": os.environ.get("H1192_HOST", "unknown"),
        "frozen_falsifier": {
            "Kstar": "argmax over cap ladder %s of d_surprise_vs_metro (text's own cap)" % str(R.CAP_LADDER),
            "F1": "d_surprise_vs_metro(K*) >= 0.5 (trained-reader saccadic reading beats uniform scan)",
            "F2": "(d_real - d_shuf) >= 0.5 at K* (advantage destroyed by time-shuffle = temporal)",
            "SUPPORTED": "F1 and F2 (SACCADIC-READING-HOLDS-AT-LESS-TOY-SCALE — de-toys H_1187 one rung)",
            "metric": "STAGE-DECODE accuracy (p7, NOT the model's loss/perplexity)",
        },
        "trained_model": {
            "kind": "numpy MLP next-byte predictor (one-hidden-layer)",
            "arch": f"{K_ORDER*256} one-hot in -> tanh {H_HID} -> softmax 256",
            "n_params": int(_READER.din * H_HID + H_HID + H_HID * 256 + 256),
            "k_order": K_ORDER, "hidden": H_HID, "epochs": N_EPOCHS, "lr": LR_MLP, "batch": BATCH,
            "train_pairs": _READER.n_train_pairs,
            "train_wall_s": round(_TRAIN_WALL, 2),
            "train_ce_curve_bits": [round(x, 4) for x in _READER.train_curve],
            "val_ce_curve_bits": [round(x, 4) for x in _READER.val_curve],
            "final_val_ce_bits": round(_READER.final_val_ce, 4),
            "unigram_val_ce_bits": round(_READER.unigram_val_ce, 4),
            "uniform_baseline_bits": 8.0,
            "not_degenerate": (not degen),
            "degenerate_reason": reason,
        },
        "construction_guards": {
            "degenerate": bool(degen), "degenerate_reason": reason,
            "position_alignment": bool(align),
            "surprise_spread_bits_seed0": surp_spread,
            "surprise_mean_bits_seed0": float(np.mean(s0)),
        },
        "Kstar": kstar,
        "d_real": d_real, "d_shuf": d_shuf, "drop": drop,
        "F1_saccadic_wins": {"d_real": d_real, "bar": 0.5, "pass": bool(f1)},
        "F2_temporal": {"drop": drop, "d_shuf": d_shuf, "bar": 0.5, "pass": bool(f2)},
        "mean_decode": {"surprise": r["mean_surp"], "metronome": r["mean_metro"], "chance": chance},
        "cap_ladder": {str(c): {"d_real": ladder[c]["d_real"], "mean_surp": ladder[c]["mean_surp"],
                                "mean_metro": ladder[c]["mean_metro"],
                                "mean_surp_cells": ladder[c]["mean_surp_cells"]} for c in R.CAP_LADDER},
        "h1187_ngram_reference": REF,
        "comparison_to_h1187": (
            f"H_1192 (TRAINED MLP): K*={kstar}, d_real={d_real:+.3f}, drop={drop:+.3f}  vs  "
            f"H_1187 (COUNT n-gram): K*={REF['Kstar']}, d_real={REF['d_real']:+.3f}, drop={REF['drop']:+.3f}. "
            + ("Result SURVIVES the de-toy — the saccadic-reading advantage reproduces on a genuine "
               "gradient-trained predictor." if supported else
               "Result does NOT survive the de-toy — the n-gram green was scale-sensitive.")),
        "supported": supported,
        "ruling": ruling,
        "reading_answer": (
            "YES, AND it de-toys — a GENUINELY TRAINED model's surprise (not a count table) still "
            "drives saccadic reading that beats a uniform scan AND is temporally grounded. The "
            "H_1187 finding is robust to a real gradient-trained predictor one rung up." if supported else
            "NO at this rung — the saccadic-reading advantage found with a COUNT n-gram does NOT "
            "reproduce when the surprise comes from a genuinely TRAINED MLP; the n-gram green is "
            "scale-sensitive (a_toy_scale_recheck). Real-LLM next-token surprise remains the "
            "unverified path."),
        "scope": "TOY-ISH ($0 CPU numpy, %d seeds) but a GENUINE TRAINED model — a one-hidden-layer "
                 "MLP next-byte predictor (SGD %d epochs, k=%d one-hot ctx, hid=%d) on ONE corpus, "
                 "a real step UP from H_1187's order-%d COUNT n-gram. Reuses the H_1163 grow_arm "
                 "METRONOME + stage_decode + cohen_d + make_text_stream and H_1187 grow_arm_surprise "
                 "+ CAP_LADDER + time-shuffle VERBATIM; the ONLY swap is the surprise SOURCE "
                 "(count-table -> trained MLP). NOT a production LLM; real-LLM surprise + real human "
                 "reading-time/eye-tracking + scale UNVERIFIED (a_scale_honest_scope, "
                 "a_toy_scale_recheck). The reader's SGD is a separate predictor; the mitosis GROWTH "
                 "arm stays Lane-M gradient-free (a_lane_akida_gpu_split). Ran on the SUMMER pool "
                 "host (CPU linux, python3.12 + numpy)."
                 % (len(H.SEEDS), N_EPOCHS, K_ORDER, H_HID, K_ORDER),
    }
    print("\n=== VERDICT ===", flush=True)
    print(f"  {ruling}\n", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1192_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
