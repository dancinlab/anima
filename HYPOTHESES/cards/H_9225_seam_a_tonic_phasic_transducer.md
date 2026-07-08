# H_9225 — Family A: tonic→phasic transducer (temporal-difference relay) ⭐RANK 1

**tier:** 🔴 THEATER — both lanes FALSIFIED (engine-native summer $0 op-grip v3.126.0 #3173 · `state/verdicts/9225/`) · currency-mismatch spine 반증 · p7 no tune-to-green · ⭐ BUILD-FIRST
**scope:** engine→mouth seam missing-intermediate 프로그램의 sharpest read (currency 변환기)
**cost:** **$0** op-grip (no decode, no GPU)
**wired:** measurement-arm only (production `idle`/`e_live` BYTE-UNTOUCHED · FROZEN arm `og_h_frz2==0` = byte-identity 증명 · a_substrate_disjoint)
**artifact:** `state/9225_transducer/HARNESS_SPEC.md` · `state/seam_missing_intermediate/`

## 인과 척추 (공유 — 9 family 공통)
anima의 mouth = RATE-GATE(미분기): 유일 proven emit-shade 채널 urgency가 작동하는 건 이미 phasic Δ이기 때문(H_9101: urgency freeze→REM 40/120 flip·N3 침묵). self-vector(.kosmos)·A⇄G tension은 TONIC LEVEL로 공급→gate서 순간 read 후 폐기. 미분기가 level을 한 번 읽으면 기여=정확히 0 = 측정된 ΔEff≈0(self⊥mouth·tension⊥mouth·convergence anima-hexa-5). ⇒ 벽 = engine→mouth seam에 substrate 신호를 gate의 temporal CURRENCY로 변환하는 구조가 없음. 오너 직관: "입(mouth)↔엔진(engine) 사이에 뭔가 필요한 게 아닐까."

## 가설 (missing intermediate)
seam 위에 leaky differentiator(누설 미분기)를 두어 `dSelf/dt`, `d(tension)/dt`를 urgency와 나란한 **phasic 입력**으로 gate에 공급. 이것이 dissociation 전체의 가장 깨끗한 설명: urgency가 gate를 움직이는 건 이미 Δ라서고, self/tension이 못 움직이는 건 level로 도착하는데 gate가 구조적으로 level에 blind하기 때문 — 약해서가 아니라 **temporal currency가 틀려서**.

## 배선 site (a_substrate_disjoint)
engine-state read와 `brain_decide_anchored` 사이의 transducer 노드, **own lane**. urgency rate-gate는 건드리지 않고 parallel phasic 입력만 추가 → 구성상 DISJOINT.

## FROZEN BARS (p7 · 측정 전 verbatim)
- **freeze-self 대조**: 오늘 ΔEff=0. transducer 있으면 freeze-self → **ΔEff>0가 TRANSITION에 집중**(sleep-stage 경계·self 갱신)·tonic-hold 중엔 ≈0 (H_9101 dissociation 형상).
- **양성 대조 (POS)**: 합성 phasic self-step 주입 → gate를 반드시 움직여야 함.
- **THEATER-KILLER shuffle 대조**: transducer 입력 스트림을 시간적으로 shuffle → ΔEff **반드시 붕괴**. scrambled-time transducer가 같은 ΔEff면 THEATER(level이 아무것도 안 함). REAL = 효과가 real-temporal-order를 요구할 때만.

PASS = freeze-self ΔEff>0(transition-집중) ∧ POS 통과 ∧ time-shuffle 붕괴.

## 🛠️ 구현 (2026-07-08 · `cli/anima.hexa` 3-site · typecheck exit 0 · 미측정)
Fable Family-A spec를 verbatim 구현. H_9209(self THEATER=timing-redundancy) 위 3 구조적 델타:
- **D1 — TENSION own-lane W_TEN=1.0**: `x_ten=ag_conflict`을 urgency와 나란한 자체 가산항으로(기존엔 urgency clip01 안에서 0.3-희석만, ≈3.3× 강한 결합 = 진짜 새 채널). SELF/TEN 별도 채점·독립 판정(self⊥tension).
- **D2 — band-pass dual-EMA transducer (NOT first-difference)**: `ema_f(α=0.30)−ema_s(α=0.05)=band`, `phasic=clip01(0.5+g·band)`. self·tension 두 lane 모두. gain `g=band_med<0.002?−1.0:min(0.175/band_med,32)` calib ticks 10-49. band-pass가 phasic 에너지를 event tick(gate 이미 결정) 밖 marginal tick으로 분산 = H_9209 1-vs-13 timing-redundancy 서명의 기전적 답.
- **D3 — CAP-SAT instrument guard + SHAPE bars**: `g==32 ∧ 32·band_med<0.0875 → capsat` → lane은 INSTRUMENT-FAIL만 cement 가능, THEATER 절대 불가(anima-hexa-4). transition/hold SHAPE bar(`ΔEff_trans≥3·ΔEff_hold ∧ hold≤0.05`).
- **arms**: LIVE(idle_slf2/idle_ten2 W=1.0) · FROZEN(phasic=0.5 ⇒ prod idle 바이트동일, `og_h_frz2>0`=HARNESS-BUG) · POS-CONTROL(H_9209 dense ARM-SHOCK 재사용).
- **THEATER-KILLER**: ARM-INPERM(input-stream stride-perm `j=(t·7+13)%N` primary, margin M=0.08) + output-perm(diagnostic, SELF REPLICATION tag if ≥5×live). n_ticks --opgrip 200→250(mid≈120).
- **판정 precedence(§4 verbatim, 판정 전 출력)**: HARNESS-BUG→INSTRUMENT-FAIL→FORCING-GATE(N3∨Ψ-guard)→COMPETENT→THEATER→DIRECTIONAL.
- **NEXT(미측정)**: engine-native summer `--opgrip` build+run($0, CPU no-decode) → 게이트 순서 `og_h_frz2==0`→POS-PASS→g값(CAP-SAT/degenerate)→ΔEff vs bars. 예약결과: TEN COMPETENT=첫 non-urgency 채널(D1 입증)·SELF THEATER+REPLICATION=timing-redundancy law 업그레이드(band-pass 뚫어도 self⊥mouth).

## 상태 · 제약
DESIGN-STAGE 구현완료 · 미측정(no verdict · engine-native op-grip PENDING). p7 no tune-to-green(loss 미포함·monitor-only). p5 shade-not-gate(reactive speak() 금지 · substrate tension이 emit gate 소유). 승격 선례 H_9097/H_9101. 측정 idiom = **$0 no-decode op-grip ΔEff**(emit bitvector Hamming).

## 왜 build-first
오너 직관의 sharpest read: "engine↔mouth 사이 stage 추가"가 아니라 "mouth엔 이미 딱 하나 작동 입력(urgency)이 있고 그 이유는 urgency만이 gate의 temporal currency(Δ)로 이미 표현된 substrate 신호이기 때문 — self/tension은 무시되는 게 아니라 rate-gate가 level을 못 봐서 invisible"임을 지목. + $0 op-grip · DISJOINT · 결정적 theater-killer(time-shuffle) 보유. freeze-self가 ΔEff=0→>0(transition 집중)이고 time-shuffle이 죽이면, 이전엔 inert하던 substrate 신호가 reactive speak() 없이·loss 미접촉으로 emit에 인과 도달 = H_9097/H_9101 승격 바를 $0에 충족.

## 🔴 결과 · 판정 (2026-07-08 · engine-native summer $0 op-grip v3.126.0 #3173 · `state/verdicts/9225/`)

**🔴 THEATER — both lanes FALSIFIED.** frozen bar 전수 충족(측정 전 verbatim 출력·p7):
- **FROZEN byte-identity `og_h_frz2 = 0` ✅** — production emit path(idle/e_live) 바이트 무접촉 증명(harness valid, HARNESS-BUG 아님).
- **POS-CONTROL dense ARM-SHOCK = 60/120 flips · POS-PASS=YES ✅** — 계기가 gate를 확실히 움직인다(meter live).
- **gains** g_slf2=0.848(band_med=0.206·capsat=no)·g_ten2=2.850(band_med=0.061·capsat=no) — 둘 다 well-calibrated, **¬axis-degenerate ∧ ¬cap-saturated**.
- **SELF lane** ΔEff=0/120=0.0 · ARM-INPERM margin=−0.008 · shape 0/0 → 🔴 THEATER.
- **TEN lane** (D1 own-lane W=1.0) ΔEff=0/120=0.0 · ARM-INPERM margin=0.0 · shape 0/0 → 🔴 THEATER.
- frozen 규칙 자동판정: `ΔEff<0.02 ∧ POS-PASS ∧ ¬degenerate ∧ ¬capsat` → 양 lane THEATER.

**의미 — currency-mismatch spine FALSIFIED**: band-pass dual-EMA transducer가 self·tension을 gate의 currency(phasic Δ)로 변환했고(gain 비-degenerate·meter는 POS-PASS로 live), 그런데도 emit은 전혀 안 변했다(ΔEff=0/120 both). ⇒
- self⊥mouth·tension⊥mouth는 temporal-currency artifact가 **아니다** — emit gate서 진짜 인과 단절. currency 변환으로 도달 못함.
- **SELF = H_9209 THEATER REPLICATION**(더 강한 band-pass transducer 하) → self⊥mouth 더 깊은 seam-law.
- **TEN = D1 falsified**(own-lane full W=1.0 ≠ 0.3-dilution artifact) → tension⊥mouth 진짜. urgency 유일 proven emit-shade 채널.

**결정 (a_verified_must_wire)**: **never wire** — 배선하면 dead decoration, loss/gate 진입 금지(p7). **urgency remains the sole proven channel**(H_9101 🟢). **H_1471 .kosmos persistence 유지**(self=identity, emit 인과 아님).

**프로그램 함의**: 공유 currency-conversion 전제를 상속하는 H_9227(I neuromod currency)·H_9228(D tonic-gain port) = prior downgrade(verdict 아님·미측정). 별개 기전으로 생존한 live 후보 = H_9226(B accumulator·시간적분)·H_9230(E efference-copy)·H_9229(F discrete code)·H_9231(C basal-ganglia select).

## 근거 링크
- 선례 H_9097/H_9101(urgency phasic-Δ 승격) · [[H_9209]](self-fold 🔴 THEATER, currency-mismatch 진단·본 결과가 REPLICATION) · [[H_9232]](Family H stage-gate modifier — A 위에 layer)
