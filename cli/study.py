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
    effort = os.environ.get("ANIMA_STUDY_CODEX_EFFORT", "").strip()
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as fh:
        last_path = fh.name
    try:
        cmd = ["codex", "exec", "--skip-git-repo-check", "-o", last_path]
        if model:
            cmd += ["-m", model]
        if effort:
            # A study turn is one short utterance — the default reasoning budget is spent on
            # nothing here, and low effort keeps a long run from costing more than the run.
            cmd += ["-c", "model_reasoning_effort=" + effort]
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
  --model NAME                (--teacher codex) teacher model, e.g. gpt-5.4-mini
                              (env ANIMA_STUDY_CODEX_MODEL)
  --effort LEVEL              (--teacher codex) model_reasoning_effort, e.g. low
                              (env ANIMA_STUDY_CODEX_EFFORT)
  --coach                     add a DESCRIPTIVE state note (emit count · silence streak ·
                              repetition) to the teacher prompt. State only, never a teaching
                              POLICY — p2/p3/p6 forbid a curriculum injection and H_1230
                              already measured test→grade→adjust dead. Changes percept bytes,
                              so default OFF (a run without it stays byte-identical).
  --max-words N               reject a teacher utterance longer than N words (0 = no cap).
                              Empty / duplicate-of-previous are rejected regardless: one retry
                              with a terse reminder, then silence. Rejections are counted and
                              persisted — a degenerate teacher makes the run INVALID, and
                              without this it was invisible in the transcript.
  --report PATH               write a run-summary JSON (config + teacher errors/rejects +
                              growth telemetry)

Growth telemetry (always on · transcript-side · $0 · DIRECTIONAL, moves no frozen bar):
  borrow_ratio   emit tokens that appeared in some earlier percept — "did the teacher's
                 words reach the mouth at all". This is the PEDESTAL.
  recomb_index   emit bigrams NOT present inside any ONE teacher utterance — composed
                 across utterances rather than echoed as a span.
  ⚠️ recomb_index alone is not composition evidence: a substrate that ignores the teacher
  scores 1.0 with nothing shared to echo. Read jointly — borrow HIGH+recomb HIGH = COMPOSE,
  borrow HIGH+recomb LOW = ECHO, borrow LOW = DETACHED (recomb VOID). Terminal reading is
  still `anima-py evaluate`; these are conversation statistics, not a verdict.
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


# --------------------------------------------------------------------------- #
# Growth telemetry — echo vs. recombination (transcript-side · $0 · no forward) #
# --------------------------------------------------------------------------- #
# Ported from anima-clm-v2's teach_dialogue.py `recomb_index`, with the pedestal the
# original lacked. A study run currently reports only "N teacher turns · M emits", which
# cannot distinguish the substrate DRAWING ON the percept from PARROTING it — the exact
# echo-vs-composition question the ρ·weave (recombination) wall is about. These are
# transcript statistics, never a verdict: they move no frozen bar and cement nothing
# (`a_engine_native_learning` — terminal reading stays `anima-py evaluate`).
#
# ⚠️ recomb_index ALONE is not evidence of composition, and reading it alone manufactures
# a positive: a substrate that ignores the teacher entirely scores 1.0 (no shared bigram
# to echo). It is only interpretable jointly with borrow_ratio, which is the "did the
# percept reach the mouth at all" pedestal:
#
#     borrow HIGH + recomb HIGH  → COMPOSE   (teacher's words, edges the teacher never said)
#     borrow HIGH + recomb LOW   → ECHO      (parroting whole spans back)
#     borrow LOW                 → DETACHED  (percept never reached the mouth · recomb VOID)
#
_WORD = re.compile(r"[가-힣]+|[A-Za-z][A-Za-z']*")


def _toks(text):
    return _WORD.findall(unicodedata.normalize("NFKC", text or "").lower())


def _bigrams(text):
    w = _toks(text)
    return {(w[i], w[i + 1]) for i in range(len(w) - 1)}


