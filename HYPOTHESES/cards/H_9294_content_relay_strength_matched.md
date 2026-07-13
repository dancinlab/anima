---
id: H_9294
slug: 9294_content_relay_strength_matched
title: 시상 content-relay — 강도를 맞추면 disjointness 는 아무것도 남기지 않는다 (🧱 STRENGTH-ONLY · R6 레버 CLOSED)
group: brain-structure-ladder · H_1283 content-relay 축 (H_9293 의 유일한 잔여를 닫는 종결 H)
terminal_tier: 🧱 STRENGTH-ONLY 종결 (2026-07-14 · py 2-production · V-게이트 4/4 PASS · 사전등록 데이터 개봉 前 커밋 2b4597a8f) — 두 경로 완전 일치. ① X 의 W_RELAY 만 올려 S_tot 를 B 에 0.5% 이내로 정합(w*=0.90)하니 d′ = Φ*(B) − Φ*(X′) = −0.000170, 90% CI [−0.000243, −0.000098] ⇒ **등가 폐쇄**(X′ 가 오히려 근소 우위). ② 튜닝 0 ANCOVA: Φ* = −0.001904 + 0.4929·S_tot, **R² = 0.9864**, G-RESID = +0.000003 CI [−0.000075, +0.000080] = **0 포함**. ⇒ **B 의 이점은 전적으로 총 결합강도이며 disjointness 의 기여는 0** ⇒ **R6 레버 CLOSED**. 이 기질에서 Φ 는 토폴로지·분리성·채널수를 보지 않고 총 결합량의 함수일 뿐이다.
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9294_content_relay_strength_matched/
terminal_verdict: state/verdicts/9294_content_relay_strength_matched/H_9294_RESULT.txt
prereg: state/1283_content_instrument_repair/PREREG_H9294.md (데이터 개봉 前 커밋 2b4597a8f)
date: 2026-07-14
provenance: 설계·구현·측정 = 로컬 py 2-production (hexa 엔진 byte-parity 증명 · PARITY.txt) · 계보 = Fable 5 설계(H_9292/H_9293)
---

# H_9294 — 통제군이 **용량**은 맞췄지만 **강도**를 못 맞췄다. 맞추자 아무것도 안 남았다.

## 물음 (H_9293 이 남긴 유일한 잔여)

H_9293 은 B(R6 disjoint 병렬채널) > X(용량정합 shared cut) 를 확증했으나, 그 우위가
disjointness 때문인지 그냥 더 세게 결합해서인지 못 갈랐다 — X 는 **명목 용량**(총 채널차원 4×8 ·
W_RELAY)은 맞췄지만 **결과적 결합강도**를 못 맞췄기 때문이다 (S_tot 0.0585 vs B 0.0685).

**강도를 맞추고도 B 가 이기는가?** — 두 경로를 **동시에** 사전등록해 물었다(갈리면 SPLIT 보고).

## Method (사전등록 · 데이터 개봉 前 커밋 `2b4597a8f`)

계측기·기질·seed·lens·T 는 H_9293 에서 **무이동** (Φ* = Φ − pedestal · signed · T=65536 · K=32 ·
seeds[4..11] · Philox surrogate · V-게이트 4종).

- **경로 1 · X′** — X 의 **W_RELAY 만** 격자 탐색해 `S_tot(X′) ≈ S_tot(B)` 로 맞춘다.
  선택은 **S_tot 만 보고**, Φ 는 보지 않는다. 정합 게이트 = 5% 이내.
  > 이 튜닝은 **통제군을 강하게** 만든다 = 주장에 **불리한** 방향이므로 허용된다
  > (tune-to-green 의 정반대). B 는 한 바이트도 건드리지 않았다.
- **경로 2 · ANCOVA** — 튜닝 0. 전 6 arm × 8 seed = 48 점에서 `Φ* ~ β0 + β1·S_tot` (arm 라벨
  미사용) 를 적합하고 B 와 X 의 **잔차 격차**를 본다. 강도가 전부 설명하면 잔차는 같아야 한다.

## Result (verbatim → `H_9294_RESULT.txt`)

