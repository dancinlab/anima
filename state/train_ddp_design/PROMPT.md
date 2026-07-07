You are designing multi-GPU (data-parallel) training support for the anima repo's trainers. This is a DESIGN + SPEC task — produce a concrete, faithful, implementation-ready plan (I will implement it locally afterward).

# Context — anima trainers (two production surfaces, byte-parity lockstep)
anima trains a 303M byte-level CLMConvMoE (CONV mouth) + ByteGPT, torch Lane-P.
- `cli/train.py` = the CANONICAL python trainer (`anima train --py` → this). torch. It is the currently-working GPU-bound path. Single-GPU today (grep for DistributedDataParallel/DataParallel/dist./world_size = 0 hits — NO multi-GPU anything).
- `cli/train.hexa` = the hexa-native production trainer (`anima train` without `--py`). Mid GPU-util fix (single-thread CPU-scalar-bound). The two are meant to be a byte-parity lockstep pair ("Lane-P torch = REFERENCE + bridge, forge = PUBLIC production trainer").
- Model: CLMConvMoE (conv trunk, MoE experts, SLW gated-write forward-slot the H_9200 E1 lever), d=3784, L=4, E0=2→Emax=3 (MITOSIS expert-split mid-run at step split_step), SAVANT golden-zone inhibition (dropout/weight-decay anneal), a JamoHead aux, several trunk-objective aux losses (predictive_info, constructive_bind, composed_nce, infonce, dict, tlora). Corpus = 4-cell (Korean/English × general/SNS) via a ByteCell sampler with proportional/roundrobin sampling; held-out val tail per cell.
- Serializes to `.clm` v0.3 (+ an SLW trailer). The TERMINAL verdict is engine-native re-measurement of the `.clm` via `anima evaluate --py`, NOT the torch CE.

# Why DDP now
A single 303M run is GPU-bound at ~3.3 s/step on an A40 → ~13h for 14000 steps. Faster GPU helps but data-parallel across N GPUs would cut wall-time ~linearly (the whole point: `a_wall_first` = wall-time first, more/bigger parallel GPUs). We want `anima train --py ... --gpus 0,1,2,3` (or torchrun) to shard the batch across GPUs and finish ~N× faster, byte-faithful to the single-GPU recipe's LEARNING (not necessarily bit-identical — held-out DESCENT is the gate, per `a_clm_gen_pipeline`).

# The HARD parts you must design carefully (these are why it's delegated)
Address EACH with a concrete mechanism:

1. **DDP vs the mid-run MITOSIS expert-split.** At `split_step` the model grows E0→Emax (new expert weights materialize, optimizer param groups change). Under DDP every rank must grow IDENTICALLY and stay in sync (same new params, same init, same optimizer state shape) or allreduce desyncs/crashes. How? (deterministic split on all ranks · rebuild DDP wrapper + optimizer after the split · or pre-allocate Emax experts and gate · seed discipline so the new expert init matches across ranks). Pick one, justify, spec it.

2. **DDP vs the SAVANT dropout/weight-decay ANNEAL schedule.** The schedule is per-step; it must be identical on all ranks (it is, if it's a pure function of step). Confirm + note any per-rank RNG that would diverge dropout masks (fine for DDP — masks differ per sample — but flag if any schedule value is drawn from a generator).

3. **The corpus sampler + per-cell held-out.** Each rank must see a DIFFERENT shard of the batch (else it's N copies of the same gradient = no speedup) but the SAME held-out val set for the DESCENT gate, and the proportional/roundrobin cell weighting must stay correct globally. Design the sharded sampler (DistributedSampler-style over the ByteCell windows, seed-offset per rank) + how val is run (rank-0 only, or all-reduce the val CE).

4. **Aux trunk-objectives (infonce/constructive_bind/composed_nce/dict/tlora/jamo) under DDP.** Some allocate their own params (aux heads) — those must be DDP-wrapped too (find_unused_parameters if an aux head is inactive some steps). constructive_bind uses torch.fft (no bf16 kernel, auto-drops to fp32). Spec how aux params join the DDP graph + the find_unused_parameters decision.

5. **Effective batch size + LR.** DDP with per-rank batch B and N ranks = global batch N·B. Does the frozen recipe's LR need linear-scaling, or keep per-rank B and global = N·B (changing the recipe)? To keep the E1/frozen-bar comparison apples-to-apples, the SAFEST is: keep GLOBAL batch = the single-GPU batch (per-rank B = B_single/N), so the optimizer sees the identical batch/LR as the 1-GPU run. Spec this (and the edge case N not dividing B).

6. **Checkpoint / serialize under DDP.** Only rank-0 writes `.clm` + the SLW trailer (unwrap `model.module`). Barrier before/after. `--save-every` periodic ckpt same. Spec.

7. **Launch surface.** `torchrun --nproc_per_node=N cli/train.py ...` vs an in-process `mp.spawn`. Which fits `anima train --py --gpus 0,1,2,3` best (the CLI already has a `--gpus` concept in `anima sweep`)? Keep the SINGLE-GPU path byte-identical when N=1 (DDP off / world_size==1 short-circuit) so nothing regresses.

8. **hexa (`cli/train.hexa`) parity.** The hexa trainer is the byte-parity twin. Does forge/flame support multi-GPU at all today? If not, spec whether DDP is py-ONLY (label the hexa side `구현됨·미배선` + a wiring follow-on) or whether forge has a device-mesh primitive to mirror. Be honest — if hexa multi-GPU is a separate large lift, say so and scope it as a follow-on, don't force a fake parity.

# Deliver (implementation-ready spec, concise)
- A step-by-step change plan for `cli/train.py` (functions/blocks to add/modify, in order), each with the exact mechanism for the 8 hard parts above.
- The `--gpus`/torchrun launch contract + the N==1 no-regression short-circuit.
- The DESCENT-gate validation plan proving the DDP run learns equivalently to 1-GPU (same held-out val_CE trajectory within noise), since bit-identity is NOT required.
- A crisp verdict on the hexa-side parity (mirror now / follow-on / N/A) with justification.
- Call out any risk where DDP would SILENTLY corrupt the frozen-recipe comparison (the thing that would invalidate the E1 SLW verdict).

Output the spec only. Assume I (the implementer) know torch DDP mechanics — focus on the anima-SPECIFIC hazards (mitosis split, savant anneal, 4-cell held-out, aux heads, frozen-recipe integrity, hexa parity).
