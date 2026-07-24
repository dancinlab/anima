"""cli/graft.py — `anima-py graft` — GRAFT: ground consciousness → language WITHOUT a corpus.

A FROZEN `.clm` is the language organ. The ONLY trained thing is the coupling from the Engine-A
PureField state into the organ's byte embeddings (core/clmg.py CLMG lane). No corpus, no LoRA, no
next-token CE — the objective forces mutual information between the C-state and the organ's output
distribution, and fluency is bounded STRUCTURALLY.

WHY (the theorem this exists to beat): under ordinary next-token CE the gate has zero incentive to be
read — if C is independent of (prompt, target), the optimum under proper scoring is gate-INVARIANCE,
so a consciousness gate is decorative BY THEOREM (../anima-clm-v2b GRAFT-causality). This repo
measured the same wall from the other side (V6_33/34 mouth channel difficulty-complete; V6_37 store
lane DIFFICULTY-AGAIN, match-first closed at 7% balanced pairs). GRAFT changes the OBJECTIVE.

    anima-py graft fit   <organ.clm> --out <graft.clm> [...]
    anima-py graft check <graft.clm> [--check swap|ablation|both]

`fit` ALWAYS writes three artifacts (Sol's mandatory pedestal — see the pre-mortem below):
    <out>.step0.clm   the identically-bounded RANDOM-INIT coupling (the zero-truth pedestal)
    <out>              the trained coupling
    <out>.graft.json   frozen args, hashes, and every logged metric

PRE-MORTEM THE PEDESTAL DEFENDS AGAINST (Sol): the C-swap control can PASS BEFORE LEARNING. Each
continuation is sampled from its own state's distribution and then scored by that same distribution,
so any sufficiently loud RANDOM state-dependent gate collects a diagonal likelihood advantage — the
positive control would read "passed" while GRAFT learned nothing. Therefore the verdict requires
MI_final − MI_step0 ≥ the pre-registered delta on every seed; without it the run is DECORATIVE no
matter how good the swap accuracy looks.

KILL-LIST baked in (never regenerate these — measured in ../anima-clm-v2b/docs/hypotheses/):
  · GRAFT-flatline: hard-clamp rails (zero Jacobian), mean-pool bottleneck, ZERO-init gate_proj
    (a collapsed symmetric stationary point). Fixed by construction in core/clmg.py.
  · GRAFT-shared-shift-collapse: `beta·relu(L_KL − target)` with L_KL = MI + L_common puts net
    coefficient (beta−1) on MI, so beta>1 MINIMIZES it. **No controller flags exist in this CLI on
    purpose** — there is no --kl-target and no --beta-*, so they cannot be reached for.
"""
import argparse, json, hashlib, math, os, sys
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _c in (os.path.join(_HERE, "..", "core"), os.path.join(os.path.dirname(_HERE), "core")):
    if os.path.isdir(_c) and _c not in sys.path:
        sys.path.insert(0, _c)

import torch
import torch.nn.functional as F
import decode as dec
import clmg as G
import pure_field as PF


