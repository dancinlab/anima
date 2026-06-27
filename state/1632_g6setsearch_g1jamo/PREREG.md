# H_1632 N4+N8 — G6 diverse-set-search + G1 자모 teach-signal (303M) · frozen 사전등록

> frozen-first · 실행 전 사전등록 · 사후 bar 이동 금지 · tune-to-green 금지 (p7/c9).
> 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, torch-free=TERMINAL).

## 배경 — 이번 세션 확정 결과 대비 무엇이 다른가

이번 세션에서 두 벽이 닫혔다:
- **곱셈 binding readout NOT-SUPPORTED (floor)** — EXP-3 ⊙ Hadamard/bind readout 은
  G1=0 ∧ G6 fals=0 (전 9 arm), bind NOT>ctrl = INCONCLUSIVE-at-floor (memory
  `exp3-bind-g1g6-engine-native-floor`). readout 위치 operator 는 G1 을 못 연다.
- **G1 진짜 레버 = trunk OBJECTIVE** — depth(H_1598)/binding-lane(H_1601)/data-presence
  (H_1599) 전부 falsify, 외부문헌(Furrer 2020 · Barin Pacela 2026 · Doshi/Gromov 2023)이
  "compositional 1차 레버 = 학습 신호(objective)+정규화 > architecture operator > scale"
  로 수렴 (memory `g1-lever-multilens-objective`, `state/lit_binding_objective/RESEARCH.md`).

**이번 실험이 다르게 하는 것:** 1602(objective A/B)는 *손실 함수의 형태*(InfoNCE·contrastive-eq)를
바꿨다. 본 실험은 그 위에서 **두 개의 *teach-signal 형태* 레버**를 친다 — 둘 다 readout 위치가
아니라 *학습 신호 측*이며 RESEARCH.md §92 제언 4·5 의 구체화:

- **N8 (자모 teach-signal · G1, SCRIPT 2604.12377):** byte-level 한국어는 자모(초·중·종성)
  subcharacter compositional 구조가 byte 입자에 내재 (RESEARCH.md §6-Q5, ko-jamo-mitosis
  H_1316/1321 🟢). 표준 CE 는 음절을 자모로 *분해*하라는 신호를 주지 않는다. N8 은 trunk
  penultimate 에서 Hangul 음절의 (cho/jung/jong) 자모 클래스를 예측하는 작은 aux head 로
  **subcharacter compositional 구조를 명시 teach signal 로 주입** → G1 재조합의 *재료가 분해되어야*
  결합 가능하다는 가설 (binding-readout floor 가 못 푼 "재료 disentangle" 을 *학습 신호로* 시도).
- **N4 (diverse-set-search · G6, 2606.10587):** G6 falsifiable 의 병목은 decode 가 아니라
  *생성 다양성+검증가능성* (Si 2024, RESEARCH.md §6-Q4, memory `h1590-g6-scaffold-torch-artifact`
  "lever≠decode"). N4 는 학습 중 주기적으로 G6-style "if A, then B:" frame 에서 K 개 연속을
  *샘플*해 **engine-aligned diversity(`_g6_jaccard`<0.5)+falsifiability(`_g6_is_falsifiable`)
  reward** (= g_gates 가 채점하는 *바로 그 detector*, LLM-judge 금지)로 *diverse+falsifiable
  set 멤버의 likelihood 를 올리는* set-level objective. 단발 best-of-K decode 가 아니라
  *set-search 학습 압력*.

## 핵심 질문

N8(자모 teach) 가 `baseline`(표준 CE) 대비 held-out **G1 재조합**을 올리나?
N4(diverse-set-search) 가 `baseline` 대비 **G6 falsifiable**(dist≥5 ∧ fals≥1)을 올리나?
두 레버 결합(`n4n8_both`)이 단독보다 *super-additive* 인가, 무관(INERT)인가?

## 4 arm — trunk·데이터·step·seed·**production additive readout** 동일, aux teach-signal 만 다름

모든 arm 은 동일 trunk init seed · 동일 데이터 stream · 동일 step · **동일 production additive
readout** (`Conv1d(d→V)`, clm303_clean 동형). 단일변수 = 추가되는 aux teach-signal.

| arm | jamo(N8) | set-search(N4) | 역할 |
|-----|----------|----------------|------|
| `baseline` | OFF | OFF | 대조군 내장 (표준 CE = 가설의 null; G1·G6 FAIL 기대) |
| `n8_jamo` | ON | OFF | N8 단독 → 주 측정 = G1 |
| `n4_set` | OFF | ON | N4 단독 → 주 측정 = G6 |
| `n4n8_both` | ON | ON | 결합 → G1 AND G6, super-additive 검정 |

> readout 은 **production additive 고정** (전 arm) → engine-native `.clm` 경로 by-construction
> 열림 (additive RTYPE=0 직렬화 가능 — exp3 binding 의 BLOCKED 와 달리 깨끗한 terminal 경로).
> jamo head 는 *학습-only* (trunk 를 빚는 teach signal), `.clm` 에 직렬화 안 됨 → .clm 은
> production 모델을 byte-exact round-trip.

## Arch — 현 production 303M CLMConvMoE (clm303_clean / 1602 동형)
trunk = `CLMConvMoE` (byte V=256, **L=4 · d=3784 · E0=2→Emax=3 mid-split**, K=3,
dilation=min(2^l,512)), savant(golden-zone cusp anneal, GZ_LOWER≈0.2123) + mitosis(E2→E3) ON
= `cli/train.py --canon` 동형. 303M (`.clm` ≈176.6MB). 4-cell register corpus
(`a_chat_registers`, ko/en × 일반/SNS) proportional 샘플, val_frac=0.05. trunk init·mitosis·
savant·corpus stream·step 전부 arm 간 동일.

