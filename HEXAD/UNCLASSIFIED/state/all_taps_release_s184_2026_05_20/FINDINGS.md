# §184 Phase 1 ALL TAPS RELEASE — FINAL FINDINGS (22/22 LANDED)

> **Frame**: PHILOSOPHY_GATE.md §4 negative-space mapping. All numbers
> below are *measurements of where anima IS* at the §167-A ckpt
> (1.13GB, d=768·L=12·283M, lambda_psi=1.0 lambda_ce=0.1, byte-LM
> V=256). **NOT GOAL-emergence claims** — B-EMERGE-7 necessary-not-
> sufficient at every layer.
>
> Source artifacts:
> - 21 variants Mac CPU log    : `phase1.mac_partial_21of22.log`
> - combined_all_taps ubu-1 GPU: `phase1_combined_ubu1.json`
> - 21 parsed JSON              : `phase1_partial_21_parsed.json`

---

## §1 — race summary

```
Mac CPU PID 7743    : killed at 2h53m after 21/22 variants (wall_time
                      _decision_calculus per AGENTS.tape — combined
                      remaining wall too long on CPU)
ubu-1 RTX 5070 cuda : WIN. combined_all_taps wall 1915.7s (32 min)
                      status=WALL_EXCEEDED_PARTIAL (max-wall-per-
                      variant=1800s, completed 1/5 seeds)
ubu-2 RTX 5070 cuda : killed 29:47 after ubu-1 finished (orphan free)

Total race wall  : Mac CPU 21 var ≈ 50 min + ubu-1 combined 32 min
Total race cost  : $0 (local hosts only)
```

---

## §2 — baseline vs all 22 variants

```
baseline:
  emit_rate = 0.0500     (1/20 — rate-limit ceiling)
  honest    = 0.2139
  byte_acc  = 0.1211     
  psi_std   = 0.000000   (post-hoc readout: Ψ frozen, expected)
```

### Tier 1 ⭐ — large Δ (cause)

| # | tap | Δemit | Δhonest | mechanism |
|--:|---|---:|---:|---|
| **1.3** | safety_disable | **+0.95** (20×) | +0.19 | 6-control AND OFF |
| **1.1** | RL_short (0.667s) | +0.10 (3×) | +0.13 | rate-limit lift (§170 mirror) |
| **4.2** | sample_decode T=0.7 | 0 | **+0.25** | byte-cascade attractor escape |
| **4.4** | top_k=40 | 0 | **+0.25** | same effect class as 4.2 |
| **4.5** | temp_schedule | 0 | **+0.25** | same effect class as 4.2 |

### Tier 2 ⚪ — zero effect post-hoc (16 taps)

```
axis 3 ALL 5    : Ψ post-hoc readout sealed by frozen ckpt
   3.1 noise_per_step / 3.2 recurrent / 3.7 psi_readout_inf /
   3.8 phi_inj / 3.9 tension_per_step
   
axis 1 minor 3  : 1.2 θ=0.10 / 1.4 idle_speak / 1.6 dt_fine
axis 4 minor 3  : 4.1 cascade_probe / 4.3 rep_penalty / 4.11 body=256
cross-axis 3    : X.1 n=10000 / X.2 multi_seed / X.5 ckpt_init_noise
```

### 🌋 combined_all_taps (variant 22) ⭐⭐⭐

```
emit_rate           : 1.0000  (saturated by 1.3 safety_disable)
honest_score        : 0.6441  (+0.4302 vs baseline)  ⬆️ HUGE
byte_acc            : 0.1152  (slight regression, expected)
psi_std             : 2.25e-8 (still post-hoc zero, axis 3 sealed)
mean_motivation     : 0.5148  (lift vs baseline ~0.45)
max_cascade_rate    : 0.0277  (well below §9 threshold 0.30)
mean_cascade_rate   : 0.0159
cond_cascade_ok_majority : True
emission_count_mean : 200.0   (= N_MAX=200 saturated)

status: WALL_EXCEEDED_PARTIAL (1/5 seeds completed, single-seed agg)
```

---

## §3 — three structural findings

