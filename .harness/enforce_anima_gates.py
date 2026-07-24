#!/usr/bin/env python3
"""anima self-harness — code-level enforcement of CLAUDE.md hard-gates.

This is mechanical enforcement (not salience): it parses the repo and EXITS NONZERO
on a violation so `harness ci` / pr-cycle / a git pre-commit hook BLOCKS it.

NO opt-out flag, NO skip marker, NO bypass branch (commons c18). The only knob is the
SCOPE of what is examined — never a way to let a violation through:

  (default)  changed scope  — hypotheses touched vs origin/main + staged/unstaged working tree.
                             You are accountable for what you change; a touched hypothesis MUST comply.
  --all                     — audit the WHOLE repo (stronger; debt burndown + CI visibility).

Gates enforced (mechanical subset of CLAUDE.md):

  G1  engine-native verdict gate  (a_engine_native_learning HARD-GATE)
      A hypothesis on a gate/ideation/G6/Φ/recombination/depth topic that carries a TERMINAL
      verdict tier (🟢 GREEN or 🧱 WALL) MUST be either
        (a) engine-native — has a `.hexa` artifact that calls a live CORE decoder
            (clm_decode / bytegpt_decode / engine_cli), OR
        (b) explicitly labeled DIRECTIONAL in its card / tier (honest torch-side label).
      A torch-side probe (state/<slug>/*.py importing torch / gauge_lib / numpy) carrying an
      UNLABELED terminal verdict is a VIOLATION.

  G2  hypothesis 2-surface  (a_hypothesis_register)
      git-tracked files under HYPOTHESES/ must be ONLY HYPOTHESES.jsonl + cards/** .

  G3  gate-card taxonomy invariant  (PROVENANCE ⊥ capability PASS closure)
      cli/evaluate.{py,hexa}'s `closure =` capability scorecard must never fold in the
      PROVENANCE result (r4/g4/prov) — that reopens the old G4 빵꾸.

  G5  VERSION lockstep  (anima-python PyPI publish · release-yml-2)
      A change touching anima-python wheel content (cli/**/*.py, core/**/*.py,
      pyproject.toml) must bump the root VERSION file in the same diff — otherwise
      release.yml/pypi-release.yml's same-VERSION skip-guard silently keeps PyPI stale.

  G7  no-scatter  (a_no_scatter_hypotheses_first)
      NO new tracked file may land under state/ (≠ verdicts/, ≠ CLAUDE.md) or archive/state/ —
      both are read-only fossils. Findings/numbers/parity → the HYPOTHESES card body + jsonl;
      verdicts → ARCHITECTURE gate nodes; volatile scratch → /tmp. Commit-time backstop to the
      H-NO-STATE-DIR pre_write hook (which only sees agent tool-calls, not script-internal writes).

  G8  new-surface ARCHITECTURE node  (single-doc · commons c4 · owner 2026-07-24)
      A NEW tracked production file under core/ or cli/ (*.py, *.hexa) must land together with
      an ARCHITECTURE.json edit that MENTIONS ITS PATH — the design SSOT gets the node when the
      surface is created, not whenever someone remembers. A verdict/gate node about the work is
      NOT a substitute: it records what was measured, while the tree records what now EXISTS.
      Precedent: core/clmg.py + cli/graft.py landed (#4501/#4502/#4504) with a gate node only,
      so the tree never learned the two new surfaces existed.

Exit: 0 = clean, 1 = violation(s), 2 = enforcer error.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HYP = REPO / "HYPOTHESES" / "HYPOTHESES.jsonl"
CARDS = REPO / "HYPOTHESES" / "cards"
CARD_ID = re.compile(r"^(H_\d+)_")

# G6 — unique-H_id invariant (a_hypothesis_register): one H id == one card == one jsonl row.
# Parallel sessions each compute "the next free H number" off their own origin/main snapshot,
# so the same id looks FREE to all of them and lands twice (convergence hypotheses-jsonl-3).
# Worse: a session then updates "its" row BY ID and silently overwrites ANOTHER session's
# verdict (2026-07-14: three sessions held H_9313; #3463 overwrote the real_dissociation row
# with a MITOSIS payload — the row survived looking healthy while a verdict evaporated).
# This gate makes a NEW collision a hard merge-block. The 35 pre-existing collisions are
# FROZEN as an explicit debt baseline below: they are listed, never silently tolerated, and the
# gate fails the moment the set GROWS. Shrinking it (renumbering a legacy pair) is always allowed.
LEGACY_DUP_IDS = frozenset({
    "H_182", "H_183", "H_184", "H_185", "H_186", "H_187", "H_188", "H_189", "H_190", "H_191",
    "H_679", "H_680", "H_6026", "H_6027", "H_6028", "H_6036", "H_6104", "H_6105", "H_6106",
    "H_6109", "H_6110", "H_6111", "H_9023", "H_9024", "H_9025", "H_9026", "H_9027", "H_9103",
    "H_9112", "H_9200", "H_9301", "H_9303", "H_9305", "H_9309", "H_9312",
})

# topics where the engine-native verdict gate bites (CLAUDE.md hard-gate #1)
GATE_TOPIC = re.compile(
    r"(ideation|\bG6\b|\bG5\b|falsifi|\bFALS\b|recombin|depth|\bΦ\b|\bphi\b|big-?phi|\bgate\b)",
    re.IGNORECASE,
)
TERMINAL = ("🟢", "🧱")  # GREEN / WALL = banked terminal verdict
TORCH_MARK = re.compile(r"import\s+torch|gauge_lib|\bnumpy\b")
# engine-native = a .hexa that calls a live core engine: the byte-mouth decoders
# (clm_decode/bytegpt_decode/engine_cli) OR the faithful-IIT4 Φ engine (a_phi_iit4_tool,
# stdlib/iit4/faithful_phi). Φ verdicts are engine-native via faithful_phi, not a byte decoder.
# The BUILT-IN G0-G6 eval (`anima evaluate`, PR #2604) is also engine-native: it is the
# canonical single-entry G-gate scorer (cli/evaluate.hexa holds the scorers + drives the
# generator L3 mouth gen_auto_ideate), so a verdict scored through it counts as engine-native
# evidence WITHOUT a per-gate python harness (a_engine_native_learning do:-carving — the
# canonical G-gate measurement command).
# (canonical 트리 재구성 후 엔진은 core/; 과거 대문자 CORE/ 도 archive 호환 위해 유지)
CORE_DECODE = re.compile(
    r"clm_decode|bytegpt_decode|engine_cli|faithful_phi|iit4_bigphi|/iit4/|\bcore/|\bCORE/|pure_field|engine_g|anima\s+eval(uate)?|cli/evaluate|gen_auto_ideate"
)
DIRECTIONAL = re.compile(r"DIRECTIONAL", re.IGNORECASE)

# 2-production (a_engine_native_learning): the py engine is a CO-EQUAL production engine
# and CAN bank a terminal G-gate verdict — but ONLY when its SCORING is byte-parity-verified
# against the WIRED hexa single-entry (cli/anima.hexa eval → cli/evaluate.hexa → generator L3).
# Decode-only byte-parity is NOT enough: a py side-harness that calls clm_decode_* directly and
# scores off a private re-implementation bypasses generator L3, so its G1/G6 numbers can DRIFT from the wired
# engine (precedent 2026-06-26 clm303_clean: side-harness G1/G6 FAIL @gen=40 was a gen-budget +
# unverified-scoring artifact). A parity-record = a state/<slug>/ evidence file proving the py
# G0-G6 SCORING == the wired hexa on a shared ckpt (e.g. golden d768, which hexa runs w/o OOM).
PARITY_RECORD = re.compile(
    r"(byte-?parity|scoring[- ]?parity|parity[- ]?gate).{0,400}(PASS|identical|byte-identical)"
    r"|wired.{0,200}(hexa|anima\s+eval).{0,200}(==|≡|identical|match)",
    re.IGNORECASE | re.DOTALL,
)
# side-harness signature: a .py that DIRECTLY invokes a decode/ideate fn (bypassing the wired
# cli/anima.hexa single entry) → py production-engine measurement, needs a parity-record.
SIDE_HARNESS = re.compile(
    r"clm_decode_(topk_sampled|argmax|grounded)(_W)?\s*\(|gen_clm_ideate|bytegpt_decode_\w+\s*\("
)


def has_parity_record(slug, arts, card=""):
    """True iff a parity-record (card body, listed artifact, or legacy state/<slug>/ fossil)
    records a SCORING byte-parity PASS vs the wired hexa engine — the 2-production gate that
    lets a py-engine verdict be terminal. New parity evidence lands in the CARD BODY
    (a_no_scatter_hypotheses_first); the legacy archive/state/<slug>/ fossil is still read for
    back-compat."""
    cands = [a for a in arts if a.startswith(("archive/state/", "state/"))]
    if card:
        cands.append(card if card.startswith("HYPOTHESES/") else "HYPOTHESES/" + card)
    sd = REPO / "archive" / "state" / slug
    if sd.is_dir():
        cands += [str(p.relative_to(REPO)) for p in sd.glob("*.txt")]
        cands += [str(p.relative_to(REPO)) for p in sd.glob("*.md")]
    for c in set(cands):
        if grep_file(c, PARITY_RECORD):
            return True
    return False


def sh(args):
    try:
        return subprocess.run(args, cwd=REPO, capture_output=True, text=True).stdout
    except Exception:
        return ""


def grep_file(path, pat):
    p = REPO / path
    if not p.is_file():
        return None  # unknown — file absent
    try:
        return bool(pat.search(p.read_text(errors="ignore")))
    except Exception:
        return None


def changed_slugs():
    """Slugs touched vs origin/main + working tree (staged + unstaged)."""
    files = set()
    base = sh(["git", "merge-base", "HEAD", "origin/main"]).strip()
    ranges = []
    if base:
        ranges.append(["git", "diff", "--name-only", base, "HEAD"])
    ranges.append(["git", "diff", "--name-only", "--cached"])
    ranges.append(["git", "diff", "--name-only"])
    for r in ranges:
        for ln in sh(r).splitlines():
            ln = ln.strip()
            if ln:
                files.add(ln)
    slugs = set()
    jsonl_touched = False
    for f in files:
        m = re.match(r"HYPOTHESES/cards/H_\d+_(.+)\.md$", f)
        if m:
            slugs.add(m.group(1))
        m = re.match(r"(?:archive/)?state/([^/]+)/", f)
        if m:
            slugs.add(m.group(1))
        if f == "HYPOTHESES/HYPOTHESES.jsonl":
            jsonl_touched = True
    if jsonl_touched:
        # include any slug whose jsonl line was added/changed on this branch
        diff = sh(["git", "diff"] + ([base] if base else []) + ["--", "HYPOTHESES/HYPOTHESES.jsonl"])
        for ln in diff.splitlines():
            if ln.startswith("+") and not ln.startswith("+++"):
                m = re.search(r'"slug"\s*:\s*"([^"]+)"', ln)
                if m:
                    slugs.add(m.group(1))
    return slugs


def load_hyps():
    rows = []
    for ln in HYP.read_text(errors="ignore").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            rows.append(json.loads(ln))
        except Exception:
            pass
    return rows


def g1_violations(rows, scope):
    out = []
    for d in rows:
        slug = d.get("slug", "")
        if scope is not None and slug not in scope:
            continue
        tier = str(d.get("tier", ""))
        title = str(d.get("title", ""))
        if not any(t in tier for t in TERMINAL):
            continue
        if not GATE_TOPIC.search(tier + " " + title + " " + slug):
            continue
        arts = d.get("artifacts", []) or []
        state_arts = [a for a in arts if a.startswith(("archive/state/", "state/"))]
        # engine-native? any .hexa artifact (or archive/state/<slug>/*.hexa) that calls a CORE decoder
        engine_native = False
        hexa_paths = [a for a in arts if a.endswith(".hexa")]
        sd = REPO / "archive" / "state" / slug
        if sd.is_dir():
            hexa_paths += [str(p.relative_to(REPO)) for p in sd.glob("*.hexa")]
        for h in hexa_paths:
            if grep_file(h, CORE_DECODE):
                engine_native = True
                break
        if engine_native:
            continue
        # torch-side? any .py artifact importing torch/gauge_lib/numpy
        torch_side = False
        py_paths = [a for a in state_arts if a.endswith(".py")]
        if sd.is_dir():
            py_paths += [str(p.relative_to(REPO)) for p in sd.glob("*.py")]
        for p in py_paths:
            g = grep_file(p, TORCH_MARK)
            if g or g is None and p.endswith(".py"):
                torch_side = True
                break
        if not torch_side:
            continue  # neither engine-native-CORE nor torch-side .py → out of mechanical scope
        # 2-PRODUCTION exception (a_engine_native_learning): a py-engine (numpy/torch) terminal
        # G-gate verdict IS allowed — but ONLY with a byte-parity record proving the py SCORING
        # == the WIRED hexa single-entry on a shared ckpt. This is what BLOCKS a side-harness
        # (a py side-harness calling clm_decode_* directly, bypassing cli/anima.hexa → generator L3)
        # from banking a terminal verdict it never verified.
        if has_parity_record(slug, arts, d.get("card", "")):
            continue
        # DIRECTIONAL labeled (honest unverified torch/py-side) → compliant
        labeled = bool(DIRECTIONAL.search(tier))
        card = d.get("card", "")
        if card and not labeled:
            cp = "HYPOTHESES/" + card if not card.startswith("HYPOTHESES/") else card
            if grep_file(cp, DIRECTIONAL):
                labeled = True
        if labeled:
            continue
        out.append((d.get("id", "?"), slug))
    return out


def g2_violations():
    # 2-surface = cards/** + HYPOTHESES.jsonl; HYPOTHESES/CLAUDE.md is the folder-guide
    # (commons folder-docs) — exempt (lockstep with .harness/enforcement.json H-UNIVERSE-CODE).
    # Still NO .py/.hexa/result under HYPOTHESES/.
    tracked = sh(["git", "ls-files", "HYPOTHESES/"]).splitlines()
    bad = [
        f.strip()
        for f in tracked
        if f.strip()
        and not f.startswith("HYPOTHESES/cards/")
        and f.strip() != "HYPOTHESES/HYPOTHESES.jsonl"
        and f.strip() != "HYPOTHESES/CLAUDE.md"
    ]
    return bad


def g6_violations(rows):
    """One H id == one card == one jsonl row. New collisions block; the legacy set may only shrink."""
    viols = []

    # (a) duplicate rows in the jsonl
    seen = {}
    for r in rows:
        hid = r.get("id")
        if hid:
            seen[hid] = seen.get(hid, 0) + 1
    for hid, n in sorted(seen.items()):
        if n > 1:
            viols.append((hid, f"jsonl 행 {n}개 (id 는 고유해야 한다)"))

    # (b) two cards claiming one id — the shape that let a verdict be overwritten
    by_id = {}
    if CARDS.is_dir():
        for f in sorted(os.listdir(CARDS)):
            m = CARD_ID.match(f)
            if m:
                by_id.setdefault(m.group(1), []).append(f)
    for hid, files in sorted(by_id.items()):
        if len(files) > 1 and hid not in LEGACY_DUP_IDS:
            viols.append((hid, "카드 " + " · ".join(files)))
    return viols


# G3 — gate-card taxonomy invariant: PROVENANCE ⊥ capability PASS closure.
# The 'G4 빵꾸' fix (검증방식 3-카드: CAPABILITY decode / SUBSTRATE read / PROVENANCE publish).
# The decode-CAPABILITY PASS closure (a7b_pass = G0∧G1∧G2) MUST NEVER fold in the PROVENANCE
# gate (G4 = sha256/HF/recovery = publish-process, N/A to decode) — that is the hole that made
# the flat G0-G6 scorecard punch out at G4. Mechanically: in the 2-production single-entry
# evaluate.{py,hexa} (the absorbed g_eval_all driver), every `closure =` assignment must NOT
# reference the provenance result (r4/g4/prov), and provenance must stay DOWNSTREAM (consume
# closure as publish-eligibility, not gate it). Current code already complies (closure = r0∧r1∧r2;
# g_eval_g4(ckpt, closure) reads it after) — this locks the redesign so the hole cannot reappear.
# NO bypass (c18).
GATECARD_FILES = ("cli/evaluate.py", "cli/evaluate.hexa")
CLOSURE_ASSIGN = re.compile(r"^\s*(?:let\s+)?closure\s*=")
PROV_IN_CLOSURE = re.compile(r"\b(r4|g4|prov)", re.IGNORECASE)


def g3_violations():
    viols = []
    for rel in GATECARD_FILES:
        p = REPO / rel
        if not p.is_file():
            continue  # tolerate absence (fresh repo); presence of one engine is enough
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        # closure assignments, excluding the g_eval_g4(ckpt, closure) call (which correctly
        # passes closure INTO provenance — the right direction, not a fold-in).
        assigns = [ln for ln in lines if CLOSURE_ASSIGN.match(ln) and "g_eval_g4" not in ln]
        if not assigns:
            viols.append((rel, "no `closure =` capability scorecard found — 3-card gate structure missing"))
            continue
        for ln in assigns:
            rhs = ln.split("=", 1)[1] if "=" in ln else ln
            if PROV_IN_CLOSURE.search(rhs):
                viols.append((rel, f"PROVENANCE folded into PASS closure (re-opens the G4 빵꾸): {ln.strip()}"))
    return viols


# G5 — VERSION lockstep gate (release-yml-2 근본수정, pip 채널): anima-python 휠에 실제로
# 담기는 파일(pyproject.toml [tool.setuptools] packages=anima_py.cli/anima_py.core 는 .py
# 모듈만 태움 — cli/**/*.hexa 는 무관)이 바뀌었는데 같은 변경범위(HEAD vs origin/main +
# staged/unstaged)에서 루트 VERSION 이 안 바뀌면 VIOLATION. 실측 재발조건: --xbind/--xfan
# eval fold(cli/evaluate.py, #3299/#3317)가 VERSION bump 없이 머지 → release.yml pypi-publish
# 의 same-VERSION skip-guard가 발행을 영구 스킵 → PyPI anima-python stale 0.13.3 고착 →
# 렌트 pod `pip install anima-python[train]` 후 `anima-py evaluate --help` 에 --xbind 결여
# → NBIND 측정 블록. `.github/workflows/pypi-release.yml` 의 PY-smoke 가 발행 시점(사후)
# 게이트라면, 이 G5 는 머지 시점(사전) 게이트 — 두 겹으로 재발을 막는다. NO bypass (c18).
# (숫자 G5 사용 이유: G4 는 이미 위 g3_violations() 텍스트가 가리키는 옛 ρ-AXON/G0-G6
# 래더의 PROVENANCE 게이트 명칭과 겹쳐 — 이 파일의 mechanical enforcement 번호와 무관한
# 도메인 개념이므로 혼동을 피해 G5 로 배정한다.)
WHEEL_PATH = re.compile(r"^(cli/.*\.py|core/.*\.py|pyproject\.toml)$")


def changed_files():
    """All files touched vs origin/main + working tree (staged + unstaged) — same diff
    ranges as changed_slugs(), just unfiltered (no HYPOTHESES/-slug extraction)."""
    files = set()
    base = sh(["git", "merge-base", "HEAD", "origin/main"]).strip()
    ranges = []
    if base:
        ranges.append(["git", "diff", "--name-only", base, "HEAD"])
    ranges.append(["git", "diff", "--name-only", "--cached"])
    ranges.append(["git", "diff", "--name-only"])
    for r in ranges:
        for ln in sh(r).splitlines():
            ln = ln.strip()
            if ln:
                files.add(ln)
    return files


def g5_violations(all_mode):
    if all_mode:
        return []  # per-change lockstep gate — a whole-repo audit has nothing to diff against
    files = changed_files()
    wheel_touched = sorted(f for f in files if WHEEL_PATH.match(f))
    if not wheel_touched or "VERSION" in files:
        return []
    return wheel_touched


# G7 — no-scatter commit-time backstop (a_no_scatter_hypotheses_first). The pre_write hook
# (H-NO-STATE-DIR) only sees agent tool-calls; a script/command that writes files internally
# slips past it. This gate is the commit-time net: NO NEW tracked file may land under state/
# (≠ verdicts/, ≠ CLAUDE.md) or archive/state/. Findings/numbers/parity → the HYPOTHESES card
# body + jsonl; verdicts → ARCHITECTURE gate nodes; volatile scratch → /tmp. NO bypass (c18).
G7_PATH = re.compile(r"^(archive/)?state/(?!verdicts/|CLAUDE\.md)")


def g7_violations(all_mode):
    if all_mode:
        return []  # per-change gate — a whole-repo audit has no baseline to diff against
    base = sh(["git", "merge-base", "HEAD", "origin/main"]).strip()
    new = set(sh(["git", "diff", "--name-only", "--diff-filter=A", "--cached"]).splitlines())
    if base:
        new |= set(sh(["git", "diff", "--name-only", "--diff-filter=A", base, "HEAD"]).splitlines())
    return sorted(f.strip() for f in new if f.strip() and G7_PATH.match(f.strip()))


# G8 — new production surface must arrive WITH its ARCHITECTURE.json node (single-doc, commons c4).
# The tree is the "what exists" SSOT; gate/convergence nodes are the "what was measured" record.
# Landing a new core//cli/ module while touching only a gate node leaves the tree blind to it.
G8_PATH = re.compile(r"^(core|cli)/[^/]*\.(py|hexa)$")


def g8_violations(all_mode):
    if all_mode:
        return []  # per-change gate — a whole-repo audit has no baseline to diff against
    base = sh(["git", "merge-base", "HEAD", "origin/main"]).strip()
    new = set(sh(["git", "diff", "--name-only", "--diff-filter=A", "--cached"]).splitlines())
    if base:
        new |= set(sh(["git", "diff", "--name-only", "--diff-filter=A", base, "HEAD"]).splitlines())
    added = sorted(f.strip() for f in new if f.strip() and G8_PATH.match(f.strip()))
    if not added:
        return []
    arch = REPO / "ARCHITECTURE.json"
    text = arch.read_text(encoding="utf-8", errors="replace") if arch.is_file() else ""
    # the node must NAME the path — an unrelated ARCHITECTURE edit in the same diff is not a node
    return [f for f in added if f not in text]


def main():
    all_mode = "--all" in sys.argv[1:]
    if not HYP.is_file():
        print("anima-gates: HYPOTHESES.jsonl not found — skipping (fresh repo)")
        return 0
    rows = load_hyps()
    scope = None if all_mode else changed_slugs()
    scope_label = "ALL" if all_mode else f"changed ({len(scope)} slug)" if scope else "changed (none)"

    g1 = g1_violations(rows, scope)
    g2 = g2_violations()  # always whole-repo; cheap structural invariant
    g3 = g3_violations()  # always whole-repo; gate-card taxonomy invariant (PROVENANCE ⊥ closure)
    g5 = g5_violations(all_mode)  # changed-scope only; VERSION lockstep vs anima-python wheel content
    g6 = g6_violations(rows)  # always whole-repo; unique-H_id invariant (a_hypothesis_register)
    g7 = g7_violations(all_mode)  # changed-scope only; no-scatter (state/ + archive/state/ new-write block)
    g8 = g8_violations(all_mode)  # changed-scope only; new core//cli/ surface must carry its ARCHITECTURE node

    if not g1 and not g2 and not g3 and not g5 and not g6 and not g7 and not g8:
        print(f"✅ anima-gates: clean · scope={scope_label} · {len(rows)} hypotheses · gate-card invariant OK")
        return 0

    print("❌ anima-gates: VIOLATION (CLAUDE.md 하드-게이트 code-level block)")
    print(f"   scope={scope_label}")
    if g1:
        print()
        print("  [G1] engine-native verdict gate (a_engine_native_learning) — "
              "terminal 🟢/🧱 on gate/ideation/G6/Φ topic but torch-side & not DIRECTIONAL-labeled:")
        for hid, slug in g1:
            print(f"        · {hid} ({slug})")
        print("     → 엔진-네이티브(.hexa via CORE clm_decode) 재측정으로 박제하거나, "
              "torch-side면 카드/tier 에 DIRECTIONAL 명기. (no bypass — c18)")
    if g2:
        print()
        print("  [G2] hypothesis 2-surface (a_hypothesis_register) — "
              "HYPOTHESES/ 에 cards/·HYPOTHESES.jsonl 외 파일:")
        for f in g2:
            print(f"        · {f}")
        print("     → 내용을 카드 본문으로 흡수하고 파일은 삭제한다 — archive/state/ 는 읽기전용 박제, "
              "신규 산출물 표면은 카드+jsonl · ARCHITECTURE · state/verdicts/ 뿐 (a_no_scatter_hypotheses_first).")
    if g3:
        print()
        print("  [G3] gate-card taxonomy (PROVENANCE ⊥ capability closure) — "
              "G4(provenance/publish)가 디코드-능력 PASS closure 에 끼어듦 (= G4 빵꾸 재발):")
        for rel, msg in g3:
            print(f"        · {rel}: {msg}")
        print("     → closure 는 디코드-CAPABILITY(G0∧G1∧G2)만; PROVENANCE(G4)는 downstream "
              "publish-eligibility 로만 (g_eval_g4(ckpt, closure)). 3-카드 분리 유지. (no bypass — c18)")
    if g5:
        print()
        print("  [G5] VERSION lockstep (anima-python PyPI 발행 · release-yml-2) — "
              "cli/·core/·pyproject.toml(wheel 콘텐츠) 변경인데 VERSION 미bump:")
        for f in g5:
            print(f"        · {f}")
        print("     → 루트 VERSION(+VERSIONS.md §0·hexa.toml, a1) patch bump 를 같은 변경분에 포함. "
              "PyPI same-VERSION skip-guard가 이 wheel 변경을 영구 스킵하지 않도록. (no bypass — c18)")
    if g6:
        print()
        print("  [G6] unique-H_id (a_hypothesis_register) — "
              "한 H id 는 카드 1개 · jsonl 행 1개여야 한다 (병렬 세션 id 경합):")
        for hid, msg in g6:
            print(f"        · {hid}: {msg}")
        print("     → 발사 시점의 FREE ≠ 머지 시점의 FREE. pr-cycle 직전 origin/main 을 재-fetch 해 "
              "내 id 가 아직 미점유인지 확인하고, 충돌하면 **나중 머지된 쪽**을 재번호하라 "
              "(카드 파일명 + jsonl + ARCHITECTURE gate 노드 lockstep · 내용/수치 verbatim 보존).")
        print("     ⚠️ id 로 행을 찾아 갱신하기 전에 그 행의 title/card 가 정말 내 가설인지 대조하라 — "
              "id 일치만 믿고 덮어쓰면 남의 verdict 가 소리 없이 증발한다 "
              "(2026-07-14 #3463 실측 · convergence hypotheses-jsonl-3). (no bypass — c18)")
    if g7:
        print()
        print("  [G7] no-scatter (a_no_scatter_hypotheses_first) — "
              "state/ (≠verdicts/) · archive/state/ 아래 신규 tracked 파일 (읽기전용 박제에 산출물 흩뿌림):")
        for f in g7:
            print(f"        · {f}")
        print("     → 내용은 카드 본문 + jsonl(수치·parity) · ARCHITECTURE gate 노드(verdict) 로 흡수하고 "
              "파일은 삭제한다. 휘발 중간물은 /tmp. frozen 계약만 state/verdicts/. (no bypass — c18)")
    if g8:
        print()
        print("  [G8] new-surface ARCHITECTURE node (single-doc · commons c4) — "
              "core//cli/ 신규 production 파일인데 ARCHITECTURE.json 이 그 경로를 담지 않음:")
        for f in g8:
            print(f"        · {f}")
        print("     → 설계 SSOT 트리에 그 파일의 노드를 같은 변경분에 만들어라 "
              "({name, role, id, detail} · 형제 노드 규약을 따를 것). "
              "게이트/verdict 노드는 대체물이 아니다 — 그건 '무엇을 측정했나'이고, "
              "트리는 '지금 무엇이 존재하나'다. 만든 시점에 만들고 이후 갱신한다(오너 2026-07-24). "
              "(no bypass — c18)")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # enforcer must fail LOUD, never silently pass
        print(f"anima-gates: ENFORCER ERROR — {e}", file=sys.stderr)
        sys.exit(2)
