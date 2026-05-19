#!/usr/bin/env python3
"""Write pod_s<SEED>.json metadata using `runpodctl pod get <POD_ID>` JSON output.
Polls until ssh.ip+ssh.port populated (max 5 min)."""
import json, subprocess, sys, time, pathlib

def main():
    if len(sys.argv) != 3:
        print("usage: write_pod_meta.py <SEED> <POD_ID>", file=sys.stderr)
        sys.exit(2)
    seed = sys.argv[1]
    pod_id = sys.argv[2]
    out_dir = pathlib.Path("/Users/ghost/core/anima/state/p9_path_a_r16_3seed_2026_05_04")
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / f"pod_s{seed}.json"
    log_path = out_dir / f"write_meta_s{seed}.log"
    name = (
        "anima-p9-pathA-r16-eval-3seed-h100-sxm-secure"
        if seed == "999"
        else f"anima-p9-pathA-r16-s{seed}-h100-sxm-secure"
    )
    log_f = log_path.open("a")
    def log(msg):
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        line = f"[{ts}] [meta-s{seed}] {msg}"
        print(line)
        log_f.write(line + "\n")
        log_f.flush()
    log(f"start pod_id={pod_id}")
    for attempt in range(1, 31):
        try:
            r = subprocess.run(
                ["/opt/homebrew/bin/runpodctl", "pod", "get", pod_id],
                capture_output=True, text=True, timeout=30,
            )
            if r.returncode != 0:
                log(f"runpodctl rc={r.returncode} err={r.stderr.strip()[:200]}")
                time.sleep(10); continue
            d = json.loads(r.stdout)
            ssh = d.get("ssh", {}) or {}
            ip, port = ssh.get("ip"), ssh.get("port")
            status = d.get("desiredStatus")
            log(f"try={attempt} status={status} ssh_ip={ip} ssh_port={port}")
            if ip and port and status == "RUNNING":
                # extra: probe TCP-level SSH readiness
                probe = subprocess.run(
                    ["ssh", "-i", "/Users/ghost/.runpod/ssh/RunPod-Key-Go",
                     "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=8",
                     "-o", "BatchMode=yes", "-p", str(port), f"root@{ip}", "echo ok"],
                    capture_output=True, text=True, timeout=20,
                )
                if probe.returncode == 0 and "ok" in probe.stdout:
                    log(f"SSH OK")
                    meta = {
                        "schema": "anima/p9_path_a_r16_3seed/pod/1",
                        "seed": int(seed),
                        "status": "PROVISIONED",
                        "pod_id": pod_id,
                        "pod_name": name,
                        "ssh_host": ip,
                        "ssh_port": str(port),
                        "captured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    }
                    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
                    log(f"DONE meta={meta_path}")
                    return
                log(f"SSH probe failed rc={probe.returncode}")
        except Exception as e:
            log(f"exception {e!r}")
        time.sleep(10)
    log("TIMEOUT")
    meta_path.write_text(json.dumps({
        "schema": "anima/p9_path_a_r16_3seed/pod/1",
        "seed": int(seed),
        "status": "TIMEOUT_NO_SSH",
        "pod_id": pod_id,
        "captured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2) + "\n")
    sys.exit(4)

if __name__ == "__main__":
    main()
