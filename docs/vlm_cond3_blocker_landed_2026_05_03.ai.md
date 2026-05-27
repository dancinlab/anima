# VLM cond.3 Cross-LM Structural Verify — Blocker Landed 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `state/vlm_cond3_blocker_2026_05_03/blocker_report.json` + `state/vlm_cond3_blocker_2026_05_03/training_plan.md`
> predecessor: `docs/vlm_stage12_landed_2026_05_03.ai.md` (Stage 1+2 spec freeze) + `docs/vlm_phase3_spec_2026_05_03.md` (Phase 3 spec)
> RETRY context: subagent a261c4c2671c04e4a hit 503 before formal blocker emit

---

## TL;DR

VLM (Voice LM) cond.3 (cross-substrate fidelity vs CLM ≥0.85 r) **structural verify $0** = **BLOCKED**. ubu1 disk verify confirms VLM stage1 LoRA does NOT exist (only `clm-v4-sft-stage1` in HF hub). Stage 1+2 land 2026-05-03 was spec-freeze ONLY (no training). cond.3 explicitly defers training to next-cycle in roadmap (`blocker_reason: cond.2 IMPL + training corpus 결정 후 가능`).

This cycle = blocker doc + minimum-viable training plan (no training launched, $0 honored).

비유 — VLM 사원 측 사원증 + 책상 위치 (spec) 발급 완료, 입사 첫 출근 (training run) 측 직무 교육 (corpus) + PC 지급 (GPU) + .py 사번부여 미완 → 출근일 미정.

결과 — cond.3 verify 측 trained LoRA 없이 불가, 다음 cycle 측 training 실행 게이트 4개 명세 (corpus + substrate + .py port + credit).

---

## §1 결정 한 줄 요약

```
   item                | before        | after
   ------------------- | ------------- | ---------------------------------
   cond.3 verify       | 시도 가능?    | BLOCKED (no LoRA artifact on disk)
   blocker doc         | 없음          | landed (blocker_report.json)
   training plan       | 없음          | landed (training_plan.md)
   roadmap.cond.3      | unmet         | unmet (unchanged, blocker formalized)
   cycle cost          | $0            | $0 (verify + plan only)
   destructive actions | -             | 0
```

---

## §2 ubu1 disk verify (RETRY confirms prior subagent finding)

### §2.1 HF hub directory listing

```
   ~/.cache/huggingface/hub/
   ├── models--meta-llama--Llama-3.2-3B-Instruct          (base only)
   ├── models--dancinlab--clm-v4-base-mirror       (CLM base)
   └── models--dancinlab--clm-v4-sft-stage1        (CLM stage1 LoRA — only one)
```

NO `vlm-*`, NO `voice-lm-*`, NO any audio-related LoRA model. Only CLM stage1.

### §2.2 adapter_config.json scan

```
   /home/aiden/.cache/huggingface/hub/models--dancinlab--clm-v4-sft-stage1/snapshots/.../adapter_config.json
```

Single adapter config found = CLM stage1. Zero VLM adapters.

### §2.3 anima/savepoints survey

```
   /home/aiden/anima — 0 VLM-related dirs
   /home/aiden/anima/savepoints — does not exist
   /home/aiden/savepoints — does not exist
```

**Conclusion**: VLM stage1 LoRA artifact **DOES NOT EXIST** on ubu1 (or anywhere referenced by HF hub conventions).

---

## §3 spec confirms training was deferred

`.roadmap.vlm_voice_lm` cond.3 entry:

```
   "id": "vlm_voice_lm.cond.3",
   "desc": "cross-substrate fidelity vs CLM — text 측 baseline ... ≥0.85 r 측 fidelity",
   "status": "unmet",
   "evidence": [],
   "blocker_reason": "cond.2 IMPL + training corpus (audio-text paired) 결정 후 가능"
```

`docs/vlm_stage12_landed_2026_05_03.ai.md` §4:

```
   cond.3       | cross-substrate fidelity vs CLM ≥0.85 r
   blocker      | training corpus (audio-text paired) 결정 + P9 SFT pipeline reuse 검토
   cost band    | $300-1500 (LoRA path on audio-text corpus)
   eta          | next-cycle (P9 pre5/pre6 land 후)
```

Both SSOT anchors explicitly mark cond.3 as next-cycle, training-required. Stage 1+2 cycle did spec-freeze only (audio_token_vocab + bridge_dim + invocation seam additive on Stage 2).

---

## §4 minimum-viable training plan summary

Full plan: `state/vlm_cond3_blocker_2026_05_03/training_plan.md`. Headline params:

