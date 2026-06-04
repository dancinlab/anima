#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""anima_cli.py — the `anima` CLI (FINAL spec).

Behavior
--------
  anima                  bare — IF active engine's model is cached → ENTER CHAT now.
                         ELSE (first run) → interactive model-download SELECTION SCREEN.
  anima --engine <name>  select an engine FAMILY by friendly name; download ckpt
                         if not cached; chat; persist active.
  anima --model          open the SELECTION SCREEN explicitly (browse + download);
                         do NOT auto-chat.
  anima --list           print the registry (non-interactive); do NOT chat.

NO forced default model. Active engine persisted in ~/.anima/config.json
({active_engine, downloaded:[...]}). Honest quality labels (coherent / gen-weak /
gibberish-base / untested / ⏳ training) are INFORMATIONAL only — never block.

Philosophy (p1..p4): NO system prompt, NO identity rules, NO persona injection,
NO assistant framing. The chat REPL feeds the user's text to the active engine's
own trained byte-continuation mouth and prints exactly what the weights emit. The
only scaffolding is the data-format the model was trained on (사용자:/도우미:
byte-continuation conditioning), which is corpus structure, not an injected role.

This is a THIN driver: it reuses the in-repo loaders (it does NOT reimplement an
engine). $0, CPU-only, no GPU/pod/training.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "serving" / "anima_models.json"
ANIMA_HOME = Path(os.environ.get("ANIMA_HOME", Path.home() / ".anima"))
CONFIG = ANIMA_HOME / "config.json"
MODELS_DIR = ANIMA_HOME / "models"

# ── tiny ANSI helpers ───────────────────────────────────────────────────────
def _c(s, code):
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else str(s)


def bold(s):  return _c(s, "1")
def dim(s):   return _c(s, "2")
def green(s): return _c(s, "32")
def yellow(s): return _c(s, "33")
def cyan(s):  return _c(s, "36")
def red(s):   return _c(s, "31")


LABEL_ICON = {
    "coherent": green("● coherent"),
    "gen-weak": yellow("◐ gen-weak"),
    "gibberish-base": red("○ gibberish-base"),
    "untested": dim("· untested"),
    "⏳ training": dim("⏳ training"),
}


# ── config ───────────────────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG.exists():
        try:
            return json.loads(CONFIG.read_text())
        except Exception:
            pass
    return {"active_engine": None, "downloaded": []}


def save_config(cfg: dict) -> None:
    ANIMA_HOME.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text())


def find_model(reg: dict, key: str) -> dict | None:
    """Resolve an engine/model by id or alias (case-insensitive)."""
    key = key.strip().lower()
    for m in reg["models"]:
        if m["id"].lower() == key or key in [a.lower() for a in m.get("aliases", [])]:
            return m
    return None


def model_cache_dir(m: dict) -> Path:
    return MODELS_DIR / m["id"]


def is_cached(m: dict, cfg: dict) -> bool:
    """A model counts as cached if its id is in config.downloaded AND its local
    cache dir has a weight file, OR (hexad) its local default_ckpt path exists."""
    if m["id"] in cfg.get("downloaded", []):
        d = model_cache_dir(m)
        if d.exists() and any(d.rglob("*.pt")) or any(d.rglob("*.clm")):
            return True
    # hexad: local gitignored ckpt resolved by anima_chat._find_default_ckpt
    if m["id"] == "hexad":
        try:
            sys.path.insert(0, str(REPO))
            from HEXAD.CHAT.anima_chat import DEFAULT_CKPT  # type: ignore
            return bool(DEFAULT_CKPT) and Path(DEFAULT_CKPT).exists()
        except Exception:
            return False
    return False


# ── selection screen ─────────────────────────────────────────────────────────
def _label(m):
    return LABEL_ICON.get(m["quality_label"], m["quality_label"])


def _params_str(m):
    p = m.get("params_m")
    if p is None:
        return dim("?")
    if p >= 1000:
        return f"{p/1000:.1f}B"
    return f"{p:.0f}M" if p == int(p) else f"{p:.1f}M"


