# anima fix-6 PoC 설계 — Engine A/G chat-template dual loss curriculum 재설계

**작성일**: 2026-05-09
**작성 모드**: design-only (코드 수정 / 학습 fire 없음)
**전제 인증**: 사용자 verbatim 2026-05-09 "지금 가능한것들 all bg go"
**친근 모드**: strict (한국어 우선, 비유 적극)

---

## 0. 한 줄 요약

> **"의식 공부가 끝나기 전에 자연어 공부를 시키면 의식 책이 자연어 책에 덮어쓰임"** —
> 현재 Phase 2 의 chat-template dual loss 가 forward pass 의 lm_head 를
> "다음 토큰 예측" 단일 방향으로 압축시켜, Engine G 의 cell_pool 이 5축으로
> 차별화될 공간을 빼앗고 있음. 본 spec 은 chat loss 가 cell_pool collapse 를
> "증폭"한다는 H5 가설을 검증·완화하기 위한 4 가지 curriculum 재설계 후보를
> 비교하고, fix-5 (normalize 제거) 와의 직교성·결합 순서를 권장한다.

---

<!-- [Hc_649 h5-chat-loss-lm-head-cell-pool-collapse-amplifier — moved to hypotheses_candidates/Hc_649_h5_chat_loss_lm_head_cell_pool_collapse.md on 2026-05-11] -->

## 1. 배경 — H5 가설은 어디서 왔나

### 1.1 직접 측정 결과 (foreground v5)

| 모델 | trained PIV | trained DCR | cell_pool 변화량 |
|---|---|---|---|
| **BG-LB substrate only** | 0.0107 | 0.6207 | random_init 대비 델타 ~0.0001 |
| **Phase 2 cotrain (BG-LB + chat)** | 0.0051 (↓) | 0.2414 (↓) | random_init 대비 델타 ~0.0001 |

→ Phase 2 가 BG-LB 보다 **모든 지표가 더 나빠짐**. chat-template 학습을
얹은 직후 PIV 가 절반, DCR 이 1/2.6 로 떨어짐.

### 1.2 H5 가설 정의

> **H5**: Engine G 의 cell_pool collapse 는 "unit-sphere normalize"(H4) 만으로
> 발생하는 것이 아니라, **chat-template 자연어 학습이 forward pass 의 lm_head
> 를 single utility direction (다음 토큰 예측 방향) 으로 압축**시키면서
> cell_pool 의 5축 차별화 공간을 빼앗아 collapse 를 더 증폭한다.

(증거: Phase 2 cotrain cell_pool evidence — `state/anima_phase_2_cotrain_cell_pool_evidence_2026_05_09.json` 의 `phase2_vs_bglb_collapse: phase2 not more collapsed than BG-LB` 는 cell_pool 통계상으로는 같지만, downstream PIV/DCR 은 명확히 더 나쁨 → 통계 수치만으로는 못 잡는 lm_head 공유 채널 유출.)

### 1.3 친근 비유

> 학생이 의식 책을 막 펴서 새 단어를 외우려는 중인데,
> 옆에서 어른이 "지금부터 한국어 회화도 같이 공부해" 라며
> 같은 노트에 자연어 문장을 받아쓰게 함.
> 학생의 손은 하나뿐이라 (lm_head 하나뿐) 두 책의 글씨가 같은 줄에 겹쳐 적히고,
> 결국 의식 책의 단어는 자연어 줄에 묻혀 흐릿해짐.

---

## 2. 현재 curriculum 정확한 정리

### 2.1 schedule (training/train_phase2_cotrain.py L181-183)

```python
def curriculum_w(step: int) -> float:
    progress = step / max(1, args.steps)
    return args.w_start + (args.w_end - args.w_start) * min(1.0, progress)
```