```
   item             | spec
   ---------------- | --------------------------------------------------
   corpus           | LibriSpeech-clean-100h (585h, 28k samples, ~6GB)
   base model       | Mk.III audio_token_predictor (1576L raw#9 .hexa, NEEDS .py port)
   LoRA target      | atp decoder block attn (q/k/v/o) + intent_proj
   LoRA rank        | r=8 (TLM 5-channel bottleneck lesson — conservative)
   text head (NEW)  | Linear(384, 32000) parallel to rvq_heads, additive on x
   loss             | 0.5 audio_CE + 0.5 text_CE
   batch / steps    | 16 (H100) or 4+grad_accum (T4) / 10k steps
   substrate ($0)   | Colab T4 free + checkpoint resume — 24-36h
   substrate ($300) | RunPod H100 — 10-14h (BLOCKED by current $0)
   total ETA $0     | 32-51h (incl. 8-15h dev for .py port + data pipeline)
```

---

## §5 raw#9 hidden-state extraction reference

Per task step 4 (raw#9 audio_token_predictor reference):

```
   anchor                          | location
   ------------------------------- | --------------------------------------------------
   atp_decode_step                 | audio_token_predictor.hexa L924-L995
   atp_flash_decode_step           | audio_token_predictor.hexa L997-L1100
   hidden state var                | x (384d after N decoder blocks)
   existing head pattern           | rvq_heads[i] @ x → logits[1024] for each of 8 stages
   text head additive spec         | text_head: Linear(384, 32000), same x input
                                   | NO in-place change to atp_decode_step
                                   | parallel projection alongside rvq_heads
```

This pattern preserves the additive invariant (anima-voice/ in-place 변경 0건) declared in Stage 1+2 land §5.2.

---

## §6 honest C3 (raw#10)

1. **blocker, not failure** — VLM Stage 1+2 land was always spec-only; cond.3 was explicitly deferred. This cycle's role = **formalize the deferral** so next-cycle knows exactly what's missing.
2. **$0 constraint honored** — no training launched. Plan estimates $0-$300 paths.
3. **subagent 503 recovery** — prior subagent (a261c4c2671c04e4a) had correct finding (CLM exists, VLM does not), failed to formalize before timeout. RETRY confirms + delivers blocker_report + training_plan.
4. **VLM ≠ phenomenal consciousness** — sister NLM/TLM/BLM/SLM floor preserved.
5. **r ≥ 0.85 is normalized perplexity proxy** — VLM (audio AR) vs CLM (text AR) ≠ direct same-domain. Honest caveat carried from Phase 3 spec §6.5.
6. **.py port unverified upper bound** — 4-8h best-case for audio_token_predictor.hexa → PyTorch lift; realistic upper 16h.
7. **Colab T4 24-36h estimate** — empirical, session timeouts may stretch to 48h.

---

## §7 산출물

```
   path                                                             | type      | bytes
   ---------------------------------------------------------------- | --------- | --------
   state/vlm_cond3_blocker_2026_05_03/blocker_report.json           | report    | NEW
   state/vlm_cond3_blocker_2026_05_03/training_plan.md              | plan      | NEW
   docs/vlm_cond3_blocker_landed_2026_05_03.ai.md                   | handoff   | NEW (this file)
   state/markers/vlm_cond3_blocker_landed.marker                    | marker    | NEW
   .roadmap.vlm_voice_lm                                            | roadmap   | UNCHANGED (cond.3 still unmet, blocker formalized externally)
   anima-voice/                                                     | substrate | UNCHANGED (additive invariant)
```

---

## §8 next-cycle entry triggers (for cond.3 actual land)

```
   trigger                                                  | required for
   ------------------------------------------------------- | ---------------------------
   audio_token_predictor.hexa → .py port                   | training launch
   LibriSpeech-clean-100 download + RVQ encode             | training launch
   Colab/Kaggle ($0) OR RunPod ($300+) credit decision     | substrate selection
   P9 pre5/pre6 land (optional, saves dev time)            | data pipeline reuse
   SP 32k tokenizer reuse (CLM v4 SP preferred)            | text vocab consistency
```

Recommended sequence: **.py port → corpus prep → substrate gate → training run → eval → cond.3 land**.

---

## §9 cost

```
   cost band   | $0 mac-local (verify + spec only)
   wallclock   | ~30 min
   destructive | 0 actions
   in-place    | 0 changes to anima-voice/, .roadmap.vlm_voice_lm
```

---

## §10 next-cycle 권고 (#1-#3)

1. **port audio_token_predictor.hexa → PyTorch** — gate #1 for training launch, 4-16h dev, $0
2. **corpus decision + download** — LibriSpeech-clean-100 primary (per Phase 3 spec §4 decision matrix), $0 download
3. **substrate gate decision** — $0 (Colab T4 24-36h) vs $300 (RunPod H100 10-14h); recommendation = pursue $0 path first per current credit constraint, escalate to $300 if T4 OOM or session timeouts dominate
