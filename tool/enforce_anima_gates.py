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
      git-tracked files under UNIVERSE/ must be ONLY HYPOTHESES.jsonl + cards/** .

Exit: 0 = clean, 1 = violation(s), 2 = enforcer error.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HYP = REPO / "UNIVERSE" / "HYPOTHESES.jsonl"

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
# The BUILT-IN G0-G6 eval (g_gates / `anima eval`, PR #2604) is also engine-native: it is the
# canonical single-entry G-gate scorer (cli/anima.hexa → generator L3 mouth gen_auto_ideate),
# so a verdict scored through it counts as engine-native evidence WITHOUT a per-gate python
# harness (a_engine_native_learning do:-carving — the canonical G-gate measurement command).
# (canonical 트리 재구성 후 엔진은 core/; 과거 대문자 CORE/ 도 archive 호환 위해 유지)
CORE_DECODE = re.compile(
    r"clm_decode|bytegpt_decode|engine_cli|faithful_phi|iit4_bigphi|/iit4/|\bcore/|\bCORE/|pure_field|engine_g|g_gates|anima\s+eval|gen_auto_ideate"
)
DIRECTIONAL = re.compile(r"DIRECTIONAL", re.IGNORECASE)

# 2-production (a_engine_native_learning): the py engine is a CO-EQUAL production engine
# and CAN bank a terminal G-gate verdict — but ONLY when its SCORING is byte-parity-verified
# against the WIRED hexa single-entry (cli/anima.hexa eval → core/g_gates.hexa → generator L3).
# Decode-only byte-parity is NOT enough: a py side-harness that calls clm_decode_* directly and
# scores with g_gates.py bypasses generator L3, so its G1/G6 numbers can DRIFT from the wired
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


def has_parity_record(slug, arts):
    """True iff a state/<slug>/ evidence file (or listed artifact) records a SCORING byte-parity
    PASS vs the wired hexa engine — the 2-production gate that lets a py-engine verdict be terminal."""
    cands = [a for a in arts if a.startswith("state/")]
    sd = REPO / "state" / slug
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
        m = re.match(r"UNIVERSE/cards/H_\d+_(.+)\.md$", f)
        if m:
            slugs.add(m.group(1))
        m = re.match(r"state/([^/]+)/", f)
        if m:
            slugs.add(m.group(1))
        if f == "UNIVERSE/HYPOTHESES.jsonl":
            jsonl_touched = True
    if jsonl_touched:
        # include any slug whose jsonl line was added/changed on this branch
        diff = sh(["git", "diff"] + ([base] if base else []) + ["--", "UNIVERSE/HYPOTHESES.jsonl"])
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
        state_arts = [a for a in arts if a.startswith("state/")]
        # engine-native? any .hexa artifact (or state/<slug>/*.hexa) that calls a CORE decoder
        engine_native = False
        hexa_paths = [a for a in arts if a.endswith(".hexa")]
        sd = REPO / "state" / slug
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
        # (py g_gates.py calling clm_decode_* directly, bypassing cli/anima.hexa → generator L3)
        # from banking a terminal verdict it never verified.
        if has_parity_record(slug, arts):
            continue
        # DIRECTIONAL labeled (honest unverified torch/py-side) → compliant
        labeled = bool(DIRECTIONAL.search(tier))
        card = d.get("card", "")
        if card and not labeled:
            cp = "UNIVERSE/" + card if not card.startswith("UNIVERSE/") else card
            if grep_file(cp, DIRECTIONAL):
                labeled = True
        if labeled:
            continue
        out.append((d.get("id", "?"), slug))
    return out


def g2_violations():
    # 2-surface = cards/** + HYPOTHESES.jsonl; UNIVERSE/CLAUDE.md is the folder-guide
    # (commons folder-docs) — exempt (lockstep with .harness/enforcement.json H-UNIVERSE-CODE).
    # Still NO .py/.hexa/result under UNIVERSE/.
    tracked = sh(["git", "ls-files", "UNIVERSE/"]).splitlines()
    bad = [
        f.strip()
        for f in tracked
        if f.strip()
        and not f.startswith("UNIVERSE/cards/")
        and f.strip() != "UNIVERSE/HYPOTHESES.jsonl"
        and f.strip() != "UNIVERSE/CLAUDE.md"
    ]
    return bad


# G3 — gate-card taxonomy invariant: PROVENANCE ⊥ capability PASS closure.
# The 'G4 빵꾸' fix (검증방식 3-카드: CAPABILITY decode / SUBSTRATE read / PROVENANCE publish).
# The decode-CAPABILITY PASS closure (a7b_pass = G0∧G1∧G2) MUST NEVER fold in the PROVENANCE
# gate (G4 = sha256/HF/recovery = publish-process, N/A to decode) — that is the hole that made
# the flat G0-G6 scorecard punch out at G4. Mechanically: in the 2-production g_gates.{py,hexa},
# every `closure =` assignment must NOT reference the provenance result (r4/g4/prov), and
# provenance must stay DOWNSTREAM (consume closure as publish-eligibility, not gate it).
# Current code already complies (closure = r0∧r1∧r2; g_eval_g4(ckpt, closure) reads it after) —
# this locks the redesign so the hole cannot reappear. NO bypass (c18).
GATECARD_FILES = ("core/g_gates.py", "core/g_gates.hexa")
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

    if not g1 and not g2 and not g3:
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
              "UNIVERSE/ 에 cards/·HYPOTHESES.jsonl 외 파일:")
        for f in g2:
            print(f"        · {f}")
        print("     → 코드/결과물은 state/<slug>/ 로 옮기고 jsonl artifacts 로 가리킨다.")
    if g3:
        print()
        print("  [G3] gate-card taxonomy (PROVENANCE ⊥ capability closure) — "
              "G4(provenance/publish)가 디코드-능력 PASS closure 에 끼어듦 (= G4 빵꾸 재발):")
        for rel, msg in g3:
            print(f"        · {rel}: {msg}")
        print("     → closure 는 디코드-CAPABILITY(G0∧G1∧G2)만; PROVENANCE(G4)는 downstream "
              "publish-eligibility 로만 (g_eval_g4(ckpt, closure)). 3-카드 분리 유지. (no bypass — c18)")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # enforcer must fail LOUD, never silently pass
        print(f"anima-gates: ENFORCER ERROR — {e}", file=sys.stderr)
        sys.exit(2)
