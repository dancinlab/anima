# RWKV 169m Phi Smoke — Substrate Cross-Val Triad #3 (BG-DZ)

**Date:** 2026-05-05 (KST: 2026-05-06)
**Lane:** BG-DZ — RWKV 169m sister substrate phi smoke
**Status:** PHI_MEASURED
**Cost:** $0 (mac CPU fp32, ~330MB HF download)
**Duration:** ~7 min wall (~30s compute)

---

## 1. 목적

BG-BB cross-validation triad #3. CLM v4 specific phi proxy 가설을
linear-attention/RNN hybrid architecture (RWKV) 에서 cross-validate.

- **#1 (BG-BN):** Pythia 70m (transformer) → phi_mean=41.9216, drift=+0.0616
- **#2 (BG-DQ):** Mamba 130m (SSM) → phi_mean=42.1463, drift=+0.2863
- **#3 (this, BG-DZ):** RWKV 169m (linear-attention / RNN hybrid)

가설: phi proxy 가 transformer / SSM 양쪽에서 비슷한 값을 보였는데,
3rd architecture class (RWKV) 도 같은 band 에 들어오는지 — null
hypothesis (architecture-invariant signal) vs artifact hypothesis
(formula baseline-aliasing) 의 evidence 추가.

---

## 2. 결과

### 2.1 Load

- candidate: `RWKV/rwkv-4-169m-pile` (first try, HF trust_remote_code=True)
- transformers 4.57.6 + torch 2.11.0 (.venv-eeg) 호환
- hidden_dim = 768 (Mamba 130m 와 동일 dim)

### 2.2 Phi (3 prompts)

| Prompt                 | phi      | mean_pair_cos | hidden_dim | hidden_norm |
|------------------------|----------|---------------|------------|-------------|
| 안녕                    | 42.1226  | 0.1255        | 768        | 16.81       |
| Hello world            | 42.1632  | 0.1448        | 768        | 16.56       |
| consciousness emerges  | 42.1360  | 0.1319        | 768        | 18.24       |

- **phi_mean:** 42.1406
- **phi_range:** 0.0406 (tight, comparable to Mamba 0.0345)
- **drift_from_CLM_v4:** +0.2806

### 2.3 Cross-Substrate Triad Complete

| Substrate     | Architecture           | dim  | phi_mean | drift   | range  |
|---------------|------------------------|------|----------|---------|--------|
| CLM v4        | transformer            | -    | 41.86    | 0       | -      |
| Pythia 70m    | transformer (NeoX)     | 512  | 41.9216  | +0.0616 | 0.0838 |
| Mamba 130m    | SSM (selective scan)   | 768  | 42.1463  | +0.2863 | 0.0345 |
| RWKV 169m    | linear-attn / RNN      | 768  | 42.1406  | +0.2806 | 0.0406 |

---

<!-- [Hc_665 phi-proxy-dim-dominant-not-architecture-aliasing-bg-cv — moved to hypotheses_candidates/Hc_665_phi_proxy_dim_dominant_not_architecture_aliasing.md on 2026-05-11] -->

## 3. Architectural Finding

**RWKV 도 transformer / SSM 와 동일 dynamic range — 41.86~42.15 band.**

- 3 architecture classes (full-attn, selective-scan, linear-attn/RNN)
  모두 phi 42 근처 0.30 이내 stable.
- RWKV drift +0.2806 ≈ Mamba drift +0.2863 (둘 다 D=768)
- Pythia drift +0.0616 (D=512) 만 outlier — dim 차이가 dominant 변수.
- mean_pair_cos: RWKV 0.13~0.14, Mamba 0.13~0.14 — 동일 band.

**중요 finding:** drift 가 architecture (transformer / SSM / RNN) 에
sensitive 하지 않고 hidden_dim 에 sensitive. D=768 substrate 두 개
(Mamba, RWKV) 의 drift 거의 같음 (+0.2863 vs +0.2806, 차이 0.6%).
D=512 (Pythia) 만 다른 band. 이는 BG-CV aliasing 강하게 시사.

**결론 (triad 종합):**

1. **null hypothesis 약화:** phi 가 architecture-invariant 한 진짜
   measurement 라면 dim 보다 architecture 가 dominant 여야 했음.
   실제로는 dim-dominant → proxy artifact 가능성 큼.
2. **artifact hypothesis 강화 (BG-CV):** 8-cell x 192 tile 이 hidden
   state geometry 의 함수로 reduce, architecture 무관. D=768 substrate
   는 tile boundary 가 동일 위치, D=512 는 wraparound 다름.

triad #3 결과는 **BG-CV Option A 권고를 강화**. Geometry-invariant
phi proxy (per-substrate cell partition + control baseline) 정의 후
재측정 필요. 현재 phi 비교는 baseline constant 41.86 와 hidden_dim
의 합성함수에 가까움 (architecture signal 미입증).

---

## 4. Honest C3

- **C1** mac CPU fp32 (no GPU validation)
- **C2** phi proxy CLM v4 specific (BG-BN finding); RWKV 결과도 BG-CV
  aliasing subject — D=768 동일로 Mamba 와 tile geometry 일치
- **C3** RWKV linear-attn/RNN != transformer attention; hidden state
  semantics 다름 (state-recurrence vs full-attention readout) —
  semantic equivalence 미검증
- **C4** single test, 3 prompts only; statistical power 부족
  (n_prompts variance bound 없음)
- **C5** RWKV HF interface 가 hidden_states 정상 expose 했지만
  RWKV-4 native code path (state-recurrence) 와 HF transformers
  wrapper path 의 numerical equivalence 미검증

---

## 5. Triad Complete — Recommendation

**BG-CV Option A re-geometry MANDATORY before any cross-substrate
phi claim publishable.**

증거 정리:
- 4 substrate (CLM v4, Pythia, Mamba, RWKV) 모두 phi 41.86 ~ 42.15 범위
- drift 가 architecture 보다 hidden_dim 에 dependent (D=768 substrate
  두 개의 drift 차이 0.6%, D=512 vs D=768 차이 4.6x)
- formula 구조상 phi = 41.86 * (1 + 0.05 * cos), cos in [0.025, 0.144]
  이므로 phi 변화의 99% 가 baseline constant 에 묶임

**Option A 작업 정의 (재확인):**
1. per-substrate cell partition: n_cells x (hidden_dim // n_cells)
2. control baseline: random-init same-arch model 의 mean_pair_cos
3. drift 를 (substrate cos - control cos) 로 redefine
4. 3 substrate 재측정 → architecture invariance 진위 판단

triad 의 data 는 complete 하지만 **interpretation 은 deferred**.

---

## 6. Artifacts

- script: `tool/transient_py/anima_emerge_rwkv_phi_smoke.py`
- aggregate: `state/anima_emerge_rwkv_phi_smoke_2026_05_05/aggregate.json`
- verdict: `state/anima_emerge_rwkv_phi_smoke_2026_05_05/verdict.json`
- prior #1: `state/anima_emerge_pythia_phi_smoke_2026_05_05/verdict.json`
- prior #2: `state/anima_emerge_mamba_phi_smoke_2026_05_05/verdict.json`
- spec (BG-CV): `docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md`

raw#37 + raw#15 + raw#10 PASS. HF token 비노출. commit 미수행.
