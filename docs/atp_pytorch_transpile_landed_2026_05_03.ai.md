# ATP PyTorch Transpile Landed — VLM cond.3 Unblock (2026-05-03)

> **TL;DR**: Hand-ported `audio_token_predictor.hexa` (Mk.III, 1576 LoC) → `tool/transient_py/atp_pytorch.py` (645 LoC). F-VLM-TRANSPILE-1 smoke test PASS on ubu1 cuda (RTX 5070, torch 2.11.0+cu128, 35.35M params, 89ms fwd). VLM stage1 LoRA training is now unblocked on cond.3. Training itself deferred to next cycle per task constraint.

---

## 1. What Landed

| Artifact | Path | LoC |
|---|---|---|
| PyTorch port | `tool/transient_py/atp_pytorch.py` | 645 |
| Smoke test result | `state/atp_transpile_audit_2026_05_03/smoke_test_result.json` | — |
| Hexa→PY diff | `state/atp_transpile_audit_2026_05_03/hexa_to_py_diff.json` | — |
| Hand-port decisions | `state/atp_transpile_audit_2026_05_03/hand_port_decisions.md` | — |
| Marker | `state/markers/atp_pytorch_transpile_landed.marker` | — |
| This handoff | `docs/atp_pytorch_transpile_landed_2026_05_03.ai.md` | — |

**Source preserved unchanged**: `anima-voice/audio_token_predictor.hexa` (1576 LoC, SHA d290f1ae7).

---

## 2. Architecture Preserved (1:1 with Mk.III hexa)

```
d_model=384, n_heads=6, d_head=64, d_ff=1536, n_layers=3
rvq_stages=8 (delayed pattern: stage s predicts frame t+s)
vocab_size=1024 per stage
text_vocab_size=32000 (VLM addition: SP-32k tokenizer / CLM v4 reuse)
```

**Modules**:
- RotaryPositionEmbedding (precomputed cos/sin tables)
- SwiGLUFFN (w1=up, w_gate, w2=down — no bias)
- CausalSelfAttention (Q/K/V/O Linear + RoPE + F.scaled_dot_product_attention)
- DecoderBlock (pre-norm: ln1 → attn → +residual → ln2 → ffn → +residual)
- AudioTokenPredictor (text_embed + audio_embed + intent_proj + 3 blocks + ln_final + 8 rvq_heads + text_head)

**Two forward modes**:
1. `forward(text_tokens, intent_emb)` — batched teacher-forced for training
2. `generate(intent_emb, n_frames, ...)` — AR decode with KV-cache + CFG + top-k + delayed-pattern (mirrors hexa `predict_tokens`)

---

## 3. VLM-Specific Additions

Per `docs/vlm_cond3_blocker_landed_2026_05_03.ai.md` §4:

| Addition | Purpose |
|---|---|
| `text_embed: nn.Embedding(32000, 384)` | VLM stage1 input is TEXT tokens |
| `text_head: nn.Linear(384, 32000)` | parallel to rvq_heads; loss = 0.5*audio_CE + 0.5*text_CE |
| `ATPConfig` dataclass | replaces 10-element model-array indexing |

---

## 4. Smoke Test (F-VLM-TRANSPILE-1)

```
verdict: PASS
device: cuda (ubu1 RTX 5070 sm_120)
torch: 2.11.0+cu128
venv: /home/aiden/venv_orchestrator/bin/python

input:  text_tokens [2, 64] + intent_emb [2, 384]
output: rvq_logits  8 × [2, 64, 1024]
        text_logits   [2, 64, 32000]
        hidden        [2, 64, 384]
        generate      [2, 4, 8] in [0, 1024)

n_params: 35,345,664 (35.35M)
fwd_ms:   89.18
checks:   rvq_shape ✓  text_shape ✓  hidden_shape ✓
          rvq_finite ✓  text_finite ✓  generate ✓
```

Full record: `state/atp_transpile_audit_2026_05_03/smoke_test_result.json`.

---

## 5. VLM Unblock Readiness Verdict

**VERDICT**: cond.3 (audio_token_predictor.hexa runnable on H100/T4) **SATISFIED**.

