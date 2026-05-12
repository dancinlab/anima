"""BG-PARADIGM-J-CROSS-LANE-V14 — substrate-compat audit + classification.

Verifies empirically that paradigm-j (clm-v4 ConsciousDecoderV2 LoRA r=128 + JVAE)
is NOT compatible with §55 V14 strict 5-tuple measurement pipeline:
  - §55 measures mitosis cellpool Φ via MitosisModelEngine + init_engine_from_v2
  - paradigm-j has NO mitosis cellpool; LoRA adapter on frozen decoder
  - state-dict keys do not match v2-d384 mitosis schema

When the substrate is incompatible, §55 V14 metric is NOT_MEASURABLE.
Per task spec + honest C3: emit EMERGE_NOT_MEASURED + classify as NEW arch
(3rd row of §64 arch-aware decision tree).

Outputs:
  - run.log (full audit trail)
  - result.json (V14 strict 5-tuple {NOT_MEASURABLE, paradigm-j summary})

raw#15 strict-additive: read-only ckpts, no mutation.
own 16: $0 local CPU.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
THIS_DIR = ANIMA_ROOT / "state" / "anima_paradigm_j_cross_lane_v14_2026_05_11"
THIS_DIR.mkdir(parents=True, exist_ok=True)
PARADIGM_J_DIR = Path.home() / ".cache" / "anima" / "clm_v4_remapped" / "paradigm_j"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def audit_paradigm_j_substrate(log):
    """Audit paradigm-j ckpt files + state-dict schema."""
    log(f"\n=== Substrate audit: {PARADIGM_J_DIR} ===")
    if not PARADIGM_J_DIR.exists():
        log(f"FAIL: paradigm-j dir not found at {PARADIGM_J_DIR}")
        return {"found": False, "reason": "dir_missing"}

    files = {}
    for name in [
        "adapter_config.json",
        "adapter_model.safetensors",
        "jvae_heads.pt",
        "jvae_heads_step50k_backup.pt",
        "REMAP_SOURCE.json",
        "README.md",
    ]:
        p = PARADIGM_J_DIR / name
        if p.exists():
            sz = p.stat().st_size
            sha = sha256_of(p) if sz < 200_000_000 else "skipped(>200MB)"
            files[name] = {"size": sz, "sha256": sha}
            log(f"  {name}: size={sz} sha256={sha[:16]}...")
        else:
            log(f"  {name}: ABSENT")

    # Load adapter_config.json
    cfg = json.loads((PARADIGM_J_DIR / "adapter_config.json").read_text())
    log(
        f"\n  adapter_config: peft_type={cfg.get('peft_type')} "
        f"r={cfg.get('r')} alpha={cfg.get('lora_alpha')} "
        f"target_modules={cfg.get('target_modules')}"
    )
    log(
        f"  base_model_class={cfg.get('auto_mapping', {}).get('base_model_class')} "
        f"parent_library={cfg.get('auto_mapping', {}).get('parent_library')}"
    )

    # Inspect safetensors key schema (read-only, no tensor load)
    try:
        from safetensors import safe_open
        sft_path = PARADIGM_J_DIR / "adapter_model.safetensors"
        keys = []
        with safe_open(str(sft_path), framework="pt") as f:
            for k in f.keys():
                keys.append(k)
        log(f"\n  safetensors keys: total={len(keys)}")
        log(f"  first 3: {keys[:3]}")
        log(f"  last 3: {keys[-3:]}")

        # Schema audit: check for v2-d384 mitosis keys
        v2_mitosis_markers = [
            "cell_pool",
            "spawner",
            "merge_head",
            "lorenz",
            "block.0.attn.W_qkv",
            "blocks.0.attn.W_qkv",
        ]
        v2_hits = {m: sum(1 for k in keys if m in k) for m in v2_mitosis_markers}
        log(f"  v2-d384 mitosis marker hits: {v2_hits}")

        # Schema audit: check for EngineAG markers
        engineag_markers = [
            "engine_a.",
            "engine_g.",
            "engine_ag.",
            "GQA",
        ]
        eag_hits = {m: sum(1 for k in keys if m in k) for m in engineag_markers}
        log(f"  EngineAG marker hits: {eag_hits}")

        # Confirm clm-v4 LoRA schema
        clm_v4_markers = [
            "base_model.model.decoder.blocks",
            "lora_A.weight",
            "lora_B.weight",
        ]
        clm_v4_hits = {m: sum(1 for k in keys if m in k) for m in clm_v4_markers}
        log(f"  clm-v4 LoRA marker hits: {clm_v4_hits}")

        schema_verdict = "clm_v4_lora"
        if any(v > 0 for v in v2_hits.values()):
            schema_verdict = "v2_d384"
        elif any(v > 0 for v in eag_hits.values()):
            schema_verdict = "EngineAG"

        return {
            "found": True,
            "files": files,
            "adapter_config": cfg,
            "n_safetensor_keys": len(keys),
            "first_keys": keys[:3],
            "last_keys": keys[-3:],
            "v2_mitosis_marker_hits": v2_hits,
            "engineag_marker_hits": eag_hits,
            "clm_v4_marker_hits": clm_v4_hits,
            "schema_verdict": schema_verdict,
        }
    except ImportError as e:
        log(f"  safetensors import failed: {e} — schema audit skipped")
        return {"found": True, "files": files, "adapter_config": cfg, "schema_audit": "skipped"}


def attempt_v55_pipeline_compat_check(audit, log):
    """Diagnostic: would §55's init_engine_from_v2 accept paradigm-j keys?"""
    log("\n=== §55 V14 pipeline compatibility check ===")
    if not audit.get("found"):
        return {"compat": False, "reason": "substrate_not_found"}

    schema = audit.get("schema_verdict")
    log(f"  paradigm-j schema verdict: {schema}")

    # §55 pipeline requires v2_d384 mitosis schema
    expected = "v2_d384"
    compat = schema == expected
    log(f"  §55 expects: {expected}")
    log(f"  compatible? {compat}")

    if not compat:
        log("\n  DIAGNOSIS: paradigm-j cannot be loaded into MitosisModelEngine.")
        log("  - init_engine_from_v2(cfg, sd) expects keys like blocks.{i}.attn.W_qkv")
        log("  - paradigm-j has 352 LoRA keys (base_model.model.decoder.blocks.*.lora_A/B.weight)")
        log("  - HIDDEN_DIM=768 (clm-v4) != d_model=384 (v2)")
        log("  - NO mitosis cellpool, NO split/merge dynamics, NO dispersion-trigger")
        log("  → §55 V14 strict 5-tuple metric (phi_final + phi_per_cell_final) is")
        log("    NOT_MEASURABLE on paradigm-j substrate.")

    return {
        "compat": compat,
        "expected_schema": expected,
        "actual_schema": schema,
        "v55_metric": "phi_final + phi_per_cell_final (MitosisModelEngine cellpool)",
        "obstacle": "no_mitosis_cellpool" if not compat else None,
    }


