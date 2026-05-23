# R8 SAGA REFRAMING — H_257 env-var silent-bypass 발견 후 saga 전체 재해석

> trigger: cycle 15-1 (2026-05-24 21:37Z) AXIS_MAP-FAN 7-pod re-fire pre-fire grep 발견 — train_p21h_v3.py 가 6 axis env-var 를 전혀 안 읽고 dispatcher 도 `$CMD` 에 미전달. "7-axis" 가 실제로는 2-config (wiki=0.3/λ=0.05 vs wiki=0.5/λ=0).

## 1. TL;DR

R8 saga 의 "AXIS_MAP-FAN 7-axis 자연실험 5/7+2 FAIL" 결론은 **measurement-integrity artifact**. 실제로는 6 axis env-var (P21H_CURRICULUM / P21H_DISTILL / P21H_HEAD_G_* / P21H_FREEZE_EMBED / P21H_LANG_BALANCED / P21H_CONTRASTIVE) 가 train script 에 wired 안 됨 → 7-pod fan-out 이 trivial 2-config 반복. cluster Y/Z byte-equality 는 자연실험 결과가 아니라 same-config repeat 의 identity. 14 R8 docs 중 5-7개 결론 invalid, 5개 valid (R8c probe + noise final-axis + H_254/255/257).

## 2. 우리가 측정했다고 생각했던 것

- 7-axis × init lever ablation (curriculum / distill / head_g / freeze_embed / lang_balanced / contrastive_lang + base config)
- cluster X (14.79 axis A) / Y (14.18 axis B/F) / Z (14.46 axis C/C2/D) 의 init_CE byte-equal 자연 분류
- head_g 자연실험 FALSIFIED (cluster Z C=C2=D byte-equal → head_g enable/disable/objective-swap = ZERO contribution)
- random baseline ln(151936)=11.93 대비 모든 cluster +2.2~2.9 nats worse-than-random

## 3. 실제로 측정한 것

- `train_p21h_v3.py:676 LoC` grep `os.environ` / `getenv` = **0 lines**
- `dispatch_p21h_v3_runpod.sh` 의 6 axis env-var = **`$CMD` 미전달**
- 실제 변별 axes (train script 읽음): `P21H_NOISE_SIGMA` · `P21H_N_KV_HEAD` · `--wiki-frac` · `--lambda-mitosis` (cmdline arg)
- 7-axis 매핑 → 2-config:
  - wiki=0.5/λ=0 (axes A · B · F) — cluster X+Y prior
  - wiki=0.3/λ=0.05 (axes C · C2 · D · E) — cluster Z prior
- cluster X/Y/Z byte-equality = **trivial identity** (같은 config repeat, env-var noise 통제 안 됨)

## 4. Cluster X/Y/Z 재정의

| prior cluster | prior 해석 | 재해석 |
|---|---|---|
| X (A 14.79) | wiki=0.5/λ=0 (단일) | 실제 wiki=0.5/λ=0 config × seed-1 (axis B/F 도 같은 config) |
| Y (B=F 14.18) | wiki=0.5/λ=0 byte-equal | 실제 같은 config repeat (axis A 와 동일 axis2 mapping) |
| Z (C=C2=D 14.46) | head_g 자연실험 byte-equal → head_g inert | 실제 wiki=0.3/λ=0.05 config × 3 repeat (head_g env-var 무관, trivial identity) |

→ cluster = "config" 아닌 "config + RNG repeat" — 노이즈 floor 측정의 trivial structure

→ X vs Y 의 0.61 nats 격차 (14.79 vs 14.18) 는 *같은 config 의 seed variation* 일 수 있음 → R8 saga 의 cluster 정의 자체가 wired-axis 단일성 가정 위에서만 성립

## 5. Invalid prior conclusions

