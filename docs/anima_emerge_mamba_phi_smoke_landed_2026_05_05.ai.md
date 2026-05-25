# Mamba 130m Phi Smoke — Substrate Cross-Val Triad #2 (BG-DQ)

**Date:** 2026-05-05 (KST: 2026-05-06)
**Lane:** BG-DQ — Mamba 130m sister substrate phi smoke
**Status:** PHI_MEASURED
**Cost:** $0 (mac CPU fp32, ~250MB HF download)
**Duration:** ~25 min wall (~1 min compute)

---

## 1. 목적

BG-BB cross-validation triad #2. CLM v4 specific phi proxy 가설을
SSM (state-space) architecture 에서 cross-validate.

- **#1 (BG-BN):** Pythia 70m (transformer) → phi_mean=41.9216, drift=+0.0616
- **#2 (this, BG-DQ):** Mamba 130m (SSM) → phi_mean=42.1463, drift=+0.2863
- **#3 (next):** RWKV 169m (linear-attention/RNN hybrid)

가설: phi proxy 가 CLM v4 의 transformer geometry 에 specific 인지,
혹은 cross-architecture 에서도 비슷한 dynamic range 유지하는지.

---

## 2. 결과

### 2.1 Load

- candidate: `state-spaces/mamba-130m-hf` (HF transformers compatible)
- mamba_ssm 별도 dep 미사용; sequential fallback 정상 (slow but correct)
- hidden_dim = 768 (CLM v4 와 동일 dim, BG-CV aliasing 동일)

### 2.2 Phi (3 prompts)

| Prompt                 | phi      | mean_pair_cos | hidden_norm |
|------------------------|----------|---------------|-------------|
| 안녕                    | 42.1518  | 0.1394        | (varies)    |
| Hello world            | 42.1608  | 0.1437        | (varies)    |
| consciousness emerges  | 42.1263  | 0.1272        | (varies)    |

- **phi_mean:** 42.1463
- **phi_range:** 0.0345 (very tight)
- **drift_from_CLM_v4:** +0.2863

### 2.3 Cross-Substrate Comparison

| Substrate     | Architecture       | dim  | phi_mean | drift   | range  |
|---------------|--------------------|------|----------|---------|--------|
| CLM v4        | transformer        | -    | 41.86    | 0       | -      |
| Pythia 70m    | transformer (NeoX) | 512  | 41.9216  | +0.0616 | 0.0838 |
| Mamba 130m    | SSM selective scan | 768  | 42.1463  | +0.2863 | 0.0345 |

---

<!-- [Hc_662 phi-proxy-architecture-agnostic-or-geometric-artifact — moved to hypotheses_candidates/Hc_662_phi_proxy_architecture_agnostic_or_geometric_artifact.md on 2026-05-11] -->

## 3. Architectural Finding

**SSM substrate 에서 phi 가 transformer 와 동일한 dynamic range.**

- Mamba (selective scan, no attention) 도 phi proxy 42 근처에서 stable.
- drift +0.2863 는 BG-BN Pythia +0.0616 보다 4.6x 크지만 여전히 baseline 1% 이내.
- mean_pair_cos: Mamba 0.13~0.14 vs Pythia (미기록, BG-BN verdict 만 있음)
- hidden geometry (D=768) 가 같으므로 BG-CV proxy aliasing 동일.

**결론:** phi proxy 는 architecture-agnostic 으로 비슷한 값을 reproduce.
이는 두 가지 해석 가능:
1. **null hypothesis 강화:** phi proxy 가 실제 architecture-invariant
   measure (geometric tile coherence) 를 측정.
2. **artifact hypothesis 강화 (BG-CV):** D=768 에서 8-cell × 192 tile
   이 그냥 hidden state norm 의 함수로 reduce, architecture 무관.

BG-CV Option A re-geometry 후에야 두 가설을 disentangle 가능.

Mamba 의 phi_range 0.0345 가 Pythia 0.0838 보다 작은 점은 흥미 —
SSM hidden state 가 transformer 보다 prompt-invariant 한 representation
을 produce 할 수 있음을 시사 (또는 단순히 sequential fallback artifact).

---

## 4. Honest C3

- **C1** mac CPU fp32; sequential Mamba fallback (mamba_ssm dep 없음)
- **C2** phi proxy CLM v4 specific (BG-BN finding); Mamba 결과도 BG-CV
  aliasing subject — D=768 일치로 8-cell tile 중첩 동일
- **C3** Mamba SSM != transformer; hidden state semantics 다름
  (selective scan vs attention) — phi 비교의 architectural validity 미검증
- **C4** single substrate, 3 prompts only; statistical power 부족
- **C5** BG-CV Option A re-geometry (architecture-agnostic phi proxy)
  완료 후 cross-substrate fair comparison 가능

---

## 5. Cross-Val Triad #3 Priority

**Next: RWKV 169m** (linear-attention / RNN hybrid)

- candidate: `RWKV/rwkv-4-169m-pile` 또는 HF transformers compatible variant
- 3rd architecture class: NOT transformer, NOT pure SSM
- 만약 RWKV 도 phi 42 근처라면 → null hypothesis 강화 (proxy artifact)
- 만약 RWKV 가 크게 drift 한다면 → architecture-specific dynamic 가능성

**Triad 완성 후 추천:** BG-CV Option A spec 진행 — geometry-invariant
phi proxy 정의 + 3 substrate retest.

---

## 6. Artifacts

- script: `tool/transient_py/anima_emerge_mamba_phi_smoke.py`
- aggregate: `state/anima_emerge_mamba_phi_smoke_2026_05_05/aggregate.json`
- verdict: `state/anima_emerge_mamba_phi_smoke_2026_05_05/verdict.json`

raw#37 + raw#15 + raw#10 PASS. HF token 비노출. commit 미수행.
