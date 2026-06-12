#!/usr/bin/env python3
"""h1146_orchestrator.py — CPU-LOCAL orchestrator for the H_1146 anchor fire.

a_cpu_local_no_waiter: runs on the Mac (nohup -> /tmp log), dispatches ONE small
RunPod GPU pod (A40/A6000-class, ~$0.40/h, ~20min), scp's the harnesses, launches
the SELF-TERMINATING pod driver (nohup on-pod, RUNPOD_KEY+RUNPOD_POD_ID exported so
the pod self-terminates), then POLLS INLINE (sleep 30) for H1146_DONE — NO Monitor/
waiter. On DONE: pulls all 3-arm artifacts, then TERMINATES via GraphQL podTerminate
(idempotent — pod may already be self-gone) and 404-VERIFIES (a_fire_recover_complete).

NEVER touches edge-vl-requant (9znqkmzv4v4yfx) or summer rbfe-prod. Tokens via
`secret get` inline. Pod name = anima-h1146-anchor.
"""
import json, os, subprocess, sys, time

ROOT = "/Users/mini/dancinlab/anima"
ART = os.path.join(ROOT, "state/h1146_anchor")
LOG = "/tmp/h1146_orch.log"
# small/cheap GPU; must hold a 14.5GB bf16 7B in inference (needs ~16-24GB). A40 48GB safe.
GPU_CANDIDATES = ["NVIDIA A40", "NVIDIA RTX A6000", "NVIDIA L40S", "NVIDIA A100 80GB PCIe"]
IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04"
POD_NAME = "anima-h1146-anchor"
PROTECTED = {"edge-vl-requant", "9znqkmzv4v4yfx"}  # NEVER terminate these

FILES = [
    "UNIVERSE/h1146_anchor_pod_run.sh",
    "UNIVERSE/h1146_anchor_conditioned_decode.py",
    "UNIVERSE/h1141_7b_g5_eval.py",
    "UNIVERSE/h1143_g5l2_nonfab_measure.py",
    "UNIVERSE/build_wiki5_bigcorpus_en.py",
]

RUNPOD_KEY = None
HF_TOKEN = None


def log(m):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def secret(k):
    s = subprocess.check_output(["secret", "get", k], text=True).strip()
    if s.startswith("[GATE"):
        s = s.split("\n")[-1].strip()
    return s


def _clean_runpod(s):
    if "rpa_" in s:
        s = s[s.index("rpa_"):].split()[0].strip()
    return s


def gql(query):
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://api.runpod.io/graphql",
                        "-H", "Content-Type: application/json",
                        "-H", f"Authorization: Bearer {RUNPOD_KEY}",
                        "-d", json.dumps({"query": query})],
                       capture_output=True, text=True, timeout=60)
    try:
        return json.loads(r.stdout)
    except Exception as e:
        log(f"gql parse FAIL: {e} | {r.stdout[:300]}")
        return None


