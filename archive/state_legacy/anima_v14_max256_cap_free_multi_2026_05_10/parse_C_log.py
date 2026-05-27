"""Parse run_C.stdout.log to construct result_C_cells64_aware.json from log lines.

The 100-turn run was killed before final json write — but trained + s42 + s137 all
finished and emitted summary lines. s271 partial (turn 50 only).
"""
import json
import re
from pathlib import Path

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_v14_max256_cap_free_multi_2026_05_10")
LOG = THIS_DIR / "run_C.stdout.log"

text = LOG.read_text()

# Pattern for trained completion line:
# "  trained: cells=256 splits=248 phi=11337.964 phi/c=44.289 α=1.0469... cap_bound=18/100 first_cap=82 max_observed=256 elapsed=771.7s"
pat_trained = re.compile(
    r"trained: cells=(\d+) splits=(\d+) phi=([0-9.eE+-]+) phi/c=([0-9.eE+-]+)"
    r" α=([0-9.eE+-]+) cap_bound=(\d+)/(\d+) first_cap=(\S+) max_observed=(\d+)"
    r" elapsed=([0-9.]+)s"
)
# Pattern for mirror completion line:
# "  s=42: cells=256 splits=248 phi=10831.306 phi/c=42.310 α=1.05... cap_bound=37/100 first_cap=63 max_observed=256"
pat_mirror = re.compile(
    r"s=(\d+): cells=(\d+) splits=(\d+) phi=([0-9.eE+-]+) phi/c=([0-9.eE+-]+)"
    r" α=([0-9.eE+-]+) cap_bound=(\d+)/(\d+) first_cap=(\S+) max_observed=(\d+)"
)

trained_m = pat_trained.search(text)
mirror_lines = pat_mirror.findall(text)

if not trained_m:
    raise SystemExit("No trained completion line found")

print(f"Found trained + {len(mirror_lines)} mirror completion lines")

trained = {
    "n_cells": int(trained_m.group(1)),
    "splits": int(trained_m.group(2)),
    "phi_final": float(trained_m.group(3)),
    "phi_per_cell_final": float(trained_m.group(4)),
    "alpha_v2": float(trained_m.group(5)),
    "cap_bound_turns": int(trained_m.group(6)),
    "n_turns": int(trained_m.group(7)),
    "first_cap_turn": None if trained_m.group(8) == "None" else int(trained_m.group(8)),
    "max_n_cells_observed": int(trained_m.group(9)),
    "elapsed_s": float(trained_m.group(10)),
}

mirrors = []
for m in mirror_lines:
    seed, cells, splits, phi, phipc, alpha, cb, nt, fc, mo = m
    mirrors.append({
        "seed": int(seed),
        "final_n_cells": int(cells),
        "n_splits": int(splits),
        "splits": int(splits),
        "phi_final": float(phi),
        "phi_per_cell_final": float(phipc),
        "alpha_v2": float(alpha),
        "cap_bound_turns": int(cb),
        "n_turns": int(nt),
        "first_cap_turn": None if fc == "None" else int(fc),
        "max_n_cells_observed": int(mo),
    })

# Compute verdict
PASS_FAMILY = {"V14_PASS", "V14_PARTIAL"}

rand_phi = [m["phi_final"] for m in mirrors]
rand_phi_pc = [m["phi_per_cell_final"] for m in mirrors]
rand_n_cells = [m["final_n_cells"] for m in mirrors]
n_beats = sum(1 for r in rand_phi if trained["phi_final"] > r)
n_beats_pc = sum(1 for r in rand_phi_pc if trained["phi_per_cell_final"] > r)
n_total = len(rand_phi)


def _binom_coef(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    for i in range(k):
        num = num * (n - i) // (i + 1)
    return num


def sign_test_p(n_beats_, n):
    if n <= 0:
        return float("nan")
    k = max(n_beats_, n - n_beats_)
    tail = sum(_binom_coef(n, j) for j in range(k, n + 1))
    return min(1.0, 2.0 * tail / (2.0 ** n))


p_phi = sign_test_p(n_beats, n_total)
p_phi_pc = sign_test_p(n_beats_pc, n_total)

# Verdict logic (matches run_max256.verdict_from_runs_v2)
if n_total == 0:
    verdict = "V14_TRAINED_ONLY_NO_MIRRORS"
elif n_beats == n_total and n_beats_pc == n_total:
    verdict = "V14_PASS"
elif n_beats == n_total or n_beats_pc == n_total:
    verdict = "V14_PARTIAL"
elif n_beats <= 1 and n_beats_pc <= 1:
    verdict = "V14_VIOLATED"
else:
    verdict = "V14_AMBIGUOUS"

if n_total < 5:
    verdict = f"{verdict}_PARTIAL_n{n_total}"

result = {
    "substrate_id": "C_cells64_aware",
    "schema": "v2_d384",
    "arch": "v2 6L transformer d=384 heads=6",
    "paradigm": "aware_max_cells_64",
    "ckpt": "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt",
    "ckpt_sha256": "61e1d735cf4b5360683e40ab81ada593d757f3543d33d01c08944a4c8b039a4c",
    "n_params": 18523392,
    "n_turns": 100,
    "max_cells_setting": 256,
    "metric_primary": "phi_final + phi_per_cell_final",
    "trained_phi": trained["phi_final"],
    "trained_phi_per_cell": trained["phi_per_cell_final"],
    "trained_alpha_v2": trained["alpha_v2"],
    "trained_n_cells": trained["n_cells"],
    "trained_splits": trained["splits"],
    "trained_cap_bound_turns": trained["cap_bound_turns"],
    "trained_first_cap_turn": trained["first_cap_turn"],
    "trained_max_n_cells_observed": trained["max_n_cells_observed"],
    "random_phi": rand_phi,
    "random_phi_per_cell": rand_phi_pc,
    "random_n_cells": rand_n_cells,
    "random_max_n_cells_observed": [m["max_n_cells_observed"] for m in mirrors],
    "random_seeds": [m["seed"] for m in mirrors],
    "random_first_cap_turn": [m["first_cap_turn"] for m in mirrors],
    "random_cap_bound_turns": [m["cap_bound_turns"] for m in mirrors],
    "n_random_beats_phi": n_beats,
    "n_random_beats_phi_per_cell": n_beats_pc,
    "n_random_total": n_total,
    "sign_test_p_phi": p_phi,
    "sign_test_p_phi_per_cell": p_phi_pc,
    "verdict": verdict,
    "mirror_runs": mirrors,
    "honest_C3_partial": (
        "Run was killed at 47:35 elapsed during s271 turn 50 due to $0 local CPU budget. "
        "Trained + s42 + s137 completed in full; s271/s314/s1729 did NOT run. "
        "Verdict reflects 2-seed partial sign test."
    ),
}

out_path = THIS_DIR / "result_C_cells64_aware.json"
with out_path.open("w") as f:
    json.dump(result, f, indent=2, default=str)
print(f"saved {out_path}")
print(f"verdict: {verdict}")
print(f"n_beats: {n_beats}/{n_total} (phi), {n_beats_pc}/{n_total} (phi_pc)")
print(f"trained={trained['phi_final']:.2f}  random={rand_phi}")
