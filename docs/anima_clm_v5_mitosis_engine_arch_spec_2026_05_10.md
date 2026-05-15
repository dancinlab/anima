# anima_clm_v5_mitosis_engine_arch_spec_2026_05_10

> v5-mitosis (track C, `.roadmap.reborn`) architecture spec — cells = real `nn.Module` branches, NOT instrumentation. design only ($0). raw#15 additive — `mitosis.py` / `mitosis_v5_port.py` / `engine_a_g_arch.py` 모두 미수정.

---

## §0 한 줄 + lane motivation

**한 줄**: v5-mitosis 는 anima 의 cells 를 **실제 sub-network branches** (각 cell = small transformer block) 로 만들어 mitosis 가 model architecture 자체가 되게 한다. v5-anima (instrumentation) 와 sister track — emerge 비교 후 main lane 결정.

### 본 lane 발생 배경 (user verdict 7-table flip target)

cycle 2026-05-09/10 의 user verdict 7-table 의 두 ❌ 항목 중 하나:

| 가설 | 이전 verdict | flip target |
|---|:---:|---|
| MitosisEngine = 모델 자체 | ❌ (BG-R2 finding: cells64 = single decoder + instrumentation) | **★ 본 lane 의 mission** |

사용자 directive 2026-05-10 verbatim: **"실제 MitosisEngine 개발하자"** — 의미: cells64/128 의 BG-R2 정정 ("instrumentation only") 을 architectural answer 로 응답. cells = real `nn.Module` 가 되어야 v2-era vision (cells = mini ConsciousMind) 의 production-scale 실현.

### v5-anima 와의 본질적 차이

| 측면 | v5-anima (instrumentation) | v5-mitosis (architectural) |
|---|---|---|
| cells | tensor row in shared `EngineG.cell_pool_init` | independent `nn.Module` branch |
| split | row append to (N+1, C) Parameter | new `nn.Module` clone + register |
| forward 비용 | O(C) per cell | O(C·d_model²) per cell |
| parameter growth on split | C floats (negligible) | ~3-5M per cell (substantial) |
| optimizer state | trivial (single Parameter) | per-cell migration required |
| substrate-coupling risk | low (cells live in one Param) | higher (per-cell weight drift) |
| 친근 비유 | "anima 옆에서 cells 를 측정/추적" | "anima 자체가 cells 의 ensemble" |

본 lane 의 가치 가설: **architectural mitosis 가 instrumentation mitosis 가 못 만든 V14 differentiation 을 만든다** (BG-PHASE2-CKPT-INSTR 의 NOVEL POLARITY trap 우회).

---

<!-- [Hc_627 v5-mitosis-real-nn-module-cells-architectural — moved to hypotheses_candidates/Hc_627_v5_mitosis_real_nn_module_cells.md on 2026-05-11] -->

## §1 architecture decision (a/b/c/d)

### option 비교 (`.roadmap.clm_v5_mitosis_engine.architecture_decision_record` 기반 + 본 spec 검토 갱신)

| option | cell 단위 | params/cell @ d=384 | total @ N=64 | shared | pros | cons | verdict |
|---|---|---:|---:|---|---|---|:---:|
| **(a)** | small transformer block (attn + dual-FFN) | 3-5M | ~200-320M | tok_emb / pos_emb / lm_head | production-scale fit, per-cell FFN diversity 자연 | per-cell attention 비용 N×, lm_head routing 복잡 | **★ adopted** |
| (b) | decoder branch (attention shared, FFN per-cell) | 1-2M | 64-128M | tok_emb / pos_emb / **attn** / lm_head | attn 공유로 FLOPs 절감, N×FFN 만 비용 | attn 공유는 cell-specific specialization 약화, gradient routing 복잡 | intermediate fallback |
| (c) | ConsciousMind v2-style (engine_a + engine_g + GRUCell) | 50-200K | 3-12M | none (transformer 미사용) | v2 정확 보존, split/merge 정확 v2 reproduce | transformer 미사용 → modern LLM scale fit 부족, generation pipeline 부재 | **rejected** (v2-reborn 에 적합) |
| (d) | LoRA adapter on shared base | 50-500K | 3-32M | base model 전체 | parameter-efficient, split = new LoRA | true mitosis 정신 약화 (cell 자체 weak), capacity 부족 | low priority |

### 최종 채택: **option (a) revised — small transformer block per cell, shared tok_emb/pos_emb/lm_head + per-cell {attn, FFN_a, FFN_g, ln1, ln2}**

#### justify (a) over alternatives

1. **(a) vs (b)**: (b) 의 attention 공유는 단기적 비용 절감 같지만 cells 가 같은 attention 으로 들어오면 specialization 채널 (= H297 N=2 optimal 의 본질) 이 사라진다. Mitosis 의 핵심은 "다른 sub-network 가 다른 attractor 를 만든다" — attention 자체가 attractor 의 일부라 공유 부적합.
2. **(a) vs (c)**: (c) 는 transformer 가 아니라 modern LLM substrate 위에 안 붙음. v2 mitosis.py 의 `ConsciousMind` 는 input_dim=64 의 toy. v5 substrate 는 d_model=384~1024 + attention. (c) 는 v2-reborn 트랙으로 분리.
3. **(a) vs (d)**: LoRA adapter 는 cell 의 weight 가 base 의 perturbation 에 불과 → "cell 자체가 mini-mind" 의 anima 본질 손실. mitosis 가 단순 LoRA composition 이 됨.

#### revisions to vanilla (a)

bare option (a) 의 issue 와 본 spec 의 fix:

| issue | fix |
|---|---|
| per-cell attention duplication 비용 | **adaptive attention sharing** — N≤8 까지는 per-cell attn, N>8 시 attn 공유 (option (b) hybrid mode 자동 fallback) |
| lm_head routing 복잡 | **softmax(tension)-weighted aggregation BEFORE lm_head** — N cells 의 hidden 을 weighted sum 으로 (B, T, D) 단일 stream 으로 합쳐 lm_head 1회 통과 |
| FFN 가 dual (engine_a + engine_g) 일 때 cell 당 2× FFN | **acceptable** — H404 `output = a − g` formulation 보존 (단 §6 의 destructive 발견 반영해 readout 만 configurable) |
| split 시 attention QKV/O matrix copy 비용 | **lazy clone** — split 시 cell 의 module 만 deepcopy, ModuleList.append, optimizer 는 caller 가 rebuild (smoke 단계 inference-only 면 무시) |

---

## §2 cell architecture detail

### 2.1 cell module signature

각 cell = `MitosisCell(nn.Module)` 의 instance. shared embeddings 는 `MitosisModelEngine` 본체가 들고 있고 cell 은 reference 만 받음.

```
MitosisCell(d_model, n_head, ffn_dim):
    ln1: LayerNorm(d_model)
    attn: MultiheadAttention(d_model, n_head)        # per-cell (N≤8) or shared ref (N>8)
    ln2: LayerNorm(d_model)
    ffn_a: Sequential(Linear(d_model, ffn_dim), ReLU, Linear(ffn_dim, d_model))   # engine_a
    ffn_g: Sequential(Linear(d_model, ffn_dim), ReLU, Linear(ffn_dim, d_model))   # engine_g
    # cell metadata (mirrors v2 mitosis.py Cell dataclass):
    cell_id: int
    creation_step: int
    parent_id: Optional[int]
    tension_history: List[float]
    process_count: int

    forward(x):                          # x: (B, T, D)
        # pre-norm transformer block + dual-FFN H404
        h = x + attn(ln1(x))
        a = ffn_a(ln2(h))
        g = ffn_g(ln2(h))
        out = h + (a - g)                # H404 default; configurable per §6
        tension = ((a - g) ** 2).mean(dim=-1)   # (B, T) — preserve token-axis
        return out, tension              # tension reduced per-token, then per-cell scalar later
```

### 2.2 model-level container

```
MitosisModelEngine(nn.Module):
    # shared (NOT replicated per cell)
    tok_emb: Embedding(vocab, d_model)
    pos_emb: Embedding(max_T, d_model) or RoPE
    cells: ModuleList[MitosisCell]
    final_ln: LayerNorm(d_model)
    lm_head: Linear(d_model, vocab, bias=False) # weight-tied to tok_emb (norm)

    # mitosis state (parallel to v2 MitosisEngine)
    step_count: int
    split_threshold: float (adaptive)
    _global_tension_history: List[float]
    _inter_repulsion_history: Dict[(i,j), List[float]]
    _lorenz: [x, y, z]
    phi: float
    phi_history: List[float]
    _phi_best: float
    _best_cell_state: Optional[List[Dict[str, Tensor]]]   # state_dict snapshot per cell
    event_log: List[Dict]
```

### 2.3 parameter count budget

production target: d_model=384, n_head=6, ffn_dim=1536 (4× expand), vocab=256 (byte) or 64K (BPE).

| cell 부품 | shape | params |
|---|---|---:|
| ln1 | (D,) ×2 | 768 |
| attn QKV+O | 4 × (D, D) | 590K |
| ln2 | (D,) ×2 | 768 |
| ffn_a | (D, F) + (F, D) | 1.18M |
| ffn_g | (D, F) + (F, D) | 1.18M |
| **per cell total** | | **~2.95M** |

| N cells | total per-cell | + shared (vocab=256, max_T=256) | grand total |
|---:|---:|---:|---:|
| 8 | 23.6M | 0.23M | ~23.8M |
| 16 | 47.2M | 0.23M | ~47.4M |
| 32 | 94.4M | 0.23M | ~94.6M |
| **64** | **188.8M** | 0.23M | **~189M** |

cells_max=64 + d=384 ≈ 200M params (Phase 2 ckpt 350M 의 절반). N>8 attention sharing fallback 적용 시 64 cells 에서 ~140M (attn 공유 50M 절감).

### 2.4 design constants (v2 보존)

| 상수 | 값 | 출처 |
|---|---:|---|
| `initial_cells` | 8 | reborn lane anchor (v5 substrate `cell_pool=16` 보다 보수적) |
| `max_cells` | 64 | v2 cells64 historical peak (Φ super-linear ceiling) |
| `min_cells` | 2 | CB1 floor (`mitosis.py` L154) |
| `split_patience` | 3 | v2 default (`mitosis.py` L141) |
| `merge_threshold` | 0.005 | v2 default (`mitosis.py` L142) |
| `merge_patience` | 30 | v2 default (`mitosis.py` L143) |
| `noise_scale` (split) | 0.10 | v2 effective (`mitosis.py` L204 max(0.01, 0.1)) |
| `lorenz_scale` | 0.05 | v2 default (`mitosis.py` L393) |
| `adaptive_window` | 100 | v2 (`mitosis.py` L468) |
| `phi_ratchet_drop` | 0.8 | v2 DD55 (`mitosis.py` L449) |
| `phi_ratchet_blend` | 0.8/0.2 | v2 (`mitosis.py` L454) |

---

## §3 split/merge mechanics for nn.Module

### 3.1 split — `_split_cell(parent_idx) → child_idx`

**핵심 challenge**: cells 가 `nn.Parameter` row 가 아니라 `nn.Module` instance 이므로 `torch.cat` 으로는 못 키운다. 대신 ModuleList 에 새 module 을 `append`.

