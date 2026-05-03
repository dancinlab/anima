# TLM + VLM Phase 3 — $200-cap Cost-Reduced Re-Spec — 2026-05-03

> spec doc, friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `docs/tlm_phase3_spec_2026_05_03.md` + `docs/vlm_phase3_spec_2026_05_03.md` (READ-ONLY)
> predecessors: `docs/tlm_stage12_landed_2026_05_03.ai.md` + `docs/vlm_stage12_landed_2026_05_03.ai.md`

---

## TL;DR

[CONSTRAIN] User constraint = GPU 비용 $200 이하 strategy only. 원래 TLM Phase 3 = $950-4400 (4 cond), VLM Phase 3 = $500-2300 (4 cond) → 양쪽 모두 cap 초과. 본 re-spec = (a) cond-단위 isolated cost re-estimate (b) $200 cap 안 viable subset 추출 (c) deferred (>$200) cond 측 별도 queue + 추후 budget unlock 시 entry trigger 정의.

비유 — 풀 옵션 신차 ($4400) vs basic trim ($200): basic trim 측 (1) chassis + (2) engine smoke test 만, 도색 + 인테리어 + entertainment system 측 다음 사이클 deferred. TLM 측 cond.5 (5ch deep validation, $100-400) + cond.6 voice partial ($0-200) 측 cap 안 가능, cond.3/cond.4 측 deferred. VLM 측 cond.4 (latency, $0 mac-local) + cond.6 (alpha endpoint, $0 deploy) 측 cap 안 zero-cost 가능, cond.3/cond.5 측 deferred.

결과 — TLM mini-spec ($100-400, cond.5 + cond.6 partial) + VLM mini-spec ($0-50, cond.4 + cond.6) + deferred queue (TLM cond.3 $650-3000 / cond.4 $200-800; VLM cond.3 $300-1500 / cond.5 $200-800) + sequencing 추천 (VLM 우선 — zero-cost path → TLM mini-spec → budget unlock 후 deferred land).

---

## §1 TLM minimum-viable cond + cost (≤$200 cap)

### §1.1 cond-단위 isolated cost breakdown

```
   cond                          | original cost | min isolated | $200 cap fit | deferred?
   ----------------------------- | ------------- | ------------ | ------------ | ----------
   cond.3 cross-LM r ≥0.85       | $650-3000     | $300-650     | NO           | YES
   cond.4 F3 MSE absolute ≤2.0   | $200-800      | $150-300     | borderline   | YES (mostly)
   cond.5 5ch deep validation    | $100-400      | $80-200      | YES          | NO
   cond.6 voice/speak downstream | $0-200        | $0-50        | YES (partial)| NO (partial)
```

**isolated min cost reasoning**:
- **cond.3**: P9 LHS-9 sweep × 4-arm random-control = 36-cell. minimum credible isolation = LHS-3 thinning × 2-arm (R1+R3) = 6-cell, ~24 GPU-hr × $5/hr ≈ $300-650 (RunPod A100/H100 spot price band). $200 cap 측 unmet.
- **cond.4**: F3 reconstruction MSE training (TLM-native loss) — encoder + head 측 5ch reconstruction sweep, minimum 2-arm random-control × 1 LR setting = ~12 GPU-hr × $5-20/hr ≈ $150-300. $200 cap 측 borderline (mac-local fallback 측 partial 가능 단 5ch encoder + LM head 측 mac-local training 측 RAM headroom unverified).
- **cond.5**: per-channel ablation (5 mask × small forward) + codebook size sweep (3 size × small training) — small-scale ablation 만, ~8 GPU-hr × $5-20/hr ≈ $80-200. $200 cap fit.
- **cond.6**: bridge LoRA Linear(512,384) + LayerNorm — additive light path, mac-local 측 fine-tune 가능 (TLM hidden 측 frozen, bridge 만 학습), ~4 GPU-hr × $5/hr ≈ $0-50 (mac-local 시 $0). speak cite gate 측 inference-only, threshold tuning 측 $0.

