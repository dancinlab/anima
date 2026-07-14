# CAL-6 — detector 이득(gain) 검산 · 사전등록 (데이터 보기 전 동결)

> 도시에 = `state/fable_killshots/w5_계측결함.out.md` 카드 A (축약판 = §4 "가장 싼 킬샷").
> **이 파일은 spike-in 을 한 줄도 실행하기 전에 작성됐다.** 아래 ladder·PASS 조건·V-gate·TOST 마진·MDE 는
> 결과를 보기 전에 못박혔다. 집행 코드 = `cal6.py` (sha256 은 `RESULT.md` 에 기록 · 실행본과 대조).

## 0. 제6결함 가설 (D6)

census detector 의 **이득(gain)이 1 미만이면** 참 효과를 압축해 실재 효과를 "ns" 로 만들고 **거짓 KILL 을 양산**한다.
기존 5대 결함 체크리스트는 전부 *부풀림(거짓양성)* 만 본다 — pedestal 은 **절편(bias-at-0)** 검사이지
**기울기(gain)** 검사가 아니다. 두 검사는 직교하며, gain 은 원장에서 **한 번도 교정된 적이 없다.**

## 1. 측정 대상 = 실재하는 census detector 6종

집행 대상 데이터 = mito organelle lane F13 (H_9285) 의 **per-item × per-arm 저장 출력** 3 seed
(engine-native 303M `py303_full.clm` aiden decode · PARITY max|Δ|=0.0 · 이미 동결된 파일):

| dataset | 파일 | n_main | 이 데이터가 라이선스한 판정 |
|---|---|---|---|
| run-1 | `mito_organelle_lane/F13_303m_reach_closure/result.json` | 120 | 원 **KILL** (헤드라인 `m_conj=min`) |
| run-2 | `.../refire/refire_result.json` | 100 | INVALID (헤드라인 `m_B_conj`) |
| run-3 | `.../cement/cement_result.json` | 334 | **EQUIVALENT_CLOSED** (TOST · `m_B_conj`) ← organelle lane 의 살아있는 종결 |

저장된 원자값 = arm 별 `m_A_conj`, `m_B_conj`, `s_A`, `s_B` (전부 logP 차분 = nats).
detector 6종은 이 원자값에서 **정확히 재구성**된다 (`margins()` in `run_refire.py:473-482` 그대로):

```
m_A_conj = lift(a|AB) − lift(f|AB)          # 원격 cue 분기 (nats)
m_B_conj = lift(b|AB) − lift(f|AB)          # 근접 cue 분기 (nats)  ← run-2/run-3 헤드라인
m_conj   = min(m_A_conj, m_B_conj)          # ★ 순서통계량 ← run-1 헤드라인 (KILL 라이선스)
m_mean   = 0.5·(m_A_conj + m_B_conj)        # (nats)
dacc     = 1[m_A_conj > 0 AND m_B_conj > 0] # ★ 유계·이진 AND detector (원장 전반의 D-acc 계급)
ceiling  = min(s_A, s_B)                    # ★ 순서통계량 (단일-cue 상한)
```

## 2. SPIKE-IN — 참값이 정확히 계산되는 주입

주입은 **분석입력 수준**(decode 출력 logP)에서, **EXP arm 에만** 건다. control arm 은 손대지 않는다
(통제군 약화 금지 — 주입은 EXP 를 *더 좋게* 만드는 방향이므로 tune-to-green 의 반대가 아니라
"참 효과가 있었다면 detector 가 그걸 봤겠는가" 를 묻는 것).

- **INJ-PROX (주 모델)**: `logP(b|AB) += δ` ⇒ `m_B_conj += δ`, `m_A_conj` 불변.
  근거 = 사전등록 문서가 못박은 "처치가 인과적으로 도달하는 축" = 근접분기(B). 참값 = **δ nats**.
- **INJ-SYM (부 모델)**: `logP(a|AB) += δ` **및** `logP(b|AB) += δ` ⇒ `m_A_conj += δ`, `m_B_conj += δ`.
  참값 = 결합소비가 양 분기에서 δ nats 만큼 진짜로 좋아진 경우. 참값 = **δ nats**.

**사다리** k ∈ {0, 0.5, 1, 2}, δ = k·σ, σ := 그 dataset 의 **item-level paired (EXP−c0) 차분의 sd**
(= 잡음 척도 · 이미 공표된 값: run-3 `prior_sd_item`=1.2192 계열). k=0 = pedestal rung.

## 3. gain 의 정의 (사전 고정 · 사후 교체 금지)

기저 효과를 빼고 **증분**만 본다: `Δ̂_D(δ) := paired-mean_D(EXP_spiked(δ) − c0) − paired-mean_D(EXP − c0)`.

- **STD-GAIN (PRIMARY · 전 detector 공통 · 척도무관)**
  `g_std(D) = OLS-through-origin slope of [ Δ̂_D(δ)/sd_D ] on [ δ/σ ]`
  (sd_D = 그 detector 의 item-level paired 차분 sd = 그 detector 자신의 잡음 단위).
  의미 = **주입된 효과크기(자기 잡음단위) 중 몇 %가 살아남는가**. 유계 detector(dacc)도 정의된다.
