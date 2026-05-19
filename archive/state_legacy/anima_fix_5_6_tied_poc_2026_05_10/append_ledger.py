"""Append BG ledger entry. argv: ledger_path pod_id pod_name elapsed_s cost_usd"""
import json, sys, time
ledger, pod_id, pod_name, elapsed_s, cost = sys.argv[1:6]
with open(ledger, "a") as f:
    f.write(json.dumps({
        "ts": time.strftime("%FT%TZ"),
        "bg_id": "FIX-5-6-TIED-POC",
        "cycle": "anima_fix_5_6_tied_poc_2026_05_10",
        "pod_id": pod_id,
        "pod_name": pod_name,
        "elapsed_s": int(elapsed_s),
        "cost_usd_est": float(cost),
        "branches": ["a", "b", "c"],
    }) + "\n")
print("ledger appended")
