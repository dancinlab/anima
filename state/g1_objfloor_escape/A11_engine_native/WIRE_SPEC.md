# A11 TPR-slot engine-native WIRE spec (UNAPPLIED — apply in lockstep with train)

Status: **DESIGN ONLY, not applied to live core/.** `a_verified_must_wire` forbids dead
code — this lands ONLY together with a trained TPR+contrastive `.clm` so the forward has
real weights to load. Insertion points below are exact (verified against the live files
this session). Path = `a_core_engine_map`: extend the SINGLE generator-L3 `.clm` forward,
no 2nd path.

## 1. Trainer objective — `archive/train/clm/train/train_lane_p.py`
Replace the CE next-byte loss with **contrastive-replace InfoNCE** (echo-A / echo-B /
wrong-D negatives), as prototyped in `a11_natural.py::train_eval`. CE is deleted (not
added-to — additive `CE+γ·L_recomb` = H_9120, already FALSIFIED). The trunk is trained
end-to-end by InfoNCE only. Keep the golden-zone inhibition schedule (`a_savant_train`).

## 2. TPR forward-slot — `core/clm_decode.hexa` `_clmd_fwd_logits` (and `_clmd_fwd_logits_sc`)
The readout today is a single linear projection (L540):
```
_clmd_conv1d(yn, roW, roB, out_logits, T, d, V, 1, 1)   // out = roW · yn
```
Insert a **multiplicative role-filler binding** BEFORE the readout (NOT additive concat):
maintain R fixed orthonormal role vectors `roles[R,d]` (R=2, `torch.eye`-analog, stored in
CLMX). For each position t, bind the post-MoE hidden `yn[t]` into role-slots
`c_r = yn[t] ⊙ roles[r]` (Hadamard = the tensor-product slot at R=2 orthonormal), then the
readout reads each slot with its own signature projection `S_r`:
`out[t] = Σ_r S_r · (yn[t] ⊙ roles[r])`. This is the `A11Model.energy` TPR branch made
autoregressive. New ops: `_clmd_role_bind(yn, roles, r, cbuf, T, d)` (elementwise) +
per-slot `_clmd_conv1d(cbuf, S_rW, S_rB, …)` accumulated. Must be **byte-identical** to the
torch reference (`a11_natural.py`) on a fixed ckpt — add a parity smoke to
`state/g1_objfloor_escape/A11_engine_native/`.

## 3. Loader + serializer — `_clmd_load` / `clm_serialize`
- `_clmd_load` (L229): parse the new `roles[R,d]` + `S_r[R][V,d]` tensors from an extended
  CLMX trailer (bump v0.2→v0.3, keep the `CLMX` magic + a new ext-block tag so old golden
  `.clm` still decode via the non-TPR path when the tag is absent).
- `clm_serialize` (torch→.clm writer): emit `roles` (frozen orthonormal) + the R signature
  projections. Verify with `verify_clm_v2.py` (byte-identical re-serialize).

## 4. Score — `anima evaluate --py`
Port `cli/evaluate.py` (absent from this branch; commit 67368a775 on main / copies under
`state/g1_growwindow_remeasure/cli/evaluate.py`) into the train pod, load the TPR `.clm`,
run mouth-generation G1: `A.novel≥2 ∧ >max_single ∧ SCRAMBLE≤1`, 5 seeds. **≥4/5 →
PREDICTIVE-ESCAPED (H_9120 FLIP→GREEN); <4/5 → FALSIFIED-CEILING (H_9120 confident-terminal).**

## 5. ARCHITECTURE.json lockstep
On WIRE landing, add the TPR binding-slot to the `core/` clm_decode node (§readout · role
ops · CLMX v0.3 ext-block) 1:1 with the live hexa (`a_verified_must_wire` box 4).

## Blocking prereqs (this session's infra reality)
GPU pod with torch (aiden down · summer torch-less) for the 303M natural-corpus InfoNCE
train + serialize + `--py` score; ckpt PULL before teardown (`a_fire_recover_complete`).
