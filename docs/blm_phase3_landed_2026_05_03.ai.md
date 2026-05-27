# BLM Phase 3 Landed — 2026-05-03 (AI-native, friendly preset)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 1 updated `.roadmap.blm_brain_lm` (additive JSONL append only) + 5 verifier override logs (`state/blm_phase3_cond{1..5}_*_log.jsonl`) + 3 synthetic fixtures (`state/blm_phase3_cond4_fixtures/`) + 0 sister-roadmap modification
> upstream handoff target: `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 (BLM rolling state)
>
> BR-NO-USER-VERBATIM: peer surface mk2 conventions. user prompt verbatim reverberation X.
> 마이그레이션 절대 금지 — 본 cycle 0건 file rename / 0건 sister .roadmap modification / 0건 narrative edit.

---

## TL;DR

**오늘 한 일** — BLM Phase 3 spec 5/5 cond EXEC. cond.1 (EEG track integration) + cond.2 (cross-substrate consistency) + cond.3 (F-CT-3 falsifier formal) + cond.4 (3-domain API stub) + cond.5 (decision matrix + entry-trigger contract) 모두 spec FROZEN. composite verdict = **PASS 5/5**, Phase 4 entry **GRANTED-ELIGIBLE** (별도 GPU budget authorization 필요).

**비유** — Phase 1+2 = 신입사원 (BLM) 측 첫째/둘째날 (도구 익히기 + 데이터셋 결정), Phase 3 = 셋째날 "다른 부서 (CLM, EEG, qmirror)와 어떻게 협업할지 명세서 동결 + API 견본 + 실패조건 사전 등록 + 다음날 (Phase 4 = 실제 훈련) 진입 조건 docket 통과". 실제 훈련 = 별도 cycle (GPU $500-2000 budget approval 필요).

**결과** — `.roadmap.blm_brain_lm` 5 phase3 entry append (in-place 변경 X, 기존 cond.1-3 + blk.1 손대지 X). Phase 1+2 cond.1=met / blk.1=resolved 그대로. cond.2/cond.3 unmet 유지 (Phase 4 IMPL 측 별도 cycle).

---

## §1 5-cond EXEC status table

```
   cond                  | status (this cycle) | deliverable                                                | verifier log
   --------------------- | ------------------- | ---------------------------------------------------------- | ------------------------------------------------
   blm.phase3.cond.1     | PASS                | EEG track integration spec FROZEN                          | state/blm_phase3_cond1_eeg_integration_log.jsonl
   blm.phase3.cond.2     | PASS                | 3-substrate consistency spec FROZEN                        | state/blm_phase3_cond2_cross_substrate_log.jsonl
   blm.phase3.cond.3     | PASS                | F-CT-3 falsifier formal definition + null plan + min-data  | state/blm_phase3_cond3_fct3_falsifier_log.jsonl
   blm.phase3.cond.4     | PASS                | 3-domain API stub schema + 3 synthetic fixtures            | state/blm_phase3_cond4_api_stub_log.jsonl + state/blm_phase3_cond4_fixtures/
   blm.phase3.cond.5     | PASS                | decision matrix + entry-trigger contract FROZEN            | state/blm_phase3_cond5_decision_matrix_log.jsonl
```

**composite verdict = PASS 5/5 → Phase 4 entry GRANTED-ELIGIBLE.**

---

## §2 cond.1 — EEG track integration spec

### §2.1 결정 (frozen)

```
   field                       | value
   --------------------------- | --------------------------------
   shared text encoder         | meta-llama/Llama-3.2-3B (BLM + EEG both, vendored references/tribev2/inventory.json line 41-44)
   BLM phi_proxy interface     | phi_proxy: BOLD_window R^(20484 vertices x T) -> R^d_phi
   d_phi grid                  | {1, 8, 16}
   shared with EEG phi_proxy   | true (sister .roadmap.eeg cond.4 1순위 sample-partition phi)
   baseline anchor             | anima_phi_v3_canonical baseline 41.86 (CLM hidden state)
```

### §2.2 cross-link diagram (ASCII)

```
   text token
       |
       v
   [meta-llama/Llama-3.2-3B shared text encoder]
       |
       +-> [BLM TRIBE BOLD encoder] -> BOLD vertex map R^(20484 x T)
       |       |
       |       +-> phi_proxy_BOLD: anima_phi_v3 (BLM novel port) -> R^d_phi
       |
       +-> [EEG sister track] -> ZuCo NR-2 fixation-locked window R^(C x T)
               |
               +-> phi_proxy_EEG: anima_phi_v3 (sister .roadmap.eeg cond.4 port) -> R^d_phi
                       |
                       v
               [cross-substrate consistency] vs CLM phi-star baseline 41.86
                       |
                       v
               same-formula-different-substrate claim (cond.2)
