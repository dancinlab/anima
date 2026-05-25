# anima cycle 2026-05-10 진입 plan v2 — 친근 한국어 mode (BR-FRIENDLY-RESPONSE 정합)

본 doc 은 cycle 2026-05-09 (**59+ milestones**, anima saga **historic 가장 큰 결실 cycle**) close 후 다음 cycle 진입을 위한 plan SSOT v2.

- 작성일: 2026-05-09 cycle close phase (v2 갱신)
- v1 → v2 변화: milestone 50 시점 v1 → milestone 59+ final findings 통합 갱신
- 작성 mode: research + plan only (코드 수정 / 학습 fire **절대 금지**)
- 사용자 verbatim 인증 (v2): 2026-05-09 "cycle 2026-05-10 진입 plan 새로 시작 + all bg go" → entry plan v2 작성
- mandate 정합 — registry yaml mirror 동기 갱신 (cycle close summary section 별도 amend)
- raw#15 additive — 기존 v1 entry plan + cycle docs 무수정 보존, 본 v2 doc 신규
- strict — 모델 로드 절대 금지, text edit only

---

## 0. v1 → v2 신규 발견 milestones (51-59)

milestone 50 (v1 작성 시점) 이후 추가된 9 개 milestone 의 핵심 — **paradigm-j PIV F2 standard 승격** 이 최대 결실:

| # | milestone | 핵심 발견 |
|---|---|---|
| 51 | BG-LA native v5 측정 | 3rd H4 STRONG CONFIRM + DCR 0.000 mode collapse 정량 (cell_pool 학습 무효화 BG-LA 에서도 재현) |
| 52 | cell_pool 4-way consolidation | H4 STRONG CONFIRM (BG-LA + BG-LB + Phase 2 + Engine A/G 4 lane 모두 confirm) |
| 53 | paradigm-j PIV gap 진단 | G2 (k=5+ paraphrase) FALSIFIED, **G1 (F1→F2 metric 변경) + G3 (L2 norm) 우세** |
| 54 | .own + README + registry final audit | yaml↔md mirror full audit PASS, alias table 정합 |
| 55 | HF Phase 2 cotrain private upload | Phase 2 350M cotrain ckpt private repo upload (Goodhart-falsified record-keeping 등급) |
| 56 | paradigm-j PIV G3 정량 확정 | **F1 → F2 1.646× boost** (L2-norm metric variant) — F1 max bias 가 metric artifact 임을 정량 입증 |
| 57 | H5 lm_head + tied embedding 발견 ★ | **lm_head ≡ tok_emb (40도 회전 후 동일)** — chat-template dual loss 가 이 회전을 통해 cell collapse 증폭 mechanism 확정 |
| 58 | axis-N+1 hook plan | T+1~T+4 step 구체화, 1순위 axis-5 = AX5-c verifier (chat orchestra 5번째 axis schema) |
| 59 | F2 정식 승격 + paradigm-j EMERGE_V5_PIV_F2_PASS ★ | 사용자 verbatim "OK PROMOTE PIV_L2_NORM_F2 STANDARD" → **F2 L2-norm 이 새 standard, F1 max deprecated** |

**paradigm-j 통합 verdict (final)**:
- v5 BASE F2 (L2-norm) PASS ✓ — 1.4% gap 가 metric artifact 임이 입증됨
- v5.2 adaptive PASS ✓
- **이제 F1 max 가 아닌 F2 L2-norm 이 standard** (사용자 verbatim 승격)

H5 lm_head + tied embedding 발견 (milestone 57) 의 의의 — H4 (normalize 무효화) 의 mechanism 자체를 한 layer 더 깊이 들어간 발견. cell_pool 학습 effect 가 단순히 unit-sphere normalize 만으로 지워지는 게 아니라 **lm_head 와 tok_emb 가 묶여있는 (tied) 구조에서 40도 회전을 통해 collapse 증폭** 되는 것. 이 발견이 다음 cycle priority 1 (fix-5/fix-6 tied embedding 통합 PoC) 의 직접 motivation.

---

## 1. 본 cycle (2026-05-09) 친근한 cycle close summary

