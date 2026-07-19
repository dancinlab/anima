---
id: H_9803
title: BRANCH-LATENT FUTURE LANE — K개 disjoint 제안 latent 이 각기 다른 '관측된 미래 모드'를 설명하게 하여 ρ·fan(G6) 을 연다
tier: PROPOSED · 계기 IMPLEMENTED + TOY e2e 통과 (CPU 토이 · DIRECTIONAL 도 아님 — 아직 아무 verdict 없음)
frontier: g6-ideation-fan
lane: ideation-fan (branch-latent · NOT a sampling knob)
created: 2026-07-20
series: R-fan
related: "[[H_9720]] · [[H_9698]] · [[H_1603]] · G1_WALL_LEVER_IS_OBJECTIVE_NOT_READOUT"
wired: no (engine-native 계기만 착륙 · 303M 미발사)
---

# H_9803 — 분기-잠재(branch-latent) 미래 레인

## ⚠️ 이 카드의 상태 (정직 선언)

**이 세션은 계기(instrument)만 구현했다.** 원래 이 카드는 존재하지 않았고(작업 지시가 "먼저 읽어라"
한 파일이 레포에 없었다 — 최대 id 는 H_9799 였다), 그래서 사양은 지시문에서 받아 이 카드로 등록한다.
아래 수치는 **CPU 토이 e2e** 에서 나온 배관 검증 수치이며, **어떤 것도 verdict 가 아니다**.
303M/GPU 는 이 세션에서 한 번도 돌리지 않았다.

## 전제 (왜 또 하나의 G6 레인인가)

ρ·fan(G6) 의 다양성 시도는 전부 **하나의 next-byte 분포에 손잡이를 다는 계급**이었다 —
temperature · top-k · entropy 보너스 · cosine repulsion. 이 계급은 같은 분포를 넓힐 뿐,
**여러 개의 다른 미래를 표상하지 않는다**. 그리고 `G1_WALL_LEVER_IS_OBJECTIVE_NOT_READOUT` 이
말하듯 고정 파라미터로 선형붕괴하는 readout-side op 은 측정 전에 DOA 다.

## 주장 (한 줄 · 반증가능)

보존된 초기 tap(L3 · H_9720 tap-DEPTH)에서 뽑은 **K개 disjoint 제안 latent** 각각이
**동일 문맥의 서로 다른 실제 관측 후속(continuation)** 을 설명하도록 min-cost(Hungarian)
할당 + set-CE 로 학습되면, 분기 다양성은 sampling trick 이 아니라
**관측된 미래 모드에 접지(grounded)** 된다.

## 기전 (engine-native · `core/ifan.py` "IFAN" trailer)

```
z_k      = tanh( tap[fork] @ W_in[k] )          # K개 disjoint 블록 · 전 분기 동일 문맥 접지
g_k(t)   = tanh( h_t @ W_h ) ⊙ z_k              # ★ Hadamard — 분기 latent 가 진행 상태를 게이팅
logits_k = logits + λ · (g_k(t) @ W_out[k])     # additive perturbation
loss     = mean_k C[k][σ(k)],  σ = Hungarian(C),  C[k][m] = CE(관측후속 m | 분기 k)
```

**분기를 갈라놓는 항은 오직 할당(σ) 하나다.** repulsion 항 · entropy 보너스 · diversity
regulariser 는 `core/ifan.py` 어디에도 없다(grep 가능). K개 분기가 한 모드로 붕괴하면
주인 없는 관측 미래가 합에 그대로 남아 set-CE 가 **올라간다** — 그것이 접지의 전부다.

`z_k` 는 **문맥(fork 지점)에서만** 계산한다. 후속 내부 위치에서 다시 읽으면 분기가
"내가 어느 target 을 채점당하는지" 를 식별할 수 있고, 그러면 set-CE 는 모드-전념이 아니라
target-식별로 풀린다(= 다양성이 trick 으로 새는 경로).

## 새 플래그 (정확한 문법)

학습 (`anima-py train`):
```
--ideation-lane {off,branch-latent}      # 기본 off ⇒ byte-identical
--ideation-branches K                    # 기본 4
--ideation-objective set-ce              # Hungarian set-CE (유일 · repulsion 변종은 DISQUALIFIED)
--ideation-route {l3-disjoint,penult}    # l3-disjoint = detached L-tap · penult = tap-DEPTH 통제
--ideation-route-l L                     # 기본 3
--ideation-assign {hungarian,shuffle}    # shuffle = 학습측 NEGATIVE CONTROL
--ideation-corpus FILE                   # 빈줄-구분 문서: 0행=문맥, 1..M행=서로 다른 실제 후속
--ideation-rank r  --ideation-lam0 λ  --ideation-weight w  --ideation-docs N
```