### §1.2 mini-spec verdict

```
   in-scope (≤$200)                                  | out-of-scope (deferred)
   ------------------------------------------------- | -------------------------------------
   cond.5 5ch deep validation ($80-200)              | cond.3 cross-LM fidelity ($300-650 min)
     - per-channel ablation (5 mask × forward)       | cond.4 F3 absolute reduction ($150-300 min)
     - codebook size sweep 64/256/1024 (small)       |
     - per-ch entropy measure                        |
   cond.6 voice/speak partial ($0-50)                |
     - bridge Linear(512, 384) LoRA (mac-local 시도) |
     - speak cite gate threshold tune ($0 inference) |
     - VLM/SLM hard dependency 측 cond.6a 만 (speak  |
       gate, downstream-light); cond.6b voice bridge |
       측 VLM Phase 3 cond.5 land 전까지 partial     |
```

**TLM mini-spec total cost** = $80-250 (best-case mac-local cond.6 + small-scale cond.5 GPU = $80; worst-case cond.5 upper $200 + cond.6 GPU $50 = $250 측 cap 약간 초과 가능 — mac-local cond.6 우선 + cond.5 측 codebook sweep 1 size 만 측 thinning 시 $150 안정 안 fit).

**recommendation**: cond.5 측 codebook sweep 측 256 (current default) + 1 alternative (64 또는 1024) 만 측 2-size sweep + per-ch ablation 5 mask 측 small forward — 추정 $100-150 GPU. cond.6a (speak gate) 측 mac-local $0. cond.6b (voice bridge) 측 mac-local 시도, GPU fallback 시 $30-50.

### §1.3 mini-spec entry gate

```
   gate                                | source                                | required for
   ----------------------------------- | ------------------------------------- | ----------------
   G1 corpus 결정 (blk.2)              | tlm_phase3_spec §8 G1                  | cond.5 (forward path)
   G2 P9 SFT pipeline LHS-3 reuse      | tlm_phase3_spec §8 G2 (thinned)        | cond.5 (small sweep)
   G3 sister .roadmap.tensionlink BR   | tlm_phase3_spec §8 G3                  | invariant (additive)
   G4 §16.2 random-control 2-arm thinning| tlm_phase3_spec §8 G4 (R1+R3 only)   | cond.5 (random gap)
   G5 anima_speak cite cleanup 검증     | docs/anima_speak_voice_cite_cleanup_landed| cond.6a (speak gate)
```

mini-spec 측 G1-G5 all ALL → entry GO. cond.5 + cond.6a 측 land 시 TLM Phase 3-mini complete, cond.3 + cond.4 + cond.6b 측 deferred queue.

---

## §2 VLM minimum-viable cond + cost (≤$200 cap)

### §2.1 cond-단위 isolated cost breakdown

```
   cond                          | original cost | min isolated | $200 cap fit | deferred?
   ----------------------------- | ------------- | ------------ | ------------ | ----------
   cond.3 CLM cross-LM r ≥0.85   | $300-1500     | $200-300     | borderline    | YES (mostly)
   cond.4 real-time latency<500ms| $0 mac-local  | $0           | YES          | NO
   cond.5 SLM prosody integration| $200-800      | $200-400     | borderline    | YES
   cond.6 alpha endpoint deploy  | $0 deploy     | $0           | YES          | NO
```

