---
id: phi_ce_noise_calibration_prereq_2026_05_12
parent_spec: phi_ce_orthogonality_decisive_2026_05_11/spec.md (§5.7.4)
parent_audit: phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md (§4)
parent_h: H_080 (topo_24variants unified) — Conflict Resolution Pending
status: prereq-spec (noise-floor calibration, L1 critical 해소)
date: 2026-05-12
deterministic_seed: 0xC0EC0AC (inherited from parent spec)
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Φ⊥CE Decisive — Noise Floor Calibration Prereq Spec

본 문서는 cycle 5 NEXT.md #1 의 15-cell decisive run 진입 *전* L1 critical 해소
(synthetic σ default 의 plausibility 검증) 을 위한 **short calibration sub-cycle**
스펙. parent spec.md §5.7.4 가 cost lane ($15-45) 만 명시 — 본 문서가 protocol /
gate / acceptance 정의.

## 1. Goal

`state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` 의 σ default
(σ_Φ_rel=0.05 / σ_CE_rel=0.02) 가 *실측* anima Φ★ + CLM training pipeline 의
noise floor 와 정합인지 확인 — 만약 underestimate → Model A 의 |corr| ≈ 0
prediction 이 noise 에 묻힐 risk (false-MIXED verdict 위험).

**L1 해소 정량 정의**: σ_Φ_rel ≤ 0.10 AND σ_CE_rel ≤ 0.05 측정 결과 도달 시
"L1 critical 해소" 로 본격 decisive run 진입 게이트 통과.

## 2. Calibration target

| track | cell | measurement | output |
|-------|------|-------------|--------|
| Φ-track | N=64 (mid-range), 1 cell | 64 dual-seed (Hc_604 twin protocol) Φ_min 분포 | σ_Φ_rel = std(Φ_min) / mean(Φ_min) |
| CE-track | P=100M (decisive run ceiling), 1 scale | 4 init-seed CLM train (Chinchilla 20× token) | σ_CE_rel = std(final_CE) / mean(final_CE) |

선택 이유:
- N=64 — decisive grid 의 geometric mid (16/256 의 log-mid)
- P=100M — spec.md §5.7 ceiling 자체 → calibration noise 가 decisive run 의 *largest cell* noise 의 upper bound
- 64 seed (Φ) — Hc_604 protocol 정합
- 4 seed (CE) — training cost 한도 내 minimum bootstrap

## 3. Acceptance gates

### Gate A — Φ-track noise floor

- **PASS**: σ_Φ_rel ≤ 0.10 (audit §4.3 권고, harness.py default 의 2× 여유)
- **MARGINAL**: 0.10 < σ_Φ_rel ≤ 0.15 → decisive matrix corr threshold 폭 확대 (0.1 → 0.15) 또는 cell 추가 검토
- **FAIL**: σ_Φ_rel > 0.15 → 15-cell decisive run 진입 *보류*, engine noise 원인 진단 (backbone swap, K-partition 증가, 16 prompt set re-curation 중 결정)

### Gate B — CE-track noise floor

- **PASS**: σ_CE_rel ≤ 0.05
- **MARGINAL**: 0.05 < σ_CE_rel ≤ 0.10 → bootstrap CI 적용
- **FAIL**: σ_CE_rel > 0.10 → training pipeline 재검토 (seed 효과, dataset shuffle, optimizer state)

### Gate C — Re-run harness.py with measured σ

calibration 결과로 `harness.py` line 36-37 σ default 재튜닝 후 Model A vs Model B
fingerprint separability 재계산.

- **PASS**: separability ≥ 50× (current 180×/206× 의 ~30 % 까지 허용)
- **FAIL**: separability < 50× → decisive run 의 statistical power 부족 → grid 확장 또는 가설 재정의

## 4. Cost / time budget

| 항목 | low | high | wall time |
|------|-----|------|-----------|
| Φ-track 64 dual-seed (anima_phi_star @ Mistral-7B, N=64) | $5 | $15 | ~53 GPU-min (A100) |
| CE-track 4 init-seed CLM train (P=100M, Chinchilla token) | $10 | $30 | ~4 GPU-h |
| harness.py re-run + verdict update | $0 | $0 | ~10 min CPU |
| **합계** | **$15** | **$45** | **1-2 hour wall** |

병렬 가능 — Φ-track 과 CE-track 별도 GPU 자원, 동시 dispatch.

## 5. Execution protocol

