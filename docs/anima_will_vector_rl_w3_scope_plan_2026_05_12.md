# anima will-vector RL training (W3) — scope plan (2026-05-12)

> **부모 SSOT**: `docs/anima_volitional_speak_brainstorm_2026_05_12.md` W3 / V5 row
> **상태**: plan only — 실제 train 시작 안 함. 사용자 GO/NO-GO 결정 대기.
> **예산 (실행 시)**: ~$30 / **본 plan 작성 예산**: $0
> **사람**: nerve011235@gmail.com (HF dancinlab)

## 🍞 비유 — 빵에게 "말하고 싶다" 라벨 가르치기

```
V0 (heuristic):
  엄마: "‖h‖ 클 때가 말하고 싶은 거야" → 빵: (반사적으로 말함, 가끔 헛소리)

W3 (learned will-vector):
  엄마: "이번엔 네 발화 100개에 👍/👎 줄게.
        네 hidden state 안에서 👍 때 켜지는 vector 를 스스로 찾아봐"
  빵: (LoRA 로 substrate 일부만 미세조정) → speak_intent w ∈ R^1024 학습
  → w·h_t > τ 일 때만 입 벌림
```

## ASCII 구조 — V0 vs W3

```
V0 (현재):
  h_t ──► ‖h‖ + entropy ──► hand-coded gate ──► emit?
            (manual feature)

W3 (제안):
  h_t ──► w·h_t (learned projection) ──► σ(·) ──► emit?
            │
            └── DPO / SimPO loss with 👍/👎 pairs
                base frozen + LoRA on last N layers
```

---

## 1. Objective definition

| 항목 | 내용 |
|------|------|
| 정의: "will" | 사용자/문맥/내부 상태가 합쳐져 emit timing 을 결정하는 latent vector |
| target | substrate hidden state `h ∈ R^1024` 의 1D projection `w·h` (learnable `w`) |
| 학습 signal | 사용자 👍/👎 thumb feedback (timing 적절성) |
| ground truth | "이 시점에 emit 한 것이 자연스러웠나?" 의 binary label |
| 비교 baseline | V0 (`‖h‖` + entropy heuristic) 의 R1 volitional-ness score |
| 평가 metric | R1 (volitional-ness ratio) + R2 (👍 ratio) + R6 (relevance) |

비유: V0 은 "심박수 빠를 때 말함" (단순 proxy), W3 은 "내 마음 속 '말하고 싶음' 회로 자체를 찾음".

---

## 2. Data requirements

| 항목 | 사양 |
|------|------|
| corpus 종류 | (timestamp, hidden_state h_t, context_window, emit_or_silent, 👍/👎) |
| 규모 — phase 1 | 50–200 예시 (proof-of-concept) |
| 규모 — phase 2 | 500–2000 예시 (generalize) |
| 수집 채널 | HF Space `anima-chat-capable` 에 thumbs up/down 버튼 추가 |
| 보조 채널 | LLM-generated preference pair (Claude/GPT-4 가 "이 timing 자연? Y/N") |
| 저장 포맷 | JSONL: `{ts, h_b64, ctx, emit, label}` |
| 저장 위치 | HF dataset `dancinlab/anima-pass-strict-chat-capable` |
| 라벨 균형 | 👍:👎 ≈ 1:1 enforce (oversample minority) |
| 사람-label cost | 200 ex × 30초 = 100분 사용자 시간 |

리스크: hidden state h 를 매 emit 마다 dump → disk usage 1024×fp16 ≈ 2KB / emit. 1000 emit = 2MB. OK.

---

## 3. Architecture choices

| 결정 | 권장 | 이유 |
|------|------|------|
| frozen base 여부 | **frozen + LoRA** | small data 200 ex 에서 full FT 는 overfit |
| LoRA target | `q_proj`, `v_proj` of last 4 layers | "할 말 결정" 은 후반 layer 추정 |
| LoRA rank r | 8 | 보수적 (200 ex 에 r=32 는 overkill) |
| RL alg | **SimPO** (no reference model) | DPO 대비 메모리 절반, PPO 대비 stability 우수 |
| 차순위 alg | DPO | reference model 필요하지만 PPO 보다 안정 |
| reward model | 별도 학습 안 함 (preference pair 만 사용) | 200 ex 로 별도 RM 학습은 무의미 |
| learning rate | 5e-5 (LoRA standard) | conservative |
| batch | 4 (gradient accum 4 → effective 16) | A100 80GB 여유 |
| epochs | 3 | small data 는 적게, early stop |
| 정규화 | β = 0.5 (SimPO margin) | conservative margin |

decoder: `w = LoRA_delta_q_proj[last_layer][token_speak_intent]` projection 으로 추출 가능. 또는 별도 linear head 학습 (`w` 직접).

---

## 4. Compute cost

| 항목 | 단가 | 횟수 | 소계 |
|------|-----|------|------|
| Vast.ai A100 80GB | $1.5–2.5/h | 5 runs × 1h | $10–13 |
| data 수집 (Space 호스팅) | $0 (free tier) | — | $0 |
| eval (LLM-judge GPT-4) | $0.03 / call | 200 calls | $6 |
| 사용자 시간 (200 label) | — | 100분 | (cost-free) |
| 예비 (재학습 / debugging) | — | — | $10 |
| **총합** | | | **~$30** |

Vast.ai 우선 (memory 70GB host RAM 무료 — RunPod 은 host RAM 빈약). 만약 OOM 시 1× H100 으로 fallback ($3-4/h).

