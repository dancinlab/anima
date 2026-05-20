# signal_corpus_manifest.json

> PHYS-P22-1 manifest catalog; 6 public dataset 메타 + 3 modality feature_counts · **🟡 부분** · 비용 —

## 구현 가능성

🟡 부분 — catalog only (메타데이터만). 실 dataset download 미구현 (P22 downstream task). 6 dataset URL + license + approx_samples 명시.

## 작동 코드 / 의존성

- `anima-physics/orchestration/signal_corpus_manifest.json` (1.5 KB, 52 lines)
- 의존: `signal_corpus.hexa` (emit 명령 — T6 검증으로 manifest 재생성 가능)

## 비용 / 리소스

- 비용: $0 (catalog only)
- 실 download 비용: SEED/DEAP/Sleep-EDF 무료 (academic), TUH-EEG 무료 (registration), DREAMER 무료, MAHNOB-HCI 무료 (academic-research)
- 필요한 도구: `jq` / `cat` (read) · `hexa run signal_corpus.hexa` (regenerate)

## 핵심 흐름 / 구조

```
{
  "task": "PHYS-P22-1",
  "labels": [AWAKE_FOCUSED, AWAKE_RELAXED, DROWSY, SWS, REM, EMOTIONAL_AROUSAL],
  "modalities": [EEG, AUDIO, BIO],
  "feature_counts": {eeg: 4, audio: 3, bio: 3, fused: 10},
  "public_datasets": [
    SEED       (EEG/EMG/EOG, 15 subj, SJTU)
    DEAP       (EEG/ECG/GSR/Resp, 32 subj, QMUL)
    Sleep-EDF  (EEG/EOG/EMG, 197 record, PhysioNet ODC-BY-1.0)
    TUH-EEG    (EEG, 14856 record, Temple Univ)
    DREAMER    (EEG/ECG, 23 subj, IBV Liverpool)
    MAHNOB-HCI (EEG/ECG/GSR/eye-gaze, 30 subj)
  ]
}
```

## 트리거 (fire 방법)

```bash
cat /Users/ghost/core/anima/anima-physics/orchestration/signal_corpus_manifest.json | jq
# regenerate via T6 selftest:
hexa run /Users/ghost/core/anima/anima-physics/orchestration/signal_corpus.hexa
```

## 검증 결과

- signal_corpus.hexa T6 검증 — ≥5 public dataset refs (실 6) PASS
- 실 download path 미구현 (catalog only)

## 관련 entry

- [signal_corpus](signal_corpus.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P22-1