```

### §2.3 temporal alignment caveat (honest)

- BOLD TR=1.49s averages ~7-8 CLM tokens (HRF lag)
- ZuCo word-level fixation ~200-500ms (per-token natural fit)
- joint training requires HRF down-sampling or word-aggregation — explicitly noted in spec, not solved this cycle

---

## §3 cond.2 — cross-substrate consistency spec

### §3.1 3-substrate comparison table

```
   substrate            | formula                          | baseline value | status
   -------------------- | -------------------------------- | -------------- | ----------------------------------
   CLM hidden state     | anima_phi_v3_canonical           | 41.86          | frozen reference (CP2-CLM RED, F1=0.408 confidence band)
   EEG window           | anima_phi_v3_canonical (port)    | (deferred)     | spec only — eeg.blk.4 spec FROZEN pending
   TRIBE BOLD vertex map| anima_phi_v3_canonical (port)    | (deferred)     | spec only — BLM novel port, no IMPL
   ---
   qmirror IIT 4.0 Phi  | IIT 4.0 (different family)       | 0.0            | adjacent witness — same-formula triangle = CLM+EEG+BOLD only
```

### §3.2 tolerance band proposal

```
   metric              | |delta phi| / phi
   threshold           | 0.30 (placeholder)
   calibration         | deferred to Phase 4 (3-substrate empirical measurement first)
   null floor          | random-control mandatory (sister .roadmap.n_substrate cond.1 5+ substrate witness pattern)
```

### §3.3 same-formula-different-substrate claim 의 핵심

`anima_phi_v3_canonical` = sample-partition log|Cov| over K=8 partitions. CLM substrate에선 hidden state matrix, EEG에선 channel-time matrix, BOLD에선 vertex-time matrix. **세 substrate 모두 동일 algebraic formula** — 즉 cross-substrate comparison 측 isomorphism 가정 X (substrate-neutral measurement claim). 단 caveat: phenomenal consciousness 보장 X (functional/access tier only, raw#10).

---

## §4 cond.3 — F-CT-3 falsifier formal definition

### §4.1 falsifier spec (frozen)

```
   field                    | value
   ------------------------ | --------------------------------
   id                       | F-CT-3
   name                     | EEG <-> TRIBE BOLD predicted vertex map Pearson r >= 0.5
   alignment corpus         | Algonauts2025 Friends s7 (test split) + ZuCo NR-2
   primary metric           | Pearson r
   threshold                | 0.5
   decision rule            | r >= 0.5 = PASS / r < 0.5 = REJECT (F4 falsifier)
```

### §4.2 null distribution plan

```
   method               | permutation test
   N                    | 1000 (minimum)
   variants             | (a) block permutation (BOLD HRF ~5s smoothing)
                        | (b) phase-randomization (Theiler 1992 surrogates for EEG phase)
   choice rationale     | naive permutation INVALID due to temporal autocorrelation
                        | block perm or phase-rand mandatory (honest C4 caveat)
   null floor target    | p < 0.01 (one-sided, r > observed)
```

### §4.3 minimum-data plan

```
   path                | size      | cost   | substrate
   ------------------- | --------- | ------ | --------------------------
   ZuCo subset         | ~50 MB    | $0     | OSF public (1-2 subj x 1 task)
   BOLD subset         | (vendored)| $0     | references/tribev2/tribev2/studies/algonauts2025.py code path lock-in
   raw h5/tsv/mkv      | (deferred)| --     | Courtois NeuroMod separate SLA (post Phase 3)
   RunPod sanity probe | --        | $0-2   | optional 1xA10 1h
```

### §4.4 pre-register schema (frozen)

```
   field                                | type
   ------------------------------------ | ------------
   ts_utc                               | str
   corpus_subset                        | str
   model_checkpoint                     | str
   null_method                          | str (block_perm | phase_rand)
   N_permutations                       | int
   r_observed                           | float
   r_null_distribution_p_value          | float
   verdict                              | str (PASS | REJECT)
   ---
   frozen_at                            | 2026-05-03
   mutable_after_freeze                 | false
