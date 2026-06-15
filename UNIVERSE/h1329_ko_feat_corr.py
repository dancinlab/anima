#!/usr/bin/env python3
# h1329_ko_feat_corr.py — H_1329: does a CORRELATION-MODELING / JOINT-PRESERVING featural mechanism
# break BELOW the jamo 2.51335 floor, where H_1326's A3 INDEPENDENT-factorization backfired (3.073)
# and A2 partition-only was sub-floor (2.730)?
#
# THE DIAGNOSIS THIS LANE OVERTURNS-OR-CONFIRMS (H_1326 🧱, confound-free geometry-fair):
#   A1 jamo opaque-id (geometry-fair bank)              = 2.51335   (calibration anchor = the floor)
#   A2 featural-partition (opaque jamo target)          = 2.73046   (ABOVE jamo — partition help only)
#   A3 label-factorization P(class)·∏ P(f_c|class)      = 3.07295   (BACKFIRED — independence discards
#                                                                     the onset/nucleus/coda joint)
#   H_1326's named next angle: a DIFFERENT MECHANISM that models feature CORRELATIONS while KEEPING
#   the feature joint — a mechanism-FAMILY change, not a representation tweak.
#
# THE NEW MECHANISM (A4 — chosen candidate (i): CHAIN / CONDITIONAL FACTORIZATION; FREEZE justified):
#   A4 = a per-cell CONDITIONAL-CHAIN featural head over the SAME within-class feature columns as A3,
#   predicted in a CHAIN that respects Hangul's design hierarchy and KEEPS THE JOINT via conditioning:
#       A3 independent (joint discarded):  P(jamo) = P(class) · ∏_c P(f_c | class)
#       A4 chain      (joint kept):        P(jamo) = P(class) · P(f_0|class)
#                                                            · P(f_1|class, f_0)
#                                                            · P(f_2|class, f_0, f_1) ...  (full chain)
#   By the chain rule ∏_c P(f_c|class, f_<c) = P(f_0..f_{C-1}|class) EXACTLY → A4 keeps the joint A3
#   threw away. FEATURE-SIMILARITY STRENGTH SHARING: jamo sharing a feature prefix share the
#   conditioning context (ㄱ/ㅋ — one feature apart — share the articulator-conditioned manner head),
#   so similar jamo pool counts = the correlation-modeling the diagnosis named. SAME geometry-fair
#   bank (FIX A), SAME featural partition X (dim 11), SAME per-cell count-MLE + LAPLACE=1.0 — ONLY the
#   TARGET factorization changes (independent → conditional-chain).
#
#   LABEL = NOT gradient-free. A4 is a count-MLE STRUCTURED head (conditional counts + Laplace); it
#   rides the SAME gradient-free Voronoi partition (mitosis grow-op unchanged) but the per-cell head
#   is a structured count-MLE estimator. NO gradient training either. Labeled clearly; engine-transfer
#   = follow-on (a_engine_native_learning, a_verified_must_wire).
#
# GREEN iff (C1 BELOW-JAMO: A4 < jamo 2.51335 by >=0.03 AND < raw 2.95342)
#       AND (C2 EARNED: A4 < A4-shuffle by >=0.05)
#       AND (C3 ATTRIBUTION: A4 < A3 AND A4 < A2 — both reproduced in-run).
# C1 fail → jamo is the genuine cross-mechanism floor (stronger 🧱). C1∧¬C3 → features-not-joint (🟠).
#
# REAL Korean only (NO synthetic, p1-p8): SAME anima-7b R2 web corpus as H_1307 RUN A / H_1316 / H_1326.
# KO window sha256 ASSERTED == the H_1307 RUN A manifest hash. R2 keys env-only at fetch time (c7).
# SCALE-HONEST: toy/DIRECTIONAL; engine-transfer to live hexa = follow-on; NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e); sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316/H_1326) ───────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342
H1316_JAMO_CE = 2.51335
C1_MARGIN = 0.03
C2_MARGIN = 0.05
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
#  HANGUL FEATURAL DESIGN MAPS — LOSSLESS BIJECTIONS within each jamo class (verbatim from H_1326)
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
CLS_INIT, CLS_MED, CLS_FIN, CLS_BYTE = 0, 1, 2, 3
def _col_max(d):
    M = np.array(list(d.values())); return M.max(axis=0).tolist()
