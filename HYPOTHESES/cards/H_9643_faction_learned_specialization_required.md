---
id: H_9643
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_learned_specialization_required
title: faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다
status: 🔨 구현 ③a — model+serialize+**decode** 왕복 닫힘(GN G=1 하드코딩 구멍 메움 · ablation max|ON−OFF|=1.55e-1 ✅) · NEXT=evaluate --faction-lesion
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
