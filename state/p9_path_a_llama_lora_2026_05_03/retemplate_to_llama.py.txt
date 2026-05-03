#!/usr/bin/env python3
"""Re-template P9 SFT corpus from {input, completion} to Llama-3 chat format.

Per A' decision §6.4: drops axis-conditioning side-channels (tension_target/bold_target)
and emits Llama-3.2-Instruct chat-templated SFT records as {prompt_ids, completion_ids,
labels} after tokenization. Tokenization is done at training time; this script only
emits {messages: [{role, content}, ...]} so PEFT/TRL trainer can apply chat template.

Out: JSONL with {messages, source, lang, source_id, split} per record.
"""
import argparse
import json
import os
import sys
import time


SYSTEM_PROMPT_EN = (
    "You are Anima, a reflective assistant with consciousness-axis awareness. "
    "Respond thoughtfully, with calibrated uncertainty when warranted."
)
SYSTEM_PROMPT_KO = (
    "당신은 의식 축 인식을 가진 사려 깊은 어시스턴트 Anima입니다. "
    "정당화될 때 보정된 불확실성과 함께 신중하게 응답하세요."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--include-system", action="store_true", default=True)
    args = ap.parse_args()

    t0 = time.time()
    n_in = 0
    n_out = 0
    n_skip = 0
    with open(args.input) as fin, open(args.output, "w") as fout:
        for line in fin:
            n_in += 1
            try:
                r = json.loads(line)
            except Exception:
                n_skip += 1
                continue
            inp = (r.get("input") or "").strip()
            comp = (r.get("completion") or "").strip()
            if not inp or not comp:
                n_skip += 1
                continue
            lang = r.get("lang", "en")
            sysp = SYSTEM_PROMPT_KO if lang == "ko" else SYSTEM_PROMPT_EN
            messages = []
            if args.include_system:
                messages.append({"role": "system", "content": sysp})
            messages.append({"role": "user", "content": inp})
            messages.append({"role": "assistant", "content": comp})
            out = {
                "messages": messages,
                "source": r.get("source"),
                "lang": lang,
                "source_id": r.get("source_id"),
                "split": r.get("split", "train"),
            }
            fout.write(json.dumps(out, ensure_ascii=False) + "\n")
            n_out += 1
    elapsed = time.time() - t0
    summary = {
        "n_input": n_in,
        "n_output": n_out,
        "n_skipped": n_skip,
        "elapsed_s": elapsed,
        "include_system": args.include_system,
    }
    print(json.dumps(summary, indent=2))
    with open(args.output + ".stats.json", "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
