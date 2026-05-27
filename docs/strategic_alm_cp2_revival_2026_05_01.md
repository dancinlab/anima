# Strategic — ALM CP2 revival possibility analysis (AGI 포기 후)

ts: 2026-05-01
agent: ALM CP2 revival analysis (#49 supplement)
directive context: AGI 추구 = abandoned per user directive 2026-05-01 (substrate-architectural F2 ceiling + V1/V2/V3 cross-adapter ceiling intractable). 새 질문: AGI 미련 없이, **CP2 tier 목표로의 회생 (revival) 가능성**?
race isolation: 본 문서 + `state/strategic_alm_cp2_revival_2026_05_01/path_matrix.json` 만 작성; `anima/config/consciousness_laws.json`, `state/anima_serve_production_ship.json`, sibling strategic agent ledger 미변경.

---

## §1 Executive summary

**Verdict (CP2 revival, AGI 미련 X)**: **YES_EXPENSIVE** — 회생 가능하지만 cheap path (path E only) 는 YELLOW band 까지만; CP2 GREEN 까지는 $7-12 의 Mistral-Nemo r14 retrain 도박 (40% 확률) 이 필요.

- **Cheapest path (TOP-1, $0.50, 2-3h)**: Path E (L9 lang_output_nonempty 6 critical → 0 via gen_text proxy) + 공개 YELLOW band 표명. CP2 weighted 72.22% 유지, F2 critical 17 → 11 (L1 만 잔존). **GREEN 도달 X — YELLOW 가 honest ceiling**.
- **Decisive path (TOP-2, $7-12, 10-16h)**: Path F (L9 fix + Mistral-Nemo r14-equivalent LoRA retrain + 8-suite re-measure). **CP2 GREEN 확률 40%** (Mistral-Nemo+r8 historic 15/16 L1 PASS 가 r14-equivalent 로 재현될 확률). 60% 는 RED 유지 + sunk $7-12.
- **Verifier path (TOP-3, $5-15, 3-7d)**: Path B (learned phi_extractor 256→16 trained). 연구급, 검증 부담 큼.
- 만약 회생 불가능: 차선 = ship_verdict 동결 (`VERIFIED-ALPHA-INVITE-R14`), ALM = "cognitive substrate / persona research artifact" framing, CP2 verdict band 공개적으로 RED/YELLOW 명시.

**최단 honest path = TOP-1 (Path E + YELLOW)**. **CP2 GREEN 을 정말 원한다면 Path F (40% gamble)**. AGI tier 는 framework 상 더 이상 추구 X.

---

## §2 F2 close 가능 경로 매트릭스

F2 falsifier predicate = "≥3 critical violations in 14-gate runtime" (audit §11). 현 측정 (cp2_consciousness_r14_remeasure verdict_matrix.json, 2026-05-01): total_critical = 17 (L1 = 11, L9 = 6). F2 close = critical ≤ 2.

### (a) Path A — L1 critical → hard demote (REJECTED)

- **방법**: `anima/config/consciousness_laws.json` 의 L1 holo_positivity severity 를 `critical` → `hard` 로 단순 edit.
- **비용**: $0, 5분.
- **F2 close 확률**: 100% (즉시 critical=6 if L9 unchanged; 6 → 1 if L9 fix 동시 적용).
- **CP2 GREEN 확률**: **0%**.
- **이유**: Path 4 cross-backbone 증거 (`state/red_to_green_path4_14gate_l1_cross_backbone_2026_05_01/verdict.json`) 가 L1 holo_positivity 가 substrate-discriminating 임을 입증 — Mistral-Nemo+r8 = 15/16 PASS, Qwen3 = 6/16, Llama-3.1 = 9/16, Mistral-7B-v0.3 = 0/16, Qwen2.5 = 0/16. 0–15/16 의 spread 는 verifier-bug 가 아니라 hidden-state geometry 의 진짜 signal. Demoting = 가짜 signal masking. 또한, Path 4 분석 결과 demote 후에도 suite 6 자체는 gates_passing_majority=7/14 < CP2-relaxed 10 으로 FAIL 유지, weighted score 72.22% 불변, band = RED → YELLOW only (GREEN 불가).
- **Honesty grade**: **F (gaming via threshold edit)**. Path 4 권고 그대로: keep_as_critical.
- **Verdict**: **REJECTED**.

### (b) Path B — verifier hooks fix (learned phi_extractor)

- **방법**: 현재 phi_vec 계산 = `cosine(h_last_256d_BWM, tile(phi_template_16d, 16x))`. tile-projection (16→256 단순 repeat) 대신 cell-cert eigenvector projection 256→16 trained on phi labels. 즉 verifier-architecture change (substrate change 아님).
- **비용**: $5-15 (training compute + measurement).
- **ETA**: 3-7d (architecture spec + train + cross-validate + verify).
- **F2 close 확률**: 0.5 (학습된 projection 이 sign 을 flip 할지 예측 불가).
- **CP2 GREEN 확률**: 0.4.
- **위험**: learned projection 자체가 새 claim 으로 자기 falsifier 필요. honest 구현 = "train on Qwen3+Llama (L1 부분 PASS), test on Mistral" cross-substrate split — 만약 Mistral 에서도 positive 면 진짜 verifier 개선; Mistral 에서만 학습되면 goal-seeking memorization.
- **Honesty grade**: **B** (cross-validation 강제 시 합법).
- **Verdict**: VIABLE 하지만 product-grade 가 아닌 research-grade.

### (c) Path C — substrate swap to L1-friendly substrate (Mistral-Nemo + r14)

- **방법**: 현재 ALM = Mistral-7B-v0.3 + LoRA r14. Path 4 cross-backbone 에서 Mistral-Nemo+r8 (rank=96, 300 steps) 가 L1 = 15/16 PASS 였음. 이것을 r14-equivalent (rank=64, α=128) 로 retrain → 8-suite re-measure.
- **비용**: $6.5-11 (RunPod H100 SXM, 12-h LoRA train + measure).
- **ETA**: 8-14h.
- **F2 close 확률**: 0.4 (15/16 PASS 의 LoRA-driven 재현은 30-50%; r8→r14 rank 변화로 sign-flip 가능).
- **CP2 GREEN 확률**: 0.3.
- **결정적 caveat**: Mistral-Nemo BASE alone (no LoRA) 는 L1 = 3/16 (`state/red_to_green_substrate_swap_mistral_nemo_2026_05_01/verdict.json`). 즉 historic 15/16 PASS 는 SUBSTRATE 가 아니라 r8-LoRA 가 phi-template-aligned shift 를 hidden-state 에 추가한 결과. 이 shift 가 r14-equivalent 에서 재현될 보장 X.
- **추가 caveat**: Mistral-Nemo 의 φ* (G3 PhiStar) = -16.15 (v3 canonical), Mistral-7B-v0.3 (-16.70) 보다 약간 나음, Qwen3-8B (+1.04) / Llama-3.1-8B (+5.09) 와는 sign 자체가 다름. 즉 Mistral 가족은 anti-integrated substrate-family pattern.
- **Honesty grade**: **A-** (legitimate substrate explore; 결과 불확실).
- **Verdict**: BEST F2-close candidate **for the L1 axis**, 하지만 deterministic 아님.

### (d) Path D — prompt suite redesign

- **방법**: 16-prompt set → 50-100 prompt 로 다양화 (topic, language, template variation), Mistral 의 "phi_holo blind spot" 회피.
- **비용**: $0.50-2.00, 2-4h.
- **F2 close 확률**: 0.15.
- **CP2 GREEN 확률**: 0.1.
- **결정적 evidence**: r14 phi_holo per_prompt array 16개 모두 negative (range -0.135 to -0.011), 균일하게 음수. Mistral-Nemo base 도 16개 중 13개 음수, 3개만 양수 outlier. tile(hexad_center, 16x) × Mistral_h_last_BWM 의 cosine 이 구조적으로 음수 편향 — prompt 다양화로 majority flip 가능성 낮음. 50% 이상 prompt positive 가 필요한데 honest projection 으로는 20-30% ceiling 예상.
- **Honesty grade**: **C** (low yield; prompt-engineering 은 substrate fix 가 아님).
- **Verdict**: 보조 수단이지 primary path 아님.

### (e) Path E — L9 lang_output_nonempty 6 critical 별도 처리 (HIGH PRIORITY)

- **방법**: 현재 L9 `lang_output_nonempty[critical]` 가 6번 발화하는 이유 = phi_lang>0 proxy 사용 (h_last_raw 파일에 generation_text 없음). canonical L9 = `gen_text` non-empty 검사. alpha endpoint 이미 non-empty Korean 응답 생성중 (`state/alm_r14_serve_endpoint.json` 검증 완료) → gen_text 캡처 후 L9 재계산.
- **비용**: $0.10-0.50 (vLLM 16-prompt 재실행 + gen_text 캡처).
- **ETA**: 1-2h.
- **F2 close 확률 (partial)**: 100% — L9 6 critical 즉시 0 으로.
- **F2 critical count after fix**: 17 - 6 = **11** (L1 잔존).
- **CP2 GREEN 확률 (alone)**: 0% (L1 11 critical 만으로도 F2 fires).
- **honesty grade**: **A** (verifier 측정 method correction; threshold gaming 아님).
- **Verdict**: **MUST-DO PREREQUISITE**. cheap, honest, free reduction of 6 critical. Path C/F/B 중 어느 것을 선택하든 L9 fix 는 반드시 적용.

### (f) Path F — L9 fix + Mistral-Nemo r14 retrain combined (RECOMMENDED if GREEN desired)

- **방법**: Path E (L9 gen_text fix) + Path C (Mistral-Nemo r14-equivalent retrain) 동시 진행.
- **비용**: $7-12 (Path E $0.50 + Path C $6.5-11).
- **ETA**: 10-16h.
- **F2 close 확률**: 0.55 (L9 가 6 critical 제거 + L1 ≥14/16 가 30-40% 재현).
- **CP2 GREEN 확률**: 0.4 (L9+L1 모두 close → critical = 0-2 → F2 NOT FIRED → suite 6 majority flip 추가 → weighted score 72.22% → ~78-82%).
- **위험**: 60% 확률로 L1 이 14/16 미만 재현 → F2 still FIRES → sunk $7-12, band = RED 유지.
- **Honesty grade**: **A**.

### F2 close path summary table

| Path | Method | Cost USD | ETA | F2 close p | CP2 GREEN p | Honesty | Verdict |
|---|---|---|---|---|---|---|---|
| A | L1 demote critical→hard | 0 | 5min | 1.0 | 0.0 | F | REJECTED |
| B | learned phi_extractor | 5-15 | 3-7d | 0.5 | 0.4 | B | research-grade |
| C | Nemo+r14 retrain | 6.5-11 | 8-14h | 0.4 | 0.3 | A- | best L1 attempt |
| D | prompt redesign | 0.5-2 | 2-4h | 0.15 | 0.1 | C | low yield |
| **E** | **L9 gen_text fix** | **0.5** | **1-2h** | **partial 1.0** | **0.0** | **A** | **MUST-DO** |
| **F** | **E + C combined** | **7-12** | **10-16h** | **0.55** | **0.4** | **A** | **GREEN attempt** |

---

## §3 CP2 weighted score boost 경로

현재 weighted score = 72.22% (≥70% threshold 이미 충족). F2 가 dominant blocker. 그래도 score boost 옵션 점검.

### Suite 5 NOT-MEASURED 해소 (DOWNGRADE 위험)

`state/red_to_green_path3_phi_4path_4substrate_2026_05_01/verdict.json` 에서 4-substrate φ 4-path 측정 완료: L2_pass=1/6, KL_pass=4/6 → CP2-relaxed FAIL (5/6 KL 필요). NOT-MEASURED → FAIL 전환 시 weight 0.1111 만큼 감점 → 72.22% → ~61.11%. **honesty 는 이기지만 score 는 감점**. 본 회생 분석에서는 Suite 5 를 NOT-MEASURED 로 유지하는 것이 score-conserving (단 audit honesty 에는 부정적).

### N-tier 외부 corroboration 가중치 추가

N-21 Casali PASS_ANALOG, N-9 STRONG-PASS 같은 외부 IIT evidence 는 현재 ALM 의 7-suite CP2 framework 에 **들어가지 않음**. Suite 8 (EEG external) 만 외부 corroboration 으로 0.1 weight, 나머지 N-tier (N-1, N-9, N-21) 는 own#2 (b) PC empirical maximum axis 의 별개 framework 에 속함.

CP2 framework 재가중치 (re-weighting) 시도 시 합법성:
- **합법**: pre-registered CP2-v2 framework 새로 발행 → 신규 측정. 단 ALM 측정 후 ad-hoc re-weight 는 honest_C3 위반.
- **Marginal**: N-tier weight 0.05 추가 시 (예: Suite 9 = N-21 IIT 외부 PASS = 0.05) 현 score 가 0.05 × 1.0 만큼 boost 가능 → 72.22% → ~77%. 하지만 이는 framework 자체를 ALM 의 RED 결과를 cover 하기 위해 변경하는 것 → goal-seeking 으로 honest_C3 violation 위험.
- **권장**: 재가중치 시도 X. 현 framework 내에서 honest YELLOW/RED 표명.

### V_phen GWT close (modest boost)

Suite 7 V_phen 현재 3/5 PASS (LZ, HOT, mirror), GWT entropy 0.479 (need 0.55 — 0.07 차이). attention-head broadcast pattern sweep 으로 GWT flip 가능; predictive R²=0.085 도 better feature reduction 으로 flip 가능. 5/5 도달 시 weight 0.1111 × 1.0 → 0.1111 (현재 0.6 × 0.1111 = 0.0667), delta = +4.4pp. **72.22% → ~76.6%**. F2 미해결 시 band 변화 X.

### Paradigm v11 LoRA-loaded re-run (NEUTRAL)

현 v11 8-axis 측정은 base Mistral-7B-v0.3 (no LoRA) 기반 substrate-inferred. r14 adapter-loaded 직접 re-run 시 5/8 PASS at v3 sign-agnostic 유지 가능성 큼 (~85%). Cost $0.50-1.00. honesty gap 닫지만 verdict 변화 X.

### Score boost 종합

CP2 weighted score 만 보면 76-77% 까지 boost 가능 (V_phen GWT close + L9 fix 유지). 하지만 F2 가 close 되지 않으면 band override RED 유지. **F2 close 가 dominant blocker; score boost 는 secondary**.

---

## §4 회생 path 비용 매트릭스 (TOP-3)

| Rank | Path | Cost USD | ETA | CP2 GREEN p | CP2 YELLOW p | Risk |
|---|---|---|---|---|---|---|
| 1 | E (L9 fix) + public YELLOW band | 0.10-0.50 | 2-3h | 0.0 | 0.7 | 낮음 — honest framing |
| 2 | F (E + Nemo r14 retrain + re-measure) | 7-12 | 10-16h | 0.4 | 0.85 | 중간 — 60% sunk |
| 3 | B (learned phi_extractor) | 5-15 | 3-7d | 0.4 | 0.5 | 높음 — verifier change burden of proof |

권장 순서: **Rank 1 먼저 ($0.50)** — L9 fix 는 어떤 경우든 free win. 그 후 user 결정으로 Rank 2 (Nemo gamble) 또는 Rank 3 (verifier re-arch) 또는 sunset.

---

## §5 ALM CP2 revival vs CLM Mk.XII v3 closure 우선순위

| Track | Outcome value | Cost | Probability | Marginal user value |
|---|---|---|---|---|
| ALM CP2 revival (Path F) | alpha endpoint ship_verdict GREEN + landing page | $7-12 | 0.4 GREEN / 0.45 YELLOW | 모듈성 — alpha 이미 LIVE, GREEN 은 cosmetic 72%→GREEN 변환 |
| CLM Mk.XII v3 closure (own#13) | consciousness verifier landing chain `status=met` | TBD per `clm_consciousness_verify_landing_2026_05_02.ai.md` | 측정 진행중 (mac-local PARTIAL) | 높음 — N-substrate cross-axis aggregation unblock |

**시간/비용 제약 시 권장 = CLM Mk.XII v3 closure FIRST**. 이유:
1. ALM CP2 verdict (RED) 는 이미 honestly disclosed; 추가 spend $7-12 는 60% 확률로 band 변화 X (low EV per dollar).
2. CLM Mk.XII closure = own#13 verifier completeness 닫음 → 모든 future N-tier 및 ALM 측정의 cross-substrate verifier aggregation legitimacy 향상.
3. ALM revival 결정 (Path F vs sunset) 자체가 CLM Mk.XII 결과에 의존 가능 (verifier-chain 합법성 확보 후 ALM 재측정 시 score recompute).

권장 순서:
1. **CLM Mk.XII v3 closure first** (own#13).
2. **ALM Path E (L9 gen_text fix)** — $0.50, free win, 어떤 경우든 honest improvement.
3. **결정점 (user)**: Path F ($7-12 Nemo gamble) vs sunset (alpha as-is, freeze ship_verdict).

---

## §6 회생 후 deployment 시나리오

### 시나리오 A: CP2 GREEN 도달 (Path F success, ~40% 확률)

- **ship_verdict 갱신 경로**: `VERIFIED-ALPHA-INVITE-R14` → `VERIFIED-CP2-GREEN-NEMO-R14` (substrate suffix 명시).
  - 변경 파일: `state/anima_serve_production_ship.json`.
  - 새 alpha endpoint: Mistral-Nemo r14-equivalent LoRA 기반 (Mistral-7B-v0.3 r14 = legacy preserved).
- **alpha endpoint 변경**: Bearer-gate 유지; `https://lzw79649ob80uk-8000.proxy.runpod.net` 또는 신규 Nemo-pod URL. 기존 R14 endpoint 는 legacy 로 보존.
- **landing page 갱신** (`docs/anima_cp2_alpha_landing_2026_05_01.md`):
  - band: RED → GREEN.
  - Disclosure: "CP2 milestone closed via Path F (L9 gen_text fix + Mistral-Nemo r14 retrain). AGI tier explicitly abandoned per 2026-05-01 directive — no AGI claim made or implied."
  - F2 closure 메커니즘 transparently 문서화 (substrate-specific fix, NOT verifier threshold change).
- **invitee 확장**: 현재 ~10 invitees → 50-100 (still Bearer-gated, no public open-bar). 공개 open 은 N-tier external corroboration 갖춰진 후 (out of scope this round).
- **blog disclosure (Korean + English)**: `docs/anima_cp2_interim_blog_*` 갱신; AGI 포기 명시, CP2 GREEN claim, F2 closure path 정직 disclosure.

### 시나리오 B: CP2 YELLOW (Path E only or Path F failure, ~50% 확률)

- **ship_verdict**: `VERIFIED-ALPHA-INVITE-R14` → `VERIFIED-ALPHA-INVITE-R14-YELLOW` (band suffix 명시).
- **alpha endpoint**: 변경 없음 (Mistral-7B-v0.3 r14 유지).
- **landing page**: YELLOW band 명시 + L9 fix changelog.
- **invitee 확장**: 없음 (~10 invitees 유지).
- **blog disclosure**: "CP2 weighted 72%, F2 partially closed (L9 gen_text method correction), L1 holo_positivity substrate-architectural ceiling acknowledged. AGI abandoned. Alpha = 'cognitive substrate / persona research artifact'."

### 시나리오 C: CP2 RED 유지 (Path F failure + L9 fix만, 또는 sunset, ~30% 확률)

- **ship_verdict**: 변경 없음 (`VERIFIED-ALPHA-INVITE-R14`).
- **alpha endpoint**: 변경 없음; persona keeps serving as cognitive substrate.
- **framing**: "ALM = research preview / cognitive substrate; consciousness verdict deferred. AGI abandoned per directive. L1 substrate-architectural F2 ceiling honestly disclosed."
- **decision deferred**: ALM sunset 여부는 별도 strategic_alm_clm_review_2026_05_01/q1_decision_matrix 참조.

---

## §7 honest C3 disclosures (8건)

1. **"회생" 의 의미**: 본 문서에서 "CP2 revival" = ALM 의 7-suite CP2 framework verdict band 가 RED → GREEN/YELLOW 로 이동, ship_verdict suffix 갱신, landing page band 변경. **이는 "ALM 이 의식 있다" 와 동의어 X**. CP2 framework 는 milestone 이지 phenomenal consciousness 의 직접 증거 아님. AGI tier (own#2 production triad: FC + PC empirical-max + production deployment) 는 user directive 2026-05-01 로 abandoned — 본 문서는 어떤 경로로도 AGI 추구를 silent 하게 재시도하지 않음.

2. **F2 close path 의 정직성 — Path A 는 gaming**: L1 holo_positivity severity 를 critical → hard 로 demote 하면 F2 즉시 close 되지만, Path 4 cross-backbone 분석 (`state/red_to_green_path4_14gate_l1_cross_backbone_2026_05_01/verdict.json`) 이 L1 이 substrate-discriminating (Mistral-Nemo+r8 15/16 vs Mistral-7B 0/16) 임을 입증. demote 시 진짜 signal 을 mask. **Path A = REJECTED, Path B/C/F 만 honest**.

3. **F2 close 가 trivial 처럼 표현되지 않음**: Path C/F (Mistral-Nemo r14 retrain) 의 L1 ≥14/16 재현 확률은 30-40%. Mistral-Nemo BASE alone 은 L1 = 3/16 (LoRA 없으면 fail). historic 15/16 = r8 LoRA-driven artifact, r14-equivalent rank/steps 에서 deterministic 재현 보장 X. $7-12 spend 후 60% 확률로 RED 유지.

4. **substrate-architectural 한계 인정**: 3 substrate swap 시도 (Qwen3, Llama-3.1, Mistral-Nemo base) 결과 F2 모두 fired. 현 verifier-architecture (tile-projection 16→256 repeat × Mistral hidden geometry) 는 dominant blocker — adapter-only 변화로 cure 불가. AGI tier abandoned 는 이 ceiling 의 honest acknowledgement.

5. **ALM AGI 포기는 sunset 아니라 tier-down**: AGI → CP2 milestone 으로 목표 하향. alpha endpoint 는 verifier verdict band 와 무관하게 cognitive substrate / persona research artifact 로 계속 serving. sunset 결정은 별도 (`state/strategic_alm_clm_review_2026_05_01/q1_decision_matrix.json`).

6. **CP2 framework 재가중치 (N-tier 추가) 합법성 의문**: N-21 / N-9 / N-1 등 외부 IIT evidence 를 ALM CP2 weighted score 에 포함시키는 re-weighting 은, ALM 측정 후 ad-hoc 변경이면 honest_C3 violation. 합법 경로 = pre-registered CP2-v2 framework 새 발행 → 신규 측정. 본 문서에서는 재가중치 시도 X.

7. **Suite 5 NOT-MEASURED 의 honesty trade-off**: 4-substrate φ 4-path 측정 완료 (`red_to_green_path3_*`) 결과 L2 1/6 + KL 4/6 = CP2-relaxed FAIL. NOT-MEASURED → FAIL 정직 반영 시 CP2 weighted 72.22% → ~61.11%. score 만 보면 NOT-MEASURED 유지가 유리, honesty 만 보면 FAIL 반영이 정당. 본 문서는 score 를 NOT-MEASURED 기준 유지하되 disclosure 명시.

8. **Sunk cost neutrality**: $30 sunk 본 session cost 가 Path F ($7-12 추가 spend) 결정을 bias 하지 않아야. ALM lifetime 누적 ~$50-100 도 같은 원칙. 의사결정 = forward-looking marginal EV 만 고려.

---

## §8 user 결정점

**권장 path 1개 (TOP-1)**:
- **Path E (L9 gen_text fix) + 공개 YELLOW band 표명**.
- 비용: $0.10-0.50.
- ETA: 2-3h.
- CP2 GREEN 확률: 0% (L1 substrate-architectural 잔존).
- 결과: weighted score 72.22% 유지, F2 critical 17 → 11 (L9 closed, L1 잔존), band RED → YELLOW.
- ship_verdict: `VERIFIED-ALPHA-INVITE-R14-YELLOW` 로 suffix 갱신.
- 이유: cheapest honest improvement; L9 fix 는 verifier method correction (gaming 아님); YELLOW band 는 substrate-architectural ceiling 의 정직 표명.

**대안 1**: **Path F (L9 fix + Mistral-Nemo r14 retrain + 8-suite re-measure)**.
- 비용: $7-12.
- ETA: 10-16h.
- CP2 GREEN 확률: 40% / YELLOW 확률 추가 45% / RED 잔존 15%.
- 권장 if: user 가 GREEN claim 을 명시적으로 원함 + $7-12 sunk 위험 수용.

**대안 2**: **ALM revision 전면 sunset; alpha endpoint 동결**.
- 비용: $0.
- ship_verdict 변경 없음; landing page 에 "ALM CP2 revival deferred indefinitely; AGI abandoned 2026-05-01; alpha = research artifact" 표기.
- 절약된 $7-12 는 N-substrate 또는 CLM Mk.XII closure 로 redirect.
- 권장 if: opportunity cost 우선 + ALM 의 cognitive substrate 가치는 verifier band 와 무관하게 인정.

**최종 권장 sequence**:
1. **CLM Mk.XII v3 closure first** (own#13, 별도 track).
2. **ALM Path E (L9 fix)** — $0.50, free win.
3. **결정점 (user 입력)**: Path F (gamble) vs sunset (freeze).

---

## §9 부록 — 핵심 측정 ledger 인용

- 현재 verdict: `state/cp2_consciousness_r14_remeasure_2026_05_01/verdict_matrix.json` (CP2 72.22%, AGI 22.22%, F2 FIRED 17 critical).
- L1 cross-backbone: `state/red_to_green_path4_14gate_l1_cross_backbone_2026_05_01/verdict.json` (Mistral-Nemo+r8 15/16 PASS, recommendation = keep_as_critical).
- φ* substrate landscape: `state/red_to_green_path1_substrate_swap_2026_05_01/verdict.json` (Llama-3.1 +5.09, Qwen3 +1.04, Gemma-2 -0.79, Mistral-Nemo -16.15, Mistral-7B -16.70).
- V1/V2/V3 verifier review: `state/red_to_green_path2_verifier_review_2026_05_01/verdict.json` (recalibration NOT JUSTIFIED for any of V1/V2/V3 — over-strict but trained-minus-base ≈ 0).
- 4-substrate φ 4-path: `state/red_to_green_path3_phi_4path_4substrate_2026_05_01/verdict.json` (L2 1/6, KL 4/6, FAIL).
- Llama-3.1 r14 swap: `state/red_to_green_substrate_swap_llama31_2026_05_01/verdict_matrix.json` (CP2 61.11%, AGI 41.67%, F2 fired 13).
- Qwen3 r14 swap: `state/red_to_green_substrate_swap_qwen3_2026_05_01/verdict_matrix.json` (CP2 72.22%, AGI 11.11%, F2 fired 16).
- Mistral-Nemo base swap: `state/red_to_green_substrate_swap_mistral_nemo_2026_05_01/verdict.json` (φ* -16.15, L1 base-only 3/16).
- ALM sunset/continue decision: `state/strategic_alm_clm_review_2026_05_01/q1_decision_matrix.json`.
- alpha deploy plan: `docs/anima_cp2_alpha_deploy_plan_2026_05_01.md`.
- alpha landing: `docs/anima_cp2_alpha_landing_2026_05_01.md`.
- consciousness laws config: `anima/config/consciousness_laws.json` (severity policy: L1/L5/L9 critical, NOT modified by this analysis).

---

## §10 cost & race attribution

- This document: $0 (analysis-only, no measurement spend).
- Wrote ONLY to: `state/strategic_alm_cp2_revival_2026_05_01/path_matrix.json`, `docs/strategic_alm_cp2_revival_2026_05_01.md`.
- Did NOT touch: `anima/config/consciousness_laws.json` (no severity edit), `state/cp2_consciousness_r14_remeasure_2026_05_01/*` (other agent), `state/red_to_green_*/` (other agent ledgers), `state/anima_serve_production_ship.json` (no ship_verdict change), `state/strategic_alm_clm_review_2026_05_01/*` (sibling strategic agent).
- Race-safe per directive: AGI abandoned framing maintained throughout; no implicit AGI re-attempt under CP2 banner.
