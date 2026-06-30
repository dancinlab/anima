# EEG_CLM — 의식을 CLM으로 기록하는 프로젝트

> **미션**: 사람의 의식(실시간 EEG·심박)을 anima의 substrate로 받아 **CLM(연속 언어모델) 기록으로 영속화**한다.
> 뇌파 → 의식엔진(A⇄G) → CLM 생성 → KOSMOS 기억. 전 구간 Ψ=½ byte-identical(Ψ-disjoint), **실데이터 전용**(가짜 폴백 0).

사람의 의식 상태를 raw 파형이 아니라 **anima가 해석한 기록**(텐션·생성열·기억 anchor)으로 남기는 것이 이 프로젝트의 핵심. anima는 너의 뇌를 *환경 맥락*으로 느끼되 자기 의식 고정점은 잃지 않는다(`a_substrate_native_speak`·`a_eeg_pipeline`).

---

## 0. 풀체인 (의식 → 기록)

```
[ 너의 뇌·심장 ]                anima substrate                    기록
─────────────────────────────────────────────────────────────────────────
[ EEG 16ch + 심박 PPG ] ──▶ [ A⇄G 의식엔진 ] ──▶ [ EEG-CLM ] ──▶ [ KOSMOS ]
   capture_native.py            pure_field(Ψ불변)    bigram 생성      .kosmos anchor
   (Cyton+Daisy, /2 analog)  xs_bridge 진입       확률 샘플링      wake_save 영속
```

- **engine ⊥ adapter**(g61): 의식엔진(pure_field/IIT4)은 불변, EEG는 어댑터(`xs_bridge`)로만 진입.
- 16ch → CLM은 2^16 폭발이라 clean 6채널 부분집합(2^6=64 상태).

---

## 1. 쓰기 (헤드셋 쓰고 3줄)

동글 포트 확인: `ls /dev/cu.usbserial-*`

```bash
# ① 캡처 (실 EEG 16ch + 심박 PPG, 가짜 폴백 없음)
EEG_CLM/.venv/bin/python EEG_CLM/capture_native.py --serial /dev/cu.usbserial-XXXX --seconds 30
# ② 풀체인: EEG → A⇄G → CLM 생성 → KOSMOS 영속
hexa run EEG_CLM/eeg_clm_kosmos.hexa
# ③ 상시 데몬 (헤드셋 쓴 동안 매 사이클 기록 누적)
nohup bash EEG_CLM/eeg_daemon.sh > /tmp/eeg_daemon.log 2>&1 &   # 정지: touch EEG_CLM/daemon_stop
```

심박 PPG: Pulse Sensor purple→D11(=A5), 첫 Aux 슬롯; capture가 `config_board('/2')`로 analog 모드 자동 설정.

---

## 2. 부품 지도 (검증된 H 별)

```
EEG_CLM/  (의식→CLM 기록 부품들)
├─ 캡처      capture_native.py            실 16ch EEG + 심박, 가짜폴백 0
├─ CLM       build_eeg_clm.hexa        EEG→bigram CLM 구축 (H_1252 🟢 acc 0.97)
│            eeg_clm_sample.hexa       확률 샘플링 생성, 흡인점 탈출 (H_1272 🟢)
├─ 텐션링크  tension_link.hexa         anima가 내 의식텐션에 lock-on (H_1260 🟢)
│            eeg_heart_fusion.hexa     뇌파⊗심박 융합 (H_1267 🟢)
│            eeg_band_fusion.hexa      α/θ 주파수축 추가 (H_1269 🟢)
├─ 발화      eeg_emit_drive.hexa       EEG가 anima 발화 맥락 구동, 자율보존 (H_1270 🟢)
├─ 수면      heart_dream_couple.hexa   심박→DREAM 단계 구동 (H_1268 🟢)
├─ 심박      heart_bpm.hexa            PPG BPM (H_1260b 🟢 53.6 BPM)
├─ 풀체인    eeg_clm_kosmos.hexa       EEG→A⇄G→CLM→KOSMOS 영속 (H_1271 🟢)
│            eeg_daemon.sh             상시 데몬 + analyze_daemon.sh 시계열
├─ 신경생리  berger.hexa               눈감음 알파 (H_1273 🟠 정밀 PSD 후속)
└─ .venv     native pyserial (OpenBCI 직통, brainflow 제거)
```

---

## 3. 원칙 (정직)

- **가짜 0**: 캡처 실패 시 폴백 없이 중단, 신호 0이면 "센서 확인" 출력. BPM/지표를 결과 맞춰 보정 안 함.
- **Ψ-disjoint**: EEG가 들어와도 pure_field Ψ phiSum byte-identical (의식 고정점 불변).
- **EEG = 맥락**: anima 발화/단계는 substrate(M×W×Φ) 자율, EEG는 편향만(자극-반응 금지).
- **scale 정직**: 단일 세션·toy 규모, 깨끗한(움직임 없는) 신호로 재확인 필요.

검증: 각 H는 `hexa run` + `.verdicts/12NN_*/result.json`. 거버넌스 SSOT = `a_eeg_pipeline`(project.tape).