**isolated min cost reasoning**:
- **cond.3**: LoRA fine-tune on audio-text paired corpus (LibriSpeech subset). minimum 측 r=8 × 1 lr setting × 5K-step subset = ~12-24 GPU-hr × $15-25/hr ≈ $200-300. $200 cap 측 borderline (single-cell minimum 측 약 $200, multi-checkpoint cadence 시 $300+).
- **cond.4**: streaming bench + KV-cache profiling — mac-local Mk.III audio_token_predictor 측 inference profiling 만, GPU 사용 X. Stage 0..6 latency budget allocation + p50/p99 measure = $0.
- **cond.5**: SLM prosody head LoRA — SLM Phase 1+2 land 측 prerequisite (currently unmet), prosody token 8d → 384d projection LoRA = ~12 GPU-hr × $15-25/hr ≈ $200-400. SLM Phase 1+2 land 측 별도 cost (recursive dep).
- **cond.6**: endpoint integration + observability wire-up — mac-local alpha (anima-side 측 integration), training 0건. wire format + chunk size + backpressure 측 implementation only = $0.

### §2.2 mini-spec verdict

```
   in-scope (≤$200)                                  | out-of-scope (deferred)
   ------------------------------------------------- | -------------------------------------
   cond.4 real-time latency ($0)                     | cond.3 cross-LM fidelity ($200-300 min, borderline)
     - Stage 0..6 latency budget allocation          | cond.5 SLM prosody integration ($200-400 + SLM dep)
     - cold first audio frame measure                |
     - p50/p99 chunk latency measure                 |
     - KV-cache prefill profiling                    |
     - barge-in VAD gate latency measure             |
   cond.6 alpha endpoint deploy ($0)                 |
     - alpha endpoint contract land                  |
     - streaming bidi wire format                    |
     - 4번째 caller (LM-augmented audio AR) 등록     |
     - graceful fallback to Mk.III only path verify  |
     - observability metrics wire-up                 |
```

**VLM mini-spec total cost** = **$0** (zero-cost path — cond.4 + cond.6 모두 mac-local + integration only, training 0건).

**recommendation**: VLM mini-spec 측 zero-cost 즉시 entry 가능 — sister .roadmap.voice cond.2 (3-caller stable interface) land 후 endpoint integration + latency profiling 측 평행 진행. cond.3 측 borderline ($200-300) 측 budget unlock 시 우선 entry, cond.5 측 SLM Phase 1+2 land 후 별도 cycle.

### §2.3 mini-spec entry gate

```
   gate                                | source                                | required for
   ----------------------------------- | ------------------------------------- | ----------------
   V1 sister .roadmap.voice cond.2 land| vlm_phase3_spec §8 (caller interface) | cond.6 (alpha endpoint)
   V2 mac-local RAM headroom measure   | vlm_phase3_spec §8 (LoRA footprint)   | cond.4 (latency baseline)
   V3 anima_voice Stage 0..6 invocation| vlm_stage12_landed (cond.2 frozen)    | cond.4 + cond.6
```

mini-spec 측 V1-V3 all ALL → entry GO. cond.4 + cond.6 land 시 VLM Phase 3-mini complete.

---

## §3 Deferred conds (>$200, queued for later)

### §3.1 deferred queue

```
   cond                              | source LM | min cost  | budget unlock trigger
   --------------------------------- | --------- | --------- | -----------------------------------
   TLM cond.3 cross-LM fidelity      | TLM       | $300-650  | budget +$650 unlock + G1-G4 ALL met
   TLM cond.4 F3 absolute reduction  | TLM       | $150-300  | budget +$300 unlock + cond.4 path verify
   TLM cond.6b voice bridge          | TLM       | $0-50     | VLM Phase 3 cond.5 (SLM prosody) land
   VLM cond.3 cross-LM fidelity      | VLM       | $200-300  | budget +$300 unlock + audio-text corpus G2
   VLM cond.5 SLM prosody integration| VLM       | $200-400  | SLM Phase 1+2 land (prerequisite)
```

### §3.2 deferred ordering rationale