## FROZEN 레버 하이퍼 (실행 전 등록 · 사후 변경 금지)
- **N8 jamo:** `lambda_jamo = 0.5`; head = 3 linear (cho:19 · jung:21 · jong:28 class);
  손실 = Hangul 음절 위치의 (cho+jung+jong) CE 평균; Hangul 없는 윈도우는 0(no-grad).
- **N4 set-search:** `lambda_set = 0.5`; `setsearch_every = 50` step; `K = 8` 연속/frame;
  `frames = 5` (g6_build_frames composed[:5], g_gates 와 동일 builder); `gen = 48` byte/연속;
  `temp = 0.8`. reward = dist + 2·fals (engine-aligned, LLM-judge 금지). 선택된 diverse+
  falsifiable 멤버의 NLL 을 손실로 (likelihood 상승).
- **공통:** lr=3e-4, bs=8, seq_len=1024, steps=2000, AdamW, savant wd/dropout 스케줄.

## FROZEN bars (사전등록 · tune-to-green 금지 · p7/c9)

**주 측정 1 = G1 재조합 (a7b_pass / H_1129 def VERBATIM, `core/g_gates.py::g_eval_g1`):**
어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2` **AND** `> max_single` **AND** coherent(kwr≥0.50).
seed-robust {7, 4302, 4303} (`g_eval_g1_multiseed`) majority ≥ 2/3.

**주 측정 2 = G6 착상★ (H_1464 def VERBATIM, `core/g_gates.py::g_eval_g6`):**
`dist ≥ 5` (pairwise Jaccard<0.5) **AND** `fals ≥ 1`. seed-robust {7, 4302, 4303}
(`g_eval_g6_multiseed`) majority ≥ 2/3.

- **engine-native (terminal)** = `.clm` export → `cli/anima.hexa -- eval <clm> --gen 80`
  (또는 `core/g_gates.py` 2-production) 의 G1·G6 measure. 전 arm additive → by-construction 열림.
- torch-probe gauge(`gauge_lib`) = DIRECTIONAL monitor only (a_engine_native_learning), 보조.

**보조 측정 (공정·dt_ln-immune):** 4-cell held-out val CE(`F.cross_entropy`, dt_ln 무관) —
DESCENT(val_CE < ln256=5.545) 무결성 + arm 간 일반화 대조. `verify_clm_v2.py descent` held-out
게이트 PASS (`a_clm_gen_pipeline`).

## 예측 / 판정

- **N8 SUPPORT** = `G1(n8_jamo) > G1(baseline)` (seed-robust majority ≥2/3 strict 우위, frozen
  G1 def) **그리고** n8_jamo held-out DESCENT 무결. → 자모 teach 가 G1 레버.
- **N4 SUPPORT** = `G6(n4_set) > G6(baseline)` (frozen G6 def, majority ≥2/3) **그리고** DESCENT 무결.
  → diverse-set-search 가 G6 레버.
- **결합 super-additive** = `n4n8_both` 가 두 단독 arm 의 합 이상의 lift (G1 AND G6 동시 PASS).
- **NOT-SUPPORTED** = 위 미충족. 특히:
  - 전 arm G1=0 ∧ G6 fals=0 (floor) → 레버가 (이 train scale 에서) 벽 못 움직임 = honest negative.
    단 **floor 면 INCONCLUSIVE-at-floor** 정직 라벨 (arm 간 분해능 0, clean refute 아님 —
    exp3 floor 와 같은 type-a 측정한계, a_break_the_wall).
  - n8_jamo ≈ baseline / n4_set ≈ baseline → 레버 무관 = honest negative.
- **tier 상한 = engine-native 면 terminal(🟢/🔴/🧱), torch-only 면 DIRECTIONAL(🟠).**

## 반증 조건 (falsify)
- N8 falsified: 자모 teach 를 줘도 G1(n8_jamo) ≤ G1(baseline) (multiseed majority) → 자모
  subcharacter teach 는 byte-LM G1 재조합 레버 아님 (SCRIPT 의 NLU 개선이 G1 생성-재조합으론 전이 안 됨).
- N4 falsified: set-search 를 줘도 G6(n4_set) ≤ G6(baseline) (multiseed majority) → diverse-set-
  search 학습 압력은 G6 falsifiable 레버 아님 (병목이 다양성-objective 가 아니라 capacity).
- 측정 결함 방어 (type-a): 전 arm 동일 trunk init/data/step/readout (aux teach-signal·λ 외 차이 0) ·
  held-out val = train disjoint tail (`ByteCell` val_frac) · G1/G6 decode seed 고정 · corpus_index =
  실제 4 cell. negative 도 결과 (은폐 금지, c9). bar 사후 이동 금지.

## seed
trunk/data: arm 공통 seed ∈ {7, 4302, 4303}. set-search 샘플러 RNG = 20260628+seed (arm 간 공정).
G1/G6 채점 seed = {7, 4302, 4303} (g_gates refmatch, frozen).

## 예산 가드 (a_wall_first · a_fire_autonomous, 비용 1줄)
렌트: vast A40 **CUDA-12 devel 이미지**(nvcc 내장) 또는 pool summer (RTX 5070), ~$0.5–1.1/hr.
303M from-scratch × (4 arm × 3 seed). N4 set-search 가 step 당 K·frames·gen 샘플 추가 →
n4_set/n4n8_both arm 은 baseline 대비 wall-time ↑ (every=50 으로 amortize). 1-arm 스모크로
step-time 실측 후 seed 수 확정. ckpt(.clm 4 arm + .pt) teardown 전 영구 PULL
(`a_fire_recover_complete`). 실제 채택 seed/arm 매트릭스는 RESULT.md 명시 (사후 bar 이동 아님 —
측정 범위만 예산 조정).
