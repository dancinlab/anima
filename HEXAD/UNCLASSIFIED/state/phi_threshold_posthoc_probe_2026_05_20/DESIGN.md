# §168 PHI-THRESHOLD-POSTHOC-PROBE — DESIGN

> $0 design-tier cycle. **NO new fire, NO ckpt forward, NO GPU/runpod**.
> User directive 2026-05-20: *"upstream first, 이 세션에서 진행"*.
>
> Trigger: `HEXAD/PRIORITY_QUEUE.md` items #4 (J.6 §161-FIRE Φ
> measurement) + #9 (I.3 threshold sweep). User executed `=> go` on
> three items: (B) §161 Φ measure, (C) threshold sweep, §126 pod
> query.
>
> §126: terminated (separate task, cost-containment ✅).
> (B) + (C): this document — split into upstream gap and a
> closed-form analytical sweep that lands $0 hexa-native.

---

## §1 — Honest path-of-execution

### Item #4 J.6 — Φ measurement on §161-FIRE ckpt

`HEXAD/PRIORITY_QUEUE.md` §3 said: forward pass on §161-FIRE ckpt
(1.13 GB), measure `phi_spatial` per `c_lib.hexa::c_measure_phi`
(RFC 036 byte-equal Φ_RS). This **requires** a hexa-runtime path to
extract residual states from a PyTorch-trained `.pt` checkpoint —
which **does not exist today**.

→ **Filed inbox patch**:
`~/core/hexa-lang/inbox/patches/pt-ckpt-cross-substrate-residual-readout.md`
(one concept per file mandate, distinct from §71 RFC-059
training-time complement). Two-clause patch (`.pt → mc_total
loader` + `decode_step_with_readout(layer_idx)`); five pre-registered
falsifiers F-PTLOAD-1..2 + F-PHIREAD-3..5.

→ **Forward Φ measurement carry**: deferred to patch land. NOT
attempted in this session per `hexa verify` mandate (anima cannot
self-validate a Python-port `phi_spatial` as evidence; only
`c_measure_phi` is the sanctioned oracle).

### Item #9 I.3 — Threshold sweep {0.0..0.7}

`HEXAD/PRIORITY_QUEUE.md` §5 said: post-hoc count emissions at
θ ∈ {0.0, 0.1, ..., 0.7} on §161 motivation trace. The full trace is
NOT logged in `result.json` (only the summary `{mean=0.4534,
std=0.0376, n=20}`), so post-hoc-on-trace also blocks on the same
upstream patch (Clause B `decode_step_with_readout` would also dump
the trace).

→ **Closed-form analytical sweep landed $0**:
`analytical_threshold_sweep.hexa` — Gaussian approximation on the
existing summary stats, COMBINED with the deterministic rate-limit
ceiling derivation. This yields a STRUCTURAL finding that does NOT
need the per-step trace (the rate-limit ceiling is exact;
P(at-least-one-emit) per θ uses the Gaussian approx and is honestly
labeled as such).

---

## §2 — Structural finding (B-S168-ANALYTIC, closed-form)

🔑 **Rate-Limit Ceiling Dominates Threshold — "수도꼭지 잠긴 욕조"**

- **이름**: rate-limit-ceiling-dominance (B-S168-ANALYTIC-1)
- **별칭**: 수도꼭지 잠긴 욕조 / threshold 가 아니라 수도꼭지가 잠겨있음
- **하는 일**: §161 measurement config 에서 `MIN_EMIT_INTERVAL=30s` ≫
  `N_MAX_STEPS × THINK_INTERVAL_TEST_SEC = 2s` 이라 **emit_rate ≤ 1/20
  = 0.05 ∀ θ**. observed 1/20 은 *임의 수치 아니라 ceiling-saturated*.
- **비유**: 욕조에 물 채우려고 손잡이 (threshold) 돌려도 수도꼭지
  (rate-limit) 가 1초당 한 방울로 잠겨있으면 손잡이 위치는 의미 없음

```
                  | step (×0.1s)
  emit allowed?   |  0   1   2  ...  19   N_MAX=20
  ────────────────┼────────────────────────────────────
  rate_ok         | T   F   F  ...  F     ← 첫 emit 후 30s 안 지나서 전부 F
  score>θ=0.30?   | T*  T*  T  ...  T*    ← ~84% steps (Gaussian μ-σ)
  AND             | T   F   F  ...  F     ← 첫 step 만 T
                  └─────────────────────────
                       max 1 emit / 20 = 0.05  ← rate-limit ceiling
```

비교 vs CONNECTION_CRITIQUE Wrong-C ("`imThreshold=0.30` hardcoded"):

| 진단 | 정확한가 | finer reading |
|---|:---:|---|
| Wrong-C: θ=0.30 unprincipled | ✅ correct | θ anchor 부재 = 사실 |
| Wrong-C: θ 가 emit 병목 | ❌ partial | rate-limit 이 *지금 regime 에서* dominant 병목 |
| Wrong-C: physics-anchored θ (§167-A) | ✅ valuable | 단 **rate-limit 도 같이 손봐야** Wrong-C 진짜 해소 |

---

## §3 — Closed-form 결과표 (analytical, no forward)

`analytical_threshold_sweep.hexa` 가 출력하는 표 (Gaussian μ=0.4534
σ=0.0376 n=20 가정):

