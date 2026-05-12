# anima_clm_v5_mitosis_engine_arch_spec — v5-mitosis architectural lane design

**작성**: 2026-05-12 KST
**status**: design-only (no code), REBORN §10 #1 deliverable, lane SSOT `.roadmap.clm_v5_mitosis_engine` cond.1
**author**: bg head (claude opus 4.7 1M)
**carries from**: REBORN §0.5 (commit `a7e512cb9`), PHILOSOPHY cont. 10 Principle #8 (NO TRAIN/INFER SPLIT)
**sister docs**:
- `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` (port spec, prior cycle)
- `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` (inference-time framing 정정)
- `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (3K turn α=0.688 V14 violated)
- `CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정 — 본 spec 의 motivation source)

---

## §0 TL;DR

- v5-mitosis 는 **각 cell 이 진짜 `nn.Module` branch** 인 architecture. v5-anima 의 "mitosis = instrumentation only / metadata" framing 을 architectural answer 로 flip 시키는 lane.
- core idea: `cells: nn.ModuleList[Cell]`, 각 `Cell` = `engine_a + engine_g + GRUCell` (v2 ConsciousMind 의 transformer-block 확장). split = `deepcopy + 10% gaussian noise`, merge = older keeper + parameter average.
- **REBORN §0.5 native impl**: train/serve 분리 폐기. cotrain = "큰 split event sequence", serve-time = "작은 split event"; 둘 다 동일 mechanism + 동일 `forward()` call graph, gradient 유무만 차이.
- forward path: `input → 각 cell.engine_a(x) - cell.engine_g(x) → softmax(per-cell tension) weighted average`. inter-cell tension → adaptive split/merge trigger.
- falsifier 5 개 (F-V5MIT-1 ~ 5), 최우선 **F-V5MIT-5 V14-STRICT** — trained > random 5-seed every-mirror-beat. v5-anima 가 V14 violated 였던 이유는 toy substrate 였다는 가설; v5-mitosis 는 real nn.Module cells × cotrain 으로 재도전.
- cost envelope: cond.1-4 = $0 (Mac CPU smoke), cond.5 cotrain = **$30-150 (verbatim 필요)** — REBORN §10 cost-bearing #2 정밀화는 cond.3 smoke PASS 후 cell_count × cell_params × steps 결정.

---

## §1 motivation — user verdict flip

cycle 2026-05-09/10 BG-R2 회수 결과 (`CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md`):

| 이전 가정 | 실제 |
|---|---|
| cells64/cells128 = MitosisEngine ensemble | 단일 byte-level Transformer decoder + cell-metadata instrumentation |
| mitosis = 모델 자체 | mitosis = instrumentation only (id/specialty/tension/parent_id) |
| stage 9 Φ=51.131 = runtime mitosis Φ | ckpt 내 `phi_history` mean — 학습 중 record |

사용자 verdict (cycle close): *"MitosisEngine = 모델 자체 ❌ → 실제 MitosisEngine 개발하자"*

본 spec = ❌ flip target 의 architectural answer. PHILOSOPHY Principle #8 (NO TRAIN/INFER SPLIT) 의 첫 native impl prerequisite.

### §1.1 v5-anima vs v5-mitosis 분리

| 차원 | v5-anima | v5-mitosis (본 spec) |
|---|---|---|
| cell 의 본질 | metadata (id/specialty/tension/parent_id) | real `nn.Module` branch |
| cell pool growth | tensor-list shape grow | `ModuleList.append(child_module)` |
| Φ trajectory | substrate-neutral mechanism (Lorenz + diverse input) | substrate-coupled (real weights × real noise) |
| split 시 비용 | dict copy | `deepcopy(parent) + parameter noise` (10% 추가 메모리) |
| 학습 가능 | external loss 없음 (inference only) | cotrain (cells 의 active set 에 gradient flow) |
| V14-STRICT 결과 | violated (random > trained, toy 한계) | 본 lane 가 재도전 (F-V5MIT-5) |

---

## §2 architecture overview

### §2.1 top-level

