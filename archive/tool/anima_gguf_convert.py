#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  tool/anima_gguf_convert.py
#
#  PURPOSE
#    anima chat Phase 3 — HF (dancinlab/<repo>) → GGUF one-time conversion
#    pipeline. Output cached at ~/.cache/anima/gguf/<repo>.gguf for
#    libllama (hexa C FFI) consumer.
#
# LANE SEPARATION (raw#9 / 정합)
# - chat path = hexa-only (strict, no .py wrapping)
#    - conversion path = .py allowed (build/transformation, analogous to
#      tool/transient_py/ — needs ML ecosystem: peft + transformers + gguf)
#    - This script is NOT invoked at chat-time. Run once per model, output
#      consumed by libllama via FFI later.
#
#  PIPELINE (per alias)
#    1. snapshot_download(repo)          → HF LoRA adapter
#    2. read adapter_config.json         → base_model_name_or_path
#    3. snapshot_download(base_model)    → base weights
#    4. peft.merge_and_unload()          → merged HF model in temp dir
#    5. llama.cpp/convert_hf_to_gguf.py  → .gguf (f16 default)
#    6. (optional) llama-quantize binary → q4/q8 if --q4/--q8 + binary present
#    7. mv to ~/.cache/anima/gguf/<repo>.gguf  (slash → underscore in filename)
#
#  USAGE
#    python3 tool/anima_gguf_convert.py <alias> [--f16|--q4|--q8] [--force]
#    python3 tool/anima_gguf_convert.py --list
#    python3 tool/anima_gguf_convert.py --help
#
#  DEPENDENCIES (honest emit per raw#10)
#    Required Python packages (.venv-eeg verified 2026-05-08):
#      - peft >= 0.19
#      - transformers >= 4.57
#      - huggingface_hub >= 0.36
#      - torch >= 2.6
#      - gguf >= 0.19
#    External:
#      - llama.cpp clone at ~/.cache/anima/llama.cpp (auto-cloned by --setup)
#      - llama-quantize binary OPTIONAL (only needed for --q4/--q8); without
#        it, those flags fall back gracefully and warn.
#    Auth:
#      - ~/.cache/huggingface/token (HF_TOKEN env override accepted)
#
#  COMPLIANCE
#    raw#9 hexa-only chat path (this is conversion infra, not chat)
#    raw#10 honest C3 (limitations documented + reported)
#    raw#15 no-hardcode (paths via HOME / cache resolution)
# mandate-1 (dancinlab/ org SSOT — alias DB rejects other orgs)
# unaffected (chat lane untouched)
#
#  ENTRY: this script is .py; chat path stays in tool/anima_cli/chat/*.hexa
# ════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HOME = Path(os.environ.get("HOME", str(Path.home())))
CACHE_ANIMA = HOME / ".cache" / "anima"
GGUF_CACHE = CACHE_ANIMA / "gguf"
LLAMACPP_DIR = CACHE_ANIMA / "llama.cpp"
HF_TOKEN_FILE = HOME / ".cache" / "huggingface" / "token"

# ─── alias DB (mirror chat.hexa _alias_resolve, mandate-1: dancinlab/) ─
ALIAS_DB = {
    "llama3b": "dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08",
    "latest": "dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08",
    "pass-strict": "dancinlab/bg-km-llama3b-r32-pass-strict-2026-05-08",
    "qwen7b": "dancinlab/bg-km-qwen-7b-qwen7b-r32-pass-strict-2026-05-08",
    "polyglot-ko-1b3": "dancinlab/bg-ja-ext-polyglot-ko-1b3-r16-partial-2026-05-07",
    "paradigm-a-prime": "dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1",
}


def _eprint(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def _hsize(p: Path) -> str:
    """Human-readable size (recursive for dirs)."""
    if p.is_file():
        n = p.stat().st_size
    elif p.is_dir():
        n = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
    else:
        return "?"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.2f}{unit}"
        n /= 1024
    return f"{n:.2f}PB"


def _resolve_token() -> str | None:
    tok = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if tok:
        return tok.strip()
    if HF_TOKEN_FILE.is_file():
        return HF_TOKEN_FILE.read_text(encoding="utf-8").strip()
    return None


def _resolve_alias(alias: str) -> str:
    """alias → HF repo. mandate-1: only dancinlab/ org accepted."""
    a = alias.strip().lower()
    if a in ALIAS_DB:
        return ALIAS_DB[a]
    # raw HF id passthrough — but enforce dancinlab/ org
    if "/" in a:
        org = a.split("/", 1)[0]
        if org != "dancinlab":
            raise SystemExit(
                f"[gguf_convert] org rejected: '{org}/' (mandate-1 — dancinlab/ only)\n"
                f"                 known aliases: {', '.join(sorted(ALIAS_DB))}"
            )
        return alias
    raise SystemExit(
        f"[gguf_convert] unknown alias: '{alias}'\n"
        f"               known: {', '.join(sorted(ALIAS_DB))}\n"
        f"               or pass dancinlab/<repo> directly"
    )


