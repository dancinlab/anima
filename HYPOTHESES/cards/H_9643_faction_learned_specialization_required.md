---
id: H_9643
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_learned_specialization_required
title: faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다
status: 🟢 계기 v2 SOUND 4다리 전부 닫힘 (perm=200 실측) — ①within-arm 전 학습 ckpt S>null95 p=.005 ②random-init 경계 p=.0448(grouped-conv 블록 confound) ③fit-matched K=1 음성(--faction-split 4) S 0.406≤null95 1.221 p=.86 결정적 clean(낮은-CE 분모서 log-ratio 무결) ④ORACLE π 회수: 코사인 A 가 λ=0 no(0.37<0.57)→λ⅓/⅔/1 yes(0.90-0.98) 단조. lam0 자유학습 within-arm PASS=파벌은 분리가능 데이터서 학습되는 레버(toy·서로소 알파벳 = token routing 착각 위험 · 실물 303M 은 공유구조라 천장 낮음 · a_toy_scale_recheck). 계기 TERMINAL 인증 완료 · 실물 arm 은 303M(위험 8개)
tier: 🟡 학습 vs 사후분할(GPU) · Sol F12
cost: GPU
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_1302, H_1462, H_9639
---

# H_9643 — faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다

## 주장 (반증가능)

사후(post-hoc) 파벌 배정은 임의 라벨이다. 파벌이 실재하려면 **학습이 그 분할을 만들어야** 한다.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py train --n-factions K --faction-specialize learned,posthoc,random`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

specialization index + held-out G1 D-acc. bar = learned 가 posthoc/random 대비 Δ≥0.10.


## 🔀 레버 설계 (2026-07-17 · Fable 위임 · fable-mode HARD PROBLEM · 코드 접지 완료)

선결조건 4/4 통과(H_9674 #3904) 후 이 카드가 파벌축의 **마지막 살아있는 가설**이 됐다. 발사에 필요한
파벌 **학습** 레버가 `core/` 에 없어(기존 계기는 전부 READ 전용) 설계를 Fable 에 위임했다.

### Q1 — 레버: `--n-factions K`(구조 분할) + `--faction-bridge-lam0`(게이트 다리) · **loss = CE 뿐**

| 후보 | 판정 |
|---|---|
| (a) 구조 분할 (CE 만) | ✅ 채택 |
| (b) 파벌간 직교화 aux | ⛔ **기각 — H_9673 과 같은 실패계급**: DV 가 penultimate 상관 모듈러리티 Q 인데 decorrelation loss 는 **그 측정 통계량을 매 스텝 직접 쓴다** = 순환 재발 |
| (c) 다리 단독 | ⛔ 단독 기각 — 분할 없이는 "파벌간"이 아니라 그냥 추가 용량 |
| (d) MoE expert 축 재활용 | ⛔ 기각 — expert 는 T-위치별 top-k 혼합, d 유닛축을 분할 안 함. 계기가 잰 블록은 **d 축** |

- `--n-factions K` (default 0=OFF · OFF 시 byte-identical): 전 TrunkLayer conv → `groups=K` ·
  embed_conv 도 groups=K · **GN(1,d) → GN(K,d)** (G=1 전역 정규화는 mean/var 통한 **파벌간 숨은 누설채널**) ·
  MoE+readout 은 full mixing 유지 = **합의 스테이지**(파벌=trunk · 토론=bridge · 합의=MoE/readout).
- `--faction-bridge-lam0` (default 0.1 · K>0 시만): trunk 말단·MoE 앞 1 모듈로 파벌내 항을 0-마스크한
  1x1 conv + 채널 게이트 + trailer 스칼라 lambda (eval 서 오버라이드 = debate ON/OFF ablation 성립).
- **학습 신호 = CE 역전파 뿐** — 다리가 유용하면 CE 가 게이트를 키운다 = **earned, not tuned**.
- 순환 회피: loss 어디에도 파벌 통계량(sync·상관·Q·직교성)이 **0 개**.

### Q2 — ⚠️ **Q 로는 learned vs post-hoc 가 안 갈린다** (내 예상을 고침)

`groups=K` 구조에선 **random-init 도 아키텍처적으로 블록을 가진다**(계기의 `--arm-random-init` 이 정확히
이를 잡는다). ⟹ Q 는 **조작확인(manipulation check)으로 강등**하고 판정은 **기능 lesion 해리**로 간다.

신규 계기: `anima-py evaluate <clm> --faction-lesion <domains.json>` — forward 중 파벌 f 채널 0-마스크 →
도메인 c 별 ΔCE 행렬. **DV = 선택성 지수 S**(파벌마다 "자기 도메인"이 있으면 S 상승).

| arm | 역할 |
|---|---|
| real (K=8 학습 · trailer 배정) | 실험군 |
| **post-hoc (같은 ckpt · 채널 랜덤 재배정 200회)** | **우연 = 이 null 의 95분위** ← H_9643 의 핵심 대조 |
| random-init (같은 groups=K · 미학습) | 구조 vs 학습 분리 |
| K=1 trained (동일예산) | 파벌 자체의 기여 |
| 양성통제 (도메인별 강제학습 toy) | 검정력 게이트 · 심은 specialization 회수 못하면 판독 자격 없음 |

bar: `S_real > post-hoc null95` **AND** `S_real / S_random-init >= 2.0` · 3 seed 중 >=2.
우연은 post-hoc 순열 null 에서 **실측 유도**([[chance-level-must-be-derived-per-metric]]).

### Q3 — ⚠️ **H_9267 XBIND 는 천장이다** (K=1 도 D-acc 1.000)

G1 벽은 DATA 벽(H_9304)이므로 **coverage-기아 XBIND**(held-out 쌍 완전 배제·비가법 조합만)를 쓰고,
**pre-gate: K=1 기저가 D-acc <=0.6 인 coverage 수준을 먼저 실측 확정**한 뒤에만 파벌 arm 발사.

| arm | debate lambda | 배정 | 예측(H_9643 참) |
|---|---|---|---|
| K=8 learned | trained (ON) | trailer | **>=0.9** |
| K=8 learned | 0 (OFF) | trailer | 기저로 붕괴 |
| K=8 learned | ON + **채널순열 배정** | permuted | 차이 소실 — "다리=범용용량" 반증 arm |
| K=1 trained | — | — | <=0.6 (floor) |

**인과 사슬 3개가 다 서야** 성립: specialization(Q2 PASS) AND Delta(ON-OFF) > Delta(permuted) AND ON >=0.9.
다리 위치는 사전등록 고정 — **층별 sweep 은 tune-to-green 이므로 금지**.

### Q4 — fire: toy 우선 · 전부 자가 pool ($0 현금)

- toy d768 scratch(이번 세션 경로 검증됨) · **재학습 필수**(레버가 학습 개입 ⟹ 기존 ckpt 재사용 불가 ·
  기존 d768 은 K=1 기저 arm 으로만 재활용).
- {K=8, K=1} x 3 seed(7·11·23) = 6 train · K=8 **하나만 사전등록**(K-sweep 후 최적 보고 = tune-to-green).
- summer + aiden 트랙당 전용 1 호스트(`a_wall_first`) ⟹ wall = max(런 1개) · 1–2일 · **$0**.
- 순서: ① K=1 floor pre-gate → ② 6 train → ③ Q2 lesion + Q 조작확인 → ④ Q3 debate ablation.
- **303M 은 toy GREEN 일 때만**(`a_toy_scale_recheck`) · scratch 재학습 = rent-fleet = **오너 go**.
  base ckpt 에 cross-block CPT 는 [[cpt-destroys-what-corpus-omits]] 위험 커서 비권장.

### Q5 — 사망조건 (사전등록 · 검정력 게이트·양성통제 통과 전제)

- **D1 specialization 불발**: 3 seed 중 >=2 서 `S_real <= post-hoc null95` = 임의 사후분할과 같다.
- **D2 G1 무효**: 특화는 생겼는데 >=2 seed 서 `D-acc(ON) < 0.9` **AND** `Delta(ON-OFF) <= Delta(permuted)`
  (TOST 등가 · [[negative-claims-need-tost-not-ns]]).
- **D3 파벌 무기여**: `D-acc(K=8,ON)` 이 `D-acc(K=1)` 과 TOST 등가.
- **파벌축 전체 DIRECTIONAL-유물 종결**: D1 or D2 or D3 AND H_9674 블록 여전히 실재 ⟹ "블록은 상관
  텍스처로 존재하나 파벌로 학습·사용 불가" 가 **2 렌즈(구조 Q + 기능 lesion)에서 일치** ⟹ H_9674 블록을
  창발 파벌이 아니라 **학습의 부산물**로 재분류하고 축을 닫는다.

### 구현 순서 (Fable 제안 · 내가 실행)

① `core/model.py` groups=K + GN(K) + bridge(OFF 시 byte-identical 확인) ② serialize trailer + VERSION(G5)
③ evaluate `--faction-lesion` + lambda 오버라이드 ④ K=1 floor pre-gate 발사

> 이 카드 본문이 설계 SSOT (`a_no_scatter_hypotheses_first` — scratch 파일은 휘발).


## 🔨 구현 ① 완료 — `core/model.py` 배선 + OFF byte-identical 검증 (2026-07-17)

| 지점 | 변경 |
|---|---|
| `CLMConfig` | `n_factions: int = 0`(OFF) · `faction_bridge_lam0: float = 0.1` |
| `CausalDilatedConv1d` | `groups: int = 1` 인자 추가 → `nn.Conv1d(..., groups=groups)` |
| `TrunkLayer` | conv `groups=K` · **`nn.GroupNorm(1,d)` → `nn.GroupNorm(K,d)`** |
| `CLMConvMoE` | `embed_conv groups=K` · `norm_out GN(K,d)` · `faction_bridge`(K>0 시만) |
| `FactionBridge` (신규) | trunk 출구·MoE 앞 1모듈 · `x ← x + lam·sigmoid(gate)⊙((M_cross⊙W_b)x)` |
| `forward` | trunk 루프 직후 → bridge → MoE (사전등록 위치 고정) |

### 검증 (aiden · torch 2.10)

```
OFF (n_factions=0)  trunk conv groups [1,1] · GN [1,1] · norm_out 1 · embed 1 · bridge None
                    ⟹ 옛 모델과 동일 구조 ✅