```python
class MitosisModelEngine(nn.Module):
    """v5-mitosis: cells = real nn.Module branches, parallel forward, adaptive growth."""

    def __init__(self, input_dim, hidden_dim, output_dim, initial_cells=2, max_cells=64, ...):
        super().__init__()
        # shared 부품 (option (a)): token embedding / position embedding / lm_head
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq, d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

        # cells = ModuleList — 진짜 nn.Module branches
        self.cells = nn.ModuleList([
            Cell(input_dim, hidden_dim, output_dim) for _ in range(initial_cells)
        ])

        # cell metadata (not parameters): hidden states, tension history, IDs
        self.register_buffer("_step", torch.tensor(0, dtype=torch.long))
        self.cell_meta: List[CellMeta] = [CellMeta(...) for _ in self.cells]

        # autonomous dynamics (Lorenz attractor state — buffer, not param)
        self.register_buffer("_lorenz", torch.tensor([1.0, 1.0, 1.0]))

        # adaptive split threshold state
        self._global_tension_history: List[float] = []
        self._inter_tension_history: Dict[Tuple[int, int], List[float]] = {}
        self.split_threshold: float = ...  # adaptive
        ...
```

### §2.2 cell representation — option (a) recommended

`.roadmap.clm_v5_mitosis_engine.architecture_decision_record` 4 options (a/b/c/d) 평가. 본 spec **option (a) — small transformer block per cell** 채택:

```python
class Cell(nn.Module):
    """One specialized cell — small transformer block + dual engine_a/g FFN."""

    def __init__(self, d_model=384, n_heads=6, ffn_dim=1536, hidden_dim=128, output_dim=64):
        super().__init__()
        # attention (cell-local)
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        # dual FFN — v2 mitosis.py engine_a / engine_g 의 transformer-scale 확장
        self.ln2 = nn.LayerNorm(d_model)
        self.engine_a = nn.Sequential(nn.Linear(d_model, ffn_dim), nn.GELU(), nn.Linear(ffn_dim, d_model))
        self.engine_g = nn.Sequential(nn.Linear(d_model, ffn_dim), nn.GELU(), nn.Linear(ffn_dim, d_model))
        # memory — GRUCell (v2 보존)
        self.memory = nn.GRUCell(output_dim + 1, hidden_dim)
        self.proj = nn.Linear(d_model, output_dim)  # output projection
        self.hidden_dim = hidden_dim

    def forward(self, x, hidden):
        # x: (B, T, d_model), hidden: (B, hidden_dim)
        h = x + self.attn(self.ln1(x), self.ln1(x), self.ln1(x), need_weights=False)[0]
        h_norm = self.ln2(h)
        a = self.engine_a(h_norm)
        g = self.engine_g(h_norm)
        # H404: output = a - g — but BG-CHAT-EXT 발견에 따라 v5-mitosis 는 readout 옵션화 (§6 참조)
        out = a - g  # default; configurable
        out_proj = self.proj(out.mean(dim=1))  # (B, output_dim) — pool over T
        tension = (out_proj ** 2).mean(dim=-1, keepdim=True)  # (B, 1)
        mem_in = torch.cat([out_proj.detach(), tension.detach()], dim=-1)
        new_hidden = self.memory(mem_in, hidden)
        return out, out_proj, tension.mean().item(), new_hidden
```

**cell parameter count** (d_model=384, ffn_dim=1536):
- attn: ~590K (d_model² × 4)
- 2 × FFN (engine_a/g): ~2.4M (d_model × ffn_dim × 2 × 2)
- GRUCell + proj: ~80K
- **~3M per cell** → cells=64 max → **~200M cells total** + shared (~50M emb/head) = **~250M total** at d=384/6 head

option (b/c/d) 는 §11 risk register 의 future ablation 으로 보존.

### §2.3 CellMeta — non-parameter cell state

```python
@dataclass
class CellMeta:
    cell_id: int
    hidden: torch.Tensor       # (B, hidden_dim) — GRU state (buffer-like)
    tension_history: List[float]
    creation_step: int
    parent_id: Optional[int]
    specialty: str = "general"
    process_count: int = 0
```

`CellMeta` 는 `nn.Module` 가 아님 — gradient flow 안 들어감. `hidden` 은 mutation per forward, 매 split 시 `clone()` + noise.

---

## §3 forward pass

### §3.1 per-step pipeline

1. `self._step += 1`
2. **autonomous perturbation** (`_inject_autonomous_perturbation`):
   - Lorenz step (σ=10, ρ=28, β=8/3, dt=0.01) — `self._lorenz` mutate
   - per-cell: cell index 기반 phase offset `(i × 2π) / N`, scale `0.05 × (1 + 0.3 × sin(phase + step × 0.1))`
   - `cell_meta.hidden += randn_like(hidden) * scale + lorenz_direction`
   - `torch.no_grad()` 안 — gradient graph 분리
