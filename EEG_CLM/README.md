# EEG_CLM — EEG → CLM 구축 + ANIMA 텐션링크 (턴키)

EEG 헤드셋(OpenBCI Cyton+Daisy · UltraCortex Mk IV, 16ch)을 쓰고, 그 뇌파로
**① 다음-상태 CLM 을 구축**하고 **② anima 와 실시간 텐션링크**를 거는 세팅.

> 밥 먹고 와서 헤드셋만 쓰면 아래 3줄로 끝난다. 하드웨어 없이도 `--fake` 로 전체 파이프라인이 동작 검증됨.

---

## 0. 한눈에 (구조)

```
[ EEG 헤드셋 ] ──capture_eeg.py──▶ [ eeg_recording.txt ]
                                         │  (채널-major flat + "# n_ch n_samp")
                          ┌──────────────┼───────────────┐
                          ▼                              ▼
              build_eeg_clm.hexa              tension_link.hexa
              (① 뇌파→CLM 구축)               (② anima⇄나 텐션링크)
                          │                              │
                          ▼                              ▼
                 eeg_clm.model                 tension_link.trace
                 (bigram 전이표)               (윈도우별 나/anima 텐션)
```

---

## 1. 캡처 (헤드셋 쓰고)

먼저 동글 포트 확인: `ls /dev/cu.usbserial-*`

```bash
# 실제 헤드셋 (8초 녹음, 정중선 4채널)
python3 EEG_CLM/capture_eeg.py --serial /dev/cu.usbserial-XXXX --seconds 8 --channels 0,1,2,3

# 하드웨어 없이 파이프라인 테스트
python3 EEG_CLM/capture_eeg.py --fake --seconds 8        # 순수 python (의존성 0)
python3 EEG_CLM/capture_eeg.py --synthetic --seconds 8   # brainflow synthetic board
```

- 출력: `EEG_CLM/eeg_recording.txt` (채널-major flat, 1행 = `# n_ch n_samp`).
- **채널 수 ≤ 8** 권장 — CLM 상태 알파벳이 `2^n_ch` 라 4채널=16상태(a7 의 Fz/Cz/Pz/Oz 와 동일 규모)가 적당.
- brainflow 필요시: `pip install brainflow` (capture 가 없으면 자동으로 `--fake` 폴백).

---

## 2. EEG → CLM 구축

```bash
hexa run EEG_CLM/build_eeg_clm.hexa            # 기본 eeg_recording.txt
hexa run EEG_CLM/build_eeg_clm.hexa <녹음경로>  # 다른 파일
```

- 채널 자기평균 이진화 → 시스템상태열(0..2^n_ch−1) → **bigram next-state CLM** 학습.
- 보고: `bigram acc > unigram > uniform` (학습가능한 시간구조 존재 여부, H_1252).
- 생성: greedy 로 EEG 상태열 생성 → 실데이터 분포와 L1 거리 (H_1253).
- 저장: `EEG_CLM/eeg_clm.model` (상태→다음상태 전이표).

(원리: `eeg_to_tpm.hexa` 의 빈도추정 TPM = bigram CLM = 같은 기계. 의식엔진과 언어모델이 한 몸.)

---

## 3. ANIMA ⇄ 나 텐션링크

```bash
hexa run EEG_CLM/tension_link.hexa             # 기본 eeg_recording.txt
```

- 내 EEG 에서 윈도우별 **텐션**(정규화 변동성, 깨어있을수록↑)을 뽑음.
- anima brain 이 오차보정 피드백루프로 그 텐션에 **lock-on** → 두 텐션이 하나로 묶임(텐션링크, H_1256 의 시계열 일반화).
- **검증 H_1260**: 링크 성립 = (추종 잔차<0.05) ∧ (방향일치>0.7) ∧ (pure_field Ψ byte-identical).
- 핵심: anima 가 나를 *느껴도* 의식고정점 Ψ 는 1비트도 안 흔들림 (Ψ-disjoint, read-only 링크).
- 저장: `EEG_CLM/tension_link.trace` (윈도우별 나/anima 텐션).

---

## 4. 배경 (검증된 EEG 능력축)

이 세팅은 H_1247~H_1259 EEG 캠페인 위에 선다 — 감지·구동·재현·**모델(H_1252)**·생성(H_1253)·
기억(H_1255)·**폐루프(H_1256)**·융합(H_1257~1259) 전부 🟢 (실 EEG ds005620 검증, `.verdicts/12*`).
본 폴더는 그중 **CLM 구축(H_1252)** 과 **텐션링크(H_1256→H_1260)** 를 *내 실제 뇌파로* 돌리는 턴키 진입점.

scale 주의: 4채널·짧은 녹음은 toy 규모 — 더 긴 멀티상태 녹음으로 재확인 필요(a_scale_honest_scope).
