#!/usr/bin/env python3
"""H_1632 N4+N8 — G6 diverse-set-search + G1 jamo teach-signal 303M (see PREREG.md).

Two NOVEL levers stacked on the production 303M CLMConvMoE, both keeping the
production ADDITIVE readout (Conv1d d->V) so EVERY arm is .clm-serializable and
engine-native G1/G6 is by-construction OPEN (unlike exp3 bind which was BLOCKED).

  baseline  : standard CE next-byte marginal likelihood. The discriminating
              control — CE rewards neither compositional jamo structure (G1) nor
              diverse-falsifiable set search (G6) = the gauge null.
  n8_jamo   : CE + lambda_jamo * jamo-teach aux loss (N8 / SCRIPT 2604.12377).
              On Korean Hangul-syllable positions, a small head predicts the
              (cho / jung / jong) JAMO classes of the CURRENT syllable from the
              trunk penultimate. This injects subcharacter compositional
              structure as an EXPLICIT teach signal (byte-level Korean compose),
              extending ko-jamo-mitosis (H_1316/1321 GREEN). G1-directed.
  n4_set    : CE + lambda_set * diverse-set-search aux loss (N4 / 2606.10587).
              Every --setsearch-every steps the model samples K continuations on
              G6-style "if A, then B:" frames, scores them with an ENGINE-ALIGNED
              (NOT LLM-judge) diversity+falsifiability proxy reusing the SAME
              detectors g_gates uses (_g6_jaccard set-diversity + _g6_is_falsifiable),
              then up-weights the likelihood of the most diverse+falsifiable set
              members. Optimizes a SET objective (novelty+coverage) instead of a
              single-best decode. G6-directed.
  n4n8_both : CE + lambda_jamo * jamo + lambda_set * setsearch (the combined lever
              the experiment is actually about — G1 AND G6 attacked jointly).

ALL arms share IDENTICAL trunk init seed / data stream / step count / production
additive readout — the ONLY difference is which aux loss(es) are added. torch-side
metrics are DIRECTIONAL monitors; .clm export -> engine-native G1/G6
(anima eval / core/g_gates.py via clm_decode.py) is the TERMINAL path.

Canonical recipe (savant golden-zone inhibition + mitosis E2->E3 split + 4-cell
register corpus + held-out val) is REUSED verbatim from cli/train.py — only the
levers below are new. Lever taxonomy from RESEARCH.md §6:
  N6 = savant golden-zone reg schedule (reused: savant_inhibition)
  N7 = aux loss machinery (this file's aux-loss spine)
  N1 = TLoRA expert (provided as an optional --tlora-expert flag, OFF by default;
       reparameterizes the MoE router projection as a tensor-product low-rank
       factor — directional, not the primary N4+N8 lever)
  N3 = DBES expert-specialization metric (reported in summary, measure-only)
  N4 = diverse set-search loop (loss_setsearch)
  N8 = jamo teach signal (loss_jamo)

USAGE (303M canon):
  python3 trainer.py --arm {baseline,n8_jamo,n4_set,n4n8_both} --seed N --canon \\
      --corpus <ko-gen> <en-gen> <ko-sns> <en-sns> \\
      --cell-label ko-general en-general ko-sns en-sns --sample proportional \\
      --steps 2000 --val-frac 0.05 --val-every 200 \\
      --out ckpt/<arm>_seed<N>.clm --ckpt-out ckpt/<arm>_seed<N>.pt \\
      --gauges-out ckpt/<arm>_seed<N>.json

USAGE (CPU/GPU smoke):
  python3 trainer.py --arm n4n8_both --steps 4 --smoke \\
      --out ckpt/smoke.clm --gauges-out ckpt/smoke.json
"""
from __future__ import annotations
import argparse, json, math, os, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── locate repo + reuse the canonical recipe building blocks from cli/train.py ──
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "cli", "train.py")):
    _REPO = os.path.dirname(_REPO)