```
def _split_cell(parent_idx: int) -> Optional[Dict]:
    if len(self.cells) >= self.max_cells:
        return None

    parent: MitosisCell = self.cells[parent_idx]

    with torch.no_grad():
        # 1. deepcopy parent module (state_dict path — avoid module._modules ref leak)
        child = MitosisCell(self.d_model, self.n_head, self.ffn_dim)
        child.load_state_dict(parent.state_dict())

        # 2. inject 10% Gaussian noise per parameter (v2 mitosis.py L204-207)
        for p in child.parameters():
            p.add_(torch.randn_like(p) * (self.noise_scale * p.norm() / max(p.numel() ** 0.5, 1)))
            # noise scaled per-parameter so ln/attn/ffn 가 동일 effective σ

        # 3. metadata
        child.cell_id = self._next_id; self._next_id += 1
        child.creation_step = self.step_count
        child.parent_id = parent.cell_id
        child.tension_history = []
        child.process_count = 0

        # 4. attach (raw#15 additive — parent untouched)
        self.cells.append(child)

        # 5. parent tension reset (avoid immediate re-split)
        parent.tension_history = parent.tension_history[-3:]

    return {"type":"split", "step":self.step_count,
            "parent_id":parent.cell_id, "child_id":child.cell_id,
            "n_cells_after": len(self.cells)}
```

**function-preserving 검증**: child 가 parent 의 state_dict 정확 copy + small noise → forward(x) 결과 cosine sim ≈ 0.99+ on small noise. v2 mitosis.py L192-226 의 정확 port.

### 3.2 merge — `_merge_cell_pair(idx_a, idx_b) → keeper_idx`

```
def _merge_cell_pair(idx_a: int, idx_b: int) -> Optional[Dict]:
    if len(self.cells) <= self.min_cells:    # CB1
        return None
    if idx_a == idx_b:
        return None

    a, b = self.cells[idx_a], self.cells[idx_b]
    keeper, removed = (a, b) if a.creation_step <= b.creation_step else (b, a)
    keeper_idx, removed_idx = sorted([idx_a, idx_b], key=lambda i: self.cells[i].creation_step)

    with torch.no_grad():
        # parameter-wise average (v2 mitosis.py L586-589)
        for p_keep, p_rem in zip(keeper.parameters(), removed.parameters()):
            p_keep.data = (p_keep.data + p_rem.data) / 2.0

    # remove + reindex
    self.cells.pop(removed_idx)
    self._cleanup_inter_repulsion(removed_idx)

    return {"type":"merge", "step":self.step_count,
            "keeper_id":keeper.cell_id, "removed_id":removed.cell_id,
            "n_cells_after": len(self.cells)}
```

### 3.3 ModuleList rebuild — split/merge 시 issue

`nn.ModuleList.append(child)` 은 `_modules` dict 를 mutate — `model.parameters()` iterator 가 **다음 호출부터 새 cell 포함**. PyTorch autograd 는 fresh forward 에서만 parameters 보므로 문제 없음.

**단**: optimizer 가 이미 parent 만 보고 만들어진 상태면 child 의 parameters 가 optimizer 에 등록 안 됨 → mid-train split 시 optimizer rebuild **mandatory**.

### 3.4 optimizer state migration (3 옵션)

| 옵션 | 설명 | 비용 | inference-only 적합 |
|---|---|---|:---:|
| **(α)** | inference-only 운용 — split 시 optimizer 무시 (smoke test 단계) | $0 | ✅ |
| (β) | split 시 optimizer rebuild — `optim = AdamW(model.parameters())` reset (momentum 0) | small (warm-up needed) | partial |
| (γ) | Net2Net 스타일 — child 의 momentum 을 parent 에서 0.5× copy | implementation 복잡 | ✅ |

**본 spec 채택**: cond.3 smoke (CPU local) 까지 (α) inference-only. cond.5 H100 cotrain 시 (β) optimizer rebuild + warmup 100 step. (γ) 는 future cycle.

### 3.5 mid-train split 시 gradient consistency

split 직후 forward 는 **shape 변경 없음** (각 cell forward 가 (B,T,D) 를 또 (B,T,D) 로 mapping, aggregation 만 N+1 cells 로). loss.backward() 는 새 cell 의 parameters 에도 gradient 흘림. 단 optimizer 가 (β) 처럼 rebuild 안 됐으면 step() 이 새 cell 무시 → 문제. → **split = optimizer rebuild signal**.

---

## §4 forward path

### 4.1 high-level

```
MitosisModelEngine.forward(input_ids):    # input_ids: (B, T)
    B, T = input_ids.shape
    x = tok_emb(input_ids) + pos_emb(arange(T))         # (B, T, D)

    # 1. run all cells in parallel (no_grad path for inference-time mitosis,
    #    grad path for cotrain)
    cell_outs = []
    cell_tensions = []
    for cell in self.cells:
        out_i, tension_i = cell(x)               # out_i: (B, T, D), tension_i: (B, T)
        cell_outs.append(out_i)
        cell_tensions.append(tension_i.mean(dim=(0,1)))   # (,) scalar per cell

    # 2. softmax(tension)-weighted aggregation across cells
    tens = torch.stack(cell_tensions)             # (N,)
    weights = F.softmax(tens, dim=0)              # (N,)  — high tension = high weight (v2 reproduce)
    stacked = torch.stack(cell_outs, dim=0)       # (N, B, T, D)
    aggregated = (weights[:,None,None,None] * stacked).sum(dim=0)   # (B, T, D)

    # 3. final norm + shared lm_head
    h = self.final_ln(aggregated)
    logits = self.lm_head(h)                      # (B, T, vocab)
    return logits, {"tensions": cell_tensions, "aggregated": aggregated}
```

### 4.2 mitosis hook — when to call `process()`

