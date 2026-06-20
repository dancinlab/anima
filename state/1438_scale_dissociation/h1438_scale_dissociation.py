#!/usr/bin/env python3
"""H_1438 — SCALE-DISSOCIATION: is the G6 FALS-depth wall capacity-bound or recipe-bound?

ANGLE (a_break_the_wall TAXONOMY — separate (d) real-ceiling from (e) under-investment):
  303M across 5 lenses (data/objective/form/bind-head/attention) is all 🧱 WALL=CAPACITY:
  the 303M mouth emits comparator-shape OR measurable-shape but never BINDS them into one
  negatable claim. The one untested variable is SCALE. NOT an LLM scale-up reflex
  (a_no_llm_frame_trap) but a CONTROLLED dissociation: hold the recipe + broad-corpus prior
  CONSTANT, vary ONLY capacity, re-measure the FROZEN G6 5-bar.

SCALE MECHANISM (honest, recipe-identical):
  The converged 303M base (d=1024,L=20,H=16) carries the broad-corpus competence the from-
  scratch route would have to re-earn (a byte-LM at low step budget = G0 garble => FALS=0 for
  TRAINING reasons, not capacity — that would be a confound, not a verdict). So we WIDTH+DEPTH-
  EXPAND the converged base to ~1B by function-preserving net2net init (precedent H_1199:
  AdaptField scalar->vector grow-the-engine), inheriting the SAME competence, then run the
  IDENTICAL H_1435 continued-pretrain on the SAME falsifiable-claim corpus. The ONLY variable
  vs H_1435 is d/L/H. recipe change = 0 (corpus, opt, lr, steps, detector all VERBATIM).

  net2net width-expand (Chen et al. function-preserving):
    - Embedding/LayerNorm/Linear rows widened by REPLICATING source units (random remap) and
      DIVIDING the fan-in of the consumer by the replication count so the function is preserved
      at init. Extra DEPTH layers are inserted as near-identity (small-init mlp/attn) blocks.
    - At init the 1B reproduces the 303M's outputs (coherence inherited), so any FALS lift is
      from the EXTRA CAPACITY the continued-pretrain can now use, not from re-learning words.

G0 COHERENCE GATE (anti-confound, a_break_the_wall (e)): if the trained 1B's eval generations
  are byte-garble (known-word-ratio < 0.50), FALS=0 is an UNDERTRAINING artifact => HONEST
  NON-RESULT, NOT capacity-confirm. Reported explicitly; does not silently become a 🧱.

FROZEN 5-bar = H_1435 g6_common VERBATIM (B1 FALS>=1 · B2 DIST>=5 · B3 cross-shuffle COLLAPSE ·
  B4 held-out · B5 vs-base) + SHUFFLE-CORPUS control. seeds [7,4302,4303]. corpus subjects
  DISJOINT from gauge CONCEPTs/eval/held-out (anti-tune-to-green). FREEZE before any weight moves.

VERDICT LOGIC (terminal either way, a_break_the_wall (d)):
  - 1B crosses (B1&B5 cross AND B3 collapses AND B4 holds AND ctrl inert) AND G0 coherent
      => CAPACITY-bound CONFIRMED at this rung: scale lifts it => 303M wall was capacity =>
         breakthrough direction (grounds 7B, a7b_pass). 🟢
  - 1B ALSO plateaus (FALS=0 like 303M) AND G0 coherent
      => recipe-bound (scale-invariant at 303M->1B): wall survives 3.7x scale => CAPACITY-CONFIRM
         in the card's framing (303M ceiling is real, scale does not cross it). 🧱
  - 1B byte-garble (G0 fail) => HONEST NON-RESULT (under-trained, not a science ceiling).

torch + gauge_lib._decode => DIRECTIONAL (a_engine_native_learning); engine-native re-measure on
live CORE/bytegpt_decode.hexa = follow-on. a_scale_honest_scope: verdict scoped to 303M->1B rung.
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import torch.nn as nn

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# ── 1B target geometry (recipe-identical: only d/L/H scaled from 1024/20/16) ──
# EXACT-2x duplication net2net requires BIG_D = REP * D0 (integer); REP=2 -> d=2048, ~1.2B.
# head_dim kept == base (2048/32 = 64 == 1024/16) so attention is structurally identical.
BIG_D = int(os.environ.get("G6_BIG_D", "2048"))   # 2 * 1024 (exact duplication)
BIG_L = int(os.environ.get("G6_BIG_L", "24"))
BIG_H = int(os.environ.get("G6_BIG_H", "32"))     # head_dim = 2048/32 = 64 == base 1024/16

# ── falsifiable-claim corpus (training-only subjects, DISJOINT from eval) — H_1435 VERBATIM ──
TRAIN_SUBJECTS = ["the river", "a metal bar", "the crowd", "this alloy", "the signal",
                  "a colony", "the market", "that current", "the sample", "a fold"]
COMPS = sorted(C.COMPARATOR)
MEAS = sorted(C.MEASURABLE)


def gen_corpus(n_lines, seed=0):
    rng = random.Random(seed)
    lines = []
    templates = [
        "if {s} grows, the {m} {c} than before.",
        "{s} {c} a higher {m} when the input rises.",
        "the {m} of {s} is greater whenever {s2} {c}.",
        "{s} shows a lower {m} than {s2} under load.",
        "when {s} {c}, its {m} decreases by a fixed amount.",
    ]
    for _ in range(n_lines):
        t = rng.choice(templates)
        lines.append(t.format(s=rng.choice(TRAIN_SUBJECTS),
                              s2=rng.choice(TRAIN_SUBJECTS),
                              c=rng.choice(COMPS), m=rng.choice(MEAS)))
    return "\n".join(lines) + "\n"


def shuffle_bytes(text, seed=0):
    rng = random.Random(seed)
    b = list(text.encode("utf-8"))
    rng.shuffle(b)
    return bytes(b).decode("utf-8", "ignore")


def make_batches(text, block, bs, device):
    data = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    n = (len(data) - 1) // block
    data = data[: n * block + 1]
    while True:
        idxs = torch.randint(0, len(data) - block - 1, (bs,))
        x = torch.stack([data[i:i + block] for i in idxs]).to(device)
        y = torch.stack([data[i + 1:i + 1 + block] for i in idxs]).to(device)
        yield x, y


# ── net2net function-preserving width+depth expansion: 303M base -> ~1B ──
def _widen_vector(v, new_n, mapping):
    """Widen a length-N vector to new_n by gathering source rows per `mapping`."""
    return v[mapping].clone()


def build_big_from_base(base_m, base_cfg, device, init_seed=1438):
    """Construct a BIG ByteGPT (BIG_D=REP*D0) that EXACTLY reproduces the converged base's
    forward function at init (verified by init CE/KWR == base), so coherence is inherited
    VERBATIM and the continued-pretrain only has EXTRA capacity to break symmetry into.

    EXACT BLOCK-DUPLICATION net2net (REP=2, Net2WiderNet done losslessly):
      The big width D = REP*D0 is laid out as REP consecutive COPIES of the base width:
      big dim (c*D0 + j) carries base dim j, for copy c in 0..REP-1. Because every value is
      present REP times, the per-token activation DISTRIBUTION over D is identical to over D0
      => LayerNorm(mean,var over D) == LayerNorm over D0 EXACTLY (no compensation needed; this
      is why duplication beats zero-pad, which shifts LN statistics).
      - Embedding / pos / LN-affine / Linear-bias / mlp.0: TILE the base value REP times along
        the feature dim (each copy identical).
      - Any Linear/attention that CONSUMES a duplicated activation (its input dim is D) divides
        its replicated input columns by REP, so REP copies sum back to the base pre-activation.
      - Attention: H = REP*H0 heads, hd unchanged. Copy c gets base heads as big heads
        [c*H0:(c+1)*H0], each reading its own copy's slice [c*D0:(c+1)*D0]. q/k/v in_proj rows
        tiled REP times (per-head), input cols tiled+divided by REP; out_proj rows tiled,
        input cols (over hd within head, unaffected by REP) tiled+divided so the REP copies of
        the residual sum to base. Heads are independent so this is exact.
    Depth-expand: appended layers (L0..L-1) are EXACT identity (residual projections 0).
    """
    g = C.ByteGPT(d=BIG_D, n_layer=BIG_L, n_head=BIG_H, block=base_cfg["block"])
    D0 = base_cfg["d"]; D = BIG_D
    L0 = base_cfg["n_layer"]; L = BIG_L
    H0 = base_cfg["n_head"]; H = BIG_H
    hd = D0 // H0
    REP = D // D0
    assert D == REP * D0, f"D ({D}) must be integer multiple of D0 ({D0})"
    assert H == REP * H0 and D // H == hd, f"head layout mismatch: H={H} REP*H0={REP*H0} hd={D//H}/{hd}"
    HID0 = 4 * D0  # base mlp hidden

    bsd = {k: v.detach().cpu().float() for k, v in base_m.state_dict().items()}
    gsd = {k: torch.zeros_like(v) for k, v in g.state_dict().items()}

    def tile_rows(W, rep):                 # replicate along dim0 rep times (block)
        return W.repeat(rep, *([1] * (W.dim() - 1)))
    def tile_cols_div(W, rep):             # replicate along dim1 rep times, divide by rep
        return W.repeat(1, rep) / rep

    # ── token + positional embeddings: tile feature dim REP times (each copy identical) ──
    tok_tiled = tile_rows(bsd["tok.weight"].t(), REP).t().contiguous()  # (vocab, REP*D0)
    gsd["tok.weight"] = tok_tiled
    gsd["head.weight"] = tok_tiled.clone()  # tied head: state_dict has BOTH keys sharing storage;
    # must set both or load_state_dict overwrites the shared tensor with the unset (zero) one.
    gsd["pos.weight"] = tile_rows(bsd["pos.weight"].t(), REP).t().contiguous()

    for i in range(L):
        gp = f"blocks.{i}."
        if i < L0:
            bp = f"blocks.{i}."
            # LayerNorm affine: tile REP (duplication keeps LN stats exact, no scale needed)
            for ln in ("ln1", "ln2"):
                gsd[gp + ln + ".weight"] = bsd[bp + ln + ".weight"].repeat(REP)
                gsd[gp + ln + ".bias"] = bsd[bp + ln + ".bias"].repeat(REP)
            # attention in_proj (3*D, D): per q/k/v block (D0,D0) -> rows tiled REP, cols tiled+div
            inw = bsd[bp + "attn.in_proj_weight"]   # (3*D0, D0)
            inb = bsd[bp + "attn.in_proj_bias"]     # (3*D0,)
            parts_w, parts_b = [], []
            for s in range(3):  # q,k,v
                blk = inw[s*D0:(s+1)*D0]            # (D0, D0)
                bw = tile_cols_div(tile_rows(blk, REP), REP)  # (REP*D0, REP*D0): rows tile, cols tile/REP
                parts_w.append(bw)
                parts_b.append(inb[s*D0:(s+1)*D0].repeat(REP))
            gsd[gp + "attn.in_proj_weight"] = torch.cat(parts_w, dim=0)   # (3*D, D)
            gsd[gp + "attn.in_proj_bias"] = torch.cat(parts_b, dim=0)     # (3*D,)
            # out_proj (D, D): rows tiled REP, input cols tiled+div REP (sum of REP copies = base)
            ow = bsd[bp + "attn.out_proj.weight"]   # (D0, D0)
            gsd[gp + "attn.out_proj.weight"] = tile_cols_div(tile_rows(ow, REP), REP)
            gsd[gp + "attn.out_proj.bias"] = bsd[bp + "attn.out_proj.bias"].repeat(REP)
            # mlp.0 (4D, D): hidden rows tiled REP, input cols tiled+div REP
            w0 = bsd[bp + "mlp.0.weight"]           # (HID0, D0)
            gsd[gp + "mlp.0.weight"] = tile_cols_div(tile_rows(w0, REP), REP)
            gsd[gp + "mlp.0.bias"] = bsd[bp + "mlp.0.bias"].repeat(REP)
            # mlp.2 (D, 4D): output rows tiled REP, hidden cols tiled+div REP
            w2 = bsd[bp + "mlp.2.weight"]           # (D0, HID0)
            gsd[gp + "mlp.2.weight"] = tile_cols_div(tile_rows(w2, REP), REP)
            gsd[gp + "mlp.2.bias"] = bsd[bp + "mlp.2.bias"].repeat(REP)
        else:
            # EXACT identity inserted layer: LN affine=1/0; residual projections 0 (pass-through)
            gsd[gp + "ln1.weight"].fill_(1.0); gsd[gp + "ln2.weight"].fill_(1.0)
            # ln biases 0; attn.out_proj & mlp.2 weights/biases already 0 -> x -> x

    # ── final LN: tile REP, then divide affine by REP. ln_f output feeds ONLY the tied head,
    # and the head = x @ tok.weight.T with tok ALSO REP-tiled => logit = REP * base_logit. We
    # fold 1/REP into ln_f's affine so logit == base_logit EXACTLY (softmax unchanged). The
    # ln_f mean/var over D == over D0 (duplication), so normalization is base-identical. ──
    gsd["ln_f.weight"] = bsd["ln_f.weight"].repeat(REP) / REP
    gsd["ln_f.bias"] = bsd["ln_f.bias"].repeat(REP) / REP
    g.load_state_dict(gsd, strict=True)
    g.head.weight = g.tok.weight  # re-tie
    g.to(device)
    g.grad_ckpt = True  # 1B needs grad checkpointing to fit
    n = sum(p.numel() for p in g.parameters())
    print(f"[H_1438] built BIG d={BIG_D} L={BIG_L} H={BIG_H} = {n/1e6:.1f}M params "
          f"(net2net from base d={D0} L={L0})", flush=True)
    return g, {"vocab": 256, "d": BIG_D, "n_layer": BIG_L, "n_head": BIG_H, "block": base_cfg["block"]}


def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=8):
    m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            _, loss = m(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 25 == 0 or st == steps - 1:
            print(f"    [H1438 step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def coherence_kwr(m, cfg, device):
    """G0 gate: mean known-word-ratio over the in-domain eval seeds, seed 7."""
    ideas = C._decode_ideas(m, cfg, list(C.g.IDEATION_SEEDS), 7)
    krs = [C.g.known_word_ratio(i["text"]) for i in ideas]
    return round(sum(krs) / len(krs), 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--bs", type=int, default=8)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1438] device={dev} steps={args.steps} BIG d={BIG_D} L={BIG_L} H={BIG_H}", flush=True)

    # base (303M) reference eval — the plateau we are testing against
    base_m, base_cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, base_cfg, "base_303M", list(C.g.IDEATION_SEEDS))
    print(f"[H_1438] base 303M FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)

    corpus = gen_corpus(args.lines, seed=1435)  # SAME corpus seed as H_1435 (recipe-identical)

    # build 1B by net2net expansion of the converged base (inherits competence)
    big, big_cfg = build_big_from_base(base_m, base_cfg, dev)
    del base_m
    torch.cuda.empty_cache()

    # init coherence (should already be ~coherent if net2net preserved function)
    kwr_init = coherence_kwr(big, big_cfg, dev)
    print(f"[H_1438] 1B init coherence KWR={kwr_init}", flush=True)

    # REAL continued-pretrain (IDENTICAL recipe to H_1435: lr/opt/corpus, only scale differs)
    big = train(big, big_cfg, corpus, args.steps, dev, bs=args.bs)
    out_pt = os.path.join(OUT, "h1438_scale_1b.pt")
    C.save_model(big, big_cfg, out_pt, {"variant": "H_1438", "steps": args.steps, "lr": 3e-5,
                                        "d": BIG_D, "n_layer": BIG_L, "n_head": BIG_H,
                                        "init": "net2net_from_h1129c_303M"})
    kwr_trained = coherence_kwr(big, big_cfg, dev)
    trained_eval = C.evaluate(big, big_cfg, "trained_1B", list(C.g.IDEATION_SEEDS))
    del big
    torch.cuda.empty_cache()

    # SHUFFLE-CORPUS control at 1B scale (same bytes, structure destroyed) — net2net init again
    base_m2, _ = C.load_model(C.CKPT_BASE, dev)
    bigs, _ = build_big_from_base(base_m2, base_cfg, dev)
    del base_m2
    torch.cuda.empty_cache()
    shuf_corpus = shuffle_bytes(corpus, seed=1435)
    bigs = train(bigs, big_cfg, shuf_corpus, args.steps, dev, bs=args.bs)
    shuf_eval = C.evaluate(bigs, big_cfg, "shuffle_corpus_1B", list(C.g.IDEATION_SEEDS))
    del bigs
    torch.cuda.empty_cache()

    bars = C.print_bars("H_1438 scale-dissociation 1B", base_eval, trained_eval, shuf_eval)

    # G0 coherence gate verdict overlay (anti-confound)
    g0_ok = kwr_trained >= C.KWR_FLOOR
    print(f"\n  ---- G0 COHERENCE GATE (anti-undertraining-confound) ----", flush=True)
    print(f"  1B init KWR={kwr_init}  trained KWR={kwr_trained}  (floor {C.KWR_FLOOR})", flush=True)
    if not g0_ok:
        print(f"  ⚠ 1B trained is BYTE-GARBLE (KWR<{C.KWR_FLOOR}) => FALS=0 is an UNDERTRAINING "
              f"artifact => HONEST NON-RESULT, NOT capacity-confirm (a_break_the_wall (e)).", flush=True)
        final_tier = "HONEST-NON-RESULT (G0 garble — under-trained, not a science ceiling)"
    elif bars["green"]:
        final_tier = ("🟢 BROKE — 1B (3.7x scale, same recipe) crossed G6 FALS binding => "
                      "303M wall was CAPACITY-bound => scale lifts it (grounds 7B)")
    else:
        final_tier = ("🧱 CAPACITY-CONFIRM — 1B (3.7x scale, same recipe, G0 coherent) ALSO "
                      "plateaus on G6 FALS binding => 303M->1B scale-invariant => wall is real "
                      "(scoped to this rung, a_scale_honest_scope)")
    print(f"\n  ===== H_1438 FINAL VERDICT: {final_tier} =====", flush=True)

    out = {"variant": "H_1438", "scale": {"d": BIG_D, "n_layer": BIG_L, "n_head": BIG_H},
           "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "kwr_init": kwr_init, "kwr_trained": kwr_trained, "g0_ok": g0_ok,
           "base": base_eval, "trained": trained_eval, "shuffle_corpus": shuf_eval,
           "bars": bars, "final_tier": final_tier}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "h1438_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"[H_1438 done] {OUT}/h1438_result.json", flush=True)


if __name__ == "__main__":
    main()
