<!-- [Hc_972 slm-nlm-phase3-200cap — moved to hypotheses_candidates/Hc_972_slm_nlm_phase3_200cap.md on 2026-05-11] -->

# SLM + NLM Phase 3 — $200 GPU-Cost Cap Re-spec — 2026-05-03

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth (READ-ONLY upstream):
>   - `docs/slm_phase3_spec_2026_05_03.md` (original SLM Phase 3 spec)
>   - `docs/nlm_phase3_spec_2026_05_03.md` (original NLM Phase 3 spec, hardware-gated)
>   - `docs/slm_stage12_landed_2026_05_03.ai.md` (Phase 1+2 landed)
> trigger: user constraint — GPU 비용 ≤ $200 strategy 만 진행.
> write: this doc only. raw#9 NO .py, raw#15 NO personal paths. NO execute. NO commit.

---

## §0 TL;DR

- **SLM viable slate (under cap)**: A1 (FAD) + C1 (TRF, soft-fallback w/ mock-EEG fixture) + D1/D3 (latency probe) → **$0–150 GPU cost**, 1–2 days mac-local + free corpus.
- **B axis (prosody)** drops out — RunPod A100 LoRA $200–800 → **DEFERRED to post-cap cycle**.
- **NLM under "GPU-cost ≤ $200" lens**: hardware capex $1,495 (sunk) + ~$200–500 peripherals are **separate budgets**, not GPU cost. GPU/dev-compute portion = **$0–100** (mac-local + ubu1 + optional Akida Cloud $1 trial). Pre-arrival = **$0 (spec only)**; post-arrival dev-compute fits inside cap.
- **Combined cap-respecting spend**: SLM $0–150 + NLM dev-compute $0–100 = **$0–250 GPU**, structurally split so SLM-only path = **$0–150** if NLM hardware never arrives.
- **Sequencing**: SLM cap-respecting axes go first (no blockers, mac-local), NLM dev-compute waits on hardware arrival event.

---

## §1 SLM minimum-viable conds under $200 cap

### §1.1 Original 4-cond entry slate (recap)

| cond  | name                          | cost band     | wall    | hardware            | cap-fit |
| ----- | ----------------------------- | ------------- | ------- | ------------------- | ------- |
| P3.A1 | FAD (Frechet Audio Distance)  | $0–50         | 4–8h    | mac-local           | YES     |
| P3.B1 | prosody embedding alignment   | $200–800      | 1–2d    | RunPod 1×A100 LoRA  | NO      |
| P3.C1 | speech envelope ↔ EEG TRF     | $0–100        | 8–16h   | mac-local + corpus  | YES (soft) |
| P3.D1 | LSL → 1st decoded text ≤300ms | $0            | 4–8h    | mac-local profile   | YES     |

### §1.2 Cap-respecting viable slate (final)

```
   cond    | name              | cost  | wall   | substrate          | hard-block?            | mitigation
   ------- | ----------------- | ----- | ------ | ------------------ | ---------------------- | ----------
   P3.A1   | FAD               | $0-50 | 4-8h   | mac-local (CPU)    | none                   | VGGish off-the-shelf
   P3.C1   | TRF (soft)        | $0-100| 8-16h  | mac-local + corpus | EEG B1-B4 unmet        | mock-EEG fixture, axis spec only
   P3.D1   | LSL latency p50   | $0    | 4-8h   | mac-local profile  | full IMPL stack absent | latency probe stub mode
   P3.D3   | RVQ quantize step | $0    | 2-4h   | mac-local          | RVQ IMPL absent        | per-epoch synthetic timing
```

**total GPU cost band**: **$0–150** (worst-case if VGGish + mTRF download / preprocess incurs minor cloud egress; baseline = $0).
**total wall band**: **18–36h** (≈ 1 SDE-day, 2 calendar-days w/ corpus download).
**substrate**: 100% mac-local (M2 Pro), zero RunPod, zero A100, zero LoRA train.

### §1.3 Soft-fallback rationale (P3.C1)