INIT_MAX = _col_max(CONS_FEAT)
MED_MAX  = _col_max(VOWEL_FEAT)
FIN_MAX  = _col_max(FINAL_FEAT)

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

# ── NO-CHEAT round-trip + accounting (same as H_1316/H_1326) ────────────────────
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
    """syms (jamo-id 256+rank or byte 0..255) · feats (N×5 within-class design vector) · nby ·
       depth · cls (factorized class id). Verbatim from H_1326 (so A2/A3 reproduce byte-exact)."""
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

# ── engine-native mitosis (BYTE-FAITHFUL to H_1306/H_1307/H_1316/H_1326) ────────
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

# ── OPAQUE-id per-byte CE (A1/A2 target = jamo id) verbatim from H_1326 ──────────
def per_byte_ce_opaque(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev):
    owner_tr = assign_all(centers_t, X_tr_t)
    Hmat = all_heads(Y_tr_t, owner_tr, centers_t.shape[0], ntr, vj, dev)
    owner_te = assign_all(centers_t, X_te_t)
    p = Hmat[owner_te, Y_te_t]; nll = -torch.log(p + 1e-12)
    nb = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    return nll.sum().item() / float(nb.sum().item())

# ── A3 INDEPENDENT-FACTORIZED per-byte CE (verbatim from H_1326; reproduced in-run for C3) ──
def per_byte_ce_factorized(centers_t, X_tr_t, ntr,
                           cls_tr, fcols_tr, sym_tr,
                           X_te_t, cls_te, fcols_te, sym_te, NB_te, dev):
    """A3: P(jamo) = P(class) · ∏_c P(f_c | class). INDEPENDENT per-column features (joint discarded)."""
    K = centers_t.shape[0]
    owner_tr = assign_all(centers_t, X_tr_t).cpu().numpy()[:ntr]
    owner_te = assign_all(centers_t, X_te_t).cpu().numpy()
    cls_tr_n = cls_tr.cpu().numpy()[:ntr]; fcols_tr_n = fcols_tr.cpu().numpy()[:ntr]
    sym_tr_n = sym_tr.cpu().numpy()[:ntr]
    cls_te_n = cls_te.cpu().numpy(); fcols_te_n = fcols_te.cpu().numpy()
    sym_te_n = sym_te.cpu().numpy(); nb_te_n = np.asarray(NB_te, np.float64)
    NCLS = 4; NCOL = 5
    GLOB = [max(INIT_MAX[c], MED_MAX[c], FIN_MAX[c]) + 1 for c in range(5)]
    col_card = {CLS_INIT: list(GLOB), CLS_MED: list(GLOB), CLS_FIN: list(GLOB)}
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

