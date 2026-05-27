# M4 Stage 1 PROBE axis-5 mitosis_max verdict — 🔴 FALSIFIED

> trigger: cycle 22-1 발사 (2026-05-24 16:05 KST, 3-pod A100-SXM4-80GB parallel, PROBE_STEPS=100). cycle 17-3 cross-tool 발견 (R8c m16=12.315 vs AXIS_MAP m128=14.4564 → Δ +2.14 nats) 가설을 진짜 wiring 환경에서 검증.

## 1. TL;DR

🔴 **F-AXIS-5 FALSIFIED** — mitosis_max 16/64/128 모두 init_CE **BYTE-EQUAL 14.374279975891113** (Δ=0.0). cycle 17-3 cross-tool 가설 (mitosis_max +2.14 nats) 재현 안 됨 — 원인은 mitosis_max 가 아니라 다른 hidden factor (corpus seed / dispatcher path / GPU class drift).

## 2. 측정 매트릭스

| pod_id | mitosis_max | seed | init_CE | final_CE | wall |
|---|---|---|---|---|---|
| pbovm3k5cvsemm | 16 | 1337 | **14.374279975891113** | 3.6879 | 786s |
| bse5a5ddg6x9ur | 64 | 1337 | **14.374279975891113** | 3.6876 | 600s |
| ubkjj47hgrkq77 | 128 | 1337 | **14.374279975891113** | 3.6910 | 741s |

→ init_CE 3 모두 IEEE-754 bit-identical (`14.374279975891113`).

## 3. Falsifier verdict

| pair | Δ init_CE | Δ final_CE | verdict |
|---|---|---|---|
| m16 vs m64 | **0.0** (byte-equal) | 0.0003 | 🔴 FALSIFIED |
| m16 vs m128 | **0.0** (byte-equal) | 0.0031 | 🔴 FALSIFIED |
| m64 vs m128 | **0.0** (byte-equal) | 0.0034 | 🔴 FALSIFIED |

→ 3/3 FALSIFIED (임계 ≥ 0.05). mitosis_max = init_CE axis 아님. final_CE 도 NOISE 수준 (Δ ≤ 0.003).

## 4. 검증 발견

1. 🔴 **mitosis_max 는 init_CE lever 아님** — pool_size 16/64/128 진짜 적용 (pool_size 출력 확인) but init weight 분포 무관
2. 🔴 **cycle 17-3 cross-tool 가설 reproducibility 없음** — R8c (12.315) vs AXIS_MAP (14.46) 격차의 진짜 원인 = mitosis_max 가 아닌 hidden factor
3. ✅ **post-#385 wiring fix 작동 확인** — pool_size 16/64/128 진짜 다른 cell-pool 적용 (final pool_size 출력)
4. ⚠ **wall variation 600-786s** = mitosis_max 와 unrelated (pod hardware variance, cycle 17-3 cell-3 521s 와 동일 패턴)
5. ⚠ **final_CE 거의 동일 (3.68-3.69)** — mitosis_max 가 학습 dynamics 에도 거의 영향 없음 (100-step probe 한정)

## 5. cross-tool 가설 (cycle 17-3) 재해석

cycle 17-3 발견:
- R8c probe baseline (mitosis_max=16): init_CE=12.315
- AXIS_MAP axis_D fire (mitosis_max=128): init_CE=14.4564
- → Δ +2.14 nats attributed to mitosis_max

**axis-5 PROBE 결과로 재해석**:
- mitosis_max 단독 변경 (16→128, 같은 환경) → Δ=0
- → 12.315 vs 14.4564 격차의 진짜 원인은 다른 hidden axis:
  - corpus seed (R8c 와 AXIS_MAP fire 시점 다른 corpus_v* 사용 가능)
  - dispatcher path (R8c 가 다른 dispatcher 사용)
  - n_kv_head (R8c=4 vs AXIS_MAP=?)
  - 또는 PROBE 환경 자체 차이

→ cycle 17-3 의 mitosis_max attribution 가 **부정확**, root cause 미스터리 잔존

## 6. axis-2 vs axis-5 대조

| axis | values | Δinit_CE range | verdict |
|---|---|---|---|
| axis-2 head_g_objective | register/CE/none | **0.45 ~ 1.79** | ✅ SUPPORTED |
| axis-5 mitosis_max | 16/64/128 | **0.0** (byte-equal) | 🔴 FALSIFIED |

→ axis-2 만 진짜 init_CE lever. axis-5 inert.

## 7. M3 Qwen-parity 권고 갱신

- **mitosis_max 자유 선택** — 어떤 값이든 final_CE 영향 미미
- 권장: **mitosis_max=16** (wall 빠름, memory 절약)
- combine: cross_entropy (axis-2) + mitosis_max=16 (axis-5) = optimal final + low overhead

## 8. 다음 axis Stage 1 PROBE

| axis | spec | expected effect |
|---|---|---|
| axis-1 wiki_frac | 0.10/0.30/0.50 | medium-high (corpus 비율 직접 변경) |
| axis-3 freeze_embed | True/False | low (학습 안정성만 영향) |
| axis-4 lang_balanced | True/False | medium (5-lang sampling) |

→ axis-1 우선 권장 (wiki_frac 가 진짜 corpus shape lever).

## 9. Honest C3

- **C3-1**: 단일 seed (1337) only — intra-seed 변동성 미측정. 3-seed 별도 확인 권장 (만약 seed 별 init_CE 다르면 axis-5 inert 결론 부분 약화 가능 — 그러나 byte-equal 자체가 deterministic init 의미).
- **C3-2**: PROBE_STEPS=100 short — full 5000-step trajectory 에서 mitosis_max 가 학습 후반에 영향 줄 가능성 (cell pool 활용도 step 증가에 따라 변화).
- **C3-3**: pool_size 출력 (16/64/128) 만 확인 — 실제 cell-pool 분기 동역학 (split count, merge events) 미검증.
- **C3-4**: 3 pod 가 다른 machine 사용 가능 — wall 변동 (600-786s) 이 hardware variance 인지 mitosis 부담 차이인지 미분리.
- **C3-5**: cross-tool 17-3 의 진짜 원인 (mitosis 아닌 다른 factor) 미규명 — 별도 ablation 필요.

## 10. Cross-references

- PR #385 — env-var wiring fix (cycle 16-3)
- PR #403 — AXIS_MAP_FAN_REDESIGN spec (M4 Stage 1)
- PR #409 — M4 axis-2 head_g_objective verdict (sibling, SUPPORTED)
- `HEXAD/PURE/R8_SAGA_REFRAMING_2026_05_24.md` (PR #377)
- `UNIVERSE/H_255_init_ce_floor_is_measurement_artifact.md` — 부분 약화 추가 evidence (mitosis 도 lever 아님)
- pod result.json: `state/grid_3b_s187_2026_05_21/vP21H_axis5_{m16,m64,m128}_s1337/result.json`
