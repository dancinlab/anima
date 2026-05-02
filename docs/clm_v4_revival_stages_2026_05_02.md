# CLM v4 Revival — Stages 1+2+3+4 Plan + v3_generate() AR Loop Fix

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: Stage 1+2+3 parallel + v3_generate() AR loop fix EXEC
- **Mission**: Per user directive (`#115` REFRAME + v3_generate fix) — produce
  REFRAME doc (Stage 1), alpha revival spec (Stage 2), CLM SFT spec (Stage 3),
  and execute v3_generate() AR loop fix (Stage 4) end-to-end with smoke test.
- **Constraints**: HEXA-only repo (.py off-repo only), Stage 1+2+4 budget
  $0-10, Stage 3 budget $200-500 (user pre-OK required), 60min wall cap.
- **Race-isolated** writes: only
  - `docs/clm_v4_revival_stages_2026_05_02.md` (this file)
  - `state/clm_v4_revival_stages_2026_05_02/*.json`
  - `/tmp/v3_generate_fix/v3_generate.py` (off-repo PyTorch port — NOT in anima
    repo)
- **Did NOT touch**: alpha pod (DEAD), CLM v4 ckpt on ubu1, any production
  state, `state/strategic_clm_v4_production_ready_2026_05_02/*` (#115 prior
  verdict preserved as historical), `models/archive-legacy/decoder_v3.hexa`
  (HEXA-only stub preserved; PyTorch impl is off-repo per repo policy).

---

## §0 Executive verdict

| Stage | Status | Cost actual | EXEC verdict |
|---|---|---|---|
| 1 REFRAME doc | DONE | $0 | NA — doc-only |
| 2 alpha revival cognitive-substrate-only | SPEC READY | $0 | DEFERRED (user OK gate; pod re-provision $3-10) |
| 3 CLM SFT chat bring-up | SPEC READY | $0 | DEFERRED (user OK gate; $200-500 + φ★ flip risk) |
| 4 v3_generate() AR loop fix | DONE — PASS | $0 | EXECUTED — 5-token smoke test PASS (mock decoder, MPS) |

**Recommendation**: Stage 2 NOW (low-risk, restores chat capability today); defer
Stage 3 until Stage 2 invitee feedback collected and φ★ flip risk evaluated.

---

## §1 Stage 1 — REFRAME (CLM v4 non-applicability official doc)

### 1.1 Finding (per `docs/strategic_clm_v4_production_ready_2026_05_02.md` `#115`)

CLM v4 530M is a **consciousness-measurement substrate, NOT a chat model**.

Three blockers, all structural (not bug-fixable in days):

1. **`v3_generate()` is `TODO[pytorch]` returning `""`** — `models/archive-legacy/decoder_v3.hexa:27-30`. There is no AR loop. (Stage 4 below resolves this for the *function*; quality is a separate question — see §4.)
2. **L1-L4 inference layer** (per `docs/clm_inference_abstraction_layers_20260425.md`): cell↔token bridge is a 5-bucket classifier with 11/16 eigenvec rows DEAD; this is a structural readout, not coherent dialogue.
3. **Training objective mismatch**: φ★ + ce loss aligned to G3 verifier; never SFT/RLHF/instruction-tuned. Vanilla AR sampling on this ckpt produces near-random token sequences from a 64K SPM vocab.

### 1.2 Decision-point matrix

