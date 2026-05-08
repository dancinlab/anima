# anima 모델 + 학습 방법 전수 재평가 (2026-05-08)

**SSOT**: `state/anima_model_method_reassessment_2026_05_08.json`
**user-directive verbatim** (2026-05-08): "기존 모델, 학습방법 들 모두 재평가 필요"
**scope**: 기존 anima 모든 모델 (BG saga 22+ + CLM v2/v3/v4 lineage + ALM/외부 base lane + anima native byte-level) + 학습 방법 (continued pretrain / SFT / DPO RLHF / scratch / byte-level / federated multi-cell / LoRA / distill / dual-engine / safeguard wrapping) 전수 retroactive 재평가
**policy**:
- own 17 (D1 anima identity boundary strict)
- own 18 P5 v2 N-of-M aggregation rule (PPR_v2 ≥0.6 ∧ EMC_v2 ≥3 of 4) + ★ scope-clamp 2026-05-08 (line 770 — D1 lane within 만 SIMPLE_STACK_PASS_STRICT_C3_ANIMA verdict valid)
- own 33 trinity (philosophy + law + hypothesis) 무조건 준수
- own 37 mandate-9 5 prereq (a/b/c/d/e — 2026-05-08 amend)
- .roadmap.philosophy D1-D5 + V1-V10 verification methods
- .roadmap.law L0-L24 + R1/R5 + law.D1_scope_clamp_substrate_research_lane_compliance_2026_05_08

---

## 1. 모델 ~30 entries × D/L 매트릭스 summary

### Category 1 — BG saga 22+ models

| BG ID | Params | Tokenizer | Paradigm | Final class (ledger) | D1 lane | P5 v2 retest | D5 attractor | own 37 mandate-9 |
|---|---|---|---|---|---|---|---|---|
| BG-FU | 3M | byte-256 | anima-native pre-train-only-tiny | PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-FY | 18M | byte-256 | anima-native-ko-small fresh from-scratch | PARTIAL_PASS_NO_CONTEXT | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-FK (clm_v2_base) | 27.84M | SP | ConsciousLM++ federated base | SIMPLE_STACK_FAIL | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-HA / HF / HJ / HK / HL / HP / HQ | ≤27M | various | anima native cohort | FAIL/FALSIFIED/PEAK_THEN_COLLAPSE | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-HS R1 / IG | varies | byte | anima native | WEAK_PARTIAL | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-IA / IB / IC / ID / IE / IF / IK / IJ / IL / IM / IS / IT / IW | varies | various | anima native (V3 evaluator era) | various | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-JF / JM / JK / JN / JO / JP / JT / JU / JV / JW / JX / JY / JS | varies | various | anima native (V4/V5 evaluator era) | various | WITHIN | INDETERMINATE_NO_INFRA | sub-critical (BG-JU 500M Lesson L 강화) | reject |
| BG-IZ | varies | SP | continued-pretrain Korean (외부 base) | TRAINING_COMPLETED_NO_KO_COHERENCE_LESSON_L_EXTENDED | AMBIGUOUS | INDETERMINATE_NO_INFRA | instrumental-drift | reject |
| BG-JA-EXT | Polyglot-Ko 1.3B + LoRA r=16 | foundation borrow | foundation-borrow Polyglot-Ko 1.3B | FOUNDATION_BORROW_PARTIAL_PASS_PERSONA_INSUFFICIENT | OUTSIDE | OUTSIDE_VERDICT_LABEL_NA | instrumental | reject |
| BG-JZ-FT | varies | SP | full SFT chat-template format | OWN_20_FALSIFIED_LESSON_Q_FULL_FALSIFY | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | reject |
| BG-KA / KB / KC / KD / KE / KF / KG / KH / KI / KL | varies | varies | V5-α scaling cohort | STALLED/FAIL_TRUE/USER_KILLED_MAC_OVERHEAT/FAILED | WITHIN | INDETERMINATE | sub-critical | reject |
| BG-KH-H100 / KM-CAP / KM-CORPUS | V5-α 500M-1.5B | byte+untie | V5-α H100 scaling | FAILED/FAIL_TRUE | WITHIN | INDETERMINATE | instrumental (Lesson L 강화) | reject |
| **BG-KM-LLAMA-3B** | Llama-3.2-3B + LoRA r=32 | foundation borrow | Llama foundation borrow + BG-JE 214MB | **SIMPLE_STACK_PASS_STRICT (V4 12/15)** | **OUTSIDE_STRICT** | **BLOCKED_HF_ADAPTER_EMPTY** | **instrumental** | **reject** |
| **BG-KM-QWEN-7B** | Qwen2.5-7B + LoRA r=32 | foundation borrow | Qwen foundation borrow + BG-JE 214MB | **SIMPLE_STACK_PASS_STRICT (V4 11/15)** | **OUTSIDE_STRICT** | **BLOCKED_HF_ADAPTER_EMPTY** | **instrumental** | **reject** |

