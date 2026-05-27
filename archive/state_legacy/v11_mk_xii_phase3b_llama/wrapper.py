#!/usr/bin/env python3
# anima Mk.XII Phase 3b — Llama-3.1-8B fp16 + Llama-3.1-70B int4 sequential wrapper
# Goal: 2-cell Llama family-internal scale curve, pairwise BBA |r|, HMK-A/B verdict
# Patterns 1,2,3,4,5,7,7b applied. raw#10 caveat: int4 vs fp16 regime mixing.
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
RESULT_8B = os.path.join(OUT_DIR, "cmt_v3_llama_3_1_8b.json")
RESULT_70B = os.path.join(OUT_DIR, "cmt_v3_llama_3_1_70b_int4.json")
DISPATCH_T0 = time.time()

STATE = {
    "schema": "anima/mk_xii_phase3b_llama_wrapper/1",
    "cell1_8b_fp16": {"status": "PENDING"},
    "cell2_70b_int4": {"status": "PENDING"},
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
    log("__MK_XII_PHASE_3B_UNHANDLED__")
    log(msg)
    STATE["status"] = "UNHANDLED_EXCEPTION"
    STATE["exc_type"] = exc_type.__name__
    STATE["exc_val"] = str(exc_val)
    STATE["traceback"] = msg
    write_summary()
    log("__MK_XII_PHASE_3B_RESULT__ FAIL_BOTH")
    sys.exit(2)
sys.excepthook = excepthook

# fd limit
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(65536, hard), hard))
except Exception:
    pass

log(f"__MK_XII_PHASE_3B_BEGIN__ HF_HOME={os.environ.get('HF_HOME')} XET={os.environ.get('HF_HUB_DISABLE_XET')}")

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
    log("__MK_XII_PHASE_3B_RESULT__ FAIL_BOTH")
    sys.exit(3)

try:
    libcuda = ctypes.CDLL("libcuda.so.1")
    rc = libcuda.cuInit(0)
    if rc != 0:
        raise RuntimeError(f"cuInit returned {rc} (CUDA_ERROR_UNKNOWN if 999)")
    log(f"__PREFLIGHT_CUINIT_OK__ rc=0")
except Exception as e:
    log(f"__PREFLIGHT_CUINIT_FAIL__ {e}")
    STATE["preflight"] = {"status": "FAIL", "stage": "cuInit", "error": str(e),
                          "advice": "spawn fresh pod (different host) — DO NOT modprobe (pod-kill abuse-trigger)"}
    write_summary()
    log("__MK_XII_PHASE_3B_RESULT__ FAIL_BOTH")
    sys.exit(4)

# torch import after cuInit success
import torch
if not torch.cuda.is_available():
    log("__PREFLIGHT_TORCH_FAIL__ torch.cuda.is_available()=False post-cuInit-OK")
    STATE["preflight"] = {"status": "FAIL", "stage": "torch_cuda", "error": "torch.cuda not available"}
    write_summary()
    log("__MK_XII_PHASE_3B_RESULT__ FAIL_BOTH")
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

# ---- Frozen-spec measurement protocol (matches gemma 2b/9b/27b cells) ----
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
LAYER_STRIDE = 4

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

