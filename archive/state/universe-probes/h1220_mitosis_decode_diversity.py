"""
H_1220 — MITOSIS-DECODE-DIVERSITY (HD9 of the depth-ceiling ladder, .verdicts/
1219_depth_ceiling_hypothesis_exhaustion/H_1219.txt).

THE QUESTION (a NEW mechanism, re-opening a prior closed-negative per a_paper_negative_ok)
==========================================================================================
The newly-wired LIVE mitosis (CORE/engine_cli.hexa VAdaptField cell-division — DIM-vector,
split on recon-error >= SPLIT_THRESH 0.30, LR 0.20; daemon GROW/sleep-persist/separation-guard
H_1202-1205) is generation-DISJOINT as currently wired (H_1205 separation-guard: emit byte-
identical ON/OFF mitosis, Ψ unchanged). PRIOR closed-negatives:
  * H_1201 🔴 mitosis -> generation via frozen single-window FEATURE-CONDITIONING (no info).
  * H_1211 🔴 scale-recheck (density half scale-robust, trajectory half toy artifact).
So the HONEST PRIOR is RED.

HD3 (the thing to recover): under GREEDY argmax the 303M byte-LM COLLAPSES on ideation/
composition (H_1218: G1 composed_distinct=0, loops); under top-k40 temp0.7 SAMPLING it PASSES
(H_1158: 11-14 distinct corpus-absent ideas). So ideation IS in the weights — greedy can't
surface it. The DECODE finding is the lever to recover.

NEW MECHANISM (distinct from H_1201's frozen-feature conditioning): use the mitosis novelty-
SPLIT TIMING as a DECODE-TIME DIVERSITY source. Run the numpy mirror of VAdaptField over the
decode-context byte stream; at each step it emits a binary "novelty-split event" (a cell splits
= recon-err crosses SPLIT_THRESH). At split steps, PERTURB the greedy pick; at non-split steps,
pure greedy. NO global temperature — the ONLY diversity source is mitosis split timing.

PERTURBATION RULE (documented, fixed before running): at a novelty-split step, replace the
greedy argmax with a SEEDED top-k sample over the post-softmax mass (top_k=40, temp=1.0,
multinomial with a per-probe RNG). At non-split steps: pure greedy argmax. This is the minimal
"inject diversity at the split" rule; it uses NO global temperature schedule — diversity is
GATED entirely by the mitosis split-event mask.

THREE ARMS (identical except the diversity gate)
================================================
  (A) PURE-GREEDY    : argmax every step (expect collapse, H_1218).
  (B) MITOSIS-GATED  : perturb ONLY at mitosis novelty-split steps (the hypothesis).
  (C) SHUFFLED-SPLIT : same NUMBER of perturbation events as (B), but at RANDOM timesteps
                       (control — isolates split TIMING from mere perturbation count).

SCORE — FROZEN evaluators VERBATIM from UNIVERSE/gauge_lib.py:
  G1 composed_distinct = len(_coverage(text))  [primary gate]
  G6 count             = distinct coherent ideas (Jaccard distance, IDEATION_SEEDS)
  G2 novelty           = corpus-absence fraction (corroborating)
  G0 kwr               = known_word_ratio coherence filter (gates G2/G6 inclusion, VERBATIM)

PRE-REGISTERED BARS (frozen BEFORE running; do not move, p7)
============================================================
  GREEN iff:
    (B) composed_distinct >= the sampling baseline (H_1158 >=5/seed) on >=3 seeds
    AND (C) SHUFFLED <= (A) baseline + small eps  (so the lift comes from mitosis novelty-
        TIMING, not mere perturbation count).
  Else 🔴 RED (decisive): mitosis-decode-diversity does NOT recover ideation -> mitosis stays
  generation-disjoint even via this new decode mechanism, reinforcing H_1201/1205/1211.

SCOPE / HONESTY (a_scale_honest_scope, p7, p8): $0 local CPU. numpy mirror of the live .hexa
VAdaptField (does NOT touch CORE/engine_cli.hexa or CORE/bytegpt_decode.hexa — mirror only,
another agent owns engine-code edits this session). Torch reference forward of the 303M ByteGPT
(byte-exact to the engine per H_1157). 3 seeds. NO LLM-judge (p7). Decisive-grade, honest RED.
"""
import os
import sys
import json
import argparse

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# gauge_lib relocated 2026-06-16 UNIVERSE/ -> tool/ (sibling of state/universe-probes/).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tool"))

