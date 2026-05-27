#!/usr/bin/env python3
# anima Mk.XII Phase 3a — gemma-2-27b INT8/4bit family-internal scale closure (alternative path 1)
# omega-blocker: gemma-27b-repeat-silent-platform-termination (3-strike fp16 fail)
# H1 hypothesis test: pre-quantized base bnb-4bit (~15.8GB vs 54GB fp16) bypass mfs throughput cap?
# raw#10 caveat: int4 vs fp16 baseline shift — measurement is on a SEPARATE axis from 2b/9b fp16
# raw#12 frozen-spec: protocol unchanged (16 prompts × stride=4 × 4 family) but quantization regime ≠ fp16 cells
import os, sys, json, time, traceback, resource

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_HOME", "/workspace/.hf_cache")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "warning")

OUT_DIR = "/workspace/out"
os.makedirs(OUT_DIR, exist_ok=True)
LOG_PATH = "/workspace/wrapper.log"
RESULT_PATH = os.path.join(OUT_DIR, "cmt_v3_gemma_2_27b_int4.json")
SUMMARY_PATH = os.path.join(OUT_DIR, "summary.json")
DISPATCH_T0 = time.time()

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def write_summary(state):
    state["wallclock_sec"] = time.time() - DISPATCH_T0
    with open(SUMMARY_PATH, "w") as f:
        json.dump(state, f, indent=2)

def excepthook(exc_type, exc_val, exc_tb):
    msg = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
    log("__GEMMA_27B_INT8_UNHANDLED__")
    log(msg)
    write_summary({
        "status": "FAIL",
        "fail_reason": "unhandled_exception",
        "exception_type": exc_type.__name__,
        "traceback": msg,
    })
    sys.exit(2)
sys.excepthook = excepthook

# Bump fd limit — xet is disabled but huggingface_hub still uses many fds for snapshot_download
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(65536, hard), hard))
    log(f"__GEMMA_27B_INT8_FD__ soft={resource.getrlimit(resource.RLIMIT_NOFILE)[0]} hard={hard}")
except Exception as e:
    log(f"fd_limit_warn={e}")

log("__GEMMA_27B_INT8_BEGIN__ model=unsloth/gemma-2-27b-bnb-4bit (pre-quantized base, ~15.8GB)")
log(f"__GEMMA_27B_INT8_ENV__ HF_HUB_DISABLE_XET={os.environ.get('HF_HUB_DISABLE_XET')} HF_HOME={os.environ.get('HF_HOME')}")

# memcg pre-flight
try:
    with open("/sys/fs/cgroup/memory.max") as f:
        memcg_max = f.read().strip()
    log(f"__GEMMA_27B_INT8_MEMCG__ max={memcg_max}")
except Exception as e:
    log(f"memcg_probe_warn={e}")

# disk pre-flight
try:
    import shutil
    du = shutil.disk_usage("/workspace")
    log(f"__GEMMA_27B_INT8_DISK__ workspace_total_gb={du.total/1e9:.1f} free_gb={du.free/1e9:.1f}")
except Exception as e:
    log(f"disk_probe_warn={e}")

# stage 1 — pre-quantized snapshot download
log("__GEMMA_27B_INT8_STAGE1_DL_BEGIN__ snapshot_download(max_workers=1)")
try:
    from huggingface_hub import snapshot_download
    t_dl_start = time.time()
    local_dir = snapshot_download(
        repo_id="unsloth/gemma-2-27b-bnb-4bit",
        max_workers=1,
        resume_download=True,
        local_dir_use_symlinks=False,
    )
    t_dl = time.time() - t_dl_start
    # measure cache size
    cache_bytes = 0
    for root, dirs, files in os.walk(local_dir):
        for f_ in files:
            try:
                cache_bytes += os.path.getsize(os.path.join(root, f_))
            except Exception:
                pass
    log(f"__GEMMA_27B_INT8_STAGE1_DL_DONE__ local_dir={local_dir} elapsed_sec={t_dl:.1f} cache_size_gb={cache_bytes/1e9:.2f}")
