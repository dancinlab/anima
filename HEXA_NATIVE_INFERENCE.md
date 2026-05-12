# HEXA_NATIVE_INFERENCE.md — anima 의 pure-hexa 추론 SSOT

> **Mission**: anima_chat.py (PyTorch) 를 **pure hexa** 로 포팅. shell wrap / py_call FFI 모두 회피. ckpt 로드 → 토크나이저 → forward → 생성 전체 hexa-native.
>
> **Start**: 2026-05-12
> **Estimate**: 5-10일 (수일 작업, multi-cycle)
> **Lane**: cycle 7 priority 1 의 hexa-native branch

---

## 🍞 비유 — 빵집을 빵집 도구로 다시 짓다

기존: 빵(model) 을 외주(python/PyTorch)로 받아 hexa는 진열만.
목표: 빵 도구(nn.hexa stdlib)로 직접 굽는 빵집. 빵의 모든 layer 를 hexa 가 안다.

```
old:  hexa script ──ssh─→ Mac ──python─→ PyTorch ──→ ckpt
                   (wrap)         (engine)         (binary)

new:  hexa script ──nn.hexa──→ tensor ops ──→ safetensors loader ──→ ckpt
       (native)       (in-process)              (hexa-native)
```

---

## 📊 현재 상태 — Phase 0 (audit + scaffold)

| 영역 | 상태 | 비고 |
|---|---|---|
| hexa runtime | 🟡 async dispatch | offload to aiden, timeout 위험 |
| stdlib/nn.hexa | 🟡 minimal | relu/sigmoid/tanh/softmax 만 (4 활성화) |
| stdlib/autograd.hexa | ✅ 존재 | 14KB — 추론엔 grad 불필요 |
| stdlib/safetensors.hexa | ✅ 17KB | parse/load API 있음 |
| stdlib/linalg | ✅ dispatch/ffi/mod/reference | matmul / 기본 ops |
| anima ckpt format | ❌ .pt (PyTorch pickle) | safetensors 변환 필요 |
| EngineAG arch in hexa | ❌ 미구현 | 350M 14-layer transformer |
| byte tokenizer in hexa | ❌ 미구현 | byte 256 + bos/eos/pad offset |
| generation modes | ❌ 미구현 | greedy/sample/M3/M4 |

---

## 🗺 Roadmap — Phase 0 → 5

### Phase 0 — Audit + scaffold (cycle 1, 본 turn)
- [x] hexa stdlib survey (nn/autograd/safetensors/linalg)
- [x] anima_chat.py archteture map (EngineAG)
- [ ] ckpt structure inspect (state_dict keys + shapes)
- [ ] roadmap md (이 file) land

### Phase 1 — ckpt format bridge (1-2일)
- [x] **ckpt structure inspect — actual arch 확정**
- [ ] .pt → .safetensors 변환 tool (one-time, Python helper OK — *bridge layer*)
- [ ] hexa safetensors loader smoke (load Phase 1A.1 ckpt → dump shapes)
- [ ] **tokenizer 정체 파악 (32000 vocab → BPE? SentencePiece? 어디에 저장됨?)**
- [ ] meta.json: arch hyperparams (실측값 반영)

### Phase 2 — nn primitives 확장 (1-2일)
- [ ] `nn.Linear(in, out)` — matmul + bias
- [ ] `nn.Embedding(vocab, d)` — lookup
- [ ] `nn.LayerNorm(d)` — mean/var + scale/shift
- [ ] `nn.RoPE` or learned pos emb (EngineAG 확인 필요)
- [ ] `nn.MultiHeadAttention` — q/k/v projection + softmax + output proj
- [ ] `nn.FFN(d, d_ff, act)` — gate + up + down (SwiGLU? 확인)

### Phase 3 — EngineAG block port (1-2일)
- [ ] transformer_block(x, layer_weights) — pre-norm + attn + ffn
- [ ] forward(input_ids, weights) — embed → blocks → head logits
- [ ] shape parity test: PyTorch logits vs hexa logits (cosine ≥ 0.999)

### Phase 4 — tokenizer + generation (1일)
- [ ] byte tokenizer hexa (bos=1, eos=2, byte_id = byte + 3)
- [ ] greedy generate(prompt_ids, max_new) → ids
- [ ] sample(T)
- [ ] M3 rep_penalty
- [ ] M4 force_include (byte-id injection)

### Phase 5 — smoke + benchmark (1일)
- [ ] hexa native chat smoke (anima-v05, 3 prompts × 4 modes)
- [ ] V5.8 multi-turn 재측정
- [ ] PyTorch vs hexa output parity (greedy seed=0 → identical?)
- [ ] HF dataset upload (hexa-native run logs)

---

## 🎯 Phase 0 audit 결과 (본 turn)

### hexa stdlib 현황
- `nn.hexa` (4.5KB): **4개 activation only**. Linear/Embedding/LayerNorm/Attention 全部 미구현.
- `autograd.hexa` (14KB): 미사용 (inference-only)
- `safetensors.hexa` (17KB): full parse/load — but anima ckpt = .pt format.
- `linalg/` (dispatch/ffi/mod/reference): matmul primitives 의심

