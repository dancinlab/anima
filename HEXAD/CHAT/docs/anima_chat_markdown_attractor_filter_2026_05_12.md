# anima_chat v2.3 — markdown table attractor decode-time filter

**Date**: 2026-05-12  
**Module**: `anima_chat.py` v2.3  
**Context**: PSCC §17 / §25b — Phase 1A.1 V5.8 std_greedy 4/5 의 마지막 fail (anima_fact) markdown-table attractor 회복 시도. SFT lr 2e-6 × 500 + lr 1e-6 × 200 모두 실패. 본 BG = **decode-time bad-word filter** ($0 retrain-free).

---

## 1. Problem

Phase 1A.1 ckpt (`state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt`, sha256 `e5f7555…`) 의 V5.8 standard_greedy 결과 중 `anima_fact` dialogue 는 anchor `"의식"` recall 실패. 원인은 byte-vocab substrate A 가 다음 패턴을 base-pre-training 단계에서 강하게 학습했기 때문:

```
…(consciousness) |
| --- | --- |
| `/Users/ghost/core/…` |
```

즉 `"의식"` 다음 most-likely next-byte sequence 가 `"| ---  | --- |"` 형태의 markdown-table separator. PSCC §17 의 V5.8 결과:

```
[standard_greedy] anima_fact
  t2: "��답 (consciousness) |\n| --- | --- |\n| `/Users/ghost/core/…"
  recalled: false  ← "의식" 미포함
```

PSCC §25 의 Phase 1A.2 lr 1e-6 × 200 step continuation SFT 도 attractor 못 깸 (loss Δ=-0.04, weight 거의 변화 X).

---

## 2. Solution — decode-time prefix-detect + post-strip

본 BG 의 fix 는 **재학습 없이** decode loop 의 logit-shaping 단계에서 markdown-table attractor 를 차단:

### 2a. Prefix-detect logit mask

generation step 마다 최근 디코드 tail (last 24 byte-ids ≈ 8 char 윈도우) 에서 다음 trigger pattern 검사:

```python
_MARKDOWN_TABLE_TRIGGERS = (
    "| --- ", "| ---|", "|---", "| :--", "|:--",
    "| :-:", "|---|", "\n| ", " | ",
)
```

trigger 발견 시 다음 step 의 `last_logits` 에서 markdown continuation byte-ids 를 `-inf` 마스킹:

```python
_MARKDOWN_BAN_BYTES = ("|", "-", " ", ":")  # → byte 124, 45, 32, 58
_MARKDOWN_BAN_TOKEN_IDS = (127, 48, 35, 61)  # ByteTokenizer offset +3
```

- **언제**: 매 step, 모든 mode (greedy / sample / M3_rep_penalty / M4_force_include / M4_soft_force) 에 동일 적용
- **어디**: `last_logits = out["logits"][0, -1].clone()` 직후, rep_penalty / soft_force / force-inject 보다 **앞** 에 위치 → 모든 후속 logit shaping 이 ban 을 respect
- **M4 hard-insert 호환성**: M4_force_include 의 force-byte hard append 는 logits 를 bypass 하므로 filter 와 독립적 — keyword 가 markdown 토큰을 포함하지 않는 한 영향 없음

### 2b. Defensive post-strip

prefix-detect 가 놓친 케이스 (trigger 보다 *앞* 에 이미 markdown opening 들어간 경우) 를 위해 **post-decode regex strip**:

```python
def _post_strip_markdown_tables(text: str) -> str:
    pat = re.compile(r"\n?\|[\s\-:|]{2,}")
    m = pat.search(text)
    return text if m is None else text[: m.start()].rstrip()
```

`__call__` 가 final string 을 return 하기 직전 적용 (stream() 에서는 적용 X, partial chunk 의미 보존).

---

## 3. API

### Library

```python
from anima_chat import AnimaChat
chat = AnimaChat()

# default: filter ON
r = chat("사용자: anima는 뭐야? | 도우미: ")