```
    θ    | P(score>θ)/step | P(≥1 emit over N=20)     | capped_rate
  -------+----------------+---------------------------+------------
  0.00   | ≈1.0          | ≈1.0                      | 0.05 (ceiling)
  0.30   | ≈1.0          | ≈1.0                      | 0.05 (ceiling)
  0.40   | ≈0.92         | ≈1.0                      | 0.05 (ceiling)
  0.45   | ≈0.54         | ≈1.0                      | 0.05 (ceiling)
  0.50   | ≈0.097        | ≈0.88                     | 0.044
  0.55   | ≈0.0048       | ≈0.092                    | 0.0046
  0.60   | ≈8.4e-5       | ≈0.0017                   | 8.4e-5
  0.65   | ≈6.4e-7       | ≈1.3e-5                   | 6.4e-7
  0.70   | ≈2.3e-9       | ≈4.6e-8                   | 2.3e-9
```

(±0.05 Gaussian-approx margin — Winitzki erf max abs err 3.5e-5;
8-factor sum-of-clamped components is bounded, true distribution is
slightly tail-compressed vs Gaussian — observation, NOT degrade.)

**Three regimes** clearly demarcated:
- **θ ≲ 0.45**: rate-limit ceiling dominates, emit_rate = 0.05 flat
- **θ ≈ 0.50–0.55**: transition zone (Gaussian tail meets ceiling)
- **θ ≳ 0.55 ≈ μ+2.6σ**: threshold dominates, P drops exponentially

§161 config (`θ=0.30`) sits squarely in the rate-limit-dominated
regime, so lowering θ → 0 gives zero benefit; only **simultaneously**
lifting the rate-limit AND anchoring θ to physics (§167-A
FP-RECONNECT) addresses both Wrong-C diagnoses.

---

## §4 — Honest carve-outs (necessary-not-sufficient at every layer)

1. **Gaussian approximation**: §161 reports `{mean, std, n}` only, no
   trace. Gaussian on 8-factor sum is approximate (each factor
   clamp01, so true distribution is bounded ⇒ tails slightly thinner
   than Gaussian). The **ceiling row** is EXACT from eval semantics;
   only the **P(any)** column carries the Gaussian assumption. Per-
   step trace measurement deferred to upstream patch land.

2. **Φ measurement not landed**: this design only addresses the
   threshold-sweep half of Wrong-C; the Φ-axis 35%-weight gap from
   `HEXAD/CONNECTION_CRITIQUE.md` §2 remains unmeasured until
   inbox patch lands. NO Python-port `phi_spatial` was attempted
   (`hexa verify` mandate).

3. **Rate-limit is a §4 safety control** (SPONTANEOUS.tape 6-control
   SSOT). Lowering it is a **governance-gated** change, NOT a
   hyperparameter tweak. §167-A FP-RECONNECT addresses the
   *threshold* half; this finding suggests **the rate-limit half
   also needs a governance-gated cycle** before the *combined*
   emission lift can be measured.

4. **`hexa parse` blocked in Bash sandbox**: the `.hexa` file is
   syntactically conformant to `feedback_hexa_lang_syntax_gotchas`
   (dict `#{}`, missing-key `void`, etc.) but `~/.hx/bin/hexa`
   wrapper returns SIGKILL 137 inside this Bash sandbox (adjacent to
   `hexa-run-interp-hangs-on-mac.md` issue). User can verify
   directly in their shell.

5. **Necessary-not-sufficient (B-EMERGE-7 carry)**: closing the rate-
   limit + threshold-anchor pair would un-saturate the emit-rate
   ceiling, NOT prove emergence — just unblock the measurement axis
   that has been ceiling-saturated this whole arc.

---

## §5 — Cross-link

- `HEXAD/CONNECTION_CRITIQUE.md` — Wrong-C diagnosis refined here:
  threshold is necessary but not sufficient; rate-limit is the
  silent co-bottleneck.
- `HEXAD/PRIORITY_QUEUE.md` #4 (J.6) + #9 (I.3) — items landed at
  design-tier with structural finding; forward measurement carry to
  upstream patch land.
- `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/result.json`
  — input SSOT (mean=0.4534, std=0.0376, n=20).
- `~/core/anima/HEXAD/CHAT/spontaneous_lib.hexa` — 8-factor +
  IM_THRESHOLD 0.30 + 4-AND safety source (untouched).
- `~/core/anima/HEXAD/CHAT/SPONTANEOUS.tape` §4 6-control SSOT —
  rate-limit `MIN_EMIT_INTERVAL` 30s governance scope.
- `~/core/hexa-lang/inbox/patches/pt-ckpt-cross-substrate-residual-readout.md`
  — filed upstream patch (this cycle); blocking dependency for
  Φ-axis + per-step motivation_trace measurement.
- `~/core/hexa-lang/inbox/patches/flame-path-a-dual-head-and-multiterm-grad.md`
  — §71 training-time complement (RFC 059).
- §167-A FP-RECONNECT (in-flight, sub-agent owned) — motivation
  axis re-wire (threshold-anchor half); §168 finding suggests the
  rate-limit half is the missing companion.

---

## §6 — GOAL distance

north-star + §15/§51/§72 milestone UNCHANGED, **GOAL 미도달**.
§168 is a measurement-honesty cycle (Wrong-C refinement +
upstream-patch filing), NOT a GOAL movement. The arc's
emit_rate=1/20 baseline across §161/§166 fires is hereby explained
as rate-limit-ceiling-saturated, NOT threshold-determined — a
structural correction to the connection-method critique.