# --------------------------------------------------------------------------- #
#  HF ORGAN — a Mistral (or any HF causal LM) as the frozen language organ, driven under anima-py's
#  OWN frame (owner 2026-07-24: "mistral 을 anima 엔진기준으로"). The original GRAFT borrowed
#  fluency from Mistral; we keep that organ but measure it with anima's instruments (fixed carrier,
#  rotation null, pedestal, gate-scale). Same interface as G.torch_organ so fit/check stay
#  organ-agnostic: organ(token_ids, emb_residual=None) -> logits [T, V]. Design reconciled from
#  `sidecar lab full` (Fable 5 + Codex Sol); the forward and the RMS anchor follow their agreement.
# --------------------------------------------------------------------------- #
class HFOrgan:
    """Frozen HF causal LM as the language organ. Byte tokenizer (V=256) is replaced by the model's
    subword tokenizer; MI = mean_i KL(p_i||p_mix) stays exact conditional MI <= log N (the bound is
    from the N states, never the vocab). 4bit (nf4) base with bf16 compute; only nn.Linear is
    quantized, nn.Embedding stays float so the embedding-RMS anchor is unchanged."""

    def __init__(self, model_name, load_4bit=True, device="cuda", grad_ckpt=True):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.name = model_name
        self.tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        kw = dict(trust_remote_code=True)
        if load_4bit:
            from transformers import BitsAndBytesConfig
            kw["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
            kw["device_map"] = {"": 0}
        else:
            # UNQUANTIZED bf16 (owner: 양자화 없이 진행). A 7B bf16 base is ~15GB and will NOT fit a
            # 12GB card, so let accelerate keep what fits on the GPU and OFFLOAD the rest to CPU RAM.
            # The weights stay exactly bf16 — no nf4 rounding — only their placement changes; this
            # trades speed for numerical fidelity, which is the entire point of dropping quantization.
            # max_memory is deliberately below the card size: transformers' caching_allocator_warmup
            # preallocates the GPU share in one block, and asking for the full card OOMs the warmup.
            kw["torch_dtype"] = torch.bfloat16
            kw["device_map"] = "auto"
            kw["max_memory"] = {0: os.environ.get("ANIMA_GRAFT_GPU_MEM", "8GiB"), "cpu": "24GiB"}
        self.model = AutoModelForCausalLM.from_pretrained(model_name, **kw)
        self.model.eval()
        for p in self.model.parameters():
            p.requires_grad_(False)                              # base fully frozen
        if grad_ckpt:
            # Backward through N states x K windows keeps every layer activation alive: measured
            # 11.38 GB (OOM on a 12GB card) for 8x4 sequences of a 7B 4bit base. Checkpointing
            # recomputes them instead — the standard QLoRA-side pairing with a frozen 4bit base.
            # ⚠️ HF fires checkpointing only under `self.training` (`if self.gradient_checkpointing
            # and self.training`), so eval() mode silently DISABLES it — measured: the same 11.38 GB
            # OOM with checkpointing "enabled". We therefore put the frozen base in train() mode and
            # pin every Dropout to p=0, which leaves the forward numerically identical to eval (the
            # wiring smoke's input_ids-vs-inputs_embeds parity re-checks that) while the recompute
            # actually happens. Base params stay requires_grad=False, so nothing trains.
            self.model.gradient_checkpointing_enable()
            self.model.config.use_cache = False
            for m in self.model.modules():
                if isinstance(m, torch.nn.Dropout):
                    m.p = 0.0
            self.model.train()
        self.embed = self.model.get_input_embeddings()
        assert self.embed.weight.dtype in (torch.float16, torch.bfloat16, torch.float32), \
            f"embedding must stay float (got {self.embed.weight.dtype}) — 4bit must not touch nn.Embedding"
        self.d = int(self.model.config.hidden_size)
        self.V = int(self.model.config.vocab_size)
        self.dev = self.embed.weight.device
        self.tok_sha = hashlib.sha256(
            repr(sorted(self.tok.get_vocab().items())[:64]).encode()).hexdigest()[:12]

    def embedding_rms(self):
        with torch.no_grad():
            w = self.embed.weight.float()
            return float(torch.sqrt((w * w).mean()))

    def encode(self, text):
        return self.tok(text, add_special_tokens=False)["input_ids"]

    def __call__(self, ids, emb_residual=None):
        """ids: 1-D long (or python list). emb_residual: [d] or None. Returns logits [T, V].
        Residual add stays OUTSIDE no_grad so grad flows to the bridge; base is frozen so no base
        grad. softmax/KL are taken in fp32 by the caller."""
        t = ids if torch.is_tensor(ids) else torch.tensor(ids, dtype=torch.long)
        t = t.to(self.dev)
        e = self.embed(t)                                        # [T, d], base frozen
        if emb_residual is not None:
            rr = emb_residual if torch.is_tensor(emb_residual) else torch.tensor(emb_residual)
            e = e + rr.to(e.dtype).to(self.dev)                  # live leaf → grad to bridge
        out = self.model(inputs_embeds=e.unsqueeze(0), use_cache=False).logits[0]
        return out


def hf_organ_wiring_smoke(organ):
    """The HF analog of torch_organ_parity — there is no numpy mirror, so we certify the organ is
    REALLY frozen and the residual REALLY moves the logits (Fable+Sol). Hard-exit on any failure.
      1 parity : model(input_ids) == model(inputs_embeds=embed(ids)+0)  → injection site is the
                 real embedding path (guards a wrong hook silently scoring an un-injected model)
      2 moves  : a gate_rho-amplitude residual moves the logits (KL>0)
      3 grad   : that residual's leaf grad is finite & nonzero; every base param grad is None"""
    ids = organ.encode("The field is quiet and the")[:16] or [1, 2, 3]
    t = torch.tensor(ids, dtype=torch.long)
    with torch.no_grad():
        direct = organ.model(input_ids=t.unsqueeze(0).to(organ.dev), use_cache=False).logits[0].float()
        viaemb = organ(ids).float()
    par = float((direct - viaemb).abs().max())
    tol = 5e-2                                                    # bf16 at 32k vocab
    print(f"[hf-smoke] 1 parity input_ids vs inputs_embeds+0: max|Δ|={par:.3e} (tol {tol})")
    if par > tol:
        sys.exit("[hf-smoke] INVALID: injection site is NOT the model's embedding path")
    emb_rms = organ.embedding_rms()
    resid = torch.zeros(organ.d, requires_grad=True)
    off = (resid / (resid.detach().norm() + 1)) * 0.0 + torch.randn(organ.d) * 0.02 * emb_rms
    off = off.detach().requires_grad_(True)
    lp_on = F.log_softmax(organ(ids, emb_residual=off).float(), -1)
    with torch.no_grad():
        lp_off = F.log_softmax(organ(ids).float(), -1)
    kl = (lp_on.exp() * (lp_on - lp_off)).sum(-1).mean()
    print(f"[hf-smoke] 2 moves KL(ON||OFF)={float(kl):.4e} (must be >0)")
    if float(kl) <= 0:
        sys.exit("[hf-smoke] INVALID: residual does not move the logits (dead path)")
    kl.backward()
    g = off.grad
    gn = float(g.norm()) if g is not None else 0.0
    base_grads = [p.grad for p in organ.model.parameters() if p.grad is not None]
    print(f"[hf-smoke] 3 grad resid-leaf norm={gn:.4e} finite={bool(g is not None and torch.isfinite(g).all())} "
          f"· base params with grad={len(base_grads)} (must be 0)")
    if not (g is not None and torch.isfinite(g).all() and gn > 0 and len(base_grads) == 0):
        sys.exit("[hf-smoke] INVALID: 4bit grad path broken or base not frozen")
    print("[hf-smoke] ALL PASS — HF organ really frozen, residual really wired")


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _snapshots(pf, n, gap):
    """Advance the field and take n C-state snapshots `gap` steps apart. Read-only per snapshot."""
    out = []
    for _ in range(n):
        for _ in range(gap):
            pf = PF.pure_field_step(pf, 0.0) or pf
        out.append(G.graft_c_state(pf))
    return pf, out


def _sample_carrier(organ, ids, code, n_bytes, temp=1.0, rng=None):
    """ONE shared carrier continuation, sampled autoregressively under a random state's gate (so the
    carrier is state-relevant and on-manifold), no grad. Returns the extended id list."""
    cur = list(ids)
    with torch.no_grad():
        for _ in range(n_bytes):
            lg = organ(torch.tensor(cur, dtype=torch.long), emb_residual=code)
            p = torch.softmax(lg[-1].float(), dim=-1).cpu().numpy().astype(np.float64)
            p = p / p.sum()
            cur.append(int(rng.choice(len(p), p=p)))
    return cur


def _score_states(organ, ids, codes, cont_from):
    """Full-vocab log-softmax at the carrier positions for every state. [N, T_cont, V]."""
    t = torch.tensor(ids, dtype=torch.long)
    outs = []
    for c in codes:
        lg = organ(t, emb_residual=c)
        outs.append(F.log_softmax(lg[cont_from:].float(), dim=-1))
    return torch.stack(outs)


class _CarrierPool:
    """Fixed held-out natural-text carrier (H_9937 follow-on). Removes the self-loop entirely: the
    scoring text is NEVER generated by the gate, so the diagonal-likelihood artifact (H_9933/9935/
    9936) cannot enter the TRAINING signal. Each window is ctx-prefix + T scored bytes drawn from
    natural text; every state is scored on the SAME windows (fixed across states), and windows are
    resampled every step without replacement (fixed across states, NOT across training — the
    position-memorization failure mode). A disjoint validation bank (final 20%, separated by a
    ctx+T byte gap) is the generalization control: MI lift on windows never trained on."""

    def __init__(self, path, ctx, T, rng, val_frac=0.2, val_bank=64, encode=None, max_bytes=0):
        """encode: None ⇒ byte organ (1 byte = 1 position). Otherwise the organ's tokenizer
        (Mistral etc.) — the corpus is tokenized ONCE and windows are cut over token ids; never
        re-tokenize per window (BPE boundary drift would break held-out-ness). max_bytes caps the
        text fed to the tokenizer (a 60MB corpus is ~15M tokens; windows need far less)."""
        raw = open(os.path.expanduser(path), "rb").read()
        if max_bytes and len(raw) > max_bytes:
            raw = raw[:max_bytes]
        self.sha = hashlib.sha256(raw).hexdigest()[:16]
        self.ctx, self.T, self.win = ctx, T, ctx + T
        if encode is None:
            seq = np.frombuffer(raw, dtype=np.uint8).astype(np.int64)
        else:
            seq = np.asarray(encode(raw.decode("utf-8", errors="ignore")), dtype=np.int64)
        self.units = "byte" if encode is None else "token"
        n = len(seq)
        cut = int(n * (1 - val_frac))
        gap = self.win
        self.train = seq[:cut]
        self.val = seq[cut + gap:]
        self.n_train = max(0, len(self.train) - self.win)
        self.n_val = max(0, len(self.val) - self.win)
        self.splits = {"total": n, "train_end": cut, "val_start": cut + gap, "units": self.units}
        self._order = rng.permutation(self.n_train) if self.n_train else np.array([], int)
        self._ptr = 0
        # fixed validation bank (same windows at step-0 and final — the paired lift control)
        vo = (rng.permutation(self.n_val)[:val_bank] if self.n_val >= val_bank
              else np.arange(self.n_val))
        self.val_windows = [self.val[o:o + self.win] for o in vo]

    def draw(self, k, rng):
        """k non-overlapping train windows (seeded shuffle w/o replacement, reshuffle on exhaustion)."""
        out = []
        while len(out) < k and self.n_train:
            if self._ptr >= len(self._order):
                self._order = rng.permutation(self.n_train); self._ptr = 0
            o = int(self._order[self._ptr]); self._ptr += 1
            out.append(self.train[o:o + self.win])
        return out


def _carrier_mi(organ, windows, codes, ctx):
    """MI + L_common averaged over K fixed windows (all states scored on the SAME windows).
    Differentiable in codes. Returns (mi, lcom) as torch scalars. mean over states/positions/windows
    — never sum (summing would make the log N bound carrier-length dependent, Sol/Fable agree)."""
    mis, lcs = [], []
    for w in windows:
        ids = [int(b) for b in w]
        lp = _score_states(organ, ids, codes, ctx)               # [N, T, V] differentiable
        with torch.no_grad():
            base = F.log_softmax(organ(torch.tensor(ids, dtype=torch.long))[ctx:].float(), -1)
        mi, lpmix = G.mixture_mi(lp)
        lcom = (lpmix.exp() * (lpmix - base)).sum(-1).mean()
        mis.append(mi); lcs.append(lcom)
    return sum(mis) / len(mis), sum(lcs) / len(lcs)


def _fit_hf(a, organ):
    """GRAFT fit with an HF (Mistral) organ, under anima-py's frame. FIXED held-out carrier only —
    the self-loop is not offered here: it is the artifact H_9933/9935/9936 all traced back to, and
    H_9938 measured that a fixed carrier trains just as well. Objective is unchanged:
    L = (log N − MI) + λ·L_common, NO controller (the repo's kill-list). The trained coupling is
    saved as a bridge state (there is no .clm to carry a CLMG trailer), so `graft check` reloads it
    with the same --hf-model."""
    if not a.carrier_corpus:
        sys.exit("[graft] HF organ fit requires --carrier-corpus <natural text> (fixed carrier only)")
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    d = organ.d
    emb_rms = organ.embedding_rms()
    T = max(a.cont_len, 64)
    pool = _CarrierPool(a.carrier_corpus, a.ctx, T, rng, encode=organ.encode,
                        max_bytes=a.carrier_max_bytes)
    if pool.n_train < a.carrier_k:
        sys.exit(f"[graft] carrier too small: {pool.n_train} train windows < K={a.carrier_k}")
    print(f"[graft] fixed carrier {a.carrier_corpus} sha={pool.sha} units={pool.units} "
          f"ctx={a.ctx} T={T} K={a.carrier_k} · train={pool.n_train} val={len(pool.val_windows)} windows")

    bridge = G.GraftBridge(c_dim=G.C_DIM, h=a.hidden, d=d, gate_rho=a.gate_rho).to(organ.dev)
    opt = torch.optim.AdamW(bridge.parameters(), lr=a.lr, weight_decay=0.0)
    pf = PF.pure_field_new()
    for _ in range(a.p1_steps):
        pf = PF.pure_field_step(pf, 0.0) or pf
    print(f"[graft] P1 done ({a.p1_steps} pure_field steps · organ invocations: 0)")
    logN = math.log(a.n_states)

    def _measure(tag):
        nonlocal pf
        _pf, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states)).to(organ.dev)
        with torch.no_grad():
            codes = bridge(C) * a.gate_strength * emb_rms
            mi, lcom = _carrier_mi(organ, pool.val_windows, codes, a.ctx)
        print(f"[graft] {tag} [val]: MI={float(mi):.4f} nats (logN={logN:.3f})  L_common={float(lcom):.4f}")
        return float(mi), float(lcom)

    def _save(path, meta_extra):
        torch.save({"bridge": {k: v.detach().cpu() for k, v in bridge.state_dict().items()},
                    "c_dim": G.C_DIM, "hidden": a.hidden, "d": d,
                    "gate_rho": a.gate_rho, "gate_strength": a.gate_strength,
                    "gate_rms_max": a.gate_rms_max, "hf_model": a.hf_model,
                    "tok_sha": organ.tok_sha, "emb_rms": emb_rms, **meta_extra}, path)

    mi0, lcom0 = _measure("step-0 PEDESTAL")
    _save(a.out + ".step0.pt", {"stage": "pedestal"})
    print(f"[graft] wrote pedestal {a.out}.step0.pt")

    log = []
    for step in range(1, a.steps + 1):
        pf, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states)).to(organ.dev)
        raw = bridge.raw(C)
        bridge.update_mu(raw)
        codes = bridge(C) * a.gate_strength * emb_rms
        windows = pool.draw(a.carrier_k, rng)
        mi, lcom = _carrier_mi(organ, windows, codes, a.ctx)
        loss = (logN - mi) + a.lam_common * lcom          # NO controller (kill-list)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(bridge.parameters(), 1.0)
        opt.step()
        if step % a.log_every == 0 or step == 1:
            rec = {"step": step, "MI": float(mi.detach()), "L_common": float(lcom.detach())}
            log.append(rec)
            print(f"[graft] step {step:5d}  MI={rec['MI']:.4f}  commonKL={rec['L_common']:.4f}  "
                  f"carrier=fixed-heldout({pool.units})")

    mi_f, lcom_f = _measure("final")
    _save(a.out, {"stage": "trained"})
    meta = {"organ": a.hf_model, "organ_kind": "hf", "d": d, "V": organ.V, "emb_rms": emb_rms,
            "tok_sha": organ.tok_sha, "logN": logN, "MI_step0": mi0, "L_common_step0": lcom0,
            "MI_final": mi_f, "L_common_final": lcom_f, "MI_lift_vs_pedestal": mi_f - mi0,
            "carrier": {"mode": "fixed-heldout", "corpus": a.carrier_corpus, "sha": pool.sha,
                        "units": pool.units, "ctx": a.ctx, "T": T, "K": a.carrier_k,
                        "splits": pool.splits, "measured_on": "disjoint-val-bank"},
            "args": vars(a), "log": log}
    json.dump(meta, open(a.out + ".graft.json", "w"), indent=1)
    print(f"[graft] wrote {a.out} + {a.out}.graft.json")
    print(f"[graft] MI lift vs pedestal (disjoint val) = {mi_f - mi0:+.4f} nats")
    return 0