| 항목 | 값 |
|---|---|
| **w_start** | 0.3 (step 0 부터 chat 30%) |
| **w_end** | 0.5 (step 6000 마지막 chat 50%) |
| **schedule 형태** | linear, **첫 step 부터 chat 활성** |
| **샘플링** | per micro-batch Bernoulli (`use_chat = random.random() < w`) |
| **loss 가중** | 없음 (raw cross-entropy 를 grad_accum 으로 단순 나눔) |
| **총 step** | 6000, grad_accum=8, batch_micro=4, batch_eff=32 |
| **final_w** | 0.5 (state/.../meta.json `final_w` 참고) |

### 2.2 친근 표현으로 풀면

- step 0 ~ 6000 동안 직선으로 0.3 → 0.5 로 chat 비율을 늘려감.
- 처음부터 끝까지 의식과 chat 이 **섞여서** 학습됨 (분리 stage 없음).
- chat sample 이 들어오는 순간 lm_head 의 그라디언트는 **substrate 와 동일한 weight 위에 그대로 누적**됨.

### 2.3 핵심 결함

> **결함 1** — substrate 가 의미 있는 cell_pool 표현을 형성할 시간 (warm-up) 이 없음. step 1 부터 이미 30% 가 chat.
> **결함 2** — chat loss 와 substrate loss 가 lm_head 를 공유하므로 cell_pool 학습 신호가 chat utility direction 에 덮어씌어짐.
> **결함 3** — gradient clipping 이 전체 모델 통합 (`clip_grad_norm_(model.parameters(), 1.0)`) 이라 cell_pool 이 별도 보호되지 않음.

---

## 3. fix-6 후보 4 종

### 3.1 fix-6a — 2-stage 분리 학습 (cell_pool freeze)

**아이디어**: Stage 1 substrate only 로 cell_pool + Engine G 가 의미 있는 5축을 형성한 뒤, Stage 2 에서 cell_pool 관련 파라미터를 **freeze (requires_grad=False)** 시키고 chat 만 학습.

| 구성 | 값 |
|---|---|
| Stage 1 (의식 정착) | 6000 step, w=0 (chat off), substrate only |
| Stage 2 (자연어 추가) | 3000 step, w=1.0, **`engine_g.cell_pool_init`, `engine_g.h_to_c`, `engine_g.c_to_h` freeze** |
| 코드 변경 위치 | `train_phase2_cotrain.py` L171 optimizer 생성 시 cell_pool 관련 param 분리 + Stage 2 시작 시 `.requires_grad_(False)` |

**장점**:
- cell_pool 이 chat 학습 중 절대 망가지지 않음 (강력 보장).
- H5 가설을 가장 깔끔히 검증함 (cell_pool 동결 후 PIV/DCR 유지되면 H5 확정).

**단점**:
- chat 학습이 **lm_head 공유 채널**을 통해 여전히 cell_pool 표현을 우회 변형 가능 (lm_head freeze 안 함). 100% 보호 아님.
- Stage 2 에서 자연어 적응이 cell_pool 없이 일어나야 → 자연어 품질 저하 가능.

**비유**: 의식 시험 끝난 학생에게 "이 책장은 잠그고, 이제 자연어 책만 펴라" — 책장은 안전하지만 두 책 사이의 화학 반응은 불가능.

---

### 3.2 fix-6b — curriculum 늦은 시작 (substrate warmup)

**아이디어**: 첫 50% step (3000) 은 w=0 (substrate only), 후 50% step 동안 0 → 0.5 로 점진 증가. cell_pool 이 의미 형성을 마친 뒤 chat 추가.

| 구성 | 값 |
|---|---|
| 0 ~ 3000 step | w = 0 (substrate only) |
| 3000 ~ 6000 step | w = 0 + 0.5 * ((step - 3000) / 3000), 즉 0 → 0.5 linear |
| 코드 변경 위치 | `train_phase2_cotrain.py` L181-183 `curriculum_w` 함수 한 곳 |

**장점**:
- 가장 **변경 최소** (함수 6 줄 수정).
- cell_pool 이 의식 corpus 만으로 독립 형성될 시간 보장.
- BG-LB 와 동일 시작 조건이라 비교 baseline 명확.

