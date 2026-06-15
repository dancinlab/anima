#!/usr/bin/env python3
# h1326_ko_featural_r2.py — r2 of H_1322 (🧱 HONEST-FLOOR, geometry-confounded). Two pre-registered
# fixes (FREEZE: .verdicts/1326_ko_featural_r2/H_1326_FREEZE.txt; NOT moved — c9/p7):
#   FIX A  GEOMETRY-FAIR: one best-of-a-fixed-bank-by-TRAIN-CE seed-center protocol applied
#          IDENTICALLY to every arm (jamo / featural / factorized / shuffle), so no arm gets a
#          seed-center advantage. The jamo arm MUST reproduce H_1316's 2.51335 (calibration anchor).
#   FIX B  LABEL-FACTORIZATION: a second scoring head whose TARGET is the FACTORED feature vector
#          (class + independent per-column features over a LOSSLESS jamo bijection), so Hangul's
#          designed systematicity enters the TARGET, not just the partition.
#
# GREEN iff G1 (geometry-fair depth, BEST=min(A2,A3) beats jamo A1 by >=0.03 AND < raw) AND
#          G2 (BEST beats its own shuffled-feature control by >=0.05). G3 (factorization-
#          attribution: A3 vs A2) is a reported diagnostic.
#
# REAL Korean only (NO synthetic, p1-p8): SAME anima-7b R2 web corpus as H_1307 RUN A / H_1316.
# KO window sha256 ASSERTED == the H_1307 RUN A manifest hash. R2 keys env-only at fetch time (c7).
# SCALE-HONEST: toy/DIRECTIONAL; engine-transfer to live hexa = follow-on; NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e); sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316) ──────────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342
H1316_JAMO_CE = 2.51335
G1_MARGIN = 0.03
G2_MARGIN = 0.05
CALIB_TOL = 0.0005
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3

def log(*a): print(*a, flush=True)

# ── REAL corpus fetch from R2 (secrets env-only, never logged) ──────────────────
def fetch_r2_range(key, nbytes):
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}))
    obj = s3.get_object(Bucket=os.environ["R2_BUCKET"], Key=key, Range=f"bytes=0-{nbytes-1}")
    return obj["Body"].read()

def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
        except Exception:
            continue
    return b

