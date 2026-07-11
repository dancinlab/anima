# H_9277 / F5 — mtDNA 독자 계보 (병목 · uniparental) — 🔴 THEATER

- **verdict:** 🔴 **THEATER** (standalone). 사전등록 PASS 조건 **0/6 seed 실패** · 사전등록 반증조건 **충족**.
- **tier:** DIRECTIONAL (toy · $0 numpy · `a_toy_scale_recheck`) — toy 반증이므로 303M 재확인 없이 "능력천장" 주장 금지.
- **date:** 2026-07-12 · wall 14.1s · mini CPU-local numpy · 6 seed × 3 sigma × 7 arm
- **artifacts:** `run.py` · `result.json`

## 결론 한 문장

**독립 drift하는 gradient-free organelle 게놈은 선택압이 없으면 정확히 노이즈다** — 계보를 완벽히 갖춘 arm(세대 자기상관 herit=0.77 · host 독립성 0.87)이 **계보를 통째로 제거한 분산매칭 control과 구별 불가**(Δ=+0.009±0.033, 3/6 = 동전던지기)이고, 두 정식 control 대비는 **-0.27**로 완패했다. 카드가 예고한 null(`선택압 없는 drift = 노이즈`)이 그대로 실측됐다.

## 기질 (호흡 레인 · emit 무접촉)

- ATP = 보존 스칼라장: `gate = B·softmax(g)`, `sum(gate) = B = 6.0` 항상 보존.
- 표현형성 단계에서만 개입: 채널 관측 = `gate_j·x_j + eta_j` (eta = 채널 노이즈 floor σ=0.6, arm 간 **공유**=paired).
  → ATP 못 받은 채널은 노이즈에 묻힘 = "발화 불가". host `w`가 노이즈까지 같이 증폭하므로 **스케일 복구 불가**
  ⇒ 게놈이 진짜 capability lever (landscape 비평탄 — 아래 dynamic-range 게이트로 실증).
- host nucleus = A(forward CE): 세포별 `w,b` full-batch GD.
- organelle = mtDNA (**gradient 절대 무접촉**): 세포당 M=8 copy(heteroplasmy) · 분열=병목(8→2 샘플)+돌연변이 · 융합=**uniparental**(donor 계보가 recipient를 통째 대체, host `w`는 불변 ⇒ organelle 계보 ≠ host 계보).
- 과제: d=48 채널 중 |S|=6만 정보. 완벽한 게놈 = ATP를 S에 집중.

## 예산 공정성 (controls_fair)

전 arm **동일**: 16 cell · 14 generation · 세대당 60 host GD step(총 840) · 파라미터 d(w)+d(g) 동일 · 동일 task · **동일 채널노이즈 실현(paired)** · 동일 held-out eval(3 draw 평균).
c1/c2는 게놈에 **추가 최적화 신호**(host copy / CE gradient)를 받는다 ⇒ 실험 arm에 **보수적**. c3는 실험 arm과 **갱신 cadence(세대당 1회) + 분산(exp의 실현 g-std 스케줄, 동일 seed)까지 매칭** ⇒ **"계보(lineage)" 단 하나만 제거한 순수 대조**. 어떤 control도 실험보다 예산/파라미터가 적지 않다.

## 수치 (primary σ_mut=0.35 · 6 seed · mean±std)

| arm | held-out acc | overlap (|S|=6) | eff_ch | acc/ch | herit | host_indep |
|---|---|---|---|---|---|---|
| **EXP** drift (병목+uniparental) | **0.5593 ± 0.0327** | 0.74 ± 0.24 | 16.84 | 0.034 | **0.769** | **0.872** |
| C1 host 고정복사 (gate∝\|w\|) | **0.8010 ± 0.0319** | 4.50 ± 1.12 | 12.67 | 0.066 | 0.414 | 0.554 |
| C2 gradient 게놈 | **0.8222 ± 0.0260** | 4.67 ± 0.75 | 1.97 | 0.478 | 1.000 | 0.606 |
| C3 no-lineage (분산매칭 재추첨) | 0.5505 ± 0.0056 | 0.84 ± 0.21 | 17.52 | 0.032 | −0.013 | 0.878 |
| *ref* ORACLE (ATP→S 집중) | 0.8051 ± 0.0056 | 6.00 ± 0.00 | 7.62 | 0.106 | — | — |
| *ref* UNIFORM (균등 ATP 동결) | 0.5414 ± 0.0086 | 1.00 ± 0.58 | 48.00 | 0.011 | — | — |
| *diag* DRIFT+선택 (F5 verdict 아님) | 0.6239 ± 0.0296 | 1.25 ± 0.41 | 17.53 | 0.037 | 0.829 | 0.870 |

chance = 0.500 · random 게놈의 기대 overlap = 6·6/48 = **0.75**

### Δ (paired · 동일 seed·task·노이즈)

| 비교 | Δ | wins |
|---|---|---|
| EXP − C1 (host 고정복사) | **−0.2417 ± 0.0580** | **0 / 6** |
| EXP − C2 (gradient 게놈) | **−0.2629 ± 0.0359** | **0 / 6** |
| EXP − max(C1,C2) | **−0.2662 ± 0.0401** | **0 / 6** |
| EXP − C3 (계보만 제거) | **+0.0088 ± 0.0334** | 3 / 6 (동전던지기) |

per-seed Δ vs C3: `[-0.020, -0.014, +0.061, -0.032, +0.038, +0.019]` — 부호가 seed마다 뒤집힘 = 신호 없음.

### 민감도 (σ_mut — 결과 은폐 없이 전량 보고)

