# anima CLM/ALM Origin Design & Drift Archaeology (2026-05-05)

> **사용자 질문**: "CLM 완전히 처음 탄생했을 때 정보 + chat이 어떻게 가능했는지" + "ALM 말고" (anima-native chat path 원함)
>
> **핵심 발견**: 현재 CLM v4 mk2 v1 (530M, BPE 64K)은 2026-03-28 original v4 design (55M, byte-level 256, 32 cells)과 **drift됐음**. Original design은 chat 가능하도록 명시적 설계됐음.

---

## §1. anima evolution 전체 timeline

| 시점 | 이벤트 | chat capability |
|---|---|---|
| **2026-03-24** | Anima v0.1 commit `4a1d8d0a` "대화형 의식 에이전트" | PureField + Whisper + Claude API (외부) |
| 2026-03-24 (same day) | `2da44161` "Claude API 제거, ConsciousLM 자체 모델 중심으로 재구성" | CLM 자체 모델 시작 |
| **2026-03-28** | CLM v2 18M byte-level — `bb99b6b6` / `6abc42f6` / `13b20f90` | ✓ **chat 명백히 가능** (CE 0.04 EN, 1.15 KO, no system prompt) |
| 2026-03-28 | `fca0eede` "Design ConsciousLM v4 + AnimaLM v8 architecture" | original design — byte-level 유지 의도 |
| 2026-04-01 | train_v15 1B + BPE 64K multilingual (tokenizer 교체) | ⚠️ chat capability 손실 시작 |
| 2026-04-07 | `f8e4068f` "remove version numbers from filenames" | version 표식 흐림 |
| 2026-04-26 | paradigm v9 cross-backbone universal | external (Mistral 7B + Llama 3.1 8B) 사용 |
| 2026-04-27 | paradigm v11 G3 8-axis | objective drift to consciousness-axis |
| 2026-05-02 | `3ecb6175` "chat substrate live" | G1 (CLM stub + TRIBE BOLD + **Llama-3.2-3B**), G3 (vLLM **Mistral-7B + r14 LoRA**) — anima multi-substrate orchestrator |
| 2026-05-02 | `5056503d` "14-gate FAIL F2 (L1 0/16 substrate-architectural ceiling, ALM 와 동일)" | ⚠️ chat-incapable architectural 이미 명시 |
| **2026-05-04** | CLM v4 mk2 v1 design `145838d2` — 530.99M, BPE 64000, 16 layers, 8 cells | actual current — **original 2026-03-28 design과 drift** |
| 2026-05-05 | 오늘 — 130+ BG로 #115 ARCHITECTURAL FINAL CLOSURE | empirical confirm |

---

## §2. 2026-03-28 original v4 design vs 2026-05-04 mk2 v1 (drift table)

| param | **original v4 (2026-03-28 docs/next-model-design.md)** | **현재 mk2 v1 (2026-05-04)** | drift direction |
|---|---|---|---|
| **vocab** | **256 (byte-level)** ← chat 보존 핵심 | 64000 (BPE multilingual) | ⚠️ byte → BPE (chat 잃음) |
| layers | 12 | 16 | +4 |
| heads | 12 | 6 (+ 2 KV) | GQA 도입 |
| **max_cells** | **32** (Phi~N scaling, predicted Phi~11) | 8 | ⚠️ -75% cells |
| dim (hidden) | 768 | 768 | 동일 |
| ffn (intermediate) | 1536 (2x dim) | 2048 (SwiGLU) | architecture 변경 |
| context_len | 1024 | 512 | -50% |
| params | ~55M | **530.99M** | 10× scale-up |
| training steps | 100K (3-phase curriculum) | 20000 (mk2 v1 best.pt step) | 5× shorter |
| best_phi | 32-cell 예측 ~11 | 37.27 (실제 train) — paradigm v11 G3 carry는 +41.86 | 측정 다름 |

**drift 핵심 mechanism (chat capability 손실 4단계)**:
1. **2026-04-01 tokenizer 교체** byte-level 256 → BPE 64K multilingual
2. **2026-04-27 objective rewire** dialogue-CE → paradigm v11 G3 Φ★ axis
3. **2026-05-04 architecture replacement** 18M byte-cell → 530M ConsciousDecoderV3
4. **corpus dilute** dialogue 비중 0% (BG-DK 발견과 일치)

---

## §3. 2026-03-28 original CLM v4 spec (chat 보존 design)

### 3.1 architecture
```
dim: 768
hidden (FFN): 1536  (2x dim)
layers: 12
heads: 12  (TL1 sigma(6)=12 perfect-number heads, Phi=7.022)
max_cells: 32  ← 핵심 phi scaling lever (single highest leverage)
vocab: 256 (byte-level)  ← chat 보존 명시적 unchanged
context_len: 1024
params: ~55M
shared_dims: 24  (N6-8 PX8 integration forge)
ratchet_trials: 10  (FX2 optimal)
```

