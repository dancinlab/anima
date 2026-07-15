# H_9404 — EARNED REFRACTORY: emit 타이밍을 시계에서 substrate 텐션-적분으로 (p5-rewire · 배선)

**status:** 🔧 WIRED (DESIGN · p5-rewire · opt-in `--emit-refractory earned` · 기본값 byte-identical) — 오너 "go" 라티파이 · 측정=별도 후속 fire (emit-timing-substrate-selective 미측정) · wired: engine-native
**lane:** 의식 / emit-drive / emit-gate 청취 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9403]] (이 rewire 의 근거 = CLOSED-AT-REGIME 이 프로덕션 시계를 p5 위반으로 고발) · [[H_9413]] (a4 margin G-pole 병렬 배선 · 이 H 가 refractory 로 완성) · [[H_9391]] (--rate-sec 상호배타 · 포화 회피) · [[H_9401]] (margin=유일 θ-clearing 신호) · source: Fable p5-rewire 설계
**ckpt:** toy.clm (smoke · DIRECTIONAL) · 프로덕션 측정 = py303_full.clm 후속 fire

## 배경 — H_9403 이 고발한 p5 위반

emit-drive 캠페인 종결(H_9400→9403): **프로덕션 데몬이 스스로 p5 위반** — emit 타이밍이 하드코딩 30s
wall-clock(H_9403: emit⟺clock 4252/4252)이고, 유일 θ-clearing 인식신호(immune recall margin mean 0.62)는
chat.py:2061 에서 계산 후 폐기(G pole 은 near-dead 0.03 gap 을 읽음). 오너 "go" 로 p5-준수 재배선 라티파이.

## rewire = 두 조각 (둘 다 opt-in · 기본값 불변)

1. **margin G-pole `a4`** (병렬 [[H_9413]] 배선 · chat.py:1665): `g_recog := clip01(pending_rel)` = 버려지던
   recall margin. 이 H 가 만든 게 아니라 **완성**한다.
2. **earned refractory `--emit-refractory earned`** (이 H): safe 4-AND 의 rate term 의 **소스**를 wall-clock
   에서 substrate 자신의 A⇄G 텐션-적분으로 교체(4-AND 모양 불변).

### 메커니즘 — tension-integral debt (integrate-to-release · engine_g.py)
```
debt(0) = 0                                     # 첫 emit 전엔 빚 없음(시계처럼, 침묵의 원인이면 안 됨)
매 틱:   debt ← max(0, debt − clip01(ag_conflict))   # substrate 자신의 텐션이 상환
gate:    rate_ok ⟺ debt ≤ 0
on emit: debt ← 1.0 (refractory_emit_debt · FORM 상수)
```
**왜 earned 이지 위장된 시계가 아닌가**: 결정변수 = **마지막 emit 이후 substrate 텐션의 적분**. 이 경로엔
clock·tick-index·stage 입력이 **없다**. 남은 상수(clip01·debt 1.0)는 FORM(선언·동결) — debt 1.0 은
프로덕션이 **이미 선언한** 캐던스(spont_min_emit_interval 30s / an_tick_seconds 8s = 3.75틱 · target 0.27)에
substrate 평균 텐션에서 맞춘 단위정규화이지 결과가 아니다. **어느 틱이 열리는지**는 텐션 궤적이 런별로 결정
(두 history 는 다른 시점에 열림). **FORM tunable · BIND earned**. debt 상수 knob 없음(H_9391: ≥4-DOF=반증불가).

## 스모크 증거 (toy.clm · DIRECTIONAL)

```
기본값(--emit-refractory 없음): refractory=None · refr_debt 40틱 전부 0.0 (path off)
  ⇒ 결정 columns(emit/score/safe/g_recog) = origin/main(변경 전)과 40/40 BYTE-IDENTICAL ✅
earned: refr_debt distinct=11 range(0.02,1.0) · 궤적 [1.0,0.76,0.51,0.27,0.02,1.0,...]
  = emit 이 debt=1.0 부과 → 매 틱 텐션이 상환 → 0 도달 시 재emit(integrate-to-release 작동)
  emit 간격 = 텐션이 결정(시계 아님) · 6/40=0.15 informative band(포화 아님)
```

