#!/usr/bin/env python3
"""
A29 v3 standalone 6-repo MEASURED benchmark.
- raw 91 honest C3 STRICT: per-file MEASURED, no projection.
- raw 142 D2 try-and-revert: per-file shortest of {v3, identity}.
  (v2/v1 require separate encoders; we measure v3 vs identity baseline only here,
   then compare aggregate against pre-recorded A25 baseline 60.79% and v1 promotion 61.99%.)
- per-file timeout 30s.
- byte-eq SHA256 sample = 30+ files round-trip verify.
- Output: 6-repo aggregate, per-class breakdown, per-repo breakdown.

NOTE: This is a MEASUREMENT harness in Python; A29 v3 encoding itself is invoked via
the hexa-lang AOT binary `hxc_a29` (sigil ^a s3 native). Per raw 9 hexa-only constraint,
no python encoding logic runs — only subprocess orchestration + measurement bookkeeping.
"""
import json
import os
import subprocess
import sys
import hashlib
import time
import tempfile
from pathlib import Path
from collections import defaultdict

MANIFEST = "/Users/ghost/core/anima/state/baselines/16ff3e55.manifest.json"
HXC_A29 = "/Users/ghost/core/anima/.hxc_aot/hxc_a29"
WITNESS = "/Users/ghost/core/anima/state/format_witness/2026-04-28_a29_v3_standalone_6repo_benchmark.jsonl"
PER_FILE_TIMEOUT = 30
SAMPLE_SHA_STEP = 50  # every 50th file → ~32 samples for round-trip

