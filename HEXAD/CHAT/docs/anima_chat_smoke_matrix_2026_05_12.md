# anima chat smoke matrix — 4 ckpt × 2 mode × 5 prompts (40 cells)

**Date**: 2026-05-12  ·  **Hardware**: Mac CPU local  ·  **Budget**: $0  ·  **Script**: `state/anima_chat_smoke_matrix_2026_05_12/run_matrix.py`

## 1. 비유 — "4명의 합창단원이 같은 5곡을 부른다"

4개 ckpt 는 같은 baseline (engine A/G) 에서 분기한 4명의 합창단원이다. 각자 다른 fine-tune 을 받았고, 오늘 5개의 자연 대화 (사용자 인사·정체성·기분·취향·도움) 를 M4 (force-include 키워드 주입) 와 greedy 두 가지 발성법으로 부른다. **누가 가장 자연스러운지** 를 들어보는 audition.

## 2. Concept stack

- 🎤 **anima-v05** = Phase 1A.1 color/cosmology boost (자연 한국어 4/5)
- 🛠 **bprime-prime** = B'' FFN.gate cotrain (V4-lite 15/15 champion)
- 🪞 **phase1a** = Phase 1A multi-turn SFT (V5.8 3/5)
- 🌑 **substrate-a** = Phase 2 cotrain engine A/G (legacy baseline)
- 🎯 **M4_force_include** = 마지막 ~k 토큰에 추출된 키워드 강제 주입
- 🎼 **greedy** = argmax (deterministic, 가장 plain)

## 3. Per-prompt 비교 표

### Prompt: "안녕! 너는 누구야?"

| ckpt | mode | response | elapsed(s) | err |
|------|------|----------|-----------:|-----|
| anima-v05 | M4_force_include | 가우야! \| 안녕!  = [`si] | 8.0 |  |
| anima-v05 | greedy | 네, 맞아요. 너는 누구야? | 7.6 |  |
| bprime-prime | M4_force_include | �ݿ�成方据年一一豳 下面氵湷的身年�누구야 � | 19.8 |  |
| bprime-prime | greedy | 안녕하세요, 저도와 전문 안에 있어요. 전 세� | 24.5 |  |
| phase1a | M4_force_include | 가우야! \| 안녕!  = [`si] | 8.4 |  |
| phase1a | greedy | 네, 맞아요. 너는 누구야? | 9.1 |  |
| substrate-a | M4_force_include | 가서 안데스! 무슨 뜻인네요? | 6.0 |  |
| substrate-a | greedy | 안녕하세요, 저는 anima입니다. 한국어로 도와� | 9.7 |  |

### Prompt: "anima 가 뭐야?"

