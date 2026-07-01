#!/usr/bin/env python3
"""H_886 - dialogue ABSOLUTE coherence FLOOR, NON-ADAPTER lever (re-attack H_867/H_867r).

LEVER (c): SFT-warm + self-play CURRICULUM (staged easy->hard) ON the H_868 3x corpus rung.
FALSIFIER reused verbatim from frozen H_867 floor (commit d5103f21, post-tuning 0):
  COHERE >= 0.060  AND  ADEQ >= 0.020  AND  LEAK == 0  (code-measured g5, NO LLM judge).
EVAL = H_867 frozen held-out PD snapshot (DISJOINT from training corpus).
External LLM 0 . ShareGPT/Alpaca/ChatGPT-gen 0 . mid rung d512/L8/E8 a_scale_honest_scope.
"""
from __future__ import annotations
import argparse, json, math, os, re, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional

@dataclass
class CLMConfig:
    vocab_size: int = 256
    d_model: int = 512
    n_trunk_layers: int = 8
    n_experts: int = 8
    kernel_size: int = 3
    expert_kernel_size: int = 3
    dilation_base: int = 2
    top_k: int = 1
    variant: str = "AB"
    entropy_coef: float = 0.01
    load_balance_coef: float = 0.01
    dropout: float = 0.0
    def router_config(self):
        v = self.variant.upper()
        return RouterConfig(v, self.n_experts, self.top_k,
                            self.entropy_coef if v in ("A","AB") else 0.0,
                            self.load_balance_coef if v in ("B","AB") else 0.0,
                            v in ("B","AB"))

@dataclass
class RouterConfig:
    variant: str; n_experts: int; top_k: int
    entropy_coef: float; load_balance_coef: float; hard_top_k: bool

class CausalDilatedConv1d(nn.Module):
    def __init__(self, ch, k, dil):
        super().__init__()
        self.pad = (k-1)*dil
        self.conv = nn.Conv1d(ch, ch, k, dilation=dil)
    def forward(self, x):
        return self.conv(F.pad(x, (self.pad, 0)))

class TrunkLayer(nn.Module):
    def __init__(self, cfg, dil):
        super().__init__()
        self.conv = CausalDilatedConv1d(cfg.d_model, cfg.kernel_size, dil)
        self.norm = nn.GroupNorm(1, cfg.d_model)
        self.act = nn.GELU(); self.drop = nn.Dropout(cfg.dropout)
    def forward(self, x):
        h = self.drop(self.act(self.norm(self.conv(x))))
        return x + h