def _regime_of(borrow_content, recomb_index, n_shared, is_repeat):
    """Classify ONE emit.

    REPEAT is a within-run invariance CONTROL, not a threshold: an utterance byte-identical
    to one the substrate already produced under a DIFFERENT percept cannot have been caused
    by this percept, so it carries zero evidence of uptake and is excluded from the counts.
    Measured live: the substrate emitted the same frozen `vault QX-7741 …` string under four
    different teacher turns and scored COMPOSE four times.

    n_shared>=2 gates COMPOSE because ONE shared content word is a lexical collision, not
    uptake — in that same run the teacher's opening happened to contain "vault", which alone
    lifted the unchanged regurgitation over the borrow floor. A single token is INCONCLUSIVE.
    """
    if borrow_content is None or recomb_index is None:
        return "TOO-SHORT"
    if is_repeat:
        return "REPEAT"
    if borrow_content <= 0.10 or n_shared == 0:
        return "DETACHED"
    if n_shared < 2:
        return "INCONCLUSIVE"
    return "COMPOSE" if recomb_index >= 0.5 else "ECHO"


def _repeat_dv(transcript):
    """H_9984 ② pre-registered DV — computed on EVERY return path below, because a REPEAT-dominated
    run exits through the NO-EVIDENCE branch and that is precisely the run this question is about.

    `modal_emit_share` — the largest byte-identical emit's share of all emits. The kill condition is
    stated on exactly this number (40 of 60 = 0.667 in the pre-wiring 40-turn run), NOT on the
    REPEAT class count, which is a per-emit label and moves for reasons of its own.
    `seed_distinct*` — unique decode-seed fingerprints over rows (`seed_sha8`, written by chat.py
    from the anchor the mouth ACTUALLY consumed). This is the MOVEMENT witness: the kill only reads
    if the seed genuinely moved turn to turn, so a run where it did not is INVALID for the question
    rather than a negative (`flat-across-manipulations-means-the-lane-is-dead`). The silent-tick
    split is the one that matters — the do() only touches percept-SILENT ticks.
    Older transcripts carry no `seed_sha8`; those read 0/0 (absent), never a fabricated 1.0.

    ⚠️ STRATIFIED BY CONSTRUCTION (`study-py-1`(e) — the defect this file has already made once):
    the do() touches ONLY percept-SILENT ticks, so the headline denominator is the SILENT stratum.
    Pooling the percept-present emits — which the manipulation never reached — into the headline is
    exactly the error that once flipped this file's conclusion. `modal_emit_share_all` is kept as a
    SECOND layer only because the card's quoted 0.667 was taken over all 60 emits; it is continuity
    with that number, not the DV.
    """
    def _modal(_rows):
        _e = [r.get("emit_text") for r in _rows if r.get("did_emit") and r.get("emit_text")]
        if not _e:
            return (None, 0, 0)
        _c = {}
        for _t in _e:
            _c[_t] = _c.get(_t, 0) + 1
        return (round(max(_c.values()) / float(len(_e)), 4), max(_c.values()), len(_e))

    silent = [r for r in transcript if not r.get("percept")]
    seeded = [r for r in transcript if r.get("percept")]
    fps = [r.get("seed_sha8") for r in transcript if r.get("seed_sha8")]
    fps_silent = [r.get("seed_sha8") for r in silent if r.get("seed_sha8")]
    m_sil, c_sil, n_sil = _modal(silent)       # ← the DV (the manipulated stratum)
    m_per, c_per, n_per = _modal(seeded)       # untouched stratum, reported separately
    m_all, c_all, n_all = _modal(transcript)   # continuity with the card's quoted 0.667
    return {"emits_total": n_all,
            "modal_emit_share": m_sil, "modal_emit_count": c_sil, "modal_emit_n": n_sil,
            "modal_emit_share_percept": m_per, "modal_emit_n_percept": n_per,
            "modal_emit_share_all": m_all, "modal_emit_count_all": c_all,
            "seed_distinct": len(set(fps)), "seed_rows": len(fps),
            "seed_distinct_silent": len(set(fps_silent)), "seed_rows_silent": len(fps_silent),
            "pw_arm": next((r.get("pw_arm") for r in transcript if r.get("pw_arm")), None)}