평가 (`anima-py evaluate`):
```
--fan-branch {live,assignment-shuffle,off} [--branches K] [--gen N]
```
- `live` — 분기 k 가 자기 W_out[k] 로 읽힌다 (TREATMENT)
- `assignment-shuffle` — K·파라미터·λ 전부 동일, **분기↔readout 대응만** π 로 파괴 (KEY CONTROL)
- `off` — 분기 residual 을 **정확히 0** 으로 강제. `ifan_apply` 가 호출자의 배열을 그대로
  반환(복사도 산술도 없음) ⇒ base decode 와 **byte-identical** 이어야 한다

## 토이 e2e 실측 (CPU · 40 step · d=64 L=3 · 다중모드 합성 코퍼스 36 문서 × 3 미래)

학습 (exit 0):
```
ideation-fan: K=4 r=16 objective=set-ce route=l3-disjoint@L3 assign=hungarian · docs=36 (dropped 0 single-future blocks) ctx_len=24
step  1  CE=5.64850  {"ifan_set_ce": 5.7627, "ifan_mean_ce": 5.8094, "ifan_worst_ce": 6.0569, "ifan_n_distinct_tgt": 3.0}
step 40  CE=3.85947  {"ifan_set_ce": 3.5915, "ifan_mean_ce": 3.6992, "ifan_worst_ce": 3.9070, "ifan_n_distinct_tgt": 3.0}
IFAN trailer appended 86044 bytes (K=4 rank=16 route_L=3)
clm_decodable=True
```

`off` 패리티 (base = **IFAN trailer 바이트를 물리적으로 제거한** 별도 ckpt · 자기 자신과의
동어반복 비교가 아님):
```
[parity] stripped-base ckpt: 117982 bytes (IFAN trailer of 86044 bytes removed)
[parity] off-arm vs base decode: 6/6 frames BYTE-IDENTICAL (parity=1.000000 · need 1.000000)
[parity] ✅ PASS
```

할당 연산자 인증 (step 1 · 학습 전이라 순수 계기 검증):
- `assign=hungarian` : set_ce **5.7627 < mean_ce 5.8094** (평균보다 좋은 짝을 고른다)
- `assign=shuffle`   : set_ce **5.9018 > mean_ce 5.8094** (평균 이하를 고른다)
⟹ 최소비용 할당이 실제로 작동한다(방향 정확).

## ⛔ 토이가 보여주지 **못한** 것 (가장 중요한 정직 항목)

`--fan-branch live` 와 `assignment-shuffle` 이 **둘 다 mean_branch_distinct = 4.0000 (max=4)**
으로 포화했다 — 즉 **collapse-Δ = 0**. 40 step · d=64 토이에서는 분기가 사실상 무작위 방향이라
치환해도 아무것도 잃지 않는다. 그러므로:

> **"다양성이 관측 미래에 접지되었다"는 것은 현재 설계상의 주장이지, 측정된 사실이 아니다.**
> 토이 규모에서 이 레인은 sampling trick 과 **구별되지 않는다**(구별 실패가 아니라 검정력 부재).

판별은 오직 **실제 학습된 규모에서 live vs assignment-shuffle 의 collapse-Δ** 로만 이루어진다
(FORM tunable · BIND earned · p7). 단일 arm 수치는 verdict 가 아니다.

## 사전등록 PASS/KILL (303M · 미발사)

- **PASS**: `live` 의 mean_branch_distinct 가 `assignment-shuffle` 대비 유의하게 높고,
  `off` 패리티 = 1.000000 유지, 기저 CE 무회귀.
- **KILL**: live ≈ shuffle (Δ≈0) ⟹ 분기 identity 가 특정 미래 모드를 나르지 않는다 =
  이 레인도 sampling trick 계급 ⟹ 종결.
- **INVALID**: `off` 패리티 < 1.000000 (레인이 base 를 오염 ⟹ 모든 수치 무효).

## 미결(이 세션이 닫지 못한 것)

1. **303M/GPU 미발사** — 지시가 토이 CPU 로 제한. 따라서 DIRECTIONAL 조차 아님.
2. **live vs shuffle 검정력** — 토이에서 포화. 실제 판별은 미측정.
3. **ByteGPT 트윈 없음** — `--ideation-lane` 은 CLM 전용(early-tap 경로의 ByteGPT 대응 부재).
   `--arch bytegpt` 와 함께 주면 하드에러.
4. **CLMS fresh tap 과의 tap 슬롯 경쟁** — `_fwd_trunk` 는 tap 슬롯이 하나라, CLMS fresh 레인이
   다른 깊이로 이미 점유 중이면 IFAN 은 penult 로 폴백한다(조용한 깊이 혼합 대신 명시 폴백).
   두 레인 동시 사용 arm 은 미검증.
5. **다중모드 코퍼스 생성기 부재** — `--ideation-corpus` 포맷은 정의했으나 `anima-py corpus`
   에 대응 subcommand 를 아직 안 만들었다(토이는 손으로 만든 합성 파일).
