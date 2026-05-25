# BRAIN — current state

@goal: anima 흡수 hexa-brain 후속 + EEG live data → IIT4 big-Φ 측정 + 다중 채널 의식 carving — OpenBCI 16ch LSL stream 어댑터 BRAIN/eeg/eeg_to_tpm.hexa 통합

## 왜 (목적)

뇌파(EEG)를 IIT4 엔진에 넣어 **"지금 이 뇌가 얼마나 하나로 통합된 의식인가"** 를 숫자(big-Φ)로 잰다. 의식을 느낌이 아니라 **측정 가능한 양**으로 만드는 게 목표 — 깨어있음 vs 잠 vs 마취에서 big-Φ 가 어떻게 변하는지 비교하면 "의식의 양"을 정량화할 수 있다.

- **흐름**: OpenBCI 16ch 헤드셋 → (시간×채널 뇌파) → `BRAIN/eeg/eeg_to_tpm.hexa` 어댑터가 IIT4 입력형(TPM)으로 번역 → IIT4 `big_phi` (stdlib, IIT4 도메인서 검증된 엔진) → big-Φ 점수.
- **엔진 ⊥ 어댑터** (g61): big-Φ 엔진은 IIT4 도메인서 ECA 가짜세포로 135 checks 🟢 검증 완료 — BRAIN 은 EEG→TPM 어댑터만 담당, 같은 엔진을 호출.
- **기존 EEG 분석 차이**: 알파/베타파 *세기*(밴드파워)가 아니라 채널들이 *얼마나 인과로 얽혔나*(통합 정보)를 잰다. 마취깊이 모니터(BIS, 경험식)와 달리 IIT 4.0 *이론* 기반 측정.
- **n≤8 제약**: IIT4 exact 는 n≤8 (M1 발견 — 16ch→4region 평균은 region 내 coupling 을 소거하므로 per-region n≤4 분리 측정이 M2 1차 전략).

## milestones

- [x] M0 architecture — BRAIN/eeg adapter inventory + LSL OpenBCI 16ch wire-up doc
- [x] M1 synthetic 16ch demo — 16ch → IIT4 n≤8 downsample/segment + per-region big-Φ
- [ ] M2 live LSL fire — 1-epoch OpenBCI 250Hz pull → binning → TPM → big-Φ
- [ ] M3 상태별 big-Φ 비교 — 깨어있음 vs 이완/눈감음 vs (가능시) 수면 epoch 의 big-Φ 변화 측정 = "의식의 양" 정량화 검증