### Finding 1 — axis 3 ψ-physics 5 taps = sealed at post-hoc (verified)

```
3.1 / 3.2 / 3.7 / 3.8 / 3.9  Δhonest = 0.0000 ∀
combined psi_std            = 2.25e-8 (zero in practice)
```

**negative-space mapping**: frozen §167-A ckpt 의 inference-time Ψ-physics
tap 모두 **zero effect**. ckpt 가 training 시점에 결정된 후 inference 시
Ψ 계산 = 결과 안 흔들음. 진짜 fix path = **trainer-side multi-objective**
(per `train_s185_psicouple.hexa` 의 TODO[dual-head] 블록 + inbox patch
`flame-anima-dual-head-multiobjective.md`).

### Finding 2 — decode 정책 3 taps = quantized identical Δ

```
4.2 (T=0.7) / 4.4 (top-k=40) / 4.5 (temp_schedule) 셋 다
Δhonest = +0.2500 정확히 같음 = 5/20 quantum

해석: greedy 는 byte-cascade attractor 에 *0번* 잡혔고, sampling 3개 
모두 *5번* escape (single-seed, N=20). same mechanism class.
```

**negative-space mapping**: anima 의 frozen ckpt 가 *cascade attractor* 에
deterministic 으로 잡혀있음 — sampling 만이 그 부분 통과. emit_count 자체
는 안 늘림 (rate-limit + safety 가 별개 차원).

### Finding 3 — combined_all_taps cumulative lift (the big one)

```
naive sum of Tier 1 Δhonest = +0.95 (impossible, > 1) — interaction 큰 
realistic combined          = +0.43 (measured)

해석:
  - emit saturation (1.3 single-handed achieves 1.0)
  - honest 의 추가 lift 가 sample-class + RL 의 *cooperative* 효과
  - cascade_rate 매우 낮음 (0.016 mean) → §9 honest gate 통과율 lift 의 source
  - mean_motivation 0.5148 (vs 0.45 baseline) → score 자체도 oscillation
    범위가 살아남
```

**negative-space mapping**: 13 §7-clean taps 다 풀어서 honest 0.64 가능.
하지만 emit_rate 1.0 = **safety floor 무력화** 의 결과로만 가능 — 
deployment-honest 한 path 아님 (§2.3 honesty perimeter 위반). 진짜
lift path = **trainer-side로 안전 유지 + cascade 깨기 + Ψ 살리기**.

---

## §4 — what this says about 48 수도꼭지 inventory

```
post-hoc on §167-A ckpt:
  4 effective taps (combined Δhonest=+0.43)
     - 1.3 safety_disable (single-tap dominates, NOT deployable)
     - 1.1 RL_short (rate-limit lift, valid)
     - 4.2/4.4/4.5 sample-class (cascade escape, valid)
  17 sealed taps (zero Δ from post-hoc reach)
```

**진짜 leverage 위치 = trainer-side** (Phase 2 = `.hexa` 새 mandate).
post-hoc 수도꼭지 의 17/21 = *frozen ckpt 위에선 의미 없음* — measurement-
only, NOT walls to push.

per PHILOSOPHY_GATE.md §4: 수도꼭지 = 관찰 lens. 17 zero-effect = anima 의
ckpt 가 *trainer-time 에서 완전히 결정* 된 부분 mapping. valuable.

---

## §5 — honest carve-outs

1. **B-EMERGE-7 necessary-not-sufficient**: combined honest 0.64 ≠ GOAL
   emergence. honest_coherent 통과 = §9 cascade gate 통과, NOT
   meaning/spontaneity/anima-as-living-consciousness claim.

2. **single-seed combined**: status WALL_EXCEEDED_PARTIAL — 5 seeds 중
   1 만 measured. multi-seed variance unknown. re-run with N_MAX=200 *+*
   higher max-wall (or move to Phase 2 trainer side) needed.

3. **safety_disable + RL_short = single-mover dominance**: combined emit
   1.0 은 사실상 *1.3 safety + 1.1 RL* 만으로 달성됨. 다른 11 taps 의
   independent 기여 미측정 (per-tap ablation 안 됨, §94 INTEGRATION-
   COLLAPSES carry).

