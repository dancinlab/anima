# H_9939 · Mistral organ 에서 GRAFT 목적함수는 **게이트를 끄는 것이 최적** — 붕괴가 아니라 올바른 최적화

**한 줄:** Mistral-7B(4bit·얼림)를 organ 으로 우리 프레임에서 GRAFT 를 학습하니 step 50 에서 MI=0.1396 을
벌었다가 **급락해 gate 가 꺼진 상태로 안착**했다. 산수로 확인하면 이는 붕괴가 아니라 최적화가 옳게 작동한
것이다 — `L=(logN−MI)+λ·L_common` 에서 그 지점의 손실 **2.1450 > gate-off 2.0794** 라 켜는 게 손해다.

- 계기: `anima-py graft fit --hf-model mistralai/Mistral-7B-Instruct-v0.2 --carrier-corpus en_general.txt`
  (고정 held-out carrier · Mistral tokenizer · K=4 windows · ctx 128 · T 64 · N=8 · gs 0.1 · λ=1.0 · 200 step ·
  seed 1 · summer RTX 5070 4bit). wiring smoke ALL PASS 선행(주입점 파리티 max|Δ|=0.000e+00 · 잔차 grad
  nonzero · base param grad 0). regime `no-corpus` · DIRECTIONAL.

## 손실 궤적 — 왜 꺼졌나 (판정은 산수로 난다)
| step | MI | L_common | loss=(logN−MI)+λ·L_common | gate-ON 이 이득? |
|---|---|---|---|---|
| 25 | 0.0035 | 0.0008 | 2.0767 | 예(간신히) |
| **50** | **0.1396** | **0.2052** | **2.1450** | ❌ **아니오 — off(2.0794)보다 나쁨** |
| 75 | 0.0083 | 0.0033 | 2.0744 | 예 |
| 200 | 0.0039 | 0.0011 | 2.0766 | 예 |

최종 val MI=0.0056 · 받침대 0.0008 · lift **+0.0048 nats**(토이 +0.21 대비 무의미). 즉 optimizer 는
"정보를 벌 수 있는 지점"을 한 번 찾았지만 **그 지점이 손실상 불리해서 되돌아갔고**, gate 가 거의 꺼진 채
off 보다 아주 약간만 유리한 자리에 머물렀다.

## 기전 — 구조 bound 는 입력에서 평균을 빼지만, 7B 의 비선형이 출력에서 공통이동을 되살린다
| organ | 최고 MI | 그때 L_common | MI/L_common |
|---|---|---|---|
| 토이 `.clm`(d=64·L=2 conv) | 0.2412 | 0.0831 | **2.90** (켜는 게 이득) |
| **Mistral-7B**(d=4096·32층) | 0.1396 | 0.2052 | **0.68** (켜는 게 손해) |

codes 는 N 상태에 걸쳐 **입력 임베딩 공간에서** 평균이 0 이 되도록 강제된다(구조 bound 1a). 그러나 organ 이
비선형이라 평균-0 인 입력 섭동들이 **출력 분포에서는 공통 이동으로 되살아난다**. 층이 깊고 민감할수록 그
되살아남이 커진다 — 토이(2층 conv)는 약하고 Mistral(32층)은 상태-구분보다 1.5배 크다.

## 판정
🔴 **Mistral organ + 현 목적함수(λ=1.0·gs=0.1) = gate-off 가 최적** · DIRECTIONAL(1 seed·200 step)
- 이것은 v2b 의 GRAFT-flatline(clamp 로 Jacobian 이 죽음)과 **다른 실패**다: 여기선 gate 가 살아 있고
  gradient 도 흐르며(wiring smoke 통과), 단지 **목적함수가 켜는 것을 벌하기 때문에** 꺼진다.
- 정직 경계: 이 판정은 `(λ=1.0, gs=0.1)` **한 점**에 대한 것이다. "Mistral 에서 GRAFT 가 불가능하다"가
  아니라 "이 설정에서는 gate-ON 이 손실상 불리하다"까지만 말한다. 이득 영역의 존재 여부는 미측정.
- 계기는 건강하다 — wiring smoke 3종 통과, 고정 carrier(Mistral tokenizer) 391,058 train/64 val windows,
  gradient checkpointing 으로 12GB 카드서 8×4 시퀀스 backward 가능(11.38→7.27GiB 실측).


## ⚠️ 양자화 경계 — 이 판은 4bit 에서 측정됐다 (오너: 양자화 없이 진행 · #4523)
이 실행의 organ 은 **nf4 4bit** 다. 오너 지시로 `--no-4bit`(bf16 + CPU offload)가 착륙했고(#4523),
**bf16 재측정이 필요하다** — 이 카드의 결론이 기대는 축이 하필 양자화에 민감할 수 있기 때문이다:
결론은 `MI/L_common` **비율**(0.68)이고, 그 비율은 organ 의 비선형 응답이 결정한다. nf4 반올림이 그
응답을 바꾸면 공통이동 비율도 함께 움직인다. 따라서 "Mistral 에서 gate-off 가 최적"은 **4bit organ 에
대한 판정**이며, bf16 에서 재현되기 전까지 organ 일반의 성질로 읽지 않는다.
(병렬 세션과 같은 작업을 동시에 진행했다 — #4523 이 언급한 "16:14 시작 4bit Mistral GRAFT"가 이 실행이다.)

## 다음
① **(λ, gate_strength) 격자에서 `gate-ON 이득 영역`이 존재하는가**를 짧은 학습(50 step)으로 측정 —
   판정식은 사전 정의돼 있다(`(logN−MI)+λ·L_common < logN`). 존재하면 거기서 본학습, 없으면
   "이 목적함수는 7B organ 에서 구조적으로 gate 를 끈다"가 결론.
② 출력측 공통이동을 구조로 막는 설계(입력 mean-center 만으로는 비선형을 못 이김) — ①이 음성일 때만.
산출물 `~/.fire-recover/graft_mistral/{fit_s1.log, graft_mistral_s1.pt, *.step0.pt, *.graft.json}`.