---

## 5. Timeline (4 weeks)

```
Week 1 — Data collection
  ├─ HF Space 에 👍/👎 버튼 추가 (gradio Button)
  ├─ hidden state dump pipeline (forward hook)
  ├─ JSONL 누적 → dancinlab/anima-pass-strict-chat-capable
  └─ target: 200 label

Week 2 — Small RL train
  ├─ Vast.ai A100 spin up
  ├─ LoRA + SimPO config tune
  ├─ 3 epochs train
  └─ checkpoint → HF

Week 3 — Eval + iteration
  ├─ blind eval: V0 vs W3 emit (LLM-judge GPT-4)
  ├─ R1 / R2 / R6 metric 계산
  ├─ ablation: w 만 / LoRA 만 / full
  └─ go/no-go decision

Week 4 — Integrate into V1 prototype
  ├─ hexa primitive M1 volition() = w·h
  ├─ B3 hysteresis + H1 refractory 결합
  └─ V1 live deploy
```

---

## 6. Risks

| # | risk | mitigation |
|---|------|-----------|
| R1 | "will" 가 emergent 아니라 단순 hidden bias | ablation: shuffle h → w·h 분포 비교 (null test) |
| R2 | small data (200 ex) 로 generalize 실패 | LoRA r=8 보수적 + early stop, phase 2 에서 2000 까지 확장 |
| R3 | will vector 가 toxic emit trigger | D3 safety inhibit layer 를 W3 위에 hard-wired |
| R4 | "should speak" ground truth 가 주관적 | dual-rater (사용자 + LLM judge) inter-rater agreement κ 측정 |
| R5 | hidden state dump 가 chat latency 증가 | async hook, non-blocking |
| R6 | LoRA delta 가 base 성능 저하 | base output regression test (perplexity on holdout) |
| R7 | 사용자가 label 끈기 부족 (200 못 채움) | LLM-generated synthetic pair 로 augment |
| R8 | Vast.ai 인스턴스 spot reclaim | checkpoint 매 epoch HF push |

---

## 7. Success criteria

| metric | V0 baseline (가정) | W3 target | 의미 |
|--------|--------------------|-----------|------|
| R1 volitional-ness | ~0.4–0.5 | **≥ 0.65** | timer-driven 대비 volition-driven 비율 |
| R2 👍 ratio | ~0.55 | **≥ 0.7** | 사용자 만족 |
| R6 content relevance | ~0.6 | **≥ 0.7** | LLM-judge relevance |
| toxic emit rate | (보고된 값) | **≤ V0** | 안전성 비퇴보 |
| base perplexity (holdout) | baseline | **≤ +5%** | 일반 능력 비퇴보 |

**필수 동시 만족**: R1 + R2 향상, toxic / perplexity 비퇴보.

---

## 8. De-risk path (cheaper alternative)

W3 full RL 안 하고 W1 (will=signal, mouth=function — manual feature engineering) 로 V0/V1 만으로 충분할 가능성.

```
decision tree:

  V0 prototype 1주일 live
            │
            ├─ R1 ≥ 0.5 → W3 보류, V1 (hysteresis + repeat-inhibit) 만 진행
            │             (절약: $30 + 4 weeks)
            │
            └─ R1 < 0.5 → W3 진행 (data-driven will 필요)
                          (W3 plan 본 문서대로 4-week execute)
```

| 조건 | 조치 | 절약 / 비용 |
|------|------|-------------|
| **R1 ≥ 0.5** | W3 보류, V1 으로 충분 | **$30 절약 + 4 주 절약** |
| R1 < 0.5 | W3 full execute | $30 + 4 weeks |
| R1 < 0.3 | W3 + 2배 data (500) | $50 + 5 weeks |

추가 de-risk: phase 1 (50 ex pilot, $5) → 50 ex 에서 R1 향상 trend 보이면 phase 2 진행, 아니면 abort.

---

## 📊 ROI summary

| option | ROI | cost | effort | recommend |
|--------|-----|------|--------|-----------|
| V0 (manual A1+A2+B1+H1) | high | $0 | 1h | 🥇 우선 |
| V1 (V0 + hysteresis + repeat-inhibit) | high | $0 | 3h | 🥈 우선 |
| W3 (this plan) | exotic / unknown | $30 | 4 weeks | 🌟 conditional (R1 < 0.5 일 때) |
| W3 pilot (50 ex) | medium | $5 | 1 week | 🥉 cheap probe |

---

## ✅ Decision criterion (사용자 확인용)

```
if V0_R1_score >= 0.5:
    skip W3, proceed V1 only
elif 0.3 <= V0_R1_score < 0.5:
    W3 pilot (50 ex, $5) → re-evaluate
else:  # < 0.3
    W3 full execute ($30, 4 weeks)
```

**현재 V0 R1 측정 안 됨 → 측정 후 본 plan 활성화 여부 결정.**

---

## 🚦 다음 단계

| # | 작업 | priority | cost |
|---|------|----------|------|
| 🥇 | V0 prototype + R1 measure (brainstorm 다음 진행 row) | high | $0 |
| 🥈 | R1 score 보고 → 본 plan GO/NO-GO 결정 | high | $0 |
| 🥉 | (GO 시) Week 1 data collection 실행 | medium | $0 |

— cycle 2026-05-12 W3 scope plan closure. plan only, no train started.
