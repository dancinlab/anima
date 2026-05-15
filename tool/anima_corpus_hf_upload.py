#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  tool/anima_corpus_hf_upload.py
#
#  PURPOSE
# mandate-1/2/3 destination 의무 응용 (FIRST CYCLE) —
#    L4 corpus 3 files (Tier A persona / Tier B dialogue / BG-LD pref pairs)
#    → HF dancinlab dataset repos upload (private + Card metadata).
#
#    이 cycle 직전 (loop iter 1 commit 0116a35d) 에서 102MB persona corpus 가
# git 에 push 됐다가 GitHub 100MB 한도로 reject 된 incident 가 의
#    직접 trigger. iter 2 commit 88787533 에서 retroactive cleanup (3 파일
# git untrack + .gitignore 강화) 완료. 본 script 는 mandate-1/2/3
#    destination 의무 (HF dancinlab dataset upload) 첫 응용.
#
#  COMPLIANCE
# mandate-2 (corpus ≥10MB → HF dataset upload 의무)
# mandate-3 (preference pairs ≥10MB → HF dataset upload 의무)
# mandate-8 (HF dancinlab + Flavor B + private + Card metadata)
# mandate-1 (org = dancinlab)
# mandate-4 Flavor B (BG iteration naming convention)
# mandate-8 (visibility default = private)
# mandate-9 (HF Card metadata mandatory tags)
# (anima-native curated — 외부 LLM dump / wiki 없음)
#    raw#9 / raw#37 (HF upload script .py allowed; chat path 외)
#    raw#10 honest C3 (--dry-run default, --apply requires explicit consent)
#
#  USAGE
#    python3 tool/anima_corpus_hf_upload.py --dry-run    (default)
#    python3 tool/anima_corpus_hf_upload.py --apply      (real upload)
#    python3 tool/anima_corpus_hf_upload.py --verify     (verify post-upload)
#
# FILES (mandate-2/3 scope, 본 cycle):
#    1. state/anima_persona_tier_a_2026_05_08.txt          103.59MB  →
#       dancinlab/anima-persona-tier-a-corpus-2026-05-08
#    2. state/anima_dialogue_tier_a_iter2_2026_05_08.txt   72.78MB   →
#       dancinlab/anima-dialogue-tier-a-corpus-2026-05-08
#    3. state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl 17.66MB →
#       dancinlab/anima-clm-l4-ld-preference-pairs-2026-05-08
#
#  DRY-RUN BEHAVIOR
#    Plans every action but DOES NOT call HfApi mutators (no create_repo, no
#    upload_file). Emits planned repo_id / Card metadata / file size. Exit 0.
#    Real upload requires explicit --apply flag (사용자 directive
#    'OK CORPUS HF UPLOAD' 또는 explicit consent 필요).
# ════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
HF_ORG = "dancinlab" # mandate-1
HF_TOKEN_FILE = Path(os.path.expanduser("~/.cache/huggingface/token"))
LOG_PATH = ANIMA_ROOT / "state" / "anima_corpus_hf_upload_log.jsonl"
CYCLE_DATE = "2026-05-08"

