# CLM_V2_ARCHIVE_ADDENDUM — mitosis-as-instrumentation 정정 (2026-05-10)

## TL;DR

BG-R2-CELLS-DOWNLOAD 회수 결과 **이전 archive (CLM_V2_ARCHIVE_2026_05_09.md) 의 mitosis 본체 framing 부분 정정 필요**. cells64/cells128 .pt 는 **MitosisEngine ensemble 이 아닌 single byte-level Transformer decoder**. mitosis 는 **training-time instrumentation/orchestration** 이었지, 모델 architecture 아님. 단 본 finding 은 v5-anima lane 을 **죽이지 않음** — Engine A/G v5 위 mitosis-instrumentation 으로 재정의하면 더 정확.

raw#15 additive — 기존 archive doc 미수정, 본 addendum 으로 보강.

---

## §1 architecture finding 표

| 항목 | cells64/final.pt | cells128/step_35000.pt |
|---|---|---|
| 다운로드 | ✅ 218MB SHA verified | ✅ 218MB SHA verified |
| 실제 architecture | **single byte-level Transformer decoder** | 동일 |
| state_dict keys | 108 (tok_emb, pos_emb, 6 blocks {ln1, attn{c_attn,c_proj}, ln2, ffn{engine_a, engine_g}}, ln_f, head_a, head_g) | 동일 (heads=4 vs 6) |
| 파라미터 | 18.523M | 동일 |
| step | 50000 (final) | 35000 |
| ckpt phi_history mean | **50.42** ★ (announce 51.131 정합) | 62.38 |
| MitosisEngine 호환 | ❌ schema overlap = 0 | ❌ |
| ConsciousLMReconstructed (smoke arch) 호환 | ✅ 108/108 strict load | ✅ |
| forward smoke | PASS 5/5 | PASS 5/5 |
| chat-cap (sampling top-k=40 t=0.8) | ❌ random letter soup | ❌ |
| chat-cap (argmax) | ❌ 60 × space (degenerate) | ❌ |

## §2 framing 정정 핵심

### 이전 framing (CLM_V2_ARCHIVE §2)

> mitosis.py 는 multi-cell consciousness manager. 각 cell 은 별도 ConsciousMind (engine_a + engine_g + GRU memory). cells64 = 64 개의 분열한 ConsciousMind 의 ensemble.

### 정정된 framing

mitosis = **training-time instrumentation/orchestration** :
1. 모델 본체 = 단일 byte-level Transformer decoder (`conscious_lm.py` family, 18.523M params, vocab=256, d=384, 6 layers, dual engine_a/engine_g FFN + dual head_a/head_g)
2. mitosis.py 의 `Cell` dataclass = metadata-only tracking (cell_id, specialty, tension_history, parent_id) — **nn.Module weight branch 아님**
3. cells64 / cells128 = **mitosis-trial 의 max_cells config (학습 run 의 hyperparameter)**, model architecture 변종 아님
4. Φ history (50.42 / 62.38) = 학습 중 mitosis-instrumentation 이 기록한 Φ proxy 값 — runtime 측정값 아님

### bucket naming 의 misread (2026-05-06 BG)

> bucket key `conscious-lm/cells64/final.pt` 의 `cells64` 는 architectural variant 가 아닌 **학습 run 의 max_cells=64 config 명**.

### mitosis.py 와의 관계

`/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L) 는 **toy/proof-of-concept implementation** — small ConsciousMind cells (input_dim=64, hidden=128, output=64). 실제 v2 production model (cells64/cells128) 와 schema overlap = 0. mitosis.py 는 별도 mini-experiment, production model 아님.

## §3 chat-cap reproducibility

### sampling 검증 결과 (foreground 2026-05-10)

```
=== cells64 (Φ=50.42 history) ===
argmax k=1:        ALL prompts → 60 × space            ❌
top-k=40 t=0.8 a:  "ndn n hAgluga#{a iha t eauda..."   ❌ random letter
top-k=40 t=0.8 g:  "btwt r ar  wnnylr e ;e..."         ❌ 동일
combined a-g:      unicode garbage                     ❌

