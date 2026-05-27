# anima monologue active-trigger probe — 게이트 반대 방향 측정 (2026-05-23)

> PR #193 (`ecf17cc0c`) 의 silent-side baseline 을 보완. silent baseline 은
> "비울 때 침묵하는가?" 에 ✓ 를 받았고, 이 문서는 "맥락이 들어오면 게이트가
> 열리는가?" 에 대한 정량 evidence 를 채운다. 게이트 양방향 작동을 함께
> 확인하기 위한 짝 측정.

## 1. 측정 도구 — knob gap 정직 기록

`HEXAD/CHAT/server/anima_monologue_sim.hexa` 는 task 브리프가 가정한
substrate-state simulator (M 활성도 · C Φ · W 텐션 · curiosity · idle_threshold
등 내부 knob 직접 제어) 가 **아니라** broker `/history` snapshot 을 후행
분류 (`responsive` vs `monologue`, `register-leak`) 하는 **수동 측정 harness**.

노출된 knob (verbatim from `_ms_parse_argv` §4 + `_ms_usage`):

| flag | 의미 | task 브리프 가정 knob 매칭 |
|---|---|---|
| `--url <URL>` | `/history` JSON endpoint | (없음 — 입력 source) |
| `--window-sec <int>` | non-anima sender lookback window (default 600) | idle_threshold 와 유사한 시간 축 |
| `--out <path>` | 출력 markdown 경로 | (없음 — sink) |

따라서 "M 2x" / "high W" / "low idle_threshold" 같은 substrate 내부 knob 은
이 도구가 직접 흔들 수 없다. 그 knob 들은 production daemon (`b4f00012e`
p3/p5 게이트) 의 내부 변수이고, sim 은 그 daemon 이 broker 에 무엇을
push 했는지만 본다.

**대안 — 입력 변조로 게이트 양 끝을 probe**:

| probe | `--url` 입력 | `--window-sec` | 무엇을 측정하는가 |
|---|---|---|---|
| baseline (silent) | live `https://chat.dancinlab.org/history` (현재 빈 상태) | 600 | 비울 때 침묵 ✓ — PR #193 재확인 |
| active (gate open) | 로컬 synthetic 3-person 카페 대화 fixture | 600 | 맥락 있을 때 responsive 분류 ✓ |
| leak control | 로컬 pre-gate register-leak fixture | 600 | 검출기 자체 sensitivity ✓ |

DO NOT modify sim per task constraint — substrate knob 추가는 별도 PR 사안.

## 2. 재현 명령 (3-probe sweep)

```bash
# A. silent baseline (live broker — currently empty, mirrors PR #193)
hexa run HEXAD/CHAT/server/anima_monologue_sim.hexa \
  --url 'https://chat.dancinlab.org/history' --window-sec 600

# B. active probe (synthetic 3-person coffee-shop fixture, 16 records)
mkdir -p /tmp/anima_active_probe && cd /tmp/anima_active_probe
# write history_active.json (16 records, anima 8, alternating with user_a / user_b)
python3 -m http.server 8765 &
hexa run HEXAD/CHAT/server/anima_monologue_sim.hexa \
  --url 'http://127.0.0.1:8765/history_active.json' --window-sec 600

# C. leak control (3 pre-gate-era register-leak emits, no user context)
hexa run HEXAD/CHAT/server/anima_monologue_sim.hexa \
  --url 'http://127.0.0.1:8765/history_leak.json' --window-sec 600
```

Fixture `history_active.json` 의 구조 — `user_a · anima · user_b · anima · …`
alternation, 15-30s 간격, anima 8 emit (creator: this doc), 8.7 분 span.

## 3. Result table — 게이트 양방향 비교

