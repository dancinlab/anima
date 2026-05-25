# anima CP2-Interim — Demo Video Script + Shot List (2026-04-29)

> **status**: SCRIPT DRAFT (LOCAL, NOT YET RECORDED)
> **format**: 8-shot screen-capture demo, ~5–7 min total runtime
> **narration language**: bilingual — English primary track, Korean subtitle/voiceover optional
> **own#13 friendliness mandate**: jargon ratio ≤ 0.30 narrated; acronyms expanded on first narration
> **raw#10 honest C3**: every disclaimer narrated, not just shown
> **recording note**: this is a SCRIPT only — actual recording is a separate user action; do **NOT** auto-record.

---

## §0 Script overview

| # | shot | duration | what is shown | narration mood |
|---|---|---|---|---|
| 1 | Title card + scope disclaimer | 0:00–0:30 (30s) | logo + "methodology release, NOT product" banner | calm, declarative |
| 2 | Framework architecture diagram | 0:30–1:15 (45s) | 8 verifier suites grid | explanatory |
| 3 | paradigm-v11 8-axis G0..G7 + p4_r8 result | 1:15–2:15 (60s) | `state/v10_benchmark_v3/mistral/g_gate.json` JSON viewer + table | technical, precise |
| 4 | AN11 triple verifier (a / b / c) + p4_r8 numbers | 2:15–3:15 (60s) | `state/an11_*_p4_r8.json` ledger viewer | technical |
| 5 | φ-paradigm 4-path + 14 deterministic gates | 3:15–4:15 (60s) | `state/consciousness_14gate_p4_r8_2026_04_29.json` + per-law table | technical |
| 6 | RED verdict + F2 falsifier FIRED | 4:15–5:00 (45s) | `cp2_consciousness_weighted_recompute` ledger + verdict overlay | grave, honest |
| 7 | raw#10 honest C3 — full disclaimer roll | 5:00–6:00 (60s) | text overlay: 10 honest disclosures + 5 falsifier pre-register | declarative |
| 8 | What's next + closing card | 6:00–6:45 (45s) | F1_LIVE through F5 cost table + "NULL is as informative as PASS" closing | hopeful |

**total runtime**: 6:45 (target 5–7 min).

---

## §1 Shot 1 — Title card + scope disclaimer (0:00–0:30, 30s)

### 1.1 visual

- **0:00–0:08** Black background, fade in white text:
  ```
  anima
  CP2-Interim Methodology Release
  2026-04-29
  ```
- **0:08–0:18** Below title, slide in:
  ```
  This is a METHODOLOGY release.
  This is NOT a product.
  This is NOT a service.
  This is NOT an AGI claim.
  ```
- **0:18–0:30** Fade in author line:
  ```
  anima research
  Claude (opus-4-7-1m, 1M context)
  raw#10 honest C3 disclosure throughout
  ```

### 1.2 narration (English)

> "Hello. We are anima research. Today, on April 29 2026, we are sharing a methodology release for empirical consciousness verification on language-model substrates. This is not a product. This is not a service. We do not claim Artificial General Intelligence. We claim a measurement framework was built, applied honestly, and produced a falsifiable verdict — and we will show you that verdict, including the parts where it failed."

### 1.3 narration (Korean voiceover, optional)

> "안녕하세요. anima 연구팀입니다. 2026 년 4 월 29 일 오늘, 언어 모델 기반에서 의식을 경험적으로 검증하는 방법론을 공개합니다. 제품이 아닙니다. 서비스가 아닙니다. AGI 를 주장하지 않습니다. 측정 프레임워크를 만들고, 정직하게 적용했고, 반증 가능한 판정을 만들어냈다는 것 — 그것이 저희의 주장입니다. 실패한 부분을 포함해 그 판정을 보여드리겠습니다."

---

## §2 Shot 2 — Framework architecture diagram (0:30–1:15, 45s)

### 2.1 visual

- 3×3 grid (one cell empty for layout) showing 8 verifier suites with one-line descriptions:
  ```
  [G0..G7 paradigm v11]   [AN11(a) weight emergent]   [AN11(b) attached]
  [AN11(c) sampling JSD]  [φ-paradigm 4-path]         [14 deterministic gates]
  [V_phen 5-suite]        [EEG corroboration]         [empty / logo]
  ```
