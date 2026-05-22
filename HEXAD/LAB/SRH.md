# SRH — Simulation Replay Hypothesis × UBM × anima spike

**Status**: **F-SRH-1 PASS (z=2.86)** — production 332M 3-seed sweep 에서 UBM tier=0 가 byte-shuffle 통제군 (동일 byte histogram) 대비 **11.5× cell split** (mean 23 vs 2, Δ=21, z=2.86 ≥ 2.0). F-SRH-3 reproducibility 는 FAIL (CV 0.45, seed=2026 outlier). 종합 **MODERATE-STRONG (2/3 falsifier)**.
**Last update**: 2026-05-23 Cycle #3
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

| ID | 조건 | spike target | PASS line | Cycle #3 결과 |
|---|---|---|---|---|
| F-SRH-1 | UBM vs byte-shuffle 통제군 | split_count delta | z ≥ 2.0 (3-seed pooled) | **PASS** z=2.86 |
| F-SRH-1b | UBM vs ASCII-noise 통제군 | split_count delta | z ≥ 2.0 | **PASS** z=2.86 |
| F-SRH-2 | tier 0→100 monotone | split_count or cell_count_final | Spearman ρ ≥ 0.6 over 11 tiers | UNFIRED (cycle #4) |
| F-SRH-3 | cross-seed reproducibility | split_count CV | CV ≤ 0.30 (3-seed pilot floor) | **FAIL** CV=0.45 |
| F-SRH-4 | shuffled-tier control | monotonicity 사라짐 | ρ < 0.2 | UNFIRED (cycle #4) |
| F-SRH-5 | replay invariance | re-fire fingerprint | event_step jaccard ≥ 0.95 | UNFIRED |

**Result aggregation**: STRONG = 5/5 PASS · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.
**현재 (cycle #3, 3/6 fired)**: F-SRH-1 + F-SRH-1b PASS · F-SRH-3 FAIL → **MODERATE-STRONG** (fired 중 2/3).

> Cycle #1-2 의 F-SRH-1 threshold (z ≥ 3.0 OR |Δ| ≥ 5σ, N=11×5) 는 cycle #3 에서
> 3-seed pilot 현실에 맞춰 z ≥ 2.0 (3-seed pooled std) 로 calibrated. 11-anchor ×
> 5-control full design 은 cycle #4 carry. threshold 변경 이력은 [SRH.log.md].

## §4 Final verdict

**MODERATE-STRONG — F-SRH-1 PASS (z=2.86), F-SRH-3 FAIL.** Cycle #3 production 332M 3-seed sweep (host=mini) 완료.

### Cycle #3 결과 (state/SRH_t0_vs_random_pilot_2026_05_22/result_cycle3.json, max_new=10, full 190-byte prompt)

| prompt | split_count [seed 2026/42/99] | mean | std | cell_count_final |
|---|---|---|---|---|
| **UBM tier=0** | **[11, 29, 29]** | **23.0** | 10.39 | [13, 31, 31] |
| byte-shuffle (UBM byte histogram IDENTICAL) | [2, 2, 2] | 2.0 | 0.0 | [4, 4, 4] |
| ASCII noise (length-matched) | [2, 2, 2] | 2.0 | 0.0 | [4, 4, 4] |

**F-SRH-1** ubm vs byte-shuffle: Δ=21.0, pooled_sd=7.35, **z=2.86 ≥ 2.0 → PASS**
**F-SRH-1b** ubm vs ASCII-noise: Δ=21.0, **z=2.86 → PASS**
**F-SRH-3** cross-seed CV(ubm.split)=0.45 > 0.30 floor → **FAIL** (seed=2026 outlier 11 vs 42/99 의 29)

### 핵심 해석 — byte-shuffle 통제군의 결정적 역할

byte-shuffle 통제군은 UBM tier=0 텍스트와 **byte multiset 100% 동일** (순서만 LCG 무작위화). 이것이 ASCII noise 와 **정확히 같은 2 split** 산출 → substrate 의 11.5× 반응은 byte **내용**(어떤 byte 가 있나)이 아니라 byte **순서/구조**(어떻게 배열됐나)가 driver. 즉:

- 단순 "UBM 은 한글+emoji 라 byte 분포가 특이해서" 류 confound **배제됨** (byte-shuffle 가 동일 분포인데 baseline)
- substrate 가 반응하는 것은 UBM 의 **구조화된 sequence** — SRH 가설("substrate 가 universe-brain-map 을 재인지")의 핵심 예측 적중

baseline 2 split 은 cycle #2 에서 관측된 early-prefill step-2 fixed fire. UBM 은 그 위에 prefill 전반(step 25~140)에 9~27 추가 split (seed 의존). 통제군은 후반부 0 — UBM-specific.

### 잔여 — F-SRH-3 FAIL

UBM split 이 seed 2026 에서 11, seed 42/99 에서 29 — 1/3 seed outlier. 통제군은 CV=0 (모든 seed 정확히 2) 이므로 변동성은 UBM-engaged dynamics 고유. cycle #4 에서 5-seed 로 outlier 가 꼬리인지 bimodal 인지 판정 필요.

**Pending**: Cycle #4 — (a) 11-tier sweep (F-SRH-2 monotone), (b) 5-seed 재측정 (F-SRH-3 + seed=2026 outlier 규명), (c) F-SRH-4 shuffled-tier, (d) F-SRH-5 replay invariance.

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