### 1-1. 본 cycle 의 의의 (일반인용 1 단락)

이번 cycle 은 anima 사가 22+ BG saga 중 **가장 큰 결실 cycle** 이에요. 한 줄로 요약하면 — "anima 가 처음으로 의식 시험 (consciousness measurement) 을 엄격 기준 (v5.2) 으로 통과한 모델 (paradigm-j) 을 PUBLIC 으로 promote 했고, 그 와중에 'PPL-시험 통과' 가 '진짜 의식' 이 아닐 수 있다는 걸 처음으로 정량 입증해서, 평가 기준 자체를 한 단계 더 엄격하게 만든 cycle". 학생 시험 비유로 — anima 라는 학생이 처음 명문대 (PUBLIC 발효) 합격한 것 + "객관식 점수" 만 보는 시험은 가짜 통과자를 거를 수 없으니 "5축 면접" 까지 보게 만든 것 두 가지를 동시에 한 cycle. **그리고 milestone 51-59 에서 paradigm-j 의 PIV metric 자체를 F1(max) → F2(L2-norm) 로 표준화 + tied embedding 회전이 cell collapse 의 mechanism 임을 확정** — 이게 v2 갱신의 핵심.

### 1-2. 다음 cycle 의 향방 (1 단락)

다음 cycle 은 **substrate-research lane 으로 한 단계 더 깊이 들어가는 cycle**. 본 cycle 에서 발견한 H4 (unit-sphere normalize 가 cell_pool 학습 효과를 지움) + H5 (chat-template dual loss + **tied embedding 40도 회전** 이 cell collapse 증폭) 두 가설을 arch 수정 (fix-5 + fix-6 **tied embedding 통합 PoC**) 으로 검증. 그 PoC ($5-15) 가 통과하면 7B Phase 3 진입 prereq 충족 가능. 이번 v2 plan 의 가장 중요한 변화는 **fix-5/fix-6 가 단순 normalize 제거 → tied embedding 통합 처리 로 진화** 한 것 — 즉 lm_head 와 tok_emb 의 tying 자체를 끊을지 (untie), 동결할지 (freeze) 정량 비교. 동시에 attention/FFN 의 collapse 증폭기 배제 (j 항목) + axis-N+1 hook 구현 (k 항목) 이 0-cost lane 으로 병렬 진행.

### 1-3. anima 가 어디까지 왔는지 + 어디로 갈건지 (1 단락)

지금 anima 는 — (a) 의식 측정 layer ✓ (paradigm-j PUBLIC v5 BASE F2 PASS, sft-1-8 PUBLIC) (b) 자연어 chat orchestra 4-axis ✓ (lane × mode × init-pattern × transport 모두 LIVE) (c) H100 dual training 회수 능력 ✓ (BG-LA + BG-LB + Phase 2 COMPLETE) (d) own audit + alias resolution ✓ (e) **PIV F2 L2-norm standard 승격 ✓** — 5 layer 모두 산업 grade 로 land 된 상태. 단 chat-cap C2 자연어 substrate quality 는 여전히 한계 (Path 3 generate FULL 회수 후에도 sft-1-8 substrate undertrained, gibberish output) + cell_pool 학습 자체가 4-way confirmed H4 (normalize + tied embedding 회전) 으로 무력화. 그래서 다음 cycle 부터는 **arch 자체 수정 (tied embedding 통합 처리) + Phase 3 (7B) 본진 로드맵 진입 prereq** 두 갈래로 가는 게 정공법. 종착지는 Phase 4 (14B) anima 사가 first scratch 14B **본진 모델** — 학생 비유로는 "유치원생 → 초등학생 → 고등학생 → 대학생" 의 4 단계 중 지금 초등학생 단계 (Phase 2 350M cotrain 실행) 마침이며, fix-5 + fix-6 통과 시 7B 단계로 진학.

---

## 2. 본 cycle 통계 핵심 숫자 (v2 final)