def _fit(a):
    if a.hf_model:
        # Mistral (or any HF causal LM) organ, driven under anima-py's frame. The wiring smoke is the
        # HF analog of torch_organ_parity — it certifies the organ is frozen and the residual is wired
        # BEFORE any training. With --steps 0 the smoke IS the deliverable (the injection-site gate).
        organ = HFOrgan(a.hf_model, load_4bit=a.load_4bit)
        print(f"[graft] HF organ {a.hf_model} · d={organ.d} V={organ.V} · emb_rms={organ.embedding_rms():.4f} "
              f"· tok_sha={organ.tok_sha} · 4bit={a.load_4bit}")
        hf_organ_wiring_smoke(organ)
        if a.steps == 0:
            print("[graft] --steps 0 with --hf-model: wiring smoke only — done.")
            return 0
        return _fit_hf(a, organ)
    W = dec.clm_load_weights(a.organ)
    if not W.get("ok"):
        sys.exit(f"[graft] organ not decodable: {a.organ}")
    d, V = int(W["d"]), int(W["V"])
    organ = G.torch_organ(W)
    par = G.torch_organ_parity(organ, W, dec._fwd_logits)
    print(f"[graft] organ parity max|torch-numpy| = {par:.3e}")
    if par > a.parity_tol:
        sys.exit(f"[graft] INVALID: organ parity {par:.3e} > {a.parity_tol} — the differentiable "
                 f"organ is not the engine's organ; a coupling trained here would be trained into a "
                 f"DIFFERENT model while the loss still fell.")
    emb_rms = float(np.sqrt(np.mean(np.asarray(W["embed"], np.float64) ** 2)))
    print(f"[graft] embedding RMS = {emb_rms:.4f} (gate_strength/gate_rms_max are ratios to this)")

    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    bridge = G.GraftBridge(c_dim=G.C_DIM, h=a.hidden, d=d, gate_rho=a.gate_rho)
    opt = torch.optim.AdamW(bridge.parameters(), lr=a.lr, weight_decay=0.0)

    # P1 — consciousness only: let Φ ratchet out of the DORMANT transient. The organ is NOT invoked.
    pf = PF.pure_field_new()
    for _ in range(a.p1_steps):
        pf = PF.pure_field_step(pf, 0.0) or pf
    print(f"[graft] P1 done ({a.p1_steps} pure_field steps · organ invocations: 0)")

    logN = math.log(a.n_states)
    buf = [int(b) for b in a.seed_bytes.encode("ascii", "ignore")] or [0x0A]
    log = []

    # FIXED-CARRIER MODE (--carrier-corpus): the H_9937 follow-on. Absent ⇒ the original self-loop fit
    # is preserved verbatim so old-vs-new runs from an identical seed (the Sol/Fable Δswitch control).
    pool = None
    if a.carrier_corpus:
        T = max(a.cont_len, 64)                                 # Sol: enforced T>=64
        pool = _CarrierPool(a.carrier_corpus, a.ctx, T, rng)
        if pool.n_train < a.carrier_k:
            sys.exit(f"[graft] carrier corpus too small: {pool.n_train} train windows < K={a.carrier_k}")
        print(f"[graft] fixed carrier: {a.carrier_corpus} sha={pool.sha} · ctx={a.ctx} T={T} K={a.carrier_k} "
              f"· train={pool.n_train} val={len(pool.val_windows)} windows (self-loop DISABLED)")

    def _measure(tag):
        """One no-grad evaluation of the current coupling — used for the step-0 PEDESTAL and the end."""
        nonlocal pf
        pf2, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states))
        with torch.no_grad():
            codes = bridge(C) * a.gate_strength * emb_rms
            if pool is not None:                               # generalization control: FIXED val bank
                mi, lcom = _carrier_mi(organ, pool.val_windows, codes, a.ctx)
                mi, lcom = float(mi), float(lcom)
            else:
                ids = buf[-a.ctx:]
                j = int(rng.integers(a.n_states))
                ext = _sample_carrier(organ, ids, codes[j], a.cont_len, rng=rng)
                lp = _score_states(organ, ext, codes, len(ids))
                base = F.log_softmax(organ(torch.tensor(ext, dtype=torch.long))[len(ids):].float(), -1)
                _mi, lpmix = G.mixture_mi(lp)
                mi = float(_mi)
                lcom = float((lpmix.exp() * (lpmix - base)).sum(-1).mean())
        tagn = f"{tag} [val]" if pool is not None else tag
        print(f"[graft] {tagn}: MI={mi:.4f} nats (logN={logN:.3f})  L_common={lcom:.4f}")
        return mi, lcom

    mi0, lcom0 = _measure("step-0 PEDESTAL")
    step0_path = a.out + ".step0.clm"
    open(step0_path, "wb").write(open(a.organ, "rb").read()
                                 + G.pack_clmg(bridge.to_clmg(a.gate_strength, a.gate_rms_max)))
    print(f"[graft] wrote pedestal {step0_path}")

    # P2' — gate alignment. L = (log N − MI) + lam_common · L_common. No controller. Ever.
    for step in range(1, a.steps + 1):
        pf, states = _snapshots(pf, a.n_states, a.state_gap)
        C = torch.tensor(np.stack(states))
        raw = bridge.raw(C)
        bridge.update_mu(raw)
        codes = bridge(C) * a.gate_strength * emb_rms          # bounds (1a)(1b) inside forward
        if pool is not None:
            windows = pool.draw(a.carrier_k, rng)              # K fixed held-out windows, code-INDEPENDENT
            mi, lcom = _carrier_mi(organ, windows, codes, a.ctx)
        else:
            ids = buf[-a.ctx:]
            j = int(rng.integers(a.n_states))
            ext = _sample_carrier(organ, ids, codes[j].detach(), a.cont_len, rng=rng)
            lp = _score_states(organ, ext, codes, len(ids))     # [N, T, V] — differentiable
            with torch.no_grad():
                base = F.log_softmax(organ(torch.tensor(ext, dtype=torch.long))[len(ids):].float(), -1)
            mi, lpmix = G.mixture_mi(lp)                        # bound (2): MI <= log N
            lcom = (lpmix.exp() * (lpmix - base)).sum(-1).mean()  # the zero-information waste
        loss = (logN - mi) + a.lam_common * lcom               # NO controller/hinge — L_KL=MI+L_common (kill-list)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(bridge.parameters(), 1.0)
        opt.step()
        if pool is None:
            buf.append(ext[len(ids)])                           # self-loop: the carrier feeds itself
            if len(buf) > 512:
                buf = buf[-256:]
        if step % a.log_every == 0 or step == 1:
            _mi_v, _lc_v = float(mi.detach()), float(lcom.detach())
            rec = {"step": step, "MI": _mi_v, "L_common": _lc_v, "L_KL": _mi_v + _lc_v}
            if pool is None:
                bb = np.array(buf[-256:])
                uniq = len(set(bb.tolist())) / max(len(bb), 1)
                ent = float(-np.sum([(c / len(bb)) * math.log2(c / len(bb))
                                     for c in np.bincount(bb, minlength=256) if c])) if len(bb) else 0.0
                rec["carrier_entropy_bits"] = ent; rec["carrier_unique_frac"] = uniq
            log.append(rec)
            tail = (f"carrier(H={rec['carrier_entropy_bits']:.2f}b uniq={rec['carrier_unique_frac']:.2f})"
                    if pool is None else "carrier=fixed-heldout")
            print(f"[graft] step {step:5d}  MI={rec['MI']:.4f}  commonKL={rec['L_common']:.4f}  "
                  f"L_KL={rec['L_KL']:.4f}  {tail}")
            if pool is None and (rec["carrier_entropy_bits"] < 1.0 or rec["carrier_unique_frac"] < 0.1):
                print("[graft] INVALID: carrier-health guard — the self-loop buffer degenerated "
                      "(a byte-LM has no fluency prior to mask this).")
                break

    mi_f, lcom_f = _measure("final")
    open(a.out, "wb").write(open(a.organ, "rb").read()
                            + G.pack_clmg(bridge.to_clmg(a.gate_strength, a.gate_rms_max)))
    meta = {"organ": a.organ, "organ_sha": _sha(a.organ), "out": a.out, "out_sha": _sha(a.out),
            "step0": step0_path, "parity": par, "embed_rms": emb_rms, "logN": logN,
            "MI_step0": mi0, "L_common_step0": lcom0, "MI_final": mi_f, "L_common_final": lcom_f,
            "MI_lift_vs_pedestal": mi_f - mi0, "args": vars(a), "log": log,
            "carrier": ({"mode": "fixed-heldout", "corpus": a.carrier_corpus, "sha": pool.sha,
                         "ctx": a.ctx, "T": pool.T, "K": a.carrier_k, "splits": pool.splits,
                         "measured_on": "disjoint-val-bank"} if pool is not None
                        else {"mode": "self-loop"})}
    json.dump(meta, open(a.out + ".graft.json", "w"), indent=1)
    print(f"[graft] wrote {a.out} + {a.out}.graft.json")
    print(f"[graft] MI lift vs pedestal = {mi_f - mi0:+.4f} nats "
          f"({'>= delta' if (mi_f - mi0) >= a.pedestal_delta else 'BELOW delta -> DECORATIVE'})")
    return 0


