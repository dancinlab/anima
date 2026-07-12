# H_9285 CEMENT — 결과 · **verdict = EQUIVALENT-CLOSED** (사전등록 TOST 등가성 증명 · lane CLOSED licensed)

**사전등록**: `PREREG.md` — `run_cement.py` sha256 = `03a91579a126dde921bbe8e59305899913da4bac308aa9cf48f5d562ab6d4125`
(실행 호스트에서 재계산한 sha 일치 확인 · `prev_exclude_all.json` = `6336d45a…0bdc`).
**호스트**: pool `aiden` (전용 · load 0.07) · ckpt `~/py303_full.clm` (d3784·E3·K3·L4·V256·T24) ·
**PARITY max|Δ| = 0.0** (프로덕션 `clm._fwd_logits`와 byte-exact ⇒ engine-native) · wall **445s** · 학습 0 · GPU비 0 · 인프라 벽 없음.
**데이터**: fresh-cue **384 items** (verdict 334 ⊥ pilot 50) · **run-1 ∪ run-2 두 seed 모두와 disjoint**
(5-tuple overlap **0** · (A,B)쌍 overlap **0** · **cue 단어 overlap 0**) · 새 seed(scramble 20260714 · arm 3000 · θ probe 21, sns_en 영역).

---

## 1. 한 문장 결론

**capacity setpoint 배분기는 held-out 재조합 마진에 실질적 크기(±0.20 nats)의 방향성 효과가 없음이 사전등록 TOST로 증명됐다**
(EXP−c0 = **+0.072**, 90% CI **[−0.016, +0.160] ⊂ ±0.20**, p_TOST = **.0083**; 셔플 대조도 등가) —
V-gate 5개 전부 통과(채널 가시성 = 처치가 항목당 헤드라인을 **0.765** 흔든다 ≫ 마진 0.20) ⇒
**organelle lane CLOSED = licensed** (검출력 없는 "ns"가 아니라 **등가 증명**).
단, 이는 **"유의 열화(KILL)"가 아니라 "효과 0"의 결착**이다 — 원 KILL(−0.209, p=.033)은 **세 번째 disjoint seed에서도 재현 실패**(이질성 z=2.67, p=.0075).

## 2. 카드 cement 3조건 집행 결과

| 조건 | 집행 | 실측 |
|---|---|---|
| **(a) V-gate를 unsigned/변위 기반으로 사전등록** | signed gate는 zero-mean 채널에서 구조적 통과불가 ⇒ **\|Δ\|/item 축**으로 사전등록 | **전부 PASS** (아래 §4) |
| **(b) blocks/n을 실측 sd 기준 사전산정** | `sd_used = max(실측 prior 1.2192, pilot 상측80% 0.838) = 1.2192` → `N_REQ = 230` · 미달 시 abort 코드 내장 | **n_main = 334 ≥ 230 · powered=True** (MDE_sup = 0.131) |
| **(c) TOST 등가성 (Δ_eq 사전고정)** | **Δ_eq = 0.20 nats** (분쟁 효과 −0.209/+0.129의 크기 · live detector 레벨의 ~31%) | **3 부호반전 축 전부 등가** ⇒ EQUIVALENT_CLOSED |

## 3. arm (헤드라인 `m_B_conj` · item-level · n=334 · paired-CRN)

| arm | mean ± SEM | D-acc |
|---|---|---|
| **c0** (프로덕션 dense) | **+0.311 ± 0.144** | .362 |
| c1_k1 | +0.333 ± 0.149 | .380 |
| c1_k2 | +0.303 ± 0.145 | .365 |
| **EXP** (절대-setpoint schedule) | **+0.383 ± 0.147** | .389 |
| c2_shuf (동일 k 분포 · 시간축 셔플) | +0.295 ± 0.148 | .359 |
| SHOCK (router 파괴) | +0.297 ± 0.143 | .365 |
| SHAM_ident (k=E no-op) | +0.311 ± 0.144 (= c0, 정확히 0 변위) | .362 |

**control별 paired-t (규칙① · max(controls) 미사용 · 전부 보고)**