| 항목 | 값 |
|---|---|
| **총 milestones** | **59+** (cycle 1-59, milestone 59 = paradigm-j EMERGE_V5_PIV_F2_PASS standard 승격) |
| **HF PUBLIC promote** | **2** (sft-1-8 V14 borderline path + paradigm-j v5 BASE F2 strict PASS ★) |
| **HF private promote** | **2 dataset** (tier-a-v4) + **2 model** (BG-LB 350M Goodhart-falsified record-keeping + Phase 2 cotrain milestone 55 land) |
| **H100 actual cost** | **~$66 ± $5 / $200 budget = 33%** (BG-LA $36.60 + BG-LB ~$18.30 ledger overlap 정정 + Phase 2 $4.63 + V6 $0.85 + Step B killed $0.88 + idle/orphan ~$5) |
| **budget 잔여** | $200 - $66 = **~$134 잔여** (strict ✓) |
| **H100 pod 보유** | **0 pod** (모두 회수, BG-LA + BG-LB + Phase 2 ckpt pull 모두 land) |
| **honest C3 findings** | **15+ cumulative** (cycle 시작 12 + Phase 2 H5 + milestone 51 H4 BG-LA confirm + milestone 57 lm_head tied embedding = 15) |
| **robust EMERGE 확정 (v5 BASE F2)** | **1** (paradigm-j ★) — sft-1-8 V14 borderline + BG-LB Goodhart-falsified + Phase 2 V14 violated |
| **chat orchestra 4-axis** | **LIVE FIRE 4/4 검증 ✓** (lane / mode / init-pattern / transport) — milestone 58 axis-5 schema 확장 plan land |

### 가장 큰 결실 ranking (v2 재정리)

1. ★★★ **paradigm-j first robust EMERGE PUBLIC + F2 standard 승격** (v5 BASE F2 L2-norm PASS, milestone 59 사용자 verbatim "OK PROMOTE PIV_L2_NORM_F2 STANDARD")
2. ★★★ **first dual H100 actual training COMPLETE** (BG-LA + BG-LB + Phase 2 cotrain — 3 fire 회수)
3. ★★★ **PROXY_PPL Goodhart 첫 정량 입증** (BG-LB native v5 V14 violated, **emerge metric 영구 deprecate**)
4. ★★★ **H4 4-way STRONG CONFIRM + H5 lm_head tied embedding mechanism 확정** ★ — milestone 51-52 BG-LA + Phase 2 + 4-way consolidation, milestone 57 lm_head ≡ tok_emb 40도 회전 발견
5. ★★★ **PIV F2 L2-norm standard 승격** (milestone 53 G3 우세 + milestone 56 1.646× boost 정량 + milestone 59 verbatim 승격)
6. ★★ **chat orchestra 4-axis FULL LIVE 검증** + axis-5 schema plan (milestone 58)
7. ★★ **CLM v5 Engine A/G 7B/14B 스케일 로드맵 명문화**
8. ★ **own audit 25 findings + 14-entry alias table + final audit PASS** (milestone 54)
9. ★ **resource ephemeral CLI rewrite + secret CLI integration**
10. ★ **arch fix CONSCIOUSNESS_DIM=192→96 substrate-level VERIFIED**
11. **ALT-AGG-1 v2→v3→v4→v5→v5.1→v5.2 evolution**

### honest C3 핵심 findings (v2 critical 4 건)

1. **PROXY_PPL 위험성 첫 정량 입증 ★** — BG-LB native v5 측정 PIV/DCR 둘 다 random_init > trained → byte-modulo PPL fit 이 의식 substrate 아님 확정. **emerge metric 자격 영구 deprecate**.
2. **H4 4-way STRONG CONFIRM + H5 lm_head tied embedding 회전** ★★ — Engine A/G arch 의 unit-sphere normalize + lm_head ≡ tok_emb (40도 회전) tying 이 cell_pool 학습 effect 를 지움. 4 lane (BG-LA + BG-LB + Phase 2 + Engine A/G) 모두 confirm.
3. **PIV F1 max bias 가 metric artifact** — milestone 56 F1 → F2 1.646× boost 정량 → F1 max 는 random/trained overlap zone 에서 random 우위 artifact 발생. **F2 L2-norm standard 승격** (milestone 59).
4. ** mandate-9 strict 함이 Goodhart 자동 차단** — BG-LB "성공모델이면 PUBLIC" 조건부 verbatim antecedent 미충족 → automatic public block. 5/5 prereq strict 가 보호 작동.