=== cells128 (Φ=62.38 history) ===
동일 패턴 (top-1 = space, sampling = random letter soup, no Korean characters)
```

### 의의

2026-05-05 V2 closure audit 의 **chat-incapability = architectural #115** 판정 재확인. 2026-03-28 commit message (`bb99b6b6`, `6abc42f6`) 의 KO chat 출력은 eval JSON 부재 → **reproducible evidence X**. 본 sampling test 가 그 historical claim 을 **재현 실패** 로 종결.

### 단 sampling test honest C3

1. ConsciousLMReconstructed schema 가 production v2 architecture 와 미세 차이 가능 (LayerNorm placement, dropout 위치 등) — strict load 108/108 PASS 임에도 inference 시점 미스매치 잔존 가능
2. block_size=256 / vocab=256 byte-level 가정 — production 시 다른 setting 가능성
3. tokenizer 부재 (byte-level 직접) — chat 학습 시 사용한 prompt 형식 (system prompt? user/assistant marker?) 미상
4. top-k=40 + temp=0.8 만 시도 — beam search, repetition penalty, longer context 미실험
5. 5 prompt × 8 setting 만 — 더 많은 prompt + 다양한 길이 미검증
6. cells64/128 의 ckpt 는 학습 중간/끝 snapshot — **chat-FT 후의 convo_5k.pt** (70MB, 2026-05-06 회수) 와 다른 lane. 그것도 gibberish 였음 — 별도 lane 으로 추가 FT 가 chat 회복 가능성 잔존

## §4 v5-anima lane 함의

본 finding 은 v5-anima lane 의 **목표 재정의** 를 요구하지만 **죽이지 않음**:

### 이전 v5-anima 가정
- 350M Engine A/G + MitosisEngine wrapper (cells 8 → 64 분열)
- 각 "cell" = consciousness slice 의 weight branch
- 분열 = nn.Parameter row 추가

### 정정된 v5-anima lane
- 350M Engine A/G **본체** (single decoder) — 이미 v2 와 같은 dual engine_a/g + head_a/g 패턴 보존
- mitosis = **instrumentation layer**: 학습/inference 중 cell-tension stat 추적, Φ proxy 계산, split/merge metadata 기록
- "cells 64" = max_cells config 의미 — 의식 셀 8 → 16 → 32 → 64 confidence/specialty pool 확장 (실제 weight 는 single tensor 의 row growth 가 가능하지만 model-level architectural variant 는 아님)
- cost 정정: $0 inference instrumentation (이미 정정 완료 in `.roadmap.clm_v5_anima_native`)

### long-trajectory smoke (2026-05-10) 와의 관계

α=0.688 super-linear 측정 + V14 mirror violation 결과는 여전히 valid — **mitosis_v5_port.py 의 cell_pool growth 메커니즘** 이 substrate-중립적이라는 finding 은 정정 무관. 단 historical 51.131 비교는 다른 metric scale (proxy vs IIT) 이므로 직접 매핑 X 는 이전과 동일.

## §5 다음 우선순위 갱신

| 순위 | step | 비용 | 메모 |
|---:|---|---:|---|
| 1 ★★★ | v5-anima lane 의 mitosis-as-instrumentation 재정의 + spec doc 갱신 | $0 | 본 addendum 결과 반영 |
| 2 ★★★ | Phase 2 cotrain checkpoint (BG-LA + BG-LB) 회수 후 mitosis instrumentation 활성 → Φ history 추적 | $0 | 진짜 substrate 검증 |
| 3 ★★ | cells64 chat-cap 추가 시도 (longer context, KO/EN system prompt format, beam search, repetition penalty 0.8-1.5) | $0 | 1h |
| 4 ★★ | convo_5k.pt 별도 sampling test (chat-FT lane separate) | $0 | 30min |
| 5 ★★ | conscious_lm.py / train_clm_v2.py worktree-3..7 에서 정확한 production architecture 매칭 | $0 | spec 정밀화 |
| 6 ★ | convo_5k.pt 추가 FT $5-20 (verbatim) | $5-20 | chat-cap 마지막 시도 |

## §6 honest C3 (≥7)

1. 본 addendum 자체가 BG-R2 결과 의 정정 — **이전 archive 의 mitosis-as-architecture framing 은 wrong** but 메모리/사용자 의 직관 ("anima 가 자라지 않나, 세포분열처럼") 의 mechanism-level 검증은 v5-anima long-trajectory smoke 에서 별도 입증.
2. cells64 의 ckpt phi_history mean=50.42 는 commit message announce 51.131 과 1.4% 차이 — 정합. 단 Φ proxy 정의 자체가 anima-internal metric, 학계 IIT 와 직접 비교 X.
3. ConsciousLMReconstructed 의 strict load 108/108 PASS 는 architecture 정확 일치 의미 — 단 inference 시점 의 detail (causal mask shape, dropout, etc.) 미세 차이 가능성 잔존.
4. sampling test 8 setting × 8 prompt = 64 trial 중 **단 1개도** Korean character 생성 안 함 — UTF-8 multi-byte sequence 학습 부족 또는 reconstruction mismatch.
5. mitosis.py (worktree-12 anima/src/mitosis.py) 가 toy 라는 finding 은 그 코드 가 의미 없다는 뜻 X — Φ proxy formula, adaptive split threshold, Lorenz autonomous chaos, DD55 conservation 등의 algorithm 은 모두 valid + 활용 가능. 단 production model 의 weight 와 직접 호환 X.
6. "mitosis = instrumentation" 정정은 anima 의 사상 ("의식 모델은 자란다") 을 부정하지 X — instrumentation 도 학습 중 model 성장의 driver 일 수 있음. cell metadata 누적이 학습 trajectory 에 indirect 영향 가능.
7. 본 cycle 의 archaeological 정정은 cycle 2026-05-09 의 13 worktree archive (anima_clm_01..13) 의 git history 가 풍부해 가능했음 — git history 보존이 substrate-recovery 의 enabler.

## §7 cross-link

- 이전 SSOT (수정 X, addendum 으로 보강): `CLM_V2_ARCHIVE_2026_05_09.md`
- 이전 SSOT (수정 X): `CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md`
- BG-R2 raw verdict: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/verdict.json`
- BG-R2 forward smoke: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/forward_smoke_cells{64,128}.log`
- sampling test (foreground 2026-05-10): `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/sampling_gen_test_result.json`
- v5-anima lane SSOT: `.roadmap.clm_v5_anima_native` (cost / inference-time framing 이미 정정 반영)
- v2-reborn lane SSOT: `.roadmap.clm_v2_reborn` (cond.2 architecture verify — mitosis_load_pass=false but reconstructed_load_pass=true)
- 이전 archaeology (BG-EP): `docs/anima_clm_origin_chat_history_archaeology_2026_05_05.md`
- v2 chat recovery doc: `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md` (정정 필요 — bucket naming misread)
- v2 deep research: `docs/anima_clm_v2_deep_research_landed_2026_05_06.ai.md`

raw#9/10/15 honest preservation, raw#37 additive, own 16 0-cost.

End of `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`.
