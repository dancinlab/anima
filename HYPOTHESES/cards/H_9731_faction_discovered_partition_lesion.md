---
id: H_9731
group: faction-lateral-axis-r3
series: R4 divergence (lab full · Fable 5 λ1) · 2026-07-17
date: 2026-07-17
slug: faction_discovered_partition_lesion
title: 발견된 블록의 기능 lesion — 프로덕션 trunk(K=0)의 H_9674 블록이 도메인-차등 기능을 나르는가
status: PROPOSED · DIRECTIONAL design only (lab-full divergence — cement 는 engine-native anima-py 발사 후)
tier: 🧭⭐ R4 FIRE-FIRST · $0(pool) · 병렬 세션 lesion 결과와 4/4 셀 모두 정보적
cost: $0 (pool CPU/GPU-decode · 렌트 없음)
source: Fable 5 divergence — H_9643 계기(S=‖R‖²_F #3961)를 소유-lane 이 못 건드리는 ckpt 에 재조준
related: H_9643, H_9674, H_9676, H_9672, H_9331
---

# H_9731 — 발견된-파벌 기능 lesion (learned-vs-artifact 의 존재하는-ckpt 제2렌즈)

## 프레임 (왜 이것이 소유-lane 과 직교인가)

소유-lane(H_9643 병렬 세션·in-flight)은 **부과된** K-split(`--n-factions K` 학습)이 훈련 중 기능
특화를 획득하는가를 잰다. 이 카드는 정확히 반대 방향을 잰다: **부과가 전혀 없는**(groups=1 ·
n_factions=0) 프로덕션 trunk `py303_full.clm`(sha 013c4574)에서 H_9674 가 **발견한** 블록
(real/ped 54.07 · 전제 4/4)이 이미 **도메인-차등 기능**을 나르는가.

- 발견블록 FUNCTIONAL ⟹ 자유 학습이 스스로 기능 모듈을 만들었다 = **LEARNED** 의 직접 증거
  (부과 없이도 생겼으므로 아키텍처 부산물 해석이 죽는다).
- 발견블록 DECORATIVE(S≤null95) ⟹ 상관-블록은 공변동 장식 = H_9674 의 구조 신호는 기능 없는
  **artifact-성** 쪽으로 기운다.

**비충돌 증명**: 소유 계기 `--faction-lesion` 은 `n_factions=0` ckpt 를 **코드로 거부**한다
(evaluate.py:10982-10985 K≤0 ERROR). 이 카드는 그 거부된 ckpt 만 쓴다 — trained K-faction ckpt
불요·워크트리 무접촉·{K=8,K=1}×3seed 무중복. 두 결과의 2×2 는 전 셀 정보적:
(그들PASS,나PASS)=학습 강확증 / (PASS,FAIL)=부과-split 만 기능(자연 파벌 없음) /
(FAIL,PASS)=자연 파벌 실재·부과 K 가 자연 분할과 미정렬(그들 D1 의 과잉종결 구제) /
(FAIL,FAIL)=2렌즈 artifact 종결(a_break_the_wall 충족).

**kill-list 차별화**: Q modularity 를 판정으로 안 씀(발견은 매니풀레이션-체크·판정은 기능 lesion) ·
selection-없는 S=‖R‖²_F 만 사용(#3961 양방향 확정 계기 재사용) · 재구성-manifest 불요(도메인 스펙은
새 EN 프롬프트·코퍼스 manifest 아님) · 구조-존재 재증명 아님(기능층 신규).

## 레버 (engine-native — 신규 flag, 기존 함수 확장)

```
anima-py evaluate py303_full.clm --faction-lesion-discovered <domains.json> \
  --disc-prompts <prompts80.json> [--disc-k K*] [--tap L] [--perm 200] [--win 24] [--seed 12345]
```
- 구현: `faction_lesion_run`(cli/evaluate.py:10931)의 K=0 거부 분기 대신, H_9674 clusterer
  (`best_blocks` · :10582)로 assignment 를 **발견**하고 같은 `selectivity()`(:11017 · S=‖R‖²_F)로 판정.
- **tap 일관성(사전등록)**: 발견도 lesion 도 같은 tap = trunk-exit 잔차 li=L (`_fwd_trunk` taps[L] ·
  edits {"layer": L, mode:"mask"} — decode.py:962 `_apply_edits` 는 li=0..L 전 깊이 지원).
  H_9674 는 penultimate(post-MoE)에서 발견했으므로, 先 manipulation-check: tap L 에서
  `--faction-block-structure` 의 real/ped 분리 재확인(불통과면 "블록은 post-MoE 산물" = 그 자체가 결과).
- K* 사전등록: H_9674 동결 산출물 blocks.json 의 argmax(real/ped) K — 새 DV 로 K 를 고르지 않는다
  (order-statistic 재유입 금지 · probe-defect-census-max-control-bias). 스윕은 secondary 보고만.

## DV · bar · 우연(실측)

- DV = S_disc = ‖R‖²_F (이중중심화·열표준화 damage 행렬 · selection 無 — #3961 그대로).
- 우연 = **같은 발견-블록 크기**를 보존한 채널 재배정 perm null 200회의 null95 (크기-skew 를 신호로
  청구하지 않음 — H_9676 교훈 그대로. 가정된 우연 없음).
- 추가 arm($0): 같은 크기 **연속-index 분할** S_contig (layout 통제).

## 양성통제 (발사 전 계기-킬 · 없으면 부적격)

1. **PC-A 발견측**: 기존 planted-block 검정력 게이트(:10667 · bar ×1.5) 를 tap L 의 N/d 에서 통과.
   실패 ⟹ INSTRUMENT-DEAD rc=1 · 판정 미발행.
2. **PC-B 기능측(신규)**: readout-anchored planted faction — 바이트클래스 B 도메인에 대해
   readout 가중 상위 채널군을 '심은 파벌'로 포함한 assignment 의 S 가 자기 null95 를 못 넘으면
   lesion→CE→S 경로가 이 window 수에서 무검정력 ⟹ 판정 미발행 (전체 경로를 아는-방향 효과로 검증).
3. **PC-C 안정성**: 프롬프트 반분 2회 발견 partition 의 일치도(NMI)가 라벨-perm null95 이하면
   잡음을 lesion 하는 것 ⟹ 판정 미발행.

## 사망조건 (사전등록)

- D1: PC-A 실패 → 계기사망(음성 아님). D2: PC-B 실패 → 계기사망. D3: PC-C 실패 → 계기사망.
- **D4(본판정)**: S_disc ≤ null95 (K* 셀) ⟹ 발견블록 = 기능 없는 장식 — 자연-학습-파벌 주장 사망.
- D5: S_disc > null95 그러나 S_contig ≥ S_disc ⟹ index-연속성 교란 미배제 = UNINTERPRETABLE(원인 규명 전 cement 금지).

## ⚠️ 선행 수리 (소유-lane 에도 보고)

origin/main `faction_lesion_run` 은 `real_assign`/`S_real`/`D_real` 를 **계산 없이 사용**
(evaluate.py:11064,11073,11076 — `real_assign = np.repeat(np.arange(K), d//K)[:d]` +
`S_real, D_real = selectivity(real_assign)` 블록 부재) ⟹ 실 ckpt 첫 발사에서 NameError 확정.
이 flag 구현 시 동일 함수를 고치게 되므로 충돌 방지 위해 **소유 세션 합류 후** 수리.

## Honest scope

DIRECTIONAL: lesion 손상은 specialization 의 한 렌즈. '부과된 split 이 훈련으로 특화되는가'는
존재하는 ckpt 로 원리적으로 불가 — 그 절반은 소유-lane 고유(분리 가능한 절반만 여기서 잰다).
