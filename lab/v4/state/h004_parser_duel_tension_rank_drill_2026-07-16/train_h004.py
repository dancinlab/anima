#!/usr/bin/env python3
"""H_004 G-2 training driver — parse-tension resolver + 5 arms (DESIGN_g2_training_fable5.md).

trunk = H_003 CLMConvMoE (d=384 L=4) on RAW UTF-8 (codec axis closed, H_003 🔴); a small resolver
R (32.5k params) ingests the per-item n×n tension field T by relative OFFSET bucket and injects a
per-node structure embedding PRE-trunk (nc5: R is an input of the same forward used at eval). The
five arms differ in EXACTLY ONE thing — the map `T_item → tensor handed to R`:
    A-duel  T            A-rank1  rank1_tiebreak(T)    C-plc  Π T Πᵀ
    C-scaf  0            C-perm   T (+ drill gold shuffled)

⚠️ RUN GATE: this driver's ~5h d=384 run is gated on native-operator G-1 + `pre_register_frozen`.
The `--smoke` d=64 path is $0 wiring verification only and needs no freeze.

Run:  python3 .../train_h004.py --smoke      # wiring (minutes)
      python3 .../train_h004.py               # full d=384 (ONLY after freeze)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANIMA = "/Users/mini/dancinlab/anima"
_NSMC = os.path.join(_ANIMA, "state", "nbind_curriculum", "ratings_train.txt")
sys.path.insert(0, _HERE)
sys.path.insert(0, _ANIMA)

import numpy as np
import g1_core_check as gc          # t_struct · concord_field · rank1_tiebreak · offtop · HEAD_A/HEAD_G
import build_tension as bt          # _heads() for K=6

ANS = ("앞", "뒤")
AP, TU = ANS[0].encode(), ANS[1].encode()      # 3 bytes each; differ at byte 0
assert len(AP) == len(TU) == 3 and AP[0] != TU[0]


# ---------------------------------------------------------------- tension per item
def _item_T(item):
    """(T ndarray (n,n), gold_flips list, n) for a multi (conjuncts) or single-bind item."""
    if "conjuncts" in item:                         # K=6 multi
        K = len(item["conjuncts"]); n = 3 * K + 2
        ha, hg = bt._heads()
        hon = np.zeros(n)
        gold = []
        for k, c in enumerate(item["conjuncts"]):
            hp = int(c["hp"]); pos1 = 1.0 if int(c["honored_position"]) == 1 else 0.0
            hon[3 * k] = hp; hon[3 * k + 1] = pos1; hon[3 * k + 2] = 1.0 - pos1
            gold.append(int(c["gold_flip"]))
        T = gc.concord_field(gc.t_struct(n, ha, hg), hon)
        return T, gold, n
    # single-bind f1' (K=1, n=5)
    n = 5
    hon = np.array([item["honorific_present"],
                    1.0 if item["n1_lexeme"].endswith("님") else 0.0,
                    1.0 if item["n2_lexeme"].endswith("님") else 0.0, 0.0, 0.0])
    T = gc.concord_field(gc.t_struct(n, gc.HEAD_A, gc.HEAD_G), hon)
    return T, [int(item["gold_flip"])], n


def _arm_tensor(T, arm, set_id, idx):
    if arm in ("A-duel", "C-perm"):
        return T
    if arm == "A-rank1":
        return gc.rank1_tiebreak(T)
    if arm == "C-scaf":
        return np.zeros_like(T)
    if arm == "C-plc":
        n = T.shape[0]
        perm = np.random.default_rng(9000 + 1000 * set_id + idx).permutation(n)
        return T[np.ix_(perm, perm)]
    raise ValueError(arm)


# ---------------------------------------------------------------- byte↔node alignment
def _node_of_byte(surface, n):
    """Map each byte index of surface.encode() (+ answer region) to its node id (0..n-1)."""
    eojeols = surface.split(" ")
    # surface = "e0 e1 ... e_{n-2} " ends with '=> ' → split gives n tokens + trailing '' (from final space)
    toks = [t for t in eojeols if t != ""]
    assert len(toks) == n, (len(toks), n, surface)
    b = surface.encode("utf-8")
    node = np.full(len(b), n - 1, dtype=np.int64)     # default → ANS node (answer region maps here too)
    pos = 0
    for i, tok in enumerate(toks):
        piece = (tok + " ").encode("utf-8")           # each eojeol owns its trailing space
        node[pos:pos + len(piece)] = i
        pos += len(piece)
    return node                                        # length == len(surface bytes); answer bytes handled by caller


# ---------------------------------------------------------------- model (subclass)
def _load(smoke):
    import torch
    import core.model as M
    d, L, E = (64, 2, 2) if smoke else (384, 4, 3)
    cfg = M.CLMConfig(vocab_size=256, d_model=d, n_trunk_layers=L, n_experts=E)

    class CLMConvMoEStruct(M.CLMConvMoE):
        def __init__(self, cfg):
            super().__init__(cfg)
            self.r_out = torch.nn.Embedding(19, 32)
            self.r_in = torch.nn.Embedding(19, 32)
            self.rmlp = torch.nn.Sequential(torch.nn.Linear(32, 64), torch.nn.GELU(),
                                            torch.nn.Linear(64, 64))
            self.rproj = torch.nn.Linear(64, cfg.d_model)

        def node_embed(self, T):                       # T: (n,n) tensor → (n,64)
            dev = self.r_out.weight.device             # move input to the module's device (MPS/CPU)
            if T.device != dev:                        # else CPU tensor + MPS params → "Placeholder
                T = T.to(dev)                          # storage not allocated on MPS" (train-h004-py-2)
            n = T.shape[0]
            delta = (torch.arange(n, device=dev)[None, :] - torch.arange(n, device=dev)[:, None])
            b = (delta.clamp(-9, 9) + 9)
            h = (T.unsqueeze(-1) * self.r_out(b)).sum(1) + (T.t().unsqueeze(-1) * self.r_in(b)).sum(1)
            return self.rmlp(h)                         # (n,64)

        def forward(self, tokens, targets=None, struct=None):
            import torch.nn.functional as F
            x = self.embed(tokens)                      # (B,T,C)
            if struct is not None:
                x = x + self.rproj(struct)              # THE injection (pre-trunk)
            x = x.transpose(1, 2)
            x = self.embed_conv(x)
            for layer in self.trunk:
                x = layer(x)
            x, stats = self.moe(x)
            x = self.norm_out(x)
            logits = self.readout(x)                    # (B,V,T)
            out = {"logits": logits, "aux_loss": stats.aux_loss}
            if targets is not None:
                ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                                     targets.reshape(-1))
                out["loss"] = ce + stats.aux_loss
                out["ce_loss"] = ce
            return out

    return torch, M, cfg, CLMConvMoEStruct


# ---------------------------------------------------------------- struct tensor for an item
def _node_layout(surf, n, gold, seq_bytes_len):
    """(seq_bytes_len,) node id per byte. Answer byte k → its conjunct-k node (3k) at the PREDICTION
    position (base+3k-1) + the 3 answer bytes, so the answer reads its slot's resolved structure
    directly (train-h004-py-1: the off-by-one lesson)."""
    nob = _node_of_byte(surf, n)
    full = np.full(seq_bytes_len, n - 1, dtype=np.int64)            # default → ANS node
    full[:len(nob)] = nob
    base = len(surf.encode("utf-8"))
    K = len(gold)
    node_k = (lambda k: 3 * k) if K > 1 else (lambda k: 0)
    for k in range(K):
        full[max(base + 3 * k - 1, 0): base + 3 * k + 3] = node_k(k)
    return full


def _struct_for(model, torch, item, arm, set_id, idx, seq_bytes_len, override_T=None):
    """(seq_bytes_len, 64) struct rows: node_embed(arm_tensor(T)) scattered by _node_layout."""
    T, gold, n = _item_T(item)
    Ta = override_T if override_T is not None else _arm_tensor(T, arm, set_id, idx)
    emb = model.node_embed(torch.tensor(Ta, dtype=torch.float32))    # (n,64)
    full = _node_layout(item["surface"], n, gold, seq_bytes_len)
    struct = emb[torch.tensor(full)]                                # (seq_bytes_len, 64)
    return struct, gold, T


# ---------------------------------------------------------------- forced-choice d_acc
def _seq_bytes(item):
    return item["surface"].encode("utf-8"), item["gold_pattern"].encode("utf-8") if "gold_pattern" in item \
        else item["gold_token"].encode("utf-8")


def _panel_free_slots(panel):
    """Slots whose gold bit is NOT prefix-determined by earlier slots — the only slots that require
    the tension FIELD to answer. d_acc must score ONLY these. The K=6 gold codebook is a GF(2)
    rank-4 linear code (slot3=s0⊕s1⊕s2, slot5=s1⊕s2⊕s4); since `_dacc_item` teacher-forces the true
    prefix when scoring slot k, ANY answer-LM (incl. the shuffled-gold C-perm harness) completes the
    two parity slots {3,5} for free → a field-BLIND ceiling of 0.667, not 0.5, that reaches held-out
    (Fable adjudication btgczi488 · confirmed on both drill + f2″). Scoring the free slots {0,1,2,4}
    restores a 0.5 floor. Computed from the codebook so it can never silently drift."""
    import itertools
    pats = sorted({it["gold_pattern"] for it in panel if "gold_pattern" in it})
    if not pats:
        return [0]                                                  # single-bind panel (K=1)
    M = [[0 if c == "앞" else 1 for c in p] for p in pats]
    K = len(M[0])
    def col_xor(cols):
        x = [0] * len(M)
        for j in cols:
            x = [a ^ M[i][j] for i, a in enumerate(x)]
        return x
    free = []
    for k in range(K):
        det = any(col_xor(list(sub)) == [row[k] for row in M]
                  for r in range(1, k + 1) for sub in itertools.combinations(range(k), r))
        if not det:
            free.append(k)
    return free


def _dacc_item(model, torch, item, arm, set_id, idx, device, free_slots=None):
    surf_b, gold_b = _seq_bytes(item)
    base = len(surf_b)
    K = len(gold_b) // 3
    seq = surf_b + gold_b
    struct, gold, _ = _struct_for(model, torch, item, arm, set_id, idx, len(seq))
    struct = struct.to(device)
    slots = range(K) if free_slots is None else free_slots

    def _nll_slots(byte_seq):
        toks = torch.tensor(list(byte_seq), dtype=torch.long, device=device)[None]
        with torch.no_grad():
            out = model(toks, struct=struct[None])
        logp = torch.log_softmax(out["logits"][0], dim=0)           # (V,T)
        nll = []
        for k in range(K):
            s = base + 3 * k
            tot = 0.0
            for j in range(3):                                      # 3 bytes of the candidate
                tot += -logp[byte_seq[s + j], s + j - 1].item()     # predict byte at pos p from p-1
            nll.append(tot)
        return nll
    nll_gold = _nll_slots(seq)
    correct = 0
    for k in slots:
        s = base + 3 * k
        flip = ANS[1 - gold[k]].encode("utf-8")
        alt = bytearray(seq); alt[s:s + 3] = flip
        nll_alt_k = _nll_slots(bytes(alt))[k]
        if nll_gold[k] <= nll_alt_k:
            correct += 1
    return correct / len(list(slots))


def dacc_panel(model, torch, panel, arm, set_id, device, free_only=True):
    """d_acc averaged over items. free_only=True (default) scores ONLY the field-carried free slots
    {0,1,2,4} — the frozen metric re-registration after the parity-ceiling defect (see _panel_free_slots)."""
    fs = _panel_free_slots(panel) if free_only else None
    return float(np.mean([_dacc_item(model, torch, panel[i], arm, set_id, i, device, free_slots=fs)
                          for i in range(len(panel))]))


def dacc_perslot(model, torch, panel, arm, set_id, device):
    """Per-slot mean d_acc on a K=6 panel (FM-2 signature: slot-0-high/others-0.5 for A-rank1)."""
    K = len(panel[0].get("gold_pattern", "앞")) if "gold_pattern" in panel[0] else 1
    acc = np.zeros(K)
    for i, it in enumerate(panel):
        surf_b, gold_b = _seq_bytes(it)
        base = len(surf_b); seq = surf_b + gold_b
        struct, gold, _ = _struct_for(model, torch, it, arm, set_id, i, len(seq))
        struct = struct.to(device)
        def _nll(byte_seq, k):
            toks = torch.tensor(list(byte_seq), dtype=torch.long, device=device)[None]
            with torch.no_grad():
                logp = torch.log_softmax(model(toks, struct=struct[None])["logits"][0], dim=0)
            s = base + 3 * k
            return sum(-logp[byte_seq[s + j], s + j - 1].item() for j in range(3))
        for k in range(K):
            s = base + 3 * k
            alt = bytearray(seq); alt[s:s + 3] = ANS[1 - gold[k]].encode()
            acc[k] += 1 if _nll(seq, k) <= _nll(bytes(alt), k) else 0
    return (acc / len(panel)).round(4).tolist()


# ---------------------------------------------------------------- CPT (raw utf-8 concat)
def _nsmc_lines(n):
    if not os.path.exists(_NSMC):
        return ["영화 재미있다 좋다"] * n            # smoke fallback if corpus absent
    raw = open(_NSMC, encoding="utf-8").read().splitlines()[1:]
    return [l.split("\t")[1] for l in raw if len(l.split("\t")) > 2][:n]


def _cpt_windows(lines, seq_len, torch):
    stream = ("\n".join(lines)).encode("utf-8")
    arr = np.frombuffer(stream, dtype=np.uint8)
    nwin = len(arr) // seq_len
    return torch.tensor(arr[:nwin * seq_len].reshape(nwin, seq_len).astype(np.int64))


# ---------------------------------------------------------------- drill (per-item padded)
def _drill_batch(model, torch, items, arm, seed, device, pad):
    """One padded batch: (tokens, targets, struct, mask, amask) for masked external CE.

    `mask`  = all predict-next positions (surface + answer).
    `amask` = ONLY the positions that predict the 3·K answer bytes (base-1 .. base+3K-2 = the
    PREDICT positions, per the off-by-one lesson train-h004-py-1). ⊆ mask. Lets the drill loop
    up-weight the 18 decisive bytes so the binding CE is not diluted by ~215 surface bytes
    (root cause of the run-1 precond failure: drill CE converged to 6·ln2/L ≈ chance-on-binding).
    """
    B = len(items)
    tok = np.zeros((B, pad), np.int64); tgt = np.zeros((B, pad), np.int64)
    mask = np.zeros((B, pad), np.float32); amask = np.zeros((B, pad), np.float32)
    struct = torch.zeros(B, pad, 64, device=device)
    for bi, (idx, item) in enumerate(items):
        surf_b, gold_b = _seq_bytes(item)
        seq = (surf_b + gold_b)[:pad]
        st, gold, _ = _struct_for(model, torch, item, arm, 0, idx, len(seq))
        L = len(seq)
        tok[bi, :L] = list(seq)
        tgt[bi, :L - 1] = list(seq[1:])
        mask[bi, :L - 1] = 1.0                            # predict-next positions
        base = len(surf_b); K = len(gold_b) // 3          # answer = 3·K bytes appended after surface
        a0 = max(base - 1, 0); a1 = min(base + 3 * K - 1, L - 1)   # predict-positions of answer bytes
        if a1 > a0:
            amask[bi, a0:a1] = 1.0
        struct[bi, :st.shape[0]] = st.to(device)
    return (torch.tensor(tok, device=device), torch.tensor(tgt, device=device), struct,
            torch.tensor(mask, device=device), torch.tensor(amask, device=device))


# drill objective constants (arm-BLIND — applied identically to all 5 arms; the only across-arm
# difference stays the T-policy in _arm_tensor · quarantine amendment to run-1's diluted objective)
LAMBDA_ANS = 5.0                     # up-weight the 18 answer bytes: 1/L → 5/18 ≈ ×65 per-position
_BASE_LR, _MIN_LR, _WARMUP = 3e-4, 1e-5, 100


def _drill_lr(step, drill_steps):
    warm = min((step + 1) / _WARMUP, 1.0)
    cos = _MIN_LR / _BASE_LR + (1 - _MIN_LR / _BASE_LR) * 0.5 * (1 + math.cos(math.pi * step / drill_steps))
    return _BASE_LR * warm * cos


def train_arm(arm, seed, cfg_tuple, panels, drill, cpt_win, steps, device, tag=None):
    torch, M, cfg, Struct = cfg_tuple
    torch.manual_seed(seed)
    model = Struct(cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=_BASE_LR)
    import torch.nn.functional as F
    logf = os.path.join(_HERE, f"train_log_{tag}.jsonl") if tag else None

    def _log(rec):
        if logf:
            with open(logf, "a") as fh:
                fh.write(json.dumps({"arm": arm, "seed": seed, **rec}, ensure_ascii=False) + "\n")

    # CPT (struct=None, identical for all arms)
    cpt_steps, drill_steps = steps
    bs = 8 if device == "cpu" else 16
    for step in range(cpt_steps):
        idx = torch.randint(0, cpt_win.shape[0], (bs,))
        w = cpt_win[idx].to(device)
        out = model(w[:, :-1], targets=w[:, 1:])
        opt.zero_grad(); out["loss"].backward(); opt.step()
        if logf and (step % 500 == 0 or step == cpt_steps - 1):
            _log({"phase": "cpt", "step": step, "ce": round(float(out["loss"].item()), 4)})
    # drill (per-item padded, external masked CE; per-arm struct)
    d_items = list(enumerate(drill))
    drill_gold = [it["gold_pattern"] for _, it in d_items]
    if arm == "C-perm":
        perm = list(range(len(d_items)))
        random.Random(seed).shuffle(perm)
        # keep item i's surface/conjuncts (⇒ real T), swap in a shuffled gold_pattern target:
        # A-duel trained on permuted gold ⇒ no consistent field→answer signal ⇒ f2″ ≈ 0.5 (harness)
        d_items = [(idx, {**it, "gold_pattern": drill_gold[perm[i]]})
                   for i, (idx, it) in enumerate(d_items)]
    pad = 256 if cfg.d_model == 64 else 320    # must fit the longest K=6 drill item (~250 bytes)
    ce_ans = torch.tensor(0.0)
    for step in range(drill_steps):
        bi = torch.randint(0, len(d_items), (min(bs, len(d_items)),))
        batch = [d_items[i] for i in bi.tolist()]
        tok, tgt, struct, mask, amask = _drill_batch(model, torch, batch, arm, seed, device, pad)
        out = model(tok, struct=struct)
        logits = out["logits"]                                       # (B,V,T)
        ce_tok = F.cross_entropy(logits[:, :, :-1].transpose(1, 2).reshape(-1, cfg.vocab_size),
                                 tgt[:, :-1].reshape(-1), reduction="none")
        m = mask[:, :-1].reshape(-1); am = amask[:, :-1].reshape(-1); sm = m - am
        ce_surf = (ce_tok * sm).sum() / sm.sum().clamp(min=1)        # ~215 surface bytes, weight 1
        ce_ans = (ce_tok * am).sum() / am.sum().clamp(min=1)         # 18 answer bytes, weight LAMBDA
        loss = ce_surf + LAMBDA_ANS * ce_ans + out["aux_loss"]
        lr = _drill_lr(step, drill_steps)                            # 100-step warmup + cosine → 1e-5
        for g in opt.param_groups:
            g["lr"] = lr
        opt.zero_grad(); loss.backward()
        gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)   # drill-only insurance
        opt.step()
        if logf and (step % 50 == 0 or step == drill_steps - 1):
            _log({"phase": "drill", "step": step, "lr": round(lr, 7),
                  "ce_surf": round(float(ce_surf.item()), 4), "ce_ans": round(float(ce_ans.item()), 4),
                  "aux": round(float(out["aux_loss"].item()), 5), "grad_norm": round(float(gnorm), 3)})
        if logf and (step % 500 == 0 or step == drill_steps - 1):
            model.eval()
            _log({"phase": "drill_eval", "step": step,
                  "drill_dacc32": round(dacc_panel(model, torch, drill[:32], arm, 0, device), 4),
                  "per_slot": dacc_perslot(model, torch, drill[:32], arm, 0, device)})
            model.train()
    model.eval()
    return model, float(ce_ans.item())     # drill_ce_final now = the binding (answer) CE, the true metric


# ---------------------------------------------------------------- smoke wiring checks
def smoke(device="cpu"):
    torch, M, cfg, Struct = _load(smoke=True)
    f2 = json.load(open(os.path.join(_HERE, "panel_f2doubleprime.json"), encoding="utf-8"))
    f1 = json.load(open(os.path.join(_HERE, "panel_f1prime.json"), encoding="utf-8"))
    drill = json.load(open(os.path.join(_HERE, "drill_grid_multi.json"), encoding="utf-8"))
    print("=" * 70); print("H_004 G-2 driver — SMOKE (wiring only, $0)"); print("=" * 70)

    # WIRING-1 alignment
    for name, panel, K in [("f2''", f2, 6), ("drill", drill, 6), ("f1'", f1, 1)]:
        it = panel[0]
        n = 3 * K + 2
        toks = [t for t in it["surface"].split(" ") if t != ""]
        assert len(toks) == n, (name, len(toks), n)
        if "conjuncts" in it:
            for k, c in enumerate(it["conjuncts"]):
                assert " ".join(toks[3 * k:3 * k + 3]) == c["surface"], (name, k)
        print(f"  WIRING-1 {name}: {len(toks)} eojeols == {n} nodes ✓")

    # WIRING-2 slots
    assert len(AP) == len(TU) == 3
    it = f2[0]; base = len(it["surface"].encode()); gp = it["gold_pattern"].encode()
    for k in range(6):
        assert gp[3 * k:3 * k + 3] in (AP, TU)
    print("  WIRING-2 slots: 앞/뒤 = 3 bytes, tile gold_pattern ✓")

    torch.manual_seed(0)
    model = Struct(cfg).to(device); model.eval()
    # untrained scorer in [0.3,0.7]
    dac = _dacc_item(model, torch, f2[0], "A-duel", 1, 0, device)
    print(f"  WIRING-2 untrained d_acc(item)= {round(dac,3)} (expect ~0.5)")

    # WIRING-3 injection liveness: flip T[0,1] sign moves A-duel logits, not C-scaf, not CPT
    it = f2[0]; surf_b, gold_b = _seq_bytes(it); seq = surf_b + gold_b
    st, gold, T = _struct_for(model, torch, it, "A-duel", 1, 0, len(seq))
    Tf = T.copy(); Tf[0, 1] = -Tf[0, 1]
    emb0 = model.node_embed(torch.tensor(T, dtype=torch.float32))
    emb1 = model.node_embed(torch.tensor(Tf, dtype=torch.float32))
    dmax = float((emb0 - emb1).abs().max())
    st_scaf, _, _ = _struct_for(model, torch, it, "C-scaf", 0, 0, len(seq))
    sc = st_scaf.detach().numpy()
    scaf_const = bool(np.allclose(sc, sc[0]))       # C-scaf = node_embed(0) = mlp(0): a CONSTANT (not zero)
    print(f"  WIRING-3 T[0,1] sign-flip moves node_embed by {round(dmax,4)} (>0 ✓) · "
          f"C-scaf struct constant across positions (=mlp(0), invariant to T): {scaf_const} ✓")

    # WIRING-5 harness: rank1_tiebreak nnz==2 on row 0; C-plc Π reproducible + conjugate
    r1 = gc.rank1_tiebreak(T)
    nz = np.argwhere(np.abs(r1) > 1e-9)
    row0 = all(r == 0 for r, _ in nz)
    print(f"  WIRING-5 rank1_tiebreak nnz={len(nz)} (expect 2), all on row 0: {row0} ✓")
    p1 = _arm_tensor(T, "C-plc", 1, 0); p2 = _arm_tensor(T, "C-plc", 1, 0)
    spec_ok = np.allclose(np.sort(np.linalg.svd(p1, compute_uv=False)),
                          np.sort(np.linalg.svd(T, compute_uv=False)), atol=1e-6)
    print(f"  WIRING-5 C-plc Π reproducible: {np.array_equal(p1,p2)} · spectrum preserved: {spec_ok} ✓")

    # WIRING-4 injection-path liveness: A-duel must overfit 16 drill items to ~1.0 (the field is
    # injected at the answer-prediction position ⇒ the model can read the sign bits). This is the
    # H_003-windower analog — if A-duel CANNOT overfit, the struct↔prediction-position alignment or
    # the slot indexing is broken. (C-scaf/A-rank1 overfit ~0.75 by MEMORIZING 16 surfaces; that is
    # NOT the field-necessity test — F3 on held-out f2″ is. So WIRING-4 gates A-duel only.)
    print("  WIRING-4 overfit A-duel on 16 drill items × 600 steps (d=64)…")
    model2, ce = train_arm("A-duel", 0, (torch, M, cfg, Struct), {"f2": f2, "f1": f1},
                           drill[:16], _cpt_windows(_nsmc_lines(1500), 128, torch),
                           (30, 600), device)
    dac_drill = float(np.mean([_dacc_item(model2, torch, drill[i], "A-duel", 0, i, device)
                               for i in range(16)]))
    print(f"  WIRING-4 A-duel drill-subset d_acc = {round(dac_drill,3)} (target ≥ 0.9; drill CE {round(ce,3)})")
    ok = (dmax > 0 and scaf_const and row0 and spec_ok and 0.2 <= dac <= 0.8 and dac_drill >= 0.9)
    print("\nSMOKE:", "wiring GREEN — alignment · injection-path (A-duel overfits) · slots · arm-tensors verified"
          if ok else "wiring RED — inspect above (esp. WIRING-4: injection/slot-alignment bug, H_003-windower class)")
    return 0 if ok else 1


ARMS = ["A-duel", "A-rank1", "C-plc", "C-scaf", "C-perm"]


def _f4_offtop(model, torch, f2, device):
    """F4 (=L1): learned T-usage rank on trained A-duel. Per item: grad of Σ logp(gold answer bytes)
    w.r.t. T; offtop(grad) mean < 0.20 ⇒ R reads ≤ a rank-1 shadow ⇒ DEAD."""
    offs = []
    for i, it in enumerate(f2):
        T, gold, n = _item_T(it)
        Tt = torch.tensor(T, dtype=torch.float32, device=device, requires_grad=True)
        emb = model.node_embed(Tt)                                   # (n,64) grad-enabled
        surf_b, gold_b = _seq_bytes(it); base = len(surf_b); seq = surf_b + gold_b
        full = _node_layout(it["surface"], n, gold, len(seq))
        struct = emb[torch.tensor(full, device=device)][None]        # (1,T,64)
        toks = torch.tensor(list(seq), dtype=torch.long, device=device)[None]
        logp = torch.log_softmax(model(toks, struct=struct)["logits"][0], dim=0)
        L = 0.0
        for k in range(len(gold)):
            s = base + 3 * k
            for j in range(3):
                L = L + logp[seq[s + j], s + j - 1]
        model.zero_grad(); L.backward()
        offs.append(gc.offtop(Tt.grad.detach().cpu().numpy()))
    return float(np.mean(offs))


def _f5_union(model, torch, f2, device):
    """F5 (=L2): inference-only substitution T → |t_struct| (both candidate edges +1, χ removed).
    ΔCE (answer bytes) and Δd_acc between the real field and the resolution-stripped skeleton."""
    ha, hg = bt._heads()
    ce_T, ce_U, dac_T, dac_U = [], [], 0, 0
    for i, it in enumerate(f2):
        T, gold, n = _item_T(it)
        union = np.abs(gc.t_struct(n, ha, hg))                       # unsigned skeleton, item-independent
        for tag, Ta in (("T", None), ("U", union)):
            surf_b, gold_b = _seq_bytes(it); base = len(surf_b); seq = surf_b + gold_b
            struct, g, _ = _struct_for(model, torch, it, "A-duel", 1, i, len(seq), override_T=Ta)
            toks = torch.tensor(list(seq), dtype=torch.long, device=device)[None]
            with torch.no_grad():
                logp = torch.log_softmax(model(toks, struct=struct.to(device)[None])["logits"][0], dim=0)
            ce = 0.0; corr = 0
            for k in range(len(gold)):
                s = base + 3 * k
                ce += sum(-logp[seq[s + j], s + j - 1].item() for j in range(3))
                alt = bytearray(seq); alt[s:s + 3] = ANS[1 - gold[k]].encode()
                t2 = torch.tensor(list(bytes(alt)), dtype=torch.long, device=device)[None]
                with torch.no_grad():
                    lp2 = torch.log_softmax(model(t2, struct=struct.to(device)[None])["logits"][0], dim=0)
                nll_alt = sum(-lp2[alt[s + j], s + j - 1].item() for j in range(3))
                nll_gold = sum(-logp[seq[s + j], s + j - 1].item() for j in range(3))
                corr += 1 if nll_gold <= nll_alt else 0
            n_ans = 3 * len(gold)
            if tag == "T":
                ce_T.append(ce / n_ans); dac_T += corr / len(gold)
            else:
                ce_U.append(ce / n_ans); dac_U += corr / len(gold)
    return {"dCE": round(float(np.mean(ce_U)) - float(np.mean(ce_T)), 4),
            "d_dacc": round(dac_T / len(f2) - dac_U / len(f2), 4)}


def run_full(device, cpt_steps, drill_steps, tag, seeds=(0, 1)):
    torch, M, cfg, Struct = _load(smoke=(drill_steps < 500))    # check mode d=64, full d=384
    f2 = json.load(open(os.path.join(_HERE, "panel_f2doubleprime.json"), encoding="utf-8"))
    f1 = json.load(open(os.path.join(_HERE, "panel_f1prime.json"), encoding="utf-8"))
    drill = json.load(open(os.path.join(_HERE, "drill_grid_multi.json"), encoding="utf-8"))
    n_cpt = 2000 if tag == "check" else 120000
    cpt_win = _cpt_windows(_nsmc_lines(n_cpt), 128 if tag == "check" else 512, torch)
    results = {}
    for seed in seeds:
        for arm in ARMS:
            print(f"  training {arm}.s{seed} (CPT {cpt_steps} + drill {drill_steps}, d={cfg.d_model})…", flush=True)
            model, ce = train_arm(arm, seed, (torch, M, cfg, Struct), {"f2": f2, "f1": f1},
                                  drill, cpt_win, (cpt_steps, drill_steps), device, tag=tag)
            rec = {
                "f2doubleprime": round(dacc_panel(model, torch, f2, arm, 1, device), 4),
                "f2doubleprime_per_slot": dacc_perslot(model, torch, f2, arm, 1, device),
                "f1prime": round(dacc_panel(model, torch, f1, arm, 2, device), 4),
                "drill_dacc": round(dacc_panel(model, torch, drill[:64], arm, 0, device), 4),
                "drill_ce_final": round(ce, 4),
            }
            if arm == "A-duel":
                rec["F4_offtop"] = round(_f4_offtop(model, torch, f2, device), 4)
                rec["F5_union"] = _f5_union(model, torch, f2, device)
            results[f"{arm}.s{seed}"] = rec
            print(f"    {arm}.s{seed}: f2″={rec['f2doubleprime']} f1′={rec['f1prime']} "
                  f"drill={rec['drill_dacc']}", flush=True)
    out = {"config": {"d": cfg.d_model, "L": cfg.n_trunk_layers, "cpt_steps": cpt_steps,
                      "drill_steps": drill_steps, "tag": tag, "seeds": list(seeds)},
           "results": results}
    fn = "train_result_full.json" if tag == "full" else f"train_result_{tag}.json"
    with open(os.path.join(_HERE, fn), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"wrote {fn}")
    return 0


def fit_check(device):
    """$0-ish pre-flight (~10-15 min MPS): does the FIXED drill objective fit A-duel to ≥0.95?

    d=64/L=2 (the smoke config), CPT 200 + full 384-item drill 1500 steps, on the TARGET device
    (train-h004-py-2: exercise the MPS struct path, never CPU-only). Trains ONLY A-duel s0, A-duel s1,
    C-perm s0. Go-bar (ALL must pass, else DO NOT launch the ~3.8h full run):
      1. A-duel drill d_acc ≥ 0.95 both seeds AND seed-spread ≤ 0.03  (optimization, not capacity)
      2. A-duel ce_ans (binding CE) decays < 0.05 both seeds            (the new answer term trains)
      3. C-perm drill d_acc vs TRUE gold ≤ 0.60                         (boosted loss ≠ shuffled fit)
    If bar-1 fails at d=64, re-test d=128 before any conclusion (capacity confound at 64; none at 384).
    """
    torch, M, cfg, Struct = _load(smoke=True)                # d=64, L=2, E=2
    drill = json.load(open(os.path.join(_HERE, "drill_grid_multi.json"), encoding="utf-8"))
    f2 = json.load(open(os.path.join(_HERE, "panel_f2doubleprime.json"), encoding="utf-8"))
    f1 = json.load(open(os.path.join(_HERE, "panel_f1prime.json"), encoding="utf-8"))
    cpt_win = _cpt_windows(_nsmc_lines(2000), 128, torch)
    logp = os.path.join(_HERE, "train_log_fitcheck.jsonl")
    if os.path.exists(logp):
        os.remove(logp)
    print(f"FIT-CHECK: d=64 L=2, CPT 200 + drill 1500 on {device} (fixed objective λ={LAMBDA_ANS} + "
          "cosine LR); A-duel s0/s1 + C-perm s0 …", flush=True)
    fs = _panel_free_slots(drill)
    print(f"    d_acc scored on FREE slots {fs} (parity slots {{3,5}} excluded — codebook rank-4)", flush=True)
    res = {}
    for arm, seed in [("A-duel", 0), ("A-duel", 1), ("C-perm", 0)]:
        model, ce_ans = train_arm(arm, seed, (torch, M, cfg, Struct), {"f2": f2, "f1": f1},
                                  drill, cpt_win, (200, 1500), device, tag="fitcheck")
        rec = {"drill_dacc": round(dacc_panel(model, torch, drill[:64], arm, 0, device), 4),
               "ce_ans_final": round(ce_ans, 4)}
        if arm == "C-perm":                                       # confirm parity slots come free, held-out clean
            rec["per_slot_all6"] = dacc_perslot(model, torch, drill[:64], arm, 0, device)
            rec["f2doubleprime_heldout"] = round(dacc_panel(model, torch, f2, arm, 1, device), 4)
        res[f"{arm}.s{seed}"] = rec
        print(f"    {arm}.s{seed}: drill_dacc(free)={rec['drill_dacc']}  ce_ans={rec['ce_ans_final']}"
              + (f"  per_slot={rec['per_slot_all6']}  f2''(held-out,free)={rec['f2doubleprime_heldout']}"
                 if arm == "C-perm" else ""), flush=True)
    ad0, ad1 = res["A-duel.s0"]["drill_dacc"], res["A-duel.s1"]["drill_dacc"]
    cp = res["C-perm.s0"]
    parity = cp["per_slot_all6"][3] >= 0.9 and cp["per_slot_all6"][5] >= 0.9   # wiring: teacher-forced parity
    bar1 = ad0 >= 0.95 and ad1 >= 0.95 and abs(ad0 - ad1) <= 0.03
    bar2 = res["A-duel.s0"]["ce_ans_final"] < 0.05 and res["A-duel.s1"]["ce_ans_final"] < 0.05
    bar3 = 0.40 <= cp["drill_dacc"] <= 0.60 and 0.45 <= cp["f2doubleprime_heldout"] <= 0.55 and parity
    GO = bar1 and bar2 and bar3
    with open(os.path.join(_HERE, "fitcheck_result.json"), "w") as fh:
        json.dump({"device": device, "free_slots": fs, "results": res,
                   "bar1_aduel_fit": bar1, "bar2_ce_ans_decays": bar2, "bar3_cperm_harness": bar3,
                   "GO": GO}, fh, indent=2, ensure_ascii=False)
    print(f"\nbar1 A-duel≥0.95 both + spread≤0.03: {'PASS' if bar1 else 'FAIL'}  (s0={ad0} s1={ad1})")
    print(f"bar2 ce_ans<0.05 both:               {'PASS' if bar2 else 'FAIL'}")
    print(f"bar3 C-perm free∈[.40,.60]+f2''∈[.45,.55]+parity: {'PASS' if bar3 else 'FAIL'}  "
          f"(drill={cp['drill_dacc']} f2''={cp['f2doubleprime_heldout']} parity_slots={cp['per_slot_all6'][3]},{cp['per_slot_all6'][5]})")
    print("\nFIT-CHECK VERDICT:", "GO — launch the full run" if GO
          else "NO-GO — do not spend the full run; diagnose from train_log_fitcheck.jsonl")
    return 0 if GO else 1


def _frozen():
    card = os.path.join(_ROOT, "HYPOTHESES", "cards", "H_004_parser_duel_tension_rank_drill.md")
    for ln in open(card, encoding="utf-8"):
        if ln.strip().startswith("pre_register_frozen:"):
            return "true" in ln.lower()
    return False


_ROOT = os.path.dirname(os.path.dirname(_HERE))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--full-check", action="store_true", help="$0 plumbing: run_full at d=64 tiny steps")
    ap.add_argument("--fit-check", action="store_true",
                    help="pre-flight: does the fixed drill objective fit A-duel ≥0.95 at d=64 (~15min MPS)")
    a = ap.parse_args()
    import torch
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    if a.smoke:
        return smoke(device="cpu")
    if a.full_check:
        print(f"FULL-CHECK: run_full plumbing at d=64 on {device} (not a verdict; exercises the "
              "target device to catch CPU/MPS placement bugs) …")
        return run_full(device, cpt_steps=20, drill_steps=120, tag="check", seeds=(0,))
    if a.fit_check:
        return fit_check(device)
    if not _frozen():
        print("FULL RUN refused: H_004 card pre_register_frozen != true. Native-operator G-1 must "
              "clear and the card must be frozen first (no-escape-hatch).")
        return 2
    print("FULL RUN — H_004 G-2 d=384 ×2seed ×5arm (~4h)…", flush=True)
    return run_full(device, cpt_steps=8000, drill_steps=4000, tag="full", seeds=(0, 1))


if __name__ == "__main__":
    raise SystemExit(main())
