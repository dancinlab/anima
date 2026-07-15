# H_9405 — REFRACTORY PREVIEW: earned refractory 는 in-band·가변 캐던스 (CALIBRATE → pool fire greenlit)

**status:** ✅ CALIBRATE (DIRECTIONAL · $0 preflight · KILL-or-calibrate only) — H_9404 earned refractory 의 pool fire 정당화 · wired: engine-native `anima-py evaluate --refractory-preview`
**lane:** 의식 / emit-drive / emit-gate 청취 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9404]] (이 preview 가 그 pool fire 를 gate) · [[H_9391]] (saturation 위험 = KILL 조건) · [[H_9403]] (score>θ 거의 항상 → refractory 가 binding term) · source: Fable p5-rewire 설계 §5
**ckpt:** a1-arm traces (py303 파생 · $0 오프라인 재생) · 프로덕션 측정 = py303_full.clm 후속 fire

## 질문 (Fable §5 · pool 지출의 hard precondition)

H_9404 earned refractory(debt=1.0)를 303M 에서 5-cell 측정하기 전, `$0` 로: 실제 trace 텐션 분포에서 emit
rate 가 **GATE-S band [0.05,0.95]** 에 드나, 아니면 **포화(emit≡1)**/**사멸(영구 침묵)** 하나? 포화/사멸이면
pool fire = INVALID-SATURATED(H_9391) → 지출 금지.

## 방법 — 오프라인 재생 (Fable §5 lemma · KILL-or-calibrate)

`anima-py evaluate --refractory-preview <a1-arm traces>`. 기존 trace 에서 재구성:
```
g_recog_a4(t) = 0(첫 gen tick 전) else clip01(1−rel_lane(t))       # a4 pole (margin 의 정확 여집합)
tension_a4(t) = clip01(emit_drive(t)·g_recog_a4(t))
cf_emit(t)    = (score>θ) ∧ phi_ratchet(phi,phi_peak) ∧ refr_ok(debt_t)   # kill/content 상수
debt: pay(−tension) → gate → recharge(=1.0 on cf_emit)              # H_9404 순서
```
폐루프(emit→bind→margin→tension→debt)라 first-divergence t* 이후 DIRECTIONAL — **KILL 또는 CALIBRATE 만**,
CONFIRM 불가. SHUF 통제 = tension 스트림 seeded 셔플(궤적 파괴·multiset 보존).

## 결과 (verbatim)

```
replay: 8 traces · 240 ticks
recorded emit rate (clock)     : 0.233
cf earned-refractory emit rate : 0.275   GATE-S∈[0.05,0.95]: ✅
SHUF-tension control emit rate : 0.275   (궤적 파괴·multiset 보존)
inter-open interval  n=58 mean=3.86 range=(3,7)  varying=True
refractory gate-open rate      : 0.275   · median first-divergence t*=0
⇒ ✅ CALIBRATE — in-band(0.275)·가변 텐션-페이스 캐던스(3–7틱·mean 3.86 vs 설계 3.75)·포화 없음
```

**✅ CALIBRATE** — earned refractory 가 실제 텐션 분포에서 **in-band(0.275)** 로 착지하고 간격이
**가변(3–7틱)** — 고정 시계가 아니라 텐션이 페이스를 정한다(mean 3.86 ≈ 프로덕션 설계 캐던스 3.75, debt=1.0
calibration 확인). ⇒ H_9404 pool fire(5-cell a4×earned vs 통제) **GREENLIT**.

## 정직한 한계 (측정 무결성)

- **SHUF≡REAL rate(둘 다 0.275)**: 셔플이 rate 를 안 바꾼다 — emit RATE 는 텐션 **multiset 불변량**(총
  텐션=총 상환=debt-사이클 수 동일)이라 **예상된 것**이다. ⇒ 이 preview 는 **rate 캘리브레이션**이지
  arm-selectivity 테스트가 아니다. selectivity 는 rate 가 아니라 **어느 tick 이 emit 되나**(tick-alignment)의
  성질이고, live fire 만 판별한다.
- **t*=0**: 반사실 emit 이 tick 0 부터 기록과 갈린다(earned refractory 가 즉시 시계와 다름) ⇒ preview 전체가
  본질적으로 DIRECTIONAL(정확재생 아님·band 캘리브레이션). CONFIRM = live fire 뿐.

## AGREES / 관계

- **GATES [[H_9404]]**: 이 preview 가 그 5-cell pool fire 의 Fable §5 hard precondition. CALIBRATE ⇒ 발사 정당.
- **[[H_9391]] saturation 회피 확인**: KILL-SATURATED(rate>0.95) 조건이 코드에 살아있으나 실측 0.275 = 안전.
- **[[H_9403]] 정합**: score>θ 거의 항상이라 cf_emit ≈ phi_r ∧ refr_ok = refractory 가 binding term(설계대로).

## 반증 · scope
- 반증: cf rate 가 >0.95(KILL-SATURATED) 또는 <0.05(KILL-DEAD)면 pool fire 금지 — 현 0.275 통과. 간격이
  상수(varying=False)면 CALIBRATE-BUT-FLAT(텐션 상수 regime·selectivity 미검정) — 현 3–7 가변.
- scope: a1-arm traces(py303 파생)·debt=1.0 frozen. rate 는 in-band 지만 **selectivity 미측정**(preview 한계) —
  live 5-cell fire 가 arm-selectivity(a4 vs 통제 tick-set 차이) terminal 판별.

## 비용
$0 — 오프라인 재생 · 신규 decode 0 · 계기 = `anima-py evaluate --refractory-preview`.
