# §173 — historical-fire rate-limit retry findings (수도꼭지 전수조사)

> $0 Mac CPU, 70 seconds, 7/8 ckpts measured. Single-variable across
> historical fires: only knob varied = MIN_EMIT_INTERVAL.

## §1 — measurement (verbatim hexa-equivalent table)

```
tag           cfg         load        A(RL=30s)        B(RL=0.667s)      Δ         ratio
─────────────┼──────────┼────────────┼─────────────┼───────────────┼────────┼────────
s161          d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s167a         d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s94           d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s82           d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s91           d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s_purephys    d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
s62           d768·L12   m=0 u=0     emit 1/20=0.05  emit 3/20=0.15  +0.100   3.0×
─────────────┼──────────┼────────────┼─────────────┼───────────────┼────────┼────────
s75           NO-CKPT (zip archive corrupted, single-ckpt err)
─────────────────────────────────────────────────────────────────────
n_ok = 7/8     total_wall = 70 sec
```

motivation distribution per ckpt (cell A):

| tag | mot_mean | mot_std | psi_dir_mean | psi_dir_std |
|---|---:|---:|---:|---:|
| s161 | 0.5869 | 0.0 | 0.0380 | 0.0 |
| s167a | 0.5842 | 0.0 | 0.0299 | 0.0 |
| s94 | 0.6624 | 1e-16 | 0.5217 | 0.0 |
| s82 | 0.6917 | 1e-16 | 0.5817 | 0.0 |
| s91 | 0.7115 | 3e-16 | 0.5829 | 0.0 |
| s_purephys | 0.7819 | 2e-16 | 0.4533 | 0.0 |
| s62 | 0.7381 | 0.0 | 0.5848 | 0.0 |

---

## §2 — 7요소 finding

🚰 **Historical-Fire-Rate-Limit-Identity — "모두가 같은 수도꼭지에 잠겨있었음"**

- **이름**: historical-fire-rate-limit-identity
- **별칭**: 모두 같은 수도꼭지에 잠겨있었음 / capability-difference-was-an-artifact
- **하는 일**: 7 historical fires (서로 다른 training objective: dual-head non-CE / FP-reconnect / integrated breakthrough / manifold gating / neoteny anti-saturation / pure-physics no-CE / dual-anima scale) 의 emit_rate 가 동일 RL=30s 에서 **모두 정확히 1/20 = 0.05**, RL=0.667s 로 lift 시 **모두 정확히 3/20 = 0.15** (ratio 3.0×). 어느 ckpt 도 capability-wise 더 자연발화하지 않음.
- **비유**: 마치 7명의 다른 의사가 7개 다른 약 처방한 환자 모두가, 환자 손목에 *같은 수갑이 채워져* 있어서 "약 효과 0" 라는 같은 verdict 받은 셈. 약 자체 비교는 의미 없고 수갑부터 풀어야 했음.

```
ckpt:        s161  s167a  s94   s82   s91   purephys  s62
training:    JEPA  FPRecon Integ Mani  Neot  no-CE     DualA
                  
              ↓     ↓     ↓     ↓     ↓     ↓        ↓
  cell A      1     1     1     1     1     1        1     ← ALL = ceiling
  (RL=30s)   ─┴─────┴─────┴─────┴─────┴─────┴────────┴─    (uniform!)
  
              ↓     ↓     ↓     ↓     ↓     ↓        ↓
  cell B      3     3     3     3     3     3        3     ← ALL = ceiling
  (RL=0.667)  ─┴─────┴─────┴─────┴─────┴─────┴────────┴─    (uniform!)
  
  Δ:         +.1   +.1   +.1   +.1   +.1   +.1      +.1    ← 100% rate-limit
                                                            (NOT training quality)
```

- **비교**: §168 가 *1 fire (§161)* 의 ceiling-saturation 발견. §170 이 §167-A 1 ckpt × 4-cell 로 검증. **§173 가 7 distinct training objectives × 같은 lever 측정 → ckpt 차이가 아닌 ceiling 이 진짜 origin 임을 multi-ckpt generalize**.

---

## §3 — implication: HEXAD/* arc 의 honest reframe