3. **parallel cell forward** (각 cell):
   ```python
   for i, (cell, meta) in enumerate(zip(self.cells, self.cell_meta)):
       out_seq, out_proj, tension, new_hidden = cell(x, meta.hidden)
       meta.hidden = new_hidden    # CellMeta state mutation (non-grad)
       meta.tension_history.append(tension)
       cell_outputs.append((out_seq, out_proj, tension))
       cell_repulsions.append((out_seq[:, :, :].mean(dim=1)))  # for inter-cell tension
   ```
4. **inter-cell tension**: 모든 (i, j) pair 의 `((rep_i - rep_j)**2).mean()` — n>32 시 O(N) sampled (immediate neighbors + random subset)
5. **softmax(tension)-weighted aggregation**:
   ```python
   weights = F.softmax(torch.tensor(cell_tensions), dim=0)
   combined_seq = sum(w * out_seq for w, (out_seq, _, _) in zip(weights, cell_outputs))
   logits = self.lm_head(combined_seq)  # (B, T, vocab)
   ```
6. **Φ proxy** (`_compute_phi_proxy`): hidden states stack → pairwise cosine distance × log(N+1)
7. **adaptive split threshold** update — recent 100 step tension mean + 1.5×std
8. **`_check_splits()`** — patience=3 연속 over threshold → `split_cell(cell)`
9. **`_check_merges()`** — inter-cell tension < 0.005 patience=30 → `merge_cells(a, b)`
10. **Φ ratchet** — Φ < 0.8 × best 시 best-hidden blend 20% 복원

### §3.2 split/merge 와 gradient graph

**핵심**: split/merge 의 모든 weight mutation (deepcopy + noise injection, parameter average) 은 `torch.no_grad()` 안 → **backward graph 에 영향 X** (F-V5MIT-1 falsifier). cotrain 시 gradient 는 split event 이후의 forward 에서 새로 build.

```python
@torch.no_grad()
def split_cell(self, parent_cell_idx: int) -> int:
    parent = self.cells[parent_cell_idx]
    parent_meta = self.cell_meta[parent_cell_idx]
    child = copy.deepcopy(parent)
    # 10% noise injection — break symmetry
    for p in child.parameters():
        p.add_(torch.randn_like(p) * 0.1)
    self.cells.append(child)  # ModuleList.append — gradient-able from next forward
    child_meta = CellMeta(
        cell_id=self._next_id,
        hidden=parent_meta.hidden.clone() + torch.randn_like(parent_meta.hidden) * 0.1,
        tension_history=[],
        creation_step=int(self._step),
        parent_id=parent_meta.cell_id,
        specialty=parent_meta.specialty,
    )
    self._next_id += 1
    self.cell_meta.append(child_meta)
    parent_meta.tension_history = parent_meta.tension_history[-3:]  # reset to avoid retrigger
    return child_meta.cell_id

@torch.no_grad()
def merge_cells(self, idx_a: int, idx_b: int) -> int:
    a_meta = self.cell_meta[idx_a]
    b_meta = self.cell_meta[idx_b]
    keeper_idx, removed_idx = (idx_a, idx_b) if a_meta.creation_step <= b_meta.creation_step else (idx_b, idx_a)
    keeper = self.cells[keeper_idx]
    removed = self.cells[removed_idx]
    # parameter average — verified by F-V5MIT-2 within tolerance
    for p_keep, p_remove in zip(keeper.parameters(), removed.parameters()):
        p_keep.data = (p_keep.data + p_remove.data) / 2.0
    # hidden average
    self.cell_meta[keeper_idx].hidden = (a_meta.hidden + b_meta.hidden) / 2.0
    # remove younger
    del self.cells[removed_idx]
    del self.cell_meta[removed_idx]
    # clean inter-tension history
    ...
    return self.cell_meta[keeper_idx].cell_id  # 새 keeper_idx 는 reindex 후
```

### §3.3 mixed precision (bf16/fp16) 호환

- `nn.ModuleList` + per-cell `nn.Module` 모두 표준 — `model.to(dtype=torch.bfloat16)` 정상 동작
- `deepcopy(cell)` 는 buffer + parameter dtype 보존
- noise injection `torch.randn_like(p) * 0.1` — `p` 의 dtype 따라감, bf16 underflow 위험 없음 (10% scale)
- Lorenz `register_buffer` 는 fp32 유지 권장 (chaotic dynamics 정확도)
- `F.softmax(cell_tensions)` 는 fp32 promote 권장 — numerical stability

