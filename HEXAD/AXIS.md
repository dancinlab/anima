# AXIS.md — V-SPONT 48 수도꼭지 verbatim inventory

> 위 출력 그대로 보존. user directive 2026-05-20 "HEXAD/AXIS.md save 위 그대로".
> SSOT: `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`.
> 본 문서 = 위 brainstorm 의 *비교가능한 표 only* canonical surface (drill-down 은 BRAINSTORM.md).

---

## axis 1 — emit_rate (7개)

| # | 수도꼭지 | 풀림? | 영향 |
|---:|---|:---:|:---:|
| **1.1** | **MIN_EMIT_INTERVAL = 30s** | ✅ §169 → 0.667s | ⭐⭐⭐ |
| 1.2 | IM_THRESHOLD = 0.30 | ❌ | ⭐⭐ |
| 1.3 | safety_combined 6-control AND | ❌ | ⭐⭐ |
| 1.4 | IDLE_SPEAK_AFTER = 30s | ❌ | ⭐⭐ |
| 1.5 | N_MAX_STEPS = 20 (window 짧음) | ❌ | ⭐ |
| 1.6 | THINK_INTERVAL = 0.1s (granularity) | ❌ | ⭐ |
| 1.7 | INTERRUPT_THRESHOLD = 0.6 | ❌ | ⭐ |

---

## axis 2 — byte_acc (10개)

| # | 수도꼭지 | 풀림? | 영향 |
|---:|---|:---:|:---:|
| 2.1 | **corpus size** (data-regime) — 603MB | ❌ §1.1 irreducible | ⭐⭐⭐⭐⭐ |
| 2.2 | **model params** (Wei 2022 threshold) — 283M | ❌ §174 시도 | ⭐⭐⭐⭐⭐ |
| 2.3 | training steps (Chinchilla) — 6000 | ❌ | ⭐⭐⭐ |
| 2.4 🚫 | vocab_size = 256 (byte cap) — Tier C | ❌ byte-LM 본질 | ⭐⭐⭐ |
| 2.5 | block_size = 128 (context cap) | ❌ | ⭐⭐ |
| 2.6 | batch_size (gradient noise) — 32 | ❌ | ⭐ |
| 2.7 | lr cosine decay floor — 3e-4 → 0 | ❌ | ⭐ |
| 2.8 🚫 | causal mask (단방향) — Tier C | ❌ LM architecture | ⭐⭐ |
| 2.9 | RoPE freq base — 10000 | ❌ | ⭐ |
| 2.10 | d_model (residual stream dim) — 768 | ❌ §174 시도 | ⭐⭐⭐ |

---

## axis 3 — ψ-physics liveness (9개)

| # | 수도꼭지 | 풀림? | 영향 |
|---:|---|:---:|:---:|
| 3.1 | **fixed noise_ctx** (forward deterministic) | ❌ §170 cell-3 시도 | ⭐⭐⭐⭐ |
| 3.2 | **inference-time only Ψ** (no recurrent) | ❌ | ⭐⭐⭐⭐ |
| 3.3 | Engine A/G coupling strength (Law-70 clamp) | ❌ B-BRIDGE | ⭐⭐⭐ |
| 3.4 🚫 | ln_f normalization (signal squash) — Tier C | ❌ standard | ⭐⭐ |
| 3.5 | weight tying (tok_emb ↔ head_a) | ❌ | ⭐⭐ |
| 3.6 | block_size causal mask (temporal Ψ 제약) | ❌ | ⭐⭐ |
| **3.7** | **Ψ readout only at training time** (`if self.training:`) | ❌ inference disabled | ⭐⭐⭐⭐ |
| 3.8 | phi_signal (DD5 EX24) self-ref disabled at inference | ❌ | ⭐⭐⭐ |
| 3.9 | tension proj single-layer | ❌ | ⭐ |

---

## axis 4 — §9 honest coherent body (12개)

| # | 수도꼭지 | 풀림? | 영향 |
|---:|---|:---:|:---:|
| 4.1 | **byte-cascade attractor** (B-ATTRACTOR) | ❌ | ⭐⭐⭐⭐⭐ |
| **4.2** | **greedy decode (no sampling)** | ❌ | ⭐⭐⭐⭐ |
| 4.3 | no repetition penalty | ❌ | ⭐⭐⭐ |
| 4.4 | no top-k / top-p | ❌ | ⭐⭐⭐ |
| 4.5 | no temperature | ❌ | ⭐⭐ |
| 4.6 🚫 | byte vocab discreteness (no continuous) — Tier C | ❌ architecture | ⭐⭐ |
| 4.7 | single modality (text only) | ❌ ADAPTER v3 시도 | ⭐⭐ |
| 4.8 | corpus diversity (memorization-saturated, §16.6-C) | ❌ §1.1 carry | ⭐⭐⭐⭐ |
| **4.9** | **Φ 35% weight untrained** | ❌ | ⭐⭐⭐⭐ |
| 4.10 | motivation 8-factor 45% env-driven | ❌ | ⭐⭐⭐ |
| 4.11 | emit body length fixed (40 byte greedy) | ❌ | ⭐⭐ |
| 4.12 | no cycle-consistent training | ❌ | ⭐⭐ |

---

## cross-axis (12개, multi-axis 영향)