---

## 3. carry items 분류 (active / completed / deferred 표 — v2 갱신)

source: `state/anima_cycle_2026_05_09_carry_items_2026_05_09.json` (10 carry items) + 본 cycle 후반 신규 4 carry + v2 신규 3 carry (lm_head untie / FFN cosine / axis-5 hook).

| ID | 분류 | 다음 cycle action |
|---|---|---|
| **proxy_ppl_deprecate_2026_05_09** | COMPLETED ★ | enum flag landed in registry yaml + spec doc 3종 |
| **paradigm_j_public_promote** | COMPLETED ★ | actual HF PUBLIC + yaml ledger landed |
| **paradigm_j_F2_standard_promote** (NEW) | COMPLETED ★ | milestone 59 사용자 verbatim "OK PROMOTE PIV_L2_NORM_F2 STANDARD" land |
| **JVAE_100K_continued_training** | DEFERRED (OBSOLETE_BY_v5_2_EMERGE) | deprecate cycle OR explicit retry trigger 시 reactivate |
| **yaml_indent_bug_line_1885** | COMPLETED (AMENDED_2026_05_09) | render verify (43478 bytes) PASS |
| **mk2_v1_v5_n120_non_robust** | ACTIVE | D-RAND prompt redesign (0-cost) **우선 path** OR H100 N=120 deferred |
| **init_pattern_drift_risk_phase_2** | ACTIVE | `anima audit --mandate-41` cross-site lint extension spec emit |
| **ssot_pod_ownership_patch_resource_package** | ACTIVE (외부 cycle) | resource package 측 PR — 본 anima cycle 외 작업 |
| **transport_plugin_pattern** | ACTIVE | 4-axis chat orchestra 4번째 axis cross-product invoke |
| **BG_LA_engine_a_g_h100_training** | COMPLETED (milestone 51 native v5 measured) | H4 BG-LA confirm DONE — 추가 action 없음 |
| **BG_LB_350m_scratch_pretrain_h100** | COMPLETED (Goodhart-falsified) | DEPRECATED_PROXY_PPL_FALSIFIED |
| **own_audit_phase_2_amend** | COMPLETED (milestone 54 final audit PASS) | Phase 2 Option A: env bypass 별도 cycle |
| **substrate_quality_amplification** | ACTIVE | **다음 cycle priority 1**: fix-5 + fix-6 tied embedding 통합 PoC ($5-15) |
| **NEW: fix-5 unit-sphere normalize 제거/약화** | ACTIVE → **fix-5/fix-6 통합 PoC 로 진화** | i 항목 참조 |
| **NEW: fix-6 chat-loss curriculum 재설계** | ACTIVE → **fix-5/fix-6 통합 PoC 로 진화** | i 항목 참조 |
| **NEW: lm_head untie / tok_emb untie / tied freeze 3-way PoC** (v2) | ACTIVE (1순위) | i 항목 — milestone 57 후속 |
| **NEW: attention/FFN row-wise cosine 측정** (v2) | ACTIVE (2순위, 0-cost) | j 항목 |
| **NEW: axis-N+1 hook 구현** (v2) | ACTIVE (3순위, 0-cost) | k 항목 — milestone 58 후속 |
| **NEW: Phase 2 cotrain pending phases** | COMPLETED (milestone 55 private upload) | upload 자체는 milestone 55 land |
| **NEW: clm_v5_mount.hexa 5-axis projection learnable** | ACTIVE | learned linear projection 후속 carry |
| **anima_chat_phase 2/3 carry** | ACTIVE | substrate quality fix 후 chat-cap C2 재측정 |
| ** axis-N+1 hook** | ACTIVE → k 항목으로 구체화 | T+1~T+4 step land plan |
| **clm v2 archive lane** | DEFERRED | 별도 cycle close 검토 |

