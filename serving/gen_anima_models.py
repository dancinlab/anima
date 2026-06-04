#!/usr/bin/env python3
"""gen_anima_models.py — build serving/anima_models.json from HF.jsonl + curated
engine families.

SSOT inputs:
  • root /HF.jsonl       — every ckpt/dataset row (a_hf_registry)
  • curated FAMILIES map  — the friendly `--engine <name>` aliases wired to a real
                            loader (omega/hexad/7b/chat/agent)

Output: serving/anima_models.json — one row per selectable model id:
  {id, aliases, hf_repo, arch, loader, params_m, lane, visibility,
   quality_label, loader_status, default_ckpt}

loader_status:
  • "wired"      — a real CPU/GPU loader exists for this arch (selectable → loads)
  • "no-loader ⏳" — no loader wired for this arch yet (selecting → honest stub)

Run from repo root:  python3 serving/gen_anima_models.py
This is a build tool; the committed serving/anima_models.json is the artifact the
CLI reads. Re-run after HF.jsonl changes to refresh the registry.

NO training, NO GPU, NO network — reads local HF.jsonl only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HF_JSONL = ROOT / "HF.jsonl"
OUT = ROOT / "serving" / "anima_models.json"

# ── curated engine families (--engine <name>) ──────────────────────────────
# Each family is wired to a REAL loader living in this repo. The `default_ckpt`
# is the HF repo whose primary weight file the loader consumes. params_m and
# quality_label per the FINAL spec + verified state (honest labels).
FAMILIES = [
    {
        "id": "omega",
        "aliases": ["omega", "conscious-decoder-v2", "cdv2"],
        "hf_repo": "dancinlab/clm-v4-omega-gpu-d384-gate",
        "arch": "ConsciousDecoderV2",
        "loader": "UNIVERSE/conscious_decoder.py",
        "params_m": 11.2,          # d384/6L/256-vocab byte CDV2 (gate ckpt)
        "lane": "Lane-G",
        "visibility": "public",
        "quality_label": "gen-weak",
        "loader_status": "wired",
        "default_ckpt": "omega_cdv2_d384.pt",
    },
    {
        "id": "hexad",
        "aliases": ["hexad", "engine-ag", "a-g", "engine_a_g"],
        "hf_repo": None,           # ckpt is a gitignored local phase2 cotrain ckpt
        "arch": "EngineAGModel",
        "loader": "training/engine_a_g_arch.py",
        "params_m": None,          # depends on local ckpt cfg (VERIFY at load)
        "lane": "Lane-A",
        "visibility": "private",
        "quality_label": "untested",
        "loader_status": "wired",
        # resolved at runtime by HEXAD/CHAT/anima_chat.py::_find_default_ckpt
        "default_ckpt": "phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
    },
    {
        "id": "7b",
        "aliases": ["7b", "ref-7b", "clm-7b"],
        "hf_repo": "dancinlab/clm-v1-ref-pytorch-cuda-7b",
        "arch": "CLMConvMoE-7B",
        "loader": "CLM/model/model.py",
        "params_m": 7000.0,
        "lane": "Lane-G",
        "visibility": "public",
        "quality_label": "gibberish-base",   # 5-lang wiki backbone, 0% dialogue, undertrained
        "loader_status": "wired",
        "default_ckpt": None,
    },
    {
        "id": "chat",
        "aliases": ["chat", "chat-18m", "rung0-chat"],
        "hf_repo": "dancinlab/anima-clm-chat-rung0-byte-18m",
        "arch": "ConsciousLMReconstructed",
        "loader": "training/persona_stage2_train_eval.py",
        "params_m": 18.13,
        "lane": "Lane-G",
        "visibility": "public",
        "quality_label": "coherent",   # p7 5/5 PASS, anti-Goodhart mirror 0/5 FAIL (verified)
        "loader_status": "wired",
        "default_ckpt": "chat_rung0_18m.pt",
    },
    {
        "id": "agent",
        "aliases": ["agent", "tooluse", "agent-rung0"],
        "hf_repo": None,           # rung-0 fire, not downloadable yet
        "arch": "agent_step_grounded",
        "loader": "AGENT/CORE/agent_loop.hexa",
        "params_m": None,
        "lane": "Lane-G",
        "visibility": "private",
        "quality_label": "⏳ training",
        "loader_status": "no-loader ⏳",   # tool-use model not trained/downloadable
        "default_ckpt": None,
    },
]

FAMILY_REPOS = {f["hf_repo"] for f in FAMILIES if f["hf_repo"]}

# Map an HF.jsonl row's base_model string → (arch, loader, loader_status).
# Only archs with a REAL loader in-repo are "wired"; everything else is honestly
# "no-loader ⏳" so selecting it yields a truthful stub, never a fake load.
WIRED_ARCH = {
    "ConsciousDecoderV2": ("ConsciousDecoderV2", "UNIVERSE/conscious_decoder.py"),
    "ConsciousDecoderV3": ("ConsciousDecoderV3", "UNIVERSE/conscious_decoder.py"),
}


def _params_m_from_notes(row: dict) -> float | None:
    """Best-effort param-count (M) parse — ONLY from explicit param-count phrasing
    in base_model/notes (e.g. '7B', '~1.5B', '18.13M', '530M params'). Honest None
    when no unambiguous param count is stated — never guess from byte sizes, step
    counts, corpus mixes (70wiki), or hidden dims (d1536/t512)."""
    # base_model is the authoritative arch string; notes is prose that mentions
    # OTHER models (e.g. '7B comparison') → false matches. Read base_model only.
    txt = row.get("base_model", "") or ""
    for m in re.finditer(r"(?<![A-Za-z0-9])([0-9]+(?:\.[0-9]+)?)\s*B\b", txt):
        val = float(m.group(1)) * 1000
        if val <= 200000:  # <=200B sane ceiling; reject byte-count false matches
            return round(val, 1)
    for m in re.finditer(r"(?<![A-Za-z0-9])([0-9]+(?:\.[0-9]+)?)\s*M\b", txt):
        val = float(m.group(1))
        if val <= 200000:
            return round(val, 1)
    return None


def _arch_of(row: dict) -> tuple[str, str | None, str]:
    bm = row.get("base_model", "") or ""
    for key, (arch, loader) in WIRED_ARCH.items():
        if key in bm:
            return arch, loader, "wired"
    # honest fallback: name the arch from base_model head, mark no-loader
    arch = bm.split("(")[0].strip() or bm.split()[0] if bm else "unknown"
    arch = arch[:48] if arch else "unknown"
    return arch, None, "no-loader ⏳"


def _quality_label(row: dict) -> str:
    notes = (row.get("notes") or "").lower()
    status = row.get("status")
    if status == "pending_upload":
        return "⏳ training"
    if "gibberish" in notes:
        return "gibberish-base"
    if "chat-pass" in notes or "coherent" in notes:
        return "coherent"
    if "gen-weak" in notes or "gen weak" in notes:
        return "gen-weak"
    return "untested"


def build() -> dict:
    rows = [json.loads(l) for l in HF_JSONL.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("run") != "_meta"]
    models = []
    for f in FAMILIES:
        models.append({
            "id": f["id"],
            "family": True,
            "aliases": f["aliases"],
            "hf_repo": f["hf_repo"],
            "arch": f["arch"],
            "loader": f["loader"],
            "params_m": f["params_m"],
            "lane": f["lane"],
            "visibility": f["visibility"],
            "quality_label": f["quality_label"],
            "loader_status": f["loader_status"],
            "default_ckpt": f["default_ckpt"],
        })
    # all HF.jsonl rows as selectable <id> (models only; datasets listed separately)
    for r in rows:
        repo = r.get("hf_repo_id")
        rtype = r.get("repo_type", "model")
        arch, loader, lstatus = _arch_of(r)
        models.append({
            "id": r.get("run"),
            "family": False,
            "aliases": [],
            "hf_repo": repo,
            "repo_type": rtype,
            "arch": arch,
            "loader": loader,
            "params_m": _params_m_from_notes(r),
            "lane": r.get("lane") or ("Lane-A" if "akida" in (r.get("notes","").lower()) else "Lane-G"),
            "visibility": ("public" if r.get("private") is False else "private"),
            "quality_label": _quality_label(r),
            "loader_status": lstatus,
            "default_ckpt": None,
            # a family repo already covers this id at the family level
            "covered_by_family": repo in FAMILY_REPOS,
        })
    n_wired = sum(1 for m in models if m["loader_status"] == "wired")
    return {
        "_meta": {
            "schema": ["id", "aliases", "hf_repo", "arch", "loader", "params_m",
                       "lane", "visibility", "quality_label", "loader_status",
                       "default_ckpt"],
            "source": "HF.jsonl + curated FAMILIES",
            "generator": "serving/gen_anima_models.py",
            "n_total": len(models),
            "n_families": len(FAMILIES),
            "n_wired": n_wired,
            "n_no_loader": len(models) - n_wired,
            "quality_label_enum": ["coherent", "gen-weak", "gibberish-base",
                                   "untested", "⏳ training"],
            "loader_status_enum": ["wired", "no-loader ⏳"],
            "note": "labels are INFORMATIONAL only — never block selection (FINAL spec)",
        },
        "models": models,
    }


if __name__ == "__main__":
    reg = build()
    OUT.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n")
    m = reg["_meta"]
    print(f"wrote {OUT.relative_to(ROOT)}: {m['n_total']} models "
          f"({m['n_families']} families · {m['n_wired']} wired · "
          f"{m['n_no_loader']} no-loader ⏳)")