def _growth_metrics(transcript):
    """Annotate transcript rows in place with echo/recombination telemetry + return a summary.

    `seen_bigrams` accumulates bigrams occurring WITHIN A SINGLE teacher utterance. An emit
    bigram absent from that set was composed across DIFFERENT utterances (or from the
    substrate's own weights) — that is the recombination sense, and it is why the union is
    built per-utterance rather than over the concatenated teacher stream.
    """
    seen_bigrams, seen_tokens, emitted_tokens = set(), set(), set()
    emits, rows = [], []
    for r in transcript:
        percept = r.get("percept")
        if percept:
            seen_bigrams |= _bigrams(percept)
            # TEACHER-ORIGINATED only. The teacher is prompted with the substrate's recent
            # emits and weaves them in, so a percept echoes the substrate's own words back —
            # crediting those as "borrow" launders a self-loop into evidence that the teacher
            # reached the mouth. Measured live: the substrate regurgitated "vault QX-7741",
            # the teacher answered "A vault like QX-7741 feels less like storage…", and the
            # substrate re-emitting its own signature scored shared_terms=[qx, vault] ⇒ a
            # COMPOSE reading built entirely on the substrate's own prior output. A token the
            # substrate already said is not exogenous content, so it can never enter the
            # pedestal (same reason p5 forbids a reactive self-seed).
            seen_tokens |= {t for t in _toks(percept) if t not in emitted_tokens}
        if not (r.get("did_emit") and r.get("emit_text")):
            continue
        text = r["emit_text"]
        eb, et = _bigrams(text), _toks(text)
        # Measured against percepts seen BEFORE this emit — a later teacher turn cannot
        # retroactively make an earlier utterance an echo.
        echo = round(len(eb & seen_bigrams) / len(eb), 4) if eb else None
        borrow = round(sum(1 for t in et if t in seen_tokens) / len(et), 4) if et else None
        # CONTENT borrow is the one the regime reads. Function words ("the", "is", "of")
        # overlap between ANY two English strings, so a raw token borrow has a large
        # content-free floor that never drops to the DETACHED band — the first live run
        # scored a training-data regurgitation ("vault QX-7741 ... Alabama States") at
        # borrow 0.259 and mislabelled it COMPOSE. Chance is derived per metric
        # (`chance-level-must-be-derived-per-metric`): the stopword floor is removed rather
        # than a threshold picked to sit above it. NOTE: the stoplist is English-only, so a
        # Korean run's content set is all its 한글 tokens (no function-word floor to remove).
        ect = [t for t in et if t not in _REACTIVE_STOP]
        shared = [t for t in ect if t in seen_tokens]
        r["echo_ratio"] = echo
        r["recomb_index"] = None if echo is None else round(1.0 - echo, 4)
        r["borrow_ratio"] = borrow
        r["borrow_content"] = round(len(shared) / len(ect), 4) if ect else None
        r["shared_terms"] = sorted(set(shared))[:12]
        r["regime"] = _regime_of(r["borrow_content"], r["recomb_index"],
                                 len(set(shared)), text in emits)
        emitted_tokens |= set(et)      # after scoring: this emit's words are now the substrate's
        emits.append(text)
        r["distinct_ratio"] = round(len(set(emits)) / len(emits), 4)
        rows.append(r)
    if not rows:
        _d = {"emits": 0, "regime": "NO-EMIT",
              "note": "the substrate never emitted — echo/recombination is UNDEFINED, not 0."}
        _d.update(_repeat_dv(transcript))
        return _d
    scored = [r for r in rows if r["recomb_index"] is not None
              and r["borrow_content"] is not None]
    if not scored:
        _d = {"emits": len(rows), "regime": "TOO-SHORT",
              "note": "every emit was too short to score (no bigram / no content token)."}
        _d.update(_repeat_dv(transcript))
        return _d
    counts = {"COMPOSE": 0, "ECHO": 0, "DETACHED": 0, "INCONCLUSIVE": 0, "REPEAT": 0}
    for r in scored:
        counts[r["regime"]] += 1
    evidential = counts["COMPOSE"] + counts["ECHO"] + counts["DETACHED"]
    if not evidential:                 # every emit was a repeat / single-token collision
        _d = {"emits": len(rows), "scored": len(scored), "regime_counts": counts,
                "recomb_index": round(sum(r["recomb_index"] for r in scored) / len(scored), 4),
                "borrow_ratio": round(sum(r["borrow_ratio"] for r in scored) / len(scored), 4),
                "borrow_content": round(sum(r["borrow_content"] for r in scored) / len(scored), 4),
                "shared_terms": sorted({t for r in scored for t in r["shared_terms"]})[:20],
                "distinct_ratio": rows[-1]["distinct_ratio"], "regime": "NO-EVIDENCE",
              "note": ("no emit carries evidence either way — %d percept-invariant repeat(s), "
                       "%d single-shared-token collision(s)."
                       % (counts["REPEAT"], counts["INCONCLUSIVE"]))}
        _d.update(_repeat_dv(transcript))
        return _d
    # Headline = the MAJORITY class, never a mean-then-classify. Averaging the two axes and
    # labelling the average mixes regimes and manufactures the verdict: a DETACHED emit scores
    # recomb≈1.0 BY CONSTRUCTION (nothing shared, so nothing to echo), so a run of mostly
    # regurgitation drags mean-recomb up and reads COMPOSE. Measured live: 5 regurgitations +
    # 1 verbatim span copy — zero composition — averaged to borrow 0.111 / recomb 0.843 and
    # labelled COMPOSE-DIRECTIONAL. Classify per emit, then count.
    order = ["DETACHED", "ECHO", "COMPOSE"]          # ties resolve to the most conservative
    regime = min(order, key=lambda k: (-counts[k], order.index(k)))
    note = ("per-emit classes — COMPOSE %d · ECHO %d · DETACHED %d · INCONCLUSIVE %d · "
            "REPEAT %d (of %d scored; only the first three carry evidence). Means below are "
            "descriptive only: they mix regimes, so read the counts."
            % (counts["COMPOSE"], counts["ECHO"], counts["DETACHED"],
               counts["INCONCLUSIVE"], counts["REPEAT"], len(scored)))
    if counts["COMPOSE"] == 0:
        note += " NO emit qualified as composition."
    _d = {"emits": len(rows), "scored": len(scored), "regime_counts": counts,
          "recomb_index": round(sum(r["recomb_index"] for r in scored) / len(scored), 4),
          "borrow_ratio": round(sum(r["borrow_ratio"] for r in scored) / len(scored), 4),
          "borrow_content": round(sum(r["borrow_content"] for r in scored) / len(scored), 4),
          "shared_terms": sorted({t for r in scored for t in r["shared_terms"]})[:20],
          "distinct_ratio": rows[-1]["distinct_ratio"],
          "regime": regime, "note": note}
    _d.update(_repeat_dv(transcript))
    return _d


