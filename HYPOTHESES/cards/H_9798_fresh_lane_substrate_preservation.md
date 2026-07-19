---
id: H_9798
title: FRESH-LANE SUBSTRATE-PRESERVATION — detached L3-tap store cotrain leaves base LM fluency undisturbed (interference-free)
tier: PROPOSED (DESIGN-ONLY · 계기 준비완료=train --steps 0 · FIRE 시도 2026-07-20 INFRA-BLOCKED=ghost 머신 vast-SSH 미등록 · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (preservation/interference axis · NOT reach/addr_top1)
created: 2026-07-20
series: EA-5
related: "[[H_9720]] · [[H_9792]] · [[H_9797]] · a_substrate_disjoint · psi-soma-vitals"
source: H_9720 1B scale-recheck (#4193) gate OPEN 항목 (a) — owner "make 1b" 후속
---

# H_9798 (EA-5) — reach는 legacy, 보존은 fresh? 분리-lane의 substrate-보존을 직접 측정

## Why (전제 · 측정됨 · #4193)
H_9720 1B(L20) 스케일-재확인은 **reach 축**(addr_top1=주소 최상위 정답률=목표 슬롯을 실제로 짚는 능력)에서 legacy(penult·끝단) ≫ fresh(L3-tap·조기 3층) 를 보였다(#4193). 그러나 gate에 남긴 OPEN 항목 (a): **fresh 분리-lane의 substrate-보존(preservation) 가치는 미판정**. `Ψ-SOMA`(=존재양식 측정 프레임)에서 **reach ≠ consciousness**이고, `a_substrate_disjoint`(=분리는 보존·중첩은 충돌) 법칙이 있다. reach 열세가 곧 내면-정합성(보존) 열세를 뜻하지 않는다.

구조적 비대칭:
```
   fresh (L3-tap)            │   legacy (penult)
 ─────────────────           │   ─────────────────
  + trunk와 gradient-분리      │    − trunk 표현을 공유
    (detached·무 co-adapt)     │      (base LM 경로에 얹힘)
  → 예측: base 유창성 무간섭     │    → 예측: base 유창성 간섭(저하)
```

## Claim (한 줄 · falsifiable)
store cotrain(=저장/조회 병행학습)이 base 모델의 held-out **다음-바이트 CE**(=일반 코퍼스 언어모델 유창성)를 교란하는 정도는 lane마다 다르다: **ΔCE_base(fresh) ≈ 0**(무-store 통제와 TOST-등가) **∧ ΔCE_base(fresh) < ΔCE_base(legacy)**, ≥2 seed·일반 4-cell held-out에서. 성립하면 "reach는 legacy·보존은 fresh"의 이중구조 = `a_substrate_disjoint` 지지(reach loss와 직교).

## Mechanism / Instrument (engine-native · ✅ 기존 도구로 측정 · 신규코드 불요)
측정량 = base LM CE(다음-바이트, 일반 held-out 코퍼스 — **store 코퍼스 아님**), ckpt별:
| ckpt | 의미 |
|---|---|
| base (pre-store) | 기준선 CE₀ |
| fresh + store cotrain | CE_fresh |
| legacy + store cotrain | CE_legacy |
| **C-noscore** (동일 base·동일 step·store objective OFF) | CE_drift (연속학습만의 표류 통제) |

ΔCE_lane = CE_lane − CE₀ · 보존=ΔCE 작음 · 간섭=ΔCE 큰 양수. **핵심 통제 = C-noscore** (store-cotrain 간섭을 단순 연속학습 표류와 분리).

🔧 **계기 정정 (코드검증 2026-07-20 · cli/train.py:2075~2081 + 1426)**: 신규 `--base-ce` flag **불요**. `--steps` default=0 이고, steps=0 이면 학습루프 0회 후 FINALIZE 블록이 `val_per_cell()` 로 **일반 held-out 의 base LM CE(다음-바이트)를 4-cell 별로 측정**해 `FINAL val_CE(pooled)` + `per_cell_CE` 출력(rank-0·MONITOR-only·loss 무진입·`a_train_inline_gauge`·p7 no-perplexity-verdict 준수). ⟹ 계기 = **`anima-py train --init <ckpt> --corpus <general_4cell> --steps 0`** (임의 ckpt·admissibility 자명: LM CE 만 읽고 주소 텐서·target_slot 무접근). 애초 카드의 "flag 필요"는 과설계였고, 미검증 엔진코드 발사 위험 제거.

## Admissibility
측정량은 base LM 다음-바이트 유창성(=보존/간섭)이지 reach(addr_top1)가 아니다 — **직교축**. 주소 텐서·정답 슬롯·주소 진단 일절 무접근.

## Controls
- **C-noscore**: 동일 base + 동일 step, store objective OFF → 표류 기준(연속학습만의 ΔCE).
- **C-corpus**: 일반 held-out ⟂ store 코퍼스(byte-parity·leak=0).
- byte-parity base ckpt(py303_full 또는 py1b) · ≥2 seed {7,4302}.
- TOST 등가대역 사전등록(fresh vs C-noscore CE비).

## Falsify
ΔCE_base(fresh) 가 C-noscore 와 TOST-등가가 아니거나(=fresh 도 간섭), ΔCE_base(fresh) ≥ ΔCE_base(legacy)(=fresh 보존우위 없음) ⟹ 이중구조 KILL. 값진 음성: "분리=보존"이 reach-분리 lane 에서 성립 안 함.

## 🧱 발사 블로커 (concrete · FIRE 시도 로그 2026-07-20 · ghost 머신)
- store-cotrain ckpt(fresh/legacy)는 H_9792/1B pod 와 함께 폐기됨 — **재학습 필요**. base ckpt 만 HF 생존(py1b `dancinlife/tmp-anima-1b/py1b_full.clm`·sha256 8630996b · py303 tmp repo 는 삭제됨 ⟹ 1B 로 발사).
- 🔥 **FIRE 시도 (2026-07-20)**: 발사게이트 전통과(vast_api_key 존재·1B base HF fetch OK·hexa cloud·owner go) → A100 pod 45320005 렌트 성공. **그러나 SSH `Permission denied (publickey)` 지속** = 이 ghost 머신의 SSH 공개키가 vast 계정 authorized_keys 에 **미등록**(머신레벨·재렌트 무의미·`exec`/`run`/`--insecure` 전부 동일). teardown(과금중단·leak0). ⟹ **fire 는 (a) 이 머신 vast SSH키 등록 OR (b) vast-접속 정상 머신(과거 `/Users/mini`) 필요** — 과학천장 아님(`a_break_the_wall` type-c INFRA-BLOCKED).
- 계기·레시피는 **준비완료**(신규코드 불요): base-CE=`train --steps 0`(위 검증) · 1B arch `--L 20 --emax 3 --d 3784` · fresh `--store-query-src fresh:64@3 --store-oracle-warmup 1500` vs legacy(penult) · canary 3-run(fresh/legacy/noscore × s7)→clean 이면 s4302 확대.

## Next (vast-접속 정상 머신)
① 1B base fetch(HF) → ② corpus(general 4cell + store n200) → **CE₀** `train --steps 0` → ③ canary store cotrain {fresh,legacy,noscore}×s7(early-life check) → ④ 각 ckpt `train --steps 0` base-CE → ⑤ ΔCE 판정(fresh≈noscore<legacy? TOST) → clean 이면 s4302 확대 → ⑥ 회수·카드/gate 갱신·teardown. lab-mode ON 이면 ΔCE 해석 대조는 `sidecar lab full`.