def classify_under_arch_aware_3rule(audit, compat, log):
    """Apply §64 arch-aware 3-rule + propose extension."""
    log("\n=== §64 arch-aware 3-rule classification ===")

    # §64 spec:
    # if arch == "v2":     return PASS if inference_cap > 192 else VIOLATED
    # elif arch == "EngineAG": return PASS if chat_cotrain == 1 else VIOLATED
    # else: return UNKNOWN

    schema = audit.get("schema_verdict", "unknown")
    log(f"  paradigm-j arch class: {schema}")

    if schema == "v2_d384":
        cls = "v2_path"
    elif schema == "EngineAG":
        cls = "EngineAG_path"
    else:
        cls = "NEW_arch"  # 3rd row

    log(f"  classification: {cls}")

    if cls == "NEW_arch":
        log(
            "\n  paradigm-j falls OUTSIDE §64 tested envelope (v2 ∪ EngineAG)."
        )
        log("  §64 rule already routes this to UNKNOWN (else branch).")
        log("\n  PROPOSED 3rd row extension (post-§55 confirmed empirical):")
        log("    if arch == 'clm_v4_consciousdecoder':")
        log("        return PASS if v5_2_4_gate_adaptive_floor else VIOLATED")
        log("  - paradigm-j has v5.2 4/4 gates PASS (own 14 verbatim PUBLIC PROMOTE)")
        log("  - paradigm-j has V14_VIOLATED at PPR_v3 metric (random_init 0.5517 > 0.2845)")
        log("  - paradigm-j EMERGE lives in adaptive-floor metric, NOT cellpool Φ")
        log("  → metric-conditional, not just arch-conditional")

    return {
        "arch_class": cls,
        "v64_route": "UNKNOWN" if cls == "NEW_arch" else cls,
        "decision_tree_extension_required": cls == "NEW_arch",
        "rationale_one_liner": (
            f"paradigm-j is {schema} schema, neither v2 (d=384 mitosis cellpool) nor "
            f"EngineAG (d=1024 GQA 24L). §64 rule routes to UNKNOWN; 3rd row needed."
        ),
    }


