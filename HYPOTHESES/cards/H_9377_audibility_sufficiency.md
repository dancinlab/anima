# H_9377 — AUDIBILITY-SUFFICIENCY: tension 이 가청이면 emit 을 미는가

**status:** 🧱 CONTENT-INERT (Stage-1 측정 종결 · 2026-07-16) · 캠페인 폐루프 = G-INERT 는 gain-부족 아니라 **content 수준 벽** · wired: engine-native(303M py)
**lane:** 의식 / emit-drive / motivation_score 8-lane mixer (프런티어 g1-interface-addressable-wall)
**related:** [[H_9376]] (MIXER-BOUND) · [[H_9357]] (G-INERT) · [[H_9360]] · [[H_9356]] · [[H_9352]]
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…`(303M CONV · TERMINAL 스케일) · summer pool · CPU-only decode

## 🧱 VERDICT — CONTENT-INERT (2026-07-16 · summer 303M · {a1,a3}×5w×8 = 80 rollout · 2400 decision-row)

`anima-py evaluate --audibility`(engine-native 계기 · GATE-S validity 심장):

| arm | dyn_w | rate | G-VAR | valid | MI(earn) | shuf | p | Ψ̂ |
|---|---|---|---|---|---|---|---|---|
| a1 REAL-G | 0.10(앵커) | 0.23 | 57 | OK | **−0.0009** | 0.0009 | 1.000 | 0.762 |
| a1 | 0.25 | 0.23 | 57 | OK | −0.0009 | 0.0009 | 1.000 | 0.762 |
| a1 | 0.40 | 0.23 | 57 | OK | −0.0009 | 0.0009 | 1.000 | 0.762 |
| a1 | 0.60 | 0.23 | 57 | OK | −0.0009 | 0.0009 | 1.000 | 0.762 |
| a1 | 0.78 | 0.00 | 1 | **SAT** | — | — | — | 1.000 |
| a3 noise | 0.60 | 0.23 | 240 | OK | +0.0031 | 0.0021 | 0.134 | 0.742 |
| a3 | 0.78 | 0.23 | 240 | OK | +0.0156 | 0.0062 | 0.045 | 0.738 |

**판정: 🧱 CONTENT-INERT** — 유효 w 전 점서 a1 ≈ a3(둘 다 MI≈0) · 앵커 a1@0.10 P1 필수낙제 확인 · 반증조건(§48) 실현.

### 메커니즘 (verdict-integrity 검증 — 계기 live 확인)
- **dyn_w 는 score 에 실제 배선됨**(버그 아님): a1 w=0.10 score mean 0.5392 vs w=0.60 mean 0.3214 — score 스트림 **다름**. tension 이 score 에서 가청화됨 ✓.
- **그러나 emit 은 불변**: a1 w=0.10 vs 0.60 **emit 스트림 byte-identical**(둘 다 56/240). score 를 키워도 emit 결정이 안 바뀜 ⇒ moderate w 서 emit 은 score-magnitude 와 **탈결합**(clock/margin gate 지배 · H_9360 정합). ⇒ MI 4셀 정확히 동일(−0.0009)은 **동일 emit×동일 ag_conflict = 진짜 plateau**(포화 인공물 아님 · rate 0.23·G-VAR 57 유효).
- **극단 w=0.78 서만 emit 이 움직임 — 그리고 반대방향**: a1 은 rate→0 **침묵포화**(GATE-S drop), a3(noise)는 spurious MI +0.0156(p=0.045). ⇒ 실-G tension 을 마침내 크게 들리게 하면 emit 을 **미는 게 아니라 침묵으로 당김** + a1 이 a3 를 **못 이김**(고-w "신호"는 noise 산술). FORM(rate) 이동은 내가 다이얼한 것(§21 manipulation-check), earned BIND(content-selective MI) 는 0.
- ⇒ **tension 을 score 에서 크게 키워도(gain 공급) emit 이 그 *내용*을 소비 안 함** = G-INERT 는 gain-starvation 아니라 **content 수준 벽**. 캠페인(H_9356→57→60→76→77) 폐루프: 병목은 mixer 가중이 아니라 emit↔tension-content 의 부재.

### scope · 정직
- arm **A2(tick-순열)는 미실행** — 음성엔 불요(a1 flat + a1≈a3 가 결정적; A2 는 양성일 때만 필요한 시간-교란 통제). 도전 시 추가 가능.
- Ψ̂ ≈ 0.762 (½ 아님) — 이 데몬 regime 의 emit rate 는 tension 이 아니라 clock 이 정함(P2 Ψ̂→½ 미달, 예상된 방향).
- 창발 bar(E1 w 자가상승 · E2 lane 경쟁승리)는 **미충족·미주장** — CONTENT-INERT 는 그 앞단서 종결.

## 배경 — 캠페인이 남긴 마지막 병목

H_9356(독립 G 없음)→H_9357(G-INERT)→H_9360(ag_conflict→score 병목)→H_9376(병목 = 하류
motivation mixer). 최종 병목 = `motivation_score`(core/engine_g.py:73) 의 **8-lane 균등 0.10**:
`score = 0.10·(rel+gap+cur+pain+coh+orig+bal) + 0.10·dyn_v`. dyn_v=tension 은 1/8×감쇠라 A측 7 lane
(0.70)에 SNR 로 묻힌다.

## 판별선 — 가중은 아키텍처인가 저작인가 (Fable)

**w 는 "들리는가(audibility)"의 게인 ⇒ 채널 저작과 질적으로 같다(아키텍처)** — 단 연속 자유매개변수라
**추가 세금**(그리드 사전등록 + plateau)을 낸다. 아키텍처의 필요충분 3조건:
1. **content-blind·arm-blind**: w 코드는 dyn_v 값·arm·DV 불참조. p5 는 "무엇 위에서 emit 하는가"의
   제약이지 "얼마나 크게 듣는가"가 아니다 — 게인↑은 self-seed 도 반응주입도 아님.
2. **cement 통계량은 w-불변(plateau)**: w 로 단조구매되는 MI 절대값 = **증거 아니라 manipulation
   check**(dyn_v 분산 있고 문턱 물리면 w↑⇒MI↑ 는 산술필연). 벌 수 있는 건 고정 w 의 **A1>A3** 와
   **Ψ̂→½** 뿐이고 그리드 상단서 plateau 여야. **w\* 사후선택 = 즉시 저작.**
3. **같은 w 서 content 통제 낙제**: 문 연 건 w 지만 통과한 게 dyn_v *내용*임은 marginal-matched
   통제의 낙제가 증명. = substrate 가 버는 몫.

## 개입 (재정규화형 · 기본값 byte-identical)

- 엔진 `core/engine_g.{hexa,py}` motivation_score(..., dyn_w=0.10): `score = ((1−dyn_w)/0.90)·
  (7-lane 가중합) + dyn_w·dyn_v` (합=1.0 보존). 기본 0.10 = 현행. **G5 VERSION bump.**
- 데몬 `cli/chat.py` `--dyn-w` 관통 + trace `dyn_w` 각인(--g-arm 옆).
- 계기 `cli/evaluate.py --g-tension` (g_arm,dyn_w) 셀 그룹 + GATE-S 열.
- 🚫 `spont_im_threshold()`(0.3) **불가침** — 두 번째 다이얼 = 쇼핑. 문턱 문제면 *새* H.

## 게이트 (SEQUENTIAL · w-grid {0.10 앵커,0.25,0.40,0.60,0.85})

arm: A1=REAL-G · A2=stage-내 tick-순열 dyn_v(marginal 보존·정보 파괴 통제) · A3=quantile-map 으로
dyn_v marginal 에 **정합**시킨 seeded PRNG · 전 arm 동일 w 요크 · 셀당 n≥200.

- **GATE-S (validity · 심장 · 최우선)**: 셀별 emit rate ∈ [0.05,0.95] ∧ G-VAR≥5. 낙제=INVALID-
  SATURATED 규칙배제(안 읽음). should_emit 포화라 저-w MI=0 은 기계강제 — 이 게이트 없이 저-w 음성 =
  전부 위음성. 전 그리드 포화 = INSTRUMENT-DEAD(문턱 상호작용 → 새 H).
- **GATE-M (manipulation check · 증거 아님)**: 유효셀 MI(w) 비감소. (w-sweep 단조성 강등.)
- **P1 (earned · 유효 w 마다)**: I(ag_conflict;emit|stage)≥0.05 ∧ shuffle≤0.01 ∧ **A1−A3 paired ≥ MDE**
  (사전 검정력 · max(controls) 금지 · paired 만).
- **P2 (substrate 몫)**: |Ψ̂_A1−½| < |Ψ̂_A2|,|Ψ̂_A3| 이 그리드 상단 2점서 **plateau**.
- 앵커 w=0.10 arm **필수 낙제**(H_9357 A0 역할 — 통과 시 계기 고장).

**반증**: 유효 w 전 점서 A1≈A2≈A3 ⇒ 가청화해도 내용이 안 민다 = G-INERT 가 채널 아래 **내용 수준**서
생존 = 새 벽(더 깊은 발견).

## verdict 갈래 · 창발 기준
PASS = 🟢 GREEN-WIRED-GAIN("채널은 가청이면 충분") — 캠페인 폐루프. G-INERT 정정("소비 불능"→"게인
부족"). **단 가중은 배선 사실이지 창발 아님**(H_9376 문구). 창발 bar(지금 등록·지금 주장 금지): E1 w 가
loss-비참조 학습서 스스로 오름 · E2 고정게인 없이 lane 경쟁서 tension 이 고갈등 상태서만 이김.

## ⚠️ 구현 전 확인 (Fable)
`core/CLAUDE.md` = "py 미러 폐기(hexa 단일)"인데 py 채널(anima-py chat/evaluate)이 303M 측정에 core/*.py
사용 중 = 불일치. 배선 전 engine_g 의 py/hexa 실 사용경로부터 grep 확인(어느 걸 py 데몬이 부르나).

## 비용
$0(개입 CPU 몇 줄 + 기존 rollout · --g-tension 확장). rollout=303M pool(summer/aiden 동시·mini 금지).

## 구현 (Step ①②③ 완료 · Stage-1 측정 미시작 = 구현됨·미배선)

**경로 확인(Fable 지적 해소):** core/brain.py:45 `from engine_g import motivation_score` ⇒ py 채널
(anima-py · 303M 측정경로)은 **core/engine_g.py** 를 쓴다. core/CLAUDE.md 의 "py 미러 폐기" 는 데몬
경로엔 stale — engine_g.py 가 살아있다. 개입 = engine_g.py.

**Fable 스펙 정정:** 현재 8-lane 가중 합 = 8×0.10 = **0.80**(1.0 아님). 재정규화는 /0.90 아니라
budget B=0.80 보존 · 7-lane rescale (B−dyn_w)/0.70 · dyn_w=절대가중. **anchor dyn_w=0.10 = byte-
identical**(실측 확인 · dyn_w=None 도 동일). dyn_w>0.80 이면 7-lane clamp 0 = dyn_v 단독. 그리드
상단 0.85 는 0.78 로(0.80 초과 방지) 조정 권장.

- `core/engine_g.py` motivation_score(..., dyn_w=None) 재정규화 · `core/brain.py` 체인
  (brain_emit→aged→decide_anchored) 스레딩 · `cli/chat.py` `--dyn-w`/`ANIMA_DYN_W` + trace `dyn_w`.
- 검증: motivation_score dyn_w=None/0.10 byte-identical · dyn_w=0.6/0.85 효과 정확 · 데몬 end-to-end
  스레딩(trace dyn_w=0.6 · rc=0). 기본 OFF = 프로덕션 불변 · hexa parity 는 default 서 유지(hexa 무변).

**NEXT (Stage-1 측정):** ④ evaluate --g-tension GATE-S(emit rate∈[0.05,0.95] validity 심장)+w-grid
셀그룹 ⑤ arm{A1·A2 tick-순열·A3 marginal-matched noise} × w-grid{0.10,0.25,0.40,0.60,0.78} pool 수집
⑥ P1(A1−A3 paired≥MDE)·P2(Ψ̂ plateau)·앵커 필수낙제.