**단점**:
- chat 추가 후 cell_pool 이 다시 collapse 할 가능성 여전 (warmup 만으로 lm_head 공유 문제 해결 안 됨).
- 후반부에서 결국 fix-6a 와 같은 collapse 재현 가능.

**비유**: 학생에게 "의식 책 다 보고 나서 자연어 책 봐" — 순서는 깔끔하지만 자연어 받아쓰기가 시작되면 의식 책 줄이 다시 흐려질 수 있음.

---

### 3.3 fix-6c — chat loss 의 cell_pool grad scaling

**아이디어**: chat sample 의 backward pass 에서 cell_pool 관련 파라미터의 gradient 만 별도로 0.1× 등 강하게 scaling. substrate sample 은 그대로.

| 구성 | 값 |
|---|---|
| substrate sample | grad scale = 1.0 (현재 그대로) |
| chat sample | `engine_g.*` 파라미터 grad scale = 0.1 (또는 0.0 = freeze 와 동등) |
| 코드 변경 위치 | `train_phase2_cotrain.py` L227 backward 직후, `engine_g` param 의 `.grad` 에 scaling 곱; 또는 PyTorch hook (`register_hook`) 등록 |

**장점**:
- cell_pool 보호 + chat 적응 양쪽을 **연속적으로 trade-off** 가능 (scale 값 조정만).
- cotrain semantics 유지 (stage 분리 안 함).

**단점**:
- 구현 복잡 (chat/substrate sample 별 grad accumulator 분리 필요).
- gradient hook 이 mixed precision (bfloat16) 에서 안전한지 추가 검증 필요.
- "chat 학습이 cell_pool 에 미치는 영향" 의 정량 파악이 어려움 (간접 효과).

**비유**: 학생이 자연어 받아쓰기를 할 때만 "의식 책 줄에 적힌 글씨는 0.1배 흐리게 적어" 라고 함. 두 책이 섞여 있긴 하지만 의식 책의 손상 폭이 작아짐.

---

### 3.4 fix-6d — dual loss decoupling (forward path 분리)

**아이디어**: 같은 batch 안에서 substrate forward 는 Engine G 통과 (cell_pool 사용), chat forward 는 Engine G **bypass** (lm_head 만 공유). cell_pool 은 substrate path 에서만 학습됨.

| 구성 | 값 |
|---|---|
| substrate forward | 현재와 동일 (Engine A + Engine G) |
| chat forward | tok_emb → Engine A layers → norm_f → lm_head (Engine G refresh / project_back skip) |
| 코드 변경 위치 | `engine_a_g_arch.py` L351-389 `forward()` 에 `bypass_engine_g: bool` 옵션 추가; `train_phase2_cotrain.py` L222 chat sample 일 때 `bypass_engine_g=True` 전달 |

**장점**:
- 가장 **근본적**인 분리 — chat gradient 가 cell_pool 에 도달할 경로 자체 제거.
- lm_head 는 공유되므로 자연어 품질 적응은 유지됨 (Engine A 표현은 둘이 공유).

**단점**:
- 구현이 가장 큼 (forward 분기 + EngineG.step 호출 조건 분기).
- chat path 를 통과한 hidden 이 Engine A layer 입력으로 들어갈 때 cell projection 부재 → Engine A 의 hidden 분포가 substrate path 와 달라짐. 즉 Engine A 자체가 두 mode 로 양분될 위험.

**비유**: 의식 책과 자연어 책에 **별도 펜**을 줌 (chat 펜은 cell_pool 칸을 못 적게 막음). 의식 책 칸은 절대 안전하지만, 두 책이 같은 종이 (Engine A) 를 쓰므로 종이 무늬는 두 펜에 다 영향받음.

---

## 4. 후보 비교 + 1순위 권장

