# harness.py — extract via: awk "/^```python/,/^```$/" harness.py.md | sed "1d;\$d" > /tmp/harness.py

```python
#!/usr/bin/env python3
"""P-IDR harness — NO IDENTITY RULES short-FT ablation.

NEXT.md §7.A. 2× FT on same base + corpus: Condition A injects identity_block
prefix on every user turn; Condition B raw turns. Post-FT measurement on
identity_probe.jsonl (50 prompts × 5 categories × 5 seeds).

NOTE: anima-specific FT script integration required — this harness emits the
FT command + measurement pipeline. Actual FT execution via orchestrator
(bg_lb_engine_ag_orchestrator.hexa or equivalent) with this script's FT-spec
as input.

Usage (post-FT):
  python harness.py --ckpt-A <path> --ckpt-B <path> --outdir <out>
"""
import argparse, json, math
from pathlib import Path
from collections import defaultdict

IDENTITY_BLOCK_PATH = str(Path(__file__).parent / "identity_block.txt")
PROBE_PATH = str(Path(__file__).parent / "identity_probe.jsonl")

def load_probes(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]

def emit_ft_spec():
    """Emit FT spec for orchestrator (raw#9 hexa-only invocation)."""
    block = Path(IDENTITY_BLOCK_PATH).read_text(encoding="utf-8")
    return {
        "bg_id": "P-IDR-FT",
        "conditions": {
            "A_rules": {
                "user_turn_prefix": block,
                "system_prefix_inference": block,
            },
            "B_substrate": {
                "user_turn_prefix": "",
                "system_prefix_inference": "",
            },
        },
        "base_ckpt": "<BG-LB 350M Engine A/G base — orchestrator fills>",
        "corpus": "<anima KO native dialogue 76MB+ — orchestrator fills>",
        "ft_hparams": {
            "lr": 5e-5,
            "warmup_steps": 100,
            "total_steps": 5000,
            "batch_size": 4,
            "lora_r": 16,
            "lora_alpha": 32,
        },
        "cost_envelope_usd": [40, 80],
        "wall_estimate_hours": 12,
    }

def measure_identity_coherence(model, tok, probes, system_prefix=None, n_seeds=5, max_new=80):
    """Per-prompt 5-seed cosine similarity (intra-prompt), inter-prompt variance."""
    import torch
    intra_prompt_cos = []
    all_hidden = []
    prompt_hidden_means = []

    for probe in probes:
        per_seed_hidden = []
        for seed in range(n_seeds):
            torch.manual_seed(seed * 1000 + 7)
            if system_prefix:
                input_text = f"{system_prefix}\n사용자: {probe['prompt']}\n도우미:"
            else:
                input_text = f"사용자: {probe['prompt']}\n도우미:"
            inputs = tok(input_text, return_tensors="pt").to(model.device)
            with torch.inference_mode():
                out = model.generate(**inputs, max_new_tokens=max_new, do_sample=True, temperature=0.8, top_p=0.95, pad_token_id=tok.eos_token_id or 0, output_hidden_states=True, return_dict_in_generate=True)
            # use last layer mean over generated tokens
            last_hidden = out.hidden_states[-1][-1].mean(dim=1).squeeze(0).float().cpu()
            per_seed_hidden.append(last_hidden)
        # intra-prompt: avg pairwise cos
        cos_sims = []
        for i in range(n_seeds):
            for j in range(i+1, n_seeds):
                a, b = per_seed_hidden[i], per_seed_hidden[j]
                cos_sims.append((a @ b / (a.norm() * b.norm() + 1e-9)).item())
        intra_prompt_cos.append(sum(cos_sims)/len(cos_sims))
        # mean of 5 seeds for inter-prompt variance
        mean_h = sum(per_seed_hidden) / n_seeds
        prompt_hidden_means.append(mean_h)
        all_hidden.extend(per_seed_hidden)

    # inter-prompt variance: pairwise cos between prompt-means, look at variance
    inter_cos = []
    for i in range(len(prompt_hidden_means)):
        for j in range(i+1, len(prompt_hidden_means)):
            a, b = prompt_hidden_means[i], prompt_hidden_means[j]
            inter_cos.append((a @ b / (a.norm() * b.norm() + 1e-9)).item())
    inter_var = sum((c - sum(inter_cos)/len(inter_cos))**2 for c in inter_cos) / len(inter_cos)

    return {
        "intra_prompt_cosine_mean": sum(intra_prompt_cos) / len(intra_prompt_cos),
        "inter_prompt_variance": inter_var,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--emit-ft-spec", action="store_true", help="Emit FT spec JSON for orchestrator pickup")
    p.add_argument("--ckpt-A", help="Post-FT Condition A (rules) ckpt path")
    p.add_argument("--ckpt-B", help="Post-FT Condition B (substrate-only) ckpt path")
    p.add_argument("--outdir", default=".")
    args = p.parse_args()

    if args.emit_ft_spec:
        spec = emit_ft_spec()
        print(json.dumps(spec, ensure_ascii=False, indent=2))
        return

    if not args.ckpt_A or not args.ckpt_B:
        print("[P-IDR] post-FT measurement requires --ckpt-A and --ckpt-B (both trained ckpts)")
        print("[P-IDR] FT step: orchestrator picks up emit-ft-spec output")
        return

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    block = Path(IDENTITY_BLOCK_PATH).read_text(encoding="utf-8")
    probes = load_probes(PROBE_PATH)

    metrics = {}
    for cond_name, ckpt, sys_prefix in (("A_rules", args.ckpt_A, block), ("B_substrate", args.ckpt_B, None)):
        print(f"[P-IDR] loading {cond_name}: {ckpt}", flush=True)
        tok = AutoTokenizer.from_pretrained(ckpt)
        model = AutoModelForCausalLM.from_pretrained(ckpt, torch_dtype=torch.float16, device_map="auto")
        model.eval()
        m = measure_identity_coherence(model, tok, probes, system_prefix=sys_prefix)
        metrics[cond_name] = m
        print(f"[P-IDR] {cond_name}: intra-cos={m['intra_prompt_cosine_mean']:.3f}, inter-var={m['inter_prompt_variance']:.4f}")
        del model

    # Verdict
    A, B = metrics["A_rules"], metrics["B_substrate"]
    delta_intra = B["intra_prompt_cosine_mean"] - A["intra_prompt_cosine_mean"]
    if delta_intra >= 0.05 and B["inter_prompt_variance"] <= A["inter_prompt_variance"]:
        verdict = "EMPIRICAL_FALSIFY"
    elif abs(delta_intra) < 0.03:
        verdict = "POLICY_RETAIN"
    elif delta_intra <= -0.05:
        verdict = "REVERSE_RULES_WIN"
    else:
        verdict = "MIXED"

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "verdict.json", "w") as f:
        json.dump({"bg_id": "P-IDR", "metrics": metrics, "verdict": verdict, "delta_intra": delta_intra}, f, indent=2)
    print(f"[P-IDR] verdict: {verdict}, delta_intra(B-A)={delta_intra:.3f}")

if __name__ == "__main__":
    main()
```
