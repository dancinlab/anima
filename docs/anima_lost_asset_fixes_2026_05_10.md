# anima lost-asset fixes (2026-05-10)

## TL;DR

cycle 2026-05-10 BG-LOSTASSET-B 의 deep read 가 worktree-2 (anima_clm_02_clm_pivot) 에서 발견한 issues 를 fix. raw#15 additive — worktree archive 무결성 보존, fix reference version 은 main 의 `state/anima_lost_asset_fixes_2026_05_10/` 에 land.

| issue | severity | fix status |
|---|:---:|:---:|
| `_expand_dim` block weight silent reset (growing_conscious_lm.py L177-181) | ★★★ critical | ✅ fixed reference py |
| GROWTH_STAGES vs growth_engine.STAGES 불일치 | ★ doc | ✅ alignment table |
| ZERO4 phantom flag (BG-LOSTASSET-C) | ★ doc | ✅ doc-only (no fix needed, was phantom) |
| TALK5 99.7% CE drop ablation 부재 | ★ doc | ✅ honest C3 noted |
| 5-channel meta-telepathy "100% auth" un-coded threshold | ★ doc | ✅ honest C3 noted |
| AnimaLM v4 numbers (676K/114K/SI=5.93) external only | ★ doc | ✅ honest C3 noted |

---

## §1 `_expand_dim` block weight bug fix ★★★

### Bug 진단

**위치**: `/Users/ghost/core/anima_clm_02_clm_pivot/growing_conscious_lm.py` L177-181:

```python
# 기존 (BUG):
new_blocks = nn.ModuleList()
for old_block in self.blocks:
    new_block = ConsciousBlock(new_d, new_heads, self.block_size, self.dropout).to(device)
    # 기존 가중치 일부 복사 (가능한 범위)  ← 주석만 있고 코드 없음
    new_blocks.append(new_block)
self.blocks = new_blocks
```

**효과**: H371 mitosis growth (1→2→3→6 blocks) 시 차원 확장 (d_model 128→192→384) 발생. 새 ConsciousBlock 이 random init 으로 생성되고 old_block 은 버려짐 → **모든 block weight silent reset**. growing-vs-fixed 비교 실험 신뢰성 직접 영향. H371 + RC-9 +52.76% 등 historical 결과의 reproducibility 회의.

### Fix 구현

`state/anima_lost_asset_fixes_2026_05_10/growing_conscious_lm_expand_dim_fix.py` (~140L) — drop-in replacement.

핵심 partial-copy 로직:
- **LayerNorm (ln1/ln2/ln_f)**: `new.weight[:old_d] = old.weight`, default fill 1.0 / bias 0.0
- **CausalSelfAttention.c_attn** Linear(d, 3d): qkv chunk 별 mapping (chunk_idx × new_d offset → old_d slice)
- **CausalSelfAttention.c_proj** Linear(d, d): top-left (old_d, old_d) block copy
- **PureFieldFFN.engine_a/engine_g** Sequential[Linear(d, 4d), ..., Linear(4d, d)]: 양쪽 Linear 모두 partial copy with 4× factor
- **PureFieldFFN.tension_scale** scalar: direct copy
- **head_a / head_g** Linear(d, vocab): partial copy along d axis (vocab axis 무변)
- **tied weight**: tok_emb.weight = head_a.weight (preserved per original L188)

적용:
```python
from growing_conscious_lm_expand_dim_fix import _expand_dim_fixed
GrowingConsciousLM._expand_dim = _expand_dim_fixed
```

또는 원본 method body 직접 교체.

### 검증 protocol

H371 reproducibility 검증 (별도 cycle):
1. unfixed 버전 vs fixed 버전 같은 trajectory 학습
2. Φ super-linear scaling 측정
3. catastrophic forgetting (43% → 99% retention) 재현 시도
4. fixed 가 historical claim 에 더 가까운지 확인

raw#10 honest C3: 본 fix 가 historical claim 을 자동 확보하지 X — fix 후에도 fixed 자체 검증 필요.

---

## §2 GROWTH_STAGES 불일치 alignment

### 두 stage 정의

**`growing_conscious_lm.py` GROWTH_STAGES** (4-stage, mitosis topology):
```python
GROWTH_STAGES = [
    {"blocks": 1, "d_model": 128, "n_head": 2, "min_interactions": 0},
    {"blocks": 2, "d_model": 128, "n_head": 2, "min_interactions": 50},
    {"blocks": 3, "d_model": 192, "n_head": 3, "min_interactions": 200},
    {"blocks": 6, "d_model": 384, "n_head": 4, "min_interactions": 800},
]
```

