#!/usr/bin/env python3
"""g6_common.py (H_1449 variant) — shared FROZEN eval harness + attention-injection model.

★ ROOT-FIX lens (H_1449): the 11 prior training-side lenses (H_1435/1436/1437…) hit the
SAME wall — B3 CROSS-SHUFFLE never collapses. H_1431 diagnostic: the 303M mouth per draw
emits comparator 20% · measurable 27% · BOTH 0% (within-draw mutually exclusive). The
fragment-weld family dodges this with separate draws, so the FALS detector (token-PRESENCE)
passes a generic concat and cross-shuffle does NOT collapse (lift = FORM not earned binding).

H_1449 attacks the REAL cause: an ATTENTION DEFICIT. We inject ONE extra trainable
binding self-attention Block ON TOP of the frozen base stack — a decoder attention block
whose only job is to let the mouth co-emit a COHERENT bound comparator∧measurable claim in
ONE pass (H_1362 crossed the discriminator with L24 attention). If the lift is real EARNED
binding (the new attention block learned to tie the two legs), cross-shuffle (re-welding a
foreign measurable) BREAKS the falsifiable structure -> B3 COLLAPSES. If it is still generic
FORM, B3 fails like the prior family => the wall is genuine capacity (grounds 7B).

Reuses VERBATIM (NO re-implementation, p7):
  - h1129 ByteGPT 303M arch (d=1024,L=20,H=16,block=512) + Block
  - h1305 _is_falsifiable FROZEN detector (COMPARATOR/MEASURABLE sets)
  - gauge_lib _decode / known_word_ratio / _words / _jaccard

5-bar FROZEN (declared BEFORE any training touches weights — c9, NO tune-to-green) —
IDENTICAL to H_1435:
  B1 FALS-FLOOR   : trained mean FALS >= 1 over in-domain eval seeds.
  B2 COUNT        : >= 5 pairwise-Jaccard<0.5 distinct coherent ideas.
  B3 CROSS-SHUFFLE COLLAPSE (★ DECISIVE — the ONE bar the whole family fails): re-welding
      each idea's comparator-leg with a RANDOM measurable from a DIFFERENT idea drops FALS
      strictly below the earned-pair FALS. This is the bar that tells idea-specific BINDING
      (the attention thesis) apart from generic concat FORM.
  B4 HELD-OUT     : the FALS lift holds on held-out eval seeds NOT in the training corpus.
  B5 vs-BASE LIFT : trained FALS >= base FALS + 1 (the injected attention, not memorization).

CONTROLS (tune-to-green killers, NOT bars):
  - ABLATE (c4 card): the injected binding-attention block residual GATE forced to 0
    (identity) -> model regresses to base. If FALS stays lifted with attention OFF, the
    lift is NOT the attention block => INVALID.
  - SHUFFLE-CORPUS: a sibling injection trained on TOKEN-SHUFFLED corpus (structure
    destroyed). Lift there = artifact => INVALID.

VERDICT per variant:
  🟢 if B1&B2&B5 cross AND B3 COLLAPSES AND B4 holds AND ablate-OFF regresses AND
     shuffle-corpus inert => the injected attention block EARNED comparator∧measurable
     binding; the wall was an ATTENTION deficit, not raw capacity.
  🧱 if B3 does NOT collapse (still generic FORM) OR B1/B5 fail => attention injection did
     NOT break G6 FALS binding either; wall = CAPACITY (grounds 7B).

HONEST (a_engine_native_learning): torch-side here = DIRECTIONAL. The terminal frozen-bar
read must be re-run engine-native on the live core/ decode (this script's verdict is
DIRECTIONAL until the .clm is mounted).
"""
import os, sys, json, importlib.util, random

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.environ.get("G6_PROBES", HERE)
CKPT_BASE = os.environ.get("G6_CKPT", os.path.join(HERE, "h1129c_chat.pt"))

