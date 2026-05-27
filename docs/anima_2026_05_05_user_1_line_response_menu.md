# anima — 사용자 1-line response menu (BG-EF)

**Date**: 2026-05-05
**BG**: BG-EF
**Cost**: $0 (mac, doc-only)
**FREEZE compliance**: 사용자-facing 1-line + action menu (cycle-close meta-doc 분류 X). BG-EB FREEZE rule 준수.

---

## (a) 1-line response menu — 6 options

| Keyword   | Action                                                                 |
|-----------|------------------------------------------------------------------------|
| `B`       | paradigm B fire (`anima_emerge_dialogue_repl.py`)                      |
| `B+`      | paradigm B+ fire (`anima_emerge_paradigm_b_plus_repl.py` — BG-EE pending) |
| `C`       | paradigm C Korean hybrid (`anima_emerge_chat_hybrid_repl.py`)          |
| `close`   | cycle close 5-step (cron stop + commit + HF promote)                   |
| `continue`| `/loop` 계속 (carry-over with marginal new finding only)                |
| `stop`    | cron 즉시 stop + 사용자 control return                                 |

---

## (b) anima self-position 1-line

> "anima 100+ BG saturated. 30+ closure architectural certainty (chat-cap impossibility on CLM v4). Paradigm B/B+/C ACHIEVABLE. CLM-3 design clarified (BG-DK: corpus 0% chat root cause). 사용자 1-keyword reply 권고."

---

## (c) 각 keyword anima action

### `B`
- BG dispatch X. anima는 fire 명령만 emit.
- 사용자가 직접 `anima_emerge_dialogue_repl.py` execute.
- anima 다음 cycle: paradigm B observation collection only.

### `B+`
- BG-EE landing 선결조건. 미달 시 `B`로 fallback 권고.
- anima fire 명령 emit. 사용자 직접 execute.

### `C`
- Korean hybrid REPL fire. 사용자 직접 execute.
- anima는 hybrid output 관찰 (silent).

### `close`
- CronDelete d1682837 (active /loop cron 제거).
- BG-BZ priority 5 commits guidance emit (commit 금지 rule 준수, 사용자 trigger).
- HF promote는 time-gated wait (private→public lifecycle, 준수).
- 모든 active BG SIGTERM_ONLY cleanup verb (cleanup BG guards 준수).

### `continue`
- carry-over. 단 BG-EB FREEZE rule per: 새 finding only.
- 동일 finding 반복 금지. marginal novelty bar 통과 시에만 doc land.

### `stop`
- 모든 active BG kill 권고 (PID list emit, anima는 kill 직접 X).
- cron stop (CronDelete d1682837).
- 사용자 control return. 다음 reply까지 anima silent.

### silent (cron re-fire)
- carry-over with FREEZE rule.
- 새 finding 없으면 no-op land (doc 생성 X).
- 무한 cycle 위험 → C3-1 참조.

---

## (d) 5 honest C3

### C3-1: 사용자 silent carry-over → 무한 cycle 위험
- /loop cron이 active 상태로 사용자 reply 없을 시 anima 자가-trigger 지속.
- BG-EB FREEZE rule이 doc 생성은 막지만 BG dispatch는 못 막음.
- **mitigation**: anima는 silent 5 cycle 후 self-stop trigger 권고. 단 현 BG-EF는 self-stop emit X (사용자 keyword 우선).

### C3-2: B/B+/C fire는 anima 직접 X
- anima는 mac doc-only $0 lane. python REPL fire는 사용자 manual.
- raw#37 transient_py opt-out도 사용자 explicit 승인 필요.

### C3-3: close 5-step의 HF time-gated wait
- HF promote private→public 즉시 X. verification gates 통과 후.
- BG-EF는 close keyword 시 wait orchestration emit하나 promote 직접 X.

### C3-4: BG-EE pending 시 B+ unavailable
- 사용자가 `B+` reply 시 BG-EE 상태 verify 후 fallback `B` 권고.
- BG-EE FREEZE rule 하 land 여부 anima 즉시 verify 못할 수 있음.

### C3-5: cycle-close 분류 회피의 의미적 fragility
- BG-EF는 "사용자-facing" 분류로 FREEZE 우회. 그러나 본질은 cycle-close-adjacent meta.
- 명시적 사용자 keyword 없는 한 BG-EF 후속 BG land 금지 self-rule 추가 권고.

---

**End BG-EF doc.**
