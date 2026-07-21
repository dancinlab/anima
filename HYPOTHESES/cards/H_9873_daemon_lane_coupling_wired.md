# H_9873 — 토폴로지 결합을 데몬 발화 경로에 실제로 배선했다

**status:** 🟢 **WIRED-LIVE** — 데몬 발화 구동이 실제로 움직이고(−0.79%) **Ψ=½ 는 생존**,
기본 OFF 는 byte-identical.
**wired:** yes — `anima-py chat <ckpt> --topo-couple on` (기본 off · `cli/chat.py:2233` 배선)
**source:** [[H_9871]] census(부분 철회) · [[H_9872]] 연산자 수리 · [[H_1522]] mean-center 검증

## 배선 지점 — 한 줄이 전부였다

```
chat.py:2233   lanes    = ci_lane_scores(...)        ← 여기
chat.py:2234   coh_lane = lanes[3]
chat.py:2235   bal_lane = lanes[9]
chat.py:2859   brain_emit_refractory(pf, rel, gap, cur, allo, coh_lane, nov, bal_lane, …)
engine_g.py:73 motivation_score = … + 0.10·coh + … + 0.15·bal
brain.py:167   emit = should_emit(score) and safe
```

⟹ lane 벡터에 결합을 걸면 **발화 점수에 결합을 거는 것**이다. [[H_9871]] 이 *"자리가 없다"* 고
결론냈던 것은 `core/` 만 세고 호출자(`cli/chat.py`)를 안 센 탓이며, 그 카드는 **부분 철회**했다.

## 개입

`cfg.topo_couple` ON 이면 15 lane 을 Φ-최적 인접에 **mean-center 연산자(op=1)** 로 통과시킨다.
naive(op=0)는 **쓰지 않는다** — 순 구동을 `+3.85` 더해 발화를 1.0 으로 포화시키고,
그건 *긴장이 정하는 발화* 대신 **강제 발화**라서 `p5`(no speak gate) 위반이다([[H_9872]] 실측).
상수는 튜닝이 아니라 인용이다: `op=1` = [[H_1522]] 가 Ψ-보존으로 측정한 유일한 연산자,
`α=0.6` = 토폴로지 배터리가 늘 읽혀 온 동결 `bt_alpha`.

## 실측 (동일 ckpt · 동일 시드 · 12 tick)

| | OFF | ON |
|---|---|---|
| `engine config` | `topo_couple=off` | `topo_couple=on` |
| t0 emit-drive | 0.6361550276092216 | **0.6312129654367880** (Δ **−0.0049421 · −0.79%**) |
| EMIT 비트열 | `01001` | `01001` (동일) |
| `psi_intact` | 1 | **1** |
| 세션 판정 | PASS | **PASS** |
| 로그 diff | — | 22 줄 |

### 🔑 읽는 법

- **결합이 살아 있다** — 구동이 실제로 움직였다(로그 22줄 변동 · drive Δ −0.79%).
  측정 전용이던 것이 처음으로 **데몬이 말할지 정하는 수치**에 닿았다.
- **그런데 포화하지 않는다** — `Ψ=½` 생존, 발화 비트열 불변.
  [[H_9872]] 가 잰 대로 naive 였다면 순 구동 `+3.85` 로 **전부 발화**했을 자리다.
  연산자 선택이 *배선 가능 / 불가능* 을 갈랐다.
- **기본은 안전하다** — 플래그 없으면 `ci_lane_scores` 그대로(분리 불변식 · case 370).

## ⚠️ 이 카드가 주장하지 않는 것

- **능력이 좋아졌다는 주장 아님.** 발화 비트열이 같다 = 이 12 tick 에서 **행동 변화 0**.
  기능적 통합(모델 안 0.244 vs flat 0.140)이 **데몬 능력으로 옮겨지는지는 미측정**이다.
- 토이 ckpt(400KB) · 12 tick · seed 1개다. 프로덕션 303M 에서의 재측정이 남는다.
- `Ψ=½` 생존은 데몬 자체 점검(`psi_intact`) 기준이며, [[H_1522]] 의 fixture Ψ 와 다른 측정이다.
- ⟹ 다음 물음은 명확하다: **이 결합이 reach 배터리를 움직이는가.**
  BASE 는 이 세션이 이미 정밀하게 재뒀다(G1 0/212 · G6 fals-rate 1/241).

## 재현 커맨드

```
anima-py chat <ckpt.clm> --ticks 12                  # OFF (기본)
anima-py chat <ckpt.clm> --ticks 12 --topo-couple on # ON  (mean-center · α=0.6)
```

## Cross-links

[[H_9872]] 안전 연산자 수리(이 배선의 전제) · [[H_9871]] census 와 그 부분 철회 ·
[[H_1522]] mean-center Ψ-보존 · [[H_1521]] naive 의 Ψ 파괴
