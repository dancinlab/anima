---
id: H_9297
slug: 9297_powered_grounding_probe
title: 검정력을 확보하고 다시 물었다 — 303M 표현에 held-out 극성은 없다 (🧱 INFO-ABSENT EARNED · n=29→91 · bar 1.62σ→2.86σ)
group: g1-crack-natural-emergence 프런티어 · NBIND-G 접지 채널 (H_9296 의 잔여를 닫는 종결 H)
terminal_tier: 🧱 INFO-ABSENT CONFIRMED (EARNED · 2026-07-14 · py 2-production · V-게이트 3/3 PASS · 사전등록 7e6a3c555, 새 dump 開封 前) — **n=29 는 데이터 한계가 아니라 코드 상한이었다**: 인증 bar 를 1바이트도 안 건드리고 같은 450k 를 다시 세니 pos 46 · neg 67 인증 통과인데 `k = min(pos, neg, **15**)` 가 막고 있었다 ⇒ 상한 해제로 held-out **29 → 91**, 동결 bar 0.65 가 **1.62σ → 2.86σ**. 새 62 원자 전부 노출 floor(occ≥30) 통과(최소 103)라 '못 본 원자라 안 읽힌다' 배제. **그 검정력 위에서도 프로브는 우연을 읽는다**: P-LIN main_s7 **0.527** (perm p=0.295 · exact p=0.338) · main_s11 **0.505** (perm p=0.425 · exact p=0.500) · 200회 순열 귀무분포 **미돌파**(null p95 = 0.583/0.604) · 비선형 monitor 도 우연(P-NL 0.505/0.516) · V-REPRO PASS(기존 29 부분집합 0.552 = H_9289 의 0.5517 재현). ⇒ **303M 의 frozen 표현은 held-out 자연 원자의 극성을 인코딩하지 않는다** — '못 찾았다'가 아니라 **'찾을 수 있는 프레임에서 없다'**. H_9289 의 INFO-ABSENT 는 결론이 옳고 근거만 부족했던 것(H_9296 이 NOT-POWERED 로 강등 → 본 H 가 정당한 근거로 **복권**). ⇒ 프런티어 사슬 완성: 오라클(정보 있음·H_9291) + 표현에 없음(EARNED) ⇒ **벽 = 추출 채널** ⇒ **O/C 채널이 옳은 다음 수**. 사전등록 예측(🟡 PARTIAL)은 반증. ⚠️ H_9290(NO-RESCUE)은 여전히 n=29 프레임 ⇒ 재측정 전까지 NOT-POWERED 주의 유지.
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9297_powered_grounding_probe/
terminal_verdict: state/verdicts/9297_powered_grounding_probe/H_9297_RESULT.txt
prereg: state/nbindg_grounding/PREREG_H9297.md (새 hidden dump 開封 前 커밋 7e6a3c555)
date: 2026-07-14
provenance: 로컬 py 2-production (anima-py evaluate --dump-hidden · frozen N2 ckpt 4-arm) · $0 · 재학습 0
---

# H_9297 — 벽이 진짜였다. 다만 그걸 **벌어내는 데** 한 단계가 더 필요했다.

## 배경 — H_9296 의 잔여, 그리고 그 잔여의 진단이 틀렸다

