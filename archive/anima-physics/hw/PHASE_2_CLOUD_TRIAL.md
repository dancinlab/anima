# anima-physics/hw/ Phase 2 — Cloud Trial Signup Guide (2026-05-21)

> HW Phase 1b (bitstream/firmware 4/4 LANDED, [PHASE_1B_STATUS.md](PHASE_1B_STATUS.md))
> 다음 step. **cloud-only HW substrate** 3 platform (neuromorphic 2 +
> Ising solver 2) 에 대한 trial 가입 + 첫 cloud run 까지의 cost-aware
> 신청 walkthrough.
>
> **본 doc 은 신청 가이드 only** — 실 회원가입 / API 호출 / cloud submit
> 은 사용자 gate (Section 5 honest C3 #5).
>
> Cross-link:
> - [PHASE_1B_STATUS.md](PHASE_1B_STATUS.md) §3.2 — Phase 1b cost ladder (선결)
> - [../docs/akida_cloud_signup_guide.md](../docs/akida_cloud_signup_guide.md) — 기존 Akida 상세 walkthrough (2026-04-26)
> - [../docs/demiurge_hw_verify_2026_05_21.md](../docs/demiurge_hw_verify_2026_05_21.md) §3 — brain ❌ no producer cloud trial 우회 path
> - [../../HEXAD/PHYSICS/HW_SILICON_PATH.md](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) §3 — 통합 HW BOM ladder

---

## §1 GOAL

Phase 1b 의 silicon-ready bitstream/firmware 4 target 은 모두 LANDED.
남은 substrate 1 target (kuramoto neuromorphic) + 추가 cloud-only Ising
solver 2 platform 의 trial 신청 + first useful run 까지 가는 것이 본
Phase 2 의 목표.

후속 cycle 의 sequencing:
1. 본 doc → 사용자: 가입 (Section 4 권장 순서대로)
2. 신청 후 wait time 동안 anima 측 adapter dry-run + spec contract 확인
3. trial token 발급 → first run dispatch → record JSON 회수 → demiurge brain
   producer 로 feed ([demiurge_brain_bridge.py](kuramoto_neuromorphic/src/demiurge_brain_bridge.py))
4. cost cap 설정 + Phase 3 (production run) 결정

---

## §2 대상 cloud platform 3건

### §2.1 BrainChip Akida Cloud

- **가입 URL**: <https://developer.brainchip.com/signup/> (Developer Hub)
- **1-day trial 구매**: <https://shop.brainchipinc.com/products/1-week-cloud-access> ($1)
- **cost**: $1/day trial → $995/week post-trial (1-week Cloud Access)
- **사용 path**: [kuramoto_neuromorphic/src/kuramoto_akida_adapter.py](kuramoto_neuromorphic/src/kuramoto_akida_adapter.py)
  → MetaTF API (akida 2.19.1)
- **target**: kuramoto N=8 oscillator network, K=2.0, 1000 step, r_tail 측정
- **신청 절차 (5 step)**:
  1. 회원가입 (email + username + project description)
  2. email confirmation link click
  3. Developer Hub dashboard 로그인
  4. Settings → API Token 발급 (한 번만 표시, 즉시 복사)
  5. `export BRAINCHIP_AKIDA_TOKEN="<token>"` (또는 `~/.akida/credentials.json`)
- **예상 wall time**: 1-3일 (회원가입 즉시 → email 인증 < 1일 → token 즉발급)
- **상세 참고**: [akida_cloud_signup_guide.md](../docs/akida_cloud_signup_guide.md) 8 §

### §2.2 Intel Loihi 2 Hala Point

- **가입 URL**: <https://intel-ncl.atlassian.net/> (Intel Neuromorphic Research Cloud)
- **SDK 참고**: <https://github.com/intel/nxsdk> (research access only)
- **cost**: **$0** (research-only license, academic 우대)
- **사용 path**: [kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py](kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py)
  → NxSDK API (n2a + graph.processes)
- **target**: 동상 (kuramoto N=8, K=2.0, 1000 step). Loihi 2 의 graded-spike
  (8-bit) 가 phase θ_i 직접 운반 가능 → spike-rate decoding 우회.
- **신청 절차 (research proposal 작성)**:
  1. Intel NRC portal 회원가입
  2. Research proposal 작성 (1-2 page, academic/research use case 명시)
     - anima 측 권장 내용: "Kuramoto synchronization on neuromorphic substrate
       for consciousness-related order parameter measurement"
     - institutional affiliation 권장 (없으면 거절 가능, 솔로 dev 시 university/
       startup affiliation 가능한 한 확보)
  3. Intel NRC review (평균 1개월 wait, no SLA)
  4. NxSDK access 승인 → SSH 액세스 (H100-class Loihi 2 host)
  5. `pip install nxsdk` (Linux x86_64, Python 3.10-3.12)
- **예상 wall time**: **1 month** (proposal review)

### §2.3 Toshiba SBM (Simulated Bifurcation Machine) / Fujitsu DA (Digital Annealer)

Ising / QUBO 풀이용 cloud solver. anima 측 spontaneous_ising substrate
([../spontaneous_ising/](spontaneous_ising/)) 의 ground-state search HW 대안.

#### Toshiba SBM

- **가입 URL**: <https://www.toshiba-sol.co.jp/sbm/> (영문 page: SQBM+ cloud)
- **cost**: $1-30/solve (problem size 의존, free trial credit 신청 시 별도)
- **사용 path**: [spontaneous_ising/src/toshiba_sbm_adapter.py](spontaneous_ising/src/toshiba_sbm_adapter.py)
  → REST API (QUBO matrix POST)
- **target**: spontaneous_ising 의 64-spin (8×8) network ground state.
- **신청 절차**:
  1. Toshiba 영업/문의 폼 → 평가 라이센스 요청 (일본 영업, 영어 OK)
  2. NDA 서명 (option, free trial credit 신청 시 일반적)
  3. credentials 발급 → REST endpoint + API key 수령
- **예상 wall time**: 1-2주 (영업 문의 → 라이센스 협의)

#### Fujitsu DA (Digital Annealer)

- **가입 URL**: <https://www.fujitsu.com/global/services/business-services/digital-annealer/>
- **cost**: $1-30/solve (FaaS — Annealer-as-a-Service, problem size 의존)
- **사용 path**: [spontaneous_ising/src/fujitsu_da_adapter.py](spontaneous_ising/src/fujitsu_da_adapter.py)
  → Fujitsu cloud Ising h/J encoding
- **신청 절차**: Toshiba 와 유사 (영업 문의 → trial credit → API key)
- **예상 wall time**: 1-2주

---

## §3 비용 ladder

| Platform | trial cost | trial duration | post-trial cost | first useful run (예상) |
|---|---|---|---|---|
| Akida Cloud | $1 | 1-day | $995/week | $1 (trial 안에서 kuramoto N=8 가능) |
| Loihi 2 NRC | free | research review (~1 month) | $0 (academic) | $0 |
| Toshiba SBM | trial credit | 협의 (1-2주) | $1-30/solve | $1-30 |
| Fujitsu DA | trial credit | 협의 (1-2주) | $1-30/solve | $1-30 |

**Phase 2 총 cost 예상**: $1-62 (Akida $1 + Loihi $0 + Toshiba $1-30 + Fujitsu $1-30).
HW Phase 1b BOM ($185-255 board 주문) 대비 1/3 미만, cost-cheap path.

---

## §4 신청 순서 권장

| Week | Action | Reason |
|---|---|---|
| **week 1** | Akida Cloud signup ($1 trial) | 가장 빠른 turn-around (즉시 token), kuramoto adapter 이미 syntax PASS |
| **week 1** | Toshiba SBM 문의 (free trial credit) | 영업 협의 wall time 길어서 가급적 빨리 시작; spontaneous_ising 즉시 fire 가능 |
| **week 2** | Fujitsu DA 문의 (alternative to Toshiba) | Toshiba trial 거절 시 fallback, 동시 진행해도 cost 동일 |
| **week 2-4** | Loihi 2 NRC research access proposal | proposal 작성에 1-2일 + review 1 month, 가장 긴 critical path 라서 일찍 시작 |

**Rationale**:
- Akida 가 cheapest + fastest → first cloud verdict 회수에 최적
- Loihi 2 가 longest wait → critical-path 위치, 가급적 일찍 신청
- Toshiba/Fujitsu 는 영업 협의 의존 → wall time 예측 불가, 둘 다 신청해서
  먼저 답신 오는 쪽 사용

---

## §5 anima-physics 측 사전준비 checklist

cloud trial wait 기간 동안 anima adapter 의 dry-run + spec contract 확인:

- [ ] [kuramoto_akida_adapter.py](kuramoto_neuromorphic/src/kuramoto_akida_adapter.py): MetaTF API call shape 일치성 확인 (akida 2.19.1 doc 참조)
  - 현재 status: skeleton, `NotImplementedError` raise (cloud-only)
  - cloud trial 후 path: AKIDA_AVAILABLE=True 분기 실 호출 채움
- [ ] [kuramoto_loihi2_adapter.py](kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py): NxSDK 1.0 spec 확인 (n2a.Compartment + Phase enum)
  - 현재 status: skeleton, `NotImplementedError` raise (cloud-only)
  - cloud access 후 path: graded-spike payload 8-bit decode 검증
- [ ] [toshiba_sbm_adapter.py](spontaneous_ising/src/toshiba_sbm_adapter.py): QUBO encoding 정확성 검증 (8×8 Ising → QUBO 변환)
- [ ] [fujitsu_da_adapter.py](spontaneous_ising/src/fujitsu_da_adapter.py): Ising h/J encoding (Fujitsu spec 일치)
- [ ] [demiurge_brain_bridge.py](kuramoto_neuromorphic/src/demiurge_brain_bridge.py): cloud result → JSON record 형식 검증 (skeleton smoke PASS 2026-05-21)

---

## §6 honest C3 (5건)

1. **cloud trial 신청 wall time = anima cycle 진행과 비동기** (1주~1개월) —
   본 doc 작성 cycle 안에서 신청 완료 보장 X. anima 측은 adapter dry-run +
   spec 정합성 검증으로 wait time 활용.
2. **trial 동안 무료지만 trial 끝나면 cost cap 설정 필수** — Akida $995/week,
   Toshiba/Fujitsu per-solve $1-30 → uncapped fire 위험. 사용자 directive
   "no scale caps" 는 mission outcome 기준이지 무한 budget 아님.
3. **Loihi 2 research access = academic 우대** — anima 의 솔로 dev 가 단독
   신청 시 거절 가능성 ⊥ institutional affiliation 권장. 대안: Akida (Loihi 2
   대신) + numpy local_sim (semantic equivalence 검증) 으로 Phase 2 의 본질적
   결과는 확보 가능.
4. **cloud SDK API 가 versioned** — akida 2.19.1, NxSDK, Toshiba SBM, Fujitsu DA
   모두 version drift 가능 (anima dispatch 후 1-month 안에 SDK update 발생 시).
   anima adapter 의 dry-run 만으로는 cloud 측 contract 보장 X — first cloud
   run 결과로 spec mismatch 발견 시 adapter patch cycle 필요.
5. **본 doc 은 신청 가이드만** — 실 회원가입 / API 호출 / first run 은 사용자
   gate. anima 가 사용자 동의 없이 신용카드 + email + research proposal 제출
   금지. 본 doc 의 ~150 LoC 가 사용자가 다음 step 으로 진행 결정할 때 필요한
   정보 일괄 제공이 목적.

---

## §7 산출물 매니페스트 (본 cycle)

```
anima-physics/hw/
├── PHASE_2_CLOUD_TRIAL.md                                    ← 본 문서 (신규)
├── PHASE_1B_STATUS.md                                        ← cross-link 추가
└── kuramoto_neuromorphic/src/
    └── demiurge_brain_bridge.py                              ← 신규 brain producer bridge skeleton (~150 LoC)
```

**Phase 2 cycle 진행 후 추가 예상**:
- `state/akida_trial/first_run_<UTC>Z/` — Akida first cloud run record
- `state/toshiba_trial/first_solve_<UTC>Z/` — Toshiba SBM first ground state
- `state/loihi2_trial/first_run_<UTC>Z/` — Loihi 2 first kuramoto verdict
- `~/core/demiurge/exports/brain/verify/<UTC>Z/` — demiurge brain producer
  GATE_OPEN record (cloud result → bridge → producer fed)