# ─── 3 corpus files (mandate-2/3 scope) ────────────────────────────
CORPUS_PLAN = [
    {
        "file": ANIMA_ROOT / "state" / "anima_persona_tier_a_2026_05_08.txt",
        "repo_id": f"{HF_ORG}/anima-persona-tier-a-corpus-{CYCLE_DATE}",
        "kind": "persona_corpus",
        "card_meta": {
            "corpus_path": "state/anima_persona_tier_a_2026_05_08.txt",
            "cycle": CYCLE_DATE,
            "paradigm": "anima-native-persona-curation",
            "size_mb": 103.59,
            "curation_source": "anima cycle docs (.raw-audit excerpt + cycle docs Tier A) — 11/12 sources accepted, density ≥0.4% threshold; iter-2 multi-keyword sem-density ≥2/6 axes",
            "density": 0.015911,
            "tier": "Tier A (anima identity-bearing persona)",
            "files_scanned": 353,
            "paragraphs_accepted": 976,
            "paragraphs_rejected": 6001,
            "iter": "iter-2 final (combined iter-1 + iter-2 semantic deepen)",
            "compliance_own": [17, 18, 19, 20, 31, 36],
        },
    },
    {
        "file": ANIMA_ROOT / "state" / "anima_dialogue_tier_a_iter2_2026_05_08.txt",
        "repo_id": f"{HF_ORG}/anima-dialogue-tier-a-corpus-{CYCLE_DATE}",
        "kind": "dialogue_corpus",
        "card_meta": {
            "corpus_path": "state/anima_dialogue_tier_a_iter2_2026_05_08.txt",
            "cycle": CYCLE_DATE,
            "paradigm": "anima-native-dialogue-chat-template",
            "size_mb": 72.78,
            "curation_source": "BG-JE persona chat-template ext (21MB) + anima_combined_paradigm_corpus chat-template (~55MB) + V4 BG-KM-LLAMA-3B v4_pass=true (23/55) + anima_core_dialogues + strategic_tribev2_dialogue",
            "density": 0.009705,
            "tier": "Tier B (chat-template dialogue)",
            "chat_template_ratio": 0.2895,
            "n_user_turns": 136073,
            "n_assistant_turns": 136140,
            "format": "사용자: <Q>\\n도우미: <A>\\n\\n (chat-template marginal 28.95%)",
            "iter": "iter-2 (12.96MB → 72.78MB ext)",
            "compliance_own": [17, 18, 19, 20, 31, 36],
        },
    },
    {
        "file": ANIMA_ROOT / "state" / "anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl",
        "repo_id": f"{HF_ORG}/anima-clm-l4-ld-preference-pairs-{CYCLE_DATE}",
        "kind": "preference_pairs",
        "card_meta": {
            "corpus_path": "state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl",
            "cycle": CYCLE_DATE,
            "paradigm": "dpo-rlhf-preference-pairs",
            "size_mb": 17.66,
            "curation_source": "BG-KM-LLAMA-3B v4_pass=true chosen pool (23) + V4 fail rejected pool (5000) + synth rejected (46: template_leak '서연:' + degenerate '이' repeat noise)",
            "density": "n/a (pairs format)",
            "tier": "BG-LD preference pairs (DPO L4 stage)",
            "pairs_count": 30023,
            "ratio": "1:1 chosen/rejected",
            "format": "JSONL: {prompt, chosen, rejected, domain, source_chosen, source_rejected}",
            "iter": "iter-1 sample (target 100MB, gap 82.34MB)",
            "compliance_own": [17, 18, 22, 24, 31, 36],
        },
    },
]


def hf_token() -> str:
    if not HF_TOKEN_FILE.exists():
        sys.exit(f"HF token missing at {HF_TOKEN_FILE}")
    return HF_TOKEN_FILE.read_text().strip()