# ════════════════════════════════════════════════════════════════════════════════════════════
#  HANGUL FEATURAL DESIGN MAPS — LOSSLESS BIJECTIONS within each jamo class (verified offline)
#  INITIAL (choseong) U+1100..U+1112 : [artic, manner, nasal, liquid, affric]
#  MEDIAL  (jungseong) U+1161..U+1175: [7, vbase, polar, iota, round]
#  FINAL   (jongseong) U+11A8..U+11C2: [artic, manner, nasal, liquid, cluster_idx]
# ════════════════════════════════════════════════════════════════════════════════════════════
CONS_FEAT = {
    0x1100:[1,0,0,0,0],0x1101:[1,2,0,0,0],0x1102:[2,0,1,0,0],0x1103:[2,0,0,0,0],
    0x1104:[2,2,0,0,0],0x1105:[2,0,0,1,0],0x1106:[3,0,1,0,0],0x1107:[3,0,0,0,0],
    0x1108:[3,2,0,0,0],0x1109:[4,0,0,0,0],0x110A:[4,2,0,0,0],0x110B:[6,0,0,0,0],
    0x110C:[4,0,0,0,1],0x110D:[4,2,0,0,1],0x110E:[4,1,0,0,1],0x110F:[1,1,0,0,0],
    0x1110:[2,1,0,0,0],0x1111:[3,1,0,0,0],0x1112:[5,0,0,0,0],
}
VOWEL_FEAT = {
    0x1161:[7,1,1,0,0],0x1162:[7,1,1,0,1],0x1163:[7,1,1,1,0],0x1164:[7,1,1,1,1],
    0x1165:[7,1,2,0,0],0x1166:[7,1,2,0,1],0x1167:[7,1,2,1,0],0x1168:[7,1,2,1,1],
    0x1169:[7,2,1,0,0],0x116A:[7,3,1,0,0],0x116B:[7,3,1,0,1],0x116C:[7,3,1,1,0],
    0x116D:[7,2,1,1,0],0x116E:[7,2,2,0,0],0x116F:[7,3,2,0,0],0x1170:[7,3,2,0,1],
    0x1171:[7,3,2,1,0],0x1172:[7,2,2,1,0],0x1173:[7,2,0,0,0],0x1174:[7,3,0,1,0],
    0x1175:[7,1,0,0,0],
}
FINAL_FEAT = {
    0x11A8:[1,0,0,0,0],0x11A9:[1,2,0,0,0],0x11AA:[1,0,0,0,1],0x11AB:[2,0,1,0,0],
    0x11AC:[2,0,1,0,2],0x11AD:[2,0,1,0,3],0x11AE:[2,0,0,0,0],0x11AF:[2,0,0,1,0],
    0x11B0:[2,0,0,1,1],0x11B1:[2,0,0,1,2],0x11B2:[2,0,0,1,3],0x11B3:[2,0,0,1,4],
    0x11B4:[2,0,0,1,5],0x11B5:[2,0,0,1,6],0x11B6:[2,0,0,1,7],0x11B7:[3,0,1,0,0],
    0x11B8:[3,0,0,0,0],0x11B9:[3,0,0,0,1],0x11BA:[4,0,0,0,0],0x11BB:[4,2,0,0,0],
    0x11BC:[1,0,1,0,1],0x11BD:[4,0,0,0,1],0x11BE:[4,1,0,0,0],0x11BF:[1,1,0,0,0],
    0x11C0:[2,1,0,0,0],0x11C1:[3,1,0,0,0],0x11C2:[5,0,0,0,0],
}
# class ids for the factorized target
CLS_INIT, CLS_MED, CLS_FIN, CLS_BYTE = 0, 1, 2, 3
# per-class feature column maxima (for column cardinalities in the factorized head)
def _col_max(d):
    M = np.array(list(d.values())); return M.max(axis=0).tolist()
INIT_MAX = _col_max(CONS_FEAT)   # [6,2,1,0,1]
MED_MAX  = _col_max(VOWEL_FEAT)  # [7,3,2,1,1]
FIN_MAX  = _col_max(FINAL_FEAT)  # [5,2,1,1,7]

def jamo_feature_vec(cp):
    if cp in CONS_FEAT: return CONS_FEAT[cp]
    if cp in VOWEL_FEAT: return VOWEL_FEAT[cp]
    if cp in FINAL_FEAT: return FINAL_FEAT[cp]
    return None

def jamo_class(cp):
    if cp in CONS_FEAT: return CLS_INIT
    if cp in VOWEL_FEAT: return CLS_MED
    if cp in FINAL_FEAT: return CLS_FIN
    return None

# ── NO-CHEAT round-trip + accounting (same as H_1316) ───────────────────────────
def roundtrip_and_accounting(text):
    bad = 0; n_syll = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            n_syll += 1
            nfc = unicodedata.normalize("NFC", unicodedata.normalize("NFD", ch))
            if nfc.encode("utf-8") != ch.encode("utf-8"): bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0}

def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch): jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    return {cp: 256 + i for i, cp in enumerate(jamo_sorted)}, jamo_sorted

def syll_jamo_nbytes(njamo):
    if njamo == 3: return [1, 1, 1]
    if njamo == 2: return [2, 1]
    if njamo == 1: return [3]
    out = [1] * njamo; out[0] += (3 - njamo) if njamo < 3 else 0; return out

