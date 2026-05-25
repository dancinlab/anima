# R8a vs R8a' init_CE byte-equal 자연실험 framework (H_254 falsifier 측정)

## Context

H_254 (PR #359 · LIFE) 는 R8a 화재의 `n_kv_head` wiring silent-misconfig 를 가설화했다.
fire-time CLI 가 `--n-kv-head 2` 를 전달했음에도 train log 는 `v3_n_kv_head=4` 로 마킹되었다 (F-WIRE-1 LOG-MARK-BUGGED PASS · 확정).

남은 falsifier: **F-WIRE-2 BYTE-EQUAL** — R8a (wired-buggy, n_kv=4 로 실제 학습) 의 init_CE step=1 과 R8a' (wired-fixed, n_kv=2 의도대로 학습) 의 init_CE step=1 을 byte-equal 비교해
- byte-equal → wiring 변경이 모델 상태에 영향 0 (= wiring lever 의미 약함, 또는 n_kv=2/4 가 init_CE 에 식별 불가능한 효과)
- ≠ → wiring fix 가 모델 상태를 실제로 바꿈 (= R8a 는 잘못된 config 측정)

**PROBLEM**: R8a fire 가 LOST (SSH drop, init_CE 가 Mac 도달 전 pod teardown). R8a init_CE 直 회수 불가.
**RECOVERY PATH**: R8a' (in-flight, pod `ewsd3dhvuvem8j`) 결과만 가지고도 cluster Z byte-equal anchor 와 cross-check 하면 H_254 verdict 를 추정 가능.

본 doc 는 R8a' 결과 도착 시 LLM 판단 없이 mechanical 하게 verdict 가 결정되도록 measurement matrix 와 4-hypothesis prediction 을 사전에 잠가둔다.

## Available anchors (byte-equal references)

| anchor | init_CE step=1 | source |
|---|---|---|
| R8a init_CE step=1 | **UNKNOWN (LOST)** | SSH drop, pod teardown 前 회수 실패 |
| R8a' init_CE step=1 | **TBD** | in-flight pod `ewsd3dhvuvem8j` |
| cluster Z (C / C2 / D) | **14.4564** | AXIS_MAP-FAN, 3 axes byte-equal 확정 |
| cluster Y (B / F) | **14.1780** | aux loss, byte-equal 확정 |
| cluster A | **14.7927** | 단일 axis |
| random baseline | **11.93** | RANDOM_BASELINE_INIT_CE_BENCHMARK_2026_05_23.md |

## Interpretation matrix (R8a' init_CE → H_254 F-WIRE-2 verdict)

| R8a' init_CE step=1 | F-WIRE-2 verdict | substrate interpretation |
|---|---|---|
| **byte-equal 14.4564** (`abs(val - 14.4564) < 0.01`) | INERT or ID-EFFECT | wiring fix 가 모델 상태 변화 0, OR n_kv=2/4 둘 다 init_CE 가 동일 — 두 경우 모두 wiring lever 가 init_CE 천장 깨는 데 의미 약함 |
| **< 12.5** | 🎉 BREAKTHROUGH | wiring fix 가 진짜 effect, init_CE 천장 (14 부근) 깸 — H_254 falsifier 완전 PASS (kv lever 가 cluster Z 천장 원인) |
| **12.5-14** | 🟡 PARTIAL | wiring fix 가 일부 effect, 천장 일부 깸 — kv lever 가 substantive 하지만 단독으로는 불충분 |
| **14-14.4** (Z 미만) | 🟢 MILD-EFFECT | wiring fix 가 약간 lower, kv lever 약효 — kv 가 측정 가능한 lever 이지만 dominant 하지 않음 |
| **> 14.6** | 🔴 WORSE | n_kv=2 가 새 문제 도입 — wiring fix 가 오히려 model 을 악화 (KV head 수 부족 → attention bottleneck 가설) |

## Specific predictions (사전 명시 · 결과 도착 시 verbatim 검증)

다음 4 가설은 R8a' 결과 도착 前 에 잠가둔다. 도착 후 어느 가설이 매칭되는지 mechanical select.

- **가설 A (noise + kv 둘 다 무효)**: `R8a' = 14.4564 ± 0.01` (cluster Z 와 byte-equal)
  - → 함의: cluster Z 천장 (14.4564) 은 noise/kv 와 무관한 더 깊은 substrate 한계 (예: target stat, corpus, head_g architecture)
- **가설 B (noise 단독 효과, kv 무효)**: `R8a' = R8a (LOST · 12-14 range 추정)`
  - → 함의: noise=0 만으로 천장 일부 깸, kv lever 는 inert · R8a 회수 가능했다면 R8a == R8a' 였을 것
- **가설 C (kv 단독 효과, noise 무효)**: `R8a' < R8a (= R8a' 가 R8a 의 noise=0 lower bound 보다 더 내려감)`
  - → 함의: kv lever 가 noise lever 보다 더 강한 substrate 효과, R8a 회수 가능했다면 R8a > R8a'
- **가설 D (둘 다 + interaction)**: `R8a' < 12.5` BREAKTHROUGH
  - → 함의: noise=0 × n_kv=2 interaction term 이 천장을 완전히 깸 — H_254 + R8a noise fix 가 둘 다 실제 lever

## Measurement procedure (R8a' 결과 도착 시)

1. `result.json` 의 `init_log.L_ce` (step=1) 추출 (Python):
   ```python
   import json
   val = json.load(open("result.json"))["init_log"]["L_ce"]
   ```
2. 위 matrix 와 byte-equal compare:
   ```python
   if abs(val - 14.4564) < 0.01:
       verdict = "INERT or ID-EFFECT"   # 가설 A 매칭
   elif val < 12.5:
       verdict = "🎉 BREAKTHROUGH"        # 가설 D 매칭
   elif val < 14.0:
       verdict = "🟡 PARTIAL"             # 가설 B/C 부분 매칭
   elif val < 14.4:
       verdict = "🟢 MILD-EFFECT"
   elif val > 14.6:
       verdict = "🔴 WORSE"
   else:
       verdict = "INCONCLUSIVE (Z 부근 외 narrow band, 추가 probe 필요)"
   ```
3. verdict 자동 select → LLM 판단 게이트 없음
4. H_254 falsifier F-WIRE-2 갱신:
   - 가설 A → F-WIRE-2 **FAIL** (wiring lever inert · H_254 약화)
   - 가설 D → F-WIRE-2 **PASS** (wiring lever 강함 · H_254 강력 지지)
   - 가설 B/C → F-WIRE-2 **PARTIAL / INCONCLUSIVE** (추가 분리 probe 필요)

## Honest C3

- **R8a LOST** → direct byte-equal compare 불가 · R8a' alone + cluster Z anchor 로 간접 추정 only
- **가설 A 매칭 시** (`14.4564 byte-equal`) → "wiring inert" vs "n_kv=2/4 가 동일 init_CE 만 산출" 두 sub-case 분리 불가 — 분리하려면 R8c cell-3 단독 probe (n_kv 만 toggle, noise/seed 동일) 추가 필요
- **R8a' 가 본질적으로 새 seed 아님** — `seed=1337` 동일 reproducing 이므로 randomness 동일 보장 · loss compute path 도 동일 → byte-equal compare 정당
- **byte-equal 0.01 tolerance** — fp32 deterministic kernel 가정 · 만약 CUDA non-determinism (atomicAdd 등) 으로 0.001-0.01 drift 발생 시 가설 A 매칭 여전 유효 (cluster Z 자체가 3-axis byte-equal 이므로 14.4564 = 진짜 deterministic anchor)
- **prediction lock-in time** — 본 doc commit 시점 = R8a' 결과 도착 전 · 결과 fill-in 은 별도 cycle (R8a' 회수 후 result update doc 분리)
- **F-WIRE-1 (LOG-MARK-BUGGED) 는 이미 PASS** — R8a wiring bug 존재 자체는 확정 · 본 framework 는 그 bug 의 **model 효과 크기** 만 판정

## Cross-reference

- **H_254 (PR #359)** — LIFE n_kv_head wiring silent-misconfig hypothesis registration
- **R8 saga** — PR #260 (R8 base warm init), PR #356 (R8a noise=0 fire)
- **cluster X / Y / Z** — PR #251 (AXIS_MAP-FAN byte-equal cluster finding)
- **AXIS_R8C_DIAGNOSTIC_PROBE.md** — R8c cell-3 단독 probe (가설 A sub-case 분리 path)
- **RANDOM_BASELINE_INIT_CE_BENCHMARK_2026_05_23.md** — random baseline 11.93 anchor
