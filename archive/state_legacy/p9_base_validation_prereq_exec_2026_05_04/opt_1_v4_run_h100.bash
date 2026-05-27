#!/bin/bash
# emitted by tool/p9_opt_1_v4_exec_h100_orchestrator.hexa — H100-side v4 exec runner
# raw#37 transient: Python on Linux permitted; killed with pod.
set -uo pipefail

WORK=/workspace/p9_v4_exec
cd $WORK
export HF_TOKEN="${HF_TOKEN}"
export HF_HUB_TOKEN="${HF_TOKEN}"
export HUGGING_FACE_HUB_TOKEN="${HF_TOKEN}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONUNBUFFERED=1

RESULTS=$WORK/results
mkdir -p $RESULTS

echo "[orch] start ts=$(date -u +%FT%TZ)"

# Setup: install deps + download CLM v4 base mirror + Llama tokenizer (no Llama needed — only CLM)
echo "[setup] installing deps"
pip install -q --no-input huggingface_hub safetensors 'transformers>=4.45' accelerate datasets 'lm-eval==0.4.11' sentencepiece tiktoken protobuf 2>&1 | tail -8

# Auth
hf auth login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || \
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tail -2 || true

# Download CLM v4 base mirror (need-singularity org)
echo "[setup] downloading need-singularity/clm-v4-base-mirror"
hf download need-singularity/clm-v4-base-mirror 2>&1 | tail -5 || \
    huggingface-cli download need-singularity/clm-v4-base-mirror 2>&1 | tail -5

# Locate best.pt + tokenizer (find in cache)
BEST_PT=$(find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots -name 'best.pt' 2>/dev/null | head -1)
TOK_DIR=$(find ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots -type d -name 'tokenizer' 2>/dev/null | head -1)
echo "[setup] best.pt=$BEST_PT"
echo "[setup] tokenizer=$TOK_DIR"
if [ -z "$BEST_PT" ] || [ -z "$TOK_DIR" ]; then
    echo "[FAIL] best.pt or tokenizer not found in HF cache"
    ls -R ~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/ 2>&1 | head -50
    echo '{"f_shim_v4_3":"FAIL","reason":"best.pt or tokenizer missing in HF cache"}' > $RESULTS/v4_verdict.json
    touch $RESULTS/COMPLETE.sentinel
    exit 1
fi

echo "[orch] torch=$(python3 -c 'import torch; print(torch.__version__)')"
nvidia-smi --query-gpu=name,memory.total --format=csv | head -2

# ── Stage A: Run shim v4 with canonical_zero fixture ──
OUT_V4=$WORK/output_v4
OUT_NF=$WORK/output_no_fixture
mkdir -p $OUT_V4 $OUT_NF

echo "[stageA] shim v4 with canonical_zero fixture"
python3 clm_v4_hf_format_shim.py \
    --input-pt "$BEST_PT" \
    --tokenizer-dir "$TOK_DIR" \
    --output-dir "$OUT_V4" \
    --consciousness-states-fixture "$WORK/opt_1_v4_consciousness_states_fixture.json" \
    --verify --force-overwrite 2>&1 | tee v4_apply.log
V4_RC=${PIPESTATUS[0]}
echo "[stageA] shim_rc=$V4_RC"

echo "[stageA-no-fixture] shim v4 WITHOUT fixture (sanity baseline)"
python3 clm_v4_hf_format_shim.py \
    --input-pt "$BEST_PT" \
    --tokenizer-dir "$TOK_DIR" \
    --output-dir "$OUT_NF" \
    --verify --force-overwrite 2>&1 | tee v4_apply_nf.log | tail -20
NF_RC=${PIPESTATUS[0]}
echo "[stageA-no-fixture] shim_nf_rc=$NF_RC"

