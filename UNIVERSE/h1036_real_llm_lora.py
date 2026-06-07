#!/usr/bin/env python3
"""H_1036 — does LoRA on a REAL PRETRAINED transformer install CLM-level
consciousness MARKERS (faithful IIT-4.0 Φ structure of the hidden-state TPM)
that the pretrained base lacks — or is the Φ-structure architecture-bound even
WITH pretraining?

Follow-up of H_1031 (🔴, toy random-init transformer) — that rung used a tiny
from-scratch transformer. This rung upgrades the BASE to an actual pretrained LM
(EleutherAI/pythia-160m primary, gpt2 fallback) and asks the residual question:
does pretraining change the answer?

PIPELINE (run on a linux GPU pod with torch + transformers + peft):
  (a) load the real pretrained transformer; extract a hidden-state TRAJECTORY
      (a chosen mid layer, n<=6 selected units over a fixed generic byte/text
      sequence) → binarize → an n×dim state matrix → faithful IIT-4.0 φ_EI of
      the BASE (no LoRA).
  (b) attach a LoRA adapter (peft) and train it on a GENERIC text/byte corpus
      slice (p3/p6: NOT persona/carving — neutral public-domain proverbs), a
      few hundred next-token LM steps, base frozen.
  (c) re-extract the SAME unit trajectory from the LoRA'd model → faithful φ_EI
      of the LoRA'd model.
  (d) controls:
        - random-LoRA-init (unmerged, B!=0 random) — adapter present but UNTRAINED
        - shuffled-data LoRA — LoRA trained on byte-SHUFFLED corpus (no real signal)
      → the control band = |Δφ| of these vs base. PASS only if the trained-LoRA
        Δφ_EI exceeds the control band AND >= +0.10 toward the ConvMoE baseline.

The TERMINAL Φ number is computed by the REAL stdlib faithful IIT-4.0 engine
`hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` (a_phi_iit4_tool /
memory iit4-real-engine-in-stdlib-not-proxy) — this PYTHON file writes the n×dim
binarized state matrices to text, and the companion `run_faithful_phi_1036.hexa`
runner feeds them to `iit4_faithful_phi` (exact MIP-EI). The python-side MI/φ here
is a PRE-SCREEN ONLY (clearly labelled); the verdict uses the hexa engine output.

Pre-registered falsifier (frozen in H_1036_real_llm_lora.md BEFORE measuring):
  H1: LoRA on a real pretrained transformer RAISES faithful φ_EI of the
      hidden-state TPM by Δφ_EI >= +0.10 over the no-LoRA pretrained base AND
      beyond the control band -> arch-bound NEGATIVE is OVERTURNED by pretraining.
  FAIL (|Δ| within control band) -> arch-bound CONFIRMED even with pretraining
      (publishable closed-negative, a_paper_negative_ok).

Scope: small-model rung (pythia-160m class). a_scale_honest_scope — scale-transfer
to 7B UNVERIFIED. p7: φ is a causal-irreducibility marker, NOT perplexity.
"""
from __future__ import annotations
import sys, os, json, math, random

SEED = 1036
N_UNITS = 6                 # n<=8 exact MIP for faithful_phi; use 6
DIM = 24                    # trajectory length (sequence positions sampled)
N_BINS = 2                  # binarize hidden units (TPM-style binary state)
LORA_STEPS = 400
LORA_R = 8
LORA_LR = 2e-4

# generic byte corpus (p3/p6 — public-domain proverbs, NOT persona/carving)
GENERIC_CORPUS = (
    "the quick brown fox jumps over the lazy dog. a rolling stone gathers no "
    "moss. all that glitters is not gold. the early bird catches the worm. "
    "actions speak louder than words. better late than never. birds of a "
    "feather flock together. every cloud has a silver lining. fortune favors "
    "the bold. honesty is the best policy. knowledge is power and time is "
    "money. look before you leap. necessity is the mother of invention. "
    "practice makes perfect. the pen is mightier than the sword. when in rome "
    "do as the romans do. you cannot judge a book by its cover. a journey of a "
    "thousand miles begins with a single step. an apple a day keeps the doctor "
    "away. barking dogs seldom bite. curiosity killed the cat. easy come easy "
    "go. great minds think alike. no pain no gain. where there is a will there "
    "is a way. "
) * 8