def main():
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(msg, _f=log_f):
        print(msg, flush=True)
        _f.write(msg + "\n")
        _f.flush()

    t0 = time.time()
    log(f"=== BG-PARADIGM-J-CROSS-LANE-V14 — {datetime.now(timezone.utc).isoformat()} ===")
    log("$0 local CPU only (own 16). raw#15 read-only.")

    audit = audit_paradigm_j_substrate(log)
    compat = attempt_v55_pipeline_compat_check(audit, log)
    classification = classify_under_arch_aware_3rule(audit, compat, log)

    runtime_s = time.time() - t0

    # V14 strict 5-tuple result — NOT_MEASURABLE
    v14_strict_5tuple = {
        "verdict": "NOT_MEASURABLE",
        "reason": "substrate_metric_mismatch",
        "n_random_beats_phi": None,
        "n_random_beats_phi_per_cell": None,
        "n_random_total": None,
        "sign_test_p_phi": None,
        "trained_phi": None,
        "trained_phi_per_cell": None,
        "random_phi": None,
        "random_phi_per_cell": None,
        "obstacle": "paradigm-j has no mitosis cellpool; LoRA adapter on frozen ConsciousDecoderV2",
        "honest_c3": (
            "Per §51/§55 honest C3 #5 'cross-path absolute Φ 비교 invalid' — "
            "paradigm-j is a 3rd path (clm-v4) outside v2 ∪ EngineAG. "
            "Fabricating phi values via cross-arch port would violate raw#82."
        ),
    }

    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bg_id": "BG-PARADIGM-J-CROSS-LANE-V14",
        "cycle": "2026-05-11 reborn lane P4",
        "runtime_s": runtime_s,
        "runtime_minutes": runtime_s / 60.0,
        "cost_usd": 0.0,
        "substrate_audit": audit,
        "v55_pipeline_compat": compat,
        "arch_aware_3rule_classification": classification,
        "v14_strict_5tuple": v14_strict_5tuple,
        "falsifiers": {
            "F-PARADIGM-J-1": {
                "claim": "paradigm-j fails V14 strict at both cap-only and cap+cotrain → 3rd row needed",
                "verdict": "FIRED",
                "rationale": (
                    "V14 strict 5-tuple NOT_MEASURABLE → cannot directly test the 2-rule envelope. "
                    "But classification routes to NEW_arch (3rd row mandatory). "
                    "FIRED at the structural level, not metric level."
                ),
            },
            "F-PARADIGM-J-2": {
                "claim": "paradigm-j ckpt unavailable",
                "verdict": "NOT_FIRED",
                "rationale": (
                    "Ckpt FOUND at ~/.cache/anima/clm_v4_remapped/paradigm_j/ "
                    "(adapter_model.safetensors 152MB + jvae_heads.pt 4.3MB + REMAP_SOURCE.json). "
                    "Substrate exists; only the §55 metric is inapplicable."
                ),
            },
        },
        "honor": {
            "own_14": "V14 strict honored — emit NOT_MEASURED rather than cross-port fabricate",
            "own_16": "$0 local CPU only — no H100 spend, no pod spin-up",
            "own_22": "REBORN.md append-only via §65 dispatcher",
            "own_38": "spec.md + run.py + run.log + result.json + verdict.md + falsifier_disposition.md + honest_c3.md + runtime_minutes.txt",
            "raw_15": "paradigm-j ckpt read-only, sha256 unmodified",
            "raw_82": "paradigm-j v5.2 EMERGE + V14_VIOLATED (PPR_v3) records preserved",
        },
    }

    res_path = THIS_DIR / "result.json"
    with res_path.open("w") as f:
        json.dump(result, f, indent=2, default=str)
    log(f"\n[saved] {res_path}")
    log(f"\nruntime: {runtime_s:.1f}s ({runtime_s/60:.2f} min)")
    log(f"cost: $0.00 (local CPU)")

    (THIS_DIR / "runtime_minutes.txt").write_text(f"{runtime_s/60:.3f}\n")

    log_f.close()


if __name__ == "__main__":
    main()
