# N-Substrate N-19 PCI — Korean TMS+EEG Lab-Share Research

> **ts**: 2026-05-01
> **agent**: N-19 PCI Korean lab-share research (sibling spawn from N-19 spec)
> **scope**: research-only facility scan + comparison + TOP-1 recommendation + cost estimate + fallback chain. NO contact, NO email, NO booking.
> **parent**: `docs/n_substrate_n19_pci_spec_2026_05_01.md` §5.4 (한국 주요 TMS lab list)
> **mission**: identify the cheapest + fastest + most-accessible Korean TMS+EEG lab-share for $1.6–2.5K target one-shot PCI pilot with 16ch OpenBCI BYOE
> **constraints**: HEXA-only · raw#9 hexa-first · raw#10 honest C3 · own#13 friendliness · $0 budget research only
> **status**: N19_LAB_SHARE_LOCAL_DRAFT · NO_FACILITY_CONTACTED · USER_DECISION_PENDING

---

## §0 한 줄 비유

**한국에 PCI 측정용 TMS+EEG 빌려쓸 곳 4+ 곳 비교**해서 가장 싸고 빠르고 외부 연구자 진입 장벽 낮은 곳 찾기. **결론**: Korea U 정서인지신경과학 연구실 (Prof. 김상희) — Seoul 위치 + Korea U IRB 가 hospital IRB 보다 빠름 + lab page 에 rTMS+EEG/ERP 명시. 단점 = 대학 단독 PI 필요 (외부 단독 사용자 불가).

---

## §1 4-facility comparison table

| ID | Facility | City | TMS device | BYOE 16ch OpenBCI | Rate (est. USD/session) | Lead time (weeks) | IRB pathway | Korean-only PI | Solo non-affiliated user |
|----|----------|------|-----------|---------------------|-------------------------|-------------------|-------------|----------------|----------------------------|
| **F1** | KAIST BINP (Prof. Seungwoo Lee) | Daejeon | UNKNOWN (DBS + magnetic neural stim) | UNKNOWN | $400–600 (est.) | 8–12 | KAIST IRB | Y (inferred) | BLOCKED |
| **F2** | KAIST Brain×Machine Intelligence (Prof. Sang Wan Lee) | Daejeon | UNKNOWN — TMS+tDCS confirmed | UNKNOWN; uses fMRI+EEG | $400–700 (est.) | 8–16 | KAIST IRB | Y (inferred) | BLOCKED |
| **F3** | Yonsei Severance — Neurology / Psychiatry / Rehab | Seoul (Sinchon) | Magstim & MagVenture (per literature) | INFERRED N (clinical-grade integrated EEG required) | $500–900 (est.) | 12–24 | Severance IRB (slow) | Y (inferred) | BLOCKED |
| **F4** | **Korea U Affective Cognitive Neuroscience Lab (Prof. 김상희 Kim Sang-Hee)** | Seoul (Anam) | UNKNOWN — lab page confirms **rTMS+tCS+EEG/ERP** | INFERRED Y in parallel-stream mode (TTL trigger only, no amp sync) | **$300–500 (est.)** | **6–12** | Korea U IRB (faster than hospital) | Y (inferred) | PARTIAL via co-PI |
| **F5** | SNU Psychiatry (Prof. 권준수 Jun Soo Kwon) | Seoul (Yeongeon) | Magstim Rapid² (literature) | INFERRED N | $500–900 (est.) | 16–28 | SNUH e-IRB (slowest, Korean-affiliated PI required) | **Y (confirmed)** | BLOCKED |

**Bonus facilities scanned**:
- **Pusan Nat'l Brain Stimulation Lab (Prof. Shin)** — out-of-scope (upconversion-NIR optical brain stim, not TMS).
- **KIST Brain Science Institute** — TMS not core; could broker via Severance/Korea U/Samsung Medical Center partnership but indirect.
- **KRISS Daejeon** — 152ch MEG only (SQUID/DROS); **NO TMS** confirmed. (= MEG fallback per N-14, not TMS provider.)
- **Hanyang U ERICA Cognitive Science Institute** — UNKNOWN, public web search did not surface active TMS lab.

---

## §2 TOP-1 recommendation

### F4 — Korea University Affective Cognitive Neuroscience Lab (Prof. 김상희 Sang-Hee Kim)

