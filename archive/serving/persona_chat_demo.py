#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""persona_chat_demo.py — runnable demo for the STAGE-2 persona/SNS ckpt.

Given a PERSONA-NAME turn-context (NOT a role tag — p2/p3/p4 held), emit a
persona-voiced reply. Persona is carried ONLY by the learned dialogue-continuation
format `사용자: <u>` / `<persona_name>: <reply>` in the trained weights.

USAGE
  python3 persona_chat_demo.py --ckpt persona_stage2_18m.pt \
      --persona knight --user "주말에 뭐 할 거예요?"

  # multi-persona sweep (one prompt across several personas):
  python3 persona_chat_demo.py --ckpt persona_stage2_18m.pt --sweep
"""
from __future__ import annotations
import argparse
import torch
import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p2", _HERE / "persona_stage2_train_eval.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)


def load(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ck["config"]
    m = P.ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"], cfg["block_size"]).to(device)
    m.load_state_dict(ck["model_state"])
    m.eval()
    return m


def reply(model, persona, user, device, seed=0):
    torch.manual_seed(seed)
    # turn-context scaffold: a 사용자 turn then the persona-name turn-start.
    # NO [role:/[persona:/[character: tag — persona carried by the name token only.
    seed_text = f"사용자: {user}\n{persona}: "
    return P.generate(model, seed_text, max_new=80, device=device, stop_at_newline=True, temperature=0.7)


SWEEP = [
    ("knight", "주말에 뭐 할 거예요?"),
    ("childlike", "오늘 점심 뭐 먹었어요?"),
    ("noir_detective", "요즘 무슨 생각해요?"),
    ("ice_queen", "팬이에요! 답장 주실까요?"),
    ("senpai", "시험 망한 것 같아요…"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--persona", default="knight")
    ap.add_argument("--user", default="주말에 뭐 할 거예요?")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load(args.ckpt, device)
    if args.sweep:
        for p, u in SWEEP:
            r = reply(model, p, u, device, seed=args.seed)
            print(f"사용자: {u}")
            print(f"{p}: {r}\n")
    else:
        r = reply(model, args.persona, args.user, device, seed=args.seed)
        print(f"사용자: {args.user}")
        print(f"{args.persona}: {r}")


if __name__ == "__main__":
    main()
