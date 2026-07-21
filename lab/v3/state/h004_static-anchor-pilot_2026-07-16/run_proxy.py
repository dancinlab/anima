"""H_004 $0 numpy PROXY pre-check — a research-before-real-measurement gate.

NOT H_004 itself (that is the seeded torch/MPS pilot in run_h004.py). This trains
a tiny numpy neural LM on the oracle vs frozen codec and measures Δ_proxy on the
EXACT D3 eval (predict the polarity mark that follows a body). Its job: get a
DIRECTIONAL reading before spending on the real pilot.

Asymmetry (stated because it governs interpretation):
  - a clear oracle >> frozen Δ_proxy = positive evidence the mechanism exists at
    minimal scale (MORPH-ATOM was itself drill-scale), de-risking the real run.
  - a null Δ_proxy is NOT decisive — a fixed-window numpy LM is far weaker than
    the 4.9M transformer, so a null could be under-capacity, not absence.

Eval (Fable D3, verbatim): prompt = SENTINEL + body + SENTINEL, body =
render(stem, [neg_affix if label==neg else plain]); candidates = POS_MARK+SEN vs
NEG_MARK+SEN, each encoded by THAT arm's codec; pick the min-NLL candidate;
correct iff it matches label. Both candidates are equal byte length, so
total-log-prob IS bits-per-byte (salvage l6).

Run: python3 state/h004_static-anchor-pilot_2026-07-16/run_proxy.py
Deterministic given seeds. numpy only, $0.
"""

from __future__ import annotations

import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "src", "generator"))
sys.path.insert(0, _HERE)

import spec as S
import stream as ST
import codec as C
import materialize as M
from lang import to_jamo, render
from stream import POS_MARK, NEG_MARK, SENTINEL, plain_forms
from nlm import NeuralLM

# --- proxy scale (deliberately small — directional, not the pilot) ------------
LINES_PER_PHASE = 16000
DIM, HIDDEN, CONTEXT = 64, 128, 12
EPOCHS, BATCH, LR = 4, 256, 3e-3
SEEDS = [101, 202]
K = 512


def build_codecs(spec):
    s1 = ST.stream_sample(spec, 1, 10000)
    s2 = ST.stream_sample(spec, 2, 10000)
    oracle = C.fit_bpe_jamo(s1 + s2, K)          # sees both phases
    frozen = C.fit_bpe_jamo(ST.stream_sample(spec, 1, 20000), K)  # phase-1 only
    return oracle, frozen


def eval_items_marked(spec):
    """Rebuild the D3 eval items: (prompt_jamo, label) — body then predict mark."""
    plains2 = plain_forms(spec, 2)
    items = ST.eval_items(spec)
    out = []
    for it in items:
        if it["label"] == "neg":
            body = it["neg"]                      # stem + novel NEG allomorph
        else:
            body = it["pos"]                      # stem + plain affix
        out.append({"prompt_jamo": to_jamo(body), "label": it["label"],
                    "stem": it["stem"], "affix": it["affix"]})
    return out


def drilled_items_marked(spec, n=256):
    """F1 sanity: drilled stems x novel NEG allomorphs (composition seen in phase-2)."""
    import random
    rng = random.Random(spec["seed"] + 5)
    drilled = spec["drilled_stems"]
    novel = spec["novel_neg_forms"]
    plains2 = plain_forms(spec, 2)
    out = []
    for _ in range(n):
        stem = rng.choice(drilled)
        if rng.random() < 0.5:
            body = render(stem, [rng.choice(novel)]); label = "neg"
        else:
            body = render(stem, [rng.choice(plains2)]); label = "pos"
        out.append({"prompt_jamo": to_jamo(body), "label": label})
    return out


