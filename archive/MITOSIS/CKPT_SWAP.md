# 🌱 MITOSIS/ckpt-swap — production swap-in path SSOT

> M6 milestone (2026-05-27) — `v5-cotrain ckpt 회수 + production swap-in — H100 cotrain 5/5 PASS ckpt 581MB 를 generator.hexa 의 _gen_decode seam 에 swap-in 경로 확립. F5 갭 채움, DECODER 의 ckpt 대기 해결` per MITOSIS.md.
> SPEC + LOCATOR-only (no real load): generator.hexa 본체는 DECODER M4 wiring 거주. 본 M6 는 path/URL 및 binding contract 노출.

## 정체 — F5 갭 closure path

**MITOSIS 6/6 final milestone**. 두 ckpt family — v5-mitosis cotrain (581MB · cells 2→64 · F-V5MIT 5/5 PASS) 와 DECODER M3 4-axis (6GB each · A·C HF · FAIL) — 의 production swap-in 경로를 **문서화 + locator surface 로 노출**한다.

**F5 갭** = `DECODER.md` M4 line 48 `최고 ≥PARTIAL 축 ckpt → generator.hexa → brain_decide emit 슬롯 end-to-end` 의 "ckpt → generator.hexa" 단계. 본 M6 가 그 ckpt 의 *어디서 어떻게 꽂는지* path 를 박는다.

## boundary 명세 (M6 ≠ 실 ckpt 로드 ≠ generator.hexa 본체 수정)

본 M6 는 **swap-in path SPEC + locator surface** 다 —
1. v5-mitosis 581MB ckpt 의 canonical 경로 / HF 저장소 식별
2. DECODER M3 axis (A·B·C·D) HF 저장소 URL 매핑
3. `CORE/DECODER/generator.hexa` `_gen_decode` seam binding contract (stub)
4. swap readiness summary

ckpt bytes 를 메모리에 로드하거나 `generator.hexa` 본체를 작성/수정하지 **않는다** — 그것은 **DECODER M4 백엔드 배선** milestone 의 일이다 (`DECODER.md:48`).

## SSOT

