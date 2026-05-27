#!/usr/bin/env python3
"""anima/_python_bridge/hf_upload_runner.py

THE SINGLE PYTHON FILE FOR HF UPLOAD PIPELINE MK2 (raw#9 disclosure)
====================================================================

raw#9 spirit (hexa-only anima deliverables) is preserved by treating this
file as a vendored runtime dependency rather than as anima source. The
hexa side (tool/hf_upload_mk2.hexa) calls this helper as a subprocess,
streaming a JSON request on stdin and reading a JSON response from stdout.

The reason this one file is python is that:

    huggingface_hub is a python-only SDK with no public C ABI and no
    hexa-callable bindings. The HTTP/multipart/LFS-pointer protocol is
    sufficiently complex (auth, retry, LFS chunked upload, repo creation,
    tag creation, commit metadata) that re-implementing it in hexa is
    not justified for a single upload utility.

The roadmap retires this file when one of the following occurs:
    (a) hexa gains a stdlib http client + LFS pointer encoder, or
    (b) huggingface_hub publishes a CLI with full upload_folder + create_tag
        coverage (current `hf` CLI v1.8.0 lacks tag creation), or
    (c) anima ports to a non-HF distribution channel (S3 + manifest).

Until then, this file is the only .py allowed for the HF upload pipeline.

Contract (stdin -> stdout JSON)
-------------------------------

Input  (one JSON object on stdin):

    {
        "mode":         "upload" | "dry_run" | "selftest",
        "repo":         "<org/name>",
        "ckpt_path":    "<absolute path to folder>",
        "readme_path":  "<absolute path to README.md>",
        "tag":          "<step or version tag>" | null,
        "private":      0 | 1,
        "path_in_repo": "<subdir or empty>" | null,
        "commit_msg":   "<commit message>" | null,
        "token":        "<HF_TOKEN>" | null,
        "audit_dir":    "<absolute path>" | null,
        "max_retries":  3
    }

Output (one JSON object on stdout, single line):

    {
        "ok":           1 | 0,
        "mode":         "upload" | "dry_run" | "selftest",
        "repo":         "<org/name>",
        "tag":          "<tag>" | null,
        "file_count":   <int>,
        "total_bytes":  <int>,
        "sha256_map":   { "<rel_path>": "<sha256>", ... },
        "commit_url":   "<url>" | null,
        "tag_url":      "<url>" | null,
        "duration_sec": <float>,
        "attempts":     <int>,
        "audit_path":   "<absolute path>" | null,
        "message":      "<status string>",
        "error":        "<error class>" | null
    }

Exit codes: always 0 (errors are signalled via ok=0 in the JSON
response). This keeps the proc_run_json_bridge contract clean.

raw#10 caveats:
  - HF rate-limit (HTTP 429) handled by exponential backoff but NOT
    coordinated across concurrent runs — parallel uploads from multiple
    BG subagents may collectively exceed quota.
  - Large file LFS handling is delegated to huggingface_hub; pointer
    files vs raw uploads are not surfaced in the audit log beyond
    sha256 of the local file (NOT the LFS oid on hub side).
  - Naming validation is regex-based on the hexa side; bridge accepts
    any non-empty string for repo / tag (false-negatives possible if
    hexa-side regex is loose).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple


def _emit(obj: Dict[str, Any]) -> None:
    """Single-line JSON to stdout, matches engine_aer bridge contract."""
    sys.stdout.write(json.dumps(obj, separators=(",", ":")))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _read_stdin_json() -> Dict[str, Any]:
    raw = sys.stdin.read()
    return json.loads(raw)


def _sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _walk_files(root: str) -> List[Tuple[str, str, int]]:
    """Return [(rel_path, abs_path, size_bytes), ...] sorted by rel_path."""
    out: List[Tuple[str, str, int]] = []
    if not os.path.isdir(root):
        if os.path.isfile(root):
            return [(os.path.basename(root), root, os.path.getsize(root))]
        return []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip dot-dirs (.git, .ipynb_checkpoints, etc.)
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.startswith("."):
                continue
            ap = os.path.join(dirpath, fn)
            rp = os.path.relpath(ap, root)
            try:
                sz = os.path.getsize(ap)
            except OSError:
                sz = 0
            out.append((rp, ap, sz))
    out.sort(key=lambda t: t[0])
    return out


def _resolve_token(req_token: Optional[str]) -> Optional[str]:
    if req_token:
        return req_token
    env = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if env:
        return env
    home = os.environ.get("HOME", "")
    for p in (
        os.path.join(home, ".huggingface", "token"),
        os.path.join(home, ".cache", "huggingface", "token"),
        "/workspace/.hf_token",
    ):
        if os.path.isfile(p):
            try:
                with open(p, "r") as f:
                    t = f.read().strip()
                if t:
                    return t
            except OSError:
                continue
    return None


def _audit_write(audit_dir: str, repo: str, payload: Dict[str, Any]) -> Optional[str]:
    try:
        os.makedirs(audit_dir, exist_ok=True)
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        safe_repo = repo.replace("/", "__")
        path = os.path.join(audit_dir, "{}_{}.jsonl".format(ts, safe_repo))
        with open(path, "a") as f:
            f.write(json.dumps(payload, separators=(",", ":")))
            f.write("\n")
        return path
    except OSError:
        return None


def _do_dry_run(req: Dict[str, Any]) -> Dict[str, Any]:
    """Walk files + compute sha256 + emit summary. NO network call."""
    t0 = time.time()
    repo = req.get("repo", "")
    ckpt = req.get("ckpt_path", "")
    tag = req.get("tag")
    readme = req.get("readme_path", "")
    files = _walk_files(ckpt)
    sha_map: Dict[str, str] = {}
    total = 0
    for rp, ap, sz in files:
        try:
            sha_map[rp] = _sha256_file(ap)
        except OSError as e:
            sha_map[rp] = "error:" + str(e)
        total += sz
    readme_ok = os.path.isfile(readme) if readme else False
    msg = "dry_run: {} files, {} bytes, readme={}".format(
        len(files), total, "ok" if readme_ok else "missing"
    )
    audit_path = None
    audit_dir = req.get("audit_dir")
    if audit_dir:
        audit_path = _audit_write(audit_dir, repo, {
            "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mode": "dry_run",
            "repo": repo,
            "tag": tag,
            "file_count": len(files),
            "total_bytes": total,
            "sha256_map": sha_map,
            "readme_present": readme_ok,
            "outcome": "dry_run_ok",
        })
    return {
        "ok": 1,
        "mode": "dry_run",
        "repo": repo,
        "tag": tag,
        "file_count": len(files),
        "total_bytes": total,
        "sha256_map": sha_map,
        "commit_url": None,
        "tag_url": None,
        "duration_sec": round(time.time() - t0, 3),
        "attempts": 0,
        "audit_path": audit_path,
        "message": msg,
        "error": None,
    }


def _do_selftest(_req: Dict[str, Any]) -> Dict[str, Any]:
    """Verify the bridge can import huggingface_hub + helpers work.

    Does NOT make any network call. Suitable for hexa-side selftest.
    """
    t0 = time.time()
    checks: List[Dict[str, Any]] = []

    # check 1: huggingface_hub importable
    hf_ok = 0
    hf_ver = None
    try:
        import huggingface_hub  # type: ignore
        hf_ver = getattr(huggingface_hub, "__version__", "unknown")
        hf_ok = 1
    except ImportError as e:
        hf_ver = "import_error:" + str(e)
    checks.append({"name": "huggingface_hub_import", "ok": hf_ok, "info": hf_ver})

    # check 2: sha256 helper round-trip
    try:
        tmp = "/tmp/hf_upload_runner_selftest_{}.bin".format(int(time.time()))
        with open(tmp, "wb") as f:
            f.write(b"anima_hf_upload_mk2_selftest\n")
        sha = _sha256_file(tmp)
        os.remove(tmp)
        sha_ok = 1 if len(sha) == 64 else 0
        checks.append({"name": "sha256_helper", "ok": sha_ok, "info": sha[:16] + "..."})
    except Exception as e:
        checks.append({"name": "sha256_helper", "ok": 0, "info": str(e)})

    # check 3: walk_files on this script's dir
    here = os.path.dirname(os.path.abspath(__file__))
    files = _walk_files(here)
    walk_ok = 1 if any(rp.endswith("hf_upload_runner.py") for rp, _, _ in files) else 0
    checks.append({"name": "walk_files", "ok": walk_ok, "info": "{} files".format(len(files))})

    all_ok = 1 if all(c["ok"] == 1 for c in checks) else 0
    return {
        "ok": all_ok,
        "mode": "selftest",
        "repo": "",
        "tag": None,
        "file_count": 0,
        "total_bytes": 0,
        "sha256_map": {},
        "commit_url": None,
        "tag_url": None,
        "duration_sec": round(time.time() - t0, 3),
        "attempts": 0,
        "audit_path": None,
        "message": "selftest: " + ("PASS" if all_ok == 1 else "FAIL"),
        "error": None,
        "checks": checks,
    }


def _do_upload(req: Dict[str, Any]) -> Dict[str, Any]:
    """Real upload via huggingface_hub.

    Performs:
      1. create_repo(if_not_exists=True)
      2. upload_folder(folder_path, path_in_repo)
      3. create_tag(tag_name) if tag provided
      4. retry with exponential backoff (3 attempts)
      5. audit log
    """
    t0 = time.time()
    repo = req.get("repo", "")
    ckpt = req.get("ckpt_path", "")
    readme = req.get("readme_path", "")
    tag = req.get("tag")
    private = bool(req.get("private", 0))
    path_in_repo = req.get("path_in_repo") or ""
    commit_msg = req.get("commit_msg") or "anima hf_upload_mk2 commit"
    audit_dir = req.get("audit_dir")
    max_retries = int(req.get("max_retries", 3))

    token = _resolve_token(req.get("token"))
    if not token:
        return {
            "ok": 0, "mode": "upload", "repo": repo, "tag": tag,
            "file_count": 0, "total_bytes": 0, "sha256_map": {},
            "commit_url": None, "tag_url": None,
            "duration_sec": round(time.time() - t0, 3),
            "attempts": 0, "audit_path": None,
            "message": "no HF token (HF_TOKEN env or ~/.huggingface/token)",
            "error": "no_token",
        }

    try:
        from huggingface_hub import HfApi  # type: ignore
        from huggingface_hub.utils import HfHubHTTPError  # type: ignore
    except ImportError as e:
        return {
            "ok": 0, "mode": "upload", "repo": repo, "tag": tag,
            "file_count": 0, "total_bytes": 0, "sha256_map": {},
            "commit_url": None, "tag_url": None,
            "duration_sec": round(time.time() - t0, 3),
            "attempts": 0, "audit_path": None,
            "message": "huggingface_hub not installed: " + str(e),
            "error": "huggingface_hub_unavailable",
        }

    # Pre-compute sha256 for audit (before upload, so we record local-side truth).
    files = _walk_files(ckpt)
    sha_map: Dict[str, str] = {}
    total = 0
    for rp, ap, sz in files:
        try:
            sha_map[rp] = _sha256_file(ap)
        except OSError as e:
            sha_map[rp] = "error:" + str(e)
        total += sz

    # Stage README into ckpt dir as README.md if the user passed one separately.
    # We do NOT mutate user dir: we inject into upload_folder's allow_patterns logic.
    # huggingface_hub.upload_folder accepts a folder; if README is outside ckpt, we
    # use upload_file separately. Implementation detail: simpler to always upload
    # the folder, then if readme is outside, upload it as a second op.

    api = HfApi(token=token)
    commit_url: Optional[str] = None
    tag_url: Optional[str] = None
    last_err: Optional[str] = None
    attempts = 0

    for attempt in range(1, max_retries + 1):
        attempts = attempt
        try:
            api.create_repo(
                repo_id=repo,
                repo_type="model",
                private=private,
                exist_ok=True,
                token=token,
            )
            ci = api.upload_folder(
                repo_id=repo,
                folder_path=ckpt,
                path_in_repo=path_in_repo or None,
                commit_message=commit_msg,
                token=token,
            )
            # ci may be a CommitInfo object with .commit_url
            commit_url = getattr(ci, "commit_url", None) or str(ci)
            # Optional: separate README if outside ckpt dir.
            if readme and os.path.isfile(readme):
                inside = os.path.abspath(readme).startswith(os.path.abspath(ckpt) + os.sep)
                if not inside:
                    api.upload_file(
                        path_or_fileobj=readme,
                        path_in_repo="README.md",
                        repo_id=repo,
                        commit_message="anima hf_upload_mk2: README",
                        token=token,
                    )
            if tag:
                try:
                    api.create_tag(
                        repo_id=repo,
                        tag=tag,
                        token=token,
                        exist_ok=True,
                    )
                    tag_url = "https://huggingface.co/{}/tree/{}".format(repo, tag)
                except TypeError:
                    # older huggingface_hub: no exist_ok param
                    try:
                        api.create_tag(repo_id=repo, tag=tag, token=token)
                        tag_url = "https://huggingface.co/{}/tree/{}".format(repo, tag)
                    except HfHubHTTPError as e:
                        # tag may already exist; record but don't fail
                        last_err = "tag_create_warn:" + str(e)
            last_err = None
            break  # success
        except HfHubHTTPError as e:
            last_err = "HfHubHTTPError:" + str(e)
        except Exception as e:
            last_err = type(e).__name__ + ":" + str(e)
        # exponential backoff: 2s, 4s, 8s
        if attempt < max_retries:
            time.sleep(2 ** attempt)

    ok = 1 if last_err is None else 0
    msg = ("upload: {} files, {} bytes, attempts={}".format(len(files), total, attempts)
           if ok == 1 else "upload FAILED after {} attempts: {}".format(attempts, last_err))

    audit_path = None
    if audit_dir:
        audit_path = _audit_write(audit_dir, repo, {
            "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mode": "upload",
            "repo": repo,
            "tag": tag,
            "private": int(private),
            "file_count": len(files),
            "total_bytes": total,
            "sha256_map": sha_map,
            "commit_url": commit_url,
            "tag_url": tag_url,
            "attempts": attempts,
            "duration_sec": round(time.time() - t0, 3),
            "outcome": "ok" if ok == 1 else "fail",
            "error": last_err,
        })

    return {
        "ok": ok,
        "mode": "upload",
        "repo": repo,
        "tag": tag,
        "file_count": len(files),
        "total_bytes": total,
        "sha256_map": sha_map,
        "commit_url": commit_url,
        "tag_url": tag_url,
        "duration_sec": round(time.time() - t0, 3),
        "attempts": attempts,
        "audit_path": audit_path,
        "message": msg,
        "error": last_err,
    }


def main() -> int:
    try:
        req = _read_stdin_json()
    except Exception as e:
        _emit({
            "ok": 0, "mode": "unknown", "repo": "", "tag": None,
            "file_count": 0, "total_bytes": 0, "sha256_map": {},
            "commit_url": None, "tag_url": None,
            "duration_sec": 0.0, "attempts": 0, "audit_path": None,
            "message": "stdin parse error: " + str(e),
            "error": "stdin_parse",
        })
        return 0

    mode = req.get("mode", "selftest")
    try:
        if mode == "selftest":
            resp = _do_selftest(req)
        elif mode == "dry_run":
            resp = _do_dry_run(req)
        elif mode == "upload":
            resp = _do_upload(req)
        else:
            resp = {
                "ok": 0, "mode": mode, "repo": req.get("repo", ""),
                "tag": req.get("tag"), "file_count": 0, "total_bytes": 0,
                "sha256_map": {}, "commit_url": None, "tag_url": None,
                "duration_sec": 0.0, "attempts": 0, "audit_path": None,
                "message": "unknown mode: " + str(mode),
                "error": "unknown_mode",
            }
    except Exception as e:
        resp = {
            "ok": 0, "mode": mode, "repo": req.get("repo", ""),
            "tag": req.get("tag"), "file_count": 0, "total_bytes": 0,
            "sha256_map": {}, "commit_url": None, "tag_url": None,
            "duration_sec": 0.0, "attempts": 0, "audit_path": None,
            "message": "bridge exception: " + str(e),
            "error": type(e).__name__,
            "traceback": traceback.format_exc(),
        }

    _emit(resp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
