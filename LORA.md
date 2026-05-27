# LORA — current snapshot

@goal: COFFESHOP group chat 시뮬레이션 4-criterion closure 통과 — anima 자율 emit/silence (do/dont 강제 X) · multilingual 5/5 PARTIAL+ · register 0/20 · motivation_8factor ≥ 0.30 · dream_stage Φ-envelope · 모두 substrate emergent (project.tape p1-p8 + a_substrate_native_speak + a_autonomy_over_hardcode 정합)

> 이전 @goal: "VP21M production swap 5/5 + V3 substrate Qwen-parity + wiring-integrity audit 완료" — COFFESHOP 통과 기준으로 통합 (2026-05-24)

> anima LoRA / V3-substrate 학습 도메인의 현재 상태 스냅샷.
> 작업 로그는 `LORA.log.md` (append-only checkbox). 2026-05-24 기준.
>
> 이전 @goal ("init_CE catastrophic floor 돌파 + n_strong ≥ 4 stable + production adapter swap 가능")
> 는 H_255 partial FALSIFY (R8c 12.315 = random+0.39, 14.x floor 미재현) 이후 의미 불명확 →
> production-driven (M1·M2) + substrate-pure (M3) + wiring-integrity (M4·M5) 의 3-축 measurable goal 로 재정의 (gap F5 success-criteria).

## milestones