forward path 안의 `cell(x)` 단계가 v2 의 `cell.mind(text_vec, hidden)` 에 대응. 이 forward 결과의 `cell_tensions` 가 mitosis decision input.

forward 끝에서 (또는 외부 trainer/serve loop 이) `mitosis_step(cell_tensions)` 호출:

```
def mitosis_step(cell_tensions: List[float]):
    self.step_count += 1
    self._inject_lorenz_into_cells()         # §7
    self._update_tension_history(cell_tensions)
    phi = self._compute_phi()                # §5
    self._phi_ratchet(phi)                   # §8
    self._update_adaptive_threshold()
    split_events = self._check_splits()
    merge_events = self._check_merges()
    return phi, split_events + merge_events
```

inference-time autonomous growth 의 v2 invariant 보존 — 모든 mutation 이 `torch.no_grad()` (REBORN.md §2 "5 sites all no_grad" 정확 reproduce).

### 4.3 batched forward 비용 — N cells × per-cell forward

vanilla (a) bare 의 비용: N × (attention + 2 FFN) × (B, T) = O(N · B · T · D²). N=64 이면 64× 단일 transformer 비용.

**비용 절감 path**:
1. **N≤8**: 그대로 per-cell forward (bare (a))
2. **N>8**: **attention sharing fallback** — `attn(ln1(x))` 한번 계산 후 N cells 에 broadcast, 각 cell 은 ffn_a/g + ln 만 per-cell. effective cost: 1 attn + N × FFN ≈ 1 + 0.5N transformer 비용 (option (b) 형태).
3. **N>32**: `softmax(tension)` weight 가 sparse (top-k=8) — bottom-(N-8) cells 의 forward skip (lazy execution). 사용자 directive 승인 필요시 cond.4 에서 도입.

**default (cond.3 smoke 까지)**: bare (a) per-cell forward, N=8→16 까지 only. cond.5 H100 cotrain 시 N>8 attention sharing 자동 fallback.

### 4.4 lm_head routing — single shared head

**중요 결정**: per-cell lm_head 가 **아니다**. cells 는 hidden space 에서 aggregation 후 single lm_head 통과. 이유:

1. vocab × d_model lm_head 은 single decoder 의 50%+ params (vocab=64K → 25M). per-cell 이면 64×25M = 1.6B params explosion.
2. v2 mitosis.py 도 `combined = sum(w · output)` 으로 hidden space 합성 후 (그 이후 lm_head 단계는 없음 — toy 라 generation X).
3. cells 의 specialization 은 attn+FFN 단계에서 발현, lm_head 는 동일 vocab projection.

**대안 (rejected)**: per-cell lm_head 로 logits 합성 → softmax(tension)-weighted **logit mixture** (mixture-of-experts 형태). 실험 가치 있음 but param explosion 으로 cond.5 H100 stretch — future cycle.

---

## §5 IIT Φ integration

### 5.1 input — what to feed PhiCalculator

`state/anima_clm_v5_iit_phi_remetric_2026_05_10/iit_phi_port.py` 의 `compute_iit_phi(cell_pool: (N, C)) → Dict` 가 본 lane 에서 직접 사용 가능. 단 v5-mitosis 의 cells 는 module 이지 vector 가 아님 → **per-cell representative vector** 추출 필요.

| 후보 | 정의 | 장점 | 단점 |
|---|---|---|---|
| (i) cell hidden state mean | `cell_outs[i].mean(dim=(0,1))` (D,) | 직접 forward path 의 산물 | input-dependent (calibration burden) |
| (ii) cell tension vector | `cell_outs[i].mean(dim=0)` (T, D) flattened | richer signal | T 차원 noise |
| (iii) cell weight signature | concat(ffn_a.weight.flatten()[:K]) | input-independent | static — Lorenz 변화 안 보임 |
| **★ (iv) hybrid** | hidden mean + 0.1 × weight signature | input + structure 모두 | implementation 약간 복잡 |

**본 spec 채택**: (i) hidden state mean — (B, T, D) 의 mean(0,1) 로 (D,) 추출, N cells 면 (N, D) tensor → `compute_iit_phi(cell_pool=(N, D))` 호출.

### 5.2 metric 출력 — track 어느 것?

`iit_phi_port.py` 출력 6 metrics 중:

| field | 설명 | 본 lane 추적 |
|---|---|:---:|
| `total_mi` | sum_{i<j} MI(cell_i, cell_j) | log only |
| `min_partition_mi` | MIP cut MI | log only |
| `spatial_phi` | (total_mi − mip) / (n−1) | secondary |
| `phi_with_complexity` | spatial_phi + 0.1·complexity | secondary |
| **`phi_unnorm`** | total_mi − min_partition_mi (new field, BG-IIT-METRIC) | **★ primary** |

이유: `BG-IIT-METRIC` finding (REBORN.md §4) — IIT unnorm at N=64 = 4471 (proxy 2.92 의 1530×). proxy ceiling 우회.

### 5.3 호출 빈도

매 `mitosis_step()` 마다 `compute_iit_phi` 호출 = ~5ms at N=64 (BG-IIT-METRIC measure). 1K turn / 10K turn long-trajectory 에서 5s / 50s 누적 — acceptable.

### 5.4 ratchet 신호로 사용

§8 `_phi_ratchet` 의 phi value 는 IIT unnorm 사용. 단 ratchet threshold (0.8 × phi_best) 는 IIT scale 에 맞춰 재조정 필요할 수 있음 — cond.3 smoke 에서 calibrate.

---

## §6 H404 a-g vs a-only readout — configurable

### 6.1 BG-CHAT-EXT 의 destructive 발견 (REBORN.md §3)