# ── A4 CONDITIONAL-CHAIN per-byte CE (THE NEW MECHANISM — joint kept via conditioning) ──────
def per_byte_ce_chain(centers_t, X_tr_t, ntr,
                      cls_tr, fcols_tr, sym_tr,
                      X_te_t, cls_te, fcols_te, sym_te, NB_te, dev):
    """A4: P(jamo) = P(class) · P(f_0|class) · P(f_1|class,f_0) · P(f_2|class,f_0,f_1) ...
       By the chain rule this EQUALS P(f_0..f_{C-1}|class) = P(jamo|class) EXACTLY → keeps the joint
       A3 discarded. Conditioning contexts are SHARED across feature-similar jamo (same feature prefix
       → same conditioning head) so similar jamo POOL counts = correlation/strength-sharing.

       Estimator (per Voronoi cell k, per class kc, per column c): a count table keyed by the cell +
       the PREFIX (f_0..f_{c-1}) → distribution over f_c, Laplace-smoothed. Unseen (cell,prefix) at
       test backs off to a Laplace-uniform over that column's cardinality (count==0 → all-Laplace row
       → uniform), so the chain is a proper distribution and the CE axis matches A1/A2/A3.
       BYTE class scored identically to A3: P(class=BYTE)·P(byte|class=BYTE) (256-way) — so the ONLY
       difference between A3 and A4 is the Hangul chain-vs-product, isolating the joint contribution."""
    K = centers_t.shape[0]
    owner_tr = assign_all(centers_t, X_tr_t).cpu().numpy()[:ntr]
    owner_te = assign_all(centers_t, X_te_t).cpu().numpy()
    cls_tr_n = cls_tr.cpu().numpy()[:ntr]; fcols_tr_n = fcols_tr.cpu().numpy()[:ntr]
    sym_tr_n = sym_tr.cpu().numpy()[:ntr]
    cls_te_n = cls_te.cpu().numpy(); fcols_te_n = fcols_te.cpu().numpy()
    sym_te_n = sym_te.cpu().numpy(); nb_te_n = np.asarray(NB_te, np.float64)
    NCLS = 4; NCOL = 5
    GLOB = [max(INIT_MAX[c], MED_MAX[c], FIN_MAX[c]) + 1 for c in range(5)]  # per-column cardinality

    # class head (same as A3)
    cls_cnt = np.full((K, NCLS), LAPLACE)
    byte_cnt = np.full((K, 256), LAPLACE)
    # CHAIN feature counts: chain_cnt[c] is a dict  (k, kc, prefix_tuple) -> np.array(card_c) counts.
    # prefix_tuple = (f_0..f_{c-1}); for c=0 the prefix is the empty tuple () → P(f_0|class).
    chain_cnt = [dict() for _ in range(NCOL)]

    for i in range(ntr):
        k = int(owner_tr[i]); kc = int(cls_tr_n[i]); cls_cnt[k, kc] += 1.0
        if kc == CLS_BYTE:
            byte_cnt[k, sym_tr_n[i]] += 1.0
        else:
            fv = fcols_tr_n[i]
            prefix = ()
            for c in range(NCOL):
                key = (k, kc, prefix)
                tbl = chain_cnt[c].get(key)
                if tbl is None:
                    tbl = np.full(GLOB[c], LAPLACE); chain_cnt[c][key] = tbl
                tbl[fv[c]] += 1.0
                prefix = prefix + (int(fv[c]),)

    cls_p = cls_cnt / cls_cnt.sum(axis=1, keepdims=True)
    byte_p = byte_cnt / byte_cnt.sum(axis=1, keepdims=True)

    total_nats = 0.0
    for i in range(owner_te.shape[0]):
        k = int(owner_te[i]); kc = int(cls_te_n[i])
        nll = -np.log(cls_p[k, kc] + 1e-12)
        if kc == CLS_BYTE:
            nll += -np.log(byte_p[k, sym_te_n[i]] + 1e-12)
        else:
            fv = fcols_te_n[i]
            prefix = ()
            for c in range(NCOL):
                key = (k, kc, prefix)
                tbl = chain_cnt[c].get(key)
                if tbl is None:
                    # unseen (cell,prefix): Laplace-uniform over card_c (proper back-off)
                    p_fc = 1.0 / GLOB[c]
                else:
                    p_fc = tbl[fv[c]] / tbl.sum()
                nll += -np.log(p_fc + 1e-12)
                prefix = prefix + (int(fv[c]),)
        total_nats += nll
    return total_nats / float(nb_te_n.sum())

