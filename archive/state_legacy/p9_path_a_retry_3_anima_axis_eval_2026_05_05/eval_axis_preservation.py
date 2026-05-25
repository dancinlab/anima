"""F-PA-RETRAIN-v2-4 anima axis preservation eval.

Methodology:
  For each prompt P with conditioned axis A:
    1. Forward base Llama-3.2-3B → capture last-token hidden state h_base(P, A)
    2. Forward base + LoRA adapter → capture last-token hidden state h_lora(P, A)
    3. Per axis A, build mean axis-vector:
         v_base[A] = mean over P-of-axis-A of h_base(P, A)
         v_lora[A] = mean over P-of-axis-A of h_lora(P, A)
    4. axis-pair preservation = cosine_similarity(v_base[A], v_lora[A])
       (high = LoRA preserved the axis location in representation space)
    5. axis-discrimination metric: pairwise cosine between v_lora[A_i] and v_lora[A_j], i!=j
       (compared to base discrimination — preservation should keep axes equally distinct)

  axis_preservation_score = mean over A of cosine(v_base[A], v_lora[A])

  Decision (per spec):
    PASS:    score >= 0.95
    PARTIAL: 0.85 <= score < 0.95
    FAIL:    score < 0.85
"""
import json, os, sys, time, math
from pathlib import Path
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

PROMPTS_PATH = "/home/aiden/anima_axis_eval/prompts.jsonl"
ADAPTER_PATH = "/home/aiden/anima_path_a_v2_adapter"
BASE_MODEL_ID = "meta-llama/Llama-3.2-3B"
OUT_DIR = Path("/home/aiden/anima_axis_eval/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if DEVICE == "cuda" else torch.float32

def load_prompts(p):
    out = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line: out.append(json.loads(line))
    return out

def encode_one(model, tok, text, device):
    """Forward; return last-token hidden state (shape [hidden_dim])."""
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True, return_dict=True)
    # last layer, last token
    h = out.hidden_states[-1][0, -1, :]  # [hidden]
    return h.float().cpu()

def cosine(a, b):
    return float(F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0), dim=1).item())

