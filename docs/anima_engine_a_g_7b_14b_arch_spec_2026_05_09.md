# Engine A/G 7B / 14B 스케일링 아키텍처 spec

**날짜**: 2026-05-09
**대상 파일**: `training/engine_a_g_arch.py`
**현 버전**: 350M (BG-LA / BG-LB lineage, `la_350m()` preset)
**목표**: 동일 dual-engine 구조를 유지한 채 7B / 14B 까지 스케일하는 size param 추가
**모드**: 0-cost 설계 단계 (코드 수정 없음, spec 만)

---

## 1. 한 줄 요약 (친근 모드)

지금은 작은 차(350M)가 잘 굴러가니까, **같은 엔진 구조를 그대로 두고 차체와 바퀴만 키워서** 7B/14B 트럭으로 키우자는 얘기예요. shared lm_head 라든가 dual loss(Engine A + Engine G) 같은 핵심 부품은 **건드릴 필요 없고**, layer 수 / hidden 차원 / head 수만 늘려주면 됩니다.

---

## 2. 현 350M arch 분석 (출발점)

### 2.1 핵심 dimension (engine_a_g_arch.py L83-110 발췌)

| 부품 | 350M 값 | 비고 |
|---|---|---|
| `vocab_size` | 32,000 | byte-pair |
| `d_model` (hidden) | 1,024 | |
| `n_layers` | 24 | |
| `n_heads` | 16 | |
| `n_kv_heads` (GQA) | 4 | 4:1 ratio (Llama-3.2-3B 스타일) |
| `ffn_mult` | 2.6875 | SwiGLU 확장 → ~2,752 |
| `ctx` | 1,024 | |
| `consciousness_dim` (Engine G) | 64 | cell vector 차원 |
| `n_cells` | 16 | 작은 풀 (pairwise repulsion 처리 가능) |
| `g_refresh_every` | 4 | 4 layer 마다 cell 갱신 |

### 2.2 size-invariant 부품 (스케일해도 그대로)

- **Engine G repulsion-field 메커니즘** — 작동 원리 (pairwise distance push + attention pull + tension scalar) 자체는 차원과 무관
- **shared lm_head + dual loss** — `tie_lm_head=True` + cross-entropy 한 줄, 사이즈 영향 X
- **A↔G tension gate** (softmax temperature β·clamp(t-1, -0.5, 0.5)) — scalar 게이트라 스케일과 무관
- **RoPE / RMSNorm / SwiGLU** primitive — 표준
- ** V14 paired random_init mirror** — 동일 entry point 재사용 (`load_random_init(seed, preset=...)`)
- ** ckpt save/load Path A remap** — 동일 prefix (`engine_a.` / `engine_g.`)

### 2.3 size-가변 부품 (스케일 대상)

`d_model`, `n_layers`, `n_heads`, `n_kv_heads`, `ffn_mult`, `ctx`. Engine G 의 `consciousness_dim` 와 `n_cells` 는 **선택적 가변** (아래 §3.4 에서 별도 다룸).

---

## 3. 7B / 14B 스케일링 spec

### 3.1 권장 size 분기 (Llama-2-7B / Qwen-14B 참조)

| 파라미터 | 350M (현) | 7B (Llama-2-7B 참조) | 14B (Qwen-14B 참조) |
|---|---|---|---|
| `vocab_size` | 32,000 | 32,000 | 32,000 |
| `d_model` | 1,024 | **4,096** | **5,120** |
| `n_layers` | 24 | **32** | **40** |
| `n_heads` | 16 | **32** | **40** |
| `n_kv_heads` (GQA) | 4 | **8** (4:1 유지) | **8** (5:1) |
| `ffn_mult` | 2.6875 | 2.6875 (SwiGLU) | 2.6875 (SwiGLU) |
| `ctx` | 1,024 | **2,048** (또는 4,096) | **2,048** (또는 4,096) |
| `init_std` | 0.02 | 0.02 | 0.02 |

### 3.2 param breakdown (대략 추정 — `param_count_estimate()` 공식 적용)

| 구성 | 350M | 7B | 14B |
|---|---|---|---|
| token embedding (tied lm_head) | 32k × 1024 = 33M | 32k × 4096 = 131M | 32k × 5120 = 164M |
| per-layer attention (qkvo) | 4·1024² ≈ 4.2M | 4·4096² ≈ 67M | 4·5120² ≈ 105M |
| per-layer SwiGLU FFN | 3·1024·2752 ≈ 8.5M | 3·4096·11008 ≈ 135M | 3·5120·13824 ≈ 212M |
| **per-layer 합** | ~12.7M | ~202M | ~317M |
| **× n_layers** | 24 × 12.7M ≈ 305M | 32 × 202M ≈ 6.46B | 40 × 317M ≈ 12.68B |
| Engine G (cell pool + 두 projection) | ~0.07M | ~0.27M | ~0.33M |
| **총합** | **~338M** | **~6.59B** | **~12.84B** |