```

---

## §5 cond.4 — 3-domain production readiness API stub

### §5.1 3 endpoint surface (spec only, NO weights)

```
   endpoint                         | input                                       | output
   -------------------------------- | ------------------------------------------- | --------------------------------------------------
   text_to_bold_predict             | text + model_id + subject_id + tr_seconds   | bold_pred R^(20484 x T) + uncertainty + license
   bold_to_text_retrieve            | bold_window R^(20484 x T) + top_k + corpus  | top_k_text + top_k_score (Pearson r) + license
   cross_substrate_phi_report       | text + optional_eeg + optional_bold + set   | phi_per_substrate + verdict (CONSISTENT/MIXED/INCONSISTENT) + license
```

### §5.2 fixtures (synthetic only)

```
   fixture path                                                       | endpoint
   ------------------------------------------------------------------ | --------------------------------
   state/blm_phase3_cond4_fixtures/text_to_bold_synthetic.json        | text_to_bold_predict
   state/blm_phase3_cond4_fixtures/bold_to_text_synthetic.json        | bold_to_text_retrieve
   state/blm_phase3_cond4_fixtures/phi_report_synthetic.json          | cross_substrate_phi_report
```

모두 synthetic JSON (no real data). API surface validation 만 — model evaluation 측 NOT (raw#10 honest).

### §5.3 license attribution mandatory

- TRIBE v2 = CC-BY-NC-4.0 (research-only, commercial deploy **BLOCKED**)
- ZuCo = CC-BY-4.0 (OSF public)
- 3 endpoint 모두 `license_attribution` field MANDATORY
- 5-domain stretch (text->BOLD->stim 3-way, EEG->BOLD bridge) = post-Phase 4 only (cond.4 PASS 측 3-domain 확정)

---

## §6 cond.5 — decision matrix + entry-trigger contract (frozen)

### §6.1 entry trigger prereqs (3/3 MET 2026-05-03)

```
   id  | name                                              | status      | evidence
   --- | ------------------------------------------------- | ----------- | -----------------------------------------------------
   P1  | BLM Phase 1+2 landed                              | true        | docs/blm_stage12_landed_2026_05_03.ai.md (cond.1 met + blk.1 resolved)
   P2  | sister .roadmap.eeg cond.3 spec landed (Paradigm B)| true       | docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md (335L 9 sections)
   P3  | anima_phi_v3_canonical baseline reference frozen   | true       | tool/anima_phi_v3_canonical.hexa baseline 41.86
```

→ **entry authorization = GRANTED-ELIGIBLE 2026-05-03 (3/3 prereqs met)**

### §6.2 per-cond outcome tree (this cycle verdicts)

```
   cond                  | PASS criteria                                     | this cycle verdict
   --------------------- | ------------------------------------------------- | ------------------
   blm.phase3.cond.1     | spec doc + cross-link diagram disk-landed         | PASS
   blm.phase3.cond.2     | 3-substrate comparison table + tolerance band     | PASS
   blm.phase3.cond.3     | pre-register JSON + null plan + min-data plan     | PASS
   blm.phase3.cond.4     | API stub schema + 3-prompt fixture                | PASS
   blm.phase3.cond.5     | §4 + §5 frozen, sister cross-links emitted        | PASS
   ---                   | ---                                               | ---
   composite             | 5/5 PASS                                          | PASS
```

### §6.3 Phase 4 prerequisites (post-PASS, this cycle = ALL 5 cond met)

1. ALL 5 cond met — **ACHIEVED 2026-05-03**
2. BOLD raw data download SLA path (Courtois NeuroMod) green-lit — **separate decision, NOT this cycle**
3. HF `facebook/tribev2` pretrained weights downloaded + license CC-BY-NC-4.0 commercial-block accepted — pending
4. GPU budget approval ($500-2000 H100 LoRA path) — pending
5. F-CT-3 pre-register frozen + null distribution computed (cond.3 PASS prereq propagation) — frozen this cycle, computed = Phase 4

### §6.4 cost-band gate

```
   phase           | actual / required             | status
   --------------- | ----------------------------- | -----------
   Phase 3 actual  | $0 mac-local enforced         | DONE
   Phase 3 envelope| $0-50 (no GPU spend)          | within
   Phase 4 required| $500-2000 (H100 LoRA)         | separate authorization required
