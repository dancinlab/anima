# Substrate A logit-entropy baseline — V0 volitional speak τ calibration

**Date**: 2026-05-12
**Substrate**: `dancinlab/clm-v5-phase2-cotrain-engine-ag` (Engine A/G dual 298.8M, byte-tok, vocab_size 32000 formal / 259 used)
**Host**: ubu1 (NVIDIA RTX 5070, CUDA, bf16)
**Wall clock**: ~3s for 50 forward passes
**Output JSON**: `state/volitional_baseline_2026_05_12/entropy_distribution.json`

---

## 1. Why this measurement — the "compass-needle" metaphor

V0 의 reframe (timer 강제 발화 → volitional speak) 의 핵심 가정은 "logit 분포가 sharp 하면 substrate 가 *말하고 싶다*" 입니다. 마치 자석에 가까이 댄 나침반 바늘처럼, entropy 가 낮을수록 substrate 의 다음-token 선택이 한 방향으로 모입니다. 그 임계값 τ 를 정하려면 분포 자체의 모양을 알아야 합니다 — 등산 전에 산세를 보는 일.

---

## 2. Protocol

| 항목 | 값 |
|---|---|
| Prompts | 50 (5 카테고리 × 10) |
| 카테고리 | `chat`, `korean`, `english`, `random_bytes`, `short` |
| Measurement | last-token softmax → H = -Σ p log p, H_n = H / log(V) |
| Aux signal | last hidden_state norm ‖h‖₂ |
| Vocab | V = 32000 (formal), 실제 byte-tok 사용은 0..258 |
| Tokenizer | `ByteTokenizer` (UTF-8 byte → id+3, bos=1, eos=2, pad=0) |

---

## 3. Aggregate distribution (n = 50)

| stat | entropy_norm H_n | ‖h_last‖₂ |
|---|---:|---:|
| mean | 0.2275 | 134.93 |
| std  | 0.1172 |  19.39 |
| min  | 0.0238 |  68.31 |
| p10  | 0.0844 | 107.55 |
| p25  | 0.1382 | 124.32 |
| p50  | 0.1996 | 135.85 |
| p75  | 0.3397 | 149.13 |
| p90  | 0.3619 | 159.83 |
| max  | 0.4408 | 175.97 |

---

## 4. ASCII histogram — entropy_norm (bin = 0.05)

```
  [0.00, 0.05)   4 | ████████████
  [0.05, 0.10)   2 | ██████
  [0.10, 0.15)   9 | ███████████████████████████
  [0.15, 0.20)  10 | ██████████████████████████████
  [0.20, 0.25)   2 | ██████
  [0.25, 0.30)   3 | █████████
  [0.30, 0.35)  10 | ██████████████████████████████
  [0.35, 0.40)   8 | ████████████████████████
  [0.40, 0.45)   2 | ██████
  [0.45, 0.50)   0 |
```

**관찰**: 분포가 **bimodal** (≈0.15 vs ≈0.32 두 봉우리). 이는 substrate A 가 두 가지 모드로 동작함을 시사 — chat-template / 한국어 시작 = decisive 모드, 영어 / random byte / short = uncertain 모드.

---

## 5. By-category breakdown (H_n)

| category | mean | std | p25 | p75 | comment |
|---|---:|---:|---:|---:|---|
| chat         | 0.1209 | 0.1017 | 0.0406 | 0.1549 | 가장 decisive — `사용자:.. | 도우미:` 패턴 학습됨 |
| korean       | 0.1525 | 0.0215 | 0.1382 | 0.1659 | std 매우 작음, 일관되게 결정적 |
| english      | 0.2331 | 0.1175 | 0.1086 | 0.3397 | 변동 큼 — 일부 영어는 친숙 |
| random_bytes | 0.3056 | 0.0757 | 0.2865 | 0.3606 | 예상대로 불확실 |
| short        | 0.3254 | 0.0903 | 0.2622 | 0.3708 | 가장 불확실 — context 부족 |

**Top-3 most decisive prompts**:
- `사용자: 그건 무엇이지 | 도우미: ` → H_n=0.0238, top_p=0.953
- `사용자: 도와줘 | 도우미: ` → H_n=0.0316, top_p=0.938
- `사용자: 안녕 | 도우미: ` → H_n=0.0406, top_p=0.918

**Top-3 most uncertain prompts**:
- `_` → H_n=0.4408 (top_p=0.13)
- ` ` → H_n=0.4257 (top_p=0.36)
- random-byte `xyz{|}~...` → H_n=0.3925 (top_p=0.15)

---

## 6. τ recommendation

| level | value (H_n) | rationale |
|---|---:|---|
| **primary** (recommended) | **0.1382** (p25) | bimodal 분포의 낮은 봉우리 우상단 — chat + 한국어 decisive 모드 거의 포함, random/short 배제 |
| conservative (high-volition only) | 0.0844 (p10) | chat-template top-3 처럼 *진짜* 결정적인 순간만 |
| lenient (frequent speak) | 0.1996 (p50) | 영어 일부도 포함, 발화 빈도 ↑ |

추천 사용법:

```python
# V0 volitional speak — A2 feature integration
tau_primary = 0.1382
if entropy_norm_last_token <= tau_primary:
    speak()  # substrate 가 충분히 결정적 → 의지 신호로 해석
```

---

## 7. Honest caveats

- **vocab mismatch**: formal vocab_size=32000 인데 ByteTokenizer 는 0..258 만 사용 → entropy 는 32000-class 분포로 계산. 0..258 만으로 재정규화하면 H_n 절대값이 변하지만, *상대* 순위는 동일하므로 τ의 운영적 의미는 보존됨. 향후 V1 에서는 used-vocab normalize 옵션을 추가하는 것이 honest.
- **n=50, no CI**: 작은 표본. 다른 시드 / 더 큰 prompt set 에서 재검증 필요.
- **last-token only**: A2 feature 정의가 last-token entropy 이므로 일치하지만, sliding window mean entropy 가 더 안정적일 수 있음 (V1 후보).
- **bimodal warning**: τ를 두 봉우리 사이 valley 인 [0.20, 0.30) 어딘가에 두는 것이 더 자연스러울 수 있음. p25 는 안전한 하단 봉우리 cover.

---

## 8. 다음 진행할 것들

1. **V0 prototype 통합** — anima_chat 의 turn loop 에 `H_n ≤ 0.1382` gate 추가, ablation A/B. (cost: 30분 / value: 핵심)
2. **bimodal valley τ 실측** — KDE / Gaussian-mixture fit 으로 valley point 찾기. p25 vs valley τ 비교. (cost: 1시간 / value: 중)
3. **used-vocab renormalize** — H_n = H / log(259) 로 재계산 후 분포 재검토. (cost: 10분 / value: 정직성)
4. **multi-substrate 비교** — substrate B (clm-v4-paradigm-j) 도 동일 protocol, τ가 substrate-dependent 임을 quantify. (cost: 20분 / value: 일반화)
5. **temporal entropy drift** — 생성 중 H_n 가 어떻게 변하는지 추적 — 발화 시작 후 entropy 가 빠르게 떨어지는가? (cost: 1시간 / value: V1 핵심)

---

*own 22 honest emit · own 33 trinity D_emergent compliance · raw#37 transient · AGENTS.md friendly preset*
