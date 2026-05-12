#!/usr/bin/env python3
"""H100 orchestrator for BG-CONVO-FT-EXTENDED (cycle 2026-05-10).

Resume FT from post_ft_ckpt.pt (BG-CONVO-FT-FIRE result) on extended 166MB
corpus (50% persona-keep + 50% strip + kowiki15) for +20K steps with cosine
LR 5e-6 → 5e-7. Estimated cost $1.50-3.00 (envelope $5-20, well under).

Pattern follows tool/transient_py/anima_km_qwen7b_h100.py with simplifications:
  - no LoRA (full FT, 18M params)
  - no HF gated download (uses local ckpts only)
  - no auto-promote (separate BG handles HF upload, own 37 mandate-9)

own 30 mandates baked in:
  - mandate-1: ckpts pull pre-delete
  - mandate-2: sha256/size verification
  - mandate-3: pod retention on pull fail
  - mandate-5: PEP 668 --break-system-packages

Cost caps:
  - hard cap $15 (kill on $15)
  - early kill $8 (kill if not DONE)
  - wall clock max 90 min
"""
from __future__ import annotations
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

# ----- BG identity -----
BG_ID = "bg_convo_5k_ft_extended_2026_05_10"
CYCLE = "2026-05-10"

# ----- mac paths -----
MAC_STATE_DIR = Path("/Users/ghost/core/anima/state/anima_convo_5k_ft_extended_2026_05_10")
MAC_STATE_DIR.mkdir(parents=True, exist_ok=True)
MAC_RESUME_CKPT = "/Users/ghost/core/anima/state/anima_convo_5k_ft_fire_2026_05_10/post_ft_ckpt.pt"
MAC_CORPUS_PATH = str(MAC_STATE_DIR / "corpus_extended.txt")
MAC_FT_SCRIPT = str(MAC_STATE_DIR / "finetune_extended.py")
MAC_FORWARD_SMOKE = "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/forward_smoke.py"

MAC_LOG_PATH = MAC_STATE_DIR / "orchestrator.log"
MAC_HEARTBEAT_PATH = MAC_STATE_DIR / "heartbeat.json"
MAC_COST_AUDIT_PATH = MAC_STATE_DIR / "cost_audit.jsonl"
MAC_FT_LOG_LOCAL = MAC_STATE_DIR / "ft_log_extended.txt"
MAC_FT_SUMMARY_LOCAL = MAC_STATE_DIR / "ft_summary.json"
MAC_COST_ACTUAL_PATH = MAC_STATE_DIR / "cost_actual.json"

# ----- pod paths -----
POD_ROOT = "/workspace"
POD_RESUME_CKPT = f"{POD_ROOT}/post_ft_ckpt.pt"
POD_CORPUS = f"{POD_ROOT}/corpus_extended.txt"
POD_FT_SCRIPT = f"{POD_ROOT}/finetune_extended.py"
POD_FORWARD_SMOKE = f"{POD_ROOT}/forward_smoke.py"
POD_OUT_PREFIX = f"{POD_ROOT}/convo_5k_ft_ext"
POD_OUT_FINAL = f"{POD_ROOT}/convo_5k_ft_ext_final.pt"
POD_FT_LOG = f"{POD_ROOT}/ft_log_extended.txt"
POD_FT_SUMMARY = f"{POD_ROOT}/ft_summary.json"
POD_TRAIN_STDOUT = f"{POD_ROOT}/train_stdout.log"
POD_HEARTBEAT_DIR = f"{POD_ROOT}/state"
POD_HEARTBEAT_JSON = f"{POD_HEARTBEAT_DIR}/heartbeat.json"
POD_VERDICT_JSON = f"{POD_HEARTBEAT_DIR}/verdict.json"

# ----- runpod config -----
COST_PER_HOUR = 2.99  # H100 SXM secure
COST_HARD_CAP_USD = 15.0
COST_EARLY_KILL_USD = 8.0
WALL_CLOCK_CAP_S = 90 * 60  # 90 minutes
GPU_ID = "NVIDIA H100 80GB HBM3"

