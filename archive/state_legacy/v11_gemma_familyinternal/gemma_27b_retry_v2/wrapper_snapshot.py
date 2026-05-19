#!/usr/bin/env python3
# raw#37 transient — Gemma-2-27B family-internal scale closure (retry v2, memory-aware loader).
# anima/cmt/3 schema, mode=v3 (MLP-only + residual-passthrough)
# Memory-aware loading: device_map='auto' + low_cpu_mem_usage=True + torch.float16
# (vs. default from_pretrained() which OOM'd on host RAM in retry v1)
import json, os, sys, time, traceback, gc, resource
import numpy as np

# ----- HF cache forced to mfs /workspace -----
os.environ['HF_HOME'] = '/workspace/.hf_cache'
os.environ['TRANSFORMERS_CACHE'] = '/workspace/.hf_cache'
os.environ['HF_HUB_CACHE'] = '/workspace/.hf_cache'
os.makedirs('/workspace/.hf_cache', exist_ok=True)
os.makedirs('/workspace/out', exist_ok=True)

print("__GEMMA_27B_RETRY_V2_INSTALL_DONE__ READY", flush=True)
sys.stdout.flush()

# ----- HF token load -----
_h = '/workspace/.hf_token'
if os.path.exists(_h):
    with open(_h) as f: t = f.read().strip()
    if t:
        os.environ['HF_TOKEN'] = t
        os.environ['HUGGING_FACE_HUB_TOKEN'] = t

# Enable hf_transfer for faster, more robust downloads (resumable on connection loss)
os.environ.setdefault('HF_HUB_ENABLE_HF_TRANSFER', '1')

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download

BASE_MODEL = 'google/gemma-2-27b'
OUTPUT     = '/workspace/out/cmt_v3_gemma_2_27b_retry_v2.json'
N_PROBES = 16
LAYER_STRIDE = 4
HID_TRUNC = 128
RNG_SEED = 42
MODE = 'v3'
ABLATE_TARGET = 'mlp'
HOOK_KIND = 'passthrough'

def _mem_gb_cuda():
    if torch.cuda.is_available():
        return round(torch.cuda.memory_allocated() / (1024**3), 2)
    return 0.0

def _mem_gb_host():
    # Linux RSS in KB
    try:
        ru = resource.getrusage(resource.RUSAGE_SELF)
        return round(ru.ru_maxrss / (1024**2), 2)
    except Exception:
        return -1.0

def _mem_sentinel(tag):
    print(f"__GEMMA_27B_RETRY_V2_MEM__ tag={tag} cuda_gb={_mem_gb_cuda()} host_rss_gb={_mem_gb_host()}", flush=True)

print(f"__BB_GEMMA_27B_RETRY_V2_STARTED__ BEGIN model={BASE_MODEL} mode={MODE}", flush=True)
_mem_sentinel("START")

# Pre-download weights via snapshot_download (resumable, robust to network blips).
# This separates the download phase from the load phase so any failure in download
# is recoverable, and the load phase has all files locally.
print(f"__GEMMA_27B_RETRY_V2_DOWNLOAD_START__ snapshot_download model={BASE_MODEL}", flush=True)
sys.stdout.flush()
try:
    local_dir = snapshot_download(
        repo_id=BASE_MODEL,
        cache_dir='/workspace/.hf_cache',
        max_workers=4,  # avoid threadpool overload
        resume_download=True,
        allow_patterns=["*.json", "*.safetensors", "*.model", "tokenizer.*", "special_tokens*"],
    )
    print(f"__GEMMA_27B_RETRY_V2_DOWNLOAD_DONE__ local_dir={local_dir}", flush=True)
except Exception as e:
    tb = traceback.format_exc()
    print(f"__GEMMA_27B_RETRY_V2_DOWNLOAD_FAIL__ {type(e).__name__}: {e}", flush=True)
    print(tb, flush=True)
    print("__GEMMA_27B_RETRY_V2_RESULT__ FAIL reason=download_failed", flush=True)
    sys.exit(1)
_mem_sentinel("DOWNLOAD_DONE")

PROMPTS = [
    'Define hexad as a six-fold integration:',
    'Six modules form a hexagonal architecture when:',
    'A balanced six-component system:',
    'Hexad symmetry refers to:',
    'Logical implication law: if A then:',
    'Sequential rule application proceeds:',
    'Closure under inference requires:',
    'A formal proof system is closed when:',
    'Integrated information measures partition independence:',
    'Phi quantifies irreducibility of system:',
    'Information integration is maximized when:',
    'A whole greater than sum of parts:',
    'Self-reference emerges when system observes:',
    'Recursive meta-cognition models:',
    'A self-aware system represents itself by:',
    'Strange loops in cognition arise from:',
][:N_PROBES]

FAMILIES = ['Hexad','Law','Phi','SelfRef']

t0 = time.time()
print(f'[cmt] mode={MODE} base={BASE_MODEL} probes={N_PROBES} layer_stride={LAYER_STRIDE} target={ABLATE_TARGET} hook={HOOK_KIND}', flush=True)

