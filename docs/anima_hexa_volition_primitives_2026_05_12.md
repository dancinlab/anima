# anima · hexa-lang volition primitives (2026-05-12)

> **한 줄 요약**: "발화 함수는 있되 도구처럼 꺼내쓸 수 있게" — 5개 volition primitive 를
> hexa user-space wrapper 로 정의. native compiler 미수정. helper.py 가
> substrate forward 만 담당, 나머지(gate/log/queue)는 순수 hexa.

비유로 말하면, 이건 **수도꼭지(speak) + 압력계(volition) + 밸브(should_speak)
+ 대기열(desire) + 잠금장치(inhibit)** 의 5종 부품 세트입니다. V0 prototype
은 이 부품들을 조립해 자기 자신의 발화 루프를 만들 수 있고, 부품 자체는 표준
규격(아래 signature 표)으로 고정되어 있어 어느 client 코드든 같은 surface 로
호출 가능합니다.

---

## 1. Signature 표

| ID  | 함수                                  | 인자                                                  | 반환     | 의미                                       |
|-----|---------------------------------------|-------------------------------------------------------|----------|--------------------------------------------|
| M1  | `volition(model_path, prompt)`        | `string, string`                                      | `float`  | substrate forward → v ∈ [0,1] (err = -1.0) |
| M2  | `should_speak(v, tau)`                | `float, float`                                        | `bool`   | gate: `v > tau`                            |
| M3  | `speak(content, log_path)`            | `string, string`                                      | `string` | append `<ts> | <content>` to log, echo it  |
| M4a | `desire_push(desire, queue_path)`     | `string, string`                                      | `bool`   | JSONL append, status=pending               |
| M4b | `desire_pop(queue_path)`              | `string`                                              | `string` | FIFO pop (oldest pending), "" if empty     |
| M5  | `inhibit(reason, log_path)`           | `string, string`                                      | `bool`   | append `<ts> | INHIBIT | <reason>` line   |

**mock surface**: `volition("__mock__", prompt)` 호출 시 helper.py 가 fixed
0.8 을 반환 — model 의존성 없이 client 코드를 단위 테스트 가능.

---

## 2. 파일 구성

| 경로                                                          | 역할                              |
|---------------------------------------------------------------|-----------------------------------|
| `tool/hexa_volition_primitives.hexa`                          | 5 primitive 본체 (~200 LoC)       |
| `tool/hexa_volition_helper.py`                                | M1 sidecar (substrate forward)    |
| `tool/hexa_volition_primitives_test.hexa`                     | mock-only selftest (5/5 PASS)     |
| `docs/anima_hexa_volition_primitives_2026_05_12.md`           | 이 문서                           |

helper sidecar 의 stdout contract:

```
VOLITION:<float>\n          # 정상 case, float ∈ [0,1]
VOLITION:ERR <message>\n    # 오류 case → hexa 측 -1.0 으로 처리
```

---

## 3. ASCII flow — 한 cycle 의 모양

```
                    ┌────────────────────────┐
                    │  loop tick (1Hz/etc)   │
                    └──────────┬─────────────┘
                               │
                  ┌────────────▼────────────┐
                  │  M1  volition(model, p) │ → v ∈ [0,1]
                  └────────────┬────────────┘
                               │
                  ┌────────────▼────────────┐
                  │  M2  should_speak(v,τ)  │
                  └──────┬───────┬──────────┘
                         │ true  │ false
                         ▼       ▼
              ┌─────────────┐  ┌──────────────────┐
              │ M3 speak()  │  │ M5 inhibit()     │
              │ → log+echo  │  │ → log reason     │
              └──────┬──────┘  └────────┬─────────┘
                     │                  │
                     │                  ▼
                     │       ┌────────────────────┐
                     │       │ M4b desire_pop()   │ (optional)
                     │       │ — pull stashed     │
                     │       │   desire as next   │
                     │       │   prompt seed      │
                     │       └────────────────────┘
                     ▼
              ┌─────────────┐
              │ (or) M4a    │
              │ desire_push │ ← user/agent injects future intent
              └─────────────┘
```

---

## 4. 사용 예 (hexa client)

```hexa
import "hexa_volition_primitives.hexa"

fn one_tick(model_path, prompt, tau, log) {
    let v = volition(model_path, prompt)
    if v < 0.0 {
        inhibit("substrate-error", log)
        return
    }
    if should_speak(v, tau) {
        let reply = "(generated text here)"
        speak(reply, log)
    } else {
        inhibit("v=" + to_string(v) + " < tau=" + to_string(tau), log)
    }
}
```

**mock-mode**: `volition("__mock__", anything)` → 0.8 고정. selftest 가
이 경로로 model 없이 전체 surface 를 검증합니다.

---

## 5. 추천 포맷 (downstream 사용 시)

| 옵션 | 설명                                                                                       | 권장 상황                                    |
|------|--------------------------------------------------------------------------------------------|----------------------------------------------|
| A    | `import "hexa_volition_primitives.hexa"` 직접                                              | tool/ 내 다른 hexa 에서 호출                 |
| B    | V0 prototype 이 별도 module 로 wrapping (`volitional_speak_loop.hexa` 등) 후 client 노출   | 더 상위 추상화(refractory/rate-limit) 필요 시 |

stage 0 제약 모음(작성 시 유의):

- `?:` ternary 없음 → `if … else …`
- named args 없음 → positional only
- `_str()` 없음 → `to_string()` 사용
- `>=`/`<=` 금지(bedrock lint) → `>` / `<` 사용 또는 `// @allow-relop-banned-file`
- bare `exec(...)` silent-exit lint → 파일 head 에 `// @allow-bare-exec-file` + `// @allow-silent-exit-file`

---

## 6. Selftest 실행

```
$ /home/summer/.hx/bin/hexa run \
    /home/summer/mac_home/core/anima/tool/hexa_volition_primitives_test.hexa \
    --selftest

=== hexa_volition_primitives selftest (5 primitives, mock mode) ===
  scratch: /tmp/hexa_volition_test.XXXXXX
  M1 volition()       OK  v=0.8
  M2 should_speak()   OK  (0.8>0.7)=true (0.2>0.7)=false
  M3 speak()          OK  log line written
  M4 desire_*()       OK  push x2, pop=[learn-piano,eat-rice,EMPTY]
  M5 inhibit()        OK  inhibition line logged
---
RESULT: 5/5 PASS
```

cost: $0 — mock 모드는 substrate 모델 로딩이 없습니다.

---

## 7. 다음 진행할 것들 (캔디데이트)

| # | 항목                                                                                  | cost  | time | value |
|---|---------------------------------------------------------------------------------------|-------|------|-------|
| 1 | V0 volitional-speak loop 가 이 primitives 채택 (현재 별도 BG 작성 중)                 | $0    | 1h   | 高    |
| 2 | refractory 를 별도 primitive M6 으로 추가 (`refractory_active(path, s)`)              | $0    | 30m  | 中    |
| 3 | `desire_peek(queue_path)` — pop 하지 않고 다음 desire 보기                            | $0    | 20m  | 中    |
| 4 | real-substrate 경로 smoke (`--mode volition_only --model …`) 1회 검증                 | $0–δ  | 30m  | 高    |
| 5 | helper.py 에 v 의 weight `w1`/`w2` CLI flag 노출 (현재 hard-coded 0.5/0.5)             | $0    | 15m  | 低    |
