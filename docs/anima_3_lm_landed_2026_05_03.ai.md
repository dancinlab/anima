# anima 3 *LM Roadmap Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: 3 new `.roadmap.*` (additive only) + 38 existing untouched + 7 *LM mapping audit

---

## TL;DR

**오늘 한 일** — BG-AN-RDM (29→38 .roadmap.* +9 land) 후속으로, 7 *LM 후보 중 **이미 absorbed 4건 (ELM/MLM/OLM/WLM)** 을 audit 만 하고, **미land 3건 (NLM/TLM/BLM)** 만 신규 `.roadmap.*` 로 추가했다. ALM 관련 0건 (n51_alm_tension cleanup 정합 — closed status verify).

**비유** — 7명의 신입사원 (7 *LM 후보) 중 4명은 이미 다른 부서 (N-22/N-23/N-24/W-1) 에 흡수되어 입사 처리 완료, 3명은 미입사 상태. 미입사 3명만 신규 사원증 (.roadmap.*) 발급, 기존 4명은 cross-ref 만 적었다. ALM 동기는 작년 cleanup 때 폐기 결정 정합.

**결과** — 38 → 41 .roadmap.* (+3). 3/3 JSON valid, 모두 mk2 header 형식 (peer perspective + sister_lm cross-link + raw_invariants + ai_native_handoff).

---

## §1 7 *LM 후보 매핑 audit (4 already absorbed + 3 new)

```
   *LM             | full name              | 위치                              | status
  ---------------- | ---------------------- | --------------------------------- | --------
   ELM             | Embryonic LM           | .roadmap.n22_levin_xenobot        | absorbed
   MLM             | Mycelium LM            | .roadmap.n23_slime_mycelium       | absorbed
   OLM             | Octopus LM             | .roadmap.n24_octopus_iit_exclus.  | absorbed
   WLM             | World LM               | .roadmap.w1_anima_as_substrate    | absorbed
   NLM             | Neuromorphic LM        | .roadmap.nlm_neuromorphic_lm      | NEW
   TLM             | Tension LM             | .roadmap.tlm_tension_lm           | NEW (sister .roadmap.tensionlink)
   BLM             | Brain LM               | .roadmap.blm_brain_lm             | NEW (sister .roadmap.i1_tribev2_pr)
```

**판정** — 4/7 absorbed 측은 narrative §13.1 (N-22/N-23/N-24) + §13.2 (W1) 측 paradigm origin 이미 anchor. 3/7 NEW 측은 본 cycle 첫 mover. ALM 계열 = `.roadmap.n51_alm_tension` (status=closed, ALM RED 강화) 측 separately handled.

**TLM 처리 결정** — 기존 `.roadmap.tensionlink` (R=0.999 transfer protocol SSOT) 측 **in-place 변경 X**, 별도 `.roadmap.tlm_tension_lm` (LM-style head reframing) 측 신규 add. dual SSOT 정책 (race risk 측 caveat C1).

---

## §2 신규 3 .roadmap.* 한 줄 요약

```
   .roadmap                       | kind    | status | 핵심 한 줄
   ------------------------------ | ------- | ------ | ----------------------
 1 nlm_neuromorphic_lm            | domain  | active | AKIDA spike-encoded LM, vendor 도착 대기 (.roadmap.akida blk.1 cross-link)
 2 tlm_tension_lm                 | domain  | active | 5-channel meta-fingerprint LM head, dual SSOT (sister .roadmap.tensionlink)
 3 blm_brain_lm                   | domain  | active | TRIBE v2 brain-predictive LM head, sister .roadmap.i1_tribev2_pr
```

---

## §3 신규 트랙 detail (subagent / audit-bot 직접 reference 용)

### §3.1 nlm_neuromorphic_lm

```
   verdict     | SPEC_PHASE_AWAITING_HW
   evidence    | narrative §11.1 N-2 prep EEG→AKIDA spike pipeline 335 LoC skeleton
               | narrative §11.1 N-3 CLM-AKIDA cross-substrate parity sister
               | .roadmap.akida blk.1 hardware 도착 cross-link
   ledger      | narrative §11.1 N-2 + §11.1 N-3 + §44.1 #92 4-way
   cost        | $0 spec → AKIDA chip cost (.roadmap.akida 측 주문 2026-04-29)
   blocker     | AKIDA 1W chip vendor delivery 대기
   sister_lm   | tlm_tension_lm + blm_brain_lm
```