def run_cell(cell_name, repo_id, sentinel_prefix, result_path, quantization=None):
    """Returns dict with status + diagnostics. Self-contained, frees memory at end."""
    log(f"__{sentinel_prefix}_BEGIN__ repo_id={repo_id} quantization={quantization}")
    cell_t0 = time.time()
    out = {"cell": cell_name, "repo_id": repo_id, "quantization": quantization, "status": "PENDING"}
    mem_sentinel(f"{sentinel_prefix}_START")

    # ---- Pattern 7: bnb pre-flight (only if quantization) ----
    if quantization == "bnb-4bit":
        try:
            import bitsandbytes as bnb
            log(f"__{sentinel_prefix}_BNB_VERSION__ {bnb.__version__}")
            # bnb GPU wheel detection
            cuda_avail = torch.cuda.is_available()
            if not cuda_avail:
                raise RuntimeError("bnb pre-flight: torch.cuda not available")
            # try a minimal bnb GPU op
            try:
                t = torch.zeros(8, 8, device="cuda")
                # just ensure torch works on GPU; bnb proper test happens in load
                del t
            except Exception as e:
                raise RuntimeError(f"bnb GPU probe fail: {e}")
            log(f"__{sentinel_prefix}_BNB_PREFLIGHT_OK__")
        except Exception as e:
            log(f"__{sentinel_prefix}_BNB_PREFLIGHT_FAIL__ {e}")
            out["status"] = "FAIL"
            out["fail_reason"] = "bnb_preflight_failed"
            out["error"] = str(e)
            return out

    # Stage 1: snapshot_download (Pattern 3)
    log(f"__{sentinel_prefix}_DL_BEGIN__")
    try:
        from huggingface_hub import snapshot_download
        t_dl = time.time()
        # filter out files we don't need to reduce ingress
        allow_patterns = [
            "*.json", "*.txt", "*.model", "tokenizer*",
            "*.safetensors",
        ]
        local_dir = snapshot_download(
            repo_id=repo_id,
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
        log(f"__{sentinel_prefix}_DL_DONE__ local_dir={local_dir} elapsed_sec={dl_elapsed:.1f} cache_size_gb={cache_bytes/1e9:.2f}")
        out["dl_elapsed_sec"] = round(dl_elapsed, 1)
        out["cache_size_gb"] = round(cache_bytes / 1e9, 2)
    except Exception as e:
        log(f"__{sentinel_prefix}_DL_FAIL__ {type(e).__name__}: {e}")
        log(traceback.format_exc())
        out["status"] = "FAIL"
        out["fail_reason"] = "snapshot_download_failed"
        out["error"] = str(e)
        return out

    mem_sentinel(f"{sentinel_prefix}_DL_DONE")

    # Stage 2: load (Pattern 2)
    log(f"__{sentinel_prefix}_LOAD_BEGIN__")
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(local_dir)
        log(f"__{sentinel_prefix}_TOKENIZER_DONE__")
        mem_sentinel(f"{sentinel_prefix}_TOKENIZER_DONE")

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
        log(f"__{sentinel_prefix}_LOAD_DONE__ elapsed_sec={load_elapsed:.1f} n_layers={n_layers} h_dim={h_dim}")
        out["load_elapsed_sec"] = round(load_elapsed, 1)
        mem_sentinel(f"{sentinel_prefix}_LOAD_DONE")
    except Exception as e:
        log(f"__{sentinel_prefix}_LOAD_FAIL__ {type(e).__name__}: {e}")
        log(traceback.format_exc())
        out["status"] = "FAIL"
        out["fail_reason"] = "model_load_failed"
        out["error"] = str(e)
        return out

    # Stage 3: CMT v3 measurement
    log(f"__{sentinel_prefix}_CMT_BEGIN__")
    try:
        device = next(model.parameters()).device
        axes = make_family_axes(h_dim, HIDDEN_TRUNCATED, device)
        log(f"__{sentinel_prefix}_AXES_BUILT__ device={device}")

        tomography = {}
        with torch.no_grad():
            layer_indices = list(range(0, n_layers, LAYER_STRIDE))
            log(f"__{sentinel_prefix}_LAYER_PLAN__ n_layers={n_layers} indices={layer_indices}")
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
                    log(f"__{sentinel_prefix}_CMT_PROGRESS__ {pi+1}/{len(PROMPTS)}")

            for li in layer_indices:
                tomography[str(li)] = {}
                for fam in FAMILIES:
                    tomography[str(li)][fam] = {
                        "abs": round(sum(accum[li][fam]["abs"]) / len(accum[li][fam]["abs"]), 6),
                        "rel": round(sum(accum[li][fam]["rel"]) / len(accum[li][fam]["rel"]), 6),
                        "norm_dy": round(sum(accum[li][fam]["norm_dy"]) / len(accum[li][fam]["norm_dy"]), 8),
                    }

        log(f"__{sentinel_prefix}_CMT_DONE__")
    except Exception as e:
        log(f"__{sentinel_prefix}_CMT_FAIL__ {type(e).__name__}: {e}")
        log(traceback.format_exc())
        out["status"] = "FAIL"
        out["fail_reason"] = "cmt_measurement_failed"
        out["error"] = str(e)
        # free model
        try:
            del model
            torch.cuda.empty_cache()
        except Exception:
            pass
        return out

    # diagnostics
    all_rels = []
    for li in layer_indices:
        for fam in FAMILIES:
            all_rels.append(tomography[str(li)][fam]["rel"])
    rel_mean = sum(all_rels) / len(all_rels)
    rel_var = sum((r - rel_mean) ** 2 for r in all_rels) / len(all_rels)
    rel_std = math.sqrt(rel_var)
    sat_frac = sum(1 for r in all_rels if r > 1.0) / len(all_rels)
    informative = (rel_std > 0.005) and (sat_frac < 0.5)

    cell = {
        "schema": "anima/cmt/3",
        "backbone": repo_id,
        "mode": "v3",
        "quantization": quantization or "fp16",
        "raw_10_caveat": ("int4 quantization regime — measurement is on SEPARATE axis from fp16 cells"
                         if quantization else None),
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
        },
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(result_path, "w") as f:
        json.dump(cell, f, indent=2)
    log(f"__{sentinel_prefix}_RESULT_WRITTEN__ {result_path}")

    out["status"] = "OK"
    out["rel_std"] = cell["diagnostics"]["rel_std"]
    out["saturation_frac"] = cell["diagnostics"]["saturation_frac"]
    out["informative"] = cell["diagnostics"]["informative"]
    out["n_layers"] = n_layers
    out["h_dim"] = h_dim
    out["wallclock_sec"] = round(time.time() - cell_t0, 1)
    out["result_path"] = result_path

    # free model
    try:
        del model
        del tok
        torch.cuda.empty_cache()
    except Exception:
        pass
    mem_sentinel(f"{sentinel_prefix}_FREED")
    return out

# ===== Cell 1: Llama-3.1-8B fp16 =====
cell1 = run_cell(
    cell_name="llama_3_1_8b_fp16",
    repo_id="meta-llama/Llama-3.1-8B",
    sentinel_prefix="LLAMA_8B",
    result_path=RESULT_8B,
    quantization=None,
)
STATE["cell1_8b_fp16"] = cell1
write_summary()
if cell1["status"] == "OK":
    log("__LLAMA_8B_RESULT__ PASS")
else:
    log("__LLAMA_8B_RESULT__ FAIL")

# ===== Cell 2: Llama-3.1-70B int4 =====
# Even if 8B failed, attempt 70B (may yield independent evidence). But if preflight fails, abort.
# Per spec: 70B termination → STOP and salvage 8B; we still attempt 70B at least once.
cell2 = run_cell(
    cell_name="llama_3_1_70b_int4",
    repo_id="unsloth/Meta-Llama-3.1-70B-bnb-4bit",
    sentinel_prefix="LLAMA_70B",
    result_path=RESULT_70B,
    quantization="bnb-4bit",
)
STATE["cell2_70b_int4"] = cell2
write_summary()
if cell2["status"] == "OK":
    log("__LLAMA_70B_INT4_RESULT__ PASS")
else:
    log("__LLAMA_70B_INT4_RESULT__ FAIL")

# Final sentinel
if cell1["status"] == "OK" and cell2["status"] == "OK":
    final = "PASS_BOTH"
elif cell1["status"] == "OK":
    final = "PASS_8B_FAIL_70B"
elif cell2["status"] == "OK":
    final = "FAIL_8B_PASS_70B"
else:
    final = "FAIL_BOTH"
STATE["final"] = final
write_summary()
log(f"__MK_XII_PHASE_3B_RESULT__ {final}")
