# H_9773 — FLIP-COH 갭 = EVEN-성분 지배 (op-gate 편향 ∨ T=1.0 fringe) — 판별 replay + odd-fusion 구조레버 (R7-1 · $0 S1)

**status:** 🔵 PROPOSED (lab full R7 · Fable 5 · H_9744 위임 브리프 · 사전등록)
**lane:** g1-interface-addressable-wall · H_9744 WIRED-STUDY-NEARMISS의 14~17% 미반전 갭
**related:** [[H_9744]] · [[H_9672]] · [[H_9695]] · [[H_9720]] · [[H_9710]] · [[H_9694]]

## ① 한 줄 주장 (반증가능)
H_9744 flip-coh 미달은 (A) F2 seed-space도 (B) λ-부족도 아니고 **lane 출력의 even(v-부호-불변) 성분 지배**다:
`z=gelu([v; g]W_h)`의 g=`h@W_g`(op-gate) 경로가 극성반전에 불변인 **op-조건부 prior**를 나르고, in-vivo 문맥오염으로 |v|(odd margin)가 줄어든 쿼리에서 even이 이긴다 — 위에 **T=1.0 byte-posterior 샘플링 fringe**(`cli/chat.py:1550` · eval은 argmax)가 얹힌다. 두 성분은 pinned-context 2×2 margin replay의 **even/odd 분해**로 쿼리별 판별 가능하다.

## ② 지면(analytic) 배제 — 재생성 금지 목록에 추가
lane_type 3(RV-3 `a−1/n` 중심화)에서 **고정 주소 a에 대해 v_flip ≡ −v_main (항등식)**:
v = Σᵢ(aᵢ−1/n)·val[polᵢ] = s_G·(val_g−val_b), s_G=Σ_{i∈G}(aᵢ−1/n) ⟹ 극성반전은 s_G 부호만 뒤집는다.
∴ **key-collision·n=8 basin·−1/n 항·특정 slot** 은 flip-incoherence의 원인이 될 수 없다(주소가 arm-간 동일한 한). 오너 실측(slot 고른분산)과 AGREES — slot-상관 분석 재생성 금지.
λ: overwrite `out[t]=λ·s`는 argmax 판독하 **완전 불활성**(행 전체 스케일), T=1.0 샘플링하 **역온도**=FORM — 크랭크 금지 확정(불법이자, C1이면 원인도 아님).

## ③ engine-native 계기 (신규 플래그 · S1 · $0)
`anima-py evaluate --store m.json --ctx-replay <gw2 transcript prefix> --margin-dump out.jsonl`
- gw2_11(+seed7) transcript의 각 qpos 직전 prefix를 문맥으로 **고정(pin)**하고 store pols만 do-개입: 2×2 = {main-ctx, flip-ctx}×{main-pols, flip-pols}.
- per-qpos 덤프: a 분포·a_target·argmax_slot·Δ=s[g]−s[b] (λ 포함 λΔ도).
- ctx 고정 분해: **even=(Δ₊+Δ₋)/2 · odd=(Δ₊−Δ₋)/2** — even은 순수 g-경로+v-짝수항.

## ④ 통제 ≥2 + 양성통제
- **양성통제(계기 인증)**: clean-ctx(eval 조건) replay에서 |odd|≫|even| ∧ flip-coh≈1 재현돼야 함. 실패=계기 VOID.
- null-1: shuffle-pols replay — odd 성분 붕괴(주소↔pol 정합 파괴)돼야 함.
- null-2: nostore — Δ 정의역 이탈(passthrough) 확인.

## ⑤ 사전등록 판정표 (bar .90 이동 없음 · 미반전 22/128(s11)·13/128(s7) 대상)
| 관측 (pinned-ctx replay) | 판정 → 후속 |
|---|---|
| 미반전 집합 ≈ {\|even\|>\|odd\|} 일치율 ≥80% ∧ even 부호가 op-조건부 상수(op=0→'g'류) | **C1 확정(even-지배)** → S2 odd-fusion 개봉 |
| 미반전 대부분 odd-지배지만 λ\|Δ\| 작음 ∧ P(미반전)≈σ(−λΔ)로 관측률 재현 | **C2 확정(T=1.0 fringe)** → genuine regime gap 정량화 · 신규 H로 posterior-margin readout 계기정렬 재사전등록(bar .90 유지) |
| main-ctx vs flip-ctx에서 a 자체가 갈림(a_target Δ>0.2) | **C3(문맥발산 주소)** → [[H_9720]] fresh-query lane in-vivo rider 개봉 |
| odd 크고 even 작고 margin 큼(어느 칸도 아님) | **INVALID** — 계기/이해 결함 · 수리 먼저 |
| 우연 아래: clean-ctx까지 flip-coh<0.9 재현 | **INVALID** — eval↔replay 불일치 = 플러밍 결함 |

## ⑥ S2 — odd-fusion 구조레버 (C1 확정 시에만 · tune-to-green 아님 논증)
`--store-fuse odd`: s_odd = ½(s(v,g) − s(−v,g)) 로 overwrite. **등변성 제약**(답은 store 극성에 odd여야 한다 = 배선 주장 그 자체)이지 knob 아님: bar·λ 불변, per-query 결과 보기 전 사전등록, 고정 주소서 flip-coh=1 **산술 보장**.
게이트: ⓐ eval 경로에서 main-bal ≥ H_9672 bar 유지 ∧ flip-coh=1.0 확인 → ⓑ in-vivo 재발사(오너). 리스크 사전등록: v≈0 꼬리에서 readability 하락(answer-byte 이탈) 가능 — readable<128 이면 그 수치로 보고(no-tune).
예측: main-bal **상승**(even-prior가 s11서 gold-b 14개를 틀리게 하던 것 제거 · main-wrong∩미반전 14/21 해소).

## ⑦ H_9695 every-token 무관 판정 (브리프 Q3)
flip-coh 손실은 **발화 성공한 답 위치**의 even/odd 비율 문제 — every-token은 발화 위치만 바꾸고 fusion 구조는 동일. gated-add fuse면 trunk logits가 답 위치에 재진입해 flip-coh **악화** 예상. 이 갭에 발사 금지(reach 축 전용).

## ⑧ 비용
S1 $0(로컬 CPU replay · transcript 보유 · 신규 플래그 1개). S2 코드+eval $0 · in-vivo 재발사만 비용(오너 go).
