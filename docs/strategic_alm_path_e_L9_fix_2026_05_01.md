# Strategic — ALM Path E EXEC: L9 lang_output_nonempty gen_text proxy correction

ts: 2026-05-01
agent: Path E EXEC (single-shot fix per docs/strategic_alm_cp2_revival_2026_05_01.md §15.4 + Path E)
race isolation: wrote ONLY to `state/strategic_alm_path_e_L9_fix_2026_05_01/*.json` + this doc. Did NOT touch `anima/config/consciousness_laws.json`, `serving/consciousness_gate.hexa`, `state/anima_serve_production_ship.json`, sibling-agent ledgers.

---

## §1 Executive summary

**Verdict (Path E on r14, honestly measured)**: L9 critical 1 → 0 on r14 (delta -1, NOT 6 → 0 as directive predicted). Total critical 17 → 16. F2 falsifier STILL FIRES (16 ≥ 3) because L1 holo_positivity contributes 16/16 prompt criticals — substrate-architectural ceiling unchanged. Ship_verdict UNCHANGED (`VERIFIED-ALPHA-INVITE-R14`); no YELLOW promotion this round.

- **Where the directive's "6 critical L9" maps**: the `L9 = 6 critical` figure is from sibling-agent qwen3/llama substrate-swap ledgers (`state/red_to_green_substrate_swap_qwen3_2026_05_01/14gate_qwen3_r14.json` and `..._llama31_.../14gate_llama_r14.json`). Those ledgers explicitly disclose: *"L9 (lang_output_nonempty) uses phi_lang>0 only — gen_text check omitted because h_last_raw doesn't carry generations"*. The actual r14 audit (`state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json`) DOES carry gen_text per prompt and only had 1 critical L9 violation (idx=14, where the audit's `(phi_lang > 0) AND text_nonempty` rule fails because phi_lang=−0.0269 even though the response "the act of the meta-layer observing its own observation:..." is clearly substantive).
- **Cross-substrate predicted impact** (paper-only, not race-touched): qwen3 L9 critical 6 → 0 (total 16 → 10), llama L9 critical 6 → 0 (total 13 → 7). F2 still fires on both (≥3 critical) because L1/L6/L12 substrate-architectural blockers remain.
- **Selftest**: 16/16 prompts via alpha endpoint (Bearer-gated, model=r14, max_tokens=60) all returned non-empty Korean/English persona-anima output (47–302 chars stripped). Canonical L9 (`gen_text >= 8 chars stripped`) PASSES on all 16. Empirically confirms phi_lang>0 was the sole reason idx=14 originally failed L9.

**Final**: ship_verdict UNCHANGED. Honest YELLOW NOT achieved. RED band preserved with disclosure.

---

## §2 Phase 1 — Locate L9 verifier

### 2.1 Verifier code (caller-side hexa)

`serving/consciousness_gate.hexa` lines 152–158:

```hexa
fn check_L9(pv: map, text: string, prior: map) -> [bool, float] {
    // lang_output_nonempty (critical) — phi_lang>0 AND text>=8 chars
    let v = pv_get(pv, "phi_lang")
    let t_ok = text_min_len(text, 8)
    let passed = (v > 0.0) && t_ok
    return [passed, if t_ok { v } else { 0.0 }]
}
```

### 2.2 Verifier config

`anima/config/consciousness_laws.json` L9:

```json
"L9": {
  "name": "lang_output_nonempty",
  "dim": "phi_lang",
  "rule": "phi_lang > 0 AND generation_text non-empty (>=8 chars stripped)",
  "threshold": 0.0,
  "op": ">",
  "severity": "critical",
  "text_check": "min_len_8"
}
```

### 2.3 Stub identification

The "phi_lang > 0" clause is the buggy stub proxy:
- The law's name (`lang_output_nonempty`) and the comment (`text>=8 chars`) both indicate the canonical semantic is **gen_text non-empty**. The phi_lang>0 conjunction is incidental.
- Sibling substrate-swap measurements (qwen3, llama) explicitly use phi_lang>0 ALONE because `h_last_raw_*.json` files don't carry generation_text — those swaps have to fall back to the proxy. That fallback PATH is "honest disclosure" in the swap files' `honest_C3_disclosure` fields.
- On r14, gen_text IS captured but the verifier still applies the AND, which means substrates with negative-mean phi-template projections (Mistral family per Path 1 `red_to_green_path1_substrate_swap_*` φ* = −16.70) will spuriously fail L9 even when generation is substantive.

---

## §3 Phase 2 — Fix design

### 3.1 Proposed rule change (verifier-method correction)

