# H_9838 — 해마 CA3 의 다단계 전이완성 — A→B, B→C 로부터 A→C (R12-1 · 🥇)

**status:** 🟢 계기 CERTIFIED · 전이 TRANSITIVE (읽기측 · **DIRECTIONAL** — 토이 세계, 학습 투입 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** yes(읽기측) — `anima-py evaluate --hippo-transitive-selftest` 로 착륙(cli/evaluate.py · VERSION 0.20.100).
학습측(`train --hippo-aux`)은 **여전히 미구현**이며 아래 §정직 범위에 이유를 적었다.

## 실측 전제 (카드 갱신 전 `origin/main` 에서 직접 읽음 · 검증됨)

`core/hippo_lane.py`(133줄 · H_9129 rung-3)는 실재한다 — ✅ 전제 유지.
`dg_decorrelate`(center_zscore) → `hippo_kwta`(치아이랑 kWTA 희소부호화) → `dg_codes` →
`hippo_build_store`(CA3 이질연합 W = Σ outer(code[nxt], code[cur])) → `hippo_relatedness`
(다단계 패턴완성). `fixture_codes` / `_fixture_report` 도 실재. numpy 순수 산술 · torch/FFI/ckpt 없음.

⚠️ **소정정 2건(내가 직접 확인한 것):**
1. `ARCHITECTURE.json` 은 **개행으로 끝나지 않는다** — `json.dumps(d, ensure_ascii=False, indent=2)` 를
   개행 **없이** 써야 byte-identical 왕복이다(개행을 붙이면 1바이트 잡음이 낀다).
2. `hippo_relatedness` 는 방문한 모든 상태의 **MAX overlap** 을 돌려준다 ⟹ 이 계기의 DV 는
   **도달가능성 판별**이지 **홉-거리 식별**이 아니다. 카드가 원래 암시하던 "몇 홉인지 맞힌다" 는 이 함수로 못 잰다.

## 배선 (착륙한 플래그)

```
anima-py evaluate --hippo-transitive-selftest \
    [--hippo-hops H] [--hippo-kwta-k K] [--hippo-seed S] \
    [--hippo-dim D] [--hippo-active A] [--hippo-chains C] [--hippo-chain-len L] [--out J]
```

ckpt 불요(`--retr-probe-selftest` H_9825 선례와 동형 · flag PRESENCE 로 디스패치) · GPU 불요 · **1.4초 · $0**.

**세계:** N개 **서로소 사슬** × `chain_len` 항목, **인접 간선만** 저장 ⟹ hops≥2 쌍은 저장소가 한 번도
듣지 못한 관계. **DV:** 참 h-홉 표적을 *다른 사슬의 모든 항목*(구성상 도달불가) 풀에서 top-1 로 집는가.
동률은 `1/t` 로 명시 처리하여, 아무 말도 못 하는 저장소가 정확히 **유도된 우연 `1/pool`** 을 읽게 했다
(`chance-level-must-be-derived-per-metric` — 우연을 가정하지 않고 realized 풀에서 유도).

## 재현 명령 (그대로 복사)

```bash
python3 -m venv /tmp/venv_h9838
/tmp/venv_h9838/bin/pip install -q --force-reinstall --no-deps .
/tmp/venv_h9838/bin/pip install -q numpy
/tmp/venv_h9838/bin/anima-py evaluate --hippo-transitive-selftest --out /tmp/h9838.json
```

## 실측 출력 (2026-07-21 · verbatim · exit 0)

```
=== --hippo-transitive-selftest — H_9838 CA3 multi-step completion (core/hippo_lane.py, H_9129 rung-3) ===
  premise world: N disjoint chains x 4 items, ONLY adjacent edges stored — every hops>=2 pair is a relation the store was never told.
  seeds=[7, 11, 20260721] · geometries(dim,active)=[(256, 8), (128, 8), (256, 16)] · robust=True · READ-SIDE ONLY (no write path into the emit-drive lane)
  ① CERTIFICATION LADDER — the treatment is read at the LARGEST certifying load; the load is picked by the CONTROL arms, never by the treatment number.
    items  edges  pool   chance  | STORED hops=1 (min)    | SHUFFLED store (max)     | status
    8      6      5      0.2000  | 1.0000  bar>=0.90 PASS | 0.5000  bar<=0.8000 PASS | CERTIFIED
    16     12     13     0.0769  | 1.0000  bar>=0.90 PASS | 0.2067  bar<=0.3077 PASS | CERTIFIED
    32     24     29     0.0345  | 0.8750  bar>=0.90 FAIL | 0.1250  bar<=0.1500 PASS | INSTRUMENT-DEAD
  → controls: CERTIFIED — reading the treatment at 16 items / 12 edges (chance=0.0769, floor bar >0.1538)
    TRANSITIVE hops=2 (never stored)             min=0.9375 max=1.0000  [③ TREATMENT] → TRANSITIVE
      ONE-STEP completion (target unreachable)   max=0.1538            [④a chaining lesion · Δ=+0.7837 · causal=True]
      kWTA OFF k=full width (no separation)      max=0.8750            [④b separation lesion · Δ=+0.0625 · causal=False]
    TRANSITIVE hops=3 (never stored)             min=0.7500 max=1.0000  [③ TREATMENT] → TRANSITIVE
      ONE-STEP completion (target unreachable)   max=0.2885            [④a chaining lesion · Δ=+0.4615 · causal=False]
      kWTA OFF k=full width (no separation)      max=0.8750            [④b separation lesion · Δ=-0.1250 · causal=False]
```

(전체 JSON = `--out` 산출물. 사다리 3개 부하 × 9개 config × 전 팔이 `ladder[].per_config` 에 박제된다.)

## 통제 (동결 순서 · 이 순서를 어기면 처치 행을 아예 인쇄하지 않는다)

| # | 팔 | 실측 | 판정 |
|---|---|---|---|
| ① | **양성통제** STORED hops=1 (실제로 쓴 쌍) | 판정부하 min **1.0000** (bar ≥0.90) | PASS |
| ② | **참값0 받침대** 값-셔플 저장소(간선수·부호 다중집합 동일, 표적만 재배정) | max **0.2067** (bar ≤0.3077) | PASS |
| ③ | 처치 hops=2 / hops=3 (한 번도 저장 안 된 쌍) | min **0.9375** / **0.7500** (floor bar >0.1538) | **TRANSITIVE** |
| ④a | 사슬절제 = 같은 질의를 completion **1 스텝**으로 절단(표적 구성상 도달불가) | max **0.1538** / 0.2885 | Δ=**+0.7837** / +0.4615 |
| ④b | 분리절제 = kWTA 무력화(k=전폭) | max **0.8750** / 0.8750 | Δ=+0.0625 / **−0.1250** |

## 읽기

1. **답은 예다.** A→B, B→C 만 저장한 상태에서 **A→C 가 우연(0.0769)의 12배**로 복원된다(0.9375).
   3홉도 0.7500. CE 가 구조적으로 못 주는 연산을, 이 저장소는 학습 없이 산술로 준다.
2. **원인은 연쇄다, 기하가 아니다.** completion 을 1 스텝으로 자르면(표적이 구성상 도달불가) 0.9375 → 0.1538
   로 floor 바에 정확히 붙는다(hops=2, causal=True). 즉 부호 기하의 우연한 유사도가 아니라 **다단계 완성**이 원인.
3. 🔻 **카드 예측의 절반은 반증됐다.** kWTA 무력화가 **붕괴시키지 않는다** — 판정부하에서 0.8750 이고
   3홉에서는 처치 min 보다 **더 높다**(Δ=−0.1250). 카드가 "패턴분리 제거 → 붕괴해야(기전 확증)" 라고 쓴 것은
   이 부하에서 **성립하지 않는다**. 미인증 32항목 부하에서는 kWTA-off 가 0.2708 로 붕괴(처치 min 0.6875)하므로
   "희소 패턴분리는 전이의 **필요조건이 아니라 용량 근처에서만 드는 보험**" 이라는 읽기가 자연스럽지만,
   그 행은 **INSTRUMENT-DEAD 부하에서 나온 수치**라 판정으로 쓸 수 없다(별도 H 필요).
4. 🔑 **용량이 실재한다.** 32항목/24간선에서는 **1홉 양성통제조차** min 0.8750 으로 0.90 바 아래로 떨어진다.
   그 부하에서 전이 수치를 읽었다면 **용량 밖 저장소를 읽은 것**이 된다.

## no-tune-to-green (내 계기의 결함을 내가 신고한 것)

첫 실행은 8사슬×4(32항목) **단일 부하**였고 양성통제 min=0.8750 < 0.90 ⟹ **INSTRUMENT-DEAD** 였다.
여기서 "통과하는 부하로 바꾼다" 는 정확히 tune-to-green 이다(오늘 H_9844 가 블록크기로 같은 함정을 자수했다).
그래서 부하를 **손으로 고르지 않고** 사다리(8/16/32항목)를 전부 돌린 뒤 **양성통제가 아직 서는 가장 큰 부하**
= 가장 불리한 인증점을 코드가 고르게 했다 — 선택은 **통제 팔**이 하고 처치 수치는 선택에 관여하지 않는다.
부하 안에서도 seed 3개 × geometry 3개를 돌려 **양성/처치는 MIN, 받침대는 MAX** 를 헤드라인으로 쓴다.
knob(`--hippo-dim/--hippo-active/--hippo-kwta-k/--hippo-seed/--hippo-chains`)을 명시하면 스윕이 그 config
하나로 접히고 JSON 에 `robust=false` 가 박힌다 — 손으로 고른 config 는 판정이 아니라 프로브다.

exit code: 0=CERTIFIED · 1=INSTRUMENT-DEAD(예: `--hippo-chains 8` 단독 = 실측 rc=1) · 3=INVALID · 2=malformed
(`--hippo-chain-len 1` = 실측 rc=2). 미지 플래그는 기존 `_reject_unknown_flags` 가 그대로 거부한다(실측 확인).

## 정직 범위 / 한계

- **DIRECTIONAL.** 심은 세계 위 저장소 자신의 numpy 산술이다 — CA3 완성이 **할 수 있는 것의 상한**이지
  학습된 303M 이 하는 것이 아니다(`a_toy_scale_recheck`). 토이 GREEN 을 판정으로 승격하지 않는다.
- **DV 는 도달가능성 판별**(위 소정정 2). 홉 거리 식별이 아니다.
- **INVALID 분기는 이번에 걸리지 않았다**(미행사 코드경로). 다만 8항목 부하에서 받침대가 0.5000 을 찍으므로
  그 팔이 큰 값을 낼 수 있다는 것 자체는 보였다.
- **학습 투입은 착륙하지 않았다.** `train --hippo-aux` 가 곧 `a_substrate_disjoint` 를 깨는 **쓰기경로**이며,
  이 selftest 는 **읽기측 전용**이다 — emit-drive(Ψ/motivation/recall_thr/generator) 로 가는 경로를 만들지 않고
  frozen bar 도 건드리지 않는다(LAW: separation = preservation, overlap = conflict).
  이 읽기측 수치가 "옮길 가치가 있다" 고 말했으므로, 학습 팔은 **별도 H 로 분리를 유지한 단방향 배선**으로 설계해야 한다.

**related:** H_9129 · H_9775 · H_9825(selftest 팔 선례) · H_9830 · H_9833 · H_9827 · H_9844(no-tune-to-green 선례)