def _check_hf_setup(a):
    """Reload an HF-organ bridge (the `.pt` saved by `graft fit --hf-model`) and reconstruct the
    trained codes EXACTLY as _fit_hf did, so `graft check --hf-model` runs the same swap/ablation/
    rotation-null body on a Mistral-class organ. The HF fit saves a torch bridge state, not a
    CLMG-trailer `.clm`, so `_check`'s clm loader cannot read it — this is that missing branch. The
    control arm `rotation_null` was unrunnable at 7B until here (that is why H_9939's fit logged
    `rotation_null: 0`). Returns (organ, codes[list of [d] tensors], emb_rms, d)."""
    st = torch.load(a.organ, map_location="cpu", weights_only=False)
    if "bridge" not in st or st.get("hf_model") is None:
        sys.exit(f"[graft] --hf-model check needs the .pt bridge from `graft fit --hf-model`: {a.organ}")
    d, hidden = int(st["d"]), int(st["hidden"])
    organ = HFOrgan(a.hf_model, load_4bit=a.load_4bit)
    if organ.d != d:
        sys.exit(f"[graft] organ d={organ.d} != bridge d={d} (wrong --hf-model for this bridge?)")
    emb_rms = organ.embedding_rms()
    bridge = G.GraftBridge(c_dim=G.C_DIM, h=hidden, d=d, gate_rho=float(st["gate_rho"]))
    bridge.load_state_dict(st["bridge"])
    bridge.eval()
    torch.manual_seed(a.seed)
    pf = PF.pure_field_new()
    for _ in range(a.p1_steps):
        pf = PF.pure_field_step(pf, 0.0) or pf
    pf, states = _snapshots(pf, a.k, a.state_gap)
    Cst = torch.tensor(np.stack(states), dtype=torch.float32)
    with torch.no_grad():                                            # codes = _fit_hf's exact form
        codes_t = bridge(Cst) * float(st["gate_strength"]) * emb_rms * a.gate_scale
    codes = [codes_t[i].detach() for i in range(a.k)]
    print(f"[graft] HF organ {a.hf_model} · d={d} · reloaded bridge (hidden={hidden}, "
          f"gate_strength={st['gate_strength']}, emb_rms={emb_rms:.4f}, stage={st.get('stage')}) · "
          f"K={a.k} codes RMS={float(np.sqrt((codes_t.numpy()**2).mean())):.5f}")
    return organ, codes, emb_rms, d