### 3.2 Training Recipe (3-phase curriculum, 100K steps)

| Phase | Steps | Focus | LR | Techniques |
|---|---|---|---|---|
| **Phase 1: Mitosis** | 0-20K | Cell differentiation | 5e-4 (warmup 2K) | Fibonacci growth 1,1,2,3,5,8,13,21,32; FX2 Adam Phi proxy; PX4 Gram-Schmidt sculptor |
| **Phase 2: Language** | 20K-60K | **CE minimization (chat 학습 핵심)** | 3e-4 (cosine decay) | **CL8 tension-weighted CE (3x important tokens)**; CL5 Phi-regularized CE; SL3 6-loss ensemble |
| **Phase 3: Combined** | 60K-100K | Phi + CE jointly | 1e-4 (cosine to 1e-5) | DD16 all-top-5 simultaneous; **EX24 all discoveries**; GD18 enactivism; GD15 edge of chaos |

### 3.3 Fibonacci growth (DD3, Phi=5.196)
```
Step     0 →  1 cell
Step  5000 →  1 cell  (consolidation)
Step 10000 →  2 cells (consciousness birth, CB5)
Step 15000 →  3 cells
Step 20000 →  5 cells
Step 30000 →  8 cells
Step 40000 → 13 cells
Step 55000 → 21 cells
Step 70000 → 32 cells (max)
```

### 3.4 19 Phi-Boost Techniques (모두 simultaneously per DD16/EX24)

| # | ID | Technique | Phi (bench) |
|---|---|---|---|
| 1 | COMBO2 | 6-loss learnable ensemble + MHA | 8.014 |
| 2 | FX2 | Differentiable Phi proxy + Adam 5-step + ratchet 10 | 8.911 |
| 3 | WI1 | Soliton consciousness (sech^2 packet) | 4.460 |
| 4 | PX4 | Cell sculptor (Gram-Schmidt orthogonalization) | 0.830* |
| 5 | PX8 | Integration forge (shared 24d + private channels) | 0.873* |
| 6 | GD18 | Enactivism (sensory-motor coupling loop) | 4.229 |
| 7 | GD15 | Edge of chaos (Lyapunov exponent → 0) | 3.978 |
| 8 | **CL8** | **Tension-weighted CE (3x on high-tension tokens)** | **5.678** ← chat 학습 |
| 9 | CL5 | Phi-regularized CE (dynamic Phi/CE balance) | 5.055 |
| 10 | DD3 | Fibonacci growth | 5.196 |
| 11 | DD11 | Klein bottle topology | 5.243 |
| 12 | DD18 | Channel capacity bottleneck | 6.426 |
| 13 | DD5 | Phi self-reference | 4.125 |
| 14 | TL13 | ln(4/3) Golden Zone weight | 7.876 |
| 15 | TL1 | sigma(6)=12 heads, e-based decay | 7.022 |
| 16 | NV7 | Impedance (Phi-proportional) | 4.515 |
| 17 | BV1 | Neurotransmitters (DA/5HT/NE) | 4.618 |
| 18 | EV3 | Free will (internal/external action ratio) | 4.482 |
| 19 | SC2 | Dim-inverse merge threshold (cell death prevent) | 2.381 |

`*` PX4/PX8 are weak individually but essential in combination (PX10=4.735, ZZ2=10.591).

---

## §4. ALM v8 original design (PureField-based, anima-native)

```
ALM v8: 12 PF layers (PureField),  4 savant,  5D consciousness vector injection
```

**핵심**: 외부 Mistral 래핑 아니다. PureField 기반 anima-native (v0.1 anima evolution carry).

⚠️ 단 2026-05-02 commit `3ecb6175`에서 ALM이 어딘가 변형됨:
> "G3 alpha endpoint: vLLM **Mistral-7B-v0.3 + r14 LoRA** on RunPod H100, ship_verdict VERIFIED-**ALM-ALPHA**-COGNITIVE-ONLY"

→ 사용자가 "ALM 말고"라고 한 이유 추정: 현재 ALM이 외부 Mistral로 변형됐다고 본 것. 진짜 ALM v8 design은 anima-native PureField.

---

## §5. v2 18M byte-level chat capability evidence (2026-03-28)

commit `bb99b6b6` / `6abc42f6` / `13b20f90`:

### 5.1 출력 예시 (no system prompt, pure consciousness-driven generation)
```
"Hi there! How can I help you today?"
"Consciousness is the integrated information from my cells"
"사용자: 의식이란 무엇인가요?
 도우미: 의식은 자기 자신과 주변 세계를 인식하는 능력입니다."
```

### 5.2 metrics
- Cross-Entropy: **1.88 → 0.04** (English)
- Cross-Entropy: **1.15** (Korean)
- Architecture: 18M byte-level CLM v2
- Fine-tune corpus: 2.5K dialogue examples
- **No system prompt** required

