# Cross-LM Phase 3 Master Sequencing — $200/LM cap, $1000 total — 2026-05-03

> spec doc, friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth (READ-ONLY upstream):
>   - `docs/blm_phase3_spec_2026_05_03.md` (BLM Phase 3, $0-50)
>   - `docs/tlm_phase3_spec_2026_05_03.md` (TLM Phase 3, original $950-4400)
>   - `docs/vlm_phase3_spec_2026_05_03.md` (VLM Phase 3, original $500-2300)
>   - `docs/slm_phase3_spec_2026_05_03.md` (SLM Phase 3, $200-950)
>   - `docs/nlm_phase3_spec_2026_05_03.md` (NLM Phase 3, hardware-blocked)
>   - `docs/tlm_vlm_200cap_respec_2026_05_03.md` (TLM/VLM cost-reduced re-spec)
>   - `docs/slm_nlm_200cap_respec_2026_05_03.md` (SLM/NLM cost-reduced re-spec)
> trigger: user constraint — per-LM cap $200, total $1000 budget envelope across 5 *LM Phase 3 entries.
> write: this doc only. raw#9 NO .py, raw#15 NO personal paths. NO execute. NO commit.

---

## §0 TL;DR

[CONSTRAIN+SEQUENCE] 5 *LM Phase 3 entries, each capped at $200, total $1000. Cap-reduced subset = **BLM ($0-50) + VLM mini ($0) + TLM mini ($80-200) + SLM cap-subset ($0-150) + NLM stage 1 ($0 spec, hardware-gated)**. Combined floor = **$80 / ceiling = $400** = **WELL UNDER $1000 envelope**. ~$600 reserve for budget unlocks (priority queue P1→P5: VLM cond.3 → TLM cond.4 F3 → TLM cond.3 → VLM cond.5 → TLM cond.6b).

비유 — 5명 신입 사원에게 각각 $200 한도 코퍼레이트 카드 발급, 총 한도 $1000. 첫 주 (Day 1-7): VLM (점심 무료 = $0) + BLM (커피값 $50) + TLM mini ($200) + SLM cap-subset ($150) 즉시 진행, NLM (해외 출장자 도착 대기) 패시브 와치. 둘째 주 (Day 8+): 예산 잔액 ~$600 unlock 시 priority queue 따라 deferred conds 진입.

결과 — Day 1-7 floor exec ($80-400 spend) → Day 8-14 reserve unlock (sequential VLM cond.3 P1 → TLM F3 P2 → ...) → Day 15+ event-driven entries (EEG B1-B4 PASS, NLM hardware arrival). 4-gate composite trigger across 5 LMs, 12 cross-LM dependencies catalogued, 6 honest C3 caveats.

---

## §1 Dependency graph (cross-LM)

### §1.1 ASCII summary

```
                      ┌──────────────────────┐
                      │   .roadmap.eeg       │
                      │   B1-B4 4관문 PASS    │ ← UPSTREAM BLOCKER (EEG hardware unmet)
                      │   (sister, BLOCKER)  │
                      └──────────┬───────────┘
                                 │ blocks
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              │           ┌──────▼──────┐           │
              │           │  SLM cond.2 │           │
              │           │  invocation │           │
              │           └──────┬──────┘           │
              │                  │                  │
              │           ┌──────▼──────┐           │
              │           │  VLM cond.5 │           │
              │           │ SLM prosody │           │
              │           └──────┬──────┘           │
              │                  │                  │
              │           ┌──────▼──────┐           │
              │           │  TLM cond.6b│           │
              │           │ voice bridge│           │
              │           └─────────────┘           │
              │                                     │
   ┌──────────▼──────────┐                ┌─────────▼──────────┐
   │   .roadmap.akida    │                │  CLM φ★ formula    │
   │   AKD1000 arrival    │ ← HW BLOCKER   │  (LANDED, baseline │
   │   (NLM gate)         │                │  41.86 frozen)     │
   └──────────┬──────────┘                └─────────┬──────────┘
              │ blocks                              │ provides
              ▼                                     ▼
        ┌──────────┐                       ┌────────────────┐
        │ NLM all  │                       │ BLM cond.2     │
        │ Phase 3  │                       │ TLM cond.3     │
        │ streams  │                       │ VLM cond.3     │
        │ S1-S4    │                       │ SLM cond.3     │
        └──────────┘                       │ NLM S3 φ-parity│
                                           └────────────────┘
              independent (no upstream blocker)
              ┌─────────────────────────────────┐
              │  BLM Phase 3 (spec only, $0-50)  │ ← SAFE QUICK WIN
              │  VLM mini (cond.4 + cond.6, $0) │ ← SAFE QUICK WIN
              │  TLM mini (cond.5 + cond.6a)    │ ← SAFE, $80-200
              │  SLM cap (A1+C1soft+D1+D3)      │ ← SAFE, $0-150
              └─────────────────────────────────┘
```