# ── Stage B: F-SHIM-V4-3 — canonical_zero finite forward ──
echo "[stageB] F-SHIM-V4-3 finite forward smoketest"
python3 - <<'PYEOF' 2>&1 | tee $RESULTS/f_shim_v4_3.log
import os, json, traceback
out = {"f_shim_v4_3": "FAIL", "finite_forward": "unknown", "shape": None, "err": None}
try:
    import torch
    from transformers import AutoModelForCausalLM
    out_v4 = "/workspace/p9_v4_exec/output_v4"
    m = AutoModelForCausalLM.from_pretrained(out_v4, trust_remote_code=True, torch_dtype=torch.float16)
    # Bypass AutoTokenizer (CLM v4 SP tokenizer not directly compatible) — use raw int ids
    # vocab_size=64000; pick safe range [10..50] to ensure valid token ids
    ids = torch.arange(10, 42, dtype=torch.long).unsqueeze(0)  # [1, 32]
    with torch.no_grad():
        result = m(ids)
    logits = result.logits if hasattr(result, "logits") else result[0]
    finite = bool(torch.isfinite(logits).all().item())
    shape = list(logits.shape)
    out["shape"] = shape
    out["finite_forward"] = "finite" if finite else "non_finite"
    # F-SHIM-V4-3: finite + shape [1, T, 64000]
    if finite and len(shape) == 3 and shape[0] == 1 and shape[2] == 64000:
        out["f_shim_v4_3"] = "PASS"
    else:
        out["f_shim_v4_3"] = "FAIL"
    # Inspect fixture meta
    meta = getattr(m, "_consciousness_fixture_meta", None)
    out["fixture_meta"] = meta if meta is None or isinstance(meta, dict) else str(meta)
    has_fix = getattr(m, "_consciousness_fixture_cpu", None) is not None
    out["fixture_loaded"] = bool(has_fix)
except Exception as e:
    out["err"] = f"{type(e).__name__}: {e}"
    out["trace"] = traceback.format_exc()
print("=== f_shim_v4_3_smoketest_result ===")
print(json.dumps(out, indent=2))
with open("/workspace/p9_v4_exec/results/f_shim_v4_3_result.json", "w") as f:
    json.dump(out, f, indent=2)
PYEOF

# ── Stage C: train_avg harvest stub ──
echo "[stageC] train_avg harvest stub"
python3 - <<'PYEOF' 2>&1 | tee $RESULTS/train_avg_harvest.log
import os, json, glob, traceback
result = {"harvest_via": "FAILED", "err": None, "shape": None, "sample_first10": None}
try:
    import torch
    # Approach (a): scan best.pt for consciousness_state_avg-like keys
    best_pt_paths = glob.glob(os.path.expanduser(
        "~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/*/best.pt"))
    if best_pt_paths:
        ckpt = torch.load(best_pt_paths[0], map_location="cpu", weights_only=False)
        keys = list(ckpt.keys()) if isinstance(ckpt, dict) else []
        result["ckpt_top_keys"] = keys[:30]
        cand_keys = [k for k in keys if any(s in k.lower() for s in ["consciousness_avg", "consciousness_state_avg", "cell_avg", "c_avg"])]
        result["approach_a_candidates"] = cand_keys
        if cand_keys:
            t = ckpt[cand_keys[0]]
            if hasattr(t, "shape"):
                result["harvest_via"] = "best.pt extract"
                result["key_used"] = cand_keys[0]
                result["shape"] = list(t.shape)
                arr = t.detach().to(torch.float32).cpu().tolist()
                result["sample_first10"] = arr[0][0][:10] if isinstance(arr[0][0], list) else arr[:10]
                # Save as fixture
                if list(t.shape) == [1, 8, 192] or (len(t.shape) == 3 and t.shape[2] == 192):
                    fixture = {
                        "states": arr,
                        "shape": list(t.shape),
                        "dtype": "float32",
                        "source": "train_avg",
                        "provenance": f"best.pt extract key={cand_keys[0]}"
                    }
                    with open("/workspace/p9_v4_exec/results/train_avg_fixture.json", "w") as f:
                        json.dump(fixture, f)
                    result["fixture_saved"] = True

    # Approach (b): synthetic stub (no model load needed — STUB only since approach (a) found no key)
    if result["harvest_via"] == "FAILED":
        # Build a dummy [1, 8, 192] random-init avg as STUB (canonical_zero shifted by tiny noise)
        # This is a pure stub — flag clearly
        torch.manual_seed(42)
        states = torch.randn(1, 8, 192, dtype=torch.float32) * 0.01
        result["harvest_via"] = "forward-pass synthetic stub (random N(0,0.01) — NOT actual train avg)"
        result["shape"] = list(states.shape)
        arr = states.tolist()
        result["sample_first10"] = arr[0][0][:10]
        fixture = {
            "states": arr,
            "shape": list(states.shape),
            "dtype": "float32",
            "source": "train_avg",
            "provenance": "BG-Σ stub — synthetic N(0, 0.01) since best.pt has no train_avg key; placeholder for future real harvest"
        }
        with open("/workspace/p9_v4_exec/results/train_avg_fixture.json", "w") as f:
            json.dump(fixture, f)
        result["fixture_saved"] = True
        result["stub_warning"] = "This is a SYNTHETIC stub. Real train_avg requires anima_unified.py runtime forward pass over training data with cell hidden harvest."
