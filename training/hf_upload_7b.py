#!/usr/bin/env python3
"""hf_upload_7b.py — upload the 7B chat+persona stage-B ckpt + artifacts to HF Hub.

Visibility per a_hf_autonomous: PUBLIC iff closure PASS (chat retained + persona signal real
+ anti-Goodhart), else PRIVATE (WIP/FAIL). Attaches model card + the verdict JSONs.

USAGE
  HF_TOKEN=... python3 hf_upload_7b.py --ckpt /root/ws/out/chat_persona_7b_stageB.pt \
      --out-dir /root/ws/out --repo dancinlab/anima-clm-chat-persona-7b --private  # or --public
"""
import argparse, json, os
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--public", action="store_true")
    ap.add_argument("--card", default=None)
    args = ap.parse_args()
    token = os.environ["HF_TOKEN"]
    api = HfApi(token=token)
    create_repo(args.repo, repo_type="model", private=not args.public, exist_ok=True, token=token)
    out = Path(args.out_dir)
    files = [args.ckpt] + [str(out / f) for f in (
        "summary.json", "p7_base_trained.json", "p7_base_mirror.json",
        "persona_voice_trained.json", "persona_voice_mirror.json",
        "train_eval.log", "demo_transcript.txt", "ckpt_sha256.txt")]
    if args.card:
        files.append(args.card)
    for f in files:
        if Path(f).exists():
            name = "README.md" if (args.card and f == args.card) else Path(f).name
            print(f"[hf] upload {f} -> {name}", flush=True)
            upload_file(path_or_fileobj=f, path_in_repo=name, repo_id=args.repo,
                        repo_type="model", token=token)
    print(f"[hf] done: https://huggingface.co/{args.repo} (private={not args.public})", flush=True)


if __name__ == "__main__":
    main()
