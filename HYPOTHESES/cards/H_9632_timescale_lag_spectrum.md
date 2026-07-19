# H_9632 — 시간척도·시차 스펙트럼 — Timescale-Lag Spectrum: z 의 느린 동역학 vs per-tick 판독 불일치 (fable R4-5 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록 · H_9628 INSTRUMENT-PASS 후 개봉) — source=fable R4-5
**lane:** mouth/tension — 검정력 확장(|ρ|<0.12 미측정 대역) + 시간구조 교락
**related:** [[H_9576]] · [[H_9628]] · [[H_9629]]

## 한 줄 주장 (반증가능)
z_PC2 는 tension 동역학의 느린 변수라 per-tick ρ 는 노이즈에 씻긴다 — 블록 평균 w∈{1,5,15,50}·시차 L∈{−10..+10} 스펙트럼에서 |ρ| 가 w↑ 에 따라 상승해 **자기상관-보존 null**(블록순열·phase-scramble)을 이기면, 참효과는 존재하되 H_9576 은 틀린 시간척도에서 읽은 것이다.

## 어느 KILL 을 왜 안 밟나
가장 가까운 KILL = H_9576 방향성. H_9576 스스로 "null95 반폭≈0.12 ⇒ 더 작은 참효과는 미측정(음성 아님)"을 명시했다 — 이 안은 바로 그 **미측정 대역**을 여는 검정력 설계이지 동일 검정의 재탕이 아니다. 부수 verdict-integrity: naive tick-permutation 은 자기상관 z 에서 null 폭을 왜곡하므로, H_9576 의 p=0.192 자체의 소급 점검을 겸한다.

## engine-native 계기
`anima-py evaluate <clm> --pc2-direction --block <w> --lag <L> --null {perm|block-perm|phase-scramble}` — 집계·시차·null 종류를 evaluate 플래그로. z 의 자기상관 시간(τ_z)·분산도 함께 출력(z 가 상수면 애초에 실험 불능 — 관측으로 보고).

## 통제군 (≥2 + 양성)
- **양성통제**: dose arm 을 동일 집계로 통과 (블록화가 참효과를 보존하는지 인증).
- null #1: rng-z 동일 집계.
- null #2: phase-scramble z (자기상관 보존).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| 어떤 (w,L) 셀에서 사전등록 부호+ ρ > block-null95 ∧ dose 동일셀 생존 (2 seed) | **PASS** — 참효과 실재·시간척도 특정 → 그 (w,L)로 조향 재설계 |
| 전 셀 null ∧ dose 생존 | **KILL** — 시간척도는 답 아님 · per-tick 부재 증거 강화 |
| 유효 n(=tick/w) 미달 셀 | **VOID** — 그 셀은 판정 불가로 봉인(음성 아님) |
| ρ 유의 음(−) 셀이 dose 양(+) 와 공존 (우연 아래 칸) | **INVALID** — 집계 연산 부호 결함 의심 · 수리 먼저 |
| phase-scramble null ≥2× naive null | **소급-INVALID 신호** — H_9576 p 값 재계산 안건 상정 |

**검정력**: w=15 에서 반폭 0.12 유지에 emit tick ≈ 4000 필요(원 270 의 ~15배) — 장기 run 분할 필수.

## 비용 / 죽는 방식
pool CPU **heavy** (7안 중 조향-계열 최고가 — H_9629 census 가 먼저 싸게 τ_z 를 재므로 그 결과로 w 격자 축소 가능). **죽는 방식**: 전 시간척도 null 이면 "느린 변수" 가설 사망 — 효과 부재(또는 z 사망) 쪽 삼각측량 완성.

## 상태
🔵 PROPOSED — 개봉 조건 = H_9628 INSTRUMENT-PASS · H_9629 의 τ_z 로 격자 사전 축소. 측정 주장 0(설계).