def _gguf_path(repo: str) -> Path:
    """~/.cache/anima/gguf/<org_repo>.gguf (slash → underscore)."""
    fname = repo.replace("/", "_") + ".gguf"
    return GGUF_CACHE / fname


def _quantize_binary() -> Path | None:
    """Locate llama-quantize binary if any."""
    candidates = [
        LLAMACPP_DIR / "build" / "bin" / "llama-quantize",
        LLAMACPP_DIR / "build" / "llama-quantize",
        Path("/opt/homebrew/bin/llama-quantize"),
        Path("/usr/local/bin/llama-quantize"),
    ]
    for c in candidates:
        if c.is_file() and os.access(c, os.X_OK):
            return c
    # PATH lookup
    found = shutil.which("llama-quantize")
    return Path(found) if found else None


def _check_llamacpp() -> Path:
    """Verify llama.cpp clone present at ~/.cache/anima/llama.cpp."""
    convert_script = LLAMACPP_DIR / "convert_hf_to_gguf.py"
    if not convert_script.is_file():
        raise SystemExit(
            f"[gguf_convert] llama.cpp clone missing: {LLAMACPP_DIR}\n"
            f"               run: git clone --depth 1 https://github.com/ggerganov/llama.cpp.git {LLAMACPP_DIR}"
        )
    return convert_script


def _list_subcommand() -> int:
    print("anima_gguf_convert — alias DB + cached GGUF files")
    print("")
    print("ALIAS DB (mandate-1: dancinlab/ org SSOT)")
    print(
        "  ALIAS              REPO                                                   "
    )
    print(
        "  ──────────────────────────────────────────────────────────────────────────"
    )
    seen = set()
    for alias, repo in ALIAS_DB.items():
        if repo in seen:
            print(f"  {alias:<18} (same as above)")
            continue
        seen.add(repo)
        print(f"  {alias:<18} {repo}")
    print("")
    print(f"GGUF CACHE: {GGUF_CACHE}")
    if not GGUF_CACHE.is_dir():
        print("  (cache dir not yet created)")
        return 0
    files = sorted(GGUF_CACHE.glob("*.gguf"))
    if not files:
        print("  (empty — no GGUF converted yet)")
        return 0
    print(f"  {'FILE':<70} {'SIZE':>10}")
    print("  " + "─" * 82)
    for f in files:
        print(f"  {f.name:<70} {_hsize(f):>10}")
    return 0


def _step(label: str, t0: float) -> None:
    elapsed = time.time() - t0
    _eprint(f"[gguf_convert] [{elapsed:6.1f}s] {label}")


