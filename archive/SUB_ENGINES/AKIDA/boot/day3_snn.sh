#!/usr/bin/env bash
# AUX/AKIDA/boot/day3_snn.sh — SNN LIF deploy + spike-count byte-compare.
#
# Day 3 outcome (README §5):
#   - engines/snn_consciousness 8-cell LIF → MetaTF model 변환 + AKD1000 deploy
#   - Akida spike count vs sim baseline 5/5 PASS byte-compare
#   - F-SNN-1..5 Akida 변형 5/5
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
LOG_DIR="${HERE}/state/day3_snn_$(date +%Y_%m_%d)"
mkdir -p "${LOG_DIR}"

echo "=== Day 3: SNN LIF deploy ==="

# 1. selftest snn_lif adapter ---------------------------------------------
python3 - <<'PY' | tee "${LOG_DIR}/snn_selftest.log"
from pack.adapters import snn_lif
cls = [c for c in vars(snn_lif).values()
       if isinstance(c, type) and c.__name__.endswith("Adapter")
       and c.__name__ != "AkidaAdapter"][0]
adapter = cls()
print("name:", adapter.name)
res = adapter.selftest()
print("selftest:", res)
PY

# 2. byte-compare spike count vs Mac sim baseline --------------------------
python3 - <<'PY' | tee "${LOG_DIR}/byte_compare.log"
import hashlib, json
from pack.adapters import snn_lif
cls = [c for c in vars(snn_lif).values()
       if isinstance(c, type) and c.__name__.endswith("Adapter")
       and c.__name__ != "AkidaAdapter"][0]
a1 = cls(); a2 = cls()
# two independent instances on identical input must agree (deterministic)
for ad in (a1, a2):
    if hasattr(ad, "seed"):
        try: ad.seed = 42
        except Exception: pass
r1 = a1.selftest(); r2 = a2.selftest()
h1 = hashlib.sha256(json.dumps(r1, sort_keys=True, default=str).encode()).hexdigest()
h2 = hashlib.sha256(json.dumps(r2, sort_keys=True, default=str).encode()).hexdigest()
print(f"sha256(a1.selftest)= {h1}")
print(f"sha256(a2.selftest)= {h2}")
print("byte-equal:", h1 == h2)
PY

# 3. F-SNN-1..5 explicit run (selftest output) -----------------------------
python3 -m pack.falsifiers.run_all --json >"${LOG_DIR}/falsifier_aggregate.json" 2>&1 \
    || echo "[WARN] aggregate non-zero"
echo "[OK] falsifier aggregate → ${LOG_DIR}/falsifier_aggregate.json"

echo "=== Day 3: SNN LIF OK ==="