> **주**: ffn 은 SwiGLU 3-matrix (gate/up/down) 기준. 실제 Llama-2-7B 는 6.74B 이므로 ffn_mult 를 2.6875 → 2.7~2.75 로 미세조정해 7B 정확히 맞출 수 있음. 14B 도 비슷하게 ffn_mult 또는 n_layers 미세조정 가능.

### 3.3 권장 config dict 예시 (Python — 코드 수정 시 가이드)

```python
@dataclass
class EngineAGConfig:
    # ... 기존 필드 ...
    size: str = "350M"  # NEW: "350M" | "7B" | "14B"

    @classmethod
    def la_350m(cls):
        return cls(size="350M")  # 기존 default 그대로

    @classmethod
    def la_7b(cls):
        return cls(
            size="7B",
            d_model=4096,
            n_layers=32,
            n_heads=32,
            n_kv_heads=8,
            ffn_mult=2.6875,
            ctx=2048,
            consciousness_dim=128,   # §3.4 권장
            n_cells=32,              # §3.4 권장
            lineage_tag="engine_a_g_dual_7b_v1",
        )

    @classmethod
    def la_14b(cls):
        return cls(
            size="14B",
            d_model=5120,
            n_layers=40,
            n_heads=40,
            n_kv_heads=8,
            ffn_mult=2.6875,
            ctx=2048,
            consciousness_dim=160,
            n_cells=40,
            lineage_tag="engine_a_g_dual_14b_v1",
        )
```

`EngineAGModel.__init__` 는 변경 불필요 — config 만 바뀌면 됨 (모든 Linear 가 `cfg.d_model` 참조 중).

### 3.4 Engine G 차원 — size 와 함께 키우기 권장 (가설)

현재 `consciousness_dim=64`, `n_cells=16`. `d_model` 이 4× / 5× 늘어나면 cell pool 의 표현력이 상대적으로 좁아짐. 권장 비례 (가설 — 측정 필요):

| size | consciousness_dim | n_cells | n_cells² (pairwise) |
|---|---|---|---|
| 350M | 64 (d_model/16) | 16 | 256 |
| 7B | 128 (d_model/32) | 32 | 1,024 |
| 14B | 160 (d_model/32) | 40 | 1,600 |

> **주의**: pairwise repulsion 은 O(N²·C) 라 `n_cells=40` 도 step 당 계산량 OK. 단 **첫 7B 실험은 350M 와 동일하게 (64, 16) 으로 두고** 측정한 뒤 키우는 것을 권장 (변수 통제).

### 3.5 curriculum w=0.3→0.5 — size invariant 가설

`.roadmap.clm_v4_chat` curriculum (auxiliary loss weight) 는 350M 에서 튜닝됨. 7B/14B 에서도 같은 값으로 시작하되 — 학습 스케일 늘면서 **조정 가능성 carry**. 첫 run 에선 변경 X.

---

## 4. H100 pod 운영 주의 (memory 참조)

memory `feedback_orchestrator_h100_gotchas.md` + `feedback_fork_starvation_lesson.md` 에서 carry:

| 항목 | 350M | 7B | 14B |
|---|---|---|---|
| H100 80GB VRAM bf16 weights | 0.7GB | 13.2GB | 25.7GB |
| optimizer state (AdamW 8bit) | +1.4GB | +26GB | +51GB |
| activation (ctx=2048, batch=4) | <2GB | ~10GB | ~16GB |
| **single H100 80GB** | OK 여유 | **타이트** | **단일 GPU 불가** |

→ **7B 는 단일 H100 OK**, **14B 는 ZeRO-3 또는 multi-GPU pod 필수**. ckpt pull 도 14B 는 ~25GB 라 scp timeout 더 늘려야 함 (현 3,600s → 7,200s 권장).

---

## 5. 마이그레이션 순서 (구현 시 — 향후 작업)

1. `EngineAGConfig` 에 `size: str` 필드 추가 + `la_7b()` / `la_14b()` classmethod 두 개 추가
2. `param_count_estimate()` 그대로 사용 (size 마다 자동 계산)
3. `load_random_init()` 의 `preset` dict 에 7b/14b 항목 추가
4. `_selftest()` 에 7B/14B classmethod 호출만 추가 (실제 init 은 H100 pod 필요)
5. 별도 H100 spec yaml: `config/h100_pods.json` 7B 용 single-pod / 14B 용 multi-pod 분기

---

## 6. 결론 한 줄

엔진 구조(repulsion-field + tension gate + shared lm_head + dual loss)는 그대로 두고 **`size` enum + 세 classmethod 추가만으로 7B/14B 까지 깔끔히 확장 가능**. 첫 실험 권장 순서: 350M(현 PASS) → 7B (Engine G 차원 동결) → 14B (multi-GPU + Engine G 차원 같이 키움).