# FROZEN evaluators + byte-feature + VAdaptField mirror — VERBATIM import (no re-impl).
import gauge_lib as G   # _coverage, _content_ngrams, _corpus_absent, known_word_ratio,
                        # _jaccard, IDEATION_SEEDS, CONCEPTS, _mitosis_byte_feature,
                        # _MITOSIS_SPLIT_THRESH, _MITOSIS_LR, _MITOSIS_MAX_CELLS, _MITOSIS_DIM

# the 303M ckpt is a gitignored local-only artifact; allow an env override.
CKPT = os.environ.get("H1220_CKPT",
                      os.path.join(HERE, "..", "state", "chat_303m", "h1129c_chat.pt"))
CORPUS = os.path.join(HERE, "..", "CORE", "testdata", "clm_mid_5lang_c4.txt")

# decode config (NO global temperature — see perturbation rule)
MAX_NEW = 96
BLOCK = 512
PERTURB_TOP_K = 40       # top-k width AT a split step (perturbation only)
KWR_FLOOR = 0.50         # G0 coherence floor (VERBATIM gauge default)
JACCARD_DISTINCT = 0.25  # G6 distinctness threshold (VERBATIM gauge default)
MITOSIS_WINDOW = 16      # byte window for the DIM=8 feature (VERBATIM gauge default)

# >=3 deterministic decode-diversity RNG seeds (the B/C perturbation RNG seeds)
SEEDS = [7, 8, 9]

# pre-registered bars (FROZEN — do NOT move, p7)
BAR_B_COMPOSED = 5       # H_1158 sampling baseline >=5 distinct / seed
BAR_C_EPS = 0.5          # SHUFFLED <= A baseline + eps  (mean over seeds)


# ──────────────────────────────────────────────────────────────────────────────
# ByteGPT (VERBATIM arch from UNIVERSE/h1129_midcap_broad_converged_recombination.py)
# ──────────────────────────────────────────────────────────────────────────────
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p))

    def forward(s, x, m):
        h = s.ln1(x)
        a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False)
        x = x + a
        return x + s.mlp(s.ln2(x))


class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d)
        s.pos = nn.Embedding(block, d)
        s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d)
        s.head = nn.Linear(d, vocab, bias=False)
        s.head.weight = s.tok.weight

    def forward(s, idx):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        return s.head(s.ln_f(x))


def load_model():
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(vocab=cfg["vocab"], d=cfg["d"], n_layer=cfg["n_layer"],
                n_head=cfg["n_head"], block=cfg["block"], p=0.0)
    m.load_state_dict(ck["model"], strict=True)
    m.eval()
    return m, cfg


# ──────────────────────────────────────────────────────────────────────────────
# mitosis novelty-split EVENT mirror — numpy mirror of CORE/engine_cli.hexa
# VAdaptField vadapt_field_step (H_1199), but returning the per-step SPLIT-EVENT
# mask (binary novelty-split timing) rather than just the final cell count.
# Mechanism is IDENTICAL to gauge_lib._vadapt_field_cells (same proto-split, LR,
# SPLIT_THRESH); only the return value differs (per-step event, not the count).
# ──────────────────────────────────────────────────────────────────────────────
def mitosis_split_events(byte_seq, window=MITOSIS_WINDOW):
    """Run the VAdaptField mirror over the byte stream; emit a binary split-event
    per windowed tick (1 = a cell split fired = novelty crossed SPLIT_THRESH).
    Returns a list aligned to feature-tick index. NUMPY MIRROR (p8) of the live
    .hexa engine — does NOT touch CORE/engine_cli.hexa."""
    b = list(byte_seq)
    if len(b) < window:
        return []
    rows = [G._mitosis_byte_feature(b[i:i + window])
            for i in range(0, len(b) - window + 1)]
    events = []
    protos = [list(rows[0])]
    for x in rows:
        best_j, best_d2 = 0, None
        for j, p in enumerate(protos):
            d2 = sum((p[k] - x[k]) ** 2 for k in range(len(x)))
            if best_d2 is None or d2 < best_d2:
                best_j, best_d2 = j, d2
        err = best_d2 ** 0.5
        if err > G._MITOSIS_SPLIT_THRESH and len(protos) < G._MITOSIS_MAX_CELLS:
            protos.append(list(x))           # SPLIT — novelty event
            events.append(1)
        else:
            p = protos[best_j]               # online winner pull
            for k in range(len(x)):
                p[k] += G._MITOSIS_LR * (x[k] - p[k])
            events.append(0)
    return events