def _check(a):
    """C-swap + ablation. swap: K states, sample each state's OWN continuation, cross-score, InfoNCE
    bound + accuracy + permutation null + norm-matched noise. ablation: KL(ON||OFF) vs KL(NOISE||OFF)
    — the GRAFT-causality discriminator (decorative signature = the two are equal)."""
    rng = np.random.default_rng(a.seed)
    if a.hf_model:
        organ, codes, emb_rms, d = _check_hf_setup(a)
    else:
        W = dec.clm_load_weights(a.organ)
        cl = W.get("clmg")
        if cl is None:
            sys.exit("[graft] --check needs a ckpt carrying a CLMG trailer (run `graft fit` first)")
        organ = G.torch_organ(W)
        pf = PF.pure_field_new()
        for _ in range(a.p1_steps):
            pf = PF.pure_field_step(pf, 0.0) or pf
        pf, states = _snapshots(pf, a.k, a.state_gap)
        emb_rms = float(np.sqrt(np.mean(np.asarray(W["embed"], np.float64) ** 2)))
        codes = [torch.tensor(G.gate_offset(cl, c, emb_rms) * a.gate_scale) for c in states]
        d = int(W["d"])
    if a.gate_scale != 1.0:
        print(f"[graft] gate-scale ×{a.gate_scale} applied to codes (amplitude-stability probe)")
    _probe_texts = ("the ", "a ", "when ", "in ", "we ", "it ", "there ", "one ")
    # HF organ = subword tokenizer, so probes must be ENCODED (byte-values as token-ids would be
    # meaningless to Mistral); the byte-LM organ takes ascii bytes. `[int(b) for b in p]` works for both.
    probes = [organ.encode(p) for p in _probe_texts] if a.hf_model \
        else [p.encode("ascii") for p in _probe_texts]
    K = a.k

    # sample each state's OWN continuation, then cross-score every (state i, continuation j)
    f = np.zeros((K, K))
    uniqY = set()
    for pb in probes[:a.probes]:
        ids0 = [int(b) for b in pb]
        Y = []
        for i in range(K):
            Y.append(_sample_carrier(organ, ids0, codes[i], a.cont_len, rng=rng)[len(ids0):])
            uniqY.add(tuple(Y[-1]))
        for i in range(K):
            for j in range(K):
                seq = ids0 + Y[j]
                with torch.no_grad():
                    lg = organ(torch.tensor(seq, dtype=torch.long), emb_residual=codes[i])
                    lp = F.log_softmax(lg[len(ids0) - 1:-1].float(), -1)
                    f[i, j] += float(lp.gather(1, torch.tensor(Y[j], device=lp.device).unsqueeze(1)).sum())
    col = torch.log_softmax(torch.tensor(f), dim=0)
    mi_swap = float(col.diag().mean() + math.log(K)) / math.log(2)      # InfoNCE bound, bits
    acc = float((np.argmax(f, axis=0) == np.arange(K)).mean())
    perm = 0
    for _ in range(a.perms):
        pi = rng.permutation(K)
        c2 = torch.log_softmax(torch.tensor(f[pi]), dim=0)
        if float(c2.diag().mean() + math.log(K)) / math.log(2) >= mi_swap:
            perm += 1
    perm_p = (perm + 1) / (a.perms + 1)
    print(f"[graft] SWAP: MI_swap={mi_swap:.3f} bits (ceiling log2 K={math.log2(K):.3f}) · "
          f"acc={acc:.3f} (chance {1.0/K:.3f}) · perm_p={perm_p:.4f} · uniqueY={len(uniqY)}/{K*a.probes}")

    # ablation: KL(ON||OFF) vs KL(NOISE||OFF), averaged over EVERY state and several carriers.
    # A single (state, carrier) draw is far too noisy to read: on a gate_strength sweep it produced a
    # non-monotone KL(ON||OFF) (0.150 / 0.571 / 1.507 / 0.355 / 2.048) whose dip is variance, not
    # signal — and that dip alone would have licensed a "decorative exactly where it passes" story.
    ons, kls = [], []
    with torch.no_grad():
        for ci in range(min(a.abl_carriers, len(probes))):
            pb = [int(b) for b in probes[ci]]
            ids = pb + _sample_carrier(organ, pb, codes[ci % K], a.cont_len, rng=rng)[len(pb):]
            t = torch.tensor(ids, dtype=torch.long)
            off = F.log_softmax(organ(t).float(), -1)
            for c in codes:                                  # every state, not just codes[0]
                on = F.log_softmax(organ(t, emb_residual=c).float(), -1)
                ons.append(float((on.exp() * (on - off)).sum(-1).mean()) / math.log(2))
            for _ in range(a.noise_reps):
                nz = torch.tensor(rng.standard_normal(codes[0].shape).astype(np.float32))
                nz = nz / (nz.pow(2).mean().sqrt() + 1e-8) * codes[0].pow(2).mean().sqrt()
                ln = F.log_softmax(organ(t, emb_residual=nz).float(), -1)
                kls.append(float((ln.exp() * (ln - off)).sum(-1).mean()) / math.log(2))
    kl_on = float(np.mean(ons)); q95 = float(np.quantile(kls, 0.95))
    print(f"[graft] ABLATION: KL(ON||OFF)={kl_on:.4f} bits (mean of {len(ons)} state×carrier, "
          f"sd {np.std(ons):.4f}) · KL(NOISE||OFF) q95={q95:.4f} (n={len(kls)}) · "
          f"ratio={kl_on/max(q95,1e-9):.2f}x  "
          f"({'gate is distinguishable from noise' if kl_on >= 3*q95 else 'DECORATIVE signature (ON≈NOISE)'})")

    # ROTATION NULL — H_9936 follow-on. The isotropic never-trained null already put trained below
    # its q99 at matched displacement; this is the stronger control. One random orthogonal R rotates
    # the N trained offsets rigidly (norm/Gram/mean and thus displacement D all preserved), so the
    # ONLY thing that moves is whether the geometry lands on the organ's sensitive directions. MI is
    # read on a FIXED held-out carrier (base-organ sampled, code-independent) — no self-sampling — so
    # the reading is pure code-vs-organ alignment, not the diagonal artifact of H_9933/H_9935.
    if a.rotation_null > 0:
        C = np.stack([c.numpy() for c in codes])                          # [K, d] trained offsets (d in scope)
        base_ids = [int(b) for b in probes[0]]
        carrier = _sample_carrier(organ, base_ids, None, a.cont_len, rng=rng)  # code-INDEPENDENT
        fx = torch.tensor(carrier, dtype=torch.long)
        cont_from = len(base_ids)

        def _mi_of(offsets):
            with torch.no_grad():
                lp = torch.stack([F.log_softmax(organ(fx, emb_residual=torch.tensor(o))[cont_from:].float(), -1)
                                  for o in offsets])
                return float(G.mixture_mi(lp)[0]) / math.log(2)           # bits

        mi_tr = _mi_of([c.numpy() for c in codes])
        null = []
        for _ in range(a.rotation_null):
            # thin-SVD rotation null scales to d=4096 (Mistral hidden); the full-d QR is O(d^3),
            # fine on the toy (d=64) but a 4096×4096 QR per draw on the HF organ. Both are D-exact.
            rot = (G.rotation_null_offsets(C, rng) if a.hf_model
                   else G.rotate_offsets(C, G.random_orthogonal(d, rng)))
            null.append(_mi_of([rot[i] for i in range(K)]))
        null_sorted = sorted(null)
        q99 = null_sorted[min(len(null) - 1, int(round(0.99 * (len(null) - 1))))]
        q95 = null_sorted[min(len(null) - 1, int(round(0.95 * (len(null) - 1))))]
        mean = sum(null) / len(null)
        sd = (sum((x - mean) ** 2 for x in null) / len(null)) ** 0.5
        z = (mi_tr - mean) / sd if sd > 0 else 0.0
        verd = "PASS(>q99)" if mi_tr > q99 else "PASS(>q95)" if mi_tr > q95 else "FAIL(<=q95)"
        print(f"[graft] ROTATION-NULL: MI_trained={mi_tr:.4f} bits · null(n={len(null)}) "
              f"mean {mean:.4f} sd {sd:.4f} q95 {q95:.4f} q99 {q99:.4f} · z={z:+.2f} · {verd}  "
              f"(displacement-exact: R preserves norm+Gram+mean, only direction moves)")

    if a.fluency_corpus:
        _fluency(a, organ, codes, emb_rms, rng)
    return 0