```
   priority | cond                              | rationale
   -------- | --------------------------------- | -----------------------------------------------
   P1       | VLM cond.3 ($200-300)             | lowest min cost, single-cell LoRA, sibling parity floor
   P2       | TLM cond.4 F3 ($150-300)          | TLM raison d'être (CLM Phase 1.6 lesson 적용 target)
   P3       | TLM cond.3 ($300-650)             | sibling parity floor, TLM 측 cross-LM r ≥0.85 entry
   P4       | VLM cond.5 ($200-400 + SLM dep)   | SLM Phase 1+2 prerequisite 측 recursive cost
   P5       | TLM cond.6b ($0-50)               | VLM cond.5 land 후에만 entry (transitive dep)
```

### §3.3 budget unlock thresholds

```
   unlocked budget | enabled cond                                       | combined min cost
   --------------- | -------------------------------------------------- | -----------------
   +$200           | VLM cond.3 OR TLM cond.4                            | $150-300
   +$500           | VLM cond.3 + TLM cond.4                             | $350-600
   +$1000          | VLM cond.3 + TLM cond.4 + TLM cond.3                | $650-1250
   +$1500          | + VLM cond.5 (after SLM Phase 1+2 land separately)  | $850-1650
   +$2000          | + TLM cond.6b (after VLM cond.5 land)               | $850-1700
```

---

## §4 추천 sequencing (TLM vs VLM 우선순위)

### §4.1 sequencing decision matrix

```
   priority | step                                       | LM   | cost     | rationale
   -------- | ------------------------------------------ | ---- | -------- | -----------------------------------
   S1       | VLM mini-spec entry (cond.4 + cond.6)      | VLM  | $0       | zero-cost, immediate entry, no GPU dep
   S2       | TLM mini-spec entry (cond.5 + cond.6a)     | TLM  | $80-200  | cap 안 max value, cond.5 측 5ch validity
   S3       | VLM cond.3 (budget unlock 후 first)        | VLM  | $200-300 | sibling parity floor 측 lowest min cost
   S4       | TLM cond.4 F3 (budget unlock 후 second)    | TLM  | $150-300 | TLM raison d'être, F3 ≤2.0 target
   S5       | TLM cond.3 cross-LM (budget unlock 후 third)| TLM | $300-650 | sibling parity floor 측 highest cost
   S6       | SLM Phase 1+2 land (separate cycle)         | SLM  | TBD      | VLM cond.5 + TLM cond.6b prerequisite
   S7       | VLM cond.5 (after SLM)                     | VLM  | $200-400 | SLM prosody integration
   S8       | TLM cond.6b (after VLM cond.5)             | TLM  | $0-50    | voice bridge, transitive dep
```

### §4.2 추천 first-batch (zero-budget required)

**Step 1: VLM 먼저** — cond.4 + cond.6 측 $0 cost, sister .roadmap.voice cond.2 + RAM measure 만 prerequisite, 즉시 entry 가능. mini-spec land 측 latency baseline + alpha endpoint contract 측 freeze, 추후 cond.3 budget unlock 시 fidelity 측 single-cell LoRA fast entry.

**Step 2: TLM mini-spec** — cond.5 + cond.6a 측 $80-200 GPU, G1-G5 entry gate 측 검증 후 entry. cond.5 (5ch deep validation) 측 encoder spec freeze 측 information-theoretic anchor (per-ch entropy + ablation), Phase 1+2 spec freeze 측 first measurable validation.

**Step 3 onward: budget unlock 의존** — $200 단위 incremental unlock 시 priority order P1→P5 따라 entry. SLM Phase 1+2 측 별도 cycle 측 independent prerequisite, VLM cond.5 + TLM cond.6b 측 cascade unblock.

### §4.3 sequencing caveat

cond.5 (TLM 5ch deep validation) 측 cond.3 (cross-LM fidelity) 와 idealy parallel entry (encoder fidelity 측 cross-LM r 측 measure 와 결합), $200 cap 측 cond.3 deferred 시 cond.5 측 isolated standalone — random-control gap (R1 ≥3.0 absolute MSE) 측 cond.5 측 internal floor 만 검증, true cross-LM fidelity 측 unmeasured carried forward.