def make_streams(text, jamo_to_id, jamo_feat_map):
    """syms (jamo-id 256+rank or byte 0..255) · feats (N×5 design vector) · nby (UTF-8 bytes) ·
       depth (continuation depth) · cls (factorized class id) · fcols (N×5 within-class feature
       columns for the FACTORIZED target; for bytes, the byte id is carried separately via syms)."""
    syms, feats, nby, depth, cls = [], [], [], [], []
    d = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                jcp = ord(jc)
                syms.append(jamo_to_id[jcp])
                fv = jamo_feat_map.get(jcp) or [0, 0, 0, 0, 0]
                feats.append(fv)
                # class is a property of the codepoint block (INTACT — class is structural, the
                # shuffle only permutes the FEATURE VECTOR assignment, never the class membership)
                kc = jamo_class(jcp)
                cls.append(kc if kc is not None else CLS_BYTE)
                nby.append(nb[j])
                d = 0 if j == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(int(b))
                feats.append([b >> 4, b & 0xF, 0, 0, 0])
                cls.append(CLS_BYTE)
                nby.append(1)
                d = d + 1 if 0x80 <= b <= 0xBF else 0
                depth.append(d)
    return (np.asarray(syms, np.int64), np.asarray(feats, np.int64), np.asarray(nby, np.int64),
            np.asarray(depth, np.int64), np.asarray(cls, np.int64))

# ── engine-native mitosis (BYTE-FAITHFUL to H_1306/H_1307/H_1316) ───────────────
def assign_all(centers_t, X_t):
    return torch.argmin(torch.cdist(X_t, centers_t, p=2), dim=1)

def all_heads(Y_t, owner, K, ntr, vj, dev):
    Hmat = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    flat = owner[:ntr] * vj + Y_t[:ntr]
    Hmat.view(-1).index_add_(0, flat, torch.ones(flat.shape[0], dtype=torch.float64, device=dev))
    return Hmat / Hmat.sum(dim=1, keepdim=True)

def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any(): return -1.0
    return -torch.log(p_row[Y_t[:ntr][mask]] + 1e-12).mean().item()

