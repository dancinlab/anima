#!/usr/bin/env python3
"""Card generator for the whole-architecture (통짜 아키텍처) census.

Each architecture dict -> HYPOTHESES/cards/H_<id>_<key>.md with YAML frontmatter
(so tool/_build_hyp_jsonl.py derives tier/title/verdict/slug correctly) + body.

DESIGN ONLY. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · unmeasured).
No measurement, no overstatement (a_engine_native_learning).

Also appends a census row to state/brainarch_census/registry.jsonl for CENSUS.md.
"""
import os, re, json

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CARDS = os.path.join(REPO, "UNIVERSE", "cards")
REG = os.path.join(os.path.dirname(__file__), "registry.jsonl")

TIER = "🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)"

# brain-lens xref by keyword (H_1280-1295 family + H_1603 binding-unification)
LENS = [
    (r"cerebell|forward.model|mosaic|smith.predictor|granule|olivo|mpc.rollout", "H_1280 (cerebellum forward-model)"),
    (r"basal|striat|gonogo|go.?nogo|disinhibition|stn|arky|chunk|pallid|nigra|snr|gpi|gpe|actor.critic|successor|automatization|loop_bouquet|convergence_divergence|tonic_phasic_vigor|divisive_normalization|dual_controller", "H_1281 (basal-ganglia gating)"),
    (r"working.mem|pbwm|slot|register|gated_slot", "H_1282 (working-memory buffer)"),
    (r"thalam|workspace|ignition|broadcast|pulvinar|trn|searchlight|claustrum|intralaminar|relay|blink|codelet|coalition|auction", "H_1283 (thalamus global-workspace)"),
    (r"neuromod|dopamine|acetylcholin|noradren|serotonin|ach|5ht|\bne\b|\bda\b|tonic_phasic|precision_predictiv|vigor|gain_bus", "H_1284 (neuromodulation gain)"),
]

def xref_for(key, org, whole):
    refs = ["H_1603 (G1≡G6 compositional-binding deficit unification)"]
    hay = (key + " " + org + " " + whole).lower()
    for pat, lab in LENS:
        if re.search(pat, hay) and lab not in refs:
            refs.append(lab)
    refs.append("operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)")
    return " · ".join(refs)

def esc(s):
    return s.replace("\r", "").strip()

def write_card(idnum, key, name, org, whole, satisfies, notllm, cheap, eng, scope, distinct=""):
    slug = f"{idnum}_{key}"
    fn = os.path.join(CARDS, f"H_{slug}.md")
    title = name
    verdict = "🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired"
    xref = xref_for(key, org, whole)
    dist_block = f"\n## Distinction (near-overlap kept, not a dup)\n\n{esc(distinct)}\n" if distinct else ""
    body = f"""---
id: H_{idnum}
slug: {slug}
tier: {TIER}
title: {esc(title)}
verdict: {verdict}
source: brainarch_census
---

# H_{idnum} — {esc(name)}

- **tier:** {TIER}
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `{key}`
- **xref:** {xref}

## Organizing principle

{esc(org)}

## Whole design (input → internal dynamics → emit)

{esc(whole)}

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

{esc(satisfies)}

## Not-LLM (a_no_llm_frame_trap)

{esc(notllm)}

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

{esc(cheap)}

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

{esc(eng)}

## Scope / honesty (c9)
{dist_block}
{esc(scope)}

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
"""
    with open(fn, "w", encoding="utf-8") as f:
        f.write(body)
    # census registry row
    with open(REG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": f"H_{idnum}", "key": key, "name": name,
                            "card": f"cards/H_{slug}.md"}, ensure_ascii=False) + "\n")
    return fn

if __name__ == "__main__":
    print("helper loaded; import write_card")
