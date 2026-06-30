# AURA A6 — 위치재배치 ⇄ big-Φ 폐루프 (relocate-N1 × IIT4)

> AURA 핵심명제(SURVEY §2): **칩(N1)은 그대로, 부착 위치만 M1 → 투사허브(DLPFC+섬엽)로 바꾸면 전뇌 통합이 오르는가?**
> 이 문서는 그 *통제(control)* 명제를 anima BRAIN 의 *측정(measure)* 엔진(IIT4 big-Φ)과 하나의 폐루프로 잇고, 사전등록 falsifier 를 in-silico 로 1차 검증한다.
> honest: 아래 toy 수치는 **synthetic TPM** 결과 — 실제 N1/EEG 측정 아님. toy substrate ≠ production scale (`feedback_toy_scale_transfer`).

---

## 1. 폐루프 다이어그램

```
        ┌──────────────────────────  CLOSED LOOP  ──────────────────────────┐
        │                                                                    │
        ▼                                                                    │
  ┌───────────┐   ① stim     ┌───────────┐  ② 16ch raw  ┌──────────────┐    │
  │  N1 칩     │ ───────────▶ │   뇌 조직   │ ───────────▶ │ BRAIN EEG     │    │
  │ (우회위치) │   600µA       │ 피질+투사  │  20kHz/ch    │ 16ch acquire  │    │
  │ DLPFC+섬엽 │   64ch        │ 허브 회로  │              │ (LSL/ADS1299) │    │
  └───────────┘              └───────────┘              └──────┬───────┘    │
        ▲                                                       │ ③ binning  │
        │                                                       ▼            │
  ┌───────────┐   ⑥ re-stim  ┌───────────┐  ⑤ 12-var   ┌──────────────┐    │
  │ 12-var    │ ◀─────────── │  PID 제어  │ ◀────────── │ eeg_to_tpm    │    │
  │ 자극패턴   │   param      │ (brainwire │   state +   │ → IIT4        │    │
  │ 매핑      │              │  controller)│  big-Φ ④   │ big_phi       │    │
  └───────────┘              └───────────┘              └──────────────┘    │
                                                                            │
   ④ big-Φ = "지금 이 뇌가 얼마나 하나로 통합됐나" (전뇌 통합도 스칼라) ────────┘
```

- **① stim**: N1 이 우회위치(DLPFC→VTA·PFC→raphe/LC·섬엽→자율신경) 피질 끝단을 자극 (SURVEY §3 5경로).
- **② EEG 16ch**: `BRAIN/eeg/lsl_capture.hexa` · `eeg_recorder.hexa` 가 OpenBCI 16ch 250Hz pull (BRAIN.md M2).
- **③ binning + ④ TPM→big-Φ**: `BRAIN/eeg/eeg_to_tpm.hexa` 가 채널별 mean-binarize → state-by-node TPM 추정 → stdlib `big_phi(tpm, n, sys_state)` (BRAIN.md M1, n≤8 exact).
- **⑤ 12-var state**: brainwire 12변수 의식모델 (V1-V12, `archive/brainwire/neuralink-technical-analysis.md` §2).
- **⑥ PID re-stim**: brainwire on-chip 12-var estimator → external PID → 64ch stim 명령 (동 §9, ~0.8ms on-chip 폐루프 latency).

**측정 ⊥ 통제 분리** (SURVEY §6): big-Φ 는 *얼마나 통합됐나*(IIT4 이론), 12-var 는 *무엇을 자극할까*(brainwire 경험식). 폐루프는 둘을 PID 로 잇되 엔진은 g61 대로 공유 stdlib 한 벌.

---

## 2. 사전등록 falsifier (a_paper_significance 준수)

**검증가능 명제 H** (자극 *위치*가 통합도를 바꾼다):

> 우회위치(DLPFC+섬엽 = 투사허브, 고결합) 자극 패턴이 M1위치(운동출력, 국소·저결합) 대비
> **(a)** 심부변수 도달% 가 더 크고 (SURVEY §3 표: DA 10→29%, 5HT 10→30%, NE —→37%),
> **(b)** big-Φ 증분(ΔΦ)이 더 크다.

