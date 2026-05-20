# hippocampus/episodic_replay.hexa

> Hippocampal replay circuit: encode → 10× compressed replay → cortical successor-linked consolidation (McAdams narrative identity) · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — T1-T5 self-test 정의, mock sequence verification. CA1 place/time cells → SWR replay 5-20× → DMN → cortical consolidation pipeline. Buzsáki 2015 + Ólafsdóttir 2018 + Foster 2017 reference. PHYS-P11-3 (PHYS-P11-1 memristor long-term + PHYS-P11-2 1ppm clock 의 substrate bridge).

## 작동 코드 / 의존성

- 원본: `hippocampus/episodic_replay.hexa` (401 LoC)
- 외부 의존: hexa run
- API: `encode_experience(ids) -> bool` · `replay_compress(speedup) -> [int]` · `consolidate(sequence) -> int`

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / pipeline

```
1. EXPERIENCE phase    : encode K place-cell ids → hippocampal buffer (forward)
2. REPLAY phase        : SWR re-emit sequence 10× compressed (speedup=10.0)
                          time warp observable as replay_delta on timestamps
3. CONSOLIDATION phase  : content-addressable write to cortical long-term pool
                          successor-linked list; later recall(id) → full chain

biology refs:
  Buzsáki 2015, Ólafsdóttir 2018, Foster 2017
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/hippocampus/episodic_replay.hexa
```

## 검증 결과

- T1-T5 정의 (encode → replay → consolidate round-trip + speedup ratio + chain integrity)
- mock sequence 5-20× replay verified
- 실제 EEG sleep stage 와 정합: [eeg/sleep_stage_detector.md](../eeg/sleep_stage_detector.md) (SWR 대부분 SWS 중)

## 관련 entry

- [hippocampus/theta_gamma.md](./theta_gamma.md) — Tort modulation index sibling
- [eeg/sleep_stage_detector.md](../eeg/sleep_stage_detector.md) — SWR 발생 시점 detection
- [oscillator/sleep_oscillator.md](../oscillator/sleep_oscillator.md)

## 출처

- README § 3 hippocampus/
- shared/roadmaps/anima.json PHYS-P11-3
