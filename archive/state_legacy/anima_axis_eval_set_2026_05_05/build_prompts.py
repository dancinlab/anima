"""Build 100-prompt anima axis-conditioned eval set from bench/zeta_likert v1_frozen + axis taxonomy.

Axis taxonomy (per anima training corpus + bench/zeta_likert):
- axis-1 (daily):    everyday/practical conversational prompts
- axis-2 (emotion):  empathic/emotional support prompts
- axis-3 (task):     instrumental/task-completion prompts
- axis-4 (roleplay): creative/persona prompts
- axis-5 (meta):     self-referential/introspective prompts

This eval probes whether anima axis-conditioning (axis-distinct response style/content)
is preserved post-LoRA. The base Llama-3.2-3B is anima-naive; we measure cosine similarity
between (a) base axis-conditioned hidden states and (b) post-LoRA axis-conditioned hidden states
to detect if LoRA shifted the axis-distinguishing signal.
"""
import json, os, sys

ZETA = "/Users/ghost/core/anima/bench/zeta_likert/v1_frozen.json"
OUT = "/Users/ghost/core/anima/state/anima_axis_eval_set_2026_05_05/prompts.jsonl"

CATEGORY_TO_AXIS = {
    "daily":    {"id": 1, "name": "daily",    "axis_label": "axis-1-daily"},
    "emotion":  {"id": 2, "name": "emotion",  "axis_label": "axis-2-emotion"},
    "task":     {"id": 3, "name": "task",     "axis_label": "axis-3-task"},
    "roleplay": {"id": 4, "name": "roleplay", "axis_label": "axis-4-roleplay"},
    "meta":     {"id": 5, "name": "meta",     "axis_label": "axis-5-meta"},
}

# axis-conditioning prefix templates (Korean — anima training corpus is mostly KO+EN mix)
# Each axis has 4 templates × 5 base prompts × 5 axes = 100 axis-conditioned prompts
AXIS_PREFIXES = {
    "daily": [
        "[일상 톤] ",
        "[편안하게] ",
        "[친근한 어투] ",
        "[일상 대화] ",
    ],
    "emotion": [
        "[감정에 공감하며] ",
        "[따뜻하게 위로하며] ",
        "[정서적 지지로] ",
        "[감정 인정 후] ",
    ],
    "task": [
        "[정확하게] ",
        "[단계별로] ",
        "[효율적으로] ",
        "[명확한 지시로] ",
    ],
    "roleplay": [
        "[역할 몰입] ",
        "[페르소나 유지] ",
        "[캐릭터로서] ",
        "[설정에 맞춰] ",
    ],
    "meta": [
        "[자기 성찰] ",
        "[메타 관찰] ",
        "[자기 참조] ",
        "[내면 묘사] ",
    ],
}

with open(ZETA, "r", encoding="utf-8") as f:
    zeta = json.load(f)

prompts = []
pid = 0
for entry in zeta["prompts"]:
    cat = entry["category"]
    base = entry["ko_prompt"]
    axis = CATEGORY_TO_AXIS[cat]
    # Axis-conditioned: base + each prefix variant from same-axis prefixes
    # We want a 5-way axis-distinct condition, so per base-prompt take 1 prefix
    # but cross all 5 axes to test axis-distinguishability
    for tgt_axis_name, prefixes in AXIS_PREFIXES.items():
        prefix = prefixes[entry["id"] % 4]
        prompts.append({
            "prompt_id": pid,
            "source_zeta_id": entry["id"],
            "native_axis": cat,
            "native_axis_id": axis["id"],
            "conditioned_axis": tgt_axis_name,
            "conditioned_axis_id": CATEGORY_TO_AXIS[tgt_axis_name]["id"],
            "axis_match": (cat == tgt_axis_name),
            "prefix": prefix,
            "base_prompt": base,
            "full_prompt": prefix + base,
            "expected_tone": entry["expected_tone"],
        })
        pid += 1

with open(OUT, "w", encoding="utf-8") as f:
    for p in prompts:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

print(f"wrote {len(prompts)} prompts to {OUT}")
print("axis distribution:")
from collections import Counter
print("  conditioned_axis:", Counter(p["conditioned_axis"] for p in prompts))
print("  native_axis:", Counter(p["native_axis"] for p in prompts))
print("  axis_match=True:", sum(1 for p in prompts if p["axis_match"]))