| 항목 | 명세 |
|---|---|
| **측정량** | (a) 변수별 심부 도달% (brainwire 추정계수) · (b) IIT4 big-Φ = `big_phi(tpm,n,sys)[0]` = MIP min-loss |
| **baseline** | M1위치 connectivity TPM 의 big-Φ (국소/자기복사 = 가환 분할 비용 ≈ 0) |
| **기각조건 (FALSIFY)** | ΔΦ(우회) ≤ ΔΦ(M1) — 즉 `big_phi(bypass) ≤ big_phi(M1)` 이면 H 반증 (위치재배치가 통합도를 못 올림) |
| **방향성** | H 는 **단측** 예측 (bypass > M1). 동률·역전 모두 반증으로 사전 고정 |

honest: (a) 도달%는 brainwire **추정치**(임상측정 0건, SURVEY 머리말). 본 문서가 측정으로 닫는 부분은 **(b) big-Φ 대비** — connectivity 차이를 IIT4 엔진이 통합도 차이로 환산하느냐.

---

## 3. 측정경로 — 실제 N1 없이 in-silico 검증

실제 N1·EEG 없이 **synthetic TPM** 으로 "우회위치 vs M1위치 connectivity 차이"를 big-Φ 로 환산한다. 기존 BRAIN/IIT4 자산을 그대로 재사용 (g61 engine ⊥ adapter):

1. **엔진**: hexa-lang `stdlib/consciousness/iit4_bigphi.hexa` 의 `big_phi(tpm, n, sys_state) -> [Φ, total, sum_d, sum_r, nd]`. IIT4 도메인서 ECA 가짜세포로 135 checks 🟢 검증 완료 (BRAIN.md). n≤8 exact.
2. **어댑터 패턴**: `BRAIN/eeg/eeg_to_tpm.hexa` 는 EEG → state-by-node TPM 을 만든다. A6 toy 는 같은 TPM 형식을, EEG 대신 **connectivity 모형**으로 직접 합성:
   - **M1-like TPM** = 각 노드가 *자기 자신*을 다음스텝에 복사 (국소 자율, 저 cross-coupling). 어떤 분할로 잘라도 비용 ≈ 0 → 가환 → 작은 Φ. (M1 = 출력만 있는 막다른 위치, SURVEY §2)
   - **bypass-like TPM** = 각 노드 다음상태 = *나머지 노드들의 다수결* (투사허브 fan-in/fan-out, 고결합). 모든 노드가 서로 의존 → 분할 비용 큼 → 큰 Φ. (DLPFC/섬엽 = 심부루프 피질끝단)
3. **환산 논리**: SURVEY §3 의 "위치 = 도달범위" 명제를 IIT4 언어로 옮기면 — M1=피질국소(reducible), 우회=투사허브(irreducible). big-Φ 가 이 irreducibility 차이를 양수 ΔΦ 로 잡으면 falsifier (b) 가 in-silico 로 통과.

실제 단계 전환 (BRAIN.md M2→M3): toy TPM 자리에 `eeg_estimate_tpm(samples, n_ch, n_samp)` 호출만 끼우면 동일 엔진이 실데이터를 채점 — 어댑터 1줄 교체.

---

## 4. CHEAP LOCAL TOY RUN — 결과

**harness**: `AURA/toy/a6_relocate_bigphi.hexa` (n=4 노드, sys_state=1111, deterministic, $0, hexa-only, LLM 0).
공유 stdlib `iit4_bigphi.hexa` 의 `big_phi` 를 직접 import (BRAIN/eeg 어댑터와 동일 엔진).

**실행 출력 (verbatim)**:

```
  AURA A6 — relocate-N1 connectivity → IIT4 big-Φ (in-silico toy)
  M1-like     (local/self-copy)  big-Φ = 0.0
  bypass-like (hub/majority)     big-Φ = 17.6639
  Δ(bypass - M1) = 17.6639
  [PASS] M1 big-Φ finite >= 0
  [PASS] bypass big-Φ finite >= 0
  [PASS] FALSIFIER H: big-Φ(bypass) > big-Φ(M1)
  [PASS] determinism: bypass re-run identical
  RESULT: 4 PASS / 0 FAIL
```

