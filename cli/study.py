"""anima study — dispatch target for `anima-py study` (percept channel + teacher).

Design (Fable, 2026-07-16): the teacher is anima's FIRST exogenous PERCEPT channel,
NOT a prompt. Teacher text enters the daemon only through the existing perception
routes (immune/afield bind + kosmos live_anchors) — it never touches the emit gate,
so p5 (no reactive self-seed) holds by STRUCTURE, not by rule. Growth is engine-
native (`a_engine_native_learning`): the teacher supplies conversation MATERIAL
(same status as HF human text), never logits/judgements to distill. Cement only via
`anima-py evaluate`. Precedent: H_9111 used an external LLM as a theta-closure-outside
oracle; H_1230 (active-teaching-policy on a clean store) is explicitly NOT repeated —
this measures exogenous-content absorption, not a teaching-method retention curve.

Teacher backend is PLUGGABLE, selected by `--teacher {codex,sealion}` or the
`ANIMA_STUDY_TEACHER` env (default: codex):
  codex   — `codex exec` headless (GPT family · off the Claude quota the research
            frontier runs on · genuinely exogenous model family).
  sealion — Cloudflare Workers AI REST `@cf/aisingapore/gemma-sea-lion-v4-27b-it`
            (pure HTTP · clean JSON · off all quotas · creds via CLOUDFLARE_* env).

The prompt is passed on STDIN (codex) / JSON body (sealion) — never on argv as a
shell string (free-text safe · no shell leak). Base channel stays stdlib-only
(subprocess + urllib) so the numpy-only install keeps working.
"""

import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

TEACHER_DEFAULT = "codex"
SEALION_MODEL = "@cf/aisingapore/gemma-sea-lion-v4-27b-it"


class TeacherError(RuntimeError):
    """A teacher backend failed to produce text (auth, network, parse, timeout)."""


# --------------------------------------------------------------------------- #
# Backend: codex (default)                                                    #
# --------------------------------------------------------------------------- #
def _teacher_codex(prompt, timeout=180, model=None):
    """`codex exec` headless. Prompt via stdin (no argv leak). Final assistant
    message extracted via --output-last-message (skips the event-log noise)."""
    model = model or os.environ.get("ANIMA_STUDY_CODEX_MODEL", "").strip()
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as fh:
        last_path = fh.name
    try:
        cmd = ["codex", "exec", "--skip-git-repo-check", "-o", last_path]
        if model:
            cmd += ["-m", model]
        try:
            proc = subprocess.run(
                cmd, input=prompt, text=True, capture_output=True, timeout=timeout
            )
        except FileNotFoundError:
            raise TeacherError("codex CLI not found on PATH (install codex or use --teacher sealion).")
        except subprocess.TimeoutExpired:
            raise TeacherError("codex exec timed out (%ds)." % timeout)
        out = ""
        try:
            with open(last_path, encoding="utf-8") as fh:
                out = fh.read().strip()
        except OSError:
            out = ""
        if not out:
            err = (proc.stderr or "").strip()
            low = err.lower()
            if "log out and sign in" in err or "unauthorized" in low or "token" in low:
                tail = err.splitlines()[-1] if err else "codex auth failed."
                raise TeacherError(
                    "codex is not authenticated — run `codex login` first "
                    "(or use --teacher sealion). Detail: " + tail
                )
            raise TeacherError("codex exec produced no message (rc=%d). stderr: %s" % (proc.returncode, err[-400:]))
        return out
    finally:
        try:
            os.unlink(last_path)
        except OSError:
            pass


