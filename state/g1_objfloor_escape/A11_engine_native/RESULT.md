# A11 engine-native step — natural-corpus DIRECTIONAL + engine-native terminal (blocked)

**Task:** flip (or cement) H_9120 objective-floor terminal by taking A11 (TPR-slot ×
contrastive-replace) from torch-DIRECTIONAL (H_9121, synthetic 5/5) to engine-native.
Chain = WIRE (core/clm_decode.hexa TPR slot + serializer + trainer InfoNCE) → TRAIN
(303M natural 4-cell) → SCORE (`anima evaluate --py` mouth-generation G1, ≥4/5).

## What was measured this session

### (A) Natural-corpus transfer, DIRECTIONAL — the `a_toy_scale_recheck` question
`a11_scaled.py` (H_9121) hit 5/5 with **SYNTHETIC** fillers = maximally-separated random
4-byte strings. RESULT.md flagged the honest risk: the escape could be a **clean-corpus
artifact** (roles=orthonormal-by-construction × maximally-separated fillers). `a11_natural.py`
isolates that ONE variable: identical A11Model / InfoNCE objective / real deep conv byte
trunk (CLMConvMoE E2/L1 d=768, 7.30M) / frozen bar / 5 seeds — only the fillers become
**REAL words** drawn from the production 4-cell natural corpus (ko/en × general/sns,
56 353-word vocab: 자유마저·진리와·river·휴머니즘·Czteroletni·…, overlapping bytes, variable length).

| seed | ADD margin | ADD | TPR margin | TPR reach_novel | TPR scr | TPR |
|------|-----------|-----|-----------|-----------------|---------|-----|
| 7    | −0.308 | floor | +34.17 | 1.00 | 0.01 | **HIT** |
| 11   | −0.249 | floor | +32.56 | 1.00 | 0.00 | **HIT** |
| 23   | −0.326 | floor | +35.67 | 1.00 | 0.00 | **HIT** |
| 42   | −0.289 | floor | +28.61 | 1.00 | 0.02 | **HIT** |
| 101  | −0.279 | floor | +35.96 | 1.00 | 0.01 | **HIT** |

**TALLY: TPR (A11) 5/5 HIT · ADD (E1 ctrl) 0/5 floor** · d=768 · 7.30M · $0 (mini CPU, light toy).
Margin drops +99 (synthetic) → +28…+36 (real overlapping words) but stays strongly positive,
reach_novel = 1.00, scramble ≤ 0.02. **VERDICT: NATURAL-TRANSFER-SURVIVES.**
JSON `a11_natural.json`; raw log `a11_natural.log`; harness `a11_natural.py`.

**Interpretation (honest, c9):** the synthetic reachability is **NOT** a clean-corpus /
maximally-separated-filler artifact — it survives real overlapping ko/en words. This
**removes** the specific `a_toy_scale_recheck` failure mode RESULT.md worried about and
keeps A11 the live escape candidate. It does **NOT** flip H_9120 (below).

### (B) Engine-native terminal — NOT reached (INFRA + the readout gap)
Per `a_engine_native_learning` HARD-GATE, (A) is **torch → DIRECTIONAL**, terminal-ineligible.
Two independent reasons the terminal is not flipped:

1. **Readout gap (scientific).** The A11 readout is a **signature-decode energy over a
   shortlist** with **roles = orthonormal identity by construction** — NOT autoregressive
   **mouth generation**. Production G1 (`anima evaluate --py`: A.novel≥2 ∧ >max_single ∧
   SCRAMBLE≤1) is measured on the byte mouth's *generated* output. A11's HIT shows the TPR
   binding *mechanism* composes on held-out pairs under a clean readout; it does **not** yet
   show a natural-corpus byte **mouth** recombines. That is exactly what only the wired +
   trained + `--py`-scored .clm can answer.
2. **Infra (operational).** aiden (the torch host that ran a11_scaled) = **unreachable**
   (ssh timeout); summer = reachable but **no torch** in any env (base miniforge + 5 venvs
   checked, hexa-native host); mini = torch-2.12 present but heavy 303M forbidden
   (`heavy-anima-eval-pool-not-mini`); `cli/evaluate.py` (the `--py` scorer) is **absent
   from this branch** (lives only as `state/g1_growwindow_remeasure/cli/evaluate.py` copies).
   A full 303M natural-corpus TPR+contrastive train + serialize + mouth-generation G1 score
   is the documented multi-pod effort that repeatedly dies on infra (h9107 RSS blowup,
   h1590 BLOCKED-INFRA, aiden/summer reboot loops) and is not completable in one subagent
   session without an explicit long-lived GPU pod babysit.

## WIRE — delivered as spec, NOT applied to live core/
`a_verified_must_wire` forbids **dead code**: wiring a TPR forward-slot into
`core/clm_decode.hexa` + serializer **without** a trained TPR ckpt to load = a phantom path
(and the task holds commit/frozen untouched, state-only). The concrete insertion points
(forward readout at `_clmd_fwd_logits` L540 `roW @ yn`; loader `_clmd_load`; v0.2 CLMX
trailer; trainer `train_lane_p.py` CE→InfoNCE) are specified in **`WIRE_SPEC.md`** as the
registered follow-on, to be applied in lockstep with the train so it never lands dead.

## Verdict
**A11 = DIRECTIONAL (natural-transfer-survives).** H_9120 objective-floor terminal
**NOT flipped** and **NOT cemented** — the natural DIRECTIONAL result strengthens the escape
candidate (kills the synthetic-artifact concern) but cannot be terminal (torch, not
engine-native mouth generation). Terminal decider = engine-native `--py` on a trained
TPR+contrastive .clm = INFRA-BLOCKED follow-on. **Neither PREDICTIVE-ESCAPED (needs
engine-native ≥4/5) nor FALSIFIED-CEILING (natural transfer did NOT fail) is earned.**

- **wired:** none live (WIRE_SPEC.md, unapplied — dead-code guard)
- **trained:** none (no 303M ckpt; 7.30M toy not serialized). host = mini CPU · cost = $0
- **g1_result:** natural TPR 5/5 HIT (margin +28…+36, reach 1.0, scr ≤0.02) · torch DIRECTIONAL · not `--py`
- **terminal_flip:** NO — engine-native mouth-generation G1 not run (infra + readout gap)
- **cost:** $0
