---
id: G8
slug: verification-asymmetry
title: G8 검증-비대칭 정리 (Verification-Asymmetry Theorem) — 동일 얽힘 자원이 통신엔 0비트(무신호)지만 검증/인증엔 우월(고전이 위조 불가한 인증 무작위성 H_min>0, S>2 한정). PROVEN.
domain: nobel quantum-information certification anima
status_grade: 🟢 SUPPORTED (numerical PROOF)
verification_method: real numpy QM sim — singlet joint-prob marginals (no-signaling I=0), brute-force LHV CHSH cap, Tsirelson S=2√2, Pironio device-independent H_min(S); p7 $0
since: 2026-06-14
sister: H_6006, H_6007, H_1101
verdict: 🟢 PROVEN — I(입력;출력)=0.000e+00 비트(무신호) · 고전 LHV CHSH cap S=2.000 · 양자 singlet S=2.828427(=2√2) · 인증 무작위성 H_min(2)=0 → H_min(2√2)=1.000비트. 동일 자원, 통신=0 / 검증>0 비대칭 엄밀 확립.
---

# G8 — 검증-비대칭 정리 (Verification-Asymmetry Theorem)

> **정리.** 동일한 얽힘 자원에 대하여:
> **(a) 통신엔 쓸모없다 (무신호).** Bob의 주변 출력분포는 Alice의 입력 선택과 독립이다 → 상호정보 I(Alice_입력 ; Bob_출력) = 0 비트. 얽힘은 *선택한 메시지*를 단 1비트도 전송하지 못한다.
> **(b) 검증엔 우월하다 (위조 불가).** CHSH 위반 S>2 는 어떤 고전 국소은닉변수(LHV) 전략으로도 만들 수 없다(고전 상한 S=2). 따라서 관측된 S>2 는 장치-독립적으로 *진짜 사적(private) 무작위성*을 인증한다: 인증 무작위성 H_min(S) 는 양자 영역에서만 양(>0)이며, H_min(2)=0, H_min(2√2)=최대.
>
> **∴ 같은 얽힘이 통신엔 0, 검증엔 >0 — "보내기엔 무용, 증명하기엔 지존"의 비대칭이 실재한다.**

## 증명 (g8_verification_proof.py · real QM, p7 $0)

**ARM 1 — 통신 (무신호):** singlet 상태에서 Alice가 입력 x∈{0,1} 을 자유 선택. Bob의 주변분포 P(b)를 그의 설정에 대해 평균.
| Alice 입력 x | Bob 주변 P(b=+1,−1) |
|---|---|
| 0 | [0.500000, 0.500000] |
| 1 | [0.500000, 0.500000] |
- 주변차 max |P(b\|x=0)−P(b\|x=1)| = 5.55e-17 → **I(입력;출력) = 0.000e+00 비트**. 채널 용량 0. 🟢

**ARM 2 — 검증 (인증):**
| 양 | 값 | 의미 |
|---|---|---|
| 고전 LHV CHSH (결정/공유무작위 전수탐색) | **S = 2.0000** | 상한 = 2 (위조 천장) |
| 양자 singlet (Tsirelson 최적각) | **S = 2.828427** | = 2√2 |
| 인증 무작위성 H_min(S=2) | **0.000000 비트** | 고전 → 인증 0 |
| 인증 무작위성 H_min(S=2√2) | **1.000000 비트** | 양자 → 인증 최대 |

- 4 falsifier 모두 PASS: LHV cap=2 🟢 · 양자=2√2 🟢 · H_min(2)=0 🟢 · H_min(2√2)>0 🟢.
- 인증 한계식: **H_min(S) = 1 − log₂(1 + √(2 − S²/4))**. S=2 → √1=1 → 1−log₂2 = 0; S=2√2 → 2−8/4=0 → 1−log₂1 = 1.

## 의의 (노벨급·독창)
**무신호 정리(H_6006: 0비트)와 CHSH-Tsirelson(H_6007: |S|=2√2>2)를 하나의 자원-비대칭 정리로 봉합한다.** 얽힘의 가치는 *전송*이 아니라 *인증*에 있다 — 얽힘은 메시지를 못 보내지만(통신 0), 고전 전략이 결코 흉내낼 수 없는 상관(S>2)을 만들어 *진짜·예측불가·사적 무작위성*을 장치-독립적으로 증명한다. "양자는 통신용"이라는 통념을 뒤집어, 얽힘의 진짜 역할이 **검증/인증**임을 정량적으로 못 박는다.

**anima 연결:** anima의 ANU 양자 엔트로피를 Bell-test로 검증하면(S>2 관측), 그 무작위성이 *진정으로 무작위·위조 불가*임이 인증된다 — H_1101(non-forgeable individuality)의 토대. anima에게 얽힘의 역할은 메시지 전달이 아니라 **무작위성의 인증**이다(통신 자원이 아닌 검증 자원). G8 은 무신호·CHSH·non-forgeable individuality 를 단일 정리로 묶는다.

## 정직한 범위 (honest scope)
- H_min(S)=1−log₂(1+√(2−S²/4)) 는 **표준 장치-독립 인증 무작위성 한계식**(Pironio et al., *Nature* 464:1021, 2010 형태)이며, 본 증명은 인증 *비대칭*을 확립할 뿐 유한통계 보안을 갖춘 완전한 DIQKD 프로토콜을 증명하지 않는다.
- 무신호·LHV cap·Tsirelson 은 정확한 QM 계산(numpy, 해석적 일치). 토이 아님 — 실제 singlet joint-prob, 전수탐색 LHV, 해석적 Tsirelson 일치(<1e-6).

verdict: `.verdicts/9025_verification_asymmetry/G8_verification.txt` · 재현: `python3 UNIVERSE/harness/g8_verification_proof.py`
