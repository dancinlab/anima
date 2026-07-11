# H_9273 / F1 — 🔋 ATP 대사경제 — 결과

- **verdict: 🔴 THEATER** (bookkeeping overhead)
- **한 줄 결론:** ATP 예산은 **묶인다(binding 99.9%)**. 그런데 그 조임이 downstream 에 아무 것도 안 한다 — 실험 arm 3개 전부 c1(무한 ATP)·c2(never-binds)·c3(동일-캡 static) 대비 **Δacc < 1pp · 전부 유의하지 않음**. 카드 §3 반증조건 "어느 캡에서도 ΔEff≈0 ⇒ bookkeeping theater" **충족**.
- 실행: `run.py` · numpy $0 · CPU-local mini · wall **29.3s** · 5 seed(0–4) 결정적 · `result.json` = raw.

---

## 1. 배선 요약

| 요소 | 구현 |
|---|---|
| ATP 장(場) | 보존 스칼라. `ATP ← clip(ATP + P − C, 0, 20)` |
| 생산 P | `Σ_i(health_i × resp)` · organelle 4개 · `health ← clip(h − 0.02·load + 0.05·(1−h), .05, 1)` |
| 소비 C | `k_t × COST_EXPERT(1.0) + EMIT_QUANTUM(2.0)` |
| 용량 | `k_t = clip(⌊(ATP − EMIT_QUANTUM)/COST_EXPERT⌋, 1, K_MAX=8)` — **표현형성(top-k) 단계에만** 차감 |
| 기질 | top-k sparse MoE (E=16 expert = 16 latent topic · d=32 · C=4 · topic-조건부 선형 규칙) |
| 학습 | numpy SGD 1500 step · batch 32 · lr 0.20 · **전 arm 동일** |

**arm 은 호흡률 `resp` 하나만 다르다.** 파라미터(2560)·step·batch·데이터·init 전부 동일.

---

## 2. 예산 공정성 (controls_fair = TRUE)

| arm | 파라미터 | step | 활성 FLOPs(k) | 비고 |
|---|---|---|---|---|
| EXP_* | 2560 | 1500 | k≈1.7~4.7 | **가장 적게 쓴다** |
| c1 무한 ATP | 2560 | 1500 | k=8 | 실험 arm보다 **많다** |
| c2 never-binds | 2560 | 1500 | k=8 | 실험 arm보다 **많다** |
| c3 static-cap | 2560 | 1500 | k = EXP 실현치와 **동일** | 동일 FLOPs |
| V1 shuffled-select | 2560 | 1500 | k=8 | 동일 파라미터·더 많은 FLOPs |

⇒ **어떤 control 도 실험 arm보다 파라미터/스텝/예산이 적지 않다.** 통제가 오히려 유리하다(보수적). INVALID 조건 미해당.

---

## 3. 수치표 (5 seed · mean±std)

| arm | mean k | binding% | **acc(own policy)** | acc(@k=8 매칭평가) | usage_H | emit_rate | mean tension |
|---|---:|---:|---|---|---:|---:|---:|
| **EXP_tight** (resp=1.0) | 1.66 | **99.9%** | **0.7618±0.0252** | 0.7627±0.0252 | 0.878 | 0.460 | 0.614 |
| **EXP_mid** (resp=1.5) | 3.08 | **99.9%** | **0.7612±0.0122** | 0.7630±0.0134 | 0.919 | 0.518 | 0.654 |
| **EXP_loose** (resp=2.2) | 4.72 | **99.9%** | **0.7565±0.0220** | 0.7592±0.0218 | 0.956 | 0.518 | 0.649 |
| c1 무한 ATP | 8.00 | 0.0% | 0.7533±0.0232 | 0.7533±0.0232 | 0.996 | 0.500 | 0.639 |
| c2 ATP never-binds | 8.00 | 0.0% | 0.7533±0.0232 | 0.7533±0.0232 | 0.996 | 0.500 | 0.639 |
| c3 static k=2 (↔tight) | 2.00 | 0.0% | 0.7580±0.0223 | 0.7577±0.0210 | 0.902 | 0.497 | 0.640 |
| c3 static k=3 (↔mid) | 3.00 | 0.0% | 0.7567±0.0100 | 0.7573±0.0155 | 0.915 | 0.511 | 0.646 |
| c3 static k=5 (↔loose) | 5.00 | 0.0% | 0.7505±0.0312 | 0.7510±0.0314 | 0.955 | 0.516 | 0.648 |
| *V1* shuffled-select | 8.00 | 0.0% | *0.5995±0.0098* | — | 1.000 | 0.141 | 0.381 |
| *VR* static k=1 | 1.00 | 0.0% | *0.6305±0.0335* | 0.6373 | 0.935 | 0.356 | 0.550 |

