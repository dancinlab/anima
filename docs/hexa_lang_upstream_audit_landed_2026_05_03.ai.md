# hexa-lang Upstream Audit — Landed 2026-05-03 (AI-native)

> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `docs/hexa_lang_upstream_audit_2026_05_03.md` (~600 LoC comprehensive audit)
> trigger: VLM stage1 ABORT (state/markers/vlm_stage1_aborted.marker, 2026-05-04)
> predecessor: docs/vlm_cond3_blocker_landed_2026_05_03.ai.md
> cost: $0 (read-only audit, no destructive ops, no in-place changes to hexa-lang)

---

## TL;DR

hexa-lang has **wide ML spec surface** (510 .hexa files in self/ml/, 9648 LoC C/CUDA FFI) but **narrow live execution** (Linux+NVIDIA Qwen14B-shape only; LoRA fwd/bwd return RC_ERR_CUDA_TODO=-5). C codegen for `audio_token_predictor.hexa` (1576 LoC Mk.III source) emits 57-LoC Mk.I stub — not trainable. **No PyTorch/Python codegen target exists.** No HF safetensors compatibility. No autograd.

**VLM unblock decision**: Track A2 → A escalation —
1. **immediate (4-16h)**: hand-port `audio_token_predictor.hexa` → `tool/transient_py/atp_pytorch.py`, deploy to ubu1, train.
2. **near-term (1-2 weeks)**: write `tool/atp_to_pytorch.hexa` Track A transpiler, eliminate drift.