# --------------------------------------------------------------------------- #
# Backend: sealion (option) — Cloudflare Workers AI REST                       #
# --------------------------------------------------------------------------- #
def _teacher_sealion(prompt, timeout=90, max_tokens=512):
    """SEA-LION v4 on Cloudflare Workers AI. Creds from CLOUDFLARE_* env (export
    from the vault; never inlined). OpenAI-style JSON: result.choices[0].message.content."""
    acc = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
    key = os.environ.get("CLOUDFLARE_API_KEY", "").strip()
    email = os.environ.get("CLOUDFLARE_EMAIL", "").strip()
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    if not acc:
        raise TeacherError("CLOUDFLARE_ACCOUNT_ID not set (export cloudflare creds from the vault).")
    url = "https://api.cloudflare.com/client/v4/accounts/%s/ai/run/%s" % (acc, SEALION_MODEL)
    body = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:                                   # scoped API token (preferred)
        headers["Authorization"] = "Bearer " + token
    elif key and email:                         # global API key fallback
        headers["X-Auth-Email"] = email
        headers["X-Auth-Key"] = key
    else:
        raise TeacherError("no Cloudflare auth: set CLOUDFLARE_API_TOKEN, or CLOUDFLARE_API_KEY + CLOUDFLARE_EMAIL.")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        raise TeacherError("SEA-LION REST call failed: %s" % e)
    if not payload.get("success", True):
        raise TeacherError("SEA-LION returned errors: %s" % payload.get("errors"))
    result = payload.get("result") or {}
    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        resp_txt = result.get("response") if isinstance(result, dict) else None
        if isinstance(resp_txt, str) and resp_txt.strip():
            return resp_txt.strip()
        raise TeacherError("SEA-LION response shape unrecognized: %s" % json.dumps(payload)[:400])


_BACKENDS = {"codex": _teacher_codex, "sealion": _teacher_sealion}


def make_teacher(backend=None):
    """Return a callable `ask(prompt) -> text` for the selected backend.

    Selection order: explicit `backend` arg > ANIMA_STUDY_TEACHER env > default (codex).
    """
    name = (backend or os.environ.get("ANIMA_STUDY_TEACHER") or TEACHER_DEFAULT).strip().lower()
    fn = _BACKENDS.get(name)
    if fn is None:
        raise TeacherError(
            "unknown teacher backend %r (choose: %s)" % (name, ", ".join(sorted(_BACKENDS)))
        )

    def ask(prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            raise TeacherError("teacher prompt is empty.")
        return fn(prompt)

    ask.backend = name
    return ask


# --------------------------------------------------------------------------- #
# CLI entry (dispatched from cli/anima.py :: main -> study)                    #
# --------------------------------------------------------------------------- #
_USAGE = """anima study — conversational percept channel (teacher = exogenous percept)

  anima-py study --teacher-selftest [--teacher codex|sealion]
        Prove the selected teacher backend answers (one trivial round · ~1 cent).

  --teacher {codex,sealion}   backend (default: codex · env ANIMA_STUDY_TEACHER)

Backends: codex = `codex exec` (needs `codex login`) · sealion = Cloudflare
Workers AI REST (needs CLOUDFLARE_* env from the vault). The teacher is an
EXOGENOUS percept, never a prompt into the emit gate (p5 by structure).
The full percept-loop (--ckpt, chat wiring, kosmos persistence) lands next.
"""


def study_mode(argv):
    backend = None
    selftest = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-h", "--help"):
            print(_USAGE)
            return 0
        elif a == "--teacher":
            backend = argv[i + 1]
            i += 2
        elif a == "--teacher-selftest":
            selftest = True
            i += 1
        else:
            print("anima study: unknown flag %r\n" % a, file=sys.stderr)
            print(_USAGE, file=sys.stderr)
            return 2
    if selftest:
        try:
            ask = make_teacher(backend)
        except TeacherError as e:
            print("teacher selftest: SETUP-FAIL — %s" % e, file=sys.stderr)
            return 1
        prompt = "You are a teacher opening a study session. Reply with exactly one word: READY"
        print("teacher selftest: backend=%s · asking one trivial round…" % ask.backend)
        try:
            reply = ask(prompt)
        except TeacherError as e:
            print("teacher selftest: 🔴 FAIL — %s" % e, file=sys.stderr)
            return 1
        one = reply.strip().splitlines()[0][:80] if reply.strip() else "(empty)"
        print("teacher selftest: 🟢 OK — backend=%s reply=%r" % (ask.backend, one))
        return 0
    print(_USAGE, file=sys.stderr)
    print("anima study: nothing to do — the percept-loop is not wired yet; "
          "run --teacher-selftest to verify the backend.", file=sys.stderr)
    return 2
