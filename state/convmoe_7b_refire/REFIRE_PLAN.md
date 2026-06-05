# M13 7B-undertrained ENGINE rung — RE-FIRE on bigger GPU

Prior attempt FAILED: d6208/L30/E30 (7.057B) was at the 80GB H100 edge (seq512 fwd 73.4GB),
bs=1/accum=32 squeeze fragile, pod reclaimed mid-fit, NO .clm produced (nothing on HF).

FIX (a_wall_first): rent ONE H200 141GB so 7B fits seq512 with headroom + batch>1 stable.

- Config: d6208/L30/E30 CLMConvMoE = 7.0568B (recomputed, matches prior claim)
- Corpus: R2 phanes anima-7b/web/{eng,fra,deu,spa,kor}/ byte-direct, ~3GB/lang = ~15GB balanced (incl ko)
- seq512, bf16, AdamW8bit, ~3000-4000 steps bounded-undertrained
- Resume the prior WIP fire script (CLM/train/fire_7b_undertrained.sh) + train_lane_p_3b.py (serialize_v3, train/val split)
- dilation cap min(2**i,512) verified in model.py

Resilience: timestamped branch off origin/main + WIP commit BEFORE training (this commit).
Poll inline in ONE Bash loop. NEVER arm a Monitor/waiter.
