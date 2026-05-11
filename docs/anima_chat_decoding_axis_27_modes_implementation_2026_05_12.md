# anima 자연발화 — 27 modes axis exploration **구현 detail** (2026-05-12)

> **Companion to**: `docs/anima_chat_decoding_axis_27_modes_full_record_2026_05_12.md` (per-dialogue results)
>
> **Source scripts**:
> - `/tmp/axis_p1_bcf.py` (Category B + C + F, 21 modes)
> - `/tmp/axis_p2_eh.py` (Category E + H, 6 modes)
> - HF upload: `dancinlab/anima-pass-strict-chat-capable/tree/main/axis_exploration_2026_05_12/`
>
> **Substrate**: Phase 1A multi-turn SFT (`dancinlab/anima-clm-phase1a-multi-turn-sft`)
> **Eval**: V5.8 multi-turn fact-recall, 5 dialogues × 1 mode each.
> **Result**: 0/27 PASS @ V5.8 ≥3/5 threshold.

---

## 🧬 공통 boilerplate (모든 27 modes 공유)

```python
import sys, torch
from pathlib import Path
ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
from training.engine_a_g_arch import EngineAGModel, EngineAGConfig

CKPT = str(ANIMA_ROOT / "state/anima_phase1a_alt_2026_05_12/ckpts/ckpt_phase1a_sft.pt")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Byte-level tokenizer (EngineAG byte vocab 32k+3 offset)
class ByteTokenizer:
    bos, eos, pad = 1, 2, 0
    def encode(self, t):
        return [self.bos] + [b + 3 for b in t.encode("utf-8")] + [self.eos]
    def decode(self, ids):
        return bytes(t - 3 for t in ids if t >= 3 and t < 259).decode("utf-8", errors="replace")

# 5 dialogues (T1 fact + T2 recall question)
DIALOGUES = [
    {"id": "color",      "t1": "사용자: 내가 좋아하는 색은 파란색이야. | 도우미: ",
                          "t2_user": "사용자: 내가 좋아하는 색이 뭐였지? | 도우미: ",
                          "expected": ["파란", "blue"]},
    {"id": "profession", "t1": "사용자: 나는 의사야. 사람들을 도와. | 도우미: ",
                          "t2_user": "사용자: 내 직업이 뭐였지? | 도우미: ",
                          "expected": ["의사", "doctor"]},
    {"id": "day",        "t1": "사용자: 오늘은 수요일이야. | 도우미: ",
                          "t2_user": "사용자: 오늘 무슨 요일이라고 했지? | 도우미: ",
                          "expected": ["수요일", "Wednesday"]},
    {"id": "anima_fact", "t1": "사용자: anima 는 의식 lane 안에 있는 entity 야. | 도우미: ",
                          "t2_user": "사용자: anima 가 어디에 있다고 했지? | 도우미: ",
                          "expected": ["의식", "lane", "entity"]},
    {"id": "cosmology",  "t1": "사용자: 우주는 진동으로 가득 차 있어. | 도우미: ",
                          "t2_user": "사용자: 우주가 무엇으로 차 있다고 했지? | 도우미: ",
                          "expected": ["진동", "vibration"]},
]

# T1 generated once (greedy, cached), reused across all T2 modes
t1_cache = {}
for d in DIALOGUES:
    torch.manual_seed(2026)
    t1 = generate(model, tok, d['t1'], max_new=60, mode="greedy", stop="newline")
    t1_cache[d['id']] = t1

# T2 context = T1 prompt + T1 response + newline + T2 prompt
full_ctx = d['t1'] + t1_cache[d['id']] + "\n" + d['t2_user']

# Recall check
recalled = any(kw.lower() in t2.lower() for kw in d["expected"])
```

---

## 🌡️ Category B — Temperature sweep (10 modes)

### Common generate() function