H_9296(#3406)은 NBIND-G 의 G-PROBE 프레임이 **held-out n=29** 위에 있어 동결 bar 0.65 가 우연에서
겨우 **1.62σ** 임을 보였다 ⇒ H_9289 의 INFO-ABSENT(0.5517 = 16/29 · p = 0.356)는 **NOT-POWERED**.
그 H 의 NEXT#1 은 *"n ≥ 100 하려면 더 크거나 다른 도메인의 코퍼스가 필요"* 였다.

**그 진단이 틀렸다.** 인증 bar 를 **1바이트도 안 건드리고** 같은 450k 를 다시 세니:

```
gen_nbindg_n2.py:  k = min(len(pos), len(neg), 15)     ← 코드에 박힌 상한 15/극성
실측 인증 통과:     pos 46 · neg 67                      (purity ≥ 0.85 · occ ≥ 100 · syll ≤ 3
                                                          · non-grid · non-past — 전부 원본)
⇒ 상한 해제:       held-out n = 29/30 → 91              (V-F authored-collision 1 탈락)
```

**노출 검사(사전등록 floor occ 30):** 새로 열린 62 원자 **전부 통과**(최소 103 · 중앙값 175)
⇒ "모델이 못 본 원자라 안 읽힌다" 는 대안 설명이 **구성상 배제**된다.

> **n=29 는 데이터 한계가 아니라 자기가 건 코드 상한이었다.**
> 검정력: 우연 sd 0.0928 → **0.0524** ⇒ 동결 bar 0.65 가 **1.62σ → 2.86σ**

## Method (사전등록 · 새 dump 뜨기 前 커밋 `7e6a3c555`)

**바꾼 것은 원자 수 하나뿐.** frozen ckpt 4 arm · 인증 기준 · K_CTX=24 · WIN=24 · 좌문맥
truncate · **bar 0.65** · split · seed 전부 H_9289 verbatim. `k_cap` 기본값 15 는 보존해
H_9289/H_9296 의 byte-재현성을 지켰다.

두 가지는 **의도적으로 다르고, 둘 다 수리이지 완화가 아니다**:
- **primary = P-LIN 하나** — H_9296 이 "프로브 용량은 범인 아님" 을 이미 보였으므로 4개를 공동
  primary 로 두면 다중검정 표면만 부풀린다. 나머지는 monitor.
- **통제 = 200회 라벨-순열 귀무분포**(백분위 판정) — H_9296 의 ±0.08 밴드는 n=29 에서 **±0.86σ**
  라 우연 셔플이 **39% 확률로 벗어나던** 계측 결함이었다. 반복하지 않는다.

## Result (n=91 · bar = 2.86σ)

| arm | P-LIN (train) | perm-null p95 | perm p | exact p | [mon] P-NL | [V-REPRO] old-29 |
|---|---|---|---|---|---|---|
| **main_s7** | **0.527** (1.00) | 0.583 | **0.295** | 0.338 | 0.505 | **0.552** |
| **main_s11** | **0.505** (1.00) | 0.604 | **0.425** | 0.500 | 0.516 | **0.552** |
| base_only | 0.549 (1.00) | 0.605 | 0.265 | 0.201 | 0.505 | 0.517 |
| shuffle_grid | 0.527 (1.00) | 0.583 | 0.300 | 0.338 | 0.560 | 0.552 |

**V-REPRO PASS** (같은 실행 안에서 기존 29-원자 부분집합 = 0.552 ⇒ H_9289 의 0.5517 재현 ·
파이프라인 동일성 확정) · **V-FIT PASS** (train_fit 전 arm 1.00) · **V-BASE PASS**

⇒ **양 seed 모두 우연에 앉는다.** 200회 순열 귀무분포도 **못 넘는다**. 비선형 monitor 도 우연.

## Verdict — 🧱 INFO-ABSENT CONFIRMED (**EARNED**)

사전등록 결정표 2행. **사전등록 예측(🟡 PARTIAL)은 반증** — 부분 신호조차 없다.

**말하는 것.**
1. **303M 의 frozen 표현은 held-out 자연 원자의 극성을 인코딩하지 않는다.** 이제 이것은
   "못 찾았다" 가 아니라 **"찾을 수 있는 프레임에서 없다"** 이다 — 2.86σ · 순열 null 미돌파 ·
   양 seed · 노출 floor 통과 · 프로브 용량 무죄(H_9296).
2. **H_9289 의 INFO-ABSENT 는 결론이 옳았고 근거만 부족했다.** H_9296 이 NOT-POWERED 로 강등했고,
   본 H 가 **정당한 근거를 벌어 복권**했다.
3. ⇒ **프런티어의 사슬이 온전해졌다:**
   **오라클(정보 있음 · H_9291) + 표현에 없음(EARNED · 본 H) ⇒ 벽 = 추출 채널**
   ⇒ **O/C 채널(확정-금지 abstention objective · 오류-표적 교정 폐루프)이 옳은 다음 수.**
   ARBITRARY-GROUNDING(H_9286)과도 정합 — **정보가 있는데도 모델은 멋대로 정했다.**

**말하지 않는 것.**
- "303M 이 이 정보를 **배울 수 없다**" 가 아니다 — **이 학습 레시피(N2)로는 인코딩 안 됐다** 는
  사실이다. objective/커리큘럼을 바꾸면 달라질 수 있고, **그것이 바로 O/C 채널 가설**이다.
- scope: 한국어 감성 극성 · 좌문맥 64byte · frozen 표현 판독(비선형 monitor 도 우연).

## ⚠️ 부수 — H_9290 의 검정력 주의는 아직 살아 있다

H_9290(NAT-ATOM NO-RESCUE)은 여전히 **같은 n=29 프레임**을 쓴다. 본 H 가 그 상한이 코드였음을
밝혔으므로 **n=91 로 재측정 가능**하다($0 · 같은 절차 · codec ckpt 필요). 그 재측정 전까지
H_9290 의 NO-RESCUE 는 **NOT-POWERED 주의**를 유지한다.

## Cross-links

H_9296 (NOT-POWERED 진단 — 본 H 가 그 잔여를 닫음) · H_9289 (INFO-ABSENT — 본 H 가 **복권**) ·
H_9291 (오라클: 정보 존재 · 사슬의 나머지 절반) · H_9286 (ARBITRARY-GROUNDING · 정합) ·
H_9290 (같은 n=29 프레임 · 재측정 대상) · `negative-claims-need-tost-not-ns` ·
`power-before-negative-verdict` · `probe-defect-census-max-control-bias` · `a_eval_py_canonical` ·
c9 · c16 · p7