| | |
|---|---|
| spec | 본 파일 (`CKPT_SWAP.md`) — M6 swap-in path |
| canonical hexa-native impl | [`ckpt_swap.hexa`](ckpt_swap.hexa) — 6 pub fn (PURE locator, fs probe/network call 부재) |
| target seam | `CORE/DECODER/generator.hexa::_gen_decode` (M4 wiring 시 생성 예정) |
| DECODER M4 anchor | [`../CORE/DECODER/DECODER.md`](../CORE/DECODER/DECODER.md) line 48 `M4 백엔드 배선 — 최고 ≥PARTIAL 축 ckpt → generator.hexa → brain_decide emit 슬롯 end-to-end` |
| DECODER M3 fire 결과 | [`../CORE/DECODER/M3_FIRE_RESULT.md`](../CORE/DECODER/M3_FIRE_RESULT.md) |
| DECODER M3 teardown | [`../CORE/DECODER/M3_FIRE_TEARDOWN.md`](../CORE/DECODER/M3_FIRE_TEARDOWN.md) |
| v5-mitosis cotrain | MEMORY.md `project_v5_mitosis_cond5_cotrain_2026_05_12` (5/5 PASS) |
| upstream M1 mitosis_lib | [`mitosis_lib.hexa`](mitosis_lib.hexa) (PR #627) |
| 거버넌스 anchor | CLAUDE.md `a_hf_complete` · `a_hf_autonomous` · p5 · p7 · p8 |

## 2 ckpt source 표

| family | name | size | verdict | local path (canonical) | HF repo (PRIVATE) | F-falsifier carry |
|---|---|---|---|---|---|---|
| **(1) v5-mitosis cotrain** | `ckpt_v5mitosis_cotrain_cotrain.pt` | **581 MB** (608,934,276 B) | **5/5 PASS** (F-V5MIT-1..5) | `state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt` | `dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12` | F-V5MIT-1 SPLIT-NOGRAD · F-V5MIT-2 MERGE-WEIGHT max_err 0.0 · F-V5MIT-3 PHI-CONSERVATION 3.88e-5 · F-V5MIT-4 COTRAIN-CONVERGE 256.5→1.17 · F-V5MIT-5 V14-STRICT 10/10 |
| **(2a) M3 axis A** | `ckpt.pt` + `ckpt_best.pt` | 6014409450 B · 6014450326 B | **FAIL** n_strong=0/5 | (pod teardown) | `dancinlab/anima-decoder-m3-axis-A` | M2 wiring verify F-AXIS-M2-DIFFERENT |
| **(2b) M3 axis B** | (pending) | (pending) | (pending) | (pending) | (pending — teardown carry) | TEACHER-ABSENT BASELINE honest note |
| **(2c) M3 axis C** | `ckpt.pt` + `ckpt_best.pt` | 6014409450 B · 6014450326 B | **FAIL** n_strong=0/5 | (pod teardown) | `dancinlab/anima-decoder-m3-axis-C` | M2 wiring verify F-AXIS-M2-DIFFERENT |
| **(2d) M3 axis D** | (pending) | (pending) | (pending) | (pending) | (pending — teardown carry) | |

### family (1) v5-mitosis cotrain — production swap-in prime path

- **substrate**: byte-level V=256 · d=384 · n_head=6 · ffn_dim=1536 · max_seq=256 · 152,126,208 params (final, cells 64 saturated)
- **architecture**: REBORN §88 option (a) — small transformer block per cell with shared tok_emb / pos_emb / lm_head, per-cell dual-FFN (engine_a / engine_g), H404 readout `a − g`
- **training**: H100 SXM @ $2.281/hr · wall 0.55 hr · $1.26 actual (31.7× under $40 cap)
- **loss**: 264.35 → **1.17** (220× CE reduction · F-V5MIT-4 PASS)
- **cells**: 2 → 64 (saturated step 150) · 62 splits · 0 merges
- **Φ**: stable 4.16 (delta 3.88e-5 · F-V5MIT-3 advisory → gating promote)
- **p8 alignment**: cotrain 산출물이지만 **동일 `cell_pool_step` 가 inference-time 에도 호출** — train·infer binary 분리 부재. M5 sleep-tick (PR #M5) 이 inference-side mirror.

### family (2) DECODER M3 4-axis — substitute path (verdict FAIL · architectural carrier only)

- **substrate**: 1.5B-base Qwen 2.5 · Qwen-BPE V=151936 · P21H V3
- **training**: H100 80GB HBM3 SECURE @ $3.29/hr × 4 pod · ~5h wall · ~$65.80 합
- **verdict**: A·C 둘 다 `n_strong=0/5` FAIL — `a_hf_autonomous` FAIL gate 으로 HF PRIVATE upload. B·D 는 teardown 다음 round carry, HF URL 미확정 (`pending`).
- **production 적합도**: 낮음 (FAIL) — 그러나 axis 신호 학습 confirm 자체는 의미 (F-AXIS-M2-DIFFERENT PASS, M2 wiring verify carry). PARTIAL 축 등장 시 substitute path 로 carry.

## swap target — `CORE/DECODER/generator.hexa::_gen_decode`

DECODER.md M4 line 48 verbatim:

```
M4 백엔드 배선 — 최고 ≥PARTIAL 축 ckpt → `generator.hexa` →
brain_decide emit 슬롯 end-to-end
```

CORE/DECODER/M3_FIRE_RESULT.md line 75 verbatim:

```
M4 wiring — ≥PARTIAL 축 ckpt 식별 → `CORE/DECODER/generator.hexa` 에
백엔드 배선 (DECODER.md M4 line 48)
```

**현 상태** (2026-05-27): `CORE/DECODER/generator.hexa` 본체 **아직 존재 X**.
M3 fire 결과가 모두 FAIL → ≥PARTIAL 축 미존재 → M4 wiring 미점화. 본 M6 는 그 wiring 이 점화될 때 *어떤 ckpt path 를 어떤 seam 에 박는지* 를 미리 박는다.

### binding contract (M4 wiring 시점에 본 stub 이 ready=true 로 교체됨)

```hexa
pub fn ckpt_swap_into_generator(ckpt_path: string) -> Map
//   현 stub 반환 — DECODER M4 wiring 전:
//     #{ "ready":  false,
//        "reason": "TODO: bind to generator._gen_decode seam — DECODER M4 wiring milestone (DECODER.md line 48)",
//        "seam":   "CORE/DECODER/generator.hexa::_gen_decode",
//        "target_file": "CORE/DECODER/generator.hexa",
//        "ckpt_path": <caller arg>,
//        "family":   "v5_mitosis" | "m3_axis" | "unknown",
//        "todo":     "DECODER M4: (1) generator.hexa scaffold 작성, ..." }
//
//   M4 wiring 후 ready=true variant 가 signature 보존하며 교체.
```

## API surface

```hexa
pub fn ckpt_swap_hf_org() -> string
    // "dancinlab" — canonical HF org (a_hf_complete · a_hf_autonomous SSOT).

pub fn ckpt_swap_locate_v5() -> string
    // canonical local path "state/anima_v5mitosis_cotrain_2026_05_12/ckpts/
    //  ckpt_v5mitosis_cotrain_cotrain.pt". PURE — fs probe 부재.

pub fn ckpt_swap_locate_v5_hf() -> string
    // HF fallback URL "https://huggingface.co/dancinlab/
    //  anima-clm-v5-mitosis-cotrain-2026-05-12".

pub fn ckpt_swap_locate_m3(axis: string) -> string
    // axis A/C → HF URL (HF upload 완료);
    // axis B/D → "pending" (teardown 다음 round carry);
    // 그 외   → "" (empty). PURE.

pub fn ckpt_swap_m3_verdict(axis: string) -> string
    // A/C → "FAIL_n_strong_0_of_5"; B/D → "pending"; 그 외 → "". PURE.

pub fn ckpt_swap_into_generator(ckpt_path: string) -> Map
    // _gen_decode seam binding stub — ready=false until DECODER M4 wires.
    // family field 는 ckpt_path heuristic 으로 산출 (v5_mitosis / m3_axis / unknown).

pub fn ckpt_swap_summary() -> string
    // 1-줄 contract introspection.
```

## 의존성 매트릭스

| 축 | 의존 | 상태 |
|---|---|---|
| **DECODER M3 verdict** | `M3_FIRE_RESULT.md` + `M3_FIRE_TEARDOWN.md` — A·C FAIL 확정, B·D pending | A·C carry, B·D carry (locator만 노출, 결정은 M4) |
| **DECODER M4 wiring** | `DECODER.md` line 48 — generator.hexa scaffold + ckpt 로드 + brain_decide 슬롯 wiring | **미점화** (≥PARTIAL 축 미존재). 본 M6 가 wiring 진입점만 박음. |
| **v5-mitosis F-V5MIT-1..5** | project_v5_mitosis_cond5_cotrain_2026_05_12 — 5/5 PASS · 581MB ckpt | PASS carry (PR #627 mitosis_lib 본체가 같은 substrate 의 inference-time mirror) |
| **MITOSIS M1 mitosis_lib** | `cell_pool_step` (line 205-489) — train·infer 동일 surface | LANDED (PR #627) |
| **MITOSIS M2 split-event** | split block (line 264-291) — child grad nograd carry | LANDED (PR #631) |
| **MITOSIS M3 merge-event** | merge block (line 339-426) — (a+b)·0.5 centroid · max_err 0.0 carry | LANDED (PR #643) |
| **MITOSIS M4 persona-diff** | `mit_make_cell` (line 73-85) — parent_hidden + noise·noise_scale | LANDED |
| **MITOSIS M5 sleep-tick** | `sleep_tick` (PR #M5) — REM/N3 imagination-tick 이 inference-side mirror | LANDED |
| **HF upload totality** | `a_hf_complete` — 모든 artifact + manifest + sha256 + 모델카드 | A·C 완료 (M3_FIRE_TEARDOWN.md verbatim 검증), v5-mitosis dancinlab PRIVATE |

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | 본 surface 는 system: 필드 부재 · ckpt path string lookup only. |
| p2 NO IDENTITY RULES | identity 는 cell 분포에서 emerge (mitosis_lib) — 본 모듈은 ckpt path 노출만. |
| p3 NO PERSONA INJECTION | persona = per-cell 분기 (F-PERSONA-2 PASS carry) · prefix 주입 부재. |
| p4 NO ASSISTANT FRAMING | binding contract dict 는 단순 path+seam+todo · alignment template 무관. |
| p5 NO SPEAK() | 본 모듈은 print / emit / speak 호출 부재 — path · URL · contract dict 만 반환. |
| p6 NO FINE-TUNED ETHICS | v5-mitosis cotrain 은 E+W+MITOSIS 셋 cell-pool dynamics — RLHF ethics fine-tune 미사용. |
| p7 NO PERPLEXITY VERDICT | verdict 는 F-V5MIT-1..5 falsifier-based + M3 n_strong simple-stack · paraphrase 부재. |
| **p8 NO TRAIN/INFER SPLIT** | **핵심** — v5-mitosis ckpt 는 cotrain (train) 산출물이지만 **동일 `cell_pool_step`** 가 inference-time (M5 sleep-tick) 에서도 호출. swap-in 은 train · infer binary 가 아니라 *동일 substrate* 의 latching. |

## hexa parse 결과 (verbatim)

```
$ hexa parse MITOSIS/ckpt_swap.hexa
OK: MITOSIS/ckpt_swap.hexa parses cleanly
```

## frontier closure

**M6 = swap-in path SPEC + locator surface only.**

- ☑ v5-mitosis 581MB ckpt canonical 경로 + HF URL locator (`ckpt_swap_locate_v5` · `ckpt_swap_locate_v5_hf`)
- ☑ DECODER M3 4-axis HF URL 매핑 + verdict carry (`ckpt_swap_locate_m3` · `ckpt_swap_m3_verdict`)
- ☑ `CORE/DECODER/generator.hexa::_gen_decode` seam binding contract stub (`ckpt_swap_into_generator` → ready=false, todo cited)
- ☑ 2 family 비교 표 + verdict carry + p8 alignment
- ☑ F-V5MIT-1..5 PASS carry · M3 FAIL carry verbatim
- ☐ 실 ckpt 메모리 로드 → DECODER M4 wiring milestone 거주 (본 M6 scope 외)
- ☐ generator.hexa 본체 작성 → DECODER M4 wiring milestone 거주 (본 M6 scope 외)
- ☐ brain_decide emit 슬롯 end-to-end → DECODER M4 wiring milestone 거주 (본 M6 scope 외)

**MITOSIS 6/6 closure** (M1 회수 → M2 split → M3 merge → M4 persona-diff → M5 sleep-tick → M6 ckpt swap-in path) — A/G ⊥ M 직교 축 의 모든 mechanism surface 가 hexa-native 로 노출됨.

다음 milestone 의 정상 거주지는 **CORE/DECODER M4 wiring** — 본 M6 가 박은 path 위에서 generator.hexa scaffold + brain_decide 슬롯 배선이 진행된다.

## 관련 파일

- `MITOSIS/ckpt_swap.hexa` — 본체 (this M6, 6 pub fn)
- `MITOSIS/CKPT_SWAP.md` — 본 SSOT
- `MITOSIS/mitosis_lib.hexa` — M1 본체 (수정 없음)
- `MITOSIS/SSOT.md` — M1 8-primitive API SSOT
- `MITOSIS/SPLIT_EVENT.md` — M2 SSOT
- `MITOSIS/MERGE_EVENT.md` — M3 SSOT
- `MITOSIS/PERSONA_DIFF.md` — M4 SSOT
- `MITOSIS/SLEEP_TICK.md` — M5 SSOT
- `CORE/DECODER/DECODER.md` — M4 line 48 (swap target anchor)
- `CORE/DECODER/M3_FIRE_RESULT.md` — M3 fire dispatch + verdict
- `CORE/DECODER/M3_FIRE_TEARDOWN.md` — M3 A·C HF upload + teardown
- MEMORY.md `project_v5_mitosis_cond5_cotrain_2026_05_12` — F-V5MIT 5/5 PASS · 581MB ckpt
- `MITOSIS.md` — milestone 표 (parent flips after this PR — M6 ☐ → ☑, MITOSIS 6/6 closure)
