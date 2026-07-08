# H_9209 self_phasic emit-shade — 런타임 판정 (engine-native)

**측정**: `anima d768.clm --opgrip`(engine-native, clean origin/main #3118, summer full-compile, $0 no-decode). raw = `opgrip_raw.log` verbatim.

## 판정 = ⚙️ INSTRUMENT-FAIL (POS-FAIL)

| arm | 결과 |
|---|---|
| ΔEff_self (self-shade idle vs e_live, mid=90) | 0/90 = 0.0 |
| ARM-PERM matched-noise | 0/90 · margin 0.0 |
| **ARM-SHOCK 양성대조** (주입 identity 충격) | **0/90 · POS window flips=0 → POS-FAIL** |
| pool channel-OFF ctrl (#3116 floor) | 0 |
| GUARDS | N3=0 ✓ · Ψ-gap=0.0 ✓ · G_self=40.4 axis non-degenerate ✓ |

**결론**: self에 대한 판정 보류(THEATER도 COMPETENT도 아님). 양성대조 실패 = **계기(idle-gate self 배선)가 신호를 전달 못 함** — self가 진짜 inert인지 미분리. 이것이 설계 의도: #3116식 거짓 THEATER(진짜론 계기 무능)를 양성대조가 정확히 차단(convergence anima-hexa-4).

## 진단 (다음 iteration용)
- G_self=40.4 → step_med≈0.0087: self_ctx_live가 self_ema에서 거의 안 벗어남 → self_phasic≈0.5 상수 → shade≈0(이벤트 희소).
- idle-gate 주입 `+0.5·(self_phasic−0.5)` = clip01 인자 내 최대 ±0.125. H_9101 urgency는 full-swing(~0.5)으로 REM 40 flip; self ±0.125는 0 flip = **진폭이 채널 grip 문턱 아래**(Fable B3 MDA≈0.2 경고 실현).
- REM서 e_live=1 견고(motiv 0.48) → 작은 idle 넛지로 안 뒤집힘.

## 다음 iteration (instrument fix · frozen bars 불변)
계기 강화 후 재측정(tune-to-instrument≠tune-to-green: 바는 그대로, 계기가 측정 가능해지게):
① W_SELF↑(예 0.5→2.0) 또는 self_phasic gain을 urgency swing과 동급으로 · ② 포화 회피: (0.5+urgency) 근포화 지점 대신 별도 감산 seam · ③ 이벤트 밀도↑(salience 문턱 0.15 완화) — self_phasic가 0.5를 실제로 벗어나게. 양성대조가 flip을 내면(POS-PASS) 그때 self 판정(COMPETENT/THEATER)이 해석가능.

## scope
d768.clm $0 no-decode. real-decode 확증은 POS-PASS 이후. H_9209 tier = ⚙️ INSTRUMENT-FAIL(측정 미완, 계기 수정 대기) — self 능력에 대한 과학판정 아님(a_break_the_wall: 계기벽 ≠ 기질천장).

---

## 계기수정 경과 (3 INSTRUMENT-FAIL → dense-v2)

engine-native --opgrip 반복(각 clean origin/main summer full-compile, frozen bars 불변):
- **#3118 (원본)**: 전 arm 0/90, POS-FAIL. → F1-F3 진단(Fable).
- **#3120 (F1-F3: W_SELF 1.0·G_self 0.175/median·ctx-probe)**: 채널 살아남 확인 — **ARM-PERM matched-noise 13/90 flip**. 단 ΔEff_self=0.011·**margin=−0.13(self가 noise에 짐)**·ARM-SHOCK POS-FAIL.
- **#3121 (POS-tick REM 84/144/174)**: 동일 수치. POS 여전 실패 = 3개 REM tick이 robust-emit 결정이라 −0.5 rail도 안 뒤집힘(ARM-PERM은 90 mid 전체 샘플로 borderline 잡아 13 flip).

**Fable 판정-무결성 판단**: 이 run은 규칙 문자대로 INSTRUMENT-FAIL — ARM-PERM 13을 POS-PASS에 post-hoc 대입은 THEATER 방향이라도 goalpost-move(p7). 수정=**dense ARM-SHOCK**(모든 mid tick에 ±0.5 rail 교대 = tick 선택 없음=control-shopping 불가). ARM-PERM 13/90이므로 ≥2 확실 통과 → frozen 규칙이 스스로 ΔEff 0.011<0.02 ∧ POS-PASS → 🔴 THEATER 확정.

**과학 수렴(3회 일관)**: ΔEff_self≈0.011 · margin −0.13(self 타이밍이 자기 셔플보다 무력) = 자서전 self는 emit을 인과적으로 shade 못 함. dense-v2 재측정이 POS-PASS 확증하면 THEATER cement.