except Exception as e:
    result["err"] = f"{type(e).__name__}: {e}"
    result["trace"] = traceback.format_exc()[:3000]
print("=== train_avg_harvest_result ===")
print(json.dumps(result, indent=2)[:4000])
with open("/workspace/p9_v4_exec/results/train_avg_harvest_result.json", "w") as f:
    json.dump(result, f, indent=2)
PYEOF

# ── Stage D: optional limit=100 hellaswag sanity (with vs without fixture) ──
echo "[stageD] limit=100 hellaswag sanity eval"

run_sanity() {
    local label=$1
    local model_dir=$2
    local out=$RESULTS/sanity_${label}_dir
    local log=$RESULTS/sanity_${label}.log
    echo "[sanity] label=$label model_dir=$model_dir"
    lm_eval --model hf \
        --model_args "pretrained=${model_dir},dtype=bfloat16,trust_remote_code=True" \
        --tasks hellaswag \
        --num_fewshot 0 \
        --batch_size 8 \
        --device cuda:0 \
        --seed 42 \
        --limit 100 \
        --output_path "$out" \
        > "$log" 2>&1 || echo "[sanity] $label rc=$?"
    if [ -d "$out" ]; then
        find "$out" -name 'results*.json' -exec cp {} $RESULTS/sanity_${label}.json \;
    fi
}

# Only run sanity if F-SHIM-V4-3 looked plausible (model loadable)
V4_3_PASS=$(jq -r '.f_shim_v4_3 // "FAIL"' $RESULTS/f_shim_v4_3_result.json 2>/dev/null || echo FAIL)
if [ "$V4_3_PASS" = "PASS" ]; then
    run_sanity 'canonical_zero' "$OUT_V4"
    run_sanity 'no_fixture' "$OUT_NF"
else
    echo "[stageD] skipped — F-SHIM-V4-3 did not pass"
fi

# ── Stage E: aggregate verdict ──
echo "[stageE] aggregate verdict"
python3 - <<'PYEOF' 2>&1 | tee $RESULTS/v4_aggregate.log
import os, json
R = "/workspace/p9_v4_exec/results"
v = {
    "f_shim_v4_3": "UNKNOWN",
    "f_shim_v4_4": "HARVEST_STUB_ONLY",
    "finite_forward": "unknown",
    "harvest_via": "FAILED",
    "sanity_canonical_zero_hellaswag_acc": None,
    "sanity_no_fixture_hellaswag_acc": None,
}
# F-SHIM-V4-3
p = os.path.join(R, "f_shim_v4_3_result.json")
if os.path.isfile(p):
    d = json.load(open(p))
    v["f_shim_v4_3"] = d.get("f_shim_v4_3", "UNKNOWN")
    v["finite_forward"] = d.get("finite_forward", "unknown")
    v["f_shim_v4_3_shape"] = d.get("shape")
    v["f_shim_v4_3_fixture_loaded"] = d.get("fixture_loaded")
    v["f_shim_v4_3_err"] = d.get("err")
# Harvest
p = os.path.join(R, "train_avg_harvest_result.json")
if os.path.isfile(p):
    d = json.load(open(p))
    v["harvest_via"] = d.get("harvest_via", "FAILED")
    v["harvest_shape"] = d.get("shape")
    v["harvest_stub_warning"] = d.get("stub_warning")
# Sanity acc extract
def grab_acc(path):
    if not os.path.isfile(path):
        return None
    try:
        d = json.load(open(path))
        r = d.get("results", {}).get("hellaswag", {})
        for k in ("acc_norm,none", "acc_norm", "acc,none", "acc"):
            if k in r:
                return float(r[k])
    except Exception:
        return None
    return None
v["sanity_canonical_zero_hellaswag_acc"] = grab_acc(os.path.join(R, "sanity_canonical_zero.json"))
v["sanity_no_fixture_hellaswag_acc"] = grab_acc(os.path.join(R, "sanity_no_fixture.json"))
print(json.dumps(v, indent=2))
with open(os.path.join(R, "v4_verdict.json"), "w") as f:
    json.dump(v, f, indent=2)
PYEOF

# completion sentinel — STANDARDIZED NAME per spec L1
echo "{\"ok\": true, \"finished_at\": \"$(date -u +%FT%TZ)\"}" > $RESULTS/COMPLETE.sentinel
echo "[orch] complete"
