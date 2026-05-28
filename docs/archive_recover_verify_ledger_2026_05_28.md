# archive-recover 가설 전체재검증 ledger (2026-05-28)

회수(PR #1326) 177 가설 + audit(PR #1328) 후, T1(verdict-claim 보유 58개)을
`hexa verify` 로 재검증. g5 — verdict verbatim은 `.verdicts/archive-recover-186/`.

## 1. 검증 요약

| 군 | 수 | tier | 근거 |
|---|---|---|---|
| n=6/완전수 약수함수 atom | 12 claim (16 fn·n) | 🔵 SUPPORTED-FORMAL | hexa-native closed-form 재현 |
| 레거시 텍스트 오기 | 2 | 🔴 FALSIFIED | calc 결정적 불일치 |
| Jordan totient J₂ | 1+ | 🟠 INSUFFICIENT | 계산기 calc-path 부재 |
| 비산술 T1 (Φ·EEG·SFT·meta) | 41 | 🟠 DEFERRED | closed-form 없음, run/external 의존 |
| n=6 → 차원 매핑 uniqueness | — | 🔴 CLOSED (H_153 L7) | perfect-number class 포화 |

## 2. 🔵 SUPPORTED-FORMAL — 약수함수 substrate (12)

n=6 군집(H_153·154·156·158·159·160·176)의 산술 substrate는 전부 재현됨.

| claim | calc | tier |
|---|---|---|
| τ(6)=4 · σ(6)=12 · φ(6)=2 · μ(6)=1 · sopfr(6)=5 | 일치 | 🔵 |
| τ(28)=6 · σ(28)=56 · φ(28)=12 · sopfr(28)=11 | 일치 | 🔵 |
| τ(496)=10 · σ(496)=992 · τ(8128)=14 | 일치 | 🔵 |

→ **산술 substrate는 진짜.** 단 이는 "정수론적 사실"이지 "물리적 차원 = 약수 수"
라는 매핑의 증명이 아님 (§4).

## 3. 🔴 FALSIFIED — 레거시 텍스트 오기 (2)

legacy 파일 본문에 잘못 전사된 값 (J₂ 중간값·오타로 추정).

| claim | calc | tier |
|---|---|---|
| φ(6)=6 | 2 ≠ 6 | 🔴 FALSIFIED |
| sopfr(28)=9 | 11 ≠ 9 | 🔴 FALSIFIED |

→ 가설 본문에 오기 잔존. 회수 시 byte-equal cp 보존 정책상 그대로 들어옴 — 정정 필요.

## 4. 🔴 CLOSED — n=6 차원 매핑 uniqueness (H_153 L7 재확인)

H_153 "τ(6)=4 → 4D Minkowski, n=6 함수가 물리적 차원 generate" 의 핵심:

- **산술**: 🔵 (§2) — τ(6)=4, σ(6)=12 등 모두 사실
- **uniqueness 주장** ("n=6 만이 특별"): 🔴 **CLOSED** — H_153 L7 binding 이미 명시:
  depth-4 formula search 에서 perfect-number class {6,28,496,8128} 가 22/22 동률
  포화, n=6 단독 특별성은 공식 반증
- **매핑 자체** ("약수 4개 = 4차원"): 🟠 INSUFFICIENT — divisor count → spacetime
  dimension 은 해석적 bridge, calc-path 없음

## 5. 🟠 DEFERRED — 비산술 T1 (41)

closed-form 부재 → 실제 run / sim / 외부 데이터 의존. 현 상태 verify 불가.

| 묶음 | 대표 H | 필요 자원 |
|---|---|---|
| LLM 학습 패러다임 | H_093~H_104 (SFT·DPO·curriculum·instruction-tune) | 학습 run |
| Φ 측정 / IIT | H_024·H_162·H_165·H_178·H_179·H_180 | IIT sim |
| ANIMA-VOICE | H_154·H_172 | 음성 합성 run |
| meta-cluster (V8 등) | H_182~H_191 | 하위 H 집계 선행 |
| 임상 Φ 상관 | H_188 (PCI Massimini) | 외부 데이터 |

## 6. 결론

- **터미널 verdict 확보**: 🔵 12 (약수함수) + 🔴 2 (오기) + 🔴 CLOSED 1 (uniqueness) = 15
- **active 등록 자격**: 약수함수 atom은 atlas에 이미 존재(idempotent) — 신규 가치 낮음.
  n=6 차원 가설은 **uniqueness 반증(L7)** 이 핵심 finding → negative-result paper 후보
  (a_paper_negative_ok)
- **잔여 41 + _pointers 114**: run/보강 전까지 🟠, active 캠페인 deferred

## 7. 다음 후보

1. 오기 2건(φ(6)=6, sopfr(28)=9) 본문 정정 PR
2. n=6 uniqueness 반증 → `/paper` negative-result (L7 + perfect-number class 포화)
3. 비산술 41 중 학습 패러다임군 → 실제 fire (cost-bearing)