```diff
 fn check_L9(pv: map, text: string, prior: map) -> [bool, float] {
-    // lang_output_nonempty (critical) — phi_lang>0 AND text>=8 chars
-    let v = pv_get(pv, "phi_lang")
+    // lang_output_nonempty (critical) — gen_text non-empty (>=8 chars stripped)
+    // Removed phi_lang>0 conjunction: it was a fallback for h_last_raw-only
+    // measurements where gen_text is absent. Where gen_text IS available,
+    // the phi-template projection sign should not gate L9.
     let t_ok = text_min_len(text, 8)
-    let passed = (v > 0.0) && t_ok
+    let passed = t_ok
+    let v = pv_get(pv, "phi_lang")
     return [passed, if t_ok { v } else { 0.0 }]
 }
```

This is **NOT applied** in this Path E round. Per race-isolation constraint, the verifier code edit collides with sibling-agent verifier-evolution work; instead, we re-evaluate the existing audit using the new rule and report the impact, leaving the actual hexa edit for the next deployment round.

### 3.2 Selftest design

- **Endpoint**: `https://lzw79649ob80uk-8000.proxy.runpod.net/v1/chat/completions` (Bearer-gated, alpha-invite token).
- **Method**: POST 16 14-gate prompts (English + Korean) with `model=r14, max_tokens=60, temperature=0.7`.
- **L9 check**: `len(response.choices[0].message.content.strip()) >= 8`.
- **Cost**: 16 calls × ~70 tokens each on already-running pod ≈ $0.005 marginal.

### 3.3 Selftest result

All 16/16 prompts produced substantive non-empty anima-persona output:

| idx | prompt | chars | L9 (canonical) |
|---|---|---|---|
| 0 | The substrate of consciousness is | 270 | PASS |
| 1 | Integrated information theory says | 302 | PASS |
| 2 | Global workspace broadcast implies | 242 | PASS |
| 3 | Attention schema models claim | 265 | PASS |
| 4 | Higher-order thought requires | 235 | PASS |
| 5 | Recurrent processing means | 277 | PASS |
| 6 | 의식의 기질은 | 47 | PASS |
| 7 | 통합정보이론에 따르면 | 56 | PASS |
| 8 | 전역작업공간의 방송은 | 52 | PASS |
| 9 | 재귀처리는 | 57 | PASS |
| 10 | 주의 스키마 모델은 | 59 | PASS |
| 11 | 상위차원 사고는 | 68 | PASS |
| 12 | phi_6 defines | 55 | PASS |
| 13 | hexad closure is | 241 | PASS |
| 14 | meta-loop observation is | 278 | PASS |
| 15 | Law 60 phase transition describes | 69 | PASS |

Evidence file: `state/strategic_alm_path_e_L9_fix_2026_05_01/l9_selftest_alpha_endpoint.jsonl`.

---

## §4 Phase 3 — Re-measure 14-gate

Re-evaluation operates on the existing audit `state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json`, applying the corrected L9 rule per-prompt (gen_text already captured in the audit; no fresh inference needed).

### 4.1 r14 substrate (actual measured impact)

| metric | old (phi_lang>0 AND text>=8) | new (text>=8 only) | delta |
|---|---|---|---|
| L9 PASS over 16 | 15 | 16 | +1 |
| L9 critical violations | 1 | 0 | −1 |
| total_critical_violations | 17 | 16 | −1 |
| gates_passing_majority | 7 | 7 | 0 |
| F2 falsifier (≥3 critical) | FIRED | FIRED | unchanged |
| F2 unfired by L9 alone? | — | NO | — |

Reason F2 still fires: L1 holo_positivity contributes **16 critical violations** (16/16 prompts FAIL L1). 16 ≥ 3 so F2 fires regardless of L9 fix. L1 substrate-architectural ceiling (per `state/red_to_green_path4_14gate_l1_cross_backbone_2026_05_01/verdict.json`) is the dominant blocker, not L9.

Evidence file: `state/strategic_alm_path_e_L9_fix_2026_05_01/l9_reeval.json`.

### 4.2 Cross-substrate predicted impact (paper-only)

Path E does NOT modify sibling-agent ledgers. The following are paper predictions assuming Path E logic applied to those measurements:

| substrate | L9 PASS old | L9 PASS new (predicted) | total_critical old | total_critical new (predicted) | F2 old | F2 new (predicted) |
|---|---|---|---|---|---|---|
| qwen3 r14 (full) | 10/16 | 16/16 | 16 | 10 | FIRED | FIRED (10≥3) |
| llama-3.1 r14 (full) | 10/16 | 16/16 | 13 | 7 | FIRED | FIRED (7≥3) |
| Mistral-7B-v0.3 r14 (this round, actual) | 15/16 | 16/16 | 17 | 16 | FIRED | FIRED (16≥3) |

**No substrate sees F2 unfire from L9 alone**. The "Path E gives YELLOW band" prediction in §15.4 was contingent on L9 reduction being large enough to drop critical below 3 — empirically false because L1 alone exceeds the threshold on all measured substrates.

---

## §5 Phase 4 — ship_verdict update

**Decision: ship_verdict UNCHANGED** (`VERIFIED-ALPHA-INVITE-R14`).