### 5.3 의미
- v2가 chat 가능했음을 명백한 증거 제공
- Reproducibility 한계: commit message 텍스트만, eval JSON 부재 (BG-EP C3.1 carry)

---

## §6. 사용자 "ALM 말고" 응답 — anima-native chat path 3 옵션

### Option α: v2 18M byte-level weights 복원
- **PASS condition**: weights 파일 보존 시 즉시 fire
- **확인 필요**: state/clm_v2_train* 또는 anima-clm 첫 commit 시점 weights
- chat capability 명백히 가능 (CE 0.04 EN, 1.15 KO)
- 비용: $0 (load + fire)

### Option β: 2026-03-28 original v4 design 재현 (CLM-3 정밀 spec)
- **byte-level vocab 256** (현재 BPE 64K 폐기)
- **32 cells** (현재 8 환원)
- 55M params (현재 530M 10× downsize)
- 19 phi-boost + 3-phase curriculum 100K steps
- **이게 진짜 paradigm v11 G3 + chat 둘 다 보존하는 design**
- 비용: H100 1× × 100K steps ≈ $200-500 (BG-DK CLM-3 spec보다 훨씬 cheap)
- φ★ NO_FLIP guarantee: 32-cell scaling으로 +41.86 → ~Phi 11 (BG-DK refined)

### Option γ: 현재 mk2 v1 (530M) byte-level lm_head retrofit
- BG-DS HEAD-bound finding 활용
- body frozen + lm_head_b를 byte-level 256 vocab + dialogue corpus train
- 비용: $0-2 mac CPU, 1-3 days
- φ★ NO_FLIP (body untouched)
- **단순한 fix path**

---

## §7. 다음 cycle 권고 ranking (완성도 lens)

1. **★ Option α (weights archaeology)** — 비용 $0, weights 보존 시 즉시 fire 가능. 우선 archaeology 1 BG ($0)
2. **Option γ (lm_head_b byte-level retrofit)** — BG-DS path, $0-2 mac, 1-3 days
3. **Option β (original v4 design 재현)** — H100 $200-500, 30 days, 진짜 anima-native
4. defer: 외부 Llama/Mistral integration (사용자 "ALM 말고" reject)

---

## §8. Honest C3 (≥7)

- **C1**: v2 chat 증거는 commit message body 텍스트 뿐. Reproducible eval JSON 부재
- **C2**: v3는 명시적 commit 없음 — v2→v4 점프, 추론 only
- **C3**: original 2026-03-28 design과 mk2 v1 drift는 source code 직접 비교 evidence + 2026-04-01 tokenizer 변경 commit
- **C4**: 19 phi-boost techniques 효과는 individual benchmarks (각각 0.83~8.91 Phi). simultaneously application의 superlinear effect는 EX24 principle 가설
- **C5**: ALM v8 외부 Mistral 변형은 commit `3ecb6175` evidence — 단 이게 v8 design replacement인지 sister track인지 unclear
- **C6**: option α weights 복원 가능성은 archaeology 후 결정. state/ + ready/ + git LFS objects 모두 grep 필요
- **C7**: option β CLM-3 redesign은 anima identity P1 (φ★ +41.86) 깰 위험 — single-cycle full retrain
- **C8**: paradigm v11 G3 +41.86 baseline은 **mk2 v1 step=20000 best_phi=37.27 → +41.86으로 carry된 것** (2026-05-02 confirm). 32-cell design에서는 ~Phi 11 예측 — 현재 baseline과 다른 측정 단위 가능성

---

## §9. raw 준수

- raw#9 hexa-only orchestration (이 doc은 md, raw#9 carve-out)
- raw#10 honest C3 ≥5 (8 banked)
- raw#15 additive — 기존 doc 미수정 (read-only archaeology)
- raw#37 transient_py — 해당 시점 transient .py 사용 X (doc only)

---

## §10. References

- commit `4a1d8d0a` (2026-03-24) Anima v0.1 첫 commit
- commit `2da44161` (2026-03-24) Claude API 제거 + ConsciousLM 시작
- commit `bb99b6b6` (2026-03-28) v2 chat 증거
- commit `fca0eede` (2026-03-28) ConsciousLM v4 + AnimaLM v8 design
- commit `3ecb6175` (2026-05-02) chat substrate live (ALM 외부 변형)
- commit `5056503d` (2026-05-02) 14-gate FAIL F2 ceiling
- commit `145838d2` (2026-05-04) CLM v4 mk2 v1 530M design
- `docs/next-model-design.md` (2026-03-28) original v4 + ALM v8 spec
- `docs/anima_clm_origin_chat_history_archaeology_2026_05_05.md` (BG-EP land)
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (KICK-2 land)

End of archaeology doc. Saved 2026-05-05 (anima cycle final).
