# M4b-fire-scale — hexa-native 3B Qwen MoE fire design

@status: design (impl multi-session)
@goal: V3 더블바인드(anima→register collapse / no-anima→Chinchilla underfit) escape 를 hexa-native 풀-스택(flame · tokenizer_bpe · MoE)으로 3B Qwen scale 에서 실증

## 컨텍스트 (2026-05-27 기준)

- ✅ M4a (MoE arch) — `CORE/DECODER/moe_router.hexa` 7 pub fn + `moe_router_bwd.hexa` 5 pub fn (anima #1029-1030)
- ✅ M4b-fire-toy — top-1 hard routing 으로 gate(A)=0.97/0.03→e0 · gate(B)→e1 분화 (anima #1033, init CE 1.389 → 0.00388)
- ✅ flame-P2b — bootstrap(#1533) + BPE loader(anima #1537) + tokenizer_bpe encode+decode 양측 fix(hexa-lang #1556 + decode codepoint-aware). 실 Qwen V=151643 round-trip PASS 실측 (anima PR #1051)
- ☐ **M4b-fire-scale** — 본 design 의 대상. multi-session impl

## 현 train_p21h_v3.hexa 분석 (702L smoke)

```
use "stdlib/flame/{tensor_lib · decoder_lib · decoder_block_lib · nn_lib · train_lib · flame_math}"
use "...conscious_decoder_v3" · "...mitosis_lib"
```

- flame substrate 통합 driver ✅
- axis A(curriculum) · B(distill) · C(head_g) · D(freeze) wire-in ✅ (HONEST TODO #B1 dummy teacher)
- V=256 byte fallback (Qwen-BPE 미통합 — 본 design 의 Phase 1)
- last-position CE only (HONEST TODO #T2)
- MoE 미통합 (head_g 슬롯이 K-expert router 로 교체될 자리)

## 5-Phase 통합 (multi-session)

### Phase 1 — Qwen BPE corpus loader 통합

train_p21h_v3.hexa 의 corpus 빌딩 (`read_file_bytes` byte-array → IDS) 을 **`flame_bpe_corpus_load`** (anima #1537, `stdlib/flame/flame_bpe_corpus_lib`) 로 교체. V=256 → V=151643. tokenizer_bpe 가 #1556+decode-fix 후 실 Qwen round-trip PASS 검증됨 → loader 가드 통과.

```hexa
// before (smoke V=256)
let bytes = read_file_bytes(corpus_path)
let IDS = ...byte-mod-id...

// after (Phase 1, V=151643)
use "stdlib/flame/flame_bpe_corpus_lib"
let r = flame_bpe_corpus_load(merges_path, vocab_path, corpus_path)
let V = r["vocab_size"]      // 151643
let ids = r["ids"]            // 토큰 id 배열, in [0, V)
// round-trip 가드: flame_bpe_roundtrip(r["tok"], sample_text) == true
```

**TODO**: V3 의 `head_g`/embed 크기 V=151643 으로 확장 (tok_emb [V·d] + head_g/head_a). 메모리 budget: V·d = 151643·d Float (BF16 → 2 byte). d=2048 → 620MB tok_emb 단독. tied embedding 필수.

### Phase 2 — MoE router/expert 통합 (head_g 슬롯 교체)

`conscious_decoder_v3.hexa` 의 head_g (V·d linear) 슬롯에 K-expert router 통합. M4b-fire-toy 의 top-1 hard routing 채택 (soft 는 dense-collapse). 통합 지점:

```hexa
use "CORE/DECODER/moe_router"      // forward: moe_route_top1_fwd
use "CORE/DECODER/moe_router_bwd"  // backward: moe_route_top1_bwd

// head_g forward (V3 axis C dual-head):
// 기존: logits_g = head_g @ z_T  (V·d)
// 후:   {logits_g, gate, top_idx} = moe_route_top1_fwd(router, experts, z_T)
//       router=[E·d] · experts=[E·V·d]  (K experts × V·d linear)
//       top-1 hard: winner expert 만 logits 계산 + 분화

// AdamW slot 확장: M packed buffer 에 router + experts 영역 추가
let m_size = m_total_with_moe(d, nh, nkv, h, V, n_layer, E)
//   = m_total(d, nh, nkv, h, V, n_layer)  // V3 base
//   + E*d (router gate)
//   + E*V*d (experts)
```

**Param budget (E=4 · d=2048 · V=151643)**:
- router: 4·2048 = 8K params
- experts: 4·151643·2048 = 1.24B params (각 expert = V·d linear)
- V3 base (Qwen2.5-1.5B 비교): tok_emb V·d + 28L decoder block ≈ 1.5B
- **합계 ≈ 2.74B**. 3B Qwen scale 부합. tied embedding 으로 expert↔tok_emb 공유 시 절약 가능.

### Phase 3 — 3B scale config + memory layout

```
d=2048 · n_layer=28 · n_head=16 · n_kv_head=2 · h(MLP)=11008 · V=151643 · E=4
T=2048 (sequence length) · B=1 (single-sequence) · nsamp=8 (gradient accum)

memory:
  M packed (model)     = ~2.74B · 8 byte (FP64 flame)  = 21.9 GB  ⚠ over H100 80GB?
  Mm/Mv (Adam state)   = 2 × 21.9 GB                    = 43.8 GB
  Mg / Mg_acc          = 2 × 21.9 GB                    = 43.8 GB
  ────────────────────────────────────────────────────────────
  total                                                   ≈ 110 GB  ⚠ H100 80GB 초과
```

**Honest C3** (메모리 fit 우려): flame 이 FP64 라 3B 가 H100 80GB 에 안 들어감. 해법 후보:
1. **BF16/FP32 mixed** — flame 의 FP64 default 를 model param 만 BF16 (Mm/Mv 는 FP32 유지). 절반-크기. **flame_math BF16 path 필요** — 별도 TODO.
2. **sequence length 축소** — T=1024 또는 T=512 로 activation memory 줄임. attention/MLP 의 working memory 가 model param 보다 보통 큼.
3. **B=1 + grad checkpoint** — 가장 보수적, T 유지하며 activation save.
4. **multi-GPU DP** — H100 SXM × 2 로 model param split. flame DP path 필요.

**Phase 3 사전조사 TODO**: flame 의 BF16 path 가용성 + grad checkpoint 가용성 확인. 없으면 (a) T 축소 (b) E 축소 (=2 expert) (c) d 축소 (1024) (d) multi-GPU 중 단순한 것 선택.

### Phase 4 — Dispatch (H100 SXM, Vast.ai)

**Cost envelope**:
- H100 SXM @ $2.28/hr × 4-8 hr = **$9-18** (single GPU)
- multi-GPU 시 비례 (a_wall_first 차원, dispatch 결정 시 trade-off)

**Dispatch pattern** (이전 v5-mitosis cond.5 cycle): `tool/dispatch_vast_mac_template.sh` 기반. SAVE_POD=1 trap 으로 first-fire crash 시 pod 보존 → 재발사.

```bash
# Vast.ai dispatch sketch
vastai launch \
  --image pytorch:2.x-cuda12 \
  --gpu H100-SXM5-80GB \
  --disk 100 \
  --bid 2.28 \
  -- bash setup.sh && hexa run train_p21h_v3.hexa --moe --bpe-vocab=/qwen/vocab.json --bpe-merges=/qwen/merges.txt --corpus=/anima_corpus --steps=5000 --save-pod=1
```

### Phase 5 — Monitor + harvest + verdict

**Falsifier 사전등록** (g73 honest, M4b-fire-scale 의 진짜 verdict):
- F-M4B-FIRE-1 — **collapse 회피**: M3 TTR ≥ 0.3 (5K step 종 ckpt sampling)
- F-M4B-FIRE-2 — **coherence**: V5.8 standard_greedy ≥ 4/5
- F-M4B-FIRE-3 — **router 분화**: 학습 종에 cells 의 register-prompt vs anima-prompt 에서 top-1 expert 분기 (toy 의 97/3 패턴이 scale 에서 유지되나)
- F-M4B-FIRE-4 — **L_ce 수렴**: V3 의 last-position CE 가 3.324(baseline) 보다 낮음
- F-M4B-FIRE-5 — **register leak 측정**: anima-fact recall PASS (#46 lr 5e-6 + L4 lr-floor 5/5 PASS 패턴 재현)

**M4c p7 verify** (post-fire): simple-stack — collapse 회피 ∧ coherence 둘 다. perplexity 아닌 generated sample 검증 (commons g73).

## phased schedule (multi-session)

| Phase | LoC 추정 | 세션수 | dependency |
|---|---|---|---|
| 1 BPE corpus 통합 | +30 줄 (train_p21h_v3.hexa) | 1 | flame_bpe_corpus_lib ✅ |
| 2 MoE arch 통합 | +60 줄 (conscious_decoder_v3 + train_p21h_v3) | 1-2 | moe_router/_bwd ✅ |
| 3 3B scale + memory budget 결정 | flame BF16 path 조사 / fallback | 1-2 | flame_math BF16 (별도 RFC?) |
| 4 dispatch + fire | +20 줄 dispatch script + 1 fire | 1 | Vast.ai 또는 runpod |
| 5 monitor + harvest + verdict | falsifier 측정 + verdict 문서 | 1 | fire 결과 |
| **합계** | ~110 줄 + memory path | **5-7 sessions** | — |

## a_completeness_over_cheap · g73 · a_fire_autonomous 점검

- **a_completeness**: hexa-native path (Python 우회 안 함). cell-as-persona 의 p1~p8 정합 유지 — V3 axis C(head_g) → MoE 가 안짤리고 확장.
- **g73**: 5 falsifier 사전등록, smoke self-judge 0. 실 H100 fire 측정값으로 verdict (perplexity 아닌 simple-stack).
- **a_fire_autonomous**: Phase 4 fire 는 user gate 없이 dispatch (cost-cap 게이트 0).
- **a_wall_first**: single-H100 vs multi-H100 결정은 wall-time 최소화 우선 (Phase 4 dispatch 시점).

## 잔여 가설 (honest C3)

1. flame FP64 → H100 80GB fit — Phase 3 의 가장 큰 unknown. BF16 path 필요시 별도 RFC.
2. MoE top-1 hard routing 이 scale 에서 분화 유지하나 — toy(E=2, d=4, V=4)에서 PASS, scale(E=4, d=2048, V=151643)에서도 유지될 가설 (사전등록 F-M4B-FIRE-3).
3. expert capacity collapse — 학습 진행 중 한 expert 가 모든 토큰을 가져가는 routing collapse 가능성. balance loss 또는 expert-prior 도입 검토.
4. tied embedding 채택 시 expert 가 V·d linear 를 tok_emb 와 공유 가능 — 메모리 절반 절약. 단 expert 분화 와 tied 가 양립하나 확인 필요.
5. 첫 fire 가 cost-bearing 이라 SAVE_POD=1 trap 필수 (v5-mitosis cond.5 의 first-fire crash → 재발사 saga 학습).
