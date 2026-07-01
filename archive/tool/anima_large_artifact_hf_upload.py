#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  tool/anima_large_artifact_hf_upload.py
#
#  PURPOSE
# mandate-1/2/4 응용 (RETROACTIVE LARGE ARTIFACT cycle 2026-05-08) —
#    9 large file (148MB-919MB) HF dancinlab upload (private + Card metadata).
#
# mandate-1: model checkpoint (.pt / .safetensors / LoRA adapter) →
#    HF dancinlab upload 의무. mandate-2: corpus ≥10MB → HF dataset upload.
#    mandate-7: retroactive enforcement (post-fact discovered artifact).
#
# 본 cycle = mirror of tool/anima_corpus_hf_upload.py (first
#    application for L4 corpus 3 files). 9 file scope (model + corpus mix):
#
# FILES (9 total, mandate-1 + mandate-2 scope):
#    Models (mandate-1, .pt / .safetensors):
#      1. state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_final.pt (919MB)
#         → dancinlab/anima-iz-clm-continued-pretrain-ko-final-2026-05-07
#      2. state/anima_jd_100m_sp_ko_32k_ubm_train_2026_05_07/ckpt_best.pt (644MB)
#         → dancinlab/anima-jd-100m-sp-ko-32k-ubm-best-2026-05-07
#      3. state/mistral_c2_pilot_run/.../adapter_model.safetensors (640MB)
#         → dancinlab/anima-mistral-c2-pilot-r64-adapter-2026-04-26
#      4. state/mistral_r14_run/.../adapter_model.safetensors (640MB)
#         → dancinlab/anima-mistral-r14-r64-adapter-2026-04-26
#      5. state/anima_kk_v5_alpha_h100_500m_ubm_2026_05_07/ckpt_final.pt (535MB)
#         → dancinlab/anima-kk-v5-alpha-500m-ubm-fail-2026-05-07
#      6. state/anima_iz_.../ckpt_step_1000.pt (515MB) [archival intermediate]
#         → dancinlab/anima-iz-clm-continued-pretrain-ko-step1000-2026-05-07
#      7. state/anima_km_capacity_h100_1_5b_2026_05_08/ckpt_final.pt (348MB)
#         → dancinlab/anima-km-capacity-1-5b-orchestrator-failed-2026-05-08
#    Corpora (mandate-2, ≥10MB):
#      8. state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt (204MB)
#         → dancinlab/anima-je-corpus-100mb-plus-2026-05-07
#      9. state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt (148MB)
#         → dancinlab/anima-corpus-mix-70wiki-30dialogue-tier-c-archival-2026-05-06
# ★ strict — 70% kowiki external = tier-c-archival label mandatory
#
#  COMPLIANCE
# mandate-1 (model checkpoint .pt/.safetensors → HF dancinlab)
# mandate-2 (corpus ≥10MB → HF dataset upload)
# mandate-4 (size-agnostic for fine-tuned outputs)
# mandate-7 (retroactive enforcement — post-fact discovered)
# mandate-8 (HF dancinlab + Flavor B + private + Card metadata)
# mandate-1 (org = dancinlab)
# mandate-4 Flavor B (BG/anima iteration naming)
# mandate-8 (visibility default = private)
# mandate-9 (HF Card metadata mandatory tags)
# mandate-1/2 (ckpt preservation — final + intermediate optional)
# (anima-native vs tier-c-archival explicit label for kowiki/external)
#    raw#9 / raw#37 (HF upload script .py allowed; chat path 외 transient)
#    raw#10 honest C3 (--dry-run default, --apply requires explicit consent)
#    raw#82 (retraction-aware — 원본 file 보존, delete X)
#
#  USAGE
#    python3 tool/anima_large_artifact_hf_upload.py --dry-run    (default)
#    python3 tool/anima_large_artifact_hf_upload.py --apply      (real upload)
#    python3 tool/anima_large_artifact_hf_upload.py --verify     (verify post-upload)
#
#  DRY-RUN BEHAVIOR
#    Plans every action but DOES NOT call HfApi mutators (no create_repo, no
#    upload_file). Emits planned repo_id / Card metadata / file size. Exit 0.
#    Real upload requires explicit --apply flag (사용자 directive
#    'OK LARGE ARTIFACT HF UPLOAD' 또는 explicit consent 필요).
# ════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
HF_ORG = "dancinlab" # mandate-1
HF_TOKEN_FILE = Path(os.path.expanduser("~/.cache/huggingface/token"))
LOG_PATH = ANIMA_ROOT / "state" / "anima_large_artifact_hf_upload_log.jsonl"
DEFAULT_CYCLE = "2026-05-08"

