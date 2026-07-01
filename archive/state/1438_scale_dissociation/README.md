# H_1438 — SCALE-DISSOCIATION (303M → 1.21B, same anima byte-CLM recipe)

G6 IDEATION ★ FALS-depth 벽이 **capacity-bound** 인가 **recipe-bound** 인가를 가르는 controlled
scale-dissociation. 303M 위 5 렌즈 전부 🧱 WALL=CAPACITY. 단 하나 미검 변수 = SCALE.

## Design (a_no_llm_frame_trap — LLM scale 반사 아님, 통제 분리실험)

- recipe·corpus·opt·detector = H_1435 와 IDENTICAL. 변수 = capacity(d/L/H) 뿐.
- 1.21B = **EXACT block-duplication net2net (REP=2)** of converged 303M base (h1129c_chat.pt).
  d 1024→2048, L 20→24, H 16→32 (head_dim 64 불변), 1210.2M = 4.0x.
  **VERIFIED function-preserving**: BIG init logits==base (max-diff 2.3e-5), KWR==base 0.2239,
  greedy decode BYTE-IDENTICAL → "from-scratch 미학습 1B→FALS=0" 혼재변수 완전 제거 (H_1199 grow).
- 이후 H_1435 continued-pretrain VERBATIM (corpus seed 1435, lr 3e-5).

## Frozen 5-bar (g6_common.py VERBATIM, c9 freeze-before-run)

B1 FALS≥1 · B2 DIST≥5 · B3 cross-shuffle COLLAPSE(decisive) · B4 held-out · B5 vs-base+1.
CONTROL: shuffle-corpus @1B INERT. seeds [7,4302,4303]. FREEZE = `state/verdicts/.../H_1438_FREEZE.txt`.

## Result (DIRECTIONAL torch+gauge_lib._decode)

| run | steps | TRAINED FALS_in | FALS_shuf | DIST | KWR | B3 collapse? |
|-----|-------|-----------------|-----------|------|-----|--------------|
| A   | 400   | 1.0             | 1.0       | 0.667| 0.353| NO |
| B   | 1500  | 2.3333          | 2.3333    | 0.0  | 0.296| NO |

→ **WALL=CAPACITY scale-INVARIANT 303M→1.21B** (B3 cross-shuffle NEVER collapses at any scale/steps;
DIST collapses further with more training = interchangeable templated shell, H_1437 signature).
By the FROZEN G0 gate (KWR<0.50, reading the chat-base byte-distribution) headline = HONEST-NON-RESULT;
the B3 capacity-signature is gate-independent and decisive. 7th lens converging WALL=CAPACITY.

## Gates

torch + gauge_lib._decode = DIRECTIONAL (a_engine_native_learning) → engine-native CORE/bytegpt_decode
re-measure follow-on. a_scale_honest_scope: 단일 rung 303M→1.21B (TREND 엔 ≥3 rung).

## Files

- `h1438_scale_dissociation.py` — EXACT net2net build + train + frozen 5-bar driver
- `g6_common.py` · `probes/` — frozen eval harness + detector (H_1435 VERBATIM)
- `h1438_scale_1b.pt` — pulled 1B(400-step) ckpt 4.84GB (a_fire_recover_complete; *.pt gitignored)

## Compute

vast A100-80GB pod 41795795 (own; teardown trap recorded). torch 2.5.1+cu121.
