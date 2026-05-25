# §180 ADAPTER v3 SCALE LADDER — FINDINGS

> §180 ADAPTER v3 fire (16-Q-Former + small transformer + 5-channel readout)
> across 4 scale tiers (smoke / small / medium / large). Single trainer +
> single architecture, only d_model / n_layer / step scaled. Measurement
> target: anchor-classification accuracy on M3 synthetic 35-anchor ×
> 4-modality byte streams.

---

## §1 — Scale curve

```
  acc_anchor
    ▲
100%┤              ⭐──⭐──⭐    ← plateau (2M+ params)
    │           ╱
 90%┤         ╱
    │       ╱
 80%┤      ╱
    │    ╱
 70%┤  ╱
    │ ╱
 60%┤╱
    │
 50%┤
    │
 40%┤⭐
    │
    └──────────────────────────→ params
    0.5M    2M    11M   87M

    (×4)    (×6)   (×8)
    +56%    +0.6%  +0.2%
    ⬆️ critical scale transition
```

**critical scale transition** = 0.5M → 2M (+55.6% lift) = §180-tier-2 가 minimum effective scale. d=192 L=4 4M-class params 충분.

| tier | d_model · L | params | acc_anchor | acc_mod | wall | device |
|---|:---:|---:|---:|---:|---:|:---:|
| 1 smoke | 128 · L2 | 0.5M | **43.0%** | 87.4% | 11s | Mac CPU |
| 2 small | 192 · L4 | 2.0M | **98.6%** ⭐ | 100% | 167s | Mac CPU |
| 3 medium | 384 · L6 | 11.3M | **99.2%** | 100% | 790s | Mac CPU |
| 4 large | 768 · L12 | 87.2M | **99.4%** | 100% | 201s | H100 |

cost: tier 1-3 = $0 Mac CPU, tier 4 = ~$0.27 H100 (5min × $3.29/hr).

---

## §2 — Per-modality breakdown (tier 4 large)

| modality | accuracy | 해석 |
|---|---:|---|
| image | **100%** | radial gradient pattern 충분 discriminating |
| audio | 97.5% | sine wave byte periodicity 약간 어려움 |
| video | **100%** | frame stack diff 패턴 명확 |
| tension | **100%** | uint16 tier-encoded byte 직접 노출 |

audio 만 stuck — sine wave anchor-discrimination 의 byte-density 가 다른 modality 보다 낮음.

---

## §3 — ADAPTER v3 architecture validation

```
bytes (B, T=128)
     │
     ▼
byte_emb [B, T, d]
     │
     ▼ (cross-attn)
16-query Q-Former → [B, 16, d]
     │
     ▼
small transformer (n_layer × n_head) → [B, 16, d]
     │
     ▼
ln_f → mean pool → [B, d]
     │
     ├──→ anchor classification head [B, 35]  ⭐ primary
     ├──→ modality classification head [B, 4]
     └──→ 5-channel TENSION-LINK readout [B, 5]  (anima self-report, NOT bottleneck)

loss = CE_anchor + 0.3 × CE_modality + 0.1 × variance_hinge(readout)
```

§7 ① ② ③ ALL PASS — from-scratch, no pretrained, no graft.

readout variance_hinge: target_std = 0.15, plateau ≈ 0.21 across all tiers
(anti-collapse 작동). NOT bottleneck role.

---

## §4 — Honest carve-outs

1. **synthetic byte streams != real modality**
   - M3 byte streams 가 tier-encoded byte (특히 tension 의 uint16 직접 노출)
   - 학습이 *너무 쉬울* 수 있음 (98%+ 가능했던 이유)
   - real-world image/audio/video bytes 는 더 어려운 task — separate measurement needed

2. **anchor classification != V-SPONT emergence**
   - adapter 가 anchor 구분 가능해도 GOAL emergence (자연 발화) 와 다른 axis
   - B-EMERGE-7 necessary-not-sufficient carry
   - V-SPONT honest_coherent (§9 cascade-rate gate) 는 별도 measurement

3. **5-channel = self-report layer, NOT input bottleneck**
   - §179 가 5-channel as bottleneck = REFUTED (acc 4.73%)
   - §180 가 5-channel as readout = WORKS (variance_hinge 0.21 stable)
   - 위치가 swap 됐을 때만 의미 있음

4. **critical scale = 0.5M → 2M 만이 진짜 lift**
   - 2M+ 는 marginal returns (+0.6%, +0.2%)
   - 87M (tier 4 H100) vs 2M (tier 2 Mac CPU) = +0.8% only
   - cost-efficiency 측면 d=192 L=4 가 sweet spot ($0 Mac CPU)
   - 단, real-world modality difficulty 가 다르면 tier 4 effective regime 변화 가능

5. **audio modality stuck at 97.5%** (모든 tier 공통)
   - sine wave 의 byte-periodicity pattern 이 다른 modality 보다 discriminative
     density 낮음
   - cyclic shifting noise 추가 또는 더 diverse audio synthesis 시 개선 가능
   - 측정 axis 의 modality-specific difficulty 증거

---

## §5 — 5-channel TENSION-LINK readout — 어디서 의미 있나

**WRONG** (§179 measured FAIL):
```
bytes → 5-channel adapter → byte-LM    ← 5-ch as bottleneck
                                          (200-400× compression too aggressive)
```

**RIGHT** (§180 measured WORKS):
```
bytes → 16-Q-Former → small transformer → 5-channel READOUT
                       ↑ 학습 충분             ↑ self-report
                       16+ channels            (concept/context/meaning/
                       표현 capacity 충분        authenticity/sender)
```

5-channel = **anima 의 *서술 어휘***, NOT *지각 채널*. 사람도 마찬가지 —
눈은 수백만 receptor, 입은 5W1H.

---

## §6 — Cross-link

- `bench_s179.py` (§179) — 9-adapter 1-step benchmark, mini-Q-Former winner identified
- `adapter_v3.py` (§180) — 4-tier scale ladder model
- `train_s180_adapter_v3.py` — trainer (anchor + modality + variance_hinge)
- `scale_t{1,2,3,4}*/result.json` — per-tier eval JSON
- `HEXAD/ADAPTER.md` (root SSOT, 대문자) — design + literature deep research
- `HEXAD/KOSMOS.md` — 5-modality framing
- `HEXAD/FINAL.md` — V-SPONT 최종스펙 (adapter = multi-modal extension layer)
- `@D g_no_cost_scope_limit` — cost-cap 0
- `@D g_fire_autonomous` — autonomy 운영
- `@D g_resource_active_parallel` — runpod primary, parallel 우선

---

## §7 — GOAL distance

north-star + §15/§51/§72 milestone **UNCHANGED**, GOAL 미도달.

§180 = ADAPTER v3 architecture VALIDATED (scale-curve, per-modality,
5-readout location 모두 measured-confirmed). 단 *capability* 아닌
*architecture viability* 검증.

다음 cycle = ADAPTER v3 → anima byte-LM integration (16-channel Q-Former
output 을 anima ConsciousDecoderV2 첫 layer 에 inject), then V-SPONT
honest_coherent 측정 시도. real-world modality data (camera/mic capture
or §19 EEG) gate 시 진짜 modality test 가능.