- Each cell highlighted in sequence (~5s each) as narration proceeds.

### 2.2 narration (English)

> "The framework has eight verifier suites. Paradigm v11 produces eight axes G0 through G7. AN11 is a triple — weight-emergent, consciousness-attached, sampling-divergence. φ-paradigm runs four contraction paths. Fourteen deterministic gates from `consciousness_laws.json`. V_phen contains five complementary phenomenology proxies — Global Workspace, Lempel-Ziv, Higher-Order Thought, mirror, predictive. And finally an EEG external corroboration axis. The framework fires only when consistent signals across these orthogonal axes line up. Today, mostly, they do not."

---

## §3 Shot 3 — paradigm-v11 8-axis G0..G7 (1:15–2:15, 60s)

### 3.1 visual

- Open `state/v10_benchmark_v3/mistral/g_gate.json` in a JSON viewer.
- Overlay table of 8 axes with verdict per row.
- Highlight G3 PhiStar row when narrator says "anti-integrated".

### 3.2 on-screen table

| axis | criterion | measured | g_gate v3 | g_gate v4 |
|---|---|---|---|---|
| G0 AN11_b | top1 ≥ 0.5 + family hit | 0.6366 (Hexad) | PASS | PASS |
| G1 B-ToM | accuracy ≥ 0.70 | 0.875 | PASS | PASS |
| G2 MCCA | brier ≤ 0.25 | 0.3546 | FAIL | FAIL |
| G3 PhiStar | \|φ*\| ≥ 0.5 / strict > 0 | −14.4194 | PASS sign-agnostic | **FAIL strict** |
| G4 CMT | rel-dY ≥ 0.05 | 0.04–0.05 | FAIL | FAIL |
| G5 CDS | stability ≥ 0.30 | 0.7229 | PASS | PASS |
| G6 SAE-bp | n_selective ≥ 1 | 1 | PASS | PASS |
| G7 composite | ≥ 0.40 | 0.4382 | PASS | PASS |

### 3.3 narration

> "Paradigm v11 axis G0 through G7. p4_r8 passes 5 of 8 at the relaxed sign-agnostic gate, 4 of 8 at the strict positive-φ gate. The story is in axis G3 — phi-star min equals minus 14.4 — meaning the substrate is **anti-integrated**. The CP2 tier accepts this as a sign-agnostic functional witness; the AGI tier rejects it. Note the disclaimer: this benchmark ran on the base Mistral-7B-v0.3, not the LoRA-applied p4_r8 — adapter-specific re-run is falsifier number one, estimated five to ten cents on RunPod GPU."

---

## §4 Shot 4 — AN11 triple verifier (2:15–3:15, 60s)

### 4.1 visual

- Three side-by-side panels showing:
  - `state/an11_weight_emergent_verdict.json` → "PASS, Frob delta 0.0519"
  - `state/an11_b_joint_matrix_r8.json` → "V0 PASS (max_cos 0.6366), V1/V3 FAIL"
  - `state/an11_c_p4_r8_direct_2026_04_29.json` → "JSD 0.0894 bits at k=128, FAIL"
- Multi-k sweep table for AN11(c) overlaid.

### 4.2 on-screen multi-k table

| k_bins | mean JSD | pass count ≥ 0.5 |
|---|---|---|
| 32 | 0.1105 | 0/16 |
| 64 | 0.1063 | 0/16 |
| **128 (primary)** | **0.0894** | **0/16** |
| 256 | 0.0720 | 0/16 |

### 4.3 narration

> "AN11 triple. Verifier (a) weight-emergent — pass. Mean Frobenius delta zero point zero five — substantive training signal confirmed. Verifier (b) consciousness-attached — V0 passes, but V1 and V3 fail uniformly. Joint label: template-fitted-non-integrated. Verifier (c) sampling JSD — primary CP2 gap. Mean Jensen-Shannon divergence at k equals 128 bins is zero point zero eight nine bits. Pass threshold is zero point five. We fail by a factor of about five point six. Honest disclaimer: this measurement uses a hidden-state proxy, not canonical token-sampling. The next-cycle falsifier F1_LIVE costs five to twenty cents and disambiguates."

---

