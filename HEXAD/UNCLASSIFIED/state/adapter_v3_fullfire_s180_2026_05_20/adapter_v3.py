"""§180 ADAPTER v3 model — 16-Q-Former + small transformer + 5-channel readout.

Architecture (from §179 winner + ADAPTER.md v3 spec):
  bytes → byte_emb → 16-Q-Former cross-attn → small transformer → ln_f
       → (5-channel readout head)  (anchor classification head)

§7 ① ② ③ all PASS: from-scratch, no pretrained, no external graft.
"""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class AdapterV3(nn.Module):
    def __init__(self, vocab_size=256, d_model=192, n_query=16,
                 n_layer=4, n_head=6, n_anchors=35, max_seq_len=128,
                 n_modalities=4):
        super().__init__()
        self.d_model = d_model
        self.n_query = n_query
        self.byte_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)

        # 16-query Q-Former (mini, §179 winner)
        self.query_tokens = nn.Parameter(torch.randn(n_query, d_model) * 0.02)
        self.qf_kv = nn.Linear(d_model, d_model * 2)
        self.qf_proj = nn.Linear(d_model, d_model)
        self.qf_ln = nn.LayerNorm(d_model)

        # small transformer (anima byte-LM proxy)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_head, dim_feedforward=d_model * 4,
            batch_first=True, dropout=0.0, activation="gelu", norm_first=True,
        )
        self.transformer = nn.TransformerEncoder(enc_layer, num_layers=n_layer)
        self.ln_f = nn.LayerNorm(d_model)

        # 5-channel TENSION-LINK readout (anima self-report)
        # (concept / context / meaning / authenticity / sender)
        self.readout_5ch = nn.Linear(d_model, 5)

        # anchor classification head (35-class)
        self.anchor_head = nn.Linear(d_model, n_anchors)

        # modality classification head (4-class image/audio/video/tension)
        self.modality_head = nn.Linear(d_model, n_modalities)

    def forward(self, x):
        """x: [B, T] byte ids → (anchor_logits [B, 35], readout_5 [B, 5], modality_logits [B, 4])"""
        B, T = x.shape
        pos = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
        e = self.byte_emb(x) + self.pos_emb(pos)  # [B, T, d]

        # mini-Q-Former cross-attention
        kv = self.qf_kv(e)
        k, v = kv.chunk(2, dim=-1)  # [B, T, d] each
        q = self.query_tokens.unsqueeze(0).expand(B, -1, -1)  # [B, 16, d]
        attn = F.softmax(q @ k.transpose(-2, -1) / math.sqrt(self.d_model), dim=-1)
        latent = q + attn @ v  # residual
        latent = self.qf_ln(self.qf_proj(latent))  # [B, 16, d]

        # small transformer over 16 latent tokens
        h = self.transformer(latent)
        h = self.ln_f(h)
        pooled = h.mean(dim=1)  # [B, d]

        # readouts
        readout_5 = torch.sigmoid(self.readout_5ch(pooled))  # [B, 5] ∈ [0,1]
        anchor_logits = self.anchor_head(pooled)  # [B, 35]
        modality_logits = self.modality_head(pooled)  # [B, 4]

        return anchor_logits, readout_5, modality_logits


def adapter_v3_param_count(d_model=192, n_layer=4, n_head=6):
    m = AdapterV3(d_model=d_model, n_layer=n_layer, n_head=n_head)
    return sum(p.numel() for p in m.parameters())


if __name__ == "__main__":
    m = AdapterV3()
    n = sum(p.numel() for p in m.parameters())
    print("AdapterV3 params:", n)
    x = torch.randint(0, 256, (4, 128))
    a, r5, ml = m(x)
    print("anchor_logits:", a.shape, "readout_5:", r5.shape, "modality_logits:", ml.shape)