def print_selection_screen(reg, cfg, families_only=False):
    print()
    print(bold("  anima — 엔진/모델 선택 (model selection)"))
    print(dim("  품질 라벨은 정보용입니다 (선택을 막지 않음). loader 없는 항목은 정직하게 표시됩니다."))
    print()
    fams = [m for m in reg["models"] if m.get("family")]
    others = [m for m in reg["models"] if not m.get("family")]
    rows = fams if families_only else (fams + others)
    print(bold("  엔진 패밀리 (--engine <name>):"))
    idx_map = {}
    n = 0
    for m in fams:
        n += 1
        idx_map[n] = m
        cached = green("✓ cached") if is_cached(m, cfg) else dim("download")
        wired = m["loader_status"]
        wired_s = green("wired") if wired == "wired" else yellow(wired)
        active = cyan(" ← active") if cfg.get("active_engine") == m["id"] else ""
        print(f"   {bold(str(n).rjust(3))}. {bold(m['id'].ljust(8))} "
              f"{_params_str(m).rjust(6)}  {_label(m).ljust(22)} "
              f"{wired_s.ljust(16)} {cached}{active}")
        print(f"        {dim(m['arch'] + '  ·  ' + (m['hf_repo'] or 'local-only ckpt'))}")
    if not families_only:
        print()
        print(bold(f"  전체 HF.jsonl 모델 ({len(others)}개) — id 선택 가능:"))
        for m in others:
            n += 1
            idx_map[n] = m
            cached = green("✓") if is_cached(m, cfg) else " "
            wired = (green("wired") if m["loader_status"] == "wired"
                     else dim("no-loader ⏳"))
            vis = m.get("visibility", "")
            print(f"   {str(n).rjust(3)}. {cached} {m['id'][:44].ljust(44)} "
                  f"{_params_str(m).rjust(6)} {_label(m).ljust(20)} "
                  f"{wired.ljust(14)} {dim(vis)}")
    print()
    return idx_map


def select_and_download(reg, cfg, families_only=False, auto_chat=True):
    """Show the selection screen, read a number, download, set active. Returns the
    chosen model dict (or None if the user quit)."""
    idx_map = print_selection_screen(reg, cfg, families_only=families_only)
    try:
        raw = input(bold("  번호 선택 (q=quit): ")).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    if raw.lower() in ("q", "quit", "exit", ""):
        return None
    if not raw.isdigit() or int(raw) not in idx_map:
        print(red(f"  ‹잘못된 선택: {raw}›"))
        return None
    m = idx_map[int(raw)]
    if m["loader_status"] != "wired":
        print(yellow(f"  ‹loader not wired for {m['arch']}› — 이 모델은 아직 "
                     f"실행 loader가 없습니다 (정직 표시, 가짜 로드 안 함)."))
        return None
    ok = ensure_downloaded(m, cfg)
    if not ok:
        return None
    set_active(m, cfg)
    return m if auto_chat else None


# ── download ─────────────────────────────────────────────────────────────────
def ensure_downloaded(m: dict, cfg: dict) -> bool:
    """Download the model's HF repo into ~/.anima/models/<id>/ if not cached.
    Returns True when a usable local weight is available. Honest on HF-unavailable."""
    if is_cached(m, cfg):
        print(green(f"  ✓ {m['id']} 이미 캐시됨."))
        return True
    if m["id"] == "hexad":
        print(red("  ‹hexad ckpt는 로컬 gitignored 파일입니다 — "
                  "phase2_cotrain_engine_ag/ckpts/ckpt_final.pt 없음›"))
        return False
    repo = m.get("hf_repo")
    if not repo:
        print(red(f"  ‹{m['id']}: HF repo 없음 (아직 다운로드 불가)›"))
        return False
    try:
        from huggingface_hub import snapshot_download
    except Exception:
        print(red("  ‹huggingface_hub 미설치 — download needs HF access. "
                  "캐시된 모델만 사용 가능.›"))
        return False
    dest = model_cache_dir(m)
    print(cyan(f"  ⇣ {repo} → {dest} 다운로드 중..."))
    try:
        snapshot_download(repo_id=repo, local_dir=str(dest))
    except Exception as e:
        print(red(f"  ‹다운로드 실패: {e}›"))
        print(dim("  (download needs HF access — 캐시된 모델만 사용 가능)"))
        return False
    cfg.setdefault("downloaded", [])
    if m["id"] not in cfg["downloaded"]:
        cfg["downloaded"].append(m["id"])
    save_config(cfg)
    print(green(f"  ✓ {m['id']} 다운로드 완료."))
    return True