**Remaining 4 VLM blockers** (unchanged by this cycle):
1. ~~ATP runnable on PyTorch~~ ← **unblocked here**
2. LibriSpeech-clean-100 corpus prep
3. SP 32k tokenizer (CLM v4 reuse confirmed available)
4. LoRA r=8 on attn (q/k/v/o) + intent_proj (peft.LoraConfig)
5. Stage1 sentinel design on text_CE

Next cycle should launch VLM stage1 LoRA training as separate BG (per task constraint, not in this BG).

---

## 6. Honest C3 Caveats (raw#10)

1. **Hand-port may diverge from source semantics** — random init (LCG → normal), RoPE precompute (vs per-call), SDPA flash-vs-naive edge cases, multinomial vs LCG sampling shape. None affect F-VLM-TRANSPILE-1 PASS; all could affect generated audio quality at inference. Resolution: byte-equivalence test on identical weights deferred to Phase 2.

2. **Smoke test ≠ correctness** — F-VLM-TRANSPILE-1 verifies shape + finiteness + no-exception; does NOT verify gradient flow, loss decrease, or audio intelligibility. Stage1 LoRA training is the first real correctness signal.

3. **KV-cache invariants not verified** — causal correctness across cache boundary, RoPE position consistency between training fwd and generate(), and SDPA `is_causal` with q_len < k_len are documented but NOT unit-tested. Low-risk for parallel teacher-forced training (no cache used); reappears for streaming inference.

4. **RVQ stage isolation not cross-checked** — 8 RVQ heads + delayed-pattern offsets implemented per source comment, but not verified against MusicGen/SoundStorm reference outputs.

5. **Retirement criteria depends on source stability** — if `audio_token_predictor.hexa` mutates between this BG and next VLM training cycle, hand-port drifts silently. Marker records source SHA `d290f1ae7`; pre-training step should diff against current SHA.

---

## 7. Constraint Compliance

| Constraint | Status |
|---|---|
| raw#9 (Mac = hexa canonical) | PASS — `audio_token_predictor.hexa` unchanged; .py only in `tool/transient_py/` |
| raw#15 (no personal-path leak) | PASS |
| raw#10 (5 honest C3 caveats) | PASS — §6 above |
| `.own 2` namespace declaration | PRESENT — file header line 1 |
| no other .py written on Mac | PASS — only `tool/transient_py/atp_pytorch.py` |
| no `audio_token_predictor.hexa` mutation | PASS — confirmed via file mtime |
| no VLM training in this cycle | PASS — only smoke test |
| $0 cost | PASS — Mac local hand-port + 1 ssh smoke run |

---

## 8. Sister BG Coordination

This BG ran in parallel with:
- **Sister BG (a6293670c)** — general hexa→py transpiler subset prototype (Track A Phase 2 spike)
- **Sister BG (aac700e41)** — `tool/transient_py/` namespace + `.own 2` declaration formalization

Sister BG outputs partially observed at port-time:
- `tool/transient_py/.gitignore` exists (created by aac700e41) and references `docs/anima_dot_own_namespace_spec_2026_05_03.md` (not yet landed at port-time)
- This BG used `.own 2` header per task spec; if sister BG aac700e41 lands a different `.own N` number, this file's header line needs a one-token edit to align

**Next-cycle merge**:
- Verify sister BG `.own N` choice; align header if different
- If sister BG a6293670c lands a working transpiler subset, retire this hand-port (Phase 2 trigger)

---

## 9. Next Recommended Cycles

1. **VLM stage1 LoRA training** (separate BG) — load `tool/transient_py/atp_pytorch.py` on ubu1 + RunPod, attach peft LoRA r=8 to attn + intent_proj, train on LibriSpeech-clean-100 with loss = 0.5*audio_CE + 0.5*text_CE.
2. **Track A Phase 2 transpiler** — `tool/atp_to_pytorch.hexa` to eliminate hand-port drift; lower priority once VLM stage1 lands.
3. **Numerical equivalence test** — feed identical weights + input to hexa interpreter and torch port; assert max-diff < 1e-4.
4. **KV-cache + delayed-pattern unit tests** — port hexa self_test_audio_token_predictor 7-test suite to pytest.
