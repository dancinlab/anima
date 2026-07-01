#!/usr/bin/env python3
"""rescore_dual.py — H_1458 dual-detector cross-shuffle re-scoring harness ($0 CPU, score-only).

Consumes DECODED G6 generations (text per (seed, arm, idx)) and scores each with BOTH the
FROZEN structural detector (H_1305) and the FROZEN semantic detector (H_1458), then computes
the cross-shuffle COLLAPSE for EACH detector on the SAME generations.

DECISIVE COMPARISON (the measurement-artifact test):
  For arm B_composed (earned idea-specific pairs) vs B_shuffle (cross-paired legs):
    collapse_struct = FALS_struct[composed] - FALS_struct[shuffle]
    collapse_sem    = FALS_sem[composed]    - FALS_sem[shuffle]
  H_1435 found collapse_struct ~ 0 (structural blind). The question:
    * collapse_sem  > collapse_struct  (semantic SEES a collapse structural misses)
        => the 5-lens WALL was a MEASUREMENT ARTIFACT (the model WAS binding; detector blind).
    * collapse_sem == collapse_struct ~ 0  (neither collapses)
        => CAPACITY ceiling reinforced (the model is NOT idea-specifically binding).

INPUT MODES:
  (A) --frags <glob...>   : engine-native / batch-cli fragment files, lines tagged
                            "<seed>|<arm>|<idx>\t<text>" (H_1305 engine-native format).
  (B) --result-json <f>   : a g6_common result.json with base/trained per_seed in_texts
                            (NB: in_texts are TRUNCATED to ~90 chars -> structural/semantic
                            FALS are LOWER-BOUNDS; use only as a smoke/illustration, NOT a verdict).
  (C) --decode <ckpt>     : decode live via gauge_lib._decode (needs torch+ckpt; e.g. on a pod).

ARMS (VERBATIM from h1305.build_frames): A_flat / B_composed / B_shuffle / B_ablate.
SEEDS = [7, 4302, 4303] (h1305 SEEDS).
"""
import os, sys, json, glob, re, importlib.util, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import semantic_detector as SD   # frozen dual detectors + frozen sets

g = SD.g
SEEDS = [7, 4302, 4303]
ARMS = ["A_flat", "B_composed", "B_shuffle", "B_ablate"]
KWR_FLOOR = 0.50


def score_text(t):
    """Return (coherent, struct_fals, sem_fals) for one generation."""
    if not t or g.known_word_ratio(t) < KWR_FLOOR:
        return (False, 0, 0)
    s = int(SD.is_falsifiable_structural(t))
    m = int(SD.is_falsifiable_semantic(t))
    return (True, s, m)


def aggregate(frags):
    """frags: dict[(seed,arm,idx)] -> text. Return per-arm mean struct/sem FALS over seeds."""
    per = {a: {"struct": [], "sem": [], "coh": []} for a in ARMS}
    # discover idx range per arm
    idxs = {a: sorted({k[2] for k in frags if k[1] == a}) for a in ARMS}
    for sr in SEEDS:
        for a in ARMS:
            sf = mf = co = 0
            for i in idxs[a] or range(5):
                t = frags.get((sr, a, i), "")
                c, s, m = score_text(t)
                co += int(c); sf += s; mf += m
            per[a]["struct"].append(sf)
            per[a]["sem"].append(mf)
            per[a]["coh"].append(co)
    mean = lambda xs: round(sum(xs) / len(xs), 4) if xs else 0.0
    out = {}
    for a in ARMS:
        out[a] = {"FALS_struct": mean(per[a]["struct"]),
                  "FALS_sem": mean(per[a]["sem"]),
                  "coherent": mean(per[a]["coh"])}
    return out


def report(label, agg):
    print(f"\n===== {label} — DUAL DETECTOR (mean/{len(SEEDS)} seeds) =====", flush=True)
    print(f"  {'arm':12s} {'coh':>5s} {'FALS_struct':>12s} {'FALS_sem':>10s}", flush=True)
    for a in ARMS:
        r = agg[a]
        print(f"  {a:12s} {r['coherent']:>5} {r['FALS_struct']:>12} {r['FALS_sem']:>10}", flush=True)
    cs = round(agg["B_composed"]["FALS_struct"] - agg["B_shuffle"]["FALS_struct"], 4)
    cm = round(agg["B_composed"]["FALS_sem"] - agg["B_shuffle"]["FALS_sem"], 4)
    print(f"\n  CROSS-SHUFFLE COLLAPSE (composed - shuffle):", flush=True)
    print(f"    structural collapse = {cs}", flush=True)
    print(f"    semantic   collapse = {cm}", flush=True)
    verdict = _verdict(cs, cm)
    print(f"  {verdict}", flush=True)
    return {"collapse_struct": cs, "collapse_sem": cm, "verdict": verdict, "arms": agg}