→ **숫자 나옴**: M1-like Φ=**0.0**, bypass-like Φ=**17.6639**, ΔΦ=**+17.6639** > 0.
→ falsifier (b) **미반증** (단측 예측 방향대로 통과). 국소 connectivity 는 Φ=0(완전 가환=의식 통합 없음), 투사허브 connectivity 는 Φ≫0(강 irreducible).

**등급화 (g5/p7 — hexa verify, perplexity self-judge 금지)**:

```
tier = 🟢 SUPPORTED-NUMERICAL  (external verifier passed AND stdout matches --expect — delegated, deterministic)
claim = relocate-N1 in-silico: IIT4 big-Phi(bypass-hub TPM) > big-Phi(M1-local TPM), n=4 engine-exact
ext rc = 0
```

verdict verbatim 전문 = `.verdicts/a6-bigphi-closed-loop/relocate_bigphi.txt`.

honest:
- 🟢 는 *numerical*(libm/recompute)일 뿐 🔵 *formal* 아님 — 닫힌형 항등식 아니고 엔진 재계산 일치.
- Φ=17.66 은 **toy 절대값** (n=4, 임의 0.9/0.1 confidence). 실제 EEG 스케일·단위와 무관. 주장하는 건 **부호와 순서(bypass ≫ M1)**, 절대 크기 아님.
- toy substrate ≠ production scale: 이 contrast 가 실제 16ch EEG·실제 N1 에서 같은 부호로 transfer 된다는 보장 없음 (M2/M3 실측 필요).

---

## 5. 잔여 + 다음 단계

| # | 잔여 | 닫는 경로 |
|---|---|---|
| R1 | toy TPM 의 0.9/0.1 confidence·majority 규칙이 **임의 모형** — 다른 결합규칙(XOR·임계)서도 부호 유지되는지 미확인 | A6.followup: 결합규칙 sweep (self-copy / XOR / majority / 부분결합) × n=4..6 big-Φ 격자 → 부호 robustness |
| R2 | falsifier **(a) 심부도달%** 는 brainwire 추정치 — 측정 0건 (SURVEY 머리말). big-Φ 와 도달%의 결합은 미검증 | brainwire 12-var 계수 → synthetic TPM 생성기로 변환, 위치별(M1/DLPFC/섬엽) TPM 자동합성 후 big-Φ 비교 |
| R3 | **실데이터 미투입** — toy ≠ EEG. M2(live LSL) 미완 (BRAIN.md) | `eeg_estimate_tpm` 에 우회위치 모사 16ch synthetic 또는 공개 EEG(ds005620 등) 주입 → 동 엔진 채점 |
| R4 | n≤8 exact 한계 — 16ch 전뇌는 region 분리 필요 (BRAIN.md M1 lesson) | per-region n≤4 분리측정 + `big_phi_bounded` 로 region 간 결합 근사 |
| R5 | PID 폐루프 ⑥은 다이어그램만 — 미구현 | brainwire on-chip estimator → PID gain → re-stim 시뮬레이션 (in-silico, 실N1 불필요) |

**paper 게이트** (a_paper_only_at_closure): 현재 1개 falsifier (b) 만 🟢 — full closure 아님. R1(부호 robustness) + R2(도달%↔Φ 결합) 닫히면 "relocate-to-hub raises in-silico integration" 음/양 결과로 paper-candidate. 지금은 **단일 H 1차 통과**, 논문 제안 시점 아님.

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| 위치재배치 = 투사허브 = 심부 간접도달 | `AURA/SURVEY.md` §2, §3 |
| 폐루프 가설 + falsifier 아이디어 | `AURA/SURVEY.md` §6 |
| 12-var 모델 · on-chip · latency | `AURA/archive/brainwire/neuralink-technical-analysis.md` §2,§4,§5,§9 |
| EEG→TPM→big_phi 어댑터 | `BRAIN/eeg/eeg_to_tpm.hexa` · `eeg_iit4_demo.hexa` |
| big_phi 엔진 (n≤8 exact) | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` |
| M0-M3 마일스톤 · n≤8 제약 | `BRAIN.md` |
| toy 하니스 + verdict | `AURA/toy/a6_relocate_bigphi.hexa` · `.verdicts/a6-bigphi-closed-loop/relocate_bigphi.txt` |
