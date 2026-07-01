"""beta_readout.py — H_1822 (β) substrate-native recombination, SEMANTIC embed.

ROUND r2 (β-readout). r1 (α, engine-native, probe.hexa) verdict = 🧱: the
substrate ALSO floors at the engine's OWN novelty radius (0/5), measured over
concept basins embedded by `immune_embed_key` = a char-trigram FNV hash =
NON-semantic / lexical. So "rain"+"bow"->"rainbow" shared only SURFACE trigrams,
not meaning. r1 NAMED this exact round: re-run the IDENTICAL substrate-G1 test,
but embed each concept via the 303M mouth TRUNK PENULTIMATE (learned SEMANTIC
vector) instead of the char-hash, to separate

   "substrate has compositional concept geometry"  (testable on learned reps)
   from "char-trigram lexical overlap"             (r1's confound).

DECISIVE QUESTION: does the SEMANTIC trunk embedding LIFT substrate-G1 where the
char-hash FLOORED (0/5)?
  YES (semantic >=2 on >=2/5, clean controls) -> missing piece is semantic concept
      representation feeding the substrate -> directional support for β engine-grown
      mouth (owner's insight, refined).
  NO  (semantic ALSO 0/5) -> 🧱 hardens: the COMBINATION machinery (the VAdaptField
      Voronoi metric) is non-compositional even WITH semantic concepts (consistent
      w/ H_1310 depth-0); lever is the combination OPERATOR, not the embedding.

SCOPE HONESTY (c9 / a_engine_native_learning): the embedding step uses
core/clm_decode.py (the byte-faithful CLMConvMoE forward, py 2-production mirror
of clm_decode.hexa) to get the trunk penultimate `yn` -> this round is
**DIRECTIONAL** (py mirror for the SEMANTIC EMBED step). The substrate-G1 metric
itself is the SAME L2-affinity / nearest-2-basin geometry the engine's
VAdaptField uses (vadapt_field_two_recon_err: dist to nearest & 2nd-nearest
basin), re-implemented in numpy here over semantic vectors (no torch). We report
this gap explicitly; a fully engine-native β would need a core/ op that feeds
trunk-penultimate vectors into VAdaptField (named, not built).

FROZEN-FIRST (p7, pre-registered — NO sliding to manufacture a pass):
  Two radii, IDENTICAL logic to r1 (probe.hexa):
   (1) engine's OWN absolute novelty radius SPLIT_THRESH = 0.30
       (vadapt_field_step:578). To make this meaningful on the SAME unit-sphere
       geometry r1 used (immune_embed_key returns UNIT keys), we L2-NORMALIZE the
       trunk penultimate concept vectors -> distances live on the unit sphere,
       0.30 is the same operating point as r1.
   (2) relative radius d_ab = inter-parent distance (the weaker "bridge-between"
       criterion). Scale-free.
  substrate_G1(r) = 1 iff composed_distinct(r) >= 2 AND irreducible(d1>eps).
  Raw d1,d2,d_ab ALWAYS printed (c2: measure-or-it-didn't-happen).

CONTROLS (same as r1):
  single  : composed = parentA alone -> irreducible FALSE (d1~0) -> G1=0
  shuffle : parentB -> UNRELATED concept -> child should NOT bridge both -> < MAIN
  contrast: SEMANTIC substrate-G1 vs r1 CHAR-HASH substrate-G1 on the SAME 5 pairs
            (char-hash recomputed here in numpy = FNV trigram unit key, the same
             64-dim hashing immune_embed_key:1003 does).

Usage:
  python3 beta_readout.py [<ckpt.clm>]   # default = local clm303 303M
"""

import sys
import os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.abspath(os.path.join(_HERE, "..", "..", "core"))
sys.path.insert(0, _CORE)
import clm_decode as cd  # byte-faithful CLMConvMoE forward (py 2-production)

T = 24                 # decode window (clm_decode.hexa)
SPLIT_THRESH = 0.30    # engine's OWN novelty radius (vadapt_field_step:578)
EPS = 1e-6

DEFAULT_CLM = "/Users/mini/dancinlab/anima/state/clm303_savant_mitosis_train/clm303.clm"

