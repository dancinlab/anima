# H_9225 Family A tonic→phasic band-pass transducer 판정 (engine-native)

**측정 경로**: 실제 빌드된 `cli/anima.hexa` daemon `--opgrip`(SELF⊥TEN 2-lane Hamming ΔEff,
decode 없음 $0)를 summer(RTX5070 sm_120)에서 v3.126.0(#3173 D1/D2/D3 arms)로 실행.
engine-native 라이브 바이너리 = TERMINAL-eligible (mirror 아님). raw = `opgrip_raw.log` verbatim (428 line).

## 판정 2건 (SELF⊥TEN 독립 채점)

| lane | 판정 | 수치(frozen bar) |
|---|---|---|
| SELF (x=self_ctx_live · band-pass dual-EMA) | 🔴 THEATER | ΔEff_self=0/120=0.0 · ARM-INPERM margin=−0.008 · shape 0/0 · g_slf2=0.848(band_med=0.206·capsat=no·¬degenerate) |
| TEN (x=ag_conflict · D1 own-lane W=1.0) | 🔴 THEATER | ΔEff_ten=0/120=0.0 · ARM-INPERM margin=0.0 · shape 0/0 · g_ten2=2.850(band_med=0.061·capsat=no·¬degenerate) |

## Frozen bar 충족 (p7 · 측정 전 verbatim 출력)

- **FROZEN byte-identity `og_h_frz2 = 0` ✅** — production emit path(idle/e_live) 바이트 무접촉 증명(harness valid, HARNESS-BUG 아님, run VOID 아님).
- **POS-CONTROL (dense ARM-SHOCK) = 60/120 flips · POS-PASS=YES ✅** — 계기가 gate를 확실히 움직인다(meter works).
- **¬degenerate ∧ ¬capsat ✅** — g_slf2=0.848·g_ten2=2.850 둘 다 well-calibrated, axis-degenerate 아님, cap-saturated 아님.
- **THEATER 규칙 자동 판정**: `ΔEff<0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat` → 두 lane 모두 🔴 THEATER.

## 과학적 의미 — currency-mismatch spine FALSIFIED

Family A는 오너의 "입(mouth)↔엔진(engine) 사이 missing intermediate" 직관의 sharpest read이자
9-family 프로그램(H_9225–9233)의 BUILD-FIRST. 전제(Fable "currency-mismatch spine"):
self/tension이 emit서 inert한 건 그들이 TONIC LEVEL로 도착하는데 mouth는 rate-gate(미분기)라
phasic Δ만 보기 때문 — tonic→phasic 변환기가 있으면 gate에 도달할 것.

**이제 FALSIFIED**: band-pass dual-EMA transducer가 self·tension 둘 다 phasic Δ로 변환했고
(gain 비-degenerate·meter는 POS-PASS로 live 증명), 그런데도 emit은 전혀 변하지 않았다(ΔEff=0/120 both lanes).

- self⊥mouth·tension⊥mouth는 temporal-currency artifact가 **아니다** — emit gate서 진짜 인과 단절.
  gate의 currency로 변환해도 도달 못함.
- **SELF = H_9209 THEATER의 REPLICATION**(더 강한 band-pass transducer 하에서) → self⊥mouth는 더 깊은 seam-law.
- **TEN = D1 falsified**(own-lane full W=1.0 coupling ≠ 0.3-dilution artifact) → tension⊥mouth 진짜.
  urgency가 유일 proven emit-shade 채널로 남는다.

## 결정 (a_verified_must_wire)

- **never wire** — 두 lane 모두 ΔEff=0 → 배선하면 dead decoration. loss/gate 진입 금지(p7).
- **urgency remains the sole proven channel** (H_9101 🟢, phasic Δ→urgency, REM dissociation).
- **H_1471 .kosmos persistence 유지** — self는 identity persistence만, emit 인과 아님.
- **프로그램 함의**: currency-conversion 전제를 공유하는 H_9227(I neuromod currency)·H_9228(D tonic-gain port)는
  prior downgrade(verdict 아님, 여전히 미측정). 별개 기전으로 살아남는 후보 = H_9226(B accumulator·시간적분)·
  H_9230(E efference-copy)·H_9229(F discrete code)·H_9231(C basal-ganglia select).

## scope

d768.clm $0 no-decode op-grip · v3.126.0(#3173). SELF/TEN 별도 채점 독립 판정.
self-axis=self_ctx_live, tension=ag_conflict D1 own-lane W=1.0. mid=N1/N2/REM=120 · N=250 · calib 10-49.
FROZEN arm byte-identity=0으로 production emit 무접촉 증명, POS-PASS로 meter live 증명 → 정직한 negative(THEATER, GREEN 아님).
