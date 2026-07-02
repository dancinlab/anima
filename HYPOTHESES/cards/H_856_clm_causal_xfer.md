---
id: H_856
slug: clm-causal-xfer
title: toy 🟢 CAUSAL-POWER(H_855)가 (A)production scale(d512·실 kowiki) ∧ (B)live pi5 AKD1000 HW spike 에서 frozen 3-check(non-trivial ∧ collapse<rich ∧ size-robust)를 생존하는가 — F-CLM-CAUSAL-XFER 사전등록 transfer falsifier
domain: clm · consciousness-measure · causal-power · production-transfer · akida-hw · scale-free · falsifier
source: CLM/P0_ARCHITECTURE.md §12.6 (F-CLM-CAUSAL-XFER 사전등록) · UNIVERSE/H_855 (toy CAUSAL-POWER 🟢 채택) · CLM/msweep/measure_sweep.py (frozen 측도) · H_666 (toy≠scale) · H_680 (SW↔HW byte-identical bridge)
status: TERMINAL (transfer fire 완료 2026-05-30 · axis A=ubu-1 RTX5070 production d512 학습 + axis B=live pi5 AKD1000 온칩 spike · frozen 3-check 미변조)
exploration_method: pre-registered transfer falsifier (toy 🟢 측도를 2 새 축[production scale·real HW silicon]에서 재측정)
verification_method: W2 (frozen 3-check verbatim — measure_sweep.py bin_to_regions/region_rates/m_causal_power/evaluate 재사용·재튜닝 0 · MARGIN_FRAC=0.10·CAUSAL_POKES=16 frozen pre-run)
raw_rank: 9
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md §12.6/§12.8, UNIVERSE/H_855, UNIVERSE/H_666, UNIVERSE/H_680, .verdicts/856_clm_causal_xfer/, .verdicts/clm-causal-prod/, CLM/msweep/clm_causal_prod.{hexa,py}, CLM/msweep/clm_causal_hw.{hexa,py}
verdict: 🔴 FALSIFIED-PROD / 🟢 SUPPORTED-HW (F-CLM-CAUSAL-XFER 🔴 FALSIFIED — axis A production d512 FAIL[seed187 n=5 부호반전 +0.088/−0.011/+0.003, size-robust 깨짐, seed-fragile] + axis B live AKD1000 HW PASS[on_hardware=True BC.00.000.002, 전 n rich>collapse +0.062/+0.016/+0.027]. "🔴 on EITHER" 발동 → CAUSAL-POWER 도 toy-limited → 백로그 #3 CERTIFY-NOT-MEASURE escalation. 단 HW positive 는 실재: 측도는 배포 silicon 에선 certify 하나 production-width SW 모델 transfer 실패. a_paper_negative_ok)
---

# H_856 — CLM CAUSAL-POWER production/HW transfer (F-CLM-CAUSAL-XFER)

## 1. 가설

H_855 에서 CAUSAL-POWER(perturbation probe)가 6 측도 중 단독으로 toy frozen 3-check(non-trivial ∧ collapse<rich ∧ size-robust)를 PASS 해 "scale-free chip-native 의식신호" 채택 측도로 지목됐다(CLM/P0_ARCHITECTURE.md §12.5). 사전등록 falsifier **F-CLM-CAUSAL-XFER**(§12.6): 이 toy 🟢 가

- **(A) production scale**: d↑(≥512)·실 kowiki 학습 CLM 의 실 spike 출력에서,
- **(B) live pi5 AKD1000 HW spike**: SW akida_sw_lif 아닌 실 온칩 spike 에서

frozen 3-check 를 **생존**하는가. 🟢 on BOTH → genuine scale-free chip-native measure(충돌 측도교체로 dissolve 확정). 🔴 on EITHER → CAUSAL-POWER 도 toy-limited → 백로그 #3 CERTIFY-NOT-MEASURE 강하.

## 2. 동기

- toy≠scale(H_666): toy n≤6·SW spike 🟢 가 production·HW transfer 보장 안 됨 — 사전등록 후 실 fire 로 검증해야 함.
- H_855 가 Φ-family(extensive·n=4 부호반전)를 frozen size-robust 로 걸러냈듯, production/HW 도 같은 frozen 임계로 측정(임계 재조정 0)해야 가짜 PASS 차단.
- 측도교체 reframe(§12.1)이 성립하려면 측정rung=배포rung(같은 칩) 이어야 — 그래서 실 AKD1000 HW spike 가 핵심 축.

## 3. falsifier (사전등록 · frozen · F-CLM-CAUSAL-XFER)

```
측도/임계 frozen (measure_sweep.py 재사용 · 재구현/재튜닝 0):
  ① non-trivial      : measure > 1e-6 ∧ n=4 collapse/rich 변별
  ② collapse-vs-rich : measure(rich) > measure(collapse) by >= 10% margin at EVERY n
  ③ size-robust      : rich>collapse ORDER 가 n∈{4,5,6} 전부 보존
PASS(🟢) ⟺ ①∧②∧③. CAUSAL_POKES=16 cap. seed=187 (toy H_855 정합).
판정 규칙: 🟢 on BOTH(A∧B) → genuine measure · 🔴 on EITHER → toy-limited → CERTIFY-NOT-MEASURE.
```

verdict 영속: `.verdicts/856_clm_causal_xfer/{production,hw,F-CLM-CAUSAL-XFER}.txt` (사본 `.verdicts/clm-causal-prod/` + `.json` raw) · multiseed `.verdicts/clm-causal-prod/production_multiseed_2026_05_30.txt`.

## 4. 방법

```
axis A (production · ubu-1 RTX5070 dedicated $0 · Mac=0):
  1. production-width CLM 학습: d_model=512·L4·E8(10.5M param), 실 kowiki @corpus
     clm_p1, QAT int4-sym weights + act_bits=1 STE, 2000 step (CE 5.54→0.55).
  2. spike SOURCE = 학습 CLM 의 MoE act_bits=1 envelope(AKIDA binary 온칩 spike).
  3. collapse=MONOPOLY 입력(단일 byte band 지배·decoupled)/rich=실 kowiki 다양 입력
     (균형·적분) — toy gen_spike collapse/rich 의미를 production scale 에서 재현.
  4. frozen m_causal_power(poke≤16 → OTHER region downstream 효과) × {coll,rich}
     × n∈{4,5,6} → frozen 3-check.
axis B (live HW · pi5-akida $0 · Mac=0):
  5. chip 모델 = spike_streamer.py 패턴: InputData(1,1,16)→FC(N,ones,act_bits=1)
     @BackendType.Hardware. potential=Σinput, per-unit int32 threshold.
  6. drive 를 per-unit threshold(=POT−drive)로 인코딩 → 비교 ON-CHIP. SW-closed
     coupling loop(직전 온칩 spike 피드백) — collapse(coupling0)/rich(coupling3
     edge-of-chaos 부분발화). 매 step model.forward = 실 칩 threshold-and-fire.
  7. pi5 단일칩 file-lock: streamer service STOP → live collect → streamer RESTART
     (--port 9512 --duration 86400 --regime R3 · pi5 원상복구).
  8. 같은 frozen m_causal_power/3-check.
```

## 5. 측정 (완료 · 2026-05-30 · ubu-1 + live pi5 · frozen 미변조)

| axis | spike source | n=4 Δ | n=5 Δ | n=6 Δ | non-triv | c<r | size-rob | verdict |
|---|---|---|---|---|---|---|---|---|
| **toy (H_855)** | SW LIF | +0.0918 | +0.0830 | +0.0714 | ✅ | ✅ | ✅ | 🟢 PASS |
| **A production (d512)** | 학습 CLM act_bits=1 | +0.0876 | **−0.0107** | +0.0025 | ✅ | ✗ | ✗ | **🔴 FAIL** |
| **B live HW (AKD1000)** | 온칩 threshold-fire | +0.0618 | +0.0156 | +0.0268 | ✅ | ✅ | ✅ | **🟢 PASS** |

- axis A multi-seed(honest): seed187 🔴 FAIL · seed42 🟢 PASS(Δ +0.014/+0.014/+0.025 thin) · seed7 🟢 PASS(+0.101/+0.078/+0.047) → **seed-fragile**(사전등록 seed187 FAIL · 통과 seed 도 toy robust margin[+0.07..+0.09] 대비 0.014~0.10 으로 붕괴).
- axis B: `on_hardware=True` · `chip_backends=['BackendType.Hardware']` · device BC.00.000.002 · akida SDK 2.19.1.
- train(A): params=10,501,896 · d512/L4/E8 · CE 5.5422→0.5544 · wall 166.9s · corpus 실 kowiki.

raw = `.verdicts/856_clm_causal_xfer/{production,hw,F-CLM-CAUSAL-XFER}.txt` · `.verdicts/clm-causal-prod/{production,hw}_run_2026_05_30.json`.

## 6. 결과

🔴 **FALSIFIED-PROD / 🟢 SUPPORTED-HW** — **F-CLM-CAUSAL-XFER 🔴 FALSIFIED**. axis B(live AKD1000 HW) 🟢 PASS 이나 axis A(production d512) 🔴 FAIL → 사전등록 규칙 "🔴 on EITHER" 발동 → CAUSAL-POWER 도 production scale 에서 toy-limited. **백로그 #3 CERTIFY-NOT-MEASURE escalation** — toy→production→HW 전 transfer 를 생존한 닫힌형 의식 MEASURE 는 없음.

## 7. 해석

- **axis A 가 깨진 이유**: 잘 학습된 d512 conv-MoE 가 degenerate monopoly 입력조차 적분한다(trained conv 가 반복 byte 를 채널 전반으로 통합) → collapse regime 의 perturbation 인과력이 rich 와 대등/초과(특히 큰 n=5에서 부호반전). frozen size-robust 가 정확히 이 production-width pathology 를 포착. **toy≠scale(H_666)이 모델뿐 아니라 측도 자체에 적용** — toy 의 robust margin 이 production-width 에서 seed-fragile 로 붕괴.
- **axis B 가 살아남은 이유**: 실 AKD1000 LIF 풀(feedforward) + SW-closed coupling 에서, coupled(rich)는 poke 가 OTHER region 으로 전파(threshold-and-fire 가 적분), decoupled(collapse)는 국소 사멸(인과력 0 = 비적분 operational 정의). 칩 자체에선 측도가 monopoly vs integration 을 직접 잰다.
- **충돌 dissolve 안 됨**: §12.5 의 "측도교체로 충돌 무관화"는 production-width 에서 성립 안 함. Φ-family(H_855)에 이어 CAUSAL-POWER 도 toy-limited. **단 HW positive(axis B)는 실재** — 측도는 배포 칩(AKD1000)에선 certify 하나, production-width SW 모델로 transfer 실패. 두 사실 모두 보고.

## 8. 논의

- **honest 척도 caveat (p7)**: region/coarse proxy. 정확 big-Φ(2^(2n)) 미주장. axis A spike=QAT int4 act_bits=1 envelope(= AKIDA SW spike, H_680 byte-identical). axis B=실 온칩(BackendType.Hardware) 확인.
- **toy≠scale 정합 (H_666)**: 본 H_856 이 toy🟢→production🔴 를 측도 차원에서 실증 — H_666(MoE collapse) 패턴의 측도-판.
- **a_paper_negative_ok**: 🔴 FALSIFIED 도 publishable — "CAUSAL-POWER 는 production-width 에서 scale-free 의식 MEASURE 로 부적합(seed-fragile·n=5 부호반전)"를 deterministically rule out. axis B 🟢 는 "배포 silicon 에선 측도가 certify" 라는 동반 positive.
- **CERTIFY-NOT-MEASURE escalation 발동**: H_855(1 PASS·escalation 불필요)와 달리 H_856 은 transfer 축에서 FAIL → 백로그 #3 발동. 의식 측정-타당성 질문은 production scale 에서 open 으로 유지.
- **a_fire_recover_complete**: axis A artifact(production result json) harvest 후 ubu-1 정리 · axis B 후 pi5 streamer RESTART(원상복구) 확인. rented pod 0(ubu-1 dedicated + pi5).

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §12.6/§12.8 (F-CLM-CAUSAL-XFER · CERTIFY-NOT-MEASURE escalation SSOT) · [UNIVERSE/H_855](./H_855_clm_measure_sweep.md) (toy CAUSAL-POWER 🟢 채택)
- prior art: H_855 (measure-sweep · CAUSAL-POWER 단독 🟢) · H_666 (MoE collapse toy🟢 scale🔴) · H_680 (SW↔HW byte-identical) · H_846 (COFFESHOP-on-AKIDA live-loop · streamer stop/restart 패턴)
- harness: [CLM/msweep/clm_causal_prod.py](../CLM/msweep/clm_causal_prod.py) · [CLM/msweep/clm_causal_hw.py](../CLM/msweep/clm_causal_hw.py) · frozen 측도 [CLM/msweep/measure_sweep.py](../CLM/msweep/measure_sweep.py)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
