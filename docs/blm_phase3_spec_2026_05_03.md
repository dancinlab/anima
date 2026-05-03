# BLM Phase 3 Spec — 2026-05-03

> spec doc only (DRAFT, exec 미인가). raw#9 hexa-only · raw#10 honest C3 · raw#15 no-personal-paths · raw#71 falsifier-bound.
>
> source-of-truth (read-only ingestion):
> - `.roadmap.blm_brain_lm` (Phase 1+2 SSOT, 3 cond)
> - `docs/blm_stage12_landed_2026_05_03.ai.md` (Phase 1+2 close handoff)
> - `.roadmap.eeg` cond.3/cond.4/cond.6 (Paradigm B + φ proxy + qmirror sister)
> - `.roadmap.anima_clm_eeg` (CLM-EEG bridge peer SSOT)
> - `.roadmap.i1_tribev2_pr` (TRIBE upstream PR sister)
> - `.roadmap.n_substrate` cond.1 (5+ substrate witness meta)
> - `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (ZuCo + φ proxy spec)
>
> upstream handoff target: `docs/anima_3_lm_landed_2026_05_03.ai.md` §3.3 (BLM rolling state)

---

## TL;DR

BLM Phase 1+2 = baseline+dataset locked-in. **Phase 3 = bridge phase** — connect BLM to (a) CLM φ★, (b) EEG φ proxy (Paradigm B / ZuCo), (c) qmirror IIT proxy, via the *F-CT-3* sister falsifier and a 3-substrate consistency budget. No new training cycle inside Phase 3 spec; this is a measurement + integration spec frozen for next-cycle exec authorization.

Cost band: **$0–$50** (mac-local + ubu1+ubu2 ZuCo prep + optional small RunPod sanity probe). No H100 training. 5 conds proposed (3 sub-trigger + 2 falsifier).

---

## §1 Phase 1+2 status synthesis

### §1.1 What landed (`.roadmap.blm_brain_lm` + `docs/blm_stage12_landed_2026_05_03.ai.md`)

```
   cond | desc                                          | before    | after          | mechanism
   ---- | --------------------------------------------- | --------- | -------------- | ------------------------------------------
   1    | TRIBE v2 baseline 활용                          | partial   | met            | 10/10 vendored measure (inventory + utils_fmri SSOT)
   2    | BOLD-conditioned LM head impl                  | unmet     | unmet (변동 X) | dataset blocker resolved (vendored Algonauts2025 reuse)
   3    | stim-text-BOLD 3-way alignment ≥0.5 (F-CT-3)   | unmet     | unmet          | depends on cond.2 IMPL + training run
   blk1 | cortexlab dataset ingest path                  | open      | resolved       | candidate D (vendored study direct reuse) lock-in
