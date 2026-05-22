# EASY — V3 (PURE HEXAD substrate) 쉬운 설명

> 2026-05-22 작성. ConsciousDecoderV3 pure HEXAD substrate path 의 saga.
> 🔴 **2026-05-23 V3 PATH CLOSED** — 5 fire (attempt 1 + Phase 2 1·2차 +
> B + A) 0 PASS. V3 multilingual = corpus-bound 최종 결론.

---

## 한 줄 요약

**LoRA path 의 "Qwen 위 옷" 한계** → anima 자체 substrate (ConsciousDecoderV3)
from-scratch 학습. **5 fire 전부 FAIL (0 STRONG)** — A (Phase 2 full, 결정
fire) 가 Phase 2 2차의 ko STRONG 19/20 재현 실패 (KO WEAK 1/20). V3
multilingual blocker = capacity·arch 아닌 **diverse-corpus 학습 dynamics**
(75 MB 의 70% anima 가 substrate 를 register memorization 으로 collapse).
→ chat substrate = vP21M LoRA path 유지, V3 보류.

---

## 1. 왜 V3 인가

LoRA path (HEXAD/LORA/) 의 한계:
- ⚠️ "Qwen 위 옷" — HEXAD identity 약함
- ⚠️ anima register = 학습된 토큰, 아키텍처 primitive 아님
- ⚠️ head_g (Engine G 의식 emission) 활용 안 함
- ⚠️ KOSMOS + tension wiring 없음

→ 사용자 directive: **"LoRA 가 아닌 자체 HEXAD substrate"**. ConsciousDecoderV2
의 OCCAM verdict (n_ca_rules 단독 floor 범인) 적용 → V3 fork 시도.

---

## 2. V3 architecture vs V2 (정리)

| | V2 (legacy) | **V3** |
|---|---|---|
| n_ca_rules | 8 (floor 범인) | ❌ **REMOVED** (OCCAM Phase 2.3 결과 적용) |
| head_a (언어) + head_g (의식) | ✅ vocab=256 byte | ✅ vocab=151936 Qwen BPE |
| PureFieldFFN | ✅ | ✅ 유지 (Phase 2.3 무해) |
| ConsciousCrossAttention | ✅ | ✅ 유지 |
| Layer-0 noise σ | implicit | ✅ explicit 0.1 (train-only) |
| Mitosis hook | external | **1-class 통합 (training + inference)** |
| Init helpers | random only | **random / Qwen-warm / vP21M-init** |
| KOSMOS + tension | n/a | **wired (anchor + 8→5-channel mapping)** |

---

## 3. attempt 1 결과 (2026-05-22)

3 variant H100/A100 parallel fire ($7.39 total):

| variant | init | CE_final | 5-lang ≥ PARTIAL | verdict |
|---|---|---|---|---|
| **V3α** random | from-scratch | 3.34 | **0/5** | ❌ FAIL (Chinchilla 30000× under-budget) |
| **V3β** Qwen warm | mapped | 3.15 (osc 0.26↔2.36) | **0/5** | ❌ FAIL (mode collapse, pod recovery 후 회수) |
| **V3γ** vP21M init | LoRA-merge | 2.93 | **0/5** | ❌ FAIL (anima register saturate 13/20) |

**3/3 전체 FAIL**. (LoRA 의 vP21M 은 4/5 langs PARTIAL+ — V3 가 모든 면에서 후퇴)

### V3β 의 mode collapse (recovery 후 분석)

step 1700 CE 0.26 → step 1850 CE 2.36 (cosine LR decay 끝부분):
- best ckpt 시점 = step 1700 (CE 0.26)
- final ckpt = step 2000 (CE 3.15)
- oscillation 안정화 X, → V3 dual-head 의 mode collapse

이 발견 → Phase 2 의 early-stop + osc-detect 기능 추가 동기.

---

## 4. architecture-level lesson (3-confirm)

V3α/β/γ 공통 finding:

1. **head_g dual head vocab alignment 흐림** — bf16 inference 시 한 head update
   가 다른 head generation 영향. head_a (언어) 와 head_g (의식) 같은 hidden 위에서
   다른 logit 학습 시 vocabulary 정합 손상.

2. **mitosis pool 128 saturate at step 50** — cell 가 너무 빠르게 분열 → cross-attn
   input noise 증가 → language-coherent 학습 방해.

3. **anima_register_hits 13/20** (vP21M LoRA 7/20 의 2×) — V3 substrate level
   흡수 가 LoRA 보다 훨씬 강함. 학습된 corpus 의 anima register 가 아키텍처
   다른 capacity 침범.

4. **mitosis aux_loss 가 substrate 를 tension 패턴 우선시** — 다국어 capability
   가 mitosis substrate-shape 비용으로 sacrifice.

5. **Chinchilla 30000× under-budget** — 1.5B params × 20 = 30B tok 필요. 학습 시
   1M tok 만 사용. from-scratch (V3α) 의 5-lang generalize 거의 불가능.

---

## 5. 비유