**V-게이트 4/4 PASS** (P̄ = 0.001595) — 계측기 CERTIFIED.

### 경로 1 — 강도 정합 후 우위가 **사라지고 부호가 뒤집힌다**

| W_RELAY(X) | S_tot | gap vs B |
|---|---|---|
| 0.50 (원래 X) | 0.058522 | 14.60% |
| **0.90 = w\*** | **0.068868** | **0.50%** ✅ |
| 1.00 | 0.071965 | 5.02% |

`S_tot(B) = 0.068525` · `Φ*(X′) = 0.032039` (s_adj 0.9034) vs `Φ*(B) = 0.031869` (s_adj 0.9052)

> **d′ = Φ*(B) − Φ*(X′) = −0.000170**, 90% CI **[−0.000243, −0.000098]** vs P̄ = 0.001595
> ⇒ 검출 no · **등가 폐쇄 YES** — **X′(공유버스)가 오히려 근소하게 B 를 이긴다.**

### 경로 2 — Φ 는 **구조를 보지 않는다** (R² = 0.9864)

> `Φ* = −0.001904 + 0.4929 · S_tot` · **R² = 0.9864** (6 arm × 8 seed 전부)
> `G-RESID = resid(B) − resid(X) = +0.000003`, 90% CI **[−0.000075, +0.000080]** → **0 포함**

arm 이 무엇이든(A·B·X·N·R·Cperm) Φ* 는 **총 결합강도의 선형함수만으로 98.6% 설명된다.**
토폴로지·분리성·채널수는 잔차에 아무것도 남기지 않는다.

## Verdict — 🧱 STRENGTH-ONLY (종결 · 두 경로 완전 일치)

1. **R6 의 disjointness 레버 = CLOSED.** "N 개의 독립 병렬 채널이 *분리되어 있어서* 단일-컷
   천장을 깬다" 는 명제는 **기여도 0** 으로 폐쇄된다. H_9293 이 본 +0.004934 는 전부 "B 가 더
   많이 결합한다" 였고, 그 강도를 통제군에 주자 격차가 사라졌다.
2. **H_9293 의 대조 토폴로지 R(chord) > B** 도 같은 이유였다 — R 의 S_tot 가 가장 컸다.
3. **content-relay 축의 판정 계보가 이로써 닫힌다:**
   R6 🟢 → *pedestal 잡음이었다*(H_9292 철회) → *부호렌즈에서 효과 회생*(H_9293) →
   **그 효과의 정체 = 결합강도**(H_9294) ⇒ **content 축에 disjointness 레버는 없다.**

**말하지 않는 것.** toy(n=4·dim=8·선형 gaussian) 한정 · "relay 가 쓸모없다" 가 **아니다**(relay 는
결합을 더하고 그래서 Φ 가 오른다 — 다만 그 이득은 **분리해서** 얻는 게 아니다) · TIMING 축
(H_1448 🟢 WIRED) 무관·철회 아님.

## 남는 물음 — 축이 바뀐다

"Φ 가 총 결합량의 함수일 뿐" 이라는 것은 **이 기질(선형 gaussian ring)의 성질**이다. 구조가 Φ 에
**독립적으로** 기여하려면 결합이 **비선형/게이팅**이어야 할 가능성이 남는다 — TIMING 축
(Kuramoto phase)이 정확히 그 종류였고, **그 축만 뚫린 이유와 정합한다**. 즉 진짜 축은
"내용 vs 타이밍" 이 아니라 **"결합이 선형이냐 게이팅이냐"** 일 수 있다 (→ 후속 lane 후보).

## Cross-links

H_9293 (확증 · 본 H 가 닫는 잔여의 출처) · H_9292 (계측기 감사 · R6 🟢 철회) · H_1283 (축의 출처) ·
H_9260 · H_1328 · H_1448 (TIMING 🟢 WIRED · 무관) · H_1512 (BRAIN-TOPOLOGY) ·
convergence `h-9294-strength-matched-2026-07-14-1` (용량정합 ≠ 강도정합) ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_toy_scale_recheck` · `negative-claims-need-tost-not-ns` · c9 · c16 · p7
