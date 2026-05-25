---
verdict_id: nexus6_1013lens_k10_cascade_smoke_2026_05_12
spec_id: nexus6_1013lens_activation_2026_05_11
parent_verdict: state/nexus6_1013lens_activation_2026_05_11/k10_reimpl/phase1_verdict_2026_05_12.md
target_h: H_135 (DD166 NEXUS 1013-lens discovery engine)
status: K=10 smoke PASS — C1/F1/F2 all PASS (3/3), legit-axis-differentiation
cycle: 6 §S (NEXT.md §4 cascade entry)
authored: 2026-05-12
authored_by: agent
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Verdict — K=10 Cascade Smoke Actual Run (NEXT.md §4)

cycle 6 §S NEXT.md §4 의 K=10 reimpl cascade *actual measurement* 실행 결과. Phase 1 verdict (`phase1_verdict_2026_05_12.md`) 의 v2 lens 10건 + F-reimpl-1/2/3 PASS 완료 후, deterministic seed cascade smoke 1건 entry.

## 0. TL;DR

- **C1 PASS** (pos_ratio=1.0 ≥ 0.6; phi_mean=0.408 > 0)
- **F1 NOT TRIPPED** (pos_ratio=10/10 > 4/10 floor; F1 falsifier silent)
- **F2 NOT TRIPPED** (cross_lens_agreement_stub=1.0 ≥ 0.50; K=50 binding only — at K=10 informational PASS)
- **gates: 3/3 PASS** → K=10 smoke step of spec §4 C1 cascade chain CHARGED for cycle 6.
- Wall: 251 ms total, 25.1 ms/lens — well under 30 min hard ceiling.
- Cost: $0 CPU (no Mistral-7B forward, no RunPod) — `~/.hx/bin/hexa` subprocess loop only.

## 1. Run Parameters

