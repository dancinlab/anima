# TLM cond.6a speak/voice gate threshold tune Landed — 2026-05-03 (AI-native)

> friendly preset (icon + analogy + 7-element + ASCII)
>
> readers: AI agents (subagents, audit cron), Claude Code (next session)
> source-of-truth: `state/tlm_cond6a_speak_gate_threshold_2026_05_03/threshold_tuning.json`
> predecessors: `docs/tlm_phase3_spec_2026_05_03.md` §2.4 + `docs/tlm_vlm_200cap_respec_2026_05_03.md` §1.1 cond.6a + `docs/anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md`
> sister landed: `docs/tlm_stage12_landed_2026_05_03.ai.md` (cond.1 met / cond.2 partial)

---

## TL;DR

**오늘 한 일** — TLM Phase 3 mini-spec 측 cond.6a (speak/voice cite cleanup gate threshold tune) 측 inference-only $0 mac-local EXEC. 12-sample validation set (anima-voice/anima_voice.hexa Test 1-4 + emotion_prosody.hexa whisper/exclamatory/interrogative rule corner) 측 5-candidate threshold grid evaluation, 결과 = **T_default (high=0.70 / low=0.30) 측 12/12 PASS (100%) lock**. spec line 122 (`tlm_phase3_spec_2026_05_03.md`) verbatim 와 동일 — tie-breaker (T_asymmetric_high 0.75/0.30 also 12/12) 측 frozen-spec minimal departure 원칙 적용. .roadmap.tlm_tension_lm 측 cond.6a sub-entry additive only update + state JSON + handoff doc + silent-land marker 측 land. sister .roadmap.tensionlink 측 0 byte diff invariant 유지.

**비유** — 송신탑 (.roadmap.tensionlink R=0.999, 잘 가동 중) 의 신호를 받는 수신탑 (TLM) 의 출력단에 "긴장도 다이얼" 이 있는데, 다이얼 위치가 **0.7 이상이면 verbose cite** (책 페이지 번호 + 출처 인용 다 적기), **0.3 이하면 minimal cite** (제목만), 중간이면 default. 본 cycle 은 다이얼의 두 눈금 (0.30 / 0.70) 이 적절한지 12개 시나리오 (잔잔 t=0.05 → 격앙 t=0.91) 로 손으로 돌려보고 모두 의도대로 동작 확인. 다이얼 자체는 spec 에 이미 적혀 있던 값, 본 cycle 은 "그 값이 실제로 작동하는지" 만 검증 + lock.

**결과** —
- threshold lock: **high=0.70 / low=0.30** (T_default)
- validation: **12/12 PASS** (100% agreement)
- evaluated grid: **5 candidates** (T_default / T_tight / T_loose / T_prosody_aligned / T_asymmetric_high)
- artifacts: **1 state JSON + 1 handoff doc + 1 marker + 1 roadmap additive update** (sister SSOT untouched)
- cost: **$0** mac-local inference-only

---

## §1 spec source + scope frame

**source rule** (from `tlm_phase3_spec_2026_05_03.md` §2.4 line 122 — paraphrased):
- TLM tension >0.7 → cite verbose mode
- TLM tension <0.3 → cite minimal mode

**re-spec scope per `tlm_vlm_200cap_respec_2026_05_03.md` §1.1**:
- cond.6a (gate, this cycle) = $0 mac-local inference-only — threshold tune + validation
- cond.6b (bridge Linear(512,384) + LayerNorm) = deferred (VLM Phase 3 cond.5 SLM prosody land 후 entry)

**downstream consumer**:
- `anima-voice/` (formerly `anima-speak/` — see `anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md`)
- handoff doc generators that emit cite breadcrumbs (source-of-truth + line number)

**fallback invariant** (tlm_phase3_spec §2.4 carried forward):
- TLM unavailable → mode = `default` (TLM-independent path, graceful degradation)

---

## §2 validation set (12 samples)

```
   id   | tension | source                                              | expected
   ---- | ------- | --------------------------------------------------- | --------
   V1   | 0.05    | anima_voice.hexa:540 Test 2 calm/neutral             | minimal
   V2   | 0.10    | anima_voice.hexa:364 VAD speaking gate floor         | minimal
   V3   | 0.15    | anima_voice.hexa:552 Test 4 sad                      | minimal
   V4   | 0.19    | emotion_prosody.hexa:183 whisper rule corner         | minimal
   V5   | 0.31    | emotion_prosody.hexa:192 interrogative lower bound   | default
   V6   | 0.42    | anima_voice.hexa:534 Test 1 joyful                   | default
   V7   | 0.50    | anima_voice.hexa:472 neutral prosody                 | default
   V8   | 0.69    | emotion_prosody.hexa:192 interrogative upper bound   | default
   V9   | 0.80    | anima_voice.hexa:474 joy prosody                     | verbose
   V10  | 0.61    | emotion_prosody.hexa:187 exclamatory rule corner     | default (see C1)
   V11  | 0.91    | anima_voice.hexa:546 Test 3 angry                    | verbose
   V12  | 0.90    | anima_voice.hexa:465 exclamatory test                | verbose
```

