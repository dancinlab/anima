# H_1602 RECOMB-OBJECTIVE (303M) — frozen pre-registration

**가설:** G1 재조합벽의 진짜 레버는 트렁크 학습 **OBJECTIVE** 다 — 표준 CE(next-byte
marginal likelihood)는 *조합(conjunction) 표현을 보상하지 않으므로* 어떤 depth/binding-lane/
data 를 줘도 G1(재조합)을 못 올린다. depth(H_1598)·binding-lane(H_1601)·data-presence(H_1599)
는 전부 falsify 됨(memory `g1-lever-multilens-objective`). 남은 단 하나의 후보 = trunk OBJECTIVE.
cheap probe(brainarch-top3, $0 numpy)는 objective-lever SUPPORT 0 이나 **under-power**(toy 가
어떤 objective 로도 grok 못 함, H_1792 grok ctrl chance = type-a 측정 한계, 천장 아님) → 303M
engine-native 만이 terminal.

**핵심 질문:** contrastive/InfoNCE objective 가 `ce_marginal`(표준 CE baseline) 대비 held-out
재조합(G1)을 *올리나*?

## 3 arm — trunk·데이터·step·seed 동일, **OBJECTIVE 만 다름**

세 arm 은 **동일 trunk init seed · 동일 데이터 stream · 동일 step · 동일 production additive
readout**(`Conv1d(d→V)`, clm303_clean 동형 — binding 변수 제거). 단일변수 = 학습 objective.

- **`ce_marginal`** (baseline / discriminating control): 표준 CE next-byte marginal likelihood.
  likelihood 는 맑게 내려가되 G1 FAIL 기대 = **대조군 내장**(CE 가 합성을 보상 안 함 = 가설의 null).
- **`infonce`**: InfoNCE/contrastive predictive objective. 각 position 의 모델 예측 분포를 정답
  byte(positive) vs corpus 에서 뽑은 negatives 와 contrast (predictive-coding). H_1792 toy 직접검정의
  303M 판. CE term + λ·InfoNCE term (λ frozen=1.0).
- **`contrastive_equilibrium`**: contrastive equilibrium-prop 류 (H_1721) — 정답 시퀀스(positive
  phase)와 모델-생성/섞은 시퀀스(negative phase)의 energy(−loglik) 차를 벌리는 objective. 조합을
  표현하지 않으면 negative phase 를 못 밀어내도록(conjunction 없이 최소화 불가) 설계. CE term +
  λ·(E_pos − E_neg)_+ margin (λ frozen=1.0, margin frozen=0.5).

> readout 은 **production additive 고정**(세 arm 전부) → objective 단일변수 격리 + **engine-native
> `.clm` 경로 by-construction 열림**(ce_marginal/infonce/contrastive 전부 additive RTYPE=0 직렬화
> 가능 — exp3 binding 과 달리 BLOCKED 아님 = 이게 binding 보다 깨끗한 terminal 경로).

## Arch — 현 production 303M CLMConvMoE (clm303_clean 동형)
trunk = `CLMConvMoE` (byte V=256, **L=4 · d=3784 · E0=2→Emax=3 mid-split**, K=3,
dilation=min(2^l,512)), savant(golden-zone inhibition cusp anneal) + mitosis(E2→E3) ON =
`cli/train.py --canon` 동형. 4-cell register corpus(`a_chat_registers`, ko/en × 일반/SNS)
proportional 샘플, val_frac=0.05. trunk init·mitosis·savant·corpus stream·step 전부 arm 간 동일.

## FROZEN bars (실행 전 사전등록 · tune-to-green 금지 · p7/c9)

**주 측정 = G1 재조합 (a7b_pass / H_1129 def VERBATIM):**
어떤 k∈{2,3,4,5} 에서 `composed_distinct ≥ 2` **AND** `> max_single` **AND** coherent(kwr≥0.50).
seed-robust {7, 4302, 4303} majority ≥ 2/3.
- **engine-native (terminal)** = `.clm` export → `anima eval` (또는 `clm_decode.py` 2-production)
  의 G1 measure. 세 arm 전부 additive → engine-native by-construction 열림.
- torch-probe gauge(`gauge_lib`) = DIRECTIONAL monitor only (a_engine_native_learning), 보조.

**보조 측정 (공정·dt_ln-immune):** 4-cell held-out val CE(`F.cross_entropy`, dt_ln 무관) —
DESCENT(val_CE < ln256=5.545) 무결성 + arm 간 일반화 대조.

- **SUPPORT** = `G1(infonce) > G1(ce_marginal)` **OR** `G1(contrastive_equilibrium) > G1(ce_marginal)`
  (seed-robust majority ≥2/3 에서 strict 우위, frozen G1 def) **그리고** 그 arm held-out DESCENT 무결.
  → objective 가 G1 레버. ce_marginal(CE-only)이 G1 FAIL 이고 contrastive arm 이 PASS 면 가설 confirm.
- **NOT-SUPPORTED** = 위 미충족. 특히:
  - 전 arm G1=0 (floor) → objective 가 (이 train scale 에서) 재조합벽 못 움직임 = honest negative.
    단 **floor 면 INCONCLUSIVE-at-floor** 정직 라벨(arm 간 분해능 0, clean refute 아님).
  - contrastive ≈ ce_marginal → objective 무관 = honest negative.
- **tier 상한 = engine-native 면 terminal(🟢/🔴/🧱), torch-only 면 DIRECTIONAL(🟠).**
  세 arm 동일 measure = 공정. floor caveat = type-a 측정한계(a_break_the_wall).

## 예산 가드 (a_wall_first · a_fire_autonomous, 비용 1줄)
렌트: vast A40 **CUDA-12 devel 이미지**(nvcc 내장), ~$0.5–1.1/hr. 303M from-scratch ×
(3 arm × seeds). exp3 실측 ≈ 20분/arm @ A40 100% util → 9 run(3×3) ≈ 3h ≈ $3–6.
1-arm 스모크로 step-time 실측 후 seed 수 확정:
- 9 run(3×3 seeds) ≲ ~$8 → full {7,4302,4303} × {ce_marginal,infonce,contrastive_equilibrium}.
- 초과 시 fallback = {7,4302,4303} × {ce_marginal,infonce} = 6 run (contrastive 는 seed7 1회).
실제 채택 seed/arm 매트릭스는 RESULT.md 명시(사후 bar 이동 아님 — 측정 범위만 예산 조정).

## 측정 결함 방어 (a_break_the_wall type-a) · 정직(c9)
- 세 arm trunk init/data/step/readout 동일(objective·λ 외 차이 0) · held-out val = train disjoint tail
  (`ByteCell` val_frac) · G1 decode seed 고정 · corpus_index = 실제 4 cell.
- negative(NOT-SUPPORTED)도 결과 — objective 가 G1 레버 아니면 honest negative 박제(g1-lever 다중렌즈
  종결 방향). bar 사후 이동 금지.
- engine-native 우선(.clm/py 2-production = terminal) · torch-only = DIRECTIONAL 정직 라벨.
- ckpt(.clm 3 arm + .pt) teardown 전 영구 PULL(`a_fire_recover_complete`).