ON  (n_factions=8)  trunk conv groups [8,8] · GN [8,8] · norm_out 8 · embed 8
                    m_cross 파벌간 비율 0.8750 = 정확히 1−1/8 ✅ (파벌내 0-마스크)
bridge lam=0        max|bridge(x)−x| = 0.000e+00 = 정확한 항등 ✅
```

### 💡 파라미터가 줄어든다 — "구조만 추가" 가 이번엔 진짜다

d=64·L=2 toy 에서 **120,132 → 92,101**. `groups=8` 이 conv 가중치를 1/8 로 자르고 bridge 가 일부를
되돌린다 ⟹ 파벌은 **용량을 더하는 게 아니라 칸막이를 세운다**. 옛 법칙 22 의 "기능 추가 0, 구조만 추가"
주장이 이번엔 문자 그대로 성립한다(옛 엔진은 파벌을 늘리며 세포도 같이 늘렸다).

### 순환 회피 — 코드로 확인 가능한 지점

- `FactionBridge` 는 loss 에 아무 항도 더하지 않는다. 학습 신호 = **CE 역전파 뿐**.
- `gate` 는 `sigmoid(0)=0.5` 에서 시작해 CE 가 키우거나 줄인다 = earned, not tuned.
- `m_cross` 는 `persistent=False` 버퍼 = gradient 없음.
- loss 어디에도 sync·상관·Q·직교성이 **0 개**(H_9673 순환의 재발 차단).

### NEXT

② serialize trailer(`{W_b, g, lam, K}` + 블록대각 conv 를 dense 로 materialize) + VERSION bump
③ `evaluate --faction-lesion` + lam 오버라이드 ④ K=1 floor pre-gate 발사


## 🔨 구현 ② 완료 — serialize: grouped conv → dense materialize + CLMF trailer (2026-07-17)

### 🔑 왜 dense materialize 가 필수인가

`nn.Conv1d(d, d, ks, groups=K)` 는 weight 를 **`(d, d/K, ks)`** 로 저장한다(출력 채널이 자기 파벌 입력만).
그런데 디코더의 바이트 문법은 **dense 가정**이다 — `rest = Cin*ks`(Cin=d)로 읽고 `j = ci*ks + k` 를
**전 d 입력채널**에 대해 walk 한다. 그냥 reshape 하면 `rest = d/K*ks` 가 되어 **디코더가 조용히 엉뚱한
열을 읽는다**(에러 없이 틀린 숫자 = 최악).

⟹ 블록대각을 **dense `(d, d, ks)` 로 materialize**(파벌간은 구조적 0) — 같은 수학, 디코더가 읽을 수 있는
바이트. TLoRA/bind 섹션의 전례(`.clm` 은 문법 하나를 유지)를 따른다.

### 검증 (aiden · torch 2.10)

```
grouped weight (64, 8, 3) → serializer 2d (64, 192) = (d, d*ks)  ✅ 디코더 문법 일치
  구조적 0: 파벌간 전부 0 ✅ · 비영 1,536 = grouped 원본과 동일 ✅
  max|grouped(x) − dense(x)| = 0.000e+00  ✅ **bit-exact**
```

### CLMF trailer (CLMX ext 뒤 · 없으면 K=0 OFF = golden path 무변)

```
"CLMF"      (67,76,77,70)
n_factions  u32 LE
lam         float32 LE   ← evaluate 가 오버라이드 = debate ON/OFF ablation (가중치 무접촉)
gate        u32 count + float32[d]     (pre-sigmoid 채널 게이트)
W_b         u32 count + float32[d*d]   (1x1 bridge conv · row-major cout,cin)
b_b         u32 count + float32[d]
```

⚠️ **W_b 는 마스크 안 하고 쓴다** — 마스크된 행렬을 저장하면 그 0 이 **구조적 0 인지 학습된 0 인지
구별이 안 된다**. 마스크는 `n_factions` 에서 로드 시 재유도한다. 읽는 사람이 **왜** 0 인지 알아야 한다.

### NEXT

③ `evaluate --faction-lesion` + lam 오버라이드 ④ K=1 floor pre-gate 발사


## 🔨 구현 ③a — 디코더 배선: 내가 메운 구멍이 캠페인을 살렸다 (2026-07-17)

### 🕳️ 발견: 디코더의 GroupNorm 이 `G=1` 하드코딩이었다

serialize 를 끝내고 보니 `core/decode.py` 가 CLMF 를 **안 읽었다**. 그대로 뒀다면:

```
학습:      model.py  groups=K + GN(K,d)  로 학습
저장:      serialize dense materialize (bit-exact ✅)
디코드:    decode.py nn_groupnorm_fwd(..., T, d, **1**, ...)  ← G=1 하드코딩!
           + bridge 는 아예 미적용