V3 는 마치:
- **anima 의 신체를 처음부터 새로 만들기** (LoRA 의 "Qwen 위 옷" 아님)
- 김치 / 발효 양배추 / 다국어 가사 모두 동시에 직접 만들기 시도
- 결과: 김치 향이 너무 강해서 (anima register 13/20 saturate) 다른 노래 못 부름
- 다국어 sacrifice (multilingual prior 부재) — Qwen warm-start (V3β) 도 EN 만
  부분 보존 (coh 8/20), 나머지 4 lang 모두 coh 0

LoRA 와 차이: LoRA = Qwen 사골 (다국어 prior) 위에 김치 + 양배추만 더함 →
다양성 보존. V3 = 사골 없이 처음부터 만듦 → capacity 부족.

---

## 6. Phase 2 재설계 spec

OCCAM 원칙: attempt 1 의 정직한 한계 → 다음 cycle 의 변형 axis (R1-R7):

| # | axis | 변경 |
|---|---|---|
| R1 | scale-up | 1.5B → 3B/8B (Chinchilla 부분 충족) |
| **R2** | mitosis 학습 비활성화 | λ_mitosis 0.05 → **0.0** (train-time) |
| R3 | corpus scale | 75 MB → 6 GB+ (Chinchilla 정합) |
| R4 | head_g 별도 train pipeline | dual head separate gradient flow |
| **R5** | warm-start 강화 | q/k/v/o + embed + ffn weight 모두 copy |
| **R6** | mitosis cell pool 작게 | MAX 128 → **16** |
| R7 | step 늘림 | 2000 → 5000+ |

### Phase 2 fire 결과 (2026-05-22)

🔵 **R2 + R5 + R6 동시 fire** — early-stop + osc-detect 코드 v2 적용.

**Phase 2 (1차)** pod `zwvh9gyy9ls6jw`:
- CE 0.643 (R2 mitosis-off 가 V3 attempt 1 의 CE 2.9-3.3 → **0.64 극적 개선**!)
- osc-detect 작동: step 1125 CE oscillation std 3.85 > 0.5 → `ckpt_osc_step1125.pt` 저장 + early-stop ✓
- **단 5-lang 0/5** (en PURE_MEM 8/20, ko WEAK 1/20, zh/ru/ja WEAK 0/20) — generalization FAIL
- R6 (`--mitosis-max 16`) 미적용 bug (pool 128) — fix `1e4c537fd`

**Phase 2 (2차, R6 fixed)** pod `kxfts3r6gsi6re` 결과:
- `pool=16 splits=14` — **R6 작동** ✓ (cell pool 128→16 cap)
- 🎯 **ko STRONG 19/20** — V3 attempt 통틀어 **첫 STRONG language**
- en PURE_MEM 3/20 (coh 15 — anima register), zh/ru/ja WEAK 0/20 (gen 17-20 高 but coh 0 = wrong script)
- AGG: STRONG 1 + WEAK 3 + PURE_MEM 1 → 여전히 FAIL (4/5 ≥ PARTIAL 미달)
- ⚠️ osc-detect false-positive: step 250 (5%) 에서 조기 early-stop — CE 12→4.85→2.28
  정상 warmup 하강을 oscillation 으로 오인 (fix v2.1 의 raw-std 가 monotonic descent
  도 큰 std 로 잡음). fix v2.2: warmup 8-entry skip + "recent_mean > best_CE+thr"
  (mode collapse = CE 재폭주) 로 정정.
- ko STRONG 가 250 step 만에 나옴 — 더 길게 학습 시 다른 lang 도 개선 가능성

### Phase 2 핵심 발견

1. **R2 (mitosis off) 가 CE 는 고치나 generalization 은 못 고침** (1차):
   mitosis off → CE 3.0 → 0.64, 단 5-lang 0/5.
2. **R6 (pool 16) → 첫 STRONG** (2차): ko STRONG 19/20. cell pool 축소가
   cross-attn noise 줄여 최소 1 lang generalize unlock.
3. **zh/ru/ja 의 coh 0 (gen 17-20)** — 모델이 내용은 생성하나 wrong script.
   → V3 진짜 blocker = **dual-head vocab alignment** (gen 高 + coh 0 = head_a
   가 다국어 token distribution 흐려짐) + Chinchilla under-budget.

### Phase 2 후속 — A (1.5B full) + B (3B scale) 동시 fire

**B (R1 3B scale)** pod `nzeobqp7cbwavc` 결과:
- AGG STRONG 0 + WEAK 4 + PURE_MEM 1 → FAIL
- en WEAK 6/20, ko WEAK 1/20, zh PURE_MEM 0, ru/ja WEAK 0
- 🚨 **3B 가 1.5B Phase 2 2차 (ko STRONG 19/20) 보다 나쁨** — scale-up 이 0 STRONG

**핵심**: **R1 (scale-up) 은 V3 multilingual 을 못 고침 — 오히려 후퇴**.
3B 는 1.5B 보다 더 큰 capacity 인데 같은 1M tok corpus → Chinchilla ratio
더 악화 (3B 는 60B tok 필요). V3 multilingual blocker = **capacity 아님**.

