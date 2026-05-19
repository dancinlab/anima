#!/usr/bin/env python3
# anima axis 96 disambiguation Step 1 — Llama-3.1-8B fp16 stride=1 full layer scan
# Goal: HFD-A (LIVING_AXIS) vs HFD-B (SUB_AXIS) vs HFD-C (ARTIFACT) decisive separator
# Patterns 1,2,3,4,5,7b applied (Pattern 6 N/A — small model, no cumulative-bytes risk)
# Reconstructed 2026-04-27 23:38Z after pod 1 (oidguj265b00zh) cuInit=999 termination —
# wrapper based on Mk.XII Phase 3b run_cell logic with LAYER_STRIDE=1 + single-cell.
import os, sys, json, time, traceback, math, resource, subprocess, ctypes, shutil

# ---- Pattern 1: HF cache on /workspace BEFORE imports ----
os.environ.setdefault("HF_HOME", "/workspace/.hf_cache")
os.environ.setdefault("HF_HUB_CACHE", "/workspace/.hf_cache")
# ---- Pattern 3: disable XET BEFORE imports ----
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "warning")

OUT_DIR = "/workspace/out"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs("/workspace/.hf_cache", exist_ok=True)
LOG_PATH = "/workspace/wrapper.log"
SUMMARY_PATH = os.path.join(OUT_DIR, "summary.json")
RESULT_PATH = os.path.join(OUT_DIR, "cmt_v3_llama_3_1_8b_stride1.json")
DISPATCH_T0 = time.time()

STATE = {
    "schema": "anima/axis96_step1_wrapper/1",
    "axis": "96 disambiguation step 1 stride=1 full sweep",
    "cell": {"status": "PENDING"},
    "preflight": {"status": "PENDING"},
}

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def write_summary():
    STATE["wallclock_sec"] = time.time() - DISPATCH_T0
    with open(SUMMARY_PATH, "w") as f:
        json.dump(STATE, f, indent=2)

# ---- Pattern 4: sys.excepthook ----
def excepthook(exc_type, exc_val, exc_tb):
    msg = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
    log("__AXIS96_STEP1_UNHANDLED__")
    log(msg)
    STATE["status"] = "UNHANDLED_EXCEPTION"
    STATE["exc_type"] = exc_type.__name__
    STATE["exc_val"] = str(exc_val)
    STATE["traceback"] = msg
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(2)
sys.excepthook = excepthook

# fd limit
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(65536, hard), hard))
except Exception:
    pass

log(f"__AXIS96_STEP1_BEGIN__ HF_HOME={os.environ.get('HF_HOME')} XET={os.environ.get('HF_HUB_DISABLE_XET')}")

# ---- Pattern 7b: cuInit pre-flight BEFORE torch import ----
log("__PREFLIGHT_CUINIT_BEGIN__")
try:
    nv = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True, timeout=15)
    if nv.returncode != 0:
        raise RuntimeError(f"nvidia-smi error: {nv.stderr}")
    log(f"__PREFLIGHT_NVSMI_OK__ {nv.stdout.strip()}")
except Exception as e:
    log(f"__PREFLIGHT_NVSMI_FAIL__ {e}")
    STATE["preflight"] = {"status": "FAIL", "stage": "nvidia-smi", "error": str(e)}
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(3)

try:
    libcuda = ctypes.CDLL("libcuda.so.1")
    rc = libcuda.cuInit(0)
    if rc != 0:
        raise RuntimeError(f"cuInit returned {rc} (CUDA_ERROR_UNKNOWN=999 / SYSTEM_NOT_READY=800). RunPod cold-start fault — re-spawn pod.")
    log(f"__PREFLIGHT_CUINIT_OK__ rc=0")
except Exception as e:
    log(f"__PREFLIGHT_CUINIT_FAIL__ {e}")
    STATE["preflight"] = {"status": "FAIL", "stage": "cuInit", "error": str(e),
                          "advice": "spawn fresh pod (different host) — DO NOT modprobe (pod-kill abuse-trigger)"}
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(4)

# torch import after cuInit success
import torch
if not torch.cuda.is_available():
    log("__PREFLIGHT_TORCH_FAIL__ torch.cuda.is_available()=False post-cuInit-OK")
    STATE["preflight"] = {"status": "FAIL", "stage": "torch_cuda", "error": "torch.cuda not available"}
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(5)
log(f"__PREFLIGHT_TORCH_OK__ device_count={torch.cuda.device_count()} dev0={torch.cuda.get_device_name(0)}")

# memcg / disk probes
try:
    with open("/sys/fs/cgroup/memory.max") as f:
        memcg_max = f.read().strip()
    log(f"__PREFLIGHT_MEMCG__ max={memcg_max}")
except Exception as e:
    log(f"memcg_probe_warn={e}")