# genuine recombination triples — IDENTICAL to r1 probe.hexa MAIN pairs
PAIRS = [
    ("rain",  "bow",    "rainbow"),
    ("snow",  "man",    "snowman"),
    ("sun",   "flower", "sunflower"),
    ("fire",  "fly",    "firefly"),
    ("water", "fall",   "waterfall"),
]
# unrelated basins for shuffle control — IDENTICAL to r1 probe.hexa
UNRELATED = ["zqxkj", "wovbm", "plktn", "grdfh", "ymcqs"]


# ════════════════════════════════════════════════════════════════════════
# (A) SEMANTIC embed: 303M trunk penultimate, mean-pooled over concept bytes
# ════════════════════════════════════════════════════════════════════════

def _penultimate(W, tok, T):
    """yn:[T,d] = CLMConvMoE trunk penultimate (post final-groupnorm, pre
    readout). 1:1 with clm_decode._fwd_logits / he_probe._penultimate."""
    d = W["d"]; E = W["E"]; K = W["K"]; L = W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = cd._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = cd._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = cd.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = cd.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil = dil * 2
    logits_r = cd._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = cd._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out[ej] = cd.nn_gelu_fwd(eo).reshape(T, d)
    y = cd.nn_moe_router_fwd(logits_r, ex_out, T, E, d)
    yn = cd.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    return yn  # [T, d]


def _semantic_rep(W, s):
    """r(concept) = MEAN-POOLED trunk penultimate over the concept's own bytes,
    right-aligned in the T=24 causal window (pad-left byte 32). Mean-pool over
    the concept positions (per-prompt spec). Returns [d]."""
    sb = s.encode("utf-8", "surrogateescape")
    slen = len(sb)
    tok = np.empty(T, dtype=np.float64)
    concept_positions = []
    for p in range(T):
        si = slen - T + p
        if si >= 0:
            tok[p] = float(sb[si])
            concept_positions.append(p)
        else:
            tok[p] = 32.0
    yn = _penultimate(W, tok, T)              # [T, d]
    pos = concept_positions if concept_positions else [T - 1]
    return yn[pos].mean(axis=0)               # [d]  mean over concept bytes


# ════════════════════════════════════════════════════════════════════════
# (B) CHAR-HASH embed: FNV char-trigram UNIT key — numpy mirror of
#     immune_embed_key (core/engine_cli.hexa:1003), for the r1 contrast.
# ════════════════════════════════════════════════════════════════════════