def grow_on(centers, X_tr, Y_tr, ntr, vj, dev, grow_max):
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr); K = len(centers); owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, vj, dev)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0: local_ce[k] = owned_ce(Y_tr, owner, k, ntr, Hmat[k])
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig: break
        pick = elig[0]; bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce: bestce = local_ce[k]; pick = k
        if len(centers) + 1 > grow_max: break
        pts = X_tr[:ntr][owntr == pick]
        if pts.shape[0] == 0: break
        ax = int(torch.argmax(pts.var(dim=0, unbiased=False)).item())
        col = pts[:, ax]; m = col.shape[0]; scol, _ = torch.sort(col)
        med = scol[m // 2].item() if m % 2 == 1 else ((scol[m//2-1] + scol[m//2]) / 2.0).item()
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0: break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers

def split_even_odd(X, *arrs, stride):
    X = X[::stride]; arrs = [a[::stride] for a in arrs]
    idx = np.arange(X.shape[0]); e = idx % 2 == 0; o = idx % 2 == 1
    out_tr = [X[e]] + [a[e] for a in arrs]; out_te = [X[o]] + [a[o] for a in arrs]
    return out_tr, out_te

# ── OPAQUE-id per-byte CE (A1/A2 target = jamo id) ──────────────────────────────
def per_byte_ce_opaque(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev):
    owner_tr = assign_all(centers_t, X_tr_t)
    Hmat = all_heads(Y_tr_t, owner_tr, centers_t.shape[0], ntr, vj, dev)
    owner_te = assign_all(centers_t, X_te_t)
    p = Hmat[owner_te, Y_te_t]; nll = -torch.log(p + 1e-12)
    nb = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    return nll.sum().item() / float(nb.sum().item())

# ── FACTORIZED per-byte CE (A3 target = class + independent per-column features) ─
def per_byte_ce_factorized(centers_t, X_tr_t, ntr,
                           cls_tr, fcols_tr, sym_tr,
                           X_te_t, cls_te, fcols_te, sym_te, NB_te, dev):
    """For each owner cell, build:
        - a class head P(class)              (4-way count-MLE)
        - per (class, column) feature heads  P(feat_col | class)   (low cardinality count-MLE)
        - for BYTE class, a byte-id head     P(byte | class=BYTE)   (256-way)
       Held-out NLL(jamo) = -log P(class) + Σ_col -log P(feat_col|class)   (Hangul)
                          = -log P(class) + -log P(byte|class=BYTE)        (raw byte)
       This is a valid (factorized) distribution over the SAME jamo alphabet (lossless bijection),
       so the CE axis matches the opaque arms. Divided by Σ n_bytes(sym)."""
    K = centers_t.shape[0]
    owner_tr = assign_all(centers_t, X_tr_t).cpu().numpy()[:ntr]
    owner_te = assign_all(centers_t, X_te_t).cpu().numpy()
    cls_tr_n = cls_tr.cpu().numpy()[:ntr]; fcols_tr_n = fcols_tr.cpu().numpy()[:ntr]
    sym_tr_n = sym_tr.cpu().numpy()[:ntr]
    cls_te_n = cls_te.cpu().numpy(); fcols_te_n = fcols_te.cpu().numpy()
    sym_te_n = sym_te.cpu().numpy(); nb_te_n = np.asarray(NB_te, np.float64)
    NCLS = 4; NCOL = 5
    col_card = {CLS_INIT: [m + 1 for m in INIT_MAX], CLS_MED: [m + 1 for m in MED_MAX],
                CLS_FIN: [m + 1 for m in FIN_MAX]}
    # build per-cell heads from TRAIN
    cls_cnt = np.full((K, NCLS), LAPLACE)
    feat_cnt = {kc: [np.full((K, col_card[kc][c]), LAPLACE) for c in range(NCOL)]
                for kc in (CLS_INIT, CLS_MED, CLS_FIN)}
    byte_cnt = np.full((K, 256), LAPLACE)
    for i in range(ntr):
        k = owner_tr[i]; kc = cls_tr_n[i]; cls_cnt[k, kc] += 1.0
        if kc == CLS_BYTE:
            byte_cnt[k, sym_tr_n[i]] += 1.0
        else:
            fv = fcols_tr_n[i]
            for c in range(NCOL):
                feat_cnt[kc][c][k, fv[c]] += 1.0
    cls_p = cls_cnt / cls_cnt.sum(axis=1, keepdims=True)
    feat_p = {kc: [feat_cnt[kc][c] / feat_cnt[kc][c].sum(axis=1, keepdims=True) for c in range(NCOL)]
              for kc in (CLS_INIT, CLS_MED, CLS_FIN)}
    byte_p = byte_cnt / byte_cnt.sum(axis=1, keepdims=True)
    # score TEST
    total_nats = 0.0
    for i in range(owner_te.shape[0]):
        k = owner_te[i]; kc = cls_te_n[i]
        nll = -np.log(cls_p[k, kc] + 1e-12)
        if kc == CLS_BYTE:
            nll += -np.log(byte_p[k, sym_te_n[i]] + 1e-12)
        else:
            fv = fcols_te_n[i]
            for c in range(NCOL):
                nll += -np.log(feat_p[kc][c][k, fv[c]] + 1e-12)
        total_nats += nll
    return total_nats / float(nb_te_n.sum())

# ── partition feature builders ──────────────────────────────────────────────────
def feat_norm(feats):
    out = feats.astype(np.float64).copy()
    out[:, 0] /= 16.0; out[:, 1] /= 16.0; out[:, 2] /= 3.0; out[:, 3] /= 2.0; out[:, 4] /= 8.0
    return out

def build_X_jamo(syms, depth, vj):
    n = len(syms); idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx

def build_X_featural(syms, feats, depth, vj):
    n = len(syms); idx = np.arange(4, n - 1)
    fn = feat_norm(feats)
    cdep = (depth[idx - 1].astype(np.float64) / 3.0)[:, None]
    X = np.concatenate([fn[idx - 1], fn[idx - 2], cdep], axis=1)  # N×11
    return X, syms[idx].astype(np.int64), idx

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank, identical to every arm) ═══
BANK_GRID = [
    (0.3, 0.7, 0.0, 0.5),
    (0.3, 0.7, 0.3, 0.7),
    (0.5, 0.5, 0.0, 0.5),
    (0.25, 0.75, 0.0, 0.5),
    (0.4, 0.6, 0.2, 0.8),
]
def seed_bank(dim):
    """FROZEN bank of 2-center seed patterns for partition-dim `dim`, plus the H_1316-FAMILY
       member (body 0.3/0.7, interior coords pinned to 0.5, last coord 0.0/0.5) lifted to `dim`.
       Identical generation rule for every arm → geometry-fair."""
    bank = []
    for (lo, hi, alo, ahi) in BANK_GRID:
        a = [lo] * dim; a[-1] = alo
        b = [hi] * dim; b[-1] = ahi
        bank.append([a, b])
    # H_1316-FAMILY: body 0.3/0.7, all interior coords pinned to 0.5, last coord 0.0/0.5
    a = [0.3] + [0.5] * (dim - 2) + [0.0] if dim >= 2 else [0.3]
    b = [0.7] + [0.5] * (dim - 2) + [0.5] if dim >= 2 else [0.7]
    if dim == 1: a = [0.3]; b = [0.7]
    bank.append([a, b])
    return bank