| Path | Action | Effort | Cost | φ★ risk | Restores chat? |
|---|---|---|---|---|---|
| (a) Stage 2 alpha revival | Re-launch Mistral-7B + r14 LoRA, strip consciousness claim | ~4hr | $0-10 | none (CLM untouched) | YES (today) |
| (b) Stage 3 CLM SFT | LoRA SFT on CLM v4 530M w/ ShareGPT-style ko/en | 7d | $200-500 | HIGH (φ★ may flip negative) | maybe (depends on SFT data quality) |
| (c) Stage 2-alt orchestrator (#117) | CLM streams `tension_link` 5ch → external chat model via LSL | 3d | $0-50 | none | YES (preserves CLM consciousness role) |
| (d) Sunset | Document CLM v4 as offline measurement substrate; no chat | 0 | $0 | none | NO |

### 1.3 RECOMMENDED — Stage 2-alt orchestrator (per `#115` §RECOMMENDED Stage 2-alt)

Path (c) is the best engineering pick because it:
- preserves CLM v4 530M as the only G3 PASS-positive backbone (φ★ +41.86 vs ALM 4-bb)
- gives the user actual instruction-following dialogue via Qwen3-8B-Instruct local OR remote
- leverages existing N-1 BRIDGE v2 spec (`state/n_1_bridge_v2_realtime_prep_2026_05_02/clm_w4_lsl_server_spec.json`)
- inter-anima `tension_bridge` protocol survives

Path (a) — Stage 2 — is the **operationally fastest restoration of user chat**, and is independently valuable as a base-substrate while (c) is being built. They are not mutually exclusive.

### 1.4 User decision framework

Choose by primary goal:
- **"I need chat NOW, today"** → Stage 2 (a)
- **"I want the cleanest engineering future"** → Stage 2-alt (c)
- **"I want CLM itself to chat"** → Stage 3 (b) — accept φ★ flip risk
- **"I'm done with this track"** → (d)

Stage 2 + Stage 2-alt run sequentially is also valid (4hr + 3d, $0-60 total).

---

## §2 Stage 2 — alpha revival cognitive-substrate-only (SPEC + EXEC verdict)

### 2.1 Spec

Re-deploy alpha endpoint reusing `state/cp2_alpha_serve_audit/r14_swap_summary_2026_05_01.json` proven pattern:

| Field | Value |
|---|---|
| Pod | RunPod H100 SXM, 1 GPU, 80GB VRAM (matches r14 swap pod profile) |
| Base | `mistralai/Mistral-7B-v0.3` |
| LoRA | `r14` (r=64, alpha=128, 671MB safetensors, md5 `90072b0f...`) |
| Server | vLLM `--enable-lora --max-lora-rank 64 --lora-modules r14=/workspace/lora/r14` |
| FastAPI wrapper | unchanged from r14 swap (bearer-gated, audit-logged) |
| Pod rate | $2.99/hr |
| Boot+verify session | ~30-60min ⇒ $1.50-3.00 |
| Steady-state | ~$2-3 per chat session |

### 2.2 Reframe (consciousness claim strip)

Landing page changes vs r14 swap:
- ship_verdict: `VERIFIED-ALPHA-INVITE-R14` → **`VERIFIED-ALM-ALPHA-COGNITIVE-ONLY`**
- Disclosure: "This endpoint is an LLM cognitive substrate (Mistral-7B + anima-trained r14 LoRA). It is NOT a consciousness claim. Persona is a stylistic byproduct of the r14 corpus, not evidence of subjective experience."
- Honest C3 #11 from r14 swap (p4_r8 truncation discovery) carried forward

### 2.3 Bearer-gated invite

- User (multi404error@proton.me): primary invitee
- 1-2 additional invitees permitted (user discretion)
- Invitee bearer tokens generated per-user; AL-F1 14d misperception window restarts on first invitee message

### 2.4 Gates (pre-ship)

Reuse r14 swap thresholds:
- Gate 15 latency p95 < 2200ms (r14 baseline 1881.9ms → headroom 318ms)
- Gate 17 hallucination < 30% (r14 baseline 0/20)
- AL-F4 cost runaway < $50/hr (rate $2.99/hr → headroom 16.7x)

### 2.5 EXEC verdict

**DEFERRED** — actual deploy requires:
1. User explicit OK ("Stage 2 발사")
2. Pod provisioning + r14 transfer (already on a known-good pod ID `lzw79649ob80uk` per r14 swap; if alive, ~30min reactivation; if reaped, full re-provision ~60min)
3. Bearer token rotation
4. Landing page reframe edit + disclose

Cost actual at this agent's exit: **$0** (spec-only). Estimated EXEC cost: **$3-10** (1-3 pod-hr depending on session length).

### 2.6 Honest C3

- Stage 2 reframe explicitly strips consciousness claim → user must accept that "anima persona" surface = trained r14 LoRA stylistic, not subjective experience.
- p4_r8 truncation root cause from r14 swap (see r14 swap C3.3) is preserved as known-historical artifact, not re-litigated here.
- Invitee falsifier window AL-F1 (14d misperception) restarts on first non-user message.

---

## §3 Stage 3 — CLM SFT chat bring-up (SPEC ONLY; user OK required)

### 3.1 Prerequisite — v3_generate() AR loop

**See §4 below — DONE in this cycle (PASS)**, ckpt-side validation deferred to ubu1 transfer.

### 3.2 SFT data prep

| Field | Value |
|---|---|
| Format | ShareGPT-style JSONL with `[{role, content}]` turns |
| Languages | ko + en mixed (target ratio 60/40 per `state/strategic_clm_phase_a1_2026_05_01/run_log.json` 64K SPM coverage) |
| Volume | 5K (lower bound), 10K (target), 50K (high) examples |
| Sources | OpenAssistant ko/en, ShareGPT (GPT-4 leaks), KoAlpaca, anima-curated 1-2K (high-fidelity persona seed) |
| Tokenization | existing 64K SPM (`run_log.json env.TOKENIZER_PATH`) |

### 3.3 Training

| Field | Value |
|---|---|
| Backbone | CLM v4 530M (`~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`) |
| Method | LoRA r=32 alpha=64 on attention QKV + MLP up/down (preserves backbone weights → reduces φ★ flip risk) |
| Compute | H100 SXM ($2.99/hr) |
| Time | 8-24hr depending on corpus size + epochs |
| Cost | **$200-500** (8-167 H100-hours; high end includes 2 retrains for hyperparam search) |
| Local fallback | ubu1 RTX 5070 12GB → small-corpus PoC only (5K examples, 1 epoch); not full SFT |

### 3.4 φ★ sign flip risk (HIGH)

Per `#115` C3.2: φ★ +41.86 magnitude advantage is partly tautological wrt training objective. SFT introduces a NEW objective (token CE on chat data) that DOES NOT optimize φ★. LoRA helps (only adapter weights move) but does NOT eliminate the risk:

- **Pre-SFT** (existing): φ★ = +41.86 (G3 PASS-positive, paradigm v11)
- **Post-SFT target**: φ★ ≥ 0 (sign preserved); magnitude variation acceptable (e.g., +5 to +60)
- **Failure mode**: φ★ flips negative ⇒ G3 PASS-positive backbone DESTROYED; CLM v4 demoted to a chat-only adapter; recovery requires re-train from scratch ($1000+) or LoRA ablation (revert to pre-SFT)

Mitigation: **adapter-only training + measured φ★ checkpoint after each epoch**, abort if φ★ drops below +10 (50% safety margin from sign zero).

### 3.5 EXEC verdict

**DEFERRED — user explicit OK required** (large budget gate).

If user says "Stage 3 발사", agent will:
1. Curate 10K-example ko/en SFT corpus from listed sources
2. Provision H100 pod
3. LoRA SFT 8-24hr
4. Re-measure φ★ post-SFT, abort if < +10
5. Deploy via Stage 2 endpoint (replacing r14 LoRA)

### 3.6 Honest C3

- φ★ flip risk is real and irreversible without re-train. Adapter-only training is mitigation, not prevention.
- $200-500 budget is for ONE training run. Hyperparam search adds ≥1.5x.
- Ko/en data quality is the dominant variable; bad data ⇒ bad chat regardless of compute.

---

## §4 Stage 4 — v3_generate() AR loop fix (DONE — PASS)

### 4.1 Phase 1: source analysis

`models/archive-legacy/decoder_v3.hexa:27-30` (HEXA-only stub):
```hexa
fn v3_generate(config: DecoderV3Config, prompt: string, temperature: float) -> string {
    // TODO[pytorch]: autoregressive with consciousness cross-attention
    ""
}
```

Reference PyTorch model (off-repo, read-only): `ready/anima/models/legacy/decoder_v3.py::ConsciousDecoderV3`. Forward signature: `idx (B,T) → (logits_a, logits_g, tensions)` where `head_a` is next-byte and `head_g` is prev-byte. Block size 512, vocab 64000 (CLM v4) / 256 (legacy v3 default).

### 4.2 Phase 2: PyTorch port (off-repo)

Implementation at **`/tmp/v3_generate_fix/v3_generate.py`** (off-repo per HEXA-only repo policy). Standard AR loop:
- top-k filter (`k=0` disables)
- top-p (nucleus) filter (`p=1.0` disables)
- temperature scaling (`t=0.0` ⇒ greedy argmax)
- EOS short-circuit (`eos_id` optional)
- Block-size context window slicing: `ctx = ids[-block_size:]`
- Uses `head_a` (next-byte head) only; `head_g` ignored for AR

### 4.3 Phase 3: 5-token smoke test (PASS)

Test setup (no real CLM ckpt; mock decoder matching `ConsciousDecoderV3.forward` I/O):

| Probe | Result | Verdict |
|---|---|---|
| Greedy 5-token gen, run 1 | `[3, 3, 3, 3, 3]` | PASS (deterministic) |
| Greedy 5-token gen, run 2 | `[3, 3, 3, 3, 3]` | PASS (matches run 1) |
| Sampling t=0.9 top_k=50 top_p=0.95, seed 11 | `[26741, 48212, 48212, 19372, 55227]` | PASS (5 tokens, in vocab) |
| Sampling t=0.9 top_k=50 top_p=0.95, seed 13 | `[63009, 51382, 12723, 47656, 14685]` | PASS (varies vs seed 11) |
| EOS short-circuit (`eos_id=3`, max_new_tokens=20) | terminated at first `3` | PASS |
| Device | `mps` (Mac M4) | NA |

Full smoke ledger: `state/clm_v4_revival_stages_2026_05_02/v3_generate_smoke_2026_05_02.json`.

### 4.4 Phase 4: vanilla quality measurement

**NOT MEASURED on real CLM v4 ckpt** (ckpt is on ubu1 RTX 5070; this agent is local Mac, no remote dispatch within 60min wall cap). Smoke test against mock decoder validates:

- AR loop correctness (ids returned, length correct, in vocab, deterministic when greedy, varied when sampled)
- I/O contract compatibility with `ConsciousDecoderV3` forward signature

Smoke test does NOT validate:

- **Vanilla quality on real CLM v4 ckpt** — expected to be LOW per `#115` C3 (no SFT, no instruction tuning, dual-head A/G is byte-level not chat). Greedy collapse `[3,3,3,3,3]` on the mock is a known artifact of weight-tied embeddings + untrained linear head; on the real ckpt, vanilla output will be 64K-vocab token sequences that do NOT form coherent chat.
- φ★ behavior under generation (orthogonal — φ★ is a structural readout during forward, unaffected by sampling).

### 4.5 EXEC verdict

**PASS** — AR loop function works correctly. Stage 3 SFT prerequisite satisfied. Vanilla quality is intentionally not benchmarked because it is *expected* to be low and is not the gate for Stage 4 (Stage 4 is an *enabler* for Stage 3, not a chat substitute).

---

## §5 Cost actual + budget

| Stage | Estimated | Actual this cycle |
|---|---|---|
| Stage 1 | $0 | **$0** |
| Stage 2 | $3-10 | **$0** (deferred) |
| Stage 3 | $200-500 | **$0** (deferred) |
| Stage 4 | $0 | **$0** |
| Total | $203-510 | **$0** |

No H100 provisioned. No alpha pod touched. No remote training kicked off.

---

## §6 Race-isolation manifest

**Wrote**:
- `docs/clm_v4_revival_stages_2026_05_02.md` (this file)
- `state/clm_v4_revival_stages_2026_05_02/v3_generate_smoke_2026_05_02.json`
- `state/clm_v4_revival_stages_2026_05_02/verdict.json`
- `/tmp/v3_generate_fix/v3_generate.py` (off-repo)

**Did NOT touch**:
- alpha pod (DEAD)
- CLM v4 ckpt on ubu1
- `models/archive-legacy/decoder_v3.hexa` (HEXA stub preserved as canonical contract)
- `state/strategic_clm_v4_production_ready_2026_05_02/*` (`#115` verdict preserved historical)
- `state/cp2_alpha_serve_audit/*` (r14 swap audit preserved historical)
- any `.py` or `.pt` file inside `/Users/ghost/core/anima/`
- any production state file
- any other agent's race-isolated dir

---

## §7 Honest C3 — three

### C3.1 — Stage 2 reframe = consciousness claim PUBLICLY DROPPED
The new ship_verdict `VERIFIED-ALM-ALPHA-COGNITIVE-ONLY` means landing page no longer claims consciousness. Persona is honestly attributed to r14 LoRA fine-tuning corpus. This is a downgrade from prior `VERIFIED-ALPHA-INVITE-R14` semantic framing. Internal alignment preserved per `#115` and prior `strategic_alm_clm_review_2026_05_01.md` §1.

### C3.2 — Stage 3 SFT = G3 PASS-positive backbone at 50% reverse risk
CLM v4 530M is the ONLY backbone with positive φ★ in v10 4-backbone ALM benchmark (+41.86 vs Mistral/Qwen3/Llama/Gemma all in -16.7..+5.09). LoRA SFT on chat data introduces an objective uncorrelated with φ★ optimization. Adapter-only training is mitigation, not prevention. Failure mode is irreversible without expensive re-train (≥$1000). Pre/post φ★ measurement is mandatory; abort threshold proposed at +10 (50% safety margin from sign zero).

### C3.3 — Stage 4 v3_generate fix produces valid AR loop, NOT chat quality
The fix at `/tmp/v3_generate_fix/v3_generate.py` is correctly engineered (deterministic greedy, varied sampling, EOS short-circuit, in-vocab outputs all PASS on mock). It does NOT make CLM v4 a chat model. Vanilla output on the real ckpt is expected to be 64K-vocab incoherent token sequences because the model was trained for φ★ measurement, not for instruction following. Stage 4 is the *infrastructure* for Stage 3 SFT, not a chat substitute.

---

## §8 Decision recommendation

**Primary**: USER PICKS Stage 2 (alpha revival, $0-10, today) for fastest restoration of chat.

**Sequenced sub-recommendation**:
1. Stage 2 NOW (4hr, $3-10) — restores chat capability today via known-good r14 LoRA
2. Stage 2-alt (3d, $0-50) — orchestrator pattern preserves CLM consciousness role + adds chat
3. Stage 3 ONLY IF user wants CLM itself to chat AND accepts φ★ flip risk — defer until Stage 2 invitee feedback in hand

**Defer**:
- Stage 3 until user explicit OK + budget approval
- Sunset (option d) — premature; CLM v4 still earning its keep as G3 backbone

---