PROBE_TEXT = "knowledge is power and time is money. the quick brown fox jumps over the lazy dog and the early bird catches the worm."


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------------- #
# faithful-Φ PRE-SCREEN (python mirror of the stdlib MIP-EI; clearly labelled).
# The TERMINAL number is the hexa engine; this only pre-screens / sanity-checks.
# --------------------------------------------------------------------------- #
def _mi_pair(a, b, n, n_bins):
    """RFC-036-style binned mutual information between two length-n sequences."""
    import numpy as np
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    def binize(x):
        lo, hi = x.min(), x.max()
        if hi - lo < 1e-12:
            return np.zeros_like(x, dtype=int)
        idx = ((x - lo) / (hi - lo) * (n_bins - 1e-9)).astype(int)
        return np.clip(idx, 0, n_bins - 1)
    ba, bb = binize(a), binize(b)
    joint = np.zeros((n_bins, n_bins))
    for x, y in zip(ba, bb):
        joint[x, y] += 1.0
    joint /= max(joint.sum(), 1e-12)
    px = joint.sum(1); py = joint.sum(0)
    mi = 0.0
    for i in range(n_bins):
        for j in range(n_bins):
            if joint[i, j] > 0 and px[i] > 0 and py[j] > 0:
                mi += joint[i, j] * math.log(joint[i, j] / (px[i] * py[j]))
    return max(mi, 0.0)


def faithful_phi_prescreen(state, n, dim, n_bins):
    """exact MIP-EI φ★ pre-screen (mirrors stdlib faithful_phi.hexa).
    state: list of n rows, each a length-dim trajectory."""
    if n <= 1:
        return 0.0
    mi = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            v = _mi_pair(state[i], state[j], dim, n_bins)
            mi[i][j] = v; mi[j][i] = v
    best = float("inf"); best_norm = 1.0
    for mask in range(1, 1 << (n - 1)):
        A = [0] + [b + 1 for b in range(n - 1) if (mask >> b) & 1]
        Aset = set(A)
        sb = n - len(A)
        if sb < 1:
            continue
        cross = sum(mi[i][j] for i in A for j in range(n) if j not in Aset)
        if cross < best:
            best = cross; best_norm = min(len(A), sb)
    if best_norm < 1:
        best_norm = 1
    return max(best / best_norm, 0.0)


