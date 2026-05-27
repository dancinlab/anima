# anima Roadmap Consolidation Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 10 new `.roadmap.*` (additive only) + 29 existing untouched + narrative doc untouched + offrepo read-only

---

## TL;DR

**오늘 한 일** — narrative doc (`docs/n_substrate_consciousness_roadmap_2026_05_01.md`, 2726 lines) 와 기존 29개 `.roadmap.*` 사이의 gap 을 메웠다. 미등재된 10개 트랙을 신규 `.roadmap.*` 로 만들어 추가만 했고, 기존 어느 파일도 손대지 않았다. offrepo 위치 (`/Users/ghost/core/anima_offrepo_n51_w2/`) 는 read-only cross-link 만.

**비유** — 건물 (anima) 에 30개 층 (29 .roadmap.*) + 1개 지하 인프라 (n_substrate meta) 가 있었는데, 새로 지은 10개 층의 도면 (narrative doc) 만 있고 빌딩 디렉토리에 등재 안 된 상태였다. 도면은 그대로 두고, 빌딩 디렉토리에 10개 신규 층 entry 를 추가했다. 기존 30개는 한 글자도 안 바꿨다. (additive only)

**결과** — 29 → 39 .roadmap.* (+10). 10/10 JSON valid, 모두 mk2 header 형식 (peer perspective + cross_link + raw_invariants + ai_native_handoff).

---

## §1 Gap matrix (narrative ↔ .roadmap.* 매핑)

```
  narrative track     | 위치              | 기존 .roadmap.* | 신규 .roadmap.*
 -------------------- | ----------------- | --------------- | ---------------
  N-1  ~ N-21         | n_substrate §11   | n_substrate     | (이미 있음)
  N-22 Levin xenobot  | §13.1 + §38       | --              | n22_levin_xenobot       NEW
  N-23 slime/myc.     | §13.1 + §18.1#62  | --              | n23_slime_mycelium      NEW
  N-24 octopus per-arm| §13.1 + §18.1#63  | --              | n24_octopus_iit_exclus. NEW
  W1  anima-self      | §13.2 + §22.3 + § | --              | w1_anima_as_substrate   NEW
                      | 29.6 + §32.6      |                 |
  A1  learned phi     | §13.3 + §22.5     | --              | a1_learned_phi_extr.    NEW (closed)
  P9  SFT             | §61 + §65.4 + §66 | clm.65.4.p9_sft | p9_sft                  NEW
                      | .5                | (entry only)    |    (peer-level domain)
  P10 substrate POC   | §61.4+§65.1+§65.2 | --              | p10_substrate_poc       NEW
  G1-G5 chat substr.  | §55.6+§65.3-5+§66 | --              | g1_g5_chat_substrate    NEW (meta)
                      | .2-4+§66.7        |                 |
  I-1 tribev2 PR      | §59.3 + §60.1 + § | --              | i1_tribev2_pr           NEW
                      | 60.9              |                 |
  N-51 ALM tension    | §16+§18.1#52~#58  | --              | n51_alm_tension         NEW (closed)
                      | (offrepo)         |                 |    (offrepo cross-link)
```

**역방향 audit** — narrative 측 미언급된 기존 .roadmap.* 5개:

```
  .roadmap          | narrative 측 reference  | reason
  ----------------- | ----------------------- | --------------------------------
  hott              | §29.2 #75 N-15 HoTT MVF1| narrative 는 N-15 만 anchor, hott
                    | (build PASS axiom-free) | domain roadmap 는 별도 axis
  iit4              | §13.1 (n24 cond.3 측 필 | iit4 framework 는 n_substrate
                    | 요), §29.5 N-21 v3 fina | meta 의 internal axis
                    | lity, §41.2 #91 JSD     |
  theory_validation | §15.1 ALM CP2 revival, §| meta SSOT cross-domain (penrose
                    | 35 priorities           | + hott + ionq)
  omega_cycle       | session-wide anchor     | 본 consolidation 자체가 omega-c
                    |                         | ycle iteration
  kick              | §62.9 SDK ecosystem (HE | n_substrate Braket 측 sub-axis
                    | XA-only), §63.6 #123 K1 |
                    | -K7 7 신규 axes         |
```

