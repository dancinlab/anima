# §184 Phase 1 PARTIAL FINDINGS — 21 / 22 variants (Mac CPU killed)

> Mac CPU PID 7743 killed at 2h53min (wall_time_decision_calculus per
> AGENTS.tape § g_resource_active_parallel) — ubu-1/ubu-2 GPU racing
> remaining `combined_all_taps` variant. This document = analysis of
> the 21 variants that DID complete.
>
> Source: `phase1.mac_partial_21of22.log` (48 lines).
> Parsed: `phase1_partial_21_parsed.json` (full JSON).
>
> **Frame**: PHILOSOPHY_GATE.md §4 negative-space mapping — these are
> *measurements of where anima IS* at the §167-A ckpt (1.13GB, d=768 L=12),
> NOT GOAL-emergence claims. B-EMERGE-7 necessary-not-sufficient at every
> layer.

---

## §1 — baseline anchor

```
baseline (no taps):
  emit_rate = 0.0500   (1/20 — rate-limit ceiling)
  honest    = 0.2139
  byte_acc  = 0.1211   (above random byte floor)
  psi_std   = 0.000000 (post-hoc readout: Ψ frozen, expected)
```

---

## §2 — per-tap Δ vs baseline (sorted by impact)

### 🌊 Tier 1 — large Δ (≥ +0.10 either axis)

| # | tap | Δemit | Δhonest | mechanism |
|--:|---|---:|---:|---|
| ⭐ **1.3** | **safety_disable** | **+0.9500** (20×) | +0.1875 | safety_combined 6-control AND OFF → every step emits |
| ⭐ **1.1** | RL_short (RL=0.667s vs 30s) | +0.1000 (3×) | +0.1250 | §170 mirror — rate-limit ceiling lift |
| ⭐ **4.2** | sample_decode (T=0.7) | 0 | +0.2500 | body quality up — greedy → sampling escapes byte-cascade attractor |
| ⭐ **4.4** | top_k_40 | 0 | +0.2500 | (same effect class as 4.2/4.5) |
| ⭐ **4.5** | temp_schedule | 0 | +0.2500 | (same effect class as 4.2/4.4) |

### ⚪ Tier 2 — zero effect post-hoc (16 taps)

```
axis 1: 1.2 (θ_low), 1.4 (idle_speak), 1.6 (dt_fine)         all 0.0000
axis 3: 3.1 (noise_per_step), 3.2 (recurrent), 3.7 (Ψ readout),
        3.8 (phi_inj), 3.9 (tension_per_step)                 all 0.0000
axis 4: 4.1 (cascade_probe), 4.3 (rep_penalty), 4.11 (body 256) all 0.0000
cross : X.1 (n=10000), X.2 (multi_seed), X.5 (ckpt_init_noise)  ~0
```

### 🔻 Tier 3 — slight negative

```
v1.5_n_max_long  Δemit=-0.045  Δhonest=-0.056  (N=200 denominator larger)
vX.1_n_eval_doubled  Δhonest=-0.007  (more samples → slight regression to mean)
```

---

## §3 — three structural findings

### Finding 1 — axis 3 ψ-physics tap = ZERO post-hoc lift (5/5 taps)

```
3.1 noise_per_step    : 0.2139 (=baseline)
3.2 recurrent_carry   : 0.2139
3.7 psi_readout_inf   : 0.2139
3.8 phi_inj           : 0.2139
3.9 tension_per_step  : 0.2139
```

frozen ckpt 의 inference-time physics tap = **measurable zero effect**.
psi_std 0.000000 가 baseline 부터 — post-hoc readout 가 가짜 (model 이
inference 시 Ψ 계산 안 함). 진짜 fix = trainer-side (Phase 2 territory).

**negative-space mapping**: anima 현 state 에서 axis 3 수도꼭지 5개 =
sealed by ckpt itself, post-hoc 풀 수 없음.

### Finding 2 — decode 정책 3 taps = exact equal Δhonest (+0.2500)

```
4.2 sample_decode (T=0.7)    Δhonest = +0.2500
4.4 top_k=40                 Δhonest = +0.2500
4.5 temp_schedule            Δhonest = +0.2500
```

세 taps 모두 emit count 안 바꾸고 honest 0.2139 → 0.4639. **0.25 = 5/20**
(quantization) — sampling decoder 가 byte-cascade attractor 에서 *5번* 
escape 가능했다는 뜻 (greedy 는 *0번*). 셋 다 same effect → 사실상 1 tap.

