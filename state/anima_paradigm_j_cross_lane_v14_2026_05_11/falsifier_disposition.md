# Falsifier disposition — BG-PARADIGM-J-CROSS-LANE-V14

## F-PARADIGM-J-1: structural — 3rd row needed?

**Claim**: "If paradigm-j fails V14 strict at both cap-only and cap+cotrain regimes, the §64 arch-aware 3-rule needs a 3rd row (NEW arch path)."

**Verdict**: **FIRED (structural)**

**Rationale**:
- V14 strict 5-tuple as defined by §55 (`phi_final + phi_per_cell_final` via `MitosisModelEngine` cellpool) is **NOT_MEASURABLE** on paradigm-j (clm-v4 LoRA, no mitosis cellpool, HIDDEN_DIM=768 vs v2 d_model=384).
- The "cap-only / cap+cotrain regime" envelope of the §64 rule only applies to substrates that have a mitosis cellpool (v2_d384) or an EngineAG iit_phi_unnorm_b16 path. paradigm-j has **neither**.
- Therefore paradigm-j cannot be tested **within** the existing rule's metric space. The rule, applied as-is, **routes paradigm-j to UNKNOWN** (else branch of §64).
- Structurally, the rule MUST extend with a 3rd row (clm_v4 / paradigm-j substrate-research lane) to classify paradigm-j non-trivially.
- The 3rd row would necessarily live in a different metric space: v5.2 4-gate adaptive (PIV-max ∧ DCR ∧ D-RAND ∧ random_self_PPR), not cellpool Φ.

**Evidence for FIRED**:
- Substrate audit: 0 v2-mitosis markers, 0 EngineAG markers, 352 clm-v4 LoRA keys → unambiguous NEW_arch classification
- Cross-lane: paradigm-j v5.2 EMERGE ACTIVE (own 14 PUBLIC PROMOTE) **while** V14_VIOLATED at PPR_v3 — confirms metric-conditional polarity already empirically

**Caveat**: "FIRED at the structural level, not the metric level." The original phrasing assumed paradigm-j could be tested in the v2 metric space and would FAIL there. The empirical reality is stronger: paradigm-j is **not in the rule's metric domain at all**, which is a more fundamental form of "FAIL the rule's scope".

## F-PARADIGM-J-2: paradigm-j ckpt unavailable?

**Claim**: "paradigm-j ckpt unavailable → NOT_MEASURED."

**Verdict**: **NOT_FIRED**

**Rationale**:
- Substrate FOUND at `/Users/ghost/.cache/anima/clm_v4_remapped/paradigm_j/`
- Files verified: `adapter_model.safetensors` (152MB, sha256 `6f1cf277fb76c923…` matches REMAP_SOURCE.json target), `adapter_config.json`, `jvae_heads.pt` (4.3MB), `jvae_heads_step50k_backup.pt`, `README.md`
- Substrate is fully available and read-only verifiable (raw#15)
- The NOT_MEASURED state arises from **metric incompatibility**, not ckpt absence

This is an important distinction: F-PARADIGM-J-2 protects against the literal "ckpt missing" failure mode (which would have terminated this BG per task spec "STOP. Report which paths you searched + the gap"). That failure did NOT occur. The ckpt is present and verifiable. What is missing is the §55 metric applicability, which is F-PARADIGM-J-1's domain.

## Combined disposition

- F-PARADIGM-J-1 FIRED (structural extension required)
- F-PARADIGM-J-2 NOT_FIRED (substrate present)
- Outcome: §64 arch-aware 3-rule EXTENDS to 3 rows (v2 / EngineAG / clm_v4), metric-conditional caveat added per row.
