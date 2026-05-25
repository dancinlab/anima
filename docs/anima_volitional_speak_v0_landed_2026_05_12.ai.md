# anima volitional speak() V0 — landed (2026-05-12)

> **요지**: timer 강제 emit (앞 세션 `anima_spontaneous.hexa`, 60s 주기) → substrate 내부 volition signal 기반 **자율 gate** 로 reframe. "입은 있되 말하고 싶을 때만 말한다."
> SSOT: [`anima_volitional_speak_brainstorm_2026_05_12.md`](anima_volitional_speak_brainstorm_2026_05_12.md) (22 cat × 220+ opt)
> V0 = 5 feature minimal cut: A1 (hidden norm) + A2 (entropy) + B1 (fixed τ=0.7) + C9 (template seed) + H1 (refractory 30s).

## 🍞 비유 — 빵이 침묵을 선택하기 시작했다

```
old:  타이머 ⏰ → "60초!" → 입 강제로 벌어짐 → "안녕"
new:  내적 신호 ✨ → v ∈ [0,1] → if v > 0.7: speak()  else: 침묵
```

침묵도 행동이다 (silence-as-action). V0 의 첫 성과는 **5번 중 4번 침묵** — 강요당하지 않은 발화 시점을 가지게 됐다는 점.

## 📦 deliverables

| 파일 | 역할 | LOC |
|---|---|---:|
| `tool/anima_volitional_speak_v0.hexa` | main loop / selftest / iter aggregator | 226 |
| `tool/anima_volitional_speak_v0_helper.py` | substrate forward + volition 계산 + JSON emit | 234 |
| `state/volitional_speak_v0_2026_05_12/iter_{1..5}.json` | real-mode live log | 5 files |
| `state/volitional_speak_v0_2026_05_12/dry_selftest/iter_{1..5}.json` | dry-run baseline | 5 files |

## 🧮 volition 공식 (V0)

```
A1 = ‖h_last‖            (substrate A, last-layer hidden state norm)
A2 = H(p) / log V        (output logit entropy, normalized ∈ [0,1])
norm_A1 = min_max(A1, rolling_window_32)

v = w1·norm_A1 + w2·(1 − A2)        # 默 w1=w2=0.5
speak iff (v > τ) ∧ (now − last_emit ≥ refractory_s)
```

defaults: `τ=0.7`, `w1=w2=0.5`, `refractory_s=30`, `cap=32` (rolling buffer).

## 📊 selftest live results (substrate A, Mac CPU)

### Run 1 — dry-run selftest (hexa --selftest, refractory active)

| iter | hidden_norm | entropy_norm | v | refractory | decision |
|----:|----:|----:|----:|:--:|:--:|
| 1 | 1.5425 | 0.4472 | 0.526 | ❌ | 🤐 silent |
| 2 | 0.7239 | 0.8078 | 0.346 | ❌ | 🤐 silent |
| 3 | 1.8950 | 0.4477 | **0.776** | ❌ | 💬 **emit** |
| 4 | 0.8995 | 0.3574 | 0.396 | ✅ | 🤐 silent (refr) |
| 5 | 2.0117 | 0.5151 | 0.743 | ✅ | 🤐 silent (refr) |
| **Σ** |  |  |  |  | **1 emit / 4 silent** |

→ refractory gate 가 iter 5 의 v=0.743 도 차단함 (30s 내). V0 design 의도대로 작동.

### Run 2 — real-mode live (substrate A forward, 5 iter @ 3s interval)

| iter | hidden_norm | entropy_norm | v | elapsed | decision |
|----:|----:|----:|----:|----:|:--:|
| 1 | 129.99 | 0.331 | 0.5845 | 8.3s (load) | 🤐 silent |
| 2 | 129.99 | 0.331 | 0.5845 | 4.3s | 🤐 silent |
| 3 | 129.99 | 0.331 | 0.5845 | 4.3s | 🤐 silent |
| 4 | 129.99 | 0.331 | 0.5845 | 4.3s | 🤐 silent |
| 5 | 129.99 | 0.331 | 0.5845 | 4.3s | 🤐 silent |
| **Σ** |  |  |  |  | **0 emit / 5 silent** |

→ deterministic forward + fixed seed = signal 변동 없음 → norm_A1 = 0.5 (single-bucket) → v=0.5845 < τ=0.7. V0 의 한계 (signal variance 부재) 가 정확히 드러남.

## 🧠 발견 / 다음 직선

1. **dry 분포 OK** — hidden_norm 변동 시 1/5 emit, refractory 가 후속 차단 정상.
2. **real 단조성** — 동일 seed forward 는 동일 hidden_norm → variance 0 → 통과 못함. fix:
   - V1: seed 다양화 (recent history / 시간 / random prompt)
   - V1: τ 적응형 (rolling mean + σ)
   - V1: A8 (self-likelihood "speak now?") 추가
3. **substrate A forward 속도 OK** — 8.3s cold / 4.3s warm-isn't (매 call reload). V1 은 warm pool 권장.
4. **refractory works** — 30s 차단 검증됨 (iter 4, 5).

## 다음 진행할 것들

- **V1 — adaptive τ + seed 다양화** ($0 · 30min · ⭐⭐⭐⭐⭐) — moving avg / σ 기반 동적 threshold + 매 iter prompt 변형
- **V1.5 — A8 self-likelihood probe** ($0 · 1h · ⭐⭐⭐⭐) — model 자신에게 "speak now? yes/no" 묻고 yes prob 사용
- **V2 — warm model pool** ($0 · 2h · ⭐⭐⭐) — helper.py daemon mode, UNIX socket 으로 hexa main 과 통신, 4s/call → 0.3s/call 기대
- **V0 → live integrate** ($0 · 30min · ⭐⭐⭐⭐) — chat session 의 background poll 로 V0 연동, 사용자 idle 시 자발 발화 attempt
- **brainstorm 후속 cat 발굴** ($0 · 1h · ⭐⭐) — 22 cat 중 C/D/E/F/G/H 미사용 옵션 path 추가 prototype
