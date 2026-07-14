# H_9338 — 실험 라벨이 프로덕션 분기 키를 타면 통제군이 조용히 무력해진다

**status**: 🟢 VERDICT (defect confirmed + fixed + fix verified on live 303M)
**tier**: TERMINAL (engine-native · `anima-py chat` canonical path · 실측 trace)
**lane**: instrument / control-integrity
**parent**: H_9328 (DO-MOUTH) · H_9337 (CLOSE-THE-LOOP)

## 주장

> `--swap-text` (C2 CARRIER-SWAP 통제군)은 **아무것도 재지 않았다**. donor 텍스트를
> 주입한 뒤 팔 라벨을 `g_back` 에 붙였는데, 하류 피드백 블록이 바로 그 `g_back` 으로
> 게이트돼 있어서 **SWAP 팔이 모든 피드백 뿌리를 우회**했다.

## 결함 (`cli/chat.py` · pre-fix)

```python
g_back = g_back + "+swap"          # :1930  — 팔 라벨을 backend 필드에 얹음
...
if g_emit and g_back == "clm" and byte_len(g_text) > 0:   # :1939/1949  C8-GROW
    ...                            # afield step · immune bind · pending_recon/pending_rel
```

`g_back` 이 `"clm+swap"` 이 되는 순간 C8-GROW 가 **False** 로 떨어진다.
⇒ SWAP 팔에서 `afield` 는 step 되지 않고 `immune` 은 bind 되지 않는다.
donor 텍스트는 **어느 뿌리에도 닿지 않았다**.

## 실측 (trace-level · 이것이 결정적이었다)

| arm | rollout | `recon_err` 고유값 |
|---|---|---|
| SWAP (pre-fix) | 16/16 | **1** 💀 |
| 같은 바이너리 · 플래그 없음 | — | 5 ✅ |

**같은 바이너리**다. 차이는 플래그 하나. ⇒ 결함은 플래그에 있다.

## ⚠️ 내가 앞서 쓴 문장의 철회

앞선 스모크에서 나는 *"주입 성공 ✅ — donor 텍스트가 실제로 뿌리를 민다"* 고 썼다.
**틀렸다.** 행동축 `A` 가 움직인 건 `g_text` **자체가 바뀌어서**지 뿌리가 밀려서가 아니다.
`A` 는 `g_text` 의 함수이므로 **주입이 무력이어도 A 는 반드시 움직인다** — 그래서 A 를 보는
스모크는 이 결함을 **원리적으로 검출할 수 없다**. 검출한 것은 **뿌리(`recon_err`)를 직접 센
trace-level 검사**뿐이었다.

## 수정

팔 라벨을 **자기 필드**로 옮긴다. `g_back` 은 건드리지 않는다.

```python
swapped = False                                  # per-tick
if _swap_texts and did_emit and g_emit and byte_len(g_text) > 0:
    _donor = _swap_texts.get(int(tick))
    if _donor is not None:
        g_text = _donor
        swapped = True                           # 라벨은 여기, g_back 은 불변
...
"gen_backend": g_back, "swapped": swapped,       # trace row
```

## 수정 검증 (실 303M · summer 격리 venv · 6 tick × 2 arm)

```
평범(no swap)   recon_err 고유값=6 · rel_lane=6 · swapped tick=0   ✅
SWAP 팔         recon_err 고유값=6 · rel_lane=6 · swapped tick=6   ✅
```

donor 가 **뿌리에 닿는다**. C2 통제군이 살아났다. (pre-fix 는 고유값 1)

## 귀결

- **모든 pre-fix SWAP trace(16개)는 담체 통제군으로서 무가치** — 격리 폐기
  (`~/h9328_swap_INERT_DISCARD`).
- H_9328 은 이미 use-claim ⛔ INVALID 로 닫혔으므로(뿌리 3개 전부 동결) SWAP 은
  H_9328 의 통제군이 아니라 **H_9337 의 C2** 로 재배치된다.
- H_9337 EXP 가 🟢 면 C2 는 **필수**(PASS 를 반증가능하게 만드는 유일한 팔), 🧱 면 확증용.

## 교훈 (convergence `interact-mi-py-3`)

> **실험 라벨은 프로덕션 경로가 분기하는 필드를 타면 안 된다.**
> 그리고 **통제군의 무력함은 DV 를 봐서는 검출되지 않는다** — DV 가 조작변수의 함수일 때,
> 조작이 무력이어도 DV 는 움직인다. **매개 경로를 직접 세라.**

관련: [[H_9328]] (V-CEILING 이 두 주변축은 지켰지만 매개 경로 용량은 아무도 안 지켰다 —
같은 병의 다른 얼굴) · [[H_9336]] · [[H_9337]]
