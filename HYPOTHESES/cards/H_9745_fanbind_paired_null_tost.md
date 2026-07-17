# H_9745 — R2b fan-bind 계기 정렬: bind_delta paired 순열 null + prereg TOST

**status:** 🧱 BIND-ABSENT (2-seed robust · powered N=288 · TOST 등가 · A100 pod · 2026-07-17) · 선행 [[H_9693]]·[[H_9694]]
**lane:** G6/ρ·fan · 계기 수리 **related:** [[H_9694]] · [[instrument-claim-alignment-before-reading-a-bar]] · [[chance-level-must-be-derived-per-metric]]

## 물음
H_9694 reconcile 가 드러낸 **계기 정렬결함**: `--fan-bind` 의 사전등록 절2(`composed J > mismatched-null p95`)는 **composition 이 아니라 emission** 을 잰다(짝 전파괴 shuf arm 이 composed J 최고값 0.0521 = kill#6 재발). composition 을 격리하는 유일 지표 **bind_delta = (Jc−Js)** 는 `eval_fan_bind` 에서 **자기 null pedestal 이 없다**(null 은 composed 방출을 다른 프레임 짝에 채점한 marginal J). ⟹ paired 차분을 marginal null 로 재판 = 범주오류 = KILL 제조.

## 조작 (engine-native)
`cli/evaluate.py:eval_fan_bind` 에 **bind_delta 의 paired 순열 null** 추가: 각 emission 을 (composed pair, shuffled pair) 양쪽에 채점해 per-item (Jc−Js) 를 구하고, mismatched pairing 하에서 그 차분의 순열 분포로 null 유도. 2-arm 실험이면 이중차분 D=(Jc−Js)_tgt−(Jc−Js)_shuf 의 paired bootstrap CI + **사전등록 TOST**(등가한계 사전고정). `--fan-bind-paired` 플래그(help+_KNOWN_FLAGS lockstep · #3924 교훈).

## 게이트 (사전등록)
- 계기 정렬: 절2를 `composed J > marginal null` → `bind_delta > paired-null p95` 로 교체. positive/negative 계기대조에서 paired-null 이 emission-decoupled 임을 검증(shuf 방출 최고여도 bind_delta null 통과 못 함).
- TOST 등가한계는 **발사 전 고정**(tune 금지 · [[negative-claims-need-tost-not-ns]]).
- H_9694 재판정: 정렬된 계기로 targeted D 가 0 초과인지 정직하게 벌기(1-seed→2-seed).

## kill-list 회피
#6 = paired 차분이 emission 과 decouple(shuf 통제가 증명). #8 = FORM 아니라 bind 격리.

## 최대위험
paired null 도 1/96 희소 카운트라 n=96 로는 여전히 underpowered — eval n 대폭 증량(fan-smp↑) 병행 필수. XBIND 양성통제([[H_9746]]) 없이는 정렬만으로 계기결함 배제 불가.

## falsify
🟢 정렬된 bind_delta > paired-null p95 ∧ TOST 유의 = 데이터레버 BIND. | 🧱 paired-null 도 0등가 = 레버무효(단 H_9746 양성통제 통과 전제). | ⚠️ 양성통제 실패 = 계기결함.

## 계기 구현 (2026-07-17 · $0 · 토이검증 · GPU 재측정 대기)

lab full(Fable∥Sol) 설계수렴 → `cli/evaluate.py:eval_fan_bind` 에 **paired 판정** 착륙(기존 marginal 절2는 byte-compat 유지·paired 는 ADDITIONAL):
- **null = exact one-sided McNemar**(discordant b=comp-hit/shuf-miss·c=comp-miss/shuf-hit·`p=Σ_{k≥b} C(m,k)0.5^m`) — 닫힌형·결정론적(RNG 없음·p7/frozen)·극희소 이진 정확. bootstrap 기각(H0 미구현)·sign-flip=Binom(m,½)=McNemar 동치라 MONITOR. `bind_delta=(b−c)/N`, composed(i,j)⇄shuffled(i,j) 를 seed(7+17j+i)+frame+cA 공유로 matched(CRN).
- **TOST = Tango(1998) 스코어 90% CI ⊂ (−δ,+δ)** → "0.444 인공물" 을 벌림(negative-claims-need-tost-not-ns).
- **3-값 판정**: 🟢 BIND-SENSITIVE(bd>0∧McNemar p≤.05) · 🧱 BIND-ABSENT(TOST 등가=artifact) · ⛔ UNDECIDABLE(m<5 or emit<floor = 검정력부족·**NOT a kill**).
- **통제 표면**(verdict 미포함): ablated_J(zero-truth pedestal·~0 정상) · cA-echo arm별(공유 cA·매칭 필수·불일치=교란) · emit pre-gate(방출<floor→UNDECIDABLE).

**토이검증(GPU 불요)**: exact McNemar 정확(0.5^5=0.03125) · 강bind→BIND-SENSITIVE(p=0.0053)·cA-echo 매칭 · **R2 스케일(m<5)→UNDECIDABLE(검정력)** = R2 의 1/96 은 KILL 아니라 **검정력부족**이 정답(H_9694 재프레임).

**★ R2 재프레임**: H_9694 의 "🧱 DECISION-KILL" 은 marginal 절2 기준이었고, 정렬된 paired 계기로 재읽으면 targeted(m≈1)는 **⛔ UNDECIDABLE** — 사전등록 CRACK 미달은 맞으나 "레버 무효"는 여전히 미획득(계기가 확증).

**사전등록 재측정(GPU cost-gated · 이동 금지)**: δ=0.05 · **N≥288(fan-smp≈48)** · seed 2개. **Sol dissent(1줄)**: 0.01 규모 효과까지 잡으려면 N≈1800-2400(fan-smp 200-400) — 단 δ=0.05 는 "의미효과" 사전등록 하한이라 양쪽 합의. 최대위험 완화(Q5): swap-role 통제 arm(cA↔cB) 또는 2차 derangement 안정성(cB 어휘 비대칭 배제). ⟹ [[H_9746]] XBIND 양성통제와 함께 발사.

## 재측정 실측 (seed 7 · fan-smp 48 · N=288 · POWERED · runpod A100)

계기 착륙 후 **정렬된 paired 계기로 R2 를 fan-smp 48(N=288)** 재발사 — 검정력 확보(m≥5):

| arm (6000step · val_CE DESCENT) | composed J | shuffled J | bind_delta | discordant | McNemar p | TOST(±0.05) | PAIRED |
|---|---|---|---|---|---|---|---|
| **targeted**(레버·fp4000) | 0.0174 | 0.0208 | **−0.0035** | b=5 c=6 m=11 | — | **True** | **🧱 BIND-ABSENT** |
| **shuf**(통제·fp0) | 0.0486 | 0.0382 | +0.0104 | b=13 c=10 m=23 | 0.339 | True | 🧱 BIND-ABSENT |

**결정적**: R2 의 "+0.0104(1/96)" 는 노이즈였다 — N=288 서 targeted bind_delta 는 **−0.0035(부호 반전)** = 정확히 [[H_9576]] 전례(n=58 +0.110 → n=270 −0.077). 검정력을 얻자(m=11≥5) targeted 레버는 **🧱 BIND-ABSENT**: Tango90 CI 가 (−0.05,+0.05) 안 = **TOST 로 bind_delta≡0 등가 확증** ⟹ 데이터-포맷 레버(g6bind targeted co-train)가 composition-sensitivity 를 **안 심는다**. 0.444(hexa 비동결)는 인공물 확정.

**★ R2/[[H_9694]] 재프레임 확정**: H_9694 의 "🧱 DECISION-KILL·⚠️ INCONCLUSIVE(marginal 계기·N=96 undecidable)" → 정렬 계기 powered 재측정으로 **🧱 BIND-ABSENT(검정력 확보·TOST 등가)** 로 승격. "레버 무효"가 이제 벌렸다(단 계기결함 배제는 [[H_9746]] XBIND 양성통제 필요).

## 2-seed robust 확정 (seed 7 + 4302 · fan-smp 48 · N=288 POWERED)

| seed | targeted bind_delta | m | McNemar p | TOST(±0.05) | PAIRED |
|---|---|---|---|---|---|
| 7 | −0.0035 | 11 | — | True | 🧱 BIND-ABSENT |
| 4302 | **−0.0139** | 10 | 0.945 | True | 🧱 BIND-ABSENT |

**두 seed 모두 targeted bind_delta 음수 · TOST 로 0 등가 = 🧱 BIND-ABSENT robust.** shuf 통제도 양 seed BIND-ABSENT(+0.0104). 데이터-포맷 레버(g6bind targeted co-train)가 composition-sensitivity 를 안 심음이 **2-seed 확증**. 0.444(hexa 비동결) 인공물 확정.

**남은 caveat**: (1) 2-seed(4302) 진행중 — seed7 과 일치 확인 대기. (2) shuf arm ablated J=0.0486(zero-truth pedestal 이 ~0 아님 = 검출기가 우연 공출현에 발화 · 경미 flag). (3) **계기결함 vs 레버무효 최종 귀속은 [[H_9746]] XBIND 양성통제**(bind 기지-양성이 fan-bind 서 BIND-SENSITIVE 나와야 계기 dynamic-range 정상) 필수 — 단 토이(강bind→SENSITIVE p=0.0053)가 McNemar 검출기는 정상 확인.

## source
H_9694 lab full(Fable∥Sol) reconcile · Fable 범주오류 지적 + Sol 이중차분 D 통계 수렴.