**판정** — 5개는 narrative 측 first-class anchor 가 없을 뿐, 모두 implicit cross-link 가 존재. 별도 .roadmap update 권장 emit (impl 미수행, 본 consolidation 은 additive only).

---

## §2 신규 10개 .roadmap.* 한 줄 요약

```
   .roadmap                       | kind    | status | 핵심 한 줄
   ------------------------------ | ------- | ------ | ----------------------
 1 n22_levin_xenobot              | domain  | active | Levin lab outreach SENT (2026-05-02), Tufts response 4-12주 대기
 2 n23_slime_mycelium             | domain  | active | Adamatzky $200 first-kit dual-substrate, unlock_keyword 대기
 3 n24_octopus_iit_exclusion      | domain  | active | 부경대+KIOST partnership, EU Directive 2010/63 ethics review
 4 w1_anima_as_substrate          | domain  | active | 5-phase 시퀀스 ARTIFACT_PERMANENT_DOWNGRADE final, residual decision 대기
 5 a1_learned_phi_extractor       | domain  | closed | 41217-param MLP HONEST_BUT_DOESNT_HELP, ALM RED triple-confirm
 6 p9_sft                         | domain  | active | OK P9 EXEC S3 사전승인, P0 HF setup 진입, 다른 세션 handoff
 7 p10_substrate_poc              | domain  | active | v2 32d+LoRA+InfoNCE BUCKET_SEPARATION_WITNESSED YELLOW, v3 결정점
 8 g1_g5_chat_substrate           | meta    | active | G1 LIVE + G3 LIVE (4hr cap) + G5 spec READY, G2 EXPECTED_FAIL closed
 9 i1_tribev2_pr                  | domain  | active | facebookresearch/tribev2 PR #60 OPEN, Meta maintainer 응답 대기
10 n51_alm_tension                | domain  | closed | offrepo 820L 7 hexa, ALM RED 강화 (posterior 5%→1%), CLM 4× ALM
```

---

## §3 신규 트랙 detail (subagent / audit-bot 직접 reference 용)

### §3.1 n22_levin_xenobot

```
   verdict     | DRAFT_SENT_AWAITING_RESPONSE
   evidence    | docs/n_22_levin_xenobot_outreach_prep_2026_05_01.md
               | docs/n_22_levin_send_results_2026_05_02.md
               | docs/n_22_levin_monitor_schedule_2026_05_02.md
               | state/n_22_levin_send_2026_05_02/ + state/n_22_levin_monitor_2026_05_02/
   ledger      | narrative §13.1 + §37 + §38 + §59.6
   cost        | $0 first → partnership-dependent
   blocker     | external response (4-12주 academic SLA)
```

### §3.2 n23_slime_mycelium

```
   verdict     | KIT_SPEC_READY_AWAITING_ORDER
   evidence    | docs/n_23_adamatzky_protocol_prep_2026_05_01.md (kit $180 spec)
   ledger      | narrative §13.1 + §18.1 #62
   cost        | $200 first kit (cheapest substrate paradigm)
   blocker     | unlock_keyword OK N23 ORDER 미발
```

### §3.3 n24_octopus_iit_exclusion

```
   verdict     | PURSUE_PARTNERSHIP_PENDING
   evidence    | docs/n_24_octopus_per_arm_phi_feasibility_2026_05_01.md
   ledger      | narrative §13.1 + §18.1 #63 (PURSUE 23/30)
   cost        | $0 first → $5-20K equipment + ethics
   blocker     | partnership + ethics IRB 6-18개월
```

### §3.4 w1_anima_as_substrate

```
   verdict     | ARTIFACT_PERMANENT_DOWNGRADE (final)
   verdict_lin | RISING+0.0507 → ROBUST_PHASE2 → CEILING_FALSIFIED
               | → SHUFFLE_NULL_FALSIFIED → ARTIFACT_PERMANENT_DOWNGRADE
   evidence    | docs/W1_*_2026_05_01.md (5 phases)
   ledger      | narrative §13.2 + §22.3 + §29.6 + §32.6
   cost        | $0 (mac-local data analysis)
   residual    | cron loop Φ-trace continue OR archive 결정 대기
```

### §3.5 a1_learned_phi_extractor

