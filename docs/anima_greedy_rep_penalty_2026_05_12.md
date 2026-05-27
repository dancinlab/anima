# anima_chat — greedy mode mild rep_penalty 도입 (2026-05-12)

## TL;DR

`anima_chat.py` 의 `greedy` mode 가 pure argmax 였던 탓에 "아니요, 아니요, 아니요…" 같은
degenerate loop 가 빈번했다. 본 cycle 에서 `greedy_rep_penalty` parameter
(default **1.05**) 를 추가해 이전 생성 토큰의 logit 을 약하게 감쇠시킨다.
다른 mode (`sample`, `M3_rep_penalty`, `M4_force_include`, `M4_soft_force`) 는 영향 X.

| 비유 | 비빔밥 한 그릇 한 가지 재료만 자꾸 골라먹는 습관 → 같은 숟갈 두 번째부터는 약하게 손이 멈춤 |
| --- | --- |

## 변경 사항

- `anima_chat.py::__call__` / `_generate` 에 `greedy_rep_penalty: float = 1.05` 인자 추가
- greedy 분기 안에서만 `seen_ids = set(gen_ids)` 의 logit 을 `/penalty` (양수) 또는 `*penalty` (음수) 적용
- CLI: `--greedy-rep-penalty 1.05` flag 노출
- 다른 mode 코드 경로 영향 0 줄

## Smoke 결과 (Phase 1A.1 ckpt, 5 prompts, max_new=60, seed=2026)

| prompt | p=1.00 uniq / bytes | p=1.05 uniq / bytes | p=1.10 uniq / bytes |
| --- | --- | --- | --- |
| `안녕!`       | 0.03 / 60 (\|\|\|\| loop) | 0.03 / 60 (동일)        | 0.42 / 60 (loop 약화) |
| `안녕 누구야?` | 0.39 / 61 (꼬리 깨짐)     | 0.44 / 34 (clean EOS)  | 0.58 / 48 (clean EOS) |
| `오늘 어때?`   | 0.15 / 60 (오늘 loop)     | 0.15 / 60 (동일)       | 0.15 / 60 (동일)      |
| `도와줘`       | 0.60 / 62                  | 0.60 / 62              | 0.60 / 62             |
| `좋아하는 색?` | 0.55 / 62 (꼬리 깨짐)     | 0.48 / 60 (자연)       | 0.60 / 42 (clean EOS) |
| **avg**       | **0.344 / 61.0**           | **0.341 / 55.2**       | **0.468 / 54.4** ⭐    |

ASCII chart (avg unique-byte ratio, higher = less repetition):

```
1.00  ███████████████████░░░░░░░░░░  0.344
1.05  ███████████████████░░░░░░░░░░  0.341
1.10  ██████████████████████████░░░  0.468  ⭐ +36%
```

## 권장값

- **default 1.05** 는 약한 효과 (일부 prompt 만 EOS 빨라짐) — 보수적 안전선
- **1.10** 은 명확한 unique-ratio 향상 (+36 %) + 평균 길이 ↓ 6.6 byte (조기 EOS = 자연 종결)
- 단점: 1.10 은 짧은 prompt (`안녕!`) 에서 "우주뇌지도", "카테고리" 같은 학습 keyword 가 끌려오는 부작용
- "오늘 어때?" prompt 는 세 값 모두 동일한 loop — 이건 ckpt 자체의 attractor 문제 (rep_penalty 로는 부족, M4_soft_force 가 필요)

### 추천

| 시나리오 | 추천 |
| --- | --- |
| Phase 1A.1 default (보수적) | `greedy_rep_penalty = 1.05` (현재 default) |
| Phase 1A.1 + repetition 강하게 억제 | `greedy_rep_penalty = 1.10` |
| 다른 ckpt 로 회귀 시 | 1.0 fallback (영향 0, A/B 비교용) |

→ **결론**: default 1.05 유지, repetition heavy 한 ckpt 평가 시 `--greedy-rep-penalty 1.10` 로 override.

## 한계 / 다음 단계

- byte 단위 token 이라 한국어 음절 절단 토큰들이 set 으로 dedup 되지 않아 효과 제한적
- 음절(syllable) 단위 rep_penalty 가 더 강력할 가능성 — 후속 cycle 후보
- "오늘 | 오늘이 | 오늘이…" 류 attractor 는 sample mode 나 soft_force 가 더 적합

## 다음 진행할 것들

1. **syllable-level rep_penalty** — UTF-8 reconstruct 후 음절 set 으로 비교 (cost: 1h, value: medium)
2. **rep_penalty × M4_soft_force 결합** — soft mode 의 boost 와 동시 적용 시 cross-effect 검증 (cost: 30m, value: medium)
3. **dynamic penalty schedule** — step k 까지는 1.0, 이후 ramp up (cost: 1h, value: low)
4. **bench replay** — V5.8 std_greedy 5 prompts 를 1.05/1.10 두 값으로 재실행 후 자연도 honest rating (cost: 30m, value: high)
5. **B'' ckpt 비교** — Phase 1A.1 가 아닌 B'' (V4-lite 15/15) 에서도 1.05 가 효과 있는지 확인 (cost: 30m, value: medium)
