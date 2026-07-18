# H_9757 — STAGE-DIVERSITY EMIT-ENTROPY — 92.7% 단일-pin 아래서 읽힌 H(emit|stage) 재검 (R6-6 · pool · (d) 정면)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · pool fire · 사전등록 · ⚠️ 발사게이트 = theta lane 비침범 확인)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis 인접 — H_9715 가 연 H_9400 재검 (H_9715 산출문이 지목한 '예측3' 승계: `chat --pc2-zeta --stage-cycle`)
**related:** [[H_9715]] · [[H_9400]] · [[H_9728]] · [[H_9743]]

## ① 한 줄 주장 (반증가능)
H_9400 의 H(emit|stage)=0.465 는 stage=4 가 92.7% 인 regime(H_9715)에서 측정된 값 — **거의-상수 조건변수라 H(emit|stage)≈H(emit)** 이며 stage 의존성에 대해 무정보다. `--stage-cycle` 로 stage 점유를 강제 다변화하면: 조건부 엔트로피가 0 으로 붕괴(emit≈stage 함수 · pin 이 가렸던 것)하거나, H(emit) 와 TOST 등가(진짜 stage-독립)로 갈린다 — 양방향 사전등록, 선호 결과 없음.

## ② 어느 KILL 을 왜 안 밟나 + 병렬 세션 인접성 (폐기조건 명시)
- **인접성**: theta/store/silence/fanbind lane 은 병렬 세션 소유. 이 안은 θ-phase store·silence content·σ-rebase 무접촉 — stage 조건부 emit 엔트로피 1개만 잰다. **폐기조건**: 발사 전 [[H_9728]](Σ-REBASE) TA-arm 목록·H_9743 후속을 재독해 stage 점유 조작 또는 H(emit|stage) 재측정이 그쪽에 있으면 **본 안 즉시 폐기·이관**. 정당성: H_9715(mouth lane 자체 판정)의 산출문이 이 검정을 '남은 유효 검정'으로 지목(evaluate.py:9613).
- p5 — 안 밟음: 조작은 stage(계기 개입)이지 emit 게이트가 아니다. wired Ψ½ 게이트(H_9743) 무변경.
- H_9400 의 다른 두 전제 재검 아님 — H(emit|stage) 한 다리만.
- 집계-단독 판독 — 안 밟음: stage 별 점유·emit 율 전 분포 보고 의무.

## ③ engine-native 계기
`anima-py chat --stage-cycle <period>` (H_9715 산출문 지목 경로 · 미구현부는 chat 플래그로 구현) × **period 2종**
`anima-py evaluate --pc2-direction <traces_dir> --emit-entropy [--min-occ 50] [--debias mm|boot] [--perm N]` (신규) — 점유-보정 debiased H(emit|stage) + 순열 null.

## ④ 통제 ≥2 + 양성통제
- null-1: stage-라벨 순열(H(emit|stage_perm) = 우연 바닥).
- null-2: cycle period 2종 일치 요구(period 인공물 통제).
- **양성통제(추정기 생존)**: H(emit|gate-margin-bin) < H(emit) — wired Ψ½ 게이트의 자기 입력(margin)은 emit 을 반드시 예측해야 함. 실패 = 추정기 사망 VOID.

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| debiased H(emit\|stage) ≤ 순열-null 바닥 + 0.1 bit (period 2종 일치) | **PASS-STAGE-FUNCTION** — emit≈stage 함수(pin 이 가림) · H_9400 해당 다리 재해석 필요 |
| debiased H(emit\|stage) ≈ H(emit) (TOST ±0.05 bit · period 2종 일치) | **PASS-STAGE-FREE** — 진짜 stage-독립 · H_9400 다리 존속(이번엔 유효 측정으로) |
| 중간 대역 ∨ period 2종 불일치 | **VOID-AMBIG/ARTIFACT** — 검정력 재설계 / period 인공물 |
| debiased H(emit\|stage) > H(emit) + CI (우연 아래 칸 · 진엔트로피론 불가능) | **INVALID** — 추정기 역전(디바이어스 결함) |
| margin 양성통제 실패 ∨ stage 별 min-occ<50 미달 | **VOID** |

검정력: 5-stage × min-occ 50 ⟹ **n≈600 tick** fire(emit·silence 겸비 창 포함). DV 식별가능성: 플러그인 엔트로피는 소표본 편향 ⟹ Miller-Madow/bootstrap 디바이어스 사전등록 · min-occ 하드게이트 · 분모-프리.

## ⑥ 비용
**pool fire**(라이브 cycling 필요 — 기존 트레이스는 92.7% pin 이라 원리적 사용 불가 · 그게 H_9715 의 발견) · summer 단독 점유.

## ⑦ 죽는 방식
① 발사 전: theta lane 카드 재독서 겹침 발견 → 폐기·이관. ② 발사 후: period 2종이 서로 다른 답 → period 인공물 · stage-cycle 계기 자체가 regime 을 오염(그 자체가 'stage 는 조작 불가능한 종속 축'이라는 발견으로 보고).