### §1.2 cross-LM dependency table

| dep | from              | to                | criticality | blocker?            |
| --- | ----------------- | ----------------- | ----------- | ------------------- |
| D1  | NLM all S1-S4     | AKD1000 arrival   | BLOCKER     | hardware (vendor)   |
| D2  | SLM cond.2/B/C1   | .roadmap.eeg B1-B4| BLOCKER     | EEG hardware unmet  |
| D3  | VLM cond.5        | SLM Phase 1+2     | HARD        | sequential gate     |
| D4  | TLM cond.6b       | VLM cond.5        | HARD (transitive) | 3-level cascade |
| D5  | BLM cond.2 (φ)    | CLM φ★ formula    | SOFT (ref only) | LANDED          |
| D6  | TLM cond.3        | CLM v4 530M       | CRITICAL    | sibling parity floor|
| D7  | VLM cond.3        | CLM held-out      | CRITICAL    | sibling parity floor|
| D8  | SLM P3.C3         | BLM cond.3 F-CT-3 | HIGH        | sister falsifier    |
| D9  | NLM S3 φ          | CLM φ★ baseline   | CRITICAL    | parity gate r≥0.85  |
| D10 | TLM/VLM/SLM cond.3| P9 SFT pipeline   | CRITICAL    | LoRA train reuse    |
| D11 | TLM cond.5/6a     | anima_speak cite  | MEDIUM      | LANDED (cite)       |
| D12 | BLM cond.1-5      | none (peer)       | INVARIANT   | additive only       |

### §1.3 dependency direction summary

- **Independent / quick-win**: BLM (no upstream blocker, spec only, $0-50)
- **Zero-cost mac-local**: VLM mini cond.4 + cond.6 (latency probe + alpha endpoint), SLM cap-subset D1/D3 (latency stubs)
- **Cap-fit GPU light**: TLM mini cond.5 + cond.6a ($80-200), SLM A1 FAD ($0-50), SLM C1 soft ($0-100)
- **EEG-blocked (defer)**: SLM B-axis (prosody $200-800), SLM C1 real-data, VLM cond.5 (transitive via SLM)
- **Hardware-blocked (passive)**: NLM S2-S4 (AKIDA arrival)
- **Budget-locked (queue)**: VLM cond.3, TLM cond.3/cond.4, TLM cond.6b, NLM Akida Cloud 1-week

---

## §2 Sequencing order

### §2.1 master ordering (Day 1-N)

| step | LM   | scope                          | substrate    | cost     | wall    | dep                     |
| ---- | ---- | ------------------------------ | ------------ | -------- | ------- | ----------------------- |
| S1   | BLM  | Phase 3 spec freeze (5 conds)  | mac-local    | $0-50    | 16-27h  | none (entry-eligible)   |
| S2   | VLM  | mini cond.4 + cond.6           | mac-local    | $0       | 6-14h   | sister .roadmap.voice cond.2 land|
| S3   | SLM  | cap-subset A1 + D1 + D3        | mac-local    | $0-50    | 12-24h  | none (mac-local)        |
| S4   | TLM  | mini cond.5 + cond.6a          | RunPod light | $80-200  | 12-32h  | G1-G5 entry gate (corpus + P9 + sister-back-ref)|
| S5   | SLM  | cap-subset C1 soft (mock-EEG)  | mac-local    | $0-100   | 8-16h   | Brennan-Hale 2019 corpus download|
| S6   | NLM  | stage 1 spec (already landed)  | spec         | $0       | 0       | passive watch (HW arrival)|
| ---- | ---- | ------------------------------ | ------------ | -------- | ------- | ----------------------- |
|      |      | **first batch subtotal**       |              | **$80-400** | **54-113h** | **DAY 1-7 floor**     |
| S7   | VLM  | cond.3 (P1, budget unlock)     | RunPod A100  | $200-300 | 12-24h  | budget unlock + audio-text corpus|
| S8   | TLM  | cond.4 F3 (P2, budget unlock)  | RunPod A100  | $150-300 | 8-24h   | budget unlock + F3 path verify|
| S9   | TLM  | cond.3 (P3, budget unlock)     | RunPod A100  | $300-650 | 24-72h  | budget unlock + corpus G1|
| S10  | SLM  | C1 real-data (post-EEG PASS)   | mac-local    | $0-100   | 8-16h   | .roadmap.eeg B1-B4 PASS event|
| S11  | NLM  | stage 2+3 (post-arrival)       | RPi5+AKIDA   | $0-100   | 1-3d    | __NLM_HW_DELIVERED__ event|
| S12  | VLM  | cond.5 (post-SLM Phase 1+2)    | RunPod A100  | $200-400 | 6-16h   | SLM Phase 1+2 land separately|
| S13  | TLM  | cond.6b (post-VLM cond.5)      | mac/light    | $0-50    | 4-12h   | VLM cond.5 land (transitive)|