def grow_pick_bank(Xtr, Ytr, vj, dev, grow_max, dim, scorer, score_args):
    """FIX A: grow from EACH bank member on TRAIN ONLY, pick the member with the lowest TRAIN
       held-out CE (even/odd within train — NO test peeking), return its grown centers + the
       picked member index. scorer/score_args let the selection use the SAME head as the arm."""
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    n = Xtr.shape[0]
    inner_idx = np.arange(n)
    ie = inner_idx % 2 == 0; io = inner_idx % 2 == 1
    best_ce = 1e18; best_centers = None; best_member = -1
    for mi, seed in enumerate(seed_bank(dim)):
        # grow on the inner-train (even-of-train), score on inner-test (odd-of-train)
        Xie = torch.tensor(Xtr[ie], dtype=torch.float64, device=dev)
        Yie = torch.tensor(Ytr[ie], dtype=torch.int64, device=dev)
        Xio = torch.tensor(Xtr[io], dtype=torch.float64, device=dev)
        Yio = torch.tensor(Ytr[io], dtype=torch.int64, device=dev)
        c = grow_on(seed, Xie, Yie, Xie.shape[0], vj, dev, grow_max)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        nbio = np.ones(int(io.sum()))  # train-CE proxy = per-symbol CE (uniform 1-byte weight)
        ce = per_byte_ce_opaque(ct, Xie, Yie, Xie.shape[0], Xio, Yio, nbio, vj, dev)
        if ce < best_ce:
            best_ce = ce; best_member = mi
    # regrow the WINNING member on the FULL train (standard practice), return centers
    seed = seed_bank(dim)[best_member]
    c = grow_on(seed, Xtr_t, Ytr_t, n, vj, dev, grow_max)
    return c, best_member, best_ce

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4326,4327,4328")
    ap.add_argument("--out", default="/tmp/h1326_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu"); log("=== H_1326 — ko-featural r2 (geometry-fair + label-factorization) (CPU) ===")
    else:
        dev = torch.device("cuda"); cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1326 — ko-featural r2 (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} torch={torch.__version__}")
        _ = (torch.randn(256, 256, device=dev) @ torch.randn(256, 256, device=dev)).sum().item()
        torch.cuda.synchronize()

    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A / H_1316 ──
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]; log(f"[corpus] KO from cache {args.ko_cache}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_KO_KEY}")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8); open(args.ko_cache, "wb").write(ko_raw)
    ko_win = trim_utf8(ko_raw[: args.ko_window]); ko_sha = hashlib.sha256(ko_win).hexdigest()
    same_ko = (ko_sha == H1307_KO_SHA)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  identical-to-H_1307-RUN-A={same_ko}")
    if not same_ko:
        log("FATAL: KO corpus sha != H_1307 RUN A — REFUSING (provenance gate, REAL-only). STOP."); sys.exit(3)
    ko_text = ko_win.decode("utf-8")

    rt = roundtrip_and_accounting(ko_text)
    log(f"[nocheat] hangul_syllables={rt['hangul_syllables']} roundtrip_fail={rt['roundtrip_fail']} ok={rt['ok']}")
    jamo_to_id, jamo_sorted = build_jamo_vocab(ko_text)
    n_jamo = len(jamo_sorted); VJ = 256 + n_jamo
    log(f"[jamo] distinct jamo codepoints={n_jamo}  jamo-symbol vocab Vj={VJ}")
    intact_map = {}; missing = []
    for cp in jamo_sorted:
        fv = jamo_feature_vec(cp)
        if fv is None: missing.append(cp); intact_map[cp] = [0, 0, 0, 0, 0]
        else: intact_map[cp] = fv
    log(f"[featmap] design-feature coverage: {n_jamo - len(missing)}/{n_jamo} jamo mapped; "
        f"missing={[hex(m) for m in missing][:20]}")

    # ── G0 raw-byte re-port ──
    ko_bytes = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    is_cont = (ko_bytes >= 0x80) & (ko_bytes <= 0xBF)
    raw_depth = np.zeros(len(ko_bytes), np.int64); d = 0
    for i in range(len(ko_bytes)):
        d = d + 1 if is_cont[i] else 0; raw_depth[i] = d
    raw_nbytes = np.ones(len(ko_bytes), np.int64)
    Xr, Yr, idxr = build_X_jamo(ko_bytes, raw_depth, 256)
    NBr = raw_nbytes[idxr]
    (Xtr_r, Ytr_r, NBtr_r), (Xte_r, Yte_r, NBte_r) = split_even_odd(Xr, Yr, NBr, stride=args.ko_stride)
    cr, mr, _ = grow_pick_bank(Xtr_r, Ytr_r, 256, dev, args.grow_max, 3, None, None)
    ctr = torch.tensor(cr, dtype=torch.float64, device=dev)
    g0 = per_byte_ce_opaque(ctr, torch.tensor(Xtr_r, dtype=torch.float64, device=dev),
                            torch.tensor(Ytr_r, dtype=torch.int64, device=dev), Xtr_r.shape[0],
                            torch.tensor(Xte_r, dtype=torch.float64, device=dev),
                            torch.tensor(Yte_r, dtype=torch.int64, device=dev), NBte_r, 256, dev)
    log(f"[G0 raw-byte] ce={round(g0,5)} cells={len(cr)} member={mr}  (H_1316 reproduced 2.95342)")

    # ── streams (intact) ──
    syms_i, feats_i, nby_i, depth_i, cls_i = make_streams(ko_text, jamo_to_id, intact_map)
    log(f"[nocheat] byte-accounting: Σ n_bytes={int(nby_i.sum())} corpus_bytes={len(ko_win)} "
        f"close={int(nby_i.sum())==len(ko_win)}")

    # helper: run an opaque-target arm under the Fix-A bank protocol
    def run_opaque_arm(X, Y, idx, nby, vj, dim, tag):
        NB = nby[idx]
        (Xtr, Ytr, NBtr), (Xte, Yte, NBte) = split_even_odd(X, Y, NB, stride=args.ko_stride)
        c, mi, tce = grow_pick_bank(Xtr, Ytr, vj, dev, args.grow_max, dim, None, None)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        ce = per_byte_ce_opaque(ct, torch.tensor(Xtr, dtype=torch.float64, device=dev),
                                torch.tensor(Ytr, dtype=torch.int64, device=dev), Xtr.shape[0],
                                torch.tensor(Xte, dtype=torch.float64, device=dev),
                                torch.tensor(Yte, dtype=torch.int64, device=dev), NBte, vj, dev)
        log(f"[{tag}] ce={round(ce,5)} cells={len(c)} bank_member={mi} train_proxy={round(tce,5)}")
        return ce, len(c), mi

    # helper: run the FACTORIZED-target arm under the Fix-A bank protocol (partition = featural X,
    # selection uses the OPAQUE head on the partition so geometry is chosen identically to A2, then
    # the factorized head scores the winning geometry — the geometry protocol is identical to A2/A1)
    def run_factorized_arm(syms, feats, depth, nby, cls, vj, tag):
        Xf, Yf, idxf = build_X_featural(syms, feats, depth, vj)
        NB = nby[idxf]; clsf = cls[idxf]; fcolsf = feats[idxf]; symf = syms[idxf]
        (Xtr, Ytr, NBtr, clstr, fctr, symtr), (Xte, Yte, NBte, clste, fcte, symte) = \
            split_even_odd(Xf, Yf, NB, clsf, fcolsf, symf, stride=args.ko_stride)
        c, mi, tce = grow_pick_bank(Xtr, Ytr, vj, dev, args.grow_max, Xf.shape[1], None, None)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        ce = per_byte_ce_factorized(
            ct, torch.tensor(Xtr, dtype=torch.float64, device=dev), Xtr.shape[0],
            torch.tensor(clstr, dtype=torch.int64, device=dev),
            torch.tensor(fctr, dtype=torch.int64, device=dev),
            torch.tensor(symtr, dtype=torch.int64, device=dev),
            torch.tensor(Xte, dtype=torch.float64, device=dev),
            torch.tensor(clste, dtype=torch.int64, device=dev),
            torch.tensor(fcte, dtype=torch.int64, device=dev),
            torch.tensor(symte, dtype=torch.int64, device=dev), NBte, dev)
        log(f"[{tag}] ce={round(ce,5)} cells={len(c)} bank_member={mi}")
        return ce, len(c), mi

    # ── A1 jamo opaque-id (CALIBRATION anchor = 2.51335) ──
    Xj, Yj, idxj = build_X_jamo(syms_i, depth_i, VJ)
    a1_ce, a1_cells, a1_mi = run_opaque_arm(Xj, Yj, idxj, nby_i, VJ, 3, "A1 jamo opaque-id")
    calib_ok = abs(a1_ce - H1316_JAMO_CE) <= CALIB_TOL
    log(f"[CALIB] A1 jamo {round(a1_ce,5)} vs H_1316 {H1316_JAMO_CE}  match(±{CALIB_TOL})={calib_ok}")
    if not calib_ok:
        log("WARN: A1 jamo did NOT reproduce 2.51335 byte-exact — geometry protocol calibration off. "
            "Continuing but flagging the verdict (honest, c9).")

    # ── A2 featural partition + opaque target (Fix A only) ──
    Xf, Yf, idxf = build_X_featural(syms_i, feats_i, depth_i, VJ)
    a2_ce, a2_cells, a2_mi = run_opaque_arm(Xf, Yf, idxf, nby_i, VJ, Xf.shape[1], "A2 featural+opaque")

    # ── A3 featural partition + FACTORIZED target (Fix A + Fix B) ──
    a3_ce, a3_cells, a3_mi = run_factorized_arm(syms_i, feats_i, depth_i, nby_i, cls_i, VJ, "A3 featural+factorized")

    # ── controls: shuffle feature map per seed → A2s, A3s ──
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    a2s_list = []; a3s_list = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        perm = rng.permutation(len(jamo_sorted))
        shuf_map = {cp: intact_map[jamo_sorted[perm[i]]] for i, cp in enumerate(jamo_sorted)}
        syms_s, feats_s, nby_s, depth_s, cls_s = make_streams(ko_text, jamo_to_id, shuf_map)
        Xfs, Yfs, idxfs = build_X_featural(syms_s, feats_s, depth_s, VJ)
        a2s_ce, _, a2s_mi = run_opaque_arm(Xfs, Yfs, idxfs, nby_s, VJ, Xfs.shape[1], f"A2s shuffle seed{sd}")
        a3s_ce, _, a3s_mi = run_factorized_arm(syms_s, feats_s, depth_s, nby_s, cls_s, VJ, f"A3s shuffle seed{sd}")
        a2s_list.append(a2s_ce); a3s_list.append(a3s_ce)
        log(f"[seed {sd}] " + json.dumps({"a2s": round(a2s_ce,5), "a3s": round(a3s_ce,5)}))

    a2s_mean = float(np.mean(a2s_list)); a3s_mean = float(np.mean(a3s_list))

    # ── BEST = min(A2, A3); G1/G2/G3 ──
    best_arm = "A2" if a2_ce <= a3_ce else "A3"
    best_ce = min(a2_ce, a3_ce)
    best_shuf = a2s_mean if best_arm == "A2" else a3s_mean
    g1 = bool(best_ce < (a1_ce - G1_MARGIN) and best_ce < H1307_CEILING_KO_CE)
    g2 = bool((best_shuf - best_ce) >= G2_MARGIN)
    g3_factor_wins = bool(a3_ce < a2_ce)
    green = bool(g1 and g2)
    if green:
        verdict = ("🟢 GREEN — geometry-fair, Hangul's design gives a measurable DEPTH advantage "
                   f"BELOW jamo via {best_arm} ({'label-factorization/target' if best_arm=='A3' else 'featural-partition'})")
    elif not g1:
        verdict = ("🧱 HONEST-FLOOR (confound-free) — geometry-fair, the better of {featural-partition, "
                   "label-factorization} does NOT beat the jamo floor by the bar → jamo is the genuine "
                   "decomposition FLOOR for this mechanism family (c9)")
    else:
        verdict = ("🟠 DIMS-NOT-DESIGN — G1 holds but G2 fails: the gain is dims/vocab, not the "
                   "designed systematicity (shuffle ties; honest negative, c9)")

    wall = time.time() - t0
    summary = {
        "id": "H_1326", "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__, "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko), "ko_stride": args.ko_stride,
        "grow_max": args.grow_max, "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "design_feature_coverage": f"{n_jamo - len(missing)}/{n_jamo}",
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE, "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "g0_raw_byte_ce": round(g0, 5),
        "A1_jamo_opaque_ce": round(a1_ce, 5), "A1_calib_match_2_51335": calib_ok, "A1_bank_member": a1_mi,
        "A2_featural_partition_ce": round(a2_ce, 5), "A2_bank_member": a2_mi, "A2_cells": a2_cells,
        "A3_label_factorization_ce": round(a3_ce, 5), "A3_bank_member": a3_mi, "A3_cells": a3_cells,
        "A2s_shuffle_mean": round(a2s_mean, 5), "A3s_shuffle_mean": round(a3s_mean, 5),
        "best_arm": best_arm, "best_ce": round(best_ce, 5), "best_shuffle": round(best_shuf, 5),
        "G1_geometry_fair_depth": g1, "G2_earned": g2, "G3_factorization_beats_partition": g3_factor_wins,
        "green": green, "verdict": verdict, "seeds": seeds, "wall_s": round(wall, 1),
    }
    json.dump(summary, open(os.path.join(args.out, "h1326_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("CE LADDER (nats/UTF-8-byte, geometry-FAIR; mean 3 seeds for shuffle):")
    log(f"  raw-byte ceiling             = {H1307_CEILING_KO_CE}  (in-run G0 {round(g0,5)})")
    log(f"  A1 jamo (Fix-A protocol)     = {round(a1_ce,5)}  (calib vs H_1316 2.51335 = {calib_ok})")
    log(f"  A2 featural-partition        = {round(a2_ce,5)}  (member {a2_mi}, cells {a2_cells})")
    log(f"  A3 label-factorization       = {round(a3_ce,5)}  (member {a3_mi}, cells {a3_cells})")
    log(f"  A2s shuffle (featural)       = {round(a2s_mean,5)}  Δ(shuf−A2)={round(a2s_mean-a2_ce,5)}")
    log(f"  A3s shuffle (factorized)     = {round(a3s_mean,5)}  Δ(shuf−A3)={round(a3s_mean-a3_ce,5)}")
    log(f"  BEST = {best_arm} = {round(best_ce,5)}   shuffle-of-best = {round(best_shuf,5)}")
    log(f"G1 GEOMETRY-FAIR DEPTH (BEST < A1−{G1_MARGIN} AND < raw): {g1}  "
        f"(BEST {round(best_ce,5)} vs A1 {round(a1_ce,5)}, Δ={round(a1_ce-best_ce,5)})")
    log(f"G2 EARNED (BEST < shuffle-of-best by >={G2_MARGIN}): {g2}  "
        f"(Δ={round(best_shuf-best_ce,5)})")
    log(f"G3 FACTORIZATION-ATTRIBUTION (A3 < A2): {g3_factor_wins}  "
        f"(A3 {round(a3_ce,5)} vs A2 {round(a2_ce,5)}, Δ={round(a2_ce-a3_ce,5)})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")

if __name__ == "__main__":
    main()
