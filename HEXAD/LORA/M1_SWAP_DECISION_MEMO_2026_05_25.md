# M1 production swap — 사용자 의사결정 memo (v11 vs v13)

> 2026-05-25 KST · session-3 cycle. LORA.md **M1** ("VP21M production swap
> criteria 5/5 PASS — v11 또는 v13 결정, eternal threshold 재정의 가능") 가
> 현재 **사용자 게이트** 로 block. 이 memo 는 swap 실행이 아니라 **사용자가
> go/no-go 를 결정할 수 있게** 옵션을 표로 정리한다. 실제 adapter 파일 교체는
> 본 memo 가 하지 않는다 (사용자 최종 결정).
>
> 선행 문서:
> - 측정 SSOT — `HEXAD/LORA/WAVE17_VERDICT_2026_05_24.md`
> - criteria 재정의 spec (Pareto / relaxed / weighted) — `HEXAD/LORA/SWAP_CRITERIA_REDEFINE_2026_05_24.md`
> - 도구 — `HEXAD/LORA/swap_criteria_check.hexa`
>
> 본 memo 의 scope = **production 후보 pick 결정** (위 두 문서는 criteria 자체
> 의 재정의를 다룸; 본 memo 는 그 위에서 "그래서 어느 adapter 를 올리나" 를 결정).

## 0. 한 줄 요약

단일 변종 5/5 PASS 는 **구조적 불가** (criterion 2 ↔ 4 anti-correlated, 같은
eternal_keep lever 의 양면). 따라서 결정은 "5/5 를 더 sweep 으로 찾기" 가
아니라 "**4/5 두 후보 중 production 가치 기준으로 pick + threshold 정의 갱신**"
이다. **추천 = 옵션 (b) — 4/5 accept + continuous hard-floor → v11 swap**.
근거는 §4 (M2 가 register-leak 30d monitor 이므로 continuous 억제가 production
가치 우선).

## 1. 입력 사실 (Wave-17 측정, 변경 없음)

| candidate | adapter | eternal_keep | n_strong (↑) | continuous_total (↓) | ja n_score | reg max | reg mean | swap |
|---|---|---|---|---|---|---|---|---|
| **A** | v11 | 0.30 | 2 ✗ | **34** ★ | 14 ✓ | 10 | 1.7 | 4/5 |
| **B** | v13 | 0.10 | **5** ★ | 72 ✗ | 16 ✓ | 21 | 3.6 | 4/5 |
| current | v5 | — | n/a | n/a | n/a | n/a | n/a | LIVE |

- criterion 1 (verdict) / 3 (ja≥13) 는 둘 다 PASS. criterion 5 (tag-leak)
  은 두 후보 모두 TBD (측정 follow-up, §6 C3-2).
- **둘의 차이는 criterion 2 vs 4 한 줄에만 있다.** v11 은 continuous 만점·
  n_strong 미달, v13 은 n_strong 만점·continuous 미달.
- anti-correlation 은 5-point sweep (0.00~0.50) 으로 empirically falsified —
  range 안에 두 축 동시 만점 점 없음 (`WAVE17_VERDICT` §New finding).

## 2. 4 옵션 → 결과 (어느 후보 swap) + trade-off

### (a) composite weighted score 최대화

`score = n_strong·w1 − continuous·w2` 최대 후보 pick. w 선택이 승자를 결정.

| w1 | w2 | v11 score | v13 score | 승자 | 비고 |
|---|---|---|---|---|---|
| 1 | 0.05 | 2 − 1.7 = **0.30** | 5 − 3.6 = **1.40** | **v13** | continuous 약하게 penalize |
| 1 | 0.079 | 2 − 2.69 = **−0.69** | 5 − 5.69 = **−0.69** | **tie** | break-even 점 |
| 1 | 0.10 | 2 − 3.4 = **−1.40** | 5 − 7.2 = **−2.20** | **v11** | continuous 강하게 penalize |
| 1 | 0.20 | 2 − 6.8 = **−4.80** | 5 − 14.4 = **−9.40** | **v11** | continuous 매우 강조 |

→ **break-even = w2 ≈ 0.079 (w1=1 기준).** w2 가 그보다 작으면 (n_strong
중시) v13, 크면 (continuous 중시) v11. **trade-off**: 단일 number 로 결정
가능하지만 w 가 곧 lever 변환 hyperparameter — corpus 가 바뀌면 (Wave-18 등)
w 재조정 필요. interpretability 낮음. 게다가 break-even 이 w2≈0.08 로 좁아서
가중치 선택이 결과를 사실상 직접 지정 = "객관적 score" 의 환상.

### (b) 4/5 accept + continuous hard-floor gate  ★추천

criterion 2 (n_strong) 의 hard ≥4 를 **soft (≥3 권고치)** 로 낮추고, 대신
criterion 4 (continuous) 를 **hard-floor gate** 로 둔다. "4/5 충족 + continuous
≤ floor" 면 swap accept.

| continuous floor | v11 (cont=34) | v13 (cont=72) | swap 결과 |
|---|---|---|---|
| ≤ 50 (현행) | PASS | FAIL | **v11 단독** |
| ≤ 70 | PASS | FAIL | **v11 단독** |
| ≤ 80 | PASS | PASS | 둘 다 → 다른 tie-break 필요 |

→ floor ≤ 50 또는 ≤ 70 시 **v11 swap, v13 탈락.** **trade-off**: production
의 핵심 위험(register burst emission)을 hard gate 로 명시 보존하고, n_strong
은 "회복 권고치" 로 둠 → M2 (register-leak 30d monitor) 와 정의가 정합.
단점: cross-lingual 일반화(v13 의 5S)를 production gate 에서 빼는 것 →
다국어 강건이 production 최우선이면 부적합 (§4 에서 이 가정 검토).

### (c) Pareto-frontier + production 우선순위 명시 pick

(n_strong, −continuous) 2-D plane 에서 dominate 되지 않은 변종 = front. 그 중
**production 우선순위를 명시 선언한 뒤** 한 점을 pick.

| Pareto front | 우선순위 선언 | pick |
|---|---|---|
| {v11(2,34), v13(5,72)} | **register-leak 억제 우선** | **v11** |
| {v11(2,34), v13(5,72)} | **다국어 강건 우선** | **v13** |

(v14/v15/v16 은 v11 또는 v13 에 dominate 되어 front 밖 — `SWAP_CRITERIA_REDEFINE` §2.A.)

→ front 가 정확히 두 후보 {v11, v13} 로 좁혀지고, 우선순위 한 줄이 곧 결정.
**trade-off**: anti-correlation 을 가장 정직하게 인정 (동시 만점 강요 안 함) +
corpus 가 바뀌어도 framework 불변(lever 무의존). 단점은 front 가 ≥2 일 때
**자동 결정 불가** → 항상 사용자가 우선순위를 선언해야 함 = automation 후퇴.
즉 (c) 는 "결정 framework", 실제 pick 은 §4 의 우선순위 논증으로 환원된다.

### (d) Wave-18 fine sweep (0.25 / 0.30 / 0.35)

0.30 주변 3-point 으로 (n_strong>2 AND continuous<50) 동시 점 탐색.

| 결과 가설 | 발견 | pick |
|---|---|---|
| 0.30 주변에 동시-만점 점 존재 | 그 점 | **신규 단일 변종 5/5** |
| 0.30 = sharp global min (U 확정) | 없음 | v11/v13 carry → 다시 (a)~(c) |

→ **trade-off**: 성공하면 진짜 5/5 단일 변종을 얻어 게이트 해소. 그러나
anti-correlation 이 sweep range 전체(0.00~0.50, 6점)에서 이미 구조적으로
관측됨 → 0.30 주변 0.05-step 으로 두 축이 동시에 뒤집힐 가능성 **낮음**
(ROI 낮음, ~$1.50, a_fire_autonomous 로 cost 자체는 문제 아니나 기대값 낮음).
이미 `WAVE17` 옵션-1 으로 등록됨 — (d) 는 "다른 옵션 결정 전 보강 측정"
성격이지 독립 결정 path 아님.

## 3. 옵션 종합 비교

| 옵션 | swap 결과 | production quality 보존 | interpretability | lever 무의존 | 게이트 잔존 | ROI |
|---|---|---|---|---|---|---|
| (a) weighted | w 따라 v11/v13 | MID (w 의존) | LOW (w2≈0.08 좁음) | ✗ | w 선택 = 게이트 | — |
| **(b) floor gate ★** | **v11** | **HIGH (burst hard-gate)** | **HIGH (단일 floor)** | △ (corpus 시 floor 재조정) | floor 값 선택 1회 | — |
| (c) Pareto | 우선순위 따라 | HIGH | MID (front pick 추가) | ✓ | 우선순위 선언 매번 | — |
| (d) Wave-18 | 신규 또는 carry | (성공 시) HIGH | — | — | (실패 시) 그대로 | **LOW ~$1.50** |

→ (a)·(c) 는 결국 "어느 축을 더 중시하나" 라는 같은 질문으로 환원되고
(가중치든 우선순위든), (d) 는 그 질문을 미루는 측정이다. **핵심은 §4 의 한
질문**: production 에서 register-leak 억제 vs 다국어 강건, 무엇이 더 가치 큰가.

## 4. 추천 — 옵션 (b), v11 swap

**추천: 옵션 (b) (4/5 accept + continuous hard-floor ≤ 50) → v11 (eternal=0.30)
production swap.**

### 근거 (production 맥락)

1. **M2 milestone 자체가 register-leak monitor.** LORA.md M2 = "mini
   production 배포 + 30-day register-leak monitor (continuous_total ≤ 50 30d
   stable)". 즉 production 의 **다음 측정 목표가 continuous ≤ 50** 이다.
   v11 (cont=34) 은 이 목표를 즉시·여유 있게 만족, v13 (cont=72) 은 첫날부터
   monitor 를 위반한 상태로 시작. **production gate 와 production 목표를
   일치**시키는 선택 = (b) + v11. 옵션 (b) 의 hard-floor 가 정확히 M2 의
   monitor 임계치와 동일 number (≤ 50) 라는 점이 정합성을 보강한다.

2. **register burst 는 사용자 가시 결함, n_strong 은 내부 OOD 지표.** continuous
   /reg burst (v13 reg_max=21) 는 chat.dancinlab.org 대화 prose 에 그대로
   leak 되어 **사용자가 직접 본다** (mini broker 50-window). n_strong 은
   held-out OOD eval 의 5-lang STRONG count — 품질이지만 사용자 직접 노출은
   약함. live production 의 1차 위험은 가시 leak 이다.

3. **다국어 강건은 이미 hot-swap router 가 보강한다.** production 은 단일
   adapter 가 아니라 **default + KOFL(ko) + JAFL(ja) hot-swap router**
   (`anima_participant.py`, README §production). 약한 언어(ko/ja)는 전용
   adapter 가 받친다 → default adapter 의 n_strong 한 점이 다국어 강건의
   유일 lever 가 아니다. 반면 register burst 는 default adapter 가 그대로
   드러낸다 → **router 가 보강 못 하는 축(continuous)을 default 에서 잡는
   것이 합리적.**

4. **honest 반론 — 다국어 강건 우선이면 v13.** 만약 production 가치 우선순위가
   "ja/ko 포함 5-lang 일관 STRONG" 이고 register leak 은 후처리 필터로 흡수
   가능하다고 보면, 옵션 (c) + "다국어 강건 우선" 선언 → **v13** 이 정답이다.
   이 경우 continuous=72 는 M2 monitor 를 재정의(≤ 80 등)해야 하고, 그러면
   monitor 자체가 약화된다. 본 memo 는 §1~3 근거로 **register 억제 우선** 을
   권하지만, 이 우선순위는 사용자 prior 이므로 최종 lever 는 사용자에게 있다.

### 추천 실행 (사용자 승인 시 — 본 memo 는 실행 안 함)

1. swap criteria 정의 갱신: criterion 2 (n_strong) hard ≥4 → soft 권고치(≥3),
   criterion 4 (continuous) 를 hard-floor gate ≤ 50 으로 격상.
2. v11 adapter → mini `~/anima_chat_pack/lora_adapter/` swap, v5 는
   `lora_adapter_v5_bak/` 로 rollback 보존.
3. M2 30-day register-leak monitor 즉시 시작 (v11 cont=34 baseline).
4. criterion 5 (tag-leak) 측정을 swap 전 선결 (`swap_criteria_check.hexa check`).

## 5. 결정 요청 (사용자 게이트)

| 결정 | 선택 시 |
|---|---|
| **(b) + v11 ★추천** | continuous hard-floor gate ≤ 50, v11 swap, M2 monitor 즉시 시작 |
| (c) + v13 | "다국어 강건 우선" 선언, v13 swap, M2 monitor 임계치 재정의(≤80) 동반 |
| (a) weighted | w1/w2 직접 지정 (break-even w2≈0.079) — 권장 안 함 (interpretability 낮음) |
| (d) Wave-18 | 결정 전 0.25/0.30/0.35 보강 측정 (~$1.50, ROI 낮음 — anti-corr 구조적) |
| NO SWAP carry | v5 LIVE 유지, criteria 재정의도 보류 |

## 6. Honest C3 (≥3)

1. **production carry adapter 라벨 불일치.** LORA.md (SSOT, 최신) 는 현
   production = `corpus_v5`, README.md (2026-05-23) 는 `corpus_v4` 로 기재.
   본 memo 는 LORA.md 의 `v5` 를 따름. baseline 라벨 정합은 swap 실행 전
   확인 필요 (rollback dir 이름이 둘 다 가능).

2. **criterion 5 (tag-leak) 두 후보 모두 미측정.** v11/v13 의 4/5 는
   criterion 5 TBD 를 "PASS 가정" 한 잠정치. swap 전 `swap_criteria_check.hexa
   check <dir>/result.json <dir>/vp21m_eval1.json` 로 측정 선결. 만약 한
   후보가 tag-leak FAIL 이면 3/5 로 떨어져 결정이 단순화될 수도 있음.

3. **n_strong 회복이 noise tier 가능.** v13 의 ja 14→16 (+2), n_strong 2→5
   (+3) 는 n=20 분모 std-dev (σ≈1.5) 안에 들 수 있음 (`WAVE17` C3-5).
   "v13 = 5-lang STRONG" 의 강건성은 3-seed 평균으로 재확인 권장 — 만약
   variance 가 크면 v13 의 유일 강점(n_strong 만점)이 약화되어 추천 (b)+v11
   이 더 강해진다.

4. **추천이 production 우선순위 가정에 의존.** §4 의 "register 억제 우선"
   은 (i) M2 가 register monitor, (ii) burst 가 가시 결함, (iii) router 가
   다국어 보강 — 세 사실에 근거하지만, 사용자가 "다국어 강건이 production
   1순위" 라는 다른 prior 를 가지면 결론이 v13 으로 뒤집힌다. 본 memo 는
   prior 를 강제하지 않고 두 분기를 §5 에 모두 노출했다.

5. **anti-correlation 은 0.10~0.50 range 내 실증.** 그 밖(예 eternal>0.50
   또는 다른 lever 와의 교차)에서 동시 만점 점이 있을 가능성은 미배제.
   다만 ROI 가 낮아(d 참조) 본 memo 는 range 내 4/5 pick 을 권한다.