```

---

## §7 5-7 caveats (raw#10 honest C3) — 3 honest C3 caveats (this cycle scope)

1. **C1 — spec freeze != working brain LM** — 본 cycle 5/5 PASS = "measurement framework + integration spec + falsifier pre-register + API surface 측 ready". 실제 BLM training (cond.2 IMPL) + F-CT-3 measurement (cond.3 actual run) + cross-substrate phi value (cond.2 empirical) 모두 Phase 4 cycle 측 별도. raw#10 honest: zombie problem still applies (Paradigm B spec §0). PASS = necessary but NOT sufficient for any consciousness claim.

2. **C2 — CLM phi baseline 41.86 fragility (cond.2 reference)** — `anima_phi_v3_canonical` baseline 41.86 = CLM hidden state K=8 partitions 측 reference value, NOT ground truth. CP2-CLM Phase A ship_verdict VERIFIED-CLM-CP2-RED, F1_score_v2 = 0.408 raw / 0.12 F2-override (RED). cond.2 tolerance band 0.30 = placeholder. CP2-CLM Phase E binding evidence cycle 측 baseline downgrade 가능 → cond.2 tolerance band re-anchor 필요. spec freeze 측 41.86 lock-in != ground truth.

3. **C3 — F-CT-3 null distribution choice deferred to Phase 4** — cond.3 spec 측 block permutation OR phase-randomization 측 enumerate 만, 실제 1순위 결정 측 Phase 4 IMPL prep (honest C4 caveat 그대로). naive permutation 측 INVALID (BOLD HRF + EEG autocorrelation), 두 candidate 中 corpus-specific empirical decision 필요. 따라서 cond.3 PASS = pre-register schema frozen 측 충분 조건 만 충족, null choice empirical justification 측 Phase 4 prerequisite.

---

## §8 file index (relative to <user>/core/anima/)

### updated 1 .roadmap.* (in-place additive append only)

```
.roadmap.blm_brain_lm                                              (+5 phase3 cond entries appended; existing cond.1-3 + blk.1 unchanged)
```

### NEW 5 verifier override logs

```
state/blm_phase3_cond1_eeg_integration_log.jsonl                  (__BLM_PHASE3_EEG_INTEGRATION__ FROZEN)
state/blm_phase3_cond2_cross_substrate_log.jsonl                  (__BLM_PHASE3_CROSS_SUBSTRATE__ FROZEN)
state/blm_phase3_cond3_fct3_falsifier_log.jsonl                   (__BLM_PHASE3_FCT3_FALSIFIER__ FROZEN)
state/blm_phase3_cond4_api_stub_log.jsonl                         (__BLM_PHASE3_API_STUB__ FROZEN)
state/blm_phase3_cond5_decision_matrix_log.jsonl                  (__BLM_PHASE3_DECISION_MATRIX__ FROZEN)
```

### NEW 3 synthetic fixtures (cond.4 API stub)

```
state/blm_phase3_cond4_fixtures/text_to_bold_synthetic.json
state/blm_phase3_cond4_fixtures/bold_to_text_synthetic.json
state/blm_phase3_cond4_fixtures/phi_report_synthetic.json
```

### NEW handoff + marker

```
docs/blm_phase3_landed_2026_05_03.ai.md                            (이 파일)
state/markers/blm_phase3_landed.marker
```

### 본 cycle 이 reference 만 한 파일 (변경 0 byte)

```
docs/blm_phase3_spec_2026_05_03.md                                 (Phase 3 spec doc, 281L 5 cond)
docs/blm_stage12_landed_2026_05_03.ai.md                           (Phase 1+2 close handoff)
docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md                     (Paradigm B + 5-method phi proxy)
.roadmap.eeg                                                        (sister, in-place 변경 X)
.roadmap.anima_clm_eeg                                              (peer, in-place 변경 X)
.roadmap.i1_tribev2_pr                                              (TRIBE PR sister, in-place 변경 X)
.roadmap.n_substrate                                                (5+ substrate witness meta, in-place 변경 X)
.roadmap.clm                                                        (phi formula owner, in-place 변경 X)
references/tribev2/inventory.json                                   (TRIBE baseline SSOT)
references/tribev2/tribev2/utils_fmri.py                            (FSAVERAGE_5 mesh SSOT)
references/tribev2/tribev2/studies/algonauts2025.py                 (Friends s7 test split SSOT)
tool/anima_phi_v3_canonical.hexa                                    (phi formula reference, baseline 41.86)
```

---

## §9 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ----------------------------------------------------------
   1. icon                | [PASS 5/5] BLM Phase 3 spec FROZEN — Phase 4 entry GRANTED-ELIGIBLE
   2. analogy             | 셋째날 협업 명세서 동결 + API 견본 + 실패조건 사전 등록 + 다음날 진입 docket 통과
                          | 다른 부서 (CLM phi 공식, EEG ZuCo, qmirror IIT) SSOT 0 byte 건드리지 X
   3. core 결과            | 5/5 cond PASS, .roadmap.blm_brain_lm 5 entry append
                          | (1) EEG track 통합 spec, (2) 3-substrate phi consistency,
                          | (3) F-CT-3 falsifier 사전등록, (4) 3-domain API stub + fixture,
                          | (5) decision matrix + entry trigger contract
   4. 마이그레이션 0          | sister 5 .roadmap.* + tool/anima_phi_v3.hexa + references/tribev2/
                          | 모두 0 byte modification, additive only 정책 준수
   5. handoff path         | 본 ai.md = 다음 subagent / audit cron 측 Phase 4 entry SSOT
                          | + 5 verifier override log (FROZEN status) + 3 synthetic fixture
   6. 다음 step             | (1) Phase 4 entry decision (GPU budget approval $500-2000 H100 LoRA path)
                          | (2) cond.3 null distribution choice (block perm vs phase-rand) empirical justify
                          | (3) BOLD raw data download SLA (Courtois NeuroMod) decision
                          | (4) HF facebook/tribev2 weights download + license accept
                          | (5) sister .roadmap.eeg cond.4 phi proxy 1순위 (sample-partition phi) IMPL coordination
   7. cost                 | $0 mac-local enforced, no GPU, no training — destructive 0
                          | optional sanity probe 미수행 (5/5 PASS 달성 측 spec only 충족)
```