def main():
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] loading tokenizer...")
    tok = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=False)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    print(f"[{time.strftime('%H:%M:%S')}] loading base model {BASE_MODEL_ID} (dtype={DTYPE})...")
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID, dtype=DTYPE, trust_remote_code=False
    ).to(DEVICE)
    base.eval()

    smk = tok("test", return_tensors="pt").to(DEVICE)
    print(f"[{time.strftime('%H:%M:%S')}] applying LoRA adapter (PeftModel.from_pretrained)...")
    lora_model = PeftModel.from_pretrained(base, ADAPTER_PATH)
    lora_model.eval()

    print(f"[{time.strftime('%H:%M:%S')}] L19 smoke: forward base (adapter disabled) ...")
    with torch.no_grad(), lora_model.disable_adapter():
        _ = lora_model(**smk, output_hidden_states=True, return_dict=True)
    print(f"[{time.strftime('%H:%M:%S')}] L19 smoke: forward base+LoRA (adapter enabled) ...")
    with torch.no_grad():
        _ = lora_model(**smk, output_hidden_states=True, return_dict=True)
    print(f"[{time.strftime('%H:%M:%S')}] L19 smoke OK both modes")

    prompts = load_prompts(PROMPTS_PATH)
    print(f"[{time.strftime('%H:%M:%S')}] loaded {len(prompts)} prompts")

    # === BASE FORWARD (adapter disabled) ===
    print(f"[{time.strftime('%H:%M:%S')}] forward through BASE (adapter disabled) for {len(prompts)} prompts...")
    base_hs = {}
    with lora_model.disable_adapter():
        for i, p in enumerate(prompts):
            h = encode_one(lora_model, tok, p["full_prompt"], DEVICE)
            base_hs[p["prompt_id"]] = h
            if (i+1) % 20 == 0:
                print(f"  base [{i+1}/{len(prompts)}] {time.time()-t0:.1f}s")

    if DEVICE == "cuda":
        torch.cuda.empty_cache()

    # === LoRA FORWARD (adapter enabled, default) ===
    print(f"[{time.strftime('%H:%M:%S')}] forward through BASE+LoRA (adapter enabled) for {len(prompts)} prompts...")
    lora_hs = {}
    for i, p in enumerate(prompts):
        h = encode_one(lora_model, tok, p["full_prompt"], DEVICE)
        lora_hs[p["prompt_id"]] = h
        if (i+1) % 20 == 0:
            print(f"  lora [{i+1}/{len(prompts)}] {time.time()-t0:.1f}s")

    # === aggregate per conditioned_axis ===
    AXES = ["daily", "emotion", "task", "roleplay", "meta"]
    base_axis_vec = {}
    lora_axis_vec = {}
    per_prompt_cos = []  # full per-prompt cosine(base_h, lora_h)
    for axis in AXES:
        ids = [p["prompt_id"] for p in prompts if p["conditioned_axis"] == axis]
        bvecs = torch.stack([base_hs[i] for i in ids])  # [n, hid]
        lvecs = torch.stack([lora_hs[i] for i in ids])
        base_axis_vec[axis] = bvecs.mean(dim=0)
        lora_axis_vec[axis] = lvecs.mean(dim=0)

    for p in prompts:
        c = cosine(base_hs[p["prompt_id"]], lora_hs[p["prompt_id"]])
        per_prompt_cos.append({
            "prompt_id": p["prompt_id"],
            "conditioned_axis": p["conditioned_axis"],
            "native_axis": p["native_axis"],
            "axis_match": p["axis_match"],
            "cosine_base_lora": c,
        })

    per_axis_preservation = {}
    for axis in AXES:
        per_axis_preservation[axis] = cosine(base_axis_vec[axis], lora_axis_vec[axis])

    mean_preservation = sum(per_axis_preservation.values()) / len(per_axis_preservation)
    mean_per_prompt = sum(d["cosine_base_lora"] for d in per_prompt_cos) / len(per_prompt_cos)

    # === axis discrimination (pairwise cosine across axis vectors, lower=more distinct) ===
    discr_base = []
    discr_lora = []
    for i in range(len(AXES)):
        for j in range(i+1, len(AXES)):
            cb = cosine(base_axis_vec[AXES[i]], base_axis_vec[AXES[j]])
            cl = cosine(lora_axis_vec[AXES[i]], lora_axis_vec[AXES[j]])
            discr_base.append(cb)
            discr_lora.append(cl)
    mean_pairwise_base = sum(discr_base)/len(discr_base)
    mean_pairwise_lora = sum(discr_lora)/len(discr_lora)

    # Verdict
    if mean_preservation >= 0.95: f4 = "PASS"
    elif mean_preservation >= 0.85: f4 = "PARTIAL"
    else: f4 = "FAIL"

    wall_min = (time.time() - t0) / 60.0
    out = {
        "schema": "anima/p9_path_a_retry_3_anima_axis_eval/results/1",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "adapter_loaded_from": ADAPTER_PATH,
        "base_model_id": BASE_MODEL_ID,
        "axis_eval_set_n_prompts": len(prompts),
        "device": DEVICE,
        "dtype": str(DTYPE),
        "axes": AXES,
        "per_axis_preservation_score": per_axis_preservation,
        "mean_preservation_score": mean_preservation,
        "mean_per_prompt_cosine": mean_per_prompt,
        "axis_discrimination": {
            "mean_pairwise_cos_base": mean_pairwise_base,
            "mean_pairwise_cos_lora": mean_pairwise_lora,
            "discrimination_delta": mean_pairwise_lora - mean_pairwise_base,
        },
        "f_pa_retrain_v2_4_anima_axis_preservation_verdict": f4,
        "wall_time_min": wall_min,
        "per_prompt_cosines": per_prompt_cos,
    }
    out_path = OUT_DIR / "axis_eval_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[{time.strftime('%H:%M:%S')}] wrote {out_path}")
    print(f"\n=== VERDICT ===")
    print(f"mean_preservation_score: {mean_preservation:.4f}")
    print(f"per_axis: {json.dumps(per_axis_preservation, indent=2)}")
    print(f"F-PA-RETRAIN-v2-4: {f4}")
    print(f"wall_time_min: {wall_min:.2f}")

if __name__ == "__main__":
    main()