- Original C1 depends on `.roadmap.eeg` B1-B4 4관문 PASS (D1 BLOCKER per §5.2 of original spec).
- B1-B4 unmet evidence remains 0건 — sister cond.1 측 unmet 유지 per original §1.3 carried-open #2.
- Cap-respecting path: spec-and-fixture only.
  - Brennan-Hale 2019 corpus (CC-BY, free download) audit + license verify (free).
  - mock-EEG fixture (synthetic 16ch×1250 float32 from band-power generator) → mTRF library (mne-python `Receptive Field`) sanity-check pipeline.
  - Pearson r ≥0.15 floor → measure on synthetic ground truth (planted signal); real-data measure DEFERRED to post-B1-B4-PASS cycle.
- Honest framing: **C1 under cap = "TRF pipeline scaffold, axis spec freeze + smoke test only"**, not the published-baseline measurement Phase 3 originally promised.

### §1.4 P3.D1 / D3 stub-mode rationale

- D1 originally requires "full IMPL stack" (P9 §4 decision matrix). Under cap: latency probe operates on stub generators (RVQ → AR-decoder dummy → text return), measuring framework overhead only.
- D3 measures RVQ quantize step latency on a CPU-only synthetic input batch — pure timing harness, no model weights required.
- Honest framing: **D1/D3 under cap = budget-floor establishment**, not closed-loop BCI demonstration.

---

## §2 NLM hardware-arrival contingency plan

### §2.1 Cost decomposition under "GPU cost" lens

| Bucket               | Original cost   | "GPU cost" classification | Cap-relevant? |
| -------------------- | --------------- | ------------------------- | ------------- |
| AKD1000 dev kit      | $1,495 (PAID)   | hardware capex            | NO (sunk + non-GPU) |
| RPi5 + HAT+ + PSU + wattmeter | $200–500 | hardware peripherals     | NO (non-GPU)  |
| x86 dev compute      | $0              | mac-local + ubu1 reuse    | YES — $0      |
| Akida Cloud trial    | $1              | optional ARM64 fallback   | YES — $1      |
| Akida Cloud 1-week   | $0–$995         | F-AK-1 contingency        | YES — but bypass under cap |

**GPU-cost-only NLM spend (excluding hardware)**:
- Pre-arrival: **$0** (spec-only, no execution possible).
- Post-arrival dev: **$0–$100** (mac-local + ubu1 free; cap absorbs $1 Akida Cloud trial; if F-AK-1 forces fallback, **declare D2 Path A x86-host degraded mode** to avoid $995 1-week cloud).

### §2.2 Three-stage contingency

```
   stage      | trigger                           | GPU cost | wall    | scope
   ---------- | --------------------------------- | -------- | ------- | -----
   stage 1    | now (hardware未도착)              | $0       | 0       | spec freeze + runbook only (already landed: nlm_phase3_spec_2026_05_03.md)
   stage 2    | __NLM_HW_DELIVERED__ = YES        | $0       | 4-8h    | D+0 bring-up: RPi5 OS install + ARM64 wheel install + MNIST cnn2snn smoke (mac-local prep, then on-device)
   stage 3    | __NLM_FIRST_BYTE_SPIKE__ = PASS   | $0-100   | 1-3d    | S1+S2-a inference loop, F-NLM-1/3 measurement (energy + sparsity); F-NLM-2/4 cross under cap if mac-local cross-substrate harness fits
```

### §2.3 Cap-respecting NLM scope (per stage)

- **stage 1 (current)**: spec only. **0 axis activated**. Doc already landed; no further write needed under cap.
- **stage 2**: sub-cond A (delivery) + sub-cond B (devkit ready) per original §1.3. Pure on-device + mac-local prep, $0 GPU.
- **stage 3**: sub-cond C (first byte-spike) + S1 substrate integration + S2-a recommended path (cnn2snn-converted small CNN-decoder, BLM byte-LM weight init, x86-train-then-deploy). x86 train uses **existing mac/ubu1**, not RunPod → **$0 GPU**. Akida Cloud trial $1 reserved as ARM64 triage only.
- **F-AK-1 hard branch**: if ARM64 wheel fails AND cap forbids $995 1-week cloud, declare **D2 Path A** (x86 host fallback, RPi5 demoted to ADM-encoder-only). Cap preserved at $0–100 GPU.

### §2.4 What cap forces NLM to defer