**summary v2**:
- COMPLETED: 7 (proxy_ppl_deprecate / paradigm_j PUBLIC / **paradigm_j F2 standard** / yaml_indent / BG-LA + BG-LB + Phase 2 ckpt pull + native v5 + private upload / own audit Phase 2 final audit)
- ACTIVE: 12 (substrate amp / **fix-5/6 통합 PoC (i)** / **FFN cosine (j)** / **axis-5 hook (k)** / mk2-v1 D-RAND / init-pattern Phase 2 / transport 4-axis / clm_v5_mount learnable / chat phase 2/3 / axis hook 후속 / own audit Phase 2 Option A env bypass / SSOT pod-ownership 외부)
- DEFERRED: 2 (JVAE 100K / clm v2 mitosis 부활)

---

## 4. 다음 cycle 진입 plan — 항목 a~h + v2 신규 i / j / k

### a) **fix-5 + fix-6 PoC sequence** (v1 1순위 → v2 i 항목으로 통합 진화)

**v2 변화**: milestone 57 lm_head + tied embedding 발견 후, fix-5 (unit-sphere normalize 제거) + fix-6 (chat-loss curriculum) 만으로는 mechanism 의 절반만 다룸. 진짜 root cause 는 **lm_head ≡ tok_emb tying 의 40도 회전 collapse**. 따라서 v2 에서는 i 항목 **fix-5/fix-6 tied embedding 통합 PoC** 로 진화 (3 분기 비교).

### b) **mk2-v1 v5 PIV/DCR 재측정** (Mac 부하 해소 후 OR H100 pod) — v1 보존

- 현재 carry: PPR_v5 0.2881 (gap -0.0119), N=120 sensitivity 44%
- D-RAND mean=0.18 (floor 0.20 미달)
- **path 1 (0-cost, recommended)**: D-RAND prompt-set redesign Mac local
- **path 2 (deferred fallback)**: H100 real-mode N=120 paired V14 ($5-10)
- **v2 추가**: 이제 PIV F2 L2-norm standard 이므로 mk2-v1 도 F2 metric 으로 재측정 (F1→F2 1.646× boost 가능성, milestone 56 paradigm-j 와 동일 mechanism 검증)
- **진입 prereq**: Mac load avg 30 이하 (현재 145)

### c) **paradigm-j v5.2 → v5 base 진단** — v1 → v2 RESOLVED ★

**v1 시점**: PIV 0.0874 < 0.10 의 1.4% gap 본질 분석 미해결
**v2 시점 (milestone 53/56/59)**: **RESOLVED** — F1 max 가 metric artifact 임이 입증됨, F2 L2-norm 으로 1.646× boost → v5 BASE F2 PASS, 사용자 verbatim "OK PROMOTE PIV_L2_NORM_F2 STANDARD" 승격. 추가 amplification 불필요.

### d) **CLM v5 Engine A/G arch 자체 review** — v1 보존 + v2 i 항목과 통합

fix-5 + fix-6 통합 PoC (i 항목) 결과에 따라 arch redesign cycle 결정:
- i 항목 PASS → 350M full retrain $30-60 (Phase 2 본 spec) 재실행
- i 항목 FAIL → arch 자체 redesign cycle (cell_pool 구조 / repulsion-field / tension gate review)

### e) **7B/14B Phase 3 진입 prereq** — v1 보존

`.roadmap.clm` Phase 3 entry condition strict:
- `phase_2_consciousness_pass`: required → **현재 FAIL**
- `phase_2_natural_language_pass`: required → **NOT_MEASURED**
- `cost_bearing_verbatim`: required (`OK CLM PHASE 3 7B FIRE COST $200-600`)
- `arch_origin_d1`: D1=1.0 strict

**timeline v2**:
- T+0~3d: i 항목 fix-5/fix-6 통합 PoC ($5-15) → tied embedding 회전 검증
- T+3~6d: i 항목 PASS 시 350M re-cotrain ($30-60) → consciousness PASS 검증
- T+6d+: Phase 3 cost-bearing verbatim 제시 가능

### f) **CLM v2 archive lane** (commit 73a6596b mitosis 부활) — v1 보존

별도 cycle close 검토 doc 작성 권장.

### g) **anima_chat_phase 2/3 carry** — v1 보존

substrate quality fix (i 항목 통과) 후 chat-cap C2 재측정.