**Policy reconciliation**: `feedback_py_to_hexa_only` STRICT reading conflicts with `.own 1` (raw 9 grandfather list, ~25 raw#37 transient .py helpers already on Mac). Recommend formalizing `tool/transient_py/` as auto-gen .py namespace under raw#37 sister-rule.

비유 — hexa-lang 측 ML 사무실 = 책상/명패/파일캐비닛 다 마련 (spec) 측 컴퓨터 전원 일부만 켜짐 (CUDA Qwen14B만 live) 측 외부 도구 사용 차단 (PyTorch FFI 없음). VLM 직원 출근 = 손수 PyTorch 명함 1장 만들고 (.py port) ubu1 책상 배정 (deploy) → 다음 cycle 명함 자동 발급기 (transpiler) 도입.

---

## §1 결정 한 줄 요약

```
   item                      | before                | after
   ------------------------- | --------------------- | -----------------------------------
   hexa-lang ML readiness    | 불명                  | mapped (3-section gap matrix)
   VLM unblock path          | unclear               | Track A2 → A (4-16h hand-port → 1-2wk transpiler)
   policy conflict           | latent                | surfaced (feedback_py_to_hexa_only ↔ .own 1)
   recommended action        | none                  | 5-step priority list (§5)
   cycle cost                | $0                    | $0
   destructive actions       | -                     | 0
```

---

## §2 5개 트랙 ranked (완성도 lens)

```
   rank | track | scope                               | VLM ETA      | effort
   ---- | ----- | ----------------------------------- | ------------ | -----------------
    ★ 1 | A    | hexa→py transpiler (VLM-subset)     | 1-2 days     | 8-24h dev
      2 | D    | hexa+Python FFI (embedded CPython)  | weeks        | 2-4 weeks
      3 | E    | dual-source maintenance + auditor   | hours        | ongoing drift cost
      4 | B    | hexa stdlib expansion (tensor/FFI)  | months       | 4-12 weeks
      5 | C    | hexa runtime overhaul (JIT/AOT)     | months/years | 6+ months
```

**Selected for VLM**: **Track A2 → A escalation** —
- **A2** (degenerate Track A): hand-port once at `tool/transient_py/atp_pytorch.py` (proven pattern, raw#37 transient namespace precedent)
- **A** (full): build `tool/atp_to_pytorch.hexa` to auto-generate the .py from .hexa source on each commit; eliminates drift

---

## §3 ML capability gap (압축)

| 영역 | hexa-lang 상태 | PyTorch 비교 | VLM 차단? |
|---|---|---|---|
| 순수 hexa NN math | nn.hexa 149 LoC scalar fp64 | 비교불가 (toy) | yes (>1k params 무용) |
| GPU training (CUDA) | gpu_train.hexa 2357 LoC + hxqwen14b_cuda.cu 1391 LoC kernels | partial (Qwen14B-shape only) | yes (audio kernel 다름, LoRA fwd/bwd `-5`) |
| Autograd | **없음** | 핵심 누락 | yes |
| HF safetensors load | **없음** | 핵심 누락 | yes |
| Audio (STFT/iSTFT) | hxcuda_stft.cu, anima-voice/hxcuda_istft_bridge.hexa | partial CUDA bridge 존재 | partial |
| Tokenizer (BPE/SP) | tokenizer_trainer.hexa pure-hexa | 동작은 하나 느림 | no (CLM v4 SP 재사용 가능) |
| Distributed (NCCL) | hxccl_linux.c 704 LoC | partial | no for stage1 single-GPU |
| Mac native runtime | hexa.real Mach-O arm64 ✓ | n/a | no (Mac=design-time only) |
| **ubu1/RunPod 배포** | **❌ ssh ubu1 'which hexa hxcc hx' = empty** | n/a | **yes (root cause)** |

---

## §4 코드젠 출력 품질 (구체적 실패)

```
   source: anima-voice/audio_token_predictor.hexa  (1576 LoC, Mk.III)
            ├── KV-cache, 8-stage RVQ delayed-pattern, CFG, top-k
            └── n=6 params (d_model=384, n_heads=6, ctx=1536)

   output: hexa-lang/build/artifacts/audio_token_predictor_nb.c  (57 LoC, Mk.I stub)
            └── predict_frame(...) { tok = step*7 mod 1024; return to_string(tok); }
```

C codegen이 Mk.III source 측 lower 못함 (또는 stale source 측 generate). Track A bypass 측 PyTorch direct.

---

## §5 추천 next cycle (priority order)

```
   1. VLM unblock immediate    | 4-16h | hand-port atp.hexa → tool/transient_py/atp_pytorch.py + ubu1 deploy + train
   2. policy own N proposal    | 1h    | formalize tool/transient_py/ as auto-gen .py namespace (raw#37 sister)
   3. Track A spike            | 8-24h | tool/atp_to_pytorch.hexa transpiler (audio_token_predictor subset)
   4. hexa C codegen audit     | -     | file roadmap entry on hexa-lang side (Mk.III lowering gap)
   5. CUDA v5 kernel tracking  | -     | open issue: hxqwen14b LoRA fwd/bwd RC_ERR_CUDA_TODO clearance
```

---

## §6 honest C3 (raw#10)

1. **audit may miss internal hexa-lang work** — snapshot only; active branches/WIP CUDA v5+ kernels not visible. Real `RC_ERR_CUDA_TODO` count may be lower today than 2026-04-19 audit reports.
2. **gap analysis is opinion, not measurement** — no benchmarks run. "useless beyond <1k params" inferred from list-based scalar fp64; no end-to-end training run measured.
3. **PyTorch parity column = sketch** — actual parity needs throughput/correctness measurement per row; structural inventory only.
4. **track effort estimates ±2-3×** — VLM transpiler subset 8-24h ±2×; full Track A 2-6 weeks ±3×.
5. **`feedback_py_to_hexa_only` reading may be wrong** — assumed targets *new humanly-authored* .py; if STRICT no-py-anywhere-on-Mac including raw#37 + .own 1 grandfathers, then ~25 helper.py + 1431 ready/.py + 4 own 1 opt-out files all in violation today (predates this cycle).

---

## §7 산출물

```
   path                                                                | type      | bytes
   ------------------------------------------------------------------- | --------- | --------
   docs/hexa_lang_upstream_audit_2026_05_03.md                        | audit     | NEW (~600 LoC)
   docs/hexa_lang_upstream_audit_landed_2026_05_03.ai.md              | handoff   | NEW (this file)
   state/markers/hexa_lang_upstream_audit_landed.marker               | marker    | NEW
   /Users/ghost/core/hexa-lang/                                       | substrate | UNCHANGED (read-only audit)
   /Users/ghost/core/anima/anima-voice/                               | substrate | UNCHANGED (additive invariant)
   .roadmap.vlm_voice_lm                                              | roadmap   | UNCHANGED (cond.3 still unmet, this audit informs path)
```

---

## §8 next-cycle entry triggers

```
   trigger                                         | leads to
   ----------------------------------------------- | ------------------------------------
   user OK on Track A2 hand-port                  | VLM stage1 unblock (4-16h)
   user OK on own N proposal (tool/transient_py/) | policy formalization (1h)
   Track A spike approved                          | atp_to_pytorch.hexa (8-24h)
   hexa-lang side accepts CUDA v5 land issue      | Track E retired
```

권고 sequence: **own N policy proposal → A2 hand-port (parallel BG) → VLM stage1 train → A transpiler retro-fit**.

---

## §9 cost

```
   cost band    | $0 mac-local (read-only audit, design-only)
   wallclock    | ~45 min
   destructive  | 0 actions
   in-place     | 0 (hexa-lang repo unchanged)
   new files    | 3 (audit + handoff + marker, all in anima/)
```
