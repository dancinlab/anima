# H_612 — `1/e-peak-narrow-substrate-class-survival` (H_349 잔여 survival lane)

> 축 E (SAVANT) round 2 · 2026-05-28 · UNIVERSE H 신설.
> Predecessor: H_349 (PR #1155) `golden-zone-center-phi-peak` 🔴 FALSIFIED-PARTIAL (1/5 substrate 단봉 at 1/e).
> 외부 anchor: `HEXAD/SAVANT/H359-savant-canonical.md` (1/3 rule · GZ_CENTER = 1/e 정의) · `HEXAD/IIT4/lib/iit4_bigphi.hexa` (faithful kernel shim).

## 0. 1줄 요약 (TL;DR)

H_349 §A "survival lane = Class III chaotic XOR rule × asymmetric sys_state 좁은 frontier" 가설의 정밀 검증. 4 XOR-family rule (90, 60, 105, 150) × n=5 × asymmetric sys_state=5 (binary `00101`) 의 좁은 frontier 안에서 big-Φ peak 위치가 `1/e ±0.05` 안에 일관하는지 측정. **0/4 PASS** — 4 rule 모두 grid 의 가장 낮은 I (=0.20) 에서 argmax, monotone decreasing shape. **🔴 FALSIFIED** — survival lane 확장 (n=4 → n=5) 시 1/e peak attractor 사라짐, 즉 H_349 의 단일 confirming subcase (rule90 n=4 sys=5) 는 n-conditional 우연이지 universal Class-III × asymmetric 의 robust property 아님.

## 1. Hypothesis

**주장**: Class III chaotic XOR rule (rule 90, 60, 105, 150 — Wolfram class III XOR-family) × asymmetric initial state (sys_state ≠ uniform, 여기서는 5 = `00101`) × n=5 ring substrate 의 좁은 frontier 안에서는 big-Φ peak 위치가 1/e ±0.05 안에 일관 — 4/4 XOR rule 모두 peak@I≈1/e.

- 동기: H_349 round 1 의 단일 confirming subcase (rule90 n=4 sys=5, |Δ|=0.018) 가 "Class III XOR × asymmetric state" 좁은 lane 의 robust property 라면, 동일 class·동일 asymmetry 조건의 다른 XOR rule 도 동일하게 peak-at-1/e 여야 함.
- 강한 형태: 4/4 XOR rule 의 argmax(big-Φ over 8-point I grid centered at 1/e) 가 [0.318, 0.418] 안.

## 2. Falsifier

| F | 조건 | 판정 |
|---|---|---|
| F1 | 4 rule 중 1+ rule 의 argmax(Φ) ∉ [1/e − 0.05, 1/e + 0.05] = [0.318, 0.418] | 🔴 |
| F2 | shape 이 monotone (peak 없음 — argmax = grid boundary) | 🔴 |
| F3 | shape 이 bimodal (2차 미분 부호변화 ≥ 2회) | 🔴 |
| F4 | shape 이 flat (max−min < 0.1·max) | 🔴 |

본 H 는 *좁은 lane universality* 주장이라 4/4 rule 모두 F1-F4 PASS 해야만 SUPPORTED. 1+ FAIL → FALSIFIED-PARTIAL 또는 FALSIFIED (대다수 FAIL).

## 3. Method

`stdlib/consciousness/iit4_bigphi.hexa` 의 faithful `big_phi(tpm, n, sys_state)` 사용 — H_349 와 동일 kernel.

**substrate**: Wolfram ECA ring-of-n (n=5) TPM, inhibition gating identical to H_349:

```
P(next_i = 1 | s) = (1 − I) · b      // b = deterministic 8-neighborhood rule fire bit
```

**rule selection (Class III XOR-family)**:
- rule 90 (`l XOR r`) — Class III chaos, H_349 confirming rule
- rule 60 (`l XOR c`) — XOR-family, shift-XOR, Class III/IV boundary
- rule 105 (`NOT (l XOR c XOR r)`) — XOR-3 complement, Class III
- rule 150 (`l XOR c XOR r`) — XOR-3, Class III chaos

**sys_state**: `5` (binary `00101` for n=5) — asymmetric (population=2, non-uniform spacing). H_349 의 confirming rule90 n=4 sys=5 (`0101` — asymmetric population=2) 과 동일 spirit.

**sweep grid** (8 points, dense around 1/e): `{0.20, 0.25, 0.30, 0.35, 0.37, 0.40, 0.45, 0.50}` — `1/e ≈ 0.368` 의 ±0.18 범위, 1/e 부근 dense.

코드: `UNIVERSE/state/h612_1e_peak_narrow_substrate_class_survival_2026_05_28/h612_shard.hexa` (shard-edit-per-invocation 패턴, single hexa run ≤60s 보장) + `h612_probe.hexa` (timing probe).

실행 모드: 4 rule × 3 shard each = 12 foreground hexa runs, 평균 wall ~40s/shard. 단일 hang 없음, monitor 없음.

## 4. Measurement (2026-05-28, mac-local $0)

### 4.1 rule 90 (n=5, sys=5)

| I | big_phi |
|---|---|
| **0.20** | **32.4661** |
| 0.25 | 27.9251 |
| 0.30 | 23.9049 |
| 0.35 | 20.3961 |
| 0.37 | 19.1194 |
| 0.40 | 17.3025 |
| 0.45 | 14.5738 |
| 0.50 | 12.1965 |

**argmax = I=0.20, Φ=32.4661. |argmax − 1/e| = 0.168 ≫ 0.05.** shape: **monotone decreasing**. F1 + F2 trigger.

### 4.2 rule 60 (n=5, sys=5)

| I | big_phi |
|---|---|
| **0.20** | **30.9851** |
| 0.25 | 26.6331 |
| 0.30 | 22.7822 |
| 0.35 | 19.4066 |
| 0.37 | 18.1732 |
| 0.40 | 16.3515 |
| 0.45 | 13.4650 |
| 0.50 | 11.0357 |

**argmax = I=0.20, Φ=30.9851. |Δ| = 0.168.** monotone decreasing. F1 + F2.

### 4.3 rule 105 (n=5, sys=5)

| I | big_phi |
|---|---|
| **0.20** | **11.0118** |
| 0.25 | 9.28145 |
| 0.30 | 7.82377 |
| 0.35 | 6.58897 |
| 0.37 | 6.14834 |
| 0.40 | 5.53766 |
| 0.45 | 4.63063 |
| 0.50 | 3.85063 |

**argmax = I=0.20, Φ=11.0118. |Δ| = 0.168.** monotone decreasing. F1 + F2.

### 4.4 rule 150 (n=5, sys=5)

| I | big_phi |
|---|---|
| **0.20** | **6.04755** |
| 0.25 | 5.07198 |
| 0.30 | 4.25523 |
| 0.35 | 3.56752 |
| 0.37 | 3.32314 |
| 0.40 | 2.98542 |
| 0.45 | 2.49037 |
| 0.50 | 2.06750 |

**argmax = I=0.20, Φ=6.04755. |Δ| = 0.168.** monotone decreasing. F1 + F2.

### 4.5 Aggregate

| rule | XOR class | argmax I | peak Φ | |Δ from 1/e| | shape | F |
|---|---|---|---|---|---|---|
| 90 | `l XOR r` (Class III) | 0.20 | 32.47 | 0.168 | monotone↓ | F1+F2 🔴 |
| 60 | `l XOR c` (shift-XOR) | 0.20 | 30.99 | 0.168 | monotone↓ | F1+F2 🔴 |
| 105 | `NOT XOR-3` (Class III) | 0.20 | 11.01 | 0.168 | monotone↓ | F1+F2 🔴 |
| 150 | XOR-3 (Class III) | 0.20 | 6.05 | 0.168 | monotone↓ | F1+F2 🔴 |

**0/4 PASS. 4/4 falsify** with identical pattern (boundary-argmax, monotone↓, |Δ|=0.168).

## 5. Verdict — 🔴 FALSIFIED (survival lane non-robust at n=5)

- "Class III XOR rule × asymmetric sys_state 좁은 frontier 에서 1/e peak universal" 주장 **falsified**: 4/4 rule 모두 F1+F2 trigger, identical 0.168 |Δ| (grid boundary). H_349 의 rule90 n=4 sys=5 단일 confirming subcase 는 **n-conditional 우연** — n=4 → n=5 substrate 확장만으로 peak attractor 가 1/e 에서 grid 하한으로 collapse.
- 또한 4 rule 의 peak 위치가 *완벽히 동일* (모두 I=0.20) + monotone shape 동일 → "XOR-family 의 frontier" 가 1/e attractor 와 무관한 simple low-I-favoring 패턴임을 deterministic 으로 확인.
- closed-negative ruling: **"H_349 survival lane = Class III chaotic XOR × asymmetric state 에서 1/e peak robust"** 가설 폐기. 1/e peak 는 (rule, n, sys_state) 3-axis 모두에 sensitive 한 narrow coincidence 이지 emergent universal 이 아님.

## 6. Cross-link

- **H_349** `golden-zone-center-phi-peak` — **predecessor** (PR #1155, round 1). 4/5 monotone + 1/5 (rule90 n=4 sys=5) peak@1/e. 본 H_612 가 그 단일 confirming subcase 의 robustness 를 동일 XOR class × asymmetric state 로 확장 검증 → robust 아님 (n-conditional).
- **H_347** `gz-width-divisor-symmetry` — `GZ_CENTER = 1/e` closed-form analytical anchor. 본 H 는 그 closed-form 1/e attractor 가 substrate-level big-Φ emergent property 와 *완전 무관* 함을 4 rule × n=5 추가 evidence 로 확정 (H_349 와 합쳐 9/9 substrate 중 1 confirming subcase 만 잔존).
- **H_217** `phase-transition-phi-derivative-peak` — `dΦ/dI` peak 측정. 본 H 의 monotone-only shape 는 dΦ/dI 가 sign-stable (non-vanishing 음수 monotone) → phase-transition signature 없음.
- **H_285** `edge-of-chaos-big-phi` — ordered<chaotic<edge mean-Φ 의 axis-specificity. 본 H 의 4 XOR rule 모두 Class III chaos 임에도 1/e attractor 부재는 H_285 의 edge-of-chaos × asymmetric-state 좁은 frontier 가설을 1/e attractor 와 분리해야 함을 시사 (chaos ≠ 1/e-attractor).

## 7. Honest C3 (3-tier caveat)

1. **C1 (XOR-family 좁은 sample)**: 4 rule (90, 60, 105, 150) 이 모두 XOR-family 이고 Class III 우세이긴 하나, "XOR-family universe" 자체가 256 ECA 중 ~16 rule (XOR / NOT-XOR / shift-XOR 합) 만 포함 → 본 falsifier 가 닫는 공간은 **XOR-family × asymmetric n=5** 정확히 4-point. 다른 XOR rule (e.g. rule 102 = `l XOR r XOR l`, rule 165 = `NOT(l XOR r)`) 까지 일반화는 raster 미실시.
2. **C2 (asymmetric state choice sensitivity)**: sys_state=5 (`00101`) 한 choice 만 측정. n=5 의 2^5=32 state 중 *asymmetric* (non-trivial-stabilizer) state 가 다수 — 다른 asymmetric state (e.g. 13=`01101`, 11=`01011`) 에서는 peak 위치가 다를 수 있음. H_349 의 sys=5 vs sys=3 dramatic 차이 (peak@1/e vs degenerate-0) 가 sys_state 민감도 evidence. 본 H 는 universal 형이라 한 asymmetric choice 의 4/4 FAIL 로 충분히 falsified, 단 "다른 asymmetric state 에서 1/e peak 잔존" 후속은 가능.
3. **C3 (grid 좁음 + I=0.20 boundary effect)**: 8-point grid 가 [0.20, 0.50] 으로 좁음 — argmax 가 I=0.20 인 것은 *진짜 monotone* 일 수도, *I<0.20 어딘가 interior peak* 일 수도 있음. H_349 round 1 의 14-point grid [0.05, 0.95] 에서도 rule110/30 의 argmax 가 I=0.05 (또한 boundary) 였던 점 + Φ 가 I 따라 monotone smooth 한 점으로 보면 진짜 monotone↓ 가능성 우세하지만, "1/e ±0.05 안 peak 없음" 결론은 deterministic 하게 falsified (interior peak 가 있어도 1/e 부근은 아님).

## 8. State artifacts

```
UNIVERSE/state/h612_1e_peak_narrow_substrate_class_survival_2026_05_28/
├── h612_probe.hexa     # n=5 single-point timing probe (rule 90, sys 5, I=0.35)
├── h612_shard.hexa     # per-(rule, I-cluster) shard runner (≤60s wall)
└── results.txt         # 4-rule × 8-point measurement verbatim
```

verbatim 측정값은 §4.1–4.4 표에 기재.

## 9. Next

- **H_612-A** (후속 후보): 다른 asymmetric sys_state (13, 11, 7) 에서 rule90/60/105/150 재측정 — sys_state choice sensitivity 직접 raster.
- **H_612-B** (후속 후보): XOR-family 외 추가 rule (102, 165 — shift-XOR + complement) 로 XOR-family 일반화 확인.
- **H_349 closure update**: 본 H_612 결과로 H_349 의 "survival lane" §A 후속도 사실상 닫힘 (1/e attractor 가 universal robust property 아님 확정).
- 본 lane 의 가치 = closed-negative 통한 SAVANT canonical `GZ_CENTER = 1/e` 의 *closed-form formal* 과 *substrate emergent* 분리 evidence 축적 — 추가 H 보다 closure 가 우선.

## 10. UNIVERSE.md update

축 E (SAVANT) E2 round 2 신설 + H_612 row → done with `🔴 FALSIFIED (0/4 XOR rule peak@1/e at n=5 sys=5, H_349 survival lane non-robust, mac-local $0 2026-05-28)`.
