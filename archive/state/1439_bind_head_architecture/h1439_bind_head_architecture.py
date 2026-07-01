#!/usr/bin/env python3
"""H_1439 — learnable BIND-HEAD architecture (comparator-slot x measurable-slot -> weld).

ANGLE (vs the H_1435/36/37 triple-WALL):
  H_1435 (continued-pretrain), H_1436 (co-occurrence aux), H_1437 (form-supervised) all
  installed the SURFACE FORM of a falsifiable claim but the cross-shuffle control did NOT
  collapse -> the comparator-leg and the measurable-leg were INTERCHANGEABLE shells, not a
  bound pair. The H_1431 diagnosis: the external deterministic weld was STARVED because the
  mouth never emitted comparator+measurable from the SAME idea.

  H_1439 adds a learnable INTERNAL binder to the ARCHITECTURE (a_engine_native_learning:
  engine-transform-to-fit-the-learning). Biological lens (a_no_llm_frame_trap): PFC / working
  memory variable-binding (Hummel-Holyoak role-filler binding) — two independent ROLE slots
  each read a FILLER from context, and a bilinear WELD binds them into one negatable claim.
  This is NOT the H_1436 co-occurrence aux (a soft reward on the LM head); it is a dedicated
  2-slot binding HEAD wired into the residual stream.

ARCHITECTURE (BindHeadByteGPT):
  - frozen 303M ByteGPT backbone (h1129c), final hidden states H in R^{B,T,d}.
  - COMPARATOR slot: a learnable query q_c reads a comparator FILLER c = softmax(H q_c) . H.
  - MEASURABLE slot: a learnable query q_m reads a measurable FILLER m = softmax(H q_m) . H.
  - WELD: a bilinear bind w = tanh(c W m + b) (role-filler product, NOT a concat) -> the only
    place the two slots interact. w is broadcast to every position and added (via a learned
    gate) into the residual stream before the (tied) LM head. The binding is the product:
    swapping the measurable filler from a different idea changes w multiplicatively.

TRAINING (backbone FROZEN, only the bind-head learns):
  full LM CE on the SAME falsifiable-claim corpus the H_1435 WALL used (templated comparator+
  measurable claims over eval-DISJOINT subjects), so the only NEW capacity is the binder. The
  corpus subjects, the gauge IDEATION eval seeds, and the held-out seeds are all DISJOINT
  (anti-tune-to-green). 3 seeds [7, 4302, 4303].

FROZEN 5-bar = g6_common VERBATIM (h1305 _is_falsifiable VERBATIM + gauge_lib._decode):
  B1 FALS-FLOOR  FALS_in>=1
  B2 COUNT       DIST_in>=5
  B3 X-SHUFFLE   FALS_shuf<FALS_in  (DECISIVE COLLAPSE — the H_1435/36/37 killer)
  B4 HELD-OUT    FALS_ho>=1
  B5 vs-BASE     FALS_in>=base+1
  CTRL SHUF-CORP lift_real-lift_shuf>=1 (byte-shuffled-corpus bind-head must be INERT)

VERDICT (g6_common.print_bars VERBATIM):
  GREEN iff B1&B2&B3&B4&B5 AND control inert -> WALL=LEARN-GAP (the binder broke it).
  WALL  otherwise -> the learnable binder did NOT break G6 FALS binding -> WALL=CAPACITY.

torch + gauge_lib._decode => DIRECTIONAL (wired: DIRECTIONAL-mirror); engine-native re-measure
is the ING follow-on (a_engine_native_learning / a_verified_must_wire).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import torch.nn as nn
import torch.nn.functional as F

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

import h1435_continued_pretrain as base1435
gen_corpus = base1435.gen_corpus
shuffle_bytes = base1435.shuffle_bytes
make_batches = base1435.make_batches


class BindHead(nn.Module):
    """2-slot role-filler binder welded into the residual stream.

    comparator-slot query q_c and measurable-slot query q_m each pool the backbone
    hidden states into a role-specific filler; a bilinear weld binds the two fillers
    (a multiplicative product, NOT a concat) and a learned gate injects the bound
    vector back into every position before the tied LM head.
    """

    def __init__(self, d, r=128):
        super().__init__()
        self.d = d
        self.r = r
        # role queries (one per slot) — independent readers
        self.q_comp = nn.Parameter(torch.randn(d) * 0.02)
        self.q_meas = nn.Parameter(torch.randn(d) * 0.02)
        # project each filler into the bind space
        self.proj_comp = nn.Linear(d, r, bias=False)
        self.proj_meas = nn.Linear(d, r, bias=False)
        # bilinear weld: w = tanh( sum_k c_k W_k m )  (role-filler binding)
        self.weld = nn.Bilinear(r, r, d, bias=True)
        # learned scalar gate for how strongly the weld enters the residual stream.
        # NOTE: gate AND weld.weight must NOT both be zero-init — that is a multiplicative
        # dead-gradient zone (d loss/d gate ∝ w≈0, d loss/d weld ∝ gate=0 => head inert,
        # which would FALSELY read as a capacity WALL, c16 type-c init bug, NOT a verdict).
        # Fix: gate starts LIVE (1.0) and weld.weight is small-random so the head begins as
        # a NEAR-noop (small magnitude) but has live gradient from step 0.
        self.gate = nn.Parameter(torch.ones(1))
        nn.init.normal_(self.weld.weight, std=1e-3)  # small-random => near-noop, live grad
        nn.init.zeros_(self.weld.bias)

    def forward(self, hidden):
        # hidden: (B, T, d). Slot-attention pool over the time axis.
        # comparator filler
        att_c = torch.softmax(hidden @ self.q_comp, dim=1)          # (B, T)
        c = torch.einsum("bt,btd->bd", att_c, hidden)               # (B, d)
        # measurable filler
        att_m = torch.softmax(hidden @ self.q_meas, dim=1)          # (B, T)
        m = torch.einsum("bt,btd->bd", att_m, hidden)               # (B, d)
        # project + bilinear weld (the ONLY place the two slots interact)
        cp = self.proj_comp(c)                                      # (B, r)
        mp = self.proj_meas(m)                                      # (B, r)
        w = torch.tanh(self.weld(cp, mp))                           # (B, d)
        # inject into every position via the learned gate
        return self.gate * w.unsqueeze(1)                          # (B, 1, d) broadcast


class BindHeadByteGPT(nn.Module):
    """Frozen ByteGPT backbone + learnable BindHead welded before the tied LM head.

    Forward signature matches the base ByteGPT (returns (logits, loss)) so the FROZEN
    gauge_lib._decode path (`model(ctx)` -> logits) works UNCHANGED — the bind-head is
    engine-native in the decode mouth, not a post-hoc eval wrapper.
    """

    def __init__(self, backbone, d, r=128):
        super().__init__()
        self.backbone = backbone           # the loaded 303M ByteGPT
        self.block = backbone.block
        self.bind = BindHead(d, r=r)
        self.grad_ckpt = False
        self.bind_on = True                # ABLATION toggle (OFF == frozen-base regression)

    def _hidden(self, idx):
        s = self.backbone
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        return x  # pre-final-LN hidden states

    def forward(self, idx, targets=None):
        s = self.backbone
        x = self._hidden(idx)
        if self.bind_on:
            weld = self.bind(x)                   # (B, 1, d) bound role-filler injection
            h = s.ln_f(x + weld)                  # weld enters the residual stream
        else:
            h = s.ln_f(x)                         # ABLATED: exact frozen-base regression
        logits = s.head(h)
        loss = F.cross_entropy(logits.view(-1, 256), targets.view(-1)) if targets is not None else None
        return logits, loss


def build_bindhead_model(ckpt_path, device, r=128, freeze_backbone=True):
    backbone, cfg = C.load_model(ckpt_path, device)
    m = BindHeadByteGPT(backbone, d=cfg["d"], r=r).to(device)
    if freeze_backbone:
        for p in m.backbone.parameters():
            p.requires_grad_(False)
    return m, cfg


def train(m, cfg, corpus_text, steps, device, lr=3e-4, bs=16, freeze_backbone=True):
    m.train()
    # only the bind-head (and optionally backbone) parameters get gradients
    params = [p for p in m.parameters() if p.requires_grad]
    n_train = sum(p.numel() for p in params)
    n_total = sum(p.numel() for p in m.parameters())
    print(f"    [bindhead] trainable={n_train:,} / total={n_total:,} "
          f"(backbone {'FROZEN' if freeze_backbone else 'LIVE'})", flush=True)
    opt = torch.optim.AdamW(params, lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, loss = m(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1439 step {st:4d}] ce={loss.item():.4f} gate={float(m.bind.gate):.4f} "
                  f"{(time.time()-t0)/60:.1f}min", flush=True)
    return m


def save_bindhead(m, cfg, out_path, meta):
    torch.save({"model": m.state_dict(),
                "config": {"vocab": 256, "d": cfg["d"], "n_layer": cfg["n_layer"],
                           "n_head": cfg["n_head"], "block": cfg["block"], "bind_r": m.bind.r},
                "meta": meta}, out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=600)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--r", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--unfreeze", action="store_true",
                    help="also low-lr the backbone (default: backbone frozen)")
    args = ap.parse_args()
    dev = args.device
    freeze = not args.unfreeze

    print(f"[H_1439] device={dev} steps={args.steps} r={args.r} lr={args.lr} "
          f"freeze_backbone={freeze}", flush=True)

    # BASE eval = the plain backbone (no bind-head) — the floor the binder must beat
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1439] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    corpus = gen_corpus(args.lines, seed=1439)

    # REAL bind-head training (frozen backbone)
    m, _ = build_bindhead_model(C.CKPT_BASE, dev, r=args.r, freeze_backbone=freeze)
    m = train(m, cfg, corpus, args.steps, dev, lr=args.lr, freeze_backbone=freeze)
    out_pt = os.path.join(OUT, "h1439_bind_head.pt")
    os.makedirs(OUT, exist_ok=True)
    save_bindhead(m, cfg, out_pt, {"variant": "H_1439", "steps": args.steps,
                                   "r": args.r, "lr": args.lr, "freeze_backbone": freeze})
    m.bind_on = True
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))
    print(f"[H_1439] trained gate={float(m.bind.gate):.4f}", flush=True)

    # ABLATED arm (leg-B emergence): head OFF on the SAME trained object == frozen-base.
    m.bind_on = False
    ablated_eval = C.evaluate(m, cfg, "ablated_bind_off", list(C.g.IDEATION_SEEDS))
    m.bind_on = True
    ablation_clean = abs(ablated_eval["FALS_in"] - base_eval["FALS_in"]) < 1e-9
    print(f"[H_1439] ABLATED(head OFF) FALS_in={ablated_eval['FALS_in']} "
          f"vs BASE={base_eval['FALS_in']}  clean={ablation_clean}", flush=True)
    del m
    torch.cuda.empty_cache()

    # SHUFFLE-CORPUS control: SAME bytes token-shuffled (structure destroyed). A bind-head
    # trained here must be INERT — if the lift persists it is an artifact => INVALID.
    shuf_corpus = shuffle_bytes(corpus, seed=1439)
    ms, _ = build_bindhead_model(C.CKPT_BASE, dev, r=args.r, freeze_backbone=freeze)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev, lr=args.lr, freeze_backbone=freeze)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    bars = C.print_bars("H_1439 bind-head architecture", base_eval, trained_eval, shuf_eval)

    print("\n  ---- BIND-HEAD ABLATION (leg-B emergence) ----", flush=True)
    print(f"  ABLATED(head OFF) FALS_in={ablated_eval['FALS_in']} "
          f"vs BASE FALS_in={base_eval['FALS_in']}  clean={ablation_clean} "
          f"(lift must be FROM the head)", flush=True)

    out = {"variant": "H_1439", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "arch": {"bind_r": args.r, "freeze_backbone": freeze, "lr": args.lr,
                    "steps": args.steps, "lines": args.lines},
           "base": base_eval, "trained": trained_eval,
           "ablated": ablated_eval, "shuffle_corpus": shuf_eval,
           "ablation_clean": bool(ablation_clean), "bars": bars}
    json.dump(out, open(os.path.join(OUT, "h1439_result.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1439 done] {OUT}/h1439_result.json", flush=True)


if __name__ == "__main__":
    main()