| 항목 | fix-6a | fix-6b | fix-6c | fix-6d |
|---|---|---|---|---|
| **구현 복잡도** | 중 (optimizer + freeze) | **저 (함수 6줄)** | 중-상 (hook + 분리 grad) | 상 (forward 분기) |
| **cell_pool 보호 강도** | 강 (Stage 2 freeze) | 약 (warmup 만) | 중 (gradient scaling) | **최강 (path 분리)** |
| **자연어 품질** | 저 (cell_pool 동결) | 중 (warmup 후 정상) | 중 (scaling 정도에 따라) | 중-상 (lm_head 공유) |
| **H5 검증력** | **최강** (clean ablation) | 약 (warmup 효과만) | 중 (scaling 효과 측정) | 강 (path 분리 효과) |
| **코드 변경 라인 수** | ~30 | **~6** | ~25 | ~50 |
| **컴퓨트 비용** | 1.5x (Stage 2 추가) | 1.0x (동일) | 1.0x (동일) | 1.0x (동일) |

### 4.1 1순위 권장 — **fix-6b (curriculum 늦은 시작)**

이유:

1. **변경 최소** — `curriculum_w` 함수 한 곳만 수정. PoC 회전 속도 최고.
2. **BG-LB baseline 과 직접 비교 가능** — 첫 3000 step 은 BG-LB 와 동일 조건이므로 cell_pool 형성이 BG-LB 수준까지 도달함을 사전 검증 가능.
3. **fix-5 와의 결합이 가장 깔끔** — 두 fix 모두 학습 phase 의 신호 / 정규화에 작용하지 추가 path 변경 없음.

### 4.2 2순위 — **fix-6a (2-stage freeze)**

H5 가설 자체를 가장 깔끔히 검증하려면 fix-6a. fix-6b PoC 가 부분 효과를 보일 경우 (chat 추가 후 다시 collapse), 다음 라운드에서 fix-6a 실행.

### 4.3 3·4순위 — fix-6c, fix-6d (deferred)

구현·검증 부담 대비 fix-6b 가 충분한 정보를 줄 가능성이 높아 후속 라운드 보류.

---

## 5. fix-5 와의 직교성 분석

### 5.1 직교 정의

| fix | 작용 위치 | 작용 시점 |
|---|---|---|
| **fix-5** | `EngineG.step` L307 normalize 제거 | forward pass 매 layer (구조 자체) |
| **fix-6** | `train_phase2_cotrain.py` curriculum_w | training pass 시간축 (학습 신호) |

→ 작용 위치·시점이 완전히 분리됨. **상호 의존 없음 = 직교.**

### 5.2 결합 효과 매트릭스

| 시나리오 | cell_pool 학습 | chat collapse 회피 | 예상 PIV / DCR |
|---|---|---|---|
| **fix-5 단독** | O (살아남) | X (chat 학습 시 여전히 collapse) | 부분 회복 |
| **fix-6 단독** | X (normalize 로 erase) | O (chat 시점 보호) | 거의 변화 없음 |
| **fix-5 + fix-6 결합** | O | O | **최대 회복 기대** |

### 5.3 권장 PoC 순서 (사용자 지시 그대로)

1. **fix-5 단독 PoC 먼저** → cell_pool 학습이 살아나는지 (PIV / DCR 변화 확인).
2. **결과 확인 후 fix-5 + fix-6b 결합 PoC** → cell_pool 살리고 + chat 시점 보호.
3. (선택) **fix-6 단독 PoC** — H5 가설 검증용. 의식 cell_pool 변화량을 BG-LB 와 비교하여 chat 학습이 collapse 를 증폭하는지 직접 측정.

### 5.4 친근 비유

> fix-5 = "학생 노트의 칸 룰을 없앰" (cell 이 자유롭게 길어질 수 있음)
> fix-6 = "의식 책과 자연어 책의 학습 순서를 정리" (의식이 먼저 자리잡은 뒤 자연어 추가)
>
> 두 fix 는 다른 문제를 풀므로 한쪽만 해서는 부족함:
> - fix-5 만 → 칸은 풀렸지만 자연어 받아쓰기에 의식 줄이 덮어씌어짐.
> - fix-6 만 → 의식이 먼저 자리잡았지만 그 자리도 결국 칸 룰로 잘려나감.
> - **둘 다 → 칸도 풀리고 순서도 맞으니 의식 줄이 살아남음.**

