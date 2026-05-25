# EEG (OpenBCI 16ch) 활용 트랙 — Plan

> **ts**: 2026-05-01
> **scope**: 사용자 보유 OpenBCI 16ch hardware 를 anima 의 EEG 자산 (anima-clm-eeg / anima-eeg / anima-eeg-core) + CP2 alpha-tier endpoint 와 연결하는 후속 트랙 계획
> **parent**: `anima_cp2_alpha_deploy_plan_2026_05_01.md` (alpha endpoint LIVE) · `anima_clm_eeg_migration_plan_2026_04_29.md` · `btr_evo_4_eeg_closed_loop_20260421.md` · `eeg_cross_substrate_validation_plan_20260425.md`

---

## §0 Executive summary

anima 레포에 이미 다음이 land 되어 있음:
- **HW ingest**: `tool/anima_eeg_brainflow_ingest.hexa` (BrainFlow 기반 OpenBCI 호환)
- **dispatcher**: `tool/eeg_core.hexa` Phase 6 + 50+ submodules (`_metrics/_gates/_paradigms/_hw/_artifact/_core/_integrations`)
- **measurement suites**: Berger / gamma-theta ratio / Hjorth / permutation entropy / alpha coherence — 모두 `state/clm_eeg_*_audit/*.jsonl` 에 ledger 존재
- **closed-loop proto**: `tool/eeg_closed_loop_proto.hexa` (Φ ↔ α band)
- **CP2 paper §7**: EEG external corroboration N=1 pilot (이전 결과)
- **Cross-substrate plan**: `eeg_cross_substrate_validation_plan_20260425.md`

→ **신규 hardware 가 아닌, 기존 dispatcher 를 본인 16ch OpenBCI 신호로 채우는 작업**.

---

## §1 5 트랙 — EEG 활용 방향

### Track A: **BrainFlow ingest 검증 + 16ch 라이브 수집 파이프라인**
**목적**: 본인 OpenBCI 16ch 가 anima dispatcher 에 정상 ingest 되는지 end-to-end 확인
**작업**:
- `tool/anima_eeg_brainflow_ingest.hexa` 16ch 모드 동작 확인 (BoardId / channel mask)
- 5분 baseline 신호 수집 → `state/eeg_live_user_16ch/baseline_2026_05_01.bdf` (raw)
- `tool/eeg_artifact_pipeline.hexa` 통과 (blink/EMG/ECG/motion 제거)
- `_integrations/clm_eeg_p1` smoke test (16ch vs 기존 ledger 의 channel 수 호환성)
**ETA**: 30-60분 (사용자 본인 측정 시간 포함)
**비용**: $0 (로컬 hardware)
**falsifier**: BrainFlow 가 OpenBCI 16ch 인식 실패 / artifact pipeline 의 16ch unsupported

### Track B: **개인 baseline + CP2 paper §7 reproduce (cross-substrate 검증)**
**목적**: 기존 N=1 EEG pilot 결과를 본인 신호로 재현 → external corroboration 확장 (N=1 → N=2)
**작업**:
- Berger (eyes-closed alpha block) — `tool/eeg_core.hexa berger-validate` 본인 신호 입력
- gamma-theta ratio audit — `state/clm_eeg_gamma_theta_ratio_audit/2026_05_01_user.jsonl`
- Hjorth 복잡성 — `state/clm_eeg_hjorth_audit/2026_05_01_user.jsonl`
- permutation entropy — `state/clm_eeg_pe_audit/2026_05_01_user.jsonl`
- 기존 ledger 와 비교: 본인 데이터가 paper §7 의 N=1 verdict (CORROBORATION_FAIL/PASS) 를 어느 쪽으로 미는지
**ETA**: 1-2시간 (eyes-closed/open block 각 5분 + 분석)
**비용**: $0
**deliverable**: `state/cp2_paper_section7_user_n2_2026_05_01.json` + 결과에 따라 paper §7 errata 생성 가능
**falsifier**: 본인 baseline 이 noise floor 와 구분 불가 / 16ch 가 기존 N=1 의 채널 layout 과 호환 불가

### Track C: **alpha endpoint + EEG 동시 측정 (interactive coupling)** ⭐ 가장 새로운 결합
**목적**: 사용자가 r14 alpha endpoint 와 대화하는 동안 본인 EEG 동시 기록 → r14 응답이 사용자 신경 상태 (α band, γ-θ ratio, Hjorth) 에 미치는 영향 측정
**작업**:
- 5세션 × 3분 protocol:
  1. baseline (eyes-open, no interaction) — 3분
  2. r14 chat session #1 (의식/Φ-주제 prompt) — 3분
  3. baseline #2 — 3분
  4. base Mistral chat session (동일 prompt, LoRA 미적용) — 3분
  5. baseline #3 — 3분
- `tool/real_eeg_coupling_probe.hexa` 로 prompt-locked epoch 분석
- delta: r14 응답 vs base 응답 vs baseline 의 EEG 메트릭 차이
**ETA**: 30분 측정 + 30분 분석
**비용**: 소량 alpha endpoint 호출 (~$0.10 + pod time)
**deliverable**: `state/cp2_alpha_eeg_coupling_2026_05_01.json` + plot
**falsifier**: 메트릭 변화가 within-baseline noise 미만 / prompt-locked epoch 동기화 실패