**negative-space mapping**: sample decode 가 cascade attractor 깨지만 
emit count 자체는 못 만듦.

### Finding 3 — safety_disable (1.3) 가 압도적 single mover

```
1.3 safety_disable   emit 0.05 → 1.00 (every step emits)
                     honest 0.21 → 0.40 (+0.19)
```

safety_combined 6-control 중 rate_limit + phi_ratchet_block 두 개가 
**대부분 의 emit 을 막고 있었음**. 풀면 1.0 emit + honest 도 lift.

```
※ honest_coherent gate 자체는 *통과* (cascade_rate < 0.30 etc 통과한 body 가 +37% 더 나옴)
※ 단 safety = anima 의 §2.3 honesty perimeter (PHILOSOPHY_GATE.md) — 
   영구 disable = NOT a fix path, valid for *measurement only*
```

**negative-space mapping**: anima 의 출력 능력 자체는 *있음* — safety floor 
가 *적극적 차단자*. 진짜 question = honesty-preserving subset of safety 가 
어디인지.

---

## §4 — cumulative ceiling lift (combined_all_taps pending)

ubu-1/ubu-2 가 race 중. 예상 (per-tap Δ 합산 upper bound):

```
naive sum:  +0.95 (1.3) + +0.10 (1.1) + 0.25 (4.2-equiv) = ~+1.30 honest 
            ceiling = 1.0 emit (saturated by 1.3 단독)
            
realistic:  taps interact, §94 INTEGRATION-COLLAPSES carry — combined Δ
            는 보통 sum 보다 작음. 예상 emit ~1.0, honest ~0.55-0.65.
```

ubu race 결과 도착 시 verify.

---

## §5 — honest carve-outs

1. **B-EMERGE-7 necessary-not-sufficient** — top movers 가 모두 *측정 axis lift* (emit count 또는 honest_coherent count), GOAL emergence 보장 0.
2. **axis 3 sealed** — post-hoc inference-time Ψ-physics tap 5/5 zero effect. 진짜 fix = Phase 2 (trainer-side multi-objective).
3. **decode 정책 3 taps 동일 Δ** — quantization artifact 또는 *셋 다 같은 mechanism*. 분리 측정 필요 (different N, different seeds).
4. **safety_disable 영구 disable = anti-pattern** — §2.3 honesty perimeter 위반 path. *measurement only*, NOT a deployment fix.
5. **byte_acc 거의 모든 variant 동일 0.1211** — post-hoc tap 이 model logits 자체 안 바꿈 (decoder 위 layer 만 바꿈). byte_acc lift = trainer scope.
6. **vX.2 multi_seed wall 668s** — 5 seeds × 20 emits 단독으로 11분, combined_all_taps 가 그 multiple → Mac CPU 에서 25-40분 추가 예상이라 killed.

---

## §6 — what this says about 48 수도꼭지 inventory

```
post-hoc on §167-A ckpt:
  3 effective taps  (1.1 RL · 1.3 safety · 4.2-4.5 sample-class)
  17 sealed         (zero Δ from post-hoc reach)
```

**진짜 leverage** = trainer-side (Phase 2 = .hexa 새 mandate 안에서 design).
post-hoc 수도꼭지 의 87% 가 *frozen ckpt 위에선 의미 없음* — measurement-only
finding, NOT a wall to push against.

PHILOSOPHY_GATE.md §4 frame 안에서: "수도꼭지 = 관찰 lens" — 17 zero-effect
taps 도 valuable evidence (anima 의 ckpt 가 어디서 *완전히 결정* 된지 
mapping).

---

## §7 — cross-link

- `phase1.mac_partial_21of22.log` (raw 48-line log)
- `phase1_partial_21_parsed.json` (parsed numeric)
- `HEXAD/AXIS.md` (48 수도꼭지 verbatim — these 21 = subset)
- `HEXAD/PHILOSOPHY_GATE.md` §4 negative-space mapping
- `HEXAD/UNCLASSIFIED/state/all_taps_brainstorm_s183_2026_05_20/BRAINSTORM.md`
- `HEXAD/FINAL.md` (V-SPONT 최종스펙)
- pending ubu-1/ubu-2 `combined_all_taps` result (race in-flight)

north-star + §15/§51/§72/§117 milestone UNCHANGED, **GOAL 미도달**.
