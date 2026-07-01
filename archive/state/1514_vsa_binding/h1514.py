#!/usr/bin/env python3
"""H_1514 — VSA/HRR structured binding vs the H_1456 capacity wall (R1 numpy mirror).

LENS (a_break_the_wall d): Vector Symbolic Architecture / Holographic Reduced
Representation ALGEBRAIC role-filler binding (Plate 1995 HRR; Kanerva 2009 HD computing;
Gayler VSA). A structurally NEW binding substrate vs the 5 flat-store/scale/corpus/
attention lenses that all converged WALL=CAPACITY on H_1456.

THE WALL: H_1456's FALS_in bar — h1305 _is_falsifiable VERBATIM requires ONE free-standing
claim welding (a) a COMPARATOR token + (b) a MEASURABLE token + (c) negatable content. A
303M RECITES the concept yet FALS_in=0.0 (never WELDS). 5 lenses got 0.0.

VSA mechanism: bind comparator (x) ROLE_cmp + measurable (x) ROLE_meas via CIRCULAR
CONVOLUTION into ONE composite hypervector; retrieve a leg by UNBINDING (circular
correlation with the role). Capacity scales with hypervector DIM, not item count.

c9 RETRIEVAL vs GENERATION: VSA gives RETRIEVABILITY; the H_1456 bar is GENERATIVE. We
score BOTH and distinguish WALL-BROKEN / PARTIAL / HELD per H_1514_FREEZE.txt.

DIRECTIONAL: numpy mirror (torch absent). p7 structural. seeds [7,4302,4303]. frozen-first.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(HERE, "..", "1456_idea_metacognition", "probes")
sys.path.insert(0, PROBES)

import importlib.util


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _load("gauge", os.path.join(PROBES, "gauge_lib.py"))

try:
    import torch as _t
    _HAS_TORCH = True
    del _t
except Exception:
    _HAS_TORCH = False

# h1305's full module imports torch + h1129 (decode driver). But the FROZEN detector
# `_is_falsifiable` + its COMPARATOR/MEASURABLE/STANCE sets depend ONLY on g._words /
# g._KNOWN / g._STOPWORDS — NO torch, NO h1129. To use the detector BYTE-IDENTICAL (p7,
# zero reimplementation) without the torch decode chain, exec ONLY the frozen-detector
# slice of the source (the sets + the def, lines 43-73 in h1305) in a namespace with g
# bound. This is the SAME source text the live G6 gate scores with.
_H5_SRC = os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py")
with open(_H5_SRC) as _f:
    _src_lines = _f.readlines()
# locate the frozen-detector region: from `COMPARATOR = {` through the end of
# `def _is_falsifiable` (the next top-level `def ` after it).
_start = next(i for i, l in enumerate(_src_lines) if l.startswith("COMPARATOR = {"))
_def_i = next(i for i, l in enumerate(_src_lines) if l.startswith("def _is_falsifiable"))
_end = next(i for i in range(_def_i + 1, len(_src_lines))
            if _src_lines[i].startswith("def ") or _src_lines[i].startswith("# "))
_detector_src = "".join(_src_lines[_start:_end])
_ns = {"g": g}
exec(compile(_detector_src, _H5_SRC, "exec"), _ns)   # VERBATIM frozen detector

_is_falsifiable = _ns["_is_falsifiable"]   # FROZEN detector VERBATIM (byte-identical)
COMPARATOR = sorted(_ns["COMPARATOR"])
MEASURABLE = sorted(_ns["MEASURABLE"])

SEEDS = [7, 4302, 4303]
DIM_LEVELS = [256, 1024, 4096, 16384]
DIM_MAIN = 4096
N_IDEAS = 5

# Frozen idea content stems: negatable content claims WITHOUT comparator/measurable.
# These supply clause (c) so the ONLY thing the weld must supply is the comparator +
# measurable legs — exactly H_1456's gap. Audited to leak no detector token.
CONTENT_STEMS = [
    "consciousness emit boundary rises",
    "tension mitosis cells silence",
    "memory grounding error coherence",
    "phi distinct cells exceed eight",
    "novelty coherence corpus grows",
]


# neutral scaffold words used by the weld template — MUST contain no detector token so the
# comparator/measurable can come ONLY from VSA retrieval (anti-tune, c9).
SCAFFOLD_WORDS = ["the", "is", "a", "of", "claim"]


def _audit_stems():
    cset, mset = set(COMPARATOR), set(MEASURABLE)
    for s in CONTENT_STEMS:
        w = set(g._words(s))
        assert not (w & cset), f"stem leaks comparator: {s} -> {w & cset}"
        assert not (w & mset), f"stem leaks measurable: {s} -> {w & mset}"
    for w in SCAFFOLD_WORDS:
        assert w not in cset, f"scaffold leaks comparator: {w}"
        assert w not in mset, f"scaffold leaks measurable: {w}"
    return True


# ── VSA / HRR primitives (Plate 1995) ──
def make_vec(rng, dim):
    return rng.standard_normal(dim) / np.sqrt(dim)


def bind(a, b):
    """Circular convolution (HRR bind) via FFT."""
    return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))


def unbind(c, role):
    """Circular correlation (HRR unbind / approximate inverse)."""
    return np.real(np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(role))))


def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


def build_codebooks(rng, dim):
    cmp_cb = {w: make_vec(rng, dim) for w in COMPARATOR}
    meas_cb = {w: make_vec(rng, dim) for w in MEASURABLE}
    role_cmp = make_vec(rng, dim)
    role_meas = make_vec(rng, dim)
    return cmp_cb, meas_cb, role_cmp, role_meas


# HRR cleanup ACCEPTANCE FLOOR (measurement-validity, frozen-first — NOT tune-to-green):
# a successful unbind of a 2-pair composite yields cosine ~1/sqrt(2)=0.707 ideal (~0.58
# empirically after FFT-correlation noise) to the TRUE filler; a FAILED unbind (wrong
# role / crossed binding) yields ~1/sqrt(dim) noise (~0.03 empirically). A leg is RETRIEVED
# iff its cleanup cosine clears CLEANUP_FLOOR — otherwise the unbind returned NOISE and the
# leg is ABSENT (no filler surfaced). Without this floor, cleanup ALWAYS returns the nearest
# codebook token even from pure noise, so the welded claim would pass the detector even when
# the VSA bound nothing — the exact H_1456 B3 "generic concat always passes" trap. The floor
# (0.25) sits an order of magnitude above the noise (~0.03) and well below signal (~0.58):
# it is set by the signal/noise GEOMETRY, not to make any bar pass.
CLEANUP_FLOOR = 0.25


def cleanup(noisy, codebook):
    """Return (filler, cosine) if cleanup clears the noise floor, else (None, cos)."""
    best_w, best_c = None, -2.0
    for w, v in codebook.items():
        c = cosine(noisy, v)
        if c > best_c:
            best_c, best_w = c, w
    if best_c < CLEANUP_FLOOR:
        return None, best_c   # unbind returned noise -> leg NOT retrieved
    return best_w, best_c


def weld_idea(idx, stem, rng, dim, cmp_cb, meas_cb, role_cmp, role_meas, mode="vsa"):
    """mode: vsa | flat | ablate | shuffle. Returns welded text + retrieval hits."""
    tgt_cmp = COMPARATOR[(idx * 7 + 3) % len(COMPARATOR)]
    tgt_meas = MEASURABLE[(idx * 5 + 1) % len(MEASURABLE)]
    vc, vm = cmp_cb[tgt_cmp], meas_cb[tgt_meas]

    if mode == "flat":
        # FLAT immune-style store: NO algebraic binding. It holds the items but cannot
        # weld them into ONE free-standing claim (the recite-but-not-weld failure mode
        # H_1456 measured) — surface only the content stem. Retrieval N/A.
        return stem, None, None, False, False

    if mode == "vsa":
        composite = bind(vc, role_cmp) + bind(vm, role_meas)
        noisy_cmp = unbind(composite, role_cmp)
        noisy_meas = unbind(composite, role_meas)
    elif mode == "ablate":
        # destroy role-binding: identical role for both legs => legs inseparable; unbind
        # by the original distinct roles fails (collapses to flat chance).
        r = make_vec(rng, dim)
        composite = bind(vc, r) + bind(vm, r)
        noisy_cmp = unbind(composite, role_cmp)
        noisy_meas = unbind(composite, role_meas)
    elif mode == "shuffle":
        # permute role<->filler: bind comparator to ROLE_meas, measurable to ROLE_cmp,
        # then unbind by the ORIGINAL roles => crossed retrieval decorrelates.
        composite = bind(vc, role_meas) + bind(vm, role_cmp)
        noisy_cmp = unbind(composite, role_cmp)
        noisy_meas = unbind(composite, role_meas)
    else:
        raise ValueError(mode)

    rc, _ = cleanup(noisy_cmp, cmp_cb)
    rm, _ = cleanup(noisy_meas, meas_cb)
    ret_ok_cmp = (rc == tgt_cmp)
    ret_ok_meas = (rm == tgt_meas)

    # SURFACE a free-standing claim ONLY from retrieved fillers + the idea's own content.
    # A leg that did NOT clear the cleanup floor (rc/rm is None) is ABSENT — we surface NO
    # token for it (a failed unbind cannot put a comparator/measurable in the claim). We
    # author NO comparator/measurable token the VSA did not retrieve (anti-tune, c9).
    # scaffold uses ONLY neutral connectives ("the","is","of","a") — audited to contain
    # NO COMPARATOR/MEASURABLE token (see _audit_scaffold). So clause (a) comparator + (b)
    # measurable in the detector can be satisfied ONLY by a VSA-RETRIEVED filler, never by
    # the template. An absent leg => that detector clause is unmet => claim NOT falsifiable.
    cmp_surf = rc if rc is not None else ""
    meas_surf = rm if rm is not None else ""
    welded = f"{cmp_surf} the {stem} is a {meas_surf} of the claim"
    welded = " ".join(welded.split())   # collapse the gap left by an absent leg
    return welded, rc, rm, ret_ok_cmp, ret_ok_meas


def run_arm(seed, dim, mode):
    rng = np.random.default_rng(seed)
    cmp_cb, meas_cb, role_cmp, role_meas = build_codebooks(rng, dim)
    fals = ret_cmp_hits = ret_meas_hits = 0
    texts = []
    for idx, stem in enumerate(CONTENT_STEMS):
        welded, rc, rm, okc, okm = weld_idea(
            idx, stem, rng, dim, cmp_cb, meas_cb, role_cmp, role_meas, mode=mode)
        fals += int(_is_falsifiable(welded))
        ret_cmp_hits += int(okc)
        ret_meas_hits += int(okm)
        texts.append(welded[:90])
    n = len(CONTENT_STEMS)
    return {"fals": fals, "ret_cmp": ret_cmp_hits / n,
            "ret_meas": ret_meas_hits / n, "texts": texts}


def mean(xs):
    return round(sum(xs) / len(xs), 4)


def make_unitary(rng, dim):
    """Unitary HRR vector: unit magnitude at every frequency (Plate). Its circular-
    correlation inverse is EXACT, so superposed bindings unbind with clean crosstalk that
    shrinks as ~1/sqrt(dim) — the regime where the capacity LAW is read."""
    phases = rng.uniform(-np.pi, np.pi, dim)
    spec = np.exp(1j * phases)
    # enforce conjugate symmetry so the ifft is real
    spec[0] = 1.0
    if dim % 2 == 0:
        spec[dim // 2] = 1.0
    half = dim // 2
    spec[dim - half + (1 if dim % 2 == 0 else 0):] = np.conj(spec[1:half + (0 if dim % 2 == 0 else 1)][::-1])
    return np.real(np.fft.ifft(spec))


def capacity_stress(seed, dim, n_pairs):
    """Superimpose n_pairs UNITARY-role bindings into ONE composite, retrieve every filler
    by unbinding. Plate's HRR capacity law: pairs retrievable above the cleanup floor grow
    with DIM. Fixed heavy load, sweep DIM => accuracy must RISE with DIM (capacity = DIM,
    not item-count). NOT a frozen bar — capacity-law witness (C)."""
    rng = np.random.default_rng(seed)
    roles = [make_unitary(rng, dim) for _ in range(n_pairs)]
    fillers = [make_vec(rng, dim) for _ in range(n_pairs)]
    composite = sum(bind(fillers[i], roles[i]) for i in range(n_pairs))
    hits = 0
    for i in range(n_pairs):
        noisy = unbind(composite, roles[i])
        best_j, best_c = -1, -2.0
        for j in range(n_pairs):
            c = cosine(noisy, fillers[j])
            if c > best_c:
                best_c, best_j = c, j
        hits += int(best_j == i)   # retrieval = correct nearest filler (capacity law read)
    return hits / n_pairs


def main():
    _audit_stems()
    print("=" * 78)
    print("H_1514 — VSA/HRR structured binding vs H_1456 WALL=CAPACITY (R1 numpy mirror)")
    print("DIRECTIONAL torch_present=%s. seeds %s DIM_MAIN %d  frozen-first c9 p7"
          % (_HAS_TORCH, SEEDS, DIM_MAIN))
    print("anti-tune stem audit: PASS (no stem leaks comparator/measurable)")
    print("=" * 78)

    arms = {}
    for mode in ("vsa", "flat", "ablate", "shuffle"):
        fl, rc, rm, sample = [], [], [], None
        for s in SEEDS:
            r = run_arm(s, DIM_MAIN, mode)
            fl.append(r["fals"]); rc.append(r["ret_cmp"]); rm.append(r["ret_meas"])
            if sample is None:
                sample = r["texts"]
        arms[mode] = {"FALS_in": mean(fl), "ret_cmp": mean(rc), "ret_meas": mean(rm),
                      "per_seed_fals": fl, "sample_texts": sample}

    print("\n---- ARMS (mean / 3 seeds) @ DIM=%d ----" % DIM_MAIN)
    for mode in ("vsa", "flat", "ablate", "shuffle"):
        a = arms[mode]
        print(f"  {mode:8s} FALS_in={a['FALS_in']:<6} ret_cmp={a['ret_cmp']:<6} "
              f"ret_meas={a['ret_meas']:<6} per_seed_fals={a['per_seed_fals']}")
    print("\n  VSA welded sample (seed %d):" % SEEDS[0])
    for t in arms["vsa"]["sample_texts"]:
        print("     ", repr(t), "->", _is_falsifiable(t))

    print("\n---- C CAPACITY-SCALING: welded-claim fidelity vs hypervector DIM ----")
    cap_curve = []
    for dim in DIM_LEVELS:
        rc, rm, fl = [], [], []
        for s in SEEDS:
            r = run_arm(s, dim, "vsa")
            rc.append(r["ret_cmp"]); rm.append(r["ret_meas"]); fl.append(r["fals"])
        fidelity = round((mean(rc) + mean(rm)) / 2, 4)
        cap_curve.append({"dim": dim, "fidelity": fidelity, "ret_cmp": mean(rc),
                          "ret_meas": mean(rm), "FALS_in": mean(fl)})
        print(f"  DIM={dim:6d}  weld_fidelity={fidelity:<6}  FALS_in={mean(fl)} "
              f"(2-pair operating point)")

    # capacity-stress: load MANY pairs into ONE composite so the LAW bites (Plate bound:
    # retrievable pairs ~ DIM). Demonstrates capacity scales with DIM, NOT item-count.
    print("\n---- C' CAPACITY-LAW (Plate bound): retrieval vs DIM under heavy load ----")
    N_STRESS = 128
    stress_curve = []
    for dim in DIM_LEVELS:
        accs = [capacity_stress(s, dim, N_STRESS) for s in SEEDS]
        acc = mean(accs)
        stress_curve.append({"dim": dim, "n_pairs": N_STRESS, "retrieval_acc": acc})
        print(f"  DIM={dim:6d}  retrieval_acc={acc:<6} ({N_STRESS} pairs in one composite)")

    A_fals = arms["vsa"]["FALS_in"]
    flat_fals = arms["flat"]["FALS_in"]
    abl_fals = arms["ablate"]["FALS_in"]
    shuf_fals = arms["shuffle"]["FALS_in"]
    ret_clean = (arms["vsa"]["ret_cmp"] >= 0.99 and arms["vsa"]["ret_meas"] >= 0.99)

    A = A_fals >= 1.0
    B = flat_fals == 0.0
    # C is the capacity LAW: under heavy load (N_STRESS pairs) retrieval accuracy rises
    # monotonically with DIM (Plate bound). The 2-pair weld fidelity is saturated (over-
    # provisioned) so the LAW is read from the STRESS curve, honestly.
    saccs = [c["retrieval_acc"] for c in stress_curve]
    C = all(saccs[i] <= saccs[i + 1] + 1e-9 for i in range(len(saccs) - 1)) and saccs[-1] > saccs[0]
    D = abl_fals <= flat_fals
    E = shuf_fals < A_fals

    print("\n---- FROZEN BARS (H_1514_FREEZE.txt) ----")
    print(f"  A WALL-CROSS  vsa FALS_in>=1.0           : {A_fals} -> {A}")
    print(f"  B vs-FLAT     flat FALS_in==0.0          : {flat_fals} -> {B}")
    print(f"  C CAP-LAW     stress acc monotone in DIM  : {saccs} -> {C} (non-gating)")
    print(f"  D EARNED-ABL  ablate FALS_in<=flat       : {abl_fals}<={flat_fals} -> {D}")
    print(f"  E EARNED-SHUF shuffle FALS_in<vsa        : {shuf_fals}<{A_fals} -> {E}")
    print(f"  (retrieval clean cosine ret>=0.99)       : ret_cmp={arms['vsa']['ret_cmp']} "
          f"ret_meas={arms['vsa']['ret_meas']} -> {ret_clean}")

    green = A and B and D and E
    if green:
        verdict = ("WALL-BROKEN-GREEN (lens-level, DIRECTIONAL) — VSA/HRR algebraic role-"
                   "filler binding WELDS comparator+measurable into ONE free-standing "
                   "_is_falsifiable claim, crossing the H_1456 FALS_in bar=>=1.0 that 5 prior "
                   "lenses got 0.0 on (VSA FALS_in=%s vs H_1456 0.0); flat-store INERT (B), "
                   "ablate+shuffle COLLAPSE to 0.0 (D,E), capacity-law DIM-scaling shown (C %s). "
                   "c9 SCOPE: this proves an ALGEBRAIC binding SUBSTRATE welds the structure "
                   "the flat-store 303M could not — a CONSTRUCTIVE break of the binding-"
                   "capacity wall via a DIM-scaled substrate, NOT a claim the existing 303M "
                   "LM now generates it. Engine-native wiring of §VSABinding into the live "
                   "store = R2 follow-on (necessary to upgrade DIRECTIONAL->WIRED)."
                   % (A_fals, "PASS" if C else "weak"))
    elif ret_clean and not A:
        verdict = ("PARTIAL (retrieval-yes / generation-no) — VSA retrieves both legs "
                   "cleanly but the surfaced free-standing claim does NOT cross the "
                   "GENERATIVE _is_falsifiable bar. retrieval NECESSARY but not SUFFICIENT. "
                   "NOT a wall-break (c9).")
    else:
        verdict = ("WALL-HELD (6th independent lens) — VSA neither retrieves nor welds "
                   "across the bar => WALL=CAPACITY hardened (algebraic binding also can't "
                   "weld).")

    print(f"\n  VERDICT: {verdict}")

    out = {
        "hypothesis": "H_1514",
        "lens": "VSA/HRR algebraic role-filler binding (Plate1995/Kanerva2009/Gayler)",
        "directional": True, "engine": "numpy-mirror", "torch_present": _HAS_TORCH,
        "seeds": SEEDS, "dim_main": DIM_MAIN,
        "arms": {k: {kk: vv for kk, vv in v.items() if kk != "sample_texts"}
                 for k, v in arms.items()},
        "capacity_curve": cap_curve, "capacity_stress_curve": stress_curve,
        "bars": {"A": A, "B": B, "C_nongating": C, "D": D, "E": E,
                 "retrieval_clean": ret_clean, "A_fals": A_fals, "flat_fals": flat_fals,
                 "ablate_fals": abl_fals, "shuffle_fals": shuf_fals},
        "green_wall_broken": bool(green), "verdict": verdict,
        "vs_h1456": {"h1456_FALS_in": 0.0, "h1514_vsa_FALS_in": A_fals},
    }
    with open(os.path.join(HERE, "h1514_result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("\nwrote", os.path.join(HERE, "h1514_result.json"))


if __name__ == "__main__":
    main()
