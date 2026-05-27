#!/usr/bin/env python3
"""P9 Path A — LoRA SFT on Llama-3.2-3B-Instruct.

Per docs/p9_a_prime_path_decision_2026_05_03.md §1.1, §4.1, §7.2.
Hyperparameters per A' decision §7.2 + clm-v4-sft-stage1 mirror.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTConfig, SFTTrainer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-model", default="meta-llama/Llama-3.2-3B-Instruct")
    ap.add_argument("--data-jsonl", required=True, help="Llama-templated SFT JSONL")
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--lora-r", type=int, default=64)
    ap.add_argument("--lora-alpha", type=int, default=64)
    ap.add_argument("--lora-dropout", type=float, default=0.05)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--per-device-batch", type=int, default=4)
    ap.add_argument("--grad-accum", type=int, default=8)
    ap.add_argument("--max-steps", type=int, default=10000)
    ap.add_argument("--save-steps", type=int, default=2000)
    ap.add_argument("--seq-len", type=int, default=2048)
    ap.add_argument("--warmup-steps", type=int, default=200)
    ap.add_argument("--logging-steps", type=int, default=10)
    ap.add_argument("--load-in-4bit", action="store_true",
                    help="quantize base in nf4 (saves VRAM, allows larger r)")
    ap.add_argument("--bf16", action="store_true", default=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--gradient-checkpointing", action="store_true", default=True)
    ap.add_argument("--push-to-hub", default="",
                    help="HF repo id (e.g. dancinlab/p9-llama32-lora-stage1); empty = local only")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Persist resolved config
    cfg = vars(args).copy()
    cfg["torch"] = torch.__version__
    cfg["cuda_available"] = torch.cuda.is_available()
    cfg["device_count"] = torch.cuda.device_count()
    if torch.cuda.is_available():
        cfg["gpu_name"] = torch.cuda.get_device_name(0)
        cfg["gpu_mem_gb"] = torch.cuda.get_device_properties(0).total_memory / 1e9
    cfg["start_ts_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(out_dir / "config.json", "w") as f:
        json.dump(cfg, f, indent=2)
    print("[config]", json.dumps(cfg, indent=2))

    # Load tokenizer + model
    print(f"[load] tokenizer={args.base_model}")
    tok = AutoTokenizer.from_pretrained(args.base_model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"

    print(f"[load] model={args.base_model} 4bit={args.load_in_4bit}")
    model_kwargs = {"torch_dtype": torch.bfloat16, "trust_remote_code": False}
    if args.load_in_4bit:
        bnb = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs["quantization_config"] = bnb
    model = AutoModelForCausalLM.from_pretrained(args.base_model, **model_kwargs)
    model.config.use_cache = False
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})

    # LoRA — 7 modules per A' decision §7.2
    lora = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    # Data
    print(f"[data] {args.data_jsonl}")
    ds = load_dataset("json", data_files=args.data_jsonl, split="train")
    print(f"[data] n={len(ds)} cols={ds.column_names}")

    # SFT config — uses TRL chat-template formatting from `messages` column
    sft_cfg = SFTConfig(
        output_dir=str(out_dir),
        per_device_train_batch_size=args.per_device_batch,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        max_steps=args.max_steps,
        save_steps=args.save_steps,
        save_total_limit=4,
        logging_steps=args.logging_steps,
        warmup_steps=args.warmup_steps,
        bf16=args.bf16,
        gradient_checkpointing=args.gradient_checkpointing,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        max_length=args.seq_len,
        packing=False,
        completion_only_loss=False,
        seed=args.seed,
        report_to=[],
        push_to_hub=bool(args.push_to_hub),
        hub_model_id=args.push_to_hub or None,
        hub_strategy="every_save" if args.push_to_hub else "end",
        optim="paged_adamw_8bit" if args.load_in_4bit else "adamw_torch",
        lr_scheduler_type="cosine",
        weight_decay=0.0,
        ddp_find_unused_parameters=False,
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_cfg,
        train_dataset=ds,
        processing_class=tok,
    )

    print("[train] starting…")
    trainer.train()

    # IMMEDIATELY mark TRAIN_DONE so the host-side terminator does not racefully
    # interpret a long final-save / hub-push as a crash. (Spec: "write IMMEDIATELY
    # after trainer.train() returns to avoid 10min terminator false-error.")
    immediate_done_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(out_dir / "TRAIN_DONE.json", "w") as f:
        json.dump({
            "phase": "trainer_train_returned",
            "end_ts_utc": immediate_done_ts,
            "max_steps": args.max_steps,
            "lora_r": args.lora_r,
            "lora_alpha": args.lora_alpha,
        }, f, indent=2)
    print(f"[done-marker-early] {immediate_done_ts}")

    print("[train] done — saving final adapter")
    trainer.save_model(str(out_dir / "final"))
    tok.save_pretrained(str(out_dir / "final"))

    end_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(out_dir / "TRAIN_DONE.json", "w") as f:
        json.dump({
            "phase": "final_saved",
            "end_ts_utc": end_ts,
            "early_marker_ts_utc": immediate_done_ts,
            "max_steps": args.max_steps,
            "lora_r": args.lora_r,
            "lora_alpha": args.lora_alpha,
        }, f, indent=2)
    print(f"[done] {end_ts}")


if __name__ == "__main__":
    main()