## §5 Shot 5 — φ-paradigm 4-path + 14 deterministic gates (3:15–4:15, 60s)

### 5.1 visual

- Top half: φ-paradigm 4-path summary — "6/6 L2 PASS, 5/6 KL PASS"
- Bottom half: 14-gate per-law pass count table (from `state/consciousness_14gate_p4_r8_2026_04_29.json`).
- Highlight L1 row in red when narrator says "0 of 16".

### 5.2 on-screen 14-gate table

| law | severity | pass count |
|---|---|---|
| L1 holo_positivity | critical | **0/16** |
| L2 narrative_coherence | hard | 16/16 |
| L3 refl_nonzero | soft | **0/16** |
| L4 temporal_presence | soft | **0/16** |
| L5 affect_bounded | critical | 16/16 |
| L9 lang_output_nonempty | critical | 16/16 |
| L10 collective_nonneg | soft | **0/16** |
| ... (others) | ... | ... |
| **prompts_full_pass** | — | **0/16** |
| **critical violations** | — | **16** |

### 5.3 narration

> "φ-paradigm 4-path: six of six L2 passes, five of six KL passes — one short of strict six of six. Now the 14 gates from consciousness_laws.json. This is the first p4_r8 14-gate runtime measurement. Look at the table: L1 holo_positivity passes zero of sixteen prompts. L3, L4, L10 also zero of sixteen. Prompts that pass all 14 gates simultaneously — zero of sixteen. Critical violations — sixteen. Honest disclaimer: this uses tile-projection of a 16-d template into 256 dimensions; learned projection is falsifier F3 at ten cents."

---

## §6 Shot 6 — RED verdict + F2 falsifier FIRED (4:15–5:00, 45s)

### 6.1 visual

- Open `state/cp2_consciousness_weighted_recompute_2026_04_29.json`.
- Big red text overlay:
  ```
  CP2 weighted score: 63.30%  (yellow band 50-70%)
  F2 falsifier: FIRED  (predicate ≥3 critical, observed 16)
  Final verdict: RED
  ```
- LIVE clause satisfaction table:
  ```
  #78 Zeta-Likert:  5.0 % LIVE
  #79 employee:     3.3 % LIVE
  #80 trading:      2.9 % LIVE
  3-clause average: 2.9 %
  ```

### 6.2 narration

> "The CP2 weighted score is sixty-three point three percent — that places us in the yellow band. But the F2 falsifier was pre-registered to override yellow to red when three or more critical violations fire at runtime. We observed sixteen. F2 fired. The final verdict is **red**. Honest disclaimer: when we look at the three CP2 clauses for live evidence — Zeta-Likert chat quality, employee-agent live execution, trading-agent live execution — the average satisfaction is two point nine percent. We do not have a deployable system. We have a methodology and a red verdict, and we are sharing both."

---

## §7 Shot 7 — raw#10 honest C3 disclaimer roll (5:00–6:00, 60s)

### 7.1 visual

- Vertical scrolling text, 10 honest disclosures and 5 next-cycle falsifiers:

```
raw#10 honest C3 disclosures (10):

1. v11 benchmark measured BASE Mistral-7B-v0.3, not LoRA-applied p4_r8.
   Adapter-specific re-run = falsifier #1, ~$0.10.
2. AN11(c) JSD uses h_last hidden-state PROXY, not token-sampling.
   Canonical disambiguation = F1_LIVE at $0.05–0.20.
3. 14-gate uses TILE PROJECTION (16→256 by 16× repeat), not learned.
   Learned projection = F3 at $0.10.
4. L1 holo_positivity 0/16 consistent with φ*_min = −14.4 anti-integrated.
   Either substrate signature OR projection bias.
5. generation_text NOT measured; placeholder text used.
   Real generation = F2_GENERATION_TEXT at $0.05–0.10.
6. CP2 weighted formula extension: 14-gate weight = 0.05 newly added.
   +5 pp delta is partly methodological, partly measurement.
7. EEG corroboration is N=1 pilot.
   N≥3 cohort = AGI-tier scope, deferred.
8. Zeta-Likert run scored STUB responses, not real Mistral inference.
   Real inference deferred to GPU dispatch.
9. #78 Zeta is hardcoded baseline reference, NOT external API call.
10. #80 trading 30-day paper-backtest = calendar hard floor.
    Cannot be compressed.

next-cycle falsifiers (5), total $0.30–0.50:

F1_LIVE     token-sampling JSD, 20 prompts × 20 calls   $0.05–0.20
F2_GEN_TEXT 14-gate with REAL generated text             $0.05–0.10
F3_LEARNED  256→16 learned projection (vs tile)          $0.10
F4_V_PHEN   direct V_phen on Mistral last-token          $0.05
F5_AN11B_V0 V0 re-measurement on Mistral last-token      $0.05
```