# --------------------------------------------------------------------------- #
# Coach note (--coach) — deterministic state note read from the transcript      #
# --------------------------------------------------------------------------- #
def _state_note(transcript):
    """A DESCRIPTIVE, deterministic note on what the substrate has been doing, so the
    teacher can stop repeating a subject that produced nothing.

    v2's teach_dialogue.py fed its teacher a coaching POLICY ("teach it one new word,
    ration vocabulary"). That is a teaching method, and anima refuses it: p2/p3/p6 forbid
    injecting identity or a curriculum policy, and H_1230 already measured the
    test→grade→adjust loop dead. So this reports STATE only ("it has been silent for N
    turns"), never a remedy — the teacher decides what to do with it. Deterministic, so
    it adds no teacher noise beyond what the emits themselves carry.
    """
    emitted = [r for r in transcript if r.get("did_emit") and r.get("emit_text")]
    if not emitted:
        n = sum(1 for r in transcript if r.get("percept"))
        return ("It has stayed silent through %d percept turn(s) so far." % n) if n else None
    silence = 0
    for r in reversed(transcript):
        if r.get("did_emit"):
            break
        silence += 1
    last3 = [r["emit_text"] for r in emitted[-3:]]
    bits = ["It has spoken %d time(s) in %d tick(s)."
            % (len(emitted), len(transcript))]
    if silence:
        bits.append("It has been silent for the last %d tick(s)." % silence)
    if len(last3) == 3 and len(set(last3)) == 1:
        bits.append("Its last three utterances were identical.")
    return " ".join(bits)