def score_f2(model, codec, ids, items):
    """Forced-choice mark prediction. Returns correct count."""
    pos_cand = M.encode_ids(codec, ids, to_jamo(POS_MARK) + SENTINEL)
    neg_cand = M.encode_ids(codec, ids, to_jamo(NEG_MARK) + SENTINEL)
    correct = 0
    for it in items:
        prompt = M.encode_ids(codec, ids, SENTINEL + it["prompt_jamo"] + SENTINEL)
        nll_pos = model.seq_nll_bits(prompt, pos_cand)
        nll_neg = model.seq_nll_bits(prompt, neg_cand)
        pick = "neg" if nll_neg < nll_pos else "pos"
        if pick == it["label"]:
            correct += 1
    return correct


def train_arm(spec, codec, ids, seed, log):
    stream_p1 = M.stream_ids(spec, 1, codec, ids, LINES_PER_PHASE)
    stream_p2 = M.stream_ids(spec, 2, codec, ids, LINES_PER_PHASE)
    ids_seq = stream_p1 + stream_p2
    model = NeuralLM(len(ids), dim=DIM, hidden=HIDDEN, context=CONTEXT, seed=seed)
    model.train(ids_seq, epochs=EPOCHS, batch=BATCH, lr=LR, seed=seed, log=log)
    return model, len(ids_seq)


def main() -> int:
    t0 = time.time()
    spec = S.build_spec()
    print("=" * 74)
    print("H_004 PROXY (numpy $0) — Δ_proxy = F2(oracle) − F2(frozen), mark-prediction")
    print("=" * 74)
    print(f"genspec {S.spec_hash(spec)[:12]} · scale {LINES_PER_PHASE}L/phase · "
          f"model d{DIM}/h{HIDDEN}/ctx{CONTEXT}")

    oracle, frozen = build_codecs(spec)
    vo, vf = M.vocab(oracle), M.vocab(frozen)
    print(f"vocab oracle {len(vo)} · frozen {len(vf)}")

    ev = eval_items_marked(spec)
    dr = drilled_items_marked(spec)
    n2, n1 = len(ev), len(dr)
    print(f"eval: {n2} held-out flip items · {n1} drilled sanity items\n")

    res = {"arms": {}, "genspec_sha256": S.spec_hash(spec)}
    for arm, codec, ids in (("oracle", oracle, vo), ("frozen", frozen, vf)):
        for seed in SEEDS:
            key = f"{arm}_{seed}"
            print(f"[{key}] training…")
            model, ntok = train_arm(spec, codec, ids, seed,
                                    log=lambda s: print(s))
            f2 = score_f2(model, codec, ids, ev)
            f1 = score_f2(model, codec, ids, dr)
            res["arms"][key] = {"F2_correct": f2, "F2_n": n2, "F2": f2 / n2,
                                "F1_correct": f1, "F1_n": n1, "F1": f1 / n1,
                                "train_tokens": ntok}
            print(f"  {key}: F2={f2}/{n2}={f2/n2:.4f}  F1={f1}/{n1}={f1/n1:.4f}\n")

    kO = res["arms"]["oracle_101"]["F2_correct"] + res["arms"]["oracle_202"]["F2_correct"]
    kF = res["arms"]["frozen_101"]["F2_correct"] + res["arms"]["frozen_202"]["F2_correct"]
    delta = (kO - kF) / (2 * n2)
    res["oracle_pooled_F2"] = kO / (2 * n2)
    res["frozen_pooled_F2"] = kF / (2 * n2)
    res["delta_proxy"] = delta
    res["elapsed_s"] = round(time.time() - t0, 1)

    print("=" * 74)
    print(f"oracle pooled F2 = {kO}/{2*n2} = {kO/(2*n2):.4f}")
    print(f"frozen pooled F2 = {kF}/{2*n2} = {kF/(2*n2):.4f}")
    print(f"Δ_proxy = {delta:+.4f}   (elapsed {res['elapsed_s']}s)")
    print("=" * 74)
    print("READING: a clear positive Δ_proxy = mechanism exists at minimal scale (de-risks")
    print("the real MPS pilot). A null is NOT decisive — this model is far weaker than the")
    print("4.9M transformer H_004 will train, so a null could be under-capacity.")

    out = os.path.join(_HERE, "proxy_result.json")
    with open(out, "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