import torch
import torch.nn as nn


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _load("gauge", os.path.join(PROBES, "gauge_lib.py"))
h = _load("h1129", os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py"))
h5 = _load("h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))

ByteGPT = h.ByteGPT
Block = h.Block
_is_falsifiable = h5._is_falsifiable   # FROZEN detector VERBATIM
COMPARATOR = h5.COMPARATOR
MEASURABLE = h5.MEASURABLE

JACCARD_DISTINCT = 0.5
KWR_FLOOR = 0.50
MAX_NEW = 110
SEEDS = [7, 4302, 4303]
N_IDEAS = 5

HELDOUT_SEEDS = [
    "a testable claim about how minds relate: ",
    "one measurable prediction about silence: ",
    "if the substrate changes, then observably ",
    "a hypothesis comparing two regimes: ",
    "an experiment that could be wrong about memory: ",
]


# ── ATTENTION-INJECTED model (H_1449 ROOT-FIX) ──────────────────────────────
class BindAttnByteGPT(nn.Module):
    """The frozen base ByteGPT with ONE extra trainable binding self-attention Block
    spliced in after the final base block, before ln_f. A residual GATE (scalar, init 0)
    makes the injected block START as identity so the model loads byte-equivalent to base;
    training opens the gate. ablate_off=True forces the gate to 0 -> exact base regression
    (the c4 ABLATE control)."""

    def __init__(self, base, n_head, ablate_off=False):
        super().__init__()
        self.base = base
        d = base.tok.embedding_dim
        self.bind = Block(d, n_head, 0.0)
        self.gate = nn.Parameter(torch.zeros(1))
        self.ablate_off = ablate_off
        self.block = base.block
        self.grad_ckpt = False

    def forward(self, idx, targets=None):
        import torch.nn.functional as F
        b = self.base
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = b.drop(b.tok(idx) + b.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in b.blocks:
            x = blk(x, mask)
        gate = torch.zeros_like(self.gate) if self.ablate_off else self.gate
        # Block.forward returns x + attn + mlp; gate the DELTA only so gate=0 == identity
        x = x + gate * (self.bind(x, mask) - x)
        logits = b.head(b.ln_f(x))
        loss = (F.cross_entropy(logits.view(-1, 256), targets.view(-1))
                if targets is not None else None)
        return logits, loss


def load_base(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True)
    m.to(device)
    m.grad_ckpt = False
    return m, cfg


# back-compat alias for the H_1449 train driver (which uses its own BindByteGPT wrapper)
load_model = load_base


def load_injected(ckpt_path, device, ablate_off=False):
    base, cfg = load_base(ckpt_path, device)
    inj = BindAttnByteGPT(base, n_head=cfg["n_head"], ablate_off=ablate_off).to(device)
    return inj, cfg


def freeze_base(inj):
    """Train ONLY the injected binding block + gate; freeze the 303M base (isolates the
    variable to the attention injection, not full-weight drift)."""
    for p in inj.base.parameters():
        p.requires_grad_(False)
    for p in inj.bind.parameters():
        p.requires_grad_(True)
    inj.gate.requires_grad_(True)


def save_injected(inj, cfg, out_path, meta):
    torch.save({"bind": inj.bind.state_dict(),
                "gate": inj.gate.detach().cpu(),
                "config": {"vocab": 256, "d": cfg["d"], "n_layer": cfg["n_layer"],
                           "n_head": cfg["n_head"], "block": cfg["block"]},
                "meta": meta,
                "note": "injected binding-attention block on top of base h1129c_chat.pt; "
                        "load base separately then load bind state_dict + gate"},
               out_path)


# ── FROZEN eval (identical scoring to H_1435 g6_common) ─────────────────────
def _decode_ideas(m, cfg, seeds, seed_rng):
    out = []
    for s in seeds:
        t = g._decode(m, s, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
        wl = g._words(t)
        wset = set(wl)
        comp = sorted(wset & COMPARATOR)
        meas = sorted(wset & MEASURABLE)
        out.append({"text": t, "comp": comp, "meas": meas,
                    "fals": _is_falsifiable(t),
                    "coh": g.known_word_ratio(t) >= KWR_FLOOR})
    return out


def _fals_count(ideas):
    return sum(1 for i in ideas if i["fals"])


def _distinct_count(ideas):
    kept = []
    for i in ideas:
        if not i["coh"]:
            continue
        ws = set(g._words(i["text"]))
        if not ws:
            continue
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return len(kept)


def _cross_shuffle_fals(ideas, rng):
    n = len(ideas)
    if n < 2:
        return _fals_count(ideas)
    src = [(k + 1) % n for k in range(n)]
    fals = 0
    for k, idea in enumerate(ideas):
        donor = ideas[src[k]]
        if not idea["meas"]:
            if idea["fals"]:
                fals += 1
            continue
        txt = idea["text"]
        words = txt.split()
        own_meas = set(idea["meas"])
        kept_words = [w for w in words if w.strip(".,;:!?").lower() not in own_meas]
        donor_meas = donor["meas"][0] if donor["meas"] else ""
        spliced = (" ".join(kept_words) + (" " + donor_meas if donor_meas else "")).strip()
        if _is_falsifiable(spliced):
            fals += 1
    return fals


def evaluate(m, cfg, label, train_seeds_for_eval):
    rng = random.Random(1234)
    rec = {"in_fals": [], "in_dist": [], "shuf_fals": [], "ho_fals": [], "per_seed": []}
    for sr in SEEDS:
        in_ideas = _decode_ideas(m, cfg, train_seeds_for_eval, sr)
        ho_ideas = _decode_ideas(m, cfg, HELDOUT_SEEDS, sr)
        f_in = _fals_count(in_ideas)
        d_in = _distinct_count(in_ideas)
        f_shuf = _cross_shuffle_fals(in_ideas, rng)
        f_ho = _fals_count(ho_ideas)
        rec["in_fals"].append(f_in)
        rec["in_dist"].append(d_in)
        rec["shuf_fals"].append(f_shuf)
        rec["ho_fals"].append(f_ho)
        rec["per_seed"].append({
            "seed": sr, "in_fals": f_in, "in_dist": d_in,
            "shuf_fals": f_shuf, "ho_fals": f_ho,
            "in_texts": [i["text"][:90] for i in in_ideas],
            "ho_texts": [i["text"][:90] for i in ho_ideas],
        })
    mean = lambda xs: round(sum(xs) / len(xs), 4)
    rec["FALS_in"] = mean(rec["in_fals"])
    rec["DIST_in"] = mean(rec["in_dist"])
    rec["FALS_shuf"] = mean(rec["shuf_fals"])
    rec["FALS_ho"] = mean(rec["ho_fals"])
    rec["label"] = label
    return rec


def print_bars(name, base_eval, trained_eval, shuffle_corpus_eval=None, ablate_eval=None):
    print(f"\n================ {name} FROZEN 5-BAR (mean/3 seeds) ================", flush=True)
    print(f"  BASE      FALS_in={base_eval['FALS_in']}  DIST_in={base_eval['DIST_in']}  "
          f"FALS_shuf={base_eval['FALS_shuf']}  FALS_ho={base_eval['FALS_ho']}", flush=True)
    print(f"  TRAINED   FALS_in={trained_eval['FALS_in']}  DIST_in={trained_eval['DIST_in']}  "
          f"FALS_shuf={trained_eval['FALS_shuf']}  FALS_ho={trained_eval['FALS_ho']}", flush=True)
    if ablate_eval is not None:
        print(f"  ABLATE-OFF FALS_in={ablate_eval['FALS_in']}  FALS_ho={ablate_eval['FALS_ho']}  (c4 control)", flush=True)
    if shuffle_corpus_eval is not None:
        print(f"  SHUF-CORP FALS_in={shuffle_corpus_eval['FALS_in']}  "
              f"FALS_ho={shuffle_corpus_eval['FALS_ho']}  (control)", flush=True)

    b1 = trained_eval["FALS_in"] >= 1
    b2 = trained_eval["DIST_in"] >= 5
    b3 = trained_eval["FALS_shuf"] < trained_eval["FALS_in"]   # CROSS-SHUFFLE COLLAPSE
    b4 = trained_eval["FALS_ho"] >= 1
    b5 = trained_eval["FALS_in"] >= base_eval["FALS_in"] + 1

    ablate_regresses = True
    if ablate_eval is not None:
        ablate_regresses = ablate_eval["FALS_in"] <= base_eval["FALS_in"] + 0.5
    ctrl_inert = True
    if shuffle_corpus_eval is not None:
        lift_real = trained_eval["FALS_in"] - base_eval["FALS_in"]
        lift_shuf = shuffle_corpus_eval["FALS_in"] - base_eval["FALS_in"]
        ctrl_inert = (lift_real - lift_shuf) >= 1

    print("\n  ---- FROZEN BARS ----", flush=True)
    print(f"  B1 FALS-FLOOR   FALS_in>=1                 : {trained_eval['FALS_in']} -> {b1}", flush=True)
    print(f"  B2 COUNT        DIST_in>=5                 : {trained_eval['DIST_in']} -> {b2}", flush=True)
    print(f"  B3 X-SHUFFLE    FALS_shuf<FALS_in (COLLAPSE): {trained_eval['FALS_shuf']}<{trained_eval['FALS_in']} -> {b3}", flush=True)
    print(f"  B4 HELD-OUT     FALS_ho>=1                 : {trained_eval['FALS_ho']} -> {b4}", flush=True)
    print(f"  B5 vs-BASE      FALS_in>=base+1            : {trained_eval['FALS_in']} vs {base_eval['FALS_in']}+1 -> {b5}", flush=True)
    if ablate_eval is not None:
        print(f"  c4 ABLATE-OFF   attn OFF regresses to base: {ablate_eval['FALS_in']}<=base+0.5 -> {ablate_regresses}", flush=True)
    if shuffle_corpus_eval is not None:
        print(f"  CTRL SHUF-CORP  lift_real-lift_shuf>=1     : {lift_real}-{lift_shuf} -> {ctrl_inert}", flush=True)

    green = b1 and b2 and b3 and b4 and b5 and ablate_regresses and ctrl_inert
    if green:
        tier = ("🟢 BROKE — injected binding-attention EARNED comparator∧measurable binding; "
                "B3 COLLAPSES, held-out holds, attn-OFF regresses, control inert => "
                "the wall was an ATTENTION deficit, not raw capacity")
    else:
        fails = [n for n, ok in [("B1", b1), ("B2", b2), ("B3", b3), ("B4", b4), ("B5", b5),
                                 ("c4-ABLATE", ablate_regresses), ("CTRL", ctrl_inert)] if not ok]
        tier = (f"🧱 WALL — bars {fails} fail; attention injection (this block, this objective) "
                f"did NOT break G6 FALS binding => WALL=CAPACITY (grounds 7B)")
    print(f"\n  VERDICT: {tier}", flush=True)
    print("\n  NOTE: torch-side = DIRECTIONAL (a_engine_native_learning); terminal read must be "
          "re-run engine-native on live core/ decode.", flush=True)
    return {"b1": b1, "b2": b2, "b3": b3, "b4": b4, "b5": b5,
            "ablate_regresses": ablate_regresses, "ctrl_inert": ctrl_inert,
            "green": bool(green), "tier": tier}