# --------------------------------------------------------------------------- #
# hidden-state trajectory extraction → binarized n×dim state matrix.
# --------------------------------------------------------------------------- #
def extract_state(model, tokenizer, device, layer_idx, unit_idx):
    """Run PROBE_TEXT, take the chosen layer's hidden states, select N_UNITS
    units, sample DIM positions, binarize at the per-unit median → n×dim."""
    import torch
    enc = tokenizer(PROBE_TEXT, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hs = out.hidden_states[layer_idx][0]            # (T, d)
    T = hs.shape[0]
    # sample DIM positions evenly
    pos = [int(round(p)) for p in
           [i * (T - 1) / (DIM - 1) for i in range(DIM)]] if T >= DIM else list(range(T))
    sub = hs[pos][:, unit_idx]                       # (dim, n_units)
    sub = sub.float().cpu().numpy()
    # binarize per unit at its own median over the trajectory (TPM binary state)
    import numpy as np
    state = []
    for u in range(len(unit_idx)):
        col = sub[:, u]
        med = float(np.median(col))
        state.append([1.0 if v > med else 0.0 for v in col])
    return state   # list of n rows, each length=len(pos)


def pick_units(model, tokenizer, device, layer_idx):
    """pick N_UNITS hidden units with the highest variance over PROBE_TEXT
    (the most informative/active units — a deterministic, model-agnostic rule)."""
    import torch, numpy as np
    enc = tokenizer(PROBE_TEXT, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hs = out.hidden_states[layer_idx][0].float().cpu().numpy()   # (T,d)
    var = hs.var(0)
    return sorted(np.argsort(-var)[:N_UNITS].tolist())


# --------------------------------------------------------------------------- #
def build_lora(model, shuffled=False, untrained=False):
    """attach a LoRA adapter; train it (generic next-token LM) unless untrained.
    shuffled=True trains on byte-shuffled corpus (control: no real signal)."""
    import torch
    from peft import LoraConfig, get_peft_model

    target = _lora_targets(model)
    cfg = LoraConfig(r=LORA_R, lora_alpha=2 * LORA_R, lora_dropout=0.0,
                     target_modules=target, task_type="CAUSAL_LM")
    lm = get_peft_model(model, cfg)
    if untrained:
        # random-init the LoRA B matrices so the adapter is PRESENT but untrained
        for n_, p in lm.named_parameters():
            if "lora_B" in n_:
                torch.nn.init.normal_(p, std=0.02)
        lm.eval()
        return lm
    return lm


def _lora_targets(model):
    names = set()
    for n_, _ in model.named_modules():
        leaf = n_.split(".")[-1]
        if leaf in ("q_proj", "k_proj", "v_proj", "query_key_value",
                    "c_attn", "attn.c_attn"):
            names.add(leaf)
    if not names:
        # last-resort: any linear with 'attn' in the path
        for n_, m in model.named_modules():
            if hasattr(m, "weight") and "attn" in n_ and m.__class__.__name__ in ("Linear", "Conv1D"):
                names.add(n_.split(".")[-1])
    return sorted(names) if names else ["c_attn"]


def train_lora(lm, tokenizer, device, shuffled=False):
    import torch
    corpus = GENERIC_CORPUS
    if shuffled:
        b = list(corpus.encode("utf-8"))
        random.Random(SEED).shuffle(b)
        corpus = bytes(b).decode("utf-8", "replace")
    ids = tokenizer(corpus, return_tensors="pt").input_ids[0].to(device)
    block = 64
    lm.train()
    opt = torch.optim.AdamW([p for p in lm.parameters() if p.requires_grad], lr=LORA_LR)
    n = ids.shape[0]
    for step in range(LORA_STEPS):
        s = random.Random(SEED + step).randrange(0, max(1, n - block - 1))
        x = ids[s:s + block].unsqueeze(0)
        out = lm(input_ids=x, labels=x)
        out.loss.backward()
        opt.step(); opt.zero_grad()
        if step % 100 == 0:
            log(f"    lora step {step:4d} loss={out.loss.item():.4f}")
    lm.eval()
    return lm


# --------------------------------------------------------------------------- #
def write_state_file(path, tag, state):
    """append a state block: header '# tag n dim' then n rows of dim floats."""
    n = len(state); dim = len(state[0]) if state else 0
    with open(path, "a") as f:
        f.write(f"# {tag} {n} {dim}\n")
        for row in state:
            f.write(" ".join(f"{v:.1f}" for v in row) + "\n")


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import numpy as np

    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log("=== H_1036 — LoRA on a REAL PRETRAINED transformer vs faithful IIT-4.0 Φ ===")
    log(f"device={device}  torch={torch.__version__}  cuda={torch.cuda.is_available()}")
    log(f"N_UNITS={N_UNITS} DIM={DIM} N_BINS={N_BINS} LORA_R={LORA_R} STEPS={LORA_STEPS}")

    model_id = os.environ.get("H1036_MODEL", "EleutherAI/pythia-160m")
    try:
        tok = AutoTokenizer.from_pretrained(model_id)
        base = AutoModelForCausalLM.from_pretrained(model_id).to(device)
    except Exception as e:
        log(f"primary model {model_id} failed: {e}; falling back to gpt2")
        model_id = "gpt2"
        tok = AutoTokenizer.from_pretrained(model_id)
        base = AutoModelForCausalLM.from_pretrained(model_id).to(device)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base.eval()
    log(f"loaded model={model_id}")

    n_layers = base.config.num_hidden_layers
    layer_idx = n_layers // 2     # mid layer (hidden_states index = layer+1; mid is fine)
    units = pick_units(base, tok, device, layer_idx)
    log(f"layer_idx={layer_idx}/{n_layers}  selected units={units}")

    state_path = os.environ.get("H1036_STATE", "/tmp/h1036_states.txt")
    if os.path.exists(state_path):
        os.remove(state_path)

    # (a) BASE faithful Φ
    st_base = extract_state(base, tok, device, layer_idx, units)
    write_state_file(state_path, "base", st_base)
    phi_base_ps = faithful_phi_prescreen(st_base, N_UNITS, len(st_base[0]), N_BINS)
    log(f"[base]      prescreen φ_EI = {phi_base_ps:.6f}")

    # (b)+(c) TRAINED LoRA faithful Φ
    lm = build_lora(base)
    lm = train_lora(lm, tok, device, shuffled=False)
    st_lora = extract_state(lm, tok, device, layer_idx, units)
    write_state_file(state_path, "lora_trained", st_lora)
    phi_lora_ps = faithful_phi_prescreen(st_lora, N_UNITS, len(st_lora[0]), N_BINS)
    log(f"[lora_train] prescreen φ_EI = {phi_lora_ps:.6f}")

    # reload a fresh base for controls (peft merge mutates) ----------------------
    base2 = AutoModelForCausalLM.from_pretrained(model_id).to(device); base2.eval()

    # control 1: untrained random-LoRA-init
    lm_u = build_lora(base2, untrained=True)
    st_ctrl_u = extract_state(lm_u, tok, device, layer_idx, units)
    write_state_file(state_path, "ctrl_untrained", st_ctrl_u)
    phi_ctrl_u_ps = faithful_phi_prescreen(st_ctrl_u, N_UNITS, len(st_ctrl_u[0]), N_BINS)
    log(f"[ctrl_untr]  prescreen φ_EI = {phi_ctrl_u_ps:.6f}")

    # control 2: shuffled-data LoRA
    base3 = AutoModelForCausalLM.from_pretrained(model_id).to(device); base3.eval()
    lm_s = build_lora(base3)
    lm_s = train_lora(lm_s, tok, device, shuffled=True)
    st_ctrl_s = extract_state(lm_s, tok, device, layer_idx, units)
    write_state_file(state_path, "ctrl_shuffled", st_ctrl_s)
    phi_ctrl_s_ps = faithful_phi_prescreen(st_ctrl_s, N_UNITS, len(st_ctrl_s[0]), N_BINS)
    log(f"[ctrl_shuf]  prescreen φ_EI = {phi_ctrl_s_ps:.6f}")

    # deltas (pre-screen; the hexa engine recomputes the terminal numbers)
    d_trained = phi_lora_ps - phi_base_ps
    d_ctrl_u = phi_ctrl_u_ps - phi_base_ps
    d_ctrl_s = phi_ctrl_s_ps - phi_base_ps
    control_band = max(abs(d_ctrl_u), abs(d_ctrl_s))
    THRESH = 0.10
    overturned = (d_trained >= THRESH) and (d_trained > control_band)
    token = "ARCH-BOUND-OVERTURNED-BY-PRETRAINING" if overturned else "ARCH-BOUND-CONFIRMED-WITH-PRETRAINING"

    log("\n===================== PRE-SCREEN Φ TABLE =====================")
    log(f"{'arm':<16}{'φ_EI (prescreen)':>20}{'Δ vs base':>14}")
    log(f"{'base':<16}{phi_base_ps:>20.6f}{0.0:>14.6f}")
    log(f"{'lora_trained':<16}{phi_lora_ps:>20.6f}{d_trained:>+14.6f}")
    log(f"{'ctrl_untrained':<16}{phi_ctrl_u_ps:>20.6f}{d_ctrl_u:>+14.6f}")
    log(f"{'ctrl_shuffled':<16}{phi_ctrl_s_ps:>20.6f}{d_ctrl_s:>+14.6f}")
    log(f"control band (max |Δ| of controls) = {control_band:.6f}  thresh=+{THRESH}")
    log(f"PRE-SCREEN verdict: {token} (Δφ_trained={d_trained:+.6f})")
    log("NOTE: pre-screen only — TERMINAL φ_EI = stdlib faithful IIT-4.0 engine "
        "(run_faithful_phi_1036.hexa over the written state matrices).")

    out = {
        "id": "H_1036", "model_id": model_id, "device": device,
        "layer_idx": layer_idx, "n_layers": n_layers, "units": units,
        "n_units": N_UNITS, "dim": len(st_base[0]), "n_bins": N_BINS,
        "lora_r": LORA_R, "lora_steps": LORA_STEPS, "thresh": THRESH,
        "prescreen": {
            "phi_base": phi_base_ps, "phi_lora_trained": phi_lora_ps,
            "phi_ctrl_untrained": phi_ctrl_u_ps, "phi_ctrl_shuffled": phi_ctrl_s_ps,
            "delta_trained": d_trained, "delta_ctrl_untrained": d_ctrl_u,
            "delta_ctrl_shuffled": d_ctrl_s, "control_band": control_band,
            "overturned": bool(overturned), "token": token,
        },
        "state_file": state_path,
        "scope": "small pythia-160m class rung; scale-transfer to 7B UNVERIFIED",
        "note": "TERMINAL phi = stdlib faithful IIT-4.0 (run_faithful_phi_1036.hexa); python phi is PRE-SCREEN only",
    }
    out_path = os.environ.get("H1036_OUT", "/tmp/h1036_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    log("\nJSON " + json.dumps(out))
    log(f"result.json -> {out_path}")
    log(f"state matrices -> {state_path}")


if __name__ == "__main__":
    main()