**label provenance**: `expected_mode` 측 anima-voice prosody 의도 + cite-cleanup cycle audit residual cite policy 에서 derived. 실제 cite-emission ground truth 측 NOT yet measured (C2 caveat).

---

## §3 candidate grid + scoreboard

```
   id                  | high | low  | agreement | rate    | verdict
   ------------------- | ---- | ---- | --------- | ------- | ----------------------
   T_default           | 0.70 | 0.30 | 12 / 12   | 1.0000  | SELECTED (frozen-spec match)
   T_asymmetric_high   | 0.75 | 0.30 | 12 / 12   | 1.0000  | tie (fallback if 0.70-0.75 over-fires)
   T_tight             | 0.80 | 0.20 | 11 / 12   | 0.9167  | dominated
   T_prosody_aligned   | 0.60 | 0.20 | 10 / 12   | 0.8333  | exclamatory-corner over-fires
   T_loose             | 0.60 | 0.40 | 9 / 12    | 0.7500  | rejected (boundary thrash)
```

**tie-breaker**: T_default vs T_asymmetric_high 모두 12/12. 결정 = **T_default** — frozen spec verbatim, sibling LM threshold convention 정합 (TLM stage12 land §1 carried forward), 0.70-0.75 band 측 verbose-overfire 측 future expanded set 에서 발견 시 T_asymmetric_high 측 fallback 가능.

---

## §4 boundary alignment (T_default lock)

```
   sample | tension | T_default decision           | prosody intent                       | aligned?
   ------ | ------- | ---------------------------- | ------------------------------------ | --------
   V4     | 0.19    | minimal (0.19 < 0.30)        | whisper rule (tension < 0.20)        | YES
   V5     | 0.31    | default (0.30 < 0.31 < 0.70) | interrogative lower (tension > 0.30) | YES
   V8     | 0.69    | default (0.30 < 0.69 < 0.70) | interrogative upper (tension < 0.70) | YES
   V10    | 0.61    | default (0.30 < 0.61 < 0.70) | exclamatory rule (tension > 0.60)    | PASS w/ caveat C1
   V11    | 0.91    | verbose (0.91 > 0.70)        | angry, max engagement                | YES
```

**boundary band semantics**:
- `[0.30, 0.40]` = default-mode floor (interrogative lower band)
- `[0.60, 0.70]` = default-mode ceiling (exclamatory corner safe band — prevents over-fire to verbose)

**hysteresis recommendation** (deferred to cond.6a IMPL phase):
- ±0.05 hysteresis around each threshold to suppress mode-thrash on time-series tension trajectories
- out of scope for this $0 inference-only spec-tune cycle

---

## §5 fallback policy

```
   condition                   | action
   --------------------------- | ----------------------------------------------------
   TLM unavailable             | mode = default (TLM-independent path)
   tension signal clipped      | tension clipped to [0.0, 1.0] before threshold compare
   Phase 3-mini placeholder    | tension scalar from 5-ch WHY-axis direct read OR .roadmap.tensionlink wire — both equivalent for threshold tune
   cond.2 IMPL pending         | true cond.6 land needs cond.2 LM head IMPL — see C3
```

---

## §6 honest C3 caveats (raw#10)

1. **C1 — exclamatory-corner conflict (V10 sample, tension=0.61)** — emotion_prosody.hexa:187 측 tension > 0.6 + arousal > 0.7 = exclamatory utterance. 직관적으로 "큰 소리 발화" 측 verbose cite 권유 가능. 단 T_default rule (high=0.70) 측 tension=0.61-0.69 측 default band 배치, NOT verbose. 본 cycle 측 PASS 라고 label — cite verbosity ≠ utterance loudness (verbose cite = SOURCE-OF-TRUTH emit, NOT prosody amplitude). C1 risk = downstream consumer 측 prosody-amplitude vs cite-volume semantics confusion 시 surprise. mitigation = handoff doc + threshold_tuning.json verdict 명시.

2. **C2 — sample size 12 small + label provenance heuristic** — expected_mode label 측 prosody intent + cite-cleanup audit narrative cases 에서 derived, 실제 cite-emission ground truth (anima-voice production runtime cite log + tension-tagged user feedback) 측 NOT measured. 12/12 PASS 측 spec-self-consistency check 측 measurement, downstream-utility measurement 측 NOT 가능. 추후 cite-emission event log 측 accumulate 후 expanded validation set (≥100 sample) 측 re-evaluate cycle 권장.

