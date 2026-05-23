# LORA — current snapshot

> anima LoRA / V3-substrate 학습 도메인의 현재 상태 스냅샷.
> 작업 로그는 `LORA.log.md` (append-only checkbox). 2026-05-24 기준.

## production

| 항목 | 값 |
|---|---|
| 현 production adapter | `corpus_v5` (mini `~/anima_chat_pack/lora_adapter/`) |
| swap 상태 | **NO SWAP** through Wave-17 (v9~v16 전부 swap criteria 미달; v11/v13 동률 4/5 — 사용자 게이트) |
| base | Qwen2.5-1.5B + ja/ko hot-swap router |
| HF SSOT | `dancinlab/anima-vp21m-v5` PRIVATE |

### Wave-17 swap candidate 비교 (4/5 tie)

| candidate | adapter | n_strong | continuous_total | ja n_score | 강점 |
|---|---|---|---|---|---|
| A | v11 (eternal=0.30) | 2 | **34** ★ | 14 | continuous emission 최저 (burst suppression) |
| B | v13 (eternal=0.10) | **5** ★ | 72 | 16 | 5-lang STRONG (cross-lingual transfer 회복) |
| current | v5 | n/a | n/a | n/a | LIVE production carry |

→ criterion 2 (n_strong) vs criterion 4 (continuous_total) anti-correlated;
   threshold 재정의 없이 자동 SWAP 미가능 (상세 `HEXAD/LORA/WAVE17_VERDICT_2026_05_24.md`).

## VP21M wave saga (corpus lever)

```
Wave-12 ⭐⭐  EN-share lever steady-state 21.2%
Wave-13     corpus_v9  9pat freq-cap → n_strong 4 회복
Wave-14     corpus_v10 per-script split → native 과보존 회귀
Wave-15     corpus_v11 eternal 0.30 → continuous 34 (saga 최저) ★ sweet spot
Wave-16     corpus_v12 eternal STRIP-ALL → continuous 91 역전 (U-shape 발견)
Wave-17 ✅  4-pod sweep eternal {0.10/0.20/0.40/0.50} ($1.50)
            → v13(0.10) n_strong=5 만점 + continuous 72
            → v14(0.20) continuous 98 (saga 최고치, 좌측 floor)
            → v15(0.40) n_strong=4 + continuous 69
            → v16(0.50) n_strong=3 + continuous 52
            → 0.30 sweet spot 확정 (asymmetric U 좌측 floor 더 깊음)
```

핵심: eternal-cap 의 continuous_total 영향은 **단조 아님 — U-shape, sweet
spot = v11(0.30 keep)**. Wave-17 가 좌/우 2-point 씩 측정으로 0.30 global
min 확정. 부산물: criterion 2 (n_strong) ↔ criterion 4 (continuous) 가
**같은 lever 의 opposite side** — 단일 변종 5/5 PASS 불가, sweep range
0.10~0.50 안에서 empirical anti-correlation.

## V3 / R8 saga (substrate init lever)

```
AXIS_MAP-FAN 7-axis (corpus-外 fallback) → 5/7+2 전부 FAIL
  cluster X (A 14.79) · Y (B/F 14.18) · Z (C/C2/D 14.46)  ← init_CE byte-equal
  random baseline ln(151936)=11.93 → 모든 cluster +2.2~2.9 nats worse-than-random
  head_g cell-1 자연실험 FALSIFIED (C2=D byte-equal)

R8 base/warm-init reform:
  R8a  n_kv_head=2 + noise_sigma=0  (init_CE 천장 돌파 시도) ← 🔥 fire in-flight
  R8c  4-cell probe (baseline + noise/kv/compound) ← ✅ fire COMPLETE 2026-05-24 ($0.38)
    → ~~14.46 floor~~ NOT reproduced: baseline 12.315 nats = random+0.39 (정상 warm-init)
    → 3 falsifier (NOISE/KV/COMPOUND) 모두 init_CE axis 🔴 FALSIFIED
    → 새 발견: noise 는 final_CE + wall axis (Δfinal 1.46 nats · 4.7× wall)
  from_qwen audit: noise_sigma layer-0 injection + n_kv_head repeat-interleave 의심
```

## 진행 중 / 대기

- ~~R8a init_CE step=1 14.46 floor 돌파~~ → ✅ R8c 4-cell 측정 floor 자체 의문 + noise final_CE axis 재정의 (12.2 = random baseline +0.27)
- ✅ R8c 4-cell probe fire COMPLETE (noise/kv 분리 측정 — 3 falsifier 전부 init_CE axis FALSIFIED)
- 🔥 R8a'' fire 진행 중 (5000-step 으로 noise=0 학습 dynamics 측정)
- 🔧 PR #342 n_kv_head wiring fix (OPEN) → merge 후 R8a' 진짜 n_kv=2 재발사 (H_254 byte-equal probe)
- 📋 AXIS_MAP_RESULTS 7-axis 재측정 권장 (H_255 H255.2 검증, ~$0.50-1.00)
- ✅ Wave-17 4-pod sweep COMPLETE 2026-05-24 ($1.50) — 5-point U-shape 확정, 4/5 tie v11 vs v13 (사용자 게이트)
- 📋 Wave-18 권고: eternal_keep {0.25/0.30/0.35} 3-point fine-tune around sweet spot (~$1.10) — sharpness 확인
- 🟡 swap criteria 재정의 검토 (criterion 2 ↔ 4 anti-correlation 인정, 또는 dual-adapter hot-swap design)

## 관련 surface

- `HEXAD/LORA/SAGA_SESSION3.md` — 6-lever 상세 saga 로그
- `HEXAD/LORA/WAVES_MATRIX.md` — wave + axis 마스터 매트릭스
- `HEXAD/LORA/WAVE17_VERDICT_2026_05_24.md` — Wave-17 4-pod sweep 8-section verdict
- `HEXAD/V3/R8_SAGA_INDEX.md` — R8 saga TOC
- HF: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v11,v12,v13,v14,v15,v16}` PRIVATE