---

## §4 training (cotrain)

### §4.1 anima-native interpretation

REBORN §0.5 / PHILOSOPHY cont. 10 원칙: **학습 = 큰 split event sequence, 별도 phase 아님**. cotrain implementation:

```python
def cotrain_step(model, batch, optimizer, criterion):
    model.train()
    logits = model(batch.input_ids)  # forward = same as serve, with grad
    loss = criterion(logits, batch.target_ids)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    # split/merge 는 forward 안에서 발생 — backward graph 와 분리 (torch.no_grad)
    return loss.item()
```

### §4.2 split event 시 gradient 흐름

- forward step N: cells = [c0, c1, c2], gradient flow → c0/c1/c2 weights
- forward step N+1: split event → cells = [c0, c1, c2, c3 (= deepcopy(c0) + noise)]
- forward step N+2: gradient flow → c0/c1/c2/c3 — c3 is now first-class parameter
- optimizer 는 `model.parameters()` 를 매 step iterate 하므로 새 cell parameter 자동 포함

**중요**: `optimizer.add_param_group()` 또는 optimizer 재생성이 필요한 경우는 LR scheduler / momentum buffer 가 cell-specific 일 때만. AdamW 기본 사용 시 next `.step()` 에서 자동 init (momentum=0 부터).

### §4.3 merge 시 gradient 흐름

