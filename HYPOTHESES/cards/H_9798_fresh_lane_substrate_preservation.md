---
id: H_9798
title: FRESH-LANE SUBSTRATE-PRESERVATION — detached L3-tap store cotrain leaves base LM fluency undisturbed (interference-free)
tier: PROPOSED (DESIGN-ONLY · engine-native instrument NOT yet built · compute-backend gated · NOT a verdict)
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

## Mechanism / Instrument (engine-native · ⚠️ 미구축)
측정량 = base LM CE(다음-바이트, 일반 held-out 코퍼스 — **store 코퍼스 아님**), ckpt별:
| ckpt | 의미 |
|---|---|
| base (pre-store) | 기준선 CE₀ |
| fresh + store cotrain | CE_fresh |
| legacy + store cotrain | CE_legacy |
| **C-noscore** (동일 base·동일 step·store objective OFF) | CE_drift (연속학습만의 표류 통제) |

ΔCE_lane = CE_lane − CE₀ · 보존=ΔCE 작음 · 간섭=ΔCE 큰 양수. **핵심 통제 = C-noscore** (store-cotrain 간섭을 단순 연속학습 표류와 분리).

🔧 **계기 상태 (코드검사 2026-07-20)**: 현 `anima-py evaluate` 에는 임의 held-out 코퍼스의 base-LM CE 를 뽑는 flag 가 **없다**(reach/store 계기만). ⟹ 신규 engine-native flag `anima-py evaluate <clm> --base-ce <general_held.txt>` 필요 — next-byte CE 만 읽어 **admissibility 자명**(주소 텐서·target_slot 무접근). (대안: `anima-py train --steps 0 --measure-only --corpus general_held` 가 val_CE 를 뽑으면 재사용 가능 — 백엔드 세션서 확인.)

## Admissibility
측정량은 base LM 다음-바이트 유창성(=보존/간섭)이지 reach(addr_top1)가 아니다 — **직교축**. 주소 텐서·정답 슬롯·주소 진단 일절 무접근.

## Controls
- **C-noscore**: 동일 base + 동일 step, store objective OFF → 표류 기준(연속학습만의 ΔCE).
- **C-corpus**: 일반 held-out ⟂ store 코퍼스(byte-parity·leak=0).
- byte-parity base ckpt(py303_full 또는 py1b) · ≥2 seed {7,4302}.
- TOST 등가대역 사전등록(fresh vs C-noscore CE비).

## Falsify
ΔCE_base(fresh) 가 C-noscore 와 TOST-등가가 아니거나(=fresh 도 간섭), ΔCE_base(fresh) ≥ ΔCE_base(legacy)(=fresh 보존우위 없음) ⟹ 이중구조 KILL. 값진 음성: "분리=보존"이 reach-분리 lane 에서 성립 안 함.

## 🧱 발사 블로커 (concrete · 이 머신)
- store-cotrain ckpt(fresh/legacy)는 H_9792/1B pod 와 함께 폐기됨 — **재학습 필요**. base ckpt 만 HF 생존(py303_full·py1b `dancinlife/tmp-anima-1b`).
- 이 체크아웃엔 anima-py 미설치·pool 호스트 0·pod 0 ⟹ **실측 발사 = compute 백엔드(pool 또는 pod rent) 필요**. pod rent = fleet-rent=spend = owner go-gate.
- $0 local 진전 가능(백엔드 세션): `--base-ce` flag 구현(engine-native·admissible) + toy byte-parity 검증. 그 뒤 303M(또는 1B) fresh/legacy/noscore × 2seed store cotrain → base-CE eval.

## Next (백엔드 갖춘 세션)
① `--base-ce` flag 구현 + toy PASS($0) → ② 303M base + store cotrain {fresh,legacy,noscore}×{7,4302} → ③ 각 ckpt base-CE eval → ④ ΔCE 판정(TOST). lab-mode ON 이면 계기 설계 발산은 `sidecar lab full`.