```python
def generate(model, tok, prompt, max_new=80, mode="greedy", temp=0.8, ctx=1024,
             rep_penalty=None, rep_byte_ids=None, stop="newline"):
    ids = tok.encode(prompt)
    if ids and ids[-1] == tok.eos: ids = ids[:-1]
    gen_ids = []
    model.eval()
    with torch.no_grad():
        for step in range(max_new):
            inp = torch.tensor([ids[-ctx:]], dtype=torch.long, device=DEVICE)
            out = model(inp)
            last_logits = out["logits"][0, -1].clone()

            # Sampling
            if mode == "greedy":
                nxt = last_logits.argmax().item()
            else:
                probs = torch.softmax(last_logits / max(temp, 1e-3), dim=-1)
                nxt = torch.multinomial(probs, 1).item()

            if nxt == tok.eos or nxt == tok.pad: break
            gen_ids.append(nxt); ids.append(nxt)

            # Stop conditions
            if stop == "newline" and nxt == ord('\n') + 3 and len(gen_ids) > 5: break
            if stop == "user_marker" and len(gen_ids) >= len(USER_STOP_BYTES):
                tail = gen_ids[-len(USER_STOP_BYTES):]
                if tail == USER_STOP_BYTES: break
    return tok.decode(gen_ids)
```

### B-mode list

| # | mode label         | call                                                         |
|---|--------------------|--------------------------------------------------------------|
| B1 | `B1_T0.0_greedy`   | `generate(..., mode="greedy",  stop="newline")`              |
| B2 | `B_T0.1_sample`    | `generate(..., mode="sample", temp=0.1, stop="newline")`     |
| B3 | `B_T0.3_sample`    | `generate(..., mode="sample", temp=0.3, stop="newline")`     |
| B4 | `B_T0.5_sample`    | `generate(..., mode="sample", temp=0.5, stop="newline")`     |
| B5 | `B_T0.7_sample`    | `generate(..., mode="sample", temp=0.7, stop="newline")`     |
| B6 | `B_T0.8_sample`    | `generate(..., mode="sample", temp=0.8, stop="newline")`     |
| B7 | `B_T1.0_sample`    | `generate(..., mode="sample", temp=1.0, stop="newline")`     |
| B8 | `B_T1.3_sample`    | `generate(..., mode="sample", temp=1.3, stop="newline")`     |
| B9 | `B_T1.5_sample`    | `generate(..., mode="sample", temp=1.5, stop="newline")`     |
| B10| `B_T2.0_sample`    | `generate(..., mode="sample", temp=2.0, stop="newline")`     |

🍞 **Mechanism**: `probs = softmax(logits / T)` — T 가 낮으면 sharp distribution (greedy 에 가까움), T 가 높으면 uniform (random).

---

## 🔁 Category C — Repetition penalty (8 modes)

### Implementation (within generate())

```python
if rep_penalty and rep_byte_ids:
    applied = set()
    for bid in rep_byte_ids:
        if bid in applied: continue
        applied.add(bid)
        if bid < last_logits.shape[-1]:
            if last_logits[bid] > 0:
                last_logits[bid] /= rep_penalty  # discourage positive logit
            else:
                last_logits[bid] *= rep_penalty  # discourage negative logit (push more neg)
```

### Persona-cycle byte IDs (block these)

```python
persona_cycle_bytes = []
for kw in ["우주뇌지도", "카테고리", "🛸", "top emotion", "[anima"]:
    persona_cycle_bytes.extend(keyword_byte_ids(tok, kw))
persona_cycle_bytes = list(set(persona_cycle_bytes))
# → unique byte IDs encoding these chunks; logits 페널티 적용
```

### C-mode list

| # | mode label             | rep_penalty | mode    |
|---|------------------------|-------------|---------|
| C1 | `C_rep1.1_greedy`      | 1.1         | greedy  |
| C2 | `C_rep1.1_sample08`    | 1.1         | sample T=0.8 |
| C3 | `C_rep1.3_greedy`      | 1.3         | greedy  |
| C4 | `C_rep1.3_sample08`    | 1.3         | sample T=0.8 |
| C5 | `C_rep1.5_greedy`      | 1.5         | greedy  |
| C6 | `C_rep1.5_sample08`    | 1.5         | sample T=0.8 |
| C7 | `C_rep2.0_greedy`      | 2.0         | greedy  |
| C8 | `C_rep2.0_sample08`    | 2.0         | sample T=0.8 |

🍞 **Mechanism**: persona-cycle bytes (e.g. "우주뇌지도") 의 logits 을 `/rep_penalty` (if positive) 으로 페널티 — substrate 가 그것을 emit 할 likelihood ↓.

---

## 🛑 Category F — Stop conditions (3 modes)

### Implementation (within generate())