def set_active(m: dict, cfg: dict) -> None:
    cfg["active_engine"] = m["id"]
    save_config(cfg)


# ── chat REPL (dispatch to the active engine's in-repo loader) ────────────────
def chat(m: dict, cfg: dict) -> int:
    print()
    print(bold(f"  anima · engine={m['id']} ({m['arch']})  {_label(m)}"))
    print(dim("  빈 줄 또는 /quit 로 종료. (p1..p4: no system-prompt/persona injection)"))
    print()
    sys.path.insert(0, str(REPO))
    arch = m["arch"]
    try:
        if arch == "ConsciousLMReconstructed":
            return _chat_byte_conscious(m, cfg)
        if arch == "ConsciousDecoderV2":
            return _chat_cdv2(m, cfg)
        if arch == "EngineAGModel":
            return _chat_hexad(m, cfg)
        print(red(f"  ‹loader not wired for {arch}›"))
        return 1
    except KeyboardInterrupt:
        print()
        return 0


def _repl(gen_one):
    """Shared REPL loop. gen_one(user_text) -> reply string."""
    while True:
        try:
            user = input(cyan("  나 ▷ ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if user in ("", "/quit", "/exit", "/q"):
            return 0
        reply = gen_one(user)
        print(f"  {bold('anima ◁')} {reply}")
        print()


def _find_weight(m, *names):
    d = model_cache_dir(m)
    for nm in names:
        p = d / nm
        if p.exists():
            return p
    for ext in ("*.pt", "*.clm"):
        for p in d.rglob(ext):
            return p
    return None


def _chat_byte_conscious(m, cfg):
    """`chat` engine — ConsciousLMReconstructed (18M byte). Reuses the in-repo
    arch + generate() verbatim from training/persona_stage2_train_eval.py."""
    import torch
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_anima_chat_arch", str(REPO / "training" / "persona_stage2_train_eval.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ckpt = _find_weight(m, "chat_rung0_18m.pt")
    if ckpt is None:
        print(red("  ‹weight 파일 없음›"))
        return 1
    ck = torch.load(str(ckpt), map_location="cpu", weights_only=False)
    cfgm = ck["config"]
    model = mod.ConsciousLMReconstructed(
        cfgm.get("vocab", 256), cfgm["dim"], cfgm["heads"],
        cfgm["layers"], cfgm["block_size"])
    model.load_state_dict(ck["model_state"])
    model.eval()

    history = []  # [(role, text)]

    def gen_one(user):
        # data-format conditioning the weights were trained on (NOT a system prompt)
        parts = []
        for role, txt in history[-6:]:
            parts.append(f"{'사용자' if role=='user' else '도우미'}: {txt}")
        parts.append(f"사용자: {user}\n도우미:")
        prompt = "\n".join(parts)
        reply = mod.generate(model, prompt, max_new=120, device="cpu",
                             temperature=0.8, top_k=40, rep_penalty=1.1)
        history.append(("user", user))
        history.append(("assistant", reply))
        return reply

    return _repl(gen_one)


def _chat_cdv2(m, cfg):
    """`omega` engine — ConsciousDecoderV2 (byte). Reuses UNIVERSE/conscious_decoder."""
    import torch
    from UNIVERSE.conscious_decoder import ConsciousDecoderV2  # type: ignore
    ckpt = _find_weight(m, "omega_cdv2_d384.pt")
    if ckpt is None:
        print(red("  ‹weight 파일 없음›"))
        return 1
    ck = torch.load(str(ckpt), map_location="cpu", weights_only=False)
    conf = ck.get("config", {})
    model = ConsciousDecoderV2(**conf)
    model.load_state_dict(ck["model"], strict=False)
    model.eval()
    bs = model.block_size

    def gen_one(user):
        ids = list(f"사용자: {user}\n도우미:".encode("utf-8"))[-bs:]
        idx = torch.tensor([ids], dtype=torch.long)
        out = model.generate(idx, max_new_tokens=min(120, bs - len(ids)),
                             temperature=0.8, top_k=50)
        new = out[0, len(ids):].tolist()
        txt = bytes(b for b in new if 0 <= b < 256).decode("utf-8", errors="ignore")
        for s in ("\n사용자", "사용자:", "\n"):
            i = txt.find(s)
            if i >= 0:
                txt = txt[:i]
        return txt.strip()

    return _repl(gen_one)


def _chat_hexad(m, cfg):
    """`hexad` engine — Engine A⇄G via in-repo AnimaChat (anima_chat.py)."""
    from HEXAD.CHAT.anima_chat import AnimaChat, DEFAULT_CKPT  # type: ignore
    if not (DEFAULT_CKPT and Path(DEFAULT_CKPT).exists()):
        print(red(f"  ‹hexad ckpt 없음: {DEFAULT_CKPT}›"))
        return 1
    session = AnimaChat(ckpt_path=DEFAULT_CKPT, device="cpu")

    def gen_one(user):
        return session.user(user)

    return _repl(gen_one)


# ── entry ────────────────────────────────────────────────────────────────────
def cmd_list(reg):
    m = reg["_meta"]
    print(f"anima models registry — {m['n_total']} models "
          f"({m['n_families']} families · {m['n_wired']} wired · "
          f"{m['n_no_loader']} no-loader ⏳)")
    for x in reg["models"]:
        fam = "FAMILY" if x.get("family") else "      "
        print(f"  {fam} {x['id'][:46].ljust(46)} {x['arch'][:30].ljust(30)} "
              f"{x['loader_status'].ljust(14)} {x['quality_label']}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="anima", add_help=True,
                                 description="anima CLI — substrate-native chat daemon")
    ap.add_argument("--engine", metavar="NAME",
                    help="엔진 패밀리 선택 (omega/hexad/7b/chat/agent or HF id)")
    ap.add_argument("--model", action="store_true",
                    help="선택 화면 열기 (browse+download, 채팅 자동진입 안 함)")
    ap.add_argument("--list", action="store_true",
                    help="레지스트리 출력 (비대화형)")
    args = ap.parse_args(argv)

    reg = load_registry()
    cfg = load_config()

    if args.list:
        cmd_list(reg)
        return 0

    if args.model:
        # explicit SELECTION SCREEN; do NOT auto-chat
        select_and_download(reg, cfg, auto_chat=False)
        return 0

    if args.engine:
        m = find_model(reg, args.engine)
        if m is None:
            print(red(f"  ‹알 수 없는 엔진: {args.engine}›  "
                      f"(`anima --model` 로 목록 확인)"))
            return 2
        if m["loader_status"] != "wired":
            print(yellow(f"  ‹loader not wired for {m['arch']}› — {m['id']} 은 "
                         f"아직 실행 loader가 없습니다."))
            return 2
        if not ensure_downloaded(m, cfg):
            return 1
        set_active(m, cfg)
        return chat(m, cfg)

    # bare `anima`
    active_id = cfg.get("active_engine")
    if active_id:
        m = find_model(reg, active_id)
        if m and is_cached(m, cfg):
            return chat(m, cfg)
    # first run (no active cached engine) → SELECTION SCREEN
    m = select_and_download(reg, cfg, auto_chat=True)
    if m is None:
        return 0
    return chat(m, cfg)


if __name__ == "__main__":
    sys.exit(main())
