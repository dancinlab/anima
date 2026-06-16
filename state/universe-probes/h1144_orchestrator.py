#!/usr/bin/env python3
"""h1144_orchestrator.py — CPU-LOCAL orchestrator for the H_1144 grounding fire.

a_cpu_local_no_waiter: runs on the Mac (nohup -> /tmp log), dispatches ONE RunPod
H100 SXM 80GB pod, scp's the harnesses, launches the pod driver (nohup on-pod),
then POLLS INLINE (sleep 60) for the H1144_DONE sentinel — NO Monitor/waiter.
On DONE: pulls all artifacts (curves, fab-rate jsons, battery jsons, manifest),
then TERMINATES via GraphQL podTerminate and 404-VERIFIES (a_fire_recover_complete).
The pod self-uploads the result ckpt to HF before DONE, so PULL_FAILED != ckpt-lost.

NEVER touches other pods (edge-vl-requant). Tokens via `secret get` inline.
"""
import json, os, subprocess, sys, time

ROOT = "/Users/mini/dancinlab/anima/.claude/worktrees/agent-ac7bce10c6e042622"
ART = os.path.join(ROOT, "state/h1144_grounding")
LOG = "/tmp/h1144_orch.log"
GPU_ID = "NVIDIA H100 80GB HBM3"
IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04"
POD_NAME = f"anima-h1144-grounding-{int(time.time())}"
PROTECTED = {"edge-vl-requant"}  # NEVER terminate these

FILES = [
    "UNIVERSE/h1144_grounding_pod_run.sh",
    "UNIVERSE/h1144_grounding_train.py",
    "UNIVERSE/h1144_slope_decide.py",
    "UNIVERSE/h1141_7b_g5_eval.py",
    "UNIVERSE/h1143_g5l2_nonfab_measure.py",
    "UNIVERSE/h1141_7b_pass_attempt.py",
    "UNIVERSE/build_wiki5_bigcorpus_en.py",
]


def log(m):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {m}"
    print(line, flush=True)
    with open(LOG, "a") as f: f.write(line + "\n")


def secret(k):
    s = subprocess.check_output(["secret", "get", k], text=True).strip()
    if s.startswith("[GATE"): s = s.split("\n")[-1].strip()
    if "rpa_" in s: s = s[s.index("rpa_"):].split()[0].strip()
    return s


RUNPOD_KEY = None
HF_TOKEN = None


def gql(query):
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.runpod.io/graphql",
                        "-H", "Content-Type: application/json",
                        "-H", f"Authorization: Bearer {RUNPOD_KEY}",
                        "-d", json.dumps({"query": query})],
                       capture_output=True, text=True, timeout=60)
    try:
        return json.loads(r.stdout)
    except Exception as e:
        log(f"gql parse FAIL: {e} | {r.stdout[:300]}"); return None


def runpodctl(args, timeout=180):
    try:
        r = subprocess.run(["runpodctl"] + args, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def _extract_pid(out):
    # runpodctl 2.3.0 create prints e.g. 'pod "<id>" created ...' or json
    try:
        pod = json.loads(out); pid = pod.get("id") or pod.get("podId")
        if pid: return pid
    except Exception:
        pass
    import re as _re
    m = _re.search(r'"([a-z0-9]{10,})"', out)
    if m: return m.group(1)
    for tok in out.replace('"', " ").split():
        if len(tok) >= 12 and tok.isalnum() and any(c.isdigit() for c in tok):
            return tok
    return None


def _extract_pid_v23(out):
    # 2.3.0 prints: pod "<id>" created for $X / hr
    import re as _re
    m = _re.search(r'pod "([a-z0-9]{8,})" created', out)
    if m: return m.group(1)
    return _extract_pid(out)


def pod_create():
    # runpodctl 2.3.0 syntax: `create pod --gpuType ... --imageName ... --secureCloud --startSSH`
    subprocess.run(["runpodctl", "config", "--apiKey", RUNPOD_KEY], capture_output=True, text=True, timeout=30)
    log(f"creating pod {POD_NAME} ({GPU_ID}) SECURE ...")
    base = ["create", "pod", "--name", POD_NAME, "--gpuType", GPU_ID, "--gpuCount", "1",
            "--imageName", IMAGE, "--containerDiskSize", "120",
            "--volumeSize", "0", "--ports", "22/tcp", "--startSSH", "--cost", "4.00"]
    rc, out, err = runpodctl(base + ["--secureCloud"])
    pid = _extract_pid_v23(out)
    if not pid:
        log(f"SECURE create rc={rc} out={(out+err)[:300]} -> retry COMMUNITY")
        rc, out, err = runpodctl(base + ["--communityCloud"])
        pid = _extract_pid_v23(out)
        if not pid:
            log(f"COMMUNITY create FAIL rc={rc} out={(out+err)[:300]}"); return None
    log(f"pod created id={pid} (raw: {out.strip()[:160]})")
    return pid


def ssh_info(pid):
    # 2.3.0 has no `ssh info`; pull connection info from GraphQL runtime ports.
    for _ in range(50):
        q = gql('query { pod(input:{podId:"%s"}) { desiredStatus runtime { ports { ip publicPort privatePort isIpPublic } } } }' % pid)
        try:
            rt = q["data"]["pod"]["runtime"]
            if rt and rt.get("ports"):
                for p in rt["ports"]:
                    if p["privatePort"] == 22 and p["isIpPublic"]:
                        return {"host": p["ip"], "port": p["publicPort"], "user": "root"}
        except Exception:
            pass
        time.sleep(15)
    return None


SSHOPT = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
          "-o", "ConnectTimeout=20", "-o", "ServerAliveInterval=20"]