def build_card_md(plan: dict) -> str:
    """Generate README.md (HF Dataset Card) per mandate-9."""
    meta = plan["card_meta"]
    repo_id = plan["repo_id"]
    name = repo_id.split("/")[-1]
    kind = plan["kind"]
    yaml_tags = [
        "  - anima",
        "  - korean",
        f"  - {kind.replace('_', '-')}",
        "  - anima-native",
        f"  - cycle-{CYCLE_DATE}",
    ]
    if "persona" in kind:
        yaml_tags.extend(["  - persona", "  - identity-bearing"])
    if "dialogue" in kind:
        yaml_tags.extend(["  - dialogue", "  - chat-template"])
    if "preference" in kind:
        yaml_tags.extend(["  - preference-pairs", "  - dpo", "  - rlhf"])

    body_lines = [
        f"# {name}",
        "",
        f"anima L4 corpus 큐레이션 산출물 — **{kind.replace('_',' ')}** ({meta['size_mb']}MB).",
        "",
        "## Origin",
        f"- Cycle: {meta['cycle']}",
        f"- Paradigm: `{meta['paradigm']}`",
        f"- Tier: {meta.get('tier','?')}",
        f"- Iter: {meta.get('iter','?')}",
        f"- Curation source: {meta['curation_source']}",
        f"- Density: {meta.get('density','n/a')}",
    ]
    if "chat_template_ratio" in meta:
        body_lines.append(f"- Chat-template ratio: {meta['chat_template_ratio']*100:.2f}% (≥30% target marginal)")
    if "n_user_turns" in meta:
        body_lines.append(f"- User turns: {meta['n_user_turns']:,} / Assistant turns: {meta['n_assistant_turns']:,}")
    if "files_scanned" in meta:
        body_lines.append(f"- Files scanned: {meta['files_scanned']}")
        body_lines.append(f"- Paragraphs accepted: {meta['paragraphs_accepted']} / rejected: {meta['paragraphs_rejected']}")
    if "pairs_count" in meta:
        body_lines.append(f"- Pairs: {meta['pairs_count']:,} ({meta.get('ratio','?')})")
    if "format" in meta:
        body_lines.append(f"- Format: `{meta['format']}`")

    body_lines.extend([
        "",
        "## own SSOT compliance",
    ])
    for o in meta["compliance_own"]:
        body_lines.append(f"- own {o}")
    body_lines.extend([
        "",
        "## Provenance",
        f"- Original path: `{meta['corpus_path']}`",
        f"- Anima repo: https://github.com/dancinlife/anima (private)",
        f"- Roadmap: `.roadmap.cli` cli.clm_l4_corpus_iter1_2026_05_08 / iter2",
        "",
        "## License",
        "anima-research (private dancinlab org). 사용자 manual approval required for any external sharing.",
    ])

    yaml_header = "---\n"
    yaml_header += "license: other\n"
    yaml_header += "language:\n  - ko\n  - en\n"
    yaml_header += "tags:\n" + "\n".join(yaml_tags) + "\n"
    yaml_header += "size_categories:\n  - 10M<n<100M\n" if meta["size_mb"] >= 10 else "size_categories:\n  - n<1K\n"
    yaml_header += f"pretty_name: {name}\n"
    yaml_header += "---\n\n"
    return yaml_header + "\n".join(body_lines) + "\n"


def append_log(entry: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def plan_emit(plan: dict, mode: str):
    f = plan["file"]
    if not f.exists():
        return {"status": "ERROR_FILE_MISSING", "file": str(f), "repo_id": plan["repo_id"]}
    size_b = f.stat().st_size
    size_mb = size_b / 1024 / 1024
    card_md = build_card_md(plan)
    return {
        "status": "PLANNED" if mode == "dry-run" else "PENDING",
        "file": str(f),
        "size_mb": round(size_mb, 2),
        "size_bytes": size_b,
        "repo_id": plan["repo_id"],
        "kind": plan["kind"],
        "card_meta": plan["card_meta"],
        "card_md_bytes": len(card_md),
        "card_md_preview": card_md[:300],
    }


def upload_one(plan: dict, token: str) -> dict:
    """Real upload: create_repo (private) + upload_file (corpus) + upload card."""
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    repo_id = plan["repo_id"]
    f = plan["file"]
    t0 = time.time()
    try:
        # mandate-8: private default
        api.create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            private=True,
            exist_ok=True,
        )
        # upload corpus file (preserve original filename in repo root)
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=f.name,
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=f" mandate-2/3 destination 의무 — {plan['kind']} corpus upload (cycle {CYCLE_DATE})",
        )
        # upload Dataset Card README.md (mandate-9)
        card_md = build_card_md(plan)
        api.upload_file(
            path_or_fileobj=card_md.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=" mandate-9 — HF Dataset Card metadata emit",
        )
        elapsed = time.time() - t0
        return {
            "status": "UPLOADED",
            "repo_id": repo_id,
            "url": f"https://huggingface.co/datasets/{repo_id}",
            "private": True,
            "elapsed_sec": round(elapsed, 2),
        }
    except Exception as e:
        return {
            "status": "ERROR_UPLOAD",
            "repo_id": repo_id,
            "error": f"{type(e).__name__}: {e}",
            "elapsed_sec": round(time.time() - t0, 2),
        }