except Exception as e:
    log(f"__GEMMA_27B_INT8_STAGE1_DL_FAIL__ {type(e).__name__}: {e}")
    log(traceback.format_exc())
    write_summary({
        "status": "FAIL",
        "fail_reason": "snapshot_download_failed",
        "exception": str(e),
    })
    sys.exit(3)

# stage 2 — load
log("__GEMMA_27B_INT8_STAGE2_LOAD_BEGIN__")
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(local_dir)
    log("__GEMMA_27B_INT8_TOKENIZER_DONE__")

    t_load_start = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        local_dir,
        device_map="auto",
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
    )
    model.eval()
    t_load = time.time() - t_load_start
    n_layers = len(model.model.layers)
    h_dim = model.config.hidden_size
    log(f"__GEMMA_27B_INT8_LOAD_DONE__ elapsed_sec={t_load:.1f} n_layers={n_layers} h_dim={h_dim}")
except Exception as e:
    log(f"__GEMMA_27B_INT8_LOAD_FAIL__ {type(e).__name__}: {e}")
    log(traceback.format_exc())
    write_summary({
        "status": "FAIL",
        "fail_reason": "model_load_failed",
        "exception": str(e),
    })
    sys.exit(4)

# stage 3 — CMT v3 measurement (16 prompts × stride=4 × 4 family axes)
log("__GEMMA_27B_INT8_STAGE3_CMT_BEGIN__")

PROMPTS = [
    # 16 prompts (stable canonical set used by 2b/9b fp16 cells)
    "The principle of recursion states that",
    "When a system observes itself, the result is",
    "The law of identity in formal logic asserts",
    "Mathematical induction requires that",
    "A fixed point of a function f is a value where",
    "The golden ratio phi appears in",
    "The Fibonacci sequence is defined recursively as",
    "Self-reference in language creates",
    "The hexadic structure of the model rests on",
    "Phi as a constant emerges in geometry when",
    "The selfref family captures the property that",
    "Lawful behavior in a dynamical system means",
    "The hexad family characterizes",
    "Phi in the context of CMT denotes",
    "Self-reference and lawful structure interact via",
    "The relationship between hexad and phi families is",
]

FAMILIES = ["Hexad", "Law", "Phi", "SelfRef"]

# Family-axis directions (frozen-spec consistent with 2b/9b cells)
def make_family_axes(h_dim, hidden_truncated, device):
    g = torch.Generator(device="cpu").manual_seed(20260427)
    axes = {}
    for fam in FAMILIES:
        # deterministic seeded direction in first hidden_truncated dims, zero elsewhere
        v = torch.zeros(h_dim, dtype=torch.float32)
        sub = torch.randn(hidden_truncated, generator=g)
        v[:hidden_truncated] = sub
        v = v / v.norm()
        axes[fam] = v.to(device)
    return axes

HIDDEN_TRUNCATED = 128
LAYER_STRIDE = 4

device = next(model.parameters()).device
axes = make_family_axes(h_dim, HIDDEN_TRUNCATED, device)
log(f"__GEMMA_27B_INT8_AXES_BUILT__ device={device}")

# capture per-layer hidden states via output_hidden_states
tomography = {}