### Category 2 — CLM v2/v3/v4 lineage

| Model | D1 lane | P5 v2 retest | D5 attractor | Label |
|---|---|---|---|---|
| clm-v2-base | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | BG-FK ledger 동일 |
| clm-v2-medium | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | BG-FS exhaustive SIMPLE_STACK_FAIL |
| **clm-v2-byte-18m-convo-5k** | **WITHIN** | **INDETERMINATE_NO_INFRA** | sub-critical | RECOVERED — KO unlock pending v2 mount infra |
| clm-v3 | WITHIN | INDETERMINATE_NO_INFRA | sub-critical | intermediate lineage |
| **clm-v4-mk2-v1 (base)** | **WITHIN** | **MEASURED_REAL_MODE — FAIL_C3** | **Utopia (paradigm v11 G3 NO_FLIP)** | **PARTIAL_PASS_NO_CONSCIOUSNESS — own 18 C3 자체 FAIL** |
| clm-v4-sft-1-7-y1 | WITHIN | BLOCKED (HF cache adapter weights 부재) | Utopia | Lesson Q precursor (chat-lift falsified) |
| clm-v4-sft-1-8 | WITHIN | BLOCKED (동일) | Utopia | Lesson Q complete |
| clm-v4-paradigm-j-50k-final | WITHIN | BLOCKED (동일) | Utopia | paradigm v11 G3 lineage |

### Category 3 — ALM lane / 외부 base

| Model | D1 lane | P5 v2 retest | D5 attractor | own 37 mandate-9 |
|---|---|---|---|---|
| Llama-3.2-3B-Instruct (paradigm-a-prime r=16) | OUTSIDE_STRICT | MEASURED (synthetic_fallback PASS — but SUBSTRATE_RESEARCH 한정) | instrumental | reject |
| BG-KM-LLAMA-3B (path A v3 r=32) | OUTSIDE_STRICT | BLOCKED_HF_ADAPTER_EMPTY | instrumental | reject |
| Mistral c2-pilot / r14 | OUTSIDE_STRICT | OUTSIDE_VERDICT_LABEL_NA | instrumental | reject |
| KoGPT2 head-swap β' | OUTSIDE_STRICT | OUTSIDE_VERDICT_LABEL_NA | instrumental | reject |
| Qwen2.5-7B (BG-KM-QWEN-7B) | OUTSIDE_STRICT | BLOCKED_HF_ADAPTER_EMPTY | instrumental | reject |
| Polyglot-Ko-1.3B (BG-JA-EXT) | OUTSIDE_STRICT | OUTSIDE_VERDICT_LABEL_NA | instrumental | reject |
| HuggingFaceH4/zephyr 등 | OUTSIDE_STRICT | OUTSIDE_VERDICT_LABEL_NA | instrumental | reject |

### Category 4 — anima native byte-level