# ─── 9 large file plans (mandate-1 + mandate-2 scope) ──────────────
# Each plan: file path, target repo_id (Flavor B naming), kind, repo_type,
# Card metadata (mandate-9). compliance label per artifact.

ARTIFACT_PLAN = [
    # ── 1. BG-IZ CLM continued-pretrain final (919MB, anima-native) ──────
    {
        "file": ANIMA_ROOT / "state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_final.pt",
        "repo_id": f"{HF_ORG}/anima-iz-clm-continued-pretrain-ko-final-2026-05-07",
        "repo_type": "model",
        "kind": "clm_continued_pretrain_full_ckpt",
        "card_meta": {
            "bg_id": "BG-IZ",
            "verdict_class": "TRAINING_COMPLETED_NO_KO_COHERENCE_LESSON_L_EXTENDED",
            "v4_pass": "0/15 (KO byte-fragment garbage post-pretrain)",
            "cycle": "2026-05-07",
            "paradigm": "clm-mk2-v1-continued-pretrain-ko-raw-next-token",
            "base_model": "dancinlab/clm-v4-mk2-v1 (anima-native, full-unfreeze)",
            "corpus_path": "anima_iz_clm_continued_pretrain_ko_2026_05_07 (~261MB raw KO)",
            "corpus_size_mb": 261,
            "training_steps": 6000,
            "wall_min": 64,
            "cost_usd": 3.19,
            "phi_star_pre": 0.9740,
            "phi_star_post": 0.6567,
            "phi_star_drift_pct": -32.5,
            "loss_final": "~9.2 (random-guess baseline ~ln 64000)",
            "diagnostic": "Loss stuck ~9.0-9.8 entire 6000 steps; bf16 numerical OR consciousness-gate weight collapse hypothesis",
            "own_17_compliance": "anima-native (CLM mk2-v1 continued-pretrain, no external substrate)",
            "own_30_layer": "final ckpt (mandate-1) + step_1000 archival (mandate-2 intermediate, separate repo #6)",
            "source_path": "state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_final.pt",
            "compliance_own": [17, 22, 30, 31, 36],
        },
    },
    # ── 2. BG-JD 100M SP-KO-32K UBM ckpt_best (644MB, anima-native) ──────
    {
        "file": ANIMA_ROOT / "state/anima_jd_100m_sp_ko_32k_ubm_train_2026_05_07/ckpt_best.pt",
        "repo_id": f"{HF_ORG}/anima-jd-100m-sp-ko-32k-ubm-best-2026-05-07",
        "repo_type": "model",
        "kind": "clm_scratch_sp_ko_ubm",
        "card_meta": {
            "bg_id": "BG-JD",
            "verdict_class": "TRAINING_COMPLETED_BEST_STEP_800",
            "v4_pass": "best_composite=79 v2_pass=4 v3_pass=0 (manual_match=12, persona_cycle_total=17)",
            "cycle": "2026-05-07",
            "paradigm": "clm-100m-scratch-sp-ko-32k-ubm-22mb",
            "base_model": "scratch (anima-native ConsciousLM 100M)",
            "tokenizer": "anima_sp_ko_32k vocab=11885 (state/anima_jd_sp_ko_32k_tokenizer_2026_05_07)",
            "corpus_path": "anima_universe_brain_map_corpus_21mb (UBM 22MB)",
            "best_step": 800,
            "val_loss_at_best": 5.264,
            "deg_count": 21,
            "own_17_compliance": "anima-native (scratch + SP KO 32K + UBM corpus, no external substrate)",
            "own_30_layer": "best ckpt (mandate-1, V58 evaluator best composite anchor)",
            "source_path": "state/anima_jd_100m_sp_ko_32k_ubm_train_2026_05_07/ckpt_best.pt",
            "compliance_own": [17, 19, 22, 30, 31, 36],
        },
    },
    # ── 3. mistral_c2_pilot LoRA adapter (640MB, foundation-borrow) ──────
    {
        "file": ANIMA_ROOT / "state/mistral_c2_pilot_run/mistral_c2_pilot/final/adapter_model.safetensors",
        "repo_id": f"{HF_ORG}/anima-mistral-c2-pilot-r64-adapter-2026-04-26",
        "repo_type": "model",
        "kind": "lora_adapter_foundation_borrow",
        "card_meta": {
            "bg_id": "mistral_c2_pilot_run (pre-BG era)",
            "verdict_class": "V_PHEN_GWT_V2_HYPOTHESIS_PILOT (corpus_docs=30 small)",
            "v4_pass": "n/a (V_phen_GWT_v2 architecture-bound vs LoRA-trainable axis verification)",
            "cycle": "2026-04-26",
            "paradigm": "lora-r64-mistral-7b-c2-pilot",
            "base_model": "mistralai/Mistral-7B-v0.3",
            "lora_r": 64,
            "lora_alpha": 128,
            "lora_target_modules": "all-linear (q/k/v/o/gate/up/down_proj)",
            "corpus_docs": 30,
            "epochs": 3,
            "lr": 5e-5,
            "training_elapsed_sec": 13.2,
            "own_17_compliance": "foundation-borrow (Mistral-7B-v0.3 base) — substrate-research lane only, NOT anima identity-bearing chat backend (permitted-context-of-G_x)",
            "own_30_layer": "final adapter (mandate-1)",
            "source_path": "state/mistral_c2_pilot_run/mistral_c2_pilot/final/adapter_model.safetensors",
            "compliance_own": [17, 22, 30, 31, 36],
        },
    },
    # ── 4. mistral_r14 LoRA adapter (640MB, foundation-borrow) ───────────
    {
        "file": ANIMA_ROOT / "state/mistral_r14_run/mistral_r14/final/adapter_model.safetensors",
        "repo_id": f"{HF_ORG}/anima-mistral-r14-r64-adapter-2026-04-26",
        "repo_type": "model",
        "kind": "lora_adapter_foundation_borrow",
        "card_meta": {
            "bg_id": "mistral_r14_run (pre-BG era)",
            "verdict_class": "V_PHEN_GWT_V2_HYPOTHESIS_FULL (corpus_docs=1200, axis verification target)",
            "v4_pass": "n/a (V_phen_GWT_v2 architecture-bound vs LoRA-trainable axis verification)",
            "cycle": "2026-04-26",
            "paradigm": "lora-r64-mistral-7b-r14-corpus",
            "base_model": "mistralai/Mistral-7B-v0.3",
            "lora_r": 64,
            "lora_alpha": 128,
            "lora_target_modules": "all-linear (q/k/v/o/gate/up/down_proj)",
            "corpus_docs": 1200,
            "epochs": 3,
            "lr": 5e-5,
            "training_elapsed_sec": 379.1,
            "own_17_compliance": "foundation-borrow (Mistral-7B-v0.3 base) — substrate-research lane only (permitted-context-of-G_x)",
            "own_30_layer": "final adapter (mandate-1)",
            "source_path": "state/mistral_r14_run/mistral_r14/final/adapter_model.safetensors",
            "compliance_own": [17, 22, 30, 31, 36],
        },
    },
    # ── 5. BG-KK V5-α 500M UBM final (535MB, anima-native) ───────────────
    {
        "file": ANIMA_ROOT / "state/anima_kk_v5_alpha_h100_500m_ubm_2026_05_07/ckpt_final.pt",
        "repo_id": f"{HF_ORG}/anima-kk-v5-alpha-500m-ubm-fail-2026-05-07",
        "repo_type": "model",
        "kind": "clm_scratch_byte_untie_v5_alpha",
        "card_meta": {
            "bg_id": "BG-KK",
            "verdict_class": "FAIL_TRUE",
            "verdict_reason": "V5-α architectural advantage scales but capacity insufficient: best_v58=0/5 even at 500M H100",
            "v4_pass": "0/5 V58 (best_composite n/a, val_loss=4.4387)",
            "cycle": "2026-05-07",
            "paradigm": "v5-alpha-byte-untie-h100-500m-ubm-22mb",
            "base_model": "scratch (anima-native, 24L/1024d/16h byte_untie, 782.6M params)",
            "arch": "vocab=256 byte-level + UNTIED head_a, n_ca_rules=8, block=1024",
            "corpus_path": "universe_brain_map 22.6MB UBM",
            "training_steps": 1500,
            "early_stop_reason": "v58 plateau at 0 for 3 consecutive evals",
            "best_val_loss_overall": 4.4336,
            "cost_usd": 0.407,
            "own_17_compliance": "anima-native (scratch byte-level, no external substrate)",
            "own_30_layer": "final ckpt (mandate-1, FAIL_TRUE preserved for Lesson L extension evidence)",
            "source_path": "state/anima_kk_v5_alpha_h100_500m_ubm_2026_05_07/ckpt_final.pt",
            "compliance_own": [17, 22, 28, 30, 31, 36],
        },
    },
    # ── 6. BG-IZ ckpt_step_1000 archival (515MB, intermediate) ───────────
    {
        "file": ANIMA_ROOT / "state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_step_1000.pt",
        "repo_id": f"{HF_ORG}/anima-iz-clm-continued-pretrain-ko-step1000-2026-05-07",
        "repo_type": "model",
        "kind": "clm_continued_pretrain_intermediate_ckpt",
        "card_meta": {
            "bg_id": "BG-IZ",
            "verdict_class": "INTERMEDIATE_CHECKPOINT_STEP_1000_ARCHIVAL",
            "v4_pass": "n/a (intermediate; final = #1 above)",
            "cycle": "2026-05-07",
            "paradigm": "clm-mk2-v1-continued-pretrain-ko-step-1000-archival",
            "base_model": "dancinlab/clm-v4-mk2-v1",
            "training_steps": 1000,
            "is_intermediate": True,
            "purpose": "Archival of mid-train state (step 1000 / 6000) for retroactive bf16-numerical OR consciousness-gate-collapse hypothesis investigation. Final ckpt preserves end-state (loss-stuck pattern visible at this intermediate step too).",
            "own_17_compliance": "anima-native (CLM mk2-v1 continued-pretrain intermediate)",
            "own_30_layer": "intermediate ckpt — mandate-1 strictly = final only; mandate-2 verify size sanity. step1000 retained as archival/diagnostic resource (raw#82 retraction-aware preserve)",
            "source_path": "state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_step_1000.pt",
            "compliance_own": [17, 22, 30, 31, 36],
            "note": " strict reads as 'final only' but mandate-7 retroactive cycle includes intermediate for diagnostic reproducibility. Public-facing default = #1 (final). step1000 = private archival.",
        },
    },
    # ── 7. BG-KM-CAP capacity-1.5B ckpt (348MB) ──────────────────────────
    # NOTE: verdict.json says final_class=FAILED + training_steps=0 (orchestrator
    # scp put failed pre-training). But ckpt_final.pt 348MB present in dir —
    # likely partial state pulled before pod teardown OR architecture skeleton
    # save before training started. Treat as orchestrator-failed archival.
    {
        "file": ANIMA_ROOT / "state/anima_km_capacity_h100_1_5b_2026_05_08/ckpt_final.pt",
        "repo_id": f"{HF_ORG}/anima-km-capacity-1-5b-orchestrator-failed-2026-05-08",
        "repo_type": "model",
        "kind": "clm_capacity_test_orchestrator_failed",
        "card_meta": {
            "bg_id": "BG-KM-CAP",
            "verdict_class": "FAILED (orchestrator scp put failed pre-training)",
            "v4_pass": "n/a (training_steps=0)",
            "cycle": "2026-05-08",
            "paradigm": "v5-alpha-byte-untie-h100-1.5b-bg-jy-corpus (planned)",
            "base_model": "scratch (anima-native, planned 1.5B)",
            "training_steps": 0,
            "stall_reason": "scp put failed local=anima_jy_chat_template_corpus → corpus transfer pre-training",
            "cost_usd": 0.817,
            "ckpt_size_mb": 348,
            "ckpt_anomaly": "ckpt_final.pt 348MB present despite training_steps=0 — likely architecture-init save before training start OR partial state pulled before pod teardown. Honest C3 — actual training did not occur per verdict.json; ckpt is architecture-skeleton snapshot.",
            "own_17_compliance": "anima-native (scratch arch skeleton, no external substrate)",
            "own_30_layer": "ckpt_final.pt (orchestrator-failed but artifact preserved per mandate-1 raw#82)",
            "source_path": "state/anima_km_capacity_h100_1_5b_2026_05_08/ckpt_final.pt",
            "compliance_own": [17, 22, 30, 31, 36],
            "note": "Upload as private archival per raw#82 (retraction-aware preserve) — failure mode evidence for mandate-1 effectiveness lessons.",
        },
    },
    # ── 8. BG-JE corpus 100MB+ (204MB, mixed source kowiki 70%) ──────────
    # ★ honest C3 — kowiki 69.6% external Wikipedia. NOT anima-native
    # in strict sense, but BG-JE was anima-curated assembly with persona
    # 3-variant rotation + chat-template format + UBM/NEXUS-UBM 28%
    # anima-native portion. Label = mixed-curated (anima curation wrapper
    # over kowiki external source). Tier B-archival (between A=full anima
    # and C=raw external).
    {
        "file": ANIMA_ROOT / "state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt",
        "repo_id": f"{HF_ORG}/anima-je-corpus-100mb-plus-2026-05-07",
        "repo_type": "dataset",
        "kind": "corpus_mixed_kowiki_ubm_persona",
        "card_meta": {
            "bg_id": "BG-JE",
            "verdict_class": "READY_FOR_TRAINING (corpus build only, $0)",
            "cycle": "2026-05-07",
            "paradigm": "corpus-100mb-plus-kowiki-ubm-nexus-outside-well-assembly",
            "size_mb": 204.372,
            "source_breakdown": {
                "kowiki": 0.6961,
                "ubm": 0.0324,
                "nexus_ubm": 0.2505,
                "outside_well": 0.0175,
                "eval_inject": 0.0034,
            },
            "kowiki_meta": "wikimedia/wikipedia 20231101.ko shard 1/3 — 85734 articles, 244471 QA pairs, 80MB extracted",
            "chat_template_ratio": 1.0,
            "hangul_ratio": 0.4761,
            "persona_3_variant_distribution": "[anima 우주뇌지도] 33% / [anima NEXUS-UBM] 33% / [anima identity] 33%",
            "eval_prompts_min_count": 160,
            "in_target_band_100_300mb": True,
            "own_17_compliance": "tier-b-mixed (anima curation wrapper over 70% kowiki external + 30% anima-native UBM/NEXUS) — substrate-research lane only, NOT anima identity-bearing pretrain corpus per strict . Persona-prefix wrap brings borderline anima-context but base text = generic Korean encyclopedia.",
            "honest_c3": [
                "kowiki content is generic Korean encyclopedia, NOT anima-domain — chat-cap signal may dilute UBM/NEXUS specificity",
                "external dataset wrapper — strict reading = anima-native lane reject; permissive reading = corpus-build lane allowed (substrate-research) with tier-b-mixed label mandatory",
            ],
            "source_path": "state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt",
            "compliance_own": [17, 22, 31, 36],
        },
    },
    # ── 9. corpus_mix 70wiki/30dialogue (148MB, ★ tier-c-archival) ───────
    # ★ strict — 70% kowiki external (corpus_v6_wiki.txt). dialogue 30% =
    # anima-native (Φ trace + RATCHET + KO 안정/이완 labels). Mixed = strict
    # tier-c-archival per recommendation (a) — preserve archival value (BG cycle
    # learning evidence) + strict + clear tier label.
    {
        "file": ANIMA_ROOT / "state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt",
        "repo_id": f"{HF_ORG}/anima-corpus-mix-70wiki-30dialogue-tier-c-archival-2026-05-06",
        "repo_type": "dataset",
        "kind": "corpus_mix_70wiki_30dialogue_archival",
        "card_meta": {
            "bg_id": "anima_corpus_mix (CLM-3 original byte-level redesign spec)",
            "verdict_class": "BUILD_COMPLETE_TIER_C_ARCHIVAL",
            "cycle": "2026-05-06",
            "paradigm": "70-30-wiki-dialogue-byte-level-mix-PATH-B-1-concat",
            "size_mb": 147.68,
            "lines_total": 3058661,
            "spec_doc": "docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md (lines 142-250)",
            "ratios_actual": "wiki 70.00% / dialogue 30.00% (line-ratio exact); byte-ratio 70.5/29.5",
            "wiki_source": "anima/ready/anima/data/corpus_v6_wiki.txt (2141063 lines, 109MB) — kowiki lineage",
            "dialogue_source": "anima/ready/anima/data/corpus_v8_dialogue.txt (head 917598 lines, ~46MB) — Φ trace + RATCHET KO 안정/이완 labels",
            "sha256": "2d15ca7d277aaaef95c7dbc9eb810ec38f0510e0578269810aa4eb879f51e0e8",
            "own_17_compliance": "tier-c-archival (★ STRICT) — 70% kowiki = external Wikipedia substrate, dialogue 30% = anima-native trace logs. Mix is NOT anima-native chat-cap pretrain corpus. Archival label MANDATORY per anima-no-external-substrate-wrapping. Used in prior BG cycle CLM-3 trainer reference but verdict_path = tier-c-archival (not promoted to anima identity-bearing pretrain lane).",
            "tier_label": "tier-c-archival",
            "archival_rationale": "User directive 2026-05-08 — recommended path (a) private archival with explicit tier-c-archival label. Reproducibility + strict + tier-label clarity. Not deletion (raw#82 retraction-aware preserve).",
            "honest_c3": [
                "wiki block = corpus_v6 lineage from kowiki → external substrate (strict reject for anima-native lane)",
                "dialogue block = anima-native Φ trace + RATCHET labels → 30% anima-native portion",
                "PATH-B-1 concat: wiki block first then dialogue — DataLoader shuffle dependency",
                "byte-ratio 70.5/29.5 vs line-ratio 70.0/30.0 (dialogue lines avg ~17.7 bytes vs wiki ~50.9 bytes)",
                "Used in prior CLM-3 trainer reference; tier-c label clarifies scope for future BG dispatchers",
            ],
            "source_path": "state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt",
            "compliance_own": [17, 22, 31, 36],
        },
    },
]


