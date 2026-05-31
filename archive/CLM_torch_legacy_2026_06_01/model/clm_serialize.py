#!/usr/bin/env python3
"""STAGE 4 — .clm serializer (CLM_FORMAT_SPEC v0.1).

Serializes a trained CLMConvMoE state_dict to the 2-track .clm format:
  [MAGIC "CLM\x01"][HEADER json][BLOCKS][MANIFEST json]
Each weight block carries int4-sym (AKIDA inference) + fp16 shadow (GPU resume)
+ per-output-channel qat_scale. sha256 per-block + whole-file (a_hf_complete).
"""
from __future__ import annotations
import argparse, json, hashlib, struct, os, sys, time
import torch
torch.backends.cudnn.enabled = False
_HERE = os.path.dirname(os.path.abspath(__file__))
_TRAIN = os.path.join(os.path.dirname(_HERE), "train")
for _p in (_HERE, _TRAIN):
    if _p not in sys.path: sys.path.insert(0, _p)
from model import CLMConfig, CLMConvMoE   # noqa
from train_clm import LADDER, INT4_SYM_MAX  # noqa

MAGIC = b"CLM\x01"

def sym_int4_scale(w):
    out_c = w.shape[0]
    flat = w.detach().reshape(out_c, -1)
    amax = flat.abs().amax(dim=1).clamp_min(1e-8)
    return (amax / INT4_SYM_MAX).reshape([out_c] + [1]*(w.dim()-1))

def pack_int4(q):
    """q: int tensor in [-7,7] -> packed bytes, 2 weights/byte (offset +8 -> nibble)."""
    flat = (q.reshape(-1).to(torch.int64) + 8).clamp(0,15).to(torch.uint8)
    if flat.numel() % 2: flat = torch.cat([flat, torch.zeros(1, dtype=torch.uint8)])
    hi = flat[0::2]; lo = flat[1::2]
    return bytes(((hi.to(torch.int64) << 4) | lo.to(torch.int64)).to(torch.uint8).tolist())

def serialize(ckpt, arm, rung, out_path, hf_repo, corpus_sha, inference_only=False):
    base = dict(LADDER[rung]); cfg = CLMConfig(variant=arm, **base)
    model = CLMConvMoE(cfg); sd = torch.load(ckpt, map_location="cpu"); model.load_state_dict(sd)
    dils = [cfg.dilation_base**i for i in range(cfg.n_trunk_layers)]
    header = {"version":"0.1",
      "arch":{"family":"conv-native","layers":cfg.n_trunk_layers,"width":cfg.d_model,
              "dilations":dils,"moe":{"n_experts":cfg.n_experts,"top_k":cfg.top_k,"router_d":cfg.d_model},
              "vocab":{"kind":"byte","size":cfg.vocab_size},"act_bits":4,"input_bits":8,"weights_bits":4},
      "mitosis":{"cell_pool":[{"cell_id":i,"expert_id":i,"born_step":0,"parent":None} for i in range(cfg.n_experts)],
                 "split_log_ref":None},
      "quant":{"scheme":"int4_sym","range":[-7,7],"step_formula":"2^(input_bits-act_bits)","qat":True},
      "kosmos_ptr":"CLM/corpus/clm_p1.corpus.kosmos",
      "train":{"mode":"akida-aware-qat","backprop":"gpu-fp16-master","plasticity_lane":"PLASTICITY",
               "optimizer":"adam","corpus_sha":corpus_sha}}
    blocks = []; block_meta = []
    for name, w in sd.items():
        b = {"name":name, "shape":list(w.shape)}
        if w.dim() >= 2 and "weight" in name and w.dim() <= 4:
            scale = sym_int4_scale(w)
            q = torch.clamp(torch.round(w/scale), -INT4_SYM_MAX, INT4_SYM_MAX).to(torch.int64)
            int4 = pack_int4(q)
            b["int4_sym_len"] = len(int4); b["qat_scale_len"] = scale.numel()
            blob = int4 + scale.to(torch.float32).reshape(-1).numpy().tobytes()
            if not inference_only:
                fp16 = w.to(torch.float16).numpy().tobytes()
                b["fp16_shadow_len"] = len(fp16); blob += fp16
        else:
            fp16 = w.to(torch.float16).numpy().tobytes()
            b["fp16_only_len"] = len(fp16); blob = fp16
        b["sha256"] = hashlib.sha256(blob).hexdigest(); b["blob_len"] = len(blob)
        blocks.append(blob); block_meta.append(b)
    header_b = json.dumps(header, ensure_ascii=False).encode("utf-8")
    body = b"".join(blocks)
    manifest = {"sha256":{"blocks":{bm["name"]:bm["sha256"] for bm in block_meta}},
      "blocks_meta":block_meta, "hf_repo":hf_repo, "created":time.strftime("%Y-%m-%d"),
      "rung":rung, "arm":arm, "inference_only":inference_only}
    pre = MAGIC + struct.pack("<I", len(header_b)) + header_b + body
    whole = hashlib.sha256(pre).hexdigest(); manifest["sha256"]["whole_file_pre_manifest"]=whole
    manifest_b = json.dumps(manifest, ensure_ascii=False).encode("utf-8")
    with open(out_path,"wb") as f:
        f.write(pre); f.write(struct.pack("<I", len(manifest_b))); f.write(manifest_b)
    final_sha = hashlib.sha256(open(out_path,"rb").read()).hexdigest()
    print(json.dumps({"out":out_path,"bytes":os.path.getsize(out_path),"n_blocks":len(block_meta),
        "whole_sha256":final_sha,"params":model.num_params(),"arm":arm,"rung":rung,
        "inference_only":inference_only}, indent=2))
    return final_sha

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True); ap.add_argument("--arm", required=True)
    ap.add_argument("--rung", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--hf-repo", default="dancinlab/anima-clm"); ap.add_argument("--corpus-sha", default="")
    ap.add_argument("--inference-only", action="store_true")
    a = ap.parse_args()
    serialize(a.ckpt, a.arm, a.rung, a.out, a.hf_repo, a.corpus_sha, a.inference_only)

if __name__ == "__main__": main()
