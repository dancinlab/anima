"""anima roadmap consolidation → JSON.

User: "과거 commit 에 로드맵 보면 holographic 말고 엄청 많이있었어 한번 가져와
볼래 / anima roadmap / json". The verification cycle touched ~30 hypotheses;
the ACTUAL anima roadmap = ~60 current `.roadmap.<domain>` JSONL SSOTs + ~10
history-only (deleted) ones. Each header line carries goal / required_conditions
(met·unmet) / blockers / cost_band / cross_link / status.

This recovers ALL of them (current tree + git-history-only) into one JSON
inventory. $0, read-only (git show for deleted).
"""
import json
import subprocess
from pathlib import Path

ROOT = Path("/Users/ghost/core/anima")
OUT = ROOT / "state/anima_roadmap_consolidated_2026_05_16.json"


def parse_header(text):
    """roadmap files: 2 comment lines then JSONL; first JSON obj = header."""
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        try:
            o = json.loads(ln)
        except Exception:
            continue
        if o.get("type") == "header":
            return o
        return o  # first json line even if not tagged header
    return None


def summarize(name, hdr, in_tree, src):
    if not hdr:
        return {"name": name, "in_tree": in_tree, "source": src,
                "parse": "no-header-json"}
    conds = hdr.get("required_conditions", []) or []
    met = sum(1 for c in conds if isinstance(c, dict) and c.get("status") == "met")
    unmet = sum(1 for c in conds if isinstance(c, dict) and c.get("status") == "unmet")
    blk = hdr.get("blockers", []) or []
    cl = hdr.get("cross_link", {}) or {}
    return {
        "name": hdr.get("name", name),
        "in_tree": in_tree,
        "source": src,
        "kind": hdr.get("kind"),
        "mk": hdr.get("mk"),
        "status": hdr.get("status"),
        "since": hdr.get("since"),
        "goal": (hdr.get("goal", "") or "")[:600],
        "n_conditions": len(conds),
        "conditions_met": met,
        "conditions_unmet": unmet,
        "blockers": [
            {"desc": (b.get("desc", "") or "")[:200], "type": b.get("type"),
             "status": b.get("status"), "eta": b.get("eta")}
            for b in blk if isinstance(b, dict)
        ],
        "cost_band": cl.get("cost_band") or hdr.get("cost_band"),
        "sister_domains": cl.get("sister_domains", []),
        "narrative_anchor": cl.get("narrative_anchor"),
    }


def main():
    # 1) current tree
    current = sorted(p.name for p in ROOT.iterdir()
                     if p.name.startswith(".roadmap") and p.is_file())
    # 2) every roadmap file ever in git history
    hist = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--all", "--pretty=format:", "--name-only"],
        capture_output=True, text=True).stdout
    ever = sorted({l for l in hist.splitlines()
                   if l.startswith(".roadmap") and "/" not in l})
    history_only = [f for f in ever if f not in current]

    roadmaps = []
    for fn in current:
        hdr = parse_header((ROOT / fn).read_text(errors="ignore"))
        roadmaps.append(summarize(fn, hdr, True, "current-tree"))

    recovered = []
    for fn in history_only:
        # newest-first commits touching fn; the latest is usually the DELETION
        # commit (blob gone there) — walk until a commit still has the blob.
        shas = subprocess.run(
            ["git", "-C", str(ROOT), "log", "--all", "--format=%H", "--", fn],
            capture_output=True, text=True).stdout.split()
        blob_text, used = None, None
        for sha in shas:
            b = subprocess.run(["git", "-C", str(ROOT), "show", f"{sha}:{fn}"],
                               capture_output=True, text=True)
            if b.returncode == 0 and b.stdout.strip():
                blob_text, used = b.stdout, sha
                break
            b2 = subprocess.run(["git", "-C", str(ROOT), "show", f"{sha}^:{fn}"],
                                capture_output=True, text=True)
            if b2.returncode == 0 and b2.stdout.strip():
                blob_text, used = b2.stdout, sha + "^"
                break
        if blob_text is None:
            recovered.append({"name": fn, "in_tree": False,
                              "source": "git-history", "parse": "blob-unrecoverable"})
            continue
        hdr = parse_header(blob_text)
        s = summarize(fn, hdr, False, f"git-history-only @ {used[:11]}")
        s["deleted_recovered_from"] = used[:11]
        recovered.append(s)

    active = [r for r in roadmaps if r.get("status") == "active"]
    by_cost = {}
    for r in roadmaps + recovered:
        cb = r.get("cost_band") or "unknown"
        by_cost[cb] = by_cost.get(cb, 0) + 1

    out = {
        "title": "anima roadmap — consolidated inventory (2026-05-16)",
        "note": ("Full .roadmap.<domain> JSONL SSOT inventory. The 2026-05-16 "
                 "verification cycle processed ~30 promoted hypotheses (H_007.. "
                 "incl. holographic H_010); THIS is the broader domain roadmap "
                 "(~%d current + %d history-only recovered) — neuromorphic / "
                 "quantum / wetware / clinical / biological-substrate tracks the "
                 "hypothesis cycle did not cover." % (len(roadmaps), len(recovered))),
        "counts": {
            "current_tree": len(roadmaps),
            "history_only_recovered": len(recovered),
            "total": len(roadmaps) + len(recovered),
            "active_current": len(active),
            "by_cost_band": by_cost,
        },
        "current_roadmaps": sorted(roadmaps, key=lambda r: r["name"]),
        "history_only_recovered": sorted(recovered, key=lambda r: r["name"]),
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"current={len(roadmaps)} history-only-recovered={len(recovered)} "
          f"total={len(roadmaps)+len(recovered)}")
    print("history-only:", [r["name"] for r in recovered])
    print("active sample:", [r["name"] for r in active[:12]])
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