def verify_one(plan: dict, token: str) -> dict:
    """Post-upload verify: repo exists + size match."""
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    repo_id = plan["repo_id"]
    f = plan["file"]
    expected_size = f.stat().st_size
    try:
        info = api.dataset_info(repo_id=repo_id, token=token)
        siblings = {s.rfilename: s.size for s in info.siblings if s.size}
        actual_size = siblings.get(f.name)
        size_match = actual_size == expected_size if actual_size else None
        return {
            "status": "VERIFIED" if size_match else "SIZE_MISMATCH",
            "repo_id": repo_id,
            "private": info.private,
            "expected_size": expected_size,
            "actual_size": actual_size,
            "files_in_repo": list(siblings.keys()),
        }
    except Exception as e:
        return {
            "status": "ERROR_VERIFY",
            "repo_id": repo_id,
            "error": f"{type(e).__name__}: {e}",
        }


def main():
    ap = argparse.ArgumentParser(description=" 응용 — anima corpus HF dancinlab dataset upload")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", default=True, help="Plan only (default)")
    g.add_argument("--apply", action="store_true", help="Real upload (사용자 explicit consent 필요)")
    g.add_argument("--verify", action="store_true", help="Post-upload verify (repo exists + size match)")
    args = ap.parse_args()

    mode = "verify" if args.verify else ("apply" if args.apply else "dry-run")
    print(f"[anima_corpus_hf_upload] mode={mode} cycle={CYCLE_DATE}")
    print(f"[anima_corpus_hf_upload] org={HF_ORG} (mandate-1)")
    print(f"[anima_corpus_hf_upload] files={len(CORPUS_PLAN)} (mandate-2/3 scope)")
    print()

    token = None
    if mode in ("apply", "verify"):
        token = hf_token()

    overall = {
        "ts_start": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": mode,
        "org": HF_ORG,
        "cycle": CYCLE_DATE,
        "plans": [],
    }

    rc_overall = 0
    for plan in CORPUS_PLAN:
        print(f"--- {plan['repo_id']} ---")
        if mode == "dry-run":
            res = plan_emit(plan, mode="dry-run")
            print(f"  status: {res['status']}")
            print(f"  file: {res.get('file')}")
            print(f"  size: {res.get('size_mb')}MB ({res.get('size_bytes')} B)")
            print(f"  kind: {res.get('kind')}")
            print(f"  card_md: {res.get('card_md_bytes')} bytes")
            print(f"  card preview: {res.get('card_md_preview','')[:200]}...")
        elif mode == "apply":
            res = upload_one(plan, token)
            print(f"  status: {res['status']}")
            if "url" in res:
                print(f"  url: {res['url']} (private)")
            if "error" in res:
                print(f"  error: {res['error']}")
                rc_overall = 1
            print(f"  elapsed: {res.get('elapsed_sec','?')}s")
        elif mode == "verify":
            res = verify_one(plan, token)
            print(f"  status: {res['status']}")
            if "private" in res:
                print(f"  private: {res['private']}")
                print(f"  expected: {res.get('expected_size')} / actual: {res.get('actual_size')}")
            if "error" in res:
                print(f"  error: {res['error']}")
                rc_overall = 1
        overall["plans"].append({
            "repo_id": plan["repo_id"],
            "result": res,
        })
        print()

    overall["ts_end"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    overall["rc"] = rc_overall
    append_log(overall)
    print(f"[anima_corpus_hf_upload] log appended: {LOG_PATH}")
    print(f"[anima_corpus_hf_upload] rc={rc_overall}")
    if mode == "dry-run":
        print()
        print("[anima_corpus_hf_upload] DRY-RUN COMPLETE — no HF mutations performed.")
        print("[anima_corpus_hf_upload] To apply: python3 tool/anima_corpus_hf_upload.py --apply")
        print("[anima_corpus_hf_upload] (사용자 explicit directive 'OK CORPUS HF UPLOAD' 권고)")
    sys.exit(rc_overall)


if __name__ == "__main__":
    main()