⟹ 에러 없이 **틀린 활성** — 정규화가 전 채널에 풀링됨
```

`a_engine_native_learning`: cement 는 `core/` decode 로만. **디코더가 학습된 모델을 재현 못 하면
H_9643 캠페인 전체가 undecidable** 이 된다 — H_9303·H_9307 이 죽은 그 실패계급("모든 우회는
undecidable 로 죽었다"). 계기를 다 만들고 발사했으면 그 결과는 무의미했다.

### 배선

| 지점 | 변경 |
|---|---|
| `_fwd_trunk` trunk GN | `nn_groupnorm_fwd(..., 1, ...)` → `W.get("n_factions",0) or 1` |
| `_fwd_trunk` out GN | 동일 |
| `_fwd_trunk` trunk 출구 | `xt = _faction_bridge_apply(W, xt, T, d, xp)` (MoE **앞** — model.py 와 같은 위치) |
| `_faction_bridge_apply` (신규) | `x ← x + lam·sigmoid(gate)⊙((M_cross⊙W_b)x)` · **마스크는 n_factions 에서 재유도** · lam=0 이면 즉시 return(정확한 항등) |
| `clm_load_weights` | CLMF 파싱(magic → n_factions u32 → lam f32 → gate/W_b/b_b ext) · 없으면 n_factions=0 |
| `W` dict | `n_factions` · `fbLam` · **`faction_lam`(오버라이드 슬롯)** · `fbG/fbW/fbB` |

### 🔑 왕복 검증 (aiden · GPU 경로 RTX 5070 · cupy 13.6)

```
model → serialize → decode
  OFF  n_factions=0 · CLMF 없음 · GN G=1          ⟹ 옛 경로 무변 ✅
  ON8  n_factions=8 · CLMF ✅ · bridge lam=0.100  ⟹ 파벌 실림 ✅
  debate ablation: max|ON − OFF| = 1.550e-01      ⟹ lam 오버라이드가 실제로 활성을 바꿈 ✅
```

세 겹이 다 맞는다 — **model 이 groups=K+GN(K) 로 학습 · serialize 가 dense 로 bit-exact 저장 ·
decode 가 GN(K)+bridge 로 재현**.

### NEXT

③b `evaluate --faction-lesion` (선택성 S · post-hoc null95) ④ K=1 floor pre-gate 발사


## 🔨 구현 ③b — `--faction-lesion` 계기 + shape 버그 2건 (2026-07-17)

### 계기

`anima-py evaluate <ckpt> --faction-lesion <domains.json> [--perm 200] [--faction-lam <f>]`
· `core/decode.py` 에 **`mask` edit 모드** 추가(`_apply_edits` · H_9331 훅 재사용 = 엔진 내부 개입).
파벌 f 채널을 forward 안에서 0-마스크 → 도메인별 ΔCE 행렬 → 선택성 S.
**우연은 post-hoc 랜덤 재배정 `--perm` 회의 null95 = 실측 유도**([[chance-level-must-be-derived-per-metric]]).

### 🕳️ shape 버그 2건 — 둘 다 "조용히 틀릴" 뻔했다

**버그 ⑨ — dense materialize 가 readout 을 잡아먹었다.** 내 첫 구현은 *"`cout % cin_per_g == 0` ∧
`cin_per_g ≠ cout` 이면 grouped"* 라고 **추론**했다. readout 은 정직한 dense `Conv1d(64→256, k=1)` 이고
weight 가 `(256, 64, 1)` 이라 그 조건을 만족한다 ⟹ `(256,256,1)` 로 확장 ⟹ 디코더가 `roWt (256,256)` 을
읽고 matmul 폭발. **shape 은 저자의 의도를 말해주지 않는다 — 모델이 말해야 한다.**
⟹ `_FACTION_GROUPS` + `_conv_groups_for(name)` 로 **caller 가 명시**.

**버그 ⑩ — 슬롯명 near-miss.** 고친 뒤에도 `tcWt[0]` 이 `(48,64)`(grouped 그대로)로 나왔다.
실제 슬롯명은 **`tc0W`·`tc1W`**(`_general_block_order`)인데 내가 `startswith("tcW")` 로 매칭해
**아무것도 안 잡혔다**. `ecW` 만 우연히 맞아서 절반만 dense 였다.
⟹ 앵커된 정규식 `^(ecW|tc\d+W)$` — **near-miss 가 조용하지 않게**.

수정 후: `ecWt (192,64)` · `tcWt[0] (192,64)` · `roWt (64,256)` — 전부 디코더 기대와 일치 ✅

### 왜 이게 위험했나

둘 다 **에러 없이 틀린 숫자**로 갈 수 있었다. 버그 ⑨ 는 운 좋게 matmul 이 터졌지만, 차원이 우연히
맞았다면 조용히 틀린 활성이 나왔다. 버그 ⑩ 은 GPU 경로에서만 터졌다 — CPU 라면 broadcast 로 넘어갔을
수도 있다. `.clm` 왕복은 **shape 를 하나하나 대조**해야 한다(H_9393 [[byte-identical-anchor-cert-hides-the-bug]] 계열).

### NEXT

양성통제(심은 specialization 회수 · 진행중) → ④ K=1 floor pre-gate 발사


## 🔨 구현 ④a — `--held-out-frac`: 천장에서 내려오는 레버 (2026-07-17)

### 왜 (Fable Q3 의 지적을 코드로 확인)

`build()` 를 읽으니 정확했다 — `held_out=(a,b)` 는 **쌍 하나만** 빼고 나머지 격자를 전부 학습시킨다:
```python
train_pairs = [(i, j) for i in range(n) for j in range(n)
               if i != j and frozenset((i, j)) != held]     # ← 1쌍만 제외