def _verdict(cs, cm):
    # FROZEN read rule (declared before scoring any ckpt):
    #   MEASUREMENT-BREAK iff semantic collapse exceeds structural by >=1 whole idea AND
    #     semantic collapse is positive (composed binds more than shuffle under semantics).
    #   else CAPACITY (neither detector sees idea-specific binding -> wall is real).
    if cm >= cs + 1 and cm > 0:
        return ("VERDICT: 🟢 MEASUREMENT-BREAK — semantic detector reveals a cross-shuffle "
                "COLLAPSE that structural misses => the WALL was a measurement artifact (model "
                "binds idea-specifically; H_1305 was blind). [DIRECTIONAL: torch-mouth/saved gen]")
    return ("VERDICT: 🧱 CAPACITY-REINFORCED — semantic collapse does NOT exceed structural "
            "(neither detector sees earned idea-specific binding) => the wall is NOT a "
            "measurement artifact; capacity ceiling stands.")


# ── input parsers ──
TAG = re.compile(r'^(\d+)\|([A-Za-z_]+)\|(\d+)\t(.*)$')


def parse_frag_files(paths):
    frags = {}
    for fn in paths:
        cur = None
        with open(fn, errors="replace") as f:
            for ln in f:
                m = TAG.match(ln)
                if m:
                    sr, a, i, txt = m.groups()
                    key = (int(sr), a, int(i))
                    if key not in frags:
                        frags[key] = txt; cur = key
                    else:
                        cur = None
                elif cur is not None:
                    frags[cur] += " " + ln.rstrip("\n")
    return frags


def parse_result_json(path):
    """Map a g6_common result.json's per_seed in_texts to (seed, B_composed, idx).
    The g6 'in' eval uses gauge IDEATION_SEEDS — we label it B_composed for the composed
    read; shuffle is NOT stored as text (only shuf_fals counts), so result.json gives us only
    the composed arm. Returns ({base..},{trained..}) frag dicts (composed only, TRUNCATED)."""
    raw = open(path).read()
    # tolerate a truncated/partial json (harvested mid-write): cut to last complete object
    d = None
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        # harvested mid-write: try closing the open braces (count unbalanced { vs }).
        for extra in range(1, 6):
            try:
                d = json.loads(raw + "}" * extra)
                break
            except json.JSONDecodeError:
                continue
        if d is None:
            # last resort: trim to last balanced top-level object
            depth = 0; endpos = 0
            for i, ch in enumerate(raw):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        endpos = i + 1
            d = json.loads(raw[:endpos]) if endpos else {}
    out = {}
    for sec in ("base", "trained"):
        if sec not in d:
            continue
        frags = {}
        for ps in d[sec].get("per_seed", []):
            sr = ps["seed"]
            for i, t in enumerate(ps.get("in_texts", [])):
                frags[(sr, "B_composed", i)] = t
        out[sec] = frags
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frags", nargs="*", default=None)
    ap.add_argument("--result-json", default=None)
    ap.add_argument("--label", default="CKPT")
    ap.add_argument("--decode", default=None, help="ckpt path to decode live (needs torch)")
    args = ap.parse_args()

    if args.result_json:
        out = parse_result_json(args.result_json)
        results = {}
        for sec, frags in out.items():
            results[sec] = report(f"{args.label}:{sec} (result.json TRUNCATED — LOWER BOUND)", aggregate(frags))
        print("\n[note] result.json in_texts are truncated to ~90 chars and store ONLY the "
              "composed arm (shuffle text not saved) -> this is a SMOKE illustration of the pipe, "
              "NOT a verdict. Use --frags from a full decode for the binding read.", flush=True)
        return
    if args.decode:
        decode_live(args.decode, args.label)
        return
    if args.frags:
        paths = []
        for pat in args.frags:
            paths += sorted(glob.glob(pat))
        frags = parse_frag_files(paths)
        print(f"[rescore] parsed {len(frags)} fragments from {len(paths)} files", flush=True)
        report(args.label, aggregate(frags))
        return
    ap.error("need --frags, --result-json, or --decode")


def decode_live(ckpt, label):
    """Decode the 4 arms x 3 seeds from a ckpt with gauge_lib._decode (torch), then dual-score.
    Lives here so a pod can run one self-contained file. DIRECTIONAL (torch-mouth)."""
    import torch
    H1305 = SD._H1305
    h5 = SD._load("h1305", H1305)
    composed, shuffled, ablated = h5.build_frames()
    arms = {"A_flat": list(g.IDEATION_SEEDS), "B_composed": composed,
            "B_shuffle": shuffled, "B_ablate": ablated}
    # model load via h1129 ByteGPT
    PROBES = os.environ.get("G6_PROBES",
                            os.environ.get("H1456_PROBES",
                                           os.path.join(ANIMA, "state", "1439_bind_head_architecture", "probes")))
    h = SD._load("h1129", os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py"))
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(ckpt, map_location=dev, weights_only=False)
    cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.to(dev); m.grad_ckpt = False
    frags = {}
    for sr in SEEDS:
        for a, frames in arms.items():
            for i, txt in enumerate(frames):
                t = g._decode(m, txt, h5.MAX_NEW, torch, block=cfg["block"], seed_rng=sr)
                frags[(sr, a, i)] = t
    report(label, aggregate(frags))


if __name__ == "__main__":
    main()
