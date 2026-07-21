#!/usr/bin/env python3
"""H_007 mech-5 G-1 — d=64 kill-only smoke ($0 cash, local MPS/CPU, hours).

DESIGN_fable5_seed.md §5-G1. Passing CANNOT prove the d=384 run (G3-0b discipline); FAILING kills
mech-5 at near-$0 before the ~7h G-2 spend. Two decisive measurements on a tiny d=64 trunk:

  (i)  P-conflict — measure cos(∇θ_trunk CE_A, ∇θ_trunk CE_G) over the drill. If NO early conflict
       (cos ≥ 0 throughout) the two objectives are COMPATIBLE at this scale ⇒ the tension premise is
       EMPIRICALLY ABSENT ⇒ KILL, write exactly that (K1).
  (ii) Probe separation — after training, linear-probe the held-out role-code (subject-class) from the
       frozen trunk. If probe(A-tug) − probe(C-dup) ≤ 0 the conflict shapes nothing ⇒ KILL before any
       d=384 spend (K2-precursor). Sets τ and E[A-tug] empirically for the G-2 freeze.

ONE shared trunk (base CLMConvMoE, NO struct injection — mech-5 has no delivered field), TWO byte-LM
heads reading the same trunk state:
  - head-A: forward next-byte CE over surface+answer (the LM objective, always).
  - head-G: next-byte CE over swap(surface) at surface positions (A-tug) — the role-swapped rendering
    forces the shared state to encode BOTH fillers AND their roles; OR forward-dup (C-dup control =
    identical params/compute/gradient-volume, ZERO objective conflict).
The ONLY across-arm difference is head-G's target bytes. cos is measured over the SHARED trunk params
(embed/conv/trunk/moe/norm_out), excluding both readout heads.

Run:  python3 state/h007_gradient_tug_role_code_drill_2026-07-17/train_g1_smoke.py [--tiny]
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_ANIMA = "/Users/mini/dancinlab/anima"
_NSMC = os.path.join(_ANIMA, "state", "nbind_curriculum", "ratings_train.txt")
sys.path.insert(0, _ANIMA)
sys.path.insert(0, _HERE)

import build_swap_xor as bx        # grammar: render/render_swap/pools/AGREE/OBJ_MARK/_all_pairs/gold_bit


# ---------------------------------------------------------------- corpus (reuse H_004's NSMC path)
def _nsmc_lines(n):
    if not os.path.exists(_NSMC):
        return ["영화 재미있다 좋다 정말"] * n            # smoke fallback if corpus absent
    raw = open(_NSMC, encoding="utf-8").read().splitlines()[1:]
    docs = [r.split("\t")[1] for r in raw if len(r.split("\t")) > 1]
    return (docs * (n // max(len(docs), 1) + 1))[:n]


def _cpt_windows(lines, seq_len, torch):
    stream = ("\n".join(lines)).encode("utf-8")
    arr = np.frombuffer(stream, dtype=np.uint8)
    nwin = len(arr) // seq_len
    return torch.tensor(arr[:nwin * seq_len].reshape(nwin, seq_len).astype(np.int64))


# ---------------------------------------------------------------- drill grid (drilled, non-reserved)
def build_drill():
    """SWAP-XOR sentences on DRILLED pairings (disjoint from the f2 reserved set). Each item carries
    the surface, the gold answer suffix, and swap(surface) for head-G."""
    reserved = set(map(tuple, json.load(open(os.path.join(_HERE, "swap_xor_reserved.json")))["reserved_pairings"]))
    items = []
    for cs in (0, 1):
        allp = [p for p in bx._all_pairs(cs) if p not in reserved]
        # balanced across marker & order → gold balanced per lexeme (drill stays heuristic-neutral)
        for order in bx.ORDERS:
            for marker in (0, 1):
                for (ns, no) in allp[:48]:                 # 48 pairs × 2 order × 2 marker × 2 cs = 384
                    g = bx.gold_bit(cs, marker)
                    items.append({
                        "surface": bx.render(ns, no, marker, order),
                        "answer": bx.AGREE[g],
                        "swap": bx.render_swap(ns, no, marker, order),
                        "cell": {"class_subj": cs, "marker": marker, "order": order, "gold": g,
                                 "n_subj": ns, "n_obj": no},
                    })
    return items


# ---------------------------------------------------------------- two-head model
def _load(tiny):
    import torch
    import core.model as M
    d, L, E = (48, 2, 2) if tiny else (64, 2, 2)
    cfg = M.CLMConfig(vocab_size=256, d_model=d, n_trunk_layers=L, n_experts=E)

    class TwoHead(M.CLMConvMoE):
        def __init__(self, cfg):
            super().__init__(cfg)
            self.head_g = torch.nn.Conv1d(cfg.d_model, cfg.vocab_size, 1)   # mirrors readout (B,V,T)

        def trunk_state(self, tokens):
            x = self.embed(tokens).transpose(1, 2)          # (B,C,T)
            x = self.embed_conv(x)
            for layer in self.trunk:
                x = layer(x)
            x, stats = self.moe(x)
            x = self.norm_out(x)
            return x, stats.aux_loss                         # (B,C,T)

        def both_logits(self, tokens):
            x, aux = self.trunk_state(tokens)
            return self.readout(x), self.head_g(x), aux      # each (B,V,T)

    return torch, M, cfg, TwoHead


def _trunk_params(model):
    """SHARED trunk params only — exclude both readout heads (readout = head-A, head_g = head-G)."""
    ex = set(id(p) for p in model.readout.parameters()) | set(id(p) for p in model.head_g.parameters())
    return [p for p in model.parameters() if id(p) not in ex]


# ---------------------------------------------------------------- batching
def _drill_batch(torch, items, arm, device, pad):
    B = len(items)
    tok = np.zeros((B, pad), np.int64)
    tgtA = np.zeros((B, pad), np.int64); tgtG = np.zeros((B, pad), np.int64)
    mA = np.zeros((B, pad), np.float32); mG = np.zeros((B, pad), np.float32)
    for bi, it in enumerate(items):
        surf = it["surface"].encode("utf-8"); ans = it["answer"].encode("utf-8")
        swap = it["swap"].encode("utf-8")
        seq = (surf + ans)[:pad]; Ls = len(surf); L = len(seq)
        tok[bi, :L] = list(seq)
        tgtA[bi, :L - 1] = list(seq[1:]); mA[bi, :L - 1] = 1.0            # head-A: full LM
        # head-G target: A-tug → swap(surface); C-dup → forward surface (duplicate). surface positions only.
        gseq = swap if arm == "A-tug" else surf
        n = min(Ls, len(gseq))
        tgtG[bi, :n - 1] = list(gseq[1:n]); mG[bi, :n - 1] = 1.0
    t = lambda a: torch.tensor(a, device=device)
    return t(tok), t(tgtA), t(tgtG), t(mA), t(mG)


def _masked_ce(torch, logits, tgt, mask):
    import torch.nn.functional as F
    ce = F.cross_entropy(logits, tgt, reduction="none")           # (B,T)
    return (ce * mask).sum() / mask.sum().clamp(min=1.0)


# ---------------------------------------------------------------- probe (self-contained torch logistic)
def _probe_acc(torch, X, y, seed, iters=300):
    """Held-out linear-probe accuracy: 70/30 split, logistic regression by SGD. X:(n,d) y:(n,) 0/1."""
    g = torch.Generator().manual_seed(seed)
    n = X.shape[0]; perm = torch.randperm(n, generator=g)
    ntr = int(n * 0.7)
    Xtr, ytr = X[perm[:ntr]], y[perm[:ntr]]; Xte, yte = X[perm[ntr:]], y[perm[ntr:]]
    mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w = torch.zeros(X.shape[1], requires_grad=True); b = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([w, b], lr=0.05)
    lossf = torch.nn.BCEWithLogitsLoss()
    for _ in range(iters):
        opt.zero_grad(); loss = lossf(Xtr @ w + b, ytr.float()); loss.backward(); opt.step()
    with torch.no_grad():
        pred = (Xte @ w + b > 0).long()
        return float((pred == yte).float().mean().item())


def _f2_dacc(torch, model, panel, device, pad):
    """THE faithful metric (mirrors G-2): forced-choice d_acc on f2. Teacher-force the surface, then
    compare NLL(gold agreement suffix) vs NLL(alt suffix) — this tests the ROLE-BINDING COMPOSITION
    (gold = class(subj)⊕marker at non-adjacent sites), not a free lexical ingredient. Single answer
    slot (3 bytes), free-slot=[0]. d_acc = mean(NLL_gold ≤ NLL_alt)."""
    model.eval()
    correct = 0
    with torch.no_grad():
        for it in panel:
            surf = it["surface"].encode("utf-8"); gold = it["gold_token"].encode("utf-8")
            alt = bx.AGREE[1 - bx.AGREE.index(it["gold_token"])].encode("utf-8")
            Ls = len(surf)

            def nll_suffix(sfx):
                seq = (surf + sfx)[:pad]
                tok = torch.zeros(1, pad, dtype=torch.long, device=device)
                tok[0, :len(seq)] = torch.tensor(list(seq), device=device)
                la, _, _ = model.both_logits(tok)                       # (1,V,pad)
                logp = torch.log_softmax(la[0], dim=0)                  # (V,pad)
                tot = 0.0
                for j in range(3):                                     # 3 answer bytes
                    p = Ls + j
                    tot += -logp[seq[p], p - 1].item()                 # predict byte@p from p-1
                return tot
            if nll_suffix(gold) <= nll_suffix(alt):
                correct += 1
    return correct / len(panel)


def _role_states(torch, model, panel, device, pad):
    """Frozen trunk state at the answer-predict position for each f2 item → (n,d), + class labels."""
    model.eval()
    xs, cs_lab, co_lab = [], [], []
    with torch.no_grad():
        for it in panel:
            surf = it["surface"].encode("utf-8"); ans = it["gold_token"].encode("utf-8")   # f2 uses gold_token
            seq = (surf + ans)[:pad]; Ls = len(surf)
            tok = torch.zeros(1, pad, dtype=torch.long, device=device)
            tok[0, :len(seq)] = torch.tensor(list(seq), device=device)
            st, _ = model.trunk_state(tok)                 # (1,C,T)
            xs.append(st[0, :, Ls - 1].float().cpu())      # state predicting the first answer byte
            cs_lab.append(it["cell"]["class_subj"]); co_lab.append(1 if it["cell"]["n_obj"] in bx.HON else 0)
    return torch.stack(xs), torch.tensor(cs_lab), torch.tensor(co_lab)


# ---------------------------------------------------------------- train one arm
def train_arm(arm, torch, cfg_tuple, drill, f2, cpt_win, steps, device, tag):
    _, M, cfg, TwoHead = cfg_tuple
    torch.manual_seed(0)
    model = TwoHead(cfg).to(device)
    tp = _trunk_params(model)
    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    cpt_steps, drill_steps = steps
    pad = 48
    logf = os.path.join(_HERE, f"g1_log_{tag}.jsonl")
    open(logf, "w").close()

    def log(rec):
        with open(logf, "a") as fh:
            fh.write(json.dumps({"arm": arm, **rec}, ensure_ascii=False) + "\n")

    # CPT — trunk becomes a real byte-LM (head-A only; struct-free)
    bs = 16 if device != "cpu" else 8
    for step in range(cpt_steps):
        idx = torch.randint(0, cpt_win.shape[0], (bs,))
        w = cpt_win[idx].to(device)
        la, _, aux = model.both_logits(w[:, :-1])
        loss = torch.nn.functional.cross_entropy(la, w[:, 1:]) + aux
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 400 == 0 or step == cpt_steps - 1:
            log({"phase": "cpt", "step": step, "ce": round(float(loss.detach()), 4)})

    # drill — two-head tension; measure cos(∇CE_A, ∇CE_G) over shared trunk
    cos_hist = []
    rng = np.random.RandomState(0)
    B = 32
    for step in range(drill_steps):
        bidx = rng.randint(0, len(drill), size=B)
        batch = [drill[i] for i in bidx]
        tok, tgtA, tgtG, mA, mG = _drill_batch(torch, batch, arm, device, pad)
        la, lg, aux = model.both_logits(tok)
        ceA = _masked_ce(torch, la, tgtA, mA)
        ceG = _masked_ce(torch, lg, tgtG, mG)
        # P-conflict: separate trunk-gradient cosine (log every 20 steps to bound cost)
        if step % 20 == 0:
            gA = torch.autograd.grad(ceA, tp, retain_graph=True, allow_unused=True)
            gG = torch.autograd.grad(ceG, tp, retain_graph=True, allow_unused=True)
            fa = torch.cat([g.reshape(-1) for g in gA if g is not None])
            fg = torch.cat([g.reshape(-1) for g in gG if g is not None])
            cos = float((fa @ fg / (fa.norm() * fg.norm() + 1e-9)).item())
            cos_hist.append({"step": step, "cos": round(cos, 4)})
            if step % 200 == 0:
                log({"phase": "drill", "step": step, "ceA": round(float(ceA.detach()), 4),
                     "ceG": round(float(ceG.detach()), 4), "cos_grad": round(cos, 4)})
        loss = ceA + ceG + aux
        opt.zero_grad(); loss.backward(); opt.step()

    # THE faithful role-binding metric: forced-choice d_acc on f2 (mirrors G-2). Plus the free-ingredient
    # probes as DIAGNOSTICS only (subject/object class are freely encoded — NOT the role-code).
    f2_dacc = _f2_dacc(torch, model, f2, device, pad)
    Xs, cs_lab, co_lab = _role_states(torch, model, f2, device, pad)
    p_subj = _probe_acc(torch, Xs, cs_lab, seed=1)
    p_obj = _probe_acc(torch, Xs, co_lab, seed=2)
    early = [c["cos"] for c in cos_hist if c["step"] < 0.3 * drill_steps]
    frac_neg = sum(1 for c in early if c < 0) / max(len(early), 1)
    result = {"arm": arm, "f2_dacc": round(f2_dacc, 4),
              "probe_subj_class": round(p_subj, 4), "probe_obj_class": round(p_obj, 4),
              "cos_frac_neg_early": round(frac_neg, 4), "cos_min": round(min([c["cos"] for c in cos_hist], default=0.0), 4),
              "cos_mean_early": round(float(np.mean(early)) if early else 0.0, 4),
              "cos_trajectory": cos_hist}
    log({"phase": "result", **{k: v for k, v in result.items() if k != "cos_trajectory"}})
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiny", action="store_true", help="d=48, few steps — plumbing smoke only")
    args = ap.parse_args()

    torch, M, cfg, TwoHead = _load(args.tiny)
    import torch as _t
    device = "mps" if _t.backends.mps.is_available() else "cpu"
    cfg_tuple = (torch, M, cfg, TwoHead)

    steps = (60, 80) if args.tiny else (1500, 2000)
    n_cpt = 400 if args.tiny else 3000
    cpt_win = _cpt_windows(_nsmc_lines(n_cpt), 128, torch)
    drill = build_drill()
    f2 = json.load(open(os.path.join(_HERE, "swap_xor_f2.json")))["panel"]

    print("=" * 78)
    print(f"H_007 mech-5 G-1 kill-only smoke — device={device} d={cfg.d_model} "
          f"steps={steps} drill={len(drill)} f2={len(f2)}")
    print("=" * 78, flush=True)

    arms = {}
    for arm in ("A-tug", "C-dup"):
        print(f"\n--- training {arm} …", flush=True)
        arms[arm] = train_arm(arm, torch, cfg_tuple, drill, f2, cpt_win, steps, device, tag=arm)
        r = arms[arm]
        print(f"  {arm}: f2_dacc={r['f2_dacc']} | probe_subj={r['probe_subj_class']} (free-ingredient "
              f"diagnostic) | cos_frac_neg_early={r['cos_frac_neg_early']} cos_mean_early={r['cos_mean_early']} "
              f"cos_min={r['cos_min']}", flush=True)

    at, cd = arms["A-tug"], arms["C-dup"]
    # P-conflict must be DIFFERENTIAL vs the C-dup control: raw trunk-gradient cos is confounded by the
    # two heads being SEPARATE readouts (decorrelated grads at init even for zero-conflict duplicate
    # objectives — the --tiny plumbing run measured C-dup cos ≈ A-tug cos, proving absolute cos is not
    # specific to the role-swap). The role-swap conflicts with forward-LM iff A-tug stays MORE conflicted
    # than its compute-matched duplicate-objective control (whose two heads should converge). More
    # negative cos_mean_early = more conflict, so conflict_diff = cd − at (positive ⇒ A-tug more conflicted).
    TAU = 0.05                                                   # differential floor (frozen at G-2 from this)
    conflict_diff = round(cd["cos_mean_early"] - at["cos_mean_early"], 4)   # >0 ⇒ A-tug more conflicted
    conflict_present = conflict_diff >= TAU
    # PRIMARY kill instrument = the faithful role-binding metric (f2 forced-choice d_acc), A-tug vs the
    # compute-matched C-dup control. The subject-class probe is a FREE-INGREDIENT diagnostic (both arms
    # ~ceiling — it does NOT isolate the composition), so it CANNOT license a kill on its own.
    dacc_sep = round(at["f2_dacc"] - cd["f2_dacc"], 4)
    probe_sep = round(at["probe_subj_class"] - cd["probe_subj_class"], 4)
    kill = (not conflict_present) or (dacc_sep <= 0.0)
    if not conflict_present:
        verdict = (f"KILL (K1) — no DIFFERENTIAL conflict vs C-dup (conflict_diff {conflict_diff} < τ={TAU}: "
                   f"role-swap no more conflicted than duplicate-forward; absolute cos is head-init noise).")
    elif dacc_sep <= 0.0:
        verdict = (f"KILL (K2) — conflict is present and role-specific (conflict_diff {conflict_diff} ≥ "
                   f"τ={TAU}) BUT buys nothing: f2 d_acc A-tug {at['f2_dacc']} ≤ C-dup {cd['f2_dacc']} "
                   f"(sep {dacc_sep}) — the tension shapes no role-binding the forward objective lacks. "
                   f"The OMEGA-consistent red. (Free-ingredient probe A-tug {at['probe_subj_class']} vs "
                   f"C-dup {cd['probe_subj_class']} is a diagnostic, not the metric.)")
    else:
        verdict = (f"PROCEED-CANDIDATE — role-specific conflict (conflict_diff {conflict_diff} ≥ τ={TAU}: "
                   f"A-tug cos_mean_early {at['cos_mean_early']} vs C-dup {cd['cos_mean_early']}, resolves "
                   f"late) AND faithful role-binding gain: f2 d_acc A-tug {at['f2_dacc']} > C-dup "
                   f"{cd['f2_dacc']} (sep +{dacc_sep}). NOT a d=384 result (G3-0b: smoke passing ≠ proof); "
                   f"sets τ={TAU}, E[A-tug d_acc]≈{at['f2_dacc']} for the G-2 freeze.")

    out = {"device": device, "d": cfg.d_model, "steps": steps, "conflict_diff_vs_cdup": conflict_diff,
           "conflict_present": conflict_present, "f2_dacc_separation": dacc_sep,
           "probe_separation_subj_DIAGNOSTIC": probe_sep, "kill": kill, "verdict": verdict, "arms": arms}
    json.dump(out, open(os.path.join(_HERE, "g1_smoke_result.json"), "w"), ensure_ascii=False, indent=1)
    print("\n" + "=" * 78)
    print("G-1 VERDICT:", verdict)
    print("wrote g1_smoke_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