def runpodctl(args, timeout=180):
    try:
        r = subprocess.run(["runpodctl"] + args, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def _extract_pid(out):
    import re as _re
    m = _re.search(r'pod "([a-z0-9]{8,})" created', out)
    if m:
        return m.group(1)
    try:
        pod = json.loads(out)
        pid = pod.get("id") or pod.get("podId")
        if pid:
            return pid
    except Exception:
        pass
    m = _re.search(r'"([a-z0-9]{10,})"', out)
    if m:
        return m.group(1)
    return None


def pod_create():
    subprocess.run(["runpodctl", "config", "--apiKey", RUNPOD_KEY], capture_output=True, text=True, timeout=30)
    for gpu in GPU_CANDIDATES:
        log(f"creating pod {POD_NAME} ({gpu}) ...")
        base = ["create", "pod", "--name", POD_NAME, "--gpuType", gpu, "--gpuCount", "1",
                "--imageName", IMAGE, "--containerDiskSize", "80",
                "--volumeSize", "0", "--ports", "22/tcp", "--startSSH", "--cost", "1.20"]
        rc, out, err = runpodctl(base + ["--secureCloud"])
        pid = _extract_pid(out)
        if not pid:
            rc, out, err = runpodctl(base + ["--communityCloud"])
            pid = _extract_pid(out)
        if pid:
            log(f"pod created id={pid} gpu={gpu} (raw: {out.strip()[:140]})")
            return pid
        log(f"  {gpu} create FAIL rc={rc} {(out+err)[:160]} -> next gpu")
    return None


def ssh_info(pid):
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


HF_RESULT_REPO = "dancinlab/anima-h1146-anchor-conditioned-decode"


def hf_result_ready():
    """True iff the pod already self-uploaded h1146_anchor_result.json to HF."""
    try:
        r = subprocess.run(
            ["curl", "-s", "-H", f"Authorization: Bearer {HF_TOKEN}",
             f"https://huggingface.co/api/datasets/{HF_RESULT_REPO}/tree/main"],
            capture_output=True, text=True, timeout=40)
        return "h1146_anchor_result.json" in r.stdout
    except Exception:
        return False


def hf_pull_results(dest):
    """Fallback: pull all result JSONs from HF if scp from the pod is unavailable."""
    pulled = []
    for f in ["h1146_anchor_result.json", "h1146_fabrate_uncond.json", "h1146_fabrate_true.json",
              "h1146_fabrate_wrong.json", "g5_result_uncond.json", "g5_result_true.json",
              "g5_result_wrong.json", "h1146.log"]:
        try:
            r = subprocess.run(
                ["curl", "-sL", "-H", f"Authorization: Bearer {HF_TOKEN}", "-o", os.path.join(dest, f),
                 f"https://huggingface.co/datasets/{HF_RESULT_REPO}/resolve/main/{f}"],
                capture_output=True, text=True, timeout=120)
            if r.returncode == 0 and os.path.getsize(os.path.join(dest, f)) > 0:
                pulled.append(f)
        except Exception:
            pass
    return pulled


def pod_terminate(pid):
    log(f"terminating pod {pid} via GraphQL podTerminate ...")
    gql('mutation { podTerminate(input:{podId:"%s"}) }' % pid)
    time.sleep(10)
    q = gql('query { pod(input:{podId:"%s"}) { id desiredStatus } }' % pid)
    pod = (q or {}).get("data", {}).get("pod")
    gone = (q is None) or (pod is None) or (pod.get("desiredStatus") in (None, "TERMINATED", "EXITED"))
    log(f"terminate 404-verify: {json.dumps(q)[:200]} gone={gone}")
    return gone


def main():
    global RUNPOD_KEY, HF_TOKEN
    os.makedirs(ART, exist_ok=True)
    RUNPOD_KEY = _clean_runpod(secret("runpod.api_key"))
    HF_TOKEN = secret("hf.token")
    bal = gql("query { myself { clientBalance } }")
    log(f"balance ${bal['data']['myself']['clientBalance'] if bal else '?'}")

    pid = pod_create()
    if not pid:
        log("ABORT: pod create failed")
        return
    if pid in PROTECTED:
        log("ABORT: refused a protected pod id")
        return

    try:
        time.sleep(30)
        ssh = ssh_info(pid)
        if not ssh:
            log("ABORT: ssh info failed")
            pod_terminate(pid)
            return
        log(f"ssh {ssh['user']}@{ssh['host']}:{ssh['port']}")
        for _ in range(24):
            rc, out, _ = ssh_run(ssh, "echo READY", timeout=30)
            if rc == 0 and "READY" in out:
                break
            time.sleep(10)
        ssh_run(ssh, "mkdir -p /workspace", timeout=30)
        for f in FILES:
            rc, _, err = scp_put(ssh, os.path.join(ROOT, f), f"/workspace/{os.path.basename(f)}")
            log(f"scp {f} rc={rc} {err[:120]}")
        # launch the SELF-TERMINATING pod driver detached; pod self-terminates via these.
        launch = (f"cd /workspace && chmod +x h1146_anchor_pod_run.sh && "
                  f"HF_TOKEN={HF_TOKEN} RUNPOD_KEY={RUNPOD_KEY} RUNPOD_POD_ID={pid} "
                  f"nohup bash h1146_anchor_pod_run.sh > /workspace/h1146_nohup.log 2>&1 & echo LAUNCHED $!")
        rc, out, err = ssh_run(ssh, launch, timeout=60)
        log(f"launch rc={rc} {out.strip()} {err[:120]}")

        # INLINE POLL (a_cpu_local_no_waiter) — no Monitor/waiter
        t0 = time.time()
        done = False
        fail = False
        ssh_fail_streak = 0
        while time.time() - t0 < 60 * 60:  # 60min hard wall (inference-only ~20min)
            time.sleep(30)
            # IMPORTANT: this remote command ALWAYS exits 0 (echo OK at the end), so a
            # non-zero rc means a TRANSPORT failure, never just "DONE not present yet".
            # ssh_run returns rc<0 ONLY on subprocess timeout/exception (true transport
            # failure). A remote exit>0 cannot happen here because we force `; echo OK`.
            rc, out, _ = ssh_run(ssh, "tail -n 3 /workspace/h1146.log 2>/dev/null; "
                                      "if [ -f /workspace/H1146_FAILED ]; then echo FAILEDFLAG; fi; "
                                      "if grep -q H1146_DONE /workspace/h1146.log 2>/dev/null; then echo DONEFLAG; fi; "
                                      "echo OK", timeout=90)
            mins = (time.time() - t0) / 60
            log(f"poll t={mins:.0f}min rc={rc} :: {out.strip()[-300:]}")
            if "DONEFLAG" in out:
                done = True
                break
            if "FAILEDFLAG" in out:
                fail = True
                break
            transport_ok = (rc >= 0) and ("OK" in out)
            # a transient slow/loading ssh must NOT be mistaken for self-termination.
            # The pod self-terminates ONLY after printing H1146_DONE + HF upload, so a
            # genuine self-terminate shows up as the result existing on HF. Require a
            # SUSTAINED streak of TRUE transport failures AND confirm via HF before giving up.
            if transport_ok:
                ssh_fail_streak = 0
            else:
                ssh_fail_streak += 1
            if ssh_fail_streak >= 6:  # ~3min of continuous TRUE unreachability
                log(f"ssh transport unreachable x{ssh_fail_streak} — checking HF for self-terminated result")
                if hf_result_ready():
                    log("HF result present — pod self-terminated after DONE")
                    done = True
                    break
                else:
                    log("HF result NOT yet present — pod may still be running; CONTINUE polling")
                    ssh_fail_streak = 0  # do NOT tear down a possibly-live pod

        # pull artifacts (a_fire_recover_complete) regardless of done/fail
        log("pulling artifacts ...")
        for f in ["h1146.log", "h1146_anchor_result.json",
                  "h1146_fabrate_uncond.json", "h1146_fabrate_true.json", "h1146_fabrate_wrong.json",
                  "g5_result_uncond.json", "g5_result_true.json", "g5_result_wrong.json"]:
            rc, _, _ = scp_get(ssh, f"/workspace/{f}", os.path.join(ART, f))
            if rc == 0:
                log(f"  pulled {f}")
        # if scp got nothing (pod self-terminated), fall back to HF (a_fire_recover_complete)
        if not os.path.exists(os.path.join(ART, "h1146_anchor_result.json")):
            log("scp result missing — HF fallback pull ...")
            got = hf_pull_results(ART)
            log(f"  HF-pulled {got}")
        log(f"done={done} fail={fail}")
    finally:
        if pid not in PROTECTED:
            gone = pod_terminate(pid)
            log(f"TEARDOWN pod {pid} gone={gone}")
    log("H1146 ORCHESTRATOR COMPLETE")


if __name__ == "__main__":
    main()
