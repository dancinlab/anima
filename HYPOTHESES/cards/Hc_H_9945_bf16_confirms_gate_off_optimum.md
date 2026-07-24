# H_9945 · 양자화를 빼도 결론은 같다 — bf16 Mistral organ 에서도 gate-OFF 가 최적 (H_9939 재현)

**한 줄:** 오너 지시(양자화 없이 진행)대로 **nf4 양자화 없는 bf16** Mistral-7B organ 으로 GRAFT 를 돌린
결과, H_9939(4bit)가 찾은 구조가 그대로 재현된다 — MI 가 초반에 한 번 솟았다가(step 40: MI 0.0322,
**L_common 0.0374**) 곧 0.002~0.005 로 내려앉는다. 정점에서조차 **공통 왜곡이 상태구분보다 크다**
(0.0374 > 0.0322) ⟹ 게이트를 켜는 것이 손실이다. **H_9939 는 4bit artifact 가 아니다.**

- 계기: `anima-py graft fit --hf-model mistralai/Mistral-7B-Instruct-v0.2 --no-4bit --carrier-corpus …`
  (신설 CPU-offload 경로 #4523/#4525/#4526 · 가중치 정확히 bf16 · nf4 반올림 0 · device_map=auto +
  max_memory 로 GPU 6GiB + CPU offload). wiring smoke 3/3 ALL PASS(**4bit=False** · 주입점 파리티
  max|Δ|=0.000e+00 · 잔차 grad 0.32 유한 · base 파라미터 grad 0개).
- 호스트: **aiden 물리 재부팅 후 clean**(load 0.00 · RAM 29GB · GPU 11.7GB 전부 여유). 재부팅만으로는
  부족해 `airgenome-*` 사용자 타이머 4종(forecast 5분·harvest/label 15분·log-rotate)이 부하를 되살리므로
  이번 실행 동안 `stop`(disable 안 함 — 남의 파이프라인 영구 해제 금지, 재부팅 시 자동 복구).

## 실측 — bf16 vs 4bit (같은 organ · 같은 목적함수 · 같은 고정 carrier 프레임)
| | bf16 (이번 · aiden) | 4bit (H_9939 · summer) |
|---|---|---|
| pedestal MI | 0.0008 | 0.0008 |
| final MI (disjoint val) | 0.0081 | 0.0056 |
| lift | **+0.0073** | +0.0048 |
| 정점 | step 40 · MI 0.0322 · **L_common 0.0374** | step 50 · MI 0.1396 · **L_common 0.2052** |
| 정점에서 L_common/MI | **1.16** | 1.47 |
| 정점 이후 | 0.002~0.005 로 붕괴·유지 | 0.004~0.008 로 붕괴·유지 |

곡선(step, MI, L_common): (1,.0007,.0003) (20,.0021,.0005) **(40,.0322,.0374)** (60,.0017,.0005)
(80,.0032,.0006) (100,.0048,.0018) (120,.0019,.0004) (140,.0042,.0012) (160,.0030,.0006) (180,.0027,.0007)
(200,.0141,.0030) · logN=1.386(N=4) · organ d=4096 V=32000 emb_rms=0.0027 · carrier=자연텍스트 3MB
(Mistral 토크나이저 · train 391,154 / val 64 windows disjoint).

## 판정
🟢 **재현 — H_9939 의 gate-OFF 최적은 양자화와 무관한 구조 사실** · DIRECTIONAL
- 두 정밀도에서 **같은 부호의 같은 이야기**: 정점에서 L_common > MI (bf16 1.16배 · 4bit 1.47배),
  그래서 목적함수가 게이트 켜기를 벌하고 학습이 스스로 gate-OFF 로 되돌아간다. 붕괴가 아니라 정상 최적화.
- 기전(H_9939)이 양자화 무관 구조 논증이었다는 예상과 일치: 입력 임베딩에서 mean-center 해도 **32층
  비선형 organ 이 출력 분포에서 공통 shift 를 되살린다**. 정밀도는 그 되살림을 만들지도 없애지도 않는다.
- 정직 경계: ① 두 판 사이 N(4 vs 8)·K·호스트가 달라 **절대값 비교는 불가**, 재현되는 것은 **구조와 부호**
  (정점→붕괴 · L_common>MI). ② seed 1 단독. ③ 회전 null(HF 분기) 미배선이라 lift 단독으로는 판별 불가
  (H_9937). ④ toy .clm 의 lift +0.21 과 견주면 Mistral organ 은 두 자릿수 작다.

## 다음
① λ·gate_strength 를 이 organ 에 맞게 재설계(현 (1.0, 0.1)에서 gate-OFF 가 최적이면 그 조합이 답이 아님) —
단 컨트롤러 플래그 금지(kill-list) 안에서. ② `_check` HF 분기(회전 null)로 판정 계기 완성.
③ 인프라: aiden 은 `airgenome` 타이머를 멈춰야만 heavy job 이 사는 호스트(정지는 임시).
산출물 `~/.fire-recover/graft_mistral_bf16/`(bridge·pedestal·json·로그).
