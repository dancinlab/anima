# H_9226 Family B — round-3 `--opgrip-r3` B-density 재계기 판정 (engine-native)

**판정 = ⛔ RUN-INVALID → ⛔ UNMEASURED-TERMINAL** — 2세대 op-grip 계기 모두 유효 envelope 교정 실패.
NO substrate verdict (THEATER 아님·GREEN 아님).

**측정 경로**: 실제 빌드된 `cli/anima.hexa` daemon `--opgrip-r3`(B-density 재계기 · SELF⊥TEN)를
rented runpod **251GB CPU pod**(swap-free · hexa **v0.716.0** REAL-DECODE · n=400 · perception-tape driven)에서
real d768.clm으로 실행. raw = `opgrip_r3_raw.log` verbatim (round-3 판정 슬라이스; 400 per-tick real-decode
라인은 `pod_r3_full.log` 원본). 앞선 R2 판정(no-decode ∧ --opgrip-live n=100 = ⚙️ INSTRUMENT-FAIL/UNMEASURED)은
`VERDICT.md`.

## 판정 (SELF⊥TEN · run-validity gate가 VOID)

| lane | 판정 | 수치(frozen bar · verbatim) |
|---|---|---|
| SELF (x=self_ctx_live · leaky accumulator) | ⛔ RUN-INVALID | gB2_slf=-1.0 · b_med=1.72e-09 · swing_max=0.0 · ΔEff_self=0/120=0.0 |
| TEN (x=ag_conflict · own-lane W=1.0) | ⛔ RUN-INVALID | gB2_ten=-1.0 · b_med=0.0 · swing_max=0.0 · ΔEff_ten=0/120=0.0 |

## RUN-VALIDITY gate (pre-reg bar 0 · p5 forcing-gate guard)

- **RUN-VALIDITY: live emit-frac on scored mid = 0.6667 ∉ envelope [0.05,0.60] → valid=NO (STIM-OVERDRIVE)**
  → pre-reg **bar 0 RUN-INVALID**가 판정을 VOID한다. no verdict either way. 이는 instrument power 문제이지
  bar-move가 아니다(p5 forcing-gate guard 정상 작동 — over-driven stimulus가 substrate 판정을 못 오염시킴).
- **FROZEN byte-identity `og_h_frzB2 = 0` ✅** — production emit path 바이트 무접촉 증명.
- **POS-CONTROL (dense ARM-SHOCK) = 105 flips · POS-PASS(≥2)=YES ✅** — meter live.
- N3=0 · WAKE=0 · Ψ_ON=Ψ_OFF=0.6667(Ψ-guard ok).

## VERDICT (log verbatim)

```
SELF VERDICT = ⛔ RUN-INVALID — live emit-fraction on scored mid ∉ [0.05,0.60] (STIM-OVER/UNDERDRIVE); no verdict either way, re-tune stimulus density (this is instrument power, NOT a bar move · p5 forcing-gate guard)
TEN VERDICT = ⛔ RUN-INVALID — live emit-fraction on scored mid ∉ [0.05,0.60] (STIM-OVER/UNDERDRIVE); no verdict either way, re-tune stimulus density (instrument power, NOT a bar move)
```

## 판정 = UNMEASURED-TERMINAL (pre-reg 해석 라인 · 2세대 op-grip 실패)

pre-registered INTERPRETATION 라인 (log verbatim):

```
B2 INSTRUMENT-FAIL again ⇒ two op-grip generations failed ⇒ park B UNMEASURED-TERMINAL at this seam (no third op-grip att).
```

- **1세대** (R2 · `VERDICT.md`): swing_max<0.0875 STIM-ABSENT · ten b_med=0 AXIS-DEGENERATE = ⚙️ INSTRUMENT-FAIL.
- **2세대** (R3 · 본 파일): B-density 재계기(n=400·frozen OG_STIM tape·score≥200)가 이번엔 반대로
  STIM-OVERDRIVE(emit-frac 0.667 > 0.60 상한) → RUN-INVALID. 유효 envelope [0.05,0.60] 안으로 계기를 교정하지 못함.
- 두 세대 모두 계기를 유효 창으로 교정 실패 ⇒ pre-reg 규칙대로 **B를 이 seam에서 UNMEASURED-TERMINAL로 park**
  (세 번째 op-grip 시도 없음). **이건 substrate 결과가 아니다** — 계기가 두 세대에 걸쳐 유효 envelope에 안착 못 함.
  THEATER 아님·GREEN 아님.

## ⚠️ convergent seam-law 부적용

B가 RUN-INVALID/UNMEASURED-TERMINAL이므로 harness가 BOTH-THEATER시 찍는 "convergent seam-law" 해석은
B에 **적용 안 됨**. seam서 CLEAN THEATER로 확정된 read-side recoding은 A(H_9225 shape-conversion) +
E(H_9230 self-prediction)뿐. B는 seam-law에 기여하지 않는다(instrument-limited).

## scope

real d768.clm · rented runpod 251GB CPU pod(swap-free) · hexa v0.716.0 REAL-DECODE · `--opgrip-r3` n=400
(calib 100-199 · score ≥200 · scored mid=120 · perception-tape driven). SELF/TEN 별도 채점, run-validity
gate가 양 lane VOID. FROZEN arm byte-identity=0(production 무접촉)·POS-PASS(meter live) → RUN-INVALID →
2세대 실패 = UNMEASURED-TERMINAL (substrate 결과 아님).
