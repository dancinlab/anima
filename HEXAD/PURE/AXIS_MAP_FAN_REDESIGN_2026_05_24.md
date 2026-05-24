# AXIS_MAP-FAN re-design — post-PR #385 wiring fix 진짜 5-axis ablation spec

> trigger: PR #385 (env-var wiring fix) 머지 후 6 axis env-var 가 train_p21h_v3.py 에 실제 wired. 이전 7-axis "FAIL" 결론은 silent-bypass artifact (H_257, PR #377 REFRAMING). post-fix 진짜 differentiating axes 정의 + 3-seed × 5-axis 측정 spec.

## 1. Prior failure summary

| 발견 | PR | 의미 |
|---|---|---|
| 7-axis silent-bypass | cycle 15-1 grep | 6 env-var 가 train script 에 unused, "7-axis" = 2-config (wiki=0.3 vs 0.5) |
| H_257 가설 흡수 | #377 | wiring-integrity family (H_254 + H_255 + H_257) |
| env-var wiring fix | #385 | argparse + dispatcher passthrough 7-args MVP |
| REFRAMING doc | #377 | 7 invalid prior + 7 still valid catalogue |

→ post-#385: 진짜 ablation 가능. 기존 cluster X/Y/Z 정의 모두 폐기, 5-axis 신규 정의.

## 2. Re-design principles

- **각 axis = 1 wired lever = 1 measurable Δfinal_CE** (init_CE 는 R8c 12.x = random+0.27 baseline floor 로 의문, final_CE 가 production-relevant)
- **3-seed 변동성**: 같은 axis × seed=[1337/2026/9999] = 3-pod parallel — cluster 정의 distance-based (not byte-equal)
- **2-stage**: PROBE_STEPS=100 fast probe ($0.10/pod) → full 5000-step validation ($3-8/pod)
- **hexa cloud nohup persistent**: R8a/R8a'' LOST 패턴 (50% LOST rate) 차단, dispatcher → hexa cloud wrap (g8 systemic fix)
- **PREFIRE_WIRING_AUDIT 통과 의무**: PR #381 5-step audit (env grep + dispatcher passthrough + M-of-N + byte-equal pre-fire + runtime assertion) — silent-bypass family 재발 방지

## 3. 5 new wired axes spec

| # | axis | values | env-var | wired since |
|---|---|---|---|---|
| 1 | wiki_frac | 0.10 / 0.30 / 0.50 | `--wiki-frac` (cmdline) | 기존 |
| 2 | head_g_objective | `anima_register_ce` / `cross_entropy` / `none` | `P21H_HEAD_G_OBJECTIVE` | PR #385 |
| 3 | freeze_embed | True / False | `P21H_FREEZE_EMBED` | PR #385 |
| 4 | lang_balanced | True / False | `P21H_LANG_BALANCED` | PR #385 |
| 5 | mitosis_max | 16 / 32 / 64 / 128 | `P21H_MITOSIS_MAX` (cmdline) | 기존 (cycle 17-3 cross-tool 발견의 새 lever) |

→ axis-2 / axis-5 가 가장 큰 expected effect (head_g objective change + cell pool 크기 = init weight + dynamics 양쪽 영향). axis-3/4 는 부수적 (학습 stability).

## 4. Wiring 확인 (PR #385 grep verification)