- F-NLM-2 (latency p50/p95 interactive class) — measurable only after stage 3, fits cap.
- F-NLM-4 (cross-substrate parity Φ_nlm vs Φ_clm, r ≥0.85) — fits cap if 16-prompt cached set reuses existing CLM φ★ outputs (no new GPU spend).
- S2-b (native SNN transformer-equivalent) — research-tier, BPTT surrogate-grad train **likely exceeds cap on x86** for any non-trivial param count → **DEFERRED** under cap regardless of arrival.
- F-NLM-1 (energy J/token vs CLM) requires a CLM J/token baseline measurement on RTX 5070 ubu1; if ubu1 wall-meter measurement is free (already-paid hardware), fits cap.

---

## §3 Deferred conds (>$200 cap)

### §3.1 SLM deferred

| cond  | name                          | original cost | reason for defer                      | unblock trigger                       |
| ----- | ----------------------------- | ------------- | ------------------------------------- | ------------------------------------- |
| P3.B1 | prosody embedding alignment   | $200–800      | RunPod A100 LoRA train > cap          | budget unlock OR mac-local LoRA harness landed |
| P3.B2 | stress marker decode (ERP)    | (in B band)   | depends on B1 + ERP analysis pipeline | B1 unblock + ERP lib audit            |
| P3.B3 | pitch contour reconstruction  | (in B band)   | depends on B1 + F0 extraction         | B1 unblock + F0 corpus audit          |
| P3.A2 | PESQ-equivalent intelligibility| (in A band, marginal) | needs speech model — may exceed cap if model download/inference triggers cloud | confirm CPU-only path; otherwise defer |
| P3.A4 | speaker consistency (ECAPA)   | (in A band)   | speaker corpus + ECAPA-TDNN inference; cap-marginal | confirm mac-local fit; otherwise defer |
| P3.C1 | TRF (REAL-data measurement)   | $0–100 (cap-fit) but **scientifically blocked by EEG B1-B4** | BLOCKER unmet | `.roadmap.eeg` B1-B4 PASS              |
| P3.C2 | T7/T8/P7/P8 auditory dominance| (in C band)   | depends on C1 real-data measurement   | C1 unblock                             |
| P3.C3 | F-CT-3 sister cross-link      | (in C band)   | depends on BLM cond.3 + TRIBE v2      | BLM cond.3 land + TRIBE v2 ingest      |
| P3.D2 | streaming KV-cache hit rate   | $0 cap-fit but depends on KV-cache IMPL absent | full IMPL stack | slm_ar_decoder.hexa land              |
| P3.D4 | end-to-end audio render       | (in D band)   | depends on anima-voice TTS pipe       | anima-voice TTS surface complete       |

### §3.2 NLM deferred (under cap)

| item                  | reason                                                       | unblock trigger                       |
| --------------------- | ------------------------------------------------------------ | ------------------------------------- |
| S2-b native SNN       | surrogate-grad BPTT x86 train likely > cap                   | budget unlock OR S2-a F-fail forces pivot |
| Akida Cloud 1-week    | $995 > cap                                                   | budget unlock if F-AK-1 fires AND no fallback acceptable |
| Φ parity full-transformer projection | original C3 carryover (last-layer only); under cap, no new compute justified | budget unlock + raw#10 re-evaluation |

---

## §4 Sequencing recommendation

### §4.1 Decision tree

```
                       ┌─ START (today, 2026-05-03) ─┐
                       │  GPU cap = $200             │
                       └──────────────┬──────────────┘
                                      │
                ┌─────────────────────┴─────────────────────┐
                │                                           │
        ┌───────▼────────┐                          ┌───────▼────────┐
        │ SLM cap-slate  │                          │ NLM stage 1    │
        │ A1+C1(soft)+   │                          │ spec only      │
        │ D1+D3          │                          │ $0, already    │
        │ $0-150, 1-2d   │                          │ landed         │
        └───────┬────────┘                          └───────┬────────┘
                │                                           │
                │ (independent, parallelizable)             │
                │                                           │
                └──────────────────┬────────────────────────┘
                                   │
                       ┌───────────▼────────────┐
                       │ wait for events:       │
                       │  - .roadmap.eeg B1-B4  │
                       │  - __NLM_HW_DELIVERED__│
                       │  - budget unlock       │
                       └───────────┬────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
        ┌───────▼──────┐   ┌───────▼──────┐   ┌───────▼──────┐
        │ EEG PASS:    │   │ HW arrives:  │   │ budget +$N:  │
        │ C1 real-data │   │ NLM stage 2+3│   │ SLM B-axis   │
        │ measurement  │   │ $0-100 GPU   │   │ unlock       │
        │ unlock       │   │              │   │              │
        └──────────────┘   └──────────────┘   └──────────────┘
```