- **NAT-GAIN (SECONDARY · nats-값 detector 전용)** `g_nat(D) = slope of Δ̂_D(δ) on δ` — 기대 1.0.

**사전 PASS/FAIL**: `g_std ∈ [0.8, 1.25]` (도시에 카드 A 그대로) — log-gain TOST 마진 ±0.2231(=log1.25).
이탈 = **그 detector 가 라이선스한 모든 KILL/음성판정이 INVALID 후보**.

## 4. pedestal (참값 0) — 2종 · 둘 다 필수

- **P0 (trivial)**: k=0 ⇒ 증분 Δ̂ 가 **정확히 0.0** 이어야 함 (파이프라인 항등성).
- **P1 (RANDSIGN · 진짜 참값-0 pedestal)**: `logP(b|AB) += ε_i·δ`, ε_i ∈ {+1,−1} **정확히 균형**
  (item 절반씩 · seed 20260714 동결). item 별 |섭동| = δ 로 실효과와 동일 크기지만 **참 평균효과 = 0**.
  PASS = 증분 Δ̂ 가 0 과 **TOST 등가** (마진 = 그 detector 의 MDE, §6).
  **이 pedestal 에서 0 이 아닌 값을 뱉는 detector = 잡음으로부터 가짜 효과를 제조하는 detector**
  (= 거짓 KILL 제조기). 참값이 구성상 0 이므로 어떤 비-0 도 순수 계기 편향이다.

## 5. 양성대조 (필수 · 실패 시 전체 INVALID)

- **PC-1 (해석적 항등성)**: INJ-PROX 하에서 `m_B_conj` 의 g_nat = **1.000 ± 1e-9** 이어야 한다
  (m_B += δ 는 산술 항등식). 아니면 harness 가 고장난 것 ⇒ 전체 INVALID.
- **PC-2 (검출 라이브니스)**: k=2 rung 에서 `m_B_conj` 의 paired-t 가 **유의**(p<.05, 주입효과 회수)해야 한다.
  아니면 파이프라인이 2σ 짜리 실효과조차 못 보는 것 ⇒ 전체 NOT-POWERED.

## 6. 검정력 — 데이터(주입 결과) 보기 전 계산

- 각 detector 의 item-level paired sd(sd_D) 는 **기존 저장파일에서** 이미 알 수 있다(주입 무관).
- `MDE_D(α=.05, power=.8) = 2.80 · sd_D / √n`.
- gain 의 표준오차: `se(g_nat) = se(Δ̂)/δ = (sd_D/√n)/δ`. k=1 rung(δ=σ) 기준 run-3(n=334):
  `se ≈ (0.97/18.3)/1.22 ≈ 0.044` ⇒ PASS 경계 이탈폭 0.20 을 **4.5σ** 로 검출 ⇒ POWERED.
- **N 부족(se(g) > 0.10)이면 그 dataset 은 판정하지 않고 NOT-POWERED 로 보고**한다.
- gain CI = **item-level (run-3) / block-level (run-1·run-2) bootstrap 10,000** (paired 구조 보존).

## 7. 금지 (위반 = 결과 무효)

- 사후 detector 교체·헤드라인 재선택 금지. 6 detector 전부 보고 (선별 금지).
- `Δ = exp − max(controls)` 금지 — 대조는 **c0 하나로 고정**, paired-t 만.
- 통제군(c0) 에 주입 금지 (통제군 약화 = tune-to-green).
- 음성 주장(= "gain 정상, D6 사망")은 **log-gain TOST** 로만. 'ns' 금지.
- pedestal(P0·P1) 또는 양성대조(PC-1·PC-2) 실패 시 verdict = **INVALID** (PASS/FAIL 아님).

## 8. 사전등록 판정분기 (실행 가능한 코드)

```python
if not (PC1_pass and PC2_pass):        verdict = "INVALID"        # 양성대조 실패
elif not (P0_pass and P1_pass_linear): verdict = "INVALID"        # pedestal 실패
elif any(se_gain > 0.10):              verdict = "NOT-POWERED"
elif all(0.8 <= g_std[D] <= 1.25):     verdict = "FAIL"           # D6 가설 사망 (전 detector 이득 정상)
else:                                  verdict = "PASS"           # ≥1 detector 이득 이탈 ⇒ 그 detector 의 KILL = INVALID 후보
```

- **PASS** = D6 실재 ⇒ 이탈 detector 가 라이선스한 음성판정 전수 INVALID 후보 (원장 재감사).
- **FAIL** = 전 detector gain≈1 ⇒ "제6결함=이득" 가설 사망, 원장 문제는 검정력 단일원인으로 확정.

## 9. 사정거리 (미리 인정)

- 이 검산은 **F13 lane 의 3 seed 저장출력**에 한정된다. 다른 lane 의 detector(예: NBIND-G 의 held-out
  D-acc)는 **같은 계급(유계 AND/순서통계량)** 이면 결론이 전이되지만, 그 lane 의 per-item 파일에서
  재검산해야 확정된다 — 여기서는 **계급 수준 전이**만 주장한다.
- 이 검산은 gain 만 본다. gain 이 정상이어도 검정력 부족(D7·D12)은 별개로 살아있다.
