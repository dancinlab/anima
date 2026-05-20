# signal_corpus.hexa

> PHYS-P22-1 multi-modal signal corpus (EEG/AUDIO/BIO 자동 태깅); 6-label consciousness tagger + 7-test deterministic LCG · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — T1-T7 PASS (synthesizer / tagger ≥0.75 / fusion length / manifest ≥5 ref / determinism). Law 2 "observe never inject" 준수 (label은 측정에서 도출).

## 작동 코드 / 의존성

- `anima-physics/orchestration/signal_corpus.hexa` (24 KB, ~620 LoC)
- 의존: 없음 (deterministic LCG, 외부 dataset 다운로드 안 함 — catalog only)
- emit: `signal_corpus_manifest.json` (P22 downstream task)

## 비용 / 리소스

- 비용: $0 (catalog + synthetic generator only)
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
Modalities:
  EEG   — 256 Hz, 20 s, 5120 samples
  AUDIO — 16 kHz, 5 s, 80000 samples summarized
  BIO   — 1 Hz, 60 s window (HR + HRV + GSR)

6 labels:
  0 AWAKE_FOCUSED
  1 AWAKE_RELAXED
  2 DROWSY
  3 SWS
  4 REM
  5 EMOTIONAL_AROUSAL

Pipeline:
  1. Synthetic generator per modality × per label (deterministic LCG)
  2. Feature extractors (EEG band power / AUDIO envelope / BIO HR+HRV+GSR)
  3. Label auto-tagger (observes features, picks label)
  4. Multi-modal fusion (concatenated feature vector len=10)
  5. Dataset assembler (N per label, shuffled deterministically)
  6. Manifest emitter (signal_corpus_manifest.json, 6 public dataset refs)

Public catalog: SEED, DEAP, Sleep-EDF, TUH-EEG, DREAMER, MAHNOB-HCI
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/signal_corpus.hexa
```

## 검증 결과

- T1 EEG synth 6 distinct label signatures PASS
- T2 AUDIO focused vs emotional arousal distinguishable PASS
- T3 BIO SWS (low HR) vs AWAKE (normal) distinguishable PASS
- T4 Auto-tagger accuracy ≥ 0.75 on 60-sample mix PASS
- T5 Fusion feature vector len = Σ per-modality counts = 10 PASS
- T6 Manifest JSON contains ≥ 5 public dataset refs (실 6) PASS
- T7 Determinism — same seed → identical labels PASS
- **7/7 PASS**

## 관련 entry

- [manifest](manifest.md)
- [rtc_sync](rtc_sync.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P22-1
