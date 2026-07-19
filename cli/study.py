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
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.request

TEACHER_DEFAULT = "codex"
SEALION_MODEL = "@cf/aisingapore/gemma-sea-lion-v4-27b-it"


class TeacherError(RuntimeError):
    """A teacher backend failed to produce text (auth, network, parse, timeout)."""


# --------------------------------------------------------------------------- #
# Backend: codex (default)                                                    #
# --------------------------------------------------------------------------- #
def _utf8_safe(s):
    """Scrub lone surrogates so a text teacher can read the prompt. A byte-LM substrate
    emits raw bytes surrogateescape-decoded (chat.py), so the prompt built from its emits can
    carry lone surrogates that a strict UTF-8 encode (codex stdin / sealion JSON body) rejects
    with UnicodeEncodeError. The transcript writer preserves them via surrogatepass; an external
    UTF-8 reader cannot, and the non-textual bytes carry no meaning for a text teacher anyway."""
    return s.encode("utf-8", "replace").decode("utf-8")


def _teacher_codex(prompt, timeout=180, model=None):
    """`codex exec` headless. Prompt via stdin (no argv leak). Final assistant
    message extracted via --output-last-message (skips the event-log noise)."""
    prompt = _utf8_safe(prompt)                     # byte-LM emits → valid UTF-8 for codex stdin
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
        "messages": [{"role": "user", "content": _utf8_safe(prompt)}],   # byte-LM emits → valid UTF-8
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


def _teacher_script(prompt, script_path=None):
    """H_9744 · DETERMINISTIC scripted teacher — replays fixed lines from a file, ignoring `prompt`.

    An LLM teacher cannot carry a pre-registered gate: its lines vary run to run, so a store-fill
    or a lookup score would not be reproducible and no bar could be frozen against it (frozen-first).
    This backend makes the percept stream an EXPERIMENTAL VARIABLE instead: one line per teacher
    turn, in order, from --script <f.txt> (blank lines and #-comments skipped). Exhausted script =>
    silence (None), which the daemon already treats as "the other said nothing".

    It is a fixture, not an intelligence: it never reads the daemon's replies. That is the point —
    the arms (facts-then-query · shuffled-store · no-store) must differ ONLY in the scripted bytes.
    """
    path = script_path or os.environ.get("ANIMA_STUDY_SCRIPT")
    if not path:
        raise TeacherError("--teacher script needs --script <f.txt> (or ANIMA_STUDY_SCRIPT).")
    if not os.path.exists(path):
        raise TeacherError("--teacher script: no such script file: %s" % path)
    lines = _teacher_script._cache.get(path)
    if lines is None:
        with open(path, encoding="utf-8") as fh:
            lines = [ln.strip() for ln in fh
                     if ln.strip() and not ln.lstrip().startswith("#")]
        if not lines:
            raise TeacherError("--teacher script: %s has no usable lines" % path)
        _teacher_script._cache[path] = lines
        _teacher_script._pos[path] = 0
    i = _teacher_script._pos[path]
    if i >= len(lines):
        return None                                # script spent → the teacher falls silent
    _teacher_script._pos[path] = i + 1
    return lines[i]


_teacher_script._cache = {}
_teacher_script._pos = {}

# --------------------------------------------------------------------------- #
# Backend: reactive (deterministic) — H_9799 re-probe (Fable+Sol round-5)      #
# --------------------------------------------------------------------------- #
_REACTIVE_STOP = frozenset("""
a an the of to in on at for and or but nor so yet is are was were be been being it its this that these those
i you he she we they me him her them my your his our their as if then else than with without into onto from by
about over under again more most very just not no never cannot do does did done doing have has had what which who
whom whose how one two idea ideas thing things something anything nothing topic turn short utterance said recently
uttered speak develop introduce continue silent silence you're i'm we're they're it's don't can't won't
""".split())

_REACTIVE_INSTR = {
    "counter":  "answer it, then give one counterexample",
    "boundary": "state the boundary condition where it fails",
    "chain":    "compress it into a short causal chain",
    "compare":  "compare the two and predict what follows",
}