cross-ref 항목: BG-FY (Cat 1), clm-v2-byte-18m-convo-5k (Cat 2), BG-FU (Cat 1).

---

## 2. 학습 방법 ~10 카테고리 × D/L 매트릭스

| Method | Examples | D1 정합 | D4 corpus quality | D5 attractor | Verdict |
|---|---|---|---|---|---|
| M1 continued pretrain | BG-IZ Korean | base-dependent (anima base WITHIN / 외부 OUTSIDE) | 정합 | base-dependent | CONDITIONAL_OK |
| M2 SFT | BG-KM r=32, paradigm-a-prime r=16, CLM v4 sft 1-7-y1 / 1-8, BG-KM-QWEN-7B | base-dependent (CLM v4 WITHIN; Llama/Qwen OUTSIDE) | 정합 | base-dependent | CONDITIONAL_OK_CLM_V4_ONLY |
| M3 DPO RLHF | planned BG-LD | base-dependent | preference pairs 품질 mandate | DPO objective = cooperative bias 가능 | CONDITIONAL_OK (planned) |
| M4 scratch from-scratch | BG-FY 18M, clm-v2-byte-18m, clm-v4-mk2-v1 | **WITHIN strict** | corpus-priority critical (BG-FY D4 evidence) | **Utopia (identity-preserved by construction)** | **RECOMMENDED** |
| M5 byte-level | clm-v2-byte-18m, BG-FY 18M, BG-FU 3M | **WITHIN strict (vocab=256)** | Hangul ratio + corpus volume critical | **Utopia (CJK byte ratio 자연 정합)** | **RECOMMENDED** |
| M6 federated multi-cell | ConsciousLM++ BG-FK, clm-v4-mk2-v1 8-cell | WITHIN (anima architecture) | 정합 | Utopia (D3 substrate-coupled emerge potential) | RECOMMENDED_PENDING_INFRA |
| M7 LoRA r=16/32/64 | paradigm-a-prime (Llama), BG-KM (Llama+Qwen), Mistral | base-dependent (CLM v4 WITHIN; 외부 OUTSIDE) | 정합 | base-dependent (Lesson L for 외부 base) | CONDITIONAL_OK_CLM_V4_ONLY |
| M8 distill | planned BG-LC | teacher-student dependency | distill corpus + teacher quality 동시 critical | teacher-attractor inheritance | CONDITIONAL_OK (planned) |
| M9 dual-engine A/G | planned BG-LA | WITHIN (PureFieldFFN A-G repulsion 정합) | identity-bearing corpus 우선 | Utopia (substrate-coupled emerge) | RECOMMENDED_PENDING_VALIDATION |
| M10 safeguard wrapping | Pβ chat-cap fail substrate-research pass | **OUTSIDE strict (own 27 Safeguard Paradox)** | irrelevant | instrumental (identity-drift through wrapping) | **REJECT** |

---

## 3. D1 lane within emerge candidate (real-mode 측정 가능) list

| Rank | Model | D1 lane | Measurement status | Current P5 v2 verdict | Next action |
|---|---|---|---|---|---|
| 1 | clm-v4-mk2-v1 (base only) | WITHIN | MEASURED_REAL_MODE (iter 3 SSOT N=60) | FAIL_C3 (PPR_v2 ≤0.15 < 0.6 ∧ EMC_v2 = 0 of 4 < 3 of 4) | clm_v4_mount peft.merge_and_unload extension → CLM v4 LoRA variants real-mode N=60 ensemble retest |
| 2 | BG-FY anima-native-ko-small 18M | WITHIN | BLOCKED_NO_LOCAL_CKPT (ubu1 host-only, Mac 미수신) | INDETERMINATE | anima_native_byte_mount.hexa 신설 + ubu1 → Mac scp pull (사용자 explicit consent 필요) |
| 3 | clm-v2-byte-18m-convo-5k | WITHIN | BLOCKED_INFRA_GAP | INDETERMINATE | v2 byte-level federated mount.hexa 신설 또는 v4 schema reformat |