def split_event_at_step(byte_prefix):
    """Is the NEXT decode step a mitosis novelty-split step? Defined as: does the
    VAdaptField mirror fire a split on the MOST-RECENT windowed tick of the current
    decode-context byte prefix? (the split timing = mitosis sees a novel local
    byte-window). Returns True iff the last tick's event == 1."""
    ev = mitosis_split_events(byte_prefix)
    if not ev:
        return False
    return ev[-1] == 1


# ──────────────────────────────────────────────────────────────────────────────
# DECODE — 3 arms, identical except the diversity gate. NO global temperature.
# ──────────────────────────────────────────────────────────────────────────────
STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]


def _truncate(text):
    for st in STOPS:
        i = text.find(st)
        if i >= 0:
            text = text[:i]
    return text.strip()


@torch.no_grad()
def decode_arm(model, seed_text, arm, rng_seed, n_split_budget=None):
    """Decode MAX_NEW bytes.
      arm == 'greedy'  : pure argmax every step.
      arm == 'mitosis' : perturb (top-k sample) at mitosis novelty-split steps; greedy else.
      arm == 'shuffled': perturb at RANDOM steps matching the mitosis split COUNT; greedy else.
    Returns (text, n_perturbations). The diversity RNG is per-(arm,seed) seeded.
    """
    g = torch.Generator(device="cpu")
    g.manual_seed(rng_seed)
    idx = torch.tensor([list(seed_text.encode("utf-8"))], dtype=torch.long)
    seed_bytes = list(seed_text.encode("utf-8"))
    out_bytes = []
    n_pert = 0

    # For the SHUFFLED arm: pre-draw which of the MAX_NEW steps get a perturbation,
    # matching the COUNT n_split_budget but at RANDOM positions (not mitosis-driven).
    shuffled_steps = set()
    if arm == "shuffled" and n_split_budget and n_split_budget > 0:
        srng = np.random.default_rng(rng_seed + 100000)
        k = min(n_split_budget, MAX_NEW)
        shuffled_steps = set(int(s) for s in srng.choice(MAX_NEW, size=k, replace=False))

    for step in range(MAX_NEW):
        ctx = idx[:, -BLOCK:]
        logits = model(ctx)[0, -1, :].float()    # (V,)

        # decide whether THIS step is a perturbation step
        if arm == "greedy":
            perturb = False
        elif arm == "mitosis":
            cur_bytes = seed_bytes + out_bytes
            perturb = split_event_at_step(cur_bytes)
        else:  # shuffled
            perturb = step in shuffled_steps

        if perturb:
            n_pert += 1
            lg = logits.clone()
            v, _ = torch.topk(lg, min(PERTURB_TOP_K, lg.shape[-1]))
            lg = lg.masked_fill(lg < v[-1], float("-inf"))
            probs = F.softmax(lg, dim=-1)         # temp=1.0 (NO global temp schedule)
            nb = int(torch.multinomial(probs, 1, generator=g).item())
        else:
            nb = int(torch.argmax(logits).item())

        out_bytes.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], dtype=torch.long)], dim=1)
        txt = bytes(out_bytes).decode("utf-8", "ignore")
        if any(st in txt for st in STOPS):
            break

    text = _truncate(bytes(out_bytes).decode("utf-8", "ignore"))
    return text, n_pert


def count_mitosis_splits_for_seed(model, seed_text, rng_seed):
    """Run the MITOSIS arm once to get the actual split-event count over its own
    generation — this count is the budget handed to the SHUFFLED control so the two
    arms have the SAME number of perturbation events (isolating TIMING)."""
    _, n_pert = decode_arm(model, seed_text, "mitosis", rng_seed)
    return n_pert