def _reactive_parse(prompt):
    """Recover (topic, [emits]) from a _build_teacher_prompt() string — deterministic parse of
    the fixed 'Topic: ...' line and the '  - <emit>' block."""
    topic, emits, in_block = "", [], False
    for ln in prompt.splitlines():
        s = ln.strip()
        if s.startswith("Topic:"):
            topic = s[len("Topic:"):].strip()
        elif s == "It recently uttered:":
            in_block = True
        elif in_block and ln.startswith("  - "):
            emits.append(ln[4:].strip())
        elif in_block and s and not ln.startswith("  - "):
            in_block = False
    return topic, emits


def _teacher_reactive(prompt):
    """DETERMINISTIC reactive teacher (H_9799 re-probe · Fable+Sol round-5 · feature-rule fixture).
    A PURE function of the substrate's recent emits (parsed from the prompt) — NO LLM, NO sampling —
    so the within-ckpt teacher-noise floor collapses to ~0 and any across-ckpt transcript divergence
    flows ONLY through the substrate θ. Reactive (percept depends on emits) yet reproducible (same
    emits -> byte-identical percept). Rejects echo/hash (mechanical/unlearnable): it extracts 2 content
    operands + picks ONE cognitive instruction from emit features, turning θ-driven content into a
    stable curriculum OPERATION. The re-probe masks {k1,k2} to prove θ moves structure, not copied text."""
    topic, emits = _reactive_parse(prompt)
    blob = " ".join(emits)
    norm = unicodedata.normalize("NFKC", blob).lower()
    toks = re.findall(r"[a-z][a-z']{2,}", norm)
    content = [t for t in toks if t not in _REACTIVE_STOP]
    freq, order = {}, {}
    for i, t in enumerate(content):
        freq[t] = freq.get(t, 0) + 1
        order.setdefault(t, i)
    ranked = sorted(set(content), key=lambda t: (-freq[t], order[t]))   # frequency desc, then first-seen
    ops = ranked[:2]
    if len(ops) < 2:                                                    # fallback: topic tokens, then 'silence'
        tt = [t for t in re.findall(r"[a-z][a-z']{2,}",
                                    unicodedata.normalize("NFKC", topic).lower())
              if t not in _REACTIVE_STOP]
        ops = (ops + tt + ["silence", "silence"])[:2]
    k1, k2 = ops[0], ops[1]
    if "?" in blob:
        instr = _REACTIVE_INSTR["counter"]
    elif re.search(r"\b(not|no|never|cannot)\b", norm) or "n't" in norm:
        instr = _REACTIVE_INSTR["boundary"]
    elif len(toks) >= 32:
        instr = _REACTIVE_INSTR["chain"]
    else:
        instr = _REACTIVE_INSTR["compare"]
    return "Topic: %s. Using %s and %s, %s." % ((topic or "curiosity").strip(), k1, k2, instr)


