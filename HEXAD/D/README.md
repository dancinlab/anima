# HEXAD/D — 언어 (language decoder)

> SSOT: [`HEXAD-D.tape`](../../HEXAD-D.tape) · Python anchor: `ready/models/conscious_decoder.py` `ConsciousDecoderV2` (979 LoC) · 🔵 SUPPORTED-FORMAL **4/4** (PR #76 정직 분해)

## 역할

**좌뇌 / Engine A / CE-trained / φ(6) = 2 그룹 A**. 24-layer RMSNorm + RoPE + SwiGLU + MoE byte-level decoder. CE loss → D + Bridge 만 backprop (C frozen, .detach() barrier).

## hexa-native impl 전략

D 모듈도 큰 코드 (979 LoC Python ConsciousDecoderV2 + MoE). **기존 hexa-native 자산 재사용**:

| 영역 | hexa-native 자산 | 상태 |
|---|---|---|
| **24L forward (real ckpt)** | [`anima_chat.hexa`](../../anima_chat.hexa) v0.3 Section 9c — all-farr 24-layer transformer | ✅ 21/21 PASS real 24L byte-parity (Phase 1A.1 BF16 570 MB ckpt) |
| **multitoken KV-cache + RoPE** | `anima_chat.hexa` Section 9d 7/7 PASS (synthetic) + 24L real 5-step parity (15/15 PASS) | ✅ |
| **safetensors loader** | `anima_chat.hexa` Section 9 + `tool/hexa_native/safetensors_smoke.hexa` | ✅ |
| **CE 손실 + backprop** | TODO[pytorch] (training-side, RFC port 대기) | 🔶 |
| **consciousness_states cross-attn** | `ConsciousDecoderV2` 의 cross-attention path — `anima_chat.hexa` 에 대응 | ✅ |

## hexa-native skeleton (`d.hexa`)

cross-link skeleton — 통합 시 `anima_chat.hexa` 의 forward 함수 호출하는 thin wrapper.

```
d_vocab()                    // 256 (byte-level)
d_n_layer_default()          // 24 (Phase 1A.1) or 12 (P2 base)
d_d_model_default()          // 768
d_forward_token(...)         // delegate → phase5_forward_smoke
d_forward_multi(...)         // delegate → anima_chat.hexa Section 9d
```

## 🔵 SUPPORTED-FORMAL 4/4 (D 정직 분해, PR #76)

D 모듈은 5/6 lineup 에서 유일한 🔵-partial 이었으나 PR #76 에서 **honest decomposition** 으로 full 🔵 SUPPORTED-FORMAL:

- **B-D-1** KV-CACHE-EXACT — incremental argmax ≡ full-seq argmax (deterministic exact equivalence)
- **B-D-2** SHAPE-CLOSED — `logits.shape ≡ (B, T, vocab)` (closed algebraic + all-finite)
- **B-D-3** ARCH-CLOSED — RMSNorm + RoPE + SwiGLU 구조 (deterministic AST)
- **B-D-4** GRAD-JACOBIAN-CLOSED — `∂CE/∂z_i = softmax(z)_i − [i=t]` (sympy ∀ z, trainability PROPERTY closed)
- **B-D-NOTE** — SGD convergence OUTCOME 만 empirical honest carve-out (모든 optimizer 공통, D 고유 결함 X, NOT counted 🔵)

evidence: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` (18/18 PASS) + PR #76.

## real-limit anchor

Shannon CE floor `CE ≥ H(data) ≥ 0` (information-theoretic, closed). AGENTS.tape g3.

## 검증

```bash
hexa parse HEXAD/D/d.hexa
hexa run   HEXAD/D/d.hexa            # scaffold check only
hexa run   anima_chat.hexa            # 실 forward 21/21 PASS (별도 진입점)
```