# ── partition feature builders (verbatim from H_1326) ───────────────────────────
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

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank, identical to every arm) verbatim H_1326 ═══
BANK_GRID = [
    (0.3, 0.7, 0.0, 0.5),
    (0.3, 0.7, 0.3, 0.7),
    (0.5, 0.5, 0.0, 0.5),
    (0.25, 0.75, 0.0, 0.5),
    (0.4, 0.6, 0.2, 0.8),
]
def seed_bank(dim):
    bank = []
    for (lo, hi, alo, ahi) in BANK_GRID:
        a = [lo] * dim; a[-1] = alo
        b = [hi] * dim; b[-1] = ahi
        bank.append([a, b])
    a = [0.3] + [0.5] * (dim - 2) + [0.0] if dim >= 2 else [0.3]
    b = [0.7] + [0.5] * (dim - 2) + [0.5] if dim >= 2 else [0.7]
    if dim == 1: a = [0.3]; b = [0.7]
    bank.append([a, b])
    return bank

def grow_pick_bank(Xtr, Ytr, vj, dev, grow_max, dim):
    """FIX A: grow from EACH bank member on inner-train ONLY, pick the lowest inner-test CE (no test
       peeking), regrow the winner on the full train. Identical protocol for every arm → geometry-fair."""
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    n = Xtr.shape[0]; inner_idx = np.arange(n)
    ie = inner_idx % 2 == 0; io = inner_idx % 2 == 1
    best_ce = 1e18; best_member = -1
    for mi, seed in enumerate(seed_bank(dim)):
        Xie = torch.tensor(Xtr[ie], dtype=torch.float64, device=dev)
        Yie = torch.tensor(Ytr[ie], dtype=torch.int64, device=dev)
        Xio = torch.tensor(Xtr[io], dtype=torch.float64, device=dev)
        Yio = torch.tensor(Ytr[io], dtype=torch.int64, device=dev)
        c = grow_on(seed, Xie, Yie, Xie.shape[0], vj, dev, grow_max)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        nbio = np.ones(int(io.sum()))
        ce = per_byte_ce_opaque(ct, Xie, Yie, Xie.shape[0], Xio, Yio, nbio, vj, dev)
        if ce < best_ce: best_ce = ce; best_member = mi
    seed = seed_bank(dim)[best_member]
    c = grow_on(seed, Xtr_t, Ytr_t, n, vj, dev, grow_max)
    return c, best_member, best_ce

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4329,4330,4331")
    ap.add_argument("--out", default="/tmp/h1329_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu"); log("=== H_1329 — ko-feat-corr (conditional-chain joint-preserving featural) (CPU) ===")
    else:
        dev = torch.device("cuda"); cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1329 — ko-feat-corr (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} torch={torch.__version__}")
        _ = (torch.randn(256, 256, device=dev) @ torch.randn(256, 256, device=dev)).sum().item()
        torch.cuda.synchronize()

    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1326 ──
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
    cr, mr, _ = grow_pick_bank(Xtr_r, Ytr_r, 256, dev, args.grow_max, 3)
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

    # helper: opaque-target arm under the Fix-A bank protocol (A1, A2)
    def run_opaque_arm(X, Y, idx, nby, vj, dim, tag):
        NB = nby[idx]
        (Xtr, Ytr, NBtr), (Xte, Yte, NBte) = split_even_odd(X, Y, NB, stride=args.ko_stride)
        c, mi, tce = grow_pick_bank(Xtr, Ytr, vj, dev, args.grow_max, dim)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        ce = per_byte_ce_opaque(ct, torch.tensor(Xtr, dtype=torch.float64, device=dev),
                                torch.tensor(Ytr, dtype=torch.int64, device=dev), Xtr.shape[0],
                                torch.tensor(Xte, dtype=torch.float64, device=dev),
                                torch.tensor(Yte, dtype=torch.int64, device=dev), NBte, vj, dev)
        log(f"[{tag}] ce={round(ce,5)} cells={len(c)} bank_member={mi} train_proxy={round(tce,5)}")
        return ce, len(c), mi

    # helper: factorized/chain-target arm under the Fix-A bank protocol (A3, A4). `head` selects the
    # scoring estimator over IDENTICAL geometry/streams → A3 vs A4 isolates product-vs-chain (the joint).
    def run_struct_arm(syms, feats, depth, nby, cls, vj, tag, head):
        Xf, Yf, idxf = build_X_featural(syms, feats, depth, vj)
        NB = nby[idxf]; clsf = cls[idxf]; fcolsf = feats[idxf]; symf = syms[idxf]
        (Xtr, Ytr, NBtr, clstr, fctr, symtr), (Xte, Yte, NBte, clste, fcte, symte) = \
            split_even_odd(Xf, Yf, NB, clsf, fcolsf, symf, stride=args.ko_stride)
        c, mi, tce = grow_pick_bank(Xtr, Ytr, vj, dev, args.grow_max, Xf.shape[1])
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        ce = head(
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

    # ── A2 featural-partition + opaque target (reproduced for C3 attribution) ──
    Xf, Yf, idxf = build_X_featural(syms_i, feats_i, depth_i, VJ)
    a2_ce, a2_cells, a2_mi = run_opaque_arm(Xf, Yf, idxf, nby_i, VJ, Xf.shape[1], "A2 featural+opaque")

    # ── A3 INDEPENDENT label-factorization (reproduced for C3 attribution) ──
    a3_ce, a3_cells, a3_mi = run_struct_arm(syms_i, feats_i, depth_i, nby_i, cls_i, VJ,
                                            "A3 featural+independent-factorized", per_byte_ce_factorized)

    # ── A4 CONDITIONAL-CHAIN joint-preserving (THE NEW MECHANISM) ──
    a4_ce, a4_cells, a4_mi = run_struct_arm(syms_i, feats_i, depth_i, nby_i, cls_i, VJ,
                                            "A4 featural+conditional-chain (joint-preserving)", per_byte_ce_chain)

    # ── controls: shuffle feature map per seed → A4 shuffle (C2) ──
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    a4s_list = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        perm = rng.permutation(len(jamo_sorted))
        shuf_map = {cp: intact_map[jamo_sorted[perm[i]]] for i, cp in enumerate(jamo_sorted)}
        syms_s, feats_s, nby_s, depth_s, cls_s = make_streams(ko_text, jamo_to_id, shuf_map)
        a4s_ce, _, a4s_mi = run_struct_arm(syms_s, feats_s, depth_s, nby_s, cls_s, VJ,
                                           f"A4s chain-shuffle seed{sd}", per_byte_ce_chain)
        a4s_list.append(a4s_ce)
        log(f"[seed {sd}] " + json.dumps({"a4s": round(a4s_ce,5)}))
    a4s_mean = float(np.mean(a4s_list))

    # ── FROZEN bars C1/C2/C3 ──
    c1_vs_jamo = bool(a4_ce < (a1_ce - C1_MARGIN))
    c1_vs_raw = bool(a4_ce < H1307_CEILING_KO_CE)
    c1 = bool(c1_vs_jamo and c1_vs_raw)
    c2 = bool((a4s_mean - a4_ce) >= C2_MARGIN)
    c3_vs_a3 = bool(a4_ce < a3_ce)
    c3_vs_a2 = bool(a4_ce < a2_ce)
    c3 = bool(c3_vs_a3 and c3_vs_a2)
    green = bool(c1 and c2 and c3)
    if green:
        verdict = ("🟢 GREEN — a CORRELATION/JOINT-MODELING (conditional-chain) mechanism breaks BELOW the "
                   "jamo 2.51335 floor: the jamo floor was MECHANISM-SPECIFIC, Hangul's designed depth IS "
                   "exploitable once the mechanism keeps the joint (L2-Voronoi + independent-factorization "
                   "were the wrong mechanism; overturns H_1326 floor as mechanism-specific)")
    elif not c1:
        verdict = ("🧱 HONEST-FLOOR (cross-mechanism) — C1 fails: even a correlation/joint-modeling "
                   "(conditional-chain) mechanism does NOT beat the jamo floor by the bar → jamo is the "
                   "genuine decomposition FLOOR ACROSS mechanism families incl. correlation-modeling "
                   "(a deeper, stronger 🧱 closure than H_1326, c9)")
    elif c1 and not c3:
        verdict = ("🟠 FEATURES-NOT-JOINT — C1 holds but C3 fails: the gain is features per se (ties/loses "
                   "vs A2/A3), NOT the modeled joint/correlations (honest, c9)")
    else:
        verdict = ("🟠 C1∧C3 but C2 fails — DIMS-NOT-DESIGN: gain is dims/vocab not the designed "
                   "systematicity (shuffle ties; honest, c9)")

    wall = time.time() - t0
    summary = {
        "id": "H_1329", "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__, "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko), "ko_stride": args.ko_stride,
        "grow_max": args.grow_max, "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "design_feature_coverage": f"{n_jamo - len(missing)}/{n_jamo}",
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE, "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "g0_raw_byte_ce": round(g0, 5),
        "A1_jamo_opaque_ce": round(a1_ce, 5), "A1_calib_match_2_51335": calib_ok, "A1_bank_member": a1_mi,
        "A2_featural_partition_ce": round(a2_ce, 5), "A2_bank_member": a2_mi, "A2_cells": a2_cells,
        "A3_independent_factorization_ce": round(a3_ce, 5), "A3_bank_member": a3_mi, "A3_cells": a3_cells,
        "A4_conditional_chain_ce": round(a4_ce, 5), "A4_bank_member": a4_mi, "A4_cells": a4_cells,
        "A4s_chain_shuffle_mean": round(a4s_mean, 5), "A4s_per_seed": [round(x,5) for x in a4s_list],
        "delta_A4_vs_jamo": round(a4_ce - a1_ce, 5),
        "delta_A4_vs_A3": round(a4_ce - a3_ce, 5),
        "delta_A4_vs_A2": round(a4_ce - a2_ce, 5),
        "delta_shuffle_minus_A4": round(a4s_mean - a4_ce, 5),
        "C1_below_jamo": c1, "C1_vs_jamo": c1_vs_jamo, "C1_vs_raw": c1_vs_raw,
        "C2_earned": c2, "C3_attribution": c3, "C3_vs_A3": c3_vs_a3, "C3_vs_A2": c3_vs_a2,
        "green": green, "verdict": verdict, "seeds": seeds, "wall_s": round(wall, 1),
        "label_note": "A4 = count-MLE conditional-chain structured head; NOT gradient-free p8 mitosis, "
                      "NOT gradient-trained. Rides the same gradient-free Voronoi partition.",
    }
    json.dump(summary, open(os.path.join(args.out, "h1329_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("CE LADDER (nats/UTF-8-byte, geometry-FAIR; mean 3 seeds for shuffle):")
    log(f"  raw-byte ceiling             = {H1307_CEILING_KO_CE}  (in-run G0 {round(g0,5)})")
    log(f"  A1 jamo (Fix-A protocol)     = {round(a1_ce,5)}  (calib vs H_1316 2.51335 = {calib_ok})")
    log(f"  A2 featural-partition        = {round(a2_ce,5)}  (member {a2_mi}, cells {a2_cells})")
    log(f"  A3 independent-factorization = {round(a3_ce,5)}  (member {a3_mi}, cells {a3_cells})")
    log(f"  A4 conditional-chain (JOINT) = {round(a4_ce,5)}  (member {a4_mi}, cells {a4_cells})")
    log(f"  A4 shuffle (chain)           = {round(a4s_mean,5)}  Δ(shuf−A4)={round(a4s_mean-a4_ce,5)}")
    log(f"C1 BELOW-JAMO (A4 < A1−{C1_MARGIN} AND < raw): {c1}  "
        f"(A4 {round(a4_ce,5)} vs A1 {round(a1_ce,5)}, Δ={round(a1_ce-a4_ce,5)})")
    log(f"C2 EARNED (A4 < shuffle by >={C2_MARGIN}): {c2}  (Δ={round(a4s_mean-a4_ce,5)})")
    log(f"C3 ATTRIBUTION (A4 < A3 AND A4 < A2): {c3}  "
        f"(vs A3 Δ={round(a3_ce-a4_ce,5)}, vs A2 Δ={round(a2_ce-a4_ce,5)})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")

if __name__ == "__main__":
    main()