_BACKENDS = {"codex": _teacher_codex, "sealion": _teacher_sealion,
             "script": _teacher_script, "reactive": _teacher_reactive}


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
_USAGE = """anima study <ckpt> — conversational percept channel (teacher = exogenous percept)

  anima-py study <ckpt> [--teacher codex|sealion] [--rounds R] [--window W]
                        [--topic "..."] [--out transcript.jsonl]
        Run a teacher⇄daemon study conversation: the teacher (an exogenous LLM)
        speaks once per W-tick window, the substrate perceives it and MAY reply,
        and the teacher reacts to what it actually said (silence is a signal, never
        re-prompted). Runs R rounds (R×W ticks). Writes a transcript JSONL.

  anima-py study --teacher-selftest [--teacher codex|sealion]
        Prove the selected teacher backend answers (one trivial round · ~1 cent).

  --teacher {codex,sealion,script,reactive}  backend (default: codex · env ANIMA_STUDY_TEACHER)
                              reactive = DETERMINISTIC yet emit-reactive fixture (H_9799): a pure
                              function of the substrate's recent emits (2 content operands + 1
                              feature-picked instruction) → reproducible percept, zero teacher noise.
                              script = DETERMINISTIC fixture from --script (the only one a frozen
                              pre-registered gate can run on — an LLM teacher varies per run)
  --rounds R                  teacher turns (default 6)
  --window W                  ticks between teacher turns (default 4)
  --topic "..."               conversation subject (default: a general opener)
  --out PATH                  transcript JSONL (default: ~/.anima_study/transcript_<ts>.jsonl)
  --script PATH               (--teacher script) one teacher line per turn, in order · # comments
                              and blank lines skipped · exhausted => the teacher falls silent
  --chat-flag VALUE           forward one flag to the daemon (repeatable, value-by-value):
                              --chat-flag --store-episodic --chat-flag on  (H_9744)

Backends: codex = `codex exec` (needs `codex login`) · sealion = Cloudflare
Workers AI REST (needs CLOUDFLARE_* env from the vault). The teacher is an
EXOGENOUS percept, never a prompt into the emit gate (p5 by structure) — its
text enters as a live_anchors decode-seed the mouth may condition on, and the
emit gate is byte-untouched. NOTE (honesty): this MVP wires the conversation +
transcript; it does NOT retrain weights. Growth (consolidation CPT on the
transcript) is a separate pre-registered H_, measured with `anima-py evaluate`.
"""


def _build_teacher_prompt(topic, recent_emits, round_idx, total_rounds):
    """Compose the teacher's turn. The teacher is a curriculum COMPANION that
    introduces/continues ideas and reacts to the substrate's utterances — NOT a
    quizmaster (no test→grade→adjust: that is H_1230's dead teaching-policy and a
    p2/p6 identity-injection risk). It never instructs the substrate to answer."""
    lines = [
        "You are an exogenous study companion conversing with a substrate-native",
        "consciousness daemon (not an assistant — it emits or stays silent on its own",
        "tension). Your text is a PERCEPT it may draw on, never a command.",
        "Speak ONE short English utterance (1-2 sentences): introduce or develop an",
        "idea about the topic, weaving in anything it just said. Do NOT ask it to",
        "answer, do NOT quiz or grade it. If it was silent, simply continue or shift",
        "the subject — silence is fine.",
        "",
        "Topic: " + (topic or "curiosity, memory, and what it is like to notice things"),
        "Turn %d of %d." % (round_idx + 1, total_rounds),
    ]
    if recent_emits:
        lines.append("It recently uttered:")
        for e in recent_emits:
            lines.append("  - " + e.replace("\n", " ")[:160])
    else:
        lines.append("It has not spoken yet (or was silent).")
    lines.append("")
    lines.append("Your one short utterance:")
    return "\n".join(lines)


