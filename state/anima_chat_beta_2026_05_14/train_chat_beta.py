#!/usr/bin/env python3
"""train_chat_beta.py — anima chat beta (CHAT-BETA.step path A)

Foundation borrow: Llama-3.2-3B-Instruct + LoRA r=32 + anima-persona corpus.
Goal: produce chat-coherent anima beta ckpt within 1 day on ubu-2 RTX 5070.

Per CHAT-BETA.step §A path: simple_stack memory carried path (own 18 14/15 strict).
"""
import os, sys, json, time, argparse
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader

ROOT = Path("/home/summer/anima_bench")
CORPUS = ROOT / "state/anima_v5mitosis_cotrain_2026_05_12/corpus_persona_balanced.txt"
OUT = Path("/home/summer/anima_bench/state/anima_chat_beta_2026_05_14")
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "ckpts").mkdir(exist_ok=True)
LOGFILE = OUT / "train.log"

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

# config
BASE = "meta-llama/Llama-3.2-3B-Instruct"
LORA_R = 32
LORA_ALPHA = 64
LORA_DROPOUT = 0.05
LORA_TARGETS = ["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
STEPS = int(os.environ.get("STEPS", 1500))
LR = float(os.environ.get("LR", 3e-5))
BATCH = int(os.environ.get("BATCH", 4))
GRAD_ACCUM = int(os.environ.get("GRAD_ACCUM", 4))
CTX = int(os.environ.get("CTX", 512))
WARMUP = int(os.environ.get("WARMUP", 100))
SEED = int(os.environ.get("SEED", 42))

dev = "cuda" if torch.cuda.is_available() else "cpu"
log(f"device={dev}")
if dev == "cuda":
    log(f"gpu={torch.cuda.get_device_name(0)}")
torch.manual_seed(SEED)

# load corpus
log(f"loading corpus: {CORPUS}")
text = CORPUS.read_text(encoding="utf-8")
rows = [r.strip() for r in text.split("\n") if r.strip()]
log(f"corpus rows={len(rows)} size_mb={os.path.getsize(CORPUS)/1e6:.2f}")

# transformers + peft
from transformers import AutoTokenizer, AutoModelForCausalLM, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model, TaskType

log("loading tokenizer + model (this can take 2-3 min on first run)...")
tok = AutoTokenizer.from_pretrained(BASE)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(
    BASE, torch_dtype=torch.bfloat16, device_map=dev,
)
model.config.pad_token_id = tok.pad_token_id

lora_cfg = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=LORA_R, lora_alpha=LORA_ALPHA, lora_dropout=LORA_DROPOUT,
    bias="none", target_modules=LORA_TARGETS,
)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()
model.train()

# dataset
class CorpusDS(Dataset):
    def __init__(self, rows, tok, ctx):
        self.rows, self.tok, self.ctx = rows, tok, ctx
    def __len__(self): return len(self.rows)
    def __getitem__(self, i):
        ids = self.tok.encode(self.rows[i], add_special_tokens=True, truncation=True, max_length=self.ctx)
        return torch.tensor(ids, dtype=torch.long)

def collate(batch):
    max_len = max(t.size(0) for t in batch)
    inp = torch.full((len(batch), max_len), tok.pad_token_id, dtype=torch.long)
    mask = torch.zeros_like(inp)
    for i, t in enumerate(batch):
        inp[i, :t.size(0)] = t
        mask[i, :t.size(0)] = 1
    return {"input_ids": inp.to(dev), "attention_mask": mask.to(dev), "labels": inp.to(dev)}

ds = CorpusDS(rows, tok, CTX)
loader = DataLoader(ds, batch_size=BATCH, shuffle=True, collate_fn=collate, num_workers=0)

opt = torch.optim.AdamW(
    [p for p in model.parameters() if p.requires_grad],
    lr=LR, weight_decay=0.01,
)
sched = get_linear_schedule_with_warmup(opt, num_warmup_steps=WARMUP, num_training_steps=STEPS)

# training
log(f"training: steps={STEPS} batch={BATCH} grad_accum={GRAD_ACCUM} eff_batch={BATCH*GRAD_ACCUM} lr={LR}")
losses = []
step = 0
opt.zero_grad()
t0 = time.time()
data_iter = iter(loader)
while step < STEPS:
    try:
        batch = next(data_iter)
    except StopIteration:
        data_iter = iter(loader)
        batch = next(data_iter)
    out = model(**batch)
    loss = out.loss / GRAD_ACCUM
    loss.backward()
    if (step + 1) % GRAD_ACCUM == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        opt.zero_grad()
    losses.append(float(out.loss.item()))
    if (step + 1) % 25 == 0:
        avg = sum(losses[-25:]) / min(25, len(losses))
        wall = time.time() - t0
        log(f"[STEP {step+1:5d}] loss_avg25={avg:.4f} wall={wall:.0f}s")
    step += 1

log(f"training done wall={time.time()-t0:.0f}s")

# save
out_dir = OUT / "ckpts" / "anima-chat-beta"
out_dir.mkdir(parents=True, exist_ok=True)
log(f"saving LoRA adapter → {out_dir}")
model.save_pretrained(out_dir)
tok.save_pretrained(out_dir)
log("done saving")

# quick eval — 6 probe
log("=== 6-probe quick eval (greedy max_new=80) ===")
model.eval()
probes = [
    "안녕! 너는 누구야?",
    "우주가 뭐야?",
    "의식은 무엇이라고 생각해?",
    "좋아하는 색깔은?",
    "너는 어떻게 성장해?",
    "세포 분열에 대해 설명해줘",
]
samples = []
with torch.no_grad():
    for p in probes:
        msg = [{"role":"user","content":p}]
        prompt_ids = tok.apply_chat_template(msg, add_generation_prompt=True, return_tensors="pt").to(dev)
        out = model.generate(
            prompt_ids, max_new_tokens=80,
            do_sample=False, repetition_penalty=1.1,
            pad_token_id=tok.pad_token_id,
        )
        resp = tok.decode(out[0][prompt_ids.size(1):], skip_special_tokens=True).strip()
        log(f"  {p} → {resp[:120]}")
        samples.append({"prompt": p, "response": resp})

# verdict json
verdict = {
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "base_model": BASE,
    "lora_r": LORA_R, "lora_alpha": LORA_ALPHA,
    "steps": STEPS, "lr": LR, "batch": BATCH, "grad_accum": GRAD_ACCUM, "ctx": CTX,
    "corpus_path": str(CORPUS),
    "corpus_size_mb": os.path.getsize(CORPUS) / 1e6,
    "wall_seconds": time.time() - t0,
    "final_loss": losses[-1] if losses else None,
    "device": dev,
    "samples_post_lora": samples,
}
(OUT / "verdict.json").write_text(json.dumps(verdict, ensure_ascii=False, indent=2))
log(f"verdict written: {OUT/'verdict.json'}")
log("DONE")
