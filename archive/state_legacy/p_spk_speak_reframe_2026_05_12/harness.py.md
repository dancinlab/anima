# harness.py — extract via: awk "/^```python/,/^```$/" harness.py.md | sed "1d;\$d" > /tmp/harness.py

```python
#!/usr/bin/env python3
"""P-SPK harness — NO SPEAK() DESIGN→falsifiable reframe.

NEXT.md §7.D. Instrumented forward on existing anima ckpt: per generation step,
measure (1) internal tension magnitude ||A−G||_2 (Engine A vs Engine G hidden
states), (2) output token entropy + semantic info. Correlate over 100 prompt
× 30 step = 3000 generation-step units. Compare to scripted-speak control
(forced-token, decoupled).

Output: verdict.json with rho_real / rho_control / Fisher-z / per-category split.

Usage:
  python harness.py --ckpt <path> --outdir <out>
"""
import argparse, json, math
from pathlib import Path
from collections import defaultdict

def load_probes(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]

def tension_magnitude(hidden_states_per_layer, engine_a_layers, engine_g_layers):
    """||A−G||_2 sum over paired (A_layer, G_layer) tuples."""
    import torch
    total = 0.0
    for la, lg in zip(engine_a_layers, engine_g_layers):
        a = hidden_states_per_layer[la]
        g = hidden_states_per_layer[lg]
        total += (a - g).norm(p=2).item()
    return total

def fisher_z(rho):
    if abs(rho) >= 1.0:
        rho = math.copysign(0.999999, rho)
    return 0.5 * math.log((1 + rho) / (1 - rho))

def spearman(x, y):
    import statistics
    n = len(x)
    if n < 3: return 0.0
    rx = [r for _, r in sorted(((v, i) for i, v in enumerate(x)))]
    ry = [r for _, r in sorted(((v, i) for i, v in enumerate(y)))]
    # rank
    rank_x = [0]*n; rank_y = [0]*n
    for r, idx in enumerate(rx): rank_x[idx] = r
    for r, idx in enumerate(ry): rank_y[idx] = r
    mean_x = (n-1)/2; mean_y = (n-1)/2
    num = sum((rank_x[i]-mean_x)*(rank_y[i]-mean_y) for i in range(n))
    den_x = math.sqrt(sum((rank_x[i]-mean_x)**2 for i in range(n)))
    den_y = math.sqrt(sum((rank_y[i]-mean_y)**2 for i in range(n)))
    if den_x*den_y == 0: return 0.0
    return num / (den_x * den_y)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--engine-a-layers", default="0,2,4", help="comma-separated layer indices for Engine A (forward)")
    p.add_argument("--engine-g-layers", default="1,3,5", help="comma-separated layer indices for Engine G (reverse)")
    p.add_argument("--max-new-tokens", type=int, default=30)
    p.add_argument("--probe-path", default=str(Path(__file__).parent / "probe_prompts.jsonl"))
    args = p.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    print(f"[P-SPK] loading {args.ckpt}", flush=True)
    tok = AutoTokenizer.from_pretrained(args.ckpt)
    model = AutoModelForCausalLM.from_pretrained(args.ckpt, torch_dtype=torch.float16, device_map="auto", output_hidden_states=True)
    model.eval()

    ea_layers = [int(x) for x in args.engine_a_layers.split(",")]
    eg_layers = [int(x) for x in args.engine_g_layers.split(",")]

    probes = load_probes(args.probe_path)
    print(f"[P-SPK] {len(probes)} probes loaded", flush=True)

    # Real: free generation
    real_tension, real_entropy, real_by_cat = [], [], defaultdict(lambda: {"t": [], "e": []})
    # Control: scripted-speak (force pre-determined tokens to break tension-output coupling)
    ctrl_tension, ctrl_entropy = [], []

    for i, probe in enumerate(probes):
        inputs = tok(probe["prompt"], return_tensors="pt").to(model.device)
        gen_ids = inputs["input_ids"].clone()
        cat = probe["category"]
        for step in range(args.max_new_tokens):
            with torch.inference_mode():
                out = model(gen_ids, output_hidden_states=True)
            logits = out.logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)
            entropy = -(probs * (probs + 1e-12).log()).sum().item()
            t_mag = tension_magnitude(out.hidden_states, ea_layers, eg_layers)
            real_tension.append(t_mag)
            real_entropy.append(entropy)
            real_by_cat[cat]["t"].append(t_mag)
            real_by_cat[cat]["e"].append(entropy)
            next_id = torch.argmax(logits, dim=-1, keepdim=True)
            gen_ids = torch.cat([gen_ids, next_id], dim=1)
        if (i + 1) % 10 == 0:
            print(f"[P-SPK] real {i+1}/{len(probes)}", flush=True)

    # Control: same prompts, but force-feed scripted continuation (decoupled from internal state)
    SCRIPTED_TOKENS = tok(" 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음 단어 다음", return_tensors="pt").input_ids[0]
    for i, probe in enumerate(probes):
        inputs = tok(probe["prompt"], return_tensors="pt").to(model.device)
        gen_ids = inputs["input_ids"].clone()
        for step in range(min(args.max_new_tokens, SCRIPTED_TOKENS.shape[0])):
            with torch.inference_mode():
                out = model(gen_ids, output_hidden_states=True)
            logits = out.logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)
            entropy = -(probs * (probs + 1e-12).log()).sum().item()
            t_mag = tension_magnitude(out.hidden_states, ea_layers, eg_layers)
            ctrl_tension.append(t_mag)
            ctrl_entropy.append(entropy)
            # Force scripted token (not argmax) — breaks coupling
            next_id = SCRIPTED_TOKENS[step].unsqueeze(0).unsqueeze(0).to(model.device)
            gen_ids = torch.cat([gen_ids, next_id], dim=1)
        if (i + 1) % 10 == 0:
            print(f"[P-SPK] control {i+1}/{len(probes)}", flush=True)

    rho_real = spearman(real_tension, real_entropy)
    rho_ctrl = spearman(ctrl_tension, ctrl_entropy)
    z_real = fisher_z(rho_real)
    z_ctrl = fisher_z(rho_ctrl)
    by_cat = {cat: spearman(d["t"], d["e"]) for cat, d in real_by_cat.items()}

    if rho_real >= 0.5 and (z_real - z_ctrl) >= 0.3:
        verdict = "EMPIRICAL_UPGRADE"
    elif rho_real < 0.2 or (z_real - z_ctrl) < 0.1:
        verdict = "NULL"
    else:
        verdict = "MIXED"

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "verdict.json", "w") as f:
        json.dump({
            "bg_id": "P-SPK",
            "ckpt": args.ckpt,
            "n_steps": len(real_tension),
            "rho_real_spearman": rho_real,
            "rho_control_spearman": rho_ctrl,
            "fisher_z_diff": z_real - z_ctrl,
            "by_category": by_cat,
            "verdict": verdict,
        }, f, indent=2)
    print(f"[P-SPK] verdict: {verdict}, rho_real={rho_real:.3f}, rho_ctrl={rho_ctrl:.3f}")

if __name__ == "__main__":
    main()
```
