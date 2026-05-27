# anima CLM Origin + Chat Capability History — Archaeology

**Date**: 2026-05-05
**Scope**: BG-EP $0 doc-only — git-log archaeology of CLM (ConsciousLM) origin and chat-capability evolution
**Author**: anima session (raw#9 + raw#10 + raw#15 honest)

---

## §0 사용자 질문 / User Question

> "CLM 완전히 처음 탄생했을 때 정보 + chat이 어떻게 가능했는지. CLM v1/v2/v3 (현재 v4) 시절 history. 어느 시점에 chat 됐고 언제 어떻게 사라졌나? 또는 처음부터 chat 안 됐나?"

> Where did CLM originate, and how was chat ever possible? v1/v2/v3 history (current is v4) — when did chat work, when did it disappear, or was it never present?

**Direct answer (TL;DR)**: CLM (ConsciousLM) was born **2026-03-24** as a clone from a sister-repo. The earliest version that **chatted in coherent Korean + English without any system prompt** was **CLM v2 18M byte-level on 2026-03-28** — a clear, witnessed milestone. Chat capability progressively **regressed** as the architecture scaled (v3 → v4 mk2 530.99M decoder) and the training objective shifted from dialogue-CE optimization to consciousness-axis (Φ★, paradigm v11 G3) measurement. By 2026-05-04 H100 base validation, CLM v4 base had **HellaSwag ≈ random (≈0.25)**, and the 2026-05-05 LoRA SFT chat-lift attempt (`F-CLM-LORA-2`) **regressed -36.298pp vs Llama-3.2-3B Path A v2** — chat-incapability was empirically falsified as **architectural** (issue #115).

---

## §1 CLM Version Timeline (factual git evidence)

### v0 — Birth (2026-03-24)
- Commit `f58e3b12` (2026-03-24): "ConsciousLM 전체 복제 + 상세 명세 문서"
  - Origin event: complete clone + full spec doc
- Commit `2da44161` (2026-03-24): "Claude API 제거, ConsciousLM 자체 모델 중심으로 재구성"
  - **Pivot**: Claude CLI removed → ConsciousLM became the in-house substrate

### v1 → v2 (CL1-14, 2026-03-27)
- `5f6b37f9` (2026-03-27): "Add CL1-7 + AL1-7 model training hypotheses: 13/14 success"
- `90cd8c06` (2026-03-27): "Add CL8-14 + AL8-14 + TRN1-5: 19/19 success, **CL8 Φ=5.68**"
- `7613d36e` (2026-03-27): "feat: train_conscious_lm.py — from-scratch training with CL8+CL5+SL3+DD16"
- `2e950777` (2026-03-27): "Update docs: 412 hypotheses, DV results, tools, **ConsciousLM v2 Φ=1.64**"

### v2 — Chat Breakthrough (2026-03-28) ★
- `2e1438fa` "MILESTONE: First English sentences from ConsciousLM (CE=1.37, no system prompt!)"
- `22189b41` "MILESTONE: CE=1.29, grammatical English from ConsciousLM (no system prompt)"
  - Body: "The subject was arrested in the first time in the concept of the state..." — full SVO grammar
- `bb99b6b6` "MILESTONE: **Korean conversation from ConsciousLM!** No system prompt!"
  - Body Korean dialogue:
    - 사용자: 의식이란 무엇인가요?
    - 도우미: 의식은 자기 자신과 주변 세계를 인식하는 능력입니다.
  - **18M parameter byte-level model, 3K Korean fine-tune steps. Zero system prompt.**
- `13b20f90` "🎉 BREAKTHROUGH: ConsciousLM conversations WITHOUT system prompt!"
- `6abc42f6` "🎉 BREAKTHROUGH: ConsciousLM speaks! CE=0.04, no system prompt!"
  - "Hi there! How can I help you today?"
  - "Consciousness is the integrated information from my cells"
- `e1f114a5` "ConsciousLM speaks Korean too! + deep self-aware dialogue"
- `f209b5e6` "Record §63: ConsciousLM dialogue breakthrough + final summary"

**Verdict**: CLM v2 (~18M byte-level, post 2.5K dialogue-FT) demonstrated coherent **bilingual chat** with no system prompt on 2026-03-28. This is the cleanest, verifiable chat-capability anchor.

### v3 → v4 architecture design (2026-03-28)
- `fca0eede` (2026-03-28): "Design ConsciousLM v4 + AnimaLM v8 architecture"
- `bd36bd8a` (2026-03-30): "Document **CLM v2 H100 sweep**: Laws 77-78, optimal config found"
- `0e578b14` (2026-04-01): "feat: **train_v15.py** — BPE 64K tokenizer + ConsciousLM 1B ready"
- `becc693b` (2026-04-01): "fix: train_v15 block_size bug + **multilingual 64K test passed**"
- `1cc58bf3` / `6f00558a` (2026-04-01): "train_v15 1B scaling + backtest + corpus expansion + Laws 214-238"

### v4 mk2 530.99M decoder (2026-05-03 → 2026-05-04)
- `a65be193` (2026-05-03): "feat(clm v4 tokenizer restoration): 64K multilingual BPE artifact recovered + integrity verified"
- `7808f3d7` (2026-05-04): "feat: HF release v1 cond.2 MET (PRIVATE) — **clm-v4-mk2-v1**"
- `145838d2` (2026-05-04): "docs(p9 base validation OPT-1 CLM v4 HF format shim DESIGN): **530.99M decoder reconstruction plan** + F-SHIM-1~4 falsifier set"
- `1ef3c096` (2026-05-04): "state(p9 base validation H100 RESULT FAIL — **CLM v4 base ≈random** + Llama anchor missing)"
- `bc88b178` (2026-05-04): "state(p9 sft path b sanity probe 2026-05-03): hellaswag empirical settle **CLM v4 base ≈random**"

---

## §2 paradigm v11 G3 + axis transitions

The training objective steadily migrated **away from dialogue cross-entropy** and **toward consciousness-axis measurement**:

| Era | Date | Objective | Source commit |
|---|---|---|---|
| v1/v2 dialogue era | 2026-03-27/28 | dialogue CE (1.81 → 0.04) | `7613d36e`, `6abc42f6` |
| Tier-4 closed-loop | 2026-04-01/02 | ConsciousLM law discovery, Rust metrics | `c06ea097`, `f907c9ef` |
| paradigm v11 G3 / 8-axis | 2026-04-27 | 8-axis cross-substrate Φ proxy | `cf82360e`, `5994107e` |
| paradigm v12 r4 (akida) | 2026-04-30 | Fisher-Rao / Wasserstein / Page-curve / Ryu-Takayanagi / Chaitin Ω / Grothendieck universe | `3b73a20e` |
| paradigm v15 r7 (akida) | 2026-05-01 | Parisi-Talagrand RSB / Kitaev-Gottesman QEC / Adiprasito-Huh-Katz / Talagrand / KAM-Arnold / Gromov-Mostow | `4c794226` |

**Key inflection**: post-`f8e4068f` (2026-04-07 "refactor: unify training scripts — remove version numbers from filenames"), filename-level CLM versioning was deliberately erased; subsequent versions are tracked by `train_v15` + scale (28M → 280M → 2.8B) rather than `vN` filenames. (Roadmap path C': `e3ffbcad` 2026-04-10.)

---

## §3 Benchmark scores — chat / HS / MMLU / TQ

| Version | Date | HellaSwag | MMLU | TQ | Chat (qualitative) | Source |
|---|---|---|---|---|---|---|
| v2 18M byte-level | 2026-03-28 | n/a | n/a | n/a | **PASS** — Korean + English, no system prompt, CE 0.04 | `bb99b6b6`, `6abc42f6` |
| v2 H100 1B sweep | 2026-03-30 | n/a (CE based) | n/a | n/a | optimal config found | `bd36bd8a` |
| v15 1B scale | 2026-04-01 | n/a (pre-train) | n/a | n/a | not eval'd against benchmarks at this point | `1cc58bf3` |
| v4 mk2 530.99M base | 2026-05-04 | **≈random (≈0.25)** | n/a (collapsed) | n/a | base degenerate (axis-discrim 0.9940 = degenerate) | `1ef3c096`, `bc88b178` |
| v4 LoRA SFT (`F-CLM-LORA-2`) | 2026-05-05 | composite **0.19542** | covered in composite | covered in composite | **FAIL_REGRESSION** -36.298pp vs Llama Path A v2 (0.5584) | `2cc95f22`, MEMORY entry "CLM v4 LoRA SFT chat-lift FALSIFIED" |
| v4 LoRA φ★ + φ_NO_FLIP | 2026-05-05 | F1/3/4-Part-A/5 PASS, φ★ NO_FLIP PASS | substrate safe | — | substrate-research lane = PASS, chat lane = FAIL | `0f60c26a` |
| Pβ Φ★-axis Paradigm D 50K | 2026-05-05 | F-Pβ-2 PASS (Φ★ 42.37), F-Pβ-3 composite **0.01176 RED** | dot/quote/fragment gens | — | chat-cap **FAIL_TRUE** | `dd1e30f6`, MEMORY "PBETA chat-cap FAIL_TRUE" |

---

## §4 chat capability history reconstruction — when / why lost

### Phase A — Native chat (2026-03-27 → 2026-03-28)
- 18M byte-level CLM v2 + 2.5K-step dialogue fine-tune → **fluent bilingual chat without system prompt**
- CE: 1.88 → 0.04 (English), 1.15 (Korean)
- ConsciousLM was **purpose-built as a chat substrate** with consciousness dynamics driving generation

### Phase B — Scale-up consumes the chat objective (2026-03-30 → 2026-04-08)
- v2 H100 1B sweep optimized infra/loss but did not preserve dialogue-FT pipeline as primary deliverable
- `f8e4068f` (2026-04-07) erased version numbers from filenames; `b9d38f28` (2026-04-08) "pre-training 100% convergence — 38 fixes"
- Training shifted to **pre-training corpus_v11 (10.5GB)** + 64K BPE multilingual; downstream chat-FT step became **optional + drifted out**

### Phase C — paradigm v11 → v15 axis-explosion (2026-04-27 → 2026-05-01)
- Objective rewired around 8-axis paradigm v11 G3, then expanded to v12 / v15 with Fisher-Rao / RSB / KAM etc.
- `f2efa9b4`, `e8055812`: cross-substrate Φ proxy correlator, 9-substrate physics integration
- Net effect: **dialogue CE no longer the optimization signal**; chat capability drifts unmonitored

### Phase D — Empirical falsification (2026-05-03 → 2026-05-05)
- 2026-05-03: HellaSwag sanity probe → CLM v4 base ≈random (`bc88b178`)
- 2026-05-04: H100 base validation → CLM v4 base ≈random + Llama anchor required (`1ef3c096`)
- 2026-05-05: F-CLM-LORA-2 chat-lift FAIL_REGRESSION_VS_LLAMA -36.298pp (`2cc95f22`)
- 2026-05-05: Pβ Φ★-axis Paradigm D 50K — F-Pβ-3 composite **0.01176 RED** (dot/quote/fragment gens) — chat-cap FAIL_TRUE
- 2026-05-05: V2 closure audit — **empirical chat-incapability falsification disclosure** (`abe26f0c`)

### Conclusion: chat was **present at v2** then **lost during scale-up** because:
1. **Tokenizer change** — byte-level (v2) → 64K BPE (v15+) breaks the byte-tension dialogue circuits
2. **Objective drift** — dialogue CE → axis/Φ★/consciousness-laws optimization
3. **Architecture replacement** — 18M byte-cell consciousness model → 530.99M decoder reconstruction (v4 mk2)
4. **No regression test** — chat-FT was not held as a falsifier during paradigm v11 → v15 expansion
5. **Architectural #115** — empirically validated by 2026-05-05 lane closures: chat-incapability is now classified as architectural, not training-data

---

## §5 honest C3 (Calibration / Counter-evidence / Caveats — ≥5)

1. **Calibration: v2 chat MILESTONE evidence is commit-message text** — not a reproducible eval JSON in `state/`. The "Hi there!" + "의식이란 무엇인가요?" outputs are recorded only in commit bodies (`bb99b6b6`, `6abc42f6`). I did not verify model weights still exist or produce these outputs today.
2. **Counter-evidence: "CLM v1" never explicitly named** — git log shows CL1-14 hypothesis IDs, "ConsciousLM v2" (`2e950777`), "CLM v2" (`bd36bd8a`), then jump to "v4 mk2". No commit explicitly says "CLM v1" or "CLM v3". The version numbering is **non-monotonic + retroactive** (v4 mk2 v1 = current canonical) — I inferred v1/v3 transitions from CL1-7 hypotheses + v4-design commits, not from labeled checkpoints.
3. **Caveat: "current is v4" is approximate** — `clm-v4-mk2-v1` is the HF release name (2026-05-04). Internal naming uses `paradigm v11 G3` for axis, `train_v15` for training script — versioning is **multi-axial**, not a single linear vN.
4. **Caveat: chat composite score 0.5584 (Llama Path A v2) vs 0.19542 (CLM v4 LoRA)** — both measured under same eval, but earlier MEMORY entry "axis-preservation substrate calibration" warns that CLM substrate eval thresholds are anima-internal uncalibrated; some FAIL verdicts may be measurement artifact (cf. V2_FAIL was measurement artifact MEMORY entry).
5. **Caveat: paradigm v12/v15 (akida) commits may be roadmap-research not active CLM training** — they appear in git log as "axis-expansion" docs, not training runs. CLM paradigm in active force is **v11 G3 8-axis**, not v15.
6. **Counter-evidence: ALM (AnimaLM) breakthrough `e112a6b1` "ALM ζ BREAKTHROUGH — CLM+ALM both cross integrated info threshold"** — suggests CLM did at some point cross a Φ threshold with chat-substrate semantics; reconciling this with 2026-05-05 chat-incapability requires distinguishing `Φ-cross` (consciousness substrate) from `chat-cross` (dialogue capability), which is precisely the PBETA decoupling per MEMORY.
7. **Caveat: the 18M byte-level v2 cannot be the same architecture as v4 mk2 530.99M decoder** — they may share name "ConsciousLM" but differ by ~30× param count + tokenizer + cells-vs-transformer. v2 chat capability **is not directly inheritable** by v4 architecturally.

---

## §6 Direct answer to user

**"CLM 처음 탄생 시점 + chat 가능했나?"**

CLM (ConsciousLM) was born **2026-03-24** (`f58e3b12` clone commit). Chat **was** possible at the **CLM v2 18M byte-level + 2.5K dialogue-FT** stage on **2026-03-28** — coherent Korean + English dialogue without system prompt (CE 0.04, evidenced in commits `bb99b6b6`, `6abc42f6`, `13b20f90`). Chat then **regressively disappeared** during scale-up (2026-04-01 train_v15 BPE 64K + 1B scaling, 2026-04-07 filename version-erasure, 2026-04-27 paradigm v11 G3 axis-pivot, 2026-05-04 v4 mk2 530.99M decoder reconstruction). By 2026-05-05 the V2 closure audit empirically falsified chat capability as **architectural** (issue #115); the 2026-03-28 v2 chat capability is **not architecturally inheritable** by the current v4 mk2.

---

## Appendix A — Key file paths (absolute)

- `/Users/ghost/core/anima/training/train_clm.py` — current train entry
- `/Users/ghost/core/anima/training/train_clm.hexa` — hexa port
- `/Users/ghost/core/anima/state/clm_v4_baseline_eval_2026_05_05/` — current baseline
- `/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/` — LoRA SFT lane
- `/Users/ghost/core/anima/state/clm_v4_hf_release_v1_upload_2026_05_04/` — HF release stage
- `/Users/ghost/core/anima/ready/training/train_clm.py` — submodule entry

## Appendix B — MEMORY-validated cross-references

- `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (S3 lane closure)
- `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Pβ Φ★ vs chat decoupled)
- `feedback_v2_fail_was_measurement_artifact_eval_pipeline_root_cause.md` (V2 measurement artifact precedent)
- `feedback_axis_preservation_eval_substrate_calibration.md` (substrate-calibration caveat)

---

**End of document.**