| field | value |
|-------|-------|
| spec_id | nexus6_1013lens_activation_2026_05_11 |
| K | 10 |
| lens_dir | `state/nexus6_1013lens_activation_2026_05_11/k10_reimpl/` (v2 + bare-name back-compat) |
| whitelist | spec §3.1 canonical 10 (info/causal/consciousness/thermo/quantum/topology/gravity/network/scale/stability) |
| whitelist_source | `spec §3.1 canonical K=10 (2026-05-11)` |
| seed | `ANIMA_LENS_SEED=1762741476` (canonical label `0xnexus6smoke` mapped to int via stable sum-of-char-codes × 1234567 — see `run_k10_cascade_smoke.sh`) |
| input modality | state (B=1, S=256) — LCG-synthesized fallback |
| hexa runner | `/home/summer/.hx/bin/hexa` (Linux x86_64 elf) |
| aggregator | `tool/anima_nexus_1013lens_cascade.hexa` (cycle 5 §4 #H rename) |
| run script | `state/.../k10_reimpl/run_k10_cascade_smoke.sh` |
| raw output | `state/.../k10_reimpl/k10_cascade_smoke_results_2026_05_12.json` |
| timestamp | 2026-05-12 (cycle 6 §S) |

## 2. Per-Lens Scores (sorted desc)

| rank | lens | score | hits/total | elapsed_ms | axis kernel |
|-----:|------|------:|:----------:|----------:|-------------|
| 1 | core_quantum | 0.707 | 6/8 | 17 | density-matrix off-diagonal coherence + Bell pair proxy |
| 2 | core_network | 0.588 | 6/8 | 19 | clustering coef + density on threshold graph (V=16) |
| 3 | core_stability | 0.561 | 6/8 | 16 | Lyapunov \|Δx\| log-rate + fixed-point convergence |
| 4 | core_thermo | 0.492 | 4/8 | 16 | windowed entropy production + mean occupancy |
| 5 | core_topology | 0.463 | 4/8 | 90 | Betti-0 over level-set filtration {0.2,0.4,0.6,0.8} quantiles |
| 6 | core_scale | 0.461 | 4/8 | 32 | multi-scale entropy + Hurst proxy |
| 7 | core_consciousness | 0.400 | 4/8 | 13 | IIT bipartition phi + 4-block integration |
| 8 | core_gravity | 0.400 | 4/8 | 15 | discrete Laplacian Ricci proxy + metric norm |
| 9 | core_info | 0.010 | 2/8 | 16 | Shannon entropy + MI(x; uniform) (histogram B=16) |
| 10 | core_causal | 0.002 | 2/8 | 12 | lag-1 transfer-entropy proxy −0.5·log(1−r²) |

- **score range**: [0.002, 0.707] — axis-specific differentiation 명확 (cycle 5 §3 #A canonical 의 모든 lens=1.0 trivial 과 정성적 대비).
- **mean(phi_lens) = 0.408**, std = 0.219 — phi_mean > 0 axis acceptance 충족.
- **top-3**: quantum / network / stability (smooth-vs-rough axis 의 강한 신호 cluster — Phase 1 verdict §2.2 의 causal↔gravity↔scale cluster 와 동일 family).

## 3. Gate Application (C1 / F1 / F2)

### 3.1 C1 — spec §3 K=10 acceptance + §4 C1 cascade chain entry

| sub-gate | criterion (spec §3 / §4) | actual | verdict |
|----------|--------------------------|--------|:-------:|
| C1-a | `mean(phi_lens) > 0` (sign-aware, spec §3) | 0.408 | PASS |
| C1-b | `Φ_lens > 0` 비율 ≥ 6/10 (spec §3 K=10 smoke) | 10/10 | PASS |
| C1-c | `cross_lens_agreement_K ≥ 0.55` (spec §3 K=10 floor) | 1.0 (sign-pair stub; all positive scores) | PASS |
| C1-d | aggregator `c1_cascade_gate` (pos_ratio ≥ c1_floor(K=10)=0.6 + phi_mean > 0) | True | PASS |
| C1-e | C3 no-mislabel-drift (whitelist matches §3.1) | binding 10/10 file-path 매칭 | PASS |

**C1 verdict = PASS** (5/5 sub-gates). spec §4 C1 SMOKE-TO-PILOT CASCADE 의 step 1 (K=10) CHARGED — K=25 진입 가능 (cascade_k25_plan §0 prereq 이미 충족).

### 3.2 F1 — spec §5 K=10 falsifier (discovery engine 가속 가설 sink)

| criterion (spec §5 F1) | actual | trip? |
|------------------------|--------|:-----:|
| K=10 smoke 에서 Φ_lens > 0 비율 ≤ 4/10 → trip | pos_ratio=10/10 (≫ 4/10 ceil) | **NO** |

**F1 verdict = NOT TRIPPED (PASS)**. Hc_586 1000x+ 가속 주장 의 "wrong direction" sink 조건 미충족 — 본 smoke 결과는 Hc_586 의 partial resume status (`candidate-unverified-partial-resume-K10-PASS-2026-05-12`, phase1_verdict §11) 와 일관.

### 3.3 F2 — spec §5 K=50 binding (lens random-walk null)

| criterion (spec §5 F2) | binding at K | actual | trip? |
|------------------------|:-----------:|--------|:-----:|
| `cross_lens_agreement < 0.50` → trip | K=50 binding | 1.0 (sign-pair stub at K=10) | **NO** (informational) |

aggregator 의 `cross_lens_agreement_stub` 는 pairwise sign agreement — 모든 10 lens score > 0 이므로 stub=1.0. spec §5 F2 는 K=50 binding 으로 K=10 smoke 에서는 informational; nonetheless 1.0 ≫ 0.50 floor → F2 **NOT TRIPPED**.

**Caveat (Phase 1 verdict §5 carry-over)**: `cross_lens_agreement_stub` 의 sign-pair stub 정의는 *score > 0* 부호만 비교 — 진정한 K-NN agreement (spec §2.4) 는 K=25/K=50 scope (cascade_k25_plan §3.1 Agent #I null synthesis 미결). Phase 1 verdict §2.2 의 signed Pearson r matrix (mean off-diag |r|=0.459) 가 *real* axis differentiation 입증 — stub 1.0 이 trivial 복제본의 산물이 *아님*을 보강.

## 4. Gate Pass Count Summary

```
C1: PASS  (5/5 sub-gates)
F1: PASS  (NOT TRIPPED)
F2: PASS  (NOT TRIPPED — informational at K=10)
─────────────────────────────────────────────
gate_pass_count = 3/3  →  K=10 smoke step CHARGED
```

## 5. Comparison — Canonical (cycle 5 §3 #A) vs Phase 1 v2 vs Smoke (this run)

| metric | canonical (TRIVIAL) | Phase 1 v2 sin (cycle 6 §Q) | smoke seed=1762741476 (이 run) |
|--------|---------------------:|---------------------------:|-------------------------------:|
| phi_mean | 1.000 | 0.560 | 0.408 |
| phi_std | 0.000 | 0.279 | 0.219 |
| pos_ratio | 1.00 | 1.00 | 1.00 |
| score range | [1.0, 1.0] | [0.040, 0.971] | [0.002, 0.707] |
| input modality | none | embed/state (sin file) | state (LCG seed=1762741476) |
| F-reimpl-1 verdict | TRIVIAL (dynamic range=0) | PASS (0.40) | inherited PASS |
| top-1 lens | (tied 1.0) | core_consciousness (0.971) | core_quantum (0.707) |
| total wall ms | 132 | 2604 | 251 |

본 smoke 는 Phase 1 verdict 의 sin/highnoise/lownoise 3 profile 중 highnoise 와 가장 가까움 (LCG seed → uniform-like dist). 모든 lens score axis-specific 으로 분화 — TRIVIAL 복제본 finding 없음.

## 6. Honest Limits (L1–L4)

- **L1**: 본 smoke 는 *단일 seed* (1762741476) — spec §4 C5 REPRODUCIBLE SEED 의 ≥3 seed 부호 보존은 cycle 7 scope. F5 falsifier (seed 변경 시 부호 보존 < 70% → frontmatter false) 는 본 run 미적용.
- **L2**: aggregator `cross_lens_agreement_stub=1.0` 는 sign-pair 만 — 진정한 K-NN agreement (cascade_k25_plan §3.1) 는 stub. F2 의 informational-only status 는 K=50 binding 까지 carry.
- **L3**: 본 cascade run 의 lens body 는 `state/.../k10_reimpl/core_<name>.hexa` (Phase 1 reimpl) — nexus repo (`/Users/ghost/core/nexus/lenses/`) 측 lens 와는 *별 layer*. spec §11 SSOT 의 K=10 binding 은 *file path* 기준 — 본 run path 와 match (whitelist_source=`spec §3.1 canonical K=10 (2026-05-11)`).
- **L4**: K=10 smoke PASS 가 K=25 canary 의 *guarantee* 는 아님 — cascade_k25_plan §1 의 13 추가 core_* lens reimpl 필요 (Phase 2-A; spec §4 Phase 2). 본 verdict 는 K=10 step CHARGE 만 (C1 chain step 1/3).

## 7. Next Step — K=25 Canary

cascade_k25_plan §0 prereq 모두 충족 (Phase 1 verdict §7):
- (a) input channel x → ✓ ANIMA_LENS_X_FILE / ANIMA_LENS_SEED
- (b) axis-specific kernel → ✓ 10 lens 모두 별 axis
- (c-e) F-reimpl-1/2/3 → ✓ PASS
- (f) back-compat → ✓ `k10_reimpl/` 별 디렉토리
- (g) lock policy → ✓ no chflags/chattr

Phase 2-A (13 추가 core_* lens reimpl) 진입 가능. 본 K=10 smoke verdict 가 cycle 6 §S 의 cascade entry checkpoint — K=25 canary 의 직접적 prereq.

## 8. Cross-Reference

| 출처 | path | 관계 |
|------|------|------|
| spec.md | `state/.../spec.md` | §3.1 K=10 whitelist + §4 C1 chain + §5 F1/F2 본 verdict 의 binding spec |
| Phase 1 verdict | `state/.../k10_reimpl/phase1_verdict_2026_05_12.md` | reimpl PASS + F-reimpl-1/2/3 PASS prereq |
| cascade aggregator | `tool/anima_nexus_1013lens_cascade.hexa` | cycle 5 §4 #H K-cascade aggregator (renamed) |
| run script | `state/.../k10_reimpl/run_k10_cascade_smoke.sh` | 본 verdict 의 actual entry harness |
| raw results | `state/.../k10_reimpl/k10_cascade_smoke_results_2026_05_12.json` | per-lens score + gate computation source |
| cascade plan K=25 | `state/.../cascade_k25_plan_2026_05_12.md` | next step (K=25 canary) prereq |
| Hc_586 | `docs/hypotheses_candidates/Hc_586_*.md` | F1 NOT TRIPPED → partial resume status 유지 |

---

**lock policy**: 본 verdict 작성 + 본 K=10 cascade smoke run 과정에서 chflags/chattr immutable flag 적용 없음. NEXT.md §4 의 NO-RUNPOD / NO-Mistral-7B / NO-cost / wall<30min hard constraints 모두 준수.
