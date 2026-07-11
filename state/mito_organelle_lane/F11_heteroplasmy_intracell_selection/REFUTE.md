# REFUTE — H_9283 / F11 적대적 검증 노트

**판정: 🔴 REFUTED — 원 결론(KILL · "효율은 THEATER가 아니라 잘못된 나침반")은 반박된다.
정정 판정 = 🎭 THEATER.**

가설 자체는 어차피 죽는다(earned lift 0). 반박되는 것은 **verdict tier와 그에 딸린
메커니즘 서사**다. 원 RESULT.md는 "THEATER가 **아니다** — 효율 선택이 earned를 **적극
훼손**한다"고 명시적으로 주장한다. 이 주장이 seed 노이즈의 산물임을 아래에서 보인다.

---

## 0. 통과한 체크리스트 (정직하게 — 이 probe는 설계가 잘 돼 있다)

| # | 항목 | 결과 |
|---|---|---|
| 1 | control 동일 예산 | ✅ **PASS**. 모든 evo arm이 매 세대 f_eff·f_ce·f_oracle **셋 다** 계산(run.py L322-324). 동일 M=24·GENS=10·EPOCHS=100·SIGMA·BETA·k=2·동일 trunk init(rng 10000+seed)·동일 게놈 init 및 RNG 스트림(rng_evo 9000+seed, perm은 모든 arm에서 draw). flops 동일. **arm은 공정하다.** |
| 3 | held-out 누출 | ✅ **PASS**. `split_pairs`가 held (a,b)를 학습에서 완전 배제(모든 a·b는 다른 파트너와만 등장) ⇒ 쌍 암기 = held parity 0.5. `fit_oracle`은 held 라벨을 쓰지만 **V1 arm 전용**이며 exp/c1/c2/c3의 replicator에 절대 들어가지 않음(L330-339). 누출 없음. |
| 5 | p5 위반 | ✅ **CLEAN**. 코드 전수 grep — emit/silence/speak 게이트가 **존재하지 않는다**. ATP는 `S = A·sigmoid(u)` → top-k mask 한 곳에만 닿는다. 하드코딩 emit gate 0. |
| 6 | tune-to-green | ✅ 흔적 없음. 디렉터리에 sweep 산출물 0, verdict rule이 헤더에 사전등록, K=2는 F6 cap 곡선에서 a priori. (오히려 반대 방향 — 아래 참조.) |

⇒ **INVALID 아님. 불공정 control 아님. p5 위반 아님.** 반박은 다른 축에서 나온다.

---

## 1. 치명 결함 A — verdict 통계량이 `max`(3 control) = **선택편향된 비교자**

`run.py` L387-390:

```python
best_c = max(summary[c][key]["mean"] for c in CONTROLS)   # max order statistic
return dict(..., delta = e - best_c)
```

Δ를 **3개 control의 최댓값**에 대해 잰다. control 3개가 참값이 동일해도, n=5·per-arm
std≈0.05~0.06(SEM≈0.023~0.027)에서 `E[max of 3] ≈ μ + 0.85·SEM ≈ μ + 0.02~0.03`.
즉 **exp가 control과 완전히 동등해도 이 규칙은 Δ ≈ −0.02~−0.03을 기계적으로 만들어낸다.**
그런데 KILL/THEATER 분기 임계값이 바로 **0.02**다(`earned_flat = |Δ|<0.02`).

⇒ verdict 분기가 max-편향과 같은 크기의 스케일 위에 서 있다. 올바른 비교자는
pooled control mean 또는 paired test다.

## 2. 치명 결함 B — earned Δ가 **seed 분산 안**에 있다 (체크리스트 #4 → THEATER)

원본 5-seed, **paired**(동일 seed·동일 init) t-검정:

| 지표 | exp−c1 | exp−c2 | exp−c3(ARM-SHOCK) |
|---|---|---|---|
| held_conj | −0.016 · t=**−0.39** · exp **3/5승** | −0.031 · t=−0.93 | −0.027 · t=−0.57 |
| held_acc | −0.036 · t=−0.90 · exp 2/5승 | −0.070 · t=−2.13 | −0.041 · t=−0.99 |

**유의한 게 하나도 없다.** held_conj에서 exp는 c1_drift를 **5 seed 중 3개에서 이긴다.**
RESULT.md의 헤드라인 "exp가 이긴 control = 0/3"은 **평균 인공물**이다.

## 3. 결정타 — seed 20개로 검정력만 올리면 결론이 **뒤집힌다**

하이퍼파라미터 **한 글자도 안 건드리고** SEEDS=0..19로만 확장(= tune-to-green이 아니라
순수 power 증가. 재현: `scratchpad/refute_power.py`).

### EARNED (BIND)

| 지표 | exp | c1_drift | c2_ce | c3_shuf | exp−pooled ctrl |
|---|---|---|---|---|---|
| **held_conj** | **0.8453** | 0.8388 | 0.8630 | 0.8606 | **−0.0088 · t=−0.64 · 11/20승** |
| **held_acc** | **0.8151** | 0.8037 | 0.8469 | 0.8334 | **−0.0129 · t=−0.88 · 10/20승** |

- exp−c1_drift: held_conj **+0.0065 (t=+0.36, 13/20승)** · held_acc **+0.0114 (t=+0.55, 13/20승)**
  ⇒ **5-seed에서 보고된 "drift에게도 진다"의 부호가 뒤집힌다.**