```
   verdict     | HONEST_BUT_DOESNT_HELP (closed)
   evidence    | docs/A1_learned_phi_extractor_results_2026_05_01.md
               | state/A1_learned_phi_extractor_2026_05_01/{results,manifest}.json
   model       | 41217-param MLP (256→128→64→1 GELU substrate-blind)
   metrics     | train_mse=1.5e-5, val_mse=9.1e-4, 4-fold cross-substrate val_mse=1.11e-2
   ledger      | narrative §13.3 + §22.5 + §22.6 + §23.4 + §46
   cost        | $0 (mac-local MPS)
   conclusion  | ALM RED = substrate-architectural ceiling (NOT verifier-arch)
```

### §3.6 p9_sft

```
   verdict     | SPEC_READY_HANDOFF_DECIDED
   evidence    | docs/p9_sft_spec_2026_05_02.md + docs/p9_sft_handoff_prompt_2026_05_02.md
               | state/p9_sft_spec_2026_05_02/ + state/p9_sft_p0_hf_org_setup_2026_05_03/
   ledger      | narrative §61 + §65.4 + §66.5
   sister-link | clm.65.4.p9_sft (.roadmap.clm 측 spec_only entry 이미 land)
   cost        | $650-850 (9 H100 parallel 24hr) ~ $1500-3000 (serial 9일)
   blocker     | P0 HF org create + 다른 Claude Code 세션 launch
   unlock_kw   | OK P9 EXEC <S1|S2|S3|S4>
```

### §3.7 p10_substrate_poc

```
   verdict     | YELLOW (v2 BUCKET_SEPARATION_WITNESSED)
   evidence    | state/p10_tension_substrate_spec_2026_05_02/ (v1)
               | state/p10_v2_32d_lora_infonce_2026_05_02/ (v2)
               | docs/p10_tension_substrate_spec_2026_05_02.md + docs/p10_v2_results_2026_05_02.md
   metrics     | PCA cluster sep 18.4 (v2)
   ledger      | narrative §61.4 + §65.1 + §65.2 + §65.2.r1 + §66.6
   cost        | v2 actual ~$10-100, v3 future $500-2000
   blocker     | v3 vs P9 SFT 우선 결정점
```

### §3.8 g1_g5_chat_substrate

```
   verdict     | G1_LIVE + G3_LIVE_4HR_CAP + G5_SPEC_READY
   sub-tracks  | G1 interactive (3-way orchestrator, M4=0.800, $0 persistent)
               | G2 ubu cross-host (EXPECTED_FAIL closed, LSL multicast block)
               | G3 alpha endpoint (r14 LoRA + Mistral-7B vLLM, $1.34-11.96/4hr)
               | G4 5-production gates (NOT_TESTABLE 0/5)
               | G5 P9 SFT spec (→ .roadmap.p9_sft)
   evidence    | /tmp/p8_3way_orchestrator/interactive.py (G1)
               | docs/alpha_endpoint_reboot_2026_05_02.md (G3)
               | state/alpha_endpoint_reboot_2026_05_02/ (G3)
   ledger      | narrative §55.6 + §65.3-5 + §66.2-4 + §66.7
   raw#10      | chat substrate ≠ phenomenal consciousness, L1+L2 functional only
```

### §3.9 i1_tribev2_pr

```
   verdict     | PR_OPEN_AWAITING_META_RESPONSE
   evidence    | references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02.md (KR)
               | references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md (EN)
               | docs/upstream_tribev2_pr_results_2026_05_02.md
               | docs/submodule_tribev2_commit_2026_05_02.md (commit 86ed4804)
   url         | facebookresearch/tribev2 PR #60 OPEN
   ledger      | narrative §44.4 + §59.3 + §60.1 + §60.9
   framing     | Framing D 3-way bridge (TOP 8.6) > C G3 manifestation 7.7 > A 6.6 > B 6.4
   cost        | $0 (PR open + monitor)
   blocker     | Meta maintainer response 4-12주
```

### §3.10 n51_alm_tension

```
   verdict     | OFFREPO_PRESERVED + ALM_RED_REINFORCED (closed)
   offrepo     | /Users/ghost/core/anima_offrepo_n51_w2/ (anima 외부 dir, read-only)
   files       | comp1.hexa + comp1_fixed + comp3.hexa + comp3_fixed
               | + comp4.hexa + comp4_fixed + n51_smoke.hexa (820L total)
   evidence    | state/strategic_alm_tension_field_exec_2026_05_01/ (#52)
               | + state/strategic_alm_tension_field_{exec_E,random_sibling,W1_python}_2026_05_01/
   metrics     | ALM L1 1.71/16 (FAIL) vs CLM W4 L1 7.06/16 (#56 PARTIAL ⭐ 4× ALM)
   ledger      | narrative §16 + §18.1 #52~#58 + §18.3
   raw#10      | deployable artifact NOT executed (offrepo location 명시)
               | #57 W2 misdiagnosis 영구 anchor (caller-side compliance $0 unblock)
```