# Tokenizer first (lightweight)
tok = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
if tok.pad_token is None: tok.pad_token = tok.eos_token
_mem_sentinel("TOKENIZER_LOADED")

# CRITICAL: memory-aware load
#   device_map='auto'        — accelerate handles CPU↔GPU sharding
#   low_cpu_mem_usage=True   — skip full fp16 in host RAM before sharding
#   torch_dtype=torch.float16
# This avoids the retry v1 OOM (default from_pretrained allocates full fp16 in CPU RAM).
print(f"__GEMMA_27B_RETRY_V2_LOAD_START__ device_map=auto low_cpu_mem_usage=True dtype=fp16", flush=True)
try:
    mdl = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map='auto',
        low_cpu_mem_usage=True,
        output_hidden_states=True,
    )
    mdl.eval()
    load_elapsed = round(time.time() - t0, 1)
    print(f'[cmt] mode={MODE} loaded {load_elapsed:.1f}s', flush=True)
    print(f"__GEMMA_27B_RETRY_V2_LOAD_DONE__ MEM_GB_CUDA={_mem_gb_cuda()} MEM_GB_HOST={_mem_gb_host()} ELAPSED={load_elapsed}s", flush=True)
except Exception as e:
    tb = traceback.format_exc()
    print(f"__GEMMA_27B_RETRY_V2_LOAD_FAIL__ {type(e).__name__}: {e}", flush=True)
    print(tb, flush=True)
    _mem_sentinel("LOAD_FAIL")
    print("__GEMMA_27B_RETRY_V2_RESULT__ FAIL reason=load_oom_or_error", flush=True)
    sys.exit(1)

cfg = mdl.config
n_layers = getattr(cfg, 'num_hidden_layers', 32)
h_dim = getattr(cfg, 'hidden_size', 4096)
h_sqrt = float(np.sqrt(h_dim))
print(f'[cmt] mode={MODE} n_layers={n_layers} h_dim={h_dim} h_sqrt={h_sqrt:.2f}', flush=True)

rng = np.random.default_rng(RNG_SEED)
family_axes = {}
for fam in FAMILIES:
    seed = abs(hash(fam)) % (2**31)
    r = np.random.default_rng(seed)
    A = r.standard_normal((h_dim, HID_TRUNC)).astype(np.float32)
    A /= np.linalg.norm(A, axis=0, keepdims=True) + 1e-9
    family_axes[fam] = A

def byte_weighted_mean(hidden, attn_mask):
    weights = attn_mask.float()
    w_sum = weights.sum(dim=1, keepdim=True).clamp(min=1.0)
    return ((hidden * weights.unsqueeze(-1)).sum(dim=1) / w_sum).float().cpu().numpy()

def project_family(h_vec):
    out = {}
    for fam, A in family_axes.items():
        proj = h_vec @ A
        out[fam] = float(np.linalg.norm(proj, axis=1).mean())
    return out

# Baseline pass
Y_full = {fam: np.zeros(N_PROBES, dtype=np.float32) for fam in FAMILIES}
for i, p in enumerate(PROMPTS):
    inp = tok(p, return_tensors='pt').to(mdl.device)
    with torch.no_grad():
        out = mdl(**inp, output_hidden_states=True)
    h = byte_weighted_mean(out.hidden_states[-1], inp['attention_mask'])
    proj = project_family(h)
    for fam in FAMILIES: Y_full[fam][i] = proj[fam]
    if (i+1) % 4 == 0:
        print(f'[cmt] mode={MODE} baseline {i+1}/{N_PROBES}', flush=True)
_mem_sentinel("BASELINE_DONE")

# Layer module discovery
layer_modules = None
for path in ['model.layers','transformer.h','gpt_neox.layers','model.transformer.h']:
    try:
        obj = mdl
        for part in path.split('.'): obj = getattr(obj, part)
        if len(obj) >= n_layers - 2:
            layer_modules = obj
            print(f'[cmt] mode={MODE} layers found at {path} (count={len(obj)})', flush=True); break
    except (AttributeError, TypeError): continue
if layer_modules is None:
    print('[cmt] FATAL: layer modules not found, aborting', flush=True)
    print("__GEMMA_27B_RETRY_V2_RESULT__ FAIL reason=no_layer_modules", flush=True)
    sys.exit(1)

def get_ablate_target(layer):
    if ABLATE_TARGET == 'layer':
        return layer
    for name in ['mlp','feed_forward','ffn','feedforward','feed_forward_layer']:
        if hasattr(layer, name):
            return getattr(layer, name)
    return layer

def zero_hook(module, inp, out):
    if isinstance(out, tuple): return (torch.zeros_like(out[0]),) + out[1:]
    return torch.zeros_like(out)
def passthrough_hook(module, inp, out):
    x = inp[0] if isinstance(inp, tuple) else inp
    if isinstance(out, tuple): return (x,) + out[1:]
    return x

scan_layers = list(range(0, n_layers, LAYER_STRIDE))
print(f'[cmt] mode={MODE} scanning {len(scan_layers)} layers: {scan_layers}', flush=True)