# ──────────────────────────────────────────────────────────────────────────────
# SCORING — FROZEN gauge_lib evaluators VERBATIM
# ──────────────────────────────────────────────────────────────────────────────
def composed_seed():
    return ". ".join(c for c, _ in G.CONCEPTS) + ". "


def score_g1(text):
    """G1 composed_distinct = len(_coverage(text)) — VERBATIM gauge_lib."""
    return len(G._coverage(text))


def score_g6(idea_texts):
    """G6 count = distinct coherent ideas (kwr-gated, Jaccard-distinct) — VERBATIM
    gauge_lib logic."""
    idea_word_sets = []
    for o in idea_texts:
        if G.known_word_ratio(o) >= KWR_FLOOR:
            ws = set(G._words(o))
            if ws:
                idea_word_sets.append(ws)
    kept = []
    for ws in idea_word_sets:
        if all(G._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return len(kept)


def score_g2(texts, corpus_paths):
    """G2 novelty = corpus-absence fraction over kwr-gated content n-grams — VERBATIM."""
    all_grams = set()
    for t in texts:
        if G.known_word_ratio(t) >= KWR_FLOOR:
            all_grams |= G._content_ngrams(t)
    if not all_grams:
        return 0.0, 0, 0
    if not corpus_paths:
        return None, 0, len(all_grams)
    n_novel = sum(1 for gram in all_grams if G._corpus_absent(gram, corpus_paths))
    return round(n_novel / len(all_grams), 5), n_novel, len(all_grams)


# ──────────────────────────────────────────────────────────────────────────────
# main — 3-arm sweep over >=3 seeds
# ──────────────────────────────────────────────────────────────────────────────
def run_seed(model, rng_seed, corpus_paths):
    comp_seed = composed_seed()

    # the mitosis split-count budget for THIS seed = the mitosis arm's own composed-seed
    # generation split count (so SHUFFLED matches the event COUNT, not timing).
    split_budget = count_mitosis_splits_for_seed(model, comp_seed, rng_seed)

    res = {"seed": rng_seed, "split_budget_composed": split_budget}
    arms = {"A_greedy": "greedy", "B_mitosis": "mitosis", "C_shuffled": "shuffled"}

    for label, arm in arms.items():
        # G1 composed
        comp_text, comp_pert = decode_arm(model, comp_seed, arm, rng_seed,
                                          n_split_budget=split_budget)
        g1 = score_g1(comp_text)

        # G6 ideation over IDEATION_SEEDS
        idea_texts = []
        idea_perts = 0
        for s in G.IDEATION_SEEDS:
            # for shuffled, recompute a per-seed split budget from the mitosis arm on
            # THIS ideation seed so the count matches that seed's mitosis run.
            sb = split_budget
            if arm == "shuffled":
                sb = count_mitosis_splits_for_seed(model, s, rng_seed)
            it, ip = decode_arm(model, s, arm, rng_seed, n_split_budget=sb)
            idea_texts.append(it)
            idea_perts += ip
        g6 = score_g6(idea_texts)

        # G2 corpus-absence over composed + ideation texts
        g2, n_novel, n_grams = score_g2([comp_text] + idea_texts, corpus_paths)

        res[label] = {
            "g1_composed_distinct": g1,
            "g6_count": g6,
            "g2_novelty": g2,
            "g2_novel_grams": n_novel,
            "g2_total_grams": n_grams,
            "comp_perturbations": comp_pert,
            "idea_perturbations": idea_perts,
            "comp_text_head": comp_text[:160],
        }
    return res


def adjudicate(per_seed):
    """Apply the FROZEN bars. GREEN iff B composed >= BAR_B_COMPOSED on >=3 seeds AND
    C mean <= A mean + BAR_C_EPS."""
    bs = [r["B_mitosis"]["g1_composed_distinct"] for r in per_seed]
    as_ = [r["A_greedy"]["g1_composed_distinct"] for r in per_seed]
    cs = [r["C_shuffled"]["g1_composed_distinct"] for r in per_seed]

    b_pass = sum(1 for v in bs if v >= BAR_B_COMPOSED)
    cond_B = b_pass >= 3 and len(per_seed) >= 3
    mean_a, mean_c = float(np.mean(as_)), float(np.mean(cs))
    cond_C = mean_c <= mean_a + BAR_C_EPS

    green = bool(cond_B and cond_C)
    return {
        "A_composed_per_seed": as_, "B_composed_per_seed": bs, "C_composed_per_seed": cs,
        "A_mean": mean_a, "B_mean": float(np.mean(bs)), "C_mean": mean_c,
        "cond_B (B>=%d on >=3 seeds)" % BAR_B_COMPOSED: {"n_pass": b_pass, "pass": cond_B},
        "cond_C (C_mean <= A_mean + eps=%.1f)" % BAR_C_EPS: {
            "C_mean": mean_c, "A_mean+eps": mean_a + BAR_C_EPS, "pass": cond_C},
        "GREEN": green,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="1 seed, quick path-check")
    a = ap.parse_args()

    seeds = SEEDS[:1] if a.smoke else SEEDS
    corpus_paths = [CORPUS] if os.path.exists(CORPUS) else []

    print("=== H_1220 — MITOSIS-DECODE-DIVERSITY (HD9 ladder) ===", flush=True)
    print(f"  ckpt={CKPT}", flush=True)
    print(f"  perturbation rule: at a mitosis novelty-SPLIT step, top-k={PERTURB_TOP_K} "
          f"temp=1.0 multinomial sample; else pure greedy argmax. NO global temperature.", flush=True)
    print(f"  3 arms: A=PURE-GREEDY  B=MITOSIS-GATED  C=SHUFFLED-SPLIT(count-matched)", flush=True)
    print(f"  FROZEN bars: GREEN iff B composed>={BAR_B_COMPOSED} on >=3 seeds AND "
          f"C_mean <= A_mean + {BAR_C_EPS}", flush=True)
    print(f"  seeds={seeds}  corpus={'present' if corpus_paths else 'ABSENT (G2=None)'}\n", flush=True)

    model, cfg = load_model()
    print(f"  model loaded: {cfg}\n", flush=True)

    per_seed = []
    for s in seeds:
        r = run_seed(model, s, corpus_paths)
        per_seed.append(r)
        print(f"  --- seed {s} (mitosis split budget={r['split_budget_composed']}) ---", flush=True)
        for label in ("A_greedy", "B_mitosis", "C_shuffled"):
            d = r[label]
            print(f"    {label:11s} G1_composed={d['g1_composed_distinct']}  G6_count={d['g6_count']}  "
                  f"G2_novelty={d['g2_novelty']}  pert(comp/idea)={d['comp_perturbations']}/{d['idea_perturbations']}",
                  flush=True)
        print(f"      B comp head: {r['B_mitosis']['comp_text_head']!r}", flush=True)

    verdict = adjudicate(per_seed) if not a.smoke else {"note": "smoke — no adjudication"}
    out = {
        "H": "H_1220",
        "title": "MITOSIS-DECODE-DIVERSITY (HD9) — does mitosis novelty-split TIMING recover "
                 "the greedy-collapsed ideation WITHOUT temperature sampling?",
        "perturbation_rule": f"at a mitosis novelty-split step: top-k={PERTURB_TOP_K} temp=1.0 "
                             f"multinomial; else greedy argmax. NO global temperature.",
        "frozen_bars": {
            "GREEN": f"B composed_distinct >= {BAR_B_COMPOSED} on >=3 seeds AND "
                     f"C_mean <= A_mean + {BAR_C_EPS}",
            "else": "RED (mitosis decode-diversity does not recover ideation -> generation-disjoint)",
        },
        "honest_prior": "RED — H_1205 separation-guard (emit byte-identical ON/OFF mitosis) + "
                        "H_1201 frozen-feature-conditioning RED + H_1211 scale-recheck. Distinct "
                        "mechanism (decode-time split TIMING vs frozen-feature input), fair test.",
        "seeds": seeds,
        "per_seed": per_seed,
        "verdict": verdict,
        "scope": "TOY/$0 local CPU, numpy mirror of CORE/engine_cli.hexa VAdaptField (p8, live "
                 ".hexa untouched), torch ref forward of 303M ByteGPT (byte-exact per H_1157). "
                 "3 seeds, scale UNVERIFIED (a_scale_honest_scope). p7 (NO LLM-judge).",
    }
    print("\n=== VERDICT JSON ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(out, open("/tmp/h1220_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