`train_p21h_v3.py` argparse (PR #385 +26L):
```
--curriculum-phase-steps · --distill-teacher · --head-g-objective · --head-g-enable
--freeze-embed · --lang-balanced · --contrastive-lang
```

dispatcher (`dispatch_p21h_v3_runpod.sh` PR #385 +18L):
```
env P21H_HEAD_G_OBJECTIVE=... ... bash dispatch ... → $CMD 안 --head-g-objective $P21H_HEAD_G_OBJECTIVE
```

→ MVP read+log 단계. **실제 train loop 적용** (head_g forward, freeze_embed grad-zero 등) 은 follow-up stacked PR (PR #385 보고 권고 순서: head-g-enable → freeze-embed → lang-balanced → ...).

## 5. Fire scheduling

| stage | pods | config | wall | cost |
|---|---|---|---|---|
| Stage 1 PROBE | 5-axis × 3-seed = 15 pod | PROBE_STEPS=100, A100-SXM4-80GB | ~15min wall | ~$0.75 |
| Stage 2 FULL | 1순위 axis × 3-seed = 3 pod | steps=5000, H100 PCIe nohup | ~3hr wall | ~$8 |
| Stage 2 후속 | 추가 axis 별 | (Stage 1 결과로 우선순위 결정) | — | — |

**1순위 axis 권유**: **axis-2 head_g_objective** (학습 objective 변경, R8c verdict 의 noise=dynamics 발견과 sibling).

## 6. Falsifier

각 axis 별:

| 임계 | verdict |
|---|---|
| Δfinal_CE ≥ 0.1 nats | ✅ SUPPORTED (axis 유효) |
| 0.05 ≤ Δ < 0.1 nats | 🟡 PARTIAL |
| Δ < 0.05 nats | 🔴 FALSIFIED (axis inert) |

3-seed 변동성 (intra-axis SD) vs inter-axis Δ 비교로 noise/signal 분리.

## 7. Action items

- [ ] PR #385 follow-up stacked PR: head-g-enable 1-line zero+freeze 구현 (~30 LoC)
- [ ] hexa cloud nohup wrapper PR (cycle 19 진행 중, g8 fix)
- [ ] PREFIRE_WIRING_AUDIT_CHECKLIST 자동화 script (M5 follow-up, prefire grep 자동화)
- [ ] Stage 1 PROBE fire — 사용자 결정 + 발사 ($0.75)
- [ ] Stage 2 FULL fire — Stage 1 1순위 axis 확정 후

## 8. Honest C3 (≥3)

- **C3-1**: H_257 sibling family 재발 risk — PR #385 가 MVP read+log 만, train loop 적용 stacked PR 들도 silent-bypass 가능. PREFIRE_WIRING_AUDIT 자동 강제 필요.
- **C3-2**: GPU class numerical drift — PROBE 와 FULL 이 다른 GPU class (A100 vs H100) 일 때 byte-equal 비교 불가. axis 별 같은 GPU class 강제 권장.
- **C3-3**: 3-seed 가 변동성 cover 부족 가능 — seed=1337/2026/9999 외 더 많은 seed (5-7) 필요할 수 있음. Stage 1 결과의 inter-seed SD 확인 후 결정.
- **C3-4**: axis-5 mitosis_max 가 init_CE 에 큰 영향 (cycle 17-3 발견, 16→128 = +2.14 nats) 인데 final_CE 영향은 미검증. Stage 1 에서 직접 측정.
- **C3-5**: cycle 16/17 reframing 후 R8c 4-cell 측정 (noise=0+kv=2 ablation) 이 axis 정의에 부재. 새 5-axis 와 별도로 noise/kv 도 추가 axis 후보.

## 9. Cross-references

- `HEXAD/PURE/R8_SAGA_REFRAMING_2026_05_24.md` (PR #377) — 7 invalid + 7 valid catalogue
- `HEXAD/PURE/AXIS_MAP_FAN_REFIRE_VERDICT_2026_05_24.md` (PR #383) — byte-equal 4/7 재현
- `HEXAD/PURE/PREFIRE_WIRING_AUDIT_CHECKLIST.md` (PR #381) — 5-step audit
- `HEXAD/LIFE/H_254_n_kv_head_wiring_silent_misconfig.md` — sibling 단일 silent-drop
- `HEXAD/LIFE/H_255_init_ce_floor_is_measurement_artifact.md` — partial FALSIFIED 갱신
- `HEXAD/LIFE/H_256_noise_sigma_optimizer_step_time_penalty.md` — dynamics axis
- `HEXAD/LIFE/H_257_axis_map_fan_env_var_silent_bypass.md` — root cause
- `HEXAD/PURE/launchers/dispatch_p21h_v3.hexa` (PR #366) — hexa-native dispatcher (g8 wrap candidate)