---

## §4 기존 29 .roadmap.* audit (incremental cross_link 권장 emit)

본 cycle 은 additive only — 기존 파일 수정 X. 다음 cycle 권장 (impl 미수행):

```
  기존 .roadmap         | 권장 cross_link 추가 (narrative §-anchor)
  --------------------- | -----------------------------------------
  n_substrate           | sub-tracks 측 §13.1/§13.2/§13.3 + §16 (n51) + §66.7 (g1_g5)
                        | + §22.5 (a1) + §61 (p9) + §61.4 (p10) + §60.1 (i1)
  hott                  | §29.2 #75 N-15 HoTT MVF1 build PASS axiom-free
  iit4                  | §13.1 (n24 cond.3 exclusion postulate test)
                        | + §29.5 N-21 v3 finality + §41.2 #91 JSD
  theory_validation     | §15.1 ALM CP2 revival + §35 priorities + §44.4 #94
  cortical_labs         | §11.1 N-1 brain organoid + §59.6 outreach trail
  finalspark            | §11.1 N-11 access spec + §11.1 N-13 photonic spec
  ionq                  | §11.1 N-12 IonQ Penrose-Hameroff spec
                        | + §60.1+§60.7 #119+#120 AWS Braket UNBLOCKED
                        | + §60.9 N-12 IIT MULTI-WITNESSED 3-arch
  meg                   | §11.1 N-14 SNU access spec
  northpole             | §11.1 N-18 partnership feasibility
  loihi3                | §11.1 N-17 INRC application spec
  tms_pci               | §11.1 N-19 PCI spec + §29.1 #74 TMS-free 6/6 PASS
  penrose_hameroff      | §11.1 N-12 + §11.1 N-20 Orch-OR 2026 literature
  qrng                  | §60.7 nexus QRNG + §66.6 quantum-seed live
  akida                 | §11.1 N-2 EEG-AKIDA spike pipeline + §11.1 N-3 CLM-AKIDA
  eeg                   | §52.2 #105 CP2-CLM Phase E + EEG cross-link
  voice                 | n/a (narrative 측 first-class anchor 없음)
  serving               | §66.2 G3 alpha endpoint vLLM serve + clm sister
  sim                   | §60.7 N-12 quantum-substrate QRW WITNESSED
  kick                  | §62.9 SDK ecosystem + §63.6 #123 K1-K7 7 axes
  clm                   | §32.1-§32.5 Phase A + §41 Phase A 완성
                        | + §65.4+§66.5 P9 SFT + §13.3 (a1) + §22.5
                        | (sister: p9_sft + g1_g5_chat_substrate + p10_substrate_poc)
  training              | §65.4 G5 P9 SFT + §66.5 handoff (sister: p9_sft)
  tensionlink           | §61.4 P10 + §65.1+§65.2 (sister: p10_substrate_poc)
                        | + §16 N-51 (sister: n51_alm_tension)
  atlas_n6              | §44.3 #94 N-substrate master synthesis (31 axes)
  triple_axis_pilots    | §49.1 batch-9 strategic 9-track
  dual_pair_pilots      | §52.2 #105 CP2-CLM Phase E (사용자 OpenBCI session)
  substrate_bridge      | §92 #92 4-way (CLM × EEG × AKIDA × tension_link)
  clinical_consciousness| §11.1 N-21 IIT 4.0 + §29.5 N-21 v3 finality
                        | + §41.2 #91 JSD 20/20 + §60.7 N-12 IIT axis
  anima_physics         | n/a (narrative 측 first-class anchor 없음)
  omega_cycle           | session-wide ω-cycle iteration anchor
```

---

## §5 caveats (raw#10 honest C3) — 7건