---

## §5 honest C3 caveats (raw#10)

1. **C1 — cost band 측 historical RunPod spot price 측 estimate, actual $/hr 측 instance type + region + spot vs on-demand 측 변동** — A100/H100 spot $1.5-3/hr (best case) vs on-demand $4-8/hr (worst case). $80-200 GPU cost 측 mid-band (~$5/hr) 가정. $200 cap 측 spot pricing 시 더 많은 hour 가능, on-demand 시 더 적은 hour. real $/hr 측 RunPod credit balance + instance type 결정 시 confirm 필수.

2. **C2 — cond.5 측 isolated entry 측 cross-LM fidelity unmeasured invariant** — TLM Phase 3 mini-spec 측 cond.5 (per-ch ablation + codebook sweep) 만 land 시 5ch encoder 측 internal validity 측 검증, sibling LM ≥0.85 r 측 cross-LM parity 측 cond.3 측 deferred — Phase 3-mini land 후 TLM 측 "sibling LM 와 동등 floor" 측 unverified carried forward. cond.3 측 budget unlock 후 entry 시까지 TLM 측 phenomenological standalone 측 framing 권고 (sibling parity claim 측 보류).

3. **C3 — TLM cond.6b (voice bridge) 측 VLM Phase 3 cond.5 (SLM prosody) 측 transitive dep cascade — Phase 3-mini 측 cond.6a (speak gate) 만 partial land** — original Phase 3 spec §6 C3 측 carried forward. cond.6b (voice bridge Linear(512,384)) 측 VLM Phase 3 cond.5 (SLM prosody integration) land 후에만 entry — VLM cond.5 측 SLM Phase 1+2 land 후 entry — SLM cycle 측 .roadmap.eeg B1-B4 PASS 후 entry. 3-level transitive cascade 측 base layer (.roadmap.eeg) fail 시 TLM cond.6b 측 indefinite block, mini-spec 측 cond.6a (speak gate, downstream-light) 만 partial land 측 mitigation.

4. **C4 — VLM mini-spec 측 zero-cost claim 측 mac-local RAM headroom verify 미완료 측 risk** — vlm_phase3_spec §6 C3 측 model size constraint carried forward. anima-voice Mk.III audio_token_predictor 측 mac-local inference 가능 size 측 검증 완료, cond.4 latency profiling 측 baseline 측 currently mac-local 가능 가정. RAM headroom verify 측 V2 entry gate (mac-local RAM headroom measure) 측 사전 land 필수 — fail 시 mini-spec entry 측 GPU fallback ($30-100) 측 partial cost 발생.

5. **C5 — $200 cap 측 minimum credible single-cell training cost 측 hard floor** — VLM cond.3 측 minimum $200-300 측 LoRA r=8 × 1 lr × 5K-step 측 single-cell 측 lower bound, P9 LHS-9 sweep 측 9-cell 측 historical cost 측 ~$300/cell 측 평균. $200 cap 측 single-cell 측 borderline 측 cost overshoot 가능성 (e.g., LR sweep 1-cell 측 1.5x cost 측 $300+). cap strictly hold 측 cond.3 측 deferred 권장, cap relaxation +$100 시 cond.3 entry 가능.

6. **C6 — mini-spec 측 Phase 3 spec freeze 측 partial measurement, full Phase 3 cond.3-6 four-condition completion 측 NOT met** — Phase 3 entry trigger (4-gate ALL) 측 mini-spec 측 cond.3 deferred 시 Phase 3 entry gate 측 partial met. mini-spec land 측 Phase 3-mini 측 별도 marker (Phase 3-mini complete, Phase 3 full deferred) 권장 — Phase 3 entry gate 측 strict reading 측 mini-spec 측 Phase 3 entry 측 partial, cond.5 + cond.6a + (VLM) cond.4 + cond.6 만 land. Phase 3 full completion 측 deferred queue 측 budget unlock 후 cond.3 + cond.4 + cond.5 (VLM) + cond.6b (TLM) land 시 freeze 가능.