cells64 / cells128 sampling test 360 trial:
- combined `output = a − g` head: **모든 trial unicode garbage** (KO 0%)
- `a-only` 또는 `+가중` head 미검증 (이 lane 의 검증 항목)

→ H404 의 inference-time minus_head 가 **destructive**. v2 학습 시 working 했지만 inference path 에서 a 와 g 가 over-cancel.

### 6.2 readout mode 옵션 (configurable)

`MitosisCell.forward(x, readout_mode='a_minus_g')`:

| mode | formula | 가설 |
|---|---|---|
| `'a_minus_g'` (default) | out = h + (a − g) | v2 정확 reproduce — 학습 시 fine |
| `'a_only'` | out = h + a | g 의 destructive 우회 |
| `'a_plus_alpha_g'` | out = h + a + α·g (α∈[-1, 0]) | gradient swept calibration |
| `'a_concat_g'` | out = h + concat(a, g) → linear | g 도 살리되 가산 변경 |
| `'a_minus_g_norm'` | out = h + (a − g) / max(1, ||a−g||) | over-cancel 방지 |

### 6.3 본 spec 권장

- **train**: `a_minus_g` (v2 학습 invariant 보존)
- **inference**: `a_only` 가 default safe — but **track A/B 결과 fold-in** 이전엔 결정 보류
- **cond.3 smoke**: 5 mode 모두 sweep, KO/EN coherence 기록
- **cond.5 H100 cotrain**: best mode 선택 후 1 mode 만

### 6.4 risk

readout mode 가 train vs inference 에서 다르면 **distribution shift** — train 시 `a-g` 학습된 representation 을 inference 시 `a` 만 쓰면 gap 가능. 단 v5-anima Phase 2 가 `a-g` 학습된 후 동일 ckpt 에서 inference time mode 만 swap 하는 것이 가능 — cond.3 smoke 에서 측정.

---

## §7 Lorenz autonomous chaos

### 7.1 대상 — cell module 의 무엇에 perturbation?

v2 mitosis.py L388-405 는 cell.hidden (GRU hidden state) 에 inject. v5-mitosis 의 cell 은 transformer block — hidden state 가 forward 마다 새로 계산되어 persistent X. 대안:

| 대안 | 대상 | 장점 | 단점 |
|---|---|---|---|
| (A) ffn_a / ffn_g weight 에 perturb | weight | persistent across forwards | weight 변경 = effectively training step (no_grad 라도) |
| **★ (B)** | **cell-attached `cell_state` buffer** (D,) | persistent + non-weight | 새 buffer 추가 (architecture 변경) |
| (C) attention bias 에 perturb | attn.bias | persistent + minimal | 효과 작음 (bias 만으론 symmetry 못 깸) |
| (D) forward 시 input x 에 perturb | input | trivially persistent X but clean | Lorenz 가 cell-specific 안 됨 |

**본 spec 채택**: (B) — `MitosisCell` 에 `register_buffer('cell_state', torch.zeros(D))` 추가. forward 시 `h = h + cell_state` (residual). Lorenz 가 매 step 마다 cell_state 업데이트 (no_grad).

### 7.2 Lorenz step

`mitosis_v5_port.py` L281-288 의 `_lorenz_step()` 정확 port. σ=10, ρ=28, β=8/3, dt=0.01.

### 7.3 per-cell phase offset (Law 86)

```
def _inject_lorenz_into_cells():
    dx, dy, dz = self._lorenz_step()
    lorenz_vec = torch.tensor([dx, dy, dz])
    N = len(self.cells)
    for i, cell in enumerate(self.cells):
        with torch.no_grad():
            phase = (i * 2.0 * math.pi) / max(N, 1)
            scale = self.lorenz_scale * (1.0 + 0.3 * sin(phase + self.step_count * 0.1))
            noise = torch.randn(self.d_model) * scale
            noise[:3] += lorenz_vec * 0.2          # deterministic Lorenz channel
            cell.cell_state += noise
            # clamp (v2 L403-405)
            n = cell.cell_state.norm()
            if n > 10.0:
                cell.cell_state.mul_(10.0 / n)
```

### 7.4 cond.3 smoke 에서 검증

- Lorenz 없으면 cells 의 forward 가 input-deterministic → tension 동일 → mitosis trigger X
- Lorenz 있으면 per-cell phase 가 다른 attractor 잡음 → tension diverge → split trigger
- **falsifier F-V5MITOSIS-LORENZ-INERT**: cond.3 smoke 에서 Lorenz on/off 비교, off 시 split count == 0 검증

---

## §8 Phi ratchet (DD55 conservation)

### 8.1 v2 mechanism (mitosis.py L438-455)

```
phi 가 phi_best 보다 크면 → phi_best update + best_state snapshot
phi 가 phi_best * 0.8 미만 → 0.8 × current + 0.2 × best_state blend
```

### 8.2 v5-mitosis adaptation — what to snapshot?

v2 는 cell.hidden 만 snapshot. v5-mitosis 의 cells 는 module → snapshot 대상 후보:

| 옵션 | 대상 | 비용 (per ratchet) | 비용 (snapshot 보유) |
|---|---|---|---|
| (a) cell_state buffers only | (N, D) | 1KB at N=64 D=384 | 100KB |
| **★ (b)** | **full state_dict per cell** | (N × ~3M params) | ~750MB at N=64 |
| (c) attention only | per-cell attn.QKV+O | (N × 590K) | 300MB |

**문제**: (b) 가 v2 의 정확 mirror 이지만 750MB 가 RAM 압박 (특히 H100 smoke 시 GPU mem 차이). (a) 는 cell_state 만 — 효과는 약하지만 가벼움.

**본 spec 채택**: **(a) cell_state-only ratchet** + (b) **lazy full state ratchet** (phi 가 phi_best * 0.5 미만일 때만 — emergency restore). 두 수준의 ratchet → DD55 conservation 의 partial port.