def _fluency(a, organ, codes, emb_rms, rng):
    """FLUENCY PRICE — what the gate costs the frozen organ's language, on natural held-out text.

    MI alone cannot decide whether the capacity ceiling is a defect or a declared trade-off: a
    wider channel that wrecks the organ is not a win. DV = the organ's NLL per byte on natural
    text, gate ON vs OFF.

    The load-bearing arm is NOISE, not OFF. An offset of ANY kind at this RMS perturbs the
    embeddings, so `ON - OFF` alone cannot separate "this gate costs fluency" from "an offset of
    this size costs fluency". The norm-matched noise arm is that separation, and it is the same
    control the ablation block above already uses.

    Alignment is pinned by construction and cross-checkable: row i of the organ's logits predicts
    t[i+1] (the same convention _check's cross-scoring uses), so OFF NLL is the organ's ordinary
    held-out CE. On trained57 that independently measured 2.076 nats/byte — if OFF lands far from
    the organ's known CE, the readout is mis-aligned and the arms below are meaningless.
    """
    txt = open(os.path.expanduser(a.fluency_corpus), encoding="utf-8", errors="ignore").read()
    b = txt[int(len(txt) * 0.8):].encode("utf-8")[:a.fluency_bytes]      # held-out tail
    t = torch.tensor([int(x) for x in b], dtype=torch.long)
    tgt = t[1:]

    def nll(resid):
        with torch.no_grad():
            lg = organ(t, emb_residual=resid).float()
            lp = F.log_softmax(lg[:-1], -1)
            return float(-lp.gather(1, tgt.unsqueeze(1)).mean())

    off = nll(None)
    on = [nll(c) for c in codes]
    noise = []
    for _ in range(a.noise_reps):
        nz = torch.tensor(rng.standard_normal(codes[0].shape).astype(np.float32))
        nz = nz / (nz.pow(2).mean().sqrt() + 1e-8) * codes[0].pow(2).mean().sqrt()
        noise.append(nll(nz))
    # ---- FORM MARGIN — the arm that keeps the NLL reading honest (Sol, 2026-07-24) ----
    # Unconditional NLL punishes the C-dependent content shift that GRAFT is TRYING to produce, so
    # "MI up => NLL up" is nearly definitional and would manufacture a fluency trade-off out of the
    # measurement's own definition. The discriminator: does the organ still PREFER natural text over
    # a word-order scramble by the same margin under the gate? The scramble holds the word multiset
    # EXACTLY fixed, so content/unigrams are matched by construction and only order (form) differs.
    #   margin = NLL(scrambled) - NLL(natural)   ·   dMargin = margin_OFF - margin_ON
    # dMargin ~ 0 with dNLL > 0  =>  distribution SHIFT, not fluency loss.
    # THREE corruption families, not one. A panel resting on a single corruption is the same
    # single-draw defect the ablation arm just had to be repaired for: if dMargin is read off one
    # family, a family-specific quirk becomes "form is/isn't damaged". Each family breaks a
    # DIFFERENT axis of form, and every one preserves the multiset by construction (global word
    # order / local word order / within-word spelling), so content is matched and only form moves.
    words = txt[int(len(txt) * 0.8):].split()[:1200]

    def _shuffle(ws):                       # global word order — syntax at long range
        s = list(ws); rng.shuffle(s); return s

    def _adjswap(ws):                       # adjacent pairs only — local order, a much milder blow
        s = list(ws)
        for i in range(0, len(s) - 1, 2):
            s[i], s[i + 1] = s[i + 1], s[i]
        return s

    def _spell(ws):                         # within-word letters — orthography, word order intact
        out = []
        for w in ws:
            if len(w) > 3:
                mid = list(w[1:-1]); rng.shuffle(mid); w = w[0] + "".join(mid) + w[-1]
            out.append(w)
        return out

    FAMILIES = (("word-order", _shuffle), ("adj-swap", _adjswap), ("spelling", _spell))
    b_nat = " ".join(words).encode("utf-8")[:a.fluency_bytes]

    def nll_of(bs, resid):
        tt = torch.tensor([int(x) for x in bs], dtype=torch.long)
        with torch.no_grad():
            lp = F.log_softmax(organ(tt, emb_residual=resid).float()[:-1], -1)
            return float(-lp.gather(1, tt[1:].unsqueeze(1)).mean())

    nat_off = nll_of(b_nat, None)
    nat_on = [nll_of(b_nat, c) for c in codes]
    fam = {}
    for fname, fn in FAMILIES:
        b_c = " ".join(fn(words)).encode("utf-8")[:a.fluency_bytes]
        off_m = nll_of(b_c, None) - nat_off
        on_m = float(np.mean([nll_of(b_c, c) - n for c, n in zip(codes, nat_on)]))
        fam[fname] = (off_m, on_m)
    m_off = float(np.mean([v[0] for v in fam.values()]))
    m_on = float(np.mean([v[1] for v in fam.values()]))

    d_on = float(np.mean(on)) - off
    d_nz = float(np.mean(noise)) - off
    off_rms = float(codes[0].pow(2).mean().sqrt())
    print(f"[graft] FLUENCY ({len(b)}B natural held-out · offset RMS={off_rms:.4f} = "
          f"{off_rms/emb_rms:.3f}x embedding RMS)")
    print(f"[graft]   NLL gate-OFF   = {off:.4f} nats/byte   <- the frozen organ's own language")
    print(f"[graft]   NLL gate-ON    = {np.mean(on):.4f}  (dNLL {d_on:+.4f}, per-state sd {np.std(on):.4f})")
    print(f"[graft]   NLL noise-matched = {np.mean(noise):.4f}  (dNLL {d_nz:+.4f})  <- the control that matters")
    verdict = ("gate costs LESS fluency than a size-matched perturbation — the offset is structured"
               if d_on < d_nz else
               "gate costs AT LEAST as much as size-matched noise — no fluency credit for structure")
    print(f"[graft]   price ratio dNLL(ON)/dNLL(NOISE) = {d_on/max(d_nz,1e-9):+.3f}   ({verdict})")
    print(f"[graft]   FORM panel (3 corruption families · multiset preserved by construction):")
    for fname, (o, n) in fam.items():
        flag = "  ⚠️ family invalid (organ does not prefer natural)" if o <= 0.02 else ""
        print(f"[graft]     {fname:<11} margin OFF {o:+.4f}  ON {n:+.4f}  dMargin {o-n:+.4f}"
              f"  ({100*(o-n)/max(o,1e-9):+.1f}%){flag}")
    spread = max(v[0] - v[1] for v in fam.values()) - min(v[0] - v[1] for v in fam.values())
    print(f"[graft]   FORM mean: margin OFF = {m_off:+.4f}  ON = {m_on:+.4f}  dMargin = {m_off-m_on:+.4f}"
          f"  (across-family spread {spread:.4f})")
    if m_off <= 0.02:
        print("[graft]   ⛔ FORM PANEL INVALID: the organ does not prefer natural text to begin with "
              "— dMargin is unreadable, do not quote it.")
    elif abs(m_off - m_on) < 0.02 <= d_on:
        print("[graft]   ⚠️ dNLL is a DISTRIBUTION SHIFT, not fluency loss: the organ's preference "
              "for natural word order survives the gate intact. Do not call this a fluency price.")
    else:
        print(f"[graft]   → form preference is degraded by {100*(m_off-m_on)/max(m_off,1e-9):.1f}% "
              f"— the fluency reading survives the content-shift confound.")