with torch.no_grad():
    layer_indices = list(range(0, n_layers, LAYER_STRIDE))
    log(f"__GEMMA_27B_INT8_LAYER_PLAN__ indices={layer_indices}")

    # accumulators per layer × family
    accum = {li: {fam: {"abs": [], "rel": [], "norm_dy": []} for fam in FAMILIES} for li in layer_indices}

    for pi, prompt in enumerate(PROMPTS):
        inputs = tok(prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = model(
                **inputs,
                output_hidden_states=True,
                return_dict=True,
            )
        # outputs.hidden_states: tuple length n_layers+1 (embedding + each layer's output)
        # use last token activation per layer
        for li in layer_indices:
            # hidden_states[li+1] is post-layer-li output; use index li+1 for "after layer li"
            # but to match 2b/9b protocol convention where layer 0 = pre-block, use hidden_states[li]
            h_pre = outputs.hidden_states[li][0, -1, :].float()    # (h_dim,)
            h_post = outputs.hidden_states[li + 1][0, -1, :].float()
            dy = h_post - h_pre
            norm_h = h_pre.norm().item() + 1e-8
            norm_dy = dy.norm().item() + 1e-8
            for fam in FAMILIES:
                v = axes[fam]
                proj_abs = float((dy * v).sum().item())
                proj_rel = proj_abs / norm_h
                accum[li][fam]["abs"].append(abs(proj_abs))
                accum[li][fam]["rel"].append(abs(proj_rel))
                accum[li][fam]["norm_dy"].append(norm_dy / norm_h)

        if (pi + 1) % 4 == 0:
            log(f"__GEMMA_27B_INT8_CMT_PROGRESS__ {pi+1}/16")

    # mean across prompts
    for li in layer_indices:
        tomography[str(li)] = {}
        for fam in FAMILIES:
            tomography[str(li)][fam] = {
                "abs": round(sum(accum[li][fam]["abs"]) / len(accum[li][fam]["abs"]), 6),
                "rel": round(sum(accum[li][fam]["rel"]) / len(accum[li][fam]["rel"]), 6),
                "norm_dy": round(sum(accum[li][fam]["norm_dy"]) / len(accum[li][fam]["norm_dy"]), 8),
            }

log("__GEMMA_27B_INT8_CMT_DONE__")

# rel_std / sat_frac / informative diagnostics
import math
all_rels = []
for li in layer_indices:
    for fam in FAMILIES:
        all_rels.append(tomography[str(li)][fam]["rel"])
rel_mean = sum(all_rels) / len(all_rels)
rel_var = sum((r - rel_mean) ** 2 for r in all_rels) / len(all_rels)
rel_std = math.sqrt(rel_var)
# saturation: fraction of cells where rel > 1.0 (projection magnitude > h_pre norm)
sat_frac = sum(1 for r in all_rels if r > 1.0) / len(all_rels)
informative = (rel_std > 0.005) and (sat_frac < 0.5)

cell = {
    "schema": "anima/cmt/3",
    "backbone": "unsloth/gemma-2-27b-bnb-4bit",
    "underlying_model": "google/gemma-2-27b (base, 4bit pre-quantized via bitsandbytes nf4)",
    "mode": "v3",
    "quantization": "bnb-4bit-nf4-prequantized",
    "raw_10_caveat": "int4 quantization regime — measurement is on SEPARATE axis from 2b/9b fp16 cells",
    "hook_kind": "passthrough",
    "n_probes": 16,
    "n_layers": n_layers,
    "layer_stride": LAYER_STRIDE,
    "hidden_truncated": HIDDEN_TRUNCATED,
    "h_dim": h_dim,
    "h_sqrt": round(math.sqrt(h_dim), 4),
    "ablate_target": "mlp",
    "families": FAMILIES,
    "tomography": tomography,
    "diagnostics": {
        "rel_std": round(rel_std, 6),
        "rel_mean": round(rel_mean, 6),
        "saturation_frac": round(sat_frac, 4),
        "informative": informative,
    },
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}
with open(RESULT_PATH, "w") as f:
    json.dump(cell, f, indent=2)
log(f"__GEMMA_27B_INT8_RESULT_WRITTEN__ {RESULT_PATH}")

write_summary({
    "status": "OK",
    "rel_std": cell["diagnostics"]["rel_std"],
    "saturation_frac": cell["diagnostics"]["saturation_frac"],
    "informative": cell["diagnostics"]["informative"],
    "n_layers": n_layers,
    "h_dim": h_dim,
    "result_path": RESULT_PATH,
})
log("__GEMMA_27B_INT8_OK__")
