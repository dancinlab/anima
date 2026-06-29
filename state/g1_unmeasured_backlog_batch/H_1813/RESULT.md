# H_1813 RESULT — TPR expert-weight TLoRA (ctrl vs tlora, recomb-obj baked)

**상태: IN-FLIGHT** (pod 43098811, 6 arms in progress)

---

## 실험 설계

| 변수 | 값 |
|------|-----|
| 위치 가설 | TPR factorization in ConvMoE **expert weight** (not readout) |
| 비교 | ctrl (dense expert) vs tlora (TLoRA rank=8 + base) |
| 두 arm 공통 | recomb-objective (L_recomb, λ=0.10, composite CE) |
| 추가 공통 | next_byte_CE + aux_moe + λ_recomb·L_recomb |
| Steps | 4000 (canonical 303M d=3784 L=4 E0=2→3 bf16 bs=8 seq=1024) |
| Seeds | {7, 4302, 4303} per arm |
| 코퍼스 | 4칸 register (ko-general/en-general/ko-sns/en-sns) |
| 측정 | py 2-production g_gates.py G0-G6 (DIRECTIONAL per PREREG) |
| Frozen bar | G1: composed_distinct≥2 ∧ >max_single ∧ coherent |
| | G6: dist≥5 ∧ fals≥1 |
| LIFT 조건 | tlora > ctrl, majority ≥2/3 seeds, strict |
| pod | vast 43098811 A40 CUDA-12.2 $0.57/hr |

---

## 결과 — held-out descent

| arm | seed | val_CE (pooled) | registers_DESCENT | DESCENT? |
|-----|------|----------------|-------------------|---------|
| ctrl | 7 | 1.581 | 4/4 | ✓ (lossF=1.576, recomb_ce=1.582) |
| ctrl | 4302 | 1.622 | 4/4 | ✓ (lossF=1.557, recomb_ce=~1.58) |
| ctrl | 4303 | 1.587 | 4/4 | ✓ (lossF=1.584, recomb_ce=~1.58) |
| tlora | 7 | PENDING (training) | — | — |
| tlora | 4302 | PENDING (training) | — | — |
| tlora | 4303 | PENDING (training) | — | — |

*Note: val_CE ~1.58 is higher than prior H_162x/H_1819 arms (~0.63-0.95) — TPR expert-weight factorization reduces capacity. All 4/4 DESCENT (< 5.545 uniform). Expert routing collapses at E2→E3 mitosis (step 2000) then recovers by step 4000.*

---

## 결과 — G0-G6 (engine-native-py DIRECTIONAL)

| arm | seed | G0 kwr | G1 distinct | G1 pass? | G6 dist | G6 fals | closure |
|-----|------|---------|-------------|----------|---------|---------|---------|
| ctrl | 7 | PENDING | PENDING | — | PENDING | PENDING | — |
| ctrl | 4302 | PENDING | PENDING | — | PENDING | PENDING | — |
| ctrl | 4303 | PENDING | PENDING | — | PENDING | PENDING | — |
| tlora | 7 | PENDING | PENDING | — | PENDING | PENDING | — |
| tlora | 4302 | PENDING | PENDING | — | PENDING | PENDING | — |
| tlora | 4303 | PENDING | PENDING | — | PENDING | PENDING | — |

---

## N3 DBES expert-specialization

| arm | seed | expert_div | router_entropy | usage_gini |
|-----|------|-----------|----------------|-----------|
| ctrl | 7 | PENDING | PENDING | PENDING |
| tlora | 7 | PENDING | PENDING | PENDING |

---

## verdict (PENDING)

**결정 기준:** tlora G1 composed_distinct > ctrl G1 composed_distinct, ≥2/3 seeds, strict.

| 결론 | 조건 |
|------|------|
| SUPPORTED | tlora > ctrl G1, ≥2/3 seeds |
| NOT-SUPPORTED | 미충족 |
| INCONCLUSIVE-at-floor | 전 arm G1=0 (undertrain 의심) |

---

## 비용

- pod: vast 43098811 $0.57/hr × ~4h training + ~1h eval = ~$2.85
- expected total: ~$3-4

---

## ckpt pull 명령 (teardown 전 실행)

```sh
rsync -az -e "ssh -p 18810 -o StrictHostKeyChecking=no" \
  root@ssh1.vast.ai:~/anima/state/g1_unmeasured_backlog_batch/H_1813/ckpt/ \
  state/g1_unmeasured_backlog_batch/H_1813/ckpt/
```