def hf_token() -> str:
    if not HF_TOKEN_FILE.exists():
        sys.exit(f"HF token missing at {HF_TOKEN_FILE}")
    return HF_TOKEN_FILE.read_text().strip()


def build_card_md(plan: dict) -> str:
    """Generate README.md (HF Model/Dataset Card) per mandate-9."""
    meta = plan["card_meta"]
    repo_id = plan["repo_id"]
    name = repo_id.split("/")[-1]
    kind = plan["kind"]
    repo_type = plan["repo_type"]
    yaml_tags = [
        "  - anima",
        "  - korean",
        f"  - {kind.replace('_', '-')}",
        f"  - cycle-{meta.get('cycle','?')}",
    ]
    if "anima-native" in str(meta.get("own_17_compliance", "")):
        yaml_tags.append("  - anima-native")
    if "foundation-borrow" in str(meta.get("own_17_compliance", "")):
        yaml_tags.append("  - foundation-borrow")
        yaml_tags.append("  - substrate-research")
    if "tier-c-archival" in str(meta.get("own_17_compliance", "")) or meta.get("tier_label") == "tier-c-archival":
        yaml_tags.append("  - tier-c-archival")
        yaml_tags.append("  - mixed-source")
    if "tier-b-mixed" in str(meta.get("own_17_compliance", "")):
        yaml_tags.append("  - tier-b-mixed")
    if "lora" in kind:
        yaml_tags.append("  - lora")
    if "corpus" in kind:
        yaml_tags.append("  - corpus")
    if "intermediate" in kind:
        yaml_tags.append("  - intermediate-checkpoint")
        yaml_tags.append("  - archival")

    body_lines = [
        f"# {name}",
        "",
        f"anima large artifact (mandate retroactive) — **{kind.replace('_',' ')}**.",
        "",
        "## Origin",
        f"- BG / source: `{meta.get('bg_id','?')}`",
        f"- Cycle: {meta.get('cycle','?')}",
        f"- Paradigm: `{meta.get('paradigm','?')}`",
        f"- Verdict class: `{meta.get('verdict_class','?')}`",
    ]
    if "v4_pass" in meta:
        body_lines.append(f"- V4 pass: `{meta['v4_pass']}`")
    if "base_model" in meta:
        body_lines.append(f"- Base model: `{meta['base_model']}`")
    if "lora_r" in meta:
        body_lines.append(f"- LoRA r: `{meta['lora_r']}` / alpha: `{meta.get('lora_alpha','?')}`")
        body_lines.append(f"- LoRA target: `{meta.get('lora_target_modules','?')}`")
    if "training_steps" in meta:
        body_lines.append(f"- Training steps: `{meta['training_steps']}`")
    if "corpus_path" in meta:
        body_lines.append(f"- Corpus: `{meta['corpus_path']}`" + (f" ({meta.get('corpus_size_mb','?')}MB)" if "corpus_size_mb" in meta else ""))
    if "size_mb" in meta:
        body_lines.append(f"- Size: `{meta['size_mb']}MB`")
    if "cost_usd" in meta:
        body_lines.append(f"- Cost: `${meta['cost_usd']}`")

    if "diagnostic" in meta:
        body_lines.extend(["", "## Diagnostic", f"- {meta['diagnostic']}"])
    if "verdict_reason" in meta:
        body_lines.extend(["", "## Verdict reason", f"- {meta['verdict_reason']}"])
    if "stall_reason" in meta:
        body_lines.extend(["", "## Stall reason", f"- {meta['stall_reason']}"])
    if "ckpt_anomaly" in meta:
        body_lines.extend(["", "## Checkpoint anomaly note", f"- {meta['ckpt_anomaly']}"])

    if "source_breakdown" in meta:
        body_lines.extend(["", "## Source breakdown"])
        for k, v in meta["source_breakdown"].items():
            body_lines.append(f"- {k}: {v*100:.2f}%")

    if "kowiki_meta" in meta:
        body_lines.extend(["", "## kowiki source", f"- {meta['kowiki_meta']}"])

    if "wiki_source" in meta:
        body_lines.extend(["", "## Sources (mix)", f"- wiki: `{meta['wiki_source']}`", f"- dialogue: `{meta['dialogue_source']}`"])

    if "honest_c3" in meta:
        body_lines.extend(["", "## Honest C3"])
        for c in meta["honest_c3"]:
            body_lines.append(f"- {c}")

    body_lines.extend(["", "## own SSOT compliance"])
    for o in meta.get("compliance_own", []):
        body_lines.append(f"- own {o}")

    body_lines.extend([
        "",
        f"** compliance**: {meta.get('own_17_compliance','?')}",
    ])
    if "own_30_layer" in meta:
        body_lines.append(f"** layer**: {meta['own_30_layer']}")

    body_lines.extend([
        "",
        "## Provenance",
        f"- Original path: `{meta.get('source_path','?')}`",
        f"- Anima repo: https://github.com/dancinlife/anima (private)",
        f"- Roadmap: `.roadmap.cli` cli.large_artifact_hf_upload_2026_05_08",
        "",
        "## License",
        "anima-research (private dancinlab org). 사용자 manual approval required for any external sharing.",
    ])

    if meta.get("note"):
        body_lines.extend(["", "## Note", meta["note"]])

    yaml_header = "---\n"
    yaml_header += "license: other\n"
    yaml_header += "language:\n  - ko\n  - en\n"
    yaml_header += "tags:\n" + "\n".join(yaml_tags) + "\n"
    if repo_type == "model" and meta.get("base_model"):
        # base_model only valid in model card metadata
        bm = meta["base_model"].split(" ")[0]  # strip parenthetical
        if "/" in bm:
            yaml_header += f"base_model: {bm}\n"
    if repo_type == "dataset" and meta.get("size_mb"):
        sz = meta["size_mb"]
        if sz >= 100:
            yaml_header += "size_categories:\n  - 100M<n<1B\n"
        elif sz >= 10:
            yaml_header += "size_categories:\n  - 10M<n<100M\n"
    yaml_header += f"pretty_name: {name}\n"
    yaml_header += "---\n\n"
    return yaml_header + "\n".join(body_lines) + "\n"