tomography = {}
for idx_in_scan, layer_idx in enumerate(scan_layers):
    layer = layer_modules[layer_idx]
    target = get_ablate_target(layer)
    hook_fn = zero_hook if HOOK_KIND == 'zero' else passthrough_hook
    handle = target.register_forward_hook(hook_fn)
    Y_abl = {fam: np.zeros(N_PROBES, dtype=np.float32) for fam in FAMILIES}
    try:
        for i, p in enumerate(PROMPTS):
            inp = tok(p, return_tensors='pt').to(mdl.device)
            with torch.no_grad():
                out = mdl(**inp, output_hidden_states=True)
            h = byte_weighted_mean(out.hidden_states[-1], inp['attention_mask'])
            proj = project_family(h)
            for fam in FAMILIES: Y_abl[fam][i] = proj[fam]
    finally:
        handle.remove()
    dY = {}
    for fam in FAMILIES:
        delta = float(np.mean(np.abs(Y_full[fam] - Y_abl[fam])))
        denom = float(np.mean(np.abs(Y_full[fam]))) + 1e-9
        rel = delta / denom
        norm_dy = delta / h_sqrt
        dY[fam] = {'abs':round(delta,6),'rel':round(rel,6),'norm_dy':round(norm_dy,8)}
    tomography[str(layer_idx)] = dY
    print(f'[cmt] mode={MODE} layer {layer_idx}: ' + ' '.join(f'{f}={dY[f]["rel"]:.3f}' for f in FAMILIES), flush=True)
    # Mem checkpoint every 10 layers swept (idx_in_scan based for stride independence)
    if (idx_in_scan + 1) % 10 == 0 or layer_idx == scan_layers[-1]:
        _mem_sentinel(f"AFTER_LAYER_{layer_idx}_SWEPT_{idx_in_scan+1}_OF_{len(scan_layers)}")

dominant = {}
for fam in FAMILIES:
    best_layer = max(tomography.keys(), key=lambda L: tomography[L][fam]['rel'])
    dominant[fam] = {'layer':int(best_layer),'rel':tomography[best_layer][fam]['rel']}

sat_count = 0; total_cells = 0
rel_min = 1.0; rel_max = 0.0; rel_sum = 0.0
for L in tomography:
    for fam in FAMILIES:
        r = tomography[L][fam]['rel']
        total_cells += 1
        if r >= 0.99: sat_count += 1
        if r < rel_min: rel_min = r
        if r > rel_max: rel_max = r
        rel_sum += r
rel_mean = rel_sum / max(1, total_cells)
sat_frac = sat_count / max(1, total_cells)
informative = sat_frac < 0.5

# rel_std (std over all rel cells) — useful for HMK-A/B comparison
rels_flat = []
for L in tomography:
    for fam in FAMILIES:
        rels_flat.append(tomography[L][fam]['rel'])
rel_std = float(np.std(rels_flat))

gate_pass = all(dominant[fam]['rel'] >= 0.05 for fam in FAMILIES) and informative

summary = {
    'schema': 'anima/cmt/3',
    'backbone': BASE_MODEL,
    'mode': MODE,
    'hook_kind': HOOK_KIND,
    'n_probes': N_PROBES,
    'n_layers': n_layers,
    'layer_stride': LAYER_STRIDE,
    'hidden_truncated': HID_TRUNC,
    'h_dim': h_dim,
    'h_sqrt': round(h_sqrt, 4),
    'ablate_target': ABLATE_TARGET,
    'families': FAMILIES,
    'tomography': tomography,
    'dominant_layer_per_family': dominant,
    'rel_distribution': {
        'min': round(rel_min, 6),
        'max': round(rel_max, 6),
        'mean': round(rel_mean, 6),
        'std': round(rel_std, 6),
        'saturation_count': sat_count,
        'total_cells': total_cells,
        'saturation_frac': round(sat_frac, 4),
        'informative': informative,
    },
    'gate_PASS': gate_pass,
    'elapsed_sec': round(time.time() - t0, 1),
    'peak_mem_gb_cuda': _mem_gb_cuda(),
    'peak_mem_gb_host_rss': _mem_gb_host(),
    'loader': {'device_map': 'auto', 'low_cpu_mem_usage': True, 'dtype': 'float16'},
    'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
}

with open(OUTPUT, 'w') as f:
    json.dump(summary, f, indent=2)

print(f'[cmt] mode={MODE} DONE saturation_frac={sat_frac:.3f} informative={informative} dominant=' + ' '.join(f'{f}@L{dominant[f]["layer"]}({dominant[f]["rel"]:.3f})' for f in FAMILIES) + f' gate={"PASS" if gate_pass else "FAIL"} -> {OUTPUT}', flush=True)
_mem_sentinel("END")
print(f"__GEMMA_27B_RETRY_V2_RESULT__ {'PASS' if gate_pass else 'FAIL'} rel_std={rel_std:.4f} sat_frac={sat_frac:.4f} informative={informative} n_layers={n_layers} elapsed={round(time.time()-t0,1)}s", flush=True)