# --------------------------------------------------------------------------- #
# Teacher-output validation (--max-words) — reject a degenerate percept stream  #
# --------------------------------------------------------------------------- #
def _validate_teacher(text, max_words, prev):
    """Return None if acceptable, else a short reason string.

    Ported from v2's `valid_teacher`. Without it a degenerate teacher (empty, runaway, or
    stuck repeating one line) silently becomes the percept stream and the run reads as
    normal afterwards — the failure is invisible in the transcript. Rejections are counted
    and persisted so a run can be judged INVALID rather than quietly believed.
    """
    if not text or not text.strip():
        return "empty"
    if max_words and len(text.split()) > max_words:
        return "over --max-words (%d)" % max_words
    if prev and text.strip() == prev.strip():
        return "identical to previous turn"
    return None


def _build_teacher_prompt(topic, recent_emits, round_idx, total_rounds, state_note=None):
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
    if state_note:
        # Placed AFTER the "  - <emit>" block on purpose: _reactive_parse() ends that block at
        # the first non-"  - " line, so the deterministic backend keeps parsing identically.
        lines.append("Observed state: " + state_note)
    lines.append("")
    lines.append("Your one short utterance:")
    return "\n".join(lines)


def _run_study(ckpt, backend, rounds, window, topic, out_path,
               script_path=None, chat_flags=None, coach=False, max_words=0,
               report_path=None):
    """Drive one within-session teacher⇄daemon conversation (weights unchanged)."""
    try:
        ask = make_teacher(backend)
    except TeacherError as e:
        print("anima study: teacher SETUP-FAIL — %s" % e, file=sys.stderr)
        return 1
    n_ticks = max(1, rounds * window)
    state = {"last_spoke": -(10 ** 9), "round": 0, "transcript": None, "errors": 0,
             "prev": "", "rejects": []}

    def percept_source(tick, transcript):
        state["transcript"] = transcript          # stash the live list for post-run persist
        if tick - state["last_spoke"] < window:
            return None
        state["last_spoke"] = tick
        recent = [r["emit_text"] for r in transcript
                  if r.get("did_emit") and r.get("emit_text")][-3:]
        note = _state_note(transcript) if coach else None
        prompt = _build_teacher_prompt(topic, recent, state["round"], rounds, state_note=note)
        state["round"] += 1
        try:
            text = ask(prompt)
        except TeacherError as e:
            state["errors"] += 1
            print("  [teacher error → silence this turn] %s" % e, file=sys.stderr)
            return None
        # Validate the NORMALIZED utterance (the exact bytes that become the percept), so
        # "identical to previous" compares like with like. One retry with a terse reminder,
        # then silence — never hand-edit the teacher's text: a percept the harness rewrote
        # is no longer an exogenous percept.
        one = " ".join(text.split())[:400]
        bad = _validate_teacher(one, max_words, state["prev"])
        if bad:
            try:
                text = ask(prompt + "\n\n(Constraint: one short utterance, "
                                    "at most %d words, different from your last.)"
                           % (max_words or 40))
            except TeacherError as e:
                state["errors"] += 1
                print("  [teacher error on retry → silence this turn] %s" % e, file=sys.stderr)
                return None
            one = " ".join((text or "").split())[:400]
            bad = _validate_teacher(one, max_words, state["prev"])
        if bad:
            state["rejects"].append({"round": state["round"], "reason": bad})
            print("  [teacher REJECTED (%s) → silence this turn]" % bad, file=sys.stderr)
            return None
        state["prev"] = one
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
    summary = _growth_metrics(transcript)          # annotates rows in place, then summarizes
    with open(out_path, "w", encoding="utf-8", errors="surrogatepass") as fh:
        for r in transcript:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("anima study: DONE — %d teacher turns · %d substrate emit(s) · teacher-errors=%d"
          % (n_percept, n_emit, state["errors"]))
    if state["rejects"]:
        print("  teacher REJECTED %d turn(s): %s"
              % (len(state["rejects"]),
                 ", ".join("r%d=%s" % (x["round"], x["reason"]) for x in state["rejects"])))
    print("  growth telemetry (transcript-side · DIRECTIONAL · moves no frozen bar):")
    if summary.get("regime_counts"):
        c = summary["regime_counts"]
        print("    per-emit classes: COMPOSE %d · ECHO %d · DETACHED %d  |  no-evidence: "
              "INCONCLUSIVE %d · REPEAT %d  (of %d scored)"
              % (c["COMPOSE"], c["ECHO"], c["DETACHED"], c["INCONCLUSIVE"], c["REPEAT"],
                 summary["scored"]))
    if summary.get("scored"):
        print("    borrow_content %.3f  (teacher CONTENT words reaching the mouth — the pedestal)"
              % summary["borrow_content"])
        print("    borrow_ratio  %.3f   (all tokens incl. function words — has a content-free floor)"
              % summary["borrow_ratio"])
        print("    recomb_index  %.3f   (emitted bigrams unseen in any ONE teacher utterance)"
              % summary["recomb_index"])
        print("    distinct_ratio %.3f  (unique emits / emits)" % summary["distinct_ratio"])
        print("    shared terms: %s"
              % (", ".join(summary["shared_terms"]) if summary["shared_terms"] else "(none)"))
    # H_9984 ② · the pre-registered DV + its movement witness, printed on EVERY exit path (a
    # REPEAT-dominated run leaves through NO-EVIDENCE and that is the run this question is about).
    if summary.get("modal_emit_share") is not None or summary.get("seed_rows"):
        print("    ── H_9984 ② percept-write DV (arm=%s) ──" % (summary.get("pw_arm") or "off"))
        print("    modal_emit_share %s  (largest byte-identical emit / emits on percept-SILENT "
              "ticks = the manipulated stratum · %s of %s)"
              % (summary.get("modal_emit_share"), summary.get("modal_emit_count"),
                 summary.get("modal_emit_n")))
        print("      percept-seeded stratum (do() never applied): %s of %s emits  |  all ticks "
              "pooled (continuity with the 0.667 the card quotes): %s"
              % (summary.get("modal_emit_share_percept"), summary.get("modal_emit_n_percept"),
                 summary.get("modal_emit_share_all")))
        print("    seed movement    %s distinct / %s silent rows  (all rows %s/%s) — the WITNESS: "
              "no movement ⇒ the run is INVALID for the question, not a negative"
              % (summary.get("seed_distinct_silent"), summary.get("seed_rows_silent"),
                 summary.get("seed_distinct"), summary.get("seed_rows")))
    print("    regime: %s — %s" % (summary["regime"], summary["note"]))
    print("  transcript → %s (%d rows · consolidation-CPT input · NO weight change this MVP)"
          % (out_path, len(transcript)))
    if report_path:
        rep = {"ckpt": ckpt, "backend": ask.backend, "rounds": rounds, "window": window,
               "ticks": n_ticks, "topic": topic, "coach": bool(coach),
               "max_words": max_words, "teacher_turns": n_percept, "emits": n_emit,
               "teacher_errors": state["errors"], "teacher_rejects": state["rejects"],
               "transcript": out_path, "growth": summary}
        parent = os.path.dirname(os.path.abspath(report_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(report_path, "w", encoding="utf-8", errors="surrogatepass") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
        print("  report → %s" % report_path)
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
    coach = False                 # --coach: deterministic state note into the teacher prompt
    max_words = 0                 # --max-words: teacher-utterance length cap (0 = no cap)
    report_path = None            # --report: run summary JSON
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
        elif a == "--coach":
            coach = True; i += 1
        elif a == "--max-words":
            max_words = int(argv[i + 1]); i += 2
        elif a == "--report":
            report_path = argv[i + 1]; i += 2
        elif a == "--model":
            # Set the env the codex backend already reads, rather than threading a model arg
            # through make_teacher()'s uniform ask(prompt) contract (which every backend shares).
            os.environ["ANIMA_STUDY_CODEX_MODEL"] = argv[i + 1]; i += 2
        elif a == "--effort":
            os.environ["ANIMA_STUDY_CODEX_EFFORT"] = argv[i + 1]; i += 2
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
                      script_path=script_path, chat_flags=chat_flags,
                      coach=coach, max_words=max_words, report_path=report_path)