def append_log(entry: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def plan_emit(plan: dict, mode: str):
    f = plan["file"]
    if not f.exists():
        return {"status": "ERROR_FILE_MISSING", "file": str(f), "repo_id": plan["repo_id"]}
    size_b = f.stat().st_size
    size_mb = size_b / 1024 / 1024
    card_md = build_card_md(plan)
    return {
        "status": "PLANNED" if mode == "dry-run" else "PENDING",
        "file": str(f),
        "size_mb": round(size_mb, 2),
        "size_bytes": size_b,
        "repo_id": plan["repo_id"],
        "repo_type": plan["repo_type"],
        "kind": plan["kind"],
        "card_meta": plan["card_meta"],
        "card_md_bytes": len(card_md),
        "card_md_preview": card_md[:300],
    }


def upload_one(plan: dict, token: str) -> dict:
    """Real upload: create_repo (private) + upload_file + Card README."""
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    repo_id = plan["repo_id"]
    repo_type = plan["repo_type"]
    f = plan["file"]
    t0 = time.time()
    try:
        # mandate-8: private default
        api.create_repo(
            repo_id=repo_id,
            repo_type=repo_type,
            private=True,
            exist_ok=True,
        )
        # upload artifact (preserve original filename in repo root)
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=f.name,
            repo_id=repo_id,
            repo_type=repo_type,
            commit_message=f" mandate-1/2 retroactive — {plan['kind']} (cycle {plan['card_meta'].get('cycle','?')})",
        )
        # upload Card README.md (mandate-9)
        card_md = build_card_md(plan)
        api.upload_file(
            path_or_fileobj=card_md.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type=repo_type,
            commit_message=" mandate-9 — HF Card metadata emit",
        )
        elapsed = time.time() - t0
        url_prefix = "datasets/" if repo_type == "dataset" else ""
        return {
            "status": "UPLOADED",
            "repo_id": repo_id,
            "url": f"https://huggingface.co/{url_prefix}{repo_id}",
            "private": True,
            "elapsed_sec": round(elapsed, 2),
        }
    except Exception as e:
        return {
            "status": "ERROR_UPLOAD",
            "repo_id": repo_id,
            "error": f"{type(e).__name__}: {e}",
            "elapsed_sec": round(time.time() - t0, 2),
        }