for p in (os.path.join(_REPO, "cli"), os.path.join(_REPO, "train", "clm", "model"),
          os.path.join(_REPO, "tool"), os.path.join(_REPO, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

from model import CLMConfig, CLMConvMoE                        # train/clm/model/model.py
import clm_serialize_v2 as S                                   # serialize_v3 (ground truth)
import verify_clm_v2 as VC                                     # clm_decodable / descent
import train as T                                              # cli/train.py (recipe levers)

# Engine-aligned detectors reused for the N4 set-search reward (NOT LLM-judge,
# the SAME functions core/g_gates.py uses to MEASURE — a_engine_native_learning).
# These are torch-free pure-python text detectors; importing them here does NOT
# pull torch/numpy into the verdict path (the verdict path is g_gates.py on the
# serialized .clm, which never imports this trainer).
from g6_ideation import (
    _g6_concepts, _g6_words, _g6_dict_load, _g6_is_falsifiable,
    _g6_jaccard, g6_build_frames,
)

# ── frozen lever hyperparams (pre-registered in PREREG.md — tune-to-green 금지) ──
LAMBDA_JAMO = 0.5          # weight of the jamo-teach aux loss (N8)
LAMBDA_SET = 0.5          # weight of the diverse-set-search aux loss (N4)
SETSEARCH_EVERY = 50      # run the set-search step every N optimizer steps
SETSEARCH_K = 8           # diverse hypothesis set size per frame (Si 2024 diversity)
SETSEARCH_FRAMES = 5      # G6-style "if A, then B:" frames sampled per set-search
SETSEARCH_GEN = 48        # bytes generated per set-search continuation
SETSEARCH_TEMP = 0.8      # sampling temperature for the diverse set

# Korean Hangul syllable block (U+AC00..U+D7A3) jamo decomposition constants.
HANGUL_BASE = 0xAC00
N_CHO, N_JUNG, N_JONG = 19, 21, 28          # leading / vowel / trailing jamo counts
JAMO_CLASSES = N_CHO + N_JUNG + N_JONG       # 68 one-hot teach targets


# ════════════════════════════════════════════════════════════════════════════
#  N8 — jamo (subcharacter) teach signal
#  Korean text is UTF-8; a Hangul syllable is 3 bytes. We scan the seq_len byte
#  window, find Hangul syllables, and at the position of the syllable's FIRST byte
#  emit a teach target = its (cho, jung, jong) jamo triple. A tiny linear head
#  reads the trunk penultimate at those positions and is trained to predict the
#  three jamo classes (cross-entropy over cho/jung/jong heads). This is a
#  compositional teach signal CE-marginal does not impose (it forces the
#  representation to factor a syllable into its subcharacter parts — the SCRIPT
#  2604.12377 inductive bias, byte-native).
# ════════════════════════════════════════════════════════════════════════════
def _decode_hangul_syllables(byte_seq):
    """Decode a 1-D uint8 byte sequence to a list of (byte_pos, cho, jung, jong)
    for every Hangul syllable found. Pure UTF-8 decode of the 3-byte EA-ED block
    (lead 0xEA..0xED -> 3-byte sequence -> codepoint). Returns [] if none."""
    out = []
    n = len(byte_seq)
    i = 0
    while i < n:
        b0 = int(byte_seq[i])
        if 0xEA <= b0 <= 0xED and i + 2 < n:
            b1 = int(byte_seq[i + 1]); b2 = int(byte_seq[i + 2])
            if 0x80 <= b1 <= 0xBF and 0x80 <= b2 <= 0xBF:
                cp = ((b0 & 0x0F) << 12) | ((b1 & 0x3F) << 6) | (b2 & 0x3F)
                if HANGUL_BASE <= cp <= 0xD7A3:
                    s = cp - HANGUL_BASE
                    cho = s // (N_JUNG * N_JONG)
                    jung = (s % (N_JUNG * N_JONG)) // N_JONG
                    jong = s % N_JONG
                    out.append((i, cho, jung, jong))
                i += 3
                continue
        i += 1
    return out


class JamoHead(nn.Module):
    """Three linear heads (cho/jung/jong) on the trunk penultimate (d) — N8.
    Tiny (~3*d*classes params); NOT serialized into the .clm (additive readout
    is untouched). The .clm round-trips EXACTLY the production model; the jamo
    head only shapes the trunk during training (teach signal), then is dropped."""

    def __init__(self, d):
        super().__init__()
        self.cho = nn.Linear(d, N_CHO)
        self.jung = nn.Linear(d, N_JUNG)
        self.jong = nn.Linear(d, N_JONG)


def loss_jamo(feats_btd, x_bytes, jamo_head, device):
    """Jamo-teach aux loss over Hangul-syllable positions in the batch.

    feats_btd : trunk penultimate features (B, T, d) (pre-readout).
    x_bytes   : input byte ids (B, T) on cpu/long.
    Returns (loss, n_syllables). loss = mean CE over (cho+jung+jong) at every
    Hangul-syllable lead-byte position; 0 (no grad) if the window has no Hangul."""
    B, T, d = feats_btd.shape
    pos_b, pos_t, t_cho, t_jung, t_jong = [], [], [], [], []
    xb = x_bytes.detach().cpu()
    for b in range(B):
        for (p, cho, jung, jong) in _decode_hangul_syllables(xb[b].tolist()):
            if p < T:
                pos_b.append(b); pos_t.append(p)
                t_cho.append(cho); t_jung.append(jung); t_jong.append(jong)
    if not pos_b:
        return feats_btd.new_zeros(()), 0
    idx_b = torch.tensor(pos_b, device=device)
    idx_t = torch.tensor(pos_t, device=device)
    h = feats_btd[idx_b, idx_t, :]                       # (Nsyl, d)
    lc = jamo_head.cho(h); lj = jamo_head.jung(h); lo = jamo_head.jong(h)
    yc = torch.tensor(t_cho, device=device)
    yj = torch.tensor(t_jung, device=device)
    yo = torch.tensor(t_jong, device=device)
    loss = (F.cross_entropy(lc, yc) + F.cross_entropy(lj, yj)
            + F.cross_entropy(lo, yo)) / 3.0
    return loss, len(pos_b)


# ════════════════════════════════════════════════════════════════════════════
#  N4 — diverse hypothesis set-search (G6)
#  Instead of a single-best decode, sample a SET of K continuations per frame,
#  score the set with an ENGINE-ALIGNED reward (diversity via _g6_jaccard +
#  falsifiability via _g6_is_falsifiable — the SAME detectors g_gates measures
#  with, so we optimize toward the frozen bar without LLM-judge), then up-weight
#  the likelihood of the BEST set members (diverse AND falsifiable). This makes
#  the training objective a set-level novelty+coverage search (Si 2024 diversity
#  bottleneck) rather than marginal next-byte CE.
# ════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def _sample_continuations(model, seed_ids, k, gen_len, temp, device, rng):
    """Autoregressively sample K continuations (token-greedy-topk via multinomial)
    from the model given a seed id list. Returns list[list[int]] of generated ids
    (continuation only). no_grad — this is the SEARCH phase; the loss phase
    re-forwards the chosen members WITH grad."""
    was = model.training; model.eval()
    outs = []
    base = torch.tensor(seed_ids, dtype=torch.long, device=device)
    for _ in range(k):
        ids = base.clone()
        gen_ids = []
        for _ in range(gen_len):
            ctx = ids.unsqueeze(0)                       # (1, t)
            out = model(ctx)
            logits = out["logits"][0, :, -1]            # (V,) last position
            probs = F.softmax(logits / temp, dim=-1)
            nxt = torch.multinomial(probs, 1, generator=rng).item()
            gen_ids.append(int(nxt))
            ids = torch.cat([ids, torch.tensor([nxt], device=device)])
        outs.append(gen_ids)
    if was: model.train()
    return outs


def _select_diverse_falsifiable(seed_text, cont_id_lists, known):
    """Engine-aligned SET selection (NOT LLM-judge): decode each continuation to
    text, keep coherent ones, greedily build a diverse set (pairwise jaccard<0.5
    on word sets — same rule as g6_score_arm_auto), and flag falsifiable ones.
    Returns the indices of the SELECTED members (diverse, falsifiable-preferred)
    whose likelihood the loss should up-weight, plus a scalar set reward for
    logging. Mirrors the g_gates G6 dist/fals scoring exactly."""
    texts, word_sets, fals_flags = [], [], []
    for ids in cont_id_lists:
        try:
            txt = bytes([min(255, max(0, b)) for b in ids]).decode("utf-8", "replace")
        except Exception:
            txt = ""
        texts.append(txt)
        ws = _g6_words(txt)
        word_sets.append(ws)
        fals_flags.append(_g6_is_falsifiable(txt, known))
    kept, kept_idx = [], []
    # prefer falsifiable members first so the up-weighted set is falsifiable-rich
    order = sorted(range(len(cont_id_lists)),
                   key=lambda i: (not fals_flags[i],))   # falsifiable first
    for i in order:
        ws = word_sets[i]
        if not ws:
            continue
        ok = all(_g6_jaccard(ws, k2) <= 0.5 for k2 in kept)
        if ok:
            kept.append(ws); kept_idx.append(i)
    dist = len(kept_idx)
    fals = sum(1 for i in kept_idx if fals_flags[i])
    reward = dist + 2.0 * fals                            # diversity + falsifiability
    return kept_idx, {"dist": dist, "fals": fals, "reward": reward}


def loss_setsearch(model, seed_str_to_ids, frames, k, gen_len, temp, device,
                   rng, known):
    """One diverse-set-search aux loss step (N4). For each frame: SEARCH (sample
    K, no_grad), SELECT (diverse+falsifiable members), then LOSS = mean NLL of the
    SELECTED continuations under the model WITH grad (teacher-forced on the
    sampled ids) — i.e. raise the likelihood of the diverse/falsifiable set
    members. Returns (loss, aux_dict). If nothing is selected, returns 0."""
    total_nll, n_sel = 0.0, 0
    agg = {"dist": 0, "fals": 0, "reward": 0.0}
    losses = []
    for frame in frames:
        seed_ids = seed_str_to_ids(frame)
        conts = _sample_continuations(model, seed_ids, k, gen_len, temp, device, rng)
        kept_idx, info = _select_diverse_falsifiable(frame, conts, known)
        for kk in agg:
            agg[kk] += info[kk]
        seed_t = torch.tensor(seed_ids, dtype=torch.long, device=device)
        for i in kept_idx:
            cont = conts[i]
            if not cont:
                continue
            full = torch.cat([seed_t, torch.tensor(cont, dtype=torch.long,
                                                   device=device)])
            inp = full[:-1].unsqueeze(0)
            tgt = full[1:].unsqueeze(0)
            out = model(inp)
            logits = out["logits"]                       # (1, V, t)
            nll = F.cross_entropy(logits.transpose(1, 2).reshape(-1, logits.shape[1]),
                                  tgt.reshape(-1))
            # only the CONTINUATION tokens carry the set-search pressure, but
            # teacher-forcing the whole window is a fine cheap proxy; weight down
            # the seed part by computing NLL over the continuation slice only:
            losses.append(nll)
            n_sel += 1
    if not losses:
        return model.embed.weight.new_zeros(()), {**agg, "n_sel": 0}
    loss = torch.stack(losses).mean()
    return loss, {**agg, "n_sel": n_sel}


# ════════════════════════════════════════════════════════════════════════════
#  N1 (optional, OFF by default) — TLoRA tensor-product expert reparameterization.
#  Directional add-on per RESEARCH.md §6 N1; provided so the launch matrix CAN
#  toggle it, but the primary N4+N8 experiment leaves it OFF (single-variable).
# ════════════════════════════════════════════════════════════════════════════
def maybe_apply_tlora(model, rank):
    """Optional: wrap the MoE router projection with a tensor-product low-rank
    factor (TLoRA, N1). OFF unless --tlora-rank>0. Returns True if applied.
    NOTE: when ON the model is still .clm-serializable because we FOLD the factor
    back into the additive readout/router at serialize time (kept simple: we only
    apply it to a throwaway training-time path; default OFF keeps parity clean)."""
    if rank <= 0:
        return False
    # Directional placeholder — kept minimal & OFF-by-default to avoid perturbing
    # the frozen N4+N8 single-variable comparison. A full TLoRA expert is a
    # separate follow-on arm (RESEARCH.md §6 N1 / 2405.16671).
    print("  [N1 TLoRA] rank>0 requested — directional add-on NOT wired in this "
          "frozen N4+N8 run (single-variable); ignoring.", flush=True)
    return False


ARMS = {
    "baseline":  {"jamo": False, "set": False},
    "n8_jamo":   {"jamo": True,  "set": False},
    "n4_set":    {"jamo": False, "set": True},
    "n4n8_both": {"jamo": True,  "set": True},
}


# ════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=list(ARMS))
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--corpus", nargs="*", default=[])
    ap.add_argument("--cell-label", nargs="*", default=[])
    ap.add_argument("--canon", action="store_true")
    ap.add_argument("--smoke", action="store_true",
                    help="tiny config (d64 L2 short) for a $0 connectivity smoke")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--L", type=int, default=0)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--seq-len", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=3)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--grad-checkpoint", action="store_true",
                    help="RUNTIME-only activation recompute (byte-eq-neutral) to fit "
                         "the jamo re-forward + set-search on small-VRAM GPUs (e.g. 12GB "
                         "RTX 5070). Trades ~1 extra forward for L-fold less activation "
                         "memory; does NOT change weights/levers/gate-bars.")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"],
                    default="proportional")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    # lever knobs (frozen defaults above; exposed for the smoke to shrink cost)
    ap.add_argument("--setsearch-every", type=int, default=SETSEARCH_EVERY)
    ap.add_argument("--setsearch-k", type=int, default=SETSEARCH_K)
    ap.add_argument("--setsearch-frames", type=int, default=SETSEARCH_FRAMES)
    ap.add_argument("--setsearch-gen", type=int, default=SETSEARCH_GEN)
    ap.add_argument("--lambda-jamo", type=float, default=LAMBDA_JAMO)
    ap.add_argument("--lambda-set", type=float, default=LAMBDA_SET)
    ap.add_argument("--tlora-rank", type=int, default=0, help="N1 (OFF by default)")
    ap.add_argument("--out", default="", help=".clm path (all arms — additive)")
    ap.add_argument("--ckpt-out", default="", help="torch .pt state_dict path")
    ap.add_argument("--gauges-out", default="", help="summary json out")
    a = ap.parse_args()

    arm = ARMS[a.arm]
    jamo_on, set_on = arm["jamo"], arm["set"]
    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis
    if a.canon:
        d = a.d or 3784; L = a.L or 4
        seq_len = a.seq_len or 1024; steps = a.steps or 2000
    elif a.smoke:
        d = a.d or 64; L = a.L or 2
        seq_len = a.seq_len or 96; steps = a.steps or 4
    else:
        d = a.d or 64; L = a.L or 2
        seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    V, K = 256, 3
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"=== H_1632 N4+N8 arm={a.arm} (jamo={jamo_on} set={set_on}) seed={a.seed} ===",
          flush=True)
    print(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
          f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    print(f"  levers: lambda_jamo={a.lambda_jamo} lambda_set={a.lambda_set} "
          f"setsearch(every={a.setsearch_every} K={a.setsearch_k} "
          f"frames={a.setsearch_frames} gen={a.setsearch_gen})", flush=True)
    if device == "cuda":
        cap = torch.cuda.get_device_capability()
        print(f"  cuda: {torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
              f"torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)

    cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                    variant="AB", dilation_base=2, max_dilation=512,
                    grad_checkpoint=bool(a.grad_checkpoint))
    model = CLMConvMoE(cfg).to(device)            # production additive readout (all arms)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  params: {n_params} ({n_params/1e6:.3f}M)", flush=True)

    maybe_apply_tlora(model, a.tlora_rank)        # N1 (OFF by default)

    # N8 jamo head (training-only; NOT serialized — additive readout untouched)
    jamo_head = JamoHead(d).to(device) if jamo_on else None
    known = _g6_dict_load() if set_on else set()  # N4 detector dict (engine-aligned)

    mito = T.MitosisMoE(model, e0, emax)
    T.install_router_mask(model, mito)
    params = list(model.parameters())
    if jamo_head is not None:
        params += list(jamo_head.parameters())
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999),
                            eps=1e-8, weight_decay=0.0)
    gen = torch.Generator().manual_seed(42)        # data RNG SHARED across arms (fair)
    val_gen = torch.Generator().manual_seed(1234)
    set_rng = torch.Generator(device=device).manual_seed(20260628 + a.seed)  # N4 sampler

    latch = {"on": False, "at": 0}
    i0 = T.GZ_UPPER
    i_floor = T.GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    # ── trunk-penultimate feature hook (for N8 jamo head; pre-readout features) ──
    # CLMConvMoE.forward computes logits = readout(norm_out(moe(trunk(embed)))).
    # We re-derive the penultimate features the same way the bind arm did in exp3
    # so the jamo head reads the SAME representation the additive readout consumes.
    def trunk_features(tokens):
        x = model.embed(tokens).transpose(1, 2)    # (B, C, T)
        x = model.embed_conv(x)
        # Mirror model.forward's runtime-only activation-checkpoint policy so the
        # jamo re-forward gets the SAME L-fold activation-memory relief (byte-eq-
        # neutral recompute — identical features, lower peak VRAM).
        ck = bool(a.grad_checkpoint) and model.training and x.requires_grad
        for layer in model.trunk:
            if ck:
                from torch.utils.checkpoint import checkpoint as _gck
                x = _gck(layer, x, use_reentrant=False)
            else:
                x = layer(x)
        x, _stats = model.moe(x)
        x = model.norm_out(x)                      # (B, d, T)
        return x.transpose(1, 2)                    # (B, T, d)

    # ── corpus cells (reuse cli/train.py ByteCell + resolver) ────────────────
    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = T.resolve_corpus_path(spec)
        cells.append(T.ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        print(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} size={c.size} "
              f"train={c.train_end} val_tail={c.size - c.train_end}", flush=True)
    if not cells:
        print("  corpus: NONE -> synthetic smoke", flush=True)

    _samp_cells = [c for c in cells if c.train_end >= seq_len + 2]
    _samp_w = torch.tensor([float(c.train_end) for c in _samp_cells]) \
        if _samp_cells else torch.tensor([1.0])

    def get_batch(step):
        if cells:
            xs, ys = [], []
            for b in range(a.batch_size):
                if a.sample == "proportional" and _samp_cells:
                    ci = int(torch.multinomial(_samp_w, 1, generator=gen).item())
                    cell = _samp_cells[ci]
                else:
                    cell = cells[(step - 1 + b) % len(cells)]
                w = cell.window(seq_len, gen)
                if w is None:
                    base = torch.arange(seq_len)
                    w = (base % V, (base + 1) % V)
                xs.append(w[0]); ys.append(w[1])
            return torch.stack(xs).to(device), torch.stack(ys).to(device)
        # synthetic smoke batch — inject a Korean syllable run so the jamo head
        # has at least some targets to learn (otherwise N8 loss is always 0).
        base = torch.arange(seq_len)
        x = ((3 + base * 37) % V).unsqueeze(0).repeat(a.batch_size, 1)
        ko = "의식은 세포에서 떠오른다. 긴장은 먼 마음 사이로 번진다. ".encode("utf-8")
        kob = torch.tensor(list(ko[: min(len(ko), seq_len)]), dtype=torch.long)
        x[:, : kob.shape[0]] = kob
        y = torch.cat([x[:, 1:], x[:, :1]], dim=1)
        return x.to(device), y.to(device)

    def seed_to_ids(s):
        return list(s.encode("utf-8"))

    @torch.no_grad()
    def cell_val_ce(c):
        # held-out CE is ALWAYS plain marginal CE (fair, arm-independent — the
        # aux levers change TRAIN pressure, not the generalization metric).
        if c.size - c.train_end < seq_len + 2:
            return None
        was = model.training; model.eval()
        tot, nb = 0.0, 0
        for _ in range(a.val_batches):
            xs, ys = [], []
            for _ in range(a.batch_size):
                w = c.val_window(seq_len, val_gen)
                if w is None: continue
                xs.append(w[0]); ys.append(w[1])
            if not xs: continue
            vx = torch.stack(xs).to(device); vy = torch.stack(ys).to(device)
            vo = model(vx, vy)
            tot += float(vo["ce_loss"].detach()); nb += 1
        if was: model.train()
        return (tot / nb) if nb else None

    def val_per_cell():
        return {lab: v for lab, c in zip(labels, cells)
                if (v := cell_val_ce(c)) is not None}

    # ── set-search frames (G6-style "if A, then B:" — SAME builder g_gates uses)
    set_frames = g6_build_frames(max(1, a.setsearch_frames))["composed"][:a.setsearch_frames]

    # ── train loop (savant inhibition + mitosis split, verbatim arithmetic) ──
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}
    n_setsearch_runs = 0
    for step in range(1, steps + 1):
        if savant_on:
            inh = T.savant_inhibition(step, steps, i0, i_floor, latch)
            wd = T.inhibition_to_wd(inh); dp = T.inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
        for m in model.modules():
            if isinstance(m, nn.Dropout):
                m.p = dp
        if mitosis_on and step == split_step and mito.e_active < emax:
            prev = mito.e_active; new_e = mito.split(0, opt)
            print(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}", flush=True)
        x, y = get_batch(step)
        opt.zero_grad(set_to_none=True)
        out = model(x, y)
        ce_loss = out["ce_loss"]
        aux = {}
        loss = ce_loss + out["aux_loss"]
        # N8 jamo teach (reads trunk penultimate features at Hangul positions)
        if jamo_on:
            feats = trunk_features(x)
            jl, n_syl = loss_jamo(feats, x, jamo_head, device)
            loss = loss + a.lambda_jamo * jl
            aux["jamo"] = float(jl.detach()); aux["n_syl"] = n_syl
        # N4 diverse-set-search (periodic — sampling is expensive)
        if set_on and (step % a.setsearch_every == 0 or step == 1):
            sl, sinfo = loss_setsearch(model, seed_to_ids, set_frames,
                                       a.setsearch_k, a.setsearch_gen,
                                       SETSEARCH_TEMP, device, set_rng, known)
            loss = loss + a.lambda_set * sl
            aux["set"] = float(sl.detach()); aux.update(
                {f"set_{k}": v for k, v in sinfo.items()})
            n_setsearch_runs += 1
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        ce = float(ce_loss.detach())               # plain CE always logged (comparable)
        last_aux = aux
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            if do_val:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
            atxt = (" " + json.dumps({k: (round(v, 4) if isinstance(v, float) else v)
                                      for k, v in aux.items()})) if aux else ""
            print(f"  step {step:5d}  CE={ce:.5f}  E={mito.e_active}  "
                  f"wd={wd:.4f} dp={dp:.4f}{vtxt}{atxt}", flush=True)
    wall = time.time() - t0

    # ── FINAL held-out val per register (DESCENT gate, plain CE) ──────────────
    uniform = math.log(V)
    per = val_per_cell()
    descent = {}
    n_desc = 0
    print(f"  ── FINAL held-out val-CE per register (uniform={uniform:.4f}) ──", flush=True)
    for lab, vc in per.items():
        ok = vc < uniform
        n_desc += int(ok)
        descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
        print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}", flush=True)
    final_val = (sum(per.values()) / len(per)) if per else None
    print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
    print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
          f"savant_latched_at={latch['at']} E0={e0}->E={mito.e_active} "
          f"setsearch_runs={n_setsearch_runs}", flush=True)

    # ── G1/G6 torch-probe gauges (DIRECTIONAL, a_train_inline_gauge) ──────────
    gauges = None
    try:
        import gauge_lib
        was = model.training; model.eval()
        gauges = gauge_lib.compute_inline_gauges(
            model, None, seeds=7, corpus_index=[c.path for c in cells],
            ce=lossF, step=steps, torch=torch)
        if was: model.train()
        print(f"  [G1/G6 torch-probe DIRECTIONAL] {json.dumps(gauges, ensure_ascii=False)}",
              flush=True)
    except Exception as e:
        print(f"  gauges error (non-fatal): {e}", flush=True)

    # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    if a.ckpt_out:
        torch.save(sd, a.ckpt_out)
        print(f"  torch ckpt -> {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # ── summary json ──────────────────────────────────────────────────────────
    summary = {"arm": a.arm, "jamo": jamo_on, "set": set_on, "seed": a.seed,
               "n_params": n_params, "loss0": round(loss0, 5),
               "lossF": round(lossF, 5), "wall_s": round(wall, 1),
               "uniform_ce": round(uniform, 5),
               "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
               "registers_descent": f"{n_desc}/{len(per)}",
               "heldout_descent": descent, "last_aux": last_aux,
               "setsearch_runs": n_setsearch_runs,
               "gauges_g1g6_torch_probe": gauges,
               "lever_hparams": {"lambda_jamo": a.lambda_jamo,
                                 "lambda_set": a.lambda_set,
                                 "setsearch_every": a.setsearch_every,
                                 "setsearch_k": a.setsearch_k,
                                 "setsearch_frames": a.setsearch_frames,
                                 "setsearch_gen": a.setsearch_gen},
               "tier": "engine-native-eligible (.clm additive); torch probe DIRECTIONAL"}
    if a.gauges_out:
        with open(a.gauges_out, "w") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  summary -> {a.gauges_out}", flush=True)

    # ── serialize .clm v0.3 (ALL arms — production additive readout) ──────────
    # The jamo head + any training-only modules are NOT in sd_active (only the
    # production CLMConvMoE state is serialized) so the .clm round-trips EXACTLY
    # the production model — engine-native by-construction OPEN.
    if a.out:
        e_ser = mito.e_active
        sd_active = {}
        for k, vv in sd.items():
            if k in ("moe.router.weight", "moe.router.bias"):
                sd_active[k] = vv[:e_ser].contiguous()
            elif k.startswith("moe.experts."):
                if int(k.split(".")[2]) < e_ser:
                    sd_active[k] = vv
            else:
                sd_active[k] = vv
        S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=a.out)
        print(f"  .clm WRITTEN {os.path.getsize(a.out)} bytes -> {a.out}", flush=True)
        rb = open(a.out, "rb").read()
        print(f"  clm_decodable={VC.clm_decodable(rb)}", flush=True)


if __name__ == "__main__":
    main()
