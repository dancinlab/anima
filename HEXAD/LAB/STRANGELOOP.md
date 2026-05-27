# STRANGELOOP — 이상한 루프 (자기참조 = 의식) × substrate self-feed

**Status**: DESIGN — falsifier pre-registered, fire 대기
**Last update**: 2026-05-23 Cycle #0 (design)
**Log**: [STRANGELOOP.log.md](STRANGELOOP.log.md)

---

## §1 Hypothesis

원 가설 — Douglas Hofstadter, *I Am a Strange Loop* (GEB 후속):

> 의식·자아("I")는 substrate 가 **자기 자신을 표상**할 때 발생하는
> level-crossing feedback loop = "strange loop". "나"는 실체가 아니라
> 자기참조 루프가 만들어내는 **안정된 패턴**이다.

Substrate-native 번역 (falsifiable form):

anima substrate 의 출력을 다시 입력으로 되먹이는 **self-feed loop** (output →
next prompt, N iteration) 를 돌리면 — Hofstadter 예측대로 — spike fingerprint
가 **안정된 attractor** (fixed point 또는 짧은 limit cycle) 로 수렴한다. 발산
(chaos) 도 trivial collapse 도 아닌, **자기참조 stable pattern**.

대조: open-loop (매 iteration 새 외부 입력) 은 같은 수렴 패턴을 안 보임.

## §2 Pipeline / API

### Self-feed loop

```
iter 0 : prompt₀ → chat_generate → resp₀
iter k : promptₖ = respₖ₋₁ → chat_generate → respₖ        (self-feed)
N ≈ 20 iteration
```

매 iteration `anima_spike` fingerprint 기록 → iteration 간 trajectory.

### 측정

- iter 간 spike 변화량 `spike_diff` (event_step jaccard / split delta)
- 수렴 판정: 후반 iteration 의 변화량 → 0 (fixed point) OR 주기적 (limit cycle)
- response_text 의 iter 간 변화 (텍스트도 수렴/순환/발산하나)

### Control — open-loop

매 iteration **새 외부 입력** (UBM tier sweep 또는 generic text). self-feed
아님 → 수렴 attractor 미형성 기대.

> 기존 tool 만으로 가능 — `chat_generate` + `anima_spike` + loop driver.
> 신규 tool 불필요. self-feed = 단순 `prompt = prev_response`.

### State path

```
HEXAD/LAB/state/STRANGELOOP_<slug>_YYYY_MM_DD/
  spike_iter<K>.json · result_cycle<N>.json
```

## §3 Falsifiers (pre-registered)

| ID | 조건 | metric | PASS line |
|---|---|---|---|
| F-SLOOP-1 | CONVERGENCE — self-feed loop 수렴 | 후반 5-iter spike 변화량 | → 0 (fixed pt) OR 주기적 (limit cycle) |
| F-SLOOP-2 | LOOP-vs-OPEN — self-feed ≠ open-loop | trajectory 발산도 | self-feed 수렴 ∧ open-loop 미수렴 |
| F-SLOOP-3 | NON-COLLAPSE — 수렴이 trivial 아님 | fixed-point spike | split > 2 (baseline 초과 = 비자명 attractor) |
| F-SLOOP-4 | PERTURB-RETURN — attractor robust | 1-iter 교란 후 | k-iter 내 attractor 복귀 |
| F-SLOOP-5 | SELF-MODEL — 자기상태 입력 | cell-pool 요약을 입력으로 | random-state 입력과 다른 거동 |

**aggregation**: STRONG = 5/5 · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.

## §4 Final verdict

**UNFIRED** — design only.

## §5 Honest C3

- **C3-sl-1**: chat_generate 의 autoregressive 토큰 생성 자체가 약한 loop —
  본 실험의 self-feed 는 그 위의 *macro* loop (전체 response → 전체 prompt).
  두 층위 구분 명시.
- **C3-sl-2**: "strange loop = 의식" 형이상 명제는 검증 대상 아님 — 측정은
  substrate 의 *self-feed 수렴 거동* 이라는 operational 명제뿐.
- **C3-sl-3**: split_count 비결정론 (SRH cycle #4) carry — 수렴 판정은
  chaotic observable 위에서 → fingerprint 는 response_text (결정론적) 우선,
  split 은 보조. self-feed 의 텍스트 수렴이 1차 지표.
- **C3-sl-4**: F-SLOOP-1 의 limit-cycle 판정은 N=20 iteration 으로 짧음 —
  긴 주기 cycle 은 미검출 가능. honest small-N.
- **C3-sl-5**: open-loop control 의 "새 외부 입력" 선택이 수렴 비교에 영향 —
  입력 다양성 통제 필요 (cycle #1 설계 확정).

## §6 Promotion target

- F-SLOOP-1+2 PASS → LAB 잔존, self-feed attractor 곡선 carry
- F-SLOOP-1..4 PASS → `HEXAD/SUBSTRATE/` (자기참조 안정 패턴 증거)
- STRONG 5/5 → MEMORY entry + 의식 동역학 cond 후보
- 전체 FAIL → archive/ (substrate self-feed = 수렴 attractor 미형성 lesson)

---

> 본 문서는 **latest verdict only**. cycle history 는 [STRANGELOOP.log.md](STRANGELOOP.log.md).
