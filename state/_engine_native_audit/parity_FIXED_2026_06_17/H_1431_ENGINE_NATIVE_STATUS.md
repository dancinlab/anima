# H_1431 engine-native re-measure — STATUS (2026-06-17)

## Outcome: trust-gate PASS; full 5-bar INFEASIBLE at current forward speed

### Trust-gate (engine forward byte-faithful) = PASS
- Rebuilt the reboot-wiped env on the DURABLE summer checkout `~/core/anima` (not /tmp).
- Hoisted all 4 i64-subscript sites in `CORE/bytegpt_decode.hexa` decode loops
  (bytegpt_decode_argmax / _topk_sampled / grounded / grounded_abstain).
- Re-serialized `chat_full.bin` (1.21 GB) from `h1129c_chat.pt`; torch golden argmax=32,
  greedy=" as the ", top5=[32,44,10,63,46].
- Engine-native forward on the hoisted decode = argmax 32 on BOTH paths:
  - `bytegpt_forward_last_ranged` → RANGED_ARGMAX 32
  - `bg_load` + `bg_forward_last_W` (resident-Map) → MAPW_ARGMAX 32
  ⇒ the engine forward is byte-faithful to torch. The parity FIX holds on a fresh env.

### Speed wall (the blocker for the H_1431 sweep)
- Single forward (T=15, ONE next-token logits, dispatch-interpreted hexa runtime) = **102 s**
  (measured, warm cache). Forward = pure-hexa nested-loop matmul, 24 layers × (3d²+d²+2·4d²)
  scalar farr_get multiply-adds at d=1024.
- H_1431 (FROZEN params, gauge_lib._decode VERBATIM): MAX_NEW=110, top_k=40, temp=0.7,
  SEEDS=[7,4302,4303], SUBJECTS=[consciousness,tension,memory,silence,dreaming].
  Generation cost = 110 forwards/fragment × 2 fragments × 5 subjects × 3 seeds = ~3,300
  forwards, × 3 arms (COMPOSE / SHUFFLE_BIND / ABLATE). At ≥102 s/forward (rising with
  context length) = **≥90–280 hours**. INFEASIBLE synchronously.
- The fast native-asm path (aprime_cc) CANNOT compile this model — the forward uses `farr_*`
  intrinsics unsupported by the native backend (Lane A r2 finding). So there is no fast
  engine path available today.

### Engine-native sampling note (a_engine_native_learning)
torch `gauge_lib._decode` samples via `torch.multinomial` with a torch `Generator(seed_rng)` —
NOT reproducible in hexa. The engine path (`bytegpt_decode_topk_sampled`) uses the engine's
OWN xorshift32 seeded top-k sampler (`_g6_topk_sample`). So the engine re-measure is a genuine
INDEPENDENT measurement on the faithful forward, not a byte-replica of the torch samples — the
correct engine-native posture, but it means parity is at the FORWARD/argmax level (verified
32==32), not the sampled-token level.

### Pilot (smallest feasible real engine-native generation)
Attempted: 1 subject ("consciousness"), relation seed, gen=20, top_k=40, temp=0.7, seed_rng=7
via `bytegpt_decode_topk_sampled` on the resident-Map path. [RESULT APPENDED BELOW WHEN DONE.]
This is a single fragment, NOT the frozen 5-bar — a directional engine sanity point only.

## Verdict vs torch DIRECTIONAL
The torch-side DIRECTIONAL stands UN-RE-VERIFIED on the engine at full scale (infeasible):
  COMPOSE FALS 0.3333 / SHUFFLE_BIND 0.0 / ABLATE 0.0 → 🧱 BIND-CAPACITY-BOUND (torch).
This is an HONEST infeasibility, not a confirmation or an overturn.

## The true unblock (recommended next lane)
Engine-native G6 re-measurement (H_1431 AND H_1432/1434) is gated on FORWARD SPEED, not on
correctness. The forward must drop from ~102 s to ≲2 s. Levers:
  1. KV-cache the attention so each new decode token is a 1-row forward, not a full-T re-compute.
  2. Route the farr matmuls through a runtime BLAS (forge / hxblas) instead of interpreted
     scalar loops.
Either makes the full frozen 5-bar feasible (~minutes) and unblocks H_1432/1434 behind it.
Depletion for that lane: single-token forward < ~2 s; then re-run this frozen 5-bar.

H_1432 (negation slot scaffold) and H_1434 (two-pass bind) are the NEXT rounds behind the same
speed gate.