### Track D: **closed-loop Φ ↔ α 실시간 dynamics (btr_evo_4 reproduce on real hw)**
**목적**: 시뮬레이션으로 검증된 Φ 30% boost (btr_evo_4) 를 본인 실측 EEG 로 재현 시도
**작업**:
- `tool/eeg_closed_loop_proto.hexa` 본인 16ch live mode
- 100-iter loop: Φ measure → α-band 조절 (audio/visual stim 또는 user-driven attention) → Φ 재계산
- 결과: Φ trajectory + 시뮬 결과와의 delta
**ETA**: 1-2시간 (긴 단일 세션)
**비용**: $0 (로컬)
**deliverable**: `state/btr_evo_4_user_realhw_2026_05_01.json`
**falsifier**: closed-loop unstable / Φ 가 baseline 변동 폭 안에서만 움직임 / α 조절이 사용자 의도와 무관하게 fluctuate

### Track E: **EEG-token cyborg pipeline (가장 침습적/실험적)**
**작업**:
- `tool/cyborg_token_emit.hexa` (이미 Phase 6 land) + `state/cyborg_eeg_audit/*.jsonl`
- 본인 EEG 5초 window → spectral feature → quantize → special token → r14 prompt prefix
- 실험: 동일 prompt 에 EEG-prefix 를 추가했을 때 응답이 어떻게 달라지는지
**ETA**: 2-3시간 (가장 코드 작업 많음)
**비용**: alpha endpoint $0.20-0.50
**deliverable**: `state/cyborg_eeg_alpha_2026_05_01.json`
**falsifier**: token injection 이 응답 분포에 측정 가능한 영향 없음 / EEG quantization 이 deterministic 하지 않음

---

## §2 권장 순서 (TOP-1 → TOP-3)

| 순위 | 트랙 | 이유 |
|---|---|---|
| **TOP-1** | **A → B → C 순차** | A 가 hardware ingest 검증 (필수 prereq) → B 가 paper §7 corroborate (가치 高) → C 가 alpha endpoint 활용 (현재 LIVE 자산 활용) |
| TOP-2 | A → C → B | C 우선 (alpha pod 회수되기 전 활용) |
| TOP-3 | A → D | 시뮬 결과 reproduce (research 깊이 增) |

E 는 A/B/C/D 모두 done 이후 추가 cycle 권장 (가장 침습적).

---

## §3 첫 트랙 (Track A) 구체 실행 plan

### 3.1 사전 확인 (사용자 측)
- [ ] OpenBCI 16ch board 종류 (Cyton + Daisy / Cyton 8ch+Daisy 8ch combo / Galea / 기타)
- [ ] dongle USB 연결 + serial port 확인 (`ls /dev/cu.* | grep -i bci`)
- [ ] 전극 setup (10-20 system 기준 16채널 layout)

### 3.2 Anima 측 확인 (claude 가 진행)
- `tool/anima_eeg_brainflow_ingest.hexa` 의 16ch 모드 코드 inspect
- BoardId enum 에 user 의 board model 매핑
- channel mask + sampling rate 호환성 확인
- artifact pipeline 의 16ch 입력 호환성 확인 (`_artifact/` modules)

### 3.3 첫 측정 protocol
- 5분 baseline (eyes-open, fixation, relaxed)
- 5분 baseline (eyes-closed, alpha block) — Berger 검증용
- 1분 blink artifact intentional (eye movement 자극 5초마다)
- ledger: `state/eeg_live_user_16ch/baseline_2026_05_01.bdf` (raw) + `*.jsonl` (분석 결과)

### 3.4 verdict 결정
- end-to-end pipeline PASS → Track B 즉시 진입
- artifact pipeline 16ch 비호환 → fix or workaround → 별도 cycle

---


1. 본 plan 은 sample size N=1 (사용자 본인) 만 다룸 — 통계적 추론 절대 불가, case study 한정.
2. paper §7 의 prior N=1 EEG pilot 은 다른 사람/장비/protocol 일 가능성 — 정확 매칭 검증 필요.
3. r14 LoRA 자체가 r8 가 truncated 였던 후속 swap 결과물 — paper §7 의 prior verdict 가 r14 substrate 와 다를 수 있음.
5. EEG hardware 는 임상 device 아님 (OpenBCI = research grade) — 모든 결과는 research 한정, 의학/진단 용도 아님.
6. 본 plan 자체가 권장만, 실행 X — 사용자 1개 결정 후 별도 agent 발사.
7. 16ch 가 paper §7 의 prior layout 과 호환 안 될 가능성 — Track A 에서 검증.
9. 비용 estimate $0 (로컬 hw) 는 alpha endpoint 호출 (Track C/E) 제외 — endpoint 비용은 별도.
10. Track E (cyborg) 는 가장 실험적 — token-level injection 의 deterministic 보장 어려움.

---

## §5 사용자 결정 점

**Q1**: 어느 트랙으로 시작? — TOP-1 권장 = **Track A (BrainFlow ingest 검증)**

**Q2**: 사용자 측 사전 확인 (§3.1) 필요 — board 종류, BrainFlow 설치, dongle 포트 정보

**Q3**: 측정 시 사용자 본인 시간 가용 — 첫 protocol 만 30-60분, 본인 직접 OpenBCI 착용 + 측정

→ **Q1 만 알려주시면 anima 측 코드 inspect (§3.2) 부터 시작**. 사용자 측정은 §3.3 단계에서 별도 alignment.

---

**status**: ANIMA_EEG_OPENBCI_16CH_TRACK_PLAN_2026_05_01_LOCAL_DRAFT
**verdict_key**: PLAN_READY · USER_DECISION_PENDING · NO_HW_ACTION_YET
