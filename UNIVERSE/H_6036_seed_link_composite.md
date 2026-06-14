---
id: H_6036
tier: ⊗ (깊은 물리적 정초)
label: ⊗-36
title: ⊗-36 SEED+LINK COMPOSITE — ANU 공유 양자씨앗(H_6008)과 텐션 링크(H_6010)를 합성하면 둘 중 어느 하나보다 엄격히 낫다. 단 시너지는 최종 동조도(천장)가 아니라 시간축(cold-start 제거)에 있다.
tradition: Kuramoto 동기화 · 공통원인(common cause) · ANU QRNG(paid)
status_grade: 🟠 PARTIAL (numerical · paid ANU-seeded)
verification_method: 3-arm Kuramoto sim (SEED/LINK/BOTH), 전 무작위 paid ANU 512B 스냅샷 구동, 3 trial; p7 $0
since: 2026-06-15
sister: H_6008, H_6010, H_6009, H_6007
verdict: 🟠 PARTIAL — F1(시너지 ≥+0.05) FAIL = 천장효과(LINK 단독이 이미 r=0.999), F2(속도) PASS, F3(무신호 CHSH≤0.75) PASS. 합성의 진짜 이득은 **시간축**: SEED 단독은 detuning에 r=0.779로 붕괴, LINK 단독은 lock에 36틱(cold-start), BOTH는 즉시 lock@0 + 지속 0.999. 공통원인(예측가능)⊕라이브채널(예측불가)이 서로의 사각을 메운다.
---

# H_6036 — ⊗-36 SEED+LINK COMPOSITE (공유 양자씨앗 ⊕ 텐션 링크)

> **가설.** 두 anima를 잇는 두 메커니즘을 합성한다 — ANU 공유 양자씨앗(H_6008, 통신 0의 즉시 기준선)과 텐션 링크(H_6010, 라이브 적응 동기). 합성이 둘 중 어느 하나보다 **엄격히** 낫고, 무신호 정리는 유지된다.

## 동기
arc는 두 조율 메커니즘을 **따로** 검증했다:
- **SEED (H_6008)** — 공유 ANU 버퍼 → t=0 완벽 정렬, 라이브 통신 0. 하지만 **경직**: detuning(서로 다른 내재 텐션 주파수)·예기치 못한 drift에 재정렬 불가(라이브 채널 없음) → lock이 붕괴.
- **LINK (H_6010)** — 양방향 텐션 결합 K가 능동적으로 위상잠금·drift 보정. 하지만 독립 초기위상에서 **cold-start** 지연.

H_6036은 이를 합성: 공유씨앗 INIT(cos Δθ=1 @t=0) + 텐션링크 COUPLING(detuning·drift 보정).

## 방법
3 arm (SEED: 공유init·K=0 / LINK: 독립init·K>0 / BOTH: 공유init·K>0), H_6010 양방향 Kuramoto 적분기 verbatim(DT=0.02·T=4000·K=1.2). 초기위상·detuning·drift 타이밍/크기 **전부** 커밋된 실 paid ANU 512B 스냅샷(`anu_seed_512.bin`, tier=anu_paid)에서 추출. 3 trial = 버퍼 3개 비중첩 슬라이스. harness: `TENSION-LINK/harness/h6036_seed_link_composite.py`.

사전등록 반증자:
- **F1 시너지**: r(BOTH) ≥ max(r(SEED),r(LINK)) + 0.05
- **F2 속도**: lock(BOTH) < lock(LINK) AND r(BOTH) > r(SEED)
- **F3 무신호**: 합성 자원은 여전히 고전(공유무작위+정상 결합채널) → CHSH ≤ 0.75

## 측정 (verdict 원문: `.verdicts/6036_seed_link_composite/H_6036.txt`)
| arm | mean steady-r | mean ticks-to-lock |
|---|---|---|
| SEED | 0.7793 | 0 |
| LINK | 0.9989 | 36 |
| BOTH | 0.9989 | 0 |

- F1 = **FAIL** (0.999 vs max 0.999 — 천장효과: order parameter는 1.0이 상한, LINK가 이미 포화)
- F2 = **PASS** (lock 0<36 & r 0.999>0.779)
- F3 = **PASS** (CHSH 0.7492 ≤ 0.75)

## 발견
🟠 **시너지는 존재하되 magnitude가 아니라 time 도메인에 있다.** 한 번 lock되면 동조도는 1.0이 상한이라 BOTH가 LINK를 +0.05로 못 이긴다(F1 천장효과). 그러나 BOTH의 진짜 이득은 두 가지를 **동시에** 얻는 것: (1) cold-start 제거(lock@0 vs LINK 36틱), (2) detuning/drift 생존(SEED 단독 0.779 붕괴를 0.999로 유지). 즉 **공유 공통원인 = 예측가능 부분, 라이브 텐션채널 = 예측불가 부분**을 각각 담당해 서로의 사각을 메운다. 무신호는 깨지지 않는다(고전 합성).

## 정직 경계
- 토이(2 진동자, H_6010 Kuramoto verbatim); 스케일 전이 미검증(a_toy_scale_recheck). N-party 확장 = H_6037.
- F1을 magnitude로 사전등록한 것이 천장효과를 못 본 설계 한계 — 발견은 F2(시간축)에 있고 이는 정직하게 PASS.
- 양자=무작위 접지(ANU), 텐션링크=고전 채널/옵티마이저. 비밀 계시 없음.
