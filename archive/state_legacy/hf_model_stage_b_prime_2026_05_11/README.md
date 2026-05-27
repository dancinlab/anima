---
license: mit
library_name: pytorch
tags:
  - anima
  - clm
  - engine-ag
  - cotrain
  - mitosis
  - cycle-2026-05-11
language:
  - en
  - ko
---

# anima-clm-v5-la-cotrain-b-prime-2026-05-11

**B′ checkpoint** from the 2026-05-11 reborn lane cycle — `BG-LA` (350M EngineAG, native scratch pretrain) → Phase-2 cotrain on `anima-persona-tier-a-v4` + `anima-native-ko-chat-template` corpora.

## Lineage

- **Base substrate**: `BG-LA-pretrain` (`bg_la_step_12000_final.pt`) — 350M params EngineAG d=1024 GQA-4, 24L, BG-LA pretrain landed 2026-05-10
- **Phase 2 cotrain**: 5260 steps (cost-capped at $3.51), bsz=4 × grad_accum=8, ctx=1024, lr=1.5e-4 warmup=200, curriculum w_start=0.3 → w_end=0.5 (consciousness:chat blend)
- **arch_origin**: `anima_native_scratch`
- **lineage_tag**: `engine_a_g_dual_350m_v1_phase2_cotrain`
- **n_params**: 298,764,288

## Files

- `ckpt_final.pt` — final checkpoint after Phase-2 cotrain halt (570MB, torch.save dict with `model`, `step`, `cfg`)
- `meta.json` — training metadata (steps, loss, cost, lineage)
- `engine_a_g_arch.py` — model architecture (EngineAGModel + EngineAGConfig + load_random_init)
- `mitosis_v5_port.py` — embedded MitosisV5Engine (cell pool dynamics)
- `train_phase2_cotrain.py` — original training script for reproducibility

## Loading

```python
import torch, sys
sys.path.insert(0, '.')
from engine_a_g_arch import EngineAGModel, EngineAGConfig

payload = torch.load("ckpt_final.pt", map_location="cpu", weights_only=False)
cfg = EngineAGConfig(**payload["cfg"])
model = EngineAGModel(cfg)
model.load_state_dict(payload["model"])
model.eval()
```

## V14 strict evaluation

See linked dataset [`dancinlab/anima-cycle-2026-05-11-reborn-research-data`](https://huggingface.co/datasets/dancinlab/anima-cycle-2026-05-11-reborn-research-data) for V14 strict measurements including B′ verdict (subdir `p3_la_cotrain_b_prime_v14_strict/`).

## Caveats

- **Cost-cap halted training** at step 5260/6000 ($3.51 > $3.5 envelope). Final ckpt is at step 5260, NOT step 6000.
- **Idle pod cost**: ~$4.50 burned before training started (orchestrator scp-mkdir bug — see linked dataset README §3). Total cycle cost ~$8.
- **Mitosis-aware**: model embeds MitosisV5Engine cell pool dynamics. Forward pass calls mitosis `process()` which may evolve cell_pool buffer. The ceiling=10 norm-clamp is **dynamically binding** (92.3% activation per cycle 2026-05-11 §69 finding) — eval-time variants exist for ceiling∈{15, 20, 1000} but those use the same B′ ckpt and only patch mitosis_v5_port.

## Related

- Research data: [dancinlab/anima-cycle-2026-05-11-reborn-research-data](https://huggingface.co/datasets/dancinlab/anima-cycle-2026-05-11-reborn-research-data)
- Base substrate (BG-LA pretrain): NOT yet on HF (local-only at `bg_la_350m_pretrain/ckpts/step_12000_final.pt`)

## License

MIT