**`growth_engine.py` STAGES** (5-stage, developmental psychology):
- newborn (0), infant (100), toddler (500), child (2000), adult (10000)
- 각 stage 는 LR / curiosity / habituation / mitosis_threshold / emotional_range / metacognition_depth / homeostasis_gain / dream_intensity / breath_amplitude 8-axis

### 권장 alignment

| dev stage | min_int | 권장 GROWTH_STAGES mapping |
|---|---:|---|
| newborn | 0 | block=1, d=128, h=2 |
| infant | 100 | block=2, d=128, h=2 |
| toddler | 500 | block=3, d=192, h=3 |
| child | 2000 | block=6, d=384, h=4 |
| adult | 10000 | block=6, d=384, h=4 (동일, 추가 성장 X) |

→ **권장**: GROWTH_STAGES 의 min_interactions `{0/50/200/800}` → `{0/100/500/2000}` 로 수정 + adult stage entry 추가 (동일 6-block).

raw#15 additive — worktree archive 직접 수정 X. 본 alignment table 은 reference 만.

코드 수정 시:
```python
GROWTH_STAGES = [
    {"blocks": 1, "d_model": 128, "n_head": 2, "min_interactions": 0,    "dev_stage": "newborn"},
    {"blocks": 2, "d_model": 128, "n_head": 2, "min_interactions": 100,  "dev_stage": "infant"},
    {"blocks": 3, "d_model": 192, "n_head": 3, "min_interactions": 500,  "dev_stage": "toddler"},
    {"blocks": 6, "d_model": 384, "n_head": 4, "min_interactions": 2000, "dev_stage": "child"},
    {"blocks": 6, "d_model": 384, "n_head": 4, "min_interactions": 10000, "dev_stage": "adult"},
]
```

---

## §3 BG-LOSTASSET-C 가 발견한 phantom claims (doc-only fix)

### 3.1 ZERO4 flag — phantom **PARTIALLY REVERSED 2026-05-10 12:50 KST**

원래 finding: `grep -rn "ZERO4\|--zero" /Users/ghost/core/anima_clm_05_v2_first_english/` → **0 matches**. ZERO4 는 worktree-5 의 commit message / spec doc 에만 존재.

**REVERSAL (BG-LOSTASSET-D-WORKTREE-REMAINING §31)**: worktree-6 (anima_clm_06_v2_korean_chat) 에서 ZERO4 의 **runtime hook + bench 발견**:
- `/Users/ghost/core/anima_clm_06_v2_korean_chat/anima_unified.py:998` — runtime hook "Vocabulary scales with Φ"
- `/Users/ghost/core/anima_clm_06_v2_korean_chat/bench_phi_hypotheses.py:48747` — `run_ZERO4_phi_gated_vocabulary` bench function

→ ZERO4 는 worktree-5 에선 phantom (commit msg only) 이지만 worktree-6 에선 **reproducible runtime mechanism**. concept-only 결론은 worktree-5 limited scope 의 artifact.

**Fix (정정)**: REBORN.md / archive doc 에서 "TALK5 + ZERO4" 표기는 다음과 같이 분리:
- worktree-5 era: "ZERO4 = spec/commit msg only, code 부재"
- worktree-6 era: "ZERO4 = Φ-gated vocabulary runtime hook + bench (reproducible)"

honest C3: BG-LOSTASSET-C 의 "phantom" 결론은 worktree-5 single-worktree 검색의 artifact — 다른 worktree 추가 검색 시 reverse 가능 case 의 대표 예. 향후 cross-worktree 검색 norm 화 권고.

### 3.2 TALK5 99.7% CE drop — docstring only

train_conscious_lm.py docstring 에 "99.7% CE drop" claim 있지만 실제 ablation 코드 부재. external eval JSON 도 부재.

**Fix**: claim 을 "docstring claim, ablation evidence 부재" 로 정정. 본 doc + REBORN.md §17 (이미 BG-C report 기록).

### 3.3 5-channel meta-telepathy "100% True/False auth" — un-coded threshold

`tension_link.py` (worktree-9, 648L) 의 authenticity head 가 Sigmoid 0-1 scalar 출력. 이진 분류기 X. "100% auth" 는 threshold 미명시 — 코드 레벨 에서 보장 X.

**Fix**: claim 을 "Sigmoid scalar continuous, '100%' threshold un-coded — claim only" 로 정정.

### 3.4 AnimaLM v4 tension numbers — external only