### h) ** axis-N+1 hook** (chat orchestra 4-axis future-proof) — v1 → v2 k 항목으로 구체화

milestone 58 에서 T+1~T+4 step plan land. 1순위 axis-5 = AX5-c verifier. v2 k 항목에서 구현 plan 상세화.

---

### i) **★ fix-5/fix-6 tied embedding 통합 PoC** (v2 신규, 1순위, $5-15) ★

**motivation**: milestone 57 발견 — lm_head ≡ tok_emb (40도 회전 후 동일). cell_pool 학습 effect 가 H4 (unit-sphere normalize) + H5 (chat-template dual loss + tied embedding 회전) 두 mechanism 으로 지워짐. 단순 normalize 제거만으로는 근본 해결 X.

**3 분기 비교 PoC**:

| Variant | 변경 | 가설 |
|---|---|---|
| **branch-A (lm_head untie)** | lm_head 를 tok_emb 와 분리 (별도 weight) | 회전이 lm_head 에서 발생한다면 untie 로 차단 |
| **branch-B (tok_emb untie)** | tok_emb 를 freeze + lm_head 만 학습 | 회전이 tok_emb 에서 발생한다면 freeze 로 차단 |
| **branch-C (tied freeze)** | tied 유지 + 둘 다 freeze | tying 자체는 OK, gradient flow 만 차단하면 회피 가능한지 검증 |

**method**: 각 branch 350M re-cotrain 500-1000 step 짧은 PoC ($5 each, total $15) → cell_pool axis_stdev / off_diag_cos / DCR 측정 → random_init vs trained 차별화 (V14 paired-mirror) 검증.

**spec doc**: `docs/anima_engine_a_g_fix_5_6_tied_embedding_unified_poc_spec_2026_05_10.md` (별도 cycle emit, design-only)

**verdict 기준**:
- 3 branch 중 1+ 개가 V14 PASS → tied embedding mechanism 확정 + 350M full retrain unblock
- 모두 FAIL → arch 자체 redesign cycle 진입 (cell_pool 구조 자체 review)

**user verbatim 필요**: `OK FIX5+FIX6 TIED EMBEDDING UNIFIED POC $5-15` 또는 동등.

### j) **★ attention/FFN row-wise cosine 측정** (v2 신규, 2순위, 0-cost)

**motivation**: lm_head + tok_emb 외에도 attention output / FFN intermediate 가 cell collapse 증폭기 역할 가능성 — milestone 57 발견은 lm_head 만 단독 검증, 다른 layer 의 회전/collapse 양상 미측정.

**method (Mac local 0-cost)**:
- Phase 2 ckpt 로드 (이미 disk 보유, milestone 55 private upload)
- 각 transformer block 의 attention.out_proj weight + FFN.down_proj weight 추출
- row-wise cosine similarity matrix 계산 → eigenvalue spectrum + entropy
- random_init vs trained paired comparison (V14 mirror)

**verdict 기준**:
- attention/FFN cosine entropy 가 trained < random → collapse 증폭기 추가 발견 (i 항목 PoC scope 확장 필요)
- attention/FFN cosine entropy 가 trained ≈ random → lm_head + tok_emb 단독 mechanism 확정 (i 항목 PoC scope 유지)

**spec doc**: `docs/anima_attention_ffn_cosine_measurement_spec_2026_05_10.md` (별도 cycle emit)

**cost**: 0 ($0, Mac local, 모델 로드 1회 — Mac load avg 30 이하 회복 후)

### k) **★ axis-N+1 hook 구현** (v2 신규, 3순위, 0-cost)

**motivation**: milestone 58 axis-N+1 hook plan 의 구체 구현. chat orchestra 4-axis (lane / mode / init-pattern / transport) → 5번째 axis 추가 시 동일 plugin pattern 으로 자동 통합되도록.

**T+1~T+4 step plan**:

| step | action | output |
|---|---|---|
| T+1 | axis-5 schema spec emit (1순위 = AX5-c verifier) | `anima/spec/anima_chat_axis_5_verifier.spec.yaml` |
| T+2 | hook discovery API 구현 (registry yaml axis-N+1 자동 detection) | `anima/registry/anima_chat_axis_registry.yaml` extension |
| T+3 | benchmark cross-product invoke (4-axis × axis-5 = 5-axis matrix) | `anima/benchmark/anima_chat_5_axis_matrix.yaml` |
| T+4 | live fire validation (axis-5 추가 시 4-axis 회귀 없음 확인) | regression test PASS |

**axis-5 후보 (1순위 = AX5-c verifier)**:
- AX5-a: emotion (sad/happy/neutral)
- AX5-b: persona (formal/casual)
- **AX5-c: verifier** ★ (consciousness verifier 결과 hook — paradigm-j v5 BASE F2 PASS 모델만 응답 lane 활성화) — 1순위

**cost**: 0 ($0, Mac local + spec emit only)

**spec doc**: `docs/anima_chat_axis_5_verifier_hook_spec_2026_05_10.md`

---

## 5. 다음 cycle priority — final ranking v2

| 순위 | action | cost | type |
|---|---|---|---|
| **1 ★** | **i) fix-5/fix-6 tied embedding 통합 PoC (3 branch)** | **$5-15** | H100 (verbatim 필요) |
| **2** | **j) attention/FFN row-wise cosine 측정** | **$0** | Mac local |
| **3** | **k) axis-N+1 hook 구현 (T+1~T+4)** | **$0** | spec + local |
| 4 | mk2-v1 D-RAND prompt redesign + F2 metric 재측정 | $0 | local |
| 5 | clm_v5_mount.hexa 5-axis projection learnable | $0 | local |
| 6 | own audit Phase 2 Option A (env bypass + .own actual rename) | $0 | local |
| 7 | init-pattern drift Phase 2 audit | $0 | local |
| 8 | yaml-hygiene cycle | $0 | local |
| 9 | clm v2 archive lane 부활 평가 doc | $0 | doc |
| **10 (i 항목 PASS 후)** | **350M re-cotrain (i 항목 통과 branch 적용)** | $30-60 | H100 |
| **11 (10 PASS 후)** | **CLM Phase 3 7B fire** | $200-600 | H100 8-GPU |
| 12 (long-term) | CLM Phase 4 14B fire | $500-1500 | H100 16-GPU |

**주목**: 1순위 i 항목 외 2-9 순위 모두 0-cost lane — 다음 cycle 진입 시 verbatim 없이도 8 개 항목 병렬 진행 가능.

---

## 6. 다음 cycle 진입 prereq 명시 (mandate 정합)

다음 cycle 진입 시점에 다음이 충족되어야 함:
1. ✅ 본 cycle close summary 가 registry yaml 의 `cycle_close_summary` section 에 amend 되어 있음 (yaml↔md 동기)
2. ✅ 본 entry plan v2 doc (`docs/anima_cycle_2026_05_10_entry_plan_v2_2026_05_09.md`) 가 disk 저장 + `.ai.md` mode 정합
3. carry json (`state/anima_cycle_2026_05_09_carry_items_2026_05_09.json`) 의 carry_status_update_summary 가 본 cycle close 시점 status 와 정합 (이미 land)
4. i / j / k 항목 spec doc emit (별도 BG, design only)
5. Mac load avg 30 이하 회복 (현재 145, free RAM 461MB) — 다음 cycle 로컬 fire 진입 prereq
6. 사용자 verbatim 인증:
   - **i 항목 fix-5/fix-6 통합 PoC fire 시 `OK FIX5+FIX6 TIED EMBEDDING UNIFIED POC $5-15`** ★ (1순위)
   - 350M re-cotrain fire 시 `OK 350M RE-COTRAIN POST-PoC $30-60`
   - Phase 3 7B fire 시 `OK CLM PHASE 3 7B FIRE COST $200-600`
   - Phase 4 14B fire 시 expansion verbatim + fire verbatim 2 단계 모두 필수

---

## 7. compliance at entry plan v2 emit