try:
    du = shutil.disk_usage("/workspace")
    log(f"__PREFLIGHT_DISK__ workspace_total_gb={du.total/1e9:.1f} free_gb={du.free/1e9:.1f}")
except Exception as e:
    log(f"disk_probe_warn={e}")

STATE["preflight"] = {"status": "OK", "device": torch.cuda.get_device_name(0),
                      "device_count": torch.cuda.device_count()}
write_summary()

# ---- Frozen-spec measurement protocol (identical to Mk.XII Phase 3b 8B cell + gemma cells) ----
PROMPTS = [
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
HIDDEN_TRUNCATED = 128
LAYER_STRIDE = 1   # *** stride=1 — axis 96 step 1 full sweep (vs Mk.XII stride=4) ***

def make_family_axes(h_dim, hidden_truncated, device):
    g = torch.Generator(device="cpu").manual_seed(20260427)
    axes = {}
    for fam in FAMILIES:
        v = torch.zeros(h_dim, dtype=torch.float32)
        sub = torch.randn(hidden_truncated, generator=g)
        v[:hidden_truncated] = sub
        v = v / v.norm()
        axes[fam] = v.to(device)
    return axes

def mem_sentinel(tag):
    try:
        import psutil
        rss = psutil.Process().memory_info().rss / 1e9
    except Exception:
        rss = -1.0
    cuda = torch.cuda.memory_allocated() / 1e9 if torch.cuda.is_available() else 0.0
    log(f"__MEM__ tag={tag} cuda_gb={cuda:.2f} host_rss_gb={rss:.2f}")

# ===== Cell: Llama-3.1-8B fp16 stride=1 =====
REPO_ID = "meta-llama/Llama-3.1-8B"
SENTINEL = "AXIS96_STEP1_8B"
out = {"cell": "llama_3_1_8b_fp16_stride1", "repo_id": REPO_ID, "status": "PENDING"}
cell_t0 = time.time()
mem_sentinel(f"{SENTINEL}_START")

# Stage 1: snapshot_download (Pattern 3)
log(f"__{SENTINEL}_DL_BEGIN__")
try:
    from huggingface_hub import snapshot_download
    t_dl = time.time()
    allow_patterns = [
        "*.json", "*.txt", "*.model", "tokenizer*",
        "*.safetensors",
    ]
    local_dir = snapshot_download(
        repo_id=REPO_ID,
        max_workers=1,
        resume_download=True,
        allow_patterns=allow_patterns,
    )
    dl_elapsed = time.time() - t_dl
    cache_bytes = 0
    for root, dirs, files in os.walk(local_dir):
        for f_ in files:
            try:
                cache_bytes += os.path.getsize(os.path.join(root, f_))
            except Exception:
                pass
    log(f"__{SENTINEL}_DL_DONE__ local_dir={local_dir} elapsed_sec={dl_elapsed:.1f} cache_size_gb={cache_bytes/1e9:.2f}")
    out["dl_elapsed_sec"] = round(dl_elapsed, 1)
    out["cache_size_gb"] = round(cache_bytes / 1e9, 2)
except Exception as e:
    log(f"__{SENTINEL}_DL_FAIL__ {type(e).__name__}: {e}")
    log(traceback.format_exc())
    out["status"] = "FAIL"
    out["fail_reason"] = "snapshot_download_failed"
    out["error"] = str(e)
    STATE["cell"] = out
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(6)

mem_sentinel(f"{SENTINEL}_DL_DONE")

# Stage 2: load (Pattern 2 device_map=auto + low_cpu_mem_usage=True)
log(f"__{SENTINEL}_LOAD_BEGIN__")
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(local_dir)
    log(f"__{SENTINEL}_TOKENIZER_DONE__")
    mem_sentinel(f"{SENTINEL}_TOKENIZER_DONE")

    t_load = time.time()
    kwargs = dict(
        device_map="auto",
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
    )
    model = AutoModelForCausalLM.from_pretrained(local_dir, **kwargs)
    model.eval()
    load_elapsed = time.time() - t_load
    n_layers = len(model.model.layers)
    h_dim = model.config.hidden_size
    log(f"__{SENTINEL}_LOAD_DONE__ elapsed_sec={load_elapsed:.1f} n_layers={n_layers} h_dim={h_dim}")
    out["load_elapsed_sec"] = round(load_elapsed, 1)
    mem_sentinel(f"{SENTINEL}_LOAD_DONE")
except Exception as e:
    log(f"__{SENTINEL}_LOAD_FAIL__ {type(e).__name__}: {e}")
    log(traceback.format_exc())
    out["status"] = "FAIL"
    out["fail_reason"] = "model_load_failed"
    out["error"] = str(e)
    STATE["cell"] = out
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(7)

# Stage 3: CMT v3 measurement (stride=1)
log(f"__{SENTINEL}_CMT_BEGIN__")
try:
    device = next(model.parameters()).device
    axes = make_family_axes(h_dim, HIDDEN_TRUNCATED, device)
    log(f"__{SENTINEL}_AXES_BUILT__ device={device}")

    tomography = {}
    with torch.no_grad():
        layer_indices = list(range(0, n_layers, LAYER_STRIDE))
        log(f"__{SENTINEL}_LAYER_PLAN__ n_layers={n_layers} stride={LAYER_STRIDE} indices_n={len(layer_indices)}")
        accum = {li: {fam: {"abs": [], "rel": [], "norm_dy": []} for fam in FAMILIES} for li in layer_indices}

        for pi, prompt in enumerate(PROMPTS):
            inputs = tok(prompt, return_tensors="pt").to(device)
            with torch.inference_mode():
                outputs = model(
                    **inputs,
                    output_hidden_states=True,
                    return_dict=True,
                )
            for li in layer_indices:
                h_pre = outputs.hidden_states[li][0, -1, :].float()
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
                log(f"__{SENTINEL}_CMT_PROGRESS__ {pi+1}/{len(PROMPTS)}")

        for li in layer_indices:
            tomography[str(li)] = {}
            for fam in FAMILIES:
                tomography[str(li)][fam] = {
                    "abs": round(sum(accum[li][fam]["abs"]) / len(accum[li][fam]["abs"]), 6),
                    "rel": round(sum(accum[li][fam]["rel"]) / len(accum[li][fam]["rel"]), 6),
                    "norm_dy": round(sum(accum[li][fam]["norm_dy"]) / len(accum[li][fam]["norm_dy"]), 8),
                }

    log(f"__{SENTINEL}_CMT_DONE__")
except Exception as e:
    log(f"__{SENTINEL}_CMT_FAIL__ {type(e).__name__}: {e}")
    log(traceback.format_exc())
    out["status"] = "FAIL"
    out["fail_reason"] = "cmt_measurement_failed"
    out["error"] = str(e)
    STATE["cell"] = out
    write_summary()
    log("__AXIS96_STEP1_RESULT__ FAIL")
    sys.exit(8)

# diagnostics — depth_std (axis 96 key metric)
all_rels = []
for li in layer_indices:
    for fam in FAMILIES:
        all_rels.append(tomography[str(li)][fam]["rel"])
rel_mean = sum(all_rels) / len(all_rels)
rel_var = sum((r - rel_mean) ** 2 for r in all_rels) / len(all_rels)
rel_std = math.sqrt(rel_var)
sat_frac = sum(1 for r in all_rels if r > 1.0) / len(all_rels)
informative = (rel_std > 0.005) and (sat_frac < 0.5)

# per-layer depth values for axis 96 depth_std (variance across depth, per family)
depth_per_fam = {}
for fam in FAMILIES:
    fam_vals = [tomography[str(li)][fam]["rel"] for li in layer_indices]
    fm = sum(fam_vals) / len(fam_vals)
    fv = sum((r - fm) ** 2 for r in fam_vals) / len(fam_vals)
    depth_per_fam[fam] = {"mean": round(fm, 6), "std": round(math.sqrt(fv), 6)}
depth_std_overall = sum(d["std"] for d in depth_per_fam.values()) / len(depth_per_fam)

cell = {
    "schema": "anima/cmt/3",
    "backbone": REPO_ID,
    "mode": "v3",
    "quantization": "fp16",
    "axis": "96 step 1 stride=1 full sweep",
    "hook_kind": "passthrough",
    "n_probes": len(PROMPTS),
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
        "depth_per_fam": depth_per_fam,
        "depth_std_overall": round(depth_std_overall, 6),
    },
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "raw_10_caveat": "Llama-3.1-8B fp16 single-cell — does NOT prove HFD-A/B/C alone; pair with stride=4 baseline (depth_std=0.3248) for confirmation.",
}
with open(RESULT_PATH, "w") as f:
    json.dump(cell, f, indent=2)
log(f"__{SENTINEL}_RESULT_WRITTEN__ {RESULT_PATH}")

out["status"] = "OK"
out["rel_std"] = cell["diagnostics"]["rel_std"]
out["depth_std_overall"] = cell["diagnostics"]["depth_std_overall"]
out["saturation_frac"] = cell["diagnostics"]["saturation_frac"]
out["informative"] = cell["diagnostics"]["informative"]
out["n_layers"] = n_layers
out["h_dim"] = h_dim
out["wallclock_sec"] = round(time.time() - cell_t0, 1)
out["result_path"] = RESULT_PATH

# free model
try:
    del model
    del tok
    torch.cuda.empty_cache()
except Exception:
    pass
mem_sentinel(f"{SENTINEL}_FREED")

STATE["cell"] = out
STATE["status"] = "OK"
write_summary()
log(f"__{SENTINEL}_RESULT__ PASS")
log(f"__AXIS96_STEP1_RESULT__ PASS")
sys.exit(0)