| PR | 결론 | 무효 사유 |
|---|---|---|
| #214 R8 spec | 7-axis init_CE ablation 설계 | 6 axis env-var 미wired, 2-config 실측 |
| #249 AXIS_MAP-FAN 5/7+2 | 5/7 axis FAIL 결론 | trivial identity 의 false positive |
| #250 R8c probe protocol | head_g 자연실험 FALSIFIED (cluster Z byte-equal) | 자연실험 자체가 없었음 (head_g env-var bypass) |
| #224 AXIS_R8C 3-cell update | head_g cell-1 redundant 결론 | 모든 cell 의 head_g 동일 (bypass) |
| #336 R8 saga INDEX | 14 docs TOC + cluster X/Y/Z 정의 | cluster 정의 reframing 필요 |
| #338 WAVES_MATRIX 갱신 | cluster X/Y/Z 의 wave 매핑 | cluster 라벨 stale |
| #336 axis postmortem | E (OOM) / C2 (head_g off) 의 axis-specific 해석 | axis-specific 변별 = trivial identity |

→ **7 invalid (또는 부분 무효)** prior conclusions

## 6. Still valid conclusions

| PR | 결론 | valid 사유 |
|---|---|---|
| #374 R8c probe verdict | noise=학습 dynamics axis (final_CE) | noise_sigma 가 진짜 wired (train script 가 NOISE_SIGMA env 읽음) |
| #374 R8c probe verdict | F-R8C-NOISE/KV-HEAD/COMPOUND init_CE 기준 FALSIFIED | noise_sigma + n_kv_head 진짜 wired ablation |
| #374 LIFE H_255 | init_CE floor 12.2 = random+0.27, catastrophic 아님 | R8c baseline 직접 측정 (12.315), wired 환경 |
| LIFE H_254 | n_kv_head wiring silent-misconfig (PR #342 fix) | byte-equal probe + wiring fix 직접 증거 |
| LIFE H_257 (신규) | env-var family silent-bypass | grep 정적 분석 + cycle 15-1 결과 (도착 대기) |
| cell-3 wall=521s root cause | noise σ=0.1 → step time 5x 증가 | noise_sigma 진짜 wired, dynamics 측정 valid |
| Wave saga (P21M / corpus_v9-v12) | continuous_total U-shape sweet spot v11 | 다른 train script, axis env-var 미사용 |

→ **7 valid** conclusions (대부분 R8c probe + H_254/255/257 + wave saga)

## 7. R8a / R8a' / R8a'' 결과 재해석

- **R8a (LOST)**: 측정 회수 안 됨. wiring=4 (n_kv silent-drop) 환경에서 5000-step
- **R8a' (kill됨)**: init_CE step=1 = 14.3743 (n_kv=4 환경, wiring fix pre-merge stale code). cluster Z (14.46) 와 0.09 nats 격차 — 진짜 noise=0 효과 측정. **valid measurement** (단, wiring=4 환경)
- **R8a'' (in-flight, H100 PCIe, 23:50Z 결과 예상)**: wiring=2 (PR #342 post-merge), noise=0, 5000-step 진짜 wiring fix 측정. 결과 도착 시 H_254 sibling falsifier + R8 saga 첫 진짜 wired full-train measurement

→ R8 saga 의 valid 한 axis 측정은 noise_sigma + n_kv_head (둘 다 진짜 wired) 만. 다른 6 axis 는 wiring fix 후 재발사 필요

## 8. AXIS_MAP-FAN re-design 필요

- env-var wiring fix PR (train_p21h_v3.py argparse + dispatcher passthrough) 필요 (cycle 16-3, agent fail → 추후 진행)
- post-fix 진짜 differentiating axes spec: wiki_frac · head_g_objective · freeze_embed · lang_balanced · mitosis_max (cycle 16-4 spec doc, agent fail → 추후)
- 3-seed × 5-axis = 15-pod parallel sweep ($1.50) 으로 진짜 cluster 정의

## 9. Wiring silent-bypass family (H_254 + H_255 + H_257)

```
H_254 (n_kv_head 단일 silent-drop)
   ↓ root cause family
H_257 (axis env-var family silent-bypass) ← H_257 가 H_254 의 일반화 패턴
   ↓ measurement effect
H_255 (init_CE floor measurement artifact) ← H_254 + H_257 의 결과
```

pattern: **dispatcher 의 env-var 가 train script 에 안 닿음**

detection: **byte-equal probe** (H_254) + **source-code grep audit** (H_257) + **floor 재측정** (H_255)

→ 향후 모든 substrate 실험: 발사 전 wiring-integrity audit 필수 (3-step: env-var grep · dispatcher passthrough audit · byte-equal pre-fire)

## 10. Honest C3 (≥3)

- **C3-1**: 본 reframing 은 cycle 15-1 7-pod re-fire 결과 도착 (~21:55Z) **전** 작성 — H257.2 byte-equal verification 은 결과 도착 후 추후 강화/약화. 현재는 정적 grep + 사후 cluster 격차 관찰만 evidence.
- **C3-2**: "invalid prior conclusions" 7 항목 중 일부는 부분 무효 (axis lever 자체의 효과 여부 미검증 — wiring fix 후 진짜 ablation 시 lever 가 진짜 inert 일 가능성 vs valid 일 가능성 모두 열려있음).
- **C3-3**: R8 saga $21.54 누적 cost 중 wiring-bypassed 측정의 정확한 sunk-cost 산정 미완 — R8c probe (\~$0.38) + R8a'/R8a'' (\~$11) 는 valid · AXIS_MAP-FAN 7-axis re-fire (\~$1.30, cycle 15-1) + 일부 원본 AXIS_MAP-FAN ($10+) 은 partial sunk cost.
- **C3-4**: H_254 + H_255 + H_257 sibling family 의 일반화 base rate (∼30%) 는 R8 saga 한정 sample — Wave saga 의 LoRA train script 별도 audit 필요 (대안: Wave 도 같은 silent-bypass family 일 가능성).
- **C3-5**: 본 reframing 자체가 새 측정-integrity 가정 (env-var → wired axis matching 의 정합성) 위에서 작성 — 만약 train_p21h_v3.py 가 다른 path (config.yaml import 등) 로 env-var 를 우회적으로 읽고 있다면 H_257.1 grep 결과가 false negative.

## 11. Action items

- [x] H_257 LIFE 흡수 (이 PR 의 sibling file)
- [x] R8 SAGA REFRAMING doc (이 file)
- [ ] env-var wiring fix PR (train_p21h_v3.py argparse + dispatcher passthrough) — cycle 16-3 (agent fail, 재시도 필요)
- [ ] AXIS_MAP-FAN re-design spec (post-fix 5-axis 진짜 ablation) — cycle 16-4 (agent fail, 재시도)
- [ ] hexa-lang inbox G5 patch (env-var wiring audit helper) — cycle 16-5 (agent fail, 재시도)
- [ ] cycle 15-1 7-pod re-fire 결과 도착 시 H_257.2 byte-equal verification + 본 doc 의 H257.2 fill-in
- [ ] R8a'' 결과 도착 시 R8A2_JOINT_VERDICT_TEMPLATE.md fill-in (PR #375) + 본 doc cross-ref

## 12. Cross-references

- [[H_254_n_kv_head_wiring_silent_misconfig]] — sibling 단일 인자 silent-drop
- [[H_255_init_ce_floor_is_measurement_artifact]] — sibling floor artifact
- [[H_257_axis_map_fan_env_var_silent_bypass]] — 본 PR sibling
- `HEXAD/PURE/R8_SAGA_INDEX.md` — 14 docs TOC, reframing 후 갱신 권고
- `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (PR #374) — still valid evidence base
- `HEXAD/PURE/R8A2_JOINT_VERDICT_TEMPLATE.md` (PR #375) — R8a'' 결과 fill-in
- `HEXAD/PURE/axis_map_fan_verdict.hexa` (PR #376) — 7-axis polling control-plane (wiring fix 후 재사용)
- `HEXAD/LORA/COST_LEDGER_SESSION3.md` (PR #360) — sunk cost 추정 갱신 권고