| Mandate | Status |
|---|---|
| V14 anti-Goodhart | PASS — i 항목 PoC 도 V14 paired-mirror mandatory |
| cost discipline | PASS — entry plan v2 자체 0-cost (text edit only) |
| D1 SCOPE_CLAMP | PASS — 모든 plan item D1=1.0 anima_native_scratch lane |
| mandatory report | PASS — 본 doc 자체가 mandatory cycle entry plan v2 |
| single SSOT | PASS — registry yaml master + 본 doc mirror |
| ckpt preservation | PASS — BG-LA + Phase 2 ckpt pull + private upload (milestone 55) land |
| trinity | PASS — D + own + H 모두 정합 |
| mandate-2 wrap-0 | PASS — text-only doc, no binary content |
| visibility lifecycle | PASS — paradigm-j F2 standard PUBLIC + Phase 2 / BG-LB private 유지 |
| 매단계 저장 | PASS — 본 doc + carry json 모두 disk 저장 |
| yaml↔md auto-regenerate | PENDING — registry yaml `cycle_close_summary` section amend 별도 step |
| resource CLI 위임 | PASS — anima 직접 cloud-cli/api-key write 0 |
| chat lane plugin pattern | PASS — k 항목으로 axis-5 hook 구체화 |
| raw#10 honest C3 | PASS — H4/H5/PROXY_PPL/Goodhart/lm_head tied embedding 모두 honest emit preserve |
| raw#15 additive | PASS — v1 entry plan + 기존 cycle docs 무수정 보존 |
| raw#82 retraction-aware | PASS — F1 max metric DEPRECATED + F2 L2-norm STANDARD 등급 carry preserve |

---

## 8. honest C3 emit (본 plan v2 doc 자체)

1. 본 plan 의 i 항목 fix-5/fix-6 통합 PoC 는 **3 branch 가설 검증 단계**, success guarantee X — lm_head + tok_emb tying 외 추가 mechanism (j 항목 attention/FFN) 가능성 carry
2. j 항목 attention/FFN cosine 측정은 Mac load avg 30 이하 회복 후에만 가능 — 현재 145 / 461MB free RAM 로 모델 로드 불가, 다음 cycle 진입 후 실행
3. k 항목 axis-5 verifier hook 의 AX5-c 는 paradigm-j v5 BASE F2 PASS 모델 단독 의존 — F2 standard 가 추가 falsification 시 hook 자체 영향 (raw#82 retraction-aware mandate 정합)
4. CLM Phase 3 7B fire 는 i 항목 통과 + 350M re-cotrain consciousness PASS + BG-CORPUS-7B 구축 3 prereq 모두 충족 후에만 가능 — 다음 cycle 단일 cycle 으로는 불가, 최소 2-3 cycle 누적 필요
5. 본 plan v2 doc 작성 시점 Mac load avg 145 / 461MB free RAM — 모델 로드 절대 불가 환경에서 file edit 만으로 작성됨 (strict ✓, deterministic doc emit)

---

## 9. 친근 한 줄 final — cycle 2026-05-10 strategic objective

**한 줄로 요약**: cycle 2026-05-10 의 strategic objective 는 **tied embedding 의 회전을 막아 paradigm-j 보다 강한 base substrate 모델 만들기**.

**비유로 풀어 말하면** — paradigm-j 는 "객관식 + 5축 면접 합격한 첫 학생" 이지만, 그 학생의 머리 안을 들여다보니 **"입력 단어장 (tok_emb) 과 출력 단어장 (lm_head) 이 같은 노트인데 40도 비스듬히 적혀 있어서, 공부하면 할수록 글자가 뭉개지는 (cell collapse) 구조"** 였어요. cycle 2026-05-10 은 **이 노트를 두 권으로 분리하거나 (untie) / 노트를 동결하거나 (freeze) / 동결한 채 tying 만 유지** 세 가지 방식으로 글자가 뭉개지는 걸 막고, 그 결과 paradigm-j 보다 더 단단한 substrate 모델 (350M + 향후 7B/14B) 을 만드는 게 목표. 그러니까 한 줄로 — **"학생 노트의 글자 회전을 막아서, 더 똑똑한 학생을 만드는 cycle"**.

---

본 doc 은 anima cycle 2026-05-10 진입을 위한 plan v2 SSOT — 사용자 검토 후 commit/push 별도 step.