def ssh_run(ssh, cmd, timeout=600):
    full = ["ssh"] + SSHOPT + ["-p", str(ssh["port"]), f"{ssh['user']}@{ssh['host']}", cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def scp_put(ssh, local, remote, timeout=1200):
    full = ["scp"] + SSHOPT + ["-P", str(ssh["port"]), local, f"{ssh['user']}@{ssh['host']}:{remote}"]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def scp_get(ssh, remote, local, timeout=1200):
    full = ["scp"] + SSHOPT + ["-P", str(ssh["port"]), f"{ssh['user']}@{ssh['host']}:{remote}", local]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def pod_terminate(pid):
    log(f"terminating pod {pid} via GraphQL podTerminate ...")
    gql('mutation { podTerminate(input:{podId:"%s"}) }' % pid)
    time.sleep(10)
    # 404-verify: pod should be gone / EXITED-removed
    q = gql('query { pod(input:{podId:"%s"}) { id desiredStatus } }' % pid)
    gone = (q is None) or (q.get("data", {}).get("pod") is None) or \
           (q.get("data", {}).get("pod", {}) or {}).get("desiredStatus") in (None, "TERMINATED", "EXITED")
    log(f"terminate 404-verify: {json.dumps(q)[:200]} gone={gone}")
    return gone


def main():
    global RUNPOD_KEY, HF_TOKEN
    os.makedirs(ART, exist_ok=True)
    RUNPOD_KEY = secret("runpod.api_key"); HF_TOKEN = secret("hf.token")
    bal = gql("query { myself { clientBalance } }")
    log(f"balance ${bal['data']['myself']['clientBalance'] if bal else '?'}")

    pid = pod_create()
    if not pid:
        log("ABORT: pod create failed"); return
    if pid in PROTECTED:
        log("ABORT: refused to use a protected pod name"); return

    try:
        time.sleep(30)
        ssh = ssh_info(pid)
        if not ssh:
            log("ABORT: ssh info failed (pod up but no connection)"); pod_terminate(pid); return
        log(f"ssh {ssh['user']}@{ssh['host']}:{ssh['port']}")
        # wait for sshd
        for _ in range(20):
            rc, out, _ = ssh_run(ssh, "echo READY", timeout=30)
            if rc == 0 and "READY" in out: break
            time.sleep(10)
        ssh_run(ssh, "mkdir -p /workspace", timeout=30)
        for f in FILES:
            rc, _, err = scp_put(ssh, os.path.join(ROOT, f), f"/workspace/{os.path.basename(f)}")
            log(f"scp {f} rc={rc} {err[:120]}")
        # launch the pod driver detached (nohup); HF_TOKEN exported on-pod
        launch = (f"cd /workspace && chmod +x h1144_grounding_pod_run.sh && "
                  f"HF_TOKEN={HF_TOKEN} nohup bash h1144_grounding_pod_run.sh "
                  f"> /workspace/h1144_nohup.log 2>&1 & echo LAUNCHED $!")
        rc, out, err = ssh_run(ssh, launch, timeout=60)
        log(f"launch rc={rc} {out.strip()} {err[:120]}")

        # INLINE POLL (a_cpu_local_no_waiter) — no Monitor/waiter
        t0 = time.time(); done = False; fail = False
        while time.time() - t0 < 6.5 * 3600:  # 6.5h hard wall (full convergence headroom)
            time.sleep(60)
            rc, out, _ = ssh_run(ssh, "tail -n 3 /workspace/h1144.log 2>/dev/null; "
                                      "ls /workspace/H1144_FAILED 2>/dev/null && echo FAILEDFLAG; "
                                      "grep -q H1144_DONE /workspace/h1144.log 2>/dev/null && echo DONEFLAG", timeout=60)
            mins = (time.time() - t0) / 60
            log(f"poll t={mins:.0f}min :: {out.strip()[-300:]}")
            if "DONEFLAG" in out: done = True; break
            if "FAILEDFLAG" in out: fail = True; break

        # pull artifacts (a_fire_recover_complete) regardless of done/fail
        log("pulling artifacts ...")
        for f in ["h1144.log", "h1144_curve_probe.json", "h1144_curve_converge.json",
                  "h1144_fabrate_probe.json", "h1144_fabrate_converge.json",
                  "h1144_battery_probe.json", "h1144_battery_converge.json",
                  "g5_result_probe.json", "g5_result_converge.json",
                  "h1144_final_manifest.json"]:
            rc, _, _ = scp_get(ssh, f"/workspace/{f}", os.path.join(ART, f))
            if rc == 0: log(f"  pulled {f}")
        log(f"done={done} fail={fail}")
    finally:
        if pid not in PROTECTED:
            gone = pod_terminate(pid)
            log(f"TEARDOWN pod {pid} gone={gone}")
    log("H1144 ORCHESTRATOR COMPLETE")


if __name__ == "__main__":
    main()
