# AURA A7 — per-region big-Φ 분리측정 (IIT4 n≤8 exact 준수)

> AURA relocate-N1 명제(A6)를 **16채널 전뇌**로 확장할 때 부딪히는 IIT4 계산한계와, 그것을 정직하게 우회하는 **region 분리측정** 전략을 in-silico 로 1차 검증한다.
> honest: 아래 region 배정·connectivity 는 **synthetic** — 실제 N1/EEG 측정 아님 (`feedback_toy_scale_transfer`). 실제 region mask 는 electrode montage(채널↔region 매핑)가 필요하다.

---

## 1. n≤8 exact 제약 (왜 16채널을 통째로 못 재나)

IIT4 big-Φ 는 **state-by-node TPM** 위에서 모든 분할(MIP)을 검색한다. 상태공간은 `2^(2n)`:

| n (units) | 2^(2n) 상태수 | exact 가능? |
|---|---|---|
| 4 | 256 | 🟢 즉시 |
| 8 | 65,536 | 🟢 (M1 한계선) |
| 16 | 4,294,967,296 (≈4.3e9) | 🔴 infeasible |

→ 16채널(또는 16-unit) 전뇌를 **통째로 exact 측정하는 길은 닫혀 있다** (BRAIN.md M1: "IIT4 exact n≤8").

---

## 2. 왜 "16→4-region 평균"은 틀렸나 (coupling 소거)

흔한 단축경로: 16채널을 4 region 으로 묶고 **region 당 1개의 평균신호**로 환원 → 4 super-node → 손쉽게 n≤8. 그러나 이것은 **틀렸다**:

```
   WRONG: 16 → 4-region 평균                HONEST: per-region n≤4 분리

   region R (4 units, 강결합)               region R (4 units, 강결합)
   ┌───┐ ┌───┐ ┌───┐ ┌───┐                 ┌───┐ ┌───┐ ┌───┐ ┌───┐
   │u0 │↔│u1 │↔│u2 │↔│u3 │   ── mean ──▶    │u0 │↔│u1 │↔│u2 │↔│u3 │
   └───┘ └───┘ └───┘ └───┘      collapse    └───┘ └───┘ └───┘ └───┘
     ↕coupling(=irreducibility)              ↑ native 해상도 그대로
          │                                  │
          ▼                                  ▼
       ┌─────────┐                       big_phi(TPM_R, n=4) = exact Φ_R
       │ 1 super │  ← unit 내부 결합이
       │  node R │    평균에 묻혀 사라짐
       └─────────┘    (self-coupled only)
       big-Φ ≡ 0  (자를 part 자체가 없음)
```

평균은 region **내부** unit 간 인과결합을 단일 평균신호 속에 묻어버린다 — 그런데 그 내부 irreducibility 가 바로 big-Φ 가 재려는 양이다. region 을 평균으로 접으면 자를 part 가 없는 1-노드가 되어 **측정 전에 Φ 가 파괴**된다 (BRAIN.md M1: "16ch→4region 평균은 region 내 coupling 을 소거").

**정직한 길** (BRAIN.md M1 의 M2 1차 전략): region 별 native 해상도 유지 → region 마다 `big_phi(TPM, n≤4)` 분리측정. 평균 없음, coupling 소거 없음, 모든 호출 engine-exact.

---

## 3. per-region big-Φ 표 (M1-region vs bypass-region)

**harness**: `AURA/toy/a7_region_split.hexa` (16-unit = 4 region × 4 unit, sys_state=1111, deterministic, $0, hexa-only, LLM 0). 공유 stdlib `iit4_bigphi.hexa` 의 `big_phi` 직접 import (BRAIN/eeg 어댑터와 동일 엔진, g61 engine ⊥ adapter).

| region | connectivity 모형 | n | big-Φ |
|---|---|---|---|
| **M1-region** | 운동출력·국소 self-copy (저결합, 막다른 위치) | 4 | **0.0** |
| **bypass-region** | DLPFC+섬엽 투사허브·다수결 fan-in/out (고결합) | 4 | **17.6639** |
| ΔΦ(bypass − M1) | | | **+17.6639** |
| ~~bypass 평균 super-node~~ (틀린 단축) | 4-unit → 1 평균노드 | 1 | **0.0** (coupling 소거) |