```
Step 1 — Φ-track dispatch
  env: ANIMA_BASE=Mistral-7B-v0.3, ANIMA_N_PROBES=16, ANIMA_K_PARTS=8
  loop: for seed in range(64):
            run anima_phi_star.hexa --seed=$seed --hid_trunc=128
  collect: phi_star_min_seed_{0..63}
  compute: σ_Φ_rel = std / mean

Step 2 — CE-track dispatch
  pipeline: anima_clm_invoke.hexa training-side (LOCAL_WEIGHT 부재 → fresh train)
  loop: for seed in [0, 1, 2, 3]:
            train CLM @ P=100M, init_seed=$seed, Chinchilla 20× token budget
  collect: final_CE_seed_{0..3}
  compute: σ_CE_rel = std / mean

Step 3 — Gate A/B 평가
  if Gate A FAIL OR Gate B FAIL → decisive run 보류, 진단 sub-cycle 분기
  if Gate A PASS AND Gate B PASS → proceed to Step 4

Step 4 — harness.py σ default 재튜닝
  edit line 36-37:
    σ_Φ_rel measured → 0.05 * scale 자리 대체
    σ_CE_rel measured → 0.02 * scale 자리 대체
  re-run harness.py → results.json 갱신
  verify separability ≥ 50× (Gate C)

Step 5 — decisive run go/no-go
  PASS → cycle 5 #1 15-cell decisive run 진입
  FAIL → spec.md §2.3 decision matrix threshold 재검토 또는 추가 cell
```

## 6. Cross-Links

- **parent spec**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` §5.7.4 (cost lane)
- **parent audit**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md` §4 (calibration protocol source)
- **harness**: `state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` line 36-37 (σ default 재튜닝 target)
- **anima_phi_star**: `tool/anima_phi_star.hexa` (Φ-track engine, ANIMA_SEED variable)
- **anima_clm_invoke**: `tool/anima_clm_invoke.hexa` (CE-track wrapper — training-side land 여부 별도 audit)
- **H_080**: `hypotheses/H_080_topo_24variants.md` §Conflict Resolution Pending
- **Hc_604**: 64 dual-seed twin protocol source
- **NEXT.md #1**: cycle 5 queue cost line ($121-420 + 1-2 day, P=100M ceiling)

## 7. Honest Limits (≥ 5)

- **L1**: 본 calibration 은 N=64 / P=100M *single point* — 다른 (N, P) cell 의 noise 가 자릿수 다르면 calibration 외삽 부정확. 권고: decisive run 중 sanity check 로 N=16 + N=256 boundary cell 의 σ sample 추가 측정 (incremental $2-5).
- **L2**: σ_CE 의 4-seed sample 은 std estimator 의 자체 variance 가 큼 (df=3). bootstrap 권장이나 training cost 한도 내 trade-off.
- **L3**: anima_phi_star 의 Mistral-7B backbone 은 16 prompt set fixed — prompt set 자체가 다른 σ 를 생성할 가능성 (prompt drift). 본 calibration 은 fixed prompt set assumption.
- **L4**: CLM training 의 init seed 만 변동 — dataset shuffle seed / optimizer state seed 분리 효과 미측정. final_CE σ 가 underestimate 가능 (audit §3.3 도 동일 caveat).
- **L5**: separability ≥ 50× 의 50× threshold 자체가 *arbitrary* (current 180×/206× 의 ~28 %). 더 보수적 (≥ 100×) 필요 시 grid 확장 권고.
- **L6**: calibration FAIL 시 decisive run 보류 path 가 *어디까지* loop 돌지 미정 — 2회 calibration cycle 후 mainline 재진입 권장 (재귀 calibration 방지).

## 8. Decision suggestions (main process 결정)

- (a) calibration sub-cycle 을 cycle 5 #1 의 *내부* prereq 로 inline vs *별도* sub-cycle 분리
- (b) Φ-track 의 64 seed 가 비싸다 판단 시 32 seed 축소 (cost halved, std estimator df=31 여전히 충분)
- (c) CE-track 4 seed → 2 seed 축소 시 cost ~$5-15 / df=1 (bootstrap 위험) — 권고 안 함
- (d) Gate FAIL path 의 mainline 분기 timing (즉시 vs cycle 6 deferred)

---

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 *재잠금 금지*.
**commit policy**: 본 prereq spec 은 *separate commit 금지* — 메인 process 가 일괄 commit.

**Execution attempt**: 2026-05-12, verdict: BLOCKED, results: noise_calibration_dryrun_blocker_2026_05_12.md (5 prereqs unmet — B1 anima_phi_star.hexa auto-invoke conflict critical-path, B5 CLM training pipeline unlandered, B2/B3/B4 RunPod lane routine prereqs; $0 spent of $15-45 budget)