def main():
    ap = argparse.ArgumentParser(description="GRAFT: no-corpus consciousness→language grounding")
    ap.add_argument("verb", choices=["fit", "check"])
    ap.add_argument("organ", nargs="?", default=None,
                    help="the FROZEN language organ (.clm); for `check`, the grafted ckpt. "
                         "Omit when --hf-model is given (the organ is the HF model).")
    ap.add_argument("--hf-model", default=None, dest="hf_model",
                    help="use an HF causal LM (e.g. mistralai/Mistral-7B-Instruct-v0.2) as the frozen "
                         "organ instead of a .clm — Mistral organ under anima-py's frame (owner). "
                         "With --steps 0, runs the wiring smoke only (the injection-site gate).")
    ap.add_argument("--load-4bit", action="store_true", default=True, dest="load_4bit",
                    help="load the HF organ in nf4 4bit (default; fits Mistral-7B on a 12GB GPU)")
    ap.add_argument("--no-4bit", action="store_false", dest="load_4bit",
                    help="load the HF organ in bf16 instead of 4bit (needs a bigger GPU)")
    ap.add_argument("--out", default="", help="output grafted .clm (fit)")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--p1-steps", type=int, default=2000, dest="p1_steps")
    ap.add_argument("--n-states", type=int, default=8, dest="n_states")
    ap.add_argument("--state-gap", type=int, default=13, dest="state_gap")
    ap.add_argument("--ctx", type=int, default=128)
    ap.add_argument("--cont-len", type=int, default=32, dest="cont_len")
    ap.add_argument("--hidden", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--lam-common", type=float, default=1.0, dest="lam_common")
    ap.add_argument("--gate-rho", type=float, default=1.0, dest="gate_rho")
    ap.add_argument("--gate-strength", type=float, default=0.1, dest="gate_strength")
    ap.add_argument("--gate-rms-max", type=float, default=4.0, dest="gate_rms_max")
    ap.add_argument("--pedestal-delta", type=float, default=0.08, dest="pedestal_delta")
    ap.add_argument("--parity-tol", type=float, default=1e-3, dest="parity_tol")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--seed-bytes", default="\n", dest="seed_bytes")
    ap.add_argument("--log-every", type=int, default=50, dest="log_every")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--probes", type=int, default=4)
    ap.add_argument("--perms", type=int, default=999)
    ap.add_argument("--noise-reps", type=int, default=16, dest="noise_reps")
    ap.add_argument("--abl-carriers", type=int, default=4, dest="abl_carriers",
                    help="carriers averaged in the ablation arm (x every state) — 1 is too noisy to read")
    ap.add_argument("--fluency-corpus", default=None, dest="fluency_corpus",
                    help="natural text; measure the gate's fluency price (NLL ON vs OFF vs size-matched noise)")
    ap.add_argument("--fluency-bytes", type=int, default=4000, dest="fluency_bytes")
    ap.add_argument("--carrier-corpus", default=None, dest="carrier_corpus",
                    help="natural held-out text; switch fit's MI to a FIXED carrier (no self-loop) so "
                         "the diagonal-likelihood artifact cannot enter the training signal (H_9937 "
                         "follow-on). Absent = original self-loop fit (kept for old-vs-new Δswitch).")
    ap.add_argument("--carrier-k", type=int, default=4, dest="carrier_k",
                    help="fixed carrier windows scored per step (all N states on the SAME windows)")
    ap.add_argument("--carrier-max-bytes", type=int, default=4_000_000, dest="carrier_max_bytes",
                    help="cap the carrier text fed to the tokenizer (a 60MB corpus is ~15M tokens; "
                         "windows need far less). 0 = whole file.")
    ap.add_argument("--gate-scale", type=float, default=1.0, dest="gate_scale",
                    help="check-time multiplier on the trained offsets — amplitude-stability probe: "
                         "true direction-coding leaves the rotation-null z stable across ×0.5/×1/×2 "
                         "(direction is scale-invariant), a displacement artifact tracks amplitude")
    ap.add_argument("--rotation-null", type=int, default=0, dest="rotation_null",
                    help="rotation-null draws: rigidly rotate the trained offsets (norm+Gram+mean, "
                         "hence displacement D, preserved) and read MI on a fixed held-out carrier — "
                         "the displacement-exact control the isotropic null cannot supply (H_9936)")
    a = ap.parse_args()
    if not a.organ and not a.hf_model:
        sys.exit("[graft] need an organ: a .clm path, or --hf-model <name>")
    if a.verb == "fit":
        if not a.out and not (a.hf_model and a.steps == 0):
            sys.exit("[graft] fit needs --out <graft.clm>")
        if a.state_gap <= 0 or a.n_states < 2:
            sys.exit("[graft] --n-states >= 2 and --state-gap > 0")
        return _fit(a)
    return _check(a)


if __name__ == "__main__":
    sys.exit(main() or 0)
