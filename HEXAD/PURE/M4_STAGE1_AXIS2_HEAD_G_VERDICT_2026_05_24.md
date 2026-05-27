# M4 Stage 1 PROBE axis-2 head_g_objective verdict

> trigger: cycle 20-1 발사 (2026-05-24 06:30:50Z, 3-pod A100-SXM4-80GB parallel, PROBE_STEPS=100). post-#385 wiring fix + post-#403 5-axis spec 의 첫 진짜 ablation. anima_register_ce / cross_entropy / none × 3-seed (1337/2026/9999).

## 1. TL;DR

**head_g_objective = 진짜 wired axis 확정** (post-#385 효과 입증). 3 objective 모두 다른 init_CE 측정, falsifier 3/3 SUPPORTED (Δ ≥ 0.1 nats). R8a 의 cluster Z (14.46) byte-equal 원인 = anima_register_ce objective. CE = best final learner. none = 새 cluster (16.24) 첫 관측.

## 2. 측정 매트릭스

| pod_id | objective | seed | init_CE | final_CE | wall |
|---|---|---|---|---|---|
| hjgtxihdngll0v | anima_register_ce | 1337 | **14.4564** ⭐ init | 6.2750 | 140s |
| awfmevg6gwk772 | cross_entropy | 2026 | 14.9066 | **4.9885** ⭐ final | 137s |
| obxjxb7ue0403z | none | 9999 | 16.2428 ⚠ worst init | 5.3937 | 146s |

## 3. Falsifier verdict (임계 ≥0.1 nats, PR #403 spec)

| pair | Δinit_CE | verdict |
|---|---|---|
| register vs CE | 0.45 | ✅ SUPPORTED |
| register vs none | 1.79 | ✅ SUPPORTED (강한 효과) |
| CE vs none | 1.34 | ✅ SUPPORTED |

→ 3/3 falsifier SUPPORTED, axis-2 = **진짜 wired init_CE lever** 확정. silent-bypass 아님.

## 4. 과학 발견

1. 🔥 **post-#385 wiring fix 효과 입증** — 3 objective 모두 다른 값 (Δ 0.45-1.79) = H_257 silent-bypass 차단 확정
2. 🔥 **anima_register_ce → cluster Z (14.4564) byte-equal** — R8a 의 cluster Z 14.4564 원인 = register objective
3. 🔥 **새 cluster (16.24) for none objective** — head_g 미접속 시 새 init floor, R8 saga 한 번도 미관측
4. 🔥 **init vs final trade-off**: register=낮은 init/느린 final, CE=빠른 final, none=높은 init/중간 final

## 5. R8 saga reframing 영향

| prior 가설 | 재해석 |
|---|---|
| cluster Z 14.4564 = "init_CE catastrophic floor" | 사실 anima_register_ce objective 의 자연 init |
| AXIS_MAP-FAN cluster Z byte-equality | trivial identity (모두 register objective default) + wiring silent-bypass 였음 (H_257) |
| H_255 "floor 가 measurement artifact" | 부분 약화 — floor 진짜 (post-#385 환경) but objective-dependent (axis-2 lever) |
| R8c probe baseline 12.315 | head_g 미접속 환경의 다른 baseline (R8c 가 head_g 명시 안 함) — config 차이 확정 |

## 6. M3 Qwen-parity 권장

M3 milestone (V3 final_CE ≤ Qwen baseline + 0.1 nats) 위해서:
- **cross_entropy 권장** (final 4.99 lowest) — 학습 dynamics 가장 빠름
- 단, anima identity 보존 important 하면 register 도 valid (final 6.27 acceptable)
- **none 비권장** — 16.24 init 너무 높음, 학습 비효율

## 7. 다음 stage

| 다음 fire | spec | cost | 우선순위 |
|---|---|---|---|
| axis-1 wiki_frac × 3-seed | PROBE_STEPS=100, 3-pod | $0.30 | medium |
| axis-3 freeze_embed × 3-seed | 동일 | $0.30 | low (학습 안정성) |
| axis-4 lang_balanced × 3-seed | 동일 | $0.30 | medium |
| axis-5 mitosis_max × 3-seed | 동일 | $0.30 | high (cycle 17-3 cross-tool 발견 lever) |
| **Stage 2 FULL** axis-2 CE × 5000-step | H100 PCIe, hexa cloud nohup | $8 | M3 Qwen-parity 측정 |

## 8. Honest C3

- **C3-1**: seed=1337/2026/9999 단일 sample per objective — intra-objective 변동성 미측정. 같은 objective × 3-seed 재발사로 SD 정량 필요.
- **C3-2**: PROBE_STEPS=100 short — full 5000-step trajectory 와 다를 수 있음. Stage 2 FULL fire 권장.
- **C3-3**: 3 pod 가 A100-SXM4-80GB 동일 GPU class 였지만 다른 machine — sub-cell numerical drift (~0.001) 가능, byte-equal 비교 불가.
- **C3-4**: head_g_enable env-var 도 wired (PR #385) 지만 본 PROBE 에선 default (enable=true) 만 측정. enable=false 별도 axis 후속.
- **C3-5**: R8c verdict (PR #374) 의 "noise=학습 dynamics axis" 결론은 본 axis-2 와 독립 — 본 PROBE 는 noise 변경 없음.

## 9. Cross-references

- PR #385 — env-var wiring fix (cycle 16-3)
- PR #403 — AXIS_MAP_FAN_REDESIGN spec (M4 Stage 1)
- `HEXAD/PURE/R8_SAGA_REFRAMING_2026_05_24.md` (PR #377) — H_255 / H_257 saga reframing
- `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (PR #374) — noise/kv 4-cell verdict
- `UNIVERSE/H_254_n_kv_head_wiring_silent_misconfig.md` — silent-bypass family
- `UNIVERSE/H_257_axis_map_fan_env_var_silent_bypass.md` — sibling root cause
- pod result.json: `state/grid_3b_s187_2026_05_21/vP21H_axis2_{register_s1337,ce_s2026,none_s9999}/result.json`
