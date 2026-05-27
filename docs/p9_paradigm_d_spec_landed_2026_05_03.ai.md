# P9 Paradigm D logit-axis spec + roadmap registration LANDED

**Date**: 2026-05-03
**Phase**: P9 SFT alternative-track (peer to S3 production sweep)
**Cost**: $0 (doc-only spec; no execution)
**Verdict**: **SPEC_LANDED — ready for pre-flight cache search + mini-run authorization**

## TL;DR

Paradigm D was previously **partially specified** (3 sister docs covered the Φ★ scalar axis only) and **NOT registered** in `.roadmap.p9_sft`. This cycle:

1. Verified roadmap status — Paradigm D was MISSING from the 5 existing conds.
2. Wrote the **logit-axis spec** (`docs/p9_paradigm_d_distill_spec_2026_05_03.md`, ~470 LoC, 12 sections) — Hinton 2015 soft-target KL distill from Mistral-7B-Instruct-v0.3 → CLM v4 350M, orthogonal to existing Φ★ axis.
3. Registered new JSONL entry `p9_sft.cond.paradigm_d_distill` as additive 6th cond (no in-place mutation of existing 5).
4. Landed two markers: `p9_paradigm_d_spec_landed.marker` + `p9_paradigm_d_roadmap_registered.marker`.

## §1 컨텍스트

### Pre-existing state

| Item | Status before this cycle |
|------|---------------------------|
| `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` | EXISTS (Φ★ axis parent spec, 240 LoC) |
| `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` | EXISTS (Mistral-7B teacher build for Φ★ side, 360 LoC) |
| `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` | EXISTS (Φ★ z-score distill runbook, 330 LoC) |
| `.roadmap.p9_sft` cond for Paradigm D | **MISSING** — only 5 conds (P0/HF, S3 sweep, F4, benchmark A' spec, benchmark A' base val) |
| Soft-logit / token-KL axis spec | **MISSING** — sister docs explicitly limit to Φ★ scalar signal type |

### User-spec context (per session memory)

- Paradigm D = Mistral-7B teacher distill to CLM v4 350M student
- Substrate: T4 originally ($3.37 spent in prior cycle)
- Status: HALTED (RunPod pod terminated to avoid burn; cache/result status unknown)
- Strategy: teacher generates soft logits or pseudo-targets, student SFT distill from those
- Falsifier candidate: F-D-1 = student matches teacher KL ≤ threshold on holdout

The user's spec specifically calls out the **soft-logit transfer** angle, which the 3 sister docs do NOT cover (they are Φ★ scalar only). This justifies a NEW spec doc rather than amending sisters.

## §2 산출

### Files created

| Path | Size | Purpose |
|------|------|---------|
| `docs/p9_paradigm_d_distill_spec_2026_05_03.md` | ~470 LoC, 12 sections | Logit-axis primary spec |
| `state/markers/p9_paradigm_d_spec_landed.marker` | small | Spec-landed marker |
| `state/markers/p9_paradigm_d_roadmap_registered.marker` | small | Roadmap-registered marker |
| `docs/p9_paradigm_d_spec_landed_2026_05_03.ai.md` | this file | Handoff |

### Files modified

| Path | Change | Type |
|------|--------|------|
| `.roadmap.p9_sft` | +1 JSONL line (entry `p9_sft.cond.paradigm_d_distill`) below the existing header line | **additive only** — header.required_conditions array unchanged, all 5 existing conds untouched |

## §3 Spec doc structure

12 sections of `docs/p9_paradigm_d_distill_spec_2026_05_03.md`:

| § | Topic | Content |
|---|-------|---------|
| 0 | TL;DR | one-table summary, 12 fields |
| 1 | Why a separate spec | logit-axis vs Φ★-axis orthogonality + composability |
| 2 | Teacher selection | Mistral-7B-Instruct-v0.3 PRIMARY (vocab match), Llama-3.2-3B fallback (vocab mismatch path) |
| 3 | Distillation signal type | Top-K=64 logits at T=4 (Hinton 2015 default) |
| 4 | Loss formulation | `α·CE + λ_kl·T²·KL_topK + β·tens + γ_φ·MSE_φ + δ·floor`, schedules, composability with sister axis |
| 5 | Pre-existing partial cache | 6-location search procedure, RunPod terminated-pod forensics, local find verdict (no cache) |
| 6 | Substrate options + cost ranking | (1) Colab T4 $0 / (2) RunPod T4 $7.50 / (3) RunPod H100 $17.50-22.50 |
| 7 | Falsifier F-D-1 | per-token holdout-500 KL ≤ 0.5 nats at T=1 readout, preregistered |
| 8 | Mini-run spec | 1K records × 2K steps, λ_kl ramp 0→0.5, ~$0-7.50, ALL-OF gate |
| 9 | Roadmap registration | additive entry JSON, "no in-place mutation" rationale |
| 10 | Honest C3 | 8 caveats (raw#91 ≥5) |
| 11 | SSOT / pointers | 13 cross-references |
| 12 | Decision summary | 12-row decision table |

## §4 Roadmap registration detail

### Action

Added a new JSONL line to `.roadmap.p9_sft` directly below the header line:

```json
{"type":"entry","id":"p9_sft.cond.paradigm_d_distill","kind":"cond","title":"Paradigm D logit-axis — Mistral-7B-Instruct-v0.3 → CLM v4 350M soft-logit distill","desc":"...","verifier":{...},"status":"unmet","evidence":[...],"blocker_reason":"spec landed; awaiting pre-flight cache search (§5.2) + EXEC authorization for mini-run launch via separate BG","ts":"2026-05-03","kind_note":"additive 6th cond peer to existing 5; Paradigm D is alternative-track to S3 production sweep, not blocking","cross_link":{"sister_axis":"...","substrate_ranking":[...],"falsifier_id":"F-D-1","falsifier_threshold":"per-token holdout-500 KL ≤ 0.5 nats at T=1 readout","cost_band":"$0-50 (mini-run); $30-50 (production single-γ on H100)","compose_with":["S1 LoRA-only","S2 multi-loss","sister Φ★-axis γ_φ term"]}}
```

### Why additive (per raw#15)

The existing 5 conds describe the canonical Strategy S3 + benchmark switch chain. Paradigm D logit-axis is a **parallel research track**, peer to S3, NOT a sequencing blocker. Inserting it as a 6th cond marks it as an alternative path that does not gate S3 production.

### Verification

```
$ awk 'NR>=3' .roadmap.p9_sft | python3 -c "import sys,json; [json.loads(l) for l in sys.stdin if l.strip()]"
# (no error — both lines parse cleanly)
```

## §5 Substrate ranking (완성도 lens)

Per `feedback_completion_quality_recommendation` memory, ranked recommendation:

1. **Free Colab T4 — RECOMMENDED** ($0, completion 8.5/10)
   - Cheapest path; aligns with raw#9 "$0 design only"
   - Quality acceptable (nf4 KL noise below dark-knowledge gradient SNR floor)
   - Failure mode: 12-h session reset; mitigation = chunk to 5 × 10K-record runs

2. **RunPod T4 spot — SECONDARY** ($7.50, completion 9/10)
   - Highest reliability per dollar
   - No session limits; cache fully assembled in one shot
   - Empirical-quality optimum if any cash budget available

3. **RunPod H100 spot — REFERENCE / FALLBACK** ($17.50-22.50, completion 9.5/10)
   - Canonical fp16 (no quantization artifact)
   - Reuses 90% of sister-doc T4 build runbook
   - Pick only if Phase 2.D-logit needs publishable cache without quantization caveat

**Default for entry mini-run**: option (1) Free Colab T4. Fall back to (2) RunPod T4 if Colab session reset bites.

## §6 Honest C3 (mirrored from spec §10)

8 caveats listed in spec doc:

1. Distillation gap is known and irreducible (Hinton/DistilBERT show student < teacher always)
2. 350M student < 7B teacher capacity — 5% compression is OUTSIDE well-studied DistilBERT regime (~67M/110M = 60%)
3. English bias (Mistral ~90% EN; CLM SFT corpus mixed KO/EN)
4. Vocab tokenization claim unverified locally (Phase-2 pre-flight MUST dump tokenizer hashes)
5. Cache freshness invariant identical to sister Φ★ runbook §C3
6. T4 nf4 quantization shifts logits (Top-K ordering robust; tail-mass dark knowledge flattens)
7. F-D-1 0.5 nats threshold anchored to BERT-class results (not Mistral-7B-Instruct → 350M directly)
8. No biology, no consciousness claim (inherits VERIFIED-ALM-ALPHA-COGNITIVE-ONLY ship verdict)

## §7 Next gates (NOT executed by this cycle — separate BG)

| Gate | Trigger | Owner |
|------|---------|-------|
| Cache search §5.2 (6 locations) | post-spec-land | separate BG |
| Tokenizer alignment §4.5 | post-cache-search | separate BG |
| Mini-run launch | gate above PASS + EXEC authorization | separate BG (Colab or RunPod T4) |
| F-D-1 measurement | post-mini-run | separate BG |
| Production trigger | F-D-1 PASS ∧ D-D-1 PASS ∧ D-D-2 PASS ∧ D-D-3 PASS | separate BG |

This cycle is **doc-only** per raw#9 + user constraint "Do NOT launch distill execution".

## §8 raw 준수

- **raw#9**: NO .py emission this cycle. Spec is doc-only Markdown.
- **raw#10**: 8 honest C3 caveats listed in spec §10 (≥5 required per raw#91).
- **raw#15**: SSOT = `docs/p9_paradigm_d_distill_spec_2026_05_03.md`. Sister docs (Φ★ axis) cross-linked but not duplicated.
- **$0 design only**: spec recommends $0 Colab T4 path as default; cash paths secondary.

## §9 SSOT pointers

- Spec: `docs/p9_paradigm_d_distill_spec_2026_05_03.md`
- Roadmap entry: `.roadmap.p9_sft` line 4 (id `p9_sft.cond.paradigm_d_distill`)
- Markers: `state/markers/p9_paradigm_d_{spec_landed,roadmap_registered}.marker`
- Sister Φ★-axis docs (READ-ONLY context):
  - `docs/p9_paradigm_d_phi_distillation_2026_05_03.md`
  - `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md`
  - `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md`
- Architecture / baseline: `state/p9_sft_spec_2026_05_02/architecture.json`
- Holdout-500 (F-D-1 measurement target): `state/p9_p0_measure_2026_05_03/sft_data_holdout_500_augmented*`
- Teacher backbone source: `tool/anima_phi_v3_canonical.hexa` line 67

---

*End handoff. Doc-only land per raw#9. Mini-run launch deferred to separate BG cycle with cache pre-flight.*