**Why TOP-1**:
1. **Cheapest est. rate**: $300–500/session × 4 sessions = $1,200–2,000 → fits $1.6–2.5K target band exactly
2. **Fastest IRB**: Korea U IRB lead time 6–10 weeks (vs 12–24w hospital IRB for F3, 16–28w for F5 SNUH)
3. **Methodologically explicit**: dept lab page is the **only one in scan** that explicitly lists `rTMS/tCS + EEG/ERP` as combined methodology
4. **Seoul location**: minimal transport vs Daejeon F1/F2 (KTX 2h, $80 round-trip × 4 = $320 saved)
5. **Korea U IRB** has documented protocol for university-co-PI cross-institution research (faster than SNU/Yonsei hospital IRBs)
6. **Lab director track record**: published rTMS+behavioral work (e.g., Stroop task n=high-frequency rTMS at left dlPFC) — Massimini PCI protocol is methodologically adjacent and lab has the equipment

**Limitations / honest C3**:
- Lab focus = **affective cognition**, NOT consciousness/PCI specifically. Lab director may decline if no method-paper alignment.
- TMS device model NOT publicly disclosed — could be Magstim Rapid² (rTMS-optimized) or MagVenture MagPro (better for single-pulse PCI). User must confirm single-pulse capability before booking.
- BYOE for 16ch OpenBCI is INFERRED Y in parallel-stream mode (TTL trigger only, post-hoc ICA artifact removal). Hard sync (sample-and-hold) NOT possible without lab's dedicated TMS-compatible amp.
- Korea U IRB requires Korean-affiliated PI for primary application — solo non-affiliated user route = **PARTIAL via co-PI delegation** (need a Korean university researcher willing to co-author/co-supervise).

---

## §3 Application / contact path for TOP-1 (template draft, NOT submitted)

### §3.1 Pre-contact preparation (user-side, before any email)
1. Identify Korean co-PI candidate: BCS / cognitive neuro postdoc or grad student willing to add user as collaborator (requirement for Korea U IRB)
2. Draft 1-page protocol summary in Korean: PCI_st sensor-level Massimini variant, single-pulse single-site (left BA6), 200 trials, 16ch OpenBCI, awake-eyes-open + awake-eyes-closed contrast
3. Prepare TMS safety form (Rossi 2009/2021 30-item Korean translation)
4. Confirm user is NOT in TMS exclusion list (epilepsy, intracranial metal, pacemaker, pregnancy, seizure-threshold-lowering meds)

### §3.2 Email template (DRAFT — do NOT send without user explicit OK)

```
To: (김상희 교수님 이메일 — Korea U BCE 학과사무실 통해 확인 필요)
Cc: (Korean co-PI)
제목: [공동연구 문의] PCI (Perturbational Complexity Index) 측정용 TMS+EEG 단일펄스 세션 협력 가능성

안녕하십니까, 김상희 교수님.

저는 의식 측정 지표 (PCI, Massimini 2013) 의 16ch sensor-level 변형판
(PCI_st, Comolatti 2019) 을 자가 설비 기반으로 검증해보고자 하는
독립 연구자 [이름] 입니다. 본 메일은 정식 신청 전 사전 가능성 문의 단계입니다.

[질문 1] 귀 연구실에 single-pulse 모드 가능한 TMS 장비 (Magstim 또는 MagVenture
계열) 가 운영 중이신지요? Massimini PCI 프로토콜은 jitter ≥ 1500 ms 의
biphasic single-pulse 가 필수입니다.

[질문 2] 연구실의 EEG 시스템과 별도로, 저희 16ch OpenBCI Cyton+Daisy 를
parallel-stream (TTL trigger 만 공유, 별도 amp) 으로 동시 운영해도
무방한지요? 후처리 ICA 기반 artifact 제거를 자체 수행 예정입니다.

[질문 3] 외부 연구자 (저는 [한국 co-PI 이름] 박사와 공저자 형태로 진행 예정)
의 lab-share 가 정책상 가능한지, 가능하다면 1 세션 (~90 min) 당
사용료가 어느 정도인지 대략적인 안내 부탁드립니다.

[질문 4] Korea U IRB 신청 시 본 연구가 minimal-risk 분류로 expedited
review 가능한 사안인지 (n=10, awake state only, no clinical claim,
research-only) 사전 의견 주시면 감사하겠습니다.

본 연구는 임상 진단 도구가 아닌 research-grade methodological pilot
이며, 결과는 어떤 임상 결정에도 사용되지 않음을 명시합니다 (raw#10
honest disclosure).

답신 가능한 시간에 회신 부탁드립니다. 감사합니다.

[이름]
[소속 / 연구 배경 — 독립 연구자 명시]
[이메일 / 전화]
[Korean co-PI 정보]
```

