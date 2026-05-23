---
slug: asymmetric-division-primitive
target: anima/tool/hexa_native/mitosis_hook_lib.hexa
kind: substrate-primitive-design
since: 2026-05-23
source_hypothesis: H_201 (HEXAD/LIFE/H_201_asymmetric_division.md)
status: design-only (no implementation requested in this cycle)
---

# Inbox patch — `split_asymmetric` substrate primitive (design)

## 동기

H_201 Cycle #1 검증 (5.13× diversity margin, 4/4 stem persistence) 은
asymmetric division 효과를 **harness-imposed post-split mutation** 으로
시연했다. 이는 H_201 Honest Limit L2 의 직접적 표현:

> substrate 에 `split_asymmetric` primitive 부재 → asymmetry 를 외부 harness 의
> post-split `farr_add_gaussian_noise` 호출로 operational 정의. 이는 cell 의 자력
> 기구가 아닌 **harness-imposed 제약** — 진정한 substrate-native 비대칭 (세포 스스로
> 한 자식만 분화 결정) 은 별도 cycle.

substrate-native 비대칭 분열을 제공하려면 `split_cell` 옆에 형제 primitive
`split_asymmetric` 를 둬서, 자식의 분화 강도를 split 시점에 지정할 수 있게
하면 된다.

## 제안 signature

```hexa
// ── Asymmetric split (H_201 sister to split_cell) ────────────────────────────
// 기본 split_cell 과 동일하나, child 의 weight 에 추가 σ=child_delta_sigma
// gaussian noise 를 in-place 가한다 (parent = stem, 변동 없음).
// child_delta_sigma=0.0 이면 split_cell 과 동일 (backward-compat).
fn split_asymmetric(parent_cell, cell_pool, step: int, child_delta_sigma: float) {
    let triple = split_cell(parent_cell, cell_pool, step)
    let new_parent = triple[0]
    let child      = triple[1]
    let new_pool   = triple[2]
    if child_delta_sigma > 0.0 {
        let _ = farr_add_gaussian_noise(child["engine_a_W"], child_delta_sigma)
        let _ = farr_add_gaussian_noise(child["engine_g_W"], child_delta_sigma)
    }
    return [new_parent, child, new_pool]
}
```

`_mit_check_splits` 에는 옵션 `cell_pool["asym_child_sigma"]` (default 0.0,
없으면 void → 0.0 처리) 를 읽어 `split_asymmetric` 으로 dispatch.

## 영향

- backward-compat: `child_delta_sigma=0.0` 이면 기존 `split_cell` 동작.
- pre-register-frozen H_201 의 ASYM arm 을 substrate-native 로 재현 가능 (현재
  harness 의 post-step mutation 루프 제거).
- D4b mitosis wiring 의 `mitosis_forward_tail` 호출자 (anima_chat.hexa 등) 가
  pool 초기화 시 `pool["asym_child_sigma"] = 0.5` 만 설정하면 자동 적용.
- 검증: H_201 의 동일 falsifier set (F-ASYM-1..6) 을 substrate-native 경로로 재실행
  → 동일 verdict 기대 (5.13× margin).

## 기각 트리거 (raw#82)

- `split_asymmetric` 만으로 H_201 의 결과를 재현 못 하면 → harness/substrate 결과가
  근본적으로 다른 동역학 (post-step vs in-split 시점 차이) — 별도 분석.
- 사용자가 명시적으로 "harness 만 유지 / substrate 손대지 마라" 라고 하면 본 patch
  보류 (substrate-native 비대칭이 의식 emergence 에 필수가 아닐 가능성).

## 우선순위

낮음 (design-only). 현재 H_201 PASS 는 harness-only 로 충분. substrate-native 비대칭이
필요한 시나리오는:
  (i)  cell 이 스스로 "내가 stem 인지 분화 자식인지" 를 결정해야 하는 D3 persona
       lane (cell-pool-as-persona 의 cell-level 자기-알기).
  (ii) D4a/D4b mitosis_hook 의 production 사용 (현재 forward 마다 harness mutation
       호출은 overhead).