- exp−c3_shuf(ARM-SHOCK): held_conj −0.015 (t=−0.90) · held_acc −0.018 (t=−1.07) → **ns**
- exp−c2_ce: held_conj −0.018 (t=−1.03) · held_acc −0.032 (t=−1.78) → **ns (p>0.05)**
- **pooled control 대비 |Δ| = 0.009 / 0.013 → run.py 자신의 THEATER 밴드(|Δ|<0.02) 안쪽.**
- 원본 exp held_acc 0.773은 20-seed에서 **0.815**. 5개 seed가 exp에 나쁜 뽑기였을 뿐이다.

### SELF-METRIC (FORM · 게임가능)

| 지표 | exp−pooled ctrl (n=20) |
|---|---|
| eff | **+0.0437 · t=+10.65 · 20/20** |
| conj_index | **+0.0766 · t=+7.28 · 20/20** |

⇒ **FORM은 바위처럼 단단하고, BIND는 정확히 0이다.** 이건 이 레포 메타법칙
(FORM tunable · BIND earned)의 **THEATER 정의 그 자체**다.

## 4. 메커니즘 서사도 붕괴한다

RESULT.md §5의 논증 축들을 하나씩:

1. **"ARM-SHOCK(c3)이 '붕괴 탓' 변명을 차단한다 — c3는 더 붕괴(ESS 2.1<3.1)하고도 exp보다
   낫다"** → 이 "낫다"가 **paired t=−0.57 (n=5) → n=20에서 t=−0.90, ns**. 노이즈다.
   ⇒ **"효율 신호의 방향 그 자체가 해롭다"는 결론의 유일한 근거가 사라진다.**
2. **"효율압이 공짜였던 additive 성분까지 파괴한다 (held_add 0.904 vs c2 0.982)"** →
   n=20에서 exp−c2 held_add = −0.037 (t=−4.62) **로버스트하지만**, exp−c3 = −0.015 (**t=−1.47, ns**),
   exp−c1 = −0.004 (**t=−0.38, ns**). 즉 **"효율이 additive를 파괴"가 아니라 "CE-선택(c2)이
   additive를 특히 잘 보존"**일 뿐이다 — c2의 적합도가 CE이고 CE 안에 topic 주효과가
   **문자 그대로 들어있으니** 당연하다. 무선택(c1)·무신호강선택(c3) 대비로는 파괴 증거 없음.
3. **"선택 < drift (아무것도 안 하는 게 낫다)"** → n=20에서 **거짓**. exp가 drift를 두 earned
   지표 모두에서 13/20으로 앞선다(둘 다 ns).
4. **"효율 신호를 더 세게/더 오래 밀면 더 나빠질 것으로 예측된다"** → **근거 없는 예측.**
   관측된 것은 harm이 아니라 **무효과**다.

## 5. 살아남는 것 (오히려 강해지는 것)

- 🏆 **conj_index는 G1 비트가 아니다** — 이 발견은 반박되기는커녕 **더 깨끗해진다**:
  n=20에서 conj_index +0.077 (t=+7.3, 20/20)인데 held_conj Δ ≈ **0.000**. "코드가 비가산적"
  ≠ "일반화되는 conjunction". 1-항 FORM detector는 게임가능하고, 방금 게임당했다.
  형제 패밀리(F6 등)는 conj_index 단독으로 conjunction을 주장하면 안 된다. **이 경고는 유지.**
- **V1 liveness PASS** — oracle(held_conj 0.927) > drift(0.837). 탐색공간에 reach를 올리는
  config가 실재하고 GA가 찾아낸다. INVALID 아님. **유지.**
- **가설 H_9283은 어차피 죽는다** — ATP-효율 선택은 earned reach를 **한 톨도** 올리지 못한다
  (Δ ≈ 0, 20 seed). 레버로서 폐기하는 실무 결론은 변하지 않는다.
- **arm 예산 공정성 · p5 clean · held-out 무결성** — 전부 진짜. 설계 자체는 모범적이다.

## 6. 왜 이게 중요한가 (tune-to-green의 거울상)

이 보고서의 오류 방향은 tune-to-green이 아니라 **over-claimed negative**다. 음수 결과도
정당하다(honesty) — 그러나 **음수의 크기를 노이즈에서 읽어내면 그것도 Goodhart다.**
"효율은 잘못된 나침반이고 밀수록 나빠진다"는 서사는 F6/F10 등 형제 패밀리의 설계 결정을
잘못된 방향으로 오염시킨다(실제로는 "효율은 무해하지만 무익한 나침반"). 그리고
`delta = e − max(controls)` 패턴은 이 레인의 **다른 probe에도 그대로 복사돼 있을 가능성이
높다** — 전 F-family에서 `best_control` = max 통계량을 pooled-mean/paired 검정으로 교체해야
한다. n=5 · per-arm std 0.05에서 max-of-3 편향(≈0.02~0.03)은 KILL/THEATER 임계값과 같은 크기다.

## 7. 정정 판정

```
verdict:          KILL  →  🎭 THEATER
controls_fair:    true  (arm 예산은 공정 · 단 verdict 비교자(max-of-3)는 편향)
p5_clean:         true  (확인)
held_out_clean:   true  (확인)
earned Δ (n=20, pooled ctrl):  held_conj −0.009 (t=−0.64) · held_acc −0.013 (t=−0.88)  → FLAT
FORM Δ  (n=20, pooled ctrl):   eff +0.044 (t=+10.7) · conj_index +0.077 (t=+7.3)      → 확실
정의상: FORM ↑↑ · BIND ≈ 0  ⇒  THEATER (run.py 자신의 사전등록 규칙 문언 그대로).
```

**재현:** `OMP_NUM_THREADS=2 python3 <scratchpad>/refute_power.py` (20 seed · ~60s · 하이퍼 무변경)
