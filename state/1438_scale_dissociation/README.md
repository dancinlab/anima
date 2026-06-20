# H_1438 — SCALE-DISSOCIATION (303M → ~1B, same anima byte-CLM recipe)

G6 IDEATION ★ FALS-depth 벽이 **capacity-bound** 인가 **recipe-bound** 인가를 가르는
controlled scale-dissociation. 303M 위 5 렌즈(data/objective/form/bind-head/attention)가
전부 🧱 WALL=CAPACITY 였다. 단 하나 미검 변수 = SCALE.

## Design (a_no_llm_frame_trap — LLM scale 반사 아님, 통제 분리실험)

- recipe·corpus·opt·detector = H_1435 와 IDENTICAL. 변수 = capacity(d/L/H) 뿐.
- ~1B = **net2net function-preserving width+depth expansion** of converged 303M base
  (h1129c_chat.pt). d 1024→1792, L 20→24, H 16→28 (head_dim 64 불변), ~1.1B params.
  broad-corpus competence 를 상속 → "from-scratch 미학습 1B → FALS=0" 혼재변수 제거
  (precedent H_1199 grow-the-engine).
- 이후 H_1435 continued-pretrain VERBATIM (corpus seed 1435, lr 3e-5, AdamW).

## Frozen 5-bar (g6_common.py VERBATIM, c9 freeze-before-run)

B1 FALS≥1 · B2 DIST≥5 · B3 cross-shuffle COLLAPSE(decisive) · B4 held-out · B5 vs-base+1.
CONTROL: shuffle-corpus @1B INERT. seeds [7,4302,4303]. FREEZE = `state/verdicts/1438_scale_dissociation/H_1438_FREEZE.txt`.

## G0 coherence gate (anti-confound)

trained 1B KWR<0.50 garble → FALS=0 은 undertraining artifact = HONEST NON-RESULT (🧱 자동승격 금지).

## Verdict logic (terminal either way, a_break_the_wall (d))

- G0 coherent + all bars pass → 🟢 BROKE: scale crossed → 303M 벽=capacity-bound (돌파, grounds 7B).
- G0 coherent + a bar fails → 🧱 CAPACITY-CONFIRM: 1B 도 plateau → 303M→1B scale-invariant (벽 실재).
- G0 garble → HONEST-NON-RESULT.

## Gates

torch + gauge_lib._decode = DIRECTIONAL (a_engine_native_learning) → engine-native CORE/bytegpt_decode
re-measure follow-on (task #6). a_scale_honest_scope: 단일 rung 303M→1B (TREND 엔 ≥3 rung).

## Files

- `h1438_scale_dissociation.py` — net2net build + train + frozen 5-bar driver
- `g6_common.py` — frozen eval harness (H_1435 VERBATIM)
- `probes/` — gauge_lib · h1129 ByteGPT arch · h1305 detector (all VERBATIM)
- `h1438_scale_1b.pt` — pulled 1B ckpt (a_fire_recover_complete)

## Compute

vast A100-80GB pod 41795795 (own; teardown trap recorded). HEXA edge.