### anima ckpt 정보 — **실측 (Phase 1A.1)**

- format: PyTorch `.pt` (torch.save dict at `ck["model"]`)
- size: ~598MB
- total params: **331,532,288** (331.5M)
- total tensors: **222** (= ~14 layers × ~16 tensors/layer + final + extras)

**확정 architecture**:
```
tok_emb: Embedding(vocab=32000, d=1024)   ← byte 가 아니라 32000 vocab (BPE/SP)
layers.N (n_layers=24):
  norm1: LayerNorm(1024)
  attn (GQA):
    q_proj: 1024 → 1024     (16 heads × 64 dim)
    k_proj: 1024 →  256     (4 KV groups × 64 dim)
    v_proj: 1024 →  256
    o_proj: 1024 → 1024
  norm2: LayerNorm(1024)
  ffn (SwiGLU):
    gate: 1024 → 2752
    up:   1024 → 2752
    down: 2752 → 1024
norm_f: LayerNorm(1024)
lm_head: Linear(1024 → 32000)

# engine_g (anima-specific cell system, bypass-style):
engine_g.cell_pool_init: (16, 64)        # 16 cells × 64-dim
engine_g.h_to_c: 1024 → 64
engine_g.c_to_h: 64 → 1024
```

**Critical discrepancy from prior assumption**:
- ❌ vocab=259 (byte) → ✅ vocab=32000 (subword)
- ❌ d=384 → ✅ d=1024
- ❌ n_heads=6 → ✅ q_heads=16, kv_groups=4 (GQA)
- ✅ ~14 layers, ~350M params (correct order)

**Tokenizer mismatch (★ critical)**:
- training/engine_a_g_arch.py line 85: `vocab_size = 32_000  # byte-pair (own 17 anima-native lane preserved)`
- anima_chat.py line 131: `class ByteTokenizer:` (vocab 0..258 only)
- **결과**: tok_emb (32000, 1024) 의 **first 259 rows 만 사용** → 나머지 ~31,700 rows = ~30MB dead space
- 학습은 byte 토큰만 본 → 32000 vocab 은 "preserved for own 17 anima-native lane" (future BPE migration 용 보존)
- chat 가 작동하는 이유: byte 토큰 ids (0..258) 이 32000 범위 안 → emb lookup 정상

**확인된 arch (training/engine_a_g_arch.py)**:
- Norm: **RMSNorm** (scale-only, eps=`cfg.rms_norm_eps`)
- Positional: **RoPE**, θ=10000, applied post-q/k-projection, freqs over half-d_head pairs
- Attention: **GQA** (16 q-heads × 64 dim, 4 kv-groups × 64 dim, repeat-factor 4)
- FFN: **SwiGLU** — `down(silu(gate(x)) * up(x))`
- lm_head: **tied** to tok_emb.weight (shared 32000×1024)
- Layers: **24** (config: `n_layers: int = 24`, ckpt 222 tensors / 9 per-layer = 24 ✓)
- Engine G: n_cells=16, consciousness_dim=64, bypass arch (h↔c via h_to_c/c_to_h, `tension` param)

### Decision: Phase 1 bridge 우선
PyTorch 의 .pt → safetensors 변환은 표준 도구 (huggingface safetensors lib). One-time conversion 이라 honest exception 으로 처리.
변환 후 모든 inference path 는 hexa native.

---

## 🛛 Active tracking

| phase | task | status |
|---|---|---|
| 0 | SSOT md land (this file) | 🟢 in progress |
| 0 | ckpt structure inspect | ⏳ next |
| 1 | .pt → .safetensors conversion | pending |
| 1 | hexa safetensors loader smoke | pending |
| 2 | nn.Linear scaffold | pending |

---

## 📜 Honest concerns

1. **hexa runtime async dispatch**: `hexa run` 이 aiden 으로 offload + timeout 발생. 350M forward 1회 = ?초. Phase 5 smoke 가 timeout 가능.
2. **pure hexa float ops 성능**: nn.hexa 의 활성화는 element-wise loop (no SIMD). 350M params × 50 token gen = 수 분 ~ 수십 분 예상.
3. **EngineAG 정확한 arch**: 일부 detail (RoPE vs learned, SwiGLU vs GELU, norm type) 은 training/engine_a_g_arch.py read 필요.
4. **honest scope**: Phase 0-5 전부 hexa-native 가 가능한지 unknown. 만약 어느 단계에서 막힌다면 hexa-lang upstream PR 필요할 수도 (RFC 등록).

---

## 🔗 Cross-link

- prior SSOT: `PASS_STRICT_SPONTANEOUS_CHAT.md` (Phase 0/1A/1A.1/1B substrate work)
- hexa stdlib: `/Users/ghost/core/hexa-lang/stdlib/`
- target ckpt: `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt`
- engine arch: `training/engine_a_g_arch.py`