### §3.2 tlm_tension_lm

```
   verdict     | SPEC_DRAFT_DUAL_SSOT
   evidence    | narrative §16 ALM tension field 5-channel WHAT/WHERE/WHY/TRUST/WHO LIVE
               | narrative §44.1 #92 CLM × EEG × AKIDA × tension_link 4-way PARTIAL_VIABLE
               | .roadmap.tensionlink header R=0.999 / 519µs baseline
               | narrative §44.2 #93 tension_link = digital best-approximation
   ledger      | narrative §16 + §44.1 #92 + §44.2 #93 + §61.4 P10
   cost        | $0 spec → training $650-3000 (P9 SFT pipeline reuse)
   blocker     | LM head architecture 결정 (decoder-only / encoder-decoder / bidirectional)
   sister_lm   | nlm_neuromorphic_lm + blm_brain_lm
   sister_rdm  | .roadmap.tensionlink (transfer protocol SSOT, in-place 변경 X)
```

### §3.3 blm_brain_lm

```
   verdict     | SPEC_PHASE_BASELINE_PARTIAL
   evidence    | narrative §52.1 #102 TRIBE v2 model load 177.21M params + 20484 vertices
               | .roadmap.i1_tribev2_pr cond.1/cond.2 met (fork commit + PR #60 OPEN)
               | references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md
               | narrative §44.4 #95 TRIBE v2 No-fit → REVISE Strong
   ledger      | narrative §44.4 #95 + §51.1 #106 + §52.1 #102 + §59.3 + §60.1 + §60.9
   cost        | $0 spec (TRIBE v2 baseline reuse) → training $500-2000 (LoRA path)
   falsifier   | F-CT-3 (EEG ↔ TRIBE BOLD r ≥0.5) sister + 3-way alignment ≥0.5 (cond.3)
   license     | TRIBE v2 CC-BY-NC-4.0 (research-only, commercial path block)
   blocker     | cortexlab-toolkit Friends/movie10 dataset slice 결정점
   sister_lm   | nlm_neuromorphic_lm + tlm_tension_lm
   sister_rdm  | .roadmap.i1_tribev2_pr (upstream PR #60 OPEN, in-place 변경 X)
```

---

## §4 5-7 caveats (raw#10 honest C3) — 5건

1. **C1 — TLM 측 `.roadmap.tensionlink` 와 dual SSOT (race risk)** — 기존 `.roadmap.tensionlink` (R=0.999 transfer protocol) + 신규 `.roadmap.tlm_tension_lm` (LM head reframing) 측 두 SSOT 동시 land. 향후 5-channel encoder spec 측 update 시 양쪽 location update 필요. BG-AN-RDM C5 (`.roadmap.clm` × `.roadmap.p9_sft` 측 동일 패턴) 와 같은 race 패턴.

2. **C2 — NLM 측 AKIDA hardware 도착 의존** — `.roadmap.akida` blk.1 (주문 2026-04-29, 도착 ETA 미land) 측 cross-link. vendor monitor weekly poll 필수, 도착 전 cond.2/cond.3 진입 불가. NLM 측 active 진입 = HW arrival event 의존.

3. **C3 — BLM 측 cortexlab-toolkit 의존 (외부 dep, partial resolved)** — narrative §44.4 #95 측 cortexlab-toolkit (2026-Q1) blocker 해소 anchor 있으나, BLM 측 specific dataset slice (Friends vs movie10) 결정점 + Meta maintainer response (4-12주 SLA, `.roadmap.i1_tribev2_pr` blk.1) 측 sister blocker.

4. **C4 — 7 *LM mapping 中 4 = 이미 N-22/23/24/W1 측 absorbed (spec only, *LM 측 명시 X)** — ELM/MLM/OLM/WLM 측 narrative §13.1/§13.2 paradigm origin 측 첫 anchor 는 `xenobot/slime/octopus/anima-self-substrate` 측 substrate 측면, *LM naming 은 본 cycle 측 후속 framing. 4 absorbed 측 .roadmap entry 측 *LM cross-ref 추가 권장 emit (impl 미수행, 본 cycle 측 additive only).