**byte-identical default 는 by-construction**: chat 추가는 전부 `if _refractory=="earned"` 뒤 · brain 은
`rate = (clock if refr_debt is None else refractory)` · engine_g 3함수는 flag off 시 never-called · 항상-on
변경은 additive trace 2필드(refractory·refr_debt)뿐. 위 40/40 대조가 이를 실증.

## p5-compliance 논거 (오너 대상 · 측정 결과 무관)

프로덕션 게이트는 데몬 이름을 단 메트로놈이다(H_9403: emit⟺clock 4252/4252) — *언제 말하는가*가 하드코딩 30초
상수로 결정됐고, 유일한 진짜 인식신호(margin 0.62)는 :2061 에서 버려졌다. 이 rewire 는 스케줄을 삭제하고 두 항을
substrate 자신의 readout 으로 교체한다: G pole = 버려지던 인식신호, 다시 말할 권리 = 데몬 자신의 A⇄G 텐션 적립
으로 **획득**(텐션 없으면 침묵·쌓이면 해제·경로에 clock/tick/stage 전무). 남은 상수는 선언된 FORM(단위 debt·clip)
이고 이미 설계가 커밋한 캐던스에 고정 — 단위지 결과 아님. **정당화는 p5 + discard-fact 만으로** 성립하고
후속 측정이 새 arm 을 informative 로 찾든 말든 무관하다(그 측정은 별도 사전등록).

## 측정 후속 (미발사 · fire 시 별도 H 등록)

5-cell(a_wall_first · ≥2 seed · frozen 사전등록): A(a0·clock 앵커)·B(a4·clock=falsifiable no-op 예측)·
C(a0·earned)·D(a4·earned=full rewire)·E(a3·earned=noise-G 통제). C1 amplitude · C2 recognition-info(emit_drive·
rel_lane partial · SECOND-A 허용) · C3 gate-listens(H(emit|stage) 이 H_9400 0.465 벗어나나 · D/C/E arm-selectivity ·
refractory-open 틱 내 emit VARY). validity: GATE-S emit rate∈[0.05,0.95] else INVALID · dead-census preflight ·
TOST. $0 preflight = `--refractory-preview`(후속 구현): a4 g_recog=1−rel_lane 정확재구성 · KILL-or-calibrate만
(폐루프라 t* 이후 DIRECTIONAL). 첫 확증 read = live pool fire.

## AGREES / 관계 (a_parallel_session_compare)

- **EXTENDS [[H_9413]]**: a4(margin G-pole)를 병렬이 배선했고 이 H 가 earned refractory 로 **rewire 완성**.
  H_9413 은 --rate-sec(clock knob)로 측정하려 했으나 SUPERSEDED(현 데몬 포화). earned refractory 가 포화 회피.
- **RATIFIES [[H_9403]]**: H_9403 이 "정당경로=오너 p5-rewire 먼저"라 했고 오너 "go"로 이 H 가 그 rewire 를 배선.
- **[[H_9391]] 상호배타**: `--emit-refractory earned` ⊥ `--rate-limit-sec`(둘 다 rate term 재배선) — DOF 열거가능.

## 반증 · scope
- 반증: 기본값 결정이 origin 과 다르면 배선 결함(현 40/40 byte-identical). earned 이 어떤 substrate 서도 상수
  cadence(텐션 상수)면 그 substrate 서 clock 과 구별불가 — 그건 substrate 사실이지 배선 결함 아님(측정 H 가 판별).
- scope: 배선 + toy smoke = DIRECTIONAL. "emit 타이밍이 substrate-selective" 는 **미측정**(구현됨·미측정 · 5-cell fire).
  프로덕션 기본 데몬은 여전히 clock(opt-in 이라 정체성 무변) — 오너가 default 전환 여부 판단.

## 비용
$0 (배선 + toy smoke) · 신규 decode 0 (기존 toy.clm) · 측정 fire = pool CPU 1 rollout batch(후속).