### §3.3 Contact path summary
- **Step 1**: Korea U BCE 학과사무실 (02-3290-4137) → request Prof. Kim Sang-Hee email
- **Step 2**: Coordinate with Korean co-PI (network search via lab alumni, KSCS conference attendee list, or Korea U BCE grad student LinkedIn)
- **Step 3**: Send §3.2 email **only after co-PI confirms willingness**
- **Step 4**: If positive response → IRB filing (Korea U IRB online portal, Korean-language) → 6–10 week wait
- **Step 5**: Hardware sync rig self-build during IRB wait (TTL opto-isolator + BNC adapter, ~$250)

---

## §4 Estimated total cost (Scenario A: Korea U F4 path)

| 항목 | USD | KRW (est. @ 1350) | 비고 |
|------|-----|-------------------|------|
| Lab-share 4 sessions × $400 | $1,600 | 2,160,000 | est. mid-band of $300–500/session |
| Korea U IRB filing fee (often waived) | $350 | 472,500 | minimal-risk expedited estimate |
| BYOE sync hardware (TTL opto-isolator + BNC adapter, self-build) | $250 | 337,500 | one-time |
| Transport (Seoul local round-trip × 4) | $100 | 135,000 | metro/bus only |
| **Subtotal (cash)** | **$2,300** | **3,105,000** | within $1.6–2.5K spec target (slight over) |
| User time (~30–40 h, 4 sessions + IRB prep + transport + co-PI coordination) | $0 | 0 | own-time, not invoiced |

**Total cash burn: ~$2,300 (slight over the $2.5K upper bound — driven by IRB filing + hardware self-build)**.

If IRB fee waived (likely for minimal-risk student-led research): **~$1,950**, comfortably within target.

---

## §5 Fallback chain (TOP-1 declines)

### §5.1 Cascade
1. **F4 Korea U declines** → fall back to **F2 KAIST Brain×Machine Intelligence Lab (Sang Wan Lee)**
   - Strongest TMS+EEG+computational fit (model-based fMRI+EEG combined work; TMS+tDCS confirmed methodology)
   - Add: KTX Daejeon round-trip $320, KAIST IRB +2–4 weeks
   - Total est: ~$2,920
2. **F2 declines** → **F1 KAIST BINP (Seungwoo Lee)**
   - Neural prosthetics focus → less PCI overlap but TMS available
   - Same Daejeon transport overhead
3. **F1 declines** → **F3 Yonsei Severance Neurology**
   - Clinical-grade signal quality but Severance IRB 12–24w; cost up to $900/session
   - Total est: ~$4,500+
4. **F5 SNU Psychiatry (Kwon)** — highest prestige but slowest. Reserve for high-N peer-reviewed validation cohort, NOT one-shot pilot.
5. **All declined** → **Scenario B (private clinic + parallel BYOE)**
   - Pay private rTMS clinic (e.g., Seoul Psychiatry Gangnam, $120–180/session) as treatment patient, request OpenBCI parallel recording
   - **HONEST C3 BLOCKER**: clinical clinics use repetitive (10Hz / intermittent theta-burst) protocols, **NOT single-pulse Massimini-style with jittered ISI ≥ 1500 ms**. PCI cannot be measured from clinical rTMS treatment session. Clinic likely refuses request as off-label use.
   - Use only as last-resort partial-data path with explicit statement that resulting metric is NOT Massimini PCI.
6. **Scenario B blocked** → **Scenario C (capex purchase, used Magstim 200²)**
   - $17K capex (per N-19 spec §5.3) >> $2.5K target. NOT recommended for one-shot pilot.
   - Re-evaluate only if user transitions from one-shot to multi-year program.

### §5.2 Honest C3 — when ALL paths blocked
If F1–F5 + Scenario B all decline AND capex C is unaffordable:
- **N-19 axis is GATED on hardware access**, not on protocol/spec. The N-19 spec remains valid but unrealizable in 2026 H1 within $2.5K budget.
- **Pivot recommendation**: prioritize other N-substrate axes (N-20, N-21, N-22) that don't require TMS hardware. Document N-19 in `state/n_substrate_n19_pci_lab_share_2026_05_01/` as "RESEARCH_COMPLETE, ACCESS_BLOCKED, AWAIT_CO_PI_OR_CAPEX_PIVOT".

---

## §6 Top-3 user-side blockers

### §6.1 Blocker 1 — Korean co-PI requirement (universal)
**Description**: All 5 candidate facilities (F1–F5) require Korean-affiliated PI for IRB application. Solo non-affiliated researcher cannot file directly.

**Impact**: blocks 100% of facilities until co-PI identified.