| 비교 (부호반전 축) | Δ | SEM | t | p |
|---|---|---|---|---|
| **EXP − c0** (setpoint level) | **+0.0723** | 0.0533 | **+1.36** | .175 (ns) |
| **EXP − c1_best** (constant-k level) | = EXP − c0 | — | — | c1_best가 **disjoint pilot에서 c0(dense) 선택** (k=3=dense가 최선 상수 · run-1과 동일 구조사실) |
| **EXP − c2_shuf** (schedule ordering) | **+0.0882** | 0.0585 | **+1.51** | .131 (ns) |
| EXP − pooled-mean(controls) | +0.0776 | 0.0451 | +1.72 | .085 (ns) |
| (부수) D-acc: EXP − c0 | +0.027 | 0.020 | +1.37 | .169 (ns) |

⇒ **PASS 미실현** (EXP가 0/3 control 유의 우세 · t_crit=1.65). 배분기가 reach 레버라는 증거 **없음**.

## 4. V-gate — 헤드라인 detector 그 자체에 · **UNSIGNED** (cement 조건 (a))

| gate | 실측 | 판정 |
|---|---|---|
| **V0** 자원보존(규칙⑧) | max\|Σ_e P[t,e] − 1\| = **2.2e−16** ≤ 1e−13 | ✅ (무에서 자원 창조 0) |
| **V0b** SHAM-IDENT 0-바닥 | k=E no-op의 max\|Δ\| = **0.0** | ✅ (unsigned 통계량이 수치잡음으로 통과 불가) |
| **V1** liveness | c0의 m_B_conj = +0.311, **t=+2.17** (p=.030) | ✅ detector 살아있음 |
| **V2a** 채널가시성 (SHOCK · unsigned) | mean\|Δ\|/item = **0.353**, 95% CI [0.323, 0.384] **> 0.20** | ✅ |
| **V2b** 채널가시성 (EXP · unsigned) | mean\|Δ\|/item = **0.765**, 95% CI [0.699, 0.830] **> 0.20** | ✅ |

> **왜 이게 등가 주장을 licensing하는가**: 처치는 항목당 헤드라인을 **우리가 배제하려는 마진(0.20)보다 3.8배 크게** 흔든다.
> 즉 detector는 처치 채널에 **눈멀지 않았다** — 그 위에서 signed mean이 ±0.20 안이면 그것은 "채널 없음"이 아니라
> **"방향성 효과 없음"**이다. (run-2에서 signed V-gate가 FAIL한 이유가 바로 이 zero-mean·고변위 구조였다.)

## 5. TOST 등가성 (cement 조건 (c) · **Δ_eq = 0.20 데이터 보기 전 고정**)

| 축 | Δ | **90% CI** | p_TOST | 등가? |
|---|---|---|---|---|
| **EXP vs c0** (= c1_best) | +0.0723 | **[−0.0156, +0.1602]** | **.0083** | ✅ |
| **EXP vs c2_shuf** | +0.0882 | **[−0.0082, +0.1847]** | **.0280** | ✅ |
| (부수) SHOCK vs c0 | −0.0143 | [−0.0553, +0.0268] | 4.2e−14 | ✅ |

**⇒ `equivalent_on_all_axes = True` → 사전등록 분기 = EQUIVALENT_CLOSED.**

**민감도(보고만 · 판정 미사용 · 사전등록)**: Δ_eq=**0.25** → 등가 ✅✅ · Δ_eq=**0.15** → **등가 아님**(CI 상한 0.160 > 0.15).
정직한 사정거리: 우리가 배제한 것은 **|효과| ≥ 0.20**이다. **0.15~0.20 크기의 (양의) 효과는 이 데이터로 배제되지 않는다.**
Δ_eq=0.20은 데이터 보기 전에 못박혔고(분쟁 효과 −0.209/+0.129의 크기 · live 마진의 31%), 사후 조정은 없다(tune-to-red/green 금지).

## 6. 3-seed 교차 회계 — 원 KILL은 세 번째 seed에서도 재현 실패