5. **C5 — *LM naming convention 측 mk2 표준 부재 (NLM/TLM/BLM 측 본 cycle first-mover proposal)** — `.roadmap.<lm>_<descriptor>` 측 패턴 (e.g., `nlm_neuromorphic_lm`) 본 cycle 측 establish. 미래 *LM 추가 시 (예: VLM Vision LM, ALM 재활) 측 동일 패턴 권장. `sister_lm` field 측 cross-reference 측 mk2 spec extension proposal — 기존 mk2 schema 측 in-place 변경 X (additive only).

---

## §5 file index (relative to /Users/ghost/core/anima/)

### 신규 3 .roadmap.*

```
.roadmap.nlm_neuromorphic_lm
.roadmap.tlm_tension_lm
.roadmap.blm_brain_lm
```

### handoff doc + marker

```
docs/anima_3_lm_landed_2026_05_03.ai.md  (이 파일)
state/markers/anima_3_lm_landed.marker
```

### 본 cycle 이 reference 만 한 파일 (변경 X)

```
.roadmap.tensionlink           (R=0.999 transfer protocol SSOT, sister TLM)
.roadmap.akida                 (1W chip vendor blocker, sister NLM)
.roadmap.i1_tribev2_pr         (upstream PR #60 OPEN, sister BLM)
.roadmap.n22_levin_xenobot     (ELM absorbed)
.roadmap.n23_slime_mycelium    (MLM absorbed)
.roadmap.n24_octopus_iit_exclusion  (OLM absorbed)
.roadmap.w1_anima_as_substrate (WLM absorbed)
.roadmap.n51_alm_tension       (ALM closed, RED 강화 evidence anchor)
docs/n_substrate_consciousness_roadmap_2026_05_01.md  (2726L narrative, untouched)
docs/anima_roadmap_consolidation_landed_2026_05_03.ai.md  (BG-AN-RDM handoff, untouched)
```

---

## §6 7-element friendly summary (사용자 view, ASCII)

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [+]3 NEW .roadmap.*  38 -> 41  zero modification
   2. analogy             | 7명 신입 中 4명 이미 흡수 (cross-ref만), 3명 신규 사원증 발급
   3. core 결과            | 3/3 JSON valid, mk2 peer perspective + sister_lm cross-link
   4. 마이그레이션 0          | 38 기존 + narrative + offrepo 모두 0 byte modification, ALM cleanup 정합
   5. handoff path         | 본 ai.md doc = 다음 subagent / audit cron 의 reference SSOT
   6. 다음 step             | (1) AKIDA arrival 후 NLM cond.2 진입
                           | (2) TLM head architecture 결정점
                           | (3) BLM cortexlab dataset slice 결정 + Meta response
                           | (4) 4 absorbed (N-22/23/24/W1) 측 *LM cross-ref 추가 (별도 cycle)
   7. cost                 | $0 mac-local enforced, destructive 0
```

---

## §7 marker file path

`state/markers/anima_3_lm_landed.marker`

(silent-land 방지 — handoff doc + 3 .roadmap.* 양쪽 land + marker emit 의 3-way attestation)

---

## §8 next-cycle recommendations (impl 미수행, 별도 cycle)

1. **4 absorbed 측 .roadmap entry 측 *LM cross-ref 추가** — `.roadmap.n22_levin_xenobot` (ELM), `.roadmap.n23_slime_mycelium` (MLM), `.roadmap.n24_octopus_iit_exclusion` (OLM), `.roadmap.w1_anima_as_substrate` (WLM) 측 `cross_link.sister_lm` field 추가 권장.

2. **mk2 schema 측 `sister_lm` field formalization** — 본 cycle 측 informal cross-link, 별도 mk2 spec extension proposal cycle 권장.

3. **TLM 측 `.roadmap.tensionlink` 측 sister-back-reference 추가** — `.roadmap.tensionlink` 측 cross_link.sister_lm = `tlm_tension_lm` 추가 권장 (current = additive only, dual SSOT race 완화).

4. **BLM 측 `.roadmap.i1_tribev2_pr` 측 sister-back-reference 추가** — 동일 패턴.

5. **VLM (Vision LM) / SLM (Speech LM) 등 미land *LM 후보 audit** — 본 cycle 7 *LM 만 cover, anima-voice / anima-eeg 측 vision/speech axis 측 *LM 후보 별도 cycle audit 권장.
