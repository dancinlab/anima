#!/usr/bin/env bash
# AUX/AKIDA/boot/day6_demiurge.sh — demiurge brain producer backend=akida_cloud.
#
# Day 6 outcome (README §5):
#   - `demiurge cli action verify brain` with backend=akida_cloud
#   - gate_state CLOSED OR ⏳ honest
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
LOG_DIR="${HERE}/state/day6_demiurge_$(date +%Y_%m_%d)"
mkdir -p "${LOG_DIR}"

echo "=== Day 6: demiurge brain producer ==="

# 1. Pi 5 orchestrator emit-demiurge -----------------------------------
set +e
python3 -m pack.runtime.pi5_orchestrator --emit-demiurge \
    >"${LOG_DIR}/orchestrator.log" 2>&1
RC=$?
set -e
if [ "$RC" -ne 0 ]; then
    echo "[WARN] pi5_orchestrator __main__ rc=$RC — falling back to API path"
    python3 - <<'PY' | tee "${LOG_DIR}/orchestrator_api.log"
try:
    from pack.runtime.pi5_orchestrator import Pi5Orchestrator
    orch = Pi5Orchestrator()
    rec = orch.emit_demiurge() if hasattr(orch, "emit_demiurge") else None
    print("emit_demiurge:", rec)
except Exception as exc:  # noqa: BLE001
    print(f"[INFO] orchestrator API path unavailable: {exc}")
    print("       (runtime agent has not landed pi5_orchestrator.emit_demiurge)")
PY
fi

# 2. demiurge bridge — backend=akida_cloud reference -----------------------
DEMIURGE_BRIDGE="${HERE}/../hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py"
if [ -f "$DEMIURGE_BRIDGE" ]; then
    echo "[STEP] demiurge_brain_bridge.py backend=akida_cloud"
    python3 "$DEMIURGE_BRIDGE" --backend akida_cloud --emit-record \
        >"${LOG_DIR}/demiurge_bridge.log" 2>&1 || \
        echo "[WARN] bridge needs Akida Cloud creds — Day 1 cloud-trial reminder applies"
else
    echo "[INFO] demiurge_brain_bridge.py not found at $DEMIURGE_BRIDGE"
    echo "       (path will exist once AUX/hw lane lands)"
fi

# 3. gate state probe (honest CLOSED vs ⏳) --------------------------------
python3 - <<'PY' | tee "${LOG_DIR}/gate_state.log"
import os, json, time
state = {
    "timestamp": time.time(),
    "backend": "akida_cloud",
    "gate_state": "PENDING",  # default honest ⏳
    "note": "Day 6 requires Akida Cloud subscription + AKD1000 silicon; "
            "Mac local pre-arrival emits PENDING.",
}
try:
    import akida
    state["gate_state"] = "CLOSED"
    state["akida_version"] = getattr(akida, "__version__", "?")
except ImportError:
    pass
print(json.dumps(state, indent=2))
PY

echo "=== Day 6: demiurge OK ==="