def _charhash_rep(s, dim=64):
    """64-dim char-trigram FNV unit key — the SAME embedding family r1 used
    (immune_embed_key). FNV-1a over each 3-gram, bucket into `dim`, L2-unit.
    numpy mirror (no engine call); used ONLY for the contrast column."""
    v = np.zeros(dim, dtype=np.float64)
    b = s.encode("utf-8", "surrogateescape")
    n = len(b)
    if n == 0:
        return v
    for i in range(n):
        c0 = b[i]
        c1 = b[i + 1] if i + 1 < n else 0
        c2 = b[i + 2] if i + 2 < n else 0
        h = 1469598103934665603
        for c in (c0, c1, c2):
            h ^= c
            h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        v[h % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


# ════════════════════════════════════════════════════════════════════════
# substrate-G1 metric — IDENTICAL logic to r1 probe.hexa, over given basins
# ════════════════════════════════════════════════════════════════════════

def _l2(a, b):
    return float(np.linalg.norm(a - b))


def measure_triple(basin_a, basin_b, child_vec):
    """d1,d2 = dist child->nearest & 2nd-nearest parent basin; d_ab inter-parent;
    composed_distinct & substrate_G1 at BOTH radii. SAME logic as probe.hexa."""
    da = _l2(child_vec, basin_a)
    db = _l2(child_vec, basin_b)
    d1, d2 = (da, db) if da <= db else (db, da)   # nearest, 2nd-nearest
    d_ab = _l2(basin_a, basin_b)
    cd_eng = int(d1 < SPLIT_THRESH) + int(d2 < SPLIT_THRESH)
    cd_rel = int(d1 < d_ab) + int(d2 < d_ab)
    irred = d1 > EPS
    g1_eng = 1 if (cd_eng >= 2 and irred) else 0
    g1_rel = 1 if (cd_rel >= 2 and irred) else 0
    return dict(d1=d1, d2=d2, d_ab=d_ab, irred=irred,
                cd_eng=cd_eng, cd_rel=cd_rel, g1_eng=g1_eng, g1_rel=g1_rel)


def _unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ════════════════════════════════════════════════════════════════════════
# self-test — prove the metric SEPARATES a planted composition from random
# (so a 0/5 below is a real floor, not a dead metric)
# ════════════════════════════════════════════════════════════════════════

def self_test(seed=0, d=64):
    """Validity check on the rel-radius metric. Plant TWO close parents (so d_ab
    is small) and ask: does a true MIDPOINT child (genuinely between them) fire,
    while a child PLACED ON ONE PARENT but pushed AWAY from the other (i.e. NOT a
    bridge) does NOT? With small d_ab the rel-radius is a real discriminator.
    (Random unit vectors in high-d are ALL ~sqrt2 apart, so a wide-d_ab test is
    non-discriminating by construction — that very degeneracy is part of the β
    finding for the semantic arm; see note in RESULT_BETA.md.)"""
    rng = np.random.default_rng(seed)
    base = _unit(rng.standard_normal(d))
    perturb = _unit(rng.standard_normal(d))
    a = _unit(base + 0.30 * perturb)               # two CLOSE parents
    b = _unit(base - 0.30 * perturb)               # small d_ab
    child_bridge = _unit((a + b) / 2.0)            # TRUE midpoint -> near BOTH
    child_offaxis = _unit(a + 1.2 * perturb)       # near a, FAR from b -> not bridge
    m_bridge = measure_triple(a, b, child_bridge)
    m_off = measure_triple(a, b, child_offaxis)
    sep = (m_bridge["g1_rel"] == 1) and (m_off["g1_rel"] == 0)
    return dict(bridge=m_bridge, off=m_off, SEPARATES=sep)


# ════════════════════════════════════════════════════════════════════════
def run_arm(name, embed_fn, label_fn):
    print("── %s ──" % name)
    se = sr = 0
    for i, (pa, pb, child) in enumerate(PAIRS):
        a = embed_fn(pa)
        b, ch = label_fn(i, embed_fn, pa, pb, child)
        m = measure_triple(a, b, ch)
        se += m["g1_eng"]; sr += m["g1_rel"]
        print("  pair%d [%s + %s -> %s]" % (i, pa, pb, child))
        print("    d1=%.4f  d2=%.4f  d_ab=%.4f  irreducible=%s"
              % (m["d1"], m["d2"], m["d_ab"], "YES" if m["irred"] else "no"))
        print("    radius(eng=0.30): composed_distinct=%d  substrate_G1=%d"
              % (m["cd_eng"], m["g1_eng"]))
        print("    radius(rel=d_ab): composed_distinct=%d  substrate_G1=%d"
              % (m["cd_rel"], m["g1_rel"]))
    print("  >>> %s substrate_G1  (eng-radius 0.30): %d/%d   (rel-radius d_ab): %d/%d"
          % (name, se, len(PAIRS), sr, len(PAIRS)))
    print()
    return se, sr


def _main_label(i, embed_fn, pa, pb, child):
    return embed_fn(pb), embed_fn(child)            # real parentB, real child

def _single_label(i, embed_fn, pa, pb, child):
    return embed_fn(pb), embed_fn(pa)               # child = parentA alone

def _shuffle_label(i, embed_fn, pa, pb, child):
    return embed_fn(UNRELATED[i]), embed_fn(child)  # parentB -> unrelated


def main(argv):
    ck = argv[1] if len(argv) > 1 else DEFAULT_CLM
    print("=" * 72)
    print("H_1822 (β) substrate-native recombination — SEMANTIC trunk embed")
    print("  DIRECTIONAL: embed step uses core/clm_decode.py (py mirror) trunk")
    print("  penultimate; substrate-G1 metric = numpy L2-affinity (no torch).")
    print("=" * 72)

    print("\n[0] METRIC SELF-TEST (planted bridge vs random far point)")
    st = self_test()
    print("    bridge (true midpoint): g1_rel=%d (d1=%.4f d2=%.4f d_ab=%.4f)"
          % (st["bridge"]["g1_rel"], st["bridge"]["d1"], st["bridge"]["d2"], st["bridge"]["d_ab"]))
    print("    off-axis (near a, far b): g1_rel=%d (d1=%.4f d2=%.4f d_ab=%.4f)"
          % (st["off"]["g1_rel"], st["off"]["d1"], st["off"]["d2"], st["off"]["d_ab"]))
    print("    SEPARATES (fires on a true bridge, NOT on an off-axis non-bridge): %s"
          % ("PASS" if st["SEPARATES"] else "FAIL"))

    if not cd.clm_decodable(ck):
        print("\n!! ckpt not v0.2-decodable:", ck)
        return 1
    print("\n[1] loading 303M trunk:", os.path.basename(ck))
    W = cd.clm_load_weights(ck)
    print("    d=%d E=%d K=%d L=%d" % (W["d"], W["E"], W["K"], W["L"]))

    sem_cache = {}
    def sem_embed(s):
        if s not in sem_cache:
            sem_cache[s] = _unit(_semantic_rep(W, s))
        return sem_cache[s]

    def char_embed(s):
        return _charhash_rep(s)

    print("\n[2] SEMANTIC arms (303M trunk penultimate concept basins)")
    sem_main = run_arm("SEMANTIC MAIN (real compounds)", sem_embed, _main_label)
    sem_single = run_arm("SEMANTIC CONTROL single", sem_embed, _single_label)
    sem_shuf = run_arm("SEMANTIC CONTROL shuffle", sem_embed, _shuffle_label)

    print("[3] CHAR-HASH arms (r1 immune_embed_key mirror — SAME 5 pairs)")
    ch_main = run_arm("CHAR-HASH MAIN (real compounds)", char_embed, _main_label)
    ch_single = run_arm("CHAR-HASH CONTROL single", char_embed, _single_label)
    ch_shuf = run_arm("CHAR-HASH CONTROL shuffle", char_embed, _shuffle_label)

    print("=" * 72)
    print("CONTRAST — SEMANTIC vs CHAR-HASH substrate-G1 on the SAME 5 pairs")
    print("=" * 72)
    print("                          eng-radius 0.30   rel-radius d_ab")
    print("  SEMANTIC  MAIN          %d/5              %d/5"  % (sem_main[0], sem_main[1]))
    print("  CHAR-HASH MAIN          %d/5              %d/5"  % (ch_main[0], ch_main[1]))
    print("  SEMANTIC  single(ctrl)  %d/5              %d/5"  % (sem_single[0], sem_single[1]))
    print("  CHAR-HASH single(ctrl)  %d/5              %d/5"  % (ch_single[0], ch_single[1]))
    print("  SEMANTIC  shuffle(ctrl) %d/5              %d/5"  % (sem_shuf[0], sem_shuf[1]))
    print("  CHAR-HASH shuffle(ctrl) %d/5              %d/5"  % (ch_shuf[0], ch_shuf[1]))
    print()
    print("  mouth-decode G1 (clm_decode CLMConvMoE) = 0  [FROZEN FLOOR H_1818/H_1602]")
    print()

    lifted_eng = sem_main[0] >= 2 and sem_single[0] == 0 and sem_shuf[0] < sem_main[0]
    print("=" * 72)
    print("DECISIVE QUESTION — did SEMANTIC lift substrate-G1 @ engine radius 0.30?")
    print("  char-hash MAIN @ eng 0.30 = %d/5 (r1 floor)" % ch_main[0])
    print("  semantic  MAIN @ eng 0.30 = %d/5" % sem_main[0])
    if lifted_eng:
        print("  => YES: semantic >=2/5 @ operating point WITH clean controls")
        print("     (single=0, shuffle<MAIN) -> missing piece = semantic concept rep.")
    else:
        print("  => NO: semantic does NOT lift @ the engine operating point.")
        print("     The COMBINATION operator (VAdaptField Voronoi) is non-compositional")
        print("     even WITH semantic concepts (consistent w/ H_1310 depth-0).")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
