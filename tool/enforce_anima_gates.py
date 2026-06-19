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
# (canonical 트리 재구성 후 엔진은 core/; 과거 대문자 CORE/ 도 archive 호환 위해 유지)
CORE_DECODE = re.compile(
    r"clm_decode|bytegpt_decode|engine_cli|faithful_phi|iit4_bigphi|/iit4/|\bcore/|\bCORE/|pure_field|engine_g"
)
DIRECTIONAL = re.compile(r"DIRECTIONAL", re.IGNORECASE)


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
        # DIRECTIONAL labeled (honest torch-side) → compliant
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
    tracked = sh(["git", "ls-files", "UNIVERSE/"]).splitlines()
    bad = [
        f.strip()
        for f in tracked
        if f.strip()
        and not f.startswith("UNIVERSE/cards/")
        and f.strip() != "UNIVERSE/HYPOTHESES.jsonl"
    ]
    return bad


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

    if not g1 and not g2:
        print(f"✅ anima-gates: clean · scope={scope_label} · {len(rows)} hypotheses")
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
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # enforcer must fail LOUD, never silently pass
        print(f"anima-gates: ENFORCER ERROR — {e}", file=sys.stderr)
        sys.exit(2)