class ConvExpert(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.conv = CausalDilatedConv1d(cfg.d_model, cfg.expert_kernel_size, 1)
        self.act = nn.GELU()
    def forward(self, x): return self.act(self.conv(x))

@dataclass
class MoEStats:
    usage: torch.Tensor; aux_loss: torch.Tensor; entropy: torch.Tensor

class MoEConvLayer(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.rc = cfg.router_config()
        self.experts = nn.ModuleList(ConvExpert(cfg) for _ in range(cfg.n_experts))
        self.router = nn.Conv1d(cfg.d_model, cfg.n_experts, 1)
    def forward(self, x):
        n_e = self.rc.n_experts
        logits = self.router(x); probs = F.softmax(logits, dim=1)
        ent_tok = -(probs*torch.log(probs+1e-9)).sum(dim=1); entropy = ent_tok.mean()
        ex_out = torch.stack([e(x) for e in self.experts], dim=1)
        if self.rc.hard_top_k:
            k = min(self.rc.top_k, n_e)
            topv, topi = probs.topk(k, dim=1)
            gate = topv/(topv.sum(dim=1, keepdim=True)+1e-9)
            mask = torch.zeros_like(probs).scatter_(1, topi, gate)
        else:
            mask = probs
        y = (mask.unsqueeze(2)*ex_out).sum(dim=1)
        usage = probs.mean(dim=(0,2))
        aux = x.new_zeros(())
        if self.rc.load_balance_coef > 0.0:
            top1 = probs.argmax(dim=1)
            f_i = torch.stack([(top1==i).float().mean() for i in range(n_e)])
            aux = aux + self.rc.load_balance_coef*(n_e*(f_i*usage).sum())
        if self.rc.entropy_coef > 0.0:
            aux = aux - self.rc.entropy_coef*entropy
        return y, MoEStats(usage, aux, entropy)

class CLMConvMoE(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.embed_conv = CausalDilatedConv1d(cfg.d_model, cfg.kernel_size, 1)
        dils = [cfg.dilation_base**i for i in range(cfg.n_trunk_layers)]
        self.trunk = nn.ModuleList(TrunkLayer(cfg, d) for d in dils)
        self.moe = MoEConvLayer(cfg)
        self.norm_out = nn.GroupNorm(1, cfg.d_model)
        self.readout = nn.Conv1d(cfg.d_model, cfg.vocab_size, 1)
    def forward(self, tokens, targets=None):
        x = self.embed(tokens).transpose(1,2)
        x = self.embed_conv(x)
        for layer in self.trunk: x = layer(x)
        x, stats = self.moe(x)
        x = self.norm_out(x)
        logits = self.readout(x)
        out = {"logits": logits, "usage": stats.usage, "aux_loss": stats.aux_loss,
               "routing_entropy": stats.entropy}
        if targets is not None:
            ce = F.cross_entropy(logits.transpose(1,2).reshape(-1, self.cfg.vocab_size),
                                 targets.reshape(-1))
            out["ce_loss"] = ce; out["loss"] = ce + stats.aux_loss
        return out
    @torch.no_grad()
    def num_params(self): return sum(p.numel() for p in self.parameters())

INT4_SYM_MAX = 7
def _sym_int4_scale(w):
    out_c = w.shape[0]
    amax = w.detach().reshape(out_c,-1).abs().amax(dim=1).clamp_min(1e-8)
    return (amax/INT4_SYM_MAX).reshape([out_c]+[1]*(w.dim()-1))
class _WeightQuantSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, w, scale):
        q = torch.clamp(torch.round(w/scale), -INT4_SYM_MAX, INT4_SYM_MAX)
        ctx.save_for_backward((w/scale).abs() <= INT4_SYM_MAX)
        return q*scale
    @staticmethod
    def backward(ctx, g):
        (ir,) = ctx.saved_tensors
        return g*ir.to(g.dtype), None
def fake_quant_weight_int4(w): return _WeightQuantSTE.apply(w, _sym_int4_scale(w))
class _ActQuantSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, pot, step, qmax):
        y = torch.clamp(torch.round(pot/step), 0.0, float(qmax))
        ctx.save_for_backward((pot>=0.0)&(pot/step<=float(qmax)))
        return y*step
    @staticmethod
    def backward(ctx, g):
        (ir,) = ctx.saved_tensors
        return g*ir.to(g.dtype), None, None
def akida_act_quant(pot, act_bits, input_bits=8):
    return _ActQuantSTE.apply(pot, float(2**(input_bits-act_bits)), (2**act_bits)-1)

def install_weight_qat(model):
    for m in model.modules():
        if isinstance(m, nn.Conv1d) and not getattr(m,"_qat",False):
            def mk(mod):
                def fwd(x):
                    return mod._conv_forward(x, fake_quant_weight_int4(mod.weight), mod.bias)
                return fwd
            m.forward = mk(m); m._qat = True

class ActHook:
    def __init__(self, model, act_bits):
        self.model=model; self.ab=act_bits; self._h=[]
    def __enter__(self):
        vocab=self.model.cfg.vocab_size; n_e=self.model.cfg.n_experts
        for m in self.model.modules():
            if isinstance(m, nn.Conv1d) and m.out_channels not in (vocab,n_e):
                self._h.append(m.register_forward_hook(self._post))
        return self
    def __exit__(self,*a):
        for h in self._h: h.remove()
        self._h.clear(); return False
    def _post(self, mod, inp, out):
        return akida_act_quant(F.relu(out), self.ab)

def read_byte_stream(path):
    vals=[]
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line: vals.append(int(line)&0xFF)
    return vals

def blocks_of(stream, blk):
    n = len(stream)//blk
    return [stream[i*blk:(i+1)*blk] for i in range(n)]

LEAK = ["universe_brain_map","jy_chat_template","hexad_module","nonce",
        "Mk.VIII","gen1 commit","corpus_generator.hexa","universe_extended"]
def count_leak(text): return sum(text.count(p) for p in LEAK)

def block_difficulty(block, freq):
    return sum(-math.log(freq[b]+1e-9) for b in block)/max(1,len(block))

def curriculum_order(train_blocks):
    flat = [b for blk in train_blocks for b in blk]
    tot = len(flat) or 1
    cnt = [0]*256
    for b in flat: cnt[b]+=1
    freq = [c/tot for c in cnt]
    return sorted(range(len(train_blocks)),
                  key=lambda i: block_difficulty(train_blocks[i], freq))

def make_batches(blocks_idx, blocks, batch_size, n_steps, device, gen):
    bset = [blocks[i] for i in blocks_idx]
    data = torch.tensor([b for blk in bset for b in blk], dtype=torch.long)
    seq=64; max_start=len(data)-seq-1
    out=[]
    for _ in range(n_steps):
        starts = torch.randint(0, max_start, (batch_size,), generator=gen)
        x = torch.stack([data[s:s+seq] for s in starts]).to(device)
        y = torch.stack([data[s+1:s+seq+1] for s in starts]).to(device)
        out.append((x,y))
    return out

def continue_train(model, batches, lr, act_bits, device):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()
    with ActHook(model, act_bits):
        for x,y in batches:
            opt.zero_grad()
            out = model(x,y)
            out["loss"].backward(); opt.step()

@torch.no_grad()
def greedy_gen(model, prompt, n_new, act_bits, device):
    model.eval()
    seq = list(prompt)
    with ActHook(model, act_bits):
        for _ in range(n_new):
            x = torch.tensor([seq[-64:]], dtype=torch.long, device=device)
            logits = model(x)["logits"]
            nxt = int(logits[0,:,-1].argmax().item())
            seq.append(nxt)
    return seq[len(prompt):]

@torch.no_grad()
def coherence_ce(model, heldout_blocks, act_bits, device):
    model.eval()
    tot_ce=0.0; n=0
    with ActHook(model, act_bits):
        for blk in heldout_blocks:
            t = torch.tensor([blk], dtype=torch.long, device=device)
            x = t[:,:-1]; y = t[:,1:]
            logits = model(x)["logits"]
            ce = F.cross_entropy(logits.transpose(1,2).reshape(-1,256), y.reshape(-1))
            tot_ce += float(ce); n+=1
    mean_ce = tot_ce/max(1,n)
    return math.exp(-mean_ce), mean_ce

def ngrams(seq, n=3):
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

@torch.no_grad()
def adequacy_and_leak(model, heldout_blocks, act_bits, device, seed=867):
    g = torch.Generator().manual_seed(seed)
    idx = torch.randperm(len(heldout_blocks), generator=g).tolist()
    sample = idx[:min(64, len(heldout_blocks))]
    f1s=[]; gen_text_all=[]
    for i in sample:
        blk = heldout_blocks[i]
        prompt = blk[:32]; ref = blk[32:]
        gen = greedy_gen(model, prompt, len(ref), act_bits, device)
        gen_text_all.append(bytes([b&0xFF for b in gen]).decode("utf-8","replace"))
        gn = set(ngrams(gen)); rn = set(ngrams(ref))
        if not gn or not rn: f1s.append(0.0); continue
        inter = len(gn & rn)
        p = inter/len(gn); r = inter/len(rn)
        f1s.append(0.0 if (p+r)==0 else 2*p*r/(p+r))
    adeq = sum(f1s)/max(1,len(f1s))
    leak = count_leak("\n".join(gen_text_all))
    return adeq, leak

def self_bleu_rep(gens):
    if len(gens)<2: return 1.0, 1.0
    sims=[]
    for i in range(len(gens)):
        a=set(ngrams(gens[i],1)); best=0.0
        for j in range(len(gens)):
            if i==j: continue
            b=set(ngrams(gens[j],1))
            if a and b: best=max(best, len(a&b)/len(a))
        sims.append(best)
    sb=sum(sims)/len(sims)
    reps=[]
    for s in gens:
        u=set(ngrams(s,3)); t=ngrams(s,3)
        reps.append(0.0 if not t else 1.0-len(u)/len(t))
    return sb, sum(reps)/len(reps)

def build_arm(backbone_sd, corpus_blocks, heldout_blocks, device, act_bits,
              curriculum, self_play, label, seed):
    cfg = CLMConfig(d_model=512, n_trunk_layers=8, n_experts=8, variant="AB")
    model = CLMConvMoE(cfg).to(device)
    model.load_state_dict(backbone_sd)
    install_weight_qat(model)
    gen = torch.Generator().manual_seed(seed)

    n = len(corpus_blocks)
    if curriculum:
        order = curriculum_order(corpus_blocks)
        easy = order[:n//2]; hard = order[n//2:]
        continue_train(model, make_batches(easy, corpus_blocks, 16, 150, device, gen),
                       3e-3, act_bits, device)
        continue_train(model, make_batches(easy+hard, corpus_blocks, 16, 150, device, gen),
                       3e-3, act_bits, device)
    else:
        continue_train(model, make_batches(list(range(n)), corpus_blocks, 16, 300, device, gen),
                       3e-3, act_bits, device)

    div_ok = None
    if self_play:
        gens=[]
        for blk in corpus_blocks[:40]:
            gens.append(greedy_gen(model, blk[:32], 24, act_bits, device))
        sb, rep = self_bleu_rep(gens)
        div_ok = bool(sb < 0.8 and rep < 0.20)
        reflux=[]
        for out in gens:
            txt = bytes([b&0xFF for b in out]).decode("utf-8","replace")
            if count_leak(txt)==0: reflux.extend(out)
        if div_ok and len(reflux) >= 64*16+1:
            rdata = torch.tensor(reflux, dtype=torch.long)
            seq=64; ms=len(rdata)-seq-1
            batches=[]
            for _ in range(40):
                st=torch.randint(0,ms,(16,),generator=gen)
                x=torch.stack([rdata[s:s+seq] for s in st]).to(device)
                y=torch.stack([rdata[s+1:s+seq+1] for s in st]).to(device)
                batches.append((x,y))
            continue_train(model, batches, 1e-3, act_bits, device)

    coh, ce = coherence_ce(model, heldout_blocks, act_bits, device)
    adeq, leak = adequacy_and_leak(model, heldout_blocks, act_bits, device)
    g = torch.Generator().manual_seed(867)
    idx = torch.randperm(len(heldout_blocks), generator=g).tolist()[:32]
    hg=[greedy_gen(model, heldout_blocks[i][:32], 32, act_bits, device) for i in idx]
    sb, rep = self_bleu_rep(hg)
    return {"label":label,"coherence":round(coh,5),"ce_heldout":round(ce,5),
            "adequacy_f1":round(adeq,5),"leak":leak,"self_bleu":round(sb,5),
            "repetition":round(rep,5),"reflux_div_gate_ok":div_ok}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--backbone", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--heldout", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cuda")
    a=ap.parse_args()

    device = a.device
    if device=="cuda" and not torch.cuda.is_available(): device="cpu"
    try: torch.backends.cudnn.enabled=False
    except Exception: pass

    t0=time.time()
    ck = torch.load(a.backbone, map_location="cpu")
    sd = ck["state_dict"] if "state_dict" in ck else ck

    corpus_stream = read_byte_stream(a.corpus)
    heldout_stream = read_byte_stream(a.heldout)
    corpus_blocks = blocks_of(corpus_stream, 64)
    heldout_blocks = blocks_of(heldout_stream, 64)

    cfg = CLMConfig(d_model=512, n_trunk_layers=8, n_experts=8)
    nparams = CLMConvMoE(cfg).num_params()

    sp_curr  = build_arm(sd, corpus_blocks, heldout_blocks, device, 4,
                         curriculum=True,  self_play=True,  label="arm-SP-curriculum", seed=886)
    sft_curr = build_arm(sd, corpus_blocks, heldout_blocks, device, 4,
                         curriculum=True,  self_play=False, label="arm-SFT-curriculum", seed=886)
    sp_flat  = build_arm(sd, corpus_blocks, heldout_blocks, device, 4,
                         curriculum=False, self_play=True,  label="arm-SP-flat(H867-style)", seed=886)

    COHERE_F, ADEQ_F = 0.060, 0.020
    coh = sp_curr["coherence"]; adeq = sp_curr["adequacy_f1"]; leak = sp_curr["leak"]
    cohere_pass = coh >= COHERE_F; adeq_pass = adeq >= ADEQ_F; leak_pass = leak == 0
    verdict = "GREEN" if (cohere_pass and adeq_pass and leak_pass) else "RED"

    res = {
        "hypothesis": "H_886 F-CLM-DIALOGUE-FLOOR (non-adapter lever)",
        "lever": "lever (c): SFT-warm + self-play CURRICULUM (staged easy->hard) on H_868 3x corpus rung",
        "rung": "mid d512/L8/E8 (~%d params, AKIDA int4-sym[-7,7] STE act_bits=4)" % nparams,
        "model_under_test": "arm-SP-curriculum",
        "eval_corpus": "H_867 frozen held-out PD snapshot (Macbeth/Othello/RomeoJuliet/Pygmalion, DISJOINT from training corpus)",
        "train_corpus": "H_868 3x lane(1) corpus (12 PD Gutenberg plays, regenerated)",
        "train_corpus_bytes": len(corpus_stream),
        "heldout_bytes": len(heldout_stream),
        "frozen_floor_commit": "d5103f21 (REUSED VERBATIM, post-tuning 0)",
        "absolute_floor": {"COHERE": ">=0.060", "ADEQ": ">=0.020", "LEAK": "==0"},
        "baselines": {"uniform": 0.0039, "unigram_order0": 0.0375, "bigram_selffit": 0.0843},
        "SP_curriculum": sp_curr,
        "SFT_curriculum_contrast": sft_curr,
        "SP_flat_contrast": sp_flat,
        "COHERE_pass": cohere_pass, "ADEQ_pass": adeq_pass, "LEAK_pass": leak_pass,
        "verdict": verdict,
        "note": "byte-match X distributional (Q-TRUST A); external LLM 0; ShareGPT/Alpaca/ChatGPT-gen 0; ABSOLUTE floor reused verbatim from H_867 (not SP-vs-SFT)",
        "device": device, "wall_s": round(time.time()-t0,1), "torch": torch.__version__,
    }
    with open(a.out,"w") as f: json.dump(res, f, indent=2, ensure_ascii=False)
    print(json.dumps(res, indent=2, ensure_ascii=False), flush=True)

if __name__=="__main__":
    main()