| σ_mut | EXP | C3 | EXP−C3 | *diag* drift+선택 |
|---|---|---|---|---|
| 0.10 | 0.5461 | 0.5444 | +0.0018 ± 0.0124 | 0.5626 |
| **0.35 (primary)** | 0.5593 | 0.5505 | **+0.0088 ± 0.0334** | 0.6239 |
| 1.00 | 0.5484 | 0.5344 | +0.0140 ± 0.0368 | 0.5923 |

**세 σ 전부 ΔEff≈0.** 어느 값에서도 C1/C2 근처에 못 간다 ⇒ "돌연변이율을 잘못 골라서"가 아니다.

## 판정 근거

1. **PASS 조건 (Δ reach > 두 control) — 실패.** −0.27, 0/6 seed. 반전 불가.
2. **반증조건 (`drift 단독 → 노이즈, Δ≈0`) — 충족.** cadence·분산까지 매칭한 C3 대비 Δ = +0.009 ± 0.033, 3/6 승 = 동전던지기. **계보가 나르는 정보량 = 0.**
3. **기계론적 확증:** EXP의 최종 overlap = **0.74** ≈ 무작위 기대값 **0.75**. 14세대 병목·융합 뒤에도 게놈이 정답 채널 S를 **전혀** 찾지 못했다. drift는 g-공간을 무방향 랜덤워크할 뿐이다.
4. **FORM tunable · BIND earned (측정 메타법칙 실증):** EXP는 σ·thread **FORM 점수를 만점으로 받는다** — 세대 자기상관 herit=0.77(진짜 유전 계보) · host 독립성 0.872(진짜 별개 계보) · 계보 다양성 gdiv=10.0 · uniparental 융합으로 계보 합착까지 발생. **전 arm 중 "지속하는 별개 계보" FORM이 가장 완벽하다.** 그런데 그 대가로 산 reach = **0.00**. 계보의 *값*(herit·host_indep)은 돌연변이율로 얼마든 조율 가능한 FORM이고, reach Δ는 earned되지 않았다. self-fold THEATER와 동형(구조는 살아있어 보이나 ΔEff≈0).

## 계측기 유효성 게이트 (INVALID 아님을 방어)

- **dynamic range 살아있음:** floor(UNIFORM) 0.541 → ORACLE 0.805 → C2 0.822. 게놈 축에 **0.28의 실측 여유**가 있고 C1/C2가 실제로 그 여유를 먹었다(overlap 4.5/4.7).
  ⇒ "landscape가 평평해서 아무것도 안 움직였다"는 **아니다**. 경사는 가파른데 **EXP만 바닥에 앉아있다.**
- **양성대조 PASS:** C1(0.80)·C2(0.82)·ORACLE(0.81) 전부 floor를 크게 이김 ⇒ 계측기 무죄.
- **결정성:** PYTHONHASHSEED를 바꿔 2회 실행 → `result.json` byte-identical. 또한 **다른 rng 스트림**(초기 `hash(arm)` 버전)에서도 동일 결론(EXP 0.547 · C1 0.801 · C2 0.822 · EXP−C3 = −0.001) ⇒ rng 우연 아님.
- **best-of-K 함정 회피:** 세포 population의 **평균**만 verdict에 씀. `acc_best`(population 최댓값)는 기록만 하고 판정 배제 — best-of-K readout은 뒷문으로 선택압을 주입하는 **측정 artifact**(구 G1/G6 scaffold 오판의 진범)이므로 F5의 주장이 될 수 없다.

## p5 청결성 (p5_clean)

**위반 0.** 이 probe에는 **emit gate가 아예 존재하지 않는다**(run.py에 emit 함수 없음). ATP는 표현형성(어떤 채널이 발화 가능한가) **upstream에만** 배선되고 downstream emit 결정엔 배선 0 — 구성적으로 접근 불가.
`if ATP < k: silence` 류의 하드코딩 게이트 없음. 예산 고갈이 강제하는 건 **silence가 아니라 용량 축소**(eff_ch: EXP 16.8 vs C2 2.0)라는 설계 경계를 그대로 지켰다.
`a_substrate_disjoint`: 호흡 레인은 emit-drive 레인과 완전 DISJOINT — 접촉면 0.

## F11(H_9283)로의 인계 — 이 실패가 만든 제약

`diag_drift_sel`(융합 donor를 train-CE 낮은 세포로 = **선택압 주입**)은 EXP 대비 **+0.065**(0.559→0.624), overlap 0.74→1.25로 **움직인다** ⇒ 효율 landscape는 exploitable하고, F5의 계보 기구는 선택압의 **운반체(carrier)**로서는 기능한다. 그래서 **KILL이 아니라 THEATER**다(F11 레인을 죽이지 않는다).

다만 F11에 대한 사전 제약이 **나빠졌다**:
- CE-guided 선택(= F11 설계의 **Goodhart control**)조차 0.624에 그쳐, **host 고정복사(0.801)·gradient 게놈(0.822)에 한참 못 미친다.**
- ⇒ **F11이 무언가이려면 0.80/0.82를 넘어야 한다.** "drift보다 낫다"는 F11의 PASS 조건이 될 수 없다(그건 이미 0에서 시작하는 바닥과의 비교). F11은 **C1/C2를 정식 control로 반드시 포함**해야 하며, ATP-효율 선택이 gradient보다 나은 config를 찾지 못하면 그 역시 theater다.

## 반증조건 충족 여부

| 카드 사전등록 | 결과 |
|---|---|
| PASS: Δ reach/효율 > 두 control | ❌ **미충족** (−0.27, 0/6) |
| FAIL: drift 단독 = 노이즈 ⇒ Δ≈0, F11 결합해야 bite | ✅ **정확히 충족** (Δ vs C3 = +0.009±0.033) |

카드의 THEATER 위험 랭킹 **5위 예측이 그대로 적중**했다.