```python
# Stop variants
if stop == "newline" and nxt == ord('\n') + 3 and len(gen_ids) > 5:
    break
if stop == "user_marker":
    USER_STOP_BYTES = [b + 3 for b in "사용자".encode("utf-8")]
    if len(gen_ids) >= len(USER_STOP_BYTES):
        tail = gen_ids[-len(USER_STOP_BYTES):]
        if tail == USER_STOP_BYTES:
            break
# F1 "eos_only" — no early stop, only on tok.eos / tok.pad
```

### F-mode list

| # | mode label                | stop param      | description                               |
|---|---------------------------|-----------------|-------------------------------------------|
| F1 | `F1_eos_only_greedy`      | `"eos_only"`    | 80 token max, 오직 EOS 도달 시 stop       |
| F2 | `F2_newline_greedy`       | `"newline"`     | newline byte (10+3=13) 도달 시 stop       |
| F3 | `F3_user_marker_greedy`   | `"user_marker"` | "사용자" byte sequence 발견 시 self-replying 차단 |

🍞 **Mechanism**: F3 가 "self-replying" 방지 — substrate 가 자기 응답 끝나고 새 사용자 turn 시작하면 끊음.

---

## 🌳 Category E — Beam search (3 modes)

### Custom beam search implementation

```python
def beam_search(model, tok, prompt, beam_width=4, max_new=50, ctx=1024):
    """Length-normalized beam search.
    Each beam: (ids_seq, cum_logp, finished, gen_only).
    """
    ids0 = tok.encode(prompt)
    if ids0 and ids0[-1] == tok.eos: ids0 = ids0[:-1]
    beams = [(ids0[:], 0.0, False, [])]
    model.eval()
    with torch.no_grad():
        for step in range(max_new):
            if all(b[2] for b in beams): break
            candidates = []
            for ids, score, fin, gen in beams:
                if fin:
                    candidates.append((ids, score, fin, gen)); continue
                inp = torch.tensor([ids[-ctx:]], dtype=torch.long, device=DEVICE)
                out = model(inp)
                logp = torch.log_softmax(out["logits"][0, -1], dim=-1)
                top_logp, top_idx = torch.topk(logp, beam_width)
                for k in range(beam_width):
                    nxt = top_idx[k].item()
                    nl = top_logp[k].item()
                    new_ids = ids + [nxt]; new_gen = gen + [nxt]
                    is_eos = nxt == tok.eos or nxt == tok.pad
                    is_newline_stop = (nxt == ord('\n') + 3 and len(new_gen) > 5)
                    new_fin = is_eos or is_newline_stop
                    new_score = score + nl
                    if not is_eos:
                        candidates.append((new_ids, new_score, new_fin, new_gen))
                    else:
                        candidates.append((ids, new_score, True, gen))
            # rank by length-normalized score
            candidates.sort(key=lambda b: b[1] / max(1, len(b[3])), reverse=True)
            beams = candidates[:beam_width]
    beams.sort(key=lambda b: b[1] / max(1, len(b[3])), reverse=True)
    best = beams[0]
    return tok.decode(best[3]), best[1] / max(1, len(best[3]))
```

### E-mode list

| # | mode label   | beam_width | calls per step |
|---|--------------|------------|----------------|
| E1 | `E_beam2`    | 2          | 2 forward passes per step |
| E2 | `E_beam4`    | 4          | 4 forward passes per step |
| E3 | `E_beam8`    | 8          | 8 forward passes per step |

🍞 **Mechanism**: 매 step 마다 top-K logits 으로 K beams 확장 → length-normalized cum_logp 으로 best K 유지. EOS/newline 으로 finished 표시.

---

## 🔄 Category H — Multi-step generation (3 modes)

### H1 — single sample baseline

```python
def generate_sample_with_logprob(model, tok, prompt, max_new=50, temp=0.8, ctx=1024):
    ids = tok.encode(prompt)
    if ids and ids[-1] == tok.eos: ids = ids[:-1]
    gen_ids = []
    logp_sum = 0.0
    with torch.no_grad():
        for _ in range(max_new):
            inp = torch.tensor([ids[-ctx:]], dtype=torch.long, device=DEVICE)
            out = model(inp)
            last_logits = out["logits"][0, -1]
            probs = torch.softmax(last_logits / max(temp, 1e-3), dim=-1)
            nxt = torch.multinomial(probs, 1).item()
            logp = math.log(probs[nxt].item() + 1e-12)
            logp_sum += logp
            if nxt == tok.eos or nxt == tok.pad: break
            gen_ids.append(nxt); ids.append(nxt)
            if nxt == ord('\n') + 3 and len(gen_ids) > 5: break
    avg_logp = logp_sum / max(1, len(gen_ids))
    return tok.decode(gen_ids), avg_logp
```