# ----- training params -----
FT_STEPS = 20000
FT_BATCH = 32
FT_SEQ = 256
FT_LR_MAX = 5e-6
FT_LR_MIN = 5e-7
FT_WARMUP = 200
FT_SAVE_EVERY = 5000


def orch_log(msg):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(MAC_LOG_PATH, "a") as f:
        f.write(line + "\n")


def runpodctl(args, timeout=180):
    cmd = ["runpodctl"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -2, "", str(e)


def get_balance():
    api_key = subprocess.check_output(["secret", "get", "runpod.api_key"], text=True).strip()
    # strip GATE prefix
    if api_key.startswith("[GATE"):
        api_key = api_key.split("\n")[-1].strip()
    if "rpa_" in api_key:
        api_key = api_key[api_key.index("rpa_"):].split()[0].strip()
    r = subprocess.run([
        "curl", "-s", "-X", "POST", "https://api.runpod.io/graphql",
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {api_key}",
        "-d", '{"query":"query { myself { clientBalance } }"}',
    ], capture_output=True, text=True, timeout=30)
    try:
        return float(json.loads(r.stdout)["data"]["myself"]["clientBalance"])
    except Exception as e:
        orch_log(f"balance query parse FAIL: {e} | {r.stdout[:200]}")
        return None


def pod_create():
    orch_log("creating H100 SXM pod (SECURE cloud)…")
    args = [
        "pod", "create",
        "--name", f"anima-convo-ext-{int(time.time())}",
        "--gpu-id", GPU_ID,
        "--gpu-count", "1",
        "--cloud-type", "SECURE",
        "--template-id", "runpod-torch-v280",
        "--container-disk-in-gb", "60",
        "--volume-in-gb", "0",
        "--ports", "22/tcp",
        "--ssh",
    ]
    rc, out, err = runpodctl(args, timeout=180)
    if rc != 0:
        orch_log(f"pod create SECURE FAIL rc={rc} err={err[:300]}")
        orch_log("retrying COMMUNITY…")
        args[args.index("SECURE")] = "COMMUNITY"
        rc, out, err = runpodctl(args, timeout=180)
        if rc != 0:
            orch_log(f"pod create COMMUNITY FAIL rc={rc} err={err[:300]}")
            return None
    try:
        pod = json.loads(out)
        pod_id = pod.get("id") or pod.get("podId")
        orch_log(f"pod created: id={pod_id} machine={pod.get('machineId','?')} ${pod.get('costPerHr','?')}/hr")
        return pod_id
    except Exception as e:
        orch_log(f"pod create parse FAIL: {e} | out={out[:300]}")
        return None


def pod_delete(pod_id):
    rc, out, err = runpodctl(["pod", "remove", pod_id], timeout=60)
    orch_log(f"pod delete rc={rc} out={out[:200]}")
    return rc == 0


def ssh_info(pod_id):
    for i in range(40):
        rc, out, err = runpodctl(["ssh", "info", pod_id], timeout=30)
        if rc == 0 and out:
            try:
                info = json.loads(out)
                host = info.get("host") or info.get("ip")
                port = info.get("port", 22)
                user = info.get("user", "root")
                if host:
                    return {"host": host, "port": port, "user": user}
            except Exception:
                pass
        time.sleep(15)
    return None


def ssh_run(ssh, cmd, timeout=300):
    full = ["ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15",
            "-o", "ServerAliveInterval=15",
            "-p", str(ssh["port"]),
            f"{ssh['user']}@{ssh['host']}", cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def scp_put(ssh, local, remote, timeout=900):
    full = ["scp", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15",
            "-P", str(ssh["port"]),
            local, f"{ssh['user']}@{ssh['host']}:{remote}"]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def scp_get(ssh, remote, local, timeout=900):
    full = ["scp", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15",
            "-P", str(ssh["port"]),
            f"{ssh['user']}@{ssh['host']}:{remote}", local]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def sha256_file(path):
    r = subprocess.run(["shasum", "-a", "256", path], capture_output=True, text=True)
    return r.stdout.split()[0] if r.returncode == 0 else None


def main():
    orch_log(f"=== {BG_ID} EXTENDED orchestrator started ===")
    orch_log(f"resume_ckpt={MAC_RESUME_CKPT}")
    orch_log(f"corpus={MAC_CORPUS_PATH}")
    orch_log(f"COST_HARD_CAP=${COST_HARD_CAP_USD} EARLY_KILL=${COST_EARLY_KILL_USD}")

    # Pre-flight checks
    if not Path(MAC_RESUME_CKPT).exists():
        orch_log(f"ABORT: resume ckpt missing")
        return
    if not Path(MAC_CORPUS_PATH).exists():
        orch_log(f"ABORT: corpus missing")
        return
    if not Path(MAC_FT_SCRIPT).exists():
        orch_log(f"ABORT: FT script missing")
        return
    if not Path(MAC_FORWARD_SMOKE).exists():
        orch_log(f"ABORT: forward_smoke.py missing")
        return

    bal_before = get_balance()
    orch_log(f"balance_before: ${bal_before}")

    pod_id = pod_create()
    if not pod_id:
        orch_log("ABORT: pod create failed")
        return

    t_start = time.time()
    cost_actual = 0.0
    ckpts_pulled = False

    try:
        time.sleep(30)
        ssh = ssh_info(pod_id)
        if not ssh:
            orch_log("ABORT: ssh info failed")
            return
        orch_log(f"ssh ready: {ssh['user']}@{ssh['host']}:{ssh['port']}")

        # GPU smoke
        rc, out, err = ssh_run(ssh,
            "python3 -c 'import torch; print(\"torch=\"+torch.__version__,\"cuda=\"+str(torch.cuda.is_available())); import subprocess; subprocess.run([\"nvidia-smi\",\"--query-gpu=name\",\"--format=csv\"])'",
            timeout=120)
        orch_log(f"GPU smoke rc={rc} out={out[:300]}")

        # mkdir
        ssh_run(ssh, f"mkdir -p {POD_HEARTBEAT_DIR}", timeout=30)

        # Stage files
        orch_log("staging resume ckpt (74MB)…")
        rc, _, err = scp_put(ssh, MAC_RESUME_CKPT, POD_RESUME_CKPT, timeout=600)
        orch_log(f"  scp ckpt rc={rc} err={err[:200]}")
        if rc != 0:
            orch_log("ABORT: ckpt upload failed")
            return

        orch_log("staging corpus (166MB)…")
        # gzip first to speed up
        corpus_gz = MAC_CORPUS_PATH + ".gz"
        if not os.path.exists(corpus_gz) or os.path.getmtime(corpus_gz) < os.path.getmtime(MAC_CORPUS_PATH):
            orch_log("  compressing corpus…")
            subprocess.run(["bash", "-c", f"gzip -c -1 {shlex.quote(MAC_CORPUS_PATH)} > {shlex.quote(corpus_gz)}"], check=True, timeout=180)
        sz_gz = os.path.getsize(corpus_gz) / 1e6
        orch_log(f"  corpus.gz size={sz_gz:.1f}MB")
        rc, _, err = scp_put(ssh, corpus_gz, f"{POD_ROOT}/corpus_extended.txt.gz", timeout=900)
        orch_log(f"  scp corpus.gz rc={rc}")
        if rc != 0:
            orch_log("ABORT: corpus upload failed")
            return
        rc, out, err = ssh_run(ssh, f"cd {POD_ROOT} && gunzip -c corpus_extended.txt.gz > {POD_CORPUS} && ls -la {POD_CORPUS}", timeout=120)
        orch_log(f"  decompress rc={rc} out={out[:200]}")

        orch_log("staging FT script + forward_smoke.py…")
        scp_put(ssh, MAC_FT_SCRIPT, POD_FT_SCRIPT, timeout=60)
        scp_put(ssh, MAC_FORWARD_SMOKE, POD_FORWARD_SMOKE, timeout=60)

        # CUDA dry-run smoke (5 step on tiny portion to verify)
        orch_log("CUDA dry-run (5 step smoke)…")
        cmd_dry = (f"cd {POD_ROOT} && python3 {POD_FT_SCRIPT} "
                   f"--ckpt {POD_RESUME_CKPT} --corpus {POD_CORPUS} "
                   f"--out {POD_ROOT}/dryrun.pt --out-prefix {POD_ROOT}/dryrun "
                   f"--log {POD_ROOT}/dryrun.log --summary {POD_ROOT}/dryrun_summary.json "
                   f"--steps 5 --batch 4 --seq 64 --lr 1e-6 --lr-min 1e-7 --warmup 1 --device cuda --save-every 0 2>&1 | tail -20")
        rc, out, err = ssh_run(ssh, cmd_dry, timeout=180)
        orch_log(f"dry-run rc={rc} out_tail={out[-800:]}")
        if rc != 0:
            orch_log(f"ABORT: dry-run failed err={err[:300]}")
            return

        # Launch main training
        orch_log("launching main training (20K step on H100)…")
        launch_cmd = (
            f"cd {POD_ROOT} && nohup python3 {POD_FT_SCRIPT} "
            f"--ckpt {POD_RESUME_CKPT} --corpus {POD_CORPUS} "
            f"--out {POD_OUT_FINAL} --out-prefix {POD_OUT_PREFIX} "
            f"--log {POD_FT_LOG} --summary {POD_FT_SUMMARY} "
            f"--steps {FT_STEPS} --batch {FT_BATCH} --seq {FT_SEQ} "
            f"--lr {FT_LR_MAX} --lr-min {FT_LR_MIN} --warmup {FT_WARMUP} "
            f"--device cuda --save-every {FT_SAVE_EVERY} "
            f"> {POD_TRAIN_STDOUT} 2>&1 & echo PID=$!"
        )
        rc, out, err = ssh_run(ssh, launch_cmd, timeout=30)
        orch_log(f"launch rc={rc} out={out[:200]}")

        # Heartbeat monitor
        last_log_size = 0
        for tick in range(int(WALL_CLOCK_CAP_S / 30) + 5):
            time.sleep(30)
            elapsed = time.time() - t_start
            cost_actual = elapsed / 3600 * COST_PER_HOUR

            # tail train stdout
            rc, out, err = ssh_run(ssh,
                f"wc -l {POD_TRAIN_STDOUT} 2>/dev/null; tail -5 {POD_TRAIN_STDOUT} 2>/dev/null",
                timeout=30)
            tail_info = out.strip().replace("\n", " | ")[:300]

            # check if final ckpt exists (= done)
            rc_done, done_out, _ = ssh_run(ssh,
                f"ls -la {POD_OUT_FINAL} {POD_FT_SUMMARY} 2>/dev/null", timeout=30)
            done = (POD_OUT_FINAL.split('/')[-1] in (done_out or "")) and (POD_FT_SUMMARY.split('/')[-1] in (done_out or ""))

            mac_hb = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                      "elapsed_s": round(elapsed, 1),
                      "cost_actual_usd": round(cost_actual, 3),
                      "pod_id": pod_id,
                      "tail": tail_info,
                      "done": done}
            json.dump(mac_hb, open(MAC_HEARTBEAT_PATH, "w"), indent=2)
            with open(MAC_COST_AUDIT_PATH, "a") as f:
                f.write(json.dumps(mac_hb) + "\n")

            orch_log(f"hb tick={tick} cost=${cost_actual:.2f} done={done} tail=[{tail_info[-150:]}]")

            if done:
                orch_log("training DONE detected — proceeding to pull")
                break
            if cost_actual > COST_HARD_CAP_USD:
                orch_log(f"COST_HARD_CAP_HIT ${cost_actual:.2f} — kill")
                break
            if cost_actual > COST_EARLY_KILL_USD and not done:
                orch_log(f"COST_EARLY_KILL ${cost_actual:.2f} — kill")
                break

        # Pull artifacts
        orch_log("pulling artifacts (ft_log, summary, ckpts)…")
        rc, _, err = scp_get(ssh, POD_FT_LOG, str(MAC_FT_LOG_LOCAL), timeout=120)
        orch_log(f"  pull ft_log rc={rc}")
        rc, _, err = scp_get(ssh, POD_FT_SUMMARY, str(MAC_FT_SUMMARY_LOCAL), timeout=60)
        orch_log(f"  pull summary rc={rc}")
        rc, _, err = scp_get(ssh, POD_TRAIN_STDOUT, str(MAC_STATE_DIR / "train_stdout.log"), timeout=60)
        orch_log(f"  pull stdout rc={rc}")

        # Final ckpt + intermediate ckpts
        ckpt_pulls = []
        for label, remote, local in [
            ("final", POD_OUT_FINAL, str(MAC_STATE_DIR / "post_ft_ext_ckpt.pt")),
            ("step_5000", f"{POD_OUT_PREFIX}_step_5000.pt", str(MAC_STATE_DIR / "convo_5k_ft_ext_step_5000.pt")),
            ("step_10000", f"{POD_OUT_PREFIX}_step_10000.pt", str(MAC_STATE_DIR / "convo_5k_ft_ext_step_10000.pt")),
            ("step_15000", f"{POD_OUT_PREFIX}_step_15000.pt", str(MAC_STATE_DIR / "convo_5k_ft_ext_step_15000.pt")),
            ("step_20000", f"{POD_OUT_PREFIX}_step_20000.pt", str(MAC_STATE_DIR / "convo_5k_ft_ext_step_20000.pt")),
        ]:
            rc, _, err = scp_get(ssh, remote, local, timeout=600)
            ckpt_pulls.append({"label": label, "rc": rc, "err": err[:200]})
            orch_log(f"  pull {label} rc={rc}")

        # Verify pull (own 30 mandate-2)
        final_local = MAC_STATE_DIR / "post_ft_ext_ckpt.pt"
        if final_local.exists() and final_local.stat().st_size > 50_000_000:
            local_sha = sha256_file(str(final_local))
            rc, pod_sha_out, _ = ssh_run(ssh, f"sha256sum {POD_OUT_FINAL} | awk '{{print $1}}'", timeout=30)
            pod_sha = pod_sha_out.strip() if rc == 0 else None
            sha_ok = (local_sha == pod_sha) if (local_sha and pod_sha) else False
            orch_log(f"sha256 verify: local={local_sha[:16] if local_sha else None}... pod={pod_sha[:16] if pod_sha else None}... match={sha_ok}")
            ckpts_pulled = sha_ok
        else:
            orch_log(f"  WARN: final ckpt local missing or too small")
            ckpts_pulled = False

    finally:
        if ckpts_pulled:
            orch_log("deleting pod (ckpts verified)…")
            pod_delete(pod_id)
        else:
            orch_log("RETAIN POD per own 30 mandate-3 (ckpts pull not verified)")
            with open(MAC_STATE_DIR / "POD_RETAINED_FOR_MANUAL_RECOVERY.txt", "w") as f:
                f.write(f"pod_id={pod_id}\nreason=ckpts_pull_not_verified\n")

        bal_after = get_balance()
        cost_final = (bal_before - bal_after) if (bal_before is not None and bal_after is not None) else None
        orch_log(f"balance_after: ${bal_after}  cost_final=${cost_final}")

        cost_data = {
            "fire_date": "2026-05-10",
            "bg": BG_ID,
            "provider": "runpod",
            "pod_id": pod_id,
            "gpu": GPU_ID,
            "balance_before_usd": bal_before,
            "balance_after_usd": bal_after,
            "actual_cost_usd": cost_final,
            "wall_clock_estimated_cost_usd": round(cost_actual, 3),
            "envelope_authorized_usd": "5-20",
            "ckpts_pulled_verified": ckpts_pulled,
            "elapsed_s": round(time.time() - t_start, 1),
        }
        with open(MAC_COST_ACTUAL_PATH, "w") as f:
            json.dump(cost_data, f, indent=2)
        orch_log(f"orchestrator done: cost=${cost_final} wall={time.time()-t_start:.0f}s ckpts_ok={ckpts_pulled}")


if __name__ == "__main__":
    main()