---

## §10 marker file path

`state/markers/blm_phase3_landed.marker`

(silent-land 방지 — handoff doc + .roadmap update + 5 verifier override log + 3 fixture + marker emit 의 11-way attestation)

---

## §11 omega-cycle compliance audit (6-step)

```
   step              | check
   ----------------- | ---------------------------------------------
   1. inventory      | docs/blm_phase3_spec_2026_05_03.md (281L) + 7 sister .roadmap.* read
                     | .roadmap.blm_brain_lm + .roadmap.eeg + .roadmap.anima_clm_eeg + .roadmap.i1_tribev2_pr +
                     | .roadmap.n_substrate + .roadmap.clm + nexus/.roadmap.qmirror
   2. propose        | 5 cond deliverable plan (per spec §2.2)
   3. apply          | 5 verifier log + 3 fixture + roadmap append + handoff doc + marker
   4. verify         | JSON valid (python json.loads PASS for 6 .jsonl + 3 fixture .json + 5 roadmap entries)
   5. honest C3      | 3 caveats (spec != working brain LM / CLM phi 41.86 fragility / null choice deferred)
   6. emit           | handoff doc + marker + 5 verifier logs + 3 fixtures (11-way attestation)
```

---

## §12 next-cycle recommendations (Phase 4 entry, 별도 cycle)

1. **Phase 4 entry authorization cycle** — GPU budget approval ($500-2000 H100 LoRA path) + Courtois NeuroMod BOLD raw data SLA decision + HF `facebook/tribev2` pretrained weights download + license CC-BY-NC-4.0 acceptance.

2. **cond.3 F-CT-3 null distribution empirical justification cycle** — block permutation vs phase-randomization 측 corpus-specific empirical decision (BOLD HRF autocorrelation profile + EEG temporal characteristic 측정 후 결정). Phase 4 IMPL prep prerequisite.

3. **sister .roadmap.eeg cond.4 phi proxy 1순위 (sample-partition phi on EEG) IMPL coordination cycle** — anima_phi_v3_canonical EEG-substrate port spec freeze (eeg.blk.4 resolution path) + anima-eeg-core/tool/modules/_metrics/ axis 자연 fit. BLM cond.2 cross-substrate consistency 측 EEG measurable substrate 확보.

4. **cond.2 tolerance band calibration cycle** — 3-substrate empirical phi measurement 후 |delta phi|/phi 0.30 placeholder → empirically calibrated band으로 re-anchor. CP2-CLM Phase E binding evidence cycle 결과 측 41.86 baseline confidence band 동기화.

5. **cond.4 5-domain stretch evaluation cycle** — Phase 4 PASS 후 (text->BOLD->stim 3-way + EEG->BOLD bridge) 2 domain 추가 측 cost/value 평가. cond.4 PASS criterion 측 3-domain 확정 (in-place 변경 X), 5-domain = 별도 stretch domain 추가.

6. **upstream `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 BLM rolling state update** — Phase 3 landed status 측 upstream handoff target update (additive only, sister 3-LM cycle aggregator 측 BLM Phase 3 PASS reflect).
