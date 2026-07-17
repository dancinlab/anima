---
id: H_9736
title: LOCKED-WINNER RIDER — unconditional value-reading transfer on the RV winner recipe (fresh seeds)
tier: PROPOSED (R8 · lab full Fable+Sol 독립 수렴 · $0 등록·대기 · DIRECTIONAL design)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9736 (R8·P2) — RV-winner rider (무조건부 값읽기 전이)

**Origin.** `sidecar lab full` 2026-07-17 — Fable(H_9736) + Sol(LOCKED-WINNER RIDER) 독립 수렴.
[[H_9683]] 의 값읽기축 = **순서가 진짜 강제되는 유일 조각**. DESIGN ONLY.

**Claim (one line).** RV lane([[H_9691]])이 seed-robust 값-레시피를 **독립적으로 고정·공표**한 뒤,
그 레시피 위에 어휘 1-DOF(nat5/nonce)만 얹어 **fresh seed {3,17}** 로 재발사하면 arm-S 가 구조적으로
seed-robust 가 되어 [[H_9683]] 원 판정표(무조건부 값읽기)가 개봉된다.

## 왜 순서가 강제되는가 (양 모델 동의)
무조건부 "nat lookup 이 seed-robust 하다"는 arm-S 양성통제가 seed-robust 해야만 판독가능한데,
그건 정확히 RV lane 이 지금 푸는 미해결 문제. RV winner **없이** 이 조각은 어떤 설계로도 못 번다
(조건부는 [[H_9735]] 상한). RV 선발과 어휘검정을 **같은 데이터로 하지 않아** winner's curse +
variant×vocab 원인혼합을 막는다([[seed-agreement-on-pooled-feature-is-not-replication]]).

## 살아있는 협업 형태 (침범 0 · split-fire)
```
in-flight RV-sweep 에 어휘 합류 = 🔴 죽은 형태      winner-후 rider = 🟢 살아있는 형태
 ─────────────────────────────                    ─────────────────────────────
 · 병렬세션 lane 침범                                · 그들 sweep·카드·seed 표면 무접촉
 · 1-DOF 오염(비용 2× · 원인귀속 불능)               · winner 공표를 read-only 로 트리거
 · RV 실패 = recipe? vocab? 귀속 불가                · fresh {3,17}(선발에 안 쓴 seed)로 재발사
```
RV winner 가 {7,11}+confirm{13} 통과해 공표되면 그 레시피 그대로:
```bash
anima-py train --init py303_full.clm --corpus {N,S}_s${S}.txt <locked winner flags> --seed ${S}
anima-py evaluate {N,S}_s${S}.clm --store HELD_balanced.json --store-addr-audit --store-flip --store-shuffle
```

## Frozen falsifier (사전등록 · fresh 양 seed)
- **계기**: arm-S 가 winner 의 `ORACLE ≥ .90 ∧ P1-bal ≥ .75 ∧ flip ≥ .90 ∧ addr-gap ≤ .20` 재현.
- **자연 값전이 🟢**: arm-N 동일 bar, 양 seed.
- **자연 값벽 🧱**: arm-S 통과 중 arm-N `P1-bal ≤ .60`, 양 seed(addr 부검으로 주소벽/값벽 분류).
- RV 전멸 공표 시 → [[H_9735]] 로 후퇴(상호배타 사전등록).

## Controls (≥2)
① winner-on arm-S ② winner flags OFF ③ `--store-shuffle` ④ `--store-flip` ⑤ anagram 포함/제외.

## Cost · kill-list · 병렬세션
지금 **$0 대기**(등록만). winner 후 N/S × 2 seed + OFF 최소 1 = **5 CPT**. Kill-list 저촉 없음
(RV sweep 대리발사 안 함 · winner recipe 를 read-only 소비). 병렬세션 침범 없음(winner 공표 뒤 rider 등록).