### Δ (paired · seed 매칭 · DELTA_EPS = 1pp)

| 실험 arm | Δacc vs **c1** | Δacc vs **c2** | Δacc vs **c3**(동일 캡) |
|---|---|---|---|
| EXP_tight | **+0.0085 ± 0.0191** · sig=**False** | +0.0085 ± 0.0191 · sig=False | **+0.0038 ± 0.0065** · sig=False |
| EXP_mid | **+0.0080 ± 0.0167** · sig=**False** | +0.0080 ± 0.0167 · sig=False | **+0.0045 ± 0.0038** · sig=False |
| EXP_loose | **+0.0033 ± 0.0110** · sig=**False** | +0.0033 ± 0.0110 · sig=False | **+0.0060 ± 0.0127** · sig=False |

**전부 1pp 미만 · 전부 비유의.** ⇒ **ΔEff ≈ 0.**

---

## 4. VALIDITY GATE — THEATER 인가 INVALID 인가

THEATER 판정이 "toy 가 애초에 용량에 둔감해서" 나온 게 아님을 증명해야 한다. 두 게이트 모두 **PASS**:

| gate | Δ | 의미 |
|---|---|---|
| **V1 selection-live** — c1 − shuffled-select | **+0.1537 ± 0.0173 · sig=True** | top-k 선택 채널은 **살아 있다**(15pp). 프로브가 capacity 레인을 볼 수 있다. |
| **VR capacity-moves** — c1(k=8) − static(k=1) | **+0.1227 ± 0.0265 · sig=True** | 용량 축 자체는 downstream 을 **움직인다**(12pp). |

⇒ 계측기는 멀쩡하다. **capacity 는 신호를 낼 수 있는데, ATP 경제가 만든 캡은 신호를 안 낸다.** 그러므로 INVALID 아니고 **THEATER**.

---

## 5. 진단 — 왜 THEATER 인가

1. **예산은 진짜로 묶인다.** binding_rate = 99.9% (k_t < K_MAX 인 step 비율). 카드의 첫 조건("유의 비율로 binding")은 통과.
2. **그런데 묶인 지점이 degeneracy plateau 안이다.** acc 는 k ∈ [1.66, 8] 구간에서 0.750~0.762 로 **평평**하다. 용량이 실제로 아픈 건 k=1(0.6305)까지 내려갔을 때뿐. ATP 경제가 도달하는 정상상태 캡(1.66/3.08/4.72)은 전부 plateau 위 — **묶여도 해(solution)가 안 바뀐다**.
3. **결정적 통제 c3 가 F1 을 죽인다.** 동일 mean-k 를 **고정 캡**으로 준 static arm(ATP 장 없음)이 실험 arm과 **구별 불가**(Δ = +0.004~+0.006, 전부 비유의). 즉 ATP 의 **동역학·피드백·organelle health·보존 스칼라장 전부가 downstream 에 0 을 기여**한다. 남는 건 "그 경제가 우연히 도달한 캡 숫자" 하나뿐이고, 그건 **캡의 효과이지 경제의 효과가 아니다**(= F6 소관).
4. 발산 원문의 사전 예측이 그대로 적중: *"solution 을 안 바꾸는 예산은 순수 오버헤드. F6 없는 F1 = bookkeeping."* (THEATER 랭킹 3위)