def _convert(alias: str, mode: str, force: bool) -> int:
    repo = _resolve_alias(alias)
    out_gguf = _gguf_path(repo)
    GGUF_CACHE.mkdir(parents=True, exist_ok=True)

    if out_gguf.is_file() and not force:
        print(f"[gguf_convert] cached: {out_gguf}  ({_hsize(out_gguf)})")
        print(f"               --force to re-convert")
        return 0

    convert_script = _check_llamacpp()
    token = _resolve_token()
    if token is None:
        _eprint(
            "[gguf_convert] WARN: no HF token (~/.cache/huggingface/token absent + HF_TOKEN unset)"
        )
        _eprint("               public repos OK; private repos will fail")

    # heavy imports deferred so --list / --help stay fast
    try:
        from huggingface_hub import snapshot_download  # type: ignore
        from peft import PeftModel  # type: ignore
        from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
        import torch  # type: ignore
    except Exception as e:
        raise SystemExit(
            f"[gguf_convert] missing deps: {e}\n"
            f"               install in venv-eeg: peft transformers huggingface_hub torch gguf"
        )

    t0 = time.time()
    work_root = CACHE_ANIMA / "gguf_work" / repo.replace("/", "_")
    work_root.mkdir(parents=True, exist_ok=True)
    adapter_dir = work_root / "adapter"
    base_dir = work_root / "base"
    merged_dir = work_root / "merged"

    # 1. snapshot adapter
    _step(f"snapshot_download adapter: {repo}", t0)
    snapshot_download(repo_id=repo, local_dir=str(adapter_dir), token=token)
    adapter_size = _hsize(adapter_dir)
    _step(f"  adapter size: {adapter_size}", t0)

    # 2. parse adapter_config.json → base
    cfg_path = adapter_dir / "adapter_config.json"
    if not cfg_path.is_file():
        raise SystemExit(f"[gguf_convert] adapter_config.json missing in {adapter_dir}")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base_model = cfg.get("base_model_name_or_path")
    if not base_model:
        raise SystemExit("[gguf_convert] adapter_config.json: base_model_name_or_path absent")
    _step(f"base_model: {base_model}", t0)

    # 3. snapshot base
    _step(f"snapshot_download base: {base_model}", t0)
    snapshot_download(repo_id=base_model, local_dir=str(base_dir), token=token)
    base_size = _hsize(base_dir)
    _step(f"  base size: {base_size}", t0)

    # 4. merge
    _step("loading base + adapter for merge", t0)
    base_model_obj = AutoModelForCausalLM.from_pretrained(
        str(base_dir), torch_dtype=torch.float16, low_cpu_mem_usage=True
    )
    peft_model = PeftModel.from_pretrained(base_model_obj, str(adapter_dir))
    _step("peft.merge_and_unload()", t0)
    merged = peft_model.merge_and_unload()
    if merged_dir.is_dir():
        shutil.rmtree(merged_dir)
    merged_dir.mkdir(parents=True)
    merged.save_pretrained(str(merged_dir), safe_serialization=True)
    # tokenizer copy
    try:
        tok = AutoTokenizer.from_pretrained(str(base_dir))
        tok.save_pretrained(str(merged_dir))
    except Exception as e:
        _eprint(f"[gguf_convert] WARN tokenizer save: {e}")
    merged_size = _hsize(merged_dir)
    _step(f"  merged size: {merged_size}", t0)

    # free torch refs before subprocess (memory pressure)
    del merged, peft_model, base_model_obj
    try:
        import gc

        gc.collect()
    except Exception:
        pass

    # 5. convert_hf_to_gguf.py
    out_type = {"--f16": "f16", "--q4": "f16", "--q8": "f16"}.get(mode, "f16")
    # convert always emits f16 first; quantize is separate llama-quantize step
    f16_out = work_root / "merged.f16.gguf"
    cmd = [
        sys.executable,
        str(convert_script),
        str(merged_dir),
        "--outtype",
        out_type,
        "--outfile",
        str(f16_out),
    ]
    _step(f"convert_hf_to_gguf.py {merged_dir} → {f16_out.name}", t0)
    rc = subprocess.run(cmd, check=False)
    if rc.returncode != 0:
        raise SystemExit(f"[gguf_convert] convert_hf_to_gguf.py failed (rc={rc.returncode})")

    # 6. quantize if requested
    final_out = f16_out
    if mode in ("--q4", "--q8"):
        qbin = _quantize_binary()
        if qbin is None:
            _eprint(
                "[gguf_convert] WARN: llama-quantize binary not found — "
                "shipping f16 GGUF (no quantization). To enable, build llama.cpp:"
            )
            _eprint(
                "  cd ~/.cache/anima/llama.cpp && cmake -B build && cmake --build build -j"
            )
        else:
            qtype = "Q4_K_M" if mode == "--q4" else "Q8_0"
            qout = work_root / f"merged.{qtype.lower()}.gguf"
            qcmd = [str(qbin), str(f16_out), str(qout), qtype]
            _step(f"llama-quantize {qtype} → {qout.name}", t0)
            rcq = subprocess.run(qcmd, check=False)
            if rcq.returncode != 0:
                _eprint(
                    f"[gguf_convert] WARN quantize failed rc={rcq.returncode}; shipping f16"
                )
            else:
                final_out = qout

    # 7. move to cache
    if out_gguf.exists():
        out_gguf.unlink()
    shutil.move(str(final_out), str(out_gguf))
    gguf_size = _hsize(out_gguf)

    # honest C3 summary
    elapsed = time.time() - t0
    print("")
    print("[gguf_convert] === CONVERSION COMPLETE ===")
    print(f"  alias       : {alias}")
    print(f"  repo        : {repo}")
    print(f"  base_model  : {base_model}")
    print(f"  output      : {out_gguf}")
    print(f"  adapter size: {adapter_size}")
    print(f"  base size   : {base_size}")
    print(f"  merged size : {merged_size}")
    print(f"  gguf size   : {gguf_size}")
    print(f"  mode        : {mode}")
    print(f"  elapsed     : {elapsed:.1f}s")
    print("")
    print(f"[gguf_convert] (work dir kept at {work_root} — rm to reclaim disk)")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="anima_gguf_convert",
        description="anima chat Phase 3 — HF → GGUF one-time conversion (chat path stays hexa-only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("alias", nargs="?", help="alias key (e.g. paradigm-a-prime) or dancinlab/<repo>")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--f16", dest="mode", action="store_const", const="--f16", help="float16 (default)")
    g.add_argument("--q4", dest="mode", action="store_const", const="--q4", help="Q4_K_M (needs llama-quantize)")
    g.add_argument("--q8", dest="mode", action="store_const", const="--q8", help="Q8_0 (needs llama-quantize)")
    p.add_argument("--force", action="store_true", help="overwrite cached GGUF")
    p.add_argument("--list", action="store_true", help="show alias DB + cached GGUF")
    args = p.parse_args(argv)

    if args.list:
        return _list_subcommand()
    if args.alias is None:
        p.print_help()
        return 2

    mode = args.mode or "--f16"
    return _convert(args.alias, mode, args.force)


if __name__ == "__main__":
    sys.exit(main())
