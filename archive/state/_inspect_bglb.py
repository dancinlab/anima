"""Inspect BG-LB substrate ckpt schema (Mac-side, no CUDA needed)."""
import torch, sys, json
P = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
try:
    payload = torch.load(P, map_location="cpu", weights_only=False)
except Exception as e:
    print("load_fail:", e)
    sys.exit(1)

if isinstance(payload, dict):
    keys = list(payload.keys())
    print("payload_keys:", keys)
    if "schema" in payload:
        print("schema:", payload["schema"])
    if "lineage_tag" in payload:
        print("lineage_tag:", payload["lineage_tag"])
    if "config" in payload:
        cfg = payload["config"]
        if isinstance(cfg, dict):
            print("config_subset:", json.dumps({k: cfg.get(k) for k in ["vocab_size","d_model","n_layers","n_heads","n_kv_heads","ctx","tie_lm_head","consciousness_dim","n_cells","lineage_tag","arch_origin"]}, indent=2))
    if "state_dict" in payload:
        sd = payload["state_dict"]
        print("n_params_keys:", len(sd))
        print("sample_keys:", list(sd.keys())[:8])
        # Check tied embedding
        tok_emb = sd.get("tok_emb.weight")
        lm_head = sd.get("lm_head.weight")
        if tok_emb is not None:
            print("tok_emb.shape:", tuple(tok_emb.shape))
        if lm_head is not None:
            print("lm_head.shape:", tuple(lm_head.shape))
        if tok_emb is not None and lm_head is not None:
            same_storage = tok_emb.data_ptr() == lm_head.data_ptr()
            cos = torch.nn.functional.cosine_similarity(tok_emb.flatten().float().unsqueeze(0), lm_head.flatten().float().unsqueeze(0)).item()
            print("tok_emb_lm_head_same_storage:", same_storage, "flat_cos:", round(cos, 4))
    if "extra" in payload:
        print("extra:", payload["extra"])
else:
    print("payload_type:", type(payload).__name__)
