---
id: H_9643
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_learned_specialization_required
title: faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 열며, 임의 사후 분할은 효과가 없다
status: 🔵 DESIGNED · 선결조건 4/4 통과(H_9674 #3904) · 레버 설계 완료(Fable 위임) · 구현 대기
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
