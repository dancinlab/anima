# LORA — current snapshot

> anima LoRA / V3-substrate 학습 도메인의 현재 상태 스냅샷.
> 작업 로그는 `LORA.log.md` (append-only checkbox). 2026-05-24 기준.

## production

| 항목 | 값 |
|---|---|
| 현 production adapter | `corpus_v5` (mini `~/anima_chat_pack/lora_adapter/`) |
| swap 상태 | **NO SWAP** through Wave-16 (v9~v12 전부 swap criteria 미달) |
| base | Qwen2.5-1.5B + ja/ko hot-swap router |
| HF SSOT | `dancinlab/anima-vp21m-v5` PRIVATE |

## VP21M wave saga (corpus lever)

```
Wave-12 ⭐⭐  EN-share lever steady-state 21.2%
Wave-13     corpus_v9  9pat freq-cap → n_strong 4 회복
Wave-14     corpus_v10 per-script split → native 과보존 회귀
Wave-15     corpus_v11 eternal 0.30 → continuous 34 (saga 최저) ★ sweet spot
Wave-16     corpus_v12 eternal STRIP-ALL → continuous 91 역전 (U-shape 발견)
Wave-17     spec only  eternal 0.10/0.20/0.40/0.50 sweep (GO, 사전검증 linear)
```

핵심: eternal-cap 의 continuous_total 영향은 **단조 아님 — U-shape**, sweet spot = v11(0.30 keep).

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
- 🟡 Wave-17 fire 미발사 (R8c verdict + R8a'' 결과 후 우선순위 재평가, marginal value 재계산)

## 관련 surface

- `HEXAD/LORA/SAGA_SESSION3.md` — 6-lever 상세 saga 로그
- `HEXAD/LORA/WAVES_MATRIX.md` — wave + axis 마스터 매트릭스
- `HEXAD/V3/R8_SAGA_INDEX.md` — R8 saga TOC
- HF: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v11,v12}` PRIVATE