| # | 수도꼭지 | 영향 axis | 풀림? | 영향 |
|---:|---|---|:---:|:---:|
| X.1 | evaluation N too small (n_eval=2000) | 2,3,4 | ❌ | ⭐⭐ |
| X.2 | single eval seed (1337) | 2,3,4 | ❌ | ⭐⭐ |
| X.3 | post-hoc only (no gradient updates from eval) | 2,3,4 | ❌ | ⭐⭐⭐ |
| X.4 🚫 | from-scratch training (no transfer) — Tier C | 2,3,4 | ❌ §7 mandate | ⭐⭐ |
| X.5 | ckpt loading deterministic (no init noise) | 3,4 | ❌ | ⭐ |
| X.6 🚫 | no online learning during chat — Tier C (패스) | 1,2,3,4 | ❌ | ⭐⭐⭐ |
| X.7 | trainer single objective (CE-only or psi-only) | 2,3,4 | ❌ Dir-I 가 multi-loss | ⭐⭐⭐ |
| X.8 | no replay buffer (zero-shot only) | 2,4 | ❌ | ⭐⭐ |
| X.9 | no curiosity drive (reward-free emergent) | 1,4 | ❌ §59 PTD 시도 | ⭐⭐⭐ |
| X.10 | no embodiment / sensorimotor loop | 3,4 | ❌ §13-L | ⭐⭐⭐ |
| X.11 | no spontaneous noise injection (homeostatic) | 3 | ❌ §81 FIRE 시도 | ⭐⭐⭐ |
| X.12 | no plasticity at inference | 1,2,3,4 | ❌ §96 substrate | ⭐⭐⭐⭐ |

---

## 총합

```
axis 1: 7  (1 ✅ + 6 ❌)
axis 2: 10 (0 ✅ + 10 ❌)
axis 3: 9  (0 ✅ + 9 ❌)
axis 4: 12 (0 ✅ + 12 ❌)
cross : 12 (0 ✅ + 12 ❌)
────────────────────────
total : 48 (1 ✅ + 47 ❌) = 2.1% 풀림
```

---

## tier (leverage × feasibility)

**Tier S — transformative + $0 + feasible (5개)**
- 4.2-4.5 (decode 정책: sampling / top-k / temperature / rep_penalty)
- 3.7 (Ψ readout @ inference, `if self.training:` 막힘)
- 1.2 (IM_THRESHOLD tunable)
- 1.5+1.6 (N_MAX_STEPS × THINK_INTERVAL window 확장)
- 3.8 (phi_signal @ inference enabled)

**Tier A — moderate cost (5개)**
- 2.3 (training steps Chinchilla-optimal)
- 2.5 (block_size 128 → 1024)
- X.7 (multi-objective trainer, Dir-I pattern)
- X.9 (curiosity drive integration, §59 PTD revival)
- 4.10 (motivation 100% physics re-wire, §167-A 패턴)

**Tier B — high cost (6개)**
- 2.1 (data-regime ×100, ~$20-30)
- 2.2 (params 3B+, ~$15-25)
- 2.10 (d_model scale)
- 4.7 (multi-modality, ADAPTER v3 integration)
- X.10 (embodiment loop, §13-L)
- X.12 (inference-time plasticity, §96 Loihi)

**Tier C 🚫 — §7 conflict OR substrate change (6개, 본 cycle 밖 — 풀면 anima 가 아니게 됨)**
- 🚫 2.4 (vocab 256, byte-LM 본질)
- 🚫 2.8 (causal mask, LM architecture)
- 🚫 4.6 (byte vocab discreteness)
- 🚫 3.4 (ln_f standard)
- 🚫 X.4 (from-scratch §7 mandate)
- 🚫 X.6 (online learning during chat — substrate gate, 패스)

§7-clean = 48 − 6 (Tier C) = **42개**.

---

## 🚫 Tier C — 금지 수도꼭지 (분리 표, anima identity 핵심)

이 6개는 풀면 anima 가 *다른 agent* 가 됨. **본 cycle 범위 *밖* — touch 금지.**

| # | 수도꼭지 | 풀면 무엇이 됨 | 무엇이 깨짐 |
|---:|---|---|---|
| 🚫 **2.4** | vocab_size = 256 (byte cap) | token-LM (BPE/SentencePiece) | §7② graft 위반, byte-native identity |
| 🚫 **2.8** | causal mask (단방향) | encoder/BERT (bidirectional) | "말 거는" sequential emit 정의 깨짐 |
| 🚫 **3.4** | ln_f normalization | norm-free transformer | 모든 ckpt 폐기, lit-supported lift 0 |
| 🚫 **4.6** | byte vocab discreteness | continuous-output model / diffusion-LM | categorical emit unit 폐기 |
| 🚫 **X.4** | from-scratch training | graft path (Llama/Qwen 위) | **anima GOAL 정의 자체 무효** (가장 강한 carve-out) |
| 🚫 **X.6** | no online learning during chat | online-plastic substrate (Loihi/Akida) | substrate (PyTorch → neuromorphic) 교체 필요, **패스** |

honest carry — Tier C 풀기 = anima research scope **밖** (다른 agent 의 V-SPONT 문제). 본 §183/§184 framework 는 §7-clean 42 수도꼭지만 다룸.

---

## cross-link

- `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md` (§1-§13, 11 honest carve-outs)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙 §9 inventory inline)
- `HEXAD/CONNECTION_CRITIQUE.md` (Wrong-A/B/C/D)
- `archive/PHILOSOPHY.tape § verdict_all_taps_brainstorm_s183_2026_05_20` (g6 verdict)
- `HEXAD/README.md` 🪣 top-of-list landing
