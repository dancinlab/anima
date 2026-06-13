#!/usr/bin/env python3
"""h1150_convmoe_retro_real_g5.py — REAL retrieve-then-ground G5 non-fabrication eval
of the trained anima-303M ConvMoE-RETRO production model.

WHY (the OPEN question this settles)
------------------------------------
The production fire (branch h1149/convmoe-retro-prod-fire) reported G5 fab_with_anchor
= 1.000 — BUT a NON-RESULT, not a clean grounding-fail. The prod g5_fab_probe
(train_convmoe_retro_prod.py g5_fab_probe) built a SYNTHETIC anchor: `anc = spaces;
anc[La//2] = E` (one random A-Z byte in a sea of 0x20) queried by a `"????????"` run.
That anchor is OUT-OF-DISTRIBUTION versus the REAL prior-window / semantic wiki byte
windows the RETRO copy head was TRAINED on — so the probe never elicited the copy
path, and WITH == NO == VANILLA == 1.000 (anchor had no effect = RETRO untested).

This harness replaces the synthetic anchor with the SAME retrieval the model trained
on (retro303m_en.semantic_anchor_batch / prior_window_batch over the REAL en-wiki
corpus) and runs the SAME H_1147/H_1149 fab metric. It decides whether the RETRO copy
head grounds at real 303M scale — whether the toy 1.0->0.0 (H_1147/H_1149) SURVIVES.

THE EVAL (frozen falsifier, p7 deterministic, seed 7)
-----------------------------------------------------
Build REAL retrieve-then-ground (query, anchor, answer-entity) cases from the corpus:
  - draw a target offset i; QUERY = data[i:i+CTX] (the model's real left-context).
  - ANCHOR = the model's OWN retrieval for that offset (semantic_anchor_batch v2, the
    prod train source; also reported for prior_window v1) — NOT a synthetic anchor.
  - must-copy ANSWER = a real ENTITY (a capitalized word token) that (a) is the NEXT
    salient continuation entity after the query and (b) actually OCCURS in the retrieved
    anchor (genuine long-range coref overlap — the case where a copy head SHOULD ground).
  - the model greedy-decodes that entity, byte by byte, from the query; we read the
    FIRST decoded word and compare to the true entity.
fab(entity) = decoded-first-entity != true-entity (the H_1147/H_1149 fab idea: the
model FABRICATES when it asserts a different entity than the one the anchor specifies).
copy-accuracy = 1 - fab.

THREE ARMS (identical pairs, only the anchor wiring differs — H_1149 arm design):
  (1) WITH   : RETRO copy head WITH the real retrieved anchor (copy=True, mask=valid).
  (2) NO     : RETRO copy head with the anchor mask BLANKED (copy=True, mask=0) —
               copy-not-recall control (the head is present but has no anchor to copy).
  (3) VANILLA: vocab head only (copy=False) — the ByteGPT-style baseline (no copy path).

VERDICT
-------
  GREEN  if fab(WITH) is SUBSTANTIALLY BELOW fab(NO) and fab(VANILLA) AND meets the
         MODEL.md a303m_pass G5-L2 bar fab(WITH) <= 0.20 — RETRO grounds at 303M scale,
         the toy 0.0 survives.
  RED    if fab(WITH) ~= fab(NO) ~= fab(VANILLA) (anchor still has no effect) OR
         fab(WITH) > 0.20 — RETRO does NOT ground at real scale; the toy 0.0 was a
         toy artifact; byte-level grounding still unsolved (cf H_1142-1146).
Both are decisive + publishable (a_paper_negative_ok). FREEZE printed before measure.

HONEST SCOPE: single ckpt (dancinlab/anima-convmoe-retro-303m, baseline_fast.pt),
en-wiki only, retrieval quality is a SEPARATE axis (the byte-trigram retriever may
hand a low-overlap anchor — we report retrieval hit-rate so a NO-effect can be told
apart from a NO-anchor-available case). p7 (NOT perplexity / NOT LLM-judge), seed 7.
"""
from __future__ import annotations
import argparse, json, math, os, sys, time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_MODEL = os.path.join(_ROOT, "CLM", "model")
_TRAIN = os.path.join(_ROOT, "CLM", "train")
for _p in (_MODEL, _TRAIN, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import torch
import torch.nn.functional as F

from model import CLMConfig, CLMConvMoE                       # noqa: E402
# the production ConvMoE-RETRO module + the REAL train-time retrieval samplers
from train_convmoe_retro_prod import ConvMoERetro             # noqa: E402
from retro303m_en import semantic_anchor_batch, prior_window_batch  # noqa: E402

VOCAB = 256
SEED = 7


# ----------------------------------------------------------------- entity helpers (p7)
def _is_word_byte(b):
    return (65 <= b <= 90) or (97 <= b <= 122)  # A-Z a-z


def first_entity_after(data, pos, max_scan=200):
    """Return (start, end, bytes) of the first CAPITALIZED word at/after `pos` in `data`
    (a real named entity surrogate at byte scale). None if none within max_scan."""
    n = data.numel()
    i = pos
    end_scan = min(n, pos + max_scan)
    while i < end_scan:
        b = int(data[i].item())
        if 65 <= b <= 90:  # uppercase start
            j = i + 1
            while j < n and _is_word_byte(int(data[j].item())):
                j += 1
            if j - i >= 3:  # >= 3 letters (skip "A", "I", "Of")
                return i, j, bytes(data[i:j].tolist())
            i = j
        else:
            i += 1
    return None


def bytes_in(needle: bytes, hay: bytes):
    return needle in hay


# ----------------------------------------------------------------- decode one entity
@torch.no_grad()
def decode_entity(model, query_ctx, anchor, anchor_mask, copy, device, n_entity_bytes,
                  ctx_cap=512):
    """Greedy-decode n_entity_bytes bytes from query_ctx with the given anchor wiring.
    Returns the decoded bytes (the model's asserted continuation entity)."""
    idx = query_ctx.clone()
    out = []
    for _ in range(n_entity_bytes):
        ctx = idx[:, -ctx_cap:]
        if copy:
            probs, _ = model(ctx, anchor, anchor_mask=anchor_mask, copy=True)
        else:
            dummy = anchor[:, :1] if anchor.shape[1] >= 1 else torch.zeros(
                1, 1, dtype=torch.long, device=device)
            probs, _ = model(ctx, dummy, copy=False)
        nb = int(probs[0, -1].argmax().item())
        out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
    return bytes(out)


def build_real_pairs(data, ctx, La, gap, n_pairs, device, retrieval, gen):
    """Build REAL retrieve-then-ground must-copy cases.

    For each case: pick offset i; QUERY = data[i:i+ctx]; the must-copy true ENTITY = the
    first capitalized word starting at i+ctx (the next salient continuation entity). The
    ANCHOR = the model's OWN retrieval for offset i (semantic v2 or prior-window v1). We
    KEEP a case only when the true entity's bytes OCCUR in the retrieved anchor (genuine
    coref overlap — the case a copy head SHOULD ground). Returns a list of dicts +
    retrieval-hit bookkeeping (how many drawn offsets yielded an in-anchor entity)."""
    n = data.numel()
    sampler = semantic_anchor_batch if retrieval == "semantic" else prior_window_batch
    pairs = []
    drawn = 0
    hits = 0
    # draw in batches via the SAME sampler the model trained on so query+anchor pairing
    # is byte-identical to training (semantic_anchor_batch returns x,y,anchor,amask).
    while len(pairs) < n_pairs and drawn < n_pairs * 60:
        if retrieval == "semantic":
            x, y, anc, amask = semantic_anchor_batch(data, ctx, La, gap, 1, device, gen=gen)
        else:
            x, y, anc, amask = prior_window_batch(data, ctx, La, gap, 1, device)
        drawn += 1
        # recover the offset i: x == data[i:i+ctx]; find i by matching the first 16 bytes.
        # (semantic_anchor_batch draws i internally; we re-derive via the returned x slice
        #  to locate the true continuation entity AFTER the query.)
        head = x[0, :16].tolist()
        # locate i by scanning — but cheaper: the sampler used randint(0, n-ctx-1); we
        # brute-find the matching window start near a hash. Robust approach: search the
        # corpus for the head (rare 16-byte string => unique). Fallback: skip if ambiguous.
        i = _find_window_start(data, x[0], n, ctx)
        if i is None:
            continue
        ent = first_entity_after(data, i + ctx)
        if ent is None:
            continue
        e_start, e_end, e_bytes = ent
        anc_bytes = bytes([int(b) for b, m in zip(anc[0].tolist(), amask[0].tolist()) if m])
        if not bytes_in(e_bytes, anc_bytes):
            continue  # entity not in retrieved anchor => not a groundable must-copy case
        hits += 1
        pairs.append({
            "i": i, "query_ctx": x.clone(), "anchor": anc.clone(),
            "anchor_mask": amask.clone(),
            "true_entity": e_bytes, "n_entity_bytes": e_end - e_start,
        })
    return pairs, drawn, hits


def _find_window_start(data, window, n, ctx):
    """Find the corpus offset i such that data[i:i+ctx] == window (the sampler drew it).
    Uses the first 24 bytes as a near-unique key, verifies full match. None if not found."""
    if window.numel() < ctx:
        return None
    key = window[:24]
    # vectorized search for the first byte then verify (corpus is ~125MB; do a chunked
    # scan on the first key byte to keep it $0/fast).
    b0 = int(key[0].item())
    cand = (data[: n - ctx] == b0).nonzero(as_tuple=True)[0]
    kl = key.tolist()
    for c in cand.tolist():
        if data[c:c + 24].tolist() == kl:
            if torch.equal(data[c:c + ctx], window[:ctx]):
                return c
    return None


def run_arm(model, pairs, arm, device, ctx_cap):
    """arm in {with, no, vanilla}. Returns (fab_rate, copy_acc, n)."""
    fab = 0
    for p in pairs:
        q = p["query_ctx"]
        anc = p["anchor"]
        amask = p["anchor_mask"]
        nb = p["n_entity_bytes"]
        if arm == "with":
            dec = decode_entity(model, q, anc, amask, True, device, nb, ctx_cap)
        elif arm == "no":
            blank = torch.zeros_like(amask)
            dec = decode_entity(model, q, anc, blank, True, device, nb, ctx_cap)
        else:  # vanilla
            dec = decode_entity(model, q, anc, amask, False, device, nb, ctx_cap)
        fab += int(dec != p["true_entity"])
    n = len(pairs)
    fr = fab / max(1, n)
    return fr, 1.0 - fr, n


def load_model(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    c = ck["config"]
    cfg = CLMConfig(n_experts=c.get("n_experts", 2),
                    n_trunk_layers=c.get("n_trunk_layers", 1),
                    d_model=c["d_model"], kernel_size=c.get("kernel_size", 3),
                    variant="AB", dropout=0.0)
    m = ConvMoERetro(cfg).to(device)
    m.load_state_dict(ck["model"])
    m.eval()
    return m, ck, cfg


FREEZE = """================ H_1150 FREEZE (pre-registered, before any measurement) ================
CLAIM: the trained anima-303M ConvMoE-RETRO RETRO copy head reduces fabrication when
given a REAL RETRIEVED anchor (the prod-fire G5=1.000 was a synthetic-anchor non-result).
MODEL: dancinlab/anima-convmoe-retro-303m baseline_fast.pt (353.7M; trunk 303.6M + RETRO
       head 50.2M; ckpt sha256 a5b7dc86...). seed 7, p7 deterministic (NOT perplexity).
EVAL: REAL retrieve-then-ground must-copy. For real corpus offsets i, QUERY=data[i:i+CTX];
      true must-copy ENTITY = first capitalized word after the query; ANCHOR = the model's
      OWN train-time retrieval (semantic_anchor_batch v2; prior_window v1 reported too);
      KEEP only cases where the true entity OCCURS in the retrieved anchor (groundable).
      Greedy-decode the entity; fab = decoded != true entity. copy-acc = 1 - fab.
ARMS (same pairs, only anchor wiring differs): (1) WITH real anchor (copy=True,mask=valid)
      (2) NO anchor (copy=True,mask=0) (3) VANILLA (copy=False, vocab head only).
FROZEN FALSIFIER:
  F1 (RETRO grounds): fab(WITH) <= 0.20  AND  fab(WITH) <= fab(NO) - 0.20
                      AND  fab(WITH) <= fab(VANILLA) - 0.20.   -> GREEN
  F2 (RETRO does NOT ground / still a non-result): fab(WITH) > 0.20
                      OR  |fab(WITH) - fab(NO)| < 0.10 AND |fab(WITH)-fab(VANILLA)|<0.10
                      (anchor has no effect at real scale, like the synthetic probe). -> RED
  Bars FROZEN (MODEL.md a303m_pass G5-L2 = fab <= 0.20; H_1149 toy F1(iii) gap >= 0.40 ->
  here >= 0.20 per arm, p7). No bar moved. n>=40 in-anchor groundable cases required;
  fewer => INCONCLUSIVE (retrieval supplied too few groundable anchors, reported honestly).
======================================================================================="""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--n-pairs", type=int, default=60)
    ap.add_argument("--ctx", type=int, default=256)
    ap.add_argument("--La", type=int, default=128)
    ap.add_argument("--gap", type=int, default=64)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if dev == "cuda":
        # VRAM cap (summer co-tenant rbfe-prod must stay alive) — <= 3.5GB of 12GB.
        try:
            torch.cuda.set_per_process_memory_fraction(3.5 / 12.0, 0)
        except Exception as e:
            print(f"[warn] mem-fraction cap failed: {e}", flush=True)
    torch.manual_seed(SEED)
    print(f"[dev] {dev}", flush=True)
    print(FREEZE, flush=True)

    m, ck, cfg = load_model(a.ckpt, dev)
    print(f"[model] loaded step={ck.get('step')} val_ce={ck.get('val_ce')} "
          f"d_model={cfg.d_model} nparam={ck.get('nparam'):,}", flush=True)

    with open(a.corpus, "rb") as f:
        raw = f.read()
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).long().to(dev)
    print(f"[data] {a.corpus} {data.numel()/1e6:.1f}MB", flush=True)

    results = {"ckpt": a.ckpt, "ckpt_sha_prefix": "a5b7dc86", "seed": SEED,
               "ctx": a.ctx, "La": a.La, "gap": a.gap, "n_pairs_target": a.n_pairs,
               "retrieval": {}}

    for retrieval in ("semantic", "prior"):
        gen = torch.Generator(device="cpu").manual_seed(SEED)
        t0 = time.time()
        pairs, drawn, hits = build_real_pairs(
            data, a.ctx, a.La, a.gap, a.n_pairs, dev, retrieval, gen)
        ctx_cap = max(a.ctx, cfg.block if hasattr(cfg, "block") else a.ctx)
        if len(pairs) == 0:
            print(f"[{retrieval}] 0 groundable pairs from {drawn} draws — INCONCLUSIVE",
                  flush=True)
            results["retrieval"][retrieval] = {"n_pairs": 0, "drawn": drawn,
                                               "hits": hits, "inconclusive": True}
            continue
        fr_with, ca_with, n = run_arm(m, pairs, "with", dev, ctx_cap)
        fr_no, ca_no, _ = run_arm(m, pairs, "no", dev, ctx_cap)
        fr_van, ca_van, _ = run_arm(m, pairs, "vanilla", dev, ctx_cap)
        dt = time.time() - t0
        gap_no = fr_no - fr_with
        gap_van = fr_van - fr_with
        f1 = (fr_with <= 0.20) and (gap_no >= 0.20) and (gap_van >= 0.20)
        no_effect = (abs(fr_with - fr_no) < 0.10) and (abs(fr_with - fr_van) < 0.10)
        f2 = (fr_with > 0.20) or no_effect
        verdict = "GREEN" if f1 else ("RED" if f2 else "AMBIGUOUS")
        rr = {"n_pairs": n, "drawn": drawn, "hits": hits,
              "retrieval_hit_rate": round(hits / max(1, drawn), 4),
              "fab_with_anchor": round(fr_with, 4), "copy_acc_with": round(ca_with, 4),
              "fab_no_anchor": round(fr_no, 4), "copy_acc_no": round(ca_no, 4),
              "fab_vanilla": round(fr_van, 4), "copy_acc_vanilla": round(ca_van, 4),
              "gap_no_minus_with": round(gap_no, 4),
              "gap_vanilla_minus_with": round(gap_van, 4),
              "F1_grounds": bool(f1), "F2_no_ground": bool(f2),
              "no_effect_signature": bool(no_effect), "verdict": verdict,
              "wall_s": round(dt, 1),
              "inconclusive": bool(n < 40)}
        results["retrieval"][retrieval] = rr
        print(f"\n[{retrieval}] n={n} (drawn={drawn} hit_rate={hits/max(1,drawn):.3f}) "
              f"{dt:.0f}s", flush=True)
        print(f"  ARM WITH-anchor   fab={fr_with:.4f}  copy-acc={ca_with:.4f}", flush=True)
        print(f"  ARM NO-anchor     fab={fr_no:.4f}  copy-acc={ca_no:.4f}", flush=True)
        print(f"  ARM VANILLA       fab={fr_van:.4f}  copy-acc={ca_van:.4f}", flush=True)
        print(f"  gap(NO-WITH)={gap_no:+.4f}  gap(VAN-WITH)={gap_van:+.4f}", flush=True)
        print(f"  F1_grounds={f1}  F2_no_ground={f2}  no_effect={no_effect}  "
              f"=> {verdict}{'  [n<40 INCONCLUSIVE]' if n < 40 else ''}", flush=True)

    # overall verdict: prod trained on SEMANTIC retrieval => semantic is the primary arm.
    prim = results["retrieval"].get("semantic", {})
    overall = prim.get("verdict", "INCONCLUSIVE")
    if prim.get("inconclusive"):
        overall = "INCONCLUSIVE"
    results["overall_verdict"] = overall
    results["primary_retrieval"] = "semantic"
    print(f"\n=== H_1150 OVERALL (primary=semantic) => {overall} ===", flush=True)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(results, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"[out] {a.out}", flush=True)


if __name__ == "__main__":
    main()