**실행 출력 (verbatim)**:

```
  PER-REGION (honest, n=4 exact):
    M1-region     (motor / local self-copy)   big-Φ = 0.0
    bypass-region (DLPFC+insula hub/majority)  big-Φ = 17.6639
    ΔΦ(bypass - M1) = 17.6639
  AVERAGED SHORTCUT (wrong, bypass -> 1 super-node):
    bypass-region averaged to mean super-node  big-Φ = 0.0
    coupling erased: Φ_avg=0.0 vs Φ_perregion=17.6639
  [PASS] FALSIFIER H: per-region big-Φ(bypass) >= big-Φ(M1)
  [PASS] SHORTCUT WRONG: averaged Φ < per-region Φ (coupling erased)
  [PASS] engine-exact: per-region n<=4 (2^(2n) feasible)
  RESULT: 7 PASS / 0 FAIL
```

→ per-region 측정에서 bypass-region(Φ=17.66) ≫ M1-region(Φ=0.0). 평균 단축경로는 같은 bypass-region 을 Φ=0.0 으로 **파괴** — region 분리측정이 정직한 길임이 in-silico 로 확증.

---

## 4. 사전등록 falsifier + verdict

**검증가능 명제**:
- **H** (relocate-N1 region 판): per-region `big_phi(bypass-region) ≥ big_phi(M1-region)`. 역전이면 H 반증.
- **단축-반박 sub-claim**: bypass-region 을 1 super-node 로 평균하면 Φ 가 파괴된다 (`Φ_avg < Φ_perregion`) → 16→4-region 평균은 틀림.

**등급화 (g5/p7 — hexa verify, perplexity self-judge 금지)**:

```
tier = 🟢 SUPPORTED-NUMERICAL  (external verifier passed AND stdout matches --expect — delegated, deterministic)
claim = AURA A7: per-region IIT4 big-Phi (n<=4 exact, no averaging) — bypass-region big-Phi >= M1-region big-Phi, AND 16->4-region averaging destroys coupling
ext rc = 0
```

verdict verbatim 전문 = `.verdicts/a7-region-split/split.txt`.

---

## 5. honest caveat

- 🟢 는 *numerical*(엔진 재계산 일치)일 뿐 🔵 *formal*(닫힌형 항등식) 아님.
- **region 배정이 synthetic**: 어떤 channel 이 M1-region/bypass-region 인지는 toy 가 임의 가정. 실제 region mask 는 **electrode montage**(채널↔뇌영역 매핑, 예: 10-20 좌표 → ROI)가 있어야 한다.
- connectivity(self-copy vs majority)도 synthetic 모형 — 실제 N1/EEG 측정 0건.
- Φ=17.66 은 **toy 절대값**(n=4, 임의 0.9/0.1 confidence). 주장하는 건 **부호와 순서**(bypass ≫ M1, 평균≪per-region)이지 절대 크기 아님.
- toy substrate ≠ production scale: 실 16ch EEG·실 N1 에서 같은 부호로 transfer 된다는 보장 없음 (BRAIN.md M2 live LSL / M3 상태별 비교 실측 필요).
- region **간** 결합(R4)은 본 toy 범위 밖 — `big_phi_bounded` 류 근사가 후속 (A6 §5 R4).

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| n≤8 exact 한계 · 16ch→4region 평균이 coupling 소거 · per-region n≤4 = M2 1차 전략 | `BRAIN.md` M1 |
| relocate-N1 명제 · M1=국소출력 / bypass=투사허브 | `AURA/SURVEY.md` §2,§3 · `AURA/A6-bigphi-closed-loop.md` |
| big_phi 엔진 (n≤8 exact) | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` |
| toy 하니스 + verdict | `AURA/toy/a7_region_split.hexa` · `.verdicts/a7-region-split/split.txt` |