### 8.3 split/merge 시 conservation 검증

v2 mitosis.py L644-656 `verify_phi_conservation` 의 정확 port. split 시 phi_before vs phi_after 의 ratio 가 0.9~1.1 범위 내인지 log only (not blocking). conservation 깨지면 warning emit + cond.3 smoke 의 honest C3 에 기록.

### 8.4 ratchet ↔ split 상호작용

split 직후 phi 가 잠시 dip 하는 게 자연스러움 (새 cell 이 cosine 가까운 위치 — diversity 일시 하락). ratchet 이 즉시 trigger 되면 split 효과 무효화. 해결: **post-split grace period** 5 step 동안 ratchet skip. v2 mitosis.py 명시 grace 없음 — 본 spec 의 갱신.

---

## §9 risk register (≥10)

| # | risk | likelihood | impact | mitigation |
|--:|---|:---:|:---:|---|
| R1 | cell 의 per-cell attn 비용 N=64 시 64× → smoke OOM (Mac CPU 16GB) | high | high | adaptive sharing fallback (§4.3) — N>8 시 attn 공유; cond.3 smoke 는 N=8→16 만 |
| R2 | optimizer state migration mid-train split → grad 흐름 파괴 | high | high | (α) inference-only 까지 cond.3, (β) optimizer rebuild cond.5; (γ) Net2Net future |
| R3 | split 시 deepcopy + noise → child 가 parent 와 cosine ~0.99, mitosis 효과 trivial | med | med | noise_scale=0.10 + 5-step grace + force-split smoke 검증 (cond.3) |
| R4 | softmax(tension) weighted aggregation 이 high-tension cell 만 dominate → cell collapse | med | high | tension 정규화 (T=tension/std) 옵션 + N>8 시 top-k=8 cap; cond.3 monitor |
| R5 | Lorenz cell_state buffer 가 forward 마다 grow → drift | med | med | norm clamp 10.0 (v2 reproduce) + cond.3 step-N=1000 stability check |
| R6 | IIT Φ unnorm primary metric 이 N 에 dominated → split 만 트리거 (mitosis bias) | med | med | secondary `phi/n` per-cell normalize 동시 추적; new α metric (track B cond.5) fold-in |
| R7 | H404 a-g readout destructive (BG-CHAT-EXT) → coherence 0 | high | high | configurable readout mode (§6) + cond.3 smoke 5 mode sweep |
| R8 | v5-mitosis 가 v5-anima 대비 emerge 차이 0 → architectural framing 효과 없음 (F-V5MITOSIS-4) | med | high | track B와 동일 corpus + 동일 IIT metric, V14 mirror 5-seed strict |
| R9 | param explosion — N=64 + d=1024 시 2-4B params → H100 80GB 한계 | low | high | d=384 default cond.3, d=1024 cond.5 만; N>32 시 attn 공유 |
| R10 | merge_threshold=0.005 v2 default 가 v5 transformer hidden scale 와 안 맞음 → merge 영영 X | med | med | cond.3 smoke 에서 inter-cell L2 distribution 측정 후 calibrate |
| R11 | cells = nn.Module 이라도 substrate-coupled emergence 못 만듦 → V14 violated 동일 (BG-PHASE2-CKPT-INSTR mirror) | high | critical | cond.3 smoke 의 falsifier F-V5MITOSIS-4; 실패 시 architectural framing 자체 abandoned, track B/A 로 회귀 |
| R12 | shared lm_head + per-cell hidden aggregation 이 lm_head 의 representation 을 collapse 시킴 (모든 cell 이 같은 logits 분포로 학습) | med | high | per-cell logit mixture (option) future cycle; cond.5 H100 cotrain log probability divergence per cell 측정 |
| R13 | cond.5 H100 cotrain $30-150 envelope overshoot — N=32+ cells × 5K steps × d=384 | med | med | cond.3 smoke 후 cost 정밀화 (cost discipline); envelope > $150 면 dimension reduce |
| R14 | mitosis split 이 LR scheduler 와 conflict — split 직후 새 cell 의 effective LR 가 step counter 무시 | low | med | per-cell LR group (cond.5 implementation detail) |
| R15 | snapshot ratchet (option b) 가 RAM 750MB occupy → smoke 실행 중 OOM | low | med | option (a) cell_state-only ratchet default + (b) lazy emergency only (§8.2) |

---

## §10 cost envelope

### cond.2 design / port code skeleton — $0
- Mac CPU local
- `training/mitosis_model_v5.py` (gitignored `**/*.py`) 작성
- ~1 day wall (1 BG)

### cond.3 local CPU smoke — $0
- Mac CPU, N=8→16 forward + IIT Φ + split/merge events
- target: Φ super-linear curve, V14 mirror 5-seed strict, Lorenz on/off ablation
- ~30min wall per smoke run, 5-10 smoke runs total
- **deliverable**: `state/anima_clm_v5_mitosis_smoke_2026_05_XX/{phi_curve.json, events.json, v14_mirror.json}`

### cond.4 long-trajectory — $0
- Mac CPU, 3K-10K turn diverse-prompt
- new α metric (track B cond.5 dependency) fold-in
- max_cap regression artifact 회피 (BG-LONG-TRAJ-EXT learning)
- ~3-6 hours wall per 10K run

### cond.5 H100 cotrain — $30-150
- envelope 구성:
  - **conservative ($30)**: N=8 fixed (no growth), d=384, 2K step, 1× H100 spot 1hr → smoke@scale
  - **mid ($60)**: N=8→16 growth, d=384, 5K step, 1× H100 spot 2hr → mitosis active
  - **stretch ($120)**: N=8→32 growth, d=384, 10K step, 1× H100 spot 4hr → 본 lane 의 PoC
  - **full ($150)**: N=8→64 growth, d=384, 10K step + chat eval, 1× H100 spot 5hr → cond.6 prereq