7. **C7 — RunPod credit balance 측 currently unverified state, cost estimate 측 abstract budget 가정** — `state/runpod_credit_status.json` 측 modified state, 실제 credit balance + spot vs on-demand 측 currently unaccessed. $200 cap 측 user constraint 측 abstract budget, actual RunPod credit + payment 측 cycle entry 시 verify 필수 (G2 entry gate prerequisite 권장 추가).

8. **C8 — sequencing 추천 (VLM 먼저, TLM 두번째) 측 zero-cost path 측 risk-free 가설, 단 VLM cond.4 latency measure 측 mac-local 측 actual hardware 측 dependent** — current mac (M1/M2/M3 등 unspecified) 측 VLM Mk.III audio_token_predictor 측 latency baseline 측 hardware-specific. <500ms target 측 mac-local 측 met 가능성 측 high (Mk.III 측 mac-local design), 단 actual measure 측 first-time. fail 시 GPU fallback (cond.4 측 partial GPU cost $30-100) 측 mini-spec total cost 측 $30-100 으로 변동 가능.

---

## §6 산출물

```
   path                                                  | type      | status
   ----------------------------------------------------- | --------- | --------
   docs/tlm_vlm_200cap_respec_2026_05_03.md              | spec      | NEW (this file)
   docs/tlm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   docs/vlm_phase3_spec_2026_05_03.md                    | spec      | unchanged (READ-ONLY source)
   .roadmap.tlm_tension_lm                               | roadmap   | unchanged (mini-spec entry 측 next-cycle update)
   .roadmap.vlm_voice_lm                                 | roadmap   | unchanged (mini-spec entry 측 next-cycle update)
```

---

## §7 7-element friendly summary

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [CONSTRAIN] TLM + VLM Phase 3 — $200 cap re-spec
   2. analogy             | basic trim ($200) vs full option ($4400) — chassis + smoke test only
   3. core 결과            | TLM mini ($80-200): cond.5 + cond.6a partial
                          | VLM mini ($0): cond.4 + cond.6
                          | deferred (>$200): TLM cond.3/4/6b, VLM cond.3/5
   4. 마이그레이션 0          | original Phase 3 spec docs 측 0 byte modification
                          | additive only — mini-spec 측 separate doc, source SSOT untouched
   5. handoff path         | 본 spec doc = mini-spec entry agent reference SSOT
                          | + entry gate (TLM G1-G5 / VLM V1-V3)
                          | + deferred queue P1-P5 priority + budget unlock threshold
   6. 다음 step             | (1) VLM mini-spec entry (cond.4 + cond.6, $0)
                          | (2) TLM mini-spec entry (cond.5 + cond.6a, $80-200)
                          | (3) RunPod credit balance verify (C7 mitigation)
                          | (4) budget unlock trigger 후 deferred queue P1→P5 순차 entry
                          | (5) SLM Phase 1+2 land 별도 cycle (VLM cond.5 prerequisite)
   7. cost                 | mini-spec total $80-200 (TLM only, VLM zero-cost)
                          | full Phase 3 deferred 추가 cost $850-1700 (budget unlock 시)
                          | mac-local inference $0 invariant 유지
```

---

## §8 doc meta

```
   doc          | docs/tlm_vlm_200cap_respec_2026_05_03.md
   type         | spec (Phase 3 cost-reduced re-spec, $200 cap)
   substrate    | READ-ONLY: tlm_phase3_spec + vlm_phase3_spec + tlm_stage12_landed + vlm_stage12_landed
   write        | this doc only
   raw#9        | NO .py (markdown only)
   raw#15       | NO personal paths
   execute      | none
   commit       | none
   marker       | none (spec doc only)
```

end-of-doc.