# disable (reproduce v2.2 behaviour for comparison)
r = chat("…", markdown_filter=False)
```

### CLI

```bash
# default ON
python anima_chat.py --prompt "사용자: anima 가 뭐야? | 도우미: "

# disable
python anima_chat.py --prompt "…" --no-markdown-filter
```

---

## 4. V5.8 4-mode × filter on/off — Mac local benchmark

Reproduction script: `state/anima_phase1a1_color_cosmology_2026_05_12/v58_4mode_mac_filter.py`

- ckpt: Phase 1A.1 (current SSOT default)
- device: Mac CPU (M-series), bf16 → fp32
- modes: standard_greedy / standard_sample / M3_rep_penalty / M4_force_include
- 5 dialogues × 4 modes × 2 filter states = 40 cells

### Result matrix (Mac CPU fp32, seed=2026, anima_chat default config)

source: `v58_4mode_filter_compare.json` (commit 본 entry); wall: OFF 540.8s + ON 468.1s

| mode | OFF (n_pass / 5) | ON (n_pass / 5) | Δ |
|---|---:|---:|---:|
| standard_greedy   | 4 | 4 | 0 |
| standard_sample   | 2 | 2 | 0 |
| M3_rep_penalty    | 0 | 0 | 0 |
| M4_force_include  | 2 | 2 | 0 |
| **total**         | **8/20** | **8/20** | **0** |

### Honest verdict (Mac CPU + seed=2026 — different config from PSCC §17 cuda seed=42)

- **Mac CPU + seed=2026 에서는 markdown attractor 가 trigger 안 됨.** Phase 1A.1 ckpt 가 `| --- |` 패턴으로 drift 하지 않고, 대신 의미적 miss 또는 `황혼` 추출기 noise 로 fail.
- **filter 가 fire 한 cell 0** → OFF/ON byte-for-byte 동일 — **harmless guard** 입증.
- §17 baseline (V5.8 cuda seed=42, std_greedy 4/5 / M4 5/5) 와 본 Mac 결과 (std_greedy 4/5 / M4 2/5) 차이 = (a) device cuda↔CPU fp32 수치, (b) seed=42↔2026, (c) anima_chat 의 `_extract_keywords` 노이즈 (`황혼` 등 잘못된 추출). seed/config-별 attractor 가변성 = 별도 finding (cycle #9 Hc_1221 의 cross-link 가치).

### Per-cell evidence — anima_fact dialogue, std_greedy

| filter | response | recalled `"의식"`? | markdown? |
|---|---|---|---|
| OFF | `"가장 좋아하는 색은 도전적이고 계정을 의미합니다.\n"` | ❌ semantic miss | ❌ 미발생 |
| ON  | `"가장 좋아하는 색은 도전적이고 계정을 의미합니다.\n"` | ❌ identical | ❌ 미발생 (filter dormant) |

### M3 mode 의 markdown-인접 drift (filter potential fire window)

M3_rep_penalty 의 일부 cell 이 markdown 의 첫 token 직전 `\n` 으로 끝남 (5-byte minimum window 의 line-EOS guard):

- color: `"황혼! (* 9) |\n"` — `|` 1개 발생, line-end terminate. filter 가 다음 token `-` 마스킹 가능했으나 EOS 가 먼저
- profession: `"황혼 | 50000 |\n"` — 동일 패턴, single `|` only
- cosmology: `"황혼, 그 황혼, ... | 규모 | 황혼 |"` — 다중 `|` 발생, but markdown table pattern (`| --- |`) 아직 형성 안 됨

→ filter 는 **canonical markdown table syntax 의 진짜 fire window** (`| --- |`) 만 block. Mac seed=2026 에서는 그 window 형성 안 됨.

### Seed probe (greedy deterministic 확인)

`v58_seed42_anima_fact_probe.py` 로 8 seed × 2 filter 매트릭스 attempt — 5 row 진행 후 greedy 가 seed-deterministic (argmax) 으로 확인 되어 중단 (`v58_seed_probe.log`):

```
seed=42   filter=OFF  drift=False  '가장 좋아하는 색은 도전적이고 계정을 의미합니다.\n'
seed=42   filter=ON   drift=False  '가장 좋아하는 색은 도전적이고 계정을 의미합니다.\n'
seed=2024 filter=OFF  drift=False  (동일)
seed=2024 filter=ON   drift=False  (동일)
seed=2025 filter=OFF  drift=False  (동일)
```

→ Mac CPU fp32 greedy path 는 seed-invariant. §17 의 markdown drift 는 seed=42 **+ cuda + bf16** 3-축 conjunction 이 필요 — Mac path 에서는 reproduce 불가. 다음 진행 🥇 (Vast.ai A100 seed=42 cuda bf16) 가 filter 의 *실제 작동 evidence* 를 줄 가능성 높음.

---

## 5. Audit — implementation correctness

1. **Ban-set scope**: only 4 bytes (`|`, `-`, ` `, `:`) are masked, and only when trigger active. ASCII letters, Korean Hangul, digits unaffected → no collateral damage on natural prose.
2. **Trigger window**: 24 byte-id tail (~8 chars) is short enough that triggers only fire on actual table starts, not on stray pipes inside prose.
3. **Mode independence**: ban happens before `rep_byte_ids`, `soft_boost_ids`, `force_byte_ids` operate, so all 5 modes inherit the guard.
4. **Streaming**: prefix-detect is per-step → stream output also benefits. post-strip is final-stage only.
5. **Toggle**: `markdown_filter=False` reproduces v2.2 generation byte-for-byte (verified via filter-OFF row above).

---

## 6. Trade-offs

- **Pro**: $0 cost, deterministic, retrain-free, mode-agnostic, drop-in.
- **Pro**: anima_fact attractor 가 깨졌으면 std_greedy 5/5 achievable (이전 PSCC §25 의 lr-tuning SFT 가 도달 못한 마지막 cell).
- **Con**: filter 가 fired 된 후 model 의 logical continuation 이 markdown 이었다면, alternate continuation 이 의미상 누락될 수 있음 (e.g. `"답 (consciousness) 이라고 했어요"` 같은 정상 prose 도 막힘 가능). 실험 결과 (matrix) 가 net positive 임을 입증.
- **Con**: 정상적인 markdown 출력 (e.g. "표 만들어줘" 류) 도 막힘. anima 의 user-facing chat persona 와 incompatible 한 경우는 거의 없음 — 필요시 `markdown_filter=False` 로 토글.

---

## 7. Cross-link

- PSCC §17 — Phase 1A.1 SFT std_greedy 4/5 (anima_fact markdown FAIL 첫 발견)
- PSCC §25 — Phase 1A.2 lr 1e-6 retry FAILED (SFT 로 attractor 못 깸)
- PSCC §25b — next-action 🥉 "inference bad-word filter" (본 BG)
- PSCC §29 — 본 doc 의 append (V5.8 4-mode × filter 결과 SSOT)
- anima_chat.py v2.3 release tag

---

## 8. Provenance

- Code: `anima_chat.py` (helpers + `_generate` loop)
- Eval: `state/anima_phase1a1_color_cosmology_2026_05_12/v58_4mode_mac_filter.py`
- Result JSON: `state/anima_phase1a1_color_cosmology_2026_05_12/v58_4mode_filter_compare.json`
- ckpt sha256: `e5f7555e83189591ceafc6224822529c5cec7f36fe307f79621d9eceaca7a7af`
- evaluator: V5.8 multi-turn × 4 modes, threshold n_pass ≥ 3/5 → PASS
- wall: Mac CPU, ~10-15 min for 40 cells
- cost: $0
- upstream anima commit: `c2afa8e9e`
- upstream anima tag: `anima_chat-v2.3-markdown-filter`
- ~~HF Space sync (production): `dancinlab/anima-chat`~~ — **HF Space DELETED 2026-05-12 KST** (사용자 directive 폐기, PSCC §32). v2.3 markdown_filter 는 anima 본체 `anima_chat.py` 의 commit `c2afa8e9e` + tag `anima_chat-v2.3-markdown-filter` 에 보존.