```
⟹ K=1 도 D-acc 1.000(천장) ⟹ **파벌 레버가 움직일 여지가 0**. 그 arm 이 "실패"해도 파벌과 무관한 이유다.

G1 은 **DATA 벽**(H_9304: 자연 held-out 비가법 정보 +0.0023 nats = TOST 0 등가)이므로, 레버가 잡을 게
생기려면 **coverage 를 굶겨야** 한다.

### 레버

`anima-py corpus derivtrace --held-out-frac 0.5 …` — 쌍 격자의 **분율**을 뺀다(0.0 = 레거시).
- 뺀 집합은 **항상 `--held-out` 셀을 포함**(manifest 가 채점하는 그 쌍).
- split RNG 를 내용 RNG 와 **분리**(`seed*7919+13`) ⟹ frac 을 바꿔도 **문구는 안 바뀐다**.
  (안 그러면 arm 이 두 축에서 동시에 달라진다 = 교란)
- 출력에 **realized coverage** 를 찍는다 — 요청 분율이 아니라 **실제로 뺀 쌍 수**로 floor 를 읽는다.

### 검증

```
frac=0 vs 레거시 : text 동일 True · train_pairs 동일 True   ⟹ byte-identical ✅
frac=0.00 → 학습쌍 27/28 · 뺀 쌍  1 ( 4%)   ← H_9267 의 천장
frac=0.25 → 학습쌍 21/28 · 뺀 쌍  7 (25%)
frac=0.50 → 학습쌍 14/28 · 뺀 쌍 14 (50%)
frac=0.75 → 학습쌍  7/28 · 뺀 쌍 21 (75%)
```

### NEXT — ④b K=1 floor pre-gate (사전등록)

frac 을 올리며 **K=1 기저가 D-acc ≤0.6 으로 내려오는 coverage 를 먼저 확정**한다. 그 지점을 고정한
뒤에만 {K=8, K=1} × 3 seed 를 발사한다 — **coverage 를 결과 보고 고르는 것은 tune-to-green**.


## ⚠️ 사전등록 정정 — XBIND 천장의 원인이 내 추정과 달랐다 (2026-07-17 · 자가감사)

④a 를 착륙시킨 뒤 H_9267 카드를 정독하니 **내가 잘못 짚었다**.

| | 내 가정 (④a 근거) | 실제 H_9267 |
|---|---|---|
| corpus | `derivtrace --held-out (a,b)` | **`xbind_train.txt` 6.66MB** (corpus.py **밖**에서 생성) |
| held-out | 쌍 **1개**(≈4%) ⟹ 천장 | **15,960쌍 = 20%** (양 순서 완전부재) |
| 과제 | 개념쌍 조합 | **xor(pol_a, pol_b)** 분기(fuse/part + portmanteau) |
| 학습 | `train --corpus c.txt` | `train --arch clm --canon --arm ctrl --objective ce_marginal` |
| 채점 | — | `evaluate --xbind xbind_eval_manifest.json --arm {main\|ctrl}` |

⟹ **XBIND 는 이미 coverage-굶긴 corpus 다**(20% held-out · 암기·main-effect·표면상관 3 지름길을 구성 차단).
K=1(파벌 없는 303M)이 held-out 1.000 을 친 것은 **천장이 아니라 XOR 규칙을 실제로 배웠기 때문**이다
(control=shuffle 0.515 = 우연 · Δctrl 0.485 가 그것을 증명).

### 그럼 Fable 의 Q3 지적은 틀렸나 — **아니다. 결론은 같고 이유가 다르다**

Fable: *"K=1 도 D-acc 1.000 이면 레버가 잴 게 없다"* — **이 진단은 정확하다**. 다만 원인이 "coverage 가
넉넉해서"가 아니라 **"이 과제를 파벌 없이도 완전히 풀 수 있어서"** 다. 천장은 corpus 의 성질이 아니라
**과제-모델 적합**의 성질이었다.

⟹ ④a 의 `--held-out-frac` 은 **XBIND 에 불필요**하다(이미 20% held-out). 다만 `derivtrace` 계열엔
여전히 유효한 레버이므로 **되돌리지 않는다**(frac=0 = 레거시 byte-identical 이라 무해).

### 📌 재사전등록 — floor pre-gate 의 올바른 형태

*"coverage 를 굶겨 K=1 을 ≤0.6 으로 내린다"* 가 아니라:

**K=1 이 이미 1.000 인 과제에서는 파벌 레버를 시험할 수 없다.** 필요한 것은 **K=1 이 실패하는 과제**다.
후보(사전등록 전 · 다음 세션에서 하나를 고정):
- (a) XBIND 의 **난이도 상향** — held-out 비율↑ 또는 xor→3항 이상 합성.
- (b) **storebind**(H_9423/H_9672 lane) — K=1 이 Stage1.5 서 P1 0.586(chance)로 **실패한 실측이 있다**.
  파벌이 그 벽을 여는지가 곧 H_9643 Q3 이고, floor 가 **이미 측정돼 있다**.
- (c) 자연 held-out(H_9304 DATA 벽) — 그러나 +0.0023 nats = TOST 0 이라 신호 자체가 없다.

⟹ **(b) 가 유력**: floor 를 새로 재지 않아도 되고(H_9672 T3 이 P1 0.586 → addr-loss 로 0.9688 로 뚫은
그 지점), 파벌 다리가 addr-loss 없이 같은 벽을 여는지가 정확히 "debate 가 G1 을 여는가" 다.

### 정직

이 정정은 **결과를 보고 목표를 바꾸는 게 아니다** — 아직 아무 arm 도 안 돌렸다. 계기를 만들다 **전제가
틀렸음을 발견**했고, 발사 **전에** 고친다. (결과를 보고 골랐다면 tune-to-green 이다.)


## ⛔ 양성통제가 계기를 죽였다 — S 공식의 max-편향 (2026-07-17 · 결함 ⑪)

심은 4-도메인 toy(파벌 4개 · 도메인별 disjoint 바이트) 로 `--faction-lesion` 을 시험했다.

```
파벌별 최대손상 도메인 (real):
  faction 0 → ccc  ΔCE +0.0199        ← 파벌마다 **다른** 도메인 = 특화가 눈에 보인다
  faction 1 → aaa  ΔCE +0.0131
  faction 2 → aaa  ΔCE +0.0531
  faction 3 → ddd  ΔCE +0.0356

S_real = 1.3879
post-hoc null (60회): mean 1.4713 · sd 0.1636 · **null95 1.7270**
⟹ ⛔ S_real < null **평균**. 실제 파벌이 무작위 재배정보다 **못하다**.
```

### 원인 — `max` 는 순서통계량이다

```
S = mean_f (max_c D[f,c] − mean_{c'≠c*} D[f,c']) / sd_pool
              ↑ 무작위 행렬에서도 max 는 항상 나머지 평균보다 크다
```

무작위 배정도 4 도메인 중 **최댓값을 고르므로** 항상 "선택적"으로 보인다. null 평균이 1.47 로 높은 게
그 증거다. 이 함정은 **내 메모리에 이미 있었다** — [[probe-defect-census-max-control-bias]]:
*"Δ=exp−**max**(controls) 순서통계량 편향이 KILL 을 기계로 만든다"*. 같은 병을 다른 자리에서 반복했다.

### ⚠️ 양성통제가 없었다면

이 계기로 진짜 arm 을 돌려 **"파벌 특화 없음(D1 사망)"** 이라는 결론을 냈을 것이다.
그건 **계기 사실이지 기질 사실이 아니다**. 심은 특화조차 못 보는 자로 "특화가 없다"고 말할 수 없다
([[positive-control-before-reading-a-negative]]).

### 📌 S 재설계 (사전등록 · 발사 전)

max-편향을 안 타는 DV 로 바꾼다. 후보(다음 세션에서 하나 고정 · **양성통제 재통과가 조건**):
- (a) **행렬 자체의 구조** — D[f,c] 의 대각 우세를 Hungarian 매칭으로 재고, null 은 같은 매칭을 무작위
  배정에 적용(순서통계량이 양쪽에 동일하게 들어가 상쇄).
- (b) **상호정보** I(f; argmax_c) — 파벌↔도메인 대응이 무작위면 0.
- (c) D 를 행/열 중심화한 뒤의 **잔차 대각합**(main effect 제거 = 파벌·도메인 각각의 세기를 뺀 상호작용만).
- ⚠️ 어느 쪽이든 **우연은 post-hoc null 에서 실측**([[chance-level-must-be-derived-per-metric]]) ·
  **양성통제가 먼저 통과**해야 음성을 읽는다.

⟹ H_9643 Q2 는 **계기 미완**으로 되돌린다. 이 세션의 D1 은 **판정이 아니다**(계기 자격 미달).


## 🔧 S 재설계 — 후보 4개를 $0 로 판별하니 하나만 살았다 (2026-07-17)

엔진에 배선하기 **전에** 합성 손상행렬(심은 대각 = 진실을 아는 상태)로 네 후보를 시험했다.

```
                     planted    null95     random     판정