| seed (disjoint) | EXP − c0 (m_B_conj) | 판정 |
|---|---|---|
| run-1 (사후 recompute · KILL 근거) | **−0.209 ± 0.091** (p=.033) | 유의 열화 주장 |
| run-2 (헤드라인 사전등록 · 130 fresh items) | **+0.129 ± 0.122** (ns) | 부호반전 |
| **run-3 (본 cement · 334 fresh items)** | **+0.072 ± 0.053** (ns) | **부호 run-2와 일치** |

- 이질성: **run-1 vs run-3 → z=2.67, p=.0075** (통계적 불일치) · **run-2 vs run-3 → z=−0.42, p=.67** (일치).
- 3-seed 고정효과 메타: **μ = +0.016 ± 0.043 (z=0.37, ns)**, 90% CI **[−0.055, +0.087] ⊂ ±0.20** · Q=8.11(df=2, p=.001, run-1이 유일 outlier).
- ⇒ **원 KILL의 p=.033은 seed 특이적 잡음 draw였다**는 진단이 3번째 독립 seed로 확증. lane은 **KILL이 아니라 EQUIVALENCE로** 닫힌다.

## 7. 정보채널 (규칙④) · 구조 사실

- `k_t = f(위치 t의 router 누적 mass)` = 입력의 함수(상수 arm이 못 봄) · k_hist {1: 67434, 2: 24726, 3: 0} · **Var(k_t)=0.196 > 0** · 분산 0 시퀀스 비율 **0.000** ⇒ 항진적 arm 아님.
- 프로덕션 router = **DENSE soft mixture**(top-k 없음) ⇒ 모든 capacity gating은 정보를 **버리는** 연산이고, best 상수 k = **dense(c0)** (disjoint pilot에서 선택). EXP(k∈{1,2})가 dense보다 nominal 우위(+0.072)인 것은 이 축이 **잡음 지배**임의 독립 증거(정보 파괴가 성능을 올릴 수는 없다).
- 원거리 branch는 여전히 죽어 있다: c0의 `m_A_conj` = +0.027 ± 0.137 (t=0.19, ns) — 303M read-side의 **살아있는 cue 슬롯 = 1개**(저장소 `best_distinct=1` 벽의 독립 재확인 · arm 무관).

## 8. licensed / not licensed

| 주장 | 상태 |
|---|---|
| organelle lane = reach 레버 (PASS) | ❌ **미지지** (3 seed 전부 양성 0 · 0/3 control) |
| capacity setpoint schedule이 held-out 재조합에 **\|효과\| ≥ 0.20 nats의 방향성 효과**를 갖는다 | ❌ **배제됨** (TOST p=.008, 3축 · V-gate 전부 통과 · powered) |
| **organelle lane CLOSED** ("배분/효율/희소성 계열은 reach 레버가 아니다") | ✅ **LICENSED — EQUIVALENT-CLOSED** (등가 증명 · 검출력 있는 detector 위 · 사전등록 · disjoint 3rd seed) |
| EXP가 재조합을 **유의하게 열화**시킨다 (원 KILL) | ❌ **반증 유지** (부호반전 · 이질성 p=.0075) |
| \|효과\| 0.15~0.20 구간의 (양의) 효과 | 🟡 **미배제** (CI 상한 +0.160) — 이 크기는 reach 레버로 보기엔 live 마진의 <½·spend 정당화 불가지만, 정직히 미배제로 기록 |

**⇒ organelle lane은 닫힌다 — 단 KILL(유의 열화)이 아니라 EQUIVALENCE(방향성 효과 부재)로.**
G1 exit은 여전히 **학습 measure 교체**(H_9267 XBIND 계열)로 단일화된다. 이 lane에 GPU spend 0.

## 9. 산출물

- `PREREG.md` (sha256 pin · 데이터 보기 전 동결) · `run_cement.py` (실행 sha 일치)
- `cement_result.json` (per-item × per-arm 전량 · V-gate · TOST · power · info-channel · VERDICT)
- `prev_exclude_all.json` (run-1 ∪ run-2 배제집합) · `probe.json` (pool 사전확인 · 채점 없음) · `run.log` (PARITY 0.0 포함)
