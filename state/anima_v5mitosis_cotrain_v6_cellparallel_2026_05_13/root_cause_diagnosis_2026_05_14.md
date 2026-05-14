# v6 cell-parallel F-V5MIT-4 COTRAIN-CONVERGE FAIL — root-cause diagnosis

**date**: 2026-05-14
**status**: ROOT CAUSE 확정 (code audit, Mac local $0)
**scope**: SAVANT.md §10.1 closure path (ii) LANDED
**Linked**: `project_v5_mitosis_cotrain_v6_cellparallel_2026_05_13.md`

## 0. 결론

> v6 cell-parallel 의 loss 17.7→17.7 횡보는 **catastrophic data incoherence**:
> 각 rank 가 *다른 batch* 를 *다른 cells* 로 forward 한 후 `all_reduce(SUM)` 으로
> 합치는데, 결과 aggregated 는 의미 없는 부분합. CE 17.7 ≫ log(vocab=256)=5.55 ⇒
> *random 보다 나쁨* 의 신호. category-routing 가설 (§52 v7 KL>0) 의 재현 실패도
> 학습 자체가 안 된 *2차* 결과.

## 1. 코드 trace

### 1.1 Per-rank seed 설정
`training/cotrain_v5mitosis_v6_cellparallel.py:607-608`:
```python
torch.manual_seed(args.seed + rank)  # different seed per rank for sample independence
random.seed(args.seed + rank)
```
원래 의도 (memory C3 #8): "per-rank corpus sampling → 효과적 batch W× 증가 (free)".

### 1.2 sample_batch — torch.randint 가 위 seed 의 영향 받음
`training/cotrain_v5mitosis_v6_cellparallel.py:126-132`:
```python
def sample_batch(corpus, batch_size, ctx, device):
    N = corpus.size(0)
    idx = torch.randint(0, N - ctx - 1, (batch_size,))  # ← rank-specific RNG
    rows = torch.stack([corpus[i: i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1: ctx + 1].to(device)
```
→ rank 0 → `x_0, y_0` / rank 1 → `x_1, y_1` / ... — **각 rank 다른 batch**.

### 1.3 Forward path with mixed batches
`training/mitosis_model_v5_cellparallel.py:185-251`:
```python
# rank r:
x_r = tok_emb(input_ids_r) + pos_emb(pos)                # rank-specific batch
local_outs_r = [cell(x_r) for cell in self.cells]        # rank-local cells × rank-local batch
local_weighted_r = (local_weights_r * stacked_r).sum(0)  # rank-r partial
dist.all_reduce(local_weighted_r, op=SUM)                # GLOBAL SUM
aggregated = sum_r local_weighted_r
            = sum_r ( sum_{c in cells_r} w_c · cell_c(x_r) )
```
→ `aggregated` 는 **서로 다른 batch (`x_0`..`x_W`) 의 부분 합** — semantically meaningless.

### 1.4 Loss with mismatched targets
`training/cotrain_v5mitosis_v6_cellparallel.py:706`:
```python
ce = F.cross_entropy(logits.reshape(-1, vocab_size), y.reshape(-1))
```
→ rank r 의 `y` = `y_r` (`x_r` 의 target). 하지만 `logits` 는 `aggregated(x_0..x_W)` 에서 옴 → **target mismatch**.

## 2. 진단 evidence

### 2.1 CE 값이 random 보다 *나쁨*
- vocab_size = 256 (byte-level, line 621)
- random uniform prediction: CE = log(256) = **5.545**
- v6 observed: CE = **17.7~18.2** 평탄 (5K steps 내내)
- → CE > 3 × log(vocab) — *systematic anti-information* signal
- ratio: exp(17.7) / exp(5.545) = **e^{12.16} ≈ 1.9 × 10⁵** times less likely than random

### 2.2 v1 baseline 비교
v1 cotrain (`project_v5_mitosis_cond5_cotrain_2026_05_12`):
- 264.35 → 1.17 (220× CE reduction, F-V5MIT-4 PASS)
- single-GPU, single batch per step → no cross-rank mixing
- 같은 model arch, 같은 loss 정의 → arch 자체는 정상

→ v6 의 실패는 *arch* 가 아니라 *distributed data flow* 의 incoherence.

### 2.3 Forward 수식 vs 실제 구현 mismatch
의도된 cell-parallel forward (각 cell c, all cells C_global):
```
y(x) = Σ_{c ∈ C_global} w_c · cell_c(x)
```
실제 v6 구현:
```
y_v6 = Σ_r Σ_{c ∈ C_r} w_c · cell_c(x_r)        # x_r per rank
     ≠ Σ_{c ∈ C_global} w_c · cell_c(x_global)  # 단일 x 가정한 형태
```

## 3. Fix 후보 (3 options)

### 3.1 (A) Same batch broadcast — recommended

`cotrain_v5mitosis_v6_cellparallel.py:703` 직전:
```python
if rank == 0:
    x, y = sample_batch(corpus, args.batch, args.ctx, device)
else:
    x = torch.empty(args.batch, args.ctx, dtype=torch.long, device=device)
    y = torch.empty(args.batch, args.ctx, dtype=torch.long, device=device)
if world_size > 1:
    dist.broadcast(x, src=0)
    dist.broadcast(y, src=0)
```

**장점**: 가장 단순, semantic 정확. 모든 rank 가 same batch 로 forward → aggregated 가 의미 있는 mixture.
**단점**: effective batch = `batch_size` (rank 수만큼 증가 없음). memory C3 #8 의 "free W× batch" 주장 무효화.

### 3.2 (B) RNG seed reset for sampling — 최소 변경

`cotrain_v5mitosis_v6_cellparallel.py:609` 추가 (line 607-608 직후, model init 전):
```python
torch.manual_seed(args.seed + rank)  # cells init: per-rank
random.seed(args.seed + rank)

# ... model init ...

# Before training loop, reset seed to base for sample_batch:
torch.manual_seed(args.seed)  # corpus sampling: all-rank identical
```

**장점**: 1-2 줄 변경. cells init 의 per-rank diversity 유지.
**단점**: 재 seed 가 *전체* RNG state reset — 다른 random 결정 (예: dropout) 도 모든 rank 동일. dropout=0.0 (line 626) 라 영향 없지만 future-proof 약함.

### 3.3 (C) DDP cell replication — 설계 변경

cells 도 모든 rank 에 *replicate*. v5_ddp 와 동일. cell-parallel 의 의미 상실 → 별도 v8 path 로 분리.

**장점**: 표준 DDP, 검증된 path. 
**단점**: cell-parallel 의 *핵심 의도* (cells dimension 자체를 GPU 에 분산) 폐기.

## 4. 영향 재평가 (post-diagnosis)

§10.1 표의 v6 FAIL 4 metric 중:
- F-V5MIT-4 COTRAIN-CONVERGE FAIL → **structural bug** (data incoherence) — fix 가능
- F-PERSONA-4a routing FAIL (KL=0.2972) → *학습 부재의 2차 결과*. fix 후 재측정 필요
- F-PERSONA-4b content FAIL (z=−0.88) → 동일 2차
- step_wall 2.4s (target 1.0s MISS) → fix 와 *무관*. all_reduce overhead 의 실측, 별도 문제

→ §52 v7 의 KL=3.45 first signal 재현 여부는 **fix 후 재실행** 까지 미정 (v6 결과는 evidence 미흡).
→ "category routing 가설 폐기" (closure path iv) 는 **시기상조** — fix 전 v6 결과로는 결론 미달.

## 5. Closure path (ii) verdict

✅ **LANDED**: v6 F-V5MIT-4 COTRAIN-CONVERGE FAIL 의 root cause = per-rank batch +
cell-shard SUM 의 catastrophic data incoherence. Fix 후보 3개 식별 (A recommended).

## 6. 후속 action items

1. **(ii-a) fix patch** ($0 Mac local code change): option (A) Same batch broadcast 적용 →
   commit 별도 patch. *re-fire 결정 사용자 위임*.
2. **(ii-b) v6 재실행 = v6.1** ($22 estimated, 4×A100 SXM4 동일 spec): fix 적용 후 5K step
   재훈련. F-V5MIT-4 PASS 여부 + F-PERSONA-4 재측정 — *category routing 가설 폐기/유지*
   결정의 *실제* evidence.
3. **(iii) §52 v7 cross-seed robustness** ($0.30-1.50 BG): v6 fix 와 *독립* — v7 single-seed
   결과의 robustness 가 *v6 fix 와 무관* 하게 검증 필요.

→ closure path (iv) "category routing 폐기" 는 (ii-b) v6.1 결과 받기 전 *유보*.

## 7. Honest C3

1. 본 진단은 *code audit 만* 으로 도출 — Mac local 에서 multi-rank smoke 재현 미실시.
   distributed gloo backend 로 smoke test 가능하지만 본 cycle 에서는 미실행.
2. v1 cotrain 의 *유일 차이* 는 단일 GPU = 단일 batch — distributed 시 multiple batches
   의 정확한 handling 검증이 별도 PR 필요.
3. fix 후에도 *step_wall* 문제는 별도 — all_reduce overhead 가 cell-loop savings 를
   상쇄하는 *근본* 의 cell-parallel 회의론 (memory C3 #2) 가 still standing.
4. memory C3 #8 ("per-rank seed → effective batch W× free") 는 **잘못된 가정으로 retract**
   필요. cell-parallel 에서는 batch 가 *공유* 되어야 cells subset 의 mixture 가 의미 있음.
   DDP (cell replication) 에서만 #8 이 유효.
5. backward gradient flow 자체는 PyTorch buffer-tracking 으로 일관됨 — 본 진단은 *forward
   data flow* 의 semantic 문제.
6. CE 17.7 의 *정확한* 분해 (rank 마다 다른 batch 가 어떻게 17.7 로 stable 한지) 는 추가
   분석 필요. 가설: random aggregated mixture 의 logits 가 *특정 byte* 에 systematically
   bias → 그 byte 와 y 의 mismatch 비율이 17.7 의 평탄 값에 수렴.
7. fix (A) 적용 시 effective batch 가 W× 증가 안 함 → wall-economic ROI 다시 평가 필요.
   v6 cost $22.43 / 24% speedup = NEGATIVE 결론 그대로.

---

— v6 root-cause diagnosis, 2026-05-14, $0 Mac local code audit, ~30 min wall