def verify_one(plan: dict, token: str) -> dict:
    """Post-upload verify: repo exists + size match."""
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    repo_id = plan["repo_id"]
    repo_type = plan["repo_type"]
    f = plan["file"]
    expected_size = f.stat().st_size
    try:
        if repo_type == "dataset":
            info = api.dataset_info(repo_id=repo_id, token=token)
        else:
            info = api.model_info(repo_id=repo_id, token=token)
        siblings = {s.rfilename: s.size for s in info.siblings if s.size}
        actual_size = siblings.get(f.name)
        size_match = actual_size == expected_size if actual_size else None
        return {
            "status": "VERIFIED" if size_match else "SIZE_MISMATCH",
            "repo_id": repo_id,
            "private": info.private,
            "expected_size": expected_size,
            "actual_size": actual_size,
            "files_in_repo": list(siblings.keys()),
        }
    except Exception as e:
        return {
            "status": "ERROR_VERIFY",
            "repo_id": repo_id,
            "error": f"{type(e).__name__}: {e}",
        }


def main():
    ap = argparse.ArgumentParser(description=" 응용 (RETROACTIVE) — 9 large artifact HF dancinlab upload")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", default=True, help="Plan only (default)")
    g.add_argument("--apply", action="store_true", help="Real upload (사용자 explicit consent 'OK LARGE ARTIFACT HF UPLOAD' 필요)")
    g.add_argument("--verify", action="store_true", help="Post-upload verify (repo exists + size match)")
    args = ap.parse_args()

    mode = "verify" if args.verify else ("apply" if args.apply else "dry-run")
    print(f"[anima_large_artifact_hf_upload] mode={mode}")
    print(f"[anima_large_artifact_hf_upload] org={HF_ORG} (mandate-1)")
    print(f"[anima_large_artifact_hf_upload] files={len(ARTIFACT_PLAN)} (mandate-1 + mandate-2 scope; mandate-7 retroactive)")
    print()

    token = None
    if mode in ("apply", "verify"):
        token = hf_token()

    overall = {
        "ts_start": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": mode,
        "org": HF_ORG,
        "scope": "9 large artifact retroactive (mandate-7)",
        "plans": [],
    }

    rc_overall = 0
    total_size_b = 0
    for plan in ARTIFACT_PLAN:
        print(f"--- {plan['repo_id']} ({plan['repo_type']}) ---")
        if mode == "dry-run":
            res = plan_emit(plan, mode="dry-run")
            print(f"  status: {res['status']}")
            print(f"  file: {res.get('file')}")
            print(f"  size: {res.get('size_mb')}MB ({res.get('size_bytes')} B)")
            print(f"  kind: {res.get('kind')}")
            print(f"  card_md: {res.get('card_md_bytes')} bytes")
            cm = res.get("card_meta", {})
            print(f"  bg_id: {cm.get('bg_id')}")
            print(f"  own_17: {cm.get('own_17_compliance','?')[:80]}...")
            if res.get("status") == "PLANNED":
                total_size_b += res.get("size_bytes", 0)
        elif mode == "apply":
            res = upload_one(plan, token)
            print(f"  status: {res['status']}")
            if "url" in res:
                print(f"  url: {res['url']} (private)")
            if "error" in res:
                print(f"  error: {res['error']}")
                rc_overall = 1
            print(f"  elapsed: {res.get('elapsed_sec','?')}s")
        elif mode == "verify":
            res = verify_one(plan, token)
            print(f"  status: {res['status']}")
            if "private" in res:
                print(f"  private: {res['private']}")
                print(f"  expected: {res.get('expected_size')} / actual: {res.get('actual_size')}")
            if "error" in res:
                print(f"  error: {res['error']}")
                rc_overall = 1
        overall["plans"].append({
            "repo_id": plan["repo_id"],
            "repo_type": plan["repo_type"],
            "result": res,
        })
        print()

    overall["ts_end"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    overall["rc"] = rc_overall
    if mode == "dry-run":
        overall["total_size_planned_mb"] = round(total_size_b / 1024 / 1024, 2)
        overall["total_size_planned_gb"] = round(total_size_b / 1024 / 1024 / 1024, 3)
    append_log(overall)
    print(f"[anima_large_artifact_hf_upload] log appended: {LOG_PATH}")
    print(f"[anima_large_artifact_hf_upload] rc={rc_overall}")
    if mode == "dry-run":
        print(f"[anima_large_artifact_hf_upload] total planned size: {overall['total_size_planned_mb']} MB ({overall['total_size_planned_gb']} GB)")
        print()
        print("[anima_large_artifact_hf_upload] DRY-RUN COMPLETE — no HF mutations performed.")
        print("[anima_large_artifact_hf_upload] To apply: python3 tool/anima_large_artifact_hf_upload.py --apply")
        print("[anima_large_artifact_hf_upload] (사용자 explicit directive 'OK LARGE ARTIFACT HF UPLOAD' 권고)")
    sys.exit(rc_overall)


if __name__ == "__main__":
    main()
