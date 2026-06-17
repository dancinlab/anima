#!/usr/bin/env python3
# Per-layer activation dump computed FROM chat_full.bin (the exact weights CORE reads),
# using the SAME ByteGPT/torch model as the golden. This isolates MATH divergence from
# any serialization mismatch: torch and CORE consume byte-identical weights.
import struct, numpy as np, torch, torch.nn as nn

PATH="/tmp/parity-verify/chat_full.bin"
PROMPT="The quick brown"

f=open(PATH,'rb')
vocab,d,nlay,nh,block = struct.unpack('<5I', f.read(20))
def rd(n):  # n floats, little-endian f32
    return torch.from_numpy(np.frombuffer(f.read(n*4), dtype='<f4').copy())
tok = rd(vocab*d).view(vocab,d)
pos = rd(block*d).view(block,d)

class Block(nn.Module):
    def __init__(s,d,h):
        super().__init__()
        s.ln1=nn.LayerNorm(d); s.attn=nn.MultiheadAttention(d,h,dropout=0.0,batch_first=True)
        s.ln2=nn.LayerNorm(d); s.mlp=nn.Sequential(nn.Linear(d,4*d),nn.GELU(),nn.Linear(4*d,d))
    def forward(s,x,m):
        h=s.ln1(x); a,_=s.attn(h,h,h,attn_mask=m,need_weights=False); x=x+a
        return x+s.mlp(s.ln2(x))

blocks=nn.ModuleList([Block(d,nh) for _ in range(nlay)])
with torch.no_grad():
    for L in range(nlay):
        b=blocks[L]
        b.ln1.weight.copy_(rd(d)); b.ln1.bias.copy_(rd(d))
        b.attn.in_proj_weight.copy_(rd(3*d*d).view(3*d,d)); b.attn.in_proj_bias.copy_(rd(3*d))
        b.attn.out_proj.weight.copy_(rd(d*d).view(d,d)); b.attn.out_proj.bias.copy_(rd(d))
        b.ln2.weight.copy_(rd(d)); b.ln2.bias.copy_(rd(d))
        b.mlp[0].weight.copy_(rd(4*d*d).view(4*d,d)); b.mlp[0].bias.copy_(rd(4*d))
        b.mlp[2].weight.copy_(rd(d*4*d).view(d,4*d)); b.mlp[2].bias.copy_(rd(d))
    lnf_w=rd(d); lnf_b=rd(d); head=rd(vocab*d).view(vocab,d)
ln_f=nn.LayerNorm(d)
with torch.no_grad(): ln_f.weight.copy_(lnf_w); ln_f.bias.copy_(lnf_b)

def dump(k,x):
    row=x[0,-1].detach().float(); print(f"TORCH_LAYER {k} {float(row.sum()):.6f} {float(row.abs().max()):.6f}")

ids=torch.tensor([[b for b in PROMPT.encode()[:block]]],dtype=torch.long)
T=ids.shape[1]
with torch.no_grad():
    x = tok[ids[0]] + pos[:T]
    x = x[None,:,:]
    dump(0,x)
    mask=torch.triu(torch.full((T,T),float("-inf")),diagonal=1)
    for i in range(nlay):
        x=blocks[i](x,mask); dump(i+1,x)
    xf=ln_f(x)[0,-1]
    logits = head @ xf
print("TORCH_ARGMAX", int(logits.argmax()))
print("TORCH_MAXVAL", float(logits.max()))
print("TORCH_TOP5", " ".join(str(int(i)) for i in torch.topk(logits,5).indices))
