# H_1812 REG-DICTAUX (303M) — RESULT (N6+N7 trunk-objective lever vs ce_marginal control)

> Engine-native verdict path = `cli/evaluate.py` → `core/g_gates.py` (torch-free numpy decode
> ← `core/clm_decode.py`) = TERMINAL-eligible (a_engine_native_learning 공인 py 2-production).
> torch-side training metrics (lossF / val_CE / dict_recon / dbes) = DIRECTIONAL monitors.

## 설정 (frozen · PREREG.md)
- arch = CLMConvMoE **L4 · d3784 · E2→E3** (mitosis mid-split) + savant golden-zone cusp anneal
  = `cli/train.py --canon`. 345.665M params, `.clm` 176584498 B.
- corpus = clean 언어검증 4칸 register (`state/clm303_clean_corpus/{gen,sns}_{ko,en}.txt`,
  proportional 샘플, val_frac=0.05).
- **steps = 2000** (matrix run by parallel agent on the shared A40 pod; PREREG spec'd 4000 for
  N6 floor-exclusion — see caveat below).
- seed = 4307 (single-seed; PREREG multiseed {4307,4308,4309} deferred under host contention).
- 하드웨어 = vast A40 (CUDA 12.4, torch 2.5.1+cu124), shared pod (clitrain-devresident).
- arms: ce_marginal (control) · n6_grok (N6 정규화 band) · n7_dictaux (N7 dict-aux λ0.05) ·
  n6n7 (N6+N7 주 레버). [n8_jamo / n1_tlora = 2차, 미실행.]

## 1. 학습-side held-out DESCENT (torch F.cross_entropy · DIRECTIONAL monitor)

**모든 arm 4/4 register DESCENT (overfit 없음 · uniform=ln256=5.5452 대비 전부 하강):**

| arm | lossF | val_pooled | ko-gen | en-gen | ko-sns | en-sns | DESCENT |
|-----|-------|-----------|--------|--------|--------|--------|---------|
| ce_marginal | 1.168 | 0.665 | 0.194 | 0.334 | 1.319 | 0.812 | **4/4** ✅ |
| n6_grok | 1.173 | 0.940 | 0.340 | 0.540 | 1.489 | 1.393 | **4/4** ✅ |
| n6n7 | 1.165 | 0.958 | 0.331 | 0.574 | 1.476 | 1.449 | **4/4** ✅ |
| n7_dictaux | 1.184 | 0.961 | 0.349 | 0.568 | 1.488 | 1.439 | **4/4** ✅ |

- H_1579 overfit 함정 회피 확인: lossF≈1.17 (암기 아님) + held-out 4/4 DESCENT (일반화).
- 주의: ce_marginal held-out CE 가 *가장 낮음* (0.665 vs 0.94–0.96) — 2000-step 에선 N6 정규화가
  CE 상으로는 아직 grok 이득 없음 (정규화는 train-fit↓ generalization 의 표준 trade-off). N6 의
  표적은 CE 가 아니라 **G1 재조합** (아래 엔진-네이티브).

## 2. 엔진-네이티브 G0-G6 (`cli/evaluate.py` --gen 80 · TERMINAL, torch-free numpy)

frozen bars (ARCHITECTURE.json): G0 kwr≥0.50 on ≥4/5 · G1 best_distinct≥2 ∧ >max_single ·
G2 novel≥3 ∧ control=0 · G6 distinct≥5 ∧ fals≥1.

| gate | ce_marginal (control) | n6n7 (N6+N7 主) | n6_grok | n7_dictaux |
|------|----------------------|------------------|---------|------------|
| G0 COHERENCE | 🔴 2/5 | 🟢 **4/5 PASS** | 🔴 2/5 | 🔴 3/5 |
| **G1 RECOMBINATION** | 🔴 best_distinct=**0** | 🔴 best_distinct=**1** | 🔴 best_distinct=**0** | 🔴 best_distinct=**0** |
| G2 NOVELTY | 🔴 novel=0 | 🔴 novel=0 (coherent=19) | 🔴 novel=0 | 🔴 novel=0 |
| G3 (read) | ✅ cont=0.99995 | ✅ cont=0.99995 | ✅ | ✅ |
| G5 NON-FAB | 🔴 fab=0.493 | 🔴 fab=0.468 | 🔴 fab=0.556 | 🔴 fab=0.494 |
| **G6 IDEATION ★** | 🔴 dist=4·**fals=0** | 🔴 dist=**5**·**fals=0** | 🔴 dist=**3**·fals=0 | 🔴 dist=**0**·fals=0 |
| CLOSURE (G0∧G1∧G2) | 🔴 FAIL | 🔴 FAIL | 🔴 FAIL | 🔴 FAIL |

**ABLATION (N6 단독 vs N7 단독 — 둘 다 floor, lift 는 COMBINATION 에서만):**
- **n6_grok (N6 정규화 단독)** = control floor 이하 (G1=0, G6 dist=3 < control 4, G0 2/5).
- **n7_dictaux (N7 dict-aux 단독)** = control floor 이하 (G1=0, G6 dist=**0** ≪ control 4, G0 3/5).
- **→ N6 단독·N7 단독 둘 다 lift 0 (오히려 G6 악화).** n6n7 의 directional lift(G1 0→1·G6 4→5·G0 2/5→4/5)는
  **N6 도 N7 도 아닌 둘의 INTERACTION(synergy)** 에서만 나온다 — additive 아닌 super-additive 상호작용
  (각 단독은 floor, 결합만 신호를 띄움). 단일 component 귀속 불가.