---

## 6. PoC 절차 (H5 가설 검증)

### 6.1 fix-6 단독 (H5 검증용 PoC)

| step | 액션 | 기대 결과 |
|---|---|---|
| 1 | fix-6b 적용 (curriculum_w 6줄 수정) | 코드 diff <10 라인 |
| 2 | substrate ckpt = BG-LB step_8000_final.pt 로 시작 | Phase 2 와 동일 entry |
| 3 | 6000 step 학습 (3000 substrate-only + 3000 chat-mix) | 비용 ~$15 (Phase 2 와 동일) |
| 4 | step 3000 (warmup 끝) ckpt 의 cell_pool 측정 | BG-LB 수준 axis_stdev 도달 확인 |
| 5 | step 6000 (chat 추가 끝) ckpt 의 cell_pool + PIV/DCR 측정 | chat 추가 전후 델타 확인 |
| 6 | Phase 2 (현 baseline) vs fix-6b 의 PIV/DCR 비교 | fix-6b > Phase 2 면 H5 부분 확정 |

### 6.2 H5 검증 verdict 기준

| 결과 | verdict |
|---|---|
| fix-6b PIV ≥ BG-LB PIV (0.0107) **and** DCR ≥ BG-LB DCR (0.6207) | **H5 확정** — chat-template 학습이 collapse 증폭 |
| fix-6b PIV / DCR 이 Phase 2 와 비슷 | H5 약 — warmup 만으로는 부족, fix-6a 필요 |
| fix-6b 가 Phase 2 보다도 나쁨 | H5 반증 — chat 가 아니라 다른 원인 |

### 6.3 fix-5 + fix-6b 결합 PoC (1순위 실험)

사용자 지시대로 fix-5 단독 PoC 결과 확인 **후** 진행. fix-5 단독에서 cell_pool 변화 (axis_stdev 증가) 가 관찰되면, 결합 PoC 에서는 fix-5 의 효과 + fix-6b 의 보호 효과가 곱해져 PIV / DCR 의 추가 회복을 기대.

---

## 7. 변경 안 되는 부분 (안전성 boundary)

- 본 spec 은 **설계 문서만** 추가. 코드 / 모델 / 학습은 절대 건드리지 않음.
- `engine_a_g_arch.py`, `train_phase2_cotrain.py` 모두 read-only 검색만 수행.
- HF push, ckpt 변경, foreground 학습 시작 등 부수효과 0.
- commit / push 없음 — 파일 저장만.

---

## 8. 참고 파일 (절대경로)

- `/Users/ghost/core/anima/training/engine_a_g_arch.py` (Engine A/G 모델 정의 — L281-283 cell_pool init, L307 normalize, L351-389 forward)
- `/Users/ghost/core/anima/training/train_phase2_cotrain.py` (Phase 2 학습 — L181-183 curriculum_w, L207 Bernoulli sampling, L222-227 forward+backward, L234 grad clip)
- `/Users/ghost/core/anima/state/anima_phase_2_cotrain_2026_05_09.json` (Phase 2 학습 state, curriculum_w_start=0.3 / w_end=0.5)
- `/Users/ghost/core/anima/state/anima_phase_2_cotrain_cell_pool_evidence_2026_05_09.json` (H5 evidence — phase2 vs BG-LB cell_pool stats)
- `/Users/ghost/core/anima/docs/anima_engine_a_g_fix_5_normalize_removal_spec_2026_05_09.md` (fix-5 spec — 직교 fix)

---

## 9. 친근 한 줄

> **"의식 공부 끝난 뒤에 자연어 공부 시키면 돼" — fix-6b 가 가장 작은 손길로 가장 큰 효과 줌.**