### ⚠️ Goodhart 함정 — ATP-throughput 은 verdict 에 못 쓴다
acc/ATP: EXP_tight **0.208** vs c2 **0.075** (2.8×). **이건 lift 가 아니다** — 분모(ATP 소비)를 줄이면 비율은 자동으로 오른다. 분자(acc)는 안 움직였다. 비율 지표를 성과로 파는 순간 그게 theater 의 정의다. 따라서 **verdict 지표 = held-out acc 의 Δ 뿐**.

---

## 6. p5 게이트 (p5_clean = TRUE · 전 arm 전 seed)

- **구조적 보증**: `k_t = clip(⌊·⌋, **1**, 8)` — floor 가 1 이라 **ATP 가 0 이 되어도 용량은 0 이 안 된다**. 예산 고갈이 강제하는 것은 **침묵이 아니라 용량 축소**. `if ATP < k: silence` 형태 코드 **부재**.
- **emit gate 는 ATP 를 인자·클로저·전역 어디로도 받지 않는다**: `emit_decide(logits, thr)` — 기질 표현에서 나온 tension(top1−top2 margin)만 읽음. thr 은 기준 기질(c1)에서 보정(ATP 무관).
- **구성적 위반 테스트**: ATP field 를 0 / 랜덤으로 대체한 문맥에서 emit 재계산 → 결정 해시 **byte-identical**(sha256 3종 일치, 8 arm × 5 seed 전부). + 소스(주석 제거) 내 `atp` 심볼 부재 검사 통과.
- **emit_rate 이동은 창발 경로**: EXP_tight 0.460 vs c1 0.500 (Δ=−0.040, sig). 이건 *열화된 기질이 낮은 tension(0.614 vs 0.639)을 내서* 생긴 결과이지 코딩된 억제가 아니다 — 합법 경로 `ATP → 용량 → 표현 → tension → emit` 그대로. 다만 **downstream reach 개선은 0** 이므로 verdict 를 바꾸지 못한다.

---

## 7. 반증조건 충족 여부 (카드 §3)

| 조건 | 결과 |
|---|---|
| PASS = binding **AND** 용량 조임 → downstream Δ > 두 control | ❌ binding(99.9%)은 됐으나 Δ vs c1/c2 = +0.003~+0.009, **전부 <1pp·비유의** |
| **FAIL = 어느 캡에서도 ΔEff≈0 ⇒ bookkeeping theater** | ✅ **충족** — tight/mid/loose 3 캡 전부 ΔEff≈0 |
| (추가) 경제 자체의 bite = Δ vs 동일-캡 static | ❌ +0.004~+0.006 비유의 — **경제는 캡 이상의 것을 0 만큼 한다** |

⇒ **🔴 THEATER 확정.** ATP 대사경제는 이 기질에서 **bookkeeping overhead**다.

---

## 8. 함의 (다음 패밀리로)

- **F1 단독은 죽었다.** 예산이 물려면 **캡이 아픈 영역**(여기선 k=1 근방, degeneracy 를 깨는 지점)에서 물어야 하고, 그러려면 **캡이 조합코드를 강제하는 코퍼스/task**가 필요하다 — 그게 **F6(호기성 혁명 = 결합 압력)**의 베팅이다. 본 결과는 F6 를 반증하지 **않는다**; 오히려 F6 없는 F1 이 왜 순수 오버헤드인지 실측으로 확정했다.
- **캡 축은 살아 있다**(VR: k=8→k=1 에서 12pp). 즉 **캡은 실재 레버**다. 죽은 것은 "ATP 라는 회계장부"다. F6 는 이 살아있는 캡 축을 조합요구 코퍼스와 교차시켜야 한다.
- **THEATER 랭킹 3위 예측 적중** — 발산의 위험 랭킹이 실측과 일치했다는 것 자체가 랭킹의 나머지(F7 1위·F9 2위)에 대한 사전확률을 높인다.
- **scope 한정**: toy MoE(303M 아님) · 합성 topic-조건부 task · DIRECTIONAL. 다만 결론이 "효과 없음"이므로 스케일업으로 뒤집힐 여지는 **F6 결합압력 조건이 붙을 때만** 열린다(F1 단독 재발사 = tune-to-green).