## 3. LIFT (frozen · PREREG) — n6n7 vs ce_marginal control

**n6n7 가 control 대비 표적 metric 에서 directional LIFT (예측 방향) — 단 frozen bar 미달:**
- G1 best_distinct: **0 → 1** (⬆️ +1, bar=≥2 미달) — 재조합 신호가 *움직였다* (flat floor 아님).
- G6 distinct: **4 → 5** (⬆️ +1, bar=≥5 *도달*); fals: **0 → 0** (= floor, bar=≥1 미달).
- G0 coherence: **2/5 → 4/5** (⬆️ PASS) — 정규화/dict-aux 가 byte-coherence 개선.
- G2/G5 ≈ 동일.
- **LIFT 판정(PREREG strict): G1 best_distinct 0→1 strictly 증가 ✅ · G6 fals 0→0 미증가 ❌.**
  G1-축 directional LIFT 는 *있으나*, 어느 것도 frozen bar 통과 못함.

## 4. 정직 verdict

**H_1812-main (N6+N7) = NOT-SUPPORTED at frozen bar, but DIRECTIONAL-positive (not flat floor).**
- N6+N7 trunk-objective 레버는 ce_marginal 대비 **G1 best_distinct 0→1, G6 distinct 4→5, G0 2/5→4/5 로
  예측 방향으로 밀었다** — H_1602 의 "objective-축 flat floor(전부 0)"와 **대조**: 정규화 band + dict-aux 가
  재조합 신호를 *바닥에서 떼어냈다*(0→1). 그러나 G1 bar(≥2)·G6 fals bar(≥1)를 **넘지 못함** → frozen bar
  기준 NOT-SUPPORTED.
- **INTERACTION(synergy)이 lift 의 원천** — ablation 이 결정적: N6 단독·N7 단독 *둘 다 floor*(오히려 G6 악화:
  N6 dist=3, N7 dist=0, 둘 다 control 4 보다 낮음)인데 **결합(n6n7)만 G1 0→1·G6 4→5·G0 2/5→4/5**.
  즉 lift 는 어느 한 component 의 효과가 아니라 **super-additive 상호작용** — "정규화 band 가 grok 으로 데려간
  manifold 위에서 dict-aux 가 재조합 표현을 짜낸다"는 결합 가설과 정합. 단일 레버로는 단순화 불가.
- **핵심 질문 답(undertrain floor vs 구조벽): 부분적으로 undertrain (interaction-gated)** — 결합 레버로
  신호가 0→1 움직였으니 완전한 구조 천장은 아니다. 단 2000-step·single-seed·bar 미달이라 "정규화+aux 로
  충분히 열린다"고도 못함 = 방향은 맞으나 강도 부족(lever real but underpowered at this step budget).
  PREREG 명시 **4000-step (N6 floor-exclusion 완전판)** 재측정이 이 모호성(결합 lift 0→1 이 큰 step 에서
  →2+ 되나)을 가르는 결정 follow-on.
- DIRECTIONAL 정직 메모: 측정 = 공인 py 2-production `core/g_gates.py`(torch-free numpy) = 엔진-네이티브
  TERMINAL-eligible. 단 single-seed + 2000-step(PREREG 4000 미달)이므로 "확정 천장" 박제 금지 —
  directional NOT-SUPPORTED + 4000-step ING follow-on.
- 협업 메모: 학습 matrix 는 같은 pod 의 병렬 에이전트가 2000-step 으로 돌렸고, 본 에이전트가 (a) py
  2-production 엔진 복원(이 브랜치 누락분) → 병렬 에이전트의 깨진 eval(rc=1) unblock, (b) 엔진-네이티브
  G0-G6 verdict + ablation 격리 + ckpt 회수를 담당. eval 은 BLAS-oversubscription(4-parallel thrash)
  진단 후 serial+16thread-cap 으로 정상화(load 282→48).

## 5. ckpt (a_fire_recover_complete — pulled, sha256)
- ce_marginal_seed4307.clm  sha256 adbb146c4526d7ff3065184d6c40fd9d0bd07fb4208e6a2fe65f4bb02fedeab3
- n6_grok_seed4307.clm       sha256 7a33fb23e30d18a0a42e760d22d23e28eabdb51f76a80d6872044b86a68544d6
- n6n7_seed4307.clm          sha256 c13001bd2f0e374706c5a643bda23ee85c3b0c27114b5c5713a932cb907042b2
- n7_dictaux_seed4307.clm    sha256 8bd5c216c897db5ff1289e86c5cfcd10d8d45d6e4045ed2b9bea8cdce8e26ff5
- all 176584498 B, local `state/1630_reg_dictaux/ckpt/`. torch `.pt` left on pod.

## 6. caveats (정직 스코프 · c9)
- **2000-step (not PREREG 4000)**: N6 grok floor-exclusion 가설은 4000-step 을 명시했으나 matrix 가
  2000-step 으로 돌았다 → N6 이 grok 전이를 완료할 만큼 충분한 step 인지 미확정 (under-step risk).
  4000-step 재측정은 ING follow-on.
- single-seed 4307 (multiseed 미실행 · 호스트 contention).
- 공인 py 2-production 엔진(`core/g_gates.py` torch-free numpy) = TERMINAL; 단 hexa `anima evaluate`
  cross-check 는 별도 (byte-parity).
