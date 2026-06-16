#!/usr/bin/env python3
"""303M-from-scratch verification — serialize the SHIPPED anima-clm-chat-303m
(state/chat_303m/h1129c_chat.pt) to the flat little-endian f32 binary that
CORE/bytegpt_decode.hexa expects, and emit torch golden next-byte logits for a
fixed prompt so the hexa CORE forward can be parity-checked byte-exact.

Reuses the EXACT serialize layout + ByteGPT block from /tmp/h1156_ref.py (the
H_1156/H_1157 mount reference). NO new metric; this is the mount-faithfulness
reproduction on the real CHAT ckpt (MODEL.md MOUNT gate).
"""
import argparse, struct, json
import torch, torch.nn as nn

class Block(nn.Module):
    def __init__(s, d, h, p=0.0):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block=block; s.n_head=n_head; s.d=d; s.n_layer=n_layer; s.vocab=vocab
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        B,T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None,:,:])
        mask = torch.triu(torch.full((T,T), float("-inf")), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))

def w(f, t):
    a = t.detach().float().contiguous().view(-1).numpy()
    f.write(a.astype('<f4').tobytes())

def serialize(m, path):
    sd = m.state_dict()
    with open(path,'wb') as f:
        f.write(struct.pack('<5I', m.vocab, m.d, m.n_layer, m.n_head, m.block))
        w(f, sd['tok.weight']); w(f, sd['pos.weight'])
        for L in range(m.n_layer):
            pre=f'blocks.{L}.'
            for k in ['ln1.weight','ln1.bias','attn.in_proj_weight','attn.in_proj_bias',
                      'attn.out_proj.weight','attn.out_proj.bias','ln2.weight','ln2.bias',
                      'mlp.0.weight','mlp.0.bias','mlp.2.weight','mlp.2.bias']:
                w(f, sd[pre+k])
        w(f, sd['ln_f.weight']); w(f, sd['ln_f.bias']); w(f, sd['tok.weight'])

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--ckpt', default='/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt')
    ap.add_argument('--prompt', default='The quick brown')
    ap.add_argument('--out', default='/tmp/verify303m/chat_full.bin')
    ap.add_argument('--steps', type=int, default=8)
    a=ap.parse_args()
    import os; os.makedirs(os.path.dirname(a.out), exist_ok=True)
    ck=torch.load(a.ckpt, map_location='cpu', weights_only=False)
    m=ByteGPT(**ck['config']); m.load_state_dict(ck['model']); m.eval()
    print('LOADED', sum(p.numel() for p in m.parameters()), 'params; config', ck['config'])
    serialize(m, a.out)
    print('SERIALIZED', a.out, os.path.getsize(a.out), 'bytes')
    ids=torch.tensor([[b for b in a.prompt.encode()[:m.block]]],dtype=torch.long)
    with torch.no_grad():
        logits=m(ids)[0,-1]
    top5=torch.topk(logits,5)
    cur=ids.clone(); gen=[]
    with torch.no_grad():
        for _ in range(a.steps):
            lg=m(cur)[0,-1]; nb=int(lg.argmax()); gen.append(nb)
            cur=torch.cat([cur,torch.tensor([[nb]])],dim=1)
            if cur.shape[1]>=m.block: break
    out={'ckpt':a.ckpt,'config':ck['config'],'prompt':a.prompt,
         'prompt_bytes':list(a.prompt.encode()),
         'last_logits_first16':[round(float(x),6) for x in logits[:16]],
         'argmax':int(logits.argmax()),
         'top5_idx':[int(i) for i in top5.indices],
         'top5_val':[round(float(v),6) for v in top5.values],
         'greedy':gen,'greedy_str':bytes(gen).decode('latin-1'),'bin':a.out}
    json.dump(out, open(a.out.replace('.bin','_golden.json'),'w'), indent=2)
    print('GOLDEN', json.dumps(out))