3. **C3 — TLM Phase 3 cond.2 (LM head) status = partial** — `.roadmap.tlm_tension_lm` cond.2 측 spec frozen, IMPL/training 0건 (decoder-only LOCKED, P9 SFT pipeline reuse plan 만, 실제 weight 0건). cond.6a tension scalar source 측 currently placeholder (5-channel WHY-axis direct read OR .roadmap.tensionlink wire), NOT TLM head output. true cond.6 full land 측 cond.2 IMPL + 실 TLM hidden-state projection layer 필요. Phase 3-mini cond.6a 측 threshold rule + validation methodology 만 capture, upstream signal source 측 Phase 3 cond.2 IMPL ($650-3000 deferred per $200 cap) 측 carried forward.

---

## §7 산출물 file index

```
state/tlm_cond6a_speak_gate_threshold_2026_05_03/threshold_tuning.json   (state JSON, source-of-truth)
docs/tlm_cond6a_landed_2026_05_03.ai.md                                  (this handoff doc)
state/markers/tlm_cond6a_speak_gate_threshold_landed.marker              (silent-land marker)
.roadmap.tlm_tension_lm                                                  (additive cond.6a sub-entry only — sister .roadmap.tensionlink 0 byte diff)
```

reference-only (no modification):
```
docs/tlm_phase3_spec_2026_05_03.md                          (READ-ONLY source — §2.4 line 122)
docs/tlm_vlm_200cap_respec_2026_05_03.md                    (READ-ONLY scope — §1.1 cond.6a)
docs/tlm_stage12_landed_2026_05_03.ai.md                    (predecessor)
docs/anima_speak_voice_cite_cleanup_landed_2026_05_03.ai.md (predecessor — cite cleanup G5 entry gate)
anima-voice/anima_voice.hexa                                (validation sample source)
anima-voice/emotion_prosody.hexa                            (validation sample source)
.roadmap.tensionlink                                        (sister SSOT — 0 byte diff invariant)
```

---

## §8 raw 15 + BR-NO-USER-VERBATIM compliance

- **raw 9 (no .py)** — 본 cycle 측 .py 0건 생성, markdown + JSON only
- **raw 10 (honest C3)** — §6 측 3 caveats 명시
- **raw 15 (no personal paths)** — absolute path prefix 측 doc 본문 0건
- **BR-NO-USER-VERBATIM** — user directive paraphrase 만, verbatim quote 0건
- **silent-land marker** — `state/markers/tlm_cond6a_speak_gate_threshold_landed.marker`
- **dual SSOT additive only** — `.roadmap.tlm_tension_lm` cond.6a sub-entry additive 만, sister `.roadmap.tensionlink` 0 byte diff 유지
- **mac-local $0** — destructive 0, training 0, GPU 0, cloud 0
- **NO commit** — user directive per spec doc §8 commit=none

---

## §9 7-element friendly summary

```
   element                | content
   ---------------------- | ---------------------------------------------
   1. icon                | [LOCK] TLM Phase 3-mini cond.6a speak/voice gate threshold tune
   2. analogy             | 송신탑 (.tensionlink) → 수신탑 (TLM) 다이얼 두 눈금 (0.30 / 0.70) 손으로 돌려서 12 시나리오 검증
   3. core 결과            | high=0.70 / low=0.30 LOCK (T_default)
                          | 12/12 PASS (100%)
                          | 5-candidate grid evaluated, frozen-spec minimal-departure tie-breaker
   4. 마이그레이션 0          | sister .roadmap.tensionlink 0 byte diff
                          | anima-voice/ in-place 변경 0건 (read-only validation source)
                          | spec doc tlm_phase3_spec / respec doc tlm_vlm_200cap 측 0 byte diff
   5. handoff path         | state/tlm_cond6a_speak_gate_threshold_2026_05_03/threshold_tuning.json (SSOT)
                          | + this doc
                          | + silent-land marker
                          | + .roadmap.tlm_tension_lm cond.6a additive sub-entry
   6. 다음 step             | (1) cond.6a IMPL phase — hysteresis ±0.05 + cite-emission event log accumulate
                          | (2) expanded validation set ≥100 sample (cite log + user feedback)
                          | (3) cond.6b (voice bridge) — deferred (VLM Phase 3 cond.5 SLM prosody 후)
                          | (4) cond.5 (5ch deep validation) — $80-200 GPU budget unlock 후 entry
   7. cost                 | $0 mac-local inference-only (no training, no GPU, no cloud)
                          | wallclock ≈ 1 min (validation set inference + decision lock)
```

---

## §10 doc meta

```
   doc          | docs/tlm_cond6a_landed_2026_05_03.ai.md
   type         | landed handoff (cycle EXEC report, AI-native friendly preset)
   substrate    | mac-local, inference-only, $0
   write        | this doc + state JSON + marker + roadmap additive update
   raw#9        | NO .py (markdown + JSON only)
   raw#10       | 3 honest C3 caveats (§6)
   raw#15       | NO personal paths in body
   execute      | inference-only (12-sample threshold validation, mac-local, $0)
   commit       | none (user directive)
   marker       | state/markers/tlm_cond6a_speak_gate_threshold_landed.marker
```

end-of-doc.