### §4.2 Recommended order of execution (no interactive ambiguity)

1. **immediate (this cycle, $0–150 GPU)**: SLM cap-slate (A1 + C1-soft + D1 + D3). 100% mac-local. No external dependency beyond Brennan-Hale 2019 corpus download (free, CC-BY).
2. **passive watch ($0)**: NLM stage 1 stays in spec-frozen state. Weekly poll cadence per `.roadmap.nlm_neuromorphic_lm` cond.1 already in place — no further write under cap.
3. **on `.roadmap.eeg` B1-B4 PASS event**: re-enter C1 (real-data TRF measurement) — fits inside original $0–100 cap-allowance, no re-budget needed.
4. **on `__NLM_HW_DELIVERED__`=YES event**: execute NLM stage 2 (D+0 bring-up, $0 GPU) → stage 3 (S1+S2-a, $0–100 GPU). Stays inside cap.
5. **deferred until budget unlock**: SLM B-axis (prosody, $200–800) + NLM S2-b + NLM Akida Cloud 1-week.

### §4.3 Anti-patterns under cap

- DO NOT attempt SLM B1 with reduced-quality LoRA on mac-local CPU — wall extends from 1–2d to 5–10d, scope creep risk high, mac thermal risk.
- DO NOT pre-pay Akida Cloud 1-week against unconfirmed F-AK-1 — wait for actual ARM64 install failure.
- DO NOT collapse cap-respecting C1 (mock-EEG fixture) into "C1 PASS" claim — it is **scaffold + smoke**, not the published-baseline measurement.
- DO NOT mix SLM B-axis exploration into the cap-respecting cycle and quietly burn cap — explicit ledger required.

---

## §5 Honest C3 caveats (raw#10) — under-cap delta

Beyond the original 6 caveats in `docs/slm_phase3_spec_2026_05_03.md` §6 (still all in force), the cap re-spec adds:

1. **C-cap-1 SLM under cap = 3 axes, not 4.** B-axis (prosody, $200–800 RunPod A100 LoRA) is **structurally outside cap**. SLM "Phase 3" delivered under cap is a **3-axis Phase 3** (acoustic + EEG-bridge-scaffold + RT-stub), not the 4-axis original. If "Phase 3 met" is later claimed without flagging this delta, that is a misrepresentation. Honest label: **"SLM Phase 3 cap-subset"**.

2. **C-cap-2 C1 under cap is scaffold-only, not measurement.** Brennan-Hale 2019 download + mTRF library smoke + mock-EEG fixture establishes the pipeline shape, but the published-baseline Pearson r ≥0.15 falsifier requires real-data run, which is `.roadmap.eeg` B1-B4 hard-blocked. Cap path **does not advance the C-axis falsifier state** beyond "pipeline exists"; it just keeps the spec executable for the day B1-B4 lands.

3. **C-cap-3 NLM "GPU cost ≤ $200" is true only because hardware capex is bucketed separately.** The $1,495 (paid) + $200–500 (peripherals) is real money, not GPU money. If the user's intent is "total NLM Phase 3 cost ≤ $200," NLM is **not cap-fit at all** — only the post-arrival dev-compute fragment fits. This re-spec interprets "GPU 비용" literally (compute spend) per user phrasing; if the intent was "total spend," NLM stays DEFERRED until budget unlock per original spec.

---

## §6 Doc meta

```
   doc          | docs/slm_nlm_200cap_respec_2026_05_03.md
   type         | spec re-derivation (cost cap layered on existing Phase 3 specs)
   substrate    | READ-ONLY: slm_phase3_spec_2026_05_03.md, nlm_phase3_spec_2026_05_03.md, slm_stage12_landed_2026_05_03.ai.md
   write        | this doc only
   raw#9        | NO .py (markdown only)
   raw#15       | NO personal paths
   execute      | none
   commit       | none
   marker       | none (re-spec doc only, marker 측 별도 land cycle)
   cap          | GPU compute cost ≤ $200 (user constraint)
```

end-of-doc.