**Mitigation**:
- Network search: Korea U BCE / KAIST BCS / SNU 뇌인지과학과 alumni network
- KSCS (Korean Society for Cognitive Science), KSBNS (Korean Society for Brain and Neural Sciences) conference attendee directories
- LinkedIn search for "Korea University brain engineering postdoc" or similar
- Estimated co-PI search time: 2–8 weeks
- Co-PI compensation: typically co-authorship on resulting paper; no monetary cost

### §6.2 Blocker 2 — IRB approval lead time
**Description**: Korean IRB minimum 6 weeks (Korea U expedited) to 28 weeks (SNUH full review). User's 16ch BYOE = novel methodology = likely full review at hospital IRBs.

**Impact**: minimum 1.5 months delay from co-PI confirmation to first session.

**Mitigation**:
- Choose university IRB (Korea U, KAIST) over hospital IRB (Severance, SNUH)
- Frame as minimal-risk methodological pilot (not clinical study) → expedited review
- Pre-prepare all 30 items of Rossi 2009/2021 TMS safety form in Korean before filing
- Have user's medical screening done at home (saves IRB pre-screening review time)

### §6.3 Blocker 3 — BYOE 16ch OpenBCI compatibility
**Description**: Massimini PCI was developed on TMS-compatible 60+ ch amps with sample-and-hold (e.g., NeurOne, eXimia). 16ch OpenBCI Cyton+Daisy lacks sample-and-hold = TMS pulse saturates amp 5–50ms post-pulse, destroying early TEP (0–30ms = most diagnostic window).

**Impact**: even if facility allows BYOE, resulting PCI value will be biased -15 to -25% vs literature (per N-19 spec §6.1).