`serve_animalm_v4.py` (worktree-7, 122L) 에서 mean_tension / savant_tension / SI=5.93 / 36.8% / alpha=0.0047 모두 print 포맷에만 있고 hardcoded value 부재. external ckpt + 별도 doc 에서 측정.

**Fix**: numbers 자체는 valid 하지만 reproducible code path 부재 → "external measurement, code-level reproduction 별도 lane" 로 정정.

### 3.5 savant ratio 명명 충돌

`serve_animalm_v4.py`: 8 PureField branch 中 2 = savant → ratio = 2/8 = 0.25 (not 1/e). "Golden Zone 36.8%" 는 dropout value (DROPOUT_NORMAL=1/e=0.368) 인데 layer ratio 와 conflated 되어 표기됨.

**Fix**: 명명 정정 — Golden Zone 36.8% = dropout p, NOT savant layer ratio.

---

## §4 fix 적용 우선순위

| 순위 | fix | 적용 대상 | 비용 |
|---:|---|---|---:|
| 1 ★★★ | `_expand_dim` block weight partial copy | growing_conscious_lm.py 사용 시 (별도 cycle 재학습 시) | $0 ref + $H100 retrain |
| 2 ★★ | GROWTH_STAGES alignment with growth_engine.STAGES | growing_conscious_lm.py 사용 시 | $0 |
| 3 ★ | doc-only phantom claim 정정 | REBORN.md / archive docs | $0 (본 doc 에 기록) |

본 doc 는 fix reference + honest C3. 실제 worktree archive 수정 X (raw#15). reference py 는 `state/anima_lost_asset_fixes_2026_05_10/` 에 보존.

---

## §5 honest C3 (≥7)

1. 본 fix 의 `_expand_dim` partial copy 가 정확하게 historical H371 결과 (43→99% retention, RC-9 +52.76%) 를 reproduce 한다는 보장 X. fix 자체도 검증 필요.
2. PureFieldFFN 의 d_inner = 4×d expansion 가정 — original code 와 일치하지만 future variant 시 mismatch risk.
3. tied weight (tok_emb.weight = head_a.weight) 가 fix 후에도 동일하게 작동하는지 별도 검증 필요 — head_a 가 새 객체로 생성되면 tying re-establish 필요 (본 fix 는 reassignment 으로 처리).
4. attention bias buffer (`register_buffer("bias")`) 는 별도 처리 안 함 — block_size 변경 없으면 OK, 변경 시 재등록 필요.
5. STAGE alignment 권장값 (newborn=0/infant=100/toddler=500/child=2000/adult=10000) 은 growth_engine 의 발달 심리학 매핑 — historical mitosis (50/200/800) 가 RC-9 +52.76% 의 evidence 시점일 수 있음. alignment 후 historical 결과 reproducibility 미검증.
6. ZERO4 phantom finding 은 BG-LOSTASSET-C 의 worktree-5 검색 결과 — 다른 worktree (e.g., 6, 7) 에 ZERO4 가 있을 가능성 미배제 (전체 13 worktree 검색 미완).
7. "100% True/False auth" 가 un-coded threshold 라는 finding 은 authenticity head 만 본 결과 — TL2 / TL3 / TL5 sender ID 등 다른 channel 의 일부 가 binary classifier 일 가능성 미배제.
8. 본 fix 의 적용 대상 = worktree-2 v2-era code. 현재 reborn lane (track A/B/C) 는 별도 architecture (Engine A/G v5 350M, byte-level decoder). fix 가 reborn 본진 에 직접 영향 X — 단 v5-mitosis (track C) cells = nn.Module 설계 시 본 fix pattern 참조 가치.

---

## §6 cross-link

- BG-LOSTASSET-B report → REBORN.md §16 (이미 append)
- BG-LOSTASSET-C report → REBORN.md §17 (이미 append)
- 본 fix doc → REBORN.md §20 [2026-05-10 HH:MM KST] append (이 cycle close 시)
- worktree-2 source: `/Users/ghost/core/anima_clm_02_clm_pivot/growing_conscious_lm.py`
- conscious_lm.py (PureFieldFFN + ConsciousBlock 정의): `/Users/ghost/core/anima_clm_02_clm_pivot/conscious_lm.py`
- fix reference py: `state/anima_lost_asset_fixes_2026_05_10/growing_conscious_lm_expand_dim_fix.py` (`**/*.py` gitignored, local-only)
- archive 무결성: worktree-2 (`archive/clm-stage-02-clm-pivot` branch) 직접 수정 X — raw#15 additive

raw#9/10/15 honest preservation, raw#37 additive, own 16 0-cost.

End of `anima_lost_asset_fixes_2026_05_10.md`.