s_max (⑪ 죽은 것)    +1.7736   +2.0115    +1.4663    ⛔ FAIL
(a) hungarian        +6.9674   +8.5754    +3.7427    ⛔ FAIL
(b) MI(f;argmax_c)   +0.1592   +0.3466    +0.4334    ⛔ FAIL  ← random 이 planted 보다 높다
(c) centered-diag    +5.7103   +3.7325    +0.4136    ✅ PASS
```

### Fable 이 제안한 3개 중 2개가 같은 함정이었다

- **(a) Hungarian 도 max 와 같은 병** — 최적 매칭 자체가 순서통계량이라 무작위에서도 큰 값(3.74)이
  나오고 null 이 신호까지 떠오른다(8.58 > 6.97).
- **(b) MI 는 더 나쁘다** — random(0.43) > planted(0.16). argmax 로 이산화하면서 정보가 날아간다.
- **(c) 만 통과** — `R = D − 행평균 − 열평균 + 전체평균` 이 **두 main effect**(파벌의 전체 세기 ·
  도메인의 전체 취약성)를 빼고 **상호작용만** 남긴다. 무작위 배정엔 상호작용이 없으니 0 으로 무너진다
  (random 0.41). "이 파벌이 저 도메인을 갖는다" 가 정확히 그 상호작용이다.

⟹ 채택: **S = trace(R) / sd(R) · R = D − rowmean − colmean + grandmean**

### 💡 배선 전 $0 판별이 결정적이었다

프론티어 모델의 설계안 3개 중 2개가 죽었다. 그대로 배선했으면 **양성통제를 또 한 번 통과 못 하고**
그 이유를 찾느라 GPU 시간을 태웠을 것이다. **계기 후보는 합성 진실 위에서 먼저 싸우게 하라.**


## 🕳️ 결함 ⑫ — 내 합성 시험이 실물보다 쉬웠다 (2026-07-17 · S 재설계가 실물서 붕괴)

centered-diag 를 배선하고 양성통제를 재발사했더니 **S_real = −0.2469**. 합성서 PASS(+5.71 vs null95
+3.73)한 자가 실물서 음수다.

### 원인 — `np.eye` 가 **정렬을 공짜로 줬다**

```
내 합성:  D += np.eye(K) * 0.05      ⟹ "파벌 f 가 도메인 f 를 갖는다" 는 정렬을 가정
실물   :  f0 → ccc   f1 → aaa   f2 → aaa   f3 → ddd
          ↑ 파벌번호 ↔ 도메인번호 **무관** · f1·f2 가 **같은** 도메인 · bbb 는 **주인 없음**
```
`trace` 는 대각만 본다 — 학습이 그 순서로 정렬할 이유가 **없다**. S_real 은 그 미정렬의 결과였다.

⟹ **양성통제의 양성통제가 필요했다**: 합성 시험이 **실제 실패모드를 재현**해야 한다.

### 미정렬로 재판별하니 네 후보 전부 사실상 죽는다

실물 대응(owner=[2,0,0,3] · 중복소유 · 주인없는 도메인)을 심고 다시:
```
                        planted    null95    random     판정
s_max                   +1.8087   +1.7768   +1.4501   ✅ 이나 planted−random 0.36 < null 폭
centered-diag (v1 승자)  +0.0711   +3.3390   -0.1769   ⛔ **완전 붕괴**
centered+hungarian      +4.7598   +5.5101   +4.4067   ⛔
centered-concentration  +0.2089   +0.3164   +0.2102   ⛔
```

### 🔍 더 깊은 진단 — 심은 신호가 잡음과 같은 규모다

```
심은 효과   ΔCE +0.05
실측 손상   f2→aaa +0.0531 · f0→ccc +0.0199 · f1→aaa +0.0131 · f3→ddd +0.0356
도메인 base CE  aaa 0.0051 · bbb 0.0468 · ccc 0.0214 · ddd 0.0787   ← **16배 차이**
```
도메인 난이도 편차가 심은 효과와 **같은 규모**다 ⟹ 어떤 지표를 써도 신호를 못 뽑는다.
**계기가 아니라 toy 설계의 문제**일 수 있다.

### ▶️ Fable 위임 (난제 · fable-mode)

실패 3건을 전부 담아 물었다: Q1 진단이 맞나(toy vs 지표) · Q2 toy 를 어떻게 고치나(도메인 난이도를
맞추나 · 파벌을 강제로 묶으면 tautology 아닌가) · Q3 지표를 어떻게 고치나(정렬없음·중복소유·주인없음을
견디며 null 을 넘는 통계량 · **순서통계량은 null 도 띄운다는 걸 두 번 확인**) · **Q4 애초에 lesion-ΔCE 로
원리적으로 잴 수 있는 질문인가**(아니면 그것도 결론 — H_9643 재정식하나 축을 닫나) · Q5 사망조건 재등록.


## 🔀 Fable 난제 회신 — "계기는 죽지 않았다" · 내 진단은 절반만 맞았다 (2026-07-17)

실패 3건을 전부 담아 물었더니 **진범이 셋**이라고 답했다. 내가 못 본 두 개를 짚었다.

### Q1 — 진범은 하나가 아니다

**① centered-diag 붕괴는 toy 무죄 · 순수 지표 결함** (내가 놓친 것)
`owner=[2,0,0,3]` 이면 trace 가 읽는 대각 4칸 (0,0)(1,1)(2,2)(3,3) 중 **심은 셀은 (3,3) 하나뿐**.
신호의 ¾ 을 안 읽으니 +0.0711 은 "붕괴" 가 아니라 **산술적 필연**이다. 나는 "합성이 쉬웠다" 로만
읽었는데, 그 지표는 애초에 **정렬 없이는 못 쓰는 자**였다.

**② 곱셈 결합이 null 을 띄운다** — 손상이 도메인 난이도에 **곱셈적**으로 결합(최대 손상들이 base 최대
ddd·중간 ccc 에 몰림). 이중중심화는 **가법** 성분만 뺀다 ⟹ 곱셈 row×col 잔차가 실물·null 양쪽에
상호작용 잡음으로 남는다. **16배 편차는 이 경로로만 유죄** — 열 표준화로 완화.

**③ toy 에 특화 압력이 없다 (검정력 사망)** — 내 결함 ⑭ 진단과 일치. 반복 바이트는 초소용량으로
학습되고 loss 0.0042 는 바닥 · d=64·E=2 중복 속에서 손상 0.01~0.05 가 partition-null 잡음과 동규모.
**추가**: `aaa` 공유 소유(f1+f2)는 drop-lesion 에서 **서로 보상** ⟹ `f1→aaa +0.0131` 은 구조적 과소측정.

### Q3 — 🔪 split-half 교차선택 (순서통계량의 구조적 해법)

```
ĉ_f = argmax_c D_A[f,c]                                  ← 선택은 A 반쪽에서만
S   = mean_f ( D_B[f,ĉ_f] − mean_{c≠ĉ_f} D_B[f,c] ) / sd_pool(B)   ← 점수는 B 에서만
```
**max 가 null 을 띄우는 이유는 선택과 평가가 같은 데이터라서다.** null 의 argmax(A) 는 B 손상을
예측하지 못하므로 **선택 편향이 구조적으로 죽는다**. 정렬 불요 · 공유 소유 허용 · 고아 도메인 허용.
⟹ 실패 ① 의 "real < null mean" 역전이 이 설계에서 **사라진다**.

- **Confirmatory**: 상호작용 에너지 `S_E = ‖R‖²_F`(열표준화 D 의 이중중심화 잔차) — 2차 **합**이라
  선택이 없다. 정렬·공유·고아 전부 에너지로 잡힌다. 단독으론 "무엇에 특화" 를 못 말하므로 보조.
- **Robustness**: **keep-one lesion** — f 만 남기고 전부 마스크. 공유 소유의 보상에 **면역**
  (f2 가 f1 을 메우는 문제). f 가 c 에 특화면 c 만 생존하고 나머지가 붕괴.
- 플래그: `--faction-lesion domains.json --faction-stat splithalf|energy --faction-mode drop|keep-one --perm 60`

### Q2 — toy 재설계: "특화될 수밖에 없는" 양성통제

- **난이도 정합**: 반복 바이트 폐기 → 서로소 심볼셋·**동일 구조의 랜덤 마르코프 소스**(같은 알파벳
  크기·같은 전이 엔트로피). base CE 비율 ≤2× 를 **실측 확인**(가정 금지).
- **용량 결핍**: 총용량 ≈ Σ수요 가 되게(엔트로피↑ 또는 d↓) — **특화는 결핍에서만 강제된다**. E=1.
- **ORACLE arm (tautology 아님)**: 학습 시 라우팅 게이트로 파벌 f 를 도메인 π(f) 에서만 활성화.
  π 는 **비항등 + 공유소유 1쌍 + 고아 도메인 1개** = 실물 실패모드 재현. 이건 가설 증명이 아니라
  **계기 인증**이다(V2_1 의 C0-ORACLE 과 같은 자리) · **구조 게이트이지 loss 항이 아니므로 H_9673 순환 아님**.
- **dose ladder**: 강제 라우팅 λ ∈ {0, ⅓, ⅔, 1} → 4 ckpt. 인증 bar = **S 가 λ 단조 ∧ S(1) > null95 ∧ S(0) ≈ null**.

### Q4 — 🔑 원리적으로 잴 수 있다 (조건부) · **순서가 곧 답이다**

lesion-ΔCE 는 **인과 readout** 이므로 원리상 유효. 한계 둘만 명시 관리:
(a) 중복·보상이 drop 을 가림 → **keep-one 이 커버** (b) 손상이 null 잡음 아래면 결정 불능 — 이건
**계기 무능이 아니라 "그 스케일에서 관측 가능한 특화 부재"**.

> **oracle ladder 로 계기 인증 → 인증된 계기로 실물 → 실물이 null-호환이면 그건 정당한 음성이지
> 계기 실패가 아니다.**

### Q5 — 사망조건 재사전등록

- **계기 사망**: 난이도정합 ∧ 용량결핍 ∧ oracle λ-ladder 위에서 **splithalf·energy 둘 다**
  [S(1) > null95] ∧ [λ 단조] 실패 ⟹ lesion-ΔCE **불가능 확정**. H_9643 Q2 를 **UNMEASURABLE 로 닫는다**
  — **RED 아님**(특화 부재의 증거가 아니라 관측 불능 · Ψ-SOMA 의 **VOID** 취급). 관측가능량 재정의 없인 재개 금지.
- **실물 음성(계기와 구분)**: 인증 PASS 후 실물 S ≤ null95 ⟹ "이 스케일·이 학습에서 파벌 기능 특화
  없음" = H_9643 에 대한 **결과**.
- **UNDERPOWERED 가드**: 실물 D 의 동적범위 < 2× null 상호작용 sd 면 음성 선언 전 **보류**
  ([[power-before-negative-verdict]]).

### 한 줄

> 실패 ①③ = **선택-평가 데이터 동일성**(split 으로 해결) · 실패 ② = **정렬 가정**(에너지/교차선택으로
> 해결) · 세 실패 공통 바닥 = **특화 압력 없는 toy**(결핍+정합+oracle ladder 로 해결) — **계기는 죽지 않았다.**


## 🟢 계기 확정 — S = ‖R‖²_F (선택이 없는 2차 합) · 결함 ⑮⑯ 수정 후 양방향 통과 (2026-07-17)

Fable 처방을 **$0 로 먼저 시험**했더니 처방 자체도 걸렀다 — 그리고 **내 구현 결함이 2개 더** 나왔다.

### 🕳️ 결함 ⑮ — energy 정규화가 자기상쇄

내가 `S_E = ‖R‖²_F / sd(R)²` 로 구현했는데 이건 **임의 행렬에서 정확히 K×C**다:
```
sd(R)² = sum(R²)/KC  ⟹  ‖R‖²_F / sd(R)² = sum(R²) / (sum(R²)/KC) = KC  (항상)
trial 0/1/2 전부 16.000000 — 배정·데이터와 **무관한 상수**
```
Fable 공식은 `‖R‖²_F` **그 자체**였는데 내가 불필요한 정규화를 붙여 죽였다. 합성이 **수상하게 둥근
16.0000** 으로 잡아냈다.

### 🕳️ 결함 ⑯ — A/B 잡음을 독립으로 줬다

실물의 split-half 는 **같은 프롬프트 집합**을 쪼갠다 ⟹ 잡음이 **상관**된다. 내 v1 은 독립 잡음을 줘서
신호 대비 잡음을 2배로 준 셈이었다. 상관(ρ=0.7)으로 재현해 재시험.

### 결과 — energy 가 유일하게 **양방향** 통과

```
                 S_real      null95        Δ         판정