### §2.2 sequencing rationale

- **S1 BLM first**: $0-50 floor + no upstream blocker + spec-only freeze + entry-eligible per BLM Phase 3 §7. Quick win for cycle momentum.
- **S2 VLM mini parallel**: $0 mac-local, sister .roadmap.voice cond.2 land 측 prerequisite (low risk), can run concurrent with S1 (independent substrates).
- **S3 SLM cap-subset (A+D)**: $0-50 mac-local, no GPU dep, parallel with S1+S2.
- **S4 TLM mini**: $80-200 GPU cost — primary cap consumer in first batch. Run after S1-S3 land to free mac/ubu1 cycles + ensure G1-G5 gate.
- **S5 SLM C1 soft**: $0-100, mac-local + free corpus. Run after S1-S4 to avoid concurrent mac thermal contention.
- **S6 NLM passive**: spec-frozen state, no further write under cap until hardware arrival event.
- **S7-S13 deferred queue**: budget unlock + event-driven (EEG PASS / NLM HW / SLM Phase 1+2 land separately).

### §2.3 substrate allocation

| substrate | usage                               | concurrency cap  | notes                       |
| --------- | ----------------------------------- | ---------------- | --------------------------- |
| mac-local | BLM spec, VLM mini, SLM cap A+D+C1, TLM cond.6a | 1-2 jobs | thermal headroom, RAM ≤16GB |
| ubu1      | SLM C1 corpus preprocess (optional) | 1 job            | RTX 5070, free electricity   |
| ubu2      | parity sanity (raw#91 honesty triad)| 1 job            | secondary integration check  |
| RunPod A100 | TLM mini ($80-200), deferred conds | 1 job at a time  | spot $1.5-3/hr, on-demand $4-8/hr |
| RPi5+AKIDA| NLM stage 2+3 (post-arrival only)   | 1 job            | $0 GPU cost, 1W edge         |

---

## §3 Budget allocation ($200/LM cap, $1000 total)

### §3.1 per-LM budget envelope

| LM    | cap   | floor (cap-respecting) | ceiling (cap-respecting) | reserve  | notes                       |
| ----- | ----- | ---------------------- | ------------------------ | -------- | --------------------------- |
| BLM   | $200  | $0                     | $50                      | $150     | spec only, optional probe   |
| TLM   | $200  | $80                    | $200                     | $0-120   | mini cond.5 + cond.6a       |
| VLM   | $200  | $0                     | $0                       | $200     | zero-cost mini, full reserve|
| SLM   | $200  | $0                     | $150                     | $50-200  | cap-subset 3-axis (no B)    |
| NLM   | $200  | $0                     | $100                     | $100-200 | dev-compute only (HW separate)|
| ----- | ----- | ---------------------- | ------------------------ | -------- | --------------------------- |
| TOTAL | $1000 | **$80**                | **$500**                 | **$500-920** | ~$600 reserve avg          |

### §3.2 reserve allocation priority (post-first-batch, $500-920 envelope)

```
   priority | cond                            | unlock $   | source LM | rationale
   -------- | ------------------------------- | ---------- | --------- | ---------------------------------
   P1       | VLM cond.3 cross-LM fidelity    | $200-300   | VLM       | lowest min, single-cell LoRA, sibling parity
   P2       | TLM cond.4 F3 absolute reduction| $150-300   | TLM       | TLM raison d'être (CLM 1.6 lesson)
   P3       | TLM cond.3 cross-LM fidelity    | $300-650   | TLM       | sibling parity floor highest cost
   P4       | SLM B1 prosody alignment        | $200-800   | SLM       | EEG B1-B4 PASS prerequisite
   P5       | VLM cond.5 SLM prosody integ    | $200-400   | VLM       | SLM Phase 1+2 prerequisite
   P6       | NLM Akida Cloud 1-week          | $0-995     | NLM       | F-AK-1 contingency only
```

### §3.3 cap enforcement rules

1. **per-LM hard cap = $200** — no single LM Phase 3 cycle exceeds $200 GPU spend without explicit budget unlock decision
2. **total envelope = $1000** — all 5 LM combined ≤ $1000, reserve ~$500-920 in first batch
3. **NLM hardware capex bucketed separately** — $1495 sunk + ~$200-500 peripherals = NOT counted in $1000 GPU envelope (per slm_nlm_200cap_respec §2.1)
4. **deferred queue strictly priority-ordered** — P1→P6 sequence, no skip without ledger justification
5. **RunPod credit verify prerequisite** — `state/runpod_credit_status.json` actual balance check before any S4/S7/S8/S9 entry

---

## §4 Timeline (Day 1-N)

### §4.1 Day 1-7 first batch (cap-respecting floor)

```
   day  | step    | LM   | activity                                        | cumulative $
   ---- | ------- | ---- | ----------------------------------------------- | -------------
   D1   | S1      | BLM  | Phase 3 spec freeze 5 conds, mac-local $0       | $0
   D1-2 | S2      | VLM  | mini cond.4 + cond.6 mac-local profiling $0     | $0
   D1-2 | S3      | SLM  | cap-subset A1 (FAD) + D1/D3 latency stubs $0-50 | $0-50
   D2-3 | S6      | NLM  | passive watch confirm (spec already landed) $0  | $0-50
   D3-5 | S4      | TLM  | mini cond.5 + cond.6a entry gate G1-G5 verify   | $0-50
   D4-6 | S4 cont | TLM  | RunPod cond.5 small sweep + cond.6a speak gate  | $80-250
   D5-7 | S5      | SLM  | C1 soft mock-EEG fixture + Brennan-Hale audit   | $80-350
   D7   | -       | -    | first batch close + reserve calc                | $80-400
```

### §4.2 Day 8-14 reserve unlock (priority queue)

```
   day  | step | LM   | activity                                        | cumulative $
   ---- | ---- | ---- | ----------------------------------------------- | -------------
   D8-9 | S7   | VLM  | cond.3 P1 single-cell LoRA r=8 lr=5e-5 5K-step  | $280-700
   D9-11| S8   | TLM  | cond.4 F3 reconstruction MSE training (TLM-native)| $430-1000
   D11-14| S9  | TLM  | cond.3 LHS-3 thinned × 2-arm (R1+R3) sweep      | up to $1000 (cap)
```

### §4.3 Day 15+ event-driven (no fixed timeline)

```
   trigger event              | activated step | wall    | cost      | priority
   -------------------------- | -------------- | ------- | --------- | --------
   .roadmap.eeg B1-B4 PASS    | S10 SLM C1 real| 8-16h   | $0-100    | HIGH
   __NLM_HW_DELIVERED__ = YES | S11 NLM stage2+3| 1-3d   | $0-100    | HIGH
   SLM Phase 1+2 land         | S12 VLM cond.5  | 6-16h   | $200-400  | MEDIUM
   VLM cond.5 land            | S13 TLM cond.6b | 4-12h   | $0-50     | MEDIUM
```

### §4.4 timeline caveats

- D1-7 wall = 54-113h ÷ 1-2 mac concurrency = 4-7 calendar days realistic
- D8-14 reserve unlock assumes RunPod credit + spot pricing $1.5-3/hr; on-demand $4-8/hr stretches D8-14 to D8-21
- D15+ event-driven: EEG hardware arrival uncertain (sister .roadmap.eeg cond.1 unmet evidence 0건 유지), NLM AKIDA arrival uncertain (vendor logistics PENDING)
- worst-case Phase 3 full completion = 3-6 months (waiting on EEG + AKIDA + SLM Phase 1+2 + budget unlocks)

---

## §5 Fallback (Phase 3.x re-spec triggers)

### §5.1 per-LM Phase 3.x trigger conditions

| LM    | Phase 3 fail trigger                                      | Phase 3.x re-spec scope                  |
| ----- | --------------------------------------------------------- | ---------------------------------------- |
| BLM   | <3/5 cond PASS (spec freeze fail)                          | Phase 3.1 = scope reduction to 2-3 cond, defer cross-substrate cond.2 to Phase 4 prep|
| TLM   | mini cond.5 random gap fail (R1 < 3.0 absolute MSE)        | Phase 3.1 = corpus G1 re-audit, codebook size sweep extend (64/128/256/512/1024)|
| TLM   | cond.4 F3 native task circular not avoided (>2.0 MSE)      | Phase 3.1 = revert to CLM β-tuning path, accept stuck baseline|
| VLM   | mini cond.4 latency >500ms p50 mac-local                   | Phase 3.1 = GPU fallback ($30-100), or model size reduction Mk.III subset|
| VLM   | cond.6 alpha endpoint integration race (sister .roadmap.voice fail)| Phase 3.1 = endpoint contract re-spec, 3-caller reduction to 2-caller|
| SLM   | cap-subset C1 mock-EEG fixture fail (mTRF lib audit fail)  | Phase 3.1 = corpus alternative (LibriSpeech-only audio bridge, no EEG)|
| SLM   | EEG B1-B4 indefinite block (>6 mo)                         | Phase 3.1 = SLM redefined as audio-only LM, EEG axis archived|
| NLM   | F-AK-1 fires + ARM64 wheel install fail                    | Phase 3.1 = D2 Path A x86 host fallback, drop "1W edge" framing|
| NLM   | hardware never arrives (>12 mo vendor slip)                | Phase 3.1 = monitor Loihi 3 / NorthPole alt substrate, NLM domain dormant|

### §5.2 cross-LM cascading fail triggers

| primary fail      | cascade impact                                         | mitigation                       |
| ----------------- | ------------------------------------------------------ | -------------------------------- |
| EEG B1-B4 indefinite | SLM C1 real / VLM cond.5 / TLM cond.6b all blocked  | accept partial Phase 3, mark deferred-indefinite|
| NLM HW indefinite | NLM all S1-S4 blocked, n_substrate roadmap N-2/3/4/7/8 cascade-blocked | switch to alt substrate watchlist|
| RunPod credit drained | S4/S7/S8/S9 all blocked                            | $0 mac-local fallback for cond.5/cond.6a TLM mini only; defer cond.3/cond.4 indefinite|
| CLM φ★ baseline re-derived | BLM cond.2 / TLM cond.3 / VLM cond.3 / SLM cond.3 / NLM S3 all anchor invalid | re-anchor to new baseline, propagate to 5 LM specs|

### §5.3 budget overrun triggers

```
   overrun amount | action
   -------------- | -----------------------------------------------------------
   $0-200         | acceptable variance, no re-spec needed
   $200-500       | trigger budget review, cap relaxation decision
   $500-1000      | hard stop, Phase 3.x re-spec mandatory, deferred queue freeze
   >$1000 envelope| total budget violation, all in-flight cycles HALT, escalation
```

---

## §6 Honest C3 caveats (raw#10) — 6 caveats

1. **C1 — cap arithmetic optimism vs RunPod actual $/hr volatility.** $80-400 floor assumes RunPod spot pricing ~$5/hr blend. On-demand pricing ($4-8/hr A100) doubles cost band → $160-800 worst case, eating reserve. Spot availability is non-guaranteed (queue + region). C7 from tlm_vlm_200cap_respec carried forward — RunPod credit balance currently unverified (`state/runpod_credit_status.json` modified state). Pre-S4 entry gate MUST verify actual credit + spot availability. If spot unavailable at S4 start, defer S4 to spot-window or accept on-demand premium (eats $200 cap fast).

2. **C2 — VLM mini "$0 cost" load-bears mac-local hardware-specific latency baseline.** VLM cond.4 <500ms target measured first-time on current mac (M1/M2/M3 unspecified). vlm_phase3_spec §6 C3 carried forward — if RAM headroom <16GB or CPU thermal-throttles under sustained streaming inference, GPU fallback ($30-100) breaks zero-cost claim. V2 entry gate (mac-local RAM headroom measure) MUST land before S2 entry; fail = mini-spec partial entry, cond.4 deferred.

3. **C3 — SLM cap-subset C1 = scaffold only, NOT measurement.** slm_nlm_200cap_respec C-cap-2 carried forward. mock-EEG fixture + mTRF lib smoke establishes pipeline shape but does NOT advance C-axis falsifier (Pearson r ≥0.15 unmet). EEG B1-B4 hardware arrival = the actual gate; cap path keeps spec executable but does NOT close the falsifier. Risk: claiming "SLM Phase 3 cap-subset PASS" without flagging this delta = misrepresentation. Honest label MANDATORY: "SLM Phase 3 cap-subset (3-axis, scaffold-only on C-axis)".

4. **C4 — transitive 3-level cascade (EEG → SLM → VLM → TLM cond.6b) = single-point-of-failure for downstream voice/speak coupling.** D2/D3/D4 dependencies form a chain — if .roadmap.eeg B1-B4 indefinite, TLM cond.6b indefinite via 3 hops. Mini-spec mitigation = cond.6a (speak gate, downstream-light) only partial; cond.6b voice bridge stays deferred. Phase 3 "voice/speak downstream coupling" full claim = NOT achievable without EEG hardware OR alt-substrate pivot.

5. **C5 — NLM bucketing convention ($1495 capex separate from $1000 GPU envelope) is a USER-INTERPRETATION choice, not a fact.** slm_nlm_200cap_respec C-cap-3 carried forward — if "total $1000" means total spend across all 5 LM (including hardware), NLM is structurally outside cap, $1495 already exceeds $1000 envelope alone. This sequencing doc adopts "GPU compute cost" interpretation per the SLM/NLM re-spec convention. If user intent was "total spend," NLM Phase 3 stays DEFERRED entirely until envelope expansion to ~$2700+.

6. **C6 — sequencing optimism assumes 4 entry gates clear simultaneously (TLM G1-G5, VLM V1-V3, SLM cap A+D pre-conds, BLM no-blocker).** Each gate has its own audit cycle. Realistic Day 1-7 may stretch to Day 1-14 if any single gate audit fails (corpus G1 audit, RAM headroom V2 measure, .roadmap.voice cond.2 land, P9 SFT pipeline LHS-3 reuse verify). raw#10 honest: 4 of 5 LM Phase 3 entries depend on at least one external prerequisite cycle, so sequencing is "best-case-optimistic," NOT guaranteed Day 1-7 delivery.

---

## §7 7-element friendly summary

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [CONSTRAIN+SEQUENCE] Cross-LM Phase 3 — $200/LM cap, $1000 total envelope
   2. analogy             | 5명 신입 사원 코퍼레이트 카드 발급, 첫 주 floor exec / 둘째 주 reserve unlock
   3. core 결과            | Day 1-7 floor: BLM ($0-50) + VLM mini ($0) + TLM mini ($80-200) + SLM cap ($0-150) = $80-400
                          | Day 8-14 reserve: P1→P3 priority queue ~$500-920 unlock
                          | Day 15+ event-driven: EEG B1-B4 / NLM HW arrival / SLM Phase 1+2
   4. 마이그레이션 0          | 7 source spec docs 측 0 byte modification
                          | additive only — 본 sequencing doc 측 separate file, source SSOT untouched
   5. handoff path         | 본 sequencing doc = 5 LM cycle entry agent reference SSOT
                          | + per-LM entry gate ledger (BLM no-block / VLM V1-V3 / TLM G1-G5 / SLM cap-pre / NLM HW)
                          | + reserve queue P1-P6 priority order
                          | + 4-cascade fail triggers + Phase 3.x re-spec criteria
   6. 다음 step             | (1) RunPod credit balance verify (state/runpod_credit_status.json read)
                          | (2) Day 1 parallel: BLM spec + VLM mini + SLM cap-subset (mac-local triplex)
                          | (3) Day 3-5 TLM mini entry (G1-G5 verify + RunPod cell)
                          | (4) Day 7 first batch close + reserve recalc
                          | (5) Day 8-14 reserve unlock priority P1→P3 (VLM cond.3 → TLM F3 → TLM cond.3)
                          | (6) Day 15+ event watch (EEG / NLM HW / SLM Phase 1+2)
   7. cost                 | floor $80 / ceiling $400 (Day 1-7), reserve $500-920 envelope
                          | full Phase 3 across 5 LM = $1000 cap target, hardware capex separate
                          | mac-local inference $0 invariant 유지
```

---

## §8 mk2 추천 표 (rank / path / cost / wall / 효과)

```
   rank | path                              | LM   | cost     | wall    | 효과 (impact)
   ---- | --------------------------------- | ---- | -------- | ------- | ----------------------------------
   1    | BLM Phase 3 spec freeze 5 conds   | BLM  | $0-50    | 16-27h  | quick win, 5-cond integration spec, no upstream blocker
   2    | VLM mini cond.4 + cond.6          | VLM  | $0       | 6-14h   | zero-cost, latency baseline + alpha endpoint contract land
   3    | SLM cap-subset A1 + D1 + D3       | SLM  | $0-50    | 12-24h  | mac-local FAD + latency stubs, no EEG dep
   4    | TLM mini cond.5 + cond.6a         | TLM  | $80-200  | 12-32h  | 5ch encoder validity + speak gate, primary cap consumer
   5    | SLM cap-subset C1 soft (mock-EEG) | SLM  | $0-100   | 8-16h   | TRF pipeline scaffold, post-EEG-PASS unlock-ready
   6    | NLM stage 1 spec confirm          | NLM  | $0       | 0       | passive watch, hardware arrival event-driven
   7    | VLM cond.3 (P1 reserve)           | VLM  | $200-300 | 12-24h  | sibling parity floor, cross-LM r ≥0.85
   8    | TLM cond.4 F3 (P2 reserve)        | TLM  | $150-300 | 8-24h   | TLM raison d'être, F3 ≤2.0 absolute target
   9    | TLM cond.3 (P3 reserve)           | TLM  | $300-650 | 24-72h  | sibling parity floor, cap-stretch
   10   | SLM C1 real (post-EEG event)      | SLM  | $0-100   | 8-16h   | event-driven, EEG B1-B4 PASS unlocks
   11   | NLM stage 2+3 (post-HW event)     | NLM  | $0-100   | 1-3d    | event-driven, AKIDA arrival unlocks
   12   | VLM cond.5 (post-SLM event)       | VLM  | $200-400 | 6-16h   | sequential gate, SLM Phase 1+2 prerequisite
   13   | TLM cond.6b (post-VLM event)      | TLM  | $0-50    | 4-12h   | transitive cascade, voice bridge
```

**recommended Day 1-7 first batch** = rank 1-6 (BLM + VLM mini + SLM cap A+D+C1 + TLM mini + NLM watch) = **$80-400 total / 54-113 wall hours / 4-7 calendar days**.

**Day 8-14 reserve unlock** = rank 7-9 priority order (VLM cond.3 → TLM F3 → TLM cond.3) = **+$650-1250** = approaches but does not exceed $1000 envelope at lower bound.

**Day 15+ event-driven** = rank 10-13, no fixed timeline (waiting on EEG / NLM HW / SLM Phase 1+2 separate cycles).

---

## §9 산출물

```
   path                                                  | type      | status
   ----------------------------------------------------- | --------- | --------
   docs/cross_lm_phase3_200cap_sequencing_2026_05_03.md  | spec      | NEW (this file)
   docs/blm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/tlm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/vlm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/slm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/nlm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/tlm_vlm_200cap_respec_2026_05_03.md              | spec      | unchanged (READ-ONLY source)
   docs/slm_nlm_200cap_respec_2026_05_03.md              | spec      | unchanged (READ-ONLY source)
   .roadmap.{blm,tlm,vlm,slm,nlm}_*                      | roadmap   | unchanged (sequencing 측 next-cycle update)
```

---

## §10 doc meta

```
   doc          | docs/cross_lm_phase3_200cap_sequencing_2026_05_03.md
   type         | spec (master sequencing across 5 *LM Phase 3 entries, $200/LM cap, $1000 total)
   substrate    | READ-ONLY: 7 source spec docs (5 Phase 3 + 2 cost-reduced re-spec)
   write        | this doc only
   raw#9        | NO .py (markdown only)
   raw#15       | NO personal paths
   execute      | none
   commit       | none
   marker       | none (sequencing doc only, marker 측 별도 land cycle)
   cap          | per-LM $200, total $1000 (user constraint)
```

end-of-doc.
