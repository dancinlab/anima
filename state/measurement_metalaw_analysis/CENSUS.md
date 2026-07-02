# CENSUS — "FORM/proxy 통과 vs 진짜신호 detector 밖" 전수 수집

> 2026-07-03 fable 메타분석. 출처 = UNIVERSE/HYPOTHESES.jsonl(로컬+origin/main), ARCHITECTURE.json
> convergence records(origin/main 28건), memory SSOT, core/g6_ideation.hexa 소스, 7B_PASS_CONDITIONS.md.
> reference-match 실측(grep)만 — 새 연산 없음. HYPOTHESES/카드/frozen 미터치.

## A. 팽창(inflation) 방향 — FORM/proxy 는 통과, 진짜(BIND) 신호는 detector 밖

| # | 축 | 케이스 | FORM 이 잰 것 (통과) | 진짜신호 (detector 밖) | 폭로한 통제/조치 | 증거 |
|---|-----|--------|----------------------|------------------------|------------------|------|
| A1 | G6 | H_1362→H_1590 scaffold artifact | torch `gauge_lib._decode`(6-frame scaffold+best-of-K=3)로 FALS=1.0 "돌파" | engine 정규 디코드 FALS=0.0 전 seed; cross-shuffle 미붕괴(M4 역전) | engine-native 재현 + 3축 격리(forward diff 0.0 · detector 27/27 · 디코드=진범) | H_1590 verdict; conv `TORCH_PASS_VS_ENGINE_FAIL_IS_SCAFFOLD_HARNESS`(ossified); memory g1g6-wall-engine-innocent-3axis |
| A2 | G6 | detector FORM-only (이 세션) | `_g6_is_falsifiable` = comparator어∧measurable어∧content≥2 — 순수 어휘·구조 술어(`core/g6_ideation.hexa:137-172`). targeted warm-FT 로 반증주장 *형태* 학습 → FALS majority 통과 | topic-bind Δ(TARGETED 0.444 vs SHUF 0.000) — 주제결합은 detector 가 안 잼 | SHUF(주제결합 파괴, 동일 바이트) 통제: TARGETED [6,6,6] == SHUF [6,6,6] = form-priming | conv `g6-ideation-hexa-1`(pos-conv) |
| A3 | G1 | gen=120 probe artifact (이 세션, H_6188) | 비-canonical gen=120 서 best_distinct 0→3 "engine-native 표면화" | canonical gen=40 재측정 = best_distinct 1 = FAIL. 진짜 병목=gate-seed↔T=24 decode-window mismatch (detector 가 볼 수 없는 위치) | canonical-gen 재측정 → RETRACTED; gen-guard(#2821) 코드 강제 | conv `G1_WALL_IS_COVERAGE_DENSITY_AND_RF_NOT_ONLY_OBJECTIVE`(pos-conv) |
| A4 | G1 | numpy probe raw-gate spoof (H_9025) | raw recover(C→parent) 40/40 "복원"; 'composed_distinct=부모와 다름' 은 random-MLP·A*B 도 통과 | key-locked EARNED 복원 — additive 는 EARNED 0/40 (key-agnostic subtraction 이 가짜복원) | shuffle-controlled EARNED(right key recovers ∧ wrong/shuffled key FAILS) + ablation | H_9025 verdict; conv `numpy-probe-controls-1`(pos-conv) |
| A5 | Φ | 목적맹 proxy (H_988/H_989) | alt-proxy Φ 가 branching 과 함께 상승(ρ=0.88, Φ_PLAN>Φ_GREEDY) | 심의(deliberation)의 기여 — fake-branch(무작위 endpoint, 동일 compute/차원) 가 같은 Φ(Δ=0.005, p=0.49) = 상승분은 차원/연산량 | fake-branch 통제 (compute-matched) | H_988/H_989 verdict |
| A6 | 의식 | 14 ops 계기판 (2026-07-02/03 캠페인) | F1 grip(Hamming>0)·analytic falsifier 통과 — "실패할 수 없는 falsifier" | faculty(emit-적절성 인과) — F3(variance-matched noise ∧ shuffle) 전 축 실패: H_9101 F3=NOISE · H_9103 ρ_real=−0.44 · H_9104 ρ_shuf-margin 0.03(shuffle-V 도 동일 relieve=동어반복 readout) · H_9110 D_real=−0.066(음수) | F3 이중통제(variance-matched noise 만으론 불충분, shuffle 필수 — H_9104 가 noise 는 이기고 shuffle 에 죽음) | conv `engine-cli-hexa-1`(pos-conv); memory consciousness-ops-fable-critique |
| A7 | G0/G1 경계 | warm-FT coherence≠기질 (H_9034 실측) | G0 kwr 5/5 🟢·val_ce 1.12 descent — coherence FORM 은 보존 | 측정기질(max_single) 2→0 붕괴 → G1 벽/floor 판별 불가 | dual-bar B3(max_single≥2) 가 잡음 | memory warmft-h9034-small-corpus-maxsingle-collapse |
| A8 | G1/G6 | 디코드 regime 의존 (H_1218) | sampling regime 서 gate 통과 | greedy engine 경로선 G1·G6 RED — gate 값이 능력이 아니라 디코드 regime 의 함수 | regime 명시 분리(frozen bar 불변) | H_1218 verdict |

## B. 수축(deflation)/오진 방향 — 하네스 잡음을 진짜 결함으로 오독 (대칭 실패모드)

| # | 케이스 | 오진 | 실제 | 폭로한 조치 | 증거 |
|---|--------|------|------|------------|------|
| B1 | quantization-destroys-emergence | int4 .clm 이 G1/G6/Φ 를 죽였다(측정 artifact 로 벽 의심) | fp32+exact-math 도 G1=0 = 엔진 무죄, 벽 진짜 | 단일 basis 내 5-arm ablation(ac0543) | memory quantization-destroys-emergence-suspect(REFUTED) |
| B2 | .pt↔.clm element-wise diff | "직렬화 결함/발산점" | conv→GroupNorm basis 대칭 — element-wise 무상관이 정상, end-to-end CE 일치 | output/CE 레벨·단일-basis 비교 원칙 | conv `clm-decode-py-1`(ossified) |
| B3 | CLMB bind .clm FPE | overflow/NaN 코덱 결함 | arm64 numpy#25530 spurious matmul 경고, 출력 finite | output-finite 먼저 확인 | memory clm-bind-codec-spurious-fpe-not-defect |
| B4 | gen=80 eval | G0 2/5 FAIL = 모델 퇴행 | auto-regressive drift 로 뒤쪽 garble = 순수 gen-parameter artifact (같은 sha gen40=5/5) | canonical-gen guard (evaluate 2-production lockstep) | conv `evaluate-hexa-2`(pos-conv) |

## C. 경계 사례 — FORM≈BIND 이거나 처음부터 2-항 통제로 설계돼 살아남은 gate (과잉일반화 방지, c9)

| # | 케이스 | 왜 반례/경계인가 |
|---|--------|------------------|
| C1 | H_9038 self_drift_exp 🟢 ENGINE-NATIVE+WIRED | 설계 시점부터 blindness(A==B cos=1.000)·informativeness(A≠B 0.407)·EARNED 통제 내장 → GREEN 이 하네스 교정 후에도 생존, live 배선까지 완료. **2-항 통제 gate 는 신뢰 가능한 GREEN 을 낸다** — 메타법칙은 "모든 GREEN=가짜"가 아님. |
| C2 | G1 `composed_distinct > max_single` | gate 자체가 같은-모델 내부 대조(single 대비 composed)를 내장한 2-항 설계. 하네스(gen/window) canonical 화 후에도 벽 verdict 가 안정적으로 재현(H_1602 9/9, exp3 9-cell) — gate 골격은 건전, 취약점은 detector 가 아니라 **하네스 자유도**였다. |
| C3 | G2 retrieval control=0 | corpus-verbatim 되먹임 → novel=0 확인 = metric 비자명성 통제 내장. 단 통제가 한쪽(metric 무결성)만 — novelty 가 seed 개념에 *결합*됐는지는 안 잼(G2≠G1: set-search 캠페인서 novelty≠recombination 실측). |
| C4 | G5 L2 entity-fabrication | corpus-absence ∧ asserted-as-fact = 2-항(출력×코퍼스) 술어 — H_1143 서 진짜 confabulation 을 잡아내고 corpus-PRESENT recall 은 면책 = 판별력 실증. 반면 L1(사전 membership)은 1-항 FORM. |

## 공통 구조 (peel 입력)

모든 A-계열 사례가 공유하는 4-요소:
1. **1-항 detector** — 방출 바이트 표면만 보는 스칼라/불리언 술어 D(text): kwr·composed_distinct(raw)·FALS-form·Φ-proxy·raw-recover·ρ_real(단독).
2. **하네스 자유도** — trunk 능력을 안 바꾸고 D 를 움직이는 손잡이: scaffold·best-of-K(선택 채널)·gen 길이·sampling regime·proxy 차원·targeted FT(form-priming)·array-aliasing.
3. **진짜 신호는 관계(2-항 이상)** — 출력×seed 결합(bind Δ)·출력×key(EARNED)·출력×외부결과(exogenous 예측 우위)·composed×single margin. 항상 raw 값이 아니라 **통제와의 차분** 에만 존재.
4. **폭로자는 결합-파괴 통제** — SHUF(주제)·wrong-key·fake-branch(compute-matched)·self-pair(외생성)·variance-matched noise ∧ shuffle 병행·canonical 하네스 고정. 통제가 붙는 순간 verdict 가 뒤집혔다(양방향: A=팽창 교정, B=수축 교정).