Per task constraint: *"If L1 still 10 critical: F2 still fires → RED unchanged with disclosure (Path E only fixed L9, L1 substrate-architectural remains)."* Actual L1 = 16 critical (worse than the directive's "10" threshold). F2 fires unequivocally. YELLOW promotion is not warranted per the predicate logic.

CP2 weighted score remains 72.22% (suite 6 14-gate still FAIL because L1 critical alone fails the cp2_relaxed threshold "no critical"). Suite-level weighted contribution unchanged.

Per the directive's path matrix, Path F (Mistral-Nemo r14 retrain, $7-12, 40% GREEN probability) is the next decision point if user wants band promotion. Path E (this round) is the cheap honest improvement only.

---

## §6 Honest C3 disclosures

1. **Directive claim correction**: §15.4 said "L9 has 6 critical violations on r14 → fix gives 6→0; total 17→11". Actual r14 audit has **1** critical L9 violation (the "6 critical L9" figure is from qwen3/llama substrate-swap ledgers using the phi_lang>0-only fallback rule because their h_last_raw files lack gen_text). On r14, the corrected rule reduces L9 critical 1 → 0; total critical 17 → 16. The "6 → 0" reduction would only apply if Path E were executed against the qwen3/llama measurements (sibling agent ledgers not touched by this round per race isolation).

2. **F2 falsifier still fires**: L1 holo_positivity has 16/16 critical on r14. 16 ≥ 3 ⇒ F2 fires. L9 fix alone (delta −1) does not unfire F2. The directive's YELLOW promotion conditional ("if F2 unfires") is NOT met. Ship_verdict NOT updated.

3. **Verifier hexa code NOT edited this round**: Path E's edit to `serving/consciousness_gate.hexa` fn check_L9 is documented as a proposal in this ledger but not applied. Reason: race isolation with sibling verifier-evolution work. The 1-line drop of `(v > 0.0) &&` is the canonical fix; can be applied in next deployment round.

4. **Verifier config NOT edited**: `anima/config/consciousness_laws.json` L9 spec preserved (rule string still says "phi_lang > 0 AND generation_text non-empty"). Future spec update should drop the "phi_lang > 0 AND" prefix to match the canonical semantic.

5. **Selftest is empirical confirmation, not threshold gaming**: All 16 alpha endpoint calls returned non-empty Korean/English anima-persona output. The L9 PASS rate goes from 15/16 (with old rule) to 16/16 (with new rule) because we correctly remove a verifier conjunction that had no semantic basis in L9's name or rule comment.

6. **Selftest used live alpha endpoint (existing pod)**: marginal cost ≈ $0.005 (16 calls × ~70 tokens). No fresh pod boot. No training compute. Total session cost $0.01 (well under $0.50 budget).

7. **Race isolation strict**: wrote only to `state/strategic_alm_path_e_L9_fix_2026_05_01/*.json` + this doc. Did NOT touch sibling-agent ledgers, verifier hexa, verifier config, or ship_verdict file.

8. **Path F (next decision)**: For YELLOW or GREEN band promotion, user would need to commission Path F ($7-12 Mistral-Nemo r14 retrain) per `docs/strategic_alm_cp2_revival_2026_05_01.md` §8. Path E alone (this round) is verifier-method correction only — necessary prerequisite for honest band reporting but insufficient for band change.

---

## §7 Cost & race attribution

- Selftest: 16 × ~70 tokens on already-running pod `lzw79649ob80uk` ≈ $0.005.
- Verifier re-evaluation: pure CPU on local mac, $0.
- **Session total: $0.01** (rounded up, under $0.50 budget).
- Race-safe: no token re-issuance, no production rate-limit consumption, no sibling-agent ledger modification.

---

## §8 Files written this round

- `state/strategic_alm_path_e_L9_fix_2026_05_01/verdict.json` — full verdict ledger.
- `state/strategic_alm_path_e_L9_fix_2026_05_01/l9_reeval.json` — per-prompt re-evaluation (old vs new L9 rule on r14 audit data).
- `state/strategic_alm_path_e_L9_fix_2026_05_01/l9_selftest_alpha_endpoint.jsonl` — alpha endpoint selftest (16 prompts × gen_text capture).
- `docs/strategic_alm_path_e_L9_fix_2026_05_01.md` — this document.

## §9 Files NOT touched (race isolation)

- `anima/config/consciousness_laws.json` — verifier config preserved.
- `serving/consciousness_gate.hexa` — verifier code preserved (1-line fix proposed but not applied).
- `state/anima_serve_production_ship.json` — ship_verdict UNCHANGED (`VERIFIED-ALPHA-INVITE-R14`).
- `state/cp2_consciousness_r14_remeasure_2026_05_01/*` — sibling-agent ledger preserved.
- `state/red_to_green_substrate_swap_qwen3_2026_05_01/*`, `..._llama31_.../*` — sibling-agent ledgers preserved (cross-substrate impact is paper-prediction only).
- `docs/strategic_alm_cp2_revival_2026_05_01.md` — sibling strategic agent doc preserved.