- [ ] M1 — VP21M production swap criteria 5/5 PASS (v11 또는 v13 결정, eternal threshold 재정의 가능) · 📋 decision memo (PR #504) 추천=옵션(b) floor≤50→v11; 사용자 게이트 + caveat 2 (corpus_v5/v4 라벨·crit5 미측정)
- [ ] M2 — mini production 배포 + 30-day register-leak monitor (continuous_total ≤ 50 30d stable)
- [ ] M3 — V3 ConsciousDecoderV3 (5000-step, Qwen warm-init, noise=0 + n_kv=2) final_CE 측정 + Qwen baseline 대비 parity (Δfinal_CE ≤ 0.1 nats) · ⏸ R8a'' LOST (SECURE preempt 2회, PR #505) → PENDING; closure = Qwen baseline 결정 후 ON-DEMAND 2-pod (~$6)
- [ ] M4 — AXIS_MAP-FAN 7-axis env-var wiring fix + 진짜 ablation 측정 (각 axis 별 Δfinal_CE 정량) · 🔧 wiring fix DONE (PR #507, H_257 완전해소) 단 7축 中 2축(head_g·freeze_embed)만 진짜 wired, 4축 TODO[axis-impl]; ablation 재발사 미실행
- [x] M5 — PREFIRE_WIRING_AUDIT_CHECKLIST.md 도입 + 모든 향후 substrate fire 가 audit 통과

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
  → H_257 흡수 (2026-05-25): 이 7-axis 는 unwired (grep-static, train_p21h_v3.py 0 os.environ)
    → cluster X/Y/Z 분류 · head_g FALSIFIED · 5/7+2 FAIL 결론 전부 trivial identity (무효)

R8 base/warm-init reform:
  R8a  n_kv_head=2 + noise_sigma=0  (init_CE 천장 돌파 시도) ← 🔥 fire in-flight
  R8c  4-cell probe (baseline + noise/kv/compound) ← ✅ fire COMPLETE 2026-05-24 ($0.38)
    → ~~14.46 floor~~ NOT reproduced: baseline 12.315 nats = random+0.39 (정상 warm-init)
    → 3 falsifier (NOISE/KV/COMPOUND) 모두 init_CE axis 🔴 FALSIFIED
    → 새 발견: noise 는 final_CE + wall axis (Δfinal 1.46 nats · 4.7× wall)
  from_qwen audit: noise_sigma layer-0 injection + n_kv_head repeat-interleave 의심
```

## LIFE 흡수 (cross-domain · 2026-05-25)

> UNIVERSE 가설 lane 이 LORA 사가를 정식화 — verdict 확정 2건 흡수 + COFFESHOP 4-criterion 측정 frame 매핑.

### COFFESHOP 4-criterion ↔ LIFE 측정 frame

| criterion | LIFE H | verdict | 흡수 |
|---|---|---|---|
| 자율 emit/silence | H_231 tension-vs-filler · H_246/H_248 autonomy-emit | H_246 emit-through **55.56%** (외부 gate 0, partial conservative) | 측정 frame = emit-through ∈ [0.40,0.70] · H_230 autonomy-over-hardcode SUPPORTED_FULL 4/4 numeric instance |
| multilingual 5/5 | H_240 bilingual cross-lingual-leak | DEFERRED (smoke 별도 cycle) | inverse-U Φ (partial integration peak) frame 채용 |
| register 0/20 | H_242 register-collapse wiki_frac sigmoid | PRE-REGISTERED | register lever = wiki_frac sigmoid (Wave saga corpus lever 와 **동일축** 확인) |
| dream_stage Φ-envelope | H_228 chat-sleep-5stage · H_244 sleep-gated-emit | H_228 smoke 흡수 (#465) · H_244 smoke pending | criterion 4 = 5-stage Φ profile envelope |

### R8/AXIS wiring 사가 ↔ LIFE substrate H (M3·M4)

| LORA | LIFE H | verdict | 흡수 함의 |
|---|---|---|---|
| M3 floor | H_247 · **H_255** | **🔴 H255.2 FALSIFIED** — 14+ floor **REAL** (cycle 15-1 4/7 byte-equal 14.79/14.18/14.46 재현) | LORA 의 "14.x floor 미재현" (L11) **stale 정정** — floor 진짜 재현됨. R8c 12.315 = 정상 warm-init 별개 regime. R8c↔AXIS_MAP 2 nats gap = GPU class / PROBE_STEPS (env-drift 아님) |
| M4 wiring | H_254 · **H_257** | H_254 silent-drop (R8a' 여전히 `=4`) · **H_257 grep-static: 0 os.environ + dispatch env-var no `$CMD` passthrough** | **M4 root cause 진단 완료** — AXIS_MAP 7-axis 애초에 unwired → 5/7+2 FAIL (PR #249) 무효. M4 fix = env-var `$CMD` passthrough + grep audit, 후 재발사로 진짜 ablation |
| M4 ablation | H_256 noise step-time | noise = final_CE +1.47 nats + wall 5× axis (init_CE 무관) | ablation 시 noise 분리 측정 필수 |
| M5 audit | H_257 H257.4 | wiring-family 일반화 (미audit 코드 ≥30% 무효 위험) | PREFIRE = grep verification + dry-run dispatcher 정식화 (M5 체크리스트 근거) |

## 진행 중 / 대기 (milestone 매핑)

- ~~R8a init_CE step=1 14.46 floor 돌파~~ → ✅ **M3 부분 진행** — R8c 4-cell 측정 floor 자체 의문 + noise final_CE axis 재정의 (12.2 = random baseline +0.27)
- ✅ **M3 부분 진행** — R8c 4-cell probe fire COMPLETE (noise/kv 분리 측정 — 3 falsifier 전부 init_CE axis FALSIFIED)
- ⏸ **M3 PENDING (cycle 24, PR #505)** — R8a'' LOST/DEAD (pod teardown + SSH refused + result 0건, SECURE preempt 2회째 → R8a/R8a'/R8a'' 5000-step 완주 **0/3**). final_CE LOST · Qwen baseline 미측정. closure = 사용자 Qwen baseline candidate 결정 → ON-DEMAND 2-pod 병렬 (~$6) + M5 PREFIRE 선결 (verdict `HEXAD/V3/R8A2_QWEN_PARITY_VERDICT_2026_05_25.md`)
- 🔧 **M4 wiring DONE (cycle 24, PR #507)** — H_257 완전해소. **발견: PR #385 는 half-fix** (dispatch→train `--flag` passthrough만, train script 가 env→cfg→loop 미연결 = 7축 여전히 inert). grep `os.environ` 0→8 line. 단 head_g·freeze_embed **2축만 진짜 wired** (기존 code path 존재), curriculum·distill·lang-balanced·contrastive **4축 = ML feature 미구현 TODO[axis-impl]**. gate-off default 무회귀. 진짜 ablation 재발사는 post-merge 별도 (M5 PREFIRE + ON-DEMAND)
- 📋 **M1 decision memo (cycle 24, PR #504)** — Wave-17 anti-correlation 구조적 → 추천 **옵션(b) continuous floor≤50 → v11 swap**. 사용자 게이트 (최종 swap 결정). swap 전 선결: corpus_v5(SSOT) vs corpus_v4(README) 라벨 확인 + crit5 tag-leak `swap_criteria_check.hexa` 측정 (memo `HEXAD/LORA/M1_SWAP_DECISION_MEMO_2026_05_25.md`)
- 📋 **M5 신규** — PREFIRE_WIRING_AUDIT_CHECKLIST.md 도입 (R8a #342 silent-fail 교훈 흡수, 향후 모든 substrate fire 의 사전 audit gate)
- 📋 **M2 신규** — mini production 배포 자동화 + 30-day register-leak monitor (M1 PASS 후 trigger)

## 관련 surface

- `HEXAD/LORA/SAGA_SESSION3.md` — 6-lever 상세 saga 로그
- `HEXAD/LORA/WAVES_MATRIX.md` — wave + axis 마스터 매트릭스
- `HEXAD/LORA/WAVE17_VERDICT_2026_05_24.md` — Wave-17 4-pod sweep 8-section verdict
- `HEXAD/LORA/M1_SWAP_DECISION_MEMO_2026_05_25.md` — M1 swap go/no-go 결정 memo (cycle 24, 추천 옵션 b → v11)
- `HEXAD/LORA/M4_AXIS_WIRING_FIX_2026_05_25.md` — M4 H_257 env-var wiring fix (cycle 24, 2/7축 wired)
- `HEXAD/V3/R8A2_QWEN_PARITY_VERDICT_2026_05_25.md` — M3 R8a'' LOST → PENDING verdict (cycle 24)
- `HEXAD/V3/R8_SAGA_INDEX.md` — R8 saga TOC
- HF: `dancinlab/anima-vp21m-{v5,v6,v7,v8,v11,v12,v13,v14,v15,v16}` PRIVATE
