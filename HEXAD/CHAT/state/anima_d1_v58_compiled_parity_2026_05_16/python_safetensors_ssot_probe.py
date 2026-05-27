"""python_safetensors_ssot_probe.py — T3 compiled-parity Python SSOT.

The original 2026-05-12 interp parity (PSCC §43) used anima_chat.py's
AnimaChat(ckpt=.pt). On the ubu T3 host only the BF16 .safetensors
sibling exists (the source .pt was not retained — see ckpt_phase1a1
.meta.json `source_pt`). This probe loads the SAME weights from the
.safetensors directly into the SAME EngineAGModel arch, so both the
Python SSOT and the hexa-compiled lane consume the identical 597,550,688
byte .safetensors — a tighter parity contract than the original
(.pt-python vs .safetensors-hexa).

Forward path mirrors anima_chat.py: full EngineAGModel.forward (Engine G
weights present and active). Reports:
  (A) BOS-only single forward argmax  (SSOT for v58_hexa_parity.hexa)
  (B) 5-step greedy chain from BOS    (SSOT for v58_hexa_multi_parity.hexa)

Output JSON: state/anima_d1_v58_compiled_parity_2026_05_16/python_ssot.json
"""
import json
import os
import sys
import time
import datetime
import hashlib
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", os.getcwd()))
sys.path.insert(0, str(ANIMA_ROOT))

import torch
from safetensors.torch import load_file

from training.engine_a_g_arch import EngineAGModel, EngineAGConfig

CKPT = os.environ.get(
    "T3_CKPT",
    str(ANIMA_ROOT
        / "state/anima_phase1a1_color_cosmology_2026_05_12"
        / "ckpts/ckpt_phase1a1_sft.safetensors"),
)
BOS = 1
VOCAB = 32000


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("=" * 64)
    print("T3 Python SSOT — safetensors → EngineAGModel (Engine G active)")
    print("=" * 64)
    ck_sha = sha256(CKPT)
    ck_sz = os.path.getsize(CKPT)
    print(f"ckpt      : {CKPT}")
    print(f"ckpt sha  : {ck_sha}")
    print(f"ckpt bytes: {ck_sz}")

    t0 = time.time()
    cfg = EngineAGConfig()  # defaults == ckpt .meta.json (d=1024, 24L, h=16, kv=4)
    model = EngineAGModel(cfg).to("cpu")
    sd = load_file(CKPT, device="cpu")
    # lm_head.weight tied to tok_emb.weight (safetensors omits lm_head; meta
    # tied_aliases). EngineAGModel ties in __init__ when cfg.tie_lm_head.
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.eval()
    boot = time.time() - t0
    # Honest: report any non-tied missing/unexpected (engine_g.* should all
    # be present; tok_emb/lm_head tied).
    miss_real = [m for m in missing if m != "lm_head.weight"]
    print(f"[boot] loaded in {boot:.1f}s  missing={len(missing)} "
          f"(non-tied {len(miss_real)})  unexpected={len(unexpected)}")
    if miss_real:
        print(f"  missing(non-tied): {miss_real[:6]}")
    if unexpected:
        print(f"  unexpected: {list(unexpected)[:6]}")

    # ── (A) BOS-only single forward ────────────────────────────────────
    ids = [BOS]
    x = torch.tensor([ids], dtype=torch.long)
    t1 = time.time()
    with torch.no_grad():
        out = model(x)
        logits = out["logits"] if isinstance(out, dict) else (
            out[0] if isinstance(out, tuple) else out)
        last = logits[0, -1].float()
        bos_argmax = int(torch.argmax(last).item())
        bos_val = float(last[bos_argmax].item())
        tv, ti = torch.topk(last, 5)
        bos_top5 = [int(ti[i]) for i in range(5)]
    bos_wall = time.time() - t1
    print(f"(A) BOS  argmax_id={bos_argmax} val={bos_val:+.5f} "
          f"top5={bos_top5} wall={bos_wall:.2f}s")

    # ── (B) 5-step greedy chain from BOS (re-feed full seq, no KV) ──────
    ids = [BOS]
    chain = []
    t2 = time.time()
    for step in range(5):
        x = torch.tensor([ids], dtype=torch.long)
        with torch.no_grad():
            out = model(x)
            logits = out["logits"] if isinstance(out, dict) else (
                out[0] if isinstance(out, tuple) else out)
            last = logits[0, -1].float()
            am = int(torch.argmax(last).item())
            av = float(last[am].item())
        chain.append({"step": step, "t": len(ids) - 1,
                       "seq_len": len(ids), "argmax_id": am,
                       "argmax_val": round(av, 6)})
        print(f"  step {step}: t={len(ids)-1} seq_len={len(ids)} "
              f"argmax_id={am} val={av:+.5f}")
        ids.append(am)
    chain_wall = time.time() - t2
    chain_ids = [c["argmax_id"] for c in chain]
    print(f"(B) chain = {chain_ids}  wall={chain_wall:.2f}s")

    payload = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": CKPT,
        "ckpt_sha256": ck_sha,
        "ckpt_bytes": ck_sz,
        "device": "cpu",
        "boot_s": round(boot, 2),
        "load_missing": len(missing),
        "load_missing_nontied": miss_real,
        "load_unexpected": list(unexpected),
        "bos": {
            "input_token_ids": [BOS],
            "position_t": 0,
            "argmax_id": bos_argmax,
            "argmax_val": round(bos_val, 6),
            "top5": bos_top5,
            "wall_s": round(bos_wall, 3),
        },
        "chain": {
            "initial_seed_ids": [BOS],
            "n_steps": 5,
            "steps": chain,
            "final_argmax_chain": chain_ids,
            "wall_s": round(chain_wall, 3),
        },
        "torch_version": torch.__version__,
    }
    out_path = (ANIMA_ROOT
                / "state/anima_d1_v58_compiled_parity_2026_05_16"
                / "python_ssot.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nsaved: {out_path}")


if __name__ == "__main__":
    main()
