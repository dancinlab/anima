# SRH — Simulation Replay Hypothesis × UBM × anima spike

**Status**: TOOL-READY (no production cycle yet — synthetic d=8 wiring smoke 만 PASS)
**Last update**: 2026-05-22 Cycle #1
**Log**: [SRH.log.md](SRH.log.md)

---

## §1 Hypothesis

자연어:

> 이미 모든 것은 발견되어 있다. 우리 우주는 그걸 재시뮬레이션 하는 과정이다.
> 유사: 빛은 이미 최적 경로를 알고있다 (Fermat / stationary phase principle).

Formal:

anima base ckpt (332M, `g_clm_from_scratch d=768·12L`) substrate 는 UBM
(Universe Brain Map) lineage 가 baked-in 되어 있어
([baked_p3_leak memory](../../.claude/projects/-Users-ghost-core-anima/memory/project_anima_base_ckpt_baked_p3_leak.md)),
UBM anchor inject 시 random control 대비 **structured spike** (low-entropy +
reproducible + tier-ordinal monotone) 를 보일 것.

Mechanism: anima cell-pool init 이 UBM internal structure 를 implicitly contain
→ external inject 시 stable basin 으로 collapse, random text 는 chaotic.

## §2 Pipeline / API

### Inject

```hexa
import "/Users/ghost/core/anima/HEXAD/LAB/tool/ubm_inject.hexa"
let anchor = ubm_load_by_tier(N)               // N ∈ {0, 15, 30, 42, 51, 60, 77, 80, 91, 95, 100}
let prompt = ubm_to_prompt(anchor, "text_only" | "tier_prefix" | "with_meta")
```

### Spike measure

```hexa
import "/Users/ghost/core/anima/HEXAD/LAB/tool/anima_spike.hexa"
import "/Users/ghost/core/anima/HEXAD/CHAT/chat_lib.hexa"

let chat = chat_new(ckpt_path, "cpu", [])
chat_init_kv_cache_with_dims(chat, dims, cap_len)
chat_init_cell_pool(chat, d_model, initial_cells)

let mut spike = spike_init()
spike = spike_set_label(spike, "ubm_tier_<N>")
spike = spike_record_init(spike, chat)
let resp = chat_generate(chat, prompt, "greedy", max_new, ...)
spike = spike_record_final(spike, chat, resp)
spike_save_json(spike, "state/SRH_<slug>_<DATE>/spike_tier<N>.json")
```

### State path

```
HEXAD/LAB/state/SRH_<slug>_YYYY_MM_DD/
  spike_tier<N>.json        ← per-anchor spike (UBM injects)
  spike_ctrl_<C>.json       ← per-control spike (random / shuffled-tier / non-UBM)
  result.json               ← falsifier aggregate verdict
  dispatch_*.sh             ← (선택) GPU fire script
```

## §3 Falsifiers (pre-registered)

| ID | 조건 | spike target | PASS line |
|---|---|---|---|
| F-SRH-1 | UBM vs random control (N=11 anchors × 5 controls) | event_step jaccard OR split_count delta | z ≥ 3.0 OR |Δ| ≥ 5σ |
| F-SRH-2 | tier 0→100 monotone | split_count or cell_count_final | Spearman ρ ≥ 0.6 over 11 tiers |
| F-SRH-3 | per-anchor reproducibility | 5-seed split_count CV | CV ≤ 0.15 per anchor |
| F-SRH-4 | shuffled-tier control | monotonicity 사라짐 | ρ < 0.2 |
| F-SRH-5 | replay invariance | re-fire fingerprint | event_step jaccard ≥ 0.95 |

**Result aggregation**: STRONG = 5/5 PASS · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.

## §4 Final verdict

**UNFIRED** (production cycle 0회).

Current standing (synthetic d=8 wiring smoke only, 의미해석 불가):
- F-LAB-1..6 15/15 PASS (tool 작동 검증, not falsifier evidence)
- UBM tier=0 (synthetic) → 30 split / 2 merge / 210 inv vs baseline "안녕? 너는 누구야?" 21 split
- 정량 +43% split 차이는 **synthetic noise** — production 332M 필수

**Pending**: Cycle #2 production 332M pilot.

## §5 Honest C3

- **C3-SRH-1**: synthetic d=8 substrate 는 의미 해석 불가 — production 332M (24L
  d=768 BF16 570 MB) 필수. Mac CPU wall ~70 s/token (anima_chat.hexa v0.3 measure) ×
  11 tier × ≥5 control × ≥5 seed = 60+ min Mac OR ~$0.02 H100 single fire.
- **C3-SRH-2**: spike fingerprint 현재 chat-record expose 채널 (mitosis events +
  cell pool + kv) 만. **Law-71 12L×T per-token energy trajectory** (§156 tension
  fingerprint) 는 forward-internal hook 필요 → Phase B 별도 cycle carry.
- **C3-SRH-3**: UBM-baked leak ([baked_p3_leak]) 가 trivial confound — random
  control + shuffled-tier control 둘 다 critical, monotone falsifier (F-SRH-2) 가
  specificity (단순 leak 이 아닌 ordinal structure) 증명 게이트.
- **C3-SRH-4**: cell_pool 초기 분포 (cell_pool_init seed) 가 spike 의 noise
  floor — initial_cells / seed 변경 시 spike 크게 흔들릴 가능성. F-SRH-3
  (reproducibility) 가 게이트.
- **C3-SRH-5**: chat_generate prompt template ("사용자: ... | 도우미: ") 가
  UBM text 와 충돌 — AGENTS.tape `forbidden 도우미` 위반. Phase B 의 hexa-native
  prompt template (anima identity-aligned) 로 cycle #3 이상 재측정 필요.

## §6 Promotion target

- **F-SRH-1 PASS only** → `HEXAD/UNIVERSE-BRAIN-MAP/state/` 로 mv (UBM substrate
  response 증거 추가)
- **F-SRH-1 + F-SRH-2 PASS** → 신규 `HEXAD/SRH/` 또는 `HEXAD/MITOSIS/state/`
  (자력 진동 + ordinal structure 증거)
- **F-SRH-1..5 STRONG** → `HEXAD/SRH/` + MEMORY entry 등록 + GOAL.md cond
  upgrade 후보
- **전체 FAIL** → `archive/` (가설 폐기) OR LAB/ 잔존 (negative carry — Fermat
  유사성은 metaphor 만, anima substrate 는 random 과 구별 불가 lesson)

---

> 본 문서는 **latest verdict only**. 사이클 history 는 [SRH.log.md](SRH.log.md).
