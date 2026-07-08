# fork-A "모든 경우의 수" — mechanism-decomposition matrix (H_9235 · 2026-07-09)

오너 "모든 경우의 수 진행" — fork-A read-side lane의 전 메커니즘 조합을 전수 측정해 *어느 부품이
ρ·weave(G1)를 깨나* 분해. **pool{mean·query·last·max} × head{gelu-bias(clml)·hadamard-bind(RETRO-ROUTE)·linear} × N_ctx{2·4·8}**.

## 결과 요약

### ✅ 이미 valid (real 303M · `fork_a_precheck.py` · 다른 세션 #3191)
`pair_hidden.npz`(실 303M per-position hidden) 위 5-arm:
- `mean+gelu = 0.98` (route 존재) · `last+gelu = 0.47` (**routing이 lever**) · `mean+linear = 0.43` (**비선형 필요**) · `handed = 1.00` (valid) · `shuffle = 0.50`.
- ⟹ ρ·weave 벽=readout-ROUTING 확증 + 비선형 bottleneck이 합성. **미측정 arm = query-pool · hadamard-bind**.

### 🔴 synthetic toy (`synth_mechanism_matrix.py`) = **INVALID (측정불가)**
real precheck를 $0로 preview하려 한 controlled toy — **2차 원칙수정(orthonormal emb + handed 양성대조 + steps↑) 후에도 handed positive-control = 0.55–0.66 < 0.85 = INVALID**. 전 arm ≈ chance(0.51–0.57). 원인=toy under-coverage(700 random pair·R=96 vs precheck 842-pair 구조split·r=128)로 32-concept held-out XOR 학습 실패. **honesty(c9)**: toy가 알려진 학습가능성(precheck handed=1.0)조차 재현 못 하므로 arm 비교 uninformative. 더 튜닝=tune-to-green 위험 → 중단. **교훈(a_toy_scale_recheck)**: mechanism 분해의 유일 valid 경로 = real hidden. toy는 대체 불가.

### ⏳ definitive (real 303M · `fork_a_matrix.py`) = **준비완료 · INFRA-GATED**
precheck와 동일 입력(`pair_hidden.npz`)에 query-pool + hadamard-bind arm 추가 = 정본 매트릭스. 코드 ready.
**블로커(infra-wall-noneval)**: clean pool 호스트 부재 — summer load 27(overfire 위험 `summer-overfire`)·aiden는 canonical `e1_slw_303m.clm` 없음(다른 ckpt만)·rent=spend(owner go). dump 1회면 즉시 실행: `anima evaluate --py <e1_slw_303m.clm> --dump-hidden pair_prompts.json --out pair_hidden.npz --win 24`.

## 남은 결정 (owner)
real 매트릭스 dump 호스트: (a) 싼 pod rent ~\$0.3 (go 필요) · (b) summer cooldown 대기 · (c) e1_slw_303m.clm aiden 전송(293MB·OOM 위험 `aiden-stable-free-terminal-eval-host`).
그 전까지 이미 valid한 사실 = **routing이 lever·비선형 필요**(precheck 5-arm). clml(mean+gelu) 학습은 병렬세션 #3193 진행중.