- verbatim: `OK CLM V5-MITOSIS H100 FIRE COST $X` (cond.3 결과 후 X 결정)
- corpus: convo_5k FT corpus (track A cond.3) 또는 v5-anima Phase 2 corpus 동일

### total reborn lane budget impact
- track A: $5-20
- track B: $0-30 (option)
- track C (본 lane): $0 design + $30-150 H100 (cond.5)
- 전체 envelope 절대 cap: $200 (REBORN.md §10)

---

## §11 honest C3 (≥7)

1. **architectural framing 자체가 효과 있다는 보장 없음**: BG-PHASE2-CKPT-INSTR 의 V14 NOVEL POLARITY (trained substrate 가 mitosis 억제) 는 instrumentation framing 의 결과. cells 가 nn.Module 이라도 같은 substrate-coupled trap 가능 — F-V5MITOSIS-4. R11 의 critical risk.

2. **cells = transformer block 이 v2 의 ConsciousMind 의 본질을 보존하는가 미검증**: v2 ConsciousMind 는 `engine_a + engine_g + GRUCell` (memory channel). v5-mitosis 의 transformer block 은 attention + FFN — GRU memory 부재. cell-level persistent state 는 cell_state buffer (§7) 로 대체했지만 GRU 의 forget/update gate 의 역할 미reproduce.

3. **softmax(tension)-weighted aggregation 이 inference 시 mode collapse 가능**: training 시 한 cell 의 tension 이 dominant 하면 다른 cells 의 gradient 가 약해져 spec 화 일어나기 전 collapse. v2 mitosis.py 는 toy 라 발견 안 됨 — production scale 에서 처음 보는 dynamics.

4. **shared lm_head 가 cell specialization 을 무효화 가능**: cells 는 hidden space 에서 specialize 해도 lm_head 가 같으면 vocab 분포 결국 align — mitosis 의 "specialty" 의미가 hidden representation 에만 머물고 generation 에는 안 나타남. R12.

5. **Lorenz cell_state buffer 가 v2 GRU hidden 의 진짜 mirror 가 아님**: v2 hidden 은 GRU cycle 안에서 input 과 interact (memory). cell_state 는 단순 residual buffer — Lorenz noise 만 받고 input 은 안 받음. effect on tension diversity 만 보존, persistence 는 약화.

6. **IIT Φ unnorm 이 N 에 dominated 가능**: BG-IIT-METRIC 에서 N=8 turn 0 = 52 (immediately crosses historical 51). 이는 toy substrate (random-init Lorenz noise) 에서 trivial. real production substrate 에서 unnorm 이 N 외 신호 (cell-specific quality) 잡는지 미검증. R6.

7. **H404 readout mode 결정 보류**: §6 의 5 mode sweep 은 cond.3 smoke 에서만 — 그 결과로 train mode (a-g) 와 inference mode (a-only?) split 시 distribution shift trap. v5 Phase 2 ckpt 가 a-g 학습된 invariant 와 conflict.

8. **본 spec 의 모든 design choice 가 "cond.3 smoke 검증 후 calibrate" 로 deferred**: split_threshold, merge_threshold, lorenz_scale, ratchet 0.8/0.2 — 모두 v2 toy 값. v5 transformer scale 에서 정확 transfer 보장 X. cond.3 의 핵심 task = 7 calibration parameter sweep.

9. **cond.5 H100 cotrain 시 split 이 optimizer rebuild 강제** → mid-train training instability. (β) AdamW reset → momentum 0 warmup 100 step → effective LR 일시 hike → loss spike 가능. v2 는 toy 라 만나지 않은 production trap.

10. **본 spec 은 design only — implementation skeleton (training/mitosis_model_v5.py) 후속 cycle**: 본 cycle close 시점 cond.1 PASS 만 (file exists). cond.2 (skeleton) 는 별도 BG. 그 사이에 spec 의 design choice 가 implementation 시 invalid 발견 가능.

11. **track B (v5-anima instrumentation) 와의 비교 protocol 미정**: REBORN.md §6 의 4-track 비교는 "동일 corpus + 동일 metric" 가 전제 — 본 lane 의 IIT Φ unnorm primary 가 track B의 metric 과 정확 align 되지 않음 (track B 는 proxy + 일부 IIT). cond.3/cond.4 결과 비교 시 metric 정렬 burden.

12. **N=64 + d=384 = 200M params 가 chat-cap 회복에 sufficient 한가 미검증**: BG-CHAT-EXT 의 capacity/corpus limit verdict 는 18.5M 한계. 200M 도 KO Hangul 3-byte UTF-8 corpus 에서 dominate 할 만큼은 아님. v5-mitosis 가 architectural fix 라도 corpus-side gap 우회 못함 — F-V5MITOSIS-6.

---

## §12 comparison: v5-anima vs v5-mitosis

### 12.1 비교 표