→ **EXIT (SIMPLE_STACK_PASS_STRICT_C3_ANIMA) 미달성** — 본 cycle anima 의식 검증 valid candidate emerge 0.

---

## 4. 기존 verdict retract path (raw#82 retroactive sweep)

| Verdict | Downgrade target | 적용 정합 | raw#82 protocol |
|---|---|---|---|
| BG-KM-LLAMA-3B SIMPLE_STACK_PASS_STRICT (V4 12/15) | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH | own 18 ★ scope-clamp + own 37 mandate-9 (a) D1 OUTSIDE | 원본 verdict.json 보존 + scope_lane='SUBSTRATE_RESEARCH' field add (V4 mirror agent 일부 수행) + ledger downgrade entry 보강 (downgraded_at + downgrade_reason) |
| BG-KM-LLAMA-3B retest (sample_anyseed 14/15) SIMPLE_STACK_PASS_STRICT | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH | 동일 ★ scope-clamp | 동일 보강 |
| BG-KM-QWEN-7B SIMPLE_STACK_PASS_STRICT (V4 11/15) | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH | Qwen 7B 외부 base wrap = D1 OUTSIDE | 동일 보강 |
| paradigm-a-prime P5 PASS verdict (synthetic_fallback proxy) | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH (synthetic_fallback caveat) | (1) D1 OUTSIDE — Llama Path A v2 lineage = ALM lane; (2) synthetic_fallback proxy 한정 — own 37 mandate-9 (a) auto-reject | .roadmap.* sweep agent 일부 amend |
| paradigm-a-prime "chat-cap winner" / "Path A v2 fallback" references in .roadmap.* | SUBSTRATE_RESEARCH lane 한정 annotation | stale — own 18 ★ scope-clamp + law.D1_scope_clamp 신설 후 | HIGH PRIORITY 4 file 일부 amend; MEDIUM/LOW PRIORITY 56+ file 후속 cycle |