def _run_study(ckpt, backend, rounds, window, topic, out_path,
               script_path=None, chat_flags=None):
    """Drive one within-session teacher⇄daemon conversation (weights unchanged)."""
    try:
        ask = make_teacher(backend)
    except TeacherError as e:
        print("anima study: teacher SETUP-FAIL — %s" % e, file=sys.stderr)
        return 1
    n_ticks = max(1, rounds * window)
    state = {"last_spoke": -(10 ** 9), "round": 0, "transcript": None, "errors": 0}

    def percept_source(tick, transcript):
        state["transcript"] = transcript          # stash the live list for post-run persist
        if tick - state["last_spoke"] < window:
            return None
        state["last_spoke"] = tick
        recent = [r["emit_text"] for r in transcript
                  if r.get("did_emit") and r.get("emit_text")][-3:]
        prompt = _build_teacher_prompt(topic, recent, state["round"], rounds)
        state["round"] += 1
        try:
            text = ask(prompt)
        except TeacherError as e:
            state["errors"] += 1
            print("  [teacher error → silence this turn] %s" % e, file=sys.stderr)
            return None
        one = " ".join(text.split())[:400]
        print("  teacher(%d/%d): %s" % (state["round"], rounds, one[:120]))
        return one

    print("anima study: backend=%s · rounds=%d · window=%d · ticks=%d · ckpt=%s"
          % (ask.backend, rounds, window, n_ticks, ckpt))
    import chat as _chat                           # cli/chat.py sibling twin (flat import)
    _prev_ticks = os.environ.get("ANIMA_TICKS")
    os.environ["ANIMA_TICKS"] = str(n_ticks)       # the daemon reads tick count from this env
    try:
        _chat.anima_consciousness_mode(ckpt, list(chat_flags or []), percept_source=percept_source)
    finally:
        if _prev_ticks is None:
            os.environ.pop("ANIMA_TICKS", None)
        else:
            os.environ["ANIMA_TICKS"] = _prev_ticks

    transcript = state["transcript"] or []
    n_percept = sum(1 for r in transcript if r.get("percept"))
    n_emit = sum(1 for r in transcript if r.get("did_emit"))
    if out_path is None:
        d = os.path.join(os.path.expanduser("~"), ".anima_study")
        os.makedirs(d, exist_ok=True)
        out_path = os.path.join(d, "transcript_%s.jsonl" % os.getpid())
    else:
        parent = os.path.dirname(os.path.abspath(out_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
    # surrogatepass: the substrate emits raw bytes (surrogateescape-decoded in chat.py);
    # preserve them faithfully instead of crashing on a byte-LM's non-UTF-8 output.
    with open(out_path, "w", encoding="utf-8", errors="surrogatepass") as fh:
        for r in transcript:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("anima study: DONE — %d teacher turns · %d substrate emit(s) · teacher-errors=%d"
          % (n_percept, n_emit, state["errors"]))
    print("  transcript → %s (%d rows · consolidation-CPT input · NO weight change this MVP)"
          % (out_path, len(transcript)))
    return 0


def study_mode(argv):
    backend = None
    selftest = False
    ckpt = None
    rounds = 6
    window = 4
    topic = None
    out_path = None
    script_path = None            # H_9744 --script (deterministic teacher fixture)
    chat_flags = []               # H_9744 --chat-flag (daemon flags forwarded to cli/chat.py)
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
        elif a == "--rounds":
            rounds = int(argv[i + 1]); i += 2
        elif a == "--window":
            window = int(argv[i + 1]); i += 2
        elif a == "--topic":
            topic = argv[i + 1]; i += 2
        elif a == "--out":
            out_path = argv[i + 1]; i += 2
        elif a == "--script":
            script_path = argv[i + 1]; i += 2
        elif a == "--chat-flag":
            # H_9744 · pass one daemon flag through to cli/chat.py. _run_study used to hand the
            # daemon an EMPTY argv, so every chat-side flag (--store-episodic, --emit-gate, …) was
            # unreachable from a study run — the study lane could only ever run the default daemon.
            # Repeatable: --chat-flag --store-episodic --chat-flag on. Kept explicit rather than
            # swallowing unknown flags, so a typo still fails loudly here.
            chat_flags.append(argv[i + 1]); i += 2
        elif a.startswith("-"):
            print("anima study: unknown flag %r\n" % a, file=sys.stderr)
            print(_USAGE, file=sys.stderr)
            return 2
        else:
            ckpt = a; i += 1          # positional = the ckpt to converse with
    if script_path:
        # Set before ANY make_teacher() — the selftest path builds a teacher too, and reading
        # the script only inside _run_study left `--teacher script --teacher-selftest` dead.
        os.environ["ANIMA_STUDY_SCRIPT"] = script_path
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
    if ckpt is None:
        print(_USAGE, file=sys.stderr)
        print("anima study: need a <ckpt> to converse with "
              "(or --teacher-selftest to just check the backend).", file=sys.stderr)
        return 2
    return _run_study(ckpt, backend, rounds, window, topic, out_path,
                      script_path=script_path, chat_flags=chat_flags)