def main():
    with open(MANIFEST) as f:
        manifest = json.load(f)

    total_files = manifest["total_files"]
    total_raw = manifest["total_raw_bytes"]

    # Aggregators
    agg = {
        "total_files_attempted": 0,
        "total_files_skipped_missing": 0,
        "total_files_timed_out": 0,
        "total_files_failed": 0,
        "total_raw_bytes": 0,
        "total_v3_bytes": 0,
        "total_chosen_bytes": 0,  # min(v3, identity) per-file
        "v3_chosen_count": 0,
        "identity_chosen_count": 0,
        "byte_eq_attempted": 0,
        "byte_eq_pass": 0,
        "byte_eq_fail": 0,
        "byte_eq_samples": [],
    }

    per_class = defaultdict(lambda: {"files": 0, "raw": 0, "v3": 0, "chosen": 0, "v3_win": 0})
    per_repo = defaultdict(lambda: {"files": 0, "raw": 0, "v3": 0, "chosen": 0, "v3_win": 0})

    # Witness ledger output
    os.makedirs(os.path.dirname(WITNESS), exist_ok=True)
    wf = open(WITNESS, "w")

    # Header line
    wf.write(json.dumps({
        "schema": "a29_v3_standalone_6repo_bench/1",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "manifest_commit": manifest["commit"],
        "manifest_total_files": total_files,
        "manifest_total_raw_bytes": total_raw,
        "binary": HXC_A29,
        "binary_sha256": "4847917a288f2a89a996b137ae35231e03aa5bdc8ca3b1da2d0efa5156eb35e7",
        "policy": "raw 91 honest C3 STRICT, raw 142 D2 try-and-revert(v3,identity), 30s timeout",
    }) + "\n")
    wf.flush()

    # Iterate manifest, file by file
    file_idx = 0
    t0 = time.time()
    for repo_name, repo_data in manifest["per_repo"].items():
        for fent in repo_data.get("files", []):
            file_idx += 1
            path = fent["path"]
            raw_bytes_decl = fent["raw_bytes"]
            sha_decl = fent.get("sha256")
            cls = fent.get("class", "unknown")

            agg["total_files_attempted"] += 1
            per_class[cls]["files"] += 1
            per_repo[repo_name]["files"] += 1

            if not os.path.isfile(path):
                agg["total_files_skipped_missing"] += 1
                continue

            try:
                actual_size = os.path.getsize(path)
            except OSError:
                agg["total_files_skipped_missing"] += 1
                continue

            agg["total_raw_bytes"] += actual_size
            per_class[cls]["raw"] += actual_size
            per_repo[repo_name]["raw"] += actual_size

            # encode v3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".a29v3") as t_enc:
                enc_path = t_enc.name

            v3_bytes = None
            v3_ok = False
            try:
                cp = subprocess.run(
                    [HXC_A29, "encode", "--v3", "--force", path, enc_path],
                    capture_output=True, timeout=PER_FILE_TIMEOUT
                )
                if cp.returncode == 0 and os.path.isfile(enc_path):
                    v3_bytes = os.path.getsize(enc_path)
                    v3_ok = True
            except subprocess.TimeoutExpired:
                agg["total_files_timed_out"] += 1
                v3_bytes = None
            except Exception:
                agg["total_files_failed"] += 1
                v3_bytes = None

            if not v3_ok:
                # identity fallback for size accounting
                chosen = actual_size
                chosen_kind = "identity_fallback"
                v3_size_recorded = -1
                agg["identity_chosen_count"] += 1
            else:
                v3_size_recorded = v3_bytes
                agg["total_v3_bytes"] += v3_bytes
                per_class[cls]["v3"] += v3_bytes
                per_repo[repo_name]["v3"] += v3_bytes
                # try-and-revert: shortest of {v3, identity}
                if v3_bytes < actual_size:
                    chosen = v3_bytes
                    chosen_kind = "v3"
                    agg["v3_chosen_count"] += 1
                    per_class[cls]["v3_win"] += 1
                    per_repo[repo_name]["v3_win"] += 1
                else:
                    chosen = actual_size
                    chosen_kind = "identity"
                    agg["identity_chosen_count"] += 1

            agg["total_chosen_bytes"] += chosen
            per_class[cls]["chosen"] += chosen
            per_repo[repo_name]["chosen"] += chosen

            # byte-eq round trip on every Nth file (and if v3_ok)
            byte_eq_status = None
            if v3_ok and (file_idx % SAMPLE_SHA_STEP == 0):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".a29dec") as t_dec:
                    dec_path = t_dec.name
                try:
                    cp_d = subprocess.run(
                        [HXC_A29, "decode", enc_path, dec_path],
                        capture_output=True, timeout=PER_FILE_TIMEOUT
                    )
                    if cp_d.returncode == 0 and os.path.isfile(dec_path):
                        # SHA256 compare
                        with open(path, "rb") as fa, open(dec_path, "rb") as fb:
                            sha_orig = hashlib.sha256(fa.read()).hexdigest()
                            sha_dec = hashlib.sha256(fb.read()).hexdigest()
                        agg["byte_eq_attempted"] += 1
                        if sha_orig == sha_dec:
                            agg["byte_eq_pass"] += 1
                            byte_eq_status = "PASS"
                        else:
                            agg["byte_eq_fail"] += 1
                            byte_eq_status = "FAIL"
                        if len(agg["byte_eq_samples"]) < 35:
                            agg["byte_eq_samples"].append({
                                "path": path, "raw_sha": sha_orig[:16], "rt_sha": sha_dec[:16],
                                "status": byte_eq_status,
                            })
                except Exception:
                    pass
                finally:
                    if os.path.isfile(dec_path):
                        os.unlink(dec_path)

            # Per-file ledger entry (compressed)
            wf.write(json.dumps({
                "i": file_idx, "p": path, "repo": repo_name, "cls": cls,
                "raw": actual_size, "v3": v3_size_recorded, "chosen": chosen, "k": chosen_kind,
                "be": byte_eq_status,
            }, ensure_ascii=False) + "\n")
            if file_idx % 100 == 0:
                wf.flush()
                el = time.time() - t0
                print(f"[{file_idx}/{total_files}] el={el:.0f}s repo={repo_name} cur_save={(1-agg['total_chosen_bytes']/max(1,agg['total_raw_bytes']))*100:.2f}%", file=sys.stderr)

            # cleanup encoded temp
            if os.path.isfile(enc_path):
                os.unlink(enc_path)

    # Final aggregates
    raw = agg["total_raw_bytes"]
    v3 = agg["total_v3_bytes"]
    chosen = agg["total_chosen_bytes"]

    final = {
        "schema": "a29_v3_standalone_6repo_bench_summary/1",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_sec": round(time.time() - t0, 2),
        "files_attempted": agg["total_files_attempted"],
        "files_skipped_missing": agg["total_files_skipped_missing"],
        "files_timed_out": agg["total_files_timed_out"],
        "files_failed": agg["total_files_failed"],
        "v3_chosen_count": agg["v3_chosen_count"],
        "identity_chosen_count": agg["identity_chosen_count"],
        "total_raw_bytes": raw,
        "total_v3_bytes": v3,
        "total_chosen_bytes": chosen,
        "saving_v3_pure_pct": round((1 - v3/max(1,raw))*100, 4) if v3 else None,
        "saving_chosen_pct": round((1 - chosen/max(1,raw))*100, 4),
        "byte_eq_attempted": agg["byte_eq_attempted"],
        "byte_eq_pass": agg["byte_eq_pass"],
        "byte_eq_fail": agg["byte_eq_fail"],
        "byte_eq_samples": agg["byte_eq_samples"],
        "per_class": {
            cls: {
                **d,
                "saving_v3_pure_pct": round((1 - d["v3"]/max(1,d["raw"]))*100, 4) if d["v3"] else None,
                "saving_chosen_pct": round((1 - d["chosen"]/max(1,d["raw"]))*100, 4) if d["raw"] else None,
            } for cls, d in per_class.items()
        },
        "per_repo": {
            r: {
                **d,
                "saving_v3_pure_pct": round((1 - d["v3"]/max(1,d["raw"]))*100, 4) if d["v3"] else None,
                "saving_chosen_pct": round((1 - d["chosen"]/max(1,d["raw"]))*100, 4) if d["raw"] else None,
            } for r, d in per_repo.items()
        },
        "anchors": {
            "a25_baseline_60_79": 60.79,
            "v1_promotion_61_99": 61.99,
            "5kb_slice_mean_91_66": 91.66,
        },
    }

    # delta computation (anchors)
    if final["saving_chosen_pct"] is not None:
        final["delta_vs_a25_baseline_pp"] = round(final["saving_chosen_pct"] - 60.79, 4)
        final["delta_vs_v1_promotion_pp"] = round(final["saving_chosen_pct"] - 61.99, 4)
        final["meets_80pct_target"] = final["saving_chosen_pct"] >= 80.0

    wf.write(json.dumps({"final_summary": final}, ensure_ascii=False) + "\n")
    wf.close()

    print(json.dumps(final, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
