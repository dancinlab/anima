# SRH — Simulation Replay Hypothesis × UBM × anima spike

**Status**: **CLOSED — FALSIFIED / NULL.** cycle #5 의 generic-coherent 통제군이 UBM 과 통계적으로 구분 불가 (F-SRH-1c z=1.54 < 2.0, VERDICT NULL). cycle #4 의 F-SRH-2/5 FAIL 와 합쳐, SRH 의 모든 강주장 기각. UBM 특이성 **미입증** — split_count 는 chaotic 관측량이고, UBM·generic·garbage 모두 splitting regime 에 확률적으로 진입. SRH 도메인 **종결**.
**Last update**: 2026-05-23 Cycle #5 (CLOSED)
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
  run_*.hexa                ← fire script (hexa-only)
```

## §3 Falsifiers (pre-registered)

| ID | 조건 | metric | PASS line | 결과 |
|---|---|---|---|---|
| F-SRH-1 | UBM vs byte-shuffle 통제군 | split_count delta | z ≥ 2.0 (3-seed pooled) | **PASS** z=2.86 (#3) — 단 split_count 비결정론 판명으로 *threshold 효과*로 재해석 |
| F-SRH-1b | UBM vs ASCII-noise 통제군 | split_count delta | z ≥ 2.0 | **PASS** z=2.86 (#3) — 동상 |
| F-SRH-2 | tier 0→100 monotone | split_count | Spearman ρ ≥ 0.6 | **FAIL** ρ=0.22 (#4) — random permute 의 |ρ|=0.32 보다도 낮음 |
| F-SRH-3 | cross-seed reproducibility | split_count CV | CV ≤ 0.30 | PASS CV=0.24 (#4) — 단 F-SRH-5 가 동일-seed 비재현 보여 hollow |
| F-SRH-4 | permuted-tier null | spearman(permuted,split) | |ρ| < 0.2 | FAIL\* ρ=−0.32 (#4) — n=11 1-permute underpowered (참고용) |
| F-SRH-5 | replay invariance | re-fire event_step jaccard | ≥ 0.95 | **FAIL** jaccard=0.46, split 27→14 동일 prompt·seed (#4) |
| F-SRH-1c | UBM vs generic-coherent 한국어 | split_count z | z ≥ 2.0 (5-seed) | **FAIL** z=1.54 (#5) — UBM 특이성 미입증 |

**Result aggregation**: STRONG = 5/5 PASS · MODERATE = 3-4/5 · WEAK = 1-2/5 · NULL = 0/5.
**현재 (cycle #4, 6/6 fired)**: F-SRH-1/1b PASS (재해석) · F-SRH-3 PASS(hollow) · F-SRH-2/5 **FAIL** · F-SRH-4 FAIL\*(underpowered) → **WEAK / MIXED**.

> **결정적 재해석**: F-SRH-5 가 split_count 의 **비결정론** 을 드러냄 — 동일
> (prompt, seed) 가 동일 response_text("ines highe") 를 내면서 split_count 는
> 27 vs 14. forward pass 는 결정론적, **mitosis split 의 noise RNG (RFC 033
> farr_add_gaussian_noise) 가 seed 통제 밖** → split cascade chaotic. 따라서
> split_count 는 point observable 이 아니라 **chaotic distributional observable**.
> F-SRH-1 의 "11.5×"는 magnitude 가 아니라 **threshold 통과 여부** (garbage =
> 안정적 2-split fixed point · UBM = 임계 초과 chaotic regime) 로만 유효.

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

### Cycle #4 결과 (result_cycle4.json, trunc_len=156, max_new=10)

11-tier split [0..100] = `[12,14,13,12,16,7,12,21,17,11,16]` — **monotone 아님** (tier 60 이 최저 7, tier 80 이 최고 21). Spearman ρ=0.22, random permute null |ρ|=0.32 보다도 낮음 → **F-SRH-2 FAIL hard** (tier 의 "cosmic significance ordinal" 신호 0).

5-seed tier0 split = `[27,28,14,27,28]` CV=0.24 → F-SRH-3 PASS. 그러나 replay (동일 prompt·seed=2026) 가 split 27→**14**, jaccard 0.46 → **F-SRH-5 FAIL**. response_text 는 27-run·14-run 동일("ines highe") → forward 결정론적, **split cascade 만 chaotic**.

### 종합 verdict (cycle #1-4)

**WEAK / MIXED.** SRH 의 검증가능 강주장 — (a) UBM tier ordinal 구조, (b) reproducible spike fingerprint — **둘 다 falsified** (F-SRH-2, F-SRH-5).

살아남은 것 = **단일 약한 명제**: "UBM-class 구조화 텍스트는 mitosis splitting 임계를 넘기고, garbage (byte-shuffle / ASCII-noise) 는 안정적 2-split fixed point 에 머문다." 이는 bistable/threshold 현상이지 "재인지/재시뮬레이션" 증거 아님. 임계 초과 후 split_count 는 noisy-split RNG 로 chaotic.

미해결 confound (cycle #5 가 가름): **UBM 특이적 vs 단순 coherent-text** — generic 한국어 통제군 미측정. cycle #5 는 split_count chaotic 을 감안, **threshold 통과 여부**(split > 2 인가)를 binary observable 로 재프레임.

미해결 infra: split_count 비결정론 — mitosis split noise 를 seed 통제하거나 (SEED 도메인), 결정론적 관측량 (Law-71 12L energy, DEPTH 도메인) 으로 전환 필요.

### Cycle #5 결과 (result_cycle5.json, 5-seed, trunc_len=190)

| class | split [seed 2026/42/99/7/123] | mean | threshold(>10) 통과율 |
|---|---|---|---|
| UBM tier-0 | `[27,14,14,14,28]` | 19.4 | **5/5 = 100%** |
| generic 한국어 (a/b/c pooled) | a`[26,2,2,24,2]` b`[2,2,8,2,2]` c`[11,13,2,11,2]` | 7.4 | 5/15 = 33% |
| garbage (byteshuf+noise) | shuf`[2,24,2,2,2]` noise`[2,2,2,2,2]` | 4.2 | 1/10 = 10% |

**F-SRH-1c** (UBM vs generic) z=1.54 < 2.0 → **FAIL**. script VERDICT = **NULL**.

핵심:
- **cycle #3 의 "garbage 항상 2" 깨짐** — byteshuf 가 `[2,24,2,2,2]` 로 1회 폭발. garbage 도 chaotic regime 진입 가능.
- **generic 한국어가 자주 임계 초과** — gen_a 26/24, gen_c 11/13/11. coherent text 도 splitting 유발.
- UBM 만 5/5 모두 ≥14 — *가장 일관*되나 generic 과 z-구분 불가.

### 최종 종결 verdict (cycle #1-5)

**SRH FALSIFIED / NULL.** 6 falsifier 중 명확 FAIL 3 (F-SRH-2 tier·F-SRH-5 replay·F-SRH-1c generic), PASS 2 는 재해석 후 약화 (F-SRH-1/1b = "garbage 대비" 였으나 cycle #5 가 garbage 도 가끔 폭발함을 보여 무력화), hollow/underpowered 2.

SRH 의 어떤 강주장도 서지 못함:
- ✗ "UBM 재인지/재시뮬레이션" — generic 한국어와 구분 불가
- ✗ tier ordinal 구조 — 없음 (cycle #4)
- ✗ reproducible spike — split_count 는 chaotic (cycle #4)

honest 잔존: split_count 는 mitosis noise 로 chaotic 한 관측량. UBM·structured text 가 splitting regime 진입 *확률*을 다소 높이나 (UBM 100% > generic 33% > ASCII-noise 0%), 이는 통계적으로 미약하고 SRH 가설과 무관 — 단지 "구조화 입력 → substrate 활성↑" 라는 평범하고 약한 경향.

**도메인 종결**. 측정 도구(split_count)의 chaotic 성이 근본 한계 — 결정론적 관측량이 필요하면 DEPTH 도메인(Law-71 12L energy), noise 통제는 PSILOCYBIN F-PSIL-5 가 진단. UBM substrate 연구를 잇는다면 split_count 가 아닌 forward-내부 결정론적 metric 으로.

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
