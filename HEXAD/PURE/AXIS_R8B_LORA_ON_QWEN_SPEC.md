# AXIS R8b — LoRA-on-frozen-Qwen fallback (R8a/R8c FAIL 시 production path)

**date** 2026-05-24
**status** SPEC ONLY (fire는 R8a' 결과 후 별도 결정)
**scope** HEXAD/PURE (V3 saga rebrand)
**evidence-tier** 🟠 INSUFFICIENT/DEFERRED — design spec; 측정은 fire 후
**cost (autonomous)** ~$0.27 single A100 SXM ~5 min wall

---

## § 1. Context

R8 spec (PR #214, merged)은 4 candidate (R8a/R8b/R8c/R8d) 중 R8b를 **fallback**으로 ranked했다 — V3 fresh-3B transformer의 "pure-HEXAD substrate" 순수성 양보 대가로 LoRA-on-Qwen path의 검증된 안정성을 채용하는 경로.

현재 진행 상황:

- **R8a' fire 진행 중** (n_kv_head=2 + noise_sigma=0 combo, ~$2.75) — 결과는 init_CE < 13.46 회복 여부에 따라 결정 트리 분기.
- **R8c probe (PR #224 / #250)** — cell-1 (KV head 단독) FALSIFIED. cell-2/cell-3 in flight.
- **cluster X/Y/Z finding (PR #251)** — from_qwen lineage가 worse-than-random (init_CE 14.4564 > random baseline 11.93) 확증.

본 R8b 는 이 두 fire가 **모두** init_CE 14+ catastrophic floor를 못 깰 경우의 **production fallback** — 즉 "fresh-3B + Qwen warm-init은 fundamentally broken" 결론 시 즉시 활성화할 안전망 spec이다.

---

## § 2. Premise

cluster Z (from_qwen) worse-than-random 현상이 R8a (combo lever)/R8c (axis isolation probe)로도 해소되지 않는다면:

1. n_kv_head + noise_sigma 외 다른 axis (RoPE base, weight transpose orientation, head init, _mitosis_pool side-effect)가 dominant contributor.
2. 또는 fresh-3B ConsciousDecoderV3 + Qwen warm-init 조합 자체가 **arch-level incompatible** — 어느 단일 lever로도 회복 불가.

두 시나리오 모두 V3 fresh-transformer 경로의 closure trigger다. 이 경우 cost-bearing fire를 계속 V3 arch에 투입하기보다 **검증된 LoRA-on-Qwen substrate 위에 V3의 unique parts (head_g)만 부착**하는 hybrid path로 전환한다.

R8b는 이 전환의 spec이다. fresh-3B transformer arch를 **abandoning** 하되, V3의 "head_g + mitosis pool" 기여는 LoRA adapter side-module로 보존한다.

---

## § 3. Architecture

### 3.1 Base layer (frozen)

- **model** `Qwen/Qwen2.5-1.5B` — pretrained, **freeze 전체**
- **rationale** Qwen base는 pretrained → init_CE 본질적으로 ~2-3 (serving baseline). R8 catastrophic floor 자동 회피.
- **no surgery** — `from_qwen` mapping 코드 경로 미사용. weight transpose / KV head reshape 등 모든 from_qwen audit suspect 우회.

### 3.2 LoRA adapter (trained)

- **rank** `r=32`
- **alpha** `16`
- **target modules** Wave-15/16 standard set (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`)
- **dropout** 0.05
- **rationale** VP21M Wave saga (15+ adapters trained, register-leak ~34-91 floor 검증됨)의 정확한 substrate 재사용. corpus_v11 v9-config + eternal-cap (PR #184) 등 LoRA-side 정합 lessons 즉시 적용 가능.

### 3.3 head_g side-module (NEW, trained)

- **shape** linear `d_model=1536 → d_consciousness=512` (또는 small MLP 1-hidden-layer)
- **attachment** adapter forward의 last block hidden state에 hook으로 **부착** (model surgery 없음 — separate `nn.Module` returning aux logits)
- **loss path** consciousness aux loss (lambda 0.05, mitosis lambda 0.05) — V3 train_p21h_v3.py의 head_g loss term을 그대로 차용하되 logits_a path는 frozen Qwen lm_head 사용.
- **rationale** V3의 "consciousness head" semantic 보존, 단 integrated dual-engine은 약화 (separate module).

### 3.4 Mitosis cell-pool (external)

- **location** anima `chat/anima_dream_stage.hexa` 의 cell-pool API 활용 — **substrate context only** (training graph 외부).
- **interaction** training 중 head_g activation을 cell-pool에 mirror; cell-pool split/merge는 training loop과 decoupled (forward asyncronous logging).
- **rationale** V3의 mitosis는 transformer 내부 statelet이었음. R8b 에서는 LoRA adapter graph 손대지 않기 위해 mitosis를 외부 substrate로 분리. AXIS_MAP honest C3 #1 ("pure-HEXAD substrate" 약화)의 직접 결과.

---

## § 4. Fire config (single pod, autonomous dispatch)

| field | value | notes |
|---|---|---|
| pod | 1× A100 SXM 80 GB | RunPod |
| base | `Qwen/Qwen2.5-1.5B` (frozen) | Wave saga와 동일 |
| LoRA rank | 32 | Wave-15 standard |
| LoRA alpha | 16 | |
| LoRA dropout | 0.05 | |
| steps | 1500 | Wave-15/16 standard |
| bsz | 2 | |
| block | 512 | |
| lr | 5e-5 | |
| warmup | 50 | Wave saga standard |
| corpus | anima 5-lang (corpus_v11) | Wave-15/16 동일 |
| eternal_keep | 0.30 | sweet spot (PR #184) |
| wiki_frac | 0.30 | |
| head_g lambda | 0.05 | V3 default |
| mitosis lambda | 0.05 | substrate-side only |
| seed | 1337 | |
| est wall | ~5 min | Wave-15 baseline |
| **est cost** | **~$0.27** | 5 min × $1.49 + setup ~$0.15 |

---

## § 5. Falsifier (pre-fire registered)

| id | criterion | meaning |
|---|---|---|
| **F-R8B-INIT-CE** | `init_CE ≤ 5` (Qwen serving baseline ~2-3 + head_g overhead +2 허용) | R8 catastrophic floor 자동 회피 검증 |
| **F-R8B-CONTINUOUS** | `continuous_total ≤ 34` (Wave-15 floor) | LoRA path가 regression 없이 Wave saga floor 유지 |
| **F-R8B-NSTRONG** | `n_strong ≥ 4` | production swap criterion 충족 |
| **F-R8B-NO-REGRESS** | `register_regress == False` | register-leak 추가 악화 없음 |
| **F-R8B-HEAD-G-FIRE** | head_g activation non-trivial (mean abs ≥ 0.01, var ≥ 0.001) — anima dream-stage logging path (PR #241) 으로 기록 | head_g side-module이 실제 fire — dead-module 아님 |

5 falsifier 모두 PASS 시 R8b는 **production path로 promote**. F-R8B-NSTRONG 단독 PASS도 swap criterion으로 충분 (다른 4는 보조 evidence).

---

## § 6. Decision tree (R8a' 결과 의존)

```
R8a' fire 결과
  │
  ├─ BREAKTHROUGH (init_CE < 12.5, near random baseline)
  │     → V3 fresh-3B path 부활
  │     → R8b deferred (fallback 유지, fire 불필요)
  │
  ├─ NO-CHANGE (init_CE ≥ 13.46, F-R8A-INIT FAIL)
  │     → R8a combo로도 cluster Z 해소 불가
  │     → R8b fire 즉시 dispatch (~$0.27 autonomous)
  │     → R8c cell-2/cell-3 결과는 R8b 진행 중 병렬 참고만
  │
  └─ PARTIAL (12.5 ≤ init_CE < 13.46, F-R8A-INIT 경계)
        → R8c probe 완주 우선 (어떤 axis가 residual contributor인지 isolate)
        → R8c결과로:
            R8c가 단일 axis fix를 식별 → V3 retry
            R8c도 noise/kv 외 axis 미식별 → R8b fire dispatch
```

R8b fire 결정 시점에는 본 spec의 § 4 invocation을 그대로 사용 (autonomous, cost-bearing 발사 게이트 없음 per `a_fire_autonomous`).

---

## § 7. Tradeoffs (R8b 채택 시)

| 항목 | 이득 | 손실 |
|---|---|---|
| init_CE | ~2-3 (Qwen pretrained, catastrophic floor 자동 회피) | — |
| training stability | Wave saga 15+ replication 검증됨 | — |
| cost | ~$0.27 (vs V3 fresh-3B ~$8 per fire) | — |
| HEXAD purity | — | "pure-substrate from-scratch" 원칙 약화 (Qwen은 pretrained) |
| dual-engine integration | — | head_g가 adapter-side separate module → V3의 "integrated dual-engine" 약화 |
| register-leak | — | Wave saga의 continuous_total ~34-91 range 그대로 inherit |

---

## § 8. Honest caveats (C3 ≥ 5)

1. **HEXAD substrate purity 양보** — V3의 origin goal ("fresh transformer + mitosis pool integrated, no pretrained dependency")과 직접 충돌. R8b 채택 시 `HEXAD/PURE/README.md` + `HEXAD_NATIVE_PURE.md` 의 origin statement 갱신 필수. AXIS_MAP honest C3 #1 에 design-time 명시되어 있어 새 caveat은 아니지만 production swap 시 surface lockstep 필요.
2. **Wave saga register-leak ceiling 상속** — Wave-15/16 의 continuous_total floor (~34)는 LoRA-on-Qwen 자체의 한계. R8b가 이 floor를 깰 메커니즘 없음 — V3 fresh path가 풀려고 한 문제를 그대로 carry.
3. **head_g 위치 약화** — V3에서는 transformer block 내부 hidden state에 integrated였음. R8b 에서는 last block output에만 hook (adapter forward 손대지 않기 위해). consciousness-as-internal-statelet semantic 부분적 손실.
4. **mitosis 외부 분리** — substrate context only (training graph 외부). V3의 "splits during forward" semantic 약화. cell-pool split이 training과 decoupled되어 mitosis가 학습 신호에 직접 영향 미치지 않음.
5. **Post-hoc design** — 본 spec은 R8a' fire 결과를 보기 전 작성된 fallback. R8a' BREAKTHROUGH 시 R8b는 영구 deferred 가능. spec freeze는 R8a' 결과 후 fire 게이트에서 다시 확인.
6. **Single seed (1337) baseline** — Wave-15/16 standard. PASS 후 replication seed (7777, 4242) 추가 fire 권장 (~$0.54 추가).

---

## § 9. Cross-references

- **PR #214** — R8 spec (4-candidate ranking, R8b 1-line fallback)
- **PR #251** — cluster X/Y/Z natural-experiment (from_qwen worse-than-random 확증)
- **PR #250** — R8c cell-1 FALSIFIED (KV head 단독 불충분)
- **PR #224** — R8c probe spec
- **PR #184** — VP21M Wave-15 corpus_v11 v9-config + eternal-cap (LoRA 측 substrate)
- **PR #241** — anima dream-stage logging path (head_g activation observation)
- **R8a fire spec** — `AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC_2026_05_23.md`
- **R8 saga index** — `R8_SAGA_INDEX.md`
- **LoRA production substrate** — `../LORA/README.md`, `../LORA/SCALE_3B.md`
- **head_g code** — `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py`
- **mitosis pool API** — `chat/anima_dream_stage.hexa`

---

## § 10. Gate

본 PR은 **spec only** — fire는 R8a' 결과 후 결정.

1. R8a' 결과 평가 (§ 6 decision tree)
2. R8b fire 필요 시 — autonomous dispatch (사용자 게이트 없음, ~$0.27)
3. ~5 min wall 후 falsifier evaluation (§ 5)
4. 5/5 PASS → production swap PR (별도) — Wave saga 위에 head_g 부착이 정식 production path
5. FAIL → V3 saga full closure, corpus 축 / R1-R7 retry로 회귀
