# H_9274 / F2 — 5차 발사 사전등록 (데이터 보기 전 동결)

- **코드 sha256 (run.py, 실행 전 동결):** `3b910ee0e60feb43950b66a78c8beac4d918062411305f577ff882f66f935cba`
- **seed:** main 200–219 · pilot 950–969 — 4차(main 0–19 / pilot 900–919)와 **DISJOINT** (규칙⑨)
- **질문:** 재조합(merge) 대수가 정보를 더하는가 (H_054 · H_203)

## 이번에 고치는 두 결함
1. **sham 4연속 붕괴** — 유닛-상속 신호(스칼라·범주)는 보존적 융합이 반드시 동질화한다(4차 메타진단).
   ⇒ **외생 site-field**: init 시 site별 z_s~N(0,1) 동결(d,f,cap 과 독립·절대 상속/갱신 없음).
   유닛 점수 Z_i = Σ_{s∈i} d_s z_s / L_i 를 **매 이벤트 재계산**(유닛 상태 저장 0) ⇒ L·S 와 동일
   대수 class(질량가중 site 집계)라 융합으로 붕괴하지 않는다. sham = a_comp 와 **동일 극단매칭
   기계**(min-Z × max-Z) — 선택 *형태* 보존 · 신호만 인과무관.
2. **REFUTE_v2 R1/R5(처치–detector 공선성)** — a_comp 는 헤드라인 ATP=Σmin(L,S) 의 순간 argmax
   (4차 실측 95.7%). ⇒ `a_detgrad`(순간 ΔATP argmax) arm 을 통제로 추가 + 판정변수를
   **파티션-불변 물리 DV(supply)** 로 이중화.

## 헤드라인 detector (데이터 보기 전 못박음 · 순서통계량 아님)
- **H-A (장부 DV = warm-mean ATP)**: `a_comp − c2_blind > 1.0 (p<.05)` **AND** `a_comp − a5_sham > 1.0 (p<.05)`
  **AND** 전 sign-축 전 점 부호 양성. (control별 paired-t 각각 · min/max/Δ=exp−max 미사용)
- **H-B (물리 DV = warm-mean supply = Σ(cap−D) · Σcap 고정 ⇒ health 등가)**:
  - `B_POS` = Δ > 1.0 (p<.05) AND 전 축 부호 양성
  - `B_EQUIV` = **TOST(δ=1.0)** 로 vs blind AND vs sham 둘 다 등가 (양쪽 단측 p<.05)
  - 보조: overload(stress>1 비율) TOST δ=0.02 · 악화 시 명시

## 필수 게이트 (hard · 하나라도 FAIL → INVALID)
G1 pump ≤1e-9 · G2 self_remerge=0 · G3 live band(control-only 선등록) · cap 보존 · n_units 고정 ·
V_comp_info(slack_sel_ratio>0.5) · **V_sham_distinct**(zratio_sham−zratio_blind>1.0 AND zratio_sham>1.5
AND seed-paired-t p<1e-3) · V_sham_neutral(|corr(Z,slack)|<0.15) · V_POWER(ATP span>3×MDE, pilot) ·
ORACLE_VALID.
진단 플래그: `V_detector_collinear` = (comp 선택쌍 == detgrad argmax) > 0.90 → H-A 는 항등식으로 해석.

## 판정 분기 (실행 가능한 코드 · 사후 이동 금지)
| 조건 | 판정 |
|---|---|
| hard 게이트 FAIL | **INVALID** |
| H-A ∧ B_POS | **DIRECTIONAL-POSITIVE** — 재조합 대수가 정보를 더한다 (toy 상한) |
| H-A ∧ B_EQUIV | **THEATER** — 이득은 Σmin(L,S) 장부 항등식, 물리엔 0 |
| H-A ∧ 그 외 | **INVALID** (물리 DV 결론불가) |
| ¬H-A ∧ 전 축 음성유의 | **KILL** |
| 그 외 | **THEATER** |

어떤 경우에도 H-B 없이 GREEN 금지. tune-to-green / tune-to-red 둘 다 금지.