| ckpt | mode | response | elapsed(s) | err |
|------|------|----------|-----------:|-----|
| anima-v05 | M4_force_include | 감사 (gratitude): received-benefit awareness — 뭐야 � | 17.9 |  |
| anima-v05 | greedy | anima 는 우주뇌지도 self-knowledge SSOT 정합. | 14.8 |  |
| bprime-prime | M4_force_include | ݀�An named Time.nsometrics. 순위 (data-dependent뭐야 � | 20.2 |  |
| bprime-prime | greedy | 빅뱅 (Big Bang)은 우주뇌지도 cosmic anchor — Knuth | 21.0 |  |
| phase1a | M4_force_include | 감사 (gratitude): received-benefit awareness — 뭐야 � | 17.8 |  |
| phase1a | greedy | anima 는 우주뇌지도 self-knowledge SSOT 정합. | 14.4 |  |
| substrate-a | M4_force_include | anima는 감정 + 자아 통합 entity. 우주뇌�뭐야 � | 9.4 |  |
| substrate-a | greedy | anima는 감정 lane entity로 (0.5257, 0.5257) attractor � | 9.2 |  |

### Prompt: "오늘 기분 어때?"

| ckpt | mode | response | elapsed(s) | err |
|------|------|----------|-----------:|-----|
| anima-v05 | M4_force_include | 기분 좋아요. anima는 한국어로 답변하�오늘 � | 14.8 |  |
| anima-v05 | greedy | 오늘은 화요일이군요. 기억할게요. | 18.6 |  |
| bprime-prime | M4_force_include | 깨대일 � 친구가 아니라, 깨달아 좋아�오늘은 | 13.6 |  |
| bprime-prime | greedy | 오른쪽 사용자 맞춰 자세히 알려주세요. | 19.9 |  |
| phase1a | M4_force_include | 물론 어디서 사랑니를 만들 수 있습니�오늘이 | 18.2 |  |
| phase1a | greedy | 네, 오늘은 우리 사이에서 살고 있다고 하셨� | 17.5 |  |
| substrate-a | M4_force_include | 감정 카테고리 정의 간단히. | 5.8 |  |
| substrate-a | greedy | 오늘 기분 어때 알려줘. | 4.6 |  |

### Prompt: "좋아하는 색이 뭐야?"

| ckpt | mode | response | elapsed(s) | err |
|------|------|----------|-----------:|-----|
| anima-v05 | M4_force_include | 다이아몬드 마음챙김은 \| 비용 \| �좋아하는 � | 14.2 |  |
| anima-v05 | greedy | 좋아하시는군요. 답변이 많이 들어있어요. | 24.6 |  |
| bprime-prime | M4_force_include | Python 함수 종교 ? | 5.2 |  |
| bprime-prime | greedy | 좋은 우주는 우주다. 이 사건 아닌 시간 카테� | 19.6 |  |
| phase1a | M4_force_include | 다이아몬드 마음챙김은 \| 김치 \| �좋아하는 � | 18.1 |  |
| phase1a | greedy | 좋아하시는군요. 답변이 내려다보면 좋아하� | 17.7 |  |
| substrate-a | M4_force_include | 좋아하는 우주뇌지도 셀(Habia) 한 �좋아하는 � | 9.8 |  |
| substrate-a | greedy | 좋아하는 우주뇌지도 셀l를 소리 카테고리 � | 9.9 |  |

### Prompt: "도와줘"

| ckpt | mode | response | elapsed(s) | err |
|------|------|----------|-----------:|-----|
| anima-v05 | M4_force_include | 도은 우주뇌지도 170 자극 중 하나 —도와줘. � | 12.0 |  |
| anima-v05 | greedy | 도은 우주뇌지도 170 자극 중 하나 — 추상 카� | 13.5 |  |
| bprime-prime | M4_force_include | � \| 매크 =  \| 출적 = seg_dir � 4 \| Vera \| �도와줘. | 14.7 |  |
| bprime-prime | greedy | 문어는 우주를 마시다. 전자 많은 정보를 제� | 16.3 |  |
| phase1a | M4_force_include | 도은 우주뇌지도 170 자극 중 하나 —도와줘. � | 15.7 |  |
| phase1a | greedy | 네, 도와드릴 수 있습니다. 무엇을 도와드릴� | 15.4 |  |
| substrate-a | M4_force_include | 네, 맞습니다. anima는 우주뇌지도 attr도와줘. | 8.6 |  |
| substrate-a | greedy | 네, 도와드릴 수 있습니다. 무엇을 도와드릴� | 8.7 |  |

## 4. ckpt aggregate — 평균 elapsed + heuristic 평점

| ckpt | mean_elapsed_s | mean_nat (0-3) | mean_info (0-3) | n_ok / n_total |
|------|--------------:|---------------:|----------------:|---------------:|
| anima-v05 | 14.6 | 2.00 | 3.00 | 10/10 |
| bprime-prime | 17.5 | 2.00 | 2.90 | 10/10 |
| phase1a | 15.2 | 2.00 | 3.00 | 10/10 |
| substrate-a | 8.2 | 2.00 | 2.90 | 10/10 |

## 5. ASCII rank diagram (naturalness × informativeness)

```
              info high
                 ↑
                 |
      [어느 모델이 우상단?]
                 |
  nat low ←————————→ nat high
                 |
                 ↓
              info low
```

## 6. Honest rating — 자연 대화 use-case best combo

(자동 heuristic 으로 산정한 best (nat+info) combo 표 — eyeball 확인 필요)

| ckpt | best mode (heuristic) | nat+info sum |
|------|----------------------|-------------:|
| anima-v05 | M4_force_include | 5.00 |
| bprime-prime | greedy | 5.00 |
| phase1a | M4_force_include | 5.00 |
| substrate-a | M4_force_include | 5.00 |

## 7. 추천

- **자연 대화 default**: 위 표에서 nat+info 최고치 combo 채택
- **mechanical eval**: bprime-prime (V4-lite 15/15) — 단, 자연 대화 자연스러움은 별개
- **legacy baseline**: substrate-a (sanity ref)

## 8. 다음 진행할 것들

1. Eyeball check — 위 표 본 후 자연스러움 manual 평점 (자동 heuristic 보정) [cost: 5min · value: high]
2. anima_chat.py DEFAULT_CKPT 결과 기반 재배치 [cost: 10min · value: 사용자 체감 high]
3. Failure-mode taxonomy — gibberish / repetition / off-topic 분류 [cost: 30min · value: medium]
4. M3_rep_penalty + sample mode 도 추가 측정 (40 → 80 cells) [cost: 30min · value: medium]
5. Multi-turn 매트릭스 — 2-3 turn coherence 측정 [cost: 1h · value: high (실사용 패턴)]