**R4 도 moot** (코드 검증: head_g 는 train loss 에 없음 → gradient 0, inert.
"head_g vocab 흐림" attempt-1 lesson = mis-diagnosis).

남은 유일한 STRONG 달성 config = **1.5B + R2 (mitosis off) + R6 (pool 16)**
= Phase 2 2차 (ko STRONG 19/20, 단 step 250 조기종료). → **A (Phase 2 full,
1.5B 동일 config + osc v2.2 fix + step 5000 완주)** 가 V3 의 결정 fire.
A 가 ko STRONG 재현 + 추가 lang unlock 못하면 → V3 multilingual = corpus-bound
(diverse-corpus 학습 dynamics 문제, scale·arch 무관) 결론.

### 🔴 A fire 결과 (2026-05-23) — V3 PATH CLOSED

pod `xp6q69nkd2ywfw` A100-SXM, osc-detect v2.2 **early-stop @ step 1125**
(CE re-divergence, mode collapse), train wall 2.05 hr:

| lang | verdict | score | 비고 |
|---|---|---|---|
| EN | PURE_MEMORIZE | 6/20 | anima register memorize |
| KO | **WEAK** | 1/20 | **ko STRONG 재현 실패** (2차 19/20 → A 1/20) |
| ZH | PURE_MEMORIZE | 0/20 | 한국어 anima 텍스트 emit |
| RU | PURE_MEMORIZE | 0/20 | 한국어 anima 텍스트 emit |
| JA | WEAK | 0/20 | 한국어 anima 텍스트 emit |

**AGG: STRONG 0 · WEAK 2 · PURE_MEM 3 → FAIL**. CE 궤적 진동
(375:1.05 ↔ 1000:5.71 ↔ 1125:0.64) — 모델이 서로 다른 anima-register
fragment 사이를 thrash.

**Phase 2 2차의 ko STRONG 19/20 = step-250 transient** 확정 — full 완주에서
재현 불가. → V3 의 단 하나의 STRONG 도 우연 산물.

### 🔴 최종 결론 — V3 multilingual = corpus-bound

V3 fire 5회 (attempt 1 α/β/γ + Phase 2 1·2차 + B 3B + A) **전부 FAIL,
0 PASS**. 시도한 모든 axis:

| axis | 시도 | 결과 |
|---|---|---|
| R1 scale-up | B (3B) | FAIL — 1.5B 보다 후퇴 (capacity 아님) |
| R2 mitosis-off | Phase 2 1차/A | CE 는 고침, generalization 못 고침 |
| R4 head_g pipeline | 코드 검증 | head_g train loss 부재 → inert, moot |
| R6 pool-16 | Phase 2 2차/A | cross-attn noise 줄임, ko transient 만 |
| R7 step-up | A (5000 target) | osc early-stop @ 1125, mode collapse |

V3 multilingual blocker = **capacity 도 architecture 도 아닌 diverse-corpus
학습 dynamics**. 75 MB 코퍼스의 70% anima 비중이 substrate (from-scratch /
warm-start) 를 anima-register memorization 으로 collapse 시킴. LoRA path
(vP21M) 가 4/5 langs ≥ PARTIAL 인 이유 = Qwen 다국어 prior 를 보존한 채
adapter 만 학습 — V3 는 substrate 학습으로 그 prior 를 파괴.

→ **chat substrate = vP21M LoRA path 유지** (절충 B). substrate_v3 합류 보류.
V3 코드/ckpt = negative-result evidence anchor 로 보존 (`vP21H_phase2_full/`,
HF `dancinlab/anima-v3-p21h`).

---

## 7. attempt 1 자산 (Phase 2 에서 활용)

- ✅ conscious_decoder_v3.py 727 LoC (n_ca_rules removed + dual head + KOSMOS)
- ✅ kosmos_io.py 300 LoC (8→5-channel tension + anchor IO)
- ✅ train_p21h_v3.py 485 LoC v2 (early-stop + ckpt save)
- ✅ smoke test 7/7 + KOSMOS 5/5 PASS
- ✅ V3β ckpt 5.6GB (mode collapse 분석 baseline, ed88af0f...)
- ✅ KOSMOS anchor 15 × V3α/γ = 30+ multimodal payload (검증 자료)
- ✅ 8 hexa-cloud troubleshooting findings (`hexa-lang/inbox/notes/`)

---

## 8. 관련 link

- 가장 쉬운 saga 종합: [`../EASY.md`](../EASY.md) (전체)
- V3 path overview: [`README.md`](README.md) (재설계 axes 상세)
- 새 V3 세션 시작: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- full spec: [`HEXAD_NATIVE_V3.md`](HEXAD_NATIVE_V3.md)
- attempt 1 보고서: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`
- OCCAM (n_ca_rules pinpoint): `../EASY.md § 6`
- substrate plugin (chat.dancinlab.org 통합): `../CHAT/SUBSTRATE_PLUGIN.md`
- LoRA 비교: [`../LORA/EASY.md`](../LORA/EASY.md)