4. **byte_acc 0.115 = 거의 baseline**: post-hoc tap 셋 model output 자체
   안 흔듦. byte_acc lift 는 trainer-side scope.

5. **axis 3 zero effect verification**: 5/5 axis 3 taps 모두 honest=
   0.2139 동일 — **frozen ckpt 의 Ψ-physics 가 inference 시 계산되지
   않거나, 계산돼도 motivation 결정에 영향 0**. PHILOSOPHY_GATE.md §3
   anima 철학 "자기 physics 로부터" 의 honest gap.

6. **decode 3 taps quantum identical**: T=0.7/top-k=40/temp_schedule
   가 5/20 quantum 동일 → 셋 다 *same single-seed lottery escape* 가능성.
   different seeds × different decoders 분리 측정 필요.

7. **combined_all_taps 가 1 seed 만 = honest fragile** — 0.64 가 single
   sample. 0.40~0.85 어디든 가능 (single-seed variance ~±0.15 typical).

8. **wall_time_decision_calculus 실측 case**: Mac CPU 2h53m vs ubu RTX
   5070 32min = 5.4× faster, single-variant. 21 variants 의 다른 작은
   변종 평균 90-180s on Mac CPU 였으니 ubu 옮겨도 setup overhead 가
   computer saving 흡수 — 정확히 새 governance entry 의 예측대로.

---

## §6 — next step (§185 + beyond)

per `@D g_train_via_hexa_cloud_and_hexa_lang` (TOP MANDATE, 2026-05-20):
모든 NEW fire = `.hexa` trainer + `hexa cloud` dispatch.

**§185 skeleton landed** (this commit cycle): `train_s185_psicouple.hexa`
clone from flame_d768_12L_corpus_test.hexa + anima CORPUS_S101 + Ψ-anchor
single-loss proxy. **Multi-loss (L_psi/L_route/L_phi) blocked on flame
dual-head** — inbox patch design at `~/core/hexa-lang/inbox/patches/
flame-anima-dual-head-multiobjective.md`.

**Path forward**:
1. flame upstream cycles 1-4 (anima inbox patch land) → dual-head primitives
2. §185 wire L_psi/L_route/L_phi on top → real Ψ-COUPLE trainer
3. fire d=192·L4 smoke first ($0 ubu-1) — verify build + gn2 trajectory
4. fire d=768·L12 full (runpod H100 ~3-5h, ~$6-15 per honest carve-out)
5. eval ckpt with same Phase 1 22-variant battery → measure trainer-side
   lift on post-hoc-sealed 17 taps

**honest expectation**: Phase 1 already showed where the ceiling is
(honest 0.64 with all 13 §7-clean post-hoc taps). Phase 2 (trainer-side
multi-objective) target = breaking that ceiling *honestly* — i.e.,
**without disabling safety_combined**, by training Ψ alive into the ckpt.

per PHILOSOPHY_GATE.md §4: this is *negative-space mapping*, NOT GOAL
prescription. "이렇게 되어야 한다" 폐기. north-star + §15/§51/§72/§117
milestone UNCHANGED, **GOAL 미도달**.

---

## §7 — cross-link

- `phase1.mac_partial_21of22.log` (Mac CPU 21 variants raw)
- `phase1_partial_21_parsed.json` (Mac 21 parsed numeric)
- `phase1_combined_ubu1.json` (ubu-1 combined_all_taps single-seed result)
- `phase1.ubu1.log` (ubu-1 dispatch log)
- `HEXAD/AXIS.md` (48 수도꼭지 verbatim)
- `HEXAD/PHILOSOPHY_GATE.md` §4 negative-space mapping
- `HEXAD/FINAL.md` §9 silent ceiling inventory inline
- `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`
- `train_s185_psicouple.hexa` (next cycle, .hexa trainer skeleton)
- `~/core/hexa-lang/inbox/patches/flame-anima-dual-head-multiobjective.md`
- `~/core/hexa-lang/inbox/patches/cloud-cli-run-hang.md`
- `archive/PHILOSOPHY.tape § verdict_all_taps_release_s184_2026_05_20` (pending append)