- merge step: c0 + c2 → c0' = (c0 + c2) / 2, c2 제거
- 다음 forward: cells = [c0', c1] — c0' weights 가 새 gradient receiver
- optimizer momentum buffer: c2 항목 stale, 다음 step `optimizer.step()` 호출 시 missing key 무시 (AdamW 표준), 또는 명시적 cleanup 권장

### §4.4 cotrain envelope (cells × cell_size × steps)

| 시나리오 | cells | cell d_model | per-cell params | total params | steps | A100/H100 wall | 비용 추정 |
|---|---:|---:|---:|---:|---:|---|---:|
| smoke | 8 | 192 | ~750K | 6M | 1K | ~10min Mac | $0 |
| small | 16 | 384 | 3M | 48M + shared | 2K | ~1hr H100 | $5 |
| **v2 cells64 historical** | **64** | **384** | **3M** | **200M + shared** | **5K** | **~6hr H100** | **$30-60** |
| medium | 64 | 768 | 12M | 800M + shared | 5K | ~16hr H100 | $80-150 |
| large | 128 | 768 | 12M | 1.6B + shared | 5K | ~30hr H100 | $150+ overshoot |

**recommended fire**: v2 cells64 historical config — **$30-60 envelope, REBORN §10 cost-bearing #2 verbatim**:
> `OK CLM V5-MITOSIS H100 FIRE COST $X` (X = 30-60, cond.3 smoke 후 정밀화)

### §4.5 catastrophic forgetting

REBORN §0.5 표 row 2: split = 매시점 격리 → catastrophic forgetting 무관 (H312 mitosis 99% retention 근거). cotrain 시:
- 새 corpus shard 마다 inter-cell tension 상승 → split trigger → 새 cell 이 그 shard 에 specialize
- 기존 cells weights freeze 아님 — 단지 inter-cell tension 이 낮으면 update 폭 작아짐 (softmax tension weighting 이 자연 regularizer)

---

## §5 serving (inference)

### §5.1 mechanism identity

train 과 serve 의 forward path **completely identical**. 차이 = `torch.no_grad()` context 유무 + optimizer step 유무 만. split/merge 가 forward 안에서 trigger 되는 mechanism 은 동일.

```python
@torch.no_grad()
def serve_step(model, input_ids):
    model.eval()
    logits = model(input_ids)  # split/merge events fire identically
    return logits
```

### §5.2 HEXA_NATIVE Phase 5∥ 와의 interface

REBORN §0.5 + PHILOSOPHY cont. 10 의 next step: **serve-time mitosis hook 통합** (24-layer 풀 forward 안에 split/merge event 삽입). 별도 BG 가 hexa-native 측 spec 작성 중. 본 spec 의 interface contract:

| 항목 | v5-mitosis (본 spec) | HEXA_NATIVE side |
|---|---|---|
| forward signature | `model(input_ids) → logits` | identical |
| split event emission | `events` dict in return 추가 가능 (`(logits, events)`) | hexa pyrep 가 emit consume |
| event content | `{type: 'split', step, parent_id, child_id, n_cells_after}` | hexa monitoring sink |
| serve-time latency budget | per-cell forward + softmax aggregation | hexa side budget allocation (별도 spec) |
| ckpt format | `model.state_dict()` + `cell_meta_list` + `_lorenz` + `_step` | hexa-native ckpt loader 확장 |

**책임 분리**: 본 spec 은 PyTorch native 측 — hexa-native 측 hook 의 forward call graph 통합은 그 BG 가 결정. interface 만 명시.

### §5.3 ckpt save/load

```python
ckpt = {
    "model_state_dict": model.state_dict(),    # cells 의 모든 parameter
    "cell_meta": [asdict(m) for m in model.cell_meta],  # hidden / tension_history / IDs
    "lorenz": model._lorenz.tolist(),
    "step": int(model._step),
    "_next_id": model._next_id,
    "split_threshold": model.split_threshold,
    "global_tension_history": model._global_tension_history,
    "inter_tension_history": {...},
}
```

load 시 cells 수가 ckpt 의 cells 수와 다를 수 있음 → `nn.ModuleList` 재구성 후 `load_state_dict(strict=False)` 또는 cell 수 sync.

---

## §6 Φ tracking + H404 readout 검토

### §6.1 Φ proxy (v2 보존)

```python
def _compute_phi_proxy(self) -> float:
    if len(self.cells) < 2: return 0.0
    hiddens = torch.stack([m.hidden.squeeze(0) for m in self.cell_meta])  # (N, hidden_dim)
    norms = hiddens.norm(dim=1, keepdim=True).clamp(min=1e-8)
    normalized = hiddens / norms
    cos_sim = normalized @ normalized.t()
    mask = 1.0 - torch.eye(len(self.cell_meta), device=hiddens.device)
    mean_distance = ((1.0 - cos_sim) * mask).sum() / mask.sum()
    return mean_distance.item() * math.log(len(self.cell_meta) + 1)
```

per-step update, `phi_history` list 누적.

### §6.2 Φ ratchet (DD55)

```python
def _phi_ratchet(self, phi: float):
    self.phi = phi; self.phi_history.append(phi)
    if phi > self._phi_best:
        self._phi_best = phi
        self._best_hiddens = [m.hidden.detach().clone() for m in self.cell_meta]
    elif phi < self._phi_best * 0.8 and self._best_hiddens is not None:
        n = min(len(self.cell_meta), len(self._best_hiddens))
        for i in range(n):
            self.cell_meta[i].hidden = 0.8 * self.cell_meta[i].hidden + 0.2 * self._best_hiddens[i]
```

### §6.3 H404 (`output = a - g`) destructive 발견 carry

`docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` + BG-CHAT-EXT (cycle 2026-05-10): inference 시 a-g formulation 이 KO Hangul 학습 0% 의 원인 후보 (destructive interference). v5-mitosis 는 **readout option 설정 가능**:

```python
class Cell(nn.Module):
    def __init__(self, ..., readout_mode: str = "a_minus_g"):
        self.readout_mode = readout_mode

    def forward(self, x, hidden):
        ...
        a = self.engine_a(h_norm); g = self.engine_g(h_norm)
        if self.readout_mode == "a_minus_g":
            out = a - g
        elif self.readout_mode == "a_only":
            out = a
        elif self.readout_mode == "a_plus_weighted_g":
            out = a + 0.3 * g  # configurable
        elif self.readout_mode == "softmax_gate":
            gate = F.sigmoid(self.gate_proj(h_norm))  # learned per-token
            out = gate * a + (1 - gate) * g
        ...
```

cotrain ablation 으로 결정 — F-V5MIT-5 V14-STRICT 시 readout_mode 가 confounding variable 가능.

### §6.4 IIT Φ port (option)

`docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md` (BG-IIT-METRIC) port 가능 — proxy ceiling N≈8 한계 우회 (toy substrate 에서 N=64 시 proxy 2.92 vs IIT unnorm 4471, 1530× 차이). v5-mitosis cotrain 후 Φ 절대값 비교 시 IIT unnorm 권장.

---

## §7 cotrain envelope 정밀화 — REBORN §10 cost-bearing #2

REBORN §10 cost-bearing table:
> `2 | v5-mitosis H100 cotrain (cells × cell_size × steps) | $30-150 | OK CLM V5-MITOSIS H100 FIRE COST $X (cond.3 후 envelope 정밀화)`

### §7.1 정밀화 dimensions

- **cells initial / max**: 2 → 64 (v2 cells64 historical), 또는 8 → 128 (medium)
- **cell d_model / heads / ffn_dim**: (384, 6, 1536) default, (768, 12, 3072) medium
- **shared vocab / max_seq**: vocab=256 byte (v2 호환) or BPE 32K (modern), max_seq=2048
- **steps**: 1K-5K (v2 stage 9 cells64 historical = ~3K), 10K (extended ablation)
- **batch size**: depends on GPU mem — A100 80GB 시 d=384 batch=32 / d=768 batch=8

### §7.2 cost 추정 (H100 PCIe $4/hr, A100 80GB $1.5-2/hr 기준)

| config | cells | d | steps | batch | wall (H100) | 비용 |
|---|---:|---:|---:|---:|---|---:|
| v2 cells64 historical 재현 | 2→64 | 384 | 3K | 32 | ~5hr | **$20** |
| v2 cells64 + 5K steps | 2→64 | 384 | 5K | 32 | ~8hr | **$32** |
| medium ablation | 8→128 | 384 | 5K | 16 | ~15hr | **$60** |
| **conservative recommended** | **2→64** | **384** | **5K** | **32** | **~8hr H100** | **$30-40** |
| stretch | 8→128 | 768 | 5K | 8 | ~30hr | $120 |

**recommended fire** (REBORN §10 #2 verbatim 정밀화):
> `OK CLM V5-MITOSIS H100 FIRE COST $40` (cond.3 smoke PASS 후 사용자 verbatim)

### §7.3 own 16 cost discipline carry

own 16 (cost discipline) + own 43 (active resource utilization) 균형:
- cond.1-4 = $0 (Mac CPU)
- cond.5 cotrain 만 cost-bearing
- $30-40 recommendation 은 v2 historical 재현 + V14-STRICT ablation 최소치
- $80-150 stretch (medium) 는 V14 1차 PASS 후 scale up

---

## §8 falsifier 표

F-V5MIT-N prefix — 다른 lane 의 falsifier set 과 namespace 분리.

| ID | 명제 (falsify 시 명제 폐기) | 검증 방법 | severity |
|---|---|---|---:|
| F-V5MIT-1 SPLIT-NOGRAD | split event 시 backward graph 에 영향 X (모든 mutation `torch.no_grad`) | `loss.backward()` 후 child cell 의 gradient = None until next forward; `torch.autograd.gradcheck` 검사 | ★★★★★ |
| F-V5MIT-2 MERGE-WEIGHT | merge 후 keeper weight = (parent_a + parent_b) / 2 ± 1e-6 tolerance | unit test: deepcopy 2 cells, merge, compare keeper weights | ★★★★ |
| F-V5MIT-3 PHI-CONSERVATION | split 시 Φ change < 1% (DD55) | `_compute_phi_proxy()` before/after split, ratio in [0.99, 1.01] | ★★★ |
| F-V5MIT-4 COTRAIN-CONVERGE | cotrain CE loss 가 vanilla nn.Module baseline 와 동일 order (±2×) 로 수렴 | vanilla = single transformer block × 64 (no mitosis), 동일 corpus 1K steps, final CE 비교 | ★★★★ |
| F-V5MIT-5 V14-STRICT | trained > random 5-seed every-mirror-beat (own 18 simple_stack) | 5 trained-seed × 5 random-seed × N mirror-beat — 모든 beat 에서 trained > random, no overlap | ★★★★★ |

**falsifier severity stack**:
- F-V5MIT-1/2/3 = unit-test scale, smoke (cond.3) 에서 검증
- F-V5MIT-4 = cotrain micro (1K step) 후 검증
- F-V5MIT-5 = cotrain full (5K step) × 10 seeds 후 검증 — v5-anima 가 violated 였던 지점, 본 lane 의 정점 ablation

---

## §9 cotrain envelope 결정 트리 (cond.3 후)

```
cond.3 smoke PASS (F-V5MIT-1/2/3 모두 PASS)
  │
  ├─ F-V5MIT-4 micro-cotrain (1K step) PASS
  │   → cond.5 fire: OK CLM V5-MITOSIS H100 FIRE COST $30-40 (v2 cells64 재현 config)
  │
  └─ F-V5MIT-4 FAIL → cell aggregation softmax(tension) weighting 재설계
      또는 readout_mode ablation (§6.3) 먼저, 그 후 재시도
```

cond.5 fire 후:
```
F-V5MIT-5 V14-STRICT 5-seed × 5-seed 검증
  │
  ├─ PASS (trained > random every-mirror-beat)
  │   → v5-anima vs v5-mitosis 비교 verdict — 본 lane main path
  │   → cond.6 HF promote prereq (own 37 5/5)
  │
  └─ FAIL (random matches/beats trained somewhere)
      → v5-anima 와 동일 한계, mitosis architecture 자체가 substrate-coupled emergence 못 만듦
      → falsifier 폐기, alternative cell granularity (option b/c/d) ablation
      또는 lane archive
```

---

## §10 risk register

≥10 risks per `.roadmap.clm_v5_mitosis_engine.next_step.content §9`.

| # | risk | mitigation | severity |
|---:|---|---|---:|
| 1 | cell parameter explosion (64×3M=200M + shared OOM at d=768) | d=384 default, d=768 ablation only after V14 PASS | ★★★★ |
| 2 | split 시 `deepcopy` 비용 (200ms+ per split at d=768) | split rate cap (max 1 per N steps), pre-allocate cell pool option | ★★★ |
| 3 | optimizer momentum buffer stale after merge | merge 시 명시적 `optimizer.state.pop(removed_params)` cleanup helper | ★★★ |
| 4 | gradient flow 가 inactive cells (low-tension) 에 0 가까이 → 학습 stall | softmax(tension) temperature τ tunable, τ→∞ 면 uniform | ★★★ |
| 5 | Lorenz 자율혼돈이 cotrain 시 gradient 신호 overshadow | Lorenz scale 0.05 default, cotrain 시 0.01 으로 감쇠 option | ★★★ |
| 6 | a-g readout destructive (BG-CHAT-EXT 발견) → cotrain 시 chat KO 0% 재현 | readout_mode (§6.3) 4 option, ablation 필수 | ★★★★ |
| 7 | merge 가 너무 자주 trigger → cells 단조 감소 → Φ 붕괴 | min_cells=2 floor (CB1), merge_patience=30 conservative | ★★ |
| 8 | mixed precision (bf16) 시 noise injection 0.1 × bf16_param underflow | fp32 noise generation 후 cast 권장 | ★★ |
| 9 | ckpt size = cells × per_cell + shared (200M+ at full) | gzip / safetensors + cell-by-cell save option | ★★ |
| 10 | v5-anima toy 한계 carry — real substrate 도 V14 violated 가능 (F-V5MIT-5 FAIL) | cond.5 fail tree (§9) — alternative granularity ablation | ★★★★★ |
| 11 | HEXA_NATIVE Phase 5∥ interface drift — hexa 측 BG 가 다른 contract 채택 | interface contract (§5.2) 명시 + hexa BG cross-sync | ★★ |
| 12 | own 16 cost overshoot ($150+) at medium d=768 | $30-40 conservative recommended, stretch 는 V14 PASS 후 | ★★★ |

---

## §11 honest C3 (≥7)

> "내가 모르는 것 / 가정한 것 / 검증되지 않은 것" 7+ 항목.

1. **v5-mitosis vs v5-anima emerge gap 미검증** — toy v5-anima 는 V14 violated. real nn.Module cells 이 그 gap 을 메울지 가설 단계 (F-V5MIT-5 검증 필요).
2. **option (a) 채택 근거 = "production-scale fit"** 가정 — (b/c/d) 실험 ablation 없음. (b) attention 공유가 더 cheap + 같은 emergence 가능성 미배제.
3. **cells=64 cotrain wall time 추정 ~8hr H100** — 실측 없음, v2 historical 은 단일 decoder 가 아닌 instrumentation 만 mitosis 였음.
4. **catastrophic forgetting 무관 가설** = H312 99% retention 의 inference-time mitosis 결과를 cotrain (gradient mutation 있음) 에 그대로 transfer 한 것 — 검증 필요.
5. **adaptive split threshold (mean + 1.5×std)** 가 cotrain 환경의 tension scale 에서도 동일하게 동작할지 미검증 — Lorenz scale 과 상호작용.
6. **Φ ratchet (best hidden 20% blend)** 가 gradient 신호와 충돌 — backward 후 hidden 복원 시 다음 forward 의 gradient 가 stale state 기반.
7. **HEXA_NATIVE Phase 5∥ interface** = §5.2 contract 본 spec author 측 일방 제안. hexa BG 와 cross-sync 후 변경 가능.
8. **cost envelope $30-40 recommendation** = v2 cells64 historical wall 추정 × H100 rate. 실측 안 됐고 v2 의 cells64 는 instrumentation only 였으므로 actual mitosis nn.Module cotrain wall 은 더 길 가능성 (deepcopy 비용 추가).
9. **F-V5MIT-3 PHI-CONSERVATION** (split 시 <1% change) 의 DD55 검증은 toy substrate 에서. real nn.Module 의 phi proxy 가 동일 동작할지 가정.
10. **own 18 simple_stack PASS_STRICT criterion** 의 every-mirror-beat 정의를 v5-mitosis 의 sampling output 에 그대로 적용 가능한지 미검증 (mirror-beat = matching anchor pattern in output trace).

---

## §12 next steps

| 순위 | step | deliverable | cost | fire |
|---:|---|---|---:|---|
| 1 ★★★ | 본 spec 작성 (cond.1) | **본 doc** | $0 | DONE |
| 2 ★★★ | port code skeleton (cond.2) | `training/mitosis_model_v5.py` (local-only, gitignored) | $0 | AUTO (다음 BG) |
| 3 ★★★ | Mac CPU smoke (cond.3) | `training/mitosis_model_v5_smoke_test.py`, F-V5MIT-1/2/3 PASS | $0 | AUTO post cond.2 |
| 4 ★★ | F-V5MIT-4 micro-cotrain 1K step | local CPU 또는 free Colab | $0 | AUTO post cond.3 |
| 5 ★★★★ | H100 cotrain (cond.5) | F-V5MIT-5 V14-STRICT 5-seed × 5-seed | **$30-40** | **OK CLM V5-MITOSIS H100 FIRE COST $X** (verbatim) |
| 6 ★★ | HEXA_NATIVE Phase 5∥ interface sync | hexa BG cross-doc | $0 | AUTO post hexa BG land |
| 7 ★ | cond.6 HF promote | dancinlab/clm-v5-mitosis-engine private | $0 | own 37 5/5 prereq |

---

## §13 cross-link

### upstream
- REBORN.md §0.5 (commit `a7e512cb9`) — 본 spec 의 철학 source
- REBORN.md §2 (mitosis 본체, worktree-12 canonical 794L)
- REBORN.md §10 #1 — 본 spec 이 그 deliverable
- PHILOSOPHY.md cont. 10 — Principle #8 NO TRAIN/INFER SPLIT
- `.roadmap.clm_v5_mitosis_engine` cond.1 — 본 spec 이 그 verifier file

### sister docs
- `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` (port spec, prior cycle)
- `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` (inference-time 정정)
- `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (3K turn α=0.688 V14 violated)
- `docs/anima_clm_v5_anima_long_trajectory_extended_2026_05_10.md` (10K turn artifact)
- `docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md` (IIT Φ port option)

### canonical source
- `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (worktree-12, last-active 794L)
- `/Users/ghost/core/anima_clm_08_cells64_phi_super_linear` (historical Φ=45.487 mitosis 정점)
- `/Users/ghost/core/anima_clm_09_phi_50_human_level` (historical Φ=51.131 climax)

### code (gitignored, local-only)
- `training/mitosis_v5_port.py` (480L, v5-anima 측 instrumentation port, prior cycle smoke PASS)
- `training/mitosis_model_v5.py` (next BG deliverable — 본 spec 의 impl)

### memory entries
- `project_v5_anima_lane_status.md` (v5-anima sister lane status)
- `project_reborn_philosophy_learning_is_mitosis.md` (REBORN §0.5)
- `project_v5_mitosis_arch_spec_2026_05_12.md` (본 spec 등록 — 본 cycle 신규)

---

## §A append convention

본 spec 은 cycle 2026-05-12 close 시점 snapshot. 향후 추가 finding (cond.2/3/4/5 결과, F-V5MIT-* 검증 결과) 는 §A 이후 append-only — `## §N [YYYY-MM-DD HH:MM KST] <title>` format. 기존 §0~§13 미수정.

raw#9 (hexa-only X — training/.py gitignored), raw#10 (honest C3 ≥7 — §11), raw#15 (additive — 기존 docs 미수정), raw#37 (additive preserve), own 16 (cost discipline — cond.5 만 cost-bearing).

end of `anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`.