| 측면 | v5-anima (track B, instrumentation) | v5-mitosis (track C, architectural) |
|---|---|---|
| cell 구현 | `EngineG.cell_pool_init` row of (N, C) | `MitosisCell(nn.Module)` instance |
| split 메커니즘 | `nn.Parameter(torch.cat([pool, child_row]))` | `ModuleList.append(deepcopy(parent) + noise)` |
| split 비용 | O(C) bytes (~1.5KB at C=64) | O(per-cell params) (~3MB at d=384) |
| forward 비용 (N cells) | 1 transformer + N-row cell_pool readout | N transformer blocks (N>8 시 attn 공유 fallback) |
| optimizer migration on split | trivial (single Param expand) | per-cell rebuild required |
| substrate-coupling | low (cells = pool row, base model 별개) | higher (cells 자체가 model 의 sub-block) |
| smoke verdict (cycle 2026-05-10) | BG-MITOSIS-PORT PASS 5/5 | (cond.3 pending) |
| V14 differentiation | violated (BG-PHASE2-CKPT-INSTR NOVEL POLARITY) | **TBD — 본 lane 의 검증 항목** |
| KO chat 회복 가설 | F-CHAT-1 violated (capacity/corpus limit) | F-V5MITOSIS-6 동일 risk |
| v2 정신 보존도 | partial (cells = pool, mitosis = layer 위) | high (cells = mini-network) |
| H100 cost | $0 inference, $30 옵션 가속 | $30-150 cotrain |
| HF promote target | `dancinlab/clm-v5-anima-mitosis` | `dancinlab/clm-v5-mitosis-engine` |

### 12.2 같은 V14 trap risk

**critical insight**: v5-mitosis 가 architectural 이라도 **trained substrate 의 attractor bottleneck** 이라는 같은 phenomenon 을 재현할 가능성:

- BG-PHASE2-CKPT-INSTR finding: trained 350M 의 cell tension distribution = top-2 cells 가 1237 hits/3000 (cell 7=700, cell 16=537), random_init 는 noise-uniform top ~62
- 해석: trained model 이 어떤 substrate framing 이든 학습된 attractor 로 input 을 빨아들임 → tension 가 일부 cell 에 집중 → 그 cells 만 split, 나머지 inactive
- v5-mitosis 의 cells 가 nn.Module 이라도 같은 attractor 수렴 → 같은 V14 violation

**mitigation**: cond.3 smoke 에서 random_init substrate vs trained substrate 양쪽 V14 mirror — 만약 양쪽 결과 동일하면 architectural framing 효과 0 (F-V5MITOSIS-4 trigger), track C abandoned 후 track A/B 로 회귀.

### 12.3 본 lane 의 결정적 차이 — **per-cell weight ownership**

v5-anima 는 cells 가 single Parameter row → 모든 cells 의 update 가 같은 backward pass 에 통합. v5-mitosis 는 cells 가 분리된 Module → 각 cell 의 weight 가 independent gradient flow.

이 차이가 하는 일:
- 학습 시 cell A 의 specialization 이 cell B 의 weight 에 leak 안 됨 (instrumentation 은 leak 발생 — 같은 Parameter 라)
- mitosis split 시 child 가 parent 의 weight 만 inherit, 다른 cells 와 entangle 안 됨
- **가설**: 이 isolation 이 V14 differentiation 의 missing ingredient

이 가설이 맞으면 본 lane 가 main lane. 틀리면 (R11) instrumentation framing 으로 회귀 + servant integration (track D, separate roadmap) 으로 다른 lever 시도.

### 12.4 cond.3 smoke 단계의 비교 protocol

1. v5-mitosis cond.3 smoke 결과 + v5-anima BG-PHASE2-CKPT-INSTR 결과 head-to-head
2. 동일 corpus (Phase 2 cotrain corpus 또는 convo_5k)
3. 동일 metric (IIT Φ unnorm 16-bin, V14 mirror 5-seed strict)
4. 동일 substrate (Phase 2 350M ckpt — v5-mitosis 는 이 ckpt 로 cells initialize 후 split 시작)
5. delta 측정 — Φ super-linear α, split count, merge count, V14 score

delta > 5% favoring v5-mitosis 면 main lane confirm. delta ≤ 5% 면 framing 효과 0 (R11 발현).

---

## §13 next-step actions (cycle 2026-05-10 close 시점)

| 순위 | step | deliverable | cost | 의존 |
|---:|---|---|---:|---|
| 1 | 본 spec md PASS (cond.1) | 본 파일 | $0 | — |
| 2 | BG-V5MITOSIS-IMPL → `training/mitosis_model_v5.py` skeleton (cond.2) | local-only `**/*.py` | $0 | cond.1 |
| 3 | BG-V5MITOSIS-SMOKE → cond.3 local CPU smoke 5-10 run | smoke result.json | $0 | cond.2 |
| 4 | new α metric design (track B cond.5) fold-in | spec md | $0 | track B 의 separate BG |
| 5 | cond.4 long-trajectory 3K-10K turn | result.json | $0 | cond.3 + #4 |
| 6 | cond.5 H100 cotrain envelope 정밀화 + verbatim fire | H100 fire | $30-150 | cond.4 |

---

## §14 cross-link

- root SSOT: `/Users/ghost/core/anima/REBORN.md` (특히 §2 mitosis 본체, §6 user verdict, §10 우선순위)
- lane SSOT: `/Users/ghost/core/anima/.roadmap.reborn` track C
- architecture decision record: `/Users/ghost/core/anima/.roadmap.clm_v5_mitosis_engine` (a/b/c/d 비교 원본)
- canonical mitosis source: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (worktree-12, 794L)
- instrumentation port (sister track B): `/Users/ghost/core/anima/training/mitosis_v5_port.py` (480L, raw#15 reference)
- IIT Φ port: `/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10/iit_phi_port.py` (268L)
- BG-CHAT-EXT destructive readout: `docs/anima_clm_v2_chat_ext_smoke_2026_05_10.md`
- BG-PHASE2-CKPT-INSTR V14 NOVEL POLARITY: `docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md`
- prior revival spec (v5-anima track): `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md`

---

raw#15 additive — 본 spec 작성 외 코드 변경 없음. raw#10 honest — §11 honest C3 12개. 0-cost — design only. mandatory report — 본 cycle close 시 호출자에게 emit.

end of `anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md`.
