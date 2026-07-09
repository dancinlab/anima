"""core/wake_memory.py — episodic append-only + working ring-buffer memory.

py 2-production twin of core/wake_memory.hexa — byte-exact mirror (owner directive 2026-07-09
"py 자체구현 · 언어간 상호의존 0"). Pure dict/list logic (no numpy, no FFI): episodic
append-only [ts·ctx_summary·phi·tension5·stage·emit_text] + working ring buffer (cap=20 FIFO).
brain_decide 의 ctx 전치 surface · 0 emit trigger · 0 boolean gate · empty perception push 도
1 tick 으로 count. Sequential copy order preserved verbatim. (hexa Map #{} → python dict.)
"""


def _working_cap():
    return 20


def mem_init():
    return {"episodic": [], "working": []}


def mem_record_emit(mem, ts, ctx_summary, phi, tension5, stage, emit_text):
    if len(tension5) != 5:
        raise ValueError("mem_record_emit: tension5 must have len=5, got " + str(len(tension5)))
    record = {
        "ts": ts,
        "ctx_summary": ctx_summary,
        "phi": phi,
        "tension5": tension5,
        "stage_name": stage,
        "emit_text": emit_text,
    }
    new_episodic = []
    i = 0
    while i < len(mem["episodic"]):
        new_episodic.append(mem["episodic"][i])
        i = i + 1
    new_episodic.append(record)
    return {"episodic": new_episodic, "working": mem["working"]}


def mem_push_ctx(mem, ctx_tokens):
    cap = _working_cap()
    new_working = []
    cur_len = len(mem["working"])
    start_idx = 1 if cur_len + 1 > cap else 0
    i = start_idx
    while i < cur_len:
        new_working.append(mem["working"][i])
        i = i + 1
    new_working.append(ctx_tokens)
    return {"episodic": mem["episodic"], "working": new_working}


def mem_recent_emits(mem, n):
    if n <= 0:
        return []
    total = len(mem["episodic"])
    if total == 0:
        return []
    start = total - n if total > n else 0
    out = []
    i = start
    while i < total:
        out.append(mem["episodic"][i])
        i = i + 1
    return out


def mem_working_window(mem):
    out = []
    i = 0
    while i < len(mem["working"]):
        out.append(mem["working"][i])
        i = i + 1
    return out


def memory_summary():
    return ("wake_memory · episodic append-only [ts·ctx_summary·phi·tension5·stage·emit_text] + "
            "working ring buffer (cap=20 FIFO) · brain_decide 의 ctx 전치 surface · 0 emit trigger · "
            "0 boolean gate · empty perception push 도 1 tick 으로 count · kosmos round-trip = "
            "core/kosmos_io follow-on (구현됨·미배선)")
