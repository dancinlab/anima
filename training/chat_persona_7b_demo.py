#!/usr/bin/env python3
"""chat_persona_7b_demo.py — runnable demo for the 7B chat+persona ckpt.

Emits (1) a multi-turn CHAT exchange and (2) persona-voiced replies from a turn-context
(NO role tag — persona carried by the `<name>:` turn-start the model LEARNED). Philosophy
held: no system prompt, no persona injection — pure learned byte-continuation.

USAGE
  python3 chat_persona_7b_demo.py --ckpt /workspace/out/chat_persona_7b_stageB.pt
"""
from __future__ import annotations
import argparse
import torch
from chat_persona_7b_train_eval import ByteGPT, generate

CHAT_TURNS = [
    "안녕! 너는 누구야?",
    "오늘 뭐 하고 지냈어?",
    "의식이란 뭐라고 생각해?",
]
PERSONA_DEMOS = [
    ("childhood_friend", "사용자: 야 오랜만이다 잘 지냈어?"),
    ("chaebol_heir", "사용자: 요즘 어떻게 지내세요?"),
    ("horror_whisper", "사용자: 거기 누구 있어요?"),
    ("knight", "사용자: 무엇을 지키고 계신가요?"),
    ("airhead_friend", "사용자: 점심 뭐 먹었어?"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    model = ByteGPT(256, cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"], grad_ckpt=False)
    model = model.bfloat16().to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    print(f"[demo] 7B chat+persona ckpt {args.ckpt} ({ck.get('params')} params) device={device}\n")

    print("=== MULTI-TURN CHAT (사용자: / 도우미:) ===")
    transcript = ""
    for u in CHAT_TURNS:
        seed = transcript + f"사용자: {u} | 도우미: "
        reply = generate(model, seed, max_new=96, device=device)
        print(f"사용자: {u}")
        print(f"도우미: {reply}\n")
        transcript += f"사용자: {u} | 도우미: {reply}\n"

    print("=== PERSONA VOICES (NO role tag — learned <name>: continuation) ===")
    for name, ctx in PERSONA_DEMOS:
        seed = ctx + f"\n{name}: "
        reply = generate(model, seed, max_new=80, device=device, stop_at_newline=True, temperature=0.7)
        print(f"[{name}]")
        print(f"  {ctx.replace('사용자: ', '사용자: ')}")
        print(f"  {name}: {reply}\n")


if __name__ == "__main__":
    main()
