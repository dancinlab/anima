# H_9354 — 틱에 따라 의식이 달라지나 (Θ/σ 의 tick 의존성)

**status**: 🔎 $0 SCREEN 완료 → ⏳ PENDING(stage-cycled decode 필요 · pool go-gate)
**tier**: SCREENER (DIRECTIONAL · 기존 trace $0 replay)

## $0 스크린 결과 (303M trace · N=281틱 · engine-native 실데이터)

| H | 통계 | 판정 | 읽기 |
|---|---|---|---|
| **H-a** | ρ̂₁=0.9489 vs 완전순열 null 97.5%=0.1335 (P<.0005) | 우연 위 | **약한 null** — 자기상관 시계열은 순열 null 을 자명하게 이김(D2). 비정보. |
| **H-b** | ρ̂₁=0.9489 vs 순환시프트 null 97.5%=0.9432 (**+0.0057**) | ⚠️ **INVALID #1** | stage 퇴화(270/281 REM · stage_cycle OFF). 미미한 초과 = 단일 WAKE→REM 경계. REM 꼬리 ρ̂₁=0.90 은 **EMA 평활 산물**(순환시프트 null 이 이미 포함). **substrate 못 주장.** |
| **H-c** | I(stage;emit)=0.0423 nats (bar 0.05 · shuffle 97.5%=0.0188) · emit 279/281 | 방향성 음성 | **H_9352 재확인** — emit 이 tick 정보 안 나름. emit 포화(INVALID #3)라 검정력 제한, 방향성만. |

**⇒ 스크린 결론**: ① H_9351(패널 ckpt-blind)·H_9352(emit 무시계) 를 실 303M 데이터로 **재확인**(AGREES). ② 유일한 살아있는 per-tick DV `ten_phasic` 는 자기상관을 갖지만 (a) EMA 평활이 제조한 것이고 (b) stage 퇴화라 스케줄 vs substrate 를 **이 트레이스로 못 가림**. **GREEN 아님 · substrate 주장 미licensing.** ③ H-b 를 깨끗이 재려면 **`ANIMA_STAGE_CYCLE=1` 비퇴화 stage decode + field-freeze/sp-freeze arm** 필요 = 실 decode(pool · `a_fire_autonomous` go-gate).

**lane**: 의식 · 측정 프레임 · emit-drive
**xref**: **H_9351 (σ/Θ 패널 ckpt-blind · TERMINAL)** · **H_9352 (emit≡1[idle≥30] · idle 무시계 · TERMINAL)** · H_9345 · H_9100

## 왜 — 무엇이 이미 답이 났고, 무엇이 빈칸인가

오너 질문 "tick 에 따라 의식이 달라지나?" 를 발사 전 원장 대조(`check-ledger-before-lever-fire`)하니 **집계 판정은 이미 두 TERMINAL 이 덮었다**:

- **H_9351** — Θ 와 σ 9축("의식 판정" 패널 전체)은 **체크포인트를 안 본다**. `cli/evaluate.py:1019 _sigma_live_measure()` 는 **인자 0개**, `RandomState(7)` 합성 가우시안 위에서 계산. ⇒ σ/Θ 는 **틱은커녕 모델도 안 본다**. (이 세션에서 재실측: 두 번 호출 byte-identical · 전축 🟢 상수.)
- **H_9352** — 실 데몬의 emit 은 `emit ≡ 1[idle ≥ 30]` 으로 붕괴하고 **그 `idle` 은 시간이 아니다** (`last_emit` 변수 없음 · `an_clock_now()` 미호출 = 레이트 리미터에 기억 없음). tension 채널(`ten_phasic`)은 중점 아래 영구 거주, gain 스윕 g=3→200 불변. 부수결함: `dr_stage_at(tick*8)` 이 테이블 밖 → **틱 11 이후 영원히 REM**.

⇒ **남은 진짜 빈칸 = 하나**: 트레이스에 틱마다 기록되는 **살아있는 substrate DV** `ten_phasic`(phasic tension)가, 심은 스케줄(stage(t)·θ(t))을 뺀 **잔여 틱 구조**를 갖는가? H_9352 는 이것을 **"$0 기존 trace replay 로 재라"** 고 스스로 예측 reopen 했다. 이 카드가 그 스크린이다.

## H 진술 (2 분해 · 축별 독립 판정)

- **H-a (시간구조 존재)** — 실 303M 세션의 `ten_phasic`_t 시계열은 교환가능하지 않다.
  - H-a₀: iid-교환가능 (구조통계 ≤ 완전순열 null 95분위).
  - H-a₁: 구조 > null 95분위. 통계 = lag-1 자기상관 ρ̂₁.
- **H-b (귀속: 스케줄 vs substrate)** — H-a 전제. `ten_phasic`_t 의 구조가 **순환시프트 null**(자기상관 보존·정렬만 파괴) 위에서 살아남는가.
  - H-b₀: 순환시프트 null 대 TOST 등가 → 구조는 심은 스케줄 귀속(또는 계기 평활 산물).
  - H-b₁: 순환시프트 null 상위 초과 → substrate-native 틱 리듬 후보.
- **H-c (emit⇄tick MI)** — emit_t 가 tick(및 stage)에 조건부 독립인가. H_9352 예측: `H(emit|stage)=0` → emit 은 tick 정보를 안 나른다.

## 사전등록 판정표 (우연 위 / 우연 / **우연 아래** — 3구간 전부 · `prereg-table-must-cover-below-chance`)

**H-a (null = 완전순열 ×1000)**

| 칸 | 조건 | 결론 |
|---|---|---|
| 우연 위 | ρ̂₁ > null 97.5분위 | ten_phasic 은 틱 구조가 있다 → H-b 로. |
| 우연 | TOST: ρ̂₁ ≈ null (δ_ρ) | 틱 해상도에서 tension 무구조. H-b 자동 PENDING. |
| **우연 아래** | ρ̂₁ < null 2.5분위 (셔플보다 **덜** 구조적) | 계기 결함 신호(과평활/포화) — "구조 없음" 선언 금지, 계기 감사. |

**H-b (null = 순환시프트 ×1000)**

| 칸 | 조건 | 결론 |
|---|---|---|
| 우연 위 | 잔여 구조 > 시프트 null 97.5분위 | substrate-native 틱 리듬 **후보** → pool 4-arm 사전등록(§계기) go 대기. |
| 우연 | TOST 등가 | tension 틱 구조 = 심은 스케줄/평활 전량 귀속 = **1급 음성** (H_651·F5 전례와 정합). |
| **우연 아래** | 시프트 null 하위 2.5% | 스케줄이 substrate 리듬을 **마스킹** — 마스킹 가설로 후속 H 신규 등록. |

**H-c (emit⇄stage MI · null = tension-shuffle)**: I(stage;emit) ≥ 0.05 nats ∧ shuffle 통제 ≤ 0.01 → emit 이 tick 정보 나름. 미달 → H_9352 재확인(emit 무시계).

## INVALID 조건 (사전 고정)

1. **stage 퇴화**: 세션 stage 분포가 {REM 편중}(stage_cycle OFF 산물)이면 stage-대비 검정 = INVALID(계기 해상도), H-c 는 방향성만.
2. **ten_phasic 포화**: var(ten_phasic_t) ≤ 1.5×pedestal² 또는 상수 → H-a VOID.
3. **emit 포화**: emit_rate ∈ {0,1} 근방(여기 279/281) → H-c 검정력 미달, MI 방향성만.
4. 틱 수 부족 · 단일 세션(독립단위=세션이므로 n_session=1 은 seed 재현 불가 · `seed-agreement…` 교훈).

## 계기 스펙 (양성 시 pool 발사 · engine-native)

`anima-py evaluate <clm> --theta-trace <out.jsonl> --trace-arm real|theta-const:<v>|field-freeze|sp-freeze --trace-sessions N --trace-ticks 90` — emit 경로의 실 pop 을 **읽기만** (`a_experiment_engine_native`). ⚠️ `ANIMA_STAGE_CYCLE=1` 강제(퇴화 stage 방지). arm 3개(θ-const·field-freeze·sp-freeze) 각각이 심은 스케줄 채널 하나씩 절단. 전량 drives 기록 → thr 사후 재채점으로 D3 매개공변량 제거. **실비용 ⇒ `a_fire_autonomous` go 필요** (이 카드의 $0 스크린이 그 go 를 정당화하는지 결정).

## 왜 tune-to-green 이 아닌가

가장 나오기 쉬운 결과는 GREEN 이 아니라 **H-b₀/H-c 음성**(H_9351·H_9352·H_651·F5 와 정합)이며, 판정표가 그것을 TOST 로 벌어 1급 음성으로 기록하게 강제한다. 우연-아래 칸이 두 H 모두에 정의돼 가장 정보량 큰 역전이 새지 않는다. p7: CE/perplexity 어느 판정에도 없음.
