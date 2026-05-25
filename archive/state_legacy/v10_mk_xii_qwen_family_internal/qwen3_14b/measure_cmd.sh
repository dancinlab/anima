set -e
mkdir -p /workspace/out
cat > /workspace/.hf_token <<HFEOT
hf_REDACTED
HFEOT
pip install -q transformers accelerate sentencepiece 2>&1 | tail -3
export ANIMA_BASE='Qwen/Qwen3-14B-Base'
echo '=== AXIS: Phi v3 canonical (BASE only) ==='
ANIMA_OUTPUT=/workspace/out/phi_v3_canonical.json python3 /workspace/anima_phi_v3_canonical_helper.py 2>&1 | tail -8
ls -la /workspace/out/