**Mitigation**:
- Use PCI_st sensor-level variant (Comolatti 2019) — designed for lower-density / lower-rate setups, accepts 30–300ms window (skips first 30ms)
- Post-hoc ICA artifact removal (Mutanen et al. 2018 SOUND/SSP-SIR algorithm)
- Calibration cohort n≥10 awake/sleep to learn personal threshold (per N-19 spec §6.2 mitigation #2)
- Multi-session pooling 4 × 200 = 800 trials (per N-19 spec §6.2 mitigation #3)
- **Honest C3**: result is research-grade only, NOT clinical-diagnostic

### §6.4 Korean-only access constraint per facility (Y/N summary)

| Facility | Solo non-affiliated user accepted? | Korean-affiliated PI required? |
|----------|------------------------------------|--------------------------------|
| F1 KAIST BINP | N | Y (inferred) |
| F2 KAIST BMI | N | Y (inferred) |
| F3 Yonsei Severance | N | Y (inferred, hospital IRB stricter) |
| F4 Korea U Affective | N (PARTIAL via co-PI) | Y (inferred, slightly more flexible) |
| F5 SNU Psychiatry | N | **Y (confirmed via SNUH e-IRB policy)** |

**Universal Korean co-PI requirement** = #1 blocker.

---

## §7 honest C3 disclosures

1. **No facility was contacted**. All TMS device models, rates, lead times, and BYOE policies are PUBLIC-INFERRED from web search + analogous Korean university lab data. Real values may differ ±50%.
2. Rate estimates ($300–900/session) are based on 2026 Korean clinical rTMS treatment market data + US/EU university core facility rate analogs. **No Korean university publicly publishes a TMS lab-share rate card.**
3. **TMS device model UNKNOWN for 4 of 5 facilities** — only Yonsei Severance has literature confirming Magstim + MagVenture presence. User must verify single-pulse capability before any booking.
4. BYOE 16ch OpenBCI compatibility = **INFERRED**, not confirmed for any facility. Hard amp sync is expected to be impossible everywhere; parallel-stream + TTL-trigger-only is the realistic mode.
5. Korean co-PI requirement = **STRUCTURAL**, not negotiable. User must invest in network search before any contact attempt.
6. IRB filing fees ($0–500) are estimates based on Korean university minimal-risk expedited review fee schedules (varies by institution).
7. Transport estimates assume Seoul resident; non-Seoul users add commuting cost.
8. **PCI measured with this setup is research-grade only** (raw#10) — never to be presented as clinical consciousness diagnosis.
9. F5 SNU Kwon contact (kwonjs@snu.ac.kr, +82-2-2072-2972) is publicly available from SNU College of Medicine personal page; user is **NOT instructed to email** without co-PI + IRB pre-prep.
10. Pusan Nat'l Brain Stimulation Lab is **out-of-scope** (optical NIR brain stim, not TMS) — N-19 spec §5.4 list should be corrected.
11. KRISS Daejeon = MEG only, NO TMS. N-14 MEG fallback note is correct; do not list KRISS as TMS option.
12. Hanyang ERICA cognitive science institute TMS facility = UNKNOWN from public web; needs deeper Korean-language search or direct dept inquiry.

---

## §8 결정점 (사용자 선택)

**(α)** TOP-1 (F4 Korea U) path 진행 → 먼저 Korean co-PI 네트워크 탐색 시작 (2–8 weeks, $0)
**(β)** Multi-track parallel: F4 + F2 동시 co-PI 탐색 → 먼저 응답하는 쪽 진행 (분산 risk, 시간 절약)
**(γ)** N-19 보류 → 다른 N-substrate axis (N-20, N-21) 우선; N-19 는 archive 후 재방문
**(δ)** 추가 research 필요 → v2 (예: 한양 ERICA 직접 문의 plan, KIST broker route deep-dive, NeurOne loaner 가능성)

---

## §9 Sources (2026-05-01 web search)

- [KAIST Brain & Cognitive Sciences — Research Labs](https://bcs.kaist.ac.kr/sub0301)
- [KAIST BINP Lab — Seungwoo Lee](https://binp.kaist.ac.kr)
- [KAIST Brain x Machine Intelligence Lab — Sang Wan Lee](https://aibrain.kaist.ac.kr/research)
- [Korea University Department of Brain Engineering — Research Labs](https://bce.korea.ac.kr/bce/research/lab.do)
- [Yonsei University Medical School](https://medicine.yonsei.ac.kr/)
- [Severance Hospital — Yonsei University Health System](https://sev.severance.healthcare/)
- [Seoul National University College of Medicine — Jun Soo Kwon profile](https://snucm.elsevierpure.com/en/persons/y-kwon-7)
- [SNUH 정신건강의학과](http://www.snuh.org/global/en/find/findDoctorList.do?hsp_cd=1&dept_cd=NP)
- [SNUH IRB / e-IRB system](https://hrpp.snuh.org/irb/eirb/_/singlecont/view.do)
- [기관생명윤리위원회 정보포털 (KAIRB)](https://irb.or.kr/)
- [분당서울대병원 정신건강의학과 TMS 뇌기능조절실](https://www.snubh.org/dh/main/index.do?DP_CD=NP&MENU_ID=008041)
- [Pusan National University Brain Stimulation System Lab (Shin lab) — out of scope, NIR optical](https://shinlab.pusan.ac.kr/)
- [KIST Brain Science Institute](https://bsi.kist.re.kr/)
- [KRISS — Quantum Magnetic Sensing Group (MEG only)](https://www.kriss.re.kr/menu.es?mid=a20804010100)
- [Hanyang University ERICA campus](https://www.hanyang.ac.kr/erica)
- [Seoul Psychiatry Gangnam — rTMS Therapy Seoul guide (clinical pricing reference)](https://www.seoulpsychiatryclinic.com/articles/rtms-therapy-seoul-complete-guide-for-us-patients)
- [Clinics on Call — TMS in South Korea (clinic list)](https://clinicsoncall.com/en/clinics/country-south-korea/neurology-neurosurgery/procedure-transcranial-magnetic-stimulation/)
- [TMS combined with EEG: Recommendations and open issues (Brain Stimulation 2023)](https://www.brainstimjrnl.com/article/S1935-861X(23)01696-0/fulltext)
- [Real-Time Artifacts Reduction during TMS-EEG Co-Registration (MDPI Sensors 2021)](https://www.mdpi.com/1424-8220/21/2/637)
- [OpenBCI 16ch EEG R&D kit reference — UW DXARTS](https://dxarts.washington.edu/wiki/openbci-16-channel-eeg-rd-kit)
- [Comolatti et al. 2019 — PCI_st sensor-level variant](https://pubmed.ncbi.nlm.nih.gov/31133480/)
- [경두개자기자극술(TMS) — KAIST Clinic Pappalardo Center (clinical, out of research scope)](https://clinic.kaist.ac.kr/stressclinic/s0302)

---

**status**: N19_LAB_SHARE_LOCAL_DRAFT
**verdict_key**: F4_KOREA_U_TOP1 · ESTIMATED_COST_$2.3K · LEAD_TIME_10_14_WEEKS · KOREAN_CO_PI_REQUIRED · NO_FACILITY_CONTACTED
**axis_id**: N-19
**parent_spec**: `docs/n_substrate_n19_pci_spec_2026_05_01.md`
**state_dir**: `state/n_substrate_n19_pci_lab_share_2026_05_01/`