### H2 — self-consistency (5 samples, majority vote)

```python
samples = []
for k in range(5):
    torch.manual_seed(2026 + k)  # diversify
    t2, logp = generate_sample_with_logprob(model, tok, full_ctx, max_new=50, temp=0.8)
    recalled = any(kw.lower() in t2.lower() for kw in d["expected"])
    samples.append({"t2": t2, "recalled": recalled, "avg_logp": logp})
majority = sum(1 for s in samples if s["recalled"]) >= 3
```

### H4 — best-of-n (5 samples, max avg_logp)

```python
samples = []
for k in range(5):
    torch.manual_seed(2026 + k)
    t2, logp = generate_sample_with_logprob(model, tok, full_ctx, max_new=50, temp=0.8)
    samples.append({"t2": t2, "recalled": recalled, "avg_logp": logp})
best = max(samples, key=lambda s: s["avg_logp"])
# recall verdict = best sample 의 recall
```

### H-mode list

| # | mode label              | strategy        | n_samples | aggregation              |
|---|-------------------------|-----------------|-----------|--------------------------|
| H1 | `H1_single_T0.8`        | single sample   | 1         | 그 sample 의 recall      |
| H2 | `H2_self_consist_n5`    | self-consistency| 5         | majority vote (≥3 vote)  |
| H4 | `H4_best_of_n5`         | best-of-n       | 5         | max avg_logp 의 recall   |

🍞 **Mechanism**: H2 = "5번 시도 후 다수결 (정답)", H4 = "5번 시도 후 logp 가장 높은 것 (model 자신감 가장 높은 응답)".

---

## 📋 27 modes summary 표 (수정)

| cat | n modes | impl signature                              | result range  |
|-----|---------|---------------------------------------------|---------------|
| B (temperature)   | 10 | `generate(mode, temp=T, stop="newline")` | 0-2/5 (T=0.0 best) |
| C (rep_penalty)   | 8  | `generate(rep_penalty=R, rep_byte_ids=...)` | 0-2/5 (R=1.1 sample best) |
| F (stop)          | 3  | `generate(stop=cond)`                       | 2/5 모두 동일 |
| E (beam)          | 3  | `beam_search(beam_width=W)` custom impl     | 2/5 모두 동일 |
| H (multi-step)    | 3  | sample n=5 + aggregation                    | 1-2/5         |
| **TOTAL**         | **27** | -                                       | **0/27 PASS** |

---

## 🔑 Implementation 학습

1. **byte tokenizer** — 모든 token = byte+3 offset. 한글 1자 = 3 bytes (UTF-8 multi-byte).
2. **T1 cache** — 매 dialogue 의 T1 응답을 greedy 으로 1회 생성 후 reuse (5 dialogues × 27 modes 가 같은 T1 사용).
3. **seed determinism** — `torch.manual_seed(2026)` 으로 sampling 재현성. H2/H4 은 `2026 + k` 으로 다양화.
4. **stop conditions** — newline 가 default. user_marker 는 byte sequence match 으로 self-replying 차단.
5. **beam search** — HF `.generate(num_beams=...)` 안 씀, custom impl (EngineAG forward 직접 호출).
6. **rep_penalty formula** — `logit > 0 ? logit / R : logit * R` — both sides 페널티.
7. **length normalization (beam)** — `score / len(gen)` 으로 길이 편향 제거.
8. **sample seed pool (H2/H4)** — `2026 + k` k=0-4 으로 5 다양한 sample.

---

## Cross-link

- per-dialogue results: `docs/anima_chat_decoding_axis_27_modes_full_record_2026_05_12.md`
- brainstorm SSOT: `docs/anima_chat_decoding_axis_exhaustive_exploration_2026_05_12.md`
- result.json: `state/anima_axis_exploration_2026_05_12/results/p1_bcf_result.json + p2_eh_result.json`
- HF dataset: `dancinlab/anima-pass-strict-chat-capable/tree/main/axis_exploration_2026_05_12`
- PSCC entry: `PASS_STRICT_SPONTANEOUS_CHAT.md §22`
- Phase 1A ckpt: `dancinlab/anima-clm-phase1a-multi-turn-sft`