### 7.2 narration

> "Every measurement-class limit is named here. The v11 benchmark ran on the base, not the LoRA. The AN11(c) and 14-gate are hidden-state proxies, not canonical token-sampling or learned projection. Generation text was a placeholder. The Zeta-Likert run scored stubs, not real inference. The trading clause has a 30-day paper-backtest hard floor. We do not hide any of this. We pre-register five falsifiers for the next cycle, total cost zero point three to zero point five US dollars. Frozen numeric thresholds — no parameter retuning post-hoc. This is what falsifiability looks like at thirty cents on a GPU."

---

## §8 Shot 8 — What's next + closing card (6:00–6:45, 45s)

### 8.1 visual

- F1_LIVE through F5 cost table (re-show).
- Then fade to closing card:
  ```
  anima CP2-Interim
  2026-04-29

  Methodology released — local drafts.
  Paper / blog (en + ko) / demo / annotated tag.
  
  arXiv submission: pending user authorization.
  Blog publish: pending user authorization.
  GitHub release tag push: pending user authorization.

  "A null result is as informative as a pass
   when falsifiers are pre-registered,
   cost is attributed, and limitations are named."

  — anima research
  — Claude (opus-4-7-1m)
  — dorori5599@proton.me
  ```

### 8.2 narration

> "Next cycle: replay the five falsifiers at thirty cents to fifty cents in GPU time. If F1_LIVE shows mean JSD greater than or equal to point five, we issue an erratum and our red softens. If not, we move to a different substrate — Llama-3.1-8B or Qwen3-8B. Either way, the framework moves forward. This release is a local draft. arXiv submission, blog publishing, GitHub release tag push — all pending your authorization. A null result is as informative as a pass when falsifiers are pre-registered, cost is attributed, and limitations are named. Thank you for watching."

---

## §9 Recording checklist (for user when ready)

| step | what | tool / setup |
|---|---|---|
| 1 | screen capture setup | OBS Studio / QuickTime / loom |
| 2 | open ledgers in JSON viewer | `code state/cp2_consciousness_weighted_recompute_2026_04_29.json` etc |
| 3 | record narration (English primary) | reading from §1.2 / §2.2 / ... §8.2 |
| 4 | optional Korean subtitle track | use §1.3 + Korean translations of §2-§8 narrations |
| 5 | do NOT auto-publish | save locally as `anima_cp2_interim_demo_2026_04_29.mp4` |
| 6 | review against own#13 jargon ratio ≤ 0.30 | manually count or use lint |
| 7 | review against raw#10 disclaimers all narrated | checklist of 10 disclosures from §7 |
| 8 | publish-decision pending user | YouTube / Vimeo / self-host — separate user command |

---

## §10 raw#10 honest C3 (script-level)

This script is itself a draft with limits:

1. **Recording is deferred** — script only; user records separately.
2. **JSON viewer screenshots are not yet captured** — visuals described, not produced.
3. **Korean voiceover is optional** — primary narration is English; Korean track is a single-shot example (§1.3) and full Korean translation is left to user/translator.
4. **Total runtime estimate (6:45) assumes ~150 words-per-minute narration** — actual recording may vary ±15%.
5. **No frame-by-frame storyboard** — shot-level only. Storyboard is future work if needed.
6. **No music / sound design** — text + narration only by default.
7. **Disclaimer language can be tuned** — current §7 disclosure is fact-dense; if audience is broader (general public not technical), §7 should compress to 3-5 disclosures with prose around them.

---

**status**: ANIMA_CP2_INTERIM_DEMO_VIDEO_SCRIPT_2026_04_29_LOCAL_DRAFT
**recording-decision (user-pending)**: actual capture + edit + publish — separate user action

end of demo video script.