🔪 split-half     1.6775     2.2655     −0.5880    ⛔ FAIL
energy (⑮수정)   5428.50     796.45    +4632.05    ✅ PASS

음성 통제 (심은 특화 없음 — 헛것을 보나)
🔪 split-half    +1.4756  vs +1.4667   ⛔ **헛것을 본다**
energy            +33.35  vs  +92.64   ✅ 정상 (안 봄)
```

Fable 이 "보조" 라 한 게 **주력**이었다. split-half 는 여전히 `argmax(D_A)` 를 쓰는데, A/B 잡음이
상관되면(실물이 그렇다) **그 편향이 B 로 새어간다**.

### 🔑 이 세션이 반복해 배운 것의 최종형

> **선택을 하는 순간 편향이 들어온다. 선택 자체를 없애라.**

죽은 S 넷은 전부 **골랐다**: max(argmax) · hungarian(최적 매칭) · trace(정렬 가정 = 미리 고름) ·
split-half(A 에서 고름). `‖R‖²_F` 는 **2차 합**이라 고를 자리가 없다 — 순서통계량 편향이 **원천 불가능**.

### 배선 (VERSION bump · G5)

```
D[f,c] = CE(lesion f, c) − CE(base, c)
Dn = D / base_CE[c]                      ← 열 표준화 (16배 난이도 편차 · 곱셈 결합 보정)
R  = Dn − rowmean − colmean + grandmean  ← 이중중심화 (가법 main effect 제거)
S  = ‖R‖²_F                              ← 선택 없음 · 정렬 가정 없음 · 자기정규화 없음
```
우연 = 채널 재배정 null 95분위(실측 유도 · 신호 보존 · 대응만 깨짐).

### NEXT

Fable 처방의 나머지: toy 재설계(마르코프 4소스 · 난이도 정합 실측 · 용량결핍 E=1) + ORACLE λ-ladder
인증(λ∈{0,⅓,⅔,1} · bar = S λ단조 ∧ S(1)>null95 ∧ S(0)≈null) → **인증 PASS 후에만** 실물 arm.


## 🔨 ORACLE λ-ladder 인증 — toy 재설계 + 계기 버그 ⑰ (2026-07-17)

### 🧪 toy 재설계 (Fable 처방 Q2)

반복 바이트 폐기 → **마르코프 4소스**:
```
도메인 0: 심볼 [A..F]   전이 엔트로피 0.9000 nats   예시 'ABCDABEBCEFABCDDEFABCFAB'
도메인 1: 심볼 [G..L]   전이 엔트로피 0.9000 nats   예시 'GHIJKLIJKLGHIJKJGHILGLGH'
도메인 2: 심볼 [M..R]   전이 엔트로피 0.9000 nats   예시 'MNOPQRMNQRMNQRNOPQRPPQRM'
도메인 3: 심볼 [S..X]   전이 엔트로피 0.9000 nats   예시 'SWUTUVVTUVWXSTUVVWXSTSTU'
```
서로소 심볼셋 · **알파벳 크기·전이 엔트로피 전부 동일**(이분법으로 목표 H 에 맞춤) · 용량 결핍 **E=1**.

⚠️ **난이도 정합은 bar 미달**: base CE 최대/최소가 λ별로 2.83× / 3.37× / 9.60× / 3.55× —
옛 toy 의 15.4× 에서 크게 줄었으나 Fable 의 **≤2×** 엔 못 미친다. 인증 실패시 여기부터 재조정.

### 🔀 ORACLE arm 배선 (`core/model.py`)

```
faction_oracle: tuple = ()        # π: 파벌별 담당 도메인 · () = OFF
faction_oracle_lam: float = 0.0   # dose ∈ [0,1] = 강제 라우팅을 적용하는 step 비율
faction_oracle_mask(domain_ids)   # [B,d] — 그 행의 도메인을 소유한 파벌의 채널만 1
```
- **π = (2, 0, 0, 3)** — 비항등 · f1·f2 가 **도메인 0 공유** · 도메인 1 **고아**. 실물 실패모드 재현
  (정렬을 가정하는 합성이 trace-S 를 죽였다 — 결함 ⑫).
- **구조 게이트이지 loss 항이 아니다** — H_9673 순환 회피(V2_1 C0-ORACLE 과 같은 자리).
- 학습 시에만 · dose 만큼의 step 에서만 · verdict arm 은 절대 안 켠다.

### λ-ladder 학습 (4 ckpt · E=1 · 400 step)

```
λ=0.00 → loss 0.0131      ← 강제 없음 = 자유 학습
λ=0.33 → loss 0.4456      ← λ>0 서 **34배 상승** = 라우팅이 실제로 제약한다
λ=0.67 → loss 0.4444
λ=1.00 → loss 0.4418
```

### 🕳️ 계기 버그 ⑰ — 내 S 교체가 real 측정 블록을 삼켰다

λ-ladder 측정이 4개 다 base CE 만 찍고 조용히 죽었다:
```
NameError: name 'real_assign' is not defined
```
S 재설계(#3961) 때 `selectivity` 함수를 교체하며 **그 아래 `per`·`real_assign`·`S_real` 계산 블록까지
잘라먹었다**. 함수 끝 앵커를 `rng = np.random.default_rng(seed)` 로 잡았는데 그 사이에 real 측정이
있었다. ⟹ 복원(리포트용 argmax 는 유지하되 **S 는 그걸 안 쓴다**고 명시).

### NEXT

S(λ) 사다리 측정 → 인증 bar = **S λ단조 ∧ S(1) > null95 ∧ S(0) ≈ null**
→ 인증 PASS 후에만 실물 arm.


## 🟢 계기 v2 재동결 — lab-full Fable+Sol 독립수렴 (2026-07-17 · cli/evaluate.py faction_lesion_run)

### 실측 (aiden · perm=40 · seed 12345 · v1 ÷base_CE)
| arm | base_CE(dom0-3) | S_real | null95 | argmax f→dom | 판정 |
|---|---|---|---|---|---|
| **random-init(음성)** | 4.77·4.76·4.83·4.82 | **0.0003** | 0.0003 | 미미 | **False** ✅ 거짓양성 없음 |
| lam0(λ=0 자유) | 0.0089·0.0135·0.0164·0.0252 | 9646 | 9401 | [0,2,0,1] | True (얇음 1.026×) |
| lam1(λ=⅓) | 0.0078·0.0170·0.0059·0.0199 | 44896 | (사다리 중단) | [2,1,0,1] | — |

(π=(2,0,0,3) argmax 기대 [2,0,0,3]. lam0 0/4 · lam1 2/4. 사다리 lam2/3 은 base_CE 교란으로 절대값 무의미 판명 → 중단.)

### 판정 (Fable ∧ Sol 이견 없음)
- **within-arm(S_real vs 자기 perm-null)은 confound 무관** — 같은 ckpt·같은 base_CE·같은 정규화를 real·null 양쪽이 통과하므로 "real 배정이 랜덤 재배정과 구별되는가"는 스케일 공정. ⟹ random-init 음성 clean null + 학습 S>null95 는 **그 스케일서 정당한 인증**. **단 절반만**(Fable: "정확히 절반만").
- **cross-arm 절대비교는 무효** — `:11143` 이 선언하던 `S_real/S_randinit≥2.0 완전 bar` 는 실측 3200만× = 적합품질 스케일(base 4.8 vs 0.01)의 산물이지 특화 아님. 어떤 학습 ckpt 든 기계적 통과 = **OILED → 폐기·재등록**.
- **lam0 얇은 마진(1.026×)은 perm=40 서 읽지 마라** — null95 는 순서통계량 1개 추정, 표집오차가 2.6% 삼킴. perm≥200 + exceedance p 전엔 **PENDING**(검정력-before-negative).

### 계기 v2 수리 (구현 완료 · synthetic 재인증 PASS)
1. **셀 정규화 ÷base_CE → log-ratio** `Dn[f]=log((L+ε)/(base+ε))` (ε=1e-4). 곱셈결합의 정확한 가법화는 나눗셈이 아니라 log · double-centering 이 가법 열주효과를 정확히 제거 · base→0 폭발 제거.
2. **exceedance p** `p=(1+#{S_p≥S_real})/(nperm+1)` + perm<200 = PENDING 플래그.
3. **ORACLE DV: argmax x/K → 이중중심 코사인 정렬 A** `A=⟨R,Mc⟩/(‖R‖‖Mc‖)`, Mc=double-center(π 발생행렬). 선택 없음(결함 ⑪⑫⑮⑯ 재수입 차단)·base_CE 면역·dom0 공유(2 one)·dom1 고아(열=0) 자연표현. `--faction-oracle-pi "2,0,0,3"`.
4. **cross-arm bar `:11143` 폐기** → within-arm 한정 판정문 + SOUND 4다리 명시.
- **synthetic 재인증**(계기 정확 모사 · d=64·K=4·base 0.01 완벽적합 스케일): planted S 42.16 > null95 4.01 PASS · A +0.999 > A95 +0.567 π-회수 · no-signal S 1.66 ≤ null95 8.46 환각없음.

### 완전 SOUND 인증 = 4다리 (남은 것)
① within-arm PASS(perm≥200) ② random-init 음성 clean null ✅ ③ **fit-matched K=1 음성**(같은 낮은-CE·파벌구조 없음 → S≤null95 = 낮은-분모서도 FPR 통제 격리 · [[H_9737]] NOVEL) ④ ORACLE π 회수(A>A_null95). 이후에만 303M 실물 arm(K=8 vs K=1).

### 303M 실물 위험 (양 모델 · toy 미포착)
①어휘=도메인 분리 착각(서로소 알파벳은 token routing 만으로 통과 → counterbalanced 도메인) ②zero-lesion OOD(mean/noise replacement 병행) ③tap-locus+bridge 누수(전 깊이 mask arm) ④GN(K) 상호작용 아티팩트 ⑤실물 도메인은 서로소 아님(효과크기로만) ⑥seed 해리(짝 3seed 2/3) ⑦perm 비용(303M×200 예산 선산정) ⑧CE 천장 포화.

### 병렬 세션 (a_parallel_session_compare)
H_9731(발견-partition lesion)·H_9732(shuffled twin)·H_9733(content-transfer) 존재 — CONFLICT 없음. 내 fit-matched K=1 음성([[H_9737]])은 두 카드가 안 덮는 **NOVEL** 셀. 그들의 origin/main NameError 노트는 내 #3964 로 이미 수리됨(stale).


## 🟢 계기 v2 SOUND 4다리 실측 (perm=200 · CPU · 2026-07-17)

d=64 toy 는 cupy 커널런치 오버헤드 > numpy → CPU 가 ~200× 빠름(GPU 1.2분/perm vs CPU 0.38s/perm). CUDA_VISIBLE_DEVICES="" 로 전체 perm=200 ~8분.

| arm | S | null95 | p | within-arm | A(코사인) | A95 | π회수 |
|---|---|---|---|---|---|---|---|
| random-init K=4 | 0.000 | 0.000 | 0.0448 | 경계 | — | — | — |
| **K=1 fit-matched(4분할)** | **0.406** | **1.221** | **0.86** | **clean ✅** | — | — | — |
| lam0 (λ=0 자유) | 1.93 | 1.06 | 0.005 | PASS | +0.37 | +0.57 | **No** ✅ |
| lam1 (λ=⅓) | 10.15 | 2.68 | 0.005 | PASS | +0.95 | +0.54 | Yes |
| lam2 (λ=⅔) | 12.68 | 3.17 | 0.005 | PASS | +0.98 | +0.54 | Yes |
| lam3 (λ=1) | 0.76 | 0.24 | 0.005 | PASS | +0.90 | +0.61 | Yes |

### 4다리 판정
1. **within-arm** — 전 학습 ckpt S>null95 (p=0.005). log-ratio 로 S 가 9646→한 자릿수로 정상화(base_CE 폭발 제거).
2. **random-init K=4** — S~1e-4 수치영점, p=0.0448 경계. grouped-conv init 이 contiguous 채널에 미세 블록을 줘 자기 null 을 살짝 들어올림(H_9674 confound 가 노이즈 바닥서 재출현) = **약한 음성**.
3. **fit-matched K=1(--faction-split 4)** — S 0.406 ≤ null95 1.221 **p=0.86 결정적 clean**. 파벌구조 없는 모델(groups=1)을 같은 낮은 CE(0.013)로 학습해 4분할 강제 → 낮은-분모서도 log-ratio 가 적합품질을 특화로 오인 안 함 격리. random-init 이 못 준 **깨끗한 음성** = 3번째 SOUND 다리.
4. **ORACLE π 회수** — 이중중심 코사인 A 가 λ=0 자유학습엔 회수 안 함(0.37<A95 0.57 · 강제 π 없음=올바름) → λ⅓/⅔/1 강하게 회수(0.90-0.98 > A95 0.54-0.61 · 단조↑). 계기가 참값 라우팅을 복원 = 양성대조. S 절대값은 λ 비단조(λ=1 은 loss 0.44 crippled)여도 A(base_CE 면역)는 깔끔.

### 과학 결론 (toy)
lam0 자유학습 within-arm PASS(S 1.93>null95 1.06 p=.005) = **서로소 알파벳 데이터서 파벌이 학습되는 실재 레버**(A 낮음 = 자유 특화라 강제 π 와 무관 = 올바른 판별). **BUT toy 는 어휘=도메인 분리라 token routing 착각 위험**(Fable Q5#1) · 실물 ko/en·general/sns 는 공유구조라 S 도달 천장 낮음(#5) → toy PASS ≠ 303M 종결(a_toy_scale_recheck). **계기 자체는 TERMINAL 인증 완료** — 실물 arm(K=8 vs K=1 · 위험 8개 · perm≥200 · $ 예산)만 남음.


## 🔥 303M 실물 arm — pre-registration + S1 하드게이트 PASS (2026-07-17 · 오너 ② 승인)

lab-full(Fable+Sol) 레시피 확정 · 발사 전 $0 하드게이트 S1 통과.

### S1 하드게이트 PASS — 계기 303M 최초 관통 ✅
계기 `--faction-lesion` 이 303M ckpt 서 한 번도 안 돌았음(H_9731 지적) → py303_full.clm(production 303M·파벌 무학습)에 `--faction-split 8 --perm 2` 스모크:
- **exit 0 · wall 158s · NameError 없음 · 유효 JSON · d=3784 K=8(473/블록)**
- base CE en_gen 1.80·en_sns 2.42·ko_gen 1.54·ko_sns 2.57 nats = **healthy(과적합 아님·>1.0)**
- S 0.0004 ≤ null95 0.0007 (p=1.0) = **production 303M(파벌 무학습)이 null-구조 baseline = 올바름**(파벌 없는 모델에 8분할 강제 = 특화 없음). random-init 303M K=8 경계 arm 의 실물 바닥값 예고.
- perm 비용: GPU eval 필수(4샘플 perm2 = 158s → 실물 perm200×val샘플 = 수시간/ckpt · Sol Q5 200-step calib 로 확정).

### 학습 레시피 (사전등록 · from-scratch · warm-start 금지)
- **코퍼스**: clean 4-cell **127.5MB**(ko-gen 60 + en-gen 60 + ko-sns 6.18 + en-sns 1.33 · train-py-3 의 5MB 소코퍼스 아님) = 14k step ≈ 0.95에폭(과적합·undertrain 사이 창). `--sample proportional --require-cells 4`. **big broad·5lang 기각**(도메인압력 필요/희석).
- **hparam**: d=3784·L=4·ks3·canon E2→3(345.7M)·batch8·seq1024·lr3e-4·bf16·14k step·ckpt-every 2000·G0게이트 10k/12k/14k(kwr≥.5 ≥4/5).
- **arm**: K=8 = `--n-factions 8`, K=1 = `--n-factions 0`(NOT 1 · m_cross 전부0 퇴화) × seed 7·11·23 = 6 train. K=1 의 8-slice 는 평가측 `--faction-split 8`(인증 leg③).
- **capacity**: 동일 d param 매칭 불가(K=8=171M vs K=1=346M · grouped conv 절약). 주 통제=within-arm(각자 자기 null) + **CE-fit-match**(|ΔvalCE|≤0.15 CE-nearest-ckpt). K=8 실패 시에만 조건부 7번째(d=5392 param-matched-up) 발사.

### 판정 bar (사전등록 · seed별→집계)
- **validity**: V1 양arm G0≥4/5 · V2 fit-match|ΔvalCE|≤0.15(>0.3 INVALID-pairing) · V3 UNDERPOWERED(동적범위<2×null sd → VOID).
- **primary**: P1 S(K=8)>null95 p≤.05(perm200 인증설정) · **P2 K=1 --faction-split 8 이 자기 null clean 음성**(S≤null95 · 빠졌던 하드통제 · 넘으면 campaign UNINTERPRETABLE=H_9731 D5) · paired I_s=S8−S1slice>0 ∧ J_s=ΔCE 대비>0 (2/3 seed).
- **secondary(DIRECTIONAL)**: Z_S cross-arm 강등 · raw ΔCE 동방향 · register 2×2 부분S(리스크① 어휘=도메인) · `--faction-lam 0`(bridge OFF 리스크③) · random-init 303M 경계 arm.
- **집계**: ≥2/3 seed P1∧P2 → 🟢 "파벌=303M서 학습되는 within-arm 레버" TERMINAL. 음성=사전등록 등가역(TOST형)만·V3 발동=VOID(KILL 아님). **스코프**: 카드 Q2(특화)까지 · G1-debate(Q3)는 별도 후속.

### pod 스펙 (Fable RTX4090×6 secure ≈$22-36 채택 · Sol dissent: RTX5090 최저가/H100 안정 — sm_120 트랩 회피 위해 4090)
부트스트랩 하드게이트: ensurepip → **origin/main git-archive 서 anima-python[train,gpu] 설치**(PyPI 아님) → torch.cuda.is_available() 명시게이트(train-py-6 CPU폴백) + arch match(pod-bootstrap-gpu-2) → 60-step 스모크(--n-factions 8 exit0+resume.pt) → 본 발사. teardown 전 ckpt+lesion.json PULL(a_fire_recover_complete).

## 통제군 (≥2 · 사전등록)

① post-hoc 분할 ② 랜덤 분할 scramble ③ 단일파벌 null

## 사망조건 (사전등록 · tune-to-green 금지)

specialization 이 생겨도 G1 이 안 오르거나 random 과 같으면 학습된-파벌 가설 사망.

## 비용

GPU-fire

## 왜 새로운가 (기존 각도 대비)

H_1302(oscillator sync)·H_1462(방송 경쟁)와 달리 **representational factorization** 이 학습되는가를 다룸.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