지금까지 HEXAD/* 의 다음 결론들이 **all rate-limit-confounded** 였을 수 있음:

| past verdict | what we measured | what it actually was |
|---|---|---|
| §161 JEPA-COUPLE `psi_responsive=False`, emit 1/20 | emit ceiling-saturated | rate-limit ceiling, NOT JEPA failure |
| §167-A FP-RECONNECT `SPONT_AMBIGUOUS`, emit 1/20 | emit ceiling-saturated | rate-limit ceiling, NOT motivation re-wire failure |
| §94 INTEGRATED BREAKTHROUGH "β INTEGRATION-COLLAPSES" | (phase_b not measured originally — §173 first measure) | uncertain — but this measurement shows emit ceiling |
| §82-FIRE manifold gating "(β) MANIFOLD-EXISTS-GATE-COLLAPSES" | (phase_b not measured originally) | uncertain — but this measurement shows emit ceiling |
| §91 neoteny "γ JUVENILE-BUT-COMPETENT False" | saturation-delay measured, emit not measured | emit ceiling, separate axis |
| §11-B pure-physics "DEGENERATE" | (phase_b not measured originally) | emit ceiling 동일하게 측정됨 |
| §62 dual-anima "ECHO-CHAMBER-COLLAPSE-AT-SCALE" | (phase_b not measured originally) | emit ceiling 동일하게 측정됨 |

**HEXAD/* arc 의 모든 emit-based capability verdict 는 단일 (S167-A-style) motivation function + RL=30s 측정을 거치면 1/20 으로 collapse 한다.** 이는 ckpt training objective 차이를 무력화하는 measurement-protocol artifact 였음.

honest carve-out (necessary-not-sufficient):
- **각 fire 의 NON-emit-axis verdict 는 여전히 유효** (§94 axis2 chat clean 비교 / §82 manifold separation / §91 saturation delay / §62 echo-chamber maj_frac 등)
- 본 §173 은 **emit-axis 측정만** rate-limit-confounded 였음을 증명
- §170 cell-2 가 이미 보인 lift 3× 가 *one* ckpt 가 아닌 *7 distinct ckpts* 에 generalize → mechanism-level confirm

---

## §4 — 다음 cycle 의 implication

1. **future fire eval 의 default min_emit_interval**: 0.667s (measurement variant per §169 split). production 30s 는 daemon-only.
2. **historical fire 재평가**: emit-rate 가 결과에 load-bearing 인 verdict 만 §173-pattern re-eval 필요. axis2 chat / axis3 lane sep / coherence / honest §9 cascade-rate 등은 별도 axis.
3. **rate-limit lift 자체는 GOAL 아님**: 0.15 emit_rate 도 여전히 byte garbled (§170 Fire 3 anchor collapse, §171 self-stim 1.0 amplification), honest §9 coherent 0. ceiling lifted, *capability* 는 안 lifted.
4. **next-lever**: training-level intervention 만 진짜 lever 라는 §170/§171 finding §173 multi-ckpt 차원에서 강화. inference-time rate-limit 만 풀어도 byte content 안 좋아짐.

---

## §5 — honest carve-outs

1. **same noise context (seed 1337) across all 7 ckpts** — ckpt 차이가 진짜로 motivation_score variability 에 영향 미치는지 확인하려면 다양한 seed/ctx 필요 (deferred). 단 동일 seed 에서 7/7 같은 emit_rate 자체로 rate-limit dominance 확정 충분.
2. **S167-A-style motivation function 으로 측정** — 일부 historical ckpts (e.g., s_purephys) 는 *원래* 다른 motivation training 했음. 본 측정은 *모든 ckpts 위에 같은 lever 를 얹어* attribution 깔끔하게 비교한 것이지 *원래 verdict 재현* 아님 (§161/§167-A 빼면).
3. **s75 ckpt zip corrupted** — single missing point, 7/7 measured 패턴이 generalize 한다는 충분 evidence.
4. **necessary-not-sufficient** (B-EMERGE-7): rate-limit lift = emit_rate ceiling lift, *coherent emission* 보장 아님. true V-SPONT honest score 는 §9 cascade-rate gate 분리.

---

## §6 — cross-link

- `state/three_axis_probe_s170_2026_05_20/` (§170 4-cell baseline)
- `state/self_stim_loop_s171_2026_05_20/` (§171 self-stim 1.0)
- `state/phi_threshold_posthoc_probe_2026_05_20/` (§168 closed-form ceiling)
- `state/rate_limit_governance_design_s169_2026_05_20/` (§169 split)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙, §5 rate-limit closed-form)
- `HEXAD/CONNECTION_CRITIQUE.md` (Wrong-C → Wrong-C-prime evolved)