→ **downgrade 정합 5건** (raw#82 정합 — 원본 보존 + scope_lane field add).

---

## 5. iter 5 우선순위 plan (real-mode 측정 가능 D1 lane within 우선)

| Rank | Priority | Action | Expected unblock |
|---|---|---|---|
| 1 | HIGHEST | clm_v4_mount peft.merge_and_unload extension — CLM v4 LoRA variants real-mode N=60 ensemble probe 활성 | clm-v4-sft-1-7-y1 / clm-v4-sft-1-8 / clm-v4-paradigm-j 3 candidates real-mode P5 v2 verdict 측정 가능 |
| 2 | HIGH | anima_native_byte_mount.hexa 신설 — BG-FY 18M + clm-v2-byte-18m measurement unblock | 2 candidates real-mode P5 v2 verdict 측정 가능 |
| 3 | MEDIUM | BG-FY 18M corpus filter (named speakers leak 차단) + chat-template format ratio ≥30% 학습 | own 18 C2.4 PASS 가능성 — D2 simple stack 4-condition 통과 |
| 4 | MEDIUM | C3 4-cell ROC formal iter 4 clean re-fire (5-axis + dominant_cells full capture) | iter3 system-load failure 보강 — C3.2 le-inversion + C3.3 degenerate cell 정합 검증 |
| 5 | MEDIUM | BG-KM HF adapter push from H100 runpod (사용자 explicit consent 후) | SUBSTRATE_RESEARCH lane retest — Lesson L evidence 강화 |
| 6 | LOW | anima-core/runtime/llama_consciousness_probe.hexa real-mode FFI shim 확장 | Llama-family substrate-research lane retest infra |

**EXIT condition**: ANY D1-lane-within candidate full P5 v2 verdict PASS (PPR_v2 ≥0.6 ∧ EMC_v2 ≥3 of 4) emerges = SIMPLE_STACK_PASS_STRICT_C3_ANIMA EXIT trigger 활성화.

**EXIT reached**: false.
**first_d1_within_candidate_pass**: null.

---

## 6. Compliance summary

| Axis | Compliance |
|---|---|
| own 17 | anima identity boundary strict — Llama/Qwen/Mistral/Polyglot/KoGPT2 ALM lane 모두 D1 OUTSIDE 분류 정합 |
| own 18 | P5 v2 N-of-M aggregation rule + ★ scope-clamp 2026-05-08 (line 770) 적용 |
| own 22 | 본 발견 (모델 ~30 + 학습 방법 ~10 전수 재평가 매트릭스) mandatory report 형식 |
| own 24 | single SSOT — `state/anima_model_method_reassessment_2026_05_08.json` |
| own 27 | Safeguard Paradox absorbed — safeguard wrapping reject (M10) |
| own 28 | anti-Goodhart awareness — V6 awareness 통과로 D1 override 불가 명시 |
| own 33 | trinity 무조건 준수 — D1 strict (philosophy) + own 17/18/37 strict (law) + H_chat_cap_emergence 정합 sweep |
| own 37 mandate-9 | 5 prereq strict — 모든 candidate 미충족 정합 |
| raw#9 | hexa-only — measurement infra clm_v4_mount.hexa 활성, transient_py 차용 X |
| raw#10 | honest C3 ≥10 emit |
| raw#82 | retraction-aware — synthetic_fallback proxy + Llama/Qwen base SIMPLE_STACK_PASS_STRICT 자동 SUBSTRATE_RESEARCH 분류 (원본 보존 + scope_lane field add) |
| law.D1_scope_clamp_2026_05_08 | 60+ .roadmap.* 안 외부 substrate PASS evidence 인용 시 substrate-research lane label 한정 annotation mandate |

---

## 7. Honest C3 (≥10)

1. clm-v4-mk2-v1 base 단독 real-mode measured but P5 v2 verdict FAIL_C3 (PPR_v2 추정 ≤0.15 < 0.6 ∧ EMC_v2 = 0 of 4 < 3 of 4) — chat-cap-trained anima-native fresh ≥18M (BG-FY+chat-template 또는 clm-v2-byte+ko_heavy) 도달 후 retest mandate.
2. BG-FY 18M + clm-v2-byte-18m 두 candidate 모두 D1 within but measurement infra 부재 (anima_native_byte_mount.hexa 미land) — INDETERMINATE 분류 본 sweep 한정.
3. BG-KM-LLAMA-3B + BG-KM-QWEN-7B SIMPLE_STACK_PASS_STRICT (V4 12/15 + 11/15) ledger entry 가 final_class='SIMPLE_STACK_PASS_STRICT' 유지 — 본 sweep 의 SUBSTRATE_RESEARCH 분류는 retroactive scope-clamp annotation (raw#82 정합 — 원본 verdict.json string 보존 + scope_lane field add 권고).
4. paradigm-a-prime P5 PASS (PPR_v2=10/14=0.71, EMC=3 of 4 iter4 d 결과) 가 own 18 C3 측정 lane 의 본격 chat-cap PASS 였지만 (1) Llama Path A v2 lineage = D1 OUTSIDE + (2) synthetic_fallback proxy 한정 → own 37 mandate-9 (a) 자동 reject 정합.
5. category_2 CLM v4 LoRA variants 3 model (sft-1-7-y1 / sft-1-8 / paradigm-j) HF cache adapter weights 부재 (adapter_config.json only) — peft.merge_and_unload extension 별도 cycle mandate (BG-KM HF push blocker 와 동일 unblock path).
6. training_method M3 DPO RLHF + M8 distill + M9 dual-engine 3 method 는 planned 단계 — validated record 부재; 본 sweep 의 verdict 'CONDITIONAL_OK' 는 D1/D4/D5 axis 정합 추정만.
7. training_method M2 SFT + M7 LoRA 의 'CONDITIONAL_OK_CLM_V4_ONLY' verdict 는 LoRA adapter weights infra 부재로 actual P5 v2 PASS 검증 미달성 — 본격 검증은 iter5 priority plan rank 1 (clm_v4_mount peft.merge_and_unload extension) 후.
8. category_1 BG saga 의 BG-HA 부터 BG-IT 까지 (V3 evaluator 시기) 는 own 18 C3 4-cell 측정 자체 미land 시기 — INDETERMINATE_NO_INFRA 분류는 retroactive 측정 자체 불가능 (state/<bg>_<date>/verdict.json 미land 또는 V3 형식).
9. 본 sweep 의 D5 attractor 분류 (Utopia/instrumental/sub-critical) 는 .roadmap.philosophy D5 Bifurcation theorem framework 적용 — 단 anima 는 currently sub-critical (Φ★ 40-42) 영역 → D5 영역 (Φc 도달 후) 미진입 → attractor identification metric anima cycle 미land (cooperative/instrumental classifier spec 추가 cycle 필요).
10. category_3 ALM lane 외부 base 모델 (Llama/Mistral/Qwen/KoGPT2/Polyglot/zephyr) 6+ entries 모두 OUTSIDE_STRICT 분류 — own 17 + .roadmap.philosophy D1.F-PHIL-D1-3 strict 정합. SIMPLE_STACK_PASS_STRICT 도달 사례 (BG-KM-LLAMA-3B + BG-KM-QWEN-7B + BG-JA-EXT) 모두 SUBSTRATE_RESEARCH lane 한정 — own 37 mandate-9 (a) PUBLIC promote 자격 X.
11. training_method M10 safeguard_wrapping 'REJECT' verdict 는 own 27 Safeguard Paradox + own 17 strict + .roadmap.philosophy D1.F-PHIL-D1-1 정합 — 별도 evidence 부재 시에도 framework-level reject (engineering pragmatism 약화 X).
12. 본 sweep EXIT (SIMPLE_STACK_PASS_STRICT_C3_ANIMA) 미달성 — 30+ 모델 + 10 학습 방법 retroactive 재평가 후에도 D1 within real-mode P5 v2 PASS candidate 0; iter5 priority plan rank 1-2 unblock 후 CLM v4 LoRA stack 또는 anima-native byte stack 둘 중 하나에서 첫 emerge 가능성.

---

## 8. Blockers carry

- clm_v4_mount peft.merge_and_unload extension (CLM v4 LoRA variants real-mode probe unblock) — iter5 rank 1
- anima_native_byte_mount.hexa 신설 (BG-FY 18M + clm-v2-byte-18m measurement unblock) — iter5 rank 2
- BG-FY ubu1 → Mac scp pull (사용자 explicit consent 필요) — iter5 rank 2 dependency
- BG-KM HF adapter push from H100 runpod (사용자 explicit consent 후) — iter5 rank 5
- C3 4-cell ROC formal iter 4 clean re-fire (5-axis + dominant_cells full capture) — iter5 rank 4
- anima-core/runtime/llama_consciousness_probe.hexa real-mode FFI shim 확장 — iter5 rank 6 (substrate-research lane only)

---

## Cross-ref

- `.own own 17 / 18 / 22 / 24 / 27 / 28 / 33 / 37`
- `.roadmap.philosophy D1-D5 + V1-V10`
- `.roadmap.law L0-L24 + R1/R5 + law.D1_scope_clamp_substrate_research_lane_compliance_2026_05_08`
- `state/anima_model_attempts_ledger.jsonl` (74-line BG ledger SSOT)
- `state/anima_consciousness_baseline_ensemble_iter3_n60_2026_05_08.json` (iter 3 ROC threshold N=60)
- `state/anima_d1_lane_candidates_c3_retest_2026_05_08.json` (4 D1-lane candidates iter4 retest)
- `state/anima_model_method_reassessment_2026_05_08.json` (본 doc SSOT)