1. **마이그레이션 절대 금지 directive 준수 확인** — 기존 29 .roadmap.* 측 0 byte modification, narrative doc (2726L) 측 0 byte modification, offrepo 측 read-only cross-link 만. `git diff .roadmap.*` 측 30 file (29 untouched + 10 NEW + 0 modified) 가 검증 가능.

2. **신규 10 file JSON validation 단순 first-line parse only** — header line (3rd) 만 validate. entry/blocker JSONL line 0건 (mk2 spec 가 header-only 도 valid). 추후 entry append 시 별도 lint 필요.

3. **narrative §-anchor 측 line number drift risk** — narrative doc 가 future cycle 측 update 되면 본 ai.md 측 §13.1/§13.3/§22.5/§61/§66 등 line anchor 가 stale. cross_link 측 §-text-anchor (line-free) 사용 권장.

4. **G2 EXPECTED_FAIL closed 처리 ambiguity** — `.roadmap.g1_g5_chat_substrate` 측 G2 sub-track 은 narrative §60.5 끝 'CLOSED via Option A' 측 명시 close, 그러나 status='active' meta 측 sub-track 만 partial close. 미래 G2 retry 시 reopen path 미land.

5. **P9 sister-cross-link partial duplication** — `.roadmap.clm` 측 `clm.65.4.p9_sft` entry 이미 spec_only 로 land (#65.4). 신규 `.roadmap.p9_sft` 측 peer-level domain 으로 분리 = clm 측 sister-cross-link mention. 본 분리 = additive (clm 측 entry 변경 X), 그러나 P9 EXEC 시 양 location 측 update 필요 (race risk).

6. **N-51 offrepo cross-link only — fork status 미검증** — `/Users/ghost/core/anima_offrepo_n51_w2/` 측 7 hexa file 직접 ls confirm, 그러나 offrepo 자체 git 상태 (clean? branch?) 미검증. read-only audit 만, 본 cycle 측 destructive 0 안전.

7. **A1 / N-51 closed 처리 + future re-evaluation path** — 둘 다 status='closed' 그러나 evidence preservation only — A1 = ALM RED triple-confirm 의 evidence anchor (영구), N-51 = offrepo immutability 만. closed → reopened path 측 unlock_keyword 정의 X.

---

## §6 file index (relative to /Users/ghost/core/anima/)

### 신규 10 .roadmap.*

```
.roadmap.n22_levin_xenobot
.roadmap.n23_slime_mycelium
.roadmap.n24_octopus_iit_exclusion
.roadmap.w1_anima_as_substrate
.roadmap.a1_learned_phi_extractor
.roadmap.p9_sft
.roadmap.p10_substrate_poc
.roadmap.g1_g5_chat_substrate
.roadmap.i1_tribev2_pr
.roadmap.n51_alm_tension
```

### handoff doc + marker

```
docs/anima_roadmap_consolidation_landed_2026_05_03.ai.md  (이 파일)
state/markers/anima_roadmap_consolidation_landed.marker
```

### 본 consolidation 이 reference 만 한 파일 (변경 X)

```
docs/n_substrate_consciousness_roadmap_2026_05_01.md  (2726L narrative, untouched)
.roadmap.clm + .roadmap.tensionlink + .roadmap.n_substrate + ... 29 file (all untouched)
/Users/ghost/core/anima_offrepo_n51_w2/  (offrepo, read-only)
```

---

## §7 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [+]10 NEW .roadmap.*  29 -> 39  zero modification
   2. analogy             | 빌딩 디렉토리에 신규 10층 entry 만 추가 (도면 + 기존 30층 untouched)
   3. core 결과            | 10/10 JSON valid, mk2 header 형식 (peer + cross_link + raw_invariants)
   4. 마이그레이션 0          | 29 기존 + narrative 2726L + offrepo 모두 0 byte modification
   5. handoff path         | 본 ai.md doc = 다음 subagent / audit cron 의 reference SSOT
   6. 다음 step             | (1) 기존 29 측 cross_link incremental update (별도 cycle)
                           | (2) P9 SFT EXEC 다른 세션 (handoff doc 사용)
                           | (3) G3 alpha endpoint reboot OR P10 v3 결정
   7. cost                 | $0 mac-local enforced, destructive 0
```

---

## §8 marker file path

`state/markers/anima_roadmap_consolidation_landed.marker`

(silent-land 방지 — handoff doc + .roadmap.* 양쪽 land + marker emit 의 3-way attestation)