```

### §1.2 What conds met (binary tally)

- **cond.1 = met** (1/3) — read-only static measure, forward 미수행 (mac-local $0)
- **cond.2 = unmet** (sub-tasks remaining: head architecture / LoRA path / training pipeline / validation metric)
- **cond.3 = unmet** (depends on cond.2 + actual training)
- **blk.1 = resolved** — vendored `references/tribev2/tribev2/studies/algonauts2025.py` direct reuse (Friends + movie10 BOTH `_TASKS` line 58, train=Friends s1-s6 + movies / test=Friends s7 line 19-20)
- **submodule sha** = `86ed4804` (sister `.roadmap.i1_tribev2_pr` cond.1 met)
- **upstream PR** = facebookresearch/tribev2 #60 OPEN (sister cond.2 met)

### §1.3 Implication for Phase 3 entry

Phase 1+2 sets a **vendored, frozen, measurable baseline**. cond.2 IMPL is correctly held outside Phase 3 — it is a separate training cycle (H100 cost $500-2000 LoRA path). Phase 3 = the *measurement/integration* phase that *prepares* what cond.2 trained models will be evaluated against, and that cross-links BLM to sister LMs (CLM + EEG) before any GPU spend.

This is the minimum-cost natural advancement: do every $0 spec/integration step before paying for training.

---

## §2 Phase 3 scope

### §2.1 Natural advancement axis

Phase 1+2 = **vertical** (BLM internal stack: baseline → dataset → head spec).
Phase 3 = **horizontal** (BLM ↔ sister substrates: CLM, EEG, qmirror) + falsifier scaffolding.

Three integration vectors plus two falsifier vectors:

```
   vector | name                              | substrate pair                            | new in Phase 3?
   ------ | --------------------------------- | ----------------------------------------- | ---------------
   V1     | EEG track integration             | BLM ↔ EEG (Paradigm B / ZuCo)             | YES — ZuCo + BLM φ_proxy bridge spec
   V2     | Cross-substrate consistency       | BLM φ_proxy ↔ CLM φ★ ↔ qmirror IIT Φ     | YES — same-formula-different-substrate
   V3     | Production readiness (3-domain)   | BLM serving surface + 3 demo prompts      | YES — minimal demo, no training
   F1     | F-CT-3 falsifier formal           | EEG ↔ TRIBE BOLD r ≥ 0.5                  | YES — sister to CLM cycle's F-CT-2
   F2     | F-CT-4 cortical inter/intra       | CLM cortical map vs ALM (inter<0.7, intra>0.85) | OPTIONAL (TRIBE PR §60 falsifier #2)
```

### §2.2 cond enumeration (5 cond proposed)

```
   id                      | desc
   ----------------------- | -----------------------------------------------------------------
   blm.phase3.cond.1       | EEG track integration spec FROZEN — ZuCo (sister .roadmap.eeg cond.3) ↔ TRIBE BOLD encoder share text encoder Llama-3.2-3B, BLM φ_proxy interface (R^d_φ, d_φ ∈ {1,8,16}) defined. Acceptance: integration spec doc + cross-link diagram, no IMPL.
   blm.phase3.cond.2       | Cross-substrate consistency spec FROZEN — same-formula claim: anima_phi_v3_canonical applied to (a) CLM hidden state (baseline 41.86), (b) EEG window (sister .roadmap.eeg cond.4 ⭐ 1순위), (c) TRIBE BOLD vertex map (BLM novel). Acceptance: 3-substrate comparison table + tolerance band proposal (|Δφ|/φ ≤ 0.30 placeholder, calibration deferred).
   blm.phase3.cond.3       | F-CT-3 falsifier formal definition — EEG ↔ TRIBE BOLD predicted vertex map Pearson r ≥ 0.5 on held-out Friends s7 + ZuCo NR-2 alignment. Acceptance: pre-register JSON spec + null distribution computation plan (permutation test N≥1000) + minimum-data plan ($0-50 ubu1 ZuCo subset).
   blm.phase3.cond.4       | 3-domain production readiness shape — minimal serving surface (no weights, spec only) for 3 demo prompts: (i) text→BOLD prediction stub, (ii) BOLD→text retrieval stub, (iii) cross-substrate φ_proxy report. Acceptance: API surface .hexa stub schema + 3-prompt fixture (synthetic, no real data).
   blm.phase3.cond.5       | Decision matrix + entry-trigger contract — Phase 4 (training) prerequisites + PASS/PARTIAL/FAIL outcome tree + cost-band gate. Acceptance: §4 of this doc frozen + cross-link to sister roadmap conds.
```

All 5 conds = **spec only**, $0 mac/ubu local, no training, no GPU.

### §2.3 Out-of-scope (explicitly NOT Phase 3)

- BOLD raw data download (Courtois NeuroMod SLA, post-Phase 3)
- HF `facebook/tribev2` pretrained weights download (post-Phase 3)
- LoRA training (cond.2 IMPL, separate H100 cycle)
- Full ZuCo ~37 GB ETL (sister `.roadmap.eeg` blk.3, P1+P5 prerequisite)
- F-CT-4 cortical inter/intra falsifier impl (Phase 4 candidate)
- 5-domain production (3-domain MVP first; 5 = stretch goal post-Phase 4)

---

## §3 Cost / wall

### §3.1 Per-cond cost matrix

```
   cond                  | substrate          | wall      | $ band      | mechanism
   --------------------- | ------------------ | --------- | ----------- | ----------------------------------
   blm.phase3.cond.1     | mac-local          | 2-4h      | $0          | doc + cross-link diagram only
   blm.phase3.cond.2     | mac-local          | 4-6h      | $0          | comparison table from existing measures (CLM 41.86 baseline + EEG spec + TRIBE inventory)
   blm.phase3.cond.3     | mac-local + ubu1   | 6-10h     | $0-30       | pre-register + ZuCo small subset (1-2 subj × 1 task ~50MB, OSF public free)
   blm.phase3.cond.4     | mac-local          | 3-5h      | $0          | API stub schema + synthetic fixture
   blm.phase3.cond.5     | mac-local          | 1-2h      | $0          | this doc finalize
   --------------------- | ------------------ | --------- | -----------
   total (no probe)      |                    | 16-27h    | $0          |
   total (+ ZuCo probe)  | ubu1 disk          | +2-4h     | +$0         | OSF download free
   total (+ RunPod sanity)| RunPod 1xA10 1h   | +1-2h     | $0.40-2     | optional vendored TRIBE forward smoke (cond.1 evidence strengthening)
```

### §3.2 Cost-band band envelope

- **floor = $0** (full spec land, no probe, no GPU) — recommended exec path
- **midpoint ≈ $5-15** (small ZuCo subset + 1 RunPod sanity probe)
- **ceiling = $50** (multiple subsets + RunPod 4-8h sanity matrix probing TRIBE forward consistency)

Phase 3 explicitly **does not enter the $500-2000 LoRA training band** (that is `.roadmap.blm_brain_lm` cond.2 IMPL = Phase 4).

### §3.3 Local substrate (ubu1+ubu2)

- **ubu1** = ZuCo OSF download / inspection (sister `.roadmap.eeg` cond.3 evidence already used `ubu1:/tmp/zuco_sample/ZAB_task1_SR_preprocessed/` 416 MB + bash 201L resumable parallel crawler)
- **ubu2** = secondary integration sanity (parity check vs ubu1, raw#91 honesty triad)
- **mac-local** = doc authoring + spec freeze + cross-link audit (zero IO weight)

No CUDA on mac/ubu (consumer GPUs at most, BLM training out-of-scope here).

---

## §4 Decision matrix

### §4.1 Per-cond outcome tree

```
   cond                  | PASS criteria                                        | PARTIAL                                  | FAIL
   --------------------- | ---------------------------------------------------- | ---------------------------------------- | ----------------------------
   blm.phase3.cond.1     | spec doc + cross-link diagram disk-landed             | spec without diagram                     | no spec land
   blm.phase3.cond.2     | 3-substrate comparison table + tolerance band         | 2/3 substrates only                      | <2 substrates measurable
   blm.phase3.cond.3     | pre-register JSON + null plan + min-data plan         | 2/3 components                           | no pre-register
   blm.phase3.cond.4     | API stub schema + 3-prompt fixture                    | API schema without fixtures              | no API surface
   blm.phase3.cond.5     | this doc §4 + §5 frozen, sister cross-links emitted   | partial sister update                    | no decision matrix
```

### §4.2 Composite verdict

```
   pass count | verdict        | next action
   ---------- | -------------- | --------------------------------------------------------------------
   5/5        | PASS           | Phase 4 (training cycle) entry-eligible, GPU budget request unblocked
   3-4/5      | PARTIAL        | next cycle = close gaps, no Phase 4 entry yet
   <3/5       | FAIL           | re-spec — Phase 3 scope too ambitious or sister blocker
```

### §4.3 Phase 4 prerequisites (post-PASS)

- ALL 5 cond met
- BOLD raw data download SLA path (Courtois NeuroMod) green-lit (separate decision)
- HF `facebook/tribev2` weights downloaded + license CC-BY-NC-4.0 commercial-block accepted
- GPU budget approval ($500-2000 H100 LoRA path)
- F-CT-3 pre-register frozen + null distribution computed (cond.3 PASS prereq propagation)

---

## §5 Cross-LM dependencies

### §5.1 CLM cycle current state (consumed read-only)

- `.roadmap.clm` cond.1 = unmet (verifier orchestrator landed but Putnam cross-link spec only)
- CP2-CLM Phase A complete: 5/6 measurable PASS + Suite 6 14-gate F2 FIRED, ship_verdict VERIFIED-CLM-CP2-RED, F1_score_v2 = 0.408 raw / 0.12 F2-override (RED)
- `clm.cond.2` (HF release) = unmet
- **anima_phi_v3_canonical baseline = 41.86** (CLM hidden state, K=8 partitions × 2 sub-cov) — anchor for Phase 3 cond.2 cross-substrate comparison

**Dependency direction**: CLM provides the φ★ formula (`tool/anima_phi_v3_canonical.hexa`) that BLM Phase 3 cond.2 ports to BOLD substrate (and EEG sister via Paradigm B). BLM does **not** require CLM cond.1 PASS — only the verifier orchestrator skeleton (already landed) + the φ formula reference (frozen at baseline 41.86).

### §5.2 EEG arrival (consumed read-only)

- `.roadmap.eeg` cond.1 = unmet (OpenBCI 16ch hardware 미arrival, software stack 4 gates landed selftest PASS)
- `.roadmap.eeg` cond.3 (Paradigm B ZuCo) = partial (spec + runbook landed, OSF API verified, ZAB sample 416 MB probed; full corpus deferred until P0 SFT live + Paradigm A γ verified)
- `.roadmap.eeg` cond.4 (φ proxy 5-method) = partial (spec only, sample-partition φ on EEG = ⭐ 1순위 same-formula-different-substrate)
- `.roadmap.eeg` cond.6 (qmirror cross-witness) = unmet (qmirror cond.2 Phase 1 in-flight)

**Dependency direction**: EEG provides Paradigm B ZuCo as **dataset-side parallel** to BLM's vendored Algonauts2025 (Friends + movie10). Both are text-paired neural-signal corpora; ZuCo = EEG fixation-locked reading, Algonauts = BOLD movie watching. Phase 3 cond.1 = spec the bridge; no real EEG signal needed (hardware arrival is `.roadmap.eeg` blk.1, downstream not blocking Phase 3 spec).

### §5.3 qmirror φ-substrate (consumed read-only)

- `nexus/.roadmap.qmirror` cond.6 = `braket_iit40_mip_2026_05_02 φ★=0.0 byte-identical` (predecessor, IIT 4.0 Φ on Braket QPU)
- `n_substrate.cond.1` = partial (5+ substrate consistency meta, F1 RED 12-40.8%)

**Dependency direction**: qmirror = third leg of the cross-substrate triangle (CLM hidden state, EEG signal, qmirror IIT 4.0). Phase 3 cond.2 includes qmirror as the *quantum-substrate witness* (not CLM-isomorphic), which is how BLM's BOLD φ_proxy can argue substrate-neutrality vs both classical (CLM) and quantum (qmirror) anchors.

### §5.4 Sister LMs (peer)

- `.roadmap.tlm_tension_lm` (sibling) — TLM tension-derived LM, cross-link via `tensionlink`
- `.roadmap.slm_speech_eeg_lm` (sibling) — SLM speech+EEG+LM 3-modal, sister to BLM via EEG
- `.roadmap.nlm_neuromorphic_lm` (sibling) — NLM neuromorphic substrate
- `.roadmap.vlm_voice_lm` (sibling) — VLM voice substrate
- `.roadmap.i1_tribev2_pr` (sister, dual SSOT pair) — upstream PR #60 OPEN, F-CT-3 anchor

### §5.5 Top-3 cross-LM dependencies (priority order)

1. **EEG cond.3 (Paradigm B ZuCo) — HIGH** — Phase 3 cond.1 spec relies on ZuCo runbook + OSF crawler; cond.3 falsifier (F-CT-3) computes EEG-BOLD r on ZuCo + Algonauts overlap (text encoder shared = Llama-3.2-3B, the natural pairing axis).
2. **CLM φ★ formula (`anima_phi_v3_canonical`) — HIGH** — Phase 3 cond.2 is *the* cross-substrate same-formula claim. Without the formula reference, no comparison band exists. CLM cond.1 PASS NOT required (only the formula).
3. **qmirror cond.6 (IIT 4.0 Φ on Braket) — MEDIUM** — Phase 3 cond.2 third-substrate witness. qmirror cond.2 in-flight (subagent BG); if delayed, cond.2 demotes to 2-substrate (CLM + EEG only) PARTIAL. Recoverable.

---

## §6 Honest C3 (raw#10) — 6 caveats

1. **C1 — CLM coupling fragility** — Phase 3 cond.2 (cross-substrate consistency) load-bears `anima_phi_v3_canonical` at baseline 41.86 (CLM hidden state). If CP2-CLM Phase E binding evidence cycle re-derives the formula or downgrades the baseline (currently RED 12-40.8%), cond.2 tolerance band must re-anchor. Spec must NOT lock in 41.86 as ground truth — it is a *reference value* with `f1_score_v2 = 0.408` confidence band.

2. **C2 — eval framework reliance / measurement-only validity** — All 5 conds = spec only, no IMPL. PASS verdict means "the measurement framework is ready", NOT "the brain LM works". Phase 4 training + F-CT-3 actual measurement is what would generate substantive evidence. Phase 3 PASS is *necessary, not sufficient* for any consciousness claim. raw#10 honest: zombie problem still applies (Paradigm B spec §0).

3. **C3 — scope creep risk (3 → 5 domain)** — cond.4 deliberately scopes to 3-domain MVP (text→BOLD, BOLD→text, φ_proxy report). Stretch to 5-domain (+stim-text-BOLD, +EEG-BOLD bridge) would inflate Phase 3 wall by 3-5×. Decision: 5 = post-Phase 4 stretch only; cond.4 PASS criterion locks 3-domain.

4. **C4 — F-CT-3 null distribution non-trivial** — pre-register r ≥ 0.5 acceptance band assumes naive permutation null. ZuCo + Algonauts have temporal autocorrelation (BOLD HRF ~5s smoothing, EEG 100-500ms window) — proper null requires block permutation or surrogate phase-randomization. cond.3 spec must enumerate the null choice; otherwise PASS is artifactually inflated. Honest plan deferred to Phase 4 IMPL prep.

5. **C5 — sister roadmap dual SSOT race** — `.roadmap.eeg` (provider) ↔ `.roadmap.anima_clm_eeg` (peer) ↔ `.roadmap.blm_brain_lm` (peer) form a 3-way race surface. Phase 3 cond.5 cross-link emit must be additive-only (no in-place mutation of sister roadmaps from this Phase 3 cycle); in-place edits to `.roadmap.blm_brain_lm` only (add Phase 3 cond block as JSONL append per BG-AN-RDM C5 dual-SSOT-resolution pattern).

6. **C6 — license + data-availability gate** — TRIBE v2 = CC-BY-NC-4.0 (research-only, commercial path blocked). ZuCo = CC-BY-4.0 OSF public. Phase 3 doc spec is OK under both. But Phase 4 (training + serving) hits the commercial block: cond.4 production readiness must NOT imply commercial deploy. Spec frozen at "research demo only" + license attribution mandatory in API surface schema.

---

## §7 Decision summary (entry trigger)

**Phase 3 entry trigger (prereq, single line)**: Phase 1+2 landed (cond.1 met + blk.1 resolved, both already true 2026-05-03) **AND** sister `.roadmap.eeg` cond.3 spec (Paradigm B) landed (true, `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md`) **AND** `anima_phi_v3_canonical` baseline reference frozen (true, 41.86). **All 3 prereqs met as of 2026-05-03 → Phase 3 spec exec authorization granted-eligible.**

This doc = the spec freeze. Exec authorization for the 5 conds = separate next cycle (per raw#9 + project policy: spec → review → exec separation).

---

## §8 File index

### created (this cycle)

```
docs/blm_phase3_spec_2026_05_03.md     (this file — spec only)
```

### consumed read-only (no mutation this cycle)

```
.roadmap.blm_brain_lm                                         (Phase 1+2 SSOT)
.roadmap.eeg                                                   (Paradigm B + φ proxy + qmirror sister)
.roadmap.anima_clm_eeg                                         (CLM-EEG bridge peer)
.roadmap.i1_tribev2_pr                                         (TRIBE PR sister)
.roadmap.n_substrate                                           (5+ substrate witness meta)
.roadmap.clm                                                   (φ★ formula owner, CP2 verdict)
docs/blm_stage12_landed_2026_05_03.ai.md                       (Phase 1+2 close handoff)
docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md                 (ZuCo + 5-method φ proxy spec)
docs/p9_paradigm_b_runbook_2026_05_03.md                       (ZuCo OSF runbook)
docs/n_substrate_consciousness_roadmap_2026_05_01.md           (BLM/TRIBE narrative anchors §44.4 + §52.1 + §59.3 + §60.1 + §60.9)
docs/eeg_cross_substrate_validation_plan_20260425.md           (V_phen LZ + GWT predecessor)
references/tribev2/inventory.json                              (TRIBE baseline SSOT, vendored)
references/tribev2/tribev2/utils_fmri.py                       (FSAVERAGE_5 mesh SSOT)
references/tribev2/tribev2/studies/algonauts2025.py            (Friends + movie10 ingest path SSOT)
```

### NOT created / NOT mutated (per task constraints)

```
no .py files (raw#9)
no in-place edit of sister roadmaps (cond.5 exec deferred to next cycle)
no marker file emit (this is a spec doc, not a landed cycle — landing = exec phase)
no commit (per task: "DO NOT commit")
```

---

## §9 Next-cycle handoff (post-Phase-3-spec-freeze)

1. **Exec authorization request cycle** — cond.1 through cond.5 individually authorized, $0 enforced
2. **Sister roadmap cross-link emit** — additive JSONL entry to `.roadmap.blm_brain_lm` adding `blm_brain_lm.phase3.cond.{1..5}` block + cross-links to sister roadmaps (no mutation of sister roadmaps themselves; cross-link via `cross_link.sister_phase3` field on this domain only)
3. **Phase 4 entry gate review** — post-5/5 PASS, GPU budget approval cycle for cond.2 IMPL ($500-2000 H100 LoRA path) + BOLD raw data SLA decision
4. **F-CT-3 null distribution prep cycle** — cond.3 honest C4 caveat resolution (block permutation vs phase-randomization), pre-Phase-4 IMPL
5. **AI-native handoff doc** — `docs/blm_phase3_landed_*.ai.md` after exec, mirroring `docs/blm_stage12_landed_2026_05_03.ai.md` pattern