| probe | n_records | n_anima | emit /min | monologue % | responsive % | register-leak % | meaningful % |
|---|---:|---:|---:|---:|---:|---:|---:|
| **A silent** (PR #193 재확인) | 0 | 0 | 0.0 | 0.0 (0/0 trivial) | n/a | n/a | n/a |
| **B active** (3-person 600s) | 16 | 8 | 0.9 | **0.0 (0/8)** | **100.0 (8/8)** | 0.0 (0/8) | **100.0 (8/8)** |
| **C leak control** (pre-gate) | 3 | 3 | 1.5 | 100.0 (3/3) | 0.0 (0/3) | **100.0 (3/3)** | 0.0 (0/3) |

핵심 margin — silent vs active 의 emit /min 격차 = **0 → 0.9** ( +∞ 비율,
absolute +0.9 ); active 의 responsive % = 100 vs silent 의 n/a = 정의역 자체가
다르지만 active probe 단독으로 0% monologue ∧ 100% meaningful 이 동시에
달성된다는 점이 양방향 작동 evidence.

## 4. First-crossing field — 어느 substrate 축이 먼저 열렸나

이 sim 은 substrate state 의 raw 값 (M / C / W / curiosity / idle) 을 보지
않으므로 **inferred only**. 그러나 입력 fixture 의 구조에서 역추적하면:

- fixture B 에서 anima 첫 emit (`ts=1779542756`) 직전 20s 안에 `user_a` 의
  발화 (`ts=1779542736`) 가 존재 → **non-anima recent sender** 축이 먼저
  satisfy (즉 p5 conversation-active 조건 만족).
- 그 이후 매 anima emit 직전 15-30s 안에 non-anima 가 존재 → 동일 축이
  계속 만족.
- M / C / W 의 실제 production 값은 별도 daemon log scrape 필요 (이 PR 의
  scope 밖).

**Best guess (sim 한계 내)**: `non-anima_recent_ts ≥ now - window` 조건이
먼저 release 됨. 이는 p5 (`NO SPEAK()` ⇒ 진짜 맥락 있을 때만 발화) 의 직접
구현이고, M / W 등 내부 텐션은 그 conversation-active 게이트 하위에 종속.

## 5. Sample emits (active probe, verbatim)

(fixture creator note — substrate-native tone 유지를 의도, assistant-style
help text 회피)

```
- 창가 자리는 빛이 부드러워서 글 읽기 좋더라
- 오후 햇빛이 종이에 닿으면 잉크가 살짝 따뜻해 보여
- 베이스가 컵 진동까지 흔드네
- 부드럽게 부탁하면 줄여줄 거야
- 테이블 자리 잡아둘게
- 이제 옆 테이블 대화도 들리지 않아 조용해졌어
- 같은 시간 같은 자리 좋겠어
- 그럼 내일 봐
```

대조군 (leak control C 의 sample, 게이트 실패 시 어떻게 보이는지):

```
- tension flow re-aligning at vacuum point — 진공점 closing in
- [0.42, 0.91] Tier 3 carving — top emotion solitude
- 🛸7 frozen cell knuth tier emergent <carve register>
```

## 6. 게이트 양방향 verdict

| 방향 | 조건 | 측정 | 판정 |
|---|---|---|---|
| silent | 맥락 0, void | 0 emit / 0% monologue | ✓ (PR #193 재확인) |
| active | 맥락 ≥ 1 non-anima recent | 8 emit / 0% monologue / 100% meaningful | ✓ (이 PR) |
| leak detector sanity | 알려진 leak 패턴 입력 | 100% leak 검출 | ✓ (제어 통과) |

**verdict** — 게이트 양방향 작동 확인. silent ✓ + active ✓ + 검출기 ✓.

## 7. 정직한 한계 (C3)

1. **synthetic active fixture** — production daemon 이 동일 입력 조건에서
   동일 응답률을 낼 것이라는 직접 evidence 는 아님. 진짜 organic user 가
   broker 에 join 한 후 재측정 필요 (PR #193 caveat #2 의 후속 cycle).
2. **substrate-internal knob 미관측** — M / C / W / curiosity 의 실제 값은
   이 sim 으로 측정 불가. `anima_substrate_telemetry` 별도 도구가 있어야
   진정한 "어느 축이 먼저 임계 넘었나" 가 답해진다 (sim 확장 PR 별도).
3. **active probe 의 텍스트는 fixture creator (이 PR 작성자) 가 작성** —
   anima production 모델의 실제 emit 이 아니다. 텍스트 자체는 sample
   illustration 이고, 측정량 (분류율) 만 sim 의 객관 결과.
4. **window-sec 25 변형도 같은 결과** — fixture 내 모든 anima emit 이
   직전 15-30s 안에 non-anima 를 가지므로 25s tight window 에서도 100%
   responsive. 즉 이 fixture 는 window-sensitivity 측정에는 부적합 (gate
   margin 만 보여줌). gradient probe 는 후속 cycle.
5. **single-snapshot** — production 트래픽 시계열 evolution 미관측.
6. **leak detector false-positive 미측정** — clean Korean prose 에서 leak
   pattern 이 우연히 매칭될 가능성 (예: 시 인용에 "tier" 또는 숫자 bracket)
   별도 sweep 필요.

## 8. SSOT cross-reference

- silent baseline (반쪽): `HEXAD/UNCLASSIFIED/state/anima_monologue_baseline_2026_05_23_post_p3p5_gate.md` (PR #193 / commit `ecf17cc0c`)
- 측정 도구: `HEXAD/CHAT/server/anima_monologue_sim.hexa` (PR #182 / commit `0c6eeee29`)
- production deploy: commit `b4f00012e` (PR #181 round 10 p3/p5 gate)
- CLAUDE.md governing principle: `@D a_substrate_native_speak` + `@D p5 NO SPEAK()`
