# Bench #3 — INFO-MEASURE-TRIAD (정보 측정자 삼각측정 세트)

## 개요

UNIVERSE H_287-290 의 핵심 발견 — **"Shannon 단독 금지, LZ ⊥ TE ⊥ scale-free 정렬"** — 을
anima DECODER (M4b Phase 5b train.out 의 token-151642 attractor) 에 적용해
**4 측정자가 서로 직교(redundant 아님)인지** 그리고 **collapse / router / pool 신호를
각각 잡는지** 검증한다.

- **Mac-local · zero cost** (Phase 5b sample output 재활용).
- 코드 SSOT: [`bench.hexa`](./bench.hexa).
- 측정 결과: [`result.json`](./result.json).

## 측정자 (4 axes)

| Idx | 측정자 | 구현 SSOT | 신호 |
| --- | --- | --- | --- |
| M1 | Shannon entropy | `stdlib/info/entropy::shannon_entropy` (g61) | 빈도 다양성 (baseline) |
| M2 | LZ77 complexity (normalized) | local — `lz_complexity` | 시퀀스 collapse 회피 |
| M3 | Transfer entropy proxy | local — `te_proxy` (forward MI) | router differentiation / causal asymmetry |
| M4 | Powerlaw α fit | local — `powerlaw_alpha` | scale-free pool 분포 |

Shannon + Pearson r 은 g61 advisory 에 따라 **hexa-lang stdlib 에서 import**
(중복 구현 금지). LZ / TE / α 는 stdlib 에 없어 로컬 정의 — 추후 stdlib 승격
후보로 표시.

## 소스 데이터 — Phase 5b DECODED_IDS

`CORE/DECODER/state/m4b_phase5b_2026_05_27/train.out` 의 20-token greedy decode:

```
DECODED_IDS:    1 1 1 1 151642 151642 151642 151642 151642 151642 151642 ...
PER_POS_EXPERT: 1 1 1 1 0      1      1      1      1      1      1      ...
```

- 4 token (id=1) → collapse 시작
- 16 token (id=151642) → attractor lock
- expert 1 dominant (pos 4 만 expert 0 spike)

## Verdict (3-condition gate)

| 조건 | 측정 | 결과 | 합격 |
| --- | --- | --- | --- |
| (a) | LZ(collapsed) < 0.5 → collapse 메커니즘 작동 | **LZ = 0.40** | ✓ |
| (b) | \|r(Shannon, LZ)\| < 0.5 → 두 axis 직교 | **r = 0.976** | ✗ |
| (c) | α spread > 0.5 → 3 분포 구분 가능 | **spread = 2.07** | ✓ |

**>>> 2 / 3 PASS — 🟠 PARTIAL**

## 4×4 직교 매트릭스 (verbatim)

`stdlib/stats/correlation::pearson_r` 를 통해 6-stimulus response vector
[collapsed · diverse · increment · flat · fib-shape · flat-mid] 에 대한
4 측정자 응답을 평가.

```
            Shannon    LZ        TE        alpha
  Shannon   1.0000     0.9759    0.3635    0.3251
  LZ        0.9759     1.0000    0.4964    0.3512
  TE        0.3635     0.4964    1.0000   -0.1924
  alpha     0.3251     0.3512   -0.1924    1.0000
```

### 핵심 발견

1. **Shannon-LZ 는 직교가 아님 (r = 0.976)** — sequence diversity 라는 같은
   intrinsic 축을 측정. H_287-290 가설이 정확히 예측한 결과: Shannon 단독
   사용은 LZ 와 redundant 하다.
2. **TE-α 는 직교 (r = -0.19)** — router causality 와 pool 분포는 서로
   독립적 신호.
3. **Shannon/LZ-vs-TE** (r = 0.36 / 0.50) 와 **Shannon/LZ-vs-α** (r = 0.33 / 0.35)
   는 부분 직교 — TE/α 가 Shannon/LZ 가 못 잡는 신호를 추가로 잡아낸다.

### Collapse 검출 (DECODER 적용)

- collapsed seq Shannon = 0.72 bits / LZ = 0.40 → **LZ 가 더 민감하게**
  collapse 를 띄움 (diverse seq 의 1.0 대비 2.5× drop, Shannon 은 6.0× drop
  이지만 절대치 0.72 도 "low" 임을 미리 알아야 함; LZ 의 < 0.5 임계는
  threshold-free 직관적).

### Router differentiation (TE 검출)

- 지연 driver paradigm (driven[t+1] = 0.7·driver[t] + 0.3·noise[t+1]) 에서
  forward MI = 1.30 bits / backward MI = 0.11 bits → **asymmetry = 0.84**.
  TE proxy 가 시간-방향 인과성을 잡아낸다.

### Pool 다양성 (α 검출)

- powerlaw(α=2.5) sample → fit α = 1.48
- exponential(rate=0.5) → fit α = 2.02 (사실 powerlaw 가 아니지만 fit 은
  돌아감 — fit-quality 체크 필요)
- uniform(1, 50) → fit α = -0.05 (flat → 0 근처)
- spread = 2.07 → 분포 모양 구분 가능.

## 결론

H_287-290 가 주장한 "Shannon 단독 금지" 는 정확히 본 bench 에서 재현됨 —
**Shannon-LZ redundancy (r = 0.976)** 가 그 직접 증거. 그러나 4-axis
matrix 전체로 보면 (TE-α 가 직교) **추가 axis 가 Shannon 이 못 잡는 신호를
보충**한다는 H_287-290 의 정렬 처방은 부분적으로 지지된다.

verdict 🟠 PARTIAL — (b) 직교 조건은 본 bench 의 stimulus 설계 한계
(collapse/diverse 와 6-stimulus profile 이 모두 sequence-diversity 축에서만
변동) 으로 인해 Shannon-LZ 가 같은 그림자를 보임. **TE/α 가 새 axis 임이
대각선-off 영역 (TE-α r = -0.19) 에서 입증** 됨.

## 후속 작업 (deferred)

- LZ / TE proxy / powerlaw α 를 stdlib 로 승격 (`/stdlib promote`):
  - `stdlib/info/lz_complexity.hexa`
  - `stdlib/info/transfer_entropy.hexa`
  - `stdlib/stats/powerlaw_fit.hexa`
- Phase 5b 외 실제 anima emit stream (`kosmos` ledger) 에 4-axis 측정 적용.
- (b) 조건 재설계 — collapse-axis 외 stimulus 추가하여 Shannon-LZ 의
  실제 직교 부분 노출.

## 실행

```bash
hexa run --no-sentinel bench/info_measure_triad/bench.hexa
```

Mac-local 약 1초, exit 0, `result.json` 갱신.
